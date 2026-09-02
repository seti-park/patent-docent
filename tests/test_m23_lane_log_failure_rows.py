# -*- coding: utf-8 -*-
"""재정 2026-09-01 T22 — 레인 로그 검사 2종의 전용 실패 행을 반증한다."""

from __future__ import annotations

import copy
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.paths import load_stage_contract  # noqa: E402
from engine.stages import StageError, failure_entry  # noqa: E402
from engine.stages.read import _failure_verdict  # noqa: E402
from reader.lib.report import CheckRow  # noqa: E402


LANE_LOG_CHECKS = ("read.lane-log-shape", "read.lane-log-digest-value")
FAILURE_NEEDLES = (
    "claim-inventory",
    "상신 축",
    "read.schema 실패",
    "원천 다이제스트",
    "같은 실패 서명",
    "exact-match 축",
    "read.lane-log-shape",
    "read.lane-log-digest-value",
    "read.verbatim",
)


def test_lane_log_verdicts_come_from_their_own_failure_rows() -> None:
    """read.verbatim 행을 변조해도 두 검사의 처분은 안 움직이고 대조군만 움직인다."""
    contract = copy.deepcopy(load_stage_contract("read", None))
    verbatim = failure_entry(contract, "read.verbatim")
    verbatim["then"] = "halt"

    for check_id in LANE_LOG_CHECKS:
        actual = _failure_verdict(contract, [CheckRow(check_id=check_id)])
        if actual != ("escalate", None):
            pytest.fail(f"{check_id} 전용 행 처분 기대 ('escalate', None), 실제 {actual!r}")

    control = _failure_verdict(contract, [CheckRow(check_id="read.verbatim")])
    if control != ("halt", None):
        pytest.fail(f"변조 유효성 대조군 read.verbatim 기대 ('halt', None), 실제 {control!r}")


def test_every_failure_verdict_needle_matches_exactly_one_contract_row() -> None:
    """부분 문자열 조회의 모든 needle이 정확히 한 행만 가리켜야 처분 출처가 단일하다."""
    contract = load_stage_contract("read", None)
    conditions = [str(row.get("condition", "")) for row in contract.get("failure") or []]
    for needle in FAILURE_NEEDLES:
        matches = [condition for condition in conditions if needle in condition]
        if len(matches) != 1:
            pytest.fail(f"failure needle {needle!r} 기대 정확히 1행, 실제 {len(matches)}행: {matches!r}")


def test_failure_needles_equal_every_literal_lookup_in_read_stage() -> None:
    """read.py의 실제 failure_entry 부분문자열 조회와 유일성 목록은 양방향으로 같아야 한다."""
    path = os.path.join(REPO, "engine", "stages", "read.py")
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    actual = set(re.findall(r'failure_entry\(contract,\s*"([^"]+)"\)', source))
    expected = set(FAILURE_NEEDLES)
    if actual != expected:
        pytest.fail(
            "failure needle 목록과 read.py 실제 조회가 다르다: "
            f"목록에만={sorted(expected - actual)!r}, 코드에만={sorted(actual - expected)!r}"
        )


def test_exit_retry_budget_comment_marks_t25_exception_without_changing_values() -> None:
    """A-6: exit 재시도 선언의 T25 예외와 T26 후속 소유자가 정본 좌표에 보여야 한다."""
    path = os.path.join(REPO, "contracts", "stages", "read.yaml")
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    marker = "★ 재정 2026-09-02 T25"
    if marker not in source or "T26" not in source:
        pytest.fail(f"exit retry_budget 주석에 T25 예외·T26 포인터가 없다: marker={marker!r}")


def test_repeated_signature_requires_an_exit_loop_failure() -> None:
    """감사 Q5: repeated=True인데 READ 출구 루프 실패가 없는 도달 불능 상태는 닫힌다."""
    contract = load_stage_contract("read", None)
    with pytest.raises(StageError, match="도달 불능 상태"):
        _failure_verdict(
            contract,
            [CheckRow(check_id="read.lane-log-shape")],
            repeated=True,
        )

    control = _failure_verdict(
        contract,
        [CheckRow(check_id="read.verbatim")],
        repeated=True,
    )
    expected = ("escalate", "국면 간 변이 재현 — 코드 결함 의심")
    if control != expected:
        pytest.fail(f"READ 루프 실패 대조군 기대 {expected!r}, 실제 {control!r}")


def test_lane_log_rows_declare_no_fictional_retry_or_reason_label() -> None:
    """두 검사는 출구 재시도 루프가 끝난 뒤 결과 목록에 합류한다.

    `engine/stages/read.py`의 루프 종료 뒤 `rows = [entry_row, *rows,
    check_lane_log_shape(...), check_lane_log_digest_value(...)]`로 붙으므로 재시도 기회는 0회다.
    `retry(n)`을 적으면 0회인 재시도를 계약이 허구로 선언하는 것이다(재정 T22).
    """
    contract = load_stage_contract("read", None)
    for check_id in LANE_LOG_CHECKS:
        row = failure_entry(contract, check_id)
        forbidden_keys = [key for key in ("points", "reason_label", "then") if key in row]
        if forbidden_keys:
            pytest.fail(f"{check_id} 전용 행에 금지 키가 있다: {forbidden_keys}")
        if str(row.get("action", "")).startswith("retry("):
            pytest.fail(f"{check_id} 전용 행이 0회인 재시도를 선언했다: {row.get('action')!r}")
        note = str(row.get("note", ""))
        missing = [token for token in ("루프", "0회", "허구", "재정 2026-09-01 T22") if token not in note]
        if missing:
            pytest.fail(f"{check_id} note 에 재시도 부재 사유가 빠졌다: {missing}")
