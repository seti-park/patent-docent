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

★ **그 범위가 2026-08-18 정정되었다 — 연 4자리는 예외다.** sol 독립 감수 P-2 ⓐ 부분 판정의
처분으로 갈래가 하나 더 붙었다.

  ③ **근접 대조** — 우선권 **관할 코드**와 **연 4자리**가 그 주장의 번호가 나타나는 자리의
     **창 안에** 있는가(`bibliography.priority_window`).

두 규칙이 서는 근거는 실측이다. 실특허 원천의 우선권 행은
`us-provisional-application US [63724151 20241122](tel:63724151 20241122)` 이며 **관할 코드도
연도도 번호 바로 곁에 실재한다** — 연도는 어느 표기 형식에서도 4자리 그대로 나타나므로
"정규화 값이라 원천에 없다"는 논거가 연도에는 성립하지 않는다. 위 ②의 관계 검사만으로는
`priority_claims[].date` 와 `dates.priority` 를 **정합적으로 함께** 위조하는 경로가 열려 있고
(등식이 서므로 통과한다), 관할은 아무도 보지 않아 전부 `KR` 로 바꿔도 통과했다.

대조는 **전역이 아니라 창**으로 한다. `US`·`KR` 두 글자는 긴 명세서 어딘가에 반드시
나타나므로 전역 부분문자열 대조는 어떤 코드든 통과시킨다 — **근접성이 이 검사의 전부다.**
창 폭은 코드가 아니라 규칙 파일이 소유하며 여기서는 읽기만 한다.

대조는 정규화 없이 한다(SPEC §2.6 검사 1 보조 규정과 같은 규율). 이름을 눈으로 옮겨 적으면
반드시 실패하며 **그 실패가 정상 동작이다**.
"""

from __future__ import annotations

from .report import CheckContext, CheckRow
from .rules import Rules, RulesError

CHECK_ID = "read.bibliography"

# `priority_claims[].date` 는 스키마가 `YYYY-MM-DD` 로 닫아 두었으므로 연도는 앞 4자다.
# 형태가 그것을 벗어난 값은 스키마가 먼저 거부한다(이 검사가 형태를 다시 파싱하지 않는 이유).
YEAR_LENGTH = 4


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

    # ⑦⑧ 우선권의 관할·연도 — 번호 **곁**에서 대조한다(2026-08-18 sol 감수 P-2 ⓐ 부분 판정).
    checked += _check_priority_proximity(row, source, rules, priority_claims)

    # ⑨ 최우선일 — C18 이 요구하는 유일한 기계 판정.
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


def _window_spec(rules: Rules) -> tuple[int, int]:
    """창 폭을 규칙 파일에서 읽는다. 코드는 이 값을 **고르지 않는다**.

    키가 없거나 정수가 아니면 통과가 아니라 **입력 오류**로 죽인다(`RulesError`). 여기서
    기본값을 지어내면 창 폭이 조용히 코드로 이주하고, 그때부터 규칙 파일의 diff 는 개정
    이력이 아니게 된다 — B-04 가 적발한 "계약 어디에도 없는 수로 판정한" 형태다.
    """
    window = rules.bibliography.get("priority_window")
    if not isinstance(window, dict):
        raise RulesError("bibliography.priority_window 가 없다(우선권 근접 대조의 창 폭)")
    before, after = window.get("before"), window.get("after")
    if not isinstance(before, int) or not isinstance(after, int) or before < 0 or after < 0:
        raise RulesError(
            "bibliography.priority_window.before/after 가 음이 아닌 정수가 아니다: "
            f"{before!r}/{after!r}"
        )
    return before, after


def _windows_around(source: str, needle: str, before: int, after: int) -> list[str]:
    """`needle` 이 나타나는 **모든** 자리의 창을 돌려준다(창은 needle 자신을 포함한다).

    출현 자리가 여럿이면 그중 하나에서만 맞아도 통과다(`match_any_occurrence`) — 실특허
    원천은 마크다운 `tel:` 링크 때문에 같은 번호가 두 번 나오고, 두 번째 자리에서는 관할
    코드가 창 밖으로 밀린다. 전건 요구는 변환 부산물로 정직한 복사를 벌한다.
    """
    windows: list[str] = []
    position = source.find(needle)
    while position != -1:
        end = position + len(needle)
        windows.append(source[max(0, position - before):end + after])
        position = source.find(needle, position + 1)
    return windows


def _check_priority_proximity(
    row: CheckRow,
    source: str,
    rules: Rules,
    priority_claims,
) -> int:
    """우선권 주장의 관할·연도가 **번호 곁**에 있는가. 반환 = 본 건수.

    ★ 번호가 원천에 없으면 **판정하지 않는다.** 그 결함은 `bib.priority-number-in-source`
    의 관할이며, 한 결함을 두 규칙이 판정하면 어느 검사가 그것을 지키는지 확정할 수 없어진다
    (`value.origin-ownership` 이 같은 판단을 이미 내렸다). 그 대신 대상에서 빠졌다는 사실이
    `checked` 에 드러난다.
    """
    if not isinstance(priority_claims, list):
        return 0
    before, after = _window_spec(rules)
    checked = 0
    for position, entry in enumerate(priority_claims):
        if not isinstance(entry, dict):
            continue
        number = entry.get("number")
        if not isinstance(number, str) or not number or number not in source:
            continue
        windows = _windows_around(source, number, before, after)
        locus = f"patent.priority_claims[{position}]"
        expected = f"{number} 둘레 {before}/{after}자 창 안"

        jurisdiction = entry.get("jurisdiction")
        if isinstance(jurisdiction, str) and jurisdiction:
            checked += 1
            if not any(jurisdiction in window for window in windows):
                row.add(
                    "bib.priority-jurisdiction-in-source",
                    f"{locus}.jurisdiction",
                    f"{jurisdiction} (number={number})",
                    expected,
                    "우선권 관할이 그 번호 곁에 없다 — 어느 나라에 무엇을 걸었는가가 서지면이 "
                    "아니라 레인에서 나왔다. 전역 대조가 아니라 근접 대조인 이유는 두 글자 "
                    "코드가 긴 명세서 어딘가에는 반드시 나타나기 때문이다",
                )

        date = entry.get("date")
        if isinstance(date, str) and len(date) >= YEAR_LENGTH:
            year = date[:YEAR_LENGTH]
            checked += 1
            if not any(year in window for window in windows):
                row.add(
                    "bib.priority-year-in-source",
                    f"{locus}.date",
                    f"{date} (연도={year}, number={number})",
                    expected,
                    "우선권 연도가 그 번호 곁에 없다 — 날짜 전체는 정규화 값이라 원천 표기와 "
                    "다르지만 연 4자리는 어느 표기에서도 그대로다. 최우선일 등식만으로는 두 "
                    "날짜를 정합적으로 함께 위조하는 경로를 막지 못한다",
                )
    return checked


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
