"""N1 격리 경계와 최종 심급 a/c 결정론 재실행, b 독립 k회."""
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import ClassVar
import json
import os

from jsonschema import Draft202012Validator
from reader.lib.report import CheckRow
from ..lanes.contract import LaneRequest, LanePending, LaneContractError, register_lane_vocabulary
from ..lanes.file_adapter import FileLaneAdapter
from ..lanes.plan import _accepted_models
from ..paths import RunPaths, load_stage_contract, load_format_parameters, repo_root
from ..pens import registry
from ..stages import (StageError, StageHaltError, read_text, load_json, load_yaml, sha256_file,
                      sha256_bytes, write_json, rows_to_dicts)
from ..stages import gate as gate_stage
from ..stages.design import latest_frozen
from .l1 import merge as merge_mod
from .l1.plan import l1_config, _locus_schema
from .l2.lint import hits, load_patterns

LANE_RUN = "final-eyes"
VARIANTS = registry.variant_ids(contract=load_stage_contract("compose"))
register_lane_vocabulary(LANE_RUN, (LANE_RUN,), VARIANTS)

@dataclass(frozen=True)
class FinalEyesLaneRequest(LaneRequest):
    RUNS: ClassVar[tuple] = (LANE_RUN,)
    TASKS: ClassVar[tuple] = VARIANTS


def payload_schema(repo):
    config = l1_config(repo)
    defect = {"type": "object", "additionalProperties": False,
        "required": ["rule", "locus", "expected", "observed"], "properties": {
            "rule": {"enum": config["veto_rules"]}, "locus": _locus_schema(),
            "expected": {"type": "string", "minLength": 1}, "observed": {"type": "string", "minLength": 1}}}
    audit = {"type": "object", "additionalProperties": False, "required": ["locus", "observation"],
             "properties": {"locus": _locus_schema(), "observation": {"type": "string", "minLength": 1}}}
    return {"type": "object", "additionalProperties": False, "required": ["l1_recheck", "observations"], "properties": {
        "l1_recheck": {"type": "object", "additionalProperties": False, "required": ["defects", "narrative_audit"],
            "properties": {"defects": {"type": "array", "items": defect}, "narrative_audit": {"type": "array", "items": audit}}},
        "observations": {"type": "array", "items": {"type": "string"}}}}


def provided_files(paths, variant, version):
    return [paths.thread_stripped_md(variant), paths.thread_annotated(variant),
            paths.frozen_spec(version), paths.final_eyes_brief(variant)]


def input_records(paths, files):
    return [{"path": os.path.relpath(p, paths.run_root), "digest": sha256_file(p)} for p in files]


def isolation_row(paths, files, inputs_read, brief, frozen_row=None):
    """N1 = 루프 전/후를 **생성 시점·출처**로 기계 판별한다(SPEC §1.10).

    시점의 관측은 파일시스템 mtime 이 아니라 **런이 스스로 기록한 사실**이다 — mtime 은 반입·체크아웃·사본
    생성으로 바뀌므로 「생성 시각」의 대리가 되지 못한다(발주자 오류 256 · 같은 동결본이 작업본마다 다른 값을
    낸다). 따라서 두 축으로 닫는다: ⓐ 발췌본은 스스로 루프 개시 전 산출임을 기록한다
    (`generated_before_loop` · `revision_round_at_generation`) ⓑ 동결본은 `run.yaml#frozen[]` 등재
    지문과 같아야 한다 — 루프가 만든 파일을 그 자리에 놓으면 여기서 걸린다."""
    row = CheckRow(check_id="gate.final-eyes-isolation", checked=len(files))
    expected = input_records(paths, files)
    if len(inputs_read) != len(expected) or {r["path"]: r["digest"] for r in inputs_read} != {r["path"]: r["digest"] for r in expected}:
        row.add(row.check_id, "final_eyes.inputs_read", str(inputs_read), str(expected), "제공 파일 집합 또는 지문 불일치")
    try:
        datetime.fromisoformat(brief["generated_at"].replace("Z", "+00:00"))
    except (ValueError, KeyError, TypeError) as exc:
        raise StageHaltError("gate.final-eyes-isolation: 생성 시각이 없다") from exc
    if brief.get("generated_before_loop") is not True or brief.get("revision_round_at_generation") != 0:
        row.add(row.check_id, "final-eyes-brief.json", "루프 이후", "루프 개시 전", "발췌본 출처 위반")
    if frozen_row is not None:
        frozen_path = next((p for p in files if os.path.basename(p) == os.path.basename(frozen_row["path"])), None)
        if frozen_path is None or sha256_file(frozen_path) != frozen_row["spec_digest"]:
            row.add(row.check_id, frozen_row["path"], sha256_file(frozen_path) if frozen_path else "부재",
                    frozen_row["spec_digest"], "동결본이 run.yaml 등재 지문과 다르다 — 루프 전 동결물이 아니다")
    return row


def scope_row(block):
    row = CheckRow(check_id="gate.final-eyes-scope", checked=1)
    reason = block.get("veto_reason")
    if reason not in (None, "a", "b", "c") or (block.get("verdict") == "veto") != (reason is not None):
        row.add(row.check_id, "final_eyes.veto_reason", str(reason), "null|a|b|c", "거부 사유 관할 위반")
    return row


def build_requests(paths, repo, variant, files, k, session="initial"):
    config = paths.contracts["gate"]["layers"]["final_eyes"]
    lane = config["lane"]
    slices = {os.path.relpath(p, paths.run_root): Path(p).read_bytes().decode("utf-8") for p in files}
    return [FinalEyesLaneRequest(lane_id=f"{LANE_RUN}/{variant}/batch-{i}", read_run=LANE_RUN, task=variant,
        model=lane["model"], effort=lane["effort"], prompt_path=config["procedure"], instructions=f"새 세션 식별자: {session}. 제공 파일만 재검한다.",
        repo_root=repo, slices=slices, response_schema=payload_schema(repo), batch=i,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, lane["model"])) for i in range(k)]


def run(run_root, repo=None, variant=None, adapter=None):
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    if variant not in registry.variant_ids(contract=paths.contracts["compose"]):
        raise StageError("최종 심급 변주가 계약 열거 밖이다")
    meta = load_yaml(paths.run_yaml)
    contract = paths.contracts["gate"]
    gate_stage._check_terminus(meta, repo, contract)
    verdict = load_json(paths.verdict_json(variant))
    if verdict.get("decision") != "advance":
        raise StageError("최종 심급은 decision advance 뒤에만 실행한다")
    revisions = os.path.dirname(paths.revisions_dir(variant, 1))
    if os.path.isdir(revisions):
        for base, _, names in os.walk(revisions):
            if "round.json" in names and load_json(os.path.join(base, "round.json")).get("status") == "open":
                raise StageHaltError("수정 루프가 열려 있다")
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    files = provided_files(paths, variant, version)
    if not all(os.path.isfile(p) for p in files):
        raise StageHaltError("최종 심급 제공 파일이 없다")
    brief = load_json(files[-1])
    k = gate_stage.l1_k(repo)
    if (verdict.get("final_eyes_brief_digest") != sha256_file(files[-1]) or brief.get("k") != k
        or brief.get("spec_digest") != sha256_file(files[2]) or brief.get("spec_digest") != frozen_row["spec_digest"]
        or brief.get("variant") != variant or brief.get("run_id") != meta["run_id"]):
        raise StageHaltError("gate.final-eyes-isolation: 발췌본 핀·재료·k 불일치")
    records = input_records(paths, files)
    previous = verdict.get("final_eyes") or {}
    if previous.get("verdict") and scope_row(previous).status == "fail":
        raise StageHaltError("gate.final-eyes-scope 실패")
    isolation = isolation_row(paths, files, previous.get("inputs_read") if previous.get("verdict") else records, brief, frozen_row)
    if isolation.status == "fail":
        verdict["checks"] = gate_stage._replace_rows(verdict["checks"], [isolation])
        write_json(paths.verdict_json(variant), verdict)
        raise StageHaltError("gate.final-eyes-isolation 실패")
    law = gate_stage.L0Law.load(repo)
    slots = load_format_parameters(repo)["parameters"]["slot_enum"]["value"]
    text = Path(files[1]).read_bytes().decode("utf-8")
    # a: 기존 로더와 모든 규칙을 그대로 재실행한다.
    fresh = gate_stage.judge_variant(text=text, variant=variant, run_id=meta["run_id"], spec_version=version,
        spec_digest=frozen_row["spec_digest"], frozen=load_json(files[2]), meta=meta, law=law,
        rules=gate_stage.load_rules_from_law(law), repo=repo, contract=contract,
        manifest=gate_stage._load_manifest(paths), slot_enum=slots)
    reason = "a" if fresh["l0"]["defects"] or fresh["l0"] != verdict["l0"] else None
    # c: 저장된 산출물을 대조한다. 재생성한 파일로 대조 대상을 덮지 않는다.
    roundtrip = []
    if fresh["stripped_md"] is not None:
        try:
            stripped = gate_stage.strip(text)
            published = Path(files[0]).read_bytes().decode("utf-8")
            actual = replace(stripped, stripped_md=published)
            roundtrip = gate_stage._strip_rows(text, actual, load_json(paths.thread_json(variant)),
                load_json(paths.annotation_index_json(variant)), gate_stage.parse_annotation(text, slot_enum=slots))
            broken = any(r.status == "fail" for r in roundtrip) or gate_stage.RESIDUAL_TAG_RE.search(published)
        except (ValueError, KeyError, TypeError) as exc:
            row = CheckRow(check_id=gate_stage.CHECK_REASSEMBLY, checked=1)
            row.add(row.check_id, "thread.json", str(exc), "무손실 구조화", "저장된 strip 산출이 깨졌다")
            roundtrip = [row]
            broken = True
        if reason is None and broken:
            reason = "c"
    observations = []
    merged = None
    verified = CheckRow(check_id="gate.final-eyes-lane-verified", checked=0)
    if reason is None:
        # 재판정은 별도 저장 공간이다. 레인에는 수정 라운드를 제공하지 않는다.
        root = os.path.join(paths.gate_lanes_dir(variant), "final-sessions", str(verdict.get("revision_round", 0)))
        session_path = os.path.join(root, "session.json")
        if os.path.isfile(session_path):
            session = load_json(session_path)["id"]
        else:
            # 레인에 전달되는 것은 불투명 세션 식별자뿐이다. 재료 입력은 여전히 4파일이다.
            session = sha256_bytes((root + datetime.now().isoformat()).encode()).split(":", 1)[1]
            write_json(session_path, {"id": session})
        requests = build_requests(paths, repo, variant, files, k, session=session)
        adapter = adapter or FileLaneAdapter(root, repo)
        try:
            responses = adapter.dispatch(requests)
        except LanePending as pending:
            return {"status": "pending", "pending": list(pending.pending), "lanes_root": pending.request_dir, "k": k}
        verified.checked = len(responses)
        if len(responses) != k:
            verified.add(verified.check_id, "responses", str(len(responses)), str(k), "정족수 부족")
        payloads = []
        narrative = {(t.n, s.i) for t in gate_stage.parse_annotation(text, slot_enum=slots).tweets for s in t.sentences if s.narrative}
        for request, response in zip(requests, responses):
            if response.mismatches(request) or response.lane_id != request.lane_id or response.input_digest != request.input_digest:
                verified.add(verified.check_id, response.lane_id, f"{response.model}/{response.effort}", f"{request.model}/{request.effort}", "좌석 불일치")
            errors = list(Draft202012Validator(request.response_schema).iter_errors(response.payload))
            if errors:
                raise StageHaltError("최종 심급 응답 관할/서식 위반: " + errors[0].message)
            recheck = response.payload["l1_recheck"]
            if {(r["locus"]["tweet"], r["locus"]["sentence"]) for r in recheck["narrative_audit"]} != narrative:
                raise StageHaltError("최종 심급 narrative 감사 목록 불일치")
            prose = json.dumps(response.payload, ensure_ascii=False)
            if hits(prose, load_patterns(repo)) or gate_stage.no_rewrite_violations(prose):
                raise StageHaltError("최종 심급 점수 또는 대체 문장 금지")
            payloads.append({"defects": [{**d, "fix_directive": "해당 좌표의 인용 재료 정합과 narrative 신고를 바로잡는다."} for d in recheck["defects"]]})
            observations.extend(response.payload["observations"])
        if verified.status == "fail":
            verdict["checks"] = gate_stage._replace_rows(verdict["checks"], [verified])
            write_json(paths.verdict_json(variant), verdict)
            raise StageHaltError("gate.final-eyes-lane-verified 실패")
        config = l1_config(repo)
        merged = merge_mod.merge(payloads, k=k, advisory_rules=config["advisory_rules"], flag_rule=config["flag_rule"],
            next_defect_no=len(verdict["l0"]["defects"]) + 1, next_flag_no=len(verdict["l0"]["flags"]) + 1)
        minority = {(f["rule"], f["locus"]["tweet"], f["locus"]["sentence"]) for f in merged["flags"]}
        observations.extend(d["observed"] for p in payloads for d in p["defects"]
                            if (d["rule"], d["locus"]["tweet"], d["locus"]["sentence"]) in minority)
        reason = "b" if merged["defects"] else None
    # 응답을 기다리는 사이 입력이 바뀌면 판정하지 않는다.
    isolation = isolation_row(paths, files, records, brief, frozen_row)
    if isolation.status == "fail":
        raise StageHaltError("gate.final-eyes-isolation: 실행 중 입력 변경")
    block = {"verdict": "veto" if reason else "pass", "veto_reason": reason,
             "observations": list(dict.fromkeys(observations)), "inputs_read": records}
    scope = scope_row(block)
    verdict["final_eyes"] = block
    verdict["checks"] = gate_stage._replace_rows(verdict["checks"], [isolation, scope, verified])
    verdict["inactive_layers"] = [r for r in verdict["inactive_layers"] if r["layer"] != "final_eyes"]
    if reason:
        verdict["thread_digest"] = sha256_bytes(text.encode())
        # 기존 revise가 소비하는 결함 필드에 재검 결과를 둔다.
        if reason == "a":
            verdict["l0"] = fresh["l0"]
        elif reason == "b":
            verdict["l1"] = merged
        if not any(verdict[layer]["defects"] for layer in ("l0", "l1")):
            verdict["l0"]["defects"] = [{"id": "d-l0-final", "layer": "l0", "rule": "annotation.schema",
                "locus": {"tweet": 1, "sentence": 1}, "expected": "주석층과 strip의 무손실 일치", "observed": "최종 심급 재실행 불일치",
                "fix_directive": "해당 주석층의 정합을 복구하여 gate 산출물을 재생성한다."}]
            verdict["l0"]["pass"] = False
        verdict["decision"] = gate_stage.decide(l0_pass=False, l1_pass=False,
            revision_round=int(verdict.get("revision_round", 0)), cap=gate_stage.revision_cap(contract))
        if verdict["decision"] == "escalate":
            write_json(paths.gate_escalation_json(variant), {"reason": reason, "final_eyes": block, "revision_round": verdict["revision_round"]})
    verdict["vacuous_pass"] = [r["check_id"] for r in verdict["checks"] if r["vacuous"] != "none"]
    write_json(paths.l0_json(variant), verdict["l0"])
    write_json(paths.l1_json(variant), verdict["l1"])
    write_json(paths.verdict_json(variant), verdict)
    write_json(os.path.join(paths.gate_dir(variant), "final-eyes-report.json"), {
        "produced_at": gate_stage._now_iso(), "final_eyes": block, "runner_inputs": input_records(paths, [paths.thread_json(variant), paths.annotation_index_json(variant)]),
        "l0": fresh["l0"], "roundtrip": rows_to_dicts(roundtrip), "l1_recheck": merged})
    return {"status": "escalate" if verdict["decision"] == "escalate" else "ok", "decision": verdict["decision"], "final_eyes": block}
