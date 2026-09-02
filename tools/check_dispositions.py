#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""지적 처분 원장 관문 (재정 2026-09-02 T27).

이 도구가 주장하는 것은 **하나**다 — *「감수 원문의 총괄 머리말에 열거된 지적이 전부
처분표에 있고, 처분표에 열거 밖 지적이 없으며, 처분 값이 4종 중 하나인가」*. 차집합은
**양방향으로** 0 이어야 한다.

★ 주장하지 않는 것 — **열거가 원문의 지적을 빠짐없이 담았는지는 기계가 모른다.** 감수 원문의
어느 문단이 지적이고 어느 문단이 소견인지는 사람이 읽어야 갈리며, 지적 하나를 앞/뒷절반으로
쪼갤지도 사람의 판단이다. 그 판단은 **반입 시점**에 일어난다(원장 T27 ⒜ ① — 주의가 가장 높은
순간에 두라는 것이 그 결정의 취지다). 이 관문은 그렇게 열거된 것과 처분표를 대조할 뿐이다.
넓게도 좁게도 적지 않는다(M0.6 FAIL 사유와 2026-08-19 감수 A′ 의 거울상 판정).

판정은 넷이다.
  G1 등재 현황 완전성 — `--lessons-root` 의 `*.md` 집합 == §0 `파일` 열 집합(양방향) · §0 중복 금지
  G2 상태 어휘       — §0 상태 ∈ {등재, 선행 종결} · `선행 종결` 은 포인터 필수 · §1 행 금지
  G3 열거 ↔ 처분표    — `등재` 파일마다 총괄 머리말 안에 열거 줄 정확히 하나 · id 집합이 §1 과 상등
  G4 처분 행 규격     — 처분 4종 · 사유·포인터 비지 않음 · (파일, id) 중복 금지 · §1 파일 ⊆ §0 파일

총괄 머리말의 판별은 `tools/check_lesson_authorship.py` 를 **import 해 재사용**한다(절 분할
`sections()` · 자기 신고 토큰 · 저자 표지 정규식). 판별 규칙을 두 벌 만들면 한 벌은 반드시
낡는다 — 그 도구는 이 파일에서 읽기만 하고 고치지 않는다.

★ 자기매칭 격리 (SPEC §8.3 8항)
이 소스에는 탐지 토큰(`지적 열거 =` · `머리말` · 처분 어휘 4종)이 리터럴로 들어 있다. 그러나
스캔 대상은 `--lessons-root` 아래의 `.md` 파일과 `--dispositions` 가 가리키는 파일 하나뿐이고,
이 소스는 `tools/` 의 `.py` 파일이라 두 시야 어디에도 들지 않는다. 기본값(`docs/lessons` ·
`docs/decisions/DISPOSITIONS.md`) 역시 `tools/` 를 포함하지 않는다. 따라서 검사기 자신의 패턴
견본이 피검체로 들어가는 자기매칭은 성립하지 않는다.

종료 코드 (SPEC §8.3 3항):
  0 = 전건 통과 / 1 = 검증 실패 / 2 = 입력·환경 오류

`assert` 없이 명시 비교와 종료 코드만 쓰므로 `python3 -O` 에서도 판정이 같다.
"""

from __future__ import annotations

import argparse
import io
import re
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import check_lesson_authorship as authorship  # noqa: E402  (경로 주입 뒤에 온다)


DEFAULT_LESSONS_ROOT = "docs/lessons"
DEFAULT_DISPOSITIONS = "docs/decisions/DISPOSITIONS.md"

STATUS_LISTED = "등재"
STATUS_CLOSED_EARLIER = "선행 종결"
STATUS_VOCABULARY: tuple[str, ...] = (STATUS_LISTED, STATUS_CLOSED_EARLIER)
DISPOSITION_VOCABULARY: tuple[str, ...] = ("수용", "부분 수용", "기각", "이연")

REGISTRY_HEADER: tuple[str, ...] = ("파일", "상태", "포인터")
DISPOSITION_HEADER: tuple[str, ...] = ("파일", "지적 id", "격", "처분", "사유", "포인터")

PREAMBLE_TOKEN = "머리말"
ENUMERATION_LABEL = "지적 열거"
ENUMERATION_RE = re.compile(rf"^[ \t]*{ENUMERATION_LABEL}[ \t]*=[ \t]*(?P<body>.*?)[ \t]*$")
ENUMERATION_EMPTY = "없음"
FINDING_ID_RE = re.compile(r"^[A-Za-z0-9′\-]+$")

# 빈 셀의 표기. 처분표의 격 열에만 허용되며 사유·포인터에서는 「비어 있음」으로 센다.
EMPTY_CELL_MARKS: tuple[str, ...] = ("", "—", "-", "–")


@dataclass(frozen=True)
class Row:
    """한 Markdown 파이프 표의 데이터 행과 그 1-based 줄 번호."""

    line_number: int
    cells: tuple[str, ...]


@dataclass(frozen=True)
class Table:
    """헤더 셀 튜플로 식별되는 표 하나."""

    line_number: int
    header: tuple[str, ...]
    rows: tuple[Row, ...]

    def column(self, row: Row, name: str) -> str:
        return row.cells[self.header.index(name)]


@dataclass(frozen=True)
class Finding:
    """한 규칙의 명시 비교 결과."""

    rule: str
    path: Path
    line_number: int
    locus: str
    expected: str
    actual: str


class InputError(Exception):
    """입력 경로나 파일을 읽을 수 없을 때의 환경 오류."""


class ExitMarkerParser(argparse.ArgumentParser):
    """인자 오류에도 리포 관례의 종료 마커를 남긴다."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print(f"INPUT ERROR: {message}", file=sys.stderr)
        print("EXIT=2")
        raise SystemExit(2)


# ---------------------------------------------------------------------------
# 읽기


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise InputError(f"파일을 읽을 수 없다: {path} — {exc}") from exc


def lesson_files(root: Path) -> list[Path]:
    if not root.exists():
        raise InputError(f"--lessons-root 경로가 없다: {root}")
    if not root.is_dir():
        raise InputError(f"--lessons-root 경로가 디렉터리가 아니다: {root}")
    try:
        files = sorted(path for path in root.rglob("*.md") if path.is_file())
    except OSError as exc:
        raise InputError(f"--lessons-root 아래를 열거할 수 없다: {root} — {exc}") from exc
    if not files:
        raise InputError(f"--lessons-root 아래에 .md 파일이 없다: {root}")
    return files


# ---------------------------------------------------------------------------
# Markdown 파이프 표 파싱


def split_pipe_row(line: str) -> tuple[str, ...] | None:
    """`| a | b |` 형태의 한 줄을 셀 튜플로 가른다. 표 행이 아니면 None."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    body = stripped[1:]
    if body.endswith("|"):
        body = body[:-1]
    return tuple(cell.strip() for cell in body.split("|"))


def is_delimiter_row(cells: tuple[str, ...]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell) is not None for cell in cells) and bool(cells)


def parse_tables(lines: list[str]) -> list[Table]:
    """문서 안의 모든 파이프 표를 헤더·데이터 행으로 나눈다."""
    tables: list[Table] = []
    index = 0
    while index < len(lines) - 1:
        header_cells = split_pipe_row(lines[index])
        delimiter_cells = split_pipe_row(lines[index + 1])
        if (
            header_cells is None
            or delimiter_cells is None
            or not is_delimiter_row(delimiter_cells)
            or len(header_cells) != len(delimiter_cells)
        ):
            index += 1
            continue
        rows: list[Row] = []
        cursor = index + 2
        while cursor < len(lines):
            cells = split_pipe_row(lines[cursor])
            if cells is None:
                break
            rows.append(Row(line_number=cursor + 1, cells=cells))
            cursor += 1
        tables.append(
            Table(line_number=index + 1, header=header_cells, rows=tuple(rows))
        )
        index = cursor
    return tables


def select_table(
    tables: list[Table], header: tuple[str, ...]
) -> tuple[Table | None, int]:
    matched = [table for table in tables if table.header == header]
    if len(matched) == 1:
        return matched[0], 1
    return None, len(matched)


# ---------------------------------------------------------------------------
# 총괄 머리말 · 열거 줄


def preamble_spans(lines: list[str]) -> list[tuple[int, int, str]]:
    """총괄 머리말 절의 (시작 index, 끝 index, 제목) 목록.

    판별은 SPEC §8.3 10항 ② 규격 그대로이며 `check_lesson_authorship` 의 절 분할과 정규식을
    그대로 쓴다 — 제목 줄이 `머리말` 로 자기 신고하고 절 머리 3줄 안에 `총괄 저작` 이 있는 절.
    """
    sections = authorship.sections(lines)
    spans: list[tuple[int, int, str]] = []
    for position, section in enumerate(sections):
        start = section.line_number - 1
        if position + 1 < len(sections):
            end = sections[position + 1].line_number - 1
        else:
            end = len(lines)
        declares_preamble = any(
            match.group(0) == PREAMBLE_TOKEN
            for match in authorship.SECTION_MARKER_RE.finditer(section.heading)
        )
        has_author_marker = (
            authorship.AUTHOR_MARKER_RE.search("\n".join(section.head)) is not None
        )
        if declares_preamble and has_author_marker:
            spans.append((start, end, section.heading))
    return spans


def enumeration_lines(lines: list[str]) -> list[tuple[int, str]]:
    """총괄 머리말 절 안의 열거 줄 목록 — (1-based 줄 번호, 본문)."""
    found: list[tuple[int, str]] = []
    for start, end, _heading in preamble_spans(lines):
        for index in range(start, end):
            match = ENUMERATION_RE.match(lines[index])
            if match is not None:
                found.append((index + 1, match.group("body")))
    return found


def parse_enumeration(body: str) -> tuple[list[str], list[str]]:
    """열거 본문을 (id 목록, 문법 위반 토큰 목록)으로 가른다."""
    if body.strip() == ENUMERATION_EMPTY:
        return [], []
    tokens = [token.strip() for token in body.split(",")]
    identifiers: list[str] = []
    malformed: list[str] = []
    for token in tokens:
        if FINDING_ID_RE.fullmatch(token) is None:
            malformed.append(token)
        else:
            identifiers.append(token)
    return identifiers, malformed


def is_empty_cell(value: str) -> bool:
    return value.strip() in EMPTY_CELL_MARKS


# ---------------------------------------------------------------------------
# 판정


def evaluate(lessons_root: Path, dispositions_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = lesson_files(lessons_root)
    ledger_lines = read_lines(dispositions_path)
    tables = parse_tables(ledger_lines)

    registry, registry_count = select_table(tables, REGISTRY_HEADER)
    dispositions, disposition_count = select_table(tables, DISPOSITION_HEADER)

    if registry is None:
        findings.append(
            Finding(
                rule="G1",
                path=dispositions_path,
                line_number=1,
                locus="§0 등재 현황표",
                expected=f"열 이름 {list(REGISTRY_HEADER)} 인 표 1개",
                actual=f"{registry_count}개",
            )
        )
    if dispositions is None:
        findings.append(
            Finding(
                rule="G4",
                path=dispositions_path,
                line_number=1,
                locus="§1 처분표",
                expected=f"열 이름 {list(DISPOSITION_HEADER)} 인 표 1개",
                actual=f"{disposition_count}개",
            )
        )
    if registry is None or dispositions is None:
        return findings

    # ---- G1 등재 현황 완전성
    actual_names = [str(path.relative_to(lessons_root)) for path in files]
    listed_names: list[str] = []
    seen: set[str] = set()
    for row in registry.rows:
        name = registry.column(row, "파일").strip("` ")
        listed_names.append(name)
        if name in seen:
            findings.append(
                Finding(
                    rule="G1",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§0 · {name}",
                    expected="§0 에 파일당 행 1개",
                    actual="중복 행",
                )
            )
        seen.add(name)

    for name in sorted(set(actual_names) - set(listed_names)):
        findings.append(
            Finding(
                rule="G1",
                path=lessons_root / name,
                line_number=1,
                locus=f"§0 미등재 · {name}",
                expected="§0 등재 현황표에 행 1개",
                actual="행 없음",
            )
        )
    for name in sorted(set(listed_names) - set(actual_names)):
        findings.append(
            Finding(
                rule="G1",
                path=dispositions_path,
                line_number=registry.line_number,
                locus=f"§0 유령 행 · {name}",
                expected=f"{lessons_root} 아래에 실재하는 파일",
                actual="파일 없음",
            )
        )

    # ---- G4 처분 행 규격 (뒤의 G2·G3 이 이 결과를 쓴다)
    rows_by_file: dict[str, list[tuple[Row, str]]] = {}
    pairs_seen: set[tuple[str, str]] = set()
    for row in dispositions.rows:
        name = dispositions.column(row, "파일").strip("` ")
        identifier = dispositions.column(row, "지적 id").strip("`* ")
        disposition = dispositions.column(row, "처분").strip("`* ")
        reason = dispositions.column(row, "사유")
        pointer = dispositions.column(row, "포인터")
        rows_by_file.setdefault(name, []).append((row, identifier))

        if disposition not in DISPOSITION_VOCABULARY:
            findings.append(
                Finding(
                    rule="G4",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§1 · {name} · {identifier}",
                    expected=f"처분 ∈ {list(DISPOSITION_VOCABULARY)}",
                    actual=repr(disposition),
                )
            )
        if is_empty_cell(reason):
            findings.append(
                Finding(
                    rule="G4",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§1 · {name} · {identifier}",
                    expected="사유 한 줄(비어 있지 않음)",
                    actual="비어 있음",
                )
            )
        if is_empty_cell(pointer):
            findings.append(
                Finding(
                    rule="G4",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§1 · {name} · {identifier}",
                    expected="포인터(처분이 실제로 적힌 자리)",
                    actual="비어 있음",
                )
            )
        if (name, identifier) in pairs_seen:
            findings.append(
                Finding(
                    rule="G4",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§1 · {name} · {identifier}",
                    expected="(파일, 지적 id) 조합당 행 1개",
                    actual="중복 행",
                )
            )
        pairs_seen.add((name, identifier))
        if name not in set(listed_names):
            findings.append(
                Finding(
                    rule="G4",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§1 · {name}",
                    expected="§0 등재 현황표에 있는 파일",
                    actual="§0 에 없음",
                )
            )

    # ---- G2 상태 어휘
    listed_files: list[str] = []
    for row in registry.rows:
        name = registry.column(row, "파일").strip("` ")
        status = registry.column(row, "상태").strip("`* ")
        pointer = registry.column(row, "포인터")
        if status not in STATUS_VOCABULARY:
            findings.append(
                Finding(
                    rule="G2",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§0 · {name}",
                    expected=f"상태 ∈ {list(STATUS_VOCABULARY)}",
                    actual=repr(status),
                )
            )
            continue
        if status == STATUS_LISTED:
            listed_files.append(name)
            continue
        if is_empty_cell(pointer):
            findings.append(
                Finding(
                    rule="G2",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§0 · {name}",
                    expected=f"`{STATUS_CLOSED_EARLIER}` 는 처분이 닫힌 자리의 포인터 필수",
                    actual="비어 있음",
                )
            )
        if name in rows_by_file:
            findings.append(
                Finding(
                    rule="G2",
                    path=dispositions_path,
                    line_number=row.line_number,
                    locus=f"§0 · {name}",
                    expected=f"`{STATUS_CLOSED_EARLIER}` 파일은 §1 에 행이 없어야 한다",
                    actual=f"§1 행 {len(rows_by_file[name])}건",
                )
            )

    # ---- G3 열거 ↔ 처분표
    for name in listed_files:
        path = lessons_root / name
        if not path.is_file():
            continue  # 파일 부재는 G1 이 이미 보고했다.
        lines = read_lines(path)
        enumerations = enumeration_lines(lines)
        if len(enumerations) != 1:
            findings.append(
                Finding(
                    rule="G3",
                    path=path,
                    line_number=enumerations[0][0] if enumerations else 1,
                    locus=f"총괄 머리말 · `{ENUMERATION_LABEL} =` 줄",
                    expected="총괄 머리말 절 안에 열거 줄 정확히 1개",
                    actual=f"{len(enumerations)}개",
                )
            )
            continue
        line_number, body = enumerations[0]
        enumerated, malformed = parse_enumeration(body)
        for token in malformed:
            findings.append(
                Finding(
                    rule="G3",
                    path=path,
                    line_number=line_number,
                    locus=f"총괄 머리말 · id {token!r}",
                    expected=f"id 문자 집합 {FINDING_ID_RE.pattern}",
                    actual="문법 위반",
                )
            )
        table_ids = [identifier for _row, identifier in rows_by_file.get(name, [])]
        for identifier in sorted(set(enumerated) - set(table_ids)):
            findings.append(
                Finding(
                    rule="G3",
                    path=path,
                    line_number=line_number,
                    locus=f"열거에 있고 §1 에 없다 · {identifier}",
                    expected="§1 처분표에 그 id 의 행",
                    actual="행 없음",
                )
            )
        for identifier in sorted(set(table_ids) - set(enumerated)):
            findings.append(
                Finding(
                    rule="G3",
                    path=dispositions_path,
                    line_number=registry.line_number,
                    locus=f"§1 에 있고 열거에 없다 · {name} · {identifier}",
                    expected=f"{name} 의 총괄 머리말 열거에 그 id",
                    actual="열거에 없음",
                )
            )

    return findings


def report_finding(finding: Finding) -> None:
    print(
        f"FAIL {finding.rule} {finding.path}:{finding.line_number}"
        f" · {finding.locus}"
        f" · 기대: {finding.expected}"
        f" · 실제: {finding.actual}"
    )


def run(lessons_root: Path, dispositions_path: Path) -> int:
    try:
        findings = evaluate(lessons_root, dispositions_path)
    except InputError as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        print("EXIT=2")
        return 2

    for finding in findings:
        report_finding(finding)

    if findings:
        print(f"RESULT: FAIL — 검증 실패 {len(findings)}건")
        print("EXIT=1")
        return 1

    print(
        "RESULT: PASS — 등재 현황·상태 어휘·열거 ↔ 처분표 차집합·처분 행 규격 전건 통과"
        " (G1·G2·G3·G4)"
    )
    print("EXIT=0")
    return 0


# ---------------------------------------------------------------------------
# --self-test — 결함 6종을 임시 사본에 심어 거부를 실증한다


def quiet_run(lessons_root: Path, dispositions_path: Path) -> int:
    """검사를 돌리되 출력은 삼킨다 — self-test 는 종료 코드만 본다."""
    sink = io.StringIO()
    with redirect_stdout(sink):
        return run(lessons_root, dispositions_path)


def canonical_probe_target(lessons_root: Path, dispositions_path: Path) -> tuple[str, Row, Table]:
    """결함을 심을 자리 — `등재` 이면서 §1 에 행이 있는 첫 파일과 그 첫 행."""
    tables = parse_tables(read_lines(dispositions_path))
    registry, _ = select_table(tables, REGISTRY_HEADER)
    dispositions, _ = select_table(tables, DISPOSITION_HEADER)
    if registry is None or dispositions is None:
        raise InputError("self-test: §0·§1 표를 찾지 못해 결함을 심을 자리가 없다")
    for row in registry.rows:
        name = registry.column(row, "파일").strip("` ")
        if registry.column(row, "상태").strip("`* ") != STATUS_LISTED:
            continue
        for disposition_row in dispositions.rows:
            if dispositions.column(disposition_row, "파일").strip("` ") == name:
                return name, disposition_row, dispositions
    raise InputError("self-test: `등재` 이면서 §1 에 행이 있는 파일이 없다")


def make_sandbox(
    lessons_root: Path, dispositions_path: Path, workspace: Path
) -> tuple[Path, Path]:
    sandbox_lessons = workspace / "lessons"
    sandbox_ledger = workspace / dispositions_path.name
    shutil.copytree(lessons_root, sandbox_lessons)
    shutil.copy2(dispositions_path, sandbox_ledger)
    return sandbox_lessons, sandbox_ledger


def replace_line(path: Path, line_number: int, replacement: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[line_number - 1 : line_number] = replacement
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_test(lessons_root: Path, dispositions_path: Path) -> int:
    """canon = exit 0 · 심은 결함 6종 = 전건 exit 1 을 실증한다."""
    outcomes: list[tuple[str, int, int]] = []

    canonical = quiet_run(lessons_root, dispositions_path)
    outcomes.append(("canon (무변조)", canonical, 0))

    target_name, target_row, disposition_table = canonical_probe_target(
        lessons_root, dispositions_path
    )
    target_id = disposition_table.column(target_row, "지적 id").strip("`* ")
    disposition_index = disposition_table.header.index("처분")

    with tempfile.TemporaryDirectory(prefix="check-dispositions-selftest-") as raw:
        base = Path(raw)

        # ⒜ 열거된 id 의 처분 행 삭제
        workspace = base / "a"
        workspace.mkdir()
        lessons, ledger = make_sandbox(lessons_root, dispositions_path, workspace)
        replace_line(ledger, target_row.line_number, [])
        outcomes.append((f"⒜ 처분 행 삭제 ({target_name} · {target_id})", quiet_run(lessons, ledger), 1))

        # ⒝ 열거에 없는 id 의 처분 행 추가
        workspace = base / "b"
        workspace.mkdir()
        lessons, ledger = make_sandbox(lessons_root, dispositions_path, workspace)
        injected = (
            f"| {target_name} | ZZ-99 | — | 수용 | self-test 가 심은 행 |"
            " self-test |"
        )
        replace_line(
            ledger,
            target_row.line_number,
            [ledger.read_text(encoding="utf-8").splitlines()[target_row.line_number - 1], injected],
        )
        outcomes.append(("⒝ 열거 밖 id 의 처분 행 추가 (ZZ-99)", quiet_run(lessons, ledger), 1))

        # ⒞ 처분 값을 `보류` 로 변조
        workspace = base / "c"
        workspace.mkdir()
        lessons, ledger = make_sandbox(lessons_root, dispositions_path, workspace)
        mutated = list(target_row.cells)
        mutated[disposition_index] = "보류"
        replace_line(ledger, target_row.line_number, ["| " + " | ".join(mutated) + " |"])
        outcomes.append(("⒞ 처분 값 변조 (보류)", quiet_run(lessons, ledger), 1))

        # ⒟ lessons-root 에 `.md` 하나 추가 (§0 미등재)
        workspace = base / "d"
        workspace.mkdir()
        lessons, ledger = make_sandbox(lessons_root, dispositions_path, workspace)
        (lessons / "zz-self-test-injected.md").write_text(
            "# self-test 가 심은 파일 — 감수 원문 보존 선언 자리\n", encoding="utf-8"
        )
        outcomes.append(("⒟ §0 미등재 파일 추가", quiet_run(lessons, ledger), 1))

        # ⒠ 등재 파일의 열거 줄 삭제 / ⒡ 열거 줄 두 개
        for label, replacement_factory, key in (
            ("⒠ 열거 줄 삭제", lambda line: [], "e"),
            ("⒡ 열거 줄 두 개", lambda line: [line, line], "f"),
        ):
            workspace = base / key
            workspace.mkdir()
            lessons, ledger = make_sandbox(lessons_root, dispositions_path, workspace)
            target_file = lessons / target_name
            enumerations = enumeration_lines(read_lines(target_file))
            if len(enumerations) != 1:
                print(
                    f"SELF-TEST INPUT ERROR: {target_name} 의 열거 줄이"
                    f" {len(enumerations)}개라 결함을 심을 수 없다",
                    file=sys.stderr,
                )
                print("EXIT=2")
                return 2
            line_number = enumerations[0][0]
            original = target_file.read_text(encoding="utf-8").splitlines()[line_number - 1]
            replace_line(target_file, line_number, replacement_factory(original))
            outcomes.append((f"{label} ({target_name})", quiet_run(lessons, ledger), 1))

    failures = 0
    for label, got, want in outcomes:
        verdict = "OK" if got == want else "MISMATCH"
        if got != want:
            failures += 1
        print(f"SELF-TEST {verdict:9} {label} — got={got} want={want}")

    if failures:
        print(f"RESULT: FAIL — self-test {len(outcomes)}건 중 {failures}건 불일치")
        print("EXIT=1")
        return 1

    print(f"RESULT: PASS — self-test {len(outcomes)}건 전건 일치 (canon 1 + 심은 결함 6종)")
    print("EXIT=0")
    return 0


# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = ExitMarkerParser(
        prog="check_dispositions.py",
        description=(
            "docs/lessons 총괄 머리말의 지적 열거와 지적 처분 원장의 처분표를 대조한다."
        ),
    )
    parser.add_argument(
        "--lessons-root",
        default=DEFAULT_LESSONS_ROOT,
        help=f"감수 원문 디렉터리 (기본: {DEFAULT_LESSONS_ROOT})",
    )
    parser.add_argument(
        "--dispositions",
        default=DEFAULT_DISPOSITIONS,
        help=f"지적 처분 원장 파일 (기본: {DEFAULT_DISPOSITIONS})",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="임시 사본에 결함 6종을 심어 거부를 실증한다 (정본 무접촉)",
    )
    args = parser.parse_args(argv)

    lessons_root = Path(args.lessons_root)
    dispositions_path = Path(args.dispositions)

    if args.self_test:
        try:
            return self_test(lessons_root, dispositions_path)
        except InputError as exc:
            print(f"INPUT ERROR: {exc}", file=sys.stderr)
            print("EXIT=2")
            return 2
        except OSError as exc:
            print(f"INPUT ERROR: self-test 사본을 만들 수 없다 — {exc}", file=sys.stderr)
            print("EXIT=2")
            return 2

    return run(lessons_root, dispositions_path)


if __name__ == "__main__":
    sys.exit(main())
