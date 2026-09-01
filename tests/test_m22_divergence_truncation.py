"""백로그 G-10 의 처분 — 수렴 갈림 보고가 갈린 자리를 보일 수 있는가.

근거 = 재정 2026-09-01 **T15 ④**(총괄 재량 즉시 집행) · 상신 `docs/decisions/D-20260901-01-pdm2-split.md`.

**무엇이 문제였나.** 갈림 항목은 `(부모 문언, 자식 문언)` 튜플인데, 구 구현이 그것을 `" | "` 로
이어 붙인 **뒤** 앞에서 잘랐다. 부모가 긴 축(`tree-edges` 의 부모 = 청구항 전문)에서는 부모가
예산을 통째로 먹어 **자식이 아예 들어가지 않았고**, 그 결과 부모가 같은 항목들이 **저장
문자열까지 동일**해졌다.

실측(2026-09-01 · `gdm-wo2026128750a1-agent-memory`): `only_in_canonical` **5건이 전부 같은
202자**. 보고서가 「무엇이 갈렸는가」를 보이려고 존재하는데 **정확히 그때** 아무것도 보이지
않았다. 표시만의 문제가 아니라 파일에 잘린 채 저장되어 **사후 복구도 불가**했다.

★ 이 결함은 기계 검사 13행·관문 8회가 전부 통과한 상태에서 **Owner 가 판독본을 읽다 발견**했다.
"""

from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from reader.lib.convergence import _MIN_PART_CHARS, _truncate_parts  # noqa: E402

# 실물 재현 — WO CL-1 의 전문(868 B)만큼 긴 부모.
LONG_PARENT = (
    "A computer-implemented method, comprising:\n\nreceiving, by a machine-learned agent "
    "system, a query associated with a user;\n\naccessing, by the machine-learned agent "
    "system, memory data from an interaction memory datastore associated with the user"
) + ("x" * 600)

CHILDREN = (
    "receiving, by a machine-learned agent system, a query associated with a user",
    "accessing, by the machine-learned agent system, memory data from an interaction",
    "inputting, by the machine-learned agent system and to a sequence processing model",
    "generating, by the machine-learned agent system and based on processing the input",
    "outputting, by the machine-learned agent system, and based on the output, a response",
)

WIDTH = 200
SUFFIX = " …"


def test_long_parent_does_not_swallow_the_child() -> None:
    """★ G-10 의 본체. 부모가 예산을 다 먹으면 다섯 항목이 한 문자열로 접힌다.

    반증 대상: 이어 붙인 뒤 앞에서 자르는 구 구현. 그 구현에서 아래 집합의 크기는 **1** 이다.
    """
    rendered = [_truncate_parts((LONG_PARENT, child), WIDTH, SUFFIX) for child in CHILDREN]
    if len(set(rendered)) != len(CHILDREN):
        pytest.fail(
            f"부모가 긴 축에서 항목이 접혔다: 고유 {len(set(rendered))} / {len(CHILDREN)}\n"
            "— 갈린 자리를 보이려는 보고가 정확히 그때 못 보이는 상태다"
        )
    for child, text in zip(CHILDREN, rendered):
        head = child[: _MIN_PART_CHARS]
        if head not in text:
            pytest.fail(f"자식이 들어가지 않았다: {head!r} ∉ {text[-90:]!r}")


def test_each_part_keeps_a_floor_even_when_parts_are_many() -> None:
    """부분이 늘어도 각 부분이 식별 가능해야 한다 — 예산 나눗셈이 0 으로 수렴하면 안 된다."""
    parts = tuple(f"part-{i}-" + "y" * 400 for i in range(12))
    text = _truncate_parts(parts, WIDTH, SUFFIX)
    for i in range(12):
        if f"part-{i}-" not in text:
            pytest.fail(f"부분 {i} 가 사라졌다(하한 {_MIN_PART_CHARS} 미달): {text[:120]!r}")


def test_short_values_are_untouched() -> None:
    """자르지 않아도 되는 값에 절단 표시가 붙으면 보고가 거짓을 말한다."""
    for value in ("짧은 값", ("가", "나"), ""):
        text = _truncate_parts(value, WIDTH, SUFFIX)
        if SUFFIX.strip() in text:
            pytest.fail(f"짧은 값에 절단 표시가 붙었다: {value!r} -> {text!r}")


def test_single_string_axis_still_renders() -> None:
    """축마다 원소 형태가 다르다(문자열·튜플). 튜플만 고치고 문자열을 깨뜨리면 안 된다."""
    long_single = "z" * 900
    text = _truncate_parts(long_single, WIDTH, SUFFIX)
    if not text.endswith(SUFFIX):
        pytest.fail(f"긴 단일 문자열이 잘리지 않았다: len={len(text)}")
    if len(text) > WIDTH + len(SUFFIX):
        pytest.fail(f"단일 문자열의 폭이 예산을 넘었다: {len(text)}")


def test_rendering_is_deterministic() -> None:
    """같은 두 독해가 매번 다른 보고서를 내면 상신 서식이 근거가 되지 못한다."""
    a = _truncate_parts((LONG_PARENT, CHILDREN[0]), WIDTH, SUFFIX)
    b = _truncate_parts((LONG_PARENT, CHILDREN[0]), WIDTH, SUFFIX)
    if a != b:
        pytest.fail("같은 입력이 다른 문자열을 냈다")
