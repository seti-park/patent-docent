# 통주 리포트 — `openai-us20260147854a1-cim-fp-3`

**지위.** 재정 **P-9**가 예행 런의 **1급 산출물**로 지정한 문서다 — *"예행의 1급 산출물 = 통주 리포트(단계별 소요·상신 이력·발견 결함·미가동 목록)."* 재료 명세가 "무엇이 나왔는가"를 말한다면 이 문서는 **"어떻게 나왔고 무엇이 아직 돌지 않았는가"**를 말한다.

**이 런이 닫는 것.** 재정 **P-13** — *"'854의 정식 CP1은 **보수 후 재생성 상신물**에 한다(현행 상신물 승인 기각 — 알려진 정답지 오염판 승인·재승인 이중 노동 회피)."* 통주 2의 상신물은 `origin: quoted` 30건 중 **23건이 오파싱 아티팩트**임이 그 런 자신에 의해 실측된 판이었다. 이 런은 그 오염을 걷은 정답지 위에서 CP1을 다시 세운다.

---

## §1 런 제원

| 항목 | 값 |
|---|---|
| 소재 | US20260147854A1 — OpenAI Opco, LLC · *FLOATING POINT MULTIPLICATIONS* |
| 원천 | 293,362 바이트(정본화 4종) · 청구항 **20** · 도면 **64** — **통주 2와 바이트 동일**(정본 sha256 `40f1905b…`, 도면 세트 지문 사전 대조) |
| `run_kind` | `rehearsal`(예행 — 게시하지 않는다) |
| **결박 커밋** | `f0b4ca15b2129a1fe191f53d2e834de7b55c3039` (러너가 스스로 기입 — 재정 P-U1) |
| worktree | `.worktrees/openai-us20260147854a1-cim-fp-3` |
| `reader_version` | **0.6.0**(이 라운드 상향 — 검사 판정 기준 강화) |
| 선행 런 | `…-cim-fp`(상신 종료) · `…-cim-fp-2`(완주, 정답지 오염판) |

**만료 통지(종료 시점 실측).** `tools/run_worktree.py expiry` → **exit 3**:

```
NOTICE: 런 개시 이후 리포가 개정되었다 — 핀 f0b4ca15b212 → HEAD ad74c1335e40
        (커밋 9건 · 법 경로 변경 3건). 산출물은 핀 커밋의 법 아래에서 만들어졌다(행위시법).
changed_paths: ["contracts/glossary.md", "contracts/schemas/convergence.schema.json", "docs/SPEC.md"]
```

세 변경은 **문서·주석뿐**이며 검증 동작을 바꾸지 않는다(수확 배제의 서술 반영). 그러나 **만료는 만료다** — 이 산출물이 어느 법 아래에서 만들어졌는지는 핀이 답한다.

---

## §2 단계별 실행 (재정 P-4 순서)

| # | 단계 | 레인 | 결과 |
|---|---|---|---|
| ① | 진입 지문 검사 | (결정론) | `read.input-digest` **checked=6 pass** |
| ② | 분해 ×2 (독립) | `read-a`·`read-b` decompose | 독립 3 · 종속 17 · element 22 · addition 21 |
| ③ | 맹검 스크리닝 메모 ×2 | 같은 레인 | 둘 다 `clear` |
| ④ | **조기 수렴 (1회차)** | (결정론) | **`dependent-set` fail — jaccard 0.8889** (§3) |
| ④′ | **재분해 ×2** | 같은 레인, `retry-1` | 결함 되먹임 → **수렴** |
| ④″ | **조기 수렴 (2회차)** | (결정론) | **6축 전부 통과** |
| ⑤ | 정본 지정 | (결정론·내용맹) | `read-a` · `rule: declaration-order` · `content_blind: true` |
| ⑥ | 접지 진입 게이트 | (결정론) | 판정서 통과 → 계속 봉투 불요 |
| ⑦ | 접지 ×2 | `ground-independent`(high) · `ground-dependent`(**low**) | 22 + 21 = 43건 · **접지 예외 0건** |
| ⑧ | **수치 수확** | (결정론) | **17건**(`quoted` 13 + `bibliographic` 4) · 배제 **89구간** |
| ⑨ | 통합·포지셔닝 | `synthesize` | implication 8 · positioning 4 · figure_note 8 · derived 3 · figure-sourced 3 |
| ⑩ | 조립·검사 전건 | (결정론) | **12행 전건 pass**(§4) |
| ⑪ | CP1 상신물 | (결정론) | 판독본 17절 · 중간 산출물 5종 |

**레인 7개 왕복.** `lane-log.json` 실측 — **전건 `digest_ok: true`**:

| 레인 | 실제 모델 | effort | mismatch | digest_ok |
|---|---|---|---|---|
| `read-a/decompose/batch-0` | `claude-opus-5[1m]` | max | false | **true** |
| `read-b/decompose/batch-0` | `claude-opus-5[1m]` | max | false | **true** |
| `read-a/decompose/retry-1/batch-0` | `claude-opus-5[1m]` | max | false | **true** |
| `read-b/decompose/retry-1/batch-0` | `claude-opus-5[1m]` | max | false | **true** |
| `read-a/ground-independent/retry-1/batch-0` | `claude-opus-5[1m]` | high | false | **true** |
| `read-a/ground-dependent/retry-1/batch-0` | `claude-opus-5[1m]` | **low** | false | **true** |
| `read-a/synthesize/retry-1/batch-0` | `claude-opus-5[1m]` | max | false | **true** |

**`read-b`에 접지·통합 레인이 없다** — 재정 P-4의 "접지 이후는 정본 1개"가 로그의 **없음**으로 증명되며 `read.lane-log-shape`(checked=7)가 그것을 판정한다.
**모델 신원이 정직하게 기록되었다** — 일곱 레인 전부 API 식별자를 그대로 적었고 계약의 별칭 표(`read.yaml#lane.model_identity`)가 티어 라벨로 정규화했다. **통주 2에서 정직한 레인이 벌받던 자리가 닫혔다.**

---

## §3 ★ 이 런이 처음으로 증명한 것 — `exact-match` 축이 발동하고 재시도가 완결됐다

직전 통주 리포트는 `retry(1)` 경로를 **"증명하지 않은 것"** 표에 올렸다 — *"run 1·2 모두 재시도 없이 결론에 도달했다."* 이번에 그 경로가 실특허에서 끝까지 돌았다.

| 축 | 정책 | 1회차 | **2회차** |
|---|---|---|---|
| `independent-count` | exact-match | 3 = 3 | 3 = 3 |
| `dependent-count` | exact-match | 17 = 17 | 17 = 17 |
| **`dependent-set`** | **exact-match 1.0** | **0.8889 → fail** | **1.0000** |
| `element-set` | escalation-trigger 0.95 | 1.0000 | 1.0000 |
| `tree-edges` | escalation-trigger 0.95 | 1.0000 | 1.0000 |
| `addition-attachment` | measure-only | — | 0.75 (판정 제외) |

**갈린 자리는 CL-9 하나였다.**

| 실행 | 1회차 CL-9 | 2회차 CL-9 |
|---|---|---|
| `read-a` | `single` | **`unclassified`** |
| `read-b` | `unclassified` | `unclassified`(변경 없음) |

CL-9 본문은 `… concurrently update the second bit **when** the first bitcell is providing …` 이고 `\bwhen\b`는 `structure_markers`의 조건부 표지에 **실재한다**. 그러므로 **두 실행 다 규율을 어기지 않았다** — 하나는 표지의 실재를 따랐고 하나는 그 `when`이 조건부 종속이 아니라 **동시성 한정**임을 읽었다. 두 레인이 각자 독립적으로 이 자리를 미결로 상신하기까지 했다.

**재시도가 고친 범위는 정확히 한 자리다.** `read-a`의 보고: *"CL-9의 `dependency_type`을 `single` → `unclassified`로 고쳤다. … 그 밖의 모든 값은 **한 바이트도 바꾸지 않았다.** 결함 보고가 지목한 축은 `dependent-set` 하나뿐이고, 수렴한 축을 건드리면 그쪽을 새로 깨뜨린다."* `read-b`의 재시도는 payload가 자기 직전 판과 **완전히 동일**했다.

**★ 그리고 바꾼 근거가 이 라운드에서 정정한 문언이었다.** `read-a`: *"직전 판은 본문에 `when`이 실재하는데도 인용부가 평범한 `according to claim 8`이라는 이유로 `single`로 적었고, **그것이 규칙 우회다**."* 이 라운드가 SPEC·계약 6곳에서 정정한 판정 기준(인용 어형의 파싱 가능성 → **본문의 구조 표지 유무**)을 레인이 읽고 스스로 바로잡았다 — **문언 정정이 실런의 행동을 바꾼 것이 실측으로 확인된 자리다.**

**이 사건은 감수 OOS-10(`\bwhen\b` 과대 탐지 · MINOR)을 가설에서 실측으로 올린다.** 직전 라운드는 *"두 실행이 갈릴 수 있다"*는 관찰로 적었다. 이제 갈렸다. **등급은 MINOR가 아니다 — `exact-match` 축을 넘어뜨리는 자리다.**

---

## §4 검사 전건 — 12행 pass

```
  [pass] read.input-digest          checked=6     viol=0 vacuous=none
  [pass] read.schema                checked=1     viol=0 vacuous=none
  [pass] read.source-digest         checked=1     viol=0 vacuous=none
  [pass] read.verbatim              checked=286   viol=0 vacuous=none
  [pass] read.pointer-resolve       checked=424   viol=0 vacuous=none
  [pass] read.coverage              checked=86    viol=0 vacuous=none
  [pass] read.dependency-parse      checked=16    viol=0 vacuous=none
  [pass] read.value-derivation      checked=40    viol=0 vacuous=none
  [pass] read.bibliography          checked=24    viol=0 vacuous=none
  [pass] read.claim-inventory       checked=20    viol=0 vacuous=none
  [pass] read.convergence           checked=6     viol=0 vacuous=none
  [pass] read.lane-log-shape        checked=7     viol=0 vacuous=none
```

**통주 2와 갈린 `checked` 수가 그 자체로 이 라운드의 개정 내역이다.**

| 검사 | 통주 2 | 통주 3 | 왜 갈렸나 |
|---|---:|---:|---|
| `read.dependency-parse` | 17 | **16** | CL-9가 `unclassified`가 되어 판정 대상에서 빠졌다 — **재정 P-1의 기제가 실물에서 처음 작동했다** |
| `read.value-derivation` | 69 | **40** | 수확 정답지가 34 → 17로 정제되었다 |
| `read.bibliography` | 16 | **24** | 우선권 근접 대조 2종(관할·연도)이 주장 4건마다 더해졌다 |
| `read.lane-log-shape` | 5 | **7** | 재분해 2회가 왕복에 더해졌다 |
| `read.verbatim` | 370 | 286 | 접지 레인이 다른 스팬을 골랐다(같은 특허라도 접지는 재현 대상이 아니다) |

| 산출 | 값 |
|---|---|
| `items` | **129** — component 43 · grounding 43 · fact 23 · implication 8 · positioning 4 · figure_note 8 |
| `fact` origin | **quoted 13 · bibliographic 4 · derived 3 · figure-sourced 3** |
| 청구항 | 독립 3 · 종속 17(전 20건 등재) · **`unclassified` 1건(CL-9)** |
| 도면 | 8 등재 · **접지 예외 0건** |
| `numeric_refs` | **6 항목 · 16 참조 · 12 대상**(통주 2: 5 · 8 · 4) |
| `extensions.docent.drop_signal` | `go` |
| CP1 판독본 | **17절** — §10 미분류 1건 · §11 맹검 메모 2건 병기 · §12 수치 인벤토리 · §13 독해 프로파일 |

---

## §5 ★ 수확 정답지가 정제되었다 — 34 → 17

**이것이 재정 P-13이 요구한 것의 실질이다.**

| | 통주 2(구 수확기) | **통주 3(신 수확기)** |
|---|---:|---:|
| `quoted` | 30 (**진짜 7 + 아티팩트 23**) | **13** |
| `bibliographic` | 4 | 4 |
| 계 | **34** | **17** |
| 배제·기각의 기록 | 도면부호만 | **89구간, 7사유** |

배제 소계(구간 기준): `figure-numeral` 34 · `boundary-left` 30 · `coordinate-triple` 9 · `figure-or-table-number` 7 · `boundary-right` 4 · `bit-slice` 3 · `subscript-index` 2.

**배제가 진짜를 먹지 않았다는 것이 한 문장에서 함께 보인다.** [0189]의 원문 — *"the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2"* — 에서 `220`은 도면부호로 정확히 배제되었고 `60`은 **진짜 공학량으로 살아남았다**. 통주 2의 수확기는 이 자리에서 `FIG. 60`의 `60`을 수치로 읽었다.

**역참조의 밀도가 세 배로 올랐다**(4 대상 → 12 대상). 정답지가 깨끗해지자 통합 레인이 근거로 삼을 수치를 실제로 찾아 썼다 — 재정 P-B의 *"고르는 일은 역참조가 한다"*가 노이즈 없는 조건에서 어떻게 달라지는지의 실측이다.

### §5.1 ★ 그러나 아티팩트가 전부 사라지지는 않았다 — 잔여 3건

**숨기지 않고 적는다.** `quoted` 13건 중 셋은 여전히 좌표류다.

| 항목 | 값 | 원천 문맥 | 성질 |
|---|---|---|---|
| `M87` | `2` | *"beyond those listed in **Tables 1 and 2**."* | 표 번호. 봉투 `figure-or-table-number`가 `Tables 1`은 잡지만 **뒤따르는 `and 2`는 잡지 못한다** |
| `M88`·`M89` | `0`·`0` | *"e.g., in **Row 0 and Col 0** of the CIM macro"* | 격자 좌표. 네 배제 계열 어디에도 속하지 않는 **새 계열**이다 |

**즉 오염률은 23/30(77%)에서 3/13(23%)으로 내려갔으나 0은 아니다.** 두 계열 다 처방이 보이지만(열거형 표 번호의 뒤 항 · `Row/Col N` 좌표) **어형 추가는 배제 규칙의 확장**이므로 `[가설]` 태그와 실물 근거를 갖춰 다음 라운드의 재료로 남긴다. 이번에 넓히지 않은 이유는 실물이 이 한 건뿐이기 때문이다 — 표본 하나로 규칙을 넓히면 그것이 이 리포가 경계해 온 과적합이다.

---

## §6 ★ 섀도 원장이 처음으로 리포에 도착했다

통주 2의 실측(총괄 적발 D-1): worktree 안 **4행** / 리포 **0행**. 원장이 `.gitignore` 대상인 소모품 안에 서서, 재정 P-U4가 부여한 목적(historian 스크리닝의 사전 훈련 데이터, 헌장 D4)이 **한 행도 달성되지 않았다.**

이 런의 실측:

```
$ wc -l ledgers/shadow/screening.jsonl        (본 리포)
1

$ cat runs/…/10-read/lanes/shadow-ledger.json
{"appended": true, "root_source": "main-worktree-resolved",
 "root": "/home/laptop/projects/patent-docent",
 "run_repo": "…/.worktrees/openai-us20260147854a1-cim-fp-3",
 "memo_count": 2, "terminated": true}
```

**런당 정확히 1행**(메모 2건 · `final_verdict: go` · `owner_decision: null` — Owner 재정은 CP1에서 내려온다). 그리고 러너가 **어느 원장에 왜 그 자리에 썼는지**를 런 안에 남긴다(`root_source: main-worktree-resolved` = "여기는 worktree라 주 작업 트리로 옮겼다"). 판정은 `engine/gitpin.py` 단일 진원을 거친다.

**소급 이관은 하지 않았다** — 통주 2의 4행은 구 커밋의 법 아래 있고 그 4행 자체가 감수가 지적한 결함의 산물이다.

---

## §7 상신 이력과 발견 결함

### §7.1 상신 이력

| # | 시점 | 내용 | 처분 |
|---|---|---|---|
| 1 | 분해 ×2 직후 | `dependent-set` 0.8889 — **기계 상신** | 재시도 1회 → 수렴(§3) |
| 2 | 분해 레인 4건 전부 | **Markush 실물 어형 미도달**(CL-10·11·19) | **Owner 재정 대기** — 레인이 넓힐 수 없다 |
| 3 | 분해 레인 | 전제부 element 여부 · addition 층위 부재 · 부착 원리의 층간 불일치 | 규약 공백 — 다음 라운드 재료 |
| 4 | 접지 레인 | **명세서와 청구항의 멀티플렉서 번호가 뒤바뀌어 있다** | 원천 자체의 불일치. 레인이 **기능 조응**을 골라 `search_note`에 기록 |
| 5 | 접지 레인 | **레인 id가 `retry-1`인데 첫 시도다** | `attempt`가 런 전역 카운터 — 로그가 사실 아닌 것을 말한다 |

### §7.2 이 런이 잡은 것 — 문서 검토로는 나오지 않았을 것들

| # | 결함 | 어떻게 드러났나 |
|---|---|---|
| 1 | **`\bwhen\b` 과대 탐지가 `exact-match` 축을 넘어뜨린다** | 두 독립 실행이 CL-9에서 갈렸다 — 가설이던 OOS-10이 실측이 되었다 |
| 2 | **레인 id의 `retry-N` 오귀속** | 접지 레인이 자기 좌표를 보고 *"첫 시도인데 재시도로 적힌다"*고 상신 |
| 3 | **잔여 아티팩트 2계열**(`Tables 1 and 2`의 뒤 항 · `Row 0 and Col 0`) | 총괄이 CP1 §12의 미참조 목록을 실물로 열어 확인(§5.1) |
| 4 | **단위 어휘에 `b`(bits)가 없다** | 경계 기각을 세기 시작하자 `boundary-right` 4건이 전부 `5b, 4b, 3b or 2b`임이 드러났다 — **진짜 수치 넷이 지금까지 무기록으로 사라지고 있었다** |
| 5 | **원천 자체의 부호 불일치**(mux 2860/2862) | 접지 레인이 이름 조응과 기능 조응이 갈리는 것을 발견 |

**적발 경로의 성질.** 1은 **기계가** 잡았고(그것이 `exact-match` 축의 존재 이유다), 2·5는 **레인의 눈**이, 3·4는 **이 라운드가 새로 만든 기록면**이 잡았다. 4가 특히 값지다 — **배제 규칙을 세우려던 개정이 배제가 아니라 누락을 먼저 드러냈다.** 보이지 않던 손실이 보이게 된 것 자체가 기록화의 값이다.

### §7.3 총괄 자신의 오류 1건

총괄이 재시도 레인 브리핑에 *"서명은 `depends_on`과 `dependency_type`으로 이루어진다"*고 적었으나, 실구현(`reader/lib/convergence.py#_dependent_signatures`)의 서명은 **`(text_verbatim, sorted(depends_on), dependency_type)` 3튜플**이다. 레인이 실물을 열어 확인하고 *"실물이 정본이므로 3튜플 전부를 재유도해 검증했고, 발주문 서술과의 불일치를 여기 명기한다"*고 되돌려 보냈다.

**이 라운드가 벌한 형태 그대로가 총괄에게서 나왔다** — 코드를 열지 않고 기억으로 쓴 명세는 낡은 명세다. 결과는 옳았으나 그것은 레인이 실물을 정본으로 삼았기 때문이지 브리핑이 옳아서가 아니다.

---

## §8 미가동 게이트 목록 (재정 P-9 · N5 규율)

**예행 판정문은 무엇이 돌지 않았는지를 반드시 적는다.** 돌지 않은 게이트를 적지 않으면 "통과"가 실제보다 넓게 읽힌다.

| 스테이지 | 상태 | 소관 |
|---|---|---|
| CP1 `material_approval` | **Owner 대기** — 상신물 완비, 봉투는 작업 레인이 쓸 수 없다(C3) | Owner |
| `freeze` | 미가동 — CP1 봉투 없이는 진입하지 않는다 | CP1 승인 후 |
| `design` · `figures` · `compose` | **미구현** | M5 · M9 |
| `gate` L0/L1/L2 · `gate.final-eyes` | **미구현** — `numeric.exhaustive`·`citation.*`·`format.*`·**`numeric.unreviewed-use`** 전부 | M4 · M6 |
| `probe` · `critique` | **미구현** — 정족수 **판정 층**(`engine/quorum.py`)은 이 라운드에 섰으나 계기를 띄우고 응답을 거두는 **수집 경로는 없다** | M7 · M8 |
| CP2 `ship_approval` · `ship` · `feedback` | **미구현** | M10 |
| `run.publish-preconditions` | **미구현** — 게시 자격의 기계 좌표는 방어층 발주의 필수 산출물로 **예약**(처분 ⓒ) | M4 + 재정 |

**따라서 재정 P-9가 정한 예행 종료선(strip 산출까지)에는 도달하지 못했다.** 이 런이 도달한 곳은 **CP1 상신**이다. **다만 그 미도달은 M1의 미이행이 아니다** — 재정 **P-15**가 예행 종료선을 M1 요구사항표에서 제거하고 예행 런의 정의로 이관했다(`contracts/run-kinds.yaml`). strip 도달은 M3~M10이 서야 열린다.

---

## §9 소요

레인 7건은 오케스트레이터가 서브에이전트로 붙였고 러너는 `LanePending`으로 즉시 반환한다(블로킹 없음). 분해 레인은 요청서 28KB로 6~40분, **접지 2레인이 가장 길었다**(요청서 각 **316KB** — 명세서 문단 전량이 슬라이스에 들어간다). 통합은 접지 산출 전량 + 수확표를 함께 받아 그보다 크다.

**결정론 구간**(진입 지문 · 조기 수렴 ×2 · 정본 지정 · 수확 · 조립 · 검사 12종 · 판독본 렌더)은 전부 합쳐 **수 초**다. 비용은 전적으로 레인에 있다.

**재시도의 비용이 이번에 처음 측정되었다** — 분해 왕복이 2회에서 4회로 늘었고, 그것이 `dependent-set` 한 축을 1.0으로 올리기 위해 치른 값이다.

---

## §10 이 런이 증명한 것과 증명하지 **않은** 것

| 증명한 것 | 증명하지 않은 것 |
|---|---|
| **P-12 왕복 지문이 실런에서 돈다** — 7왕복 전건 `digest_ok`, 모델 신원 정직 기록 | 낡은 응답이 **실제로** 주입되었을 때의 거부(도구가 증명하나 실런에서는 발생하지 않았다) |
| **`exact-match` 축이 발동하고 재시도가 수렴시킨다**(0.8889 → 1.0) | 재시도가 **언제나** 수렴시키는지 — 이번은 한 축·한 항목이었다 |
| **수확 정제가 실특허에서 34 → 17**, 배제가 진짜를 먹지 않음 | 정답지가 **깨끗한지** — 잔여 아티팩트 3건이 남았다(§5.1) |
| **섀도 원장이 리포에 도착한다**(1행 · 판정 사유 기록) | 축적물로서의 값 — 표본이 1건이다 |
| 서지 근접 대조 2종이 실특허에서 통과 | 다른 관할·다른 표기 형식의 서지면에서도 그러한지(`[가설]`) |
| 접지 3중이 실물에서 **예외 0건**으로 선다 | 인용한 문단이 그 구성요소를 **실제로 조응하는지**(어떤 결정론 검사도 판정하지 못한다 — CP1의 Owner 몫) |
| `low` 레인이 같은 정확성을 낸다(재정 R3, 2회째) | 다른 특허에서도 그러한지 |

---

## §11 ★ 이 상신물의 유효성은 재정 하나에 달렸다

**Markush 실물 어형(Q1)이 `ⓐ 승인`으로 재정되면 `reader/reader-rules.yaml`이 바뀌고, 그것은 법의 개정이므로 이 런은 무효가 된다**(행위시법 — 재정 P-U1). CL-10·11·19가 `unclassified`로 서면 `read.dependency-parse`의 `checked`가 16 → 13으로 줄고 CP1 §10 미분류 목록이 1건 → 4건이 된다.

**`ⓑ 기각`이면 이 런이 그대로 선다.**

재정 P-13이 이 라운드의 종결 요건으로 재실행을 명시했으므로 총괄이 순서를 미루지 않았다. **다만 Q1을 먼저 받는 편이 쌌을 수 있다**는 사실을 기록한다 — 판단은 Owner의 것이다. 상신 원문 = `docs/decisions/D-20260819-01-m16-close.md` §6.
