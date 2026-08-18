# -*- coding: utf-8 -*-
"""레인 요청·응답의 자료형과 어댑터 프로토콜.

규율 셋(전부 재정 문언의 이행이다).

① **모델·effort 는 요청에 반드시 명시된다.** 빈 값으로는 `LaneRequest` 를 만들 수 없다.
   프롬프트 문구로 소프트 지정하지 않는다(SPEC §7.3 펜 배정 규율 2 · `read.yaml`
   `lane.lane_discipline`).
② **조용한 대체 금지.** 응답은 자기가 **실제로** 돌아간 모델을 적고, 요청과 다르면 러너가
   레인 기록에 `mismatch: true` 를 남기고 결함으로 보고한다(같은 규율 4).
③ **블로킹 금지.** 응답이 없으면 기다리지 않고 `LanePending` 을 던진다. 대기는 오케스트레이터의
   일이며, 러너가 잠들면 체크포인트 무응답이 시간 초과 자동 진행으로 미끄러진다(재정 R8).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from jsonschema import Draft202012Validator

REQUEST_JSON = "request.json"
REQUEST_MD = "request.md"
RESPONSE_JSON = "response.json"


class LaneContractError(Exception):
    """요청·응답이 계약을 어겼다(필수 필드 부재·스키마 위반·lane_id 불일치)."""


class LanePending(Exception):
    """응답이 아직 없다. 미충족 요청의 `lane_id` 목록과 요청 디렉터리를 들고 있다.

    ★ 이것은 오류가 아니라 **상태**다. 오케스트레이터는 이 예외를 받고 서브에이전트를
    붙인 뒤 같은 스테이지를 다시 부른다. 러너는 기다리지 않는다.
    """

    def __init__(self, pending: list[str], request_dir: str) -> None:
        self.pending = list(pending)
        self.request_dir = request_dir
        super().__init__(
            f"레인 응답 미도착 {len(self.pending)}건: {', '.join(self.pending)} "
            f"(요청 위치 {request_dir})"
        )


@dataclass(frozen=True)
class LaneRequest:
    """레인 1건에 대한 요청.

    `lane_id` 는 요청·응답 파일의 좌표이자 레인 기록의 키다
    (예: `read-a/ground-independent/batch-2`).
    """

    lane_id: str
    read_run: str
    task: str
    model: str
    effort: str
    prompt_path: str
    instructions: str
    slices: dict = field(default_factory=dict)
    response_schema: dict = field(default_factory=dict)
    batch: int = 0
    # ★ 같은 모델의 다른 표기(2026-08-18 통주 실측). 정본 = `read.yaml#lane.model_identity`.
    #   계약이 쓰는 값은 티어 라벨이고 레인이 관측하는 값은 API 식별자다 — 문자열 동등으로
    #   대조하면 **정직한 레인이 벌받는다**. 비어 있으면 문자열 동등으로 되돌아간다(구 동작).
    accepted_models: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # 모델·effort 미지정 요청은 만들어지지 않는다(규율 ①).
        for name in ("lane_id", "read_run", "task", "model", "effort", "prompt_path"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise LaneContractError(
                    f"레인 요청의 {name} 이 비어 있다 — 모델·effort·절차 문서는 "
                    f"요청마다 명시한다(lane_id={self.lane_id!r})"
                )
        if not isinstance(self.response_schema, dict) or not self.response_schema:
            raise LaneContractError(
                f"레인 요청 {self.lane_id} 에 response_schema 가 없다 — 응답을 검사할 "
                "계약이 없으면 무엇이 와도 통과한다"
            )
        if not isinstance(self.batch, int) or self.batch < 0:
            raise LaneContractError(f"레인 요청 {self.lane_id} 의 batch 가 음수·비정수다")

    def to_dict(self) -> dict:
        """`request.json` 본문. 키 순서는 고정이며 값은 그대로 싣는다."""
        return {
            "lane_id": self.lane_id,
            "read_run": self.read_run,
            "task": self.task,
            "model": self.model,
            "effort": self.effort,
            "prompt_path": self.prompt_path,
            "instructions": self.instructions,
            "slices": self.slices,
            "response_schema": self.response_schema,
            "batch": self.batch,
        }


@dataclass(frozen=True)
class LaneResponse:
    """레인 1건의 응답. `model`·`effort` 는 **실제로** 돌아간 값이다."""

    lane_id: str
    model: str
    effort: str
    payload: dict

    def mismatches(self, request: LaneRequest) -> bool:
        """요청과 다른 모델·effort 로 돌았는가(조용한 대체 금지 — 재정 R10 규율 4).

        모델 대조는 **티어 라벨로 정규화한 뒤** 한다. 계약은 라벨(`opus-5`)을 쓰고 레인은
        API 식별자(`claude-opus-5[1m]`)를 관측하므로, 문자열 동등으로 보면 같은 모델이
        대체로 잡힌다 — 2026-08-18 실특허 통주에서 실제로 일어난 일이며, 그때 레인은
        검사를 통과시키려 자기 관측을 고쳐 적어야 했다. 거짓 경보를 내는 검사는 우회되고,
        우회되는 검사는 없는 검사보다 나쁘다. 허용 표기의 정본은 계약이며
        (`contracts/stages/read.yaml#lane.model_identity`) 코드는 그것을 읽을 뿐이다.

        `accepted_models` 가 비면 구 동작(문자열 동등)으로 되돌아간다 — 계약이 라벨 공간을
        선언하지 않은 스테이지에서 코드가 관대해지지 않게 하기 위함이다.
        """
        if request.accepted_models:
            model_ok = self.model in request.accepted_models
        else:
            model_ok = self.model == request.model
        return (not model_ok) or self.effort != request.effort


@runtime_checkable
class LaneAdapter(Protocol):
    """요청 묶음 하나를 보내고 응답 묶음 하나를 받는다(배치 단위)."""

    def dispatch(self, requests: list[LaneRequest]) -> list[LaneResponse]: ...


def render_request_md(request: LaneRequest, repo_root: str) -> str:
    """사람·레인이 그대로 읽는 완성 프롬프트.

    절차 문서(`reader/procedure/*.md`)의 본문을 **인라인으로 실어** 이 파일 하나로 레인이
    작업할 수 있게 한다. 절차를 링크로만 주면 레인마다 열람 여부가 갈리고, 그 순간 두
    독립 실행이 같은 절차를 따랐다는 보장이 사라진다(수렴 검사의 전제).
    """
    procedure_path = os.path.join(repo_root, *request.prompt_path.split("/"))
    try:
        with open(procedure_path, encoding="utf-8") as handle:
            procedure = handle.read()
    except FileNotFoundError as exc:
        raise LaneContractError(f"절차 문서가 없다: {procedure_path}") from exc

    lines: list[str] = []
    lines.append(f"# 레인 요청 — {request.lane_id}")
    lines.append("")
    lines.append("| 항목 | 값 |")
    lines.append("|---|---|")
    lines.append(f"| 독립 실행 | `{request.read_run}` |")
    lines.append(f"| 작업 | `{request.task}` |")
    lines.append(f"| 모델 | `{request.model}` |")
    lines.append(f"| effort | `{request.effort}` |")
    lines.append(f"| 배치 | `{request.batch}` |")
    lines.append(f"| 절차 문서 | `{request.prompt_path}` |")
    lines.append("")
    lines.append("**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는")
    lines.append("`{\"lane_id\": ..., \"model\": ..., \"effort\": ..., \"payload\": {...}}` 이고,")
    lines.append("`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가")
    lines.append("레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 `request.json` 의")
    lines.append("`response_schema` 를 통과해야 하며, 위반은 응답 자체가 거부된다.")
    lines.append("")
    lines.append("## 이 요청의 지시")
    lines.append("")
    lines.append(request.instructions.rstrip())
    lines.append("")
    lines.append("## 원천 조각")
    lines.append("")
    for name in sorted(request.slices):
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append("```text")
        lines.append(str(request.slices[name]).rstrip("\n"))
        lines.append("```")
        lines.append("")
    lines.append("## 절차 (정본 = " + request.prompt_path + ")")
    lines.append("")
    lines.append(procedure.rstrip())
    lines.append("")
    return "\n".join(lines)


def lane_dir(root: str, lane_id: str) -> str:
    return os.path.join(root, *lane_id.split("/"))


def load_response(request: LaneRequest, path: str) -> LaneResponse:
    """`response.json` 을 읽고 계약을 대조한다."""
    with open(path, encoding="utf-8") as handle:
        try:
            raw = json.load(handle)
        except json.JSONDecodeError as exc:
            raise LaneContractError(f"레인 응답이 JSON 이 아니다: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise LaneContractError(f"레인 응답 최상위가 객체가 아니다: {path}")
    missing = [key for key in ("lane_id", "model", "effort", "payload") if key not in raw]
    if missing:
        raise LaneContractError(
            f"레인 응답에 필수 키가 없다({', '.join(missing)}): {path}"
        )
    if raw["lane_id"] != request.lane_id:
        raise LaneContractError(
            f"레인 응답의 lane_id 가 요청과 다르다: {raw['lane_id']!r} != {request.lane_id!r}"
        )
    payload = raw["payload"]
    if not isinstance(payload, dict):
        raise LaneContractError(f"레인 응답 payload 가 객체가 아니다: {path}")
    errors = sorted(
        Draft202012Validator(request.response_schema).iter_errors(payload),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        first = errors[0]
        locus = "/".join(str(step) for step in first.absolute_path) or "$"
        raise LaneContractError(
            f"레인 응답이 response_schema 를 위반한다({request.lane_id} @ {locus}): "
            f"{first.message}"
        )
    return LaneResponse(
        lane_id=raw["lane_id"],
        model=str(raw["model"]),
        effort=str(raw["effort"]),
        payload=payload,
    )
