# -*- coding: utf-8 -*-
"""`read.coverage` — 전 구성요소 접지(D5 ③ · 재정 R3) + 1:1 + 역참조 일치.

필수 대상 = **독립항 element 전량(재귀) + 종속항 `additions[]` 전량**. 구 스펙의 "종속항
접지는 권고" 완화와 `coverage.advisory` 키는 전면 삭제되었다(재정 R3).

세 규칙이 함께 있어야 이 검사가 무언가를 반증한다(재감수 B-02).
  ① 각 element·addition 의 `material_id`(component 항목)를 `grounding.component` 로
     참조하는 항목이 1개 이상 있다.
  ② `material_id` 는 **1:1** 이다 — 두 element 가 같은 component 항목을 공유하면 접지
     1건이 둘을 덮는다.
  ③ `component.claim_ref` 가 자기를 가리킨 element·addition 의 id 와 **역방향으로 일치**한다.

접지 예외 2종(`no-anchor-found`·`not-depicted`)은 미접지가 아니라 **신고된 상태**이며,
`extras["grounding_exceptions"]` 로 수집되어 CP1 표면에 전량 노출된다. 감춰진 예외는
예외가 아니라 은폐다.
"""

from __future__ import annotations

from .report import CheckContext, CheckRow
from .spec_io import SpecIndex

CHECK_ID = "read.coverage"


def check(ctx: CheckContext) -> CheckRow:
    row = CheckRow(check_id=CHECK_ID)
    index = SpecIndex.build(ctx.spec)

    # component 항목 id → 그 항목을 접지하는 active grounding 항목들
    grounded: dict[str, list[str]] = {}
    exceptions: list[dict] = []
    for item_id, item in index.items.items():
        if item.get("kind") != "grounding":
            continue
        component = item.get("component")
        if isinstance(component, str) and item.get("status") == "active":
            grounded.setdefault(component, []).append(item_id)
        anchor = item.get("anchor_state") or {}
        if anchor.get("spec") == "no-anchor-found" or anchor.get("figure") == "not-depicted":
            exceptions.append(
                {
                    "material_id": item_id,
                    "component": component,
                    "spec": anchor.get("spec"),
                    "figure": anchor.get("figure"),
                    "search_note": item.get("search_note"),
                }
            )

    targets: list[tuple[str, dict]] = []
    targets.extend(index.elements.items())
    targets.extend(index.additions.items())

    owners: dict[str, list[str]] = {}
    for target_id, target in targets:
        material_id = target.get("material_id")
        if isinstance(material_id, str):
            owners.setdefault(material_id, []).append(target_id)

    for target_id, target in targets:
        material_id = target.get("material_id")
        if not isinstance(material_id, str):
            continue
        # ① 접지
        if not grounded.get(material_id):
            row.add(
                "coverage.grounded",
                target_id,
                f"{material_id} 를 접지하는 grounding 0건",
                "grounding 1건 이상",
                "구성요소가 접지되지 않았다(D5 ③ 전 구성요소 3중 접지)",
            )
        # ③ 역참조 일치
        component_item = index.items.get(material_id)
        if component_item is not None and component_item.get("kind") == "component":
            claim_ref = component_item.get("claim_ref")
            if claim_ref != target_id:
                row.add(
                    "coverage.claim-ref-reverse",
                    f"{material_id}.claim_ref",
                    str(claim_ref),
                    target_id,
                    "component 의 claim_ref 가 자기를 가리킨 element·addition 과 어긋난다",
                )

    # ④ 고아 component — 커버리지는 **청구항 쪽에서 세므로**, 청구항이 통째로 빠지면 셀
    #    대상도 함께 빠져 통과한다(재감수 M-07 의 논지가 재현되는 자리). 인벤토리 검사가 주
    #    방어이고, 그 뒤에 남는 잔여가 어느 element·addition 도 가리키지 않는 성분 항목이다.
    #    물러난 항목(retracted·superseded)은 대상이 아니다 — 개정으로 남은 자취를 고아로
    #    잡으면 append-only 규율과 충돌한다.
    orphan_candidates = [
        item
        for item in index.items.values()
        if item.get("kind") == "component" and item.get("status") == "active"
    ]
    for component_item in orphan_candidates:
        component_id = component_item.get("id")
        if component_id not in owners:
            row.add(
                "coverage.no-orphan-component",
                str(component_id),
                f"claim_ref={component_item.get('claim_ref')} (지목한 element·addition 없음)",
                "element 또는 addition 1건이 material_id 로 지목",
                "어느 구성요소도 가리키지 않는 성분 항목이다 — 청구항이 명세에서 통째로 "
                "빠졌을 때 남는 흔적이다",
            )

    # ② 1:1
    for material_id, holders in sorted(owners.items()):
        if len(holders) > 1:
            row.add(
                "coverage.material-id-unique",
                material_id,
                ", ".join(sorted(holders)),
                "element·addition 1건",
                "두 구성요소가 같은 component 항목을 공유한다 — 접지 1건이 둘을 덮는다",
            )

    # 검사 대상 = 접지 대상(element·addition) + 고아 판정 대상(active component).
    # 후자를 빼면 element 가 0 건인 인스턴스에서 고아 결함이 나와도 행이 "대상 0건"으로 보인다.
    row.checked = len(targets) + len(orphan_candidates)
    row.extras["grounding_exceptions"] = exceptions
    row.extras["required"] = len(targets)
    row.extras["grounded"] = sum(
        1
        for target_id, target in targets
        if grounded.get(target.get("material_id") or "")
    )
    return row
