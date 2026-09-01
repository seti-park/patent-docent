# -*- coding: utf-8 -*-
"""감사 Y-3 — phase_gates[0] 선언을 실제 판정서·코드 어휘에 양방향 결속한다."""

from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from engine.paths import RunPaths, load_stage_contract  # noqa: E402
import engine.stages.read as read_stage  # noqa: E402
from test_m22_continue_envelope_scope import (  # noqa: E402
    claim_failure_batch,
    load_json,
    run_twice_with_envelope,
)


def phase_gate_contract() -> dict:
    contract = load_stage_contract("read")
    gates = contract.get("phase_gates") or []
    if len(gates) != 1 or not isinstance(gates[0], dict):
        pytest.fail(f"read.phase_gates 기대 매핑 1건, 실제 {gates!r}")
    return gates[0]


def test_verdict_artifact_keys_equal_actual_phase_gate_keys(tmp_path) -> None:
    """선언 키와 실제 러너 산출 키가 양방향 상등이어야 누락·유령 선언을 함께 잡는다."""
    root, _, _, _, _ = run_twice_with_envelope(
        tmp_path, payloads_by_run=claim_failure_batch()
    )
    artifact = load_json(RunPaths(root).phase_gate_json)
    declared = set((phase_gate_contract().get("verdict_artifact_keys") or {}).keys())
    actual = set(artifact.keys())
    if declared != actual:
        pytest.fail(
            "phase-gate.json 최상위 키와 verdict_artifact_keys 불일치: "
            f"산출 누락 선언={sorted(declared - actual)}, 미선언 산출={sorted(actual - declared)}"
        )


def test_blocked_by_vocabulary_equals_engine_constants() -> None:
    """계약 blocked_by 어휘가 엔진이 발행할 수 있는 PHASE_GATE_* 값 전종과 정확히 같다."""
    vocabulary = phase_gate_contract().get("blocked_by_vocabulary") or []
    malformed = [entry for entry in vocabulary if not isinstance(entry, dict) or not entry.get("meaning")]
    if malformed:
        pytest.fail(f"blocked_by_vocabulary 값·뜻 형식이 불완전하다: {malformed!r}")
    declared = {str(entry.get("value")) for entry in vocabulary}
    code_values = {
        value
        for name, value in vars(read_stage).items()
        if name.startswith("PHASE_GATE_") and isinstance(value, str)
    }
    if declared != code_values:
        pytest.fail(
            "blocked_by_vocabulary 와 엔진 상수 불일치: "
            f"계약 전용={sorted(declared - code_values)}, 코드 전용={sorted(code_values - declared)}"
        )


def test_envelope_scope_values_belong_to_blocked_by_vocabulary() -> None:
    """봉투 적용·배제 라벨은 모두 blocked_by 어휘 안에서만 골라야 한다."""
    gate = phase_gate_contract()
    vocabulary = {
        str(entry.get("value"))
        for entry in gate.get("blocked_by_vocabulary") or []
        if isinstance(entry, dict)
    }
    scope = gate.get("envelope_scope") or {}
    scoped = set(scope.get("applies_to") or []) | set(scope.get("not_applies_to") or [])
    outside = scoped - vocabulary
    if outside:
        pytest.fail(f"envelope_scope 에 blocked_by 어휘 밖 라벨이 있다: {sorted(outside)}")


def test_phase_gate_declarations_are_bound_or_classified() -> None:
    """phase_gates[0] 각 선언 키의 강제 층을 빠짐·중복 없이 분류한다."""
    gate = phase_gate_contract()
    status = gate.get("binding_status") or {}
    categories = {
        name: set(status.get(name) or [])
        for name in ("runner_reads", "test_bound", "prose_only")
    }
    classified = set().union(*categories.values())
    duplicates = {
        key
        for key in classified
        if sum(key in values for values in categories.values()) > 1
    }
    if duplicates:
        pytest.fail(f"phase_gates[0] 결속 분류가 겹친 키: {sorted(duplicates)}")
    actual = set(gate) - {"binding_status"}
    if classified != actual:
        pytest.fail(
            "phase_gates[0] 결속 분류 불일치: "
            f"미분류={sorted(actual - classified)}, 존재하지 않는 분류={sorted(classified - actual)}"
        )
