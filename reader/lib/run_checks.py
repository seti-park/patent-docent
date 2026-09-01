# -*- coding: utf-8 -*-
"""전 검사 실행 오케스트레이터 + `10-read/convergence.json` 본문 조립.

READ 스테이지의 조기 청구항 소유 검사(T16)·`checks_before_exit`(SPEC §1.4)와 `freeze` 종료 전
검사(§1.6)를 한 자리에서 돌린다. 등재는 `CHECK_REGISTRY` 한 곳이며, **등재만 하고 시험하지
않는 검사**를 막는 것은 `tests/test_m1_reader.py::test_every_registered_check_has_a_failing_case` 다.

산출 서식의 행은 재정 N5 의 `verdict-check-row/v0` 8키다 — 공허 2종(규칙 0항·대상 0건)이
행마다 자동으로 드러난다.
"""

from __future__ import annotations

from . import (
    bibliography,
    convergence,
    coverage,
    dependency_parse,
    derivation,
    freeze_integrity,
    inventory,
    pointers,
    schema_check,
    source_digest,
    verbatim,
)
from .report import CheckContext, CheckRow
from .spec_io import SpecIndex

# ★ 순서에 뜻이 있다 — `read.source-digest` 가 `read.schema` 바로 다음이다. 불변식 I1 이
#   "다이제스트가 어긋나면 결정론 검사 전부 무효"라고 적었으므로, 그 판정이 아래 검사들보다
#   먼저 나와야 보고서를 읽는 사람이 순서를 오해하지 않는다.
READ_CHECK_IDS: tuple[str, ...] = (
    "read.schema",
    "read.source-digest",
    "read.verbatim",
    "read.pointer-resolve",
    "read.coverage",
    "read.dependency-parse",
    "read.value-derivation",
    # `read.bibliography` 는 `read.value-derivation` 다음이다(재정 P-2 ⓐ) — 서지 복사 사실의
    # 값 대조가 먼저 서고, 그 위에서 서지 **구조**(목록·코드·최우선일)를 본다.
    "read.bibliography",
    "read.claim-inventory",
    "read.convergence",
)

# ★ 조기 국면 등재부 (재정 2026-09-01 T16-ⓐ).
#
#   **정의는 하나이고 호출점이 둘이다.** 아래 두 검사는 `READ_CHECK_IDS` 에 **그대로 남는다** —
#   두 국면이 보는 것이 다르기 때문이다.
#
#     조기 실패 = **분해 결함**(조기 예산 · 분해 재시도)
#     출구 실패(조기 통과 후) = **국면 간 변이**(후속 예산 · 정본 후속 재시도)
#
#   출구 행을 지우면 그 계열은 「못 고치는 결함」이 아니라 **「탐지조차 안 되는 결함」**으로
#   격하된다 — 조립기가 `copy.deepcopy` 직후 청구항 트리의 material_id 를 전량 재작성하고
#   그 번호표는 접지·통합·수확 산출까지 포함해 만들어지므로, 그 오염은 분해 산출에
#   나타나지 않는다(재정 T16 §2 ⒜).
EARLY_CLAIM_CHECK_IDS: tuple[str, ...] = (
    "read.claim-inventory",
    "read.dependency-parse",
)

FREEZE_CHECK_IDS: tuple[str, ...] = (
    "freeze.id-monotonic",
    "freeze.payload-immutable",
)

CHECK_REGISTRY: dict[str, callable] = {
    "read.schema": schema_check.check,
    "read.source-digest": source_digest.check,
    "read.verbatim": verbatim.check,
    "read.pointer-resolve": pointers.check,
    "read.coverage": coverage.check,
    "read.dependency-parse": dependency_parse.check,
    "read.value-derivation": derivation.check,
    "read.bibliography": bibliography.check,
    "read.claim-inventory": inventory.check,
    "read.convergence": convergence.check,
    "freeze.id-monotonic": freeze_integrity.check_id_monotonic,
    "freeze.payload-immutable": freeze_integrity.check_payload_immutable,
}


def run_early_claim_checks(ctx: CheckContext) -> list[CheckRow]:
    """조기 국면의 청구항 소유 검사 — **분해 산출 하나** 위에서 돈다(재정 T16).

    호출자는 `read_run` 마다 한 번씩 부른다. `ctx.spec` 은 그 실행의 분해 전용 명세
    (`engine/stages/read.py#decompose_only_spec`)이고 `ctx.source_text`·`ctx.rules` 가 함께
    온다 — 이 두 검사는 원천과 규칙 파일을 읽는다.
    """
    return [CHECK_REGISTRY[check_id](ctx) for check_id in EARLY_CLAIM_CHECK_IDS]


def run_read_checks(ctx: CheckContext) -> list[CheckRow]:
    """READ 종료 전 검사 전건을 순서대로 실행한다(`READ_CHECK_IDS`).

    `peer_spec` 이 없으면 `read.convergence` 는 `checked=0` · `findings=[]` 로 나오고
    `extras["skipped"]` 가 남는다 — 행 서식의 `vacuous: "empty-target"` 이 그 사실을
    자동으로 표기하므로, 2회차 없는 런이 수렴 통과로 보이지 않는다.
    """
    return [CHECK_REGISTRY[check_id](ctx) for check_id in READ_CHECK_IDS]


def run_freeze_checks(ctx: CheckContext) -> list[CheckRow]:
    """동결 종료 전 검사 2종."""
    return [CHECK_REGISTRY[check_id](ctx) for check_id in FREEZE_CHECK_IDS]


def to_convergence_payload(
    rows: list[CheckRow],
    spec: dict | None = None,
    *,
    phase: str = "full",
    canonical_read_run: str | None = None,
    screening_memos=(),
    skipped_tokens=(),
) -> dict:
    """`10-read/convergence.json` 본문을 만든다.

    서식 정본 = `contracts/schemas/convergence.schema.json`(convergence/v0). 그 파일을 여기서
    읽지 않는다(이식 단위가 `contracts/` 를 참조하면 안 된다) — 동치는
    `tests/test_m1_reader.py::test_convergence_payload_validates_against_contract` 가 대조한다.

    `spec` 은 실질적으로 필수다. `run_id`·`reader_version`·`spec_version`·`source_digest` 를
    그 인스턴스에서 복사하며, 주지 않으면 계약을 만족하지 못하는 뼈대만 나온다.
    `vacuous_pass[]` 는 손으로 채우는 필드가 아니라 `checks[]` 에서 파생한다(재정 N5).

    신설 인자(전부 기본값이 있어 기존 호출부를 깨지 않는다):

      `phase`               `"early"` = 조기 수렴 판정서(분해 직후, 재정 P-4) ·
                            `"full"` = 정본이 전 단계를 마친 최종 보고서.
      `canonical_read_run`  정본으로 지정된 실행 식별자. 생략하면 `provenance.read_runs[0]`
                            에서 읽는다 — 규칙이 **선언 순서**이므로 그 값이 곧 정본이다
                            (내용맹·결정론, 품질 비교 금지 — 재정 P-4).
      `screening_memos`     맹검 메모 2건(재정 P-A·P-U4). 러너가 레인 응답에서 모은다.
      `skipped_tokens`      수확에서 건너뛴 토큰. 주지 않으면 `read.value-derivation` 행이
                            남긴 것을 쓴다.

    ★ `phase == "early"` 에 접지·수확 산물이 실려 있으면 계약이 그것을 거부한다. 이 함수가
    값을 지워서 맞추지 않는 이유가 그것이다 — 순서가 무너진 사실은 산출물에 남아야 한다.
    """
    source = spec or {}
    patent = source.get("patent") or {}
    provenance = source.get("provenance") or {}
    read_runs = provenance.get("read_runs") or []
    findings = [finding.as_dict() for row in rows for finding in row.findings]
    check_rows = [row.to_row_dict() for row in rows]
    payload = {
        "schema": "convergence/v0",
        "run_id": source.get("run_id", ""),
        "reader_version": source.get("reader_version", ""),
        "spec_version": source.get("spec_version", 1),
        "source_digest": patent.get("source_digest", ""),
        "phase": phase,
        # 정본 지정은 **선언 순서**이고 내용을 보지 않는다(재정 P-4). 두 값이 상수인 이유는
        # 그것이 변수가 되는 순간 "어느 쪽이 더 나은가"를 묻는 자리가 생기기 때문이다.
        "canonical_selection": {
            "read_run": canonical_read_run or (read_runs[0] if read_runs else ""),
            "rule": "declaration-order",
            "content_blind": True,
        },
        "checks": check_rows,
        "vacuous_pass": [
            entry["check_id"] for entry in check_rows if entry["vacuous"] != "none"
        ],
        "findings": findings,
        "convergence_detail": {
            "executed": False,
            "attempt": 0,
            "independent_count": [],
            "dependent_count": [],
            "axes": [],
        },
        "convergence_report": {"axes": [], "escalations": [], "divergences": []},
        "unclassified_dependents": [],
        "numeric_inventory": {
            "total": 0,
            "referenced": [],
            "unreferenced": [],
            "skipped": list(skipped_tokens),
        },
        "screening_memos": [dict(memo) for memo in screening_memos],
        "fact_classification": {
            "quoted_span": {"count": 0, "material_ids": []},
            "bibliographic_ids": [],
            "derived": [],
            "figure_sourced": [],
        },
        "manual_verification_required": [],
        "grounding_exceptions": [],
    }
    for row in rows:
        for key in ("fact_classification", "manual_verification_required", "grounding_exceptions"):
            if key in row.extras:
                payload[key] = row.extras[key]
        if row.check_id == "read.value-derivation" and "numeric_inventory" in row.extras:
            # 전수 수확의 인벤토리(재정 P-B) — 중요분은 numeric_refs 역참조가 도출한다.
            inventory_block = dict(row.extras["numeric_inventory"])
            if skipped_tokens:
                inventory_block["skipped"] = list(skipped_tokens)
            payload["numeric_inventory"] = inventory_block
        if row.check_id == "read.dependency-parse":
            payload["unclassified_dependents"] = _unclassified_rows(
                source, row.extras.get("unclassified") or []
            )
        if row.check_id == "read.convergence":
            executed = not row.extras.get("skipped", False)
            payload["convergence_detail"] = {
                "executed": executed,
                # 재실행 횟수는 스테이지 러너(M2)가 아는 값이다. 검증기는 1회 실행만 안다.
                "attempt": 1 if executed else 0,
                "independent_count": row.extras.get("independent_count", []),
                "dependent_count": row.extras.get("dependent_count", []),
                "axes": row.extras.get("axes", []),
            }
            # 독해 프로파일(재정 P-3) — 프레임 라벨은 사람이 읽는 자리(CP1 판독본)의 것이고
            # 계약 블록은 세 배열만 든다.
            profile = row.extras.get("profile") or {}
            payload["convergence_report"] = {
                "axes": profile.get("axes", []),
                "escalations": profile.get("escalations", []),
                "divergences": profile.get("divergences", []),
            }
    return payload


def _unclassified_rows(spec: dict, claim_ids: list) -> list[dict]:
    """미분류 종속항 목록(재정 P-1) — ID 만으로는 "무엇이 미분류인지"를 말하지 못한다.

    전문을 함께 싣는 이유는 사람이 그 자리에서 구조를 읽어야 하기 때문이다. 이 목록의
    항목은 **결함이 아니다** — 판정에서 빠졌다는 사실을 드러내는 자리다.
    """
    index = SpecIndex.build(spec)
    rows: list[dict] = []
    for claim_id in claim_ids:
        claim = index.claims.get(claim_id) or {}
        rows.append(
            {
                "claim": claim_id,
                "dependency_type": "unclassified",
                "text_verbatim": claim.get("text_verbatim", ""),
            }
        )
    return rows
