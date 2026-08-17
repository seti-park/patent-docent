# -*- coding: utf-8 -*-
"""`freeze.id-monotonic` + `freeze.payload-immutable` — 동결 항목의 시간 안정성.

`freeze.id-monotonic` 은 **ID 의 존재**만 본다. 따라서 개정본에서 기존 `active` 항목의
내용이 조용히 바뀌어도 통과한다. 항목 ID 의 시간 안정성(SPEC §2.4)은 ID 가 아니라
**의미**가 고정되어야 성립하는데, 지금까지 고정되던 것은 ID 뿐이었다(재감수 M-08).
`freeze.payload-immutable` 이 그 자리를 메운다.

정본 payload = `status`·`superseded_by` 를 제외한 전 필드(규칙 파일 `payload_canonicalization`).
이 둘은 생애 상태이며 전이표가 그 변경을 허용한다 — payload 에 넣으면 정상적인 철회·교체가
전부 불변성 위반으로 잡혀 검사가 사용 불가가 된다.

승계 사슬은 링크를 고치지 않고 **추적**으로 해소한다(구 규칙 폐기, `supersession_chain`) —
A→B→C 에서 A 는 B 를 계속 가리키고, 종단 C 가 `active` 여야 한다. 동결본을 고치는 경로가
이 규칙에는 없다.
"""

from __future__ import annotations

import hashlib
import json

from .report import CheckContext, CheckRow
from .rules import Rules

ID_MONOTONIC_ID = "freeze.id-monotonic"
PAYLOAD_IMMUTABLE_ID = "freeze.payload-immutable"


def canonical_payload(item: dict, rules: Rules) -> str:
    """정본 payload 직렬화. 규칙 파일의 serialization 설정을 그대로 쓴다."""
    excluded = set(rules.payload_excluded_fields())
    body = {key: value for key, value in item.items() if key not in excluded}
    serialization = rules.payload_serialization()
    separators = tuple(serialization.get("separators") or (",", ":"))
    return json.dumps(
        body,
        sort_keys=bool(serialization.get("sort_keys", True)),
        separators=separators,
        ensure_ascii=bool(serialization.get("ensure_ascii", False)),
    )


def payload_digest(item: dict, rules: Rules) -> str:
    """`sha256(직렬화 바이트)`."""
    return hashlib.sha256(canonical_payload(item, rules).encode("utf-8")).hexdigest()


def _items_by_id(spec: dict | None) -> dict[str, dict]:
    if not spec:
        return {}
    out: dict[str, dict] = {}
    for item in spec.get("items") or []:
        item_id = item.get("id")
        if isinstance(item_id, str):
            out[item_id] = item
    return out


def check_id_monotonic(ctx: CheckContext) -> CheckRow:
    """항목 ID 규율 2종 — 연속성(`M1..Mn` 빠짐 없음)과 무손실(`v<N-1>` ⊆ `v<N>`).

    연속성이 없으면 append-only 규율이 "번호가 건너뛰어도 통과"로 남는다 —
    지워진 항목이 **처음부터 없었던 것처럼** 보이고, 그 순간 삭제와 미생성이 구별되지 않는다
    (SPEC §2.8 제약 6).
    """
    row = CheckRow(check_id=ID_MONOTONIC_ID)
    prior = _items_by_id(ctx.prior_spec)
    current = _items_by_id(ctx.spec)
    row.checked = len(current)

    # ① 연속성 — 첫 동결에도 적용된다(비교 대상 없이 인스턴스 자체로 판정 가능하다).
    numbers = sorted(_item_number(item_id) for item_id in current if _item_number(item_id))
    if numbers:
        missing = [f"M{n}" for n in range(1, numbers[-1] + 1) if n not in set(numbers)]
        if missing:
            row.add(
                "lifecycle.id-contiguous",
                "items[].id",
                f"M1..M{numbers[-1]} 중 결번 {', '.join(missing)}",
                f"M1..M{numbers[-1]} 빠짐 없음",
                "항목 번호에 결번이 있다 — 추가 전용 규율에서 결번은 삭제의 흔적이다",
            )

    # ② 무손실 — 직전 동결본이 있을 때만.
    if ctx.prior_spec is None:
        row.extras["skipped_prior_comparison"] = True
        return row
    row.checked += len(prior)
    for item_id in sorted(prior):
        if item_id not in current:
            row.add(
                "lifecycle.no-id-loss",
                item_id,
                "(개정본에 없음)",
                "개정본에 존재",
                "직전 동결본의 항목 ID 가 사라졌다 — 항목 ID 는 추가 전용이다(SPEC §1.6)",
            )
    return row


def _item_number(item_id: str) -> int | None:
    if isinstance(item_id, str) and item_id.startswith("M") and item_id[1:].isdigit():
        return int(item_id[1:])
    return None


def check_payload_immutable(ctx: CheckContext) -> CheckRow:
    """정본 payload 불변 + 단방향 전이 + 승계 사슬(비순환·종단 active)."""
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=PAYLOAD_IMMUTABLE_ID,
        ruleset="reader-rules#item_lifecycle",
        ruleset_version=rules.version,
        ruleset_size=len(rules.item_lifecycle.get("rules") or ()),
    )
    current = _items_by_id(ctx.spec)
    prior = _items_by_id(ctx.prior_spec)
    row.checked = len(current)

    # ① superseded_by ⟺ status == "superseded"
    for item_id, item in sorted(current.items()):
        has_link = item.get("superseded_by") is not None
        is_superseded = item.get("status") == "superseded"
        if has_link != is_superseded:
            row.add(
                "lifecycle.superseded-by-iff",
                f"{item_id}.superseded_by",
                f"superseded_by={item.get('superseded_by')} / status={item.get('status')}",
                'superseded_by non-null ⟺ status == "superseded"',
                "승계 링크와 생애 상태가 어긋난다(스키마 $comment (7) 의 검증기 몫)",
            )

    # ② 승계 사슬 — 같은 kind · 비순환 · 종단 active
    for item_id, item in sorted(current.items()):
        if item.get("superseded_by") is None:
            continue
        seen = [item_id]
        cursor = item
        while True:
            next_id = cursor.get("superseded_by")
            if next_id is None:
                break
            if next_id in seen:
                row.add(
                    "supersession.acyclic",
                    item_id,
                    " → ".join(seen + [next_id]),
                    "비순환 승계 사슬",
                    "승계 사슬이 순환한다 — 종단이 없으므로 인용의 수정 지시가 갈 곳이 없다",
                )
                cursor = None
                break
            following = current.get(next_id)
            if following is None:
                cursor = None  # 해소 실패는 read.pointer-resolve 가 보고한다
                break
            if following.get("kind") != cursor.get("kind"):
                row.add(
                    "supersession.same-kind",
                    f"{seen[-1]}.superseded_by",
                    f"{next_id} (kind={following.get('kind')})",
                    f"kind={cursor.get('kind')}",
                    "승계 대상의 kind 가 다르다 — 같은 대상에 대한 더 나은 항목이 아니다",
                )
            seen.append(next_id)
            cursor = following
        if cursor is not None and cursor.get("status") != "active":
            row.add(
                "supersession.terminal-active",
                item_id,
                f"{seen[-1]} (status={cursor.get('status')})",
                "종단 항목의 status = active",
                "승계 사슬의 종단이 살아 있지 않다 — 인용의 수정 지시가 지목할 대상이 없다",
            )

    if not prior:
        return row

    # ③ 정본 payload 불변 + ④ 단방향 전이
    transitions = rules.lifecycle_transitions()
    for item_id in sorted(set(prior) & set(current)):
        old = prior[item_id]
        new = current[item_id]
        if payload_digest(old, rules) != payload_digest(new, rules):
            row.add(
                "lifecycle.payload-frozen",
                item_id,
                canonical_payload(new, rules),
                canonical_payload(old, rules),
                "동결 항목의 정본 payload 가 바뀌었다 — 내용을 고치려면 새 ID 를 추가하고 "
                "옛 항목을 superseded 로 표시해야 한다",
            )
        old_status = old.get("status")
        new_status = new.get("status")
        if old_status != new_status:
            allowed = transitions.get(old_status) or []
            if new_status not in allowed:
                row.add(
                    "lifecycle.one-way",
                    f"{item_id}.status",
                    f"{old_status} → {new_status}",
                    f"{old_status} → {' | '.join(allowed) if allowed else '(전이 없음)'}",
                    "상태 전이가 전이표에 없다 — 종단 상태에서 되돌아오는 경로는 없다",
                )
    return row


def check(ctx: CheckContext) -> list[CheckRow]:
    """동결 검사 2행을 함께 낸다."""
    return [check_id_monotonic(ctx), check_payload_immutable(ctx)]
