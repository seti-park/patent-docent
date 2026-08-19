# -*- coding: utf-8 -*-
"""`read` 스테이지 — D5 5단계 독해 실행 경로.

계약 = `contracts/stages/read.yaml`(정본 서술 = SPEC §1.4 + §1.5 CP1).

실행 순서(재정 P-4 · P-A · P-C · P-U3 · P-U4 · P-B — SPEC §1.4).

```
① 진입 지문 검사(P-C)                      → 불일치면 StageEnvironmentError(재시도 아님)
② read-a.decompose · read-b.decompose      → 분해 **2회**. 여기까지만 2회다.
③ 맹검 스크리닝 메모 2건 수집(P-A·P-U4)    → 섀도 원장(런 밖)에 한 행으로 등재
④ 조기 수렴 검사(P-4)                      → 10-read/convergence-early.json (phase: "early")
⑤ 정본 지정(P-4)                           → read_runs[0]. 내용맹·결정론. 품질 비교 금지.
⑥ 접지 진입 게이트(P-U3)                   → 판정서 존재 ∧ (통과 ∨ Owner '계속' 봉투)
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

검사 구현은 여기 없다(이식 단위 `reader/lib` 안에 있다). 감춰진 예외는 예외가 아니라 은폐다.
"""

from __future__ import annotations

import copy
import json
import os
import re
from datetime import datetime, timezone

from jsonschema import Draft202012Validator

from reader.lib import CHECK_REGISTRY, run_read_checks, to_convergence_payload
from reader.lib.harvest import harvest_numeric_facts
from reader.lib.report import CheckContext, CheckRow
from reader.lib.rules import Rules
from reader.lib.spec_io import load_schema

from . import (
    StageEnvironmentError,
    StageError,
    failure_entry,
    findings_of,
    load_json,
    load_yaml,
    read_text,
    sha256_bytes,
    sha256_file,
    verify_declared_inputs,
    write_json,
    write_text,
)
from ..lanes.contract import (
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
CONTINUE_CHECKPOINT = "convergence_continue"
RETRY_PATTERN = re.compile(r"retry\((?P<count>\d+)\)")


class LaneAssignmentError(StageError):
    """레인이 요청과 다른 모델·effort 로 돌았다(조용한 대체 금지 — SPEC §7.3 규율 4)."""


class RunnerContractError(StageError):
    """러너 산출이 자기 계약(`convergence/v0`)을 위반했다."""


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

        `None` 은 "요청 파일이 없는 어댑터로 돌았다"는 사실이다(재생 어댑터 — 응답 트리만 읽고
        요청을 쓰지 않는다). 그 사실을 지어내지 않고 그대로 적으며, 판정
        (`lane-log.request-file-digest`)은 그 행을 대상에서 빼되 **몇 건을 뺐는지 산출에 남긴다**.
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
    """어댑터가 쓴 `request.md` 파일 바이트의 지문 — 없는 어댑터면 `None`(재정 2026-08-19 S4).

    능력 조회(`getattr`)로 묻는 이유: 요청을 **쓰지 않는** 어댑터가 있다(재생 어댑터는 미리
    준비된 응답 트리만 읽는다). 그 경로에 요청 파일 지문을 요구하면 없는 파일을 지어내야 하고,
    지어낸 지문은 없느니만 못하다. 값이 없다는 사실은 `None` 으로 그대로 적히며 판정이 그
    행을 대상에서 뺀다 — 무엇을 뺐는지는 판정 산출에 남는다.
    """
    probe = getattr(adapter, "request_md_digest", None)
    if probe is None:
        return None
    try:
        return probe(request)
    except OSError:
        # 파일이 없다·읽을 수 없다는 것도 사실이며, 여기서 던지면 그 사실이 로그에 닿기 전에
        # 런이 죽는다. 값을 비우면 판정이 대상에서 빼되 건수를 남긴다.
        return None


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


def _retry_budget(contract: dict) -> int:
    """계약의 `failure[].action` 에서 `retry(n)` 을 회수한다(코드에 박지 않는다)."""
    budget = 0
    for entry in contract.get("failure") or []:
        match = RETRY_PATTERN.search(str(entry.get("action", "")))
        if match:
            budget = max(budget, int(match.group("count")))
    return budget


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
    """분해 산출만으로 만드는 조립본.

    수렴 6축은 전부 `claims` 위에서 계산되므로(구성요소 문언·트리 간선·종속항 서명·부착)
    접지·통합 없이도 축이 전부 선다 — 그것이 수렴을 분해 직후로 옮길 수 있는 이유다
    (재정 P-4). 이 조립본은 판정용이며 산출물로 남지 않는다.
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
    """④ 조기 수렴 검사 — 두 분해 산출만으로 6축을 계산한다(재정 P-4).

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


def check_lane_log_shape(
    journal: LaneJournal, *, read_runs: tuple[str, ...], canonical: str
) -> CheckRow:
    """⑨ `read.lane-log-shape` — 레인 로그가 계약 실행 형태와 일치하는가(재정 P-4 · P-U3 · P-12).

    판정 5항. **형태** 3항: ⓐ 분해가 두 실행 각각에 존재 ⓑ 접지·통합이 정본 실행에 존재
    ⓒ 접지·통합이 **비정본 실행에 부재**. ⓒ가 이 검사가 생긴 이유다 — "정본 1개만
    진행했다"는 사실은 로그에 **없음으로** 증명되며, 그 부재를 아무도 보지 않으면 재정
    P-4 의 절반(접지 이후 1회)이 관습으로만 남는다.

    **시점 결속** 3항: ⓓ 모든 행이 요청 지문을 든다(재정 P-12) ⓔ 응답이 도착한 행은 응답
    지문을 들고 반향이 일치한다(재정 P-12) ⓕ 모든 행이 **요청 파일 지문**을 든다
    (재정 2026-08-19 S4 · Q8 ③ — 판정 관할의 확장이므로 재정이 근거다). 여기서 보는 것도 같은
    종류의 사실이다 — 결속이 코드에만 있고 로그에 남지 않으면, 다음 개정이 그것을 지워도
    산출물은 아무 말도 하지 않는다.

    ★ ⓕ의 대상 제외 하나: `request_digest` 가 **명시적으로 `None`** 인 행(요청 파일을 쓰지
    않는 재생 어댑터의 왕복)은 요구하지 않는다. 제외 건수는 `request_digest_exempt` 로 산출에
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
                "요청 파일 지문이 빈 값이다 — 레인이 읽은 요청서가 지금 그 자리의 파일과 "
                "같은지 사후에 판정할 근거가 로그에 없다(재정 S4 · Q8 ③)",
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

    반환 = `{"rows", "spec", "convergence", "status", "reason_label"}`. 원장 자리는 반환값이
    아니라 **산출물**에 남는다 — `10-read/lanes/shadow-ledger.json`(아래 `_write_shadow_pointer`).
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

    source_text = read_text(paths.patent_md)
    actual_digest = sha256_bytes(source_text.encode("utf-8"))
    view = ReadView(source_text, rules)
    profiles = lane_profiles(repo)
    journal = LaneJournal()
    schema = load_schema()
    budget = _retry_budget(contract)

    # ⑤ 정본 지정(재정 P-4) — **선언 순서**다. 내용맹이며 결정론이고, 어떤 품질 비교·판정도
    #   하지 않는다. 근거: 수렴 통과는 두 독해가 동치라는 선언이므로 정본 선택에 판정자가
    #   없고, 남는 요구는 재현성뿐이다. "어느 쪽이 더 나은가"를 묻는 코드가 여기 생기는
    #   순간 재정 P-4 가 금지한 품질 비교가 부활한다.
    canonical_run = read_runs[0]
    peer_run = read_runs[1] if len(read_runs) > 1 else None

    memos: list[dict] = []
    final_signal: dict | None = None
    # ★ 두 카운터의 층이 다르다(재정 2026-08-19 Q7 ②).
    #
    #   `attempt` = **런 전역 재시도 예산**의 소진량이다. 분해 재시도와 정본 후속 재시도가
    #   그 하나를 나눠 쓰고(`budget` 은 계약의 `retry(n)` 에서 온다), `convergence_detail.attempt`
    #   가 싣는 것도 이 값이다. 예산을 레인별로 쪼개면 재시도 총량이 조용히 늘어나므로
    #   **여기는 건드리지 않는다** — 재정이 고치라고 한 것은 예산이 아니라 좌표다.
    #
    #   `decompose_attempt` · `tail_attempt` = **각 레인 자신의 시도 회차**이며 레인 id 발번에만
    #   쓴다. 구 판은 레인 id 도 `attempt` 로 매겨서, 분해가 한 번 재시도하면 그 뒤의 접지·통합이
    #   **첫 시도인데도** `retry-1/batch-0` 으로 서고 `batch-0` 은 아예 존재하지 않았다(통주 3
    #   실측 — 접지 레인이 "첫 시도 기록이 남지 않은 것이 의도인가"를 물어 왔다). 재정 P-12 로
    #   레인 로그의 증거력을 세운 직후이므로 같은 로그의 다른 필드가 오도하는 것을 두지 않는다.
    attempt = 0
    decompose_attempt = 0
    tail_attempt = 0
    run_id = str(run_meta.get("run_id", ""))

    # ★ 원장 기입은 런이 **종결**될 때 한 번이다(재정 P-U4 의 "한 행" 문언 이행).
    #   `LanePending` 은 오류가 아니라 상태이며 오케스트레이터가 서브에이전트를 붙이고 같은
    #   스테이지를 다시 부른다 — 그 재진입마다 원장에 적으면 한 run_id 아래 미완성 행이
    #   쌓인다(2026-08-18 감수 실측: 4행, 앞 3행은 `final_verdict: null`). 축적물의 값은
    #   무편집성에 있으므로 이미 쓴 행을 지우거나 갱신해 고칠 수는 없다. 그러므로 애초에
    #   **적지 않는다** — 아직 끝나지 않은 런은 기록할 관찰이 아니라 진행 중인 상태다.
    terminated = True
    try:
        # ②③④ 분해 2회 → 맹검 메모 → 조기 수렴. 재시도가 일어나는 자리는 **여기 하나**다.
        early_defects: list[dict] | None = None
        while True:
            decomposes: dict[str, dict] = {}
            memos = []
            for read_run in read_runs:
                decomposes[read_run] = _execute_decompose(
                    read_run=read_run,
                    adapter=adapter,
                    view=view,
                    profiles=profiles,
                    journal=journal,
                    lane_attempt=decompose_attempt,
                    defects=early_defects,
                    repo=repo,
                )
                memos.append(screening_memo(read_run, decomposes[read_run]))

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
            early_row = early_convergence_row(
                canonical_spec=decompose_specs[canonical_run],
                peer_spec=decompose_specs[peer_run] if peer_run else None,
                rules=rules,
            )
            early_payload = to_convergence_payload(
                [entry_row, early_row],
                decompose_specs[canonical_run],
                phase="early",
                canonical_read_run=canonical_run,
                screening_memos=memos,
            )
            if early_payload["convergence_detail"]["executed"]:
                early_payload["convergence_detail"]["attempt"] = attempt + 1
            _validate_convergence(early_payload, paths.repo)
            write_json(paths.convergence_early_json, early_payload)

            escalations = escalation_entries(early_row)
            # exact-match 축 미달 = 판정 행 fail. 재시도는 **분해**를 다시 돌린다 — 접지
            # 지출 이후로 미루지 않는다(재정 P-4). 상신 축 미달은 재시도 대상이 아니다:
            # 해석 차이는 다시 돌린다고 줄지 않으며, 재정이 그것을 "실패가 아니라 상신"이라
            # 정했다(재정 P-3).
            if early_row.status == "fail" and attempt < budget:
                early_defects = findings_of([early_row])
                # 예산(런 전역)과 좌표(이 레인)를 함께 올린다 — 분해 구간에서는 두 값이
                # 같은 걸음으로 가지만, 뜻이 다르므로 두 이름으로 센다(재정 Q7 ②).
                attempt += 1
                decompose_attempt += 1
                continue
            break

        # ⑥ 접지 진입 게이트(재정 P-U3) — 판정서 존재 ∧ (통과 ∨ Owner '계속' 봉투 유효).
        early_passed = early_row.status == "pass" and not escalations
        envelope_ok, envelope_note = continue_envelope_state(paths)
        if not early_passed and not envelope_ok:
            if early_row.status == "fail":
                entry = failure_entry(contract, "exact-match 축")
                status = str(entry.get("then", entry.get("action")))
            else:
                entry = failure_entry(contract, "상신 축")
                status = str(entry.get("action"))
            return {
                "rows": [entry_row, early_row],
                "spec": None,
                "convergence": early_payload,
                "status": status,
                "reason_label": entry.get("reason_label"),
                "gate_note": envelope_note,
            }

        # ⑦ 접지 → 수확 → 통합. **정본 1개만** 여기 들어간다(재정 P-4).
        tail_defects: list[dict] | None = None
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
            rows = run_read_checks(
                CheckContext(
                    spec=canonical,
                    source_text=source_text,
                    rules=rules,
                    schema=schema,
                    peer_spec=decompose_specs[peer_run] if peer_run else None,
                )
            )
            failing = [row for row in rows if row.status == "fail"]
            if not failing or attempt >= budget:
                break
            # 재시도는 결함 목록을 레인에 되돌려 준다 — 그러지 않으면 같은 오류를 재생산한다.
            # 이 재시도는 **정본 후속**만 다시 돈다(분해는 이미 수렴 판정을 받았다).
            tail_defects = findings_of(failing)
            # 예산은 분해와 공유하고(그래서 총량이 늘지 않는다) 좌표는 이 구간의 것만 센다.
            attempt += 1
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

        # ⑨ 출구 검사 + 레인 로그 형태 판정.
        rows = [entry_row, *rows, check_lane_log_shape(
            journal, read_runs=read_runs, canonical=canonical_run
        )]

        payload = to_convergence_payload(
            rows,
            canonical,
            phase="full",
            canonical_read_run=canonical_run,
            screening_memos=memos,
            skipped_tokens=tail["skipped"],
        )
        if payload["convergence_detail"]["executed"]:
            payload["convergence_detail"]["attempt"] = attempt + 1
        _validate_convergence(payload, paths.repo)
        write_json(paths.convergence_json, payload)

        write_drop_signal_md(paths, memos, final_signal)

        failing = [row for row in rows if row.status == "fail"]
        if failing:
            # C5 — 검사가 하나라도 실패하면 산출을 확정하지 않는다. 판정 보고서와 drop 신호는
            # Owner 가 판단할 자료이므로 남기되, 재료 명세와 판독본은 쓰지 않는다.
            status, reason_label = _failure_verdict(contract, failing)
            return {
                "rows": rows,
                "spec": None,
                "convergence": payload,
                "status": status,
                "reason_label": reason_label,
            }

        # ⑩ CP1 상신물.
        write_json(paths.material_spec_json, canonical)
        write_claim_trees(paths, canonical)
        write_grounding_md(paths, canonical, payload)
        write_positioning_md(paths, canonical)
        write_text(paths.material_spec_md, render(canonical, payload, contract, paths.repo))

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


def _failure_verdict(contract: dict, failing: list[CheckRow]) -> tuple[str, str | None]:
    """검사 실패 → 조치. 재시도 예산은 이미 소진된 뒤 호출된다."""
    ids = {row.check_id for row in failing}
    if "read.schema" in ids:
        entry = failure_entry(contract, "read.schema 실패")
        return str(entry.get("then", entry.get("action"))), entry.get("reason_label")
    if "read.source-digest" in ids:
        # 계약이 두 층을 구별해 남겼다(재정 P-C) — 같은 불일치를 **진입 시점**에 잡는 자리는
        # checks_on_entry 의 read.input-digest(환경 오류)이고, 이 행은 그 **이후 구간**에서
        # 명세 위로 드러난 불일치의 조치를 정한다. 조치는 halt 다: 원천이 바뀐 런은 폐기 대상이다.
        entry = failure_entry(contract, "원천 다이제스트")
        return str(entry.get("then", entry.get("action"))), entry.get("reason_label")
    if CONVERGENCE_CHECK_ID in ids:
        # 계약 문언이 "read.convergence 미달"에서 "read.convergence 의 exact-match 축 미달"로
        # 바뀌었다(재정 P-3) — 상신 축 미달은 판정 행을 fail 로 만들지 않으므로 여기 오지 않는다.
        entry = failure_entry(contract, "exact-match 축")
        return str(entry.get("then", entry.get("action"))), entry.get("reason_label")
    entry = failure_entry(contract, "read.verbatim")
    return str(entry.get("then", entry.get("action"))), entry.get("reason_label")


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
