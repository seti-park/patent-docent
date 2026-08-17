# -*- coding: utf-8 -*-
"""`read.dependency-parse` — 종속항 전문 ↔ `depends_on[]`·`dependency_type`.

어형 정본 = `reader/reader-rules.yaml#dependency_citation.forms`(SPEC §2.3 의 5종을 데이터로
옮긴 것). 우선순위 순으로 시도하고 **먼저 매칭된 구간은 소비한다** — `claims 1 to 3` 이
`claim 1` 로 부서지지 않게 하는 유일한 장치가 이 소비 규칙이다.

파싱 불능은 **실패**다(`parse.no-silent-pass`). 읽지 못한 어형을 통과시키면 다중 종속의
논리 형태가 조용히 사라지고, 그것이 구 스칼라 표기가 만들던 손실 그 자체다(재정 R1).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .report import CheckContext, CheckRow
from .rules import Rules
from .spec_io import SpecIndex

CHECK_ID = "read.dependency-parse"

_NUMBER = re.compile(r"\d+")


@dataclass
class CitationParse:
    """종속항 전문 1건의 파싱 결과."""

    numbers: set[int] = field(default_factory=set)
    implied_types: set[str] = field(default_factory=set)
    matches: list[dict] = field(default_factory=list)

    @property
    def parsed(self) -> bool:
        return bool(self.matches)


def _overlaps(span: tuple[int, int], consumed: list[tuple[int, int]]) -> bool:
    start, end = span
    for used_start, used_end in consumed:
        if start < used_end and used_start < end:
            return True
    return False


def parse_citations(text: str, rules: Rules) -> CitationParse:
    """전문에서 인용 청구항 번호를 결정론 파싱한다(어형 rank 순 · 구간 소비)."""
    result = CitationParse()
    consumed: list[tuple[int, int]] = []
    for form in rules.dependency_forms:
        for match in form["pattern"].finditer(text):
            span = (match.start(), match.end())
            if _overlaps(span, consumed):
                continue
            literal = form.get("requires_literal")
            if literal and literal.lower() not in match.group(0).lower():
                continue
            numbers = _expand(form, match)
            if not numbers:
                continue
            consumed.append(span)
            result.numbers.update(numbers)
            if form.get("implies_type"):
                result.implied_types.add(form["implies_type"])
            result.matches.append(
                {
                    "form": form.get("id"),
                    "rank": form.get("rank"),
                    "text": match.group(0),
                    "numbers": sorted(numbers),
                }
            )
    return result


def _expand(form: dict, match: "re.Match[str]") -> set[int]:
    groups = match.groupdict()
    if "lo" in groups and "hi" in groups:
        low = int(groups["lo"])
        high = int(groups["hi"])
        return set(range(low, high + 1))
    if "nums" in groups and groups["nums"] is not None:
        return {int(number) for number in _NUMBER.findall(groups["nums"])}
    if "n" in groups and groups["n"] is not None:
        return {int(groups["n"])}
    return set()


def check(ctx: CheckContext) -> CheckRow:
    """종속항 전량에 대해 파싱 집합·논리 형태를 대조한다."""
    rules: Rules = ctx.rules
    block = rules.dependency_citation
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#dependency_citation",
        ruleset_version=rules.version,
        ruleset_size=len(rules.dependency_forms),
    )
    index = SpecIndex.build(ctx.spec)
    dependents = index.dependents
    row.checked = len(dependents)

    for dependent in dependents:
        claim_id = dependent.get("id", "?")
        text = dependent.get("text_verbatim") or ""
        declared = [str(value) for value in (dependent.get("depends_on") or [])]
        declared_type = dependent.get("dependency_type")
        parsed = parse_citations(text, rules)

        if not parsed.parsed:
            row.add(
                "parse.no-silent-pass",
                f"{claim_id}.text_verbatim",
                text,
                "5종 어형 중 하나에 매칭",
                "종속 인용을 파싱하지 못했다 — 침묵 통과 금지(원문을 첨부한다)",
            )
            continue

        parsed_ids = {f"CL-{number}" for number in parsed.numbers}
        if parsed_ids != set(declared):
            row.add(
                "parse.set-equals",
                f"{claim_id}.depends_on",
                ", ".join(sorted(declared)) or "(빈 배열)",
                ", ".join(sorted(parsed_ids)),
                f"전문 파싱 집합과 depends_on 이 다르다: {text}",
            )

        if declared_type not in parsed.implied_types:
            row.add(
                "parse.type-agrees",
                f"{claim_id}.dependency_type",
                str(declared_type),
                " 또는 ".join(sorted(parsed.implied_types)) or "(어형 미상)",
                f"어형이 함의하는 논리 형태와 선언값이 다르다: {text}",
            )

    return row
