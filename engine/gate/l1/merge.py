# -*- coding: utf-8 -*-
"""k 표 병합 — SPEC §4.5 글자 그대로(재정 2026-09-13 T67 ② · M6-a).

| 항목 | 값 |
|---|---|
| 동일성 | 같은 `rule` + 같은 `locus`(tweet, sentence). 문언 표현의 차이는 무시 |
| 채택 | 과반(≥ k//2 + 1) 일치 항목만 `defect`. `expected`·`observed`·`fix_directive` 는 **첫 회차의 문언** |
| 강등 | 과반 미달 → `flag`(`origin: minority-vote` · `votes: {k, for, against}` · `note` = 회차 문언) |
| 자문 규칙 | `l1.advice-implicit`(veto false) 는 표수 무관 `flag`(`origin: advisory-rule` · votes) |
| 화행 | 표수 무관 `flag`(`origin: speech-act` · `predicate` · `votes`) — 다수결이어도 defect 승격 없음(재정 R7) |
| 불일치 로그 | 만장일치 아닌 항목 전부 `disagreement_log[] {rule, locus, for, against}` — 삭제·요약 금지(재정 R9) |
| 기록 | `votes[]` 에 회차별 원 판정 보존 |

★ 결정론 — 같은 payload 목록이면 같은 출력이다. 항목 순서 = (tweet, sentence, rule) 정렬. id 는 `verdict.json` 안에서
유일하며 L0 발행분 다음 번호를 잇는다(호출자가 `next_defect_no`·`next_flag_no` 를 준다).
"""

from __future__ import annotations

LAYER = "l1"
ORIGIN_MINORITY = "minority-vote"
ORIGIN_ADVISORY = "advisory-rule"
ORIGIN_SPEECH_ACT = "speech-act"


def majority_threshold(k: int) -> int:
    return k // 2 + 1


def _key(rule: str, locus: dict) -> tuple[str, int, int]:
    return (str(rule), int(locus["tweet"]), int(locus["sentence"]))


def _locus(key: tuple[str, int, int]) -> dict:
    return {"tweet": key[1], "sentence": key[2]}


def _sort_key(key: tuple[str, int, int]) -> tuple[int, int, str]:
    return (key[1], key[2], key[0])


def _tally(payloads: list[dict], field: str, rule_of) -> dict[tuple[str, int, int], list[dict]]:
    """key → 그 항목을 낸 회차의 레코드 목록(회차 순). 한 회차가 같은 항목을 둘 내면 하나로 센다."""
    out: dict[tuple[str, int, int], list[dict]] = {}
    for payload in payloads:
        seen: set[tuple[str, int, int]] = set()
        for record in payload.get(field) or []:
            key = _key(rule_of(record), record["locus"])
            if key in seen:
                continue
            seen.add(key)
            out.setdefault(key, []).append(record)
    return out


def merge(payloads: list[dict], *, k: int, advisory_rules: list[str] | tuple[str, ...], flag_rule: str,
          next_defect_no: int = 1, next_flag_no: int = 1) -> dict:
    """k 개 payload(회차 순) → `{pass, k, votes, defects, flags, disagreement_log}`.

    `advisory_rules` = 거부권 없는 L1 규칙 id(계약 `gate.yaml#layers.l1.rules[].veto == false`) ·
    `flag_rule` = 화행 flag 의 rule 형(`speech-act.<predicate>` · 계약 `layers.speech_act_flag.flag_rule`).
    """
    if len(payloads) != k:
        raise ValueError(f"payload 수 {len(payloads)} ≠ k {k}")
    threshold = majority_threshold(k)
    advisory = {str(rule) for rule in advisory_rules}
    votes = [{"i": index, "defects": list(p.get("defects") or []), "flags": list(p.get("flags") or []),
              "speech_acts": list(p.get("speech_acts") or [])} for index, p in enumerate(payloads)]

    defects_out: list[dict] = []
    flags_out: list[dict] = []
    disagreement: list[dict] = []
    defect_no, flag_no = next_defect_no, next_flag_no

    def log_if_split(rule: str, key: tuple[str, int, int], support: int) -> None:
        if 0 < support < k:
            disagreement.append({"rule": rule, "locus": _locus(key), "for": support, "against": k - support})

    # ① 거부권 규칙(defects[]) — 과반 → defect · 미달 → minority flag
    tally = _tally(payloads, "defects", lambda r: r["rule"])
    for key in sorted(tally, key=_sort_key):
        records = tally[key]
        support = len(records)
        first = records[0]
        log_if_split(key[0], key, support)
        if key[0] in advisory:
            # 계약이 veto false 로 둔 규칙이 defects[] 로 왔어도 거부권은 항목이 정한다 — flag 로 내린다.
            flags_out.append({"id": f"f-{LAYER}-{flag_no:03d}", "layer": LAYER, "rule": key[0], "locus": _locus(key),
                              "note": str(first.get("fix_directive") or first.get("expected") or ""), "origin": ORIGIN_ADVISORY,
                              "votes": {"k": k, "for": support, "against": k - support}})
            flag_no += 1
        elif support >= threshold:
            defects_out.append({"id": f"d-{LAYER}-{defect_no:03d}", "layer": LAYER, "rule": key[0], "locus": _locus(key),
                                "expected": str(first["expected"]), "observed": str(first.get("observed", "")),
                                "fix_directive": str(first["fix_directive"])})
            defect_no += 1
        else:
            note = str(first.get("fix_directive") or first.get("expected") or "")
            flags_out.append({"id": f"f-{LAYER}-{flag_no:03d}", "layer": LAYER, "rule": key[0], "locus": _locus(key),
                              "note": note, "origin": ORIGIN_MINORITY, "votes": {"k": k, "for": support, "against": k - support}})
            flag_no += 1

    # ② 자문 규칙(flags[]) — 표수 무관 flag(origin advisory-rule)
    tally = _tally(payloads, "flags", lambda r: r["rule"])
    for key in sorted(tally, key=_sort_key):
        records = tally[key]
        support = len(records)
        log_if_split(key[0], key, support)
        flags_out.append({"id": f"f-{LAYER}-{flag_no:03d}", "layer": LAYER, "rule": key[0], "locus": _locus(key),
                          "note": str(records[0]["note"]), "origin": ORIGIN_ADVISORY,
                          "votes": {"k": k, "for": support, "against": k - support}})
        flag_no += 1

    # ③ 화행(speech_acts[]) — 표수 무관 flag(origin speech-act · predicate) · 승격 없음
    tally = _tally(payloads, "speech_acts", lambda r: flag_rule.replace("<predicate>", str(r["predicate"])))
    for key in sorted(tally, key=_sort_key):
        records = tally[key]
        support = len(records)
        log_if_split(key[0], key, support)
        flags_out.append({"id": f"f-{LAYER}-{flag_no:03d}", "layer": LAYER, "rule": key[0], "locus": _locus(key),
                          "note": str(records[0]["note"]), "origin": ORIGIN_SPEECH_ACT, "predicate": str(records[0]["predicate"]),
                          "votes": {"k": k, "for": support, "against": k - support}})
        flag_no += 1

    return {"pass": len(defects_out) == 0, "k": k, "votes": votes, "defects": defects_out, "flags": flags_out,
            "disagreement_log": disagreement}


__all__ = ["ORIGIN_ADVISORY", "ORIGIN_MINORITY", "ORIGIN_SPEECH_ACT", "majority_threshold", "merge"]
