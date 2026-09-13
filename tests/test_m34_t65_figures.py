# -*- coding: utf-8 -*-
"""M34 — `figures` 스테이지 실물화(prepare crop-only 렌더 · select) · `format.stop-shape` 가동 · `n/N` 순번 토크나이저 ·
compose 2회차 · gate rounds · 구동기 `figures`·`compose --variant --round`(재정 2026-09-13 T65 ③ · 자잘).

모델 호출 없음. 실 브라우저도 부르지 않는다 — 렌더러는 가짜(표준 라이브러리 zlib 로 2400×1350 PNG 합성)를 넘긴다.
실 브라우저 스모크 1건은 `PD_REAL_RENDER=1` 일 때만 돈다.

픽스처 = 런 -3 동결본 사본(읽기만 · tmp 로) + 합성 `figures-raw/`(동결본 `figures[].raw_path` 이름으로 1×1 PNG · 복합
시트 1건 = FIG-8·FIG-9 가 `fig-08-09.png` 하나를 가리킨다 — 런 -3 원천 파일명 실측) + `source-report.json` 도면별
행(sha256 맞춤) + 런 -3 `blueprint.json` 사본 + 합성 run.yaml(`partial_until: gate`).

★ 골든 rc-0008 의 기대값은 `samples.json` 이 들고 여기서는 실측을 그 파일에 물린다(값 복제 금지).
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.annotation import parse as parse_mod  # noqa: E402
from engine.annotation import strip as strip_mod  # noqa: E402
from engine.figures import asset_id_for_figure, asset_id_of  # noqa: E402
from engine.figures import render as render_mod  # noqa: E402
from engine.gate.l0 import L0Context, L0Law, load_rules_from_law  # noqa: E402
from engine.gate.l0 import rules_numeric  # noqa: E402
from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.pens import lint  # noqa: E402
from engine.stages import StageEnvironmentError, StageError, sha256_bytes, sha256_file  # noqa: E402
from engine.stages import compose as compose_stage  # noqa: E402
from engine.stages import figures as figures_stage  # noqa: E402
from engine.stages import gate as gate_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

RUN_ID = "gdm-wo2026128750a1-agent-memory-3"
RUN3 = os.path.join(REPO, "runs", RUN_ID)
RUN3_FROZEN = os.path.join(RUN3, "15-frozen", "material-spec.v1.json")
RUN3_BLUEPRINT = os.path.join(RUN3, "20-design", "blueprint.json")
RUN3_V2_THREAD = os.path.join(RUN3, "40-compose", "v2", "thread.annotated.md")
GOLDEN_THREAD = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless", "thread.annotated.md")
GOLDEN_0001 = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless")
GOLDEN_0008 = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0008-thread-marker-counterexamples", "samples.json")
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
FIXTURES = os.path.join(REPO, "tests", "fixtures", "schema-enforcement")
LAW_TREES = ("contracts", "reader", "studio")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"))
COMPOSITE_FILE = "fig-08-09.png"
SLOT_ENUM = compose_stage.sheet_values(REPO)["slot_enum"]
SHEET = compose_stage.sheet_values(REPO)


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str, payload) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)


def make_png(width: int, height: int, seed: int = 0) -> bytes:
    """표준 라이브러리만으로 8비트 그레이 PNG(필터 0)."""
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    row = bytes([0]) + bytes([(seed + x) % 256 for x in range(width)])
    raw = row * height
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 1)) + chunk(b"IEND", b""))


def _git(cwd: str, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        pytest.fail(f"git {' '.join(args)} 실패: {proc.stderr}")
    return proc.stdout.strip()


def make_law(destination: str) -> str:
    for tree in LAW_TREES:
        shutil.copytree(os.path.join(REPO, tree), os.path.join(destination, tree),
                        ignore=shutil.ignore_patterns("__pycache__", "node_modules"), dirs_exist_ok=True)
    for parts in LAW_FILES:
        target = os.path.join(destination, *parts)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(os.path.join(REPO, *parts), target)
    _git(destination, "init", "-q", "-b", "main")
    _git(destination, "config", "user.email", "runner@example.com")
    _git(destination, "config", "user.name", "runner")
    _git(destination, "add", "contracts", "reader", "docs", "engine", "studio")
    _git(destination, "commit", "-q", "-m", "law")
    return destination


def fixture_frozen() -> dict:
    """런 -3 동결본 사본 + 복합 시트: FIG-8 의 raw_path 를 실측 파일명(fig-08-09.png)으로, FIG-9 를 같은 파일로 추가."""
    frozen = read_json(RUN3_FROZEN)
    figures = frozen["figures"]
    for figure in figures:
        if figure["id"] == "FIG-8":
            figure["raw_path"] = f"00-source/figures-raw/{COMPOSITE_FILE}"
    template = copy.deepcopy(next(figure for figure in figures if figure["id"] == "FIG-8"))
    template["id"] = "FIG-9"
    template["caption_quote"] = "Figure 9 is a block diagram that illustrates aspects of a machine-learned agent system."
    template["numerals"] = []
    figures.insert([f["id"] for f in figures].index("FIG-8") + 1, template)
    return frozen


def make_run(root: str, *, partial_until: str = "gate", frozen: dict | None = None, run_kind: str = "partial",
             blueprint_mutate=None, drafts: dict | None = None) -> str:
    run_root = os.path.join(root, "runs", RUN_ID)
    frozen = frozen or fixture_frozen()
    frozen_dir = os.path.join(run_root, "15-frozen")
    os.makedirs(frozen_dir, exist_ok=True)
    frozen_path = os.path.join(frozen_dir, "material-spec.v1.json")
    write_json(frozen_path, frozen)
    os.chmod(frozen_path, 0o444)
    digest = sha256_file(frozen_path)
    # 원천 도면 — raw_path 이름 그대로 1×1 PNG(복합 시트는 파일 하나)
    raw_dir = os.path.join(run_root, "00-source", "figures-raw")
    os.makedirs(raw_dir, exist_ok=True)
    rows = []
    seen: set[str] = set()
    for index, figure in enumerate(frozen["figures"]):
        name = os.path.basename(figure["raw_path"])
        if name in seen:
            continue
        seen.add(name)
        blob = make_png(1, 1, seed=index)
        with open(os.path.join(raw_dir, name), "wb") as handle:
            handle.write(blob)
        rows.append({"filename": name, "sha256": sha256_bytes(blob), "figure_number": index + 1, "bytes": len(blob),
                     "counted_as": 1, "counting_unit": "source-figure-file"})
    write_json(os.path.join(run_root, "00-source", "source-report.json"),
               {"stage": "source", "run_id": RUN_ID, "figure_count": len(rows), "figures": rows,
                "figures_manifest_digest": "sha256:" + "0" * 64, "source": {"canonical_sha256": "sha256:" + "0" * 64}})
    meta = {
        "schema": "run/v0", "run_id": RUN_ID, "status": "active", "run_kind": run_kind, "partial_until": partial_until,
        "engine": {"commit": "e" * 40, "worktree": None}, "numeric_whitelist": [],
        "frozen": [{"spec_version": 1, "path": "15-frozen/material-spec.v1.json", "spec_digest": digest}],
    }
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    blueprint = read_json(RUN3_BLUEPRINT)
    blueprint["spec_digest"] = digest
    blueprint["run_id"] = RUN_ID
    if blueprint_mutate:
        blueprint_mutate(blueprint)
    write_json(os.path.join(run_root, "20-design", "blueprint.json"), blueprint)
    for variant, text in (drafts or {}).items():
        path = os.path.join(run_root, "40-compose", variant, "thread.annotated.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    return run_root


class FakeRenderer:
    """`renderer(jobs, jobs_path) -> results` — 2400×1350 PNG 를 합성한다. `size` 로 틀린 치수를, `fail` 로 실패 자산을 심는다."""

    def __init__(self, size=(2400, 1350), fail=()):
        self.size = size
        self.fail = set(fail)
        self.calls: list[list[dict]] = []

    def __call__(self, jobs, jobs_path):
        self.calls.append(list(jobs))
        results = []
        for job in jobs:
            if job["asset_id"] in self.fail:
                results.append({"out": job["out"], "ok": False, "error": "planted"})
                continue
            os.makedirs(os.path.dirname(job["out"]), exist_ok=True)
            with open(job["out"], "wb") as handle:
                handle.write(make_png(*self.size, seed=len(self.calls)))
            results.append({"out": job["out"], "ok": True})
        return results


def run_digest(run_root: str) -> str:
    return yaml.safe_load(read(os.path.join(run_root, "run.yaml")))["frozen"][0]["spec_digest"]


def prepared(run_root: str, law: str, **kwargs):
    renderer = FakeRenderer(**kwargs)
    outcome = figures_stage.prepare(run_root, law, renderer=renderer)
    return outcome, renderer


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(read_json(os.path.join(SCHEMAS, f"{name}.schema.json")))


def rows_by_id(outcome: dict) -> dict:
    return {row.check_id: row for row in outcome["rows"]}


def frontmatter_for(variant: str, digest: str, effort: str) -> str:
    return (f"---\nrun_id: {RUN_ID}\nvariant: {variant}\npen: {{ vendor: anthropic, model: opus-5, effort: {effort} }}\n"
            f"spec_version: 1\nspec_digest: {digest}\n---\n")


def golden_body() -> str:
    return read(GOLDEN_THREAD).split("---\n", 2)[2]


def draft_for(variant: str, run_root: str, *, headers: dict[int, str] | None = None) -> str:
    """골든 본문 + 픽스처 프런트매터. `headers` = {T: figspec} 로 헤더 fig 를 바꾼다."""
    efforts = {pen["variant"]: pen["effort"] for pen in compose_stage.registry.pens(REPO)}
    body = golden_body()
    if headers:
        def swap(match):
            n = int(match.group(1))
            return f"## T{n} {{slot: {match.group(2)}, fig: {headers.get(n, match.group(3))}}}"
        body = re.sub(r"^## T(\d+) \{slot: ([a-z]+), fig: ([^}]+)\}$", swap, body, flags=re.M)
    return frontmatter_for(variant, run_digest(run_root), efforts[variant]) + body


def headers_from_selection(selection: dict) -> dict[int, str]:
    by_tweet = figures_stage.selection_assets_by_tweet(selection)
    return {n: "+".join(assets) for n, assets in by_tweet.items()}


def respond(run_root: str, lane_id: str, payload: dict, *, model: str = "claude-opus-5") -> str:
    directory = os.path.join(run_root, "40-compose", "lanes", *lane_id.split("/"))
    request = read_json(os.path.join(directory, "request.json"))
    path = os.path.join(directory, "response.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"lane_id": lane_id, "model": model, "effort": request["effort"], "input_digest": request["input_digest"],
                   "payload": payload}, handle, ensure_ascii=False)
    return path


def tournament(run_root: str) -> list[dict]:
    path = os.path.join(run_root, "40-compose", "tournament-rows.jsonl")
    return [json.loads(line) for line in read(path).splitlines() if line.strip()] if os.path.isfile(path) else []


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(str(tmp_path))


# ---------------------------------------------------------------------------
# ⑴ 계약 · 경로
# ---------------------------------------------------------------------------


def test_contract_loads_and_paths_declare_manifest_and_selection(law) -> None:
    contract = load_stage_contract("figures", law)
    if contract["schema"] != "stage-contract/v0" or contract["id"] != "figures":
        pytest.fail("figures.yaml 골격이 다르다")
    steps = [step["id"] for step in contract["steps"]]
    if steps != ["figures.prepare", "figures.select"]:
        pytest.fail(f"steps 둘이 아니다: {steps}")
    if contract["steps"][0]["lane"] != {"tool": "headless-chromium", "model": "none"} or contract["steps"][1]["lane"]["model"] is not None:
        pytest.fail("단계 좌석이 계약 문언(prepare = headless-chromium · select = 결정론 도구 · 재량 ⓐ)과 다르다")
    ids = [row["id"] for row in contract["checks_before_exit"]]
    if ids != ["figures.asset-completeness", "figures.render-spec", "figures.manifest-parity", "figures.selection-resolve",
               "figures.publish-gate", "figures.no-copy"]:
        pytest.fail(f"검사 6 이 다르다: {ids}")
    if [row["id"] for row in contract["checks_on_entry"]] != ["figures.input-digest"] or len(contract["failure"]) != 6:
        pytest.fail("진입 검사·실패표 5+1 이 다르다")
    if "20-design/**" not in contract["steps"][0]["must_not_read"] or "00-source/**" not in contract["steps"][1]["must_not_read"]:
        pytest.fail("prepare 의 20-design 금지 · select 의 00-source 금지가 없다")
    paths = RunPaths("/nonexistent/run", law)
    if paths.STAGES != ("source", "read", "freeze", "design", "figures", "compose", "gate", "probe", "critique", "ship"):   # T69 ⑦
        pytest.fail(f"STAGES 에 figures 가 design 뒤에 없다: {paths.STAGES}")
    if not paths.figures_manifest_json.endswith("30-figures/assets/manifest.json") or not paths.figures_selection_json.endswith("30-figures/selection.json"):
        pytest.fail("manifest.json·selection.json 선언 경로가 다르다")
    if not paths.figures_report_json.endswith("30-figures/figures-report.json") or not paths.figure_asset("fig-03").endswith("30-figures/assets/fig-03.png"):
        pytest.fail("figures-report·자산 경로가 다르다")
    if not paths.compose_round_dir("v2", 1).endswith("40-compose/v2/rounds/r1") or not paths.gate_round_dir("v2", 1).endswith("50-gate/v2/rounds/r1"):
        pytest.fail("rounds 경로가 다르다")


# ---------------------------------------------------------------------------
# ⑵ 스키마 2 — accept/reject 픽스처
# ---------------------------------------------------------------------------


def test_figures_schemas_accept_and_reject_fixtures() -> None:
    cases = [case for case in read_json(os.path.join(FIXTURES, "manifest.json"))["cases"] if "figures-" in case["file"]]
    if sum(1 for c in cases if c["schema"].endswith("figures-manifest.schema.json") and c["expect"] == "accept") != 1 \
            or sum(1 for c in cases if c["schema"].endswith("figures-manifest.schema.json") and c["expect"] == "reject") < 2 \
            or sum(1 for c in cases if c["schema"].endswith("figures-selection.schema.json") and c["expect"] == "accept") != 1 \
            or sum(1 for c in cases if c["schema"].endswith("figures-selection.schema.json") and c["expect"] == "reject") < 2:
        pytest.fail(f"스키마 2 의 accept 1 · reject ≥2 픽스처가 아니다: {[c['file'] for c in cases]}")
    for case in cases:
        schema = read_json(os.path.join(REPO, case["schema"]))
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema).iter_errors(read_json(os.path.join(FIXTURES, case["file"]))))
        actual = "accept" if not errors else "reject"
        if actual != case["expect"]:
            pytest.fail(f"{case['file']}: 기대 {case['expect']} ≠ 실제 {actual} — {errors[0].message if errors else ''}")
    for name, line in (("figures-manifest", "figures-manifest/v0"), ("figures-selection", "figures-selection/v0")):
        if read_json(os.path.join(SCHEMAS, f"{name}.schema.json"))["title"] != line:
            pytest.fail(f"{name} 스키마 title 이 계약 라인이 아니다")


# ---------------------------------------------------------------------------
# ⑶ prepare — 가짜 렌더러
# ---------------------------------------------------------------------------


def test_prepare_renders_all_figures_with_composite_sheet_and_manifest_keys(law, run_root) -> None:
    outcome, renderer = prepared(run_root, law)
    frozen = read_json(os.path.join(run_root, "15-frozen", "material-spec.v1.json"))
    figures = [f["id"] for f in frozen["figures"]]
    if outcome["status"] != "ok" or len(renderer.calls) != 1 or len(renderer.calls[0]) != len(figures):
        pytest.fail(f"prepare 가 한 번의 렌더로 전량을 만들지 않았다: {outcome['status']} {outcome['reason_label']} calls={len(renderer.calls)}")
    manifest = read_json(os.path.join(run_root, "30-figures", "assets", "manifest.json"))
    errors = [e.message for e in validator("figures-manifest").iter_errors(manifest)]
    if errors:
        pytest.fail(f"매니페스트가 figures-manifest/v0 를 위반한다: {errors[0]}")
    items = manifest["items"]
    assets = sorted(name for name in os.listdir(os.path.join(run_root, "30-figures", "assets")) if name.endswith(".png"))
    if len(items) != len(figures) or len(assets) != len(figures) or [i["figure_id"] for i in items] != figures:
        pytest.fail(f"자산 수 ≠ figures 수: items {len(items)} · files {len(assets)} · figures {len(figures)}")
    by_id = {item["figure_id"]: item for item in items}
    eight, nine = by_id["FIG-8"], by_id["FIG-9"]
    if eight["asset_id"] != "fig-08" or nine["asset_id"] != "fig-09" or eight["source_raw_path"] != nine["source_raw_path"] \
            or eight["source_sha256"] != nine["source_sha256"] or eight["sha256"] == "" or eight["asset_path"] == nine["asset_path"]:
        pytest.fail(f"복합 시트 두 FIG 가 같은 원본·다른 자산이 아니다: {eight} {nine}")
    ops = {edit["op"]: edit for edit in eight["edits"]}
    if "composite-sheet" not in ops or ops["composite-sheet"]["shares_with"] != ["FIG-9"] or \
            {e["op"]: e for e in nine["edits"]}["composite-sheet"]["shares_with"] != ["FIG-8"]:
        pytest.fail(f"composite-sheet edits 가 다르다: {eight['edits']} {nine['edits']}")
    required = {"figure_id", "source_raw_path", "asset_path", "sha256", "renderer", "template", "fallback", "edits", "edit_class",
                "publishable", "rendered_at", "asset_id", "source_sha256"}
    for item in items:
        if set(item) != required or item["edit_class"] != "crop-only" or item["publishable"] is not True or item["fallback"] is not True:
            pytest.fail(f"항목 키·값이 §7.5 10키 + asset_id·source_sha256 · crop-only · publishable true 가 아니다: {item}")
        if item["source_sha256"] != sha256_file(os.path.join(run_root, item["source_raw_path"])) \
                or item["sha256"] != sha256_file(os.path.join(run_root, item["asset_path"])):
            pytest.fail("원천·자산 지문이 실측과 다르다")
    rows = rows_by_id(outcome)
    for check in ("figures.asset-completeness", "figures.render-spec", "figures.manifest-parity"):
        if rows[check].status != "pass" or rows[check].checked == 0:
            pytest.fail(f"{check} 가 pass·checked>0 이 아니다: {rows[check].to_row_dict()}")
    report = read_json(os.path.join(run_root, "30-figures", "figures-report.json"))
    if report["steps"]["figures.prepare"]["status"] != "ok" or len(report["steps"]["figures.prepare"]["rows"]) != 4:
        pytest.fail("figures-report.json 의 prepare 블록이 다르다")
    if manifest["renderer"]["playwright"] != render_mod.playwright_pin(law) or manifest["renderer"]["viewport"] != [1200, 675]:
        pytest.fail("renderer 블록이 핀·뷰포트와 다르다")
    html = read(os.path.join(run_root, "30-figures", "assets", ".render", "fig-01.html"))
    if "data:image/png;base64," not in html or "figures-raw" in html:
        pytest.fail("렌더 입력이 원본 바이트를 인라인하지 않았거나 원천 경로를 참조한다")


# ---------------------------------------------------------------------------
# ⑷ 재진입 — 자산 보존 · 없는 것만 더함
# ---------------------------------------------------------------------------


def test_reentry_calls_no_renderer_and_fills_only_missing_item(law, run_root) -> None:
    prepared(run_root, law)
    manifest_path = os.path.join(run_root, "30-figures", "assets", "manifest.json")
    before = read_json(manifest_path)
    outcome, renderer = prepared(run_root, law)
    if outcome["status"] != "ok" or renderer.calls or read_json(manifest_path) != before:
        pytest.fail(f"재진입이 렌더러를 불렀거나 매니페스트를 바꿨다: calls={len(renderer.calls)}")
    # 항목 하나(FIG-3)를 지우고 그 자산 파일도 지우면 그것만 렌더된다
    manifest = read_json(manifest_path)
    manifest["items"] = [item for item in manifest["items"] if item["figure_id"] != "FIG-3"]
    write_json(manifest_path, manifest)
    os.remove(os.path.join(run_root, "30-figures", "assets", "fig-03.png"))
    others = {name: sha256_file(os.path.join(run_root, "30-figures", "assets", name))
              for name in os.listdir(os.path.join(run_root, "30-figures", "assets")) if name.endswith(".png")}
    outcome, renderer = prepared(run_root, law)
    if outcome["status"] != "ok" or len(renderer.calls) != 1 or [job["asset_id"] for job in renderer.calls[0]] != ["fig-03"]:
        pytest.fail(f"없는 항목만 렌더하지 않았다: {[[j['asset_id'] for j in c] for c in renderer.calls]}")
    after = read_json(manifest_path)
    if [i["figure_id"] for i in after["items"]] != [i["figure_id"] for i in before["items"]]:
        pytest.fail("재진입 뒤 항목 순서가 동결본 순서가 아니다")
    for name, digest in others.items():
        if sha256_file(os.path.join(run_root, "30-figures", "assets", name)) != digest:
            pytest.fail(f"기존 자산 {name} 이 덮어써졌다(§7.5)")
    # 매니페스트에 없는 자산 파일이 남아 있으면 덮어쓰지 않고 멈춘다
    manifest = read_json(manifest_path)
    manifest["items"] = [item for item in manifest["items"] if item["figure_id"] != "FIG-2"]
    write_json(manifest_path, manifest)
    with pytest.raises(StageError, match="덮어쓰지 않는다"):
        prepared(run_root, law)


# ---------------------------------------------------------------------------
# ⑸ render-spec 위반 → retry(1) → halt
# ---------------------------------------------------------------------------


def test_wrong_pixel_size_fails_render_spec_and_halts_after_one_retry(law, run_root) -> None:
    outcome, renderer = prepared(run_root, law, size=(1200, 675))
    rows = rows_by_id(outcome)
    if outcome["status"] != "halt" or outcome["attempts"] != 2 or len(renderer.calls) != 2:
        pytest.fail(f"render-spec 위반이 retry(1) → halt 가 아니다: {outcome['status']} attempts={outcome['attempts']} calls={len(renderer.calls)}")
    if rows["figures.render-spec"].status != "fail" or "1200x675" not in rows["figures.render-spec"].findings[0].found:
        pytest.fail(f"render-spec 행이 실측 치수를 적지 않았다: {rows['figures.render-spec'].to_row_dict()}")
    if os.path.isfile(os.path.join(run_root, "30-figures", "assets", "manifest.json")):
        if read_json(os.path.join(run_root, "30-figures", "assets", "manifest.json"))["items"]:
            pytest.fail("치수가 틀린 자산이 매니페스트에 올랐다")


# ---------------------------------------------------------------------------
# ⑹ 원본 누락 → asset-completeness fail → escalate 누락 목록
# ---------------------------------------------------------------------------


def test_missing_source_figure_escalates_with_missing_list(law, run_root) -> None:
    os.remove(os.path.join(run_root, "00-source", "figures-raw", "fig-03.png"))
    outcome, renderer = prepared(run_root, law)
    rows = rows_by_id(outcome)
    if outcome["status"] != "escalate" or outcome["missing"] != ["FIG-3"] or rows["figures.asset-completeness"].status != "fail":
        pytest.fail(f"원본 누락이 escalate + 누락 목록이 아니다: {outcome['status']} {outcome['missing']}")
    if any(job["asset_id"] == "fig-03" for job in renderer.calls[0]):
        pytest.fail("원본이 없는 도면을 렌더하려 했다")
    # 렌더 실패(일부)도 같은 행 — retry(1) 뒤 escalate
    run2 = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "second"))
    outcome2, renderer2 = prepared(run2, law, fail={"fig-07"})
    if outcome2["status"] != "escalate" or outcome2["missing"] != ["FIG-7"] or len(renderer2.calls) != 2 \
            or [job["asset_id"] for job in renderer2.calls[1]] != ["fig-07"]:
        pytest.fail(f"일부 렌더 실패가 retry(1)(실패분만) → escalate 가 아니다: {outcome2['status']} {outcome2['missing']} {[[j['asset_id'] for j in c] for c in renderer2.calls]}")


# ---------------------------------------------------------------------------
# ⑹-b 재정 T66 ① — 동결본 raw_path 부재 시 source-report 도면 번호 유일 일치로 해소(재료 무변경)
# ---------------------------------------------------------------------------


def _rename_source(run_root: str, old: str, new: str, *, extra_row: bool = False) -> None:
    raw_dir = os.path.join(run_root, "00-source", "figures-raw")
    os.rename(os.path.join(raw_dir, old), os.path.join(raw_dir, new))
    report_path = os.path.join(run_root, "00-source", "source-report.json")
    report = read_json(report_path)
    for row in report["figures"]:
        if row["filename"] == old:
            row["filename"] = new
            if extra_row:
                report["figures"].append(dict(row, filename=old + ".dup"))
    write_json(report_path, report)


def test_resolves_missing_raw_path_by_unique_figure_number_and_records_edit(law, run_root) -> None:
    """런 -3 실측(FIG-19 fig-19.png ↔ fig-19.jpg)의 재현 — 동결본은 그대로, 매니페스트에 해소 기록."""
    _rename_source(run_root, "fig-03.png", "fig-03.jpg")
    outcome, renderer = prepared(run_root, law)
    rows = rows_by_id(outcome)
    if outcome["status"] != "ok" or rows["figures.asset-completeness"].status != "pass":
        pytest.fail(f"유일 일치 해소가 통과하지 않았다: {outcome['status']} {[f.locus for f in rows['figures.asset-completeness'].findings]}")
    item = next(entry for entry in outcome["manifest"]["items"] if entry["figure_id"] == "FIG-3")
    edit = next((edit for edit in item["edits"] if edit["op"] == figures_stage.OP_RESOLVED), None)
    if edit is None or edit["from"] != "00-source/figures-raw/fig-03.png" or edit["to"] != "00-source/figures-raw/fig-03.jpg" \
            or item["source_raw_path"] != "00-source/figures-raw/fig-03.jpg":
        pytest.fail(f"해소 기록이 없거나 다르다: {item['edits']} {item['source_raw_path']}")
    frozen = read_json(os.path.join(run_root, "15-frozen", "material-spec.v1.json"))
    if next(f for f in frozen["figures"] if f["id"] == "FIG-3")["raw_path"] != "00-source/figures-raw/fig-03.png":
        pytest.fail("재료가 바뀌었다 — 해소는 기록이지 개정이 아니다(재정 T66 ①)")
    if not any(job["asset_id"] == "fig-03" for job in renderer.calls[0]):
        pytest.fail("해소된 도면을 렌더하지 않았다")


def test_resolution_requires_unique_number_and_matching_digest(law, run_root, tmp_path) -> None:
    # 같은 번호 행이 둘이면 풀지 않는다 → 종전대로 누락 · escalate
    _rename_source(run_root, "fig-03.png", "fig-03.jpg", extra_row=True)
    outcome, _ = prepared(run_root, law)
    if outcome["status"] != "escalate" or outcome["missing"] != ["FIG-3"]:
        pytest.fail(f"비유일 일치가 해소되었다: {outcome['status']} {outcome['missing']}")
    # 유일 일치이되 지문이 다르면 환경 오류(원천 변경 · P-U2)
    run2 = make_run(os.path.join(str(tmp_path), "second"))
    _rename_source(run2, "fig-03.png", "fig-03.jpg")
    with open(os.path.join(run2, "00-source", "figures-raw", "fig-03.jpg"), "wb") as handle:
        handle.write(make_png(3, 3, seed=7))
    with pytest.raises(StageEnvironmentError, match="fig-03.jpg"):
        prepared(run2, law)


# ---------------------------------------------------------------------------
# ⑺ 원천 지문 불일치 → 환경 오류 · ⑧ 렌더 환경 부재
# ---------------------------------------------------------------------------


def test_changed_source_bytes_is_environment_error(law, run_root) -> None:
    with open(os.path.join(run_root, "00-source", "figures-raw", "fig-02.png"), "wb") as handle:
        handle.write(make_png(2, 2, seed=99))
    with pytest.raises(StageEnvironmentError, match="figures-raw/fig-02.png"):
        prepared(run_root, law)


def test_missing_render_environment_names_what_is_absent(law, run_root, monkeypatch) -> None:
    def fake_report(repo):
        return {"missing": ["node(PATH 에 없다)", "브라우저 디렉터리(~/.cache/ms-playwright/chromium-1148 · 전체 빌드 chromium-1148)"],
                "node": None, "package": "1.49.1", "playwright_pin": "1.49.1", "browser": None}
    monkeypatch.setattr(render_mod, "environment_report", fake_report)
    with pytest.raises(StageEnvironmentError) as caught:
        figures_stage.prepare(run_root, law, renderer=None)
    if "node" not in str(caught.value) or "chromium-1148" not in str(caught.value):
        pytest.fail(f"진단에 무엇이 없는지가 없다: {caught.value}")
    monkeypatch.undo()
    report = render_mod.environment_report(law)
    if set(report) < {"node", "package", "browser", "missing", "playwright_pin"} or report["playwright_pin"] != "1.49.1":
        pytest.fail(f"환경 실측 보고 형태가 다르다: {report}")


# ---------------------------------------------------------------------------
# ⑨ select
# ---------------------------------------------------------------------------


def test_select_projects_figure_plan_into_pointer_slots(law, run_root) -> None:
    prepared(run_root, law)
    outcome = figures_stage.select(run_root, law)
    if outcome["status"] != "ok":
        pytest.fail(f"select 가 ok 가 아니다: {outcome['status']} {outcome['reason_label']}")
    selection = read_json(os.path.join(run_root, "30-figures", "selection.json"))
    errors = [e.message for e in validator("figures-selection").iter_errors(selection)]
    if errors:
        pytest.fail(f"selection 이 figures-selection/v0 를 위반한다: {errors[0]}")
    by_tweet = figures_stage.selection_assets_by_tweet(selection)
    if by_tweet.get(1) != ["fig-01"] or by_tweet.get(3) != ["fig-08", "fig-07"] or 9 in by_tweet:
        pytest.fail(f"슬롯 사영이 블루프린트 figure_plan 과 다르다: {by_tweet}")
    roles = [(s["tweet"], s["role"]) for s in selection["slots"]]
    if roles[0] != (1, "hero") or any(role == "hero" for tweet, role in roles[1:]):
        pytest.fail(f"role 배정이 다르다: {roles}")
    if selection["blueprint_digest"] != sha256_file(os.path.join(run_root, "20-design", "blueprint.json")) or selection["spec_digest"] != run_digest(run_root):
        pytest.fail("selection 의 지문 결속이 다르다")
    rows = rows_by_id(outcome)
    for check in ("figures.selection-resolve", "figures.no-copy", "figures.publish-gate"):
        if rows[check].status != "pass":
            pytest.fail(f"{check} 가 pass 가 아니다: {rows[check].to_row_dict()}")
    if rows["figures.publish-gate"].extras["branch"] != "①" or rows["figures.publish-gate"].extras["run_kind"] != "partial":
        pytest.fail(f"partial 런의 publish-gate 가 ①만이 아니다: {rows['figures.publish-gate'].extras}")
    if not os.path.isfile(os.path.join(run_root, "30-figures", "corrections-rows.md")) or "기각 | 0" not in read(os.path.join(run_root, "30-figures", "corrections-rows.md")):
        pytest.fail("교정 원장 행(런 안)이 없거나 「기각 0」이 없다")
    # publishable false 자산 지목 → halt
    manifest_path = os.path.join(run_root, "30-figures", "assets", "manifest.json")
    manifest = read_json(manifest_path)
    for item in manifest["items"]:
        if item["figure_id"] == "FIG-1":
            item["publishable"] = False
    write_json(manifest_path, manifest)
    os.remove(os.path.join(run_root, "30-figures", "selection.json"))
    outcome = figures_stage.select(run_root, law)
    if outcome["status"] != "halt" or rows_by_id(outcome)["figures.publish-gate"].status != "fail" or os.path.isfile(os.path.join(run_root, "30-figures", "selection.json")):
        pytest.fail(f"publishable false 지목이 halt 가 아니거나 selection 을 썼다: {outcome['status']}")
    # 블루프린트가 매니페스트에 없는 FIG 지목 → reject-upstream(→ design)
    run2 = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "second"),
                    blueprint_mutate=lambda bp: bp["figure_plan"][1]["figures"].append("FIG-13"))
    prepared(run2, law)
    manifest_path = os.path.join(run2, "30-figures", "assets", "manifest.json")
    manifest = read_json(manifest_path)
    manifest["items"] = [item for item in manifest["items"] if item["figure_id"] != "FIG-13"]
    write_json(manifest_path, manifest)
    os.remove(os.path.join(run2, "30-figures", "assets", "fig-13.png"))
    outcome = figures_stage.select(run2, law)
    if outcome["status"] != "reject-upstream" or outcome["unresolved"] != ["T2:FIG-13"]:
        pytest.fail(f"자산층에 없는 도면 지목이 reject-upstream 이 아니다: {outcome['status']} {outcome['unresolved']}")


# ---------------------------------------------------------------------------
# ⑩ 트윗 자산 5 → selection-resolve fail(시트 값)
# ---------------------------------------------------------------------------


def test_too_many_assets_per_tweet_fails_selection_resolve(law, tmp_path) -> None:
    limit = int(SHEET["images_per_post_max"])
    extra = ["FIG-1", "FIG-3", "FIG-10", "FIG-13", "FIG-19", "FIG-21"][: limit + 1 - 1]

    def mutate(bp):
        plan = bp["figure_plan"][1]
        plan["figures"] = list(dict.fromkeys([*plan["figures"], *extra]))[: limit + 1]

    run_root = make_run(str(tmp_path), blueprint_mutate=mutate)
    prepared(run_root, law)
    outcome = figures_stage.select(run_root, law)
    row = rows_by_id(outcome)["figures.selection-resolve"]
    if outcome["status"] != "escalate" or row.status != "fail" or row.extras["per_tweet"]["T2"] != limit + 1:
        pytest.fail(f"트윗 자산 {limit + 1} 이 selection-resolve fail → escalate 가 아니다: {outcome['status']} {row.extras}")
    if os.path.isfile(os.path.join(run_root, "30-figures", "selection.json")):
        pytest.fail("실패한 선택을 파일로 썼다")


# ---------------------------------------------------------------------------
# ⑪ stop-shape 가동 — 실제 manifest + 런 -3 v2 주석본
# ---------------------------------------------------------------------------


def context_for(text: str, law_root: str, manifest: dict | None, frozen: dict) -> L0Context:
    law = L0Law.load(law_root)
    parsed = parse_mod.parse(text, slot_enum=SLOT_ENUM)
    if parsed.errors:
        pytest.fail(f"표본이 파싱되지 않는다: {parsed.errors[:2]}")
    stripped = strip_mod.strip(text)
    return L0Context(law=law, repo=law_root, parsed=parsed, stripped=stripped, index=None, frozen=frozen,
                     spec_digest="sha256:" + "0" * 64, meta={}, manifest=manifest, inactive={}, url_re=gate_stage.URL_RE,
                     slot_enum=tuple(SLOT_ENUM))


def test_stop_shape_is_active_with_real_manifest(law, run_root) -> None:
    prepared(run_root, law)
    manifest = read_json(os.path.join(run_root, "30-figures", "assets", "manifest.json"))
    frozen = read_json(os.path.join(run_root, "15-frozen", "material-spec.v1.json"))
    # 읽기만 · fig 전부 none 인 판 = 1회차(런 -3 v2 는 T65 ③ 회차 2 로 도면 헤더가 붙어 rounds/r1 에 보존됐다 — 875d7a9 뒤 낡은 경로 정정 · T67 ②)
    text = read(os.path.join(os.path.dirname(RUN3_V2_THREAD), "rounds", "r1", "thread.annotated.md"))
    rule = {r.id: r for r in load_rules_from_law(L0Law.load(law))}["format.stop-shape"]
    res = rule.run(context_for(text, law, manifest, frozen))
    stops = [t.n for t in parse_mod.parse(text, slot_enum=SLOT_ENUM).tweets if t.slot in ("stop", "pivot")]
    if res.row.checked != len(stops) or sorted(d["locus"]["tweet"] for d in res.defects) != sorted(stops):
        pytest.fail(f"fig none 인 스톱 전부가 자산 0 으로 실패하지 않았다: checked={res.row.checked} defects={[d['locus']['tweet'] for d in res.defects]}")
    if "inactive_reason" in res.row.extras:
        pytest.fail("매니페스트가 있는데 미가동 표지가 남았다")
    # T2 헤더에 fig-02 + 본문 두 문장 → pass · 세 문장 → fail
    lines = text.split("\n")
    idx = next(i for i, line in enumerate(lines) if line.startswith("## T2 "))
    lines[idx] = "## T2 {slot: stop, fig: fig-02}"
    body_end = next(i for i in range(idx + 1, len(lines)) if lines[i].strip() == "")
    two = lines[:idx + 1] + lines[idx + 1:idx + 3] + lines[body_end:]
    res2 = rule.run(context_for("\n".join(two), law, manifest, frozen))
    if 2 in [d["locus"]["tweet"] for d in res2.defects]:
        pytest.fail(f"자산 1 · 문장 2 인 T2 가 통과하지 않았다: {[d for d in res2.defects if d['locus']['tweet'] == 2]}")
    three = lines[:idx + 1] + lines[idx + 1:idx + 4] + lines[body_end:]
    if len(three[idx + 1:idx + 4]) != 3:
        pytest.fail("표본 T2 에 문장 3 개가 없다")
    res3 = rule.run(context_for("\n".join(three), law, manifest, frozen))
    hit = [d for d in res3.defects if d["locus"]["tweet"] == 2]
    if not hit or "sentences=3" not in hit[0]["observed"]:
        pytest.fail(f"문장 3 인 T2 가 실패하지 않았다: {hit}")
    # 매니페스트 없이 gate.run → inactive_layers 에 stop-shape 가 있고, 있으면 없다
    contract = load_stage_contract("gate", law)
    _block, inactive = gate_stage.inactive_layers(contract)
    if any(row["layer"] == "format.stop-shape" for row in inactive):
        pytest.fail("계약 layers 가 stop-shape 를 아직 inactive 로 적는다")
    digest = run_digest(run_root)
    drafts = {"v2": draft_for("v2", run_root)}
    run_a = make_run(os.path.join(os.path.dirname(os.path.dirname(run_root)), "nomanifest"), drafts=drafts)
    outcome = gate_stage.run(run_root=run_a, repo=law)
    verdict = read_json(os.path.join(run_a, "50-gate", "v2", "verdict.json"))
    if not any(row["layer"] == "format.stop-shape" for row in verdict["inactive_layers"]):
        pytest.fail(f"매니페스트 없는 런의 verdict 에 stop-shape 미가동 행이 없다: {verdict['inactive_layers']}")
    figures_stage.select(run_root, law)
    selection = read_json(os.path.join(run_root, "30-figures", "selection.json"))
    path = os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(draft_for("v2", run_root, headers=headers_from_selection(selection)))
    outcome = gate_stage.run(run_root=run_root, repo=law)
    verdict = read_json(os.path.join(run_root, "50-gate", "v2", "verdict.json"))
    if any(row["layer"] == "format.stop-shape" for row in verdict["inactive_layers"]) or digest != verdict["spec_digest"]:
        pytest.fail(f"매니페스트 있는 런의 verdict 가 stop-shape 를 미가동으로 적었다: {verdict['inactive_layers']}")
    stop_row = next(row for row in verdict["checks"] if row["check_id"] == "format.stop-shape")
    if stop_row["checked"] == 0 or stop_row["vacuous"] != "none":
        pytest.fail(f"가동 stop-shape 행이 공허하다: {stop_row}")
    images = read_json(os.path.join(run_root, "50-gate", "v2", "thread.json"))["images"]
    if not images or any(image["asset_path"] is None for image in images):
        pytest.fail(f"thread.json#images 의 asset_path 가 매니페스트로 해소되지 않았다: {images[:2]}")


# ---------------------------------------------------------------------------
# ⑫ 순번 토크나이저 · 골든 rc-0008 · rc-0001 불변
# ---------------------------------------------------------------------------


def test_thread_marker_tokenizer_matches_golden_rc0008_and_whitelist() -> None:
    numeric = L0Law.load(REPO).block("numeric")
    tokenizers = rules_numeric.load_tokenizers(numeric)
    if tokenizers[0][0] != 0 or tokenizers[0][1] != "thread-marker" or len(tokenizers) != 12:
        pytest.fail(f"rank 0 thread-marker 가 맨 앞이 아니거나 토큰화 12종이 아니다: {[(r, k) for r, k, _ in tokenizers]}")
    if numeric["normalization"].get("thread_marker") is None or str(numeric["tokenizer_amendments"][-1]["at"]) != "2026-09-13":
        pytest.fail("normalization.thread_marker · tokenizer_amendments 2026-09-13 행이 없다")
    aliases = dict(numeric["normalization"]["unit_aliases"])
    golden = read_json(GOLDEN_0008)
    pattern = re.compile(golden["whitelist_pattern"])
    legacy = re.compile(golden["whitelist_legacy_pattern"])
    for sample in golden["samples"]:
        tokens = [[kind, raw] for _s, _e, kind, raw in rules_numeric.tokenize(sample["text"], tokenizers)]
        keys = [key for _s, _e, kind, raw in rules_numeric.tokenize(sample["text"], tokenizers) for key in rules_numeric.keys_of(kind, raw, aliases)]
        if tokens != sample["expect_tokens"] or keys != sample["expect_keys"]:
            pytest.fail(f"{sample['id']}: 실측 {tokens} {keys} ≠ 골든 {sample['expect_tokens']} {sample['expect_keys']}")
        passes = any(pattern.fullmatch(key) for key in keys)
        legacy_passes = any(legacy.fullmatch(key) for key in keys)
        if passes != sample["whitelist_pass"] or legacy_passes != sample["whitelist_legacy_pass"]:
            pytest.fail(f"{sample['id']}: 화이트리스트 통과 실측 {passes}/{legacy_passes} ≠ 골든 {sample['whitelist_pass']}/{sample['whitelist_legacy_pass']}")
    # 과광화 표본이 골든에 정직하게 있다(1/2 inch → 순번)
    if not any(s["id"] == "tm-04" and s["expect_tokens"] == [["thread-marker", "1/2"]] and s["whitelist_pass"] for s in golden["samples"]):
        pytest.fail("골든이 알려진 과광화(1/2 inch)를 적지 않았다")
    cases = [json.loads(line) for line in read(os.path.join(REPO, "ledgers", "regression", "cases.jsonl")).splitlines() if line.strip()]
    if not any(c["case_id"] == "rc-0008" and c["expect"]["must_detect"] is False for c in cases):
        pytest.fail("cases.jsonl 에 rc-0008 행이 없다")


def test_golden_rc0001_still_passes_every_rule_with_new_tokenizer(tmp_path) -> None:
    run_root = os.path.join(str(tmp_path), "runs", "example-xx0000000a1-cable-guide")
    frozen_dir = os.path.join(run_root, "15-frozen")
    os.makedirs(frozen_dir)
    frozen = os.path.join(frozen_dir, "material-spec.v1.json")
    shutil.copyfile(os.path.join(GOLDEN_0001, "material-spec.frozen.json"), frozen)
    os.chmod(frozen, 0o444)
    digest = sha256_file(frozen)
    meta = {"schema": "run/v0", "run_id": "example-xx0000000a1-cable-guide", "status": "active", "run_kind": "partial",
            "partial_until": "gate", "engine": {"commit": "e" * 40, "worktree": None}, "numeric_whitelist": [],
            "frozen": [{"spec_version": 1, "path": "15-frozen/material-spec.v1.json", "spec_digest": digest}]}
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    blueprint = read_json(os.path.join(GOLDEN_0001, "blueprint.json"))
    blueprint["spec_digest"] = digest
    write_json(os.path.join(run_root, "20-design", "blueprint.json"), blueprint)
    text = re.sub(r"spec_digest: sha256:[0-9a-f]{64}", f"spec_digest: {digest}", read(GOLDEN_THREAD), count=1)
    path = os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")
    os.makedirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    outcome = gate_stage.run(run_root=run_root, repo=REPO)
    state = outcome["variants"]["v2"]
    if not state["l0_pass"] or state["defects"] != 0:
        pytest.fail(f"골든 rc-0001 이 새 토큰화 아래에서 통과하지 않는다: {state}")
    verdict = read_json(os.path.join(run_root, "50-gate", "v2", "verdict.json"))
    numeric_row = next(row for row in verdict["checks"] if row["check_id"] == "numeric.exhaustive")
    if numeric_row["checked"] != 0 or numeric_row["vacuous"] != "empty-target":
        pytest.fail(f"rc-0001 numeric.exhaustive 기대 행이 바뀌었다: {numeric_row}")


# ---------------------------------------------------------------------------
# ⑬ compose 2회차 · ⑭ fig-selection 불일치
# ---------------------------------------------------------------------------


def _round_one(law: str, run_root: str) -> dict:
    """1회차 확정본 3판 + 토너먼트 행 3 + 도면 자산층(prepare·select). 반환 = selection."""
    prepared(run_root, law)
    figures_stage.select(run_root, law)
    for variant in ("v1", "v2", "v3"):
        path = os.path.join(run_root, "40-compose", variant, "thread.annotated.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(draft_for(variant, run_root))
    rows = []
    for pen in compose_stage.registry.pens(law):
        rows.append({"variant": pen["variant"], "pen": compose_stage.registry.pen_assignment(pen), "comparison_axis": "effort",
                     "taste_weight": "low", "spec_version": 1, "spec_digest": run_digest(run_root), "recorded_at": "2026-09-13T09:42:30Z",
                     "outcome": "drafted"})
    with open(os.path.join(run_root, "40-compose", "tournament-rows.jsonl"), "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return read_json(os.path.join(run_root, "30-figures", "selection.json"))


def test_compose_round_two_preserves_previous_and_attaches_figures(law, run_root) -> None:
    selection = _round_one(law, run_root)
    before = {v: read(os.path.join(run_root, "40-compose", v, "thread.annotated.md")) for v in ("v1", "v2", "v3")}
    with pytest.raises(StageError, match="대상 변주"):
        compose_stage.run(run_root=run_root, repo=law, round_no=2)
    outcome = compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=2)
    if outcome["status"] != "pending" or outcome["pending"] != ["compose-r2/v2/batch-0"]:
        pytest.fail(f"회차 2 요청 좌표가 compose-r2/v2/batch-0 이 아니다: {outcome['status']} {outcome['pending']}")
    lane_dir = os.path.join(run_root, "40-compose", "lanes", "compose-r2", "v2", "batch-0")
    request = read_json(os.path.join(lane_dir, "request.json"))
    if "30-figures/selection.json" not in request["slices"] or "30-figures/assets/manifest.json" not in request["slices"]:
        pytest.fail(f"요청서 원천 조각에 selection·manifest 가 없다: {list(request['slices'])}")
    rendered = read(os.path.join(lane_dir, "request.md"))
    if "## 도면 헤더 — 트윗별 자산 표" not in rendered or "| T3 | `exhibit` | `fig-08` | `FIG-8` |" not in rendered \
            or "재정 T64 ④" in rendered or f"stop_shape.sentences_max` = `{SHEET['stop_shape_sentences_max']}`" not in rendered:
        pytest.fail("요청서에 트윗별 자산 표·문장 수 지시가 없거나 T64 ④ 블록이 남았다")
    if lint.lint_prompt(rendered, law):
        pytest.fail(f"회차 2 요청서가 린트를 통과하지 않는다: {lint.lint_prompt(rendered, law)}")
    lint_rows = [row for row in outcome["rows"] if row.check_id == lint.CHECK_ID]
    if len(lint_rows) != 2 or any(row.status != "pass" for row in lint_rows):
        pytest.fail("린트 행 2 가 pass 가 아니다")
    if os.path.isdir(os.path.join(run_root, "40-compose", "lanes", "compose-r2", "v1")):
        pytest.fail("대상 밖 변주의 요청서가 생겼다")
    new_text = draft_for("v2", run_root, headers=headers_from_selection(selection))
    respond(run_root, "compose-r2/v2/batch-0", {"thread_annotated_md": new_text})
    outcome = compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=2)
    if outcome["status"] != "ok" or outcome["variants"]["v2"]["status"] != "ok" or outcome["variants"]["v2"].get("round") != 2:
        pytest.fail(f"회차 2 확정이 ok 가 아니다: {outcome['status']} {outcome['variants']}")
    preserved = os.path.join(run_root, "40-compose", "v2", "rounds", "r1")
    if read(os.path.join(preserved, "thread.annotated.md")) != before["v2"] or not os.path.isfile(os.path.join(preserved, "response.json")) is False and False:
        pytest.fail("직전 판이 rounds/r1 에 바이트 그대로 보존되지 않았다")
    if read(os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")) != new_text:
        pytest.fail("새 판이 thread.annotated.md 에 쓰이지 않았다")
    for variant in ("v1", "v3"):
        if read(os.path.join(run_root, "40-compose", variant, "thread.annotated.md")) != before[variant] or os.path.isdir(os.path.join(run_root, "40-compose", variant, "rounds")):
            pytest.fail(f"{variant} 가 바뀌었다")
    report = read_json(os.path.join(run_root, "40-compose", "compose-report.json"))
    if report["rounds"].get("v2") != 2 or report["round"] != 2 or report["figures_attached"] is not True:
        pytest.fail(f"compose-report.json#rounds 가 다르다: {report.get('rounds')} {report.get('round')}")
    rows = tournament(run_root)
    if [(r["variant"], r["outcome"], r.get("round", 1)) for r in rows] != [("v1", "drafted", 1), ("v2", "drafted", 1), ("v3", "drafted", 1), ("v2", "redrafted", 2)] \
            or rows[-1]["reason"] != "figures attached (T65 ③)":
        pytest.fail(f"토너먼트 행이 다르다: {rows}")
    # 재진입은 보존 자리를 다시 만들지 않는다(멱등)
    outcome = compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=2)
    if outcome["status"] != "ok" or len(tournament(run_root)) != 4 or read(os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")) != new_text:
        pytest.fail("회차 2 재진입이 멱등이 아니다")
    # 회차 3 을 열면 rounds/r2 가 생긴다 · 자리가 이미 있으면 StageError
    outcome = compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=3)
    if outcome["pending"] != ["compose-r3/v2/batch-0"]:
        pytest.fail("회차 3 좌표가 다르다")
    os.makedirs(os.path.join(run_root, "40-compose", "v2", "rounds", "r2"))
    respond(run_root, "compose-r3/v2/batch-0", {"thread_annotated_md": new_text})
    with pytest.raises(StageError, match="덮어쓰지 않는다"):
        compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=3)


def test_header_fig_mismatch_with_selection_is_annotation_schema_finding(law, run_root) -> None:
    selection = _round_one(law, run_root)
    compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=2)
    wrong = dict(headers_from_selection(selection))
    wrong[2] = "fig-13"
    respond(run_root, "compose-r2/v2/batch-0", {"thread_annotated_md": draft_for("v2", run_root, headers=wrong)})
    outcome = compose_stage.run(run_root=run_root, repo=law, variants=("v2",), round_no=2)
    row = next(r for r in outcome["rows"] if r.check_id == "compose.annotation-syntax" and r.extras.get("variant") == "v2")
    if row.status != "fail" or row.findings[0].rule != "annotation.schema" or compose_stage.FIG_MISMATCH_LABEL not in row.findings[0].message \
            or row.extras["fig_selection_mismatch"] != [{"tweet": 2, "found": "fig-13", "expected": "fig-02"}]:
        pytest.fail(f"fig-selection 불일치가 annotation.schema finding 으로 나오지 않았다: {row.to_row_dict()} {[f.as_dict() for f in row.findings]} {row.extras}")
    if outcome["status"] != "pending" or outcome["pending"] != ["compose-r2/v2/retry-1/batch-0"]:
        pytest.fail(f"불일치가 retry 로 가지 않았다: {outcome['status']} {outcome['pending']}")
    if os.path.isdir(os.path.join(run_root, "40-compose", "v2", "rounds")):
        pytest.fail("실패한 판인데 직전 판을 옮겼다")
    # 1회차(선택 없는 런)에서는 fig 대조를 하지 않는다 — 검사 함수 직접
    parsed = parse_mod.parse(draft_for("v2", run_root, headers={1: "fig-13"}), slot_enum=SLOT_ENUM)
    if compose_stage.check_annotation_syntax(parsed, None).status != "pass":
        pytest.fail("선택 없이도 fig 대조를 했다")


# ---------------------------------------------------------------------------
# ⑮ gate 재판정 — rounds/r1 보존
# ---------------------------------------------------------------------------


def test_gate_rejudge_preserves_previous_verdict_in_rounds(law, run_root) -> None:
    selection = _round_one(law, run_root)
    outcome = gate_stage.run(run_root=run_root, repo=law, variants=["v2"])
    first = read_json(os.path.join(run_root, "50-gate", "v2", "verdict.json"))
    path = os.path.join(run_root, "40-compose", "v2", "thread.annotated.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(draft_for("v2", run_root, headers=headers_from_selection(selection)))
    outcome = gate_stage.run(run_root=run_root, repo=law, variants=["v2"])
    state = outcome["variants"]["v2"]
    preserved = os.path.join(run_root, "50-gate", "v2", "rounds", "r1")
    if state.get("reentered") or not state.get("preserved_previous", "").endswith("50-gate/v2/rounds/r1"):
        pytest.fail(f"재판정이 직전 산출을 옮기지 않았다: {state}")
    if read_json(os.path.join(preserved, "verdict.json")) != first or not os.path.isfile(os.path.join(preserved, "thread.stripped.md")):
        pytest.fail("rounds/r1 의 verdict 가 직전 판정과 다르거나 strip 산출이 없다")
    second = read_json(os.path.join(run_root, "50-gate", "v2", "verdict.json"))
    if second["thread_digest"] == first["thread_digest"]:
        pytest.fail("새 판정의 주석본 지문이 바뀌지 않았다")
    outcome = gate_stage.run(run_root=run_root, repo=law, variants=["v2"])
    if not outcome["variants"]["v2"].get("reentered") or os.path.isdir(os.path.join(run_root, "50-gate", "v2", "rounds", "r2")):
        pytest.fail("같은 지문 재진입이 또 옮겼다")


# ---------------------------------------------------------------------------
# ⑯ 구동기
# ---------------------------------------------------------------------------


class PenStub:
    """`claude -p` json 출력 흉내 — 좌표의 변주에 맞는 초안(선택과 같은 헤더)을 낸다."""

    def __init__(self, run_root: str, headers: dict[int, str]):
        self.run_root = run_root
        self.headers = headers
        self.calls: list[list[str]] = []

    def __call__(self, argv, stdin, env, timeout):
        self.calls.append(list(argv))
        text = stdin.decode("utf-8")
        lane_id = text.split("\n", 1)[0].replace("# 레인 요청 — ", "").strip()
        digest = next(line for line in text.split("\n") if line.startswith("| 입력 지문 | `")).split("`")[1]
        variant = lane_id.split("/")[1]
        observed = argv[argv.index("--model") + 1]
        payload = {"thread_annotated_md": draft_for(variant, self.run_root, headers=self.headers)}
        body = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "duration_ms": 3, "total_cost_usd": 0.0,
                "session_id": "stub", "structured_output": {"lane_id": lane_id, "model": "self", "effort": "self", "input_digest": digest,
                                                             "payload": payload},
                "modelUsage": {observed: {"inputTokens": 1, "outputTokens": 9}}}
        return drv.ExecResult(0, json.dumps(body, ensure_ascii=False).encode(), b"", False, 3)


def _drive(law: str, run_root: str, evidence: str, *argv: str, executor=None, dry_run: bool = False):
    lines: list[str] = []
    head = ["--repo", law, "--run-root", run_root, "--evidence-dir", evidence]
    if dry_run:
        head.append("--dry-run")
    return drv.main([*head, *argv], executor=executor, out=lines.append), lines


def test_driver_figures_and_compose_round_two(law, run_root, tmp_path, monkeypatch) -> None:
    evidence = os.path.join(str(tmp_path), "evidence")
    if len(drv.COMMANDS) != 25 or drv.COMMANDS[11:15] != ("figures", "compose", "gate-l0", "strip"):
        pytest.fail(f"명령 25 가 아니다: {drv.COMMANDS}")
    parser = drv.build_parser()
    listed = tuple(parser._subparsers._group_actions[0].choices)  # noqa: SLF001
    if listed != drv.COMMANDS:
        pytest.fail(f"--help 목록이 COMMANDS 와 다르다: {listed}")
    # 렌더 환경 부재 → 2(진단)
    monkeypatch.setattr(render_mod, "environment_report", lambda repo: {"missing": ["node(PATH 에 없다)"], "node": None, "package": None, "playwright_pin": "1.49.1", "browser": None})
    code, lines = _drive(law, run_root, evidence, "figures", RUN_ID)
    if code != drv.EXIT_USAGE:
        pytest.fail(f"렌더 환경 부재가 2 가 아니다: {code} {lines}")
    monkeypatch.undo()
    # 가짜 렌더러를 NodeRenderer 자리에 — 실 브라우저 없이 figures 0
    fake = FakeRenderer()
    monkeypatch.setattr(render_mod.NodeRenderer, "__call__", lambda self, jobs, jobs_path: fake(jobs, jobs_path))
    code, lines = _drive(law, run_root, evidence, "figures", RUN_ID, dry_run=True)
    if code != drv.EXIT_OK or not lines[0].startswith("[dry-run] figures.prepare"):
        pytest.fail(f"figures dry-run: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "figures", RUN_ID)
    if code != drv.EXIT_OK or not os.path.isfile(os.path.join(run_root, "30-figures", "selection.json")) or not any(line.startswith("선택: 슬롯") for line in lines):
        pytest.fail(f"figures 명령: {code} {lines}")
    # 종료선 앞이면 13
    early = make_run(os.path.join(str(tmp_path), "e"), partial_until="design")
    code, _ = _drive(law, early, evidence, "figures", RUN_ID)
    if code != drv.EXIT_TERMINAL_FAIL:
        pytest.fail(f"종료선 앞 figures 가 13 이 아니다: {code}")
    # 1회차 확정본 3판(compose 스텁) → --round 2 는 --variant 필수(2) → --variant v2 --round 2 = 0 · 좌표 compose-r2
    selection = read_json(os.path.join(run_root, "30-figures", "selection.json"))
    stub = PenStub(run_root, headers_from_selection(selection))
    code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 3:
        pytest.fail(f"1회차 compose: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, "--round", "2", executor=stub)
    if code != drv.EXIT_USAGE:
        pytest.fail(f"--round 2 without --variant 가 2 가 아니다: {code} {lines}")
    code, lines = _drive(law, run_root, evidence, "compose", RUN_ID, "--variant", "v2", "--round", "2", executor=stub)
    if code != drv.EXIT_OK or len(stub.calls) != 4 or "--effort xhigh" not in " ".join(stub.calls[-1]):
        pytest.fail(f"compose --variant v2 --round 2: {code} {lines} calls={len(stub.calls)}")
    receipts = sorted(name for name in os.listdir(os.path.join(evidence, "calls")) if name.endswith(".json") and not name.endswith(".raw.json"))
    if "compose-r2__v2__batch-0.json" not in receipts:
        pytest.fail(f"회차 2 영수증이 없다: {receipts}")
    if not os.path.isfile(os.path.join(run_root, "40-compose", "v2", "rounds", "r1", "thread.annotated.md")):
        pytest.fail("구동기 회차 2 가 직전 판을 보존하지 않았다")
    code, lines = _drive(law, run_root, evidence, "gate-l0", RUN_ID, "--variant", "v2")
    if code != drv.EXIT_OK or not any(line.startswith("v2: l0 ") for line in lines):
        pytest.fail(f"gate-l0: {code} {lines}")
    code, _ = _drive(law, run_root, evidence, "seal", RUN_ID)
    manifest = read(os.path.join(evidence, "MANIFEST-sha256.txt")).splitlines()
    rels = [line.split("  ", 1)[1] for line in manifest]
    for needle in ("30-figures/assets/manifest.json", "30-figures/selection.json", "40-compose/v2/rounds/r1/thread.annotated.md", "30-figures/assets/fig-01.png"):
        if not any(rel.endswith(needle) for rel in rels):
            pytest.fail(f"seal 에 {needle} 이 없다")
    code, lines = _drive(law, run_root, evidence, "lanes", RUN_ID)
    if code != drv.EXIT_OK or not any("compose-r2/v2/batch-0" in line for line in lines):
        pytest.fail(f"lanes 가 회차 좌표를 보이지 않는다: {lines}")


# ---------------------------------------------------------------------------
# ⑰ 실 브라우저 스모크 — PD_REAL_RENDER=1 일 때만
# ---------------------------------------------------------------------------


@pytest.mark.skipif(os.environ.get("PD_REAL_RENDER") != "1", reason="실 브라우저 스모크는 PD_REAL_RENDER=1 일 때만(총괄이 켠다)")
def test_real_render_smoke_produces_2400x1350(law, run_root) -> None:
    # 법 사본은 node_modules 를 복사하지 않는다(픽스처 크기) — 리포의 설치본을 링크해 쓴다(핀 대조는 environment_report 가 한다).
    installed = os.path.join(REPO, "studio", "renderer", "node_modules")
    linked = os.path.join(law, "studio", "renderer", "node_modules")
    if os.path.isdir(installed) and not os.path.exists(linked):
        os.symlink(installed, linked)
    report = render_mod.environment_report(law)
    if report["missing"]:
        pytest.fail(f"렌더 환경이 없다: {report['missing']}")
    outcome = figures_stage.prepare(run_root, law)
    if outcome["status"] != "ok":
        pytest.fail(f"실 렌더 prepare 가 ok 가 아니다: {outcome['status']} {outcome['reason_label']}")
    sizes = {name: render_mod.png_size(os.path.join(run_root, "30-figures", "assets", name))
             for name in os.listdir(os.path.join(run_root, "30-figures", "assets")) if name.endswith(".png")}
    if set(sizes.values()) != {(2400, 1350)}:
        pytest.fail(f"실 렌더 치수가 2400×1350 이 아니다: {sizes}")
    sys.stderr.write(f"[real-render] {len(sizes)} assets · {sorted(set(sizes.values()))} · playwright {report['package']} · {report['node']}\n")
