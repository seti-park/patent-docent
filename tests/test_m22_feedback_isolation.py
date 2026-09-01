# -*- coding: utf-8 -*-
"""감사 지적 B-2 — 두 실행이 함께 실패할 때 검사 소견의 비누설을 반증한다."""

from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402


def test_peer_findings_do_not_reach_the_other_run(tmp_path) -> None:
    """상대 실행의 Finding.found 가 재시도 요청서로 방송되면 독립 독해가 무너진다."""
    marker_a = "SENTINEL-A-8f31"
    marker_b = "SENTINEL-B-2c07"
    if marker_a in m2.SOURCE or marker_b in m2.SOURCE:
        pytest.fail("비누설 표지가 요청서에 인라인되는 원천에 이미 있다")

    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source status 기대 ok, 실제 {source_outcome['status']}")
    first = {
        "read-a": m2.payload_set(claim_three_text=m2.CLAIM_3 + f" {marker_a}"),
        "read-b": m2.payload_set(claim_three_text=m2.CLAIM_3 + f" {marker_b}"),
    }
    second = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    m2.write_lane_responses(root, payloads_by_run=first, attempts=(0,))
    lanes_root = m2.write_lane_responses(root, payloads_by_run=second, attempts=(1,))
    adapter = m2.ReplayLaneAdapter(lanes_root)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"회차 1 정상 응답 뒤 status 기대 ok, 실제 {outcome['status']}")

    instructions = {}
    for read_run in ("read-a", "read-b"):
        lane_id = f"{read_run}/decompose/retry-1/batch-0"
        matches = [request for request in adapter.dispatched if request.lane_id == lane_id]
        if len(matches) != 1:
            pytest.fail(f"{lane_id} 재시도 요청 기대 1개, 실제 {len(matches)}")
        instructions[read_run] = matches[0].instructions

    # 대조군: 되먹임이 통째로 비어도 비누설 단언은 참이므로 자기 표지부터 실제 존재시킨다.
    if marker_a not in instructions["read-a"]:
        pytest.fail("read-a 재시도 요청서에 자기 실패 표지가 없다")
    if marker_b not in instructions["read-b"]:
        pytest.fail("read-b 재시도 요청서에 자기 실패 표지가 없다")

    if marker_b in instructions["read-a"]:
        pytest.fail("read-a 재시도 요청서에 read-b 검사 소견 표지가 누설됐다")
    if marker_a in instructions["read-b"]:
        pytest.fail("read-b 재시도 요청서에 read-a 검사 소견 표지가 누설됐다")
