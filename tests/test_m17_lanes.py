# -*- coding: utf-8 -*-
"""러너·레인 계약 4건의 pytest — 재정 2026-08-19 **Q7 ② · Q8 ① · Q8 ② · Q8 ③ · Q3**.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다
(`tests/test_m2_read.py`·`tests/test_m16_lane_binding.py` 와 같은 형식).

★ 통주 하네스는 `tests/test_m2_read.py` 의 것을 그대로 쓴다(원천 생성 · 레인 응답 트리 ·
**섀도 원장 격리**). 같은 하네스를 두 벌 만들면 한 벌은 반드시 낡고, 특히 격리 규율(재정 G6 ·
P-U2)이 낡는 순간 합성 픽스처가 생산 원장을 오염시킨다.

맨 `assert` 는 pytest 모듈이므로 허용되지만(CLAUDE.md §3 — AST 재작성으로 `-O` 에서도
살아남는다) 여기서는 옆 모듈들과 같은 관용구를 따라 `pytest.fail()` 로 **명시 비교**를 적는다.
서브프로세스를 부르는 자리는 없다 — 있었다면 종료 코드를 명시 비교로 봤을 것이다.
"""

from __future__ import annotations

import copy
import os
import re
import subprocess
import sys
import textwrap

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.lanes.plan import (  # noqa: E402
    BIBLIOGRAPHIC_EXCERPT,
    HARVEST_EXCERPT_MARGIN,
    _grounding_block,
    _harvest_block,
    harvest_band_start,
    lane_profiles,
    plan_synthesis,
)
from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.read_view import ReadView  # noqa: E402
from engine.stages import StageHaltError, load_json, load_yaml  # noqa: E402
from reader.lib.harvest import harvest_numeric_facts  # noqa: E402

# 통합 지시문이 절대 해소할 수 없는 참조. 대역 계산(`harvest_band_start`)이 3천 대에서
# 끝나므로 이 번호는 어느 레인의 대역에도 들지 않는다 — 즉 반드시 유령 참조다.
DANGLING_ID = "M9999"

TAIL_TASKS = ("ground-independent", "ground-dependent", "synthesize")


# ---------------------------------------------------------------------------
# 하네스 보조 — `test_m2_read` 의 것을 조합만 한다
# ---------------------------------------------------------------------------


def payloads_with_dangling_reference() -> dict:
    """정본 후속 검사를 실패시키는 payload 묶음(`read.pointer-resolve` 대상).

    분해 산출은 손대지 않는다 — 수렴 축은 전부 `claims` 위에서 계산되므로, 여기서 분해를
    건드리면 "정본 후속만 실패했다"는 시험의 전제가 무너진다.
    """
    payloads = m2.payload_set()
    for item in payloads["synthesize"]["items"]:
        if item.get("kind") == "implication":
            item["derived_from"] = [*item.get("derived_from", []), DANGLING_ID]
    return payloads


def payloads_with_phantom_dependent() -> dict:
    """분해의 청구항 원장 검사만 실패시키는 read-b payload 묶음."""
    payloads = m2.payload_set()
    phantom = copy.deepcopy(payloads["decompose"]["claims"]["dependents"][0])
    phantom["id"] = "CL-9"
    payloads["decompose"]["claims"]["dependents"].append(phantom)
    return payloads


def run_with_attempts(tmp_path, *, first: dict, second: dict):
    """시도 회차별로 다른 응답을 깔고 READ 를 한 번 돌린다.

    `write_lane_responses` 를 `attempts` 를 갈라 두 번 부르는 방식이며, 새 하네스를 짓지
    않는다. 반환 = `(run_root, outcome, adapter)`.
    """
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 가 ok 를 내지 않았다: {source_outcome['status']}")
    m2.write_lane_responses(root, payloads_by_run=first, attempts=(0,))
    lanes_root = m2.write_lane_responses(root, payloads_by_run=second, attempts=(1,))
    adapter = m2.ReplayLaneAdapter(lanes_root)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    return root, outcome, adapter


def dispatched_ids(adapter) -> list[str]:
    return [request.lane_id for request in adapter.dispatched]


def tail_lane_ids(lane_ids) -> list[str]:
    return [
        lane_id
        for lane_id in lane_ids
        if any(f"/{task}/" in lane_id for task in TAIL_TASKS)
    ]


# ===========================================================================
# ① 재정 Q7 ② — 레인별 시도 카운터 분리
# ===========================================================================


def test_tail_lanes_are_not_labeled_retry_after_a_decompose_retry(tmp_path) -> None:
    """이 시험이 없으면 레인 로그가 **첫 시도를 재시도라고 말해도** 아무도 모른다(재정 Q7 ②).

    통주 3 의 실측 자리다 — 분해가 한 번 재시도하자 그 뒤의 접지·통합이 전부
    `retry-1/batch-0` 으로 발번되고 `batch-0` 은 아예 존재하지 않았다. 재정 P-12 가 레인
    로그의 증거력을 세운 직후이므로, 같은 로그의 다른 필드가 오도하는 것을 두지 않는다.
    """
    diverged = {
        "read-a": m2.payload_set(),
        "read-b": m2.payload_set(dependency_type="multiple-or"),  # exact-match 축을 가른다
    }
    converged = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    root, outcome, adapter = run_with_attempts(tmp_path, first=diverged, second=converged)

    if outcome["status"] != "ok":
        pytest.fail(f"재시도 후 수렴한 런인데 status 가 {outcome['status']} 다")

    lane_ids = dispatched_ids(adapter)
    # ⓐ 분해는 재시도했다 — 이 사실이 없으면 아래 ⓑ 가 공허하다(재시도 자체가 없었던 런).
    if "read-b/decompose/retry-1/batch-0" not in lane_ids:
        pytest.fail(f"분해 재시도 좌표가 없다: {lane_ids}")
    # ⓑ 그럼에도 후속 레인은 **첫 시도**이므로 접두가 없다.
    mislabelled = [lane_id for lane_id in tail_lane_ids(lane_ids) if "/retry-" in lane_id]
    if mislabelled:
        pytest.fail(f"첫 시도인 후속 레인이 재시도로 발번됐다: {mislabelled}")
    for expected in ("read-a/ground-independent/batch-0", "read-a/synthesize/batch-0"):
        if expected not in lane_ids:
            pytest.fail(f"후속 레인의 첫 시도 좌표가 없다: {expected} — 실제 {lane_ids}")

    # ⓒ 로그도 같은 사실을 말한다. 증거는 메모리의 어댑터가 아니라 **런 폴더의 파일**이다.
    log = load_json(RunPaths(root).lane_log)
    logged = [row["lane_id"] for row in log]
    if "read-b/decompose/retry-1/batch-0" not in logged:
        pytest.fail(f"레인 로그에 분해 재시도 행이 없다: {logged}")
    stray = [row["lane_id"] for row in log if row["task"] in TAIL_TASKS and "/retry-" in row["lane_id"]]
    if stray:
        pytest.fail(f"레인 로그가 첫 시도를 재시도로 적었다: {stray}")
    tail_logged = sorted(row["lane_id"] for row in log if row["task"] in TAIL_TASKS)
    if tail_logged != [
        "read-a/ground-dependent/batch-0",
        "read-a/ground-independent/batch-0",
        "read-a/synthesize/batch-0",
    ]:
        pytest.fail(f"후속 레인의 로그 좌표가 기대와 다르다: {tail_logged}")


def test_retry_budget_is_unchanged_by_the_split(tmp_path) -> None:
    """★ 개정 (재정 2026-09-01 T16) — 이 시험이 고정하던 현상을 재정이 **풀었다**.

    **구 docstring 원문(폐기)** — *"이 시험이 없으면 카운터 분리가 재시도 총량을 조용히 늘려도
    드러나지 않는다(재정 Q7 ②). 예산(`failure[].action` 의 `retry(n)`)은 여전히 런 전역이다.
    분해가 그 예산을 쓰면 정본 후속은 자기 회차가 0 이어도 **재시도하지 못한다** — 좌표를 나눈
    것이 예산까지 나눈 것으로 미끄러지면 재시도 총량이 계약을 넘는다."*

    **무엇이 왜 바뀌었나.** 그 문언은 재정 Q7 의 **범위 보존** 진술("카운터를 나눴다고 예산까지
    몰래 늘리지 마라")을 **예산 배분의 독립 판단**으로 읽은 것이었다 — Q7 의 안건은 레인 id
    어휘였고 세 선택지 어디에도 예산 배분이 없었다. 그 사이 재정 P-4 가 판정점을 하나에서 둘로
    늘렸고, 전역 슬롯의 뜻이 「총비용 상한」에서 **「먼저 도착한 판정점의 우선권」**으로 조용히
    미끄러졌다. 실물 런에서 **출구 검사 78건에 재시도 0회** — 그 구간에 되먹임 루프가 아예
    **존재하지 않았다**. 재정 T16 이 예산을 **판정점별**(조기 = 레인별 1 · 출구 = 1)로 갈랐고,
    아래 ⓑ 는 구 시험이 **금지하던 사실**을 이제 **요구한다**.

    **Q7 이 지키려던 것은 여전히 지킨다.** 카운터를 나눈 것이 총량을 **몰래** 늘리는 것으로
    미끄러지지 않는다 — **각 판정점의 상한은 계약이 정한 값이고 러너가 임의로 늘리지 않는다.**
    ⓐ 가 계약 두 곳(`retry_budget.points[]` ↔ `failure[].action` 의 `retry(n)`)의 일치를 재고,
    ⓒ 가 실측 재시도 수가 그 상한을 넘지 않음을 잰다. **몰래 늘어난 예산은 여기서 잡힌다.**
    """
    contract = load_stage_contract("read", None)
    points = {
        entry.get("id"): entry
        for entry in (contract.get("retry_budget") or {}).get("points") or []
        if isinstance(entry, dict)
    }
    if set(points) != {"early", "exit"}:
        pytest.fail(f"판정점 기대 early·exit, 실제 {sorted(points)}")
    for point_id, point in points.items():
        if type(point.get("max_retries")) is not int:
            pytest.fail(f"{point_id}.max_retries 가 정수가 아니다: {point.get('max_retries')!r}")

    action_budgets: set[int] = set()
    for entry in contract.get("failure") or []:
        action = str(entry.get("action", ""))
        match = re.fullmatch(r"retry\((\d+)\)", action)
        if match:
            action_budgets.add(int(match.group(1)))
    for point_id, point in points.items():
        if point["max_retries"] not in action_budgets:
            pytest.fail(
                "러너의 상한이 조치 표가 선언한 값 밖이다 — 코드가 예산을 늘렸거나 "
                f"계약 두 곳이 갈렸다: {point_id}={point['max_retries']}, 조치={sorted(action_budgets)}"
            )
    if points["early"].get("scope") != "per-read-run":
        pytest.fail(f"early scope 기대 per-read-run, 실제 {points['early'].get('scope')}")
    if points["exit"].get("scope") != "run":
        pytest.fail(f"exit scope 기대 run, 실제 {points['exit'].get('scope')}")

    # ⓑ ★ 분해가 조기 예산을 썼어도 정본 후속은 자기 예산으로 재시도한다.
    broken = payloads_with_dangling_reference()
    root, outcome, adapter = run_with_attempts(
        tmp_path,
        first={
            "read-a": copy.deepcopy(broken),
            "read-b": payloads_with_phantom_dependent(),
        },
        second={"read-a": m2.payload_set(), "read-b": m2.payload_set()},
    )
    lane_ids = dispatched_ids(adapter)
    if "read-b/decompose/retry-1/batch-0" not in lane_ids:
        pytest.fail(f"분해가 예산을 쓰지 않았다 — 시험 전제가 성립하지 않는다: {lane_ids}")
    tail_retries = [lane_id for lane_id in tail_lane_ids(lane_ids) if "/retry-" in lane_id]
    if not tail_retries:
        pytest.fail(f"분해 재시도 뒤에도 후속이 자기 예산으로 재시도하지 않았다: {lane_ids}")
    if "read-a/decompose/retry-1/batch-0" in lane_ids:
        pytest.fail(f"성한 read-a 분해까지 다시 돌았다: {lane_ids}")
    if outcome["status"] != "ok":
        pytest.fail(f"두 판정점의 재시도 뒤 status 기대 ok, 실제 {outcome['status']}")

    # ⓒ 계약 상한보다 많은 회차를 발송하지 않는다.
    if any("/retry-2/" in lane_id for lane_id in lane_ids):
        pytest.fail(f"retry-2 좌표가 발송됐다: {lane_ids}")
    for read_run in ("read-a", "read-b"):
        retries = {
            lane_id.split("/")[2]
            for lane_id in lane_ids
            if lane_id.startswith(f"{read_run}/decompose/retry-")
        }
        if len(retries) > points["early"]["max_retries"]:
            pytest.fail(f"{read_run} 분해 재시도 {len(retries)}회가 조기 상한을 넘었다")
    tail_attempts = {
        lane_id.split("/")[2]
        for lane_id in tail_lane_ids(lane_ids)
        if "/retry-" in lane_id
    }
    if len(tail_attempts) > points["exit"]["max_retries"]:
        pytest.fail(f"후속 재시도 {len(tail_attempts)}회가 출구 상한을 넘었다")

    # ⓓ read-b 분해는 두 번 돌았지만 조기 수렴은 청구항 실패 뒤 **한 번만** 판정됐다.
    detail = load_json(RunPaths(root).convergence_early_json)["convergence_detail"]
    if detail["attempt"] != 1:
        pytest.fail(f"조기 판정점 실행 회차 기대 1, 실제 {detail['attempt']}")


# ===========================================================================
# ② 재정 Q8 ① — 통합 요청서의 자기완결성
# ===========================================================================


def synthesis_request(groundings, harvest=None):
    """통합 요청 1건을 계획한다(러너를 통과하지 않는다)."""
    claims = m2.decompose_payload()["claims"]
    view = ReadView(m2.SOURCE, m2.RULES)
    return plan_synthesis(
        "read-a",
        claims,
        view,
        lane_profiles(REPO),
        0,
        None,
        groundings,
        harvest,
    )[0]


def test_synthesis_request_carries_grounding_ids(tmp_path) -> None:
    """이 시험이 없으면 통합 레인이 **요청서 밖의 파일**을 열어야 하고 그 사실이 드러나지 않는다.

    `implication.derived_from` 은 실재 항목 ID 를 요구하는데, 구 판의 요청서는 접지 산출을
    도면 목록으로만 실었다 — 통주 3 의 통합 레인은 같은 실행의 `ground-*/response.json` 을
    직접 열어 ID 를 확인했고 다른 실행은 열지 않았다. 요청서 하나로 작업할 수 있어야 한다는
    원칙(재정 2026-08-19 Q8 ①)이 그 자리에서 깨져 있었다.
    """
    groundings = [m2.ground_independent_payload(), m2.ground_dependent_payload()]
    request = synthesis_request(groundings)
    body = request.instructions

    # ⓐ 접지 항목 ID 전건이 실린다.
    for item_id in ("M4", "M5", "M6"):
        if f"`{item_id}`" not in body:
            pytest.fail(f"통합 지시문에 접지 ID {item_id} 가 없다")
    # ⓑ 그 항목이 무엇에 붙었고 근거가 원천의 어디인가 — ID 만으로는 되짚을 수 없다.
    for coordinate in ("`M1`", "`M2`", "`M3`", "[0012]", "[0013]", "[0014]"):
        if coordinate not in body:
            pytest.fail(f"통합 지시문에 접지 좌표 {coordinate} 가 없다")
    if "not-depicted" not in body:
        pytest.fail("anchor_state 예외가 실리지 않았다 — 접지가 붙지 않은 자리를 레인이 모른다")
    # ⓒ 열람 범위가 문언으로 못 박힌다.
    for needle in ("derived_from", "이 표가 전부", "다른 파일을 열지 마라", "response.json"):
        if needle not in body:
            pytest.fail(f"통합 지시문이 {needle!r} 을 말하지 않는다")

    # ⓓ 접지가 비었을 때도 문언이 선다 — 빈 배열과 필드 누락은 다른 사건이다.
    empty = synthesis_request([]).instructions
    for needle in ("빈 배열", "다른 파일을 열지도 마라"):
        if needle not in empty:
            pytest.fail(f"접지 0건의 문언에 {needle!r} 이 없다")

    # ⓔ 통주 경로에서도 같은 사실이 선다 — 계획 함수만 옳고 러너가 다른 값을 넘기면 헛것이다.
    _, _, adapter = m2.run_read(tmp_path)
    dispatched = [
        request for request in adapter.dispatched if request.task == "synthesize"
    ]
    if not dispatched:
        pytest.fail("통주에서 통합 요청이 나가지 않았다")
    for item_id in ("M4", "M5", "M6"):
        if f"`{item_id}`" not in dispatched[0].instructions:
            pytest.fail(f"통주의 통합 요청에 접지 ID {item_id} 가 없다")


# ===========================================================================
# ③ 재정 Q8 ① 파생(총괄 재량 처분) — 수확 표의 출처 좌표와 원 스팬
# ===========================================================================


def harvested_facts() -> list[dict]:
    """픽스처 payload → 전수 수확 결과(원문 스팬 갈래 + 서지 갈래)."""
    spec = m2.assemble_from(m2.payload_set())
    facts, _ = harvest_numeric_facts(
        spec, rules=m2.RULES, id_start=harvest_band_start(m2.decompose_payload()["claims"])
    )
    return facts


def table_rows(block: str) -> list[str]:
    return [line for line in block.splitlines() if line.startswith("| `M")]


def test_harvest_table_carries_source_span() -> None:
    """이 시험이 없으면 수확 표가 다시 `numeric value at [0186]` 로 주저앉아도 통과한다.

    라벨만으로는 **그 수가 무엇의 수인지** 확정할 수 없고, 통주 3 의 통합 레인은 그래서
    참조를 포기했다. 좌표와 원 스팬이 실려야 `numeric_refs` 가 판단이 되고 추측이 아니게 된다
    (재정 2026-08-19 Q8 ① 파생 · 총괄 재량 처분 — 명시 재정 아님).
    """
    facts = harvested_facts()
    quoted = [fact for fact in facts if fact.get("origin") == "quoted"]
    bibliographic = [fact for fact in facts if fact.get("origin") == "bibliographic"]
    if not quoted or not bibliographic:
        pytest.fail(f"두 갈래가 다 서지 않았다: quoted {len(quoted)} · bib {len(bibliographic)}")

    block = _harvest_block(facts)
    for header in ("출처 좌표", "원 스팬 발췌"):
        if header not in block:
            pytest.fail(f"수확 표에 {header!r} 열이 없다")

    rows = table_rows(block)
    if len(rows) != len(facts):
        pytest.fail(f"표 행수 {len(rows)} != 수확 {len(facts)}")

    # ⓐ 원문 스팬 갈래 — 좌표와 값 둘레의 원문이 함께 선다.
    speed = next(fact for fact in quoted if fact["value_raw"].startswith("12"))
    row = next(line for line in rows if line.startswith(f"| `{speed['id']}` |"))
    if speed["source"]["locator"] not in row:
        pytest.fail(f"출처 좌표가 행에 없다: {row}")
    window = speed["source"]["quote"]
    if window[: min(len(window), 12)] not in row:
        pytest.fail(f"원 스팬 발췌가 원문과 다르다: {row}")

    # ⓑ 서지 갈래 — 인용 스팬이 **없다**는 사실이 문언으로 선다(빈칸이 거짓말하지 않는다).
    bib_row = next(line for line in rows if line.startswith(f"| `{bibliographic[0]['id']}` |"))
    if BIBLIOGRAPHIC_EXCERPT not in bib_row:
        pytest.fail(f"서지 갈래의 발췌 표기가 없다: {bib_row}")
    cells = [cell.strip() for cell in bib_row.strip("|").split("|")]
    if "" in cells:
        pytest.fail(f"빈칸이 남았다 — 없는 것과 적지 않은 것이 구별되지 않는다: {bib_row}")

    # ⓒ 어느 행에도 빈 발췌 칸이 없다.
    for line in rows:
        if line.strip().endswith("|  |") or "|  |" in line:
            pytest.fail(f"발췌가 빈 행이 있다: {line}")

    # ⓓ 표를 깨는 문자·줄바꿈이 접힌다 — 한 행이 헤더와 같은 칸 수를 갖는다.
    hostile = copy.deepcopy(speed)
    hostile["source"] = {
        "locator": "[0999]",
        "quote": "a rate of 12 rpm | see Table 2\nfor the second column",
        "value_span": {"start": 12, "end": 18},
    }
    hostile_block = _harvest_block([hostile])
    hostile_row = table_rows(hostile_block)[0]
    header_row = next(
        line for line in hostile_block.splitlines() if line.startswith("| 참조 ID |")
    )
    if hostile_row.count("|") - hostile_row.count("\\|") != header_row.count("|"):
        pytest.fail(f"발췌가 표를 깼다: {hostile_row}")
    if "\n" in hostile_row or "\\|" not in hostile_row:
        pytest.fail(f"줄바꿈 접기·파이프 이스케이프가 되지 않았다: {hostile_row}")

    # ⓔ 발췌는 **창**이다 — 상한이 없으면 요청서가 접지 응답의 사본이 된다.
    long_quote = "x" * 400 + "12 rpm" + "y" * 400
    windowed = copy.deepcopy(speed)
    windowed["source"] = {
        "locator": "[0999]",
        "quote": long_quote,
        "value_span": {"start": 400, "end": 406},
    }
    long_row = table_rows(_harvest_block([windowed]))[0]
    if len(long_row) > 400:
        pytest.fail(f"발췌 창이 상한을 지키지 않았다({len(long_row)}자): {long_row[:120]}…")
    if "x" * (HARVEST_EXCERPT_MARGIN + 1) in long_row:
        pytest.fail(f"발췌 창이 좌측 상한 {HARVEST_EXCERPT_MARGIN} 자를 넘었다")


# ===========================================================================
# ④-1 재정 Q8 ③ 파생(총괄 재량 처분) — 요청 파일의 무변경 재기록 중지
# ===========================================================================


def test_request_files_are_not_rewritten_when_unchanged(tmp_path) -> None:
    """이 시험이 없으면 러너 재진입이 요청 파일의 시각을 흔들어 **응답보다 뒤에 세운다**.

    오염은 없다 — 지문이 같으므로 재정 P-12 의 결속은 그대로다. 그러나 사후 감사는 "응답
    뒤에 요청이 바뀌었다"로 읽고, 그 오독을 없애는 값싼 방법이 **쓰지 않는 것**이다.
    시각에 기대지 않으려고 과거 시각을 박고 `st_mtime_ns` 로 본다(결정론).
    """
    root = os.path.join(str(tmp_path), "lanes")
    adapter = FileLaneAdapter(root, REPO)
    request = m2.plan_decompose(
        "read-a", ReadView(m2.SOURCE, m2.RULES), lane_profiles(REPO), repo=REPO
    )[0]

    directory = adapter.write_request(request)
    paths = [os.path.join(directory, name) for name in ("request.json", "request.md")]
    for path in paths:
        if not os.path.isfile(path):
            pytest.fail(f"요청 파일이 쓰이지 않았다: {path}")
        os.utime(path, ns=(1_000_000_000_000_000_000, 1_000_000_000_000_000_000))
    before = {path: os.stat(path).st_mtime_ns for path in paths}

    # ⓐ 같은 요청으로 재진입 — 바이트가 같으므로 아무것도 쓰지 않는다.
    adapter.write_request(request)
    for path in paths:
        after = os.stat(path).st_mtime_ns
        if after != before[path]:
            pytest.fail(f"내용이 같은데 다시 썼다: {os.path.basename(path)} {before[path]} → {after}")

    # ⓑ 대조군 — 요청이 실제로 바뀌면 파일도 지문도 바뀐다(과잉 제약 배제).
    changed = m2.plan_decompose(
        "read-a",
        ReadView(m2.SOURCE, m2.RULES),
        lane_profiles(REPO),
        0,
        [{"check": "read.convergence", "rule": "dependent-set", "locus": "CL-2",
          "message": "갈렸다", "found": "0.88", "expected": "1.0"}],
        repo=REPO,
    )[0]
    if changed.input_digest == request.input_digest:
        pytest.fail("지시문을 바꿨는데 지문이 그대로다 — 대조군이 성립하지 않는다")
    adapter.write_request(changed)
    for path in paths:
        if os.stat(path).st_mtime_ns == before[path]:
            pytest.fail(f"요청이 바뀌었는데 파일이 그대로다: {path}")
    written = load_json(paths[0])
    if written["input_digest"] != changed.input_digest:
        pytest.fail(f"갱신된 요청의 지문이 파일에 없다: {written['input_digest']}")


# ===========================================================================
# ④-2 재정 Q3 ⓑ — 핀 불일치 halt 의 진단문
# ===========================================================================


def test_pin_mismatch_halt_explains_that_the_supersede_mark_is_absent(tmp_path) -> None:
    """이 시험이 없으면 halt 가 **자기가 남기지 않은 것**을 말하지 않는다(재정 2026-08-19 Q3 ⓑ).

    핀 검사(P-U1)가 진입 검사(P-U2 표시)보다 먼저 도는 현행 순서는 그대로 둔다. 대신 halt 가
    그 귀결을 스스로 말한다 — 원천 변경과 리포 개정이 함께 오면(실무에서 흔하다) 구 런에는
    표시가 아직 서지 않으며, 그 부재를 "원천이 그대로였다"로 읽으면 안 된다.
    """
    law = m2.make_law_repo(os.path.join(str(tmp_path), "law"))
    root, outcome = m2.run_source(tmp_path, repo=law)
    if outcome["status"] != "ok":
        pytest.fail(f"첫 런이 열리지 않았다: {outcome['status']}")
    pinned = ((load_yaml(RunPaths(root).run_yaml) or {}).get("engine") or {}).get("commit")

    # 리포 개정 — 실무의 그 순서다(원천을 다시 만지는 사이 리포가 앞으로 나간다).
    with open(os.path.join(law, "contracts", "format-parameters.yaml"), "a", encoding="utf-8") as handle:
        handle.write("\n# 런 개시 뒤의 개정\n")
    m2.commit_law(law, "런 개시 뒤의 리포 개정")

    with pytest.raises(StageHaltError) as excinfo:
        m2.run_source(tmp_path, repo=law, run_root=root)
    diagnosis = str(excinfo.value)

    for needle in (
        "[halt]",
        "재정 P-U1",
        str(pinned),
        "재정 P-U2",
        "superseded-by-source-change",
        "아직",
        "run_worktree.py create",
    ):
        if needle not in diagnosis:
            pytest.fail(f"핀 halt 진단에 {needle!r} 이 없다: {diagnosis}")

    # 진단이 말한 것이 사실인가 — 표시는 정말로 서지 않았다.
    meta = load_yaml(RunPaths(root).run_yaml) or {}
    if meta.get("status") == "superseded-by-source-change":
        pytest.fail("진단은 '표시가 서지 않았다'는데 실제로는 서 있다")

    # 계약도 같은 사실을 든다 — 어휘와 순서의 정본은 계약이다.
    contract = load_stage_contract("source", None)
    order_note = str((contract.get("run_binding") or {}).get("order_before_entry_checks", ""))
    for needle in ("superseded-by-source-change", "진단문"):
        if needle not in order_note:
            pytest.fail(f"source.yaml 이 순서의 귀결을 적지 않았다: {order_note!r}")


# ---------------------------------------------------------------------------
# ⑦ 관문 승격의 대가 — 환경 오류가 검증 실패로 오독되지 않는가 (재정 H7 · sol 감수 A′)
# ---------------------------------------------------------------------------


def test_lane_binding_gate_reports_env_failure_as_exit_two() -> None:
    """이 시험이 없으면 **환경 때문에 막힌 커밋이 "레인 결속이 깨졌다"로 적힌다**.

    재정 2026-08-19 **H7** 이 `tools/check_lane_binding.py` 를 커밋 전 필수 관문의 넷째로
    올렸다. 그 직후 sol 감수 A′ 가 읽기 전용 샌드박스(쓸 수 있는 `/tmp` 없음)에서 이 도구만
    `FileNotFoundError` 트레이스백과 함께 **exit 1** 로 죽는 것을 실측했다 — SPEC §8.3 3항의
    종료 코드 규약은 `1` = 검증 실패 · `2` = 입력·환경 오류이므로, 그 자리는 규약 위반이었다.
    관문이 된 도구가 두 사건을 같은 코드로 말하면 그 신호는 마모된다.

    **서브프로세스의 종료 코드는 테스트 안에서도 명시 비교로 본다**(CLAUDE.md §3).
    """
    program = textwrap.dedent(
        """
        import runpy, sys, tempfile
        def boom(*args, **kwargs):
            raise FileNotFoundError(2, "No usable temporary directory found in ['/tmp']")
        tempfile.mkdtemp = boom
        sys.argv = ["check_lane_binding.py"]
        runpy.run_path("tools/check_lane_binding.py", run_name="__main__")
        """
    )
    for optimized in (False, True):
        argv = [sys.executable] + (["-O"] if optimized else []) + ["-c", program]
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=REPO)
        if proc.returncode != 2:
            pytest.fail(
                f"임시 작업장 실패의 종료 코드가 {proc.returncode} 다 — 기대 2"
                f"({'-O' if optimized else 'plain'}) · stderr={proc.stderr[-400:]}"
            )
        if "ENVIRONMENT ERROR" not in (proc.stderr + proc.stdout):
            pytest.fail(f"환경 오류 표기가 없다: {proc.stderr[-400:]}")
