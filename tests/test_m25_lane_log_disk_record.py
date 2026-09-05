# -*- coding: utf-8 -*-
"""재정 2026-08-31 T3 — 레인 로그 검사가 디스크 기록본을 소비하는지 반증한다.

READ 통주는 `test_m2_read`의 섀도 원장 격리 하네스를 재사용한다. `assert` 대신
`pytest.fail()`을 써 최적화 모드에서도 단언이 사라지지 않게 한다.
"""

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

from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.stages import StageError, load_json  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402


class RequestWritingReplayAdapter(m2.ReplayLaneAdapter):
    """합성 응답을 재생하되 실 운용 어댑터와 같은 `request.md`를 남긴다."""

    def __init__(self, root: str) -> None:
        super().__init__(root)
        self._writer = FileLaneAdapter(root, REPO)

    def dispatch(self, requests):
        for request in requests:
            self._writer.write_request(request)
        return super().dispatch(requests)

    def request_md_digest(self, request):
        return self._writer.request_md_digest(request)


def _prepared_run(tmp_path):
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source 대조군 실패: {source_outcome!r}")
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": m2.payload_set(), "read-b": m2.payload_set()},
    )
    return root, RequestWritingReplayAdapter(lanes_root)


def _check_row(outcome: dict, check_id: str):
    matches = [row for row in outcome["rows"] if row.check_id == check_id]
    if len(matches) != 1:
        pytest.fail(f"{check_id} 행 기대 1, 실제 {len(matches)}")
    return matches[0]


def _install_lane_log_mutation(monkeypatch, mutate):
    """최초 게시를 마친 뒤 디스크 사본만 바꾸고 메모리 rows 참조를 보존한다."""
    original_write_json = read_stage.write_json
    observed = {"writes": 0, "memory_rows": None, "original_rows": None}

    def write_json_then_mutate(path, payload) -> None:
        original_write_json(path, payload)
        if os.path.basename(path) != "lane-log.json":
            return
        observed["writes"] += 1
        if observed["writes"] != 1:
            return
        observed["memory_rows"] = payload
        observed["original_rows"] = copy.deepcopy(payload)
        mutate(path, original_write_json)

    monkeypatch.setattr(read_stage, "write_json", write_json_then_mutate)
    return observed


def test_disk_digest_mutation_drives_value_check_and_is_preserved(
    tmp_path, monkeypatch
) -> None:
    """파일만 바꾼 요청 지문을 값 검사가 잡고, 검사한 B가 최종 로그로 남아야 한다."""
    root, adapter = _prepared_run(tmp_path)
    forged = "f" * 64
    changed = {}

    def mutate(path, original_write_json) -> None:
        disk_rows = load_json(path)
        target = next(
            (
                row
                for row in disk_rows
                if row.get("request_digest") and row.get("task") == "ground-independent"
            ),
            None,
        )
        if target is None:
            pytest.fail("실재 request.md 지문을 가진 접지 행이 없다")
        changed["lane_id"] = target["lane_id"]
        changed["original_digest"] = target["request_digest"]
        target["request_digest"] = forged
        changed["rows"] = copy.deepcopy(disk_rows)
        original_write_json(path, disk_rows)

    observed = _install_lane_log_mutation(monkeypatch, mutate)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)

    value = _check_row(outcome, "read.lane-log-digest-value")
    rules = {finding.rule for finding in value.findings}
    if value.status != "fail" or "lane-log.digest-value-mismatch" not in rules:
        pytest.fail(f"디스크 지문 위조를 값 검사가 잡지 못했다: {value.status}, {sorted(rules)}")
    if outcome["status"] != "escalate" or outcome["reason_label"] is not None:
        pytest.fail(f"T22 실패표 처분 기대 escalate/None, 실제 {outcome!r}")
    if any("/retry-" in request.lane_id for request in adapter.dispatched):
        pytest.fail("레인 로그 검사 실패 뒤 재시도가 발송됐다")

    memory_rows = observed["memory_rows"]
    original_rows = observed["original_rows"]
    memory_target = next(row for row in memory_rows if row["lane_id"] == changed["lane_id"])
    if memory_target["request_digest"] != changed["original_digest"]:
        pytest.fail("파일 변조가 메모리 journal.rows까지 오염시켰다")
    if memory_rows != original_rows:
        pytest.fail("검사 과정이 메모리 journal.rows를 바꿨다")
    final_rows = load_json(RunPaths(root).lane_log)
    if final_rows != changed["rows"] or observed["writes"] != 1:
        pytest.fail("검사가 소비한 변조본 B가 finally에서 덮였거나 로그가 두 번 게시됐다")


def test_disk_read_run_mutation_drives_only_shape_check(tmp_path, monkeypatch) -> None:
    """접지 행의 실행명만 바꾸면 형태만 실패하고 값 검사는 통과해야 한다."""
    root, adapter = _prepared_run(tmp_path)
    changed = {}

    def mutate(path, original_write_json) -> None:
        disk_rows = load_json(path)
        target = next(
            (
                row
                for row in disk_rows
                if row.get("read_run") == "read-a"
                and row.get("task") == "ground-independent"
                and row.get("request_digest")
            ),
            None,
        )
        if target is None:
            pytest.fail("형태 전용 변조에 쓸 정본 접지 행이 없다")
        changed["lane_id"] = target["lane_id"]
        target["read_run"] = "read-b"
        changed["rows"] = copy.deepcopy(disk_rows)
        original_write_json(path, disk_rows)

    observed = _install_lane_log_mutation(monkeypatch, mutate)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)

    shape = _check_row(outcome, "read.lane-log-shape")
    value = _check_row(outcome, "read.lane-log-digest-value")
    shape_rules = {finding.rule for finding in shape.findings}
    if shape.status != "fail" or "lane-log.non-canonical-tail" not in shape_rules:
        pytest.fail(f"디스크 read_run 변조를 형태 검사가 잡지 못했다: {shape.status}, {shape_rules}")
    if value.status != "pass":
        pytest.fail(f"형태 전용 변조가 값 검사까지 붉혔다: {[f.rule for f in value.findings]}")
    memory_target = next(
        row for row in observed["memory_rows"] if row["lane_id"] == changed["lane_id"]
    )
    if memory_target["read_run"] != "read-a":
        pytest.fail("파일의 read_run 변조가 메모리 journal.rows까지 오염시켰다")
    if load_json(RunPaths(root).lane_log) != changed["rows"] or observed["writes"] != 1:
        pytest.fail("형태 검사가 소비한 변조본이 최종 로그로 보존되지 않았다")


def test_exception_before_exit_check_still_records_the_journal(tmp_path, monkeypatch) -> None:
    """⑨ 전 예외에서도 기존 finally가 그 시점의 저널을 한 번 기록해야 한다."""
    root, adapter = _prepared_run(tmp_path)
    paths = RunPaths(root)
    original_write_json = read_stage.write_json
    observed = {"memory_rows": None, "writes": 0}

    class BeforeExitError(RuntimeError):
        pass

    def fail_before_exit(path, payload) -> None:
        if path == os.path.join(paths.lanes_dir, read_stage.ID_MAP_BASENAME):
            raise BeforeExitError("⑨ 전 주입 예외")
        original_write_json(path, payload)
        if path == paths.lane_log:
            observed["writes"] += 1
            observed["memory_rows"] = copy.deepcopy(payload)

    monkeypatch.setattr(read_stage, "write_json", fail_before_exit)
    with pytest.raises(BeforeExitError, match="⑨ 전 주입 예외"):
        m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)

    if not os.path.isfile(paths.lane_log):
        pytest.fail("⑨ 전 예외 뒤 lane-log.json이 남지 않았다")
    if load_json(paths.lane_log) != observed["memory_rows"] or observed["writes"] != 1:
        pytest.fail("⑨ 전 예외 로그가 그 시점의 저널과 다르거나 한 번 넘게 쓰였다")


@pytest.mark.parametrize("damage", ["null", "non-dict-row", "broken-json", "deleted"])
def test_reread_defects_are_stage_errors_and_are_not_repaired(
    tmp_path, monkeypatch, damage
) -> None:
    """게시 뒤 재독 불능·형태 위반은 런 결함이며 손상본을 메모리 A로 복원하지 않는다."""
    root, adapter = _prepared_run(tmp_path)
    damaged = {}

    def mutate(path, original_write_json) -> None:
        if damage == "null":
            original_write_json(path, None)
        elif damage == "non-dict-row":
            original_write_json(path, [0])
        elif damage == "broken-json":
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("{broken-json\n")
            damaged["text"] = "{broken-json\n"
        elif damage == "deleted":
            os.remove(path)

    observed = _install_lane_log_mutation(monkeypatch, mutate)
    with pytest.raises(StageError) as excinfo:
        m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)

    message = str(excinfo.value)
    path = RunPaths(root).lane_log
    if path not in message or "검사 실패가 아니라 런 결함" not in message:
        pytest.fail(f"StageError가 경로·런 결함 사유를 모두 싣지 않았다: {message}")
    if observed["writes"] != 1:
        pytest.fail(f"재독 실패 뒤 로그를 다시 썼다: 게시 횟수 {observed['writes']}")
    if damage == "deleted":
        if os.path.exists(path):
            pytest.fail("외부 삭제된 로그를 메모리 저널로 자동 복원했다")
    elif damage == "broken-json":
        with open(path, encoding="utf-8") as handle:
            if handle.read() != damaged["text"]:
                pytest.fail("파싱 불가 손상 바이트가 finally에서 바뀌었다")
    elif damage == "null":
        if load_json(path) is not None:
            pytest.fail("null 손상본이 그대로 보존되지 않았다")
    elif load_json(path) != [0]:
        pytest.fail("list[dict] 형태 위반 손상본이 그대로 보존되지 않았다")


def test_normal_completion_publishes_once_and_matches_memory_rows(
    tmp_path, monkeypatch
) -> None:
    """정상 런의 최종 로그는 저널 rows와 같고 게시 쓰기는 한 번이어야 한다."""
    root, adapter = _prepared_run(tmp_path)

    def no_mutation(path, original_write_json) -> None:
        _ = path, original_write_json

    observed = _install_lane_log_mutation(monkeypatch, no_mutation)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"정상 통주가 실패했다: {outcome['status']}")
    if observed["writes"] != 1:
        pytest.fail(f"정상 로그 게시 기대 1회, 실제 {observed['writes']}회")
    if load_json(RunPaths(root).lane_log) != observed["memory_rows"]:
        pytest.fail("정상 완료 로그가 메모리 journal.rows와 다르다")


def test_first_lane_log_publish_oserror_falls_back_to_memory_journal(
    tmp_path, monkeypatch
) -> None:
    """첫 게시가 실패하면 원 예외를 보존하면서 finally가 메모리 저널을 기록해야 한다."""
    root, adapter = _prepared_run(tmp_path)
    paths = RunPaths(root)
    original_write_json = read_stage.write_json
    observed = {"lane_log_calls": 0, "fallback_rows": None}

    def fail_first_lane_log_publish(path, payload) -> None:
        if path == paths.lane_log:
            observed["lane_log_calls"] += 1
            if observed["lane_log_calls"] == 1:
                raise OSError("첫 lane-log 게시 실패")
            observed["fallback_rows"] = copy.deepcopy(payload)
        original_write_json(path, payload)

    monkeypatch.setattr(read_stage, "write_json", fail_first_lane_log_publish)
    with pytest.raises(OSError, match="첫 lane-log 게시 실패"):
        m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)

    if observed["lane_log_calls"] != 2:
        pytest.fail(
            "첫 게시 실패 뒤 finally 폴백 기대 총 2회 호출, 실제 "
            f"{observed['lane_log_calls']}회"
        )
    if not os.path.isfile(paths.lane_log):
        pytest.fail("첫 게시 OSError 뒤 finally 폴백 lane-log.json이 없다")
    if load_json(paths.lane_log) != observed["fallback_rows"]:
        pytest.fail("finally 폴백 기록이 예외 시점의 메모리 journal.rows와 다르다")
    if not os.path.isfile(paths.shadow_pointer):
        pytest.fail("첫 게시 OSError 뒤 종전 finally 포인터 기록이 사라졌다")
    if not os.path.isfile(m2.shadow_ledger_for(root)):
        pytest.fail("첫 게시 OSError 뒤 종전 finally 원장 기록이 사라졌다")
