# -*- coding: utf-8 -*-
"""감사 A-7 — reported_by enum과 READ 기본 실행 id 어휘의 순서 결속을 고정한다.

`canonical_selection.read_run`은 현재 자유 문자열이며 값 공간 구속이 상신 중이므로 이 시험은
그 자리를 대조하지 않는다.
"""

from __future__ import annotations

import inspect
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.stages import read as read_stage  # noqa: E402


def test_reported_by_enum_matches_default_read_runs_in_order() -> None:
    """스키마 신고 실행 enum과 엔진 기본 실행 id는 순서까지 같아야 한다."""
    path = os.path.join(REPO, "contracts", "schemas", "convergence.schema.json")
    with open(path, encoding="utf-8") as handle:
        schema = json.load(handle)
    try:
        enum = schema["properties"]["unclassified_dependents"]["items"]["properties"][
            "reported_by"
        ]["items"]["enum"]
    except (KeyError, TypeError) as exc:
        pytest.fail(f"reported_by.items.enum 정본 경로가 없다: {exc}")
    default = inspect.signature(read_stage.run).parameters["read_runs"].default
    if list(default) != enum:
        pytest.fail(
            "reported_by enum과 run(read_runs=...) 기본값이 순서까지 같지 않다: "
            f"schema={enum!r}, engine={list(default)!r}"
        )
