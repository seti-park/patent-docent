# -*- coding: utf-8 -*-
"""봉투 배제와 경계 기각의 pytest — 재정 P-B 잔여(수치 전수 수확)의 반증대.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다.

이 파일의 전제는 통주 2 의 자기 실측이다 — `runs/openai-us20260147854a1-cim-fp-2` 의
`origin: quoted` **30건 중 23건이 오파싱 아티팩트**였고, 계열은 정확히 넷이었다.

  · FP 3항 표기 `FP8 (1-5-2)` → `range` 로 9건 (셋째 필드는 **기록 없이 소실**)
  · 비트 슬라이스 `Act 0 <6:3>` → `inequality`+`scalar` 로 8건
  · 도면·표 번호 `Table 2` · `FIG. **60**` → `scalar` 로 4건
  · 아래첨자 인덱스 `C.sub.j−1` → `scalar` 로 2건 (마이너스가 U+2212 라 경계 기각을 피했다)

그래서 이 파일은 **양방향**으로 잰다. 배제가 배제되는가만 재면 절반이다 — 배제가
**진짜 수치를 먹으면 그것이 더 큰 결함**이므로, 같은 시험에서 살아남아야 할 일곱 어형
(`2, 3, 4, or 5` · `5, 4, 3 or 2` · `12 columns` · `4, 3, and 2`)을 함께 본다.

★ 2026-08-19 (재정 S7) — 계열이 **둘 늘었다**(`figure-or-table-number-list` ·
`row-column-coordinate`). 이 파일의 "넷"은 **통주 2 시점의 사실**이며 현재의 계수가 아니다.
같은 날 후속 보수로 `row-column-coordinate` 는 봉투가 아니라 **토큰 조건 규칙**이 되었다 —
봉투가 구간과 겹치는 진짜 값(`a column 12 mm wide` 의 `12 mm`)을 함께 삼키는 것이 감수
C′-1·D 에서 독립으로 실증되었기 때문이다. 그래서 지금 `match: enclosing-pattern` 은 **5종**
이고, 이 파일의 봉투 반증(`test_removing_the_envelope_patterns_kills_the_load`)이 덮지 못하게
된 자리는 `test_removing_the_preceding_pattern_kills_the_load` 가 새로 진다.
신설 둘의 반증대는 `tests/test_m17_rules.py` 와 반례 golden
`ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples` 에 있고, 이 파일이
지는 몫은 **그 신설이 이 핀 런의 계수를 건드리지 않았다는 실측**이다(아래 사유별 전량 등식).

`assert` 를 쓰지 않는다 — 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고한다
(CLAUDE.md §3 · `tests/test_m1_reader.py` 와 같은 규율).
"""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.render.material_spec_md import ANSWER_SCOPE_TEXT  # noqa: E402
from reader.lib.harvest import harvest_numeric_facts  # noqa: E402
from reader.lib.rules import DEFAULT_RULES_PATH, Rules, RulesError  # noqa: E402

RULES = Rules.load()

# 실특허 통주 런(재정 P-9 의 1급 산출물이 나온 그 런). **읽기 전용**이다 — 구 커밋의 런이며
# 이 레인의 소관이 아니다. 읽어서 복사한 뒤 그 복사본에 현행 수확기를 돌린다.
RUN_SPEC = os.path.join(
    REPO, "runs", "openai-us20260147854a1-cim-fp-2", "10-read", "material-spec.json"
)


def spec_with(quote: str) -> dict:
    """인용문 1건만 든 최소 명세. 수확기가 훑는 것은 접지 인용뿐이다."""
    return {
        "items": [
            {
                "id": "M1",
                "kind": "grounding",
                "status": "active",
                "component": "M0",
                "spec_refs": [{"locator": "[0001]", "quote": quote}],
            }
        ]
    }


def harvest(quote: str) -> tuple[list[dict], list[dict]]:
    """인용문 1건을 수확한다. 반환 = `(quoted fact 들, 거두지 못한 자리들)`."""
    facts, skipped = harvest_numeric_facts(spec_with(quote), rules=RULES)
    return [fact for fact in facts if fact.get("origin") == "quoted"], skipped


def raw_values(facts: list[dict]) -> list[str]:
    return [str(fact.get("value_raw")) for fact in facts]


def reasons(skipped: list[dict]) -> list[str]:
    return [str(entry.get("reason")) for entry in skipped]


# ---------------------------------------------------------------------------
# ① 배제 — 좌표 표현 4계열이 정답지에 오르지 않는다 (2026-08-18 시점의 넷 · 현재 목록은 6종)
# ---------------------------------------------------------------------------

# 통주 2 의 **실물 문자열**이다. 손으로 다듬은 표본을 쓰면 "우리가 만든 판에서만 도는" 규칙이
# 되고, 그것이 합성 픽스처가 실물 표기 변이를 가렸던 M1 스모크의 재발이다.
COORDINATE_SAMPLES = [
    (
        "For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); "
        "FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes "
        "FP4 (1-2-1), FP (1-1-2).",
        "coordinate-triple",
        7,
    ),
    (
        "half adders can be used to add the exponent bits of the activation value "
        "Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> "
        "(simplified as W0 <4:2>).",
        "bit-slice",
        3,
    ),
    (
        "Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats.",
        "figure-or-table-number",
        2,
    ),
    (
        "FIG. **3** illustrates a block diagram of an exemplary column cell.",
        "figure-or-table-number",
        1,
    ),
    (
        "A second multiplexer selects zero or a prior stage carry-out bit C.sub.j−1 "
        "from a prior stage half adder.",
        "subscript-index",
        1,
    ),
    (
        "selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder.",
        "subscript-index",
        1,
    ),
]


@pytest.mark.parametrize("quote,label,envelopes", COORDINATE_SAMPLES)
def test_coordinate_expressions_are_excluded(quote: str, label: str, envelopes: int) -> None:
    """이 배제가 없으면 `1-5`(=1 이상 5 이하)처럼 원문이 하지 않은 주장이 정답지에 심긴다."""
    facts, skipped = harvest(quote)
    if facts:
        pytest.fail(f"좌표 표현에서 수치가 수확됐다: {raw_values(facts)}")
    counted = reasons(skipped).count(label)
    if counted != envelopes:
        pytest.fail(
            f"봉투 배제 기록이 기대와 다르다 — {label} 기대 {envelopes}건, 실제 {counted}건 "
            f"(전체 {reasons(skipped)})"
        )


def test_third_field_of_a_format_triple_is_no_longer_lost_in_silence() -> None:
    """★ 이 시험이 없으면 "시끄럽게 실패한다"가 이 자리에서만 거짓인 채로 남는다.

    `(1-5-2)` 의 셋째 필드는 오파싱이 아니라 **기록 없이 사라지던** 값이었다 — 선행 부호를
    포함한 scalar 가 `-2` 로 잡히고 왼쪽 이웃이 숫자라 기각되는데, 그 기각이 `continue`
    하나여서 `skipped[]` 에 아무것도 남지 않았다.
    """
    facts, skipped = harvest("FP8 (1-5-2) is one of the supported formats.")
    if facts:
        pytest.fail(f"좌표 표현이 수확됐다: {raw_values(facts)}")
    if not skipped:
        pytest.fail("배제도 기각도 기록되지 않았다 — 침묵으로 줄어든 전수는 전수가 아니다")
    tokens = [entry["token"] for entry in skipped if entry["reason"] == "coordinate-triple"]
    if tokens != ["(1-5-2)"]:
        pytest.fail(f"봉투 전문이 기록되지 않았다: {skipped}")


def test_boundary_rejections_are_counted() -> None:
    """경계 기각이 기록되지 않으면 CP1 §12.3 이 "무엇이 빠졌는가"를 절반만 말한다."""
    left, _ = harvest("the volume is 25 cm3 in one arrangement")
    if raw_values(left) != ["25"]:
        pytest.fail(f"`cm3` 의 `3` 이 수치로 새거나 `25` 가 사라졌다: {raw_values(left)}")
    _, left_skipped = harvest("the volume is 25 cm3 in one arrangement")
    if [entry for entry in left_skipped if entry["reason"] == "boundary-left"] == []:
        pytest.fail(f"왼쪽 경계 기각이 기록되지 않았다: {left_skipped}")

    right, right_skipped = harvest("a 3D printed housing encloses the module")
    if right:
        pytest.fail(f"`3D` 의 `3` 이 수치로 새어 나왔다: {raw_values(right)}")
    if [entry for entry in right_skipped if entry["reason"] == "boundary-right"] == []:
        pytest.fail(f"오른쪽 경계 기각이 기록되지 않았다: {right_skipped}")


def test_one_lost_place_is_recorded_once() -> None:
    """한 자리가 여러 줄로 불어나면 "몇 건이 빠졌는가"의 계수가 오히려 흐려진다."""
    _, skipped = harvest("the label abc12-34 is printed on the housing")
    boundary = [entry for entry in skipped if entry["reason"].startswith("boundary-")]
    if len(boundary) != 1:
        pytest.fail(f"같은 자리가 여러 줄로 기록됐다: {boundary}")


# ---------------------------------------------------------------------------
# ② 반대 방향 — 진짜 수치는 계속 수확된다 (배제가 진짜를 먹으면 더 큰 결함이다)
# ---------------------------------------------------------------------------

# 통주 2 의 진짜 7건이 실제로 든 어형이다. 배제 신설이 이 일곱 중 하나라도 먹으면
# 그 손실은 정답지에서 **조용히** 일어난다 — 빠진 사실을 결함으로 보는 검사는 없다.
SURVIVING_SAMPLES = [
    (
        "disclosed accelerator designs may support activation values with different "
        "counts of exponent bits, such as 2, 3, 4, or 5, by sizing the exponent logic.",
        ["2, 3, 4, or 5"],
    ),
    (
        "the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits",
        ["5, 4, 3 or 2"],
    ),
    (
        "the common cell includes 12 columns and 12 rows, where number 12 is the least "
        "common multiple of number 4, 3, and 2.",
        ["12", "12", "12", "4, 3, and 2"],
    ),
]


@pytest.mark.parametrize("quote,expected", SURVIVING_SAMPLES)
def test_true_numbers_survive_the_new_exclusions(quote: str, expected: list) -> None:
    """배제가 진짜를 먹으면 그 손실은 조용하다 — 빠진 사실을 결함으로 보는 검사가 없다."""
    facts, _ = harvest(quote)
    if raw_values(facts) != expected:
        pytest.fail(f"수확 결과가 기대와 다르다: {raw_values(facts)} != {expected}")


def test_existing_harvest_behaviour_does_not_regress() -> None:
    """앞선 회차가 고친 자리(단위 회수·토큰 내부 기각)가 이번 개정에 밀려 되돌아가면 안 된다."""
    facts, _ = harvest("the hydraulic diameter is 0.08 mm, and the drawings do not mark it")
    if raw_values(facts) != ["0.08 mm"]:
        pytest.fail(f"구두점 앞 단위 회수가 깨졌다: {raw_values(facts)}")
    if facts[0].get("unit") != "mm":
        pytest.fail(f"단위가 붙지 않았다: {facts[0].get('unit')!r}")

    forms, _ = harvest(
        "the thickness is 0.05 to 0.10 mm, the length is at least 12 mm, "
        "and coolant occupies 50 ±5 % of the volume"
    )
    if raw_values(forms) != ["0.05 to 0.10 mm", "at least 12 mm", "50 ±5 %"]:
        pytest.fail(f"복합 어형이 평평해졌다: {raw_values(forms)}")


def test_a_real_range_in_parentheses_is_not_swallowed() -> None:
    """봉투가 넓으면 괄호 안의 진짜 범위까지 먹는다 — 좁게 틀리는 쪽을 골랐다는 선언의 반증대."""
    facts, _ = harvest("the thickness (0.05 to 0.10 mm) is measured at the seam")
    if raw_values(facts) != ["0.05 to 0.10 mm"]:
        pytest.fail(f"괄호 안의 진짜 범위가 사라졌다: {raw_values(facts)}")


# ---------------------------------------------------------------------------
# ③ 규칙 파일이 법을 든다 — 부재는 통과가 아니라 오류다
# ---------------------------------------------------------------------------


def load_rules_from(raw: dict, tmp_path) -> Rules:
    path = os.path.join(str(tmp_path), "reader-rules.yaml")
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(raw, handle, allow_unicode=True)
    return Rules.load(path)


def rules_document() -> dict:
    with open(DEFAULT_RULES_PATH, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_removing_the_envelope_patterns_kills_the_load(tmp_path) -> None:
    """부재가 통과로 읽히면 한 줄을 지우는 것만으로 배제가 조용히 꺼진다(재정 P-B 잔여)."""
    raw = rules_document()
    raw["numeric_harvest"]["exclusions"] = [
        entry
        for entry in raw["numeric_harvest"]["exclusions"]
        if entry.get("match") != "enclosing-pattern"
    ]
    with pytest.raises(RulesError):
        load_rules_from(raw, tmp_path)


def test_removing_the_preceding_pattern_kills_the_load(tmp_path) -> None:
    """부재가 통과로 읽히면 한 줄을 지우는 것만으로 **행·열 좌표 배제**가 조용히 꺼진다.

    ★ 이 자리는 2026-08-19 에 생겼다. `row-column-coordinate` 가 봉투에서 **토큰 조건 규칙**
    으로 바뀌었고(봉투가 `a column 12 mm wide` 의 진짜 `12 mm` 를 함께 삼켰다 — 감수 C′-1·D
    독립 실증), 그 순간 위 `test_removing_the_envelope_patterns_kills_the_load` 의 보호
    범위에서 빠졌다. 형태를 바꾸면서 안전판을 하나 지우면 그것은 교체가 아니라 후퇴다.
    """
    raw = rules_document()
    for entry in raw["numeric_harvest"]["exclusions"]:
        entry.pop("preceding_pattern", None)
    with pytest.raises(RulesError):
        load_rules_from(raw, tmp_path)


def test_removing_the_required_flag_kills_the_load(tmp_path) -> None:
    """선언만 지우고 패턴을 남기는 우회로가 열려 있으면 위 시험은 반쪽이다."""
    raw = rules_document()
    raw["numeric_harvest"].pop("enclosing_exclusions", None)
    with pytest.raises(RulesError):
        load_rules_from(raw, tmp_path)


def test_removing_the_boundary_labels_kills_the_load(tmp_path) -> None:
    """라벨이 없으면 경계 기각은 다시 이름 없는 `continue` 로 돌아간다."""
    raw = rules_document()
    raw["numeric_harvest"]["token_boundary"].pop("rejection_labels", None)
    with pytest.raises(RulesError):
        load_rules_from(raw, tmp_path)


def test_envelope_patterns_are_not_parsers() -> None:
    """전개를 붙이면 수확기가 FP 표기법의 의미론을 재정 없이 입법하게 된다(D7).

    이름 있는 그룹은 "무엇을 뽑아 쓰겠다"는 선언이다. 이 목록은 좌표를 **해석하지 않고
    있는지만 보므로** 그런 선언이 있어서는 안 된다.
    """
    for entry in RULES.harvest_envelope_patterns:
        if entry["pattern"].groupindex:
            pytest.fail(
                f"봉투 패턴 {entry['id']} 에 이름 있는 그룹이 있다: "
                f"{sorted(entry['pattern'].groupindex)}"
            )


def test_surface_scope_text_matches_the_rules_file() -> None:
    """표면 문언이 정본과 어긋나면 CP1 이 "어느 범위의 계수인가"를 틀리게 말한다."""
    scope = rules_document()["numeric_harvest"]["answer_scope"]
    expected = (
        # 선언 순서를 그대로 쓴다 — 정렬하면 표면이 정본의 순서를 다시 쓰게 되고,
        # 그것은 대조가 아니라 두 번째 규칙이 된다.
        f"kind {scope['kind']} · origin ∈ {{{', '.join(scope['origin'])}}} "
        f"· status {scope['status']}"
    )
    if ANSWER_SCOPE_TEXT != expected:
        pytest.fail(
            f"CP1 표면의 범위 표지가 정본과 다르다: {ANSWER_SCOPE_TEXT!r} != {expected!r}"
        )


# ---------------------------------------------------------------------------
# ④ 실특허 재현 — 이 개정의 최종 증거
# ---------------------------------------------------------------------------

