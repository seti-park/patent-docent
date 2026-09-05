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
④ **시점 결속**(재정 P-12 · 재정 2026-08-19 S4). 요청은 자기 내용의 지문(`input_digest`)을
   싣고, 응답은 그 지문을 반향하며, 러너는 반향이 어긋난 응답을 **거부**한다. 파일 지문 규율
   (런 결박 · 봉투 결속)의 레인 왕복 확장이다 — 왕복에 시점이 없으면 "같은 요청에 두 응답"이
   존재해도 런이 어느 쪽을 소비했는지 스스로 증명하지 못한다(2026-08-18 감수 OOS-01·OOS-02
   에서 실제로 일어났다).

★ ④가 필드가 아니라 **파생값**인 이유. 요청이 지문을 필드로 들면 그 필드는 요청 내용과 함께
갱신되지 않을 수 있고, 갱신되지 않은 지문은 없느니만 못하다(맞다고 말하는 거짓 증거). 지문은
요청 내용의 함수여야 잊거나 위조할 수 없다.

★ **지문이 무엇의 함수인가**(재정 2026-08-19 S4 — 규격 개정). 구 판은 요청 필드 10개의 정규
JSON 을 쟀고, 그중 절차 문서는 `prompt_path` 라는 **경로 문자열**로만 들어갔다. 그래서 절차
문서 본문이 바뀌어도 지문이 그대로였고, **서로 다른 실제 프롬프트가 같은 지문을 공유**했다
(2026-08-19 감수 D 실측: 보관 요청문 29,046 B ↔ 같은 필드로 재렌더한 39,152 B, 지문은 동일).
그 창으로 구 응답이 통과한다. 지금 지문이 재는 것은 **렌더된 요청서 본문 전체**이며 지문 행
자신만 빠진다 — 레인이 실제로 읽는 그 바이트가 곧 지문의 원본이고, 파일 하나만 있으면
제3자가 셸 한 줄로 재계산한다:

    grep -v '^| 입력 지문 |' request.md | sha256sum
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from jsonschema import Draft202012Validator

REQUEST_JSON = "request.json"
REQUEST_MD = "request.md"
RESPONSE_JSON = "response.json"

LANE_ID_PATTERN = re.compile(
    r"^(?P<read_run>[a-z0-9]+(?:-[a-z0-9]+)*)/"
    r"(?P<task>[a-z0-9]+(?:-[a-z0-9]+)*)(?:/retry-(?P<retry>[1-9][0-9]*))?/"
    r"batch-(?P<batch>0|[1-9][0-9]*)$"
)
# 정본 = contracts/schemas/convergence.schema.json#$defs.read_run. 다리 시험이 상등을 고정한다.
READ_RUNS: tuple[str, ...] = ("read-a", "read-b")
# 정본 = contracts/stages/read.yaml#lane.sub_lanes[].id. 같은 다리 시험이 상등을 고정한다.
LANE_TASKS: tuple[str, ...] = (
    "decompose",
    "ground-independent",
    "ground-dependent",
    "synthesize",
)

# 응답이 요청 지문을 반향하는 자리(응답 JSON 최상위 키).
INPUT_DIGEST_KEY = "input_digest"

# ★ `request.json` 이 싣는 필드 목록. **지문 산정 대상 목록이 아니다**(재정 2026-08-19 S4).
#
#   이름이 구 판(BINDING_FIELDS [폐기])에서 바뀐 이유가 그 구별이다 — 지문의 규격은 이제 이
#   튜플이 아니라 **렌더된 요청서 본문**(`render_request_body`)이 정한다. 이름을 그대로 두면
#   다음 사람이 지문 규격을 여기서 읽고, 실제 결속과 어긋난 이해를 계약으로 착각한다.
#
#   `accepted_models` 가 여기 없는 이유는 그대로다: 계약에서 파생되는 값이라 요청 파일에
#   실리지 않으며(따라서 요청서 본문에도 없고 지문에도 들어가지 않는다), 파일에 없는 값을
#   지문에 넣으면 대조가 코드의 특권이 된다(총괄 재량 H2 의 원칙).
REQUEST_JSON_FIELDS: tuple[str, ...] = (
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

# ★ 요청서 표의 지문 행 접두. 지문 산정에서 **이 접두로 시작하는 줄만** 빠진다
#   (재정 2026-08-19 S4). 값이 자기 자신을 재는 순환을 끊는 유일한 예외이며, 예외가 하나뿐인
#   덕에 제3자가 `grep -v` 한 줄로 같은 원본을 복원할 수 있다.
DIGEST_ROW_PREFIX = "| 입력 지문 |"

# 지문 행이 들어가는 자리 = 이 행 **바로 다음**. 삽입은 순수한 한 줄 삽입이어야 하며(다른
# 바이트를 함께 건드리면 위 `grep -v` 복원이 성립하지 않는다) 앵커가 사라지면 렌더가 조용히
# 바뀐 것이므로 계약 위반으로 던진다.
DIGEST_ROW_ANCHOR = "| 절차 문서 |"


class LaneContractError(Exception):
    """요청·응답이 계약을 어겼다(필수 필드 부재·스키마 위반·lane_id 불일치)."""


def _check_lane_id_vocabulary(lane_id: str) -> re.Match[str]:
    """`lane_id`의 계약 형태와 read_run·task 정본 집합 소속을 검사한다."""
    match = LANE_ID_PATTERN.fullmatch(lane_id) if isinstance(lane_id, str) else None
    if match is None:
        raise LaneContractError(
            "lane_id 가 계약 어휘(read.yaml#lane.lane_id_vocabulary.form)를 벗어난다 — "
            f"어휘 위반(형태) · 재정 T4 · lane_id={lane_id!r}"
        )
    if match["read_run"] not in READ_RUNS or match["task"] not in LANE_TASKS:
        raise LaneContractError(
            "lane_id 가 계약 어휘의 정본 집합을 벗어난다 — 어휘 위반(소속) · "
            "read_run/task 가 정본 집합 밖 · 재정 T4 · "
            f"lane_id={lane_id!r} · read_run={match['read_run']!r} · task={match['task']!r}"
        )
    return match


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

    형태와 read_run·task의 정본 집합 소속을 보고 필드 정합은 보지 않는다.
    예컨대 `read-b/decompose/batch-0`에 `task=synthesize`를 짝지은 요청은 통과한다.

    ★ `repo_root` 가 필수인 이유(재정 2026-08-19 S4). 요청서는 `prompt_path` 가 가리키는 절차
    문서의 **본문을 인라인**하며 지문은 그 본문의 함수다. 따라서 **어느 절차 트리의 본문을
    싣는지가 정해지지 않으면 요청이 완전히 지정되지 않는다** — 경로 문자열만으로는 같은
    요청이 트리마다 다른 프롬프트가 되고, 구 판에서 그 차이가 지문에 닿지 않아 서로 다른
    프롬프트가 같은 지문을 공유했다. 이 값은 `request.json` 에 싣지 않는다: 환경 경로일 뿐
    이고, 그것이 만든 **본문**은 `request.md` 가 든다. 같은 절차 본문이면 두 리포에서 같은
    지문이 나오는 것이 옳은 동작이다(지문은 본문의 함수이지 경로의 함수가 아니다).
    """

    lane_id: str
    read_run: str
    task: str
    model: str
    effort: str
    prompt_path: str
    instructions: str
    repo_root: str = ""
    slices: dict = field(default_factory=dict)
    response_schema: dict = field(default_factory=dict)
    batch: int = 0
    # ★ 같은 모델의 다른 표기(2026-08-18 통주 실측). 정본 = `read.yaml#lane.model_identity`.
    #   계약이 쓰는 값은 티어 라벨이고 레인이 관측하는 값은 API 식별자다 — 문자열 동등으로
    #   대조하면 **정직한 레인이 벌받는다**. 비어 있으면 문자열 동등으로 되돌아간다(구 동작).
    accepted_models: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # 모델·effort 미지정 요청은 만들어지지 않는다(규율 ①).
        for name in (
            "lane_id",
            "read_run",
            "task",
            "model",
            "effort",
            "prompt_path",
            # 절차 트리도 필수다 — 어느 절차 본문을 인라인하는지가 요청의 일부다(재정 S4).
            "repo_root",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise LaneContractError(
                    f"레인 요청의 {name} 이 비어 있다 — 모델·effort·절차 문서·절차 트리는 "
                    f"요청마다 명시한다(lane_id={self.lane_id!r})"
                )
        if not isinstance(self.response_schema, dict) or not self.response_schema:
            raise LaneContractError(
                f"레인 요청 {self.lane_id} 에 response_schema 가 없다 — 응답을 검사할 "
                "계약이 없으면 무엇이 와도 통과한다"
            )
        if not isinstance(self.batch, int) or self.batch < 0:
            raise LaneContractError(f"레인 요청 {self.lane_id} 의 batch 가 음수·비정수다")
        _check_lane_id_vocabulary(self.lane_id)

    def _request_json_body(self) -> dict:
        """`request.json` 본문 그대로(`REQUEST_JSON_FIELDS` 순서)."""
        return {name: getattr(self, name) for name in REQUEST_JSON_FIELDS}

    @property
    def input_digest(self) -> str:
        """**렌더된 요청서 본문**의 sha256 — 지문 행 자신만 빠진다(재정 2026-08-19 S4).

        재료 버전(`instructions` 의 수확 목록)도 원문 조각(`slices`)도 절차 문서 **본문**도
        전부 그 본문에 실려 있으므로, 무엇 하나가 바뀌면 지문이 따라 바뀐다. 구 판이 절차
        본문을 경로 문자열로만 들어 서로 다른 프롬프트가 같은 지문을 공유했던 창이 여기서
        닫힌다.

        값이 **파일의 함수**라는 점이 규격의 요점이다 — 요청서 하나만 받은 제3자가
        `grep -v '^| 입력 지문 |' request.md | sha256sum` 으로 같은 값을 낸다. 파일에 실리지
        않는 값을 지문에 넣으면 대조가 코드의 특권이 된다(총괄 재량 H2 의 원칙).
        """
        return compute_input_digest(render_request_body(self, self.repo_root))

    def to_dict(self) -> dict:
        """`request.json` 본문. 키 순서는 고정이며 값은 그대로 싣는다.

        지문을 함께 싣는 이유: 레인은 `request.json` 만 보고 반향할 값을 알아야 한다. 지문이
        파일에 없으면 레인은 그것을 다시 계산해야 하고, 계산 규약이 갈리는 순간 정직한 레인이
        거부당한다(모델 신원 대조에서 이미 한 번 일어난 실패다).
        """
        body = self._request_json_body()
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


def _resolve_repo_root(request: LaneRequest, repo_root: str | None) -> str:
    """렌더가 쓸 절차 트리를 정한다 — 요청이 결속한 트리와 다르면 던진다(재정 S4).

    두 값이 갈리면 **파일에 적힌 지문과 그 파일 본문이 어긋난다**: 지문은 요청이 든
    `repo_root` 로 계산되는데 본문은 다른 트리의 절차를 실어 나르기 때문이다. 그 산출은
    제3자 재계산에서 즉시 불일치를 내며, 그때 의심받는 것은 렌더가 아니라 응답이다.
    """
    if repo_root is None or not str(repo_root).strip():
        return request.repo_root
    if os.path.realpath(repo_root) != os.path.realpath(request.repo_root):
        raise LaneContractError(
            f"요청 {request.lane_id} 이 결속한 절차 트리와 다른 트리로 렌더하려 한다 — "
            f"요청 {request.repo_root} ≠ 렌더 {repo_root}. 지문은 요청이 결속한 트리의 절차 "
            "본문으로 계산되므로, 다른 트리로 렌더하면 파일이 든 지문과 본문이 갈린다"
            "(재정 2026-08-19 S4)"
        )
    return request.repo_root


def render_request_body(request: LaneRequest, repo_root: str | None = None) -> str:
    """지문 행이 **없는** 요청서 본문 — 절차 문서 본문을 인라인한 완성 프롬프트다.

    이것이 지문의 원본이다(재정 2026-08-19 S4). 사람·레인이 읽는 파일(`render_request_md`)은
    여기에 지문 행 한 줄만 끼워 넣은 것이며, 그래서 그 한 줄을 다시 지우면 정확히 이 문자열이
    복원된다.

    절차 문서를 **인라인으로 싣는** 이유는 그대로다 — 이 파일 하나로 레인이 작업할 수 있어야
    한다. 절차를 링크로만 주면 레인마다 열람 여부가 갈리고, 그 순간 두 독립 실행이 같은 절차를
    따랐다는 보장이 사라진다(수렴 검사의 전제). 구 판의 결함은 그렇게 실어 놓고도 **지문은
    경로만 재고 있었다**는 것이다.

    `response_schema` 도 여기 싣는다. 요청 필드 전량이 본문에 있어야 "본문의 지문 = 요청의
    지문"이 성립하고, 덧붙여 레인이 응답 계약을 보려고 `request.json` 을 따로 열 필요가 없어
    진다(자기완결 — 재정 2026-08-19 Q8 ①과 같은 취지).
    """
    root = _resolve_repo_root(request, repo_root)
    procedure_path = os.path.join(root, *request.prompt_path.split("/"))
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
    lines.append(f"{DIGEST_ROW_ANCHOR} `{request.prompt_path}` |")
    lines.append("")
    lines.append("**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는")
    lines.append(
        "`{\"lane_id\": ..., \"model\": ..., \"effort\": ..., "
        "\"input_digest\": ..., \"payload\": {...}}` 이고,"
    )
    lines.append("`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가")
    lines.append("레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 아래 응답 계약을")
    lines.append("통과해야 하며, 위반은 응답 자체가 거부된다.")
    lines.append("")
    lines.append("**★ 입력 지문 반향(필수 · 재정 P-12).** `input_digest` 에는 위 표의 값을")
    lines.append("**그대로** 적는다. 계산하지 말고 옮겨 적어라 — 이 값은 네가 실제로 읽은 요청이")
    lines.append("어느 판이었는지를 가리키는 시점 표지다. 요청이 갱신되면 지문이 바뀌므로, 옛")
    lines.append("응답을 그대로 두면 러너가 그것을 **낡은 응답으로 거부한다**. 지문이 다르거나")
    lines.append("빠진 응답은 소비되지 않으며, 거부 사실은 레인 기록에 남는다.")
    lines.append("")
    lines.append("**★ 지문의 규격(재정 2026-08-19 S4).** 위 표의 값은 **이 요청서 본문 전체**의")
    lines.append("sha256 이며 지문 행 자신만 빠진다. 절차 문서 본문도 원문 조각도 여기 실려 있으므로")
    lines.append("전부 지문에 들어간다. 이 파일만으로 다시 계산할 수 있다 —")
    lines.append("`grep -v '^| 입력 지문 |' request.md | sha256sum`.")
    lines.append("")
    lines.append("## 응답 계약 (response_schema)")
    lines.append("")
    lines.append("```json")
    lines.append(
        json.dumps(request.response_schema, ensure_ascii=False, sort_keys=True, indent=2)
    )
    lines.append("```")
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

    body = "\n".join(lines)

    # ★ 지문 행 접두와 충돌하는 줄이 본문에 있으면 제외 규칙이 **한 줄을 지목하지 못한다** —
    #   제3자의 `grep -v` 는 그 줄까지 지우므로 재계산이 갈린다. 조용히 갈리게 두면 정직한
    #   레인이 위조 의심을 받으므로, 여기서 크게 실패한다(재정 2026-08-19 S4).
    #   판정을 **join 뒤의 실제 줄**로 하는 이유: 지시문·원문 조각·응답 계약은 여러 줄을 담은
    #   한 덩어리로 들어오므로, 덩어리 단위로 보면 그 안쪽 줄의 충돌을 놓친다.
    collision = [line for line in body.split("\n") if line.startswith(DIGEST_ROW_PREFIX)]
    if collision:
        raise LaneContractError(
            f"요청 본문에 지문 행과 같은 접두({DIGEST_ROW_PREFIX})로 시작하는 줄이 있다 — "
            f"제외 규칙이 한 줄을 지목하지 못해 제3자 재계산이 갈린다: {collision[0][:80]!r} "
            f"(lane_id={request.lane_id!r})"
        )
    return body


def digest_source(rendered: str) -> str:
    """렌더된 요청서에서 지문 행을 지운 나머지 = 지문의 원본(재정 2026-08-19 S4).

    셸 `grep -v '^| 입력 지문 |'` 와 **같은 뜻**이어야 한다 — 그것이 이 규격의 존재 이유이기
    때문이다(파일만 받은 사람이 코드 없이 재계산한다). 그래서 접두로 시작하는 줄을 **전부**
    지우며, 그런 줄이 둘 이상 생길 수 없다는 보장은 `render_request_body` 가 든다.
    """
    kept = [line for line in rendered.split("\n") if not line.startswith(DIGEST_ROW_PREFIX)]
    return "\n".join(kept)


def compute_input_digest(body: str) -> str:
    """요청서 본문(지문 행 제외)의 sha256. 사람이 손으로 낸 `sha256sum` 과 같아야 한다."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def render_request_md(request: LaneRequest, repo_root: str | None = None) -> str:
    """사람·레인이 그대로 읽는 완성 프롬프트 = 본문 + 지문 행 한 줄.

    삽입은 **순수한 한 줄 삽입**이다. 다른 바이트를 함께 건드리면
    `compute_input_digest(digest_source(render_request_md(r)))  ==  r.input_digest` 가 깨지고,
    그 불변식이 깨지는 순간 "파일만으로 재계산한다"는 규격이 거짓이 된다(재정 2026-08-19 S4).
    """
    body = render_request_body(request, repo_root)
    row = f"{DIGEST_ROW_PREFIX} `{compute_input_digest(body)}` |"
    lines = body.split("\n")
    for index, line in enumerate(lines):
        if line.startswith(DIGEST_ROW_ANCHOR):
            lines.insert(index + 1, row)
            break
    else:
        raise LaneContractError(
            f"요청서에 지문 행의 앵커({DIGEST_ROW_ANCHOR})가 없다 — 렌더가 바뀌었고 지문 행이"
            f" 설 자리를 잃었다(lane_id={request.lane_id!r})"
        )
    return "\n".join(lines)


def lane_dir(root: str, lane_id: str) -> str:
    """T4 어휘·디렉터리 포함을 강제한다. 구 판은 맨 `os.path.join`이었다."""
    _check_lane_id_vocabulary(lane_id)
    path = os.path.join(root, *lane_id.split("/"))
    root_real = os.path.realpath(root)
    if not os.path.realpath(path).startswith(root_real + os.sep):
        raise LaneContractError(
            "lane_id 가 레인 루트 밖을 가리킨다 — 루트 밖(디렉터리) · "
            f"재정 T4 · lane_id={lane_id!r} · root={root!r}"
        )
    return path


def lane_file(root: str, lane_id: str, name: str) -> str:
    """말단까지 루트 포함을 검사한다(B-02).

    경로를 열거나 쓰기 직전에 부른다. 검사와 I/O 사이의 교체는 안 보는 축이다(자문 ⓓ).
    """
    directory = lane_dir(root, lane_id)
    if not isinstance(name, str) or not name or "/" in name or ".." in name:
        raise LaneContractError(
            f"레인 아티팩트 이름이 계약 어휘를 벗어난다 — 어휘 위반 · name={name!r}"
        )
    path = os.path.join(directory, name)
    root_real = os.path.realpath(root)
    if not os.path.realpath(path).startswith(root_real + os.sep):
        raise LaneContractError(
            "레인 아티팩트가 레인 루트 밖을 가리킨다 — 루트 밖(말단) · "
            f"재정 T4 · lane_id={lane_id!r} · name={name!r} · root={root!r}"
        )
    return path


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
