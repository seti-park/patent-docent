# -*- coding: utf-8 -*-
"""재정 2026-09-01 T17 의 '계속' 봉투 적용 범위를 반증한다."""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine.paths import RunPaths  # noqa: E402


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def phantom_claim_payload() -> dict:
    payload = m2.payload_set()
    phantom = copy.deepcopy(payload["decompose"]["claims"]["dependents"][0])
    phantom["id"] = "CL-9"
    payload["decompose"]["claims"]["dependents"].append(phantom)
    return payload


def run_twice_with_envelope(tmp_path, *, payloads_by_run: dict):
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source status 기대 ok, 실제 {source_outcome['status']}")
    lanes_root = m2.write_lane_responses(root, payloads_by_run=payloads_by_run)
    first_adapter = m2.ReplayLaneAdapter(lanes_root)
    first = m2.run_read_stage(run_root=root, adapter=first_adapter, rules=m2.RULES)
    verdict = RunPaths(root).convergence_early_json
    if not os.path.isfile(verdict):
        pytest.fail(f"봉투 결속 대상 판정서가 실재해야 한다: {verdict}")
    m2._write_continue_envelope(root)
    second_adapter = m2.ReplayLaneAdapter(lanes_root)
    second = m2.run_read_stage(run_root=root, adapter=second_adapter, rules=m2.RULES)
    gate = load_json(RunPaths(root).phase_gate_json)
    return root, first, second, second_adapter, gate


def claim_failure_batch() -> dict:
    broken = phantom_claim_payload()
    return {"read-a": m2.payload_set(), "read-b": broken}


def test_envelope_does_not_carry_an_early_claim_failure(tmp_path) -> None:
    """이 시험이 없으면 T17의 반증 조건인 '유효한 봉투도 청구항 결함은 못 넘긴다'가 공허해진다."""
    _, _, outcome, adapter, gate = run_twice_with_envelope(
        tmp_path, payloads_by_run=claim_failure_batch()
    )
    if outcome["status"] == "ok":
        pytest.fail(f"청구항 실패 + 봉투 status 기대 ok 아님, 실제 {outcome['status']!r}")
    spent = [task for task in adapter.tasks_dispatched() if task.startswith("ground")]
    if spent:
        pytest.fail(f"범위 밖 봉투인데 접지 레인 기대 0건, 실제 {spent}")
    expected = {
        "present": True,
        "valid": True,
        "in_scope": False,
        "applied": False,
        "blocked_by": "claim-checks",
        "entered": False,
    }
    actual = {
        "present": gate.get("envelope", {}).get("present"),
        "valid": gate.get("envelope", {}).get("valid"),
        "in_scope": gate.get("envelope", {}).get("in_scope"),
        "applied": gate.get("envelope", {}).get("applied"),
        "blocked_by": gate.get("blocked_by"),
        "entered": gate.get("entered"),
    }
    if actual != expected:
        pytest.fail(f"청구항 차단 게이트 기대 {expected!r}, 실제 {actual!r}")


def test_envelope_still_carries_the_escalation_axis(tmp_path) -> None:
    """이 시험이 없으면 봉투 범위 좁힘이 과해져 상신 축까지 막았는지 드러나지 않는다."""
    payloads = {
        "read-a": m2.payload_set(),
        "read-b": m2.payload_set(element_two=m2.E2_TEXT_VARIANT),
    }
    _, _, _, adapter, gate = run_twice_with_envelope(tmp_path, payloads_by_run=payloads)
    if "ground-independent" not in adapter.tasks_dispatched():
        pytest.fail(
            "상신 축의 유효 봉투 기대 ground-independent 발송, 실제 "
            f"{adapter.tasks_dispatched()!r}"
        )
    expected = {
        "blocked_by": "convergence-escalation",
        "present": True,
        "valid": True,
        "in_scope": True,
        "applied": True,
        "entered": True,
    }
    actual = {
        "blocked_by": gate.get("blocked_by"),
        "present": gate.get("envelope", {}).get("present"),
        "valid": gate.get("envelope", {}).get("valid"),
        "in_scope": gate.get("envelope", {}).get("in_scope"),
        "applied": gate.get("envelope", {}).get("applied"),
        "entered": gate.get("entered"),
    }
    if actual != expected:
        pytest.fail(f"상신 축 게이트 기대 {expected!r}, 실제 {actual!r}")


def test_phase_gate_records_why_the_envelope_did_not_apply(tmp_path) -> None:
    """이 시험이 없으면 봉투가 있는데도 멈춘 이유와 처분을 다음 사람이 코드에서 다시 추적해야 한다."""
    _, _, outcome, _, gate = run_twice_with_envelope(
        tmp_path, payloads_by_run=claim_failure_batch()
    )
    reason = str(gate.get("reason", ""))
    missing = [token for token in ("T17", "분해 재시도", "계속 봉투 유효") if token not in reason]
    if missing:
        pytest.fail(f"게이트 사유 기대 T17·처분·유효 봉투 사실, 누락 {missing}, 실제 {reason!r}")
    if outcome.get("gate_note") != reason:
        pytest.fail(
            f"러너 gate_note 기대 산출 reason 과 동일 {reason!r}, 실제 {outcome.get('gate_note')!r}"
        )
