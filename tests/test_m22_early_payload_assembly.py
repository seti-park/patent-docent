# -*- coding: utf-8 -*-
"""감사 X-1·X-2·X-3·C-3 의 조기 판정서 조립 회귀를 반증한다."""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.stages import failure_entry  # noqa: E402
from engine.stages.read import _failure_verdict  # noqa: E402
from reader.lib.report import CheckRow  # noqa: E402


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def run_attempts(tmp_path, *, per_attempt: dict[int, dict]):
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source status 기대 ok, 실제 {source_outcome['status']}")
    lanes_root = None
    for attempt, payloads_by_run in sorted(per_attempt.items()):
        lanes_root = m2.write_lane_responses(
            root, payloads_by_run=payloads_by_run, attempts=(attempt,)
        )
    if lanes_root is None:
        pytest.fail("응답 회차가 하나도 없다 — 조기 조립 시험이 공허하다")
    adapter = m2.ReplayLaneAdapter(lanes_root)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    return root, outcome, adapter


def ghost_unclassified_payload() -> dict:
    payload = m2.payload_set()
    ghost = copy.deepcopy(payload["decompose"]["claims"]["dependents"][0])
    ghost["id"] = "CL-9"
    ghost["dependency_type"] = "unclassified"
    ghost["additions"] = []
    payload["decompose"]["claims"]["dependents"].append(ghost)
    return payload


def test_both_runs_vacuous_dependency_parse_still_writes_the_verdict(tmp_path) -> None:
    """이 시험이 없으면 공허 파생 목록의 중복 제거가 판정 행 자체를 지운 것으로 바뀌어도 드러나지 않는다."""
    payloads = {
        "read-a": m2.payload_set(dependency_type="unclassified"),
        "read-b": m2.payload_set(dependency_type="unclassified"),
    }
    root, _, _ = m2.run_read(tmp_path, payloads_by_run=payloads)
    path = RunPaths(root).convergence_early_json
    if not os.path.isfile(path):
        pytest.fail(f"조기 판정서가 실재해야 한다: {path}")
    report = load_json(path)
    vacuous = report.get("vacuous_pass") or []
    if len(set(vacuous)) != len(vacuous):
        pytest.fail(f"vacuous_pass 기대 중복 없음, 실제 {vacuous}")
    count = vacuous.count("read.dependency-parse")
    if count != 1:
        pytest.fail(f"vacuous_pass dependency-parse 기대 1회, 실제 {count}: {vacuous}")
    check_count = sum(
        1 for row in report.get("checks") or [] if row.get("check_id") == "read.dependency-parse"
    )
    if check_count != 2:
        pytest.fail(f"checks[] dependency-parse 기대 실행 수 2행, 실제 {check_count}")


def test_peer_run_unclassified_id_is_read_from_its_own_spec(tmp_path) -> None:
    """이 시험이 없으면 비정본의 미분류 ID를 정본 명세에서 조회해 판정서 쓰기 자체가 막혀도 드러나지 않는다."""
    first = {"read-a": m2.payload_set(), "read-b": ghost_unclassified_payload()}
    second = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    root, _, _ = run_attempts(tmp_path, per_attempt={0: first, 1: second})
    path = RunPaths(root).convergence_early_json
    if not os.path.isfile(path):
        pytest.fail(f"조기 판정서가 실재해야 한다: {path}")
    report = load_json(path)
    empty = [
        entry
        for entry in report.get("unclassified_dependents") or []
        if not entry.get("text_verbatim")
    ]
    if empty:
        pytest.fail(f"미분류 문언 기대 전건 비어 있지 않음, 실제 빈 항목 {empty}")


def test_canonical_unclassified_report_is_not_overwritten_by_the_peer(tmp_path) -> None:
    """이 시험이 없으면 미분류 누적을 고치지 않고 마지막 실행의 덮어쓰기 방향만 바꿔도 통과한다."""
    canonical_payloads = {
        "read-a": m2.payload_set(dependency_type="unclassified"),
        "read-b": m2.payload_set(),
    }
    canonical_root, _, _ = m2.run_read(
        tmp_path.joinpath("canonical"), payloads_by_run=canonical_payloads
    )
    canonical = load_json(RunPaths(canonical_root).convergence_early_json)
    canonical_entries = [
        entry
        for entry in canonical.get("unclassified_dependents") or []
        if entry.get("claim") == "CL-3"
    ]
    if not canonical_entries:
        pytest.fail(
            "정본 read-a가 신고한 CL-3 기대 목록에 남음, 실제 "
            f"{canonical.get('unclassified_dependents')!r}"
        )
    actual_texts = [entry.get("text_verbatim") for entry in canonical_entries]
    if m2.CLAIM_3 not in actual_texts:
        pytest.fail(f"정본 CL-3 문언 기대 {m2.CLAIM_3!r}, 실제 {actual_texts!r}")

    peer_payloads = {
        "read-a": m2.payload_set(),
        "read-b": m2.payload_set(dependency_type="unclassified"),
    }
    peer_root, _, _ = m2.run_read(tmp_path.joinpath("peer"), payloads_by_run=peer_payloads)
    peer = load_json(RunPaths(peer_root).convergence_early_json)
    if not (peer.get("unclassified_dependents") or []):
        pytest.fail("비정본 read-b만 신고한 대조군 기대 미분류 목록 비지 않음, 실제 []")


# 계약이 **halt** 를 정한 검사와 그 조치를 든 failure 행의 표지.
# 감사 지적 C-3 은 `read.schema` 하나를 지목했지만 결함은 계열이었다 — 계약이 halt 를 정한
# 행이 `repeated` escalate 뒤에 서 있는 것. 한 행만 고치고 시험도 그 한 행만 보면 남은 절반이
# 「고쳐진 계열」로 보인다. 그래서 표로 든다.
HALT_CHECKS = (
    ("read.schema", "read.schema 실패"),
    ("read.source-digest", "원천 다이제스트"),
)


@pytest.mark.parametrize(("check_id", "label"), HALT_CHECKS)
def test_contract_halt_outranks_repeat_escalation(check_id: str, label: str) -> None:
    """계약이 halt 를 정한 검사는 같은 실패 서명의 재현에도 halt 를 유지한다.

    ★ 이 시험은 **전제부터 잰다.** 계약이 그 행을 halt 가 아닌 무엇으로 바꾸면 아래 대조가
    조용히 무의미해지므로(escalate == escalate 로 통과한다) 먼저 halt 임을 확인한다.
    """
    contract = load_stage_contract("read")
    entry = failure_entry(contract, label)
    expected = str(entry.get("then", entry.get("action")))
    if expected != "halt":
        pytest.fail(
            f"전제 붕괴 — 계약이 {label!r} 에 정한 조치가 halt 가 아니라 {expected!r} 다. "
            "이 시험의 대조가 무의미해졌으니 표(HALT_CHECKS)를 다시 보라"
        )
    actual, _ = _failure_verdict(contract, [CheckRow(check_id=check_id)], repeated=True)
    if actual != expected:
        pytest.fail(f"{check_id} 반복 처분 기대 {expected!r}, 실제 {actual!r}")


def test_repeat_escalation_still_applies_where_the_contract_did_not_say_halt() -> None:
    """역대조 — halt 를 앞세우느라 `repeated` 상신 자체를 죽이면 재정 T16 §6 ⑤ 가 무효가 된다."""
    contract = load_stage_contract("read")
    repeated_entry = failure_entry(contract, "같은 실패 서명")
    expected_repeated = str(repeated_entry["action"])
    actual_repeated, _ = _failure_verdict(
        contract, [CheckRow(check_id="read.verbatim")], repeated=True
    )
    if actual_repeated != expected_repeated:
        pytest.fail(
            f"read.verbatim 반복 처분 기대 {expected_repeated!r}, 실제 {actual_repeated!r}"
        )
