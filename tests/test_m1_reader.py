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
from reader.lib.harvest import harvest_numeric_facts  # noqa: E402
from reader.lib.normalize import NormalizeError  # noqa: E402
from reader.lib.rules import DEFAULT_RULES_PATH  # noqa: E402
from reader.lib.source_digest import digest_of  # noqa: E402

RULES = Rules.load()
SCHEMA = load_schema()
with open(os.path.join(REPO, "reader", "READER-VERSION"), encoding="utf-8") as _handle:
    # 골든이 판 번호를 리터럴로 들면 `reader_version` 상향 때마다 골든이 낡는다.
    READER_VERSION = _handle.read().strip()

# ---------------------------------------------------------------------------
# 가공 원천·가공 인스턴스 (SPEC §2.7 의 더미를 이 파일 안에서 재구성한다)
# 실재 특허가 아니며 실재 특허를 인용하지 않는다.
# ---------------------------------------------------------------------------

SOURCE = """# Example Devices — stacked module (fictional example)

Applicant: Example Devices, Inc.
Inventors: Dana Reyes; Kim Anders
Priority: application XX2024-0000111 filed on 11 March 2024 (XX)
Int. Cl.: H01L 23/473
CPC: H01L 23/473

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
GROUND_QUOTE_E2 = "The heat spreader 210 is bonded to the first surface 112 of the substrate 110."
GROUND_QUOTE_E1 = "the first surface 112 of the substrate 110"
GROUND_QUOTE_A1 = "the hydraulic diameter is 0.08 mm, and the drawings do not mark this dimension"
GROUND_QUOTE_A2 = (
    "The folded flow path 214 doubles back within the footprint so that the total flow "
    "path length is 12 mm"
)
SEARCH_NOTE = (
    "FIG-2 전 도면부호(110·112·210·214)와 캡션을 확인했으나 수력직경 치수는 도면에 "
    "표기되지 않음."
)

# ---------------------------------------------------------------------------
# 항목 ID 이름표
#
# ★ 골든의 수치 사실은 **손으로 쓰지 않는다**(재정 P-B). `origin ∈ {quoted, bibliographic}`
#   는 수확기(`reader/lib/harvest.py`)의 소유이므로 골든도 그 산출을 그대로 싣는다 —
#   손으로 다듬으면 `value.harvest-parity` 가 즉시 실패하며, 그 실패는 검사의 결함이 아니라
#   **골든이 규율을 어긴 것**이다. 그래서 ID 는 세 구간으로 나뉜다:
#     M1~M10   레인 소유 골격(구성요소·접지·함의·포지셔닝)
#     M11~M16  수확기 소유(원문 스팬 2 + 서지 4) — 순서는 수확기의 등장 순이다
#     M17~M18  레인 소유 수치(`derived`·`figure-sourced`)
#   아래 이름표는 그 구간의 문서화이며, 실제 배치는 `golden_spec()` 이 계산으로 확인한다.
# ---------------------------------------------------------------------------

M_E1 = "M1"                 # component — CL-1/e1
M_E2 = "M2"                 # component — CL-1/e2
M_A1 = "M3"                 # component — CL-5/a1
M_A2 = "M4"                 # component — CL-7/a1
M_GROUND_E1 = "M5"          # grounding — M1
M_GROUND_E2 = "M6"          # grounding — M2
M_GROUND_A1 = "M7"          # grounding — M3 (도면 미표기 = 접지 예외)
M_GROUND_A2 = "M8"          # grounding — M4
M_IMPLICATION = "M9"
M_POSITIONING = "M10"
M_DIAMETER = "M11"          # 수확 — 원문 스팬 `0.08 mm`
M_LENGTH = "M12"            # 수확 — 원문 스팬 `12 mm`
M_BIB_NUMBER = "M13"        # 수확 — patent.number
M_BIB_PRIORITY = "M14"      # 수확 — patent.dates.priority
M_BIB_FILING = "M15"        # 수확 — patent.dates.filing
M_BIB_PUBLICATION = "M16"   # 수확 — patent.dates.publication
M_DERIVED = "M17"           # 레인 소유 — 산식
M_FIGURE_SOURCED = "M18"    # 레인 소유 — 도면 판독

HARVESTED_IDS = [
    M_DIAMETER,
    M_LENGTH,
    M_BIB_NUMBER,
    M_BIB_PRIORITY,
    M_BIB_FILING,
    M_BIB_PUBLICATION,
]


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


def _base_spec() -> dict:
    """수확 **전**의 골격 — 레인이 소유하는 항목만 든다.

    수확기가 훑는 것은 `grounding.spec_refs[].quote` 이므로, 이 골격이 곧 수확의 입력이다.
    """
    return {
        "schema": "material-spec/v0",
        "reader_version": READER_VERSION,
        "spec_version": 1,
        "status": "frozen",
        "run_id": "example-xx0000000a1-stacked-module",
        "patent": {
            "number": "XX0000000A1",
            "title": "Stacked module with an integrated fluid channel (fictional example)",
            "jurisdiction": "XX",
            "kind_code": "A1",
            "assignee": "Example Devices, Inc.",
            # ★ 목록형 서지(재정 P-2 ⓐ). 각 문자열은 원천의 **바이트 정확 부분문자열**이며
            #   그 대조는 `read.bibliography` 가 한다 — 눈으로 옮겨 적으면 반드시 실패한다.
            "applicants": ["Example Devices, Inc."],
            "inventors": ["Dana Reyes", "Kim Anders"],
            "dates": {
                "priority": "2024-03-11",
                "filing": "2025-03-10",
                "publication": "2026-01-15",
            },
            "priority_claims": [
                {
                    "number": "XX2024-0000111",
                    "date": "2024-03-11",
                    "jurisdiction": "XX",
                }
            ],
            "classifications": {"ipc": ["H01L 23/473"], "cpc": ["H01L 23/473"]},
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
                            "material_id": M_E1,
                            "children": [],
                        },
                        {
                            "id": "CL-1/e2",
                            "text_verbatim": E2_TEXT,
                            "material_id": M_E2,
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
                            "material_id": M_A1,
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
                            "material_id": M_A2,
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
                    "material_id": M_IMPLICATION,
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
                "id": M_E1,
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e1",
                "label_en": "substrate having a first surface",
                "text_verbatim": E1_TEXT,
            },
            {
                "id": M_E2,
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e2",
                "label_en": "heat spreader that defines the fluid channel in its own body",
                "text_verbatim": E2_TEXT,
            },
            {
                "id": M_A1,
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-5/a1",
                "label_en": "hydraulic diameter limitation on the fluid channel",
                "text_verbatim": A1_TEXT,
            },
            {
                "id": M_A2,
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-7/a1",
                "label_en": "flow path length limitation on the fluid channel",
                "text_verbatim": A2_TEXT,
            },
            {
                "id": M_GROUND_E1,
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": M_E1,
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [
                    {
                        "locator": "[0042]",
                        "quote": GROUND_QUOTE_E1,
                        "span": _source_span(GROUND_QUOTE_E1),
                    }
                ],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["110", "112"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": M_GROUND_E2,
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": M_E2,
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [
                    {
                        "locator": "[0042]",
                        "quote": GROUND_QUOTE_E2,
                        "span": _source_span(GROUND_QUOTE_E2),
                    }
                ],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["210", "112"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": M_GROUND_A1,
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": M_A1,
                "anchor_state": {"spec": "found", "figure": "not-depicted"},
                "spec_refs": [{"locator": "[0043]", "quote": GROUND_QUOTE_A1}],
                "figure_refs": [],
                "search_note": SEARCH_NOTE,
            },
            {
                "id": M_GROUND_A2,
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": M_A2,
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [{"locator": "[0044]", "quote": GROUND_QUOTE_A2}],
                "figure_refs": [
                    {"figure": "FIG-2", "numerals": ["214"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": M_IMPLICATION,
                "kind": "implication",
                "status": "active",
                "superseded_by": None,
                "statement_en": (
                    "Forming the channel inside the spreader body points at removing a "
                    "cold plate rather than adding one."
                ),
                "basis": "spec",
                "derived_from": [M_E2, M_GROUND_E2],
                # ★ 중요분은 LLM 의 중요도 판단이 아니라 이 역참조가 도출한다(재정 P-B).
                "numeric_refs": [M_DIAMETER],
                "evidence_quotes": [
                    "the channel is formed within the spreader so that a separate cold plate is not required"
                ],
                "confidence": "inferred",
            },
            {
                "id": M_POSITIONING,
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
                "numeric_refs": [M_LENGTH],
                "quotes": [
                    "Conventional assemblies stack a cold plate on top of the module, which adds one more thermal interface.",
                    "the thermal interface count is reduced by one",
                ],
            },
        ],
        "extensions": {
            # ★ `drop_signal` 은 최상위가 아니라 확장 블록에 산다(재정 P-2 ⓑ) — 사실이 아니라
            #   **편집 판단**이므로 공유 코어에 있을 수 없다. historian 은 이 블록을 쓰지 않는다.
            "docent": {
                "drop_signal": {
                    "stage": "final",
                    "verdict": "go",
                    "reason": "권리 관심이 한 구성에 뚜렷하고, 효과 주장이 명세서 문언으로 존재함.",
                }
            }
        },
        "provenance": {
            "read_runs": ["read-a-0f1c2d3", "read-b-9a8b7c6"],
            "produced_at": "2026-02-01T00:00:00Z",
            "engine_commit": "0000000",
        },
        # 판 0.9.0(재정 T59 ①) — 최상위 필수 배열. 이 골든은 요청이 없는 재료다(빈 배열 = 「없음」).
        "review_requests": [],
    }


def golden_spec() -> dict:
    """전 검사를 통과해야 하는 가공 인스턴스.

    ★ 수치 사실은 **수확기 산출을 그대로** 싣는다(재정 P-B). 손으로 쓴 부분 발췌를 실으면
    `value.harvest-parity` 가 그 자리에서 실패하며 그것이 정상 동작이다 — 골든이 규율의
    바깥에 서면 아래 전 실패 케이스가 '무엇 때문에 실패했는가'를 말할 수 없다.
    """
    spec = _base_spec()
    harvested, _skipped = harvest_numeric_facts(
        spec, rules=RULES, id_start=len(spec["items"]) + 1
    )
    spec["items"].extend(harvested)

    # 레인 소유 수치 2종은 수확 대역 **뒤**에 온다(`origin` 소유권 — 재정 P-B).
    spec["items"].append(
        {
            "id": M_DERIVED,
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
                    {"name": "length_mm", "ref": M_LENGTH},
                    {"name": "diameter_mm", "ref": M_DIAMETER},
                ],
                "rounding": {"mode": "none", "digits": 0},
            },
        }
    )
    spec["items"].append(
        {
            "id": M_FIGURE_SOURCED,
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
        }
    )
    return spec


def new_item_id(spec: dict) -> str:
    """이 명세에 항목 하나를 덧붙일 때 쓸 다음 ID(`lifecycle.id-contiguous` 준수)."""
    return f"M{len(spec['items']) + 1}"


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


def _axis_rule(axis_id: str) -> dict:
    """규칙 파일의 수렴 축 1건. 축이 사라지면 그 사실이 여기서 먼저 드러난다."""
    for axis in RULES.convergence_axes:
        if axis.get("id") == axis_id:
            return axis
    pytest.fail(f"reader-rules#convergence.axes 에 {axis_id} 축이 없다")
    return {}  # pragma: no cover — pytest.fail 이 이미 종료한다


def _axis_status(row, axis_id: str) -> str:
    """판정 행 부속의 축별 status(`pass`·`fail`·`escalate`·`measured`)."""
    for axis in row.extras.get("axes") or []:
        if axis.get("id") == axis_id:
            return str(axis.get("status"))
    pytest.fail(f"{row.check_id} 의 axes 에 {axis_id} 가 없다: {row.extras.get('axes')}")
    return ""  # pragma: no cover


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
    item(spec, M_E1)["kind"] = "widget"
    return context(spec)


def _fail_source_digest() -> CheckContext:
    spec = golden_spec()
    spec["patent"]["source_digest"] = "sha256:" + "0" * 64
    return context(spec)


def _fail_verbatim() -> CheckContext:
    spec = golden_spec()
    item(spec, M_GROUND_E2)["spec_refs"][0]["quote"] = GROUND_QUOTE_E2.replace("112", "122")
    return context(spec)


def _fail_pointer() -> CheckContext:
    spec = golden_spec()
    spec["claims"]["dependents"][0]["additions"][0]["attaches_to"] = "CL-1/e9"
    return context(spec)


def _fail_coverage() -> CheckContext:
    spec = golden_spec()
    spec["items"] = [entry for entry in spec["items"] if entry["id"] != M_GROUND_E2]
    return context(spec)


def _fail_dependency_parse() -> CheckContext:
    spec = golden_spec()
    spec["claims"]["dependents"][1]["depends_on"] = ["CL-1"]
    spec["claims"]["dependents"][1]["dependency_type"] = "single"
    return context(spec)


def _fail_value_derivation() -> CheckContext:
    spec = golden_spec()
    item(spec, M_DIAMETER)["value_raw"] = "999 mm"
    return context(spec)


def _fail_bibliography() -> CheckContext:
    """서지 확장 필드를 원천에 없는 이름으로 바꾼 판(재정 P-2 ⓐ)."""
    spec = golden_spec()
    spec["patent"]["inventors"] = ["Ivan Nonexistent"]
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
    """2회차가 다중 종속의 논리 형태를 다르게 읽은 판.

    ★ 축을 고른 근거 = 재정 P-3. 판정 행을 `fail` 로 만드는 것은 **exact-match 축**뿐이며
    `dependent-set` 이 그 셋 중 하나다(임계 1.0). 구 표본은 element 문언을 갈랐는데 그 축은
    이제 상신 트리거이므로 행을 실패시키지 않는다 — 등재부의 실패 케이스로 쓸 수 없다.
    """
    peer = golden_spec()
    peer["claims"]["dependents"][1]["depends_on"] = ["CL-1"]
    peer["claims"]["dependents"][1]["dependency_type"] = "single"
    return context(golden_spec(), peer_spec=peer)


def _diverging_peer() -> dict:
    """element 입도가 갈린 2회차(해석 여지 축의 표본 — 재정 P-3 의 상신 트리거)."""
    peer = golden_spec()
    elements = peer["claims"]["independent"][0]["elements"]
    elements[1] = {
        "id": "CL-1/e2",
        "text_verbatim": "a heat spreader thermally coupled to the first surface",
        "material_id": M_E2,
        "children": [],
    }
    elements.append(
        {
            "id": "CL-1/e3",
            "text_verbatim": "the heat spreader defining a fluid channel.",
            "material_id": M_A2,
            "children": [],
        }
    )
    return peer


def _fail_id_monotonic() -> CheckContext:
    prior = golden_spec()
    prior["items"].append(
        {
            "id": new_item_id(prior),
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
    item(current, M_E1)["label_en"] = "quietly rewritten label under the same id"
    return context(current, prior_spec=prior)


FAILING_CASE_BUILDERS = {
    "read.schema": _fail_schema,
    "read.source-digest": _fail_source_digest,
    "read.verbatim": _fail_verbatim,
    "read.pointer-resolve": _fail_pointer,
    "read.coverage": _fail_coverage,
    "read.dependency-parse": _fail_dependency_parse,
    "read.value-derivation": _fail_value_derivation,
    "read.bibliography": _fail_bibliography,
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


def test_dependent_set_axis_requires_exact_match() -> None:
    """종속항 서명축이 0.95 로 남으면 P-3 의 1.0 승격이 미집행 — 다중 종속의 논리 형태가 조용히 갈린다."""
    axis = _axis_rule("dependent-set")
    if axis.get("policy") != "exact-match" or float(axis.get("threshold")) != 1.0:
        pytest.fail(f"dependent-set 축이 재정 P-3 과 다르다: {axis!r}")
    row = CHECK_REGISTRY["read.convergence"](_fail_convergence())
    require_fail(row, "dependent-set")
    if _axis_status(row, "dependent-set") != "fail":
        pytest.fail(f"exact-match 축이 fail 로 판정되지 않았다: {row.extras['axes']}")

    # 대조군 — 서명이 같으면 통과한다(전부 거부하는 검사와 구별되어야 한다).
    clean = run("read.convergence", golden_spec(), peer_spec=golden_spec())
    require_pass(clean)
    if _axis_status(clean, "dependent-set") != "pass":
        pytest.fail(f"무변조에서 dependent-set 이 통과하지 않았다: {clean.extras['axes']}")


def test_interpretive_axis_below_threshold_escalates_not_fails() -> None:
    """해석 축 미달이 fail 이면 "실패가 아니라 상신"이 문서에만 남는다(재정 P-3)."""
    for axis_id in ("element-set", "tree-edges"):
        axis = _axis_rule(axis_id)
        if axis.get("policy") != "escalation-trigger":
            pytest.fail(f"{axis_id} 축의 정책이 상신 트리거가 아니다: {axis.get('policy')!r}")

    row = run("read.convergence", golden_spec(), peer_spec=_diverging_peer())
    # ① 판정 행은 실패가 아니다 — 결함 목록에 그 축이 오르지 않는다.
    require_pass(row)
    if "element-set" in rules_of(row):
        pytest.fail(f"상신 축이 결함으로 등재되었다: {rules_of(row)}")
    # ② 그러나 침묵하지도 않는다 — 상신 목록과 status 에 남는다.
    escalated = {entry["axis"] for entry in row.extras["escalations"]}
    if "element-set" not in escalated:
        pytest.fail(f"상신 목록에 element-set 이 없다: {row.extras['escalations']}")
    if _axis_status(row, "element-set") != "escalate":
        pytest.fail(f"status 어휘가 escalate 가 아니다: {row.extras['axes']}")
    # ③ 상신 서식 = 독해 프로파일(갈린 항목의 실물).
    profile = row.extras["profile"]
    diverged = {entry["axis"] for entry in profile["divergences"]}
    if "element-set" not in diverged:
        pytest.fail(f"프로파일에 갈린 항목이 실리지 않았다: {profile['divergences']}")

    # 대조군 — 갈리지 않으면 상신도 없다.
    clean = run("read.convergence", golden_spec(), peer_spec=golden_spec())
    if clean.extras["escalations"]:
        pytest.fail(f"무변조인데 상신이 생겼다: {clean.extras['escalations']}")


def test_addition_attachment_axis_is_measure_only() -> None:
    """측정 전용 축이 판정하면 부착 관례 입법 전에 법이 생긴다(재정 P-3)."""
    axis = _axis_rule("addition-attachment")
    if axis.get("policy") != "measure-only" or axis.get("threshold") is not None:
        pytest.fail(f"addition-attachment 축이 재정 P-3 과 다르다: {axis!r}")

    peer = golden_spec()
    # 두 부가 한정의 부착 대상을 통째로 옮긴다 — 부착 집합이 완전히 갈린다.
    for dependent in peer["claims"]["dependents"]:
        dependent["additions"][0]["attaches_to"] = "CL-1/e1"
    row = run("read.convergence", golden_spec(), peer_spec=peer)

    require_pass(row)  # 판정하지 않는 축이므로 행을 실패시키지 않는다
    if "addition-attachment" in {entry["axis"] for entry in row.extras["escalations"]}:
        pytest.fail("측정 전용 축이 상신 목록에 올랐다 — 판정 제외가 아니라 상신이 되었다")
    if _axis_status(row, "addition-attachment") != "measured":
        pytest.fail(f"status 어휘가 measured 가 아니다: {row.extras['axes']}")
    # 판정은 하지 않아도 **값은 잰다** — 그 값이 부착 관례 입법의 근거 자료다.
    score = row.extras["jaccard"].get("addition-attachment")
    if score is None or score >= 1.0:
        pytest.fail(f"측정 전용 축의 값이 기록되지 않았다: {row.extras['jaccard']}")


def test_material_id_append_only_rejects_renumber() -> None:
    """개정본이 포지셔닝 항목을 다른 내용으로 재사용해도 통과하면 ID 규율 붕괴."""
    prior = golden_spec()
    current = golden_spec()
    reused = item(current, M_POSITIONING)
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
    item(spec, M_DIAMETER)["source"]["value_span"] = {"start": 0, "end": 7}
    require_fail(run("read.value-derivation", spec), "value.quoted-span")


def test_derived_value_recomputation_mismatch_is_rejected() -> None:
    """산식 재계산 불일치가 통과하면 파생 수치가 사실상 자유 기입이 됨."""
    spec = golden_spec()
    derived = item(spec, M_DERIVED)
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
    if ids != [M_FIGURE_SOURCED]:
        pytest.fail(f"manual_verification_required 기대 [{M_FIGURE_SOURCED!r}], 실제 {ids}")
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
    item(spec, M_E1)["label_en"] = "제1 표면을 갖는 기판"
    require_fail(run("read.schema", spec), "schema.validate")
    require_fail(run("read.value-derivation", spec), "value.en-only")


def test_origin_mixed_attachment_is_rejected() -> None:
    """`quoted` 항목이 `derivation` 을 함께 갖는 것이 통과하면 provenance 가 두 갈래로 갈려 어느 쪽이 근거인지 판정 불가."""
    spec = golden_spec()
    item(spec, M_DIAMETER)["derivation"] = {
        "formula": "a * 2",
        "inputs": [{"name": "a", "ref": M_LENGTH}],
        "rounding": {"mode": "none", "digits": 0},
    }
    require_fail(run("read.schema", spec), "schema.validate")


def test_derived_fact_of_derived_fact_is_rejected() -> None:
    """파생의 파생이 통과하면 원문 스팬까지의 거리가 무한해지고 재계산 대조가 사슬 어딘가에서 끊김(재정 N9 의 깊이 1)."""
    spec = golden_spec()
    spec["items"].append(
        {
            "id": new_item_id(spec),
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
                "inputs": [{"name": "ratio", "ref": M_DERIVED}],
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
    """element 집합만 보면 같은 문자열이 서로 다른 계층으로 조립되어도 수렴한 것으로 판정된다(재감수 M-07 구조 축).

    ★ 판정 층이 바뀌었다(재정 P-3). 트리 조직은 해석 여지가 있는 축이므로 미달이 `fail` 이
    아니라 **상신**이다 — 그래서 이 테스트가 보는 것은 "실패했는가"가 아니라 **"트리 축만
    잡혔는가"** 다. 구조 축의 독립성이라는 M-07 의 요지는 그대로이며, 그것이 사라지면 같은
    문자열의 다른 계층이 아무 데서도 드러나지 않는다.
    """
    peer = golden_spec()
    elements = peer["claims"]["independent"][0]["elements"]
    nested = elements.pop(1)
    nested["id"] = "CL-1/e1/e1"
    elements[0]["children"] = [nested]
    for dependent in peer["claims"]["dependents"]:
        dependent["additions"][0]["attaches_to"] = "CL-1/e1/e1"
    row = run("read.convergence", golden_spec(), peer_spec=peer)
    axes = {entry["axis"] for entry in row.extras["escalations"]}
    if "tree-edges" not in axes:
        pytest.fail(f"트리 간선 축이 상신되지 않았다: {row.extras['escalations']}")
    if "element-set" in axes:
        pytest.fail("element 집합 축이 함께 상신됐다 — 구조 축의 독립성을 시험하지 못한다")
    if _axis_status(row, "element-set") != "pass":
        pytest.fail(f"element 집합은 갈리지 않았는데 status 가 pass 가 아니다: {row.extras['axes']}")


def test_payload_change_under_same_id_is_rejected() -> None:
    """개정본이 기존 `active` 항목 내용을 조용히 바꿔도 통과하면 고정되는 것은 ID 뿐이고 의미가 아니다."""
    row = CHECK_REGISTRY["freeze.payload-immutable"](_fail_payload_immutable())
    require_fail(row, "lifecycle.payload-frozen")
    # 상태 변경(active → retracted)은 payload 대상이 아니므로 통과해야 한다.
    prior = golden_spec()
    current = golden_spec()
    item(current, M_DIAMETER)["status"] = "retracted"
    require_pass(CHECK_REGISTRY["freeze.payload-immutable"](context(current, prior_spec=prior)))


def test_supersession_chain_terminal_must_be_active() -> None:
    """2차 승계에서 종단을 보지 않으면 인용의 수정 지시가 죽은 항목을 지목한다."""
    spec = golden_spec()
    first = int(new_item_id(spec)[1:])
    head, middle, terminal = (f"M{first + step}" for step in range(3))
    chain = [
        (head, "superseded", middle),
        (middle, "superseded", terminal),
        (terminal, "active", None),
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
    item(dead, terminal)["status"] = "retracted"
    require_fail(
        CHECK_REGISTRY["freeze.payload-immutable"](context(dead)),
        "supersession.terminal-active",
    )


def test_lifecycle_transition_is_one_way() -> None:
    """종단 상태에서 되돌아오는 전이가 통과하면 철회·교체 기록이 뒤집힐 수 있다."""
    prior = golden_spec()
    item(prior, M_DIAMETER)["status"] = "retracted"
    current = golden_spec()  # 현행에서는 active 다
    require_fail(
        CHECK_REGISTRY["freeze.payload-immutable"](context(current, prior_spec=prior)),
        "lifecycle.one-way",
    )


def test_value_type_mismatch_with_value_raw_is_rejected() -> None:
    """범위를 스칼라로 뭉개 담아도 통과하면 게이트가 그 값에서 문자열 일치 여부밖에 판정하지 못한다."""
    spec = golden_spec()
    fact = item(spec, M_DIAMETER)
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
    item(spec, M_DIAMETER)["value_raw"] = "999 mm"
    require_pass(run("read.verbatim", spec))


def test_self_referencing_derivation_input_is_rejected() -> None:
    """`derivation.inputs[].ref` 자기참조가 통과하면 원문 스팬까지의 거리가 정의되지 않는다(재감수 B-02 validator-scope)."""
    spec = golden_spec()
    item(spec, M_DERIVED)["derivation"]["inputs"][0] = {"name": "length_mm", "ref": M_DERIVED}
    require_fail(run("read.pointer-resolve", spec), "pointer.no-self-reference")


def test_reference_graph_cycle_is_rejected() -> None:
    """2항 순환이 통과하면 참조 그래프에 종단이 없어 해소가 무한 루프가 된다."""
    spec = golden_spec()
    cycle_id = new_item_id(spec)
    item(spec, M_IMPLICATION)["derived_from"] = [cycle_id]
    spec["items"].append(
        {
            "id": cycle_id,
            "kind": "implication",
            "status": "active",
            "superseded_by": None,
            "statement_en": "An implication that points back at the first one.",
            "basis": "spec",
            "derived_from": [M_IMPLICATION],
            "numeric_refs": [],
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
    payload = to_convergence_payload(rows, spec, canonical_read_run="read-a")
    if payload["schema"] != "convergence/v0" or payload["run_id"] != spec["run_id"]:
        pytest.fail(f"산출 머리가 다르다: {payload['schema']} / {payload['run_id']}")
    if len(payload["checks"]) != len(READ_CHECK_IDS):
        pytest.fail(f"checks 행 수가 다르다: {len(payload['checks'])}")
    classification = payload["fact_classification"]
    # 서지 복사는 원문 스팬과 같은 갈래로 계수하되 정체는 `bibliographic_ids` 로 드러난다(§1.4).
    if classification["quoted_span"]["material_ids"] != [
        M_DIAMETER, M_LENGTH, M_BIB_NUMBER, M_BIB_PRIORITY, M_BIB_FILING, M_BIB_PUBLICATION
    ]:
        pytest.fail(f"수치 3분류의 원문 스팬 갈래가 다르다: {classification['quoted_span']}")
    if [entry["material_id"] for entry in classification["derived"]] != [M_DERIVED]:
        pytest.fail(f"파생 갈래가 다르다: {classification['derived']}")
    if [entry["material_id"] for entry in classification["figure_sourced"]] != [M_FIGURE_SOURCED]:
        pytest.fail(f"도면 유래 갈래가 다르다: {classification['figure_sourced']}")
    if classification["bibliographic_ids"] != [
        M_BIB_NUMBER, M_BIB_PRIORITY, M_BIB_FILING, M_BIB_PUBLICATION
    ]:
        pytest.fail(f"서지 갈래가 다르다: {classification['bibliographic_ids']}")
    if [entry["material_id"] for entry in payload["manual_verification_required"]] != [M_FIGURE_SOURCED]:
        pytest.fail("도면 유래 수치가 사람 검증 목록에 오르지 않았다")
    exceptions = payload["grounding_exceptions"]
    if [entry["material_id"] for entry in exceptions] != [M_GROUND_A1]:
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
        # 폴백 경로는 재현하지 않는다 — 폴백은 접미 표기를 내어 enum 과 정합하지 않음(재정 T32 §5 ③ · 합본 감사 RD-5)
        payload = to_convergence_payload(rows, spec, canonical_read_run="read-a")
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
    shared["claims"]["dependents"][1]["additions"][0]["material_id"] = M_A1
    require_fail(run("read.coverage", shared), "coverage.material-id-unique")

    reversed_spec = golden_spec()
    item(reversed_spec, M_A1)["claim_ref"] = "CL-1/e1"
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
    outside["claims"]["dependents"][0]["text_verbatim"] = GROUND_QUOTE_E2
    require_fail(run("read.verbatim", outside), "verbatim.claim-section")


def test_orphan_component_item_is_rejected() -> None:
    """커버리지는 청구항 쪽에서 세므로, 청구항이 통째로 빠지면 셀 대상도 함께 빠져 통과한다 — 남는 흔적이 고아 성분 항목이다."""
    spec = golden_spec()
    orphan_id = new_item_id(spec)
    spec["items"].append(
        {
            "id": orphan_id,
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
    item(retired, orphan_id)["status"] = "retracted"
    require_pass(run("read.coverage", retired))


def test_standalone_retracted_item_is_not_a_chain_violation() -> None:
    """단독 철회 항목을 사슬 위반으로 읽으면 정상 개정본이 통과하지 못한다(retracted = 대체물 없음)."""
    spec = golden_spec()
    item(spec, M_DIAMETER)["status"] = "retracted"  # superseded_by 는 null 그대로
    require_pass(CHECK_REGISTRY["freeze.payload-immutable"](context(spec)))
    definition = RULES.item_lifecycle["supersession_chain"].get("chain_definition")
    if not definition:
        pytest.fail("규칙 파일에 chain_definition 이 없다 — 사슬의 출발점 정의가 문언에 없다")


def test_reference_cycle_edges_cover_all_five_link_kinds() -> None:
    """간선 5종 중 하나라도 빠지면 그 링크로 만든 순환은 영원히 보이지 않는다.

    ★ 5번째가 `numeric_refs[]` 다(재정 P-B). 역참조가 그래프의 간선이 아니면 함의 A 가
    수치 B 를, B 가 다시 A 를 가리키는 순환이 해소 검사를 통과한다.
    """
    from reader.lib.pointers import GRAPH_FIELDS

    expected = {
        "derivation.inputs[].ref",
        "derived_from[]",
        "superseded_by",
        "grounding.component",
        "numeric_refs[]",
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
    fact = item(spec, M_BIB_PRIORITY)
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
    number = item(spec, M_BIB_NUMBER)
    if number["origin"] != "bibliographic" or number["bib_source"]["field"] != "patent.number":
        pytest.fail(f"수확본의 서지 식별자가 기대 형태가 아니다: {number}")
    require_pass(run("read.value-derivation", spec))

    wrong = copy.deepcopy(spec)
    item(wrong, M_BIB_NUMBER)["value_type"] = {"kind": "scalar", "approximate": False, "value": "0"}
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


def test_set_accepts_the_conjunction_before_the_last_member() -> None:
    """청구항의 실제 열거 어형을 담지 못하면, 원문에 실재하는 값이 정답지에서 조용히 빠진다.

    ★ 2026-08-18 실특허 스모크 적발. 청구항 어형은 `2, 3, 4 and 5` 와 `2, 3, 4, or 5` 인데
    구 패턴은 **둘 다 파싱 실패**였다. 독해 레인은 "수치를 지어내지 마라"와 "수치 사실을
    등재하라" 사이에서 후자를 포기했고(3원소로 잘라 담으면 4원소 집합의 왜곡이므로 옳은
    판단이었다), 그 결과 원문의 값이 숫자 전수 대조의 정답지에서 빠졌다.

    계약의 구멍이 **실패가 아니라 산출물의 축소**로 새는 자리이며, 빠진 사실을 결함으로
    보는 검사는 없다 — 그래서 문법 쪽에서 막아야 한다.
    """
    for raw in ("2, 3, 4 and 5", "2, 3, 4, or 5"):
        parsed = parse_value(raw, None, RULES)
        if parsed["kind"] != "set" or parsed["members"] != ["2", "3", "4", "5"]:
            pytest.fail(f"{raw!r} 의 집합 파싱 결과가 다르다: {parsed}")
        if render_value(parsed) != "2;3;4;5":
            pytest.fail(f"{raw!r} 의 렌더가 다르다: {render_value(parsed)}")
    # 연결어를 열었다고 천단위 구분자까지 열려서는 안 된다.
    if parse_value("1,200", None, RULES)["kind"] != "scalar":
        pytest.fail("천단위 구분자가 집합 원소 구분자로 새어 들어갔다")


def test_convergence_refuses_to_invent_a_missing_threshold() -> None:
    """임계가 없을 때 코드가 기본값을 지어내면, 계약 어디에도 없는 수로 판정하게 된다.

    ★ M1 재감수 B-04 적발. 구 구현은 `threshold` 가 없는 축에 **조용히 0.95** 를 적용하면서
    판정 상세에는 `threshold: null` 로 보고했다 — 지어낸 법으로 판정하고 그 사실을 보고서가
    감췄다. D7 이 금지하는 자기 입법이며, 임계는 규칙 파일이 정하는 것이지 코드가 고르는
    것이 아니다. 없으면 판정하지 말고 결함으로 낸다.
    """
    import tempfile

    import yaml

    raw = yaml.safe_load(open(DEFAULT_RULES_PATH, encoding="utf-8"))
    for axis in raw["convergence"]["axes"]:
        axis.pop("threshold", None)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as handle:
        yaml.safe_dump(raw, handle, allow_unicode=True)
        stripped = handle.name
    try:
        context_without_thresholds = CheckContext(
            spec=golden_spec(),
            source_text=SOURCE,
            rules=Rules.load(stripped),
            schema=SCHEMA,
            peer_spec=golden_spec(),
        )
        row = CHECK_REGISTRY["read.convergence"](context_without_thresholds)
        if row.status != "fail":
            pytest.fail("임계가 없는데도 판정이 통과했다 — 코드가 기본값을 지어냈다")
        if "convergence.threshold-missing" not in rules_of(row):
            pytest.fail(f"임계 부재를 다른 결함으로 보고했다: {rules_of(row)}")
    finally:
        os.unlink(stripped)


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
    date_id = new_item_id(spec)
    spec["items"].append(
        {
            "id": date_id,
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
    item(spec, M_DERIVED)["derivation"]["inputs"][0] = {"name": "length_mm", "ref": date_id}
    require_fail(run("read.value-derivation", spec), "value.input-not-arithmetic")


def test_spec_ref_span_is_byte_offset() -> None:
    """`span` 을 문자 오프셋으로 읽으면 ASCII 원천에서만 우연히 맞고, 한글 한 줄이 섞이는 순간 전 인용이 어긋난다."""
    # 앞에 멀티바이트 문자가 있어 바이트 오프셋 ≠ 문자 오프셋인 원천.
    prefix = "# 한글 주석 — 이 줄이 바이트와 문자를 갈라놓는다\n\n"
    source = prefix + SOURCE
    spec = golden_spec()
    spec["patent"]["source_digest"] = digest_of(source)
    quote = GROUND_QUOTE_E2
    byte_start = source.encode("utf-8").index(quote.encode("utf-8"))
    char_start = source.index(quote)
    if byte_start == char_start:
        pytest.fail("표본 원천이 바이트≠문자를 만들지 못했다 — 이 테스트가 공허하다")

    item(spec, M_GROUND_E2)["spec_refs"][0]["span"] = {
        "start": byte_start,
        "end": byte_start + len(quote.encode("utf-8")),
    }
    item(spec, M_GROUND_E1)["spec_refs"][0]["span"] = None
    item(spec, M_GROUND_E1)["spec_refs"][0].pop("span")
    require_pass(run("read.verbatim", spec, source_text=source))

    wrong = copy.deepcopy(spec)
    item(wrong, M_GROUND_E2)["spec_refs"][0]["span"] = {
        "start": char_start,
        "end": char_start + len(quote),
    }
    require_fail(run("read.verbatim", wrong, source_text=source), "verbatim.span")


def test_value_span_is_character_offset() -> None:
    """`value_span` 을 바이트로 읽으면 인용문에 한글·기호가 섞인 순간 정상 수치가 날조로 판정된다."""
    spec = golden_spec()
    fact = item(spec, M_DIAMETER)
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
    item(byte_based, M_DIAMETER)["source"]["value_span"] = {"start": start, "end": start + 7}
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
    item(spec, M_GROUND_E2)["spec_refs"][0]["span"] = {"start": 3, "end": 9}  # '한' 의 중간
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
    gapped["items"] = [entry for entry in gapped["items"] if entry["id"] != M_GROUND_A1]
    require_fail(run("freeze.id-monotonic", gapped), "lifecycle.id-contiguous")


def test_bibliographic_copy_mismatch_is_rejected() -> None:
    """서지 복사가 `patent` 블록과 달라도 통과하면 결정론 복사가 자유 기입이 된다."""
    spec = golden_spec()
    # 수확본의 서지 사실을 `patent` 블록과 어긋나게 고쳐 쓴다 — 필드는 그대로 두고 값만 바꾼다.
    forged = item(spec, M_BIB_PUBLICATION)
    forged["value_raw"] = "1999-01-01"
    forged["value_normalized"] = "1999-01-01"
    forged["value_type"] = {"kind": "date", "approximate": False, "value": "1999-01-01"}
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
    derived = item(spec, M_DERIVED)
    derived["derivation"]["formula"] = "length_mm / diameter_mm / 7"
    derived["derivation"]["rounding"] = {"mode": "decimal-places", "digits": 2}
    derived["value_raw"] = "21.43"
    derived["value_normalized"] = "21.43"
    derived["value_type"] = {"kind": "scalar", "approximate": False, "value": "21.43"}
    require_pass(run("read.value-derivation", spec))


# ---------------------------------------------------------------------------
# 재정 반증 (2026-08-18 P 계열)
#
# 각 테스트는 변조본을 **실제로 만들고** 검사가 그것을 잡는지 본다. 변조본이 실패하는 것만
# 보이면 과잉 제약과 구별되지 않으므로, 같은 테스트 안에 **무변조 대조군**을 함께 둔다.
# ---------------------------------------------------------------------------

# 구조 표지가 있는 종속항 전문(Markush). 표지 목록의 정본 =
# `reader-rules.yaml#dependency_citation.unclassified.structure_markers`.
MARKUSH_CLAIM = (
    "The stacked module of claim 1, wherein the heat spreader is formed of a material "
    "selected from the group consisting of copper, aluminum, and a copper alloy."
)


def _unclassified_spec(text: str, *, depends_on=("CL-1", "CL-5")) -> dict:
    """CL-7 을 `unclassified` 로 선언한 판. 전문과 `depends_on` 을 시험이 정한다."""
    spec = golden_spec()
    dependent = spec["claims"]["dependents"][1]
    dependent["dependency_type"] = "unclassified"
    dependent["text_verbatim"] = text
    dependent["depends_on"] = list(depends_on)
    return spec


def test_unclassified_dependent_is_excluded_from_parse_verdict() -> None:
    """미분류 표지가 판정 대상에 남으면 P-1 이 이름뿐 — 규칙의 공백이 실제 결함과 같은 모양으로 계상된다."""
    # 대조군 ① 무변조 — 두 종속항이 모두 판정 대상이고 미분류 목록은 비어 있다.
    clean = run("read.dependency-parse", golden_spec())
    require_pass(clean)
    if clean.checked != 2 or clean.extras["unclassified"]:
        pytest.fail(f"무변조 기대 checked=2 · 미분류 없음, 실제 {clean.checked} / {clean.extras}")

    # 대조군 ② 같은 전문·같은 `depends_on` 인데 표지가 아니면 **실패한다**.
    #   (전문은 claim 1 만 인용하는데 depends_on 은 두 건 — 판정 대상이면 반드시 걸린다.)
    judged = _unclassified_spec(MARKUSH_CLAIM)
    judged["claims"]["dependents"][1]["dependency_type"] = "single"
    require_fail(run("read.dependency-parse", judged), "parse.set-equals")

    # 본체 — 표지를 붙이면 그 종속항은 판정에서 빠지고, 그 사실이 목록으로 드러난다.
    row = run("read.dependency-parse", _unclassified_spec(MARKUSH_CLAIM))
    require_pass(row)
    if row.checked != 1:
        pytest.fail(f"미분류가 checked 에서 빠지지 않았다: checked={row.checked}")
    if row.extras["unclassified"] != ["CL-7"]:
        pytest.fail(f"미분류 목록이 비었거나 다르다: {row.extras['unclassified']}")


def test_unclassified_without_structure_marker_is_rejected() -> None:
    # ★ 개명(2026-08-19). 구 이름 `test_unclassified_declared_on_parseable_claim_is_rejected`
    #   의 `on_parseable_claim` 은 폐기된 판정 기준(인용 어형의 파싱 가능성)의 어휘였고,
    #   본문 ⓐ가 검증하는 것과 **정반대**였다 — ⓐ는 파싱이 잘 되는 Markush 종속항의
    #   `unclassified` 선언이 **통과해야 한다**고 못 박는다. 이름이 본문과 모순하면
    #   다음 사람이 이름을 믿고 규칙을 되돌린다. 구 이름을 인용한 자리 =
    #   `docs/decisions/D-20260818-04-m1-close.md` §1 — 그 문서는 기록이므로 고치지 않고,
    #   대응은 `D-20260819-01` 이 든다.
    """미분류가 회피 통로가 되면 침묵 통과가 부활한다 — 판정 기준은 본문의 **구조 표지 유무**다(재정 P-1)."""
    # ⓐ 구조 표지가 있는 청구항의 선언은 **통과**한다.
    #    (재정이 명한 사용을 벌하면 그 규칙은 재정을 뒤집는 것이다.)
    allowed = run("read.dependency-parse", _unclassified_spec(MARKUSH_CLAIM))
    if "parse.unclassified-not-an-escape" in rules_of(allowed):
        pytest.fail(f"구조 표지가 있는 선언이 거부됐다: {rules_of(allowed)}")

    # ⓑ 표지가 하나도 없는 청구항의 선언은 **실패**한다.
    plain = _unclassified_spec(CLAIM_7, depends_on=("CL-1", "CL-5"))
    require_fail(run("read.dependency-parse", plain), "parse.unclassified-not-an-escape")

    # 두 방향을 다 보지 않으면 가드가 절반만 증명된다 — 표본이 실제로 갈리는지 확인한다.
    if not RULES.structure_markers_in(MARKUSH_CLAIM):
        pytest.fail("표지 표본에서 구조 표지를 찾지 못했다 — ⓐ 가 공허하다")
    if RULES.structure_markers_in(CLAIM_7):
        pytest.fail("무표지 표본에 구조 표지가 있다 — ⓑ 가 공허하다")


def test_bibliography_rejects_fabricated_inventor() -> None:
    """서지 확장이 원천 대조 없이 통과하면 "결정론 복사"가 자유 기입이 된다(재정 P-2 ⓐ)."""
    require_pass(run("read.bibliography", golden_spec()))  # 대조군 — 정직한 복사는 통과한다

    spec = golden_spec()
    spec["patent"]["inventors"] = ["Dana Reyes", "Ivan Nonexistent"]
    row = run("read.bibliography", spec)
    require_fail(row, "bib.inventors-in-source")
    if "patent.inventors[1]" not in {finding.locus for finding in row.findings}:
        pytest.fail(f"어느 발명자가 날조인지 좌표가 없다: {[f.locus for f in row.findings]}")

    # 한 글자만 달라도 잡힌다 — 눈으로 옮겨 적는 경로를 막는 것이 이 검사의 목적이다.
    typo = golden_spec()
    typo["patent"]["applicants"] = ["Example Devices Inc."]  # 원천은 `Devices, Inc.`
    require_fail(run("read.bibliography", typo), "bib.applicants-in-source")


def test_bibliography_rejects_wrong_earliest_priority() -> None:
    """최우선일이 우선권 목록과 어긋나도 통과하면 C18 요건이 문서로만 존재한다(재정 P-2 ⓐ)."""
    spec = golden_spec()
    spec["patent"]["priority_claims"].append(
        # 같은 번호의 더 이른 주장 — 번호는 원천에 실재하므로 부분문자열 대조는 통과한다.
        #
        # ★ 날짜를 2024년 안에서 고른다(2026-08-19 정정). 구 픽스처는 `2023-11-02` 를 썼는데
        #   골든 원천은 `Priority: application XX2024-0000111 filed on 11 March 2024 (XX)` 라
        #   적으므로 **2023 은 원천 어디에도 없다** — 즉 구 대조군은 그 자체가 날조된 우선권
        #   날짜였고, 신설 규칙 `bib.priority-year-in-source`(재정 P-2 ⓐ 부분 판정의 처분)가
        #   정확히 그것을 잡는다. 이 시험의 의도(최우선일 등식의 반증)는 연도를 바꾸어도
        #   그대로 살아 있으므로 픽스처를 고친다. 규칙을 느슨하게 하는 쪽이 아니다.
        {"number": "XX2024-0000111", "date": "2024-01-05", "jurisdiction": "XX"}
    )
    row = run("read.bibliography", spec)
    require_fail(row, "bib.earliest-priority")

    # 대조군 — 최우선일을 목록의 최소 날짜로 맞추면 통과한다(과잉 제약 배제).
    fixed = copy.deepcopy(spec)
    fixed["patent"]["dates"]["priority"] = "2024-01-05"
    require_pass(run("read.bibliography", fixed))


def test_harvest_parity_detects_planted_number() -> None:
    """심은 수치가 통과하면 전수 수확이 공허해진다 — 정답지가 다시 자유 기입이 된다(재정 P-B)."""
    clean = run("read.value-derivation", golden_spec())
    require_pass(clean)  # 대조군 — 수확기 산출 그대로면 통과한다

    spec = golden_spec()
    quote = "a hydraulic diameter of 0.08 mm"
    spec["items"].append(
        {
            # 실재하는 인용문 옆에 수확기가 낸 적 없는 좌표로 값을 하나 심는다.
            "id": new_item_id(spec),
            "kind": "fact",
            "status": "active",
            "superseded_by": None,
            "label_en": "planted hydraulic diameter",
            "origin": "quoted",
            "value_raw": "0.08 mm",
            "value_normalized": "0.08",
            "value_type": {"kind": "scalar", "approximate": False, "value": "0.08"},
            "unit": "mm",
            "machine_verifiable": True,
            "source": {
                "locator": "claim 5",
                "quote": quote,
                "value_span": _value_span(quote, "0.08 mm"),
            },
        }
    )
    row = run("read.value-derivation", spec)
    require_fail(row, "value.harvest-parity")
    if not [f for f in row.findings if f.rule == "value.harvest-parity" and "[추가]" in f.message]:
        pytest.fail(f"심은 값이 '추가'로 분류되지 않았다: {[f.message[:60] for f in row.findings]}")

    # 좌표는 그대로 두고 값만 바꾼 판 = **변조**. 갈래가 갈려야 국소 수정 지시가 선다(D8).
    forged = golden_spec()
    item(forged, M_DIAMETER)["value_raw"] = "0.09 mm"
    forged_row = run("read.value-derivation", forged)
    require_fail(forged_row, "value.harvest-parity")
    if not [
        f for f in forged_row.findings
        if f.rule == "value.harvest-parity" and "[변조]" in f.message
    ]:
        pytest.fail(f"변조가 '변조'로 분류되지 않았다: {[f.message[:60] for f in forged_row.findings]}")


def test_harvest_parity_detects_dropped_number() -> None:
    """수확 누락이 통과하면 "전수"가 이름뿐이 된다 — 빠진 사실은 어느 검사도 결함으로 보지 않는다(재정 P-B)."""
    spec = golden_spec()
    # 수확된 값 하나를 통째로 들어낸다. 그 값을 참조하던 자리도 함께 정리해, 남는 결함이
    # **누락 하나**가 되도록 한다(다른 규칙에 업혀 통과하는 것을 막는다).
    spec["items"] = [entry for entry in spec["items"] if entry["id"] not in (M_LENGTH, M_DERIVED)]
    item(spec, M_POSITIONING)["numeric_refs"] = []
    row = run("read.value-derivation", spec)
    require_fail(row, "value.harvest-parity")
    dropped = [
        finding for finding in row.findings
        if finding.rule == "value.harvest-parity" and "[누락]" in finding.message
    ]
    if len(dropped) != 1:
        pytest.fail(f"누락 1건 기대, 실제 {[f.message[:80] for f in row.findings]}")
    if "12 mm" not in dropped[0].expected:
        pytest.fail(f"무엇이 빠졌는지 기대값에 실리지 않았다: {dropped[0].expected!r}")

    # 대조군 — 같은 항목을 그대로 둔 판은 통과한다.
    require_pass(run("read.value-derivation", golden_spec()))


def test_numeric_refs_must_resolve_to_fact_items() -> None:
    """역참조가 해소되지 않으면 중요분 도출이 무의미해진다 — 고르는 일 전체가 이 참조 하나에 걸려 있다(재정 P-B)."""
    require_pass(run("read.pointer-resolve", golden_spec()))  # 대조군

    dangling = golden_spec()
    item(dangling, M_IMPLICATION)["numeric_refs"] = ["M999"]
    require_fail(run("read.pointer-resolve", dangling), "pointer.resolve")

    # 해소는 되지만 **fact 가 아닌** 항목을 가리키는 판. 존재만 보면 이것이 통과한다.
    wrong_kind = golden_spec()
    item(wrong_kind, M_POSITIONING)["numeric_refs"] = [M_E1]
    row = run("read.pointer-resolve", wrong_kind)
    require_fail(row, "pointer.kind")
    if f"{M_POSITIONING}.numeric_refs[0]" not in {finding.locus for finding in row.findings}:
        pytest.fail(f"역참조의 좌표가 결함에 실리지 않았다: {[f.locus for f in row.findings]}")
