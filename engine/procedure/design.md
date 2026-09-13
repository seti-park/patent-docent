# 설계 레인 절차 — `design/blueprint`

정본 서술 = `docs/SPEC.md` §1.7. 이 문서는 요청서에 인라인되어 레인이 읽는 절차이며, 값·필드명은 EN 원문이고 산문은 KR 이다.

## 0. 직무

동결 재료로부터 레시피를 만든다 — 훅·논지·트윗 골격·도면 배치(D6). 독자는 학습자가 아니라 투자자-팬이므로(D2) 훅은 그 불안·질문에 조응하되, 답은 특허 물증에 근거한 기술 서사로만 하도록 골격을 짠다(D3).

너는 원천을 보지 않는다. 요청서의 「원천 조각」 절에 실린 동결 재료(`material-spec.v<N>.json`)가 네가 아는 전부이며, 그 안의 ID(`M<n>` · `FIG-…`)만이 네가 쓸 수 있는 좌표다.

## 1. 순서

⑴ **재료 통독.** 구성요소 트리(`claims` · `items[kind == "component"]`) → 접지(`items[kind == "grounding"]`) → 기술적 함의(`items[kind == "implication"]`) → 포지셔닝(`items[kind == "positioning"]`) → 도면 주석(`items[kind == "figure_note"]` · `figures[]`) 순으로 읽는다. `status == "active"` 인 항목만 재료다.

⑵ **강한 전시물 후보 열거.** 전시물 = 구성요소 묶음 + 그것을 보이는 도면 + 그 묶음이 내는 함의. 후보마다 재료 ID(`M<n>`)와 도면 ID(`FIG-…`)를 붙여 적는다. 도면 없이 서는 전시물은 후보에서 뒤로 민다.

⑶ **훅.** 투자자-팬의 질문(D3 — 「해자가 진짜인가」 「이것이 왜 지금 되는가」 류)을 EN 한 문장으로 `hook.question_en` 에 적는다. 그 질문에 답하는 최강 도면 하나를 `hook.figure` 에 지정하고, 답의 논지를 `hook.thesis_en` 에 EN 한 문장으로 적는다. 왜 그 질문·그 도면인지는 `hook.rationale_kr` 에 KR 로 적는다.

⑷ **슬롯 아크.** D11 ③ — `hook` → `stop`/`pivot` … → `landing` → `tail`. 각 `slots[]` 원소는 `n`(1부터 연속) · `slot` · `exhibit`(`material_ids` + `point_en`) · `figures` 를 갖는다. 트윗 수는 강한 전시물 수의 종속변수다 — 분량을 채우려 쪼개지 않고, 초기 런은 적은 쪽으로 간다. 각 `stop` 은 **구성요소 하나**를 제시한다. `pivot` 은 질문에 답하는 결정적 물증이다. `landing` 은 안도감 결론이고 `tail` 은 있으면 마지막이다. 시트 값(요청서의 「시트 값」 표)이 개수·위치의 판정 기준이다.

⑸ **전달 표적.** `transmission_targets` = 독자가 다 읽고 기억해야 하는 재료 ID 목록. 이것이 계기 질문의 유일한 파생원이다(D9). 슬롯이 전시한 재료 중 논지를 지탱하는 것만 고른다.

⑹ **용어 메모.** `new_terms` = 도입할 신규 용어(`term_en`)와 배정 트윗(`tweet`) · 한 줄 풀이(`gloss_en`). 작업 메모이며 게이트는 이것을 읽지 않는다.

⑺ **도면 계획.** `figure_plan` 은 트윗마다 한 원소(`tweet` = 그 슬롯의 `n`)이며 `figures` 는 그 슬롯의 `figures` 와 같은 집합이고 `intent_kr` 에 무엇을 보이려는지 적는다. 이번 초안은 도면을 **지정만** 한다 — 자산은 아직 없다.

⑻ **허용 수치.** `numeric_whitelist` 에는 스레드 순번 `n/N` 하나만 제안한다(`pattern` 은 MATCH_KEY 형태 `n/N|` 에 fullmatch 되는 정규식 — 예 `^\d{1,2}/\d{1,2}\|$` · 키 끝의 `|` 는 단위 자리가 비었다는 표기이며 패턴이 그것까지 덮어야 닿는다 · `rationale` 은 한 줄). 재료에 없어도 허용할 수치는 그것뿐이다.

⑼ **상신.** 재료로 훅이 서지 않으면 `escalation: {reason: "hook-not-feasible", note_kr}` 를 채우고 나머지는 최선의 초안으로 둔다. 강한 전시물이 시트의 `tweet_count.max` 를 넘으면 `escalation: {reason: "exhibit-overflow", note_kr}` 와 `overflow_proposal: {proposal, rationale_kr}` 를 함께 채운다 — 자르지도 쪼개지도 않는다. 선별인지 시리즈 분할인지는 Owner 가 결정한다. 상신이 없으면 `escalation` 과 `overflow_proposal` 은 둘 다 `null` 이다.

⑽ **응답.** `payload` 하나를 응답 계약(요청서의 `response_schema`)대로 낸다. 모든 재료 ID·도면 ID 는 동결 재료의 것이며, 재료에 있는 사실만 쓴다. EN 값은 EN 으로, `*_kr` 필드는 KR 로 적는다.
