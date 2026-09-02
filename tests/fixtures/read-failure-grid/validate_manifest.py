# -*- coding: utf-8 -*-
"""READ 실패 격자 manifest의 형식·우주·β·provenance 검증기.

엔진 값 자체는 검사하지 않는다. 이 모듈은 stdlib만 사용하며, 호출자가 넘긴 검사 ID와
커밋 provenance를 기준으로 순수하게 manifest 한 값을 검증한다.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any


GENERATOR = "tests/fixtures/read-failure-grid/generate.py"
GENERATION_COMMAND = r'''set -euo pipefail; MAIN="${MAIN:-/home/laptop/projects/patent-docent}"; BASE="${BASE:-99fad78}"; OUT_PATH="${OUT_PATH:-$MAIN/tests/fixtures/read-failure-grid/manifest.json}"; PYTHON_BIN="${PYTHON_BIN:-$MAIN/.venv/bin/python}"; cd "$MAIN"
git diff --quiet "$BASE" HEAD -- engine contracts reader
TMP="$(mktemp -d /tmp/pd-golden-XXXXXX)"; trap 'git -C "$MAIN" worktree remove --force "$TMP" >/dev/null 2>&1 || true' EXIT
git worktree add --detach "$TMP" "$BASE"
OUT="$("$PYTHON_BIN" -I "$MAIN/tests/fixtures/read-failure-grid/generate.py" --repo "$TMP" --out "$OUT_PATH" --base-commit "$BASE" | tee /dev/stderr)"; test "${OUT##*$'\n'}" = "EXIT=0"'''
CELL_KEY = (
    "<mask 10진>:<repeated 0|1> — mask 의 비트 i(LSB=0) 가 1 이면 "
    "이 파일의 check_ids[i] ∈ 실패 집합"
)
EXCEPTION_RULE = (
    "read.convergence ∈ 출구 실패 집합 → 재디스패치 0회 (재정 T28 ⒟ · §3 ②)"
)
EXCEPTION_PREDICATE = (
    'repeated == 1 and (mask & (1 << check_ids.index("read.convergence"))) != 0'
)
EXCEPTION_MEANING = "값은 그대로 · 출구 경로에서 도달 불능 표지"

COUNT_KEY_SLUGS = {
    "halt_null": "halt/null",
    "escalate_null": "escalate/null",
    "escalate_repeat": "escalate/국면 간 변이 재현 — 코드 결함 의심",
    "stage_error": "StageError",
    "total": "total",
}

CONSTRAINT_IDS = (
    "manifest.type",
    "top.keys.exact",
    "comment.type",
    "comment.contains.T26",
    "comment.contains.T28",
    "comment.contains.T29",
    "base_commit.eq",
    "generator.eq",
    "generation_command.eq",
    "check_ids.type",
    "check_ids.items.str",
    "check_ids.items.nonempty",
    "check_ids.unique",
    "check_ids.expected_set",
    "cell_key.eq",
    "expected_counts.type",
    "expected_counts.keys.exact",
    "expected_counts.halt_null.type",
    "expected_counts.escalate_null.type",
    "expected_counts.escalate_repeat.type",
    "expected_counts.stage_error.type",
    "expected_counts.total.type",
    "expected_counts.halt_null.eq",
    "expected_counts.escalate_null.eq",
    "expected_counts.escalate_repeat.eq",
    "expected_counts.stage_error.eq",
    "expected_counts.total.eq",
    "exceptions.type",
    "exceptions.len1",
    "exception.item.type",
    "exception.keys.exact",
    "exception.id.eq",
    "exception.rule.eq",
    "exception.predicate.eq",
    "exception.meaning.eq",
    "exception.cell_count.type",
    "exception.cell_count.eq",
    "exception.cells.type",
    "exception.cells.items.str",
    "exception.cells.items.nonempty",
    "exception.cells.unique",
    "exception.cells.set",
    "cells.type",
    "cells.keys.exact",
    "cells.value.type",
    "cells.value.sentinel",
    "cells.value.len2",
    "cells.value.action_vocab",
    "cells.value.label_type",
    "provenance.type",
    "provenance.keys.exact",
    "provenance.tree_head.eq",
    "provenance.read_module.type",
    "provenance.read_module.absolute",
    "provenance.run_checks_module.type",
    "provenance.run_checks_module.absolute",
    "provenance.contract.type",
    "provenance.contract.absolute",
    "provenance.out.type",
    "provenance.out.absolute",
    "provenance.engine_path.type",
    "provenance.engine_path.len1",
    "provenance.engine_path.items.str",
    "provenance.engine_path.absolute",
    "provenance.reader_path.type",
    "provenance.reader_path.len1",
    "provenance.reader_path.items.str",
    "provenance.reader_path.absolute",
    "provenance.generated_at.type",
    "provenance.generated_at.iso",
)

_TOP_KEYS = {
    "$comment",
    "base_commit",
    "provenance",
    "generator",
    "generation_command",
    "check_ids",
    "cell_key",
    "expected_counts",
    "exceptions",
    "cells",
}
_PROVENANCE_KEYS = {
    "tree_head",
    "read_module",
    "run_checks_module",
    "contract",
    "engine_path",
    "reader_path",
    "out",
    "generated_at",
}
_EXCEPTION_KEYS = {"id", "rule", "predicate", "meaning", "cell_count", "cells"}
_ACTIONS = {"halt", "reject-upstream", "escalate"}
_CELL_KEYS = {f"{mask}:{repeated}" for mask in range(1, 1 << 12) for repeated in (0, 1)}


def _violation(out: list[str], constraint_id: str, description: str) -> None:
    out.append(f"{constraint_id}: {description}")


def _validate_cells(cells: Any, violations: list[str]) -> bool:
    """cells DAG를 검사하고, 뒤 필드가 의존할 수 있는 완전 통과 여부를 돌려준다."""
    if not isinstance(cells, dict):
        _violation(violations, "cells.type", "cells가 dict가 아니다")
        return False
    if set(cells) != _CELL_KEYS:
        _violation(violations, "cells.keys.exact", "cells 키 우주가 8,190개 정본과 다르다")
        return False

    valid = True
    for key, value in cells.items():
        if isinstance(value, str):
            if value != "StageError":
                _violation(violations, "cells.value.sentinel", f"{key}의 문자열 sentinel이 잘못됐다")
                valid = False
            continue
        if not isinstance(value, list):
            _violation(violations, "cells.value.type", f"{key}의 값 타입이 허용되지 않는다")
            valid = False
            continue
        if len(value) != 2:
            _violation(violations, "cells.value.len2", f"{key}의 배열 길이가 2가 아니다")
            valid = False
            continue
        if value[0] not in _ACTIONS:
            _violation(violations, "cells.value.action_vocab", f"{key}의 action이 허용 어휘가 아니다")
            valid = False
            continue
        if value[1] is not None and not isinstance(value[1], str):
            _violation(violations, "cells.value.label_type", f"{key}의 label이 str|null이 아니다")
            valid = False
    return valid


def _validate_path_field(
    provenance: dict[str, Any], field: str, violations: list[str]
) -> None:
    prefix = f"provenance.{field}"
    value = provenance[field]
    if not isinstance(value, str):
        _violation(violations, f"{prefix}.type", f"{field}가 str이 아니다")
    elif not os.path.isabs(value):
        _violation(violations, f"{prefix}.absolute", f"{field}가 절대경로가 아니다")


def _validate_path_list(
    provenance: dict[str, Any], field: str, violations: list[str]
) -> None:
    prefix = f"provenance.{field}"
    value = provenance[field]
    if not isinstance(value, list):
        _violation(violations, f"{prefix}.type", f"{field}가 list가 아니다")
        return
    if len(value) != 1:
        _violation(violations, f"{prefix}.len1", f"{field}의 원소 수가 1이 아니다")
        return
    if not isinstance(value[0], str):
        _violation(violations, f"{prefix}.items.str", f"{field} 원소가 str이 아니다")
        return
    if not os.path.isabs(value[0]):
        _violation(violations, f"{prefix}.absolute", f"{field} 원소가 절대경로가 아니다")


def validate_manifest(
    manifest: dict,
    *,
    expected_check_ids: set[str],
    required_base_commit: str,
    required_tree_head: str,
) -> list[str]:
    """manifest 위반 목록을 돌려준다. 빈 목록이면 모든 정적 제약을 통과했다."""
    violations: list[str] = []
    if not isinstance(manifest, dict):
        _violation(violations, "manifest.type", "manifest 최상위가 dict가 아니다")
        return violations
    if set(manifest) != _TOP_KEYS:
        _violation(violations, "top.keys.exact", "최상위 키 집합이 정본과 다르다")
        return violations

    comment = manifest["$comment"]
    if not isinstance(comment, str):
        _violation(violations, "comment.type", "$comment가 str이 아니다")
    else:
        for marker, constraint_id in (
            ("T26 §3 ②", "comment.contains.T26"),
            ("T28", "comment.contains.T28"),
            ("T29", "comment.contains.T29"),
        ):
            if marker not in comment:
                _violation(violations, constraint_id, f"$comment에 {marker!r}가 없다")

    if manifest["base_commit"] != required_base_commit:
        _violation(violations, "base_commit.eq", "base_commit이 요구값과 다르다")
    if manifest["generator"] != GENERATOR:
        _violation(violations, "generator.eq", "generator 경로가 정본과 다르다")
    if manifest["generation_command"] != GENERATION_COMMAND:
        _violation(violations, "generation_command.eq", "generation_command가 정본과 다르다")
    if manifest["cell_key"] != CELL_KEY:
        _violation(violations, "cell_key.eq", "cell_key 설명이 정본과 다르다")

    check_ids = manifest["check_ids"]
    check_ids_valid = False
    if not isinstance(check_ids, list):
        _violation(violations, "check_ids.type", "check_ids가 list가 아니다")
    elif not all(isinstance(item, str) for item in check_ids):
        _violation(violations, "check_ids.items.str", "check_ids 원소가 모두 str이 아니다")
    elif not all(check_ids):
        _violation(violations, "check_ids.items.nonempty", "check_ids에 빈 문자열이 있다")
    elif len(check_ids) != len(set(check_ids)):
        _violation(violations, "check_ids.unique", "check_ids가 고유하지 않다")
    elif len(check_ids) != 12 or set(check_ids) != expected_check_ids:
        _violation(violations, "check_ids.expected_set", "check_ids 집합이 요구된 12개 ID와 다르다")
    else:
        check_ids_valid = True

    cells_valid = _validate_cells(manifest["cells"], violations)

    expected_counts = manifest["expected_counts"]
    count_types_valid = False
    if not isinstance(expected_counts, dict):
        _violation(violations, "expected_counts.type", "expected_counts가 dict가 아니다")
    elif set(expected_counts) != set(COUNT_KEY_SLUGS.values()):
        _violation(violations, "expected_counts.keys.exact", "expected_counts 키 집합이 정본과 다르다")
    else:
        count_types_valid = True
        for slug, key in COUNT_KEY_SLUGS.items():
            if type(expected_counts[key]) is not int:
                _violation(violations, f"expected_counts.{slug}.type", f"{key}가 정확한 int 타입이 아니다")
                count_types_valid = False
        if count_types_valid and cells_valid:
            recomputed = {key: 0 for key in COUNT_KEY_SLUGS.values()}
            for value in manifest["cells"].values():
                if value == "StageError":
                    recomputed["StageError"] += 1
                else:
                    label = "null" if value[1] is None else value[1]
                    bucket = f"{value[0]}/{label}"
                    if bucket in recomputed:
                        recomputed[bucket] += 1
                recomputed["total"] += 1
            for slug, key in COUNT_KEY_SLUGS.items():
                if expected_counts[key] != recomputed[key]:
                    _violation(violations, f"expected_counts.{slug}.eq", f"{key}가 cells 실측과 다르다")

    exceptions = manifest["exceptions"]
    if not isinstance(exceptions, list):
        _violation(violations, "exceptions.type", "exceptions가 list가 아니다")
    elif len(exceptions) != 1:
        _violation(violations, "exceptions.len1", "exceptions 길이가 1이 아니다")
    elif not isinstance(exceptions[0], dict):
        _violation(violations, "exception.item.type", "exceptions[0]이 dict가 아니다")
    elif set(exceptions[0]) != _EXCEPTION_KEYS:
        _violation(violations, "exception.keys.exact", "exceptions[0] 키 집합이 정본과 다르다")
    else:
        exception = exceptions[0]
        if exception["id"] != "T28-beta":
            _violation(violations, "exception.id.eq", "예외 id가 T28-beta가 아니다")
        if exception["rule"] != EXCEPTION_RULE:
            _violation(violations, "exception.rule.eq", "예외 rule이 정본과 다르다")
        if exception["predicate"] != EXCEPTION_PREDICATE:
            _violation(violations, "exception.predicate.eq", "예외 predicate가 정본과 다르다")
        if exception["meaning"] != EXCEPTION_MEANING:
            _violation(violations, "exception.meaning.eq", "예외 meaning이 정본과 다르다")

        cell_count = exception["cell_count"]
        if type(cell_count) is not int:
            _violation(violations, "exception.cell_count.type", "예외 cell_count가 정확한 int 타입이 아니다")
        elif cell_count != 2048:
            _violation(violations, "exception.cell_count.eq", "예외 cell_count가 2048이 아니다")

        beta_cells = exception["cells"]
        if not isinstance(beta_cells, list):
            _violation(violations, "exception.cells.type", "예외 cells가 list가 아니다")
        elif not all(isinstance(item, str) for item in beta_cells):
            _violation(violations, "exception.cells.items.str", "예외 cells 원소가 모두 str이 아니다")
        elif not all(beta_cells):
            _violation(violations, "exception.cells.items.nonempty", "예외 cells에 빈 문자열이 있다")
        elif len(beta_cells) != len(set(beta_cells)):
            _violation(violations, "exception.cells.unique", "예외 cells가 고유하지 않다")
        elif check_ids_valid:
            convergence_bit = check_ids.index("read.convergence")
            required_beta = {
                f"{mask}:1"
                for mask in range(1, 1 << 12)
                if (mask >> convergence_bit) & 1
            }
            if set(beta_cells) != required_beta:
                _violation(violations, "exception.cells.set", "예외 cells가 고정 β 식의 집합과 다르다")

    provenance = manifest["provenance"]
    if not isinstance(provenance, dict):
        _violation(violations, "provenance.type", "provenance가 dict가 아니다")
    elif set(provenance) != _PROVENANCE_KEYS:
        _violation(violations, "provenance.keys.exact", "provenance 키 집합이 정본과 다르다")
    else:
        if provenance["tree_head"] != required_tree_head:
            _violation(violations, "provenance.tree_head.eq", "tree_head가 요구된 전체 SHA와 다르다")
        for field in ("read_module", "run_checks_module", "contract", "out"):
            _validate_path_field(provenance, field, violations)
        _validate_path_list(provenance, "engine_path", violations)
        _validate_path_list(provenance, "reader_path", violations)
        generated_at = provenance["generated_at"]
        if not isinstance(generated_at, str):
            _violation(violations, "provenance.generated_at.type", "generated_at이 str이 아니다")
        else:
            try:
                datetime.fromisoformat(generated_at)
            except ValueError:
                _violation(violations, "provenance.generated_at.iso", "generated_at이 ISO 8601이 아니다")

    return violations
