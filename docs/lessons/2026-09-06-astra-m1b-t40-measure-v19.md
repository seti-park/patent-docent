# 독립 감수 원문 — M1b 설계 도전 19차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v19 · 판정 REVISE(MED 3)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `c6e1ae9828468455f928d8bdcc243854b10256c3be6fd4e793312e472b044a35` · 17708 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v19/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 10:4x → 11:0x. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `8412b7f` · 마커 pin·order 일치 확인 · v19 sha256 `96212bb0…` · v1~v18 동봉). 폐쇄 = **이전 62건 closed 56 · partially 6 · open 0**(NN-3·NO-2·NO-4·NP-1~3 이 NQ 로 이어짐). **B·C·E·F PASS**(14회 연속).

**판정 = REVISE · 3건(MED 3) · 기각 0 · 발주자 귀책.** **NQ-1**: v19 가 「반향(echoed) 있음」도 소비로 분류해 러너의 정상 거부 기록(`record_rejected` · rejected=true · echoed=틀린 반향 · 모델·응답 SHA 없음)을 손상으로 exit 4 — 거부 행과 소비 행은 요건이 다르다. **NQ-2**: T38 ③ 세 번째 근거(원장의 대상 run_id 행)를 안 봐서 「완주 판정서 기록 전 예외 종결(LaneAssignmentError) → finally 원장 기록 → 최종 포인터 기록 실패」 경로를 in-progress 로 보고 · 포인터 부재를 exit 4 로 닫아 후순위 근거를 조회하지 않음 — **이번 3 런에도 실제로 일어날 수 있는 경로**. **NQ-3**: fail 행에 finding ≥1 만 요구해 violations=2 · findings 1 을 통과 · 조기 판정서는 그 검사조차 없어 findings 전량 제거 + sidecar 갱신이 통과 — 생성 규칙은 `violations = len(row.findings)`.

지적 열거 = NQ-1, NQ-2, NQ-3

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 18**. **전부 수용 → 지표 v20**(소비 = actual_model·response_digest 비-null 만 · 거부 행은 별도 요건(모델·SHA 없음 · digest_ok=false · reason 문자열 · 반향 ≠ 요청 지문) · 종결 근거 셋 순서 조회(포인터 → 완주 판정서 → 원장 run_id 행) · 포인터 부재 = 근거 부재 · 원장 단독 종결 = terminated-incomplete(ledger-only) · 조기·완주 모두 check_id 별 violations == findings 수 · 런 상태 무관 exit 4) → **M1b 20차 도전(지적 `NR-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 62건: closed 56 · partially 6 · open 0. 신규 NQ-1~3은 모두 MED입니다.** 18차 지정 변형은 차단됐지만, 정상 거부 기록의 오거부·원장만 남은 종결의 오분류·소견 일부 결측의 수용이 남았습니다. 실측 착수 불가입니다.

**A — MY~NP 폐쇄 판정**

범위 표기는 해당 ID 각각에 적용합니다. 지정 반례 해결과 수용된 처분 전체의 폐쇄를 구별했습니다.

| 이전 지적 | v19 판정 | 근거 |
|---|---|---|
| MY-1~13 | closed | 고정 핀·절차·27단위·표본·통합 계수·배치·증거 보존 유지 |
| MZ-1~9 | closed | 병합 후보 재사용·스냅샷 결속·예외 경계·발주 상한·경로 거부 확인 |
| NA-1~7 | closed | 최신 retry 계약 거부의 N/A, 조회 분리, 다중 조기 기록, 발췌 처분 확인 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 검사·판정서 형태 검증 유지 |
| NC-1~3 | closed | 실제 enter 실패→14·단일 읽기·수치 제약 유지 |
| ND-1~2 | closed | findings 필수 배열·원소 계약 검증·검증한 응답 바이트로 계수 |
| NE-1~2 | closed | 조기·완주 공통 형태 검사와 finding 필드 검사 유지 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조·실행본 버전 표기 |
| NH-1~2 | closed | donor와 모델 불일치 소비 응답의 결속 검사·baseline 제한 |
| NI-1~2 | closed | 요청 MD 재계산·dispatch·원천 지문 사슬 |
| NJ-1 | closed | 원천 부재·변경·읽기 실패 거부 |
| NK-1 | closed | 명세 필수 필드 결측 거부 |
| NL-1 | closed | grounding·component 전량 제거·dependents=[] 거부 |
| NM-1~2 | closed | 실패 판정서까지 검사 집합 대조·원천 단일 읽기 |
| NN-1·2·4 | closed | 조기 다중집합·로그 중복/동반 결측·엄격한 필드 타입 |
| **NN-3** | **partially** | 기존 합법 상태는 수용. 반향 거부와 원장 단독 종결은 NQ-1·2 |
| NO-1·3 | closed | 후속 pending·최신 계약 거부·응답 단일 읽기 |
| **NO-2** | **partially** | 기존 손상 반례는 차단. 소견 일부 결측은 NQ-3 |
| **NO-4** | **partially** | 지정 공통 검사 반례는 차단. 거부 행·소견 정합의 잔여는 NQ-1·3 |
| **NP-1** | **partially** | 4행·13행 지정 변형은 모두 차단. violations와 소견 수 불일치는 NQ-3 |
| **NP-2** | **partially** | 모델 불일치 소비 행의 검증은 해결. 정상 거부 행까지 소비로 분류: NQ-1 |
| **NP-3** | **partially** | false 포인터+full 판정서는 해결. 원장만 남는 경로는 NQ-2 |

§8의 격은 유지됩니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 문언 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이고, 인덱스·후보 제시·런 표기는 구현 재량입니다. G-12의 일반 집행 공백은 그대로이며, 이번 발주의 `partial/read` 제한과 구별해야 합니다.

**지적 목록**

**NQ-1 · MED — 정상적인 반향 거부 행을 소비 기록 손상으로 오판한다.**

좌표: 메모 §5 소비 행 정의·전 상태 공통 검사·§9 D; [t40_metrics.py:280](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:280), 302행의 `consumed`; [read.py:231](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:231) `LaneJournal.record_rejected`.

실제 파일 어댑터에 synthesize 응답의 잘못된 `input_digest`를 공급했습니다. `_dispatch()`는 `LaneStaleResponseError`를 잡아 다음 행을 남기고 다시 던집니다.

```text
rejected=true, ok=false, mismatch=false
echoed_digest=<틀린 반향>
actual_model=null, response_digest=null, digest_ok=false
```

이는 **러너가 정해진 형식으로 생성한 거부 기록**입니다. 그런데 v19는 `echoed_digest is not None`만으로도 소비 행으로 분류하고, 올바른 반향·모델·응답 SHA를 요구합니다.

```text
RUN stale LaneStaleResponseError
METRICS stale exit 4
소비 행인데 반향·digest_ok·응답 지문·actual_model 이 정합하지 않다
```

NP-2의 모델 불일치 행은 실제로 소비됐지만, 이 행은 반향 검사에서 거부됐습니다. 두 상태를 같은 요건으로 검사하면 실패 증거를 그대로 보존한 런이 손상 자료로 바뀝니다.

**고치는 문안:** “`record_rejected` 형식의 반향 거부 행을 소비 행과 분리하여 요청 결속·거부 반향·사유를 검증하고, 해당 형식에 존재하지 않는 모델·응답 SHA를 요구하지 않으며 지표는 N/A로 보존한다.”

**NQ-2 · MED — 원장만 남는 실제 종결 경로를 진행 중으로 보고한다.**

좌표: 메모 §5 종결 정의·§9 D; [t40_metrics.py:181](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:181), 187행 `terminated`; T38 ③; [read.py:1094](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1094) `_run_is_terminated`.

**세 번째 근거 누락은 이번 3런에도 문제가 됩니다.** 실제 러너에서 다음 경로를 재현했습니다.

1. 이전 대기 포인터는 `terminated=false`.
2. synthesize 모델 불일치로 `LaneAssignmentError` 발생 — 완주 판정서 기록 전입니다.
3. `finally`의 실제 `append_screening_ledger()`는 메모 2건을 가진 원장 행을 기록.
4. 마지막 포인터 기록에만 `PermissionError` 발생.

파일 출력은 메모리로 받았으며, 원장 행 생성 함수와 사후 종결 가드는 실제 코드였습니다.

```text
full_exists False
pointer {'terminated': False, 'awaiting': 'convergence_continue'}
ACTUAL_TERMINATION_GUARD (True, 'shadow_ledger')
LEDGER_ONLY_FINAL exit 0 state in-progress
```

따라서 “포인터→완주 판정서” 두 근거만으로는 T38 ③을 이행하지 못합니다. 또한 포인터가 아예 없으면 181행에서 즉시 exit 4여서 후순위 근거를 조회하지 않습니다.

**고치는 문안:** “T38 ③의 포인터·phase=full 판정서·대상 run_id 원장 행을 모두 순서대로 조회해 종결을 확정하고, 포인터 부재·false와 원장 단독 종결은 사유를 가진 종결 상태 및 N/A로 보존한다.”

**NQ-3 · MED — 소견 존재 검사만으로는 소견 결측을 막지 못하며, 조기 판정서는 그 검사도 빠진다.**

좌표: 메모 §5 손상 검증·검사/findings 보존·§9 D; [t40_metrics.py:249](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:249) `find_checks`, [조기 출력:221](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:221); `CheckRow.to_row_dict`·`to_convergence_payload`.

실제 러너에 서로 다른 두 항목의 스키마 위반을 공급했습니다. 재시도 뒤 나온 판정서는 **full/halt·attempt 2·13행·executed=true·read.schema violations=2·findings 2건**입니다.

그 판정서에서 **findings 한 건만 제거**했습니다. 검사 행과 violations는 유지했습니다.

```text
ONE_OF_TWO_FINDINGS_REMOVED exit 0 state terminated-failure
REMAINING 1 RECORDED 2
```

v19는 해당 check의 finding이 하나 이상인지만 봅니다. 실제 생성 규칙인 `violations = len(row.findings)`와 대조하지 않으므로 일부 소견이 사라져도 통과합니다.

조기 경로는 더 넓게 열려 있습니다. 실제 러너가 생성한 `convergence-exact-match` 대기 자료는 조기 6행 중 `read.convergence fail·violations=1·finding 1건`입니다. **findings 전량을 제거하고 변경본에 맞는 sidecar를 공급해도** 다음처럼 통과했습니다.

```text
ACTUAL_EARLY_FINDINGS_REMOVED exit 0 state in-progress
```

스키마·SHA 검증은 이 행과 소견 사이의 불일치를 잡지 못합니다.

**고치는 문안:** “조기·완주 판정서 모두 check_id별 violations 합계와 findings의 해당 check 계수를 대조하고, 실패 상태·소견 귀속·계수가 어긋나면 런 상태와 무관하게 exit 4로 거부한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| A 원장 정합·폐쇄·격 | **REVISE** | T38 세 번째 종결 근거 및 실패 증거 처리 잔여 |
| B 계측 커밋 셋 | **PASS** | 부모·tree·blob·전체 팔 diff·numstat·프로필·최초 요청 동일성 확인 |
| C 구동 v6 | **PASS — 확인 범위** | 종료 분류·진입/증거 실패·스냅샷·조회/발주·상한 재확인 |
| D 지표 v19 | **REVISE** | NQ-1~3 |
| E 발췌 v4 | **PASS — 확인 범위** | 27단위·병합 후보 재사용·표본·판정 불가 처분 유지 |
| F Workflow v4 | **PASS — 대체 실행 범위** | 지정 사전 거부·wrote/null 구별 확인 |
| G 결정 공백 | **REVISE** | 거부 자료·원장 단독 종결·소견 결측의 처분이 구현과 충돌 |

NQ-1~3은 기존 원장과 기록 규칙의 집행 수정으로 닫을 수 있습니다. 새로운 좌석 값이나 임계 재정이 필요한 지적은 아닙니다.

**B — 직접 대조 결과**

마커의 path·pin·order·disposable과 HEAD는 모두 일치했습니다. 메모 SHA-256도 `96212bb0545de80f6fe9e030fadbf566d0a1250d1ac4c262fcf68604d6b80d9d`로 일치합니다.

base 부모는 `6d92cad`, R1·R2 부모는 `ad4c6c3`입니다. 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `6d92cad→base`는 절차 6파일뿐이고, 두 팔은 각각 `2/2 contracts/stages/read.yaml`뿐입니다.

§0′의 d4e6ca2 이후 변경 열거 **16파일 전부 일치**했습니다.

| 파일 | 추가/삭제 |
|---|---|
| read.yaml · convergence 스키마 · run-kinds | 321/31 · 42/7 · 24/2 |
| read.py · source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| lanes/plan.py · file_adapter.py · replay_adapter.py | 2/7 · 6/4 · 2/2 |
| paths.py · stages/__init__.py | 19/0 · 69/0 |
| render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py · convergence.py · dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

`lane_profiles()`는 R1 분해·통합만 xhigh, R2 종속 접지만 sonnet-5/high로 산출했습니다. Sonnet aliases도 확인했습니다. 규칙·material-spec 스키마 diff는 비었고, 기준 요청 재렌더 **6/6 바이트 동일**, 신규 최초 분해 요청 차이 필드는 `[]`였습니다. 재시도 소견을 넣으면 본문·지문은 달라집니다. 동일성 범위를 최초 요청으로 한정한 문안은 맞습니다.

**D — 지정 반례와 실제 실행 경로**

| 검증 | v19 결과 |
|---|---|
| 4행 halt: fail 행+findings 제거 / pass 행 중복 / 엔진 3행 제거 / findings만 제거 | **4/4 exit 4** |
| 13행 실패 판정서의 같은 네 변형 | **4/4 exit 4** |
| 4행 유지·executed=false·전건 pass로 변경 | **exit 4** |
| finding이 pass 검사를 지목 | **exit 4** |
| 온전한 4행 source halt / 13행 schema halt | **exit 0·terminated-failure** |
| 온전한 모델 불일치 소비 행 | **exit 0·terminated-failure** |
| 해당 응답 교체·제거·반향 변조·model/input_digest/lane_id 불일치 | **전부 exit 4** |
| false 포인터+정상 full 판정서 | **terminated-incomplete·pointer-not-terminated** |
| 판정서 통과 뒤 명세 기록 실패 | **terminated-incomplete·spec-absent** |
| 접지 retry 일부 도착 | **in-progress**, 미소비 응답 2좌표 보존 |
| 최신 synthesize retry 계약 거부 | **terminated-failure**, 해당 미소비 응답 보존·㉣ N/A |
| 정상 synthesize 응답 대기 | **in-progress·㉣ N/A** |

**halt의 행 집합은 처분 이름만으로 정해지지 않습니다.** 출구 원천 재독 `OSError` 경로는 `input-digest·source-digest·lane-log-shape·lane-log-digest-value` **4행·executed=false**입니다. 반면 직접 생성한 `read.schema retry→halt`는 **법의 전건 13행·executed=true**였습니다. 현재 실측의 두 독해 실행 조건에서는 v19의 두 기대 집합과 맞습니다.

MY~NO의 형태·결측·수치·결속 지정 반례를 재구성한 **234건은 전부 exit 4**였습니다. 실제 CIM-FP-3 donor 명세·요청/응답/로그 묶음도 거부됐습니다. 단일 읽기 프로브에서는 원천·스냅샷·통합 응답이 각각 1회 읽혔고 **fact=3**이 유지됐습니다.

기준 CLI 결과는 **complete·163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact/implication/positioning/figure_note=3/20/7/10·na=[]**입니다.

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`이며, 메모리 시험은 `PY -c '<하네스>'`로 전경 실행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `8412b7f4cd279e03760c2e6d797bf3af49cae04f` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `96212bb0545de80f6…6b80d9d` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| base→R1·R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader/lib` | `90 35 reader/lib/run_checks.py` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `}` · exit 0 |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다` · exit 4 |
| 부재 `--first-early` 지정 | `first-early 스냅샷 없음` · exit 4 |
| 실제 CLI 본문·불일치 sidecar 공급 | `스냅샷 sha256 불일치` · exit 4 |
| 실제 CLI·실측 런 baseline / 옵션 병용 | exit **4 / 3** |
| 지표 오류 입력 회귀 | `REGRESSION_EXPECT4 234 COUNTS {4: 234} UNEXPECTED []` |
| 실제 러너 반향 거부→추출기 | `METRICS stale exit 4` |
| 실제 원장 append·포인터 실패→종결 가드/추출기 | `(True, 'shadow_ledger')` / `state in-progress` |
| 실제 schema 소견 2건 중 1건 제거 | `REMAINING 1 RECORDED 2` · exit 0 |
| 실제 조기 exact-match 소견 제거 | `ACTUAL_EARLY_FINDINGS_REMOVED exit 0 state in-progress` |
| 구동 분류·예외 분류 | `CLASSIFY [0,13,11,12,12,14,14]` · `AFTER_EXCEPTION [13,14]` |
| 실제 enter worktree 부재·잘못된 런 이름 | 각각 `14 SYSTEMEXIT_EVIDENCE True` |
| 증거 기록 실패 | `ENGINE_EVIDENCE_FAIL 14` · `RECORD_NO_RETHROW False` |
| 스냅샷 미실행 보존·최초 유지·SHA | `SNAPSHOT True True True` |
| 발주 A/A/A/B/C/D·조회 4회 | 코드 `0/14/14/0/0/15` · 회차 `1/1/1/2/3/3` · 조회 불변 |
| 실제 pending 순차 공급 | 호출 4의 조기 기록 `[(False,0,0),(True,1,6)]` · 최초 실행 스냅샷 유지 |
| 발췌 순수 함수 import | `EXCERPT_SELF 27 /27` · 병합 `[['M20'],['M20'],['M20'],['M20'],['M20']]` |
| 표본·원문 대조 | CL-2·4·7·9·12·14·16·19·21·24 · `LOCATORS 27 RESOLVED 27` |
| `node --input-type=module -`·Workflow 본문 | toString·constructor·/./·중복·교차·좌표 오류 모두 `calls:0,error:true` |
| Workflow 정상 보고 | `requested:3,wrote:1,not_written:1,dropped:["r2"]` |
| 봉투 stdout 미리보기→실제 검증기 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**v6에는 `_next_dispatch`가 없습니다.** 현행 계수 경로인 `cmd_dispatch`를 시험했습니다. 발췌 `ex1/ex2`와 발췌 CLI는 실행하지 않았습니다.

러너 시험은 실제 `read.run`·요청 생성·`FileLaneAdapter`·응답 계약 검사·판정서 생성 경로를 사용했습니다. 진입 지문 검사·최초 종결 가드·봉투 확인은 대체했고, 절차는 base blob, 응답 payload는 보관 자료를 공급했습니다. 파일 읽기·쓰기는 메모리 자료로 대체했습니다. NQ-2의 원장 행 생성과 사후 종결 가드는 실제 함수를 실행했습니다. 234건 회귀는 `metrics()`와 CLI와 같은 예외 처분 경계에서 수행했고, 옵션·sidecar·필드 결측은 실제 CLI 본문으로도 확인했습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다.
- 실제 Workflow 모델 호출·transcript/journal 이벤트 형식·실호출 effort·문맥 격리는 검증하지 않았습니다.
- 실제 worktree 생성·source 봉인·봉투 발행·생산 원장 기록은 수행하지 않았습니다.
- 역사적 d4e6ca2 러너 재기동, 비용·시간·토큰·가용 메모리 추정은 검증하지 않았습니다.
- 구동·발췌·Workflow의 이전 실행본과의 바이트 동일성은 검증하지 않았습니다.

**읽은 파일**

- 원장·이력: T40 §1·§4·§5, D-20260905-02 §17와 추기, MY~NP 도전 원문의 지적·반례·처분, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v19 및 v18 대조, bundle 스크립트 5종.
- 구현: read·source 러너, lanes의 plan·contract·file_adapter, paths·ReadView, convergence·run_checks·report·schema_check 및 관련 검사 호출 경로.
- 실물: 기준 run.yaml·원천·조기/완주 판정서·명세·로그·요청/응답 6벌, CIM-FP-3 donor 자료, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.