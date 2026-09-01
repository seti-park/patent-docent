---
schema: approval-envelope/v0
checkpoint: material_approval
run_id: gdm-wo2026128750a1-agent-memory
target:
  path: 10-read/material-spec.json
  digest: sha256:e146a956a9b693c0e2dd55e6be8137a3658412a94605c081d3918618a67bb0b7
decision: approved
owner_quote: 승인
quote_provenance:
  channel: session-transcript
  located_at: 'session_011sBzix6vtfqZryjyGYhcat — CP1 판독본(artifact cb8f3183) 제시 + 고지 2건(수렴 미달 잔존 · 수확 정답지가 도면부호뿐) 이후 Owner 회신. 도면 유래 수치 3건의 확인은 그 직전 육성 「도면 세 건 모두 셋 다 맞아」이며 이것과 층이 다르다'
decided_at: '2026-09-01T03:24:30Z'
recorded_by: orchestrator
numeric_whitelist_printed: []
manual_verification_ack:
  - M124
  - M125
  - M126
derived_fact_ack: []
---

# CP1 승인 봉투 — `gdm-wo2026128750a1-agent-memory` 판 1

## 육성 3건은 층이 다르다

| 육성 | 무엇을 했나 |
|---|---|
| `a` | 조기 수렴 '계속' — **재료 승인이 아니다**(봉투 = `10-read/convergence-continue.md`) |
| `도면 세 건 모두 셋 다 맞아` | **ack 근거** — M124·M125·M126 개별 값 확인. `owner_quote` **아님** |
| **`승인`** | **CP1 재료 승인** — 이 봉투의 `owner_quote` |

## 승인 시점에 고지된 것 둘 — 알고 넘어간 기록

**⑴ 수렴 미달이 완주 판정서에 남아 있다.** `tree-edges` **0.0909**(임계 0.95)가
`escalate` 로 살아 있다. 이 재료는 **두 번째 실행이 갈린 독해 위에** 선다 — 정본
`read-a` 는 경계 규약을 지킨 쪽이고 갈린 원인은 좌표 하나(`CL-1.text_verbatim` 868 B ↔ 42 B)로
진단되었다. 재정 **T14 ⒟** 의 CP1 재고지 의무는 이 문단으로 이행되었다.

**⑵ 수확 정답지가 도면부호뿐이다.** `origin: quoted` **7건 전량**이 도면부호(`204-1`·`202-1`·
`53`·`50`·`50`·`63`·`60`)이며 측정값이 아니다. 원인 둘 — 배제 정답지(`figures[].numerals`)를
레인이 채우므로 레인의 누락이 곧 배제의 누락이 되는 **구조 문제**, 그리고 하이픈 부호(`204-1`)를
정수 조건이 잡지 못하는 **어형 문제**. **재정 Q4 동결이므로 등재만 하고 고치지 않았다.**
재료 자신이 이 사실을 **M146** 에서 신고한다.

## 파생 수치 없음

`derived_fact_ack` 는 **빈 배열**이다 — 이 판에 `origin: derived` 항목이 없다(판독본 §6.2).
빈 배열이 서명이 아니라 사실인 자리다.
