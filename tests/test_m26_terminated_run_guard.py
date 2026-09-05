# -*- coding: utf-8 -*-
"""재정 T38 — 종결 런 재호출을 부작용 전에 막고 봉투 대기는 열어 둔다."""

from __future__ import annotations

__doc__ += """

ⓦ fail-closed 의존표 — Owner가 「판정 불가 = 그 근거 거짓 → 다음 근거」로 뒤집으면:

| 시험 | 현재 핀 | ⓦ 반전 때 바뀌는 기대 |
|---|---|---|
| ⓜ1×3 | 판정서 손상·형태를 즉시 판정 불가로 닫음 | 가드 통과 뒤 `phase: full`로 덮어씀 |
| ⓜ2 | 포인터 읽기 오류를 즉시 판정 불가로 닫음 | 최종 포인터 쓰기에서 `IsADirectoryError` 누출 |
| ⓜ3 | 원장 루트 거부를 dispatch 전에 닫고 포인터를 남기지 않음 | dispatch 뒤 append에서 `ShadowLedgerRootError` |
| ⓘ1×3 | 포인터 손상·형태를 즉시 판정 불가로 닫음 | 판정서가 남아 `convergence.json` 근거 종결 재호출 |
| ⓘ2×2 | 정상 행 앞·뒤 손상행을 즉시 판정 불가로 닫음 | 같은 ID 정상 행이 남아 `shadow_ledger` 근거 종결 재호출 |
| ⓘ3×2 | 비객체·run_id 형태 위반 행을 즉시 판정 불가로 닫음 | 같은 ID 정상 행이 남아 `shadow_ledger` 근거 종결 재호출 |
"""

import builtins
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402
import test_m16_lane_binding as m16  # noqa: E402

from engine import paths as engine_paths  # noqa: E402
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


def _supplement_reader_and_commit(repo: str) -> None:
    """소형 법 리포에 실제 READ 절차 트리를 보충하고 그 행위시법을 커밋한다."""
    shutil.copytree(
        os.path.join(REPO, "reader"),
        os.path.join(repo, "reader"),
        ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", ".pytest_cache"),
        dirs_exist_ok=True,
    )
    for args in (("add", "reader"), ("commit", "-q", "-m", "supplement reader")):
        proc = subprocess.run(
            ["git", "-C", repo, *args], capture_output=True, text=True, check=False
        )
        if proc.returncode != 0:
            pytest.fail(f"임시 법 리포 git {' '.join(args)} 실패: {proc.stderr}")
    status = subprocess.run(
        ["git", "-C", repo, "status", "--short"],
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode != 0 or status.stdout:
        pytest.fail(
            f"reader 보충 커밋 뒤 계약 트리가 깨끗하지 않다: "
            f"exit={status.returncode}, status={status.stdout!r}, stderr={status.stderr!r}"
        )


def _fresh_run_with_responses(tmp_path, *, repo=None):
    """SOURCE 직후 `10-read/` 부재를 확인한 다음에만 응답 트리를 만든다."""
    root, source_outcome = m2.run_source(tmp_path, repo=repo)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    read_root = os.path.join(root, "10-read")
    if os.path.exists(read_root):
        pytest.fail(f"write_lane_responses 전인데 10-read가 이미 있다: {read_root}")
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": m2.payload_set(), "read-b": m2.payload_set()},
    )
    return root, lanes_root


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


def test_linked_worktree_rerun_uses_main_ledger_with_implicit_root(
    tmp_path, monkeypatch
) -> None:
    """ⓙ 실제 `shadow_root=None` 경로도 주 원장 행만으로 종결 재호출을 막는다."""
    main, worktree = m16.make_main_and_worktree(tmp_path)
    _supplement_reader_and_commit(worktree)
    tmp_real = os.path.realpath(str(tmp_path))
    for label, path in (("main", main), ("worktree", worktree)):
        if os.path.commonpath((tmp_real, os.path.realpath(path))) != tmp_real:
            pytest.fail(f"{label} 임시 트리가 tmp_path 밖에 있다: {path}")
    if m2._main_worktree_by_git(worktree) != main:
        pytest.fail(
            f"git 실측 주 트리 기대 {main}, 실제 {m2._main_worktree_by_git(worktree)}"
        )

    production = engine_paths.shadow_screening_ledger()
    expected_ledger = os.path.join(main, "ledgers", "shadow", "screening.jsonl")
    if expected_ledger == production:
        pytest.fail(f"임시 원장과 생산 원장이 같은 경로다: {production}")
    before_production = m2._ledger_fingerprint(production)
    try:
        root, lanes_root = _fresh_run_with_responses(tmp_path, repo=worktree)
        adapter = m2.ReplayLaneAdapter(lanes_root)
        opened_reader = set()
        original_open = builtins.open

        def tracked_open(file, *args, **kwargs):
            path = os.path.realpath(os.fspath(file))
            reader_root = os.path.join(worktree, "reader") + os.sep
            if path.startswith(reader_root):
                opened_reader.add(os.path.relpath(path, worktree))
            return original_open(file, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", tracked_open)
        first = read_stage.run(
            run_root=root,
            adapter=adapter,
            rules=m2.RULES,
            repo=worktree,
            shadow_root=None,
        )
        if first["status"] != "ok":
            pytest.fail(f"worktree 생산 경로 첫 통주가 종결하지 않았다: {first!r}")
        expected_opened = {
            "reader/READER-VERSION",
            "reader/procedure/10-decompose.md",
            "reader/procedure/20-grounding.md",
            "reader/procedure/30-synthesis.md",
        }
        if opened_reader != expected_opened:
            pytest.fail(
                f"worktree 통주가 연 reader 파일 기대 {sorted(expected_opened)!r}, "
                f"실제 {sorted(opened_reader)!r}"
            )

        paths = RunPaths(root, worktree)
        pointer = load_json(paths.shadow_pointer)
        if pointer.get("root_source") != "main-worktree-resolved":
            pytest.fail(f"포인터의 주 트리 해석 사유가 다르다: {pointer!r}")
        if pointer.get("ledger") != expected_ledger:
            pytest.fail(f"포인터 원장 기대 {expected_ledger}, 실제 {pointer!r}")
        rows = _read_ledger(expected_ledger)
        if len(rows) != 1 or rows[0].get("run_id") != m2.RUN_ID:
            pytest.fail(f"첫 통주 뒤 주 원장에 이 런 1행이 없다: {rows!r}")
        orphan = os.path.join(worktree, "ledgers", "shadow", "screening.jsonl")
        if os.path.exists(orphan):
            pytest.fail(f"worktree에 고아 원장이 생겼다: {orphan}")

        os.remove(paths.shadow_pointer)
        os.remove(paths.convergence_json)
        before_ledger = _bytes(expected_ledger)
        try:
            with pytest.raises(StageError) as excinfo:
                read_stage.run(
                    run_root=root,
                    adapter=adapter,
                    rules=m2.RULES,
                    repo=worktree,
                    shadow_root=None,
                )
        except pytest.fail.Exception as exc:
            changed_rows = _read_ledger(expected_ledger)
            pytest.fail(
                f"{exc}; 재호출 뒤 주 원장 실제 {len(changed_rows)}행: {changed_rows!r}"
            )
        message = str(excinfo.value)
        missing = [
            token
            for token in (m2.RUN_ID, "shadow_ledger", "종결한 런 재호출")
            if token not in message
        ]
        if missing:
            pytest.fail(f"생산 경로 종결 재호출 문언 누락 {missing!r}: {message}")
        if _bytes(expected_ledger) != before_ledger or len(_read_ledger(expected_ledger)) != 1:
            pytest.fail(f"재호출이 주 원장을 바꿨다: {_read_ledger(expected_ledger)!r}")
    finally:
        after_production = m2._ledger_fingerprint(production)
        if after_production != before_production:
            pytest.fail(
                f"생산 섀도 원장이 변했다: {before_production} → "
                f"{after_production} ({production})"
            )


def test_other_run_ids_in_ledger_do_not_terminate_new_run(tmp_path) -> None:
    """ⓚ 접두가 같은 ID와 무관한 ID 행은 현재 런의 종결 근거가 아니다."""
    root, lanes_root = _fresh_run_with_responses(tmp_path)
    ledger = m2.shadow_ledger_for(root)
    os.makedirs(os.path.dirname(ledger), exist_ok=True)
    seeded_ids = (f"{m2.RUN_ID}-x", "example-zz9999999z9-unrelated")
    with open(ledger, "w", encoding="utf-8") as handle:
        for run_id in seeded_ids:
            row = {
                "run_id": run_id,
                "recorded_at": "2026-09-05T00:00:00Z",
                "memos": [],
                "final_verdict": "go",
                "final_reason": "음성 대조",
                "owner_decision": None,
            }
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    outcome = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if outcome["status"] != "ok":
        pytest.fail(f"다른 run_id 행이 새 런을 막았다: {outcome!r}")
    rows = _read_ledger(ledger)
    if len(rows) != 3:
        pytest.fail(f"심은 2행 + 새 1행 기대, 실제 {len(rows)}행: {rows!r}")
    if [row.get("run_id") for row in rows[:2]] != list(seeded_ids):
        pytest.fail(f"미리 심은 다른 run_id 두 행이 바뀌었다: {rows!r}")
    if rows[2].get("run_id") != m2.RUN_ID:
        pytest.fail(f"새 행의 run_id가 정확 일치하지 않는다: {rows[2]!r}")


def test_nonfull_convergence_is_not_termination_evidence(tmp_path) -> None:
    """ⓛ `phase: early` 판정서는 비참이므로 다음 근거로 넘어가 새 런을 연다."""
    root, lanes_root = _fresh_run_with_responses(tmp_path)
    paths = RunPaths(root)
    with open(paths.convergence_json, "w", encoding="utf-8") as handle:
        json.dump({"phase": "early"}, handle)
    outcome = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if outcome["status"] != "ok":
        pytest.fail(f"비참 판정서가 정상 새 런을 막았다: {outcome!r}")
    convergence = load_json(paths.convergence_json)
    if convergence.get("phase") != "full":
        pytest.fail(f"정상 종결이 판정서를 phase full로 덮지 않았다: {convergence!r}")


@pytest.mark.parametrize(
    ("damaged", "reason"),
    [
        ("{broken", "JSON 파싱 오류"),
        ("null", "최상위가 객체가 아님"),
        ('{"phase": 0}', "phase가 문자열이 아님"),
    ],
)
def test_indeterminate_convergence_is_fail_closed(tmp_path, damaged, reason) -> None:
    """ⓜ1 판정서 파싱·최상위·phase 형태 위반은 부재로 접지 않는다."""
    root, lanes_root = _fresh_run_with_responses(tmp_path)
    paths = RunPaths(root)
    with open(paths.convergence_json, "w", encoding="utf-8") as handle:
        handle.write(damaged)
    before = _bytes(paths.convergence_json)
    message = _expect_indeterminate_error(root, lanes_root, "convergence.json")
    for token in (reason, paths.convergence_json):
        if token not in message:
            pytest.fail(f"판정서 판정 불가 문언에 {token!r} 누락: {message}")
    if _bytes(paths.convergence_json) != before:
        pytest.fail("판정 불가 가드가 손상 판정서를 덮어썼다")


def test_shadow_pointer_read_error_is_fail_closed(tmp_path) -> None:
    """ⓜ2 포인터 자리가 디렉터리인 읽기 오류는 `IsADirectoryError`로 누출되지 않는다."""
    root, lanes_root = _fresh_run_with_responses(tmp_path)
    paths = RunPaths(root)
    os.mkdir(paths.shadow_pointer)
    message = _expect_indeterminate_error(root, lanes_root, "shadow_pointer")
    for token in ("읽기 오류", paths.shadow_pointer):
        if token not in message:
            pytest.fail(f"포인터 읽기 오류 문언에 {token!r} 누락: {message}")
    if not os.path.isdir(paths.shadow_pointer):
        pytest.fail("판정 불가 가드가 포인터 자리 디렉터리를 바꿨다")


def test_unlocatable_ledger_root_is_rejected_before_dispatch(tmp_path, monkeypatch) -> None:
    """ⓜ3 원장 루트를 못 찾으면 dispatch 전에 닫고 거부 포인터도 쓰지 않는다."""
    main = os.path.join(str(tmp_path), "src")
    m2.make_law_repo(main)
    _supplement_reader_and_commit(main)
    bare = os.path.join(str(tmp_path), "bare.git")
    detached = os.path.join(str(tmp_path), "detached")
    for args in (
        ("git", "clone", "-q", "--bare", main, bare),
        ("git", "-C", bare, "worktree", "add", "-q", detached, "HEAD"),
    ):
        proc = subprocess.run(args, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            pytest.fail(f"{' '.join(args)} 실패(exit {proc.returncode}): {proc.stderr}")

    root, source_outcome = m2.run_source(tmp_path, repo=detached)
    if source_outcome["status"] != "ok":
        pytest.fail(f"detached source 대조군 실패: {source_outcome!r}")
    read_root = os.path.join(root, "10-read")
    if os.path.exists(read_root):
        pytest.fail(f"write_lane_responses 전인데 10-read가 이미 있다: {read_root}")
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": m2.payload_set(), "read-b": m2.payload_set()},
    )
    adapter = m2.ReplayLaneAdapter(lanes_root)
    dispatches = {"count": 0}
    original_dispatch = m2.ReplayLaneAdapter.dispatch

    def counted_dispatch(instance, requests):
        dispatches["count"] += 1
        return original_dispatch(instance, requests)

    monkeypatch.setattr(m2.ReplayLaneAdapter, "dispatch", counted_dispatch)
    try:
        with pytest.raises(StageError) as excinfo:
            read_stage.run(
                run_root=root,
                adapter=adapter,
                rules=m2.RULES,
                repo=detached,
                shadow_root=None,
            )
    except engine_paths.ShadowLedgerRootError as exc:
        pytest.fail(
            f"원장 루트 거부가 가드에서 닫히지 않고 dispatch "
            f"{dispatches['count']}회 뒤 append에서 누출됐다: {exc}"
        )
    message = str(excinfo.value)
    for token in ("종결 판정 불가", "shadow_ledger", "원장 루트 판정 거부"):
        if token not in message:
            pytest.fail(f"원장 루트 거부 문언에 {token!r} 누락: {message}")
    if dispatches["count"] != 0:
        pytest.fail(f"원장 루트 거부 뒤 dispatch가 실행됐다: {dispatches!r}")
    pointer = RunPaths(root, detached).shadow_pointer
    if os.path.exists(pointer):
        pytest.fail(f"가드가 거부 포인터를 남겼다: {pointer}")
