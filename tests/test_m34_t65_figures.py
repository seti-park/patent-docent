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

GOLDEN_THREAD = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless", "thread.annotated.md")
GOLDEN_0001 = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless")
GOLDEN_0008 = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0008-thread-marker-counterexamples", "samples.json")
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
FIXTURES = os.path.join(REPO, "tests", "fixtures", "schema-enforcement")
LAW_TREES = ("contracts", "reader", "studio")
LAW_FILES = (("docs", "CHARTER.md"), ("engine", "procedure", "design.md"), ("engine", "pens", "prompt-template.md"))


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


def tournament(run_root: str) -> list[dict]:
    path = os.path.join(run_root, "40-compose", "tournament-rows.jsonl")
    return [json.loads(line) for line in read(path).splitlines() if line.strip()] if os.path.isfile(path) else []


@pytest.fixture
def law(tmp_path) -> str:
    return make_law(os.path.join(str(tmp_path), "law"))


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


# ---------------------------------------------------------------------------
# ⑷ 재진입 — 자산 보존 · 없는 것만 더함
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑸ render-spec 위반 → retry(1) → halt
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑹ 원본 누락 → asset-completeness fail → escalate 누락 목록
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑹-b 재정 T66 ① — 동결본 raw_path 부재 시 source-report 도면 번호 유일 일치로 해소(재료 무변경)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑺ 원천 지문 불일치 → 환경 오류 · ⑧ 렌더 환경 부재
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑨ select
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑩ 트윗 자산 5 → selection-resolve fail(시트 값)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑪ stop-shape 가동 — 실제 manifest + 런 -3 v2 주석본
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# ⑮ gate 재판정 — rounds/r1 보존
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑯ 구동기
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# ⑰ 실 브라우저 스모크 — PD_REAL_RENDER=1 일 때만
# ---------------------------------------------------------------------------

