# -*- coding: utf-8 -*-
"""`read.schema` — 재료 명세 스키마 검증(SPEC §1.4 종료 전 검사).

스키마 정본은 `reader/schemas/material-spec.schema.json` **실파일** 한 벌이다(SPEC §2.8).
검사기는 그 파일을 로드할 뿐 사본을 들지 않는다 — 두 벌이 존재하는 순간 한 벌은 반드시
뒤처지고, 뒤처진 사본으로 구현한 코드가 계약을 깬다.

`oneOf`·`allOf` 가 낸 상위 오류는 사람이 읽을 수 없으므로 **잎 오류**로 내린 뒤 보고한다.
"""

from __future__ import annotations

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from .report import CheckContext, CheckRow
from .spec_io import load_schema

CHECK_ID = "read.schema"


def _locus(error) -> str:
    parts: list[str] = []
    for step in error.absolute_path:
        if isinstance(step, int):
            parts.append(f"[{step}]")
        else:
            parts.append(f".{step}" if parts else str(step))
    return "".join(parts) or "$"


def _leaf(error):
    """`oneOf`·`anyOf` 의 하위 오류로 내려가 가장 구체적인 오류를 고른다."""
    current = error
    guard = 0
    while getattr(current, "context", None) and guard < 20:
        deeper = best_match(current.context)
        if deeper is None:
            break
        current = deeper
        guard += 1
    return current


def check(ctx: CheckContext) -> CheckRow:
    row = CheckRow(check_id=CHECK_ID, checked=1)
    schema = ctx.schema if ctx.schema is not None else load_schema()
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(ctx.spec), key=lambda err: list(err.absolute_path))
    for error in errors:
        leaf = _leaf(error)
        row.add(
            "schema.validate",
            _locus(leaf),
            repr(leaf.instance),
            str(leaf.schema) if not isinstance(leaf.schema, dict) else str(leaf.validator_value),
            f"스키마 검증 실패({leaf.validator}): {leaf.message}",
        )
    return row
