# -*- coding: utf-8 -*-
"""국소화 · 집계(SPEC §5.4 · 재정 R9 · T69 ⑥ · D9) — 전부 결정론.

① 표적 재료의 도달률 `hit_rate` = 유효 답변의 환산값 평균(`probe.yaml#grading.scores` · 무효 답변은 분모 제외 · 유효 0 이면 null).
② `annotation-index.json#by_material[M]` 을 역조회해 그 표적을 인용한 문장의 트윗 집합을 후보로 삼는다.
③ `weakest_tweet` = 2단 규칙 — 1차 그 표적을 인용한 **문장 수가 가장 적은** 트윗 · 2차(동점) **트윗 번호가 큰** 쪽. 사람도 모델도 고르지 않는다.
④ 인용 문장이 없으면 `weakest_tweet: null` + `unrepresented: true`(블루프린트가 표적으로 선언했으나 본문에 배치되지 않은 경우).
⑤ `delivery_fidelity` = 표적 간 **비가중 평균**(v0). `loci[]` = 임계 필터 없이 걸림 지점 전량(`{locus, issue, count, n}`).
"""

from __future__ import annotations

from collections import Counter

from .run_probes import KIND_NOT_STATED, KIND_STATED

ISSUE_MISS = "miss"
ISSUE_PARTIAL = "partial"
ISSUE_NOT_STATED = "not-stated"
ISSUE_INVALIDATED = "invalidated"
ISSUE_UNREPRESENTED = "unrepresented"


def weakest_tweet(index: dict, material_id: str) -> tuple[int | None, bool]:
    """→ (트윗 번호 | None, unrepresented). 2단 결정론 규칙(§5.4)."""
    entries = [e for e in ((index.get("by_material") or {}).get(material_id) or []) if isinstance(e, dict) and e.get("tweet") is not None]
    if not entries:
        return None, True
    counts = Counter(int(e["tweet"]) for e in entries)
    fewest = min(counts.values())
    return max(tweet for tweet, count in counts.items() if count == fewest), False


def target_row(*, material_id: str, kind: str, method: str, verdicts: list[dict], index: dict, scores: dict) -> dict:
    """`verdicts` = 그 표적에 대한 프로브별 `{probe_id, answer_kind, grade|None, invalid: bool}`."""
    counts = {"hit": 0, "partial": 0, "miss": 0, "not_stated": 0, "invalidated": 0}
    total = 0.0
    valid = 0
    for row in verdicts:
        if row.get("invalid"):
            counts["invalidated"] += 1
            continue
        valid += 1
        if row.get("answer_kind") == KIND_NOT_STATED:
            counts["not_stated"] += 1
            counts["miss"] += 1
            total += float(scores["miss"])
            continue
        grade = str(row.get("grade"))
        counts[grade] += 1
        total += float(scores[grade])
    tweet, unrepresented = weakest_tweet(index, material_id)
    return {"material_id": material_id, "kind": kind, "method": method, "hit_rate": (round(total / valid, 4) if valid else None),
            "weakest_tweet": tweet, "unrepresented": unrepresented, "answers": counts}


def loci_rows(per_target: list[dict], n: int) -> list[dict]:
    """걸림 지점 전량 — 표적마다 miss(not-stated 제외) · partial · not-stated · invalidated · unrepresented 를 횟수와 함께."""
    out: list[dict] = []
    for target in per_target:
        answers = target["answers"]
        locus = {"tweet": target["weakest_tweet"], "material_id": target["material_id"]}
        for issue, count in ((ISSUE_MISS, answers["miss"] - answers["not_stated"]), (ISSUE_PARTIAL, answers["partial"]),
                             (ISSUE_NOT_STATED, answers["not_stated"]), (ISSUE_INVALIDATED, answers["invalidated"])):
            if count > 0:
                out.append({"locus": locus, "issue": issue, "count": int(count), "n": n})
        if target["unrepresented"]:
            out.append({"locus": locus, "issue": ISSUE_UNREPRESENTED, "count": 1, "n": n})
    return out


def delivery_fidelity(per_target: list[dict]) -> float | None:
    rates = [t["hit_rate"] for t in per_target if t["hit_rate"] is not None]
    return round(sum(rates) / len(rates), 4) if rates else None


def build_score(*, run_id: str, variant: str, n: int, input_digest: str, question_set_digest: str, per_target: list[dict],
                restatement: dict, invalidated: list[dict], notes: str, grading_input_digest: str | None = None) -> dict:
    return {
        "schema": "probe-score/v0",
        "run_id": run_id,
        "variant": variant,
        "probe_n": n,
        "input_digest": input_digest,
        "question_set_digest": question_set_digest,
        **({"grading_input_digest": grading_input_digest} if grading_input_digest else {}),
        "delivery_fidelity": delivery_fidelity(per_target),
        "per_target": per_target,
        "restatement": restatement,
        "invalidated_answers": invalidated,
        "loci": loci_rows(per_target, n),
        "notes": notes,
    }


__all__ = ["ISSUE_INVALIDATED", "ISSUE_MISS", "ISSUE_NOT_STATED", "ISSUE_PARTIAL", "ISSUE_UNREPRESENTED", "KIND_STATED", "build_score",
           "delivery_fidelity", "loci_rows", "target_row", "weakest_tweet"]
