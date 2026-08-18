# 통주 리포트 — `openai-us20260147854a1-cim-fp-2`

**지위.** 재정 **P-9**가 예행 런의 **1급 산출물**로 지정한 문서다 — *"예행의 1급 산출물 = 통주 리포트(단계별 소요·상신 이력·발견 결함·미가동 목록)."* 재료 명세가 "무엇이 나왔는가"를 말한다면 이 문서는 **"어떻게 나왔고 무엇이 아직 돌지 않았는가"**를 말한다.

**이 런이 닫는 것.** M1 잔여 BLOCKER **B-04** — 직전 감수 문언: ***"the real-patent integration smoke was not an execution of the implemented READ contract."*** 이번에는 러너가 끝까지 돌았고, 총괄이 러너 밖에서 손으로 계산한 자리는 없다.

---

## §1 런 제원

| 항목 | 값 |
|---|---|
| 소재 | US20260147854A1 — OpenAI Opco, LLC · *FLOATING POINT MULTIPLICATIONS* |
| 원천 | 293,362 바이트(정본화 4종 적용) · 청구항 **20** · 도면 **64** |
| `run_kind` | `rehearsal` (예행 — 게시하지 않는다) |
| **결박 커밋** | `83490945c222379fe90f94eecd40fb96fefdea93` (재정 P-U1) |
| worktree | `.worktrees/openai-us20260147854a1-cim-fp-2` (그 커밋의 격리 체크아웃) |
| `reader_version` | 0.5.0 |
| 선행 런 | `openai-us20260147854a1-cim-fp` (커밋 `4cdc835`) — **상신으로 종료**(§3) |

**만료 통지(종료 시점 실측).** `tools/run_worktree.py expiry` → **exit 3**:

```
NOTICE: 런 개시 이후 리포가 개정되었다 — 핀 83490945c222 → HEAD fb866aea41cf
        (커밋 1건 · 법 경로 변경 2건). 산출물은 핀 커밋의 법 아래에서 만들어졌다(행위시법).
changed_paths: ["docs/SPEC.md", "reader/schemas/material-spec.schema.json"]
```

두 변경은 **문서·주석뿐**이며 검증 동작을 바꾸지 않는다(SPEC §9.33 ② 재분류 · 스키마 `$comment`의 폐기된 판정 기준 정정). 그러나 **만료는 만료다** — 이 산출물이 어느 법 아래에서 만들어졌는지는 핀이 답한다.

---

## §2 단계별 실행 (재정 P-4 순서)

| # | 단계 | 레인 | 결과 |
|---|---|---|---|
| ① | 진입 지문 검사 | (결정론) | `read.input-digest` **checked=6 pass** |
| ② | 분해 ×2 (독립) | `read-a`·`read-b` decompose | 독립 3 · 종속 17 · element 22 · addition 21 |
| ③ | 맹검 스크리닝 메모 ×2 | 같은 레인 | 둘 다 `clear` · 섀도 원장 1행 |
| ④ | **조기 수렴** | (결정론) | **6축 전부 통과** — `convergence-early.json`(`phase: early`) |
| ⑤ | **정본 지정** | (결정론·내용맹) | `read-a` · `rule: declaration-order` · `content_blind: true` |
| ⑥ | 접지 진입 게이트 | (결정론) | 판정서 통과 → 계속 봉투 불요 |
| ⑦ | 접지 ×2 | `ground-independent`(max) · `ground-dependent`(**low**) | 22 + 21 = 43건 · **접지 예외 0건** |
| ⑧ | **수치 수확** | (결정론) | 34건 수확(`quoted` 30 + `bibliographic` 4) |
| ⑨ | 통합·포지셔닝 | `synthesize` | implication 11 · positioning 3 · figure_note 12 · fact(도면 유래) 1 |
| ⑩ | 조립·검사 전건 | (결정론) | **12행 전건 pass**(§4) |
| ⑪ | CP1 상신물 | (결정론) | 판독본 17절 · 중간 산출물 5종 |

**레인 5개, 전부 정상 배정.** `lane-log.json` 실측:

| 레인 | 실제 모델 | effort | mismatch |
|---|---|---|---|
| `read-a/decompose/batch-0` | `claude-opus-5[1m]` | max | false |
| `read-b/decompose/batch-0` | `claude-opus-5[1m]` | max | false |
| `read-a/ground-independent/batch-0` | `claude-opus-5[1m]` | high | false |
| `read-a/ground-dependent/batch-0` | `opus-5` | **low** | false |
| `read-a/synthesize/batch-0` | `claude-opus-5[1m]` | max | false |

**`read-b`에 접지·통합 레인이 없다** — 재정 P-4의 "접지 이후는 정본 1개"가 로그의 **있음이 아니라 없음**으로 증명되며, `read.lane-log-shape`(checked=5)가 그것을 판정한다.
**`ground-dependent`가 `effort: low`로 돌았다** — 재정 R3의 "관할을 낮춘 것이 아니라 레인을 낮춘 것"이 실물로 집행되었다.
**모델 표기가 두 형태로 섞였는데 mismatch가 0이다** — 계약이 `lane.model_identity`에 라벨 공간을 선언한 결과다(§5 결함 1).

---

## §3 상신 이력

### run 1 — `escalate` · `독해 프로파일 상신` (커밋 `4cdc835`)

조기 수렴에서 해석 축 2개가 임계를 밑돌아 **실패가 아니라 상신**으로 처리되었다(재정 P-3).

| 축 | 정책 | 실측 | 판정 |
|---|---|---|---|
| `independent-count` · `dependent-count` | exact-match | 3=3 · 17=17 | pass |
| `dependent-set` | exact-match **1.0** | 1.0000 | pass |
| `element-set` | escalation-trigger 0.95 | **0.9444** | **escalate** |
| `tree-edges` | escalation-trigger 0.95 | **0.5517** | **escalate** |
| `addition-attachment` | measure-only | 1.0000 | measured |

`convergence_report.divergences`가 갈린 자리를 지목했고 **두 곳뿐이었다** — 순수 연결구를 element로 볼 것인가, 다중 대상 후치 수식절을 어느 층에 놓을 것인가. **두 실행 다 규율을 어기지 않았다**(규약이 답을 갖지 않았다).

**처분** — D6 규율 ③(결정론은 절차 고정에 산다)대로 검사가 아니라 절차를 고쳤다: `10-decompose.md` §2에 **경계 규약 ⑤·⑥ 신설**. 임계·정책·축 목록은 **한 줄도 손대지 않았다**.
그리고 규약 개정은 **법의 개정**이므로 재정 P-U1(행위시법)에 따라 run 1을 이어가지 않고 **새 런을 열었다**.

### run 2 — 상신 0건

| 축 | 실측 |
|---|---|
| 6축 전부 | **1.0000** (`divergences` 0건 · `escalations` 0건) |

**규약이 수렴을 만들었다는 것이 이로써 실측되었다** — 직전 감수가 요구한 바로 그 실증이다(*"No rerun demonstrates that the newly added decomposition boundary rules caused convergence to pass."*).

| 축 | M1 스모크(규약 없음) | run 1(①~④) | **run 2(①~⑥)** |
|---|---|---|---|
| `element-set` | 0.5909 | 0.9444 | **1.0000** |
| `tree-edges` | 0.5714 | 0.5517 | **1.0000** |
| `addition-attachment` | 0.1667 | 1.0000 | **1.0000** |

---

## §4 검사 판정 행 전문 (run 2)

```
  [pass] read.input-digest          checked=6     viol=0 vacuous=none
  [pass] read.schema                checked=1     viol=0 vacuous=none
  [pass] read.source-digest         checked=1     viol=0 vacuous=none
  [pass] read.verbatim              checked=370   viol=0 vacuous=none
  [pass] read.pointer-resolve       checked=428   viol=0 vacuous=none
  [pass] read.coverage              checked=86    viol=0 vacuous=none
  [pass] read.dependency-parse      checked=17    viol=0 vacuous=none
  [pass] read.value-derivation      checked=69    viol=0 vacuous=none
  [pass] read.bibliography          checked=16    viol=0 vacuous=none
  [pass] read.claim-inventory       checked=20    viol=0 vacuous=none
  [pass] read.convergence           checked=6     viol=0 vacuous=none
  [pass] read.lane-log-shape        checked=5     viol=0 vacuous=none
```

**공허 0건.** `checked` 수가 합성 코퍼스의 3~5배다(verbatim 370 vs 81 · 포인터 428 vs 123 · 커버리지 86 vs 24). 통과가 공허하지 않다는 뜻이며, 그 근거를 서식이 스스로 싣는다(재정 N5).

**재료 명세**: items **147**(component 43 · grounding 43 · fact 35 · implication 11 · positioning 3 · figure_note 12) · 도면 12 · `extensions.docent.drop_signal: go`.

---

## §5 발견한 결함 — 문서 검토로는 나오지 않았을 것들

**일곱 중 넷은 레인이 규칙을 지키려다 막혀서** 드러났다.

| # | 결함 | 처분 |
|---|---|---|
| 1 | **조용한 대체 검사가 거짓 경보를 냈다** — 계약은 티어 라벨(`opus-5`), 레인은 API 식별자(`claude-opus-5[1m]`). 문자열 동등 대조라 같은 모델이 대체로 잡혔고 **정직한 레인이 자기 관측을 고쳐 적어야 했다** | 라벨 공간을 계약이 선언(`read.yaml#lane.model_identity`), 코드는 읽기만. 계약이 침묵하면 구 동작으로 회귀 |
| 2 | **`effort` 자기 신고는 관측이 아니라 반향이다** — 레인은 자기 reasoning effort를 내성할 수 없다 | 계약 `lane.effort_evidence`에 증거 등급을 명기. 실증은 transcript 실호출 확인 |
| 3 | **러너가 커밋 핀을 쓰지 않았다** — `engine.commit`이 빈 문자열이라 총괄이 손으로 넣었다. **손으로 넣는 결박은 결박이 아니다** | `engine/gitpin.py`(판정 단일 진원) + 러너가 스스로 기입 + 더러운 트리 = 런 개시 불가 |
| 4 | **진입 지문 검사가 승인 봉투 실효를 삼켰다** — 환경 오류(세계가 어긋남)와 봉투 실효(재승인 필요)는 성질이 다른데 전자가 후자를 먹어 `approval.target-digest`가 도달 불능이 되었다 | 봉투 결속을 출구 관할로 복귀 |
| 5 | **SPEC §2.7 예시가 경계 규약과 반대로 분해되어 있었다** — 끝 구분자 포함 · 후치 수식절 평탄화. `10-decompose.md` §3 예시도 같은 위반 | 예시 재분해 + "규약이 개정되면 예시도 함께" 경고. **두 독해 레인이 독립적으로 지적** |
| 6 | **테스트 스위트가 생산 섀도 원장을 오염시켰다** — 합성 픽스처 메모 **1,178행** | 경로 주입 + 회귀 테스트 |
| 7 | `source.figures-manifest`가 입력 디렉터리의 **비-도면 파일 2건**을 거부 | 입력 정리 후 재실행(검사가 옳았다) |

### ★ 그리고 닫지 못한 것 하나 — 수확 정답지가 이 특허에서 노이즈다

접지 레인이 **자기 인용에 수확기를 직접 돌려** 실측했다. 수확 34건 중 **진짜 공학량이 사실상 없다.**

| 유형 | 실례 |
|---|---|
| FP 포맷 3항 표기 `(1-5-2)` → `range 1–5` 오인 | `1-5`·`1-4`·`1-3`·`1-2`·`1-1` |
| 비트 슬라이스 `<6:3>` → `inequality`+scalar 오인 | `<6`·`3` |
| 도면·표 **번호**(부호가 아니다) | `60`(FIG. 60) · `2`(Table 2) · `1`(in FIG. 1) |
| 첨자·인덱스 | `C.sub.j−1` → 1 · `Act 0` → 0 |

**원인은 토큰 경계다.** `(1-5-2)`의 앵커 파싱은 실패하지만 **스캔이 그 안의 `1-5`를 부분 매칭**한다. `cm3`의 `3`을 잡던 것과 **같은 형태의 결함**이며, 그때는 알파벳 이웃만 막았고 숫자·구두점 이웃은 남았다. 도면 **번호**는 도면 **부호** 배제 규칙(`figures[].numerals` 소속)으로는 원리적으로 막히지 않는다.

**귀결.** CP1 §12가 `전체 34건 — 참조 3건 표시, 미참조 31건 접힘`으로 정직하게 표시하고, `numeric_refs`는 근거가 실재하는 3건만 채워졌다. 그러나 이대로 M4가 오면 `numeric.exhaustive`의 정답지가 노이즈로 채워진다. **이 런은 그 사실을 실측으로 남기는 데까지 갔고, 고치지는 않았다** — 고치면 법이 바뀌고 이 런은 다시 무효가 되기 때문이다(P-U1).

---

## §6 미가동 게이트 목록 (재정 P-9 · N5 규율)

**예행 판정문은 무엇이 돌지 않았는지를 반드시 적는다.** 돌지 않은 게이트를 적지 않으면 "통과"가 실제보다 넓게 읽힌다.

| 스테이지 | 상태 | 소관 |
|---|---|---|
| CP1 `material_approval` | **Owner 대기** — 상신물은 완비되었고 봉투는 작업 레인이 쓸 수 없다(C3) | Owner |
| `freeze` | 미가동 — CP1 봉투 없이는 진입하지 않는다 | CP1 승인 후 |
| `design` · `figures` · `compose` | **미구현** | M5 · M9 |
| `gate` L0/L1/L2 · `gate.final-eyes` | **미구현** — `numeric.exhaustive`·`citation.resolve`·`format.*`·`numeric.unreviewed-use` 전부 | M4 · M6 |
| `probe` · `critique` | **미구현** | M7 · M8 |
| CP2 `ship_approval` · `ship` · `feedback` | **미구현** | M10 |
| `run.publish-preconditions` | **미구현** — 게시 자격의 기계 좌표는 방어층 발주의 필수 산출물로 **예약**(처분 ⓒ) | M4 + 재정 |

**따라서 재정 P-9가 정한 예행 종료선(strip 산출까지)에는 도달하지 못했다.** 이 런이 도달한 곳은 **CP1 상신**이며, 그 앞의 `read` 구간만이 구현되어 있다. 예행 종료선은 M3~M10이 서야 열린다.

---

## §7 소요

레인 5개는 오케스트레이터가 서브에이전트로 붙였고 러너는 `LanePending`으로 즉시 반환한다(블로킹 없음). 벽시계 기준 레인 1건당 9~17분, 접지 2레인이 가장 길었다(요청서 316KB — 명세서 문단 전량이 슬라이스에 들어간다).

**결정론 구간**(진입 지문 · 조기 수렴 · 정본 지정 · 수확 · 조립 · 검사 12종 · 판독본 렌더)은 전부 합쳐 **수 초**다. 비용은 전적으로 레인에 있다.

---

## §8 이 런이 증명한 것과 증명하지 **않은** 것

| 증명한 것 | 증명하지 않은 것 |
|---|---|
| 구현된 스테이지 시퀀스가 실특허에서 **끝까지 돈다** | 재료 명세가 **좋은지** — 그 판단은 CP1의 Owner 몫이다(D6) |
| `escalate` 경로가 **실제로 발동**한다(run 1) | `retry(1)` 경로 — run 1·2 모두 재시도 없이 결론에 도달했다 |
| 경계 규약이 **수렴을 만든다**(0.59 → 0.94 → 1.00) | 다른 특허에서도 그러한지 |
| 접지 3중이 실물에서 **예외 0건**으로 선다 | 인용한 문단이 그 구성요소를 **실제로 조응하는지**(어떤 결정론 검사도 판정하지 못한다) |
| 전수 수확이 **작동**한다 | 수확 결과가 **쓸모 있는지** — 이 특허에서는 아니었다(§5) |
| 커밋 결박·만료 통지가 **실물로 돈다** | 재개 런이 같은 커밋을 쓰는지(재개를 시험하지 않았다) |
