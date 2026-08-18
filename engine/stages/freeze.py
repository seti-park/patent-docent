# -*- coding: utf-8 -*-
"""`freeze` 스테이지 — 승인된 재료에 버전 스탬프와 다이제스트를 찍고 읽기 전용화한다.

계약 = `contracts/stages/freeze.yaml`(정본 서술 = SPEC §1.6).

★ `freeze.approval-valid` 은 스키마 밖 3항을 **추가로** 본다(M0.6 재감수 M-01 잔여의 처분).

① `extensions.docent.drop_signal.verdict == "drop-proposed"` 면 `drop_decision` 필수
   (경로 정정 — 층 분리로 drop 은 docent 확장 블록에 산다: 재정 P-2 ⓑ. 확정 재정의 자리는
   CP1 한 곳이다: 재정 P-A)
② `derived_fact_ack[]` 집합 == `origin: "derived"` 항목 집합 (부분집합이 아니라 **정확히 일치**)
③ `manual_verification_ack[]` 집합 == `origin: "figure-sourced"` 항목 집합

대조 없는 목록은 승인이 아니라 **서명**이다 — 빈 목록도 유령 ID 도 통과하던 자리가 여기였다.
빠진 id 와 유령 id 는 각각 별도 결함으로 낸다(수정 지시가 무엇을 지목해야 하는지 다르다).

★★ 더해 봉투의 **신원** 4항을 본다(sol 재감수 BLOCKER B-02 의 처분). 그전까지 검증되던 것은
`decision` · `owner_quote` · `target.digest` 뿐이어서, 다음이 전부 동결을 통과했다 —
CP2 봉투(`checkpoint: "ship_approval"`)로 재료를 동결 · **다른 런**의 봉투 · `run.yaml` 을
가리키는 봉투(그 파일의 올바른 해시를 들면 해시 대조도 통과한다) · `../` 로 런 밖을 가리키는 봉투.
해시가 맞는다는 것은 "대상이 바뀌지 않았다"만 증명하며 "그것이 승인 대상이다"는 증명하지 않는다.
이는 CP1 의 오보가 아니라 **우회**였다(헌장 D6 · 재정 R8).

④ `checkpoint == "material_approval"` — 체크포인트 종류
⑤ `run_id == run.yaml#run_id` — 런 신원
⑥ `target.path` 가 **정확히** 재료 명세(계약 선언에서 유도한 런 상대 경로)
⑦ `target.path` 의 realpath 가 런 루트 안 — **파일을 열기 전에** 판정한다

⑦의 순서가 규율이다. 런 밖 파일을 읽고 나서 거부하는 것은 이미 읽은 것이며, 거부 사유를
"해시 불일치"로 적는 순간 무엇이 잘못됐는지도 흐려진다.
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
    verify_declared_inputs,
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


def _cp1_checkpoint_id(paths: RunPaths) -> str:
    """CP1 체크포인트 id 의 정본 = `contracts/stages/read.yaml#owner_checkpoint.id`.

    러너가 `"material_approval"` 을 따로 들고 있으면 계약이 바뀔 때 한쪽이 낡는다.
    """
    checkpoint = paths.contracts["read"].get("owner_checkpoint") or {}
    declared = checkpoint.get("id")
    if not isinstance(declared, str) or not declared:
        raise StageError(
            "read 계약이 owner_checkpoint.id 를 선언하지 않았다 — 봉투 신원을 대조할 기준이 없다"
        )
    return declared


def _inside_run(run_root: str, candidate: str) -> bool:
    """대상 경로가 런 작업장 안인가. **파일을 열기 전에** 묻는 질문이다.

    `os.path.join` 은 `..` 를 막지 않는다 — 이어 붙일 뿐이다. 심링크까지 풀어(`realpath`)
    실제로 닿는 자리를 보고, 런 루트와 같거나 그 아래일 때만 참이다. 런 밖을 읽고 나서
    "해시가 다르다"고 거부하는 것은 이미 읽은 것이다.
    """
    root = os.path.realpath(run_root)
    target = os.path.realpath(candidate)
    return target == root or target.startswith(root + os.sep)


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


# 판독본이 **값 그대로** 실어야 하는 필드(재정 P-U5 · freeze.yaml#freeze.render-parity).
# 항목 kind 별 단일 문자열 필드와 배열 필드를 따로 적는다.
PARITY_TEXT_FIELDS = (
    "label_en",
    "statement_en",
    "what_it_shows_en",
    "background_problem",
    "asserted_effect",
    "delta",
    "text_verbatim",
    "caption_quote",
)
# ★ `search_note` 는 대상이 아니다 — KR 규정 필드이며 계약이 든 대조 목록에 없다
#   (`freeze.yaml#freeze.render-parity`). 판독본은 그것을 렌더하지만 검사 관할은 EN 값이다.
PARITY_LIST_FIELDS = ("evidence_quotes", "quotes")


def _parity_values(spec: dict) -> list[tuple[str, str, str]]:
    """판독본에 바이트 그대로 있어야 하는 `(좌표, 필드, 값)` 전량.

    ★ 대상은 **ID 가 아니라 값**이다(재정 P-U5). 구 구현은 `items[].id` 가 문서에 1회
    등장하는지만 봤고, 그래서 판독본이 값을 잃어도(요약·의역·절단) 통과했다. 판독본은
    KR 틀 + EN 값이므로 검사 대상은 그 값이며, 파생 번역이 값을 대체하면 이 대조가 잡는다.
    """
    out: list[tuple[str, str, str]] = []

    def note(locus: str, field: str, value) -> None:
        if isinstance(value, str) and value:
            out.append((locus, field, value))

    for item in spec.get("items") or []:
        item_id = str(item.get("id"))
        for field in PARITY_TEXT_FIELDS:
            note(f"items#{item_id}", field, item.get(field))
        for field in PARITY_LIST_FIELDS:
            for position, value in enumerate(item.get(field) or []):
                note(f"items#{item_id}", f"{field}[{position}]", value)
        for position, ref in enumerate(item.get("spec_refs") or []):
            note(f"items#{item_id}", f"spec_refs[{position}].quote", (ref or {}).get("quote"))
        for position, ref in enumerate(item.get("figure_refs") or []):
            note(
                f"items#{item_id}",
                f"figure_refs[{position}].caption_quote",
                (ref or {}).get("caption_quote"),
            )
        source = item.get("source") or {}
        note(f"items#{item_id}", "source.quote", source.get("quote"))

    claims = spec.get("claims") or {}

    def walk(elements, claim_id: str) -> None:
        for element in elements or []:
            note(f"claims#{claim_id}/{element.get('id')}", "text_verbatim", element.get("text_verbatim"))
            walk(element.get("children") or [], claim_id)

    for claim in claims.get("independent") or []:
        claim_id = str(claim.get("id"))
        note(f"claims#{claim_id}", "text_verbatim", claim.get("text_verbatim"))
        walk(claim.get("elements") or [], claim_id)
    for claim in claims.get("dependents") or []:
        claim_id = str(claim.get("id"))
        note(f"claims#{claim_id}", "text_verbatim", claim.get("text_verbatim"))
        for addition in claim.get("additions") or []:
            note(
                f"claims#{claim_id}/{addition.get('id')}",
                "text_verbatim",
                addition.get("text_verbatim"),
            )
    for position, interest in enumerate(claims.get("applicant_interest") or []):
        note(f"claims#applicant_interest[{position}]", "signal", interest.get("signal"))

    for figure in spec.get("figures") or []:
        note(f"figures#{figure.get('id')}", "caption_quote", figure.get("caption_quote"))
    return out


def _render_parity(row: CheckRow, spec: dict, rendered: str) -> None:
    """판독본에 각 항목의 **EN 값이 바이트 그대로 존재**하는가(재정 P-U5).

    ★ 폐기: 구 판정 "모든 `items[].id` 가 1회 이상 등장". ID 존재만 보면 판독본이 값을
    잃어도 통과하며, 그것이 CP1 표면의 완결성을 보증한다는 말은 실제보다 넓은 주장이었다.
    """
    values = _parity_values(spec)
    row.checked = len(values)
    for locus, field, value in values:
        if value not in rendered:
            row.add(
                "freeze.render-parity",
                f"10-read/material-spec.md ← {locus}.{field}",
                "(값 부재)",
                value,
                "CP1 판독본에 이 값이 바이트 그대로 없다 — 요약·의역이 값을 대체했거나 절이 빠졌다",
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

    # ★ 진입 지문 검사(재정 P-C). 보는 것은 **선언된 입력**(재료 명세·판독본의 실재와, 그
    #   재료가 이 런의 원천 위에서 만들어졌는가)까지다. 봉투는 이 층에 오지 않는다 —
    #   부재·신원 위조·target.digest 실효 전부 아래 출구 검사(freeze.approval-valid)의 몫이며,
    #   특히 **봉투 실효는 환경 오류가 아니라 정상적인 생애 사건**(승인 후 재료 개정 → 자동
    #   실효 → 재승인)이므로 판정 행에 남아야 한다(재정 R8 · P-C). 그래서 봉투 경로를
    #   진입 검사에 넘기지 않는다.
    verify_declared_inputs(paths, contract, STAGE_ID)

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

    # ② 봉투 신원 — 이 체크포인트의, 이 런의 봉투인가(재감수 B-02).
    checkpoint_id = _cp1_checkpoint_id(paths)
    if envelope.get("checkpoint") != checkpoint_id:
        approval_row.add(
            "approval.checkpoint",
            "checkpoint",
            str(envelope.get("checkpoint")),
            checkpoint_id,
            "다른 체크포인트의 봉투로는 재료를 동결하지 않는다 — CP2 승인이 CP1 을 대신하지 않는다(D6)",
        )
    declared_run_id = str((load_yaml(paths.run_yaml) or {}).get("run_id", ""))
    if str(envelope.get("run_id", "")) != declared_run_id:
        approval_row.add(
            "approval.run-id",
            "run_id",
            str(envelope.get("run_id")),
            declared_run_id or "(run.yaml 에 run_id 없음)",
            "다른 런의 승인 봉투다 — 승인은 런 밖으로 옮겨 붙지 않는다",
        )

    # ③ 대상 결속 — "무엇을 승인했는가"(경로)와 "그것이 바뀌지 않았는가"(해시)는 다른 질문이다.
    #    해시 일치는 대상의 불변만 증명하고 대상의 정체는 증명하지 않는다(B-02).
    target = envelope.get("target") or {}
    declared_target = str(target.get("path", ""))
    expected_target = os.path.relpath(paths.material_spec_json, paths.run_root).replace(
        os.sep, "/"
    )
    target_path = os.path.join(paths.run_root, *declared_target.split("/"))
    if declared_target != expected_target:
        approval_row.add(
            "approval.target-is-material-spec",
            "target.path",
            declared_target or "(비어 있음)",
            expected_target,
            "봉투가 재료 명세 아닌 파일을 가리킨다 — 해시가 맞아도 그것은 승인 대상이 아니다",
        )
    if not _inside_run(paths.run_root, target_path):
        # 열기 전에 끊는다. 아래 존재·해시 검사로 내려보내면 런 밖 파일을 읽게 된다.
        approval_row.add(
            "approval.target-inside-run",
            "target.path",
            declared_target or "(비어 있음)",
            "런 작업장 안의 경로",
            "봉투 대상이 런 밖을 가리킨다 — 읽지 않고 거부한다(런 밖 파일은 이 런의 승인 대상이 아니다)",
        )
    elif not os.path.isfile(target_path):
        approval_row.add(
            "approval.target-missing",
            "target.path",
            declared_target or "(비어 있음)",
            "런 안의 실재 파일",
            "봉투가 가리키는 대상 파일이 없다",
        )
    else:
        actual = sha256_file(target_path)
        if actual != target.get("digest"):
            # ★ 이 자리는 **도달 가능해야** 한다(재정 R8). 한때 진입 지문 검사가 같은
            #   불일치를 먼저 환경 오류로 삼켜 여기 제어가 닿지 않았고, 그 동안 판정문에서
            #   재승인 경로가 사라졌다. 승인 후 재료가 바뀌는 것은 결함이 아니라 정상적인
            #   생애 사건이며, 그 처분은 진단이 아니라 **재승인**이다.
            approval_row.add(
                "approval.target-digest",
                "target.digest",
                str(target.get("digest")),
                actual,
                "승인 시점 대상과 현재 파일이 다르다 — 봉투는 자동 실효한다. 처분은 재승인이다(재정 R8)",
            )

    # ④ 스키마 밖 3항
    # ★ 경로 정정(재정 P-2 ⓑ): drop 은 공유 코어가 아니라 docent 확장 블록에 산다.
    #   구 경로(최상위 `drop_signal`)를 보던 판은 층 분리 이후 **언제나 빈 값**을 읽어
    #   drop 제안이 처분 없이 승인되는 통로가 된다.
    drop_signal = ((spec.get("extensions") or {}).get("docent") or {}).get("drop_signal") or {}
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
        # 조치의 정본은 계약의 failure 목록이다. 봉투 **실효**(target.digest)는 계약이 별도
        # 행으로 든 조건이므로 그 행을 조회한다 — 조치는 같은 halt 지만, 어느 조건으로 멈췄는지가
        # 계약에서 조회되어야 "재승인 필요"라는 처분이 계약 문언에 붙어 있게 된다(재정 R8).
        stale = any(finding.rule == "approval.target-digest" for finding in approval_row.findings)
        statuses.append(
            str(
                failure_entry(
                    contract, "target.digest 불일치" if stale else "승인 봉투 부재"
                ).get("action")
            )
        )

    # ⑤ 원천 다이제스트 대조
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

    # ⑥ 렌더 패리티
    parity_row = CheckRow(check_id="freeze.render-parity", checked=len(spec.get("items") or []))
    _render_parity(parity_row, spec, read_text(paths.material_spec_md))
    if parity_row.status == "fail":
        statuses.append(str(failure_entry(contract, "freeze.render-parity 실패").get("action")))
    rows.append(parity_row)

    # ⑦ 개정 검사 2종(reader/lib) — 직전 판이 있으면 그것과 대조한다.
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

    # ⑧ 동결 — 덮어쓰기 금지(§7.6). 개정은 새 파일이며 옛 판을 지우지 않는다.
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

    # ⑨ 읽기 전용 확인 — "동결"이 이름뿐이 되지 않게 실제 모드를 본다.
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
