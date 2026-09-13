# -*- coding: utf-8 -*-
"""`compose.prompt-lint` — 펜 프롬프트의 긍정형 규율을 입력에서 집행한다(SPEC §1.9 · 헌장 D8).

두 법(같은 검사 id · 다른 ruleset).

| ruleset | 무엇을 보는가 | 정본 |
|---|---|---|
| `prompt-negation` | 부정 명령형 패턴 `PROMPT_NEGATION_RE` 출현 0 | SPEC §1.9 코드블록(표 셀 밖) |
| `speech-acts+defect-catalog` | 화행 술어의 정의문·분류 질문·예문, 결함 카탈로그 `entries[].pattern` 의 **리터럴 부분 문자열** 출현 0(공백 정규화 후) | `contracts/lexicon/speech-acts.yaml` · `defect-catalog.yaml` |

대상은 산출물이 아니라 **프롬프트 자체**다 — 이 규율은 결과물에서 사후 확인할 수 없고 입력에서만
집행 가능하다. 대상 범위 = 렌더된 요청서에서 「원천 조각」 절(재료·블루프린트 전문 = 데이터)과
지시 블록 안의 블루프린트 요약 표(설계 레인이 쓴 EN 값 = 데이터)를 뺀 나머지. 특허 원문에는 `avoid`
같은 낱말이 흔하고, 설계 레인의 `point_en` 도 펜 프롬프트 템플릿이 아니다(총괄 재량 · T64 집행 ②).

★ 정규식은 **SPEC 코드블록을 글자 그대로** 옮긴다. 표 셀에서 옮기면 `\\|` 이스케이프가 섞여 존재하지
않는 형태를 검사하게 된다(감수 2026-08-17 · sol BLOCKER #6).
"""

from __future__ import annotations

import os
import re

import yaml

from reader.lib.report import CheckRow, Finding

CHECK_ID = "compose.prompt-lint"
RULESET_NEGATION = "prompt-negation"
RULESET_LEXICON = "speech-acts+defect-catalog"
RULESET_NEGATION_VERSION = "SPEC-1.9"

PROMPT_NEGATION_RE = re.compile(r"\b(do not|don't|never|avoid|금지|하지 마)\b", re.IGNORECASE)

SPEECH_ACTS = ("contracts", "lexicon", "speech-acts.yaml")
DEFECT_CATALOG = ("contracts", "lexicon", "defect-catalog.yaml")
PREDICATE_STRING_FIELDS = ("definition_kr", "classification_question")
PREDICATE_LIST_FIELDS = ("positive_examples", "negative_examples")

#: 렌더된 요청서(`render_request_body`)에서 린트 대상으로 **남기는** 절 제목 접두.
LINT_SECTION_PREFIXES = ("## 응답 계약", "## 이 요청의 지시", "## 절차")
#: 린트 대상에서 **빼는** 절 제목 접두(데이터 절).
DATA_SECTION_PREFIXES = ("## 원천 조각", "## 블루프린트 요약")
#: 지시 블록 안의 데이터 절 제목(지시 블록은 `##` 절로 구성된다).
DATA_SUBSECTION_PREFIX = "## 블루프린트 요약"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _load_yaml(repo: str, parts: tuple[str, ...]) -> dict:
    path = os.path.join(repo, *parts)
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} 최상위가 매핑이 아니다")
    return data


def lexicon_literals(repo: str) -> tuple[list[tuple[str, str]], str, int, str]:
    """`[(출처 라벨, 문자열)]` · 화행 버전 · 카탈로그 항목 수 · 카탈로그 버전."""
    acts = _load_yaml(repo, SPEECH_ACTS)
    catalog = _load_yaml(repo, DEFECT_CATALOG)
    literals: list[tuple[str, str]] = []
    for predicate in acts.get("predicates") or []:
        if not isinstance(predicate, dict):
            continue
        pid = str(predicate.get("id", "?"))
        for key in PREDICATE_STRING_FIELDS:
            value = predicate.get(key)
            if isinstance(value, str) and value.strip():
                literals.append((f"speech-acts:{pid}.{key}", value))
        for key in PREDICATE_LIST_FIELDS:
            for index, value in enumerate(predicate.get(key) or []):
                if isinstance(value, str) and value.strip():
                    literals.append((f"speech-acts:{pid}.{key}[{index}]", value))
    entries = [entry for entry in (catalog.get("entries") or []) if isinstance(entry, dict)]
    for entry in entries:
        pattern = entry.get("pattern")
        if isinstance(pattern, str) and pattern.strip():
            literals.append((f"defect-catalog:{entry.get('id', '?')}.pattern", pattern))
    return literals, str(acts.get("version", "")), len(entries), str(catalog.get("version", ""))


def lint_target(rendered: str) -> str:
    """렌더된 요청서 → 린트 대상 텍스트(데이터 절 제거).

    `##` 절 단위로 자른다. 요청서 머리(표·응답 규약 보일러플레이트 = 레인 공통 서식이며 펜 프롬프트가
    아니다)와 데이터 절은 빼고 `LINT_SECTION_PREFIXES` 의 절만 남긴다. 절 안의 하위 `##`(지시 블록의
    블루프린트 요약)도 데이터로 뺀다. 렌더 형식이 아닌 텍스트(템플릿 단독)는 그대로 전부가 대상이다.
    """
    lines = rendered.split("\n")
    if not any(line.startswith(LINT_SECTION_PREFIXES) for line in lines):
        return rendered
    kept: list[str] = []
    section: str | None = None       # "lint" | "data" | "sub-data" | None(머리)
    for line in lines:
        if line.startswith("## "):
            if line.startswith(DATA_SECTION_PREFIXES[0]):
                section = "data"
            elif line.startswith(LINT_SECTION_PREFIXES):
                section = "lint"
            elif section in ("lint", "sub-data"):
                # 지시 블록 안의 하위 절 — 블루프린트 요약만 데이터, 나머지(런 표지·시트 값·재시도)는 대상.
                section = "sub-data" if line.startswith(DATA_SUBSECTION_PREFIX) else "lint"
        if section == "lint":
            kept.append(line)
    return "\n".join(kept)


def lint_rows(text: str, repo: str) -> list[CheckRow]:
    """판정 행 2(같은 id · ruleset 둘). `text` 는 이미 대상 범위로 잘린 텍스트다."""
    lines = text.split("\n")
    negation = CheckRow(check_id=CHECK_ID, ruleset=RULESET_NEGATION, ruleset_version=RULESET_NEGATION_VERSION,
                        ruleset_size=1, checked=len(lines))
    for number, line in enumerate(lines, 1):
        for match in PROMPT_NEGATION_RE.finditer(line):
            negation.add("prompt.negation", f"line {number}", match.group(0), "긍정형 문장",
                         "펜 프롬프트는 긍정형만 담는다 — 부정 명령형 패턴이 있다(D8)")

    literals, acts_version, catalog_entries, catalog_version = lexicon_literals(repo)
    lexicon = CheckRow(check_id=CHECK_ID, ruleset=RULESET_LEXICON,
                       ruleset_version=f"{acts_version}+{catalog_version}", ruleset_size=len(literals),
                       checked=len(lines))
    lexicon.extras["defect_catalog"] = {
        "ruleset_size": catalog_entries,
        "vacuous": "empty-ruleset" if catalog_entries == 0 else "none",
    }
    normalized_text = _normalize(text)
    for label, literal in literals:
        needle = _normalize(literal)
        if needle and needle in normalized_text:
            lexicon.add("prompt.lexicon-literal", label, needle[:80], "부재",
                        "검증 심급의 문언(화행 술어·결함 카탈로그)이 펜 프롬프트에 실렸다(D8 · must_not_read)")
    return [negation, lexicon]


def lint_prompt(text: str, repo: str) -> list[Finding]:
    """발주 서명 — finding 목록(0 이면 통과). `text` 는 렌더된 요청서 또는 템플릿 단독."""
    return [finding for row in lint_rows(lint_target(text), repo) for finding in row.findings]


__all__ = [
    "CHECK_ID",
    "PROMPT_NEGATION_RE",
    "RULESET_LEXICON",
    "RULESET_NEGATION",
    "lexicon_literals",
    "lint_prompt",
    "lint_rows",
    "lint_target",
]
