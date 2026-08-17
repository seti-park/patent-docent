# -*- coding: utf-8 -*-
"""스키마 집행 실증 픽스처의 pytest.

`tools/check_schema_enforcement.py`와 **같은 manifest**를 읽어 같은 판정을 확인한다.
도구는 사람이 손으로 돌리는 관문이고 이 테스트는 스위트에 걸리는 관문이라, 둘 중 하나만
남으면 집행 증명이 조용히 빠져나간다.

`assert`를 쓰지 않는다(`python3 -O`에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
불일치는 `pytest.fail()`로 명시 비교와 함께 보고한다.

★ 자기매칭 격리: 이 테스트도 도구와 같은 이유로 자기매칭이 성립하지 않는다 — 탐지 패턴을
갖지 않고 계약 스키마를 인스턴스에 적용할 뿐이며, 심은 결함 문자열은 소스가 아니라
`tests/fixtures/schema-enforcement/`의 `reject/`·`validator-scope/` 데이터 파일에만 있다
(모듈 docstring of `tools/check_schema_enforcement.py` 참조).

기대 클래스는 셋이다 — `reject`(스키마가 거부해야 함) · `accept`(통과시켜야 함) ·
`validator-scope`(무효 인스턴스지만 스키마가 설계상 통과시키며 집행은 `enforced_by`의
검증기 검사 몫). 비교 기준은 `case.expect`가 아니라 `case.schema_verdict`다.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import check_schema_enforcement as cse  # noqa: E402  (경로 주입 후 임포트)


def _cases() -> list[cse.Case]:
    return cse.load_manifest(REPO)


CASES = _cases()


def test_manifest_has_both_expectations() -> None:
    """무효·유효 양쪽이 다 있어야 집행 증명이 성립한다(한쪽만이면 공허하다)."""
    rejects = [case for case in CASES if case.expect == "reject"]
    accepts = [case for case in CASES if case.expect == "accept"]
    if not rejects:
        pytest.fail("manifest 에 expect=reject 케이스가 없다 — 무효 인스턴스 없이는 집행을 증명할 수 없다")
    if not accepts:
        pytest.fail("manifest 에 expect=accept 케이스가 없다 — 유효 인스턴스 없이는 과잉 제약을 배제할 수 없다")


def test_validator_scope_cases_name_their_enforcer() -> None:
    """`validator-scope` 항목은 집행할 검사 id 를 반드시 들고 있다.

    이 클래스는 "스키마가 설계상 통과시키는 무효 인스턴스"이므로, 집행 주체를 적지 않으면
    통과가 곧 '아무도 막지 않는다'는 사실을 숨긴다(M0.6 재감수 B-02).
    """
    nameless = [case.file for case in CASES if case.expect == "validator-scope" and not case.enforced_by]
    if nameless:
        pytest.fail("enforced_by 가 없는 validator-scope 케이스: " + ", ".join(nameless))


def test_manifest_covers_every_fixture_on_disk() -> None:
    """디스크의 픽스처가 전부 manifest 에 등재되었는지 확인한다(미등재 = 증명의 구멍)."""
    listed = {case.file for case in CASES}
    found: set[str] = set()
    for bucket in cse.FIXTURE_BUCKETS:
        directory = os.path.join(REPO, cse.FIXTURE_ROOT, bucket)
        if not os.path.isdir(directory):
            pytest.fail(f"픽스처 디렉터리가 없다: {cse.FIXTURE_ROOT}/{bucket}")
        found |= {f"{bucket}/{name}" for name in os.listdir(directory) if name.endswith(".json")}
    orphans = sorted(found - listed)
    if orphans:
        pytest.fail("manifest 미등재 픽스처: " + ", ".join(orphans))
    missing = sorted(listed - found)
    if missing:
        pytest.fail("manifest 에 있으나 디스크에 없는 픽스처: " + ", ".join(missing))


@pytest.mark.parametrize("case", CASES, ids=[case.file for case in CASES])
def test_schema_enforcement(case: cse.Case) -> None:
    schema_path = os.path.join(REPO, case.schema)
    if not os.path.isfile(schema_path):
        pytest.fail(f"스키마 파일이 없다: {case.schema}")
    with open(schema_path, encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)

    outcome = cse.run_case(REPO, case, Draft202012Validator(schema))
    if outcome.actual == case.schema_verdict:
        return

    verdict = cse.verdict_line(case, outcome.actual)
    detail = "(오류 없음)" if outcome.actual == "accept" else f"{outcome.error_path} — {outcome.first_error}"
    pytest.fail(
        "\n".join(
            [
                f"픽스처 : {case.file}",
                f"스키마 : {case.schema}",
                f"계열   : {case.series}",
                f"기대   : {case.expect} (스키마 판정 {case.schema_verdict})",
                f"실제   : {outcome.actual}",
                f"판정   : {verdict}",
                f"상세   : {detail}",
                f"근거   : {case.basis}",
            ]
        )
    )


# ---------------------------------------------------------------------------
# manifest 계약 자체의 집행 — `enforced_status` · `enforcement_evidence`
#
# 위 테스트들은 **픽스처가 스키마에 대해** 옳은지를 본다. 아래 테스트들은 한 층 위,
# **manifest 가 도구의 계약을 지키는지**를 본다. 이 층이 비면 요약 줄의 "구현됨 n / 미구현 m"
# 이 근거 없이 아무 말이나 할 수 있게 되고, 그것이 곧 집행 범위를 실제와 다르게 신고하는
# 경로다(M0.6 재감수가 판정한 결함의 뿌리).
#
# 도구를 함수로 부르지 않고 **서브프로세스 종료 코드**로 확인한다 — 규율 위반이 exit 2
# (입력 오류)로 나오는 것까지가 계약이며, 그 계약을 지키는 것은 예외 타입이 아니라 종료 코드다.
# 종료 코드 비교는 명시 비교 + pytest.fail 이다(이 파일의 규율: assert 금지).
# ---------------------------------------------------------------------------

TOOL = os.path.join(REPO, "tools", "check_schema_enforcement.py")


def _scope_index(doc: dict) -> int:
    """`enforced_status: implemented` 인 validator-scope 항목의 위치."""
    for index, case in enumerate(doc["cases"]):
        if case.get("expect") == "validator-scope" and case.get(cse.STATUS_KEY) == "implemented":
            return index
    pytest.fail(f"manifest 에 {cse.STATUS_KEY}=implemented 인 validator-scope 항목이 없다 — 음성 시험의 전제가 사라졌다")
    return -1  # pragma: no cover - pytest.fail 이 이미 종료한다


def _sandbox(tmp_path, mutate=None) -> str:
    """리포 사본을 만든다. 픽스처만 복사하고 계약 소스는 심링크한다.

    manifest 를 변형해 도구를 돌려야 하는데 정본 픽스처 트리를 건드릴 수는 없다. 스키마는
    읽기 전용이므로 심링크로 충분하며, 이렇게 하면 사본이 계약 정본과 어긋날 여지도 없다.
    """
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    for name in ("reader", "contracts"):
        os.symlink(os.path.join(REPO, name), repo / name)
    shutil.copytree(os.path.join(REPO, "tests", "fixtures"), repo / "tests" / "fixtures")

    manifest_path = repo / cse.MANIFEST_REL
    with open(manifest_path, encoding="utf-8") as handle:
        doc = json.load(handle)
    if mutate is not None:
        mutate(doc)
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(doc, handle, ensure_ascii=False, indent=2)
    return str(repo)


def _run_tool(repo: str, optimized: bool = False) -> subprocess.CompletedProcess:
    argv = [sys.executable]
    if optimized:
        argv.append("-O")
    argv += [TOOL, "--repo", repo]
    return subprocess.run(argv, capture_output=True, text=True)


def _drop_status(doc: dict) -> None:
    del doc["cases"][_scope_index(doc)][cse.STATUS_KEY]


def _bad_status(doc: dict) -> None:
    doc["cases"][_scope_index(doc)][cse.STATUS_KEY] = "maybe"


def _drop_evidence(doc: dict) -> None:
    del doc["cases"][_scope_index(doc)][cse.EVIDENCE_KEY]


def _empty_evidence(doc: dict) -> None:
    doc["cases"][_scope_index(doc)][cse.EVIDENCE_KEY] = ""


def _planned_with_evidence(doc: dict) -> None:
    doc["cases"][_scope_index(doc)][cse.STATUS_KEY] = "planned"


def _drop_enforcer(doc: dict) -> None:
    del doc["cases"][_scope_index(doc)][cse.SCOPE_KEY]


def _status_on_non_scope(doc: dict) -> None:
    for case in doc["cases"]:
        if case.get("expect") != "validator-scope":
            case[cse.STATUS_KEY] = "implemented"
            return
    pytest.fail("manifest 에 validator-scope 가 아닌 항목이 없다")


# (id, 변형, 이 변형이 막히지 않으면 무엇이 공허해지는가)
SCOPE_CONTRACT_MUTATIONS = [
    (
        "status-missing",
        _drop_status,
        "집행 상태를 아예 신고하지 않고도 validator-scope 항목을 등재할 수 있게 된다",
    ),
    (
        "status-out-of-enum",
        _bad_status,
        "planned·implemented 밖의 임의 문자열이 상태 자리에 앉아 요약 줄의 계수를 무의미하게 만든다",
    ),
    (
        "implemented-without-evidence",
        _drop_evidence,
        "근거 없이 '구현됨'을 선언하는 경로가 열린다 — 집행 범위를 실제보다 넓게 말하는 쪽의 결함",
    ),
    (
        "implemented-with-empty-evidence",
        _empty_evidence,
        "키만 두고 내용을 비우는 우회로가 열려 위 검사가 형식만 남는다",
    ),
    (
        "planned-with-stale-evidence",
        _planned_with_evidence,
        "구현을 되돌리면서 증거만 남겨 두는 상태가 통과해, 증거가 어느 상태의 것인지 알 수 없게 된다",
    ),
    (
        "scope-without-enforcer",
        _drop_enforcer,
        "집행 주체 없는 validator-scope 가 통과해 '아무도 막지 않는다'는 사실이 숨는다",
    ),
    (
        "status-on-non-scope-case",
        _status_on_non_scope,
        "reject·accept 항목이 집행 상태를 참칭해도 조용히 무시되어, 읽는 사람이 없는 집행을 있다고 읽는다",
    ),
]


def test_scope_contract_baseline_sandbox_passes(tmp_path) -> None:
    """사본은 무변형이면 통과해야 한다 — 아래 음성 시험들의 대조군.

    이 테스트가 없으면 사본 만드는 절차가 깨졌을 때 모든 음성 시험이 '엉뚱한 이유로' exit 2 를
    내고도 초록으로 보인다(공허 통과의 전형).
    """
    result = _run_tool(_sandbox(tmp_path))
    if result.returncode != 0:
        pytest.fail(
            f"무변형 사본이 통과하지 못했다: exit={result.returncode} (기대 0)\n"
            f"stdout 끝: {result.stdout.strip()[-400:]}\nstderr: {result.stderr.strip()[-400:]}"
        )


@pytest.mark.parametrize(
    ("mutation_id", "mutate", "what_goes_vacuous"),
    SCOPE_CONTRACT_MUTATIONS,
    ids=[item[0] for item in SCOPE_CONTRACT_MUTATIONS],
)
def test_scope_contract_violation_exits_two(tmp_path, mutation_id, mutate, what_goes_vacuous) -> None:
    """manifest 의 집행 상태 규율을 어긴 판은 입력 오류(exit 2)로 거부되어야 한다.

    이 테스트가 없으면 새 키(enforced_status·enforcement_evidence)를 지키는 것이 도구 소스의
    문장뿐이 되고, 그 문장은 다음 개정에서 조용히 사라져도 아무 데서도 드러나지 않는다.
    """
    result = _run_tool(_sandbox(tmp_path, mutate))
    if result.returncode != 2:
        pytest.fail(
            "\n".join(
                [
                    f"변형   : {mutation_id}",
                    f"기대   : exit 2 (입력 오류)",
                    f"실제   : exit {result.returncode}",
                    f"공허화 : {what_goes_vacuous}",
                    f"stderr : {result.stderr.strip()[-400:] or '(없음)'}",
                ]
            )
        )
    if "ENVIRONMENT ERROR" not in result.stderr:
        pytest.fail(f"{mutation_id}: exit 2 는 났으나 stderr 에 입력 오류 문장이 없다 — {result.stderr.strip()[-300:]}")


@pytest.mark.parametrize("mutation", [None, _drop_evidence], ids=["baseline", "implemented-without-evidence"])
def test_scope_contract_holds_under_optimize_flag(tmp_path, mutation) -> None:
    """`python3` 와 `python3 -O` 가 같은 종료 코드를 내야 한다(SPEC §8.3 ④).

    이 테스트가 없으면 검증이 assert 로 되돌아가도 아무도 모른다 — `-O` 에서 assert 는 통째로
    제거되므로, 그 순간 위 음성 시험 전부가 최적화 실행에서 공허 통과한다.
    """
    repo = _sandbox(tmp_path, mutation)
    plain = _run_tool(repo, optimized=False)
    optimized = _run_tool(repo, optimized=True)
    if plain.returncode != optimized.returncode:
        pytest.fail(
            f"python3 와 python3 -O 의 종료 코드가 다르다: {plain.returncode} vs {optimized.returncode} "
            f"— 최적화 실행에서 사라지는 검증 기제가 섞여 있다\nstderr(-O): {optimized.stderr.strip()[-400:]}"
        )
    expected = 0 if mutation is None else 2
    if plain.returncode != expected:
        pytest.fail(f"두 실행의 종료 코드는 같으나 기대와 다르다: {plain.returncode} (기대 {expected})")


def test_scope_contract_mutations_actually_change_the_manifest(tmp_path) -> None:
    """각 변형이 정말 manifest 를 바꾸는지 확인한다.

    이 테스트가 없으면 변형 함수가 아무것도 하지 않게 되었을 때(키 이름 개정 등) 위 음성
    시험들이 '변형 없는 사본'을 돌리게 되고, 그때는 exit 2 가 아니라 0 이 나므로 실패로
    드러나기는 한다 — 그러나 반대 방향(다른 이유로 exit 2)이면 초록으로 남는다.
    """
    with open(os.path.join(REPO, cse.MANIFEST_REL), encoding="utf-8") as handle:
        original = json.load(handle)
    unchanged = []
    for mutation_id, mutate, _why in SCOPE_CONTRACT_MUTATIONS:
        doc = copy.deepcopy(original)
        mutate(doc)
        if doc == original:
            unchanged.append(mutation_id)
    if unchanged:
        pytest.fail("manifest 를 바꾸지 못한 변형: " + ", ".join(unchanged))
