# -*- coding: utf-8 -*-
"""원천 슬라이싱 — 레인에게 **필요한 조각만** 준다.

레인에 원천 전문을 통째로 주지 않는 이유는 비용이 아니라 **주의 집중**이다. 청구항을
분해하는 레인에게 배경기술 30문단을 함께 주면 분해가 요약으로 미끄러진다.

★ 청구항 구간·청구항 본문 파서는 `reader/lib/inventory.py` 의 것을 **재사용**한다.
파서를 다시 쓰면 두 벌 중 하나는 반드시 낡고, 그때 `source.claims-section` 이 통과시킨
원천이 하류에서 파서 문제로 넘어진다(구현 이중화 금지 — SPEC §8.4 M1).

여기서 새로 파싱하는 것은 원천 정본의 **서식 관습** 둘뿐이다 — `[nnnn]` 문단 번호와
`FIG.` 로 시작하는 캡션 행. 둘 다 청구항 판정에 관여하지 않으므로 규칙 계약
(`reader-rules.yaml`)의 관할 밖이며, 어긋나면 그 슬라이스가 비는 것으로 드러난다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from reader.lib.inventory import claim_body_map, find_claim_section
from reader.lib.rules import Rules

# 문단 번호 `[0041]`. USPTO 전문을 마크다운으로 옮긴 원천의 관습이다.
PARAGRAPH_MARKER = re.compile(r"^\[(?P<number>[0-9]{3,6})\]", re.MULTILINE)
# 도면 캡션 행. `FIG. 2` · `FIGURE 3A` 를 받아 `FIG-2` · `FIG-3A` 로 정규화한다.
FIGURE_CAPTION = re.compile(
    r"^(?:\*\*)?FIG(?:URE)?[.]?\s*(?P<number>[0-9]+[A-Za-z]?)(?:\*\*)?\b",
    re.MULTILINE,
)
HEADING = re.compile(r"^#{1,6}\s", re.MULTILINE)


@dataclass(frozen=True)
class Paragraph:
    """명세서 문단 1개. `locator` 는 재료 명세의 `spec_refs[].locator` 와 같은 문자열이다."""

    locator: str
    text: str
    start: int
    end: int


@dataclass(frozen=True)
class FigureCaption:
    """도면 캡션 1행."""

    figure_id: str
    text: str
    start: int
    end: int


class ReadView:
    """원천 1건에 대한 슬라이스 모음. 원천을 변형하지 않는다(읽기 전용)."""

    def __init__(self, source_text: str, rules: Rules) -> None:
        self.source_text = source_text
        self.rules = rules

    # -- 청구항 (reader/lib 재사용) -----------------------------------------

    def claims_section(self) -> str:
        """청구항 구간 본문. 구간을 찾지 못하면 빈 문자열."""
        section = find_claim_section(self.source_text, self.rules)
        return section.text if section.found else ""

    def claims_section_found(self) -> bool:
        return find_claim_section(self.source_text, self.rules).found

    def claim_bodies(self) -> dict[str, str]:
        """`CL-<n>` → 그 청구항의 원문 본문."""
        return claim_body_map(self.source_text, self.rules)

    # -- 서지 머리 ----------------------------------------------------------

    def bibliographic_head(self) -> str:
        """청구항 구간 헤더 **이전**의 머리글(제목·서지·초록 자리).

        구간 헤더의 위치는 `reader-rules.yaml#claim_inventory.section.headings` 가 정한
        패턴으로 찾는다 — 구간 파서와 같은 규칙 데이터를 쓰되, 파싱은 하지 않는다.
        """
        best = None
        for pattern in self.rules.inventory_heading_patterns:
            match = pattern.search(self.source_text)
            if match and (best is None or match.start() < best):
                best = match.start()
        if best is None:
            return ""
        return self.source_text[:best]

    # -- 명세서 문단 --------------------------------------------------------

    def paragraphs(self) -> list[Paragraph]:
        """`[nnnn]` 단위 문단 목록. 끝은 다음 문단 번호 또는 다음 헤더 또는 파일 끝."""
        marks = list(PARAGRAPH_MARKER.finditer(self.source_text))
        out: list[Paragraph] = []
        for position, mark in enumerate(marks):
            start = mark.start()
            if position + 1 < len(marks):
                end = marks[position + 1].start()
            else:
                heading = HEADING.search(self.source_text, mark.end())
                end = heading.start() if heading else len(self.source_text)
            out.append(
                Paragraph(
                    locator=f"[{mark.group('number')}]",
                    text=self.source_text[start:end].rstrip("\n"),
                    start=start,
                    end=end,
                )
            )
        return out

    def paragraph_block(self) -> str:
        """문단 전량을 한 덩어리로(레인 슬라이스용)."""
        return "\n\n".join(paragraph.text for paragraph in self.paragraphs())

    # -- 도면 캡션 ----------------------------------------------------------

    def figure_captions(self) -> list[FigureCaption]:
        """`FIG.` 로 시작하는 캡션 행 목록. 같은 도면이 두 번 나오면 첫 행만 취한다."""
        out: list[FigureCaption] = []
        seen: set[str] = set()
        for mark in FIGURE_CAPTION.finditer(self.source_text):
            line_end = self.source_text.find("\n", mark.start())
            if line_end == -1:
                line_end = len(self.source_text)
            figure_id = f"FIG-{mark.group('number')}"
            if figure_id in seen:
                continue
            seen.add(figure_id)
            out.append(
                FigureCaption(
                    figure_id=figure_id,
                    text=self.source_text[mark.start():line_end],
                    start=mark.start(),
                    end=line_end,
                )
            )
        return out

    def caption_block(self) -> str:
        return "\n".join(caption.text for caption in self.figure_captions())

    # -- 레인 슬라이스 ------------------------------------------------------

    def slices_for(self, task: str) -> dict:
        """작업별 슬라이스. 여기 없는 조각은 그 레인이 볼 이유가 없는 조각이다."""
        if task == "decompose":
            return {
                "claims-section": self.claims_section(),
                "bibliographic-head": self.bibliographic_head(),
            }
        if task in ("ground-independent", "ground-dependent"):
            return {
                "description-paragraphs": self.paragraph_block(),
                "figure-captions": self.caption_block(),
            }
        if task == "synthesize":
            return {
                "claims-section": self.claims_section(),
                "description-paragraphs": self.paragraph_block(),
                "figure-captions": self.caption_block(),
            }
        raise ValueError(f"알 수 없는 작업: {task}")
