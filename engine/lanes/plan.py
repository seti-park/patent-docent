# -*- coding: utf-8 -*-
"""D5 5단계 → 레인 요청 계획.

단계 대응(`contracts/stages/read.yaml#lane.sub_lanes` · `stage_artifacts`).

| D5 | 작업(task) | 레인 |
|---|---|---|
| ① 전 분해 + ② 관계 트리 | `decompose` | 계약이 정한 모델·effort |
| ③ 3중 접지(독립항 element) | `ground-independent` | 〃 |
| ③ 3중 접지(종속항 additions) | `ground-dependent` | 〃 (저비용 레인 허용 — 재정 R3) |
| ④ 유기적 통합 + ⑤ 포지셔닝 | `synthesize` | 〃 |

★ 이 표에 **수확(harvest)은 없다**(재정 P-B). 수확은 접지와 통합 사이에 도는 **결정론 실행**
이며 LLM 레인이 아니다 — 그래서 `read.yaml#lane.sub_lanes` 에도, 레인 로그에도 나타나지
않는다. 다만 발번 대역은 한 칸 차지한다(`harvest_band_start`): 통합 레인이 수확 항목의 임시
ID 를 `numeric_refs` 로 되가리키므로 번호가 겹치면 그 참조의 해소 근거가 사라진다.

**모델·effort 를 여기 적지 않는다.** 계약에서 읽는다 — 값이 코드에 박히면 재정으로 레인을
낮춰도(재정 R3) 러너가 따라오지 않는다.

**팬아웃 규율.** 한 배치는 30 미만이며(`MAX_FANOUT = 29`) 초과분은 자동으로 쪼갠다.
상한의 근거는 오케스트레이션 규정(런당 팬아웃 30 미만)이고, 배치마다 체크포인트가 남는
구조는 `read.yaml#lane.lane_discipline` 이 요구한 것이다.
"""

from __future__ import annotations

from .contract import LaneContractError, LaneRequest
from ..paths import load_stage_contract

# 한 배치의 최대 요청 수. "30 미만"이므로 29 다.
MAX_FANOUT = 29

# ★ 항목 ID 대역 — 레인이 **작업용으로만** 쓰는 임시 번호다.
#
# 최종 `M<n>` 은 엔진이 소유한다. 조립기(`engine/stages/read.py#assemble_spec`)가 레인
# 투입 순서대로 `M1` 부터 다시 매기고 참조 전량을 고쳐 쓰므로, 대역이 아무리 띄엄띄엄해도
# 조립본은 언제나 `M1..Mn` 연속이다. 여기서 나눠 준 번호가 그대로 산출에 남지 않는다.
# (2026-08-18 sol 재감수 B-01 — 대역을 이어 붙이기만 하던 판은 결번 1958 개를 남겨
# `lifecycle.id-contiguous` 를 위반했고, 정상 산출을 동결할 수 없었다.)
#
# 그럼에도 대역이 필요한 이유는 **참조의 일의성**이다. 두 레인이 같은 번호를 쓰면 항목은
# 재번호로 갈라지지만, 레인을 가로지르는 참조(`implication.derived_from[]` 이 분해 항목과
# 통합 항목을 함께 가리킨다)가 어느 항목을 뜻하는지 판정할 근거가 사라진다. 대역이 지켜지는
# 한 원본 ID 는 런 안에서 유일하고 그 판정이 필요 없다.
#
# 폭을 넉넉히 두는 이유: 대역이 좁으면 레인이 대역을 넘고 그 순간 위 전제가 무너진다.
# `M<n>` 은 런 내부 순번일 뿐 의미를 갖지 않으므로(SPEC §2.4) 번호가 띄엄띄엄해도 무해하다.
ID_BAND_WIDTH = 1000

TASKS: tuple[str, ...] = (
    "decompose",
    "ground-independent",
    "ground-dependent",
    "synthesize",
)

# 작업 ↔ 절차 문서. 문서 자체가 프롬프트이며 정본은 `reader/procedure/` 에 있다.
PROCEDURE_DOCS: dict[str, str] = {
    "decompose": "reader/procedure/10-decompose.md",
    "ground-independent": "reader/procedure/20-grounding.md",
    "ground-dependent": "reader/procedure/20-grounding.md",
    "synthesize": "reader/procedure/30-synthesis.md",
}

# ---------------------------------------------------------------------------
# 응답 계약 — 레인 산출이 만족해야 하는 최소 형태.
# ★ 여기서 재료 명세 스키마를 다시 쓰지 않는다. 항목의 정합은 `read.schema` 이하 8종이
#   조립본 위에서 판정하며, 이 스키마는 "조립할 수 있는 형태인가"만 본다. 두 벌의 전체
#   스키마가 존재하면 한 벌은 반드시 낡는다.
# ---------------------------------------------------------------------------

_ITEM = {
    "type": "object",
    "required": ["id", "kind"],
    "properties": {
        "id": {"type": "string", "pattern": "^M[0-9]+$"},
        "kind": {"type": "string"},
    },
}

_DROP_SIGNAL = {
    "type": "object",
    "required": ["stage", "verdict", "reason"],
    "properties": {
        "stage": {"enum": ["early", "final"]},
        "verdict": {"enum": ["go", "drop-proposed"]},
        "reason": {"type": "string", "minLength": 1},
    },
}

# ★ 맹검 스크리닝 메모(재정 P-A · P-U4). 분해 레인의 조기 판단은 이제 `drop_signal` 이
#   아니라 이 메모다 — 상신하지 않고 **기록만** 하며 러너를 세우지 않는다. 서식은 스크리닝
#   판단 기록형(판단 방향 하나 + 근거 요지 하나)이고 정본 서술은
#   `reader/procedure/10-decompose.md` §5 · `40-output-contract.md` §1 이다.
#   키 이름이 `reason` 인 것은 그 두 절차 문서의 실물 서식을 따른 것이다(레인이 읽는 것은
#   절차 문서이므로 계약을 절차에 맞춘다). CP1 표면·섀도 원장에서는 이 값이 `note` 로 실린다.
_SCREENING_MEMO = {
    "type": "object",
    "required": ["direction", "reason"],
    "properties": {
        "direction": {"enum": ["concern", "clear"]},
        "reason": {"type": "string", "minLength": 1},
    },
}

# ★ 폐기: `DECOMPOSE_SCHEMA` 의 `drop_signal`(stage: early).
#   근거 = 재정 P-A. 조기 drop 의 escalate 가 폐지되었고 조기 판단은 맹검 메모로 강등되었다.
#   폐기가 손실을 만들지 않는 이유는 판단 자체가 사라진 것이 아니라 **자리와 구속력**만
#   바뀌었기 때문이다 — 기록은 남고(섀도 원장·CP1 병기), 확정 재정은 CP1 한 자리로 모인다.
DECOMPOSE_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "lane-response/decompose",
    "type": "object",
    "required": ["claims", "items", "screening_memo"],
    "properties": {
        "claims": {
            "type": "object",
            "required": ["independent", "dependents", "applicant_interest"],
            "properties": {
                "independent": {"type": "array", "minItems": 1},
                "dependents": {"type": "array"},
                "applicant_interest": {"type": "array"},
            },
        },
        "items": {"type": "array", "minItems": 1, "items": _ITEM},
        "screening_memo": _SCREENING_MEMO,
    },
}

GROUNDING_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "lane-response/grounding",
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "allOf": [_ITEM, {"properties": {"kind": {"const": "grounding"}}}]
            },
        }
    },
}

SYNTHESIS_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "lane-response/synthesis",
    "type": "object",
    "required": ["items", "figures", "drop_signal"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "allOf": [
                    _ITEM,
                    {
                        "properties": {
                            "kind": {
                                "enum": ["fact", "implication", "positioning", "figure_note"]
                            }
                        }
                    },
                    # ★ 수확 소유권(재정 P-B). `origin ∈ {quoted, bibliographic}` 은 전수
                    #   기계 수확기(reader/lib/harvest.py)의 소유이며 레인이 만들지 않는다 —
                    #   레인이 만들면 같은 수치가 두 벌 생기거나(중복) 수확본과 갈린다(변조).
                    #   레인 소유는 `derived`(산식)와 `figure-sourced`(도면 판독) 둘뿐이다.
                    #   이 조건이 없어도 `value.harvest-parity` 가 사후에 잡지만, 응답 계약이
                    #   먼저 거부하면 레인이 그 사실을 즉시 안다.
                    {
                        "if": {
                            "required": ["kind"],
                            "properties": {"kind": {"const": "fact"}},
                        },
                        "then": {
                            "required": ["origin"],
                            "properties": {
                                "origin": {"enum": ["derived", "figure-sourced"]}
                            },
                        },
                    },
                ]
            },
        },
        "figures": {"type": "array"},
        "drop_signal": {
            "allOf": [_DROP_SIGNAL, {"properties": {"stage": {"const": "final"}}}]
        },
    },
}

RESPONSE_SCHEMAS: dict[str, dict] = {
    "decompose": DECOMPOSE_SCHEMA,
    "ground-independent": GROUNDING_SCHEMA,
    "ground-dependent": GROUNDING_SCHEMA,
    "synthesize": SYNTHESIS_SCHEMA,
}


# ---------------------------------------------------------------------------
# 레인 배정 — 계약에서 읽는다.
# ---------------------------------------------------------------------------


def _accepted_models(lane: dict, label: str) -> tuple[str, ...]:
    """티어 라벨 하나가 받아들이는 표기 전량(라벨 자신 포함).

    정본 = `read.yaml#lane.model_identity.labels`. 계약이 그 블록을 선언하지 않으면 **빈 튜플**을
    돌려주고, 그러면 대조는 구 동작(문자열 동등)으로 남는다 — 계약이 라벨 공간을 말하지 않은
    스테이지에서 코드가 제멋대로 관대해지지 않게 하기 위함이다(D7: 코드는 자기 법을 갖지 않는다).
    """
    identity = lane.get("model_identity") or {}
    for entry in identity.get("labels") or []:
        if entry.get("label") == label:
            aliases = [str(name) for name in (entry.get("aliases") or [])]
            return tuple(dict.fromkeys([label, *aliases]))
    return ()


def lane_profiles(repo: str | None = None) -> dict[str, dict]:
    """`read.yaml#lane.sub_lanes` → `{task: {model, effort, scope, accepted_models}}`."""
    contract = load_stage_contract("read", repo)
    lane = contract.get("lane") or {}
    profiles: dict[str, dict] = {}
    for entry in lane.get("sub_lanes") or []:
        task = entry.get("id")
        if not isinstance(task, str):
            continue
        model = entry.get("model")
        effort = entry.get("effort")
        if not model or not effort:
            raise LaneContractError(
                f"read.yaml 의 sub_lane {task} 에 model·effort 가 없다 — "
                "레인 지정은 API 레벨 하드 지정이며 빈 값을 허용하지 않는다"
            )
        profiles[task] = {
            "model": str(model),
            "effort": str(effort),
            "scope": entry.get("scope", ""),
            "accepted_models": _accepted_models(lane, str(model)),
        }
    missing = [task for task in TASKS if task not in profiles]
    if missing:
        raise LaneContractError(
            f"read.yaml 이 선언하지 않은 하위 레인이 있다: {', '.join(missing)}"
        )
    return profiles


def lane_id_for(read_run: str, task: str, batch: int, attempt: int = 0) -> str:
    """레인 좌표. 재시도는 별도 경로를 쓴다 — 같은 자리에 덮어쓰면 1차 응답이 사라진다."""
    if attempt:
        return f"{read_run}/{task}/retry-{attempt}/batch-{batch}"
    return f"{read_run}/{task}/batch-{batch}"


def batched(entries: list, size: int = MAX_FANOUT) -> list[list]:
    """팬아웃 상한으로 자른다. 빈 목록은 배치 0개."""
    if size < 1:
        raise LaneContractError("배치 크기는 1 이상이어야 한다")
    return [entries[start:start + size] for start in range(0, len(entries), size)]


# ---------------------------------------------------------------------------
# 접지 대상 추출 — 분해 산출에서 구성요소 목록을 뽑는다.
# ---------------------------------------------------------------------------


def _walk_elements(elements: list, claim_id: str, out: list) -> None:
    for element in elements or []:
        out.append(
            {
                "target_id": element.get("id"),
                "claim": claim_id,
                "material_id": element.get("material_id"),
                "text": element.get("text_verbatim", ""),
            }
        )
        _walk_elements(element.get("children") or [], claim_id, out)


def independent_targets(claims: dict) -> list[dict]:
    """독립항 element 전량(중첩 포함)."""
    out: list[dict] = []
    for claim in claims.get("independent") or []:
        _walk_elements(claim.get("elements") or [], claim.get("id"), out)
    return out


def dependent_targets(claims: dict) -> list[dict]:
    """종속항 `additions` 전량."""
    out: list[dict] = []
    for claim in claims.get("dependents") or []:
        for addition in claim.get("additions") or []:
            out.append(
                {
                    "target_id": addition.get("id"),
                    "claim": claim.get("id"),
                    "material_id": addition.get("material_id"),
                    "text": addition.get("text_verbatim", ""),
                }
            )
    return out


def _target_lines(targets: list[dict]) -> str:
    return "\n".join(
        f"- `{entry['target_id']}` (component `{entry['material_id']}`): {entry['text']}"
        for entry in targets
    )


def _defect_block(defects: list[dict] | None) -> str:
    """재시도 지시. 결함 목록을 되돌려 주지 않으면 재시도는 같은 오류를 재생산한다."""
    if not defects:
        return ""
    lines = [
        "",
        "## 재시도 — 직전 판의 결함",
        "",
        "아래는 결정론 검사가 낸 결함이다. **같은 자리를 같은 방식으로 다시 적지 마라.**",
        "특히 `read.verbatim` 계열은 기대 원문 바이트가 함께 적혀 있으므로 그것을 그대로 옮긴다.",
        "",
    ]
    for defect in defects:
        lines.append(
            f"- `{defect.get('check')}` / `{defect.get('rule')}` @ `{defect.get('locus')}`: "
            f"{defect.get('message')}"
        )
        lines.append(f"  - 실측: `{defect.get('found')}`")
        lines.append(f"  - 기대: `{defect.get('expected')}`")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 요청 생성
# ---------------------------------------------------------------------------


def highest_item_number(claims: dict) -> int:
    """이미 발번된 `M<n>` 의 최대값. 분해 산출의 `material_id` 전량을 훑는다."""
    highest = 0

    def note(value) -> None:
        nonlocal highest
        if isinstance(value, str) and value.startswith("M") and value[1:].isdigit():
            highest = max(highest, int(value[1:]))

    def walk(elements) -> None:
        for element in elements or ():
            note(element.get("material_id"))
            walk(element.get("children"))

    for claim in claims.get("independent") or ():
        walk(claim.get("elements"))
    for claim in claims.get("dependents") or ():
        for addition in claim.get("additions") or ():
            note(addition.get("material_id"))
    for entry in claims.get("applicant_interest") or ():
        note(entry.get("material_id"))
    return highest


def _band_block(start: int, width: int = ID_BAND_WIDTH) -> str:
    """레인에게 발번 대역을 알리는 지시 문단."""
    return (
        f"\n\n**항목 ID 대역 — `M{start}` ~ `M{start + width - 1}` 안에서만 발번한다.**\n"
        "이 번호는 작업용이며 최종 번호는 조립기가 다시 매긴다. 그래도 대역을 지켜야 하는\n"
        "이유는 다른 레인의 항목을 가리키는 참조가 어느 항목을 뜻하는지 일의적으로 정해지기\n"
        "때문이다 — 두 레인이 같은 번호를 쓰면 그 판정 근거가 사라진다."
    )


def grounding_slot_count(claims: dict) -> int:
    """접지가 쓰는 대역 슬롯 수(독립·종속 각각의 배치 수)."""
    return len(batched(independent_targets(claims))) + len(batched(dependent_targets(claims)))


def synthesis_band_start(claims: dict) -> int:
    """통합 레인의 발번 대역 시작. 접지 대역 **다음**이다."""
    return highest_item_number(claims) + 1 + grounding_slot_count(claims) * ID_BAND_WIDTH


def harvest_band_start(claims: dict) -> int:
    """수확기의 임시 발번 대역 시작 — 통합 대역 **다음** 칸(재정 P-B).

    수확은 레인이 아니라 결정론 실행이지만 대역은 똑같이 지켜야 한다. 통합 레인이
    `numeric_refs` 에 수확 항목의 임시 ID 를 적어 내고, 조립기는 그 참조를 원본 ID 로
    해소하기 때문이다 — 두 자리가 같은 번호를 쓰면 그 해소가 어느 항목을 뜻하는지
    판정할 근거가 사라진다(`engine/stages/read.py#_Renumbering`).

    수확이 통합보다 **먼저** 도는데 대역은 뒤에 두는 이유: 대역 배치는 계획 시점에
    결정론으로 계산되고 실행 순서와 무관하다. 통합 대역을 옮기면 이미 굳은 계산
    (`plan_synthesis`)이 함께 흔들린다.
    """
    return synthesis_band_start(claims) + ID_BAND_WIDTH


def _harvest_block(harvest: list[dict] | None) -> str:
    """수확된 수치 목록을 통합 레인 지시에 싣는다(재정 P-B).

    ★ 이 표가 있어야 통합 레인이 `numeric_refs` 를 **참조 ID로** 적을 수 있다. 표가 없으면
    레인은 자기가 본 원문에서 숫자를 다시 옮겨 적게 되고, 그 순간 같은 수치가 두 벌 생겨
    `value.harvest-parity` 가 실패한다. 고르는 주체를 서사가 아니라 참조로 옮긴다는 것이
    재정 P-B 의 요지다.
    """
    if not harvest:
        return (
            "\n\n**수확된 수치.** 접지 스팬에서 수확된 수치가 없다. `numeric_refs` 는 빈 배열로"
            "\n적는다 — 없다는 사실을 빈 배열로 적는 것과 필드를 빠뜨리는 것은 다르다."
        )
    lines = [
        "",
        "",
        "**★ 수확된 수치 목록(전수 · 재정 P-B).** 아래는 접지 스팬과 서지면에서 **이미 전수**",
        "기계 수확된 수치다. 함의·포지셔닝 항목은 근거로 삼은 수치를 `numeric_refs` 에",
        "**참조 ID로** 적는다. **수치를 새로 지어내지 마라** — 원문 스팬 수치와 서지 수치는",
        "이미 전수 수확되어 있으므로, 네가 만들 수 있는 `fact` 는 산식(`derived`)과",
        "도면 판독(`figure-sourced`) 둘뿐이다.",
        "",
        "| 참조 ID | 라벨 | 정규화 값 | 단위 |",
        "|---|---|---|---|",
    ]
    for item in harvest:
        unit = item.get("unit")
        lines.append(
            f"| `{item.get('id')}` | {item.get('label_en', '')} | "
            f"`{item.get('value_normalized', '')}` | {unit if unit else '-'} |"
        )
    lines.append("")
    lines.append(
        "이 표의 ID 는 작업용 임시 번호이며 최종 번호는 조립기가 다시 매긴다 — 그래도 참조는"
    )
    lines.append("보존된다(조립기가 `numeric_refs` 를 함께 고쳐 쓴다).")
    return "\n".join(lines)


def _request(
    *,
    read_run: str,
    task: str,
    batch: int,
    attempt: int,
    profiles: dict,
    instructions: str,
    slices: dict,
) -> LaneRequest:
    profile = profiles[task]
    return LaneRequest(
        lane_id=lane_id_for(read_run, task, batch, attempt),
        read_run=read_run,
        task=task,
        model=profile["model"],
        effort=profile["effort"],
        prompt_path=PROCEDURE_DOCS[task],
        instructions=instructions,
        slices=slices,
        response_schema=RESPONSE_SCHEMAS[task],
        batch=batch,
        accepted_models=profile.get("accepted_models", ()),
    )


def plan_decompose(
    read_run: str,
    view,
    profiles: dict,
    attempt: int = 0,
    defects: list[dict] | None = None,
) -> list[LaneRequest]:
    """D5 ①② — 청구항 구간 전체를 한 레인이 본다(트리는 쪼개면 트리가 아니다)."""
    instructions = (
        "청구항 구간 전량을 분해한다. 원천에 있는 **모든** 청구항이 대상이며, 하나라도 빠지면\n"
        "`read.claim-inventory` 가 잡는다. 산출은 `claims`(독립·종속·출원인 관심)과\n"
        "`items`(kind: component) 와 `screening_memo` 다.\n"
        "맹검 스크리닝 메모는 **상신이 아니다** — 기록만 하며 네 메모가 런을 세우지 않는다"
        "(재정 P-A). 판단 방향(`clear`·`concern`) 하나와 근거 요지(KR) 하나를 적는다.\n"
        f"이 요청은 독립 실행 `{read_run}` 의 것이며, 다른 실행의 산출을 보지 않는다."
        + _defect_block(defects)
    )
    return [
        _request(
            read_run=read_run,
            task="decompose",
            batch=0,
            attempt=attempt,
            profiles=profiles,
            instructions=instructions,
            slices=view.slices_for("decompose"),
        )
    ]


def plan_grounding(
    read_run: str,
    claims: dict,
    view,
    profiles: dict,
    attempt: int = 0,
    defects: list[dict] | None = None,
) -> list[LaneRequest]:
    """D5 ③ — 구성요소별 3중 접지. 독립·종속을 다른 레인으로 나누고 배치로 쪼갠다."""
    requests: list[LaneRequest] = []
    plan = (
        ("ground-independent", independent_targets(claims), "독립항 element"),
        ("ground-dependent", dependent_targets(claims), "종속항 부가 한정"),
    )
    # 분해가 쓴 최대 번호 다음부터 레인마다 겹치지 않는 대역을 나눠 준다.
    band_start = highest_item_number(claims) + 1
    slot = 0
    for task, targets, label in plan:
        for batch, chunk in enumerate(batched(targets)):
            instructions = (
                f"{label} {len(chunk)}건에 3중 접지를 붙인다(구성요소 ↔ 명세서 문단 ↔ 도면부호).\n"
                "접지 대상 component 항목 ID 는 아래 목록이 정본이며, `grounding` 항목의\n"
                "`component` 가 그 ID 를 가리켜야 한다. 접지가 불가능하면 누락하지 말고\n"
                "`anchor_state` 예외(`no-anchor-found`·`not-depicted`)로 신고하고 `search_note`(KR)를 단다.\n\n"
                f"{_target_lines(chunk)}"
                + _band_block(band_start + slot * ID_BAND_WIDTH)
                + _defect_block(defects)
            )
            slot += 1
            requests.append(
                _request(
                    read_run=read_run,
                    task=task,
                    batch=batch,
                    attempt=attempt,
                    profiles=profiles,
                    instructions=instructions,
                    slices=view.slices_for(task),
                )
            )
    return requests


def referenced_figures(groundings: list[dict] | None) -> list[str]:
    """접지 레인이 실제로 참조한 도면 id 목록(정렬·중복 제거)."""
    found: set[str] = set()
    for payload in groundings or ():
        for item in (payload or {}).get("items") or ():
            for ref in item.get("figure_refs") or ():
                figure = ref.get("figure")
                if isinstance(figure, str) and figure:
                    found.add(figure)

    def sort_key(figure_id: str):
        tail = figure_id[4:] if figure_id.startswith("FIG-") else figure_id
        digits = "".join(ch for ch in tail if ch.isdigit())
        return (int(digits) if digits else 0, figure_id)

    return sorted(found, key=sort_key)


def _figure_registry_block(figures: list[str]) -> str:
    """접지가 참조한 도면을 반드시 등재하라는 지시.

    ★ 2026-08-18 실특허 스모크에서 접지 레인이 올린 결합 공백의 처분. `figures[]` 는
    **synthesize 산출에서만** 조립되는데(`engine/stages/read.py`), `figure_refs[].figure` 는
    `read.pointer-resolve` 가 그 배열에 대고 해소한다. 접지 레인은 자기가 참조한 도면을
    등재할 수단이 없고 synthesize 는 무엇이 참조되었는지 알 방법이 없었다 — 두 레인 사이에
    아무도 책임지지 않는 구간이 있었고, 거기서 유령 참조가 **구조적으로** 발생한다.
    """
    if not figures:
        return (
            "\n\n**도면 등재.** 접지 레인이 참조한 도면이 없다. `figures` 는 빈 배열이어도 되지만,"
            "\n네가 `figure_note` 나 `figure-sourced` 수치를 만든다면 그 도면은 반드시 등재한다."
        )
    listed = " · ".join(f"`{figure}`" for figure in figures)
    return (
        "\n\n**★ 도면 등재(필수).** 접지 레인이 아래 도면을 참조했다. `figures` 배열에 "
        "**전건을 등재**하라 —\n"
        f"{listed}\n"
        "등재하지 않으면 그 접지 항목의 `figure_refs` 가 해소되지 않아 `read.pointer-resolve` 가\n"
        "실패한다. 네가 추가로 참조하는 도면이 있으면 함께 등재한다. `asset_path` 는 영구히 `null` 이다."
    )


def plan_synthesis(
    read_run: str,
    claims: dict,
    view,
    profiles: dict,
    attempt: int = 0,
    defects: list[dict] | None = None,
    groundings: list[dict] | None = None,
    harvest: list[dict] | None = None,
) -> list[LaneRequest]:
    """D5 ④⑤ — 유기적 통합·포지셔닝·수치 사실·최종 drop 신호.

    ★ **맹검 유지(재정 P-A).** 분해 레인의 `screening_memo` 를 이 지시문에 **싣지 않는다.**
    최종 서사 평가는 조기 판단을 모른 채 이루어져야 하며(앵커링 방지), 두 판단이 독립일 때만
    축적물(맹검 판단 · 최종 평가 · Owner 재정 3층)이 의미를 갖는다. 메모를 여기 실으면 그
    독립성이 조용히 사라지고, 사라진 사실은 산출물 어디에도 드러나지 않는다.
    """
    claim_ids = [claim.get("id") for claim in claims.get("independent") or []]
    instructions = (
        "분해된 골격 위에서 ④ 유기적 통합과 ⑤ 포지셔닝을 낸다. 산출은 `items`\n"
        "(kind: fact · implication · positioning · figure_note)와 `figures` 와 최종 `drop_signal` 이다.\n"
        f"독립항: {', '.join(str(entry) for entry in claim_ids)}\n"
        "수치 사실의 origin 은 `derived`(산식, 깊이 1)와 `figure-sourced`(도면 판독, 기계 검증\n"
        "불가) 둘뿐이다 — 원문 스팬(`quoted`)과 서지 복사(`bibliographic`)는 이미 전수 수확되어\n"
        "있으므로 네 소유가 아니다(재정 P-B)."
        # 접지 레인이 쓴 대역 **다음**을 준다. 슬롯 수는 `plan_grounding` 과 같은 함수로
        # 다시 세므로(레인 산출을 참조하지 않는다) 두 계획이 어긋날 수 없다.
        + _band_block(synthesis_band_start(claims))
        + _figure_registry_block(referenced_figures(groundings))
        + _harvest_block(harvest)
        + _defect_block(defects)
    )
    return [
        _request(
            read_run=read_run,
            task="synthesize",
            batch=0,
            attempt=attempt,
            profiles=profiles,
            instructions=instructions,
            slices=view.slices_for("synthesize"),
        )
    ]
