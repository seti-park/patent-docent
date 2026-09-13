# -*- coding: utf-8 -*-
"""L0 규칙이 받는 입력 묶음(`L0Context`)과 돌려주는 산출(`RuleResult`), 그리고 법 객체(`L0Law`).

법 객체는 `contracts/l0-format.yaml`(규칙 문언의 정본)과 `contracts/format-parameters.yaml`(모든 수치의
정본 · 재정 N-D11)을 읽어 **포인터를 값으로 해소**한다. 규칙 구현은 수치·슬롯명·예외 목록·정규식을
리터럴로 갖지 않고 전부 이 객체에서 받는다 — 시트가 바뀌면 판정이 따라 바뀌어야 하고, 그 연동은
사본으로는 보장되지 않는다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import yaml

from reader.lib.report import CheckRow

from ...annotation.parse import Parsed
from ...annotation.strip import Stripped
from ...stages import StageError

L0_FORMAT_REL = ("contracts", "l0-format.yaml")
POINTER_PREFIX = "format-parameters.yaml#"


def _load_yaml(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise StageError(f"계약 파일이 없다: {path}") from exc
    if not isinstance(data, dict):
        raise StageError(f"계약 최상위가 매핑이 아니다: {path}")
    return data


@dataclass(frozen=True)
class L0Law:
    """`l0-format.yaml` + 그것이 가리키는 시트. 값 조회는 전부 포인터 경유."""

    doc: dict
    sheet: dict
    repo: str

    @classmethod
    def load(cls, repo: str) -> "L0Law":
        doc = _load_yaml(os.path.join(repo, *L0_FORMAT_REL))
        source = str(doc.get("params_source") or "")
        if not source:
            raise StageError("l0-format.yaml 에 params_source 가 없다 — 시트 위치를 알 수 없다")
        sheet = _load_yaml(os.path.join(repo, *source.split("/")))
        if "parameters" not in sheet:
            raise StageError(f"형식 파라미터 시트에 parameters 블록이 없다: {source}")
        return cls(doc=doc, sheet=sheet, repo=repo)

    @property
    def version(self) -> str:
        return str(self.doc.get("version"))

    def param(self, pointer: str) -> Any:
        """`format-parameters.yaml#a.b` → 시트 `parameters.a.b.value`."""
        if not pointer.startswith(POINTER_PREFIX):
            raise StageError(f"시트 포인터 형식이 아니다: {pointer!r}")
        dotted = pointer[len(POINTER_PREFIX):]
        cursor: Any = self.sheet["parameters"]
        trail: list[str] = []
        for key in dotted.split("."):
            trail.append(key)
            if not isinstance(cursor, dict) or key not in cursor:
                raise StageError(f"형식 파라미터 시트에 {'.'.join(trail)} 이 없다(포인터 {pointer})")
            cursor = cursor[key]
        if not isinstance(cursor, dict) or "value" not in cursor:
            raise StageError(f"시트 항목 {dotted} 에 value 키가 없다(포인터 {pointer})")
        return cursor["value"]

    def block(self, name: str) -> dict:
        value = self.doc.get(name)
        if not isinstance(value, dict):
            raise StageError(f"l0-format.yaml 에 {name} 블록이 없다")
        return value

    def rule_entry(self, rule_id: str) -> dict:
        for entry in self.doc.get("rules") or []:
            if isinstance(entry, dict) and entry.get("id") == rule_id:
                return entry
        raise StageError(f"l0-format.yaml#rules[] 에 {rule_id!r} 가 없다")

    def rule_params(self, rule_id: str) -> dict[str, Any]:
        """규칙 항목의 `params`(문자열 또는 배열) → `{pointer: value}`."""
        raw = self.rule_entry(rule_id).get("params")
        pointers = [raw] if isinstance(raw, str) else list(raw or [])
        return {pointer: self.param(pointer) for pointer in pointers}

    def param_of(self, rule_id: str, tail: str) -> Any:
        """규칙 `params` 중 `#<tail>` 로 끝나는 포인터의 값 하나."""
        for pointer, value in self.rule_params(rule_id).items():
            if pointer == POINTER_PREFIX + tail:
                return value
        raise StageError(f"{rule_id} 의 params 에 #{tail} 포인터가 없다 — 값은 계약에서 온다")


@dataclass
class L0Context:
    """규칙 하나가 보는 세계 — 전부 읽기 전용."""

    law: L0Law
    repo: str
    parsed: Parsed
    stripped: Stripped | None
    index: dict | None
    frozen: dict
    spec_digest: str
    meta: dict
    manifest: dict | None = None
    inactive: dict = field(default_factory=dict)
    url_re: Any = None
    slot_enum: tuple[str, ...] = ()


@dataclass
class RuleResult:
    row: CheckRow
    defects: list[dict] = field(default_factory=list)
    flags: list[dict] = field(default_factory=list)

    def defect(self, rule: str, tweet: int | None, sentence: int | None, expected: str, observed: str,
               fix_directive: str) -> None:
        locus = f"T{tweet}" + (f"/S{sentence}" if sentence else "") if tweet else "thread"
        self.row.add(rule, locus, observed, expected, fix_directive)
        self.defects.append({
            "rule": rule, "locus": {"tweet": tweet, "sentence": sentence},
            "expected": expected, "observed": observed, "fix_directive": fix_directive,
        })

    def flag(self, rule: str, tweet: int | None, sentence: int | None, note: str) -> None:
        self.flags.append({"rule": rule, "locus": {"tweet": tweet, "sentence": sentence}, "note": note,
                           "origin": "advisory-rule"})


__all__ = ["L0Context", "L0Law", "RuleResult", "POINTER_PREFIX"]
