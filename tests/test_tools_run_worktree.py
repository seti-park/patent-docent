# -*- coding: utf-8 -*-
"""`tools/run_worktree.py` 회귀 테스트 (재정 P-U1 · P-8).

임시 git 리포를 그 자리에서 만들어 도구를 **서브프로세스로** 돌린다. 도구가 하는 일이
git 상태에 대한 판정이므로, 함수 호출로는 그 판정을 시험할 수 없다.

규약(CLAUDE.md §3): 테스트 모듈의 맨 `assert` 는 pytest 가 AST 를 재작성하므로 `-O` 에서도
살아남는다. 다만 **서브프로세스의 종료 코드는 명시 비교 + `pytest.fail()`** 로 본다 —
종료 코드는 이 도구의 계약면이고, 계약면은 재작성에 기대지 않는다.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "run_worktree.py"

# 사용자 전역 설정·서명 훅과 격리한다(판정이 환경에 따라 달라지면 안 된다).
GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "docent-test",
    "GIT_AUTHOR_EMAIL": "docent@example.invalid",
    "GIT_COMMITTER_NAME": "docent-test",
    "GIT_COMMITTER_EMAIL": "docent@example.invalid",
}


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        env=GIT_ENV,
    )
    if proc.returncode != 0:
        pytest.fail(f"git {' '.join(args)} 실패 (exit {proc.returncode}): {proc.stderr}")
    return proc.stdout.strip()


def run_tool(args: list[str], *, optimized: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable]
    if optimized:
        cmd.append("-O")
    cmd += [str(TOOL), *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=GIT_ENV)


def expect_exit(proc: subprocess.CompletedProcess, expected: int, what: str) -> None:
    """종료 코드 명시 비교 — `assert` 에 기대지 않는다."""
    if proc.returncode != expected:
        pytest.fail(
            f"{what}: 종료 코드 기대 {expected} · 실측 {proc.returncode}\n"
            f"stdout={proc.stdout}\nstderr={proc.stderr}"
        )


def payload(proc: subprocess.CompletedProcess) -> dict:
    try:
        return json.loads(proc.stdout.strip())
    except json.JSONDecodeError as exc:
        pytest.fail(f"stdout 이 JSON 한 줄이 아니다: {exc}\nstdout={proc.stdout!r}")
        raise  # 도달하지 않는다


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """법 경로(contracts/·docs/)와 비법 경로(runs/)를 갖춘 최소 리포."""
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-b", "main")
    write(root / "contracts" / "stages" / "read.yaml", "line: read/v0\n")
    write(root / "docs" / "SPEC.md", "# spec v0\n")
    write(root / "runs" / "note.txt", "run artifact\n")
    git(root, "add", "contracts/stages/read.yaml", "docs/SPEC.md", "runs/note.txt")
    git(root, "commit", "-m", "init")
    return root


def write_run_yaml(base: Path, commit: str, run_id: str = "r1") -> Path:
    path = base / "runs" / run_id / "run.yaml"
    write(
        path,
        "schema: run/v0\n"
        "run_id: r1\n"
        "engine:\n"
        f"  commit: '{commit}'\n"
        "  gate_version: '1.2'\n",
    )
    return path


# --- create ---------------------------------------------------------------


def test_create_refuses_dirty_worktree(repo: Path) -> None:
    """커밋되지 않은 변경은 커밋에 결박될 수 없다 — 거부하지 않으면 핀이 거짓말이 된다."""
    write(repo / "contracts" / "stages" / "read.yaml", "line: read/v0\nmutated: true\n")
    write(repo / "untracked.md", "미추적 파일\n")

    proc = run_tool(["create", "run-dirty", "--repo", str(repo)])

    expect_exit(proc, 2, "더러운 트리에서의 create")
    assert "untracked.md" in proc.stderr
    assert "contracts/stages/read.yaml" in proc.stderr
    assert proc.stdout.strip() == ""
    assert not (repo / ".worktrees").exists()


def test_create_pins_head_commit_and_makes_worktree(repo: Path) -> None:
    """worktree 가 실재하고 그 HEAD 가 핀 커밋과 같아야 한다."""
    head = git(repo, "rev-parse", "HEAD")

    proc = run_tool(["create", "run-1", "--repo", str(repo)])

    expect_exit(proc, 0, "정상 create")
    data = payload(proc)
    assert data["run_id"] == "run-1"
    assert data["commit"] == head
    assert data["created"] is True
    assert data["reused"] is False

    worktree = Path(data["worktree"])
    assert worktree == Path(os.path.realpath(repo)) / ".worktrees" / "run-1"
    assert worktree.is_dir()
    assert git(worktree, "rev-parse", "HEAD") == head
    # 체크아웃 내용이 핀 커밋의 법이다.
    assert (worktree / "contracts" / "stages" / "read.yaml").read_text(encoding="utf-8") == "line: read/v0\n"


def test_create_is_idempotent_for_same_commit(repo: Path) -> None:
    """재개 런은 같은 커밋을 쓴다 — 기존 worktree 를 덮어쓰지 않고 재사용한다."""
    first = run_tool(["create", "run-1", "--repo", str(repo)])
    expect_exit(first, 0, "첫 create")
    marker = Path(payload(first)["worktree"]) / "resume-marker.txt"
    marker.write_text("재개 흔적\n", encoding="utf-8")

    second = run_tool(["create", "run-1", "--repo", str(repo)])

    expect_exit(second, 0, "재개 create")
    data = payload(second)
    assert data["commit"] == payload(first)["commit"]
    assert data["worktree"] == payload(first)["worktree"]
    assert data["created"] is False
    assert data["reused"] is True
    assert marker.exists(), "재사용은 기존 체크아웃을 지우지 않는다"


def test_create_rejects_existing_worktree_at_other_commit(repo: Path) -> None:
    """같은 경로가 다른 커밋에 결박돼 있으면 그것은 재개가 아니라 새 런이다."""
    first = run_tool(["create", "run-1", "--repo", str(repo)])
    expect_exit(first, 0, "첫 create")
    pinned = payload(first)["commit"]

    write(repo / "docs" / "SPEC.md", "# spec v0.5\n")
    git(repo, "add", "docs/SPEC.md")
    git(repo, "commit", "-m", "개정")

    proc = run_tool(["create", "run-1", "--repo", str(repo)])

    expect_exit(proc, 2, "커밋이 어긋난 경로에서의 create")
    assert pinned in proc.stderr
    assert proc.stdout.strip() == ""


# --- expiry ---------------------------------------------------------------


def test_expiry_exits_zero_when_unchanged(repo: Path) -> None:
    head = git(repo, "rev-parse", "HEAD")
    run_yaml = write_run_yaml(repo, head)

    proc = run_tool(["expiry", str(run_yaml), "--repo", str(repo)])

    expect_exit(proc, 0, "개정 없는 expiry")
    data = payload(proc)
    assert data["pinned"] == head
    assert data["head"] == head
    assert data["expired"] is False
    assert data["commits_since"] == 0
    assert data["changed_paths"] == []


def test_expiry_exits_three_after_law_change(repo: Path) -> None:
    """개정이 있었으면 만료 통지(exit 3) + 법 경로만 목록에 오른다."""
    pinned = git(repo, "rev-parse", "HEAD")
    run_yaml = write_run_yaml(repo, pinned)

    write(repo / "contracts" / "stages" / "read.yaml", "line: read/v0\nphase_gates: []\n")
    write(repo / "runs" / "note.txt", "run artifact 2\n")
    git(repo, "add", "contracts/stages/read.yaml", "runs/note.txt")
    git(repo, "commit", "-m", "P-U3 반영")

    proc = run_tool(["expiry", str(run_yaml), "--repo", str(repo)])

    expect_exit(proc, 3, "개정 이후 expiry")
    data = payload(proc)
    assert data["pinned"] == pinned
    assert data["head"] == git(repo, "rev-parse", "HEAD")
    assert data["expired"] is True
    assert data["commits_since"] == 1
    # 법 경로만 — 런 산출물(`runs/`)의 변경은 법의 개정이 아니다.
    assert data["changed_paths"] == ["contracts/stages/read.yaml"]


def test_expiry_rejects_missing_input(repo: Path, tmp_path: Path) -> None:
    """파일 부재·필드 부재·핀 미존재는 전부 입력 오류(exit 2)이지 만료가 아니다."""
    missing = run_tool(["expiry", str(repo / "runs" / "none" / "run.yaml"), "--repo", str(repo)])
    expect_exit(missing, 2, "run.yaml 부재")

    empty_pin = write_run_yaml(repo, "")
    expect_exit(run_tool(["expiry", str(empty_pin), "--repo", str(repo)]), 2, "engine.commit 공란")

    no_engine = tmp_path / "no-engine.yaml"
    write(no_engine, "schema: run/v0\nrun_id: r2\n")
    expect_exit(run_tool(["expiry", str(no_engine), "--repo", str(repo)]), 2, "engine 블록 부재")

    ghost = write_run_yaml(repo, "0" * 40)
    expect_exit(run_tool(["expiry", str(ghost), "--repo", str(repo)]), 2, "리포에 없는 핀 커밋")


# --- -O 동등성 -------------------------------------------------------------


def test_tool_behaves_identically_under_O(repo: Path, tmp_path: Path) -> None:
    """`python3 -O` 에서 stdout·종료 코드가 동일해야 한다.

    도구가 `assert` 로 판정하고 있었다면 `-O` 에서 그 판정이 통째로 사라져 결과가 갈린다.

    run.yaml 을 리포 **밖**에 두는 이유: 이 테스트는 뒤에서 `create` 도 부르는데, 리포 안에
    미추적 파일을 남기면 그 create 가 (정당하게) 더러움으로 거부되어 시험 대상이 바뀐다.
    """
    pinned = git(repo, "rev-parse", "HEAD")
    run_yaml = write_run_yaml(tmp_path / "outside", pinned)
    write(repo / "docs" / "SPEC.md", "# spec v0.5\n")
    git(repo, "add", "docs/SPEC.md")
    git(repo, "commit", "-m", "개정")

    # ① expiry (만료 통지 경로)
    plain = run_tool(["expiry", str(run_yaml), "--repo", str(repo)])
    optimized = run_tool(["expiry", str(run_yaml), "--repo", str(repo)], optimized=True)
    expect_exit(plain, 3, "expiry(일반)")
    expect_exit(optimized, 3, "expiry(-O)")
    assert plain.stdout == optimized.stdout

    # ② create (신규 → 재사용 경로. 두 재사용 호출의 출력이 완전히 같아야 한다)
    expect_exit(run_tool(["create", "run-1", "--repo", str(repo)]), 0, "create(신규)")
    reuse_plain = run_tool(["create", "run-1", "--repo", str(repo)])
    reuse_opt = run_tool(["create", "run-1", "--repo", str(repo)], optimized=True)
    expect_exit(reuse_plain, 0, "create 재사용(일반)")
    expect_exit(reuse_opt, 0, "create 재사용(-O)")
    assert reuse_plain.stdout == reuse_opt.stdout

    # ③ 거부 경로도 동일하게 거부해야 한다(공허 통과 봉쇄).
    write(repo / "untracked.md", "미추적\n")
    dirty_plain = run_tool(["create", "run-2", "--repo", str(repo)])
    dirty_opt = run_tool(["create", "run-2", "--repo", str(repo)], optimized=True)
    expect_exit(dirty_plain, 2, "더러운 트리 거부(일반)")
    expect_exit(dirty_opt, 2, "더러운 트리 거부(-O)")
    assert dirty_plain.stdout == dirty_opt.stdout == ""
