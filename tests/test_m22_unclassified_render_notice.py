# -*- coding: utf-8 -*-
"""재정 T23 — CP1 미분류 목록의 실제 실행 귀속과 구 산출 호환 렌더를 고정한다."""

from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.render.material_spec_md import render  # noqa: E402


def render_unclassified(entries: list[dict]) -> str:
    spec = {
        "run_id": "render-notice-test",
        "spec_version": 1,
        "status": "draft",
        "schema": "material-spec/v0",
        "reader_version": "test",
    }
    convergence = {"unclassified_dependents": entries}
    return render(spec, convergence=convergence, contract={"owner_checkpoint": {}}, repo=REPO)


def test_unclassified_items_render_actual_attribution_without_the_old_notice() -> None:
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_status": "verbatim",
                "text_verbatim": "The assembly of claim 1 in a Markush form.",
                "reported_by": ["read-a", "read-b"],
            }
        ]
    )
    section = rendered.split("## 10. ★ 미분류 종속 구조", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    forbidden = [
        token
        for token in (
            "두 실행",
            "합집합",
            "두 행",
            "additionalProperties: false",
            "어느 실행의 신고인지",
            "재정 T14",
            "감수하고 넘어가는 것의 명기",
            "상신 중",
        )
        if token in section
    ]
    if forbidden:
        pytest.fail(f"삭제되어야 할 실행 귀속 한계 고지 토큰이 남았다: {forbidden}")
    expected = "신고 실행: read-a, read-b"
    if expected not in section:
        pytest.fail(f"실제 실행 귀속 줄 기대 {expected!r}")


def test_absent_text_is_reported_as_absent_without_quoting_it() -> None:
    marker = "THIS MUST NOT BE QUOTED AS CLAIM TEXT"
    rendered = render_unclassified(
        [
            {
                "claim": "CL-9",
                "dependency_type": "unclassified",
                "text_status": "absent",
                "text_verbatim": marker,
            }
        ]
    )
    for token in ("전문 부재 신고", "text_verbatim", "재정 2026-09-01 T18", "부재 자체가 신호"):
        if token not in rendered:
            pytest.fail(f"absent 미분류 항목의 부재 신고에 {token!r} 이 없다")
    if marker in rendered:
        pytest.fail("text_status=absent 항목의 text_verbatim 을 청구항 문언처럼 인용했다")


def test_legacy_item_without_text_status_keeps_the_old_rendering() -> None:
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_verbatim": "Legacy dependent claim text.",
            }
        ]
    )
    expected = "전문: “Legacy dependent claim text.”"
    if expected not in rendered:
        pytest.fail(f"text_status 없는 구 산출 렌더 기대 {expected!r}")
    if "신고 실행:" in rendered:
        pytest.fail("reported_by 없는 구 산출물에 실행 귀속 줄을 지어냈다")


def test_verbatim_text_is_rendered_exactly() -> None:
    text = "The feeder assembly of claim 1, wherein the valve has pockets."
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_status": "verbatim",
                "text_verbatim": text,
            }
        ]
    )
    expected = f"전문: “{text}”"
    if expected not in rendered:
        pytest.fail(f"verbatim 미분류 항목 문언 기대 {expected!r}")
