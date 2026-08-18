# -*- coding: utf-8 -*-
"""계기 정족수 판정 — 재정 2026-08-18 P-6 의 **집행 층**.

재정이 정한 것은 넷이다. **정족수 5/5**(유효 응답 = `probe.n` 전원) · **죽은 인스턴스만
재시도**(살아있는 응답 보존) · **상한 내 복구 실패 = 기계 강등 금지, Owner 상신**(대기 /
결측 진행 / 부분 인정, 뒤 둘은 육성 봉투) · **결측·부분 런은 계기 상관 점검 표본 제외**.
그 문언의 정본은 `contracts/parameters.yaml#instrument_quorum` 이고, 여기는 그 문언을
**실행하는 자리**다 — 감수(2026-08-18 P-6 "부분")가 지적한 것이 정확히 "문언은 옳은데
집행하는 모듈도 반증하는 시험도 없다"였다.

★ 구현 경계 — 무엇이 실물이고 무엇이 예정인가 (M1.5 시점, 2026-08-18)

  이 모듈은 **인스턴스 상태 목록을 받아 판정하는 결정론 순수 함수 층**이다. 그게 전부다.
  실제 계기 수집 경로 — 프로브 인스턴스를 띄우고, 응답을 거두고, 죽은 대를 다시 부르고,
  `60-probe/**` 를 쓰는 일 — 은 **아직 없다. M7 소관이다**(SPEC §8.4 M7). 여기 함수가
  있다고 해서 "계기가 돈다"고 말하지 마라. 상태 목록을 만들어 넣는 주체가 아직 없다.
  같은 규율의 선례 = `contracts/glossary.md` §2.2("여기 있는 id 를 '검사가 있다'고 말하지 마라").

  이 모듈은 **검사 id 를 발행하지 않는다.** 계기 정족수에 대응하는 검사 id 는 사전
  (`contracts/glossary.md` §2)에 등재된 것이 없고, 검사 id 신설은 Owner 재정 전용이다
  (헌장 규율 7). 판정 행(`verdict-check-row/v0`)을 쓰는 소비자는 등재 이후에 생긴다.

★ 왜 이 모듈에 "정족수를 낮추는 인자"가 하나도 없는가

  구 규칙 `min_effective_rule`(`ceil(probe.n / 2)`)이 폐기된 이유가 그 인자였다 — 과반만
  살아도 판정이 나왔고, 그 판정이 5대 판정과 **같은 이름으로** 기록되었다. 그래서 여기서는
  요구 대수(`required`)가 `probe.n` 에서만 오고 호출자가 건드릴 문이 없다. 상한을 소진해도
  낮아지지 않는다 — 소진의 처분은 강등이 아니라 상신이다. 계약의 `on_exhausted` 가
  `owner-escalation` 이 아니면 로드 자체가 실패한다(순종하지 않고 넘어진다).

  같은 이유로 **선택지를 고르는 코드가 여기 없다.** `EscalationForm` 은 세 선택지를 전부
  실은 서식이며, 그중 하나를 지목하는 필드가 없다. 고르는 것은 Owner 다(D9 — 구속력 있는
  결정은 재정뿐).

`assert` 를 쓰지 않는다(`python3 -O` 에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import yaml

# engine/quorum.py → 리포 루트
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_PARAMETERS = ("contracts", "parameters.yaml")
_CONTRACT_LINE = "parameters/v0"

# 인스턴스 상태 2종. 지표 원장의 `collected`·`not-collected` 를 빌려 쓰지 않는 이유는
# 그 어휘가 **뜨지 않기로 한 관측**(미수집)을 가리키기 때문이다 — 죽은 계기는 결측이지
# 미수집이 아니다. 셋을 한 이름으로 뭉개지 말라는 것이 `metrics-row/v0` 규율 (4)의 요지다.
LIVE = "live"
DEAD = "dead"
_STATES = (LIVE, DEAD)

# 판정 3종. `retry`·`escalate` 는 사전 §4 "실패 조치"의 기존 어휘이며,
# `satisfied` 는 실패 조치가 아니라 정족수가 선 상태의 이름이다.
SATISFIED = "satisfied"
RETRY = "retry"
ESCALATE = "escalate"

RULING = "재정 2026-08-18 P-6"

# 상신 사유 문구. 사전 §4 의 "escalate 사유" 닫힌 집합에 계기 정족수 항목이 **아직 없다** —
# 등재는 재정 전용이므로(헌장 규율 7) 여기서는 토큰을 만들지 않고 서술 문구만 싣는다.
ESCALATION_REASON = "계기 정족수 미달 — 죽은 인스턴스 재시도 상한 소진"


class QuorumContractError(Exception):
    """계약(`contracts/parameters.yaml#instrument_quorum`)이 없거나 판정을 세울 수 없는 모양이다.

    조용히 기본값으로 때우지 않는다. 기본값을 코드가 들고 있으면 그 순간 정족수의 진원이
    둘이 되고, 둘 중 하나는 반드시 낡는다.
    """


class RosterError(Exception):
    """건네받은 인스턴스 대장이 판정의 전제를 깨뜨렸다(대수 불일치·중복 id·상태 모순)."""


# ---------------------------------------------------------------------------
# 계약 로드
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QuorumPolicy:
    """계약에서 읽어 온 정족수 규율. **이 객체 밖에 수치가 없다.**"""

    required: int                                   # = adjustable["probe.n"]
    max_attempts: int                               # = instrument_quorum.dead_instance_retry.max_attempts
    options: tuple[str, ...]                        # Owner 선택지(순서 보존 — 재정 원문 순서)
    voice_envelope_options: frozenset[str]          # 육성 봉투가 필요한 선택지
    correlation_excluded_terminals: frozenset[str]  # 상관 표본에서 빠지는 종결 상태
    rule: str                                       # 규율 문언 원문
    options_note: str                               # 육성 봉투 안내 원문
    exclusion_note: str                             # 표본 제외 문언 원문
    ruling: str
    source: str                                     # 읽어 온 계약 파일 경로


def _require(mapping: Any, key: str, where: str) -> Any:
    if not isinstance(mapping, dict) or key not in mapping:
        raise QuorumContractError(f"{where} 에 {key} 선언이 없다 — {RULING} 의 집행 전제가 빠졌다")
    return mapping[key]


def load_policy(repo: str | None = None) -> QuorumPolicy:
    """`contracts/parameters.yaml` 에서 정족수 규율을 읽는다.

    ★ 검증을 로드 시점에 몰아 두는 이유. 이 모듈이 잘못 쓰이는 가장 그럴듯한 경로는
    "계약이 조금 다른 모양인데 코드가 알아서 참는 것"이다. 참으면 그 런은 재정과 다른
    규율로 돌고, 로그에는 정상으로 남는다. 그래서 여기서 넘어진다.
    """
    target = os.path.join(repo or _REPO_ROOT, *_PARAMETERS)
    try:
        with open(target, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise QuorumContractError(f"조정 가능 파라미터 계약이 없다: {target}") from exc
    if not isinstance(data, dict):
        raise QuorumContractError(f"계약 최상위가 매핑이 아니다: {target}")
    if data.get("schema") != _CONTRACT_LINE:
        raise QuorumContractError(
            f"계약 라인이 {_CONTRACT_LINE} 가 아니다: {data.get('schema')!r} ({target})"
        )

    adjustable = _require(data, "adjustable", target)
    probe_n = _require(adjustable, "probe.n", f"{target}#adjustable")
    if not isinstance(probe_n, int) or isinstance(probe_n, bool) or probe_n < 1:
        raise QuorumContractError(f"probe.n 이 양의 정수가 아니다: {probe_n!r}")

    quorum = _require(data, "instrument_quorum", target)
    where = f"{target}#instrument_quorum"

    # 강등 금지의 **로드 시점 집행**. 다른 값이 적혀 있으면 순종하지 않고 넘어진다 —
    # 재정이 금지한 처분을 계약 오기 한 줄로 되살릴 수 있으면 금지가 아니다.
    on_exhausted = _require(quorum, "on_exhausted", where)
    if on_exhausted != "owner-escalation":
        raise QuorumContractError(
            f"on_exhausted 가 owner-escalation 이 아니다: {on_exhausted!r} — "
            f"상한 소진의 처분은 기계 강등이 아니라 Owner 상신이다({RULING})"
        )

    retry_block = _require(quorum, "dead_instance_retry", where)
    max_attempts = _require(retry_block, "max_attempts", f"{where}.dead_instance_retry")
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 0:
        raise QuorumContractError(f"max_attempts 가 0 이상의 정수가 아니다: {max_attempts!r}")

    options = _require(quorum, "owner_options", where)
    if not isinstance(options, list) or not options or not all(
        isinstance(item, str) and item for item in options
    ):
        raise QuorumContractError(f"owner_options 가 비어 있지 않은 문자열 목록이 아니다: {options!r}")
    options_tuple = tuple(options)
    if len(set(options_tuple)) != len(options_tuple):
        raise QuorumContractError(f"owner_options 에 중복이 있다: {options!r}")

    voice = _subset(quorum, "owner_options_requiring_voice_envelope", options_tuple, where)
    excluded = _subset(quorum, "correlation_excluded_terminals", options_tuple, where)

    return QuorumPolicy(
        required=probe_n,
        max_attempts=max_attempts,
        options=options_tuple,
        voice_envelope_options=voice,
        correlation_excluded_terminals=excluded,
        rule=str(_require(quorum, "rule", where)),
        options_note=str(_require(quorum, "owner_options_note", where)),
        exclusion_note=str(_require(quorum, "excluded_from_correlation", where)),
        ruling=str(quorum.get("ruling", RULING)),
        source=target,
    )


def _subset(quorum: dict, key: str, options: tuple[str, ...], where: str) -> frozenset[str]:
    """선택지 부분집합 선언을 읽는다 — 산문(`*_note`)에서 이름을 긁어내지 않는다.

    산문 파싱을 피하는 이유는 문장이 다듬어지는 날 코드가 조용히 틀리기 때문이다.
    """
    value = _require(quorum, key, where)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise QuorumContractError(f"{key} 가 문자열 목록이 아니다: {value!r}")
    unknown = [item for item in value if item not in options]
    if unknown:
        raise QuorumContractError(f"{key} 에 owner_options 밖의 값이 있다: {unknown!r}")
    return frozenset(value)


# ---------------------------------------------------------------------------
# 인스턴스 대장
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Instance:
    """계기 1대의 관측 상태.

    `state` 와 `response` 를 따로 적게 두면 "살아있다고 적힌 빈 응답"이 생긴다 —
    그 행 하나가 정족수를 소리 없이 채운다. 그래서 둘의 결속을 생성 시점에 강제한다.
    """

    instance_id: str
    state: str
    response: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.instance_id, str) or not self.instance_id:
            raise RosterError(f"instance_id 가 비어 있다: {self.instance_id!r}")
        if self.state not in _STATES:
            raise RosterError(f"알 수 없는 상태: {self.state!r} (허용 = {_STATES})")
        if self.state == LIVE and self.response is None:
            raise RosterError(
                f"{self.instance_id}: live 인데 응답이 없다 — 응답 없는 대는 정족수를 채우지 못한다"
            )
        if self.state == DEAD and self.response is not None:
            raise RosterError(
                f"{self.instance_id}: dead 인데 응답을 들고 있다 — 죽음과 결측을 갈라 적어라"
            )


def _validated_roster(instances: Iterable[Instance], policy: QuorumPolicy) -> tuple[Instance, ...]:
    roster = tuple(instances)
    for item in roster:
        if not isinstance(item, Instance):
            raise RosterError(f"대장 항목이 Instance 가 아니다: {item!r}")
    ids = [item.instance_id for item in roster]
    if len(set(ids)) != len(ids):
        raise RosterError(f"대장에 중복 instance_id 가 있다: {ids!r}")
    if len(roster) != policy.required:
        # 빠진 행과 죽은 행은 다르다. 행이 없으면 대장이 사실 대신 **침묵**을 담고,
        # 침묵은 세지지 않으므로 4대 대장이 4/4 로 통과해 버린다.
        raise RosterError(
            f"대장이 {len(roster)}대인데 정족수 기준은 {policy.required}대다 — "
            f"부르지 못한 대도 dead 로 적어라(빠진 행은 결측이 아니라 침묵이다)"
        )
    return roster


# ---------------------------------------------------------------------------
# 판정 산출물
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RetryPlan:
    """재시도 1회의 계획. `targets` 는 **죽은 인스턴스만**이고 `preserved` 는 손대지 않을 대다."""

    attempt_no: int
    remaining_attempts: int
    targets: tuple[str, ...]
    preserved: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "attempt_no": self.attempt_no,
            "remaining_attempts": self.remaining_attempts,
            "targets": list(self.targets),
            "preserved": list(self.preserved),
        }


@dataclass(frozen=True)
class EscalationOption:
    """Owner 선택지 1개. **고른 흔적을 담는 필드가 없다** — 고르는 것은 Owner 다."""

    label: str
    voice_envelope_required: bool
    correlation_excluded: bool

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "voice_envelope_required": self.voice_envelope_required,
            "correlation_excluded": self.correlation_excluded,
        }


@dataclass(frozen=True)
class EscalationForm:
    """상신 서식. 세 선택지를 **전부** 싣고, 어느 것도 지목하지 않는다."""

    to: str
    ruling: str
    reason: str
    rule: str
    required: int
    live_count: int
    dead_count: int
    dead_instances: tuple[str, ...]
    attempts_made: int
    options: tuple[EscalationOption, ...]
    options_note: str

    def to_dict(self) -> dict:
        return {
            "to": self.to,
            "ruling": self.ruling,
            "reason": self.reason,
            "rule": self.rule,
            "required": self.required,
            "live_count": self.live_count,
            "dead_count": self.dead_count,
            "dead_instances": list(self.dead_instances),
            "attempts_made": self.attempts_made,
            "options": [option.to_dict() for option in self.options],
            "options_note": self.options_note,
        }


@dataclass(frozen=True)
class QuorumDecision:
    """정족수 판정 1회.

    `required` 는 언제나 `probe.n` 이다 — 상한을 소진해도, 몇 대가 죽어도 변하지 않는다.
    이 필드가 입력에 따라 흔들리는 순간 폐기된 과반 규칙이 이름만 바꿔 되살아난다.
    """

    outcome: str
    required: int
    live_count: int
    dead_count: int
    live_instances: tuple[str, ...]
    dead_instances: tuple[str, ...]
    attempts_made: int
    max_attempts: int
    rationale: str
    ruling: str
    retry_plan: RetryPlan | None = None
    escalation: EscalationForm | None = None

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "required": self.required,
            "live_count": self.live_count,
            "dead_count": self.dead_count,
            "live_instances": list(self.live_instances),
            "dead_instances": list(self.dead_instances),
            "attempts_made": self.attempts_made,
            "max_attempts": self.max_attempts,
            "rationale": self.rationale,
            "ruling": self.ruling,
            "retry_plan": self.retry_plan.to_dict() if self.retry_plan else None,
            "escalation": self.escalation.to_dict() if self.escalation else None,
        }


# ---------------------------------------------------------------------------
# ① 정족수 판정
# ---------------------------------------------------------------------------


def evaluate(
    instances: Iterable[Instance],
    *,
    attempts_made: int = 0,
    policy: QuorumPolicy | None = None,
    repo: str | None = None,
) -> QuorumDecision:
    """정족수를 판정한다 — `satisfied` / `retry` / `escalate` 중 하나.

    인자에 "요구 대수"가 없는 것이 이 함수의 요점이다. 요구 대수는 계약에서만 온다.
    """
    policy = policy or load_policy(repo)
    if not isinstance(attempts_made, int) or isinstance(attempts_made, bool) or attempts_made < 0:
        raise RosterError(f"attempts_made 가 0 이상의 정수가 아니다: {attempts_made!r}")
    roster = _validated_roster(instances, policy)

    live = tuple(item.instance_id for item in roster if item.state == LIVE)
    dead = tuple(item.instance_id for item in roster if item.state == DEAD)
    common = dict(
        required=policy.required,
        live_count=len(live),
        dead_count=len(dead),
        live_instances=live,
        dead_instances=dead,
        attempts_made=attempts_made,
        max_attempts=policy.max_attempts,
        ruling=policy.ruling,
    )

    if not dead:
        return QuorumDecision(
            outcome=SATISFIED,
            rationale=f"유효 응답 {len(live)}/{policy.required} — 정족수 충족({policy.rule})",
            **common,
        )

    if attempts_made < policy.max_attempts:
        return QuorumDecision(
            outcome=RETRY,
            rationale=(
                f"유효 응답 {len(live)}/{policy.required} — 죽은 {len(dead)}대만 다시 부른다"
                f"(시도 {attempts_made + 1}/{policy.max_attempts}). 살아있는 응답은 재요청 대상이 아니다"
            ),
            retry_plan=RetryPlan(
                attempt_no=attempts_made + 1,
                remaining_attempts=policy.max_attempts - attempts_made,
                targets=dead,
                preserved=live,
            ),
            **common,
        )

    return QuorumDecision(
        outcome=ESCALATE,
        rationale=(
            f"유효 응답 {len(live)}/{policy.required} — 재시도 상한 {policy.max_attempts}회를 소진했다. "
            f"정족수를 낮추지 않고 Owner 에게 상신한다({policy.ruling})"
        ),
        escalation=_escalation_form(policy, live, dead, attempts_made),
        **common,
    )


def _escalation_form(
    policy: QuorumPolicy,
    live: tuple[str, ...],
    dead: tuple[str, ...],
    attempts_made: int,
) -> EscalationForm:
    return EscalationForm(
        to="owner",
        ruling=policy.ruling,
        reason=ESCALATION_REASON,
        rule=policy.rule,
        required=policy.required,
        live_count=len(live),
        dead_count=len(dead),
        dead_instances=dead,
        attempts_made=attempts_made,
        options=tuple(
            EscalationOption(
                label=label,
                voice_envelope_required=label in policy.voice_envelope_options,
                correlation_excluded=label in policy.correlation_excluded_terminals,
            )
            for label in policy.options
        ),
        options_note=policy.options_note,
    )


# ---------------------------------------------------------------------------
# ② 재시도 결과 반영 — 살아있는 응답의 보존
# ---------------------------------------------------------------------------


def apply_attempt(
    instances: Iterable[Instance],
    results: Mapping[str, str | None],
    *,
    policy: QuorumPolicy | None = None,
    repo: str | None = None,
) -> tuple[Instance, ...]:
    """재시도 1회의 결과를 대장에 반영한 **새 대장**을 낸다.

    `results` = {죽은 인스턴스 id: 새 응답 또는 None(이번에도 죽었다)}.

    ★ 살아있는 항목은 새 객체로 다시 만들지도 않는다 — 원래 객체를 **그대로** 옮긴다.
    같은 값으로 재구성하는 것도 "갈아치우지 않았다"의 증명으로는 약하다: 재구성 경로가
    있으면 언젠가 그 경로에 값이 실린다. 살아있는 id 가 `results` 에 나타나면 그 자체가
    결함이므로 반영하지 않고 넘어진다.
    """
    policy = policy or load_policy(repo)
    roster = _validated_roster(instances, policy)
    by_id = {item.instance_id: item for item in roster}

    unknown = [key for key in results if key not in by_id]
    if unknown:
        raise RosterError(f"대장에 없는 인스턴스의 재시도 결과다: {unknown!r}")
    trespass = [key for key in results if by_id[key].state == LIVE]
    if trespass:
        raise RosterError(
            f"살아있는 인스턴스를 재시도 결과로 덮으려 한다: {trespass!r} — "
            f"재시도 대상은 죽은 인스턴스만이다({RULING})"
        )

    updated: list[Instance] = []
    for item in roster:
        if item.instance_id not in results:
            updated.append(item)          # 살아있는 대·이번에 부르지 않은 대 = 원 객체 그대로
            continue
        response = results[item.instance_id]
        if response is None:
            updated.append(item)          # 이번에도 죽었다 — 상태가 바뀌지 않는다
        else:
            updated.append(Instance(item.instance_id, LIVE, response))
    return tuple(updated)


# ---------------------------------------------------------------------------
# ④ 상관 표본 제외 플래그 (런 단위)
# ---------------------------------------------------------------------------


def correlation_sample_flag(
    run_id: str,
    *,
    outcome: str,
    owner_option: str | None = None,
    policy: QuorumPolicy | None = None,
    repo: str | None = None,
) -> dict:
    """이 런이 계기 상관 점검(SPEC §5.8)의 표본에 드는가를 런 단위로 산출한다.

    ★ `outcome` 이 `escalate` 면 `owner_option` 없이는 답이 없다 — 상신 중인 런은 아직
    종결하지 않았고, 종결하지 않은 런에 "표본에 든다/안 든다"를 미리 적으면 그 값이
    Owner 재정을 앞질러 버린다. 그래서 답하지 않고 넘어진다.
    """
    policy = policy or load_policy(repo)
    if not isinstance(run_id, str) or not run_id:
        raise RosterError(f"run_id 가 비어 있다: {run_id!r}")

    if outcome == SATISFIED:
        if owner_option is not None:
            raise RosterError(
                f"정족수를 채운 런에 Owner 선택지가 붙었다: {owner_option!r} — 상신이 없었다"
            )
        excluded = False
        basis = "정족수 충족 런 — 온전한 관측이므로 표본에 든다"
    elif outcome == ESCALATE:
        if owner_option is None:
            raise RosterError(
                f"{run_id}: 상신 중인 런은 아직 종결하지 않았다 — Owner 선택 후에 다시 물어라"
            )
        if owner_option not in policy.options:
            raise RosterError(
                f"계약에 없는 Owner 선택지다: {owner_option!r} (허용 = {list(policy.options)})"
            )
        if owner_option not in policy.correlation_excluded_terminals:
            # 예: '대기'. 기다렸다가 정족수를 채우면 그 런은 온전한 관측이고,
            # 못 채우면 다시 상신이 온다 — 어느 쪽이든 여기서 종결을 선언할 자리가 아니다.
            raise RosterError(
                f"{owner_option!r} 는 종결 상태가 아니다 — 표본 판정은 종결한 런에만 붙는다"
            )
        excluded = True
        basis = policy.exclusion_note
    else:
        raise RosterError(
            f"표본 판정을 붙일 수 없는 판정이다: {outcome!r} — 런이 아직 진행 중이다"
        )

    return {
        "run_id": run_id,
        "excluded_from_correlation": excluded,
        "outcome": outcome,
        "owner_option": owner_option,
        "basis": basis,
        "ruling": policy.ruling,
    }
