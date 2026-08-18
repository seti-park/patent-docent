# -*- coding: utf-8 -*-
"""레인 요청·응답의 자료형과 어댑터 프로토콜.

규율 넷(전부 재정 문언의 이행이다).

① **모델·effort 는 요청에 반드시 명시된다.** 빈 값으로는 `LaneRequest` 를 만들 수 없다.
   프롬프트 문구로 소프트 지정하지 않는다(SPEC §7.3 펜 배정 규율 2 · `read.yaml`
   `lane.lane_discipline`).
② **조용한 대체 금지.** 응답은 자기가 **실제로** 돌아간 모델을 적고, 요청과 다르면 러너가
   레인 기록에 `mismatch: true` 를 남기고 결함으로 보고한다(같은 규율 4).
③ **블로킹 금지.** 응답이 없으면 기다리지 않고 `LanePending` 을 던진다. 대기는 오케스트레이터의
   일이며, 러너가 잠들면 체크포인트 무응답이 시간 초과 자동 진행으로 미끄러진다(재정 R8).
④ **시점 결속**(재정 P-12). 요청은 자기 내용의 지문(`input_digest`)을 싣고, 응답은 그 지문을
   반향하며, 러너는 반향이 어긋난 응답을 **거부**한다. 파일 지문 규율(런 결박 · 봉투 결속)의
   레인 왕복 확장이다 — 왕복에 시점이 없으면 "같은 요청에 두 응답"이 존재해도 런이 어느 쪽을
   소비했는지 스스로 증명하지 못한다(2026-08-18 감수 OOS-01·OOS-02 에서 실제로 일어났다).

★ ④가 필드가 아니라 **파생값**인 이유. 요청이 지문을 필드로 들면 그 필드는 요청 내용과 함께
갱신되지 않을 수 있고, 갱신되지 않은 지문은 없느니만 못하다(맞다고 말하는 거짓 증거). 지문은
요청 내용의 함수여야 잊거나 위조할 수 없다.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from jsonschema import Draft202012Validator

REQUEST_JSON = "request.json"
REQUEST_MD = "request.md"
RESPONSE_JSON = "response.json"

# 응답이 요청 지문을 반향하는 자리(응답 JSON 최상위 키).
INPUT_DIGEST_KEY = "input_digest"

# ★ 지문 산정 대상 필드(재정 P-12). 정본 선언 = `read.yaml#lane.round_trip_binding`.
#   `to_dict()` 가 싣는 필드 전량이며 지문 자신만 빠진다 — 즉 **요청 파일을 받은 사람이
#   그 파일만으로 지문을 다시 계산할 수 있다.** `accepted_models` 가 여기 없는 것도 같은
#   이유다: 그 값은 계약에서 파생되어 `request.json` 에 실리지 않으므로, 지문에 넣으면
#   파일만 보고는 재계산이 불가능해져 대조가 코드의 특권이 된다.
BINDING_FIELDS: tuple[str, ...] = (
    "lane_id",
    "read_run",
    "task",
    "model",
    "effort",
    "prompt_path",
    "instructions",
    "slices",
    "response_schema",
    "batch",
)


class LaneContractError(Exception):
    """요청·응답이 계약을 어겼다(필수 필드 부재·스키마 위반·lane_id 불일치)."""


class LaneStaleResponseError(LaneContractError):
    """응답이 **지금 요청이 아닌 다른 요청**에 대한 것이다 — 낡은 응답(재정 P-12).

    ★ 이 예외가 따로 있는 이유. 낡은 응답은 형식이 온전하고 스키마를 통과하며 항목 ID 도
    여전히 유효하다 — 그래서 조립기가 결함을 **결함 그대로** 재번호해 실어 나르고, 그 뒤의
    어떤 결정론 검사도 그것을 잡지 못한다. 탐지 불가한 의미 오염 경로이므로 계약 위반 중에서도
    처분이 다르다: 러너는 이것을 레인 기록에 **거부 행**으로 남긴 뒤 던진다.
    """

    def __init__(self, lane_id: str, expected: str, actual: str) -> None:
        self.lane_id = lane_id
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"레인 응답이 낡았다 — {lane_id} 의 응답이 반향한 입력 지문이 지금 요청의 것과 "
            f"다르다(요청 {expected} ≠ 반향 {actual}). 요청이 갱신된 뒤 옛 응답이 그대로 "
            "남아 있는 상태이며, 그 응답의 항목 ID 는 여전히 유효하므로 조립기가 결함을 "
            "결함 그대로 옮긴다 — 어떤 결정론 검사도 이 오염을 잡지 못한다. 응답을 다시 "
            "받아라(재정 P-12)."
        )


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

    def _binding_body(self) -> dict:
        """지문 산정 대상 그대로의 본문(`BINDING_FIELDS` 순서)."""
        return {name: getattr(self, name) for name in BINDING_FIELDS}

    @property
    def input_digest(self) -> str:
        """요청 내용의 sha256 — 재료 버전과 원문 조각이 함께 들어간다(재정 P-12).

        수확 목록이 바뀌면 `instructions` 가 바뀌고, 다른 원문 조각을 주면 `slices` 가
        바뀌므로 지문이 따라 바뀐다. 그것이 "어느 재료 버전·어느 원문 조각에 대한 요청인가"를
        한 값에 담는 방식이다.

        직렬화가 고정된 이유는 **결정론**이다 — 같은 요청이 두 지문을 가지면 대조가 무너진다.
        정렬 키 · `ensure_ascii=False`(한글을 이스케이프해 표기를 갈라 놓지 않는다) ·
        공백 없는 구분자 셋이 그 고정이며, 이 세 값은 계약이 선언한다
        (`read.yaml#lane.round_trip_binding.canonical_json`).
        """
        blob = json.dumps(
            self._binding_body(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict:
        """`request.json` 본문. 키 순서는 고정이며 값은 그대로 싣는다.

        지문을 함께 싣는 이유: 레인은 `request.json` 만 보고 반향할 값을 알아야 한다. 지문이
        파일에 없으면 레인은 그것을 다시 계산해야 하고, 계산 규약이 갈리는 순간 정직한 레인이
        거부당한다(모델 신원 대조에서 이미 한 번 일어난 실패다).
        """
        body = self._binding_body()
        body[INPUT_DIGEST_KEY] = self.input_digest
        return body


@dataclass(frozen=True)
class LaneResponse:
    """레인 1건의 응답. `model`·`effort` 는 **실제로** 돌아간 값이다.

    지문 둘은 층이 다르다(재정 P-12).

    - `input_digest` = 레인이 **반향한** 요청 지문. 왕복의 시점을 잇는다.
    - `response_digest` = `response.json` **파일 바이트**의 sha256. 런이 소비한 것이 지금
      그 자리에 있는 파일과 같은가를 잇는다. 파일 바이트를 재는 이유는 사람이
      `sha256sum response.json` 으로 곧장 대조할 수 있어야 하기 때문이다 — OOS-02 는 "같은
      요청에 두 응답"이 있었는데 런이 어느 쪽을 읽었는지 증명하지 못한 사건이었다.
    """

    lane_id: str
    model: str
    effort: str
    payload: dict
    input_digest: str
    response_digest: str

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
    lines.append(f"| 입력 지문 | `{request.input_digest}` |")
    lines.append("")
    lines.append("**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는")
    lines.append(
        "`{\"lane_id\": ..., \"model\": ..., \"effort\": ..., "
        "\"input_digest\": ..., \"payload\": {...}}` 이고,"
    )
    lines.append("`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가")
    lines.append("레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 `request.json` 의")
    lines.append("`response_schema` 를 통과해야 하며, 위반은 응답 자체가 거부된다.")
    lines.append("")
    lines.append("**★ 입력 지문 반향(필수 · 재정 P-12).** `input_digest` 에는 위 표의 값을")
    lines.append("**그대로** 적는다. 계산하지 말고 옮겨 적어라 — 이 값은 네가 실제로 읽은 요청이")
    lines.append("어느 판이었는지를 가리키는 시점 표지다. 요청이 갱신되면 지문이 바뀌므로, 옛")
    lines.append("응답을 그대로 두면 러너가 그것을 **낡은 응답으로 거부한다**. 지문이 다르거나")
    lines.append("빠진 응답은 소비되지 않으며, 거부 사실은 레인 기록에 남는다.")
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
    """`response.json` 을 읽고 계약을 대조한다.

    파일을 **바이트로** 읽는 이유는 소비한 그 바이트의 지문을 응답에 실어 보내기 위해서다
    (재정 P-12). 텍스트로 읽고 다시 인코딩해 재면 개행·인코딩 처리에 따라 사람이 손으로 낸
    `sha256sum` 과 갈릴 수 있고, 갈리는 순간 대조 도구로서 죽는다.
    """
    with open(path, "rb") as handle:
        blob = handle.read()
    response_digest = hashlib.sha256(blob).hexdigest()
    try:
        raw = json.loads(blob.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LaneContractError(f"레인 응답이 JSON 이 아니다: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise LaneContractError(f"레인 응답 최상위가 객체가 아니다: {path}")
    missing = [
        key
        for key in ("lane_id", "model", "effort", "payload", INPUT_DIGEST_KEY)
        if key not in raw
    ]
    if missing:
        hint = ""
        if INPUT_DIGEST_KEY in missing:
            # 반향 누락은 "빠뜨린 필드"가 아니라 **시점 결속의 부재**다. 그 뜻을 여기서 밝히지
            # 않으면 레인은 임의의 값을 채워 넣어 통과하려 든다.
            hint = (
                f" — {INPUT_DIGEST_KEY} 는 요청서(request.md · request.json)의 입력 지문을 "
                f"그대로 옮겨 적는 자리다(기대 {request.input_digest}). 반향이 없으면 이 응답이 "
                "어느 판의 요청에 답한 것인지 런이 증명하지 못한다(재정 P-12)"
            )
        raise LaneContractError(
            f"레인 응답에 필수 키가 없다({', '.join(missing)}): {path}{hint}"
        )
    if raw["lane_id"] != request.lane_id:
        raise LaneContractError(
            f"레인 응답의 lane_id 가 요청과 다르다: {raw['lane_id']!r} != {request.lane_id!r}"
        )
    # 지문 대조는 payload 검사보다 **앞**이다. 낡은 응답은 스키마를 온전히 통과하므로, 뒤에
    # 두면 "형식은 옳고 시점만 틀린" 응답이 스키마 통과라는 인상을 남기고 소비 직전까지 간다.
    echoed = str(raw[INPUT_DIGEST_KEY])
    if echoed != request.input_digest:
        raise LaneStaleResponseError(request.lane_id, request.input_digest, echoed)
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
        input_digest=echoed,
        response_digest=response_digest,
    )
