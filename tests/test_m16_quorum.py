# -*- coding: utf-8 -*-
"""계기 정족수 판정의 반증 시험 — 재정 2026-08-18 P-6.

감수(2026-08-18, P-6 "부분")가 남긴 지적은 하나였다: **문언은 옳은데 그것을 집행하는 모듈도,
집행을 반증하는 시험도 없다.** 이 파일이 그 뒤쪽을 맡는다. 그래서 여기서 확인하는 것은
"함수가 돌아간다"가 아니라 **재정이 금지한 일이 일어나지 않는다**이다 —

  · 4/5 로는 정족수가 서지 않는다(기계 강등의 부재)
  · 재시도가 살아있는 응답에 닿지 않는다(보존의 부재 아닌 존재)
  · 상한 소진 산출에 선택지를 고른 흔적이 없다(자동 결정의 부재)
  · 수치가 코드가 아니라 계약에서 온다(사본의 부재)

`assert` 를 쓴다 — pytest 가 AST 를 재작성하므로 `PYTHONOPTIMIZE=1` 에서도 살아남는다
(CLAUDE.md §3, 2026-08-18 실측 확정). 서브프로세스는 쓰지 않는다.

★ 이 시험이 덮지 않는 것: 실제 계기 수집·인스턴스 구동은 M7 소관이며 아직 없다.
여기서 다루는 대장(roster)은 전부 시험이 손으로 만든 것이다.
"""

from __future__ import annotations

import os
import sys

import pytest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.quorum import (  # noqa: E402
    DEAD,
    ESCALATE,
    LIVE,
    RETRY,
    SATISFIED,
    Instance,
    QuorumContractError,
    RosterError,
    apply_attempt,
    correlation_sample_flag,
    evaluate,
    load_policy,
)

CONTRACT_REL = os.path.join("contracts", "parameters.yaml")


# ---------------------------------------------------------------------------
# 픽스처 — 대장 만들기 · 계약 갈아 끼우기
# ---------------------------------------------------------------------------


def roster(dead_count: int, total: int = 5) -> list[Instance]:
    """앞쪽 `dead_count` 대가 죽은 `total` 대 대장. 응답 문자열은 id 로 구별한다."""
    made = []
    for index in range(1, total + 1):
        if index <= dead_count:
            made.append(Instance(f"probe-{index}", DEAD))
        else:
            made.append(Instance(f"probe-{index}", LIVE, f"응답 본문 {index}"))
    return made


def contract_repo(tmp_path, mutate) -> str:
    """실계약을 복사해 `mutate` 로 고친 임시 리포를 만든다.

    실계약을 출발점으로 삼는 이유 — 시험이 손으로 지은 계약을 읽으면, 실계약의 키 이름이
    바뀌는 날 시험만 계속 통과한다.
    """
    with open(os.path.join(REPO, CONTRACT_REL), encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    mutate(data)
    target_dir = tmp_path / "contracts"
    target_dir.mkdir(parents=True, exist_ok=True)
    with open(target_dir / "parameters.yaml", "w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
    return str(tmp_path)


@pytest.fixture(scope="module")
def policy():
    return load_policy()


# ---------------------------------------------------------------------------
# 계약 로드 — 판정의 전제
# ---------------------------------------------------------------------------


def test_policy_reads_the_real_contract(policy):
    """정족수의 요구 대수는 `probe.n` 이고, 상한은 계약이 든다."""
    assert policy.required == 5
    assert policy.max_attempts >= 0
    assert policy.options == ("대기", "결측 진행", "부분 인정")
    assert policy.voice_envelope_options == frozenset({"결측 진행", "부분 인정"})
    assert policy.correlation_excluded_terminals == frozenset({"결측 진행", "부분 인정"})


def test_load_refuses_machine_downgrade_in_contract(tmp_path):
    """계약이 `on_exhausted` 를 강등으로 바꿔 적으면 **순종하지 않고 넘어진다**.

    재정이 금지한 처분을 계약 오기 한 줄로 되살릴 수 있으면 그것은 금지가 아니다.
    """

    def mutate(data):
        data["instrument_quorum"]["on_exhausted"] = "machine-downgrade"

    repo = contract_repo(tmp_path, mutate)
    with pytest.raises(QuorumContractError) as caught:
        load_policy(repo)
    assert "owner-escalation" in str(caught.value)


# ---------------------------------------------------------------------------
# 시험 1·2 — 5/5 는 완전 일치다
# ---------------------------------------------------------------------------


def test_1_full_roster_is_satisfied(policy):
    decision = evaluate(roster(0), policy=policy)
    assert decision.outcome == SATISFIED
    assert (decision.live_count, decision.dead_count) == (5, 0)
    assert decision.required == 5
    assert decision.retry_plan is None and decision.escalation is None


def test_2_four_of_five_is_not_satisfied(policy):
    """4/5 는 만족이 아니다 — 기계 강등의 직접 반증."""
    decision = evaluate(roster(1), policy=policy)
    assert decision.outcome != SATISFIED
    assert decision.outcome in (RETRY, ESCALATE)
    assert decision.live_count == 4
    assert decision.required == 5          # 요구 대수는 죽은 대수에 반응하지 않는다


@pytest.mark.parametrize("dead_count", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("attempts_made", [0, 1, 2, 3, 7])
def test_2b_no_shortfall_ever_satisfies(policy, dead_count, attempts_made):
    """죽은 대가 하나라도 있으면 어떤 시도 횟수에서도 `satisfied` 가 나오지 않는다."""
    decision = evaluate(roster(dead_count), attempts_made=attempts_made, policy=policy)
    assert decision.outcome != SATISFIED
    assert decision.required == policy.required


def test_2c_short_roster_is_refused(policy):
    """4대짜리 대장은 4/4 로 통과하지 않는다 — 빠진 행은 결측이 아니라 침묵이다."""
    with pytest.raises(RosterError) as caught:
        evaluate(roster(0, total=4), policy=policy)
    assert "5대" in str(caught.value)


def test_2d_live_without_response_is_refused():
    """'살아있다'고 적힌 빈 응답이 정족수를 채우는 경로를 생성 시점에 막는다."""
    with pytest.raises(RosterError):
        Instance("probe-1", LIVE, None)
    with pytest.raises(RosterError):
        Instance("probe-2", DEAD, "응답 본문")


# ---------------------------------------------------------------------------
# 시험 3·4 — 죽은 것만, 살아있는 것은 보존
# ---------------------------------------------------------------------------


def test_3_retry_targets_exactly_the_dead(policy):
    decision = evaluate(roster(2), policy=policy)
    assert decision.outcome == RETRY
    plan = decision.retry_plan
    assert plan is not None
    assert plan.targets == ("probe-1", "probe-2")
    assert plan.preserved == ("probe-3", "probe-4", "probe-5")
    assert set(plan.targets) & set(plan.preserved) == set()
    assert plan.attempt_no == 1


def test_4_live_responses_survive_the_attempt_byte_identical(policy):
    """재시도 왕복 후 살아있는 응답이 **바이트 동일**하다 — 보존의 반증."""
    before = roster(2)
    live_before = {item.instance_id: item.response for item in before if item.state == LIVE}

    after = apply_attempt(before, {"probe-1": "복구된 응답 1", "probe-2": None}, policy=policy)

    live_after = {item.instance_id: item.response for item in after if item.state == LIVE}
    for instance_id, text in live_before.items():
        assert live_after[instance_id] == text
        assert live_after[instance_id].encode("utf-8") == text.encode("utf-8")

    # 값이 같은 새 객체로 다시 지어진 것도 아니다 — 원 객체가 그대로 옮겨진다.
    by_id_before = {item.instance_id: item for item in before}
    for item in after:
        if item.instance_id in live_before:
            assert item is by_id_before[item.instance_id]

    # 죽은 쪽만 움직였다: 복구된 1대는 live, 여전히 죽은 1대는 dead.
    states = {item.instance_id: item.state for item in after}
    assert states["probe-1"] == LIVE
    assert states["probe-2"] == DEAD


def test_4b_overwriting_a_live_instance_is_refused(policy):
    """살아있는 id 를 재시도 결과에 실으면 반영하지 않고 넘어진다."""
    with pytest.raises(RosterError) as caught:
        apply_attempt(roster(2), {"probe-5": "갈아치운 응답"}, policy=policy)
    assert "probe-5" in str(caught.value)


def test_4c_recovered_roster_satisfies(policy):
    """2대를 다 살리면 그때 비로소 5/5 다."""
    after = apply_attempt(
        roster(2), {"probe-1": "복구 1", "probe-2": "복구 2"}, policy=policy
    )
    assert evaluate(after, attempts_made=1, policy=policy).outcome == SATISFIED


# ---------------------------------------------------------------------------
# 시험 5 — 상한 소진 = Owner 상신
# ---------------------------------------------------------------------------


def test_5_exhausted_escalates_with_all_three_options(policy):
    decision = evaluate(roster(1), attempts_made=policy.max_attempts, policy=policy)
    assert decision.outcome == ESCALATE
    assert decision.retry_plan is None

    form = decision.escalation
    assert form is not None
    assert form.to == "owner"
    assert [option.label for option in form.options] == ["대기", "결측 진행", "부분 인정"]

    envelope = {option.label: option.voice_envelope_required for option in form.options}
    assert envelope == {"대기": False, "결측 진행": True, "부분 인정": True}

    assert "육성 봉투" in form.options_note
    assert form.dead_instances == ("probe-1",)


# ---------------------------------------------------------------------------
# 시험 6 — 강등·자동 선택 경로의 **부재**
# ---------------------------------------------------------------------------


# 자동 결정을 담을 법한 키 이름들. 하나라도 산출에 나타나면 그 자체가 결함이다.
FORBIDDEN_KEYS = {
    "verdict",
    "decision",
    "decided",
    "chosen",
    "choice",
    "selected",
    "selection",
    "resolution",
    "effective_quorum",
    "effective_required",
    "min_effective",
    "quorum_override",
    "downgrade",
    "degraded",
    "pass",
    "fail",
}


def _walk(node, keys, strings, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            keys.add(key)
            _walk(value, keys, strings, path + (key,))
    elif isinstance(node, list):
        for value in node:
            _walk(value, keys, strings, path)
    elif isinstance(node, str):
        strings.append((path, node))


@pytest.mark.parametrize("dead_count", [0, 1, 2, 3, 4, 5])
@pytest.mark.parametrize("attempts_made", [0, 1, 2, 3, 9])
def test_6_no_downgrade_and_no_auto_choice(policy, dead_count, attempts_made):
    """어떤 입력으로도 정족수가 낮아지지 않고, 선택지가 골라지지 않는다."""
    decision = evaluate(roster(dead_count), attempts_made=attempts_made, policy=policy)
    payload = decision.to_dict()

    # ① 요구 대수는 언제나 계약값이다.
    assert payload["required"] == policy.required
    assert decision.live_count + decision.dead_count == policy.required

    # ② `satisfied` 는 결원이 0 일 때만 나온다.
    assert (payload["outcome"] == SATISFIED) == (dead_count == 0)

    keys, strings = set(), []
    _walk(payload, keys, strings)

    # ③ 자동 결정을 담을 법한 키가 없다.
    assert keys & FORBIDDEN_KEYS == set()

    # ④ 선택지 이름이 등장하는 자리는 **선택지 목록 안뿐**이다. 다른 어느 자리에서도
    #    특정 선택지가 지목되지 않는다("고른 흔적"의 부재).
    option_labels = set(policy.options)
    for path, text in strings:
        if path[-2:] == ("options", "label"):
            continue
        assert text not in option_labels, f"{path} 가 선택지를 지목했다: {text}"

    # ⑤ 상신 서식은 세 선택지를 **전부** 싣는다(하나를 빼는 것도 고르는 일이다).
    if payload["escalation"] is not None:
        labels = [option["label"] for option in payload["escalation"]["options"]]
        assert labels == list(policy.options)


def test_6b_caller_cannot_pass_a_lower_quorum(policy):
    """호출자가 요구 대수를 건네는 문이 없다 — 폐기된 과반 규칙의 재입장 경로 차단."""
    with pytest.raises(TypeError):
        evaluate(roster(2), required=3, policy=policy)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# 시험 7 — 상관 표본 제외 플래그 (런 단위)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("option", ["결측 진행", "부분 인정"])
def test_7_missing_or_partial_run_is_excluded(policy, option):
    flag = correlation_sample_flag(
        "openai-us20260147854a1-cim-fp-2", outcome=ESCALATE, owner_option=option, policy=policy
    )
    assert flag["excluded_from_correlation"] is True
    assert flag["owner_option"] == option
    assert flag["run_id"] == "openai-us20260147854a1-cim-fp-2"


def test_7b_normal_run_is_not_excluded(policy):
    """정상 종결 런에는 플래그가 서지 않는다 — 과잉 제외의 반증."""
    flag = correlation_sample_flag("정상-런-1", outcome=SATISFIED, policy=policy)
    assert flag["excluded_from_correlation"] is False
    assert flag["owner_option"] is None


def test_7c_unresolved_escalation_has_no_flag(policy):
    """상신 중인 런에는 답이 없다 — 미리 적으면 그 값이 Owner 재정을 앞지른다."""
    with pytest.raises(RosterError):
        correlation_sample_flag("상신-중-런", outcome=ESCALATE, policy=policy)
    with pytest.raises(RosterError):
        correlation_sample_flag("재시도-중-런", outcome=RETRY, policy=policy)


def test_7d_waiting_is_not_a_terminal(policy):
    """'대기'는 종결이 아니다 — 표본 판정은 종결한 런에만 붙는다."""
    with pytest.raises(RosterError) as caught:
        correlation_sample_flag("대기-런", outcome=ESCALATE, owner_option="대기", policy=policy)
    assert "종결" in str(caught.value)


# ---------------------------------------------------------------------------
# 시험 8 — 수치가 계약에서 온다
# ---------------------------------------------------------------------------


def test_8_max_attempts_comes_from_the_contract(tmp_path):
    """계약의 상한을 바꾸면 같은 입력의 판정이 따라 바뀐다(코드에 숫자가 없다)."""

    def to_zero(data):
        data["instrument_quorum"]["dead_instance_retry"]["max_attempts"] = 0

    def to_five(data):
        data["instrument_quorum"]["dead_instance_retry"]["max_attempts"] = 5

    zero_repo = load_policy(contract_repo(tmp_path / "zero", to_zero))
    five_repo = load_policy(contract_repo(tmp_path / "five", to_five))

    # 상한 0 = 재시도 없이 곧장 상신.
    first = evaluate(roster(1), attempts_made=0, policy=zero_repo)
    assert first.outcome == ESCALATE

    # 상한 5 = 실계약(2)이라면 상신이었을 자리에서 아직 재시도.
    second = evaluate(roster(1), attempts_made=2, policy=five_repo)
    assert second.outcome == RETRY
    assert second.retry_plan.remaining_attempts == 3


def test_8b_probe_n_drives_the_quorum(tmp_path):
    """정족수 대수도 계약(`probe.n`)에서 온다 — 5 가 코드에 박혀 있지 않다."""

    def to_three(data):
        data["adjustable"]["probe.n"] = 3

    three = load_policy(contract_repo(tmp_path / "three", to_three))
    assert three.required == 3
    assert evaluate(roster(0, total=3), policy=three).outcome == SATISFIED
    with pytest.raises(RosterError):
        evaluate(roster(0, total=5), policy=three)


def test_8c_option_set_comes_from_the_contract(tmp_path):
    """육성 봉투 대상도 계약 선언에서 온다 — 코드가 선택지 이름을 알지 못한다."""

    def envelope_all(data):
        data["instrument_quorum"]["owner_options_requiring_voice_envelope"] = [
            "대기",
            "결측 진행",
            "부분 인정",
        ]

    policy = load_policy(contract_repo(tmp_path / "all", envelope_all))
    decision = evaluate(roster(1), attempts_made=policy.max_attempts, policy=policy)
    assert all(option.voice_envelope_required for option in decision.escalation.options)


def test_8d_unknown_option_in_expansion_is_refused(tmp_path):
    """전개 목록이 선택지 밖의 이름을 들면 로드가 넘어진다(전개와 문언의 어긋남)."""

    def stray(data):
        data["instrument_quorum"]["correlation_excluded_terminals"] = ["결측 진행", "적당히 진행"]

    with pytest.raises(QuorumContractError) as caught:
        load_policy(contract_repo(tmp_path / "stray", stray))
    assert "적당히 진행" in str(caught.value)
