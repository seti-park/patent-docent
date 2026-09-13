# -*- coding: utf-8 -*-
"""L1 레인 요청 조립(재정 2026-09-13 T67 ② · M6-a).

한 변주의 주석본 한 판에 대해 **바이트 동일한 요청 k 건**을 만든다 — 독립 실행은 좌표(`batch-<i>`)로만 갈린다
(SPEC §4.5 「동일 프롬프트·동일 입력으로 독립 실행 k회」). 요청서에 실리는 것은 §1.10 `may_read` 안의 넷뿐이다:
주석본 · 동결본 · 주석 인덱스 · 화행 술어 파일. `00-source/**` 와 다른 변주는 싣지 않는다(must_not_read).

★ 값을 코드에 두지 않는다 — k = `parameters.yaml#gate.l1.k` · 좌석 = `gate.yaml#layers.l1.lane` · 규칙 id =
`gate.yaml#layers.l1.rules[]` · 술어 = `speech-acts.yaml#predicates` · 화행 flag rule 형 = `gate.yaml#layers.speech_act_flag.flag_rule`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import ClassVar

from ...lanes.contract import LaneRequest, register_lane_vocabulary
from ...lanes.plan import _accepted_models
from ...paths import RunPaths, load_stage_contract
from ...pens import registry
from ...stages import StageError, load_yaml, read_text

STAGE_ID = "gate"
LANE_RUN = "gate-l1"
LANE_RUNS: tuple[str, ...] = (LANE_RUN,)
PARAMETERS_REL = ("contracts", "parameters.yaml")
SPEECH_ACTS_REL = ("contracts", "lexicon", "speech-acts.yaml")
LAYER_L1 = "l1"
LAYER_SPEECH_ACT = "speech_act_flag"

_CONTRACT_AT_IMPORT = load_stage_contract(STAGE_ID)
VARIANTS: tuple[str, ...] = registry.variant_ids(contract=load_stage_contract("compose"))
register_lane_vocabulary(LANE_RUN, LANE_RUNS, VARIANTS)


@dataclass(frozen=True)
class GateL1LaneRequest(LaneRequest):
    """L1 레인 요청 — 어휘는 `gate-l1`/`v1|v2|v3` 뿐이다(계약 `gate.yaml#lane.lane_id_vocabulary`)."""

    RUNS: ClassVar[tuple[str, ...]] = LANE_RUNS
    TASKS: ClassVar[tuple[str, ...]] = VARIANTS


# ---------------------------------------------------------------------------
# 계약 값
# ---------------------------------------------------------------------------


def l1_k(repo: str) -> int:
    data = load_yaml(os.path.join(repo, *PARAMETERS_REL))
    value = (data.get("adjustable") or {}).get("gate.l1.k")
    if not isinstance(value, int) or value < 1:
        raise StageError("parameters.yaml#adjustable.gate.l1.k 가 없다")
    return value


def l1_config(repo: str, contract: dict | None = None) -> dict:
    """`{model, effort, k, rules, veto_rules, advisory_rules, flag_rule, procedure, predicates}` — 전부 파일에서."""
    contract = contract or load_stage_contract(STAGE_ID, repo)
    layers = contract.get("layers") or {}
    l1 = layers.get(LAYER_L1) or {}
    lane = l1.get("lane") or {}
    model, effort = str(lane.get("model", "")), str(lane.get("effort", ""))
    if str(l1.get("status")) != "active" or not model or not effort:
        raise StageError("gate.yaml#layers.l1 이 active 가 아니거나 lane.model·effort 가 없다")
    rules = [dict(rule) for rule in (l1.get("rules") or []) if isinstance(rule, dict) and rule.get("id")]
    if not rules:
        raise StageError("gate.yaml#layers.l1.rules 가 비어 있다 — L1 규칙 id 는 계약이 든다")
    speech = layers.get(LAYER_SPEECH_ACT) or {}
    flag_rule = str(speech.get("flag_rule", ""))
    if str(speech.get("status")) != "active" or "<predicate>" not in flag_rule:
        raise StageError("gate.yaml#layers.speech_act_flag 가 active 가 아니거나 flag_rule 에 <predicate> 자리가 없다")
    acts = load_yaml(os.path.join(repo, *SPEECH_ACTS_REL))
    predicates = [dict(p) for p in (acts.get("predicates") or []) if isinstance(p, dict) and p.get("id")]
    if not predicates:
        raise StageError("speech-acts.yaml#predicates 가 비어 있다")
    return {
        "model": model,
        "effort": effort,
        "k": l1_k(repo),
        "rules": rules,
        "veto_rules": [str(r["id"]) for r in rules if r.get("veto") is True],
        "advisory_rules": [str(r["id"]) for r in rules if r.get("veto") is False],
        "flag_rule": flag_rule,
        "procedure": str(l1.get("procedure") or "engine/gate/l1/procedure.md"),
        "predicates": predicates,
        "speech_act_version": str(acts.get("version", "")),
        "scope": str(acts.get("scope", "")).strip(),
    }


# ---------------------------------------------------------------------------
# payload 스키마 — $defs 없이 인라인(구동기 래퍼가 그대로 품는다)
# ---------------------------------------------------------------------------


def _locus_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["tweet", "sentence"],
        "properties": {"tweet": {"type": "integer", "minimum": 1}, "sentence": {"type": "integer", "minimum": 1}},
    }


def payload_schema(config: dict) -> dict:
    """`{defects[], flags[], speech_acts[]}` — 전부 배열(빈 배열 허용) · additionalProperties false."""
    return {
        "type": "object",
        "title": "lane-response/gate-l1",
        "additionalProperties": False,
        "required": ["defects", "flags", "speech_acts"],
        "properties": {
            "defects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["rule", "locus", "expected", "observed", "fix_directive"],
                    "properties": {
                        "rule": {"enum": list(config["veto_rules"])},
                        "locus": _locus_schema(),
                        "expected": {"type": "string", "minLength": 1},
                        "observed": {"type": "string"},
                        "fix_directive": {"type": "string", "minLength": 1},
                    },
                },
            },
            "flags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["rule", "locus", "note"],
                    "properties": {
                        "rule": {"enum": list(config["advisory_rules"])},
                        "locus": _locus_schema(),
                        "note": {"type": "string", "minLength": 1},
                    },
                },
            },
            "speech_acts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["predicate", "locus", "note"],
                    "properties": {
                        "predicate": {"enum": [str(p["id"]) for p in config["predicates"]]},
                        "locus": _locus_schema(),
                        "note": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def _import_time_schema() -> dict:
    try:
        config = l1_config(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),
                           _CONTRACT_AT_IMPORT)
    except StageError:
        return {"type": "object"}
    return payload_schema(config)


_PAYLOAD_SCHEMA = _import_time_schema()
#: 셋 다 **같은** 스키마 객체 — 구동기 `wrapper_schema(task, read_run="gate-l1")` 가 task(변주 id)로 조회한다.
RESPONSE_SCHEMAS: dict[str, dict] = {variant: _PAYLOAD_SCHEMA for variant in VARIANTS}


# ---------------------------------------------------------------------------
# 요청
# ---------------------------------------------------------------------------


def lane_id_for(variant: str, batch: int, attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_RUN}/{variant}/retry-{attempt}/batch-{batch}"
    return f"{LANE_RUN}/{variant}/batch-{batch}"


def _cell(value) -> str:
    return str("" if value is None else value).replace("|", "\\|").replace("\n", " ")


def _predicate_block(config: dict) -> str:
    """술어 3종 — 분류 질문 **원문 그대로**(파일에서 읽어 인라인) + 스코프 조항 + 긍정·부정 예문."""
    lines = [
        f"## 화행 술어 3종 (contracts/lexicon/speech-acts.yaml · version {config['speech_act_version']})",
        "",
        "스코프 조항(재정 R7 원문):",
        "",
        "> " + config["scope"].replace("\n", " "),
        "",
    ]
    for predicate in config["predicates"]:
        lines.append(f"### `{predicate['id']}` — {predicate.get('name', '')}")
        lines.append("")
        lines.append("classification_question (원문):")
        lines.append("")
        lines.append("> " + " ".join(str(predicate.get("classification_question", "")).split()))
        lines.append("")
        lines.append("| positive_examples | negative_examples |")
        lines.append("|---|---|")
        pos = [str(x) for x in predicate.get("positive_examples") or []]
        neg = [str(x) for x in predicate.get("negative_examples") or []]
        for index in range(max(len(pos), len(neg))):
            left = pos[index] if index < len(pos) else ""
            right = neg[index] if index < len(neg) else ""
            lines.append(f"| {_cell(left)} | {_cell(right)} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def build_instructions(*, run_id: str, variant: str, spec_version: int, spec_digest: str, thread_digest: str,
                       config: dict, batch: int, frozen_name: str, index_name: str, thread_name: str) -> str:
    """지시 블록. k 요청에서 **회차 i 표지 줄 하나만** 다르다 … 가 아니라 — 회차 표지도 싣지 않는다(바이트 동일).

    독립 실행의 구별은 좌표(`lane_id`)가 하며 요청서 첫 줄이 그것을 든다. 지시 블록 안에 회차를 적으면 k 요청의
    바이트가 갈리고, 갈리면 「같은 요청의 k 회 독립 실행」이라는 §4.5 의 전제가 문서상으로 깨진다.
    """
    rules_rows = "\n".join(
        f"| `{rule['id']}` | `{'defect' if rule.get('veto') else 'flag'}` | {_cell(rule.get('jurisdiction'))} |"
        for rule in config["rules"]
    )
    blocks = [
        "## 런 표지\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| variant | `{variant}` |\n"
        f"| spec_version | `{spec_version}` |\n"
        f"| spec_digest | `{spec_digest}` |\n"
        f"| thread_digest | `{thread_digest}` |\n"
        f"| k | `{config['k']}` (독립 실행 · 이 요청은 그중 하나 · 좌표 = 요청서 첫 줄) |\n\n"
        "너는 L1 국소 대조 심급이다. 글을 고치지 않는다 — 판정 레코드만 낸다(D8). 파일 시스템을 열지 않는다 · "
        "필요한 것은 전부 「원천 조각」 절에 있다.",
        "## 좌표계\n\n"
        f"`locus = {{tweet, sentence}}` 는 「원천 조각」의 `{index_name}` 의 `tweets[].n` · `sentences[].i` 와 같다"
        "(SPEC §3.3 · §4.2). 판정 대상 = 문장 전건. `narrative_sentences[]` 는 밀수 감사의 우선 표본이다(§3.4). "
        f"주석본 원문은 `{thread_name}`, 재료 정답지는 `{frozen_name}` 이다.",
        "## 규칙\n\n| rule | 산출 | 관할 |\n|---|---|---|\n" + rules_rows + "\n\n"
        "화행 3종은 `speech_acts[]` 로 낸다(술어 id `sa-01`·`sa-02`·`sa-03` · 아래 질문 원문 기준 · 거부권 없음 · 표수만 기록).",
        _predicate_block(config),
        "## 응답\n\n"
        "`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `defects[]` · `flags[]` · `speech_acts[]` 세 배열이며 "
        "해당 없음은 빈 배열이다. `fix_directive` 는 「어디를 · 어느 재료로」 지시문이다. 대체 문장을 쓰면 러너가 "
        "`gate.no-rewrite` 로 응답을 거부한다(§4.7).",
    ]
    return "\n\n".join(blocks) + "\n"


def build_request(*, paths: RunPaths, repo: str, meta: dict, frozen_row: dict, variant: str, thread_text: str,
                  index_text: str, batch: int, config: dict | None = None, attempt: int = 0) -> GateL1LaneRequest:
    """요청 1건(회차 `batch`). `config` 를 주면 계약을 다시 읽지 않는다(k 건이 같은 config 를 쓴다)."""
    config = config or l1_config(repo, paths.contracts[STAGE_ID])
    version = int(frozen_row["spec_version"])
    frozen_path = paths.frozen_spec(version)
    rel = lambda path: os.path.relpath(path, paths.run_root).replace(os.sep, "/")  # noqa: E731
    frozen_name, index_name, thread_name = rel(frozen_path), rel(paths.annotation_index_json(variant)), rel(paths.thread_annotated(variant))
    acts_name = "/".join(SPEECH_ACTS_REL)
    slices = {
        thread_name: thread_text,
        frozen_name: read_text(frozen_path),
        index_name: index_text,
        acts_name: read_text(os.path.join(repo, *SPEECH_ACTS_REL)),
    }
    from ...stages import sha256_bytes  # noqa: PLC0415 - 순환 회피(stages → gate.l1 → stages)

    return GateL1LaneRequest(
        lane_id=lane_id_for(variant, batch, attempt),
        read_run=LANE_RUN,
        task=variant,
        model=config["model"],
        effort=config["effort"],
        prompt_path=config["procedure"],
        instructions=build_instructions(
            run_id=str(meta.get("run_id", "")), variant=variant, spec_version=version,
            spec_digest=str(frozen_row.get("spec_digest", "")), thread_digest=sha256_bytes(thread_text.encode("utf-8")),
            config=config, batch=batch, frozen_name=frozen_name, index_name=index_name, thread_name=thread_name,
        ),
        repo_root=repo,
        slices=slices,
        response_schema=payload_schema(config),
        batch=batch,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, config["model"]),
    )


__all__ = [
    "LANE_RUN",
    "LANE_RUNS",
    "RESPONSE_SCHEMAS",
    "VARIANTS",
    "GateL1LaneRequest",
    "build_instructions",
    "build_request",
    "l1_config",
    "l1_k",
    "lane_id_for",
    "payload_schema",
]
