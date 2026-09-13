# -*- coding: utf-8 -*-
"""M32 — `compose` 스테이지 실물화(재정 2026-09-13 T64 ③·④) + 구동기 `compose`.

실제 `claude` 는 부르지 않는다(스텁 실행기 · 파일 어댑터에 시험이 응답을 쓴다). 런 -3 동결본은 읽기만
하고 tmp 로 복사한다. 초안 표본 = `ledgers/regression/golden/rc-0001-numberless/thread.annotated.md` 를 읽어
프런트매터만 픽스처 값으로 바꾼 것이다.
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

from engine.annotation import parse as annotation  # noqa: E402
from engine.lanes.contract import LaneContractError, LaneRequest  # noqa: E402
from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.pens import lint, registry  # noqa: E402
from engine.stages import StageHaltError, sha256_file  # noqa: E402
from engine.stages import compose as compose_stage  # noqa: E402
from engine.stages import design as design_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

RUN_ID = "gdm-wo2026128750a1-agent-memory-3"
FROZEN_FIXTURE = os.path.join(REPO, "runs", RUN_ID, "15-frozen", "material-spec.v1.json")
GOLDEN_THREAD = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless", "thread.annotated.md")
LAW_TREES = ("contracts", "reader")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"))
TEMPLATE = os.path.join(REPO, "engine", "pens", "prompt-template.md")
PENS = registry.pens(REPO)
VARIANTS = [pen["variant"] for pen in PENS]
EFFORTS = {pen["variant"]: pen["effort"] for pen in PENS}
SLOT_ENUM = compose_stage.sheet_values(REPO)["slot_enum"]


# ---------------------------------------------------------------------------
# 픽스처
# ---------------------------------------------------------------------------


def _git(cwd: str, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        pytest.fail(f"git {' '.join(args)} 실패: {proc.stderr}")
    return proc.stdout.strip()


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


def frozen_spec() -> dict:
    with open(FROZEN_FIXTURE, encoding="utf-8") as handle:
        return json.load(handle)


FROZEN = frozen_spec()
FIGS = [figure["id"] for figure in FROZEN["figures"]]
COMPONENTS = [item["id"] for item in FROZEN["items"] if item["kind"] == "component"]


def blueprint_for(spec_digest: str) -> dict:
    """①이 만든 `blueprint/v0` 를 통과하는 합성 블루프린트(6 슬롯)."""
    slots = [
        {"n": 1, "slot": "hook", "exhibit": {"material_ids": [COMPONENTS[0]], "point_en": "Ask the question."}, "figures": [FIGS[0]]},
        {"n": 2, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[1]], "point_en": "One component."}, "figures": [FIGS[1]]},
        {"n": 3, "slot": "stop", "exhibit": {"material_ids": [COMPONENTS[2]], "point_en": "Another component."}, "figures": [FIGS[2]]},
        {"n": 4, "slot": "pivot", "exhibit": {"material_ids": [COMPONENTS[3]], "point_en": "The decisive evidence."}, "figures": [FIGS[3]]},
        {"n": 5, "slot": "landing", "exhibit": {"material_ids": [COMPONENTS[0], COMPONENTS[1]], "point_en": "Relief."}, "figures": []},
        {"n": 6, "slot": "tail", "exhibit": {"material_ids": [], "point_en": "Notes link."}, "figures": []},
    ]
    return {
        "schema": "blueprint/v0", "run_id": RUN_ID, "spec_version": 1, "spec_digest": spec_digest,
        "lane": {"model": "claude-fable-5-1", "effort": "high", "lane_id": "design/blueprint/batch-0"},
        "law_commit": "a" * 40,
        "hook": {"question_en": "Is the moat real?", "figure": FIGS[0], "thesis_en": "It is.", "rationale_kr": "최강 도면."},
        "slots": slots,
        "transmission_targets": [COMPONENTS[0], COMPONENTS[1], COMPONENTS[2]],
        "new_terms": [{"term_en": "datastore", "tweet": 2, "gloss_en": "where memories live"}],
        "figure_plan": [{"tweet": slot["n"], "figures": list(slot["figures"]), "intent_kr": "지정만"} for slot in slots],
        "numeric_whitelist": [{"pattern": "^\\d{1,2}/\\d{1,2}$", "rationale": "thread ordinal n/N"}],
        "overflow_proposal": None,
        "escalation": None,
    }


def make_run(root: str, *, partial_until: str = "gate") -> str:
    run_root = os.path.join(root, "runs", RUN_ID)
    frozen_dir = os.path.join(run_root, "15-frozen")
    os.makedirs(frozen_dir, exist_ok=True)
    frozen = os.path.join(frozen_dir, "material-spec.v1.json")
    shutil.copyfile(FROZEN_FIXTURE, frozen)
    os.chmod(frozen, 0o444)
    digest = sha256_file(frozen)
    meta = {
        "schema": "run/v0", "run_id": RUN_ID, "status": "active", "run_kind": "partial",
        "partial_until": partial_until, "engine": {"commit": "e" * 40, "worktree": None},
        "numeric_whitelist": [],
        "frozen": [{"spec_version": 1, "path": "15-frozen/material-spec.v1.json", "spec_digest": digest}],
    }
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    os.makedirs(os.path.join(run_root, "20-design"), exist_ok=True)
    with open(os.path.join(run_root, "20-design", "blueprint.json"), "w", encoding="utf-8") as handle:
        json.dump(blueprint_for(digest), handle, ensure_ascii=False, indent=2, sort_keys=True)
    return run_root


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(str(tmp_path))


def golden_body() -> str:
    text = open(GOLDEN_THREAD, encoding="utf-8").read()
    return text.split("---\n", 2)[2]


def frontmatter_for(variant: str, *, digest: str, effort: str | None = None, run_id: str = RUN_ID,
                    spec_version: int = 1, extra: str = "") -> str:
    effort = effort or EFFORTS[variant]
    return (
        f"---\nrun_id: {run_id}\nvariant: {variant}\n"
        f"pen: {{ vendor: anthropic, model: opus-5, effort: {effort} }}\n"
        f"spec_version: {spec_version}\nspec_digest: {digest}\n{extra}---\n"
    )


def draft_for(variant: str, run_root: str, **kwargs) -> str:
    digest = run_digest(run_root)
    return frontmatter_for(variant, digest=kwargs.pop("digest", digest), **kwargs) + golden_body()


def run_digest(run_root: str) -> str:
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    return meta["frozen"][0]["spec_digest"]


def lane_dir(run_root: str, lane_id: str) -> str:
    return os.path.join(run_root, "40-compose", "lanes", *lane_id.split("/"))


def respond(run_root: str, lane_id: str, payload: dict, *, model: str = "claude-opus-5", effort: str | None = None) -> str:
    directory = lane_dir(run_root, lane_id)
    request = json.load(open(os.path.join(directory, "request.json"), encoding="utf-8"))
    effort = effort or request["effort"]
    path = os.path.join(directory, "response.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"lane_id": lane_id, "model": model, "effort": effort, "input_digest": request["input_digest"],
                   "payload": payload}, handle, ensure_ascii=False)
    return path


def respond_draft(run_root: str, variant: str, *, attempt: int = 0, text: str | None = None, **kwargs) -> str:
    return respond(run_root, compose_stage.lane_id_for(variant, attempt),
                   {"thread_annotated_md": text or draft_for(variant, run_root)}, **kwargs)


def run_compose(run_root: str, law: str, **kwargs) -> dict:
    return compose_stage.run(run_root=run_root, repo=law, **kwargs)


def rows_by(outcome: dict, check_id: str, variant: str | None = None):
    return [row for row in outcome["rows"] if row.check_id == check_id and (variant is None or row.extras.get("variant") == variant)]


def tournament(run_root: str) -> list[dict]:
    path = os.path.join(run_root, "40-compose", "tournament-rows.jsonl")
    if not os.path.isfile(path):
        return []
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def read_json(path: str):
    return json.load(open(path, encoding="utf-8"))


# ---------------------------------------------------------------------------
# ⑴ 계약 · 경로
# ---------------------------------------------------------------------------


def test_contract_loads_and_paths_declare_variant_slot(law) -> None:
    contract = load_stage_contract("compose", law)
    ids = [row["id"] for row in contract["checks_before_exit"]]
    if contract["schema"] != "stage-contract/v0" or contract["id"] != "compose":
        pytest.fail("compose.yaml 골격이 다르다")
    if ids != ["compose.lane-verified", "compose.spec-digest", "compose.annotation-syntax", "compose.frontmatter"]:
        pytest.fail(f"종료 검사 4 가 다르다: {ids}")
    entry = [row["id"] for row in contract["checks_on_entry"]]
    if entry != ["compose.input-digest", "compose.prompt-lint"]:
        pytest.fail(f"진입 검사가 다르다: {entry}")
    if len(contract["failure"]) != 7:
        pytest.fail(f"실패표가 6+1 행이 아니다: {len(contract['failure'])}")
    if [pen["effort"] for pen in registry.pens(law)] != ["high", "xhigh", "max"] or registry.comparison_axis(law) != "effort":
        pytest.fail("펜 배정이 R10 사다리가 아니다")
    paths = RunPaths("/nonexistent/run", law)
    if "compose" not in paths.STAGES or paths.STAGES.index("compose") != len(paths.STAGES) - 2:
        pytest.fail(f"STAGES 에 compose 가 없거나 자리가 다르다(gate 가 뒤에 온다 — T64 집행 ③): {paths.STAGES}")
    if "<variant>" not in paths.declared("thread.annotated.md"):
        pytest.fail("thread.annotated.md 선언에 <variant> 자리가 없다")
    threads = {paths.thread_annotated(variant) for variant in VARIANTS}
    if len(threads) != 3 or not all(path.endswith(f"40-compose/{v}/thread.annotated.md") for v, path in zip(VARIANTS, sorted(threads))):
        pytest.fail(f"세 변주 경로가 다르지 않다: {threads}")
    if not paths.material_defect("v2").endswith("40-compose/v2/material-defect.md"):
        pytest.fail("material_defect 경로가 다르다")
    if not paths.compose_lanes_dir.endswith("40-compose/lanes") or not paths.compose_report_json.endswith("40-compose/compose-report.json"):
        pytest.fail("compose_lanes_dir·compose_report_json 이 다르다")
    if not paths.tournament_rows_jsonl.endswith("40-compose/tournament-rows.jsonl"):
        pytest.fail("tournament_rows_jsonl 경로가 다르다")
    for basename in ("run.yaml", "blueprint.json", "material-spec.v<N>.json"):
        paths.declared(basename)


def test_blueprint_fixture_passes_blueprint_schema(run_root) -> None:
    schema = design_stage.load_blueprint_schema(REPO)
    blueprint = read_json(os.path.join(run_root, "20-design", "blueprint.json"))
    errors = list(Draft202012Validator(schema).iter_errors(blueprint))
    if errors:
        pytest.fail(f"합성 블루프린트가 blueprint/v0 를 위반한다: {errors[0].message}")


# ---------------------------------------------------------------------------
# ⑵ ⑶ 파서
# ---------------------------------------------------------------------------


def test_parser_golden_sample_parses_clean() -> None:
    text = open(GOLDEN_THREAD, encoding="utf-8").read()
    parsed = annotation.parse(text, slot_enum=SLOT_ENUM)
    if parsed.errors or len(parsed.tweets) != 6 or parsed.sentence_count != 12:
        pytest.fail(f"golden 표본이 깨끗하게 파싱되지 않는다: {parsed.errors} {len(parsed.tweets)} {parsed.sentence_count}")
    raw = text.split("---\n", 2)[1].rstrip("\n")
    if parsed.frontmatter_raw != raw:
        pytest.fail("frontmatter_raw 가 --- 사이 원문과 다르다")
    if parsed.frontmatter["pen"] != {"vendor": "anthropic", "model": "opus-5", "effort": "max"}:
        pytest.fail("프런트매터 pen 이 파싱되지 않았다")
    hook = parsed.tweets[0]
    if hook.slot != "hook" or hook.figures != ("fig-01",) or hook.sentences[0].narrative or hook.sentences[0].citations != ():
        # 첫 문장은 [narrative]
        if not hook.sentences[0].narrative:
            pytest.fail("T1/S1 이 narrative 로 읽히지 않았다")
    if parsed.tweets[0].sentences[1].citations != ("M7",) or parsed.tweets[0].sentences[1].text.endswith("]"):
        pytest.fail("인용·태그 제거 텍스트가 다르다")


def _golden_lines() -> list[str]:
    return open(GOLDEN_THREAD, encoding="utf-8").read().split("\n")


def _mutate(fn) -> list[str]:
    lines = _golden_lines()
    fn(lines)
    return "\n".join(lines)


def _errors(text: str) -> list[tuple[str, str]]:
    return [(err.rule, err.locus) for err in annotation.parse(text, slot_enum=SLOT_ENUM).errors]


@pytest.mark.parametrize(
    "name, mutate, expected",
    [
        ("태그 없음", lambda ls: ls.__setitem__(10, ls[10].replace("[M7]", "")), ("annotation.missing-tag", "T1/S2")),
        ("태그 2", lambda ls: ls.__setitem__(10, ls[10] + "[M8]"), ("annotation.schema", "T1/S2")),
        ("태그 앞 공백", lambda ls: ls.__setitem__(10, ls[10].replace(".[M7]", ". [M7]")), ("annotation.schema", "T1/S2")),
        ("태그 내부 공백", lambda ls: ls.__setitem__(10, ls[10].replace("[M7]", "[M7, M8]")), ("annotation.schema", "T1/S2")),
        ("줄 중간 태그", lambda ls: ls.__setitem__(10, ls[10].replace("grit", "grit[M2]")), ("annotation.schema", "T1/S2")),
        ("헤더 번호 건너뜀", lambda ls: ls.__setitem__(12, ls[12].replace("## T2", "## T3")), ("annotation.schema", "T3")),
        ("슬롯 enum 밖", lambda ls: ls.__setitem__(12, ls[12].replace("slot: stop", "slot: bridge")), ("annotation.schema", "T2")),
        ("fig 문법", lambda ls: ls.__setitem__(12, ls[12].replace("fig: fig-02", "fig: FIG-2")), ("annotation.schema", "T2")),
        ("프런트매터 6키", lambda ls: ls.insert(6, "extra: 1"), ("annotation.schema", "frontmatter")),
        ("트윗 내부 빈 줄", lambda ls: ls.insert(10, ""), ("annotation.schema", "T1/S2")),
    ],
)
def test_parser_detects_each_violation_with_locus(name, mutate, expected) -> None:
    found = _errors(_mutate(mutate))
    if expected not in found:
        pytest.fail(f"{name}: {expected} 가 잡히지 않았다 — {found}")


def test_parser_collects_all_errors_instead_of_stopping() -> None:
    text = _mutate(lambda ls: (ls.__setitem__(10, ls[10].replace("[M7]", "")), ls.__setitem__(13, ls[13].replace("[M1]", ""))))
    found = _errors(text)
    if found != [("annotation.missing-tag", "T1/S2"), ("annotation.missing-tag", "T2/S1")]:
        pytest.fail(f"오류 2 개짜리 표본이 2 로 모이지 않는다: {found}")
    if annotation.TAG_RE.search("Sentence.[M3,M7]") is None or annotation.TAG_RE.search("Sentence.[M3, M7]") is not None:
        pytest.fail("TAG_RE 가 SPEC §3.2 태그식과 다르다")
    if annotation.HEADER_RE.match("## T1 {slot: hook, fig: none}") is None or annotation.HEADER_RE.match("## T1 {slot: hook,fig: none}") is not None:
        pytest.fail("HEADER_RE 가 콤마 뒤 공백 1칸을 강제하지 않는다")


# ---------------------------------------------------------------------------
# ⑷ 린트
# ---------------------------------------------------------------------------


def test_prompt_lint_template_and_instructions_clean_and_plants_caught(law, run_root) -> None:
    template = open(TEMPLATE, encoding="utf-8").read()
    if lint.lint_prompt(template, law):
        pytest.fail(f"템플릿이 린트를 통과하지 않는다: {lint.lint_prompt(template, law)}")
    outcome = run_compose(run_root, law)
    if outcome["status"] != "pending":
        pytest.fail(f"첫 진입이 pending 이 아니다: {outcome['status']}")
    rendered = open(os.path.join(lane_dir(run_root, "compose/v1/batch-0"), "request.md"), encoding="utf-8").read()
    if lint.lint_prompt(rendered, law):
        pytest.fail(f"렌더된 요청서(원천 조각 제외)가 린트를 통과하지 않는다: {lint.lint_prompt(rendered, law)}")
    rows = lint.lint_rows(lint.lint_target(rendered), law)
    if [row.ruleset for row in rows] != ["prompt-negation", "speech-acts+defect-catalog"] or any(row.check_id != "compose.prompt-lint" for row in rows):
        pytest.fail(f"판정 행 2 의 id·ruleset 이 다르다: {[(r.check_id, r.ruleset) for r in rows]}")
    if rows[0].ruleset_size != 1 or rows[1].extras["defect_catalog"] != {"ruleset_size": 0, "vacuous": "empty-ruleset"}:
        pytest.fail(f"ruleset 크기·카탈로그 공허 표기가 다르다: {rows[0].ruleset_size} {rows[1].extras}")
    planted = template + "\nYou should never mention this.\n"
    found = lint.lint_prompt(planted, law)
    if len(found) != 1 or found[0].rule != "prompt.negation" or found[0].found != "never":
        pytest.fail(f"never 를 심었는데 1 건이 아니다: {found}")
    acts = yaml.safe_load(open(os.path.join(law, "contracts", "lexicon", "speech-acts.yaml"), encoding="utf-8"))
    question = acts["predicates"][0]["classification_question"]
    found = lint.lint_prompt(template + "\n" + question + "\n", law)
    if len(found) != 1 or found[0].rule != "prompt.lexicon-literal":
        pytest.fail(f"화행 분류 질문을 심었는데 1 건이 아니다: {found}")
    # 원천 조각 절의 avoid 는 안 잡힌다 — 데이터다.
    with_avoid = rendered.replace("## 원천 조각\n", "## 원천 조각\n\navoid this phrase lives in the material\n", 1)
    if lint.lint_prompt(with_avoid, law):
        pytest.fail("원천 조각 절의 avoid 가 잡혔다")
    # 지시 블록에 심으면 잡힌다.
    with_never = rendered.replace("## 이 요청의 지시\n", "## 이 요청의 지시\n\nnever do that\n", 1)
    if len(lint.lint_prompt(with_never, law)) != 1:
        pytest.fail("지시 블록의 never 가 잡히지 않았다")


def test_prompt_lint_failure_halts_entry(law, run_root) -> None:
    path = os.path.join(law, "engine", "pens", "prompt-template.md")
    open(path, "a", encoding="utf-8").write("\nDo not cite anything.\n")
    with pytest.raises(StageHaltError, match="compose.prompt-lint"):
        run_compose(run_root, law)
    report = read_json(os.path.join(run_root, "40-compose", "compose-report.json"))
    if report["status"] != "halt" or not any(row["check_id"] == "compose.prompt-lint" and row["status"] == "fail" for row in report["rows"]):
        pytest.fail("린트 halt 가 보고에 남지 않았다")
    if os.path.isdir(os.path.join(run_root, "40-compose", "lanes", "compose")):
        pytest.fail("린트 halt 뒤에 요청서가 써졌다")


# ---------------------------------------------------------------------------
# ⑸ ⑥ 요청서 동일성 · must_not_read
# ---------------------------------------------------------------------------


def _sections(rendered: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = "head"
    for line in rendered.split("\n"):
        if line.startswith("## ") and not line.startswith("## 런 표지") and current != "instr-inner":
            current = line
        out[current] = out.get(current, "") + line + "\n"
    return out


def test_three_requests_differ_only_in_effort_and_variant_marker(law, run_root) -> None:
    run_compose(run_root, law)
    bodies = {}
    for variant in VARIANTS:
        directory = lane_dir(run_root, f"compose/{variant}/batch-0")
        request = read_json(os.path.join(directory, "request.json"))
        if request["model"] != "opus-5" or request["effort"] != EFFORTS[variant] or request["task"] != variant or request["read_run"] != "compose":
            pytest.fail(f"{variant} request.json 좌석이 다르다: {request['model']}/{request['effort']}/{request['task']}")
        bodies[variant] = open(os.path.join(directory, "request.md"), encoding="utf-8").read()

    def strip_marker(text: str, variant: str) -> str:
        lines = [line for line in text.split("\n")
                 if not line.startswith("| variant |") and not line.startswith("| pen |") and not line.startswith("| effort |")
                 and not line.startswith("| 입력 지문 |") and not line.startswith("| 작업 |") and not line.startswith("# 레인 요청 — ")]
        return "\n".join(lines)

    stripped = {variant: strip_marker(body, variant) for variant, body in bodies.items()}
    if len(set(stripped.values())) != 1:
        pytest.fail("세 요청서가 표지 줄을 빼고 바이트 동일하지 않다")
    if len({body for body in bodies.values()}) != 3:
        pytest.fail("세 요청서가 effort 표지로 구별되지 않는다")
    body = bodies["v1"]
    frozen_text = open(FROZEN_FIXTURE, encoding="utf-8").read().rstrip("\n")
    blueprint_text = open(os.path.join(run_root, "20-design", "blueprint.json"), encoding="utf-8").read().rstrip("\n")
    if frozen_text not in body or blueprint_text not in body:
        pytest.fail("동결본·블루프린트 전문이 요청서에 없다")
    for needle in ("# 펜 절차", "각 전시 스톱은 구성요소 하나를 다룬다", "| slot_enum |", "헤더 `fig` 는 전부 `none`", f"| run_id | `{RUN_ID}` |"):
        if needle not in body:
            pytest.fail(f"요청서에 {needle!r} 가 없다")
    outside = body.replace(frozen_text, "").replace(blueprint_text, "")
    for forbidden in ("00-source", "10-read", "speech-acts", "defect-catalog", "metrics.jsonl", "50-gate", "65-critique"):
        if forbidden in outside:
            pytest.fail(f"요청서(원천 조각 밖)에 must_not_read 문자열 {forbidden!r} 가 있다")
    # 어휘 고리 — compose 어휘는 READ 기본 LaneRequest 를 통과하지 않는다.
    fields = dict(lane_id="compose/v1/batch-0", read_run="compose", task="v1", model="opus-5", effort="high",
                  prompt_path="engine/pens/prompt-template.md", instructions="x", repo_root=REPO, response_schema={"type": "object"})
    compose_stage.ComposeLaneRequest(**fields)
    with pytest.raises(LaneContractError, match=r"어휘 위반\(소속\)"):
        LaneRequest(**fields)
    with pytest.raises(LaneContractError, match=r"어휘 위반\(소속\)"):
        compose_stage.ComposeLaneRequest(**dict(fields, lane_id="compose/v4/batch-0", task="v4"))
    if compose_stage.lane_id_for("v2", 1) != "compose/v2/retry-1/batch-0":
        pytest.fail("재시도 좌표 문법이 다르다")


# ---------------------------------------------------------------------------
# ⑦ 왕복 · 재진입
# ---------------------------------------------------------------------------


def test_round_trip_three_drafts_ok_and_reentry_idempotent(law, run_root) -> None:
    first = run_compose(run_root, law)
    if first["status"] != "pending" or first["pending"] != [f"compose/{v}/batch-0" for v in VARIANTS]:
        pytest.fail(f"첫 진입 pending 좌표가 다르다: {first['pending']}")
    meta = yaml.safe_load(open(os.path.join(run_root, "run.yaml"), encoding="utf-8"))
    if meta["pens"] != PENS or meta["comparison_axis"] != "effort":
        pytest.fail(f"run.yaml pens·comparison_axis 가 기입되지 않았다: {meta.get('pens')} {meta.get('comparison_axis')}")
    for variant in VARIANTS:
        respond_draft(run_root, variant)
    outcome = run_compose(run_root, law)
    if outcome["status"] != "ok" or {v: s["status"] for v, s in outcome["variants"].items()} != {v: "ok" for v in VARIANTS}:
        pytest.fail(f"셋 다 초안인데 ok 가 아니다: {outcome['status']} {outcome['variants']}")
    for variant in VARIANTS:
        path = os.path.join(run_root, "40-compose", variant, "thread.annotated.md")
        if open(path, encoding="utf-8").read() != draft_for(variant, run_root):
            pytest.fail(f"{variant} 확정본이 레인 바이트 그대로가 아니다")
    report = read_json(os.path.join(run_root, "40-compose", "compose-report.json"))
    if report["status"] != "ok" or report["pens"] != PENS or len(report["rows"]) != 1 + 6 + 12:
        pytest.fail(f"보고 행 수가 다르다(진입 1 + 린트 2×3 + 검사 4×3): {len(report['rows'])}")
    rows = tournament(run_root)
    if [row["variant"] for row in rows] != VARIANTS or any(row["outcome"] != "drafted" or row["comparison_axis"] != "effort" or row["taste_weight"] != "low" for row in rows):
        pytest.fail(f"토너먼트 행 3 이 다르다: {rows}")
    if rows[1]["pen"] != {"vendor": "anthropic", "model": "opus-5", "effort": "xhigh"} or rows[0]["spec_version"] != 1:
        pytest.fail(f"토너먼트 행의 pen·spec_version 이 다르다: {rows[1]}")
    before = {os.path.join(d, f): os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(os.path.join(run_root, "40-compose", "lanes")) for f in fs}
    again = run_compose(run_root, law)
    after = {os.path.join(d, f): os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(os.path.join(run_root, "40-compose", "lanes")) for f in fs}
    if again["status"] != "ok" or before != after or len(tournament(run_root)) != 3:
        pytest.fail("재진입이 요청서를 다시 썼거나 토너먼트 행이 중복됐다")
    lane_row = rows_by(outcome, "compose.lane-verified", "v3")[0]
    if lane_row.extras["effort_evidence"] != "requested-flag":
        pytest.fail("lane-verified 의 effort_evidence 가 requested-flag 가 아니다")


def test_draft_without_trailing_newline_gets_exactly_one(law, run_root) -> None:
    run_compose(run_root, law)
    for variant in VARIANTS:
        respond_draft(run_root, variant, text=draft_for(variant, run_root).rstrip("\n"))
    outcome = run_compose(run_root, law)
    if outcome["status"] != "ok":
        pytest.fail(f"끝 개행 없는 초안이 ok 가 아니다: {outcome['variants']}")
    text = open(os.path.join(run_root, "40-compose", "v1", "thread.annotated.md"), encoding="utf-8").read()
    if not text.endswith("]\n") or text.endswith("\n\n"):
        pytest.fail("끝 개행 정규화가 하나가 아니다")


# ---------------------------------------------------------------------------
# ⑧ ⑨ ⑩ halt 계열
# ---------------------------------------------------------------------------


def test_frontmatter_pen_effort_mismatch_halts(law, run_root) -> None:
    run_compose(run_root, law)
    respond_draft(run_root, "v1", text=draft_for("v1", run_root, effort="max"))
    respond_draft(run_root, "v2")
    respond_draft(run_root, "v3")
    outcome = run_compose(run_root, law)
    row = rows_by(outcome, "compose.frontmatter", "v1")[0]
    if row.status != "fail" or not any(f.rule == "frontmatter.pen" for f in row.findings):
        pytest.fail(f"pen.effort 불일치가 frontmatter fail 로 잡히지 않는다: {[f.rule for f in row.findings]}")
    if outcome["status"] != "halt" or outcome["variants"]["v1"]["status"] != "halt" or outcome["variants"]["v2"]["status"] != "ok":
        pytest.fail(f"halt 처분이 다르다: {outcome['status']} {outcome['variants']}")
    if os.path.isfile(os.path.join(run_root, "40-compose", "v1", "thread.annotated.md")):
        pytest.fail("halt 변주의 초안이 확정본으로 써졌다")


def test_spec_digest_mismatch_halts(law, run_root) -> None:
    run_compose(run_root, law)
    respond_draft(run_root, "v1")
    respond_draft(run_root, "v2", text=draft_for("v2", run_root, digest="sha256:" + "0" * 64))
    respond_draft(run_root, "v3")
    outcome = run_compose(run_root, law)
    row = rows_by(outcome, "compose.spec-digest", "v2")[0]
    if row.status != "fail" or outcome["status"] != "halt" or outcome["variants"]["v2"]["status"] != "halt":
        pytest.fail(f"spec_digest 불일치가 halt 가 아니다: {outcome['status']} {outcome['variants']}")


def test_lane_verified_model_mismatch_halts_only_that_variant(law, run_root) -> None:
    run_compose(run_root, law)
    respond_draft(run_root, "v1")
    respond_draft(run_root, "v2")
    respond_draft(run_root, "v3", model="claude-fable-5-1")
    outcome = run_compose(run_root, law)
    row = rows_by(outcome, "compose.lane-verified", "v3")[0]
    if row.status != "fail" or not any(f.rule == "lane.model" for f in row.findings):
        pytest.fail(f"모델 불일치가 lane-verified fail 이 아니다: {[f.rule for f in row.findings]}")
    if outcome["status"] != "halt" or outcome["variants"]["v3"]["status"] != "halt":
        pytest.fail(f"lane-verified 실패가 halt 가 아니다: {outcome['status']}")
    if outcome["variants"]["v1"]["status"] != "ok" or outcome["variants"]["v2"]["status"] != "ok":
        pytest.fail("다른 변주의 판정이 바뀌었다")
    # `claude-opus-5[1m]` 표기는 수용 집합 안이다(정직한 레인이 벌받지 않는다).
    shutil.rmtree(os.path.join(run_root, "40-compose"))
    run_compose(run_root, law)
    for variant in VARIANTS:
        respond_draft(run_root, variant, model="claude-opus-5[1m]")
    if run_compose(run_root, law)["status"] != "ok":
        pytest.fail("model_identity 별칭이 거부됐다")


# ---------------------------------------------------------------------------
# ⑪ 재시도 → escalate
# ---------------------------------------------------------------------------


def test_annotation_syntax_retries_twice_then_escalates_while_others_survive(law, run_root) -> None:
    run_compose(run_root, law)
    bad = draft_for("v2", run_root).replace(".[M7]", ".", 1)
    respond_draft(run_root, "v1")
    respond_draft(run_root, "v3")
    respond_draft(run_root, "v2", text=bad)
    outcome = run_compose(run_root, law)
    retry_1 = "compose/v2/retry-1/batch-0"
    if outcome["status"] != "pending" or outcome["pending"] != [retry_1]:
        pytest.fail(f"재시도 좌표가 대기로 나오지 않는다: {outcome['status']} {outcome['pending']}")
    request_md = open(os.path.join(lane_dir(run_root, retry_1), "request.md"), encoding="utf-8").read()
    if "## 재시도 — 직전 판의 결함" not in request_md or "annotation.missing-tag" not in request_md or "T1/S2" not in request_md:
        pytest.fail("재시도 요청서에 결함 표가 없다")
    if lint.lint_prompt(request_md, law):
        pytest.fail(f"재시도 요청서가 린트를 통과하지 않는다: {lint.lint_prompt(request_md, law)}")
    if os.path.isfile(os.path.join(run_root, "40-compose", "v1", "thread.annotated.md")):
        pytest.fail("v2 가 대기인데 v1 이 먼저 확정됐다(순서 효과)")
    respond_draft(run_root, "v2", attempt=1, text=bad)
    outcome = run_compose(run_root, law)
    if outcome["pending"] != ["compose/v2/retry-2/batch-0"]:
        pytest.fail(f"둘째 재시도가 나오지 않는다: {outcome['pending']}")
    respond_draft(run_root, "v2", attempt=2, text=bad)
    outcome = run_compose(run_root, law)
    if outcome["status"] != "ok" or outcome["variants"]["v2"]["status"] != "escalate":
        pytest.fail(f"3회째 실패가 escalate 가 아니거나 생존 2 인데 런이 멎었다: {outcome['status']} {outcome['variants']}")
    if outcome["variants"]["v1"]["status"] != "ok" or outcome["variants"]["v3"]["status"] != "ok":
        pytest.fail("v1·v3 가 ok 가 아니다")
    rows = tournament(run_root)
    if [row["variant"] for row in rows] != ["v1", "v3"]:
        pytest.fail(f"escalate 변주가 토너먼트에 올랐다: {rows}")
    if os.path.isfile(os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")):
        pytest.fail("escalate 변주의 초안이 확정본으로 써졌다")
    if compose_stage.decide(load_stage_contract("compose", law), rows_by(outcome, "compose.annotation-syntax", "v2"), 5) != "escalate":
        pytest.fail("decide 가 예산 밖에서 retry 를 낸다")


# ---------------------------------------------------------------------------
# ⑫ 반려서
# ---------------------------------------------------------------------------


def test_material_defect_writes_four_field_envelope_and_rejects_upstream(law, run_root) -> None:
    run_compose(run_root, law)
    respond_draft(run_root, "v1")
    respond_draft(run_root, "v2")
    defect = {"material_ids": [COMPONENTS[1], COMPONENTS[2]], "defect_kind": "unresolvable-grounding",
              "evidence": "M2 says X while M3 says the opposite.", "blocked_slots": [2, 3]}
    respond(run_root, "compose/v3/batch-0", {"material_defect": defect})
    outcome = run_compose(run_root, law)
    if outcome["status"] != "reject-upstream" or outcome["variants"]["v3"]["status"] != "reject-upstream" or outcome["variants"]["v3"]["to"] != "read":
        pytest.fail(f"반려가 reject-upstream 이 아니다: {outcome['status']} {outcome['variants']}")
    if "material-defect.md" not in str(outcome["reason_label"]):
        pytest.fail(f"전체 status 에 반려서 경로가 없다: {outcome['reason_label']}")
    path = os.path.join(run_root, "40-compose", "v3", "material-defect.md")
    text = open(path, encoding="utf-8").read()
    front = yaml.safe_load(text.split("---\n", 2)[1])
    if front != {"material_ids": [COMPONENTS[1], COMPONENTS[2]], "defect_kind": "unresolvable-grounding",
                 "evidence": "M2 says X while M3 says the opposite.", "blocked_slots": [2, 3]}:
        pytest.fail(f"반려서 4필드가 다르다: {front}")
    rows = tournament(run_root)
    if [(row["variant"], row["outcome"]) for row in rows] != [("v1", "drafted"), ("v2", "drafted"), ("v3", "material-defect")]:
        pytest.fail(f"토너먼트 행이 다르다: {rows}")
    # 반려서 스키마 — defect_kind 밖 값은 응답 자체가 거부된다(oneOf).
    errors = list(Draft202012Validator(compose_stage.RESPONSE_SCHEMAS["v1"]).iter_errors({"material_defect": dict(defect, defect_kind="typo")}))
    if not errors:
        pytest.fail("defect_kind enum 밖 값이 payload 스키마를 통과했다")
    if list(Draft202012Validator(compose_stage.RESPONSE_SCHEMAS["v1"]).iter_errors({"thread_annotated_md": "x", "material_defect": defect})):
        pass
    else:
        pytest.fail("초안과 반려서를 함께 낸 payload 가 통과했다")


# ---------------------------------------------------------------------------
# ⑬ 결측
# ---------------------------------------------------------------------------


def test_missing_variant_recorded_and_run_continues_or_halts(law, run_root) -> None:
    run_compose(run_root, law)
    respond_draft(run_root, "v2")
    respond_draft(run_root, "v3")
    outcome = run_compose(run_root, law, missing={"v1": "좌표 호출 상한 3 초과"})
    if outcome["status"] != "ok" or outcome["variants"]["v1"]["status"] != "missing":
        pytest.fail(f"결측 1 · 생존 2 가 ok 가 아니다: {outcome['status']} {outcome['variants']}")
    rows = tournament(run_root)
    missing = [row for row in rows if row["outcome"] == "missing"]
    if len(missing) != 1 or missing[0]["variant"] != "v1" or missing[0]["missing_reason"] != "좌표 호출 상한 3 초과" or missing[0]["comparison_axis"] != "effort":
        pytest.fail(f"결측 행이 다르다: {rows}")
    # 재진입(신고 없이) — 결측 행이 상태다.
    again = run_compose(run_root, law)
    if again["status"] != "ok" or again["variants"]["v1"]["status"] != "missing" or len(tournament(run_root)) != 3:
        pytest.fail(f"재진입에서 결측이 유지되지 않거나 행이 중복됐다: {again['variants']}")
    # 셋 다 결측 → halt
    shutil.rmtree(os.path.join(run_root, "40-compose"))
    run_compose(run_root, law)
    outcome = run_compose(run_root, law, missing={v: "dead" for v in VARIANTS})
    if outcome["status"] != "halt" or len(tournament(run_root)) != 3:
        pytest.fail(f"전 변주 결측이 halt 가 아니다: {outcome['status']} {tournament(run_root)}")


# ---------------------------------------------------------------------------
# ⑭ 종료선 · 진입 지문
# ---------------------------------------------------------------------------


def test_terminus_before_compose_halts_and_blueprint_digest_is_entry_check(law, tmp_path) -> None:
    run_root = make_run(str(tmp_path), partial_until="design")
    with pytest.raises(StageHaltError, match="compose 앞의 종료선"):
        run_compose(run_root, law)
    run_root2 = make_run(os.path.join(str(tmp_path), "second"))
    blueprint_path = os.path.join(run_root2, "20-design", "blueprint.json")
    blueprint = read_json(blueprint_path)
    blueprint["spec_digest"] = "sha256:" + "1" * 64
    json.dump(blueprint, open(blueprint_path, "w", encoding="utf-8"))
    from engine.stages import StageEnvironmentError

    with pytest.raises(StageEnvironmentError, match="blueprint.json#spec_digest"):
        run_compose(run_root2, law)


# ---------------------------------------------------------------------------
# ⑮ ⑯ 구동기
# ---------------------------------------------------------------------------


class PenStub:
    """`claude -p` json 출력 흉내 — 좌표의 변주에 맞는 초안 payload 를 낸다."""

    def __init__(self, run_root: str):
        self.run_root = run_root
        self.calls: list[list[str]] = []

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        digest = next(line for line in text.split("\n") if line.startswith("| 입력 지문 | `")).split("`")[1]
        variant = lane_id.split("/")[1]
        observed = argv[argv.index("--model") + 1]
        payload = {"thread_annotated_md": draft_for(variant, self.run_root)}
        body = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "duration_ms": 3,
                "total_cost_usd": 0.0, "session_id": "stub",
                "structured_output": {"lane_id": lane_id, "model": "self", "effort": "self", "input_digest": digest, "payload": payload},
                "modelUsage": {observed: {"inputTokens": 1, "outputTokens": 9}}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 3)


def _drive(law: str, run_root: str, evidence: str, *argv: str, executor=None, dry_run: bool = False) -> tuple[int, list[str]]:
    lines: list[str] = []
    head = ["--repo", law, "--run-root", run_root, "--evidence-dir", evidence]
    if dry_run:
        head.append("--dry-run")
    return drv.main([*head, *argv], executor=executor, out=lines.append), lines


def test_driver_compose_stub_receipts_dry_run_and_seal(law, run_root, tmp_path) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    # 블루프린트 없음 → 13
    os.rename(os.path.join(run_root, "20-design", "blueprint.json"), os.path.join(run_root, "20-design", "bp.bak"))
    code, _ = _drive(law, run_root, evidence, "compose", RUN_ID)
    if code != drv.EXIT_TERMINAL_FAIL:
        pytest.fail(f"블루프린트 없는 compose 가 13 이 아니다: {code}")
    os.rename(os.path.join(run_root, "20-design", "bp.bak"), os.path.join(run_root, "20-design", "blueprint.json"))
    # 요청서 생성 뒤 dry-run 은 세 명령줄
    run_compose(run_root, law)
    code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, dry_run=True)
    if code != drv.EXIT_PENDING or len(lines) != 3 or not all(line.startswith("[dry-run] compose/") for line in lines):
        pytest.fail(f"dry-run 이 세 명령줄이 아니다: {code} {lines}")
    if lines[0].count("--effort high") != 1 or "--effort xhigh" not in lines[1] or "--effort max" not in lines[2] or "--model claude-opus-5" not in lines[0]:
        pytest.fail(f"dry-run 명령줄의 좌석이 다르다: {lines}")
    stub = PenStub(run_root)
    code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 3:
        pytest.fail(f"compose 가 0 이 아니거나 호출 수가 3 이 아니다: {code} {lines}")
    if [argv[argv.index("--effort") + 1] for argv in stub.calls] != ["high", "xhigh", "max"]:
        pytest.fail("좌표 순서·effort 가 v1→v2→v3 순차가 아니다")
    receipts = sorted(name for name in os.listdir(os.path.join(evidence, "calls")) if name.endswith(".json") and not name.endswith(".raw.json"))
    if receipts != [f"compose__{v}__batch-0.json" for v in VARIANTS]:
        pytest.fail(f"영수증 3 이 아니다: {receipts}")
    for variant in VARIANTS:
        receipt = read_json(os.path.join(evidence, "calls", f"compose__{variant}__batch-0.json"))
        if receipt["requested"] != {"model": "opus-5", "effort": EFFORTS[variant], "api_id": "claude-opus-5"} or receipt["observed"]["main_model"] != "claude-opus-5":
            pytest.fail(f"{variant} 영수증이 다르다: {receipt['requested']} {receipt['observed']}")
    for variant in VARIANTS:
        if not os.path.isfile(os.path.join(run_root, "40-compose", variant, "thread.annotated.md")):
            pytest.fail(f"{variant} 확정본이 없다")
    code, _ = _drive(law, run_root, evidence, "compose", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 3:
        pytest.fail("compose 재진입이 다시 호출했다")
    code, lines = _drive(law, run_root, evidence, "lanes", RUN_ID)
    if code != drv.EXIT_OK or not any("compose/v2/batch-0" in line and line.startswith("완료") for line in lines):
        pytest.fail(f"lanes 가 펜 좌표를 보이지 않는다: {lines}")
    code, _ = _drive(law, run_root, evidence, "seal", RUN_ID)
    manifest = open(os.path.join(evidence, "MANIFEST-sha256.txt"), encoding="utf-8").read().splitlines()
    rels = [line.split("  ", 1)[1] for line in manifest]
    if code != drv.EXIT_OK or not any(rel.endswith("40-compose/v1/thread.annotated.md") for rel in rels) or not any(rel.endswith("40-compose/tournament-rows.jsonl") for rel in rels):
        pytest.fail(f"MANIFEST 에 펜 산출이 없다: {rels}")


def test_driver_declares_missing_after_call_cap(law, run_root, tmp_path) -> None:
    """v1 좌표가 늘 실패하면 회차 4 에서 15 → 결측 신고 → 생존 2 로 0."""
    evidence = os.path.join(str(tmp_path), "evidence")
    good = PenStub(run_root)

    def flaky(argv, stdin, env, timeout):
        lane_id = stdin.decode("utf-8").split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        if lane_id.startswith("compose/v1/"):
            return drv.ExecResult(1, json.dumps({"type": "result", "is_error": True, "result": "dead"}).encode(), b"dead", False, 1)
        return good(argv, stdin, env, timeout)

    codes = []
    for _ in range(4):
        code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, executor=flaky)
        codes.append(code)
        if code == drv.EXIT_OK:
            break
    if codes[:3] != [drv.EXIT_PENDING] * 3 or codes[-1] != drv.EXIT_OK:
        pytest.fail(f"호출 상한 뒤 결측 신고로 0 이 되지 않는다: {codes} {lines}")
    rows = tournament(run_root)
    if [(row["variant"], row["outcome"]) for row in rows] != [("v1", "missing"), ("v2", "drafted"), ("v3", "drafted")]:
        pytest.fail(f"결측 행이 다르다: {rows}")


def test_help_lists_fourteen_commands_with_compose_before_gate() -> None:
    """명령 12 → 14(T64 집행 ③ · gate-l0 · strip 이 compose 뒤에 온다)."""
    parser = drv.build_parser()
    listed = tuple(parser._subparsers._group_actions[0].choices)  # noqa: SLF001
    if listed != drv.COMMANDS or len(listed) != 15 or listed[-3:] != ("compose", "gate-l0", "strip"):
        pytest.fail(f"명령 15 가 아니다: {listed}")
    wrapper = drv.wrapper_schema("v2")
    if wrapper["properties"]["payload"] is not compose_stage.RESPONSE_SCHEMAS["v2"] or compose_stage.RESPONSE_SCHEMAS["v1"] is not compose_stage.RESPONSE_SCHEMAS["v3"]:
        pytest.fail("구동기 래퍼가 compose.RESPONSE_SCHEMAS 상수를 품지 않거나 세 변주의 스키마가 다른 객체다")
    Draft202012Validator.check_schema(wrapper)
