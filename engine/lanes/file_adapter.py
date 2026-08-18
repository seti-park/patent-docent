# -*- coding: utf-8 -*-
"""파일 기반 레인 어댑터 — 실 운용 경로.

배치 하나를 받으면 **요청 전량을 먼저 쓰고**(오케스트레이터가 한 번에 팬아웃할 수 있게)
그다음 응답을 모은다. 하나라도 없으면 `LanePending` 을 던지며 **기다리지 않는다**.

★ 쓰기가 읽기보다 먼저인 이 순서가 시점 결속을 실효로 만든다(재정 P-12). 요청이 갱신되면
`request.json` 의 입력 지문이 먼저 바뀌고, 같은 자리에 남아 있던 옛 응답은 그 다음 걸음에서
반향 불일치로 걸린다 — 러너가 낡은 응답을 소비하는 창이 열리지 않는다.

★ 재진입이 **내용이 같은 요청을 다시 쓰지는 않는다**(재정 2026-08-19 Q8 ③ 파생 · 총괄 재량).
건너뛰는 것은 바이트가 동일할 때뿐이므로 위 순서의 보증은 그대로다 — 요청이 갱신되면 지문이
바뀌고, 지문이 바뀌면 파일도 바뀌므로 쓰기가 일어난다.
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
        """요청 1건을 기계 판독본과 사람 판독본 두 벌로 남긴다.

        ★ **내용이 같으면 다시 쓰지 않는다**(재정 2026-08-19 Q8 ③ 파생 · 총괄 재량 처분 —
        명시 재정 아님). 러너 재진입(`LanePending` 뒤의 같은 스테이지 재호출)은 같은 요청을
        다시 계획하고 그때마다 두 파일을 덮어썼다. 오염은 없었다 — 통주 3 의 통합 레인이
        지문을 재계산해 MATCH 를 확인했고, 재정 P-12 가 정확히 그 자리를 위해 설계되었다.
        그러나 **요청 파일의 수정 시각이 응답보다 뒤에 서는** 산출이 남았고, 사후 감사가
        그것을 "응답 뒤에 요청이 바뀌었다"로 읽는다. 바이트가 같은데 시각만 흔드는 쓰기는
        기록을 늘리지 않고 사료만 흐린다.

        ★ 이것은 **관찰 좌표의 신설이 아니다.** 요청 파일 쪽 지문을 레인 로그에 더하는 안
        (응답 쪽 `response_digest` 의 거울상)은 판정 관할의 확장이므로 **재정 사항**이며
        총괄이 상신했다 — 여기서 하지 않는다. 여기서 한 것은 "쓸 필요가 없을 때 쓰지 않는다"
        하나이고, 요청 내용이 실제로 바뀌면 파일도 지문도 그대로 바뀐다.
        """
        directory = lane_dir(self.root, request.lane_id)
        os.makedirs(directory, exist_ok=True)
        body = json.dumps(
            request.to_dict(), ensure_ascii=False, indent=2, sort_keys=True
        ) + "\n"
        _write_if_changed(os.path.join(directory, REQUEST_JSON), body)
        _write_if_changed(
            os.path.join(directory, REQUEST_MD), render_request_md(request, self.repo)
        )
        return directory


def _write_if_changed(path: str, text: str) -> bool:
    """바이트가 다를 때만 쓴다. 반환 = 실제로 썼는가.

    비교를 바이트로 하는 이유는 판정이 파일 그 자체여야 하기 때문이다 — 텍스트로 읽고 다시
    인코딩해 비교하면 개행·인코딩 처리에 따라 "같다"의 뜻이 플랫폼마다 갈린다(같은 이유로
    `load_response` 도 응답을 바이트로 읽는다).
    """
    blob = text.encode("utf-8")
    try:
        with open(path, "rb") as handle:
            if handle.read() == blob:
                return False
    except FileNotFoundError:
        pass
    with open(path, "wb") as handle:
        handle.write(blob)
    return True
