# -*- coding: utf-8 -*-
"""`read` 스테이지 — D5 5단계 독해 실행 경로.

계약 = `contracts/stages/read.yaml`(정본 서술 = SPEC §1.4 + §1.5 CP1).

실행 순서(재정 P-4 · P-A · P-C · P-U3 · P-U4 · P-B · T16 — SPEC §1.4).

```
① 진입 지문 검사(P-C)                      → 불일치면 StageEnvironmentError(재시도 아님)
② read-a.decompose · read-b.decompose      → 분해 **2회**. 여기까지만 2회다.
③ 맹검 스크리닝 메모 2건 수집(P-A·P-U4)    → 섀도 원장(런 밖)에 한 행으로 등재
④-a 조기 청구항 소유 검사(T16, 실행별)      → claim-inventory · dependency-parse
④-b 조기 수렴 검사(P-4·T16)                 → ④-a 실패 시 보류 · phase: "early"
⑤ 정본 지정(P-4)                           → read_runs[0]. 내용맹·결정론. 품질 비교 금지.
⑥ 접지 진입 게이트(P-U3·T17)               → 판정서 존재 ∧ (통과 ∨ 상신 축 Owner '계속' 봉투)
⑦ 접지 → 수확(P-B) → 통합                  → **정본 1개만**
⑧ 조립 → 검사 전건 → convergence.json (phase: "full")
⑨ 출구 검사 + read.lane-log-shape          → 비정본 실행에 접지·통합 레인이 **없음**을 판정
⑩ CP1 상신물 — 판독본·중간 산출물
```

순서가 이렇게 생긴 이유는 하나다. **수렴이 통과하면 두 독해는 동치로 선언되고, 동치인 것을
두 벌 접지하는 것은 지출이다.** 반대로 수렴이 깨졌다면 그 사실은 접지 지출 **전에** 드러나야
한다 — 그것이 조기 수렴 이동(P-4)이고, 접지 진입을 판정서에 결속한 것(P-U3)이 그 이동을
관습이 아니라 기계 강제로 만든다. 정본 1개만 진행했다는 사실은 **레인 로그에 없음으로**
증명된다.

★ 재시도 예산은 **판정점별**이다(재정 2026-09-01 T16): 조기는 read_run 별 1회이며 결함
실행만 다시 분해하고, 출구는 런 전역 정본 후속 1회다. 구 판의 런 전역 슬롯은 먼저 도착한
판정점이 뒤 판정점의 기회를 없애는 우선권으로 작동했으므로 폐기되었다.

검사 구현은 여기 없다(이식 단위 `reader/lib` 안에 있다). 감춰진 예외는 예외가 아니라 은폐다.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from datetime import datetime, timezone

from jsonschema import Draft202012Validator

from reader.lib import (
    CHECK_REGISTRY,
    READ_CHECK_IDS,
    run_early_claim_checks,
    run_read_checks,
    to_convergence_payload,
)
from reader.lib.harvest import harvest_numeric_facts
from reader.lib.report import CheckContext, CheckRow
from reader.lib.rules import Rules
from reader.lib.spec_io import load_schema

from . import (
    StageEnvironmentError,
    StageError,
    failure_row_of_kind,
    failure_rows_for_checks,
    findings_of,
    load_json,
    load_yaml,
    read_text,
    sha256_bytes,
    sha256_file,
    select_failure_row,
    terminal_action,
    verify_declared_inputs,
    write_json,
    write_text,
)
from ..lanes.contract import (
    REQUEST_MD,
    LanePending,
    LaneRequest,
    LaneResponse,
    LaneStaleResponseError,
)
from ..lanes.plan import (
    harvest_band_start,
    lane_profiles,
    plan_decompose,
    plan_grounding,
    plan_synthesis,
)
from ..paths import (
    SHADOW_LEDGER_RELATIVE,
    RunPaths,
    ShadowLedgerRootError,
    reader_version,
    repo_root,
    shadow_ledger_root,
    shadow_screening_ledger,
)
from ..read_view import ReadView
from ..render.material_spec_md import render
from .freeze import parse_envelope

STAGE_ID = "read"
CONVERGENCE_SCHEMA = ("contracts", "schemas", "convergence.schema.json")
APPROVAL_SCHEMA = ("contracts", "schemas", "approval-envelope.schema.json")
CONVERGENCE_CHECK_ID = "read.convergence"
LANE_LOG_SHAPE_CHECK_ID = "read.lane-log-shape"
LANE_LOG_DIGEST_VALUE_CHECK_ID = "read.lane-log-digest-value"

# ★ 엔진 소관 검사 id 의 단일 목록(재정 2026-08-31 Q1 의 집행 형태).
#
#   재정 Q1 은 새 검사 id 를 *"`contracts/glossary.md` §2.1 목록과 `CHECK_REGISTRY` 에
#   **동시에** 등재한다(대조를 시험이 집행한다)"* 로 명했다. 그런데 `CHECK_REGISTRY`
#   (`reader/lib/run_checks.py`)는 **이식 단위의 등재부**이고 그 항목은
#   `CheckContext(spec, peer_spec, rules)` 만 받는다 — 파일 시스템도 레인 디렉터리도 보지
#   못한다. 신설 검사는 디스크의 `request.md` 를 **실제로 읽어야** 성립하므로 그 등재부에
#   들어갈 수 없다(형제 검사 `read.lane-log-shape` 가 엔진 소관인 것과 같은 이유다).
#
#   그래서 재정이 요구한 **효과**(등재 누락을 시험이 잡는다)를 자리만 옮겨 세운다. 이 튜플이
#   엔진 소관 검사의 등재부이고, `tests/test_m1_corpus.py::test_glossary_registers_every_check_id`
#   가 `CHECK_REGISTRY` 와 **이 목록을 함께** 훑는다. 구 시험은 이식 단위 등재부만 보았으므로
#   엔진 검사 id 는 사전에서 빠져도 아무도 울지 않았다 — 재정 문언의 축소가 아니라 확장이다.
#
#   ★ 여기 없는 엔진 검사는 `source.*`·`freeze.*` 다. 그 둘은 각자의 스테이지 모듈이 소유하며
#   이 목록은 **READ 스테이지의 엔진 소관분**만 든다(`read.input-digest` 는 스테이지 공통
#   진입 검사라 `engine/stages/__init__.py` 가 발행한다).
ENGINE_READ_CHECK_IDS: tuple[str, ...] = (
    LANE_LOG_SHAPE_CHECK_ID,
    LANE_LOG_DIGEST_VALUE_CHECK_ID,
)
RETRY_POINT_IDS = ("early", "exit")
# 승인된 재시도 집합(재정 T26 ⓐ ③·T28 β·T25). 계약이 다르면 계약이 틀린 것이다.
EARLY_RETRY_CHECK_IDS = (
    "read.claim-inventory",
    "read.dependency-parse",
    "read.convergence",
)
EXIT_RETRY_CHECK_IDS = (
    "read.schema",
    "read.claim-inventory",
    "read.dependency-parse",
    "read.verbatim",
    "read.pointer-resolve",
    "read.coverage",
    "read.value-derivation",
    "read.bibliography",
)
CONTINUE_CHECKPOINT = "convergence_continue"
PHASE_GATE_NONE = "none"
PHASE_GATE_CLAIM_CHECKS = "claim-checks"
PHASE_GATE_EXACT_MATCH = "convergence-exact-match"
ENVELOPE_SCOPE = ("convergence-escalation",)
PHASE_GATE_ESCALATION = ENVELOPE_SCOPE[0]


class LaneAssignmentError(StageError):
    """레인이 요청과 다른 모델·effort 로 돌았다(조용한 대체 금지 — SPEC §7.3 규율 4)."""


class RunnerContractError(StageError):
    """러너가 READ 계약의 예산·산출 서식을 이행할 수 없을 때 거부한다."""


# ---------------------------------------------------------------------------
# 레인 왕복 기록
# ---------------------------------------------------------------------------


class LaneJournal:
    """전 요청·응답의 배정 기록. `10-read/lanes/lane-log.json` 의 본문이 된다.

    행이 드는 것은 두 켤레다. **모델·effort 병기**(요청 ↔ 실호출)가 조용한 대체를 드러내고,
    **지문 4종**(요청 지문 ↔ 반향 ↔ 요청 파일 지문 ↔ 응답 파일 지문)이 시점 결속을 드러낸다
    (재정 P-12 · 재정 2026-08-19 S4). 뒤엣것은 앞엣것의 확장이지 대체가 아니다 — 두 병기가
    답하는 질문이 다르다: "누가 답했는가"와 "무엇에 대해 답했으며 그 답이 지금도 그 파일인가".

    ★ `request_digest`(재정 2026-08-19 S4 · Q8 ③ 승인)는 `response_digest` 의 **거울상**이다.
    응답 쪽만 파일 바이트를 재던 동안, 왕복의 다른 끝인 요청서는 사후에 대조할 근거가 없었다 —
    레인이 읽은 요청서가 지금 그 자리의 파일과 같은지 로그가 말하지 못했다. 값은
    `sha256(request.md)` 이며 사람이 `sha256sum request.md` 로 곧장 맞춰 본다.
    """

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def record(
        self,
        request: LaneRequest,
        response: LaneResponse | None,
        *,
        request_digest: str | None = None,
    ) -> None:
        """왕복 1건. `request_digest` = 레인이 읽은 `request.md` **파일 바이트**의 sha256.

        `None` 은 "요청 파일을 **쓰지 않는 어댑터**로 돌았다"는 사실이다(재생 어댑터 — 응답
        트리만 읽고 요청을 쓰지 않는다). 그 사실을 지어내지 않고 그대로 적으며, 판정
        (`lane-log.request-file-digest`)은 그 행을 대상에서 빼되 **몇 건을 뺐는지 산출에 남긴다**.

        ★ 요청 파일을 **쓰는** 어댑터가 그 파일을 읽지 못한 경우는 `None` 이 아니라 빈
        문자열이며, 그것은 면제가 아니라 결함으로 판정에 걸린다(`_request_file_digest`).
        """
        mismatch = response is not None and response.mismatches(request)
        digest_ok = response is not None and response.input_digest == request.input_digest
        self.rows.append(
            {
                "lane_id": request.lane_id,
                "read_run": request.read_run,
                "task": request.task,
                "batch": request.batch,
                "requested_model": request.model,
                "requested_effort": request.effort,
                "actual_model": response.model if response else None,
                "actual_effort": response.effort if response else None,
                # 시점 결속 3종(재정 P-12). `response_digest` 는 러너가 **실제로 소비한
                # 파일 바이트**의 지문이며, 사후에 `sha256sum response.json` 과 대조된다 —
                # 값이 갈리면 소비 이후 그 파일이 바뀐 것이다(감수 OOS-02 가 실증한 사고).
                "input_digest": request.input_digest,
                "echoed_digest": response.input_digest if response else None,
                # 요청 파일 바이트의 지문(재정 2026-08-19 S4 · Q8 ③) — 응답 쪽의 거울상이다.
                "request_digest": request_digest,
                "response_digest": response.response_digest if response else None,
                "digest_ok": digest_ok,
                "rejected": False,
                "reason": None,
                "ok": response is not None and not mismatch,
                "mismatch": mismatch,
            }
        )

    def record_rejected(
        self,
        request: LaneRequest,
        *,
        echoed: str,
        reason: str,
        request_digest: str | None = None,
    ) -> None:
        """러너가 **거부한** 응답의 행(재정 P-12 ③④).

        거부는 소비하지 않은 사건이므로 실호출 모델도 응답 지문도 없다 — 남는 것은 "무엇을
        요청했고 무엇이 반향되었으며 왜 물렸는가"다. 이 행이 없으면 거부는 예외 메시지로만
        존재하고 런 폴더에는 아무 흔적도 남지 않는다. 재정 ③이 요구한 것이 바로 그 흔적이다.
        """
        self.rows.append(
            {
                "lane_id": request.lane_id,
                "read_run": request.read_run,
                "task": request.task,
                "batch": request.batch,
                "requested_model": request.model,
                "requested_effort": request.effort,
                "actual_model": None,
                "actual_effort": None,
                "input_digest": request.input_digest,
                "echoed_digest": echoed,
                "request_digest": request_digest,
                "response_digest": None,
                "digest_ok": False,
                "rejected": True,
                "reason": reason,
                "ok": False,
                "mismatch": False,
            }
        )

    def mismatched(self) -> list[dict]:
        return [row for row in self.rows if row["mismatch"]]


def _request_file_digest(adapter, request: LaneRequest) -> str | None:
    """어댑터가 쓴 `request.md` 파일 바이트의 지문 — 능력이 없는 어댑터면 `None`(재정 2026-08-19 S4).

    능력 조회(`getattr`)로 묻는 이유: 요청을 **쓰지 않는** 어댑터가 있다(재생 어댑터는 미리
    준비된 응답 트리만 읽는다). 그 경로에 요청 파일 지문을 요구하면 없는 파일을 지어내야 하고,
    지어낸 지문은 없느니만 못하다. 값이 없다는 사실은 `None` 으로 그대로 적히며 판정이 그
    행을 대상에서 뺀다 — 무엇을 뺐는지는 판정 산출에 남는다.

    ★ **`None` 은 능력의 부재만을 뜻한다**(2026-08-19 보수 — 감수 C′-2 NEW BLOCKER ①).
    구 코드는 능력이 **있는** 어댑터의 읽기 실패(`OSError`)도 `None` 으로 접었고, 판정은 그
    `None` 을 **면제**로 셌다. 그래서 파일 어댑터가 쓴 `request.md` 가 사라지거나 읽히지
    않아도 `lane-log.request-file-digest` 가 한 건도 울지 않았다 — 면제의 뜻이 "그 어댑터는
    요청 파일을 쓰지 않는다"에서 "요청 파일을 못 읽었다"로 조용히 넓어져 있었다.

    능력이 있는데 읽기가 실패하면 그것은 면제가 아니라 **결함**이다. 그래서 빈 문자열을
    돌려주어 판정에 걸리게 한다(`""` 는 "칸은 있는데 값이 없다" — 판정이 그 형태를 이미
    구별한다). 여기서 예외를 다시 던지지 않는 이유는 그대로다: 던지면 그 사실이 로그에 닿기
    전에 런이 죽고, 무엇이 왜 없었는지가 런 폴더에 남지 않는다. **이것은 판정 관할을 넓히는
    것이 아니라 잘못 넓혀진 면제를 좁히는 것이다** — 새로 보기 시작한 대상이 없고, 면제로
    세던 것을 결함으로 되돌릴 뿐이다.
    """
    probe = getattr(adapter, "request_md_digest", None)
    if probe is None:
        # 능력의 부재 = 면제. 이 한 갈래만 `None` 이다.
        return None
    try:
        return probe(request)
    except OSError:
        return ""


def _dispatch(adapter, requests: list[LaneRequest], journal: LaneJournal) -> list[LaneResponse]:
    """배치 1개를 보내고 배정 기록을 남긴다. 응답 순서는 요청 순서에 맞춘다.

    낡은 응답은 **기록한 뒤 다시 던진다**(재정 P-12 ④). 던지기만 하면 런이 죽으면서 거부
    사실이 함께 사라지고, 기록만 하면 오염된 응답이 조립까지 흘러간다. `run()` 의 `finally`
    가 레인 로그를 쓰므로 이 행은 런 폴더에 남는다.

    요청 파일 지문은 **어댑터에서 얻는다**(재정 2026-08-19 S4). 그 값을 아는 것은 파일을 쓴
    당사자뿐이며, 러너가 경로를 다시 조립해 재면 두 곳이 같은 규칙을 두 벌 갖게 된다.
    """
    try:
        responses = adapter.dispatch(requests)
    except LaneStaleResponseError as exc:
        stale = {request.lane_id: request for request in requests}.get(exc.lane_id)
        if stale is not None:
            journal.record_rejected(
                stale,
                echoed=exc.actual,
                reason=str(exc),
                request_digest=_request_file_digest(adapter, stale),
            )
        raise
    by_id = {response.lane_id: response for response in responses}
    ordered: list[LaneResponse] = []
    for request in requests:
        response = by_id.get(request.lane_id)
        journal.record(
            request, response, request_digest=_request_file_digest(adapter, request)
        )
        if response is None:
            raise StageError(f"레인 응답이 요청과 짝지어지지 않았다: {request.lane_id}")
        ordered.append(response)
    return ordered


# ---------------------------------------------------------------------------
# 조립
# ---------------------------------------------------------------------------


# ★ 항목 ID 재번호 (2026-08-18 sol 재감수 B-01 의 처분).
#
# 레인에게 나눠 준 1000 폭 대역(`engine/lanes/plan.py`)은 **작업용 임시 번호**다. 그것을
# 그대로 이어 붙이면 조립본에 결번 1958 개가 남고, `lifecycle.id-contiguous` 가 요구하는
# `M1..Mn` 연속을 만족하지 못해 **정상 산출을 동결할 수 없다**. 대역(예방)과 연속성(계약)이
# 정면으로 충돌했고, 고칠 쪽은 대역이다 — 연속성을 버리면 "항목 하나가 사라졌다"의 신호가
# 함께 사라진다(SPEC §2.4 · §2.8 제약 6).
#
# 그러므로 최종 `M<n>` 은 **엔진이 소유한다**. 레인은 자기 응답 안에서만 쓰는 번호를 쓰고,
# 조립기가 투입 순서대로 `M1` 부터 다시 매긴 뒤 참조 전량을 같은 표로 고쳐 쓴다.
ID_MAP_BASENAME = "id-map.json"
DECOMPOSE_LANE = "decompose"
HARVEST_LANE = "harvest"
SYNTHESIS_LANE = "synthesize"


def lane_payloads(
    decompose: dict,
    groundings: list[dict],
    synthesis: dict,
    harvest: dict | None = None,
) -> list[tuple[str, dict]]:
    """레인 투입 순서 그대로의 `(lane_key, payload)`. 이 순서가 최종 ID 순서다.

    순서 = `decompose` → `grounding[i]` → **`harvest`** → `synthesize`(재정 P-B).
    수확 슬롯이 통합 **앞**인 이유는 실행 순서 그대로이기 때문이다 — 수확은 접지 스팬 위에서
    돌고, 통합은 그 수확 목록을 받아 `numeric_refs` 를 적는다.

    접지 레인을 위치로 키잉하는 이유: 조립기는 `groundings` 를 **배열로만** 받고, 한 작업이
    팬아웃 상한에 걸려 배치로 쪼개지면 접지 payload 는 둘보다 많아진다. 배열 위치는
    `plan_grounding` 의 계획 순서(독립 → 종속)와 언제나 같다.

    ★ `harvest` 는 LLM 레인이 아니라 **결정론 실행**이다. 그래서 레인 로그(`lane-log.json`)
    에는 나타나지 않고 여기 ID 대역 계산에만 자리를 갖는다 — `read.lane-log-shape` 가 이
    슬롯을 결함으로 읽지 않는 근거가 그것이다(`read.yaml#checks_before_exit` note).
    """
    lanes: list[tuple[str, dict]] = [(DECOMPOSE_LANE, decompose)]
    for position, payload in enumerate(groundings or []):
        lanes.append((f"grounding[{position}]", payload))
    lanes.append((HARVEST_LANE, harvest or {}))
    lanes.append((SYNTHESIS_LANE, synthesis))
    return lanes


def renumber_items(lane_payloads: list[tuple[str, dict]]) -> tuple[list[dict], dict[str, dict[str, str]]]:
    """레인별 원본 ID → 최종 `M<n>` 재번호.

    반환 = (재번호된 items, `{lane_key: {원본 id: 최종 id}}`).

    순서는 레인 투입 순서이고 레인 안에서는 **원본 배열 순서 그대로**다 — 정렬하지 않는다.
    정렬은 레인이 의도한 순서(구성요소 나열 순 · 접지 대상 순)를 지운다.

    매핑이 레인별로 갈라지는 이유: 두 레인이 같은 원본 ID 를 써도 둘은 **다른 항목**이며
    라벨만 겹쳤을 뿐이다. 각자 다른 최종 ID 를 받는 것이 옳다.
    """
    items: list[dict] = []
    id_map: dict[str, dict[str, str]] = {}
    for lane_key, payload in lane_payloads:
        lane_map = id_map.setdefault(lane_key, {})
        for item in (payload or {}).get("items") or []:
            entry = copy.deepcopy(item)
            final_id = f"M{len(items) + 1}"
            original = entry.get("id")
            entry["id"] = final_id
            if isinstance(original, str):
                lane_map[original] = final_id
            items.append(entry)
    return items, id_map


class _Renumbering:
    """재번호 표 + 참조 재작성. 재번호의 계약은 **참조가 가리키던 대상의 보존**이다.

    참조를 어느 레인의 매핑으로 고쳐 쓸지는 대상의 `kind` 가 정한다 — 레인마다 만드는 kind 가
    갈리기 때문이다(component=분해 · grounding=접지 · fact/implication/positioning/figure_note=통합).
    레인 매핑을 잘못 고르면 **조용히 다른 항목을 가리키게 되므로** 여기가 이 보수에서 가장
    위험한 자리다. 특히 두 곳이 직관을 배신한다.

    - `claims.applicant_interest[].material_id` 는 `implication` 을 가리킨다 —
      `claims` 안에 있지만 분해 레인이 아니라 **통합 레인**이 만든 항목이다.
    - `implication.derived_from[]` 은 kind 제약이 없어 **레인을 가로지른다**(실특허 산출에서
      분해 항목과 통합 항목을 함께 가리켰다). 자기 레인 매핑만 보면 대부분이 어긋난다.

    대역이 지켜지면 원본 ID 는 런 안에서 유일하므로 후보가 갈릴 일이 없다. 갈리는 경우
    (레인이 대역을 넘은 판)의 선택은 결정론이며 순서는 아래 `resolve` 에 적었다.
    """

    def __init__(self, payloads: list[tuple[str, dict]]) -> None:
        self.items, self.id_map = renumber_items(payloads)
        # 원본 ID → [(lane_key, 최종 id, kind)]. 레인 순서를 유지한다(동점 처리의 결정론).
        self._candidates: dict[str, list[tuple[str, str, str | None]]] = {}
        self._lane_of: dict[str, str] = {}
        cursor = 0
        for lane_key, payload in payloads:
            for item in (payload or {}).get("items") or []:
                final = self.items[cursor]
                cursor += 1
                self._lane_of[final["id"]] = lane_key
                original = item.get("id")
                if isinstance(original, str):
                    self._candidates.setdefault(original, []).append(
                        (lane_key, final["id"], final.get("kind"))
                    )

    def resolve(self, ref, *, owner_lane: str | None, kind: str | None):
        """원본 참조 1건 → 최종 ID.

        후보가 여럿이면 ① 같은 레인 + kind 일치 ② kind 일치 ③ 같은 레인 ④ 레인 순서 첫째.
        해소할 항목이 아예 없으면 **원본을 그대로 남긴다** — 유령 참조를 지어내지 않고
        `read.pointer-resolve` 가 결함으로 잡게 둔다. 재번호는 결함도 결함 그대로 옮긴다.
        """
        if not isinstance(ref, str):
            return ref
        candidates = self._candidates.get(ref)
        if not candidates:
            return ref
        rankings = (
            lambda entry: entry[0] == owner_lane and (kind is None or entry[2] == kind),
            lambda entry: kind is not None and entry[2] == kind,
            lambda entry: entry[0] == owner_lane,
            lambda entry: True,
        )
        for accepts in rankings:
            for entry in candidates:
                if accepts(entry):
                    return entry[1]
        return ref

    def rewrite_items(self) -> None:
        """항목이 들고 있는 참조 전량을 최종 ID 로 고쳐 쓴다."""
        for item in self.items:
            owner = self._lane_of.get(item.get("id"), None)
            kind = item.get("kind")
            if item.get("superseded_by") is not None:
                item["superseded_by"] = self.resolve(
                    item["superseded_by"], owner_lane=owner, kind=kind
                )
            # ★ 수치 역참조(재정 P-B). 함의·포지셔닝이 **어느 수치를 근거로 삼았는가**가
            #   여기서 보존되지 않으면 중요분 도출식 자체가 끊긴다 — 중요분은 LLM 의
            #   중요도 판단이 아니라 이 역참조로 도출되기 때문이다. 대상 kind 는 `fact`
            #   하나이며 소유 레인은 수확(quoted·bibliographic)과 통합(derived·figure-sourced)
            #   양쪽에 걸치므로, 레인이 아니라 **kind** 로 해소한다.
            if kind in ("implication", "positioning") and isinstance(
                item.get("numeric_refs"), list
            ):
                item["numeric_refs"] = [
                    self.resolve(ref, owner_lane=owner, kind="fact")
                    for ref in item["numeric_refs"]
                ]
            if kind == "grounding":
                item["component"] = self.resolve(
                    item.get("component"), owner_lane=DECOMPOSE_LANE, kind="component"
                )
            elif kind == "implication":
                if isinstance(item.get("derived_from"), list):
                    item["derived_from"] = [
                        self.resolve(ref, owner_lane=owner, kind=None)
                        for ref in item["derived_from"]
                    ]
            elif kind == "fact":
                for entry in (item.get("derivation") or {}).get("inputs") or []:
                    if isinstance(entry, dict) and "ref" in entry:
                        entry["ref"] = self.resolve(entry["ref"], owner_lane=owner, kind="fact")

    def rewrite_claims(self, claims: dict) -> None:
        """청구항 트리의 `material_id` 전량. 대상 kind 가 어느 레인을 볼지 정한다."""

        def walk(elements) -> None:
            for element in elements or []:
                element["material_id"] = self.resolve(
                    element.get("material_id"), owner_lane=DECOMPOSE_LANE, kind="component"
                )
                walk(element.get("children") or [])

        for claim in claims.get("independent") or []:
            walk(claim.get("elements") or [])
        for claim in claims.get("dependents") or []:
            for addition in claim.get("additions") or []:
                addition["material_id"] = self.resolve(
                    addition.get("material_id"), owner_lane=DECOMPOSE_LANE, kind="component"
                )
        for interest in claims.get("applicant_interest") or []:
            interest["material_id"] = self.resolve(
                interest.get("material_id"), owner_lane=SYNTHESIS_LANE, kind="implication"
            )


def assemble_spec(
    *,
    run_meta: dict,
    decompose: dict,
    groundings: list[dict],
    synthesis: dict,
    read_runs: tuple[str, ...],
    repo: str | None,
    source_digest: str,
    harvest: dict | None = None,
) -> dict:
    """레인 산출 → 재료 명세 초안. 조립은 결정론이며 값을 만들지 않는다.

    항목 ID 는 여기서 `M1..Mn` 으로 다시 매겨진다(위 `_Renumbering` 의 주석 참조). 투입
    payload 는 건드리지 않는다 — 레인 응답 파일이 정본 왕복 기록이므로 그 사본을 변조하면
    "레인이 무엇을 답했는가"를 사후에 되짚을 수 없다.
    """
    patent = dict((run_meta.get("patent") or {}))
    patent.pop("source_sha256", None)
    patent["source_digest"] = source_digest
    patent.setdefault("source_path", "00-source/patent.md")

    renumbering = _Renumbering(
        lane_payloads(decompose, groundings or [], synthesis, harvest)
    )
    renumbering.rewrite_items()
    claims = copy.deepcopy(decompose.get("claims") or {})
    renumbering.rewrite_claims(claims)

    engine_block = run_meta.get("engine") or {}
    return {
        "schema": "material-spec/v0",
        "reader_version": reader_version(repo),
        "spec_version": 1,
        "status": "draft",
        "run_id": run_meta.get("run_id", ""),
        "patent": patent,
        "claims": claims,
        "figures": copy.deepcopy(synthesis.get("figures") or []),
        "items": renumbering.items,
        # ★ 층 분리(재정 P-2 ⓑ). `drop_signal` 은 사실이 아니라 **편집 판단**이고 그 판단은
        #   docent 고유의 것이다 — 이식 상대(historian)는 같은 재료를 읽으면서 그 판단을
        #   하지 않는다. 그래서 공유 코어 최상위가 아니라 확장 네임스페이스 안에 산다.
        "extensions": {
            "docent": {"drop_signal": copy.deepcopy(synthesis.get("drop_signal") or {})}
        },
        "provenance": {
            # 정본은 첫 실행이고 둘째는 수렴 비교 전용이다 — 그 역할을 문자열에 적어 둔다.
            "read_runs": [
                f"{read_runs[0]}:canonical",
                *[f"{name}:convergence-peer" for name in read_runs[1:]],
            ],
            "produced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "engine_commit": str(engine_block.get("commit", "")),
        },
    }


# ---------------------------------------------------------------------------
# 중간 산출물
# ---------------------------------------------------------------------------


def _tree_lines(elements: list, additions_by_target: dict, depth: int, out: list[str]) -> None:
    for element in elements or []:
        indent = "  " * depth
        out.append(
            f"{indent}- `{element.get('id')}` → **{element.get('material_id')}** — "
            f"{element.get('text_verbatim', '')}"
        )
        for addition in additions_by_target.get(element.get("id"), []):
            out.append(
                f"{indent}  - (종속 `{addition['claim']}`) `{addition['id']}` → "
                f"**{addition.get('material_id')}** — {addition.get('text_verbatim', '')}"
            )
        _tree_lines(element.get("children") or [], additions_by_target, depth + 1, out)


def write_claim_trees(paths: RunPaths, spec: dict) -> list[str]:
    """D5 ①② — 독립항별 트리 1장. 종속항 부가 한정은 부착 지점 밑에 누적한다."""
    claims = spec.get("claims") or {}
    additions_by_target: dict[str, list[dict]] = {}
    for claim in claims.get("dependents") or []:
        for addition in claim.get("additions") or []:
            entry = dict(addition)
            entry["claim"] = claim.get("id")
            additions_by_target.setdefault(addition.get("attaches_to"), []).append(entry)

    written: list[str] = []
    for claim in claims.get("independent") or []:
        claim_id = str(claim.get("id"))
        lines = [f"# 청구항 트리 — `{claim_id}`", "", f"> {claim.get('text_verbatim', '')}", ""]
        lines.append("## 골격 (독립항 element)와 누적 층위 (종속항 부가 한정)")
        lines.append("")
        body: list[str] = []
        _tree_lines(claim.get("elements") or [], additions_by_target, 0, body)
        lines.extend(body)
        lines.append("")
        dependents = [
            claim_entry
            for claim_entry in claims.get("dependents") or []
            if claim_id in (claim_entry.get("depends_on") or [])
        ]
        lines.append("## 이 청구항을 인용하는 종속항")
        lines.append("")
        if not dependents:
            lines.append("_없음._")
        for entry in dependents:
            lines.append(
                f"- `{entry.get('id')}` — `{entry.get('dependency_type')}` "
                f"(인용: {', '.join(entry.get('depends_on') or [])})"
            )
        lines.append("")
        path = paths.claim_tree(claim_id)
        write_text(path, "\n".join(lines))
        written.append(path)
    return written


def write_grounding_md(paths: RunPaths, spec: dict, convergence: dict) -> None:
    """D5 ③ — 구성요소 ↔ 명세서 문단 ↔ 도면부호."""
    lines = ["# 3중 접지 (D5 ③)", ""]
    lines.append("접지 전량이 원칙이다(재정 R3). 예외는 아래 §2 에 전량 드러난다.")
    lines.append("")
    lines.append("## 1. 접지 목록")
    lines.append("")
    for item in spec.get("items") or []:
        if item.get("kind") != "grounding":
            continue
        anchor = item.get("anchor_state") or {}
        lines.append(
            f"### **{item.get('id')}** ← 구성요소 {item.get('component')} "
            f"(명세서 `{anchor.get('spec')}` · 도면 `{anchor.get('figure')}`)"
        )
        lines.append("")
        for ref in item.get("spec_refs") or []:
            lines.append(f"- 명세서 `{ref.get('locator', '')}`: “{ref.get('quote', '')}”")
        for ref in item.get("figure_refs") or []:
            numerals = ", ".join(ref.get("numerals") or [])
            lines.append(
                f"- 도면 `{ref.get('figure')}` (도면부호 {numerals}): "
                f"“{ref.get('caption_quote', '')}”"
            )
        if item.get("search_note"):
            lines.append(f"- 탐색 기록: {item.get('search_note')}")
        lines.append("")
    lines.append("## 2. 접지 예외")
    lines.append("")
    exceptions = convergence.get("grounding_exceptions") or []
    if not exceptions:
        lines.append("_예외 없음._")
        lines.append("")
    for entry in exceptions:
        lines.append(
            f"- **{entry.get('material_id')}** (구성요소 {entry.get('component')}) — "
            f"명세서 `{entry.get('spec')}` · 도면 `{entry.get('figure')}`: "
            f"{entry.get('search_note', '')}"
        )
    lines.append("")
    write_text(paths.grounding_md, "\n".join(lines))


def write_positioning_md(paths: RunPaths, spec: dict) -> None:
    """D5 ⑤ — 배경기술·효과 대비."""
    lines = ["# 포지셔닝 (D5 ⑤)", ""]
    for item in spec.get("items") or []:
        if item.get("kind") != "positioning":
            continue
        lines.append(f"## {item.get('id')}")
        lines.append("")
        lines.append(f"- 배경 문제: {item.get('background_problem', '')}")
        lines.append(f"- 주장 효과: {item.get('asserted_effect', '')}")
        lines.append(f"- 차이: {item.get('delta', '')}")
        for quote in item.get("quotes") or []:
            lines.append(f"- 인용: “{quote}”")
        lines.append("")
    lines.append("## 출원인 관심 신호")
    lines.append("")
    interests = ((spec.get("claims") or {}).get("applicant_interest")) or []
    if not interests:
        lines.append("_등재된 신호가 없다._")
    for interest in interests:
        lines.append(
            f"- `{interest.get('claim')}` → **{interest.get('material_id')}** — "
            f"{interest.get('signal', '')}"
        )
    lines.append("")
    write_text(paths.positioning_md, "\n".join(lines))


def write_drop_signal_md(paths: RunPaths, memos: list[dict], final: dict | None) -> None:
    """D4 2단 신호 — 조기 = 맹검 메모 2건, 최종 = drop 신호(재정 P-A 로 문언 개정).

    ★ 폐기: 조기 `drop-proposed` 로 나머지 단계를 돌리지 않고 즉시 escalate 하던 문단.
    근거 = 재정 P-A. 청구항만 본 조기 판단으로 런을 세우면 "완전 정보 위에서 1회"라는
    원칙이 깨진다. 조기 판단은 버리지 않고 맹검 관찰 메모로 강등해 축적하며(historian
    스크리닝의 사전 훈련 데이터 — D4), 확정 재정의 자리는 CP1 한 곳이다.
    """
    lines = ["# drop 신호 (D4 · 2단 — 재정 P-A)", ""]
    lines.append("## 1. 조기 — 맹검 스크리닝 메모 (상신 없음 · 진행 계속)")
    lines.append("")
    lines.append("`read-a`·`read-b` 가 **각자** 쓴다. 둘 다 싣는 이유는 두 독립 관찰의")
    lines.append("일치/불일치 자체가 신호이기 때문이다(재정 P-U4). 이 메모는 최종 서사 평가")
    lines.append("레인(`synthesize`)에 전달되지 않는다(앵커링 방지).")
    lines.append("")
    lines.append("| 실행 | 방향 | 근거 요지 |")
    lines.append("|---|---|---|")
    if not memos:
        lines.append("| _없음_ | _없음_ | 분해 레인이 메모를 내지 않았다 |")
    for memo in memos:
        lines.append(
            f"| `{memo.get('read_run', '')}` | `{memo.get('direction', '')}` | "
            f"{memo.get('note', '')} |"
        )
    lines.append("")
    directions = {memo.get("direction") for memo in memos}
    if len(directions) > 1:
        lines.append("★ 두 관찰의 방향이 **갈렸다**. 갈림은 결함이 아니라 신호다 — CP1 이 본다.")
        lines.append("")
    lines.append("## 2. 최종 — 포지셔닝 확정 후")
    lines.append("")
    lines.append("| 시점 | 판정 | 사유 |")
    lines.append("|---|---|---|")
    if final is None:
        lines.append("| 포지셔닝 확정 후 | _미산출_ | 통합 단계에 닿기 전에 멈춘 런 |")
    else:
        lines.append(
            f"| 포지셔닝 확정 후 | `{final.get('verdict', '')}` | {final.get('reason', '')} |"
        )
    lines.append("")
    if final is not None and final.get("verdict") == "drop-proposed":
        lines.append(
            "★ 최종 신호가 `drop-proposed` 다. 사유 표기는 `안도감 부적합`이며, "
            "`source` 의 `형식 전제 미충족`과는 판단의 종류가 다르다(재정 N12)."
        )
        lines.append(
            "★ 그럼에도 러너는 여기서 멈추지 않는다 — drop 의 **확정 재정은 CP1 에 통합**되며"
            "(재정 P-A), 승인 봉투가 `drop_decision`(`go` | `drop`)을 담는다."
        )
        lines.append("")
    write_text(paths.drop_signal_md, "\n".join(lines))


# ---------------------------------------------------------------------------
# 실행
# ---------------------------------------------------------------------------


def _retry_budget(contract: dict, point: str) -> int:
    """판정점 `point` 의 재시도 상한 — 정본은 계약의 `retry_budget.points[]` 다(재정 T16).

    구 판은 `failure[].action` 전건의 `retry(n)` 을 `max()` 로 뭉쳐 **런 전역 1회**를 냈다.
    재정 P-4 가 판정점을 둘로 늘린 뒤 그 하나는 「총비용 상한」이 아니라 **「먼저 도착한
    판정점의 우선권」**으로 작동했고, 실물 런에서 출구 검사 78건에 재시도 0회가 났다.

    **코드가 상한을 지어내지 않는다.** 계약에 그 판정점이 없으면 기본값을 만들지 않고
    거부한다 — 같은 규율이 `reader/lib/convergence.py` 의 `convergence.threshold-missing`
    에 이미 서 있다(임계가 없으면 판정하지 말고 결함으로 낸다).
    """
    for entry in (contract.get("retry_budget") or {}).get("points") or []:
        if isinstance(entry, dict) and entry.get("id") == point:
            value = entry.get("max_retries")
            if type(value) is int:
                return value
            raise RunnerContractError(
                f"판정점 {point!r} 의 max_retries 가 정수가 아니다 — "
                "계약: contracts/stages/read.yaml"
            )
    raise RunnerContractError(
        f"판정점 {point!r} 이 retry_budget.points[] 에 없다 — "
        "계약: contracts/stages/read.yaml"
    )


def _retry_checks(contract: dict, point: str) -> set[str]:
    """판정점의 재시도 검사 목록을 정확히 한 행에서 읽는다."""
    points = (contract.get("retry_budget") or {}).get("points") or []
    matches = [
        entry
        for entry in points
        if isinstance(entry, dict) and entry.get("id") == point
    ]
    if len(matches) != 1:
        raise RunnerContractError(
            f"판정점 {point!r}의 retry_budget.points[] 행은 정확히 1개여야 한다: {len(matches)}"
        )
    checks = matches[0].get("checks")
    if not isinstance(checks, list) or not checks:
        raise RunnerContractError(f"판정점 {point!r}의 checks는 비지 않은 list여야 한다")
    if any(not isinstance(check_id, str) or not check_id for check_id in checks):
        raise RunnerContractError(f"판정점 {point!r}의 checks 원소는 비지 않은 문자열이어야 한다")
    if len(checks) != len(set(checks)):
        raise RunnerContractError(f"판정점 {point!r}의 checks에 중복이 있다")
    allowed = set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS)
    unknown = set(checks) - allowed
    if unknown:
        raise RunnerContractError(
            f"판정점 {point!r}의 checks에 출구 12 id 밖의 값이 있다: {sorted(unknown)!r}"
        )
    return set(checks)


def _validate_retry_contract(contract: dict) -> None:
    """레인 디스패치 전에 판정점·승인 집합을 거부 경계로 닫는다."""
    points = (contract.get("retry_budget") or {}).get("points") or []
    ids = [entry.get("id") for entry in points if isinstance(entry, dict)]
    expected_points = set(RETRY_POINT_IDS)
    actual_points = set(ids)
    if (
        len(ids) != len(points)
        or len(ids) != len(set(ids))
        or actual_points != expected_points
    ):
        raise RunnerContractError(
            "retry_budget 판정점이 승인값과 다르다: "
            f"승인에만={sorted(expected_points - actual_points)!r}, "
            f"계약에만={sorted(actual_points - expected_points)!r}, ids={ids!r}"
        )
    for point, approved in (
        ("early", set(EARLY_RETRY_CHECK_IDS)),
        ("exit", set(EXIT_RETRY_CHECK_IDS)),
    ):
        actual = _retry_checks(contract, point)
        if actual != approved:
            raise RunnerContractError(
                f"판정점 {point!r} 재시도 목록이 승인 집합과 다르다: "
                f"승인에만={sorted(approved - actual)!r}, 계약에만={sorted(actual - approved)!r}"
            )


def _exit_retry_eligible(contract: dict, failing: list[CheckRow]) -> bool:
    """비지 않은 출구 실패 집합 전부가 재시도 목록에 들었는지 대조한다."""
    if not failing:
        return False
    return {row.check_id for row in failing} <= _retry_checks(contract, "exit")


def _failure_signature(rows: list[CheckRow]) -> tuple[tuple[str, str, str], ...]:
    """실패 판정 행의 **서명** — (check_id, rule, locus) 의 정렬 튜플(재정 T16 §6 ⑤).

    값(`found`)을 서명에 넣지 않는 이유: 같은 코드 결함이 회차마다 조금씩 다른 실측값을
    낼 수 있고(항목 ID 재번호가 그렇다), 그러면 재현이 재현으로 보이지 않는다. 무엇이
    어디서 어떤 규칙으로 걸렸는가가 같으면 그것이 같은 실패다.
    """
    return tuple(
        sorted(
            (row.check_id, finding.rule, finding.locus)
            for row in rows
            for finding in row.findings
        )
    )


def _execute_decompose(
    *,
    read_run: str,
    adapter,
    view: ReadView,
    profiles: dict,
    journal: LaneJournal,
    lane_attempt: int,
    defects: list[dict] | None,
    repo: str | None = None,
) -> dict:
    """② 분해 1회. **두 실행이 도는 구간은 여기까지다**(재정 P-4 · E 지시).

    구 `_execute_read_run` 은 한 실행이 분해→접지→통합을 통째로 돌았고, 그것이 두 번
    반복됐다. 재정 P-4 가 수렴을 분해 직후로 옮기고 접지 이후를 정본 1개로 확정했으므로
    실행 단위를 **분해 전용**과 **정본 후속** 둘로 가른다.

    ★ `lane_attempt` = **이 레인 자신의 시도 회차**이며 런 전역 예산 카운터가 아니다
    (재정 2026-08-19 Q7 ②). 이름을 `attempt` 에서 바꾼 이유가 그 구별이다 — 두 값이 같은
    이름을 쓰던 동안 분해의 재시도가 그 뒤 레인의 좌표까지 밀어 올렸다.

    ★ 폐기: 조기 `drop_signal.verdict == "drop-proposed"` 면 접지 지출 전에 멈추던 분기.
    근거 = 재정 P-A(조기 drop 의 escalate 폐지). 조기 판단은 `screening_memo` 로 기록만
    되고 러너는 멈추지 않는다 — 확정 재정의 자리는 CP1 한 곳이다.
    """
    return _dispatch(
        adapter,
        # `repo` 를 넘기는 이유: 요청 지문이 **절차 본문**까지 결속하므로 어느 절차 트리에서
        # 인라인하는지가 요청의 일부다(재정 2026-08-19 S4).
        plan_decompose(read_run, view, profiles, lane_attempt, defects, repo=repo),
        journal,
    )[0].payload


def _execute_canonical_tail(
    *,
    read_run: str,
    decompose: dict,
    adapter,
    view: ReadView,
    profiles: dict,
    journal: LaneJournal,
    lane_attempt: int,
    defects: list[dict] | None,
    rules: Rules,
    run_meta: dict,
    read_runs: tuple[str, ...],
    repo: str | None,
    source_digest: str,
) -> dict:
    """⑦ 접지 → **수확** → 통합. 정본 실행 하나만 여기 들어온다(재정 P-4).

    수확이 접지와 통합 **사이**에 있는 이유(재정 P-B): 수확기는 접지 항목의
    `spec_refs[].quote` 를 스캔하므로 접지 뒤여야 하고, 통합 레인은 그 수확 목록을 받아
    `numeric_refs` 를 적으므로 통합 앞이어야 한다. 순서가 바뀌면 "고르는 주체가 서사가
    아니라 참조"라는 도출식이 성립하지 않는다.

    ★ `lane_attempt` = **정본 후속 자신의 시도 회차**다(재정 2026-08-19 Q7 ②). 분해가 몇 번
    재시도했든 이 구간의 첫 실행은 `retry-` 접두 없이 선다 — 레인 로그가 "이 레인이
    재시도했다"를 말할 때 그것이 사실이어야 하기 때문이다.
    """
    claims = decompose.get("claims") or {}
    grounding_requests = plan_grounding(
        read_run, claims, view, profiles, lane_attempt, defects, repo=repo
    )
    groundings = [
        response.payload for response in _dispatch(adapter, grounding_requests, journal)
    ]

    # 수확은 조립된 명세 위에서 돈다 — 수확기가 보는 것은 원천 파일이 아니라 **접지 스팬**이다.
    # 여기서 만드는 임시 조립본은 통합 전 단계의 것이며 산출물로 남지 않는다.
    provisional = assemble_spec(
        run_meta=run_meta,
        decompose=decompose,
        groundings=groundings,
        synthesis={},
        read_runs=read_runs,
        repo=repo,
        source_digest=source_digest,
    )
    harvested, skipped = harvest_numeric_facts(
        provisional, rules=rules, id_start=harvest_band_start(claims)
    )

    synthesis = _dispatch(
        adapter,
        # 접지 산출을 넘기는 이유: `figures[]` 는 synthesize 만 만들 수 있는데 그 배열에
        # 해소되어야 하는 `figure_refs` 는 접지가 만든다. 무엇이 참조되었는지 알려 주지
        # 않으면 두 레인 사이에 아무도 책임지지 않는 구간이 남는다(실특허 스모크 적발).
        # 수확 목록을 함께 넘기는 이유는 재정 P-B — 수치를 다시 지어내지 않게 하기 위해서다.
        plan_synthesis(
            read_run,
            claims,
            view,
            profiles,
            lane_attempt,
            defects,
            groundings,
            harvested,
            repo=repo,
        ),
        journal,
    )[0].payload
    return {
        "decompose": decompose,
        "groundings": groundings,
        "harvest": {"items": harvested},
        "skipped": skipped,
        "synthesis": synthesis,
    }


# ---------------------------------------------------------------------------
# 맹검 스크리닝 메모 (재정 P-A · P-U4)
# ---------------------------------------------------------------------------


def screening_memo(read_run: str, decompose: dict) -> dict:
    """분해 응답의 `screening_memo` → 보고 서식 1행.

    응답 키는 `reason`(절차 문서 `reader/procedure/10-decompose.md` §5 의 실물 서식)이고
    보고 서식의 키는 `note`(`convergence/v0#screening_memos`)다. 두 이름을 잇는 자리를
    여기 하나로 둔다 — 두 곳에서 각자 옮기면 한쪽이 반드시 낡는다.
    """
    memo = decompose.get("screening_memo") or {}
    note = memo.get("reason")
    if not isinstance(note, str) or not note:
        note = str(memo.get("note", ""))
    return {
        "read_run": read_run,
        "direction": str(memo.get("direction", "")),
        "note": note,
    }


def append_screening_ledger(
    repo: str | None,
    *,
    run_id: str,
    memos: list[dict],
    final: dict | None,
    shadow_root: str | None = None,
) -> str | None:
    """섀도 원장(`ledgers/shadow/screening.jsonl`)에 **한 행**을 추가한다(재정 P-U4).

    ★ 런 밖이고 재료 명세 계약면 밖이다. 한 행 = 맹검 메모 2건 + 최종 평가 + Owner 재정이며,
    Owner 재정은 CP1 에서 내려오므로 이 시점에는 `null` 이다(재정 P-A — 확정은 CP1 한 자리).
    추가 전용이며 이미 쓴 행을 고쳐 쓰지 않는다 — 축적물의 값은 그 무편집성에 있다.

    ★ "한 행"은 이 함수가 아니라 **호출 자리**가 지킨다. 무편집성 탓에 여기서 중복을 사후에
    지울 수 없으므로, 러너는 런이 종결될 때만 이 함수를 부른다(`run()` 의 `terminated` 주석).

    목적은 섀도 모드다: 청구항만 본 맹검 판단 · 접지 후 최종 평가 · Owner 재정의 3층이
    자매 프로젝트 patent-historian 의 스크리닝 능력에 대한 사전 훈련 데이터가 된다(D4).

    `shadow_root` 는 **원장 누적 루트의 명시 지정**이다(2026-08-19 정정 — 구 문언은 "테스트
    하네스 전용 주입구"였다). 테스트 격리는 그 지정의 **한 사용자**일 뿐이며(합성 픽스처의
    메모가 생산 원장에 섞이면 축적물이 훈련 데이터로서 죽는다 — 재정 G6·P-U2), 다른 사용자는
    누적 자리를 런과 다른 곳에 두려는 운영자다. 비우면 `shadow_ledger_root` 가 판정한다 —
    주 작업 트리면 거기, 격리 체크아웃이면 **주 작업 트리로 옮겨** 쌓는다(재정 P-U1 + P-U4).
    `repo` 는 계약 트리의 루트이고 이 인자는 원장의 루트다. 층이 다르므로 합치지 않는다.
    """
    if not memos:
        return None
    path = shadow_screening_ledger(repo, shadow_root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = {
        "run_id": run_id,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "memos": memos,
        "final_verdict": (final or {}).get("verdict"),
        "final_reason": (final or {}).get("reason"),
        "owner_decision": None,
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return path


# ---------------------------------------------------------------------------
# 조기 수렴 · 접지 진입 게이트 (재정 P-4 · P-U3)
# ---------------------------------------------------------------------------


def decompose_only_spec(
    *,
    run_meta: dict,
    decompose: dict,
    read_runs: tuple[str, ...],
    repo: str | None,
    source_digest: str,
) -> dict:
    """분해 산출만으로 만드는 조립본(재정 P-4 · T16 부속 4).

    구 판은 수렴 6축만을 목적으로 적었다. 이제 청구항 소유 검사도 같은 조립본에서 돈다 —
    조립기를 따로 만들지 않고 출구와 같은 `assemble_spec` 에 접지·통합·수확 자리표시를
    넘긴다. 수렴 6축과 두 소유 검사는 모두 `claims` 위에서 판정할 수 있으므로 접지·통합이
    필요 없다. 이 조립본은 판정용이며 산출물로 남지 않는다.
    """
    return assemble_spec(
        run_meta=run_meta,
        decompose=decompose,
        groundings=[],
        synthesis={},
        read_runs=read_runs,
        repo=repo,
        source_digest=source_digest,
    )


def early_convergence_row(*, canonical_spec: dict, peer_spec: dict | None, rules: Rules) -> CheckRow:
    """④-b 조기 수렴 검사 — 두 분해 산출만으로 6축을 계산한다(재정 P-4 · T16).

    검사 구현은 이식 단위(`reader/lib/convergence.py`)에 있고 러너는 등재부를 거쳐 부른다.
    여기서 축을 다시 계산하면 구현이 두 벌이 되고, 두 벌 중 하나는 반드시 낡는다.
    """
    return CHECK_REGISTRY[CONVERGENCE_CHECK_ID](
        CheckContext(spec=canonical_spec, peer_spec=peer_spec, rules=rules)
    )


def escalation_entries(row: CheckRow) -> list[dict]:
    """상신 축(`escalation-trigger`)의 미달 기록(재정 P-3).

    판정 행의 `fail` 과 **층이 다르다** — 상신 축의 미달은 실패가 아니라 Owner 상신이므로
    검사기가 결함을 등재하지 않고 이 목록에만 남긴다. 러너는 그 층 구분을 그대로 따른다.
    """
    entries = row.extras.get("escalations") or []
    return [dict(entry) for entry in entries if isinstance(entry, dict)]


def continue_envelope_state(paths: RunPaths) -> tuple[bool, str]:
    """Owner '계속' 봉투가 **이 판정서에** 결속되어 있는가(재정 P-U3).

    조건 4항: 봉투 실재 · `approval-envelope/v0` 통과 · `checkpoint == convergence_continue`
    이고 `decision == approved` · `target.digest` 가 **판정서 파일의 실제 SHA-256**.
    마지막 항이 핵심이다 — 봉투가 판정서에 결속되지 않으면 '계속'은 판정서와 무관한 종이가
    되고, 재분해로 판정서가 바뀌어도 옛 승인이 살아남는다(R8 규격의 자동 실효).
    """
    path = paths.convergence_continue_md
    if not os.path.isfile(path):
        return False, "계속 봉투가 없다"
    try:
        envelope = parse_envelope(read_text(path))
    except StageError as exc:
        return False, f"계속 봉투 서식 위반 — {exc}"
    schema = load_json(os.path.join(paths.repo, *APPROVAL_SCHEMA))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(envelope),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        return False, f"계속 봉투가 approval-envelope/v0 를 위반한다: {errors[0].message}"
    if envelope.get("checkpoint") != CONTINUE_CHECKPOINT:
        return False, (
            f"계속 봉투의 checkpoint 가 {envelope.get('checkpoint')!r} 다 — "
            f"{CONTINUE_CHECKPOINT!r} 이어야 한다"
        )
    if envelope.get("decision") != "approved":
        return False, f"계속 봉투가 승인이 아니다(decision={envelope.get('decision')!r})"
    if not os.path.isfile(paths.convergence_early_json):
        return False, "결속 대상인 조기 수렴 판정서가 없다"
    actual = sha256_file(paths.convergence_early_json)
    declared = str((envelope.get("target") or {}).get("digest", ""))
    if declared != actual:
        return False, (
            f"계속 봉투가 다른 판정서에 결속되어 있다 — 봉투 {declared} ≠ 판정서 {actual}"
        )
    return True, "계속 봉투 유효(판정서 지문 결속 확인)"


def phase_gate_reason(
    *,
    blocked_by: str,
    envelope_ok: bool,
    envelope_in_scope: bool,
    envelope_note: str,
) -> str:
    """접지 진입·차단의 사람이 읽는 사유를 만든다(재정 2026-09-01 T17)."""
    labels = {
        PHASE_GATE_NONE: "조기 판정 전부 통과",
        PHASE_GATE_CLAIM_CHECKS: "조기 청구항 소유 검사 실패",
        PHASE_GATE_EXACT_MATCH: "조기 수렴 exact-match 축 미달",
        PHASE_GATE_ESCALATION: "조기 수렴 상신 축 미달",
    }
    label = labels.get(blocked_by, f"알 수 없는 차단 사유({blocked_by})")
    if blocked_by == PHASE_GATE_NONE:
        return f"{label} — 접지에 진입한다. {envelope_note}"
    if envelope_ok and envelope_in_scope:
        return f"{label} — Owner '계속' 봉투로 진입한다. {envelope_note}"
    if envelope_ok and not envelope_in_scope:
        dispositions = {
            PHASE_GATE_CLAIM_CHECKS: "분해 재시도 — 조기 예산 소진 시 계약 실패표(escalate)",
            PHASE_GATE_EXACT_MATCH: "조기 수렴 재시도 — 예산 소진 시 계약 실패표(escalate)",
        }
        disposition = dispositions.get(blocked_by, "접지 진입 차단")
        return (
            f"{label}이 접지 진입을 막았다. 재정 2026-09-01 T17에 따라 봉투는 조기 "
            f"수렴의 상신 축 미달에만 적용된다. 처분: {disposition}. {envelope_note}"
        )
    return f"{label}로 접지 진입을 차단한다. {envelope_note}"


def check_lane_log_shape(
    journal: LaneJournal, *, read_runs: tuple[str, ...], canonical: str
) -> CheckRow:
    """⑨ `read.lane-log-shape` — 레인 로그가 계약 실행 형태와 일치하는가(재정 P-4 · P-U3 · P-12).

    판정 **6항**. **형태** 3항: ⓐ 분해가 두 실행 각각에 존재 ⓑ 접지·통합이 정본 실행에 존재
    ⓒ 접지·통합이 **비정본 실행에 부재**. ⓒ가 이 검사가 생긴 이유다 — "정본 1개만
    진행했다"는 사실은 로그에 **없음으로** 증명되며, 그 부재를 아무도 보지 않으면 재정
    P-4 의 절반(접지 이후 1회)이 관습으로만 남는다.

    **시점 결속** 3항: ⓓ 모든 행이 요청 지문을 든다(재정 P-12) ⓔ 응답이 도착한 행은 응답
    지문을 들고 반향이 일치한다(재정 P-12) ⓕ 모든 행이 **요청 파일 지문**을 든다
    (재정 2026-08-19 S4 · Q8 ③ — 판정 관할의 확장이므로 재정이 근거다). 여기서 보는 것도 같은
    종류의 사실이다 — 결속이 코드에만 있고 로그에 남지 않으면, 다음 개정이 그것을 지워도
    산출물은 아무 말도 하지 않는다.

    ★ ⓕ의 대상 제외 하나: `request_digest` 가 **명시적으로 `None`** 인 행(요청 파일을 쓰지
    않는 재생 어댑터의 왕복)은 요구하지 않는다. 제외의 뜻은 **능력의 부재**뿐이며, 요청 파일을
    쓰는 어댑터의 읽기 실패는 빈 문자열로 적혀 여기서 **결함으로 걸린다**(2026-08-19 보수 —
    구 코드는 그 실패까지 `None` 으로 접어 면제로 셌다). 제외 건수는 `request_digest_exempt` 로 산출에
    남으므로 조용한 통과가 아니다. 반면 **키 자체가 없는 행**은 결함이다 — 그것은 "요청 파일이
    없었다"가 아니라 "러너가 아무것도 적지 않았다"이며, 구 서식으로의 퇴행이 정확히 그 모습을
    한다.

    ★ 수확 슬롯은 판정 대상이 아니다. 결정론 실행이라 `lane.sub_lanes`(LLM 레인 배정의
    정본)에 등재되지 않으며 레인 로그에도 나타나지 않는다(`read.yaml` 의 같은 검사 note).
    """
    row = CheckRow(check_id=LANE_LOG_SHAPE_CHECK_ID, checked=len(journal.rows))
    tail_tasks = {"ground-independent", "ground-dependent", "synthesize"}
    tasks_by_run: dict[str, list[str]] = {}
    for entry in journal.rows:
        tasks_by_run.setdefault(str(entry.get("read_run")), []).append(str(entry.get("task")))
    row.extras["lane_tasks"] = {name: sorted(set(tasks)) for name, tasks in tasks_by_run.items()}

    for read_run in read_runs:
        tasks = tasks_by_run.get(read_run, [])
        if "decompose" not in tasks:
            row.add(
                "lane-log.decompose-present",
                f"10-read/lanes/{read_run}/decompose",
                "(레인 로그 없음)",
                "분해 1건",
                "분해는 두 독립 실행 각각에 존재해야 한다 — 없으면 수렴 검사의 전제가 없다",
            )
        if read_run == canonical:
            continue
        stray = sorted({task for task in tasks if task in tail_tasks})
        if stray:
            row.add(
                "lane-log.non-canonical-tail",
                f"10-read/lanes/{read_run}",
                ", ".join(stray),
                "(부재)",
                "비정본 실행이 접지·통합 레인을 돌았다 — 접지 이후는 정본 1개다(재정 P-4)",
            )

    canonical_tasks = tasks_by_run.get(canonical, [])
    if "synthesize" not in canonical_tasks:
        row.add(
            "lane-log.canonical-tail",
            f"10-read/lanes/{canonical}/synthesize",
            "(레인 로그 없음)",
            "통합 1건",
            "정본 실행이 통합에 닿지 않았다 — 조립할 산출이 없다",
        )

    # ⓓⓔⓕ 시점 결속. 응답이 도착하지 않은 행(미충족·짝 없음)은 응답 지문을 가질 수
    # 없으므로 ⓔ의 대상이 아니고, **거부 행**은 대상이다 — 거부는 "응답이 있었으나 물렸다"는
    # 사건이며 그 사실이 판정에서 빠지면 거부가 조용한 통과가 된다.
    exempt = 0
    for entry in journal.rows:
        locus = f"10-read/lanes/{entry.get('lane_id')}"
        # ⓕ 요청 파일 지문(재정 2026-08-19 S4 · Q8 ③).
        if "request_digest" not in entry:
            row.add(
                "lane-log.request-file-digest",
                locus,
                "(요청 파일 지문 칸 없음)",
                "sha256(request.md)",
                "요청 파일 지문이 없는 왕복이다 — 레인이 읽은 요청서가 지금 그 자리의 파일과 "
                "같은지 사후에 판정할 근거가 로그에 없다(재정 S4 · Q8 ③)",
            )
        elif entry.get("request_digest") is None:
            # 요청 파일을 쓰지 않는 어댑터의 왕복 — 대상에서 뺀다(건수는 아래 extras 에 남는다).
            exempt += 1
        elif not str(entry.get("request_digest")).strip():
            row.add(
                "lane-log.request-file-digest",
                locus,
                f"요청 파일 지문 {entry.get('request_digest')!r}",
                "sha256(request.md)",
                "요청 파일 지문이 빈 값이다 — 어댑터가 요청 파일을 **쓰는데도 읽지 못했다**"
                "(또는 지문이 비어 기록됐다). 레인이 읽은 요청서가 지금 그 자리의 파일과 "
                "같은지 사후에 판정할 근거가 로그에 없다(재정 S4 · Q8 ③). 요청 파일을 쓰지 "
                "않는 어댑터는 이 자리에 null 을 적으므로 면제이고, 빈 값은 면제가 아니다",
            )
        if not str(entry.get("input_digest") or ""):
            row.add(
                "lane-log.request-digest",
                locus,
                "(입력 지문 없음)",
                "sha256(요청 본문)",
                "요청 지문이 없는 왕복이다 — 응답이 어느 판의 요청에 답한 것인지 증명할 "
                "근거가 로그에 없다(재정 P-12 ①③)",
            )
        arrived = entry.get("actual_model") is not None or bool(entry.get("rejected"))
        if not arrived:
            continue
        if not str(entry.get("response_digest") or "") or not entry.get("digest_ok"):
            row.add(
                "lane-log.response-digest",
                locus,
                f"응답 지문 {entry.get('response_digest')!r} · digest_ok={entry.get('digest_ok')!r}",
                "sha256(response.json) 기록 + digest_ok: true",
                "소비한 응답의 지문·반향 일치가 로그에 없다 — 같은 자리에 응답이 두 번 "
                "쓰이면 런이 정본을 증명하지 못한다(재정 P-12 ②③)",
            )
    # 제외를 산출에 남긴다 — 몇 건을 무엇 때문에 빼고 통과시켰는지가 보이지 않으면, 그 제외는
    # 판정이 아니라 사각지대가 된다(재정 2026-08-19 S4).
    row.extras["request_digest_exempt"] = exempt
    return row


def _bare_sha256_file(path: str) -> str:
    """파일 바이트의 sha256 을 **접두어 없는 맨 hex** 로 낸다 — 레인 지문의 층위다.

    ★ **엔진의 `sha256_file` 을 쓰지 않는 이유가 여기 있고, 그것이 이 함수의 존재 이유다.**
    이 리포에는 지문 표기가 두 층 있다. 하나는 계약면의 다이제스트로 `sha256:` 접두를 달고
    (`contracts/glossary.md` §3 — `^sha256:[0-9a-f]{64}$`), 다른 하나는 **레인 로그의 왕복
    지문**으로 맨 hex 다(`FileLaneAdapter.request_md_digest` · `LaneResponse.response_digest`
    가 `hashlib.sha256(...).hexdigest()` 를 그대로 싣는다). 맨 hex 인 이유는 재정 S4 가 든
    근거 그대로다 — **사람이 `sha256sum request.md` 로 곧장 대조할 수 있어야** 한다.

    두 층을 섞으면 대조가 **항상 불일치**한다. 실제로 이 검사의 초판이 `sha256_file` 을 썼고
    정직한 왕복에서 *"로그 `b8e85947…` ≠ 파일 `sha256:b8e85947…`"* 로 울었다 — 값은 같은데
    표기가 달라서 난 거짓 양성이며, 시험이 그것을 개발 중에 잡았다. 여기서 층을 명시로
    고정해 둔다.
    """
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def check_lane_log_digest_value(
    journal: LaneJournal, *, lanes_root: str | None
) -> CheckRow:
    """⑨-b `read.lane-log-digest-value` — 로그가 적은 요청 지문이 **그 자리의 파일과 같은가**
    (재정 2026-08-31 Q1).

    **형제 검사와 무엇이 다른가.** `read.lane-log-shape` 는 로그의 **형태**를 주장한다 —
    칸이 있는가, 비어 있지 않은가, 면제가 명시적인가. 이 검사는 **값**을 주장한다 — 그 칸에
    적힌 64자리가 지금 그 자리의 `request.md` 를 sha256 한 값과 **같은가**. 둘은 다른 주장이며,
    한 검사가 둘을 지면 **어느 쪽이 통과시켰는지 판정문에서 사라진다**(재정 Q1 의 근거이자 이
    리포의 원리 — *"네 도구는 각자 하나의 주장만 증명한다"*, `CLAUDE.md` §6).

    **무엇을 잡는가 — 2026-08-19 감수 D 가 실측한 두 구멍이 여기서 닫힌다.**

      M-D  값만 위조   로그의 `request_digest` 를 `ffff…ffff` 로 바꾼다. 형태는 온전하므로
                       `lane-log-shape` 는 `pass checked=5 violations=0` 이었다.
                       → 여기서 `lane-log.digest-value-mismatch` 로 걸린다.
      M-E  `null` 위장 `FileLaneAdapter` 가 **실제로 `request.md` 를 쓴** 행의 값을 `null` 로
                       바꾼다. 형태 검사는 `null` 을 **무조건 제외**로 세므로
                       `request_digest_exempt=1` 만 늘고 통과했다.
                       → 여기서 `lane-log.digest-null-disguise` 로 걸린다. **면제의 자격은
                       선언이 아니라 사실이다** — 요청 파일이 그 자리에 **없을 때만** 면제다.
      M-C  사후 교체   소비 뒤 `request.md` 를 다른 내용으로 덮어쓴다. 직전 라운드에는
                       **사람이 손으로 대조해야만** 드러났다(감수의 "DETECTED—로그↔파일 대조").
                       → 여기서 기계가 잡는다. 같은 규칙(`digest-value-mismatch`)이며, 위조와
                       교체는 **로그와 파일이 갈렸다**는 하나의 사실의 두 원인이다.

    ★ **`None` 면제의 현행 축소분을 되돌리지 않는다**(재정 Q1 의 명시 조건). 직전 라운드가
    `_request_file_digest` 에서 면제를 「능력 부재」 하나로 좁힌 것은 유효하며, 이 검사는 그
    **위에** 값 대조를 얹는다. 좁힌 뒤에도 남아 있던 구멍이 *"능력이 있는 어댑터의 행을
    누군가 `null` 로 고쳐 적으면?"* 이었고 그 자리를 파일의 실재로 판정한다.

    ★ **어댑터에 다시 묻지 않는다.** 값을 낸 코드(`FileLaneAdapter.request_md_digest`)를 다시
    불러 대조하면 같은 함수가 자기 출력을 승인하는 꼴이고, 그것은 아무것도 증명하지 않는다
    (같은 형태의 결함을 감수가 `value.harvest-parity` 에서 지적했다 — 수확기가 정답 생성에
    다시 쓰여 자기 손실을 못 본다). 그래서 **파일을 직접 열어 sha256 을 다시 낸다.**

    ★ **이 검사가 증명하지 않는 것.** `lanes_root` 가 어디인가는 런 **구성**이지 증거가
    아니다 — 이 검사는 "로그의 값이 그 루트 아래 파일과 같다"만 주장하고, 그 루트가 옳은
    루트인지는 주장하지 않는다. 경계를 넓게 말하지 않기 위해 적어 둔다.

    **판정 대상 밖 둘**(형태 검사의 소관이므로 여기서 이중으로 세지 않는다):
    칸 자체가 없는 행 · 값이 **빈 문자열**인 행. 둘 다 `lane-log-shape` 가 이미 결함으로
    잡으며, 여기서 또 잡으면 한 결함이 두 판정 행에서 두 번 울어 계수가 부풀려진다.
    건수는 `deferred_to_shape` 로 산출에 남으므로 조용한 통과가 아니다.
    """
    row = CheckRow(
        check_id=LANE_LOG_DIGEST_VALUE_CHECK_ID, checked=len(journal.rows)
    )
    verified = 0
    exempt_verified = 0
    deferred = 0

    for entry in journal.rows:
        lane_id = str(entry.get("lane_id"))
        locus = f"10-read/lanes/{lane_id}"
        if "request_digest" not in entry:
            deferred += 1
            continue
        declared = entry.get("request_digest")
        if declared is not None and not str(declared).strip():
            deferred += 1
            continue

        request_md = (
            None
            if lanes_root is None
            else os.path.join(lanes_root, *lane_id.split("/"), REQUEST_MD)
        )
        present = request_md is not None and os.path.isfile(request_md)

        if declared is None:
            # 면제 주장. 자격은 **요청 파일의 부재**이며 선언이 아니다.
            if present:
                row.add(
                    "lane-log.digest-null-disguise",
                    locus,
                    "request_digest: null (그런데 request.md 가 그 자리에 있다)",
                    "요청 파일이 있으면 sha256(request.md) 를 적는다",
                    "요청 파일을 **쓰는** 왕복이 면제를 주장한다 — 면제의 뜻은 「능력의 부재」 "
                    "하나뿐이고(재정 2026-08-19 S4 의 축소분), 파일이 실재하는 행의 null 은 "
                    "능력 부재가 아니라 **기록의 삭제**다. 이 위장은 형태 검사에서 제외 계수만 "
                    "늘리고 통과했다(2026-08-19 감수 D 의 M-E)",
                )
            else:
                exempt_verified += 1
            continue

        # 값 주장. 파일을 직접 열어 다시 잰다.
        if not present:
            row.add(
                "lane-log.digest-file-missing",
                locus,
                f"request_digest {str(declared)[:16]}… (그런데 request.md 가 없다)",
                f"{locus}/{REQUEST_MD} 실재",
                "로그가 요청 파일 지문을 드는데 그 파일이 없다 — 지문이 지목하는 대상이 "
                "사라졌으므로 값 대조가 성립하지 않는다. 요청 파일을 쓰지 않는 어댑터라면 "
                "값이 아니라 null 이어야 한다",
            )
            continue
        try:
            actual = _bare_sha256_file(request_md)
        except OSError as exc:
            row.add(
                "lane-log.digest-file-unreadable",
                locus,
                f"{type(exc).__name__}: {exc}",
                f"{locus}/{REQUEST_MD} 읽기 가능",
                "요청 파일이 있는데 읽을 수 없다 — 값 대조가 성립하지 않는다. 여기서 예외를 "
                "다시 던지지 않는 이유는 형태 검사와 같다: 던지면 그 사실이 판정에 닿기 전에 "
                "런이 죽고 무엇이 왜 없었는지가 런 폴더에 남지 않는다",
            )
            continue
        if actual != str(declared):
            row.add(
                "lane-log.digest-value-mismatch",
                locus,
                f"로그 {str(declared)[:16]}… ≠ 파일 {actual[:16]}…",
                f"로그의 request_digest == sha256({REQUEST_MD})",
                "레인 로그가 적은 요청 파일 지문이 지금 그 자리의 파일과 다르다 — 값이 "
                "위조되었거나(감수 D 의 M-D) 소비 뒤 요청 파일이 교체되었다(M-C). 어느 "
                "쪽이든 로그는 더 이상 레인이 실제로 읽은 요청서를 지목하지 못한다. "
                f"사람이 `sha256sum {REQUEST_MD}` 로 곧장 같은 대조를 할 수 있다",
            )
            continue
        verified += 1

    # 무엇을 대조했고 무엇을 미뤘는지 전부 산출에 남긴다 — 보이지 않는 제외는 판정이 아니라
    # 사각지대가 된다(재정 2026-08-19 S4 가 `request_digest_exempt` 를 남긴 것과 같은 규율).
    row.extras["digest_verified"] = verified
    row.extras["exempt_verified"] = exempt_verified
    row.extras["deferred_to_shape"] = deferred
    row.extras["lanes_root_present"] = lanes_root is not None
    return row


def _validate_convergence(payload: dict, repo: str | None) -> None:
    target = os.path.join(repo or repo_root(), *CONVERGENCE_SCHEMA)
    with open(target, encoding="utf-8") as handle:
        schema = json.load(handle)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        first = errors[0]
        locus = "/".join(str(step) for step in first.absolute_path) or "$"
        raise RunnerContractError(
            f"{payload.get('phase', '')} 수렴 보고서가 convergence/v0 를 위반한다(@{locus}): "
            f"{first.message}"
        )


def run(
    *,
    run_root: str,
    adapter,
    rules: Rules,
    read_runs: tuple[str, str] = ("read-a", "read-b"),
    repo: str | None = None,
    shadow_root: str | None = None,
) -> dict:
    """READ 스테이지 1회. 실행 순서는 모듈 docstring 의 ①~⑩ 그대로다.

    실패 반환 = `{"rows", "spec", "convergence", "status", "reason_label", "diagnostic"}`.
    `read.source-digest` 실패의 diagnostic 은 원천 파일·기대 지문·재독 실측 지문을 든다.
    원장 자리는 반환값이 아니라 **산출물**에 남는다 — `10-read/lanes/shadow-ledger.json`
    (아래 `_write_shadow_pointer`).
    반환값은 호출자의 메모리에서 끝나고 산출물은 런 폴더에 남으므로, 사후 감사가 볼 수 있는
    것은 뒤엣것뿐이다.

    `shadow_root` = **섀도 원장 누적 루트의 명시 지정**(재정 P-U4). 비우면 러너가 판정한다 —
    주 작업 트리면 거기, **커밋 결박된 격리 체크아웃이면 주 작업 트리로 옮겨** 쌓는다
    (`engine/paths.py#shadow_ledger_root`). 법은 worktree 에서 오고(재정 P-U1 행위시법) 축적은
    리포에 남는다는 귀결이며, 이 배선이 없던 동안 통주 2 의 메모 4행은 worktree 와 함께 사라져
    리포에 한 행도 도착하지 않았다.

    합성 픽스처로 이 함수를 부르는 하네스는 이 인자를 **반드시** 채운다(재정 G6·P-U2 — 표본은
    자기완결 미니 세계, 과거 생산 원장 1,178행 오염). 판정에 기대지 마라: 픽스처의 계약 트리는
    대개 임시 git 리포이므로 판정은 그 임시 리포를 정직하게 가리킬 뿐이다.
    """
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    paths.ensure_read_dirs()
    run_meta = load_yaml(paths.run_yaml)

    # ① 진입 지문 검사(재정 P-C).
    #
    # ★ 폐기: 여기서 patent.md ↔ patent.sha256 ↔ run.yaml 을 직접 대조해
    #   `read.source-digest` 행으로 halt 하던 블록. 근거 = 재정 P-C — 같은 불일치를 보는
    #   자리를 진입 검사 한 곳으로 모으고, 그 처분을 품질 결함이 아니라 **환경 오류**로
    #   바꾼다(재시도·수정 루프가 아니라 즉시 중단 + 진단). 같은 불변식 I1 을 **명세 위에서**
    #   보는 출구 검사 `read.source-digest`(reader/lib)는 그대로 돈다 — 층이 다르다.
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID)
    _validate_retry_contract(contract)

    source_text = read_text(paths.patent_md)
    actual_digest = sha256_bytes(source_text.encode("utf-8"))
    view = ReadView(source_text, rules)
    profiles = lane_profiles(repo)
    journal = LaneJournal()
    schema = load_schema()
    early_budget = _retry_budget(contract, "early")  # 레인별
    tail_budget = _retry_budget(contract, "exit")  # 런 전역(정본 후속 구간)

    # ⑤ 정본 지정(재정 P-4) — **선언 순서**다. 내용맹이며 결정론이고, 어떤 품질 비교·판정도
    #   하지 않는다. 근거: 수렴 통과는 두 독해가 동치라는 선언이므로 정본 선택에 판정자가
    #   없고, 남는 요구는 재현성뿐이다. "어느 쪽이 더 나은가"를 묻는 코드가 여기 생기는
    #   순간 재정 P-4 가 금지한 품질 비교가 부활한다.
    canonical_run = read_runs[0]
    peer_run = read_runs[1] if len(read_runs) > 1 else None

    memos: list[dict] = []
    final_signal: dict | None = None
    # ★ 판정점별 예산과 레인 좌표(재정 2026-09-01 T16, Q7 ② 개정).
    #
    #   ★ 폐기: 구 `attempt` 는 **런 전역 예산**을 분해와 정본 후속이 나눠 쓰고,
    #   `convergence_detail.attempt` 도 그 소진량을 실었다. Q7 의 범위 보존 문언을 예산 배분의
    #   독립 판단으로 잘못 읽은 결과였고, P-4 뒤에는 먼저 도착한 판정점의 우선권이 되었다.
    #
    #   이제 `decompose_attempt[read_run]` 은 그 레인의 발번과 **조기 예산 소진량**을 함께
    #   나타내고, `tail_attempt` 은 정본 후속의 발번과 출구 예산 소진량을 나타낸다.
    #   `early_convergence_attempt` 은 비교 판정점의 실행 회차다. 계약이 각 상한을 정하며
    #   러너는 늘리지 않는다. `convergence_detail.attempt` 도 해당 판정점의 실행 회차를 싣는다.
    decompose_attempt: dict[str, int] = {name: 0 for name in read_runs}
    early_convergence_attempt = 0
    run_id = str(run_meta.get("run_id", ""))

    # ★ 원장 기입은 런이 **종결**될 때 한 번이다(재정 P-U4 의 "한 행" 문언 이행).
    #   `LanePending` 은 오류가 아니라 상태이며 오케스트레이터가 서브에이전트를 붙이고 같은
    #   스테이지를 다시 부른다 — 그 재진입마다 원장에 적으면 한 run_id 아래 미완성 행이
    #   쌓인다(2026-08-18 감수 실측: 4행, 앞 3행은 `final_verdict: null`). 축적물의 값은
    #   무편집성에 있으므로 이미 쓴 행을 지우거나 갱신해 고칠 수는 없다. 그러므로 애초에
    #   **적지 않는다** — 아직 끝나지 않은 런은 기록할 관찰이 아니라 진행 중인 상태다.
    terminated = True
    try:
        # ②③④ 분해 → 맹검 메모 → 실행별 청구항 소유 검사 → 조기 수렴(재정 T16).
        pending = list(read_runs)
        decomposes: dict[str, dict] = {}
        early_defects: dict[str, list[dict]] = {}
        early_claim_rows: dict[str, list[CheckRow]] = {}
        while True:
            for read_run in pending:
                decomposes[read_run] = _execute_decompose(
                    read_run=read_run,
                    adapter=adapter,
                    view=view,
                    profiles=profiles,
                    journal=journal,
                    lane_attempt=decompose_attempt[read_run],
                    defects=early_defects.get(read_run),
                    repo=repo,
                )

            memos = [screening_memo(name, decomposes[name]) for name in read_runs]
            decompose_specs = {
                name: decompose_only_spec(
                    run_meta=run_meta,
                    decompose=payload,
                    read_runs=read_runs,
                    repo=repo,
                    source_digest=actual_digest,
                )
                for name, payload in decomposes.items()
            }

            # ④-a 청구항 소유 검사 — 실행별 판정이므로 실패한 실행만 표적 재시도한다.
            early_claim_rows = {}
            for name in read_runs:
                run_rows = run_early_claim_checks(
                    CheckContext(
                        spec=decompose_specs[name],
                        source_text=source_text,
                        rules=rules,
                    )
                )
                for row in run_rows:
                    row.extras["read_run"] = name
                early_claim_rows[name] = run_rows
            claim_failures = {
                name: [row for row in rows if row.status == "fail"]
                for name, rows in early_claim_rows.items()
            }
            claim_failures = {name: rows for name, rows in claim_failures.items() if rows}

            # ④-b 수렴은 청구항 원인 검사가 실패하면 보류한다(재정 T16 부속 3).
            early_row = None
            escalations = []
            if not claim_failures:
                early_convergence_attempt += 1
                early_row = early_convergence_row(
                    canonical_spec=decompose_specs[canonical_run],
                    peer_spec=decompose_specs[peer_run] if peer_run else None,
                    rules=rules,
                )
                escalations = escalation_entries(early_row)

            early_rows = [entry_row, *early_claim_rows[canonical_run]]
            if peer_run:
                early_rows.extend(early_claim_rows[peer_run])
            if early_row is not None:
                early_rows.append(early_row)

            early_payload = to_convergence_payload(
                early_rows,
                decompose_specs[canonical_run],
                phase="early",
                canonical_read_run=canonical_run,
                screening_memos=memos,
            )
            if early_payload["convergence_detail"]["executed"]:
                early_payload["convergence_detail"]["attempt"] = early_convergence_attempt
            _validate_convergence(early_payload, paths.repo)
            write_json(paths.convergence_early_json, early_payload)

            if claim_failures:
                retryable = [
                    name
                    for name in read_runs
                    if name in claim_failures and decompose_attempt[name] < early_budget
                ]
                if not retryable:
                    break
                # 회차마다 새로 만들고 각 실행 자신의 Finding 8키만 돌려준다(T16 부속 5).
                early_defects = {
                    name: findings_of(claim_failures[name]) for name in retryable
                }
                pending = retryable
                for name in retryable:
                    decompose_attempt[name] += 1
                continue

            if early_row is not None and early_row.status == "fail":
                retryable = [
                    name for name in read_runs if decompose_attempt[name] < early_budget
                ]
                if not retryable:
                    break
                # 수렴 행은 두 실행의 비교이므로 같은 소견만 양쪽에 보내며 payload 는 보내지 않는다.
                early_defects = {
                    name: findings_of([early_row]) for name in retryable
                }
                pending = retryable
                for name in retryable:
                    decompose_attempt[name] += 1
                continue
            break

        # ⑥ 접지 진입 게이트(재정 P-U3).
        #
        # 재정 T16 이 청구항 소유 검사를 조기 국면에 등재하면서 봉투가 그 실패까지 함께
        # 넘기게 되었고(감사 지적 C-2), **T16 은 그 확대를 명하지 않았다**. 청구항이 틀린 것은
        # 「갈림」이 아니라 「결함」이며 그 처분은 분해 재시도다 — 봉투로 넘기면 방금 만든
        # 되먹임 경로를 우회하고 그 봉투가 만능 통행증이 된다(재정 T17). **소급하지 않는다** —
        # WO 런의 봉투는 `tree-edges` 미달 하나를 넘겼으므로 이 좁힘 뒤에도 그대로 유효하다.
        early_passed = (
            not claim_failures
            and early_row is not None
            and early_row.status == "pass"
            and not escalations
        )
        if claim_failures:
            blocked_by = PHASE_GATE_CLAIM_CHECKS
        elif early_row is None:
            # 이 상태는 도달 가능한 분기로 만들 수 없다. claim_failures 가 비면 위 루프가
            # early_convergence_row() 의 CheckRow 를 반드시 받는다는 불변식이 있기 때문이다.
            # 그래서 감사 Y-4 가 벌한 「있는 척」 라벨을 지우고 계약 위반으로 소리 나게
            # 멈춘다. no-verdict 는 어떤 런에서도 발행된 적이 없으므로 값 공간을 좁히는
            # 변경도 아니다 — 여기 왔다면 조기 루프 또는 수렴 판정의 불변식이 깨진 것이다.
            raise RunnerContractError(
                "READ 조기 게이트 불변식 위반 — claim_failures가 비었는데 early_row가 없다. "
                "early_convergence_row()가 CheckRow를 반환한다는 분해→수렴 불변식 또는 "
                "조기 재시도 루프의 제어 흐름이 깨졌다"
            )
        elif early_row.status == "fail":
            blocked_by = PHASE_GATE_EXACT_MATCH
        elif escalations:
            blocked_by = PHASE_GATE_ESCALATION
        else:
            blocked_by = PHASE_GATE_NONE
        envelope_ok, envelope_note = continue_envelope_state(paths)
        envelope_in_scope = blocked_by in ENVELOPE_SCOPE
        envelope_applied = envelope_ok and envelope_in_scope
        entered = early_passed or envelope_applied
        gate_reason = phase_gate_reason(
            blocked_by=blocked_by,
            envelope_ok=envelope_ok,
            envelope_in_scope=envelope_in_scope,
            envelope_note=envelope_note,
        )
        write_json(
            paths.phase_gate_json,
            {
                "phase": "grounding",
                "declared_input": "10-read/convergence-early.json",
                "entered": entered,
                "early_passed": early_passed,
                "blocked_by": blocked_by,
                "envelope_scope": list(ENVELOPE_SCOPE),
                "envelope": {
                    "present": os.path.isfile(paths.convergence_continue_md),
                    "valid": envelope_ok,
                    "in_scope": envelope_in_scope,
                    "applied": envelope_applied,
                    "note": envelope_note,
                },
                "reason": gate_reason,
                "ruling": ["재정 P-U3", "재정 2026-09-01 T17"],
            },
        )
        if not entered:
            if blocked_by == PHASE_GATE_CLAIM_CHECKS:
                status, reason_label = _failure_verdict(
                    contract,
                    [row for rows in claim_failures.values() for row in rows],
                )
            elif blocked_by == PHASE_GATE_EXACT_MATCH:
                status, reason_label = _failure_verdict(contract, [early_row])
            else:
                status, reason_label = _gate_escalation_verdict(contract)
            return {
                "rows": early_rows,
                "spec": None,
                "convergence": early_payload,
                "status": status,
                "reason_label": reason_label,
                "diagnostic": None,
                "gate_note": gate_reason,
            }

        # ⑦ 접지 → 수확 → 통합. **정본 1개만** 여기 들어간다(재정 P-4).
        tail_defects: list[dict] | None = None
        tail_attempt = 0
        previous_signature = None
        repeated_signature = False
        id_maps: dict[str, dict[str, str]] = {}
        while True:
            tail = _execute_canonical_tail(
                read_run=canonical_run,
                decompose=decomposes[canonical_run],
                adapter=adapter,
                view=view,
                profiles=profiles,
                journal=journal,
                lane_attempt=tail_attempt,
                defects=tail_defects,
                rules=rules,
                run_meta=run_meta,
                read_runs=read_runs,
                repo=repo,
                source_digest=actual_digest,
            )
            final_signal = tail["synthesis"].get("drop_signal") or final_signal
            canonical = assemble_spec(
                run_meta=run_meta,
                decompose=tail["decompose"],
                groundings=tail["groundings"],
                synthesis=tail["synthesis"],
                read_runs=read_runs,
                repo=repo,
                source_digest=actual_digest,
                harvest=tail["harvest"],
            )
            # 재번호 표는 레인 응답과 최종 명세를 잇는 **유일한 좌표**다. 남기지 않으면
            # "레인이 답한 M2065 가 명세의 어느 항목인가"를 사후에 되짚을 길이 끊긴다.
            _, lane_id_map = renumber_items(
                lane_payloads(
                    tail["decompose"], tail["groundings"], tail["synthesis"], tail["harvest"]
                )
            )
            id_maps = {
                f"{canonical_run}/{lane_key}": mapping
                for lane_key, mapping in lane_id_map.items()
            }

            # ⑧ 검사 전건. 수렴 축의 peer 는 **분해만 돈** 비정본 실행이다 — 6축은 claims
            #    위에서 계산되므로 접지·통합이 없어도 같은 판정이 선다.
            #
            # 재정 2026-09-02 T24 ⒜ — 출구 검사는 매 회차 디스크 재독본 위에서 돈다. 조기
            # 판정점은 진입 시 읽은 메모리 사본을 유지한다. 조기에 다시 읽으면 파일 변경이
            # 분해 결함으로 오진되고, 그 판정점에는 원천 지문 검사도 없다.
            try:
                exit_source_text = read_text(paths.patent_md)
            except OSError as exc:
                # 감사 A-4 — 이식 단위 reader/lib 는 파일 시스템을 모르므로 엔진이
                # read.source-digest 대리 행을 만들어 기존 halt·진단 흐름에 합류시킨다.
                declared = canonical["patent"]["source_digest"]
                actual = f"(읽을 수 없음: {exc})"
                row = CheckRow(check_id="read.source-digest")
                row.checked = 1
                row.extras["declared"] = declared
                row.extras["actual"] = actual
                row.add(
                    "source.digest-match",
                    "patent.source_digest",
                    declared or "(없음)",
                    actual,
                    "출구 재독 실패 — 원천 파일을 읽을 수 없어 지문을 대조하지 못했다. "
                    "이 인스턴스의 인용 검사 전부가 무효이므로 READ 중단 대상이다",
                )
                rows = [row]
            else:
                rows = run_read_checks(
                    CheckContext(
                        spec=canonical,
                        source_text=exit_source_text,
                        rules=rules,
                        schema=schema,
                        peer_spec=decompose_specs[peer_run] if peer_run else None,
                    )
                )
            for row in rows:
                row.extras["read_run"] = canonical_run
            failing = [row for row in rows if row.status == "fail"]
            if not failing:
                break
            # 감사 A-3 · 원장 T25 ⒜ 「하나라도」 — 실패 검사를 각각 자기 계약 행에
            # 대조한다. read.schema(action: retry(1), then: halt)는 종전처럼 한 번 재시도한다.
            if not _exit_retry_eligible(contract, failing):
                break
            signature = _failure_signature(failing)
            if previous_signature is not None and signature == previous_signature:
                # ★ 재현 자체가 진단이다 — 남은 예산을 태우지 않고 상신한다(재정 T16 §6 ⑤).
                repeated_signature = True
                break
            if tail_attempt >= tail_budget:
                break
            # 재시도는 Finding 8키만 정본 후속에 돌려준다. 분해와 예산을 공유하지 않는다(T16).
            tail_defects = findings_of(failing)
            previous_signature = signature
            tail_attempt += 1

        write_json(os.path.join(paths.lanes_dir, ID_MAP_BASENAME), id_maps)

        mismatched = journal.mismatched()
        if mismatched:
            raise LaneAssignmentError(
                "레인이 요청과 다른 모델·effort 로 돌았다(조용한 대체 금지): "
                + ", ".join(
                    f"{row['lane_id']} 요청 {row['requested_model']}/{row['requested_effort']} "
                    f"→ 실제 {row['actual_model']}/{row['actual_effort']}"
                    for row in mismatched
                )
                + f" — 기록: {paths.lane_log}"
            )

        # ⑨ 출구 검사 + 레인 로그 형태 판정 + 레인 로그 지문 **값** 판정.
        #
        # ★ 둘은 따로 보고된다(재정 2026-08-31 Q1) — 형태와 값은 다른 주장이고, 한 행이 둘을
        #   지면 어느 쪽이 통과시켰는지 판정문에서 사라진다. 값 검사의 대조 대상은 어댑터가
        #   요청 파일을 쓴 자리이며, 요청 파일을 쓰지 않는 어댑터(재생 어댑터)는 `root` 가
        #   없으므로 `None` 이 간다 — 그 경우 전 행이 명시 `null` 이어야 정합이다.
        rows = [
            entry_row,
            *rows,
            check_lane_log_shape(journal, read_runs=read_runs, canonical=canonical_run),
            check_lane_log_digest_value(
                journal, lanes_root=getattr(adapter, "root", None)
            ),
        ]

        payload = to_convergence_payload(
            rows,
            canonical,
            phase="full",
            canonical_read_run=canonical_run,
            screening_memos=memos,
            skipped_tokens=tail["skipped"],
        )
        if payload["convergence_detail"]["executed"]:
            # 재정 T16: 전역 예산 소진량이 아니라 정본 후속 판정점의 실행 회차다.
            payload["convergence_detail"]["attempt"] = tail_attempt + 1
        _validate_convergence(payload, paths.repo)
        write_json(paths.convergence_json, payload)

        write_drop_signal_md(paths, memos, final_signal)

        failing = [row for row in rows if row.status == "fail"]
        if failing:
            # C5 — 검사가 하나라도 실패하면 산출을 확정하지 않는다. 판정 보고서와 drop 신호는
            # Owner 가 판단할 자료이므로 남기되, 재료 명세와 판독본은 쓰지 않는다.
            status, reason_label = _failure_verdict(
                contract, failing, repeated=repeated_signature
            )
            source_digest_rows = [
                row for row in failing if row.check_id == "read.source-digest"
            ]
            diagnostic = None
            if source_digest_rows:
                source_digest_row = source_digest_rows[0]
                diagnostic = {
                    "check_id": "read.source-digest",
                    "path": paths.patent_md,
                    "declared": source_digest_row.extras.get("declared"),
                    "actual": source_digest_row.extras.get("actual"),
                }
            return {
                "rows": rows,
                "spec": None,
                "convergence": payload,
                "status": status,
                "reason_label": reason_label,
                "diagnostic": diagnostic,
            }

        # ⑩ CP1 상신물.
        write_json(paths.material_spec_json, canonical)
        write_claim_trees(paths, canonical)
        write_grounding_md(paths, canonical, payload)
        write_positioning_md(paths, canonical)
        write_text(
            paths.material_spec_md,
            render(
                canonical,
                payload,
                contract,
                paths.repo,
                convergence_early=(
                    load_json(paths.convergence_early_json)
                    if os.path.isfile(paths.convergence_early_json)
                    else None
                ),
            ),
        )

        # ★ 최종 drop 이 `drop-proposed` 여도 러너는 멈추지 않는다(재정 P-A). 계약의 failure
        #   표에서 drop 행이 삭제되었고, 확정 재정의 자리는 CP1(승인 봉투의 drop_decision)
        #   한 곳이다 — 부분 정보 위에서 두 번 판단하는 것보다 완전한 정보 위에서 한 번이 낫다.
        return {
            "rows": rows,
            "spec": canonical,
            "convergence": payload,
            "status": "ok",
            "reason_label": None,
        }
    except LanePending:
        # 재진입 — 이 호출은 런의 끝이 아니다. 레인 로그는 아래 `finally` 가 그대로 남긴다
        # (요청이 어디까지 나갔는지는 대기 중에도 볼 수 있어야 한다).
        terminated = False
        raise
    finally:
        _finish_lane_log(paths, journal)
        # 메모는 런의 **성패**와 무관하게 남는다 — 축적물이 목적이므로 중단된 런의 관찰도
        # 신호다. 성패와 종결은 다른 축이며, 여기서 가르는 것은 종결 여부 하나다.
        written = None
        if terminated:
            written = append_screening_ledger(
                paths.repo,
                run_id=run_id,
                memos=memos,
                final=final_signal,
                shadow_root=shadow_root,
            )
        # 어느 원장에 썼는지를 산출에 남긴다. 재진입 회차(`terminated=False`)도 적는다 —
        # "아직 아무것도 쓰지 않았다"는 것 역시 그 시점의 사실이고, 적지 않으면 사후에
        # "왜 이 회차에는 기록이 없는가"를 다시 조사하게 된다.
        _write_shadow_pointer(
            paths,
            shadow_root=shadow_root,
            written=written,
            terminated=terminated,
            memo_count=len(memos),
        )


def _failure_verdict(
    contract: dict, failing: list[CheckRow], *, repeated: bool = False
) -> tuple[str, str | None]:
    """검사 실패 → 조치. 재시도 예산은 이미 소진된 뒤 호출된다."""
    if repeated and not ({row.check_id for row in failing} & set(READ_CHECK_IDS)):
        raise StageError(
            "도달 불능 상태 — repeated=True 인데 출구 루프 검사 실패가 없다: "
            f"{sorted(row.check_id for row in failing)!r}"
        )
    candidates = failure_rows_for_checks(contract, {row.check_id for row in failing})
    if repeated:
        candidates.append(failure_row_of_kind(contract, "retry-repeat"))
    entry = select_failure_row(contract, candidates)
    return terminal_action(entry), entry.get("reason_label")


def _gate_escalation_verdict(contract: dict) -> tuple[str, str | None]:
    """조기 상신 축 사건도 종단 어휘 검증을 우회하지 않는다."""
    entry = failure_row_of_kind(contract, "gate-escalation")
    return terminal_action(entry), entry.get("reason_label")


def _finish_lane_log(paths: RunPaths, journal: LaneJournal) -> None:
    write_json(paths.lane_log, journal.rows)


def _write_shadow_pointer(
    paths: RunPaths,
    *,
    shadow_root: str | None,
    written: str | None,
    terminated: bool,
    memo_count: int,
) -> None:
    """`10-read/lanes/shadow-ledger.json` — 이 런이 **어느 섀도 원장에 썼는가**(재정 P-U4).

    ★ 이 파일이 있는 이유. 원장은 런 밖에 누적되므로(재정 P-U4) 런 산출물만 보아서는 그것이
    어디에 있는지 알 수 없다. 2026-08-18 통주 2 는 커밋 결박된 격리 체크아웃에서 돌았고
    (재정 P-U1) 메모 4행이 그 worktree 안에 쌓였는데, **런은 그 사실을 아무 데도 적지 않았다** —
    worktree 가 소모품이라 행이 함께 사라진 뒤에야 리포 원장 0행으로 드러났다. 쓴 자리를 적지
    않으면 다음에 또 사라진다.

    `root_source` 는 자리의 **판정 사유**이며(`engine/paths.py` 의 상수 4종) 자리 자체보다
    중요하다 — `main-worktree-resolved` 는 "여기는 worktree 였고 러너가 주 트리로 옮겼다"를,
    `explicit` 은 "호출자가 지정했다"를 뜻한다. 사유 없이 경로만 적으면 그 경로가 옳은지를
    다음 사람이 처음부터 다시 조사해야 한다.
    """
    payload = {
        "run_repo": paths.repo,
        "root_source": None,
        "root": None,
        "ledger": None,
        "appended": written is not None,
        "terminated": terminated,
        "memo_count": memo_count,
    }
    try:
        root, source = shadow_ledger_root(paths.repo, shadow_root)
    except ShadowLedgerRootError as exc:
        # 판정이 거부로 끝났다면 그 사실 자체가 기록 대상이다. 여기서 조용해지면 러너가 왜
        # 멈췄는지가 런 폴더에 남지 않는다(예외는 호출자에게만 간다).
        payload["root_source"] = "refused"
        payload["error"] = str(exc)
    else:
        payload["root_source"] = source
        payload["root"] = root
        payload["ledger"] = os.path.join(root, *SHADOW_LEDGER_RELATIVE)
    write_json(paths.shadow_pointer, payload)
