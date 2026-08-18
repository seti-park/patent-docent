# -*- coding: utf-8 -*-
"""우선권 근접 대조 2종의 pytest — sol 감수 P-2 ⓐ **부분 판정**의 반증대.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다.

감수 원문(`docs/lessons/2026-08-18-sol-audit-m15-full.md` P-2 ⓐ)이 실측한 것과, 총괄이
독립 재현한 것(`docs/decisions/D-20260818-04-m1-close.md` §5.3)이 이 파일의 전제다.

  · 우선권 **관할** 미대조 = 실재 공백. 실특허 런의 관할을 전부 `KR` 로 바꿔도
    `read.bibliography` 는 **pass · checked=16** 이었다.
  · 우선권 **날짜** 미대조 = 감수의 절반은 실측과 달랐다. 전부 `1900-01-01` 로 바꾸면
    `bib.earliest-priority` 가 운다. **그러나 두 날짜를 정합적으로 함께 위조하면 통과한다** —
    관계만 보는 검사는 관계를 지킨 거짓을 막지 못한다.

그래서 이 파일은 **실특허 런의 실물 산출**을 읽어 복사한 뒤 변조한다. 합성 픽스처만으로는
"감수자가 본 그 판정이 뒤집혔는가"를 증명할 수 없기 때문이다. 원본 런 파일은 **읽기만**
한다(구 커밋의 런이며 이 레인의 소관이 아니다).

`assert` 를 쓰지 않는다 — 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고한다
(CLAUDE.md §3 · `tests/test_m1_reader.py` 와 같은 규율).
"""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from reader.lib import CheckContext, Rules, load_schema, run_checks  # noqa: E402
from reader.lib.rules import DEFAULT_RULES_PATH, RulesError  # noqa: E402

CHECK_ID = "read.bibliography"
JURISDICTION_RULE = "bib.priority-jurisdiction-in-source"
YEAR_RULE = "bib.priority-year-in-source"
NUMBER_RULE = "bib.priority-number-in-source"
EARLIEST_RULE = "bib.earliest-priority"

# 실특허 통주 런(재정 P-9의 1급 산출물이 나온 그 런). **읽기 전용**이다.
RUN_DIR = os.path.join(REPO, "runs", "openai-us20260147854a1-cim-fp-2")
RUN_SPEC = os.path.join(RUN_DIR, "10-read", "material-spec.json")
RUN_SOURCE = os.path.join(RUN_DIR, "00-source", "patent.md")

RULES = Rules.load()
SCHEMA = load_schema()

# 코퍼스 — 이 레인이 더한 변조본 2건의 **규칙 수준** 결박(도구는 검사 수준까지만 본다).
CORPUS = os.path.join(REPO, "tests", "fixtures", "reader")


def _load_run() -> tuple[dict, str]:
    """실특허 런의 재료 명세와 원천을 읽는다. 없으면 건너뛰지 않고 **실패**한다.

    skip 으로 처리하면 감수 재현이 조용히 사라진다 — 이 파일의 존재 이유가 그 재현이다.
    """
    for path in (RUN_SPEC, RUN_SOURCE):
        if not os.path.isfile(path):
            pytest.fail(f"실특허 런 산출이 없다: {path} — 감수 재현의 피검체가 사라졌다")
    with open(RUN_SPEC, encoding="utf-8") as handle:
        spec = json.load(handle)
    with open(RUN_SOURCE, encoding="utf-8") as handle:
        source = handle.read()
    return spec, source


RUN_SPEC_DATA, RUN_SOURCE_TEXT = _load_run()


def run_bibliography(spec: dict, source: str, rules: Rules = RULES):
    """`read.bibliography` 한 행만 낸다."""
    ctx = CheckContext(spec=spec, source_text=source, rules=rules, schema=SCHEMA)
    return run_checks.CHECK_REGISTRY[CHECK_ID](ctx)


def run_all_read(spec: dict, source: str) -> list:
    """READ 검사 전종. "이 규칙만 우는가"를 보려면 옆 검사들도 함께 봐야 한다."""
    ctx = CheckContext(spec=spec, source_text=source, rules=RULES, schema=SCHEMA)
    return list(run_checks.run_read_checks(ctx))


# ★ 기준선 예외 1건 (2026-08-18 봉투 배제 신설 — 재정 P-B 잔여).
#   이 런은 **봉투 배제 이전 커밋에 결박**되어 있고(행위시법 — 재정 P-U1·P-8), 그 시점의
#   수확기는 좌표 표현(`FP8 (1-5-2)` · `Act 0 <6:3>` · `FIG. 60` · `C.sub.j−1`)을 수치로
#   읽었다. 그래서 동결된 명세는 그 23건을 들고 있고, **지금의** 수확기로 다시 훑으면
#   `value.harvest-parity` 가 그것을 [추가]로 신고한다. 그 신고는 옳다 — 옛 산출이 새 법에
#   맞지 않는다는 사실의 정확한 기술이며, 런을 고쳐서 지울 것이 아니다(원본은 읽기 전용).
#   그러므로 이 파일은 그 한 검사만 예외로 두되 **범위를 좁혀** 둔다: 아래 헬퍼가
#   "이 실패가 정말 그 표류인가"(전 결함이 value.harvest-parity 의 [추가]인가)를 확인하며,
#   다른 규칙이 섞이는 순간 예외는 성립하지 않는다.
PINNED_HARVEST_DRIFT = "read.value-derivation"


def is_pinned_harvest_drift(row) -> bool:
    """이 실패가 "핀 커밋의 옛 수확본 ↔ 현행 수확기" 표류인가.

    표류가 아닌 결함(값 파싱·산식 재계산·정규화 불일치)이 하나라도 섞이면 False 다 —
    예외의 폭이 넓어지면 예외가 곧 은폐가 된다.
    """
    if row.check_id != PINNED_HARVEST_DRIFT or not row.findings:
        return False
    return all(
        finding.rule == "value.harvest-parity" and "[추가]" in finding.message
        for finding in row.findings
    )


def rule_tally(row) -> dict:
    tally: dict = {}
    for finding in row.findings:
        tally[finding.rule] = tally.get(finding.rule, 0) + 1
    return tally


def run_spec_copy() -> dict:
    """실특허 산출의 **복사본**. 원본은 손대지 않는다."""
    return copy.deepcopy(RUN_SPEC_DATA)


def synthetic(claim: dict) -> dict:
    """우선권 1건만 든 최소 명세. 옆 규칙이 함께 울지 않도록 서지 목록은 비워 둔다.

    합성 원천을 쓰는 시험(창 안/창 밖·번호 부재)은 실특허 원천을 쓸 수 없다 — 원천을 지어내면
    발명자·분류가 그 원천에 없어서 다른 규칙이 함께 울고, 그러면 무엇이 실패를 유발했는지
    증명되지 않는다(코퍼스의 "한 곳만" 규율과 같은 이유).
    """
    return {
        "patent": {
            "number": "US1234567A1",
            "jurisdiction": "US",
            "kind_code": "A1",
            "dates": {"priority": claim["date"]},
            "priority_claims": [copy.deepcopy(claim)],
        }
    }


CLAIM = {"number": "63724151", "date": "2024-11-22", "jurisdiction": "KR"}


# ---------------------------------------------------------------------------
# ① 대조군 — 정직한 복사가 벌받으면 안 된다
# ---------------------------------------------------------------------------


def test_unmutated_real_run_still_passes() -> None:
    """무변조 실특허 산출이 실패하면 신설 규칙은 과잉 제약이고 아래 반증은 전부 무의미하다."""
    row = run_bibliography(RUN_SPEC_DATA, RUN_SOURCE_TEXT)
    if row.status != "pass":
        detail = "; ".join(f"{f.rule}@{f.locus}: {f.found}" for f in row.findings)
        pytest.fail(f"무변조 실특허 산출이 실패했다 — {detail}")
    if row.vacuous != "none":
        pytest.fail(f"공허 날인: {row.vacuous} (checked={row.checked})")
    # 근접 대조 2종이 실제로 대상을 가졌는가. 우선권 4건 × 2규칙 = 8건이 checked 에 들어온다.
    if row.checked < 8:
        pytest.fail(f"checked={row.checked} — 근접 대조가 대상을 갖지 못했다(공허 통과)")


def test_unmutated_real_run_passes_every_read_check() -> None:
    """옆 검사가 이미 실패 중이면 "이 규칙만 운다"는 아래 판정들이 기준선 없이 읽힌다."""
    rows = [row for row in run_all_read(RUN_SPEC_DATA, RUN_SOURCE_TEXT) if row.status != "pass"]
    failing = [row.check_id for row in rows if not is_pinned_harvest_drift(row)]
    if failing:
        pytest.fail(f"무변조 실특허 산출에서 실패한 검사: {failing}")


# ---------------------------------------------------------------------------
# ② 감수 재현 — 관할 전부 KR
# ---------------------------------------------------------------------------


def test_sol_mutation_all_priority_jurisdictions_to_kr_now_fails() -> None:
    """이 판이 통과하면 우선권 관할은 여전히 자유 기입이다 — 감수 P-2 ⓐ 가 실측한 그 공백이다."""
    spec = run_spec_copy()
    claims = spec["patent"]["priority_claims"]
    for claim in claims:
        claim["jurisdiction"] = "KR"

    row = run_bibliography(spec, RUN_SOURCE_TEXT)
    if row.status != "fail":
        pytest.fail(
            "우선권 관할을 전부 KR 로 바꿔도 통과했다 — 감수가 실측한 공백이 그대로다 "
            f"(checked={row.checked}, viol={row.violations})"
        )
    tally = rule_tally(row)
    if tally != {JURISDICTION_RULE: len(claims)}:
        pytest.fail(f"규칙별 위반이 기대와 다르다: {tally} (기대 {{{JURISDICTION_RULE}: {len(claims)}}})")
    loci = sorted(f.locus for f in row.findings)
    expected_loci = sorted(f"patent.priority_claims[{i}].jurisdiction" for i in range(len(claims)))
    if loci != expected_loci:
        pytest.fail(f"어느 주장이 어긋났는지의 좌표가 다르다: {loci}")


def test_kr_elsewhere_in_the_source_does_not_rescue_a_forged_jurisdiction() -> None:
    """전역 부분문자열 대조로 구현하면 두 글자 코드는 무엇으로 바꿔도 통과한다 — 근접성이 이 검사의 전부다."""
    # 창 밖(약 200자 뒤)에 KR 이 실재하는 원천. 번호 곁에는 없다.
    far = (
        "Related U.S. Application Data\n"
        "us-provisional-application US [63724151 20241122](tel:63724151 20241122)\n"
        + "\n".join(f"[00{n}] Filler paragraph {n} of the description." for n in range(41, 46))
        + "\nThe applicant also filed a KR counterpart in a later year.\n"
    )
    if "KR" not in far:
        pytest.fail("합성 원천에 KR 이 없다 — 이 시험이 공허하다")
    row = run_bibliography(synthetic(CLAIM), far)
    if rule_tally(row) != {JURISDICTION_RULE: 1}:
        pytest.fail(f"창 밖의 KR 로 통과했다(전역 대조의 징후): {rule_tally(row)}")

    # 대조군 — 같은 코드가 **번호 곁**에 있으면 통과한다(과잉 제약 배제).
    near = far.replace("US [63724151", "KR [63724151")
    near_row = run_bibliography(synthetic(CLAIM), near)
    if JURISDICTION_RULE in rule_tally(near_row):
        pytest.fail(f"번호 곁의 KR 을 인정하지 않았다 — 정직한 복사가 벌받는다: {rule_tally(near_row)}")


# ---------------------------------------------------------------------------
# ③ 잔여 구멍 — 두 날짜를 정합적으로 함께 위조하는 경로
# ---------------------------------------------------------------------------


def test_coherent_date_forgery_bypasses_earliest_priority_but_not_the_year_rule() -> None:
    """이 판이 통과하면 최우선일 등식은 **관계를 지킨 거짓**을 그대로 통과시킨다(총괄 실측 §5.3)."""
    spec = run_spec_copy()
    claims = spec["patent"]["priority_claims"]
    for claim in claims:
        claim["date"] = "1900-01-01"
    spec["patent"]["dates"]["priority"] = "1900-01-01"

    row = run_bibliography(spec, RUN_SOURCE_TEXT)
    tally = rule_tally(row)
    if EARLIEST_RULE in tally:
        pytest.fail(
            f"정합 위조인데 {EARLIEST_RULE} 가 울었다 — 이 판은 잔여 구멍의 표본이 아니다: {tally}"
        )
    if tally != {YEAR_RULE: len(claims)}:
        pytest.fail(f"연도 대조가 정합 위조를 잡지 못했다: {tally}")


def test_year_rule_is_the_only_guard_of_a_single_priority_claim_date() -> None:
    """한 주장의 날짜만 위조한 판을 다른 검사가 잡아 준다면 이 규칙은 있어도 없어도 같다."""
    spec = run_spec_copy()
    # 뒤로 미룬 날짜 — 최소값이 바뀌지 않으므로 bib.earliest-priority 는 성립하고,
    # dates.priority 를 건드리지 않으므로 서지 수확 대조(value.bibliographic·harvest-parity)도
    # 조용하다. 남는 집행자가 하나뿐임을 보이는 것이 이 시험의 전부다.
    spec["patent"]["priority_claims"][3]["date"] = "2025-06-01"

    failing = {
        row.check_id: row
        for row in run_all_read(spec, RUN_SOURCE_TEXT)
        if row.status != "pass" and not is_pinned_harvest_drift(row)
    }
    if list(failing) != [CHECK_ID]:
        pytest.fail(f"실패한 검사가 {sorted(failing)} 다 — 기대는 [{CHECK_ID}] 뿐이다")
    tally = rule_tally(failing[CHECK_ID])
    if tally != {YEAR_RULE: 1}:
        pytest.fail(f"규칙별 위반이 기대와 다르다: {tally}")
    locus = failing[CHECK_ID].findings[0].locus
    if locus != "patent.priority_claims[3].date":
        pytest.fail(f"어느 주장의 날짜가 어긋났는지의 좌표가 다르다: {locus}")


# ---------------------------------------------------------------------------
# ④ 관할의 경계 — 번호가 원천에 없으면 판정하지 않는다
# ---------------------------------------------------------------------------


def test_absent_priority_number_is_judged_by_the_number_rule_alone() -> None:
    """한 결함을 두 규칙이 판정하면 어느 검사가 그것을 지키는지 확정할 수 없어진다."""
    source = "Related U.S. Application Data\nno application number appears on this page.\n"
    row = run_bibliography(synthetic(CLAIM), source)
    tally = rule_tally(row)
    if tally != {NUMBER_RULE: 1}:
        pytest.fail(f"번호 부재를 두 규칙이 함께 판정했다(관할 중복): {tally}")


def test_abstention_is_visible_in_checked_not_hidden() -> None:
    """판정하지 않은 사실이 `checked` 에 드러나지 않으면 미판정과 통과가 구별되지 않는다(재정 N5)."""
    present = "us-provisional-application US [63724151 20241122](tel:63724151 20241122)\n"
    absent = "no application number appears on this page.\n"
    with_number = run_bibliography(synthetic(CLAIM), present).checked
    without_number = run_bibliography(synthetic(CLAIM), absent).checked
    # 번호가 있으면 관할·연도 2건을 더 본다. 그 차이가 곧 미판정의 표시다.
    if with_number - without_number != 2:
        pytest.fail(
            f"checked 차이가 {with_number - without_number} 다(기대 2) — "
            f"번호 있음={with_number} · 번호 없음={without_number}"
        )


# ---------------------------------------------------------------------------
# ⑤ 창 폭의 소유 — 규칙 파일이 정하고 코드는 읽는다
# ---------------------------------------------------------------------------


def test_window_width_comes_from_the_rules_file() -> None:
    """코드가 기본값을 지어내면 창 폭이 조용히 코드로 이주하고 규칙 파일의 diff 는 개정 이력이 아니게 된다."""
    raw = copy.deepcopy(RULES.raw)
    raw["bibliography"]["priority_window"]["before"] = 0
    raw["bibliography"]["priority_window"]["after"] = 0
    narrowed = Rules(raw, DEFAULT_RULES_PATH)

    # 창을 0/0 으로 좁히면 번호 문자열 자신만 남는다 — 실특허의 관할·연도는 번호 밖에 있으므로
    # 전건이 실패해야 한다. 실패하지 않으면 검사가 이 값을 읽지 않는다는 뜻이다.
    row = run_bibliography(RUN_SPEC_DATA, RUN_SOURCE_TEXT, rules=narrowed)
    claims = len(RUN_SPEC_DATA["patent"]["priority_claims"])
    if rule_tally(row) != {JURISDICTION_RULE: claims, YEAR_RULE: claims}:
        pytest.fail(f"창 폭을 0/0 으로 바꿔도 판정이 그대로다 — 코드가 계약을 읽지 않는다: {rule_tally(row)}")


def test_missing_window_declaration_is_an_input_error_not_a_pass() -> None:
    """규칙 파일에서 창 폭이 사라졌는데 검사가 통과하면, 그 통과는 아무것도 뜻하지 않는다."""
    raw = copy.deepcopy(RULES.raw)
    del raw["bibliography"]["priority_window"]
    crippled = Rules(raw, DEFAULT_RULES_PATH)
    try:
        row = run_bibliography(RUN_SPEC_DATA, RUN_SOURCE_TEXT, rules=crippled)
    except RulesError:
        return
    pytest.fail(f"창 폭 선언이 없는데 검사가 {row.status} 로 끝났다 — 기본값을 지어냈다")


# ---------------------------------------------------------------------------
# ⑥ 계약·코퍼스 결박
# ---------------------------------------------------------------------------


def test_new_rule_ids_are_declared_in_the_rules_file() -> None:
    """코드가 규칙 파일에 없는 id 로 결함을 내면 판정문의 근거를 계약에서 찾을 수 없다."""
    declared = set(RULES.bibliography_rule_ids())
    missing = [rid for rid in (JURISDICTION_RULE, YEAR_RULE) if rid not in declared]
    if missing:
        pytest.fail(f"reader-rules.yaml#bibliography.rules 에 없는 규칙 id: {missing}")
    if RULES.bibliography.get("priority_window", {}).get("tag") != "[가설]":
        pytest.fail("창 폭 선언에 [가설] 태그가 없다 — 실측 1건에 기댄 값임이 문서에서 사라진다")


@pytest.mark.parametrize(
    "fixture_name, expected_rule",
    [
        ("bibliography-priority-jurisdiction-out-of-window.json", JURISDICTION_RULE),
        ("bibliography-priority-year-coherent-forgery.json", YEAR_RULE),
    ],
)
def test_corpus_mutants_bind_to_the_rule_that_must_catch_them(fixture_name: str, expected_rule: str) -> None:
    """도구는 **검사 id 까지만** 대조한다 — 규칙이 바뀌어도 다른 규칙이 우연히 울면 코퍼스가 침묵한다."""
    with open(os.path.join(CORPUS, "invalid", fixture_name), encoding="utf-8") as handle:
        spec = json.load(handle)
    with open(os.path.join(CORPUS, "base", "patent.md"), encoding="utf-8") as handle:
        source = handle.read()
    tally = rule_tally(run_bibliography(spec, source))
    if tally != {expected_rule: 1}:
        pytest.fail(f"{fixture_name}: 규칙별 위반이 {tally} 다(기대 {{{expected_rule}: 1}})")


def test_corpus_manifest_registers_the_two_new_mutants() -> None:
    """등재하지 않은 픽스처는 집행 증명의 구멍이고, 하한을 올리지 않으면 지워도 아무도 울지 않는다."""
    with open(os.path.join(CORPUS, "manifest.json"), encoding="utf-8") as handle:
        manifest = json.load(handle)
    listed = {case["file"] for case in manifest["cases"]}
    expected = {
        "invalid/bibliography-priority-jurisdiction-out-of-window.json",
        "invalid/bibliography-priority-year-coherent-forgery.json",
    }
    missing = sorted(expected - listed)
    if missing:
        pytest.fail(f"manifest 에 등재되지 않은 신규 변조본: {missing}")
    if manifest["floors"]["min_cases"] != len(manifest["cases"]):
        pytest.fail(
            f"래칫이 실제 케이스 수와 다르다: min_cases={manifest['floors']['min_cases']} · "
            f"cases={len(manifest['cases'])}"
        )
