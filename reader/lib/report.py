# -*- coding: utf-8 -*-
"""판정 산출 자료구조 — `Finding` · `CheckRow` · `CheckContext`.

`CheckRow.to_row_dict()` 는 `contracts/schemas/verdict-check-row.schema.json`(재정 N5)의
8키 서식을 만든다. 그 스키마 파일을 여기서 **읽지 않는다** — `reader/` 는 이식 단위이고
`contracts/` 를 참조하는 순간 그 성질이 깨진다(SPEC §6.2 판별식 1). 두 쪽의 동치는
`tests/test_m1_reader.py` 가 실제 스키마로 매 실행 대조한다.

`vacuous` 는 신고값이 아니라 파생값이다(재정 N5 규율 (3)) — 여기 구현이 스키마의 파생
규칙과 어긋나면 공허 2종이 보고에서 사라진다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # 런타임 임포트를 만들지 않는다(모듈 간 결합을 서식 쪽에 두지 않기 위함).
    from .rules import Rules

# 긴 값의 절단 길이. 판정 행은 사람이 읽는 것이므로 원문 전체를 싣지 않는다.
FOUND_MAX_LEN = 200
TRUNCATION_SUFFIX = " …"


def truncate(value: str) -> str:
    """긴 문자열을 200자로 자르고 절단 표지를 붙인다."""
    if len(value) <= FOUND_MAX_LEN:
        return value
    return value[:FOUND_MAX_LEN] + TRUNCATION_SUFFIX


@dataclass(frozen=True)
class Finding:
    """검사 1건의 위반 1건. 좌표·실측·기대를 한 줄에 들고 다닌다."""

    check: str
    rule: str
    locus: str
    found: str
    expected: str
    message: str

    def as_dict(self) -> dict:
        return {
            "check": self.check,
            "rule": self.rule,
            "locus": self.locus,
            "found": self.found,
            "expected": self.expected,
            "message": self.message,
        }


@dataclass
class CheckRow:
    """검사 1종의 판정 행. `to_row_dict()` 가 계약 서식(verdict-check-row/v0)이다."""

    check_id: str
    ruleset: str | None = None
    ruleset_version: str | None = None
    ruleset_size: int | None = None
    checked: int = 0
    findings: list[Finding] = field(default_factory=list)
    extras: dict = field(default_factory=dict)

    @property
    def violations(self) -> int:
        return len(self.findings)

    @property
    def status(self) -> str:
        return "pass" if not self.findings else "fail"

    @property
    def vacuous(self) -> str:
        if self.ruleset_size == 0:
            return "empty-ruleset"
        if self.checked == 0:
            return "empty-target"
        return "none"

    def add(
        self,
        rule: str,
        locus: str,
        found: str,
        expected: str,
        message: str,
    ) -> Finding:
        """이 행에 위반 1건을 등재한다(`check` 는 행의 id 를 그대로 쓴다)."""
        finding = Finding(
            check=self.check_id,
            rule=rule,
            locus=locus,
            found=truncate(found),
            expected=truncate(expected),
            message=message,
        )
        self.findings.append(finding)
        return finding

    def to_row_dict(self) -> dict:
        """verdict-check-row/v0 의 8키 딕셔너리. `extras`·`findings` 는 싣지 않는다."""
        return {
            "check_id": self.check_id,
            "ruleset": self.ruleset,
            "ruleset_version": self.ruleset_version,
            "ruleset_size": self.ruleset_size,
            "checked": self.checked,
            "violations": self.violations,
            "status": self.status,
            "vacuous": self.vacuous,
        }


@dataclass
class CheckContext:
    """검사 입력 일체. 검사는 **읽기 전용**이며 이 안의 객체를 변형하지 않는다."""

    spec: dict
    source_text: str = ""
    rules: "Rules" = None
    schema: dict | None = None
    peer_spec: dict | None = None
    prior_spec: dict | None = None
