# -*- coding: utf-8 -*-
"""`run_kind` 계약 어휘와 `partial_until` 진입 가드의 회귀 시험."""

from __future__ import annotations

import os
import re
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine import paths as engine_paths  # noqa: E402
from engine.stages import StageError, load_yaml  # noqa: E402
from engine.stages import source as source_stage  # noqa: E402


def _inputs_and_run(tmp_path, name: str, *, repo: str | None = None, **overrides):
    """입력·법 리포는 런 작업장 밖에 두고 source 진입을 한 번 호출한다."""
    base = os.path.join(str(tmp_path), name)
    inbox = os.path.join(base, "inbox")
    os.makedirs(inbox, exist_ok=True)
    patent_path, figures = m2.make_source_inputs(inbox)
    law = repo or m2.make_law_repo(os.path.join(base, "law"))
    run_root = os.path.join(base, "runs", name)
    kwargs = {
        "run_root": run_root,
        "source_patent_path": patent_path,
        "figures_dir": figures,
        "run_id": "example-xx1111111a1-rotary-feeder",
        "patent_meta": m2.PATENT_META.copy(),
        "repo": law,
    }
    kwargs.update(overrides)
    return run_root, source_stage.run(**kwargs)


def _expect_no_artifacts(run_root: str) -> None:
    if os.path.exists(run_root) and os.listdir(run_root):
        pytest.fail(f"진입 거부 전에 산출물이 생겼다: {os.listdir(run_root)!r}")


def test_unknown_run_kind_is_rejected_before_artifacts(tmp_path) -> None:
    """(a) enum 밖 문자열은 기록되지 않고 어떤 산출물도 만들지 않는다."""
    run_root = os.path.join(str(tmp_path), "a", "runs", "a")
    with pytest.raises(StageError, match="run_kind 어휘 위반"):
        _inputs_and_run(tmp_path, "a", run_kind="bogus")
    _expect_no_artifacts(run_root)


def test_partial_requires_partial_until_before_artifacts(tmp_path) -> None:
    """(b) 부분 런의 종료선 누락은 산출 전에 거부된다."""
    run_root = os.path.join(str(tmp_path), "b", "runs", "b")
    with pytest.raises(StageError, match="partial 런은 partial_until 이 필요하다"):
        _inputs_and_run(tmp_path, "b", run_kind="partial")
    _expect_no_artifacts(run_root)


def test_partial_rejects_unknown_termination_before_artifacts(tmp_path) -> None:
    """(c) 부분 런 종료선도 계약의 13종 어휘에 속해야 한다."""
    run_root = os.path.join(str(tmp_path), "c", "runs", "c")
    with pytest.raises(StageError, match="partial 런은 partial_until 이 필요하다"):
        _inputs_and_run(
            tmp_path, "c", run_kind="partial", partial_until="bogus-stage"
        )
    _expect_no_artifacts(run_root)


def test_partial_records_declared_termination(tmp_path) -> None:
    """(d) 유효한 부분 런은 종료선을 run.yaml과 조기 보고 양쪽에 기록한다."""
    run_root, outcome = _inputs_and_run(
        tmp_path, "d", run_kind="partial", partial_until="read"
    )
    recorded = load_yaml(os.path.join(run_root, "run.yaml"))
    if recorded.get("run_kind") != "partial" or recorded.get("partial_until") != "read":
        pytest.fail(f"부분 런 선언이 run.yaml에 보존되지 않았다: {recorded!r}")
    if outcome["report"].get("partial_until") != "read":
        pytest.fail(f"조기 보고가 종료선을 싣지 않았다: {outcome['report']!r}")


def test_default_run_records_declared_absence(tmp_path) -> None:
    """(e) 비부분 런도 `partial_until: null` 키를 항상 기록한다."""
    run_root, outcome = _inputs_and_run(tmp_path, "e")
    recorded = load_yaml(os.path.join(run_root, "run.yaml"))
    if "partial_until" not in recorded or recorded["partial_until"] is not None:
        pytest.fail(f"partial_until의 선언된 부재가 없다: {recorded!r}")
    if "partial_until" not in outcome["report"] or outcome["report"]["partial_until"] is not None:
        pytest.fail(f"조기 보고의 선언된 부재가 없다: {outcome['report']!r}")


def test_nonpartial_rejects_meaningless_partial_until(tmp_path) -> None:
    """(f) 부분 런이 아닌데 종료선을 주면 뜻 없는 값을 거부한다."""
    run_root = os.path.join(str(tmp_path), "f", "runs", "f")
    with pytest.raises(StageError, match="partial 이 아닌 런에 partial_until"):
        _inputs_and_run(tmp_path, "f", run_kind="rehearsal", partial_until="read")
    _expect_no_artifacts(run_root)


def test_run_kind_enum_is_loaded_from_the_pinned_law_repo(tmp_path) -> None:
    """(g) enum의 정본은 엔진 작업트리가 아니라 그 런에 결박된 법 리포다."""
    law = m2.make_law_repo(os.path.join(str(tmp_path), "g", "law"))
    target = os.path.join(law, "contracts", "run-kinds.yaml")
    with open(target, encoding="utf-8") as handle:
        contract = yaml.safe_load(handle)
    contract["run_kind_enum"].remove("partial")
    with open(target, "w", encoding="utf-8") as handle:
        yaml.safe_dump(contract, handle, allow_unicode=True, sort_keys=False)
    m2.commit_law(law, "drop partial")

    run_root = os.path.join(str(tmp_path), "g-run", "runs", "g-run")
    with pytest.raises(StageError, match="run_kind 어휘 위반") as excinfo:
        _inputs_and_run(
            tmp_path,
            "g-run",
            repo=law,
            run_kind="partial",
            partial_until="read",
        )
    if type(excinfo.value) is not StageError:
        pytest.fail(f"정확한 예외형이 StageError가 아니다: {type(excinfo.value)!r}")
    _expect_no_artifacts(run_root)


def test_partial_termination_enum_equals_spec_stage_ids() -> None:
    """(h) SPEC §1.3~§1.15 제목의 백틱 ID 13개를 정규식으로 뽑아 enum과 집합 대조한다."""
    with open(os.path.join(REPO, "docs", "SPEC.md"), encoding="utf-8") as handle:
        spec = handle.read()
    stage_ids = set(
        re.findall(
            r"^### §1\.(?:[3-9]|1[0-5])(?: ★CP[12] —)? `([^`]+)`",
            spec,
            flags=re.MULTILINE,
        )
    )
    if len(stage_ids) != 13:
        pytest.fail(f"SPEC §1.3~§1.15에서 13개 ID를 못 뽑았다: {sorted(stage_ids)!r}")
    contract_ids = set(
        engine_paths.run_kinds_contract(REPO)["kinds"]["partial"]["terminates_at_enum"]
    )
    if contract_ids != stage_ids:
        pytest.fail(f"partial 종료선 {sorted(contract_ids)!r} != SPEC {sorted(stage_ids)!r}")


def test_legacy_contract_without_partial_allows_default_rehearsal(tmp_path) -> None:
    """(i) 구 법 트리의 rehearsal은 없는 partial 블록을 읽지 않는다."""
    law = m2.make_law_repo(os.path.join(str(tmp_path), "i", "law"))
    target = os.path.join(law, "contracts", "run-kinds.yaml")
    with open(target, encoding="utf-8") as handle:
        contract = yaml.safe_load(handle)
    contract["run_kind_enum"].remove("partial")
    del contract["kinds"]["partial"]
    with open(target, "w", encoding="utf-8") as handle:
        yaml.safe_dump(contract, handle, allow_unicode=True, sort_keys=False)
    m2.commit_law(law, "restore legacy run kinds")

    run_root, _outcome = _inputs_and_run(tmp_path, "i-run", repo=law)
    recorded = load_yaml(os.path.join(run_root, "run.yaml"))
    if "partial_until" not in recorded or recorded["partial_until"] is not None:
        pytest.fail(f"구 법 rehearsal의 partial_until 부재 선언이 없다: {recorded!r}")


def test_partial_without_partial_contract_block_is_stage_error(tmp_path) -> None:
    """(j) enum만 남은 손상 법은 partial 진입을 제어된 계약 오류로 거부한다."""
    law = m2.make_law_repo(os.path.join(str(tmp_path), "j", "law"))
    target = os.path.join(law, "contracts", "run-kinds.yaml")
    with open(target, encoding="utf-8") as handle:
        contract = yaml.safe_load(handle)
    del contract["kinds"]["partial"]
    with open(target, "w", encoding="utf-8") as handle:
        yaml.safe_dump(contract, handle, allow_unicode=True, sort_keys=False)
    m2.commit_law(law, "damage partial contract block")

    with pytest.raises(
        StageError, match=r"run_kind 어휘 위반|terminates_at_enum"
    ) as excinfo:
        _inputs_and_run(
            tmp_path,
            "j-run",
            repo=law,
            run_kind="partial",
            partial_until="read",
        )
    if type(excinfo.value) is not StageError:
        pytest.fail(f"정확한 예외형이 StageError가 아니다: {type(excinfo.value)!r}")
