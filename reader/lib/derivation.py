# -*- coding: utf-8 -*-
"""`read.value-derivation` — 수치 사실의 출처 결속(SPEC §2.6 검사 6).

이 검사가 M1 의 심장이다. 재감수 B-04 가 실측한 구멍 — **실재하는 인용문 옆에 날조한
`value_raw` 를 적어 넣은 인스턴스가 스키마를 통과한다** — 를 닫는 것이 유일한 목적이며,
그 값이 곧 숫자 전수 대조의 정답지이기 때문에(SPEC §4.4.1) 오류가 하류 전체로 전파된다.

origin 별 대조 + 전 origin 공통 2종 + 깊이 1 + `_en` 한글 재확인을 한 행에 싣는다.

  1. `quoted`        `value_raw == source.quote[value_span]` 바이트 동일
  2. `derived`       산식 재계산 + `rounding` 적용 == `value_normalized` 문자열 일치
  3. `bibliographic` `patent` 블록 해당 필드와 일치
  4. `figure-sourced` 대조 면제 + `manual_verification_required[]` 수집(면제를 완료로
     조용히 바꾸지 않는다)
  5. 공통 ①  `parse_value(value_raw, unit) == value_type` — 범위·부등호를 스칼라로 뭉개
     담는 경로를 막는다
  6. 공통 ②  `value_normalized == render_value(value_type)`
  7. 깊이 1  `derivation.inputs[].ref` 가 가리키는 `fact` 의 `origin` 은 `quoted` 여야 한다
     (재정 N9 · 재감수 M-01 — 원문 스팬만이 원천이다)
  8. `_en` 슬롯에 한글이 없다(재감수 M-02 — 스키마가 1차로 막고 스크립트가 재확인한다)

산식 평가는 **재귀 하강 파서**로 한다. `eval`·`exec` 를 쓰지 않는다 — 정답지를 만드는
경로에 임의 코드 실행을 두면 그 검사가 방어가 아니라 구멍이 된다.
"""

from __future__ import annotations

import decimal
import re

from .normalize import format_decimal, normalize_number, NormalizeError
from .report import CheckContext, CheckRow
from .rules import Rules
from .spec_io import SpecIndex, load_schema
from .value_grammar import ValueGrammarError, parse_value, render_value

CHECK_ID = "read.value-derivation"

# `_en` 언어 정책의 집행 대상 8슬롯(SPEC §2.4 표).
EN_SLOTS: dict[str, tuple[str, ...]] = {
    "component": ("label_en",),
    "fact": ("label_en",),
    "implication": ("statement_en",),
    "figure_note": ("what_it_shows_en",),
    "positioning": ("background_problem", "asserted_effect", "delta"),
}

# 서지 복사의 출처 필드(스키마 bib_source.field enum).
BIB_FIELDS: dict[str, tuple[str, ...]] = {
    "patent.number": ("number",),
    "patent.dates.priority": ("dates", "priority"),
    "patent.dates.filing": ("dates", "filing"),
    "patent.dates.publication": ("dates", "publication"),
}

_ARITH_CONTEXT = decimal.Context(prec=60)
_TOKEN = re.compile(r"\s*(?:(?P<name>[a-z][a-z0-9_]*)|(?P<number>\d+(?:\.\d+)?|\.\d+)|(?P<op>[-+*/()]))")

_HANGUL_CACHE: "re.Pattern[str] | None" = None
_NON_ARITHMETIC_CACHE: tuple | None = None


class FormulaError(ValueError):
    """산식 파싱·평가 실패."""


# ---------------------------------------------------------------------------
# 안전 산술 평가기 (eval 금지 — 재귀 하강)
# ---------------------------------------------------------------------------


def _tokenize(formula: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    position = 0
    while position < len(formula):
        if formula[position].isspace():
            position += 1
            continue
        match = _TOKEN.match(formula, position)
        if not match or match.end() == position:
            raise FormulaError(f"산식에 허용되지 않는 문자가 있다: {formula[position]!r}")
        for kind in ("name", "number", "op"):
            value = match.group(kind)
            if value is not None:
                tokens.append((kind, value))
                break
        position = match.end()
    return tokens


class _Parser:
    """expr := term (('+'|'-') term)* / term := factor (('*'|'/') factor)* /
    factor := ('+'|'-')? primary / primary := NAME | NUMBER | '(' expr ')'"""

    def __init__(self, tokens: list[tuple[str, str]], names: dict[str, decimal.Decimal]) -> None:
        self.tokens = tokens
        self.names = names
        self.position = 0

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self) -> tuple[str, str]:
        token = self.peek()
        if token is None:
            raise FormulaError("산식이 도중에 끝났다")
        self.position += 1
        return token

    def parse(self) -> decimal.Decimal:
        value = self.expr()
        if self.peek() is not None:
            raise FormulaError(f"산식 끝에 남은 토큰이 있다: {self.peek()[1]!r}")
        return value

    def expr(self) -> decimal.Decimal:
        value = self.term()
        while True:
            token = self.peek()
            if token is None or token[0] != "op" or token[1] not in "+-":
                return value
            self.take()
            right = self.term()
            value = _ARITH_CONTEXT.add(value, right) if token[1] == "+" else _ARITH_CONTEXT.subtract(value, right)

    def term(self) -> decimal.Decimal:
        value = self.factor()
        while True:
            token = self.peek()
            if token is None or token[0] != "op" or token[1] not in "*/":
                return value
            self.take()
            right = self.factor()
            if token[1] == "*":
                value = _ARITH_CONTEXT.multiply(value, right)
            else:
                if right == 0:
                    raise FormulaError("0 으로 나눈다")
                value = _ARITH_CONTEXT.divide(value, right)

    def factor(self) -> decimal.Decimal:
        token = self.peek()
        if token is not None and token[0] == "op" and token[1] in "+-":
            self.take()
            value = self.factor()
            return value if token[1] == "+" else _ARITH_CONTEXT.minus(value)
        return self.primary()

    def primary(self) -> decimal.Decimal:
        kind, value = self.take()
        if kind == "name":
            if value not in self.names:
                raise FormulaError(f"산식의 입력 이름이 inputs 에 없다: {value}")
            return self.names[value]
        if kind == "number":
            return _ARITH_CONTEXT.create_decimal(value)
        if value == "(":
            inner = self.expr()
            closing = self.take()
            if closing[1] != ")":
                raise FormulaError("괄호가 닫히지 않았다")
            return inner
        raise FormulaError(f"산식에서 값이 와야 할 자리에 {value!r} 이 있다")


def evaluate_formula(formula: str, names: dict[str, decimal.Decimal]) -> decimal.Decimal:
    """안전 산술식을 평가한다(입력 name · 십진 리터럴 · `+ - * / ( )` 만)."""
    return _Parser(_tokenize(formula or ""), names).parse()


def apply_rounding(value: decimal.Decimal, rounding: dict) -> decimal.Decimal:
    """`rounding` = `{mode, digits}`. mode 는 none·decimal-places·significant-digits."""
    mode = (rounding or {}).get("mode", "none")
    digits = int((rounding or {}).get("digits", 0))
    if mode == "none":
        return value
    if mode == "decimal-places":
        quantum = decimal.Decimal(1).scaleb(-digits)
        return value.quantize(quantum, rounding=decimal.ROUND_HALF_UP)
    if mode == "significant-digits":
        if digits < 1:
            raise FormulaError("significant-digits 는 digits ≥ 1 이어야 한다")
        context = decimal.Context(prec=digits, rounding=decimal.ROUND_HALF_UP)
        return context.plus(value)
    raise FormulaError(f"알 수 없는 rounding.mode: {mode!r}")


# ---------------------------------------------------------------------------
# 검사
# ---------------------------------------------------------------------------


def _hangul_regex(schema: dict | None) -> "re.Pattern[str]":
    """한글 탐지 패턴은 스키마 `$defs/en_text` 가 정본이다(코드에 리터럴을 두지 않는다)."""
    global _HANGUL_CACHE
    source = None
    target = schema
    if target is None:
        if _HANGUL_CACHE is not None:
            return _HANGUL_CACHE
        target = load_schema()
    en_text = ((target.get("$defs") or {}).get("en_text") or {})
    source = (en_text.get("not") or {}).get("pattern")
    if not source:
        raise ValueError("스키마 $defs/en_text 에서 한글 패턴을 찾지 못했다")
    compiled = re.compile(source)
    if schema is None:
        _HANGUL_CACHE = compiled
    return compiled


def _non_arithmetic_kinds(schema: dict | None) -> tuple:
    """산식에 넣을 수 없는 `value_type.kind` 목록을 **스키마에서 도출**한다.

    판별식: `value` 필드를 갖되 그것이 `$defs/decimal` 참조가 아닌 분기(= `date`·`identifier`).
    코드에 kind 이름을 열거하면 유니온이 늘 때 이 검사만 조용히 낡는다.
    """
    global _NON_ARITHMETIC_CACHE
    target = schema
    if target is None:
        if _NON_ARITHMETIC_CACHE is not None:
            return _NON_ARITHMETIC_CACHE
        target = load_schema()
    kinds = []
    for branch in ((target.get("$defs") or {}).get("value_type") or {}).get("oneOf") or []:
        properties = branch.get("properties") or {}
        value = properties.get("value")
        if value is None:
            continue
        if value.get("$ref") != "#/$defs/decimal":
            kinds.append((properties.get("kind") or {}).get("const"))
    result = tuple(kind for kind in kinds if kind)
    if schema is None:
        _NON_ARITHMETIC_CACHE = result
    return result


def _span_text(text: str, span: dict) -> str | None:
    start = span.get("start")
    end = span.get("end")
    if not isinstance(start, int) or not isinstance(end, int):
        return None
    if start < 0 or end > len(text) or start >= end:
        return None
    return text[start:end]


def check(ctx: CheckContext) -> CheckRow:
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#value_grammar",
        ruleset_version=rules.version,
        ruleset_size=len(rules.value_forms),
    )
    index = SpecIndex.build(ctx.spec)
    patent = ctx.spec.get("patent") or {}

    facts = [item for item in index.items.values() if item.get("kind") == "fact"]
    row.checked = len(facts)

    quoted_ids: list[str] = []
    bibliographic_ids: list[str] = []
    derived_entries: list[dict] = []
    figure_entries: list[dict] = []
    manual: list[dict] = []

    for fact in facts:
        item_id = fact.get("id", "?")
        origin = fact.get("origin")
        value_raw = fact.get("value_raw") or ""
        value_normalized = fact.get("value_normalized") or ""
        value_type = fact.get("value_type")
        unit = fact.get("unit")

        if origin == "quoted":
            quoted_ids.append(item_id)
            _check_quoted(row, fact, item_id)
        elif origin == "bibliographic":
            # §1.4 — 서지 복사는 원문 스팬과 **같은 갈래로 계수**하되, 어느 항목이 서지인지는
            # 따로 드러낸다(계수는 합치되 정체는 숨기지 않는다).
            quoted_ids.append(item_id)
            bibliographic_ids.append(item_id)
            _check_bibliographic(row, fact, item_id, patent)
        elif origin == "derived":
            derived_entries.append(
                _check_derived(row, fact, item_id, index, _non_arithmetic_kinds(ctx.schema))
            )
        elif origin == "figure-sourced":
            figure_source = fact.get("figure_source") or {}
            figure_entries.append(
                {
                    "material_id": item_id,
                    "figure": figure_source.get("figure"),
                    "machine_verifiable": bool(fact.get("machine_verifiable")),
                }
            )
            manual.append(
                {
                    "material_id": item_id,
                    "reason": "figure-sourced",
                    "figure": figure_source.get("figure"),
                    "numerals": list(figure_source.get("numerals") or []),
                }
            )

        # origin ↔ kind 결속(규칙 파일 `origin_kind_binding`) — origin 이 값의 종류를
        # 결정하는 경우, 문법의 추측이 아니라 그 결속이 파싱 형태를 지정한다.
        binding = rules.kind_binding_for(origin, (fact.get("bib_source") or {}).get("field"))
        expect_kind = binding["expect_kind"] if binding else None
        if binding and binding.get("require_kind"):
            actual_kind = value_type.get("kind") if isinstance(value_type, dict) else None
            if actual_kind != binding["require_kind"]:
                row.add(
                    "value.origin-kind-binding",
                    f"{item_id}.value_type.kind",
                    str(actual_kind),
                    str(binding["require_kind"]),
                    "origin 이 결정하는 값의 종류와 선언된 kind 가 다르다 — "
                    "서지 복사값이 수치로 읽히면 정답지에 없는 수가 하나 는다",
                )

        # 공통 ① value_type 대조
        try:
            parsed = parse_value(value_raw, unit, rules, expect_kind=expect_kind)
        except ValueGrammarError as exc:
            parsed = None
            row.add(
                "value.parse",
                f"{item_id}.value_raw",
                value_raw,
                "수치 문법(reader-rules#value_grammar)으로 파싱 가능",
                f"value_raw 를 파싱하지 못했다: {exc}",
            )
        if parsed is not None and parsed != value_type:
            row.add(
                "value.type-agrees",
                f"{item_id}.value_type",
                _compact(value_type),
                _compact(parsed),
                "value_type 이 value_raw 의 파싱 결과와 다르다 — 범위·부등호를 스칼라로 뭉갠 경로",
            )

        # 공통 ② 렌더 대조
        if isinstance(value_type, dict):
            try:
                rendered = render_value(value_type, rules)
            except ValueGrammarError as exc:
                rendered = None
                row.add(
                    "value.render",
                    f"{item_id}.value_type",
                    _compact(value_type),
                    "렌더 가능한 value_type",
                    f"value_type 을 렌더하지 못했다: {exc}",
                )
            if rendered is not None and rendered != value_normalized:
                row.add(
                    "value.normalized-agrees",
                    f"{item_id}.value_normalized",
                    value_normalized,
                    rendered,
                    "value_normalized 가 value_type 의 렌더와 다르다",
                )

    # 8. `_en` 한글 재확인 — 스키마가 1차로 막고 여기서 스크립트가 재확인한다(재감수 M-02).
    en_checked = _check_en_slots(row, ctx, index)

    row.extras["fact_classification"] = {
        "quoted_span": {"count": len(quoted_ids), "material_ids": quoted_ids},
        "bibliographic_ids": bibliographic_ids,
        "derived": derived_entries,
        "figure_sourced": figure_entries,
    }
    row.extras["manual_verification_required"] = manual
    row.extras["en_slots_checked"] = en_checked
    return row


def _compact(value) -> str:
    if isinstance(value, dict):
        return "{" + ", ".join(f"{key}: {value[key]}" for key in sorted(value)) + "}"
    return str(value)


def _check_quoted(row: CheckRow, fact: dict, item_id: str) -> None:
    source = fact.get("source") or {}
    quote = source.get("quote") or ""
    span = source.get("value_span") or {}
    value_raw = fact.get("value_raw") or ""
    extracted = _span_text(quote, span)
    if extracted is None:
        row.add(
            "value.span-bounds",
            f"{item_id}.source.value_span",
            f"[{span.get('start')},{span.get('end')}) / quote 길이 {len(quote)}",
            "0 <= start < end <= len(quote)",
            "value_span 이 quote 범위를 벗어난다",
        )
        return
    if extracted != value_raw:
        row.add(
            "value.quoted-span",
            f"{item_id}.value_raw",
            value_raw,
            extracted,
            "value_raw 가 인용 스팬의 바이트와 다르다 — 실재하는 인용문 옆의 날조 수치(재감수 B-04)",
        )


def _check_bibliographic(row: CheckRow, fact: dict, item_id: str, patent: dict) -> None:
    field = (fact.get("bib_source") or {}).get("field")
    path = BIB_FIELDS.get(field)
    if path is None:
        row.add(
            "value.bib-field",
            f"{item_id}.bib_source.field",
            str(field),
            " · ".join(sorted(BIB_FIELDS)),
            "알 수 없는 서지 필드다",
        )
        return
    node = patent
    for key in path:
        node = (node or {}).get(key) if isinstance(node, dict) else None
    if node != (fact.get("value_raw") or ""):
        row.add(
            "value.bibliographic",
            f"{item_id}.value_raw",
            fact.get("value_raw") or "",
            str(node),
            f"서지 복사값이 patent 블록의 {field} 와 다르다",
        )


def _check_derived(
    row: CheckRow,
    fact: dict,
    item_id: str,
    index: SpecIndex,
    non_arithmetic_kinds: tuple = (),
) -> dict:
    derivation = fact.get("derivation") or {}
    formula = derivation.get("formula") or ""
    entry = {
        "material_id": item_id,
        "formula": formula,
        "inputs": [],
        "depth": 1,
    }
    names: dict[str, decimal.Decimal] = {}
    usable = True

    for position, source in enumerate(derivation.get("inputs") or []):
        name = source.get("name")
        locus = f"{item_id}.derivation.inputs[{position}]"
        if "ref" in source:
            ref = source.get("ref")
            target = index.items.get(ref)
            origin = (target or {}).get("origin")
            entry["inputs"].append({"name": name, "ref": ref, "origin": origin})
            if target is None or target.get("kind") != "fact":
                usable = False  # 해소 실패는 read.pointer-resolve 가 보고한다
                continue
            if origin != "quoted":
                row.add(
                    "value.depth-one",
                    f"{locus}.ref",
                    f"{ref} (origin={origin})",
                    "origin=quoted",
                    "파생의 원천은 원문 스팬(quoted)뿐이다 — 깊이 1(재정 N9 · 재감수 M-01)",
                )
                usable = False
                continue
            target_kind = (target.get("value_type") or {}).get("kind")
            if target_kind in non_arithmetic_kinds:
                usable = False
                row.add(
                    "value.input-not-arithmetic",
                    f"{locus}.ref",
                    f"{ref} (value_type.kind={target_kind})",
                    "산술 가능한 value_type(십진 값)",
                    "날짜·식별자는 산식의 입력이 될 수 없다 — 원문 스팬에서 왔다는 사실이 "
                    "그 값을 수로 만들지는 않는다",
                )
                continue
            try:
                names[name] = decimal.Decimal(normalize_number(target.get("value_normalized") or ""))
            except (NormalizeError, decimal.InvalidOperation):
                usable = False
                row.add(
                    "value.input-not-numeric",
                    f"{locus}.ref",
                    str(target.get("value_normalized")),
                    "십진 수치",
                    "참조한 fact 의 value_normalized 를 수치로 읽을 수 없다(범위·부등호는 산식 입력이 될 수 없다)",
                )
        else:
            quote = source.get("quote") or ""
            extracted = _span_text(quote, source.get("value_span") or {})
            entry["inputs"].append(
                {"name": name, "locator": source.get("locator") or "", "origin": "inline-span"}
            )
            if extracted is None:
                usable = False
                row.add(
                    "value.span-bounds",
                    f"{locus}.value_span",
                    f"quote 길이 {len(quote)}",
                    "0 <= start < end <= len(quote)",
                    "산식 입력의 value_span 이 quote 범위를 벗어난다",
                )
                continue
            try:
                names[name] = decimal.Decimal(normalize_number(extracted))
            except (NormalizeError, decimal.InvalidOperation):
                usable = False
                row.add(
                    "value.input-not-numeric",
                    f"{locus}.quote",
                    extracted,
                    "십진 수치",
                    "산식 입력 스팬이 수치가 아니다",
                )

    if not usable:
        return entry

    try:
        result = apply_rounding(evaluate_formula(formula, names), derivation.get("rounding") or {})
        rendered = format_decimal(result)
    except (FormulaError, NormalizeError, decimal.DecimalException) as exc:
        row.add(
            "value.formula",
            f"{item_id}.derivation.formula",
            formula,
            "안전 산술식의 평가 성공",
            f"산식을 재계산하지 못했다: {exc}",
        )
        return entry

    # 재계산값은 `fact_classification` 계약(convergence/v0)의 필드가 아니므로 행 부속으로만 남긴다.
    row.extras.setdefault("recomputed", {})[item_id] = rendered
    if rendered != (fact.get("value_normalized") or ""):
        row.add(
            "value.derived-recompute",
            f"{item_id}.value_normalized",
            fact.get("value_normalized") or "",
            rendered,
            f"산식 재계산 결과와 다르다(formula={formula})",
        )
    return entry


def _check_en_slots(row: CheckRow, ctx: CheckContext, index: SpecIndex) -> int:
    hangul = _hangul_regex(ctx.schema)
    checked = 0
    for item_id, item in index.items.items():
        for field in EN_SLOTS.get(item.get("kind"), ()):
            value = item.get(field)
            if not isinstance(value, str):
                continue
            checked += 1
            if hangul.search(value):
                row.add(
                    "value.en-only",
                    f"{item_id}.{field}",
                    value,
                    "한글 없는 EN 값",
                    "값 언어 EN 단일 정책 위반(재정 R2 · 재감수 M-02)",
                )
    claims = ctx.spec.get("claims") or {}
    for position, interest in enumerate(claims.get("applicant_interest") or []):
        value = interest.get("signal")
        if not isinstance(value, str):
            continue
        checked += 1
        if hangul.search(value):
            row.add(
                "value.en-only",
                f"claims.applicant_interest[{position}].signal",
                value,
                "한글 없는 EN 값",
                "값 언어 EN 단일 정책 위반(재정 R2 · 재감수 M-02)",
            )
    return checked
