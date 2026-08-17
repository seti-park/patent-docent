# -*- coding: utf-8 -*-
"""전 검사 실행 오케스트레이터 + `10-read/convergence.json` 본문 조립.

READ 스테이지의 `checks_before_exit`(SPEC §1.4)와 `freeze` 종료 전 검사(§1.6)를 한 자리에서
돌린다. 등재는 `CHECK_REGISTRY` 한 곳이며, **등재만 하고 시험하지 않는 검사**를 막는 것은
`tests/test_m1_reader.py::test_every_registered_check_has_a_failing_case` 다.

산출 서식의 행은 재정 N5 의 `verdict-check-row/v0` 8키다 — 공허 2종(규칙 0항·대상 0건)이
행마다 자동으로 드러난다.
"""

from __future__ import annotations

from . import (
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
    "read.claim-inventory",
    "read.convergence",
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
    "read.claim-inventory": inventory.check,
    "read.convergence": convergence.check,
    "freeze.id-monotonic": freeze_integrity.check_id_monotonic,
    "freeze.payload-immutable": freeze_integrity.check_payload_immutable,
}


def run_read_checks(ctx: CheckContext) -> list[CheckRow]:
    """READ 종료 전 검사 8종을 순서대로 실행한다.

    `peer_spec` 이 없으면 `read.convergence` 는 `checked=0` · `findings=[]` 로 나오고
    `extras["skipped"]` 가 남는다 — 행 서식의 `vacuous: "empty-target"` 이 그 사실을
    자동으로 표기하므로, 2회차 없는 런이 수렴 통과로 보이지 않는다.
    """
    return [CHECK_REGISTRY[check_id](ctx) for check_id in READ_CHECK_IDS]


def run_freeze_checks(ctx: CheckContext) -> list[CheckRow]:
    """동결 종료 전 검사 2종."""
    return [CHECK_REGISTRY[check_id](ctx) for check_id in FREEZE_CHECK_IDS]


def to_convergence_payload(rows: list[CheckRow], spec: dict | None = None) -> dict:
    """`10-read/convergence.json` 본문을 만든다.

    서식 정본 = `contracts/schemas/convergence.schema.json`(convergence/v0). 그 파일을 여기서
    읽지 않는다(이식 단위가 `contracts/` 를 참조하면 안 된다) — 동치는
    `tests/test_m1_reader.py::test_convergence_payload_validates_against_contract` 가 대조한다.

    `spec` 은 실질적으로 필수다. `run_id`·`reader_version`·`spec_version`·`source_digest` 를
    그 인스턴스에서 복사하며, 주지 않으면 계약을 만족하지 못하는 뼈대만 나온다.
    `vacuous_pass[]` 는 손으로 채우는 필드가 아니라 `checks[]` 에서 파생한다(재정 N5).
    """
    source = spec or {}
    patent = source.get("patent") or {}
    findings = [finding.as_dict() for row in rows for finding in row.findings]
    check_rows = [row.to_row_dict() for row in rows]
    payload = {
        "schema": "convergence/v0",
        "run_id": source.get("run_id", ""),
        "reader_version": source.get("reader_version", ""),
        "spec_version": source.get("spec_version", 1),
        "source_digest": patent.get("source_digest", ""),
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
    return payload
