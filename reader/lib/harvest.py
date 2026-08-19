# -*- coding: utf-8 -*-
"""전수 수치 수확 — 접지 스팬에서 수치를 기계가 남김없이 거둔다(재정 2026-08-18 P-B).

이 모듈은 검사가 아니라 **생성기**다. 그럼에도 이식 단위(`reader/`) 안에 사는 이유는
수확이 "특허를 읽는 일"이기 때문이다 — 어떤 문자열이 수치이고 그 값이 무엇인지는 출력
채널(X 스레드)을 모르는 판단이며, historian 도 같은 답을 내야 한다.

**무엇이 바뀌었나.** 구 규정은 ⑤단계 독해 레인이 "중요한 수치"를 골라 등재하게 했다. 그것은
서사가 정답지를 고르는 구조였고, 도면을 선택분만 편집하지 않는 이유(D12 전량 선편집)와 같은
논리로 폐지되었다 — 선택이 생성보다 앞서면 선택되지 않은 것은 존재조차 하지 않게 되고,
나중에 필요해졌을 때 되돌아갈 자리가 없다. 그래서 수확은 **전수**이고, 고르는 일은
함의·포지셔닝의 `numeric_refs` **역참조**가 한다(재정 P-B).

**무엇을 훑는가.** `items[]` 중 `kind == "grounding"` 의 `spec_refs[].quote` **문자열 내부**다.
원천 파일이 아니다 — 재정 문언이 "접지 스팬 기반"이며, 원천을 통째로 훑으면 접지되지 않은
문단의 수치까지 정답지에 올라 `read.verbatim`·`read.coverage` 어느 쪽으로도 뒷받침되지 않는
사실이 된다.

**어떻게 훑는가.** 낱개 십진이 아니라 §4 어형(`value_grammar.forms`)을 **rank 순으로** 적용하고
먼저 매칭된 구간을 소비한다 — 그러지 않으면 `0.05 to 0.10 mm`(range)·`50 ±5 %`(tolerance)가
통째로 사라지고 `at least 12 mm` 가 `12` 로 뭉개진다. 형태를 잃은 수확은 전수가 아니다.
매칭의 좌우에는 토큰 경계를 요구한다 — `cm3` 의 `3` 은 영숫자 토큰의 내부이지 수치가 아니다.

**무엇을 빼는가.** 둘이다. ① 도면부호(`figures[].numerals` ∪ `grounding.figure_refs[].numerals`)는
정답지에 올리지 않는다(SPEC §2.5). ② **좌표 표현 구간**(FP 3항 표기 `(1-5-2)` · 비트 슬라이스
`<6:3>` · 도면·표 번호 `FIG. 60` · 그 번호의 나열 꼬리 `Tables 1 and 2` · 행·열 좌표 `Row 0` ·
아래첨자 인덱스 `.sub.j−1`)은 스캔 **전에** 통째로 표시하고 그 구간과 겹치는 수확을 배제한다.
둘 다 배제한 사실을 `skipped[]` 에 남긴다.

★ ②를 토큰 규칙이 아니라 **구간 규칙**으로 두는 이유(2026-08-18 통주 2 실측): `(1-5-2)` 의
셋째 필드는 매칭이 **생성조차 되지 않는다** — 선행 부호를 포함한 `scalar` 가 `-2` 로 잡히고
왼쪽 이웃이 숫자라 기각되므로 토큰 규칙이 심사할 대상이 없다. 닿지 않는 것은 먼저 표시하는
수밖에 없다. 통주 2 의 `origin: quoted` 30건 중 23건이 그때 관측된 **네 계열**의 오파싱이었다.

★ 계열은 2026-08-19 **재정 S7** 로 여섯이 되었다 — 통주 3 이 남긴 아티팩트 3건(`Tables 1 and 2`
의 뒤 항 · `Row 0` · `Col 0`)의 건별 처분이다. 이 개정의 방향은 **전수성 > 순도**이며, 그래서
두 신설 어형은 좁게 틀리는 쪽으로 설계되고 반례 golden 을 동반한다(재정 S7 의 조건). 목록·패턴·
근거는 전부 규칙 파일에 있고 여기에는 없다 — 이 모듈은 "그 구간의 숫자는 값이 아니라 자리다"
하나만 안다.

**시끄럽게 실패하되 죽이지 않는다.** 정규식에 걸렸으나 값 문법으로 파싱되지 않는 토큰은
수확하지 않고 둘째 반환값에 기록한다. 수확은 검사가 아니므로 스테이지를 멈추지 않지만,
기록하지 않으면 "전수"가 조용히 줄어든다. ★ 그 규율이 **경계 기각에서만 지켜지지 않고
있었다** — 왼쪽·오른쪽 이웃 기각이 `continue` 하나여서 `(1-5-2)` 의 셋째 필드는 오파싱이
아니라 **기록 없이 사라졌다**. 지금은 두 기각도 `boundary-left`·`boundary-right` 로 센다.

규칙 정본 = `reader/reader-rules.yaml#numeric_harvest`. 패턴·라벨 서식·단위 인정 범위·중복
제거 키·서지 필드 표를 여기에 리터럴로 두지 않는다(D7 — 코드가 자기 법을 갖지 않는다).
"""

from __future__ import annotations

from .normalize import UNIT_ALIASES, NormalizeError
from .rules import Rules
from .value_grammar import ValueGrammarError, parse_value, render_value

# 토큰 1건이 값이 되지 못하는 사유는 두 갈래로 온다 — 어형 미매칭(`ValueGrammarError`)과
# 정규화 불능(`NormalizeError`, 예: 과학표기 전개가 자릿수 상한을 넘음). 둘 다 **그 토큰
# 하나의** 실패이며 수확 전체의 실패가 아니다. 여기서 잡지 않으면 원천에 큰 지수 하나가
# 있다는 이유로 스테이지가 죽는다(2026-08-18 구현 중 실측).
_HARVEST_FAILURES = (ValueGrammarError, NormalizeError)

# 수확기가 소유하는 origin 2종(재정 P-B `value.origin-ownership`).
# `derived`·`figure-sourced` 는 레인 소유이며 여기서 만들지 않는다.
HARVESTED_ORIGINS: tuple[str, ...] = ("quoted", "bibliographic")

# 단위 인정 집합은 토큰마다 다시 만들지 않는다(대량 인용에서 비용이 선형으로 는다).
_KNOWN_UNITS: frozenset | None = None


def known_units(rules: Rules | None = None) -> frozenset:
    """단위로 인정하는 문자열 집합(소문자).

    규칙 파일의 `unit_detection.accept` 가 `UNIT_ALIASES` 의 **키와 값** 양쪽을 가리킨다 —
    `um` 과 `µm` 은 같은 단위의 두 표기이지 서로 다른 단위가 아니다. 표에 없는 꼬리
    문자열을 단위로 받지 않는 이유는 그 표가 `contracts/l0-format.yaml` §9 와 같은 답을
    내야 하는 계약이고 그 확장이 입법이기 때문이다(재정 사항).
    """
    global _KNOWN_UNITS
    if _KNOWN_UNITS is None:
        _KNOWN_UNITS = frozenset(
            {str(key).lower() for key in UNIT_ALIASES}
            | {str(value).lower() for value in UNIT_ALIASES.values()}
        )
    if rules is None:
        return _KNOWN_UNITS
    # 인식 어휘는 규칙 파일이 든다 — 정규화 표를 늘리지 않고 "무엇을 단위로 볼 것인가"만
    # 넓힌다(규칙 파일 `unit_detection.accept_why`). 합집합은 규칙 인스턴스에 1회 캐시한다:
    # 토큰마다 다시 만들면 대량 인용에서 비용이 선형으로 는다. 로더(`rules.py`)에서 만들지
    # 않는 이유는 그쪽이 `normalize` 를 import 하면 순환이 되기 때문이다.
    cached = getattr(rules, "_harvest_known_units", None)
    if cached is None:
        cached = _KNOWN_UNITS | rules.harvest_unit_vocabulary
        rules._harvest_known_units = cached
    return cached


def harvest_numeric_facts(
    spec: dict,
    *,
    rules: Rules,
    id_start: int = 1,
) -> tuple[list[dict], list[dict]]:
    """접지 인용과 서지면에서 수치 사실을 전수 수확한다.

    반환 = `(수확된 fact 항목들, 건너뛴 토큰 기록들)`.
    결정론이며 같은 입력에 같은 출력을 낸다 — `value.harvest-parity` 가 이 성질 위에 선다.

    산출 항목의 `id` 는 `M{id_start+i}` 로 **임시 발번**한다. 최종 번호는 조립기가 다시
    매기므로(engine 의 재번호) 여기서의 번호는 순서의 표현일 뿐이다.
    """
    harvested: list[dict] = []
    skipped: list[dict] = []
    seen: set[tuple] = set()
    numerals = _figure_numerals(spec)
    numeral_rule = rules.harvest_exclusion("figure-numeral")
    # 행·열 좌표는 **토큰 조건 규칙**이다(봉투가 아니다 — 규칙 파일 `form_change`).
    # 봉투는 구간과 겹치는 진짜 값을 함께 삼켰다: `a column 12 mm wide` 의 `12 mm`.
    coordinate_rule = rules.harvest_exclusion("row-column-coordinate")
    coordinate_pattern = rules.harvest_preceding_pattern("row-column-coordinate")

    candidates, rejections = _quoted_candidates(spec, rules)
    for entry in candidates:
        key = (
            entry["locator"],
            entry["quote"],
            entry["value_span"]["start"],
            entry["value_span"]["end"],
        )
        if key in seen:
            # 중복 제거(`dedupe_key`) — 같은 인용문이 두 접지 항목에 실려도 값은 한 번이다.
            continue
        seen.add(key)
        if _is_figure_numeral(entry, numerals, numeral_rule):
            # 도면부호는 숫자 전수 대조의 정답지에 오르지 않는다(SPEC §2.5 · 재정 P-B).
            # 조용히 버리지 않고 기록한다 — CP1 이 "무엇이 빠졌는가"를 봐야 한다.
            skipped.append(
                {
                    "locator": entry["locator"],
                    "token": entry["value_raw"],
                    "reason": str(numeral_rule.get("reason_label")),
                }
            )
            continue
        coordinate = _row_column_coordinate_token(entry, coordinate_rule, coordinate_pattern)
        if coordinate is not None:
            # 행·열 좌표는 자리이지 값이 아니다(재정 2026-08-19 S7). 침묵으로 줄이지 않고
            # 봉투 시절과 **같은 사유 라벨·같은 기록 폭**으로 남긴다 — CP1 §12.3 의 계수
            # 어휘가 곧 계약이며, 형태가 바뀌어도 기록은 바뀌지 않아야 한다.
            skipped.append(
                {
                    "locator": entry["locator"],
                    "token": coordinate,
                    "reason": str(coordinate_rule.get("reason_label")),
                }
            )
            continue
        fact = _build_quoted_fact(entry, rules)
        if fact is None:
            skipped.append(
                {
                    "locator": entry["locator"],
                    "token": entry["value_raw"],
                    "reason": entry["reason"],
                }
            )
            continue
        harvested.append(fact)

    # 봉투 배제와 경계 기각은 **값 후보가 되기 전에** 갈린 것들이라 위 반복이 보지 못한다.
    # 뒤에 붙이는 이유는 순서가 결정론이어야 하기 때문이며, 앞뒤 어느 쪽이든 상관없되 한쪽으로
    # 고정되어야 한다 — 섞어 넣으면 같은 명세가 두 번 다른 `skipped[]` 를 낸다.
    skipped.extend(rejections)

    # 서지 수확은 인용 스팬을 갖지 않는다(스키마가 bibliographic 에 `source` 를 금지한다).
    # 순서는 규칙 파일의 `emission_order` 대로 원문 스팬 뒤에 온다.
    for fact, failure in _bibliographic_facts(spec, rules):
        if fact is None:
            skipped.append(failure)
            continue
        harvested.append(fact)

    template = rules.harvest_id_template
    for offset, fact in enumerate(harvested):
        fact["id"] = template.replace("{n}", str(id_start + offset))
    return harvested, skipped


# ---------------------------------------------------------------------------
# 원문 스팬 수확
# ---------------------------------------------------------------------------


def _quoted_candidates(spec: dict, rules: Rules) -> tuple[list[dict], list[dict]]:
    """접지 인용을 훑어 값 후보를 등장 순으로 뽑는다(파싱 전).

    반환 = `(값 후보들, 거두지 못한 자리들)`. 둘째가 생긴 이유는 스캔 단계의 배제·기각이
    지금까지 **아무 기록도 남기지 않았기** 때문이다(2026-08-18 통주 2 실측) — 값이 되기 전에
    사라진 자리는 어느 목록에도 없었고, 그래서 "전수"가 조용히 줄었다.

    ★ 어형 rank 순으로 훑고 **먼저 매칭된 구간은 소비한다**(규칙 파일 `numeric_harvest.scan`).
    낱개 십진만 훑던 초판은 `0.05 to 0.10 mm`(range)·`50 ±5 %`(tolerance)를 통째로 잃고
    `at least 12 mm`(inequality)를 `12` 로 뭉갰다 — 형태를 잃은 수확은 전수가 아니다
    (2026-08-18 총괄 검수 실측). 소비 규칙이 `claims 1 to 3` 을 지키는 종속 파서의 것과 같다.
    """
    out: list[dict] = []
    rejections: list[dict] = []
    # 같은 인용문이 두 접지 항목에 실려도 기각 기록은 한 번이다(값 후보의 `dedupe_key` 와
    # 같은 논리 — 같은 자리를 두 번 세면 §12.3 의 계수가 접지 구조를 반영하게 된다).
    seen_rejects: set[tuple] = set()
    for item in spec.get("items") or []:
        if not isinstance(item, dict) or item.get("kind") != "grounding":
            continue
        item_id = item.get("id") or ""
        for ref in item.get("spec_refs") or []:
            if not isinstance(ref, dict):
                continue
            quote = ref.get("quote")
            if not isinstance(quote, str) or not quote:
                continue
            # 좌표가 비면 지어내지 않고 그 인용을 든 접지 항목의 ID 를 쓴다
            # (규칙 파일 `locator_fallback`).
            locator = ref.get("locator") or item_id
            spans, rejected = _scan_quote(quote, rules)
            for span in spans:
                start, end, unit = span
                out.append(
                    {
                        "locator": str(locator),
                        "quote": quote,
                        "value_span": {"start": start, "end": end},
                        "value_raw": quote[start:end],
                        "unit": unit,
                        "reason": "",
                    }
                )
            for start, end, reason in rejected:
                key = (str(locator), quote, start, end, reason)
                if key in seen_rejects:
                    continue
                seen_rejects.add(key)
                rejections.append(
                    {
                        "locator": str(locator),
                        "token": quote[start:end],
                        "reason": reason,
                    }
                )
    return out, rejections


def _scan_quote(
    quote: str, rules: Rules
) -> tuple[list[tuple[int, int, str | None]], list[tuple[int, int, str]]]:
    """인용문 1건에서 값 스팬을 뽑는다.

    반환 = `(등장 순 (start, end, unit), 등장 순 (start, end, 사유 라벨))`. 둘째가 "거두지
    못한 자리"이며 셋 중 하나에서 온다 — 봉투 배제 · 왼쪽 경계 기각 · 오른쪽 경계 기각.
    """
    # ★ 좌표 표현은 스캔 **전에** 통째로 표시한다(규칙 파일 `enclosing_exclusions`).
    #   토큰 규칙으로는 닿지 않는 자리가 있기 때문이다 — `(1-5-2)` 의 셋째 필드는 매칭이
    #   생성조차 되지 않는다. 표시된 구간은 여기서 한 줄로 기록하고, 그 안의 매칭은 이미
    #   센 자리이므로 다시 세지 않는다.
    masked = _envelope_spans(quote, rules)
    rejected: list[tuple[int, int, str]] = list(masked)
    # `blocked` = 배제·기각으로 이미 처분된 구간. `consumed`(정상 수확 구간)와 갈라 두는
    # 이유는 겹침의 뜻이 다르기 때문이다 — consumed 와 겹치면 **더 긴 어형이 이미 거둔**
    # 자리라 손실이 아니고, blocked 와 겹치면 **이미 기록된 손실**이라 두 번 적지 않는다.
    blocked: list[tuple[int, int]] = [(start, end) for start, end, _ in masked]
    consumed: list[tuple[int, int]] = []
    found: list[tuple[int, int, str | None]] = []
    labels = rules.harvest_boundary_labels
    for form in rules.value_scan_forms:
        for match in form["scan"].finditer(quote):
            start, end = match.start(), match.end()
            if _overlaps((start, end), consumed):
                continue
            if _overlaps((start, end), blocked):
                continue
            # ★ 왼쪽 경계 — 앞이 영숫자면 그 매칭은 토큰의 **내부**다(`cm3` 의 `3`).
            #   수치가 아닌 것을 수치로 올리면 정답지에 없는 값이 하나 생긴다.
            if start > 0 and rules.harvest_left_forbidden.match(quote[start - 1]):
                rejected.append((start, end, labels["left"]))
                blocked.append((start, end))
                continue
            # 단위는 어형 매칭 **뒤**에 붙는다 — 값 스팬이 단위까지 늘어나는 경우가 있다.
            end_with_unit, unit = _unit_after(quote, end, rules)
            if _overlaps((end, end_with_unit), consumed) and end_with_unit != end:
                end_with_unit, unit = end, None
            # ★ 오른쪽 경계 — 뒤에 영문자가 붙어 있는데 그것이 단위로 인정되지 않았다면
            #   역시 토큰의 내부다(`3D` 의 `3`). 단위로 소비된 경우만 살린다.
            if unit is None and end < len(quote) and rules.harvest_right_letter.match(quote[end]):
                rejected.append((start, end, labels["right"]))
                blocked.append((start, end))
                continue
            consumed.append((start, end_with_unit))
            found.append((start, end_with_unit, unit))
    found.sort()
    rejected.sort()
    return found, rejected


def _envelope_spans(quote: str, rules: Rules) -> list[tuple[int, int, str]]:
    """좌표 표현 구간을 등장 순으로 표시한다(규칙 파일이 패턴을 든다).

    겹치는 봉투는 **먼저 시작하는 것**을 남기고 시작이 같으면 **긴 쪽**을 남긴다. 임의
    선택이 아니라 결정론이 필요해서 정한 순서다 — 집합·사전 순회에 기대면 같은 명세가 두 번
    다른 `skipped[]` 를 내고, `value.harvest-parity` 가 서는 결정론이 무너진다.

    이 함수는 좌표를 **해석하지 않는다**. `(1-5-2)` 가 부호 1·지수 5·가수 2 라는 사실은
    여기서 알 바가 아니며, 아는 것은 "그 구간의 숫자들은 값이 아니라 자리다" 하나뿐이다
    (규칙 파일 `enclosing_exclusions.not_a_parser` — 전개를 붙이면 수확기가 표기법을
    입법하게 된다).
    """
    spans: list[tuple[int, int, str]] = []
    for entry in rules.harvest_envelope_patterns:
        for match in entry["pattern"].finditer(quote):
            spans.append((match.start(), match.end(), entry["reason_label"]))
    spans.sort(key=lambda span: (span[0], -span[1], span[2]))
    merged: list[tuple[int, int, str]] = []
    for span in spans:
        if merged and span[0] < merged[-1][1]:
            continue
        merged.append(span)
    return merged


def _overlaps(span: tuple[int, int], consumed: list[tuple[int, int]]) -> bool:
    """이미 소비된 구간과 겹치는가. 겹치면 그 매칭은 버린다(긴 어형 우선)."""
    start, end = span
    for used_start, used_end in consumed:
        if start < used_end and used_start < end:
            return True
    return False


def _figure_numerals(spec: dict) -> frozenset:
    """`figures[].numerals` ∪ 전 `grounding.figure_refs[].numerals`.

    두 자리를 합치는 이유는 도면부호의 정본이 한 곳이 아니기 때문이다 — 도면 목록이 든
    번호와 접지가 실제로 지목한 번호가 다를 수 있고, 어느 쪽이든 도면부호다.
    """
    numerals: set[str] = set()
    for figure in spec.get("figures") or []:
        if isinstance(figure, dict):
            numerals.update(str(value) for value in figure.get("numerals") or [])
    for item in spec.get("items") or []:
        if not isinstance(item, dict) or item.get("kind") != "grounding":
            continue
        for ref in item.get("figure_refs") or []:
            if isinstance(ref, dict):
                numerals.update(str(value) for value in ref.get("numerals") or [])
    return frozenset(numerals)


def _is_figure_numeral(entry: dict, numerals: frozenset, rule: dict | None) -> bool:
    """배제 조건 3항 — 정수 ∧ 단위 없음 ∧ 도면부호 집합에 속함(규칙 파일 `exclusions`).

    셋을 다 요구하는 이유: `0.08` 은 도면부호일 수 없고(소수점), `210 °C` 는 단위가 붙는
    순간 도면부호가 아니라 온도이며, 도면부호 집합에 없는 정수는 그냥 수치다. 조건 하나만
    보면 정직한 수치가 정답지에서 사라진다.
    """
    if rule is None:
        return False
    if entry.get("unit") is not None:
        return False
    token = str(entry.get("value_raw") or "")
    if not token.isdigit():
        return False
    return token in numerals


def _row_column_coordinate_token(entry: dict, rule: dict | None, pattern) -> str | None:
    """배제 조건 3항 — 정수 ∧ 단위 없음 ∧ 선행 문맥이 행·열 낱말(규칙 파일 `exclusions`).

    `Row 0` · `Col 0` 은 CIM 매크로 안의 **자리**이지 값이 아니다. 도면부호 배제가 닿지 않는
    이유는 `0` 이 `figures[].numerals` 에 없기 때문이고, 경계 기각이 닿지 않는 이유는 앞이
    공백이라 토큰 내부가 아니기 때문이다 — 두 기존 방어 사이의 틈이다.

    ★ **이것은 봉투가 아니다**(2026-08-19 보수 — 규칙 파일 `form_change`). 봉투였을 때는
    낱말부터 수까지의 구간을 표시하고 그 구간과 겹치는 수확을 전부 버렸으므로,
    `a column 12 mm wide` 에서 진짜 `12 mm` 가 통째로 사라졌다(감수 C′-1·D 독립 실증).
    조건 규칙은 후보 하나만 보고 **단위를 든 후보를 애초에 제외**하므로 그 손실이 없다.

    ★ 단위표를 여기에 복제하지 않는다 — 수확기가 이미 `unit` 을 판정했고 이 함수는 그
    결과를 읽을 뿐이다. 복제하면 두 벌 중 한 벌은 반드시 낡는다.

    ★ **복합 어형은 걸리지 않는다.** `Rows 0 and 1.` 은 `set` 어형이 `0 and 1` 을 한 값으로
    거두므로 첫 조건(정수)에서 빠진다. 그것을 열려면 조건이 복합 어형의 구성원을 들여다봐야
    하는데, 그것은 규칙 파일 `not_a_parser` 가 금한 자리이므로 재정 사항이다. 남은 구멍은
    반례 golden `rc-0005` 의 `hx-10` 이 기대값으로 못 박아 기록한다.
    """
    if rule is None or pattern is None:
        return None
    if entry.get("unit") is not None:
        return None
    if not str(entry.get("value_raw") or "").isdigit():
        return None
    quote = str(entry.get("quote") or "")
    start = int(entry["value_span"]["start"])
    match = pattern.search(quote[:start])
    if match is None:
        return None
    # 기록하는 것은 낱말까지 포함한 **좌표 라벨 전문**이다(`Row 0`). 값 토큰만 적으면
    # CP1 §12.3 에 `0` 만 남아 무엇이 왜 빠졌는지가 읽는 사람에게 사라진다 — 봉투 시절의
    # 기록 폭을 그대로 잇는다(`enclosing_exclusions.recording` 과 같은 원칙: 기록의 단위는
    # 잃은 **자리**다).
    return quote[match.start() : int(entry["value_span"]["end"])]


def _unit_after(quote: str, position: int, rules: Rules) -> tuple[int, str | None]:
    """토큰 뒤의 단위 후보를 본다. 표에 없으면 단위로 인정하지 않는다.

    반환 = `(값 스팬의 끝, 인정된 단위 또는 None)`. 인정한 경우에만 스팬이 단위까지 늘어난다 —
    인정하지 않은 문자열을 스팬에 넣으면 `value_raw` 가 파싱 불능이 되어 값 자체를 잃는다.
    """
    match = rules.harvest_unit_pattern.match(quote, position)
    if match is None:
        return position, None
    candidate = match.group("unit")
    if not candidate or len(candidate) > rules.harvest_unit_max_length:
        return position, None
    if candidate.lower() not in known_units(rules):
        return position, None
    # 전방탐색(경계)은 소비하지 않으므로 스팬 끝은 단위 토큰의 끝이다.
    return match.start("unit") + len(candidate), candidate


def _build_quoted_fact(entry: dict, rules: Rules) -> dict | None:
    """토큰 후보 1건을 `fact` 항목으로 만든다. 파싱 실패면 None(호출자가 기록한다)."""
    value_raw = entry["value_raw"]
    unit = entry["unit"]
    try:
        value_type = parse_value(value_raw, unit, rules)
        value_normalized = render_value(value_type, rules)
    except _HARVEST_FAILURES as exc:
        entry["reason"] = str(exc)
        return None
    return {
        # id 는 호출자가 등장 순으로 발번한다.
        "id": "",
        "kind": "fact",
        "status": "active",
        "superseded_by": None,
        "label_en": rules.harvest_label_template.format(locator=entry["locator"]),
        "origin": "quoted",
        "value_raw": value_raw,
        "value_normalized": value_normalized,
        "value_type": value_type,
        "unit": unit,
        "machine_verifiable": True,
        "source": {
            "locator": entry["locator"],
            "quote": entry["quote"],
            "value_span": dict(entry["value_span"]),
        },
    }


# ---------------------------------------------------------------------------
# 서지 수확
# ---------------------------------------------------------------------------


def _bibliographic_facts(spec: dict, rules: Rules) -> list[tuple[dict | None, dict]]:
    """`patent` 블록의 서지 4필드를 수확한다.

    `expect_kind` 를 주어 파싱한다 — origin 이 값의 종류를 이미 결정하므로 문법이
    추측하지 않는다(순전히 숫자로 된 공개번호가 scalar 로 읽히면 정답지에 없는 수가 하나
    는다. 규칙 정본 = `value_grammar.origin_kind_binding`).
    """
    patent = spec.get("patent") or {}
    out: list[tuple[dict | None, dict]] = []
    for entry in rules.harvest_bib_fields:
        node = patent
        for key in entry["path"]:
            node = node.get(key) if isinstance(node, dict) else None
        field = entry["field"]
        if not isinstance(node, str) or not node:
            out.append(
                (
                    None,
                    {
                        "locator": field,
                        "token": "(부재)",
                        "reason": "patent 블록에 서지 필드 값이 없다",
                    },
                )
            )
            continue
        try:
            value_type = parse_value(node, None, rules, expect_kind=entry["expect_kind"])
            value_normalized = render_value(value_type, rules)
        except _HARVEST_FAILURES as exc:
            out.append((None, {"locator": field, "token": node, "reason": str(exc)}))
            continue
        out.append(
            (
                {
                    "id": "",
                    "kind": "fact",
                    "status": "active",
                    "superseded_by": None,
                    "label_en": rules.harvest_bib_label_template.format(field=field),
                    "origin": "bibliographic",
                    "value_raw": node,
                    "value_normalized": value_normalized,
                    "value_type": value_type,
                    "unit": None,
                    "machine_verifiable": True,
                    "bib_source": {"field": field},
                },
                {},
            )
        )
    return out


# ---------------------------------------------------------------------------
# 대조 키 (`value.harvest-parity` 가 쓴다)
# ---------------------------------------------------------------------------


def parity_key(fact: dict, rules: Rules) -> tuple | None:
    """수확 동일성 판정의 키. `origin` 이 수확기 소유가 아니면 None.

    키의 구성은 규칙 파일 `numeric_harvest.parity_key` 가 정한다 — 갈래마다 다른 이유는
    서지 수확에 인용 스팬이 없기 때문이며(스키마가 금지한다), 그 자리를 `bib_source.field`
    가 대신한다. 없는 스팬을 지어내지 않는다.
    """
    origin = fact.get("origin")
    paths = rules.harvest_parity_key.get(origin)
    if paths is None:
        return None
    return tuple(_freeze(_at_path(fact, path)) for path in paths)


def identity_key(fact: dict, rules: Rules) -> tuple | None:
    """좌표만으로 된 키. 좌표가 같은데 값이 다르면 그것은 **변조**다."""
    origin = fact.get("origin")
    if origin not in rules.harvest_parity_key:
        return None
    if origin == "bibliographic":
        # 서지 갈래의 좌표는 필드 이름 하나뿐이다.
        return (origin, _freeze(_at_path(fact, "bib_source.field")))
    return tuple(_freeze(_at_path(fact, path)) for path in rules.harvest_identity_key)


def _at_path(node, path: str):
    """`a.b.c` 점 경로로 값을 읽는다. 없으면 None."""
    current = node
    for key in str(path).split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _freeze(value):
    """해시 가능한 형태로 접는다(dict → 정렬된 튜플, list → 튜플)."""
    if isinstance(value, dict):
        return tuple(sorted((key, _freeze(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value
