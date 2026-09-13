# -*- coding: utf-8 -*-
"""계기 요청 n 건(SPEC §5.2 프로브 A/B · 입력 격리 · 답변 규약 · 재정 T69 ⑥ · 재정 P-6).

n 요청은 **바이트 동일**하고 좌표(`probe/<v>[/retry-<k>]/batch-<i>`)로만 갈린다. 요청서에 실리는 것 = 출하 후보 텍스트
(`thread.stripped.md`) + 질문지(세 필드)뿐이다 — 재료 · 블루프린트 · 주석층 · 판정 · 원천은 물리적으로 싣지 않는다(must_not_read 집행).
응답 = `a_restatement[3]` + `b_answers[]`(자기평가 필드 없음 · 스키마). `quoted_span` 이 텍스트의 부분문자열이 아니면 그 답변은
프로브 환각으로 **무효**다(분모 제외 · `not-stated` 로도 세지 않는다).
"""

from __future__ import annotations

import os
import re
import unicodedata

from . import LANE_PROBE, ProbeLaneRequest
from ..lanes.plan import _accepted_models
from ..paths import RunPaths

PROBE_ID_FORMAT = "p{}"
KIND_STATED = "stated"
KIND_NOT_STATED = "not-stated"
INVALID_REASON = "quoted_span-not-substring"
_WS_RE = re.compile(r"\s+")


def lane_id_for(variant: str, batch: int, attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_PROBE}/{variant}/retry-{attempt}/batch-{batch}"
    return f"{LANE_PROBE}/{variant}/batch-{batch}"


def payload_schema(questions: list[dict]) -> dict:
    """레인 몫 = `a_restatement[3]` · `b_answers[]`(질문지 전건 · id enum). 점수·자기평가 필드는 존재하지 않는다(D9)."""
    return {
        "type": "object",
        "title": "lane-response/probe",
        "additionalProperties": False,
        "required": ["a_restatement", "b_answers"],
        "properties": {
            "a_restatement": {"type": "array", "minItems": 3, "maxItems": 3, "items": {"type": "string", "minLength": 1}},
            "b_answers": {
                "type": "array",
                "minItems": len(questions),
                "maxItems": len(questions),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["question_id", "target_material_id", "answer_kind", "answer", "quoted_span"],
                    "properties": {
                        "question_id": {"enum": [q["question_id"] for q in questions]},
                        "target_material_id": {"enum": sorted({q["target_material_id"] for q in questions})},
                        "answer_kind": {"enum": [KIND_STATED, KIND_NOT_STATED]},
                        "answer": {"type": ["string", "null"]},
                        "quoted_span": {"type": ["string", "null"]},
                    },
                    "if": {"properties": {"answer_kind": {"const": KIND_STATED}}},
                    "then": {"properties": {"answer": {"type": "string", "minLength": 1}, "quoted_span": {"type": "string", "minLength": 1}}},
                    "else": {"properties": {"answer": {"type": "null"}, "quoted_span": {"type": "null"}}},
                },
            },
        },
    }


def build_instructions(*, run_id: str, variant: str, input_digest: str, question_set_digest: str, thread_name: str, questions_name: str) -> str:
    """회차 표지를 싣지 않는다 — n 요청의 바이트가 같아야 한다(독립 실행의 구별은 좌표가 한다)."""
    return "\n\n".join([
        "## 런 표지\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| variant | `{variant}` |\n"
        f"| input_digest | `{input_digest}` |\n"
        f"| question_set_digest | `{question_set_digest}` |\n\n"
        "너는 읽기 계기다. 「원천 조각」의 스레드 텍스트와 질문지만 본다. 다른 계기의 답도, 정답지도 없다.",
        "## 과제\n\n"
        f"A. `{thread_name}` 을 읽고 핵심 주장을 **세 문장**으로 다시 말한다(`a_restatement`).\n\n"
        f"B. `{questions_name}` 의 질문마다 답한다(`b_answers`) — 스레드에서 답을 찾았으면 `answer_kind: stated` 와 답과 근거가 된 "
        "**스레드 원문 구간**(`quoted_span` · 글자 그대로 복사)을, 스레드에 없으면 `answer_kind: not-stated` 와 `answer: null` · `quoted_span: null` 을 적는다. "
        "`not-stated` 는 정당한 답이다 — 없는 것을 지어내지 않는다.",
        "## 응답\n\n`payload` 하나를 응답 계약(`response_schema`)대로 낸다.",
    ]) + "\n"


def build_request(*, paths: RunPaths, repo: str, meta: dict, variant: str, thread_text: str, input_digest: str, questions: list[dict],
                  questions_text: str, question_set_digest: str, batch: int, config: dict, attempt: int = 0) -> ProbeLaneRequest:
    lane = config["lanes"][LANE_PROBE]
    thread_name = os.path.relpath(paths.thread_stripped_md(variant), paths.run_root).replace(os.sep, "/")
    questions_name = os.path.relpath(paths.questions_json, paths.run_root).replace(os.sep, "/")
    return ProbeLaneRequest(
        lane_id=lane_id_for(variant, batch, attempt),
        read_run=LANE_PROBE,
        task=variant,
        model=lane["model"],
        effort=lane["effort"],
        prompt_path=lane["procedure"],
        instructions=build_instructions(run_id=str(meta.get("run_id", "")), variant=variant, input_digest=input_digest,
                                        question_set_digest=question_set_digest, thread_name=thread_name, questions_name=questions_name),
        repo_root=repo,
        slices={thread_name: thread_text, questions_name: questions_text},
        response_schema=payload_schema(questions),
        batch=batch,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, lane["model"]),
    )


def _fold(text: str) -> str:
    return _WS_RE.sub(" ", unicodedata.normalize("NFKC", text)).strip()


def is_substring(span: str, text: str) -> bool:
    """결정론 — 원문 그대로 부분문자열이거나, 공백 접기(NFKC + 연속 공백 1) 뒤 부분문자열. 그 밖은 환각이다."""
    if not span:
        return False
    return span in text or _fold(span) in _fold(text)


def invalid_answers(report: dict, text: str) -> list[dict]:
    """`stated` 인데 `quoted_span` 이 텍스트의 부분문자열이 아닌 답변 — `{probe_id, question_id, reason}`."""
    out: list[dict] = []
    for answer in report.get("b_answers") or []:
        if answer.get("answer_kind") == KIND_STATED and not is_substring(str(answer.get("quoted_span") or ""), text):
            out.append({"probe_id": str(report.get("probe_id")), "question_id": str(answer.get("question_id")), "reason": INVALID_REASON})
    return out


def build_report(*, index: int, response, lane: dict, input_digest: str, question_set_digest: str, produced_at: str) -> dict:
    """레인 payload + 러너 기입(`probe_id` · `model`(관측) · 지문 2 · `produced_at`) → probe-report/v0."""
    payload = response.payload
    return {
        "schema": "probe-report/v0",
        "probe_id": PROBE_ID_FORMAT.format(index),
        "model": {"vendor": lane["vendor"], "model": str(response.model), "effort": str(response.effort)},
        "input_digest": input_digest,
        "question_set_digest": question_set_digest,
        "a_restatement": [str(s) for s in payload["a_restatement"]],
        "b_answers": [dict(a) for a in payload["b_answers"]],
        "produced_at": produced_at,
    }


__all__ = ["INVALID_REASON", "KIND_NOT_STATED", "KIND_STATED", "PROBE_ID_FORMAT", "build_instructions", "build_report", "build_request",
           "invalid_answers", "is_substring", "lane_id_for", "payload_schema"]
