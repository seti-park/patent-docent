# -*- coding: utf-8 -*-
"""도면 자산층의 공용 조각(재정 2026-09-13 T65 ③ · SPEC §1.8 · §7.5).

여기 있는 것은 **매니페스트 항목의 해석**뿐이다 — 자산 id · 자산 경로 · edit_class 를 항목에서 읽는 규칙 하나.
`figures.select`·`gate`(format.stop-shape · thread.json#images) 가 같은 함수를 부르므로 basename 추정이 두 자리에서
갈리지 않는다(총괄 재량 ⓒ — 매니페스트가 asset_id 를 든다).

호환: 골든 표본(`ledgers/regression/golden/rc-0001-numberless/assets-manifest.json`)은 `figure: fig-NN` 로 자산 id 를
적는다. 그 표기도 읽되, 실물 매니페스트(`figures-manifest/v0`)의 `asset_id` 가 먼저다.
"""

from __future__ import annotations

import os

ASSET_PREFIX = "fig-"
ASSET_EXT = ".png"
FIGURE_PREFIX = "FIG-"


def asset_id_of(item: dict) -> str | None:
    """매니페스트 항목 → 자산 id(`fig-NN`). `asset_id` → `figure`(골든 표기) → `asset_path` basename 순."""
    if not isinstance(item, dict):
        return None
    for key in ("asset_id", "figure"):
        value = item.get(key)
        if isinstance(value, str) and value.startswith(ASSET_PREFIX):
            return value
    path = item.get("asset_path")
    if isinstance(path, str) and path:
        base = os.path.basename(path)
        if base.endswith(ASSET_EXT):
            base = base[: -len(ASSET_EXT)]
        if base.startswith(ASSET_PREFIX):
            return base
    return None


def figure_id_of(item: dict) -> str | None:
    """매니페스트 항목 → 재료 도면 id(`FIG-n`). `figure_id` → `material_figure`(골든 표기)."""
    if not isinstance(item, dict):
        return None
    for key in ("figure_id", "material_figure"):
        value = item.get(key)
        if isinstance(value, str) and value.startswith(FIGURE_PREFIX):
            return value
    return None


def manifest_items(manifest: dict | None) -> list[dict]:
    if not isinstance(manifest, dict):
        return []
    return [item for item in (manifest.get("items") or []) if isinstance(item, dict)]


def asset_classes(manifest: dict | None) -> dict[str, str]:
    """`{asset_id: edit_class}` — format.stop-shape 가 헤더 fig 항목을 해소하는 표."""
    out: dict[str, str] = {}
    for item in manifest_items(manifest):
        asset = asset_id_of(item)
        if asset:
            out[asset] = str(item.get("edit_class", ""))
    return out


def asset_paths(manifest: dict | None) -> dict[str, str]:
    """`{asset_id: asset_path}` — thread.json#images[].asset_path 의 원천."""
    out: dict[str, str] = {}
    for item in manifest_items(manifest):
        asset = asset_id_of(item)
        if asset and item.get("asset_path"):
            out[asset] = str(item["asset_path"])
    return out


def asset_id_for_figure(figure_id: str) -> str:
    """`FIG-n` → `fig-NN`(n 을 2자리 0채움 · 100 이상이면 자릿수 그대로). 숫자가 아닌 접미(`FIG-3A`)는 소문자로 잇는다."""
    tail = figure_id[len(FIGURE_PREFIX):] if figure_id.startswith(FIGURE_PREFIX) else figure_id
    if tail.isdigit():
        return f"{ASSET_PREFIX}{int(tail):02d}"
    return ASSET_PREFIX + tail.lower()


__all__ = ["ASSET_EXT", "ASSET_PREFIX", "FIGURE_PREFIX", "asset_classes", "asset_id_for_figure", "asset_id_of",
           "asset_paths", "figure_id_of", "manifest_items"]
