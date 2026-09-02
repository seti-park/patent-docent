# -*- coding: utf-8 -*-
"""감사 지적 B-1 — 재시도 상한을 계약 밖에서 지어내는 경로를 반증한다."""

from __future__ import annotations

import copy
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.paths import load_stage_contract  # noqa: E402
from engine.stages.read import RunnerContractError, _retry_budget, _retry_checks  # noqa: E402


def test_missing_judgment_point_is_refused_not_defaulted() -> None:
    """계약에 없는 판정점을 기본 상한으로 덮으면 계약 부재가 정상 실행으로 세탁된다."""
    contract = load_stage_contract("read", None)
    control = _retry_budget(contract, "early")
    if type(control) is not int:
        pytest.fail(f"실계약 early 대조군 기대 정수, 실제 {control!r}")
    broken = copy.deepcopy(contract)
    points = (broken.get("retry_budget") or {}).get("points") or []
    broken["retry_budget"]["points"] = [point for point in points if point.get("id") != "early"]
    with pytest.raises(RunnerContractError):
        _retry_budget(broken, "early")


def test_non_integer_max_retries_is_refused() -> None:
    """문자열·실수·불을 정수 상한으로 받으면 선언 형식의 거부 경계가 사라진다."""
    contract = load_stage_contract("read", None)
    for invalid in ("1", 1.0, True):
        broken = copy.deepcopy(contract)
        early = next(
            point
            for point in broken["retry_budget"]["points"]
            if point.get("id") == "early"
        )
        early["max_retries"] = invalid
        with pytest.raises(RunnerContractError):
            _retry_budget(broken, "early")

    zero = copy.deepcopy(contract)
    early = next(point for point in zero["retry_budget"]["points"] if point.get("id") == "early")
    early["max_retries"] = 0
    if _retry_budget(zero, "early") != 0:
        pytest.fail("max_retries: 0 대조군이 유효한 '재시도 없음' 선언으로 통과하지 않았다")


def test_the_refusal_is_what_the_spec_says_it_is() -> None:
    """문서의 거부 주장과 런타임 경계를 함께 묶지 않으면 둘 중 한 벌이 낡는다."""
    path = os.path.join(REPO, "docs", "SPEC.md")
    with open(path, encoding="utf-8") as handle:
        spec = handle.read()
    wording = "기본값을 지어내지 않고 거부한다"
    if wording not in spec:
        pytest.fail(f"docs/SPEC.md §1.4 에 재시도 상한 거부 문언이 없다: {wording!r}")


def test_retry_checks_rejects_missing_shape_unknown_entry_duplicate_and_point_duplicate() -> None:
    contract = load_stage_contract("read", None)

    missing = copy.deepcopy(contract)
    missing["retry_budget"]["points"] = [
        row for row in missing["retry_budget"]["points"] if row.get("id") != "exit"
    ]
    with pytest.raises(RunnerContractError):
        _retry_checks(missing, "exit")

    for bad in ("not-a-list", ["read.__ghost__"], ["read.input-digest"]):
        broken = copy.deepcopy(contract)
        point = next(row for row in broken["retry_budget"]["points"] if row["id"] == "exit")
        point["checks"] = bad
        with pytest.raises(RunnerContractError):
            _retry_checks(broken, "exit")

    duplicate = copy.deepcopy(contract)
    point = next(row for row in duplicate["retry_budget"]["points"] if row["id"] == "exit")
    point["checks"].append(point["checks"][0])
    with pytest.raises(RunnerContractError):
        _retry_checks(duplicate, "exit")

    duplicate_point = copy.deepcopy(contract)
    point = next(row for row in duplicate_point["retry_budget"]["points"] if row["id"] == "exit")
    duplicate_point["retry_budget"]["points"].append(copy.deepcopy(point))
    with pytest.raises(RunnerContractError):
        _retry_checks(duplicate_point, "exit")
