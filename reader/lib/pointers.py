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
GRAPH_FIELDS = ("derivation.inputs[].ref", "derived_from[]", "superseded_by", "grounding.component")


def check(ctx: CheckContext) -> CheckRow:
    row = CheckRow(check_id=CHECK_ID)
    index = SpecIndex.build(ctx.spec)
    spec = ctx.spec
    checked = 0
    edges: dict[str, list[tuple[str, str]]] = {}

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
