# -*- coding: utf-8 -*-
"""`annotation.schema` · `annotation.missing-tag` — 파서 `errors` 를 규칙 id 로 접는다(SPEC §3.2 대응표).

파서(`engine/annotation/parse.py#parse`)가 유일한 판정자다 — 여기서 문법을 다시 보지 않는다. 더하는 것은
하나뿐: 프런트매터 `spec_digest` ≠ 현재 동결본 → `annotation.schema`(낡은 재료로 쓴 원고는 검사하지 않는다).
"""

from __future__ import annotations

import re

from reader.lib.report import CheckRow

from ...annotation.parse import RULE_MISSING_TAG, RULE_SCHEMA
from .context import L0Context, RuleResult

_LOCUS_RE = re.compile(r"^T(\d+)(?:/S(\d+))?$")


def locus_of(text: str) -> tuple[int | None, int | None]:
    """파서 좌표 문자열(`frontmatter` · `T<n>` · `T<n>/S<i>`) → `(tweet, sentence)`."""
    match = _LOCUS_RE.match(text or "")
    if not match:
        return None, None
    tweet = int(match.group(1)) or None
    sentence = int(match.group(2)) if match.group(2) else None
    return tweet, sentence


def _fold(ctx: L0Context, rule: str, fix: str) -> RuleResult:
    res = RuleResult(CheckRow(check_id=rule, checked=ctx.parsed.sentence_count))
    for error in ctx.parsed.errors:
        if error.rule != rule:
            continue
        tweet, sentence = locus_of(error.locus)
        res.defect(rule, tweet, sentence, error.expected, error.found, f"{error.locus} — {error.message}. {fix}")
    return res


def schema(ctx: L0Context) -> RuleResult:
    res = _fold(ctx, RULE_SCHEMA, "주석층 문법(SPEC §3.2)대로 고치라.")
    res.row.checked += 1                                  # 프런트매터 spec_digest 대조 1건
    found = str(ctx.parsed.frontmatter.get("spec_digest", "")) if isinstance(ctx.parsed.frontmatter, dict) else ""
    if found != ctx.spec_digest:
        res.defect(RULE_SCHEMA, None, None, ctx.spec_digest, found or "(없음)",
                   "프런트매터 spec_digest 가 현재 동결본과 다르다 — 현재 동결본 위에서 다시 쓰고 그 지문을 적으라(SPEC §3.2 · 재정 N11).")
    return res


def missing_tag(ctx: L0Context) -> RuleResult:
    return _fold(ctx, RULE_MISSING_TAG, "근거 재료 태그를 달거나, 서사 문장이면 [narrative] 로 신고하라.")


__all__ = ["locus_of", "missing_tag", "schema"]
