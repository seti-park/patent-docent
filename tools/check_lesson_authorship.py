#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`docs/lessons/` 저자 경계 관문 (재정 2026-09-01 T20).

이 도구가 주장하는 것은 **「추기·머리말로 자기 신고한 절에 저자 표시가 있는가」 하나**다.
표지 없이 감수자 절 **안에** 끼워 넣은 총괄 문장은 기계가 구별할 수 없다 — 그 경계는 사람이
지킨다. M0.6 이 FAIL 을 받은 사유가 *"강제의 범위를 실제보다 넓게 말한 것"* 이고,
2026-08-19 감수 A′ 가 그 거울상(**좁게 말한 것**)도 같은 결함으로 판정했다. 그러므로 넓게도
좁게도 적지 않는다.

판정은 세 가지뿐이다. R1은 각 Markdown 파일 앞 20줄의 원문 보존 선언을, R2는 제목에서
`추기`·`머리말`로 자기 신고한 절 머리 3줄의 정확한 저자 표지 `총괄 저작`을, R3은 그 표지를
단 절 제목의 자기 신고를 대조한다. 절은 ATX 제목 줄에서 다음 ATX 제목 줄 직전까지다.

★ 자기매칭 격리
이 소스에는 탐지 토큰(`추기`·`총괄 저작`)이 리터럴로 들어 있다. 그러나 검사 대상은 `--root`
아래의 `.md` 파일뿐이고 이 소스는 `tools/`의 `.py` 파일이므로 스캔 시야 밖이다. 기본 루트
`docs/lessons/` 역시 `tools/`를 포함하지 않는다. 따라서 검사기 자신의 패턴 견본이 피검체로
들어가는 자기매칭은 성립하지 않는다(`tools/check_schema_enforcement.py`의 선례와 같은 격리).

종료 코드 (SPEC §8.3 관례):
  0 = 전건 통과 / 1 = 검증 실패 / 2 = 입력·환경 오류

명시 비교와 종료 코드만 사용하므로 `python3 -O`에서도 판정이 같다.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PRESERVATION_MARKERS: tuple[str, ...] = (
    "감수 원문",
    "자문 원문",
    "원문 보존",
    "원문 그대로",
)
SECTION_MARKERS: tuple[str, ...] = ("추기", "머리말")
AUTHOR_MARKER = "총괄 저작"
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SECTION_MARKER_RE = re.compile(
    rf"(?<![0-9A-Za-z가-힣_])(?:{'|'.join(map(re.escape, SECTION_MARKERS))})"
    r"(?![0-9A-Za-z가-힣_])"
)
# `총괄 저작이며`처럼 조사가 붙은 표지는 허용하되 `총괄 저작분` 같은 합성어의 부분 일치는
# 표지로 세지 않는다. 제목 토큰도 같은 이유로 `머리말이`를 `머리말` 신고로 세지 않는다.
AUTHOR_MARKER_RE = re.compile(
    r"총괄 저작(?=$|[^0-9A-Za-z가-힣_]|이(?:며|다|라고|라는|므로|어서|지만)"
    r"(?=$|[^0-9A-Za-z가-힣_]))"
)


@dataclass(frozen=True)
class Section:
    """ATX 제목으로 시작하는 한 절과 그 1-based 좌표."""

    line_number: int
    heading: str
    head: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    """한 규칙의 명시 비교 결과."""

    rule: str
    path: Path
    line_number: int
    heading: str
    expected: str
    actual: str


class InputError(Exception):
    """입력 루트나 Markdown 파일을 읽을 수 없을 때의 환경 오류."""


class ExitMarkerParser(argparse.ArgumentParser):
    """인자 오류에도 리포 관례의 종료 마커를 남긴다."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print(f"INPUT ERROR: {message}", file=sys.stderr)
        print("EXIT=2")
        raise SystemExit(2)


def read_markdown(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise InputError(f"Markdown 파일을 읽을 수 없다: {path} — {exc}") from exc


def sections(lines: list[str]) -> list[Section]:
    """Markdown의 ATX 제목 줄을 경계로 절을 나눈다."""
    starts: list[int] = []
    fence_character = ""
    fence_length = 0
    for index, line in enumerate(lines):
        if fence_character:
            closing_fence = re.fullmatch(
                rf" {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                line,
            )
            if closing_fence is not None:
                fence_character = ""
                fence_length = 0
            continue
        fence_match = FENCE_RE.match(line)
        if fence_match is not None:
            fence = fence_match.group(1)
            fence_character = fence[0]
            fence_length = len(fence)
            continue
        if HEADING_RE.match(line):
            starts.append(index)
    result: list[Section] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        head_end = min(start + 3, end)
        result.append(
            Section(
                line_number=start + 1,
                heading=lines[start].strip(),
                head=tuple(lines[start:head_end]),
            )
        )
    return result


def check_file(path: Path) -> list[Finding]:
    lines = read_markdown(path)
    findings: list[Finding] = []

    first_twenty = lines[:20]
    has_preservation_marker = any(
        marker in line for line in first_twenty for marker in PRESERVATION_MARKERS
    )
    if not has_preservation_marker:
        findings.append(
            Finding(
                rule="R1",
                path=path,
                line_number=1,
                heading=lines[0].strip() if lines else "(빈 파일)",
                expected="앞 20줄 안에 원문 보존 선언 1개 이상",
                actual="없음",
            )
        )

    for section in sections(lines):
        declares_section_kind = SECTION_MARKER_RE.search(section.heading) is not None
        head_text = "\n".join(section.head)
        has_author_marker = AUTHOR_MARKER_RE.search(head_text) is not None

        if declares_section_kind and not has_author_marker:
            findings.append(
                Finding(
                    rule="R2",
                    path=path,
                    line_number=section.line_number,
                    heading=section.heading,
                    expected=f"절 머리 3줄 안에 정확한 문자열 `{AUTHOR_MARKER}`",
                    actual="없음",
                )
            )
        if has_author_marker and not declares_section_kind:
            findings.append(
                Finding(
                    rule="R3",
                    path=path,
                    line_number=section.line_number,
                    heading=section.heading,
                    expected="제목 줄에 `추기` 또는 `머리말` 토큰",
                    actual="없음",
                )
            )

    return findings


def markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        raise InputError(f"--root 경로가 없다: {root}")
    if not root.is_dir():
        raise InputError(f"--root 경로가 디렉터리가 아니다: {root}")
    try:
        files = sorted(path for path in root.rglob("*.md") if path.is_file())
    except OSError as exc:
        raise InputError(f"--root 아래 파일을 열거할 수 없다: {root} — {exc}") from exc
    if not files:
        raise InputError(f"--root 아래에 .md 파일이 없다: {root}")
    return files


def report_finding(finding: Finding) -> None:
    print(
        f"FAIL {finding.rule} {finding.path}:{finding.line_number}"
        f" · 제목: {finding.heading}"
        f" · 기대: {finding.expected}"
        f" · 실제: {finding.actual}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = ExitMarkerParser(
        prog="check_lesson_authorship.py",
        description="docs/lessons Markdown 절의 원문 보존 선언·총괄 추기 저자 표지를 대조한다.",
    )
    parser.add_argument(
        "--root",
        default="docs/lessons",
        help="검사할 lessons 디렉터리 (기본: docs/lessons)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root)

    try:
        files = markdown_files(root)
        findings = [finding for path in files for finding in check_file(path)]
    except InputError as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        print("EXIT=2")
        return 2

    for finding in findings:
        report_finding(finding)

    if findings:
        print(f"RESULT: FAIL — {len(files)}개 파일 · 검증 실패 {len(findings)}건")
        print("EXIT=1")
        return 1

    print(f"RESULT: PASS — {len(files)}개 Markdown 파일 전건 통과 (R1·R2·R3)")
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
