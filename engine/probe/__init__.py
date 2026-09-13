# -*- coding: utf-8 -*-
"""계기(probe) — 스레드만 읽는 Haiku n 대로 **전달 충실도**를 재는 자문 층(재정 2026-09-13 T69 ⑥ · M7-a · SPEC §1.11 · §5 · D9).

실물 = `questions.py`(질문 생성 레인 · 런 단위 질문지 · 1:1 검증) · `run_probes.py`(계기 요청 n · 동일 바이트 · 무효 답변 결정론 검사) ·
`grade.py`(채점 분리 — 결정론 kind 3 + 모델 채점 kind 3 · 재서술 축) · `localize.py`(annotation-index 역참조 · 2단 규칙 · score.json) ·
`procedure-*.md`(레인 절차 3). 러너 = `engine/stages/probe.py`.

★ 계기와 채점자의 분리가 계약이다(§1.11). 계기 요청서에는 스레드와 질문지만 실리고, 채점자 요청서에는 스레드가 실리지 않는다.
★ 계기는 거부권이 없다(§5.7) — `score.json` 에 판정 키가 없고(스키마), 결과는 `compose` 재리비전을 트리거하지 못한다.
★ 값을 코드에 두지 않는다 — n · 상한 · 좌석 · 채점 판별식 · 환산값 · 정규식은 `contracts/stages/probe.yaml`·`parameters.yaml` 에서 읽는다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import ClassVar

from ..lanes.contract import LaneRequest, register_lane_vocabulary
from ..paths import load_stage_contract
from ..pens import registry
from ..stages import StageError, load_yaml

STAGE_ID = "probe"
PARAMETERS_REL = ("contracts", "parameters.yaml")
LANE_QUESTIONS = "probe-q"
LANE_PROBE = "probe"
LANE_GRADE = "probe-grade"
LANE_RUNS: tuple[str, ...] = (LANE_QUESTIONS, LANE_PROBE, LANE_GRADE)

_CONTRACT_AT_IMPORT = load_stage_contract(STAGE_ID)
VARIANTS: tuple[str, ...] = registry.variant_ids(contract=load_stage_contract("compose"))
register_lane_vocabulary(STAGE_ID, LANE_RUNS, VARIANTS)


@dataclass(frozen=True)
class ProbeLaneRequest(LaneRequest):
    """계기 계열 레인 요청 — 어휘는 `probe-q|probe|probe-grade`/`v1|v2|v3` 뿐이다(계약 `probe.yaml#lane.lane_id_vocabulary`)."""

    RUNS: ClassVar[tuple[str, ...]] = LANE_RUNS
    TASKS: ClassVar[tuple[str, ...]] = VARIANTS


def probe_n(repo: str) -> int:
    data = load_yaml(os.path.join(repo, *PARAMETERS_REL))
    value = (data.get("adjustable") or {}).get("probe.n")
    if not isinstance(value, int) or value < 1:
        raise StageError("parameters.yaml#adjustable.probe.n 이 없다")
    return value


def probe_config(repo: str, contract: dict | None = None) -> dict:
    """`{n, lanes: {id: {vendor, model, effort, procedure}}, grading: {...}, input_clean_patterns: [...]}` — 전부 계약에서."""
    contract = contract or load_stage_contract(STAGE_ID, repo)
    lane = contract.get("lane") or {}
    lanes: dict[str, dict] = {}
    for entry in lane.get("sub_lanes") or []:
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        lanes[str(entry["id"])] = {"vendor": str(entry.get("vendor", "")), "model": str(entry.get("model", "")),
                                   "effort": str(entry.get("effort", "")), "procedure": str(entry.get("procedure", ""))}
    for lane_id in LANE_RUNS:
        entry = lanes.get(lane_id) or {}
        if not entry.get("model") or not entry.get("effort") or not entry.get("procedure"):
            raise StageError(f"probe.yaml#lane.sub_lanes 에 {lane_id} 의 model·effort·procedure 가 없다")
    grading = contract.get("grading") or {}
    det = [str(row.get("kind")) for row in (grading.get("deterministic") or []) if isinstance(row, dict)]
    mod = [str(row.get("kind")) for row in (grading.get("model") or []) if isinstance(row, dict)]
    grades = [str(g) for g in (grading.get("grades") or [])]
    scores = {str(k): float(v) for k, v in (grading.get("scores") or {}).items()}
    restatement = [str(g) for g in (grading.get("restatement") or [])]
    if not det or not mod or set(det) & set(mod) or not grades or set(scores) != set(grades) or not restatement:
        raise StageError("probe.yaml#grading 이 불완전하다 — kind 판별식 · 등급 · 환산값 · 재서술 축 전부가 필요하다")
    patterns = [str(p) for p in (contract.get("input_clean_patterns") or [])]
    if not patterns:
        raise StageError("probe.yaml#input_clean_patterns 가 비어 있다")
    return {"n": probe_n(repo), "lanes": lanes, "grading": {"deterministic": det, "model": mod, "grades": grades, "scores": scores,
                                                             "restatement": restatement}, "input_clean_patterns": patterns}


def targets_of(blueprint: dict) -> list[str]:
    targets = [str(t) for t in (blueprint.get("transmission_targets") or [])]
    if not targets:
        raise StageError("blueprint.json#transmission_targets 가 비어 있다 — 프로브 B 질문의 파생원이 없다(§5.2)")
    return targets


def items_by_id(frozen: dict) -> dict[str, dict]:
    return {str(item.get("id")): item for item in (frozen.get("items") or []) if isinstance(item, dict)}


__all__ = ["LANE_GRADE", "LANE_PROBE", "LANE_QUESTIONS", "LANE_RUNS", "STAGE_ID", "VARIANTS", "ProbeLaneRequest", "items_by_id",
           "probe_config", "probe_n", "targets_of"]
