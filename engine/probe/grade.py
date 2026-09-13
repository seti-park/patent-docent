# -*- coding: utf-8 -*-
"""채점 분리(SPEC §5.3 · 재정 T69 ⑥ · D9) — 결정론 kind 3 + 모델 채점 kind 3 + 재서술 축.

판별식(고정 · 정본 = `probe.yaml#grading`): `fact` = `value_normalized + unit`(`reader.lib.normalize.match_key`) · `component` =
`text_verbatim` 정규화 문자열 포함 여부 · `figure_note` = `numerals[]` 집합 일치 / `grounding` · `implication` · `positioning` = 모델 채점
(레인 `probe-grade/<v>/batch-0` · 입력 = 표적별 답변 묶음 + 그 동결 항목의 EN 값 · **스레드 없음**).

정규화(결정론 경로) = NFKC → 소문자 → 연속 공백 1 → 문장부호 제거(수치의 소수점·하이픈 보존) → 수치 십진 표준형 → 단위 별칭 —
구현은 `reader/lib/normalize.py` 한 벌을 게이트 `numeric.exhaustive` 와 **공용**한다(사본 금지 · §5.3).

우선순위 불변식 — 결정론이 판정한 항목은 모델 채점이 뒤집지 못한다: 채점자에게 그 항목이 **전달되지 않는다**(입력에서 제외).
"""

from __future__ import annotations

import json
import os
import re
import unicodedata

from reader.lib.normalize import NormalizeError, match_key, normalize_number, normalize_unit

from . import LANE_GRADE, LANE_PROBE, ProbeLaneRequest
from .run_probes import KIND_STATED
from ..lanes.plan import _accepted_models
from ..paths import RunPaths

METHOD_DETERMINISTIC = "deterministic"
METHOD_MODEL = "model"
GRADING_INPUT_SLICE = "60-probe/<variant>/grading-input.json"
_NUMBER_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
_NUMERAL_RE = re.compile(r"\d+")
_PUNCT_RE = re.compile(r"[^\w\s.\-]", re.UNICODE)
_DANGLING_RE = re.compile(r"(?<!\d)[.\-]|[.\-](?!\d)")
_WS_RE = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# 정규화 · 결정론 대조
# ---------------------------------------------------------------------------


def normalize_text(text: str) -> str:
    """NFKC → 소문자 → 문장부호 제거(수치 안의 `.`·`-` 보존) → 연속 공백 1."""
    folded = unicodedata.normalize("NFKC", text or "").lower()
    folded = _PUNCT_RE.sub(" ", folded)
    folded = _DANGLING_RE.sub(" ", folded)
    return _WS_RE.sub(" ", folded).strip()


def _answer_text(answer: dict) -> str:
    return " ".join(str(answer.get(key) or "") for key in ("answer", "quoted_span"))


def _numeric_keys(text: str, unit: str | None) -> set[str]:
    keys: set[str] = set()
    for match in _NUMBER_RE.finditer(text):
        try:
            keys.add(match_key(normalize_number(match.group(0)), unit))
        except NormalizeError:
            continue
    return keys


def grade_fact(item: dict, answer: dict) -> str:
    """`value_normalized + unit` 일치 → hit. 수치가 아닌 값(식별자 등)은 정규화 문자열 포함으로 본다."""
    if answer.get("answer_kind") != KIND_STATED:
        return "miss"
    text = _answer_text(answer)
    value = str(item.get("value_normalized", ""))
    unit = item.get("unit")
    try:
        expected = match_key(normalize_number(value), unit)
    except NormalizeError:
        return "hit" if normalize_text(value) and normalize_text(value) in normalize_text(text) else "miss"
    resolved = normalize_unit(unit)
    if resolved and resolved not in normalize_text(text):
        return "miss"
    return "hit" if expected in _numeric_keys(text, unit) else "miss"


def grade_component(item: dict, answer: dict) -> str:
    """`text_verbatim` 정규화 문자열이 답변(답 + 인용 구간) 정규화 문자열에 포함되면 hit."""
    if answer.get("answer_kind") != KIND_STATED:
        return "miss"
    needle = normalize_text(str(item.get("text_verbatim", "")))
    return "hit" if needle and needle in normalize_text(_answer_text(answer)) else "miss"


def grade_figure_note(item: dict, answer: dict) -> str:
    """답변의 숫자열 집합 == `numerals[]` 집합 → hit."""
    if answer.get("answer_kind") != KIND_STATED:
        return "miss"
    expected = {str(n) for n in (item.get("numerals") or [])}
    found = set(_NUMERAL_RE.findall(_answer_text(answer)))
    return "hit" if expected and found == expected else "miss"


_DETERMINISTIC = {"fact": grade_fact, "component": grade_component, "figure_note": grade_figure_note}


def method_for(kind: str, grading: dict) -> str:
    if kind in grading["deterministic"]:
        if kind not in _DETERMINISTIC:
            raise ValueError(f"계약이 결정론으로 선언한 kind {kind!r} 의 판별식이 구현에 없다")
        return METHOD_DETERMINISTIC
    if kind in grading["model"]:
        return METHOD_MODEL
    raise ValueError(f"probe.yaml#grading 이 kind {kind!r} 의 채점 방식을 선언하지 않았다")


def grade_deterministic(item: dict, answer: dict) -> str:
    return _DETERMINISTIC[str(item.get("kind"))](item, answer)


# ---------------------------------------------------------------------------
# 모델 채점 — 레인 요청 1회 묶음(총괄 재량 ⓐ)
# ---------------------------------------------------------------------------


def item_values(item: dict) -> dict:
    """채점자에게 주는 항목의 EN 값 — kind 별 대조 대상(§5.3 표)만."""
    kind = str(item.get("kind"))
    if kind == "grounding":
        return {"component": item.get("component"), "spec_quotes": [str(r.get("quote", "")) for r in (item.get("spec_refs") or [])],
                "figure_captions": [str(r.get("caption_quote", "")) for r in (item.get("figure_refs") or [])]}
    if kind == "implication":
        return {"statement_en": item.get("statement_en"), "evidence_quotes": list(item.get("evidence_quotes") or [])}
    if kind == "positioning":
        return {"background_problem": item.get("background_problem"), "delta": item.get("delta"), "asserted_effect": item.get("asserted_effect")}
    raise ValueError(f"모델 채점 대상이 아닌 kind: {kind}")


def lane_id_for(variant: str, attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_GRADE}/{variant}/retry-{attempt}/batch-0"
    return f"{LANE_GRADE}/{variant}/batch-0"


def build_grading_input(*, reports: list[dict], questions: list[dict], items: dict, grading: dict, thesis_en: str,
                        invalid: set[tuple[str, str]]) -> dict:
    """채점자 입력 — 모델 채점 kind 의 표적만 · 무효 답변 제외 · 스레드 없음."""
    by_qid = {q["question_id"]: q for q in questions}
    targets: list[dict] = []
    for question in questions:
        item = items[question["target_material_id"]]
        if method_for(str(item.get("kind")), grading) != METHOD_MODEL:
            continue
        answers = []
        for report in reports:
            for answer in report["b_answers"]:
                if answer["question_id"] != question["question_id"] or (report["probe_id"], answer["question_id"]) in invalid:
                    continue
                answers.append({"probe_id": report["probe_id"], "answer_kind": answer["answer_kind"], "answer": answer["answer"],
                                "quoted_span": answer["quoted_span"]})
        targets.append({"question_id": question["question_id"], "question_en": by_qid[question["question_id"]]["question_en"],
                        "material_id": item["id"], "kind": item["kind"], "item_values": item_values(item), "answers": answers})
    return {"targets": targets, "restatements": [{"probe_id": r["probe_id"], "a_restatement": list(r["a_restatement"])} for r in reports],
            "thesis_en": thesis_en}


def payload_schema(grading_input: dict, grading: dict) -> dict:
    pairs = [(t["question_id"], a["probe_id"]) for t in grading_input["targets"] for a in t["answers"]]
    probe_ids = sorted({r["probe_id"] for r in grading_input["restatements"]})
    question_ids = sorted({q for q, _p in pairs}) or ["Q0"]
    return {
        "type": "object",
        "title": "lane-response/probe-grade",
        "additionalProperties": False,
        "required": ["grades", "restatement"],
        "properties": {
            "grades": {
                "type": "array",
                "minItems": len(pairs),
                "maxItems": len(pairs),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["probe_id", "question_id", "grade", "evidence"],
                    "properties": {
                        "probe_id": {"enum": probe_ids},
                        "question_id": {"enum": question_ids},
                        "grade": {"enum": list(grading["grades"])},
                        "evidence": {"type": "string", "minLength": 1},
                    },
                },
            },
            "restatement": {
                "type": "array",
                "minItems": len(probe_ids),
                "maxItems": len(probe_ids),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["probe_id", "judgement"],
                    "properties": {"probe_id": {"enum": probe_ids}, "judgement": {"enum": list(grading["restatement"])}},
                },
            },
        },
    }


def build_instructions(*, run_id: str, variant: str, input_name: str, grading: dict, n_targets: int, n_probes: int) -> str:
    return "\n\n".join([
        "## 런 표지\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| variant | `{variant}` |\n"
        f"| 모델 채점 표적 | {n_targets} |\n"
        f"| 프로브 | {n_probes} |\n\n"
        "너는 계기의 채점자다. 스레드를 보지 않는다 — 「원천 조각」의 채점 입력(프로브 답변 + 동결 항목의 EN 값 + 훅 논지)만 본다.",
        "## 과제\n\n"
        f"① `{input_name}#targets[]` 의 표적마다, 각 프로브 답변이 `item_values` 와 합치하는지 `{ ' | '.join(grading['grades']) }` 로 판정하고 "
        "근거로 삼은 **답변 구간**을 `evidence` 에 인용한다(`not-stated` 답변은 `miss` 다 — 전달되지 않았다는 뜻이며 프로브의 잘못이 아니다).\n\n"
        f"② `restatements[]` 의 프로브마다 세 문장 재서술이 `thesis_en` 과 정합하는지 `{ ' | '.join(grading['restatement']) }` 로 판정한다.",
        "## 응답\n\n`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — 답변마다 grades 1 행, 프로브마다 restatement 1 행. 총평은 쓰지 않는다.",
    ]) + "\n"


def build_grade_request(*, paths: RunPaths, repo: str, meta: dict, variant: str, grading_input: dict, config: dict,
                        attempt: int = 0) -> ProbeLaneRequest:
    lane = config["lanes"][LANE_GRADE]
    input_name = GRADING_INPUT_SLICE.replace("<variant>", variant)
    return ProbeLaneRequest(
        lane_id=lane_id_for(variant, attempt),
        read_run=LANE_GRADE,
        task=variant,
        model=lane["model"],
        effort=lane["effort"],
        prompt_path=lane["procedure"],
        instructions=build_instructions(run_id=str(meta.get("run_id", "")), variant=variant, input_name=input_name, grading=config["grading"],
                                        n_targets=len(grading_input["targets"]), n_probes=len(grading_input["restatements"])),
        repo_root=repo,
        slices={input_name: json.dumps(grading_input, ensure_ascii=False, indent=2, sort_keys=True) + "\n"},
        response_schema=payload_schema(grading_input, config["grading"]),
        batch=0,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, lane["model"]),
    )


def model_grades_needed(grading_input: dict) -> bool:
    return bool(grading_input["targets"]) or bool(grading_input["restatements"])


def apply_model_grades(grading_input: dict, payload: dict) -> tuple[dict[tuple[str, str], dict], dict[str, str]]:
    """→ (`{(probe_id, question_id): {grade, evidence}}`, `{probe_id: judgement}`). 빠짐·초과·중복은 ValueError."""
    expected = {(a["probe_id"], t["question_id"]) for t in grading_input["targets"] for a in t["answers"]}
    grades: dict[tuple[str, str], dict] = {}
    for row in payload.get("grades") or []:
        key = (str(row["probe_id"]), str(row["question_id"]))
        if key not in expected or key in grades:
            raise ValueError(f"채점 행이 입력 밖이거나 중복이다: {key}")
        grades[key] = {"grade": str(row["grade"]), "evidence": str(row["evidence"])}
    if set(grades) != expected:
        raise ValueError(f"채점 행이 입력 전건을 덮지 않는다: 누락 {sorted(expected - set(grades))}")
    probes = {r["probe_id"] for r in grading_input["restatements"]}
    judgements: dict[str, str] = {}
    for row in payload.get("restatement") or []:
        pid = str(row["probe_id"])
        if pid not in probes or pid in judgements:
            raise ValueError(f"재서술 판정이 입력 밖이거나 중복이다: {pid}")
        judgements[pid] = str(row["judgement"])
    if set(judgements) != probes:
        raise ValueError(f"재서술 판정이 프로브 전건을 덮지 않는다: 누락 {sorted(probes - set(judgements))}")
    return grades, judgements


__all__ = ["GRADING_INPUT_SLICE", "LANE_PROBE", "METHOD_DETERMINISTIC", "METHOD_MODEL", "apply_model_grades", "build_grade_request",
           "build_grading_input", "build_instructions", "grade_component", "grade_deterministic", "grade_fact", "grade_figure_note",
           "item_values", "lane_id_for", "method_for", "model_grades_needed", "normalize_text", "payload_schema"]
