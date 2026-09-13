# -*- coding: utf-8 -*-
"""M35 — L1 국소 대조 · 화행 플래그 · 수정 루프 · final-eyes-brief · CP2 봉투(재정 2026-09-13 T67 ② · M6-a).

모델 호출 없음 — L1·펜 응답은 시험이 파일 어댑터 자리에 쓴다. 픽스처 = 런 -3 v2 2회차 실물
(`runs/gdm-wo2026128750a1-agent-memory-3/{15-frozen, 20-design, 30-figures, 40-compose, 50-gate/v2}` 읽기만 · tmp 런 루트로 복사)
+ 합성 run.yaml. 법 트리 = contracts·reader 사본 + 절차 문서 3(펜 템플릿 · 설계 · L1) · git init(compose 의 law_commit).

★ 변조 표본의 심은 문장 리터럴은 이 파일에 없다 — 골든과의 행 단위 diff 로 좌표만 확인한다(SPEC §4.8 자기매칭 격리).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.gate import checkpoint2 as cp2_mod  # noqa: E402
from engine.gate import loop as loop_mod  # noqa: E402
from engine.gate.l1 import merge as merge_mod  # noqa: E402
from engine.gate.l1 import plan as l1_plan  # noqa: E402
from engine.lanes.contract import REQUEST_JSON, RESPONSE_JSON, lane_file  # noqa: E402
from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.pens import lint  # noqa: E402
from engine.stages import StageError, StageHaltError, sha256_bytes, sha256_file  # noqa: E402
from engine.stages import compose as compose_stage  # noqa: E402
from engine.stages import gate as gate_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

RUN_ID = "gdm-wo2026128750a1-agent-memory-3"
RUN3 = os.path.join(REPO, "runs", RUN_ID)
VARIANT = "v2"
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
REGRESSION = os.path.join(REPO, "ledgers", "regression")
GOLDEN = os.path.join(REGRESSION, "golden", "rc-0009-agent-memory-v2")
MUTATED = {"rc-0009": "rc-0009-hallucinated-claim", "rc-0010": "rc-0010-smuggled-claim", "rc-0011": "rc-0011-solicitation"}
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"),
             ("engine", "gate", "l1", "procedure.md"))
COPIED_DIRS = ("15-frozen", "20-design", "30-figures", "40-compose", os.path.join("50-gate", VARIANT))
L1_MODEL = "claude-opus-5"


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


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(read_json(os.path.join(SCHEMAS, f"{name}.schema.json")))


def schema_errors(name: str, instance) -> list[str]:
    return [error.message for error in validator(name).iter_errors(instance)]


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


# ---------------------------------------------------------------------------
# 픽스처
# ---------------------------------------------------------------------------


def make_law(destination: str) -> str:
    for tree in LAW_TREES:
        shutil.copytree(os.path.join(REPO, tree), os.path.join(destination, tree),
                        ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
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


def make_run(root: str, *, variants=(VARIANT,), partial_until: str = "gate") -> str:
    """런 -3 v2 2회차 실물을 tmp 로 복사(읽기만) + 합성 run.yaml. `variants` 에 v1 이 있으면 v2 사본에 L0 결함을 심는다."""
    run_root = os.path.join(root, "runs", RUN_ID)
    for rel in COPIED_DIRS:
        shutil.copytree(os.path.join(RUN3, rel), os.path.join(run_root, rel))
    frozen = os.path.join(run_root, "15-frozen", "material-spec.v1.json")
    os.chmod(frozen, 0o444)
    real = yaml.safe_load(read(os.path.join(RUN3, "run.yaml")))
    meta = {
        "schema": "run/v0", "run_id": RUN_ID, "status": "active", "run_kind": "partial", "partial_until": partial_until,
        "patent": real["patent"], "engine": {"commit": "e" * 40, "worktree": None},
        "numeric_whitelist": real["numeric_whitelist"], "frozen": real["frozen"],
        "pens": real["pens"], "comparison_axis": real["comparison_axis"],
    }
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    if sha256_file(frozen) != real["frozen"][-1]["spec_digest"]:
        pytest.fail("런 -3 동결본 사본의 지문이 run.yaml 기록과 다르다")
    for variant in variants:
        if variant == VARIANT:
            continue
        text = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
        text = text.replace(f"variant: {VARIANT}\n", f"variant: {variant}\n", 1).replace("[M1,M2,M3,M4,M5,M6]", "[M999,M2,M3,M4,M5,M6]", 1)
        path = os.path.join(run_root, "40-compose", variant, "thread.annotated.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    return run_root


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(os.path.join(str(tmp_path), "r"))


def verdict_of(run_root: str, variant: str = VARIANT) -> dict:
    return read_json(os.path.join(run_root, "50-gate", variant, "verdict.json"))


def rows_by_id(verdict: dict) -> dict:
    return {row["check_id"]: row for row in verdict["checks"]}


def lanes_root(run_root: str, variant: str = VARIANT) -> str:
    return os.path.join(run_root, "50-gate", variant, "lanes")


def clean_payload() -> dict:
    return {"defects": [], "flags": [], "speech_acts": []}


def defect(rule: str, tweet: int, sentence: int, directive: str | None = None) -> dict:
    return {"rule": rule, "locus": {"tweet": tweet, "sentence": sentence}, "expected": "재료 항목의 EN 값과 합치",
            "observed": "재료가 말하지 않는 단정", "fix_directive": directive or f"T{tweet}/S{sentence} 가 인용한 재료로 재서술하라 — 재료 밖 단정을 빼라"}


def respond_l1(run_root: str, payloads: list[dict], *, model: str = L1_MODEL, effort: str = "high", variant: str = VARIANT) -> None:
    root = lanes_root(run_root, variant)
    for index, payload in enumerate(payloads):
        lane_id = f"gate-l1/{variant}/batch-{index}"
        request = read_json(lane_file(root, lane_id, REQUEST_JSON))
        write_json(lane_file(root, lane_id, RESPONSE_JSON), {
            "lane_id": lane_id, "model": model, "effort": effort, "input_digest": request["input_digest"], "payload": payload,
        })


def run_l1(run_root: str, law: str, variant: str = VARIANT) -> dict:
    return gate_stage.run_l1(run_root=run_root, repo=law, variant=variant)


def l1_to_pending(run_root: str, law: str) -> dict:
    outcome = run_l1(run_root, law)
    if outcome["status"] != "pending" or len(outcome["pending"]) != 3:
        pytest.fail(f"첫 진입이 대기 3 이 아니다: {outcome}")
    return outcome


def replace_sentence(text: str, tweet: int, sentence: int, new_line: str) -> str:
    """주석본에서 T<n>/S<i> 줄을 통째로 바꾼다(태그 포함)."""
    lines = text.split("\n")
    header = next(i for i, line in enumerate(lines) if line.startswith(f"## T{tweet} "))
    lines[header + sentence] = new_line
    return "\n".join(lines)


def respond_pen(run_root: str, lane_id: str, text: str) -> None:
    root = os.path.join(run_root, "40-compose", "lanes")
    request = read_json(lane_file(root, lane_id, REQUEST_JSON))
    write_json(lane_file(root, lane_id, RESPONSE_JSON), {
        "lane_id": lane_id, "model": L1_MODEL, "effort": request["effort"], "input_digest": request["input_digest"],
        "payload": {"thread_annotated_md": text},
    })


T4S2_TAG = "[M24,M27,M28,M75,M78,M79,M115,M119]"


def revised_line(round_no: int) -> str:
    """T4/S2 의 정당한 국소 수정 — 인용 그대로 · 재료 안 문언(회차마다 한 낱말이 달라 지문이 바뀐다)."""
    extra = " again" * (round_no - 1)
    return f"It compares a query embedding to memory value embeddings by cosine similarity and keeps a top subset{extra}.{T4S2_TAG}"


# ---------------------------------------------------------------------------
# ⑴ 계약 · 경로
# ---------------------------------------------------------------------------


def test_contract_activates_l1_and_paths_declare_new_outputs(law) -> None:
    contract = load_stage_contract("gate", law)
    layers = contract["layers"]
    if layers["l1"]["status"] != "active" or layers["speech_act_flag"]["status"] != "active":
        pytest.fail("gate.yaml#layers.l1·speech_act_flag 가 active 가 아니다")
    if layers["l1"]["lane"] != {"kind": "llm", "model": "opus-5", "effort": "high", "k": "parameters.yaml#gate.l1.k"}:
        pytest.fail(f"L1 좌석이 다르다: {layers['l1']['lane']}")
    if layers["l2"]["status"] != "inactive" or layers["final_eyes"]["status"] != "inactive":
        pytest.fail("L2·최종 심급은 미가동 그대로여야 한다(재정 T67 ② 범위 밖)")
    raw = yaml.safe_load(read(os.path.join(law, "contracts", "stages", "gate.yaml")))
    if gate_stage.revision_cap(contract) != raw["loop"]["revision_cap"] or not isinstance(raw["loop"]["revision_cap"], int):
        pytest.fail("revision_cap 이 파일에서 오지 않는다")
    checks = {row["id"]: row for row in contract["checks_before_exit"]}
    if checks["gate.l1-clean"].get("status") == "inactive" or checks["gate.l1-clean"]["implemented_by"] != "engine/stages/gate.py":
        pytest.fail("gate.l1-clean 이 구현 표기가 아니다")
    if "gate.l1-lane-verified" not in checks or "L1" not in checks["gate.no-rewrite"]["note"]:
        pytest.fail("gate.l1-lane-verified 신설 · gate.no-rewrite 대상 확장(L1)이 계약에 없다")
    if contract["lane"]["lane_id_vocabulary"]["membership"] != {"run": ["gate-l1"], "task": ["v1", "v2", "v3"]}:
        pytest.fail("L1 어휘 membership 이 다르다")
    paths = RunPaths("/nonexistent/run", law)
    if not paths.l1_json(VARIANT).endswith("50-gate/v2/l1.json") or not paths.final_eyes_brief(VARIANT).endswith("50-gate/v2/final-eyes-brief.json") \
            or not paths.checkpoint2_md.endswith("70-ship/checkpoint2.md") or not paths.revisions_dir(VARIANT, 2).endswith("50-gate/v2/revisions/r2") \
            or not paths.gate_lanes_dir(VARIANT).endswith("50-gate/v2/lanes") or not paths.gate_escalation_json(VARIANT).endswith("50-gate/v2/escalation.json") \
            or not paths.design_escalation_json.endswith("20-design/escalation.json"):
        pytest.fail("RunPaths 가 L1·발췌본·CP2·라운드 경로를 계약에서 해소하지 못한다")
    config = l1_plan.l1_config(law)
    if config["k"] != yaml.safe_load(read(os.path.join(law, "contracts", "parameters.yaml")))["adjustable"]["gate.l1.k"]:
        pytest.fail("k 가 parameters.yaml 에서 오지 않는다")
    if config["veto_rules"] != ["l1.citation-mismatch", "l1.narrative-smuggling"] or config["advisory_rules"] != ["l1.advice-implicit"]:
        pytest.fail(f"L1 규칙 id 가 계약과 다르다: {config}")


# ---------------------------------------------------------------------------
# ⑵ 요청 k 건
# ---------------------------------------------------------------------------


def test_k_requests_are_identical_except_coordinate_and_carry_the_four_slices(run_root, law) -> None:
    outcome = l1_to_pending(run_root, law)
    if outcome["pending"] != [f"gate-l1/{VARIANT}/batch-{i}" for i in range(3)] or outcome["k"] != 3:
        pytest.fail(f"좌표가 gate-l1/v2/batch-0..2 가 아니다: {outcome['pending']}")
    root = lanes_root(run_root)
    requests = [read_json(lane_file(root, lane_id, REQUEST_JSON)) for lane_id in outcome["pending"]]
    stripped = [{k: v for k, v in r.items() if k not in ("lane_id", "batch", "input_digest")} for r in requests]
    if stripped[0] != stripped[1] or stripped[1] != stripped[2]:
        pytest.fail("k 요청의 본문(지시·원천 조각·스키마·좌석)이 서로 다르다")
    if {r["model"] for r in requests} != {"opus-5"} or {r["effort"] for r in requests} != {"high"} or {r["read_run"] for r in requests} != {"gate-l1"}:
        pytest.fail("좌석·run 세그먼트가 다르다")
    slices = requests[0]["slices"]
    if set(slices) != {"40-compose/v2/thread.annotated.md", "15-frozen/material-spec.v1.json", "50-gate/v2/annotation-index.json",
                       "contracts/lexicon/speech-acts.yaml"}:
        pytest.fail(f"원천 조각 넷이 아니다: {sorted(slices)}")
    if slices["40-compose/v2/thread.annotated.md"] != read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")):
        pytest.fail("주석본 원문이 그대로 실리지 않았다")
    acts = yaml.safe_load(read(os.path.join(law, "contracts", "lexicon", "speech-acts.yaml")))
    md = read(lane_file(root, outcome["pending"][0], "request.md"))
    for predicate in acts["predicates"]:
        question = " ".join(predicate["classification_question"].split())
        if question not in md:
            pytest.fail(f"{predicate['id']} 의 분류 질문 원문이 요청서에 없다")
    if any(name.startswith(("00-source", "40-compose/v1", "40-compose/v3", "10-read")) for name in slices) or "### `00-source" in md:
        pytest.fail("must_not_read 대상이 원천 조각으로 실렸다")
    if "## 절차 (정본 = engine/gate/l1/procedure.md)" not in md or "l1.narrative-smuggling" not in md:
        pytest.fail("절차 문서가 인라인되지 않았다")


# ---------------------------------------------------------------------------
# ⑶ 래퍼 사전 분기 · 스키마
# ---------------------------------------------------------------------------


def test_wrapper_schema_branches_on_read_run_and_payload_schema_is_inline() -> None:
    wrapper = drv.wrapper_schema("v2", "gate-l1")
    if wrapper["properties"]["payload"] is not l1_plan.RESPONSE_SCHEMAS["v2"] or l1_plan.RESPONSE_SCHEMAS["v1"] is not l1_plan.RESPONSE_SCHEMAS["v3"]:
        pytest.fail("구동기 래퍼가 l1_plan.RESPONSE_SCHEMAS 상수를 품지 않거나 세 변주의 스키마가 다른 객체다")
    if drv.wrapper_schema("v2")["properties"]["payload"] is not compose_stage.RESPONSE_SCHEMAS["v2"] \
            or drv.wrapper_schema("v2", "compose-r2")["properties"]["payload"] is not compose_stage.RESPONSE_SCHEMAS["v2"]:
        pytest.fail("read_run 이 없거나 compose 이면 compose 스키마여야 한다(m30~m34 불변)")
    dumped = json.dumps(wrapper)
    if "$ref" in dumped or "$defs" in dumped:
        pytest.fail("래퍼에 $ref·$defs 가 있다 — CLI --json-schema 는 자기완결이어야 한다")
    Draft202012Validator.check_schema(wrapper)
    payload = {"defects": [defect("l1.citation-mismatch", 4, 2)], "flags": [{"rule": "l1.advice-implicit", "locus": {"tweet": 8, "sentence": 1}, "note": "n"}],
               "speech_acts": [{"predicate": "sa-01", "locus": {"tweet": 9, "sentence": 2}, "note": "x"}]}
    errors = list(Draft202012Validator(wrapper["properties"]["payload"]).iter_errors(payload))
    if errors:
        pytest.fail(f"유효 payload 가 거부된다: {[e.message for e in errors]}")
    bad = {"defects": [{**defect("l1.citation-mismatch", 4, 2), "extra": 1}], "flags": [], "speech_acts": []}
    if not list(Draft202012Validator(wrapper["properties"]["payload"]).iter_errors(bad)):
        pytest.fail("additionalProperties 가 열려 있다")
    with pytest.raises(drv.DriverExit):
        drv.wrapper_schema("decompose", "gate-l1")


# ---------------------------------------------------------------------------
# ⑷ 병합
# ---------------------------------------------------------------------------


def test_merge_majority_minority_advisory_speech_act_and_ids(law) -> None:
    config = l1_plan.l1_config(law)
    d42 = defect("l1.citation-mismatch", 4, 2)
    d51 = defect("l1.narrative-smuggling", 5, 1)
    d11 = defect("l1.citation-mismatch", 1, 1)
    adv = {"rule": "l1.advice-implicit", "locus": {"tweet": 8, "sentence": 1}, "note": "결론을 대신 내린다"}
    sa = {"predicate": "sa-01", "locus": {"tweet": 9, "sentence": 2}, "note": "권유"}
    payloads = [
        {"defects": [d42, d51, d11], "flags": [adv], "speech_acts": [sa]},
        {"defects": [d42, d51], "flags": [adv], "speech_acts": [sa]},
        {"defects": [d42], "flags": [adv], "speech_acts": []},
    ]
    out = merge_mod.merge(payloads, k=3, advisory_rules=config["advisory_rules"], flag_rule=config["flag_rule"], next_defect_no=1, next_flag_no=3)
    if [(d["id"], d["rule"], d["locus"]["tweet"]) for d in out["defects"]] != [("d-l1-001", "l1.citation-mismatch", 4), ("d-l1-002", "l1.narrative-smuggling", 5)]:
        pytest.fail(f"3:0 · 2:1 결함 채택이 다르다: {out['defects']}")
    flags = {f["id"]: f for f in out["flags"]}
    if [f["id"] for f in out["flags"]] != ["f-l1-003", "f-l1-004", "f-l1-005"]:
        pytest.fail(f"flag id 연번(L0 다음)이 아니다: {list(flags)}")
    minority = flags["f-l1-003"]
    if minority["origin"] != "minority-vote" or minority["votes"] != {"k": 3, "for": 1, "against": 2} or minority["locus"] != {"tweet": 1, "sentence": 1}:
        pytest.fail(f"1:2 강등이 다르다: {minority}")
    advisory = flags["f-l1-004"]
    if advisory["origin"] != "advisory-rule" or advisory["votes"]["for"] != 3 or advisory["rule"] != "l1.advice-implicit":
        pytest.fail(f"advice-implicit 3:0 이 flag 가 아니다: {advisory}")
    speech = flags["f-l1-005"]
    if speech["origin"] != "speech-act" or speech["predicate"] != "sa-01" or speech["rule"] != "speech-act.sa-01" or speech["votes"] != {"k": 3, "for": 2, "against": 1}:
        pytest.fail(f"화행 2:1 이 승격 없는 flag 가 아니다: {speech}")
    if out["disagreement_log"] != [
        {"rule": "l1.citation-mismatch", "locus": {"tweet": 1, "sentence": 1}, "for": 1, "against": 2},
        {"rule": "l1.narrative-smuggling", "locus": {"tweet": 5, "sentence": 1}, "for": 2, "against": 1},
        {"rule": "speech-act.sa-01", "locus": {"tweet": 9, "sentence": 2}, "for": 2, "against": 1},
    ]:
        pytest.fail(f"불일치 로그가 다르다: {out['disagreement_log']}")
    if out["pass"] is not False or len(out["votes"]) != 3 or out["votes"][2]["speech_acts"] != []:
        pytest.fail("pass·votes 보존이 다르다")
    ids = [d["id"] for d in out["defects"]] + list(flags)
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"^(d|f)-l1-[0-9]{3}$", i) for i in ids):
        pytest.fail(f"id 가 유일·정규식 안이 아니다: {ids}")
    if merge_mod.merge([clean_payload()] * 3, k=3, advisory_rules=(), flag_rule="speech-act.<predicate>")["pass"] is not True:
        pytest.fail("결함 0 이면 pass 여야 한다")


# ---------------------------------------------------------------------------
# ⑸ gate.no-rewrite(L1) · ⑹ gate.l1-lane-verified
# ---------------------------------------------------------------------------


def test_no_rewrite_halts_on_quoted_sentence_in_lane_directive(run_root, law) -> None:
    l1_to_pending(run_root, law)
    smuggled = defect("l1.citation-mismatch", 4, 2, 'T4/S2 를 "The embeddings are stored on the device forever."로 바꿔라.')
    respond_l1(run_root, [{"defects": [smuggled], "flags": [], "speech_acts": []}] * 3)
    with pytest.raises(StageHaltError):
        run_l1(run_root, law)
    verdict = verdict_of(run_root)
    row = rows_by_id(verdict)["gate.no-rewrite"]
    if row["status"] != "fail" or row["checked"] != 1 or verdict["l1"]["defects"][0]["id"] != "d-l1-001":
        pytest.fail(f"no-rewrite 행이 L1 지시문을 잡지 못했다: {row}")
    if len([r for r in verdict["checks"] if r["check_id"] == "gate.no-rewrite"]) != 1:
        pytest.fail("gate.no-rewrite 행이 둘이다(L0 행을 갱신해야 한다)")
    with pytest.raises(StageHaltError):
        run_l1(run_root, law)          # 재진입도 halt 를 다시 낸다(기록된 실패)
    # 지시문 형식은 통과
    fresh = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "ok"))
    l1_to_pending(fresh, law)
    respond_l1(fresh, [{"defects": [defect("l1.citation-mismatch", 4, 2)], "flags": [], "speech_acts": []}] * 3)
    outcome = run_l1(fresh, law)
    if outcome["status"] != "ok" or rows_by_id(verdict_of(fresh))["gate.no-rewrite"]["status"] != "pass":
        pytest.fail(f"지시문 형식이 통과하지 않는다: {outcome}")


def test_lane_verified_rejects_wrong_model_or_effort(run_root, law) -> None:
    l1_to_pending(run_root, law)
    respond_l1(run_root, [clean_payload()] * 3, model="claude-fable-5-1")
    with pytest.raises(StageHaltError):
        run_l1(run_root, law)
    row = rows_by_id(verdict_of(run_root))["gate.l1-lane-verified"]
    if row["status"] != "fail" or row["violations"] != 3 or row["checked"] != 6:
        pytest.fail(f"lane-verified 가 fable 응답을 잡지 못했다: {row}")
    other = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "e"))
    l1_to_pending(other, law)
    respond_l1(other, [clean_payload()] * 3, effort="xhigh")
    with pytest.raises(StageHaltError):
        run_l1(other, law)
    if rows_by_id(verdict_of(other))["gate.l1-lane-verified"]["violations"] != 3:
        pytest.fail("effort 불일치가 잡히지 않는다")


# ---------------------------------------------------------------------------
# ⑺ final-eyes-brief
# ---------------------------------------------------------------------------


def test_final_eyes_brief_generated_once_pinned_and_immutable(run_root, law) -> None:
    brief_path = os.path.join(run_root, "50-gate", VARIANT, "final-eyes-brief.json")
    if os.path.isfile(brief_path):
        pytest.fail("픽스처에 발췌본이 이미 있다")
    l1_to_pending(run_root, law)
    if not os.path.isfile(brief_path):
        pytest.fail("L1 첫 진입에 발췌본이 생성되지 않았다")
    brief = read_json(brief_path)
    meta = yaml.safe_load(read(os.path.join(run_root, "run.yaml")))
    thread = read_json(os.path.join(run_root, "50-gate", VARIANT, "thread.json"))
    if brief["numeric_whitelist"] != [{k: e.get(k) for k in ("pattern", "rationale", "added_by", "approved_in")} for e in meta["numeric_whitelist"]] \
            or brief["k"] != 3 or brief["slots"] != [{"n": t["n"], "slot": t["slot"]} for t in thread["tweets"]] \
            or brief["spec_digest"] != meta["frozen"][-1]["spec_digest"] or brief["generated_before_loop"] is not True \
            or brief["revision_round_at_generation"] != 0:
        pytest.fail(f"발췌본 내용이 다르다: {brief}")
    for forbidden in ("question_en", "thesis_en", "point_en", "transmission_targets", "exhibit"):
        if forbidden in json.dumps(brief):
            pytest.fail(f"발췌본에 블루프린트 논지·의도가 실렸다: {forbidden}")
    verdict = verdict_of(run_root)
    digest = sha256_file(brief_path)
    if verdict.get("final_eyes_brief_digest") != digest:
        pytest.fail("verdict.json 에 발췌본 지문이 핀되지 않았다")
    if schema_errors("gate-report", verdict):
        pytest.fail(schema_errors("gate-report", verdict))
    before = open(brief_path, "rb").read()
    respond_l1(run_root, [clean_payload()] * 3)
    run_l1(run_root, law)
    run_l1(run_root, law)
    if open(brief_path, "rb").read() != before or verdict_of(run_root)["final_eyes_brief_digest"] != digest:
        pytest.fail("재진입에서 발췌본이 바뀌었다")
    brief["k"] = 99
    write_json(brief_path, brief)
    with pytest.raises(StageHaltError):
        run_l1(run_root, law)


# ---------------------------------------------------------------------------
# ⑻ decision · inactive_layers  ⑼ L0 결함 변주
# ---------------------------------------------------------------------------


def test_decision_advance_on_clean_and_revise_on_defect(run_root, law) -> None:
    l1_to_pending(run_root, law)
    respond_l1(run_root, [clean_payload()] * 3)
    outcome = run_l1(run_root, law)
    verdict = verdict_of(run_root)
    if outcome["status"] != "ok" or verdict["decision"] != "advance" or verdict["l1"]["pass"] is not True:
        pytest.fail(f"l0 pass ∧ l1 pass 가 advance 가 아니다: {outcome}")
    if [row["layer"] for row in verdict["inactive_layers"]] != ["l2", "final_eyes"]:
        pytest.fail(f"inactive_layers 가 [l2, final_eyes] 가 아니다: {verdict['inactive_layers']}")
    ids = [row["check_id"] for row in verdict["checks"]]
    if "gate.l1-clean" not in ids or "gate.l1-lane-verified" not in ids or ids.count("gate.no-rewrite") != 1:
        pytest.fail(f"L1 검사 행이 없다: {ids}")
    if schema_errors("gate-report", verdict):
        pytest.fail(schema_errors("gate-report", verdict))
    l1_json = read_json(os.path.join(run_root, "50-gate", VARIANT, "l1.json"))
    if l1_json != verdict["l1"]:
        pytest.fail("l1.json 은 verdict.json#l1 과 같은 객체여야 한다")
    if run_l1(run_root, law).get("reentered") is not True:
        pytest.fail("같은 지문 재진입이 재계산했다")
    # 결함 → revise
    other = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "d"))
    l1_to_pending(other, law)
    respond_l1(other, [{"defects": [defect("l1.narrative-smuggling", 1, 1)], "flags": [], "speech_acts": []}] * 3)
    outcome = run_l1(other, law)
    verdict = verdict_of(other)
    if outcome["status"] != "ok" or verdict["decision"] != "revise" or verdict["l1"]["pass"] is not False \
            or rows_by_id(verdict)["gate.l1-clean"]["status"] != "fail" or verdict["revision_round"] != 0:
        pytest.fail(f"L1 결함이 revise 가 아니다: {verdict['decision']}")
    if schema_errors("gate-report", verdict):
        pytest.fail(schema_errors("gate-report", verdict))


def test_l0_defect_variant_skips_l1_and_stays_revise(tmp_path, law) -> None:
    run_root = make_run(os.path.join(str(tmp_path), "r"), variants=("v1", VARIANT))
    gate_stage.run(run_root=run_root, repo=law, variants=["v1"])
    verdict = verdict_of(run_root, "v1")
    if verdict["l0"]["pass"] is not False or verdict["decision"] != "revise":
        pytest.fail("v1 사본이 L0 결함 판이 아니다")
    if not any(row["layer"] == "l1" for row in verdict["inactive_layers"]):
        pytest.fail("L0 만 돈 판정문에 l1 pending 행이 없다")
    outcome = run_l1(run_root, law, "v1")
    if outcome["status"] != "skipped-l0" or os.path.isdir(lanes_root(run_root, "v1")) or verdict_of(run_root, "v1")["decision"] != "revise":
        pytest.fail(f"L0 결함 변주에 L1 요청이 생겼거나 판정이 바뀌었다: {outcome}")
    if not os.path.isfile(os.path.join(run_root, "50-gate", "v1", "final-eyes-brief.json")):
        pytest.fail("L0 결함 변주도 루프 개시 전 발췌본은 생성된다")
    with pytest.raises(StageError):
        run_l1(run_root, law, "v3")


# ---------------------------------------------------------------------------
# ⑽ ⑾ ⑿ 수정 라운드
# ---------------------------------------------------------------------------


def _l1_defect_state(run_root: str, law: str) -> dict:
    l1_to_pending(run_root, law)
    respond_l1(run_root, [{"defects": [defect("l1.citation-mismatch", 4, 2)], "flags": [], "speech_acts": []}] * 3)
    return run_l1(run_root, law)


def test_revise_round_directives_pen_request_copies_and_rejudges(run_root, law) -> None:
    _l1_defect_state(run_root, law)
    outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    round_dir = os.path.join(run_root, "50-gate", VARIANT, "revisions", "r1")
    directives = read_json(os.path.join(round_dir, "directives.json"))
    if outcome["status"] != "pending" or outcome["phase"] != "compose" or outcome["pending"] != ["compose-r3/v2/batch-0"]:
        pytest.fail(f"라운드 1 이 펜 대기가 아니다: {outcome}")
    if directives["round"] != 1 or [d["id"] for d in directives["directives"]] != ["d-l1-001"] or directives["directives"][0]["locus"] != {"tweet": 4, "sentence": 2} \
            or directives["thread_digest"] != verdict_of(run_root)["thread_digest"] or not directives["final_eyes_brief_digest"]:
        pytest.fail(f"directives.json 이 다르다: {directives}")
    request_md = read(os.path.join(run_root, "40-compose", "lanes", "compose-r3", "v2", "batch-0", "request.md"))
    if "## 국소 수정 지시 표" not in request_md or "d-l1-001" not in request_md or "T4/S2" not in request_md \
            or "revisions/r1/directives.json" not in request_md:
        pytest.fail("펜 요청서에 지시 표가 없다")
    if lint.lint_prompt(request_md, law):
        pytest.fail("펜 요청서 린트가 0 이 아니다")
    before = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
    respond_pen(run_root, "compose-r3/v2/batch-0", replace_sentence(before, 4, 2, revised_line(1)))
    outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    if outcome["status"] != "pending" or outcome["phase"] != "gate-l1" or len(outcome["pending"]) != 3:
        pytest.fail(f"펜 뒤 L1 대기가 아니다: {outcome}")
    if read(os.path.join(round_dir, "thread.annotated.md")) != read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")):
        pytest.fail("결과 사본이 revisions/r1/ 에 없다")
    if read(os.path.join(run_root, "40-compose", VARIANT, "rounds", "r2", "thread.annotated.md")) != before:
        pytest.fail("직전 판이 40-compose/v2/rounds/r2/ 에 보존되지 않았다")
    gate_rounds = os.path.join(run_root, "50-gate", VARIANT, "rounds")
    if not os.path.isfile(os.path.join(gate_rounds, "r2", "verdict.json")) or not os.path.isdir(os.path.join(gate_rounds, "r2", "lanes")):
        pytest.fail("직전 판정·L1 레인이 50-gate/v2/rounds/r2/ 에 보존되지 않았다(r1 = 픽스처 실물)")
    if verdict_of(run_root)["revision_round"] != 1 or verdict_of(run_root)["l0"]["pass"] is not True:
        pytest.fail("재판정 L0 · revision_round 1 이 아니다")
    respond_l1(run_root, [clean_payload()] * 3)
    outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    verdict = verdict_of(run_root)
    if outcome["status"] != "ok" or verdict["decision"] != "advance" or verdict["revision_round"] != 1 or verdict["l1"]["pass"] is not True:
        pytest.fail(f"라운드 1 종결이 advance · round 1 이 아니다: {outcome} {verdict['decision']}")
    if read_json(os.path.join(round_dir, "round.json"))["status"] != "closed" or schema_errors("gate-report", verdict):
        pytest.fail("라운드 상태·판정문 서식이 다르다")
    brief = os.path.join(run_root, "50-gate", VARIANT, "final-eyes-brief.json")
    if sha256_file(brief) != verdict["final_eyes_brief_digest"] or sha256_file(brief) != directives["final_eyes_brief_digest"]:
        pytest.fail("발췌본이 라운드를 지나며 바뀌었거나 핀이 끊겼다")
    with pytest.raises(StageError):
        loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)      # advance 상태에서는 라운드를 열지 않는다


def test_revise_rejects_changes_outside_directive_loci(run_root, law) -> None:
    _l1_defect_state(run_root, law)
    loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    before = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
    changed = replace_sentence(before, 4, 2, revised_line(1))
    changed = changed.replace("No performance numbers are given.[M116]", "No performance numbers are given at all.[M116]", 1)
    respond_pen(run_root, "compose-r3/v2/batch-0", changed)
    outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    if outcome["status"] != loop_mod.OUTCOME_LOCALITY_FAILED or outcome["revision_round"] != 1 or outcome["decision"] != "revise":
        pytest.fail(f"지시 밖 변경이 라운드 실패가 아니다: {outcome}")
    findings = outcome["findings"]
    if not findings or findings[0]["rule"] != "annotation.schema" or loop_mod.LOCALITY_MESSAGE not in findings[0]["message"] or findings[0]["locus"] != "T8/S1":
        pytest.fail(f"국소성 finding 이 다르다: {findings}")
    if read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")) != before:
        pytest.fail("현행본이 직전 판으로 복원되지 않았다")
    locality = read_json(os.path.join(run_root, "50-gate", VARIANT, "revisions", "r1", "locality.json"))
    if locality["status"] != "fail" or read_json(os.path.join(run_root, "50-gate", VARIANT, "revisions", "r1", "round.json"))["outcome"] != loop_mod.OUTCOME_LOCALITY_FAILED:
        pytest.fail("라운드 실패 기록이 없다")
    if verdict_of(run_root)["revision_round"] != 1:
        pytest.fail("실패 라운드가 캡에 계수되지 않았다")


def test_revise_cap_escalates_after_three_rounds(run_root, law) -> None:
    _l1_defect_state(run_root, law)
    cap = gate_stage.revision_cap(load_stage_contract("gate", law))
    for round_no in range(1, cap + 1):
        outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
        if outcome["status"] != "pending" or outcome["phase"] != "compose":
            pytest.fail(f"라운드 {round_no} 펜 대기가 아니다: {outcome}")
        lane_id = outcome["pending"][0]
        before = read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md"))
        respond_pen(run_root, lane_id, replace_sentence(before, 4, 2, revised_line(round_no)))
        outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
        if outcome["status"] != "pending" or outcome["phase"] != "gate-l1":
            pytest.fail(f"라운드 {round_no} L1 대기가 아니다: {outcome}")
        respond_l1(run_root, [{"defects": [defect("l1.citation-mismatch", 4, 2)], "flags": [], "speech_acts": []}] * 3)
        outcome = loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
        verdict = verdict_of(run_root)
        if verdict["revision_round"] != round_no:
            pytest.fail(f"revision_round 가 {round_no} 가 아니다: {verdict['revision_round']}")
        if round_no < cap and (outcome["status"] != "ok" or verdict["decision"] != "revise"):
            pytest.fail(f"라운드 {round_no} 가 revise 가 아니다: {outcome}")
    escalation = os.path.join(run_root, "50-gate", VARIANT, "escalation.json")
    if outcome["status"] != "escalate" or verdict["decision"] != "escalate" or not os.path.isfile(escalation):
        pytest.fail(f"캡 뒤 escalate 가 아니다: {outcome}")
    record = read_json(escalation)
    if record["revision_round"] != cap or record["reason"] != loop_mod.ESCALATION_REASON or [d["id"] for d in record["remaining_defects"]] != ["d-l1-001"]:
        pytest.fail(f"escalation.json 이 다르다: {record}")
    if schema_errors("gate-report", verdict):
        pytest.fail(schema_errors("gate-report", verdict))
    with pytest.raises(StageError):
        loop_mod.revise(run_root=run_root, repo=law, variant=VARIANT)
    rounds = sorted(os.listdir(os.path.join(run_root, "50-gate", VARIANT, "revisions")))
    if rounds != [f"r{n}" for n in range(1, cap + 1)]:
        pytest.fail(f"라운드 디렉터리가 다르다: {rounds}")


# ---------------------------------------------------------------------------
# ⒀ CP2
# ---------------------------------------------------------------------------


def _advanced_with_flags(run_root: str, law: str) -> dict:
    l1_to_pending(run_root, law)
    sa = {"predicate": "sa-02", "locus": {"tweet": 8, "sentence": 3}, "note": "전망"}
    respond_l1(run_root, [{"defects": [], "flags": [], "speech_acts": [sa]}] * 3)
    return run_l1(run_root, law)


def test_cp2_surfaces_draft_and_approve_ship_envelope(run_root, law, tmp_path) -> None:
    _advanced_with_flags(run_root, law)
    view = cp2_mod.surfaces(run_root=run_root, repo=law, variant=VARIANT)
    flag_ids = [f["id"] for f in view["present"]["flags"]]
    if flag_ids != ["f-l0-001", "f-l0-002", "f-l1-003"] or view["present"]["flags"][2]["origin"] != "speech-act":
        pytest.fail(f"플래그 전건(L0 자문 2 + L1 화행 1)이 아니다: {flag_ids}")
    if {row["path"] for row in view["unimplemented"]} != {"50-gate/<variant>/l2.md", "60-probe/<variant>/score.json", "65-critique/<variant>/memo.md", "verdict.json#final_eyes"}:
        pytest.fail(f"결번 표가 다르다: {view['unimplemented']}")
    draft = view["draft"]
    if [row["flag_id"] for row in draft["flags_adjudicated"]] != flag_ids or any(row["verdict"] for row in draft["flags_adjudicated"]):
        pytest.fail("봉투 초안의 flags_adjudicated 가 전 flag id · verdict 비움이 아니다")
    printed = draft["numeric_whitelist_printed"]
    if len(printed) != 1 or set(printed[0]) != {"pattern", "rationale", "added_by", "approved_in"} or printed[0]["approved_in"] != "70-ship/checkpoint2.md":
        pytest.fail(f"numeric_whitelist_printed 4키 · approved_in 봉투 파일명이 아니다: {printed}")
    if draft["manual_verification_ack"] != [] or draft["selected_variant"] != VARIANT or view["present"]["thread_stripped"]["path"] != "50-gate/v2/thread.stripped.md":
        pytest.fail("초안 필드가 다르다")
    # 봉투 — 미판정 1 남긴 채 승인 → 경고 · 스키마 통과 · 파일 생성
    adjudicated = [{"flag_id": fid, "verdict": "accept"} for fid in flag_ids[:2]]
    envelope, warnings = cp2_mod.build_envelope(run_root=run_root, repo=law, variant=VARIANT, decision="approved", owner_quote="출하한다",
                                                located_at="세션", flags_adjudicated=adjudicated)
    if schema_errors("approval-envelope", envelope) or len(warnings) != 1 or "f-l1-003" not in warnings[0]:
        pytest.fail(f"봉투·경고가 다르다: {warnings} {schema_errors('approval-envelope', envelope)}")
    if envelope["target"] != {"path": "50-gate/v2/thread.stripped.md", "digest": sha256_file(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md"))} \
            or envelope["recorded_by"] != "orchestrator" or envelope["checkpoint"] != "ship_approval":
        pytest.fail("봉투 결속 필드가 다르다")
    path = cp2_mod.write_envelope(run_root=run_root, repo=law, envelope=envelope, title="# CP2")
    if not path.endswith("70-ship/checkpoint2.md") or not os.path.isfile(path):
        pytest.fail("70-ship/checkpoint2.md 가 생기지 않았다")
    front = yaml.safe_load(read(path).split("---\n")[1])
    if front != envelope:
        pytest.fail("프런트매터가 봉투와 다르다")
    with pytest.raises(StageError):
        cp2_mod.build_envelope(run_root=run_root, repo=law, variant=VARIANT, decision="rejected", owner_quote="보류", located_at="세션",
                               flags_adjudicated=adjudicated)          # rejected 에 directive 없음 → 스키마 위반
    with pytest.raises(StageError):
        cp2_mod.build_envelope(run_root=run_root, repo=law, variant=VARIANT, decision="approved", owner_quote="x", located_at="세션",
                               flags_adjudicated=[{"flag_id": "f-l0-001", "verdict": ""}])


# ---------------------------------------------------------------------------
# ⒁ 구동기
# ---------------------------------------------------------------------------


class L1Stub:
    """`claude -p` json 출력 흉내 — L1 좌표엔 깨끗한 payload, 펜 좌표엔 국소 수정 초안."""

    def __init__(self, run_root: str):
        self.run_root = run_root
        self.calls: list[list[str]] = []

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        digest = next(line for line in text.split("\n") if line.startswith("| 입력 지문 | `")).split("`")[1]
        observed = argv[argv.index("--model") + 1]
        if lane_id.startswith("gate-l1/"):
            payload = clean_payload()
        else:
            before = read(os.path.join(self.run_root, "40-compose", VARIANT, "thread.annotated.md"))
            payload = {"thread_annotated_md": replace_sentence(before, 4, 2, revised_line(1))}
        body = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "duration_ms": 3, "total_cost_usd": 0.0,
                "session_id": "stub", "structured_output": {"lane_id": lane_id, "model": "self", "effort": "self", "input_digest": digest,
                                                             "payload": payload},
                "modelUsage": {observed: {"inputTokens": 1, "outputTokens": 9}}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 3)


def _drive(law: str, run_root: str, evidence: str, *argv: str, executor=None):
    lines: list[str] = []
    head = ["--repo", law, "--run-root", run_root, "--evidence-dir", evidence]
    return drv.main([*head, *argv], executor=executor, out=lines.append), lines


def test_driver_gate_l1_cp2_approve_ship_and_seal(run_root, law, tmp_path) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    if len(drv.COMMANDS) != 19 or drv.COMMANDS[-4:] != ("gate-l1", "revise", "cp2", "approve-ship"):
        pytest.fail(f"명령 19 가 아니다: {drv.COMMANDS}")
    parser = drv.build_parser()
    listed = tuple(parser._subparsers._group_actions[0].choices)  # noqa: SLF001
    if listed != drv.COMMANDS:
        pytest.fail(f"--help 목록이 COMMANDS 와 다르다: {listed}")
    stub = L1Stub(run_root)
    code, lines = _drive(law, run_root, evidence, "gate-l1", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 3 or not any(line.startswith("v2: l1 pass · defects 0") for line in lines):
        pytest.fail(f"gate-l1 명령: {code} {lines} calls={len(stub.calls)}")
    for argv in stub.calls:
        if argv[argv.index("--model") + 1] != L1_MODEL or argv[argv.index("--effort") + 1] != "high" or argv[argv.index("--tools") + 1] != "":
            pytest.fail(f"L1 레인 명령줄이 다르다: {argv}")
        schema = json.loads(argv[argv.index("--json-schema") + 1])
        if schema["properties"]["payload"].get("title") != "lane-response/gate-l1":
            pytest.fail("L1 좌표에 compose 스키마가 실렸다(래퍼 사전 분기 실패)")
    receipts = sorted(name for name in os.listdir(os.path.join(evidence, "calls")) if name.endswith(".json") and not name.endswith(".raw.json"))
    if receipts != [f"gate-l1__v2__batch-{i}.json" for i in range(3)]:
        pytest.fail(f"영수증 3 이 아니다: {receipts}")
    receipt = read_json(os.path.join(evidence, "calls", receipts[0]))
    if receipt["requested"] != {"model": "opus-5", "effort": "high", "api_id": L1_MODEL} or receipt["observed"]["main_model"] != L1_MODEL:
        pytest.fail(f"영수증 요청·관측이 다르다: {receipt['requested']}")
    code, lines = _drive(law, run_root, evidence, "gate-l1", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 3 or not any("재진입" in line for line in lines):
        pytest.fail(f"gate-l1 재진입: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "cp2", RUN_ID, "--variant", VARIANT)
    if code != drv.EXIT_OK or not any(line.startswith("CP2 ship_approval") for line in lines) or not any("f-l0-001" in line for line in lines):
        pytest.fail(f"cp2 명령: {code} {lines}")
    draft_start = next(i for i, line in enumerate(lines) if line.startswith("--- 봉투 초안"))
    draft = json.loads("\n".join(lines[draft_start + 1:]))
    flags_path = os.path.join(str(tmp_path), "flags.json")
    write_json(flags_path, [{**row, "verdict": "accept"} for row in draft["flags_adjudicated"]])
    quote = os.path.join(str(tmp_path), "quote.txt")
    with open(quote, "w", encoding="utf-8") as handle:
        handle.write("v2 로 출하한다\n")
    code, lines = _drive(law, run_root, evidence, "approve-ship", RUN_ID, "--quote-file", quote, "--selected", VARIANT, "--flags", flags_path,
                         "--decision", "rejected")
    if code != drv.EXIT_USAGE:
        pytest.fail(f"rejected 에 directive 없음이 2 가 아니다: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "approve-ship", RUN_ID, "--quote-file", quote, "--selected", VARIANT, "--flags", flags_path)
    envelope_path = os.path.join(run_root, "70-ship", "checkpoint2.md")
    if code != drv.EXIT_OK or not os.path.isfile(envelope_path) or any(line.startswith("경고") for line in lines):
        pytest.fail(f"approve-ship: {code} {lines}")
    front = yaml.safe_load(read(envelope_path).split("---\n")[1])
    if schema_errors("approval-envelope", front) or front["selected_variant"] != VARIANT or front["numeric_whitelist_printed"][0]["approved_in"] != "70-ship/checkpoint2.md" \
            or front["manual_verification_ack"] != []:
        pytest.fail(f"봉투가 다르다: {front}")
    code, lines = _drive(law, run_root, evidence, "lanes", RUN_ID)
    if code != drv.EXIT_OK or sum("gate-l1/v2/batch-" in line for line in lines) != 3:
        pytest.fail(f"lanes 에 L1 좌표가 없다: {lines}")
    code, lines = _drive(law, run_root, evidence, "seal", RUN_ID)
    manifest = read(os.path.join(evidence, "MANIFEST-sha256.txt"))
    for needle in ("50-gate/v2/lanes/gate-l1/v2/batch-0/response.json", "70-ship/checkpoint2.md", "50-gate/v2/final-eyes-brief.json", "50-gate/v2/l1.json"):
        if not any(line.endswith(needle) for line in manifest.splitlines()):
            pytest.fail(f"seal 에 {needle} 이 없다")


def test_driver_revise_one_round_with_stub(run_root, law, tmp_path) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    _l1_defect_state(run_root, law)
    stub = L1Stub(run_root)
    code, lines = _drive(law, run_root, evidence, "revise", RUN_ID, "--variant", VARIANT, executor=stub)
    verdict = verdict_of(run_root)
    if code != drv.EXIT_OK or len(stub.calls) != 4 or verdict["revision_round"] != 1 or verdict["decision"] != "advance":
        pytest.fail(f"revise 명령: {code} {lines} calls={len(stub.calls)} {verdict['decision']}")
    if not any("라운드 1 종결" in line for line in lines):
        pytest.fail(f"revise 출력이 다르다: {lines}")
    receipts = sorted(name for name in os.listdir(os.path.join(evidence, "calls")) if name.endswith(".json") and not name.endswith(".raw.json"))
    if "compose-r3__v2__batch-0.json" not in receipts or "gate-l1__v2__batch-2.json" not in receipts:
        pytest.fail(f"라운드 영수증이 다르다: {receipts}")
    early = make_run(os.path.join(str(tmp_path), "e"), partial_until="compose")
    code, _ = _drive(law, early, evidence, "gate-l1", RUN_ID)
    if code != drv.EXIT_TERMINAL_FAIL:
        pytest.fail(f"종료선 앞 gate-l1 이 13 이 아니다: {code}")


# ---------------------------------------------------------------------------
# ⒂ 회귀 표본
# ---------------------------------------------------------------------------


def test_regression_golden_is_byte_copy_of_run3_and_mutated_samples_are_registered() -> None:
    pairs = (("thread.annotated.md", os.path.join(RUN3, "40-compose", VARIANT, "thread.annotated.md")),
             ("material-spec.frozen.json", os.path.join(RUN3, "15-frozen", "material-spec.v1.json")),
             ("blueprint.json", os.path.join(RUN3, "20-design", "blueprint.json")))
    for name, source in pairs:
        if open(os.path.join(GOLDEN, name), "rb").read() != open(source, "rb").read():
            pytest.fail(f"골든 {name} 이 런 -3 실물과 바이트가 다르다")
    meta = read_json(os.path.join(GOLDEN, "meta.json"))
    if meta["golden_id"] != "rc-0009-agent-memory-v2" or meta["spec_digest"] != sha256_file(os.path.join(GOLDEN, "material-spec.frozen.json")) \
            or "실특허 실물" not in meta["note"] or "가공 아님" not in meta["note"] or meta["source"]["byte_identical"] is not True:
        pytest.fail("골든 meta.json 이 실물 복사를 명기하지 않는다")
    golden_lines = read(os.path.join(GOLDEN, "thread.annotated.md")).split("\n")
    rows = {}
    with open(os.path.join(REGRESSION, "cases.jsonl"), encoding="utf-8") as handle:
        for raw in handle:
            if raw.strip():
                row = json.loads(raw)
                rows[row["case_id"]] = row
    index = read_json(os.path.join(RUN3, "50-gate", VARIANT, "annotation-index.json"))
    sentence_counts = {t["n"]: len(t["sentences"]) for t in index["tweets"]}
    expected = {"rc-0009": ("hallucinated-claim", "l1.citation-mismatch"), "rc-0010": ("smuggled-claim-in-narrative", "l1.narrative-smuggling"),
                "rc-0011": ("solicitation-sentence", "speech-act.sa-01")}
    for case_id, (mtype, detector) in expected.items():
        row = rows.get(case_id)
        if row is None or set(row) != {"case_id", "base", "mutation", "expect"} or row["base"] != "golden/rc-0009-agent-memory-v2/thread.annotated.md":
            pytest.fail(f"cases.jsonl 의 {case_id} 행이 §4.8 서식이 아니다: {row}")
        if row["mutation"]["type"] != mtype or row["expect"] != {"detector": detector, "must_detect": True}:
            pytest.fail(f"{case_id} 의 mutation.type·expect 가 다르다: {row}")
        locus = row["mutation"]["locus"]
        if locus["tweet"] not in sentence_counts or not 1 <= locus["sentence"] <= sentence_counts[locus["tweet"]]:
            pytest.fail(f"{case_id} 의 locus 가 표본 밖이다: {locus}")
        folder = os.path.join(REGRESSION, "mutated", MUTATED[case_id])
        sample = read(os.path.join(folder, "thread.annotated.md")).split("\n")
        if len(sample) != len(golden_lines):
            pytest.fail(f"{case_id} 변조본의 행 수가 골든과 다르다")
        diff = [i for i, (a, b) in enumerate(zip(golden_lines, sample)) if a != b]
        header = next(i for i, line in enumerate(golden_lines) if line.startswith(f"## T{locus['tweet']} "))
        if diff != [header + locus["sentence"]]:
            pytest.fail(f"{case_id} 변조본이 좌표 문장 하나만 바꾸지 않았다: diff 행 {diff} · 기대 {header + locus['sentence']}")
        mmeta = read_json(os.path.join(folder, "meta.json"))
        if mmeta["case_id"] != case_id or mmeta["mutation"] != row["mutation"] or mmeta["expected_detector"] != detector or mmeta["base_golden_id"] != "rc-0009-agent-memory-v2":
            pytest.fail(f"{case_id} meta.json 이 cases.jsonl 과 어긋난다")
        if mmeta["spec_digest"] != meta["spec_digest"] or f"spec_digest: {meta['spec_digest']}" not in "\n".join(sample[:6]):
            pytest.fail(f"{case_id} 변조본의 재료 판이 골든과 다르다")
    # 자기매칭 격리 — 심은 문장 리터럴이 시험 소스·원장·meta 에 없다
    source = read(os.path.realpath(__file__))
    for case_id, folder_name in MUTATED.items():
        folder = os.path.join(REGRESSION, "mutated", folder_name)
        sample = read(os.path.join(folder, "thread.annotated.md")).split("\n")
        locus = rows[case_id]["mutation"]["locus"]
        header = next(i for i, line in enumerate(sample) if line.startswith(f"## T{locus['tweet']} "))
        planted = sample[header + locus["sentence"]].rsplit("[", 1)[0]
        for haystack_path in (os.path.realpath(__file__), os.path.join(REGRESSION, "cases.jsonl"), os.path.join(folder, "meta.json")):
            if planted in read(haystack_path):
                pytest.fail(f"{case_id} 의 심은 문장이 {haystack_path} 에 리터럴로 있다(§4.8 격리 위반)")
    if "planted" not in source:
        pytest.fail("자기 점검 표지")


# ---------------------------------------------------------------------------
# ⒃ 절차 문서 · 펜 템플릿 린트 · gate.run 보존 규약
# ---------------------------------------------------------------------------


def test_procedure_doc_names_predicates_and_pen_template_stays_lint_clean(law) -> None:
    procedure = read(os.path.join(law, "engine", "gate", "l1", "procedure.md"))
    for needle in ("l1.citation-mismatch", "l1.narrative-smuggling", "l1.advice-implicit", "sa-01", "sa-02", "sa-03", "gate.no-rewrite",
                   "This is the part where the memory sits right next to the compute."):
        if needle not in procedure:
            pytest.fail(f"L1 절차 문서에 {needle} 이 없다")
    template = read(os.path.join(law, "engine", "pens", "prompt-template.md"))
    if "## 9. 국소 수정" not in template or "바이트 그대로" not in template:
        pytest.fail("펜 템플릿에 국소 수정 절이 없다")
    if lint.lint_prompt(template, law):
        pytest.fail(f"펜 템플릿 린트가 0 이 아니다: {lint.lint_prompt(template, law)}")
    if lint.DATA_SUBSECTION_PREFIXES[1] != "## 국소 수정 지시 표" or lint.DATA_SUBSECTION_PREFIX != "## 블루프린트 요약":
        pytest.fail("린트 데이터 절 접두가 다르다")


def test_rejudgment_preserves_lanes_but_keeps_brief_and_revisions_in_place(run_root, law) -> None:
    l1_to_pending(run_root, law)
    respond_l1(run_root, [clean_payload()] * 3)
    run_l1(run_root, law)
    gate_dir = os.path.join(run_root, "50-gate", VARIANT)
    brief_before = open(os.path.join(gate_dir, "final-eyes-brief.json"), "rb").read()
    os.makedirs(os.path.join(gate_dir, "revisions", "r9"), exist_ok=True)
    path = os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")
    changed = replace_sentence(read(path), 4, 2, revised_line(1))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(changed)
    gate_stage.run(run_root=run_root, repo=law, variants=[VARIANT])
    kept = sorted(os.listdir(gate_dir))
    if "lanes" in kept or "l1.json" in kept or "final-eyes-brief.json" not in kept or "revisions" not in kept:
        pytest.fail(f"보존 규약이 다르다: {kept}")
    if open(os.path.join(gate_dir, "final-eyes-brief.json"), "rb").read() != brief_before:
        pytest.fail("발췌본이 재판정에서 바뀌었다")
    moved = sorted(os.listdir(os.path.join(gate_dir, "rounds", "r2")))
    if "lanes" not in moved or "l1.json" not in moved or "verdict.json" not in moved:
        pytest.fail(f"rounds/r2 에 레인·l1.json·판정문이 없다: {moved}")
    verdict = verdict_of(run_root)
    if verdict["l1"]["pass"] is not None or not any(row["layer"] == "l1" for row in verdict["inactive_layers"]) or "final_eyes_brief_digest" in verdict:
        pytest.fail("재판정 판정문이 L1 미실행 상태로 돌아가지 않았다")
    outcome = run_l1(run_root, law)
    if outcome["status"] != "pending" or verdict_of(run_root)["final_eyes_brief_digest"] != sha256_bytes(brief_before):
        pytest.fail("재판정 뒤 L1 재진입이 보존 판정문의 핀을 잇지 못한다")
