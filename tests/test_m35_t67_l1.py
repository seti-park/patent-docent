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

# 런 -3 는 살아 있는 런이라 반입마다 상태가 앞으로 간다. 이 시험의 전제(L0 통과 · L1 미실행)는 `98ce4e7^`(= c42f1ff) 상태의
# 바이트 사본 `tests/fixtures/run3-snapshots/pre-l1/` 에 고정한다(40-compose · 50-gate/v2 두 트리 · 나머지는 실물 그대로).
VARIANT = "v2"
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"),
             ("engine", "gate", "l1", "procedure.md"))


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


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


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


def clean_payload() -> dict:
    return {"defects": [], "flags": [], "speech_acts": []}


def defect(rule: str, tweet: int, sentence: int, directive: str | None = None) -> dict:
    return {"rule": rule, "locus": {"tweet": tweet, "sentence": sentence}, "expected": "재료 항목의 EN 값과 합치",
            "observed": "재료가 말하지 않는 단정", "fix_directive": directive or f"T{tweet}/S{sentence} 가 인용한 재료로 재서술하라 — 재료 밖 단정을 빼라"}


def run_l1(run_root: str, law: str, variant: str = VARIANT) -> dict:
    return gate_stage.run_l1(run_root=run_root, repo=law, variant=variant)


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


# ---------------------------------------------------------------------------
# ⒁ 구동기
# ---------------------------------------------------------------------------


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

