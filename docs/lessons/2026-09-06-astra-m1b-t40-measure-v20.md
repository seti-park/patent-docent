# 독립 감수 원문 — M1b 설계 도전 20차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v21 · 판정 REVISE(HIGH 2 · MED 3 · LOW 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `44875da3dde32638d8071da5f2b1b2b0061548391e5662daf7329d423426375c` · 23075 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v20b/`(첫 기동 `astra-m1b-t40v20/` 은 Codex 주간 한도로 판정 없이 무산 · 재정 T41 ① B 크레딧 구매 뒤 재기동 · 회차 번호는 판정 있는 도전만 셈).

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(함정 O). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `813622e` · 메모 v21 sha256 `a11df3b2…` · v1~v20 + 외부 자문 봉투·회신 + 회귀표 v1 동봉). **발주문에 처음으로 ⑽ ⓑ 트리거 계수 조항(L-055)을 넣었고 도전자가 첫 줄에 「발동(컴포넌트 D · 연속 REVISE 20회)」을 명기했다.** 폐쇄 = **이전 65건 closed 59 · partially 6 · open 0**. **B·C·E·F PASS**(15회 연속).

**판정 = REVISE · 6건(HIGH 2 · MED 3 · LOW 1) · 기각 0 · 발주자 귀책.** **NR-1 HIGH**: v21 이 새로 넣은 `E.attempt ≤ full.attempt` 가 합법 완료(조기 수렴 재시도 뒤 통과 · 출구 재시도 없음 = E 2 · full 1)를 손상으로 거부 — 조기·출구 회차는 독립 계수. **NR-2 MED**: 회귀표 v1 의 합법 부모(L09·L10·L11·L12·L02·L13)가 러너 실제 경로와 다름(거부·불일치 행은 full 전 예외 종결 · `record(req,None)` 은 FileLaneAdapter 미도달 · 5행 전건 pass 는 생성 불가 · 통합 대기에 통합 소비 행 잔존) + 조기 생성 불변식(청구항 실패 ↔ 수렴 미실행 · 스냅샷 있는데 현재 E 없음) 누락. **NR-3 HIGH**: 요청 JSON 의 좌석을 검증하지만 그 JSON 이 요청 MD 를 생성했는지는 대조하지 않음 — R1 런에 MD effort=max · JSON/프로필/로그/응답 xhigh 를 공급하자 정상 지표로 수용. **NR-4 MED**: 포인터 memo_count(2→999)를 원장 memos·판정서 screening_memos 와 대조하지 않음. **NR-5 MED**: 스냅샷 부재 처분이 메모 §2(0·11·12·13 인데 부재 → N/A)와 §5·코드(full·수렴 실행 E 있으면 exit 4)에서 다름. **NR-6 LOW**: 사본 `.audit-sandbox` order 가 v20 으로 남음(총괄 sed 가 order 를 안 갈음 · 18차 pin 사고와 같은 뿌리).

지적 열거 = NR-1, NR-2, NR-3, NR-4, NR-5, NR-6

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 20**. **전부 수용 → 지표 v22 + 회귀표 v2**(대소관계 제거 · 조기 판정서 청구항↔수렴 맞물림 · 거부·불일치·짝 없음 행은 예외 종결 런에만 · 요청 JSON → LaneRequest → render_request_md 바이트 == 저장 MD ∧ 계산 지문 == 저장 지문 · memo_count 대조 · `--law-tree`(기준 런은 절차 문서 09-01 판 트리로 재렌더) · 회귀표 L 행을 러너 실제 경로로 재제조 + C32~C40 · 55 사례 PASS) · 메모 §2·§5 통일 · order 갱신 → **M1b 21차 도전(지적 `NS-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 20회)

외부 자문은 **회신·반영 단계**이며 대기 중이 아닙니다. 계수는 지표 컴포넌트 기준으로 이어집니다. 1차에서 E로 분류했던 지표 지적도 같은 부류로 세었고, 외부 자문을 별도 도전 회차로 더하지 않았습니다.

**합법적인 조기 재시도 후 완료를 v21이 거부합니다.** 반대로 요청 MD의 좌석 지시와 JSON·계약 프로필이 다른 자료는 정상 지표로 수용합니다. 회귀표 44건의 출력은 재현됐지만, 일부 “합법 상태”의 생성 근거가 틀렸습니다.

**A — 원장 정합·MY~NQ 폐쇄: REVISE**

앞선 **65건 중 closed 59 · partially 6 · open 0**입니다. `partially`는 지정 반례는 막혔지만 원 지적이 요구한 증거 결속·상태 구별에 잔여가 있다는 뜻입니다.

| 회차 | closed | partially | 잔여 |
|---|---|---|---|
| MY | MY-1~13 | — | — |
| MZ | MZ-1·3~9 | MZ-2 | 스냅샷 결측 처분의 문서 충돌: NR-5 |
| NA | NA-1~7 | — | — |
| NB | NB-1~3 | — | — |
| NC | NC-1~3 | — | — |
| ND | ND-1~2 | — | 단일 읽기 회귀 없음 |
| NE | NE-1~2 | — | — |
| NF | NF-1 | — | — |
| NG | NG-1~2 | — | — |
| NH | NH-2 | NH-1 | 왕복 자료의 요청 메타 결속: NR-3 |
| NI | NI-2 | NI-1 | MD와 JSON을 잇는 검증 잔여: NR-3 |
| NJ | NJ-1 | — | — |
| NK | NK-1 | — | — |
| NL | NL-1 | — | — |
| NM | NM-1~2 | — | — |
| NN | NN-1·2·4 | NN-3 | 합법 완료 오거부: NR-1 |
| NO | NO-1·3 | NO-2·4 | 생성 불가능 상태·포인터 정합: NR-2·4 |
| NP | NP-1~3 | — | 지정 반례 차단 확인 |
| NQ | NQ-1~3 | — | 실제 거부·원장 단독 종결·소견 삭제 재시험으로 확인 |

§8의 격 구분은 유지할 수 있습니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이고, 인덱스·후보 제시·런 표시는 재량입니다. 아래 결함은 이 구분을 바꾸는 새 입법 요구가 아닙니다.

**지적 목록 — HIGH 2 · MED 3 · LOW 1**

**NR-1 · HIGH — 서로 독립인 조기·출구 회차에 대소관계를 강제한다.**

좌표: 메모 §5 생성 불변식, [지표:359](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:359); `read.run`의 `early_convergence_attempt`·`tail_attempt`.

러너는 조기 비교 회차와 정본 후속 회차를 **따로 셉니다**. 조기 수렴 재시도 뒤 통과하고 출구 재시도 없이 완료하면 `E.attempt=2`, `full.attempt=1`입니다.

실제 `read.run()`에서 쓰기를 메모리로 대체하고 첫 조기 `CheckRow`에 실패를 주입했습니다. 이후 루프·검사·산출 생성은 러너 코드를 사용했습니다.

```text
RUNNER ok
ACTUAL_COUNTERS 2 1 FULL_ROWS 13
ACTUAL_E2_FULL1_METRICS 4
[t40_metrics] 조기 attempt 가 완주 attempt 보다 크다(생성 순서 위반)
```

따라서 v21이 새로 넣은 “생성 순서” 검사가 합법 완료를 손상으로 바꿉니다.

**고치는 문안:** “조기와 출구 attempt는 각각 자기 판정점의 회차·예산·요청 좌표로 검증하며, `E.attempt ≤ full.attempt` 조건은 제거한다.”

**NR-2 · MED — 회귀표의 합법 부모가 실제 경로와 다르고, 조기 생성 불변식도 남아 있다.**

좌표: 메모 §5·§9 D, [회귀 생성기:129](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_regress.py:129), `Fx.to_pending`·`synth_early`; [지표:278](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:278).

대표적인 불일치는 다음과 같습니다.

- **L09·L10:** 거부 또는 mismatch 행과 실패 full 판정서를 함께 만듭니다. 실제 stale은 `_dispatch`에서 다시 던지고, mismatch는 **full 기록 전** `LaneAssignmentError`를 냅니다. 직접 생성한 두 경로 모두 full이 없었습니다.
- **L11:** `record(req,None)`을 in-progress로 만듭니다. FileLaneAdapter는 전량 응답 또는 예외를 반환하므로 이 형식에 도달하지 않습니다. 다른 어댑터로 빈 응답 목록을 주어도 `_dispatch`가 `StageError`를 내며 **종결**합니다.
- **L12:** “청구항 검사 실패”라고 적었지만 5행을 **전부 pass**로 만듭니다. 러너는 청구항 실패가 없으면 수렴 행을 추가하므로 이런 5행은 생성하지 않습니다.
- **L02·L13:** 통합 대기라고 하면서 완료 런의 통합 소비 행을 남깁니다. `memo_count=0`, `awaiting=synthesize`도 해당 LanePending 경로의 실제 포인터와 다릅니다.

v21은 다음 조합도 수용했습니다.

```text
IMPOSSIBLE_5_ALL_PASS             exit 0 in-progress
IMPOSSIBLE_CURRENT_E0             exit 0 in-progress
IMPOSSIBLE_EXECUTED_CLAIM_FAIL    exit 0 in-progress
SNAPSHOT_WITHOUT_CURRENT_E       exit 0 in-progress
```

세 번째는 청구항 fail·violations·findings를 서로 맞췄는데도 수렴 실행을 함께 허용한 사례입니다. 소견 합계 검증만으로 생성 조건을 대신할 수 없습니다.

**고치는 문안:** “L행을 러너의 실제 생성 경로와 기록 접두부로 다시 만들고, E/S에 청구항 실패↔수렴 실행·회차 기본값·파일 존재 관계를 적용한 뒤 검증된 L에서 C를 파생한다.”

**NR-3 · HIGH — 요청 JSON의 좌석을 검증하지만 그 JSON이 요청 MD를 생성했는지는 확인하지 않는다.**

좌표: 메모 §5 요청 메타 결속, [지표:418](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:418); `LaneRequest` 재구성·`render_request_md`.

현재 검증은 다음 두 갈래입니다.

- MD 바이트 → 재계산 지문 → JSON의 `input_digest`·로그·응답
- JSON의 model/effort → 로그·계약 프로필

그러나 **JSON 필드로 재생성한 요청 본문과 실제 MD의 관계가 빠져 있습니다.** 재구성한 `LaneRequest`도 mismatch 계산에만 씁니다.

메모리 R1 런에 정확한 R1 ID·핀·partial/read·dispatch·스냅샷을 공급했습니다. 프로필과 JSON·로그·응답 effort는 xhigh로 맞추되 MD의 `effort=max`는 유지했습니다.

```text
R1_MEASURE_MD_MAX_ACCEPTED complete
gdm-wo2026128750a1-t40-r1
530b096146e1b7a42f05ffe242e8eccaec2c4d16
component=56
synth={'fact':3,'implication':20,'positioning':7,'figure_note':10}
R1_REQUEST_MD ['| effort | `max` |']
```

이는 실제 API가 max로 호출됐다는 증명이 아닙니다. **서로 모순되는 요청 증거를 R1의 정상 측정 근거로 받아들인다는 반증**입니다.

**고치는 문안:** “해당 트리의 요청 JSON으로 `LaneRequest`를 재구성하여 계산 지문과 `render_request_md` 바이트를 저장된 요청 지문·MD에 대조하고, 그 뒤 프로필·로그·응답 결속을 검사한다.”

**NR-4 · MED — 원장 무결성 검사가 포인터의 생성 관계까지 확인하지 않는다.**

좌표: 메모 §5 원장 무결성·생성 불변식, [지표:251](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:251); `append_screening_ledger`·`_write_shadow_pointer`.

포인터 `memo_count`는 값이 있으면 비음수 정수인지만 검사합니다. 실제 원장·판정서의 메모 수와 대조하지 않습니다. 기준 포인터의 **2를 999로 바꾼 단일 필드 변형**이 다음처럼 통과했습니다.

```text
POINTER_MEMOS_999 exit 0 complete component_count=56
```

종결 가드가 run_id만으로 재호출을 막는 의미는 유지해야 합니다. 그러나 별도로 선언한 무결성 검사가 이 모순까지 증명한 것은 아닙니다.

**고치는 문안:** “종결 가드와 별도로 포인터의 필수 필드·타입 및 종결 시 memo_count·appended를 해당 원장 메모와 대조하되, 대기 포인터 잔존과 기준 런의 역사적 다중행은 구별한다.”

**NR-5 · MED — 스냅샷 부재 처분이 §2와 §5에서 다르다.**

좌표: 메모 §2 마지막 스냅샷 문단·§5 A-05, `metrics`의 275·293행.

§2는 여전히 **0·11·12·13인데 first-early가 없으면 N/A·재상신**이라고 합니다. §5와 코드는 full 또는 수렴 실행 E가 있으면 **증거 결측 exit 4**로 정했습니다. 정상 완료 후 스냅샷 결측에서 적용할 문장이 둘입니다.

코드의 구분은 직접 확인했습니다. 실제 청구항 실패 5행·수렴 미실행은 N/A로 수용했고, full과 스냅샷 부재의 공존은 exit 4였습니다.

**고치는 문안:** “스냅샷 부재는 full·수렴 실행 E가 없는 미관측 상태에서만 N/A이며, 둘 중 하나가 있으면 증거 결측 exit 4로 처리한다고 §2·§5를 통일한다.”

**NR-6 · LOW — 사본 발주 식별자가 요청과 다르다.**

좌표: [.audit-sandbox:3](/home/laptop/projects/workspaces/pd-m1b-t40/.audit-sandbox:3).

path·pin·disposable과 HEAD는 맞지만 실제 order는 다음과 같습니다.

```text
order=M1B-t40-measure-v20-20260906
```

요청은 `…v21…`입니다. 메모 해시는 정확히 일치하여 v21 감수는 수행했지만, **사본 3검증 전부 통과**라고 기록할 수 없습니다.

**고치는 문안:** “사본 준비자가 order를 `M1B-t40-measure-v21-20260906`으로 바로잡고 path·pin·order를 함께 검증한다.”

**B — 계측 커밋 셋: PASS**

부모·전체 팔 diff·절차 tree·프로필을 직접 확인했습니다.

- base `ad4c6c3`의 부모는 `6d92cad`.
- R1 `530b096`, R2 `00e0bed`의 부모는 모두 base.
- base→각 팔은 `contracts/stages/read.yaml` **2/2만** 변경.
- 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`.
- 기준 요청서 재렌더 **6/6 바이트 동일**.
- R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high이며 aliases도 일치.

`d4e6ca2→6d92cad` numstat도 §0′의 16개 열거 파일과 일치했습니다.

| 파일군 | 추가/삭제 |
|---|---|
| read.yaml · convergence.schema · run-kinds | 321/31 · 42/7 · 24/2 |
| read.py · source.py · lanes/contract.py | 713/126 · 46/1 · 67/1 |
| run_checks · convergence · dependency_parse | 90/35 · 32/5 · 30/1 |
| material_spec_md · paths · stages/__init__ · reader/lib/__init__ | 85/1 · 19/0 · 69/0 · 4/0 |
| lanes/plan · file_adapter · replay_adapter | 2/7 · 6/4 · 2/2 |

검사·재시도 변경은 후속 요청 발생과 `defects`에 닿습니다. 동일성을 **같은 입력의 최초 요청**으로 한정한 설명은 맞습니다.

**C — 구동 v6: PASS**

분류 함수에서 **0/11/12/13/14**, 실제 `cmd_read` 대입에서 LanePending **10**, 엔진 예외·종결 포인터 **13**, 증거·스냅샷 실패 **14**를 확인했습니다. 실제 `enter`의 worktree 부재와 잘못된 런 이름도 모두 **14**였습니다.

조회는 무기록입니다. 발주 1~3회는 성공하고 4회째 **15·무기록**, 기존 배치 충돌은 **14·회차 불변**입니다. 축 없는 문서는 별도 보존하고, 생성된 첫 스냅샷은 후속 회차에서 유지합니다.

v6에는 `_next_dispatch`가 없습니다. 후계인 `cmd_dispatch`를 시험했습니다.

**D — 지표 v21·회귀표: REVISE**

기준 CLI는 exit 0이며 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 3/20/7/10·조기 2행·완주 13행**으로 일치했습니다.

자문 수정의 수용 여부는 다음과 같습니다.

| 자문 | 판정 | 근거 |
|---|---|---|
| A-01 | 핵심 수정 수용 | 실제 종결 가드와 원장 루트 해석을 재사용하고 별도 무결성 검사를 명시함. 추가 잔여는 NR-4 |
| A-02 | partially | 세 행 형식·응답 effort·alias 의미 재계산은 구현됨. 검증된 요청 MD와 JSON 메타의 연결은 NR-3 |
| A-03 | partially | 지정 4행·attempt 0·정본 상수·vacuous 변형은 차단. 새 회차 조건은 오거부하고 조기 생성 조건은 누락: NR-1·2 |
| A-04 | closed | check_id별 violations **합계**로 대조. 실제 13행 스키마 실패의 소견 2→1 삭제도 exit 4 |
| A-05 | partially | 코드에서 합법적 부재와 증거 결측을 구별함. §2는 이전 문언 잔존: NR-5 |

자문의 미확인 사항 중 이번에 확인한 것은 다음과 같습니다.

- `shadow_ledger_root`는 링크된 worktree에서 공용 `.git`의 부모를 주 작업 트리로 해석합니다. 실제 함수에 git 판정값만 메모리 대입하여 `main-worktree-resolved`를 확인했습니다. 이 사본 자체는 독립 리포이므로 실제 결과는 `main-worktree`입니다.
- FileLaneAdapter는 모든 요청을 반환하거나 `LanePending`·계약 예외를 던집니다. `load_response`도 lane_id를 대조하므로 **응답 짝 없음 행은 이 어댑터에서 도달하지 않습니다**.
- 계측 세 트리의 `lane_profiles` 값은 §0′와 맞습니다. 값이 맞는 것과 MD까지 결속되는 것은 별개이며 후자는 NR-3입니다.

**44행의 출력 재현과 생성 근거 판정은 다릅니다.**

`Fx`의 파일 작업을 메모리로 바꾸고 원본 `CASES()`와 전체 `metrics()`를 실행한 결과는 **44/44 기대 일치**였습니다. 그러나 L행 검토 결과는 다음과 같습니다.

| L행 | 생성 근거 판정 |
|---|---|
| L01 | 역사적 기준 완료 자료로 유효 |
| L03·L04 | 13행 실패·4행 재독 실패 경로는 존재. 별도 실제 러너 대입으로 확인 |
| L05·L07 | full 뒤 명세/포인터 기록 실패의 존재 조합은 가능 |
| L08 | 원장 단독 종결 경로 가능. 실제 mismatch→원장→포인터 실패로 확인 |
| L02·L13 | 통합 대기 설명과 남긴 소비 행·포인터 값 불일치 |
| L06 | “이전 대기 포인터”라면서 완료 포인터의 terminated만 바꿔 appended=true를 남김 |
| L09·L10 | 거부/mismatch 예외가 full 기록 전에 발생하는 순서와 불일치 |
| L11 | FileLaneAdapter에서 도달 불가. 일반 어댑터로 만들어도 in-progress가 아님 |
| L12 | 청구항 실패가 없는 5행·수렴 미실행 자료를 합법으로 등재 |

C행 역시 모두 “합법 L에서 한 가지만 바꿈”이라고 인증할 수 없습니다.

| C행 | 판단 |
|---|---|
| C01~04·08~13·17·19~21·24~26·28~30 | 의도한 거부 결과 재현. C08·09·29는 여러 필드를 함께 바꾸며, C19는 3행 제거이므로 “하나”의 단위를 불변식/결측 사건으로 명시해야 함 |
| C05~07·22~23·27 | L09~11 계열의 잘못된 부모 상태를 먼저 바로잡아야 함 |
| C14~16·18·31 | 합성 조기 판정서의 생성 근거 보완 필요. 특히 C14는 소견 합계 결측 외에 **청구항 실패와 수렴 실행 공존**도 만들어 독립 변형이 아님 |

추가·교체할 행 문안은 다음과 같습니다.

| 행 제안 | 생성·변형 | 기대 | 이번 실제 |
|---|---|---|---|
| L14 | 조기 수렴 재시도 성공 E=2 → 출구 첫 검사 full=1 완료 | complete | **exit 4** |
| L15 | read.schema 실패 2건 → 후속 재시도 → full 13행·attempt 2·halt | terminated-failure | 일치 |
| L16 | 실제 청구항 실패 → E 5행·수렴 미실행·S 부재 | in-progress·㉠ N/A | 일치 |
| L17 | stale 반향 거부 → finally 기록·종결·full 부재 | terminated-incomplete | 일치 |
| L18 | mismatch → full 전 예외 → 원장 append → 포인터 기록 실패 | terminated-incomplete·ledger-only | 일치 |
| C32 | E 5행에서 청구항 실패 사건을 제거해 전건 pass로 만듦 | exit 4 | **exit 0** |
| C33 | S는 유지하고 현재 실행 E의 attempt만 0으로 변경 | exit 4 | **exit 0** |
| C34 | R1 JSON·프로필 xhigh와 요청 MD max가 공존하도록 결속 불일치 구성 | exit 4 | **complete** |
| C35 | 종결 포인터 memo_count 2→999 | exit 4 | **complete** |
| C36 | S가 있는 미완 자료에서 현재 E 파일만 제거 | 증거 결측 exit 4 | **in-progress** |

기존 지적과 회귀표의 대응도 전량 피복은 아닙니다.

| 지적 부류 | 기존 C행 대응 | 이번 추가 확인 |
|---|---|---|
| MY-5·MZ-5·NA-1 | 직접 대응 없음 | 최신 retry 계약 거부·행 부재에서 이전 synth로 후퇴하지 않고 N/A |
| MY-6·MZ-2·3·NA-4·NB-3·NC-2·3 | C15·16·31 일부 | snapshot ID·phase·SHA·수치·축·파싱 변형 |
| MY-7·MZ-6·NN-1 | C14 일부 | 조기 청구항 4행 결측·배열 보존·실행 귀속 추정 |
| ND-1·NE-1·2 | 직접 대응 없음 | 조기·완주 findings 컨테이너·필수 필드·형태 변형 |
| ND-2·NO-3·NM-2 | 직접 대응 없음 | snapshot·원천·synthesize 응답 각각 단일 읽기 확인 |
| NF-1·NG-1·NH-1·2·NI-1·2·NJ-1 | C28 일부 | 실제 donor 명세/왕복 자료·식별자·원천·MD·dispatch 변형 |
| NK-1·NL-1 | 직접 대응 없음 | 명세 필드 및 component·grounding·종속항 집합 결측 |
| NM-1·NN-2·4 | C19·20·24·26 일부 | 검사 3행·로그 필드·접지 행과 응답 동반 결측 |
| NO-2·4·NP-1~3·NQ-1~3 | C01·19~30의 관련 행 | 실제 4/13행 실패·거부·원장 단독 종결·소견 삭제 |
| 나머지 B·C·E·F·문언 지적 | 지표 C행 대상 아님 | Git 대조·구동 대입·발췌 helper·Node 본문·원장 대조 |

기존 표 외 손상 변형 **42+23=65건**은 모두 exit 4였습니다. 이 숫자는 지적 ID 수와 별개입니다. 앞서 제시한 NR 반례는 별도 시험입니다.

**E — 발췌 v4: PASS**

`ex1/ex2`는 실행하지 않았습니다. 지정 helper를 import하여 확인했습니다.

- implication 자기 대조 **20/20**.
- 5→1 병합에서 같은 후보가 **다섯 단위 모두**에 제시됨. 후보 소비·자동 열위 없음.
- 표본은 **CL-2·4·7·9·12·14·16·19·21·24**.
- 인용 부재·단락 미해소·접지 부재의 판정 불가, search_note 표시, 표본 교체 금지·재상신 문언은 재정 범위와 맞음.

**F — Workflow v4: PASS**

Node에서 실제 본문을 실행하고 `agent/pipeline`을 대체했습니다. `toString`, `/./`, 좌표·dispatch 중복, 런·레인 경로 불일치는 **agent 호출 0회로 거부**됐습니다. 정상 입력의 model/effort 옵션, `wrote=false`와 null 구별도 확인했습니다.

실호출 증거 대조와 dispatch별 이동 보존 절차는 문서상 정합합니다. 실제 API transcript에 대한 확인은 아래 미검증 범위입니다.

**G — 결정 공백: REVISE**

§2와 §5의 스냅샷 결측 처분이 충돌하고, 합법 완료를 거부하는 회차 조건을 실행 중 사람이 우회해야 하는 상태입니다. 이 둘을 현장 재량으로 처리하며 실측을 시작할 수 없습니다. NR-1~5는 기존 원장·생성 코드에 맞춰 고칠 수 있습니다.

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 결과 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `813622e16158b6a16e90c26b59d790ca6cebc1cd` — order 불일치는 NR-6 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `a11df3b2f3b513df60afaab9f486998cb553de75027ff6363ca446d9c24662c9` |
| `sha256sum -c BUNDLE-SHA256.txt` | `bundle/t40_regress.py: OK` — 전건 OK |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git show` 계약 blob → `lane_profiles`; 기준 요청 JSON → 재렌더 | `RERENDER_BYTES_EQUAL 6 /6` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 0·마지막 줄 `}` |
| 같은 CLI에서 옵션 부재·없는 snapshot·sidecar 부재 | 각각 exit 4 |
| `--baseline --first-early …` | exit 3·`함께 쓸 수 없다` |
| `PY - <<'PY' … CASES()/metrics() … PY` — 파일 작업 메모리 대체 | `MEMORY_REGRESS 44 /44` |
| 실제 `read.run`·첫 조기 실패 주입·쓰기 메모리 대체 | `ACTUAL_E2_FULL1_METRICS 4 … 조기 attempt 가 완주 attempt 보다 크다` |
| 실제 schema 재시도·소견 한 건 삭제 | `NQ3_REMOVE_ONE 4 … 합계=2 인데 findings 는 1건` |
| 실제 mismatch·최종 포인터 쓰기 실패 주입 | `… 0 terminated-incomplete shadow_ledger` |
| 실제 최신 synthesize retry 계약 거부 | `LATEST_BAD_RESPONSE_PRESERVED 0 None ['read-a/synthesize/retry-1/batch-0']` |
| 추가 손상 대입 두 묶음 | `DESIGNATED_DAMAGE_REGRESSION 42 / 42`; `EXTRA_PRIOR_REGRESSION 23 / 23` |
| 읽기 횟수 계측 | `SINGLE_READ 0 1 1 1 {'fact':3,…}` |
| 실제 metrics CLI 원천 읽기 예외 대입 | `ACTUAL_METRICS_CLI_SOURCE_READ_FAILURE 4` |
| 구동 분류·진입·발주 메모리 시험 | `DISPATCH_1_4 [(0,False),(0,False),(0,False),(15,True)]`; `LANES_READ_ONLY 0 True` |
| 발췌 helper import·병합·표본 시험 | `MERGE_5_TO_1 ['M100','M100','M100','M100','M100']` |
| `node --input-type=module -` — Workflow 본문 대체 실행 | `WORKFLOW_PROBES_DONE` |
| 봉투 stdout 미리보기 → 러너 검증기 메모리 공급 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |

**[미검증]**

- 실제 계측 worktree 생성·source/read 파일 쓰기·생산 원장 append·봉투 발행·유료 레인 호출은 수행하지 않았습니다.
- `t40_regress.py --work`의 파일 생성·서브프로세스 CLI는 실행하지 않았습니다. 원본 사례 생성 함수와 전체 추출기를 메모리 파일 계층에서 재실행했습니다.
- 연결된 실제 계측 worktree의 git 메타데이터는 만들거나 읽지 않았습니다. 원장 루트는 사본의 실제 판정과, git 판정값을 대입한 실제 해석 함수로 확인했습니다.
- 외부 스테이징 TXT·도면, 실제 Workflow transcript/journal 형식·실호출 effort·문맥 격리, 시간·비용 추정은 미검증입니다.
- 쓰기 오류 시험은 메모리 예외 주입이며 실제 디스크 장애 시험이 아닙니다.

**읽은 파일**

T40 §1·§4·§5, D-20260905-02 §17과 추기, 1~19차 도전 원문의 지적·검증 관련 절, SPEC 지정 행, T14·T17·T38, run-kinds/read 계약과 approval-envelope 스키마, 설계 v3·v21 및 관련 판본, bundle 구동·지표·회귀·발췌·Workflow·봉투·자문 문서, `read.py`·`source.py`·`paths.py`·레인 plan/contract/file_adapter·convergence/run_checks/report 관련 구현, 기준 런 산출물·왕복 자료, donor CIM-FP-3 명세·왕복 자료, 지정 Git tree/blob/diff를 읽었습니다.

파일·임시물·캐시는 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.