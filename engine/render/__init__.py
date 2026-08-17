# -*- coding: utf-8 -*-
"""결정론 렌더 — 기계 정본을 사람이 판정할 수 있는 표면으로 편다.

렌더는 **같은 입력에 같은 바이트**를 낸다(시각·난수·순회 순서 의존 금지). 그래야
`freeze.render-parity` 의 재생성 지시가 의미를 갖는다 — 다시 렌더했더니 다른 문서가
나온다면 무엇이 승인된 것인지 말할 수 없다.
"""

from __future__ import annotations

from .material_spec_md import render

__all__ = ["render"]
