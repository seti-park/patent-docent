# -*- coding: utf-8 -*-
"""인스턴스 로드와 인덱싱.

`SpecIndex` 는 인스턴스를 **1회 순회**해 전 검사 모듈이 쓰는 조회표를 만든다. 각 검사가
자기 순회를 따로 쓰면 재귀 전개(중첩 element)의 해석이 모듈마다 갈리고, 그 순간 검사들이
서로 다른 인스턴스를 보게 된다.

검사는 읽기 전용이다 — 이 모듈은 인스턴스를 복사하지도 변형하지도 않고 **참조만** 담는다.
"""

from __future__ import annotations

import json
import os

# 스키마 정본은 이식 단위 안에 있다(SPEC §2.1). reader/lib/spec_io.py → reader/schemas/...
DEFAULT_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "schemas",
    "material-spec.schema.json",
)


def load_spec(path: str) -> dict:
    """재료 명세 인스턴스(JSON)를 읽는다."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(path: str | None = None) -> dict:
    """재료 명세 스키마를 읽는다. 생략 시 `reader/schemas/material-spec.schema.json`."""
    with open(path or DEFAULT_SCHEMA_PATH, encoding="utf-8") as handle:
        return json.load(handle)


class SpecIndex:
    """인스턴스 1회 순회로 만드는 인덱스."""

    def __init__(self) -> None:
        self.items: dict[str, dict] = {}
        self.elements: dict[str, dict] = {}
        self.element_parent: dict[str, str | None] = {}
        self.element_claim: dict[str, str] = {}
        self.additions: dict[str, dict] = {}
        self.addition_claim: dict[str, str] = {}
        self.claims: dict[str, dict] = {}
        self.figures: dict[str, dict] = {}
        self.independent: list[dict] = []
        self.dependents: list[dict] = []

    @classmethod
    def build(cls, spec: dict) -> "SpecIndex":
        index = cls()
        for item in spec.get("items") or []:
            item_id = item.get("id")
            if isinstance(item_id, str):
                index.items[item_id] = item
        for figure in spec.get("figures") or []:
            figure_id = figure.get("id")
            if isinstance(figure_id, str):
                index.figures[figure_id] = figure
        claims = spec.get("claims") or {}
        for claim in claims.get("independent") or []:
            claim_id = claim.get("id")
            if isinstance(claim_id, str):
                index.claims[claim_id] = claim
            index.independent.append(claim)
            index._walk_elements(claim.get("elements") or [], None, claim_id)
        for claim in claims.get("dependents") or []:
            claim_id = claim.get("id")
            if isinstance(claim_id, str):
                index.claims[claim_id] = claim
            index.dependents.append(claim)
            for addition in claim.get("additions") or []:
                addition_id = addition.get("id")
                if isinstance(addition_id, str):
                    index.additions[addition_id] = addition
                    index.addition_claim[addition_id] = claim_id
        return index

    def _walk_elements(
        self, elements: list, parent_id: str | None, claim_id: str | None
    ) -> None:
        for element in elements:
            element_id = element.get("id")
            if isinstance(element_id, str):
                self.elements[element_id] = element
                self.element_parent[element_id] = parent_id
                if claim_id is not None:
                    self.element_claim[element_id] = claim_id
            self._walk_elements(element.get("children") or [], element_id, claim_id)

    # -- 조회 편의 ----------------------------------------------------------

    def items_of_kind(self, kind: str) -> list[dict]:
        return [item for item in self.items.values() if item.get("kind") == kind]

    def element_or_addition(self, target_id: str) -> dict | None:
        return self.elements.get(target_id) or self.additions.get(target_id)

    def claim_of(self, target_id: str) -> str | None:
        """element·addition id 가 속한 청구항 id."""
        if target_id in self.element_claim:
            return self.element_claim[target_id]
        return self.addition_claim.get(target_id)
