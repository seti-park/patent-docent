# -*- coding: utf-8 -*-
"""`lane_id` 형태·소속·루트 포함(디렉터리·말단)의 회귀 시험."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import shutil
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.lanes import contract as lane_contract  # noqa: E402
from engine.lanes import plan  # noqa: E402
from engine.lanes.contract import LaneContractError, LaneRequest  # noqa: E402
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402

RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {"items": {"type": "array"}},
}


def _request(lane_id: str, *, read_run: str = "read-a", task: str = "decompose", batch: int = 0):
    return LaneRequest(
        lane_id=lane_id,
        read_run=read_run,
        task=task,
        model="opus-5",
        effort="high",
        prompt_path="reader/procedure/10-decompose.md",
        instructions="ground every assertion",
        repo_root=REPO,
        slices={"claims": "1. An apparatus."},
        response_schema=RESPONSE_SCHEMA,
        batch=batch,
    )


@pytest.mark.parametrize(
    "lane_id",
    ["read-a/decompose/batch-0", "read-b/synthesize/retry-3/batch-12"],
)
def test_positive_lane_ids_are_accepted(lane_id) -> None:
    """정본 형태와 소속을 함께 만족하는 두 대표 좌표는 허용한다."""
    read_run, task = lane_id.split("/", 2)[:2]
    _request(lane_id, read_run=read_run, task=task)


def test_every_lane_id_for_output_is_accepted() -> None:
    """유일 조립 자리의 4×2×2×2 산출 전건이 요청 계약을 통과한다."""
    for task in ("decompose", "ground-independent", "ground-dependent", "synthesize"):
        for read_run in ("read-a", "read-b"):
            for retry in (0, 1):
                for batch in (0, 1):
                    _request(
                        plan.lane_id_for(read_run, task, batch, retry),
                        read_run=read_run,
                        task=task,
                        batch=batch,
                    )


@pytest.mark.parametrize(
    "lane_id",
    [
        "../x/batch-0",
        "/read-a/decompose/batch-0",
        "read-a/decompose/batch-0/..",
        "read-a/decompose/batch-0/",
        "read-a//batch-0",
        "Read-A/decompose/batch-0",
        "read-a/decompose/retry-0/batch-0",
        "read-a/decompose/batch--1",
        "read-a/decompose/batch-01",
        "read-a/decompose/batch-0\n",
        "read-a/decompose/batch-0\t",
        "read-a/decompose/batch-0 ",
        " read-a/decompose/batch-0",
    ],
)
def test_lane_id_shape_rejects_non_contract_forms(lane_id) -> None:
    """형태 음성 13종은 모두 `fullmatch` 경계에서 구별해 거부한다."""
    with pytest.raises(LaneContractError, match=r"어휘 위반\(형태\)"):
        _request(lane_id)


@pytest.mark.parametrize(
    "lane_id",
    [
        "read-c/decompose/batch-0",
        "read-a/other/batch-0",
        "other/unknown/batch-0",
    ],
)
def test_lane_id_membership_rejects_unknown_contract_terms(lane_id) -> None:
    """형태만 맞는 미등록 read_run·task는 소속 위반으로 거부한다(B-01)."""
    with pytest.raises(LaneContractError, match=r"어휘 위반\(소속\)"):
        _request(lane_id)


def test_lane_request_deliberately_does_not_check_field_alignment() -> None:
    """필드 정합은 조립 자리가 보장하며 LaneRequest는 형태·소속만 본다(MR-1)."""
    _request(
        "read-b/decompose/batch-0",
        read_run="read-b",
        task="synthesize",
    )


def test_lane_dir_revalidates_vocabulary(tmp_path) -> None:
    """LaneRequest를 거치지 않은 경로 조립도 같은 형태 어휘를 적용한다."""
    with pytest.raises(LaneContractError, match=r"어휘 위반\(형태\)"):
        lane_contract.lane_dir(str(tmp_path), "../x")


def test_lane_dir_rejects_intermediate_symlink_escape(tmp_path) -> None:
    """중간 디렉터리 링크가 루트 밖을 가리키면 디렉터리 포함 검사로 거부한다."""
    root = os.path.join(str(tmp_path), "lanes")
    outside = os.path.join(str(tmp_path), "outside")
    os.makedirs(os.path.join(root, "read-a"), exist_ok=True)
    os.makedirs(outside)
    os.symlink(outside, os.path.join(root, "read-a", "decompose"))
    with pytest.raises(LaneContractError, match=r"루트 밖\(디렉터리\)"):
        lane_contract.lane_dir(root, "read-a/decompose/batch-0")


def test_lane_dir_accepts_a_symlink_root(tmp_path) -> None:
    """루트 자체의 링크는 그 루트의 realpath를 경계로 삼으므로 정상이다."""
    real = os.path.join(str(tmp_path), "real")
    link = os.path.join(str(tmp_path), "link")
    os.makedirs(real)
    os.symlink(real, link)
    path = lane_contract.lane_dir(link, "read-a/decompose/batch-0")
    if not os.path.realpath(path).startswith(os.path.realpath(real) + os.sep):
        pytest.fail(f"링크 루트 아래 경로가 아니다: {path!r}")


def test_lane_file_rejects_terminal_symlink_escape(tmp_path) -> None:
    """lane_dir가 통과해도 말단 request.md 링크는 별도로 거부한다(B-02)."""
    root = os.path.join(str(tmp_path), "lanes")
    lane_id = "read-a/decompose/batch-0"
    directory = os.path.join(root, *lane_id.split("/"))
    outside = os.path.join(str(tmp_path), "outside")
    os.makedirs(directory, exist_ok=True)
    os.makedirs(outside)
    target = os.path.join(outside, "request.md")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write("outside\n")
    os.symlink(target, os.path.join(directory, "request.md"))
    lane_contract.lane_dir(root, lane_id)
    with pytest.raises(LaneContractError, match=r"루트 밖\(말단\)"):
        lane_contract.lane_file(root, lane_id, "request.md")


@pytest.mark.parametrize("name", ["../request.md", "nested/request.md", ".."])
def test_lane_file_rejects_non_basename_names(tmp_path, name) -> None:
    """말단 이름에는 경로 구분자와 `..`를 허용하지 않는다."""
    with pytest.raises(LaneContractError, match="어휘 위반"):
        lane_contract.lane_file(
            str(tmp_path), "read-a/decompose/batch-0", name
        )


def _recorded_round_trip(base: str):
    """FileLaneAdapter가 request.md를 실제로 쓴 비null 지문 로그 한 행."""
    paths = RunPaths(os.path.join(base, "runs", "lane-log"))
    adapter = FileLaneAdapter(paths.lanes_dir, REPO)
    request = _request("read-a/decompose/batch-0")
    directory = adapter.write_request(request)
    response_path = os.path.join(directory, "response.json")
    with open(response_path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "lane_id": request.lane_id,
                "model": request.model,
                "effort": request.effort,
                "input_digest": request.input_digest,
                "payload": {"items": []},
            },
            handle,
            ensure_ascii=False,
        )
    journal = read_stage.LaneJournal()
    read_stage._dispatch(adapter, [request], journal)
    if journal.rows[0].get("request_digest") is None:
        pytest.fail(f"FileLaneAdapter 행의 지문이 null이다: {journal.rows[0]!r}")
    read_stage._finish_lane_log(paths, journal)
    return paths, directory


def _messages(row) -> str:
    return "\n".join(finding.message for finding in row.findings)


def test_recorded_lane_log_control_passes(tmp_path) -> None:
    """⑴ FileLaneAdapter의 변조 전 비null 지문 기록본은 대조군으로 통과한다."""
    control_paths, _ = _recorded_round_trip(os.path.join(str(tmp_path), "control"))
    control = read_stage.check_lane_log_digest_value(
        read_stage._load_recorded_lane_log(control_paths),
        lanes_root=control_paths.lanes_dir,
    )
    if control.status != "pass":
        pytest.fail(f"⑴ 변조 전 대조군이 실패했다: {control.findings!r}")


def test_recorded_lane_log_rejects_shape_spoof(tmp_path) -> None:
    """⑵ 기록본 lane_id의 형태 위조는 파일 조립 전에 계약 사유로 거부한다."""
    shape_paths, _ = _recorded_round_trip(os.path.join(str(tmp_path), "shape"))
    with open(shape_paths.lane_log, encoding="utf-8") as handle:
        rows = json.load(handle)
    rows[0]["lane_id"] = "../../outside/batch-0"
    with open(shape_paths.lane_log, "w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False)
    shape = read_stage.check_lane_log_digest_value(
        read_stage._load_recorded_lane_log(shape_paths), lanes_root=shape_paths.lanes_dir
    )
    if shape.status != "fail" or "어휘 위반(형태)" not in _messages(shape):
        pytest.fail(f"⑵ 형태 위조를 계약 사유로 잡지 못했다: {shape.findings!r}")


def test_recorded_lane_log_rejects_directory_escape(tmp_path) -> None:
    """⑶ 정상 어휘의 중간 링크는 디렉터리 포함 사유로 거부한다."""
    directory_paths, directory = _recorded_round_trip(
        os.path.join(str(tmp_path), "directory")
    )
    decompose = os.path.dirname(directory)
    outside_decompose = os.path.join(str(tmp_path), "outside-directory")
    shutil.move(decompose, outside_decompose)
    os.symlink(outside_decompose, decompose)
    directory_row = read_stage.check_lane_log_digest_value(
        read_stage._load_recorded_lane_log(directory_paths),
        lanes_root=directory_paths.lanes_dir,
    )
    if directory_row.status != "fail" or "루트 밖(디렉터리)" not in _messages(directory_row):
        pytest.fail(f"⑶ 중간 링크를 디렉터리 사유로 잡지 못했다: {directory_row.findings!r}")


def test_recorded_lane_log_rejects_terminal_escape_before_open(tmp_path, monkeypatch) -> None:
    """⑷ 말단 링크는 바깥 파일을 열기 전에 거부한다(B-02·MU-1)."""
    terminal_paths, terminal_directory = _recorded_round_trip(
        os.path.join(str(tmp_path), "terminal")
    )
    request_md = os.path.join(terminal_directory, "request.md")
    outside_file = os.path.join(str(tmp_path), "outside-request.md")
    shutil.copyfile(request_md, outside_file)
    os.unlink(request_md)
    os.symlink(outside_file, request_md)
    calls: list[str] = []
    original = read_stage._bare_sha256_file

    def counted(path: str) -> str:
        calls.append(path)
        return original(path)

    monkeypatch.setattr(read_stage, "_bare_sha256_file", counted)
    terminal_row = read_stage.check_lane_log_digest_value(
        read_stage._load_recorded_lane_log(terminal_paths),
        lanes_root=terminal_paths.lanes_dir,
    )
    opened = [path for path in calls if path == request_md]
    if terminal_row.status != "fail" or "루트 밖(말단)" not in _messages(terminal_row):
        pytest.fail(
            f"⑷ 말단 링크를 계약 사유로 잡지 못했다: {terminal_row.findings!r} · "
            f"_bare_sha256_file 호출={len(opened)}"
        )
    if opened:
        pytest.fail(f"⑷ 거부 전에 루트 밖 request.md를 열었다: {opened!r}")


def test_lane_vocabulary_single_sources_are_bridged() -> None:
    """(ii)-D 정본 집합 두 벌과 엔진 기본값·plan 별칭의 동일성을 단언한다."""
    with open(
        os.path.join(REPO, "contracts", "schemas", "convergence.schema.json"),
        encoding="utf-8",
    ) as handle:
        schema = json.load(handle)
    with open(os.path.join(REPO, "contracts", "stages", "read.yaml"), encoding="utf-8") as handle:
        read_contract = yaml.safe_load(handle)
    read_runs = getattr(lane_contract, "READ_RUNS")
    lane_tasks = getattr(lane_contract, "LANE_TASKS")
    if read_runs != tuple(schema["$defs"]["read_run"]["enum"]):
        pytest.fail(f"READ_RUNS가 스키마 정본과 다르다: {read_runs!r}")
    expected_tasks = tuple(sub["id"] for sub in read_contract["lane"]["sub_lanes"])
    if lane_tasks != expected_tasks:
        pytest.fail(f"LANE_TASKS가 read.yaml 정본과 다르다: {lane_tasks!r}")
    if inspect.signature(read_stage.run).parameters["read_runs"].default != read_runs:
        pytest.fail("read_stage.run 기본값이 READ_RUNS와 다르다")
    if plan.TASKS is not lane_tasks:
        pytest.fail("plan.TASKS가 LANE_TASKS 객체를 그대로 가리키지 않는다")
