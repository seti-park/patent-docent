# -*- coding: utf-8 -*-
"""독해 LLM 레인의 **계약 경계**.

이 리포의 엔진은 파이썬 프로세스이고 LLM API 클라이언트를 갖지 않는다(키·SDK 없음).
실제 레인 구동은 상위 오케스트레이터(Claude Code 세션)가 서브에이전트로 한다. 따라서
여기 있는 것은 호출기가 아니라 **계약**이다 — 요청을 파일로 내고 응답을 파일로 받는다.

이것이 타협이 아니라 설계인 이유: 레인 요청·응답이 파일로 남으면 런의 **감사 가능성**이
생긴다. 어떤 프롬프트에 어떤 모델이 무엇을 답했는가가 런 폴더 안에 남고, 사후에
`requested_model != actual_model` 을 대조할 수 있다(SPEC §7.3 펜 배정 규율 3·4의 정신).

★ 다만 파일로 남는 것만으로는 부족하다는 것이 2026-08-18 의 실측이다 — 같은 요청 자리에
응답이 두 번 쓰였고 런이 어느 쪽을 소비했는지 증명하지 못했다(감수 OOS-02). 그래서 왕복에
**시점**을 넣는다: 요청 지문 → 응답의 반향 → 레인 로그의 응답 지문 → 러너의 거부(재정 P-12).
"""

from __future__ import annotations

from .contract import (
    LaneAdapter,
    LaneContractError,
    LanePending,
    LaneRequest,
    LaneResponse,
    LaneStaleResponseError,
    render_request_md,
)
from .file_adapter import FileLaneAdapter
from .replay_adapter import ReplayLaneAdapter

__all__ = [
    "FileLaneAdapter",
    "LaneAdapter",
    "LaneContractError",
    "LanePending",
    "LaneRequest",
    "LaneResponse",
    "LaneStaleResponseError",
    "ReplayLaneAdapter",
    "render_request_md",
]
