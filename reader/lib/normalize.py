# -*- coding: utf-8 -*-
"""수치 정규화 표 — **단일 구현**.

정본 문언은 두 곳에 있고 답은 하나여야 한다.

  - `reader/reader-rules.yaml#value_grammar.render.number_normalization` (재료 쪽)
  - `contracts/l0-format.yaml` §9 `numeric.normalization` (본문 쪽)

두 쪽이 같은 MATCH_KEY 를 만들지 못하면 숫자 전수 대조가 성립하지 않는다. 구현은 이 파일
한 벌뿐이며(SPEC §8.4 M1 — 게이트·계기가 이것을 import 한다), 두 문언의 동치는
`tests/test_m1_reader.py::test_normalization_table_matches_l0_contract` 가 매 실행 대조한다.
**사본이 아니라 대조**로 묶는 이유는 `reader/` 가 `contracts/` 를 읽으면 이식 단위가 깨지기
때문이다(SPEC §6.2 판별식 1).

산출 문자열은 스키마 `$defs/decimal`(`^-?(?:0|[1-9][0-9]*)(?:[.][0-9]*[1-9])?$`)을 만족한다 —
선행 `+` 없음 · 선행 0 패딩 없음 · 후행 0 없음 · 과학표기 없음.
"""

from __future__ import annotations

import decimal
import unicodedata

from .rules import Rules

# ---------------------------------------------------------------------------
# 단위 별칭 — `contracts/l0-format.yaml` §9 numeric.normalization.unit_aliases 와 동일.
# 확장은 입법이며 Owner 재정 사항이다(l0-format 문언). 여기서 임의로 늘리지 않는다.
# ---------------------------------------------------------------------------
UNIT_ALIASES: dict[str, str] = {
    "um": "µm",
    "micron": "µm",
    "℃": "°c",
    "$": "usd",
}

# 과학표기 전개 자릿수 상한. 초과 시 실패한다(규칙 문언: "전개 자릿수가 30 을 넘으면 실패").
MAX_EXPANDED_DIGITS = 30

# 십진 파싱은 유효숫자 손실 없이 해야 하므로 넉넉한 정밀도를 쓴다.
_CONTEXT = decimal.Context(prec=60)

_RULES: Rules | None = None


class NormalizeError(ValueError):
    """정규화 불능 — 십진 문법 위반, 전개 자릿수 초과."""


def _rules() -> Rules:
    """십진 토큰 패턴은 규칙 파일이 정본이다(코드에 리터럴로 두지 않는다)."""
    global _RULES
    if _RULES is None:
        _RULES = Rules.load()
    return _RULES


def _to_ascii_digits(text: str) -> str:
    """유니코드 숫자를 ASCII 로 정규화한다(l0: unicode_digits)."""
    out = []
    for char in text:
        if char.isdigit() and not ("0" <= char <= "9"):
            digit = unicodedata.digit(char, None)
            if digit is None:
                out.append(char)
            else:
                out.append(str(digit))
        else:
            out.append(char)
    return "".join(out)


def _count_digits(text: str) -> int:
    return sum(1 for char in text if char.isdigit())


def format_decimal(value: decimal.Decimal) -> str:
    """`Decimal` 을 정규 십진 문자열로 편다. 과학표기를 쓰지 않는다."""
    if value.is_nan() or value.is_infinite():
        raise NormalizeError(f"유한수가 아니다: {value}")
    if value == 0:
        # `-0` 과 `0` 이 다른 MATCH_KEY 를 만들지 않도록 부호 없는 0 으로 접는다.
        return "0"
    text = format(value, "f")
    if _count_digits(text) > MAX_EXPANDED_DIGITS:
        raise NormalizeError(
            f"전개 자릿수가 {MAX_EXPANDED_DIGITS} 를 넘는다: {text}"
        )
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def normalize_number(raw: str) -> str:
    """십진 문자열을 정규 형태로 만든다.

    규칙 = `reader-rules.yaml#value_grammar.render.number_normalization`
    (천단위 `,` 제거 · 후행 0 제거 · 선행 `.` 보정 · 선행 `+` 제거 · 과학표기 전개 ·
    유니코드 숫자 ASCII 화).
    """
    if raw is None:
        raise NormalizeError("빈 입력")
    text = _to_ascii_digits(str(raw).strip())
    text = text.replace(",", "")
    if not text:
        raise NormalizeError("빈 입력")
    if not _rules().decimal_pattern.fullmatch(text):
        raise NormalizeError(f"십진 문법에 맞지 않는다: {raw!r}")
    try:
        value = _CONTEXT.create_decimal(text)
    except decimal.InvalidOperation as exc:  # pragma: no cover - 위 패턴이 먼저 막는다
        raise NormalizeError(f"십진 파싱 실패: {raw!r}") from exc
    return format_decimal(value)


def normalize_unit(unit: str | None) -> str | None:
    """단위를 소문자화하고 별칭 사전을 적용한다(l0: units)."""
    if unit is None:
        return None
    text = str(unit).strip()
    if not text:
        return None
    lowered = text.lower()
    return UNIT_ALIASES.get(lowered, lowered)


def match_key(value_normalized: str, unit: str | None) -> str:
    """`{value_normalized}|{unit or ''}` — l0-format §9 numeric.match_key 와 같은 키."""
    resolved = normalize_unit(unit)
    return f"{value_normalized}|{resolved or ''}"
