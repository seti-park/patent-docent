# -*- coding: utf-8 -*-
"""게이트 — 정답이 존재하는 범위만 판정하는 결정론 층(D7 · D8).

이 패키지가 실물로 갖는 것은 **L0 결정론 층**(`engine/gate/l0/`)과 문장 계수(`sentence_count.py`)뿐이다
(재정 2026-09-13 T64 ② · M3). L1 국소 대조 · L2 자문 · 화행 플래그 · 최종 심급은 계약(`contracts/stages/gate.yaml`
`layers` 블록)이 미가동으로 적고, 러너(`engine/stages/gate.py`)가 그 사실을 판정문에 옮긴다.

★ 게이트는 글을 고치지 않는다(D8). 여기 어떤 함수도 본문 문자열을 돌려주지 않으며, 결함 레코드의
`fix_directive` 는 「어디를 · 어느 재료로」 지시문이다(SPEC §4.7).
"""

from __future__ import annotations

__all__: list[str] = []
