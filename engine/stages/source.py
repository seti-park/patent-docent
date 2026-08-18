# -*- coding: utf-8 -*-
"""`source` 스테이지 — 원천 정본 고정과 조기 보고.

계약 = `contracts/stages/source.yaml`(정본 서술 = SPEC §1.3).

**원천 취득은 엔진 범위 밖이다**(SPEC §9.0 E8). 이 스테이지는 이미 손에 있는 원문 파일을
받아 **정본화 변환**만 하고, 그 변환 목록과 원본·정본 양쪽의 SHA-256 을 `PROVENANCE.md` 에
남긴다. 되짚을 수 없는 변환은 변환이 아니라 훼손이다.

**조기 보고를 여기서 내는 이유**(재정 N12): 도면 수와 전시물 후보 수는 READ 의 전량 접지
비용을 지출하기 **전에** 확정된다. 형식 전제가 서지 않는 소재를 알아내려고 독해 2회분을
태우는 것은 순서가 뒤바뀐 것이다.

**런 결박을 거는 자리도 여기다**(재정 P-U1 · P-8). 파이프라인의 첫 스테이지가 진입 시점의
git 커밋을 확정해 `run.yaml#engine.commit` 에 기입한다(`_engine_pin`). 도구가 아니라 러너가
쓰는 이유는 SPEC §7.3 기입 주체 행 그대로다 — 기록 주체가 둘이면 "누가 쓴 값인가"가 다시
미정이 된다. 손으로 넣어야 하는 결박은 결박이 아니다.
"""

from __future__ import annotations

import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone

from reader.lib.inventory import find_claim_section, parse_source_claims
from reader.lib.report import CheckRow
from reader.lib.rules import Rules

from . import (
    StageEnvironmentError,
    StageError,
    StageHaltError,
    failure_entry,
    figures_manifest_digest,
    load_yaml,
    dump_yaml,
    sha256_bytes,
    verify_declared_inputs,
    write_json,
    write_text,
    worst_status,
)
from .. import gitpin
from ..paths import RunPaths, format_parameter, load_format_parameters, reader_version

STAGE_ID = "source"

# 정본화 변환 목록. 결정론이며 순서가 곧 정의다.
#   ②③의 근거 = 실측한 USPTO→마크다운 산출물에 NBSP 1,700여 개와 보이지 않는 곱셈 기호가
#   섞여 있었다. 이것은 특허 내용이 아니라 변환 아티팩트이며, 정본이 무엇인가를 정하는 일은
#   엔진 밖의 원천 생성 규약 소관이다(SPEC §1.3). 검사 1(`read.verbatim`)은 이 정본 위에서
#   정규화 **없이** 바이트 비교한다 — 그 규율은 그대로다.
NBSP = " "
INVISIBLE_TIMES = "⁢"

CANONICALIZATION = (
    ("nfc", "유니코드 NFC 정규화"),
    ("nbsp-to-space", f"U+00A0(NBSP) → U+0020 치환"),
    ("drop-invisible-times", "U+2062(INVISIBLE TIMES) 제거"),
    ("final-newline", "파일 끝 개행 보장"),
)

# 도면 파일명에서 도면 번호를 뽑는다(정렬 가능성 판정용).
FIGURE_NUMBER = re.compile(r"(\d+)")
# 계약 문언에서 정규식을 회수할 때 쓰는 백틱 인용 패턴.
BACKTICK_PATTERN = re.compile(r"`(\^[^`]+\$)`")


def canonicalize(raw: str) -> tuple[str, dict]:
    """원문 → 정본. 변환별 적용 횟수를 함께 돌려준다(PROVENANCE 의 근거)."""
    counts = {
        "nfc": 0,
        "nbsp-to-space": raw.count(NBSP),
        "drop-invisible-times": raw.count(INVISIBLE_TIMES),
        "final-newline": 0,
    }
    text = unicodedata.normalize("NFC", raw)
    counts["nfc"] = 0 if text == raw else 1
    text = text.replace(NBSP, " ")
    text = text.replace(INVISIBLE_TIMES, "")
    if not text.endswith("\n"):
        text = text + "\n"
        counts["final-newline"] = 1
    return text, counts


def _check_entry(contract: dict, check_id: str) -> dict:
    for entry in contract.get("checks_before_exit") or []:
        if entry.get("id") == check_id:
            return entry
    raise StageError(f"계약에 검사 {check_id} 가 없다")


def _run_id_pattern(contract: dict) -> re.Pattern:
    """`source.run-id` 판정 기준 문언에서 정규식을 회수한다(코드에 박지 않는다)."""
    criterion = str(_check_entry(contract, "source.run-id").get("criterion", ""))
    match = BACKTICK_PATTERN.search(criterion)
    if not match:
        raise StageError("source.run-id 판정 기준에서 정규식을 찾지 못했다")
    return re.compile(match.group(1))


def _figure_rows(figures_dir: str) -> list[dict]:
    """도면별 행 — 파일명·바이트·SHA-256·산정 규칙 적용 결과.

    재정이 내려오면 **원천을 다시 읽지 않고 소급 재계산**할 수 있어야 한다
    (`source.yaml#exhibit_candidates.recompute_requirement`).
    """
    rows: list[dict] = []
    for name in sorted(os.listdir(figures_dir)):
        path = os.path.join(figures_dir, name)
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as handle:
            payload = handle.read()
        number = FIGURE_NUMBER.search(name)
        rows.append(
            {
                "filename": name,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "figure_number": int(number.group(1)) if number else None,
                "counted_as": 1,
                "counting_unit": "source-figure-file",
            }
        )
    return rows


def _exhibit_block(contract: dict, figure_rows: list[dict], repo: str | None) -> dict:
    """전시물 후보 산정 블록. 산정식·태그·처분을 **계약에서 그대로** 옮긴다.

    ★ 개명(재정 P-5): `provisional_resolutions` → `resolutions`. 산정식이 **정식 승인**되어
    더는 잠정이 아니며, "첫 런 개시 전 Owner 재정 대상"이라 적던 `open` 필드는 폐기되었다.
    대신 `adjudicated_in`(재정 원장 좌표)과 `observation_metric`(채택률 관찰 지표)을 싣는다 —
    승인 사실과 그 승인을 실물로 검증할 지표가 보고에 함께 남아야 한다.
    `tag: "[가설]"` 은 유지된다: 산정식이 승인된 것과 그 산정식이 실물에서 옳은가는 별개다.
    """
    declared = contract.get("exhibit_candidates") or {}
    floor = format_parameter("tweet_count.value.min", repo)
    sheet = load_format_parameters(repo)
    return {
        "count": sum(row["counted_as"] for row in figure_rows),
        "tag": declared.get("tag"),
        "unit": declared.get("unit"),
        "formula": declared.get("formula"),
        "rationale": declared.get("rationale"),
        "adjudicated_in": declared.get("adjudicated_in"),
        "resolutions": declared.get("resolutions") or [],
        "observation_metric": declared.get("observation_metric") or {},
        "floor": {
            "value": floor,
            "source": "contracts/format-parameters.yaml#tweet_count.value.min",
            "sheet_version": str(sheet.get("version", "")),
        },
        "recompute_requirement": declared.get("recompute_requirement"),
    }


def _engine_pin(paths: RunPaths) -> tuple[str, str | None]:
    """런 결박 핀 `(커밋 40hex, worktree 또는 None)` 을 **러너가 스스로 확정한다**(재정 P-U1·P-8).

    재정 원문은 "런은 시작 시점의 git 커밋에 결박된다 … 예외 없음"이다. 손으로 넣어야 하는
    결박은 결박이 아니므로, 이 값은 사람도 도구도 아닌 **러너**가 진입 시점에 기입한다
    (`tools/run_worktree.py` 는 worktree 를 만들 뿐 `run.yaml` 을 쓰지 않는다 — SPEC §7.3
    기입 주체 행). 판정 자체는 `engine/gitpin.py` 한 곳에서 오며 도구도 같은 함수를 부른다.

    실패 두 갈래를 구별한다.

      · **더러운 작업 트리** → `halt`. 커밋되지 않은 변경은 커밋에 결박될 수 없다. 세계가
        고장 난 것이 아니라 런을 열 전제가 서지 않은 것이므로, 진단에 더러운 파일 목록을
        싣고 사람이 커밋·되돌림 후 다시 개시한다. 우회 스위치는 없다.
      · **git 부재·리포 아님** → **환경 오류**. 핀을 만들 수 없다는 뜻이고, 핀 없는 런은
        "무엇이 당시 법이었는가"에 답하지 못한다. 조용히 넘어가지 않는다(재정 P-C 와 같은 성질).

    기존 `run.yaml` 이 다른 커밋을 들고 있으면 덮어쓰지 않고 멈춘다 — **재개 런은 같은 커밋을
    쓴다**(재정 P-U1). 핀이 달라졌다면 그것은 재개가 아니라 새 런이다.
    """
    # 이 결박 기제 자신의 생성물은 더러움으로 세지 않는다 — worktree 루트와 이 런의 작업장.
    exclude = [gitpin.DEFAULT_WORKTREE_ROOT]
    run_rel = gitpin.relative_inside(paths.repo, paths.run_root)
    if run_rel:
        exclude.append(run_rel)

    try:
        commit, worktree = gitpin.resolve_pin(paths.repo, exclude_rels=exclude)
    except gitpin.DirtyWorktree as dirty:
        listed = "; ".join(gitpin.format_dirty(dirty.entries))
        raise StageHaltError(
            f"[halt] {gitpin.DIRTY_HEADLINE} · {len(dirty.entries)}건 — {listed} · "
            f"{gitpin.DIRTY_REMEDY}"
        ) from dirty
    except gitpin.GitUnavailable as exc:
        raise StageEnvironmentError(
            f"[환경 오류] 런 커밋 핀을 만들 수 없다: {exc} — 런은 시작 시점 git 커밋에 "
            "결박된다(재정 P-U1·P-8). 핀 없는 런은 열지 않는다"
        ) from exc

    if os.path.exists(paths.run_yaml):
        pinned = str((load_yaml(paths.run_yaml).get("engine") or {}).get("commit") or "")
        if pinned and pinned != commit:
            raise StageHaltError(
                f"[halt] run.yaml 의 기존 핀과 현재 HEAD 가 다르다: 기존 {pinned} · HEAD {commit} — "
                "재개 런은 같은 커밋을 쓴다(재정 P-U1). 커밋이 달라졌으면 그것은 새 런이다"
            )
    return commit, worktree


def _provenance_md(
    *,
    run_id: str,
    original_path: str,
    original_digest: str,
    canonical_digest: str,
    counts: dict,
    figure_rows: list[dict],
) -> str:
    lines: list[str] = []
    lines.append(f"# 원천 정본화 기록 — `{run_id}`")
    lines.append("")
    lines.append(
        "원천 취득은 엔진 범위 밖이다(SPEC §9.0 E8). 이 스테이지가 한 일은 **결정론 변환**과"
    )
    lines.append("**다이제스트 고정**뿐이며, 아래 목록이 그 전부다.")
    lines.append("")
    lines.append("## 1. 투입물")
    lines.append("")
    lines.append(f"- 경로: `{original_path}`")
    lines.append(f"- 원본 SHA-256: `{original_digest}`")
    lines.append("")
    lines.append("## 2. 적용한 변환 (순서가 곧 정의)")
    lines.append("")
    lines.append("| # | 변환 | 내용 | 적용 |")
    lines.append("|---|---|---|---|")
    for position, (key, label) in enumerate(CANONICALIZATION, start=1):
        lines.append(f"| {position} | `{key}` | {label} | {counts.get(key, 0)} |")
    lines.append("")
    lines.append(f"- 정본 SHA-256: `{canonical_digest}`")
    lines.append("")
    lines.append(
        "변환 ②③은 특허 내용이 아니라 변환 아티팩트를 지운다. 검사 1(`read.verbatim`)은 이 "
        "정본 위에서 정규화 없이 바이트 비교하며, 그 규율은 변하지 않는다."
    )
    lines.append("")
    lines.append("## 3. 도면 원본")
    lines.append("")
    lines.append("| 파일 | 바이트 | SHA-256 |")
    lines.append("|---|---|---|")
    for row in figure_rows:
        lines.append(f"| `{row['filename']}` | {row['bytes']} | `{row['sha256']}` |")
    lines.append("")
    return "\n".join(lines)


def run(
    *,
    run_root: str,
    source_patent_path: str,
    figures_dir: str,
    run_id: str,
    patent_meta: dict,
    run_kind: str = "rehearsal",
    repo: str | None = None,
) -> dict:
    """`00-source/` 를 고정하고 `source-report.json` 을 낸다.

    반환 = `{"rows", "report", "status", "reason_label"}`.
    """
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]

    # ⓪ 런 결박(재정 P-U1 · P-8) — 다른 무엇보다 먼저다. 이 런의 법(계약·스키마·검증기·러너)이
    #    어느 커밋에서 고정되는지를 확정하지 못하면 그 뒤의 어떤 산출물도 "어떤 법 아래
    #    만들어졌는가"에 답할 수 없다. 확정한 값은 아래 ④에서 run.yaml 에 기입된다.
    commit, worktree = _engine_pin(paths)

    with open(source_patent_path, "rb") as handle:
        raw_bytes = handle.read()
    original_digest = sha256_bytes(raw_bytes)
    canonical_text, counts = canonicalize(raw_bytes.decode("utf-8"))
    canonical_bytes = canonical_text.encode("utf-8")
    canonical_digest = sha256_bytes(canonical_bytes)

    # ① 진입 지문 검사(재정 P-C · P-U2). 투입물의 실재·지문을 기록하고, 런 작업장에 이미
    #    00-source/ 가 있으면 patent.md 지문과 **도면 세트 매니페스트 지문**을 대조한다.
    #    어긋나면 덮어쓰지 않고 즉시 중단한다 — 원천이 바뀌었을 때의 처분은 부분 복구가
    #    아니라 **새 런**이며(재정 P-U2), 바이트 오프셋 특성상 부분 재사용은 정확성 위반이다.
    #    구 런은 status: superseded-by-source-change 로 표시하고 상호 링크를 보존한다.
    verify_declared_inputs(
        paths,
        contract,
        STAGE_ID,
        inputs={
            "source_patent_path": source_patent_path,
            "figures_dir": figures_dir,
            "canonical_digest": canonical_digest,
        },
    )

    # ② 00-source/ 는 한 번만 쓴다(SPEC §7.4 — 이후 어떤 스테이지도 수정하지 못한다).
    #    지문이 같아도 재투입은 허용하지 않는다. 위 진입 검사가 통과했다는 것은 "바뀌지
    #    않았다"만 뜻하며, 그것이 "다시 써도 된다"는 뜻은 아니다.
    if os.path.exists(paths.patent_md):
        raise StageError(
            f"00-source/ 가 이미 고정되어 있다: {paths.patent_md} — "
            "원천 재투입은 런을 새로 만드는 일이다"
        )
    paths.ensure_source_dirs()

    write_text(paths.patent_md, canonical_text)
    write_text(paths.patent_sha256, canonical_digest + "\n")

    # ② 도면 원본 복사
    if os.path.isdir(figures_dir):
        for name in sorted(os.listdir(figures_dir)):
            origin = os.path.join(figures_dir, name)
            if os.path.isfile(origin):
                shutil.copy2(origin, os.path.join(paths.figures_raw, name))
    figure_rows = _figure_rows(paths.figures_raw)

    write_text(
        paths.provenance_md,
        _provenance_md(
            run_id=run_id,
            original_path=os.path.abspath(source_patent_path),
            original_digest=original_digest,
            canonical_digest=canonical_digest,
            counts=counts,
            figure_rows=figure_rows,
        ),
    )

    # ③ 조기 보고
    exhibit = _exhibit_block(contract, figure_rows, repo)
    report = {
        "stage": STAGE_ID,
        "run_id": run_id,
        "run_kind": run_kind,
        "source": {
            "input_path": os.path.abspath(source_patent_path),
            "original_sha256": original_digest,
            "canonical_sha256": canonical_digest,
            "canonical_bytes": len(canonical_bytes),
            "transforms": [
                {"id": key, "description": label, "applied": counts.get(key, 0)}
                for key, label in CANONICALIZATION
            ],
        },
        "figures": figure_rows,
        "figure_count": len(figure_rows),
        # ★ 도면 세트 매니페스트 지문(재정 P-U2). 원천은 patent.md 하나가 아니라 **도면 세트
        #   전체**이고, 세트의 변경(파일 추가·삭제·교체)은 파일 하나의 지문으로는 드러나지
        #   않는다. 하류 read.input-digest 가 이 값을 대조한다.
        #   ★ 생산 경로에 **재봉인(지문 재계산) 함수를 두지 않는다**(재정 P-U2). 이 값은
        #   봉인 시점에 한 번 산출되고 이후 갱신되지 않으며, 픽스처 재봉인 도구는 테스트
        #   하네스에만 산다 — 생산 경로에 재계산 자리가 있으면 "원천이 바뀌면 새 런"이라는
        #   규율이 스위치 하나로 우회된다.
        "figures_manifest_digest": figures_manifest_digest(
            (row["filename"], row["sha256"]) for row in figure_rows
        ),
        "exhibit_candidates": exhibit,
    }
    write_json(paths.source_report, report)

    # ④ run.yaml 골격 — 여기서 커밋 핀이 실물이 된다(재정 P-U1).
    _write_run_yaml(
        paths=paths,
        run_id=run_id,
        run_kind=run_kind,
        patent_meta=patent_meta,
        canonical_digest=canonical_digest,
        repo=repo,
        commit=commit,
        worktree=worktree,
    )

    # ⑤ 종료 전 검사 5종
    rows = _checks(
        paths=paths,
        contract=contract,
        run_id=run_id,
        canonical_text=canonical_text,
        canonical_digest=canonical_digest,
        figure_rows=figure_rows,
        exhibit=exhibit,
        manifest_digest=report["figures_manifest_digest"],
    )
    status, reason_label = _verdict(contract, rows)
    return {"rows": rows, "report": report, "status": status, "reason_label": reason_label}


def _write_run_yaml(
    *,
    paths: RunPaths,
    run_id: str,
    run_kind: str,
    patent_meta: dict,
    canonical_digest: str,
    repo: str | None,
    commit: str,
    worktree: str | None,
) -> None:
    """런 메타 골격(SPEC §7.3). 이미 있으면 원천 관련 필드와 **커밋 핀**만 갱신한다.

    핀은 `_engine_pin` 이 확정한 값이며(재정 P-U1·P-8), 빈 문자열 골격을 남기지 않는다 —
    빈 핀은 "아직 아무도 쓰지 않았다"를 "결박이 있다"처럼 보이게 만든다. 기존 블록의 다른
    필드(`gate_version` 등)는 보존한다.
    """
    existing = load_yaml(paths.run_yaml) if os.path.exists(paths.run_yaml) else {}
    patent = dict(patent_meta or {})
    patent.setdefault("source_path", "00-source/patent.md")
    patent["source_sha256"] = canonical_digest
    engine_block = dict(existing.get("engine") or {})
    engine_block["commit"] = commit
    engine_block["worktree"] = worktree
    engine_block.setdefault("gate_version", "")
    payload = {
        "schema": "run/v0",
        "run_id": run_id,
        "created_at": existing.get(
            "created_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ),
        "status": "active",
        "run_kind": run_kind,
        "patent": patent,
        "engine": engine_block,
        "reader_version": reader_version(repo),
        "numeric_whitelist": existing.get("numeric_whitelist", []),
    }
    for key in ("pens", "comparison_axis", "probe", "gate", "figures", "frozen"):
        if key in existing:
            payload[key] = existing[key]
    dump_yaml(paths.run_yaml, payload)


def _checks(
    *,
    paths: RunPaths,
    contract: dict,
    run_id: str,
    canonical_text: str,
    canonical_digest: str,
    figure_rows: list[dict],
    exhibit: dict,
    manifest_digest: str,
) -> list[CheckRow]:
    rules = Rules.load()
    rows: list[CheckRow] = []

    # source.digest-recorded
    row = CheckRow(check_id="source.digest-recorded", checked=1)
    recorded = ""
    if os.path.exists(paths.patent_sha256):
        with open(paths.patent_sha256, encoding="utf-8") as handle:
            recorded = handle.read().strip()
    if recorded != canonical_digest:
        row.add(
            "source.digest",
            "00-source/patent.sha256",
            recorded or "(없음)",
            canonical_digest,
            "기록된 다이제스트가 정본의 실제 SHA-256 과 다르다 — 이후 전 인용 검증의 기준점이 무너진다",
        )
    rows.append(row)

    # source.claims-section — READ 와 **같은 파서**를 쓴다(여기서 통과한 원천은 하류에서
    # 파서 문제로 다시 넘어지지 않는다).
    row = CheckRow(
        check_id="source.claims-section",
        ruleset="reader-rules#claim_inventory",
        ruleset_version=rules.version,
        ruleset_size=len(rules.inventory_rules),
        checked=1,
    )
    section = find_claim_section(canonical_text, rules)
    if not section.found:
        row.add(
            "source.claims-section",
            "00-source/patent.md",
            "(구간 없음)",
            "청구항 구간 헤더",
            "청구항 구간 경계를 찾지 못했다 — 원천 형식 문제이므로 자동 복구 대상이 아니다",
        )
    else:
        claims = parse_source_claims(canonical_text, rules)
        row.extras["source_claim_numbers"] = [claim.number for claim in claims]
        if not claims:
            row.add(
                "source.claims-section",
                "00-source/patent.md",
                "0건",
                "1건 이상",
                "구간은 찾았으나 청구항을 하나도 파싱하지 못했다",
            )
    rows.append(row)

    # source.figures-manifest
    row = CheckRow(check_id="source.figures-manifest", checked=len(figure_rows))
    if not figure_rows:
        row.add(
            "source.figures-manifest",
            "00-source/figures-raw/",
            "0개",
            "1개 이상",
            "도면 원본이 없다 — 전시 스톱을 세울 자산이 존재하지 않는다",
        )
    for entry in figure_rows:
        if entry["figure_number"] is None:
            row.add(
                "source.figures-manifest",
                f"00-source/figures-raw/{entry['filename']}",
                entry["filename"],
                "파일명에 도면 번호",
                "파일명으로 도면 번호를 정렬할 수 없다",
            )
    rows.append(row)

    # source.figures-manifest-digest — 세트 지문이 실제 봉인분과 일치하는가(재정 P-U2).
    row = CheckRow(check_id="source.figures-manifest-digest", checked=len(figure_rows))
    actual_manifest = figures_manifest_digest(
        (entry["filename"], entry["sha256"]) for entry in figure_rows
    )
    if actual_manifest != manifest_digest:
        row.add(
            "source.figures-manifest-digest",
            "00-source/source-report.json#figures_manifest_digest",
            manifest_digest,
            actual_manifest,
            "매니페스트 지문이 봉인된 도면 세트와 다르다 — 하류 진입 검사의 기준점이 어긋난다",
        )
    row.extras["figures_manifest_digest"] = actual_manifest
    rows.append(row)

    # source.run-id
    pattern = _run_id_pattern(contract)
    row = CheckRow(check_id="source.run-id", checked=1)
    if not pattern.fullmatch(run_id):
        row.add(
            "source.run-id",
            "run.yaml#run_id",
            run_id,
            pattern.pattern,
            "런 ID 문법 위반(SPEC §7.1) — 디렉토리 재생성이 필요하다",
        )
    directory = os.path.basename(paths.run_root)
    if directory != run_id:
        row.add(
            "source.run-id",
            "runs/<run-id>/",
            directory,
            run_id,
            "런 디렉터리명과 run_id 가 다르다",
        )
    rows.append(row)

    # source.exhibit-candidates — 하한의 정본은 형식 파라미터 시트다(재정 N12).
    floor = exhibit["floor"]["value"]
    row = CheckRow(
        check_id="source.exhibit-candidates",
        ruleset="format-parameters#tweet_count",
        ruleset_version=exhibit["floor"]["sheet_version"],
        ruleset_size=1,
        checked=1,
    )
    row.extras["exhibit_candidates"] = exhibit["count"]
    row.extras["floor"] = floor
    if len(figure_rows) < 1 or exhibit["count"] < floor:
        row.add(
            "source.exhibit-candidates",
            "00-source/source-report.json#exhibit_candidates",
            f"도면 {len(figure_rows)}개 · 후보 {exhibit['count']}개",
            f"도면 1개 이상 · 후보 {floor}개 이상",
            "형식 전제가 서지 않는다 — 독해 2회분을 태우기 전에 멈춘다(재정 N12)",
        )
    rows.append(row)
    return rows


def _verdict(contract: dict, rows: list[CheckRow]) -> tuple[str, str | None]:
    """검사 결과 → 조치·사유. 매핑의 정본은 계약의 `failure` 목록이다."""
    failures = {row.check_id for row in rows if row.status == "fail"}
    statuses: list[str] = []
    reason_label: str | None = None

    if "source.digest-recorded" in failures:
        statuses.append(str(failure_entry(contract, "원천 텍스트 취득 실패").get("action")))
    if "source.claims-section" in failures:
        statuses.append(str(failure_entry(contract, "청구항 구간 경계 식별 실패").get("action")))
    if failures & {"source.figures-manifest", "source.exhibit-candidates"}:
        entry = failure_entry(contract, "전시물 후보")
        statuses.append(str(entry.get("action")))
        reason_label = entry.get("reason_label")
    if "source.figures-manifest-digest" in failures:
        # 세트 지문이 봉인분과 어긋나면 하류 진입 검사가 근거 없는 값을 대조하게 된다 —
        # 원천 변경과 같은 층의 사고이므로 같은 행의 조치를 쓴다(재정 P-U2).
        statuses.append(str(failure_entry(contract, "원천 변경 감지").get("action")))
    if "source.run-id" in failures:
        statuses.append(str(failure_entry(contract, "run_id 형식 위반").get("action")))

    status = worst_status(statuses or ["ok"])
    if status == "halt":
        # halt 는 사유 라벨을 쓰지 않는다 — escalate 의 두 사유(형식 전제 미충족 /
        # 안도감 부적합)를 구별하기 위한 어휘이기 때문이다(재정 N12 · 글로사리 §4).
        reason_label = None
    return status, reason_label
