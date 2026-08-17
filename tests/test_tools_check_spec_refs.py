# -*- coding: utf-8 -*-
"""`tools/check_spec_refs.py` 회귀 테스트.

규약(CLAUDE.md §3): **`assert` 금지.** `python3 -O`에서 assert가 제거되면 테스트가
공허하게 통과한다. 여기서는 명시 비교 + `pytest.fail()`로 쓴다.

표본은 코드가 아니라 `tests/fixtures/check_spec_refs/` 데이터에 둔다
(자기매칭 격리 요건 2항 — 검사기 소스·테스트 소스에 탐지 표본 문자열을 두지 않는다).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_spec_refs.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "check_spec_refs"

# 픽스처 → 기대 종료 코드
FIXTURE_EXPECTATIONS = {
    "ok": 0,
    "bad-refs": 1,
    "bad-contracts": 1,
    "bad-retired": 1,
    "bad-schema": 1,
    "bad-glob": 1,
}

# 픽스처 → 결함이 나야 하는 검사 id
FIXTURE_FAILING_CHECKS = {
    "ok": set(),
    "bad-refs": {"K1", "K4"},
    "bad-contracts": {"K2"},
    "bad-retired": {"K5"},
    "bad-schema": {"K6"},
    "bad-glob": {"K2"},
}


def run_tool(args: list[str], optimized: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable]
    if optimized:
        cmd.append("-O")
    cmd += [str(TOOL)] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))


def load_module():
    spec = importlib.util.spec_from_file_location("check_spec_refs", TOOL)
    if spec is None or spec.loader is None:
        pytest.fail(f"모듈 로드 실패: {TOOL}")
    module = importlib.util.module_from_spec(spec)
    # dataclass 처리가 sys.modules 등록을 전제하므로 exec 전에 등록한다(python 3.14 실측).
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("fixture,expected", sorted(FIXTURE_EXPECTATIONS.items()))
def test_fixture_exit_codes(fixture: str, expected: int) -> None:
    """픽스처별 종료 코드 — ok=0, 결함 픽스처=1."""
    proc = run_tool(["--repo", str(FIXTURES / fixture)])
    if proc.returncode != expected:
        pytest.fail(
            f"EXIT MISMATCH ({fixture}): got={proc.returncode} want={expected}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


@pytest.mark.parametrize("fixture,expected", sorted(FIXTURE_EXPECTATIONS.items()))
def test_checker_behaves_identically_under_O(fixture: str, expected: int) -> None:
    """SPEC §8.3 ④ — `python3 -O`에서도 동일한 종료 코드."""
    proc = run_tool(["--repo", str(FIXTURES / fixture)], optimized=True)
    if proc.returncode != expected:
        pytest.fail(
            f"-O EXIT MISMATCH ({fixture}): got={proc.returncode} want={expected}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


@pytest.mark.parametrize("fixture,failing", sorted(FIXTURE_FAILING_CHECKS.items()))
def test_failing_checks_are_the_planted_ones(fixture: str, failing: set[str]) -> None:
    """심은 결함만 검출되고, 다른 검사는 오탐하지 않는다."""
    proc = run_tool(["--repo", str(FIXTURES / fixture), "--json"])
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"--json 출력 파싱 실패 ({fixture}): {exc}\nstdout:\n{proc.stdout}")
    got = {check["id"] for check in payload["checks"] if check["status"] == "FAIL"}
    if got != failing:
        pytest.fail(f"FAILING CHECK MISMATCH ({fixture}): got={sorted(got)} want={sorted(failing)}")


def test_glob_rows_are_checked_by_match_count() -> None:
    """재감수 N-02 — 글로브 행은 부모 디렉터리가 아니라 **매칭 파일 수**로 판정한다.

    `bad-glob` 표본은 두 방향을 동시에 어긋내 두었다(`현행` 매칭 0건 · `예정` 매칭 1건).
    한 방향만 구현하면 이 테스트가 걸린다.
    """
    proc = run_tool(["--repo", str(FIXTURES / "bad-glob"), "--json"])
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"--json 출력 파싱 실패: {exc}\nstdout:\n{proc.stdout}")
    globs = [
        finding
        for finding in payload["findings"]
        if finding["check"] == "K2" and "*" in finding["found"]
    ]
    got = sorted(finding["found"].split(" ", 1)[0] for finding in globs)
    want = ["contracts/lexicon/*.yaml", "contracts/stages/*.yaml"]
    if got != want:
        pytest.fail(f"GLOB FINDING MISMATCH: got={got} want={want}\nfindings:\n{globs}")
    planned = [finding for finding in globs if finding["found"].startswith("contracts/stages/")]
    if "표를 갱신하라" not in planned[0]["message"]:
        pytest.fail(f"`예정` 글로브 결함 메시지에 표 갱신 지시가 없다: {planned[0]['message']!r}")


def test_all_seven_checks_are_reported() -> None:
    proc = run_tool(["--repo", str(FIXTURES / "ok"), "--json"])
    payload = json.loads(proc.stdout)
    got = [check["id"] for check in payload["checks"]]
    want = ["K1", "K2", "K3", "K4", "K5", "K6", "K7"]
    if got != want:
        pytest.fail(f"CHECK LIST MISMATCH: got={got} want={want}")


def test_verbose_prints_target_section_titles() -> None:
    """--verbose는 해소된 참조를 대상 절 제목과 함께 출력한다(사람이 오참조를 잡는 근거)."""
    proc = run_tool(["--repo", str(FIXTURES / "ok"), "--verbose"])
    spec = (FIXTURES / "ok" / "docs" / "SPEC.md").read_text(encoding="utf-8")
    title = next(
        line.lstrip("#").strip()
        for line in spec.splitlines()
        if line.startswith("### ") and "6.7" in line
    )
    if title not in proc.stdout:
        pytest.fail(f"VERBOSE 출력에 대상 절 제목이 없다: {title!r}\nstdout:\n{proc.stdout}")


def test_missing_document_is_environment_error() -> None:
    """필수 문서 부재 = exit 2 (검증 실패가 아니다)."""
    proc = run_tool(["--repo", str(FIXTURES)])
    if proc.returncode != 2:
        pytest.fail(f"EXIT MISMATCH: got={proc.returncode} want=2\nstderr:\n{proc.stderr}")


def test_bad_repo_path_is_environment_error() -> None:
    proc = run_tool(["--repo", str(REPO_ROOT / "no-such-dir")])
    if proc.returncode != 2:
        pytest.fail(f"EXIT MISMATCH: got={proc.returncode} want=2\nstderr:\n{proc.stderr}")


def test_isolation_violation_refuses_to_run() -> None:
    """격리 요건 3항 — 스캔 목록에 tools/·tests/가 들어오면 finding이 아니라 exit 2."""
    module = load_module()
    for forbidden in ("tools/check_spec_refs.py", "tests/fixtures/check_spec_refs/ok/docs/SPEC.md",
                      "ledgers/regression/mutated/case-0001.md"):
        with pytest.raises(SystemExit) as excinfo:
            module.enforce_isolation([forbidden], "테스트", set(), str(REPO_ROOT))
        if excinfo.value.code != 2:
            pytest.fail(f"ISOLATION EXIT MISMATCH ({forbidden}): got={excinfo.value.code} want=2")


def test_scan_allowlist_excludes_tool_and_test_paths() -> None:
    """allowlist 자체가 격리 대상 접두를 포함하지 않는다."""
    module = load_module()
    targets = list(module.DOC_TARGETS) + [module.CONTRACT_TABLE_DOC] + list(module.CONTRACT_GLOBS)
    bad = [
        target
        for target in targets
        for prefix in module.FORBIDDEN_SCAN_PREFIXES
        if target.startswith(prefix)
    ]
    if bad:
        pytest.fail(f"allowlist가 격리 대상 경로를 포함한다: {bad}")


def test_source_contains_no_assert_statement() -> None:
    """`assert` 금지 규약의 기계 확인."""
    import ast

    tree = ast.parse(TOOL.read_text(encoding="utf-8"))
    hits = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    if hits:
        pytest.fail(f"검사기 소스에 assert 문이 있다 (행 {hits})")
