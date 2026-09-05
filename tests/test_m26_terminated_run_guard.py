# -*- coding: utf-8 -*-
"""재정 T38 — 종결 런 재호출을 부작용 전에 막고 봉투 대기는 열어 둔다."""

from __future__ import annotations

import copy
import hashlib
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

from engine.lanes.contract import LanePending  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.stages import StageError, load_json  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402


def _prepared_run(tmp_path):
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": m2.payload_set(), "read-b": m2.payload_set()},
    )
    return root, lanes_root


def _complete_run(tmp_path):
    root, lanes_root = _prepared_run(tmp_path)
    outcome = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if outcome["status"] != "ok":
        pytest.fail(f"종결 대조군 status 기대 ok, 실제 {outcome['status']!r}")
    return root, lanes_root, RunPaths(root), m2.shadow_ledger_for(root)


def _bytes(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def _sha256(path: str) -> str:
    return hashlib.sha256(_bytes(path)).hexdigest()


def _read_ledger(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _read_tree_snapshot(root: str) -> dict[str, tuple[str, int]]:
    snapshot = {}
    for directory, _, filenames in os.walk(root):
        for filename in filenames:
            path = os.path.join(directory, filename)
            relative = os.path.relpath(path, root)
            snapshot[relative] = (_sha256(path), os.stat(path).st_mtime_ns)
    return snapshot


def _expect_terminated_error(root: str, lanes_root: str, evidence: str) -> str:
    with pytest.raises(StageError) as excinfo:
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    message = str(excinfo.value)
    missing = [token for token in (m2.RUN_ID, evidence, "종결한 런 재호출") if token not in message]
    if missing:
        pytest.fail(f"종결 재호출 StageError 문언 누락 {missing!r}: {message}")
    return message


def _expect_indeterminate_error(root: str, lanes_root: str, evidence: str) -> str:
    with pytest.raises(StageError) as excinfo:
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    message = str(excinfo.value)
    missing = [token for token in (m2.RUN_ID, evidence, "종결 판정 불가") if token not in message]
    if missing:
        pytest.fail(f"판정 불가 StageError 문언 누락 {missing!r}: {message}")
    return message


def test_terminated_rerun_is_rejected_before_every_side_effect(
    tmp_path, monkeypatch
) -> None:
    """ⓐ 포인터 종결 재호출은 원장·런 산출·호출 횟수를 하나도 바꾸지 않는다."""
    root, lanes_root, paths, ledger = _complete_run(tmp_path)
    read_root = os.path.join(root, "10-read")
    before_tree = _read_tree_snapshot(read_root)
    before_pointer = _bytes(paths.shadow_pointer)
    before_ledger = _bytes(ledger)
    calls = {"ensure_read_dirs": 0, "dispatch": 0, "append": 0, "write_json": 0}

    original_ensure = RunPaths.ensure_read_dirs
    original_dispatch = m2.ReplayLaneAdapter.dispatch
    original_append = read_stage.append_screening_ledger
    original_write_json = read_stage.write_json

    def counted_ensure(instance) -> None:
        calls["ensure_read_dirs"] += 1
        original_ensure(instance)

    def counted_dispatch(instance, requests):
        calls["dispatch"] += 1
        return original_dispatch(instance, requests)

    def counted_append(*args, **kwargs):
        calls["append"] += 1
        return original_append(*args, **kwargs)

    def counted_write_json(*args, **kwargs):
        calls["write_json"] += 1
        return original_write_json(*args, **kwargs)

    monkeypatch.setattr(RunPaths, "ensure_read_dirs", counted_ensure)
    monkeypatch.setattr(m2.ReplayLaneAdapter, "dispatch", counted_dispatch)
    monkeypatch.setattr(read_stage, "append_screening_ledger", counted_append)
    monkeypatch.setattr(read_stage, "write_json", counted_write_json)

    message = _expect_terminated_error(root, lanes_root, "shadow_pointer")
    if paths.shadow_pointer not in message:
        pytest.fail(f"종결 근거 파일 경로가 StageError에 없다: {message}")
    if calls != {"ensure_read_dirs": 0, "dispatch": 0, "append": 0, "write_json": 0}:
        pytest.fail(f"종결 가드 앞 부작용 호출 기대 전부 0, 실제 {calls!r}")
    if _read_tree_snapshot(read_root) != before_tree:
        pytest.fail("종결 재호출 전후 10-read 파일 집합·sha256·mtime가 달라졌다")
    if _bytes(paths.shadow_pointer) != before_pointer:
        pytest.fail("종결 재호출이 포인터 바이트를 바꿨다")
    if _bytes(ledger) != before_ledger:
        pytest.fail("종결 재호출이 격리 원장 바이트를 바꿨다")


def test_legacy_run_without_pointer_uses_full_convergence(tmp_path) -> None:
    """ⓑ 포인터 없는 구 런도 최종 판정서로 종결을 알아본다."""
    root, lanes_root, paths, _ = _complete_run(tmp_path)
    os.remove(paths.shadow_pointer)
    message = _expect_terminated_error(root, lanes_root, "convergence.json")
    if paths.convergence_json not in message:
        pytest.fail(f"최종 판정서 근거 경로가 StageError에 없다: {message}")


def test_run_with_only_ledger_row_is_rejected(tmp_path) -> None:
    """ⓒ append 뒤 포인터 실패를 원장 행만으로도 막는다."""
    root, lanes_root, paths, ledger = _complete_run(tmp_path)
    os.remove(paths.shadow_pointer)
    os.remove(paths.convergence_json)
    before = _bytes(ledger)
    message = _expect_terminated_error(root, lanes_root, "shadow_ledger")
    if ledger not in message:
        pytest.fail(f"섀도 원장 근거 경로가 StageError에 없다: {message}")
    if _bytes(ledger) != before:
        pytest.fail("원장 근거 재호출이 원장 바이트를 바꿨다")


def test_early_escalation_waits_without_ledger_then_finishes_once(tmp_path) -> None:
    """ⓓ 조기 상신은 비종결 포인터만 남기고 봉투 뒤 최종 종결에서 한 행을 쓴다."""
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    payloads = {
        "read-a": m2.payload_set(),
        "read-b": m2.payload_set(element_two=m2.E2_TEXT_VARIANT),
    }
    lanes_root = m2.write_lane_responses(root, payloads_by_run=payloads)
    first = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    paths = RunPaths(root)
    ledger = m2.shadow_ledger_for(root)
    if first["status"] != "escalate":
        pytest.fail(f"첫 조기 상신 status 기대 escalate, 실제 {first['status']!r}")
    if _read_ledger(ledger):
        pytest.fail(f"조기 상신 대기에 원장 행이 생겼다: {_read_ledger(ledger)!r}")
    pointer = load_json(paths.shadow_pointer)
    if pointer.get("terminated") is not False:
        pytest.fail(f"조기 상신 포인터 terminated 기대 false, 실제 {pointer!r}")
    if pointer.get("awaiting") != "convergence_continue":
        pytest.fail(f"조기 상신 포인터 awaiting 표지가 다르다: {pointer!r}")
    if os.path.exists(paths.convergence_json):
        pytest.fail("조기 상신 대기에 full convergence.json이 생겼다")

    m2._write_continue_envelope(root)
    second = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if second["status"] != "ok":
        pytest.fail(f"봉투 뒤 종결 status 기대 ok, 실제 {second['status']!r}")
    ours = [row for row in _read_ledger(ledger) if row.get("run_id") == m2.RUN_ID]
    if len(ours) != 1:
        pytest.fail(f"조기 상신→종결 원장 기대 최종 1행, 실제 {len(ours)}행: {ours!r}")
    pointer = load_json(paths.shadow_pointer)
    if pointer.get("terminated") is not True or "awaiting" in pointer:
        pytest.fail(f"최종 포인터 기대 terminated true + awaiting 부재, 실제 {pointer!r}")


def test_lane_pending_pointer_has_no_awaiting_marker(tmp_path) -> None:
    """ⓔ LanePending은 비종결이지만 T38의 봉투 대기 표지는 갖지 않는다."""
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": {"decompose": m2.payload_set()["decompose"]}},
    )
    with pytest.raises(LanePending):
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    pointer = load_json(RunPaths(root).shadow_pointer)
    if pointer.get("terminated") is not False or "awaiting" in pointer:
        pytest.fail(f"LanePending 포인터 기대 terminated false + awaiting 부재, 실제 {pointer!r}")


def test_new_run_with_no_termination_evidence_passes_guard(tmp_path) -> None:
    """ⓕ 세 근거가 전부 없는 새 런은 가드를 통과한다."""
    root, lanes_root = _prepared_run(tmp_path)
    paths = RunPaths(root)
    ledger = m2.shadow_ledger_for(root)
    present = [
        path
        for path in (paths.shadow_pointer, paths.convergence_json, ledger)
        if os.path.exists(path)
    ]
    if present:
        pytest.fail(f"새 런 양성 대조군에 종결 근거가 이미 있다: {present!r}")
    outcome = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if outcome["status"] != "ok":
        pytest.fail(f"세 근거 부재 새 런이 가드에 막혔다: {outcome['status']!r}")


def test_true_pointer_alone_rejects_rerun(tmp_path) -> None:
    """ⓖ 다른 두 근거가 없어도 참 포인터 단독이면 종결이다."""
    root, lanes_root, paths, ledger = _complete_run(tmp_path)
    os.remove(paths.convergence_json)
    os.remove(ledger)
    _expect_terminated_error(root, lanes_root, "shadow_pointer")


def test_false_pointer_still_falls_through_to_matching_ledger_row(tmp_path) -> None:
    """ⓗ 거짓 포인터는 뒤의 동일 ID 원장 행을 가리지 않는다."""
    root, lanes_root, paths, _ = _complete_run(tmp_path)
    os.remove(paths.convergence_json)
    pointer = load_json(paths.shadow_pointer)
    pointer["terminated"] = False
    pointer["appended"] = False
    read_stage.write_json(paths.shadow_pointer, pointer)
    _expect_terminated_error(root, lanes_root, "shadow_ledger")


@pytest.mark.parametrize("damage", ["null", "broken-json", "non-bool"])
def test_indeterminate_pointer_is_fail_closed(tmp_path, damage) -> None:
    """ⓘ1 포인터 파싱·최상위·terminated 형태 위반은 부재로 접지 않는다."""
    root, lanes_root, paths, _ = _complete_run(tmp_path)
    if damage == "null":
        damaged = "null\n"
    elif damage == "broken-json":
        damaged = "{broken-json\n"
    else:
        damaged = json.dumps({"terminated": "yes"}) + "\n"
    with open(paths.shadow_pointer, "w", encoding="utf-8") as handle:
        handle.write(damaged)
    before = _bytes(paths.shadow_pointer)
    message = _expect_indeterminate_error(root, lanes_root, "shadow_pointer")
    if paths.shadow_pointer not in message:
        pytest.fail(f"손상 포인터 경로가 StageError에 없다: {message}")
    if _bytes(paths.shadow_pointer) != before:
        pytest.fail("판정 불가 재호출이 손상 포인터 바이트를 바꿨다")


@pytest.mark.parametrize("position", ["before", "after"])
def test_indeterminate_ledger_jsonl_is_fail_closed(tmp_path, position) -> None:
    """ⓘ2 정상 행 앞·뒤의 손상행 모두 원장 전체 판정을 불가능하게 한다."""
    root, lanes_root, paths, ledger = _complete_run(tmp_path)
    os.remove(paths.shadow_pointer)
    os.remove(paths.convergence_json)
    normal = _bytes(ledger)
    broken = b"{broken-json\n"
    damaged = broken + normal if position == "before" else normal + broken
    with open(ledger, "wb") as handle:
        handle.write(damaged)
    before_sha = _sha256(ledger)
    message = _expect_indeterminate_error(root, lanes_root, "shadow_ledger")
    if ledger not in message:
        pytest.fail(f"손상 원장 경로가 StageError에 없다: {message}")
    if _sha256(ledger) != before_sha:
        pytest.fail("판정 불가 재호출이 손상행 포함 원장 바이트를 바꿨다")


@pytest.mark.parametrize("malformed", [None, {"owner_decision": None}])
def test_indeterminate_ledger_row_shape_is_fail_closed(tmp_path, malformed) -> None:
    """ⓘ3 객체 아닌 행과 문자열 run_id 없는 객체 행을 즉시 거부한다."""
    root, lanes_root, paths, ledger = _complete_run(tmp_path)
    os.remove(paths.shadow_pointer)
    os.remove(paths.convergence_json)
    with open(ledger, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(malformed, sort_keys=True) + "\n")
    before_sha = _sha256(ledger)
    _expect_indeterminate_error(root, lanes_root, "shadow_ledger")
    if _sha256(ledger) != before_sha:
        pytest.fail("행 형태 판정 불가 재호출이 원장 바이트를 바꿨다")
