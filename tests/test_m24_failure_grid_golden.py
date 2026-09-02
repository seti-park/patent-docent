# -*- coding: utf-8 -*-
"""재정 T26·T28·T29의 동결된 READ 실패 격자를 현 구현과 전 칸 대조한다."""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

from engine.paths import load_stage_contract
from engine.stages import StageError
from engine.stages.read import ENGINE_READ_CHECK_IDS, _failure_verdict
from reader.lib.report import CheckRow
from reader.lib.run_checks import READ_CHECK_IDS


REPO = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = REPO / "tests" / "fixtures" / "read-failure-grid"
MANIFEST = FIXTURE / "manifest.json"
VALIDATOR = FIXTURE / "validate_manifest.py"
if not VALIDATOR.is_file():
    pytest.fail(f"manifest 검증기가 없다: {VALIDATOR}")
_spec = importlib.util.spec_from_file_location("read_failure_grid_validator", VALIDATOR)
if _spec is None or _spec.loader is None:
    pytest.fail(f"manifest 검증기 적재 명세를 만들 수 없다: {VALIDATOR}")
validate_manifest_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_manifest_mod)

TESTS = REPO / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))
from test_m24a_failure_grid_generator import TV_MUTATIONS  # noqa: E402


def _tree_head() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "99fad78"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        pytest.fail(f"git rev-parse 99fad78 실패(exit {proc.returncode}): {proc.stderr}")
    return proc.stdout.strip()


@pytest.fixture(scope="module")
def manifest() -> dict:
    if not MANIFEST.is_file():
        pytest.fail(f"골든 manifest가 없다: {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _validate(value) -> list[str]:
    return validate_manifest_mod.validate_manifest(
        value,
        expected_check_ids=set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS),
        required_base_commit="99fad78",
        required_tree_head=_tree_head(),
    )


def _violation_ids(violations: list[str]) -> set[str]:
    return {line.partition(":")[0] for line in violations}


def test_manifest_shape_universe_beta_and_provenance(manifest: dict) -> None:
    violations = _validate(manifest)
    if violations:
        pytest.fail(f"골든 manifest 정적 검증 실패: {violations!r}")
    expected_keys = {
        f"{mask}:{repeated}"
        for mask in range(1, 1 << 12)
        for repeated in (0, 1)
    }
    if set(manifest["cells"]) != expected_keys:
        pytest.fail("골든 셀 키 우주가 시험이 독립 생성한 8,190칸과 다르다")
    bit = manifest["check_ids"].index("read.convergence")
    beta = {f"{mask}:1" for mask in range(1, 1 << 12) if (mask >> bit) & 1}
    exception = manifest["exceptions"][0]
    if set(exception["cells"]) != beta or exception["cell_count"] != len(beta):
        pytest.fail("T28 β 표지가 시험의 고정 convergence 식과 다르다")


def test_every_golden_cell_matches_runtime(manifest: dict) -> None:
    contract = load_stage_contract("read", None)
    check_ids = manifest["check_ids"]
    mismatches: list[tuple[str, object, object]] = []
    for mask in range(1, 1 << 12):
        failing = [
            CheckRow(check_id=check_id)
            for index, check_id in enumerate(check_ids)
            if mask & (1 << index)
        ]
        for repeated in (0, 1):
            key = f"{mask}:{repeated}"
            expected = manifest["cells"][key]
            try:
                actual = list(_failure_verdict(contract, failing, repeated=bool(repeated)))
            except StageError:
                actual = "StageError"
            if actual != expected:
                mismatches.append((key, expected, actual))
                if len(mismatches) >= 10:
                    break
        if len(mismatches) >= 10:
            break
    if mismatches:
        pytest.fail(f"골든↔런타임 불일치(최대 10개): {mismatches!r}")


def test_validator_constraint_ids_equal_tv(manifest: dict) -> None:
    ids = validate_manifest_mod.CONSTRAINT_IDS
    tv_ids = [constraint_id for constraint_id, _ in TV_MUTATIONS]
    if not isinstance(ids, tuple) or not all(isinstance(item, str) for item in ids):
        pytest.fail(f"CONSTRAINT_IDS 형식 위반: {ids!r}")
    if len(ids) != len(set(ids)) or len(ids) != len(tv_ids) or set(ids) != set(tv_ids):
        pytest.fail("CONSTRAINT_IDS와 T-V 변조표가 양방향 상등이 아니다")


@pytest.mark.parametrize("constraint_id,mutate", TV_MUTATIONS, ids=[row[0] for row in TV_MUTATIONS])
def test_each_tv_mutation_reports_exactly_its_constraint(
    constraint_id: str, mutate, manifest: dict
) -> None:
    box = {"manifest": copy.deepcopy(manifest)}
    if constraint_id == "manifest.type":
        mutate(box)
    else:
        mutate(box["manifest"])
    actual = _violation_ids(_validate(box["manifest"]))
    if actual != {constraint_id}:
        pytest.fail(f"T-V {constraint_id} 기대 단독 위반, 실제 {sorted(actual)!r}")
