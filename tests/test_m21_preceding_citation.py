"""재정 2026-09-01 T11-ⓒ — PCT 선행 청구항 인용 어형과 부분집합 판정.

원장 = `docs/decisions/ruling-20260901-02-T11.md` §3.

이 파일이 지는 것은 재정 T11-ⓒ 의 **집행 조건 4종 중 셋**이다(넷째 = 전수 시험·관문은 상시 규약).

  ① 반례 golden 을 세우고, **기대값은 golden 파일이 들고 시험은 그 파일을 읽는다.**
     시험에 값을 복제하면 한 벌이 반드시 낡는다.
  ② **`'854` 무회귀** — 수정 전 규칙 폭과 수정 후 규칙 폭을 같은 실행에서 직접 비교한다.
  ③ **부분집합 판정의 비공허성** — 빈 배열·자기 자신·후행 번호는 실패하고 정당한 부분집합은
     통과해야 한다.

★ `all-preceding` 은 본문이 구체 번호를 말하지 않는다. 따라서 검사는 `1..n-1` 과 정확 일치를
요구하지 않고, 레인이 선언한 값이 그 집합의 비어 있지 않은 부분집합인지에만 답한다.
"""

from __future__ import annotations

import ast
import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from reader.lib import CHECK_REGISTRY, CheckContext, Rules, load_schema  # noqa: E402
from reader.lib.dependency_parse import parse_citations  # noqa: E402
from reader.lib.inventory import parse_source_claims  # noqa: E402

GOLDEN_DIR = os.path.join(
    REPO, "ledgers", "regression", "golden", "rc-0007-preceding-citation-counterexamples"
)
CASES_PATH = os.path.join(REPO, "ledgers", "regression", "cases.jsonl")
DEPENDENCY_SOURCE = os.path.join(REPO, "reader", "lib", "dependency_parse.py")
US854_SOURCE = os.path.join(
    REPO, "runs", "openai-us20260147854a1-cim-fp-3", "00-source", "patent.md"
)
US854_SPEC = os.path.join(
    REPO,
    "runs",
    "openai-us20260147854a1-cim-fp-3",
    "15-frozen",
    "material-spec.v1.json",
)


def narrowed_rules() -> Rules:
    """`all-preceding` 어형을 뺀 규칙 — 재정 T11 이전의 폭을 그대로 재현한다."""
    raw = copy.deepcopy(Rules.load().raw)
    forms = raw["dependency_citation"]["forms"]
    raw["dependency_citation"]["forms"] = [
        form for form in forms if form.get("id") != "all-preceding"
    ]
    return Rules(raw, "<pre-T11>")


def load_json(path: str) -> dict:
    if not os.path.isfile(path):
        pytest.fail(f"golden 표본이 없다: {path} — 반례가 사라지면 그 주장은 근거를 잃는다")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def read_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def sample_spec(sample: dict) -> dict:
    dependent = {
        "id": f"CL-{sample['self_claim']}",
        "depends_on": list(sample["declared"]["depends_on"]),
        "dependency_type": sample["declared"]["dependency_type"],
        "text_verbatim": sample["quote"],
        "additions": [],
    }
    return {
        "claims": {
            "independent": [],
            "dependents": [dependent],
            "applicant_interest": [],
        },
        "items": [],
    }


def check_sample(sample: dict, rules: Rules | None = None):
    active_rules = rules or Rules.load()
    context = CheckContext(
        spec=sample_spec(sample),
        source_text="",
        rules=active_rules,
        schema=load_schema(),
    )
    return CHECK_REGISTRY["read.dependency-parse"](context)


def finding_rules(row) -> list[str]:
    return sorted(finding.rule for finding in row.findings)


# ---------------------------------------------------------------------------
# ① 규칙 파일이 새 어형을 선언하고, 코드는 expands 선언을 읽는다
# ---------------------------------------------------------------------------


def test_new_form_is_declared_in_the_rules_file_not_the_code() -> None:
    """새 어형 id가 코드 분기 조건으로 새면 규칙 파일이 더는 어형의 정본이 아니다."""
    rules = Rules.load()
    forms = [form for form in rules.dependency_forms if form.get("id") == "all-preceding"]
    if len(forms) != 1:
        pytest.fail(f"all-preceding 선언이 정확히 1건이어야 한다: {len(forms)}")
    form = forms[0]
    got = (form.get("implies_type"), form.get("expands"))
    want = ("all-preceding", "preceding")
    if got != want:
        pytest.fail(f"all-preceding 선언 배선 불일치: got={got!r} want={want!r}")

    with open(DEPENDENCY_SOURCE, encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), filename=DEPENDENCY_SOURCE)
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        literals = [
            child.value
            for child in ast.walk(node)
            if isinstance(child, ast.Constant) and isinstance(child.value, str)
        ]
        if "all-preceding" in literals:
            offenders.append(node.lineno)
    if offenders:
        pytest.fail(f"어형 id 리터럴이 코드 Compare 분기에 박혔다: lines={offenders}")


def test_existing_five_forms_are_untouched() -> None:
    """기존 5어형 기대값을 규칙 파일에서 다시 읽으면 변경을 보존으로 오인하는 동어반복이 된다."""
    expected = [
        (
            "range",
            1,
            "multiple-or",
            r"\bany\s+(?:one\s+)?of\s+claims?\s+(?P<lo>\d+)\s*(?:-|–|—|to|through)\s*(?P<hi>\d+)",
        ),
        (
            "bare-range",
            2,
            "multiple-or",
            r"\bclaims\s+(?P<lo>\d+)\s*(?:-|–|—|to|through)\s*(?P<hi>\d+)",
        ),
        (
            "or-list",
            3,
            "multiple-or",
            r"\bclaims?\s+(?P<nums>\d+(?:\s*(?:,|,?\s*or)\s*(?:claim\s+)?\d+)+)",
        ),
        (
            "and-list",
            4,
            "multiple-and",
            r"\bclaims?\s+(?P<nums>\d+(?:\s*(?:,|,?\s*and)\s*(?:claim\s+)?\d+)+)",
        ),
        ("single", 5, "single", r"\bclaims?\s+(?P<n>\d+)"),
    ]
    got = [
        (form.get("id"), form.get("rank"), form.get("implies_type"), form["pattern"].pattern)
        for form in Rules.load().dependency_forms
        if form.get("id") != "all-preceding"
    ]
    if got != expected:
        pytest.fail(f"기존 5어형이 움직였다:\ngot={got!r}\nwant={expected!r}")


# ---------------------------------------------------------------------------
# ② golden — 기대값은 파일이 들고 실제 파서·검사에 물린다
# ---------------------------------------------------------------------------


def test_golden_samples_match_the_real_parser_and_check() -> None:
    """golden 기대값이 실제 파서·검사와 갈리면 반례 파일은 근거가 아니라 장식이다."""
    samples = load_json(os.path.join(GOLDEN_DIR, "samples.json"))["samples"]
    if len(samples) < 12:
        pytest.fail(f"표본이 줄었다: {len(samples)}")
    rules = Rules.load()
    failures = []
    for sample in samples:
        parsed = parse_citations(sample["quote"], rules, sample["self_claim"])
        got_forms = [match["form"] for match in parsed.matches]
        want_forms = list(sample["expect_matched_forms"])
        if got_forms != want_forms:
            failures.append(
                f"  {sample['id']} forms: got={got_forms!r} want={want_forms!r}"
            )
        got_rules = finding_rules(check_sample(sample, rules))
        want_rules = list(sample["expect_rules"])
        if got_rules != want_rules:
            failures.append(
                f"  {sample['id']} rules: got={got_rules!r} want={want_rules!r}"
            )
    if failures:
        pytest.fail("golden 표본 불일치:\n" + "\n".join(failures))


def test_golden_holds_all_three_directions() -> None:
    """적중·기존 보존·실패 중 한 방향이 사라지면 무엇이든 잡거나 받는 규칙도 통과한다."""
    samples = load_json(os.path.join(GOLDEN_DIR, "samples.json"))["samples"]
    hits = [
        sample
        for sample in samples
        if "all-preceding" in sample["expect_matched_forms"]
        and sample["expect_rules"] == []
    ]
    preserved = [
        sample
        for sample in samples
        if "all-preceding" not in sample["expect_matched_forms"]
    ]
    failures = [sample for sample in samples if sample["expect_rules"] != []]
    counts = (len(hits), len(preserved), len(failures))
    if any(count < 3 for count in counts):
        pytest.fail(
            "golden 세 방향 중 표본이 3건 미만이다: "
            f"all-preceding 적중={counts[0]} 기존 보존={counts[1]} 실패={counts[2]}"
        )


def test_golden_is_registered_in_the_case_ledger() -> None:
    """장부에 등재되지 않은 golden은 회귀 스위트가 모르는 파일이다(SPEC §6.5 · 재정 N4)."""
    rows = {}
    with open(CASES_PATH, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                row = json.loads(line)
                rows[row["case_id"]] = row
    row = rows.get("rc-0007")
    if row is None:
        pytest.fail(f"cases.jsonl 에 rc-0007 이 없다: {sorted(rows)}")
    base = os.path.join(REPO, "ledgers", "regression", row["base"])
    if not os.path.isfile(base):
        pytest.fail(f"rc-0007 의 base 가 실물을 가리키지 않는다: {row['base']}")
    if row["expect"]["must_detect"] is not False:
        pytest.fail(f"rc-0007 은 반례이므로 must_detect 가 false 여야 한다: {row['expect']}")
    meta = load_json(os.path.join(GOLDEN_DIR, "meta.json"))
    if meta.get("case_id") != "rc-0007":
        pytest.fail(f"meta.json 의 case_id 가 어긋난다: {meta.get('case_id')}")
    if "ruling-20260901-02-T11.md" not in str(meta.get("note") or ""):
        pytest.fail("rc-0007 의 meta.note 가 등재 근거 재정을 가리키지 않는다")


# ---------------------------------------------------------------------------
# ③ 실물 무회귀와 부분집합 비공허성
# ---------------------------------------------------------------------------


def test_us854_dependency_parse_does_not_regress() -> None:
    """같은 실행의 전후 비교가 없으면 새 어형이 기존 US 인용을 움직여도 무회귀라 부르게 된다."""
    narrowed = narrowed_rules()
    full = Rules.load()
    probe = parse_citations(
        "The method of any of the preceding claims, wherein X.", narrowed, 6
    )
    if probe.matches:
        pytest.fail(f"수정 전 폭이 all-preceding 탐침을 이미 잡는다: {probe.matches}")
    if not os.path.isfile(US854_SOURCE) or not os.path.isfile(US854_SPEC):
        pytest.skip(f"통주 3 원천 또는 동결 재료가 없다: {US854_SOURCE} · {US854_SPEC}")

    with open(US854_SOURCE, encoding="utf-8") as handle:
        source_text = handle.read()
    claims = parse_source_claims(source_text, full)
    before_matches = 0
    differences = []
    for claim in claims:
        before = parse_citations(claim.body, narrowed, claim.number)
        after = parse_citations(claim.body, full, claim.number)
        before_matches += len(before.matches)
        before_value = (
            sorted(before.numbers),
            sorted(before.implied_types),
            [match["form"] for match in before.matches],
        )
        after_value = (
            sorted(after.numbers),
            sorted(after.implied_types),
            [match["form"] for match in after.matches],
        )
        if before_value != after_value:
            differences.append(
                f"CL-{claim.number}: before={before_value!r} after={after_value!r}"
            )
    if before_matches == 0:
        pytest.fail("수정 전 폭의 '854 인용 매칭이 0건이다 — 대조군이 성립하지 않는다")
    if differences:
        pytest.fail("'854 원천 인용 파싱이 움직였다:\n  " + "\n  ".join(differences))

    spec = read_json(US854_SPEC)
    schema = load_schema()
    before_row = CHECK_REGISTRY["read.dependency-parse"](
        CheckContext(spec=spec, source_text=source_text, rules=narrowed, schema=schema)
    )
    after_row = CHECK_REGISTRY["read.dependency-parse"](
        CheckContext(spec=spec, source_text=source_text, rules=full, schema=schema)
    )
    before_result = (
        before_row.checked,
        before_row.violations,
        finding_rules(before_row),
    )
    after_result = (
        after_row.checked,
        after_row.violations,
        finding_rules(after_row),
    )
    if before_result != after_result:
        pytest.fail(
            f"'854 동결 재료 판정이 움직였다: before={before_result!r} after={after_result!r}"
        )


def test_preceding_subset_is_not_vacuous() -> None:
    """범위 밖·빈 배열을 직접 실패시키지 않으면 부분집합 규칙이 무엇이든 받는 공허한 이름이 된다."""
    cases = [
        ("outside", ["CL-3", "CL-6"], "fail", ["parse.preceding-subset"]),
        ("valid", ["CL-1", "CL-5"], "pass", []),
        ("empty", [], "fail", ["parse.preceding-subset"]),
    ]
    failures = []
    for case_id, depends_on, want_status, want_rules in cases:
        sample = {
            "self_claim": 6,
            "quote": "The method of any of the preceding claims, wherein X.",
            "declared": {
                "depends_on": depends_on,
                "dependency_type": "all-preceding",
            },
        }
        row = check_sample(sample)
        got = (row.status, finding_rules(row))
        want = (want_status, want_rules)
        if got != want:
            failures.append(f"{case_id}: got={got!r} want={want!r}")
    if failures:
        pytest.fail("부분집합 비공허성 불일치:\n  " + "\n  ".join(failures))


def test_preceding_claim_is_still_counted_and_typed() -> None:
    """새 어형이 checked·형태 대조에서 빠지면 unclassified와 같은 판정 면제를 얻게 된다."""
    base = {
        "self_claim": 6,
        "quote": "The method of any of the preceding claims, wherein X.",
        "declared": {"depends_on": ["CL-1"], "dependency_type": "all-preceding"},
    }
    row = check_sample(base)
    got = (row.checked, row.status, row.extras.get("unclassified"), finding_rules(row))
    want = (1, "pass", [], [])
    if got != want:
        pytest.fail(f"all-preceding 계수·분류 불일치: got={got!r} want={want!r}")

    wrong = copy.deepcopy(base)
    wrong["declared"]["dependency_type"] = "single"
    wrong_row = check_sample(wrong)
    wrong_got = (wrong_row.checked, wrong_row.status, finding_rules(wrong_row))
    wrong_want = (1, "fail", ["parse.type-agrees"])
    if wrong_got != wrong_want:
        pytest.fail(
            f"all-preceding 논리 형태 오선언 판정 불일치: got={wrong_got!r} want={wrong_want!r}"
        )
