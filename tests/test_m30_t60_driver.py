# -*- coding: utf-8 -*-
"""M30 — READ 부분 런 구동기 `tools/drive_partial_read.py`(재정 T60 집행 · 설계 D-20260913-03 §9).

실제 `claude` 는 한 번도 부르지 않는다 — 실행기는 전부 이 파일의 스텁이다. 09-01 런 픽스처는
읽기만 한다. 섀도 원장은 임시 법 리포의 주 트리로 해석되므로 생산 원장에 닿지 않는다.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
if os.path.join(REPO, "tests") not in sys.path:
    sys.path.insert(0, os.path.join(REPO, "tests"))

import test_m2_read as m2  # noqa: E402
from engine.lanes.contract import LaneRequest, load_response  # noqa: E402
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.lanes.plan import DECOMPOSE_SCHEMA, RESPONSE_SCHEMAS, _accepted_models, lane_profiles  # noqa: E402
from engine.paths import load_stage_contract  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.stages import freeze as freeze_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

FIXTURE_LANE = os.path.join(
    REPO, "runs", "gdm-wo2026128750a1-agent-memory", "10-read", "lanes",
    "read-a", "decompose", "batch-0",
)
PROFILES = lane_profiles(REPO)


# ---------------------------------------------------------------------------
# 스텁 실행기 — `claude -p` 의 json 출력 형태를 흉내 낸다
# ---------------------------------------------------------------------------


def _row(text: str, label: str) -> str:
    prefix = f"| {label} | `"
    for line in text.split("\n"):
        if line.startswith(prefix):
            return line[len(prefix):].split("`", 1)[0]
    return ""


class Stub:
    """레인 출력을 (read_run, task) 별 payload 로 낸다. 호출 기록을 든다."""

    def __init__(self, payloads_by_run: dict, *, model_override: str | None = None,
                 is_error: bool = False, timed_out: bool = False, drop_usage: bool = False,
                 payload_override: dict | None = None):
        self.payloads_by_run = payloads_by_run
        self.model_override = model_override
        self.is_error = is_error
        self.timed_out = timed_out
        self.drop_usage = drop_usage
        self.payload_override = payload_override
        self.calls: list[list[str]] = []

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        read_run, task = _row(text, "독립 실행"), _row(text, "작업")
        digest = _row(text, "입력 지문")
        api_id = argv[argv.index("--model") + 1]
        if self.timed_out:
            return drv.ExecResult(-1, b"", b"[driver] wall clock exceeded", True, timeout * 1000)
        if self.is_error:
            body = {"type": "result", "is_error": True, "result": "stub failure"}
            return drv.ExecResult(1, json.dumps(body).encode(), b"boom", False, 5)
        payload = self.payload_override if self.payload_override is not None else self.payloads_by_run[read_run][task]
        observed = self.model_override or api_id
        body = {
            "type": "result", "subtype": "success", "is_error": False, "num_turns": 1,
            "duration_ms": 7, "total_cost_usd": 0.01, "session_id": f"stub-{len(self.calls)}",
            "structured_output": {
                "lane_id": lane_id, "model": "self-reported", "effort": "self-effort",
                "input_digest": digest, "payload": payload,
            },
        }
        if not self.drop_usage:
            body["modelUsage"] = {observed: {"inputTokens": 10, "outputTokens": 20}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 7)


# ---------------------------------------------------------------------------
# 픽스처 — 법 리포(main 브랜치) · 런 worktree 배치 · 단독 좌표
# ---------------------------------------------------------------------------


def _git(cwd: str, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        pytest.fail(f"git {' '.join(args)} 실패: {proc.stderr}")
    return proc.stdout.strip()


def make_law_repo(destination: str) -> str:
    """contracts + reader 를 담은 깨끗한 git 리포 · 브랜치 main."""
    os.makedirs(destination, exist_ok=True)
    for tree in ("contracts", "reader"):
        shutil.copytree(os.path.join(REPO, tree), os.path.join(destination, tree),
                        ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
    _git(destination, "init", "-q", "-b", "main")
    _git(destination, "config", "user.email", "runner@example.com")
    _git(destination, "config", "user.name", "runner")
    _git(destination, "add", "contracts", "reader")
    _git(destination, "commit", "-q", "-m", "law")
    return destination


class Harness:
    def __init__(self, tmp_path):
        self.tmp = str(tmp_path)
        self.law = make_law_repo(os.path.join(self.tmp, "law"))
        self.wt_root = os.path.join(self.tmp, "wt")
        self.run_id = m2.RUN_ID
        self.worktree = os.path.join(self.wt_root, self.run_id)
        self.run_root = os.path.join(self.worktree, "runs", self.run_id)
        self.evidence = os.path.join(self.worktree, "evidence")
        self.lines: list[str] = []

    def base(self, *extra: str) -> list[str]:
        return ["--repo", self.law, "--worktree-root", self.wt_root, *extra]

    def run(self, *argv: str, executor=None, dry_run: bool = False) -> int:
        self.lines = []
        head = self.base("--dry-run") if dry_run else self.base()
        return drv.main([*head, *argv], executor=executor, out=self.lines.append)

    def init(self) -> int:
        patent, figures = m2.make_source_inputs(self.tmp)
        meta = os.path.join(self.tmp, "meta.json")
        with open(meta, "w", encoding="utf-8") as handle:
            json.dump(m2.PATENT_META, handle)
        return self.run("init", self.run_id, "--source", patent, "--figures", figures, "--patent-meta", meta)

    def paths(self) -> RunPaths:
        return RunPaths(self.run_root, self.worktree)

    def quote(self, text: str) -> str:
        path = os.path.join(self.tmp, "quote.txt")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def adjudicated(self, entries: list) -> str:
        path = os.path.join(self.tmp, "adjudicated.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(entries, handle)
        return path


def payloads_with_requests() -> dict:
    payloads = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    payloads["read-a"]["ground-independent"]["review_requests"] = [{"target": "M4", "reason": "조응."}]
    payloads["read-a"]["synthesize"]["review_requests"] = [{"target": "M10", "reason": "귀속."}]
    return payloads


def single_lane(tmp_path, *, model: str = "fable-5.1", effort: str = "low", task: str = "decompose"):
    """엔진 어댑터로 요청 한 좌표를 렌더한 단독 문맥(법 = 본 리포)."""
    lanes = os.path.join(str(tmp_path), "lanes")
    fixture = json.load(open(os.path.join(FIXTURE_LANE, "request.json"), encoding="utf-8"))
    fields = {k: v for k, v in fixture.items() if k != "input_digest"}
    fields.update({"model": model, "effort": effort, "task": task, "lane_id": f"read-a/{task}/batch-0"})
    accepted = _accepted_models(load_stage_contract("read", REPO).get("lane") or {}, model)
    request = LaneRequest(**fields, repo_root=REPO, accepted_models=accepted)
    FileLaneAdapter(lanes, repo=REPO).write_request(request)
    lines: list[str] = []
    ctx = drv.Context(run_id="x", repo=REPO, worktree=str(tmp_path), run_root=os.path.join(str(tmp_path), "runs", "x"),
                      evidence=os.path.join(str(tmp_path), "evidence"), law=REPO, executor=lambda *a: None, out=lines.append)
    return ctx, lanes, request, lines


def receipt(ctx, lane_id: str) -> dict:
    return json.load(open(os.path.join(ctx.calls_dir, drv.safe_lane_name(lane_id) + ".json"), encoding="utf-8"))


# ---------------------------------------------------------------------------
# ⑴ ⑵ 명령줄 · 스키마
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑶ ⑷ 응답 파일의 model · effort
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑹ ⑺ ⑻ 실패 처분
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑼ 09-01 런 픽스처 왕복
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑽ ⑾ ⑿ 전 명령 흐름 · 봉투 · continue · 영수증 · MANIFEST · dry-run
# ---------------------------------------------------------------------------


def _findings(outcome) -> list[str]:
    return [finding.rule for row in outcome["rows"] for finding in row.findings]


def test_full_flow_init_step_cp1_approve_freeze_seal(tmp_path) -> None:
    h = Harness(tmp_path)
    if h.init() != drv.EXIT_OK:
        pytest.fail(f"init 실패: {h.lines}")
    if h.init() != drv.EXIT_OK:
        pytest.fail("init 재진입이 0 이 아니다")
    stub = Stub(payloads_with_requests())
    code = h.run("step", h.run_id, executor=stub)
    if code != drv.EXIT_CP1_WAIT:
        pytest.fail(f"step 이 CP1 대기(20)가 아니다: {code} · {h.lines}")
    tasks = sorted({call[call.index("--model") + 1] for call in stub.calls})
    if tasks != ["claude-fable-5-1", "claude-opus-5"]:
        pytest.fail(f"호출 모델이 계약 좌석과 다르다: {tasks}")
    calls_before = len(stub.calls)
    if h.run("step", h.run_id, executor=stub) != drv.EXIT_CP1_WAIT or len(stub.calls) != calls_before:
        pytest.fail("step 재진입이 다시 호출했다")
    if h.run("lanes", h.run_id) != drv.EXIT_OK or not any(line.startswith("완료") for line in h.lines):
        pytest.fail(f"lanes 조회가 다르다: {h.lines}")
    if h.run("continue", h.run_id, "--quote-file", h.quote("계속")) != drv.EXIT_USAGE:
        pytest.fail("상신 축 미달이 아닌데 continue 가 2 로 서지 않았다")

    if h.run("cp1", h.run_id) != drv.EXIT_OK:
        pytest.fail(f"cp1 실패: {h.lines}")
    joined = "\n".join(h.lines)
    if "review_requests: 2건" not in joined or "## 8-b" not in joined or '"verdict": ""' not in joined:
        pytest.fail(f"cp1 출력이 규격과 다르다: {joined}")
    targets = [e["target"] for e in json.load(open(h.paths().convergence_json, encoding="utf-8"))["review_requests"]]
    ack = ["--derived-ack", m2.DERIVED_FACT_ID, "--manual-ack", m2.FIGURE_FACT_ID,
           "--decided-at", "2026-09-13T00:00:00Z"]
    quote = h.quote("이 재료로 CP1 승인한다.")

    def approve(entries, decision="approved", *extra):
        return h.run("approve", h.run_id, "--quote-file", quote, "--adjudicated", h.adjudicated(entries),
                     "--decision", decision, *ack, *extra)

    # 실패 픽스처 3 — 빠짐 · 유령 · defect+approved
    if approve([{"target": targets[0], "verdict": "confirmed"}]) != drv.EXIT_OK:
        pytest.fail("빠짐 봉투 작성이 막혔다(구동기는 경고만 한다)")
    if not any("답이 없다" in line for line in h.lines):
        pytest.fail("빠짐 경고가 없다")
    missing = freeze_stage.run(run_root=h.run_root, spec_version=1, rules=m2.RULES, repo=h.worktree)
    if "approval.review-complete" not in _findings(missing):
        pytest.fail(f"빠짐 봉투가 항 ④ 를 통과했다: {_findings(missing)}")
    if h.run("freeze", h.run_id) != drv.EXIT_TERMINAL_FAIL:
        pytest.fail("빠짐 봉투인데 freeze 가 13 이 아니다")

    approve([{"target": t, "verdict": "confirmed"} for t in targets] + [{"target": "M77", "verdict": "confirmed"}])
    phantom = freeze_stage.run(run_root=h.run_root, spec_version=2, rules=m2.RULES, repo=h.worktree)
    if "approval.review-no-phantom" not in _findings(phantom):
        pytest.fail(f"유령 봉투가 항 ④ 를 통과했다: {_findings(phantom)}")

    approve([{"target": targets[0], "verdict": "defect"}, {"target": targets[1], "verdict": "confirmed"}])
    defect = freeze_stage.run(run_root=h.run_root, spec_version=3, rules=m2.RULES, repo=h.worktree)
    if "approval.review-defect-approved" not in _findings(defect):
        pytest.fail(f"defect+approved 가 항 ④ 를 통과했다: {_findings(defect)}")

    # 통과 픽스처 1 — 전건 답(undecided 포함) · 스키마 통과 · freeze ok
    if approve([{"target": targets[0], "verdict": "confirmed"}, {"target": targets[1], "verdict": "undecided", "note": "판정 불가"}]) != drv.EXIT_OK:
        pytest.fail(f"승인 봉투 작성 실패: {h.lines}")
    envelope = freeze_stage.parse_envelope(open(h.paths().approval(4), encoding="utf-8").read())
    schema = json.load(open(os.path.join(REPO, *freeze_stage.APPROVAL_SCHEMA), encoding="utf-8"))
    if list(Draft202012Validator(schema).iter_errors(envelope)):
        pytest.fail("작성한 봉투가 스키마를 위반한다")
    if envelope["owner_quote"] != "이 재료로 CP1 승인한다." or envelope["recorded_by"] != "orchestrator" or envelope["checkpoint"] != "material_approval":
        pytest.fail(f"봉투 필드가 다르다: {envelope}")
    if h.run("freeze", h.run_id) != drv.EXIT_OK:
        pytest.fail(f"freeze 실패: {h.lines}")
    if not os.path.isfile(h.paths().frozen_spec(4)):
        pytest.fail("동결본이 없다")

    # 영수증 서식
    rec = receipt(drv.Context("x", REPO, h.worktree, h.run_root, h.evidence, h.worktree, stub), "read-a/decompose/batch-0")
    required = {"lane_id", "request_md_sha256", "response_json_sha256", "requested", "observed", "lane_self_report",
                "is_error", "num_turns", "total_cost_usd", "duration_ms", "session_id", "stderr_tail", "started_at", "ended_at", "attempt"}
    if not required <= set(rec) or rec["requested"] != {"model": "fable-5.1", "effort": "low", "api_id": "claude-fable-5-1"}:
        pytest.fail(f"영수증 서식이 다르다: {sorted(rec)}")
    if not rec["observed"]["modelUsage"] or rec["observed"]["main_model"] != "claude-fable-5-1":
        pytest.fail(f"영수증 관측이 비었다: {rec['observed']}")
    with open(os.path.join(h.evidence, "calls", "read-a__decompose__batch-0.raw.json"), encoding="utf-8") as handle:
        if json.load(handle)["type"] != "result":
            pytest.fail("원시 출력이 보존되지 않았다")

    # seal — MANIFEST 서식 · 대상 집합
    if h.run("seal", h.run_id) != drv.EXIT_OK:
        pytest.fail(f"seal 실패: {h.lines}")
    manifest = open(os.path.join(h.evidence, "MANIFEST-sha256.txt"), encoding="utf-8").read().splitlines()
    rels = [line.split("  ", 1)[1] for line in manifest]
    if any(len(line.split("  ", 1)[0]) != 64 for line in manifest) or rels != sorted(rels):
        pytest.fail("MANIFEST 행 서식·정렬이 다르다")
    run_rel = f"runs/{h.run_id}"
    if f"{run_rel}/15-frozen/approval-v4.md" not in rels or f"{run_rel}/10-read/convergence.json" not in rels \
            or "evidence/calls/read-a__decompose__batch-0.json" not in rels or "evidence/MANIFEST-sha256.txt" in rels:
        pytest.fail(f"MANIFEST 대상 집합이 다르다: {rels}")
    if not any(rel.startswith("evidence/schemas/") for rel in rels):
        pytest.fail("스키마 파일이 MANIFEST 에 없다")


def test_step_stops_with_pending_when_a_lane_fails_and_dry_run_writes_nothing(tmp_path) -> None:
    h = Harness(tmp_path)
    if h.init() != drv.EXIT_OK:
        pytest.fail(f"init 실패: {h.lines}")
    failing = Stub({}, is_error=True)
    if h.run("step", h.run_id, executor=failing) != drv.EXIT_PENDING:
        pytest.fail(f"실패 좌표가 10 으로 서지 않았다: {h.lines}")
    pending_before = sorted(row["lane_id"] for row in drv.lane_inventory(h.paths().lanes_dir) if not row["response"])
    # 엔진은 독립 실행을 하나씩 발송하므로 첫 실패 뒤 대기는 read-a 한 좌표다.
    if pending_before != ["read-a/decompose/batch-0"]:
        pytest.fail(f"read-a 분해 좌표가 대기여야 한다: {pending_before}")
    snapshot = {os.path.join(d, f) for d, _, fs in os.walk(h.worktree) for f in fs if ".git" not in d}
    if h.run("step", h.run_id, executor=failing, dry_run=True) != drv.EXIT_PENDING:
        pytest.fail("dry-run 이 대기 좌표를 인쇄하지 않았다")
    after = {os.path.join(d, f) for d, _, fs in os.walk(h.worktree) for f in fs if ".git" not in d}
    if after != snapshot or len(failing.calls) != 1:
        pytest.fail("dry-run 이 파일을 썼거나 실행기를 불렀다")
    if not all(line.startswith("[dry-run] read-") and "--setting-sources project" in line for line in h.lines):
        pytest.fail(f"dry-run 출력이 명령줄이 아니다: {h.lines}")
    # 같은 좌표를 다시 부른다 · 성공하면 계속 간다
    good = Stub({"read-a": m2.payload_set(), "read-b": m2.payload_set()})
    if h.run("step", h.run_id, executor=good) != drv.EXIT_CP1_WAIT:
        pytest.fail(f"재진입 뒤 CP1 대기가 아니다: {h.lines}")
    if receipt(drv.Context("x", REPO, h.worktree, h.run_root, h.evidence, h.worktree, good), "read-a/decompose/batch-0")["attempt"] != 2:
        pytest.fail("재호출 회차가 2 가 아니다")


def test_continue_envelope_binds_verdict_and_unblocks_grounding(tmp_path) -> None:
    h = Harness(tmp_path)
    if h.init() != drv.EXIT_OK:
        pytest.fail(f"init 실패: {h.lines}")
    payloads = {"read-a": m2.payload_set(), "read-b": m2.payload_set(element_two=m2.E2_TEXT_VARIANT)}
    stub = Stub(payloads)
    if h.run("step", h.run_id, executor=stub) != drv.EXIT_CONTINUE_POSSIBLE:
        pytest.fail(f"상신 축 미달이 11 로 서지 않았다: {h.lines}")
    if h.run("continue", h.run_id, "--quote-file", h.quote("계속 진행한다."), "--decided-at", "2026-09-13T00:00:00Z") != drv.EXIT_OK:
        pytest.fail(f"continue 실패: {h.lines}")
    envelope = freeze_stage.parse_envelope(open(h.paths().convergence_continue_md, encoding="utf-8").read())
    if envelope["checkpoint"] != "convergence_continue" or envelope["target"]["path"] != "10-read/convergence-early.json" \
            or envelope["target"]["digest"] != "sha256:" + drv._sha256_file(h.paths().convergence_early_json):
        pytest.fail(f"계속 봉투 결속이 다르다: {envelope}")
    if h.run("step", h.run_id, executor=stub) != drv.EXIT_CP1_WAIT:
        pytest.fail(f"봉투 뒤 접지·통합이 CP1 까지 가지 않았다: {h.lines}")
    gate = json.load(open(h.paths().phase_gate_json, encoding="utf-8"))
    if not gate.get("entered") or not gate["envelope"]["applied"]:
        pytest.fail(f"게이트가 봉투로 진입하지 않았다: {gate}")


def test_help_lists_fourteen_commands() -> None:
    parser = drv.build_parser()
    listed = parser._subparsers._group_actions[0].choices  # noqa: SLF001 - 명령 집합 대조
    if tuple(listed) != drv.COMMANDS or len(drv.COMMANDS) != 26:
        pytest.fail(f"명령 26 가 아니다(T69 ⑥ · gate-l2·revise-free·probe): {tuple(listed)}")


def _echo_stub(lane_id_echo: str, digest_echo: str):
    class Echo:
        calls: list = []
        def __call__(self, argv, stdin, env, timeout):
            self.calls.append(argv)
            body = {"lane_id": lane_id_echo, "model": "fable-5.1", "effort": "low",
                    "input_digest": digest_echo, "payload": {"items": []}}
            out = {"result": json.dumps(body), "structured_output": body, "is_error": False,
                   "modelUsage": {"claude-fable-5-1": {"outputTokens": 10}}, "num_turns": 1,
                   "total_cost_usd": 0.1, "duration_ms": 5, "session_id": "s"}
            return drv.ExecResult(0, json.dumps(out).encode(), b"", False, 5)
    return Echo()

