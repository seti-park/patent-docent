# -*- coding: utf-8 -*-
"""**CP1 판독본 (KR 틀 · EN 값)** — `material-spec.json` → `material-spec.md`.

이 문서가 M1 의 **사용자 대면 산출물**이다. 헌장은 "체크포인트 1 의 재료 검토가 Owner
이해층을 겸한다 — 별도 브리핑은 두지 않는다"고 재정했으므로(D6), 이 파일 하나가 하류
기계의 정답지이자 Owner 의 이해 문서다. 따라서 품질 기준은 문체가 아니라 **완결성**이다:
빠진 항목은 곧 Owner 가 볼 수 없는 항목이다.

★ 명명(재정 P-U5): 구 명명 "KR 인간 판독본"은 폐기되었다. 판독본은 **KR 틀 + EN 값**이며,
번역본이 아니다 — 장 제목·안내·라벨만 KR 이고 인용·해설·함의의 값은 EN 원문 그대로다.
**파생 번역(EN 값의 KR 요약·의역)을 만드는 코드 경로를 두지 않는다.** 요약이 값을 대체하면
`freeze.render-parity` 가 그 사실을 잡는다(그 검사는 ID 존재가 아니라 **값의 바이트 존재**를
본다 — 재정 P-U5). KR 지원이 필요하면 검토 중 대화로 한다.

강조 노출 7종 — 수치 3분류(재정 N9) · `manual_verification_required[]`(재정 R1) ·
`grounding_exceptions[]`(재정 R3) · **미분류 종속 구조**(재정 P-1) · **맹검 스크리닝 메모
2건 병기**(재정 P-A·P-U4) · **수치 인벤토리**(재정 P-B) · **수렴 프로파일**(재정 P-3).
전부 "기계가 무엇을 보증했고 무엇을 보증하지 못했는가"의 목록이며, 감춰진 예외는 예외가
아니라 은폐다.
"""

from __future__ import annotations

import json
import os
from typing import Any

from ..paths import load_stage_contract, repo_root

APPROVAL_SCHEMA = ("contracts", "schemas", "approval-envelope.schema.json")
_CONVERGENCE_EARLY_UNSET = object()

# ★ 수치 인벤토리 계수의 **범위 표지**(2026-08-18 통주 2 처분).
# 구 표면은 "전체 34건 — 참조 3건 표시"라고만 적었고, 그 런의 실제 역참조 대상은 4였다
# (하나가 `figure-sourced` 라 정답지 밖이었다). 두 수가 어긋난 것이 아니라 **어느 범위의
# 계수인지가 적혀 있지 않았던 것**이며, 범위를 밝히지 않은 수치는 이 리포가 M-04 로 벌한
# 바로 그 형태다.
#
# 정본은 `reader/reader-rules.yaml#numeric_harvest.answer_scope` 이고 이 문자열은 사본이
# 아니라 **대조로 묶인 표면 문언**이다 — 렌더러는 이식 단위(`reader/`)를 import 하지 않는
# 것이 이 모듈의 규율이라 값을 읽어 올 수 없고, 대신 tests 의 대조 시험이 두 문언의 동치를
# 집행한다(정규화 표가 `contracts/l0-format.yaml` 과 묶인 방식과 같다).
ANSWER_SCOPE_TEXT = "kind fact · origin ∈ {quoted, bibliographic} · status active"

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
    convergence_early: Any = _CONVERGENCE_EARLY_UNSET,
) -> str:
    """재료 명세 1건의 KR 판독본. 같은 입력에 같은 바이트를 낸다."""
    contract = contract if contract is not None else load_stage_contract("read", repo)
    # 기존 직접 호출은 final 판정서를 두 번째 인자로만 넘겼다. 그 호출은 같은 목록을 조기
    # 판정서의 호환 입력으로 삼고, 파일 부재를 아는 호출자는 None 을 명시해 구 판을 드러낸다.
    if convergence_early is _CONVERGENCE_EARLY_UNSET:
        convergence_early = convergence
    checkpoint = contract.get("owner_checkpoint") or {}
    convergence = convergence or {}
    index = _item_by_id(spec)
    lines: list[str] = []

    def out(text: str = "") -> None:
        lines.append(text)

    # -- 0. 표제와 체크포인트 안내 -----------------------------------------
    out(
        f"# CP1 판독본 (KR 틀 · EN 값) — `{spec.get('run_id', '')}` "
        f"(판 {spec.get('spec_version', '')})"
    )
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
    # ★ 서지 확장 6필드를 렌더한다(재정 P-2 ⓐ · 총괄 처분 2026-08-18).
    #   근거 둘. ⓐ 판독본의 품질 기준은 완결성이다(SPEC §1.5 — "Owner 가 원천 특허를 다시
    #   열지 않고 판정할 수 있는가"). ⓑ 재정 P-2 ⓐ 가 이 필드를 넣은 근거가 **C18 최우선일의
    #   정확성 요건**인데, 최우선일이 옳은지는 우선권 목록을 나란히 보아야 판정된다 — 기계가
    #   산식으로 한 번(`read.bibliography#bib.earliest-priority`), 사람이 표면에서 한 번 보는
    #   이중 구조이며 표면이 없으면 뒤의 한 번이 사라진다.
    #   목록형 필드(inventors·applicants·priority_claims)를 단수로 접지 않는다 — 접는 순간
    #   P-2 ⓐ 가 폐기한 "assignee 단수 하나로 뭉갠" 구조로 되돌아간다.
    #   값 언어 규율 그대로: 틀은 KR, 값은 EN 원문이며 번역·요약하지 않는다(재정 P-U5).
    patent = spec.get("patent") or {}
    dates = patent.get("dates") or {}
    priority_claims = patent.get("priority_claims") or []
    classifications = patent.get("classifications") or {}
    out("## 1. 특허")
    out()
    out("| 항목 | 값 |")
    out("|---|---|")
    out(f"| 번호 | {patent.get('number', '')} |")
    out(f"| 제목 | {patent.get('title', '')} |")
    out(
        f"| 관할 · 공보 종별 | `{patent.get('jurisdiction', '')}` · "
        f"`{patent.get('kind_code', '')}` |"
    )
    out(f"| 출원인 (런 ID 유래 단수) | {patent.get('assignee', '')} |")
    out(f"| 출원인 목록 | {' · '.join(patent.get('applicants') or []) or '_없음_'} |")
    out(f"| 발명자 목록 | {' · '.join(patent.get('inventors') or []) or '_없음_'} |")
    out(
        f"| 날짜 | 우선 {dates.get('priority', '')} · 출원 {dates.get('filing', '')} · "
        f"공개 {dates.get('publication', '')} |"
    )
    if not priority_claims:
        # 누락과 '없음'을 구별한다 — 행을 지우면 "우선권을 보지 않았다"와 구별되지 않는다.
        out("| 우선권 주장 | _없음_ |")
    for position, claim in enumerate(priority_claims, start=1):
        out(
            f"| 우선권 주장 {position} | {claim.get('number', '')} · "
            f"{claim.get('date', '')} · `{claim.get('jurisdiction', '')}` |"
        )
    out(f"| 분류 IPC | {' · '.join(classifications.get('ipc') or []) or '_없음_'} |")
    out(f"| 분류 CPC | {' · '.join(classifications.get('cpc') or []) or '_없음_'} |")
    out(f"| 원천 | `{patent.get('source_path', '')}` |")
    out(f"| 원천 다이제스트 | `{patent.get('source_digest', '')}` |")
    out()
    # 최우선일 대조 — 기계가 무엇을 보증했는가를 사람이 눈으로 재확인하는 자리.
    if priority_claims:
        earliest = min(str(claim.get("date", "")) for claim in priority_claims)
        agreement = "일치" if str(dates.get("priority", "")) == earliest else "**불일치**"
        out(
            f"**최우선일 대조** — `dates.priority` {dates.get('priority', '')} ↔ "
            f"우선권 목록 최소 {earliest} → {agreement}"
        )
        out()
        out("이 대조는 `read.bibliography#bib.earliest-priority` 가 산식으로 이미 판정했다.")
        out("여기 다시 놓는 이유는 CP1 이 **기계가 무엇을 보증했는가**를 사람이 재확인하는")
        out("자리이기 때문이다(C18 최우선일의 정확성 요건 — 재정 P-2 ⓐ).")
        out()
    else:
        out("**최우선일 대조** — 우선권 주장이 없어 대조할 목록이 없다(대조 불가이며 결함이 아니다).")
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
    # ★ 경로 정정(재정 P-2 ⓑ): drop 은 사실이 아니라 편집 판단이므로 공유 코어가 아니라
    #   docent 확장 블록에 산다. 최상위 `drop_signal` 을 보던 구 경로는 폐기한다.
    drop = ((spec.get("extensions") or {}).get("docent") or {}).get("drop_signal") or {}
    out("## 9. drop 신호 (D4 — 최종)")
    out()
    out(f"- 단계: `{drop.get('stage', '')}` · 판정: `{drop.get('verdict', '')}`")
    out(f"- 사유: {drop.get('reason', '')}")
    if drop.get("verdict") == "drop-proposed":
        out("- ★ `drop-proposed` 이므로 봉투에 `drop_decision`(`go` | `drop`)이 **필수**다.")
        out("- 확정 재정의 자리는 **여기 CP1 한 곳**이다(재정 P-A). 조기 판단은 아래 §11 의")
        out("  맹검 메모로만 남아 있고, 그 자체로는 어떤 구속력도 갖지 않았다.")
    out()

    # -- 10. 미분류 종속 구조 (재정 P-1) ------------------------------------
    unclassified = convergence.get("unclassified_dependents") or []
    out("## 10. ★ 미분류 종속 구조 (재정 P-1)")
    out()
    out("Markush·조건부·수단항·카테고리 전환은 typed operator 입법을 범위에서 **제외**했고,")
    out("대신 `unclassified` 표지 + 이 목록 + 판정 행 계수 셋으로 침묵을 막는다.")
    out("**이 목록의 항목은 결함이 아니다** — 구조 미분류라는 사실의 표지이며, 종속 형태")
    out("판정(`parse.set-equals`·`parse.type-agrees`)의 대상에서 빠졌다는 뜻이다. 전문은")
    out("이미 보존되어 있으므로(재정 R1) 여기서 사람 눈이 마지막 심급이 된다.")
    selection = convergence.get("canonical_selection") or {}
    canonical_run = selection.get("read_run")
    if isinstance(canonical_run, str) and canonical_run:
        out(
            f"이 목록은 정본 실행 `{canonical_run}` 의 신고다. 두 실행이 갈린 신고는 "
            "아래 10-b 블록에 있다."
        )
    out()
    if not unclassified:
        out("_미분류 종속항 없음 — 전 종속항이 5종 어형으로 파싱되었다._")
        out()
    for entry in unclassified:
        out(f"- **`{entry.get('claim', '')}`** (`{entry.get('dependency_type', '')}`)")
        reported_by = entry.get("reported_by") or []
        if reported_by:
            out(f"  - 신고 실행: {', '.join(reported_by)}")
        if entry.get("text_status") == "absent":
            out(
                "  - 전문 부재 신고: 레인이 `text_verbatim` 을 비웠거나 키를 내지 않았다 "
                "(재정 2026-09-01 T18)."
            )
            out("  - 문언의 부재 자체가 신호이므로 이 항목은 목록에 남는다.")
        else:
            # 행위시법 P-U1 — 기존 runs/** 산출에는 text_status 가 없다. 키 부재는 구 판의
            # verbatim 렌더를 그대로 유지하며, 소급해서 absent 로 재해석하지 않는다.
            out(f"  - 전문: “{entry.get('text_verbatim', '')}”")
    out()

    # -- 10-b. 조기 합집합의 갈린 신고 (재정 T31) --------------------------
    out("## 10-b. ★ 조기 합집합 — 두 실행이 갈린 미분류 신고 (재정 T31)")
    out()
    if convergence_early is None:
        # 행위시법 P-U1 — 조기 판정서가 없던 구 런은 파일 부재 자체를 정직하게 보인다.
        out("조기 판정서 없음 — 구 판 산출")
        out()
    else:
        early_unclassified = convergence_early.get("unclassified_dependents") or []
        split_reports = [
            entry
            for entry in early_unclassified
            if len(entry.get("reported_by") or []) == 1
        ]
        if not split_reports:
            out("갈린 신고 없음 — 두 실행의 미분류 신고가 전건 일치")
            out()
        else:
            out("| `reported_by` | `claim` | `dependency_type` | `text_status` | `text_verbatim` |")
            out("|---|---|---|---|---|")
            for entry in split_reports:
                reported_by = ", ".join(entry.get("reported_by") or [])
                out(
                    f"| `{reported_by}` | `{entry.get('claim', '')}` | "
                    f"`{entry.get('dependency_type', '')}` | `{entry.get('text_status', '')}` | "
                    f"{entry.get('text_verbatim', '')} |"
                )
            out()

    # -- 11. 맹검 스크리닝 메모 (재정 P-A · P-U4) ---------------------------
    memos = convergence.get("screening_memos") or []
    out("## 11. ★ 맹검 스크리닝 메모 — 두 실행 병기 (재정 P-A · P-U4)")
    out()
    out("분해 직후 `read-a`·`read-b` 가 **각자** 적은 1차 판단이다. 상신이 아니었고 런을")
    out("세우지 않았으며, 최종 서사 평가 레인에는 비공개였다(앵커링 방지). 둘 다 싣는 이유는")
    out("**두 독립 관찰의 일치/불일치 자체가 신호**이기 때문이다 — 한 건으로 합치면 그 신호가")
    out("소멸한다.")
    out()
    out("| 실행 | 방향 | 근거 요지 |")
    out("|---|---|---|")
    if not memos:
        out("| _없음_ | _없음_ | 분해 레인이 메모를 내지 않았다 |")
    for memo in memos:
        out(
            f"| `{memo.get('read_run', '')}` | `{memo.get('direction', '')}` | "
            f"{memo.get('note', '')} |"
        )
    out()
    directions = {memo.get("direction") for memo in memos}
    if len(directions) > 1:
        out("★ 두 관찰의 **방향이 갈렸다.** 갈림은 결함이 아니라 신호이며, drop 의 확정 재정은")
        out("이 표와 위 §9 를 함께 놓고 이 자리에서 1회 내려진다.")
    elif memos:
        out(f"두 관찰의 방향이 `{sorted(directions)[0]}` 로 일치했다.")
    out()

    # -- 12. 수치 인벤토리 (재정 P-B) ---------------------------------------
    inventory = convergence.get("numeric_inventory") or {}
    referenced = inventory.get("referenced") or []
    unreferenced = inventory.get("unreferenced") or []
    total = inventory.get("total", len(referenced) + len(unreferenced))
    skipped = inventory.get("skipped") or []
    out("## 12. ★ 수치 인벤토리 — 전수 수확 (재정 P-B)")
    out()
    out("수치는 접지 스팬과 서지면에서 **전수 기계 수확**되었고, 중요분은 LLM 의 중요도")
    out("판단이 아니라 함의·포지셔닝이 실제로 참조했는가(`numeric_refs`)로 **역참조 도출**된다.")
    out()
    # ★ 계수의 범위를 밝힌다(2026-08-18 통주 2 처분). 구 문언은 "전체 34건 — 참조 3건"이라
    #   적었는데 그 런의 실제 역참조 대상은 4였다(하나는 `figure-sourced` 라 정답지 밖이다).
    #   범위를 밝히지 않은 수치가 이 리포가 M-04 로 벌한 형태이며, 같은 형태를 우리 표면이
    #   짓고 있었다. 이제 무엇을 세는 계수인지가 헤드라인 안에 있다.
    out(
        f"**수확 정답지 {total}건({ANSWER_SCOPE_TEXT}) — 참조 {len(referenced)}건 표시, "
        f"미참조 {len(unreferenced)}건 접힘**"
    )
    out()
    out("_카운트를 상시 표기하는 이유: 카운트가 없으면 미참조분 접힘이 은폐가 된다._")
    out()
    # 역참조는 정답지 밖 항목(도면 유래·파생)도 가리킬 수 있다. 그 차이를 적지 않으면
    # "역참조 N건"과 "참조 M건 표시"가 한 문서 안에서 어긋난 채로 남는다.
    refs_all = _numeric_ref_targets(spec)
    outside = [ref for ref in refs_all if ref not in set(referenced) | set(unreferenced)]
    out(
        f"역참조 총 {len(refs_all)}건 중 **{len(outside)}건이 이 정답지 밖**이다"
        + (f" — {', '.join(outside)}" if outside else "")
        + ". 정답지 밖 참조는 수확기 소유가 아닌 수치(`derived`·`figure-sourced`)이거나"
    )
    out("철회·대체된 항목이며, 위 계수에 들지 않는다.")
    out()
    out("### 12.1 참조된 수치 (함의·포지셔닝의 근거)")
    out()
    if not referenced:
        out("_참조된 수치 없음._")
        out()
    for item_id in referenced:
        item = index.get(item_id) or {}
        out(f"- {_fact_line(item)}")
        source = item.get("source") or {}
        if source:
            out(f"  - 원천 `{source.get('locator', '')}`: “{source.get('quote', '')}”")
        out(f"  - 이 수치를 참조한 항목: {', '.join(_referrers(spec, item_id)) or '(없음)'}")
    out()
    out(f"### 12.2 미참조 수치 {len(unreferenced)}건 (접힘 — 숨김이 아니다)")
    out()
    out("<details>")
    out(f"<summary>미참조 {len(unreferenced)}건 펼치기</summary>")
    out()
    if not unreferenced:
        out("_미참조 수치 없음 — 수확분 전량이 함의·포지셔닝의 근거로 쓰였다._")
        out()
    for item_id in unreferenced:
        item = index.get(item_id) or {}
        out(f"- {_fact_line(item)}")
        source = item.get("source") or {}
        if source:
            out(f"  - 원천 `{source.get('locator', '')}`: “{source.get('quote', '')}”")
    out()
    out("</details>")
    out()
    out("★ 미참조 수치를 본문이 처음 인용하면 CP2 에 **\"미검토 수치 사용\" 플래그**가 자동")
    out("첨부된다(재정 P-B). 무검토 게시 경로는 없다 — 모든 수치는 CP1 검토 또는 사용 시 검토다.")
    out()
    # ★ 12.3 은 **조건 없이** 렌더한다(2026-08-18 통주 2 처분). 구 코드는 `if skipped:` 였고,
    #   그래서 "빠진 토큰 없음"과 "이 절을 만들지 않았음"이 표면에서 같은 모습이었다 —
    #   누락과 없음의 구별은 이 리포의 상시 규율이다.
    out(f"### 12.3 수확하지 못한 토큰 {len(skipped)}건 (숨기지 않고 센다)")
    out()
    out("수확 전 단계에서 갈린 자리를 **전부** 싣는다. 세 갈래에서 온다 — ① 좌표 표현 봉투")
    out("배제(FP 3항 표기·비트 슬라이스·도면/표 번호·아래첨자 인덱스) ② 토큰 경계 기각")
    out("(`cm3` 의 `3` 처럼 영숫자 토큰 내부) ③ 값 문법 파싱 실패. 시끄럽게 실패하되")
    out("스테이지를 죽이지 않는다 — 수확은 검사가 아니다.")
    out()
    out("사유 라벨의 정본은 `reader/reader-rules.yaml#numeric_harvest` 의")
    out("`exclusions[].reason_label` 과 `token_boundary.rejection_labels` 다.")
    out()
    out("★ **배제 구간 수와 사라진 수치 수는 다르다.** 봉투 하나가 여러 수확을 막을 수 있다")
    out("(예: `Act 0 <6:3>` 한 구간이 `0`·`<6`·`3` 셋을 막는다). 아래 소계는 **구간**을 센다.")
    out()
    out("| 사유 | 건수 |")
    out("|---|---|")
    tally = _skip_tally(skipped)
    if not tally:
        out("| _없음_ | 0 |")
    for reason, count in tally:
        out(f"| `{reason}` | {count} |")
    out()
    out("<details>")
    out(f"<summary>전건 {len(skipped)}건 펼치기</summary>")
    out()
    out("| 위치 | 토큰 | 사유 |")
    out("|---|---|---|")
    if not skipped:
        out("| _없음_ | _없음_ | 수확 전 단계에서 갈린 자리가 없다 |")
    for entry in skipped:
        out(
            f"| `{entry.get('locator', '')}` | `{entry.get('token', '')}` | "
            f"{entry.get('reason', '')} |"
        )
    out()
    out("</details>")
    out()

    # -- 13. 수렴 프로파일 (재정 P-3) ---------------------------------------
    report = convergence.get("convergence_report") or {}
    axes = report.get("axes") or []
    escalations = report.get("escalations") or []
    divergences = report.get("divergences") or []
    out("## 13. 독해 프로파일 — 수렴 (재정 P-3)")
    out()
    out("**이 절은 결함 후보 목록이 아니다.** 두 독립 분해가 어떻게 갈렸는가의 기술이며,")
    out("갈림 자체가 실패를 뜻하지 않는다. 축은 세 층으로 읽는다 — `exact-match`(구조 사실:")
    out("법) · `escalation-trigger`(해석 여지: 미달 = 실패가 아니라 상신) · `measure-only`")
    out("(판정 제외·측정 전용).")
    out()
    out("| 축 | 정책 | 값 | 임계 | 상태 |")
    out("|---|---|---|---|---|")
    if not axes:
        out("| _없음_ | - | - | - | 수렴 검사가 돌지 않았다 |")
    for axis in axes:
        jaccard = axis.get("jaccard")
        threshold = axis.get("threshold")
        out(
            f"| `{axis.get('id', '')}` | `{axis.get('policy', '')}` | "
            f"{'-' if jaccard is None else f'{jaccard:.4f}'} | "
            f"{'-' if threshold is None else threshold} | `{axis.get('status', '')}` |"
        )
    out()
    if escalations:
        out("### 13.1 상신 축 — Owner 판단 대상")
        out()
        for entry in escalations:
            out(
                f"- `{entry.get('axis', '')}` — 실측 {entry.get('jaccard')} "
                f"< 임계 {entry.get('threshold')}"
            )
        out()
    if divergences:
        out("### 13.2 갈린 항목")
        out()
        for entry in divergences:
            out(f"- `{entry.get('axis', '')}`")
            for value in entry.get("only_in_canonical") or []:
                out(f"  - 정본에만: {value}")
            for value in entry.get("only_in_peer") or []:
                out(f"  - 비교본에만: {value}")
        out()

    # -- 14. 도면 ----------------------------------------------------------
    out("## 14. 도면")
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

    # -- 15. 항목 색인 ------------------------------------------------------
    out("## 15. 항목 색인 (전량)")
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

    # -- 16. 절차 이력 ------------------------------------------------------
    provenance = spec.get("provenance") or {}
    out("## 16. 절차 이력")
    out()
    out("| 항목 | 값 |")
    out("|---|---|")
    selection = convergence.get("canonical_selection") or {}
    out(f"| 독립 실행 | {', '.join(provenance.get('read_runs') or [])} |")
    out(f"| 정본 실행 | `{selection.get('read_run', '')}` |")
    out(f"| 정본 지정 규칙 | `{selection.get('rule', '')}` · 내용맹 `{selection.get('content_blind', '')}` |")
    out(f"| 산출 시각 | {provenance.get('produced_at', '')} |")
    out(f"| 엔진 커밋 | `{provenance.get('engine_commit', '')}` |")
    out()
    out("분해는 **두 독립 실행**이 돌았고, 접지 이후는 **정본 1개**만 돌았다(재정 P-4).")
    out("정본 지정은 선언 순서이며 **내용을 보지 않는다** — 수렴 통과는 두 독해가 동치라는")
    out("선언이므로 정본 선택에 판정자가 없고, 남는 요구는 재현성뿐이기 때문이다. 두 실행은")
    out("서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.")
    out()
    return "\n".join(lines)


def _numeric_ref_targets(spec: dict) -> list[str]:
    """`numeric_refs` 가 가리킨 항목 ID 전량(중복 제거 · 등장 순).

    수확 정답지 계수와 함께 실어야 하는 값이다 — 역참조는 정답지 **밖**(도면 유래·파생·
    철회분)도 가리킬 수 있고, 그 차이를 적지 않으면 "역참조 4건"과 "참조 3건 표시"가 한
    문서 안에서 어긋난 채로 남는다. 통주 2 판독본이 실제로 그 상태였다.
    """
    out: list[str] = []
    for item in spec.get("items") or []:
        for ref in item.get("numeric_refs") or []:
            if isinstance(ref, str) and ref not in out:
                out.append(ref)
    return out


def _skip_tally(skipped: list) -> list[tuple[str, int]]:
    """수확하지 못한 자리를 **사유별로** 센다(건수 내림차순 · 동수는 라벨 순).

    전건 목록만 두면 "무엇이 얼마나 빠졌는가"를 사람이 손으로 세야 하고, 그러면 표가 길어질수록
    아무도 세지 않는다. 소계가 없는 목록은 숨기지 않았을 뿐 보이지도 않는다.
    """
    tally: dict[str, int] = {}
    for entry in skipped:
        reason = str(entry.get("reason", ""))
        tally[reason] = tally.get(reason, 0) + 1
    return sorted(tally.items(), key=lambda pair: (-pair[1], pair[0]))


def _referrers(spec: dict, fact_id: str) -> list[str]:
    """이 수치를 `numeric_refs` 로 가리킨 함의·포지셔닝 항목의 ID(재정 P-B).

    역참조를 **양방향으로** 보여주는 이유: "이 수치가 왜 중요분인가"의 답은 그것을 근거로
    삼은 항목이며, 그 연결이 표면에 없으면 Owner 는 중요분 선정을 검증할 수 없다.
    """
    out: list[str] = []
    for item in spec.get("items") or []:
        if item.get("kind") not in ("implication", "positioning"):
            continue
        if fact_id in (item.get("numeric_refs") or []):
            out.append(str(item.get("id")))
    return out
