# -*- coding: utf-8 -*-
"""주석층 문법 파서 — `parse(text) -> Parsed`(SPEC §3.2 · 재정 2026-09-13 T64 ③).

**관대한 파싱 · 엄격한 린트.** 파서는 가능한 한 끝까지 읽고 위반을 `errors` 에 전부 모은다 — 첫
오류에서 멈추면 재시도 지시가 결함 하나씩만 실어 나르고, 그러면 세 번의 재시도 예산이 세 결함에
소진된다. 순수 함수이며 파일 I/O 가 없다.

위반 → L0 규칙 id 의 대응은 SPEC §3.2 「문법 위반 → L0 규칙 대응표」 그대로다.

| 위반 | rule |
|---|---|
| 프런트매터 여닫음·YAML 파싱·5키 정확히 | `annotation.schema` |
| 헤더 형식 · `slot` enum 밖 · `fig` 형식 · 번호 불연속 | `annotation.schema` |
| 태그 2개 이상 · 줄 중간 태그 · 태그 내부 공백 · 태그 앞 공백 · 트윗 내부 빈 줄 | `annotation.schema` |
| 태그 없는 문장 | `annotation.missing-tag` |

좌표(`locus`) = `frontmatter` · `T<n>` · `T<n>/S<i>`(i 는 그 트윗 안의 문장 순번 · 1부터).

★ 모듈 상수 두 개(`TAG_RE` · `HEADER_RE`)를 L0·strip 이 import 한다. `TAG_RE` 는 줄 끝의 태그 하나를
잡는 식이고(strip 4단계의 제거식 · SPEC §3.3), `HEADER_RE` 는 트윗 헤더식이다. `slot` enum 은 시트
`format-parameters.yaml#slot_enum` 이 정본이라 여기 리터럴로 두지 않는다 — 호출자가 `slot_enum` 으로
넘기고, 넘기지 않으면 enum 검사는 하지 않는다(파서는 시트를 읽지 않는다).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Sequence

import yaml

RULE_SCHEMA = "annotation.schema"
RULE_MISSING_TAG = "annotation.missing-tag"

FRONTMATTER_KEYS: tuple[str, ...] = ("run_id", "variant", "pen", "spec_version", "spec_digest")
FRONTMATTER_FENCE = "---"

#: 트윗 헤더 — `## T<n> {slot: <slot>, fig: <figspec>}`. 콤마 뒤 공백 1칸 고정(SPEC §3.2 「공백」 행).
HEADER_RE = re.compile(r"^## T(\d+) \{slot: ([a-z]+), fig: ([^}]+)\}$")
#: 줄 끝의 인용 태그 하나 — `[M<n>(,M<n>)*]` 또는 `[narrative]`(SPEC §3.2 「인용 태그」 문법 행 ·
#: strip 4단계의 제거식 §3.3). 태그 앞 공백 0 은 이 식이 아니라 파서의 별도 판정이다.
TAG_RE = re.compile(r"\[(M\d+(?:,M\d+)*|narrative)\]$")
#: 헤더처럼 보이는 줄(형식 오류 판정용 — 관대한 인식).
HEADER_LIKE_RE = re.compile(r"^## ")
#: `fig` 값 — `none` 또는 `fig-NN` 을 `+` 로 이은 것.
FIG_RE = re.compile(r"^(none|fig-\d{2}(?:\+fig-\d{2})*)$")
#: 본문에서 이스케이프되지 않은 대괄호 묶음 전부(태그 후보). `\[` 는 리터럴이므로 제외한다.
_BRACKET_GROUP_RE = re.compile(r"(?<!\\)\[([^\]]*)\]")
#: 태그 내용의 정확한 문법(공백 없음).
_TAG_BODY_RE = re.compile(r"^(M\d+(?:,M\d+)*|narrative)$")


@dataclass(frozen=True)
class ParseError:
    rule: str
    locus: str
    found: str
    expected: str
    message: str

    def as_dict(self) -> dict:
        return {
            "rule": self.rule,
            "locus": self.locus,
            "found": self.found,
            "expected": self.expected,
            "message": self.message,
        }


@dataclass(frozen=True)
class Sentence:
    i: int
    text_with_tag: str
    text: str
    citations: tuple[str, ...]
    narrative: bool
    tag_raw: str


@dataclass(frozen=True)
class Tweet:
    n: int
    slot: str
    figspec: str
    figures: tuple[str, ...]
    sentences: tuple[Sentence, ...]


@dataclass
class Parsed:
    frontmatter_raw: str
    frontmatter: dict
    tweets: list[Tweet] = field(default_factory=list)
    errors: list[ParseError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def sentence_count(self) -> int:
        return sum(len(tweet.sentences) for tweet in self.tweets)


def _split_frontmatter(text: str, errors: list[ParseError]) -> tuple[str, dict, int]:
    """`---` 사이 원문(바이트 그대로)·파싱된 매핑·본문 시작 줄 번호."""
    lines = text.split("\n")
    if not lines or lines[0] != FRONTMATTER_FENCE:
        errors.append(ParseError(RULE_SCHEMA, "frontmatter", lines[0][:40] if lines else "(빈 문서)",
                                 FRONTMATTER_FENCE, "첫 줄은 프런트매터 여는 울타리 `---` 다"))
        return "", {}, 0
    close = None
    for index in range(1, len(lines)):
        if lines[index] == FRONTMATTER_FENCE:
            close = index
            break
    if close is None:
        errors.append(ParseError(RULE_SCHEMA, "frontmatter", "(닫는 --- 없음)", FRONTMATTER_FENCE,
                                 "프런트매터를 닫는 울타리 `---` 가 있어야 한다"))
        return "\n".join(lines[1:]), {}, len(lines)
    raw = "\n".join(lines[1:close])
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        errors.append(ParseError(RULE_SCHEMA, "frontmatter", str(exc).split("\n")[0][:80], "유효한 YAML 매핑",
                                 "프런트매터 YAML 파싱에 실패했다"))
        return raw, {}, close + 1
    if not isinstance(loaded, dict):
        errors.append(ParseError(RULE_SCHEMA, "frontmatter", type(loaded).__name__, "매핑",
                                 "프런트매터 최상위는 매핑이다"))
        return raw, {}, close + 1
    keys = list(loaded.keys())
    if sorted(map(str, keys)) != sorted(FRONTMATTER_KEYS):
        errors.append(ParseError(RULE_SCHEMA, "frontmatter", ", ".join(map(str, keys)), ", ".join(FRONTMATTER_KEYS),
                                 "프런트매터 키는 5개 정확히다(초과·누락 둘 다 위반)"))
    return raw, loaded, close + 1


def _parse_sentence(line: str, locus: str, index: int, errors: list[ParseError]) -> Sentence:
    """문장 한 줄 — 태그 개수·위치·내부 공백·앞 공백을 본다. 위반이 있어도 문장을 돌려준다(관대)."""
    groups = list(_BRACKET_GROUP_RE.finditer(line))
    tag_like = [
        match for match in groups
        if _TAG_BODY_RE.match(match.group(1)) or _TAG_BODY_RE.match(re.sub(r"\s+", "", match.group(1)))
    ]
    if not tag_like:
        errors.append(ParseError(RULE_MISSING_TAG, locus, line[-40:], "줄 끝의 `[M<n>,...]` 또는 `[narrative]`",
                                 "문장마다 태그가 정확히 1개 있어야 한다 — 이 문장에는 없다"))
        return Sentence(index, line, line, (), False, "")
    if len(tag_like) > 1:
        errors.append(ParseError(RULE_SCHEMA, locus, str(len(tag_like)), "1",
                                 "문장 하나에 태그는 정확히 1개다"))
    match = tag_like[-1]
    tag_raw = match.group(0)
    body = match.group(1)
    if match.end() != len(line):
        errors.append(ParseError(RULE_SCHEMA, locus, line[match.start():match.start() + 24], "줄 끝의 태그",
                                 "태그는 문장 종결부호 뒤, 줄 끝 직전에 온다"))
    if not _TAG_BODY_RE.match(body):
        errors.append(ParseError(RULE_SCHEMA, locus, tag_raw, "[" + re.sub(r"\s+", "", body) + "]",
                                 "태그 안은 콤마만 — 공백 없이 `[M3,M7]` 로 적는다"))
    if match.start() > 0 and line[match.start() - 1].isspace():
        errors.append(ParseError(RULE_SCHEMA, locus, repr(line[max(0, match.start() - 8):match.start() + 4]),
                                 "종결부호 바로 뒤의 태그", "태그 앞 공백은 0개다 — 공백이 있으면 strip 이 역방향으로 재조립되지 않는다"))
    text = line[:match.start()].rstrip() if match.end() == len(line) else line
    normalized = re.sub(r"\s+", "", body)
    narrative = normalized == "narrative"
    citations = () if narrative else tuple(normalized.split(","))
    return Sentence(index, line, text, citations, narrative, tag_raw)


def parse(text: str, *, slot_enum: Sequence[str] | None = None) -> Parsed:
    """주석층 문서 전문 → `Parsed`. 오류를 전부 모은다(첫 오류에서 멈추지 않는다)."""
    errors: list[ParseError] = []
    frontmatter_raw, frontmatter, body_start = _split_frontmatter(text, errors)
    lines = text.split("\n")
    tweets: list[Tweet] = []

    current: dict | None = None          # {"n", "slot", "figspec", "figures", "sentences": []}
    expected_n = 1
    blank_pending = False                # 직전 줄이 빈 줄이었는가(트윗 안 빈 줄 판정)
    seen_header = False

    def close_current() -> None:
        nonlocal current
        if current is None:
            return
        tweets.append(Tweet(
            n=current["n"], slot=current["slot"], figspec=current["figspec"],
            figures=tuple(current["figures"]), sentences=tuple(current["sentences"]),
        ))
        current = None

    for line in lines[body_start:]:
        if line.strip() == "":
            blank_pending = True
            continue
        if HEADER_LIKE_RE.match(line):
            close_current()
            seen_header = True
            match = HEADER_RE.match(line)
            if match is None:
                errors.append(ParseError(RULE_SCHEMA, f"T{expected_n}", line[:60],
                                         "## T<n> {slot: <slot>, fig: <figspec>}",
                                         "헤더 형식 — 콤마 뒤 공백 1칸 · 중괄호 안 두 키 순서 고정"))
                current = {"n": expected_n, "slot": "", "figspec": "", "figures": [], "sentences": []}
                expected_n += 1
                blank_pending = False
                continue
            n = int(match.group(1))
            slot = match.group(2)
            figspec = match.group(3)
            locus = f"T{n}"
            if n != expected_n:
                errors.append(ParseError(RULE_SCHEMA, locus, f"T{n}", f"T{expected_n}",
                                         "트윗 번호는 1부터 이어지는 연속 정수다"))
            if slot_enum is not None and slot not in list(slot_enum):
                errors.append(ParseError(RULE_SCHEMA, locus, slot, ", ".join(slot_enum),
                                         "slot 은 시트 slot_enum 의 값이다"))
            if not FIG_RE.match(figspec):
                errors.append(ParseError(RULE_SCHEMA, locus, figspec, "none | fig-NN(+fig-NN)*",
                                         "fig 는 `fig-NN` 을 `+` 로 잇거나 `none` 이다"))
            figures = [] if figspec == "none" else figspec.split("+")
            current = {"n": n, "slot": slot, "figspec": figspec, "figures": figures, "sentences": []}
            expected_n = n + 1
            blank_pending = False
            continue
        # 문장 줄
        if current is None:
            locus = "T0" if not seen_header else f"T{expected_n - 1}"
            errors.append(ParseError(RULE_SCHEMA, locus, line[:40], "## T<n> 헤더 뒤의 문장",
                                     "문장은 트윗 헤더 아래에 온다"))
            current = {"n": 0, "slot": "", "figspec": "", "figures": [], "sentences": []}
        index = len(current["sentences"]) + 1
        locus = f"T{current['n']}/S{index}"
        if blank_pending and current["sentences"]:
            errors.append(ParseError(RULE_SCHEMA, locus, "(빈 줄)", "문장 줄 연속",
                                     "트윗 안에는 빈 줄이 없다 — 빈 줄 하나는 트윗 사이에만 온다"))
        blank_pending = False
        current["sentences"].append(_parse_sentence(line, locus, index, errors))
    close_current()

    return Parsed(frontmatter_raw=frontmatter_raw, frontmatter=frontmatter, tweets=tweets, errors=errors)


__all__ = [
    "FIG_RE",
    "FRONTMATTER_KEYS",
    "HEADER_RE",
    "Parsed",
    "ParseError",
    "RULE_MISSING_TAG",
    "RULE_SCHEMA",
    "Sentence",
    "TAG_RE",
    "Tweet",
    "parse",
]
