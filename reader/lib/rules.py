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
    # 재정 2026-08-18 P-B(전수 수치 수확) · P-2 ⓐ(서지 확장 대조)로 신설된 블록.
    # 없으면 `reader/lib/harvest.py`·`bibliography.py` 가 조용히 공허해지므로 로드에서 막는다.
    "numeric_harvest",
    "bibliography",
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

    @property
    def figure_captions(self) -> dict:
        return self.raw["figure_captions"]

    @property
    def numeric_harvest(self) -> dict:
        """전수 수치 수확 규칙(재정 P-B)."""
        return self.raw["numeric_harvest"]

    @property
    def bibliography(self) -> dict:
        """서지 확장 대조 규칙(재정 P-2 ⓐ)."""
        return self.raw["bibliography"]

    # -- 컴파일 -------------------------------------------------------------

    def _compile(self) -> None:
        self._compile_inventory()
        self._compile_dependency()
        self._compile_value_grammar()
        self._compile_convergence()
        self._compile_figure_captions()
        self._compile_numeric_harvest()
        self._compile_bibliography()

    def _compile_figure_captions(self) -> None:
        """도면 캡션 패턴. 탐지 패턴은 코드가 아니라 규칙 파일에 산다(SPEC §4.8 격리 요건 2항)."""
        block = self.raw.get("figure_captions") or {}
        line = block.get("caption_line")
        if not line:
            raise RulesError("figure_captions.caption_line 이 없다")
        self.figure_caption_line = re.compile(line, re.MULTILINE)
        strip = block.get("number_strip")
        self.figure_number_strip = re.compile(strip) if strip else None
        separator = block.get("id_separator")
        self.figure_id_separator = re.compile(separator) if separator else None
        self.figure_id_separator_replacement = str(
            block.get("id_separator_replacement", "-")
        )

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
        self._compile_structure_markers(block)
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

    def _compile_structure_markers(self, block: dict) -> None:
        """구조 표지 어형(재정 P-1 · 2026-08-18 총괄 정정).

        ★ **파서가 아니다.** 구조를 파싱하는 것이 아니라 **있는지 보는** 것이며, 그 구별이
        재정 P-1 의 "typed operator 신설은 N14 범위에서 제외한다"를 지키는 자리다. 그래서
        여기서 뽑는 것은 `(구조 이름, 컴파일된 패턴)` 뿐이고 그룹 포획을 두지 않는다.
        """
        markers = block.get("unclassified", {}).get("structure_markers") or {}
        flags = re.IGNORECASE if markers.get("case_insensitive") else 0
        compiled = []
        for entry in markers.get("forms") or []:
            structure = entry.get("structure")
            for pattern in entry.get("patterns") or []:
                compiled.append((str(structure), re.compile(pattern, flags)))
        if not compiled:
            raise RulesError(
                "dependency_citation.unclassified.structure_markers.forms 가 비어 있다 — "
                "표지 어형이 없으면 parse.unclassified-not-an-escape 가 전건을 실패시킨다"
            )
        self.structure_markers = tuple(compiled)

    def structure_markers_in(self, text: str) -> tuple:
        """본문에서 발견된 구조 이름 목록(중복 제거·발견 순). 없으면 빈 튜플."""
        found: list[str] = []
        for structure, pattern in self.structure_markers:
            if structure not in found and pattern.search(text or ""):
                found.append(structure)
        return tuple(found)

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
        self._compile_scan_forms(block, compiled)
        render = block.get("render") or {}
        if not render.get("forms"):
            raise RulesError("value_grammar.render.forms 가 없다")
        self.render_forms = render["forms"]
        self.render_approximate_prefix = render.get("approximate_prefix", "~")
        self.number_normalization = tuple(
            render.get("number_normalization") or ()
        )

    def _compile_scan_forms(self, block: dict, compiled: list) -> None:
        """어형 패턴의 **스캔용 파생**(앵커 제거)을 만든다 — `numeric_harvest.scan`.

        §4 의 어형 패턴은 값 문자열 전체를 판정하므로 `^…$` 앵커가 걸려 있다. 수확은 문장
        안에서 찾는 일이라 앵커가 있으면 아무것도 찾지 못하고, 그래서 초판이 낱개 십진만
        훑다가 복합 어형(range·inequality·tolerance·set)을 통째로 잃었다(2026-08-18 총괄
        검수 실측). 패턴을 두 벌 적지 않고 **같은 패턴에서 파생**한다.
        """
        scan = (self.raw.get("numeric_harvest") or {}).get("scan") or {}
        excluded = set(scan.get("exclude_kinds") or ())
        forms = []
        for form in compiled:
            if form.get("kind") in excluded:
                continue
            source = form["compiled"].pattern
            if scan.get("anchors") == "strip":
                if source.startswith("^"):
                    source = source[1:]
                if source.endswith("$"):
                    source = source[:-1]
            entry = dict(form)
            entry["scan"] = re.compile(source)
            forms.append(entry)
        # rank 순 정렬은 `_compile_value_grammar` 가 이미 했다 — 그 순서가 곧 소비 우선순위다.
        self.value_scan_forms = tuple(forms)

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
        # ★ 축별 정책(재정 P-3). 정책 정의는 `convergence.policies` 가 정본이고, 코드는
        #   status 어휘·임계 요구 여부를 그 표에서 읽는다 — 어느 축이 법이고 어느 축이
        #   계기인지를 코드가 고르면 그 순간 검사가 자기 입법이 된다(D7).
        policies = self.convergence.get("policies") or []
        if not policies:
            raise RulesError("convergence.policies 가 비어 있다(재정 P-3)")
        table: dict[str, dict] = {}
        for policy in policies:
            policy_id = policy.get("id")
            if not policy_id:
                raise RulesError("convergence.policies 에 id 없는 항목이 있다")
            table[str(policy_id)] = policy
        self.convergence_policies = table
        for axis in self.convergence_axes:
            axis_policy = axis.get("policy")
            if axis_policy not in table:
                raise RulesError(
                    f"convergence.axes[{axis.get('id')}] 의 policy 가 정의되지 않았다: "
                    f"{axis_policy!r} (재정 P-3 — 축마다 policy 는 필수다)"
                )
        self.convergence_profile = self.convergence.get("profile") or {}

    def _compile_numeric_harvest(self) -> None:
        """수확 규칙(재정 P-B). 단위 후보 패턴은 규칙 파일이 정본이다."""
        block = self.numeric_harvest
        detection = block.get("unit_detection") or {}
        pattern = detection.get("pattern")
        if not pattern:
            raise RulesError("numeric_harvest.unit_detection.pattern 이 없다")
        boundary = detection.get("boundary")
        if not boundary:
            raise RulesError("numeric_harvest.unit_detection.boundary 가 없다")
        # 경계는 패턴 뒤에 붙는 전방탐색이다 — 긴 낱말의 앞머리가 단위로 읽히는 것을 막는다.
        self.harvest_unit_pattern = re.compile(pattern + boundary)
        self.harvest_unit_max_length = int(detection.get("max_length", 0))
        if self.harvest_unit_max_length <= 0:
            raise RulesError("numeric_harvest.unit_detection.max_length 가 없다")
        # 토큰 경계 — 영숫자 토큰 **내부**의 숫자를 수치로 읽지 않는다(`cm3` 의 `3`).
        # 입법이 아니라 토큰화 규율이므로 단위표와 무관하다(규칙 파일 `token_boundary`).
        boundaries = block.get("token_boundary") or {}
        left = boundaries.get("left_forbidden")
        right = boundaries.get("right_letter")
        if not left or not right:
            raise RulesError("numeric_harvest.token_boundary 가 없다")
        self.harvest_left_forbidden = re.compile(left)
        self.harvest_right_letter = re.compile(right)
        # 경계 기각의 사유 라벨 — 지금까지 이 기각은 `continue` 하나였고 아무 기록도 남기지
        # 않았다(2026-08-18 통주 2 실측). 라벨을 코드가 아니라 파일에 두는 이유는 CP1 §12.3 이
        # 사유별로 세는 어휘가 곧 계약이기 때문이다.
        labels = boundaries.get("rejection_labels") or {}
        if not labels.get("left") or not labels.get("right"):
            raise RulesError(
                "numeric_harvest.token_boundary.rejection_labels 에 left·right 가 없다"
                "(경계 기각을 기록 없이 버리는 경로를 막는다)"
            )
        self.harvest_boundary_labels = {
            "left": str(labels["left"]),
            "right": str(labels["right"]),
        }
        vocabulary = detection.get("vocabulary")
        if not vocabulary:
            raise RulesError("numeric_harvest.unit_detection.vocabulary 가 비어 있다")
        # 인식 어휘 — 정규화 표(`UNIT_ALIASES`)와 역할이 다르다(규칙 파일 `accept_why`).
        self.harvest_unit_vocabulary = frozenset(
            str(unit).lower() for unit in vocabulary
        )
        label = block.get("label_template")
        if not label:
            raise RulesError("numeric_harvest.label_template 이 없다")
        self.harvest_label_template = str(label)
        bib_label = block.get("bibliographic_label_template")
        if not bib_label:
            raise RulesError("numeric_harvest.bibliographic_label_template 이 없다")
        self.harvest_bib_label_template = str(bib_label)
        fields = block.get("bibliographic_fields") or []
        if not fields:
            raise RulesError("numeric_harvest.bibliographic_fields 가 비어 있다")
        self.harvest_bib_fields = tuple(
            {
                "field": str(entry.get("field")),
                "path": tuple(entry.get("path") or ()),
                "expect_kind": entry.get("expect_kind"),
            }
            for entry in fields
        )
        for entry in self.harvest_bib_fields:
            if not entry["path"] or not entry["expect_kind"]:
                raise RulesError(
                    f"numeric_harvest.bibliographic_fields[{entry['field']}] 에 "
                    "path 또는 expect_kind 가 없다"
                )
        template = str(block.get("id_template") or "")
        if "{n}" not in template:
            raise RulesError("numeric_harvest.id_template 에 {n} 자리가 없다")
        self.harvest_id_template = template
        parity = block.get("parity_key") or {}
        if not parity.get("quoted") or not parity.get("bibliographic"):
            raise RulesError("numeric_harvest.parity_key 에 두 갈래가 다 있어야 한다")
        self.harvest_parity_key = {
            origin: tuple(paths) for origin, paths in parity.items()
        }
        identity = block.get("identity_key") or ()
        if not identity:
            raise RulesError("numeric_harvest.identity_key 가 없다")
        self.harvest_identity_key = tuple(identity)
        # 대조 범위 — 정답지의 정의(`l0-format §9 answer_sources`)와 같은 범위여야 한다.
        # 코드가 `"active"` 를 리터럴로 들면 정답지의 정의가 바뀔 때 이쪽만 낡는다.
        scope = block.get("answer_scope") or {}
        if not scope.get("status") or not scope.get("origin") or not scope.get("kind"):
            raise RulesError("numeric_harvest.answer_scope 가 없다(kind·origin·status 필수)")
        self.harvest_answer_scope = {
            "kind": str(scope["kind"]),
            "origin": tuple(scope["origin"]),
            "status": str(scope["status"]),
        }
        # 배제 규칙(도면부호 등) — 조건은 코드가 알고 **어느 규칙이 켜져 있는지**는 파일이 안다.
        exclusions = block.get("exclusions") or []
        self.harvest_exclusions = tuple(exclusions)
        self._compile_harvest_envelopes(block, exclusions)

    def _compile_harvest_envelopes(self, block: dict, exclusions) -> None:
        """봉투 배제 — 좌표 표현 **구간**을 먼저 표시하는 패턴들(2026-08-18 통주 2 처분).

        `figure-numeral` 과 달리 조건을 코드가 알지 못한다. 여기서 아는 것은 "규칙 파일이
        든 정규식에 걸리는 구간은 값이 아니라 자리다" 하나뿐이며, 무엇이 좌표 표현인지는
        전적으로 파일이 든다(D7 — 코드가 자기 법을 갖지 않는다).

        ★ 부재는 통과가 아니라 오류다. 여섯(2026-08-18 넷 + 재정 2026-08-19 S7 둘) 중
        하나를 지우는 것만으로 배제가 조용히 꺼지면 통주 2 가 실측한 23건이 아무 신호 없이
        정답지로 돌아온다. 같은 회차의 `bibliography.priority_window` 가 세운 선례를 그대로
        따른다. **세는 것은 개수가 아니라 존재다** — 특정 수를 요구하면 재정이 항목을 더할
        때마다 로더가 함께 낡는다. 현재 계수의 정본은 규칙 파일
        `numeric_harvest.enclosing_exclusions.required_why` 다.
        """
        declaration = block.get("enclosing_exclusions") or {}
        if declaration.get("required") is not True:
            raise RulesError(
                "numeric_harvest.enclosing_exclusions.required 가 true 가 아니다"
                "(봉투 배제의 부재를 통과로 읽는 경로를 막는다 — 재정 P-B 잔여)"
            )
        compiled = []
        for entry in exclusions:
            if entry.get("match") != "enclosing-pattern":
                continue
            pattern = entry.get("pattern")
            label = entry.get("reason_label")
            if not pattern or not label:
                raise RulesError(
                    f"numeric_harvest.exclusions[{entry.get('id')}] 에 pattern 또는 "
                    "reason_label 이 없다(봉투 배제)"
                )
            compiled.append(
                {
                    "id": str(entry.get("id")),
                    "pattern": re.compile(str(pattern)),
                    "reason_label": str(label),
                }
            )
        if not compiled:
            raise RulesError(
                "numeric_harvest.exclusions 에 match: enclosing-pattern 항목이 하나도 없다"
                "(봉투 배제가 꺼졌다 — 좌표 오파싱이 정답지로 돌아온다)"
            )
        self.harvest_envelope_patterns = tuple(compiled)

    def in_answer_scope(self, item: dict) -> bool:
        """항목이 **정답지 범위**에 드는가(kind·origin·status 3조건).

        철회·대체된 항목은 정답지가 아니다 — append-only 규율상 그 항목들은 명세에 남아
        있으므로, 상태를 보지 않으면 규율을 지킨 명세가 반드시 실패한다.
        """
        scope = self.harvest_answer_scope
        return (
            item.get("kind") == scope["kind"]
            and item.get("origin") in scope["origin"]
            and item.get("status") == scope["status"]
        )

    def harvest_exclusion(self, exclusion_id: str) -> dict | None:
        """배제 규칙 1건. 파일에서 지우면 그 배제가 사라진다(코드가 아니라 계약이 켜고 끈다)."""
        for entry in self.harvest_exclusions:
            if entry.get("id") == exclusion_id:
                return entry
        return None

    def _compile_bibliography(self) -> None:
        """서지 대조 규칙(재정 P-2 ⓐ)."""
        block = self.bibliography
        rules = block.get("rules") or []
        if not rules:
            raise RulesError("bibliography.rules 가 비어 있다")
        self.bibliography_rules = tuple(rules)
        targets = block.get("source_substring_targets") or []
        if not targets:
            raise RulesError("bibliography.source_substring_targets 가 비어 있다")
        self.bibliography_substring_targets = tuple(str(item) for item in targets)

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

    def policy_of(self, axis: dict) -> dict:
        """축의 정책 정의(재정 P-3). 로드 시 존재가 보장되어 있다."""
        return self.convergence_policies[axis.get("policy")]

    def dependency_rule_ids(self) -> tuple:
        """`dependency_citation.rules` 의 id 목록(규칙 수 = ruleset_size 의 근거)."""
        return tuple(
            entry.get("id") for entry in (self.dependency_citation.get("rules") or ())
        )

    def bibliography_rule_ids(self) -> tuple:
        return tuple(entry.get("id") for entry in self.bibliography_rules)

    def unclassified_value(self) -> str:
        """구조 미분류 표지 값(재정 P-1). 코드에 문자열을 박지 않는다."""
        block = self.dependency_citation.get("unclassified") or {}
        value = block.get("value")
        if not value:
            raise RulesError("dependency_citation.unclassified.value 가 없다(재정 P-1)")
        return str(value)
