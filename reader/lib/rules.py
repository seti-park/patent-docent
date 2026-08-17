# -*- coding: utf-8 -*-
"""독해층 규칙 계약(`reader/reader-rules.yaml`)의 로더.

★ 이 모듈이 있는 이유 — 탐지 패턴을 코드에 리터럴로 두지 않기 위해서다
(SPEC §4.8 자기매칭 격리 요건 2항 · reader-rules.yaml 머리말 ①②).
청구항 구간 경계·종속 인용 어형·수치 문법·생애 전이표·수렴 축은 전부 그 파일이 정본이고,
여기서는 **읽어서 컴파일할 뿐**이다. 규칙을 바꾸려면 파일을 고쳐야 하고 diff 가 곧 개정
이력이 된다.

패턴은 로드 시 1회 컴파일한다 — 검사가 항목마다 재컴파일하면 대량 인스턴스에서 비용이
선형으로 늘고, 컴파일 오류가 검사 도중에 터진다(로드 시점에 터지는 편이 낫다).
"""

from __future__ import annotations

import os
import re

import yaml

# 규칙 파일의 기본 위치 = 이식 단위 안. reader/lib/rules.py → reader/reader-rules.yaml
DEFAULT_RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "reader-rules.yaml",
)

# 로더가 존재를 요구하는 최상위 블록. 하나라도 없으면 그 블록을 소비하는 검사가
# 조용히 공허해지므로 로드 시점에 실패시킨다.
# 규칙 문언 안에서 패턴을 뽑을 때 쓰는 보조 — 백틱 사이의 첫 조각.
BACKTICK_PATTERN = re.compile(r"`([^`]+)`")

# `origin_kind_binding.when` 에 등장하는 서지 필드 토큰(스키마 bib_source.field enum 과 동형).
BIB_FIELD_TOKEN = re.compile(r"patent\.(?:number|dates\.(?:priority|filing|publication))")

REQUIRED_BLOCKS = (
    "claim_inventory",
    "dependency_citation",
    "item_lifecycle",
    "value_grammar",
    "convergence",
)


class RulesError(Exception):
    """규칙 파일 부재·파싱 불능·필수 키 누락."""


class Rules:
    """reader-rules.yaml 로더. 패턴은 로드 시 1회 컴파일한다."""

    def __init__(self, raw: dict, path: str) -> None:
        self.raw = raw
        self.path = path
        self.version = str(raw.get("version", ""))
        self.schema = raw.get("schema", "")
        self._compile()

    # -- 로드 ---------------------------------------------------------------

    @classmethod
    def load(cls, path: str | None = None) -> "Rules":
        """규칙 파일을 읽는다. `path` 생략 시 패키지 상대 경로를 쓴다."""
        target = path or DEFAULT_RULES_PATH
        try:
            with open(target, encoding="utf-8") as handle:
                raw = yaml.safe_load(handle)
        except FileNotFoundError as exc:
            raise RulesError(f"규칙 파일이 없다: {target}") from exc
        except yaml.YAMLError as exc:
            raise RulesError(f"규칙 파일 파싱 불능: {target}: {exc}") from exc
        if not isinstance(raw, dict):
            raise RulesError(f"규칙 파일 최상위가 매핑이 아니다: {target}")
        missing = [key for key in REQUIRED_BLOCKS if key not in raw]
        if missing:
            raise RulesError(f"규칙 파일에 필수 블록이 없다: {', '.join(missing)} ({target})")
        return cls(raw, target)

    # -- 편의 접근자 --------------------------------------------------------

    @property
    def claim_inventory(self) -> dict:
        return self.raw["claim_inventory"]

    @property
    def dependency_citation(self) -> dict:
        return self.raw["dependency_citation"]

    @property
    def item_lifecycle(self) -> dict:
        return self.raw["item_lifecycle"]

    @property
    def value_grammar(self) -> dict:
        return self.raw["value_grammar"]

    @property
    def convergence(self) -> dict:
        return self.raw["convergence"]

    # -- 컴파일 -------------------------------------------------------------

    def _compile(self) -> None:
        self._compile_inventory()
        self._compile_dependency()
        self._compile_value_grammar()
        self._compile_convergence()

    def _compile_inventory(self) -> None:
        block = self.claim_inventory
        section = block.get("section") or {}
        headings = section.get("headings") or []
        if not headings:
            raise RulesError("claim_inventory.section.headings 가 비어 있다")
        # 헤더는 행 단위로 찾으므로 MULTILINE 이 필수다.
        self.inventory_heading_patterns = tuple(
            re.compile(pattern, re.MULTILINE) for pattern in headings
        )
        claim_start = block.get("claim_start")
        if not claim_start:
            raise RulesError("claim_inventory.claim_start 가 없다")
        self.inventory_claim_start = re.compile(claim_start, re.MULTILINE)
        canceled = block.get("canceled_body")
        if not canceled:
            raise RulesError("claim_inventory.canceled_body 가 없다")
        self.inventory_canceled = re.compile(canceled)
        self.inventory_rules = tuple(block.get("rules") or ())

    def _compile_dependency(self) -> None:
        block = self.dependency_citation
        forms = block.get("forms") or []
        if not forms:
            raise RulesError("dependency_citation.forms 가 비어 있다")
        flags = re.IGNORECASE if block.get("case_insensitive") else 0
        compiled = []
        for form in sorted(forms, key=lambda item: item.get("rank", 0)):
            compiled.append(
                {
                    "rank": form.get("rank"),
                    "id": form.get("id"),
                    "implies_type": form.get("implies_type"),
                    "requires_literal": form.get("requires_literal"),
                    "pattern": re.compile(form["pattern"], flags),
                }
            )
        self.dependency_forms = tuple(compiled)

    def _compile_value_grammar(self) -> None:
        block = self.value_grammar
        self._compile_preprocess(block)
        self._compile_origin_bindings(block)
        decimal = block.get("decimal")
        if not decimal:
            raise RulesError("value_grammar.decimal 이 없다")
        self.decimal_source = decimal
        self.decimal_pattern = re.compile(decimal)
        self.decimal_full = re.compile(f"^(?:{decimal})$")
        placeholder = block.get("placeholder", "DEC")
        self.value_placeholder = placeholder
        markers = block.get("approximate_markers") or []
        self.approximate_markers = tuple(
            (source, re.compile(source, re.IGNORECASE)) for source in markers
        )
        forms = block.get("forms") or []
        if not forms:
            raise RulesError("value_grammar.forms 가 비어 있다")
        compiled = []
        for form in sorted(forms, key=lambda item: item.get("rank", 0)):
            # `DEC` 자리표시자를 십진 토큰으로 치환해 컴파일한다(패턴 중복 기입 금지).
            source = form["pattern"].replace(placeholder, f"(?:{decimal})")
            entry = dict(form)
            entry["compiled"] = re.compile(source)
            compiled.append(entry)
        self.value_forms = tuple(compiled)
        render = block.get("render") or {}
        if not render.get("forms"):
            raise RulesError("value_grammar.render.forms 가 없다")
        self.render_forms = render["forms"]
        self.render_approximate_prefix = render.get("approximate_prefix", "~")
        self.number_normalization = tuple(
            render.get("number_normalization") or ()
        )

    def _compile_preprocess(self, block: dict) -> None:
        """`value_grammar.preprocess` 를 순서대로 컴파일한다.

        ★ 천단위 규칙의 정규식은 `rule` 문언 안의 백틱 사이에 산다 — 규칙 파일에 전용
        `pattern:` 키가 없기 때문이다. 여기서 문언 밖으로 뽑아 컴파일하되, 뽑지 못하면
        **로드 시점에 실패**시킨다(코드에 사본을 두면 그 순간 정본이 둘이 된다).
        """
        steps = block.get("preprocess") or []
        compiled = []
        for step in steps:
            step_id = step.get("id")
            if step_id == "strip-unit":
                compiled.append({"id": step_id, "op": "strip-unit", "regex": None})
                continue
            match = BACKTICK_PATTERN.search(str(step.get("rule", "")))
            if not match:
                raise RulesError(
                    f"value_grammar.preprocess[{step_id}] 의 rule 에서 패턴을 찾지 못했다"
                )
            compiled.append(
                {"id": step_id, "op": "regex-remove", "regex": re.compile(match.group(1))}
            )
        self.value_preprocess = tuple(compiled)

    def _compile_origin_bindings(self, block: dict) -> None:
        """`origin_kind_binding` 표를 구조화한다.

        표의 조건은 산문형 `when` 문언이므로, 로더가 이해하는 형태는 둘뿐이다 —
        ① `origin == "bibliographic"` + `patent.*` 서지 필드 열거 ② 제약 없는 포괄 행.
        그 밖의 조건이 표에 추가되면 **조용히 무시하지 않고 로드에서 실패**한다.
        """
        entries = block.get("origin_kind_binding") or []
        compiled = []
        for entry in entries:
            when = str(entry.get("when", ""))
            fields = tuple(sorted(set(BIB_FIELD_TOKEN.findall(when))))
            require_kind = entry.get("require_kind")
            expect_kind = entry.get("expect_kind_for_parse")
            if require_kind is None and expect_kind is None and not fields:
                compiled.append({"catch_all": True})
                continue
            if '"bibliographic"' not in when or not fields:
                raise RulesError(
                    f"origin_kind_binding 의 조건을 해석하지 못했다: {when!r}"
                )
            compiled.append(
                {
                    "catch_all": False,
                    "origin": "bibliographic",
                    "bib_fields": fields,
                    "require_kind": require_kind,
                    "expect_kind": expect_kind,
                }
            )
        self.origin_kind_binding = tuple(compiled)

    def kind_binding_for(self, origin: str | None, bib_field: str | None) -> dict | None:
        """origin 이 kind 를 결정하는 경우의 결속 행. 해당 없으면 None."""
        for entry in self.origin_kind_binding:
            if entry.get("catch_all"):
                continue
            if entry["origin"] == origin and bib_field in entry["bib_fields"]:
                return entry
        return None

    def _compile_convergence(self) -> None:
        axes = self.convergence.get("axes") or []
        if not axes:
            raise RulesError("convergence.axes 가 비어 있다")
        self.convergence_axes = tuple(axes)

    # -- 파생 조회 ----------------------------------------------------------

    def lifecycle_transitions(self) -> dict:
        return self.item_lifecycle.get("transitions") or {}

    def lifecycle_terminal_states(self) -> tuple:
        return tuple(self.item_lifecycle.get("terminal_states") or ())

    def payload_excluded_fields(self) -> tuple:
        canon = self.item_lifecycle.get("payload_canonicalization") or {}
        return tuple(canon.get("excluded_fields") or ())

    def payload_serialization(self) -> dict:
        canon = self.item_lifecycle.get("payload_canonicalization") or {}
        return canon.get("serialization") or {}

    def axis(self, axis_id: str) -> dict:
        for axis in self.convergence_axes:
            if axis.get("id") == axis_id:
                return axis
        raise RulesError(f"convergence.axes 에 {axis_id} 축이 없다")
