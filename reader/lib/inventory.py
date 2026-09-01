# -*- coding: utf-8 -*-
"""`read.claim-inventory` — 원천 청구항 목록 ↔ 등재분.

왜 필요한가(reader-rules.yaml#claim_inventory.purpose): 커버리지 검사는 **등재된 것들
사이의** 접지만 본다. 청구항 하나가 통째로 빠져도 남은 것들이 서로 잘 접지되어 있으면
통과한다. 원천 쪽 정답 목록을 만드는 것이 이 검사의 유일한 일이다(M0 M12 · 재감수 M-07).

구간을 헤더로 먼저 자르고 그 **안에서만** 청구항 시작을 찾는다 — 구간 직전에 청구항처럼
생긴 `Clause N:` 블록이 수십 개 있는 원천이 실재하기 때문이다(규칙 파일의 실측 함정 ①).

파싱 0건은 통과가 아니라 **실패**다. 대상이 0건이면 아래 대조가 전부 공허하게 통과한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .dependency_parse import parse_citations
from .report import CheckContext, CheckRow
from .rules import Rules
from .spec_io import SpecIndex

CHECK_ID = "read.claim-inventory"

_HEADING_LEVEL = re.compile(r"^(#{1,6})")


@dataclass(frozen=True)
class SourceClaim:
    """원천에서 파싱한 청구항 1건."""

    number: int
    body: str
    start: int
    end: int
    canceled: bool

    @property
    def claim_id(self) -> str:
        return f"CL-{self.number}"


@dataclass(frozen=True)
class ClaimSection:
    """청구항 구간. `found` 가 거짓이면 구간을 찾지 못한 것(환경 오류 계열)."""

    found: bool
    text: str = ""
    start: int = 0
    end: int = 0


def find_claim_section(source_text: str, rules: Rules) -> ClaimSection:
    """청구항 구간을 잘라낸다. 끝 = 같거나 더 높은 수준의 다음 헤더 또는 파일 끝."""
    best = None
    for pattern in rules.inventory_heading_patterns:
        match = pattern.search(source_text)
        if match and (best is None or match.start() < best.start()):
            best = match
    if best is None:
        return ClaimSection(found=False)
    level_match = _HEADING_LEVEL.match(best.group(0))
    level = len(level_match.group(1)) if level_match else 6
    body_start = best.end()
    if body_start < len(source_text) and source_text[body_start] == "\n":
        body_start += 1
    closing = re.compile(rf"^#{{1,{level}}}\s", re.MULTILINE)
    following = closing.search(source_text, body_start)
    body_end = following.start() if following else len(source_text)
    return ClaimSection(
        found=True,
        text=source_text[body_start:body_end],
        start=body_start,
        end=body_end,
    )


def parse_source_claims(source_text: str, rules: Rules) -> list[SourceClaim]:
    """구간 안에서 청구항을 파싱한다. 구간이 없으면 빈 목록(호출자가 실패로 다룬다)."""
    section = find_claim_section(source_text, rules)
    if not section.found:
        return []
    starts = list(rules.inventory_claim_start.finditer(section.text))
    claims: list[SourceClaim] = []
    for position, match in enumerate(starts):
        begin = match.start()
        finish = starts[position + 1].start() if position + 1 < len(starts) else len(section.text)
        body = section.text[begin:finish]
        head = section.text[match.start("head"):finish]
        canceled = bool(rules.inventory_canceled.match(head.strip()))
        claims.append(
            SourceClaim(
                number=int(match.group("number")),
                body=body,
                start=section.start + begin,
                end=section.start + finish,
                canceled=canceled,
            )
        )
    return claims


def claim_body_map(source_text: str, rules: Rules) -> dict[str, str]:
    """`CL-<n>` → 그 청구항의 원문 본문. verbatim 검사가 구간 한정에 쓴다."""
    return {claim.claim_id: claim.body for claim in parse_source_claims(source_text, rules)}


def check(ctx: CheckContext) -> CheckRow:
    """규칙 파일의 7개 판정 규칙을 전부 집행한다."""
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#claim_inventory",
        ruleset_version=rules.version,
        ruleset_size=len(rules.inventory_rules),
    )
    section = find_claim_section(ctx.source_text or "", rules)
    if not section.found:
        # 규칙 파일 `section.on_missing: environment-error`. 여기서는 예외를 던지지 않고
        # 실패 + 표지로 보고한다 — 검사 러너가 다른 행까지 잃지 않게 하되, 침묵은 없다.
        row.extras["environment_error"] = True
        row.add(
            "inventory.section-missing",
            "source.claims-section",
            "(구간 없음)",
            "청구항 구간 헤더",
            "원천에서 청구항 구간을 찾지 못했다 — 환경 오류 계열(입력 원천을 확인한다)",
        )
        return row

    claims = parse_source_claims(ctx.source_text or "", rules)
    row.checked = len(claims)
    row.extras["source_claim_numbers"] = [claim.number for claim in claims]
    row.extras["canceled_numbers"] = [claim.number for claim in claims if claim.canceled]

    if not claims:
        row.add(
            "inventory.non-empty",
            "source.claims-section",
            "0건",
            "1건 이상",
            "청구항 구간에서 청구항을 하나도 파싱하지 못했다 — 공허 통과 금지",
        )
        return row

    seen: dict[int, SourceClaim] = {}
    previous = None
    for claim in claims:
        if claim.number in seen:
            row.add(
                "inventory.unique-numbers",
                f"source.claim {claim.number}",
                f"번호 {claim.number} 재등장",
                "청구항 번호는 1회만 시작",
                "같은 청구항 번호가 두 번 시작한다 — 구간 분할이 틀렸을 수 있다",
            )
        else:
            seen[claim.number] = claim
        if previous is not None and claim.number <= previous:
            row.add(
                "inventory.ascending",
                f"source.claim {claim.number}",
                f"{previous} → {claim.number}",
                "등장 순서대로 증가",
                "청구항 번호가 되돌아갔다 — 구간 분할이 틀렸다는 신호다",
            )
        previous = claim.number

    index = SpecIndex.build(ctx.spec)
    registered = set(index.claims)
    independent_ids = {claim.get("id") for claim in index.independent}
    dependent_ids = {claim.get("id") for claim in index.dependents}

    for number, claim in sorted(seen.items()):
        if claim.canceled:
            continue
        if claim.claim_id not in registered:
            row.add(
                "inventory.registered-superset",
                f"claims.{claim.claim_id}",
                "(미등재)",
                f"{claim.claim_id} 등재",
                f"원천 청구항 {number} 이 재료 명세에 등재되지 않았다",
            )
            continue
        # T11-ⓒ: 자기 번호를 넘겨야 선행 인용 15건을 독립항으로 오판한 자리가 닫힌다.
        citations = parse_citations(claim.body, rules, claim.number)
        if citations.parsed and claim.claim_id not in dependent_ids:
            row.add(
                "inventory.type-agrees",
                f"claims.{claim.claim_id}",
                "independent 로 등재",
                "dependents 로 등재",
                f"원천 청구항 {number} 은 다른 청구항을 인용한다(종속항)",
            )
        if not citations.parsed and claim.claim_id not in independent_ids:
            row.add(
                "inventory.type-agrees",
                f"claims.{claim.claim_id}",
                "dependents 로 등재",
                "independent 로 등재",
                f"원천 청구항 {number} 은 다른 청구항을 인용하지 않는다(독립항)",
            )
        registered_claim = index.claims.get(claim.claim_id) or {}
        text = registered_claim.get("text_verbatim") or ""
        if text and text not in claim.body:
            row.add(
                "inventory.text-in-own-claim",
                f"claims.{claim.claim_id}.text_verbatim",
                text,
                f"청구항 {number} 본문 구간 안의 부분문자열",
                "청구항 전문이 자기 구간 밖에서 왔다 — 청구항 간 교차 오염",
            )

    for claim_id in sorted(registered):
        number = _claim_number(claim_id)
        if number is None or number not in seen:
            row.add(
                "inventory.no-phantom",
                f"claims.{claim_id}",
                claim_id,
                "원천 인벤토리에 존재",
                "원천에 없는 청구항이 등재되었다",
            )

    return row


def _claim_number(claim_id: str) -> int | None:
    match = re.fullmatch(r"CL-(\d+)", claim_id or "")
    return int(match.group(1)) if match else None
