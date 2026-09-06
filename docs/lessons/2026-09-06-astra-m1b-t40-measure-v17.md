# 독립 감수 원문 — M1b 설계 도전 17차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v17 · 판정 REVISE(MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `ed1a0e3697bcc7f51b2f47e7af7b13333400cf783dafcf89fd6ed46de471ace7` · 18412 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v17/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 09:37:25 → 09:56 · **USAGE = input 4,783,115(cached 4,576,896) · output 27,887(reasoning 7,047)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `4894eee` · v17 sha256 `ae24f8d6…` · v1~v16 동봉 · 지표 v17 전면 재작성). 폐쇄 = **이전 55건 closed 47 · partially 7 · open 1**(ND-2 가 v17 재작성에서 **회귀** — NO-3). **B·C·E·F PASS**(12회 연속).

**판정 = REVISE · 4건(MED 4) · 기각 0 · 발주자 귀책.** **NO-1**: `terminated=false` 는 조기 대기뿐 아니라 접지·통합 응답 대기(LanePending)에도 쓰이는데 v17 이 「분해 외 행 = 모순」으로 오거부 · 배치 미완·계약 거부로 소비되지 않은 응답을 「응답 있는데 행 없음」으로 오거부. **NO-2**: complete 의 부정을 실패로 정의 → 검사 3행 제거·행 중복(전건 pass) 손상이 「종결 실패」로 빠짐 · 반대로 러너는 판정서를 먼저 쓰고 명세를 뒤에 쓰므로 「판정서 pass ∧ 명세 부재」는 합법 상태인데 exit 4. **NO-3**: ㉣ 계수가 검증 밖 재읽기 바이트 사용(ND-2 회귀). **NO-4**: 비 complete 상태에서 명세 원천 지문·소비 행 반향/digest_ok 정합·lane-log 파일 부재·`batch=true`·포인터 `terminated=1` 을 수용.

지적 열거 = NO-1, NO-2, NO-3, NO-4

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 16**. **전부 수용 → 지표 v18**(상태 = complete / in-progress / terminated-failure / **terminated-incomplete**(판정서 pass ∧ 명세 부재 = N/A) · 손상(fail 없는데 id 집합 불일치·중복) = exit 4 · 소비되지 않은 응답은 근거 보존 + N/A · ㉣ = 검증한 바이트 그대로 · 전 상태에서 명세 원천 지문·행 내부 정합·엄격 bool/int·lane-log 부재+응답 존재 거부) → **M1b 18차 도전(지적 `NP-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 55건: closed 47 · partially 7 · open 1.** 16차 합법 상태 넷 중 **둘만** exit 0·N/A로 추출됩니다. 완주 검사 결측과 통합 응답 계수의 회귀도 확인했습니다. **NO-1~4, 모두 MED. 실측 착수 불가입니다.**

사본 path·pin·order·disposable과 HEAD `4894eee0e5a3d39f888a1c6fedae387a42e7a88d`가 일치합니다. 메모 SHA-256도 지정값 `ae24f8d625e0af7c…`와 일치합니다.

**A — MY~NN 폐쇄표**

범위 표기는 해당 ID 각각에 적용합니다. 기존 반례와 수용된 처분 범위를 기준으로 판정했습니다.

| 이전 지적 | v17 판정 | 근거 |
|---|---|---|
| MY-1~4 | closed | 고정 핀·절차 동일성·잡음 방향 한정·27단위·청구항 표본 유지 |
| MY-5~7 | closed | 수확 제외·6축·검사 배열 보존. 추가 지문 문제는 ND-2 |
| MY-8~13 | closed | 구동 분류·배치 순서·완료 구별·호출별 증거·보존 범위 유지 |
| MZ-1 | closed | 5→1 병합 후보를 다섯 단위에서 재사용, 자동 열위 없음 |
| **MZ-2** | **partially** | 미실행 스냅샷 제외 유지. 합법적 미완의 N/A 처리는 NO-1 |
| MZ-3~4 | closed | 스냅샷 결속·옵션 제한·구동 예외 분류 유지 |
| **MZ-5** | **partially** | 이전 성공값으로 후퇴하지 않지만 계수 바이트 결속은 NO-3으로 회귀 |
| MZ-6~9 | closed | 검사 귀속 추정·증명 기준·발주 상한·Workflow 방어 유지 |
| **NA-1** | **partially** | 로그 없는 최신 계약 거부를 N/A 전에 차단: NO-1 |
| NA-2~7 | closed | 예외 경계·조회 분리·형태 검증·보존 설명·경로·발췌 처분 유지 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 검사·판정서 형태 검증 유지 |
| NC-1~3 | closed | 실제 enter 실패→14·스냅샷 단일 읽기·수치 제약 유지 |
| ND-1 | closed | findings 필수 배열·원소 계약 검증 유지 |
| **ND-2** | **open** | 동일 경로 두 번째 읽기의 fact 제거 반례가 다시 적격으로 통과: NO-3 |
| NE-1~2 | closed | 조기·완주 공통 형태 검증·finding 필드 검증 유지 |
| NF-1 | closed | 완주 run_id 대조 유지 |
| NG-1~2 | closed | 명세 run_id 대조·버전 표기 일치 |
| NH-1~2 | closed | 지정 donor 요청·응답 반례 거부·baseline 우회 차단 |
| NI-1 | closed | 요청 MD 재계산·request_digest 필수·dispatch 대조 유지 |
| **NI-2** | **partially** | complete에서는 원천 사슬 검사. awaiting의 타 원천 명세는 통과: NO-4 |
| NJ-1 | closed | 원천 부재·읽기 실패·변경 거부 |
| NK-1 | closed | 명세 필수 필드 결측 거부 |
| NL-1 | closed | complete의 grounding·component 전량 제거·dependents=[] 거부 |
| **NM-1** | **partially** | 완주 엔진 검사 3행 제거가 exit 0으로 회귀: NO-2 |
| NM-2 | closed | 원천 읽기 1회, 재읽기 예외 경로 제거 유지 |
| NN-1~2 | closed | 지정 조기 4행 결측·접지 행+응답 결측·정상 행 중복 모두 exit 4 |
| **NN-3** | **partially** | 합법 상태 4개 중 2개만 해결: NO-1 |
| **NN-4** | **partially** | 필드 결측은 exit 4. `batch=true`는 타입 검사 통과: NO-4 |

§8의 격은 유지됩니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 문언 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표기는 재량입니다. 아래 결함은 이 해석의 집행 문제입니다.

**NO-1 · MED — pending과 미소비 응답을 여전히 기록 결측으로 오판한다.**

좌표: 메모 §5 상태별 요건·㉣·§9 D; [t40_metrics.py:245](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:245), [272행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:272); `FileLaneAdapter.dispatch`, `read._dispatch`.

실제 `read.run`과 파일 어댑터를 실행하고 파일 출력만 메모리로 바꾼 결과입니다.

| 16차 합법 상태 | 실제 러너 산출 | v17 추출 |
|---|---|---|
| 조기 상신 대기 | early 6행·분해 로그 2행·terminated=false | **exit 0 · awaiting · N/A** |
| 접지 retry 일부 도착 | LanePending·기존 로그 6행·terminated=false | **exit 4** — “분해 외 레인 행이 있다” |
| 최신 synthesize retry의 LaneContractError | 최신 응답 존재·그 좌표 로그 없음·terminated=true | **exit 4** — “응답이 있는데 lane-log 행이 없다” |
| 출구 원천 재독 실패 | halt·full 4행·executed=false | **exit 0 · terminated-failure · N/A** |

`terminated=false`는 조기 상신뿐 아니라 **접지·통합 응답 대기**에도 쓰입니다. 실제 정상 통합 응답 대기도 로그 5행을 남기며 같은 오류로 거부됐습니다.

또 파일 어댑터는 배치 일부가 미도착하면 이미 읽은 응답도 반환하지 않습니다. `LaneContractError` 역시 `_dispatch`의 기록 전에 발생할 수 있습니다. 따라서 응답 파일의 존재만으로 소비 행을 요구할 수 없습니다.

**고치는 문안:** “조기 상신과 후속 LanePending을 구별하고, 배치 미완·계약 거부로 소비되지 않은 응답은 그 근거와 N/A를 보존하며, 근거 없는 소비 기록 결측만 exit 4로 거부한다.”

**NO-2 · MED — complete의 부정을 실패로 정의하여 손상 자료를 합법적 실패로 바꾼다.**

좌표: 메모 §5 complete 판정식·§9 D; [t40_metrics.py:214](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:214), `complete`, `state`; `read.run`의 완주 판정서·명세 기록 순서.

정상 R0 대조 자료에서 다른 증거를 유지하고 완주 판정서만 변경했습니다.

| 변경 | 결과 |
|---|---|
| `read.input-digest`·lane-log 검사 2종 제거 | **exit 0 · terminated-failure** |
| 정상 검사 행 하나 중복 | **exit 0 · terminated-failure** |

첫 사례는 **NM-1의 지정 반례**입니다. 남은 10행은 전부 pass인데, 실패 근거 없이 “정상 종결 형태가 아니다 → 종결 실패”로 처리합니다. 완전성 검사를 통과하지 못한 자료가 그 검사 적용 대상에서 빠지는 구조입니다.

반대 방향의 오판도 실제 러너로 확인했습니다. 러너는 [완주 판정서를 먼저 기록](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:2084)하고 [명세를 나중에 기록](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:2117)합니다. 명세 기록에만 `PermissionError`를 주면:

- terminated=true
- 완주 13행 전건 pass·executed=true
- material-spec 부재

가 남습니다. v17은 이를 complete로 선택한 뒤 **“complete 런인데 material-spec.json이 없다”**로 거부합니다. 따라서 제시한 식은 정상 검사 경로와 맞지만 **러너의 성공 완료를 확정하는 충분조건은 아닙니다.**

**고치는 문안:** “성공·실패·미확정은 실행 및 예외 증거로 먼저 확정하고 경로별 검사 다중집합을 검증하며, complete 요건 불충족 자체를 실패의 증거로 사용하지 않는다.”

**NO-3 · MED — 통합 계수가 다시 지문 검증 밖의 재읽기 바이트를 사용한다.**

좌표: 메모 §5 ㉣ `[ND-2]`; [t40_metrics.py:258](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:258), [329행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:329).

로그 검증에서 읽은 응답은 SHA를 대조하지만, 계수 단계에서 같은 파일을 다시 읽고 **그 바이트의 SHA는 대조하지 않습니다.**

ND-2와 같은 메모리 반례를 재실행했습니다. 첫 읽기에는 기준 응답 원본, 두 번째 읽기에는 fact 항목만 제거한 JSON을 공급했습니다.

```text
ND2_EXACT_SECOND_READ_FACT_REMOVAL exit 0 state complete
synth {'implication': 20, 'positioning': 7, 'figure_note': 10}
ND2_READS 2 HASHED_FACT 3 COUNTED_FACT 0 ELIGIBLE True
```

실제 동시 변경이 발생했다는 주장이 아닙니다. **로그가 지목한 응답과 다른 바이트의 계수를 적격 지표로 출력할 수 있다는 직접 반증**입니다.

**고치는 문안:** “㉣은 로그와 SHA를 대조한 단일 응답 바이트를 그대로 파싱·계수하며, 계수 단계의 파일 재읽기를 제거한다.”

**NO-4 · MED — 비complete 상태에서 상시 적용한다고 선언한 결속·타입 검사가 빠진다.**

좌표: 메모 §5 “어느 상태에서도 위조·혼입·손상은 exit 4”; [t40_metrics.py:178](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:178), lane-log 분기, [비complete 명세 검증:333](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:333).

독립 반례는 다음과 같습니다.

| 대입 | v17 결과 |
|---|---|
| 정상 awaiting 자료에 실물 CIM-FP-3 명세의 run_id만 R0로 바꿔 추가 | **exit 0 · awaiting** — 다른 원천 지문 수용 |
| awaiting의 소비 행에서 echoed_digest 변경·digest_ok=false, ok=true 유지 | **exit 0 · awaiting** |
| awaiting의 lane-log 파일 전체 제거, 분해 응답·dispatch 유지 | **exit 0 · awaiting** |
| awaiting 로그의 batch를 `true`로 변경 | **exit 0 · awaiting** |
| 정상 자료의 포인터 terminated를 숫자 `1`로 변경 | **exit 0 · terminated-failure** |

원인은 구체적입니다.

- 비complete 명세에서는 `patent.source_digest`를 대조하지 않습니다.
- 소비 행의 반향·digest_ok 정합을 검사하던 엔진 검사는 complete에만 적용됩니다.
- lane-log 파일 자체가 없으면 dispatch 대조도 건너뜁니다.
- `isinstance(True, int)`와 `1 in (True, False)`가 타입 검사를 통과합니다.

이 자료들은 정상 지표로 계수되지는 않지만, 선언한 **“손상은 exit 4, 합법적 미완만 N/A”** 경계를 통과합니다.

**고치는 문안:** “상태와 무관한 식별자·원천·소비 행 결속·엄격한 타입 검사를 공통 적용하고, 로그 파일 부재도 발주·응답 증거와 대조하여 손상을 합법적 미완으로 수용하지 않는다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합. 결측·실패·N/A 집행에 NO-1~4 |
| **B 계측 커밋 셋** | **PASS** | 부모·tree·blob·팔 diff·16파일 numstat·프로필·최초 요청 동일성 확인 |
| **C 구동 v6** | **PASS** | 종료 분류·실제 enter 실패·증거 실패·스냅샷·발주 상한 재시험 |
| **D 지표 v17** | **REVISE** | 합법 상태 오거부·검사 결측 수용·계수 지문 회귀·상시 검증 누락 |
| **E 발췌 v4** | **PASS** | 27단위·병합 후보 재사용·청구항 표본·판정 불가 처분 확인 |
| **F Workflow v4** | **PASS** | 지정 사전 거부와 wrote/null 구별 재시험 |
| **G 결정 공백** | **REVISE** | 미소비·실패·증거 손상의 처분을 실행 중 수작업 선택 없이 적용할 수 없음 |

C·E·F의 PASS는 정적·메모리 검증 범위입니다.

**B — 직접 확인한 변경 범위**

base 부모는 `6d92cad`, R1·R2 부모는 `ad4c6c3`입니다. 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `6d92cad→base`는 절차 6파일뿐이며, 각 팔은 `2 2 contracts/stages/read.yaml`뿐입니다.

§0′의 변경 열거 **16파일 전부** 재실측과 일치했습니다.

| 파일 묶음 | 추가/삭제 |
|---|---|
| read.yaml·convergence 스키마·run-kinds | 321/31 · 42/7 · 24/2 |
| read.py·source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| lanes/plan.py·file_adapter.py·replay_adapter.py | 2/7 · 6/4 · 2/2 |
| paths.py·stages/__init__.py | 19/0 · 69/0 |
| render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py·convergence.py·dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

`lane_profiles()`는 R1의 분해·통합만 xhigh, R2의 종속 접지만 sonnet-5/high로 산출했습니다. 최초 요청서 재렌더는 **6/6 바이트·지문 동일**, 신규 최초 분해 요청의 차이 필드는 `[]`입니다. 실제 소견을 넣은 재시도 요청에서는 본문과 지문이 바뀌었습니다. 최초 요청의 동일성을 재시도까지 확대하지 않은 문안은 맞습니다.

**D — 회귀 시험 범위와 결과**

오류 입력 회귀 **237건 중 236건은 exit 4**, 나머지 하나는 **완주 엔진 검사 3행 제거 → exit 0**이었습니다. 별도로 실물 donor 명세·요청·응답 계열 6건은 complete에서 모두 exit 4였습니다. 같은 donor 명세를 awaiting에 넣으면 NO-4처럼 통과합니다.

237건에는 조기·완주 필수 필드, 식별자·국면, 축 결측·중복, bool·음수 계수, bool·NaN·무한대·범위 밖 Jaccard, checks·findings 형태, finding 필수 키, 명세 필수 필드·집합 결측, 로그 필드, 요청·응답·dispatch·원천 결속 반례를 포함했습니다.

기준 CLI는 **exit 0·complete·163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 3/20/7/10·na=[]**였습니다. 스냅샷과 원천은 각각 읽기 1회였으며 NC-2·NM-2는 유지됩니다. 통합 응답만 읽기 2회로 회귀했습니다.

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 다음 명령입니다.

```text
PYTHONDONTWRITECODE=1   # 사용하지 않음
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python
```

메모리 시험은 `PY - <<'PY' … PY`로 전경 실행했습니다. 지표 시험은 `open/io.open/isfile/isdir/exists/listdir/walk`를 메모리 자료로 대체하고 **실제 CLI 본문과 검증 함수**를 실행했습니다. 변경한 스냅샷에는 일치하는 sidecar를 공급했습니다.

러너 시험은 진입 지문·종결 가드, 봉투 확인, 출력·원장 append를 대체했습니다. 분해·접지·통합은 보관 payload를 사용했고, 제어 흐름·파일 어댑터·응답 계약 검증·검사·판정서 생성은 실제 코드를 실행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `4894eee0e5a3d39f888a1c6fedae387a42e7a88d` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `ae24f8d625e0af7cd30c945364a8735f9ff42726040f618455143e6e94095200` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| base→R1·R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · exit 0 |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다` · exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json` · exit 4 |
| 메모리 sidecar SHA 불일치 | `스냅샷 sha256 불일치` · exit 4 |
| 회귀 CLI 하네스 | `REGRESSION_EXPECT_EXIT4 237 COUNTS {4: 236, 0: 1}` |
| 실제 러너→지표, 접지 retry pending | `awaiting 상태인데 분해 외 레인 행이 있다(모순)` |
| 실제 러너→지표, 최신 통합 계약 거부 | `응답이 있는데 lane-log 행이 없다` |
| 통합 두 번째 읽기의 fact 제거 | `HASHED_FACT 3 COUNTED_FACT 0 ELIGIBLE True` |
| 구동 `classify`·예외 분류 | `CLASSIFY [0, 13, 11, 12, 12, 14, 14] AFTER_EXCEPTION [13, 14]` |
| 실제 enter의 worktree 부재·잘못된 런 이름 | 각각 `14 … SYSTEMEXIT_EVIDENCE True` |
| 증거 기록 실패·종결 포인터 true | `ENGINE_EXCEPTION_EVIDENCE False 14` |
| 스냅샷 메모리 복사·쓰기 | `SNAPSHOT_NOCONV True FIRST_PRESERVED True SHA_MATCH True` |
| 발주 A/A/A/B/C/D | 종료 `0/14/14/0/0/15`, 회차 `1/1/1/2/3/3` |
| 조회 4회 | `LANES_QUERY4_UNCHANGED True` |
| 발췌 함수 import·자기 대조 | `EXCERPT_SELF 27 /27 ORDER_STABLE True` |
| 5→1 병합 | `[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| 표본·원문 단락 대조 | CL-2·4·7·9·12·14·16·19·21·24 · `LOCATORS 27 RESOLVED 27` |
| Node Workflow 본문, agent/pipeline 대체 | toString·constructor·/./·중복·교차·좌표 오류 모두 `calls 0` |
| Workflow 정상 보고 분기 | `wrote:1, not_written:1, dropped:r2, requested:3` |
| 봉투 stdout 미리보기→러너 검증기 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 최종 `git status --porcelain --untracked-files=no` | 빈 출력 |

**v6에는 `_next_dispatch`가 없습니다.** 현재 계수 구현인 `cmd_dispatch`를 시험했습니다. 발췌의 `ex1/ex2` 또는 CLI는 실행하지 않았습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다. 사본 원천과 PATENT_META는 확인했습니다.
- 실제 Workflow 모델 호출·transcript/journal 형식·실호출 effort·문맥 격리는 검증하지 않았습니다.
- 실제 source 봉인·worktree 생성·봉투 쓰기·생산 원장 append는 수행하지 않았습니다.
- 기준 런 재검사는 현재 사본 코드로 수행했습니다. 역사적 `d4e6ca2` 러너를 재기동한 것은 아닙니다.
- 구동·발췌·Workflow의 전판 실행본과 바이트 동일성, 비용·시간·토큰·메모리 추정은 검증하지 않았습니다.

**읽은 파일**

- 원장: T40 전문, D-20260905-02 §17·추기, 1·2차 도전 원문, 3~15차 지적·반례 관련 부분, 16차 원문, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v17, v16→v17 대조, bundle 스크립트 5종.
- 구현: read·source 러너, lanes의 plan·contract·file_adapter, paths, ReadView, reader의 convergence·run_checks·report·검사 호출 경로.
- 실물: 기준 run.yaml·원천·두 판정서·명세·로그·요청/응답 6벌, CIM-FP-3 donor 명세·통합 자료, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.