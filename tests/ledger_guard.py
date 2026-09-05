# -*- coding: utf-8 -*-
"""시험 스위트의 생산 섀도 원장 보호 관문과 동적 결속 헬퍼."""

from __future__ import annotations

import ast
import contextlib
import glob
import hashlib
import os
import subprocess
from collections.abc import Iterable, Iterator

import pytest

from engine import paths as engine_paths
from engine.stages import read as read_stage


REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def _ledger_fingerprint(path: str):
    """원장 파일의 상태 지문 — 미존재는 `None`, 존재하면 (바이트 수, sha256)."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as handle:
        blob = handle.read()
    return len(blob), hashlib.sha256(blob).hexdigest()


def _main_worktree_by_git(tree: str) -> str:
    """`tree` 가 속한 주 작업 트리를 git 에 직접 물어 구한다."""
    try:
        proc = subprocess.run(
            ["git", "-C", tree, "rev-parse", "--path-format=absolute", "--git-common-dir"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return os.path.realpath(tree)
    if proc.returncode != 0:
        return os.path.realpath(tree)
    common = proc.stdout.strip()
    if os.path.basename(common) != ".git":
        return os.path.realpath(tree)
    return os.path.realpath(os.path.dirname(common))


def production_ledger() -> str:
    """현재 정본 주 작업 트리의 생산 섀도 원장 경로."""
    return os.path.join(
        _main_worktree_by_git(REPO), "ledgers", "shadow", "screening.jsonl"
    )


def _inside(root: str, path: str) -> bool:
    try:
        return os.path.commonpath((root, path)) == root
    except ValueError:
        return False


def _same_existing_path(left: str, right: str) -> bool:
    return os.path.exists(left) and os.path.exists(right) and os.path.samefile(left, right)


@contextlib.contextmanager
def production_ledger_untouched(tmp_path, *trees: str) -> Iterator[None]:
    """임시 트리와 암묵 원장 해석을 결속하고 생산 원장의 전후 지문을 지킨다.

    세 시험에 흩어졌던 보호를 한 블록으로 모아 정적 관문이 그 존재를 볼 수 있게 한다.
    지문 비교가 보증하는 것은 전후 바이트 변경 탐지뿐이며, 쓰기 전 차단은 진입 시 원장
    실경로 검사와 해석 감싸기가 맡는다. 검사와 I/O 사이의 파일시스템 교체, 헬퍼 밖에서
    미리 잡은 핸들, 블록 안 `os.replace`/직접 `open` 같은 엔진 밖 기입은 보지 않는다.
    """
    if not trees:
        pytest.fail("보호할 트리가 하나 이상 필요하다")
    tmp_real = os.path.realpath(os.fspath(tmp_path))
    tree_reals = [os.path.realpath(os.fspath(tree)) for tree in trees]
    for tree_real in tree_reals:
        if not _inside(tmp_real, tree_real):
            pytest.fail(f"트리가 tmp_path 밖에 있다: {tree_real}")

    mains = [_main_worktree_by_git(tree_real) for tree_real in tree_reals]
    for main in mains:
        if not _inside(tmp_real, main):
            pytest.fail(f"주 트리가 tmp_path 밖에 있다: {main}")

    production = os.path.realpath(engine_paths.shadow_screening_ledger())
    if _inside(tmp_real, production):
        pytest.fail(f"생산 자리가 tmp_path 안에 있다: {production}")

    expected_set: set[str] = set()
    for main in mains:
        expected = os.path.realpath(
            os.path.join(main, "ledgers", "shadow", "screening.jsonl")
        )
        if (
            not _inside(tmp_real, expected)
            or expected == production
            or _same_existing_path(expected, production)
        ):
            pytest.fail(f"원장 실경로가 안전하지 않다: {expected}")
        expected_set.add(expected)

    before = _ledger_fingerprint(production)
    original = read_stage.shadow_screening_ledger

    def bound(repo=None, shadow_root=None):
        path = original(repo, shadow_root)
        real = os.path.realpath(path)
        if (
            not _inside(tmp_real, real)
            or real == production
            or _same_existing_path(real, production)
        ):
            pytest.fail(f"생산 원장 해석을 거부한다: {real}")
        if shadow_root is None and real not in expected_set:
            pytest.fail(f"원장 대상 결속이 어긋났다: {real}")
        return path

    read_stage.shadow_screening_ledger = bound
    try:
        yield
    finally:
        read_stage.shadow_screening_ledger = original
        after = _ledger_fingerprint(production)
        if after != before:
            pytest.fail(f"생산 섀도 원장이 변했다: {before} → {after} ({production})")


_ALLOWED_PARENT_FIELDS: set[tuple[type[ast.AST], str]] = {
    (ast.Expr, "value"),
    (ast.Assign, "value"),
    (ast.AugAssign, "value"),
    (ast.AnnAssign, "value"),
    (ast.Return, "value"),
    (ast.Raise, "exc"),
    (ast.Raise, "cause"),
    (ast.Assert, "test"),
    (ast.Assert, "msg"),
    (ast.If, "test"),
    (ast.If, "body"),
    (ast.If, "orelse"),
    (ast.For, "iter"),
    (ast.For, "body"),
    (ast.For, "orelse"),
    (ast.While, "test"),
    (ast.While, "body"),
    (ast.While, "orelse"),
    (ast.Try, "body"),
    (ast.Try, "handlers"),
    (ast.Try, "orelse"),
    (ast.Try, "finalbody"),
    (ast.ExceptHandler, "body"),
    (ast.Match, "subject"),
    (ast.match_case, "body"),
    (ast.With, "body"),
    (ast.With, "items"),
    (ast.AsyncWith, "body"),
    (ast.AsyncWith, "items"),
    (ast.withitem, "context_expr"),
    (ast.Call, "args"),
    (ast.Call, "keywords"),
    (ast.keyword, "value"),
    (ast.Starred, "value"),
    (ast.Attribute, "value"),
    (ast.Subscript, "value"),
    (ast.Subscript, "slice"),
    (ast.Tuple, "elts"),
    (ast.List, "elts"),
    (ast.Set, "elts"),
    (ast.Dict, "keys"),
    (ast.Dict, "values"),
    (ast.BinOp, "left"),
    (ast.BinOp, "right"),
    (ast.UnaryOp, "operand"),
    (ast.BoolOp, "values"),
    (ast.Compare, "left"),
    (ast.Compare, "comparators"),
    (ast.IfExp, "test"),
    (ast.IfExp, "body"),
    (ast.IfExp, "orelse"),
    (ast.NamedExpr, "value"),
    (ast.Await, "value"),
    (ast.FormattedValue, "value"),
    (ast.JoinedStr, "values"),
}
if hasattr(ast, "TryStar"):
    for _field in ("body", "handlers", "orelse", "finalbody"):
        _ALLOWED_PARENT_FIELDS.add((ast.TryStar, _field))


def _parent_fields(tree: ast.AST) -> dict[ast.AST, tuple[ast.AST, str]]:
    parents: dict[ast.AST, tuple[ast.AST, str]] = {}
    for parent in ast.walk(tree):
        for field, value in ast.iter_fields(parent):
            children = value if isinstance(value, list) else (value,)
            for child in children:
                if isinstance(child, ast.AST):
                    parents[child] = (parent, field)
    return parents


def _is_guard_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Name) and func.id == "production_ledger_untouched"
    ) or (
        isinstance(func, ast.Attribute) and func.attr == "production_ledger_untouched"
    )


def _none_call_reason(node: ast.Call, parents) -> str | None:
    child: ast.AST = node
    while child in parents:
        parent, field = parents[child]
        if isinstance(parent, (ast.With, ast.AsyncWith)):
            helper = any(_is_guard_call(item.context_expr) for item in parent.items)
            if helper:
                if field == "body":
                    return None
                if field == "items":
                    return "헬퍼 인자 위치"
        if isinstance(parent, ast.Module):
            return "production_ledger_untouched 블록 밖"
        if (type(parent), field) not in _ALLOWED_PARENT_FIELDS:
            return f"허용 목록 밖 ({type(parent).__name__}.{field})"
        child = parent
    return "production_ledger_untouched 블록 밖"


def direct_engine_ledger_calls(modules: Iterable[str] | None = None) -> list[str]:
    """두 엔진 철자의 직접 호출에 대한 닫힌 구문 허용 목록 회귀 검사를 한다.

    별칭·재바인딩·partial/동적 전달, 헬퍼 `as` 별칭, 동명 사칭, 런타임 `None` 변수는
    보지 않는다. 따라서 전체 무기입 보증은 세션 기입 거부와 동적 헬퍼가 맡는다. 새 구문이
    정당하면 이 닫힌 목록에 추가해야 하며 기존 규칙을 느슨하게 하지 않는다.
    """
    guarded = {("read_stage", "run"), ("read_stage", "append_screening_ledger")}
    selected = modules
    if selected is None:
        selected = sorted(glob.glob(os.path.join(REPO, "tests", "test_*.py")))
    offenders: list[str] = []
    for module in selected:
        with open(module, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=module)
        parents = _parent_fields(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            owner = node.func.value
            if not isinstance(owner, ast.Name) or (owner.id, node.func.attr) not in guarded:
                continue
            keyword = next((item for item in node.keywords if item.arg == "shadow_root"), None)
            reason = None
            if keyword is None:
                reason = "shadow_root 없음"
            elif isinstance(keyword.value, ast.Constant) and keyword.value.value is None:
                reason = _none_call_reason(node, parents)
            if reason is not None:
                offenders.append(
                    f"{os.path.relpath(module, REPO)}:{node.lineno} "
                    f"({owner.id}.{node.func.attr}) — {reason}"
                )
    return offenders
