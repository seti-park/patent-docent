# -*- coding: utf-8 -*-
"""재정 T23 — CP1 미분류 목록의 실제 실행 귀속과 구 산출 호환 렌더를 고정한다."""

from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.render.material_spec_md import _has_duplicate_values, render  # noqa: E402


def render_unclassified(
    entries: list[dict],
    *,
    canonical_selection: dict | None = None,
    convergence_early: dict | None = None,
) -> str:
    spec = {
        "run_id": "render-notice-test",
        "spec_version": 1,
        "status": "draft",
        "schema": "material-spec/v0",
        "reader_version": "test",
    }
    convergence = {"unclassified_dependents": entries}
    if canonical_selection is not None:
        convergence["canonical_selection"] = canonical_selection
    return render(
        spec,
        convergence=convergence,
        contract={"owner_checkpoint": {}},
        repo=REPO,
        convergence_early=convergence_early,
    )


def test_has_duplicate_values_does_not_assume_hashability() -> None:
    """이 방어는 렌더 호출점에서 도달 불능(허용값 검사가 앞선다 · 재감사 3 RG-2) —
    헬퍼 단위에서 해시 가능성 비가정을 고정한다.
    """
    # 비해시 객체의 중복과 비중복을 직접 판별한다.
    if _has_duplicate_values([{}, {}]) is not True:
        pytest.fail("빈 객체 중복을 찾지 못했다")
    if _has_duplicate_values([{}, {"a": 1}]) is not False:
        pytest.fail("서로 다른 비해시 객체를 중복으로 보았다")
    # 위치와 순서가 달라도 비해시 객체 비교가 보존되어야 한다.
    if _has_duplicate_values([{}, {"a": 1}, {}]) is not True:
        pytest.fail("비인접 빈 객체 중복을 찾지 못했다")
    if _has_duplicate_values([{"a": 1}, {}]) is not False:
        pytest.fail("역순의 서로 다른 비해시 객체를 중복으로 보았다")
    # 리스트 원소도 해시 가능성을 가정하지 않고 비교한다.
    if _has_duplicate_values([[1], [1]]) is not True:
        pytest.fail("같은 리스트 원소의 중복을 찾지 못했다")
    if _has_duplicate_values([[1], [2]]) is not False:
        pytest.fail("서로 다른 리스트 원소를 중복으로 보았다")
    # 해시 가능한 문자열에 대한 기존 중복 판별도 회귀하지 않는다.
    if _has_duplicate_values(["read-a", "read-a"]) is not True:
        pytest.fail("같은 문자열의 중복을 찾지 못했다")
    if _has_duplicate_values(["read-a", "read-b"]) is not False:
        pytest.fail("서로 다른 문자열을 중복으로 보았다")


def test_unclassified_items_render_actual_attribution_without_the_old_notice() -> None:
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_status": "verbatim",
                "text_verbatim": "The assembly of claim 1 in a Markush form.",
                "reported_by": ["read-a"],
            }
        ],
        canonical_selection={
            "read_run": "read-a",
            "rule": "declaration-order",
            "content_blind": True,
        },
    )
    section = rendered.split("## 10. ★ 미분류 종속 구조", 1)[1].split(
        "## 10-b. ★ 조기 합집합", 1
    )[0]
    forbidden = [
        token
        for token in (
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
    scope = "이 목록은 정본 실행 `read-a` 의 신고다. 두 실행이 갈린 신고는 아래 10-b 블록에 있다."
    if scope not in section:
        pytest.fail(f"정본 실행 범위 표지 기대 {scope!r}")
    expected = "신고 실행: read-a"
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


def test_legacy_convergence_without_canonical_selection_omits_scope_and_attribution() -> None:
    """canonical_selection 없는 구 산출에는 정본 범위와 신고 실행을 지어내지 않는다."""
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_verbatim": "Legacy dependent claim text.",
            }
        ]
    )
    if "이 목록은 정본 실행" in rendered:
        pytest.fail("canonical_selection 없는 구 산출에 정본 범위 표지를 지어냈다")
    if "신고 실행:" in rendered:
        pytest.fail("reported_by 없는 구 산출에 신고 실행 줄을 지어냈다")


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


def test_early_union_without_split_reports_renders_one_agreement_line() -> None:
    """두 실행 전건 일치 때 10-b가 빈 표 대신 합의 상태 한 줄을 보여야 한다."""
    rendered = render_unclassified(
        [],
        convergence_early={
            "unclassified_dependents": [
                {
                    "claim": "CL-3",
                    "dependency_type": "unclassified",
                    "text_status": "verbatim",
                    "text_verbatim": "The assembly of claim 1 in a Markush form.",
                    "reported_by": ["read-a", "read-b"],
                }
            ]
        },
    )
    block = rendered.split("## 10-b. ★ 조기 합집합", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    expected = "갈린 신고 없음 — 두 실행의 미분류 신고가 전건 일치"
    if expected not in block:
        pytest.fail(f"갈린 신고 0건 안내 기대 {expected!r}")
    if "| `reported_by` |" in block:
        pytest.fail("갈린 신고 0건인데 표를 렌더했다")


def test_early_union_renders_only_split_reports_with_full_attribution() -> None:
    """갈린 신고 n건은 n행·귀속·전문 전량이고, 일치 항목은 표에서 빠져야 한다."""
    read_a_text = "The assembly of claim 1, selected from A, B, and C without truncation."
    read_b_text = "The method of claim 2, when the sensor reports a conditional state."
    agreed_text = "The apparatus of claim 1, wherein both readers agree."
    rendered = render_unclassified(
        [],
        convergence_early={
            "unclassified_dependents": [
                {
                    "claim": "CL-3",
                    "dependency_type": "unclassified",
                    "text_status": "verbatim",
                    "text_verbatim": read_a_text,
                    "reported_by": ["read-a"],
                },
                {
                    "claim": "CL-4",
                    "dependency_type": "unclassified",
                    "text_status": "verbatim",
                    "text_verbatim": read_b_text,
                    "reported_by": ["read-b"],
                },
                {
                    "claim": "CL-5",
                    "dependency_type": "unclassified",
                    "text_status": "verbatim",
                    "text_verbatim": agreed_text,
                    "reported_by": ["read-a", "read-b"],
                },
            ]
        },
    )
    block = rendered.split("## 10-b. ★ 조기 합집합", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    header = "| `reported_by` | `claim` | `dependency_type` | `text_status` | `text_verbatim` |"
    if header not in block:
        pytest.fail(f"10-b 귀속 표 머리 기대 {header!r}")
    rows = [line for line in block.splitlines() if line.startswith("| `read-")]
    if len(rows) != 2:
        pytest.fail(f"갈린 신고 기대 2행, 실제 {len(rows)}행: {rows}")
    for expected in ("`read-a`", "`read-b`", "`CL-3`", "`CL-4`", read_a_text, read_b_text):
        if expected not in block:
            pytest.fail(f"10-b 갈린 신고 표에 {expected!r} 이 없다")
    if agreed_text in block or "`CL-5`" in block:
        pytest.fail("두 실행이 일치 신고한 항목이 갈린 신고 표에 들어갔다")


MISSING_REPORTED_BY = object()


ATTRIBUTION_SHAPE_CASES = (
    pytest.param([["read-a"], []], 1, 0, 0, 0, 0, id="G01-singleton-plus-empty"),
    pytest.param([[]], 1, 0, 0, 0, 0, id="G02-empty-list"),
    pytest.param([MISSING_REPORTED_BY], 1, 0, 0, 0, 0, id="G03-key-absent"),
    pytest.param([None], 1, 0, 0, 0, 0, id="G04-null"),
    pytest.param([False], 1, 0, 0, 0, 0, id="G05-false"),
    pytest.param([0], 1, 0, 0, 0, 0, id="G06-zero"),
    pytest.param([""], 1, 0, 0, 0, 0, id="G07-empty-string"),
    pytest.param([{}], 1, 0, 0, 0, 0, id="G08-empty-object"),
    pytest.param([[], ["read-c"], ["read-a"]], 1, 0, 0, 0, 0, id="G09-empty-plus-invalid-plus-singleton"),
    pytest.param([["read-a", "read-b", "read-c"]], 0, 1, 1, 0, 0, id="I01-length-three"),
    pytest.param(["read-a"], 0, 1, 1, 0, 0, id="I02-string"),
    pytest.param([5], 0, 1, 1, 0, 0, id="I03-number"),
    pytest.param([{"read-a": 1}], 0, 1, 1, 0, 0, id="I04-object"),
    pytest.param([["read-c"]], 0, 1, 1, 0, 0, id="I05-unknown-singleton"),
    pytest.param([["read-c", "read-d"]], 0, 1, 1, 0, 0, id="I06-two-unknown-values"),
    pytest.param([["read-a", "read-b"], ["read-c"]], 0, 1, 1, 0, 0, id="I07-agreement-plus-invalid"),
    pytest.param([["read-a", "read-a"]], 0, 1, 1, 0, 0, id="I08-duplicate-a"),
    pytest.param([True], 0, 1, 1, 0, 0, id="I09-true"),
    pytest.param([[None]], 0, 1, 1, 0, 0, id="I10-list-null"),
    pytest.param([[False]], 0, 1, 1, 0, 0, id="I11-list-false"),
    pytest.param([[{}]], 0, 1, 1, 0, 0, id="I12-list-object"),
    pytest.param([[[]]], 0, 1, 1, 0, 0, id="I13-list-list"),
    pytest.param([[{}, {}]], 0, 1, 1, 0, 0, id="I14-duplicate-unhashable-objects"),
    pytest.param([["read-b", "read-b"]], 0, 1, 1, 0, 0, id="I15-duplicate-b"),
    pytest.param(
        [["read-a", "read-b", "read-c"], ["read-a", "read-b", "read-c"]],
        0,
        1,
        2,
        0,
        0,
        id="I2-01-two-length-three-items",
    ),
    pytest.param(
        [["read-a"], ["read-a", "read-b", "read-c"]],
        0,
        1,
        1,
        1,
        0,
        id="I1T01-invalid-then-one-table-row",
    ),
    pytest.param([["read-a", "read-b"]], 0, 0, 0, 0, 1, id="A01-a-b"),
    pytest.param([["read-b", "read-a"]], 0, 0, 0, 0, 1, id="A02-b-a"),
    pytest.param([], 0, 0, 0, 0, 1, id="A03-no-unclassified-items"),
    pytest.param([["read-a"]], 0, 0, 0, 1, 0, id="T01-singleton-a"),
)


@pytest.mark.parametrize(
    (
        "reported_by_values",
        "expected_missing",
        "expected_invalid_lines",
        "expected_invalid_count",
        "expected_rows",
        "expected_agreement",
    ),
    ATTRIBUTION_SHAPE_CASES,
)
def test_early_union_attribution_shape_table(
    reported_by_values,
    expected_missing: int,
    expected_invalid_lines: int,
    expected_invalid_count: int,
    expected_rows: int,
    expected_agreement: int,
) -> None:
    """MB-2 형태표 30사례 — 우선순위·계수·표·합의와 혼재 순서를 사례별 고정한다."""
    entries = []
    for index, reported_by in enumerate(reported_by_values):
        entry = {
            "claim": f"CL-{index + 3}",
            "dependency_type": "unclassified",
            "text_status": "verbatim",
            "text_verbatim": f"Attribution shape case item {index + 1}.",
        }
        if reported_by is not MISSING_REPORTED_BY:
            entry["reported_by"] = reported_by
        entries.append(entry)

    rendered = render_unclassified(
        [], convergence_early={"unclassified_dependents": entries}
    )
    block = rendered.split(
        "## 10-b. ★ 조기 합집합 — 두 실행이 갈린 미분류 신고 (재정 T31)", 1
    )[1].split("## 11. ★ 맹검 스크리닝 메모", 1)[0]
    invalid_line = "귀속 값이 규격 밖 — 두 실행(read-a·read-b) 외 값 또는 형태 이상"
    table_header = "| `reported_by` | `claim` | `dependency_type` | `text_status` | `text_verbatim` |"
    agreement_line = "갈린 신고 없음 — 두 실행의 미분류 신고가 전건 일치"
    rows = [line for line in block.splitlines() if line.startswith("| `read-")]

    actual_missing = block.count("귀속 정보 없음 — 구 판 산출(재정 T23 이전)")
    if actual_missing != expected_missing:
        pytest.fail(f"귀속 정보 없음 기대 {expected_missing}회, 실제 {actual_missing}회: {block!r}")
    actual_invalid_lines = block.count(invalid_line)
    if actual_invalid_lines != expected_invalid_lines:
        pytest.fail(
            f"규격 밖 안내 기대 {expected_invalid_lines}회, 실제 {actual_invalid_lines}회: {block!r}"
        )
    if expected_invalid_lines:
        expected_count_text = f"항목 {expected_invalid_count}건"
        if expected_count_text not in block:
            pytest.fail(f"규격 밖 계수 기대 {expected_count_text!r}: {block!r}")
    expected_headers = 1 if expected_rows else 0
    actual_headers = block.count(table_header)
    if actual_headers != expected_headers:
        pytest.fail(f"표 머리 기대 {expected_headers}회, 실제 {actual_headers}회: {block!r}")
    if len(rows) != expected_rows:
        pytest.fail(f"표 본문 기대 {expected_rows}행, 실제 {len(rows)}행: {rows!r}")
    actual_agreement = block.count(agreement_line)
    if actual_agreement != expected_agreement:
        pytest.fail(f"전건 일치 기대 {expected_agreement}회, 실제 {actual_agreement}회: {block!r}")

    if expected_missing:
        forbidden = [token for token in (invalid_line, table_header, agreement_line) if token in block]
        if forbidden:
            pytest.fail(f"귀속 없음 우선 갈래에 후순위 출력이 섞였다: {forbidden!r}")
    if (
        expected_invalid_lines
        and expected_rows
        and block.index(invalid_line) >= block.index(table_header)
    ):
        pytest.fail("혼재 출력은 규격 밖 안내 줄이 표 머리보다 앞서야 한다")


def test_legacy_run_without_early_verdict_renders_notice_without_error() -> None:
    """조기 판정서 없는 구 런은 예외 없이 행위시법 안내 한 줄을 렌더해야 한다."""
    rendered = render_unclassified([])
    block = rendered.split("## 10-b. ★ 조기 합집합", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    expected = "조기 판정서 없음 — 구 판 산출"
    if expected not in block:
        pytest.fail(f"조기 판정서 부재 안내 기대 {expected!r}")


def test_final_verdict_cannot_substitute_for_missing_early_verdict() -> None:
    """최종 판정서만 있어도 조기 판정서 부재를 전건 일치로 갈음하지 않는다."""
    rendered = render_unclassified(
        [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_status": "verbatim",
                "text_verbatim": "Both final readers reported this dependent claim.",
                "reported_by": ["read-a", "read-b"],
            }
        ],
        convergence_early=None,
    )
    block = rendered.split("## 10-b. ★ 조기 합집합", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    if "조기 판정서 없음 — 구 판 산출" not in block:
        pytest.fail("최종 판정서를 조기 판정서로 갈음하지 않고 부재를 밝혀야 한다")
    if "전건 일치" in block:
        pytest.fail("조기 판정서가 없는데 최종 판정서로 전건 일치를 선언했다")


def test_legacy_early_item_without_attribution_does_not_declare_agreement() -> None:
    """reported_by 없는 구 조기 판정서는 귀속 부재를 밝히고 일치를 선언하지 않는다."""
    rendered = render_unclassified(
        [],
        convergence_early={
            "unclassified_dependents": [
                {
                    "claim": "CL-3",
                    "dependency_type": "unclassified",
                    "text_verbatim": "Legacy dependent claim text.",
                }
            ]
        },
    )
    block = rendered.split("## 10-b. ★ 조기 합집합", 1)[1].split(
        "## 11. ★ 맹검 스크리닝 메모", 1
    )[0]
    if "귀속 정보 없음 — 구 판 산출(재정 T23 이전)" not in block:
        pytest.fail("reported_by 없는 구 조기 판정서에 귀속 정보 부재 안내가 없다")
    if "전건 일치" in block:
        pytest.fail("reported_by 없는 구 조기 판정서가 전건 일치를 선언했다")
