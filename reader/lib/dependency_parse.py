# -*- coding: utf-8 -*-
"""`read.dependency-parse` — 종속항 전문 ↔ `depends_on[]`·`dependency_type`.

어형 정본 = `reader/reader-rules.yaml#dependency_citation.forms`(SPEC §2.3 과 후속 재정을
데이터로 옮긴 것). 우선순위 순으로 시도하고 **먼저 매칭된 구간은 소비한다** — `claims 1 to 3` 이
`claim 1` 로 부서지지 않게 하는 유일한 장치가 이 소비 규칙이다.

재정 T11-ⓒ 로 숫자 없는 PCT 어형 `all-preceding` 이 늘었다. 이 어형은 본문이 구체 번호를
말하지 않으므로 `1..n-1` 과의 정확 일치를 요구하지 않는다 — 그러면 카테고리 전환형에서 앞의
장치항까지 인용했다고 기계가 지어낸다. 대신 레인이 선언한 값이 선행 집합의 비어 있지 않은
부분집합인지만 `parse.preceding-subset` 으로 판정한다.

파싱 불능은 **실패**다(`parse.no-silent-pass`). 읽지 못한 어형을 통과시키면 다중 종속의
논리 형태가 조용히 사라지고, 그것이 구 스칼라 표기가 만들던 손실 그 자체다(재정 R1).

★ 예외는 하나 — `dependency_type: "unclassified"`(구조 미분류, 재정 P-1). Markush·조건부·
수단항·카테고리 전환은 typed operator 신설이 N14 범위에서 **제외**되면서 "틀린 형태"가
아니라 **읽을 규칙이 없는 구조**가 되었다. 그런 종속항을 판정 대상에 남기면 규칙의 공백이
실제 결함과 같은 모양으로 계상된다. 그래서 셋을 한다: 판정에서 빼고, `checked` 에서 빼고,
**목록에는 전건 남긴다**(`extras["unclassified"]`·`extras["unclassified_detail"]`). 셋 중
마지막이 침묵을 막는 자리다.

미분류가 면제를 주므로 그 면제는 무조건일 수 없다 — 본문에 **구조 표지 어형이 하나도 없는데**
미분류를 선언하면 `parse.unclassified-not-an-escape` 가 실패시킨다(회피 통로 봉쇄).
어형 목록은 `reader-rules.yaml#dependency_citation.unclassified.structure_markers` 가 든다.

★ 그 판정은 **구조를 파싱하지 않고 있는지만 본다.** 재정 P-1 이 typed operator 신설을 N14
범위에서 제외했으므로, 표지 어형에 그룹 포획과 전개를 붙이는 순간 그 제외가 무효가 된다.
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
    preceding: bool = False

    @property
    def parsed(self) -> bool:
        return bool(self.matches)


def _overlaps(span: tuple[int, int], consumed: list[tuple[int, int]]) -> bool:
    start, end = span
    for used_start, used_end in consumed:
        if start < used_end and used_start < end:
            return True
    return False


def parse_citations(
    text: str, rules: Rules, self_number: int | None = None
) -> CitationParse:
    """전문에서 인용 청구항 번호를 결정론 파싱한다(어형 rank 순 · 구간 소비)."""
    # 기본값 None 은 번호를 모르는 호출을 편의상 허용하려는 것이 아니라, 그런 호출에서
    # 위치 기반 어형이 조용히 전개되는 것을 막기 위한 것이다.
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
            numbers = _expand(form, match, self_number)
            if not numbers:
                continue
            if form.get("expands") == "preceding":
                result.preceding = True
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


def _expand(
    form: dict, match: "re.Match[str]", self_number: int | None
) -> set[int]:
    if form.get("expands") == "preceding":
        if self_number is None or self_number < 2:
            return set()
        return set(range(1, self_number))
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


def _self_number(claim_id: str) -> int | None:
    match = re.fullmatch(r"CL-(\d+)", claim_id or "")
    return int(match.group(1)) if match else None


def check(ctx: CheckContext) -> CheckRow:
    """종속항 전량에 대해 파싱 집합·논리 형태를 대조한다."""
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#dependency_citation",
        ruleset_version=rules.version,
        ruleset_size=len(rules.dependency_forms),
    )
    index = SpecIndex.build(ctx.spec)
    dependents = index.dependents
    unclassified_value = rules.unclassified_value()

    # 미분류 표지는 판정 대상에서 빠지되 목록에서는 빠지지 않는다(재정 P-1).
    # `checked` 는 아래에서 판정 대상만 센다 — 전 종속항이 미분류면 checked == 0 이 되고
    # 판정 행이 `vacuous: "empty-target"` 으로 자동 날인된다(그것이 정상 동작이다).
    unclassified: list[str] = []
    unclassified_detail: list[dict] = []
    row.checked = 0

    for dependent in dependents:
        claim_id = dependent.get("id", "?")
        text = dependent.get("text_verbatim") or ""
        declared = [str(value) for value in (dependent.get("depends_on") or [])]
        declared_type = dependent.get("dependency_type")
        self_number = _self_number(claim_id)
        # 형식이 어긋난 id 를 조용히 보정하지 않는다. 번호가 없으면 위치 기반 어형은 전개되지
        # 않고, 다른 어형도 없을 때 기존 경로인 parse.no-silent-pass 가 침묵을 막는다.
        parsed = parse_citations(text, rules, self_number)

        if declared_type == unclassified_value:
            unclassified.append(claim_id)
            # 문언은 그 항목을 신고한 **자기 명세**에서 읽는다. 보고서 조립 층이 조기 국면에서
            # 두 실행의 행을 함께 받게 되면서, 거기서 ID 를 정본 명세 하나에 조회하면 비정본의
            # ID 가 빈 문언이 되어 convergence/v0 의 `minLength: 1` 을 깬다(감사 지적 X-2).
            # 명세를 아는 자리가 문언도 읽는다.
            unclassified_detail.append(
                {
                    "claim": claim_id,
                    "dependency_type": unclassified_value,
                    "text_verbatim": dependent.get("text_verbatim") or "",
                }
            )
            # 회피 통로 봉쇄 — 판정 기준은 **본문의 구조 표지 유무**다.
            #
            # ★ 구 기준(인용 어형의 파싱 가능성)은 폐기되었다(2026-08-18 총괄 정정).
            #   재정 P-1 은 "이 4구조를 **만나면** 표지"라고 적었으므로 표지의 대상은
            #   청구항 **본문의 구조**인데, 구 가드는 인용 어형을 봤다. 두 기준이 다르므로
            #   `of claim 1` 로 정상 인용하는 Markush 종속항이 **재정을 따르면 반드시
            #   실패**했다 — 재정이 명한 사용을 벌하는 규칙이었다.
            markers = rules.structure_markers_in(text)
            if not markers:
                row.add(
                    "parse.unclassified-not-an-escape",
                    f"{claim_id}.dependency_type",
                    unclassified_value,
                    "본문에 구조 표지 어형(Markush·조건부·수단항·카테고리 전환) 1건 이상",
                    "구조 표지가 없는 종속항에 미분류를 선언했다 — 표지는 규칙이 못 읽는 "
                    f"구조를 위한 것이지 읽기 귀찮은 구조를 위한 것이 아니다: {text}",
                )
            continue

        row.checked += 1

        if not parsed.parsed:
            row.add(
                "parse.no-silent-pass",
                f"{claim_id}.text_verbatim",
                text,
                "인용 어형 중 하나에 매칭",
                "종속 인용을 파싱하지 못했다 — 침묵 통과 금지(원문을 첨부한다)",
            )
            continue

        declared_set = set(declared)
        if parsed.preceding:
            # preceding 이 참이면 _expand 가 성공했으므로 self_number 는 반드시 2 이상이다.
            allowed = {f"CL-{number}" for number in range(1, self_number)}
            outside = sorted(declared_set - allowed)
            if not declared_set or outside:
                message = (
                    f"선행 인용인데 depends_on 이 비었다: {text}"
                    if not declared_set
                    else f"선행 범위 밖의 번호: {', '.join(outside)}: {text}"
                )
                row.add(
                    "parse.preceding-subset",
                    f"{claim_id}.depends_on",
                    ", ".join(sorted(declared_set)) or "(빈 배열)",
                    f"CL-1 … CL-{self_number - 1} 의 비어 있지 않은 부분집합",
                    message,
                )
        else:
            parsed_ids = {f"CL-{number}" for number in parsed.numbers}
            if parsed_ids != declared_set:
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

    # 미분류 목록 — CP1 표면과 `convergence.json#unclassified_dependents` 가 이것을 렌더한다.
    # 판정에서 뺀 것을 보고에서까지 빼면 그것이 침묵이다(재정 P-1).
    row.extras["unclassified"] = unclassified
    row.extras["unclassified_detail"] = unclassified_detail
    return row
