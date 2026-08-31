# -*- coding: utf-8 -*-
"""`read.lane-log-digest-value` — 레인 로그 지문의 **값** 대조 (재정 2026-08-31 Q1).

**이 파일이 지키는 주장 하나**: 로그에 적힌 요청 파일 지문이 **그 자리의 파일과 같은가**.
형태(칸의 있음·빈 값 아님·면제의 명시)는 형제 검사 `read.lane-log-shape` 의 소관이며 여기서
다시 세지 않는다 — 그 분리가 재정 Q1 의 내용이다.

**무엇이 이 검사를 만들었는가**(2026-08-19 감수 D 의 변조표 실측):

    M-D 값만 `ffff…ffff` 로 위조   → **NOT DETECTED** (`pass checked=5 violations=0`)
    M-E 파일 어댑터 행을 `null` 위장 → **NOT DETECTED** (`exempt` 계수만 늘고 통과)
    M-C 소비 후 `request.md` 교체   → 사람이 손으로 대조해야만 드러남

셋 다 여기서 기계 판정으로 옮겨진다. **뒤집기 검증을 함께 둔다** — 위조가 실제로 FAIL 하는
것만 보이면 그 검사가 무엇이든 FAIL 하는 것일 수도 있으므로, 정직한 왕복이 **통과하는** 것을
같은 하네스가 함께 보인다(공허하지 않음의 실증).

`assert` 는 pytest 가 AST 를 재작성하므로 시험 모듈에서 허용된다(CLAUDE.md §3) — 다만 이
파일은 명시 비교 + `pytest.fail` 형태를 쓴다(러너 시험 관례를 따른다).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.lanes.contract import REQUEST_MD, LaneRequest  # noqa: E402
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.stages.read import (  # noqa: E402
    ENGINE_READ_CHECK_IDS,
    LANE_LOG_DIGEST_VALUE_CHECK_ID,
    LaneJournal,
    _dispatch,
    check_lane_log_digest_value,
    check_lane_log_shape,
)

LANE_ID = "read-a/decompose/batch-0"
MODEL = "opus-5"
EFFORT = "max"
PROCEDURE = "reader/procedure/10-decompose.md"
RESPONSE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["items"],
    "properties": {"items": {"type": "array"}},
}


def _request(repo: str = REPO) -> LaneRequest:
    return LaneRequest(
        lane_id=LANE_ID,
        read_run="read-a",
        task="decompose",
        model=MODEL,
        effort=EFFORT,
        prompt_path=PROCEDURE,
        repo_root=repo,
        instructions="청구항 구간 전량을 분해한다.",
        slices={"claims": "1. An apparatus comprising a frame."},
        response_schema=RESPONSE_SCHEMA,
        batch=0,
    )


def _write_response(path: str, echo: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "lane_id": LANE_ID,
                "model": MODEL,
                "effort": EFFORT,
                "input_digest": echo,
                "payload": {"items": [{"id": "M1", "kind": "component"}]},
            },
            handle,
            ensure_ascii=False,
        )


def _honest_round_trip(tmp_path) -> tuple[LaneJournal, str]:
    """정직한 왕복 1건. 반환 = (레인 로그, 레인 루트).

    **실제 러너 경로**(`_dispatch`)와 **실 운용 어댑터**(`FileLaneAdapter`)를 쓴다 — 로그 행을
    손으로 지어내면 이 시험이 재는 것이 러너가 아니라 시험 자신이 된다.
    """
    lanes_root = os.path.join(str(tmp_path), "10-read", "lanes")
    adapter = FileLaneAdapter(lanes_root, REPO)
    request = _request()
    adapter.write_request(request)
    _write_response(
        os.path.join(lanes_root, *LANE_ID.split("/"), "response.json"),
        request.input_digest,
    )
    journal = LaneJournal()
    _dispatch(adapter, [request], journal)
    return journal, lanes_root


# ---------------------------------------------------------------------------
# 시나리오 ③ — 정상 통과 (뒤집기 검증: 이 검사가 무엇이든 FAIL 하는 것이 아님)
# ---------------------------------------------------------------------------


def test_honest_round_trip_passes_and_verifies_the_value(tmp_path) -> None:
    """정직한 왕복은 통과하고, **대조를 실제로 했다는 사실**이 산출에 남는다.

    `pass` 만으로는 부족하다 — 아무것도 대조하지 않아도 `pass` 이기 때문이다. 그래서
    `digest_verified` 가 1 인지 함께 본다(공허 통과가 아님의 실증).
    """
    journal, lanes_root = _honest_round_trip(tmp_path)
    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "pass":
        pytest.fail(f"정직한 왕복이 막혔다: {[f.message for f in row.findings]}")
    if row.extras["digest_verified"] != 1:
        pytest.fail(
            f"값 대조를 실제로 하지 않았다 — digest_verified={row.extras['digest_verified']} "
            "(통과했으나 아무것도 대조하지 않았다면 그 통과는 공허하다)"
        )
    if row.extras["exempt_verified"] or row.extras["deferred_to_shape"]:
        pytest.fail(f"면제·이월이 있어서는 안 되는 왕복이다: {row.extras}")
    if row.vacuous != "none":
        pytest.fail(f"공허 판정이 붙었다: {row.vacuous}")


def test_logged_digest_equals_the_file_a_human_can_hash(tmp_path) -> None:
    """로그의 값 = 사람이 `sha256sum request.md` 로 얻는 값. 제3자 재계산이 성립한다."""
    journal, lanes_root = _honest_round_trip(tmp_path)
    path = os.path.join(lanes_root, *LANE_ID.split("/"), REQUEST_MD)
    with open(path, "rb") as handle:
        by_hand = hashlib.sha256(handle.read()).hexdigest()
    logged = journal.rows[-1]["request_digest"]
    if logged != by_hand:
        pytest.fail(f"로그 {logged} ≠ 손계산 {by_hand}")


# ---------------------------------------------------------------------------
# 시나리오 ① — 위조값은 FAIL (감수 D 의 M-D)
# ---------------------------------------------------------------------------


def test_forged_digest_value_fails(tmp_path) -> None:
    """64자리 위조값(`ffff…ffff`)이 걸린다 — 형태 검사는 이것을 통과시켰다."""
    journal, lanes_root = _honest_round_trip(tmp_path)
    journal.rows[-1]["request_digest"] = "f" * 64

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "fail":
        pytest.fail("위조값이 통과했다 — 재정 2026-08-31 Q1 이 닫으려던 구멍 그대로다")
    rules = {finding.rule for finding in row.findings}
    if "lane-log.digest-value-mismatch" not in rules:
        pytest.fail(f"기대 규칙 lane-log.digest-value-mismatch, 실제 {sorted(rules)}")
    if row.extras["digest_verified"] != 0:
        pytest.fail("위조 행을 대조 성공으로 셌다")


def test_the_shape_check_still_passes_the_forged_value(tmp_path) -> None:
    """**관할 분리의 반증** — 같은 위조를 형제 검사는 통과시킨다.

    이 시험이 이 파일에서 가장 중요하다. 값 검사가 FAIL 하는 것만 보이면 *"형태 검사가 이미
    잡고 있었는데 하나 더 만든 것 아닌가"* 라는 물음에 답할 수 없다. 답은 여기 있다 —
    **형태 검사는 이 위조를 지금도 통과시킨다.** 그것이 재정 Q1 이 id 를 나눈 이유이고,
    2026-08-19 감수 D 가 `pass checked=5 violations=0` 으로 실측한 그 자리다.
    """
    journal, _ = _honest_round_trip(tmp_path)
    journal.rows[-1]["request_digest"] = "f" * 64

    shape = check_lane_log_shape(
        journal, read_runs=("read-a",), canonical="read-a"
    )
    forged = [
        finding
        for finding in shape.findings
        if finding.rule == "lane-log.request-file-digest"
    ]
    if forged:
        pytest.fail(
            "형태 검사가 값 위조를 잡았다 — 그렇다면 두 검사의 관할이 겹치므로 이 파일의 "
            f"전제(재정 Q1 의 분리)를 다시 보아야 한다: {[f.message for f in forged]}"
        )


# ---------------------------------------------------------------------------
# 시나리오 ② — `null` 위장은 제외로 새지 않는다 (감수 D 의 M-E)
# ---------------------------------------------------------------------------


def test_null_disguise_on_a_real_request_file_fails(tmp_path) -> None:
    """요청 파일이 **실재하는데** 로그가 `null` 을 적으면 걸린다.

    면제의 자격은 선언이 아니라 **사실**이다. 형태 검사는 `null` 을 무조건 제외로 세어
    `request_digest_exempt` 만 하나 늘리고 통과했다(감수 D 의 M-E).
    """
    journal, lanes_root = _honest_round_trip(tmp_path)
    journal.rows[-1]["request_digest"] = None

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "fail":
        pytest.fail("null 위장이 제외로 샜다 — 재정 Q1 이 닫으려던 두 번째 구멍이다")
    rules = {finding.rule for finding in row.findings}
    if "lane-log.digest-null-disguise" not in rules:
        pytest.fail(f"기대 규칙 lane-log.digest-null-disguise, 실제 {sorted(rules)}")
    if row.extras["exempt_verified"] != 0:
        pytest.fail("위장 행을 정당한 면제로 셌다")


def test_the_shape_check_still_exempts_the_disguised_null(tmp_path) -> None:
    """**관할 분리의 반증 둘째** — 같은 위장을 형태 검사는 지금도 면제로 센다."""
    journal, _ = _honest_round_trip(tmp_path)
    journal.rows[-1]["request_digest"] = None

    shape = check_lane_log_shape(
        journal, read_runs=("read-a",), canonical="read-a"
    )
    if shape.extras.get("request_digest_exempt") != 1:
        pytest.fail(
            "형태 검사가 위장을 면제로 세지 않았다 — 이 시험의 전제가 바뀌었으니 확인하라: "
            f"{shape.extras}"
        )
    # ★ 행 전체의 status 를 보지 않는다. 이 하네스의 로그에는 분해 왕복 1건뿐이라 형태 검사가
    #   `lane-log.canonical-tail`(정본 실행이 통합에 닿지 않았다)로 따로 운다 — 그것은 이
    #   시험의 관심사가 아니다. 관심사는 **지문 칸에 대한 판정**이며, 그 규칙만 골라 본다.
    digest_rules = {
        finding.rule
        for finding in shape.findings
        if finding.rule.startswith("lane-log.request")
    }
    if digest_rules:
        pytest.fail(
            "형태 검사가 null 위장을 지문 결함으로 잡았다 — 관할이 겹친다면 재정 Q1 의 "
            f"전제를 다시 보라: {sorted(digest_rules)}"
        )


def test_a_genuine_exemption_still_passes(tmp_path) -> None:
    """**면제를 없애지 않았다** — 요청 파일이 정말 없는 행은 통과한다.

    재정 Q1 은 *"`None` 면제의 현행 축소분을 되돌리지 마라"* 로 명한다. 신설 검사가 면제를
    통째로 막으면 요청 파일을 쓰지 않는 재생 어댑터의 왕복이 전부 결함이 되고, 그것은 재정이
    금지한 방향이다.
    """
    journal, lanes_root = _honest_round_trip(tmp_path)
    journal.rows[-1]["request_digest"] = None
    os.remove(os.path.join(lanes_root, *LANE_ID.split("/"), REQUEST_MD))

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "pass":
        pytest.fail(
            f"정당한 면제가 막혔다: {[f.message for f in row.findings]} — 재정 Q1 이 "
            "명시로 금지한 방향이다"
        )
    if row.extras["exempt_verified"] != 1:
        pytest.fail(f"면제를 세지 않았다: {row.extras}")


# ---------------------------------------------------------------------------
# 파생 — 사후 교체(M-C)와 파일 부재
# ---------------------------------------------------------------------------


def test_post_consumption_request_swap_is_detected(tmp_path) -> None:
    """소비 뒤 `request.md` 가 바뀌면 걸린다(감수 D 의 M-C — 손 대조에서 기계 판정으로).

    로그도 위조하지 않았고 파일 권한도 그대로다. 바뀐 것은 **파일의 내용**뿐이며, 그 사실이
    로그와 파일의 지문 차이로 드러난다.
    """
    journal, lanes_root = _honest_round_trip(tmp_path)
    path = os.path.join(lanes_root, *LANE_ID.split("/"), REQUEST_MD)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("\n\n## [변조] 소비 뒤에 덧붙인 절\n")

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "fail":
        pytest.fail("소비 후 요청 파일 교체가 탐지되지 않았다")
    rules = {finding.rule for finding in row.findings}
    if "lane-log.digest-value-mismatch" not in rules:
        pytest.fail(f"기대 규칙 lane-log.digest-value-mismatch, 실제 {sorted(rules)}")


def test_missing_request_file_with_a_declared_digest_fails(tmp_path) -> None:
    """값을 적어 놓고 파일이 없으면 걸린다 — 지문이 지목하는 대상이 사라졌다."""
    journal, lanes_root = _honest_round_trip(tmp_path)
    os.remove(os.path.join(lanes_root, *LANE_ID.split("/"), REQUEST_MD))

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    rules = {finding.rule for finding in row.findings}
    if "lane-log.digest-file-missing" not in rules:
        pytest.fail(f"기대 규칙 lane-log.digest-file-missing, 실제 {sorted(rules)}")


def test_empty_and_absent_columns_are_deferred_not_double_counted(tmp_path) -> None:
    """빈 문자열·칸 부재는 **형태 검사의 소관**이며 여기서 이중으로 세지 않는다.

    한 결함이 두 판정 행에서 두 번 울면 계수가 부풀려진다. 다만 조용히 넘기지도 않는다 —
    건수가 `deferred_to_shape` 에 남는다.
    """
    journal, lanes_root = _honest_round_trip(tmp_path)
    honest = dict(journal.rows[-1])

    empty = dict(honest, lane_id="read-a/decompose/batch-1", request_digest="")
    absent = dict(honest, lane_id="read-a/decompose/batch-2")
    absent.pop("request_digest")
    journal.rows.extend([empty, absent])

    row = check_lane_log_digest_value(journal, lanes_root=lanes_root)
    if row.status != "pass":
        pytest.fail(
            f"이월 대상을 결함으로 셌다(이중 계수): {[f.rule for f in row.findings]}"
        )
    if row.extras["deferred_to_shape"] != 2:
        pytest.fail(f"이월 건수가 기록되지 않았다: {row.extras}")
    if row.checked != 3:
        pytest.fail(f"checked 기대 3, 실제 {row.checked}")


# ---------------------------------------------------------------------------
# 등재 — 검사 id 가 사전과 계약에 함께 서 있는가 (재정 Q1 의 명시 조건)
# ---------------------------------------------------------------------------


def test_the_new_check_is_registered_in_the_engine_ledger() -> None:
    """등재부에 없으면 사전 대조 시험이 이 검사를 훑지 않는다."""
    if LANE_LOG_DIGEST_VALUE_CHECK_ID not in ENGINE_READ_CHECK_IDS:
        pytest.fail(
            f"{LANE_LOG_DIGEST_VALUE_CHECK_ID} 가 ENGINE_READ_CHECK_IDS 에 없다 — "
            "등재하지 않은 이름은 계약이 아니라 관습이 된다(glossary 머리말)"
        )


def test_the_new_check_is_declared_in_the_stage_contract() -> None:
    """계약이 모르는 검사는 사후 감사에서 근거 없는 검사가 된다(read.yaml 의 자기 규율)."""
    import yaml  # noqa: PLC0415

    contract = yaml.safe_load(
        open(os.path.join(REPO, "contracts", "stages", "read.yaml"), encoding="utf-8")
    )
    declared = [entry["id"] for entry in contract["checks_before_exit"]]
    if LANE_LOG_DIGEST_VALUE_CHECK_ID not in declared:
        pytest.fail(
            f"{LANE_LOG_DIGEST_VALUE_CHECK_ID} 가 checks_before_exit 에 없다: {declared}"
        )
