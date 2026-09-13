# -*- coding: utf-8 -*-
"""`citation.resolve` — 태그의 M id 가 동결본 `items[]` 에 존재하고 `status != retracted`(D6 규율 ① · D8).

`superseded` 인용은 결함이 아니라 플래그다(SPEC §4.8 [ENG-확정] E3 · `origin: advisory-rule`) — 낡은 것이지
거짓이 아니므로 거부권을 넓히지 않고 가시성만 얻는다(D7).
"""

from __future__ import annotations

from reader.lib.report import CheckRow

from .context import L0Context, RuleResult

RULE = "citation.resolve"
RETRACTED = "retracted"
SUPERSEDED = "superseded"


def resolve(ctx: L0Context) -> RuleResult:
    statuses: dict[str, str] = {}
    for item in ctx.frozen.get("items") or []:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            statuses[item["id"]] = str(item.get("status", ""))
    res = RuleResult(CheckRow(check_id=RULE, checked=0))
    for tweet in ctx.parsed.tweets:
        for sentence in tweet.sentences:
            for material in sentence.citations:
                res.row.checked += 1
                status = statuses.get(material)
                if status is None:
                    res.defect(RULE, tweet.n, sentence.i, "material id present in frozen items[]", f"{material} (absent)",
                               f"T{tweet.n}/S{sentence.i} 가 인용한 {material} 은 동결본에 없다. 실재하는 active 항목으로 재서술하라.")
                elif status == RETRACTED:
                    res.defect(RULE, tweet.n, sentence.i, "active material id", f"{material} ({status})",
                               f"T{tweet.n}/S{sentence.i} 가 인용한 {material} 은 {status} 다. 다른 active 항목으로 재서술하라.")
                elif status == SUPERSEDED:
                    res.flag(RULE, tweet.n, sentence.i,
                             f"T{tweet.n}/S{sentence.i} 가 인용한 {material} 은 superseded 다 — 낡은 것이지 거짓은 아니다(E3). 승계 항목이 있는지 Owner 가 본다.")
    return res


__all__ = ["resolve"]
