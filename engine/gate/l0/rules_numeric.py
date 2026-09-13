# -*- coding: utf-8 -*-
"""`numeric.exhaustive` · `numeric.unreviewed-use` — 숫자 전수 대조(SPEC §4.4.1 · `l0-format.yaml` §9).

절차(§4.4.1 그대로):

    tokens  = tokenize(shipped_text)          # 출하본(strip 산출) 기준 · 토큰화 = numeric.tokenizers rank 순 · 소비
    keys    = { normalize(t) for t in tokens }
    answers = facts ∪ patent_number ∪ patent_dates ∪ whitelist
    unmatched = keys - answers → 토큰마다 defect (locus = annotation-index 문장)

★ 토큰화 정규식은 **로드**한다(`numeric.tokenizers[]` · 여기 리터럴 없음). 정규화 중 시트에 있는 것(천단위 ·
후행 0 · 유니코드 숫자 · 단위 소문자화 + 별칭 · MATCH_KEY)은 `reader.lib.normalize` 를 **재사용**한다(§8.4 M4 DoD —
별도 구현 금지). 시트에 없는 것(날짜 환산 · 통화 · 범위 분해 · 특허번호 정규화)만 `numeric.normalization` 문언대로
여기 구현한다. `match_policy: exact-only` — 근사·반올림 없음(D7).

`numeric.unreviewed-use`(veto: false · 재정 P-B)는 미참조(미검토) 수치의 첫 사용을 **플래그**한다. 미참조 목록은
`10-read/convergence.json` 이 아니라 **동결본에서 재계산**한다(총괄 재량 ⓓ — 그 파일은 gate 의 may_read 밖이고
`reader/lib/derivation.py#_numeric_inventory` 와 같은 규칙: 참조 = `implication`·`positioning` 항목의 `numeric_refs[]`
합집합 · 범위 = `reader-rules.yaml#numeric_harvest.answer_scope` · 미참조 = 범위 안 fact − 참조).

★ 총괄 재량 ⓖ 의 처분(재정 2026-09-13 T65 자잘 · 값 공간 승인): 화이트리스트 `pattern` 은 MATCH_KEY 에 fullmatch 한다
(§4.4.1). 구 토큰화 11종에는 스레드 순번 `n/N` 을 한 토큰으로 잡는 어형이 없어 `3/9` 가 bare-number 둘(`3|` · `9|`)로
쪼개졌고 어떤 순번 패턴도 그 키에 닿지 않았다. 재정 T65 가 `thread-marker`(rank 0 · `l0-format.yaml#numeric.tokenizers`)를
승인했다 — 정규화 = 값 문자열 그대로 · unit 없음 → MATCH_KEY `3/9|`. 그러므로 화이트리스트는 `^\\d{1,2}/\\d{1,2}\\|$`
형태로 적어야 닿는다(`|` 가 키의 일부다 · `engine/procedure/design.md` ⑻). 반례 골든 = `rc-0008`(알려진 과광화 —
`1/2 inch` 도 순번으로 잡힌다 · 어형을 좁히는 것은 재정 사항).
"""

from __future__ import annotations

import re
from typing import Iterable

from reader.lib.normalize import NormalizeError, match_key, normalize_number, normalize_unit
from reader.lib.report import CheckRow
from reader.lib.rules import Rules

from ...stages import StageError
from .context import L0Context, RuleResult

R_EXHAUSTIVE = "numeric.exhaustive"
R_UNREVIEWED = "numeric.unreviewed-use"

FACT_KIND = "fact"
ACTIVE = "active"
REFERRING_KINDS = ("implication", "positioning")
YEAR_UNIT = "year"

_MONTHS = {name: index for index, name in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), start=1)}
_RANGE_SPLIT = re.compile(r"^(\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*(\d+(?:\.\d+)?)\s*([A-Za-zµ%°]*)$")
_CURRENCY_SPLIT = re.compile(r"^\$\s?([\d,]*(?:\.\d+)?)(?:\s?([KMBT]))?$")
_VALUE_UNIT_SPLIT = re.compile(r"^(\d[\d,]*(?:\.\d+)?)\s*(.+)$")
_EN_DATE_SPLIT = re.compile(r"^([A-Za-z]+)\.?\s+(\d{1,2}),\s+(\d{4})$")


# ---------------------------------------------------------------------------
# 토큰화 — 계약에서 로드
# ---------------------------------------------------------------------------


def load_tokenizers(numeric_block: dict) -> list[tuple[int, str, re.Pattern[str]]]:
    rows = numeric_block.get("tokenizers") or []
    out: list[tuple[int, str, re.Pattern[str]]] = []
    for row in rows:
        try:
            out.append((int(row["rank"]), str(row["kind"]), re.compile(str(row["pattern"]))))
        except (KeyError, TypeError, re.error) as exc:
            raise StageError(f"numeric.tokenizers 항목이 불완전하다: {row!r} — {exc}") from exc
    if not out:
        raise StageError("numeric.tokenizers 가 비어 있다")
    return sorted(out, key=lambda item: item[0])


def tokenize(text: str, tokenizers: list[tuple[int, str, re.Pattern[str]]]) -> list[tuple[int, int, str, str]]:
    """rank 순으로 시도하고 매칭 구간은 소비한다. 반환 = `(start, end, kind, text)` 위치 정렬."""
    consumed: list[tuple[int, int]] = []
    tokens: list[tuple[int, int, str, str]] = []
    for _rank, kind, pattern in tokenizers:
        for match in pattern.finditer(text):
            start, end = match.span()
            if start == end or any(s < end and start < e for s, e in consumed):
                continue
            consumed.append((start, end))
            tokens.append((start, end, kind, match.group(0)))
    return sorted(tokens)


# ---------------------------------------------------------------------------
# 정규화 — 시트에 없는 것만 여기(문언 = numeric.normalization)
# ---------------------------------------------------------------------------


def normalize_patent_number(raw: str) -> str:
    """`patent_number: 공백·하이픈·슬래시 제거 + 대문자화`."""
    return re.sub(r"[\s\-/]", "", raw).upper()


def _en_date(raw: str) -> str | None:
    match = _EN_DATE_SPLIT.match(raw.strip())
    if not match:
        return None
    month = _MONTHS.get(match.group(1)[:3].lower())
    if month is None:
        return None
    return f"{int(match.group(3)):04d}-{month:02d}-{int(match.group(2)):02d}"


def _safe_number(raw: str) -> str:
    try:
        return normalize_number(raw)
    except NormalizeError:
        return raw.replace(",", "").strip()


def keys_of(kind: str, raw: str, aliases: dict) -> list[str]:
    """토큰 하나 → MATCH_KEY 목록(범위는 두 끝값 + 범위 키)."""
    text = raw.strip()
    if kind == "thread-marker":
        # `normalization.thread_marker`: 값 = 문자열 그대로(n/N) · unit 없음 → 'n/N|'.
        return [match_key(text, None)]
    if kind in ("patent-number-slash", "patent-number"):
        return [match_key(normalize_patent_number(text), None)]
    if kind == "iso-date":
        return [match_key(text, None)]
    if kind == "en-date":
        iso = _en_date(text)
        return [match_key(iso, None)] if iso else [match_key(text, None)]
    if kind == "currency":
        match = _CURRENCY_SPLIT.match(text)
        if match:
            value = _safe_number(match.group(1)) + (match.group(2) or "")
            return [match_key(value, aliases.get("$", "$"))]
        return [match_key(text, None)]
    if kind == "range":
        match = _RANGE_SPLIT.match(text)
        if match:
            unit = match.group(3) or None
            a, b = _safe_number(match.group(1)), _safe_number(match.group(2))
            return [match_key(a, unit), match_key(b, unit), match_key(f"{a}-{b}", unit)]
        return [match_key(text, None)]
    if kind == "percent":
        return [match_key(_safe_number(text.rstrip("%").strip()), "%")]
    if kind == "multiplier":
        return [match_key(_safe_number(text.rstrip("x×").strip()), "x")]
    if kind == "value-unit":
        match = _VALUE_UNIT_SPLIT.match(text)
        if match:
            return [match_key(_safe_number(match.group(1)), match.group(2).strip())]
        return [match_key(_safe_number(text), None)]
    if kind == "bare-year":
        return [match_key(text, YEAR_UNIT)]
    return [match_key(_safe_number(text), None)]


# ---------------------------------------------------------------------------
# 정답지
# ---------------------------------------------------------------------------


def _fact_keys(item: dict) -> set[str]:
    value = item.get("value_normalized")
    if value is None:
        return set()
    keys = {match_key(str(value), item.get("unit"))}
    kind = item.get("value_type")
    kind_name = kind.get("kind") if isinstance(kind, dict) else kind
    if kind_name == "identifier":
        keys.add(match_key(normalize_patent_number(str(value)), item.get("unit")))
    return keys


def answer_set(frozen: dict, whitelist: Iterable[dict]) -> tuple[set[str], list[re.Pattern[str]]]:
    """`answers = facts(active · 전 origin) ∪ patent.number ∪ patent.dates.* ∪ whitelist(fullmatch 패턴)`."""
    answers: set[str] = set()
    for item in frozen.get("items") or []:
        if isinstance(item, dict) and item.get("kind") == FACT_KIND and item.get("status") == ACTIVE:
            answers |= _fact_keys(item)
    patent = frozen.get("patent") or {}
    number = patent.get("number")
    if isinstance(number, str) and number:
        answers.add(match_key(normalize_patent_number(number), None))
    for value in (patent.get("dates") or {}).values():
        if isinstance(value, str) and value:
            answers.add(match_key(value, None))
    patterns: list[re.Pattern[str]] = []
    for row in whitelist:
        pattern = (row or {}).get("pattern") if isinstance(row, dict) else None
        if isinstance(pattern, str) and pattern:
            try:
                patterns.append(re.compile(pattern))
            except re.error as exc:
                raise StageError(f"run.yaml#numeric_whitelist 패턴이 정규식이 아니다: {pattern!r} — {exc}") from exc
    return answers, patterns


def _matches(key: str, answers: set[str], patterns: list[re.Pattern[str]]) -> bool:
    return key in answers or any(pattern.fullmatch(key) for pattern in patterns)


def _sentences(ctx: L0Context):
    if ctx.index is None:
        raise StageError("numeric.* 는 annotation-index 위에서만 돈다(locus 역참조)")
    for tweet in ctx.index["tweets"]:
        for sentence in tweet["sentences"]:
            yield int(tweet["n"]), int(sentence["i"]), str(sentence["text"])


def _scan(ctx: L0Context):
    numeric = ctx.law.block("numeric")
    tokenizers = load_tokenizers(numeric)
    aliases = dict((numeric.get("normalization") or {}).get("unit_aliases") or {})
    for tweet, sentence, text in _sentences(ctx):
        for _s, _e, kind, raw in tokenize(text, tokenizers):
            yield tweet, sentence, kind, raw, keys_of(kind, raw, aliases)


def exhaustive(ctx: L0Context) -> RuleResult:
    answers, patterns = answer_set(ctx.frozen, ctx.meta.get("numeric_whitelist") or [])
    res = RuleResult(CheckRow(check_id=R_EXHAUSTIVE, checked=0))
    res.row.extras["answers"] = len(answers)
    res.row.extras["whitelist_patterns"] = len(patterns)
    for tweet, sentence, kind, raw, keys in _scan(ctx):
        res.row.checked += 1
        if kind == "range":
            # 두 끝값 대조 + 범위 자체 키(재료가 범위를 한 항목으로 담은 경우) — 어느 쪽이든 정답지에 있으면 통과.
            ends_ok = all(_matches(k, answers, patterns) for k in keys[:2])
            if ends_ok or _matches(keys[2], answers, patterns):
                continue
            observed = " / ".join(keys)
        else:
            if all(_matches(k, answers, patterns) for k in keys):
                continue
            observed = " / ".join(keys)
        res.defect(R_EXHAUSTIVE, tweet, sentence, "numeric token in frozen fact set or run whitelist", observed,
                   f"T{tweet}/S{sentence} 의 수치({kind})를 동결본 fact 항목으로 재서술하라. 재료에 없는 값이면 문장에서 수치를 제거하라.")
    return res


# ---------------------------------------------------------------------------
# numeric.unreviewed-use — 미참조 목록의 재계산(총괄 재량 ⓓ)
# ---------------------------------------------------------------------------


def _material_order(item_id: str) -> tuple:
    digits = item_id[1:]
    return (0, int(digits)) if digits.isdigit() else (1, 0, item_id)


def unreferenced_facts(frozen: dict, rules: Rules | None = None) -> list[str]:
    """동결본에서 미참조 fact id 목록 — `derivation.py#_numeric_inventory` 와 같은 규칙(범위 = answer_scope)."""
    rules = rules or Rules.load()
    items = [item for item in frozen.get("items") or [] if isinstance(item, dict)]
    referenced: set[str] = set()
    for item in items:
        if item.get("kind") in REFERRING_KINDS:
            for ref in item.get("numeric_refs") or []:
                if isinstance(ref, str):
                    referenced.add(ref)
    scoped = [item["id"] for item in items if rules.in_answer_scope(item) and isinstance(item.get("id"), str)]
    return sorted({item_id for item_id in scoped if item_id not in referenced}, key=_material_order)


def unreviewed_use(ctx: L0Context) -> RuleResult:
    ids = unreferenced_facts(ctx.frozen)
    by_id = {item["id"]: item for item in ctx.frozen.get("items") or [] if isinstance(item, dict) and isinstance(item.get("id"), str)}
    unreviewed_keys: dict[str, str] = {}
    for item_id in ids:
        for key in _fact_keys(by_id[item_id]):
            unreviewed_keys.setdefault(key, item_id)
    answers, patterns = answer_set(ctx.frozen, ctx.meta.get("numeric_whitelist") or [])
    res = RuleResult(CheckRow(check_id=R_UNREVIEWED, checked=0))
    res.row.extras["unreferenced"] = ids
    seen: set[str] = set()
    for tweet, sentence, _kind, _raw, keys in _scan(ctx):
        res.row.checked += 1
        for key in keys:
            if key in seen or key not in unreviewed_keys or not _matches(key, answers, patterns):
                continue
            seen.add(key)
            res.flag(R_UNREVIEWED, tweet, sentence,
                     f"미검토 수치 사용 — T{tweet}/S{sentence} 의 {key} 는 {unreviewed_keys[key]} 이며 CP1 에서 어떤 함의·포지셔닝도 참조하지 않았다(재정 P-B). 판정자 = Owner(CP2).")
    res.row.extras["flagged_keys"] = sorted(seen)
    return res


__all__ = ["answer_set", "exhaustive", "keys_of", "load_tokenizers", "normalize_patent_number", "tokenize",
           "unreferenced_facts", "unreviewed_use"]
