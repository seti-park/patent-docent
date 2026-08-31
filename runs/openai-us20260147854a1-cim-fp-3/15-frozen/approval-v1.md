---
schema: approval-envelope/v0
checkpoint: material_approval
run_id: openai-us20260147854a1-cim-fp-3
target:
  path: 10-read/material-spec.json
  digest: sha256:166104c15d5e753381eea6ee5057af5eaba2d8a0837f3bd3ed0892dfd1680ef8
decision: approved
owner_quote: 통과
quote_provenance:
  channel: session-transcript
  located_at: 'session_011sBzix6vtfqZryjyGYhcat — PD-M1.9 라운드, CP1 상신(D-20260831-01 §12) 직후 Owner 승인 회신'
decided_at: '2026-08-31T11:47:40Z'
recorded_by: orchestrator
numeric_whitelist_printed: []
manual_verification_ack:
  - M107
  - M108
  - M109
derived_fact_ack:
  - M104
  - M105
  - M106
---

# CP1 승인 봉투 — `openai-us20260147854a1-cim-fp-3` (판 1)

**지위.** 재정 R8 의 승인 봉투이며 스키마 대상은 위 프런트매터다. 이 본문은 프런트매터 **밖**이고
스키마가 보지 않는다 — 인용 필드를 오염시키지 않으면서 맥락을 남기는 자리다.

## 1. 두 인용의 역할이 다르다 — 섞지 마라

| 인용 | 육성 원문 | 역할 |
|---|---|---|
| **결정 인용** | **`통과`** | 프런트매터 `owner_quote` 의 값. **이 두 글자가 결정의 전부**이며 다듬거나 늘리거나 번역하지 않았다 |
| **확인 인용** | **`6건 다 맞아`** | **`owner_quote` 가 아니다.** 아래 §2 의 ack 목록 6건에 대한 Owner 응답이며 `manual_verification_ack`·`derived_fact_ack` 의 **근거**다 |

**★ 이 구별을 적는 이유.** 판독본 §0 이 *"`owner_quote` 는 Owner 가 실제로 타이핑한 원문이다.
시스템 요약의 인용은 무효다"* 로 못 박는다. 두 육성을 합치거나 확인 인용을 결정 인용 자리에 넣으면
**결정의 문언이 총괄의 편집을 거친 것이 된다.** 그래서 프런트매터에는 `통과` 만 두고 나머지는
전부 이 본문에 남긴다.

**위조 방어의 한계를 함께 적는다**(스키마 $comment 규율 5): 봉투는 총괄이 **대필**했고 위조 방어는
**규약 기반이며 암호학적 보증이 없다.** 대필 주체가 인용을 날조할 수 있다는 잔여 리스크는 이 리포가
명시 수용한 상태다.

## 2. 확인 6건 — Owner 가 개별로 본 값

**도면 유래 3건**(`figure-sourced` · 기계 검증 불가 · `manual_verification_ack`)

| 항목 | 값 | 도면 | 무엇을 세었나 |
|---|---:|---|---|
| **M107** | 8 | FIG-60 | Table 2 의 동작 모드 행 수 |
| **M108** | 3 | FIG-29 | 12열 공유 셀 안의 가중치 비트 구획 수 |
| **M109** | 4 | FIG-28 | 지수 단(stage)당 멀티플렉서 수 |

**계산 3건**(`derived` · `derived_fact_ack`)

| 항목 | 값 | 산식 | 입력 |
|---|---:|---|---|
| **M104** | 144 | `columns * rows` | M96(12) · M97(12) |
| **M105** | 3600 | `columns * rows` | M91(60) · M92(60) |
| **M106** | 25 | `(wide_columns * wide_rows) / (narrow_columns * narrow_rows)` | M91(60) · M92(60) · M96(12) · M97(12) |

**확인 도구**: 도면 3장(FIG-28 · FIG-29 · FIG-60)을 아티팩트로 제공해 Owner 가 직접 세었다.

## 3. ★ M106 은 **유보를 고지한 뒤 받은 승낙**이다

이 한 건은 나머지 다섯과 격이 다르므로 따로 적는다. 승인 전에 발주자가 Owner 에게 다음을 **사전
고지**했다:

> 실측한 것은 **셀 개수의 비율**인데 판독본이 이 값을 **「면적 증가 배수」**(*growth factor in
> column cell area*)로 명명했다. 그렇게 부르려면 **셀 하나의 크기가 같다는 전제**가 필요한데
> **명세서가 그 전제를 직접 말하지 않는다.**

**Owner 는 그 유보를 포함해 수용했다.**

**★ 이 기록의 목적은 다음 판에서 이 명명을 다시 열 수 있게 하는 것이다.** 승낙이 있었다는 사실과
**무엇을 알고 승낙했는가**가 함께 남아야, 뒷사람이 이 명명을 재검할 때 *"이미 승인된 것"* 으로
닫히지 않는다. 무처분 소멸 금지의 취지가 이 자리에 걸린다 — 값은 승인되었고 **명명은 열려 있다.**

## 4. 봉투 값의 실측 근거

| 필드 | 값의 출처 |
|---|---|
| `run_id` | `run.yaml#run_id` 실측(타이핑하지 않았다) |
| `target.path` | **`10-read/material-spec.json`** — 발주문은 `.md` 를 지정했으나 **정본이 `.json` 을 요구한다**. 사유는 아래 §5 |
| `target.digest` | 승인 시점 `10-read/material-spec.json` 의 SHA-256. `hashlib` 과 `sha256sum` **두 방법으로 대조** |
| `numeric_whitelist_printed` | `run.yaml#numeric_whitelist` 가 **`[]`** 이므로 빈 배열. 추측이 아니라 실측이며, 스키마가 *"run.yaml 의 numeric_whitelist[] 전량 인쇄"* 로 그 파일을 출처로 지정한다 |
| `manual_verification_ack` | `material-spec.json` 의 `origin: figure-sourced` 집합과 **정확히 일치**(판독본 §7 과도 대조) |
| `derived_fact_ack` | 같은 파일의 `origin: derived` 집합과 **정확히 일치**(판독본 §6.2 와도 대조) |
| `drop_decision` | **없다.** `drop_signal.verdict` 가 `go` 이므로 스키마 밖 검사 ①의 요구 대상이 아니다 |

**`target.digest` 의 뜻**: 승인 후 재료가 바뀌면 봉투는 **자동 실효**되고 `freeze` 가 `halt` 한다.
승인은 **이 판**에 걸린 것이지 파일 이름에 걸린 것이 아니다.

## 5. ★ `target.path` 가 판독본이 아니라 기계 정본인 이유 (발주문과의 어긋남 1건)

**발주문은 `target.path` 를 `10-read/material-spec.md` 로 지정했고, 이 봉투는 `…​.json` 을 쓴다.**
값을 총괄이 임의로 바꾼 것이 아니라 **정본이 그 값을 유일하게 결정**하기 때문이며, 그 어긋남을
숨기지 않고 여기 적는다.

**계약이 둘을 갈라 둔다.**

| 개념 | 정본 | 값 |
|---|---|---|
| Owner 가 **읽는 표면** | `contracts/stages/read.yaml#owner_checkpoint.surfaces` | `material-spec.md` · `drop-signal.md` · `positioning.md` · `convergence-early.json` · `convergence.json` **5종** |
| 승인이 **결속하는 대상** | `engine/stages/freeze.py` 검사 ③ (`approval.target-is-material-spec`) | **`10-read/material-spec.json`** 하나 |

**왜 갈라 두는가 — 검사 코드의 주석이 직접 답한다**: *"무엇을 승인했는가(경로)와 그것이 바뀌지
않았는가(해시)는 다른 질문이다. **해시 일치는 대상의 불변만 증명하고 대상의 정체는 증명하지
않는다**(B-02)."* 판독본에 결속하면 **판독본만 고정되고 기계 정본은 자유로워진다** — `freeze` 가
동결하는 것은 `.json` 이므로, 그 구조에서는 승인된 적 없는 재료가 동결될 수 있다. 감수 B-02 가
실측한 결함이 정확히 그것이다.

**★ 이 정정이 Owner 승인의 뜻을 바꾸지 않는다.** `freeze.render-parity` 가 **380항 전건 통과**
했다 — 판독본이 기계 정본의 값을 빠짐없이 싣는다는 것이 기계로 확인되었다. 따라서 Owner 가
`.md` 를 읽고 내린 `통과` 는 **그 `.md` 가 렌더한 `.json` 에 대한 승인과 같은 것**이며, 봉투는 그
사실을 계약이 정한 자리에 적을 뿐이다. **판독본의 지문도 기록으로 남긴다**:
`sha256:4ea28cb626a898c86dd58b2460b810c4c7f67eb80c4e63ee8d98eeb8a2bde48e` — 결속 대상은 아니나 *"Owner 가 실제로 읽은 바이트"* 가 무엇이었는지가 남아야 한다.
