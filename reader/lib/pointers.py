# -*- coding: utf-8 -*-
"""`read.pointer-resolve` — 참조 무결성 + kind 제약 + 자기참조 금지 + 비순환.

반증 대상 = 존재하지 않는 대상을 참조하는 유령 링크와 오타 ID(SPEC §2.6 검사 2).
kind 제약 표는 §2.6 의 것이고, 자기참조·비순환은 재정 N9 와 스키마 `$comment` (8) 이다 —
스키마는 참조를 해소하지 못하므로 이 셋은 전량 검증기 몫이다.

★ `superseded_by` 의 kind 제약은 **동일 kind 까지**다. 구 규칙("동일 kind + status active")은
2차 승계 A→B→C 에서 A 의 링크를 고치게 만들어 동결본을 변조하는 경로였고,
`reader-rules.yaml#item_lifecycle.supersession_chain` 이 그것을 폐기했다. 사슬의 종단이
`active` 인지는 `freeze.payload-immutable` 이 사슬 추적으로 본다.
"""

from __future__ import annotations

from .report import CheckContext, CheckRow
from .spec_io import SpecIndex

CHECK_ID = "read.pointer-resolve"

# 참조 그래프의 간선을 만드는 필드(스키마 $comment (8) 의 비순환 대상).
# `numeric_refs[]` 는 재정 P-B 로 신설된 역참조다 — 함의·포지셔닝이 근거로 삼은 수치를
# 가리키며, 대상 kind 제약은 `fact` 다. 자기참조·비순환 규율은 다른 간선과 같다.
GRAPH_FIELDS = (
    "derivation.inputs[].ref",
    "derived_from[]",
    "numeric_refs[]",
    "superseded_by",
    "grounding.component",
)


def check(ctx: CheckContext) -> CheckRow:
    row = CheckRow(check_id=CHECK_ID)
    index = SpecIndex.build(ctx.spec)
    spec = ctx.spec
    checked = 0
    edges: dict[str, list[tuple[str, str]]] = {}

    # ★ 불변식 I5(SPEC §2.2) — `items[].id` 는 인스턴스 안에서 유일하다.
    #
    # 스펙은 위반 시 "스키마 검증 실패"라고 적었으나 **JSON Schema 는 이것을 표현하지
    # 못한다**(`uniqueItems` 는 원소 전체의 동일성만 보므로, 같은 id 에 다른 내용을 담은
    # 두 항목은 서로 다른 원소여서 통과한다). 그 결과 I5 는 선언만 있고 집행자가 없었다.
    #
    # 위험은 조용하다: 두 레인이 같은 `M<n>` 을 쓰면 조립이 그대로 이어 붙이고,
    # `SpecIndex` 와 동결 검사의 dict 인덱싱이 **뒤엣것으로 덮어써** 항목 하나가 소리 없이
    # 사라진다. 결번이 아니므로 ID 연속성 검사도 보지 못한다. 인용 `[M7]` 이 가리키는
    # 대상이 조용히 바뀌는 것은 append-only 규율이 막으려던 실패의 원형 그 자체다(§2.4).
    # 2026-08-18 실특허 스모크에서 레인이 이 경로를 지적했고 총괄이 재현했다.
    raw_items = spec.get("items")
    if isinstance(raw_items, list):
        seen_ids: set[str] = set()
        for position, item in enumerate(raw_items):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str):
                continue
            checked += 1
            if item_id in seen_ids:
                row.add(
                    "pointer.item-id-unique",
                    f"items[{position}].id",
                    item_id,
                    "인스턴스 안에서 유일한 항목 ID",
                    "같은 항목 ID 가 두 번 등재되었다 — 인덱싱이 뒤엣것으로 덮어써 "
                    "항목 하나가 조용히 사라진다(불변식 I5)",
                )
            seen_ids.add(item_id)

    def resolve_item(locus: str, ref, kind: str | None, owner: str | None = None) -> None:
        """항목 참조 1건을 해소한다. `kind` 가 None 이면 kind 제약 없음."""
        nonlocal checked
        checked += 1
        target = index.items.get(ref)
        if target is None:
            row.add(
                "pointer.resolve",
                locus,
                str(ref),
                "items[].id 로 해소",
                "존재하지 않는 항목을 참조한다(유령 링크·오타 ID)",
            )
            return
        if kind is not None and target.get("kind") != kind:
            row.add(
                "pointer.kind",
                locus,
                f"{ref} (kind={target.get('kind')})",
                f"kind={kind}",
                "참조 대상의 kind 가 제약과 다르다(§2.6 검사 2 kind 제약 표)",
            )
        if owner is not None and ref == owner:
            row.add(
                "pointer.no-self-reference",
                locus,
                str(ref),
                f"{owner} 이외의 항목",
                "자기 자신을 참조한다(재정 N9 · 스키마 $comment (8))",
            )

    def resolve_numeric_refs(item_id: str, item: dict) -> None:
        """`numeric_refs[]` — 함의·포지셔닝이 근거로 삼은 수치의 역참조(재정 P-B).

        kind 제약은 **`fact`** 다. 이 참조가 해소되지 않으면 중요분 도출식 자체가 무의미해진다
        — 수확은 전수이고 고르는 일 전체가 이 역참조 하나에 걸려 있기 때문이다.
        """
        for position, ref in enumerate(item.get("numeric_refs") or []):
            locus = f"{item_id}.numeric_refs[{position}]"
            resolve_item(locus, ref, "fact", owner=item_id)
            if isinstance(ref, str):
                edges.setdefault(item_id, []).append((ref, "numeric_refs[]"))

    def resolve_structural(locus: str, ref, table: dict, expected: str) -> None:
        nonlocal checked
        checked += 1
        if ref not in table:
            row.add(
                "pointer.resolve",
                locus,
                str(ref),
                expected,
                "존재하지 않는 구조 ID 를 참조한다",
            )

    # -- 청구항 트리 --------------------------------------------------------
    for element_id, element in index.elements.items():
        resolve_item(f"{element_id}.material_id", element.get("material_id"), "component")
    for addition_id, addition in index.additions.items():
        resolve_item(f"{addition_id}.material_id", addition.get("material_id"), "component")
        resolve_structural(
            f"{addition_id}.attaches_to",
            addition.get("attaches_to"),
            index.elements,
            "element id",
        )
    for claim in index.dependents:
        claim_id = claim.get("id", "?")
        for position, target in enumerate(claim.get("depends_on") or []):
            resolve_structural(
                f"{claim_id}.depends_on[{position}]", target, index.claims, "claims 의 청구항 id"
            )

    claims = spec.get("claims") or {}
    for position, interest in enumerate(claims.get("applicant_interest") or []):
        locus = f"claims.applicant_interest[{position}]"
        resolve_item(f"{locus}.material_id", interest.get("material_id"), "implication")
        resolve_structural(
            f"{locus}.claim", interest.get("claim"), index.claims, "claims 의 청구항 id"
        )

    # -- 항목 ---------------------------------------------------------------
    for item_id, item in index.items.items():
        kind = item.get("kind")
        superseded_by = item.get("superseded_by")
        if superseded_by is not None:
            resolve_item(f"{item_id}.superseded_by", superseded_by, kind, owner=item_id)
            edges.setdefault(item_id, []).append((superseded_by, "superseded_by"))
        if kind == "component":
            resolve_structural(
                f"{item_id}.claim_ref",
                item.get("claim_ref"),
                {**index.elements, **index.additions},
                "element id 또는 addition id",
            )
        elif kind == "grounding":
            component = item.get("component")
            resolve_item(f"{item_id}.component", component, "component", owner=item_id)
            if isinstance(component, str):
                edges.setdefault(item_id, []).append((component, "grounding.component"))
            for position, ref in enumerate(item.get("figure_refs") or []):
                resolve_structural(
                    f"{item_id}.figure_refs[{position}].figure",
                    ref.get("figure"),
                    index.figures,
                    "figures[].id",
                )
        elif kind == "fact":
            derivation = item.get("derivation") or {}
            for position, entry in enumerate(derivation.get("inputs") or []):
                if "ref" in entry:
                    locus = f"{item_id}.derivation.inputs[{position}].ref"
                    resolve_item(locus, entry.get("ref"), "fact", owner=item_id)
                    if isinstance(entry.get("ref"), str):
                        edges.setdefault(item_id, []).append(
                            (entry["ref"], "derivation.inputs[].ref")
                        )
            figure_source = item.get("figure_source") or {}
            if figure_source:
                resolve_structural(
                    f"{item_id}.figure_source.figure",
                    figure_source.get("figure"),
                    index.figures,
                    "figures[].id",
                )
        elif kind == "implication":
            for position, ref in enumerate(item.get("derived_from") or []):
                locus = f"{item_id}.derived_from[{position}]"
                resolve_item(locus, ref, None, owner=item_id)
                if isinstance(ref, str):
                    edges.setdefault(item_id, []).append((ref, "derived_from[]"))
            resolve_numeric_refs(item_id, item)
        elif kind == "positioning":
            resolve_numeric_refs(item_id, item)
        elif kind == "figure_note":
            resolve_structural(
                f"{item_id}.figure", item.get("figure"), index.figures, "figures[].id"
            )

    # -- 참조 그래프 비순환 --------------------------------------------------
    for cycle in _find_cycles(edges, index):
        checked += 1
        row.add(
            "pointer.acyclic",
            cycle[0],
            " → ".join(cycle),
            "비순환 참조 그래프",
            f"참조 그래프에 순환이 있다(간선 = {', '.join(GRAPH_FIELDS)})",
        )

    row.checked = checked
    row.extras["reference_edges"] = sum(len(values) for values in edges.values())
    return row


def _find_cycles(edges: dict[str, list[tuple[str, str]]], index: SpecIndex) -> list[list[str]]:
    """DFS 로 순환을 찾는다. 순환마다 1건씩, 경로를 그대로 보고한다."""
    cycles: list[list[str]] = []
    reported: set[frozenset] = set()
    state: dict[str, int] = {}  # 0=미방문 1=진행중 2=완료
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for target, _field in edges.get(node, []):
            if target not in index.items:
                continue  # 해소 실패는 pointer.resolve 가 이미 보고했다
            status = state.get(target, 0)
            if status == 1:
                start = stack.index(target)
                path = stack[start:] + [target]
                key = frozenset(path)
                if key not in reported:
                    reported.add(key)
                    cycles.append(path)
            elif status == 0:
                visit(target)
        stack.pop()
        state[node] = 2

    for node in index.items:
        if state.get(node, 0) == 0:
            visit(node)
    return cycles
