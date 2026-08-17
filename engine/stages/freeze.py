# -*- coding: utf-8 -*-
"""`freeze` 스테이지 — 승인된 재료에 버전 스탬프와 다이제스트를 찍고 읽기 전용화한다.

계약 = `contracts/stages/freeze.yaml`(정본 서술 = SPEC §1.6).

★ `freeze.approval-valid` 은 스키마 밖 3항을 **추가로** 본다(M0.6 재감수 M-01 잔여의 처분).

① `drop_signal.verdict == "drop-proposed"` 면 `drop_decision` 필수
② `derived_fact_ack[]` 집합 == `origin: "derived"` 항목 집합 (부분집합이 아니라 **정확히 일치**)
③ `manual_verification_ack[]` 집합 == `origin: "figure-sourced"` 항목 집합

대조 없는 목록은 승인이 아니라 **서명**이다 — 빈 목록도 유령 ID 도 통과하던 자리가 여기였다.
빠진 id 와 유령 id 는 각각 별도 결함으로 낸다(수정 지시가 무엇을 지목해야 하는지 다르다).
"""

from __future__ import annotations

import json
import os
import re
import stat

import yaml
from jsonschema import Draft202012Validator

from reader.lib import run_freeze_checks
from reader.lib.report import CheckContext, CheckRow
from reader.lib.rules import Rules

from . import (
    StageError,
    dump_yaml,
    failure_entry,
    load_json,
    load_yaml,
    read_text,
    sha256_file,
    worst_status,
)
from ..paths import RunPaths

STAGE_ID = "freeze"
APPROVAL_SCHEMA = ("contracts", "schemas", "approval-envelope.schema.json")
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\s*?(?:\n|\Z)", re.DOTALL)
READONLY_MODE = 0o444


def parse_envelope(text: str) -> dict:
    """봉투 md 의 YAML 프런트매터를 판다. 실물은 md 이고 스키마 대상은 프런트매터다."""
    match = FRONTMATTER.match(text)
    if not match:
        raise StageError("승인 봉투에 YAML 프런트매터가 없다(`---` 로 여닫는다)")
    data = yaml.safe_load(match.group("body"))
    if not isinstance(data, dict):
        raise StageError("승인 봉투 프런트매터 최상위가 매핑이 아니다")
    return data


def _facts_by_origin(spec: dict, origin: str) -> list[str]:
    return [
        str(item.get("id"))
        for item in spec.get("items") or []
        if item.get("kind") == "fact" and item.get("origin") == origin
    ]


def _compare_ack(
    row: CheckRow,
    *,
    field: str,
    declared: list,
    expected: list,
    origin: str,
) -> None:
    """ack 목록 ↔ 실제 집합. 빠진 id 와 유령 id 를 각각 별도 결함으로 낸다."""
    declared_set = {str(entry) for entry in declared or []}
    expected_set = set(expected)
    for missing in sorted(expected_set - declared_set):
        row.add(
            "approval.ack-complete",
            f"{field}",
            "(목록에 없음)",
            missing,
            f"origin `{origin}` 항목 {missing} 이 {field} 에 없다 — 항목 단위 승인이 성립하지 않았다",
        )
    for phantom in sorted(declared_set - expected_set):
        row.add(
            "approval.ack-no-phantom",
            f"{field}",
            phantom,
            f"origin `{origin}` 항목 집합",
            f"{field} 의 {phantom} 은 재료에 그런 origin 의 항목이 아니다(유령 ID)",
        )


def _render_parity(row: CheckRow, spec: dict, rendered: str) -> None:
    """`material-spec.md` 에 모든 `items[].id` 가 1회 이상 등장하는가."""
    for item in spec.get("items") or []:
        item_id = str(item.get("id"))
        pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(item_id)}(?![0-9])")
        if not pattern.search(rendered):
            row.add(
                "freeze.render-parity",
                f"10-read/material-spec.md#{item_id}",
                "(등장 없음)",
                f"{item_id} 1회 이상",
                "KR 판독본이 항목을 빠뜨렸다 — CP1 검토 표면이 불완전하다",
            )


def run(
    *,
    run_root: str,
    spec_version: int,
    rules: Rules,
    repo: str | None = None,
) -> dict:
    """승인 봉투를 검증하고 동결본을 0444 로 쓴다.

    반환 = `{"rows", "spec", "status", "reason_label", "path", "digest"}`.
    """
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    paths.ensure_frozen_dir()

    frozen_path = paths.frozen_spec(spec_version)
    rows: list[CheckRow] = []
    statuses: list[str] = []

    # ① 승인 봉투 — 부재는 곧 체크포인트 우회다.
    approval_row = CheckRow(check_id="freeze.approval-valid", checked=1)
    approval_path = paths.approval(spec_version)
    if not os.path.exists(approval_path):
        approval_row.add(
            "approval.present",
            os.path.relpath(approval_path, paths.run_root),
            "(봉투 없음)",
            "approval-envelope/v0 프런트매터를 담은 md",
            "승인 봉투 없이는 동결하지 않는다 — 무인 진행 경로는 없다(재정 R8)",
        )
        rows.append(approval_row)
        entry = failure_entry(contract, "승인 봉투 부재")
        return {
            "rows": rows,
            "spec": None,
            "status": str(entry.get("action")),
            "reason_label": entry.get("reason_label"),
            "path": None,
            "digest": None,
        }

    envelope = parse_envelope(read_text(approval_path))
    schema_path = os.path.join(paths.repo, *APPROVAL_SCHEMA)
    with open(schema_path, encoding="utf-8") as handle:
        envelope_schema = json.load(handle)
    for error in sorted(
        Draft202012Validator(envelope_schema).iter_errors(envelope),
        key=lambda err: list(err.absolute_path),
    ):
        locus = "/".join(str(step) for step in error.absolute_path) or "$"
        approval_row.add(
            "approval.schema",
            f"{os.path.basename(approval_path)}#{locus}",
            repr(error.instance)[:120],
            "approval-envelope/v0",
            f"승인 봉투가 스키마를 위반한다: {error.message}",
        )

    spec = load_json(paths.material_spec_json)

    if envelope.get("decision") != "approved":
        approval_row.add(
            "approval.decision",
            "decision",
            str(envelope.get("decision")),
            "approved",
            "승인되지 않은 봉투로는 동결하지 않는다(조건부 승인 제도 없음)",
        )
    if not str(envelope.get("owner_quote", "")).strip():
        approval_row.add(
            "approval.owner-quote",
            "owner_quote",
            "(비어 있음)",
            "Owner 가 실제로 타이핑한 원문",
            "육성 인용이 없는 봉투는 승인이 아니다(시스템 요약 인용은 무효)",
        )

    # ② 대상 해시 결속 — 승인 후 재료가 조용히 바뀌는 경로의 봉쇄.
    target = envelope.get("target") or {}
    target_path = os.path.join(paths.run_root, *str(target.get("path", "")).split("/"))
    if not os.path.exists(target_path):
        approval_row.add(
            "approval.target-missing",
            "target.path",
            str(target.get("path")),
            "런 안의 실재 파일",
            "봉투가 가리키는 대상 파일이 없다",
        )
    else:
        actual = sha256_file(target_path)
        if actual != target.get("digest"):
            approval_row.add(
                "approval.target-digest",
                "target.digest",
                str(target.get("digest")),
                actual,
                "승인 시점 대상과 현재 파일이 다르다 — 봉투는 자동 실효한다(재정 R8)",
            )

    # ③ 스키마 밖 3항
    drop_signal = spec.get("drop_signal") or {}
    if drop_signal.get("verdict") == "drop-proposed" and not envelope.get("drop_decision"):
        approval_row.add(
            "approval.drop-decision",
            "drop_decision",
            "(없음)",
            "go | drop",
            "drop 제안이 있는 재료를 처분 없이 승인할 수는 없다",
        )
    _compare_ack(
        approval_row,
        field="derived_fact_ack",
        declared=envelope.get("derived_fact_ack") or [],
        expected=_facts_by_origin(spec, "derived"),
        origin="derived",
    )
    _compare_ack(
        approval_row,
        field="manual_verification_ack",
        declared=envelope.get("manual_verification_ack") or [],
        expected=_facts_by_origin(spec, "figure-sourced"),
        origin="figure-sourced",
    )
    rows.append(approval_row)
    if approval_row.status == "fail":
        statuses.append(str(failure_entry(contract, "승인 봉투 부재").get("action")))

    # ④ 원천 다이제스트 대조
    digest_row = CheckRow(check_id="freeze.digest-match", checked=1)
    recorded_digest = read_text(paths.patent_sha256).strip()
    spec_digest = str((spec.get("patent") or {}).get("source_digest", ""))
    if spec_digest != recorded_digest:
        digest_row.add(
            "freeze.digest-match",
            "patent.source_digest",
            spec_digest,
            recorded_digest,
            "동결하려는 재료가 이 런의 원천 위에서 만들어지지 않았다",
        )
        statuses.append(str(failure_entry(contract, "freeze.digest-match 실패").get("action")))
    rows.append(digest_row)

    # ⑤ 렌더 패리티
    parity_row = CheckRow(check_id="freeze.render-parity", checked=len(spec.get("items") or []))
    _render_parity(parity_row, spec, read_text(paths.material_spec_md))
    if parity_row.status == "fail":
        statuses.append(str(failure_entry(contract, "freeze.render-parity 실패").get("action")))
    rows.append(parity_row)

    # ⑥ 개정 검사 2종(reader/lib) — 직전 판이 있으면 그것과 대조한다.
    prior_path = paths.frozen_spec(spec_version - 1) if spec_version > 1 else None
    prior_spec = load_json(prior_path) if prior_path and os.path.exists(prior_path) else None
    integrity_rows = run_freeze_checks(
        CheckContext(spec=spec, rules=rules, prior_spec=prior_spec)
    )
    rows.extend(integrity_rows)
    for row in integrity_rows:
        if row.status == "fail":
            statuses.append(
                str(failure_entry(contract, f"{row.check_id} 실패").get("action"))
            )

    status = worst_status(statuses or ["ok"])
    if status != "ok":
        return {
            "rows": rows,
            "spec": None,
            "status": status,
            "reason_label": None,
            "path": None,
            "digest": None,
        }

    # ⑦ 동결 — 덮어쓰기 금지(§7.6). 개정은 새 파일이며 옛 판을 지우지 않는다.
    if os.path.exists(frozen_path):
        raise StageError(
            f"동결본이 이미 있다: {frozen_path} — 개정은 v{spec_version + 1} 로 새로 쓴다"
        )
    frozen = dict(spec)
    frozen["status"] = "frozen"
    frozen["spec_version"] = spec_version
    with open(frozen_path, "w", encoding="utf-8") as handle:
        json.dump(frozen, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    os.chmod(frozen_path, READONLY_MODE)
    digest = sha256_file(frozen_path)

    # ⑧ 읽기 전용 확인 — "동결"이 이름뿐이 되지 않게 실제 모드를 본다.
    readonly_row = CheckRow(check_id="freeze.readonly", checked=1)
    mode = stat.S_IMODE(os.stat(frozen_path).st_mode)
    if mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        readonly_row.add(
            "freeze.readonly",
            os.path.relpath(frozen_path, paths.run_root),
            oct(mode),
            oct(READONLY_MODE),
            "동결본이 쓰기 가능하다 — 물리적 불변이 성립하지 않는다",
        )
    rows.append(readonly_row)

    _record_digest(paths, spec_version, frozen_path, digest)

    status = "ok" if readonly_row.status == "pass" else "halt"
    return {
        "rows": rows,
        "spec": frozen,
        "status": status,
        "reason_label": None,
        "path": frozen_path,
        "digest": digest,
    }


def _record_digest(paths: RunPaths, spec_version: int, frozen_path: str, digest: str) -> None:
    """동결본의 SHA-256 을 `run.yaml` 에 남긴다 — 하류가 `spec_digest` 로 복사한다."""
    meta = load_yaml(paths.run_yaml)
    frozen = meta.get("frozen")
    if not isinstance(frozen, list):
        frozen = []
    entry = {
        "spec_version": spec_version,
        "path": os.path.relpath(frozen_path, paths.run_root).replace(os.sep, "/"),
        "spec_digest": digest,
    }
    frozen = [row for row in frozen if row.get("spec_version") != spec_version]
    frozen.append(entry)
    frozen.sort(key=lambda row: row.get("spec_version", 0))
    meta["frozen"] = frozen
    dump_yaml(paths.run_yaml, meta)
