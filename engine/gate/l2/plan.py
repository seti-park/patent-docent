# -*- coding: utf-8 -*-
"""L2 레인 요청 조립(재정 2026-09-13 T69 ⑥ · M4/M8-a).

한 변주의 주석본 한 판에 대해 요청 **1건**을 만든다 — 좌표 `gate-l2/<v>/batch-0`(재요청 없음 · 위상 봉쇄 · D8).
요청서에 실리는 것 = 주석본 · 동결본 · 블루프린트(§1.10 `may_read` 안). `00-source/**` · 다른 변주 · 이전 판정 · L1 로그는
싣지 않는다 — L2 는 전역 판단이지 재판정이 아니다.

★ 값을 코드에 두지 않는다 — 좌석 = `gate.yaml#layers.l2.lane` · 절차 = `layers.l2.procedure` · memo.rule 접두 = `layers.l2.memo_rule_prefix`.
payload = `{memos: [{rule: "l2.<slug>", locus: {tweet|null, sentence|null}, text}]}` · id `m-l2-NNN` 은 러너가 부여한다(§4.2).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import ClassVar

from ...lanes.contract import LaneRequest, register_lane_vocabulary
from ...lanes.plan import _accepted_models
from ...paths import RunPaths, load_stage_contract
from ...pens import registry
from ...stages import StageError, read_text

STAGE_ID = "gate"
LANE_RUN = "gate-l2"
LANE_RUNS: tuple[str, ...] = (LANE_RUN,)
LAYER_L2 = "l2"
BATCH = 0

_CONTRACT_AT_IMPORT = load_stage_contract(STAGE_ID)
VARIANTS: tuple[str, ...] = registry.variant_ids(contract=load_stage_contract("compose"))
register_lane_vocabulary(LANE_RUN, LANE_RUNS, VARIANTS)


@dataclass(frozen=True)
class GateL2LaneRequest(LaneRequest):
    """L2 레인 요청 — 어휘는 `gate-l2`/`v1|v2|v3` 뿐이다(계약 `gate.yaml#layers.l2.lane_id_vocabulary`)."""

    RUNS: ClassVar[tuple[str, ...]] = LANE_RUNS
    TASKS: ClassVar[tuple[str, ...]] = VARIANTS


def l2_config(repo: str, contract: dict | None = None) -> dict:
    """`{model, effort, procedure, rule_prefix, free_revision}` — 전부 계약에서."""
    contract = contract or load_stage_contract(STAGE_ID, repo)
    l2 = (contract.get("layers") or {}).get(LAYER_L2) or {}
    lane = l2.get("lane") or {}
    model, effort = str(lane.get("model", "")), str(lane.get("effort", ""))
    if str(l2.get("status")) != "active" or not model or not effort:
        raise StageError("gate.yaml#layers.l2 가 active 가 아니거나 lane.model·effort 가 없다")
    prefix = str(l2.get("memo_rule_prefix", ""))
    if not prefix:
        raise StageError("gate.yaml#layers.l2.memo_rule_prefix 가 없다")
    free = (contract.get("loop") or {}).get("free_revision")
    if not isinstance(free, int) or free < 1:
        raise StageError("gate.yaml#loop.free_revision 이 없다 — 자유 리비전 횟수는 계약이 든다")
    return {
        "model": model,
        "effort": effort,
        "procedure": str(l2.get("procedure") or "engine/gate/l2/procedure.md"),
        "rule_prefix": prefix,
        "free_revision": free,
    }


def payload_schema(config: dict) -> dict:
    """`{memos[]}` — 전 속성 string(숫자 필드 없음 · §4.6 기제 2) · additionalProperties false · 빈 배열 허용."""
    return {
        "type": "object",
        "title": "lane-response/gate-l2",
        "additionalProperties": False,
        "required": ["memos"],
        "properties": {
            "memos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["rule", "locus", "text"],
                    "properties": {
                        "rule": {"type": "string", "pattern": "^" + config["rule_prefix"].replace(".", "\\.") + "[a-z][a-z0-9-]*$"},
                        "locus": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["tweet", "sentence"],
                            "properties": {"tweet": {"type": ["integer", "null"], "minimum": 1},
                                           "sentence": {"type": ["integer", "null"], "minimum": 1}},
                        },
                        "text": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def _import_time_schema() -> dict:
    try:
        config = l2_config(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),
                           _CONTRACT_AT_IMPORT)
    except StageError:
        return {"type": "object"}
    return payload_schema(config)


_PAYLOAD_SCHEMA = _import_time_schema()
#: 셋 다 **같은** 스키마 객체 — 구동기 `wrapper_schema(task, read_run="gate-l2")` 가 task(변주 id)로 조회한다.
RESPONSE_SCHEMAS: dict[str, dict] = {variant: _PAYLOAD_SCHEMA for variant in VARIANTS}


def lane_id_for(variant: str) -> str:
    return f"{LANE_RUN}/{variant}/batch-{BATCH}"


def build_instructions(*, run_id: str, variant: str, spec_version: int, spec_digest: str, thread_digest: str, config: dict,
                       frozen_name: str, blueprint_name: str, thread_name: str, index_name: str) -> str:
    return "\n\n".join([
        "## 런 표지\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| variant | `{variant}` |\n"
        f"| spec_version | `{spec_version}` |\n"
        f"| spec_digest | `{spec_digest}` |\n"
        f"| thread_digest | `{thread_digest}` |\n\n"
        "너는 L2 자문 심급이다. 전역 판단의 메모만 낸다 — 글을 고치지 않고, 판정을 바꾸지 않으며, 점수를 매기지 않는다(D8·D15). "
        "파일 시스템을 열지 않는다 · 필요한 것은 전부 「원천 조각」 절에 있다.",
        "## 좌표계\n\n"
        f"`locus = {{tweet, sentence}}` 는 「원천 조각」의 `{index_name}` 의 `tweets[].n` · `sentences[].i` 와 같다(SPEC §3.3 · §4.2). "
        "전역 메모(특정 문장이 아닌 구조·흐름)는 둘 다 `null` 로, 트윗 단위는 `sentence: null` 로 적는다. "
        f"주석본 원문은 `{thread_name}`, 재료 정답지는 `{frozen_name}`, 설계는 `{blueprint_name}` 이다.",
        "## 응답\n\n"
        f"`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `memos[]` 이며 해당 없음은 빈 배열이다. `rule` 은 `{config['rule_prefix']}<slug>` 형태의 "
        "관점 표지이고 `text` 는 서술이다. 이 메모는 펜의 **자유 리비전 1회**의 데이터로 전달된다 — 펜은 네 판단으로 고칠지 말지를 정한다. "
        "메모는 그 뒤 다시 돌지 않는다(위상 봉쇄).",
    ]) + "\n"


def build_request(*, paths: RunPaths, repo: str, meta: dict, frozen_row: dict, variant: str, thread_text: str,
                  config: dict | None = None) -> GateL2LaneRequest:
    config = config or l2_config(repo, paths.contracts[STAGE_ID])
    version = int(frozen_row["spec_version"])
    frozen_path = paths.frozen_spec(version)
    rel = lambda path: os.path.relpath(path, paths.run_root).replace(os.sep, "/")  # noqa: E731
    frozen_name, blueprint_name = rel(frozen_path), rel(paths.blueprint_json)
    thread_name, index_name = rel(paths.thread_annotated(variant)), rel(paths.annotation_index_json(variant))
    slices = {
        thread_name: thread_text,
        frozen_name: read_text(frozen_path),
        blueprint_name: read_text(paths.blueprint_json),
        index_name: read_text(paths.annotation_index_json(variant)),
    }
    from ...stages import sha256_bytes  # noqa: PLC0415 - 순환 회피

    return GateL2LaneRequest(
        lane_id=lane_id_for(variant),
        read_run=LANE_RUN,
        task=variant,
        model=config["model"],
        effort=config["effort"],
        prompt_path=config["procedure"],
        instructions=build_instructions(
            run_id=str(meta.get("run_id", "")), variant=variant, spec_version=version,
            spec_digest=str(frozen_row.get("spec_digest", "")), thread_digest=sha256_bytes(thread_text.encode("utf-8")),
            config=config, frozen_name=frozen_name, blueprint_name=blueprint_name, thread_name=thread_name, index_name=index_name,
        ),
        repo_root=repo,
        slices=slices,
        response_schema=payload_schema(config),
        batch=BATCH,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, config["model"]),
    )


__all__ = ["LANE_RUN", "LANE_RUNS", "RESPONSE_SCHEMAS", "VARIANTS", "GateL2LaneRequest", "build_instructions", "build_request",
           "l2_config", "lane_id_for", "payload_schema"]
