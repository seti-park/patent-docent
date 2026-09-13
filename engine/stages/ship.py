"""승인본 복사·자산 해소·출하 원장 기입. 텍스트를 저작하지 않는다."""
import json
from datetime import datetime
import os
from pathlib import Path
import shutil

from reader.lib.report import CheckRow
from ..paths import RunPaths, repo_root, run_kinds_contract
from ..gate.checkpoint2 import validate_envelope, flags_of, figure_sourced_ids, numeric_whitelist_printed, surfaces
from ..gate.final_eyes import provided_files, input_records, scope_row
from . import (StageError, StageHaltError, load_json, load_yaml, read_text, write_json, write_text,
               sha256_file, rows_to_dicts, dump_yaml, verify_declared_inputs, findings_of, failure_entry)
from .freeze import parse_envelope
from .design import terminus_index, latest_frozen
from .figures import check_selection_resolve, check_no_copy, check_publish_gate, _images_per_post_max
from .gate import _now_iso


def run(run_root, repo=None):
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts["ship"]
    meta = load_yaml(paths.run_yaml)
    rows = []
    report = os.path.join(paths.ship_dir, "ship-report.json")

    def record(status):
        write_json(report, {"stage": "ship", "status": status, "rows": rows_to_dicts(rows), "findings": findings_of(rows), "extras": {r.check_id: r.extras for r in rows if r.extras}, "recorded_at": _now_iso()})

    def check(suffix, valid, detail, checked=1):
        row = CheckRow(check_id="ship." + suffix, checked=checked)
        rows.append(row)
        if not valid:
            row.add(row.check_id, suffix, detail, "계약 충족", detail)
            record("halt")
            raise StageHaltError(row.check_id + ": " + detail)
        return row

    if meta.get("run_kind") != "partial":
        raise StageHaltError("T69 출하 러너의 범위는 partial 게시물 패키지다")
    if terminus_index(repo, str(meta.get("partial_until"))) < terminus_index(repo, "ship"):
        raise StageHaltError("출하 종료선 연장이 필요하다")
    try:
        envelope = parse_envelope(read_text(paths.checkpoint2_md))
        errors = validate_envelope(repo, envelope)
    except (StageError, OSError, ValueError) as exc:
        check("approval-valid", False, "승인 봉투 부재·무효: " + str(exc))
    variant = envelope.get("selected_variant")
    variants = [r["variant"] for r in paths.contracts["compose"]["lane"]["variants"]]
    valid = not errors and variant in variants and envelope.get("decision") == "approved" and bool(envelope.get("owner_quote"))
    valid = valid and envelope.get("checkpoint") == "ship_approval" and envelope.get("run_id") == meta.get("run_id")
    if not valid:
        check("approval-valid", False, "승인 봉투 신원·스키마·이진 승인 불일치: " + str(errors))
    source_md = paths.thread_stripped_md(variant)
    target = envelope.get("target") or {}
    valid = target.get("path") == os.path.relpath(source_md, paths.run_root) and os.path.isfile(source_md)
    valid = valid and target.get("digest") == sha256_file(source_md)
    check("approval-valid", valid, "승인 대상 또는 digest 불일치 — 재승인")
    version = int(latest_frozen(meta)["spec_version"])
    rows.append(verify_declared_inputs(paths, contract, "ship", inputs={"variant": variant, "spec_version": version}))
    verdict = load_json(paths.verdict_json(variant))
    final = verdict.get("final_eyes") or {}
    if (verdict.get("decision") != "advance" or final.get("verdict") != "pass" or scope_row(final).status == "fail"
        or final.get("inputs_read") != input_records(paths, provided_files(paths, variant, version))
        or any(r["status"] == "fail" for r in verdict.get("checks", []))):
        raise StageHaltError("최종 심급 통과본이 아니다 — final-eyes → CP2 재상신")
    final_report_path = os.path.join(paths.gate_dir(variant), "final-eyes-report.json")
    if not os.path.isfile(final_report_path) or load_json(final_report_path).get("runner_inputs") != input_records(paths, [paths.thread_json(variant), paths.annotation_index_json(variant)]):
        check("byte-identical", False, "최종 심급 이후 구조화 파일이 바뀌었다 — 재실행·재승인")
    final_report = load_json(final_report_path)
    approval_time = datetime.fromisoformat(envelope["decided_at"].replace("Z", "+00:00"))
    final_time = datetime.fromisoformat(final_report["produced_at"].replace("Z", "+00:00"))
    if approval_time < final_time or os.stat(paths.checkpoint2_md).st_mtime_ns < os.stat(final_report_path).st_mtime_ns:
        check("approval-valid", False, "최종 심급 이전 봉투다 — CP2 재상신·재승인")
    surfaces(run_root=paths.run_root, repo=repo, variant=variant)
    # 기존 복사본을 먼저 검사한다. 재호출로 개작 흔적을 덮지 않는다.
    pairs = [(source_md, paths.ship_thread_md), (paths.thread_json(variant), paths.ship_thread_json)]
    for source, dest in pairs:
        check_valid = not os.path.exists(dest) or Path(source).read_bytes() == Path(dest).read_bytes()
        if not check_valid:
            check("byte-identical", False, "출하본 한 바이트 이상 불일치: " + dest)
    for source, dest in pairs:
        if not os.path.exists(dest):
            shutil.copyfile(source, dest)
    check("byte-identical", all(Path(a).read_bytes() == Path(b).read_bytes() for a, b in pairs), "출하 텍스트 바이트 동일", len(pairs))
    selection = load_json(paths.figures_selection_json)
    manifest = load_json(paths.figures_manifest_json)
    resolve = check_selection_resolve(selection, manifest, _images_per_post_max(repo))
    resolve.check_id = "ship.image-resolve"
    rows.append(resolve)
    safe = check_no_copy(selection).status != "fail"
    assets = list(dict.fromkeys(str(s["asset"]) for s in selection.get("slots", [])))
    # retry(1)은 다음 동일 명령 호출에서 재해소한다. 실패 횟수도 디스크에 남긴다.
    if resolve.status == "fail" or not safe or not all(os.path.isfile(paths.figure_asset(a)) for a in assets):
        state_path = os.path.join(paths.ship_dir, "image-resolve-state.json")
        attempts = (load_json(state_path).get("attempts", 0) if os.path.isfile(state_path) else 0) + 1
        write_json(state_path, {"attempts": attempts})
        if resolve.status != "fail":
            resolve.add(resolve.check_id, "selection.json", "자산 파일/포인터 부재", "승인 자산 실재", "도면 포인터 미해소")
        record("retry" if attempts == 1 else "halt")
        retry_cap = int(failure_entry(contract, "도면 포인터 미해소")["action"].partition("(")[2].rstrip(")"))
        if attempts <= retry_cap:
            return {"status": "retry", "check": resolve.check_id}
        raise StageHaltError("ship.image-resolve: retry(1) 소진")
    mapping = {}
    tweet_ids = {int(t["n"]) for t in load_json(paths.thread_json(variant))["tweets"]}
    for slot in selection.get("slots", []):
        if int(slot["tweet"]) not in tweet_ids:
            check("image-resolve", False, "존재하지 않는 트윗 포인터")
        mapping.setdefault(str(slot["tweet"]), []).append(slot["asset"])
    expected_names = {a + ".png" for a in assets} | {"index.json"}
    os.makedirs(paths.ship_images_dir, exist_ok=True)
    if set(os.listdir(paths.ship_images_dir)) - expected_names:
        check("image-resolve", False, "승인 포인터 밖 이미지 파일")
    for asset in assets:
        source = paths.figure_asset(asset)
        dest = os.path.join(paths.ship_images_dir, asset + ".png")
        if os.path.exists(dest) and Path(source).read_bytes() != Path(dest).read_bytes():
            check("image-resolve", False, "출하 이미지 개작: " + asset)
        if not os.path.exists(dest):
            shutil.copyfile(source, dest)
    index_path = os.path.join(paths.ship_images_dir, "index.json")
    if os.path.exists(index_path) and load_json(index_path) != mapping:
        check("image-resolve", False, "이미지 매핑이 기존 출하본과 다르다")
    write_json(index_path, mapping)
    publish = check_publish_gate(selection, manifest, run_kind=meta["run_kind"], meta=meta, repo=repo)
    publish.extras["usage_rights_decision"] = contract["usage_rights_decision"]
    rows.append(publish)
    if publish.status == "fail":
        record("halt")
        raise StageHaltError("figures.publish-gate 실패")
    adjudicated = {f["flag_id"] for f in envelope.get("flags_adjudicated", [])}
    check("flags-adjudicated", {f["id"] for f in flags_of(verdict)} <= adjudicated, "미판정 flag 존재 — CP2 재상신")
    frozen = load_json(paths.frozen_spec(version))
    if (set(envelope.get("manual_verification_ack", [])) != set(figure_sourced_ids(frozen))
        or envelope.get("numeric_whitelist_printed") != numeric_whitelist_printed(meta, os.path.relpath(paths.checkpoint2_md, paths.run_root))):
        raise StageHaltError("CP2 숫자 전량 인쇄·도면 확인이 현재 입력과 다르다")
    if envelope.get("figure_overrides") and set(envelope["figure_overrides"]) != set(assets):
        raise StageHaltError("도면 override는 selection에 반영 후 CP2 재상신해야 한다")
    # 원장별 멱등성: 이미 이관된 행의 개수까지 대조한다. 부분 실패 뒤 재호출도 중복 기입하지 않는다.
    ledger_root = os.path.join(repo, "ledgers")
    os.makedirs(ledger_root, exist_ok=True)
    tournament = os.path.join(ledger_root, "tournament.jsonl")
    corrections = os.path.join(ledger_root, "corrections.md")
    staged = [json.loads(line) for line in read_text(paths.tournament_rows_jsonl).splitlines() if line.strip()]
    existing = [json.loads(line) for line in read_text(tournament).splitlines() if line.strip()] if os.path.isfile(tournament) else []
    prior_selection = [r for r in existing if r.get("run_id") == meta["run_id"] and r.get("recorded_by") == "ship"]
    selected = {"run_id": meta["run_id"], "selected_variant": variant, "comparison_axis": "effort", "taste_weight": "low",
                "pens": meta.get("pens", []), "decided_in": os.path.relpath(paths.checkpoint2_md, paths.run_root),
                "recorded_by": "ship", "recorded_at": prior_selection[0]["recorded_at"] if prior_selection else _now_iso()}
    if prior_selection and prior_selection != [selected]:
        check("ledger-write", False, "같은 런의 출하 선택이 기존 원장과 다르다")
    wanted = staged + [selected]
    appended = []
    for i, row in enumerate(wanted):
        if not isinstance(row, dict):
            check("ledger-write", False, "토너먼트 행이 JSON 객체가 아니다")
        if existing.count(row) < wanted[:i + 1].count(row):
            existing.append(row)
            appended.append(row)
    if appended:
        with open(tournament, "a", encoding="utf-8") as handle:
            if os.path.isfile(tournament) and os.path.getsize(tournament) and not Path(tournament).read_bytes().endswith(b"\n"):
                handle.write("\n")
            for row in appended:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    prior = read_text(corrections) if os.path.isfile(corrections) else ""
    heading = "## " + meta["run_id"]
    correction_body = read_text(paths.figures_corrections_md).strip()
    section = heading + "\n\n" + correction_body + "\n"
    if heading in prior.splitlines():
        if section not in prior:
            check("ledger-write", False, "기존 도면 정정 절과 런 안 행이 다르다")
    else:
        with open(corrections, "a", encoding="utf-8") as handle:
            handle.write(("\n" if prior else "") + section)
    parsed = [json.loads(line) for line in read_text(tournament).splitlines() if line.strip()]
    check("ledger-write", parsed.count(selected) == 1 and all(parsed.count(r) >= staged.count(r) for r in staged), "원장 이관 및 선택 1행", len(wanted))
    if run_kinds_contract(repo)["kinds"][meta["run_kind"]]["anchor_ledger"] != "excluded":
        raise StageHaltError("partial 앵커 제외 계약 불일치")
    layers = [name for name, row in paths.contracts["gate"]["layers"].items() if isinstance(row, dict) and row.get("status") == "active"]
    unavailable = {r["layer"] for r in verdict.get("inactive_layers", [])}
    layers = [name for name in layers if name not in unavailable]
    if os.path.isfile(paths.score_json(variant)):
        layers.append("instrument")
    lines = ["# 출하 패키지", "", "이 런은 partial · 게시는 Owner 손으로 한다.", "",
        "텍스트: thread.md · 구조화 복사본: thread.json · 이미지 매핑: images/index.json", "",
        "| 트윗 순서 | 이미지 파일 |", "|---|---|"]
    lines.extend(f"| {n} | {', '.join('images/' + a + '.png' for a in mapping.get(str(n), [])) or '없음'} |" for n in sorted(tweet_ids))
    lines.extend(["", "게시 전제 3 (partial 표기용)", f"- defense_layers: {', '.join(layers)} · 가동 층 확인",
        f"- figures_usage_rights_decision: {contract['usage_rights_decision']} · crop-only 허용",
        "- template_freeze: 없음", "", "앵커 미편입: partial.anchor_ledger = excluded"])
    write_text(paths.ship_md, "\n".join(lines) + "\n")
    record("ok")
    meta["status"] = "shipped"
    dump_yaml(paths.run_yaml, meta)
    return {"status": "ok", "run_status": "shipped", "package": paths.ship_md, "rows": rows_to_dicts(rows)}
