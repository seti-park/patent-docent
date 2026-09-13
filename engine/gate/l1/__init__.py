# -*- coding: utf-8 -*-
"""L1 국소 대조(재정 2026-09-13 T67 ② · M6-a).

`plan.py` = 요청 조립(어휘 `gate-l1/<v>/batch-<i>` · payload 스키마 · 절차 문서 인라인) ·
`merge.py` = k 표 병합(다수결 · 강등 · 불일치 로그 · 화행 표수 — SPEC §4.5 글자 그대로) ·
`procedure.md` = L1 레인 절차 문서(검증 심급이므로 금지 열거를 담는다 — D8 의 펜 규율과 층이 다르다).
"""

from .merge import merge as merge_votes
from .plan import RESPONSE_SCHEMAS, GateL1LaneRequest, build_request, l1_config, lane_id_for, payload_schema

__all__ = [
    "RESPONSE_SCHEMAS",
    "GateL1LaneRequest",
    "build_request",
    "l1_config",
    "lane_id_for",
    "merge_votes",
    "payload_schema",
]
