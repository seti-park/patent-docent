# -*- coding: utf-8 -*-
"""READ 실행 경로(`engine/**` · `reader/procedure/**`)의 pytest.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다
(SPEC §8.4 검증 계획표의 '반증 대상' 열과 같은 형식).

`assert` 를 쓰지 않는다 — `python3 -O` 에서 전부 제거되어 망가진 코드가 공허 통과한다
(CLAUDE.md §3). 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고한다.

★ 픽스처 두 경로. 공유 코퍼스(`tests/fixtures/reader/base/`)는 다른 레인의 작업 구역이며
있으면 쓰고 없으면 이 파일이 `tmp_path` 에 자체 가공 원천·레인 응답을 만들어 통주한다.
두 경로 모두 시험을 남기는 이유는, 공유 코퍼스가 생기는 날 이 파일이 조용히 낡지 않게
하기 위해서다.
"""

from __future__ import annotations

import ast
import copy
import glob
import hashlib
import json
import os
import re
import shutil
import stat
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine import paths as engine_paths  # noqa: E402
from engine.lanes.contract import LaneContractError, LanePending, LaneRequest  # noqa: E402
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.lanes.plan import (  # noqa: E402
    MAX_FANOUT,
    batched,
    highest_item_number,
    lane_id_for,
    lane_profiles,
    plan_decompose,
    plan_grounding,
    plan_synthesis,
    referenced_figures,
)
from engine.lanes.replay_adapter import ReplayLaneAdapter  # noqa: E402
from engine.paths import RunPaths, format_parameter  # noqa: E402
from engine.read_view import ReadView  # noqa: E402
from engine.render.material_spec_md import render  # noqa: E402
from engine.stages import StageError, load_json, load_yaml, read_text  # noqa: E402
from engine.stages import freeze as freeze_stage  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402
from engine.stages import source as source_stage  # noqa: E402
from reader.lib import READ_CHECK_IDS, run_read_checks  # noqa: E402
from reader.lib.report import CheckContext  # noqa: E402
from reader.lib.rules import Rules  # noqa: E402
from reader.lib.spec_io import load_schema  # noqa: E402

RULES = Rules.load()
SCHEMA = load_schema()
PROFILES = lane_profiles(REPO)

SHARED_CORPUS = os.path.join(REPO, "tests", "fixtures", "reader", "base")
CORPUS_SOURCE = os.path.join(SHARED_CORPUS, "patent.md")
CORPUS_SPEC = os.path.join(SHARED_CORPUS, "material-spec.json")

RUN_ID = "example-xx1111111a1-rotary-feeder"

# ---------------------------------------------------------------------------
# 가공 원천 — 실재 특허가 아니며 실재 특허를 인용하지 않는다.
# ---------------------------------------------------------------------------

SOURCE = """# Rotary Feeder Assembly — worked example (fictional)

Applicant: Example Powders, Inc.

## Claims

1. A feeder assembly comprising: a hopper defining an outlet aperture; and a rotary valve seated below the outlet aperture, the rotary valve having a plurality of pockets.

3. The feeder assembly of claim 1, wherein each pocket has a nominal volume of 25 cm3.

## Brief description of the drawings

FIG. 1 is a section view of the feeder assembly.

## Description

[0011] Known feeders meter powder with a screw, which grinds the powder against the barrel wall.

[0012] The rotary valve 220 is seated below the outlet aperture 112 of the hopper 110, and the pockets carry the powder without shearing it, so the screw is removed from the metering path.

[0013] Each pocket 224 has a nominal volume of 25 cm3, and the drawings do not mark this volume.

[0014] In the illustrated arrangement the valve turns at 12 rpm.
"""

CLAIM_1 = (
    "A feeder assembly comprising: a hopper defining an outlet aperture; and a rotary "
    "valve seated below the outlet aperture, the rotary valve having a plurality of pockets."
)
CLAIM_3 = (
    "The feeder assembly of claim 1, wherein each pocket has a nominal volume of 25 cm3."
)
E1_TEXT = "a hopper defining an outlet aperture;"
E2_TEXT = (
    "a rotary valve seated below the outlet aperture, the rotary valve having a "
    "plurality of pockets."
)
E2_TEXT_VARIANT = "a rotary valve seated below the outlet aperture"
A1_TEXT = "wherein each pocket has a nominal volume of 25 cm3"
CAPTION = "FIG. 1 is a section view of the feeder assembly."
SPEC_QUOTE_M4 = "the outlet aperture 112 of the hopper 110"
SPEC_QUOTE_M5 = "The rotary valve 220 is seated below the outlet aperture 112"
SPEC_QUOTE_M6 = (
    "Each pocket 224 has a nominal volume of 25 cm3, and the drawings do not mark this volume"
)
FACT_QUOTE_M7 = "a nominal volume of 25 cm3"
FACT_QUOTE_M8 = "the valve turns at 12 rpm"
EVIDENCE_M11 = (
    "the pockets carry the powder without shearing it, so the screw is removed from the "
    "metering path"
)
BACKGROUND_QUOTE = (
    "Known feeders meter powder with a screw, which grinds the powder against the barrel wall."
)
SEARCH_NOTE = (
    "FIG-1 의 전 도면부호(110·112·220·224)와 캡션을 확인했으나 포켓 용적 치수는 도면에 "
    "표기되지 않음."
)


def _value_span(quote: str, value: str) -> dict:
    """`quote` 문자열 **내부의** 문자 오프셋(0-based, end exclusive). 손으로 적지 않는다."""
    start = quote.index(value)
    return {"start": start, "end": start + len(value)}


# ---------------------------------------------------------------------------
# 레인 응답 payload — D5 단계별 산출
# ---------------------------------------------------------------------------


def decompose_payload(*, verdict: str = "go", element_two: str = E2_TEXT) -> dict:
    return {
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
                            "text_verbatim": element_two,
                            "material_id": "M2",
                            "children": [],
                        },
                    ],
                }
            ],
            "dependents": [
                {
                    "id": "CL-3",
                    "depends_on": ["CL-1"],
                    "dependency_type": "single",
                    "text_verbatim": CLAIM_3,
                    "additions": [
                        {
                            "id": "CL-3/a1",
                            "attaches_to": "CL-1/e2",
                            "text_verbatim": A1_TEXT,
                            "material_id": "M3",
                        }
                    ],
                }
            ],
            "applicant_interest": [
                {
                    "claim": "CL-1",
                    "signal": (
                        "The interest is staked on metering by pocket volume instead of by "
                        "a screw."
                    ),
                    "material_id": "M11",
                }
            ],
        },
        "items": [
            {
                "id": "M1",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e1",
                "label_en": "hopper defining an outlet aperture",
                "text_verbatim": E1_TEXT,
            },
            {
                "id": "M2",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-1/e2",
                "label_en": "rotary valve with pockets seated below the aperture",
                "text_verbatim": element_two,
            },
            {
                "id": "M3",
                "kind": "component",
                "status": "active",
                "superseded_by": None,
                "claim_ref": "CL-3/a1",
                "label_en": "nominal pocket volume limitation",
                "text_verbatim": A1_TEXT,
            },
        ],
        "drop_signal": {
            "stage": "early",
            "verdict": verdict,
            "reason": (
                "권리 관심이 한 구성(포켓 계량)에 뚜렷함."
                if verdict == "go"
                else "청구항이 통상적 계량 구조의 나열이라 일반 독자에게 줄 안도감이 없음."
            ),
        },
    }


def ground_independent_payload() -> dict:
    return {
        "items": [
            {
                "id": "M4",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M1",
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [{"locator": "[0012]", "quote": SPEC_QUOTE_M4}],
                "figure_refs": [
                    {"figure": "FIG-1", "numerals": ["110", "112"], "caption_quote": CAPTION}
                ],
            },
            {
                "id": "M5",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M2",
                "anchor_state": {"spec": "found", "figure": "found"},
                "spec_refs": [{"locator": "[0012]", "quote": SPEC_QUOTE_M5}],
                "figure_refs": [
                    {"figure": "FIG-1", "numerals": ["220", "224"], "caption_quote": CAPTION}
                ],
            },
        ]
    }


def ground_dependent_payload() -> dict:
    return {
        "items": [
            {
                "id": "M6",
                "kind": "grounding",
                "status": "active",
                "superseded_by": None,
                "component": "M3",
                "anchor_state": {"spec": "found", "figure": "not-depicted"},
                "spec_refs": [{"locator": "[0013]", "quote": SPEC_QUOTE_M6}],
                "figure_refs": [],
                "search_note": SEARCH_NOTE,
            }
        ]
    }


def synthesis_payload(*, verdict: str = "go") -> dict:
    return {
        "items": [
            {
                "id": "M7",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "nominal volume of one pocket",
                "origin": "quoted",
                "value_raw": "25 cm3",
                "value_normalized": "25",
                "value_type": {"kind": "scalar", "approximate": False, "value": "25"},
                "unit": "cm3",
                "machine_verifiable": True,
                "source": {
                    "locator": "claim 3",
                    "quote": FACT_QUOTE_M7,
                    "value_span": _value_span(FACT_QUOTE_M7, "25 cm3"),
                },
            },
            {
                "id": "M8",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "rotary valve speed in the illustrated arrangement",
                "origin": "quoted",
                "value_raw": "12 rpm",
                "value_normalized": "12",
                "value_type": {"kind": "scalar", "approximate": False, "value": "12"},
                "unit": "rpm",
                "machine_verifiable": True,
                "source": {
                    "locator": "[0014]",
                    "quote": FACT_QUOTE_M8,
                    "value_span": _value_span(FACT_QUOTE_M8, "12 rpm"),
                },
            },
            {
                "id": "M9",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "swept pocket volume per minute at the illustrated speed",
                "origin": "derived",
                "value_raw": "300 cm3",
                "value_normalized": "300",
                "value_type": {"kind": "scalar", "approximate": False, "value": "300"},
                "unit": "cm3",
                "machine_verifiable": True,
                "derivation": {
                    "formula": "pocket_volume_cm3 * speed_rpm",
                    "inputs": [
                        {"name": "pocket_volume_cm3", "ref": "M7"},
                        {"name": "speed_rpm", "ref": "M8"},
                    ],
                    "rounding": {"mode": "none", "digits": 0},
                },
            },
            {
                "id": "M10",
                "kind": "fact",
                "status": "active",
                "superseded_by": None,
                "label_en": "number of pockets visible in the section view",
                "origin": "figure-sourced",
                "value_raw": "6",
                "value_normalized": "6",
                "value_type": {"kind": "scalar", "approximate": False, "value": "6"},
                "unit": None,
                "machine_verifiable": False,
                "figure_source": {
                    "figure": "FIG-1",
                    "numerals": ["224"],
                    "locator": "FIG. 1",
                },
            },
            {
                "id": "M11",
                "kind": "implication",
                "status": "active",
                "superseded_by": None,
                "statement_en": (
                    "Metering by pocket volume points at removing the screw from the path "
                    "rather than making it gentler."
                ),
                "basis": "spec",
                "derived_from": ["M2", "M5"],
                "evidence_quotes": [EVIDENCE_M11],
                "confidence": "inferred",
            },
            {
                "id": "M12",
                "kind": "positioning",
                "status": "active",
                "superseded_by": None,
                "background_problem": (
                    "Known feeders meter powder with a screw that grinds the powder against "
                    "the barrel wall."
                ),
                "asserted_effect": (
                    "The specification states in words that the screw is removed from the "
                    "metering path."
                ),
                "delta": (
                    "The asserted delta is a structural change of the metering element, not "
                    "a claimed performance number."
                ),
                "quotes": [BACKGROUND_QUOTE, "the screw is removed from the metering path"],
            },
            {
                "id": "M13",
                "kind": "figure_note",
                "status": "active",
                "superseded_by": None,
                "figure": "FIG-1",
                "what_it_shows_en": (
                    "A section through the hopper and the rotary valve, with the pockets "
                    "facing the outlet aperture."
                ),
                "numerals": ["110", "112", "220", "224"],
            },
        ],
        "figures": [
            {
                "id": "FIG-1",
                "numerals": ["110", "112", "220", "224"],
                "caption_quote": CAPTION,
                "raw_path": "00-source/figures-raw/fig-01.png",
                "asset_path": None,
            }
        ],
        "drop_signal": {
            "stage": "final",
            "verdict": verdict,
            "reason": (
                "배경기술 대비 차이가 명세서 문언으로 존재하고, 도면이 그 차이를 보여줌."
                if verdict == "go"
                else "포지셔닝 확정 후에도 일반 독자에게 줄 안도감이 없음."
            ),
        },
    }


def payload_set(*, early_verdict: str = "go", element_two: str = E2_TEXT) -> dict:
    return {
        "decompose": decompose_payload(verdict=early_verdict, element_two=element_two),
        "ground-independent": ground_independent_payload(),
        "ground-dependent": ground_dependent_payload(),
        "synthesize": synthesis_payload(),
    }


# ---------------------------------------------------------------------------
# 런 작업장 조립
# ---------------------------------------------------------------------------


PATENT_META = {
    "number": "XX1111111A1",
    "title": "Rotary feeder assembly with pocket metering (fictional example)",
    "assignee": "Example Powders, Inc.",
    "dates": {"priority": "2024-05-02", "filing": "2025-04-30", "publication": "2026-02-11"},
}


def make_source_inputs(tmp_path, *, figure_count: int = 6, source_text: str = SOURCE):
    """투입물(원문 파일 + 도면 원본)을 만든다. 런 작업장 밖의 자리다."""
    inbox = os.path.join(str(tmp_path), "inbox")
    figures = os.path.join(inbox, "figures")
    os.makedirs(figures, exist_ok=True)
    patent_path = os.path.join(inbox, "patent-source.md")
    with open(patent_path, "w", encoding="utf-8") as handle:
        handle.write(source_text)
    for index in range(1, figure_count + 1):
        with open(os.path.join(figures, f"fig-{index:02d}.png"), "wb") as handle:
            handle.write(b"\x89PNG\r\n\x1a\n" + bytes([index]) * 16)
    return patent_path, figures


def run_source(tmp_path, *, figure_count: int = 6, source_text: str = SOURCE, repo=None,
               run_id: str = RUN_ID, run_root: str | None = None):
    patent_path, figures = make_source_inputs(
        tmp_path, figure_count=figure_count, source_text=source_text
    )
    root = run_root or os.path.join(str(tmp_path), "runs", run_id)
    outcome = source_stage.run(
        run_root=root,
        source_patent_path=patent_path,
        figures_dir=figures,
        run_id=run_id,
        patent_meta=copy.deepcopy(PATENT_META),
        repo=repo,
    )
    return root, outcome


def write_lane_responses(
    run_root: str,
    *,
    payloads_by_run: dict,
    attempts: tuple[int, ...] = (0, 1),
    model_override: dict | None = None,
) -> str:
    """재생 어댑터가 읽을 응답 트리를 만든다(요청은 쓰지 않는다).

    재시도 경로(`retry-1`)까지 미리 채우는 이유 — 재시도가 응답 부재로 `LanePending` 이
    되면 "재시도했다"와 "재시도 요청만 쓰고 멈췄다"를 시험이 구별하지 못한다.
    """
    paths = RunPaths(run_root)
    root = paths.lanes_dir
    for read_run, payloads in payloads_by_run.items():
        for task, payload in payloads.items():
            profile = PROFILES[task]
            model = (model_override or {}).get("model", profile["model"])
            effort = (model_override or {}).get("effort", profile["effort"])
            for attempt in attempts:
                lane_id = lane_id_for(read_run, task, 0, attempt)
                directory = os.path.join(root, *lane_id.split("/"))
                os.makedirs(directory, exist_ok=True)
                with open(
                    os.path.join(directory, "response.json"), "w", encoding="utf-8"
                ) as handle:
                    json.dump(
                        {
                            "lane_id": lane_id,
                            "model": model,
                            "effort": effort,
                            "payload": payload,
                        },
                        handle,
                        ensure_ascii=False,
                    )
    return root


def run_read(tmp_path, *, payloads_by_run=None, model_override=None, run_root=None):
    """`source` → 레인 응답 배치 → `read` 통주."""
    root = run_root
    if root is None:
        root, source_outcome = run_source(tmp_path)
        if source_outcome["status"] != "ok":
            pytest.fail(f"source 가 ok 를 내지 않았다: {source_outcome['status']}")
    payloads_by_run = payloads_by_run or {
        "read-a": payload_set(),
        "read-b": payload_set(),
    }
    lanes_root = write_lane_responses(
        root, payloads_by_run=payloads_by_run, model_override=model_override
    )
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = read_stage.run(run_root=root, adapter=adapter, rules=RULES)
    return root, outcome, adapter


def approval_envelope(
    run_root: str,
    *,
    decision: str = "approved",
    derived_ack=None,
    manual_ack=None,
    drop_decision=None,
    target_path: str = "10-read/material-spec.json",
    digest: str | None = None,
    owner_quote: str = "이 재료로 CP1 승인한다. 파생 300 cm3 은 계산값으로 이해했다.",
) -> str:
    """승인 봉투 md 를 쓴다. 봉투는 **오케스트레이터가** 쓴다는 규율의 시험용 대역이다."""
    paths = RunPaths(run_root)
    absolute = os.path.join(run_root, *target_path.split("/"))
    if digest is None:
        with open(absolute, "rb") as handle:
            digest = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    frontmatter = {
        "schema": "approval-envelope/v0",
        "checkpoint": "material_approval",
        "run_id": RUN_ID,
        "target": {"path": target_path, "digest": digest},
        "decision": decision,
        "owner_quote": owner_quote,
        "quote_provenance": {
            "channel": "session-transcript",
            "located_at": "2026-08-18 세션 · CP1 응답",
        },
        "decided_at": "2026-08-18T04:00:00Z",
        "recorded_by": "orchestrator",
        "manual_verification_ack": ["M10"] if manual_ack is None else manual_ack,
        "derived_fact_ack": ["M9"] if derived_ack is None else derived_ack,
        "numeric_whitelist_printed": [],
    }
    if decision == "rejected":
        frontmatter["directives"] = ["파생 수치의 산식을 다시 적어라."]
    if drop_decision is not None:
        frontmatter["drop_decision"] = drop_decision
    path = paths.approval(1)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"---\n{body}---\n\n# CP1 승인 — 재료 명세 v1\n")
    return path


def fail_rows(rows) -> list[str]:
    return [
        f"{row.check_id}/{finding.rule}@{finding.locus}: {finding.message}"
        for row in rows
        for finding in row.findings
    ]


# ===========================================================================
# 1. source — 조기 보고
# ===========================================================================


def test_source_report_precedes_read(tmp_path) -> None:
    """조기 보고가 READ 뒤에 나오면 형식 전제 미충족 소재에 독해 2회분을 태우게 됨(재정 N12)."""
    root, outcome = run_source(tmp_path)
    paths = RunPaths(root)
    if not os.path.exists(paths.source_report):
        pytest.fail("source-report.json 이 없다")
    if os.path.exists(paths.material_spec_json):
        pytest.fail("READ 산출물이 source 단계에서 이미 존재한다 — 순서가 뒤바뀌었다")
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")
    report = load_json(paths.source_report)
    if report["figure_count"] != 6:
        pytest.fail(f"도면 수 기대 6, 실제 {report['figure_count']}")


def test_source_report_records_recompute_basis(tmp_path) -> None:
    """도면별 행과 산정 근거가 없으면 재정 후 원천을 다시 읽어야 한다(재감수 M-04)."""
    root, _ = run_source(tmp_path)
    report = load_json(RunPaths(root).source_report)
    exhibit = report["exhibit_candidates"]
    missing = [
        key
        for key in ("tag", "unit", "formula", "rationale", "provisional_resolutions", "floor")
        if not exhibit.get(key)
    ]
    if missing:
        pytest.fail(f"exhibit_candidates 에 산정 근거가 빠졌다: {missing}")
    if exhibit["tag"] != "[가설]":
        pytest.fail(f"산정식 태그 기대 [가설], 실제 {exhibit['tag']}")
    if len(exhibit["provisional_resolutions"]) != 3:
        pytest.fail(f"미결 3논점 기대 3건, 실제 {len(exhibit['provisional_resolutions'])}건")
    for row in report["figures"]:
        for key in ("filename", "bytes", "sha256", "counted_as"):
            if key not in row:
                pytest.fail(f"도면 행에 {key} 가 없다: {row}")
    recomputed = sum(row["counted_as"] for row in report["figures"])
    if recomputed != exhibit["count"]:
        pytest.fail(f"소급 재계산 {recomputed} != 보고값 {exhibit['count']}")


def test_source_records_canonicalization_provenance(tmp_path) -> None:
    """정본화 변환을 기록하지 않으면 원본으로 되짚을 수 없다(§1.3 정본 생성 규약)."""
    dirty = SOURCE.replace("25 cm3", "25 cm3").replace("12 rpm", "12⁢rpm")
    root, outcome = run_source(tmp_path, source_text=dirty)
    paths = RunPaths(root)
    canonical = read_text(paths.patent_md)
    if " " in canonical or "⁢" in canonical:
        pytest.fail("정본에 변환 아티팩트(NBSP·INVISIBLE TIMES)가 남았다")
    provenance = read_text(paths.provenance_md)
    for needle in ("원본 SHA-256", "정본 SHA-256", "nbsp-to-space", "drop-invisible-times"):
        if needle not in provenance:
            pytest.fail(f"PROVENANCE.md 에 {needle} 기록이 없다")
    report = load_json(paths.source_report)
    if report["source"]["original_sha256"] == report["source"]["canonical_sha256"]:
        pytest.fail("변환이 있었는데 원본·정본 다이제스트가 같다")
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']}")


def test_missing_figures_escalates_with_distinct_reason(tmp_path) -> None:
    """도면 부재 escalate 가 D4 drop 제안과 같은 사유로 기록되면 둘이 사후에 구별 불가."""
    root, outcome = run_source(tmp_path, figure_count=0)
    if outcome["status"] != "escalate":
        pytest.fail(f"status 기대 escalate, 실제 {outcome['status']}")
    if outcome["reason_label"] != "형식 전제 미충족":
        pytest.fail(f"사유 기대 '형식 전제 미충족', 실제 {outcome['reason_label']!r}")
    _ = root


def test_exhibit_candidate_floor_comes_from_sheet(tmp_path) -> None:
    """하한이 코드 리터럴이면 시트를 고쳐도 판정이 따라 바뀌지 않는다(재정 N12)."""
    floor = format_parameter("tweet_count.value.min")
    if floor != 6:
        pytest.fail(f"현행 시트 하한 기대 6, 실제 {floor}")

    # ① 정본 시트(하한 6)에서 도면 4개 → 미충족
    _, strict = run_source(
        tmp_path, figure_count=4, run_root=os.path.join(str(tmp_path), "runs", RUN_ID)
    )
    if strict["status"] != "escalate":
        pytest.fail(f"하한 6 에서 도면 4개는 escalate 여야 한다, 실제 {strict['status']}")

    # ② 하한만 3 으로 바꾼 계약 사본에서 같은 입력 → 통과
    fake_repo = os.path.join(str(tmp_path), "fake-repo")
    shutil.copytree(os.path.join(REPO, "contracts"), os.path.join(fake_repo, "contracts"))
    os.makedirs(os.path.join(fake_repo, "reader"), exist_ok=True)
    shutil.copy2(
        os.path.join(REPO, "reader", "READER-VERSION"),
        os.path.join(fake_repo, "reader", "READER-VERSION"),
    )
    sheet_path = os.path.join(fake_repo, "contracts", "format-parameters.yaml")
    with open(sheet_path, encoding="utf-8") as handle:
        sheet = yaml.safe_load(handle)
    sheet["parameters"]["tweet_count"]["value"]["min"] = 3
    with open(sheet_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(sheet, handle, allow_unicode=True, sort_keys=False)

    _, relaxed = run_source(
        tmp_path,
        figure_count=4,
        repo=fake_repo,
        run_root=os.path.join(str(tmp_path), "runs2", RUN_ID),
    )
    if relaxed["status"] != "ok":
        pytest.fail(
            f"하한 3 에서 도면 4개는 통과여야 한다, 실제 {relaxed['status']} — "
            f"{fail_rows(relaxed['rows'])}"
        )
    if relaxed["report"]["exhibit_candidates"]["floor"]["value"] != 3:
        pytest.fail("보고서가 시트 하한을 그대로 싣지 않는다")


def test_source_refuses_to_write_00_source_twice(tmp_path) -> None:
    """00-source/ 를 두 번 쓸 수 있으면 '원천 고정'이 이름뿐이다(SPEC §7.4)."""
    root, _ = run_source(tmp_path)
    patent_path, figures = make_source_inputs(tmp_path, figure_count=6)
    with pytest.raises(StageError):
        source_stage.run(
            run_root=root,
            source_patent_path=patent_path,
            figures_dir=figures,
            run_id=RUN_ID,
            patent_meta=copy.deepcopy(PATENT_META),
        )


def test_bibliographic_head_stops_at_the_body_not_at_the_claims_heading() -> None:
    """서지 머리가 명세서 본문까지 삼키면, 레인에 조각이 아니라 원천 전문을 넘기게 된다.

    ★ 회귀 표본이다(2026-08-18 실특허 스모크 실측). 구현 초판은 경계를 청구항 구간 헤더로만
    잡았는데 **실제 공개공보는 청구항을 문서 끝에 둔다** — 그 배치에서 293KB 원천의 서지 머리가
    285KB(문서의 97%)로 나왔다. 합성 픽스처는 청구항을 앞쪽에 두어 이 결함을 가렸으므로,
    이 테스트는 **실물 배치**(서지 → 본문 → 청구항)를 명시적으로 재현한다.
    """
    source_text = (
        "United States\n"
        "Patent Application Publication: 00000000\n"
        "Publication Date: May 28, 2026\n"
        "\n"
        "## EXAMPLE TITLE\n"
        "\n"
        "### Abstract\n"
        "\n"
        "An abstract sentence.\n"
        "\n"
        "### Background/Summary\n"
        "\n"
        + "".join(
            f"[{n:04d}] Body paragraph {n} that must not be counted as bibliographic head.\n"
            for n in range(1, 40)
        )
        + "\n"
        "## Claims\n"
        "\n"
        "1. A device comprising: a widget.\n"
    )
    head = ReadView(source_text, RULES).bibliographic_head()
    assert "[0001]" not in head, "서지 머리가 명세서 본문 문단을 삼켰다"
    assert "1. A device comprising" not in head, "서지 머리가 청구항까지 삼켰다"
    assert "EXAMPLE TITLE" in head, "서지 머리가 제목을 놓쳤다"
    assert "An abstract sentence." in head, "서지 머리가 초록을 놓쳤다"
    # 문서의 절반을 넘기면 그것은 슬라이스가 아니라 전문 전달이다.
    assert len(head) < len(source_text) / 2, (
        f"서지 머리가 원천의 {len(head) / len(source_text):.0%} 를 차지한다 — 슬라이싱이 아니다"
    )


# ===========================================================================
# 2. 레인 계약
# ===========================================================================


def test_lane_request_declares_model_and_effort() -> None:
    """모델 미지정 요청이 만들어지면 레인 지정이 프롬프트 문구로 미끄러진다(SPEC §7.3 규율 2)."""
    view = ReadView(SOURCE, RULES)
    for request in plan_decompose("read-a", view, PROFILES):
        if not request.model or not request.effort:
            pytest.fail(f"{request.lane_id}: model·effort 가 비었다")
        if request.model != PROFILES["decompose"]["model"]:
            pytest.fail(
                f"모델이 계약과 다르다: {request.model} != {PROFILES['decompose']['model']}"
            )
    with pytest.raises(LaneContractError):
        LaneRequest(
            lane_id="read-a/decompose/batch-0",
            read_run="read-a",
            task="decompose",
            model="",
            effort="max",
            prompt_path="reader/procedure/10-decompose.md",
            instructions="",
            slices={},
            response_schema={"type": "object"},
            batch=0,
        )


def test_lane_effort_ladder_comes_from_contract() -> None:
    """effort 를 코드에 박으면 재정으로 레인을 낮춰도(R3) 러너가 따라오지 않는다."""
    contract = engine_paths.load_stage_contract("read")
    declared = {
        entry["id"]: (entry["model"], entry["effort"])
        for entry in contract["lane"]["sub_lanes"]
    }
    for task, profile in PROFILES.items():
        if (profile["model"], profile["effort"]) != declared[task]:
            pytest.fail(
                f"{task}: 로더 {profile['model']}/{profile['effort']} != "
                f"계약 {declared[task][0]}/{declared[task][1]}"
            )


def test_synthesis_request_names_every_figure_the_grounding_referenced() -> None:
    """등재 지시가 없으면 `figure_refs` 가 해소될 도면이 존재하지 않는다 — 유령 참조가 구조적으로 발생한다.

    ★ 2026-08-18 실특허 스모크에서 접지 레인이 올린 결합 공백이다. `figures[]` 는
    **synthesize 산출에서만** 조립되는데 `figure_refs[].figure` 는 `read.pointer-resolve` 가
    그 배열에 대고 해소한다. 접지 레인은 자기가 참조한 도면을 등재할 수단이 없고 synthesize 는
    무엇이 참조되었는지 알 방법이 없었다 — 두 레인 사이에 **아무도 책임지지 않는 구간**이
    있었다. 그 구간은 레인이 아무리 성실해도 닫히지 않는다.
    """
    view = ReadView(SOURCE, RULES)
    profiles = lane_profiles()
    claims = decompose_payload()["claims"]
    groundings = [ground_independent_payload(), ground_dependent_payload()]

    referenced = referenced_figures(groundings)
    assert referenced, "픽스처의 접지 산출이 도면을 하나도 참조하지 않는다 — 이 테스트가 공허해진다"

    request = plan_synthesis("read-a", claims, view, profiles, groundings=groundings)[0]
    for figure_id in referenced:
        assert figure_id in request.instructions, (
            f"synthesize 요청이 접지가 참조한 {figure_id} 의 등재를 지시하지 않는다"
        )


def test_lane_requests_carry_disjoint_item_id_bands() -> None:
    """대역이 없거나 겹치면 두 레인이 같은 `M<n>` 을 발번하고 조립에서 항목이 조용히 사라진다.

    ★ 2026-08-18 실특허 스모크에서 레인이 지적하고 총괄이 재현한 경로다. dict 인덱싱이
    뒤엣것으로 덮어쓰며, 결번이 아니므로 ID 연속성 검사도 보지 못한다.
    `pointer.item-id-unique` 가 충돌을 **잡지만** 잡히면 런이 실패한다 — 이 테스트가 보는
    것은 **예방** 쪽이며, 탐지와 예방은 다른 일이다.
    """
    view = ReadView(SOURCE, RULES)
    profiles = lane_profiles()
    claims = decompose_payload()["claims"]
    requests = plan_grounding("read-a", claims, view, profiles) + plan_synthesis(
        "read-a", claims, view, profiles
    )
    highest = highest_item_number(claims)
    assert highest >= 1, "분해 산출에서 발번된 M<n> 을 하나도 찾지 못했다 — 픽스처가 대역 시험을 못 한다"

    bands: list[tuple[int, int]] = []
    for request in requests:
        found = re.search(r"`M(\d+)` ~ `M(\d+)` 안에서만 발번", request.instructions)
        assert found, f"{request.lane_id} 요청에 항목 ID 대역이 없다"
        low, high = int(found.group(1)), int(found.group(2))
        assert low > highest, (
            f"{request.lane_id} 대역이 이미 발번된 M{highest} 를 침범한다 (M{low} 부터 시작)"
        )
        bands.append((low, high))

    ordered = sorted(bands)
    for (low_a, high_a), (low_b, _) in zip(ordered, ordered[1:]):
        assert high_a < low_b, f"대역이 겹친다: M{low_a}~M{high_a} 와 M{low_b}~"
    assert len(bands) == len(requests), "요청 수와 대역 수가 다르다"


def test_lane_fanout_batch_under_cap() -> None:
    """한 배치가 30건 이상이면 팬아웃 규율(런당 30 미만)이 문서로만 존재한다."""
    if MAX_FANOUT >= 30:
        pytest.fail(f"MAX_FANOUT 기대 < 30, 실제 {MAX_FANOUT}")
    claims = {
        "independent": [
            {
                "id": "CL-1",
                "text_verbatim": CLAIM_1,
                "elements": [
                    {
                        "id": f"CL-1/e{index}",
                        "text_verbatim": f"element {index}",
                        "material_id": f"M{index}",
                        "children": [],
                    }
                    for index in range(1, 101)
                ],
            }
        ],
        "dependents": [],
    }
    view = ReadView(SOURCE, RULES)
    requests = plan_grounding("read-a", claims, view, PROFILES)
    independent = [entry for entry in requests if entry.task == "ground-independent"]
    if len(independent) != 4:
        pytest.fail(f"100건 → 배치 기대 4개(29·29·29·13), 실제 {len(independent)}개")
    for position, request in enumerate(independent):
        if request.batch != position:
            pytest.fail(f"배치 번호가 어긋난다: {request.batch} != {position}")
    sizes = [len(chunk) for chunk in batched(list(range(100)))]
    if max(sizes) >= 30:
        pytest.fail(f"배치 크기 기대 < 30, 실제 {max(sizes)}")


def test_file_adapter_writes_request_and_raises_pending(tmp_path) -> None:
    """응답을 기다리면 체크포인트 무응답이 시간 초과 자동 진행으로 미끄러진다(재정 R8)."""
    view = ReadView(SOURCE, RULES)
    requests = plan_decompose("read-a", view, PROFILES)
    root = os.path.join(str(tmp_path), "lanes")
    adapter = FileLaneAdapter(root)
    with pytest.raises(LanePending) as excinfo:
        adapter.dispatch(requests)
    if excinfo.value.pending != [requests[0].lane_id]:
        pytest.fail(f"미충족 목록 기대 {[requests[0].lane_id]}, 실제 {excinfo.value.pending}")
    directory = os.path.join(root, *requests[0].lane_id.split("/"))
    for name in ("request.json", "request.md"):
        if not os.path.exists(os.path.join(directory, name)):
            pytest.fail(f"요청 파일 {name} 이 없다")
    written = json.load(open(os.path.join(directory, "request.json"), encoding="utf-8"))
    if written["model"] != PROFILES["decompose"]["model"]:
        pytest.fail("request.json 이 모델을 싣지 않았다")
    prompt = read_text(os.path.join(directory, "request.md"))
    if "청구항 구성요소 전 분해" not in prompt:
        pytest.fail("request.md 에 절차 문서가 인라인으로 실리지 않았다")


def test_lane_response_violating_schema_is_rejected(tmp_path) -> None:
    """응답 계약을 검사하지 않으면 무엇이 와도 조립까지 흘러간다."""
    view = ReadView(SOURCE, RULES)
    requests = plan_decompose("read-a", view, PROFILES)
    root = os.path.join(str(tmp_path), "lanes")
    directory = os.path.join(root, *requests[0].lane_id.split("/"))
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "response.json"), "w", encoding="utf-8") as handle:
        json.dump(
            {
                "lane_id": requests[0].lane_id,
                "model": PROFILES["decompose"]["model"],
                "effort": PROFILES["decompose"]["effort"],
                "payload": {"claims": {}, "items": [], "drop_signal": {}},
            },
            handle,
        )
    with pytest.raises(LaneContractError):
        ReplayLaneAdapter(root).dispatch(requests)


def test_lane_model_mismatch_is_recorded_as_defect(tmp_path) -> None:
    """실호출 모델이 요청과 달라도 조용히 넘어가면 조용한 대체가 성립한다(SPEC §7.3 규율 4)."""
    root, _ = run_source(tmp_path)
    lanes_root = write_lane_responses(
        root,
        payloads_by_run={"read-a": payload_set(), "read-b": payload_set()},
        model_override={"model": "haiku-imposter", "effort": "low"},
    )
    adapter = ReplayLaneAdapter(lanes_root)
    with pytest.raises(read_stage.LaneAssignmentError):
        read_stage.run(run_root=root, adapter=adapter, rules=RULES)
    log = load_json(RunPaths(root).lane_log)
    mismatched = [row for row in log if row["mismatch"]]
    if not mismatched:
        pytest.fail("레인 기록에 mismatch 행이 없다")
    if mismatched[0]["actual_model"] != "haiku-imposter":
        pytest.fail(f"실호출 모델이 기록되지 않았다: {mismatched[0]}")
    if mismatched[0]["requested_model"] != PROFILES["decompose"]["model"]:
        pytest.fail("요청 모델이 기록되지 않았다")


# ===========================================================================
# 3. read — D5 5단계와 산출물
# ===========================================================================


def test_read_emits_all_five_stage_artifacts(tmp_path) -> None:
    """중간 산출물 누락이 통과하면 '검증 가능한 중간 산출물' 규율이 공허하다."""
    root, outcome, _ = run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")
    paths = RunPaths(root)
    expected = [
        paths.claim_tree("CL-1"),
        paths.grounding_md,
        paths.positioning_md,
        paths.drop_signal_md,
        paths.material_spec_md,
        paths.material_spec_json,
        paths.convergence_json,
    ]
    missing = [path for path in expected if not os.path.exists(path)]
    if missing:
        pytest.fail(f"산출물 누락: {[os.path.basename(path) for path in missing]}")
    tree = read_text(paths.claim_tree("CL-1"))
    if "CL-3/a1" not in tree:
        pytest.fail("청구항 트리에 종속항 부가 한정이 누적되지 않았다")


def test_read_passes_every_deterministic_check(tmp_path) -> None:
    """조립본이 READ 검사 전종을 통과하지 못하면 이 파일의 다른 통주 시험이 전부 무의미하다."""
    _, outcome, _ = run_read(tmp_path)
    failing = [row.check_id for row in outcome["rows"] if row.status == "fail"]
    if failing:
        pytest.fail(f"실패한 검사: {failing} — {fail_rows(outcome['rows'])}")
    # 행 수를 리터럴로 적지 않는다 — 검사가 늘면 이 시험이 그 사실을 따라간다.
    produced = [row.check_id for row in outcome["rows"]]
    if produced != list(READ_CHECK_IDS):
        pytest.fail(f"검사 행 기대 {list(READ_CHECK_IDS)}, 실제 {produced}")


def test_read_rejects_source_digest_mismatch(tmp_path) -> None:
    """원천이 바뀐 채 진행되면 모든 verbatim 검사의 기준점이 붕괴한다."""
    root, _ = run_source(tmp_path)
    paths = RunPaths(root)
    with open(paths.patent_md, "a", encoding="utf-8") as handle:
        handle.write("\n[0015] Silently appended after the digest was pinned.\n")
    lanes_root = write_lane_responses(
        root, payloads_by_run={"read-a": payload_set(), "read-b": payload_set()}
    )
    outcome = read_stage.run(
        run_root=root, adapter=ReplayLaneAdapter(lanes_root), rules=RULES
    )
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    if os.path.exists(paths.material_spec_json):
        pytest.fail("다이제스트 불일치인데 재료 명세가 쓰였다")


def test_drop_signal_emitted_at_both_stages(tmp_path) -> None:
    """1단만 나와도 통과하면 D4 2단 신호가 실효 없다."""
    root, _, _ = run_read(tmp_path)
    text = read_text(RunPaths(root).drop_signal_md)
    for needle in ("`early`", "`final`", "청구항 분해 직후", "포지셔닝 확정 후"):
        if needle not in text:
            pytest.fail(f"drop-signal.md 에 {needle} 이 없다")


def test_early_drop_signal_halts_before_grounding(tmp_path) -> None:
    """조기 신호가 접지 지출 뒤에 멈추면 하류 산출물이 Owner 판단을 오염시킨다(D4)."""
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(early_verdict="drop-proposed"),
        "read-b": payload_set(early_verdict="drop-proposed"),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = read_stage.run(run_root=root, adapter=adapter, rules=RULES)
    if outcome["status"] != "escalate":
        pytest.fail(f"status 기대 escalate, 실제 {outcome['status']}")
    if outcome["reason_label"] != "안도감 부적합":
        pytest.fail(f"사유 기대 '안도감 부적합', 실제 {outcome['reason_label']!r}")
    tasks = adapter.tasks_dispatched()
    spent = [task for task in tasks if task.startswith("ground") or task == "synthesize"]
    if spent:
        pytest.fail(f"조기 drop 인데 하류 레인이 돌았다: {spent}")
    text = read_text(RunPaths(root).drop_signal_md)
    if "미산출" not in text:
        pytest.fail("drop-signal.md 가 최종 신호 미산출 사실을 적지 않았다")


def test_convergence_failure_escalates_after_one_retry(tmp_path) -> None:
    """무한 재시도되면 불안정 신호가 은폐된다(수렴 미달 = 절차 신호)."""
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(),
        "read-b": payload_set(element_two=E2_TEXT_VARIANT),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = read_stage.run(run_root=root, adapter=adapter, rules=RULES)
    if outcome["status"] != "escalate":
        pytest.fail(f"status 기대 escalate, 실제 {outcome['status']}")
    failing = [row.check_id for row in outcome["rows"] if row.status == "fail"]
    if failing != ["read.convergence"]:
        pytest.fail(f"실패 검사 기대 ['read.convergence'], 실제 {failing}")
    detail = outcome["convergence"]["convergence_detail"]
    if detail["attempt"] != 2:
        pytest.fail(f"시도 횟수 기대 2(최초 + 재시도 1), 실제 {detail['attempt']}")
    retried = [
        request.lane_id for request in adapter.dispatched if "/retry-1/" in request.lane_id
    ]
    if not retried:
        pytest.fail("재시도 요청이 만들어지지 않았다")
    if os.path.exists(RunPaths(root).material_spec_json):
        pytest.fail("검사 실패인데 재료 명세가 확정되었다(C5 위반)")


def test_retry_returns_defects_to_the_lane(tmp_path) -> None:
    """결함 목록을 되돌려 주지 않으면 재시도가 같은 오류를 재생산한다."""
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(),
        "read-b": payload_set(element_two=E2_TEXT_VARIANT),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    read_stage.run(run_root=root, adapter=adapter, rules=RULES)
    retried = [
        request for request in adapter.dispatched if "/retry-1/" in request.lane_id
    ]
    if not retried:
        pytest.fail("재시도 요청이 없다")
    if "재시도 — 직전 판의 결함" not in retried[0].instructions:
        pytest.fail("재시도 지시에 결함 목록이 실리지 않았다")
    if "convergence" not in retried[0].instructions:
        pytest.fail("재시도 지시가 어떤 검사가 실패했는지 밝히지 않았다")


def test_convergence_json_validates_against_contract(tmp_path) -> None:
    """산출이 `convergence/v0` 를 벗어나면 CP1 표면의 입력 계약이 성립하지 않는다."""
    root, outcome, _ = run_read(tmp_path)
    payload = load_json(RunPaths(root).convergence_json)
    with open(
        os.path.join(REPO, "contracts", "schemas", "convergence.schema.json"),
        encoding="utf-8",
    ) as handle:
        schema = json.load(handle)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        pytest.fail(f"convergence/v0 위반 {len(errors)}건: {errors[0].message}")
    if payload["manual_verification_required"][0]["material_id"] != "M10":
        pytest.fail("도면 유래 수치가 사람 검증 목록에 오르지 않았다")
    if payload["grounding_exceptions"][0]["material_id"] != "M6":
        pytest.fail("접지 예외가 목록에 오르지 않았다")
    _ = outcome


def test_lane_log_records_every_round_trip(tmp_path) -> None:
    """레인 왕복이 기록되지 않으면 '어떤 모델이 무엇을 답했는가'를 사후에 알 수 없다."""
    root, _, adapter = run_read(tmp_path)
    log = load_json(RunPaths(root).lane_log)
    if len(log) != len(adapter.dispatched):
        pytest.fail(f"기록 {len(log)}행 != 발송 {len(adapter.dispatched)}건")
    for row in log:
        for key in ("requested_model", "requested_effort", "actual_model", "actual_effort"):
            if not row.get(key):
                pytest.fail(f"레인 기록에 {key} 가 없다: {row}")
        if row["mismatch"]:
            pytest.fail(f"정상 런인데 mismatch 가 참이다: {row}")


# ===========================================================================
# 4. CP1 표면
# ===========================================================================


def test_kr_render_contains_every_material_id(tmp_path) -> None:
    """판독본이 항목을 빠뜨려도 통과하면 CP1 검토 표면이 불완전하다."""
    root, outcome, _ = run_read(tmp_path)
    rendered = read_text(RunPaths(root).material_spec_md)
    missing = [
        item["id"]
        for item in outcome["spec"]["items"]
        if item["id"] not in rendered
    ]
    if missing:
        pytest.fail(f"판독본에 없는 항목: {missing}")


def test_cp1_render_is_byte_deterministic(tmp_path) -> None:
    """렌더가 실행마다 달라지면 무엇이 승인되었는지 말할 수 없다."""
    root, outcome, _ = run_read(tmp_path)
    convergence = outcome["convergence"]
    first = render(outcome["spec"], convergence)
    second = render(copy.deepcopy(outcome["spec"]), copy.deepcopy(convergence))
    if first != second:
        pytest.fail("같은 입력의 두 렌더가 바이트로 다르다")
    on_disk = read_text(RunPaths(root).material_spec_md)
    if on_disk != first:
        pytest.fail("디스크의 판독본이 렌더 결과와 다르다")


def test_cp1_surface_separates_three_numeric_classes(tmp_path) -> None:
    """파생 수치가 원문 수치와 같은 층으로 보이면 '계산값을 실어도 되는가'를 판단할 자리가 없다."""
    root, _, _ = run_read(tmp_path)
    rendered = read_text(RunPaths(root).material_spec_md)
    for needle in (
        "### 6.1 원문 스팬 수치",
        "### 6.2 파생 수치",
        "### 6.3 도면 유래 수치",
    ):
        if needle not in rendered:
            pytest.fail(f"수치 3분류 절이 없다: {needle}")
    derived_section = rendered.split("### 6.2 파생 수치")[1].split("### 6.3")[0]
    for needle in ("pocket_volume_cm3 * speed_rpm", "M7", "M8", FACT_QUOTE_M7):
        if needle not in derived_section:
            pytest.fail(f"파생 수치 절에 {needle} 이 없다(산식·원천 스팬 병기 요건)")
    figure_section = rendered.split("### 6.3 도면 유래 수치")[1].split("## 7.")[0]
    if "기계 검증 불가" not in figure_section:
        pytest.fail("도면 유래 수치에 '기계 검증 불가' 표시가 없다")


def test_cp1_surface_exposes_grounding_exceptions(tmp_path) -> None:
    """감춰진 예외는 예외가 아니라 은폐다(재정 R3)."""
    root, _, _ = run_read(tmp_path)
    rendered = read_text(RunPaths(root).material_spec_md)
    section = rendered.split("## 8. ★ 접지 예외")[1].split("## 9.")[0]
    if "M6" not in section:
        pytest.fail("접지 예외 항목이 별도 절에 노출되지 않았다")
    if SEARCH_NOTE not in section:
        pytest.fail("search_note(KR)가 예외와 함께 실리지 않았다")
    manual_section = rendered.split("## 7. ★ 사람 검증 필요 목록")[1].split("## 8.")[0]
    if "M10" not in manual_section:
        pytest.fail("도면 유래 수치가 사람 검증 절에 노출되지 않았다")


def test_cp1_surface_carries_envelope_instructions(tmp_path) -> None:
    """봉투 작성 안내가 없으면 Owner 가 무엇을 어디에 적어야 하는지 표면에 없다."""
    root, _, _ = run_read(tmp_path)
    rendered = read_text(RunPaths(root).material_spec_md)
    for needle in (
        "15-frozen/approval-v<N>.md",
        "`target.digest`",
        "`owner_quote`",
        "`derived_fact_ack`",
        "`manual_verification_ack`",
        "`numeric_whitelist_printed`",
        "작업 레인은 봉투를 쓰지 않는다",
    ):
        if needle not in rendered:
            pytest.fail(f"승인 봉투 안내에 {needle} 이 없다")
    if "이 재료만 읽고" not in rendered:
        pytest.fail("CP1 질문이 계약에서 실리지 않았다")


# ===========================================================================
# 5. freeze
# ===========================================================================


def test_freeze_refuses_without_approval_envelope(tmp_path) -> None:
    """봉투 없이 동결되면 체크포인트 1 이 우회 가능하다."""
    root, _, _ = run_read(tmp_path)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    if os.path.exists(RunPaths(root).frozen_spec(1)):
        pytest.fail("봉투 없이 동결본이 쓰였다")


def test_freeze_writes_readonly_and_records_digest(tmp_path) -> None:
    """동결본이 쓰기 가능하면 '동결'이 이름뿐이다."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")
    frozen_path = RunPaths(root).frozen_spec(1)
    mode = stat.S_IMODE(os.stat(frozen_path).st_mode)
    if mode != 0o444:
        pytest.fail(f"권한 기대 0444, 실제 {oct(mode)}")
    frozen = load_json(frozen_path)
    if frozen["status"] != "frozen" or frozen["spec_version"] != 1:
        pytest.fail(f"버전 스탬프가 찍히지 않았다: {frozen['status']}/{frozen['spec_version']}")
    meta = load_yaml(RunPaths(root).run_yaml)
    recorded = meta["frozen"][0]["spec_digest"]
    with open(frozen_path, "rb") as handle:
        actual = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    if recorded != actual:
        pytest.fail(f"run.yaml 의 digest 가 실물과 다르다: {recorded} != {actual}")


def test_freeze_stamps_monotonic_spec_version(tmp_path) -> None:
    """버전이 되감기거나 덮어써지면 정답지 동일성이 깨진다(§7.6)."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root)
    freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    approval_envelope(root)
    with pytest.raises(StageError):
        freeze_stage.run(run_root=root, spec_version=1, rules=RULES)


def test_freeze_rejects_stale_target_digest(tmp_path) -> None:
    """승인 후 재료가 조용히 바뀌어도 통과하면 해시 결속이 장식이다(재정 R8)."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root, digest="sha256:" + "0" * 64)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    rules_hit = [
        finding.rule
        for row in outcome["rows"]
        for finding in row.findings
        if finding.rule == "approval.target-digest"
    ]
    if not rules_hit:
        pytest.fail("대상 해시 불일치가 결함으로 나오지 않았다")


def test_derived_fact_ack_must_match_derived_set(tmp_path) -> None:
    """대조 없는 ack 목록은 승인이 아니라 서명이다(재감수 M-01 잔여)."""
    root, _, _ = run_read(tmp_path)

    # ① 빠짐 — 빈 목록
    approval_envelope(root, derived_ack=[])
    missing = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    rules_hit = [
        finding.rule for row in missing["rows"] for finding in row.findings
    ]
    if "approval.ack-complete" not in rules_hit:
        pytest.fail(f"빈 derived_fact_ack 가 통과했다: {rules_hit}")
    if missing["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {missing['status']}")

    # ② 유령 — 실재하지 않는 파생 항목
    approval_envelope(root, derived_ack=["M9", "M99"])
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    phantom_rules = [
        finding.rule for row in phantom["rows"] for finding in row.findings
    ]
    if "approval.ack-no-phantom" not in phantom_rules:
        pytest.fail(f"유령 ID 가 통과했다: {phantom_rules}")

    # ③ 정확히 일치 — 통과
    approval_envelope(root, derived_ack=["M9"])
    exact = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if exact["status"] != "ok":
        pytest.fail(f"정확히 일치인데 실패했다: {fail_rows(exact['rows'])}")


def test_manual_verification_ack_must_match_figure_sourced_set(tmp_path) -> None:
    """도면 유래 수치의 확인 목록이 대조되지 않으면 '검증 불가'가 '검증 완료'로 바뀐다(재정 R1)."""
    root, _, _ = run_read(tmp_path)

    approval_envelope(root, manual_ack=[])
    missing = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if missing["status"] != "halt":
        pytest.fail(f"빈 manual_verification_ack 가 통과했다: {missing['status']}")

    approval_envelope(root, manual_ack=["M10", "M77"])
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    phantom_rules = [
        finding.rule for row in phantom["rows"] for finding in row.findings
    ]
    if "approval.ack-no-phantom" not in phantom_rules:
        pytest.fail(f"유령 ID 가 통과했다: {phantom_rules}")

    approval_envelope(root, manual_ack=["M10"])
    exact = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if exact["status"] != "ok":
        pytest.fail(f"정확히 일치인데 실패했다: {fail_rows(exact['rows'])}")


def test_freeze_render_parity_detects_missing_item(tmp_path) -> None:
    """판독본이 항목을 빠뜨려도 동결되면 CP1 표면의 불완전이 영구화한다."""
    root, _, _ = run_read(tmp_path)
    paths = RunPaths(root)
    rendered = read_text(paths.material_spec_md)
    with open(paths.material_spec_md, "w", encoding="utf-8") as handle:
        handle.write(rendered.replace("M13", "(삭제됨)"))
    approval_envelope(root)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "reject-upstream":
        pytest.fail(f"status 기대 reject-upstream, 실제 {outcome['status']}")


def test_freeze_rejects_unapproved_envelope(tmp_path) -> None:
    """`rejected` 봉투로 동결되면 이진 결정이 무의미해진다."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root, decision="rejected")
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")


# ===========================================================================
# 6. 규율 — 코드 자체에 대한 시험
# ===========================================================================


def test_no_assert_in_engine_sources() -> None:
    """`assert` 가 남아 있으면 `python3 -O` 에서 그 검증이 통째로 사라진다(CLAUDE.md §3)."""
    offenders: list[str] = []
    for path in sorted(glob.glob(os.path.join(REPO, "engine", "**", "*.py"), recursive=True)):
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                offenders.append(f"{os.path.relpath(path, REPO)}:{node.lineno}")
    if offenders:
        pytest.fail(f"engine 소스에 assert 가 있다: {offenders}")


def test_dependency_direction_is_one_way() -> None:
    """`reader/` 가 `engine/` 을 import 하면 이식 단위가 깨진다(SPEC §6.2 판별식 1).

    판정은 문자열 검색이 아니라 **import 구문의 AST**로 한다 — 주석·docstring 이
    `engine/**` 을 **언급**하는 것은 위반이 아니고(실제로 규칙 파일이 그 사실을 서술한다),
    위반은 오직 그것을 **가져오는** 일이다.
    """
    offenders: list[str] = []
    for path in sorted(glob.glob(os.path.join(REPO, "reader", "lib", "*.py"))):
        tree = ast.parse(read_text(path), filename=path)
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                if name == "engine" or name.startswith("engine."):
                    offenders.append(f"{os.path.relpath(path, REPO)}:{node.lineno} → {name}")
    if offenders:
        pytest.fail(f"이식 단위가 러너를 import 한다: {offenders}")


def test_procedure_docs_exist_for_every_task() -> None:
    """절차 문서가 없으면 레인이 무엇을 하라는 지시 없이 돌게 된다."""
    from engine.lanes.plan import PROCEDURE_DOCS, TASKS

    for task in TASKS:
        path = os.path.join(REPO, *PROCEDURE_DOCS[task].split("/"))
        if not os.path.exists(path):
            pytest.fail(f"{task} 의 절차 문서가 없다: {PROCEDURE_DOCS[task]}")
    overview = os.path.join(REPO, "reader", "procedure", "00-overview.md")
    contract_doc = os.path.join(REPO, "reader", "procedure", "40-output-contract.md")
    for path in (overview, contract_doc):
        if not os.path.exists(path):
            pytest.fail(f"절차 문서가 없다: {path}")


def test_run_paths_come_from_stage_contracts(tmp_path) -> None:
    """경로가 코드 리터럴이면 계약이 트리를 바꿔도 러너가 옛 자리에 쓴다."""
    paths = RunPaths(os.path.join(str(tmp_path), "runs", RUN_ID))
    contract = engine_paths.load_stage_contract("read")
    declared = set(contract["outputs"])
    for relative in (
        "10-read/material-spec.json",
        "10-read/material-spec.md",
        "10-read/convergence.json",
    ):
        if relative not in declared:
            pytest.fail(f"계약이 {relative} 을 선언하지 않는다 — 시험 전제가 틀렸다")
    if not paths.material_spec_json.endswith(os.path.join("10-read", "material-spec.json")):
        pytest.fail(f"경로 해석이 계약과 다르다: {paths.material_spec_json}")
    with pytest.raises(engine_paths.PathContractError):
        paths.declared("존재하지-않는-산출물.json")


# ===========================================================================
# 7. 공유 픽스처 코퍼스 경로 (다른 레인의 작업 구역)
# ===========================================================================


def test_shared_fixture_corpus_runs_end_to_end() -> None:
    """공유 코퍼스가 생겼는데 이 파일이 그것을 쓰지 않으면 두 레인의 정본이 갈라진다.

    가정 레이아웃 = `tests/fixtures/reader/base/{patent.md, material-spec.json}`.
    없으면 건너뛴다(자체 픽스처 경로가 위의 전 시험을 이미 통주한다).
    """
    if not (os.path.exists(CORPUS_SOURCE) and os.path.exists(CORPUS_SPEC)):
        pytest.skip(
            "공유 코퍼스 미존재 — tests/fixtures/reader/base/{patent.md,material-spec.json}"
        )
    source_text = read_text(CORPUS_SOURCE)
    spec = load_json(CORPUS_SPEC)
    rows = run_read_checks(
        CheckContext(
            spec=spec,
            source_text=source_text,
            rules=RULES,
            schema=SCHEMA,
            peer_spec=copy.deepcopy(spec),
        )
    )
    failing = [row.check_id for row in rows if row.status == "fail"]
    if failing:
        pytest.fail(f"공유 코퍼스가 검사를 통과하지 못한다: {failing} — {fail_rows(rows)}")
    from reader.lib import to_convergence_payload

    payload = to_convergence_payload(rows, spec)
    rendered = render(spec, payload)
    missing = [item["id"] for item in spec.get("items") or [] if item["id"] not in rendered]
    if missing:
        pytest.fail(f"공유 코퍼스 판독본에 없는 항목: {missing}")
