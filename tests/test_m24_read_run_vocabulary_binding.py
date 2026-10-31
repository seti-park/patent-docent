# -*- coding: utf-8 -*-
"""재정 T32·T35 — 독해 실행 id 단일 진원과 러너·실런 판정서의 계약 적합성을 고정한다."""

from __future__ import annotations

import inspect
import json
import os
import sys

import pytest
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.stages import read as read_stage  # noqa: E402
from engine.paths import RunPaths  # noqa: E402

import test_m2_read as m2  # noqa: E402
import test_m21_retry_budget_by_judgment_point as m21  # noqa: E402


SCHEMA_PATH = os.path.join(REPO, "contracts", "schemas", "convergence.schema.json")
RUN_REPORTS = (
    "runs/gdm-wo2026128750a1-agent-memory/10-read/convergence.json",
    "runs/gdm-wo2026128750a1-agent-memory/10-read/convergence-early.json",
    "runs/openai-us20260147854a1-cim-fp-2/10-read/convergence.json",
    "runs/openai-us20260147854a1-cim-fp-2/10-read/convergence-early.json",
    "runs/openai-us20260147854a1-cim-fp-3/10-read/convergence.json",
    "runs/openai-us20260147854a1-cim-fp-3/10-read/convergence-early.json",
)


def load_schema() -> tuple[str, dict]:
    with open(SCHEMA_PATH, encoding="utf-8") as handle:
        text = handle.read()
    return text, json.loads(text)


def test_reported_by_enum_matches_default_read_runs_in_order() -> None:
    """스키마 신고 실행 enum과 엔진 기본 실행 id는 순서까지 같아야 한다."""
    _, schema = load_schema()
    try:
        enum = schema["$defs"]["read_run"]["enum"]
    except (KeyError, TypeError) as exc:
        pytest.fail(f"$defs.read_run.enum 정본 경로가 없다: {exc}")
    default = inspect.signature(read_stage.run).parameters["read_runs"].default
    if list(default) != enum:
        pytest.fail(
            "read_run enum과 run(read_runs=...) 기본값이 순서까지 같지 않다: "
            f"schema={enum!r}, engine={list(default)!r}"
        )


def test_read_run_has_one_definition_three_references_and_one_literal() -> None:
    """T35 — 단일 진원과 네 사용처(T59 로 하나 늘었다)가 다시 서로 다른 값 공간으로 늙지 않게 한다."""
    text, schema = load_schema()
    expected_ref = {"$ref": "#/$defs/read_run"}
    expected_definition = {
        "enum": ["read-a", "read-b"],
        "$comment": (
            "재정 2026-09-02 T32 · 2026-09-05 T35 — 독해 실행 식별자의 단일 진원 · "
            "`reported_by.items` · `canonical_selection.read_run` · `screening_memos[].read_run` · "
            "`review_requests[].read_run`(재정 T59) 넷이 참조한다"
        ),
    }
    if schema["$defs"].get("read_run") != expected_definition:
        pytest.fail(f"$defs.read_run 단일 정의가 재정 T32와 다르다: {schema['$defs'].get('read_run')}")
    reported_by_items = schema["properties"]["unclassified_dependents"]["items"][
        "properties"
    ]["reported_by"]["items"]
    canonical = schema["properties"]["canonical_selection"]["properties"]["read_run"]
    screening_memo = schema["properties"]["screening_memos"]["items"]["properties"]["read_run"]
    if reported_by_items != expected_ref:
        pytest.fail(f"reported_by.items 참조 기대 {expected_ref}, 실제 {reported_by_items}")
    if canonical.get("$ref") != expected_ref["$ref"]:
        pytest.fail(f"canonical_selection.read_run 참조가 없다: {canonical}")
    expected_screening_memo = {
        "$ref": "#/$defs/read_run",
        "$comment": (
            "재정 2026-09-05 T35 ⑴ — 독해 실행 식별자의 단일 진원에 편입(T32 가 남긴 둘째 "
            "자유 문자열). 행위시법 P-U1 — runs/** 기존 산출물 무소급."
        ),
    }
    if screening_memo != expected_screening_memo:
        pytest.fail(f"screening_memos[].read_run 참조가 T35와 다르다: {screening_memo}")

    refs: list[str] = []

    def collect_refs(node) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if ref == expected_ref["$ref"]:
                refs.append(ref)
            for value in node.values():
                collect_refs(value)
        elif isinstance(node, list):
            for value in node:
                collect_refs(value)

    collect_refs(schema)
    # 재정 2026-09-13 T59 ① 이 넷째 참조(`review_requests[].read_run`)를 더했다.
    if len(refs) != 4:
        pytest.fail(f"$defs.read_run 참조 기대 4곳, 실제 {len(refs)}곳")
    review_read_run = schema["properties"]["review_requests"]["items"]["properties"]["read_run"]
    if review_read_run.get("$ref") != expected_ref["$ref"]:
        pytest.fail(f"review_requests[].read_run 이 단일 진원을 참조하지 않는다: {review_read_run}")
    literal_count = text.count('"read-a"')
    if literal_count != 1:
        pytest.fail(f'스키마의 "read-a" 리터럴 기대 1회, 실제 {literal_count}회')
    expected_comment = (
        "정본 지정은 러너가 `read_runs[0]` 로 정해 `canonical_read_run=` 으로 명시 전달한다 · "
        "재료 명세의 `provenance.read_runs` 는 역할 접미(`:canonical`·`:convergence-peer`)를 "
        "든 별개 표기다 · 재정 T32. [정정 T32] 구 문언 「provenance.read_runs[0] 과 같아야 "
        "하며, 그 대조는 스키마 밖이다(러너의 출구 검사 몫)」은 실물과 어긋나므로 폐기한다."
    )
    if canonical.get("$comment") != expected_comment:
        pytest.fail(f"canonical_selection.read_run 정정 기록이 실물 문언과 다르다: {canonical}")


def test_reported_by_max_items_survives_a_third_enum_value() -> None:
    """T35 ⑵ — enum이 셋으로 넓어져도 reported_by의 설계 상한은 둘이다."""
    _, schema = load_schema()
    extended_schema = json.loads(json.dumps(schema))
    extended_schema["$defs"]["read_run"]["enum"] = ["read-a", "read-b", "read-c"]
    fixture_path = os.path.join(
        REPO,
        "tests",
        "fixtures",
        "schema-enforcement",
        "accept",
        "convergence.screening-memos-two-runs.json",
    )
    with open(fixture_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    payload["unclassified_dependents"][0]["reported_by"] = ["read-a", "read-b", "read-c"]

    errors = sorted(
        Draft202012Validator(extended_schema).iter_errors(payload),
        key=lambda error: (list(error.absolute_path), list(error.absolute_schema_path)),
    )
    keywords = [error.validator for error in errors]
    if keywords != ["maxItems"]:
        pytest.fail(
            "확장 enum의 세 고유 실행은 enum·uniqueItems가 아니라 maxItems 하나로 거부되어야 한다: "
            f"keywords={keywords!r}, errors={[error.message for error in errors]!r}"
        )


def test_runner_convergence_reports_validate_against_shared_read_run_enum(tmp_path) -> None:
    """정상 러너가 쓴 early·full 판정서가 새 enum 때문에 거부되면 과잉 제약이다."""
    root, outcome, _ = m21.run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": m2.payload_set(), "read-b": m2.payload_set()},
        },
    )
    if outcome["status"] != "ok":
        pytest.fail(f"정상 READ 통주 status 기대 ok, 실제 {outcome['status']}")
    _, schema = load_schema()
    validator = Draft202012Validator(schema)
    paths = RunPaths(root)
    for label, path in (
        ("convergence-early.json", paths.convergence_early_json),
        ("convergence.json", paths.convergence_json),
    ):
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        errors = sorted(
            validator.iter_errors(payload), key=lambda error: list(error.absolute_path)
        )
        if errors:
            pytest.fail(
                f"러너 산출 {label} 이 convergence/v0 위반: "
                f"{errors[0].json_path} — {errors[0].message}"
            )
