#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문서·계약 정합 검사기 (K1~K7).

`docs/SPEC.md`·`docs/CHARTER.md`와 `contracts/`·`reader/schemas/`의 실물 계약 파일이
서로 어긋나지 않는지를 기계로 확인한다. read-only 도구이며 어떤 파일도 쓰지 않는다.

★ 자기매칭 격리 (설계 요건 — 정본: `docs/SPEC.md` §4.8 자기매칭 격리 요건 4항 +
`docs/decisions/D-20260817-02-spec-revision-m05.md` §5 규율 3. SPEC §8.3 ⑧이 이 요건을
검사 도구에도 동일 적용하라고 지시한다.)
M0 감수에서 grep 서식 견본이 자기 자신에 매칭되어 오탐한 사건이 있었다. 그 구조적 방지를
이 도구의 설계 요건으로 삼는다. 아래 번호는 이 도구의 이행 목록이며, 정본 표의 4항을
도구 문맥으로 옮긴 것이다.

  1. 스캔 대상은 allowlist(`DOC_TARGETS`·`CONTRACT_GLOBS`)로만 정한다. 암묵 전수 스캔을
     하지 않는다.
  2. 탐지 패턴·표본 데이터는 코드에서 분리한다 — 폐지 토큰과 그 예외 규칙은
     `tools/retired-tokens.yaml`(도구 자산, 스캔 대상 아님)에, 결함 표본은
     `tests/fixtures/`에 둔다. 검사기 소스에 표본 문장을 리터럴로 두지 않는다.
  3. 스캔 목록에 검사기 자신(`tools/**`)이나 픽스처(`tests/**`), 회귀 변조본
     (`ledgers/regression/**`)이 들어오면 finding이 아니라 **exit 2로 실행을 거부**한다
     (`FORBIDDEN_SCAN_PREFIXES`, `enforce_isolation()`).
  4. 위 3항을 코드 주석과 `--help`에 명문화한다(이 docstring과 `EPILOG`).

종료 코드 (SPEC §8.3):
  0 = 전 검사 통과 / 1 = 검증 실패(정합 결함) / 2 = 입력·환경 오류(파일 부재·파싱 불능·격리 위반)

`assert`를 쓰지 않는다(`python3 -O` 공허 통과 방지 — CLAUDE.md §3).
"""

from __future__ import annotations

import argparse
import glob as globlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - 환경 오류 경로
    print(f"ENVIRONMENT ERROR: pyyaml 로드 실패: {exc}", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - 환경 오류 경로
    print(f"ENVIRONMENT ERROR: jsonschema 로드 실패: {exc}", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# 스캔 대상 allowlist (격리 요건 1항) — 여기 없는 경로는 어떤 검사도 읽지 않는다.
# ---------------------------------------------------------------------------

# K1(절 참조)·K4(조항 참조)·K5(폐지 토큰)·K3(문서측 계약 라인) 대상 = 이 두 문서뿐.
DOC_TARGETS: tuple[str, ...] = ("docs/CHARTER.md", "docs/SPEC.md")

# K2(§6.7 계약 파일 현황표) 대상 문서.
CONTRACT_TABLE_DOC = "docs/SPEC.md"

# K6(파싱)·K7(JSON Schema 메타)·K3(파일측 계약 라인) 대상 글로브.
#
# ★ `reader/*.yaml` 는 M1 에서 추가되었다. 재정 2026-08-18 N8 ①의 경계 규칙("이식 단위에
#   속하는 계약 = reader/")에 따라 독해층 규칙 계약(`reader/reader-rules.yaml`)이 `reader/`
#   루트에 산다. 이 글로브가 없으면 그 파일이 선언한 계약 라인을 K3 가 보지 못해, 문서에만
#   있는 계약으로 오판하거나(반대로) 파일의 선언이 영영 대조되지 않는다. `reader/schemas/`
#   에도 향후 YAML 계약이 올 수 있으므로 함께 연다.
CONTRACT_GLOBS: tuple[str, ...] = (
    "contracts/**/*.json",
    "contracts/**/*.yaml",
    "contracts/**/*.yml",
    "reader/*.yaml",
    "reader/schemas/*.json",
    "reader/schemas/*.yaml",
)

# 어떤 검사의 스캔 대상도 될 수 없는 경로 접두 (격리 요건 3항).
FORBIDDEN_SCAN_PREFIXES: tuple[str, ...] = ("tools/", "tests/", "ledgers/regression/")

# K5 데이터 파일 — 도구 자산이므로 스크립트 위치 기준으로 읽는다(`--repo` 무관).
RETIRED_TOKENS_FILE = "retired-tokens.yaml"

# K4 조항 번호 범위 (헌장 D1~D15).
CLAUSE_MIN = 1
CLAUSE_MAX = 15

# 절 헤더: `## §6`, `### §6.7`, `#### §4.4.1` 등 (깊이 무관, 3단 번호까지 허용).
RE_SECTION_HEADER = re.compile(r"^(#{1,6})\s+§([0-9]+(?:\.[0-9]+)*)\s*(.*)$")
# 절 참조: `§6`, `§6.7`, `§4.4.1`.
RE_SECTION_REF = re.compile(r"§([0-9]+(?:\.[0-9]+)*)")
# 조항 참조: `D8`. 16진 색상(`#D19730`)·재정 파일명(`D-20260817-01`)·긴 토큰은 제외.
RE_CLAUSE_REF = re.compile(r"(?<![0-9A-Za-z#_\-])D([0-9]+)(?![0-9A-Za-z_\-])")
# 계약 라인 문자열: `material-spec/v0`. 경로 일부(`contracts/schemas/x/v0`)는 제외.
RE_CONTRACT_LINE = re.compile(r"(?<![0-9A-Za-z_/\-])([a-z][a-z0-9\-]*)/(v[0-9]+)(?![0-9A-Za-z_\-])")
# 마크다운 표 셀의 백틱 경로.
RE_BACKTICK = re.compile(r"`([^`]+)`")

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"

EPILOG = """\
검사 항목:
  K1  절 참조 해소     docs/*.md 의 §N[.M] 참조가 실재 절 헤더로 해소되는가
  K2  계약 파일 현황   SPEC §6.7 표의 `현행` 경로 실재 / `예정` 경로 부재
                       글로브 행은 매칭 파일 수로 본다 — `현행` 1개 이상 / `예정` 0개
  K3  스키마 이름 일치 문서의 <name>/vN 계약 라인 ↔ 실제 계약 파일 선언 (양방향)
  K4  조항 참조 범위   D<n> 참조가 D1~D15 범위인가
  K5  폐지 토큰 부재   tools/retired-tokens.yaml 에 등재된 폐지 토큰의 부재
  K6  계약 파일 파싱   contracts/**·reader/*.yaml·reader/schemas/** 의 JSON·YAML 파싱
  K7  스키마 메타 검증 $schema 선언이 draft 2020-12 이고 check_schema() 통과

★ 자기매칭 격리 (이 도구의 설계 요건 — 정본: SPEC §4.8 · D-20260817-02 §5 규율 3):
  1. 스캔 대상은 allowlist로만 정한다 — 암묵 전수 스캔 없음.
     K1·K3·K4·K5 = docs/CHARTER.md, docs/SPEC.md 뿐.
     K6·K7 = contracts/**, reader/*.yaml, reader/schemas/** 뿐.
  2. 탐지 패턴·표본은 코드 밖 데이터 파일에 둔다(tools/retired-tokens.yaml, tests/fixtures/).
  3. tools/ · tests/ · ledgers/regression/ 이 스캔 목록에 들어오면 finding이 아니라
     ISOLATION VIOLATION 으로 즉시 exit 2 한다 — 격리 위반은 결함 보고가 아니라 실행 거부다.
  4. 이 도구는 read-only 다. --fix/--write 류 플래그는 설계상 두지 않는다.

종료 코드: 0 통과 / 1 검증 실패 / 2 입력·환경 오류 (격리 위반 포함)
"""


# ---------------------------------------------------------------------------
# 자료 구조
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    check: str
    path: str
    line: int
    found: str
    expected: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "check": self.check,
            "path": self.path,
            "line": self.line,
            "found": self.found,
            "expected": self.expected,
            "message": self.message,
        }


@dataclass
class CheckResult:
    id: str
    name: str
    findings: list[Finding] = field(default_factory=list)
    resolved: list[str] = field(default_factory=list)  # --verbose 출력용
    waived: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "PASS" if not self.findings else "FAIL"


@dataclass
class DocFile:
    rel: str
    abs: str
    lines: list[str]


# ---------------------------------------------------------------------------
# 격리 집행 (요건 3항)
# ---------------------------------------------------------------------------


def fail_env(message: str) -> None:
    """입력·환경 오류 = exit 2."""
    print(f"ENVIRONMENT ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def enforce_isolation(rel_paths: list[str], label: str, self_paths: set[str], repo: str) -> None:
    """스캔 목록의 격리 위반을 검사한다. 위반 = finding이 아니라 실행 거부(exit 2).

    두 축으로 본다.
      (a) 리포 상대 경로가 FORBIDDEN_SCAN_PREFIXES 에 속하는가.
      (b) 절대 경로가 검사기 자신 또는 그 데이터 파일과 같은가(자기 배제 단정).
    """
    violations: list[str] = []
    for rel in rel_paths:
        norm = rel.replace(os.sep, "/")
        for prefix in FORBIDDEN_SCAN_PREFIXES:
            if norm == prefix.rstrip("/") or norm.startswith(prefix):
                violations.append(f"{label}: {norm} (금지 접두 `{prefix}`)")
        real = os.path.realpath(os.path.join(repo, rel))
        if real in self_paths:
            violations.append(f"{label}: {norm} (검사기 자신 또는 그 데이터 파일)")
    if violations:
        print("ISOLATION VIOLATION — 스캔 목록에 격리 대상 경로가 포함되어 실행을 거부한다.")
        for item in violations:
            print(f"  - {item}")
        print("격리 위반은 결함 보고가 아니라 실행 거부다 (SPEC §4.8 자기매칭 격리 요건 4항).")
        sys.exit(2)


# ---------------------------------------------------------------------------
# 입력 로딩
# ---------------------------------------------------------------------------


def load_retired_tokens(script_dir: str) -> dict[str, Any]:
    """폐지 토큰·예외 규칙 데이터 파일을 읽는다 (격리 요건 2항: 코드 상수 아님)."""
    path = os.path.join(script_dir, RETIRED_TOKENS_FILE)
    if not os.path.isfile(path):
        fail_env(f"폐지 토큰 데이터 파일 부재: {path}")
    try:
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except Exception as exc:  # noqa: BLE001 - 파싱 불능 = 환경 오류
        fail_env(f"폐지 토큰 데이터 파일 파싱 불능: {path}: {exc}")
    if not isinstance(data, dict):
        fail_env(f"폐지 토큰 데이터 파일 형식 오류(맵 아님): {path}")
    tokens = data.get("tokens")
    if not isinstance(tokens, list) or not tokens:
        fail_env(f"폐지 토큰 목록(tokens)이 비었거나 목록이 아니다: {path}")
    for entry in tokens:
        if not isinstance(entry, dict) or not isinstance(entry.get("token"), str):
            fail_env(f"tokens 항목 형식 오류(token 문자열 필요): {path}")
    exemptions = data.get("exemptions", [])
    if not isinstance(exemptions, list):
        fail_env(f"exemptions 형식 오류(목록 필요): {path}")
    for entry in exemptions:
        if not isinstance(entry, dict):
            fail_env(f"exemptions 항목 형식 오류(맵 필요): {path}")
        kind = entry.get("kind")
        if kind == "span":
            if not isinstance(entry.get("pattern"), str):
                fail_env(f"exemptions[kind=span]에 pattern 문자열 필요: {path}")
        elif kind == "line-marker":
            if not isinstance(entry.get("marker"), str):
                fail_env(f"exemptions[kind=line-marker]에 marker 문자열 필요: {path}")
        else:
            fail_env(f"exemptions kind 미지원: {kind!r} ({path})")
    return data


def load_doc(repo: str, rel: str) -> DocFile:
    path = os.path.join(repo, rel)
    if not os.path.isfile(path):
        fail_env(f"필수 문서 부재: {rel} (repo={repo})")
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except Exception as exc:  # noqa: BLE001
        fail_env(f"문서 읽기 실패: {rel}: {exc}")
    return DocFile(rel=rel, abs=path, lines=text.splitlines())


def glob_matches(repo: str, pattern: str) -> list[str]:
    """리포 안에서 글로브 패턴에 매칭되는 **파일** 목록(리포 상대 경로, 결정론 정렬).

    디렉터리는 세지 않는다 — `§6.7` 표의 글로브 행이 약속하는 것은 파일의 실재이지
    디렉터리의 실재가 아니다(디렉터리 부재는 K2가 별도 finding으로 본다).
    """
    found: set[str] = set()
    for path in globlib.glob(os.path.join(repo, pattern), recursive=True):
        if os.path.isfile(path):
            found.add(os.path.relpath(path, repo).replace(os.sep, "/"))
    return sorted(found)


def glob_contract_files(repo: str) -> list[str]:
    """CONTRACT_GLOBS 를 리포 상대 경로 목록으로 전개한다(결정론 정렬)."""
    found: set[str] = set()
    for pattern in CONTRACT_GLOBS:
        found.update(glob_matches(repo, pattern))
    return sorted(found)


# ---------------------------------------------------------------------------
# 문서 파싱 보조
# ---------------------------------------------------------------------------


def build_section_index(docs: list[DocFile]) -> dict[str, tuple[str, int, str]]:
    """절 번호 → (문서, 행 번호, 헤더 제목). 두 문서의 헤더를 합집합으로 본다."""
    index: dict[str, tuple[str, int, str]] = {}
    for doc in docs:
        for lineno, line in enumerate(doc.lines, start=1):
            match = RE_SECTION_HEADER.match(line)
            if match:
                number = match.group(2)
                title = line.lstrip("#").strip()
                if number not in index:
                    index[number] = (doc.rel, lineno, title)
    return index


def iter_reference_lines(doc: DocFile):
    """(행 번호, 행 문자열, 헤더 정의 소비 여부) — 헤더 행의 자기 번호는 참조가 아니다."""
    for lineno, line in enumerate(doc.lines, start=1):
        header = RE_SECTION_HEADER.match(line)
        yield lineno, line, (header.group(2) if header else None)


# ---------------------------------------------------------------------------
# K1 — 절 참조 해소
# ---------------------------------------------------------------------------


def check_k1(docs: list[DocFile], sections: dict[str, tuple[str, int, str]]) -> CheckResult:
    result = CheckResult("K1", "절 참조 해소")
    for doc in docs:
        for lineno, line, own_number in iter_reference_lines(doc):
            skipped_self = False
            for match in RE_SECTION_REF.finditer(line):
                number = match.group(1)
                if own_number is not None and number == own_number and not skipped_self:
                    skipped_self = True  # 헤더 자신의 번호 = 정의이지 참조가 아니다
                    continue
                target = sections.get(number)
                if target is None:
                    result.findings.append(
                        Finding(
                            check="K1",
                            path=doc.rel,
                            line=lineno,
                            found=f"§{number}",
                            expected="실재 절 헤더",
                            message=f"미해소 절 참조 — `§{number}` 헤더가 문서에 없다",
                        )
                    )
                else:
                    result.resolved.append(
                        f"{doc.rel}:{lineno}  §{number} -> {target[0]}:{target[1]}  {target[2]}"
                    )
    return result


# ---------------------------------------------------------------------------
# K2 — 계약 파일 현황표
# ---------------------------------------------------------------------------


def parse_status_table(doc: DocFile) -> tuple[list[tuple[int, str, str, str]], str | None]:
    """SPEC §6.7 표를 (행번호, 경로, 상태, 소관) 목록으로 파싱한다."""
    start = None
    for lineno, line in enumerate(doc.lines, start=1):
        header = RE_SECTION_HEADER.match(line)
        if header and header.group(2) == "6.7":
            start = lineno
            break
    if start is None:
        return [], "SPEC에 `§6.7` 절 헤더가 없다"

    rows: list[tuple[int, str, str, str]] = []
    seen_header_row = False
    for lineno in range(start + 1, len(doc.lines) + 1):
        line = doc.lines[lineno - 1]
        if RE_SECTION_HEADER.match(line) or line.startswith("#"):
            break
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if not seen_header_row:
            seen_header_row = True
            continue  # 표 머리 행
        if set(cells[0]) <= {"-", ":", " "}:
            continue  # 구분 행
        path_cell, status_cell, owner_cell = cells[0], cells[1], cells[2]
        backtick = RE_BACKTICK.search(path_cell)
        path = backtick.group(1) if backtick else path_cell
        rows.append((lineno, path, status_cell, owner_cell))
    if not rows:
        return [], "`§6.7` 절에 3열 계약 파일 현황표가 없다"
    return rows, None


def check_k2(repo: str, spec: DocFile, rows: list[tuple[int, str, str, str]], table_error: str | None) -> CheckResult:
    result = CheckResult("K2", "계약 파일 현황")
    if table_error is not None:
        result.findings.append(
            Finding(
                check="K2",
                path=spec.rel,
                line=0,
                found="(표 없음)",
                expected="§6.7 계약 파일 현황표 (3열: 경로|상태|소관)",
                message=table_error,
            )
        )
        return result

    for lineno, path, status, owner in rows:
        if status not in ("현행", "예정"):
            result.findings.append(
                Finding(
                    check="K2",
                    path=spec.rel,
                    line=lineno,
                    found=status,
                    expected="`현행` 또는 `예정`",
                    message=f"상태 값 미지원 — {path}",
                )
            )
            continue
        target = os.path.join(repo, path)
        if "*" in path:
            # 글로브 행은 두 단으로 본다: ① 부모 디렉터리 실재 ② 매칭 파일 수.
            # ①이 무너지면 ②는 자동으로 0이므로 중복 보고하지 않고 여기서 끊는다.
            parent = os.path.dirname(path)
            if parent and not os.path.isdir(os.path.join(repo, parent)):
                result.findings.append(
                    Finding(
                        check="K2",
                        path=spec.rel,
                        line=lineno,
                        found=path,
                        expected=f"디렉터리 `{parent}/` 존재",
                        message="글로브 행의 부모 디렉터리가 없다",
                    )
                )
                continue
            matches = glob_matches(repo, path)
            sample = ", ".join(matches[:3]) + (" …" if len(matches) > 3 else "")
            if status == "현행" and not matches:
                result.findings.append(
                    Finding(
                        check="K2",
                        path=spec.rel,
                        line=lineno,
                        found=f"{path} (매칭 0건)",
                        expected="매칭 파일 1개 이상",
                        message="`현행`으로 표기된 글로브 경로에 파일이 하나도 없다",
                    )
                )
            elif status == "예정" and matches:
                result.findings.append(
                    Finding(
                        check="K2",
                        path=spec.rel,
                        line=lineno,
                        found=f"{path} (매칭 {len(matches)}건: {sample})",
                        expected="매칭 0건 (소관 모듈에서 신설 예정)",
                        message=f"`예정({owner})`으로 표기된 글로브 경로에 파일이 이미 있다 — 표를 갱신하라",
                    )
                )
            else:
                result.resolved.append(
                    f"{spec.rel}:{lineno}  {path} [{status}] 글로브 매칭 {len(matches)}건 소관={owner}"
                )
            continue
        exists = os.path.exists(target)
        if status == "현행" and not exists:
            result.findings.append(
                Finding(
                    check="K2",
                    path=spec.rel,
                    line=lineno,
                    found=f"{path} (부재)",
                    expected="실재하는 파일",
                    message="`현행`으로 표기된 계약 파일이 리포에 없다",
                )
            )
        elif status == "예정" and exists:
            result.findings.append(
                Finding(
                    check="K2",
                    path=spec.rel,
                    line=lineno,
                    found=f"{path} (실재)",
                    expected="부재 (소관 모듈에서 신설 예정)",
                    message=f"`예정({owner})`으로 표기된 경로가 이미 실재한다 — 표를 갱신하라",
                )
            )
        else:
            result.resolved.append(f"{spec.rel}:{lineno}  {path} [{status}] 소관={owner}")
    return result


# ---------------------------------------------------------------------------
# K3 — 스키마 이름 일치
# ---------------------------------------------------------------------------


def collect_doc_contract_lines(docs: list[DocFile]) -> dict[str, list[tuple[str, int]]]:
    """문서에 등장하는 `<name>/vN` 계약 라인 → 등장 위치 목록."""
    hits: dict[str, list[tuple[str, int]]] = {}
    for doc in docs:
        for lineno, line in enumerate(doc.lines, start=1):
            for match in RE_CONTRACT_LINE.finditer(line):
                name = f"{match.group(1)}/{match.group(2)}"
                hits.setdefault(name, []).append((doc.rel, lineno))
    return hits


def collect_file_contract_lines(parsed: dict[str, Any]) -> dict[str, list[str]]:
    """계약 파일이 선언한 `<name>/vN` → 선언 파일 목록.

    JSON  : `title`, `properties.schema.const`
    YAML  : 최상위 `schema`
    """
    hits: dict[str, list[str]] = {}

    def record(value: Any, rel: str) -> None:
        if isinstance(value, str) and RE_CONTRACT_LINE.fullmatch(value):
            hits.setdefault(value, []).append(rel)

    for rel, data in parsed.items():
        if not isinstance(data, dict):
            continue
        if rel.endswith(".json"):
            record(data.get("title"), rel)
            properties = data.get("properties")
            if isinstance(properties, dict):
                schema_prop = properties.get("schema")
                if isinstance(schema_prop, dict):
                    record(schema_prop.get("const"), rel)
        else:
            record(data.get("schema"), rel)
    return hits


def planned_names_from_table(rows: list[tuple[int, str, str, str]]) -> set[str]:
    """`예정` 행의 파일명에서 계약 이름 후보를 뽑는다 (K2와의 모순 방지용 면제 근거)."""
    names: set[str] = set()
    for _lineno, path, status, _owner in rows:
        if status != "예정":
            continue
        base = os.path.basename(path)
        for suffix in (".schema.json", ".json", ".yaml", ".yml", ".md"):
            if base.endswith(suffix):
                base = base[: -len(suffix)]
                break
        if base and "*" not in base:
            names.add(base)
    return names


def check_k3(
    doc_hits: dict[str, list[tuple[str, int]]],
    file_hits: dict[str, list[str]],
    planned: set[str],
) -> CheckResult:
    result = CheckResult("K3", "스키마 이름 일치")
    for name in sorted(doc_hits):
        locations = doc_hits[name]
        if name in file_hits:
            result.resolved.append(
                f"{name}  문서 {len(locations)}곳 <-> 파일 {', '.join(sorted(set(file_hits[name])))}"
            )
            continue
        base = name.split("/")[0]
        if base in planned:
            result.waived.append(
                f"{name}  문서 {len(locations)}곳 — SPEC §6.7 `예정` 행이므로 면제"
            )
            continue
        rel, lineno = locations[0]
        result.findings.append(
            Finding(
                check="K3",
                path=rel,
                line=lineno,
                found=name,
                expected="동일 이름을 선언한 계약 파일 (title 또는 properties.schema.const)",
                message=f"문서에만 있는 계약 라인 — 등장 {len(locations)}곳",
            )
        )
    for name in sorted(file_hits):
        if name not in doc_hits:
            result.findings.append(
                Finding(
                    check="K3",
                    path=file_hits[name][0],
                    line=0,
                    found=name,
                    expected="문서(docs/SPEC.md·docs/CHARTER.md)의 동일 계약 라인 언급",
                    message="파일에만 있는 계약 라인 — 문서가 이 계약을 서술하지 않는다",
                )
            )
    return result


# ---------------------------------------------------------------------------
# K4 — 조항 참조 범위
# ---------------------------------------------------------------------------


def check_k4(docs: list[DocFile]) -> CheckResult:
    result = CheckResult("K4", "조항 참조 범위")
    for doc in docs:
        for lineno, line in enumerate(doc.lines, start=1):
            for match in RE_CLAUSE_REF.finditer(line):
                number = int(match.group(1))
                if number < CLAUSE_MIN or number > CLAUSE_MAX:
                    result.findings.append(
                        Finding(
                            check="K4",
                            path=doc.rel,
                            line=lineno,
                            found=f"D{number}",
                            expected=f"D{CLAUSE_MIN}~D{CLAUSE_MAX}",
                            message="헌장 조항 번호 범위 밖",
                        )
                    )
                else:
                    result.resolved.append(f"{doc.rel}:{lineno}  D{number}")
    return result


# ---------------------------------------------------------------------------
# K5 — 폐지 토큰 부재
# ---------------------------------------------------------------------------


def exemption_spans(line: str, exemptions: list[dict[str, Any]]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for entry in exemptions:
        if entry.get("kind") != "span":
            continue
        try:
            pattern = re.compile(entry["pattern"])
        except re.error as exc:
            fail_env(f"exemptions span 패턴 컴파일 실패: {entry['pattern']!r}: {exc}")
        for match in pattern.finditer(line):
            spans.append((match.start(), match.end()))
    return spans


def line_is_marked(line: str, exemptions: list[dict[str, Any]]) -> bool:
    for entry in exemptions:
        if entry.get("kind") == "line-marker" and entry["marker"] in line:
            return True
    return False


def check_k5(docs: list[DocFile], data: dict[str, Any]) -> CheckResult:
    result = CheckResult("K5", "폐지 토큰 부재")
    tokens: list[dict[str, Any]] = data["tokens"]
    exemptions: list[dict[str, Any]] = data.get("exemptions", []) or []
    for doc in docs:
        for lineno, line in enumerate(doc.lines, start=1):
            marked = line_is_marked(line, exemptions)
            spans = exemption_spans(line, exemptions)
            for entry in tokens:
                token = entry["token"]
                haystack = line.lower() if entry.get("case_insensitive") else line
                needle = token.lower() if entry.get("case_insensitive") else token
                start = haystack.find(needle)
                while start != -1:
                    inside = any(lo <= start < hi for lo, hi in spans)
                    if marked or inside:
                        # 폐지 사실을 기록하는 문맥(취소선·폐지 표지)은 면제하되 감사 가능하게 남긴다.
                        result.waived.append(
                            f"{doc.rel}:{lineno}  {token} — {'폐지 표지' if marked else '취소선'} 문맥"
                        )
                    else:
                        result.findings.append(
                            Finding(
                                check="K5",
                                path=doc.rel,
                                line=lineno,
                                found=token,
                                expected="폐지 토큰 부재 (또는 취소선·폐지 표지 문맥)",
                                message=str(entry.get("note", "폐지 토큰이 살아있는 문언에 등장한다")),
                            )
                        )
                    start = haystack.find(needle, start + 1)
    return result


# ---------------------------------------------------------------------------
# K6·K7 — 계약 파일 파싱 · JSON Schema 메타 검증
# ---------------------------------------------------------------------------


def check_k6(repo: str, rel_paths: list[str]) -> tuple[CheckResult, dict[str, Any]]:
    result = CheckResult("K6", "계약 파일 파싱")
    parsed: dict[str, Any] = {}
    for rel in rel_paths:
        path = os.path.join(repo, rel)
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except Exception as exc:  # noqa: BLE001
            result.findings.append(
                Finding("K6", rel, 0, type(exc).__name__, "읽기 가능한 UTF-8 파일", str(exc))
            )
            continue
        try:
            if rel.endswith(".json"):
                parsed[rel] = json.loads(text)
            else:
                parsed[rel] = yaml.safe_load(text)
        except json.JSONDecodeError as exc:
            result.findings.append(
                Finding("K6", rel, exc.lineno, exc.msg, "유효한 JSON", f"JSON 파싱 실패: {exc}")
            )
            continue
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            lineno = (mark.line + 1) if mark is not None else 0
            result.findings.append(
                Finding("K6", rel, lineno, str(getattr(exc, "problem", exc)), "유효한 YAML", f"YAML 파싱 실패: {exc}")
            )
            continue
        result.resolved.append(f"{rel}  파싱 OK")
    return result, parsed


def check_k7(parsed: dict[str, Any]) -> CheckResult:
    result = CheckResult("K7", "스키마 메타 검증")
    for rel in sorted(parsed):
        if not rel.endswith(".json"):
            continue
        data = parsed[rel]
        if not isinstance(data, dict) or "$schema" not in data:
            continue
        declared = data.get("$schema")
        if declared != DRAFT_2020_12:
            result.findings.append(
                Finding("K7", rel, 0, str(declared), DRAFT_2020_12, "draft 2020-12 선언이 아니다")
            )
            continue
        try:
            Draft202012Validator.check_schema(data)
        except Exception as exc:  # noqa: BLE001 - jsonschema 예외 계층 폭이 넓다
            result.findings.append(
                Finding("K7", rel, 0, type(exc).__name__, "check_schema() 통과", str(exc).splitlines()[0])
            )
            continue
        result.resolved.append(f"{rel}  draft 2020-12 · check_schema OK")
    return result


# ---------------------------------------------------------------------------
# 출력
# ---------------------------------------------------------------------------


def emit_text(results: list[CheckResult], verbose: bool) -> None:
    for check in results:
        print(f"{check.status}  {check.id}  {check.name}"
              f"  (해소 {len(check.resolved)} · 면제 {len(check.waived)} · 결함 {len(check.findings)})")
        for finding in check.findings:
            locus = f"{finding.path}:{finding.line}" if finding.line else finding.path
            print(f"    - [{finding.check}] {locus}")
            print(f"        found   : {finding.found}")
            print(f"        expected: {finding.expected}")
            print(f"        {finding.message}")
        if verbose:
            for item in check.waived:
                print(f"    ~ 면제: {item}")
            for item in check.resolved:
                print(f"    . {item}")
    total = sum(len(check.findings) for check in results)
    print("RESULT: PASS" if total == 0 else f"RESULT: FAIL ({total} findings)")


def emit_json(repo: str, results: list[CheckResult], verbose: bool) -> None:
    total = sum(len(check.findings) for check in results)
    payload: dict[str, Any] = {
        "repo": repo,
        "result": "PASS" if total == 0 else "FAIL",
        "finding_count": total,
        "checks": [
            {
                "id": check.id,
                "name": check.name,
                "status": check.status,
                "findings": len(check.findings),
                "resolved": len(check.resolved),
                "waived": check.waived,
            }
            for check in results
        ],
        "findings": [finding.as_dict() for check in results for finding in check.findings],
    }
    if verbose:
        payload["resolved"] = {check.id: check.resolved for check in results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    default_repo = os.path.dirname(script_dir)

    parser = argparse.ArgumentParser(
        prog="check_spec_refs.py",
        description="patent-docent 문서·계약 정합 검사기 (read-only).",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    parser.add_argument("--verbose", action="store_true", help="해소된 참조를 대상 절 제목과 함께 전량 출력")
    parser.add_argument("--json", action="store_true", dest="as_json", help="기계 판독 결과(JSON) 출력")
    args = parser.parse_args(argv)

    repo = os.path.realpath(args.repo)
    if not os.path.isdir(repo):
        fail_env(f"리포 경로가 디렉터리가 아니다: {args.repo}")

    # 자기 배제 단정용 절대 경로 집합 (격리 요건 3항).
    self_paths = {script_path, os.path.realpath(os.path.join(script_dir, RETIRED_TOKENS_FILE))}

    retired = load_retired_tokens(script_dir)

    # --- 스캔 목록 확정 → 격리 검사 → 그 다음에야 읽는다 ---
    doc_targets = list(DOC_TARGETS)
    enforce_isolation(doc_targets, "K1·K3·K4·K5 문서 대상", self_paths, repo)

    contract_targets = glob_contract_files(repo)
    enforce_isolation(contract_targets, "K6·K7 계약 대상", self_paths, repo)

    docs = [load_doc(repo, rel) for rel in doc_targets]
    spec = next((doc for doc in docs if doc.rel == CONTRACT_TABLE_DOC), None)
    if spec is None:
        fail_env(f"계약 현황표 대상 문서가 allowlist에 없다: {CONTRACT_TABLE_DOC}")

    sections = build_section_index(docs)
    table_rows, table_error = parse_status_table(spec)

    k6, parsed = check_k6(repo, contract_targets)
    results = [
        check_k1(docs, sections),
        check_k2(repo, spec, table_rows, table_error),
        check_k3(
            collect_doc_contract_lines(docs),
            collect_file_contract_lines(parsed),
            planned_names_from_table(table_rows),
        ),
        check_k4(docs),
        check_k5(docs, retired),
        k6,
        check_k7(parsed),
    ]
    results.sort(key=lambda check: check.id)

    if args.as_json:
        emit_json(repo, results, args.verbose)
    else:
        emit_text(results, args.verbose)

    total = sum(len(check.findings) for check in results)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
