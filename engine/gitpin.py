# -*- coding: utf-8 -*-
"""런 결박에 쓰는 git 판정의 **단일 진원** (재정 P-U1 · P-8).

런은 시작 시점의 git 커밋에 결박된다. 그 결박을 세우는 데 필요한 판정은 셋뿐이다 —
**작업 트리가 깨끗한가**(커밋되지 않은 변경은 커밋에 결박될 수 없다) · **HEAD 는 무엇인가** ·
**여기가 격리 체크아웃(worktree)인가**. 이 셋을 여기 한 곳에 둔다.

★ 한 곳인 이유. 소비자가 둘이다 — `tools/run_worktree.py`(worktree 를 만든다)와
`engine/stages/source.py`(`run.yaml#engine.commit` 을 기입한다). 같은 판정을 두 벌 적으면
한 벌은 반드시 낡고, 그날 도구와 러너가 서로 다른 기준으로 같은 런을 판정한다. 그래서
문언(`DIRTY_HEADLINE`·`DIRTY_REMEDY`)까지 여기서 나눠 쓴다.

이 모듈은 **판정만** 하고 처분하지 않는다. 종료 코드로 끝낼지(도구) 예외로 올릴지(러너)는
소비자가 정한다 — 그래서 여기에는 `sys.exit` 가 없고 예외 2종만 있다.

`assert` 를 쓰지 않는다(`python3 -O` 에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import os
import re
import subprocess

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# worktree 루트 기본값 — 리포 **안**이다(런 작업장이 리포와 함께 이동해야 핀의 의미가 산다).
DEFAULT_WORKTREE_ROOT = ".worktrees"

# 더러운 트리를 거부할 때의 문언. 도구와 러너가 같은 말을 하도록 여기 둔다.
DIRTY_HEADLINE = "작업 트리가 더럽다 — 커밋되지 않은 변경은 커밋에 결박될 수 없다 (재정 P-U1)"
DIRTY_REMEDY = "처분: 변경을 커밋하거나 되돌린 뒤 다시 개시한다. 우회 스위치는 없다."
MAX_DIRTY_LISTED = 20


class GitUnavailable(Exception):
    """git 이 없거나 그 경로가 git 작업 트리가 아니다 — 핀을 만들 수 없다.

    조용히 넘어갈 자리가 아니다. 핀이 없으면 "이 런의 법이 무엇이었는가"에 답할 수 없고,
    그 물음에 답하지 못하는 런은 재정 P-U1 이 금지한 런이다.
    """


class DirtyWorktree(Exception):
    """커밋되지 않은 변경이 있다. `entries` = `(상태, 경로)` 목록."""

    def __init__(self, entries: list[tuple[str, str]]) -> None:
        self.entries = entries
        super().__init__(f"{DIRTY_HEADLINE} · {len(entries)}건")


def run_git(cwd: str, args: list[str]) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise GitUnavailable(f"git 실행 파일을 찾을 수 없다: {exc}") from exc


def git_out(cwd: str, args: list[str], what: str) -> str:
    proc = run_git(cwd, args)
    if proc.returncode != 0:
        detail = " / ".join(line for line in proc.stderr.strip().splitlines() if line)
        raise GitUnavailable(f"{what} 실패 (git {' '.join(args)} · exit {proc.returncode}) {detail}".strip())
    return proc.stdout.strip()


def resolve_repo(raw: str) -> str:
    """git 작업 트리임을 확인하고 realpath 를 돌려준다."""
    repo = os.path.realpath(raw)
    if not os.path.isdir(repo):
        raise GitUnavailable(f"리포 경로가 디렉터리가 아니다: {raw}")
    proc = run_git(repo, ["rev-parse", "--git-common-dir"])
    if proc.returncode != 0:
        raise GitUnavailable(f"git 작업 트리가 아니다: {repo}")
    return repo


def git_common_dir(repo: str) -> str:
    raw = git_out(repo, ["rev-parse", "--git-common-dir"], "git 디렉터리 조회")
    return os.path.realpath(os.path.join(repo, raw))


def head_commit(repo: str) -> str:
    commit = git_out(repo, ["rev-parse", "HEAD"], "HEAD 조회")
    if not COMMIT_RE.match(commit):
        raise GitUnavailable(f"HEAD 가 40hex 커밋이 아니다: {commit!r}")
    return commit


def porcelain_entries(repo: str) -> list[tuple[str, str]]:
    """`git status --porcelain -z` 를 (상태, 경로) 목록으로 읽는다.

    `-z` 를 쓰는 이유는 경로 인용(따옴표·이스케이프) 해석을 피하기 위해서다. 이름 변경·복사
    항목(`R`·`C`)은 원본 경로가 **다음 레코드**로 따라오므로 함께 소비한다.
    """
    raw = run_git(repo, ["status", "--porcelain", "-z"])
    if raw.returncode != 0:
        detail = " / ".join(line for line in raw.stderr.strip().splitlines() if line)
        raise GitUnavailable(f"작업 트리 상태 조회 실패 (exit {raw.returncode}) {detail}".strip())
    records = [rec for rec in raw.stdout.split("\0") if rec]
    entries: list[tuple[str, str]] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if len(record) < 4:
            continue
        status, path = record[:2], record[3:]
        if status[0] in ("R", "C") and index < len(records):
            index += 1  # 원본 경로 레코드 소비
        entries.append((status, path))
    return entries


def dirty_entries(repo: str, exclude_rels=()) -> list[tuple[str, str]]:
    """더러운 항목 목록. `exclude_rels` 아래는 제외한다.

    제외를 두는 이유: **이 결박 기제 자신이 만든 생성물**은 소스가 아니다. worktree 루트
    (`.worktrees/`)를 더러움으로 세면 첫 런을 만든 순간 두 번째 런과 재개 런이 전부 막히고
    (자기 봉쇄), 런 작업장(`runs/<run-id>/`)을 세면 러너가 자기 산출물 때문에 자기 런을
    거부한다. 무시 규칙(`.gitignore`)을 두는 것은 리포 총괄의 처분이고, 이 판정은 그 처분의
    유무와 무관하게 같은 답을 내야 한다.
    """
    entries = porcelain_entries(repo)
    prefixes = [rel.rstrip("/") for rel in exclude_rels if rel]
    if not prefixes:
        return entries
    return [
        (status, path)
        for status, path in entries
        if not any(path == prefix or path.startswith(prefix + "/") for prefix in prefixes)
    ]


def format_dirty(entries: list[tuple[str, str]]) -> list[str]:
    """더러운 항목의 진단 줄 — 도구와 러너가 같은 형태로 싣는다."""
    listed = [f"{status} {path}" for status, path in entries[:MAX_DIRTY_LISTED]]
    if len(entries) > MAX_DIRTY_LISTED:
        listed.append(f"... 외 {len(entries) - MAX_DIRTY_LISTED}건")
    return listed


def relative_inside(repo: str, path: str) -> str | None:
    """`path` 가 리포 안이면 리포 상대 경로를, 밖이면 None 을 돌려준다."""
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(repo))
    if rel == os.pardir or rel.startswith(os.pardir + os.sep) or os.path.isabs(rel):
        return None
    return rel.replace(os.sep, "/")


def worktree_of(repo: str) -> str | None:
    """이 경로가 **링크된 worktree** 면 기록용 경로를, 주 작업 트리면 None 을 돌려준다.

    판별은 `--git-dir` ↔ `--git-common-dir` 의 차이다(링크된 worktree 는 자기 git 디렉터리가
    공용 디렉터리 아래의 `worktrees/<name>` 이다). 기록용 경로는 주 작업 트리 기준 상대경로를
    쓴다 — `run.yaml` 예시(`.worktrees/<run-id>`, SPEC §7.3)와 같은 형태를 만들기 위해서다.
    리포 밖에 만든 worktree 는 상대화할 자리가 없으므로 절대경로 그대로 적는다.
    """
    git_dir = os.path.realpath(
        os.path.join(repo, git_out(repo, ["rev-parse", "--git-dir"], "git 디렉터리 조회"))
    )
    common = git_common_dir(repo)
    if git_dir == common:
        return None
    main_root = os.path.dirname(common) if os.path.basename(common) == ".git" else None
    if main_root:
        rel = relative_inside(main_root, repo)
        if rel:
            return rel
    return os.path.realpath(repo)


def resolve_pin(repo: str, *, exclude_rels=()) -> tuple[str, str | None]:
    """런 결박 핀 — `(커밋 40hex, worktree 경로 또는 None)`.

    순서가 규율이다. ① git 작업 트리인가(아니면 핀을 만들 수 없다 — `GitUnavailable`)
    ② 작업 트리가 깨끗한가(아니면 `DirtyWorktree`) ③ 그제서야 HEAD 를 확정한다.
    더러운 트리에서 HEAD 를 먼저 읽으면 "무엇에 결박되었는가"가 거짓이 된 채로 값이 생긴다.
    """
    root = resolve_repo(repo)
    dirty = dirty_entries(root, exclude_rels)
    if dirty:
        raise DirtyWorktree(dirty)
    return head_commit(root), worktree_of(root)


__all__ = [
    "COMMIT_RE",
    "DEFAULT_WORKTREE_ROOT",
    "DIRTY_HEADLINE",
    "DIRTY_REMEDY",
    "DirtyWorktree",
    "GitUnavailable",
    "MAX_DIRTY_LISTED",
    "dirty_entries",
    "format_dirty",
    "git_common_dir",
    "git_out",
    "head_commit",
    "porcelain_entries",
    "relative_inside",
    "resolve_pin",
    "resolve_repo",
    "run_git",
    "worktree_of",
]
