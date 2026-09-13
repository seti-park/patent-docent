# -*- coding: utf-8 -*-
"""X 가중 글자 수 — 시트 `format-parameters.yaml#weighted_length`(twitter-text v3 구성)의 구현.

    weighted = sum(weight) / scale

· `ranges` 안의 코드포인트는 그 행의 `weight`, 밖은 `default_weight`(CJK 등).
· URL 구간은 매칭 구간 전체를 `transformed_url_length * scale` 로 치환한다.
· 이모지 그래핌 클러스터는 클러스터 전체가 `default_weight` 1회다.

★ 값(scale · default_weight · ranges · transformed_url_length)은 전부 시트에서 온다 — 여기 리터럴이 없다.
★ URL 어형은 시트에 없어 러너의 최소 어형(총괄 재량 ⓒ · `engine/stages/gate.py#URL_RE`)을 호출자가 넘긴다.

**[가설] 이모지 그래핌 클러스터는 표준 라이브러리 근사다.** twitter-text 는 Unicode emoji 정규식 전체를
쓰지만 이 리포는 새 의존성을 들이지 않는다(제약). 근사 규칙 = `unicodedata` 범주 `So`(기타 기호) 또는
이모지 블록(U+1F000~U+1FAFF · 지역 표시자 U+1F1E6~U+1F1FF)을 기저로 보고, 뒤따르는 변이 선택자(U+FE0F) ·
키캡(U+20E3) · 피부색 수정자(U+1F3FB~U+1F3FF) · 태그(U+E0020~U+E007F) · ZWJ(U+200D)+다음 기저를 같은
클러스터로 접는다. 지역 표시자는 둘씩 짝짓는다. 이 근사가 twitter-text 와 갈리는 자리(예: `So` 밖의
텍스트 표현 기호 · 미등재 ZWJ 시퀀스)는 verdict.json#advisory_measurements.note 에 `[가설]` 로 적힌다.
"""

from __future__ import annotations

import unicodedata
from typing import Pattern

from ...stages import StageError

EMOJI_APPROXIMATION_NOTE = (
    "[가설] weighted_char_counts 의 이모지 그래핌 클러스터는 표준 라이브러리 근사다"
    "(unicodedata 범주 So + 이모지 블록 · ZWJ·VS16·키캡·피부색·태그 결합 · 지역 표시자 쌍). "
    "twitter-text 의 정규식 전체와 갈릴 수 있다 — engine/gate/l0/weighted_length.py"
)

_VS16 = 0xFE0F
_ZWJ = 0x200D
_KEYCAP = 0x20E3
_SKIN = (0x1F3FB, 0x1F3FF)
_TAG = (0xE0020, 0xE007F)
_REGIONAL = (0x1F1E6, 0x1F1FF)
_EMOJI_BLOCK = (0x1F000, 0x1FAFF)


def _is_emoji_base(char: str) -> bool:
    code = ord(char)
    if _EMOJI_BLOCK[0] <= code <= _EMOJI_BLOCK[1]:
        return True
    return unicodedata.category(char) == "So"


def _in(code: int, span: tuple[int, int]) -> bool:
    return span[0] <= code <= span[1]


def emoji_clusters(text: str) -> list[tuple[int, int]]:
    """이모지 그래핌 클러스터의 `(start, end)` 구간 목록(근사 — 모듈 docstring)."""
    spans: list[tuple[int, int]] = []
    i = 0
    n = len(text)
    while i < n:
        if not _is_emoji_base(text[i]):
            i += 1
            continue
        start = i
        i += 1
        if _in(ord(text[start]), _REGIONAL) and i < n and _in(ord(text[i]), _REGIONAL):
            i += 1
        while i < n:
            code = ord(text[i])
            if code == _VS16 or code == _KEYCAP or _in(code, _SKIN) or _in(code, _TAG):
                i += 1
                continue
            if code == _ZWJ and i + 1 < n and _is_emoji_base(text[i + 1]):
                i += 2
                continue
            break
        spans.append((start, i))
    return spans


def _weight_of(code: int, ranges: list[dict], default_weight: int) -> int:
    for row in ranges:
        if int(row["start"]) <= code <= int(row["end"]):
            return int(row["weight"])
    return default_weight


def weighted_length(text: str, config: dict, url_re: Pattern[str] | None) -> int:
    """`config` = 시트 `weighted_length.value`. 반환은 정수(가중 합 / scale · 내림 없이 정확히 나눠떨어진다)."""
    try:
        scale = int(config["scale"])
        default_weight = int(config["default_weight"])
        ranges = list(config["ranges"])
        url_length = int(config["transformed_url_length"])
        emoji_enabled = bool(config.get("emoji_parsing_enabled", True))
    except (KeyError, TypeError, ValueError) as exc:
        raise StageError(f"시트 weighted_length 구성이 불완전하다: {exc}") from exc

    # 구간 치환표: (start, end, weight_total)
    replaced: list[tuple[int, int, int]] = []
    if url_re is not None:
        for match in url_re.finditer(text):
            replaced.append((match.start(), match.end(), url_length * scale))
    if emoji_enabled:
        for start, end in emoji_clusters(text):
            if any(s <= start < e for s, e, _ in replaced):
                continue
            replaced.append((start, end, default_weight))
    replaced.sort()

    total = 0
    cursor = 0
    for start, end, weight in replaced:
        for char in text[cursor:start]:
            total += _weight_of(ord(char), ranges, default_weight)
        total += weight
        cursor = end
    for char in text[cursor:]:
        total += _weight_of(ord(char), ranges, default_weight)
    return total // scale if total % scale == 0 else (total + scale - 1) // scale


__all__ = ["EMOJI_APPROXIMATION_NOTE", "emoji_clusters", "weighted_length"]
