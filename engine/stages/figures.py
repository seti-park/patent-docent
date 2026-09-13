# -*- coding: utf-8 -*-
"""`figures` 스테이지 — `prepare`(전량 크롭 프레이밍 · 결정론 도구) / `select`(블루프린트 figure_plan 의 포인터 사영).

계약 = `contracts/stages/figures.yaml`(정본 서술 = SPEC §1.8 · §6.6 · §7.5 · 재정 R11 · 재정 2026-09-13 T65 ③).

`prepare(run_root, repo, renderer=None)`
  ① 진입 — 종료선(`partial_until`) · `figures.input-digest`(동결본 + 원천 도면 변경 감지 · P-U2). 자산 디렉터리가
     이미 있고 매니페스트 항목 수 == 동결본 `figures[]` 수면 **재진입 ok**(자산 삭제·덮어쓰기 금지 §7.5 — 모자라면
     없는 것만 더한다).
  ② 동결본 `figures[]` 마다 `FIG-n` → 자산 id `fig-NN` · 원본 실재 + sha256. 복합 시트(총괄 재량 ⓑ): 둘 이상의 FIG 가
     같은 raw_path 를 가리키면 각 FIG 가 같은 원본의 전장 프레이밍을 자기 자산으로 갖고 `edits[]` 에
     `{op: composite-sheet, shares_with: [...]}` 를 적는다.
  ③ 템플릿 `studio/templates/crop-only.html` 에 원본 바이트를 base64 로 인라인해 `assets/.render/fig-NN.html` 로 쓰고
     렌더러를 **한 번** 부른다(기본 = `node studio/renderer/render.mjs <jobs.json>` · 시험 = 가짜 렌더러).
  ④ 산출 PNG 치수 = IHDR 2400×1350(`figures.render-spec`) · `manifest.json`(figures-manifest/v0 · §7.5 10키 + asset_id ·
     source_sha256 — 재량 ⓒ).
  ⑤ 검사 3(`figures.asset-completeness` · `figures.render-spec` · `figures.manifest-parity`) → 실패표대로(일부 렌더 실패
     `retry(1)` → `escalate` 누락 목록 · render-spec `retry(1)` → `halt`).
  ⑥ `30-figures/figures-report.json`.

`select(run_root, repo)`
  블루프린트 `figure_plan[]` → `selection.json`(figures-selection/v0 · 슬롯 = `{tweet, asset, role}` · T1 첫 자산 = hero ·
  나머지 exhibit). 검사 3(`figures.selection-resolve` · `figures.no-copy` · `figures.publish-gate`) → 실패표대로. 교정 원장 행은
  런 안 `30-figures/corrections-rows.md`(총괄 재량 ⓓ — `ledgers/corrections.md` 의 쓰기 소유는 `ship` · §1.17).

★ 시트 값·검사 id·조치 어휘를 여기 리터럴로 두지 않는다 — 시트·계약에서 읽는다. `00-source/**`·`15-frozen/**`·
`20-design/**` 에는 쓰지 않는다. 렌더가 원천 디렉터리를 열지 않는다(러너가 바이트를 인라인한다).
"""

from __future__ import annotations

import base64
import datetime as _dt
import json
import os
import re
from typing import Callable

from reader.lib.report import CheckRow

from . import (
    StageEnvironmentError,
    StageError,
    StageHaltError,
    failure_entry,
    findings_of,
    load_json,
    load_yaml,
    rows_to_dicts,
    sha256_bytes,
    sha256_file,
    verify_declared_inputs,
    write_json,
    write_text,
)
from .design import latest_frozen, terminus_index
from ..figures import ASSET_EXT, asset_id_for_figure, asset_id_of, figure_id_of, manifest_items
from ..figures import render as render_mod
from ..paths import RunPaths, load_format_parameters, repo_root, run_kinds_contract

STAGE_ID = "figures"
STEP_PREPARE = "figures.prepare"
STEP_SELECT = "figures.select"
MANIFEST_SCHEMA = "figures-manifest/v0"
SELECTION_SCHEMA = "figures-selection/v0"
EDIT_CLASS_CROP = "crop-only"
ROLE_HERO = "hero"
ROLE_EXHIBIT = "exhibit"
OP_COMPOSITE = "composite-sheet"
OP_CROP = "crop-only-framing"
RETRY_RE = re.compile(r"^retry\((\d+)\)$")
ASSET_FILE_RE = re.compile(r"^fig-[0-9]{2,}(?:\.r[1-9][0-9]*)?\.png$")
#: 자산 id 문법(선택 포인터의 no-copy 판정) — 경로 구분자·data URI 가 들어올 자리가 없다.
ASSET_ID_RE = re.compile(r"^fig-[0-9]{2,}(?:\.r[1-9][0-9]*)?$")

CHECK_ENTRY = "figures.input-digest"
CHECK_COMPLETENESS = "figures.asset-completeness"
CHECK_RENDER_SPEC = "figures.render-spec"
CHECK_PARITY = "figures.manifest-parity"
CHECK_SELECTION = "figures.selection-resolve"
CHECK_PUBLISH = "figures.publish-gate"
CHECK_NO_COPY = "figures.no-copy"

MIME_BY_EXT = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
               ".svg": "image/svg+xml", ".tif": "image/tiff", ".tiff": "image/tiff"}

Renderer = Callable[[list[dict], str], list[dict]]


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_terminus(meta: dict, repo: str, contract: dict) -> None:
    if meta.get("run_kind") != "partial":
        return
    until = str(meta.get("partial_until", ""))
    if terminus_index(repo, until) < terminus_index(repo, STAGE_ID):
        entry = failure_entry(contract, "partial_until 종료선")
        raise StageHaltError(
            f"[{entry.get('action')}] partial_until={until!r} 은 figures 앞의 종료선이다 — "
            f"{entry.get('note')}. 연장 봉투(extension-envelope/v0)로 종료선을 옮긴 뒤 다시 부른다"
        )


def _frozen_figures(frozen: dict) -> list[dict]:
    out = [figure for figure in (frozen.get("figures") or []) if isinstance(figure, dict) and figure.get("id")]
    if not out:
        raise StageError("동결본 figures[] 가 비어 있다 — 도면 없는 재료로는 자산층을 만들지 않는다(source.exhibit-candidates 가 먼저다)")
    return out


def _data_uri(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mime = MIME_BY_EXT.get(ext, "application/octet-stream")
    with open(path, "rb") as handle:
        blob = handle.read()
    return f"data:{mime};base64," + base64.b64encode(blob).decode("ascii")


def _asset_files(assets_dir: str) -> list[str]:
    if not os.path.isdir(assets_dir):
        return []
    return sorted(name for name in os.listdir(assets_dir) if ASSET_FILE_RE.match(name) and os.path.isfile(os.path.join(assets_dir, name)))


def _load_manifest(path: str) -> dict | None:
    if not os.path.isfile(path):
        return None
    manifest = load_json(path)
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA:
        raise StageError(f"매니페스트가 {MANIFEST_SCHEMA} 가 아니다: {path}")
    return manifest


def _terminal(contract: dict, needle: str) -> tuple[str, int]:
    """실패표 행 → (종단 조치, 재시도 예산)."""
    entry = failure_entry(contract, needle)
    action = str(entry.get("action", ""))
    match = RETRY_RE.match(action)
    if match:
        return str(entry.get("then", "escalate")), int(match.group(1))
    return action, 0


def _report_path(paths: RunPaths) -> str:
    return paths.figures_report_json


def _write_report(paths: RunPaths, step: str, *, status: str, rows: list[CheckRow], extra: dict) -> dict:
    """`30-figures/figures-report.json` — 단계별 블록을 합친다(prepare 가 쓰고 select 가 더한다)."""
    path = _report_path(paths)
    report = load_json(path) if os.path.isfile(path) else {"stage": STAGE_ID, "steps": {}}
    if not isinstance(report, dict):
        report = {"stage": STAGE_ID, "steps": {}}
    steps = report.setdefault("steps", {})
    steps[step] = {"status": status, "rows": rows_to_dicts(rows), "findings": findings_of(rows),
                   "extras": {row.check_id: row.extras for row in rows if row.extras}, **extra}
    report["status"] = status
    report["rows"] = [row for block in steps.values() for row in block.get("rows", [])]
    report["findings"] = [finding for block in steps.values() for finding in block.get("findings", [])]
    write_json(path, report)
    return report


# ---------------------------------------------------------------------------
# prepare — 검사 3
# ---------------------------------------------------------------------------


def check_asset_completeness(figures: list[dict], assets_dir: str, *, missing_raw: list[str], failed_render: list[str],
                             rejected: set[str] | None = None) -> CheckRow:
    """`rejected` = 파일은 있으나 치수 위반으로 받아들이지 않은 자산 id(매니페스트 밖 · 사료)."""
    row = CheckRow(check_id=CHECK_COMPLETENESS, checked=len(figures))
    for figure in figures:
        figure_id = str(figure["id"])
        asset = asset_id_for_figure(figure_id)
        path = os.path.join(assets_dir, asset + ASSET_EXT)
        if figure_id in missing_raw:
            row.add("asset.source-missing", figure_id, str(figure.get("raw_path")), "00-source/figures-raw/ 의 실재 파일",
                    "동결본이 가리키는 원본 도면이 없다 — 편집할 원천이 없어 자산을 만들 수 없다")
        elif not os.path.isfile(path) or asset in (rejected or set()):
            reason = "렌더 실패" if figure_id in failed_render else "자산 파일 부재"
            row.add("asset.missing", figure_id, "(파일 없음)", f"30-figures/assets/{asset}.png", f"{reason} — 전량 편집이 완결되지 않았다(D12)")
    row.extras["missing"] = [finding.locus for finding in row.findings]
    return row


def check_render_spec(assets_dir: str, names: list[str]) -> CheckRow:
    width, height = render_mod.expected_pixels()
    row = CheckRow(check_id=CHECK_RENDER_SPEC, checked=len(names))
    sizes: dict[str, list[int]] = {}
    for name in names:
        path = os.path.join(assets_dir, name)
        try:
            actual = render_mod.png_size(path)
        except (OSError, StageError) as exc:
            row.add("render.unreadable", name, str(exc)[:80], "PNG IHDR", "자산 PNG 를 읽지 못했다")
            continue
        sizes[name] = list(actual)
        if actual != (width, height):
            row.add("render.size", name, f"{actual[0]}x{actual[1]}", f"{width}x{height}",
                    "자산 픽셀 치수가 1200×675 @2x 가 아니다 — 렌더 뷰포트·배율을 확인하라(SPEC §6.6)")
    row.extras["sizes"] = sizes
    row.extras["expected"] = [width, height]
    return row


def check_manifest_parity(manifest: dict, figures: list[dict], assets_dir: str, rejected: set[str] | None = None) -> CheckRow:
    """`rejected` = 치수 위반으로 매니페스트 밖에 남은 파일의 자산 id(항목 수 대조에서 뺀다 — 그 위반은 render-spec 행의 몫)."""
    items = manifest_items(manifest)
    files = [name for name in _asset_files(assets_dir) if name[: -len(ASSET_EXT)] not in (rejected or set())]
    row = CheckRow(check_id=CHECK_PARITY, checked=max(len(items), 1))
    if len(items) != len(files):
        row.add("parity.count", "manifest.json#items", str(len(items)), str(len(files)), "매니페스트 항목 수와 자산 파일 수가 다르다")
    known = {str(figure["id"]) for figure in figures}
    seen_assets: set[str] = set()
    for index, item in enumerate(items):
        locus = f"items[{index}]"
        figure_id = figure_id_of(item)
        if figure_id not in known:
            row.add("parity.figure-id", locus, str(figure_id), "동결본 figures[].id", "매니페스트 항목이 동결본 도면으로 해소되지 않는다")
        asset = asset_id_of(item)
        if not asset or asset + ASSET_EXT not in files:
            row.add("parity.asset-file", locus, str(asset), "30-figures/assets/ 의 파일", "항목이 가리키는 자산 파일이 없다")
        if asset in seen_assets:
            row.add("parity.asset-duplicate", locus, str(asset), "유일한 자산 id", "같은 자산 id 항목이 둘이다")
        seen_assets.add(str(asset))
        for key in ("edit_class", "publishable"):
            if key not in item:
                row.add(f"parity.{key}", locus, "(없음)", key, f"항목에 {key} 가 없다(재정 R11 필수 필드)")
    return row


# ---------------------------------------------------------------------------
# prepare
# ---------------------------------------------------------------------------


def _plan_items(figures: list[dict], paths: RunPaths, missing_raw: list[str]) -> list[dict]:
    """동결본 도면 → 렌더 계획 행(자산 id · 원본 · 복합 시트 관계). 원본이 없는 도면은 계획에서 뺀다."""
    by_raw: dict[str, list[str]] = {}
    for figure in figures:
        by_raw.setdefault(str(figure.get("raw_path", "")), []).append(str(figure["id"]))
    plan: list[dict] = []
    for figure in figures:
        figure_id = str(figure["id"])
        if figure_id in missing_raw:
            continue
        raw = str(figure.get("raw_path", ""))
        shares = [other for other in by_raw.get(raw, []) if other != figure_id]
        edits = [{"op": OP_CROP, "template": render_mod.TEMPLATE_ID, "note": "전장 프레이밍 · 오버레이 없음"}]
        if shares:
            edits.append({"op": OP_COMPOSITE, "shares_with": shares,
                          "note": "복합 시트 — 같은 원본의 전장 프레이밍 · 하위 크롭 상자는 사용권 재정 뒤(총괄 재량 ⓑ)"})
        plan.append({"figure_id": figure_id, "asset_id": asset_id_for_figure(figure_id), "raw_path": raw,
                     "raw_abs": paths.absolute(raw), "edits": edits})
    return plan


def pending_ids(pending: list[dict]) -> set[str]:
    return {item["asset_id"] for item in pending}


def _render_batch(plan: list[dict], paths: RunPaths, template: str, renderer: Renderer) -> tuple[list[str], list[str]]:
    """계획 행 전량을 한 번에 렌더. 반환 = (성공 자산 id, 실패 자산 id)."""
    paths.ensure_figures_dirs()
    jobs: list[dict] = []
    for item in plan:
        html_path = os.path.join(paths.figures_render_dir, item["asset_id"] + ".html")
        write_text(html_path, render_mod.fill_template(template, _data_uri(item["raw_abs"])))
        jobs.append({"html": html_path, "out": paths.figure_asset(item["asset_id"]), "asset_id": item["asset_id"]})
    results = renderer(jobs, os.path.join(paths.figures_render_dir, "jobs.json"))
    ok_outs = {str(record.get("out")) for record in results if record.get("ok") is True}
    done = [job["asset_id"] for job in jobs if job["out"] in ok_outs and os.path.isfile(job["out"])]
    failed = [job["asset_id"] for job in jobs if job["asset_id"] not in done]
    return done, failed


def prepare(run_root: str, repo: str | None = None, renderer: Renderer | None = None) -> dict:
    """`figures.prepare` 1회 진입. 반환 = `{status, rows, manifest, missing, attempts, reason_label}`."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)

    # ① 진입
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID, inputs={"spec_version": version})
    missing_raw = list(entry_row.extras.get("missing_raw") or [])
    verified_raw = dict(entry_row.extras.get("verified_raw") or {})
    frozen = load_json(paths.frozen_spec(version))
    figures = _frozen_figures(frozen)
    assets_dir = paths.figures_assets_dir
    manifest_path = paths.figures_manifest_json
    manifest = _load_manifest(manifest_path)
    run_id = str(meta.get("run_id", ""))
    pin = render_mod.playwright_pin(repo)

    existing: dict[str, dict] = {}
    if manifest is not None:
        if str(manifest.get("spec_digest", "")) != spec_digest:
            raise StageError("기존 매니페스트가 다른 재료 판 위에 서 있다 — 재료 개정 뒤의 자산층은 새 판(fig-NN.r2.png)으로 더한다(§7.5 · 재정 N11)")
        for item in manifest_items(manifest):
            existing[str(figure_id_of(item))] = item
    stray = [name for name in _asset_files(assets_dir) if not any(asset_id_of(item) + ASSET_EXT == name for item in existing.values())]
    if stray:
        raise StageError(f"매니페스트에 없는 자산 파일이 있다 — 덮어쓰지 않는다(§7.5): {stray}")

    todo = [figure for figure in figures if str(figure["id"]) not in existing and str(figure["id"]) not in missing_raw]
    plan = _plan_items([figure for figure in figures if str(figure["id"]) in {str(f["id"]) for f in todo}], paths, missing_raw)
    renderer = renderer or render_mod.NodeRenderer(repo)
    env_report = None

    # ③ 렌더(없는 것만). 실패표 두 행이 여기 한 루프에 겹친다 — 「일부 도면 렌더 실패」 retry(1) → escalate ·
    #    「figures.render-spec 위반」 retry(1) → halt. 재시도 대상 = 실패분 + 치수가 틀린 분(§7.5 의 덮어쓰기 금지는
    #    매니페스트에 오른 자산의 규율이다 — 아직 받아들이지 않은 렌더 출력은 자산이 아니라 시도다).
    done_all: list[str] = []
    failed: list[str] = []
    wrong_size: list[str] = []
    attempts = 0
    if plan:
        env_report = render_mod.environment_report(repo) if renderer.__class__ is render_mod.NodeRenderer else {"fake": True}
        template = render_mod.template_text(repo)
        _terminal_render, budget_fail = _terminal(contract, "일부 도면 렌더 실패")
        _terminal_spec, budget_spec = _terminal(contract, "figures.render-spec 위반")
        expected = render_mod.expected_pixels()
        pending = list(plan)
        while pending:
            attempts += 1
            done, failed = _render_batch(pending, paths, template, renderer)
            wrong_size = []
            for asset in done:
                try:
                    if render_mod.png_size(paths.figure_asset(asset)) != expected:
                        wrong_size.append(asset)
                except StageError:
                    wrong_size.append(asset)
            done_all = [asset for asset in done_all if asset not in pending_ids(pending)] + [asset for asset in done if asset not in wrong_size]
            retry_fail = failed if attempts <= budget_fail else []
            retry_spec = wrong_size if attempts <= budget_spec else []
            if not retry_fail and not retry_spec:
                break
            again = set(retry_fail) | set(retry_spec)
            pending = [item for item in pending if item["asset_id"] in again]

    # ④ 매니페스트 — 기존 항목 보존 + 새 항목 추가(덮어쓰기 없음)
    rendered_at = _now_iso()
    new_items: list[dict] = []
    for item in plan:
        asset_path = paths.figure_asset(item["asset_id"])
        if item["asset_id"] not in done_all or not os.path.isfile(asset_path):
            continue
        name = os.path.basename(item["raw_path"])
        new_items.append({
            "figure_id": item["figure_id"], "source_raw_path": item["raw_path"],
            "source_sha256": verified_raw.get(name) or sha256_file(item["raw_abs"]),
            "asset_id": item["asset_id"],
            "asset_path": os.path.relpath(asset_path, paths.run_root).replace(os.sep, "/"),
            "sha256": sha256_file(asset_path), "renderer": render_mod.renderer_label(), "template": render_mod.TEMPLATE_ID,
            "fallback": True, "edits": item["edits"], "edit_class": EDIT_CLASS_CROP, "publishable": True,
            "rendered_at": rendered_at,
        })
    order = {str(figure["id"]): index for index, figure in enumerate(figures)}
    items = sorted([*existing.values(), *new_items], key=lambda item: order.get(str(figure_id_of(item)), len(order)))
    manifest_out = {
        "schema": MANIFEST_SCHEMA, "run_id": run_id, "spec_version": version, "spec_digest": spec_digest,
        "renderer": render_mod.renderer_descriptor(pin), "items": items,
    }

    # ⑤ 검사 3 — 렌더 실패 도면은 asset-completeness 가 잡는다(부분 자산층으로 진행하지 않는다)
    failed_figures = [item["figure_id"] for item in plan if item["asset_id"] in failed or item["asset_id"] in wrong_size]
    rows = [
        entry_row,
        check_asset_completeness(figures, assets_dir, missing_raw=missing_raw, failed_render=failed_figures,
                                 rejected={item["asset_id"] for item in plan if item["asset_id"] in wrong_size}),
        check_render_spec(assets_dir, [asset_id_of(item) + ASSET_EXT for item in items] + [asset + ASSET_EXT for asset in wrong_size]),
        check_manifest_parity(manifest_out, figures, assets_dir, rejected=set(wrong_size)),
    ]
    by_id = {row.check_id: row for row in rows}
    if wrong_size or by_id[CHECK_RENDER_SPEC].status == "fail":
        # 「figures.render-spec 위반」 retry(1) → halt. 치수가 틀린 출력은 매니페스트에 올리지 않았고(위 ③) 파일은 지우지
        # 않는다(사료). 재시도 뒤에도 그대로면 렌더 환경의 문제다 — halt.
        terminal, budget = _terminal(contract, "figures.render-spec 위반")
        status = terminal
        reason = f"render-spec 위반 {len(wrong_size) or by_id[CHECK_RENDER_SPEC].violations}건(재시도 예산 {budget} 소진 · {sorted(wrong_size)[:3]})"
    elif by_id[CHECK_COMPLETENESS].status == "fail":
        terminal, _budget = _terminal(contract, "일부 도면 렌더 실패")
        status = terminal
        reason = "누락 도면 " + ", ".join(by_id[CHECK_COMPLETENESS].extras.get("missing") or [])
    elif by_id[CHECK_PARITY].status == "fail":
        status, reason = "halt", "manifest-parity 위반 " + str(by_id[CHECK_PARITY].violations)
    else:
        status, reason = "ok", None
    if status != "halt" or existing or manifest_out["items"]:
        # 매니페스트는 통과한 항목만 든다. 부분 자산층이라도 만들어진 자산은 사료다(§7.5) — 파일은 남기되 상태는 위대로.
        if manifest_out["items"] or manifest is not None:
            write_json(manifest_path, manifest_out)
    _write_report(paths, STEP_PREPARE, status=status, rows=rows, extra={
        "renderer_environment": env_report, "attempts": attempts, "rendered": done_all, "render_failed": failed,
        "reentered": not plan and not missing_raw, "spec_version": version, "spec_digest": spec_digest,
    })
    return {"status": status, "rows": rows, "manifest": manifest_out if manifest_out["items"] else None,
            "manifest_path": manifest_path, "missing": list(by_id[CHECK_COMPLETENESS].extras.get("missing") or []),
            "attempts": attempts, "rendered": done_all, "reason_label": reason}


# ---------------------------------------------------------------------------
# select — 검사 3
# ---------------------------------------------------------------------------


def _images_per_post_max(repo: str) -> int:
    params = load_format_parameters(repo)["parameters"]
    try:
        return int(params["images_per_post_max"]["value"])
    except (KeyError, TypeError, ValueError) as exc:
        raise StageError(f"형식 파라미터 시트에 images_per_post_max 가 없다: {exc}") from exc


def build_selection(blueprint: dict, manifest: dict, *, run_id: str, spec_version: int, spec_digest: str,
                    blueprint_digest: str) -> tuple[dict, list[str]]:
    """figure_plan → 슬롯 행. 반환 = (selection, 자산층에 없는 FIG 목록)."""
    by_figure = {str(figure_id_of(item)): asset_id_of(item) for item in manifest_items(manifest)}
    slots: list[dict] = []
    unresolved: list[str] = []
    hero_done = False
    for entry in sorted((blueprint.get("figure_plan") or []), key=lambda row: int((row or {}).get("tweet", 0))):
        tweet = int(entry.get("tweet", 0))
        for figure_id in entry.get("figures") or []:
            asset = by_figure.get(str(figure_id))
            if not asset:
                unresolved.append(f"T{tweet}:{figure_id}")
                continue
            role = ROLE_HERO if (tweet == 1 and not hero_done) else ROLE_EXHIBIT
            if role == ROLE_HERO:
                hero_done = True
            slots.append({"tweet": tweet, "asset": asset, "role": role})
    selection = {"schema": SELECTION_SCHEMA, "run_id": run_id, "spec_version": int(spec_version), "spec_digest": spec_digest,
                 "blueprint_digest": blueprint_digest, "slots": slots}
    return selection, unresolved


def check_selection_resolve(selection: dict, manifest: dict, limit: int) -> CheckRow:
    assets = {asset_id_of(item) for item in manifest_items(manifest)}
    slots = list(selection.get("slots") or [])
    row = CheckRow(check_id=CHECK_SELECTION, checked=len(slots))
    per_tweet: dict[int, int] = {}
    for index, slot in enumerate(slots):
        asset = str(slot.get("asset"))
        if asset not in assets:
            row.add("selection.unresolved", f"slots[{index}]", asset, "manifest.json#items[].asset_id", "선택 포인터가 매니페스트에 해소되지 않는다")
        per_tweet[int(slot.get("tweet", 0))] = per_tweet.get(int(slot.get("tweet", 0)), 0) + 1
    for tweet, count in sorted(per_tweet.items()):
        if count > limit:
            row.add("selection.images-per-post", f"T{tweet}", str(count), f"<=sheet images_per_post_max ({limit})", "트윗당 도면 수가 시트 상한을 넘는다")
    row.extras["per_tweet"] = {f"T{tweet}": count for tweet, count in sorted(per_tweet.items())}
    return row


def check_no_copy(selection: dict) -> CheckRow:
    slots = list(selection.get("slots") or [])
    row = CheckRow(check_id=CHECK_NO_COPY, checked=len(slots))
    allowed = {"tweet", "asset", "role"}
    for index, slot in enumerate(slots):
        extra = sorted(set(slot) - allowed)
        if extra:
            row.add("no-copy.extra-key", f"slots[{index}]", ", ".join(extra), "tweet · asset · role", "슬롯 행에 포인터 밖의 키가 있다 — 선택은 자산 id 참조만 담는다(§7.5)")
        asset = str(slot.get("asset", ""))
        if not ASSET_ID_RE.match(asset) or "/" in asset or asset.startswith("data:"):
            row.add("no-copy.asset-id", f"slots[{index}]", asset[:60], "fig-NN", "asset 값이 자산 id 문법이 아니다(경로·데이터 복사 의심)")
    return row


def check_publish_gate(selection: dict, manifest: dict, *, run_kind: str, meta: dict, repo: str) -> CheckRow:
    """SPEC §1.8 run_kind 분기표. partial 은 rehearsal 과 같이 ①만(계약 note · run-kinds.yaml#kinds.partial.publishes: false)."""
    kinds = (run_kinds_contract(repo).get("kinds") or {})
    kind_row = kinds.get(run_kind) or {}
    publishes = bool(kind_row.get("publishes"))
    by_asset = {asset_id_of(item): item for item in manifest_items(manifest)}
    slots = list(selection.get("slots") or [])
    row = CheckRow(check_id=CHECK_PUBLISH, checked=len(slots))
    row.extras["run_kind"] = run_kind
    row.extras["branch"] = "①+②" if publishes else "①"
    for index, slot in enumerate(slots):
        item = by_asset.get(str(slot.get("asset")))
        if item is None:
            continue   # 미해소는 selection-resolve 의 몫(한 위반을 두 행에 싣지 않는다)
        if item.get("publishable") is not True:
            row.add("publish.publishable", f"slots[{index}]", f"{slot.get('asset')} publishable={item.get('publishable')!r}",
                    "publishable == true", "게시 보류 자산을 지목했다 — 사용권 재정 전에는 게시하지 않는다(재정 R11)")
    if publishes:
        row.checked += 1
        decision = ((meta.get("figures") or {}).get("usage_rights_decision") if isinstance(meta.get("figures"), dict) else None)
        target = os.path.join(repo, "docs", "decisions", f"{decision}.md") if decision else ""
        if not decision or not os.path.isfile(target):
            row.add("publish.usage-rights", "run.yaml#figures.usage_rights_decision", str(decision), "docs/decisions/ 에 실재하는 재정 파일",
                    "게시 런인데 도면 사용권 재정 파일이 없다(재정 R11 · 재감수 B-05)")
    return row


def _corrections_rows(selection: dict, unresolved: list[str]) -> str:
    lines = ["# 교정 원장 행 — figures.select (런 안 사본 · 총괄 재량 ⓓ)", "",
             "`ledgers/corrections.md` 의 쓰기 소유자는 `ship` 이다(SPEC §1.17). 이 파일의 행을 `ship` 이 옮긴다.", "",
             "| 항목 | 값 |", "|---|---|",
             "| 선택 방식 | 블루프린트 `figure_plan` 의 결정론 사영(v1 자산 = 도면당 전장 크롭 1개 · 총괄 재량 ⓐ) |",
             f"| 슬롯 수 | {len(selection.get('slots') or [])} |",
             "| 기각 | 0 — 고를 대안이 없는 자산층이라 기각이 성립하지 않는다 |",
             f"| 미해소 | {', '.join(unresolved) if unresolved else '없음'} |",
             f"| 기록 시각 | {_now_iso()} |", ""]
    return "\n".join(lines)


def select(run_root: str, repo: str | None = None) -> dict:
    """`figures.select` 1회 진입. 반환 = `{status, rows, selection, selection_path, reason_label, unresolved}`."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID, inputs={"spec_version": version})
    manifest = _load_manifest(paths.figures_manifest_json)
    if manifest is None:
        raise StageEnvironmentError("[환경 오류] 30-figures/assets/manifest.json 이 없다 — figures.prepare 가 먼저다(depends_on)")
    if str(manifest.get("spec_digest", "")) != spec_digest:
        raise StageEnvironmentError("[환경 오류] 매니페스트가 다른 재료 판 위에 서 있다 — 재료 개정 뒤 자산층을 다시 준비한다(재정 N11)")
    if not os.path.isfile(paths.blueprint_json):
        raise StageEnvironmentError(f"[환경 오류] 블루프린트가 없다 — design 이 먼저다(depends_on): {paths.blueprint_json}")
    blueprint = load_json(paths.blueprint_json)
    if str(blueprint.get("spec_digest", "")) != spec_digest:
        raise StageEnvironmentError("[환경 오류] 블루프린트가 다른 재료 판 위에 서 있다(재정 N11)")
    run_id = str(meta.get("run_id", ""))
    run_kind = str(meta.get("run_kind", ""))

    selection, unresolved = build_selection(blueprint, manifest, run_id=run_id, spec_version=version, spec_digest=spec_digest,
                                            blueprint_digest=sha256_file(paths.blueprint_json))
    limit = _images_per_post_max(repo)
    rows = [entry_row, check_selection_resolve(selection, manifest, limit), check_no_copy(selection),
            check_publish_gate(selection, manifest, run_kind=run_kind, meta=meta, repo=repo)]
    by_id = {row.check_id: row for row in rows}
    if unresolved:
        by_id[CHECK_SELECTION].add("selection.figure-not-in-assets", "figure_plan", ", ".join(unresolved), "manifest.json 의 figure_id",
                                   "블루프린트가 지정한 도면이 자산층에 없다 — 설계로 되돌린다")
        entry = failure_entry(contract, "블루프린트가 지정한 도면이 자산층에 없음")
        status, reason = str(entry.get("action")), f"자산층에 없는 도면 {', '.join(unresolved)} (→ {entry.get('to')})"
    elif by_id[CHECK_PUBLISH].status == "fail":
        entry = failure_entry(contract, "figures.publish-gate 실패")
        status, reason = str(entry.get("action")), "게시 보류 자산 지목 " + str(by_id[CHECK_PUBLISH].violations)
    elif by_id[CHECK_SELECTION].status == "fail":
        terminal, _budget = _terminal(contract, "selection.json 포인터 미해소")
        status, reason = terminal, "selection-resolve 위반 " + str(by_id[CHECK_SELECTION].violations)
    elif by_id[CHECK_NO_COPY].status == "fail":
        status, reason = "halt", "no-copy 위반 " + str(by_id[CHECK_NO_COPY].violations)
    else:
        status, reason = "ok", None
    selection_path = paths.figures_selection_json
    if status == "ok":
        write_json(selection_path, selection)
        write_text(paths.figures_corrections_md, _corrections_rows(selection, unresolved))
    _write_report(paths, STEP_SELECT, status=status, rows=rows, extra={
        "unresolved": unresolved, "slots": len(selection["slots"]), "images_per_post_max": limit,
        "spec_version": version, "spec_digest": spec_digest,
    })
    return {"status": status, "rows": rows, "selection": selection if status == "ok" else None, "selection_path": selection_path,
            "reason_label": reason, "unresolved": unresolved}


def load_selection(paths: RunPaths) -> dict | None:
    path = paths.figures_selection_json
    if not os.path.isfile(path):
        return None
    selection = load_json(path)
    if not isinstance(selection, dict) or selection.get("schema") != SELECTION_SCHEMA:
        raise StageError(f"선택 파일이 {SELECTION_SCHEMA} 가 아니다: {path}")
    return selection


def selection_assets_by_tweet(selection: dict | None) -> dict[int, list[str]]:
    """`{tweet: [asset_id, ...]}` — figure_plan 순서 그대로(펜 헤더 `fig` 의 기대 집합)."""
    out: dict[int, list[str]] = {}
    for slot in (selection or {}).get("slots") or []:
        out.setdefault(int(slot.get("tweet", 0)), []).append(str(slot.get("asset")))
    return out


__all__ = ["CHECK_COMPLETENESS", "CHECK_ENTRY", "CHECK_NO_COPY", "CHECK_PARITY", "CHECK_PUBLISH", "CHECK_RENDER_SPEC",
           "CHECK_SELECTION", "MANIFEST_SCHEMA", "SELECTION_SCHEMA", "STEP_PREPARE", "STEP_SELECT", "build_selection",
           "check_asset_completeness", "check_manifest_parity", "check_no_copy", "check_publish_gate", "check_render_spec",
           "check_selection_resolve", "load_selection", "prepare", "select", "selection_assets_by_tweet"]
