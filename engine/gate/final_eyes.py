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


def _fix_directive(defect: dict) -> str:
    """최종 심급 결함의 수정 지시문 — 레인이 쓴 `expected`(정합 조건)·`observed`(발견 사실)에서 만든다.

    재정 2026-09-14 T70 ①. 고정 문구(「해당 좌표의 인용 재료 정합과 narrative 신고를 바로잡는다」)를 넘기면
    펜이 좌표만 받고 **무엇이 왜 어긋나는지** 모른다 — 런 -3 에서 같은 결함(T6/S2)이 두 회차 연속 남았고,
    구체적 지시문을 받은 게이트 L1 의 결함은 한 라운드에 고쳐졌다. `expected`·`observed` 는 조건과 사실이지
    고쳐 쓴 문장이 아니므로 D8 규율 3 에 저촉되지 않으며, 지시문은 `gate.no-rewrite` 검사를 그대로 받는다.
    """
    expected = str(defect.get("expected") or "").strip()
    observed = str(defect.get("observed") or "").strip()
    parts = [t for t in (expected, observed) if t]
    if not parts:
        return "해당 좌표의 인용 재료 정합과 narrative 신고를 바로잡는다."
    body = " / ".join(parts)
    return f"{body} — 이 좌표의 인용 재료 정합과 narrative 신고를 그에 맞게 바로잡는다."


def waive(*, run_root: str, repo: str | None = None, variant: str, owner_quote: str, located_at: str) -> dict:
    """최종 심급의 거부를 **Owner 재정으로 관할 밖 소견으로 강등**한다(계약 `gate.yaml#layers.final_eyes.waiver`).

    거부권을 무를 수 있는 것은 Owner 뿐이다(재정 R4 — 관할 밖 발견의 판정자는 Owner · D8·D15). 캡이 소진된
    뒤의 에스컬레이션에서 「체크포인트로 두자」는 재정이 오면, 심급이 쓴 결함 문언을 **한 글자도 바꾸지 않고**
    `observations[]` 로 옮겨 CP2 표면에 싣는다. 강등 사실은 `waived` 블록으로 남아 표면에서 숨겨지지 않는다.
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError(f"verdict.json 이 없다: {verdict_path}")
    verdict = load_json(verdict_path)
    block = verdict.get("final_eyes") or {}
    if block.get("verdict") != "veto":
        raise StageError(f"최종 심급이 거부 상태가 아니다({block.get('verdict')}) — 강등할 것이 없다")
    if not os.path.isfile(paths.gate_escalation_json(variant)):
        raise StageError("에스컬레이션 기록이 없다 — 캡 소진 뒤의 재정에만 쓴다")
    quote = (owner_quote or "").strip()
    if not quote:
        raise StageError("Owner 육성 인용이 비었다 — 강등은 재정으로만 한다")
    defects = [dict(d) for d in ((verdict.get("l1") or {}).get("defects") or []) if d.get("layer") == "l1" or True]
    carried = [
        f"[강등된 최종 심급 결함] {d.get('rule')} · T{d['locus']['tweet']}/S{d['locus']['sentence']} — {d.get('observed')}"
        for d in defects if d.get("locus")
    ]
    block["observations"] = carried + [o for o in (block.get("observations") or [])]
    block["verdict"] = "pass"
    block["veto_reason"] = None
    block["waived"] = {
        "by": "owner", "quote": quote, "located_at": located_at, "recorded_at": gate_stage._now_iso(),
        "defect_count": len(carried), "escalation": "50-gate/%s/escalation.json" % variant,
    }
    verdict["final_eyes"] = block
    verdict["decision"] = gate_stage.DECISION_ADVANCE
    write_json(verdict_path, verdict)
    return {"status": "waived", "carried": len(carried), "decision": verdict["decision"]}


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
        # 자리를 가르는 키는 수정 회차 **와 요청 지문**이다 — 절차 문서를 고치면 요청이 바뀌고, 그때 옛 자리에
        # 남은 응답은 새 요청의 답이 될 수 없다(레인 결속). 회차만으로 가르면 러너가 매 회 그 응답을 만나 멈춘다.
        probe = build_requests(paths, repo, variant, files, 1, session="probe")[0]
        session_key = f"{verdict.get('revision_round', 0)}-{str(probe.input_digest).split(':')[-1][:12]}"
        root = os.path.join(paths.gate_lanes_dir(variant), "final-sessions", session_key)
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
            # 등급 어휘는 낱말 검사이므로 직렬화 문자열에 걸어도 된다. 그러나 **대체 문장 검사는 저자가 쓴
            # 따옴표를 본다** — 직렬화 문자열에 걸면 JSON 문법의 따옴표가 필드 값 전체를 「인용」으로 만들고,
            # 한국어 서술 안의 재료 ID 나열(M12·M26·M63·M77)이 영어 낱말 다섯으로 세어져 오탐이 난다.
            # 런 -3 실측 = 전체 직렬화 3건 위반 · 필드별 0건(저자가 쓴 따옴표 인용은 하나도 없었다).
            written = [str(t) for t in response.payload.get("observations", [])]
            for item in recheck["defects"]:
                written += [str(item.get("expected", "")), str(item.get("observed", ""))]
            for item in recheck["narrative_audit"]:
                written.append(str(item.get("observation", "")))
            if hits(prose, load_patterns(repo)) or any(gate_stage.no_rewrite_violations(t) for t in written):
                raise StageHaltError("최종 심급 점수 또는 대체 문장 금지")
            payloads.append({"defects": [{**d, "fix_directive": _fix_directive(d)} for d in recheck["defects"]]})
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
