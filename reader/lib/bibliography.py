# -*- coding: utf-8 -*-
"""`read.bibliography` — 서지 확장 필드가 서지면에서 결정론 복사되었는가(재정 P-2 ⓐ).

반증 대상 = **자유 기입**이다. 스키마는 형태만 닫는다 — `^[A-Z]{2}$` 를 만족하는 관할 코드는
무한히 지어낼 수 있고, 발명자 이름 목록은 문자열이기만 하면 통과한다. 재정 P-2 ⓐ 가 "전부
서지면에서 결정론 복사"라고 적었으므로, 그 말을 사실로 만드는 검사가 이 자리에 선다.

판정은 두 갈래다.

  ① **원천 대조** — 발명자·출원인·분류 코드·우선권 번호가 원천의 바이트 정확 부분문자열인가.
  ② **자기 정합** — 관할이 번호의 접두인가, 공보 종별이 번호의 접미인가, 최우선일이
     우선권 목록의 최소 날짜인가(C18).

★ **날짜는 원천 부분문자열 검사를 하지 않는다.** `dates.*` 와 `priority_claims[].date` 는
정규화 값(`YYYY-MM-DD`)이고, 서지면의 표기는 `March 11, 2024`·`2024/03/11`·`11.03.2024` 등
발행 기관마다 다르다. 정규화된 문자열이 원천에 그대로 나타날 이유가 없으므로 그런 값에
부분문자열 대조를 걸면 **정직한 복사가 실패**하고, 그 실패를 피하려면 정규화를 포기해야 한다.
그래서 날짜는 대조에서 빼고 대신 **날짜들 사이의 관계**를 본다 — "원천에 있는가"를 못 보는
자리에서 "서로 맞는가"를 보는 것이 이 검사의 형태다(규칙 파일
`bibliography.dates_excluded_why` 가 같은 문언을 든다).

대조는 정규화 없이 한다(SPEC §2.6 검사 1 보조 규정과 같은 규율). 이름을 눈으로 옮겨 적으면
반드시 실패하며 **그 실패가 정상 동작이다**.
"""

from __future__ import annotations

from .report import CheckContext, CheckRow
from .rules import Rules

CHECK_ID = "read.bibliography"


def check(ctx: CheckContext) -> CheckRow:
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#bibliography",
        ruleset_version=rules.version,
        ruleset_size=len(rules.bibliography_rules),
    )
    source = ctx.source_text or ""
    patent = ctx.spec.get("patent") or {}
    checked = 0

    number = patent.get("number") or ""
    jurisdiction = patent.get("jurisdiction")
    kind_code = patent.get("kind_code")

    # ① 관할 접두 — 관할이 번호와 어긋나면 둘 중 하나는 다른 문서의 것이다.
    if isinstance(jurisdiction, str):
        checked += 1
        if not number.startswith(jurisdiction):
            row.add(
                "bib.jurisdiction-prefix",
                "patent.jurisdiction",
                f"{jurisdiction} (number={number})",
                f"number 가 {jurisdiction} 으로 시작",
                "관할 코드가 공보 번호의 접두와 다르다 — 서지면에서 복사한 값이 아니다",
            )

    # ② 공보 종별 접미.
    if isinstance(kind_code, str):
        checked += 1
        if not number.endswith(kind_code):
            row.add(
                "bib.kind-code-suffix",
                "patent.kind_code",
                f"{kind_code} (number={number})",
                f"number 가 {kind_code} 으로 끝남",
                "공보 종별이 번호의 접미와 다르다 — 공개공보인지 등록공보인지를 두 자리가 "
                "서로 다르게 말한다",
            )

    # ③~⑥ 원천 바이트 정확 부분문자열 대조.
    checked += _check_substrings(
        row, source, "bib.inventors-in-source", "patent.inventors",
        patent.get("inventors"), "발명자",
    )
    checked += _check_substrings(
        row, source, "bib.applicants-in-source", "patent.applicants",
        patent.get("applicants"), "출원인",
    )
    classifications = patent.get("classifications") or {}
    for scheme in ("ipc", "cpc"):
        checked += _check_substrings(
            row, source, "bib.classification-in-source",
            f"patent.classifications.{scheme}", classifications.get(scheme),
            f"{scheme.upper()} 분류 코드",
        )
    priority_claims = patent.get("priority_claims") or []
    checked += _check_substrings(
        row, source, "bib.priority-number-in-source", "patent.priority_claims",
        [entry.get("number") for entry in priority_claims if isinstance(entry, dict)],
        "우선권 번호",
    )

    # ⑦ 최우선일 — C18 이 요구하는 유일한 기계 판정.
    dates = patent.get("dates") or {}
    claim_dates = [
        entry.get("date")
        for entry in priority_claims
        if isinstance(entry, dict) and isinstance(entry.get("date"), str)
    ]
    if claim_dates:
        checked += 1
        earliest = min(claim_dates)
        declared = dates.get("priority")
        if declared != earliest:
            row.add(
                "bib.earliest-priority",
                "patent.dates.priority",
                str(declared),
                earliest,
                "최우선일이 우선권 목록의 최소 날짜와 다르다 — 목록과 날짜 중 하나가 "
                "틀렸고, 그 둘이 어긋나면 C18 의 정확성 요건이 문서로만 존재한다",
            )

    row.checked = checked
    return row


def _check_substrings(
    row: CheckRow,
    source: str,
    rule_id: str,
    locus_prefix: str,
    values,
    label: str,
) -> int:
    """목록의 각 문자열이 원천의 바이트 정확 부분문자열인가. 반환 = 본 건수."""
    if not isinstance(values, list):
        return 0
    checked = 0
    for position, value in enumerate(values):
        if not isinstance(value, str) or not value:
            continue
        checked += 1
        if value not in source:
            row.add(
                rule_id,
                f"{locus_prefix}[{position}]",
                value,
                "원천의 바이트 정확 부분문자열",
                f"{label}가 원천에 없다 — 서지면에서 복사한 값이 아니라 지어낸 값이다",
            )
    return checked
