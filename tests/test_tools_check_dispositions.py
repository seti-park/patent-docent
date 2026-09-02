# -*- coding: utf-8 -*-
"""`tools/check_dispositions.py` 관문 회귀·거부 실증 (재정 2026-09-02 T27).

CLAUDE.md §3 관례에 따라 서브프로세스 종료 코드는 명시 비교하고, 불일치는 `pytest.fail()`로
기대·실제를 함께 보고한다. 정본 `docs/lessons`와 `docs/decisions/DISPOSITIONS.md`는 읽기만
하며 모든 변조는 `tmp_path` 사본에 심는다 — 도구의 `--self-test` 와 **별개로** 여기서 직접
심는다(도구가 자기 결함을 자기가 채점하는 순환을 피한다).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_dispositions.py"
LESSONS = REPO_ROOT / "docs" / "lessons"
DISPOSITIONS = REPO_ROOT / "docs" / "decisions" / "DISPOSITIONS.md"

# 결함을 심는 자리. 이 파일은 열거가 한 줄(`지적 열거 = V`)이고 §1 행이 하나뿐이라
# 변조의 전제가 명시적으로 확인된다.
TARGET_LESSON = "2026-09-01-fable-advice-g6-defect-ownership.md"
TARGET_ENUMERATION = "지적 열거 = V"
TARGET_ROW_PREFIX = f"| {TARGET_LESSON} | V |"


def run_tool(
    lessons_root: Path,
    dispositions: Path,
    *,
    self_test: bool = False,
    optimized: bool = False,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if optimized:
        env["PYTHONOPTIMIZE"] = "1"
    argv = [
        sys.executable,
        str(TOOL),
        "--lessons-root",
        str(lessons_root),
        "--dispositions",
        str(dispositions),
    ]
    if self_test:
        argv.append("--self-test")
    return subprocess.run(
        argv, cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False
    )


def output(proc: subprocess.CompletedProcess[str]) -> str:
    return f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"


def require_exit(proc: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    if proc.returncode != expected:
        pytest.fail(
            f"{label} EXIT MISMATCH: got={proc.returncode} want={expected}\n{output(proc)}"
        )


def require_output_contains(
    proc: subprocess.CompletedProcess[str], needles: tuple[str, ...], label: str
) -> None:
    combined = proc.stdout + proc.stderr
    missing = [needle for needle in needles if needle not in combined]
    if missing:
        pytest.fail(f"{label} OUTPUT MISMATCH: missing={missing!r}\n{output(proc)}")


def sandbox(tmp_path: Path) -> tuple[Path, Path]:
    lessons = tmp_path / "lessons"
    ledger = tmp_path / "DISPOSITIONS.md"
    shutil.copytree(LESSONS, lessons)
    shutil.copy2(DISPOSITIONS, ledger)
    return lessons, ledger


def rewrite_lines(path: Path, transform) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(transform(lines)) + "\n", encoding="utf-8")


def locate_once(lines: list[str], prefix: str, path: Path) -> int:
    matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        pytest.fail(f"변조 전제 불일치: {path.name}에서 {prefix!r} count={len(matches)}, want=1")
    return matches[0]


# ---------------------------------------------------------------------------
# canon


def test_canonical_ledger_passes() -> None:
    proc = run_tool(LESSONS, DISPOSITIONS)
    require_exit(proc, 0, "canonical")
    require_output_contains(proc, ("EXIT=0",), "canonical")


def test_canonical_ledger_passes_with_pythonoptimize() -> None:
    proc = run_tool(LESSONS, DISPOSITIONS, optimized=True)
    require_exit(proc, 0, "optimized canonical")


def test_self_test_passes() -> None:
    proc = run_tool(LESSONS, DISPOSITIONS, self_test=True)
    require_exit(proc, 0, "self-test")


def test_self_test_passes_with_pythonoptimize() -> None:
    proc = run_tool(LESSONS, DISPOSITIONS, self_test=True, optimized=True)
    require_exit(proc, 0, "optimized self-test")


# ---------------------------------------------------------------------------
# 결함 6종 — 여기서 직접 심는다


def test_missing_disposition_row_is_rejected(tmp_path: Path) -> None:
    """⒜ 열거된 id 의 처분 행을 지우면 G3 이 잡는다."""
    lessons, ledger = sandbox(tmp_path)
    rewrite_lines(
        ledger,
        lambda lines: [
            line for index, line in enumerate(lines)
            if index != locate_once(lines, TARGET_ROW_PREFIX, ledger)
        ],
    )
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒜ 처분 행 삭제")
    require_output_contains(proc, ("G3", TARGET_LESSON, "행 없음"), "⒜ 처분 행 삭제")


def test_unenumerated_disposition_row_is_rejected(tmp_path: Path) -> None:
    """⒝ 열거에 없는 id 의 처분 행을 더하면 G3 이 잡는다."""
    lessons, ledger = sandbox(tmp_path)
    injected = f"| {TARGET_LESSON} | ZZ-99 | — | 수용 | 심은 행 | 심은 포인터 |"

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        return lines[: index + 1] + [injected] + lines[index + 1 :]

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒝ 열거 밖 행 추가")
    require_output_contains(proc, ("G3", "ZZ-99", "열거에 없음"), "⒝ 열거 밖 행 추가")


def test_unknown_disposition_value_is_rejected(tmp_path: Path) -> None:
    """⒞ 처분 값을 어휘 밖(`보류`)으로 바꾸면 G4 가 잡는다."""
    lessons, ledger = sandbox(tmp_path)

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if cells[3] != "수용":
            pytest.fail(f"변조 전제 불일치: 처분 셀 got={cells[3]!r} want='수용'")
        cells[3] = "보류"
        lines[index] = "| " + " | ".join(cells) + " |"
        return lines

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒞ 처분 값 변조")
    require_output_contains(proc, ("G4", "'보류'"), "⒞ 처분 값 변조")


def test_unregistered_lesson_file_is_rejected(tmp_path: Path) -> None:
    """⒟ §0 에 없는 `.md` 가 lessons-root 에 있으면 G1 이 잡는다."""
    lessons, ledger = sandbox(tmp_path)
    (lessons / "zz-injected.md").write_text("# 심은 파일\n", encoding="utf-8")
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒟ 미등재 파일")
    require_output_contains(proc, ("G1", "zz-injected.md", "행 없음"), "⒟ 미등재 파일")


def test_missing_enumeration_line_is_rejected(tmp_path: Path) -> None:
    """⒠ 등재 파일의 열거 줄을 지우면 G3 이 잡는다(0개)."""
    lessons, ledger = sandbox(tmp_path)
    target = lessons / TARGET_LESSON
    rewrite_lines(
        target,
        lambda lines: [
            line for index, line in enumerate(lines)
            if index != locate_once(lines, TARGET_ENUMERATION, target)
        ],
    )
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒠ 열거 줄 삭제")
    require_output_contains(proc, ("G3", TARGET_LESSON, "0개"), "⒠ 열거 줄 삭제")


def test_duplicate_enumeration_line_is_rejected(tmp_path: Path) -> None:
    """⒡ 열거 줄이 둘이면 G3 이 잡는다 — 어느 쪽이 정본인지 기계가 정하지 않는다."""
    lessons, ledger = sandbox(tmp_path)
    target = lessons / TARGET_LESSON

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ENUMERATION, target)
        return lines[: index + 1] + [lines[index]] + lines[index + 1 :]

    rewrite_lines(target, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "⒡ 열거 줄 두 개")
    require_output_contains(proc, ("G3", TARGET_LESSON, "2개"), "⒡ 열거 줄 두 개")


# ---------------------------------------------------------------------------
# 상태 어휘 · `선행 종결` 의 두 조건 (G2)


def test_unknown_status_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)
    prefix = f"| {TARGET_LESSON} | 등재 |"

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, prefix, ledger)
        lines[index] = lines[index].replace("| 등재 |", "| 보류 |", 1)
        return lines

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G2 상태 어휘")
    require_output_contains(proc, ("G2", "'보류'"), "G2 상태 어휘")


def test_closed_earlier_file_with_disposition_row_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)
    closed_prefix = "| 2026-08-18-sol-audit-m06-full.md | 선행 종결 |"
    injected = "| 2026-08-18-sol-audit-m06-full.md | Q-1 | — | 이연 | 심은 행 | 심은 포인터 |"

    def transform(lines: list[str]) -> list[str]:
        locate_once(lines, closed_prefix, ledger)
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        return lines[: index + 1] + [injected] + lines[index + 1 :]

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G2 선행 종결 · §1 행")
    require_output_contains(
        proc, ("G2", "2026-08-18-sol-audit-m06-full.md"), "G2 선행 종결 · §1 행"
    )


def test_closed_earlier_file_without_pointer_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)
    closed_prefix = "| 2026-08-18-sol-audit-m06-full.md | 선행 종결 |"

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, closed_prefix, ledger)
        lines[index] = f"{closed_prefix} — |"
        return lines

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G2 선행 종결 · 포인터")
    require_output_contains(proc, ("G2", "비어 있음"), "G2 선행 종결 · 포인터")


# ---------------------------------------------------------------------------
# 사유·포인터 · 중복 (G4)


def test_empty_reason_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        cells[4] = ""
        lines[index] = "| " + " | ".join(cells) + " |"
        return lines

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G4 빈 사유")
    require_output_contains(proc, ("G4", "사유 한 줄"), "G4 빈 사유")


def test_empty_pointer_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        cells[5] = "—"
        lines[index] = "| " + " | ".join(cells) + " |"
        return lines

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G4 빈 포인터")
    require_output_contains(proc, ("G4", "포인터"), "G4 빈 포인터")


def test_duplicate_file_id_pair_is_rejected(tmp_path: Path) -> None:
    lessons, ledger = sandbox(tmp_path)

    def transform(lines: list[str]) -> list[str]:
        index = locate_once(lines, TARGET_ROW_PREFIX, ledger)
        return lines[: index + 1] + [lines[index]] + lines[index + 1 :]

    rewrite_lines(ledger, transform)
    proc = run_tool(lessons, ledger)
    require_exit(proc, 1, "G4 중복 행")
    require_output_contains(proc, ("G4", "중복 행"), "G4 중복 행")


# ---------------------------------------------------------------------------
# 최적화 모드 동치 · 입력 오류


def test_rejection_is_identical_under_pythonoptimize(tmp_path: Path) -> None:
    """`-O` 에서도 같은 판정이어야 한다 — `assert` 로 검증하지 않았음의 실증."""
    lessons, ledger = sandbox(tmp_path)
    rewrite_lines(
        ledger,
        lambda lines: [
            line for index, line in enumerate(lines)
            if index != locate_once(lines, TARGET_ROW_PREFIX, ledger)
        ],
    )
    plain = run_tool(lessons, ledger)
    optimized = run_tool(lessons, ledger, optimized=True)
    require_exit(plain, 1, "plain rejection")
    require_exit(optimized, 1, "optimized rejection")
    if plain.stdout != optimized.stdout:
        pytest.fail(
            "OPTIMIZE MISMATCH: plain 과 -O 의 판정 출력이 다르다\n"
            f"plain:\n{plain.stdout}\n-O:\n{optimized.stdout}"
        )


def test_missing_dispositions_file_is_input_error(tmp_path: Path) -> None:
    lessons, _ledger = sandbox(tmp_path)
    proc = run_tool(lessons, tmp_path / "없는-파일.md")
    require_exit(proc, 2, "입력 오류")
    require_output_contains(proc, ("EXIT=2",), "입력 오류")
