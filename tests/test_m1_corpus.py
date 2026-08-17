# -*- coding: utf-8 -*-
"""M1 합성 코퍼스 관문의 **상설화**.

`tools/check_validator_enforcement.py` 는 커밋 전 관문이지만, 사람이 손으로 돌리는 관문은
돌리지 않으면 없는 것과 같다. 이 파일은 그 도구를 pytest 로 묶어 **매 스위트 실행에서**
재확인한다 — M0.6 재감수가 "표본은 전부 데이터로 존재하나 이를 돌리는 실행기가 없다"를
결함으로 판정한 바로 그 자리다(잔여 목록 19번).

여기서 `assert` 를 쓰는 것은 무방하다(pytest 는 AST 재작성으로 assert 를 if/raise 로 바꾸므로
`python3 -O` 에서도 사라지지 않는다). 다만 **서브프로세스의 종료 코드는 명시 비교**로 본다 —
그것이 이 리포가 요구하는 검증 서식이다(SPEC §8.3 2항).
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tools", "check_validator_enforcement.py")
CORPUS = os.path.join(REPO, "tests", "fixtures", "reader")


def _run(args: list[str], *, optimize: bool = False) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if optimize:
        env["PYTHONOPTIMIZE"] = "1"
    env["PYTHONPATH"] = REPO + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, TOOL, *args],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_corpus_directory_is_not_empty():
    """코퍼스가 비어 있으면 아래 모든 판정이 공허하게 통과한다 — 이 리포가 반복해서 벌해 온 결함의 형태다."""
    invalid = os.path.join(CORPUS, "invalid")
    assert os.path.isdir(invalid), f"변조본 디렉터리가 없다: {invalid}"
    entries = [n for n in os.listdir(invalid) if n.endswith((".json", ".md"))]
    assert len(entries) >= 20, f"변조본이 {len(entries)}건뿐이다 — 하한 20"


def test_validator_enforcement_gate_passes():
    """검증기가 합성 코퍼스의 변조본을 **정확히 선언된 검사만으로** 잡지 못하면, N14의 '구현으로 해소'가 주장에 그친다."""
    proc = _run([])
    if proc.returncode != 0:
        pytest.fail(
            f"check_validator_enforcement.py 종료 코드 {proc.returncode} (기대 0)\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )


def test_validator_enforcement_gate_is_identical_under_optimize():
    """`python3 -O` 에서 판정이 달라지면 그 도구는 최적화 모드에서 공허 통과하는 것이다(SPEC §8.3 4항)."""
    plain = _run([])
    optimized = _run([], optimize=True)
    if plain.returncode != optimized.returncode:
        pytest.fail(
            f"종료 코드 불일치: python3={plain.returncode} · python3 -O={optimized.returncode}\n"
            f"--- -O stderr ---\n{optimized.stderr}"
        )


def test_baseline_block_reports_every_check():
    """기준선 블록이 검사를 하나라도 빠뜨리면 '무변조가 전부 통과한다'는 주장이 부분 주장이 된다."""
    proc = _run(["--json"])
    if proc.returncode != 0:
        pytest.fail(f"도구 실패(exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    import json

    payload = json.loads(proc.stdout)
    rows = payload["baseline"]["checks"]
    ids = [row["check_id"] for row in rows]
    assert len(ids) == len(set(ids)), f"판정 행이 중복되었다: {ids}"

    sys.path.insert(0, REPO)
    from reader.lib import run_checks  # noqa: PLC0415

    expected = set(run_checks.READ_CHECK_IDS) | set(run_checks.FREEZE_CHECK_IDS)
    assert set(ids) == expected, f"기준선이 덮지 않은 검사: {sorted(expected - set(ids))}"


def test_no_baseline_check_is_vacuous():
    """대상 0건으로 통과한 검사가 기준선에 있으면, 그 검사는 코퍼스에 대해 아무것도 반증하지 않는다(재정 N5)."""
    proc = _run(["--json"])
    import json

    payload = json.loads(proc.stdout)
    vacuous = payload["baseline"]["vacuous"]
    assert not vacuous, f"공허 날인된 기준선 검사: {vacuous}"


def test_every_declared_check_has_a_mutant_except_schema():
    """변조본이 배정되지 않은 검사는 '있다고 적혀 있으나 시험되지 않은 검사'다.

    `read.schema` 만 예외이며 그것은 누락이 아니라 이 코퍼스의 정의다 — 전 변조본이 스키마를
    통과해야 검증기를 시험한 것이 되므로, 스키마가 거부하는 판은 정의상 여기 들어올 수 없다
    (그 몫은 `tests/fixtures/schema-enforcement/`).
    """
    proc = _run(["--json"])
    import json

    payload = json.loads(proc.stdout)
    tally = payload["tally"]
    unexercised = sorted(cid for cid, n in tally.items() if n == 0 and cid != "read.schema")
    assert not unexercised, f"변조본 0건인 검사: {unexercised}"
    assert tally.get("read.schema", 0) == 0, (
        "read.schema 에 변조본이 배정되었다 — 스키마가 잡는 결함은 이 코퍼스의 대상이 아니다"
    )
