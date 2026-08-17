# -*- coding: utf-8 -*-
"""CP1 주 표면 — `material-spec.json` → `material-spec.md`(KR 골격 · EN 값).

이 문서가 M1 의 **사용자 대면 산출물**이다. 헌장은 "체크포인트 1 의 재료 검토가 Owner
이해층을 겸한다 — 별도 브리핑은 두지 않는다"고 재정했으므로(D6), 이 파일 하나가 하류
기계의 정답지이자 Owner 의 이해 문서다. 따라서 품질 기준은 문체가 아니라 **완결성**이다:
빠진 항목은 곧 Owner 가 볼 수 없는 항목이다.

언어 정책(재정 R2) — 문서 골격·절 제목·검토 안내·drop 사유는 KR, **재료 항목의 값은 EN
원문 그대로**. 값을 번역하는 순간 하류 대조가 원문과 어긋난다.

강조 노출 3종(재정 R1·R3·N9) — 수치 3분류 · `manual_verification_required[]` ·
`grounding_exceptions[]`. 전부 "기계가 무엇을 보증했고 무엇을 보증하지 못했는가"의 목록이며,
감춰진 예외는 예외가 아니라 은폐다.
"""

from __future__ import annotations

import json
import os

from ..paths import load_stage_contract, repo_root

APPROVAL_SCHEMA = ("contracts", "schemas", "approval-envelope.schema.json")

KIND_LABELS = {
    "component": "구성요소",
    "grounding": "3중 접지",
    "fact": "수치 사실",
    "implication": "기술적 함의",
    "positioning": "포지셔닝",
    "figure_note": "도면 주석",
}


def _load_envelope_fields(repo: str | None) -> tuple[list[str], list[str]]:
    """승인 봉투의 필수 필드 목록을 스키마에서 읽는다(사본을 만들지 않는다)."""
    target = os.path.join(repo or repo_root(), *APPROVAL_SCHEMA)
    with open(target, encoding="utf-8") as handle:
        schema = json.load(handle)
    common = list(schema.get("required") or [])
    cp1: list[str] = []
    for branch in schema.get("allOf") or []:
        condition = ((branch.get("if") or {}).get("properties") or {})
        checkpoint = (condition.get("checkpoint") or {}).get("const")
        decision = (condition.get("decision") or {}).get("const")
        if checkpoint == "material_approval" and decision == "approved":
            cp1 = list((branch.get("then") or {}).get("required") or [])
    return common, cp1


def _items_of(spec: dict, kind: str) -> list[dict]:
    return [item for item in spec.get("items") or [] if item.get("kind") == kind]


def _item_by_id(spec: dict) -> dict:
    return {item.get("id"): item for item in spec.get("items") or []}


def _element_lines(elements: list, depth: int, out: list[str]) -> None:
    for element in elements or []:
        indent = "  " * depth
        out.append(
            f"{indent}- `{element.get('id')}` → **{element.get('material_id')}** — "
            f"{element.get('text_verbatim', '')}"
        )
        _element_lines(element.get("children") or [], depth + 1, out)


def _fact_line(item: dict) -> str:
    unit = item.get("unit")
    unit_text = f" {unit}" if unit else ""
    return (
        f"**{item.get('id')}** — {item.get('label_en', '')} · "
        f"`{item.get('value_raw', '')}` → `{item.get('value_normalized', '')}{unit_text}`"
    )


def render(
    spec: dict,
    convergence: dict | None = None,
    contract: dict | None = None,
    repo: str | None = None,
) -> str:
    """재료 명세 1건의 KR 판독본. 같은 입력에 같은 바이트를 낸다."""
    contract = contract if contract is not None else load_stage_contract("read", repo)
    checkpoint = contract.get("owner_checkpoint") or {}
    convergence = convergence or {}
    index = _item_by_id(spec)
    lines: list[str] = []

    def out(text: str = "") -> None:
        lines.append(text)

    # -- 0. 표제와 체크포인트 안내 -----------------------------------------
    out(f"# 재료 명세 검토본 — `{spec.get('run_id', '')}` (판 {spec.get('spec_version', '')})")
    out()
    out(
        f"상태 `{spec.get('status', '')}` · 스키마 `{spec.get('schema', '')}` · "
        f"reader `{spec.get('reader_version', '')}`"
    )
    out()
    out("이 문서는 `10-read/material-spec.json` 의 **결정론 렌더**다. 기계 정본은 JSON 이고,")
    out("판정의 표면은 이 문서다. 렌더가 항목을 빠뜨리면 `freeze.render-parity` 가 잡는다.")
    out()
    out("## 0. 체크포인트 1 — 무엇을 판정하는가")
    out()
    question = " ".join(str(checkpoint.get("question", "")).split())
    out(f"> {question}")
    out()
    out("### 승인 봉투 작성 안내")
    out()
    confirm = checkpoint.get("confirm_file", "")
    out(f"- 봉투 경로: `{confirm}` (프런트매터가 `approval-envelope/v0` 의 대상이다)")
    common, cp1 = _load_envelope_fields(repo)
    out(f"- 공통 필수 필드: {', '.join(f'`{name}`' for name in common)}")
    out(f"- CP1 승인 추가 필수: {', '.join(f'`{name}`' for name in cp1)}")
    out("- `target.digest` 는 승인 시점 대상 파일의 SHA-256 이다. 승인 후 재료가 바뀌면")
    out("  봉투는 **자동 실효**되고 `freeze` 가 `halt` 한다(재정 R8).")
    out("- `owner_quote` 는 Owner 가 **실제로 타이핑한 원문**이다. 시스템 요약의 인용은 무효다.")
    out("- 결정은 이진이다 — `approved` / `rejected`. **조건부 승인 제도는 없다.**")
    out("- `manual_verification_ack[]` 는 아래 §7 목록과, `derived_fact_ack[]` 는 §6.2 목록과")
    out("  **정확히 일치**해야 한다(`freeze.approval-valid`). 빈 목록·유령 ID 는 승인이 아니라 서명이다.")
    out("- **작업 레인은 봉투를 쓰지 않는다.** 봉투는 오케스트레이터가 Owner 응답 후 기록한다(SPEC §1.2 C3).")
    out("- 무응답은 무기한 대기다. 시간 초과 자동 진행 경로는 없다(재정 R8).")
    out()

    # -- 1. 특허 -----------------------------------------------------------
    patent = spec.get("patent") or {}
    dates = patent.get("dates") or {}
    out("## 1. 특허")
    out()
    out("| 항목 | 값 |")
    out("|---|---|")
    out(f"| 번호 | {patent.get('number', '')} |")
    out(f"| 제목 | {patent.get('title', '')} |")
    out(f"| 출원인 | {patent.get('assignee', '')} |")
    out(
        f"| 날짜 | 우선 {dates.get('priority', '')} · 출원 {dates.get('filing', '')} · "
        f"공개 {dates.get('publication', '')} |"
    )
    out(f"| 원천 | `{patent.get('source_path', '')}` |")
    out(f"| 원천 다이제스트 | `{patent.get('source_digest', '')}` |")
    out()

    # -- 2. 청구항 골격 -----------------------------------------------------
    claims = spec.get("claims") or {}
    out("## 2. 청구항 골격 (D5 ① 전 분해 · ② 관계 트리)")
    out()
    for claim in claims.get("independent") or []:
        out(f"### 독립항 `{claim.get('id')}`")
        out()
        out(f"> {claim.get('text_verbatim', '')}")
        out()
        body: list[str] = []
        _element_lines(claim.get("elements") or [], 0, body)
        lines.extend(body)
        out()
    for claim in claims.get("dependents") or []:
        depends = ", ".join(claim.get("depends_on") or [])
        out(
            f"### 종속항 `{claim.get('id')}` — `{claim.get('dependency_type')}` "
            f"(인용: {depends})"
        )
        out()
        out(f"> {claim.get('text_verbatim', '')}")
        out()
        for addition in claim.get("additions") or []:
            out(
                f"- `{addition.get('id')}` (부착: `{addition.get('attaches_to')}`) → "
                f"**{addition.get('material_id')}** — {addition.get('text_verbatim', '')}"
            )
        out()
    interests = claims.get("applicant_interest") or []
    if interests:
        out("### 출원인 관심 신호")
        out()
        for interest in interests:
            out(
                f"- `{interest.get('claim')}` → **{interest.get('material_id')}** — "
                f"{interest.get('signal', '')}"
            )
        out()

    # -- 3. 유기적 통합 그림 -------------------------------------------------
    out("## 3. 유기적 통합 그림 (D5 ④)")
    out()
    implications = _items_of(spec, "implication")
    if not implications:
        out("_등재된 함의 항목이 없다._")
        out()
    for item in implications:
        basis = item.get("basis", "")
        confidence = item.get("confidence", "")
        sources = ", ".join(item.get("derived_from") or [])
        out(f"- **{item.get('id')}** ({basis} · {confidence}) — {item.get('statement_en', '')}")
        out(f"  - 근거 항목: {sources}")
        for quote in item.get("evidence_quotes") or []:
            out(f"  - 인용: “{quote}”")
    out()

    # -- 4. 포지셔닝 --------------------------------------------------------
    out("## 4. 포지셔닝 (D5 ⑤)")
    out()
    positionings = _items_of(spec, "positioning")
    if not positionings:
        out("_등재된 포지셔닝 항목이 없다._")
        out()
    for item in positionings:
        out(f"- **{item.get('id')}**")
        out(f"  - 배경 문제: {item.get('background_problem', '')}")
        out(f"  - 주장 효과: {item.get('asserted_effect', '')}")
        out(f"  - 차이: {item.get('delta', '')}")
        for quote in item.get("quotes") or []:
            out(f"  - 인용: “{quote}”")
    out()

    # -- 5. 구성요소와 접지 -------------------------------------------------
    out("## 5. 구성요소와 3중 접지 (D5 ③)")
    out()
    out("| 구성요소 | 청구항 좌표 | 라벨(EN) | 접지 |")
    out("|---|---|---|---|")
    groundings = _items_of(spec, "grounding")
    by_component: dict[str, list[dict]] = {}
    for item in groundings:
        by_component.setdefault(str(item.get("component")), []).append(item)
    for item in _items_of(spec, "component"):
        anchors = by_component.get(str(item.get("id")), [])
        if anchors:
            anchor_text = " / ".join(
                f"**{anchor.get('id')}** "
                f"(명세서 {(anchor.get('anchor_state') or {}).get('spec')} · "
                f"도면 {(anchor.get('anchor_state') or {}).get('figure')})"
                for anchor in anchors
            )
        else:
            anchor_text = "**접지 없음**"
        out(
            f"| **{item.get('id')}** | `{item.get('claim_ref')}` | "
            f"{item.get('label_en', '')} | {anchor_text} |"
        )
    out()
    for item in groundings:
        out(f"- **{item.get('id')}** ← 구성요소 {item.get('component')}")
        for ref in item.get("spec_refs") or []:
            out(f"  - 명세서 `{ref.get('locator', '')}`: “{ref.get('quote', '')}”")
        for ref in item.get("figure_refs") or []:
            numerals = ", ".join(ref.get("numerals") or [])
            out(f"  - 도면 `{ref.get('figure')}` (도면부호 {numerals}): “{ref.get('caption_quote', '')}”")
        if item.get("search_note"):
            out(f"  - 탐색 기록: {item.get('search_note')}")
    out()

    # -- 6. 수치 3분류 ------------------------------------------------------
    classification = convergence.get("fact_classification") or {}
    quoted = classification.get("quoted_span") or {}
    derived = classification.get("derived") or []
    figure_sourced = classification.get("figure_sourced") or []
    bibliographic = classification.get("bibliographic_ids") or []

    out("## 6. 수치 사실 — 3분류 (재정 N9)")
    out()
    out("기계가 **무엇을 보증했는가**가 갈래마다 다르다. 갈래를 섞어 보면 승인은 형식이 된다.")
    out()
    out("### 6.1 원문 스팬 수치 (`quoted` · `bibliographic`)")
    out()
    out(f"- 원문 스팬 수치: **{quoted.get('count', 0)}건** — {', '.join(quoted.get('material_ids') or []) or '없음'}")
    out(f"- 서지 복사: {', '.join(bibliographic) or '없음'} (`patent` 블록에서 결정론 복사)")
    out()
    for item_id in quoted.get("material_ids") or []:
        item = index.get(item_id) or {}
        source = item.get("source") or {}
        out(f"- {_fact_line(item)}")
        out(f"  - 원천 `{source.get('locator', '')}`: “{source.get('quote', '')}”")
    out()
    out("### 6.2 파생 수치 (`derived`) — 산식과 원천 스팬을 나란히")
    out()
    if not derived:
        out("_파생 수치 없음. 승인 봉투의 `derived_fact_ack` 는 빈 배열로 적는다._")
        out()
    for entry in derived:
        item = index.get(entry.get("material_id")) or {}
        out(f"- {_fact_line(item)}")
        out(f"  - 산식: `{entry.get('formula', '')}` (깊이 {entry.get('depth')})")
        for source in entry.get("inputs") or []:
            reference = source.get("ref")
            if reference:
                referenced = index.get(reference) or {}
                origin_quote = (referenced.get("source") or {}).get("quote", "")
                out(
                    f"  - 입력 `{source.get('name')}` ← **{reference}** "
                    f"(`{referenced.get('value_raw', '')}`) — 원천 인용: “{origin_quote}”"
                )
            else:
                out(
                    f"  - 입력 `{source.get('name')}` ← 원문 스팬 "
                    f"`{source.get('locator', '')}`"
                )
        out("  - ★ 이 값은 **원문 어디에도 문자열로 없다.** 계산의 결과다.")
    out()
    out("### 6.3 도면 유래 수치 (`figure-sourced`) — 기계 검증 불가")
    out()
    if not figure_sourced:
        out("_도면 유래 수치 없음._")
        out()
    for entry in figure_sourced:
        item = index.get(entry.get("material_id")) or {}
        out(f"- {_fact_line(item)}")
        out(
            f"  - 도면 `{entry.get('figure')}` · `machine_verifiable: "
            f"{str(entry.get('machine_verifiable')).lower()}` — **기계 검증 불가**"
        )
    out()

    # -- 7. 사람 검증 필요 --------------------------------------------------
    manual = convergence.get("manual_verification_required") or []
    out("## 7. ★ 사람 검증 필요 목록 (재정 R1)")
    out()
    out("도면에서 읽은 값은 기계가 대조할 원문 스팬이 없다. **검사가 통과시켰다는 사실이 값이**")
    out("**옳다는 뜻이 아니다.** 아래 목록은 봉투의 `manual_verification_ack[]` 와 정확히 일치해야 한다.")
    out()
    if not manual:
        out("_해당 없음. 봉투에는 빈 배열로 적는다(생략은 누락과 '없음'을 구별하지 못한다)._")
        out()
    for entry in manual:
        numerals = ", ".join(entry.get("numerals") or [])
        item = index.get(entry.get("material_id")) or {}
        out(
            f"- **{entry.get('material_id')}** — {item.get('label_en', '')} · "
            f"값 `{item.get('value_raw', '')}` · 도면 `{entry.get('figure')}` "
            f"(도면부호 {numerals}) · 사유 `{entry.get('reason')}`"
        )
    out()

    # -- 8. 접지 예외 -------------------------------------------------------
    exceptions = convergence.get("grounding_exceptions") or []
    out("## 8. ★ 접지 예외 (재정 R3)")
    out()
    out("접지 전량이 원칙이므로 예외는 날조하거나 숨기지 않고 드러낸다. **예외가 많으면 그것이**")
    out("**소재 신호다.**")
    out()
    if not exceptions:
        out("_예외 없음 — 전 구성요소가 명세서·도면 양쪽에 접지되었다._")
        out()
    for entry in exceptions:
        out(
            f"- **{entry.get('material_id')}** (구성요소 {entry.get('component')}) — "
            f"명세서 `{entry.get('spec')}` · 도면 `{entry.get('figure')}`"
        )
        out(f"  - 탐색 기록: {entry.get('search_note', '')}")
    out()

    # -- 9. drop 신호 -------------------------------------------------------
    drop = spec.get("drop_signal") or {}
    out("## 9. drop 신호 (D4)")
    out()
    out(f"- 단계: `{drop.get('stage', '')}` · 판정: `{drop.get('verdict', '')}`")
    out(f"- 사유: {drop.get('reason', '')}")
    if drop.get("verdict") == "drop-proposed":
        out("- ★ `drop-proposed` 이므로 봉투에 `drop_decision`(`go` | `drop`)이 **필수**다.")
    out()

    # -- 10. 도면 ----------------------------------------------------------
    out("## 10. 도면")
    out()
    figures = spec.get("figures") or []
    if not figures:
        out("_등재된 도면이 없다._")
        out()
    for figure in figures:
        numerals = ", ".join(figure.get("numerals") or [])
        out(f"- `{figure.get('id')}` — “{figure.get('caption_quote', '')}”")
        out(f"  - 원본 `{figure.get('raw_path', '')}` · 도면부호 {numerals}")
    for item in _items_of(spec, "figure_note"):
        numerals = ", ".join(item.get("numerals") or [])
        out(
            f"- **{item.get('id')}** ({item.get('figure')}) — {item.get('what_it_shows_en', '')} "
            f"· 도면부호 {numerals}"
        )
    out()

    # -- 11. 항목 색인 ------------------------------------------------------
    out("## 11. 항목 색인 (전량)")
    out()
    out("| 항목 | 종류 | 상태 | 승계 |")
    out("|---|---|---|---|")
    for item in spec.get("items") or []:
        kind = item.get("kind", "")
        out(
            f"| **{item.get('id')}** | {KIND_LABELS.get(kind, kind)} | "
            f"{item.get('status', '')} | {item.get('superseded_by') or '-'} |"
        )
    out()

    # -- 12. 절차 이력 ------------------------------------------------------
    provenance = spec.get("provenance") or {}
    out("## 12. 절차 이력")
    out()
    out("| 항목 | 값 |")
    out("|---|---|")
    out(f"| 독립 실행 | {', '.join(provenance.get('read_runs') or [])} |")
    out(f"| 산출 시각 | {provenance.get('produced_at', '')} |")
    out(f"| 엔진 커밋 | `{provenance.get('engine_commit', '')}` |")
    out()
    out("정본 재료는 첫 실행(`read-a`)의 산출이며, 둘째 실행(`read-b`)은 **수렴 비교 전용**이다.")
    out("두 실행은 서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.")
    out()
    return "\n".join(lines)
