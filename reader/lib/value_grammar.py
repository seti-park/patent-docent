# -*- coding: utf-8 -*-
"""재료 측 수치 문법 — `value_raw` ↔ `value_type` ↔ `value_normalized`.

규칙 정본 = `reader/reader-rules.yaml#value_grammar`. 어형 패턴·우선순위·근사 표지·렌더
서식은 전부 그 파일에서 읽는다(코드에 리터럴 패턴을 두지 않는다).

이 모듈이 막는 것은 하나다 — **범위·부등호·공차를 스칼라로 뭉개 담는 경로**. `fact` 가
`value_normalized` 문자열 하나만 갖던 시절에는 `0.05-0.10 mm` 를 `0.05` 로 적어도 아무도
반증하지 못했고, 그 값이 곧 숫자 게이트의 정답지였다(SPEC §9.28 · 재감수 M-09).
"""

from __future__ import annotations

import re

from .normalize import normalize_number
from .rules import Rules

_RULES: Rules | None = None


class ValueGrammarError(ValueError):
    """파싱 불능 — 어형 미매칭, 단위 불일치, 지원하지 않는 표기."""


def _default_rules() -> Rules:
    global _RULES
    if _RULES is None:
        _RULES = Rules.load()
    return _RULES


def _strip_approximate(text: str, rules: Rules) -> tuple[str, bool]:
    """근사 표지를 떼어내고 `approximate` 를 판정한다.

    `~` 는 `range` 어형의 구분자이기도 하므로 **문자열 맨 앞**에 있을 때만 근사 표지로
    읽는다(`0.05~0.10` 은 범위, `~0.08` 은 근사). 나머지 표지는 위치를 가리지 않는다.
    """
    approximate = False
    result = text
    for source, pattern in rules.approximate_markers:
        while True:
            match = pattern.search(result)
            if not match:
                break
            if source == "~" and match.start() != 0:
                break
            approximate = True
            result = (result[: match.start()] + " " + result[match.end():]).strip()
    return re.sub(r"\s+", " ", result).strip(), approximate


def _strip_unit(text: str, unit: str | None, rules: Rules) -> str:
    """`value_raw` 꼬리의 단위를 잘라낸다. 불일치는 실패다(단위 정본 = `fact.unit`)."""
    if unit is None:
        return text
    unit_text = str(unit).strip()
    if not unit_text:
        return text
    if not text.endswith(unit_text):
        raise ValueGrammarError(
            f"단위가 값과 어긋난다: value_raw={text!r} 의 꼬리가 unit={unit_text!r} 이 아니다"
        )
    return text[: -len(unit_text)].strip()


def _numbers_in(text: str, rules: Rules) -> list[str]:
    return [match.group(0) for match in rules.decimal_pattern.finditer(text)]


def _preprocess(text: str, unit: str | None, rules: Rules) -> str:
    """`value_grammar.preprocess` 를 **파일에 적힌 순서대로** 1회 적용한다."""
    result = text
    for step in rules.value_preprocess:
        if step["op"] == "strip-unit":
            result = _strip_unit(result, unit, rules)
        else:
            result = step["regex"].sub("", result)
    return result.strip()


def parse_value(
    value_raw: str,
    unit: str | None,
    rules: Rules | None = None,
    *,
    expect_kind: str | None = None,
) -> dict:
    """`value_raw` 를 `value_type` 객체로 파싱한다. 실패 시 `ValueGrammarError`.

    `expect_kind` 를 주면 **그 형태만** 시도한다 — 서지 복사 사실처럼 origin 이 이미 값의
    종류를 결정하는 경우에 쓴다(순전히 숫자로 된 공개번호가 scalar 로 읽히는 것을 문법의
    추측이 아니라 호출자의 지식으로 막는다. 규칙 정본 = `value_grammar.origin_kind_binding`).
    """
    active = rules or _default_rules()
    if value_raw is None:
        raise ValueGrammarError("빈 value_raw")
    text = str(value_raw).strip()
    text, approximate = _strip_approximate(text, active)
    text = _preprocess(text, unit, active)
    if not text:
        raise ValueGrammarError(f"전처리 뒤 남은 값이 없다: {value_raw!r}")

    candidates = active.value_forms
    if expect_kind is not None:
        candidates = tuple(form for form in candidates if form["kind"] == expect_kind)
        if not candidates:
            raise ValueGrammarError(f"규칙 파일에 {expect_kind!r} 어형이 없다")

    for form in candidates:
        match = form["compiled"].match(text)
        if not match or match.end() != len(text):
            continue
        return _build_value_type(form, match, text, approximate, active)

    scope = f"{expect_kind} 어형" if expect_kind else "어떤 수치 어형에도"
    raise ValueGrammarError(
        f"{scope} 매칭되지 않는다: {value_raw!r} (전처리 후 {text!r})"
    )


def _build_value_type(
    form: dict,
    match: "re.Match[str]",
    text: str,
    approximate: bool,
    rules: Rules,
) -> dict:
    kind = form["kind"]
    if kind == "scalar":
        return {
            "kind": "scalar",
            "approximate": approximate,
            "value": normalize_number(match.group("value")),
        }
    if kind in ("date", "identifier"):
        # 비수치 2종 — 정규화 대상이 아니다(날짜를 수치로 취급하면 정답지에 없는 수가 생긴다).
        groups = match.groupdict()
        raw = groups.get("value") if groups.get("value") is not None else match.group(0)
        return {"kind": kind, "approximate": approximate, "value": raw}
    if kind == "range":
        low_inclusive, high_inclusive = (
            form.get("inclusivity_default") or [True, True]
        )
        return {
            "kind": "range",
            "approximate": approximate,
            "low": normalize_number(match.group("low")),
            "high": normalize_number(match.group("high")),
            "low_inclusive": bool(low_inclusive),
            "high_inclusive": bool(high_inclusive),
        }
    if kind == "inequality":
        operator = re.sub(r"\s+", " ", match.group("op").strip()).lower()
        direction_map = {
            str(key).lower(): value for key, value in (form.get("direction_map") or {}).items()
        }
        direction = direction_map.get(operator)
        if direction is None:
            raise ValueGrammarError(f"부등호 어형의 방향을 알 수 없다: {operator!r}")
        return {
            "kind": "inequality",
            "approximate": approximate,
            "bound": normalize_number(match.group("bound")),
            "direction": direction,
        }
    if kind == "tolerance":
        percent = match.group("pct")
        return {
            "kind": "tolerance",
            "approximate": approximate,
            "center": normalize_number(match.group("center")),
            "tolerance": normalize_number(match.group("tol")),
            "tolerance_unit": "percent" if percent else "absolute",
        }
    if kind == "set":
        members = [normalize_number(number) for number in _numbers_in(match.group("members"), rules)]
        minimum = int(form.get("min_members", 2))
        if len(members) < minimum:
            raise ValueGrammarError(f"집합 원소가 {minimum} 개 미만이다: {text!r}")
        if len(set(members)) != len(members):
            raise ValueGrammarError(f"집합 원소가 중복된다: {text!r}")
        return {"kind": "set", "approximate": approximate, "members": members}
    raise ValueGrammarError(f"알 수 없는 수치 어형: {kind!r}")


_SET_TEMPLATE = re.compile(r"\}([^{}]+)\{")


def _set_separator(forms: dict) -> str:
    """집합 렌더 구분자를 규칙 파일의 서식(`{m1};{m2};…`)에서 뽑는다.

    코드에 문자를 박지 않는 이유: 이 문자는 MATCH_KEY 구분자(`|`)와 충돌해선 안 된다는
    이유로 한 번 개정되었다(`|` → `;`). 다음 개정도 파일에서 일어나야 한다.
    """
    match = _SET_TEMPLATE.search(str(forms.get("set", "")))
    if not match:
        raise ValueGrammarError("render.forms.set 에서 집합 구분자를 뽑지 못했다")
    return match.group(1)


def render_value(value_type: dict, rules: Rules | None = None) -> str:
    """`value_type` → `value_normalized` 문자열.

    서식 정본 = `reader-rules.yaml#value_grammar.render.forms`. `approximate` 가 참이면
    접두 `~` 를 붙인다 — "약 0.08" 과 "0.08" 은 다른 주장이며 MATCH_KEY 가 섞이면 게이트가
    그 차이를 영원히 보지 못한다.
    """
    active = rules or _default_rules()
    if not isinstance(value_type, dict):
        raise ValueGrammarError(f"value_type 이 객체가 아니다: {value_type!r}")
    kind = value_type.get("kind")
    forms = active.render_forms
    try:
        if kind in ("scalar", "date", "identifier"):
            body = str(forms[kind]).format(value=value_type["value"])
        elif kind == "range":
            body = str(forms["range"]).format(
                low=value_type["low"], high=value_type["high"]
            )
        elif kind == "inequality":
            template = forms["inequality"][value_type["direction"]]
            body = str(template).format(bound=value_type["bound"])
        elif kind == "tolerance":
            template = forms["tolerance"][value_type["tolerance_unit"]]
            body = str(template).format(
                center=value_type["center"], tolerance=value_type["tolerance"]
            )
        elif kind == "set":
            body = _set_separator(forms).join(str(member) for member in value_type["members"])
        else:
            raise ValueGrammarError(f"알 수 없는 value_type.kind: {kind!r}")
    except KeyError as exc:
        raise ValueGrammarError(f"value_type 에 필드가 없다: {exc}") from exc
    prefix = active.render_approximate_prefix if value_type.get("approximate") else ""
    return f"{prefix}{body}"
