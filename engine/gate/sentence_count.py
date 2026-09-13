# -*- coding: utf-8 -*-
"""문장 계수 — `contracts/l0-format.yaml#sentence_counting`(재정 N3 · 결정론 보장)의 구현.

기본 규칙: 문장 1개 = 줄 1개(비어 있지 않은 본문 줄 수). 한 줄 안에 종결부호가 2회 이상이면 줄 안을
다시 센다(뒷문 봉쇄) — 경계 = 종결부호 다음이 공백 또는 줄끝인 지점. 재계수는 약어 예외 목록 ·
소수점 가드 · 머리글자 가드를 적용하며 비교는 소문자화 후다.

★ 종결부호 · 예외 목록 · 대소문자 규칙은 전부 파일에서 온다. 예외 목록의 확장은 Owner 재정 사항이다(D7).
"""

from __future__ import annotations

from ..stages import StageError


def _load_spec(spec: dict) -> tuple[tuple[str, ...], frozenset[str], bool]:
    try:
        terminators = tuple(str(t) for t in spec["terminators"])
        exceptions = spec.get("exceptions") or {}
        abbreviations = frozenset(str(a).lower() for a in (exceptions.get("abbreviations") or []))
        fold = str(spec.get("case_folding", "lowercase")) == "lowercase"
    except (KeyError, TypeError) as exc:
        raise StageError(f"sentence_counting 블록이 불완전하다: {exc}") from exc
    if not terminators:
        raise StageError("sentence_counting.terminators 가 비어 있다")
    return terminators, abbreviations, fold


def _boundaries(line: str, terminators: tuple[str, ...], abbreviations: frozenset[str], fold: bool) -> int:
    """줄 안의 문장 경계 수(예외 적용 후)."""
    count = 0
    n = len(line)
    for i, char in enumerate(line):
        if char not in terminators:
            continue
        # 경계 조건 — 다음 문자가 공백이거나 줄끝.
        if i + 1 < n and not line[i + 1].isspace():
            continue
        if char == ".":
            # 소수점 가드 — 숫자 사이의 '.' (줄끝은 숫자 뒤가 아니므로 해당 없음).
            if i > 0 and i + 1 < n and line[i - 1].isdigit() and line[i + 1].isdigit():
                continue
            # 직전 단어(공백 이후 ~ 이 종결부호까지).
            start = i
            while start > 0 and not line[start - 1].isspace():
                start -= 1
            word = line[start:i + 1]
            word_cmp = word.lower() if fold else word
            if word_cmp in abbreviations:
                continue
            # 머리글자 가드 — 단일 대문자 뒤의 '.' (예: A. B.).
            if len(word) == 2 and word[0].isalpha() and word[0].isupper():
                continue
        count += 1
    return count


def count_sentences(text: str, spec: dict) -> int:
    """트윗 본문(태그 제거본)의 문장 수."""
    terminators, abbreviations, fold = _load_spec(spec)
    total = 0
    for line in text.split("\n"):
        if not line.strip():
            continue
        raw_terminators = sum(1 for char in line if char in terminators)
        if raw_terminators >= 2:
            total += max(1, _boundaries(line, terminators, abbreviations, fold))
        else:
            total += 1
    return total


__all__ = ["count_sentences"]
