# -*- coding: utf-8 -*-
"""L0 결정론 층 — 로더(`load_rules`) + 규칙 구현 사전.

`contracts/l0-format.yaml#rules[]` 가 규칙 목록의 정본이다. 로더는 그 목록을 읽어 규칙 객체를 만들며,

· `retired[]` 의 id 가 `rules[]` 에 있으면 `StageError`(폐지 규칙의 부활은 Owner 재정 사항).
· 구현 사전(`RULE_IMPLEMENTATIONS`)은 **계약 id 를 키로** 하고, 구현 없는 id 는 로드 시 `StageError`
  (계약이 모르는 검사도, 구현이 없는 선언도 결함이다).
· `veto` 는 **항목에서 읽는다** — 목록 위치에서 추정하지 않는다(l0-format §7 헤더 · `numeric.unreviewed-use` 만 false).
· 수치는 시트에서 온다(`L0Law.param`). 여기 리터럴 값이 없다.

판정 행은 규칙 하나당 행 하나다. ★ `ruleset` 3키는 **null** 이다 — 정본(`verdict-check-row.schema.json` 규율 (6) ·
SPEC §4.3 예시 · golden rc-0001 meta.json 의 기대 행)이 L0 규칙을 「목록을 소비하지 않는 검사」로 분류한다
(목록형 = 결함 카탈로그 · 화행 술어 · 점수 린트). 발주문 §3.3 의 `ruleset: "l0-format"` 문언과 어긋나는 자리이며
정본이 이긴다. 로드된 법의 신원(파일 version · 규칙 수)은 행의 `extras["ruleset"]` 에 남긴다(보고 밖 · 감사용).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from reader.lib.report import CheckRow

from ...stages import StageError
from . import rules_annotation, rules_citation, rules_format, rules_numeric, rules_run
from .context import L0Context, L0Law, RuleResult

RULESET = "l0-format"

RULE_IMPLEMENTATIONS: dict[str, Callable[[L0Context], RuleResult]] = {
    "run.publish-preconditions": rules_run.publish_preconditions,
    "format.tweet-count": rules_format.tweet_count,
    "format.slot-count": rules_format.slot_count,
    "format.body-length": rules_format.body_length,
    "format.stop-shape": rules_format.stop_shape,
    "format.hashtag-zero": rules_format.hashtag_zero,
    "format.no-link-in-body": rules_format.no_link_in_body,
    "format.images-per-post": rules_format.images_per_post,
    "annotation.schema": rules_annotation.schema,
    "annotation.missing-tag": rules_annotation.missing_tag,
    "citation.resolve": rules_citation.resolve,
    "numeric.exhaustive": rules_numeric.exhaustive,
    "numeric.unreviewed-use": rules_numeric.unreviewed_use,
}


@dataclass(frozen=True)
class Rule:
    id: str
    stage: str
    veto: bool
    basis: str
    params: tuple[str, ...]
    impl: Callable[[L0Context], RuleResult]

    def run(self, ctx: L0Context) -> RuleResult:
        return self.impl(ctx)


def load_rules_from_law(law: L0Law) -> list[Rule]:
    retired = {str(entry.get("id")) for entry in law.doc.get("retired") or [] if isinstance(entry, dict)}
    raw_rules = law.doc.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise StageError("l0-format.yaml#rules[] 가 비어 있다")
    rules: list[Rule] = []
    seen: set[str] = set()
    for entry in raw_rules:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise StageError(f"l0-format.yaml#rules[] 항목에 id 가 없다: {entry!r}")
        rule_id = entry["id"]
        if rule_id in retired:
            raise StageError(f"폐지된 규칙 {rule_id!r} 가 rules[] 에 있다 — 부활은 Owner 재정 사항이다(l0-format §10)")
        if rule_id in seen:
            raise StageError(f"규칙 id 중복: {rule_id!r}")
        seen.add(rule_id)
        if "veto" not in entry or not isinstance(entry["veto"], bool):
            raise StageError(f"규칙 {rule_id!r} 에 veto 가 없다 — 거부권은 항목이 정한다(목록 위치에서 추정하지 않는다)")
        impl = RULE_IMPLEMENTATIONS.get(rule_id)
        if impl is None:
            raise StageError(f"규칙 {rule_id!r} 의 구현이 없다 — 계약에만 있는 규칙을 로드하지 않는다")
        raw_params = entry.get("params")
        params = (raw_params,) if isinstance(raw_params, str) else tuple(raw_params or [])
        for pointer in params:
            law.param(pointer)            # 포인터가 시트에 실재하는지 로드 시점에 확인한다
        rules.append(Rule(id=rule_id, stage=str(entry.get("stage", "thread")), veto=bool(entry["veto"]),
                          basis=str(entry.get("basis", "")), params=params, impl=impl))
    return rules


def load_rules(repo: str) -> list[Rule]:
    return load_rules_from_law(L0Law.load(repo))


def stamp_ruleset(row: CheckRow, law: L0Law, size: int) -> CheckRow:
    """행에 법의 신원을 extras 로 남긴다 — 8키 서식의 ruleset 3키는 null 그대로(모듈 docstring)."""
    row.extras["ruleset"] = {"name": RULESET, "version": law.version, "size": size}
    return row


__all__ = ["RULESET", "RULE_IMPLEMENTATIONS", "L0Context", "L0Law", "Rule", "RuleResult", "load_rules",
           "load_rules_from_law", "stamp_ruleset"]
