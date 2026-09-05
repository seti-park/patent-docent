# -*- coding: utf-8 -*-
"""T26 실패표 계약·엔진·관문 사이의 독립 다리와 역프로브."""

from __future__ import annotations

import ast
import copy
import importlib.util
import os
import pathlib
import subprocess
import sys

import pytest
import yaml

REPO = pathlib.Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))
import test_m2_read as m2  # noqa: E402

from engine.paths import load_stage_contract  # noqa: E402
from engine.stages import (  # noqa: E402
    StageError,
    TERMINAL_ACTIONS as ENGINE_TERMINAL_ACTIONS,
    failure_row_of_kind,
    failure_rows_for_checks,
    select_failure_row,
    terminal_action,
)
from engine.stages.read import (  # noqa: E402
    CONVERGENCE_CHECK_ID,
    EARLY_RETRY_CHECK_IDS,
    ENGINE_READ_CHECK_IDS,
    EXIT_RETRY_CHECK_IDS,
    RETRY_POINT_IDS,
    RunnerContractError,
    _gate_escalation_verdict,
    _validate_retry_contract,
)
from reader.lib import EARLY_CLAIM_CHECK_IDS, READ_CHECK_IDS  # noqa: E402


TOOL = REPO / "tools" / "check_failure_table.py"
_tool_spec = importlib.util.spec_from_file_location("check_failure_table", TOOL)
if _tool_spec is None or _tool_spec.loader is None:
    pytest.fail(f"관문 적재 명세를 만들 수 없다: {TOOL}")
gate = importlib.util.module_from_spec(_tool_spec)
_tool_spec.loader.exec_module(gate)


def _point(contract: dict, point: str) -> dict:
    return next(row for row in contract["retry_budget"]["points"] if row.get("id") == point)


def _check_row(contract: dict, check_id: str) -> dict:
    return failure_rows_for_checks(contract, {check_id})[0]


def _run_gate(path: pathlib.Path, optimized: bool = False, self_test: bool = False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(TOOL), "--contract", str(path)])
    if self_test:
        command.append("--self-test")
    return subprocess.run(command, cwd=REPO, text=True, capture_output=True, check=False)


def test_entry_guard_rejects_point_and_approved_set_mutations() -> None:
    contract = load_stage_contract("read", None)
    mutations = []

    missing_early = copy.deepcopy(contract)
    missing_early["retry_budget"]["points"] = [row for row in missing_early["retry_budget"]["points"] if row["id"] != "early"]
    mutations.append(missing_early)

    duplicate_exit = copy.deepcopy(contract)
    duplicate_exit["retry_budget"]["points"].append(copy.deepcopy(_point(duplicate_exit, "exit")))
    mutations.append(duplicate_exit)

    early_without_convergence = copy.deepcopy(contract)
    _point(early_without_convergence, "early")["checks"].remove("read.convergence")
    mutations.append(early_without_convergence)

    coherent = copy.deepcopy(contract)
    _point(coherent, "exit")["checks"].remove("read.value-derivation")
    _check_row(coherent, "read.value-derivation")["checks"].remove("read.value-derivation")
    coherent["failure"].append({"checks": ["read.value-derivation"], "action": "escalate", "condition": "split", "note": "split"})
    mutations.append(coherent)

    for broken in mutations:
        with pytest.raises(RunnerContractError):
            _validate_retry_contract(broken)


def test_coherent_retry_tamper_is_rejected_before_dispatch(tmp_path, monkeypatch) -> None:
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    contract = copy.deepcopy(load_stage_contract("read", None))
    _point(contract, "exit")["checks"].remove("read.value-derivation")
    _check_row(contract, "read.value-derivation")["checks"].remove("read.value-derivation")
    contract["failure"].append({"checks": ["read.value-derivation"], "action": "escalate", "condition": "split", "note": "split"})

    import engine.paths as paths_mod

    original = paths_mod.load_stage_contract

    def load(stage_id: str, repo: str | None = None):
        if stage_id == "read":
            return copy.deepcopy(contract)
        return original(stage_id, repo)

    monkeypatch.setattr(paths_mod, "load_stage_contract", load)
    lanes_root = os.path.join(root, "10-read", "lanes")
    adapter = m2.ReplayLaneAdapter(lanes_root)
    with pytest.raises(RunnerContractError):
        m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    if adapter.dispatched:
        pytest.fail(f"진입 가드 거부 전에 레인이 디스패치됐다: {[r.lane_id for r in adapter.dispatched]!r}")


def test_terminal_action_and_gate_escalation_fail_closed() -> None:
    contract = load_stage_contract("read", None)
    schema = _check_row(contract, "read.schema")
    mutations = []
    no_then = copy.deepcopy(schema); no_then.pop("then"); mutations.append(no_then)
    retry_then = copy.deepcopy(schema); retry_then["then"] = "retry(1)"; mutations.append(retry_then)
    nonretry_then = copy.deepcopy(failure_row_of_kind(contract, "gate-escalation")); nonretry_then["then"] = "halt"; mutations.append(nonretry_then)
    for row in mutations:
        with pytest.raises(StageError):
            terminal_action(row)

    for key, value in (("then", "halt"), ("action", "__bogus__")):
        broken = copy.deepcopy(contract)
        failure_row_of_kind(broken, "gate-escalation")[key] = value
        with pytest.raises(StageError):
            _gate_escalation_verdict(broken)

    with pytest.raises(StageError):
        select_failure_row(contract, [])


def test_upstream_defect_exists_is_unique_and_has_no_engine_caller() -> None:
    contract = load_stage_contract("read", None)
    row = failure_row_of_kind(contract, "upstream-defect")
    if row.get("action") != "reject-upstream" or "checks" in row:
        pytest.fail(f"upstream-defect 계약 행이 틀렸다: {row!r}")
    calls = []
    for path in (REPO / "engine").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "failure_row_of_kind":
                continue
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and node.args[1].value == "upstream-defect":
                calls.append(f"{path}:{node.lineno}")
    if calls:
        pytest.fail(f"upstream-defect 엔진 호출자 기대 0, 실제 {calls!r}")


def test_failure_binding_status_classifies_exactly_the_used_keys() -> None:
    contract = load_stage_contract("read", None)
    status = contract.get("failure_binding_status") or {}
    used = {key for row in contract["failure"] for key in row}
    classified = set(status.get("runner_reads") or []) | set(status.get("test_bound") or []) | set(status.get("prose_only") or [])
    if used != classified:
        pytest.fail(f"failure 결속 차집합: 사용에만={sorted(used-classified)!r}, 분류에만={sorted(classified-used)!r}")
    deferred = status.get("deferred") or []
    expected = [row for row in deferred if row.get("key") == "kind" and row.get("value") == "upstream-defect" and row.get("binding") == "test_bound"]
    if len(expected) != 1:
        pytest.fail(f"upstream-defect deferred/test_bound 기대 1행, 실제 {expected!r}")
    retry_status = contract["retry_budget"]["binding_status"]
    if "checks" not in (retry_status.get("runner_reads") or []):
        pytest.fail("retry_budget.binding_status.runner_reads에 checks가 없다")


def test_gate_plain_optimized_self_test_and_five_real_yaml_mutations(tmp_path) -> None:
    canonical = load_stage_contract("read", None)
    contract_path = tmp_path / "read.yaml"
    contract_path.write_text(yaml.safe_dump(canonical, allow_unicode=True, sort_keys=False), encoding="utf-8")
    plain = _run_gate(contract_path)
    optimized = _run_gate(contract_path, optimized=True)
    if plain.returncode != 0 or optimized.returncode != 0 or plain.stdout != optimized.stdout:
        pytest.fail(f"관문 plain/-O 불일치: plain={plain.returncode}/{plain.stdout!r}, O={optimized.returncode}/{optimized.stdout!r}")
    self_plain = _run_gate(contract_path, self_test=True)
    self_opt = _run_gate(contract_path, optimized=True, self_test=True)
    if self_plain.returncode != 0 or self_opt.returncode != 0:
        pytest.fail(f"관문 self-test 실패: plain={self_plain.stdout!r}, O={self_opt.stdout!r}")

    probes = []
    one = copy.deepcopy(canonical); one["checks_before_exit"].append({"id": "read.__ghost__", "phases": ["exit"]}); probes.append(one)
    ten = copy.deepcopy(canonical); _check_row(ten, "read.verbatim")["points"] = ["early"]; probes.append(ten)
    seventeen = copy.deepcopy(canonical); next(row for row in seventeen["checks_before_exit"] if row["id"] == "read.schema")["phases"].append("__ghost_phase__"); probes.append(seventeen)
    twenty_one = copy.deepcopy(canonical); _point(twenty_one, "exit")["checks"].remove("read.value-derivation"); _check_row(twenty_one, "read.value-derivation")["checks"].remove("read.value-derivation"); twenty_one["failure"].append({"checks": ["read.value-derivation"], "action": "escalate", "condition": "split", "note": "split"}); probes.append(twenty_one)
    thirty = copy.deepcopy(canonical); _point(thirty, "early")["max_retries"] = True; probes.append(thirty)
    for index, probe in enumerate(probes, 1):
        path = tmp_path / f"probe-{index}.yaml"
        path.write_text(yaml.safe_dump(probe, allow_unicode=True, sort_keys=False), encoding="utf-8")
        result = _run_gate(path)
        if result.returncode != 1:
            pytest.fail(f"관문 실물 변조 {index} 기대 exit 1, 실제 {result.returncode}: {result.stdout!r}")


def test_terminal_and_retry_constants_are_equal_across_layers() -> None:
    expected_terminal = {"halt", "reject-upstream", "escalate"}
    if set(gate.TERMINAL_ACTIONS) != set(ENGINE_TERMINAL_ACTIONS) or set(gate.TERMINAL_ACTIONS) != expected_terminal:
        pytest.fail("관문·엔진 종단 어휘 두 벌이 정확히 같지 않다")
    expected_retry = {"early": set(EARLY_RETRY_CHECK_IDS), "exit": set(EXIT_RETRY_CHECK_IDS)}
    actual_retry = {key: set(value) for key, value in gate.APPROVED_RETRY_CHECKS.items()}
    if actual_retry != expected_retry:
        pytest.fail(f"관문·엔진 승인 재시도 집합이 다르다: {actual_retry!r}")


def test_contract_engine_constant_bridge_is_bidirectional() -> None:
    contract = load_stage_contract("read", None)
    exit_ids = [row["id"] for row in contract["checks_before_exit"]]
    entry_ids = [row["id"] for row in contract["checks_on_entry"]]
    engine_exit = set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS)
    if len(exit_ids) != len(set(exit_ids)) or set(exit_ids) != engine_exit:
        pytest.fail(f"출구 선언↔엔진 상수 불일치: 선언={exit_ids!r}")
    if len(entry_ids) != len(set(entry_ids)) or set(entry_ids) != {"read.input-digest"}:
        pytest.fail(f"진입 선언 불일치: {entry_ids!r}")
    for point in contract["retry_budget"]["points"]:
        if not set(point["checks"]) <= set(exit_ids):
            pytest.fail(f"{point['id']} 재시도 목록이 출구 선언의 부분집합이 아니다")
    if set(EARLY_RETRY_CHECK_IDS) != set(EARLY_CLAIM_CHECK_IDS) | {CONVERGENCE_CHECK_ID}:
        pytest.fail("early 승인 상수 다리가 끊겼다")
    if not set(EXIT_RETRY_CHECK_IDS) < set(exit_ids):
        pytest.fail("exit 승인 8종이 출구 12종의 진부분집합이 아니다")
    if set(RETRY_POINT_IDS) != {"early", "exit"}:
        pytest.fail(f"RETRY_POINT_IDS가 두 판정점이 아니다: {RETRY_POINT_IDS!r}")


EXIT_UNIVERSE = set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS)
# 재정 T24·T25: source-digest halt는 출구 재시도 예산을 쓰지 않는다.
HALT_EXIT_CHECKS = {"read.source-digest"}
# 재정 T28 β: convergence가 든 출구 실패 집합은 재디스패치하지 않는다.
BETA_EXCLUDED = {CONVERGENCE_CHECK_ID}
# 재정 T22: lane-log 두 검사는 출구 루프 뒤 합류하므로 retry(n) 대상이 아니다.
POST_LOOP_NO_RETRY = {"read.lane-log-shape", "read.lane-log-digest-value"}


def test_ledger_exclusions_derive_exit_retry_independently() -> None:
    """T22·T24·T25·T28·T29 도출 — 계약·엔진·관문 사본과 독립."""
    if len(EXIT_UNIVERSE) != 12:
        pytest.fail(f"T29 출구 검사 우주 기대 12종, 실제 {len(EXIT_UNIVERSE)}종")
    exclusions = (HALT_EXIT_CHECKS, BETA_EXCLUDED, POST_LOOP_NO_RETRY)
    if any(not excluded <= EXIT_UNIVERSE for excluded in exclusions):
        pytest.fail("명시 배제 집합이 T29 출구 검사 우주의 부분집합이 아니다")
    if any(left & right for index, left in enumerate(exclusions) for right in exclusions[index + 1 :]):
        pytest.fail("명시 배제 세 집합이 서로 겹친다")
    derived = EXIT_UNIVERSE - HALT_EXIT_CHECKS - BETA_EXCLUDED - POST_LOOP_NO_RETRY
    if set(EXIT_RETRY_CHECK_IDS) != derived:
        pytest.fail(f"엔진 exit 승인 집합이 원장 도출값과 다르다: {sorted(derived)!r}")
    if set(gate.APPROVED_RETRY_CHECKS["exit"]) != derived:
        pytest.fail(f"관문 exit 승인 집합이 원장 도출값과 다르다: {sorted(derived)!r}")
    contract = load_stage_contract("read", None)
    contract_exit = set(_point(contract, "exit")["checks"])
    if contract_exit != derived:
        pytest.fail(f"계약 exit 승인 집합이 원장 도출값과 다르다: {sorted(derived)!r}")
    for check_id in POST_LOOP_NO_RETRY:
        row = _check_row(contract, check_id)
        if not (
            row.get("action") == "escalate"
            and not str(row.get("action", "")).startswith("retry(")
            and "then" not in row
            and "points" not in row
        ):
            pytest.fail(f"T22 루프 뒤 합류 행이 무재시도 escalate가 아니다: {row!r}")


def test_approved_failure_skeleton_matches_contract_exactly() -> None:
    contract = load_stage_contract("read", None)
    rows = contract["failure"]
    actual = tuple(gate._machine(row) for row in rows)
    if actual != gate.APPROVED_FAILURE_TABLE or len(rows) != 11:
        pytest.fail("계약 failure 기계 골격이 승인 11행과 순서까지 같지 않다")
    for row, approved in zip(rows, gate.APPROVED_FAILURE_TABLE):
        machine_keys = {key for key, value in approved.items() if value is not None}
        if set(row) != machine_keys | {"condition", "note"}:
            pytest.fail(f"failure 실제 키 열이 승인 기계 키+산문 둘과 다르다: {row!r}")
        if any(not isinstance(row.get(key), str) or not row[key] for key in ("condition", "note")):
            pytest.fail(f"failure 산문이 비공 str이 아니다: {row!r}")
    lane_rows = [_check_row(contract, check_id) for check_id in ("read.lane-log-shape", "read.lane-log-digest-value")]
    if lane_rows[0] is lane_rows[1] or any(len(row["checks"]) != 1 for row in lane_rows):
        pytest.fail("lane-log 두 검사가 서로 다른 singleton failure 행이 아니다")
    kinds = {row["kind"]: row["action"] for row in rows if "kind" in row}
    if kinds != {"retry-repeat": "escalate", "gate-escalation": "escalate", "upstream-defect": "reject-upstream"}:
        pytest.fail(f"kind 세 행 action이 틀렸다: {kinds!r}")
    judged = [index for index, row in enumerate(rows, 1) if row.get("judged_at") == "entry"]
    if judged != [3]:
        pytest.fail(f"judged_at: entry 기대 3행만, 실제 {judged!r}")
