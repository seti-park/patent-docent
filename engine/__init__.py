# -*- coding: utf-8 -*-
"""`engine/` — 런 작업장 위에서 스테이지를 돌리는 러너 층.

의존 방향은 한 갈래다: `engine/` 은 `reader/lib` 을 import 하고 그 반대는 없다
(SPEC §6.2 판별식 1 — `reader/` 는 이식 단위이므로 파이프라인을 모른다).
따라서 독해층 검사의 구현은 여기 없다. 여기 있는 것은 **검사를 어디서 무엇에 대고
돌릴 것인가**, 그리고 **LLM 레인과 어떤 계약으로 주고받을 것인가**뿐이다.

이 층의 규율 셋(전부 M1 발주 문언 그대로다).

1. 수치·경로·모델 지정을 코드에 리터럴로 박지 않는다. 런 트리 경로는
   `contracts/stages/*.yaml`, 형식 수치는 `contracts/format-parameters.yaml`,
   레인 모델·effort 는 `contracts/stages/read.yaml#lane.sub_lanes` 가 정본이다.
2. `assert` 를 쓰지 않는다 — `python3 -O` 에서 전부 제거되어 망가진 코드가 공허 통과한다
   (CLAUDE.md §3). 불변식 위반은 예외로 던지거나 판정 행의 결함으로 낸다.
3. 무인 실행 플래그(`--yes` 류)를 만들지 않는다. 체크포인트 무응답은 무기한 대기이며
   시간 초과 자동 진행 경로는 존재하지 않는다(재정 R8).
"""

from __future__ import annotations

__all__ = ["gitpin", "paths", "read_view", "lanes", "stages", "render"]
