# -*- coding: utf-8 -*-
"""감사 X-1·X-2·X-3·C-3 의 조기 판정서 조립 회귀를 반증한다."""

from __future__ import annotations

import copy
import json
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.stages import (  # noqa: E402
    StageEnvironmentError,
    failure_row_of_kind,
    failure_rows_for_checks,
)
from engine.stages.read import _failure_verdict  # noqa: E402
from reader.lib.report import CheckRow  # noqa: E402
from reader.lib.run_checks import to_convergence_payload  # noqa: E402


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


def unclassified_row(read_run: str | None, *, text: str) -> CheckRow:
    extras = {
        "unclassified_detail": [
            {
                "claim": "CL-3",
                "dependency_type": "unclassified",
                "text_verbatim": text,
                "text_status": "verbatim",
            }
        ]
    }
    if read_run is not None:
        extras["read_run"] = read_run
    return CheckRow(check_id="read.dependency-parse", checked=1, extras=extras)


def test_t23_unclassified_union_preserves_identity_and_reports_both_runs() -> None:
    """같은 3튜플을 한 행으로 접은 뒤 신고 실행만 순회 순서대로 합친다(재정 T23)."""
    rows = [
        unclassified_row("read-a", text="The assembly of claim 1 in a Markush form."),
        unclassified_row("read-b", text="The assembly of claim 1 in a Markush form."),
    ]
    payload = to_convergence_payload(rows, phase="early", canonical_read_run="read-a")
    actual = payload["unclassified_dependents"]
    if len(actual) != 1:
        pytest.fail(f"같은 미분류 신고 기대 1행, 실제 {len(actual)}행: {actual!r}")
    if actual[0].get("reported_by") != ["read-a", "read-b"]:
        pytest.fail(
            "같은 신고의 reported_by 기대 정본 순서 [read-a, read-b], 실제 "
            f"{actual[0].get('reported_by')!r}"
        )


def test_t23_unclassified_divergence_keeps_two_attributed_rows() -> None:
    """문언이 갈린 신고는 dedupe 축을 넓히지 않고 각각 자기 실행에 귀속한다(재정 T23)."""
    rows = [
        unclassified_row("read-a", text="Canonical wording of claim 3."),
        unclassified_row("read-b", text="Peer wording of claim 3."),
    ]
    payload = to_convergence_payload(rows, phase="early", canonical_read_run="read-a")
    actual = payload["unclassified_dependents"]
    if len(actual) != 2:
        pytest.fail(f"갈린 미분류 신고 기대 2행, 실제 {len(actual)}행: {actual!r}")
    attributions = [entry.get("reported_by") for entry in actual]
    if attributions != [["read-a"], ["read-b"]]:
        pytest.fail(f"갈린 신고 귀속 기대 [[read-a], [read-b]], 실제 {attributions!r}")


def test_t23_nonempty_unclassified_report_without_run_fails_closed() -> None:
    """실행 귀속 없는 비어 있지 않은 신고를 받으면 익명 판정서를 만들지 않는다(재정 T23)."""
    row = unclassified_row(None, text="Unattributed wording of claim 3.")
    with pytest.raises(ValueError) as excinfo:
        to_convergence_payload([row], phase="early", canonical_read_run="read-a")
    message = str(excinfo.value)
    for token in ("read.dependency-parse", "실행 귀속 없는 미분류 신고"):
        if token not in message:
            pytest.fail(f"귀속 누락 ValueError 에 {token!r} 이 없다: {message!r}")


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


# 계약이 **halt** 를 정한 failure[] 행에서 검사 id 를 파생한다. 손으로 든 표는 계약에 행이
# 늘거나 빠져도 따라갈 의무가 없어 감사 지적 3처럼 세탁될 수 있었다. 진입 검사는 예외 경로,
# 나머지는 _failure_verdict 경로이므로 checks_on_entry 등재 여부로 두 갈래를 나눈다.
def contract_halt_partitions() -> tuple[tuple[tuple[str, str], ...], tuple[tuple[str, str], ...], int, tuple[str, ...]]:
    contract = load_stage_contract("read")
    entry_ids = {
        str(entry.get("id"))
        for entry in contract.get("checks_on_entry") or []
        if isinstance(entry, dict) and str(entry.get("id", "")).startswith("read.")
    }
    entry_path: list[tuple[str, str]] = []
    verdict_path: list[tuple[str, str]] = []
    missing_ids: list[str] = []
    halt_rows = 0
    for row in contract.get("failure") or []:
        final_action = str(row.get("then", row.get("action")))
        if final_action != "halt":
            continue
        halt_rows += 1
        condition = str(row.get("condition", ""))
        check_ids = tuple(row.get("checks") or ())
        if not check_ids:
            missing_ids.append(condition)
            continue
        for check_id in check_ids:
            target = entry_path if row.get("judged_at") == "entry" else verdict_path
            target.append((check_id, condition))
    return tuple(entry_path), tuple(verdict_path), halt_rows, tuple(missing_ids)


ENTRY_HALT_CHECKS, VERDICT_HALT_CHECKS, HALT_ROW_COUNT, HALT_ROWS_WITHOUT_IDS = (
    contract_halt_partitions()
)
# 공허한 파라미터 목록은 pytest 의 skip 으로 세탁되지 않게 실패 표본을 하나 세운다. 아래
# 비-파라미터 완전성 시험도 두 갈래의 계수 하한을 독립적으로 고정한다.
VERDICT_HALT_CASES = VERDICT_HALT_CHECKS or ((None, ""),)


def test_contract_halt_partition_is_complete_and_nonempty() -> None:
    """계약 halt 행 전량이 진입·판정 두 경로로 빠짐없이 갈리고 어느 갈래도 공허하지 않다."""
    if HALT_ROWS_WITHOUT_IDS:
        pytest.fail(f"halt failure 행에서 read.* 검사 id 를 뽑지 못했다: {HALT_ROWS_WITHOUT_IDS!r}")
    if len(ENTRY_HALT_CHECKS) < 1:
        pytest.fail(f"진입 경로 halt 검사 계수 기대 1 이상, 실제 {len(ENTRY_HALT_CHECKS)}")
    if len(VERDICT_HALT_CHECKS) < 1:
        pytest.fail(f"_failure_verdict 경로 halt 검사 계수 기대 1 이상, 실제 {len(VERDICT_HALT_CHECKS)}")
    derived_count = len(ENTRY_HALT_CHECKS) + len(VERDICT_HALT_CHECKS)
    if derived_count != HALT_ROW_COUNT:
        pytest.fail(f"halt 행당 검사 id 기대 {HALT_ROW_COUNT}건, 실제 파생 {derived_count}건")


@pytest.mark.parametrize(("check_id", "condition"), VERDICT_HALT_CASES)
def test_contract_halt_outranks_repeat_escalation(
    check_id: str | None, condition: str
) -> None:
    """계약이 halt 를 정한 검사는 같은 실패 서명의 재현에도 halt 를 유지한다.

    ★ 이 시험은 **전제부터 잰다.** 계약이 그 행을 halt 가 아닌 무엇으로 바꾸면 아래 대조가
    조용히 무의미해지므로(escalate == escalate 로 통과한다) 먼저 halt 임을 확인한다.
    """
    if check_id is None:
        pytest.fail("_failure_verdict 경로 halt 검사가 0건이다 — 공허 parametrize 는 허용하지 않는다")
    contract = load_stage_contract("read")
    entry = failure_rows_for_checks(contract, {check_id})[0]
    expected = str(entry.get("then", entry.get("action")))
    if expected != "halt":
        pytest.fail(
            f"전제 붕괴 — 계약이 {condition!r} 에 정한 조치가 halt 가 아니라 {expected!r} 다. "
            "이 시험의 대조가 무의미해졌으니 계약 파생 결과를 다시 보라"
        )
    actual, _ = _failure_verdict(contract, [CheckRow(check_id=check_id)], repeated=True)
    if actual != expected:
        pytest.fail(f"{check_id} 반복 처분 기대 {expected!r}, 실제 {actual!r}")


def test_repeat_escalation_still_applies_where_the_contract_did_not_say_halt() -> None:
    """역대조 — halt 를 앞세우느라 `repeated` 상신 자체를 죽이면 재정 T16 §6 ⑤ 가 무효가 된다."""
    contract = load_stage_contract("read")
    verbatim_entry = failure_rows_for_checks(contract, {"read.verbatim"})[0]
    verbatim_final = str(verbatim_entry.get("then", verbatim_entry.get("action")))
    if verbatim_final == "halt":
        pytest.fail(
            "전제 붕괴 — 계약의 read.verbatim 최종 조치가 halt 다. "
            "'계약이 halt 라고 하지 않은 자리'라는 역대조가 무의미하다"
        )
    repeated_entry = failure_row_of_kind(contract, "retry-repeat")
    expected_repeated = str(repeated_entry["action"])
    expected_reason = repeated_entry.get("reason_label")
    actual_repeated, actual_reason = _failure_verdict(
        contract, [CheckRow(check_id="read.verbatim")], repeated=True
    )
    if actual_repeated != expected_repeated:
        pytest.fail(
            f"read.verbatim 반복 처분 기대 {expected_repeated!r}, 실제 {actual_repeated!r}"
        )
    if actual_reason != expected_reason:
        pytest.fail(
            f"같은 실패 서명 reason_label 기대 {expected_reason!r}, 실제 {actual_reason!r}"
        )


def test_read_input_digest_halt_stays_on_the_entry_exception_path(tmp_path, monkeypatch) -> None:
    """read.input-digest 의 halt 는 진입 예외 경로에 머물러야 한다.

    이 분리가 깨져 진입 검사가 fail 판정 행을 반환하면 `_failure_verdict` 는 이 검사 전용
    분기를 갖지 않으므로 계약이 halt 로 정한 처분이 코드에서 조용히 escalate 로 강등된다.
    """
    entry_ids = {check_id for check_id, _ in ENTRY_HALT_CHECKS}
    if "read.input-digest" not in entry_ids:
        pytest.fail(
            "계약 파생 진입 경로 halt 검사에 read.input-digest 가 없다: "
            f"{sorted(entry_ids)}"
        )

    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source status 기대 ok, 실제 {source_outcome['status']}")
    paths = RunPaths(root)
    with open(paths.patent_md, "a", encoding="utf-8") as handle:
        handle.write("\n[entry-digest-mismatch] actual file mutation\n")
    contract = load_stage_contract("read")
    entry = failure_rows_for_checks(contract, {"read.input-digest"})[0]
    if entry.get("judged_at") != "entry" or entry.get("action") != "halt" or entry.get("reason_label") != "환경 오류":
        pytest.fail(f"read.input-digest 진입 행 값이 틀렸다: {entry!r}")

    import engine.stages.read as read_stage

    calls = 0
    original = read_stage._failure_verdict

    def counted(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(read_stage, "_failure_verdict", counted)
    adapter = m2.ReplayLaneAdapter(os.path.join(root, "10-read", "lanes"))
    with pytest.raises(StageEnvironmentError) as excinfo:
        m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    if calls != 0:
        pytest.fail(f"진입 지문 실패가 _failure_verdict를 호출했다: {calls}")
    diagnosis = str(excinfo.value)
    missing = [
        token
        for token in (
            "환경 오류",
            "00-source/patent.sha256",
            "run.yaml#patent.source_sha256",
            "실측",
            "기대",
        )
        if token not in diagnosis
    ]
    if missing:
        pytest.fail(f"진입 지문 예외 진단 누락 {missing}, 실제 {diagnosis!r}")
