# -*- coding: utf-8 -*-
"""M1.7 독해층 규칙 개정의 반증대 — 재정 2026-08-19 Q1 · Q4 · Q5 ② + 판 0.7.0.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다
(`tests/test_m16_harvest_boundary.py` 와 같은 서식).

이 파일이 지키는 것 넷.

  · **Q1 = 기각** — `comprises/is at least one of …` 는 Markush 가 **아니다**. 어형을 넓히지
    않았다는 사실을 기계가 지킨다. 다음 사람이 "실물이 도달하지 못한다"는 관찰만 보고
    목록을 넓히면 그것이 재정 없는 입법이다(규칙 파일 `legislation_path`).
  · **Q4 = 승인** — 수확 단위 어휘에 `b`(bits) 하나. 단일 문자 단위를 일부러 뺀 원칙의
    **명시적 예외**이며, 두 벌(규칙 파일 ↔ l0-format)이 갈리면 재료와 본문이 다른 MATCH_KEY 를
    만든다.
  · **Q5 ② = ⓑ** — 맨 `when`·`if` 는 구조 표지가 아니다. 명확 구문만이 조건부를 연다.
  · **판 0.7.0** — 검사 판정 기준이 바뀌면 판을 올린다(재정 N15 의 기록 의무). 계약 라인은
    `material-spec/v0` 그대로다(0.x 미동결).

★ 규칙·어휘의 정본은 **파일**이다. 여기에 단위 목록·패턴 목록을 리터럴로 복제하지 않는다 —
사본은 반드시 낡는다. 대조는 전부 파일을 읽어서 한다(`test_normalization_table_matches_l0_contract`
의 선례와 같은 방식).

`assert` 를 쓰지 않고 불일치를 `pytest.fail()` 로 명시 비교와 함께 보고한다(CLAUDE.md §3 ·
이 리포의 기존 테스트 서식).
"""

from __future__ import annotations

import json
import os
import re
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from reader.lib import CheckContext, Rules, load_schema, run_checks  # noqa: E402
from reader.lib.harvest import harvest_numeric_facts  # noqa: E402

RULES_PATH = os.path.join(REPO, "reader", "reader-rules.yaml")
L0_PATH = os.path.join(REPO, "contracts", "l0-format.yaml")
VERSION_PATH = os.path.join(REPO, "reader", "READER-VERSION")
CORPUS_BASE = os.path.join(REPO, "tests", "fixtures", "reader", "base")

# 실특허 통주 3 — 재정 P-13 의 1급 산출물이 나온 그 런. **읽기 전용**이다(이 레인의 소관이
# 아니며, 행위시법상 이 라운드의 개정은 그 런에 소급하지 않는다).
RUN_DIR = os.path.join(REPO, "runs", "openai-us20260147854a1-cim-fp-3")
RUN_SOURCE = os.path.join(RUN_DIR, "00-source", "patent.md")
RUN_SPEC = os.path.join(RUN_DIR, "10-read", "material-spec.json")

RULES = Rules.load()
SCHEMA = load_schema()

with open(RULES_PATH, encoding="utf-8") as _handle:
    RULES_RAW = yaml.safe_load(_handle)
with open(L0_PATH, encoding="utf-8") as _handle:
    L0_RAW = yaml.safe_load(_handle)


# ---------------------------------------------------------------------------
# 공용 — 규칙 파일에서 읽어 오는 자리들 (리터럴 복제 금지)
# ---------------------------------------------------------------------------


def marker_forms() -> list[dict]:
    """`dependency_citation.unclassified.structure_markers.forms` 원본(파싱 전 문자열)."""
    return (
        RULES_RAW["dependency_citation"]["unclassified"]["structure_markers"]["forms"]
    )


def patterns_of(structure: str) -> list[str]:
    for entry in marker_forms():
        if entry.get("structure") == structure:
            return list(entry.get("patterns") or [])
    pytest.fail(f"구조 표지 목록에 `{structure}` 항목이 없다 — 규칙 파일이 무너졌다")
    return []


def unit_vocabulary() -> list[str]:
    return list(RULES_RAW["numeric_harvest"]["unit_detection"]["vocabulary"])


def l0_value_unit_pattern() -> str:
    for entry in L0_RAW["numeric"]["tokenizers"]:
        if entry.get("kind") == "value-unit":
            return str(entry["pattern"])
    pytest.fail("l0-format 의 토큰화 목록에 value-unit 이 없다")
    return ""


def l0_unit_alternatives() -> list[str]:
    """rank 9 패턴 꼬리의 단위 대안 목록. 순서가 곧 매칭 우선순위다(좌측 우선)."""
    pattern = l0_value_unit_pattern()
    match = re.search(r"\(\?:([^()]*)\)\\b\Z", pattern)
    if match is None:
        pytest.fail(f"value-unit 패턴에서 단위 대안 목록을 읽지 못했다: {pattern}")
    return match.group(1).split("|")


def spec_with(quote: str, *, locator: str) -> dict:
    """인용문 1건만 든 최소 명세. 수확기가 훑는 것은 접지 인용뿐이다."""
    return {
        "items": [
            {
                "id": "M1",
                "kind": "grounding",
                "status": "active",
                "component": "M0",
                "spec_refs": [{"locator": locator, "quote": quote}],
            }
        ]
    }


def read_text(path: str) -> str:
    if not os.path.isfile(path):
        pytest.fail(f"실측의 피검체가 없다: {path}")
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# ---------------------------------------------------------------------------
# ① 재정 Q4 — 단위 어휘 `b`(bits)
# ---------------------------------------------------------------------------

# 통주 특허 `[0189]` 의 **실문언 조각**이다. 손으로 다듬은 표본을 쓰면 "우리가 만든 판에서만
# 도는" 규칙이 되고, 그것이 합성 픽스처가 실물 표기 변이를 가렸던 M1 스모크의 재발이다.
BIT_WIDTH_QUOTE = (
    "support activation values and weight values having exponents with 5b, 4b, 3b or 2b"
)


def test_the_bit_width_quote_is_real() -> None:
    """표본이 실물이 아니면 아래 재현은 우리가 지어낸 문장에 대한 재현일 뿐이다."""
    source = read_text(RUN_SOURCE)
    if BIT_WIDTH_QUOTE not in source:
        pytest.fail(
            f"`[0189]` 실문언 조각이 원천에 없다(바이트 정확 대조) — {RUN_SOURCE}"
        )


def test_harvest_recovers_bit_width_units() -> None:
    """★ 재정 Q4 의 실측 재현. 이 시험이 없으면 `5b, 4b, 3b, 2b` 는 다시 **값째로** 사라진다.

    단위로 인정되지 않는 `b` 는 단위를 잃는 사건이 아니라 **값을 잃는 사건**이었다 — 뒤따르는
    영문자가 토큰 내부로 읽혀 매칭 전체가 `boundary-right` 로 기각되기 때문이다. 그래서 이
    테스트는 두 가지를 함께 본다: 넷이 `unit == "b"` 로 수확되는가, 그리고 그 넷에 대한
    경계 기각이 **한 건도 남지 않는가**.
    """
    facts, skipped = harvest_numeric_facts(
        spec_with(BIT_WIDTH_QUOTE, locator="[0189]"), rules=RULES
    )
    quoted = [fact for fact in facts if fact.get("origin") == "quoted"]
    harvested = [
        (fact["value_raw"], fact["unit"], fact["value_normalized"]) for fact in quoted
    ]
    expected = [("5b", "b", "5"), ("4b", "b", "4"), ("3b", "b", "3"), ("2b", "b", "2")]
    if harvested != expected:
        pytest.fail(f"비트 폭 수확이 기대와 다르다 — 기대 {expected}, 실제 {harvested}")

    boundary = [
        entry
        for entry in skipped
        if str(entry.get("reason")) == RULES.harvest_boundary_labels["right"]
    ]
    if boundary:
        pytest.fail(f"단위 `b` 를 인정하고도 오른쪽 경계 기각이 남았다: {boundary}")


def test_unit_vocabulary_and_l0_value_unit_pattern_agree_on_b() -> None:
    """두 벌이 갈리면 재료와 본문이 다른 MATCH_KEY 를 만들어 숫자 전수 대조가 성립하지 않는다.

    (`test_normalization_table_matches_l0_contract` 와 같은 이유의 대조다 — `reader/` 는
    `contracts/` 를 읽지 않으므로 사본이 아니라 **대조**로 묶는다.)
    """
    vocabulary = [str(unit).lower() for unit in unit_vocabulary()]
    alternatives = l0_unit_alternatives()
    lowered = [unit.lower() for unit in alternatives]
    if "b" not in vocabulary:
        pytest.fail(f"규칙 파일의 인식 어휘에 `b` 가 없다: {vocabulary}")
    if "b" not in lowered:
        pytest.fail(f"l0-format rank 9 의 단위 대안에 `b` 가 없다: {alternatives}")

    # 좌측 우선 규율 — `b` 는 자기를 접두로 갖는 긴 표기들보다 **뒤**에 있어야 한다.
    index = lowered.index("b")
    for longer in [unit for unit in lowered if unit != "b" and unit.endswith("b")]:
        if lowered.index(longer) > index:
            pytest.fail(
                f"`{longer}` 가 `b` 보다 뒤에 있다 — 좌측 우선이라 긴 표기가 잘린다: {alternatives}"
            )

    # 행동으로도 확인한다: `5 bits` 는 여전히 `bits` 로 잡히고, `5b` 는 `b` 로 잡힌다.
    compiled = re.compile(l0_value_unit_pattern())
    for text, expected in (("5 bits", "5 bits"), ("5b", "5b"), ("12 Gb", "12 Gb")):
        match = compiled.search(text)
        actual = match.group(0) if match else None
        if actual != expected:
            pytest.fail(f"value-unit 토큰화 {text!r} 기대 {expected!r}, 실제 {actual!r}")

    # 인식 어휘의 확장이지 **정규화 매핑의 신설이 아니다**(재정 문언은 `b` 하나만 말했다).
    aliases = L0_RAW["numeric"]["normalization"]["unit_aliases"]
    if "b" in aliases or "b" in set(aliases.values()):
        pytest.fail(f"`unit_aliases` 가 함께 움직였다 — 별개의 입법이다: {aliases}")


# ---------------------------------------------------------------------------
# ② 재정 Q5 ② — 나표지 제거, 조건부는 명확 구문만
# ---------------------------------------------------------------------------


def real_cl9() -> dict:
    """통주 3 의 CL-9 실물(읽기 전용). 두 독립 실행이 갈린 바로 그 자리다."""
    if not os.path.isfile(RUN_SPEC):
        pytest.fail(f"실특허 런 산출이 없다: {RUN_SPEC} — 실측의 피검체가 사라졌다")
    with open(RUN_SPEC, encoding="utf-8") as handle:
        spec = json.load(handle)
    for claim in spec["claims"]["dependents"]:
        if claim.get("id") == "CL-9":
            return claim
    pytest.fail("통주 3 산출에 CL-9 가 없다")
    return {}


def test_bare_when_is_not_a_structure_marker() -> None:
    """맨 `when`·`if` 가 표지로 남으면 회피 통로가 그대로 열려 있고, CL-9 의 갈림이 되풀이된다.

    피검체는 **실물**이다 — 통주 3 의 CL-9 는 시간 용법 `when`(동시 갱신의 시점) 하나만 들고
    있으면서 `unclassified` 로 선언되었고, 그 선언이 통과한 유일한 이유가 나표지였다.
    개정 후에는 표지가 0건이므로 같은 선언은 `parse.unclassified-not-an-escape` 에 걸린다
    (행위시법 — 그 런에는 소급하지 않는다).
    """
    claim = real_cl9()
    if claim.get("dependency_type") != "unclassified":
        pytest.fail(
            f"CL-9 의 선언이 `unclassified` 가 아니다: {claim.get('dependency_type')} — "
            "이 시험이 겨누는 자리가 사라졌다"
        )
    found = RULES.structure_markers_in(claim["text_verbatim"])
    if found:
        pytest.fail(f"시간 용법 `when` 이 여전히 구조 표지로 잡힌다: {found}")

    # 나표지 두 개가 실제로 목록에서 빠졌는가(문자열 동일성으로 본다 — `if … then` 은
    # `\bif\b` 를 부분문자열로 갖지만 그것은 별개의 어형이다).
    bare = [pattern for pattern in patterns_of("조건부") if pattern in (r"\bif\b", r"\bwhen\b")]
    if bare:
        pytest.fail(f"나표지가 목록에 남아 있다: {bare}")


def test_bare_when_declaration_is_now_rejected_end_to_end() -> None:
    """표지 목록만 보면 `parse.unclassified-not-an-escape` 가 실제로 그 선언을 벌하는지 알 수 없다.

    ★ 양방향으로 잰다 — 나표지뿐인 선언은 **실패**하고, 명확 구문을 든 선언은 **통과**한다.
    한쪽만 보이면 과잉 제약과 구별되지 않는다.
    """
    temporal = (
        "The stacked thermal module of claim 1, wherein the fluid channel is sealed "
        "when the module is assembled."
    )
    explicit = (
        "The stacked thermal module of claim 1, wherein the fluid channel is sealed "
        "in response to a pressure signal."
    )
    for text, should_fail in ((temporal, True), (explicit, False)):
        row = run_dependency_parse(text)
        rules_hit = {finding.rule for finding in row.findings}
        hit = "parse.unclassified-not-an-escape" in rules_hit
        if hit != should_fail:
            pytest.fail(
                f"기대 {'실패' if should_fail else '통과'} 인데 결과가 반대다 — "
                f"본문={text!r} · status={row.status} · 결함={sorted(rules_hit)}"
            )


def run_dependency_parse(text: str):
    """코퍼스 기준본의 CL-2 를 `unclassified` 로 선언하고 그 본문만 갈아 끼운다."""
    with open(os.path.join(CORPUS_BASE, "material-spec.json"), encoding="utf-8") as handle:
        spec = json.load(handle)
    source = read_text(os.path.join(CORPUS_BASE, "patent.md"))
    dependent = spec["claims"]["dependents"][0]
    if dependent.get("id") != "CL-2":
        pytest.fail(f"기준본의 첫 종속항이 CL-2 가 아니다: {dependent.get('id')}")
    dependent["dependency_type"] = "unclassified"
    dependent["text_verbatim"] = text
    dependent["depends_on"] = ["CL-1"]
    ctx = CheckContext(spec=spec, source_text=source, rules=RULES, schema=SCHEMA)
    return run_checks.CHECK_REGISTRY["read.dependency-parse"](ctx)


EXPLICIT_CONDITIONAL_SAMPLES = [
    (
        "in response to",
        "The apparatus of claim 1, wherein the controller opens the valve in response to "
        "a pressure signal.",
    ),
    (
        "if … then",
        "The apparatus of claim 1, wherein if the temperature exceeds a threshold then "
        "the controller opens the valve.",
    ),
    (
        "only when",
        "The apparatus of claim 1, wherein the controller opens the valve only when the "
        "pressure exceeds a threshold.",
    ),
    (
        "unless",
        "The apparatus of claim 1, wherein the controller keeps the valve open unless the "
        "pressure drops below a threshold.",
    ),
]


@pytest.mark.parametrize("label,text", EXPLICIT_CONDITIONAL_SAMPLES)
def test_explicit_conditional_forms_are_markers(label: str, text: str) -> None:
    """명확 구문까지 잡지 못하면 조건부 구조는 표지 없는 구조가 되고, 정직한 미분류 선언이 전건 벌받는다."""
    found = RULES.structure_markers_in(text)
    if "조건부" not in found:
        pytest.fail(f"명확 구문 `{label}` 이 조건부 표지로 잡히지 않았다: {found} — {text!r}")


# ---------------------------------------------------------------------------
# ③ 재정 Q1 = 기각 — Markush 어형을 넓히지 않았다
# ---------------------------------------------------------------------------


def test_markush_forms_were_not_widened() -> None:
    """★ 재정 Q1 = **기각**의 기계 집행.

    이 시험이 없으면 규칙 파일의 실측 데이터(`comprises/is at least one of …` 가 표지에
    도달하지 못한다)를 읽은 다음 사람이 그 관찰만 보고 목록을 넓히게 된다 — 재정은 그 판단을
    **기각**했으므로, 넓히는 순간 그것은 재정 없는 입법이다.
    """
    markush = patterns_of("Markush")
    if len(markush) != 2:
        pytest.fail(f"Markush 어형이 2형태가 아니다: {markush}")

    # 어형 목록 **전체**에 `at least one of` 계열이 없다(다른 구조 아래로 숨어 들어가는 경로도 막는다).
    for entry in marker_forms():
        for pattern in entry.get("patterns") or []:
            if "at least one of" in str(pattern):
                pytest.fail(
                    f"기각된 어형이 `{entry.get('structure')}` 아래 표지로 들어와 있다: {pattern}"
                )

    # 행동 확인 — 실물 어형(통주 특허 청구항 10·11·19 계열)은 표지를 만들지 않는다.
    rejected_form = (
        "The hardware accelerator of claim 1, wherein the first data format comprises "
        "at least one of an integer format, a floating point format and a block format."
    )
    found = RULES.structure_markers_in(rejected_form)
    if found:
        pytest.fail(f"기각된 어형이 표지로 잡힌다: {found} — 재정 Q1 이 뒤집혔다")


# ---------------------------------------------------------------------------
# ④ 판 0.7.0 — 검사 판정 기준이 바뀌면 판을 올린다(재정 N15)
# ---------------------------------------------------------------------------


def test_reader_version_is_0_7_0_and_contract_line_stays_v0() -> None:
    """판을 올리지 않으면 "무엇이 언제 바뀌었는가"가 사라지고, 라인을 올리면 0.x 미동결 규율이 깨진다."""
    version = read_text(VERSION_PATH).strip()
    if version != "0.7.0":
        pytest.fail(f"READER-VERSION={version!r} (기대 '0.7.0')")

    line = SCHEMA["properties"]["schema"]["const"]
    if line != "material-spec/v0":
        pytest.fail(f"계약 라인이 승격됐다: {line} — 0.x 미동결 구간의 minor 상향이다(재정 N15)")

    root_comment = SCHEMA["$comment"]
    if "reader_version = 0.7.0" not in root_comment:
        pytest.fail("스키마 루트 $comment 가 현재 판을 0.7.0 으로 적지 않았다")
    if "판 0.7.0" not in root_comment:
        pytest.fail("판 0.7.0 이 바꾼 것의 기록이 스키마에 없다 — 0.x 의 자유는 기록 없는 자유가 아니다")
    property_comment = SCHEMA["properties"]["reader_version"]["$comment"]
    if '"0.7.0"' not in property_comment:
        pytest.fail(f"reader_version property 의 $comment 가 낡았다: {property_comment}")
