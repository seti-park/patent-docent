# -*- coding: utf-8 -*-
"""strip — 주석본 → 출하 후보 텍스트(SPEC §3.3 · 결정론 변환 · 판단 없음).

단계는 고정이며 순서를 바꾸지 않는다.

| 단계 | 동작 |
|---|---|
| ① | 프런트매터(`---` … `---`) 제거 → `frontmatter_raw`(구분선 제외 · 원문 바이트 그대로 · 끝 개행 포함) |
| ② | `## T<n> {...}` 헤더 제거 → 트윗 구조 메타(`n` · `slot` · `figures`) |
| ③ | 줄 끝 인용 태그를 빈 문자열로(`STRIP_TAG_RE` = 파서의 `TAG_RE` — 여기서 다시 만들지 않는다) |
| ④ | `\\[` → `[` (이스케이프 복원) — ③ 뒤에 와야 한다(순서가 뒤집히면 복원된 `[` 가 태그로 오인된다) |
| ⑤ | 트윗 사이 빈 줄 정확히 1 · 그 외 원문 유지 · 끝 개행 1 |

출하본 = 트윗 텍스트(문장 줄을 `\\n` 으로 이은 것)를 `\\n\\n` 으로 이어붙인 것 + `\\n`.

★ `_reference_strip` 은 순방향 round-trip 검사(`strip.roundtrip-forward`)의 **오라클**이다 — 태그·헤더·
프런트매터만 제거하는 별도 최소 구현이며 주 구현과 코드를 공유하지 않는다(서로 부르지 않고 상수도
같이 쓰지 않는다). 오라클이 주 구현을 부르면 검사는 자기 자신과 비교하는 것이 된다. 그 안의 태그 정규식은
SPEC §3.3 코드블록 `STRIP_TAG_RE` 의 문언 그대로다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

from .parse import FRONTMATTER_FENCE, HEADER_RE, TAG_RE

#: ③ 의 제거식 = 파서 상수(유일한 파서 · 여기서 다시 만들지 않는다).
STRIP_TAG_RE = TAG_RE
#: §3.3 「출하 전 최종 안전망」 — strip 이후 이 패턴이 남아 있으면 안 된다(`strip.residual-tag`).
RESIDUAL_TAG_RE = re.compile(r"\[(M\d+|narrative)")
ESCAPED_BRACKET = "\\["
BRACKET = "["


class StripError(ValueError):
    """strip 이 전제(프런트매터 울타리 · 헤더 아래 문장)를 만족하지 않는 입력을 받았다."""


@dataclass
class StrippedTweet:
    n: int
    slot: str
    figspec: str
    figures: list[str]
    sentences_raw: list[str] = field(default_factory=list)   # ③ 뒤 · ④ 전
    sentences: list[str] = field(default_factory=list)       # ④ 뒤

    @property
    def text(self) -> str:
        return "\n".join(self.sentences)


@dataclass
class Stripped:
    frontmatter_raw: str
    frontmatter: dict
    tweets: list[StrippedTweet]
    stripped_md: str

    @property
    def meta(self) -> dict:
        return {"frontmatter_raw": self.frontmatter_raw, "frontmatter": self.frontmatter}


def strip(text: str) -> Stripped:
    """주석본 전문 → `Stripped`. 문법 위반본에는 부르지 않는다(파서 오류 0 이 전제 · SPEC §3.2 연쇄 오보 방지)."""
    lines = text.split("\n")
    # ① 프런트매터
    if not lines or lines[0] != FRONTMATTER_FENCE:
        raise StripError("첫 줄이 프런트매터 울타리가 아니다")
    close = None
    for index in range(1, len(lines)):
        if lines[index] == FRONTMATTER_FENCE:
            close = index
            break
    if close is None:
        raise StripError("프런트매터를 닫는 울타리가 없다")
    frontmatter_raw = "\n".join(lines[1:close]) + "\n"
    frontmatter = yaml.safe_load(frontmatter_raw)
    if not isinstance(frontmatter, dict):
        raise StripError("프런트매터가 매핑이 아니다")

    tweets: list[StrippedTweet] = []
    current: StrippedTweet | None = None
    for line in lines[close + 1:]:
        if line.strip() == "":
            continue                                     # ⑤ 빈 줄은 경계일 뿐 — 트윗 사이에 정확히 1 로 재생성
        header = HEADER_RE.match(line)
        if header:                                       # ② 헤더 → 구조 메타
            figspec = header.group(3)
            current = StrippedTweet(
                n=int(header.group(1)), slot=header.group(2), figspec=figspec,
                figures=[] if figspec == "none" else figspec.split("+"),
            )
            tweets.append(current)
            continue
        if current is None:
            raise StripError("헤더 앞에 문장이 있다")
        raw = STRIP_TAG_RE.sub("", line)                 # ③ 태그 제거
        current.sentences_raw.append(raw)
        current.sentences.append(raw.replace(ESCAPED_BRACKET, BRACKET))   # ④ 이스케이프 복원
    stripped_md = "\n\n".join(tweet.text for tweet in tweets) + "\n"      # ⑤
    return Stripped(frontmatter_raw=frontmatter_raw, frontmatter=frontmatter, tweets=tweets, stripped_md=stripped_md)


def _reference_strip(text: str) -> str:
    """순방향 오라클 — 프런트매터·헤더·태그만 지우고 나머지는 손대지 않는다(주 구현과 코드 공유 없음)."""
    body = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    body = re.sub(r"^## T[0-9]+ \{[^}\n]*\}\n", "", body, flags=re.M)
    body = re.sub(r"\[(M\d+(,M\d+)*|narrative)\]$", "", body, flags=re.M)
    body = body.replace("\\[", "[")
    body = re.sub(r"\n{2,}", "\n\n", body).strip("\n")
    return body + "\n"


__all__ = ["RESIDUAL_TAG_RE", "STRIP_TAG_RE", "StripError", "Stripped", "StrippedTweet", "strip", "_reference_strip"]
