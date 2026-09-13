# -*- coding: utf-8 -*-
"""변주 → 펜 배정 등록부 — 계약 `contracts/stages/compose.yaml#lane.variants` 의 유일한 독자.

값(변주 id · vendor · model · effort · 비교 축)을 여기 리터럴로 두지 않는다. 계약이 정본이고 이 모듈은
그것을 읽어 형태를 검증한 뒤 돌려준다(재정 R10 · T64 ③). `run.yaml#pens` 에 기입되는 행도 이 목록
그대로다(SPEC §7.3).
"""

from __future__ import annotations

from ..paths import PathContractError, load_stage_contract

STAGE_ID = "compose"
PEN_KEYS: tuple[str, ...] = ("variant", "vendor", "model", "effort")


class PenRegistryError(PathContractError):
    """계약의 펜 배정이 형태를 어겼다(빈 목록 · 키 누락 · 변주 중복 · 어휘 불일치)."""


def pens(repo: str | None = None, contract: dict | None = None) -> list[dict]:
    """계약 `lane.variants` → `[{variant, vendor, model, effort}, …]`(계약 순서 · 사본)."""
    contract = contract or load_stage_contract(STAGE_ID, repo)
    lane = contract.get("lane") or {}
    raw = lane.get("variants")
    if not isinstance(raw, list) or not raw:
        raise PenRegistryError("compose.yaml#lane.variants 가 비어 있다 — 펜 배정 없이는 변주를 만들 수 없다")
    out: list[dict] = []
    seen: set[str] = set()
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise PenRegistryError(f"compose.yaml#lane.variants[{index}] 가 매핑이 아니다")
        missing = [key for key in PEN_KEYS if not str(entry.get(key, "")).strip()]
        if missing:
            raise PenRegistryError(f"compose.yaml#lane.variants[{index}] 에 {', '.join(missing)} 가 없다 — 모델·effort 는 하드 지정이다")
        variant = str(entry["variant"])
        if variant in seen:
            raise PenRegistryError(f"compose.yaml#lane.variants 에 변주 {variant!r} 가 둘 이상이다")
        seen.add(variant)
        out.append({key: str(entry[key]) for key in PEN_KEYS})
    membership = ((lane.get("lane_id_vocabulary") or {}).get("membership") or {}).get("task") or []
    if [pen["variant"] for pen in out] != [str(task) for task in membership]:
        raise PenRegistryError(
            "compose.yaml#lane.variants 의 변주 목록과 lane_id_vocabulary.membership.task 가 다르다 — "
            f"{[pen['variant'] for pen in out]} ≠ {membership}"
        )
    return out


def pen_for(variant: str, repo: str | None = None, contract: dict | None = None) -> dict:
    for pen in pens(repo, contract):
        if pen["variant"] == variant:
            return dict(pen)
    raise PenRegistryError(f"compose.yaml#lane.variants 에 변주 {variant!r} 가 없다")


def variant_ids(repo: str | None = None, contract: dict | None = None) -> tuple[str, ...]:
    return tuple(pen["variant"] for pen in pens(repo, contract))


def comparison_axis(repo: str | None = None, contract: dict | None = None) -> str:
    contract = contract or load_stage_contract(STAGE_ID, repo)
    axis = (contract.get("lane") or {}).get("comparison_axis")
    if not isinstance(axis, str) or not axis.strip():
        raise PenRegistryError("compose.yaml#lane.comparison_axis 가 없다 — 토너먼트 행의 비교 축을 정할 수 없다(R10 규약 4)")
    return axis


def pen_assignment(pen: dict) -> dict:
    """프런트매터 `pen` 과 대조할 3키 `{vendor, model, effort}`."""
    return {"vendor": pen["vendor"], "model": pen["model"], "effort": pen["effort"]}


__all__ = ["PEN_KEYS", "PenRegistryError", "comparison_axis", "pen_assignment", "pen_for", "pens", "variant_ids"]
