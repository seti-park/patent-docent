#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""READ 부분 런 구동기 — `run_kind: partial` · `partial_until: freeze` (재정 T60 집행) + 런 -3 연장·설계(재정 T64).

설계 정본 = `docs/decisions/D-20260913-03-read-run-2-driver.md`(§3 명령 11 · §4 레인 호출 규격 ·
§5 순서 · §9 성공 판정). 재정 좌표 = T60(구동 = M1a 직접 · 전 레인 CLI · 결정론 파이썬) ·
T58 ②(좌석) · T59(봉투 `review_adjudicated[]`) · T64 ①②(연장 봉투 `extend` · 설계 스테이지 `design`).

역할 경계.

- 엔진(`engine/stages/source.py#run` · `read.py#run` · `freeze.py#run`)과 파일 어댑터
  (`engine/lanes/file_adapter.py`)가 이끈다. 구동기는 엔진이 `LanePending` 으로 낸 대기 좌표를
  `claude -p` 서브프로세스 한 번씩으로 채우고, 응답 파일을 쓰고, 영수증을 남긴다.
- 구동기는 판단하지 않는다. 실패는 비영 종료 코드와 사유 한 줄이다. 자동 재시도는 없다 —
  실패한 좌표는 다음 `step` 이 같은 자리를 다시 대기로 낸다(좌표당 호출 상한 3).
- 쓰는 곳 = 런 작업장(엔진이 쓴다) · 봉투 두 종(구동기가 쓴다) · `<worktree>/evidence/**`
  (구동기 영수증). 그 밖에는 쓰지 않는다.

종료 코드(재정 T40 구동기 어휘 재사용).

| 코드 | 뜻 |
|---|---|
| 0 | 정상 진행 또는 종결 |
| 10 | 대기 좌표가 남았다 — 다시 `step` |
| 11 | 조기 수렴 상신 축 미달 — `continue` 가능 |
| 12 | 조기 수렴 봉투 불가 대기 — 사람이 본다 |
| 13 | 종결 실패(엔진 판정 halt·escalate·reject-upstream) |
| 14 | 판정 불능 · 증거 기록 실패(io_fault · modelUsage 부재 · 첫 좌표 실호출 불일치) |
| 15 | 좌표 호출 상한 초과 |
| 20 | CP1 대기 — `cp1` · `approve` 차례 |
| 2 | 인자 · 환경 오류 |

`extend` 는 `15-frozen/extension-v<N>.md`(extension-envelope/v0)를 쓰고 `run.yaml#partial_until` 을
옮긴다 · `design` 은 `engine/stages/design.py#run` 을 재진입(상한 4)하며 대기 좌표를 같은 `call_lane`
으로 채운다(0 · 10 · 13 · 14 · 15).

실행기는 주입 가능한 호출체다. 기본 = 실제 `claude` 서브프로세스. 시험은 스텁을 넣는다.
이 모듈은 표준 라이브러리와 리포 모듈만 쓴다.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Callable

_HERE = os.path.dirname(os.path.realpath(__file__))
_DEFAULT_REPO = os.path.dirname(_HERE)
if _DEFAULT_REPO not in sys.path:
    sys.path.insert(0, _DEFAULT_REPO)

import yaml  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

from engine import gitpin  # noqa: E402
from engine.lanes.contract import (  # noqa: E402
    REQUEST_JSON,
    REQUEST_MD,
    RESPONSE_JSON,
    LaneContractError,
    LanePending,
    lane_dir,
    lane_file,
)
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.lanes.plan import RESPONSE_SCHEMAS  # noqa: E402
from engine.paths import PathContractError, RunPaths, load_stage_contract, run_kinds_contract  # noqa: E402
from engine.stages import StageError, freeze as freeze_stage  # noqa: E402
from engine.stages import design as design_stage  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402
from engine.stages import source as source_stage  # noqa: E402
from reader.lib.rules import Rules  # noqa: E402

# ---------------------------------------------------------------------------
# 상수 — 설계 §3 · §4 의 값. 값 공간을 바꾸는 판단은 상신 사항이다(규율 11).
# ---------------------------------------------------------------------------

EXIT_OK = 0
EXIT_PENDING = 10
EXIT_CONTINUE_POSSIBLE = 11
EXIT_GATE_WAIT = 12
EXIT_TERMINAL_FAIL = 13
EXIT_UNDECIDABLE = 14
EXIT_CALL_CAP = 15
EXIT_CP1_WAIT = 20
EXIT_USAGE = 2

RUN_KIND = "partial"
PARTIAL_UNTIL = "freeze"
STEP_REENTRY_CAP = 12
CALL_CAP_PER_LANE = 3
WALL_CLOCK_SECONDS = 900
STDIN_MAX_BYTES = 10 * 1024 * 1024
LANE_ENV = {"MEMORY_HOOKS": "off", "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "128000"}
DEFAULT_WORKTREE_ROOT_REL = ".worktrees"
DEFAULT_INIT_REF = "main"
CP1_CHECKPOINT = "material_approval"
CONTINUE_CHECKPOINT = read_stage.CONTINUE_CHECKPOINT
ESCALATION_AXIS = read_stage.PHASE_GATE_ESCALATION
APPROVAL_SCHEMA_REL = freeze_stage.APPROVAL_SCHEMA
APPROVAL_NAME_RE = re.compile(r"^approval-v([1-9][0-9]*)\.md$")
STDERR_TAIL_CHARS = 2000
REVIEW_SECTION_LINES = 12
COMMANDS = ("init", "step", "lanes", "rewrap", "continue", "cp1", "approve", "freeze", "seal", "extend", "design")
DESIGN_REENTRY_CAP = 4
EXTENSION_SCHEMA_REL = ("contracts", "schemas", "extension-envelope.schema.json")
EXTENSION_NAME_RE = re.compile(r"^extension-v([1-9][0-9]*)\.md$")
# 법 트리 더러움 판정에서 제외하는 접두(런 작업장 · 영수증 · 결박 worktree — 결박 기제 자신의 생성물).
LAW_DIRTY_EXEMPT_PREFIXES = ("runs/", "evidence/", ".worktrees/")
# 작업 스키마 조회 사전 — plan.py(READ 4 작업) + design.py(설계 1 작업). 값은 각 모듈의 상수 그대로(복사 아님).
TASK_SCHEMAS = {**RESPONSE_SCHEMAS, **design_stage.RESPONSE_SCHEMAS}
MANIFEST_BASENAME = "MANIFEST-sha256.txt"


class DriverExit(Exception):
    """종료 코드와 사유 한 줄. `main` 이 받아서 stderr 에 적고 코드를 돌려준다."""

    def __init__(self, code: int, reason: str) -> None:
        self.code = code
        self.reason = reason
        super().__init__(reason)


# ---------------------------------------------------------------------------
# 실행기 — `claude -p` 서브프로세스 한 번. 시험은 같은 서명의 스텁을 넣는다.
# ---------------------------------------------------------------------------


@dataclass
class ExecResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    duration_ms: int


Executor = Callable[[list[str], bytes, dict, int], ExecResult]


def claude_executor(argv: list[str], stdin: bytes, env: dict, timeout: int) -> ExecResult:
    """실제 CLI 호출. 벽시계 상한을 넘기면 프로세스를 죽이고 `timed_out` 으로 돌려준다."""
    started = _dt.datetime.now(_dt.timezone.utc)
    try:
        # `_LANE_CWD` = 중립 작업 디렉터리(프로젝트 `.claude/`·CLAUDE.md 가 없는 빈 곳) — 환경 변수가 아니라
        # 실행기 전달 인자이며 자식 프로세스 환경에서는 뺀다. 스텁 실행기는 무시한다.
        env = dict(env)
        cwd = env.pop("_LANE_CWD", None)
        if cwd:
            os.makedirs(cwd, exist_ok=True)
        proc = subprocess.run(
            argv, input=stdin, env=env, capture_output=True, timeout=timeout, check=False, cwd=cwd
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = _dt.datetime.now(_dt.timezone.utc) - started
        return ExecResult(
            returncode=-1,
            stdout=exc.stdout or b"",
            stderr=(exc.stderr or b"") + b"\n[driver] wall clock exceeded",
            timed_out=True,
            duration_ms=int(elapsed.total_seconds() * 1000),
        )
    except OSError as exc:
        raise DriverExit(EXIT_USAGE, f"claude 실행 불가: {exc}") from exc
    elapsed = _dt.datetime.now(_dt.timezone.utc) - started
    return ExecResult(
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        timed_out=False,
        duration_ms=int(elapsed.total_seconds() * 1000),
    )


def stub_executor_from_dir(stub_dir: str) -> Executor:
    """CLI 옵션 `--executor stub` 의 실행기. `<evidence>/stub-responses/<safe>.json` 이 있으면
    그 파일(레인 출력 봉투 전체)을 결과로 되돌리고, 없으면 `is_error` 결과를 낸다.
    실제 모델을 부르지 않는다. 시험 전용이다."""

    def run(argv: list[str], stdin: bytes, env: dict, timeout: int) -> ExecResult:
        lane_id = _lane_id_from_request_md(stdin.decode("utf-8", errors="replace"))
        model = argv[argv.index("--model") + 1] if "--model" in argv else ""
        candidate = os.path.join(stub_dir, safe_lane_name(lane_id or "unknown") + ".json")
        if not os.path.isfile(candidate):
            body = {"type": "result", "is_error": True, "result": f"stub: no fixture for {lane_id}"}
            return ExecResult(1, _json_bytes(body), b"stub: no fixture", False, 0)
        with open(candidate, encoding="utf-8") as handle:
            structured = json.load(handle)
        body = {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "num_turns": 1,
            "duration_ms": 0,
            "total_cost_usd": 0.0,
            "session_id": "stub",
            "modelUsage": {model: {"inputTokens": 0, "outputTokens": 1}},
            "structured_output": structured,
        }
        return ExecResult(0, _json_bytes(body), b"", False, 0)

    return run


def _lane_id_from_request_md(text: str) -> str | None:
    first = text.split("\n", 1)[0]
    prefix = "# 레인 요청 — "
    return first[len(prefix):].strip() if first.startswith(prefix) else None


# ---------------------------------------------------------------------------
# 경로 · 문맥
# ---------------------------------------------------------------------------


@dataclass
class Context:
    """한 런의 자리들. `law` = 계약·절차를 읽는 트리(기본 = 런의 worktree)."""

    run_id: str
    repo: str
    worktree: str
    run_root: str
    evidence: str
    law: str
    executor: Executor
    dry_run: bool = False
    out: Callable[[str], None] = field(default=lambda line: print(line))

    @property
    def calls_dir(self) -> str:
        return os.path.join(self.evidence, "calls")

    @property
    def schemas_dir(self) -> str:
        return os.path.join(self.evidence, "schemas")

    def paths(self) -> RunPaths:
        try:
            return RunPaths(self.run_root, self.law)
        except PathContractError as exc:
            raise DriverExit(EXIT_USAGE, f"계약 트리 불량({self.law}): {exc}") from exc


def build_context(args: argparse.Namespace, executor: Executor | None) -> Context:
    repo = os.path.realpath(args.repo or _DEFAULT_REPO)
    worktree_root = os.path.realpath(
        args.worktree_root or os.path.join(repo, DEFAULT_WORKTREE_ROOT_REL)
    )
    worktree = os.path.join(worktree_root, args.run_id)
    run_root = os.path.realpath(args.run_root) if args.run_root else os.path.join(
        worktree, "runs", args.run_id
    )
    law = worktree if not args.run_root else repo
    evidence = os.path.realpath(args.evidence_dir) if args.evidence_dir else os.path.join(
        worktree, "evidence"
    )
    if executor is None:
        if args.executor == "stub":
            executor = stub_executor_from_dir(os.path.join(evidence, "stub-responses"))
        else:
            executor = claude_executor
    return Context(
        run_id=args.run_id,
        repo=repo,
        worktree=worktree,
        run_root=run_root,
        evidence=evidence,
        law=law,
        executor=executor,
        dry_run=bool(args.dry_run),
    )


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def _json_bytes(payload) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _write_bytes(path: str, blob: bytes) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(blob)


def _sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return _sha256_bytes(handle.read())


def _load_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_lane_name(lane_id: str) -> str:
    """`read-a/decompose/batch-0` → `read-a__decompose__batch-0`(경로 안전형)."""
    return lane_id.replace("/", "__")


def api_id_for_label(law: str, label: str) -> str:
    """계약 `read.yaml#lane.model_identity.labels[label].aliases[0]` — 플래그로 넘길 API 식별자."""
    contract = load_stage_contract("read", law)
    identity = (contract.get("lane") or {}).get("model_identity") or {}
    for entry in identity.get("labels") or []:
        if entry.get("label") == label:
            aliases = [str(name) for name in (entry.get("aliases") or [])]
            if aliases:
                return aliases[0]
            break
    raise DriverExit(
        EXIT_USAGE,
        f"계약 model_identity 에 라벨 {label!r} 의 alias 가 없다 — API 식별자를 정할 수 없다",
    )


def wrapper_schema_json(task: str) -> str:
    """`--json-schema` 인자 = 스키마 **JSON 문자열**(파일 경로가 아니다 — CLI 가 `is not valid JSON` 으로 거부 · 2026-09-13 step 1 실측). 파일은 영수증용으로 따로 남긴다."""
    return json.dumps(wrapper_schema(task), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def lane_argv(api_id: str, effort: str, schema_json: str) -> list[str]:
    """설계 §4 의 플래그 전건 · 순서 고정. `schema_json` = 스키마 JSON 문자열(경로 아님)."""
    # `--bare` 는 키체인 읽기도 건너뛰어 구독 로그인이 풀린다(LANE-RUNTIME 함정 S · 2026-09-13 실측).
    # 대체 = 설정 원천을 project 로 한정 + 중립 cwd(`_LANE_CWD`) + 슬래시 명령·MCP 차단 —
    # 실측(system/init): 훅 0 · 플러그인 0 · MCP 0 · 스킬 0 · 자동 메모리 = 중립 cwd 의 빈 디렉터리.
    return [
        "claude",
        "-p",
        "--setting-sources",
        "project",
        "--disable-slash-commands",
        "--strict-mcp-config",
        "--model",
        api_id,
        "--effort",
        effort,
        "--output-format",
        "json",
        "--json-schema",
        schema_json,
        "--permission-mode",
        "dontAsk",
        "--permission-prompts",
        "none",
        "--tools",
        "",
    ]


def lane_env() -> dict:
    env = dict(os.environ)
    env.update(LANE_ENV)
    return env


def wrapper_schema(task: str) -> dict:
    """응답 봉투 스키마 — `payload` 에 plan.py·design.py 의 작업 스키마를 그대로 품는다(복사 아님)."""
    if task not in TASK_SCHEMAS:
        raise DriverExit(EXIT_USAGE, f"plan.py·design.py 가 모르는 작업이다: {task!r}")
    return {
        "type": "object",
        "required": ["lane_id", "model", "effort", "input_digest", "payload"],
        "properties": {
            "lane_id": {"type": "string"},
            "model": {"type": "string"},
            "effort": {"type": "string"},
            "input_digest": {"type": "string"},
            "payload": TASK_SCHEMAS[task],
        },
    }


def main_model_of(model_usage) -> str | None:
    """`modelUsage` 에서 출력 토큰이 가장 큰 키. 동률이면 키 정렬 순 첫째(결정론)."""
    if not isinstance(model_usage, dict) or not model_usage:
        return None
    best: tuple[int, str] | None = None
    for key in sorted(model_usage):
        usage = model_usage[key] if isinstance(model_usage[key], dict) else {}
        tokens = usage.get("outputTokens", 0)
        tokens = int(tokens) if isinstance(tokens, (int, float)) else 0
        if best is None or tokens > best[0]:
            best = (tokens, key)
    return best[1] if best else None


def _receipt_path(ctx: Context, lane_id: str) -> str:
    return os.path.join(ctx.calls_dir, safe_lane_name(lane_id) + ".json")


def _raw_path(ctx: Context, lane_id: str) -> str:
    return os.path.join(ctx.calls_dir, safe_lane_name(lane_id) + ".raw.json")


def _previous_receipt(ctx: Context, lane_id: str) -> dict | None:
    path = _receipt_path(ctx, lane_id)
    if not os.path.isfile(path):
        return None
    try:
        return _load_json(path)
    except (OSError, ValueError) as exc:
        raise DriverExit(EXIT_UNDECIDABLE, f"영수증을 읽을 수 없다: {path}: {exc}") from exc


def _rotate_receipt(ctx: Context, lane_id: str, attempt: int) -> None:
    """이전 회차의 영수증·원시 출력을 `.attempt-<k>` 이름으로 보존한다(덮어쓰지 않는다)."""
    for suffix in (".json", ".raw.json"):
        current = os.path.join(ctx.calls_dir, safe_lane_name(lane_id) + suffix)
        if os.path.isfile(current):
            kept = os.path.join(
                ctx.calls_dir, f"{safe_lane_name(lane_id)}.attempt-{attempt}{suffix}"
            )
            os.replace(current, kept)


def _any_verified_call(ctx: Context) -> bool:
    """이 런에서 응답 파일을 낸 호출이 하나라도 있었는가(첫 좌표 실호출 검증의 기준)."""
    if not os.path.isdir(ctx.calls_dir):
        return False
    for name in sorted(os.listdir(ctx.calls_dir)):
        if not name.endswith(".json") or name.endswith(".raw.json"):
            continue
        try:
            receipt = _load_json(os.path.join(ctx.calls_dir, name))
        except (OSError, ValueError):
            continue
        if isinstance(receipt, dict) and receipt.get("response_json_sha256"):
            return True
    return False


# ---------------------------------------------------------------------------
# 레인 호출 한 번
# ---------------------------------------------------------------------------


@dataclass
class CallOutcome:
    lane_id: str
    ok: bool
    reason: str
    receipt_path: str | None = None
    response_path: str | None = None


def call_lane(ctx: Context, lanes_root: str, lane_id: str) -> CallOutcome:
    """대기 좌표 하나를 `claude -p` 한 번으로 채운다(설계 §4).

    응답 파일은 구동기가 쓴다. `payload` · `input_digest` · `lane_id` = 레인 출력 그대로 ·
    `model` = CLI `modelUsage` 주 키 · `effort` = 요청 플래그 값. 레인 자기 신고는 영수증에만.
    """
    try:
        request_json = lane_file(lanes_root, lane_id, REQUEST_JSON)
        request_md = lane_file(lanes_root, lane_id, REQUEST_MD)
        response_json = lane_file(lanes_root, lane_id, RESPONSE_JSON)
    except LaneContractError as exc:
        raise DriverExit(EXIT_USAGE, f"좌표 어휘 위반: {exc}") from exc
    if not os.path.isfile(request_json) or not os.path.isfile(request_md):
        raise DriverExit(EXIT_UNDECIDABLE, f"요청 파일이 없다: {lane_dir(lanes_root, lane_id)}")
    if os.path.isfile(response_json):
        return CallOutcome(lane_id, True, "응답 파일이 이미 있다 — 호출하지 않는다", None, response_json)

    request = _load_json(request_json)
    task = str(request.get("task", ""))
    label = str(request.get("model", ""))
    effort = str(request.get("effort", ""))
    if not task or not label or not effort:
        raise DriverExit(EXIT_USAGE, f"request.json 에 task·model·effort 가 없다: {request_json}")
    api_id = api_id_for_label(ctx.law, label)
    with open(request_md, "rb") as handle:
        stdin = handle.read()
    if len(stdin) > STDIN_MAX_BYTES:
        raise DriverExit(
            EXIT_USAGE,
            f"요청서가 stdin 상한 {STDIN_MAX_BYTES} B 를 넘는다({len(stdin)} B): {request_md}",
        )

    schema_path = os.path.join(ctx.schemas_dir, safe_lane_name(lane_id) + ".json")
    argv = lane_argv(api_id, effort, wrapper_schema_json(task))
    if ctx.dry_run:
        ctx.out(f"[dry-run] {lane_id}: " + " ".join(_shell_quote(part) for part in argv))
        return CallOutcome(lane_id, True, "dry-run", None, None)

    previous = _previous_receipt(ctx, lane_id)
    attempt = int(previous.get("attempt", 0)) + 1 if isinstance(previous, dict) else 1
    if attempt > CALL_CAP_PER_LANE:
        raise DriverExit(
            EXIT_CALL_CAP,
            f"좌표 {lane_id} 호출 상한 {CALL_CAP_PER_LANE} 초과(회차 {attempt}) — 사람이 본다",
        )
    if previous is not None:
        _rotate_receipt(ctx, lane_id, attempt - 1)
    _write_bytes(schema_path, _json_bytes(wrapper_schema(task)))

    started_at = _now_iso()
    env = lane_env()
    env["_LANE_CWD"] = os.path.join(ctx.evidence, "lane-cwd")  # 중립 cwd(설계 §4 정정 · 함정 S)
    result = ctx.executor(argv, stdin, env, WALL_CLOCK_SECONDS)
    ended_at = _now_iso()
    _write_bytes(_raw_path(ctx, lane_id), result.stdout)

    parsed: dict = {}
    parse_note = ""
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout.decode("utf-8"))
            parsed = loaded if isinstance(loaded, dict) else {}
            if not isinstance(loaded, dict):
                parse_note = "CLI 출력 최상위가 객체가 아니다"
        except (UnicodeDecodeError, ValueError) as exc:
            parse_note = f"CLI 출력이 JSON 이 아니다: {exc}"
    else:
        parse_note = "CLI 출력이 비었다"

    is_error = bool(parsed.get("is_error")) or result.timed_out or result.returncode != 0
    structured = _structured_output(parsed)
    self_report = structured if isinstance(structured, dict) else {}
    model_usage = parsed.get("modelUsage")
    main_model = main_model_of(model_usage)

    receipt = {
        "lane_id": lane_id,
        "request_md_sha256": _sha256_bytes(stdin),
        "response_json_sha256": None,
        "requested": {"model": label, "effort": effort, "api_id": api_id},
        "observed": {"modelUsage": model_usage, "main_model": main_model},
        "lane_self_report": {
            "model": self_report.get("model"),
            "effort": self_report.get("effort"),
            "lane_id": self_report.get("lane_id"),
        },
        "is_error": is_error,
        "num_turns": parsed.get("num_turns"),
        "total_cost_usd": parsed.get("total_cost_usd"),
        "duration_ms": parsed.get("duration_ms", result.duration_ms),
        "session_id": parsed.get("session_id"),
        "stderr_tail": result.stderr.decode("utf-8", errors="replace")[-STDERR_TAIL_CHARS:],
        "started_at": started_at,
        "ended_at": ended_at,
        "attempt": attempt,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "note": parse_note,
    }
    receipt_path = _receipt_path(ctx, lane_id)

    if is_error or parse_note:
        reason = "시간 초과" if result.timed_out else (parse_note or "is_error")
        receipt["note"] = reason
        _write_bytes(receipt_path, _json_bytes(receipt))
        return CallOutcome(lane_id, False, f"{lane_id}: 호출 실패({reason}) — 응답 미작성", receipt_path)

    if not isinstance(structured, dict) or not all(
        key in structured for key in ("lane_id", "input_digest", "payload")
    ):
        receipt["note"] = "레인 출력에 lane_id·input_digest·payload 가 없다"
        _write_bytes(receipt_path, _json_bytes(receipt))
        return CallOutcome(lane_id, False, f"{lane_id}: {receipt['note']} — 응답 미작성", receipt_path)

    if main_model is None:
        receipt["note"] = "CLI 출력에 modelUsage 가 없다 — model 을 정할 수 없어 응답을 쓰지 않는다"
        _write_bytes(receipt_path, _json_bytes(receipt))
        raise DriverExit(EXIT_UNDECIDABLE, f"{lane_id}: {receipt['note']}")

    expected_digest = str(request.get("input_digest", ""))
    if str(structured.get("input_digest", "")) != expected_digest:
        receipt["note"] = "입력 지문 반향 불일치 — 레인이 다른 요청서를 읽었거나 옮겨 적지 않았다 · 응답 미작성"
        _write_bytes(receipt_path, _json_bytes(receipt))
        return CallOutcome(lane_id, False, f"{lane_id}: {receipt['note']}", receipt_path)

    first_call = not _any_verified_call(ctx)
    # `lane_id` 는 구동기가 아는 좌표다 — 레인의 반향은 영수증에만(2026-09-13 step 3 실측: opus low 레인이
    # 'read-a' 만 적어 러너가 LaneContractError 로 거부). `input_digest` 는 P-12 시점 결속이라 레인 반향을 쓴다.
    response = {
        "lane_id": lane_id,
        "model": main_model,
        "effort": effort,
        "input_digest": structured["input_digest"],
        "payload": structured["payload"],
    }
    response_blob = (json.dumps(response, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    try:
        _write_bytes(response_json, response_blob)
    except OSError as exc:
        receipt["note"] = f"io_fault: 응답 파일 쓰기 실패 {exc}"
        _write_bytes(receipt_path, _json_bytes(receipt))
        raise DriverExit(EXIT_UNDECIDABLE, f"{lane_id}: {receipt['note']}") from exc
    receipt["response_json_sha256"] = _sha256_bytes(response_blob)
    _write_bytes(receipt_path, _json_bytes(receipt))

    if first_call and main_model != api_id:
        raise DriverExit(
            EXIT_UNDECIDABLE,
            f"첫 좌표 실호출 검증 실패 — {lane_id}: 관측 {main_model!r} ≠ 요청 {api_id!r} "
            "(응답 파일은 관측값으로 썼다 · 정지 · 상신)",
        )
    return CallOutcome(lane_id, True, "응답 작성", receipt_path, response_json)


def _structured_output(parsed: dict):
    """`--json-schema` 결과 자리. `structured_output` 이 있으면 그것, 없으면 `result` 문자열을 JSON 으로 본다."""
    if isinstance(parsed.get("structured_output"), dict):
        return parsed["structured_output"]
    text = parsed.get("result")
    if isinstance(text, str):
        try:
            loaded = json.loads(text)
        except ValueError:
            return None
        return loaded if isinstance(loaded, dict) else None
    return None


def _shell_quote(part: str) -> str:
    if part == "":
        return '""'
    if re.fullmatch(r"[A-Za-z0-9_./=:@%+,-]+", part):
        return part
    return "'" + part.replace("'", "'\\''") + "'"


# ---------------------------------------------------------------------------
# 대기 좌표 조회(무변경) — dry-run · lanes
# ---------------------------------------------------------------------------


def lane_inventory(lanes_root: str) -> list[dict]:
    """`<lanes>/<read_run>/<task>[/retry-N]/batch-M` 전건 — 요청 유무 · 응답 유무."""
    rows: list[dict] = []
    if not os.path.isdir(lanes_root):
        return rows
    for dirpath, _dirs, files in os.walk(lanes_root):
        if REQUEST_JSON not in files:
            continue
        rel = os.path.relpath(dirpath, lanes_root).replace(os.sep, "/")
        rows.append(
            {
                "lane_id": rel,
                "request": True,
                "response": RESPONSE_JSON in files,
            }
        )
    rows.sort(key=lambda row: row["lane_id"])
    return rows


# ---------------------------------------------------------------------------
# 명령
# ---------------------------------------------------------------------------


def _load_meta(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle) if path.endswith(".json") else yaml.safe_load(handle)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise DriverExit(EXIT_USAGE, f"patent-meta 를 읽을 수 없다: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise DriverExit(EXIT_USAGE, f"patent-meta 최상위가 매핑이 아니다: {path}")
    return data


def _ensure_worktree(ctx: Context, ref: str) -> None:
    """`git worktree add --detach <worktree> <ref>`. 이미 있으면 git worktree 인지만 확인하고 재사용."""
    if os.path.exists(ctx.worktree):
        probe = gitpin.run_git(ctx.worktree, ["rev-parse", "HEAD"])
        if probe.returncode != 0:
            raise DriverExit(EXIT_USAGE, f"기존 경로가 git worktree 가 아니다: {ctx.worktree}")
        ctx.out(f"worktree 재사용: {ctx.worktree} @ {probe.stdout.strip()}")
        return
    os.makedirs(os.path.dirname(ctx.worktree), exist_ok=True)
    add = gitpin.run_git(ctx.repo, ["worktree", "add", "--detach", ctx.worktree, ref])
    if add.returncode != 0:
        raise DriverExit(
            EXIT_USAGE,
            f"worktree 생성 실패 {ctx.worktree} @ {ref} (exit {add.returncode}): "
            + " / ".join(line for line in add.stderr.strip().splitlines() if line),
        )
    ctx.out(f"worktree 생성: {ctx.worktree} @ {ref}")


def cmd_init(ctx: Context, args: argparse.Namespace) -> int:
    if args.expect_sha256:
        actual = _sha256_file(args.source)
        expected = args.expect_sha256.removeprefix("sha256:")
        if actual != expected:
            raise DriverExit(
                EXIT_USAGE, f"소재 지문 불일치 — 기대 {expected} · 실측 {actual}: {args.source}"
            )
    if not os.path.isfile(args.source):
        raise DriverExit(EXIT_USAGE, f"소재 파일이 없다: {args.source}")
    if not os.path.isdir(args.figures):
        raise DriverExit(EXIT_USAGE, f"도면 디렉터리가 없다: {args.figures}")
    meta = _load_meta(args.patent_meta)
    if ctx.dry_run:
        ctx.out(f"[dry-run] git worktree add --detach {ctx.worktree} {args.ref}")
        ctx.out(f"[dry-run] source.run(run_root={ctx.run_root}, run_kind={RUN_KIND}, partial_until={PARTIAL_UNTIL})")
        return EXIT_OK
    if not args.run_root:
        _ensure_worktree(ctx, args.ref)
    paths = ctx.paths()
    if os.path.isfile(paths.source_report):
        ctx.out(f"이미 개시된 런 — source-report 실재: {paths.source_report}")
        return EXIT_OK
    try:
        outcome = source_stage.run(
            run_root=ctx.run_root,
            source_patent_path=args.source,
            figures_dir=args.figures,
            run_id=ctx.run_id,
            patent_meta=meta,
            run_kind=RUN_KIND,
            partial_until=PARTIAL_UNTIL,
            repo=ctx.law,
        )
    except OSError as exc:
        raise DriverExit(EXIT_UNDECIDABLE, f"io_fault: source 스테이지 {exc}") from exc
    except StageError as exc:
        raise DriverExit(EXIT_TERMINAL_FAIL, f"source 스테이지 정지: {exc}") from exc
    ctx.out(f"source: status={outcome['status']} reason={outcome.get('reason_label')}")
    if outcome["status"] != "ok":
        raise DriverExit(EXIT_TERMINAL_FAIL, f"source 판정 {outcome['status']}: {outcome.get('reason_label')}")
    return EXIT_OK


def _classify_read_outcome(ctx: Context, outcome: dict) -> tuple[int, str]:
    if "gate_note" in outcome:
        gate = _load_json(ctx.paths().phase_gate_json)
        blocked_by = str(gate.get("blocked_by"))
        if blocked_by == ESCALATION_AXIS:
            return EXIT_CONTINUE_POSSIBLE, f"조기 수렴 상신 축 미달 — `continue` 가능: {outcome.get('gate_note')}"
        return EXIT_GATE_WAIT, f"접지 진입 차단({blocked_by}) — 봉투 불가 · 사람이 본다: {outcome.get('gate_note')}"
    if outcome.get("status") == "ok" and outcome.get("spec") is not None:
        return EXIT_CP1_WAIT, "CP1 대기 — `cp1` 로 판독본을 내고 `approve` 로 봉투를 쓴다"
    return EXIT_TERMINAL_FAIL, f"READ 종결 실패: status={outcome.get('status')} reason={outcome.get('reason_label')}"


def cmd_step(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    lanes_root = paths.lanes_dir
    if ctx.dry_run:
        pending = [row["lane_id"] for row in lane_inventory(lanes_root) if not row["response"]]
        if not pending:
            ctx.out("[dry-run] 대기 없음 — 응답 없는 요청 좌표가 없다")
            return EXIT_OK
        for lane_id in pending:
            call_lane(ctx, lanes_root, lane_id)
        return EXIT_PENDING
    terminated, reason = _read_already_terminated(paths)
    if terminated:
        # 엔진은 종결한 런의 재호출을 거부한다(재정 T38 ②). 여기서는 산출물만 보고 같은 답을 낸다.
        code = EXIT_CP1_WAIT if os.path.isfile(paths.material_spec_json) else EXIT_TERMINAL_FAIL
        ctx.out(f"READ 는 이미 종결했다({reason}) — 엔진을 다시 부르지 않는다")
        if code == EXIT_CP1_WAIT:
            ctx.out("CP1 대기 — `cp1` 로 판독본을 내고 `approve` 로 봉투를 쓴다")
            return code
        raise DriverExit(code, "READ 가 재료 명세 없이 종결했다 — convergence.json 판정을 본다")
    rules = Rules.load()
    for _round in range(STEP_REENTRY_CAP):
        adapter = FileLaneAdapter(lanes_root, repo=ctx.law)
        try:
            outcome = read_stage.run(run_root=ctx.run_root, adapter=adapter, rules=rules, repo=ctx.law)
        except LanePending as pending:
            lane_ids = list(pending.pending)
        except OSError as exc:
            raise DriverExit(EXIT_UNDECIDABLE, f"io_fault: read 스테이지 {exc}") from exc
        except StageError as exc:
            raise DriverExit(EXIT_TERMINAL_FAIL, f"read 스테이지 정지: {exc}") from exc
        else:
            code, reason = _classify_read_outcome(ctx, outcome)
            ctx.out(reason)
            return code
        ctx.out(f"대기 좌표 {len(lane_ids)}건: {', '.join(lane_ids)}")
        failed: list[str] = []
        for lane_id in lane_ids:
            result = call_lane(ctx, lanes_root, lane_id)
            ctx.out(f"  {lane_id}: {result.reason}")
            if not result.ok:
                failed.append(lane_id)
        if failed:
            raise DriverExit(EXIT_PENDING, f"호출 실패 좌표 {len(failed)}건 — 다음 step 이 다시 대기로 낸다: {', '.join(failed)}")
    raise DriverExit(EXIT_PENDING, f"재진입 상한 {STEP_REENTRY_CAP} 도달 — 대기 좌표가 남았다")


def _read_already_terminated(paths: RunPaths) -> tuple[bool, str]:
    """엔진의 종결 근거 두 가지(`shadow-ledger.json#terminated` · `convergence.json#phase == full`)를
    읽기만 한다. 판정 규격의 정본은 `read.py#_run_is_terminated` 이며 여기서는 그 앞 두 근거만 본다."""
    if os.path.isfile(paths.shadow_pointer):
        try:
            pointer = _load_json(paths.shadow_pointer)
        except (OSError, ValueError):
            pointer = None
        if isinstance(pointer, dict) and pointer.get("terminated") is True:
            return True, "shadow-ledger.json#terminated"
    if os.path.isfile(paths.convergence_json):
        try:
            convergence = _load_json(paths.convergence_json)
        except (OSError, ValueError):
            convergence = None
        if isinstance(convergence, dict) and convergence.get("phase") == "full":
            return True, "convergence.json#phase=full"
    return False, ""


def cmd_rewrap(ctx: Context, args: argparse.Namespace) -> int:
    """보존된 원시 출력(`.raw.json`)에서 응답 파일을 다시 조립한다 — 모델 호출 없음 · 결정론.

    쓰는 경우 = 구동기 자신의 조립 결함으로 응답 파일이 잘못 써진 좌표(예: lane_id 칸). 레인 출력의
    `payload`·`input_digest` 는 그대로, `lane_id` = 좌표, `model` = 원시 출력 `modelUsage` 주 키,
    `effort` = request.json 값. 입력 지문 반향이 요청과 다르면 쓰지 않는다.
    """
    paths = ctx.paths()
    lanes_root = paths.lanes_dir
    lane_id = args.lane_id
    try:
        request_json = lane_file(lanes_root, lane_id, REQUEST_JSON)
        response_json = lane_file(lanes_root, lane_id, RESPONSE_JSON)
    except LaneContractError as exc:
        raise DriverExit(EXIT_USAGE, f"좌표 어휘 위반: {exc}") from exc
    raw_path = _raw_path(ctx, lane_id)
    if not os.path.isfile(request_json) or not os.path.isfile(raw_path):
        raise DriverExit(EXIT_USAGE, f"request.json 또는 원시 출력이 없다: {lane_id}")
    request = _load_json(request_json)
    with open(raw_path, "rb") as handle:
        parsed = json.loads(handle.read().decode("utf-8"))
    structured = _structured_output(parsed)
    if not isinstance(structured, dict) or not all(k in structured for k in ("input_digest", "payload")):
        raise DriverExit(EXIT_UNDECIDABLE, f"{lane_id}: 원시 출력에 input_digest·payload 가 없다")
    if str(structured.get("input_digest", "")) != str(request.get("input_digest", "")):
        raise DriverExit(EXIT_UNDECIDABLE, f"{lane_id}: 입력 지문 반향 불일치 — 다시 조립하지 않는다")
    main_model = main_model_of(parsed.get("modelUsage"))
    if main_model is None:
        raise DriverExit(EXIT_UNDECIDABLE, f"{lane_id}: 원시 출력에 modelUsage 가 없다")
    response = {
        "lane_id": lane_id,
        "model": main_model,
        "effort": str(request.get("effort", "")),
        "input_digest": structured["input_digest"],
        "payload": structured["payload"],
    }
    blob = (json.dumps(response, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if ctx.dry_run:
        ctx.out(f"[dry-run] rewrap {lane_id}: {len(blob)} B · model={main_model}")
        return EXIT_OK
    _write_bytes(response_json, blob)
    receipt_path = _receipt_path(ctx, lane_id)
    receipt = _previous_receipt(ctx, lane_id) if os.path.isdir(ctx.calls_dir) else None
    if isinstance(receipt, dict):
        receipt["response_json_sha256"] = _sha256_bytes(blob)
        receipt["rewrapped_at"] = _now_iso()
        _write_bytes(receipt_path, _json_bytes(receipt))
    ctx.out(f"rewrap {lane_id}: 응답 파일 재조립 · model={main_model}")
    return EXIT_OK


def cmd_lanes(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    rows = lane_inventory(paths.lanes_dir) + lane_inventory(paths.design_lanes_dir)
    if not rows:
        ctx.out("요청 좌표 없음")
    for row in rows:
        receipt = _previous_receipt(ctx, row["lane_id"]) if os.path.isdir(ctx.calls_dir) else None
        summary = "영수증 없음"
        if isinstance(receipt, dict):
            summary = (
                f"attempt={receipt.get('attempt')} is_error={receipt.get('is_error')} "
                f"main_model={(receipt.get('observed') or {}).get('main_model')}"
            )
        state = "완료" if row["response"] else "대기"
        ctx.out(f"{state}  {row['lane_id']}  {summary}")
    return EXIT_OK


def _read_quote(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as handle:
            quote = handle.read()
    except OSError as exc:
        raise DriverExit(EXIT_USAGE, f"quote-file 을 읽을 수 없다: {path}: {exc}") from exc
    if not quote.strip():
        raise DriverExit(EXIT_USAGE, f"quote-file 이 비어 있다: {path}")
    return quote


def _validate_envelope(ctx: Context, envelope: dict) -> None:
    schema = _load_json(os.path.join(ctx.law, *APPROVAL_SCHEMA_REL))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(envelope), key=lambda err: list(err.absolute_path)
    )
    if errors:
        first = errors[0]
        locus = "/".join(str(step) for step in first.absolute_path) or "$"
        raise DriverExit(EXIT_USAGE, f"봉투가 approval-envelope/v0 를 위반한다(@{locus}): {first.message}")


def _envelope_text(envelope: dict, title: str) -> str:
    body = yaml.safe_dump(envelope, allow_unicode=True, sort_keys=False)
    return f"---\n{body}---\n\n{title}\n"


def _run_id_of(paths: RunPaths) -> str:
    try:
        with open(paths.run_yaml, encoding="utf-8") as handle:
            meta = yaml.safe_load(handle) or {}
    except OSError as exc:
        raise DriverExit(EXIT_USAGE, f"run.yaml 이 없다: {paths.run_yaml}") from exc
    return str(meta.get("run_id", ""))


def cmd_continue(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    if not os.path.isfile(paths.phase_gate_json):
        raise DriverExit(EXIT_USAGE, "phase-gate.json 이 없다 — 조기 수렴 판정 전이다")
    gate = _load_json(paths.phase_gate_json)
    if gate.get("blocked_by") != ESCALATION_AXIS or gate.get("entered"):
        raise DriverExit(
            EXIT_USAGE,
            f"계속 봉투는 상신 축 미달({ESCALATION_AXIS})에만 쓴다 — 지금 blocked_by="
            f"{gate.get('blocked_by')!r} entered={gate.get('entered')!r}(재정 T17)",
        )
    if not os.path.isfile(paths.convergence_early_json):
        raise DriverExit(EXIT_USAGE, "결속 대상인 조기 수렴 판정서가 없다")
    quote = _read_quote(args.quote_file)
    envelope = {
        "schema": "approval-envelope/v0",
        "checkpoint": CONTINUE_CHECKPOINT,
        "run_id": _run_id_of(paths),
        "target": {
            "path": "10-read/convergence-early.json",
            "digest": "sha256:" + _sha256_file(paths.convergence_early_json),
        },
        "decision": "approved",
        "owner_quote": quote,
        "quote_provenance": {"channel": "session-transcript", "located_at": args.located_at},
        "decided_at": args.decided_at or _now_iso(),
        "recorded_by": "orchestrator",
    }
    _validate_envelope(ctx, envelope)
    text = _envelope_text(envelope, "# Owner 「계속」 — 조기 수렴 상신 축 미달(재정 P-U3 · T17)")
    if ctx.dry_run:
        ctx.out(f"[dry-run] 계속 봉투 → {paths.convergence_continue_md}")
        return EXIT_OK
    _write_bytes(paths.convergence_continue_md, text.encode("utf-8"))
    ctx.out(f"계속 봉투 작성: {paths.convergence_continue_md}")
    return EXIT_OK


def _review_requests(paths: RunPaths) -> list[dict]:
    if not os.path.isfile(paths.convergence_json):
        return []
    raw = (_load_json(paths.convergence_json) or {}).get("review_requests")
    return [entry for entry in raw if isinstance(entry, dict)] if isinstance(raw, list) else []


def cmd_cp1(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    if not os.path.isfile(paths.material_spec_md):
        raise DriverExit(EXIT_USAGE, f"판독본이 없다(CP1 전): {paths.material_spec_md}")
    requests = _review_requests(paths)
    targets = sorted({str(entry.get("target")) for entry in requests})
    ctx.out(f"판독본: {paths.material_spec_md}")
    ctx.out(f"재료 명세: {paths.material_spec_json}")
    ctx.out(f"review_requests: {len(requests)}건 · target {len(targets)}종")
    with open(paths.material_spec_md, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    start = next((index for index, line in enumerate(lines) if line.startswith("## 8-b")), None)
    ctx.out("--- §8-b 첫 줄 ---")
    if start is None:
        ctx.out("(§8-b 절을 찾지 못했다)")
    else:
        for line in lines[start : start + REVIEW_SECTION_LINES]:
            ctx.out(line)
    ctx.out("--- 봉투 서식 초안(approve 인자 --adjudicated 의 JSON) ---")
    draft = [{"target": target, "verdict": ""} for target in targets]
    ctx.out(json.dumps(draft, ensure_ascii=False, indent=2))
    return EXIT_OK


def _next_approval_version(paths: RunPaths) -> int:
    frozen = paths.frozen_dir
    highest = 0
    if os.path.isdir(frozen):
        for name in os.listdir(frozen):
            match = APPROVAL_NAME_RE.match(name)
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def _current_approval_version(paths: RunPaths) -> int | None:
    version = _next_approval_version(paths) - 1
    return version if version >= 1 else None


def _split_ids(raw: str | None) -> list[str]:
    return [part.strip() for part in (raw or "").split(",") if part.strip()]


def cmd_approve(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    if not os.path.isfile(paths.material_spec_json):
        raise DriverExit(EXIT_USAGE, f"재료 명세가 없다(CP1 전): {paths.material_spec_json}")
    quote = _read_quote(args.quote_file)
    try:
        with open(args.adjudicated, encoding="utf-8") as handle:
            adjudicated = json.load(handle)
    except (OSError, ValueError) as exc:
        raise DriverExit(EXIT_USAGE, f"adjudicated JSON 을 읽을 수 없다: {args.adjudicated}: {exc}") from exc
    if not isinstance(adjudicated, list):
        raise DriverExit(EXIT_USAGE, "adjudicated 는 배열이어야 한다")
    run_meta_whitelist: list = []
    try:
        with open(paths.run_yaml, encoding="utf-8") as handle:
            run_meta_whitelist = list((yaml.safe_load(handle) or {}).get("numeric_whitelist") or [])
    except OSError:
        run_meta_whitelist = []
    envelope: dict = {
        "schema": "approval-envelope/v0",
        "checkpoint": CP1_CHECKPOINT,
        "run_id": _run_id_of(paths),
        "target": {
            "path": "10-read/material-spec.json",
            "digest": "sha256:" + _sha256_file(paths.material_spec_json),
        },
        "decision": args.decision,
        "owner_quote": quote,
        "quote_provenance": {"channel": "session-transcript", "located_at": args.located_at},
        "decided_at": args.decided_at or _now_iso(),
        "recorded_by": "orchestrator",
        "manual_verification_ack": _split_ids(args.manual_ack),
        "derived_fact_ack": _split_ids(args.derived_ack),
        "numeric_whitelist_printed": run_meta_whitelist,
        "review_adjudicated": adjudicated,
    }
    if args.drop_decision:
        envelope["drop_decision"] = args.drop_decision
    if args.decision == "rejected":
        envelope["directives"] = list(args.directive or [])
    _validate_envelope(ctx, envelope)

    requested = {str(entry.get("target")) for entry in _review_requests(paths)}
    answered = {str(entry.get("target")) for entry in adjudicated if isinstance(entry, dict)}
    for missing in sorted(requested - answered):
        ctx.out(f"경고: 판독 요청 {missing} 에 답이 없다 — freeze 가 거부한다(재정 T59 ②)")
    for phantom in sorted(answered - requested):
        ctx.out(f"경고: {phantom} 은 이 런의 판독 요청에 없는 target 이다 — freeze 가 거부한다")

    version = _next_approval_version(paths)
    path = paths.approval(version)
    text = _envelope_text(envelope, f"# CP1 {args.decision} — 재료 명세 v{version}")
    if ctx.dry_run:
        ctx.out(f"[dry-run] 승인 봉투 → {path}")
        return EXIT_OK
    _write_bytes(path, text.encode("utf-8"))
    ctx.out(f"승인 봉투 작성: {path} (decision={args.decision} · review_adjudicated {len(adjudicated)}건)")
    return EXIT_OK


def cmd_freeze(ctx: Context, args: argparse.Namespace) -> int:
    paths = ctx.paths()
    version = _current_approval_version(paths)
    if version is None:
        raise DriverExit(EXIT_USAGE, "승인 봉투가 없다 — `approve` 가 먼저다")
    if ctx.dry_run:
        ctx.out(f"[dry-run] freeze.run(spec_version={version})")
        return EXIT_OK
    try:
        outcome = freeze_stage.run(
            run_root=ctx.run_root, spec_version=version, rules=Rules.load(), repo=ctx.law
        )
    except OSError as exc:
        raise DriverExit(EXIT_UNDECIDABLE, f"io_fault: freeze 스테이지 {exc}") from exc
    except StageError as exc:
        raise DriverExit(EXIT_TERMINAL_FAIL, f"freeze 스테이지 정지: {exc}") from exc
    for row in outcome.get("rows") or []:
        for finding in getattr(row, "findings", []) or []:
            ctx.out(f"  {row.check_id}/{finding.rule}@{finding.locus}: {finding.message}")
    if outcome.get("status") != "ok":
        raise DriverExit(
            EXIT_TERMINAL_FAIL, f"freeze 판정 {outcome.get('status')}: {outcome.get('reason_label')}"
        )
    ctx.out(f"동결: {outcome.get('path')} digest={outcome.get('digest')} — partial_until={PARTIAL_UNTIL} 도달 · 종결")
    return EXIT_OK


def manifest_lines(ctx: Context) -> list[str]:
    """`evidence/**` 전건(MANIFEST 자신 제외) + `10-read/*.json` + `15-frozen/*` 의 sha256 · 경로."""
    paths = ctx.paths()
    entries: list[tuple[str, str]] = []
    base = ctx.worktree if os.path.commonpath([ctx.worktree, ctx.run_root]) == ctx.worktree else os.path.dirname(ctx.run_root)

    def add(path: str) -> None:
        entries.append((_sha256_file(path), os.path.relpath(path, base).replace(os.sep, "/")))

    if os.path.isdir(ctx.evidence):
        for dirpath, _dirs, files in os.walk(ctx.evidence):
            for name in files:
                full = os.path.join(dirpath, name)
                if os.path.realpath(full) == os.path.realpath(os.path.join(ctx.evidence, MANIFEST_BASENAME)):
                    continue
                add(full)
    if os.path.isdir(paths.read_dir):
        for name in os.listdir(paths.read_dir):
            full = os.path.join(paths.read_dir, name)
            if name.endswith(".json") and os.path.isfile(full):
                add(full)
    if os.path.isdir(paths.frozen_dir):
        for name in os.listdir(paths.frozen_dir):
            full = os.path.join(paths.frozen_dir, name)
            if os.path.isfile(full):
                add(full)
    if os.path.isdir(paths.design_dir):
        for dirpath, _dirs, files in os.walk(paths.design_dir):
            for name in files:
                add(os.path.join(dirpath, name))
    entries.sort(key=lambda pair: pair[1])
    return [f"{digest}  {rel}" for digest, rel in entries]


# ---------------------------------------------------------------------------
# extend · design (재정 T64 ①②)
# ---------------------------------------------------------------------------


def _terminus_enum(law: str) -> list[str]:
    kinds = run_kinds_contract(law).get("kinds") or {}
    enum = (kinds.get("partial") or {}).get("terminates_at_enum") or []
    if not enum:
        raise DriverExit(EXIT_USAGE, "run-kinds.yaml#kinds.partial.terminates_at_enum 이 비어 있다")
    return [str(value) for value in enum]


def _law_dirty_entries(law: str) -> list[str]:
    """법 트리의 `git status --porcelain` 중 결박 기제 자신의 생성물 밖 변경 목록. git 트리가 아니면 2."""
    proc = gitpin.run_git(law, ["status", "--porcelain"])
    if proc.returncode != 0:
        raise DriverExit(EXIT_USAGE, f"법 트리가 git 작업 트리가 아니다: {law}")
    dirty: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if path.startswith(LAW_DIRTY_EXEMPT_PREFIXES):
            continue
        dirty.append(line.rstrip())
    return dirty


def _next_extension_version(paths: RunPaths) -> int:
    highest = 0
    if os.path.isdir(paths.frozen_dir):
        for name in os.listdir(paths.frozen_dir):
            match = EXTENSION_NAME_RE.match(name)
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def _load_run_yaml(paths: RunPaths) -> dict:
    try:
        with open(paths.run_yaml, encoding="utf-8") as handle:
            meta = yaml.safe_load(handle) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise DriverExit(EXIT_USAGE, f"run.yaml 을 읽을 수 없다: {paths.run_yaml}: {exc}") from exc
    if not isinstance(meta, dict):
        raise DriverExit(EXIT_USAGE, "run.yaml 최상위가 매핑이 아니다")
    return meta


def cmd_extend(ctx: Context, args: argparse.Namespace) -> int:
    """부분 런 종료선 연장 봉투 — `15-frozen/extension-v<N>.md` + `run.yaml#partial_until` 이동(재정 T64 ①)."""
    paths = ctx.paths()
    meta = _load_run_yaml(paths)
    if meta.get("status") != "active":
        raise DriverExit(EXIT_USAGE, f"연장은 active 런에만 — 지금 status={meta.get('status')!r}")
    if meta.get("run_kind") != RUN_KIND:
        raise DriverExit(EXIT_USAGE, f"연장은 partial 런에만 — 지금 run_kind={meta.get('run_kind')!r}")
    enum = _terminus_enum(ctx.law)
    current = str(meta.get("partial_until", ""))
    if current not in enum:
        raise DriverExit(EXIT_USAGE, f"run.yaml#partial_until={current!r} 이 terminates_at_enum 밖이다")
    if args.until not in enum:
        raise DriverExit(EXIT_USAGE, f"--until {args.until!r} 이 terminates_at_enum 밖이다: {enum}")
    if enum.index(args.until) <= enum.index(current):
        raise DriverExit(
            EXIT_USAGE, f"--until {args.until!r} 은 현재 종료선 {current!r} 보다 뒤가 아니다(순서 = {enum})"
        )
    dirty = _law_dirty_entries(ctx.law)
    if dirty:
        raise DriverExit(
            EXIT_USAGE, "법 트리가 더럽다 — 연장은 커밋된 법 아래에서만 기록한다: " + " / ".join(dirty)
        )
    law_commit = gitpin.run_git(ctx.law, ["rev-parse", "HEAD"]).stdout.strip()
    quote = _read_quote(args.quote_file)
    decided_at = args.decided_at or _now_iso()
    envelope = {
        "schema": "extension-envelope/v0",
        "kind": "partial_until_extension",
        "run_id": str(meta.get("run_id", "")),
        "from": current,
        "to": args.until,
        "owner_quote": quote,
        "quote_provenance": {"located_at": args.located_at, "decided_at": decided_at},
        "recorded_by": "orchestrator",
        "rulings": list(args.ruling or []),
        "engine": {
            "commit_at_start": str((meta.get("engine") or {}).get("commit", "")),
            "law_commit": law_commit,
        },
    }
    schema = _load_json(os.path.join(ctx.law, *EXTENSION_SCHEMA_REL))
    errors = sorted(Draft202012Validator(schema).iter_errors(envelope), key=lambda err: list(err.absolute_path))
    if errors:
        first = errors[0]
        locus = "/".join(str(step) for step in first.absolute_path) or "$"
        raise DriverExit(EXIT_USAGE, f"연장 봉투가 extension-envelope/v0 를 위반한다(@{locus}): {first.message}")
    version = _next_extension_version(paths)
    target = paths.extension(version)
    text = _envelope_text(envelope, f"# Owner 「연장」 — partial_until {current} → {args.until}(재정 T64 ①)") + "\n" + quote
    if not text.endswith("\n"):
        text += "\n"
    if ctx.dry_run:
        ctx.out(f"[dry-run] 연장 봉투 → {target} · run.yaml partial_until {current} → {args.until}")
        return EXIT_OK
    _write_bytes(target, text.encode("utf-8"))
    meta["partial_until"] = args.until
    extensions = meta.get("extensions")
    if not isinstance(extensions, list):
        extensions = []
    extensions.append(
        {
            "path": os.path.relpath(target, paths.run_root).replace(os.sep, "/"),
            "from": current,
            "to": args.until,
            "law_commit": law_commit,
            "decided_at": decided_at,
        }
    )
    meta["extensions"] = extensions
    from engine.stages import dump_yaml  # noqa: PLC0415 - 러너와 같은 직렬화로 쓴다

    dump_yaml(paths.run_yaml, meta)
    ctx.out(f"연장 봉투 작성: {target} · partial_until {current} → {args.until}")
    return EXIT_OK


def cmd_design(ctx: Context, args: argparse.Namespace) -> int:
    """설계 스테이지 1회 구동 — `design.run` 재진입(상한 4) + 대기 좌표 호출(재정 T64 ②)."""
    paths = ctx.paths()
    meta = _load_run_yaml(paths)
    enum = _terminus_enum(ctx.law)
    current = str(meta.get("partial_until", ""))
    if meta.get("run_kind") == RUN_KIND and (current not in enum or enum.index(current) < enum.index("design")):
        raise DriverExit(EXIT_TERMINAL_FAIL, f"종료선 — partial_until={current!r} 은 design 앞이다 · `extend` 가 먼저다")
    lanes_root = paths.design_lanes_dir
    if ctx.dry_run:
        pending = [row["lane_id"] for row in lane_inventory(lanes_root) if not row["response"]]
        if not pending:
            ctx.out(f"[dry-run] design.run(run_root={ctx.run_root}) — 대기 좌표 없음(요청은 실행 시 생긴다)")
            return EXIT_OK
        for lane_id in pending:
            call_lane(ctx, lanes_root, lane_id)
        return EXIT_PENDING
    for _round in range(DESIGN_REENTRY_CAP):
        try:
            outcome = design_stage.run(run_root=ctx.run_root, repo=ctx.law)
        except OSError as exc:
            raise DriverExit(EXIT_UNDECIDABLE, f"io_fault: design 스테이지 {exc}") from exc
        except StageError as exc:
            raise DriverExit(EXIT_TERMINAL_FAIL, f"design 스테이지 정지: {exc}") from exc
        for row in outcome.get("rows") or []:
            for finding in getattr(row, "findings", []) or []:
                ctx.out(f"  {row.check_id}/{finding.rule}@{finding.locus}: {finding.message}")
        status = str(outcome.get("status"))
        if status == "pending":
            lane_ids = list(outcome.get("pending") or [])
            ctx.out(f"대기 좌표 {len(lane_ids)}건: {', '.join(lane_ids)}")
            failed: list[str] = []
            for lane_id in lane_ids:
                result = call_lane(ctx, lanes_root, lane_id)
                ctx.out(f"  {lane_id}: {result.reason}")
                if not result.ok:
                    failed.append(lane_id)
            if failed:
                raise DriverExit(EXIT_PENDING, f"호출 실패 좌표 {len(failed)}건 — 다음 design 이 다시 대기로 낸다: {', '.join(failed)}")
            continue
        if status == "ok":
            ctx.out(f"설계: {outcome.get('path')} digest={outcome.get('digest')}")
            return EXIT_OK
        raise DriverExit(EXIT_TERMINAL_FAIL, f"design 판정 {status}: {outcome.get('reason_label')}")
    raise DriverExit(EXIT_CALL_CAP, f"design 재진입 상한 {DESIGN_REENTRY_CAP} 도달")


def cmd_seal(ctx: Context, args: argparse.Namespace) -> int:
    lines = manifest_lines(ctx)
    target = os.path.join(ctx.evidence, MANIFEST_BASENAME)
    if ctx.dry_run:
        ctx.out(f"[dry-run] MANIFEST {len(lines)}행 → {target}")
        return EXIT_OK
    _write_bytes(target, ("\n".join(lines) + "\n").encode("utf-8"))
    ctx.out(f"MANIFEST 작성: {target} ({len(lines)}행)")
    return EXIT_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="drive_partial_read.py",
        description="READ 부분 런 구동기(partial · partial_until=freeze) + 연장·설계(T64) — 재정 T60 집행. 명령 11 · 판단 없음.",
    )
    parser.add_argument("--repo", help="정본 리포(기본 = 이 파일의 위치에서 추정)")
    parser.add_argument("--worktree-root", help="런 worktree 의 부모(기본 <repo>/.worktrees)")
    parser.add_argument("--run-root", help="런 작업장 경로를 직접 지정(worktree 배치 대신 · 그때 법 = --repo)")
    parser.add_argument("--evidence-dir", help="영수증 자리(기본 <worktree>/evidence)")
    parser.add_argument("--executor", choices=("claude", "stub"), default="claude", help="stub 은 시험 전용")
    parser.add_argument("--dry-run", action="store_true", help="레인 명령줄만 인쇄 · 파일을 쓰지 않는다")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="worktree 생성 + source 스테이지(partial · freeze)")
    init.add_argument("run_id")
    init.add_argument("--source", required=True)
    init.add_argument("--figures", required=True)
    init.add_argument("--patent-meta", required=True, help="yaml 또는 json")
    init.add_argument("--ref", default=DEFAULT_INIT_REF, help="worktree 가 결박될 ref(기본 main)")
    init.add_argument("--expect-sha256", help="소재 지문 대조(어긋나면 정지)")

    sub.add_parser("step", help="read 스테이지 재진입 + 대기 좌표 순차 호출").add_argument("run_id")
    sub.add_parser("lanes", help="무변경 조회 — 좌표 상태 · 영수증 요약").add_argument("run_id")
    rewrap = sub.add_parser("rewrap", help="원시 출력(.raw.json)에서 응답 파일 재조립 — 모델 호출 없음")
    rewrap.add_argument("run_id")
    rewrap.add_argument("lane_id")

    cont = sub.add_parser("continue", help="상신 축 미달에만 · convergence_continue 봉투")
    cont.add_argument("run_id")
    cont.add_argument("--quote-file", required=True)
    cont.add_argument("--located-at", default="세션 대화창 · Owner 「계속」")
    cont.add_argument("--decided-at", help="ISO-8601 UTC(기본 지금)")

    sub.add_parser("cp1", help="CP1 판독본 경로 · 요청 건수 · §8-b · 봉투 서식 초안").add_argument("run_id")

    approve = sub.add_parser("approve", help="CP1 승인 봉투 15-frozen/approval-v<N>.md")
    approve.add_argument("run_id")
    approve.add_argument("--quote-file", required=True)
    approve.add_argument("--adjudicated", required=True, help="review_adjudicated[] JSON 파일")
    approve.add_argument("--decision", choices=("approved", "rejected"), default="approved")
    approve.add_argument("--manual-ack", help="figure-sourced 항목 id 쉼표 목록")
    approve.add_argument("--derived-ack", help="derived 항목 id 쉼표 목록")
    approve.add_argument("--drop-decision", choices=("go", "drop"))
    approve.add_argument("--directive", action="append", help="rejected 일 때 지시(반복 가능)")
    approve.add_argument("--located-at", default="세션 대화창 · CP1 응답")
    approve.add_argument("--decided-at", help="ISO-8601 UTC(기본 지금)")

    sub.add_parser("freeze", help="freeze 스테이지 1회 — partial_until 도달 = 종결").add_argument("run_id")
    sub.add_parser("seal", help="evidence/MANIFEST-sha256.txt").add_argument("run_id")

    extend = sub.add_parser("extend", help="부분 런 종료선 연장 봉투 15-frozen/extension-v<N>.md(재정 T64 ①)")
    extend.add_argument("run_id")
    extend.add_argument("--quote-file", required=True)
    extend.add_argument("--until", required=True, help="새 종료선(run-kinds.yaml#kinds.partial.terminates_at_enum 의 값 · 현 종료선보다 뒤)")
    extend.add_argument("--ruling", action="append", help="근거 재정 id(반복 가능)")
    extend.add_argument("--located-at", default="세션 대화창 · Owner 「연장」")
    extend.add_argument("--decided-at", help="ISO-8601 UTC(기본 지금)")

    sub.add_parser("design", help="design 스테이지 1회 구동(재진입 상한 4 · 대기 좌표 호출) — 재정 T64 ②").add_argument("run_id")
    return parser


_COMMANDS = {
    "init": cmd_init,
    "step": cmd_step,
    "lanes": cmd_lanes,
    "rewrap": cmd_rewrap,
    "continue": cmd_continue,
    "cp1": cmd_cp1,
    "approve": cmd_approve,
    "freeze": cmd_freeze,
    "seal": cmd_seal,
    "extend": cmd_extend,
    "design": cmd_design,
}


def main(argv: list[str] | None = None, *, executor: Executor | None = None, out=None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else EXIT_USAGE
    ctx = build_context(args, executor)
    if out is not None:
        ctx.out = out
    try:
        return _COMMANDS[args.command](ctx, args)
    except DriverExit as exc:
        print(f"[exit {exc.code}] {exc.reason}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
