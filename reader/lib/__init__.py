# -*- coding: utf-8 -*-
"""`reader/lib` — 재료 명세의 결정론 검증기 일체.

이 패키지는 **이식 단위**(`reader/`)에 속한다. 표준 라이브러리와 `yaml`·`jsonschema` 외에는
아무것도 import 하지 않으며, `contracts/**`·`engine/**`·`docs/**` 를 읽지 않는다 —
patent-historian 이 `reader/` 만 스냅샷해도 그대로 동작해야 하기 때문이다
(SPEC §6.2 판별식 1 · D14).

검사가 판정하는 것은 "독해가 옳은가"가 아니라 **"독해가 자기 산출물에 대해 거짓말을 하지
않았는가"**뿐이다(D6 규율 ③ · SPEC §2.6). 전 검사를 통과한 명세도 여전히 얕거나 초점이
틀릴 수 있으며, 그 판단은 체크포인트 1 의 Owner 몫이다.
"""

from __future__ import annotations

from .harvest import (
    HARVESTED_ORIGINS,
    harvest_numeric_facts,
    identity_key,
    parity_key,
)
from .normalize import (
    UNIT_ALIASES,
    NormalizeError,
    format_decimal,
    match_key,
    normalize_number,
    normalize_unit,
)
from .report import CheckContext, CheckRow, Finding
from .rules import Rules, RulesError
from .run_checks import (
    CHECK_REGISTRY,
    EARLY_CLAIM_CHECK_IDS,
    FREEZE_CHECK_IDS,
    READ_CHECK_IDS,
    run_early_claim_checks,
    run_freeze_checks,
    run_read_checks,
    to_convergence_payload,
)
from .spec_io import SpecIndex, load_schema, load_spec
from .value_grammar import ValueGrammarError, parse_value, render_value

__all__ = [
    "CHECK_REGISTRY",
    "HARVESTED_ORIGINS",
    "CheckContext",
    "CheckRow",
    "EARLY_CLAIM_CHECK_IDS",
    "FREEZE_CHECK_IDS",
    "Finding",
    "NormalizeError",
    "READ_CHECK_IDS",
    "Rules",
    "RulesError",
    "SpecIndex",
    "UNIT_ALIASES",
    "ValueGrammarError",
    "format_decimal",
    "harvest_numeric_facts",
    "identity_key",
    "load_schema",
    "load_spec",
    "match_key",
    "normalize_number",
    "normalize_unit",
    "parity_key",
    "parse_value",
    "render_value",
    "run_early_claim_checks",
    "run_freeze_checks",
    "run_read_checks",
    "to_convergence_payload",
]
