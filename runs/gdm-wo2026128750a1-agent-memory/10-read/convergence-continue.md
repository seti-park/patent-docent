---
schema: approval-envelope/v0
checkpoint: convergence_continue
run_id: gdm-wo2026128750a1-agent-memory
target:
  path: 10-read/convergence-early.json
  digest: sha256:90dca50a682181f3bfc738aa75e46ef1bbf83bf548067be2617f73e69d39c8c4
decision: approved
owner_quote: a
quote_provenance:
  channel: session-transcript
  located_at: 'session_011sBzix6vtfqZryjyGYhcat — WO READ 부분 시험 v3 보고 직후, 총괄이 제시한 선택지 ⓐ·ⓑ·ⓒ 중 ⓐ("계속 봉투를 내고 read-a 로 진행")를 가리키는 회신. 재정 원장 = docs/decisions/ruling-20260901-05-T14.md'
decided_at: '2026-09-01T02:26:00Z'
recorded_by: orchestrator
---

# 조기 수렴 '계속' 봉투 — `gdm-wo2026128750a1-agent-memory`

**★ 이 봉투는 미달을 없애지 않는다. 알고 넘어간다는 기록이다.**

## 무엇이 미달했나

`10-read/convergence-early.json`(`attempt: 1`)의 상신 축 **`tree-edges` = 0.0909**(임계 0.95).
계약이 이 조건에 정한 조치는 재시도가 아니라 **상신**이다(`read.yaml#failure` · 재정 P-3).

나머지 축은 전부 섰다 — `independent-count` pass · `dependent-count` pass ·
`element-set` **1.0000** · `dependent-set` **1.0000** · `addition-attachment` 0.6724(판정 제외).

## 원인 — 좌표 하나

| 실행 | `CL-1.text_verbatim` |
|---|---|
| **read-a**(정본) | **868 B** — 청구항 전문 |
| read-b | **42 B** — 전제부만(`A computer-implemented method, comprising:` · 콜론에서 끊음) |

최상위 element 의 부모 문언이 통째로 갈려 6간선 중 1개만 공유 → **1/11 = 0.0909**.
**성문 규약 위반이다** — `reader/procedure/10-decompose.md` 의 경계 규약 ②는
*"마지막 마침표까지가 청구항이다"* 이며 **read-a 가 지켰고 read-b 가 어겼다.**

## 무엇을 감수하는가

**수렴이 실제로는 미달인 채로 접지에 들어간다.** 이 런의 CP1 판독본은 **두 번째 실행이 갈린
독해 위에** 선다. 정본 `read-a` 는 규약을 지킨 쪽이므로 산출물 오염은 없으나,
**「봉투를 냈으므로 수렴이 성립했다」로 읽어서는 안 된다.**

**★ 이 사실은 CP1 상신 때 Owner 에게 다시 고지된다**(재정 T14 ⒟).

## 후속

청구항 전문 완전성 검사의 부재가 백로그 **G-9** 로 등재되었다 — 잘린 `text_verbatim` 은 원천의
정당한 부분문자열이라 `read.verbatim` 을 통과하고 `read.claim-inventory` 는 번호만 본다.
그래서 이번 잘림은 레인 단계에서 잡히지 않고 `tree-edges` 붕괴라는 **먼 증상**으로만 드러났다.
