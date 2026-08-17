# -*- coding: utf-8 -*-
"""`read.verbatim` — 인용 전량이 원천의 **바이트 정확 부분문자열**인가.

반증 대상 = 독해가 원문을 다듬어 인용하거나 없는 문장을 지어낸 것(SPEC §2.6 검사 1).

★ 정규화를 넣지 않는다(검사 1 보조 규정). 원천은 생성 시 1회 NFC 정규화된 UTF-8 로
고정되고(§1.3), 검사는 그 위에서 추가 정규화 **없이** 비교한다. 공백 접힘·따옴표 치환 같은
"친절한" 정규화를 넣는 순간 검사가 반증할 수 있는 대상이 줄어든다 — NBSP 가 1,700 회 섞인
원천에서 인용을 눈으로 옮겨 적으면 반드시 실패하며, **그 실패가 정상 동작이다**.

청구항 `text_verbatim` 은 파일 전체가 아니라 **자기 청구항 구간 안에서** 찾는다. 구간
파서는 `inventory` 모듈의 것을 재사용한다(파서가 두 벌이 되면 한 벌은 반드시 낡는다).
"""

from __future__ import annotations

from .inventory import find_claim_section
from .report import CheckContext, CheckRow
from .rules import Rules
from .spec_io import SpecIndex

CHECK_ID = "read.verbatim"


def _quote_targets(spec: dict, index: SpecIndex) -> list[tuple[str, str]]:
    """(좌표, 인용문) 목록. 청구항 전문은 별도로 다루므로 여기 담지 않는다."""
    targets: list[tuple[str, str]] = []

    for element_id, element in index.elements.items():
        targets.append((f"{element_id}.text_verbatim", element.get("text_verbatim") or ""))
    for addition_id, addition in index.additions.items():
        targets.append((f"{addition_id}.text_verbatim", addition.get("text_verbatim") or ""))
    for figure_id, figure in index.figures.items():
        targets.append((f"figures.{figure_id}.caption_quote", figure.get("caption_quote") or ""))

    for item_id, item in index.items.items():
        kind = item.get("kind")
        if kind == "component":
            targets.append((f"{item_id}.text_verbatim", item.get("text_verbatim") or ""))
        elif kind == "grounding":
            for position, ref in enumerate(item.get("spec_refs") or []):
                targets.append((f"{item_id}.spec_refs[{position}].quote", ref.get("quote") or ""))
            for position, ref in enumerate(item.get("figure_refs") or []):
                targets.append(
                    (
                        f"{item_id}.figure_refs[{position}].caption_quote",
                        ref.get("caption_quote") or "",
                    )
                )
        elif kind == "fact":
            source = item.get("source") or {}
            if source:
                targets.append((f"{item_id}.source.quote", source.get("quote") or ""))
            derivation = item.get("derivation") or {}
            for position, entry in enumerate(derivation.get("inputs") or []):
                if "quote" in entry:
                    targets.append(
                        (f"{item_id}.derivation.inputs[{position}].quote", entry.get("quote") or "")
                    )
        elif kind == "implication":
            for position, quote in enumerate(item.get("evidence_quotes") or []):
                targets.append((f"{item_id}.evidence_quotes[{position}]", quote or ""))
        elif kind == "positioning":
            for position, quote in enumerate(item.get("quotes") or []):
                targets.append((f"{item_id}.quotes[{position}]", quote or ""))

    return targets


def _span_targets(index: SpecIndex) -> list[tuple[str, str, dict]]:
    """`span` 을 든 인용(= 원천 파일 오프셋 힌트) 목록."""
    out: list[tuple[str, str, dict]] = []
    for item_id, item in index.items.items():
        if item.get("kind") != "grounding":
            continue
        for position, ref in enumerate(item.get("spec_refs") or []):
            span = ref.get("span")
            if isinstance(span, dict):
                out.append((f"{item_id}.spec_refs[{position}]", ref.get("quote") or "", span))
    return out


def check(ctx: CheckContext) -> CheckRow:
    rules: Rules = ctx.rules
    source = ctx.source_text or ""
    row = CheckRow(check_id=CHECK_ID)
    index = SpecIndex.build(ctx.spec)

    # ★ 청구항 전문의 대조 범위 = **청구항 절 전체**(`claim_inventory.section` 이 잘라 준 구간)
    #   이지 개별 청구항 본문이 아니다. 개별 청구항 한정(`CL-5` 자리에 `CL-7` 문장)은
    #   `read.claim-inventory` 의 `inventory.text-in-own-claim` 이 **단독으로** 진다 —
    #   그 규칙의 why 문언이 "일반 verbatim 검사는 파일 전체에서 찾으므로 …"라고 적어 자기
    #   존재 이유를 거기에 두고 있다. 관할이 겹치면 어느 검사가 그 결함을 지키는지 확정할 수
    #   없어진다. verbatim 은 "원문에 있는 말인가"를, inventory 는 "제자리에 있는 말인가"를 본다.
    section = find_claim_section(source, rules) if rules is not None else None
    claim_scope = section.text if section is not None and section.found else None

    checked = 0

    # ① 청구항 전문 — 청구항 절 안에서 찾는다(§2.6 검사 1).
    for claim_id, claim in index.claims.items():
        text = claim.get("text_verbatim") or ""
        checked += 1
        if claim_scope is not None:
            if text not in claim_scope:
                row.add(
                    "verbatim.claim-section",
                    f"{claim_id}.text_verbatim",
                    text,
                    "청구항 절 안의 바이트 정확 부분문자열",
                    "청구항 전문이 청구항 절 안에 없다 — 다듬은 인용이거나 지어낸 문장",
                )
        elif text not in source:
            row.add(
                "verbatim.substring",
                f"{claim_id}.text_verbatim",
                text,
                "원천의 바이트 정확 부분문자열",
                "청구항 전문이 원천에 없다(구간 파싱도 실패 — read.claim-inventory 참조)",
            )

    # ② 나머지 인용 전량 — 파일 전체에서 찾는다.
    for locus, text in _quote_targets(ctx.spec, index):
        checked += 1
        if text not in source:
            row.add(
                "verbatim.substring",
                locus,
                text,
                "원천의 바이트 정확 부분문자열",
                "인용문이 원천에 없다 — 다듬은 인용이거나 지어낸 문장",
            )

    # ③ `span` 힌트 대조. `quote` 가 정본이고 span 은 위치 지목용이므로 별도 결함으로 낸다.
    #    ★ `spec_refs[].span` 은 **바이트 오프셋**이다(SPEC §2.4 — "span 은 {start, end} 바이트
    #    오프셋(source_path 기준)"). `fact.source.value_span`·`derivation.inputs[].value_span` 은
    #    반대로 **quote 내부의 문자 오프셋**이며, 두 규정이 다르다는 것이 계약의 사실이다.
    #    파이썬 문자열을 그대로 슬라이스하면 ASCII 원천에서만 우연히 맞는다.
    source_bytes = source.encode("utf-8")
    for locus, text, span in _span_targets(index):
        start = span.get("start")
        end = span.get("end")
        checked += 1
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        try:
            actual = source_bytes[start:end].decode("utf-8")
        except UnicodeDecodeError as exc:
            row.add(
                "verbatim.span-boundary",
                f"{locus}.span",
                f"바이트 [{start},{end}) — {exc.reason}",
                "문자 경계에 맞는 바이트 오프셋",
                "span 의 바이트 경계가 문자를 쪼갠다 — 위치 지목 힌트로도 쓸 수 없다",
            )
            continue
        if actual != text:
            row.add(
                "verbatim.span",
                f"{locus}.span",
                actual,
                text,
                f"바이트 span [{start},{end}) 의 원문이 quote 와 다르다 — quote 가 정본이고 span 이 어긋났다",
            )

    row.checked = checked
    return row
