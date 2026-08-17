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

import json
import os
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
