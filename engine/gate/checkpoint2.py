# -*- coding: utf-8 -*-
"""CP2 전 표면과 승인 봉투. 소견 레인 장애만 결번으로 허용한다.

표면 정본 = critique.yaml#owner_checkpoint. 봉투 작성자는 오케스트레이터다.
숫자 화이트리스트 전량·플래그 전건·도면 변경 자리를 Owner에게 제공한다.
"""

from __future__ import annotations

import datetime as _dt
import os

from jsonschema import Draft202012Validator

from ..paths import RunPaths, repo_root
from ..stages import StageError, load_json, load_yaml, sha256_file, write_text, read_text

CHECKPOINT = "ship_approval"
ENVELOPE_SCHEMA = "approval-envelope/v0"
APPROVAL_SCHEMA_REL = ("contracts", "schemas", "approval-envelope.schema.json")
QUOTE_CHANNEL = "session-transcript"
FIGURE_SOURCED = "figure-sourced"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def checkpoint_block(paths: RunPaths) -> dict:
    block = paths.contracts["critique"].get("owner_checkpoint") or {}
    if str(block.get("id")) != CHECKPOINT or not block.get("confirm_file"):
        raise StageError("critique.yaml#owner_checkpoint 블록이 없거나 id 가 ship_approval 이 아니다")
    return block


def confirm_file_rel(paths: RunPaths) -> str:
    return str(checkpoint_block(paths)["confirm_file"])


def flags_of(verdict: dict) -> list[dict]:
    """판정문의 플래그 전건(L0 자문 규칙 + L1 강등·자문·화행) — Owner 판정 대상 id 집합의 정본."""
    out: list[dict] = []
    for layer in ("l0", "l1"):
        for flag in (verdict.get(layer) or {}).get("flags") or []:
            out.append({key: flag.get(key) for key in ("id", "layer", "rule", "origin", "locus", "note", "votes", "predicate") if key in flag})
    return out


def numeric_whitelist_printed(meta: dict, envelope_rel: str) -> list[dict]:
    """run.yaml#numeric_whitelist[] 전량 → 4키. `approved_in` null(재량 항목)은 이 봉투 파일명으로(SPEC §4.4.1)."""
    out: list[dict] = []
    for entry in meta.get("numeric_whitelist") or []:
        if not isinstance(entry, dict):
            continue
        approved = entry.get("approved_in")
        out.append({
            "pattern": str(entry.get("pattern", "")),
            "rationale": str(entry.get("rationale", "")),
            "added_by": str(entry.get("added_by", "")),
            "approved_in": str(approved) if approved else envelope_rel,
        })
    return out


def figure_sourced_ids(frozen: dict) -> list[str]:
    return [str(item["id"]) for item in frozen.get("items") or []
            if isinstance(item, dict) and item.get("kind") == "fact" and item.get("origin") == FIGURE_SOURCED and item.get("status") == "active"]


def surfaces(*, run_root: str, repo: str | None = None, variant: str) -> dict:
    """CP2 핵심 표면 7종 + 화이트리스트 + 봉투 초안. 읽기만."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    block = checkpoint_block(paths)
    meta = load_yaml(paths.run_yaml)
    envelope_rel = confirm_file_rel(paths)
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError(f"verdict.json 이 없다 — gate-l0 · gate-l1 이 먼저다: {verdict_path}")
    verdict = load_json(verdict_path)
    stripped = paths.thread_stripped_md(variant)
    if not os.path.isfile(stripped):
        raise StageError(f"출하 후보 텍스트가 없다: {stripped}")
    for required in (paths.figures_selection_json, paths.l1_json(variant), paths.l2_md(variant), paths.score_json(variant)):
        if not os.path.isfile(required):
            raise StageError("CP2 필수 표면 부재: " + required)
    if verdict.get("decision") != "advance" or (verdict.get("final_eyes") or {}).get("verdict") != "pass":
        raise StageError("CP2는 최종 심급 통과본만 상정한다")
    memo_path = paths.critique_memo(variant)
    missing_path = os.path.join(paths.critique_dir(variant), "memo-missing.json")
    if not os.path.isfile(memo_path) and not os.path.isfile(missing_path):
        raise StageError("소견 또는 소견 결번 기록이 없다")
    report_path = os.path.join(paths.critique_dir(variant), "critique-report.json")
    if not os.path.isfile(report_path):
        raise StageError("소견 검사 보고가 없다")
    critique_report = load_json(report_path)
    if critique_report.get("candidate_digest") != sha256_file(stripped) or critique_report.get("status") not in ("ok", "missing"):
        raise StageError("소견이 현 출하 후보의 것이 아니다 — critique 재실행")
    if os.path.isfile(memo_path) and critique_report.get("memo_digest") != sha256_file(memo_path):
        raise StageError("소견이 검사 후 바뀌었다")
    if load_json(paths.score_json(variant)).get("input_digest") != sha256_file(stripped):
        raise StageError("계기가 현 출하 후보의 관측이 아니다 — probe 재실행")
    from .final_eyes import provided_files, input_records, scope_row
    version = int((meta.get("frozen") or [{}])[-1]["spec_version"])
    final = verdict["final_eyes"]
    if scope_row(final).status == "fail" or final["inputs_read"] != input_records(paths, provided_files(paths, variant, version)):
        raise StageError("최종 심급 입력이 현재 후보와 다르다 — 재실행")
    flags = flags_of(verdict)
    selection = load_json(paths.figures_selection_json) if os.path.isfile(paths.figures_selection_json) else None
    frozen_row = (meta.get("frozen") or [{}])[-1]
    frozen = load_json(paths.frozen_spec(int(frozen_row.get("spec_version", 1))))
    present = {
        "thread_stripped": {"path": os.path.relpath(stripped, paths.run_root).replace(os.sep, "/"), "digest": sha256_file(stripped), "text": read_text(stripped)},
        "selection": selection,
        "l2": read_text(paths.l2_md(variant)),
        "score": load_json(paths.score_json(variant)),
        "memo": "\n".join(read_text(memo_path).splitlines()[:20]) if os.path.isfile(memo_path) else "소견 결번: " + str(load_json(missing_path).get("reason")),
        "flags": flags,
        "verdict": {
            "final_eyes": verdict.get("final_eyes"), "legislated": verdict.get("legislated"),
            "decision": verdict.get("decision"), "revision_round": verdict.get("revision_round"),
            "l0_pass": (verdict.get("l0") or {}).get("pass"), "l1_pass": (verdict.get("l1") or {}).get("pass"),
            "checks_fail": [row["check_id"] for row in verdict.get("checks") or [] if row.get("status") == "fail"],
            "vacuous_pass": list(verdict.get("vacuous_pass") or []),
            "inactive_layers": list(verdict.get("inactive_layers") or []),
            "disagreement_log": list((verdict.get("l1") or {}).get("disagreement_log") or []),
            "final_eyes_brief_digest": verdict.get("final_eyes_brief_digest"),
        },
        "numeric_whitelist": list(meta.get("numeric_whitelist") or []),
    }

    draft = {
        "selected_variant": variant,
        "flags_adjudicated": [{"flag_id": flag["id"], "verdict": ""} for flag in flags],
        "figure_overrides": [],
        "manual_verification_ack": figure_sourced_ids(frozen),
        "numeric_whitelist_printed": numeric_whitelist_printed(meta, envelope_rel),
    }
    return {"variant": variant, "checkpoint": CHECKPOINT, "confirm_file": envelope_rel, "present": present,
            "question": block["question"], "draft": draft, "verdict_decision": verdict.get("decision")}


def validate_envelope(repo: str, envelope: dict) -> list[str]:
    schema = load_json(os.path.join(repo, *APPROVAL_SCHEMA_REL))
    errors = sorted(Draft202012Validator(schema).iter_errors(envelope), key=lambda err: list(err.absolute_path))
    return [("/".join(str(step) for step in err.absolute_path) or "$") + ": " + err.message for err in errors]


def build_envelope(*, run_root: str, repo: str | None = None, variant: str, decision: str, owner_quote: str, located_at: str,
                   flags_adjudicated: list[dict], figure_overrides=(), directives=(), decided_at: str | None = None) -> tuple[dict, list[str]]:
    """봉투 객체 + 경고 목록(미판정 플래그 · 유령 플래그). 스키마 위반은 `StageError`."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    meta = load_yaml(paths.run_yaml)
    envelope_rel = confirm_file_rel(paths)
    verdict = load_json(paths.verdict_json(variant))
    stripped = paths.thread_stripped_md(variant)
    frozen_row = (meta.get("frozen") or [{}])[-1]
    frozen = load_json(paths.frozen_spec(int(frozen_row.get("spec_version", 1))))
    envelope: dict = {
        "schema": ENVELOPE_SCHEMA,
        "checkpoint": CHECKPOINT,
        "run_id": str(meta.get("run_id", "")),
        "target": {"path": os.path.relpath(stripped, paths.run_root).replace(os.sep, "/"), "digest": sha256_file(stripped)},
        "decision": decision,
        "owner_quote": owner_quote,
        "quote_provenance": {"channel": QUOTE_CHANNEL, "located_at": located_at},
        "decided_at": decided_at or _now_iso(),
        "recorded_by": "orchestrator",
        "selected_variant": variant,
        "flags_adjudicated": [{"flag_id": str(row.get("flag_id")), "verdict": str(row.get("verdict"))} for row in flags_adjudicated],
        "figure_overrides": [str(x) for x in figure_overrides],
        "manual_verification_ack": figure_sourced_ids(frozen),
        "numeric_whitelist_printed": numeric_whitelist_printed(meta, envelope_rel),
    }
    if decision == "rejected":
        envelope["directives"] = [str(d) for d in directives]
    errors = validate_envelope(repo, envelope)
    if errors:
        raise StageError("봉투가 approval-envelope/v0 를 위반한다: " + " / ".join(errors[:3]))
    known = {flag["id"] for flag in flags_of(verdict)}
    answered = {row["flag_id"] for row in envelope["flags_adjudicated"]}
    warnings = [f"미판정 플래그 {fid} — ship.flags-adjudicated(M10) 가 halt 한다" for fid in sorted(known - answered)]
    warnings.extend(f"유령 플래그 {fid} — 이 변주의 판정문에 없는 id" for fid in sorted(answered - known))
    return envelope, warnings


def write_envelope(*, run_root: str, repo: str | None = None, envelope: dict, title: str) -> str:
    """`70-ship/checkpoint2.md` — YAML 프런트매터(봉투) + 제목. 이때 `70-ship/` 이 처음 생긴다."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    path = paths.checkpoint2_md
    os.makedirs(paths.ship_dir, exist_ok=True)
    import io  # noqa: PLC0415

    buffer = io.StringIO()
    import yaml  # noqa: PLC0415

    yaml.safe_dump(envelope, buffer, allow_unicode=True, sort_keys=False)
    write_text(path, f"---\n{buffer.getvalue()}---\n\n{title}\n")
    return path


__all__ = ["CHECKPOINT", "build_envelope", "flags_of", "numeric_whitelist_printed", "surfaces", "validate_envelope", "write_envelope"]
