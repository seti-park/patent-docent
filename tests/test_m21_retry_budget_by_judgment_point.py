# -*- coding: utf-8 -*-
"""재정 2026-09-01 T16 의 판정점별 재시도 예산·결함 소유 단계를 반증한다.

각 시험의 docstring 한 줄은 **"이 시험이 없으면 무엇이 공허해지는가"** 다
(`tests/test_m2_read.py`·`tests/test_m17_lanes.py` 와 같은 형식).

맨 `assert` 를 쓰지 않는다 — `python3 -O` 에서 사라지지 않는 `pytest.fail()` 명시 비교로
기대와 실측을 함께 보고한다. 서브프로세스를 부르는 자리는 없으며, 생기면 종료 코드를 명시
비교한다. READ 통주는 `test_m2_read` 의 섀도 원장 격리 하네스만 조합한다.
"""

from __future__ import annotations

import copy
import importlib
import json
import os
import re
import shutil
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402
import test_m17_lanes as m17  # noqa: E402

from engine.paths import RunPaths, load_stage_contract  # noqa: E402
from engine.stages.read import decompose_only_spec  # noqa: E402
from reader.lib import (  # noqa: E402
    EARLY_CLAIM_CHECK_IDS,
    READ_CHECK_IDS,
    CheckContext,
    run_early_claim_checks,
)

TAIL_TASKS = ("ground-independent", "ground-dependent", "synthesize")
READ_RUNS = ("read-a", "read-b")


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def run_with_payloads(tmp_path, *, per_attempt: dict[int, dict]):
    """회차별 `payloads_by_run` 을 깔고 READ 를 한 번 돌린다. 반환 (run_root, outcome, adapter).

    회차마다 **모든 실행의 응답을 깐다** — 그래야 "러너가 발송하지 않았다"가 응답 부재에
    떠밀린 결과가 아니라 러너의 선택임이 증명된다.
    """
    root, source_outcome = m2.run_source(tmp_path)
    if source_outcome["status"] != "ok":
        pytest.fail(f"source status 기대 ok, 실제 {source_outcome['status']}")
    lanes_root = None
    for attempt, payloads_by_run in sorted(per_attempt.items()):
        missing = sorted(set(READ_RUNS) - set(payloads_by_run))
        if missing:
            pytest.fail(f"회차 {attempt} 에 모든 실행의 응답이 없다: {missing}")
        lanes_root = m2.write_lane_responses(
            root, payloads_by_run=payloads_by_run, attempts=(attempt,)
        )
    if lanes_root is None:
        pytest.fail("응답 회차가 하나도 없다 — READ 하네스가 공허하다")
    adapter = m2.ReplayLaneAdapter(lanes_root)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES)
    return root, outcome, adapter


def phantom_dependent_payloads() -> dict:
    """원천에 없는 CL-9 를 등재해 조기 청구항 인벤토리만 실패시킨다."""
    payloads = m2.payload_set()
    phantom = copy.deepcopy(payloads["decompose"]["claims"]["dependents"][0])
    phantom["id"] = "CL-9"
    payloads["decompose"]["claims"]["dependents"].append(phantom)
    return payloads


def dispatched_ids(adapter) -> list[str]:
    return [request.lane_id for request in adapter.dispatched]


def tail_lane_ids(lane_ids: list[str]) -> list[str]:
    return [
        lane_id
        for lane_id in lane_ids
        if any(f"/{task}/" in lane_id for task in TAIL_TASKS)
    ]


def point_budgets(repo: str | None = None) -> dict[str, int]:
    contract = load_stage_contract("read", repo)
    points = {
        entry.get("id"): entry.get("max_retries")
        for entry in (contract.get("retry_budget") or {}).get("points") or []
        if isinstance(entry, dict)
    }
    if set(points) != {"early", "exit"}:
        pytest.fail(f"판정점 기대 early·exit, 실제 {sorted(points)}")
    for point, budget in points.items():
        if type(budget) is not int:
            pytest.fail(f"{point}.max_retries 가 정수가 아니다: {budget!r}")
    return points


def retry_attempts(lane_ids: list[str], *, task: str | None = None) -> set[str]:
    selected = lane_ids
    if task is not None:
        selected = [lane_id for lane_id in selected if f"/{task}/" in lane_id]
    return {
        part
        for lane_id in selected
        for part in lane_id.split("/")
        if part.startswith("retry-")
    }


def test_v1a_early_failure_routes_to_decompose(tmp_path) -> None:
    """조기 결함의 기대·금지 좌표를 함께 재지 않으면 분해 소유라는 라우팅이 공허하다."""
    root, outcome, adapter = run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": m2.payload_set(), "read-b": phantom_dependent_payloads()},
            1: {"read-a": m2.payload_set(), "read-b": m2.payload_set()},
        },
    )
    lane_ids = dispatched_ids(adapter)
    expected = "read-b/decompose/retry-1/batch-0"
    if expected not in lane_ids:
        pytest.fail(f"조기 실패의 분해 재시도 좌표가 없다: {lane_ids}")
    forbidden = "read-a/decompose/retry-1/batch-0"
    if forbidden in lane_ids:
        pytest.fail(f"성한 read-a 분해까지 재시도했다: {lane_ids}")
    leaked = [lane_id for lane_id in tail_lane_ids(lane_ids) if "/retry-" in lane_id]
    if leaked:
        pytest.fail(f"조기 결함이 후속 재시도로 샜다: {leaked}")
    if outcome["status"] != "ok":
        pytest.fail(f"표적 재시도 뒤 status 기대 ok, 실제 {outcome['status']}")
    _ = root


def test_v1b_exit_failure_routes_to_canonical_tail(tmp_path) -> None:
    """출구 결함의 기대·금지 좌표를 함께 재지 않으면 후속 소유라는 라우팅이 공허하다."""
    broken = m17.payloads_with_dangling_reference()
    root, outcome, adapter = run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": broken, "read-b": m2.payload_set()},
            1: {"read-a": copy.deepcopy(broken), "read-b": m2.payload_set()},
        },
    )
    lane_ids = dispatched_ids(adapter)
    retried_tail = [lane_id for lane_id in tail_lane_ids(lane_ids) if "/retry-" in lane_id]
    if not retried_tail:
        pytest.fail(f"출구 실패가 후속 레인으로 돌아가지 않았다: {lane_ids}")
    wrong = [lane_id for lane_id in lane_ids if "/decompose/retry-" in lane_id]
    if wrong:
        pytest.fail(f"출구 실패가 분해로 잘못 라우팅됐다: {wrong}")
    if outcome["status"] == "ok":
        pytest.fail("두 회차 모두 유령 참조인데 status 가 ok 다")
    _ = root


def test_v1c_early_failure_defers_convergence(tmp_path) -> None:
    """원인 검사 실패 때 수렴을 보류하지 않으면 먼 증상이 다시 근인을 가린다."""
    root, outcome, _ = run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": m2.payload_set(), "read-b": phantom_dependent_payloads()},
            1: {"read-a": m2.payload_set(), "read-b": phantom_dependent_payloads()},
        },
    )
    if outcome["status"] == "ok":
        pytest.fail("조기 결함이 두 회차 모두 남았는데 status 가 ok 다")
    early = load_json(RunPaths(root).convergence_early_json)
    check_ids = [row["check_id"] for row in early["checks"]]
    if "read.convergence" in check_ids:
        pytest.fail(f"청구항 원인 실패인데 수렴 행이 실행됐다: {check_ids}")
    if early["convergence_detail"].get("executed") is not False:
        pytest.fail(f"수렴 보류의 executed 기대 False, 실제 {early['convergence_detail']}")
    inventory_rows = [row for row in early["checks"] if row["check_id"] == "read.claim-inventory"]
    if len(inventory_rows) != len(READ_RUNS):
        pytest.fail(
            f"청구항 검사가 실행별로 남지 않았다: 기대 {len(READ_RUNS)}, 실제 {len(inventory_rows)}"
        )
    failed_rules = {
        finding["rule"]
        for finding in early.get("findings") or []
        if finding.get("check") == "read.claim-inventory"
    }
    if "inventory.no-phantom" not in failed_rules:
        pytest.fail(f"유령 종속항의 근인 소견이 없다: {sorted(failed_rules)}")


def test_v1d_early_gate_orders_cause_before_convergence(tmp_path) -> None:
    """관문 순서를 실측하지 않으면 원인 검사가 수렴 앞에 선다는 부속 3 이 공허하다."""
    root, outcome, _ = m2.run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"정상 통주 status 기대 ok, 실제 {outcome['status']}")
    check_ids = [row["check_id"] for row in load_json(RunPaths(root).convergence_early_json)["checks"]]
    if not check_ids or check_ids[0] != "read.input-digest":
        pytest.fail(f"조기 관문의 첫 행이 read.input-digest 가 아니다: {check_ids}")
    if check_ids[-1:] != ["read.convergence"]:
        pytest.fail(f"조기 관문의 마지막 행이 read.convergence 가 아니다: {check_ids}")
    for check_id in EARLY_CLAIM_CHECK_IDS:
        positions = [index for index, actual in enumerate(check_ids) if actual == check_id]
        if not positions:
            pytest.fail(f"조기 관문에 {check_id} 행이 없다: {check_ids}")
        if min(positions) <= 0 or max(positions) >= len(check_ids) - 1:
            pytest.fail(f"{check_id} 가 입력 지문과 수렴 사이에 있지 않다: {check_ids}")


def test_v2_exit_retry_repairs_phase_drift(tmp_path) -> None:
    """출구 재시도가 실제 변이를 고치지 않으면 「출구 행 존치」의 존재 이유가 공허하다.

    통합이 분해 산출에서 claims 를 재복사하므로 조기 통과 후의 출구 실패는 후속 재시도가
    실제로 고친다(재정 T16 §2 ⒜).
    """
    root, outcome, adapter = run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": m17.payloads_with_dangling_reference(), "read-b": m2.payload_set()},
            1: {"read-a": m2.payload_set(), "read-b": m2.payload_set()},
        },
    )
    lane_ids = dispatched_ids(adapter)
    if outcome["status"] != "ok":
        pytest.fail(f"후속 재시도로 고친 런 status 기대 ok, 실제 {outcome['status']}")
    expected = [lane_id for lane_id in tail_lane_ids(lane_ids) if "/retry-" in lane_id]
    if not expected:
        pytest.fail(f"출구 실패의 후속 재시도 좌표가 없다: {lane_ids}")
    forbidden = [lane_id for lane_id in lane_ids if "/decompose/retry-" in lane_id]
    if forbidden:
        pytest.fail(f"출구 결함을 분해로 잘못 돌려보냈다: {forbidden}")
    if not os.path.isfile(RunPaths(root).material_spec_json):
        pytest.fail("후속 재시도가 변이를 고쳤는데 material-spec.json 이 쓰이지 않았다")


def test_v3_retry_counts_stay_within_contract_limits(tmp_path) -> None:
    """실측 회차를 계약 상한과 대조하지 않으면 판정점별 유한 예산이 공허하다."""
    budgets = point_budgets()
    early_root, early_outcome, early_adapter = run_with_payloads(
        tmp_path / "early",
        per_attempt={
            0: {"read-a": m2.payload_set(), "read-b": phantom_dependent_payloads()},
            1: {"read-a": m2.payload_set(), "read-b": phantom_dependent_payloads()},
        },
    )
    broken = m17.payloads_with_dangling_reference()
    exit_root, exit_outcome, exit_adapter = run_with_payloads(
        tmp_path / "exit",
        per_attempt={
            0: {"read-a": broken, "read-b": m2.payload_set()},
            1: {"read-a": copy.deepcopy(broken), "read-b": m2.payload_set()},
        },
    )
    early_ids = dispatched_ids(early_adapter)
    exit_ids = dispatched_ids(exit_adapter)
    for read_run in READ_RUNS:
        attempts = retry_attempts(
            [lane_id for lane_id in early_ids if lane_id.startswith(f"{read_run}/")],
            task="decompose",
        )
        if len(attempts) > budgets["early"]:
            pytest.fail(f"{read_run} 조기 재시도 {len(attempts)}회가 상한 {budgets['early']}을 넘었다")
    exit_attempts = retry_attempts(tail_lane_ids(exit_ids))
    if len(exit_attempts) > budgets["exit"]:
        pytest.fail(f"출구 재시도 {len(exit_attempts)}회가 상한 {budgets['exit']}을 넘었다")
    for label, lane_ids in (("early", early_ids), ("exit", exit_ids)):
        retry_coordinates = [lane_id for lane_id in lane_ids if "/retry-" in lane_id]
        ceiling = len(READ_RUNS) * budgets["early"] + budgets["exit"]
        if len(retry_coordinates) > ceiling:
            pytest.fail(f"{label} 런의 재시도 좌표 {len(retry_coordinates)}개가 총상한 {ceiling}을 넘었다")
        retry_two = [lane_id for lane_id in lane_ids if "/retry-2/" in lane_id]
        if retry_two:
            pytest.fail(f"{label} 런에 retry-2 좌표가 있다: {retry_two}")
    if early_outcome["status"] == "ok" or exit_outcome["status"] == "ok":
        pytest.fail(
            "상한 표본의 결함이 사라졌다: "
            f"early={early_outcome['status']} exit={exit_outcome['status']}"
        )
    _ = early_root, exit_root


def test_v4_us854_early_and_final_claim_checks_match() -> None:
    """낡은 기준 상수는 통과하든 실패하든 무회귀를 증명하지 못하므로 같은 실행의 전후를 잰다.

    선례는 `tests/test_m20_figure_caption_case.py#narrowed_rules` 이며, verdict 를 시험에 박지 않는다.
    """
    root = os.path.join(REPO, "runs", "openai-us20260147854a1-cim-fp-3")
    if not os.path.isdir(root):
        pytest.skip("'854 기록 런이 이 체크아웃에 없다")
    paths = RunPaths(root)
    full = load_json(paths.material_spec_json)
    canonical = str(full["provenance"]["read_runs"][0]).removesuffix(":canonical")
    lane_log = load_json(paths.lane_log)
    rows = [
        row
        for row in lane_log
        if row.get("task") == "decompose" and row.get("read_run") == canonical
    ]
    if not rows:
        pytest.fail(f"정본 실행 {canonical} 의 분해 로그가 없다")
    lane_id = rows[-1]["lane_id"]
    response = load_json(os.path.join(paths.lanes_dir, *lane_id.split("/"), "response.json"))
    payload = response.get("payload")
    if not isinstance(payload, dict):
        pytest.fail(f"마지막 정본 분해 응답에 payload 가 없다: {lane_id}")
    early = decompose_only_spec(
        run_meta={
            "run_id": full["run_id"],
            "patent": dict(full["patent"]),
            "engine": {"commit": ""},
        },
        decompose=payload,
        read_runs=READ_RUNS,
        repo=REPO,
        source_digest=full["patent"]["source_digest"],
    )
    with open(paths.patent_md, encoding="utf-8") as handle:
        source_text = handle.read()

    def verdicts(spec: dict) -> tuple[dict[str, tuple], int]:
        rows_here = run_early_claim_checks(
            CheckContext(spec=spec, source_text=source_text, rules=m2.RULES)
        )
        return (
            {
                row.check_id: (
                    row.status,
                    row.checked,
                    row.violations,
                    sorted(finding.rule for finding in row.findings),
                )
                for row in rows_here
            },
            sum(row.checked for row in rows_here),
        )

    before, before_checked = verdicts(early)
    after, after_checked = verdicts(full)
    if before_checked == 0 or after_checked == 0:
        pytest.fail(f"'854 청구항 검사 대상이 비었다: early={before_checked}, final={after_checked}")
    if before != after:
        pytest.fail(f"'854 조기·최종 청구항 verdict 가 달라졌다: early={before}, final={after}")


def test_v6_repeat_signature_escalates_before_budget_exhaustion(tmp_path) -> None:
    """코드 결함의 같은 서명 재현을 즉시 진단하지 않으면 남은 출구 예산을 헛되이 태운다.

    국면 간 변이가 **코드 결함**이면 후속 재시도가 같은 실패를 재현하고, **그 재현 자체가
    진단**이므로 예산을 다 쓰기 전에 상신한다(재정 T16 §6 ⑤). 예산을 2로 올려 재는 이유는
    상한이 1이면 「서명 재현으로 멈춘 것」과 「예산이 떨어져 멈춘 것」이 구별되지 않기 때문이다.
    """
    law = m2.make_law_repo(os.path.join(str(tmp_path), "law"))
    # `run_read_stage(..., repo=law)` 는 요청 지문에 법 사본의 절차 본문을 인라인한다.
    # 소형 법 리포 하네스는 계약과 버전만 복사하므로, 이 실행에 필요한 절차도 같은 법에 둔다.
    shutil.copytree(
        os.path.join(REPO, "reader", "procedure"),
        os.path.join(law, "reader", "procedure"),
    )
    contract_path = os.path.join(law, "contracts", "stages", "read.yaml")
    with open(contract_path, encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    exit_points = [
        entry
        for entry in (raw.get("retry_budget") or {}).get("points") or []
        if isinstance(entry, dict) and entry.get("id") == "exit"
    ]
    if len(exit_points) != 1:
        pytest.fail(f"법 사본의 exit 판정점 기대 1개, 실제 {len(exit_points)}")
    exit_points[0]["max_retries"] = 2
    with open(contract_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(raw, handle, allow_unicode=True, sort_keys=False)
    m2.commit_law(law, "raise exit retry budget for T16 V-6")

    root, source_outcome = m2.run_source(tmp_path / "run", repo=law)
    if source_outcome["status"] != "ok":
        pytest.fail(f"법 사본 source status 기대 ok, 실제 {source_outcome['status']}")
    broken = m17.payloads_with_dangling_reference()
    lanes_root = m2.write_lane_responses(
        root,
        payloads_by_run={"read-a": broken, "read-b": m2.payload_set()},
        attempts=(0, 1, 2),
    )
    adapter = m2.ReplayLaneAdapter(lanes_root)
    outcome = m2.run_read_stage(run_root=root, adapter=adapter, rules=m2.RULES, repo=law)
    lane_ids = dispatched_ids(adapter)
    tail_attempts = retry_attempts(tail_lane_ids(lane_ids))
    if tail_attempts != {"retry-1"}:
        pytest.fail(f"후속 재시도 기대 정확히 1회, 실제 {sorted(tail_attempts)} — {lane_ids}")
    if outcome["status"] != "escalate":
        pytest.fail(f"같은 실패 서명 재현 status 기대 escalate, 실제 {outcome['status']}")
    law_contract = load_stage_contract("read", law)
    repeated = [
        entry
        for entry in law_contract.get("failure") or []
        if "같은 실패 서명" in str(entry.get("condition", ""))
    ]
    if len(repeated) != 1:
        pytest.fail(f"같은 실패 서명 조치 행 기대 1개, 실제 {len(repeated)}")
    expected_label = repeated[0].get("reason_label")
    if outcome.get("reason_label") != expected_label:
        pytest.fail(
            f"상신 라벨 기대 계약값 {expected_label!r}, 실제 {outcome.get('reason_label')!r}"
        )
    retry_two = [lane_id for lane_id in lane_ids if "/retry-2/" in lane_id]
    if retry_two:
        pytest.fail(f"같은 서명을 진단한 뒤 retry-2 를 발송했다: {retry_two}")


def test_feedback_does_not_leak_the_peer_run(tmp_path) -> None:
    """되먹임이 상대 산출을 누설하면 두 분해 실행의 독립성은 더 이상 성립하지 않는다.

    2회 독립은 "서로의 산출을 보지 않는다"는 뜻이다(SPEC §2.6 검사 4 보조 규정). 되먹임이
    그 구멍이 되면 두 실행은 더 이상 독립이 아니다(재정 T16 부속 5 · 계약
    `retry_budget.feedback_discipline`).
    """
    marker = "SENTINEL-READ-A-ONLY-8f31"
    read_a = m2.payload_set(note=marker)
    read_b_broken = phantom_dependent_payloads()
    if marker in m2.SOURCE or marker in json.dumps(read_b_broken, ensure_ascii=False):
        pytest.fail("비누설 표지가 원천 또는 read-b payload 에 이미 있다")
    root, outcome, adapter = run_with_payloads(
        tmp_path,
        per_attempt={
            0: {"read-a": read_a, "read-b": read_b_broken},
            1: {"read-a": m2.payload_set(), "read-b": m2.payload_set()},
        },
    )
    requests = [
        request
        for request in adapter.dispatched
        if request.lane_id == "read-b/decompose/retry-1/batch-0"
    ]
    if len(requests) != 1:
        pytest.fail(f"read-b 표적 재시도 요청 기대 1개, 실제 {len(requests)}")
    instructions = requests[0].instructions
    if marker in instructions:
        pytest.fail("read-b 되먹임에 read-a 전용 screening_memo 가 누설됐다")
    check_names = set(
        re.findall(r"^- `(read\.[^`]+)` /", instructions, flags=re.MULTILINE)
    )
    allowed = set(EARLY_CLAIM_CHECK_IDS)
    if not check_names:
        pytest.fail(f"재시도 결함 블록에 검사 이름이 없다: {instructions}")
    if not check_names <= allowed:
        pytest.fail(f"read-b 되먹임에 조기 청구항 검사 밖의 이름이 섞였다: {sorted(check_names)}")
    if "read.claim-inventory" not in check_names:
        pytest.fail(f"유령 종속항의 원인 검사 이름이 되먹임에 없다: {sorted(check_names)}")
    if outcome["status"] != "ok":
        pytest.fail(f"비누설 표본의 표적 재시도 뒤 status 기대 ok, 실제 {outcome['status']}")
    _ = root


def test_decompose_only_spec_matches_early_phase_contract() -> None:
    """분해 전용 명세를 성문화·대조하지 않으면 검사가 의도와 다른 인공물 위에서 돈다."""
    contract = load_stage_contract("read", None)
    declared = contract.get("early_phase_spec") or {}
    actual = decompose_only_spec(
        run_meta={
            "run_id": m2.RUN_ID,
            "patent": dict(m2.PATENT_META),
            "engine": {"commit": ""},
        },
        decompose=m2.decompose_payload(),
        read_runs=READ_RUNS,
        repo=REPO,
        source_digest="0" * 64,
    )
    missing = [key for key in declared.get("carries") or [] if key not in actual]
    if missing:
        pytest.fail(f"early_phase_spec.carries 중 실제 산출에 없는 키: {missing}")
    if actual.get("figures") != []:
        pytest.fail(f"분해 전용 figures 자리표시 기대 [], 실제 {actual.get('figures')!r}")
    drop_signal = ((actual.get("extensions") or {}).get("docent") or {}).get("drop_signal")
    if drop_signal != {}:
        pytest.fail(f"분해 전용 drop_signal 자리표시 기대 {{}}, 실제 {drop_signal!r}")
    payload_kinds = {item.get("kind") for item in m2.decompose_payload().get("items") or []}
    actual_kinds = {item.get("kind") for item in actual.get("items") or []}
    if actual_kinds != payload_kinds:
        pytest.fail(f"분해 전용 item kind 기대 {sorted(payload_kinds)}, 실제 {sorted(actual_kinds)}")
    forbidden = {"grounding", "fact", "implication", "positioning"} & actual_kinds
    if forbidden:
        pytest.fail(f"분해 전용 명세에 후속 kind 가 섞였다: {sorted(forbidden)}")

    for field in ("owner", "assembled_by"):
        reference = str(declared.get(field, ""))
        if "#" not in reference:
            pytest.fail(f"early_phase_spec.{field} 가 모듈#함수를 가리키지 않는다: {reference!r}")
        module_path, function_name = reference.split("#", 1)
        module_name = module_path.removesuffix(".py").replace("/", ".")
        module = importlib.import_module(module_name)
        target = getattr(module, function_name, None)
        if not callable(target):
            pytest.fail(f"early_phase_spec.{field} 대상 함수가 실재하지 않는다: {reference}")
    expected_checks = set(EARLY_CLAIM_CHECK_IDS) | {"read.convergence"}
    actual_checks = set(declared.get("judged_here") or [])
    if actual_checks != expected_checks:
        pytest.fail(f"조기 판정 검사 기대 {sorted(expected_checks)}, 실제 {sorted(actual_checks)}")


def test_claim_check_phase_meanings_and_exit_rows_are_declared() -> None:
    """두 실패의 뜻과 출구 행을 성문화하지 않으면 국면 간 변이의 유일한 탐지기가 사라진다."""
    contract = load_stage_contract("read", None)
    checks = contract.get("checks_before_exit") or []
    missing_exit = [entry.get("id") for entry in checks if "exit" not in (entry.get("phases") or [])]
    if missing_exit:
        pytest.fail(f"checks_before_exit 에 exit 국면이 없는 행: {missing_exit}")
    early_declared = {
        entry.get("id") for entry in checks if "early" in (entry.get("phases") or [])
    }
    if early_declared != set(EARLY_CLAIM_CHECK_IDS):
        pytest.fail(
            f"early phases 기대 {sorted(EARLY_CLAIM_CHECK_IDS)}, 실제 {sorted(early_declared)}"
        )
    by_id = {entry.get("id"): entry for entry in checks}
    for check_id in EARLY_CLAIM_CHECK_IDS:
        meaning = str(by_id.get(check_id, {}).get("phase_meaning", ""))
        if not meaning.strip():
            pytest.fail(f"{check_id}.phase_meaning 이 비었다")
        missing_terms = [term for term in ("분해 결함", "국면 간 변이") if term not in meaning]
        if missing_terms:
            pytest.fail(f"{check_id}.phase_meaning 에 뜻이 빠졌다: {missing_terms}")
    missing_from_exit = set(EARLY_CLAIM_CHECK_IDS) - set(READ_CHECK_IDS)
    if missing_from_exit:
        pytest.fail(f"조기 청구항 검사 출구 행이 사라졌다: {sorted(missing_from_exit)}")
