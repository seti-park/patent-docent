# -*- coding: utf-8 -*-
"""기록 재생 어댑터 — 테스트·재현 전용.

같은 레이아웃에서 **응답만** 읽고 요청은 쓰지 않는다. 실행 경로의 시험대가 자기가 쓴
요청을 다시 읽는 구조가 되면, 요청 생성이 틀려도 시험이 통과한다 — 재생 어댑터는 미리
준비된 응답 트리 위에서만 돌기 때문에 그 자기충족이 성립하지 않는다.

★ 시점 결속(재정 P-12)에 대해서도 이 어댑터는 관대해지지 않는다 — `load_response` 를 그대로
쓰므로 응답 트리가 반향 지문을 들고 있지 않으면 재생이 실패한다. 기록된 런의 재생은 그 조건을
자연히 만족한다(실행 당시 레인이 반향을 적었기 때문이다). 반면 **합성 픽스처**는 요청이
존재하기 전에 저작되므로 반향을 가질 수 없고, 그 자리를 메우는 일은 라이브러리가 아니라
테스트 하네스의 몫이다 — 여기에 "없으면 채워 준다"를 넣는 순간 그 관대함이 실 운용 경로로
새어 나간다.
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
