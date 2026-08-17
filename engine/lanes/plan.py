# -*- coding: utf-8 -*-
"""D5 5단계 → 레인 요청 계획.

단계 대응(`contracts/stages/read.yaml#lane.sub_lanes` · `stage_artifacts`).

| D5 | 작업(task) | 레인 |
|---|---|---|
| ① 전 분해 + ② 관계 트리 | `decompose` | 계약이 정한 모델·effort |
| ③ 3중 접지(독립항 element) | `ground-independent` | 〃 |
| ③ 3중 접지(종속항 additions) | `ground-dependent` | 〃 (저비용 레인 허용 — 재정 R3) |
| ④ 유기적 통합 + ⑤ 포지셔닝 | `synthesize` | 〃 |

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

# ★ 항목 ID 대역 (2026-08-18 실특허 스모크에서 적발한 조용한 소실 경로의 **예방**).
#
# 한 독립 실행 안에서 여러 레인이 동시에 `M<n>` 을 발번한다. 대역을 나눠 주지 않으면
# 두 레인이 나란히 `M1` 부터 세고, 조립은 그대로 이어 붙이며, dict 인덱싱이 **뒤엣것으로
# 덮어써** 항목 하나가 소리 없이 사라진다. 결번이 아니므로 ID 연속성 검사도 보지 못했다.
#
# 이제 `read.pointer-resolve` 의 `pointer.item-id-unique` 가 충돌을 **잡지만**, 잡히면
# 런이 실패한다. 탐지와 예방은 다른 일이며 둘 다 필요하다 — 여기가 예방이다.
#
# 폭을 넉넉히 두는 이유: 대역이 좁으면 레인이 대역을 넘고 그 순간 예방이 탐지로 되돌아간다.
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

DECOMPOSE_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "lane-response/decompose",
    "type": "object",
    "required": ["claims", "items", "drop_signal"],
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
        "drop_signal": {
            "allOf": [_DROP_SIGNAL, {"properties": {"stage": {"const": "early"}}}]
        },
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


def lane_profiles(repo: str | None = None) -> dict[str, dict]:
    """`read.yaml#lane.sub_lanes` → `{task: {model, effort, scope}}`."""
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
        profiles[task] = {"model": str(model), "effort": str(effort), "scope": entry.get("scope", "")}
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
        "다른 레인이 같은 번호를 쓰면 조립에서 항목 하나가 조용히 사라진다.\n"
        "`read.pointer-resolve` 의 `pointer.item-id-unique` 가 그것을 결함으로 잡는다."
    )


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
        "`items`(kind: component) 와 조기 `drop_signal` 이다.\n"
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
) -> list[LaneRequest]:
    """D5 ④⑤ — 유기적 통합·포지셔닝·수치 사실·최종 drop 신호."""
    claim_ids = [claim.get("id") for claim in claims.get("independent") or []]
    instructions = (
        "분해된 골격 위에서 ④ 유기적 통합과 ⑤ 포지셔닝을 낸다. 산출은 `items`\n"
        "(kind: fact · implication · positioning · figure_note)와 `figures` 와 최종 `drop_signal` 이다.\n"
        f"독립항: {', '.join(str(entry) for entry in claim_ids)}\n"
        "수치 사실은 origin 을 반드시 구별한다 — 원문 스팬(`quoted`)·산식(`derived`, 깊이 1)·\n"
        "도면 판독(`figure-sourced`, 기계 검증 불가)·서지 복사(`bibliographic`)."
        # 접지 레인이 쓴 대역 **다음**을 준다. 슬롯 수는 `plan_grounding` 과 같은 함수로
        # 다시 세므로(레인 산출을 참조하지 않는다) 두 계획이 어긋날 수 없다.
        + _band_block(
            highest_item_number(claims)
            + 1
            + (
                len(batched(independent_targets(claims)))
                + len(batched(dependent_targets(claims)))
            )
            * ID_BAND_WIDTH
        )
        + _figure_registry_block(referenced_figures(groundings))
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
