# -*- coding: utf-8 -*-
"""기록 재생 어댑터 — 테스트·재현 전용.

같은 레이아웃에서 **응답만** 읽고 요청은 쓰지 않는다. 실행 경로의 시험대가 자기가 쓴
요청을 다시 읽는 구조가 되면, 요청 생성이 틀려도 시험이 통과한다 — 재생 어댑터는 미리
준비된 응답 트리 위에서만 돌기 때문에 그 자기충족이 성립하지 않는다.
"""

from __future__ import annotations

import os

from .contract import (
    RESPONSE_JSON,
    LanePending,
    LaneRequest,
    LaneResponse,
    lane_dir,
    load_response,
)


class ReplayLaneAdapter:
    """`<root>/<lane_id>/response.json` 만 읽는 어댑터."""

    def __init__(self, root: str) -> None:
        self.root = os.path.abspath(root)
        # 무엇을 요청받았는지는 기록해 둔다 — 어떤 단계가 실제로 돌았는지(예: 조기 drop
        # 신호가 접지 지출 전에 멈췄는지)를 시험이 확인할 수 있어야 한다.
        self.dispatched: list[LaneRequest] = []

    def dispatch(self, requests: list[LaneRequest]) -> list[LaneResponse]:
        self.dispatched.extend(requests)
        pending: list[str] = []
        responses: list[LaneResponse] = []
        for request in requests:
            path = os.path.join(lane_dir(self.root, request.lane_id), RESPONSE_JSON)
            if not os.path.exists(path):
                pending.append(request.lane_id)
                continue
            responses.append(load_response(request, path))
        if pending:
            raise LanePending(pending, self.root)
        return responses

    def tasks_dispatched(self) -> list[str]:
        return [request.task for request in self.dispatched]
