#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""READ failure[] 계약 관문(재정 T26·T28·T29·T30).

G1 골격, G2 완전성, G3 재시도 등식, G4 국면, G5 진입 표지, G6 종단 어휘를
YAML만 읽어 대조한다. 엔진은 import하지 않는다. 종료 코드는 0/1/2다.
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path
from typing import Any, Callable

import yaml


TERMINAL_ACTIONS = ("halt", "reject-upstream", "escalate")
KINDS = ("retry-repeat", "gate-escalation", "upstream-defect")
POINT_IDS = ("early", "exit")
APPROVED_RETRY_CHECKS = {
    # 재정 T26 ⒜ ③·T28 β: convergence는 early에만, exit는 실제 재시도 8종.
    "early": ("read.claim-inventory", "read.dependency-parse", "read.convergence"),
    "exit": (
        "read.schema",
        "read.claim-inventory",
        "read.dependency-parse",
        "read.verbatim",
        "read.pointer-resolve",
        "read.coverage",
        "read.value-derivation",
        "read.bibliography",
    ),
}


def _approved(
    *,
    checks: tuple[str, ...] | None = None,
    kind: str | None = None,
    action: str,
    then: str | None = None,
    reason_label: str | None = None,
    points: tuple[str, ...] | None = None,
    judged_at: str | None = None,
) -> dict[str, Any]:
    return {
        "checks": checks,
        "kind": kind,
        "action": action,
        "then": then,
        "reason_label": reason_label,
        "points": points,
        "judged_at": judged_at,
    }


APPROVED_FAILURE_TABLE = (
    # 1 T25·T26
    _approved(checks=("read.schema",), action="retry(1)", then="halt", points=("exit",)),
    # 2 T24·T25
    _approved(checks=("read.source-digest",), action="halt"),
    # 3 T29
    _approved(checks=("read.input-digest",), action="halt", reason_label="환경 오류", judged_at="entry"),
    # 4 T16 §6 ⑤
    _approved(kind="retry-repeat", action="escalate", reason_label="국면 간 변이 재현 — 코드 결함 의심"),
    # 5 P-4·T28
    _approved(checks=("read.convergence",), action="retry(1)", then="escalate", points=("early",)),
    # 6 T22
    _approved(checks=("read.lane-log-shape",), action="escalate"),
    # 7 T22
    _approved(checks=("read.lane-log-digest-value",), action="escalate"),
    # 8 T17·T26 ⒜ ③
    _approved(checks=("read.claim-inventory", "read.dependency-parse"), action="retry(1)", then="escalate", points=("early", "exit")),
    # 9 T17·T26 ⒜ ③
    _approved(checks=("read.verbatim", "read.pointer-resolve", "read.coverage", "read.value-derivation", "read.bibliography"), action="retry(1)", then="escalate", points=("exit",)),
    # 10 P-3
    _approved(kind="gate-escalation", action="escalate", reason_label="독해 프로파일 상신"),
    # 11 D6·T2
    _approved(kind="upstream-defect", action="reject-upstream"),
)

DEFAULT_CONTRACT = Path("contracts/stages/read.yaml")
_RETRY_RE = re.compile(r"retry\((\d+)\)\Z")


def _add(errors: list[str], gate: str, message: str) -> None:
    errors.append(f"{gate}: {message}")


def _rows(contract: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    value = contract.get("failure")
    if not isinstance(value, list):
        _add(errors, "G1", "failure가 list가 아니다")
        return []
    if any(not isinstance(row, dict) for row in value):
        _add(errors, "G1", "failure 원소가 dict가 아니다")
        return []
    return value


def _machine(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checks": tuple(row["checks"]) if isinstance(row.get("checks"), list) else row.get("checks"),
        "kind": row.get("kind"),
        "action": row.get("action"),
        "then": row.get("then"),
        "reason_label": row.get("reason_label"),
        "points": tuple(row["points"]) if isinstance(row.get("points"), list) else row.get("points"),
        "judged_at": row.get("judged_at"),
    }


def _declared_ids(contract: dict[str, Any], key: str, errors: list[str]) -> list[str] | None:
    rows = contract.get(key)
    if not isinstance(rows, list):
        _add(errors, "G2", f"{key}가 list가 아니다")
        return None
    ids: list[str] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            _add(errors, "G2", f"{key}[{index}]의 id 선언 형식이 잘못됐다")
            return None
        ids.append(row["id"])
    if len(ids) != len(set(ids)):
        _add(errors, "G2", f"{key} id가 중복됐다")
        return None
    return ids


def _point_rows(contract: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    points = (contract.get("retry_budget") or {}).get("points")
    if not isinstance(points, list):
        _add(errors, "G3", "retry_budget.points가 list가 아니다")
        return {}
    ids = [p.get("id") for p in points if isinstance(p, dict)]
    if len(ids) != len(points) or len(ids) != len(set(ids)) or set(ids) != set(POINT_IDS):
        _add(errors, "G3", f"판정점 id가 정확히 {POINT_IDS!r} 각 1행이 아니다: {ids!r}")
        return {}
    return {p["id"]: p for p in points}


def validate_contract(contract: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["G1: YAML 최상위가 dict가 아니다"]
    rows = _rows(contract, errors)

    # G1 — 승인된 11행의 기계 필드와 실제 키 열을 순서까지 고정한다.
    if len(rows) != len(APPROVED_FAILURE_TABLE):
        _add(errors, "G1", f"failure 행 수 기대 {len(APPROVED_FAILURE_TABLE)}, 실제 {len(rows)}")
    for index, (actual, approved) in enumerate(zip(rows, APPROVED_FAILURE_TABLE), 1):
        checks = actual.get("checks")
        if "checks" in actual and (
            not isinstance(checks, list)
            or not checks
            or any(not isinstance(item, str) or not item for item in checks)
            or len(checks) != len(set(checks))
        ):
            _add(errors, "G1", f"{index}행 checks가 비공 문자열 고유 list가 아니다")
        if ("checks" in actual) == ("kind" in actual):
            _add(errors, "G1", f"{index}행은 checks xor kind가 아니다")
        if _machine(actual) != approved:
            _add(errors, "G1", f"{index}행 기계 필드 기대={approved!r} 실제={_machine(actual)!r}")
        machine_keys = {key for key, value in approved.items() if value is not None}
        expected_keys = machine_keys | {"condition", "note"}
        if set(actual) != expected_keys:
            _add(errors, "G1", f"{index}행 키 기대={sorted(expected_keys)!r} 실제={sorted(actual)!r}")
        for prose in ("condition", "note"):
            if not isinstance(actual.get(prose), str) or not actual[prose]:
                _add(errors, "G1", f"{index}행 {prose}가 비공 str이 아니다")
    kinds = [row.get("kind") for row in rows if "kind" in row]
    if len(kinds) != len(set(kinds)) or set(kinds) != set(KINDS):
        _add(errors, "G1", f"kind 사전/유일성 위반: {kinds!r}")

    # G2 — entry ∪ exit ∪ judged_here 와 failure checks 합집합의 양방향 상등.
    entry_ids = _declared_ids(contract, "checks_on_entry", errors)
    exit_ids = _declared_ids(contract, "checks_before_exit", errors)
    judged = (contract.get("early_phase_spec") or {}).get("judged_here")
    judged_ok = isinstance(judged, list) and bool(judged) and all(isinstance(x, str) and x for x in judged) and len(judged) == len(set(judged))
    if not judged_ok:
        _add(errors, "G2", "early_phase_spec.judged_here가 비공 문자열 고유 list가 아니다")
    point_map = _point_rows(contract, errors)
    if entry_ids is not None and exit_ids is not None and judged_ok:
        declared = set(entry_ids) | set(exit_ids) | set(judged)
        row_ids = {check_id for row in rows for check_id in row.get("checks", []) if isinstance(check_id, str)}
        if declared != row_ids:
            _add(errors, "G2", f"선언↔failure 차집합: 선언에만={sorted(declared-row_ids)!r}, failure에만={sorted(row_ids-declared)!r}")
        early_phase_ids = {
            row["id"]
            for row in contract.get("checks_before_exit", [])
            if isinstance(row, dict) and isinstance(row.get("phases"), list) and "early" in row["phases"]
        }
        point_early = set(point_map.get("early", {}).get("checks", []))
        if set(judged) != point_early or set(judged) != early_phase_ids:
            _add(errors, "G2", f"조기 선언 세 벌 불일치: judged={sorted(judged)!r}, point={sorted(point_early)!r}, phases={sorted(early_phase_ids)!r}")

    # G3 — 판정점 목록/승인 집합/행 합집합/예산의 정확 등식.
    exit_set = set(exit_ids or [])
    for point in POINT_IDS:
        point_row = point_map.get(point)
        if not point_row:
            continue
        checks = point_row.get("checks")
        if not isinstance(checks, list) or not checks or any(not isinstance(x, str) or not x for x in checks) or len(checks) != len(set(checks)):
            _add(errors, "G3", f"{point}.checks가 비공 문자열 고유 list가 아니다")
            continue
        actual = set(checks)
        if not actual <= exit_set:
            _add(errors, "G3", f"{point}.checks가 출구 12 id의 부분집합이 아니다: {sorted(actual-exit_set)!r}")
        approved = set(APPROVED_RETRY_CHECKS[point])
        if actual != approved:
            _add(errors, "G3", f"{point} 승인 집합 차집합: 승인에만={sorted(approved-actual)!r}, 계약에만={sorted(actual-approved)!r}")
        union: set[str] = set()
        retries: set[int] = set()
        for row in rows:
            match = _RETRY_RE.fullmatch(str(row.get("action", "")))
            points = row.get("points")
            if match and isinstance(points, list) and point in points:
                union.update(row.get("checks") or [])
                retries.add(int(match.group(1)))
        if actual != union:
            _add(errors, "G3", f"{point} retry 행 등식 차집합: 목록에만={sorted(actual-union)!r}, 행에만={sorted(union-actual)!r}")
        budget = point_row.get("max_retries")
        if type(budget) is not int:
            _add(errors, "G3", f"{point}.max_retries 타입이 int가 아니다: {type(budget).__name__}")
        elif retries != {budget}:
            _add(errors, "G3", f"{point} retry(n)={sorted(retries)!r}, max_retries={budget!r}")
    for index, row in enumerate(rows, 1):
        retry = bool(_RETRY_RE.fullmatch(str(row.get("action", ""))))
        if retry != ("points" in row) or retry != ("then" in row):
            _add(errors, "G3", f"{index}행 retry(n)⇔points⇔then 위반")
        if "points" in row:
            points = row["points"]
            if not isinstance(points, list) or not points or len(points) != len(set(points)) or not set(points) <= set(POINT_IDS):
                _add(errors, "G3", f"{index}행 points 형식/어휘 위반: {points!r}")

    # G4 — phases의 정확한 국면과 retry 행 points 포함.
    phase_map: dict[str, set[str]] = {}
    for index, row in enumerate(contract.get("checks_before_exit") or [], 1):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            continue
        phases = row.get("phases")
        valid = isinstance(phases, list) and bool(phases) and len(phases) == len(set(phases)) and set(phases) <= set(POINT_IDS) and "exit" in phases
        if not valid:
            _add(errors, "G4", f"checks_before_exit[{index}] phases 위반: {phases!r}")
            continue
        phase_map[row["id"]] = set(phases)
        early_expected = row["id"] in set(APPROVED_RETRY_CHECKS["early"])
        if ("early" in phases) != early_expected:
            _add(errors, "G4", f"{row['id']} early phase 귀속이 early 목록과 다르다")
    for index, row in enumerate(rows, 1):
        if _RETRY_RE.fullmatch(str(row.get("action", ""))):
            for check_id in row.get("checks") or []:
                if check_id not in phase_map or not set(row.get("points") or []) <= phase_map[check_id]:
                    _add(errors, "G4", f"{index}행 {check_id} phases가 points를 포함하지 않는다")

    # G5 — 진입 검사는 전용 표지·halt·무points이고 다른 행에는 judged_at이 없다.
    entry_set = set(entry_ids or [])
    for index, row in enumerate(rows, 1):
        checks = set(row.get("checks") or [])
        is_entry = bool(checks & entry_set)
        if is_entry:
            if not checks <= entry_set or row.get("judged_at") != "entry" or row.get("action") != "halt" or "points" in row:
                _add(errors, "G5", f"{index}행 진입 표지/조치/points 위반")
            for point in point_map.values():
                if checks & set(point.get("checks") or []):
                    _add(errors, "G5", f"{index}행 진입 id가 재시도 목록에 들었다")
        elif "judged_at" in row:
            _add(errors, "G5", f"{index}행 비진입 검사에 judged_at이 있다")

    # G6 — 종단 어휘.
    for index, row in enumerate(rows, 1):
        action = row.get("action")
        retry = bool(_RETRY_RE.fullmatch(str(action or "")))
        if retry:
            if row.get("then") not in TERMINAL_ACTIONS:
                _add(errors, "G6", f"{index}행 retry의 then이 종단 어휘가 아니다: {row.get('then')!r}")
        elif action not in TERMINAL_ACTIONS or "then" in row:
            _add(errors, "G6", f"{index}행 비retry action/then 위반: {action!r}/{row.get('then')!r}")
    return errors


def _failure_row(contract: dict[str, Any], *, check: str | None = None, kind: str | None = None) -> dict[str, Any]:
    for row in contract["failure"]:
        if check is not None and check in (row.get("checks") or []):
            return row
        if kind is not None and row.get("kind") == kind:
            return row
    raise KeyError(check or kind)


def _phase_row(contract: dict[str, Any], check: str) -> dict[str, Any]:
    return next(row for row in contract["checks_before_exit"] if row.get("id") == check)


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _mutations() -> list[Mutation]:
    def add_missing_check(c): c["checks_before_exit"].append({"id": "read.__ghost__", "phases": ["exit"]})
    def add_ghost_row(c): c["failure"].append({"checks": ["read.__ghost__"], "action": "escalate", "condition": "ghost", "note": "ghost"})
    def add_exit_source(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "exit")["checks"].append("read.source-digest")
    def drop_exit_schema(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "exit")["checks"].remove("read.schema")
    def duplicate_check(c): _failure_row(c, check="read.convergence")["checks"].append("read.schema")
    def duplicate_kind(c): c["failure"].append(copy.deepcopy(_failure_row(c, kind="retry-repeat")))
    def bad_kind(c): _failure_row(c, kind="upstream-defect").__setitem__("kind", "__ghost__")
    def both_keys(c): _failure_row(c, check="read.schema").__setitem__("kind", "retry-repeat")
    def no_key(c): _failure_row(c, check="read.schema").pop("checks")
    def early_exit_only(c): _failure_row(c, check="read.verbatim")["points"] = ["early"]
    def no_then(c): _failure_row(c, check="read.schema").pop("then")
    def retry_then(c): _failure_row(c, check="read.schema")["then"] = "retry(1)"
    def no_judged(c): _failure_row(c, check="read.input-digest").pop("judged_at")
    def input_in_exit(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "exit")["checks"].append("read.input-digest")
    def judged_nonentry(c): _failure_row(c, check="read.convergence")["judged_at"] = "entry"
    def input_escalate(c): _failure_row(c, check="read.input-digest")["action"] = "escalate"
    def ghost_phase(c): _phase_row(c, "read.schema")["phases"].append("__ghost_phase__")
    def duplicate_exit_point(c): c["retry_budget"]["points"].append(copy.deepcopy(next(p for p in c["retry_budget"]["points"] if p["id"] == "exit")))
    def false_early(c): _phase_row(c, "read.source-digest")["phases"] = ["early", "exit"]
    def no_exit(c): _phase_row(c, "read.verbatim")["phases"] = ["early"]
    def coherent_retry_tamper(c):
        next(p for p in c["retry_budget"]["points"] if p["id"] == "exit")["checks"].remove("read.value-derivation")
        _failure_row(c, check="read.verbatim")["checks"].remove("read.value-derivation")
        c["failure"].append({"checks": ["read.value-derivation"], "action": "escalate", "condition": "split", "note": "split"})
    def duplicate_exit_decl(c): c["checks_before_exit"].append(copy.deepcopy(_phase_row(c, "read.schema")))
    def duplicate_entry_decl(c): c["checks_on_entry"].append(copy.deepcopy(c["checks_on_entry"][0]))
    def kind_then(c): _failure_row(c, kind="gate-escalation")["then"] = "halt"
    def merge_lanes(c):
        a = _failure_row(c, check="read.lane-log-shape")
        b = _failure_row(c, check="read.lane-log-digest-value")
        a["checks"].append("read.lane-log-digest-value")
        c["failure"].remove(b)
    def swap_tie(c): c["failure"][3], c["failure"][4] = c["failure"][4], c["failure"][3]
    def upstream_halt(c): _failure_row(c, kind="upstream-defect")["action"] = "halt"
    def no_gate_label(c): _failure_row(c, kind="gate-escalation").pop("reason_label")
    def budget_two(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "early")["max_retries"] = 2
    def budget_true(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "early")["max_retries"] = True
    def budget_float(c): next(p for p in c["retry_budget"]["points"] if p["id"] == "early")["max_retries"] = 1.0
    def extra_field(c): _failure_row(c, check="read.schema")["unapproved_machine_field"] = "halt"
    def move_judged(c):
        _failure_row(c, check="read.input-digest").pop("judged_at")
        _failure_row(c, check="read.convergence")["judged_at"] = "entry"
    def ghost_judged(c): c["early_phase_spec"]["judged_here"].append("read.__ghost__")
    def no_condition(c): _failure_row(c, check="read.schema").pop("condition")
    def integer_note(c): _failure_row(c, kind="retry-repeat")["note"] = 0
    return [
        ("01 missing declared check", add_missing_check), ("02 ghost row", add_ghost_row),
        ("03 exit source", add_exit_source), ("04 drop exit schema", drop_exit_schema),
        ("05 duplicate check", duplicate_check), ("06 duplicate kind", duplicate_kind),
        ("07 unknown kind", bad_kind), ("08 checks and kind", both_keys), ("09 no key", no_key),
        ("10 exit-only early point", early_exit_only), ("11 retry no then", no_then),
        ("12 retry then", retry_then), ("13 no judged_at", no_judged), ("14 input in exit", input_in_exit),
        ("15 judged nonentry", judged_nonentry), ("16 input action", input_escalate),
        ("17 ghost phase", ghost_phase), ("18 duplicate exit point", duplicate_exit_point),
        ("19 false early", false_early), ("20 exit missing", no_exit),
        ("21 coherent retry tamper", coherent_retry_tamper), ("22 duplicate exit declaration", duplicate_exit_decl),
        ("23 duplicate entry declaration", duplicate_entry_decl), ("24 kind then", kind_then),
        ("25 merge lanes", merge_lanes), ("26 swap tie", swap_tie), ("27 upstream halt", upstream_halt),
        ("28 gate label", no_gate_label), ("29 retry budget two", budget_two),
        ("30 retry budget bool", budget_true), ("31 retry budget float", budget_float),
        ("32 extra field", extra_field), ("33 move judged_at", move_judged),
        ("34 ghost judged_here", ghost_judged), ("35 no condition", no_condition), ("36 integer note", integer_note),
    ]


def load_contract(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"계약을 읽을 수 없다: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"계약 최상위가 dict가 아니다: {path}")
    return value


def run_self_test(canonical: dict[str, Any]) -> bool:
    failures: list[str] = []
    mutations = _mutations()
    for name, mutate in mutations:
        probe = copy.deepcopy(canonical)
        mutate(probe)
        if not validate_contract(probe):
            failures.append(name)
    print(f"SELF-TEST mutations={len(mutations)} rejected={len(mutations)-len(failures)}")
    if failures:
        print(f"SELF-TEST passed unexpectedly: {failures!r}")
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--self-test", action="store_true")
    try:
        args = parser.parse_args(argv)
        contract = load_contract(args.contract)
    except (SystemExit, ValueError) as exc:
        if isinstance(exc, SystemExit):
            return 2 if exc.code else 0
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        print("EXIT=2")
        return 2
    if args.self_test:
        canonical_errors = validate_contract(contract)
        if canonical_errors:
            print("정본 계약이 승인 골격과 다르다 — self-test 미실행")
            for error in canonical_errors:
                print(error)
            print("EXIT=1")
            return 1
        ok = run_self_test(contract)
        print(f"EXIT={0 if ok else 1}")
        return 0 if ok else 1
    errors = validate_contract(contract)
    for error in errors:
        print(error)
    print(
        f"failure_rows={len(contract.get('failure') or [])} "
        f"early_retry={len(APPROVED_RETRY_CHECKS['early'])} "
        f"exit_retry={len(APPROVED_RETRY_CHECKS['exit'])}"
    )
    print(f"EXIT={0 if not errors else 1}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
