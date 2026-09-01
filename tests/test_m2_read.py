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
    harvest_band_start,
    highest_item_number,
    lane_id_for,
    lane_profiles,
    plan_decompose,
    plan_grounding,
    plan_synthesis,
    referenced_figures,
)
from engine.lanes.replay_adapter import (  # noqa: E402
    ReplayLaneAdapter as _EngineReplayLaneAdapter,
)
from engine.paths import RunPaths, format_parameter  # noqa: E402
from engine.read_view import ReadView  # noqa: E402
from engine.render.material_spec_md import ANSWER_SCOPE_TEXT, render  # noqa: E402
from engine.stages import (  # noqa: E402
    StageEnvironmentError,
    StageError,
    StageHaltError,
    load_json,
    load_yaml,
    read_text,
)
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

# 조립본의 최종 ID 배치 — 레인 투입 순서가 그대로 번호가 된다
# (분해 → 접지 → **수확** → 통합, `engine/stages/read.py#lane_payloads`).
#
#   M1~M3    분해 — 구성요소 3
#   M4~M6    접지 — 독립항 2 · 종속항 1
#   M7~M12   **수확** — 원문 스팬 2 + 서지 4 (재정 P-B)
#   M13~M17  통합 — 파생 · 도면 유래 · 함의 · 포지셔닝 · 도면 노트
#
# 이 배치는 `test_assembled_item_layout_follows_lane_order` 가 실물로 확인한다 — 상수만 두면
# 배치가 바뀌었을 때 아래 시험들이 엉뚱한 항목을 가리키며 통과할 수 있다.
DERIVED_FACT_ID = "M13"
FIGURE_FACT_ID = "M14"

# 수확 6건의 좌표(원문 스팬 2 + 서지 4). 순서는 수확기의 등장 순이다.
HARVESTED_LABELS = (
    "12 rpm",
    "25 cm3",
    "patent.number",
    "patent.dates.priority",
    "patent.dates.filing",
    "patent.dates.publication",
)

# ---------------------------------------------------------------------------
# 가공 원천 — 실재 특허가 아니며 실재 특허를 인용하지 않는다.
# ---------------------------------------------------------------------------

SOURCE = """# Rotary Feeder Assembly — worked example (fictional)

Applicant: Example Powders, Inc.
Inventors: Mira Solberg; Tomas Weill
Priority: application XX2024-0000222 filed on 2 May 2024 (XX)
Int. Cl.: B65G 65/48
CPC: B65G 65/48

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
SPEC_QUOTE_SPEED = "the valve turns at 12 rpm"
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


def decompose_payload(
    *,
    direction: str = "clear",
    element_two: str = E2_TEXT,
    note: str | None = None,
    dependency_type: str = "single",
    claim_three_text: str | None = None,
) -> dict:
    """분해 레인 1회분.

    ★ `drop_signal`(stage: early)이 사라지고 `screening_memo` 가 그 자리에 섰다(재정 P-A).
    조기 판단은 상신하지 않고 기록만 하며 러너를 세우지 않는다 — 확정 재정의 자리는 CP1
    한 곳이다. 메모는 `read-a`·`read-b` 가 **각자** 쓴다(재정 P-U4).
    """
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
                    "dependency_type": dependency_type,
                    "text_verbatim": CLAIM_3 if claim_three_text is None else claim_three_text,
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
        "screening_memo": {
            "direction": direction,
            "reason": note
            or (
                "권리 관심이 한 구성(포켓 계량)에 뚜렷함."
                if direction == "clear"
                else "청구항이 통상적 계량 구조의 나열이라 일반 독자에게 줄 안도감이 적음."
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
                # ★ 두 번째 인용은 수확의 입력이다(재정 P-B) — 수확기는 원천 파일이 아니라
                #   접지 스팬을 훑으므로, 접지되지 않은 문단의 수치는 정답지에 오르지 않는다.
                "spec_refs": [
                    {"locator": "[0012]", "quote": SPEC_QUOTE_M5},
                    {"locator": "[0014]", "quote": SPEC_QUOTE_SPEED},
                ],
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


def harvest_ref(offset: int) -> str:
    """수확 대역의 `offset` 번째 임시 ID.

    통합 레인이 `numeric_refs` 와 산식 입력을 **참조 ID로** 적을 수 있는 유일한 좌표다
    (재정 P-B). 대역의 시작은 계약 계산(`harvest_band_start`)이 정하고, 대역 안의 순서는
    수확기의 **등장 순** — 접지 항목 순서 → 그 항목의 `spec_refs` 순서 → 서지 4필드다.
    이 픽스처에서는 `[0014]`(속도)가 `[0013]`(용적)보다 앞선다: 속도 인용이 실린 접지
    항목(M5)이 용적 인용이 실린 항목(M6)보다 앞에 있기 때문이다.
    """
    return f"M{harvest_band_start(decompose_payload()['claims']) + offset}"


HARVEST_SPEED = harvest_ref(0)    # `12 rpm` — M5 의 [0014] 인용
HARVEST_VOLUME = harvest_ref(1)   # `25 cm3` — M6 의 [0013] 인용


def synthesis_payload(*, verdict: str = "go") -> dict:
    """통합 레인 1회분.

    ★ `origin ∈ {quoted, bibliographic}` 인 fact 는 **여기 없다**(재정 P-B). 원문 스팬 수치와
    서지 수치는 접지 직후 전수 기계 수확되므로 레인의 소유가 아니며, 레인이 만들 수 있는
    fact 는 산식(`derived`)과 도면 판독(`figure-sourced`) 둘뿐이다. 레인이 하는 일은 수치를
    옮겨 적는 것이 아니라 **어느 수치를 근거로 삼았는지 참조 ID 로 밝히는 것**이다.
    """
    return {
        "items": [
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
                        {"name": "pocket_volume_cm3", "ref": HARVEST_VOLUME},
                        {"name": "speed_rpm", "ref": HARVEST_SPEED},
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
                "numeric_refs": [HARVEST_VOLUME],
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
                "numeric_refs": [HARVEST_SPEED],
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


def payload_set(
    *,
    direction: str = "clear",
    element_two: str = E2_TEXT,
    note: str | None = None,
    dependency_type: str = "single",
    claim_three_text: str | None = None,
) -> dict:
    return {
        "decompose": decompose_payload(
            direction=direction,
            element_two=element_two,
            note=note,
            dependency_type=dependency_type,
            claim_three_text=claim_three_text,
        ),
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
    # ★ 서지 확장 6필드(재정 P-2 ⓐ). 목록형 값은 전부 원천 서지면의 **바이트 정확
    #   부분문자열**이며, 그 대조는 `read.bibliography` 가 한다.
    "jurisdiction": "XX",
    "kind_code": "A1",
    "assignee": "Example Powders, Inc.",
    "applicants": ["Example Powders, Inc."],
    "inventors": ["Mira Solberg", "Tomas Weill"],
    "dates": {"priority": "2024-05-02", "filing": "2025-04-30", "publication": "2026-02-11"},
    "priority_claims": [
        {"number": "XX2024-0000222", "date": "2024-05-02", "jurisdiction": "XX"}
    ],
    "classifications": {"ipc": ["B65G 65/48"], "cpc": ["B65G 65/48"]},
}


# ---------------------------------------------------------------------------
# 법 리포 — 런이 결박될 **깨끗한 git 커밋**을 가진 소형 리포 (재정 P-U1 · P-8)
# ---------------------------------------------------------------------------
#
# `source.run` 은 진입 시점에 리포의 HEAD 를 핀으로 확정하고, 작업 트리가 더러우면 런을
# 시작하지 않는다. 그래서 시험이 **본 리포의 작업 상태에 좌우되면 안 된다** — 개발 중
# 더러운 트리에서는 런이 거부되는 것이 정상이기 때문이다(같은 이유를
# `test_run_is_pinned_to_engine_commit` 이 이미 적어 두었다: "본 리포의 HEAD 에 기대면
# 시험이 작업 상태에 좌우된다"). 러너가 리포에서 읽는 것은 계약과 `reader/READER-VERSION`
# 뿐이므로 그 둘만 복사해 커밋한 소형 리포를 세우고, 그것을 런의 법으로 준다.

_LAW_REPO: list[str] = []  # 세션 캐시(모듈 전역 1개 — 만드는 비용을 시험마다 치르지 않는다)


def git_law(repo: str, *args: str) -> None:
    """법 리포에 git 명령 하나. 실패하면 그 자리에서 시험을 세운다(조용한 실패 금지)."""
    import subprocess  # noqa: PLC0415

    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        pytest.fail(f"법 리포 git {' '.join(args)} 실패(exit {proc.returncode}): {proc.stderr}")


def make_law_repo(destination: str) -> str:
    """계약 + `reader/READER-VERSION` 만 담은 **깨끗한** git 리포를 세운다."""
    os.makedirs(destination, exist_ok=True)
    shutil.copytree(
        os.path.join(REPO, "contracts"),
        os.path.join(destination, "contracts"),
        ignore=shutil.ignore_patterns("__pycache__"),
        dirs_exist_ok=True,
    )
    os.makedirs(os.path.join(destination, "reader"), exist_ok=True)
    shutil.copy2(
        os.path.join(REPO, "reader", "READER-VERSION"),
        os.path.join(destination, "reader", "READER-VERSION"),
    )
    git_law(destination, "init", "-q")
    git_law(destination, "config", "user.email", "runner@example.com")
    git_law(destination, "config", "user.name", "runner")
    commit_law(destination, "law snapshot")
    return destination


def law_head(repo: str) -> str:
    """법 리포의 현재 HEAD."""
    import subprocess  # noqa: PLC0415

    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        pytest.fail(f"법 리포 HEAD 조회 실패(exit {proc.returncode}): {proc.stderr}")
    return proc.stdout.strip()


def commit_law(repo: str, message: str) -> str:
    """법 리포의 현재 상태를 커밋하고 HEAD 를 돌려준다(`git add -A` 를 쓰지 않는다)."""
    git_law(repo, "add", "contracts", "reader")
    git_law(repo, "commit", "-q", "-m", message)
    return law_head(repo)


def law_repo() -> str:
    """세션 공용 법 리포. 없으면 만들고, 프로세스 종료 시 지운다."""
    import atexit  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    if not _LAW_REPO:
        root = tempfile.mkdtemp(prefix="patent-docent-law-")
        make_law_repo(root)
        _LAW_REPO.append(root)
        atexit.register(shutil.rmtree, root, True)
    return _LAW_REPO[0]


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
        # 법은 **깨끗한 커밋**에서 온다(재정 P-U1) — 위 `law_repo()` 주석 참조.
        repo=repo or law_repo(),
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


class ReplayLaneAdapter(_EngineReplayLaneAdapter):
    """픽스처 트리 전용 재생 어댑터 — **부재한** 입력 지문 반향만 채운다(재정 P-12).

    ★ 이 우회가 필요한 이유. 응답은 요청 지문을 반향해야 하는데(재정 P-12 ②), 합성 픽스처의
    응답은 **요청이 존재하기 전에** 저작되므로 반향할 값을 가질 수 없다. 기록된 실제 런의
    재생에는 이 문제가 없다 — 그때 레인이 반향을 적었기 때문이다. 그러므로 이 메움은 픽스처의
    사정이지 계약의 완화가 아니며, 그래서 엔진이 아니라 여기 산다(`engine/lanes/replay_adapter.py`
    docstring 의 같은 판단).

    ★ 메움의 경계가 이 클래스의 핵심이다 — **키가 없을 때만** 채우고 값이 있으면 손대지 않는다.
    덕분에 "낡은 응답"(지문이 있으나 다른 값) 시나리오는 재생 경로에서도 그대로 거부되며,
    이 우회가 시점 결속 자체를 무력화하지 않는다.
    """

    def dispatch(self, requests):
        for request in requests:
            path = os.path.join(self.root, *request.lane_id.split("/"), "response.json")
            if not os.path.exists(path):
                continue
            raw = json.loads(read_text(path))
            if not isinstance(raw, dict) or "input_digest" in raw:
                continue
            raw["input_digest"] = request.input_digest
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(raw, handle, ensure_ascii=False)
        return super().dispatch(requests)


def shadow_root_for(run_root: str) -> str:
    """이 런의 섀도 원장 루트 — 런 작업장 **옆**의 임시 경로다(런 밖이라는 성질은 보존한다).

    ★ 이 우회가 필요한 이유: 섀도 원장(재정 P-U4)은 런 디렉터리가 아니라 리포 루트에 누적되므로,
    `tmp_path` 로 런을 격리해도 원장만은 격리되지 않는다. 재정 P-U2 가 세운 원칙("표본은
    자기완결 미니 세계 — 재봉인 도구는 테스트 하네스에만")을 그 원장에 적용한 것이 이 함수다.
    실측: 이 격리가 없던 동안 실제 런 0건인 리포 원장에 가공 런 ID 행 1,178 개가 쌓였다.
    """
    return os.path.abspath(os.path.join(run_root, os.pardir, "_shadow"))


def shadow_ledger_for(run_root: str) -> str:
    """`shadow_root_for()` 아래의 원장 파일 경로. 경로 조립은 엔진의 해석기에 맡긴다."""
    return engine_paths.shadow_screening_ledger(shadow_root=shadow_root_for(run_root))


def run_read_stage(
    *, run_root: str, adapter, rules=RULES, shadow_root: str | None = None, **kwargs
):
    """`read_stage.run` 의 **유일한** 테스트 진입점 — 섀도 원장을 임시 경로로 돌린다.

    엔진 함수를 직접 부르지 마라(`read_stage` 의 `run`). `shadow_root` 를 비우고 부르면 생산 원장
    (`<repo>/ledgers/shadow/screening.jsonl`)에 합성 메모가 쌓인다 — 그 재발을
    `test_test_suite_does_not_write_production_shadow_ledger` 가 정적으로도 막는다.
    """
    return read_stage.run(
        run_root=run_root,
        adapter=adapter,
        rules=rules,
        shadow_root=shadow_root or shadow_root_for(run_root),
        **kwargs,
    )


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
    outcome = run_read_stage(run_root=root, adapter=adapter, rules=RULES)
    return root, outcome, adapter


def approval_envelope(
    run_root: str,
    *,
    decision: str = "approved",
    derived_ack=None,
    manual_ack=None,
    drop_decision=None,
    checkpoint: str = "material_approval",
    run_id: str = RUN_ID,
    target_path: str = "10-read/material-spec.json",
    digest: str | None = None,
    owner_quote: str = "이 재료로 CP1 승인한다. 파생 300 cm3 은 계산값으로 이해했다.",
) -> str:
    """승인 봉투 md 를 쓴다. 봉투는 **오케스트레이터가** 쓴다는 규율의 시험용 대역이다.

    `checkpoint` · `run_id` · `target_path` 를 열어 둔 것은 봉투 **신원** 검사(재감수 B-02)의
    시험을 위해서다 — 이 세 값을 바꿔 쓸 수 없으면 신원 위조를 재현할 수 없다.
    """
    paths = RunPaths(run_root)
    absolute = os.path.join(run_root, *target_path.split("/"))
    if digest is None:
        with open(absolute, "rb") as handle:
            digest = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    frontmatter = {
        "schema": "approval-envelope/v0",
        "checkpoint": checkpoint,
        "run_id": run_id,
        "target": {"path": target_path, "digest": digest},
        "decision": decision,
        "owner_quote": owner_quote,
        "quote_provenance": {
            "channel": "session-transcript",
            "located_at": "2026-08-18 세션 · CP1 응답",
        },
        "decided_at": "2026-08-18T04:00:00Z",
        "recorded_by": "orchestrator",
        "manual_verification_ack": [FIGURE_FACT_ID] if manual_ack is None else manual_ack,
        "derived_fact_ack": [DERIVED_FACT_ID] if derived_ack is None else derived_ack,
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


def finding_rules(rows) -> list[str]:
    return [finding.rule for row in rows for finding in row.findings]


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


# ★ 재정 P-5 가 명한 **세 처분의 내용**(2026-08-19 보수 — 감수 C′-2 NEW BLOCKER ③).
#
#   구 시험은 `len(resolutions) == 3` 과 필드의 truthiness 까지만 봤다. 감수 문언 그대로 —
#   *"세 처분을 임의의 다른 세 문장으로 바꿔도 통과하므로 해당 요구를 실제로 반증하지
#   못한다."* 개수는 재정의 내용이 아니다. 그래서 여기에 **무엇을 어떻게 처분했는가**를
#   못 박는다: 파일 단위 · 다각도 각각 · 흐름도 포함.
#
#   ★ 이 상수는 시험이 지어낸 값이 아니다. 아래 `test_p5_resolutions_match_the_ruling_ledger`
#   가 **재정 원장 원문**과 대조하므로, 상수가 원장에서 벗어나면 그 시험이 운다. 원장이
#   상류이고 계약·코드·시험이 하류라는 규율(CLAUDE.md §0)을 시험 층에서 지키는 형태다.
P5_RESOLUTIONS = (
    {"question_needle": "서브도면", "ruling_needle": "파일 단위로 센다"},
    {"question_needle": "다른 각도", "ruling_needle": "각각 센다"},
    {"question_needle": "흐름도", "ruling_needle": "흐름도 포함"},
)
P5_RULING = os.path.join(REPO, "docs", "decisions", "ruling-20260818-03-P1-P11.md")


def test_source_report_records_recompute_basis(tmp_path) -> None:
    """도면별 행과 산정 근거가 없으면 재정 후 원천을 다시 읽어야 한다(재감수 M-04).

    ★ 개명(재정 P-5): `provisional_resolutions` → `resolutions`. 산정식이 **정식 승인**되어
    세 논점이 더는 잠정이 아니므로 이름에서 '잠정'이 빠졌고, 그 대신 재정 좌표
    (`adjudicated_in`)와 채택률 관찰 지표(`observation_metric`)가 함께 실린다. `[가설]` 태그는
    유지된다 — 재정이 명시로 그렇게 정했다(산정식은 승인됐고 수치의 타당성은 관찰 대상이다).

    ★ 2026-08-19 조임 — 세 처분의 **내용**을 명시 비교한다(감수 C′-2 NEW BLOCKER ③).
    개수만 세던 구 형태는 처분을 임의의 다른 세 문장으로 바꿔도 통과했고, 그러면 이 시험이
    반증하는 것은 "리스트가 셋이다"뿐이지 재정이 아니다.
    """
    root, _ = run_source(tmp_path)
    report = load_json(RunPaths(root).source_report)
    exhibit = report["exhibit_candidates"]
    missing = [
        key
        for key in (
            "tag", "unit", "formula", "rationale", "adjudicated_in", "resolutions",
            "observation_metric", "floor",
        )
        if not exhibit.get(key)
    ]
    if missing:
        pytest.fail(f"exhibit_candidates 에 산정 근거가 빠졌다: {missing}")
    if "provisional_resolutions" in exhibit:
        pytest.fail("폐기된 키 `provisional_resolutions` 가 남아 있다(재정 P-5 개명)")
    if exhibit["tag"] != "[가설]":
        pytest.fail(f"산정식 태그 기대 [가설], 실제 {exhibit['tag']}")
    if len(exhibit["resolutions"]) != len(P5_RESOLUTIONS):
        pytest.fail(
            f"처분 {len(P5_RESOLUTIONS)}논점 기대, 실제 {len(exhibit['resolutions'])}건"
        )
    # ★ 내용 대조 — 순서까지 본다(재정이 셋을 나열한 순서가 곧 논점의 순서다).
    for index, (actual, expected) in enumerate(zip(exhibit["resolutions"], P5_RESOLUTIONS)):
        question = str(actual.get("question") or "")
        ruling = str(actual.get("ruling") or "")
        if expected["question_needle"] not in question:
            pytest.fail(
                f"처분 {index + 1} 의 논점이 재정과 다르다 — "
                f"`{expected['question_needle']}` 가 없다: {question!r}"
            )
        if expected["ruling_needle"] not in ruling:
            pytest.fail(
                f"처분 {index + 1} 의 결론이 재정과 다르다 — "
                f"`{expected['ruling_needle']}` 가 없다: {ruling!r}"
            )
        if not str(actual.get("rationale") or "").strip():
            pytest.fail(f"처분 {index + 1} 에 사유가 없다: {actual}")
    if "ruling-20260818-03-P1-P11.md#P-5" not in str(exhibit["adjudicated_in"]):
        pytest.fail(f"재정 좌표가 원장을 가리키지 않는다: {exhibit['adjudicated_in']!r}")
    if exhibit["observation_metric"].get("id") != "exhibit-adoption-ratio":
        pytest.fail(f"채택률 관찰 지표가 실리지 않았다: {exhibit['observation_metric']}")
    for row in report["figures"]:
        for key in ("filename", "bytes", "sha256", "counted_as"):
            if key not in row:
                pytest.fail(f"도면 행에 {key} 가 없다: {row}")
    recomputed = sum(row["counted_as"] for row in report["figures"])
    if recomputed != exhibit["count"]:
        pytest.fail(f"소급 재계산 {recomputed} != 보고값 {exhibit['count']}")


def test_p5_resolutions_match_the_ruling_ledger() -> None:
    """★ 위 시험의 기대 상수가 **원장에서 왔음**을 기계가 확인한다(CLAUDE.md §0 — 원장이 상류).

    이 시험이 없으면 `P5_RESOLUTIONS` 는 시험이 지어낸 값과 구별되지 않는다. 계약과 시험이
    같이 틀리면 둘의 대조는 아무것도 증명하지 못하므로, 대조의 한쪽 끝은 **원장 원문**이어야
    한다. 재정 P-5 원문의 문언은 *"단위=도면 파일(서브도면은 파일 단위·다각도 각각·흐름도
    포함)"* 이다.
    """
    if not os.path.isfile(P5_RULING):
        pytest.fail(f"재정 원장이 없다: {P5_RULING} — 대조의 상류가 사라졌다")
    with open(P5_RULING, encoding="utf-8") as handle:
        ledger = handle.read()
    for needle in ("파일 단위", "다각도 각각", "흐름도 포함"):
        if needle not in ledger:
            pytest.fail(f"재정 원장에 `{needle}` 문언이 없다 — 기대 상수가 원장을 벗어났다")


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
    #    ★ 고친 법은 **커밋한다**(재정 P-U1). 커밋하지 않은 계약 위에서는 런이 시작되지도
    #    않으므로, 여기서의 재커밋은 편의가 아니라 그 규율의 실연이다.
    fake_repo = make_law_repo(os.path.join(str(tmp_path), "fake-repo"))
    sheet_path = os.path.join(fake_repo, "contracts", "format-parameters.yaml")
    with open(sheet_path, encoding="utf-8") as handle:
        sheet = yaml.safe_load(handle)
    sheet["parameters"]["tweet_count"]["value"]["min"] = 3
    with open(sheet_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(sheet, handle, allow_unicode=True, sort_keys=False)
    commit_law(fake_repo, "tweet_count.value.min = 3")

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
            repo=law_repo(),
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
            # 절차 트리는 채워 둔다 — 이 시험이 재는 빈 값은 model 하나다(재정 S4 로 repo_root
            # 도 필수가 되었으므로, 비워 두면 무엇 때문에 던졌는지가 흐려진다).
            repo_root=REPO,
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


def test_every_slice_is_a_verbatim_substring_of_the_source() -> None:
    """슬라이스가 원천의 복사본이 아니면, 지시를 **충실히 따른** 레인이 통과할 수 없다.

    요청서는 레인에게 "요청서에 실린 원천 조각에서 복사하라"고 지시하고 `read.verbatim` 은
    `patent.md` 로 대조한다. 둘이 어긋나면 성실한 레인이 벌을 받고, 그 벌은 레인이 고칠 수
    없다 — 구 구현이 문단을 뽑아 `"\\n\\n".join(...)` 으로 다시 이었고, 원천이 개행을 하나만
    둔 자리에서 바이트가 갈렸다(2026-08-18 실특허 스모크에서 접지 레인이 실제로 만나 회피·보고).

    연속 구간을 그대로 자르면 슬라이스의 어떤 부분문자열도 원천의 부분문자열이므로 이
    함정이 **원리적으로** 사라진다. 이 테스트가 보는 것이 그 성질이다.
    """
    # ★ 합성 픽스처로는 이 성질을 시험할 수 없다. 픽스처는 문단을 빈 줄로 나누므로
    #   구 구현의 `"\n\n".join(...)` 이 원천을 **우연히 그대로 재현**한다(변조 시험에서
    #   공허 통과로 실측됨). 실물 공개공보는 문단 사이에 개행을 하나만 두고 수식 문단
    #   안에서도 그렇다 — 그 배치를 재현해야 비로소 재구성과 복사가 갈린다.
    dense = (
        "## Description\n"
        "[0156] The value can be expressed as:  \n"
        "[00001](-1)Act<7>x2Act<6:3>.  \n"
        "In the above expression, the terms are defined.  \n"
        "[0157] The weight can be expressed as:  \n"
        "[00002](-1)Wdata<5>x2Wdata<4:2>.  \n"
        "In the above expression, the terms are defined.  \n"
        "[0158] A third paragraph closes the block.\n"
    )
    # 불변식은 두 층이다.
    #   ① 모든 슬라이스: **줄 단위**로 원천의 부분문자열이다. 흩어진 조각을 모은 슬라이스
    #      (도면 캡션)는 연속 구간일 수 없으므로 여기까지가 보장의 한계다.
    #   ② 본문 문단 슬라이스: **연속 구간 전체**가 원천의 부분문자열이다. 레인이 문단을
    #      걸쳐 인용하는 것이 정상 사용이므로 이 슬라이스만은 복사본이어야 한다.
    contiguous_required = {"description-paragraphs", "claims-section"}
    for source_text in (SOURCE, dense):
        view = ReadView(source_text, RULES)
        for task in ("decompose", "ground-independent", "ground-dependent", "synthesize"):
            for name, text in view.slices_for(task).items():
                if not text:
                    continue
                for line in text.split("\n"):
                    if not line.strip():
                        continue
                    assert line in source_text, (
                        f"{task} 의 슬라이스 `{name}` 에 원천에 없는 줄이 있다: {line[:80]!r}"
                    )
                if name in contiguous_required:
                    assert text in source_text, (
                        f"{task} 의 슬라이스 `{name}` 이 원천의 **연속** 부분문자열이 아니다 — "
                        "레인이 문단을 걸쳐 복사한 인용은 read.verbatim 을 통과할 수 없다"
                    )

    # 수식 라벨(`[00001]`)을 문단 시작으로 오인하면 문단이 한가운데서 쪼개진다.
    locators = [paragraph.locator for paragraph in ReadView(dense, RULES).paragraphs()]
    assert locators == ["[0156]", "[0157]", "[0158]"], (
        f"수식 라벨이 문단 로케이터로 오인되었다: {locators}"
    )


def test_figure_caption_ids_satisfy_the_schema_pattern() -> None:
    """캡션을 인식하는 규칙과 그 캡션에 id 를 주는 규칙이 다른 문자 집합을 전제하면, 레인이 쓸 수 없는 도면이 생긴다.

    ★ 2026-08-18 실측. `caption_line` 은 `FIGS. 7 and 8` 을 캡션으로 받는데 그 번호를 그대로
    id 로 쓰면 `FIG-7 and 8` 이 되어 스키마의 `figure_id` 패턴을 통과하지 못한다. 접지 레인이
    그런 도면 2건을 **쓸 수 없어 회피**했다 — 계약의 불일치가 산출물의 축소로 새는 자리다.
    """
    schema = json.load(
        open(
            os.path.join(REPO, "reader", "schemas", "material-spec.schema.json"),
            encoding="utf-8",
        )
    )
    pattern = re.compile(schema["$defs"]["figure_id"]["pattern"])
    sample = (
        "## Brief description of the drawings\n\n"
        "FIG. **1** illustrates a thing.\n"
        "FIGS. **7** and **8** illustrate other things.\n"
        "FIGS. **10**-**11** illustrate more things.\n"
    )
    captions = ReadView(sample, RULES).figure_captions()
    assert captions, "표본에서 캡션을 하나도 찾지 못했다 — 이 테스트가 공허해진다"
    for caption in captions:
        assert pattern.fullmatch(caption.figure_id), (
            f"캡션 id `{caption.figure_id}` 가 스키마의 figure_id 패턴을 통과하지 못한다"
        )
    ids = {caption.figure_id for caption in captions}
    assert "FIG-7-8" in ids, f"`and` 연결어가 하이픈으로 정규화되지 않았다: {sorted(ids)}"


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


# --- 조립 시 항목 ID 재번호(재감수 B-01) ------------------------------------
# 위 대역 시험은 **요청 지시문**만 본다. 대역이 아무리 잘 나뉘어도 조립본이 그것을 이어
# 붙이기만 하면 `M1..Mn` 연속이 깨지고 동결이 불가능해진다 — 아래 4건이 그 자리를 본다.

BAND_OFFSETS = {
    # 분해 레인도 0 이 아닌 자리에서 센다. 0 으로 두면 분해 항목의 원본 ID 와 최종 ID 가
    # 우연히 같아져, `grounding.component` 재작성을 통째로 빼도 시험이 통과한다(변조 시험 M3).
    "decompose": 100,
    "ground-independent": 1000,
    "ground-dependent": 2000,
    "synthesize": 3000,
}


def _remap_ids(payloads: dict, table: dict) -> dict:
    """레인 payload 전량의 항목 ID·참조를 `table` 로 바꿔 쓴다(시험용 대역 살포).

    엔진의 재작성과 **반대 방향**이며 전역 표 하나만 쓴다 — 같은 코드를 두 번 쓰면 시험이
    구현의 거울이 되어 아무것도 반증하지 못한다.
    """
    out = copy.deepcopy(payloads)

    def ref(value):
        return table.get(value, value) if isinstance(value, str) else value

    def walk(elements) -> None:
        for element in elements or []:
            element["material_id"] = ref(element.get("material_id"))
            walk(element.get("children") or [])

    for payload in out.values():
        for item in payload.get("items") or []:
            item["id"] = ref(item.get("id"))
            if item.get("superseded_by") is not None:
                item["superseded_by"] = ref(item["superseded_by"])
            if item.get("kind") == "grounding":
                item["component"] = ref(item.get("component"))
            elif item.get("kind") == "implication":
                item["derived_from"] = [ref(entry) for entry in item.get("derived_from") or []]
            elif item.get("kind") == "fact":
                for entry in (item.get("derivation") or {}).get("inputs") or []:
                    if "ref" in entry:
                        entry["ref"] = ref(entry["ref"])
        claims = payload.get("claims") or {}
        for claim in claims.get("independent") or []:
            walk(claim.get("elements") or [])
        for claim in claims.get("dependents") or []:
            for addition in claim.get("additions") or []:
                addition["material_id"] = ref(addition.get("material_id"))
        for interest in claims.get("applicant_interest") or []:
            interest["material_id"] = ref(interest.get("material_id"))
    return out


def banded_payload_set() -> dict:
    """레인이 1000 폭 대역을 받아 쓴 판. 기본 픽스처는 연속 번호라 재번호를 시험하지 못한다."""
    payloads = payload_set()
    table = {
        item["id"]: f"M{int(item['id'][1:]) + offset}"
        for task, offset in BAND_OFFSETS.items()
        for item in payloads[task]["items"]
    }
    remapped = _remap_ids(payloads, table)
    # ★ 수확 대역은 레인 대역 **뒤**에 계산되므로(재정 P-B · `harvest_band_start`), 레인
    #   대역이 옮겨가면 수확 대역도 함께 옮겨간다. 통합 레인의 참조를 그대로 두면 그 참조는
    #   유령이 되고, 이 시험은 재번호가 아니라 유령 참조를 보게 된다.
    shifted = {
        HARVEST_SPEED: f"M{harvest_band_start(remapped['decompose']['claims'])}",
        HARVEST_VOLUME: f"M{harvest_band_start(remapped['decompose']['claims']) + 1}",
    }
    for item in remapped["synthesize"]["items"]:
        if isinstance(item.get("numeric_refs"), list):
            item["numeric_refs"] = [shifted.get(ref, ref) for ref in item["numeric_refs"]]
        for entry in (item.get("derivation") or {}).get("inputs") or []:
            entry["ref"] = shifted.get(entry.get("ref"), entry.get("ref"))
    return remapped


def assemble_from(payloads: dict) -> dict:
    """레인 payload 4종 → 조립본. 러너를 통과하지 않고 조립기만 부른다."""
    return read_stage.assemble_spec(
        run_meta={
            "run_id": RUN_ID,
            "patent": copy.deepcopy(PATENT_META),
            "engine": {"commit": "test"},
        },
        decompose=payloads["decompose"],
        groundings=[payloads["ground-independent"], payloads["ground-dependent"]],
        synthesis=payloads["synthesize"],
        read_runs=("read-a", "read-b"),
        repo=REPO,
        source_digest="sha256:" + hashlib.sha256(SOURCE.encode("utf-8")).hexdigest(),
    )


def item_fingerprint(item):
    """항목의 신원. **ID 파생값을 쓰지 않는다** — ID 는 재번호가 바꾸는 바로 그 값이다."""
    if item is None:
        return None
    return (
        item.get("kind"),
        item.get("label_en")
        or item.get("statement_en")
        or item.get("what_it_shows_en")
        or item.get("background_problem")
        or "",
        item.get("text_verbatim", ""),
        item.get("value_raw", ""),
        " / ".join(str(entry.get("quote", "")) for entry in item.get("spec_refs") or []),
    )


def reference_sites(claims: dict, items: list) -> list[tuple[str, str]]:
    """참조 자리 → `(자리 이름, 참조값)`. 자리 이름은 ID 가 아니라 **위치**로 짓는다."""
    sites: list[tuple[str, str]] = []

    def walk(elements, prefix) -> None:
        for position, element in enumerate(elements or []):
            sites.append((f"{prefix}/e{position}.material_id", element.get("material_id")))
            walk(element.get("children") or [], f"{prefix}/e{position}")

    for position, claim in enumerate(claims.get("independent") or []):
        walk(claim.get("elements") or [], f"independent[{position}]")
    for position, claim in enumerate(claims.get("dependents") or []):
        for index, addition in enumerate(claim.get("additions") or []):
            sites.append(
                (f"dependents[{position}].additions[{index}].material_id",
                 addition.get("material_id"))
            )
    for position, interest in enumerate(claims.get("applicant_interest") or []):
        sites.append(
            (f"applicant_interest[{position}].material_id", interest.get("material_id"))
        )
    for position, item in enumerate(items):
        if item.get("superseded_by") is not None:
            sites.append((f"items[{position}].superseded_by", item["superseded_by"]))
        kind = item.get("kind")
        if kind == "grounding":
            sites.append((f"items[{position}].component", item.get("component")))
        elif kind == "implication":
            for index, entry in enumerate(item.get("derived_from") or []):
                sites.append((f"items[{position}].derived_from[{index}]", entry))
        elif kind == "fact":
            for index, entry in enumerate((item.get("derivation") or {}).get("inputs") or []):
                if "ref" in entry:
                    sites.append(
                        (f"items[{position}].derivation.inputs[{index}].ref", entry["ref"])
                    )
    return sites


def test_assembled_spec_has_contiguous_item_ids() -> None:
    """대역을 이어 붙이기만 하면 결번이 남고 `lifecycle.id-contiguous` 가 **정상 산출을** 막는다."""
    payloads = banded_payload_set()
    raw = [
        item["id"]
        for task in ("decompose", "ground-independent", "ground-dependent", "synthesize")
        for item in payloads[task]["items"]
    ]
    numbers = sorted(int(entry[1:]) for entry in raw)
    if numbers == list(range(1, len(numbers) + 1)):
        pytest.fail("대역 살포가 결번을 만들지 않았다 — 이 시험이 공허해진다")

    spec = assemble_from(payloads)
    expected = [f"M{index}" for index in range(1, len(spec["items"]) + 1)]
    actual = [item["id"] for item in spec["items"]]
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        pytest.fail(f"조립본 ID 가 M1..M{len(expected)} 연속이 아니다 — 결번 {missing[:8]}")


def test_assembly_survives_freeze_id_monotonic(tmp_path) -> None:
    """조립본을 동결에 **실제로 넣지 않으면** 대역·연속성 충돌이 시험을 통과한 채 남는다.

    ★ 재감수 B-01 의 자리다. 기존 대역 시험은 요청 지시문만 보았고, 조립과 동결을 한 번도
    거치지 않아 "정상 READ 산출을 동결할 수 없다"는 결함을 놓쳤다.
    """
    payloads = banded_payload_set()
    root, outcome, _ = run_read(
        tmp_path, payloads_by_run={"read-a": payloads, "read-b": copy.deepcopy(payloads)}
    )
    if outcome["status"] != "ok":
        pytest.fail(f"read status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")

    approval_envelope(root)
    frozen = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    monotonic = [row for row in frozen["rows"] if row.check_id == "freeze.id-monotonic"]
    if not monotonic:
        pytest.fail(f"freeze.id-monotonic 이 돌지 않았다: {[row.check_id for row in frozen['rows']]}")
    if monotonic[0].status != "pass":
        pytest.fail(f"동결 ID 검사가 실패했다: {fail_rows(frozen['rows'])}")
    if frozen["status"] != "ok":
        pytest.fail(f"freeze status 기대 ok, 실제 {frozen['status']} — {fail_rows(frozen['rows'])}")


def test_renumbering_preserves_reference_targets() -> None:
    """참조 재작성을 빠뜨리면 번호만 남고 **가리키는 대상이 조용히 바뀐다** — 유령 참조다."""
    payloads = banded_payload_set()
    before_items = [
        item
        for task in ("decompose", "ground-independent", "ground-dependent", "synthesize")
        for item in payloads[task]["items"]
    ]
    before_index = {item["id"]: item for item in before_items}
    before = reference_sites(payloads["decompose"]["claims"], before_items)

    spec = assemble_from(payloads)
    after_index = {item["id"]: item for item in spec["items"]}
    after = reference_sites(spec["claims"], spec["items"])

    if not before:
        pytest.fail("픽스처에 참조 자리가 하나도 없다 — 이 시험이 공허해진다")
    if len(before) != len(after):
        pytest.fail(f"참조 자리 수가 달라졌다: 전 {len(before)} / 후 {len(after)}")

    drifted: list[str] = []
    for (old_locus, old_ref), (new_locus, new_ref) in zip(before, after):
        if old_locus != new_locus:
            drifted.append(f"자리 이름 불일치: {old_locus} vs {new_locus}")
            continue
        old_target = item_fingerprint(before_index.get(old_ref))
        new_target = item_fingerprint(after_index.get(new_ref))
        if old_target != new_target:
            drifted.append(f"{old_locus}: {old_ref} → {new_ref} 가 다른 대상을 가리킨다")
    if drifted:
        pytest.fail(f"재번호가 참조 대상을 옮겼다: {drifted}")


def test_two_lanes_reusing_one_id_do_not_merge() -> None:
    """같은 라벨을 쓴 두 레인의 항목이 하나로 합쳐지면 항목 하나가 **소리 없이 사라진다**."""
    payloads = banded_payload_set()
    collided = payloads["ground-independent"]["items"][0]["id"]
    dependent = payloads["ground-dependent"]["items"][0]
    dependent["id"] = collided  # 두 접지 레인이 같은 번호를 발번한 판

    spec = assemble_from(payloads)
    expected_count = sum(len(payloads[task]["items"]) for task in BAND_OFFSETS)
    if len(spec["items"]) != expected_count:
        pytest.fail(f"항목 수 기대 {expected_count}, 실제 {len(spec['items'])} — 하나가 합쳐졌다")

    ids = [item["id"] for item in spec["items"]]
    if len(set(ids)) != len(ids):
        pytest.fail(f"조립본에 중복 ID 가 있다: {sorted(ids)}")

    fingerprints = [item_fingerprint(item) for item in spec["items"]]
    for payload_key in ("ground-independent", "ground-dependent"):
        wanted = item_fingerprint(payloads[payload_key]["items"][0])
        if wanted not in fingerprints:
            pytest.fail(f"{payload_key} 의 접지 항목이 조립본에서 사라졌다: {wanted}")

    _, id_map = read_stage.renumber_items(
        read_stage.lane_payloads(
            payloads["decompose"],
            [payloads["ground-independent"], payloads["ground-dependent"]],
            payloads["synthesize"],
        )
    )
    finals = {
        lane: mapping[collided] for lane, mapping in id_map.items() if collided in mapping
    }
    if len(finals) != 2 or len(set(finals.values())) != 2:
        pytest.fail(f"두 레인의 같은 원본 ID 가 서로 다른 최종 ID 를 받지 않았다: {finals}")


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
        run_read_stage(run_root=root, adapter=adapter, rules=RULES)
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
    #
    # ★ 구성이 셋으로 늘었다. 앞은 **진입 지문 검사**(재정 P-C — 환경이 서 있는가), 가운데는
    #   이식 단위의 결정론 검사 전종, 뒤는 **엔진 소관 검사 전종**. 세 층은 보는 대상이
    #   다르므로 한 층만 세면 나머지가 조용히 빠진다.
    #
    # ★ 2026-08-31 — 꼬리를 리터럴에서 **등재부 참조**로 바꿨다. 머리 문장이 *"검사가 늘면 이
    #   시험이 그 사실을 따라간다"* 고 적는데 꼬리만은 `"read.lane-log-shape"` 를 손으로 적고
    #   있었고, 그래서 재정 2026-08-31 Q1 이 검사를 하나 늘리자 이 시험이 **따라가지 못하고
    #   깨졌다**. 선언과 실물이 갈린 자리이며, 이제 둘 다 `ENGINE_READ_CHECK_IDS` 를 본다.
    produced = [row.check_id for row in outcome["rows"]]
    expected = [
        "read.input-digest",
        *READ_CHECK_IDS,
        *read_stage.ENGINE_READ_CHECK_IDS,
    ]
    if produced != expected:
        pytest.fail(f"검사 행 기대 {expected}, 실제 {produced}")


def test_entry_digest_mismatch_is_environment_error(tmp_path) -> None:
    """지문 불일치가 재시도되면 환경 오류가 품질 결함으로 오분류된다(재정 P-C).

    ★ 판정 층이 바뀌었다. 구 구현은 원천 변조를 `read.source-digest` **판정 행**으로 보고
    `halt` 했다 — 그러면 그것이 재료의 품질 문제로 읽히고 재시도·수정 루프의 대상이 된다.
    재정 P-C 는 이것을 **환경 오류**로 못 박았다: 즉시 중단이며 판정 행조차 돌려주지 않는다.
    """
    root, _ = run_source(tmp_path)
    paths = RunPaths(root)
    with open(paths.patent_md, "a", encoding="utf-8") as handle:
        handle.write("\n[0015] Silently appended after the digest was pinned.\n")
    lanes_root = write_lane_responses(
        root, payloads_by_run={"read-a": payload_set(), "read-b": payload_set()}
    )
    with pytest.raises(StageEnvironmentError) as excinfo:
        run_read_stage(run_root=root, adapter=ReplayLaneAdapter(lanes_root), rules=RULES)

    diagnosis = str(excinfo.value)
    # 진단이 "어긋났다"만 말하면 사람이 다시 찾아야 한다 — **어긋난 자리의 경로**와
    # 기대·실측이 함께 실린다(재정 P-C 의 "즉시 중단 + 진단").
    for needle in ("00-source/patent.sha256", "run.yaml#patent.source_sha256", "실측", "기대"):
        if needle not in diagnosis:
            pytest.fail(f"진단에 {needle} 이 없다: {diagnosis}")
    if "환경 오류" not in diagnosis:
        pytest.fail(f"진단이 환경 오류임을 밝히지 않는다: {diagnosis}")
    if os.path.exists(paths.material_spec_json):
        pytest.fail("다이제스트 불일치인데 재료 명세가 쓰였다")

    # 대조군 — 변조하지 않은 런은 같은 자리를 통과한다(과잉 제약 배제).
    clean_root, clean_outcome, _ = run_read(tmp_path.joinpath("clean"))
    if clean_outcome["status"] != "ok":
        pytest.fail(f"무변조 런이 진입 검사에서 걸렸다: {clean_outcome['status']}")
    _ = clean_root


def test_drop_signal_emitted_at_both_stages(tmp_path) -> None:
    """1단만 나와도 통과하면 D4 2단 신호가 실효 없다.

    ★ 1단의 **형태**가 바뀌었다(재정 P-A). 조기 신호는 상신하는 `drop_signal` 이 아니라
    상신 없는 **맹검 스크리닝 메모**이며, 확정 재정의 자리는 CP1 한 곳이다. 2단 구조 자체는
    남는다 — 사라진 것은 조기 단계의 **구속력**이지 관찰이 아니다.
    """
    root, _, _ = run_read(tmp_path)
    text = read_text(RunPaths(root).drop_signal_md)
    for needle in (
        "맹검 스크리닝 메모",
        "상신 없음 · 진행 계속",
        "포지셔닝 확정 후",
        "`read-a`",
        "`read-b`",
    ):
        if needle not in text:
            pytest.fail(f"drop-signal.md 에 {needle} 이 없다")


def test_screening_memos_recorded_for_both_runs(tmp_path) -> None:
    """메모가 1건이면 두 관찰의 일치/불일치 신호가 소멸한다(재정 P-A · P-U4).

    ★ 폐기된 것을 함께 시험한다 — 조기 `drop-proposed` 로 접지 전에 멈추던 경로다. 재정 P-A 가
    그 escalate 를 폐지했으므로, 우려 방향의 메모가 나와도 러너는 **멈추지 않고 끝까지 간다.**
    """
    root, _ = run_source(tmp_path)
    payloads = {
        # 두 실행이 서로 다른 방향을 적은 판 — 갈림 자체가 신호다(재정 P-U4).
        "read-a": payload_set(direction="clear"),
        "read-b": payload_set(direction="concern", note="계량 구조가 통상적이라 훅이 약함."),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = run_read_stage(run_root=root, adapter=adapter, rules=RULES)

    # ① 우려 메모가 런을 세우지 않는다(재정 P-A — 확정 재정의 자리는 CP1 하나다).
    if outcome["status"] != "ok":
        pytest.fail(f"메모가 런을 세웠다: {outcome['status']} — {fail_rows(outcome['rows'])}")
    tasks = adapter.tasks_dispatched()
    if "synthesize" not in tasks:
        pytest.fail(f"우려 메모에 접지·통합이 멈췄다: {tasks}")

    # ② 두 건이 **각자** 기록된다.
    memos = outcome["convergence"]["screening_memos"]
    by_run = {memo["read_run"]: memo for memo in memos}
    if sorted(by_run) != ["read-a", "read-b"]:
        pytest.fail(f"메모 2건 기대(read-a·read-b), 실제 {memos}")
    if by_run["read-a"]["direction"] != "clear" or by_run["read-b"]["direction"] != "concern":
        pytest.fail(f"두 관찰의 방향이 보존되지 않았다: {memos}")
    if not by_run["read-b"]["note"]:
        pytest.fail("근거 요지가 비었다 — 방향만 남으면 판단 기록이 아니다")

    # ③ 섀도 원장(런 밖·계약면 밖)에 한 행으로 축적된다(재정 P-U4).
    #    ★ 보는 자리는 **격리 원장**이다 — 생산 원장을 보면 이 시험이 그 파일을 오염시킨다
    #    (재정 P-U2). 원장 기입 자체는 여기서 그대로 반증된다.
    ledger = shadow_ledger_for(root)
    if not os.path.exists(ledger):
        pytest.fail(f"섀도 원장이 없다: {ledger}")
    rows = [json.loads(line) for line in read_text(ledger).splitlines() if line.strip()]
    ours = [row for row in rows if row.get("run_id") == RUN_ID]
    if not ours or len(ours[-1]["memos"]) != 2:
        pytest.fail(f"원장 행에 메모 2건이 실리지 않았다: {ours[-1:] or '(행 없음)'}")

    # ④ CP1 판독본에 **둘 다 병기**된다 — 한 건으로 합치면 신호가 소멸한다.
    rendered = read_text(RunPaths(root).material_spec_md)
    section = rendered.split("## 11. ★ 맹검 스크리닝 메모")[1].split("## 12.")[0]
    for needle in ("read-a", "read-b", "clear", "concern"):
        if needle not in section:
            pytest.fail(f"CP1 메모 절에 {needle} 이 없다")


def _ledger_fingerprint(path: str):
    """원장 파일의 상태 지문 — 미존재는 `None`, 존재하면 (바이트 수, sha256)."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as handle:
        blob = handle.read()
    return len(blob), hashlib.sha256(blob).hexdigest()


def _direct_engine_ledger_calls() -> list[str]:
    """`shadow_root` 없이 엔진의 원장 기입 경로를 부르는 테스트 코드 자리(파일:행)."""
    guarded = {("read_stage", "run"), ("read_stage", "append_screening_ledger")}
    offenders: list[str] = []
    for module in sorted(glob.glob(os.path.join(REPO, "tests", "test_*.py"))):
        tree = ast.parse(read_text(module))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            owner = node.func.value
            if not isinstance(owner, ast.Name):
                continue
            if (owner.id, node.func.attr) not in guarded:
                continue
            if any(keyword.arg == "shadow_root" for keyword in node.keywords):
                continue
            offenders.append(
                f"{os.path.relpath(module, REPO)}:{node.lineno} "
                f"({owner.id}.{node.func.attr})"
            )
    return offenders


def test_test_suite_does_not_write_production_shadow_ledger(tmp_path) -> None:
    """이 시험이 없으면 합성 픽스처의 메모가 생산 섀도 원장에 축적된다(재정 P-U4 · P-U2).

    실측 결함(2026-08-18): 실제 런 0건인 리포의 `ledgers/shadow/screening.jsonl` 에 가공 런 ID
    `example-xx1111111a1-rotary-feeder` 행이 1,178 개 쌓여 있었다. 원장의 값은 무편집 축적에
    있고(historian 스크리닝의 사전 훈련 데이터 — D4), 합성 잡음이 섞인 순간 그 값이 사라진다.
    재정 P-U2 가 "표본은 자기완결 미니 세계"라고 못 박은 원칙을 재정 P-U4 의 원장에 적용한다.
    """
    # ① 생산 기본값은 그대로다 — 격리가 생산 자리를 옮긴 것이 아님을 함께 못 박는다(재정 P-U4).
    production = engine_paths.shadow_screening_ledger()
    expected = os.path.join(REPO, "ledgers", "shadow", "screening.jsonl")
    if production != expected:
        pytest.fail(f"생산 원장 자리가 옮겨졌다: {production!r} (기대 {expected!r})")

    before = _ledger_fingerprint(production)

    # ② 원장을 실제로 기입하는 통주를 돌린다 — 기입이 없으면 이 시험이 공허해진다.
    root, outcome, _ = run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"통주가 ok 를 내지 않았다: {outcome['status']}")

    # ③ 그 사이 생산 원장의 바이트는 변하지 않았다.
    after = _ledger_fingerprint(production)
    if after != before:
        pytest.fail(f"생산 섀도 원장이 변했다: {before} → {after} ({production})")

    # ③' 대신 격리 원장에 쌓였다 — 이 확인이 없으면 "기입을 통째로 막아" 통과하는 길이 열린다.
    isolated = shadow_ledger_for(root)
    rows = [
        json.loads(line)
        for line in (read_text(isolated) if os.path.exists(isolated) else "").splitlines()
        if line.strip()
    ]
    if not [row for row in rows if row.get("run_id") == RUN_ID]:
        pytest.fail(f"격리 원장에 이 런의 행이 없다 — 기입 경로가 죽었다: {isolated}")

    # ④ 정적 관문 — 어떤 테스트 모듈도 `shadow_root` 없이 엔진 기입 경로를 부르지 않는다.
    #    ②③ 은 이 시험이 부른 통주 하나만 보므로, 다음 사람이 다른 자리에 같은 구멍을 내는 것은
    #    이 검사만 막을 수 있다.
    offenders = _direct_engine_ledger_calls()
    if offenders:
        pytest.fail(
            "shadow_root 없이 엔진 원장 기입 경로를 부른다(테스트는 run_read_stage 를 쓴다): "
            + ", ".join(offenders)
        )


def test_screening_memo_is_withheld_from_synthesis_prompt(tmp_path) -> None:
    """메모가 통합 레인에 새면 앵커링 방지가 실패한다 — 두 판단의 독립성이 조용히 사라진다(재정 P-A)."""
    marker = "이 문장이 통합 레인에 새면 앵커링 방지가 무너진다."
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(direction="concern", note=marker),
        "read-b": payload_set(direction="concern", note=marker),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = run_read_stage(run_root=root, adapter=adapter, rules=RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")

    synthesis_requests = [
        request for request in adapter.dispatched if request.task == "synthesize"
    ]
    if not synthesis_requests:
        pytest.fail("통합 요청이 없다 — 이 시험이 공허해진다")
    for request in synthesis_requests:
        haystack = request.instructions + json.dumps(request.slices, ensure_ascii=False)
        if marker in haystack or "screening_memo" in haystack:
            pytest.fail(f"{request.lane_id} 지시문에 맹검 메모가 실렸다")

    # 대조군 — 메모는 **어딘가에는** 남아야 한다(비공개가 폐기가 되면 축적물이 사라진다).
    if marker not in json.dumps(outcome["convergence"]["screening_memos"], ensure_ascii=False):
        pytest.fail("메모가 보고서에서도 사라졌다 — 비공개가 아니라 폐기다")


def test_convergence_failure_escalates_after_one_retry(tmp_path) -> None:
    """무한 재시도되면 불안정 신호가 은폐된다(수렴 미달 = 절차 신호).

    구 표본(`dependency_type="multiple-or"`)은 read-b 자체의 **규약 위반**이다. 재정 T16
    부속 3 이 원인 검사(`read.dependency-parse`)를 수렴 앞에 세웠으므로 이제 원인이 먼저
    잡히고 수렴은 보류된다. 이 시험이 재려던 것은 **수렴 미달의 재시도·상신**이므로 표본을
    두 실행이 각자 성하지만 서로 갈리는 것으로 바꾼다.
    """
    root, _ = run_source(tmp_path)
    payloads = {
        # ★ 갈라놓는 축은 `dependent-set`(exact-match · 임계 1.0)이다. element 문언을 가르던
        #   구 표본은 재정 P-3 이후 **상신 트리거**라 판정 행을 실패시키지 않는다.
        "read-a": payload_set(),
        "read-b": payload_set(claim_three_text=CLAIM_3.rstrip(".")),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = run_read_stage(run_root=root, adapter=adapter, rules=RULES)
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
    """결함 목록을 되돌려 주지 않으면 재시도가 같은 오류를 재생산한다.

    구 규약 위반 표본은 T16 부속 3 에 따라 원인 검사에서 멎으므로, 각 실행은 성하지만 서로
    갈리는 표본으로 수렴 결함의 되먹임을 잰다.
    """
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(),
        "read-b": payload_set(claim_three_text=CLAIM_3.rstrip(".")),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    run_read_stage(run_root=root, adapter=adapter, rules=RULES)
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
    if payload["manual_verification_required"][0]["material_id"] != FIGURE_FACT_ID:
        pytest.fail("도면 유래 수치가 사람 검증 목록에 오르지 않았다")
    if payload["grounding_exceptions"][0]["material_id"] != "M6":
        pytest.fail("접지 예외가 목록에 오르지 않았다")
    # 신설 6키(재정 P-1·P-3·P-4·P-A·P-B·P-U4)가 실제로 채워지는지 본다 — 계약을 만족하는
    # 빈 껍데기는 계약을 만족하되 아무것도 보고하지 않는다.
    if payload["phase"] != "full":
        pytest.fail(f"phase 기대 full, 실제 {payload['phase']!r}")
    selection = payload["canonical_selection"]
    if selection["rule"] != "declaration-order" or selection["content_blind"] is not True:
        pytest.fail(f"정본 지정 규칙이 계약과 다르다: {selection}")
    if not payload["convergence_report"]["axes"]:
        pytest.fail("독해 프로파일의 축이 비었다")
    if payload["numeric_inventory"]["total"] != len(HARVESTED_LABELS):
        pytest.fail(f"전수 수확 카운트가 다르다: {payload['numeric_inventory']}")
    if len(payload["screening_memos"]) != 2:
        pytest.fail(f"맹검 메모 2건 기대, 실제 {payload['screening_memos']}")
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
    # 산식과 **입력 항목의 원천 스팬**이 나란히 실려야 한다 — 수확본을 입력으로 쓰므로
    # 그 스팬은 접지 인용 전문이다(재정 P-B).
    for needle in ("pocket_volume_cm3 * speed_rpm", "M7", "M8", SPEC_QUOTE_M6):
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
    if FIGURE_FACT_ID not in manual_section:
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


def test_stale_approval_digest_is_halt_not_environment_error(tmp_path) -> None:
    """승인 후 재료가 조용히 바뀌어도 통과하면 해시 결속이 장식이다(재정 R8).

    ★ 판정 자리를 **출구로 되돌렸다**(구명 `test_freeze_rejects_stale_target_digest`).
    한동안 진입 지문 검사(재정 P-C)가 같은 불일치를 먼저 잡아 `StageEnvironmentError` 로
    중단했고, 그 결과 출구 규칙 `approval.target-digest` 에 제어가 닿지 않았다(도달 불능).

    두 실패는 성질이 다르다. 진입 지문은 **세계가 어긋난 것**(환경 오류)이고, 봉투
    `target.digest` 는 세계가 멀쩡한 채 **승인이 실효한 것**이다 — 재료가 개정되면 봉투는
    자동 실효하는 것이 설계이며(R8), 그때 필요한 것은 진단이 아니라 **재승인**이다. 진입이
    그것을 삼키면 재승인 경로가 판정문에서 사라진다.

    쌍이 되는 반증 = `test_entry_digest_mismatch_is_environment_error`(원천 지문 불일치는
    여전히 환경 오류다) · `test_freeze_entry_digest_mismatch_is_environment_error`.
    """
    root, _, _ = run_read(tmp_path)
    approval_envelope(root, digest="sha256:" + "0" * 64)
    try:
        outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    except StageEnvironmentError as exc:
        pytest.fail(f"봉투 실효가 환경 오류로 처리됐다 — 이것은 재승인 사건이다: {exc}")

    rules_hit = finding_rules(outcome["rows"])
    if "approval.target-digest" not in rules_hit:
        pytest.fail(f"출구 판정 행에 결속 실패가 없다: {fail_rows(outcome['rows'])}")
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    # 판정문이 **무엇을 하라**를 말해야 한다 — "다시 승인받아라"(재정 R8).
    message = " ".join(fail_rows(outcome["rows"]))
    if "재승인" not in message:
        pytest.fail(f"판정문에 재승인 경로가 없다: {message}")
    if os.path.exists(RunPaths(root).frozen_spec(1)):
        pytest.fail("해시가 어긋났는데 동결본이 쓰였다")

    # 대조군 — 실제 해시를 적은 봉투는 같은 자리를 통과한다.
    approval_envelope(root)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"정상 봉투가 거부됐다: {fail_rows(outcome['rows'])}")


def test_freeze_entry_digest_mismatch_is_environment_error(tmp_path) -> None:
    """봉투 결속을 진입에서 뺐다고 진입 검사까지 무력해지면 P-C 가 약해진다.

    freeze 의 진입 검사는 **선언된 입력**을 계속 본다 — 동결하려는 재료가 이 런의 원천 위에서
    만들어졌는가. 그 불일치는 환경 오류이며 판정 행이 아니다(재정 P-C). 위 시험과 이 시험이
    함께 서는 것이 이번 처분의 요점이다: 뺀 것은 봉투 결속 한 조각뿐이다.
    """
    root, _, _ = run_read(tmp_path)
    approval_envelope(root)
    paths = RunPaths(root)
    with open(paths.patent_sha256, "w", encoding="utf-8") as handle:
        handle.write("sha256:" + "0" * 64 + "\n")

    with pytest.raises(StageEnvironmentError) as excinfo:
        freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    diagnosis = str(excinfo.value)
    for needle in ("환경 오류", "material-spec.json#patent.source_digest", "실측", "기대"):
        if needle not in diagnosis:
            pytest.fail(f"진단에 {needle} 이 없다: {diagnosis}")
    if os.path.exists(paths.frozen_spec(1)):
        pytest.fail("원천 지문이 어긋났는데 동결본이 쓰였다")


# --- 봉투 신원(재감수 B-02) -------------------------------------------------
# 아래 5건은 한 덩어리다. 앞 4건은 "봉투가 어느 관문의 · 어느 런의 · 무엇에 대한 승인인가"를
# 위조한 경우이고, 마지막 1건은 그 4건이 과잉 제약이 아님을 잡아 두는 반증이다.


def test_freeze_rejects_ship_approval_envelope(tmp_path) -> None:
    """이것이 없으면 CP2 봉투로 CP1 을 통과할 수 있다 — 관문 무력화지 오보가 아니다."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root, checkpoint="ship_approval")
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if "approval.checkpoint" not in finding_rules(outcome["rows"]):
        pytest.fail(f"ship_approval 봉투가 체크포인트 대조를 통과했다: {fail_rows(outcome['rows'])}")
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    if os.path.exists(RunPaths(root).frozen_spec(1)):
        pytest.fail("다른 체크포인트의 봉투로 동결본이 쓰였다")


def test_freeze_rejects_envelope_from_another_run(tmp_path) -> None:
    """이것이 없으면 다른 런에서 받은 승인이 이 런의 승인으로 재사용된다."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root, run_id="example-xx9999999z9-other-machine")
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if "approval.run-id" not in finding_rules(outcome["rows"]):
        pytest.fail(f"다른 런의 봉투가 통과했다: {fail_rows(outcome['rows'])}")
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")


def test_freeze_rejects_envelope_targeting_another_file(tmp_path) -> None:
    """이것이 없으면 해시만 맞는 아무 파일에 대한 승인이 재료 승인 행세를 한다."""
    root, _, _ = run_read(tmp_path)
    # 대상 = run.yaml. 해시는 **그 파일의 올바른 값**이므로 해시 대조로는 걸리지 않는다.
    approval_envelope(root, target_path="run.yaml")
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    rules_hit = finding_rules(outcome["rows"])
    if "approval.target-is-material-spec" not in rules_hit:
        pytest.fail(f"엉뚱한 대상을 가리키는 봉투가 통과했다: {fail_rows(outcome['rows'])}")
    if "approval.target-digest" in rules_hit:
        pytest.fail("해시는 맞았어야 한다 — 이 봉투가 걸린 이유는 대상의 정체여야 한다")
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")


def test_freeze_rejects_target_path_escaping_run_root(tmp_path) -> None:
    """이것이 없으면 봉투가 런 밖 파일을 대상으로 지목하고, 러너가 그것을 읽는다."""
    root, _, _ = run_read(tmp_path)
    outside = os.path.join(os.path.dirname(root), "outside-secret.json")
    with open(outside, "w", encoding="utf-8") as handle:
        handle.write('{"not": "this run"}\n')

    hashed: list[str] = []
    original = freeze_stage.sha256_file

    def spy(path: str) -> str:
        hashed.append(os.path.realpath(path))
        return original(path)

    approval_envelope(root, target_path="../outside-secret.json")
    freeze_stage.sha256_file = spy
    try:
        outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    finally:
        freeze_stage.sha256_file = original

    if "approval.target-inside-run" not in finding_rules(outcome["rows"]):
        pytest.fail(f"런 밖 대상이 통과했다: {fail_rows(outcome['rows'])}")
    if outcome["status"] != "halt":
        pytest.fail(f"status 기대 halt, 실제 {outcome['status']}")
    # ★ 거부만으로는 부족하다 — 읽고 나서 거부하면 이미 읽은 것이다.
    if os.path.realpath(outside) in hashed:
        pytest.fail(f"런 밖 파일을 읽고 나서 거부했다: {hashed}")


def test_freeze_accepts_a_correct_material_approval_envelope(tmp_path) -> None:
    """이것이 없으면 '전부 거부'하는 검사도 위 4건에서 만점을 받는다."""
    root, _, _ = run_read(tmp_path)
    approval_envelope(root)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "ok":
        pytest.fail(f"정상 봉투가 거부됐다: {fail_rows(outcome['rows'])}")
    identity = {
        "approval.checkpoint",
        "approval.run-id",
        "approval.target-is-material-spec",
        "approval.target-inside-run",
    }
    hit = identity.intersection(finding_rules(outcome["rows"]))
    if hit:
        pytest.fail(f"정상 봉투에 신원 결함이 붙었다: {sorted(hit)}")


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
    approval_envelope(root, derived_ack=[DERIVED_FACT_ID, "M99"])
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    phantom_rules = [
        finding.rule for row in phantom["rows"] for finding in row.findings
    ]
    if "approval.ack-no-phantom" not in phantom_rules:
        pytest.fail(f"유령 ID 가 통과했다: {phantom_rules}")

    # ③ 정확히 일치 — 통과
    approval_envelope(root, derived_ack=[DERIVED_FACT_ID])
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

    approval_envelope(root, manual_ack=[FIGURE_FACT_ID, "M77"])
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    phantom_rules = [
        finding.rule for row in phantom["rows"] for finding in row.findings
    ]
    if "approval.ack-no-phantom" not in phantom_rules:
        pytest.fail(f"유령 ID 가 통과했다: {phantom_rules}")

    approval_envelope(root, manual_ack=[FIGURE_FACT_ID])
    exact = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if exact["status"] != "ok":
        pytest.fail(f"정확히 일치인데 실패했다: {fail_rows(exact['rows'])}")


def test_render_parity_checks_en_values_not_ids(tmp_path) -> None:
    """ID 존재만 보면 판독본이 값을 잃어도 통과한다 — 그것이 구 구현의 결함이었다(재정 P-U5).

    두 방향을 다 본다. ⓐ **값**을 지우면 잡힌다 ⓑ 값은 그대로 두고 **ID 표기만** 바꾸면
    잡히지 않는다. ⓑ 가 없으면 이 검사가 값을 보는지 ID 를 보는지 구별되지 않는다.
    """
    root, _, _ = run_read(tmp_path)
    paths = RunPaths(root)
    original = read_text(paths.material_spec_md)

    # ⓐ EN 값 하나를 요약으로 대체한다 — 판독본은 KR 틀 + EN 값이므로 이것이 값의 손실이다.
    victim = "A section through the hopper and the rotary valve, with the pockets"
    if victim not in original:
        pytest.fail("표본 값이 판독본에 없다 — 이 시험이 공허해진다")
    with open(paths.material_spec_md, "w", encoding="utf-8") as handle:
        handle.write(original.replace(victim, "(도면 설명 요약)"))
    approval_envelope(root)
    outcome = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if outcome["status"] != "reject-upstream":
        pytest.fail(f"status 기대 reject-upstream, 실제 {outcome['status']}")
    hit = [
        finding for finding in
        [f for row in outcome["rows"] for f in row.findings]
        if finding.rule == "freeze.render-parity"
    ]
    if not hit:
        pytest.fail(f"값 손실이 render-parity 로 잡히지 않았다: {fail_rows(outcome['rows'])}")
    if victim not in hit[0].expected:
        pytest.fail(f"어느 값이 사라졌는지 결함에 실리지 않았다: {hit[0].expected!r}")

    # ⓑ 값은 그대로 두고 ID 표기만 바꾼 판 — 이것은 값의 손실이 아니므로 통과해야 한다.
    with open(paths.material_spec_md, "w", encoding="utf-8") as handle:
        handle.write(original.replace(f"`{FIGURE_FACT_ID}`", "`(항목)`"))
    approval_envelope(root)
    relaxed = freeze_stage.run(run_root=root, spec_version=1, rules=RULES)
    if relaxed["status"] != "ok":
        pytest.fail(
            "ID 표기만 바꾼 판이 거부됐다 — 검사가 아직 ID 를 보고 있다: "
            f"{fail_rows(relaxed['rows'])}"
        )


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


# ===========================================================================
# 8. 재정 반증 (2026-08-18 P 계열)
#
# 각 테스트는 변조·변주를 실제로 만들고 러너가 그것을 잡는지 본다. 변조본만 실패시키면
# 과잉 제약과 구별되지 않으므로 무변조 대조군을 같은 테스트 안에 둔다.
# ===========================================================================


def test_assembled_item_layout_follows_lane_order(tmp_path) -> None:
    """레인 순서가 곧 항목 번호다 — 그것이 흔들리면 이 파일의 ID 상수 전부가 엉뚱한 항목을 가리킨다."""
    _, outcome, _ = run_read(tmp_path)
    kinds = [(item["id"], item["kind"], item.get("origin")) for item in outcome["spec"]["items"]]
    expected = [
        ("M1", "component", None), ("M2", "component", None), ("M3", "component", None),
        ("M4", "grounding", None), ("M5", "grounding", None), ("M6", "grounding", None),
        ("M7", "fact", "quoted"), ("M8", "fact", "quoted"),
        ("M9", "fact", "bibliographic"), ("M10", "fact", "bibliographic"),
        ("M11", "fact", "bibliographic"), ("M12", "fact", "bibliographic"),
        (DERIVED_FACT_ID, "fact", "derived"), (FIGURE_FACT_ID, "fact", "figure-sourced"),
        ("M15", "implication", None), ("M16", "positioning", None),
        ("M17", "figure_note", None),
    ]
    if kinds != expected:
        pytest.fail(f"항목 배치가 다르다:\n기대 {expected}\n실제 {kinds}")


def test_convergence_runs_before_grounding(tmp_path) -> None:
    """조기 수렴이 뒤로 밀리면 접지 지출이 낭비된다 — 수렴 미달인 런이 접지를 다 돌고 나서 멈춘다(재정 P-4)."""
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(),
        "read-b": payload_set(dependency_type="multiple-or"),  # exact-match 축을 가른다
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)
    adapter = ReplayLaneAdapter(lanes_root)
    outcome = run_read_stage(run_root=root, adapter=adapter, rules=RULES)

    if outcome["status"] != "escalate":
        pytest.fail(f"status 기대 escalate, 실제 {outcome['status']}")
    spent = [task for task in adapter.tasks_dispatched() if task.startswith("ground")]
    if spent:
        pytest.fail(f"수렴 미달인데 접지 레인이 돌았다: {spent}")
    # 조기 판정서는 그 자리에서 산출된다 — 없으면 P-U3 의 진입 조건이 결속할 대상이 없다.
    early = load_json(RunPaths(root).convergence_early_json)
    if early["phase"] != "early":
        pytest.fail(f"조기 판정서의 phase 가 early 가 아니다: {early['phase']!r}")
    for key in ("fact_classification", "numeric_inventory"):
        block = early[key]
        occupied = block.get("total") or block.get("quoted_span", {}).get("material_ids")
        if occupied:
            pytest.fail(f"분해 직후인데 {key} 가 채워져 있다: {block}")

    # 대조군 — 두 분해가 수렴하면 접지가 돈다(수렴 검사가 접지를 막기만 하는 것이 아니다).
    clean_root, clean_outcome, clean_adapter = run_read(tmp_path.joinpath("clean"))
    if clean_outcome["status"] != "ok":
        pytest.fail(f"무변조 런이 escalate 됐다: {clean_outcome['status']}")
    if "ground-independent" not in clean_adapter.tasks_dispatched():
        pytest.fail("수렴 통과인데 접지가 돌지 않았다")
    _ = clean_root


def test_canonical_selection_is_content_blind(tmp_path) -> None:
    """정본 지정이 품질 비교를 하면 판정자 부재 원칙이 붕괴한다(재정 P-4).

    두 실행의 산출을 **서로 바꿔** 넣어도 정본은 언제나 `read_runs[0]` 이어야 한다.
    내용을 보고 고르는 코드가 있으면 이 대칭이 깨진다.
    """
    picks = []
    for index, (first, second) in enumerate((("read-a", "read-b"), ("read-b", "read-a"))):
        root, _ = run_source(tmp_path.joinpath(f"case-{index}"))
        # 한쪽 산출을 일부러 '빈약하게' 만든다 — 품질 비교가 있다면 이쪽이 탈락할 것이다.
        payloads = {
            first: payload_set(direction="concern", note="훅이 약함."),
            second: payload_set(direction="clear"),
        }
        lanes_root = write_lane_responses(root, payloads_by_run=payloads)
        outcome = run_read_stage(
            run_root=root,
            adapter=ReplayLaneAdapter(lanes_root),
            rules=RULES,
            read_runs=(first, second),
        )
        if outcome["status"] != "ok":
            pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")
        selection = outcome["convergence"]["canonical_selection"]
        if selection["read_run"] != first:
            pytest.fail(f"정본이 선언 순서를 따르지 않았다: {selection} (선언 {first} 우선)")
        if selection["rule"] != "declaration-order" or selection["content_blind"] is not True:
            pytest.fail(f"정본 지정이 내용맹·결정론으로 신고되지 않았다: {selection}")
        picks.append(selection["read_run"])
    if picks != ["read-a", "read-b"]:
        pytest.fail(f"두 배치에서 같은 실행이 뽑혔다 — 내용으로 고른 것이다: {picks}")


def test_non_canonical_run_has_no_grounding_lane(tmp_path) -> None:
    """비정본 실행이 접지를 돌면 "정본 1개" 가 미집행이다 — 그 사실은 로그에 **없음으로** 증명된다(재정 P-4·P-U3)."""
    root, outcome, adapter = run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"status 기대 ok, 실제 {outcome['status']} — {fail_rows(outcome['rows'])}")

    log = load_json(RunPaths(root).lane_log)
    tasks_by_run: dict[str, set] = {}
    for row in log:
        tasks_by_run.setdefault(row["read_run"], set()).add(row["task"])
    if tasks_by_run.get("read-b") != {"decompose"}:
        pytest.fail(f"비정본 실행이 분해 밖의 레인을 돌았다: {sorted(tasks_by_run.get('read-b', []))}")
    for task in ("ground-independent", "ground-dependent", "synthesize"):
        if task not in tasks_by_run.get("read-a", set()):
            pytest.fail(f"정본 실행이 {task} 를 돌지 않았다: {sorted(tasks_by_run.get('read-a', []))}")

    # 그 부재를 **검사가 본다**. 로그만 그렇고 검사가 없으면 다음 개정에서 조용히 되돌아간다.
    shape = [row for row in outcome["rows"] if row.check_id == "read.lane-log-shape"]
    if not shape or shape[0].status != "pass":
        pytest.fail(f"레인 로그 형태 검사가 없거나 실패했다: {shape}")

    # 변조 — 비정본 실행에 접지 레인 기록을 심으면 검사가 잡는다.
    journal = read_stage.LaneJournal()
    journal.rows = [
        {"read_run": "read-a", "task": "decompose"},
        {"read_run": "read-b", "task": "decompose"},
        {"read_run": "read-b", "task": "ground-independent"},
        {"read_run": "read-a", "task": "synthesize"},
    ]
    row = read_stage.check_lane_log_shape(
        journal, read_runs=("read-a", "read-b"), canonical="read-a"
    )
    if row.status != "fail":
        pytest.fail("비정본 실행의 접지 기록이 통과했다 — 부재의 증명이 성립하지 않는다")
    if "lane-log.non-canonical-tail" not in [finding.rule for finding in row.findings]:
        pytest.fail(f"결함 규칙이 다르다: {[f.rule for f in row.findings]}")
    _ = adapter


def test_cp1_surface_shows_total_numeric_count(tmp_path) -> None:
    """전량 카운트가 없으면 "미참조 접힘"이 은폐가 된다(재정 P-B)."""
    root, outcome, _ = run_read(tmp_path)
    rendered = read_text(RunPaths(root).material_spec_md)
    inventory = outcome["convergence"]["numeric_inventory"]
    total = inventory["total"]
    referenced = inventory["referenced"]
    unreferenced = inventory["unreferenced"]

    if total != len(HARVESTED_LABELS):
        pytest.fail(f"전수 수확 카운트가 다르다: {total} != {len(HARVESTED_LABELS)}")
    if len(referenced) + len(unreferenced) != total:
        pytest.fail(f"참조·미참조의 합이 전량과 다르다: {inventory}")
    # 중요분은 LLM 판단이 아니라 **역참조**로 도출된다 — 통합 레인이 실제로 적은 두 건이다.
    if sorted(referenced) != sorted(["M7", "M8"]):
        pytest.fail(f"역참조로 도출된 중요분이 다르다: {referenced}")

    # ★ 헤드라인은 **범위를 밝히고** 센다(2026-08-18 통주 2 처분 ⓒ). 구 문언 "전체 N건"은
    #   어느 범위의 계수인지를 적지 않아, 정답지 밖 역참조(figure-sourced)가 하나 섞이면
    #   같은 문서 안의 두 수가 어긋난 채로 읽혔다.
    headline = (
        f"**수확 정답지 {total}건({ANSWER_SCOPE_TEXT}) — "
        f"참조 {len(referenced)}건 표시, 미참조 {len(unreferenced)}건 접힘**"
    )
    if headline not in rendered:
        pytest.fail(f"전량 카운트 상시 표기가 없다: {headline!r}")
    section = rendered.split("## 12. ★ 수치 인벤토리")[1].split("## 13.")[0]
    if "<details>" not in section:
        pytest.fail("미참조분이 접히지 않았다")
    for item_id in unreferenced:
        if item_id not in section:
            pytest.fail(f"미참조 수치 {item_id} 이 표면에서 통째로 빠졌다 — 접힘이 아니라 은폐다")


def _write_continue_envelope(root: str, *, digest: str | None = None) -> str:
    """Owner '계속' 봉투(재정 P-U3). 대상은 **조기 수렴 판정서 자체**다."""
    paths = RunPaths(root)
    if digest is None:
        with open(paths.convergence_early_json, "rb") as handle:
            digest = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    frontmatter = {
        "schema": "approval-envelope/v0",
        "checkpoint": "convergence_continue",
        "run_id": RUN_ID,
        "target": {"path": "10-read/convergence-early.json", "digest": digest},
        "decision": "approved",
        "owner_quote": "독해 프로파일을 봤다. 이 갈림은 받아들이고 계속 간다.",
        "quote_provenance": {
            "channel": "session-transcript",
            "located_at": "2026-08-18 세션 · 수렴 상신 응답",
        },
        "decided_at": "2026-08-18T05:00:00Z",
        "recorded_by": "orchestrator",
    }
    body = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
    with open(paths.convergence_continue_md, "w", encoding="utf-8") as handle:
        handle.write(f"---\n{body}---\n\n# 수렴 계속 — 독해 프로파일 확인\n")
    return paths.convergence_continue_md


def test_grounding_requires_convergence_verdict_or_envelope(tmp_path) -> None:
    """접지 진입이 판정서에 결속되지 않으면 "앞으로 옮겼다"가 실행 순서의 관습으로만 남는다(재정 P-U3).

    표본은 **상신 축**(element-set)이 갈린 판이다 — 판정 행은 실패가 아니지만(재정 P-3)
    접지는 열리지 않는다. 그 둘이 다른 층이라는 것이 이 게이트의 요지다.
    """
    root, _ = run_source(tmp_path)
    payloads = {
        "read-a": payload_set(),
        "read-b": payload_set(element_two=E2_TEXT_VARIANT),
    }
    lanes_root = write_lane_responses(root, payloads_by_run=payloads)

    # ① 판정서만 있고 봉투가 없으면 접지가 열리지 않는다.
    blocked_adapter = ReplayLaneAdapter(lanes_root)
    blocked = run_read_stage(run_root=root, adapter=blocked_adapter, rules=RULES)
    if blocked["status"] != "escalate":
        pytest.fail(f"상신 축 미달인데 status 가 {blocked['status']} 다")
    if blocked["reason_label"] != "독해 프로파일 상신":
        pytest.fail(f"사유 라벨이 다르다: {blocked['reason_label']!r}")
    if [row.check_id for row in blocked["rows"] if row.status == "fail"]:
        pytest.fail("상신 축 미달이 판정 행 fail 로 나왔다 — 층이 섞였다(재정 P-3)")
    if [task for task in blocked_adapter.tasks_dispatched() if task.startswith("ground")]:
        pytest.fail("판정서만 있고 봉투가 없는데 접지가 돌았다")

    # ② 다른 판정서에 결속된 봉투는 열지 못한다 — 결속이 없으면 '계속'은 무관한 종이다.
    _write_continue_envelope(root, digest="sha256:" + "0" * 64)
    stale_adapter = ReplayLaneAdapter(lanes_root)
    stale = run_read_stage(run_root=root, adapter=stale_adapter, rules=RULES)
    if stale["status"] != "escalate":
        pytest.fail(f"엉뚱한 판정서에 결속된 봉투가 접지를 열었다: {stale['status']}")
    if "결속" not in str(stale.get("gate_note", "")):
        pytest.fail(f"게이트가 결속 실패를 밝히지 않는다: {stale.get('gate_note')!r}")

    # ③ 이 판정서에 결속된 봉투가 있으면 접지가 열린다(과잉 제약 배제).
    _write_continue_envelope(root)
    opened_adapter = ReplayLaneAdapter(lanes_root)
    opened = run_read_stage(run_root=root, adapter=opened_adapter, rules=RULES)
    if "ground-independent" not in opened_adapter.tasks_dispatched():
        pytest.fail(f"유효한 계속 봉투인데 접지가 돌지 않았다: {opened['status']}")


def test_source_change_requires_new_run(tmp_path) -> None:
    """원천 변경이 덮어쓰기로 처리되면 바이트 오프셋이 조용히 어긋난다 — 처분은 새 런이다(재정 P-U2)."""
    root, _ = run_source(tmp_path)

    # ① 원문이 바뀐 투입물로 같은 런 작업장에 다시 봉인하려 하면 **환경 오류**다.
    changed = SOURCE.replace("12 rpm", "18 rpm")
    patent_path, figures = make_source_inputs(
        tmp_path.joinpath("changed"), figure_count=6, source_text=changed
    )
    with pytest.raises(StageEnvironmentError) as excinfo:
        source_stage.run(
            run_root=root,
            source_patent_path=patent_path,
            figures_dir=figures,
            run_id=RUN_ID,
            patent_meta=copy.deepcopy(PATENT_META),
            repo=law_repo(),
        )
    if "00-source/patent.md" not in str(excinfo.value):
        pytest.fail(f"진단이 어느 파일이 바뀌었는지 밝히지 않는다: {excinfo.value}")

    # ② 도면 세트만 바뀌어도 같은 처분이다 — 원천은 원문 + **도면 세트 전체**다.
    same_text, more_figures = make_source_inputs(
        tmp_path.joinpath("more-figures"), figure_count=7, source_text=SOURCE
    )
    with pytest.raises(StageEnvironmentError) as excinfo:
        source_stage.run(
            run_root=root,
            source_patent_path=same_text,
            figures_dir=more_figures,
            run_id=RUN_ID,
            patent_meta=copy.deepcopy(PATENT_META),
            repo=law_repo(),
        )
    if "매니페스트" not in str(excinfo.value):
        pytest.fail(f"도면 세트 변경이 매니페스트 지문으로 판정되지 않았다: {excinfo.value}")

    # ③ 대조군 — 같은 투입물이면 지문 대조는 통과한다(그 뒤 '두 번 쓰지 않는다'가 막는다).
    same_path, same_figures = make_source_inputs(
        tmp_path.joinpath("identical"), figure_count=6, source_text=SOURCE
    )
    with pytest.raises(StageError) as excinfo:
        source_stage.run(
            run_root=root,
            source_patent_path=same_path,
            figures_dir=same_figures,
            run_id=RUN_ID,
            patent_meta=copy.deepcopy(PATENT_META),
            repo=law_repo(),
        )
    if isinstance(excinfo.value, StageEnvironmentError):
        pytest.fail(f"같은 투입물인데 지문 불일치로 판정됐다: {excinfo.value}")

    # ④ 생산 경로에 재봉인(지문 재계산) 함수를 두지 않는다 — 그 자리는 테스트 하네스다.
    import inspect  # noqa: PLC0415

    source_code = inspect.getsource(source_stage)
    for forbidden in ("def reseal", "def rewrite_digest", "def force_source"):
        if forbidden in source_code:
            pytest.fail(f"생산 경로에 재봉인 자리가 있다: {forbidden}")


def test_run_is_pinned_to_engine_commit(tmp_path) -> None:
    """커밋 핀이 없으면 "런의 법이 무엇이었나"를 되짚을 수 없다(재정 P-U1 · P-8)."""
    import subprocess  # noqa: PLC0415

    def git(*args, cwd) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
        )

    # 소형 리포 하나를 세운다 — 본 리포의 HEAD 에 기대면 시험이 작업 상태에 좌우된다.
    fake = tmp_path / "law"
    fake.mkdir()
    git("init", "-q", cwd=fake)
    git("config", "user.email", "t@example.com", cwd=fake)
    git("config", "user.name", "t", cwd=fake)
    (fake / "contracts").mkdir()
    (fake / "contracts" / "pipeline.yaml").write_text("schema: pipeline/v0\n", encoding="utf-8")
    git("add", "contracts/pipeline.yaml", cwd=fake)
    git("commit", "-q", "-m", "law v1", cwd=fake)

    tool = os.path.join(REPO, "tools", "run_worktree.py")
    created = subprocess.run(
        [sys.executable, tool, "create", RUN_ID, "--repo", str(fake), "--root", str(tmp_path / "wt")],
        capture_output=True, text=True, check=False,
    )
    if created.returncode != 0:
        pytest.fail(f"create 종료 코드 {created.returncode} (기대 0) — {created.stderr}")
    payload = json.loads(created.stdout)
    commit = payload["commit"]
    if len(commit) != 40 or not all(char in "0123456789abcdef" for char in commit):
        pytest.fail(f"커밋 핀이 40hex 가 아니다: {commit!r}")
    if not os.path.isdir(payload["worktree"]):
        pytest.fail(f"격리 체크아웃이 만들어지지 않았다: {payload['worktree']}")

    # 핀을 든 run.yaml 은 만료되지 않았다고 통지한다(종료 코드 0).
    run_yaml = tmp_path / "run.yaml"
    run_yaml.write_text(
        yaml.safe_dump(
            {"schema": "run/v0", "run_id": RUN_ID, "engine": {"commit": commit, "worktree": payload["worktree"]}},
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    fresh = subprocess.run(
        [sys.executable, tool, "expiry", str(run_yaml), "--repo", str(fake)],
        capture_output=True, text=True, check=False,
    )
    if fresh.returncode != 0:
        pytest.fail(f"동일 커밋인데 expiry 가 {fresh.returncode} 를 냈다 — {fresh.stdout}{fresh.stderr}")

    # 법이 개정되면 **만료를 통지한다**(종료 코드 3) — 재검을 막지 않고 알려 줄 뿐이다.
    (fake / "contracts" / "pipeline.yaml").write_text(
        "schema: pipeline/v0\nchanged: true\n", encoding="utf-8"
    )
    git("add", "contracts/pipeline.yaml", cwd=fake)
    git("commit", "-q", "-m", "law v2", cwd=fake)
    expired = subprocess.run(
        [sys.executable, tool, "expiry", str(run_yaml), "--repo", str(fake)],
        capture_output=True, text=True, check=False,
    )
    if expired.returncode != 3:
        pytest.fail(f"개정 후 expiry 종료 코드 {expired.returncode} (기대 3) — {expired.stdout}")
    notice = json.loads(expired.stdout)
    if notice["expired"] is not True or notice["commits_since"] < 1:
        pytest.fail(f"만료 통지의 내용이 비었다: {notice}")
    if notice["pinned"] != commit:
        pytest.fail(f"통지가 핀을 잘못 읽었다: {notice['pinned']} != {commit}")

    # 핀이 40hex 가 아니면 **판정하지 않고 입력 오류**를 낸다(지어낸 기준으로 판정하지 않는다).
    run_yaml.write_text(
        yaml.safe_dump({"schema": "run/v0", "run_id": RUN_ID, "engine": {"commit": ""}}),
        encoding="utf-8",
    )
    unpinned = subprocess.run(
        [sys.executable, tool, "expiry", str(run_yaml), "--repo", str(fake)],
        capture_output=True, text=True, check=False,
    )
    if unpinned.returncode != 2:
        pytest.fail(f"핀 없는 run.yaml 의 종료 코드 {unpinned.returncode} (기대 2)")


def test_source_writes_engine_commit_pin(tmp_path) -> None:
    """핀을 사람이 손으로 넣어야 하면 그것은 결박이 아니다(재정 P-U1 · P-8).

    ★ 실측 배경: 실특허 통주 개시 때 `run.yaml#engine.commit` 이 **빈 문자열**로 나왔고 핀을
    손으로 넣어야 했다. 도구(`tools/run_worktree.py`)는 의도적으로 `run.yaml` 을 쓰지 않으므로
    (SPEC §7.3 기입 주체 행 — 기록 주체는 러너 하나다) **아무도 핀을 쓰지 않는** 공백이 있었다.
    이 시험은 그 공백을 막는다: 도구를 부르지 않아도 러너가 스스로 핀을 든다.
    """
    law = make_law_repo(os.path.join(str(tmp_path), "law"))
    head = law_head(law)

    root, outcome = run_source(tmp_path, repo=law)
    if outcome["status"] != "ok":
        pytest.fail(f"source 가 ok 를 내지 않았다: {outcome['status']}")

    engine_block = (load_yaml(RunPaths(root).run_yaml) or {}).get("engine") or {}
    commit = str(engine_block.get("commit", ""))
    if len(commit) != 40 or not all(char in "0123456789abcdef" for char in commit):
        pytest.fail(f"engine.commit 이 40hex 가 아니다: {commit!r}")
    if commit != head:
        pytest.fail(f"핀이 그 시점 HEAD 와 다르다: {commit} != {head}")
    if "worktree" not in engine_block:
        pytest.fail(f"engine.worktree 가 기입되지 않았다: {engine_block}")
    if engine_block["worktree"] is not None:
        pytest.fail(f"주 작업 트리에서 돈 런인데 worktree 가 채워졌다: {engine_block['worktree']}")

    # 격리 체크아웃(worktree)에서 돌면 **그 경로**가 기록된다 — 재정 P-U1 의 구현 형태다.
    # `.worktrees/` 는 이 결박 기제 자신의 생성물이므로 더러움으로 세지 않는다(그렇지 않으면
    # 첫 런을 만든 순간 다음 런이 전부 막힌다).
    checkout = os.path.join(law, ".worktrees", RUN_ID)
    git_law(law, "worktree", "add", "--detach", checkout, head)
    wt_root, wt_outcome = run_source(tmp_path.joinpath("in-worktree"), repo=checkout)
    if wt_outcome["status"] != "ok":
        pytest.fail(f"격리 체크아웃에서 source 가 ok 를 내지 않았다: {wt_outcome['status']}")
    wt_engine = (load_yaml(RunPaths(wt_root).run_yaml) or {}).get("engine") or {}
    if wt_engine.get("commit") != head:
        pytest.fail(f"체크아웃의 핀이 다르다: {wt_engine.get('commit')} != {head}")
    if wt_engine.get("worktree") != f".worktrees/{RUN_ID}":
        pytest.fail(f"worktree 경로가 기록되지 않았다: {wt_engine.get('worktree')!r}")


def test_source_refuses_to_start_on_dirty_tree(tmp_path) -> None:
    """커밋되지 않은 변경은 커밋에 결박될 수 없다 — 그런 런은 시작하지 않는다(재정 P-U1).

    핀이 있어도 트리가 더러우면 그 핀은 거짓말이다("이 법 아래 돌았다"고 적힌 커밋에 실제로
    돈 코드가 없다). `tools/run_worktree.py create` 가 같은 판정을 하며, 판정의 정본은
    `engine/gitpin.py` 한 곳이다 — 도구와 러너가 두 벌로 적으면 한 벌이 낡는다.
    """
    law = make_law_repo(os.path.join(str(tmp_path), "law"))
    # ① 추적 파일의 미커밋 개정 + ② 미추적 파일. 둘 다 더러움이다.
    with open(os.path.join(law, "contracts", "format-parameters.yaml"), "a", encoding="utf-8") as handle:
        handle.write("\n# 커밋되지 않은 개정\n")
    with open(os.path.join(law, "untracked.md"), "w", encoding="utf-8") as handle:
        handle.write("미추적 파일\n")

    root = os.path.join(str(tmp_path), "runs", RUN_ID)
    with pytest.raises(StageError) as excinfo:
        run_source(tmp_path, repo=law, run_root=root)

    diagnosis = str(excinfo.value)
    # 더러운 트리는 **세계의 고장이 아니라 런을 열 전제의 미비**다 — 환경 오류가 아니다.
    if isinstance(excinfo.value, StageEnvironmentError):
        pytest.fail(f"더러운 트리가 환경 오류로 분류됐다(조치는 halt 다): {diagnosis}")
    if not isinstance(excinfo.value, StageHaltError):
        pytest.fail(f"조치가 halt 계열이 아니다: {type(excinfo.value).__name__} — {diagnosis}")
    for needle in ("halt", "재정 P-U1", "contracts/format-parameters.yaml", "untracked.md"):
        if needle not in diagnosis:
            pytest.fail(f"진단에 {needle} 이 없다: {diagnosis}")

    # 결박 전에는 **아무것도 쓰지 않는다** — 반쯤 열린 런을 남기지 않는다.
    if os.path.exists(root):
        pytest.fail(f"거부된 런의 작업장이 만들어졌다: {sorted(os.listdir(root))}")

    # 대조군 — 변경을 정리하면 같은 입력으로 런이 열린다(과잉 제약 배제).
    os.remove(os.path.join(law, "untracked.md"))
    head = commit_law(law, "개정 커밋")
    _, outcome = run_source(tmp_path, repo=law, run_root=root)
    if outcome["status"] != "ok":
        pytest.fail(f"깨끗해진 트리에서 런이 열리지 않았다: {outcome['status']}")
    engine_block = (load_yaml(RunPaths(root).run_yaml) or {}).get("engine") or {}
    if engine_block.get("commit") != head:
        pytest.fail(f"핀이 방금 만든 커밋과 다르다: {engine_block.get('commit')} != {head}")
