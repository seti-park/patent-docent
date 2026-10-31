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
# 런 -3 는 살아 있는 런이라 반입마다 상태가 앞으로 간다. 이 시험의 전제(L0 통과 · L1 미실행)는 `98ce4e7^`(= c42f1ff) 상태의
# 바이트 사본 `tests/fixtures/run3-snapshots/pre-l1/` 에 고정한다(40-compose · 50-gate/v2 두 트리 · 나머지는 실물 그대로).
SNAPSHOT = os.path.join(REPO, "tests", "fixtures", "run3-snapshots", "pre-l1")
VARIANT = "v2"
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
REGRESSION = os.path.join(REPO, "ledgers", "regression")
GOLDEN = os.path.join(REGRESSION, "golden", "rc-0009-agent-memory-v2")
MUTATED = {"rc-0009": "rc-0009-hallucinated-claim", "rc-0010": "rc-0010-smuggled-claim", "rc-0011": "rc-0011-solicitation"}
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"),
             ("engine", "gate", "l1", "procedure.md"))
COPIED_DIRS = ("15-frozen", "20-design", "30-figures", "40-compose", os.path.join("50-gate", VARIANT))
SNAPSHOT_DIRS = ("40-compose", os.path.join("50-gate", VARIANT))


def run3_source(rel: str) -> str:
    return os.path.join(SNAPSHOT if rel in SNAPSHOT_DIRS else RUN3, rel)
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
        shutil.copytree(run3_source(rel), os.path.join(run_root, rel))
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
    if layers["l2"]["status"] != "active" or layers["final_eyes"]["status"] != "active":   # L2 = T69 ⑥ · 최종 심급 = T69 ⑦
        pytest.fail("L2·최종 심급이 가동 표기가 아니다")
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


# ---------------------------------------------------------------------------
# ⑺ final-eyes-brief
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑻ decision · inactive_layers  ⑼ L0 결함 변주
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑽ ⑾ ⑿ 수정 라운드
# ---------------------------------------------------------------------------


def _l1_defect_state(run_root: str, law: str) -> dict:
    l1_to_pending(run_root, law)
    respond_l1(run_root, [{"defects": [defect("l1.citation-mismatch", 4, 2)], "flags": [], "speech_acts": []}] * 3)
    return run_l1(run_root, law)


def test_revision_cap_matches_schema_maximum(law) -> None:
    """캡은 두 곳에 있다 — 계약 `gate.yaml#loop.revision_cap` 과 판정문 스키마의 `revision_round.maximum`.

    어긋나면 캡 안의 마지막 라운드가 스키마에서 거부된다(재정 T70 ① 로 캡을 3→4 로 늘렸을 때 실측).
    """
    cap = gate_stage.revision_cap(load_stage_contract("gate", law))
    schema = read_json(os.path.join(SCHEMAS, "gate-report.schema.json"))
    maximum = schema["properties"]["revision_round"]["maximum"]
    if maximum != cap:
        pytest.fail(f"스키마 상한 {maximum} 과 계약 캡 {cap} 이 다르다 — 캡 안의 라운드가 거부된다")


# ---------------------------------------------------------------------------
# ⒀ CP2
# ---------------------------------------------------------------------------


def synthesize_downstream(run_root: str, law: str, variant: str = VARIANT) -> None:
    """CP2 는 T69 ⑦ 부터 L2·계기·소견·최종 심급을 전제한다. 이 모듈은 ⑤(L1·수정 루프·봉투) 시험이므로
    그 네 층은 **최소 합성**으로만 세운다 — 각 층의 본시험은 m36(L2·계기)·m37(소견·최종 심급·출하)이다."""
    from engine.gate import final_eyes as fe_mod
    from engine.stages import write_text as _write_text

    paths = RunPaths(run_root, law)
    stripped = paths.thread_stripped_md(variant)
    digest = sha256_file(stripped)
    targets = read_json(paths.blueprint_json)["transmission_targets"]
    write_json(paths.score_json(variant), {
        "input_digest": digest, "delivery_fidelity": 0.5,
        "per_target": [{"material_id": t, "hit_rate": 0.5, "weakest_tweet": 1} for t in targets],
        "restatement": {"aligned": len(targets)},
    })
    _write_text(paths.l2_md(variant), "# L2 자문 메모\n구조의 흐름을 확인했다.\n")
    memo_path = paths.critique_memo(variant)
    _write_text(memo_path, "# 소견\n훅은 조응하고 착지는 안도감으로 닫힌다.\n")
    write_json(os.path.join(paths.critique_dir(variant), "critique-report.json"), {
        "status": "ok", "candidate_digest": digest, "memo_digest": sha256_file(memo_path),
    })
    meta = yaml.safe_load(read(paths.run_yaml))
    version = int(meta["frozen"][-1]["spec_version"])
    verdict = read_json(paths.verdict_json(variant))
    verdict["inactive_layers"] = []
    verdict["final_eyes"] = {
        "verdict": "pass", "veto_reason": None, "observations": [],
        "inputs_read": fe_mod.input_records(paths, fe_mod.provided_files(paths, variant, version)),
    }
    write_json(paths.verdict_json(variant), verdict)


def _advanced_with_flags(run_root: str, law: str) -> dict:
    l1_to_pending(run_root, law)
    sa = {"predicate": "sa-02", "locus": {"tweet": 8, "sentence": 3}, "note": "전망"}
    respond_l1(run_root, [{"defects": [], "flags": [], "speech_acts": [sa]}] * 3)
    return run_l1(run_root, law)


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


# ---------------------------------------------------------------------------
# ⒂ 회귀 표본
# ---------------------------------------------------------------------------


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

