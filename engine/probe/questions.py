# -*- coding: utf-8 -*-
"""프로브 B 질문지(SPEC §5.2 파생 규칙 · 재정 T69 ⑥ · 총괄 재량 ⓑ = 좌석 opus-5 low).

질문의 유일한 파생원 = 블루프린트 `transmission_targets[]`. 질문 생성기는 **동결 재료 전문 + 표적 목록**만 읽고 출하 후보 스레드는
보지 않는다 — 스레드를 보고 만든 질문은 「스레드에 있는 것만 묻는」 자기 충족 측정이다. 질문지는 **런 단위**(`60-probe/questions.json`)이며
변주가 같은 질문지로 재야 비교가 성립한다(D10).

검증(결정론) — 표적마다 정확히 1(1:1) · 표적 밖 재료를 묻는 질문은 **폐기** · 같은 표적의 둘째 질문도 폐기(첫째만) · 부족한 표적이 있으면
`retry(1)` → `escalate`(계약 failure). 채택된 질문은 표적 순서로 `Q1..` 재번호되고 레인이 준 id 는 `lane_question_id` 에 남는다.
"""

from __future__ import annotations

import json
import os

from . import LANE_QUESTIONS, ProbeLaneRequest, items_by_id
from ..lanes.plan import _accepted_models
from ..paths import RunPaths
from ..stages import read_text, sha256_bytes

TARGETS_SLICE = "20-design/blueprint.json#transmission_targets"
QUESTION_ID_FORMAT = "Q{}"
DISCARD_OUTSIDE = "target-outside-transmission_targets"
DISCARD_DUPLICATE = "duplicate-target"


def lane_id_for(variant: str, attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_QUESTIONS}/{variant}/retry-{attempt}/batch-0"
    return f"{LANE_QUESTIONS}/{variant}/batch-0"


def payload_schema(targets: list[str]) -> dict:
    return {
        "type": "object",
        "title": "lane-response/probe-q",
        "additionalProperties": False,
        "required": ["questions"],
        "properties": {
            "questions": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["question_id", "target_material_id", "question_en"],
                    "properties": {
                        "question_id": {"type": "string", "pattern": "^Q[1-9][0-9]*$"},
                        "target_material_id": {"type": "string", "pattern": "^M[0-9]+$"},
                        "question_en": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def build_instructions(*, run_id: str, spec_version: int, spec_digest: str, targets: list[str], frozen_name: str, items: dict) -> str:
    rows = "\n".join(f"| `{mid}` | `{(items.get(mid) or {}).get('kind', '?')}` |" for mid in targets)
    return "\n\n".join([
        "## 런 표지\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| spec_version | `{spec_version}` |\n"
        f"| spec_digest | `{spec_digest}` |\n"
        f"| targets | {len(targets)} |\n\n"
        "너는 계기의 질문 생성기다. 출하 후보 스레드를 보지 않는다 — 「원천 조각」의 동결 재료와 표적 목록만 본다.",
        "## 전달 표적 (blueprint.json#transmission_targets · 질문의 유일한 파생원)\n\n| material_id | kind |\n|---|---|\n" + rows,
        "## 응답\n\n"
        f"`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `questions[]` 이며 표적 재료 하나마다 질문 **정확히 하나**다"
        f"(`target_material_id` 는 위 표의 id 중 하나 · 재료 정답지는 `{frozen_name}`). 표적 밖 재료를 묻는 질문은 러너가 폐기한다.",
    ]) + "\n"


def build_request(*, paths: RunPaths, repo: str, meta: dict, frozen_row: dict, variant: str, targets: list[str], config: dict,
                  attempt: int = 0) -> ProbeLaneRequest:
    lane = config["lanes"][LANE_QUESTIONS]
    version = int(frozen_row["spec_version"])
    frozen_path = paths.frozen_spec(version)
    frozen_text = read_text(frozen_path)
    frozen_name = os.path.relpath(frozen_path, paths.run_root).replace(os.sep, "/")
    items = items_by_id(json.loads(frozen_text))
    slices = {frozen_name: frozen_text, TARGETS_SLICE: json.dumps(targets, ensure_ascii=False)}
    return ProbeLaneRequest(
        lane_id=lane_id_for(variant, attempt),
        read_run=LANE_QUESTIONS,
        task=variant,
        model=lane["model"],
        effort=lane["effort"],
        prompt_path=lane["procedure"],
        instructions=build_instructions(run_id=str(meta.get("run_id", "")), spec_version=version,
                                        spec_digest=str(frozen_row.get("spec_digest", "")), targets=targets, frozen_name=frozen_name, items=items),
        repo_root=repo,
        slices=slices,
        response_schema=payload_schema(targets),
        batch=0,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, lane["model"]),
    )


def validate_questions(raw_questions: list[dict], targets: list[str]) -> tuple[list[dict], list[dict], list[str]]:
    """→ (채택 = 표적 순서 · Q 재번호, 폐기 = 사유 동반, 부족 표적). 표적마다 정확히 1(1:1 · §5.2)."""
    by_target: dict[str, dict] = {}
    discarded: list[dict] = []
    for raw in raw_questions:
        target = str(raw.get("target_material_id", ""))
        entry = {"lane_question_id": str(raw.get("question_id", "")), "target_material_id": target, "question_en": str(raw.get("question_en", ""))}
        if target not in targets:
            discarded.append({**entry, "reason": DISCARD_OUTSIDE})
        elif target in by_target:
            discarded.append({**entry, "reason": DISCARD_DUPLICATE})
        else:
            by_target[target] = entry
    accepted = [{"question_id": QUESTION_ID_FORMAT.format(index), **by_target[target]}
                for index, target in enumerate([t for t in targets if t in by_target], start=1)]
    missing = [t for t in targets if t not in by_target]
    return accepted, discarded, missing


def question_set_digest(questions: list[dict]) -> str:
    """질문지 지문 — 프로브가 읽는 세 필드의 정규 JSON."""
    body = json.dumps([{"question_id": q["question_id"], "target_material_id": q["target_material_id"], "question_en": q["question_en"]}
                       for q in questions], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(body.encode("utf-8"))


def probe_facing_text(questions: list[dict]) -> str:
    """프로브 요청서에 싣는 질문지 — 세 필드만(레인 id · 폐기 목록 · 표적 kind 는 싣지 않는다)."""
    return json.dumps({"questions": [{"question_id": q["question_id"], "target_material_id": q["target_material_id"], "question_en": q["question_en"]}
                                     for q in questions]}, ensure_ascii=False, indent=2) + "\n"


__all__ = ["DISCARD_DUPLICATE", "DISCARD_OUTSIDE", "TARGETS_SLICE", "build_instructions", "build_request", "lane_id_for", "payload_schema",
           "probe_facing_text", "question_set_digest", "validate_questions"]
