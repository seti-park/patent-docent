# -*- coding: utf-8 -*-
"""M1 독해층 검증기(`reader/lib/**`)의 pytest.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다
(SPEC §8.4 검증 계획표의 '반증 대상' 열과 같은 형식).

`assert` 를 쓰지 않는다 — `python3 -O` 에서 전부 제거되어 망가진 코드가 공허 통과한다
(CLAUDE.md §3). 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고한다.

★ 픽스처는 이 파일 안에서 파이썬 딕셔너리로 구성한다. `tests/fixtures/` 는 다른 레인의
작업 구역이고, 검사기의 시험대가 남의 데이터에 묶이면 두 작업이 서로를 깨뜨린다.
"""

from __future__ import annotations

import ast
import copy
import glob
import json
import os
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from reader.lib import (  # noqa: E402
    CHECK_REGISTRY,
    CheckContext,
    FREEZE_CHECK_IDS,
    READ_CHECK_IDS,
    Rules,
    UNIT_ALIASES,
    load_schema,
    match_key,
    normalize_number,
    normalize_unit,
    ValueGrammarError,
    parse_value,
    render_value,
    run_freeze_checks,
    run_read_checks,
    to_convergence_payload,
)
from reader.lib.normalize import NormalizeError  # noqa: E402
from reader.lib.source_digest import digest_of  # noqa: E402

RULES = Rules.load()
SCHEMA = load_schema()

# ---------------------------------------------------------------------------
# 가공 원천·가공 인스턴스 (SPEC §2.7 의 더미를 이 파일 안에서 재구성한다)
# 실재 특허가 아니며 실재 특허를 인용하지 않는다.
# ---------------------------------------------------------------------------

SOURCE = """# Example Devices — stacked module (fictional example)

## Claims

1. A stacked module comprising: a substrate having a first surface; and a heat spreader thermally coupled to the first surface, the heat spreader defining a fluid channel.

5. The stacked module of claim 1, wherein the fluid channel has a hydraulic diameter of 0.08 mm.

7. The stacked module of claim 1 or claim 5, wherein the fluid channel has a flow path length of 12 mm.

## Brief description of the drawings

FIG. 2 is a section view of the heat spreader.

## Description

[0041] Conventional assemblies stack a cold plate on top of the module, which adds one more thermal interface.

[0042] The heat spreader 210 is bonded to the first surface 112 of the substrate 110. In this arrangement the channel is formed within the spreader so that a separate cold plate is not required, and the thermal interface count is reduced by one.

[0043] The channel cross-section is sized so that the hydraulic diameter is 0.08 mm, and the drawings do not mark this dimension.

[0044] The folded flow path 214 doubles back within the footprint so that the total flow path length is 12 mm.
"""

CLAIM_1 = (
    "A stacked module comprising: a substrate having a first surface; and a heat "
    "spreader thermally coupled to the first surface, the heat spreader defining a "
    "fluid channel."
)
CLAIM_5 = (
    "The stacked module of claim 1, wherein the fluid channel has a hydraulic "
    "diameter of 0.08 mm."
)
CLAIM_7 = (
    "The stacked module of claim 1 or claim 5, wherein the fluid channel has a flow "
    "path length of 12 mm."
)
E1_TEXT = "a substrate having a first surface;"
E2_TEXT = (
    "a heat spreader thermally coupled to the first surface, the heat spreader "
    "defining a fluid channel."
)
A1_TEXT = "wherein the fluid channel has a hydraulic diameter of 0.08 mm"
A2_TEXT = "wherein the fluid channel has a flow path length of 12 mm"
CAPTION = "FIG. 2 is a section view of the heat spreader."
SPEC_QUOTE_M4 = "The heat spreader 210 is bonded to the first surface 112 of the substrate 110."
SPEC_QUOTE_M8 = "the first surface 112 of the substrate 110"
SPEC_QUOTE_M10 = "the hydraulic diameter is 0.08 mm, and the drawings do not mark this dimension"
SPEC_QUOTE_M11 = "The folded flow path 214 doubles back within the footprint"
FACT_QUOTE_M5 = "a hydraulic diameter of 0.08 mm"
FACT_QUOTE_M12 = "the total flow path length is 12 mm"


def _source_span(quote: str) -> dict:
    """원천 파일 기준 **바이트** 오프셋(SPEC §2.4). 손으로 적지 않고 계산한다.

    ★ 이 원천은 머리글에 em dash(3바이트)가 있어 바이트 오프셋 ≠ 문자 오프셋이다 —
    골든 자체가 그 구별의 증인이 되도록 일부러 남겨 둔다.
    """
    data = SOURCE.encode("utf-8")
    target = quote.encode("utf-8")
    start = data.index(target)
    return {"start": start, "end": start + len(target)}


def _value_span(quote: str, value: str) -> dict:
    """`quote` 문자열 내부의 문자 오프셋(0-based, end exclusive)."""
    start = quote.index(value)
    return {"start": start, "end": start + len(value)}


def golden_spec() -> dict:
    """전 검사를 통과해야 하는 가공 인스턴스."""
    return {
        "schema": "material-spec/v0",
        "reader_version": "0.4.0",
        "spec_version": 1,
        "status": "frozen",
        "run_id": "example-xx0000000a1-stacked-module",
        "patent": {
            "number": "XX0000000A1",
            "title": "Stacked module with an integrated fluid channel (fictional example)",
            "assignee": "Example Devices, Inc.",
            "dates": {
                "priority": "2024-03-11",
                "filing": "2025-03-10",
                "publication": "2026-01-15",
            },
            # 손으로 적지 않고 원천에서 계산한다 — 불변식 I1 의 기준점이다.
            "source_digest": digest_of(SOURCE),
            "source_path": "00-source/patent.md",
        },
        "claims": {
            "independent": [
                {
                    "id": "CL-1",
                    "type": "independent",
                    "text_verbatim": CLAIM_1,
                    "elements": [
                        {
                            "id": "CL-1/e1",
                            "text_verbatim": E1_TEXT,
                            "material_id": "M1",
                            "children": [],
                        },
                        {
                            "id": "CL-1/e2",
                            "text_verbatim": E2_TEXT,
                            "material_id": "M2",
                            "children": [],
                        },
                    ],
                }
            ],
            "dependents": [
                {
                    "id": "CL-5",
                    "depends_on": ["CL-1"],
                    "dependency_type": "single",
                    "text_verbatim": CLAIM_5,
                    "additions": [
                        {
                            "id": "CL-5/a1",
                            "attaches_to": "CL-1/e2",
                            "text_verbatim": A1_TEXT,
                            "material_id": "M3",
                        }
                    ],
                },
                {
                    "id": "CL-7",
                    "depends_on": ["CL-1", "CL-5"],
                    "dependency_type": "multiple-or",
                    "text_verbatim": CLAIM_7,
                    "additions": [
                        {
                            "id": "CL-7/a1",
                            "attaches_to": "CL-1/e2",
                            "text_verbatim": A2_TEXT,
                            "material_id": "M9",
                        }
                    ],
                },
            ],
            "applicant_interest": [
                {
                    "claim": "CL-1",
                    "signal": (
                        "The interest is staked on placing the coolant path inside the "
                        "spreader body rather than in a separate part."
                    ),
                    "material_id": "M6",
                }
            ],
        },
        "figures": [
            {
                "id": "FIG-2",
                "numerals": ["110", "112", "210", "214"],
                "caption_quote": CAPTION,
                "raw_path": "00-source/figures-raw/fig-02.png",
                "asset_path": None,
            }
        ],
        "items": [
            {
                "id": "M1",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e1",
                "label_en": "substrate having a first surface",
                "text_verbatim": E1_TEXT,
            },
            {
                "id": "M2",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e2",
                "label_en": "heat spreader that defines the fluid channel in its own body",
                "text_verbatim": E2_TEXT,
            },
            {
                "id": "M3",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-5/a1",
                "label_en": "hydraulic diameter limitation on the fluid channel",
                "text_verbatim": A1_TEXT,
            },
            {
                "id": "M4",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M2",
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [
                    {
                        "locator": "[0042]",
                        "quote": SPEC_QUOTE_M4,
                        "span": _source_span(SPEC_QUOTE_M4),
                    }
                ],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["210", "112"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": "M5",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "hydraulic diameter of the fluid channel",
                "origin": "quoted",
                "value_raw": "0.08 mm",
                "value_normalized": "0.08",
                "value_type": {"kind": "scalar", "approximate": False, "value": "0.08"},
                "unit": "mm",
                "machine_verifiable": True,
                "source": {
                    "locator": "claim 5",
                    "quote": FACT_QUOTE_M5,
                    "value_span": _value_span(FACT_QUOTE_M5, "0.08 mm"),
                },
            },
            {
                "id": "M6",
                "kind": "implication",
                "status": "active",
                "superseded_by": None,
                "statement_en": (
                    "Forming the channel inside the spreader body points at removing a "
                    "cold plate rather than adding one."
                ),
                "basis": "spec",
                "derived_from": ["M2", "M4"],
                "evidence_quotes": [
                    "the channel is formed within the spreader so that a separate cold plate is not required"
                ],
                "confidence": "inferred",
            },
            {
                "id": "M7",
                "kind": "positioning",
                "status": "active",
                "superseded_by": None,
                "background_problem": (
                    "Conventional assemblies put a cold plate on top of the module, which "
                    "adds one more thermal interface."
                ),
                "asserted_effect": (
                    "The specification states in words that the thermal interface count is "
                    "reduced by one."
                ),
                "delta": (
                    "The asserted delta is structural simplification, not a claimed "
                    "performance number."
                ),
                "quotes": [
                    "Conventional assemblies stack a cold plate on top of the module, which adds one more thermal interface.",
                    "the thermal interface count is reduced by one",
                ],
            },
            {
                "id": "M8",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M1",
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [
                    {
                        "locator": "[0042]",
                        "quote": SPEC_QUOTE_M8,
                        "span": _source_span(SPEC_QUOTE_M8),
                    }
                ],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["110", "112"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": "M9",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-7/a1",
                "label_en": "flow path length limitation on the fluid channel",
                "text_verbatim": A2_TEXT,
            },
            {
                "id": "M10",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M3",
                "anchor_state": {"spec": "found", "figure": "not-depicted"},
                "spec_refs": [{"locator": "[0043]", "quote": SPEC_QUOTE_M10}],
                "figure_refs": [],
                "search_note": (
                    "FIG-2 전 도면부호(110·112·210·214)와 캡션을 확인했으나 수력직경 치수는 "
                    "도면에 표기되지 않음."
                ),
            },
            {
                "id": "M11",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M9",
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [{"locator": "[0044]", "quote": SPEC_QUOTE_M11}],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["214"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": "M12",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "total flow path length of the fluid channel",
                "origin": "quoted",
                "value_raw": "12 mm",
                "value_normalized": "12",
                "value_type": {"kind": "scalar", "approximate": False, "value": "12"},
                "unit": "mm",
                "machine_verifiable": True,
                "source": {
                    "locator": "[0044]",
                    "quote": FACT_QUOTE_M12,
                    "value_span": _value_span(FACT_QUOTE_M12, "12 mm"),
                },
            },
            {
                "id": "M13",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "ratio of flow path length to hydraulic diameter",
                "origin": "derived",
                "value_raw": "150",
                "value_normalized": "150",
                "value_type": {"kind": "scalar", "approximate": False, "value": "150"},
                "unit": None,
                "machine_verifiable": True,
                "derivation": {
                    "formula": "length_mm / diameter_mm",
                    "inputs": [
                        {"name": "length_mm", "ref": "M12"},
                        {"name": "diameter_mm", "ref": "M5"},
                    ],
                    "rounding": {"mode": "none", "digits": 0},
                },
            },
            {
                "id": "M14",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "priority date",
                "origin": "bibliographic",
                "value_raw": "2024-03-11",
                "value_normalized": "2024-03-11",
                "value_type": {"kind": "date", "approximate": False, "value": "2024-03-11"},
                "unit": None,
                "machine_verifiable": True,
                "bib_source": {"field": "patent.dates.priority"},
            },
            {
                "id": "M15",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "number of channel passes visible in the section view",
                "origin": "figure-sourced",
                "value_raw": "4",
                "value_normalized": "4",
                "value_type": {"kind": "scalar", "approximate": False, "value": "4"},
                "unit": None,
                "machine_verifiable": False,
                "figure_source": {"figure": "FIG-2", "numerals": ["214"], "locator": "FIG. 2"},
            },
        ],
        "drop_signal": {
            "stage": "final",
            "verdict": "go",
            "reason": "권리 관심이 한 구성에 뚜렷하고, 효과 주장이 명세서 문언으로 존재함.",
        },
        "provenance": {
            "read_runs": ["read-a-0f1c2d3", "read-b-9a8b7c6"],
            "produced_at": "2026-02-01T00:00:00Z",
            "engine_commit": "0000000",
        },
    }


def context(spec: dict, **kwargs) -> CheckContext:
    return CheckContext(
        spec=spec,
        source_text=kwargs.pop("source_text", SOURCE),
        rules=RULES,
        schema=SCHEMA,
        **kwargs,
    )


def run(check_id: str, spec: dict, **kwargs):
    return CHECK_REGISTRY[check_id](context(spec, **kwargs))


def item(spec: dict, item_id: str) -> dict:
    for entry in spec["items"]:
        if entry["id"] == item_id:
            return entry
    raise KeyError(item_id)


def rules_of(row) -> list[str]:
    return [finding.rule for finding in row.findings]


def require_fail(row, rule: str | None = None) -> None:
    if row.status != "fail":
        pytest.fail(f"{row.check_id}: status 기대 fail, 실제 {row.status} (findings={rules_of(row)})")
    if rule is not None and rule not in rules_of(row):
        pytest.fail(f"{row.check_id}: 규칙 {rule} 기대, 실제 {rules_of(row)}")


def require_pass(row) -> None:
    if row.status != "pass":
        detail = "; ".join(f"{f.rule}@{f.locus}: {f.message}" for f in row.findings)
        pytest.fail(f"{row.check_id}: status 기대 pass, 실제 fail — {detail}")


# ---------------------------------------------------------------------------
# 실패 케이스 등재부 — `test_every_registered_check_has_a_failing_case` 의 정본.
# 등재만 하고 시험하지 않는 검사를 막는다.
# ---------------------------------------------------------------------------


def _fail_schema() -> CheckContext:
    spec = golden_spec()
    item(spec, "M1")["kind"] = "widget"
    return context(spec)


def _fail_source_digest() -> CheckContext:
    spec = golden_spec()
    spec["patent"]["source_digest"] = "sha256:" + "0" * 64
    return context(spec)


def _fail_verbatim() -> CheckContext:
    spec = golden_spec()
    item(spec, "M4")["spec_refs"][0]["quote"] = SPEC_QUOTE_M4.replace("112", "122")
    return context(spec)


def _fail_pointer() -> CheckContext:
    spec = golden_spec()
    spec["claims"]["dependents"][0]["additions"][0]["attaches_to"] = "CL-1/e9"
    return context(spec)


def _fail_coverage() -> CheckContext:
    spec = golden_spec()
    spec["items"] = [entry for entry in spec["items"] if entry["id"] != "M4"]
    return context(spec)


def _fail_dependency_parse() -> CheckContext:
    spec = golden_spec()
    spec["claims"]["dependents"][1]["depends_on"] = ["CL-1"]
    spec["claims"]["dependents"][1]["dependency_type"] = "single"
    return context(spec)


def _fail_value_derivation() -> CheckContext:
    spec = golden_spec()
    item(spec, "M5")["value_raw"] = "999 mm"
    return context(spec)


def _fail_claim_inventory() -> CheckContext:
    # 원천에는 청구항 9가 있는데 재료 명세에 등재되지 않은 판.
    extra = SOURCE.replace(
        "## Brief description",
        "9. The stacked module of claim 1, wherein the substrate comprises glass.\n\n"
        "## Brief description",
    )
    return context(golden_spec(), source_text=extra)


def _fail_convergence() -> CheckContext:
    peer = golden_spec()
    elements = peer["claims"]["independent"][0]["elements"]
    elements[1] = {
        "id": "CL-1/e2",
        "text_verbatim": "a heat spreader thermally coupled to the first surface",
        "material_id": "M2",
        "children": [],
    }
    elements.append(
        {
            "id": "CL-1/e3",
            "text_verbatim": "the heat spreader defining a fluid channel.",
            "material_id": "M9",
            "children": [],
        }
    )
    return context(golden_spec(), peer_spec=peer)


def _fail_id_monotonic() -> CheckContext:
    prior = golden_spec()
    prior["items"].append(
        {
            "id": "M16",
            "kind": "component",
            "status": "active",
            "superseded_by": None,
            "claim_ref": "CL-1/e1",
            "label_en": "an item that the revision deleted",
            "text_verbatim": E1_TEXT,
        }
    )
    return context(golden_spec(), prior_spec=prior)


def _fail_payload_immutable() -> CheckContext:
    prior = golden_spec()
    current = golden_spec()
    item(current, "M1")["label_en"] = "quietly rewritten label under the same id"
    return context(current, prior_spec=prior)


FAILING_CASE_BUILDERS = {
    "read.schema": _fail_schema,
    "read.source-digest": _fail_source_digest,
    "read.verbatim": _fail_verbatim,
    "read.pointer-resolve": _fail_pointer,
    "read.coverage": _fail_coverage,
    "read.dependency-parse": _fail_dependency_parse,
    "read.value-derivation": _fail_value_derivation,
    "read.claim-inventory": _fail_claim_inventory,
    "read.convergence": _fail_convergence,
    "freeze.id-monotonic": _fail_id_monotonic,
    "freeze.payload-immutable": _fail_payload_immutable,
}


# ---------------------------------------------------------------------------
# SPEC §8.4 M1 검증 계획표 (17행)
# ---------------------------------------------------------------------------


def test_schema_validates_minimal_instance() -> None:
    """최소 인스턴스가 거부되면 스키마가 과잉 제약."""
    require_pass(run("read.schema", golden_spec()))


def test_schema_rejects_unknown_kind() -> None:
    """`kind` 오타가 통과하면 kind 열거가 무의미."""
    require_fail(CHECK_REGISTRY["read.schema"](_fail_schema()), "schema.validate")


def test_verbatim_rejects_single_char_edit() -> None:
    """quote 를 한 글자 바꾼 변조본이 통과하면 verbatim 검사가 무의미."""
    require_fail(CHECK_REGISTRY["read.verbatim"](_fail_verbatim()), "verbatim.substring")


def test_verbatim_accepts_exact_substring() -> None:
    """정상 인용이 거부되면 검사가 실사용 불가."""
    row = run("read.verbatim", golden_spec())
    require_pass(row)
    if row.checked < 20:
        pytest.fail(f"verbatim 대상 수가 너무 적다: {row.checked} (인용 전량을 세지 않는다)")


def test_pointer_resolution_detects_dangling_attaches_to() -> None:
    """존재하지 않는 `attaches_to` 가 통과하면 포인터 해소 검사가 무의미."""
    require_fail(CHECK_REGISTRY["read.pointer-resolve"](_fail_pointer()), "pointer.resolve")


def test_coverage_flags_ungrounded_element() -> None:
    """접지 없는 청구항 element 가 통과하면 커버리지 검사가 무의미."""
    require_fail(CHECK_REGISTRY["read.coverage"](_fail_coverage()), "coverage.grounded")


def test_convergence_jaccard_below_threshold_fails() -> None:
    """0.95 미만 쌍이 pass 면 수렴 임계가 집행되지 않음."""
    row = CHECK_REGISTRY["read.convergence"](_fail_convergence())
    require_fail(row, "element-set")


def test_material_id_append_only_rejects_renumber() -> None:
    """개정본이 `M7` 을 다른 내용으로 재사용해도 통과하면 ID 규율 붕괴."""
    prior = golden_spec()
    current = golden_spec()
    reused = item(current, "M7")
    reused["background_problem"] = "A different background problem under the same id."
    row = CHECK_REGISTRY["freeze.payload-immutable"](context(current, prior_spec=prior))
    require_fail(row, "lifecycle.payload-frozen")


def test_reader_version_matches_schema_major() -> None:
    """버전과 `material-spec/vN` 이 어긋나도 통과하면 semver 정책이 문서로만 존재."""
    with open(os.path.join(REPO, "reader", "READER-VERSION"), encoding="utf-8") as handle:
        version = handle.read().strip()
    line = SCHEMA["properties"]["schema"]["const"]
    major = version.split(".")[0]
    expected_line = f"material-spec/v{major}"
    if line != expected_line:
        pytest.fail(f"READER-VERSION={version} 인데 계약 라인은 {line} (기대 {expected_line})")


def test_dependency_parse_matches_multiple_dependency_array() -> None:
    """다중 종속 원문("claim 1 or claim 5")과 `depends_on[]` 이 어긋나도 통과하면 종속 구조가 다시 손실 표현이 됨."""
    require_pass(run("read.dependency-parse", golden_spec()))
    row = CHECK_REGISTRY["read.dependency-parse"](_fail_dependency_parse())
    require_fail(row, "parse.set-equals")


def test_value_span_mismatch_is_rejected() -> None:
    """인용문과 어긋난 `value_span` 이 통과하면 "실재하는 인용 + 날조된 수치"가 정답지에 들어감."""
    spec = golden_spec()
    item(spec, "M5")["source"]["value_span"] = {"start": 0, "end": 7}
    require_fail(run("read.value-derivation", spec), "value.quoted-span")


def test_derived_value_recomputation_mismatch_is_rejected() -> None:
    """산식 재계산 불일치가 통과하면 파생 수치가 사실상 자유 기입이 됨."""
    spec = golden_spec()
    derived = item(spec, "M13")
    derived["value_normalized"] = "15"
    derived["value_raw"] = "15"
    derived["value_type"] = {"kind": "scalar", "approximate": False, "value": "15"}
    require_fail(run("read.value-derivation", spec), "value.derived-recompute")


def test_figure_sourced_fact_is_listed_for_manual_verification() -> None:
    """`machine_verifiable: false` 항목이 CP1 목록에 오르지 않으면 "검증 불가"가 "검증 완료"로 조용히 바뀜."""
    row = run("read.value-derivation", golden_spec())
    require_pass(row)
    manual = row.extras["manual_verification_required"]
    ids = [entry["material_id"] for entry in manual]
    if ids != ["M15"]:
        pytest.fail(f"manual_verification_required 기대 ['M15'], 실제 {ids}")
    if manual[0]["reason"] != "figure-sourced" or manual[0]["figure"] != "FIG-2":
        pytest.fail(f"수집 항목의 사유·도면이 다르다: {manual[0]}")


def test_dependent_with_empty_additions_is_rejected() -> None:
    """빈 `additions` 가 통과하면 "전 구성요소 3중 접지"가 접지할 것이 없어서 공허 통과한다."""
    spec = golden_spec()
    spec["claims"]["dependents"][0]["additions"] = []
    require_fail(run("read.schema", spec), "schema.validate")


def test_hangul_in_en_field_is_rejected() -> None:
    """한국어 `label_en` 이 통과하면 EN 단일 정책이 문서로만 존재하고 historian 이 받는 값의 언어가 런마다 달라짐."""
    spec = golden_spec()
    item(spec, "M1")["label_en"] = "제1 표면을 갖는 기판"
    require_fail(run("read.schema", spec), "schema.validate")
    require_fail(run("read.value-derivation", spec), "value.en-only")


def test_origin_mixed_attachment_is_rejected() -> None:
    """`quoted` 항목이 `derivation` 을 함께 갖는 것이 통과하면 provenance 가 두 갈래로 갈려 어느 쪽이 근거인지 판정 불가."""
    spec = golden_spec()
    item(spec, "M5")["derivation"] = {
        "formula": "a * 2",
        "inputs": [{"name": "a", "ref": "M12"}],
        "rounding": {"mode": "none", "digits": 0},
    }
    require_fail(run("read.schema", spec), "schema.validate")


def test_derived_fact_of_derived_fact_is_rejected() -> None:
    """파생의 파생이 통과하면 원문 스팬까지의 거리가 무한해지고 재계산 대조가 사슬 어딘가에서 끊김(재정 N9 의 깊이 1)."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": "M16",
            "kind": "fact",
            "status": "active",
            "superseded_by": None,
            "label_en": "ratio derived from another derived value",
            "origin": "derived",
            "value_raw": "300",
            "value_normalized": "300",
            "value_type": {"kind": "scalar", "approximate": False, "value": "300"},
            "unit": None,
            "machine_verifiable": True,
            "derivation": {
                "formula": "ratio * 2",
                "inputs": [{"name": "ratio", "ref": "M13"}],
                "rounding": {"mode": "none", "digits": 0},
            },
        }
    )
    require_fail(run("read.value-derivation", spec), "value.depth-one")


# ---------------------------------------------------------------------------
# 추가 요건 (발주 §6)
# ---------------------------------------------------------------------------


def test_normalization_table_matches_l0_contract() -> None:
    """정규화 표가 두 벌로 갈리면 재료와 본문이 다른 MATCH_KEY 를 만들어 숫자 전수 대조가 성립하지 않는다."""
    with open(os.path.join(REPO, "contracts", "l0-format.yaml"), encoding="utf-8") as handle:
        l0 = yaml.safe_load(handle)
    contract_aliases = l0["numeric"]["normalization"]["unit_aliases"]
    if dict(contract_aliases) != dict(UNIT_ALIASES):
        pytest.fail(
            "단위 별칭 사전이 다르다 — "
            f"l0-format={contract_aliases} vs normalize.UNIT_ALIASES={UNIT_ALIASES}"
        )
    # l0 정규화 문언 각 항의 (입력, 기대) — 문언이 바뀌면 여기가 먼저 깨져야 한다.
    cases = [
        ("1,200", "1200"),        # thousands_separator: ',' 제거
        ("0.80", "0.8"),          # decimals: 후행 0 제거
        ("0.8", "0.8"),           # decimals: 선행 0 보존
        (".8", "0.8"),            # decimals: .8 → 0.8
        ("١٢", "12"),             # unicode_digits: ASCII 로 정규화
        ("1.2e3", "1200"),        # 과학표기 전개(reader-rules 측 문언)
        ("+5", "5"),              # 선행 + 제거
        ("-0.50", "-0.5"),        # 선행 - 보존 + 후행 0 제거
    ]
    for raw, expected in cases:
        actual = normalize_number(raw)
        if actual != expected:
            pytest.fail(f"normalize_number({raw!r}) 기대 {expected!r}, 실제 {actual!r}")
    if normalize_unit("UM") != "µm" or normalize_unit("Micron") != "µm":
        pytest.fail(f"단위 별칭 적용 실패: UM→{normalize_unit('UM')}, Micron→{normalize_unit('Micron')}")
    if match_key("0.08", "mm") != "0.08|mm" or match_key("12", None) != "12|":
        pytest.fail("MATCH_KEY 서식이 l0-format §9 numeric.match_key 와 다르다")
    with pytest.raises(NormalizeError):
        normalize_number("1e40")  # 전개 자릿수 30 초과 = 실패


def test_claim_inventory_detects_missing_source_claim() -> None:
    """원천에 있는 청구항이 등재되지 않아도 통과하면, 커버리지는 남은 것들끼리의 접지만 보므로 청구항 하나가 통째로 사라진다."""
    row = CHECK_REGISTRY["read.claim-inventory"](_fail_claim_inventory())
    require_fail(row, "inventory.registered-superset")
    require_pass(run("read.claim-inventory", golden_spec()))


def test_claim_inventory_rejects_zero_parsed_claims() -> None:
    """파싱 0건이 통과가 되면 그 아래 전 대조가 공허하게 통과한다(공허 통과는 통과가 아니다)."""
    empty = "# Example\n\n## Claims\n\n(no claims were converted)\n\n## Description\n\ntext\n"
    row = run("read.claim-inventory", golden_spec(), source_text=empty)
    require_fail(row, "inventory.non-empty")
    if row.vacuous != "empty-target":
        pytest.fail(f"대상 0건인데 vacuous={row.vacuous} (공허가 행에 드러나지 않는다)")


def test_convergence_detects_same_elements_different_tree() -> None:
    """element 집합만 보면 같은 문자열이 서로 다른 계층으로 조립되어도 수렴한 것으로 판정된다(재감수 M-07 구조 축)."""
    peer = golden_spec()
    elements = peer["claims"]["independent"][0]["elements"]
    nested = elements.pop(1)
    nested["id"] = "CL-1/e1/e1"
    elements[0]["children"] = [nested]
    for dependent in peer["claims"]["dependents"]:
        dependent["additions"][0]["attaches_to"] = "CL-1/e1/e1"
    row = run("read.convergence", golden_spec(), peer_spec=peer)
    require_fail(row, "tree-edges")
    if "element-set" in rules_of(row):
        pytest.fail("element 집합 축이 함께 실패했다 — 구조 축의 독립성을 시험하지 못한다")


def test_payload_change_under_same_id_is_rejected() -> None:
    """개정본이 기존 `active` 항목 내용을 조용히 바꿔도 통과하면 고정되는 것은 ID 뿐이고 의미가 아니다."""
    row = CHECK_REGISTRY["freeze.payload-immutable"](_fail_payload_immutable())
    require_fail(row, "lifecycle.payload-frozen")
    # 상태 변경(active → retracted)은 payload 대상이 아니므로 통과해야 한다.
    prior = golden_spec()
    current = golden_spec()
    item(current, "M5")["status"] = "retracted"
    require_pass(CHECK_REGISTRY["freeze.payload-immutable"](context(current, prior_spec=prior)))


def test_supersession_chain_terminal_must_be_active() -> None:
    """2차 승계에서 종단을 보지 않으면 인용의 수정 지시가 죽은 항목을 지목한다."""
    spec = golden_spec()
    chain = [
        ("M16", "superseded", "M17"),
        ("M17", "superseded", "M18"),
        ("M18", "active", None),
    ]
    for item_id, status, following in chain:
        spec["items"].append(
            {
                "id": item_id,
                "kind": "component",
                "status": status,
                "superseded_by": following,
                "claim_ref": "CL-1/e1",
                "label_en": f"chain member {item_id}",
                "text_verbatim": E1_TEXT,
            }
        )
    require_pass(CHECK_REGISTRY["freeze.payload-immutable"](context(spec)))

    dead = copy.deepcopy(spec)
    item(dead, "M18")["status"] = "retracted"
    require_fail(
        CHECK_REGISTRY["freeze.payload-immutable"](context(dead)),
        "supersession.terminal-active",
    )


def test_lifecycle_transition_is_one_way() -> None:
    """종단 상태에서 되돌아오는 전이가 통과하면 철회·교체 기록이 뒤집힐 수 있다."""
    prior = golden_spec()
    item(prior, "M5")["status"] = "retracted"
    current = golden_spec()  # M5 는 active
    require_fail(
        CHECK_REGISTRY["freeze.payload-immutable"](context(current, prior_spec=prior)),
        "lifecycle.one-way",
    )


def test_value_type_mismatch_with_value_raw_is_rejected() -> None:
    """범위를 스칼라로 뭉개 담아도 통과하면 게이트가 그 값에서 문자열 일치 여부밖에 판정하지 못한다."""
    spec = golden_spec()
    fact = item(spec, "M5")
    fact["value_raw"] = "0.05-0.10 mm"
    fact["source"] = {
        "locator": "[0043]",
        "quote": "a hydraulic diameter of 0.05-0.10 mm",
        "value_span": {"start": 24, "end": 36},
    }
    row = run("read.value-derivation", spec)
    require_fail(row, "value.type-agrees")
    # 문법 자체는 범위를 담을 수 있어야 한다(과잉 거부 배제).
    parsed = parse_value("0.05-0.10 mm", "mm", RULES)
    if parsed["kind"] != "range" or render_value(parsed, RULES) != "0.05-0.1":
        pytest.fail(f"범위 파싱·렌더가 규칙 문언과 다르다: {parsed}")


def test_fabricated_value_raw_with_valid_quote_is_rejected() -> None:
    """인용문은 실재하는데 `value_raw` 만 날조한 판이 통과하면 그 값이 곧 숫자 게이트의 정답지가 된다(재감수 B-04)."""
    row = CHECK_REGISTRY["read.value-derivation"](_fail_value_derivation())
    require_fail(row, "value.quoted-span")
    # verbatim 검사는 이 변조를 잡지 못한다 — 그래서 검사 6 이 따로 필요하다.
    spec = golden_spec()
    item(spec, "M5")["value_raw"] = "999 mm"
    require_pass(run("read.verbatim", spec))


def test_self_referencing_derivation_input_is_rejected() -> None:
    """`derivation.inputs[].ref` 자기참조가 통과하면 원문 스팬까지의 거리가 정의되지 않는다(재감수 B-02 validator-scope)."""
    spec = golden_spec()
    item(spec, "M13")["derivation"]["inputs"][0] = {"name": "length_mm", "ref": "M13"}
    require_fail(run("read.pointer-resolve", spec), "pointer.no-self-reference")


def test_reference_graph_cycle_is_rejected() -> None:
    """2항 순환이 통과하면 참조 그래프에 종단이 없어 해소가 무한 루프가 된다."""
    spec = golden_spec()
    item(spec, "M6")["derived_from"] = ["M16"]
    spec["items"].append(
        {
            "id": "M16",
            "kind": "implication",
            "status": "active",
            "superseded_by": None,
            "statement_en": "An implication that points back at the first one.",
            "basis": "spec",
            "derived_from": ["M6"],
            "evidence_quotes": ["the thermal interface count is reduced by one"],
            "confidence": "inferred",
        }
    )
    require_fail(run("read.pointer-resolve", spec), "pointer.acyclic")


def test_check_row_validates_against_verdict_check_row_schema() -> None:
    """행 서식이 계약과 어긋나면 게이트 판정문 전체가 서식 밖에서 보고된다(재정 N5)."""
    with open(
        os.path.join(REPO, "contracts", "schemas", "verdict-check-row.schema.json"),
        encoding="utf-8",
    ) as handle:
        row_schema = json.load(handle)
    validator = Draft202012Validator(row_schema)

    spec = golden_spec()
    rows = list(run_read_checks(context(spec, peer_spec=golden_spec())))
    rows += list(run_freeze_checks(context(spec, prior_spec=golden_spec())))
    rows += list(run_read_checks(context(spec)))  # peer 없음 = 공허 경로
    for builder in FAILING_CASE_BUILDERS.values():
        ctx = builder()
        for check_id in READ_CHECK_IDS + FREEZE_CHECK_IDS:
            rows.append(CHECK_REGISTRY[check_id](ctx))

    for row in rows:
        errors = sorted(validator.iter_errors(row.to_row_dict()), key=str)
        if errors:
            pytest.fail(
                f"{row.check_id} 의 행이 verdict-check-row/v0 를 통과하지 못했다: "
                f"{row.to_row_dict()} / {errors[0].message}"
            )


def test_every_registered_check_has_a_failing_case() -> None:
    """등재만 하고 시험하지 않은 검사가 있으면 그 검사는 언제 깨졌는지 아무도 모른다."""
    missing = sorted(set(CHECK_REGISTRY) - set(FAILING_CASE_BUILDERS))
    if missing:
        pytest.fail(f"실패 케이스가 없는 등재 검사: {missing}")
    for check_id, builder in sorted(FAILING_CASE_BUILDERS.items()):
        row = CHECK_REGISTRY[check_id](builder())
        if row.status != "fail":
            pytest.fail(f"{check_id}: 실패 케이스가 실패하지 않는다 (findings={rules_of(row)})")


def test_no_assert_in_library_sources() -> None:
    """라이브러리에 `assert` 가 남으면 `python3 -O` 에서 검사가 통째로 사라진다."""
    offenders = []
    for path in sorted(glob.glob(os.path.join(REPO, "reader", "lib", "*.py"))):
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                offenders.append(f"{os.path.relpath(path, REPO)}:{node.lineno}")
    if offenders:
        pytest.fail(f"reader/lib 에 assert 가 있다: {offenders}")


# ---------------------------------------------------------------------------
# 통합 — 골든 인스턴스와 산출 서식
# ---------------------------------------------------------------------------


def test_golden_instance_passes_every_read_check() -> None:
    """골든이 통과하지 못하면 이하 모든 실패 케이스가 '무엇 때문에' 실패했는지 말할 수 없다."""
    rows = run_read_checks(context(golden_spec(), peer_spec=golden_spec()))
    ids = [row.check_id for row in rows]
    if ids != list(READ_CHECK_IDS):
        pytest.fail(f"검사 순서가 다르다: {ids}")
    for row in rows:
        require_pass(row)
        if row.vacuous != "none":
            pytest.fail(f"{row.check_id}: 골든에서 vacuous={row.vacuous} (대상이 비었다)")


def test_convergence_payload_carries_three_cp1_blocks() -> None:
    """세 블록이 빠지면 CP1 표면이 '기계가 무엇을 보증하지 못했는가'를 보여주지 못한다(재정 R1·R3·N9)."""
    spec = golden_spec()
    rows = run_read_checks(context(spec, peer_spec=golden_spec()))
    payload = to_convergence_payload(rows, spec)
    if payload["schema"] != "convergence/v0" or payload["run_id"] != spec["run_id"]:
        pytest.fail(f"산출 머리가 다르다: {payload['schema']} / {payload['run_id']}")
    if len(payload["checks"]) != len(READ_CHECK_IDS):
        pytest.fail(f"checks 행 수가 다르다: {len(payload['checks'])}")
    classification = payload["fact_classification"]
    # 서지 복사는 원문 스팬과 같은 갈래로 계수하되 정체는 `bibliographic_ids` 로 드러난다(§1.4).
    if classification["quoted_span"]["material_ids"] != ["M5", "M12", "M14"]:
        pytest.fail(f"수치 3분류의 원문 스팬 갈래가 다르다: {classification['quoted_span']}")
    if [entry["material_id"] for entry in classification["derived"]] != ["M13"]:
        pytest.fail(f"파생 갈래가 다르다: {classification['derived']}")
    if [entry["material_id"] for entry in classification["figure_sourced"]] != ["M15"]:
        pytest.fail(f"도면 유래 갈래가 다르다: {classification['figure_sourced']}")
    if classification["bibliographic_ids"] != ["M14"]:
        pytest.fail(f"서지 갈래가 다르다: {classification['bibliographic_ids']}")
    if [entry["material_id"] for entry in payload["manual_verification_required"]] != ["M15"]:
        pytest.fail("도면 유래 수치가 사람 검증 목록에 오르지 않았다")
    exceptions = payload["grounding_exceptions"]
    if [entry["material_id"] for entry in exceptions] != ["M10"]:
        pytest.fail(f"접지 예외 전량 노출이 어긋난다: {exceptions}")
    if exceptions[0]["figure"] != "not-depicted" or not exceptions[0]["search_note"]:
        pytest.fail(f"접지 예외 항목의 신고 내용이 비었다: {exceptions[0]}")


def test_convergence_payload_validates_against_contract() -> None:
    """산출 서식이 `convergence/v0` 계약과 어긋나면 READ 의 보고서가 파이프라인 밖 서식이 된다."""
    with open(
        os.path.join(REPO, "contracts", "schemas", "convergence.schema.json"),
        encoding="utf-8",
    ) as handle:
        payload_schema = json.load(handle)
    validator = Draft202012Validator(payload_schema)

    spec = golden_spec()
    for peer in (golden_spec(), None):  # 2회차 있는 런과 없는 런(공허 경로) 둘 다
        rows = run_read_checks(context(spec, peer_spec=peer))
        payload = to_convergence_payload(rows, spec)
        errors = sorted(validator.iter_errors(payload), key=str)
        if errors:
            pytest.fail(
                f"convergence 산출이 계약을 통과하지 못했다(peer={'있음' if peer else '없음'}): "
                f"{errors[0].json_path} — {errors[0].message}"
            )
        if peer is None and payload["vacuous_pass"] != ["read.convergence"]:
            pytest.fail(f"공허 행 파생이 어긋난다: {payload['vacuous_pass']}")


def test_convergence_without_peer_is_marked_vacuous_not_passed() -> None:
    """2회차 없는 런이 수렴 통과로 보이면 재현성 검사가 있는 척만 하게 된다."""
    rows = {row.check_id: row for row in run_read_checks(context(golden_spec()))}
    row = rows["read.convergence"]
    if row.checked != 0 or row.violations != 0:
        pytest.fail(f"peer 없음인데 checked={row.checked}, violations={row.violations}")
    if row.vacuous != "empty-target" or not row.extras.get("skipped"):
        pytest.fail(f"공허 표기가 없다: vacuous={row.vacuous}, extras={row.extras}")


def test_coverage_counts_dependent_additions_as_required() -> None:
    """종속항 부가 한정이 필수 대상에서 빠지면 '전 구성요소 접지'가 독립항만 보는 검사가 된다(재정 R3)."""
    row = run("read.coverage", golden_spec())
    require_pass(row)
    if row.extras["required"] != 4:
        pytest.fail(f"접지 필수 대상 수 기대 4(element 2 + addition 2), 실제 {row.extras['required']}")
    # 행의 `checked` 는 접지 대상 + 고아 판정 대상(active component 4건)이다.
    if row.checked != 8:
        pytest.fail(f"검사 대상 수 기대 8, 실제 {row.checked}")


def test_coverage_rejects_shared_component_and_reverse_mismatch() -> None:
    """1:1 과 역참조를 보지 않으면 접지 1건이 두 구성요소를 덮고도 통과한다(재감수 B-02)."""
    shared = golden_spec()
    shared["claims"]["dependents"][1]["additions"][0]["material_id"] = "M3"
    require_fail(run("read.coverage", shared), "coverage.material-id-unique")

    reversed_spec = golden_spec()
    item(reversed_spec, "M3")["claim_ref"] = "CL-1/e1"
    require_fail(run("read.coverage", reversed_spec), "coverage.claim-ref-reverse")


def test_cross_claim_text_is_caught_by_inventory_not_verbatim() -> None:
    """두 검사의 관할이 겹치면 어느 쪽이 그 결함을 지키는지 확정할 수 없고, 한쪽을 고칠 때 다른 쪽이 조용히 방어를 떠맡는다."""
    spec = golden_spec()
    # CL-5 의 전문 자리에 CL-7 의 문장을 넣는다 — 청구항 절 안에는 실재하는 문장이다.
    spec["claims"]["dependents"][0]["text_verbatim"] = CLAIM_7
    require_pass(run("read.verbatim", spec))  # verbatim = "원문에 있는 말인가"
    require_fail(run("read.claim-inventory", spec), "inventory.text-in-own-claim")  # = "제자리인가"

    # 절 밖(설명부)의 문장을 청구항 전문에 넣으면 그때는 verbatim 이 잡는다.
    outside = golden_spec()
    outside["claims"]["dependents"][0]["text_verbatim"] = SPEC_QUOTE_M4
    require_fail(run("read.verbatim", outside), "verbatim.claim-section")


def test_orphan_component_item_is_rejected() -> None:
    """커버리지는 청구항 쪽에서 세므로, 청구항이 통째로 빠지면 셀 대상도 함께 빠져 통과한다 — 남는 흔적이 고아 성분 항목이다."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": "M16",
            "kind": "component",
            "status": "active",
            "superseded_by": None,
            "claim_ref": "CL-1/e1",
            "label_en": "a component item that no element points at",
            "text_verbatim": E1_TEXT,
        }
    )
    require_fail(run("read.coverage", spec), "coverage.no-orphan-component")

    # 물러난 항목은 대상이 아니다 — 개정의 자취를 고아로 잡으면 append-only 규율과 충돌한다.
    retired = copy.deepcopy(spec)
    item(retired, "M16")["status"] = "retracted"
    require_pass(run("read.coverage", retired))


def test_standalone_retracted_item_is_not_a_chain_violation() -> None:
    """단독 철회 항목을 사슬 위반으로 읽으면 정상 개정본이 통과하지 못한다(retracted = 대체물 없음)."""
    spec = golden_spec()
    item(spec, "M5")["status"] = "retracted"  # superseded_by 는 null 그대로
    require_pass(CHECK_REGISTRY["freeze.payload-immutable"](context(spec)))
    definition = RULES.item_lifecycle["supersession_chain"].get("chain_definition")
    if not definition:
        pytest.fail("규칙 파일에 chain_definition 이 없다 — 사슬의 출발점 정의가 문언에 없다")


def test_reference_cycle_edges_cover_all_four_link_kinds() -> None:
    """간선 4종 중 하나라도 빠지면 그 링크로 만든 순환은 영원히 보이지 않는다."""
    from reader.lib.pointers import GRAPH_FIELDS

    expected = {
        "derivation.inputs[].ref",
        "derived_from[]",
        "superseded_by",
        "grounding.component",
    }
    if set(GRAPH_FIELDS) != expected:
        pytest.fail(f"간선 집합이 계약과 다르다: {sorted(GRAPH_FIELDS)}")


def test_dependency_parse_rejects_unparsable_citation() -> None:
    """파싱 불능이 침묵 통과하면 읽지 못한 어형이 조용히 사라진다(parse.no-silent-pass)."""
    spec = golden_spec()
    spec["claims"]["dependents"][0]["text_verbatim"] = "The stacked module of the preceding claim."
    require_fail(run("read.dependency-parse", spec), "parse.no-silent-pass")


def test_bibliographic_date_fact_passes_value_grammar() -> None:
    """서지 날짜(§2.7 M14 형태)가 파싱되지 않으면 M1 DoD 1행("예시 인스턴스가 전 검사 통과")이 성립하지 않는다."""
    spec = golden_spec()
    fact = item(spec, "M14")
    if fact["origin"] != "bibliographic" or fact["value_type"]["kind"] != "date":
        pytest.fail(f"골든의 서지 사실이 §2.7 M14 형태가 아니다: {fact}")
    require_pass(run("read.value-derivation", spec))
    require_pass(run("read.schema", spec))
    parsed = parse_value("2024-03-11", None, RULES, expect_kind="date")
    if parsed != {"kind": "date", "approximate": False, "value": "2024-03-11"}:
        pytest.fail(f"날짜 파싱 결과가 다르다: {parsed}")
    if render_value(parsed, RULES) != "2024-03-11":
        pytest.fail("날짜 렌더가 원값과 다르다 — 날짜를 수치로 정규화하면 안 된다")


def test_bibliographic_patent_number_requires_identifier_kind() -> None:
    """공개번호가 `scalar` 로 통과하면 서지 식별자가 정답지에 '수치'로 한 건 늘어난다."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": "M16",
            "kind": "fact",
            "status": "active",
            "superseded_by": None,
            "label_en": "publication number",
            "origin": "bibliographic",
            "value_raw": "XX0000000A1",
            "value_normalized": "XX0000000A1",
            "value_type": {"kind": "identifier", "approximate": False, "value": "XX0000000A1"},
            "unit": None,
            "machine_verifiable": True,
            "bib_source": {"field": "patent.number"},
        }
    )
    require_pass(run("read.value-derivation", spec))

    wrong = copy.deepcopy(spec)
    item(wrong, "M16")["value_type"] = {"kind": "scalar", "approximate": False, "value": "0"}
    require_fail(run("read.value-derivation", wrong), "value.origin-kind-binding")


def test_thousands_separator_does_not_split_into_set() -> None:
    """`1,200` 이 집합 {1, 200} 으로 읽히면 같은 블록의 두 조항(천단위 제거 vs 집합 구분자)이 서로를 무효화한다."""
    parsed = parse_value("1,200", None, RULES)
    if parsed != {"kind": "scalar", "approximate": False, "value": "1200"}:
        pytest.fail(f"1,200 파싱 결과가 다르다: {parsed}")
    if parse_value("12,345,678", None, RULES)["value"] != "12345678":
        pytest.fail("연속 천단위 구분자가 제거되지 않는다")
    with pytest.raises(ValueGrammarError):
        parse_value("1,2345", None, RULES)  # 세 자리가 아니면 천단위가 아니다 — 시끄럽게 실패


def test_set_members_require_spaced_separator() -> None:
    """쉼표 뒤 공백을 요구하지 않으면 천단위 구분자와 원소 구분자가 갈리지 않는다."""
    parsed = parse_value("4, 8, 16", None, RULES)
    if parsed["kind"] != "set" or parsed["members"] != ["4", "8", "16"]:
        pytest.fail(f"집합 파싱 결과가 다르다: {parsed}")
    if parse_value("4 or 8", None, RULES)["members"] != ["4", "8"]:
        pytest.fail("`or` 구분자가 동작하지 않는다")
    with pytest.raises(ValueGrammarError):
        parse_value("4,8", None, RULES)


def test_fraction_is_a_parse_failure() -> None:
    """`1/2` 가 집합 {1, 2} 로 읽히면 "분수는 파싱 실패" 규정이 한 번도 발동할 수 없는 죽은 문언이 된다."""
    with pytest.raises(ValueGrammarError):
        parse_value("1/2", None, RULES)


def test_set_render_does_not_collide_with_match_key() -> None:
    """집합 렌더에 `|` 가 들어가면 MATCH_KEY(`{value}|{unit}`)에서 값과 단위의 경계가 사라진다."""
    rendered = render_value(parse_value("4, 8, 16", None, RULES), RULES)
    if "|" in rendered:
        pytest.fail(f"집합 렌더에 MATCH_KEY 구분자가 들어 있다: {rendered}")
    key = match_key(rendered, "mm")
    if key.count("|") != 1:
        pytest.fail(f"MATCH_KEY 에 구분자가 둘 이상이다: {key}")


def test_negative_zero_normalizes_to_zero() -> None:
    """`-0` 이 살아남으면 같은 수가 두 표기를 갖고 MATCH_KEY 가 두 벌이 된다."""
    for raw in ("-0", "-0.0", "-0.00"):
        result = normalize_number(raw)
        if result != "0":
            pytest.fail(f"normalize_number({raw!r}) 기대 '0', 실제 {result!r}")


def test_negative_zero_is_rejected_by_schema_decimal() -> None:
    """스키마가 `-0` 을 받아주면 정규화 구현이 되돌아가도 아무도 알아채지 못한다."""
    validator = Draft202012Validator({"$ref": "#/$defs/decimal", "$defs": SCHEMA["$defs"]})
    for bad in ("-0", "-0.0"):
        if validator.is_valid(bad):
            pytest.fail(f"스키마가 {bad!r} 를 통과시킨다")
    for good in ("0", "-0.5", "1200"):
        if not validator.is_valid(good):
            pytest.fail(f"스키마가 정상 십진 {good!r} 를 거부한다")


def test_identifier_with_space_is_rejected() -> None:
    """공백 낀 식별자가 통과하면 같은 번호의 두 표기가 정답지에 들어가 숫자 전수 대조가 갈라진다."""
    with pytest.raises(ValueGrammarError):
        parse_value("US 2026/0147854 A1", None, RULES, expect_kind="identifier")
    parsed = parse_value("US20260147854A1", None, RULES, expect_kind="identifier")
    if parsed["value"] != "US20260147854A1":
        pytest.fail(f"정본 형태 식별자 파싱 결과가 다르다: {parsed}")


def test_date_kind_is_tried_before_range() -> None:
    """날짜가 범위보다 늦게 시도되면 ISO 날짜의 하이픈이 범위 구분자로 오독될 여지가 남는다."""
    ranks = {form["kind"]: form["rank"] for form in RULES.value_forms}
    if ranks.get("date") >= ranks.get("range"):
        pytest.fail(f"어형 우선순위가 뒤집혔다: date={ranks.get('date')} range={ranks.get('range')}")
    if ranks.get("identifier") <= ranks.get("scalar"):
        pytest.fail("식별자가 수치보다 먼저 시도된다 — 모든 수치를 삼킨다")
    parsed = parse_value("2024-03-11", None, RULES)  # expect_kind 없이도 날짜로 읽힌다
    if parsed["kind"] != "date":
        pytest.fail(f"날짜가 {parsed['kind']} 로 읽혔다")


def test_derived_input_cannot_be_a_date() -> None:
    """날짜·식별자가 산식 입력으로 통과하면 "원문 스팬에서 왔다"가 "수다"로 둔갑한다."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": "M16",
            "kind": "fact",
            "status": "active",
            "superseded_by": None,
            "label_en": "date read from the specification body",
            "origin": "quoted",
            "value_raw": "2024-03-11",
            "value_normalized": "2024-03-11",
            "value_type": {"kind": "date", "approximate": False, "value": "2024-03-11"},
            "unit": None,
            "machine_verifiable": True,
            "source": {
                "locator": "[0041]",
                "quote": "2024-03-11 is the priority date",
                "value_span": {"start": 0, "end": 10},
            },
        }
    )
    item(spec, "M13")["derivation"]["inputs"][0] = {"name": "length_mm", "ref": "M16"}
    require_fail(run("read.value-derivation", spec), "value.input-not-arithmetic")


def test_spec_ref_span_is_byte_offset() -> None:
    """`span` 을 문자 오프셋으로 읽으면 ASCII 원천에서만 우연히 맞고, 한글 한 줄이 섞이는 순간 전 인용이 어긋난다."""
    # 앞에 멀티바이트 문자가 있어 바이트 오프셋 ≠ 문자 오프셋인 원천.
    prefix = "# 한글 주석 — 이 줄이 바이트와 문자를 갈라놓는다\n\n"
    source = prefix + SOURCE
    spec = golden_spec()
    spec["patent"]["source_digest"] = digest_of(source)
    quote = SPEC_QUOTE_M4
    byte_start = source.encode("utf-8").index(quote.encode("utf-8"))
    char_start = source.index(quote)
    if byte_start == char_start:
        pytest.fail("표본 원천이 바이트≠문자를 만들지 못했다 — 이 테스트가 공허하다")

    item(spec, "M4")["spec_refs"][0]["span"] = {
        "start": byte_start,
        "end": byte_start + len(quote.encode("utf-8")),
    }
    item(spec, "M8")["spec_refs"][0]["span"] = None
    item(spec, "M8")["spec_refs"][0].pop("span")
    require_pass(run("read.verbatim", spec, source_text=source))

    wrong = copy.deepcopy(spec)
    item(wrong, "M4")["spec_refs"][0]["span"] = {
        "start": char_start,
        "end": char_start + len(quote),
    }
    require_fail(run("read.verbatim", wrong, source_text=source), "verbatim.span")


def test_value_span_is_character_offset() -> None:
    """`value_span` 을 바이트로 읽으면 인용문에 한글·기호가 섞인 순간 정상 수치가 날조로 판정된다."""
    spec = golden_spec()
    fact = item(spec, "M5")
    quote = "치수 표기 — a hydraulic diameter of 0.08 mm"
    fact["source"] = {
        "locator": "[0043]",
        "quote": quote,
        "value_span": {"start": quote.index("0.08 mm"), "end": quote.index("0.08 mm") + len("0.08 mm")},
    }
    row = run("read.value-derivation", spec)
    if "value.quoted-span" in rules_of(row):
        pytest.fail("문자 오프셋 value_span 이 거부되었다 — §2.4 는 이것을 문자 오프셋으로 규정한다")

    byte_based = copy.deepcopy(spec)
    quote_bytes = quote.encode("utf-8")
    start = quote_bytes.index(b"0.08 mm")
    item(byte_based, "M5")["source"]["value_span"] = {"start": start, "end": start + 7}
    row = run("read.value-derivation", byte_based)
    # 바이트 오프셋으로 적힌 value_span 은 범위 밖으로 나가거나(span-bounds) 다른 바이트를
    # 집는다(quoted-span). 둘 중 무엇이든 **거부**되는 것이 요점이다.
    if row.status != "fail" or not {"value.quoted-span", "value.span-bounds"} & set(rules_of(row)):
        pytest.fail(f"바이트 오프셋 value_span 이 거부되지 않았다: {rules_of(row)}")


def test_span_cutting_a_character_boundary_is_rejected() -> None:
    """문자를 쪼개는 바이트 경계가 조용히 통과하면 span 이 위치 지목 힌트 구실조차 못 한다."""
    prefix = "# 한글\n\n"
    source = prefix + SOURCE
    spec = golden_spec()
    spec["patent"]["source_digest"] = digest_of(source)
    item(spec, "M4")["spec_refs"][0]["span"] = {"start": 3, "end": 9}  # '한' 의 중간
    require_fail(run("read.verbatim", spec, source_text=source), "verbatim.span-boundary")


def test_source_digest_mismatch_is_rejected() -> None:
    """다이제스트를 아무도 보지 않으면 원천이 바뀐 런에서 verbatim 계열 전부가 엉뚱한 기준점 위에서 통과한다(불변식 I1)."""
    require_pass(run("read.source-digest", golden_spec()))
    row = CHECK_REGISTRY["read.source-digest"](_fail_source_digest())
    require_fail(row, "source.digest-match")
    # 원천이 한 글자만 달라도 잡힌다.
    altered = SOURCE.replace("0.08 mm", "0.09 mm", 1)
    require_fail(run("read.source-digest", golden_spec(), source_text=altered), "source.digest-match")


def test_source_digest_absent_source_is_vacuous_not_pass() -> None:
    """원천 없이 돌린 검사가 통과로 보이면 '기준점을 확인했다'는 보고가 거짓이 된다."""
    row = run("read.source-digest", golden_spec(), source_text="")
    if row.checked != 0 or row.violations != 0:
        pytest.fail(f"원천 없음인데 checked={row.checked}, violations={row.violations}")
    if row.vacuous != "empty-target" or not row.extras.get("skipped"):
        pytest.fail(f"공허 표기가 없다: vacuous={row.vacuous}, extras={row.extras}")


def test_source_digest_runs_before_the_checks_it_underwrites() -> None:
    """I1 판정이 뒤에 오면 '전부 무효'라는 문언과 보고서의 읽는 순서가 어긋난다."""
    order = list(READ_CHECK_IDS)
    if order[:2] != ["read.schema", "read.source-digest"]:
        pytest.fail(f"검사 순서가 다르다: {order[:3]}")
    if order.index("read.source-digest") > order.index("read.verbatim"):
        pytest.fail("다이제스트 검사가 verbatim 뒤에 있다")


def test_item_ids_must_be_contiguous() -> None:
    """결번이 통과하면 추가 전용 규율이 "번호가 건너뛰어도 통과"로 남고 삭제와 미생성이 구별되지 않는다."""
    require_pass(run("freeze.id-monotonic", golden_spec()))
    gapped = golden_spec()
    gapped["items"] = [entry for entry in gapped["items"] if entry["id"] != "M7"]
    require_fail(run("freeze.id-monotonic", gapped), "lifecycle.id-contiguous")


def test_bibliographic_copy_mismatch_is_rejected() -> None:
    """서지 복사가 `patent` 블록과 달라도 통과하면 결정론 복사가 자유 기입이 된다."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": "M16",
            "kind": "fact",
            "status": "active",
            "superseded_by": None,
            "label_en": "publication year",
            "origin": "bibliographic",
            "value_raw": "1999",
            "value_normalized": "1999",
            "value_type": {"kind": "scalar", "approximate": False, "value": "1999"},
            "unit": None,
            "machine_verifiable": True,
            "bib_source": {"field": "patent.dates.publication"},
        }
    )
    require_fail(run("read.value-derivation", spec), "value.bibliographic")


def test_formula_evaluator_refuses_non_arithmetic_input() -> None:
    """산식 평가가 임의 표현식을 받으면 정답지를 만드는 경로에 코드 실행이 열린다."""
    from reader.lib.derivation import FormulaError, evaluate_formula

    with pytest.raises(FormulaError):
        evaluate_formula("__import__('os').getcwd()", {})
    with pytest.raises(FormulaError):
        evaluate_formula("2 ** 8", {})
    with pytest.raises(FormulaError):
        evaluate_formula("a / b", {"a": __import__("decimal").Decimal(1), "b": __import__("decimal").Decimal(0)})


def test_rounding_modes_are_applied_before_comparison() -> None:
    """반올림이 대조 전에 적용되지 않으면 `rounding` 선언이 장식이 된다."""
    spec = golden_spec()
    derived = item(spec, "M13")
    derived["derivation"]["formula"] = "length_mm / diameter_mm / 7"
    derived["derivation"]["rounding"] = {"mode": "decimal-places", "digits": 2}
    derived["value_raw"] = "21.43"
    derived["value_normalized"] = "21.43"
    derived["value_type"] = {"kind": "scalar", "approximate": False, "value": "21.43"}
    require_pass(run("read.value-derivation", spec))
