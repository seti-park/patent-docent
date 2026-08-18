# -*- coding: utf-8 -*-
"""재정 ↔ 문서 전사 대조 — 원장이 상류이고 문서가 하류라는 규율의 **기계 집행**.

CLAUDE.md §0 과 재정 N6 이 정한 순서는 하나다: **재정 발생 → 원장 등재 → 문서 반영.**
원장과 문서가 어긋나면 원장이 이긴다. 그런데 그 규율을 집행하는 것이 없으면, 재정이
문서에 닿지 못한 채(전사 누락) 또는 원장 없이 문서에만 나타난 채(출처 없는 조문) 지나간다 —
M0 부터 반복된 사고 형태이며 재정 N6 이 그 처분이다.

이 파일이 보는 것은 **세 자리의 정합**이다.

  ① 원장 파일 §1 에 재정 라벨이 전건 실재하는가(머리말의 `entries:` 가 그 목록의 정본이다)
  ② 각 라벨이 **최소 1개 하류 파일**에서 인용되는가(반영되지 않은 재정이 조용히 남지 않는다)
  ③ 원장 파일이 색인(`RULINGS-LEDGER.md` §2)에 등재되고 `text_status` 를 선언하는가

여기서 `assert` 를 쓰는 것은 무방하다(pytest 는 AST 재작성으로 assert 를 if/raise 로 바꾸므로
`python3 -O` 에서도 사라지지 않는다 — CLAUDE.md §3). 서브프로세스는 쓰지 않는다.
"""

from __future__ import annotations

import glob
import os
import re

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULING_REL = os.path.join("docs", "decisions", "ruling-20260818-03-P1-P11.md")
LEDGER_REL = os.path.join("docs", "decisions", "RULINGS-LEDGER.md")

# 하류 = 재정이 닿아야 하는 자리. 원장 자신과 총괄 문서(`D-*.md`)는 대상이 아니다 —
# 전자는 상류이고 후자는 처분 기록이지 반영처가 아니다.
DOWNSTREAM_GLOBS = (
    os.path.join("docs", "CHARTER.md"),
    os.path.join("docs", "SPEC.md"),
    os.path.join("contracts", "**", "*"),
    os.path.join("reader", "**", "*"),
    os.path.join("engine", "**", "*"),
    os.path.join("tools", "**", "*"),
)


def _read(relative: str) -> str:
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


RULING = _read(RULING_REL)
LEDGER = _read(LEDGER_REL)


def _declared_labels() -> list[str]:
    """머리말 `entries:` 가 든 P 계열 라벨 목록.

    목록을 이 파일에 리터럴로 두지 않는 이유는 그러면 **사본이 하나 더 생기기** 때문이다 —
    사본은 반드시 낡고, 낡은 사본으로 원장을 검사하면 검사가 원장을 따라가지 못한다.
    `P-U1+P-8` 처럼 한 블록에 둘이 묶인 자리도 라벨은 둘로 센다.
    """
    match = re.search(r"^entries:\s*(.+?)^\w+:", RULING, re.MULTILINE | re.DOTALL)
    if match is None:
        pytest.fail("원장 머리말에서 `entries:` 를 찾지 못했다")
    labels = re.findall(r"P-(?:U[0-9]|[0-9]+|[A-C])", match.group(1))
    ordered: list[str] = []
    for label in labels:
        if label not in ordered:
            ordered.append(label)
    return ordered


DECLARED_LABELS = _declared_labels()


def _pattern(label: str) -> re.Pattern:
    """`P-1` 이 `P-11` 안에서 매칭되지 않도록 오른쪽 경계를 요구한다."""
    return re.compile(re.escape(label) + r"(?![0-9])")


def _downstream_files() -> list[str]:
    found: list[str] = []
    for pattern in DOWNSTREAM_GLOBS:
        for path in glob.glob(os.path.join(REPO, pattern), recursive=True):
            if os.path.isfile(path) and "__pycache__" not in path:
                found.append(path)
    return sorted(set(found))


DOWNSTREAM_FILES = _downstream_files()


def test_ledger_declares_the_entries_it_carries():
    """머리말이 목록을 들지 않으면 아래 대조 전부가 무엇에 대한 것인지 말할 수 없다."""
    assert DECLARED_LABELS, "머리말 `entries:` 에서 P 계열 라벨을 하나도 뽑지 못했다"
    # 발주문·원장 §표기 주의 2 가 센 수 = 블록 17 · 라벨 18(`P-U1+P-8` 이 한 블록이다).
    assert len(DECLARED_LABELS) == 18, (
        f"P 계열 라벨 18개 기대, 실제 {len(DECLARED_LABELS)}개 — {DECLARED_LABELS}"
    )


def test_every_declared_ruling_has_a_block_in_the_original_text():
    """머리말이 든 라벨의 조문이 §1 에 없으면, 원장이 '있다고 적힌 재정'을 들고 있는 것이다."""
    body = RULING[RULING.index("## §1"):RULING.index("## §2")]
    # 조문의 머리는 굵은 글씨다. `P-U1 … + P-8 …` 처럼 한 머리에 둘이 묶인 자리가 있으므로
    # 라벨을 머리 **문자열 안**에서 찾는다(머리의 시작을 요구하면 묶인 쪽을 놓친다).
    headers = re.findall(r"\*\*(.+?)\*\*", body, re.DOTALL)
    assert headers, "§1 에서 조문 머리를 하나도 찾지 못했다"
    missing = [
        label for label in DECLARED_LABELS
        if not any(_pattern(label).search(header) for header in headers)
    ]
    assert not missing, f"§1 에 조문 블록이 없는 라벨: {missing}"


def test_every_ruling_is_cited_by_at_least_one_downstream_file():
    """반영되지 않은 재정은 조용히 남는다 — 원장이 상류라는 규율은 하류가 그것을 인용할 때만 성립한다."""
    assert DOWNSTREAM_FILES, "하류 파일을 하나도 찾지 못했다 — 이 시험이 공허해진다"
    texts = {}
    for path in DOWNSTREAM_FILES:
        try:
            with open(path, encoding="utf-8") as handle:
                texts[path] = handle.read()
        except (UnicodeDecodeError, OSError):
            continue  # 바이너리 자산은 인용의 자리가 아니다

    uncited: list[str] = []
    for label in DECLARED_LABELS:
        pattern = _pattern(label)
        if not any(pattern.search(text) for text in texts.values()):
            uncited.append(label)
    assert not uncited, (
        f"하류 어디에서도 인용되지 않은 재정: {uncited} — "
        "재정이 원장에만 있고 계약·코드·스펙에 닿지 않았다"
    )


def test_ledger_index_lists_this_ruling_file():
    """색인에 없는 원장 파일은 제도 밖의 문서가 된다 — 다음 사람이 그것을 찾을 경로가 없다."""
    index = LEDGER[LEDGER.index("## §2"):]
    basename = os.path.basename(RULING_REL)
    assert basename in index, f"RULINGS-LEDGER §2 색인에 {basename} 행이 없다"
    row = next(line for line in index.splitlines() if basename in line)
    assert "원문" in row, f"색인 행이 원문/재구성본 구별을 적지 않았다: {row}"


def test_ruling_file_declares_its_text_status():
    """원문과 재구성본을 구별해 적지 않으면 사후 재구성이 원문으로 위장할 수 있다(재정 N6·N7)."""
    match = re.search(r"^text_status:\s*(\S+)", RULING, re.MULTILINE)
    assert match is not None, "원장 파일에 `text_status` 선언이 없다"
    assert match.group(1) == "원문", (
        f"이 원장은 발주문에 담겨 내려온 원문이다 — text_status={match.group(1)!r}"
    )
    # 지위 문단이 그 사실을 산문으로도 밝히는지 본다(기계 표기만 있으면 읽는 사람이 놓친다).
    assert "요약·의역·재구성이 없다" in RULING, "원문 선언의 근거 문장이 본문에 없다"
