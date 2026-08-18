# -*- coding: utf-8 -*-
"""파일 기반 레인 어댑터 — 실 운용 경로.

배치 하나를 받으면 **요청 전량을 먼저 쓰고**(오케스트레이터가 한 번에 팬아웃할 수 있게)
그다음 응답을 모은다. 하나라도 없으면 `LanePending` 을 던지며 **기다리지 않는다**.

★ 쓰기가 읽기보다 먼저인 이 순서가 시점 결속을 실효로 만든다(재정 P-12). 요청이 갱신되면
`request.json` 의 입력 지문이 먼저 바뀌고, 같은 자리에 남아 있던 옛 응답은 그 다음 걸음에서
반향 불일치로 걸린다 — 러너가 낡은 응답을 소비하는 창이 열리지 않는다.
"""

from __future__ import annotations

import json
import os

from .contract import (
    REQUEST_JSON,
    REQUEST_MD,
    RESPONSE_JSON,
    LanePending,
    LaneRequest,
    LaneResponse,
    lane_dir,
    load_response,
    render_request_md,
)
from ..paths import repo_root


class FileLaneAdapter:
    """`<root>/<lane_id>/{request.json,request.md,response.json}` 레이아웃."""

    def __init__(self, root: str, repo: str | None = None) -> None:
        self.root = os.path.abspath(root)
        self.repo = repo or repo_root()

    # -- LaneAdapter --------------------------------------------------------

    def dispatch(self, requests: list[LaneRequest]) -> list[LaneResponse]:
        for request in requests:
            self.write_request(request)
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

    # -- 요청 기록 ----------------------------------------------------------

    def write_request(self, request: LaneRequest) -> str:
        """요청 1건을 기계 판독본과 사람 판독본 두 벌로 남긴다."""
        directory = lane_dir(self.root, request.lane_id)
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, REQUEST_JSON), "w", encoding="utf-8") as handle:
            json.dump(request.to_dict(), handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        with open(os.path.join(directory, REQUEST_MD), "w", encoding="utf-8") as handle:
            handle.write(render_request_md(request, self.repo))
        return directory
