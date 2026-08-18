#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""런 커밋 핀 도구 — 런을 **시작 시점의 git 커밋에 결박**한다 (재정 P-U1 · P-8).

런이 도는 동안 리포가 개정되면 "무엇이 당시 법이었는가"를 되짚을 수 없다. M1 내내 반복된
그 사고 형태를 이 도구가 통째로 없앤다 — 런의 법은 언제나 `run.yaml` 의 커밋 **하나**이고,
계약·스키마·검증기·러너가 그 커밋에서 **함께** 고정된다("법/구현 경계 문제의 소멸").
구현 수단은 git worktree, 즉 그 커밋의 **격리 체크아웃**이다(재정 P-8).

  `create <run-id>`   현재 HEAD 를 40hex 로 확정 → `<root>/<run-id>` 에 worktree 체크아웃
  `expiry <run.yaml>` `engine.commit` 과 현재 HEAD 를 대조 → **만료 통지**

**예외가 없는 이유.** 재정 원문은 "런 중 리포 개정은 다음 런부터(행위시법). **예외 없음**"이라고
적는다. 진행 중인 런에 리포 개정을 밀어 넣는 통로를 하나라도 두면, 그 런의 산출물이 어떤 법
아래에서 만들어졌는지가 다시 미정이 되고 결박은 이름만 남는다. 긴급 수정이 필요하면 경로는
**Owner 명시 재시작** 하나뿐이다 — 고쳐서 이어 도는 것이 아니라, 고친 커밋 위에서 새 런을 연다.
그래서 이 도구에는 `--fix`·`--sync` 류의 우회 스위치가 없고, 앞으로도 두지 않는다.

**소급 재검 가능성.** 커밋 핀은 사후 재현의 좌표다. `run.yaml#engine.commit` 이 남아 있는 한
같은 커밋으로 worktree 를 다시 만들어(=이 도구의 `create` 를 그 커밋 위에서 다시 호출) 당시의
계약·검증기로 산출물을 **재실행·재검**할 수 있다. 만료 통지(개정이 있었다는 사실)는 그 재검을
막지 않는다 — 무엇이 달라졌는지(`changed_paths`)를 함께 내는 이유가 그것이다.
**재개 런은 같은 커밋을 쓴다** — 그래서 `create` 는 같은 커밋에 대해 멱등이다(기존 worktree 재사용).

**이 도구는 `run.yaml` 을 쓰지 않는다.** 커밋을 확정해 stdout 으로 낼 뿐이고, `engine.commit` ·
`engine.worktree` 의 기입은 **러너의 몫**이다(`engine/stages/source.py#run` — 진입 시점에
스스로 기입한다). 기록 주체를 둘로 늘리면 "누가 쓴 값인가"가 다시 미정이 되고, 도구가 런
상태를 건드리는 순간 read-only 도구 계열의 규율도 함께 깨진다.
(worktree 생성 자체는 이 도구의 유일한 쓰기다 — 그 쓰기 대상은 런 산출물이 아니라 체크아웃이다.)

**★ git 판정은 이 파일이 소유하지 않는다.** 깨끗함·HEAD·worktree 여부의 판정은
`engine/gitpin.py` 한 곳에 있고 이 도구와 러너가 그것을 함께 부른다(문언까지 공유한다).
두 벌로 적으면 한 벌이 낡고, 그날 도구와 러너가 같은 런을 서로 다른 기준으로 판정한다.
이 도구가 소유하는 것은 그 판정의 **처분**(종료 코드 0/2/3)과 worktree 배치뿐이다.

종료 코드 (SPEC §8.3 관례):
  0 = 정상 (create 성공 / expiry: 핀 == HEAD, 만료 없음)
  2 = 입력·환경 오류 (더러운 작업 트리 · 파일 부재 · 필드 부재 · 커밋 미존재 · 경로 충돌)
  3 = `expiry` 전용 — **개정이 있었다**(만료 통지). 실패가 아니라 통지다.

`assert` 를 쓰지 않는다(`python3 -O` 에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from engine import gitpin  # noqa: E402  (경로 삽입 후에만 import 할 수 있다)

EXIT_OK = 0
EXIT_INPUT = 2
EXIT_EXPIRED = 3

# worktree 루트 기본값 — 리포 **안**이다. 런 작업장이 리포와 함께 이동해야 핀의 의미가 산다.
# (`.worktrees/` 를 git 무시 목록에 넣는 일은 이 도구의 관할이 아니다 — 아래 dirty 검사 주석 참조.)
DEFAULT_ROOT_REL = gitpin.DEFAULT_WORKTREE_ROOT

COMMIT_RE = gitpin.COMMIT_RE
# 런 ID 는 경로 성분 하나다. 경로 조작·상위 탈출을 원천 차단한다.
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# **법에 해당하는 경로** — 이 접두 아래의 변경만 만료 통지의 `changed_paths` 에 오른다.
# 런의 산출물(`runs/`)이나 원장(`ledgers/`)이 바뀐 것은 법의 개정이 아니다.
LAW_PATH_PREFIXES: tuple[str, ...] = (
    "contracts/",
    "reader/",
    "docs/CHARTER.md",
    "docs/SPEC.md",
    "engine/",
    "tools/",
)
MAX_CHANGED_PATHS = 50

EPILOG = """\
하는 일:
  create <run-id>       현재 HEAD 커밋을 확정하고 <root>/<run-id> 에 격리 체크아웃을 만든다.
                        작업 트리가 더러우면 거부한다 — 커밋되지 않은 변경은 커밋에 결박될 수 없다.
                        같은 경로가 같은 커밋에 이미 있으면 그것을 재사용한다(재개 런).
  expiry <run.yaml>     run.yaml#engine.commit 과 현재 HEAD 를 대조해 만료 여부를 낸다.

★ 이 도구가 하지 않는 것:
  - run.yaml 을 쓰지 않는다(engine.commit·engine.worktree 기입은 러너의 몫).
  - 우회 스위치(--fix·--sync 류)를 제공하지 않는다. 런 중 개정의 유일한 처분은
    Owner 명시 재시작이다(재정 P-U1 — 예외 없음).

종료 코드: 0 정상 · 2 입력/환경 오류 · 3 만료(개정 있었음, expiry 전용)
"""


def fail_env(message: str, detail: list[str] | None = None) -> None:
    """입력·환경 오류로 즉시 중단한다(exit 2). 진단은 stderr 로만 낸다."""
    print(f"ENVIRONMENT ERROR: {message}", file=sys.stderr)
    for line in detail or []:
        print(f"  {line}", file=sys.stderr)
    sys.exit(EXIT_INPUT)


def guarded(call, *args, **kwargs):
    """`engine/gitpin.py` 의 판정을 부르고, 판정 불능(`GitUnavailable`)을 exit 2 로 처분한다.

    판정은 저쪽이 하고 처분은 이쪽이 한다 — 그 경계가 이 함수 하나다.
    """
    try:
        return call(*args, **kwargs)
    except gitpin.GitUnavailable as exc:
        fail_env(str(exc))
        raise  # 도달하지 않는다(fail_env 가 종료한다) — 타입 흐름용


def run_git(cwd: str, args: list[str]) -> subprocess.CompletedProcess:
    return guarded(gitpin.run_git, cwd, args)


def git_out(cwd: str, args: list[str], what: str) -> str:
    return guarded(gitpin.git_out, cwd, args, what)


def resolve_repo(raw: str) -> str:
    return guarded(gitpin.resolve_repo, raw)


def git_common_dir(repo: str) -> str:
    return guarded(gitpin.git_common_dir, repo)


def head_commit(repo: str) -> str:
    return guarded(gitpin.head_commit, repo)


def relative_inside(repo: str, path: str) -> str | None:
    return gitpin.relative_inside(repo, path)


def emit(payload: dict) -> None:
    """stdout 은 기계 판독 JSON **한 줄**만 낸다(진단은 전부 stderr)."""
    print(json.dumps(payload, ensure_ascii=False))


# --- create ---------------------------------------------------------------


def cmd_create(args: argparse.Namespace) -> int:
    run_id = args.run_id
    if not RUN_ID_RE.match(run_id):
        fail_env(
            f"런 ID 형식 오류: {run_id!r}",
            ["런 ID 는 경로 성분 하나여야 한다 — 허용 문자 [A-Za-z0-9._-], 선두는 영숫자."],
        )

    repo = resolve_repo(args.repo)
    root = os.path.realpath(args.root) if args.root else os.path.join(repo, DEFAULT_ROOT_REL)
    root_rel = relative_inside(repo, root)

    # ①② 더러운 작업 트리 거부 후 커밋 확정 — 판정은 `engine/gitpin.py#resolve_pin` 하나다.
    #    러너(`source`)가 부르는 것과 **같은 함수**이며, 그래서 도구가 만든 worktree 와 러너가
    #    기입하는 핀이 어긋날 자리가 없다(재정 P-U1).
    try:
        commit, _worktree = guarded(gitpin.resolve_pin, repo, exclude_rels=[root_rel])
    except gitpin.DirtyWorktree as dirty:
        fail_env(
            f"{gitpin.DIRTY_HEADLINE} · {len(dirty.entries)}건",
            gitpin.format_dirty(dirty.entries) + [gitpin.DIRTY_REMEDY],
        )
        raise  # 도달하지 않는다 — 타입 흐름용
    target = os.path.join(root, run_id)

    # ③ 이미 있는 경로는 **덮어쓰지 않는다** — 같은 커밋이면 재사용(재개 런), 다르면 거부.
    if os.path.exists(target):
        if not os.path.isdir(target):
            fail_env(f"worktree 경로 자리에 디렉터리가 아닌 것이 있다: {target}")
        probe = run_git(target, ["rev-parse", "HEAD"])
        if probe.returncode != 0:
            fail_env(
                f"기존 경로가 git worktree 가 아니다: {target}",
                ["덮어쓰지 않는다 — 경로를 비우거나 다른 --root 를 쓴다."],
            )
        existing = probe.stdout.strip()
        existing_common = git_common_dir(target)
        if existing_common != git_common_dir(repo):
            fail_env(
                f"기존 경로가 다른 리포의 작업 트리다: {target}",
                [f"기대 git 디렉터리 {git_common_dir(repo)} · 실측 {existing_common}"],
            )
        if existing != commit:
            fail_env(
                f"기존 worktree 가 다른 커밋에 결박되어 있다: {target}",
                [
                    f"기존 {existing}",
                    f"HEAD {commit}",
                    "재개 런은 같은 커밋을 쓴다(재정 P-U1) — 커밋이 달라졌으면 그것은 새 런이다.",
                ],
            )
        emit(
            {
                "run_id": run_id,
                "commit": commit,
                "worktree": target,
                "created": False,
                "reused": True,
            }
        )
        return EXIT_OK

    # ④ 신규 체크아웃.
    try:
        os.makedirs(root, exist_ok=True)
    except OSError as exc:
        fail_env(f"worktree 루트 생성 실패: {root}: {exc}")
    add = run_git(repo, ["worktree", "add", "--detach", target, commit])
    if add.returncode != 0:
        fail_env(
            f"worktree 생성 실패: {target} @ {commit} (exit {add.returncode})",
            [line for line in add.stderr.strip().splitlines() if line],
        )
    emit(
        {
            "run_id": run_id,
            "commit": commit,
            "worktree": target,
            "created": True,
            "reused": False,
        }
    )
    return EXIT_OK


# --- expiry ---------------------------------------------------------------


def load_pinned_commit(run_yaml: str) -> str:
    if not os.path.isfile(run_yaml):
        fail_env(f"run.yaml 부재: {run_yaml}")
    try:
        import yaml  # 지연 임포트 — `--help` 는 PyYAML 없이도 떠야 한다.
    except ImportError as exc:  # pragma: no cover - 환경 오류 경로
        fail_env(f"PyYAML 로드 실패: {exc}")
    try:
        with open(run_yaml, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except OSError as exc:
        fail_env(f"run.yaml 읽기 실패: {run_yaml}: {exc}")
    except yaml.YAMLError as exc:
        fail_env(f"run.yaml 파싱 실패: {run_yaml}: {exc}")
    if not isinstance(data, dict):
        fail_env(f"run.yaml 형식 오류(맵 아님): {run_yaml}")
    engine = data.get("engine")
    if not isinstance(engine, dict):
        fail_env(f"run.yaml 에 engine 블록이 없다(맵 필요): {run_yaml}")
    commit = engine.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit):
        fail_env(
            f"engine.commit 이 40hex 커밋이 아니다: {commit!r} ({run_yaml})",
            ["런은 시작 시점 커밋에 결박된다(재정 P-U1) — 핀이 없는 런은 만료를 판정할 수 없다."],
        )
    return commit


def law_paths(repo: str, pinned: str, head: str) -> list[str]:
    """핀→HEAD 사이에서 **법에 해당하는 경로**의 변경 목록.

    `--no-renames` 를 쓰는 이유: 이름 변경을 하나로 접으면 법 경로 **밖으로 나간** 파일이
    목록에서 사라진다. 만료 통지는 무엇이 움직였는지를 있는 그대로 보여야 한다.
    """
    raw = git_out(
        repo,
        ["diff", "--name-only", "--no-renames", f"{pinned}..{head}"],
        "변경 경로 조회",
    )
    changed = [line for line in raw.splitlines() if line]
    hits = [path for path in changed if path.startswith(LAW_PATH_PREFIXES)]
    if len(hits) > MAX_CHANGED_PATHS:
        print(
            f"NOTE: 법 경로 변경 {len(hits)}건 중 {MAX_CHANGED_PATHS}건만 표기한다.",
            file=sys.stderr,
        )
        hits = hits[:MAX_CHANGED_PATHS]
    return hits


def cmd_expiry(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    pinned = load_pinned_commit(os.path.realpath(args.run_yaml))

    exists = run_git(repo, ["cat-file", "-e", f"{pinned}^{{commit}}"])
    if exists.returncode != 0:
        fail_env(
            f"핀 커밋이 이 리포에 없다: {pinned}",
            [f"리포 {repo}", "다른 리포의 핀이거나 커밋이 사라졌다 — 만료를 판정할 수 없다."],
        )

    head = head_commit(repo)
    expired = pinned != head
    if expired:
        commits_since = int(git_out(repo, ["rev-list", "--count", f"{pinned}..{head}"], "커밋 수 조회"))
        changed = law_paths(repo, pinned, head)
    else:
        commits_since = 0
        changed = []

    emit(
        {
            "pinned": pinned,
            "head": head,
            "expired": expired,
            "commits_since": commits_since,
            "changed_paths": changed,
        }
    )
    if expired:
        # 실패가 아니라 **통지**다 — 완주 보고에 개정 사실을 명기하라는 신호(재정 P-U1).
        print(
            f"NOTICE: 런 개시 이후 리포가 개정되었다 — 핀 {pinned[:12]} → HEAD {head[:12]} "
            f"(커밋 {commits_since}건 · 법 경로 변경 {len(changed)}건). "
            "산출물은 핀 커밋의 법 아래에서 만들어졌다(행위시법).",
            file=sys.stderr,
        )
        return EXIT_EXPIRED
    return EXIT_OK


# --- entry ----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_repo = os.path.dirname(script_dir)

    parser = argparse.ArgumentParser(
        prog="run_worktree.py",
        description="런 커밋 핀 도구 — 런을 시작 시점의 git 커밋에 결박한다 (재정 P-U1 · P-8).",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser(
        "create",
        help="현재 HEAD 커밋에 결박된 worktree 를 만든다",
        description="현재 HEAD 커밋을 확정하고 <root>/<run-id> 에 격리 체크아웃을 만든다.",
    )
    create.add_argument("run_id", metavar="run-id", help="런 ID (경로 성분 하나)")
    create.add_argument(
        "--root",
        default=None,
        help=f"worktree 루트 (기본: <repo>/{DEFAULT_ROOT_REL})",
    )
    create.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    create.set_defaults(handler=cmd_create)

    expiry = sub.add_parser(
        "expiry",
        help="핀 커밋과 현재 HEAD 를 대조해 만료를 통지한다",
        description="run.yaml#engine.commit 과 현재 HEAD 를 대조한다. 종료 코드 0=동일 · 3=개정 있었음 · 2=입력 오류.",
    )
    expiry.add_argument("run_yaml", metavar="run-yaml-path", help="런의 run.yaml 경로")
    expiry.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    expiry.set_defaults(handler=cmd_expiry)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
