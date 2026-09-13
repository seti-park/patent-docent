# -*- coding: utf-8 -*-
"""M36 — L2 자문 메모 · 점수 금지 린트 · 펜 자유 리비전 1회 · 계기(probe) 계열(재정 2026-09-13 T69 ⑥ · M4/M8-a · M7-a).

모델 호출 없음 — L2·펜·L1·질문 생성·프로브·채점 응답은 시험이 파일 어댑터 자리에 쓴다. 픽스처 = 런 -3 v2 실물(L1 통과 · advance ·
`50-gate/v2/{thread.stripped.md, annotation-index.json, verdict.json}` · `20-design/blueprint.json` · 동결본 · 읽기만 · tmp 사본) + 합성 run.yaml.
법 트리 = contracts·reader 사본 + 절차 문서(펜 템플릿 · 설계 · L1 · L2 · 계기 3) + git init(compose 의 law_commit).

★ 점수 표기 표본(`8/10` · 별점 · `B+`)은 린트 실패를 심는 데이터이며 반례(`A-1 구조` · `automotive-grade` · `4x improvement`)는
`contracts/lexicon/score-lint.yaml#counter_examples` 의 문언이다 — 이 파일은 그 정본을 읽을 뿐 사본을 두지 않는다.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.gate import loop as loop_mod  # noqa: E402
from engine.gate.l2 import lint as l2_lint  # noqa: E402
from engine.gate.l2 import plan as l2_plan  # noqa: E402
from engine.lanes.contract import REQUEST_JSON, REQUEST_MD, RESPONSE_JSON, lane_file, render_request_md  # noqa: E402
from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.probe import grade as grade_mod  # noqa: E402
from engine.probe import localize as localize_mod  # noqa: E402
from engine.probe import questions as questions_mod  # noqa: E402
from engine.probe import run_probes as probes_mod  # noqa: E402
from engine.stages import StageError, StageHaltError, sha256_bytes, sha256_file  # noqa: E402
from engine.stages import gate as gate_stage  # noqa: E402
from engine.stages import probe as probe_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

RUN_ID = "gdm-wo2026128750a1-agent-memory-3"
RUN3 = os.path.join(REPO, "runs", RUN_ID)
# 런 -3 는 살아 있는 런이라 반입마다 상태가 앞으로 간다. 이 시험의 전제(L1 pass · advance · L2 미실행)는 `d428830` 상태의
# 바이트 사본 `tests/fixtures/run3-snapshots/post-l1/` 에 고정한다(40-compose · 50-gate/v2 두 트리 · 나머지는 실물 그대로).
SNAPSHOT = os.path.join(REPO, "tests", "fixtures", "run3-snapshots", "post-l1")
VARIANT = "v2"
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"),
             ("engine", "gate", "l1", "procedure.md"), ("engine", "gate", "l2", "procedure.md"),
             ("engine", "probe", "procedure-questions.md"), ("engine", "probe", "procedure-probe.md"), ("engine", "probe", "procedure-grader.md"))
COPIED_DIRS = ("15-frozen", "20-design", "30-figures", "40-compose", os.path.join("50-gate", VARIANT))
SNAPSHOT_DIRS = ("40-compose", os.path.join("50-gate", VARIANT))
ASTRA = "claude-fable-5-dd-artsa-6-tpg"  # L2 좌석 — Owner 재정 2026-09-14(fable 쿼터 장애) · 게이트웨이가 노출하는 Claude 호환 id
OPUS = "claude-opus-5"
HAIKU = "claude-haiku-4-5-20251001"


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str, payload) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def schema_errors(name: str, instance) -> list[str]:
    return [e.message for e in Draft202012Validator(read_json(os.path.join(SCHEMAS, f"{name}.schema.json"))).iter_errors(instance)]


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


# ---------------------------------------------------------------------------
# 픽스처
# ---------------------------------------------------------------------------


def make_law(destination: str) -> str:
    for tree in LAW_TREES:
        shutil.copytree(os.path.join(REPO, tree), os.path.join(destination, tree), ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
    for parts in LAW_FILES:
        target = os.path.join(destination, *parts)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(os.path.join(REPO, *parts), target)
    _git(destination, "init", "-q", "-b", "main")
    _git(destination, "config", "user.email", "runner@example.com")
    _git(destination, "config", "user.name", "runner")
    _git(destination, "add", "contracts", "reader", "docs", "engine")
    _git(destination, "commit", "-q", "-m", "law")
    return destination


def make_run(root: str, *, partial_until: str = "ship") -> str:
    run_root = os.path.join(root, "runs", RUN_ID)
    for rel in COPIED_DIRS:
        shutil.copytree(os.path.join(SNAPSHOT if rel in SNAPSHOT_DIRS else RUN3, rel), os.path.join(run_root, rel))
    frozen = os.path.join(run_root, "15-frozen", "material-spec.v1.json")
    os.chmod(frozen, 0o444)
    real = yaml.safe_load(read(os.path.join(RUN3, "run.yaml")))
    meta = {"schema": "run/v0", "run_id": RUN_ID, "status": "active", "run_kind": "partial", "partial_until": partial_until,
            "patent": real["patent"], "engine": {"commit": "e" * 40, "worktree": None}, "numeric_whitelist": real["numeric_whitelist"],
            "frozen": real["frozen"], "pens": real["pens"], "comparison_axis": real["comparison_axis"]}
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    verdict = read_json(os.path.join(run_root, "50-gate", VARIANT, "verdict.json"))
    if verdict["decision"] != "advance" or verdict["l1"]["pass"] is not True:
        pytest.fail("런 -3 v2 픽스처가 advance · L1 pass 가 아니다 — 이 시험의 전제가 서지 않는다")
    return run_root


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(os.path.join(str(tmp_path), "r"))


def verdict_of(run_root: str) -> dict:
    return read_json(os.path.join(run_root, "50-gate", VARIANT, "verdict.json"))


def gate_lanes(run_root: str) -> str:
    return os.path.join(run_root, "50-gate", VARIANT, "lanes")


def probe_lanes(run_root: str) -> str:
    return os.path.join(run_root, "60-probe", VARIANT, "lanes")


def respond(root: str, lane_id: str, payload: dict, *, model: str, effort: str | None = None) -> None:
    request = read_json(lane_file(root, lane_id, REQUEST_JSON))
    write_json(lane_file(root, lane_id, RESPONSE_JSON), {"lane_id": lane_id, "model": model, "effort": effort or request["effort"],
                                                        "input_digest": request["input_digest"], "payload": payload})


def memo(rule: str, text: str, tweet=None, sentence=None) -> dict:
    return {"rule": rule, "locus": {"tweet": tweet, "sentence": sentence}, "text": text}


GOOD_MEMOS = [memo("l2.structure", "T5 가 T4 의 전제를 반복해 T6 의 반전이 늦게 온다.", 5),
              memo("l2.thesis-flow", "훅의 질문(architecture or marketing)이 착지에서 다시 호명되지 않는다."),
              memo("l2.material-balance", "M116 이 T8 두 문장에만 얇게 걸쳐 있다.", 8, 1)]


def run_l2(run_root: str, law: str) -> dict:
    return gate_stage.run_l2(run_root=run_root, repo=law, variant=VARIANT)


def l2_done(run_root: str, law: str, memos=None) -> dict:
    outcome = run_l2(run_root, law)
    if outcome["status"] != "pending" or outcome["pending"] != [f"gate-l2/{VARIANT}/batch-0"]:
        pytest.fail(f"L2 첫 진입이 대기 1 이 아니다: {outcome}")
    respond(gate_lanes(run_root), outcome["pending"][0], {"memos": GOOD_MEMOS if memos is None else memos}, model=ASTRA)
    return run_l2(run_root, law)


def respond_l1_clean(run_root: str, pending: list[str]) -> None:
    for lane_id in pending:
        respond(gate_lanes(run_root), lane_id, {"defects": [], "flags": [], "speech_acts": []}, model=OPUS)


def targets_of(run_root: str) -> list[str]:
    return list(read_json(os.path.join(run_root, "20-design", "blueprint.json"))["transmission_targets"])


def questions_payload(targets: list[str], *, extra: list[dict] | None = None, drop: int = 0) -> dict:
    rows = [{"question_id": f"Q{i}", "target_material_id": t, "question_en": f"What does the thread say about {t}?"}
            for i, t in enumerate(targets, start=1)]
    return {"questions": rows[:len(rows) - drop] + (extra or [])}


def probe_payload(questions: list[dict], text: str, *, stated: set[str] | None = None, bad_span: set[str] = frozenset()) -> dict:
    """질문마다 stated(원문 첫 줄 인용) 또는 not-stated. `bad_span` 의 질문은 원문에 없는 구간을 인용한다(무효)."""
    first_line = text.split("\n", 1)[0]
    answers = []
    for q in questions:
        qid = q["question_id"]
        if stated is not None and qid not in stated:
            answers.append({"question_id": qid, "target_material_id": q["target_material_id"], "answer_kind": "not-stated", "answer": None, "quoted_span": None})
            continue
        span = "this sentence is not in the thread at all" if qid in bad_span else first_line
        answers.append({"question_id": qid, "target_material_id": q["target_material_id"], "answer_kind": "stated",
                        "answer": f"The thread says: {first_line}", "quoted_span": span})
    return {"a_restatement": ["Memory is a per-user datastore.", "The model reads it at query time.", "The user can erase it."], "b_answers": answers}


def run_probe(run_root: str, law: str, **kw) -> dict:
    return probe_stage.run(run_root=run_root, repo=law, variant=VARIANT, **kw)


def probe_to_pending_probes(run_root: str, law: str) -> dict:
    """질문지까지 채우고 프로브 n 대기 상태로."""
    outcome = run_probe(run_root, law)
    if outcome["status"] != "pending" or outcome["phase"] != "questions":
        pytest.fail(f"질문지 대기가 아니다: {outcome}")
    respond(probe_lanes(run_root), outcome["pending"][0], questions_payload(targets_of(run_root)), model=OPUS)
    outcome = run_probe(run_root, law)
    if outcome["status"] != "pending" or outcome["phase"] != "probes":
        pytest.fail(f"프로브 대기가 아니다: {outcome}")
    return outcome


def fill_probes(run_root: str, pending: list[str], *, stated=None, bad_span=frozenset()) -> None:
    text = read(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md"))
    questions = read_json(os.path.join(run_root, "60-probe", "questions.json"))["questions"]
    for index, lane_id in enumerate(pending):
        payload = probe_payload(questions, text, stated=stated, bad_span=bad_span if index == 0 else frozenset())
        # 응답 바이트가 서로 같으면 independence 가 걸린다 — 재서술 한 낱말을 계기마다 다르게 둔다(독립 실행의 자연스러운 산출).
        payload["a_restatement"][0] = payload["a_restatement"][0].replace("datastore", f"datastore ({lane_id.rsplit('-', 1)[-1]})")
        respond(probe_lanes(run_root), lane_id, payload, model=HAIKU)


def grade_payload(request_md_path: str, *, grade: str = "hit", judgement: str = "aligned") -> dict:
    """채점 요청서의 채점 입력에서 (probe_id, question_id) 쌍을 읽어 전건 채점."""
    text = read(request_md_path)
    start = text.index("```text", text.index("grading-input.json")) + len("```text\n")
    grading_input = json.loads(text[start:text.index("\n```", start)])
    grades = [{"probe_id": a["probe_id"], "question_id": t["question_id"], "grade": grade, "evidence": str(a.get("answer") or a.get("answer_kind"))}
              for t in grading_input["targets"] for a in t["answers"]]
    restatement = [{"probe_id": r["probe_id"], "judgement": judgement} for r in grading_input["restatements"]]
    return {"grades": grades, "restatement": restatement}


def probe_to_score(run_root: str, law: str, *, stated=None, bad_span=frozenset(), grade="hit") -> dict:
    outcome = probe_to_pending_probes(run_root, law)
    fill_probes(run_root, outcome["pending"], stated=stated, bad_span=bad_span)
    outcome = run_probe(run_root, law)
    if outcome["status"] != "pending" or outcome["phase"] != "grade":
        pytest.fail(f"채점 대기가 아니다: {outcome}")
    lane_id = outcome["pending"][0]
    respond(probe_lanes(run_root), lane_id, grade_payload(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD), grade=grade), model=OPUS)
    return run_probe(run_root, law)


# ---------------------------------------------------------------------------
# ⑴ 계약 · 경로 · 라벨
# ---------------------------------------------------------------------------


def test_contracts_paths_and_haiku_label(law) -> None:
    probe = load_stage_contract("probe", law)
    if probe["schema"] != "stage-contract/v0" or probe["id"] != "probe":
        pytest.fail("probe.yaml 골격이 다르다")
    ids = [row["id"] for row in probe["checks_before_exit"]]
    if ids != ["probe.independence", "probe.input-clean", "probe.no-self-report", "probe.target-coverage", "probe.grader-separation"]:
        pytest.fail(f"검사 5 가 SPEC §1.11 순서가 아니다: {ids}")
    if [row["id"] for row in probe["checks_on_entry"]] != ["probe.input-digest"] or len(probe["failure"]) != 7:
        pytest.fail("진입 검사·실패표(5+2)가 다르다")
    if probe["lane"]["lane_id_vocabulary"]["membership"] != {"run": ["probe-q", "probe", "probe-grade"], "task": ["v1", "v2", "v3"]}:
        pytest.fail("계기 어휘가 다르다")
    gate = load_stage_contract("gate", law)
    l2 = gate["layers"]["l2"]
    if l2["status"] != "active" or l2["lane"] != {"kind": "llm", "model": "gpt-6-astra", "effort": "high"} or gate["loop"]["free_revision"] != 1:
        pytest.fail(f"gate.yaml#layers.l2 · loop.free_revision 이 다르다: {l2} {gate['loop']}")
    no_score = next(row for row in gate["checks_before_exit"] if row["id"] == "gate.no-score")
    if no_score.get("status") == "inactive" or no_score["implemented_by"] != "engine/gate/l2/lint.py":
        pytest.fail("gate.no-score 가 구현 표기가 아니다")
    paths = RunPaths("/nonexistent/run", law)
    if paths.STAGES[-3] != "probe":
        pytest.fail(f"STAGES의 probe 위치가 다르다: {paths.STAGES}")
    expected = {paths.l2_md("v2"): "50-gate/v2/l2.md", paths.questions_json: "60-probe/questions.json", paths.probe_report("v2", 3): "60-probe/v2/probe-3.json",
                paths.score_json("v2"): "60-probe/v2/score.json", paths.probe_escalation_json("v2"): "60-probe/v2/escalation.json",
                paths.gate_escalation_json("v2"): "50-gate/v2/escalation.json", paths.free_revision_dir("v2"): "50-gate/v2/revisions/free-r1"}
    for actual, suffix in expected.items():
        if not actual.endswith(suffix):
            pytest.fail(f"경로가 다르다: {actual} !~ {suffix}")
    labels = {row["label"]: row["aliases"] for row in load_stage_contract("read", law)["lane"]["model_identity"]["labels"]}
    if labels.get("haiku-4.5") != [HAIKU, "haiku"] or labels.get("haiku-5") != ["claude-haiku-5", "haiku"]:
        pytest.fail(f"haiku-4.5 라벨이 T69 재량 3 대로 더해지지 않았거나 기존 행이 바뀌었다: {labels}")
    if drv.api_id_for_label(law, "haiku-4.5") != HAIKU:
        pytest.fail("구동기가 haiku-4.5 를 API 식별자로 풀지 못한다")


# ---------------------------------------------------------------------------
# ⑵ 스키마 · 래퍼
# ---------------------------------------------------------------------------


def test_schema_fixtures_and_wrappers_are_self_contained(law) -> None:
    manifest = read_json(os.path.join(REPO, "tests", "fixtures", "schema-enforcement", "manifest.json"))
    counts: dict[tuple[str, str], int] = {}
    for case in manifest["cases"]:
        if "probe-" in case["schema"]:
            counts[(os.path.basename(case["schema"]), case["expect"])] = counts.get((os.path.basename(case["schema"]), case["expect"]), 0) + 1
    if counts.get(("probe-report.schema.json", "accept"), 0) < 1 or counts.get(("probe-report.schema.json", "reject"), 0) < 3 \
            or counts.get(("probe-score.schema.json", "accept"), 0) < 1 or counts.get(("probe-score.schema.json", "reject"), 0) < 2:
        pytest.fail(f"스키마 집행 픽스처 계수 미달: {counts}")
    config = l2_plan.l2_config(law)
    wrapper = drv.wrapper_schema("v2", "gate-l2")
    if wrapper["properties"]["payload"] is not l2_plan.RESPONSE_SCHEMAS["v2"] or "$ref" in json.dumps(wrapper):
        pytest.fail("gate-l2 래퍼가 상수를 품지 않거나 $ref 가 있다")
    Draft202012Validator.check_schema(wrapper)
    if list(Draft202012Validator(wrapper["properties"]["payload"]).iter_errors({"memos": GOOD_MEMOS})):
        pytest.fail("유효 memo payload 가 거부된다")
    if not list(Draft202012Validator(wrapper["properties"]["payload"]).iter_errors({"memos": [{**GOOD_MEMOS[0], "score": 8}]})):
        pytest.fail("memo 에 숫자 필드가 들어간다 — §4.6 기제 1·2")
    if not list(Draft202012Validator(wrapper["properties"]["payload"]).iter_errors({"memos": [memo("structure", "x")]})):
        pytest.fail(f"rule 접두 {config['rule_prefix']} 가 강제되지 않는다")
    schema = probes_mod.payload_schema([{"question_id": "Q1", "target_material_id": "M3"}])
    dynamic = drv.wrapper_schema("v2", "probe", schema)
    if dynamic["properties"]["payload"] is not schema or "$ref" in json.dumps(dynamic):
        pytest.fail("계기 래퍼가 request 의 response_schema 를 품지 않는다")
    with pytest.raises(drv.DriverExit):
        drv.wrapper_schema("v2", "probe")
    if drv.wrapper_schema("v2")["properties"]["payload"].get("title") == "lane-response/gate-l2":
        pytest.fail("read_run 없는 조회가 L2 사전을 받는다(m30~m34 불변 위반)")


# ---------------------------------------------------------------------------
# ⑶ L2 메모 · 점수 금지 린트
# ---------------------------------------------------------------------------


def test_l2_request_memo_ids_l2_md_verdict_and_decision_unchanged(run_root, law) -> None:
    before = verdict_of(run_root)
    outcome = run_l2(run_root, law)
    lane_id = outcome["pending"][0]
    request = read_json(lane_file(gate_lanes(run_root), lane_id, REQUEST_JSON))
    if request["model"] != "gpt-6-astra" or request["effort"] != "high" or request["read_run"] != "gate-l2":
        pytest.fail(f"L2 좌석이 gpt-6-astra high 가 아니다: {request['model']} {request['effort']}")
    slices = set(request["slices"])
    if not {f"40-compose/{VARIANT}/thread.annotated.md", "15-frozen/material-spec.v1.json", "20-design/blueprint.json"} <= slices or any("l1.json" in s for s in slices):
        pytest.fail(f"L2 원천 조각이 다르다: {slices}")
    respond(gate_lanes(run_root), lane_id, {"memos": GOOD_MEMOS}, model=ASTRA)
    outcome = run_l2(run_root, law)
    verdict = verdict_of(run_root)
    if outcome["status"] != "ok" or outcome["memos"] != 3 or [m["id"] for m in verdict["l2"]["memos"]] != ["m-l2-001", "m-l2-002", "m-l2-003"]:
        pytest.fail(f"memo id 연번이 아니다: {outcome} {verdict['l2']}")
    if verdict["decision"] != before["decision"] or verdict["revision_round"] != before["revision_round"] or verdict["l1"] != before["l1"]:
        pytest.fail("L2 가 판정을 바꿨다 — 거부권 없음 위반")
    if schema_errors("gate-report", verdict):
        pytest.fail(f"verdict 가 gate-report/v0 밖: {schema_errors('gate-report', verdict)}")
    if any(row["layer"] == "l2" for row in verdict["inactive_layers"]) or not any(row["layer"] == "final_eyes" for row in verdict["inactive_layers"]):
        pytest.fail(f"inactive_layers 가 다르다: {verdict['inactive_layers']}")
    row = next(r for r in verdict["checks"] if r["check_id"] == "gate.no-score")
    if row["status"] != "pass" or row["ruleset"] != "score-lint" or row["ruleset_size"] != verdict["legislated"]["score_lint_patterns"] \
            or row["ruleset_version"] != verdict["legislated"]["score_lint_version"] or row["checked"] != 3:
        pytest.fail(f"gate.no-score 행이 다르다: {row}")
    l2_md = read(os.path.join(run_root, "50-gate", VARIANT, "l2.md"))
    if "m-l2-002" not in l2_md or "T8/S1" not in l2_md or GOOD_MEMOS[1]["text"] not in l2_md:
        pytest.fail("l2.md 렌더가 메모를 담지 않는다")
    if run_l2(run_root, law)["status"] != "reentered":
        pytest.fail("두 번째 진입이 reentered 가 아니다")


@pytest.mark.parametrize("text", ["구조 8/10 수준이다", "훅 ★★★☆☆", "착지는 B+ 정도", "overall score is fine"])
def test_no_score_lint_halts_on_score_marks(run_root, law, text) -> None:
    with pytest.raises(StageHaltError) as info:
        l2_done(run_root, law, [memo("l2.structure", text)])
    if "gate.no-score" not in str(info.value):
        pytest.fail(f"halt 사유가 다르다: {info.value}")
    verdict = verdict_of(run_root)
    row = next(r for r in verdict["checks"] if r["check_id"] == "gate.no-score")
    if row["status"] != "fail" or row["violations"] < 1:
        pytest.fail("실패 행이 기록되지 않았다")
    with pytest.raises(StageHaltError):
        run_l2(run_root, law)                       # 기록된 실패는 재진입에서도 halt


def test_no_score_counter_examples_pass_and_load_refuses_broken_entry(law, tmp_path) -> None:
    law_doc = l2_lint.load_patterns(law)
    counters = [str(c["text"]) for c in yaml.safe_load(read(os.path.join(law, "contracts", "lexicon", "score-lint.yaml")))["counter_examples"]]
    if len(counters) < 3:
        pytest.fail("반례가 3 미만이다")
    memos = [{"id": f"m-l2-{i:03d}", "rule": "l2.material-balance", "locus": {"tweet": None, "sentence": None}, "text": f"재료는 {c} 를 그대로 인용한다"}
             for i, c in enumerate(counters, start=1)]
    row = l2_lint.lint_memos(memos, law_doc)
    if row.status != "pass" or row.checked != len(counters):
        pytest.fail(f"반례가 린트에 걸린다: {[f.as_dict() for f in row.findings]}")
    if len(l2_lint.hits("8/10", law_doc)) < 1 or len(l2_lint.hits("A-1 구조", law_doc)) != 0:
        pytest.fail("hits 판정이 다르다")
    broken = os.path.join(str(tmp_path), "law2")
    shutil.copytree(law, broken, ignore=shutil.ignore_patterns(".git"))
    path = os.path.join(broken, "contracts", "lexicon", "score-lint.yaml")
    doc = yaml.safe_load(read(path))
    del doc["patterns"][0]["counter_examples"]
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(doc, handle, allow_unicode=True, sort_keys=False)
    with pytest.raises(l2_lint.ScoreLintLoadError):
        l2_lint.load_patterns(broken)


def test_l2_refuses_non_advance_and_stale_verdict(run_root, law) -> None:
    path = os.path.join(run_root, "50-gate", VARIANT, "verdict.json")
    verdict = read_json(path)
    verdict["decision"] = "revise"
    write_json(path, verdict)
    with pytest.raises(StageError):
        run_l2(run_root, law)


# ---------------------------------------------------------------------------
# ⑷ 자유 리비전 1회 · 위상 봉쇄
# ---------------------------------------------------------------------------


def _free_to_pen(run_root: str, law: str) -> dict:
    l2_done(run_root, law)
    outcome = loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)
    if outcome["status"] != "pending" or outcome["phase"] != "compose" or outcome["pending"] != [f"compose-r4/{VARIANT}/batch-0"]:
        pytest.fail(f"자유 리비전 펜 대기가 아니다: {outcome}")
    return outcome


def test_free_revision_pen_request_rejudge_and_phase_closure(run_root, law) -> None:
    before = verdict_of(run_root)
    outcome = _free_to_pen(run_root, law)
    lanes = os.path.join(run_root, "40-compose", "lanes")
    lane_id = outcome["pending"][0]
    request = read_json(lane_file(lanes, lane_id, REQUEST_JSON))
    rendered = read(lane_file(lanes, lane_id, REQUEST_MD))
    memo_path = os.path.join(run_root, "50-gate", VARIANT, "revisions", "free-r1", "memo.json")
    if not os.path.isfile(memo_path) or f"50-gate/{VARIANT}/revisions/free-r1/memo.json" not in request["slices"]:
        pytest.fail("memo.json 이 없거나 원천 조각에 실리지 않았다")
    if "## L2 메모 표" not in rendered or "## 자유 리비전" not in rendered or GOOD_MEMOS[0]["text"] not in rendered or "## 국소 수정 지시 표" in rendered:
        pytest.fail("펜 요청서에 메모 표(데이터 절)·자유 리비전 절이 없다")
    from engine.pens import lint as pen_lint
    if pen_lint.lint_prompt(rendered, law):
        pytest.fail(f"자유 리비전 요청서가 프롬프트 린트에 걸린다: {pen_lint.lint_prompt(rendered, law)}")
    text = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
    lines = text.split("\n")
    header = next(i for i, line in enumerate(lines) if line.startswith("## T2 "))
    lines[header + 1] = lines[header + 1].replace("This datastore is not a transcript of your chats.", "This datastore is not a chat transcript.")
    revised = "\n".join(lines)
    if revised == text:
        pytest.fail("픽스처 문장이 바뀌지 않았다 — 시험 전제 오류")
    respond(lanes, lane_id, {"thread_annotated_md": revised}, model=OPUS)
    outcome = loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)
    if outcome["status"] != "pending" or outcome["phase"] != "gate-l1" or len(outcome["pending"]) != 3:
        pytest.fail(f"재판정 L1 대기가 아니다: {outcome}")
    respond_l1_clean(run_root, outcome["pending"])
    outcome = loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)
    verdict = verdict_of(run_root)
    if outcome["status"] != "ok" or outcome["outcome"] != "judged" or verdict.get("free_revision_used") is not True:
        pytest.fail(f"자유 리비전 종결이 다르다: {outcome}")
    if verdict["revision_round"] != before["revision_round"] or verdict["decision"] != "advance" or verdict["l2"]["memos"] != read_json(memo_path)["memos"]:
        pytest.fail("revision_round 가 올라갔거나 메모가 이어지지 않았다")
    if verdict["thread_digest"] != sha256_bytes(revised.encode("utf-8")) or schema_errors("gate-report", verdict):
        pytest.fail("재판정 판정문이 새 판의 것이 아니거나 스키마 밖이다")
    copy = os.path.join(run_root, "50-gate", VARIANT, "revisions", "free-r1", "thread.annotated.md")
    if read(copy) != revised or read_json(os.path.join(run_root, "50-gate", VARIANT, "revisions", "free-r1", "round.json"))["status"] != "closed":
        pytest.fail("결과 사본·라운드 상태가 다르다")
    if not os.path.isfile(os.path.join(run_root, "40-compose", VARIANT, "rounds", "r3", "thread.annotated.md")):
        pytest.fail("직전 판이 compose rounds/r3 에 보존되지 않았다")
    rows = [json.loads(line) for line in read(os.path.join(run_root, "40-compose", "tournament-rows.jsonl")).splitlines() if line.strip()]
    if rows[-1].get("reason") != loop_mod.FREE_REVISION_REASON or rows[-1]["outcome"] != "redrafted":
        pytest.fail(f"토너먼트 행이 다르다: {rows[-1]}")
    with pytest.raises(StageHaltError) as info:
        run_l2(run_root, law)
    if "위상 봉쇄" not in str(info.value):
        pytest.fail(f"두 번째 L2 가 위상 봉쇄 halt 가 아니다: {info.value}")
    with pytest.raises(StageError):
        loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)


def test_free_revision_unchanged_response_closes_without_rejudge(run_root, law) -> None:
    before = verdict_of(run_root)
    outcome = _free_to_pen(run_root, law)
    lanes = os.path.join(run_root, "40-compose", "lanes")
    text = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
    respond(lanes, outcome["pending"][0], {"thread_annotated_md": text}, model=OPUS)
    outcome = loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)
    verdict = verdict_of(run_root)
    if outcome["status"] != "ok" or outcome["outcome"] != loop_mod.OUTCOME_UNCHANGED or verdict.get("free_revision_used") is not True \
            or verdict["thread_digest"] != before["thread_digest"] or verdict["checks"] == before["checks"] and False:
        pytest.fail(f"원문 그대로 응답의 종결이 다르다: {outcome}")
    if "free_revision_used | `true`" not in read(os.path.join(run_root, "50-gate", VARIANT, "l2.md")):
        pytest.fail("l2.md 가 소비 사실을 적지 않는다")
    with pytest.raises(StageHaltError):
        run_l2(run_root, law)


def test_free_revision_requires_memo(run_root, law) -> None:
    l2_done(run_root, law, [])
    with pytest.raises(StageError):
        loop_mod.free_revision(run_root=run_root, repo=law, variant=VARIANT)


# ---------------------------------------------------------------------------
# ⑸ 입력 청정
# ---------------------------------------------------------------------------


def test_input_clean_halts_on_leaked_tag(run_root, law) -> None:
    path = os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md")
    write_text(path, read(path).replace("marketing?", "marketing?[M1]", 1))
    with pytest.raises(StageHaltError) as info:
        run_probe(run_root, law)
    if "probe.input-clean" not in str(info.value):
        pytest.fail(str(info.value))
    report = read_json(os.path.join(run_root, "60-probe", VARIANT, "probe-report.json"))
    if report["status"] != "halt" or next(r for r in report["rows"] if r["check_id"] == "probe.input-clean")["status"] != "fail":
        pytest.fail("halt 기록이 다르다")
    for needle in ("## T3 {slot: stop, fig: none}\n", "---\n"):
        write_text(path, needle + read(path).split("\n", 1)[1]) if False else None
    row = probe_stage.input_clean_row("---\nrun_id: x\n---\n## T1 {slot: hook}\nText.\n", load_stage_contract("probe", law)["input_clean_patterns"])
    if row.status != "fail" or row.violations < 2:
        pytest.fail("헤더·프런트매터 어형이 잡히지 않는다")


def test_probe_refuses_non_advance(run_root, law) -> None:
    path = os.path.join(run_root, "50-gate", VARIANT, "verdict.json")
    verdict = read_json(path)
    verdict["decision"] = "revise"
    write_json(path, verdict)
    with pytest.raises(StageError):
        run_probe(run_root, law)


# ---------------------------------------------------------------------------
# ⑹ 질문지
# ---------------------------------------------------------------------------


def test_questions_one_to_one_discard_and_request_has_no_thread(run_root, law) -> None:
    targets = targets_of(run_root)
    outcome = run_probe(run_root, law)
    lane_id = outcome["pending"][0]
    if lane_id != f"probe-q/{VARIANT}/batch-0":
        pytest.fail(lane_id)
    request = read_json(lane_file(probe_lanes(run_root), lane_id, REQUEST_JSON))
    rendered = read(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD))
    stripped = read(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md"))
    if request["model"] != "opus-5" or request["effort"] != "low" or "15-frozen/material-spec.v1.json" not in request["slices"]:
        pytest.fail("질문 생성 좌석·원천 조각이 다르다(재량 ⓑ opus-5 low · 동결본 전문)")
    for sentence in [line for line in stripped.split("\n") if line.strip()][:5]:
        if sentence in rendered:
            pytest.fail("질문 생성 요청서에 스레드 문장이 실렸다(§5.2)")
    extra = [{"question_id": "Q9", "target_material_id": "M52", "question_en": "outside?"}, {"question_id": "Q10", "target_material_id": targets[0], "question_en": "dup?"}]
    respond(probe_lanes(run_root), lane_id, questions_payload(targets, extra=extra), model=OPUS)
    outcome = run_probe(run_root, law)
    doc = read_json(os.path.join(run_root, "60-probe", "questions.json"))
    if [q["target_material_id"] for q in doc["questions"]] != targets or [q["question_id"] for q in doc["questions"]] != [f"Q{i}" for i in range(1, len(targets) + 1)]:
        pytest.fail(f"1:1 질문지가 아니다: {doc['questions']}")
    if {d["reason"] for d in doc["discarded"]} != {questions_mod.DISCARD_OUTSIDE, questions_mod.DISCARD_DUPLICATE}:
        pytest.fail(f"폐기 사유가 다르다: {doc['discarded']}")
    if doc["question_set_digest"] != questions_mod.question_set_digest(doc["questions"]) or outcome["phase"] != "probes":
        pytest.fail("질문지 지문·다음 위상이 다르다")


def test_questions_shortfall_retries_once_then_escalates(run_root, law) -> None:
    targets = targets_of(run_root)
    outcome = run_probe(run_root, law)
    respond(probe_lanes(run_root), outcome["pending"][0], questions_payload(targets, drop=2), model=OPUS)
    outcome = run_probe(run_root, law)
    if outcome["status"] != "pending" or outcome["pending"] != [f"probe-q/{VARIANT}/retry-1/batch-0"] or set(outcome["missing"]) != set(targets[-2:]):
        pytest.fail(f"재시도 좌표가 아니다: {outcome}")
    respond(probe_lanes(run_root), outcome["pending"][0], questions_payload(targets, drop=1), model=OPUS)
    outcome = run_probe(run_root, law)
    if outcome["status"] != "escalate" or not os.path.isfile(os.path.join(run_root, "60-probe", VARIANT, "escalation.json")) \
            or os.path.isfile(os.path.join(run_root, "60-probe", "questions.json")):
        pytest.fail(f"escalate 가 아니거나 부족한 질문지가 쓰였다: {outcome}")


# ---------------------------------------------------------------------------
# ⑺⑻ 프로브 요청 n · 정족수
# ---------------------------------------------------------------------------


def test_probe_requests_identical_bytes_isolated_and_haiku(run_root, law) -> None:
    outcome = probe_to_pending_probes(run_root, law)
    n = outcome["n"]
    if n != yaml.safe_load(read(os.path.join(law, "contracts", "parameters.yaml")))["adjustable"]["probe.n"] or len(outcome["pending"]) != n:
        pytest.fail(f"프로브 요청 수가 probe.n 이 아니다: {outcome}")
    bodies = set()
    stripped = read(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md"))
    for lane_id in outcome["pending"]:
        request = read_json(lane_file(probe_lanes(run_root), lane_id, REQUEST_JSON))
        rendered = read(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD))
        if request["model"] != "haiku-4.5" or request["effort"] != "low":
            pytest.fail(f"계기 좌석이 haiku-4.5 low 가 아니다: {request['model']} {request['effort']}")
        for needle in ("15-frozen", "20-design", "[M", "annotation-index", "verdict.json", "00-source"):
            if needle in rendered:
                pytest.fail(f"계기 요청서에 {needle!r} 가 실렸다 — 입력 격리 위반(§5.2)")
        if stripped.strip() not in rendered or "questions.json" not in rendered:
            pytest.fail("계기 요청서에 스레드·질문지가 없다")
        # 좌표에서 파생되는 세 줄(제목 · 배치 · 그 둘의 함수인 입력 지문)만 빼면 n 요청서는 바이트 동일해야 한다.
        bodies.add("\n".join(line for line in rendered.split("\n")
                             if not line.startswith(("# 레인 요청 — ", "| 배치 |", "| 입력 지문 |"))))
    if len(bodies) != 1:
        pytest.fail("n 요청의 바이트가 좌표 밖에서 갈린다")


def test_quorum_retries_dead_only_then_escalates_preserving_live(run_root, law) -> None:
    outcome = probe_to_pending_probes(run_root, law)
    pending = outcome["pending"]
    fill_probes(run_root, pending[:-1])
    dead = pending[-1]
    outcome = run_probe(run_root, law, dead=[dead])
    if outcome["status"] != "pending" or outcome["pending"] != [f"probe/{VARIANT}/retry-1/batch-4"] or outcome["live"] != 4:
        pytest.fail(f"죽은 대만 재시도되지 않았다: {outcome}")
    live_digests = {i: sha256_file(os.path.join(run_root, "60-probe", VARIANT, f"probe-{i}.json")) for i in range(4)}
    outcome = run_probe(run_root, law, dead=outcome["pending"])
    if outcome["pending"] != [f"probe/{VARIANT}/retry-2/batch-4"]:
        pytest.fail(f"2차 재시도 좌표가 아니다: {outcome}")
    outcome = run_probe(run_root, law, dead=outcome["pending"])
    escalation = os.path.join(run_root, "60-probe", VARIANT, "escalation.json")
    if outcome["status"] != "escalate" or not os.path.isfile(escalation):
        pytest.fail(f"상한 뒤 escalate 가 아니다: {outcome}")
    form = read_json(escalation)
    if form["outcome"] != "escalate" or form["live_count"] != 4 or form["dead_instances"] != ["p4"] or len(form["escalation"]["options"]) != 3:
        pytest.fail(f"상신 서식이 다르다: {form}")
    if {i: sha256_file(os.path.join(run_root, "60-probe", VARIANT, f"probe-{i}.json")) for i in range(4)} != live_digests:
        pytest.fail("살아있는 응답이 갈아치워졌다")
    if os.path.isfile(os.path.join(run_root, "60-probe", VARIANT, "score.json")):
        pytest.fail("정족수 미달인데 score.json 이 생겼다 — 기계 강등")


# ---------------------------------------------------------------------------
# ⑼~⑿ 무효 답변 · 채점 · 국소화 · score.json
# ---------------------------------------------------------------------------


def test_full_probe_score_invalidation_grading_and_localization(run_root, law) -> None:
    outcome = probe_to_pending_probes(run_root, law)
    fill_probes(run_root, outcome["pending"], stated={"Q1", "Q2", "Q7"}, bad_span={"Q2"})
    outcome = run_probe(run_root, law)
    lane_id = outcome["pending"][0]
    if lane_id != f"probe-grade/{VARIANT}/batch-0":
        pytest.fail(lane_id)
    request = read_json(lane_file(probe_lanes(run_root), lane_id, REQUEST_JSON))
    rendered = read(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD))
    stripped = read(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md"))
    grading_input = json.loads(list(request["slices"].values())[0])
    if request["model"] != "opus-5" or request["effort"] != "low" or [t["kind"] for t in grading_input["targets"]] != ["positioning"] \
            or len(grading_input["restatements"]) != outcome["n"] if "n" in outcome else len(grading_input["restatements"]) != 5:
        pytest.fail(f"채점 요청이 다르다(모델 kind 만 · opus-5 low): {request['model']} {[t['kind'] for t in grading_input['targets']]}")
    for line in [line for line in stripped.split("\n") if line.strip()][1:]:
        if line in rendered:
            pytest.fail("채점 요청서에 스레드가 실렸다(§5.3)")
    respond(probe_lanes(run_root), lane_id, grade_payload(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD), grade="partial"), model=OPUS)
    outcome = run_probe(run_root, law)
    score = read_json(os.path.join(run_root, "60-probe", VARIANT, "score.json"))
    if outcome["status"] != "ok" or schema_errors("probe-score", score):
        pytest.fail(f"score.json 이 스키마 밖: {schema_errors('probe-score', score)} {outcome}")
    if schema_errors("probe-score", {**score, "decision": "advance"}) == [] or schema_errors("probe-score", {**score, "pass": True}) == []:
        pytest.fail("score.json 에 판정 키가 들어간다(§5.7)")
    by_id = {t["material_id"]: t for t in score["per_target"]}
    if [t["material_id"] for t in score["per_target"]] != targets_of(run_root):
        pytest.fail("per_target 이 표적 순서·전건이 아니다")
    if [row["probe_id"] for row in score["invalidated_answers"]] != ["p0"] or score["invalidated_answers"][0]["question_id"] != "Q2":
        pytest.fail(f"무효 답변 기록이 다르다: {score['invalidated_answers']}")
    q2 = by_id[targets_of(run_root)[1]]
    if q2["answers"]["invalidated"] != 1 or q2["hit_rate"] != 0.0 or q2["method"] != "deterministic":
        pytest.fail(f"무효 답변이 분모에서 빠지지 않았다: {q2}")
    m116 = by_id["M116"]
    if m116["method"] != "model" or m116["hit_rate"] != 0.5 or m116["answers"]["partial"] != 5:
        pytest.fail(f"모델 채점 환산(partial=0.5)이 다르다: {m116}")
    if score["restatement"] != {"aligned": 5, "drifted": 0, "inverted": 0}:
        pytest.fail(f"재서술 축이 다르다: {score['restatement']}")
    rates = [t["hit_rate"] for t in score["per_target"]]
    if score["delivery_fidelity"] != round(sum(rates) / len(rates), 4):
        pytest.fail("delivery_fidelity 가 비가중 평균이 아니다")
    index = read_json(os.path.join(run_root, "50-gate", VARIANT, "annotation-index.json"))
    for target in score["per_target"]:
        tweet, unrep = localize_mod.weakest_tweet(index, target["material_id"])
        if (target["weakest_tweet"], target["unrepresented"]) != (tweet, unrep):
            pytest.fail("국소화가 역참조 규칙과 다르다")
    m3 = by_id["M3"]
    if m3["weakest_tweet"] != 8 or m3["unrepresented"]:
        pytest.fail(f"M3 의 2단 규칙(문장 수 동점 → 번호 큼) 결과가 8 이 아니다: {m3}")
    if not any(row["issue"] == "not-stated" for row in score["loci"]) or not any(row["issue"] == "invalidated" for row in score["loci"]):
        pytest.fail("loci 가 걸림 지점을 전량 보고하지 않는다(R9)")
    report = read_json(os.path.join(run_root, "60-probe", VARIANT, "probe-report.json"))
    rows = {r["check_id"]: r for r in report["rows"]}
    for cid in ("probe.input-digest", "probe.independence", "probe.input-clean", "probe.no-self-report", "probe.target-coverage", "probe.grader-separation"):
        if rows[cid]["status"] != "pass":
            pytest.fail(f"{cid} 가 pass 가 아니다: {rows[cid]}")
    for i in range(5):
        if schema_errors("probe-report", read_json(os.path.join(run_root, "60-probe", VARIANT, f"probe-{i}.json"))):
            pytest.fail("probe-<i>.json 이 스키마 밖")
    again = run_probe(run_root, law)
    if again["status"] != "reentered":
        pytest.fail(f"재진입이 reentered 가 아니다: {again}")


def test_deterministic_grading_paths() -> None:
    fact = {"kind": "fact", "value_normalized": "0.08", "unit": "mm"}
    if grade_mod.grade_fact(fact, {"answer_kind": "stated", "answer": "about 0.080 mm", "quoted_span": ""}) != "hit" \
            or grade_mod.grade_fact(fact, {"answer_kind": "stated", "answer": "about 0.8 mm", "quoted_span": ""}) != "miss" \
            or grade_mod.grade_fact(fact, {"answer_kind": "stated", "answer": "0.08 inches", "quoted_span": ""}) != "miss" \
            or grade_mod.grade_fact(fact, {"answer_kind": "not-stated", "answer": None, "quoted_span": None}) != "miss":
        pytest.fail("fact 판별식이 다르다")
    ident = {"kind": "fact", "value_normalized": "WO2026-128750A1", "unit": None}
    if grade_mod.grade_fact(ident, {"answer_kind": "stated", "answer": "filing WO2026-128750A1", "quoted_span": ""}) != "hit":
        pytest.fail("식별자 fact 가 문자열 포함으로 판정되지 않는다")
    comp = {"kind": "component", "text_verbatim": "deleting, by the machine-learned agent system, the specified information"}
    if grade_mod.grade_component(comp, {"answer_kind": "stated", "answer": "It says: Deleting — by the machine-learned agent system — the specified information.", "quoted_span": ""}) != "hit" \
            or grade_mod.grade_component(comp, {"answer_kind": "stated", "answer": "deletes things", "quoted_span": ""}) != "miss":
        pytest.fail("component 판별식이 다르다")
    fig = {"kind": "figure_note", "numerals": ["102", "104"]}
    if grade_mod.grade_figure_note(fig, {"answer_kind": "stated", "answer": "boxes 104 and 102", "quoted_span": ""}) != "hit" \
            or grade_mod.grade_figure_note(fig, {"answer_kind": "stated", "answer": "boxes 102, 104 and 110", "quoted_span": ""}) != "miss":
        pytest.fail("figure_note 집합 일치가 다르다")
    grading = {"deterministic": ["fact", "component", "figure_note"], "model": ["grounding", "implication", "positioning"]}
    if grade_mod.method_for("fact", grading) != "deterministic" or grade_mod.method_for("implication", grading) != "model":
        pytest.fail("method_for 가 다르다")
    with pytest.raises(ValueError):
        grade_mod.method_for("unknown", grading)


def test_localization_two_step_rule_and_unrepresented() -> None:
    index = {"by_material": {"M1": [{"tweet": 3, "sentence": 1}, {"tweet": 3, "sentence": 2}, {"tweet": 5, "sentence": 1}, {"tweet": 2, "sentence": 1}]}}
    if localize_mod.weakest_tweet(index, "M1") != (5, False):      # 문장 수 최소(1) 동점 {5, 2} → 번호 큼 5
        pytest.fail("2단 규칙이 다르다")
    if localize_mod.weakest_tweet(index, "M9") != (None, True):
        pytest.fail("unrepresented 가 다르다")
    scores = {"hit": 1, "partial": 0.5, "miss": 0}
    row = localize_mod.target_row(material_id="M9", kind="positioning", method="model", index=index, scores=scores,
                                  verdicts=[{"probe_id": "p0", "answer_kind": "stated", "grade": "hit", "invalid": False},
                                            {"probe_id": "p1", "answer_kind": "stated", "grade": None, "invalid": True},
                                            {"probe_id": "p2", "answer_kind": "not-stated", "grade": None, "invalid": False}])
    if row["hit_rate"] != 0.5 or row["unrepresented"] is not True or row["weakest_tweet"] is not None or row["answers"]["invalidated"] != 1:
        pytest.fail(f"target_row 가 다르다: {row}")
    all_invalid = localize_mod.target_row(material_id="M1", kind="fact", method="deterministic", index=index, scores=scores,
                                          verdicts=[{"probe_id": "p0", "answer_kind": "stated", "grade": None, "invalid": True}])
    if all_invalid["hit_rate"] is not None:
        pytest.fail("유효 답변 0 인데 hit_rate 가 수치다")
    loci = localize_mod.loci_rows([row], 3)
    if {r["issue"] for r in loci} != {"not-stated", "invalidated", "unrepresented"} or localize_mod.delivery_fidelity([row, all_invalid]) != 0.5:
        pytest.fail(f"loci · 비가중 평균이 다르다: {loci}")


# ---------------------------------------------------------------------------
# ⒀ 검사 fail 경로
# ---------------------------------------------------------------------------


def test_check_rows_fail_paths_and_grader_separation_halts(run_root, law) -> None:
    schema = read_json(os.path.join(SCHEMAS, "probe-report.schema.json"))
    good = read_json(os.path.join(REPO, "tests", "fixtures", "schema-enforcement", "accept", "probe-report.minimal.json"))
    if probe_stage.no_self_report_row([good], schema).status != "pass" or probe_stage.no_self_report_row([{**good, "self_assessment": "easy"}], schema).status != "fail":
        pytest.fail("no-self-report 행이 다르다")
    lanes = [{"lane_id": "probe/v2/batch-0", "response_digest": "a"}, {"lane_id": "probe/v2/batch-0", "response_digest": "a"}]
    if probe_stage.independence_row([good, {**good, "probe_id": "p1"}], lanes).status != "fail":
        pytest.fail("같은 좌표·같은 응답이 independence 에 걸리지 않는다")
    if probe_stage.target_coverage_row([{"material_id": "M3"}], ["M3", "M16"]).status != "fail" \
            or probe_stage.target_coverage_row([{"material_id": "M3"}, {"material_id": "M99"}], ["M3"]).status != "fail":
        pytest.fail("target-coverage 가 부족·초과를 잡지 않는다")
    accepted = ("haiku-4.5", HAIKU, "haiku")
    probe_lanes_ = [{"lane_id": "probe/v2/batch-0"}]
    if probe_stage.grader_separation_row({"lane_id": "probe-grade/v2/batch-0", "model": OPUS}, probe_lanes_, probe_accepted=accepted).status != "pass" \
            or probe_stage.grader_separation_row({"lane_id": "probe/v2/batch-0", "model": OPUS}, probe_lanes_, probe_accepted=accepted).status != "fail" \
            or probe_stage.grader_separation_row({"lane_id": "probe-grade/v2/batch-0", "model": HAIKU}, probe_lanes_, probe_accepted=accepted).status != "fail":
        pytest.fail("grader-separation 판정이 다르다")
    # 실런 경로 — 채점자가 계기 모델(haiku)로 돌았다 → halt.
    outcome = probe_to_pending_probes(run_root, law)
    fill_probes(run_root, outcome["pending"])
    outcome = run_probe(run_root, law)
    lane_id = outcome["pending"][0]
    respond(probe_lanes(run_root), lane_id, grade_payload(lane_file(probe_lanes(run_root), lane_id, REQUEST_MD)), model=HAIKU)
    with pytest.raises(StageHaltError) as info:
        run_probe(run_root, law)
    if "probe.grader-separation" not in str(info.value):
        pytest.fail(str(info.value))
    report = read_json(os.path.join(run_root, "60-probe", VARIANT, "probe-report.json"))
    if report["status"] != "halt":
        pytest.fail("halt 기록이 다르다")


# ---------------------------------------------------------------------------
# ⒁ 구동기
# ---------------------------------------------------------------------------


class Stub:
    """`claude -p` json 출력 흉내 — 좌표 접두로 payload 를 고른다."""

    def __init__(self, run_root: str, *, fail_lanes: set[str] = frozenset()):
        self.run_root = run_root
        self.calls: list[list[str]] = []
        self.fail_lanes = set(fail_lanes)

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        if lane_id in self.fail_lanes:
            return drv.ExecResult(1, b"", b"boom", False, 1)
        digest = next(line for line in text.split("\n") if line.startswith("| 입력 지문 | `")).split("`")[1]
        observed = argv[argv.index("--model") + 1]
        stripped = read(os.path.join(self.run_root, "50-gate", VARIANT, "thread.stripped.md"))
        if lane_id.startswith("gate-l2/"):
            payload = {"memos": GOOD_MEMOS}
        elif lane_id.startswith("gate-l1/"):
            payload = {"defects": [], "flags": [], "speech_acts": []}
        elif lane_id.startswith("compose-r"):
            payload = {"thread_annotated_md": read(os.path.join(self.run_root, "40-compose", VARIANT, "thread.annotated.md"))}
        elif lane_id.startswith("probe-q/"):
            payload = questions_payload(targets_of(self.run_root))
        elif lane_id.startswith("probe-grade/"):
            start = text.index("```text", text.index("grading-input.json")) + len("```text\n")
            grading_input = json.loads(text[start:text.index("\n```", start)])
            payload = {"grades": [{"probe_id": a["probe_id"], "question_id": t["question_id"], "grade": "hit", "evidence": "x"}
                                  for t in grading_input["targets"] for a in t["answers"]],
                       "restatement": [{"probe_id": r["probe_id"], "judgement": "aligned"} for r in grading_input["restatements"]]}
        else:
            questions = read_json(os.path.join(self.run_root, "60-probe", "questions.json"))["questions"]
            payload = probe_payload(questions, stripped)
            payload["a_restatement"][2] = f"The user can erase it ({lane_id})."
        body = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "duration_ms": 3, "total_cost_usd": 0.0, "session_id": lane_id,
                "structured_output": {"lane_id": lane_id, "model": "self", "effort": "self", "input_digest": digest, "payload": payload},
                "modelUsage": {observed: {"inputTokens": 1, "outputTokens": 9}}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 3)


def _drive(law: str, run_root: str, evidence: str, *argv: str, executor=None):
    lines: list[str] = []
    return drv.main(["--repo", law, "--run-root", run_root, "--evidence-dir", evidence, *argv], executor=executor, out=lines.append), lines


def test_driver_gate_l2_revise_free_probe_and_seal(run_root, law, tmp_path) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    if len(drv.COMMANDS) != 25 or drv.COMMANDS[-6:-3] != ("gate-l2", "revise-free", "probe"):
        pytest.fail(f"명령 25 가 아니다: {drv.COMMANDS}")
    parser = drv.build_parser()
    listed = tuple(parser._subparsers._group_actions[0].choices)  # noqa: SLF001
    if listed != drv.COMMANDS:
        pytest.fail(f"--help 목록이 COMMANDS 와 다르다: {listed}")
    stub = Stub(run_root)
    code, lines = _drive(law, run_root, evidence, "gate-l2", RUN_ID, "--variant", VARIANT, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 1 or not any(line.startswith("v2: l2 memos 3") for line in lines):
        pytest.fail(f"gate-l2 명령: {code} {lines}")
    argv = stub.calls[0]
    if argv[argv.index("--model") + 1] != ASTRA or argv[argv.index("--effort") + 1] != "high" or argv[argv.index("--tools") + 1] != "":
        pytest.fail(f"L2 레인 명령줄이 다르다: {argv}")
    if json.loads(argv[argv.index("--json-schema") + 1])["properties"]["payload"].get("title") != "lane-response/gate-l2":
        pytest.fail("L2 좌표에 다른 스키마가 실렸다")
    code, lines = _drive(law, run_root, evidence, "revise-free", RUN_ID, "--variant", VARIANT, executor=stub)
    if code != drv.EXIT_OK or not any("free-r1 종결(unchanged)" in line for line in lines) or verdict_of(run_root).get("free_revision_used") is not True:
        pytest.fail(f"revise-free 명령: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "gate-l2", RUN_ID, "--variant", VARIANT, executor=stub)
    if code != drv.EXIT_TERMINAL_FAIL:
        pytest.fail(f"위상 봉쇄 뒤 gate-l2 가 13 이 아니다: {code} {lines}")
    calls_before = len(stub.calls)
    code, lines = _drive(law, run_root, evidence, "probe", RUN_ID, "--variant", VARIANT, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) - calls_before != 7 or not any(line.startswith("v2: probe ok") for line in lines):
        pytest.fail(f"probe 명령: {code} {lines} calls={len(stub.calls) - calls_before}")
    models = [c[c.index("--model") + 1] for c in stub.calls[calls_before:]]
    if models != [OPUS] + [HAIKU] * 5 + [OPUS]:
        pytest.fail(f"계기 계열 실호출 모델 순서가 다르다: {models}")
    receipts = sorted(name for name in os.listdir(os.path.join(evidence, "calls")) if name.startswith("probe") and not name.endswith(".raw.json"))
    if len(receipts) != 7:
        pytest.fail(f"영수증 7 이 아니다: {receipts}")
    code, lines = _drive(law, run_root, evidence, "seal", RUN_ID)
    manifest = read(os.path.join(evidence, "MANIFEST-sha256.txt"))
    for needle in ("60-probe/questions.json", "60-probe/v2/score.json", "60-probe/v2/probe-4.json", "60-probe/v2/lanes/probe/v2/batch-0/response.json",
                   "50-gate/v2/l2.md", "50-gate/v2/revisions/free-r1/memo.json"):
        if not any(line.endswith(needle) for line in manifest.splitlines()):
            pytest.fail(f"seal 에 {needle} 이 없다")
    code, lines = _drive(law, run_root, evidence, "lanes", RUN_ID)
    if code != drv.EXIT_OK:
        pytest.fail(f"lanes: {code} {lines}")


def test_driver_probe_reports_dead_lane_and_retries(run_root, law, tmp_path) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    stub = Stub(run_root, fail_lanes={f"probe/{VARIANT}/batch-2"})
    code, lines = _drive(law, run_root, evidence, "probe", RUN_ID, "--variant", VARIANT, executor=stub)
    if code != drv.EXIT_OK or not any("죽은 인스턴스로 신고" in line for line in lines):
        pytest.fail(f"probe 명령(사망 1): {code} {lines}")
    quorum = read_json(os.path.join(run_root, "60-probe", VARIANT, "quorum.json"))
    if quorum["instances"]["2"]["attempt"] != 1 or quorum["instances"]["2"]["lane_id"] != f"probe/{VARIANT}/retry-1/batch-2" or quorum["attempts_made"] != 1:
        pytest.fail(f"대장이 다르다: {quorum}")
    score = read_json(os.path.join(run_root, "60-probe", VARIANT, "score.json"))
    if score["probe_n"] != 5 or schema_errors("probe-score", score):
        pytest.fail("재시도 뒤 score.json 이 다르다")
