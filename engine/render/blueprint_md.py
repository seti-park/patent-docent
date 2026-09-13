# -*- coding: utf-8 -*-
"""`blueprint.json` → `blueprint.md`(KR 틀 · EN 값) — 결정론 렌더.

값을 요약·의역하지 않는다. 동결본에서 항목의 EN 라벨(`label_en` · `statement_en` ·
`what_it_shows_en` · `background_problem`)을 찾아 ID 옆에 그대로 싣는다. 같은 입력이면 같은
바이트가 나온다(시각을 싣지 않는다).
"""

from __future__ import annotations

# 항목 kind 별 대표 EN 문자열 필드(첫 번째로 있는 것을 쓴다).
_LABEL_FIELDS = ("label_en", "statement_en", "what_it_shows_en", "background_problem")

_ROW_KEYS = (
    "check_id",
    "ruleset",
    "ruleset_version",
    "ruleset_size",
    "checked",
    "violations",
    "status",
    "vacuous",
)


def _cell(value) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _item_index(frozen: dict) -> dict[str, dict]:
    return {str(item.get("id")): item for item in frozen.get("items") or [] if isinstance(item, dict)}


def _label(item: dict | None) -> str:
    if not item:
        return "(동결본에 없음)"
    for field in _LABEL_FIELDS:
        value = item.get(field)
        if isinstance(value, str) and value:
            return value
    return ""


def _ids_with_labels(ids: list, index: dict[str, dict]) -> str:
    parts = []
    for material_id in ids or []:
        item = index.get(str(material_id))
        parts.append(f"`{material_id}` {_cell(_label(item))}".rstrip())
    return "<br>".join(parts)


def render(blueprint: dict, frozen: dict, rows: list[dict], *, notes: list[str]) -> str:
    """KR 틀 + EN 값. `rows` = verdict-check-row/v0 8키 행 목록. `notes` = 미가동·부재 표지."""
    index = _item_index(frozen)
    lines: list[str] = []
    lines.append(f"# 블루프린트 — `{blueprint.get('run_id')}`")
    lines.append("")
    lines.append("## 1. 표지")
    lines.append("")
    lines.append("| 항목 | 값 |")
    lines.append("|---|---|")
    lines.append(f"| run_id | `{_cell(blueprint.get('run_id'))}` |")
    lines.append(f"| spec_version | `{_cell(blueprint.get('spec_version'))}` |")
    lines.append(f"| spec_digest | `{_cell(blueprint.get('spec_digest'))}` |")
    lane = blueprint.get("lane") or {}
    lines.append(
        f"| lane | model `{_cell(lane.get('model'))}` · effort `{_cell(lane.get('effort'))}` · "
        f"lane_id `{_cell(lane.get('lane_id'))}` |"
    )
    lines.append(f"| law_commit | `{_cell(blueprint.get('law_commit'))}` |")
    lines.append("")

    hook = blueprint.get("hook") or {}
    lines.append("## 2. 훅")
    lines.append("")
    lines.append("| 항목 | 값 |")
    lines.append("|---|---|")
    lines.append(f"| question_en | {_cell(hook.get('question_en'))} |")
    lines.append(f"| figure | `{_cell(hook.get('figure'))}` |")
    lines.append(f"| thesis_en | {_cell(hook.get('thesis_en'))} |")
    lines.append(f"| rationale_kr | {_cell(hook.get('rationale_kr'))} |")
    lines.append("")

    lines.append("## 3. 슬롯")
    lines.append("")
    lines.append("| 트윗 | slot | 전시 재료(ID · EN 값) | figures | point_en |")
    lines.append("|---|---|---|---|---|")
    for slot in blueprint.get("slots") or []:
        exhibit = slot.get("exhibit") or {}
        figures = ", ".join(f"`{fig}`" for fig in slot.get("figures") or [])
        lines.append(
            f"| T{_cell(slot.get('n'))} | `{_cell(slot.get('slot'))}` | "
            f"{_ids_with_labels(exhibit.get('material_ids') or [], index)} | {figures} | "
            f"{_cell(exhibit.get('point_en'))} |"
        )
    lines.append("")

    lines.append("## 4. 전달 표적")
    lines.append("")
    lines.append("| ID | kind | EN 값 |")
    lines.append("|---|---|---|")
    for target in blueprint.get("transmission_targets") or []:
        item = index.get(str(target))
        lines.append(
            f"| `{_cell(target)}` | `{_cell((item or {}).get('kind'))}` | {_cell(_label(item))} |"
        )
    lines.append("")

    lines.append("## 5. 도면 계획")
    lines.append("")
    lines.append("| 트윗 | figures | intent_kr |")
    lines.append("|---|---|---|")
    for plan in blueprint.get("figure_plan") or []:
        figures = ", ".join(f"`{fig}`" for fig in plan.get("figures") or [])
        lines.append(f"| T{_cell(plan.get('tweet'))} | {figures} | {_cell(plan.get('intent_kr'))} |")
    lines.append("")

    lines.append("## 6. 용어 메모 (작업 메모 · 게이트 무관 · 재정 N2)")
    lines.append("")
    terms = blueprint.get("new_terms") or []
    if terms:
        lines.append("| term_en | 트윗 | gloss_en |")
        lines.append("|---|---|---|")
        for term in terms:
            lines.append(
                f"| {_cell(term.get('term_en'))} | T{_cell(term.get('tweet'))} | {_cell(term.get('gloss_en'))} |"
            )
    else:
        lines.append("(없음)")
    lines.append("")

    lines.append("## 7. 허용 수치 제안 (run.yaml#numeric_whitelist 추기 · added_by run-discretion)")
    lines.append("")
    whitelist = blueprint.get("numeric_whitelist") or []
    if whitelist:
        lines.append("| pattern | rationale |")
        lines.append("|---|---|")
        for entry in whitelist:
            lines.append(f"| `{_cell(entry.get('pattern'))}` | {_cell(entry.get('rationale'))} |")
    else:
        lines.append("(없음)")
    lines.append("")

    lines.append("## 8. 판정 행 (verdict-check-row/v0)")
    lines.append("")
    lines.append("| " + " | ".join(_ROW_KEYS) + " |")
    lines.append("|" + "---|" * len(_ROW_KEYS))
    for row in rows:
        lines.append("| " + " | ".join(_cell(row.get(key)) for key in _ROW_KEYS) + " |")
    lines.append("")

    lines.append("## 9. 미가동·부재")
    lines.append("")
    for note in notes:
        lines.append(f"- {note}")
    if not notes:
        lines.append("(없음)")
    lines.append("")
    return "\n".join(lines)
