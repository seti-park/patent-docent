# -*- coding: utf-8 -*-
"""점수 금지 린트 `gate.no-score`(SPEC §4.6 세 겹 중 셋째 · 재정 N4 · T69 ⑥ · D8·D15).

정본 = `contracts/lexicon/score-lint.yaml#patterns[]`. 이 모듈은 **패턴을 하나도 들지 않는다** — 파일에서 읽고, 등재 4요소
(`pattern` · `detection.method+regex` · `counter_examples[]` · `decision`+`decision_item`)가 빠진 항목은 **로드 거부**한다
(입법 없이 집행하지 않는다 · D7). 반례 `counter_examples[]` 는 로드 시점에 그 패턴이 잡지 않아야 한다 — 잡으면 그 패턴은
어휘 검사로 퇴화한 것이며 로드 거부다.

대상 범위 = 파일 `targets[]` allowlist 안의 것만 — 여기서는 `verdict.json#l2.memos[]` 의 **키와 본문**(rule slug + text 전문).
`l2.md` 는 같은 값의 렌더라 따로 훑지 않는다(두 번 훑으면 두 진원이 생긴다). 스레드 본문은 대상이 아니다(`not_targets`).
자기매칭 격리(§4.8 4항): 스캔 목록에 린트 정의 파일이나 `ledgers/regression/` 이 들어오면 판정이 아니라 실행 거부다.
"""

from __future__ import annotations

import os
import re

from reader.lib.report import CheckRow

from ...stages import StageError, load_yaml

SCORE_LINT_REL = ("contracts", "lexicon", "score-lint.yaml")
CHECK_ID = "gate.no-score"
RULESET = "score-lint"
REQUIRED_ENTRY_KEYS = ("id", "pattern", "detection", "counter_examples", "decision", "decision_item")
FORBIDDEN_SCAN_PREFIXES = ("contracts/lexicon/score-lint.yaml", "ledgers/regression/")
MEMO_TARGET = "50-gate/<variant>/verdict.json#l2.memos[]"


class ScoreLintLoadError(StageError):
    """린트 정의 파일이 등재 규격을 어긴다 — 집행하지 않고 넘어진다."""


def load_patterns(repo: str) -> dict:
    """`{version, schema, patterns: [{id, regex: compiled, decision, decision_item}], targets, not_targets}` — 로드 시 4요소·반례 검증."""
    path = os.path.join(repo, *SCORE_LINT_REL)
    data = load_yaml(path)
    entries = data.get("patterns")
    if not isinstance(entries, list) or not entries:
        raise ScoreLintLoadError(f"{path}#patterns 가 비어 있다 — 린트 정의가 없으면 집행할 법이 없다")
    targets = [str(t.get("path", "")) for t in (data.get("targets") or []) if isinstance(t, dict)]
    for target in targets:
        if any(target.startswith(prefix) for prefix in FORBIDDEN_SCAN_PREFIXES):
            raise ScoreLintLoadError(f"스캔 대상에 린트 정의·회귀 표본이 들어 있다 — 자기매칭 격리 위반(§4.8): {target}")
    if MEMO_TARGET not in targets:
        raise ScoreLintLoadError(f"{path}#targets 에 {MEMO_TARGET} 가 없다 — memo 는 allowlist 로만 훑는다")
    patterns: list[dict] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ScoreLintLoadError("patterns[] 원소가 매핑이 아니다")
        missing = [key for key in REQUIRED_ENTRY_KEYS if key not in entry]
        if missing:
            raise ScoreLintLoadError(f"패턴 {entry.get('id')!r} 에 등재 4요소가 빠졌다({', '.join(missing)}) — 로드 거부")
        detection = entry.get("detection") or {}
        if str(detection.get("method")) != "regex" or not isinstance(detection.get("regex"), str):
            raise ScoreLintLoadError(f"패턴 {entry['id']!r} 의 detection 이 regex 가 아니다")
        if not re.fullmatch(r"ruling-[0-9]{8}-[0-9]{2}-.+", str(entry.get("decision", ""))):
            raise ScoreLintLoadError(f"패턴 {entry['id']!r} 의 decision 이 재정 원장이 아니다: {entry.get('decision')!r}")
        counters = entry.get("counter_examples")
        if not isinstance(counters, list) or not counters:
            raise ScoreLintLoadError(f"패턴 {entry['id']!r} 에 반례가 없다 — 오탐을 증명할 방법이 없다")
        compiled = re.compile(detection["regex"])
        for counter in counters:
            text = str((counter or {}).get("text", "")) if isinstance(counter, dict) else str(counter)
            if compiled.search(text):
                raise ScoreLintLoadError(f"패턴 {entry['id']!r} 가 자기 반례 {text!r} 를 잡는다 — 어휘 검사로 퇴화했다(재정 N4)")
        patterns.append({"id": str(entry["id"]), "regex": compiled, "decision": str(entry["decision"]),
                         "decision_item": str(entry["decision_item"])})
    return {"version": str(data.get("version", "")), "schema": str(data.get("schema", "")), "patterns": patterns,
            "targets": targets, "not_targets": [str(t.get("path", "")) for t in (data.get("not_targets") or []) if isinstance(t, dict)]}


def hits(text: str, law: dict) -> list[tuple[str, str]]:
    """`[(pattern_id, matched_text)]` — 텍스트 하나에 대한 전 패턴 매칭."""
    out: list[tuple[str, str]] = []
    for pattern in law["patterns"]:
        for match in pattern["regex"].finditer(text or ""):
            out.append((pattern["id"], match.group(0)))
    return out


def lint_memos(memos: list[dict], law: dict) -> CheckRow:
    """판정 행 1 — `ruleset: score-lint` · version · size = 패턴 수 · checked = memo 수. 대상 = 각 memo 의 rule slug + text 전문."""
    row = CheckRow(check_id=CHECK_ID, ruleset=RULESET, ruleset_version=law["version"], ruleset_size=len(law["patterns"]),
                   checked=len(memos))
    row.extras["targets"] = [MEMO_TARGET]
    for memo in memos:
        memo_id = str(memo.get("id") or memo.get("rule") or "?")
        for field in ("rule", "text"):
            for pattern_id, matched in hits(str(memo.get(field, "")), law):
                row.add(pattern_id, f"{memo_id}#{field}", matched, "점수·등급 표기 없음",
                        "자문 메모가 점수·등급을 발행했다 — 굿하트 미끼(D15 · SPEC §4.6 · 재정 N4)")
    return row


__all__ = ["CHECK_ID", "MEMO_TARGET", "RULESET", "ScoreLintLoadError", "hits", "lint_memos", "load_patterns"]
