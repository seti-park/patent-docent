# -*- coding: utf-8 -*-
"""재정 T18·T21의 미분류 문언 부재 자리표시와 짝 필드 결속을 반증한다.

레인이 제 나름의 자리표시(`"N/A"`·`"없음"` 등)를 `text_status: "verbatim"` 으로 실으면
스키마는 통과시킨다. 이 설계가 막는 것은 **엔진이 만드는 자리표시의 표류**이지 레인의
창작이 아니다. 후자는 `parse.unclassified-not-an-escape` 계열의 검증기 몫이며 이 스키마의
주장 범위 밖이다.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine.paths import RunPaths  # noqa: E402
from reader.lib.dependency_parse import (  # noqa: E402
    UNCLASSIFIED_TEXT_ABSENT,
    UNCLASSIFIED_TEXT_STATUS_ABSENT,
    UNCLASSIFIED_TEXT_STATUS_VERBATIM,
)


CASES = (
    ("canonical-cl3", "empty", "CL-3"),
    ("canonical-cl3", "missing", "CL-3"),
    ("peer-cl3", "empty", "CL-3"),
    ("peer-cl3", "missing", "CL-3"),
    ("peer-ghost-cl9", "empty", "CL-9"),
    ("peer-ghost-cl9", "missing", "CL-9"),
)


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def payloads_for(scenario: str, text_mode: str) -> dict[str, dict]:
    payloads = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    if scenario == "canonical-cl3":
        payloads["read-a"] = m2.payload_set(dependency_type="unclassified")
        target = payloads["read-a"]["decompose"]["claims"]["dependents"][0]
    elif scenario == "peer-cl3":
        payloads["read-b"] = m2.payload_set(dependency_type="unclassified")
        target = payloads["read-b"]["decompose"]["claims"]["dependents"][0]
    elif scenario == "peer-ghost-cl9":
        ghost = copy.deepcopy(
            payloads["read-b"]["decompose"]["claims"]["dependents"][0]
        )
        ghost["id"] = "CL-9"
        ghost["dependency_type"] = "unclassified"
        ghost["additions"] = []
        payloads["read-b"]["decompose"]["claims"]["dependents"].append(ghost)
        target = ghost
    else:
        pytest.fail(f"시나리오 기대 canonical-cl3|peer-cl3|peer-ghost-cl9, 실제 {scenario!r}")

    if text_mode == "empty":
        target["text_verbatim"] = ""
    elif text_mode == "missing":
        target.pop("text_verbatim", None)
    else:
        pytest.fail(f"문언 모드 기대 empty|missing, 실제 {text_mode!r}")
    return payloads


def run_case(tmp_path, scenario: str, text_mode: str) -> tuple[str, dict]:
    try:
        root, _, _ = m2.run_read(
            tmp_path,
            payloads_by_run=payloads_for(scenario, text_mode),
        )
    except Exception as exc:
        pytest.fail(
            f"{scenario}/{text_mode} 기대 예외 없이 완주, 실제 "
            f"{type(exc).__name__}: {exc}"
        )
    path = RunPaths(root).convergence_early_json
    if not os.path.isfile(path):
        pytest.fail(f"{scenario}/{text_mode} 기대 조기 판정서 실재, 실제 없음: {path}")
    return root, load_json(path)


def one_unclassified(report: dict, claim_id: str) -> dict:
    matches = [
        entry
        for entry in report.get("unclassified_dependents") or []
        if entry.get("claim") == claim_id
    ]
    if len(matches) != 1:
        pytest.fail(
            f"{claim_id} 미분류 항목 기대 정확히 1건, 실제 {len(matches)}건: "
            f"{report.get('unclassified_dependents')!r}"
        )
    return matches[0]


@pytest.mark.parametrize(("scenario", "text_mode", "claim_id"), CASES)
def test_all_six_absent_text_variants_finish_and_write_early_report(
    tmp_path, scenario: str, text_mode: str, claim_id: str
) -> None:
    """6개 회귀 변형 중 하나라도 계약 예외로 죽으면 T18 처분은 집행되지 않은 것이다."""
    _, report = run_case(tmp_path, scenario, text_mode)
    if report.get("schema") != "convergence/v0":
        pytest.fail(
            f"{scenario}/{text_mode} 조기 판정서 schema 기대 convergence/v0, "
            f"실제 {report.get('schema')!r}"
        )
    _ = claim_id


@pytest.mark.parametrize(("scenario", "text_mode", "claim_id"), CASES)
def test_all_six_absent_text_variants_preserve_the_unclassified_signal(
    tmp_path, scenario: str, text_mode: str, claim_id: str
) -> None:
    """빈 문언을 이유로 항목을 버리면 유령 청구항을 만든 레인의 신호가 사라진다."""
    _, report = run_case(tmp_path, scenario, text_mode)
    entry = one_unclassified(report, claim_id)
    actual = {
        "text_verbatim": entry.get("text_verbatim"),
        "text_status": entry.get("text_status"),
    }
    expected = {
        "text_verbatim": UNCLASSIFIED_TEXT_ABSENT,
        "text_status": UNCLASSIFIED_TEXT_STATUS_ABSENT,
    }
    if actual != expected:
        pytest.fail(
            f"{scenario}/{text_mode}/{claim_id} 기대 부재 신고 {expected!r}, 실제 {actual!r}"
        )


def test_placeholder_cannot_be_misread_as_source_text() -> None:
    """자리표시가 원천에 있으면 보고서의 값만으로 원문과 부재 신고를 구별할 수 없다."""
    if UNCLASSIFIED_TEXT_ABSENT in m2.SOURCE:
        pytest.fail(
            f"자리표시 기대 원천 부분문자열 아님, 실제 포함됨: {UNCLASSIFIED_TEXT_ABSENT!r}"
        )
    present_delimiters = [delimiter for delimiter in ("«", "»") if delimiter in m2.SOURCE]
    if present_delimiters:
        pytest.fail(f"겹화살괄호 기대 원천에 없음, 실제 포함 {present_delimiters!r}")


@pytest.mark.parametrize("scenario", ("canonical-cl3", "peer-cl3", "peer-ghost-cl9"))
def test_missing_key_and_empty_string_produce_the_same_pair(tmp_path, scenario: str) -> None:
    """키 부재와 빈 문자열이 다른 출력을 만들면 같은 부재가 입력 표기에 따라 갈라진다."""
    claim_id = "CL-9" if scenario == "peer-ghost-cl9" else "CL-3"
    _, empty_report = run_case(tmp_path.joinpath("empty"), scenario, "empty")
    _, missing_report = run_case(tmp_path.joinpath("missing"), scenario, "missing")
    empty_entry = one_unclassified(empty_report, claim_id)
    missing_entry = one_unclassified(missing_report, claim_id)
    keys = ("text_verbatim", "text_status")
    empty_pair = {key: empty_entry.get(key) for key in keys}
    missing_pair = {key: missing_entry.get(key) for key in keys}
    if empty_pair != missing_pair:
        pytest.fail(
            f"{scenario} 빈 문자열·키 부재 기대 동일, 실제 "
            f"empty={empty_pair!r}, missing={missing_pair!r}"
        )


def test_existing_unclassified_verbatim_text_is_unchanged(tmp_path) -> None:
    """실제 원문까지 자리표시로 바꾸면 부재 처리의 범위가 정상 문언을 침범한다."""
    payloads = {
        "read-a": m2.payload_set(dependency_type="unclassified"),
        "read-b": m2.payload_set(),
    }
    try:
        root, _, _ = m2.run_read(tmp_path, payloads_by_run=payloads)
    except Exception as exc:
        pytest.fail(
            f"정상 미분류 문언 기대 예외 없이 완주, 실제 {type(exc).__name__}: {exc}"
        )
    report = load_json(RunPaths(root).convergence_early_json)
    entry = one_unclassified(report, "CL-3")
    actual = {
        "text_verbatim": entry.get("text_verbatim"),
        "text_status": entry.get("text_status"),
    }
    expected = {
        "text_verbatim": m2.CLAIM_3,
        "text_status": UNCLASSIFIED_TEXT_STATUS_VERBATIM,
    }
    if actual != expected:
        pytest.fail(f"정상 미분류 문언 기대 {expected!r}, 실제 {actual!r}")


def test_reader_placeholder_matches_both_schema_const_sites() -> None:
    """코드와 스키마의 토큰이 갈라지면 엔진이 만든 정상형을 계약이 거부한다."""
    schema_path = os.path.join(REPO, "contracts", "schemas", "convergence.schema.json")
    schema = load_json(schema_path)
    item_schema = schema["properties"]["unclassified_dependents"]["items"]
    absent_const = item_schema["allOf"][0]["then"]["properties"]["text_verbatim"][
        "const"
    ]
    verbatim_excluded_const = item_schema["allOf"][1]["then"]["properties"][
        "text_verbatim"
    ]["not"]["const"]
    schema_consts = (absent_const, verbatim_excluded_const)
    expected = (UNCLASSIFIED_TEXT_ABSENT, UNCLASSIFIED_TEXT_ABSENT)
    if schema_consts != expected:
        pytest.fail(
            f"스키마 양방향 const 기대 reader 상수와 동일 {expected!r}, 실제 {schema_consts!r}"
        )
