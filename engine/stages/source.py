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


def _engine_pin(paths: RunPaths, contract: dict) -> tuple[str, str | None]:
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

    ★ 이 검사는 진입 검사(재정 P-U2 의 원천 변경 표시)보다 **먼저** 돈다. 순서는 재정
    2026-08-19 Q3 이 ⓑ 로 확정했다 — 순서를 바꾸지 않고 **핀 불일치 halt 의 진단문이 그
    귀결을 스스로 말하게 한다**. 귀결은 이렇다: 원천 변경과 리포 개정이 함께 오면(실무에서
    흔하다) 여기서 먼저 넘어지므로 구 런에는 `superseded-by-source-change` 표시가 **아직
    서지 않는다**. 그 사실을 사람이 알지 못하면 "표시가 없으니 원천은 그대로였다"로 읽는다.
    `contract` 를 받는 이유도 그것이다 — 표시의 어휘는 계약이 들고(코드가 리터럴로 들면
    두 벌이 되어 한 벌이 낡는다) 진단문은 그 값을 전사한다.
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
                "재개 런은 같은 커밋을 쓴다(재정 P-U1). 커밋이 달라졌으면 그것은 새 런이다. "
                + _pin_halt_supersede_note(contract, pinned)
            )
    return commit, worktree


def _pin_halt_supersede_note(contract: dict, pinned: str) -> str:
    """핀 불일치 halt 의 뒷문장 — **P-U2 표시가 아직 서지 않았다**(재정 2026-08-19 Q3 ⓑ).

    이 문장이 없으면 halt 는 자기가 무엇을 남기지 **않았는지**를 말하지 않는다. 원천 변경은
    실무에서 리포 개정과 함께 오고, 그때 이 halt 를 먼저 만난 사람은 구 런의 `run.yaml` 을
    열어 보고 표시가 없는 것을 확인한 뒤 "원천은 바뀌지 않았다"고 읽는다 — 실제로는 원천
    변경 감지 자체가 아직 돌지 않았을 뿐이다.
    """
    try:
        marking = _marking_term(contract, "old_run", "status")
    except StageError:
        # 계약이 어휘를 선언하지 않았다면 그 사실을 적는다. 리터럴로 메우지 않는다 —
        # 어휘의 정본은 계약이고, 여기서 지어내면 두 벌 중 하나가 낡는다.
        marking = "(계약이 old_run.status 를 선언하지 않았다)"
    return (
        f"★ 이 halt 가 **원천 변경과 함께** 왔다면(구 런 작업장에 바뀐 원천을 재투입한 경우) "
        f"구 런에는 아직 아무 표시도 서지 않았다 — 핀 검사(재정 P-U1)가 진입 검사보다 먼저 "
        f"돌고, 원천 변경 표시(재정 P-U2 · run.yaml#status = {marking})는 그 진입 검사가 "
        f"넘어질 때 선다. 표시의 부재는 '원천이 그대로였다'가 아니라 '아직 보지 않았다'는 "
        f"뜻이다. 처방: 작업 트리를 이 런의 핀 커밋 {pinned} 에 세우고(같은 커밋의 격리 "
        f"체크아웃을 그 커밋 위에서 다시 만들면 된다 — tools/run_worktree.py create 는 같은 "
        f"커밋에 멱등이다) 같은 투입물로 다시 개시하면, 그때 진입 검사가 원천 변경을 감지해 "
        f"구 런에 표시와 진단을 남긴다. 그 뒤에 새 런을 열고 supersedes_run_root 로 구 런을 "
        f"가리키면 상호 링크가 닫힌다"
    )


# ---------------------------------------------------------------------------
# 원천 변경 처분 — 표시·상호 링크·진단 (재정 P-U2)
# ---------------------------------------------------------------------------


def _source_change_policy(contract: dict) -> dict:
    """원천 변경 처분 정책 블록. 상태값·필드명의 **정본은 계약**이고 러너는 읽을 뿐이다.

    코드가 `superseded-by-source-change` 를 리터럴로 들면 어휘가 두 벌이 되고, 두 벌이 되면
    한 벌은 반드시 낡는다 — `failure_entry` 가 사유 라벨을 계약에서 전사하는 규율과 같다.
    """
    policy = contract.get("source_change_policy")
    if not isinstance(policy, dict):
        raise StageError("계약에 source_change_policy 가 없다(재정 P-U2)")
    return policy


def _marking_term(contract: dict, side: str, key: str) -> str:
    """`source_change_policy.marking.<side>.<key>` 한 낱말. 선언이 없으면 그 자리에서 넘어진다."""
    marking = _source_change_policy(contract).get("marking") or {}
    value = (marking.get(side) or {}).get(key)
    if not isinstance(value, str) or not value:
        raise StageError(f"계약 source_change_policy.marking.{side}.{key} 선언이 없다")
    return value


def _dir_entries(directory: str) -> dict[str, tuple[int, str]]:
    """`{파일명: (바이트, 지문)}`.

    지문만 들지 않고 **바이트까지** 드는 이유 = 진단이 "무엇이 **얼마나** 달라졌는가"에
    답해야 하기 때문이다(재정 P-U2 — 변경 내용은 파일·규모로 명시한다). 지문만으로는
    "달라졌다"까지밖에 말하지 못하고, 그것만으로는 재취득이 옳았는지 판정할 수 없다.
    """
    out: dict[str, tuple[int, str]] = {}
    if not os.path.isdir(directory):
        return out
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as handle:
            payload = handle.read()
        out[name] = (len(payload), sha256_bytes(payload))
    return out


def _change_row(
    path: str, old: tuple[int, str] | None, new: tuple[int, str] | None
) -> dict | None:
    """변경 1건의 행. 같으면 `None`(행을 만들지 않는다 — 무변경까지 적으면 진단이 아니라 목록이다)."""
    if old == new:
        return None
    kind = "modified" if old and new else ("added" if new else "removed")
    old_bytes = old[0] if old else None
    new_bytes = new[0] if new else None
    return {
        "path": path,
        "change": kind,
        "old_sha256": old[1] if old else None,
        "new_sha256": new[1] if new else None,
        "old_bytes": old_bytes,
        "new_bytes": new_bytes,
        "byte_delta": (new_bytes or 0) - (old_bytes or 0),
    }


def _source_changes(
    paths: RunPaths, *, figures_dir: str, canonical_bytes: bytes, canonical_digest: str
) -> list[dict]:
    """봉인분 ↔ 새 투입물의 **차이 목록**. 비어 있으면 원천은 바뀌지 않은 것이다.

    이 함수가 진입 검사와 별도로 존재하는 이유 — 진입 검사(`verify_declared_inputs`)는
    "어긋났는가"를 판정할 뿐 "무엇이 얼마나"를 남기지 않는다. 그리고 진입 검사의 실패에는
    원천 변경 말고도 **투입물 부재**가 섞여 있다. 둘을 같은 표시로 처리하면 파일 하나가
    없어진 사고가 "원천이 바뀌었다"로 기록된다 — 그래서 표시는 이 목록이 비지 않을 때만
    선다(정직한 경로가 벌받지 않아야 한다).
    """
    changes: list[dict] = []
    if os.path.isfile(paths.patent_md):
        with open(paths.patent_md, "rb") as handle:
            sealed = handle.read()
        row = _change_row(
            "00-source/patent.md",
            (len(sealed), sha256_bytes(sealed)),
            (len(canonical_bytes), canonical_digest),
        )
        if row:
            changes.append(row)

    sealed_figures = _dir_entries(paths.figures_raw)
    incoming_figures = _dir_entries(figures_dir)
    for name in sorted(set(sealed_figures) | set(incoming_figures)):
        row = _change_row(
            f"00-source/figures-raw/{name}",
            sealed_figures.get(name),
            incoming_figures.get(name),
        )
        if row:
            changes.append(row)
    return changes


def _changes_summary(changes: list[dict]) -> str:
    """변경 목록 → 한 줄. 진단문과 파일에 **같은 문장**이 실리게 하려고 한 곳에서 만든다."""
    parts: list[str] = []
    for row in changes:
        label = {"modified": "수정", "added": "추가", "removed": "삭제"}[row["change"]]
        old_size = row["old_bytes"] if row["old_bytes"] is not None else "-"
        new_size = row["new_bytes"] if row["new_bytes"] is not None else "-"
        size = f"{old_size}→{new_size} bytes({row['byte_delta']:+d})"
        parts.append(
            f"{row['path']} {label} {size} "
            f"{row['old_sha256'] or '(없음)'} → {row['new_sha256'] or '(없음)'}"
        )
    return f"변경 {len(changes)}건: " + " · ".join(parts)


def _mark_superseded(
    paths: RunPaths,
    contract: dict,
    *,
    changes: list[dict],
    input_path: str,
    sealed_manifest: str,
    incoming_manifest: str,
) -> str:
    """구 런의 **메타에만** 표시를 남긴다(재정 P-U2). 반환 = 진단 한 줄.

    ★ 이 함수가 여는 파일은 `run.yaml` 하나다. `00-source/` 의 봉인물(patent.md ·
      patent.sha256 · figures-raw/)은 다시 쓰지 않는다 — 이 보수는 덮어쓰기 거부를 없애는
      일이 아니라 그 거부의 **흔적을 남기는** 일이다. 봉인에 손이 닿는 순간 "원천이 바뀌면
      새 런"이라는 규율은 표시 절차에 딸린 뒷문을 얻는다.
    ★ `superseded_by` 가 null 인 채로 표시가 서는 것이 **정상**이다. 감지 시점에 신 런은
      아직 없기 때문이며, 그 미완성 상태의 뜻(`link_state: pending`)을 파일 자신이 적는다 —
      "링크가 아직 비었다"와 "링크를 잃었다"를 사람이 구별할 수 있어야 한다.
    """
    summary = _changes_summary(changes)
    if not os.path.isfile(paths.run_yaml):
        # 표시를 남길 메타 자체가 없다. 조용히 넘어가지 않고 그 사실을 진단에 싣는다.
        return f"{summary} · 구 런에 run.yaml 이 없어 표시를 남기지 못했다"

    policy = _source_change_policy(contract)
    status_value = _marking_term(contract, "old_run", "status")
    link_field = _marking_term(contract, "old_run", "cross_link_field")
    diagnostics_field = _marking_term(contract, "old_run", "diagnostics_field")
    link_states = (policy.get("marking") or {}).get("link_states") or {}

    meta = load_yaml(paths.run_yaml)
    meta["status"] = status_value
    meta.setdefault(link_field, None)
    meta[diagnostics_field] = {
        "ruling": policy.get("ruling"),
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link_state": "pending" if meta.get(link_field) in (None, "") else "linked",
        "link_note": str(link_states.get("pending", "")),
        "input_path": os.path.abspath(input_path),
        "summary": summary,
        "changes": changes,
        "figures_manifest_digest": {"old": sealed_manifest, "new": incoming_manifest},
    }
    dump_yaml(paths.run_yaml, meta)
    return (
        f"{summary} · 구 런 표시: run.yaml#status={status_value} · "
        f"{link_field}=null(신 런 미정 — 처분은 새 런이다)"
    )


def _supersedes_target(
    contract: dict, supersedes_run_root: str, repo: str | None, new_run_id: str
) -> tuple[RunPaths, str]:
    """승계 대상(구 런)을 열어 신원을 확인한다 — **봉인 전에** 본다(재정 P-U2).

    링크는 표시의 뒤를 따른다. 표시되지 않은 런을 승계로 적으면 "왜 대체되었는가"가 사라진
    링크가 남고, 그 링크는 사료가 아니라 주장이다. 그래서 구 런이 `superseded-by-source-change`
    로 서 있지 않으면 여기서 넘어진다.
    """
    old_paths = RunPaths(supersedes_run_root, repo)
    if not os.path.isfile(old_paths.run_yaml):
        raise StageError(f"승계 대상 런에 run.yaml 이 없다: {old_paths.run_yaml}")
    meta = load_yaml(old_paths.run_yaml)
    status_value = _marking_term(contract, "old_run", "status")
    link_field = _marking_term(contract, "old_run", "cross_link_field")
    if str(meta.get("status") or "") != status_value:
        raise StageError(
            f"승계 대상 런이 {status_value} 로 표시되어 있지 않다: "
            f"status={meta.get('status')!r} — 링크는 표시의 뒤를 따른다(재정 P-U2)"
        )
    linked = meta.get(link_field)
    if linked and str(linked) != new_run_id:
        raise StageError(
            f"이미 다른 런에 승계되었다: {link_field}={linked!r} — 승계는 한 번뿐이고, "
            "링크를 갈아 끼우면 앞선 승계의 사료가 사라진다"
        )
    old_run_id = str(meta.get("run_id") or "")
    if not old_run_id:
        raise StageError(f"승계 대상 런의 run.yaml 에 run_id 가 없다: {old_paths.run_yaml}")
    return old_paths, old_run_id


def _close_cross_link(old_paths: RunPaths, contract: dict, *, new_run_id: str) -> None:
    """구 런의 링크 절반을 채운다 — 여기서 왕복이 닫힌다(재정 P-U2).

    신 런의 `run.yaml` 이 실물이 된 **뒤에** 부른다. 순서가 반대이면 구 런이 존재하지 않는
    런을 가리키는 창이 생기고, 그 창에서 죽으면 링크가 유령을 가리킨 채 남는다.
    """
    link_field = _marking_term(contract, "old_run", "cross_link_field")
    diagnostics_field = _marking_term(contract, "old_run", "diagnostics_field")
    meta = load_yaml(old_paths.run_yaml)
    meta[link_field] = new_run_id
    block = meta.get(diagnostics_field)
    if isinstance(block, dict):
        link_states = (_source_change_policy(contract).get("marking") or {}).get(
            "link_states"
        ) or {}
        block["link_state"] = "linked"
        block["link_note"] = str(link_states.get("linked", ""))
        block["linked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        meta[diagnostics_field] = block
    dump_yaml(old_paths.run_yaml, meta)


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
    supersedes_run_root: str | None = None,
) -> dict:
    """`00-source/` 를 고정하고 `source-report.json` 을 낸다.

    반환 = `{"rows", "report", "status", "reason_label"}`.

    `supersedes_run_root` = 이 런이 **대체하는 구 런의 작업장**(재정 P-U2). 원천이 바뀌면
    처분은 언제나 새 런이고, 그 새 런이 열릴 때 상호 링크의 나머지 절반이 닫힌다. 경로를
    추측하지 않고 인자로 받는 이유는 이 리포의 규율 그대로다 — 경로는 드러나야 한다.
    """
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]

    # ⓪ 런 결박(재정 P-U1 · P-8) — 다른 무엇보다 먼저다. 이 런의 법(계약·스키마·검증기·러너)이
    #    어느 커밋에서 고정되는지를 확정하지 못하면 그 뒤의 어떤 산출물도 "어떤 법 아래
    #    만들어졌는가"에 답할 수 없다. 확정한 값은 아래 ④에서 run.yaml 에 기입된다.
    commit, worktree = _engine_pin(paths, contract)

    # ⓪' 승계 대상 확인(재정 P-U2). 봉인 **전에** 본다 — 링크가 설 수 없는 상태(표시 없음·
    #    이미 다른 런에 승계됨)라면 이 런은 열리기 전에 멈춰야 한다. 산출물을 만든 뒤에
    #    링크에서 넘어지면 반쯤 열린 런이 남는다.
    old_paths: RunPaths | None = None
    supersedes_id: str | None = None
    if supersedes_run_root:
        old_paths, supersedes_id = _supersedes_target(
            contract, supersedes_run_root, repo, run_id
        )

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
    #
    #    ★ 그 표시를 **여기서 실물로** 남긴다. 표시가 계약과 주석에만 있으면 "폐기하되 지우지
    #    않는다"는 규율이 문서상의 말로만 산다(sol 재감수 P-U2 = 부분). 표시는 구 런의 메타
    #    (run.yaml)에만 닿고 봉인물은 건드리지 않으며, 표시를 남긴 뒤에도 중단은 그대로다 —
    #    이 자리가 하는 일은 거부를 없애는 것이 아니라 거부의 흔적을 남기는 것이다.
    try:
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
    except StageEnvironmentError as entry_error:
        changes = _source_changes(
            paths,
            figures_dir=figures_dir,
            canonical_bytes=canonical_bytes,
            canonical_digest=canonical_digest,
        )
        if not changes:
            # 진입 검사는 원천 변경 말고도 투입물 부재로 넘어진다. 그것은 다른 사고이므로
            # 승계 표시를 남기지 않는다 — 과잉 표시는 표시의 뜻을 지운다.
            raise
        note = _mark_superseded(
            paths,
            contract,
            changes=changes,
            input_path=source_patent_path,
            sealed_manifest=figures_manifest_digest(
                (name, digest)
                for name, (_size, digest) in _dir_entries(paths.figures_raw).items()
            ),
            incoming_manifest=figures_manifest_digest(
                (name, digest)
                for name, (_size, digest) in _dir_entries(figures_dir).items()
            ),
        )
        raise StageEnvironmentError(f"{entry_error} · {note}") from entry_error

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
        supersedes=supersedes_id,
    )

    # ④' 상호 링크 닫기(재정 P-U2). 신 런의 run.yaml 이 실물이 된 **뒤에** 구 런의 절반을
    #    채운다 — 순서가 반대이면 구 런이 아직 없는 런을 가리키는 창이 생긴다.
    if old_paths is not None:
        _close_cross_link(old_paths, contract, new_run_id=run_id)

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
    supersedes: str | None = None,
) -> None:
    """런 메타 골격(SPEC §7.3). 이미 있으면 원천 관련 필드와 **커밋 핀**만 갱신한다.

    핀은 `_engine_pin` 이 확정한 값이며(재정 P-U1·P-8), 빈 문자열 골격을 남기지 않는다 —
    빈 핀은 "아직 아무도 쓰지 않았다"를 "결박이 있다"처럼 보이게 만든다. 기존 블록의 다른
    필드(`gate_version` 등)는 보존한다.

    `supersedes`·`superseded_by` 는 **상호 링크의 두 끝**이다(재정 P-U2, 필드 명세 = SPEC §7.3).
    승계가 없는 평범한 런에서도 두 키를 null 로 적는 이유는, 링크의 부재가 **선언된 부재**여야
    하기 때문이다 — 키가 없으면 "승계가 없다"와 "이 판 러너는 승계를 모른다"가 구별되지 않는다.
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
        "supersedes": supersedes if supersedes is not None else existing.get("supersedes"),
        "superseded_by": existing.get("superseded_by"),
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
