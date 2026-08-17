# -*- coding: utf-8 -*-
"""스테이지 러너 3종(`source` · `read` · `freeze`)과 그들이 공유하는 최소 도구.

여기 있는 함수는 전부 **결정론**이며 판단하지 않는다. 판단은 레인(LLM)과 Owner 의 몫이고,
러너는 계약이 정한 자리에 계약이 정한 형태로 산출물을 놓고 검사 결과를 그대로 보고한다.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any

import yaml

from reader.lib.report import CheckRow

DIGEST_PREFIX = "sha256:"


class StageError(Exception):
    """러너 자신의 계약 위반(입력 부재·산출 자리 충돌·보고 서식 위반)."""


def sha256_bytes(payload: bytes) -> str:
    """`sha256:<hex>` 형태의 다이제스트(글로사리 §3 ID 문법)."""
    return DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return sha256_bytes(handle.read())


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def write_json(path: str, payload: Any) -> None:
    """결정론 JSON 쓰기 — 키 정렬 + 고정 들여쓰기 + 끝 개행."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def load_json(path: str) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise StageError(f"YAML 최상위가 매핑이 아니다: {path}")
    return data


def dump_yaml(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)


def worst_status(statuses: list[str]) -> str:
    """`halt` > `reject-upstream` > `escalate` > `ok`.

    조치 어휘 4종의 정본은 SPEC §1.2 C6 이며(`retry(n)`은 스테이지 안에서 소진되므로
    여기 오지 않는다), 순서는 "런이 얼마나 멀리 되돌아가는가"다 — `halt` 는 런을 세우고,
    `reject-upstream` 은 상류 스테이지로 되돌리며, `escalate` 는 Owner 를 부른다.
    """
    order = {"ok": 0, "escalate": 1, "reject-upstream": 2, "halt": 3}
    worst = "ok"
    for status in statuses:
        if order.get(status, 0) > order[worst]:
            worst = status
    return worst


def rows_to_dicts(rows: list[CheckRow]) -> list[dict]:
    return [row.to_row_dict() for row in rows]


def failed_rows(rows: list[CheckRow]) -> list[CheckRow]:
    return [row for row in rows if row.status == "fail"]


def findings_of(rows: list[CheckRow]) -> list[dict]:
    return [finding.as_dict() for row in rows for finding in row.findings]


def failure_entry(contract: dict, needle: str) -> dict:
    """계약의 `failure[]` 에서 조건 문언에 `needle` 이 든 항목을 찾는다.

    조치·사유 표기를 코드에 적지 않기 위한 조회다 — `escalate` 의 사유 라벨
    (`형식 전제 미충족` · `안도감 부적합`)은 계약 파일이 정본이고 러너는 전사할 뿐이다.
    """
    for entry in contract.get("failure") or []:
        if needle in str(entry.get("condition", "")):
            return entry
    raise StageError(f"계약의 failure 목록에 '{needle}' 조건이 없다")


__all__ = [
    "DIGEST_PREFIX",
    "StageError",
    "dump_yaml",
    "failed_rows",
    "failure_entry",
    "findings_of",
    "load_json",
    "load_yaml",
    "read_text",
    "rows_to_dicts",
    "sha256_bytes",
    "sha256_file",
    "worst_status",
    "write_json",
    "write_text",
]
