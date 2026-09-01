# -*- coding: utf-8 -*-
"""`tools/check_lesson_authorship.py` 관문 회귀·거부 실증.

CLAUDE.md §3 관례에 따라 서브프로세스 종료 코드는 명시 비교하고, 불일치는
`pytest.fail()`로 기대·실제를 함께 보고한다. 정본 `docs/lessons`는 읽기만 하며 모든 변조는
`tmp_path` 사본에 심는다.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_lesson_authorship.py"
LESSONS = REPO_ROOT / "docs" / "lessons"
TARGET_NAME = "2026-09-01-fable-advice-g6-defect-ownership.md"
AUTHORED_HEADING = (
    "## ★ 총괄의 독립 확인 "
    "(2026-09-01 · 추기 — 이 절은 총괄 저작이며 자문 원문이 아니다)"
)


def run_tool(root: Path, *, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if optimized:
        env["PYTHONOPTIMIZE"] = "1"
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def output(proc: subprocess.CompletedProcess[str]) -> str:
    return f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"


def require_exit(proc: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    if proc.returncode != expected:
        pytest.fail(
            f"{label} EXIT MISMATCH: got={proc.returncode} want={expected}\n{output(proc)}"
        )


def lessons_copy(tmp_path: Path) -> Path:
    target = tmp_path / "lessons"
    shutil.copytree(LESSONS, target)
    return target


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        pytest.fail(f"변조 전제 불일치: {path.name}에서 {old!r} count={count}, want=1")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def require_output_contains(
    proc: subprocess.CompletedProcess[str], needles: tuple[str, ...], label: str
) -> None:
    combined = proc.stdout + proc.stderr
    missing = [needle for needle in needles if needle not in combined]
    if missing:
        pytest.fail(f"{label} OUTPUT MISMATCH: missing={missing!r}\n{output(proc)}")


def test_canonical_lessons_all_pass() -> None:
    proc = run_tool(LESSONS)
    require_exit(proc, 0, "canonical")


def test_missing_author_marker_is_rejected(tmp_path: Path) -> None:
    root = lessons_copy(tmp_path)
    target = root / TARGET_NAME
    mutated_heading = AUTHORED_HEADING.replace("총괄 저작", "총괄 기록")
    replace_once(target, AUTHORED_HEADING, mutated_heading)

    proc = run_tool(root)
    require_exit(proc, 1, "R2 rejection")
    require_output_contains(proc, ("R2", TARGET_NAME, mutated_heading), "R2 rejection")


def test_author_marker_without_appendix_token_is_rejected(tmp_path: Path) -> None:
    root = lessons_copy(tmp_path)
    target = root / TARGET_NAME
    mutated_heading = AUTHORED_HEADING.replace("추기 — ", "")
    replace_once(target, AUTHORED_HEADING, mutated_heading)

    proc = run_tool(root)
    require_exit(proc, 1, "R3 rejection")
    require_output_contains(proc, ("R3", TARGET_NAME, mutated_heading), "R3 rejection")


def test_missing_preservation_declaration_is_rejected(tmp_path: Path) -> None:
    root = lessons_copy(tmp_path)
    target = root / TARGET_NAME
    replace_once(target, "# 자문 원문 보존 —", "# 자문 기록 보전 —")

    proc = run_tool(root)
    require_exit(proc, 1, "R1 rejection")
    require_output_contains(proc, ("R1", TARGET_NAME), "R1 rejection")


def test_canonical_lessons_all_pass_with_pythonoptimize() -> None:
    proc = run_tool(LESSONS, optimized=True)
    require_exit(proc, 0, "optimized canonical")


def test_missing_author_marker_is_rejected_with_pythonoptimize(tmp_path: Path) -> None:
    root = lessons_copy(tmp_path)
    target = root / TARGET_NAME
    mutated_heading = AUTHORED_HEADING.replace("총괄 저작", "총괄 기록")
    replace_once(target, AUTHORED_HEADING, mutated_heading)

    proc = run_tool(root, optimized=True)
    require_exit(proc, 1, "optimized R2 rejection")
    require_output_contains(
        proc,
        ("R2", TARGET_NAME, mutated_heading),
        "optimized R2 rejection",
    )
