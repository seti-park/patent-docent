# -*- coding: utf-8 -*-
"""M31 — `design` 스테이지 실물화(재정 2026-09-13 T64 ②) + 구동기 `extend`·`design`(T64 ①·재량).

실제 `claude` 는 부르지 않는다(스텁 실행기). 런 -3 픽스처(동결본 v1)는 읽기만 하고 tmp 로 복사해 쓴다.
법 트리는 계약 + reader + 헌장 + 설계 절차 문서만 담은 깨끗한 임시 git 리포다.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import stat
import subprocess
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.lanes.contract import LaneContractError, LaneRequest, render_request_body  # noqa: E402
from engine.lanes.file_adapter import FileLaneAdapter  # noqa: E402
from engine.paths import RunPaths, load_format_parameters, load_stage_contract  # noqa: E402
from engine.stages import StageEnvironmentError, StageHaltError, sha256_file  # noqa: E402
from engine.stages import design as design_stage  # noqa: E402
from engine.stages import freeze as freeze_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

RUN_ID = "gdm-wo2026128750a1-agent-memory-3"
FROZEN_FIXTURE = os.path.join(REPO, "runs", RUN_ID, "15-frozen", "material-spec.v1.json")
FIXTURE_DIR = os.path.join(REPO, "tests", "fixtures", "schema-enforcement")
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"))
LANE_ID = "design/blueprint/batch-0"
RETRY_LANE_ID = "design/blueprint/retry-1/batch-0"


# ---------------------------------------------------------------------------
# 픽스처
# ---------------------------------------------------------------------------


def _git(cwd: str, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        pytest.fail(f"git {' '.join(args)} 실패: {proc.stderr}")
    return proc.stdout.strip()


def make_law(destination: str) -> str:
    """계약 + reader + 헌장 + 설계 절차 문서를 담은 깨끗한 git 리포(브랜치 main)."""
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


def make_run(root: str, *, partial_until: str = "gate") -> str:
    """동결본 v1 을 복사(0444)하고 합성 run.yaml 을 둔 런 루트."""
    run_root = os.path.join(root, "runs", RUN_ID)
    frozen_dir = os.path.join(run_root, "15-frozen")
    os.makedirs(frozen_dir, exist_ok=True)
    frozen = os.path.join(frozen_dir, "material-spec.v1.json")
    shutil.copyfile(FROZEN_FIXTURE, frozen)
    os.chmod(frozen, 0o444)
    meta = {
        "schema": "run/v0",
        "run_id": RUN_ID,
        "status": "active",
        "run_kind": "partial",
        "partial_until": partial_until,
        "engine": {"commit": "e" * 40, "worktree": None},
        "numeric_whitelist": [],
        "frozen": [{"spec_version": 1, "path": "15-frozen/material-spec.v1.json", "spec_digest": sha256_file(frozen)}],
    }
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    return run_root


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(str(tmp_path))


def frozen_spec() -> dict:
    with open(FROZEN_FIXTURE, encoding="utf-8") as handle:
        return json.load(handle)


FROZEN = frozen_spec()
SHEET = design_stage.sheet_values(REPO)
FIGS = [figure["id"] for figure in FROZEN["figures"]]
COMPONENTS = [item["id"] for item in FROZEN["items"] if item["kind"] == "component"]


def good_payload() -> dict:
    """시트(6~12 · hook@T1 · landing 1 · other ∈ stop|pivot · 도면 ≤ 4)를 만족하는 레인 응답 payload."""
    slots = [
        {"n": 1, "slot": "hook", "exhibit": {"material_ids": [COMPONENTS[0]], "point_en": "Ask the question."}, "figures": [FIGS[0]]},
        {"n": 2, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[1]], "point_en": "One component."}, "figures": [FIGS[1]]},
        {"n": 3, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[2]], "point_en": "Another component."}, "figures": [FIGS[2]]},
        {"n": 4, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[3]], "point_en": "Third component."}, "figures": [FIGS[3]]},
        {"n": 5, "slot": "pivot", "exhibit": {"material_ids": [COMPONENTS[4]], "point_en": "The decisive evidence."}, "figures": [FIGS[4]]},
        {"n": 6, "slot": "landing", "exhibit": {"material_ids": [COMPONENTS[0], COMPONENTS[1]], "point_en": "Relief."}, "figures": []},
    ]
    return {
        "hook": {"question_en": "Is the moat real?", "figure": FIGS[0], "thesis_en": "It is.", "rationale_kr": "최강 도면."},
        "slots": slots,
        "transmission_targets": [COMPONENTS[0], COMPONENTS[1], COMPONENTS[2]],
        "new_terms": [{"term_en": "datastore", "tweet": 2, "gloss_en": "where memories live"}],
        "figure_plan": [{"tweet": slot["n"], "figures": list(slot["figures"]), "intent_kr": "지정만"} for slot in slots],
        "numeric_whitelist": [{"pattern": "^\\d{1,2}/\\d{1,2}$", "rationale": "thread ordinal n/N"}],
        "overflow_proposal": None,
        "escalation": None,
    }


def candidate_from(payload: dict, run_root: str, *, law: str) -> dict:
    """러너 6키를 채운 후보(검사 단위 시험용)."""
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    out = dict(copy.deepcopy(payload))
    out.update({
        "schema": "blueprint/v0", "run_id": RUN_ID, "spec_version": 1,
        "spec_digest": meta["frozen"][0]["spec_digest"],
        "lane": {"model": "claude-fable-5-1", "effort": "high", "lane_id": LANE_ID},
        "law_commit": design_stage.law_commit_of(law),
    })
    return out


def respond(run_root: str, lane_id: str, payload: dict, *, model: str = "claude-fable-5-1", effort: str = "high") -> str:
    """파일 어댑터가 쓴 요청의 지문을 반향하는 응답 파일을 쓴다(시험이 레인 역할)."""
    directory = os.path.join(run_root, "20-design", "lanes", *lane_id.split("/"))
    with open(os.path.join(directory, "request.json"), encoding="utf-8") as handle:
        request = json.load(handle)
    path = os.path.join(directory, "response.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"lane_id": lane_id, "model": model, "effort": effort,
                   "input_digest": request["input_digest"], "payload": payload}, handle, ensure_ascii=False)
    return path


def run_design(run_root: str, law: str) -> dict:
    return design_stage.run(run_root=run_root, repo=law)


def rules_of(row) -> list[str]:
    return [finding.rule for finding in row.findings]


def rows_by_id(outcome: dict) -> dict:
    return {row.check_id: row for row in outcome["rows"]}


# ---------------------------------------------------------------------------
# ⑴ 계약 · 경로
# ---------------------------------------------------------------------------


def test_contract_loads_and_paths_declare_design_outputs(law) -> None:
    contract = load_stage_contract("design", law)
    ids = [row["id"] for row in contract["checks_before_exit"]]
    if contract["schema"] != "stage-contract/v0" or contract["id"] != "design" or len(ids) != 6:
        pytest.fail(f"design.yaml 골격이 다르다: {contract.get('schema')} · {ids}")
    if contract["lane"]["model"] != "fable-5.1" or contract["lane"]["effort"] != "high":
        pytest.fail("설계 좌석이 fable-5.1 high 가 아니다(T64 재량)")
    paths = RunPaths("/nonexistent/run", law)
    if paths.STAGES[:4] != ("source", "read", "freeze", "design"):
        pytest.fail(f"STAGES 가 다르다: {paths.STAGES}")
    if not paths.blueprint_json.endswith("20-design/blueprint.json") or not paths.blueprint_md.endswith("20-design/blueprint.md"):
        pytest.fail("blueprint.json·blueprint.md 선언이 없다")
    if not paths.design_lanes_dir.endswith("20-design/lanes") or not paths.design_report_json.endswith("design-report.json"):
        pytest.fail("design_lanes_dir·design_report_json 이 다르다")
    if not paths.extension(3).endswith("15-frozen/extension-v3.md"):
        pytest.fail("extension(N) 경로가 다르다")
    # READ 세 계약의 선언과 충돌하지 않는다(같은 basename 이 다른 경로로 둘 이상 선언되지 않는다).
    for basename in ("run.yaml", "patent.md", "material-spec.json", "material-spec.v<N>.json", "approval-v<N>.md"):
        paths.declared(basename)


def test_schema_slot_enum_equals_sheet_slot_enum() -> None:
    schema = design_stage.load_blueprint_schema(REPO)
    if schema["$defs"]["slot"]["enum"] != list(SHEET["slot_enum"]):
        pytest.fail("스키마 슬롯 enum 이 시트 slot_enum 과 다르다 — 시트가 정본이다")


# ---------------------------------------------------------------------------
# ⑵ ⑶ 스키마 · 응답 payload 파생
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name, locus",
    [
        ("missing-hook", "$"),
        ("slot-outside-enum", "slots/1/slot"),
        ("spec-digest-format", "spec_digest"),
        ("overflow-without-proposal", "overflow_proposal"),
        ("empty-targets", "transmission_targets"),
    ],
)
def test_reject_fixtures_fail_at_declared_locus(name, locus) -> None:
    schema = design_stage.load_blueprint_schema(REPO)
    validator = Draft202012Validator(schema)
    accept = json.load(open(os.path.join(FIXTURE_DIR, "accept", "blueprint.minimal.json"), encoding="utf-8"))
    if list(validator.iter_errors(accept)):
        pytest.fail("accept 픽스처가 스키마를 통과하지 못한다")
    instance = json.load(open(os.path.join(FIXTURE_DIR, "reject", f"blueprint.{name}.json"), encoding="utf-8"))
    loci = sorted({"/".join(str(step) for step in err.absolute_path) or "$" for err in validator.iter_errors(instance)})
    if loci != [locus]:
        pytest.fail(f"{name}: 선언한 자리 하나에서 거부되지 않는다 — {loci}")


def test_payload_schema_is_file_schema_minus_runner_keys() -> None:
    file_schema = design_stage.load_blueprint_schema(REPO)
    payload = design_stage.RESPONSE_SCHEMAS["blueprint"]
    defs = file_schema["$defs"]
    expected_props = design_stage._inline_refs(
        {k: v for k, v in file_schema["properties"].items() if k not in design_stage.RUNNER_KEYS}, defs
    )
    if payload["properties"] != expected_props:
        pytest.fail("payload 스키마 properties 가 파일 스키마 − 러너 6키(참조 인라인)가 아니다")
    if payload["required"] != [k for k in file_schema["required"] if k not in design_stage.RUNNER_KEYS]:
        pytest.fail("payload 스키마 required 가 파생물이 아니다")
    if payload["allOf"] != design_stage._inline_refs(file_schema["allOf"], defs) or "$defs" in payload:
        pytest.fail("allOf 가 파생되지 않았거나 $defs 가 남아 있다")
    if any(branch.get("type") != "object" for branch in payload["allOf"]):
        pytest.fail("allOf 가지에 type: object 가 없다(CLI strict 경고)")
    wrapper = drv.wrapper_schema("blueprint")
    if wrapper["properties"]["payload"] is not payload:
        pytest.fail("구동기 wrapper_schema 가 design.RESPONSE_SCHEMAS 상수를 품지 않는다")


def _refs_in(node) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            found.append(node["$ref"])
        for value in node.values():
            found.extend(_refs_in(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(_refs_in(value))
    return found


def test_wrapper_schema_is_self_contained_and_resolves_inside_cli_wrapper() -> None:
    """2026-09-13 런 -3 design 첫 호출 실측 — 래퍼 안의 `#/$defs/figure_id` 가 해소되지 않아 CLI 가
    `--json-schema is not a valid JSON Schema: can't resolve reference` 로 호출을 거부했다(발주자 오류 253).
    래퍼 전체에 `$ref` 가 없어야 하고, 래퍼 루트 기준으로 유효 payload 가 실제로 검증되어야 한다."""
    wrapper = drv.wrapper_schema("blueprint")
    refs = _refs_in(wrapper)
    if refs:
        pytest.fail(f"래퍼 스키마에 해소되지 않는 참조가 남아 있다: {refs}")
    Draft202012Validator.check_schema(wrapper)
    with open(os.path.join(REPO, "tests", "fixtures", "schema-enforcement", "accept", "blueprint.minimal.json"),
              encoding="utf-8") as handle:
        accepted = json.load(handle)
    payload = {k: v for k, v in accepted.items() if k not in design_stage.RUNNER_KEYS}
    envelope = {"lane_id": "design/blueprint/batch-0", "model": "claude-fable-5-1", "effort": "high",
                "input_digest": "0" * 64, "payload": payload}
    errors = list(Draft202012Validator(wrapper).iter_errors(envelope))
    if errors:
        pytest.fail(f"유효 payload 가 래퍼 루트 기준 검증에서 거부됐다: {errors[0].message}")
    bad = dict(envelope, payload=dict(payload, hook=dict(payload["hook"], figure="fig-01")))
    if not list(Draft202012Validator(wrapper).iter_errors(bad)):
        pytest.fail("인라인된 figure_id 패턴이 무효 도면 ID 를 통과시켰다 — 참조 본문이 펴지지 않았다")


# ---------------------------------------------------------------------------
# ⑷ ⑸ 어휘 · 요청서
# ---------------------------------------------------------------------------


def _fields(lane_id: str, read_run: str, task: str) -> dict:
    return dict(lane_id=lane_id, read_run=read_run, task=task, model="fable-5.1", effort="high",
                prompt_path="engine/procedure/design.md", instructions="x", repo_root=REPO,
                response_schema={"type": "object"})


def test_design_vocabulary_hook_keeps_read_vocabulary_unchanged() -> None:
    design_stage.DesignLaneRequest(**_fields(LANE_ID, "design", "blueprint"))
    design_stage.DesignLaneRequest(**_fields(RETRY_LANE_ID, "design", "blueprint"))
    with pytest.raises(LaneContractError, match=r"어휘 위반\(소속\)"):
        LaneRequest(**_fields(LANE_ID, "design", "blueprint"))
    with pytest.raises(LaneContractError, match=r"어휘 위반\(소속\)"):
        design_stage.DesignLaneRequest(**_fields("read-a/decompose/batch-0", "read-a", "decompose"))
    if design_stage.lane_id_for(0) != LANE_ID or design_stage.lane_id_for(1) != RETRY_LANE_ID:
        pytest.fail("설계 좌표 문법이 다르다")


def test_request_body_inlines_frozen_sheet_charter_and_excludes_source(law, run_root) -> None:
    outcome = run_design(run_root, law)
    if outcome["status"] != "pending" or outcome["pending"] != [LANE_ID]:
        pytest.fail(f"첫 진입이 pending 이 아니다: {outcome['status']} {outcome['pending']}")
    request_md = os.path.join(run_root, "20-design", "lanes", "design", "blueprint", "batch-0", "request.md")
    body = open(request_md, encoding="utf-8").read()
    frozen_text = open(FROZEN_FIXTURE, encoding="utf-8").read().rstrip("\n")
    if frozen_text not in body:
        pytest.fail("동결본 JSON 전문이 요청서에 없다")
    for needle in (f"| tweet_count.max | `{SHEET['tweet_count']['max']}` |", f"| images_per_post_max | `{SHEET['images_per_post_max']}` |",
                   "## D2. 독자상", "## D3. 핵심 독트린", "## D11. 형식", "재정된 앵커 0건", "도면은 **지정만**",
                   "# 설계 레인 절차", "| 모델 | `fable-5.1` |", "| effort | `high` |"):
        if needle not in body:
            pytest.fail(f"요청서에 {needle!r} 가 없다")
    # 동결본 값(figures[].raw_path · patent.source_path)은 원천 **경로 문자열**을 든다 — 그것은 재료의
    # 값이지 원천 내용이 아니다. 금지 대조는 동결본 조각을 뺀 나머지(지시·절차·헌장 발췌)에 건다.
    outside_slice = body.replace(frozen_text, "")
    for forbidden in ("00-source", "10-read"):
        if forbidden in outside_slice:
            pytest.fail(f"요청서(동결본 조각 밖)에 must_not_read 경로 {forbidden!r} 문자열이 있다")
    request_json = json.load(open(request_md.replace("request.md", "request.json"), encoding="utf-8"))
    if request_json["model"] != "fable-5.1" or request_json["effort"] != "high" or request_json["task"] != "blueprint":
        pytest.fail(f"request.json 좌석이 다르다: {request_json['model']}/{request_json['effort']}")


# ---------------------------------------------------------------------------
# ⑹ 앵커 필터
# ---------------------------------------------------------------------------


def test_anchor_filter_and_check(law, run_root, tmp_path) -> None:
    ledger = os.path.join(law, "ledgers", "anchors", "anchors.jsonl")
    os.makedirs(os.path.dirname(ledger), exist_ok=True)
    rows = [
        {"id": "A1", "state": "active", "adjudicated_in": "ruling-20260913-09-T64.md", "text": "x"},
        {"id": "A2", "state": "provisional", "adjudicated_in": "ruling-x.md", "text": "y"},
        {"id": "A3", "state": "active", "adjudicated_in": None, "text": "z"},
    ]
    with open(ledger, "w", encoding="utf-8") as handle:
        handle.write("\n".join(json.dumps(row) for row in rows) + "\n")
    provided, excluded = design_stage.adjudicated_anchors(law)
    if [row["id"] for row in provided] != ["A1"] or excluded != 2:
        pytest.fail(f"앵커 필터가 다르다: {provided} · 차단 {excluded}")
    outcome = run_design(run_root, law)
    provided_path = os.path.join(run_root, "20-design", "anchors-provided.json")
    written = json.load(open(provided_path, encoding="utf-8"))
    if [row["id"] for row in written["provided"]] != ["A1"] or written["excluded_count"] != 2:
        pytest.fail("anchors-provided.json 이 필터 결과와 다르다")
    request_md = open(os.path.join(outcome["lanes_root"], "design", "blueprint", "batch-0", "request.md"), encoding="utf-8").read()
    if "`A1`" not in request_md or "A2" in request_md or "A3" in request_md:
        pytest.fail("요청서의 앵커 블록이 제공 목록과 다르다")
    row = design_stage.check_anchors_adjudicated_only(provided_path)
    if row.status != "pass" or row.checked != 1:
        pytest.fail(f"제공 1건이 통과하지 않는다: {rules_of(row)}")
    written["provided"][0]["state"] = "provisional"
    json.dump(written, open(provided_path, "w", encoding="utf-8"))
    if design_stage.check_anchors_adjudicated_only(provided_path).status != "fail":
        pytest.fail("provisional 이 섞였는데 통과했다")
    missing = os.path.join(str(tmp_path), "absent.json")
    empty = design_stage.check_anchors_adjudicated_only(missing)
    if empty.checked != 0 or empty.to_row_dict()["vacuous"] != "empty-target":
        pytest.fail("원장 부재가 정직한 공허(empty-target)로 서지 않는다")


# ---------------------------------------------------------------------------
# ⑺ ⑻ slot-count · 시트 결속
# ---------------------------------------------------------------------------


def _slots(n: int) -> list[dict]:
    out = [{"n": 1, "slot": "hook", "exhibit": {"material_ids": [COMPONENTS[0]], "point_en": "q"}, "figures": [FIGS[0]]}]
    for k in range(2, n):
        out.append({"n": k, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[k % len(COMPONENTS)]], "point_en": "s"}, "figures": []})
    out.append({"n": n, "slot": "landing", "exhibit": {"material_ids": [COMPONENTS[0]], "point_en": "l"}, "figures": []})
    return out


def test_slot_count_rules_each_fail_with_distinct_rule() -> None:
    base = {"slots": _slots(6)}
    if design_stage.check_slot_count(base, SHEET).status != "pass":
        pytest.fail("기준 판이 통과하지 않는다")

    def mutate(fn):
        payload = copy.deepcopy(base)
        fn(payload["slots"])
        return rules_of(design_stage.check_slot_count(payload, SHEET))

    cases = {
        "slot.hook-count": lambda s: s[1].__setitem__("slot", "hook"),
        "slot.hook-position": lambda s: (s[0].__setitem__("slot", "stop"), s[1].__setitem__("slot", "hook")),
        "slot.landing-count": lambda s: s[-1].__setitem__("slot", "stop"),
        "slot.tail-position": lambda s: s[2].__setitem__("slot", "tail"),
        "slot.count-range": lambda s: (s.pop(), s.extend(_slots(13)[5:])),
        "slot.n-contiguous": lambda s: s[3].__setitem__("n", 9),
        # 시트 enum 의 값은 전부 이름 있는 슬롯이거나 other.allowed 라서, other-allowed 는 enum 밖 값에서만 함께 선다
        "slot.other-allowed": lambda s: s[2].__setitem__("slot", "bridge"),
    }
    for rule, fn in cases.items():
        rules = mutate(fn)
        if rule not in rules:
            pytest.fail(f"{rule} 이 잡히지 않았다: {rules}")
    five = rules_of(design_stage.check_slot_count({"slots": _slots(5)}, SHEET))
    thirteen = rules_of(design_stage.check_slot_count({"slots": _slots(13)}, SHEET))
    if "slot.count-range" not in five or "slot.count-range" not in thirteen:
        pytest.fail(f"5·13 슬롯이 범위 밖으로 잡히지 않는다: {five} {thirteen}")
    # landing 이 둘이면 landing-count 가, other-allowed 는 이름 있는 슬롯을 보지 않는다
    two_landing = rules_of(design_stage.check_slot_count({"slots": [*_slots(5), {"n": 6, "slot": "landing", "exhibit": {"material_ids": [], "point_en": "x"}, "figures": []}]}, SHEET))
    if "slot.landing-count" not in two_landing:
        pytest.fail(f"landing 2 가 잡히지 않는다: {two_landing}")


def test_sheet_binding_raising_tweet_max_admits_thirteen_slots(law) -> None:
    sheet_path = os.path.join(law, "contracts", "format-parameters.yaml")
    data = yaml.safe_load(open(sheet_path, encoding="utf-8"))
    data["parameters"]["tweet_count"]["value"]["max"] = 14
    with open(sheet_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
    sheet = design_stage.sheet_values(law)
    if sheet["tweet_count"]["max"] != 14:
        pytest.fail("법 사본의 시트가 읽히지 않는다")
    row = design_stage.check_slot_count({"slots": _slots(13)}, sheet)
    if row.status != "pass":
        pytest.fail(f"시트 max 14 인데 13 슬롯이 실패한다(코드 상수 의심): {rules_of(row)}")
    if design_stage.check_slot_count({"slots": _slots(13)}, SHEET).status != "fail":
        pytest.fail("정본 시트(12)에서는 13 슬롯이 실패해야 한다")


# ---------------------------------------------------------------------------
# ⑼ ⑽ targets-resolve · figure-budget
# ---------------------------------------------------------------------------


def test_targets_resolve_distinguishes_ghost_retracted_and_slot_locus(tmp_path) -> None:
    payload = good_payload()
    payload["transmission_targets"].append("M9999")
    row = design_stage.check_targets_resolve(payload, FROZEN)
    loci = [(f.rule, f.locus) for f in row.findings]
    if ("targets.unresolved", "transmission_targets[3]") not in loci:
        pytest.fail(f"유령 M9999 가 잡히지 않는다: {loci}")
    frozen = copy.deepcopy(FROZEN)
    target = payload["transmission_targets"][1]
    for item in frozen["items"]:
        if item["id"] == target:
            item["status"] = "retracted"
    row = design_stage.check_targets_resolve(good_payload(), frozen)
    if not any(f.rule == "targets.retracted-or-superseded" and f.locus == "transmission_targets[1]" for f in row.findings):
        pytest.fail(f"retracted 지목이 잡히지 않는다: {[(f.rule, f.locus) for f in row.findings]}")
    payload = good_payload()
    payload["slots"][2]["exhibit"]["material_ids"] = ["M8888"]
    row = design_stage.check_targets_resolve(payload, FROZEN)
    if not any(f.rule == "targets.unresolved" and f.locus == "slots[3].exhibit.material_ids[0]" for f in row.findings):
        pytest.fail(f"slots 좌표의 유령이 갈라 잡히지 않는다: {[(f.rule, f.locus) for f in row.findings]}")
    if design_stage.check_targets_resolve(good_payload(), FROZEN).status != "pass":
        pytest.fail("기준 판이 통과하지 않는다")


def test_figure_budget_rules_and_resolution_source(tmp_path) -> None:
    absent = os.path.join(str(tmp_path), "30-figures", "assets", "manifest.json")
    base = design_stage.check_figure_budget(good_payload(), FROZEN, SHEET, manifest_path=absent)
    if base.status != "pass" or base.extras["resolution_source"] != "frozen-figures":
        pytest.fail(f"기준 판이 통과하지 않거나 해소 원천이 다르다: {rules_of(base)} {base.extras}")
    five = good_payload()
    five["slots"][1]["figures"] = FIGS[:5]
    five["figure_plan"][1]["figures"] = FIGS[:5]
    if "figure.per-tweet-max" not in rules_of(design_stage.check_figure_budget(five, FROZEN, SHEET, manifest_path=absent)):
        pytest.fail("트윗 하나에 도면 5 가 잡히지 않는다")
    ghost = good_payload()
    ghost["slots"][1]["figures"] = ["FIG-99"]
    ghost["figure_plan"][1]["figures"] = ["FIG-99"]
    if "figure.unresolved" not in rules_of(design_stage.check_figure_budget(ghost, FROZEN, SHEET, manifest_path=absent)):
        pytest.fail("유령 FIG-99 가 잡히지 않는다")
    skew = good_payload()
    skew["figure_plan"][1]["figures"] = [FIGS[5]]
    rules = rules_of(design_stage.check_figure_budget(skew, FROZEN, SHEET, manifest_path=absent))
    if "figure.plan-slot-parity" not in rules:
        pytest.fail(f"figure_plan ↔ slots 불일치가 잡히지 않는다: {rules}")
    dropped = good_payload()
    dropped["figure_plan"].pop()
    if "figure.plan-tweet-set" not in rules_of(design_stage.check_figure_budget(dropped, FROZEN, SHEET, manifest_path=absent)):
        pytest.fail("figure_plan 트윗 집합 불일치가 잡히지 않는다")
    hook = good_payload()
    hook["hook"]["figure"] = FIGS[1]
    if "figure.hook-in-t1" not in rules_of(design_stage.check_figure_budget(hook, FROZEN, SHEET, manifest_path=absent)):
        pytest.fail("훅 도면이 T1 밖인데 잡히지 않는다")
    # 매니페스트 합성 — 해소 원천이 바뀌고, 매니페스트에 없는 도면은 유령이 된다
    os.makedirs(os.path.dirname(absent), exist_ok=True)
    json.dump({"items": [{"id": FIGS[0], "edit_class": "crop-only", "publishable": False}]}, open(absent, "w", encoding="utf-8"))
    row = design_stage.check_figure_budget(good_payload(), FROZEN, SHEET, manifest_path=absent)
    if row.extras["resolution_source"] != "assets-manifest" or "figure.unresolved" not in rules_of(row):
        pytest.fail(f"매니페스트 해소가 다르다: {row.extras} {rules_of(row)}")


# ---------------------------------------------------------------------------
# ⑾ spec-digest
# ---------------------------------------------------------------------------


def test_spec_digest_entry_mismatch_is_environment_error_and_runner_values_match(law, run_root) -> None:
    meta_path = os.path.join(run_root, "run.yaml")
    meta = yaml.safe_load(open(meta_path, encoding="utf-8"))
    original = meta["frozen"][0]["spec_digest"]
    meta["frozen"][0]["spec_digest"] = "sha256:" + "0" * 64
    yaml.safe_dump(meta, open(meta_path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    with pytest.raises(StageEnvironmentError, match="design 진입 지문 불일치"):
        run_design(run_root, law)
    meta["frozen"][0]["spec_digest"] = original
    yaml.safe_dump(meta, open(meta_path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    run_design(run_root, law)
    respond(run_root, LANE_ID, good_payload())
    outcome = run_design(run_root, law)
    if outcome["status"] != "ok":
        pytest.fail(f"왕복이 ok 가 아니다: {outcome['status']} {[rules_of(r) for r in outcome['rows']]}")
    blueprint = json.load(open(os.path.join(run_root, "20-design", "blueprint.json"), encoding="utf-8"))
    frozen_path = os.path.join(run_root, "15-frozen", "material-spec.v1.json")
    if blueprint["spec_digest"] != sha256_file(frozen_path) or blueprint["spec_version"] != 1:
        pytest.fail("러너가 기입한 spec_digest·spec_version 이 동결본 실측과 다르다")
    row = design_stage.check_spec_digest(dict(blueprint, spec_digest="sha256:" + "1" * 64), spec_version=1,
                                         spec_digest=blueprint["spec_digest"], frozen_path=frozen_path)
    if row.status != "fail":
        pytest.fail("spec_digest 불일치가 검사에서 잡히지 않는다")


# ---------------------------------------------------------------------------
# ⑿ 러너 왕복 · 재진입
# ---------------------------------------------------------------------------


def test_runner_round_trip_writes_outputs_and_is_reentrant(law, run_root) -> None:
    first = run_design(run_root, law)
    if first["status"] != "pending":
        pytest.fail("첫 진입이 pending 이 아니다")
    respond(run_root, LANE_ID, good_payload())
    outcome = run_design(run_root, law)
    if outcome["status"] != "ok":
        pytest.fail(f"ok 가 아니다: {outcome['status']} · {[(r.check_id, rules_of(r)) for r in outcome['rows']]}")
    ids = [row.check_id for row in outcome["rows"]]
    if ids != ["design.input-digest", "design.schema", "design.spec-digest", "design.anchors-adjudicated-only",
               "design.targets-resolve", "design.slot-count", "design.figure-budget"]:
        pytest.fail(f"판정 행 순서가 다르다: {ids}")
    design = os.path.join(run_root, "20-design")
    for name in ("blueprint.json", "blueprint.md", "design-report.json", "anchors-provided.json"):
        if not os.path.isfile(os.path.join(design, name)):
            pytest.fail(f"{name} 이 없다")
    blueprint = json.load(open(os.path.join(design, "blueprint.json"), encoding="utf-8"))
    schema = design_stage.load_blueprint_schema(law)
    if list(Draft202012Validator(schema).iter_errors(blueprint)):
        pytest.fail("쓴 블루프린트가 스키마를 위반한다")
    if blueprint["lane"] != {"model": "claude-fable-5-1", "effort": "high", "lane_id": LANE_ID} or blueprint["law_commit"] != design_stage.law_commit_of(law):
        pytest.fail(f"러너 기입 lane·law_commit 이 다르다: {blueprint['lane']} {blueprint['law_commit']}")
    report = json.load(open(os.path.join(design, "design-report.json"), encoding="utf-8"))
    row_schema = json.load(open(os.path.join(REPO, "contracts", "schemas", "verdict-check-row.schema.json"), encoding="utf-8"))
    for row in report["rows"]:
        if list(Draft202012Validator(row_schema).iter_errors(row)):
            pytest.fail(f"판정 행이 verdict-check-row/v0 를 위반한다: {row}")
    if report["status"] != "ok" or report["lane"]["mismatch"] is not False or report["lane_id"] != LANE_ID:
        pytest.fail(f"design-report 가 다르다: {report['status']} {report['lane']}")
    md = open(os.path.join(design, "blueprint.md"), encoding="utf-8").read()
    if "도면 자산층 부재" not in md or "format.stop-shape" not in md or "| T1 | `hook` |" not in md or "design.slot-count" not in md:
        pytest.fail("blueprint.md 에 표지·슬롯 표·판정 행이 없다")
    if FROZEN["items"][0]["label_en"] not in md:
        pytest.fail("blueprint.md 에 재료의 EN 값이 없다")
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    if meta["numeric_whitelist"] != [{"pattern": "^\\d{1,2}/\\d{1,2}$", "rationale": "thread ordinal n/N", "added_by": "run-discretion", "approved_in": None}]:
        pytest.fail(f"run.yaml#numeric_whitelist 추기가 다르다: {meta['numeric_whitelist']}")
    frozen_dir_before = sorted(os.listdir(os.path.join(run_root, "15-frozen")))
    before = open(os.path.join(design, "blueprint.md"), encoding="utf-8").read()
    again = run_design(run_root, law)
    if again["status"] != "ok" or sorted(os.listdir(os.path.join(run_root, "20-design", "lanes", "design", "blueprint"))) != ["batch-0"]:
        pytest.fail("재진입이 ok 가 아니거나 새 좌표를 만들었다")
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    if len(meta["numeric_whitelist"]) != 1 or open(os.path.join(design, "blueprint.md"), encoding="utf-8").read() != before:
        pytest.fail("재진입이 whitelist 를 중복 추기했거나 렌더가 비결정적이다")
    if sorted(os.listdir(os.path.join(run_root, "15-frozen"))) != frozen_dir_before:
        pytest.fail("러너가 15-frozen/ 에 썼다")


# ---------------------------------------------------------------------------
# ⒀ ⒁ ⒂ retry · 상신 · 종료선
# ---------------------------------------------------------------------------


def test_retry_once_then_escalate_and_halt_on_reentry(law, run_root) -> None:
    bad = good_payload()
    bad["slots"][1]["slot"] = "hook"
    run_design(run_root, law)
    respond(run_root, LANE_ID, bad)
    outcome = run_design(run_root, law)
    if outcome["status"] != "pending" or outcome["pending"] != [RETRY_LANE_ID]:
        pytest.fail(f"retry(1) 요청이 생기지 않았다: {outcome['status']} {outcome['pending']}")
    retry_md = open(os.path.join(run_root, "20-design", "lanes", *RETRY_LANE_ID.split("/"), "request.md"), encoding="utf-8").read()
    if "## 재시도 — 직전 판의 결함" not in retry_md or "slot.hook-count" not in retry_md or "| rule | locus | found | expected | message |" not in retry_md:
        pytest.fail("재시도 요청서에 결함 표가 없다")
    respond(run_root, RETRY_LANE_ID, bad)
    outcome = run_design(run_root, law)
    if outcome["status"] != "escalate":
        pytest.fail(f"두 번째 실패가 escalate 가 아니다: {outcome['status']}")
    escalation = json.load(open(os.path.join(run_root, "20-design", "escalation.json"), encoding="utf-8"))
    if escalation["lane_id"] != RETRY_LANE_ID or not escalation["rows"] or not any(f["rule"] == "slot.hook-count" for f in escalation["findings"]):
        pytest.fail(f"escalation.json 에 판정 행이 없다: {escalation.keys()}")
    if os.path.isfile(os.path.join(run_root, "20-design", "blueprint.json")):
        pytest.fail("실패한 판이 확정되었다")
    with pytest.raises(StageHaltError, match="상신 미처분"):
        run_design(run_root, law)


def test_lane_escalation_bypasses_checks(law, run_root) -> None:
    payload = good_payload()
    payload["escalation"] = {"reason": "exhibit-overflow", "note_kr": "강한 전시물 15"}
    payload["overflow_proposal"] = {"proposal": "split-series", "rationale_kr": "시리즈 둘"}
    payload["slots"][1]["slot"] = "hook"  # 검사가 돌았다면 잡혔을 결함 — 상신은 검사 앞이다
    run_design(run_root, law)
    respond(run_root, LANE_ID, payload)
    outcome = run_design(run_root, law)
    if outcome["status"] != "escalate" or outcome["reason_label"] != "exhibit-overflow" or len(outcome["rows"]) != 1:
        pytest.fail(f"상신이 검사 없이 escalate 로 서지 않는다: {outcome['status']} {outcome['reason_label']} {len(outcome['rows'])}")
    escalation = json.load(open(os.path.join(run_root, "20-design", "escalation.json"), encoding="utf-8"))
    if escalation["overflow_proposal"] != payload["overflow_proposal"] or escalation["reason"] != "exhibit-overflow":
        pytest.fail("escalation.json 에 overflow_proposal 이 없다")


def test_partial_until_before_design_halts(law, tmp_path) -> None:
    run_root = make_run(str(tmp_path), partial_until="freeze")
    with pytest.raises(StageHaltError, match="종료선"):
        run_design(run_root, law)
    if os.path.exists(os.path.join(run_root, "20-design")):
        pytest.fail("종료선 앞인데 20-design/ 을 만들었다")


def test_halt_checks_are_immediate_no_retry(law, run_root) -> None:
    run_design(run_root, law)
    provided = os.path.join(run_root, "20-design", "anchors-provided.json")
    contract = load_stage_contract("design", law)
    row = design_stage.check_anchors_adjudicated_only(provided)
    row.add("design.anchors-adjudicated-only", "x", "provisional", "active", "m")
    action, _ = design_stage.decide(contract, [row], 0)
    if action != "halt":
        pytest.fail(f"anchors 실패가 halt 가 아니다: {action}")
    retry_row = design_stage.check_slot_count({"slots": _slots(5)}, SHEET)
    if design_stage.decide(contract, [retry_row], 0)[0] != "retry" or design_stage.decide(contract, [retry_row], 1)[0] != "escalate":
        pytest.fail("slot-count 가 retry(1) → escalate 로 처분되지 않는다")


# ---------------------------------------------------------------------------
# ⒃ ⒄ 구동기 — extend · design · seal · help
# ---------------------------------------------------------------------------


class DesignStub:
    """`claude -p` 의 json 출력 흉내 — 설계 좌표 하나에 payload 를 낸다."""

    def __init__(self, payload: dict, *, model_override: str | None = None):
        self.payload = payload
        self.model_override = model_override
        self.calls: list[list[str]] = []

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        digest = next(line for line in text.split("\n") if line.startswith("| 입력 지문 | `")).split("`")[1]
        observed = self.model_override or argv[argv.index("--model") + 1]
        body = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "duration_ms": 3,
                "total_cost_usd": 0.0, "session_id": "stub",
                "structured_output": {"lane_id": lane_id, "model": "self", "effort": "self", "input_digest": digest, "payload": self.payload},
                "modelUsage": {observed: {"inputTokens": 1, "outputTokens": 9}}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 3)


def _drive(law: str, run_root: str, evidence: str, *argv: str, executor=None, dry_run: bool = False) -> tuple[int, list[str]]:
    lines: list[str] = []
    head = ["--repo", law, "--run-root", run_root, "--evidence-dir", evidence]
    if dry_run:
        head.append("--dry-run")
    return drv.main([*head, *argv], executor=executor, out=lines.append), lines


def test_driver_extend_then_design_then_seal(law, tmp_path) -> None:
    run_root = make_run(str(tmp_path), partial_until="freeze")
    evidence = os.path.join(str(tmp_path), "evidence")
    quote = os.path.join(str(tmp_path), "quote.txt")
    open(quote, "w", encoding="utf-8").write("C. 이 특허로 한번 도슨트 글까지 가보자\n")
    # 종료선 앞 — design 은 13
    code, _ = _drive(law, run_root, evidence, "design", RUN_ID)
    if code != drv.EXIT_TERMINAL_FAIL:
        pytest.fail(f"종료선 앞 design 이 13 이 아니다: {code}")
    # --until 이 뒤가 아니다 → 2
    code, _ = _drive(law, run_root, evidence, "extend", RUN_ID, "--quote-file", quote, "--until", "read")
    if code != drv.EXIT_USAGE:
        pytest.fail(f"--until read 가 2 가 아니다: {code}")
    # 법 트리 더러움 → 2
    open(os.path.join(law, "contracts", "dirty.txt"), "w").write("x")
    code, _ = _drive(law, run_root, evidence, "extend", RUN_ID, "--quote-file", quote, "--until", "gate")
    if code != drv.EXIT_USAGE:
        pytest.fail(f"더러운 법 트리가 2 가 아니다: {code}")
    os.remove(os.path.join(law, "contracts", "dirty.txt"))
    code, lines = _drive(law, run_root, evidence, "extend", RUN_ID, "--quote-file", quote, "--until", "gate",
                         "--ruling", "T64", "--decided-at", "2026-09-13T12:00:00Z")
    if code != drv.EXIT_OK:
        pytest.fail(f"extend 실패: {code} {lines}")
    envelope_path = os.path.join(run_root, "15-frozen", "extension-v1.md")
    envelope = freeze_stage.parse_envelope(open(envelope_path, encoding="utf-8").read())
    schema = json.load(open(os.path.join(REPO, "contracts", "schemas", "extension-envelope.schema.json"), encoding="utf-8"))
    if list(Draft202012Validator(schema).iter_errors(envelope)):
        pytest.fail("연장 봉투가 스키마를 위반한다")
    if envelope["from"] != "freeze" or envelope["to"] != "gate" or envelope["rulings"] != ["T64"] or envelope["engine"]["commit_at_start"] != "e" * 40:
        pytest.fail(f"봉투 필드가 다르다: {envelope}")
    if envelope["owner_quote"] != "C. 이 특허로 한번 도슨트 글까지 가보자\n":
        pytest.fail("육성 원문이 그대로가 아니다")
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    if meta["partial_until"] != "gate" or len(meta["extensions"]) != 1 or meta["extensions"][0]["path"] != "15-frozen/extension-v1.md":
        pytest.fail(f"run.yaml 이 연장을 반영하지 않았다: {meta.get('partial_until')} {meta.get('extensions')}")
    # dry-run 은 아무것도 쓰지 않는다
    snapshot = {os.path.join(d, f) for d, _, fs in os.walk(str(tmp_path)) for f in fs if ".git" not in d}
    code, lines = _drive(law, run_root, evidence, "design", RUN_ID, dry_run=True)
    after = {os.path.join(d, f) for d, _, fs in os.walk(str(tmp_path)) for f in fs if ".git" not in d}
    if code != drv.EXIT_OK or after != snapshot or not lines or not lines[0].startswith("[dry-run]"):
        pytest.fail(f"dry-run 이 파일을 썼거나 출력이 다르다: {code} {lines}")
    # 스텁 관측 모델이 요청과 다르면 14 · 응답은 관측값으로 쓴다
    wrong = DesignStub(good_payload(), model_override="claude-opus-5")
    code, _ = _drive(law, run_root, evidence, "design", RUN_ID, executor=wrong)
    if code != drv.EXIT_UNDECIDABLE:
        pytest.fail(f"첫 좌표 관측 모델 불일치가 14 가 아니다: {code}")
    # 되감기 — 응답·영수증을 지우고 정상 스텁으로
    shutil.rmtree(os.path.join(run_root, "20-design", "lanes"))
    shutil.rmtree(evidence)
    stub = DesignStub(good_payload())
    code, lines = _drive(law, run_root, evidence, "design", RUN_ID, executor=stub)
    if code != drv.EXIT_OK:
        pytest.fail(f"design 이 0 이 아니다: {code} {lines}")
    argv = stub.calls[0]
    if argv[argv.index("--model") + 1] != "claude-fable-5-1" or argv[argv.index("--effort") + 1] != "high":
        pytest.fail(f"레인 명령줄 좌석이 다르다: {argv}")
    receipt = json.load(open(os.path.join(evidence, "calls", "design__blueprint__batch-0.json"), encoding="utf-8"))
    if receipt["requested"] != {"model": "fable-5.1", "effort": "high", "api_id": "claude-fable-5-1"} or receipt["observed"]["main_model"] != "claude-fable-5-1":
        pytest.fail(f"영수증이 다르다: {receipt['requested']} {receipt['observed']}")
    if not os.path.isfile(os.path.join(run_root, "20-design", "blueprint.json")):
        pytest.fail("구동기 design 뒤 blueprint.json 이 없다")
    code, _ = _drive(law, run_root, evidence, "design", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 1:
        pytest.fail("design 재진입이 다시 호출했다")
    code, lines = _drive(law, run_root, evidence, "lanes", RUN_ID)
    if code != drv.EXIT_OK or not any("design/blueprint/batch-0" in line and line.startswith("완료") for line in lines):
        pytest.fail(f"lanes 가 설계 좌표를 보이지 않는다: {lines}")
    code, _ = _drive(law, run_root, evidence, "seal", RUN_ID)
    manifest = open(os.path.join(evidence, "MANIFEST-sha256.txt"), encoding="utf-8").read().splitlines()
    rels = [line.split("  ", 1)[1] for line in manifest]
    if code != drv.EXIT_OK or not any(rel.endswith("20-design/blueprint.json") for rel in rels) or not any(rel.endswith("15-frozen/extension-v1.md") for rel in rels):
        pytest.fail(f"MANIFEST 에 설계 산출·연장 봉투가 없다: {rels}")
    # 두 번째 연장은 v2 로 · 뒤가 아니면 2
    code, _ = _drive(law, run_root, evidence, "extend", RUN_ID, "--quote-file", quote, "--until", "design")
    if code != drv.EXIT_USAGE:
        pytest.fail("gate → design 이 2 가 아니다")


def test_help_lists_twelve_commands_including_extend_and_design() -> None:
    parser = drv.build_parser()
    listed = tuple(parser._subparsers._group_actions[0].choices)  # noqa: SLF001
    if listed != drv.COMMANDS or len(listed) != 12 or listed[-3:] != ("extend", "design", "compose"):
        pytest.fail(f"명령 12 가 아니다: {listed}")
