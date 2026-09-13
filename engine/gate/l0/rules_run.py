# -*- coding: utf-8 -*-
"""`run.publish-preconditions`(`stage: run-start` · 재정 N10) — 게시 런의 전제조건 3종을 `run-kinds.yaml#requirements` 로 대조.

판정 대상은 스레드가 아니라 **런 자체**다. `run_kind != publish` 이면 대상이 없다(`checked 0` → `vacuous: empty-target`
파생) — 부분·예행 런에서 이 행이 통과로 보이는 이유를 판정문이 스스로 말한다(재정 N5).

세 요건의 기계 판정.

| id | 판정 |
|---|---|
| `defense_layers` | `layers[]` 의 각 층이 gate 계약 `layers` 블록에서 `status: active` 로 선언되어 있다(선언이 없거나 inactive 면 미충족) |
| `figures_usage_rights_decision` | `run.yaml` 의 `run_yaml_key` 경로 값이 null 이 아니고 `docs/decisions/<ID>.md` 가 실재 |
| `template_freeze` | 계약이 기계 증거를 정의하지 않았다 — **총괄 가정**: `run.yaml#template_freeze` 가 참값이면 충족. 계약이 증거를 정하면 이 줄이 바뀐다 |
"""

from __future__ import annotations

import os

from reader.lib.report import CheckRow

from ...paths import run_kinds_contract
from .context import L0Context, RuleResult

RULE = "run.publish-preconditions"
PUBLISH = "publish"
LAYER_ALIASES = {"l1_veto": "l1", "speech_act_flag": "speech_act_flag", "instrument": "instrument", "final_eyes": "final_eyes"}
DECISIONS_DIR = ("docs", "decisions")


def _walk(meta: dict, dotted: str):
    cursor = meta
    for key in dotted.split("."):
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor


def publish_preconditions(ctx: L0Context) -> RuleResult:
    res = RuleResult(CheckRow(check_id=RULE, checked=0))
    run_kind = str(ctx.meta.get("run_kind", ""))
    res.row.extras["run_kind"] = run_kind
    if run_kind != PUBLISH:
        return res
    requirements = run_kinds_contract(ctx.repo).get("requirements") or []
    for requirement in requirements:
        rid = str(requirement.get("id", ""))
        res.row.checked += 1
        unmet: str | None = None
        if rid == "defense_layers":
            for layer in requirement.get("layers") or []:
                entry = ctx.inactive.get(LAYER_ALIASES.get(str(layer), str(layer))) or {}
                if str(entry.get("status", "inactive")) != "active":
                    unmet = f"{rid} unmet ({layer} inactive)"
                    break
        elif rid == "figures_usage_rights_decision":
            value = _walk(ctx.meta, str(requirement.get("run_yaml_key") or "figures.usage_rights_decision"))
            if not value:
                unmet = f"{rid} unmet (null)"
            else:
                name = str(value) if str(value).endswith(".md") else f"{value}.md"
                if not os.path.isfile(os.path.join(ctx.repo, *DECISIONS_DIR, name)):
                    unmet = f"{rid} unmet ({name} 부재)"
        elif rid == "template_freeze":
            if not ctx.meta.get("template_freeze"):
                unmet = f"{rid} unmet"
        else:
            unmet = f"{rid} unmet (판정식 없음)"
        if unmet:
            res.defect(RULE, None, None, "all publish preconditions met", unmet,
                       f"게시 런 전제조건 {rid} 를 충족한 뒤 런을 다시 시작하라(재정 N10 · run-kinds.yaml#requirements).")
    return res


__all__ = ["publish_preconditions"]
