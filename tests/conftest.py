# -*- coding: utf-8 -*-
"""pytest가 시험 모듈을 단독 수집할 때 리포 루트를 import 경로에 둔다."""

from __future__ import annotations

import sys
from pathlib import Path

import os

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import ledger_guard  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402


def _same_existing_path(left: str, right: str) -> bool:
    return os.path.exists(left) and os.path.exists(right) and os.path.samefile(left, right)


def pytest_sessionstart(session) -> None:
    """수집 전에 구문 위반을 닫고 시험 환경의 마지막 생산 원장 기입 거부층을 건다.

    이것은 시험 환경의 마지막 층이며 엔진 값 공간이 아니다. 엔진 쪽 동적 강제는 자문 ⓑ로
    이연했다(D-02 §9).
    """
    offenders = ledger_guard.direct_engine_ledger_calls()
    if offenders:
        raise pytest.UsageError(
            "shadow_root 없이 또는 보호 밖에서 엔진 원장 기입 경로를 부르는 시험 모듈이 있다 "
            "— 수집 전에 멈춘다: " + ", ".join(offenders)
        )

    original = read_stage.append_screening_ledger
    session.config._pd_original_append = original

    def guarded(repo, *, run_id, memos, final, shadow_root=None):
        target = os.path.realpath(read_stage.shadow_screening_ledger(repo, shadow_root))
        production = os.path.realpath(ledger_guard.production_ledger())
        if target == production or _same_existing_path(target, production):
            pytest.fail(f"시험 환경에서 생산 섀도 원장 기입 거부: {target}")
        return original(
            repo, run_id=run_id, memos=memos, final=final, shadow_root=shadow_root
        )

    read_stage.append_screening_ledger = guarded


def pytest_sessionfinish(session, exitstatus) -> None:
    """세션 기입 거부 감싸기를 원복한다."""
    original = getattr(session.config, "_pd_original_append", None)
    if original is not None:
        read_stage.append_screening_ledger = original
