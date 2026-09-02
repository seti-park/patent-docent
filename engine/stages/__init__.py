# -*- coding: utf-8 -*-
"""스테이지 러너 3종(`source` · `read` · `freeze`)과 그들이 공유하는 최소 도구.

여기 있는 함수는 전부 **결정론**이며 판단하지 않는다. 판단은 레인(LLM)과 Owner 의 몫이고,
러너는 계약이 정한 자리에 계약이 정한 형태로 산출물을 놓고 검사 결과를 그대로 보고한다.

★ 진입 지문 검사(재정 P-C). 일반 원리 = **"모든 스테이지는 진입 시 선언된 입력의 지문을
검증한다"**. 그 검사 목록의 소유자는 코드가 아니라 계약(`checks_on_entry`)이며, 여기 있는
것은 계약이 부른 검사 id 의 **구현**뿐이다 — 목록을 코드가 들면 계약이 검사를 늘려도 러너가
따라오지 않고, 반대로 코드가 검사를 늘리면 계약이 모르는 검사가 생긴다. 양방향 다 결함이다.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Any

import yaml

from reader.lib.report import CheckRow

DIGEST_PREFIX = "sha256:"
TERMINAL_ACTIONS = ("halt", "reject-upstream", "escalate")


class StageError(Exception):
    """러너 자신의 계약 위반(입력 부재·산출 자리 충돌·보고 서식 위반)."""


class StageEnvironmentError(StageError):
    """선언된 입력의 지문이 어긋났다 — **환경 오류**이며 품질 결함이 아니다(재정 P-C).

    그러므로 이 예외는 **재시도·수정 루프의 대상이 아니다.** 러너는 즉시 멈추고 진단
    (파일·기대·실측)을 문자열로 싣는다. 원천 자체가 바뀐 경우의 처분은 부분 복구가 아니라
    새 런이다(재정 P-U2).
    """


class StageHaltError(StageError):
    """런의 **전제**가 서지 않아 시작하지 못한다 — 조치는 `halt` 다.

    `StageEnvironmentError` 와 층이 다르다. 환경 오류는 **세계가 어긋났다**(선언된 입력이
    기록과 다르다)이고, 이것은 **세계는 멀쩡한데 런을 열 자격이 없다**(예: 작업 트리가
    더러워 커밋에 결박될 수 없다 — 재정 P-U1)이다. 처분도 다르다 — 앞은 진단이고 이것은
    사람이 전제를 갖춘 뒤 다시 개시하는 일이다. 두 실패를 한 예외로 접으면 진단문이
    "무엇을 하라"를 말하지 못한다.
    """


def sha256_bytes(payload: bytes) -> str:
    """`sha256:<hex>` 형태의 다이제스트(글로사리 §3 ID 문법)."""
    return DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return sha256_bytes(handle.read())


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def write_json(path: str, payload: Any) -> None:
    """결정론 JSON 쓰기 — 키 정렬 + 고정 들여쓰기 + 끝 개행."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def load_json(path: str) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise StageError(f"YAML 최상위가 매핑이 아니다: {path}")
    return data


def dump_yaml(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)


def worst_status(statuses: list[str]) -> str:
    """`halt` > `reject-upstream` > `escalate` > `ok`.

    조치 어휘 4종의 정본은 SPEC §1.2 C6 이며(`retry(n)`은 스테이지 안에서 소진되므로
    여기 오지 않는다), 순서는 "런이 얼마나 멀리 되돌아가는가"다 — `halt` 는 런을 세우고,
    `reject-upstream` 은 상류 스테이지로 되돌리며, `escalate` 는 Owner 를 부른다.
    """
    order = {"ok": 0, "escalate": 1, "reject-upstream": 2, "halt": 3}
    worst = "ok"
    for status in statuses:
        if order.get(status, 0) > order[worst]:
            worst = status
    return worst


def rows_to_dicts(rows: list[CheckRow]) -> list[dict]:
    return [row.to_row_dict() for row in rows]


def failed_rows(rows: list[CheckRow]) -> list[CheckRow]:
    return [row for row in rows if row.status == "fail"]


def findings_of(rows: list[CheckRow]) -> list[dict]:
    return [finding.as_dict() for row in rows for finding in row.findings]


def failure_entry(contract: dict, needle: str) -> dict:
    """계약의 `failure[]` 에서 조건 문언에 `needle` 이 든 항목을 찾는다.

    조치·사유 표기를 코드에 적지 않기 위한 조회다 — `escalate` 의 사유 라벨
    (`형식 전제 미충족` · `안도감 부적합`)은 계약 파일이 정본이고 러너는 전사할 뿐이다.
    """
    for entry in contract.get("failure") or []:
        if needle in str(entry.get("condition", "")):
            return entry
    raise StageError(f"계약의 failure 목록에 '{needle}' 조건이 없다")


def failure_rows_for_checks(contract: dict, check_ids) -> list[dict]:
    """실패 검사 id 집합의 후보 행을 계약 순서로 돌려준다(재정 T26)."""
    rows = contract.get("failure") or []
    if not isinstance(rows, list):
        raise StageError("계약 failure이 list가 아니다")
    wanted = set(check_ids)
    for check_id in wanted:
        matches = [
            row
            for row in rows
            if isinstance(row, dict)
            and isinstance(row.get("checks"), list)
            and check_id in row["checks"]
        ]
        if len(matches) != 1:
            raise StageError(
                f"검사 {check_id!r}의 failure 행은 정확히 1개여야 한다: {len(matches)}"
            )
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("checks"), list)
        and wanted.intersection(row["checks"])
    ]


def failure_row_of_kind(contract: dict, kind: str) -> dict:
    """failure[]의 비검사 사건 행을 kind로 단독 조회한다."""
    rows = contract.get("failure") or []
    matches = [row for row in rows if isinstance(row, dict) and row.get("kind") == kind]
    if len(matches) != 1:
        raise StageError(f"kind {kind!r}의 failure 행은 정확히 1개여야 한다: {len(matches)}")
    return matches[0]


def terminal_action(row: dict) -> str:
    """retry(n)은 then, 나머지는 action의 종단 어휘를 fail-closed로 읽는다."""
    action = row.get("action")
    if isinstance(action, str) and re.fullmatch(r"retry\(\d+\)", action):
        then = row.get("then")
        if then not in TERMINAL_ACTIONS:
            raise StageError(f"{action!r} 행의 then이 종단 어휘가 아니다: {then!r}")
        return str(then)
    if action not in TERMINAL_ACTIONS or "then" in row:
        raise StageError(
            f"비재시도 행은 종단 action만 들어야 한다: "
            f"action={action!r}, then={row.get('then')!r}"
        )
    return str(action)


def select_failure_row(contract: dict, candidates) -> dict:
    """조치 격자의 최대를 고르고 동률은 failure[] 계약 순서로 풀어낸다."""
    rows = contract.get("failure") or []
    candidate_rows = list(candidates)
    if not candidate_rows:
        raise StageError("실패 후보 행이 없다")
    actions = [terminal_action(row) for row in candidate_rows]
    winner = worst_status(actions)
    for row in rows:
        if any(row is candidate for candidate in candidate_rows):
            if terminal_action(row) == winner:
                return row
    raise StageError("실패 후보 행이 계약 failure[] 안에 없다")


# ---------------------------------------------------------------------------
# 진입 지문 검사 (재정 P-C)
# ---------------------------------------------------------------------------


def figures_manifest_digest(entries) -> str:
    """도면 세트 **매니페스트 지문**(재정 P-U2).

    `sha256("\\n".join(f"{filename}\\t{digest}"))` 이며 파일명으로 정렬한다. 원천은
    `patent.md` 하나가 아니라 **도면 세트 전체**이고, 세트의 변경(파일 추가·삭제·교체)은
    파일 하나의 지문으로는 드러나지 않는다 — 그 공백을 메우는 값이다.

    `entries` = `(filename, digest)` 쌍의 나열. `digest` 는 이 모듈의 `sha256_bytes` 산출
    형태(`sha256:<hex>`)를 **그대로** 쓴다. 산출자(`source`)와 대조자(`read`)가 같은 함수를
    부르므로 표기가 갈릴 자리가 없다.
    """
    body = "\n".join(f"{name}\t{digest}" for name, digest in sorted(entries))
    return sha256_bytes(body.encode("utf-8"))


def _figure_digests(figures_dir: str) -> list[tuple[str, str]]:
    """도면 원본 디렉터리의 `(파일명, 지문)` 목록(파일명 정렬)."""
    if not os.path.isdir(figures_dir):
        return []
    out: list[tuple[str, str]] = []
    for name in sorted(os.listdir(figures_dir)):
        path = os.path.join(figures_dir, name)
        if os.path.isfile(path):
            out.append((name, sha256_file(path)))
    return out


def _require_file(row: CheckRow, check_id: str, path: str, label: str) -> bool:
    """선언된 입력의 실재 확인. 부재도 환경 오류다(대조할 대상이 없다)."""
    if os.path.isfile(path):
        return True
    row.add(
        check_id,
        label,
        "(파일 없음)",
        path,
        "선언된 입력이 실재하지 않는다 — 지문을 대조할 대상 자체가 없다",
    )
    return False


def _compare(row: CheckRow, check_id: str, locus: str, found: str, expected: str, message: str) -> None:
    if found != expected:
        row.add(check_id, locus, found or "(없음)", expected or "(없음)", message)


def _entry_read_input_digest(row: CheckRow, paths, entry: dict, inputs: dict) -> None:
    """`read.input-digest` — 원천 텍스트 4자리 + 도면 세트 매니페스트 지문의 대조."""
    check_id = str(entry.get("id"))
    if not _require_file(row, check_id, paths.patent_md, "00-source/patent.md"):
        return
    with open(paths.patent_md, "rb") as handle:
        actual = sha256_bytes(handle.read())
    row.checked += 1

    if _require_file(row, check_id, paths.patent_sha256, "00-source/patent.sha256"):
        row.checked += 1
        # 실측(현재 원천) ↔ 기대(그 자리가 신고한 값). 좌표가 "어디가 신고했는가"를 말한다.
        _compare(
            row, check_id, "00-source/patent.sha256",
            actual, read_text(paths.patent_sha256).strip(),
            "핀된 다이제스트가 원천의 실측과 다르다 — 원천이 도중에 바뀐 런이다(재정 P-U2)",
        )
    if _require_file(row, check_id, paths.run_yaml, "run.yaml"):
        row.checked += 1
        declared = str((load_yaml(paths.run_yaml).get("patent") or {}).get("source_sha256", ""))
        _compare(
            row, check_id, "run.yaml#patent.source_sha256", actual, declared,
            "런 메타가 신고한 원천 다이제스트가 실측과 다르다",
        )
    if _require_file(row, check_id, paths.source_report, "00-source/source-report.json"):
        report = load_json(paths.source_report)
        row.checked += 1
        _compare(
            row, check_id, "00-source/source-report.json#source.canonical_sha256",
            actual, str((report.get("source") or {}).get("canonical_sha256", "")),
            "source 스테이지가 기록한 정본 다이제스트가 실측과 다르다",
        )
        # 도면 세트는 파일 하나가 아니라 **세트**가 원천이다(재정 P-U2).
        row.checked += 1
        actual_manifest = figures_manifest_digest(_figure_digests(paths.figures_raw))
        _compare(
            row, check_id, "00-source/figures-raw/ (매니페스트 지문)",
            actual_manifest, str(report.get("figures_manifest_digest", "")),
            "도면 세트가 source 보고와 다르다 — 파일 추가·삭제·교체는 매니페스트 지문에만 드러난다",
        )
        row.checked += 1
        recorded_manifest = figures_manifest_digest(
            (str(figure.get("filename", "")), str(figure.get("sha256", "")))
            for figure in report.get("figures") or []
        )
        _compare(
            row, check_id, "00-source/source-report.json#figures[].sha256",
            recorded_manifest, str(report.get("figures_manifest_digest", "")),
            "보고서 안에서 도면 행과 매니페스트 지문이 어긋난다",
        )


def _entry_source_input_digest(row: CheckRow, paths, entry: dict, inputs: dict) -> None:
    """`source.input-digest` — 외부 투입물의 실재·지문 기록 + 원천 변경 감지(재정 P-U2).

    `source` 는 파이프라인의 첫 스테이지라 대조할 상류 지문이 없다. 대신 ⓐ 투입물이 실재하는지
    보고 ⓑ 런 작업장에 이미 `00-source/` 가 있으면 그 지문과 대조한다. 투입물 경로는 계약이
    아니라 호출자가 안다 — 그래서 `inputs` 로 받는다.
    """
    check_id = str(entry.get("id"))
    patent_path = str(inputs.get("source_patent_path", ""))
    figures_dir = str(inputs.get("figures_dir", ""))
    if not _require_file(row, check_id, patent_path, "Owner 투입물(원문 파일)"):
        return
    row.checked += 1
    with open(patent_path, "rb") as handle:
        original_digest = sha256_bytes(handle.read())
    row.extras["input_digest"] = {
        "source_patent_path": os.path.abspath(patent_path),
        "original_sha256": original_digest,
        "figures": [
            {"filename": name, "sha256": digest}
            for name, digest in _figure_digests(figures_dir)
        ],
    }
    row.checked += 1

    # 기존 00-source/ 가 없으면 대조할 것이 없다(첫 봉인).
    if not os.path.isfile(paths.patent_md):
        return
    canonical = str(inputs.get("canonical_digest", ""))
    row.checked += 1
    with open(paths.patent_md, "rb") as handle:
        pinned = sha256_bytes(handle.read())
    if canonical and canonical != pinned:
        row.add(
            check_id,
            "00-source/patent.md",
            canonical,
            pinned,
            "새 투입물의 정본 지문이 기존 봉인과 다르다 — 덮어쓰지 않는다. 처분은 새 런이다(재정 P-U2)",
        )
    row.checked += 1
    new_manifest = figures_manifest_digest(_figure_digests(figures_dir))
    pinned_manifest = figures_manifest_digest(_figure_digests(paths.figures_raw))
    if new_manifest != pinned_manifest:
        row.add(
            check_id,
            "00-source/figures-raw/ (매니페스트 지문)",
            new_manifest,
            pinned_manifest,
            "도면 세트가 기존 봉인과 다르다 — 부분 재사용은 바이트 오프셋 특성상 정확성 위반이다(재정 P-U2)",
        )


def _entry_freeze_input_digest(row: CheckRow, paths, entry: dict, inputs: dict) -> None:
    """`freeze.input-digest` — **선언된 입력**(재료 명세·판독본)의 실재와 지문 대조.

    ★ 폐기(재정 R8 우선): 구 구현은 여기서 승인 봉투의 `target.digest` ↔ 재료 실측까지
    대조하고 어긋나면 `StageEnvironmentError` 를 던졌다. 그 결과 출구 규칙
    `freeze.approval-valid#approval.target-digest` 에 **제어가 닿지 않았다**(도달 불능).

    두 실패는 성질이 다르므로 겹치면 안 된다.

      · 진입 지문(재정 P-C) — **세계가 어긋났다**. 선언된 입력이 기록과 다르다. 환경 오류이며
        즉시 중단 + 진단이다(재시도·수정 루프가 아니다).
      · 봉투 `target.digest`(재정 R8) — 세계는 멀쩡하고 **승인이 실효**했다. 승인 후 재료가
        개정되면 봉투는 자동 실효하는 것이 설계이며, 그때 필요한 것은 "환경을 진단하라"가
        아니라 **"다시 승인받아라"**다. 처분은 `halt` + 재승인이고 그 사실은 **판정 행**에
        남아야 한다 — 진입 검사가 그것을 삼키면 재승인 경로가 판정문에서 사라진다.

    그러므로 봉투 결속은 출구(`engine/stages/freeze.py`)의 몫이고, 진입이 보는 것은 여기까지다.
    """
    check_id = str(entry.get("id"))
    if not _require_file(row, check_id, paths.material_spec_json, "10-read/material-spec.json"):
        return
    row.checked += 1
    _require_file(row, check_id, paths.material_spec_md, "10-read/material-spec.md")
    row.checked += 1

    if _require_file(row, check_id, paths.patent_sha256, "00-source/patent.sha256"):
        row.checked += 1
        spec = load_json(paths.material_spec_json)
        _compare(
            row, check_id, "10-read/material-spec.json#patent.source_digest",
            read_text(paths.patent_sha256).strip(),
            str((spec.get("patent") or {}).get("source_digest", "")),
            "동결하려는 재료가 이 런의 원천 위에서 만들어지지 않았다",
        )

    # ★ 봉투는 여기서 열지 않는다. 부재·신원 위조·`target.digest` 실효 전부 출구
    #   (`freeze.approval-valid`)의 관할이다 — 위 docstring 참조(재정 R8 · P-C).
    #   구 구현의 봉투 프런트매터 얕은 해석기(`_envelope_frontmatter`)도 함께 폐기했다:
    #   진입이 봉투를 읽을 이유가 사라졌고, 해석기가 둘이면 서식 판정이 두 자리에서 갈린다
    #   (본 해석기 = `engine/stages/freeze.py#parse_envelope`).


_ENTRY_CHECKS = {
    "read.input-digest": _entry_read_input_digest,
    "source.input-digest": _entry_source_input_digest,
    "freeze.input-digest": _entry_freeze_input_digest,
}


def verify_declared_inputs(paths, contract: dict, stage_id: str, *, inputs: dict | None = None) -> CheckRow:
    """계약의 `checks_on_entry` 를 읽어 실행한다(재정 P-C).

    반환 = 판정 행 1건(계약이 검사 여럿을 선언하면 한 행에 합산한다 — 진입 검사는 "환경이
    서 있는가" 하나의 물음이다). 불일치가 있으면 행을 돌려주지 않고 `StageEnvironmentError`
    를 던지며, 진단 문자열에 **파일·기대·실측**을 싣는다. 재시도 대상이 아니기 때문이다.

    `inputs` = 계약이 알 수 없는 스테이지별 부수 입력(외부 투입물 경로·봉투 경로 등).
    """
    declared = contract.get("checks_on_entry") or []
    row = CheckRow(check_id=f"{stage_id}.input-digest", checked=0)
    if declared:
        # 계약이 진입 검사를 선언했으면 행 id 는 그 선언을 따른다(코드가 이름을 정하지 않는다).
        row.check_id = str(declared[0].get("id") or row.check_id)
    for entry in declared:
        check_id = str(entry.get("id", ""))
        handler = _ENTRY_CHECKS.get(check_id)
        if handler is None:
            raise StageError(
                f"{stage_id} 계약이 선언한 진입 검사 {check_id!r} 의 구현이 러너에 없다 — "
                "계약이 모르는 검사도, 구현이 없는 선언도 결함이다"
            )
        handler(row, paths, entry, inputs or {})
    if row.findings:
        diagnosis = "; ".join(
            f"{finding.locus}: 실측 {finding.found} ≠ 기대 {finding.expected} ({finding.message})"
            for finding in row.findings
        )
        raise StageEnvironmentError(
            f"[환경 오류] {stage_id} 진입 지문 불일치 {len(row.findings)}건 — {diagnosis}"
        )
    return row


__all__ = [
    "DIGEST_PREFIX",
    "StageEnvironmentError",
    "StageError",
    "StageHaltError",
    "figures_manifest_digest",
    "verify_declared_inputs",
    "dump_yaml",
    "failed_rows",
    "failure_entry",
    "findings_of",
    "load_json",
    "load_yaml",
    "read_text",
    "rows_to_dicts",
    "sha256_bytes",
    "sha256_file",
    "worst_status",
    "write_json",
    "write_text",
]
