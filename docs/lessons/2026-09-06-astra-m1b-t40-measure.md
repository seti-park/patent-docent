# 독립 감수 원문 — M1b 설계 도전 1차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v1 · 판정 REVISE(BLOCKER 1 · HIGH 9 · MED 3)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `28ed1a0bdd492d6457c605d164986ee1d24e9f6524205e31f49d8ecb2c022cc6` · 22451 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 04:47:39 → 05:01 · **USAGE = input 2,723,119(cached 2,565,248) · output 22,680(reasoning 7,523)**. 사본 `~/projects/workspaces/pd-m1b-t40`(detached `1880ae8` · `bundle/T40-MEASURE-DESIGN.md` v1 sha256 `3a4818be…9be2` · 구동·Workflow·지표 스크립트 3종 + 기준 런 봉투 동봉 · `origin/t40-r1` `8b678cb` · `origin/t40-r2` `57f0414` fetch). 대상 = 재정 T40 ④ A(3 런 좌석 비교 실측)의 총괄 설계. 도전자는 계측 커밋 blob·부모·전체 diff · `lane_profiles` · sonnet aliases · 기준 런 163 항목·anchor 51/5·45/5 · 조기/완주 축 동일성 · 기준 봉투 검증기 통과를 직접 재실측했고, 러너 제어 흐름(쓰기 대체)·구동 exit 코드·지표 추출기·Workflow 본문을 메모리 반례로 반증했다.

**판정 = REVISE · 13건(BLOCKER 1 · HIGH 9 · MED 3) · 기각 0 · 전부 발주자 귀책.** **MY-1 HIGH**: 재정 §4 「같은 절차 문서」 — R0 가 현재 main 의 절차 본문(`d4e6ca2` 뒤 개정)을 쓰면 09-01 과 프롬프트가 다르고 그것을 재정 이행으로 분류할 수 없다 · R0 핀도 「개시 시점 HEAD」라 셋이 계약 값만 다르다는 보장이 없다 → 고정 핀 + 같은 절차 본문. **MY-2 MED**: 문언 이동이 잡음 폭을 「반드시 넓힌다」는 방향 주장은 틀렸다(상쇄 가능 · CLI→Workflow 차이도 혼재). **MY-3 BLOCKER**: 27 항목 비교의 **대응 단위·짝짓기 규칙·분할/병합/누락/추가 채점 처분**이 없다 — `M<n>` 순번 대응은 의미 대응이 아니다(재번호는 투입 순서). **MY-4 HIGH**: 「종속항 표본 10건」을 addition 10건으로 바꿨다(기준 런에 적용하면 청구항 9개 · CL-18 중복 · 반올림 구현 미정). **MY-5 HIGH**: 「통합 항목 수」에 기계 수확 fact(11 = quoted 7 + bibliographic 4)를 섞었다 — synthesize 응답의 fact 는 3. **MY-6 HIGH**: 수렴 축 범위(`dependent-set` 누락) · count 축 비교 타입 · 채택 회차(추출기가 `convergence.json` 우선 · 조기 재시도가 같은 파일을 덮어씀) 미완결. **MY-7 HIGH**: 추출기가 `check_id` 만 키로 삼아 실행별 조기 검사 행(read-a fail · read-b pass)을 덮어 지운다. **MY-8 HIGH**: exit 11 이 「봉투 가능한 대기」를 뜻하지 않는다 — 출구 실패(`full` · 종결)와 조기 대기(`awaiting`)가 같은 코드 · 조기 exact-match·청구항 실패도 `awaiting: convergence_continue` 로 돌아온다. **MY-9 HIGH**: 러너는 read-a 가 `LanePending` 이면 즉시 반환해 read-b 요청을 아직 만들지 않는다 — 첫 배치는 6 이 아니라 **3**(A-a → 엔진 → A-b). **MY-10 HIGH**: Workflow 결과의 `wrote:false` 도 truthy 라 「완료」로 세고 · `dropped` 에 run 이 없어 세 런의 같은 `lane_id` 를 구별 못 하고 · 응답 경로 중복 미거부 · 재발주가 기존 응답을 덮을 수 있다. **MY-11 HIGH**: `"model"` grep 건수는 실호출 대조가 아니고 · 「응답 삭제」는 P-12 시점 증거 파기. **MY-12 MED**: 보존 대상이 「완주 런」만이라 실패·대기 런 증거와 외부 구동 스크립트·args·transcript 가 빠진다. **MY-13 MED**: `shadow_root` 는 「합성 픽스처 전용 우회」가 아니라 일반 누적 루트 지정 · 6→9 는 세 런 모두 메모 보유 종결 시의 예상.

지적 열거 = MY-1, MY-2, MY-3, MY-4, MY-5, MY-6, MY-7, MY-8, MY-9, MY-10, MY-11, MY-12, MY-13

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17**. **전부 수용 → 설계 메모 v2 + 계측 베이스 커밋(절차 본문 = `d4e6ca2` 판) + 스크립트 4종 개정 → M1b 2차 도전(지적 `MZ-*`)** — BLOCKER 가 있으므로 재도전 없이 착수하지 않는다.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

계측 커밋의 blob·부모·좌석 변경과 기준 런 계수는 맞습니다. 그러나 현재 설계는 **27항목 비교의 대응 단위가 없고, 종속항 표본 단위를 바꾸며, 지표 추출에서 조기 실패를 지울 수 있습니다.** 실행 배치와 종료 코드도 실제 러너와 어긋납니다. 이 상태로 실측을 시작하면 결과 표를 재정 ①②의 근거로 그대로 사용할 수 없습니다.

대상 확인: 사본 마커의 path·pin·order·disposable 전부 일치, HEAD `1880ae8ec6a43b66611ef298a0ae1569a3077708`, 메모 SHA-256 `3a4818be06a1fb66a123bd1fce368ed8036603fcbb6b3dbbd841d7073a6b9de2`.

좌표의 약칭은 [메모]( /home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md), [구동]( /home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py), [Workflow]( /home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_lanes.workflow.js), [지표]( /home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py)입니다.

**지적 목록 — BLOCKER 1 · HIGH 9 · MED 3**

**MY-1 · HIGH — ‘같은 절차 문서’의 불일치를 재정 이행으로 분류했다.**  
좌표: 메모 §1 법 이동·§2 런 표·§8 ⓖ; `ruling-20260905-05-T40.md:§4`.

원장은 「09-01 런과 같은 원천 · 같은 절차 문서」라고 적었습니다. 메모가 재정 문언으로 인용한 「계측 브랜치 = main에서 분기」는 §4에 없습니다. 실제 절차 본문은 바뀌었으며, 규약 값이 같다는 사실만으로 프롬프트 변경까지 승인받았다고 할 수 없습니다. 또한 R1/R2의 부모는 고정된 `1880ae8`인데 R0만 ‘개시 시점 main HEAD’여서, 실행 시점에도 계약 값만 다른 셋이라는 보장이 없습니다.

닫는 문안: **“R0는 `1880ae8`로 고정하고, 기준 런과 다른 절차 본문을 사용하는 비교의 허용 여부를 ‘같은 절차 문서’ 요건의 예외로 재정받기 전에는 개시하지 않는다.”**

**MY-2 · MED — 문언 이동이 잡음 폭을 반드시 넓힌다는 방향 주장은 틀렸다.**  
좌표: 메모 §1 법 이동·§8 ⓖ.

`|R0−B|`에서 실행 변동과 문언 효과는 상쇄될 수 있습니다. 예를 들어 B=10, 동일 절차 재런=12, 문언 효과=−1이면 폭은 2에서 1로 줄어듭니다. 현재 자료로는 ‘xhigh·sonnet 채택에 유리’도, ‘넓어졌다는 사실’도 확정할 수 없습니다. CLI→Workflow 변경도 함께 있어 차이를 절차 문언 효과로만 설명할 수 없습니다.

닫는 문안: **“이 폭에는 실행 변동·절차 본문·호출 환경 차이가 혼재하며 확대·축소 방향은 미확정이라고 기록한다.”**

**MY-3 · BLOCKER — 27항목의 비교 대응표가 없다.**  
좌표: 메모 §5 ㉤; `engine/stages/read.py:lane_payloads`, `renumber_items`.

7 positioning·20 implication은 **기준 런의 관측값**입니다. 새 R0/R1에서도 같은 수가 나올 의무는 없습니다. 같은 수가 나오더라도 런별 `M<n>` 오름차순은 의미 대응이 아닙니다. ID는 각 런의 항목 투입 순서로 다시 매겨집니다. 항목 분할·병합·누락·추가가 발생하면 어느 것을 짝짓고 무엇을 ‘열위 1건’으로 셀지 총괄이 실행 후 선택하게 됩니다.

닫는 문안: **“27개 비교 단위와 런 간 대응 기준, 분할·병합·누락·추가 및 대응 불가의 채점 처분을 실행 전에 확정하여 발췌 생성과 Owner 판독에 동일하게 적용한다.”**

**MY-4 · HIGH — ‘종속항 표본 10건’을 addition 10건으로 바꿨다.**  
좌표: 메모 §5 ㉦·§8 ⓘ.

기준 런에 명시된 규칙을 적용하면 다음 청구항이 뽑힙니다.

`CL-2, CL-4, CL-6, CL-10, CL-12, CL-15, CL-18, CL-18, CL-21, CL-22`

즉 **청구항 9개에서 addition 10개**입니다. CL-18은 두 번 세며, addition을 많이 분할한 청구항의 표본 비중이 커집니다. 이는 단순한 결정론 구현 선택에 앞서 표본 단위를 바꾸는 해석입니다. `round`도 구현 미정입니다. N=49이면 i=5에서 Python은 24, JavaScript는 25를 고릅니다.

닫는 문안: **“표본 단위를 종속 청구항 10건으로 고정하고 항 내 인용 판독·오답 집계와 반올림 규칙을 명시하며, addition 10건으로 변경하려면 그 단위 변경을 재정받는다.”**

**MY-5 · HIGH — ‘통합 항목 수’에 기계 수확 항목을 섞었다.**  
좌표: 메모 §5 ㉣; `bundle/t40_metrics.py:metrics/synth_counts`(39행); `engine/stages/read.py:lane_payloads`.

실측:

- 최종 명세 fact: **14**
- synthesize 응답 fact: **3**
- 차이: `quoted` 7 + `bibliographic` 4 = **기계 수확 11**

따라서 `synth_counts.fact=14`는 통합 레인이 낸 항목 수가 아닙니다. 접지 인용에 따라 변하는 수확량까지 통합 수로 계산하면 ①의 해당 지표와 잡음 폭이 달라집니다.

닫는 문안: **“㉣은 채택된 synthesize 응답의 kind별 항목 수로 추출하고, 수확 fact와 최종 명세 전체 fact 수는 별도 참고 행으로 기록한다.”**

**MY-6 · HIGH — 수렴 축의 범위·회차·판정 타입이 완결되지 않았다.**  
좌표: 메모 §5 ㉠; `bundle/t40_metrics.py:metrics`(16–22행); `engine/stages/read.py:run` 조기 판정서 기록·attempt 기입.

㉠에는 `dependent-set`이 빠져 있습니다. 추출기는 그 축을 출력하므로 **메모의 채택 조건과 추출 결과의 범위가 다릅니다.** count축의 `pass/fail`에 절댓값 식을 어떻게 적용할지도 정하지 않았습니다.

또 메모는 ‘조기 attempt 1’을 지정하지만 추출기는 `convergence.json`을 우선하고 attempt를 버립니다. 러너는 조기 재시도 때 같은 `convergence-early.json`을 다시 쓰며, 완주 판정서 attempt는 **후속 판정점 회차**입니다. 따라서 ‘완주 attempt 1’을 ‘첫 조기 판정’으로 사용할 수 없습니다.

닫는 문안: **“수렴 6축의 비교 타입과 채택 회차를 명시하고, 최초 조기 판정은 재시도 전 별도 보존하여 phase·attempt·digest와 함께 추출한다.”**

**MY-7 · HIGH — 조기 검사 실패가 추출 과정에서 사라진다.**  
좌표: `bundle/t40_metrics.py:metrics/checks`(22행); `contracts/stages/read.yaml:retry_budget`; 메모 §4·§5 결과 표.

현재 조기 판정서는 `read-a`와 `read-b`에 같은 검사 ID를 각각 싣습니다. 추출기는 `check_id`만 키로 삼아 앞 행을 덮습니다. 메모리 반례에서:

```text
INPUT [('read-a', 'fail'), ('read-b', 'pass')]
OUTPUT {'read.claim-inventory': {'status': 'pass', 'checked': None, 'violations': 0}}
```

기준 런의 조기 검사에는 이 두 실행별 청구항 검사 행이 없어서 기준값 재실측만으로는 드러나지 않는 결함입니다.

닫는 문안: **“검사 행은 배열 또는 `(check_id, read_run)` 복합 키로 보존하고, 실행 귀속·findings·조기 게이트 차단 사유를 결과 표에서 누락하지 않는다.”**

**MY-8 · HIGH — exit 11은 재호출 가능한 조기 대기를 뜻하지 않는다.**  
좌표: 메모 §2 종결 재호출·§4; `bundle/t40_drive.py:cmd_read`(121행); `engine/stages/read.py:run`, `_run_is_terminated`.

구동 함수는 모든 non-ok 반환을 exit 11로 바꿉니다. 직접 대체 실행에서 `early/escalate`, `full/escalate`, `full/halt`가 모두 11이었습니다. 그러나 출구 실패도 `phase: full` 판정서를 남기고 종결하므로 재호출하면 G-5가 막습니다.

반대로 조기 exact-match·청구항 실패도 현재 러너에서는 `terminated:false`, `awaiting:convergence_continue`로 돌아옵니다. 따라서 awaiting 표지만으로 봉투 적용 가능 여부를 판단할 수도 없습니다. 메모의 ‘거기서 끝’은 운영상 중단과 엔진 종결을 구별해야 합니다.

닫는 문안: **“반환 phase·종결 근거·`phase-gate.blocked_by`로 성공 종결, 실패 종결, 봉투 가능한 대기, 봉투 불가 중단을 구분하고 각각의 종료 코드와 재호출 조건을 고정한다.”**

**MY-9 · HIGH — 첫 분해 배치 6개는 현행 구동으로 생성되지 않는다.**  
좌표: 메모 §3 배치 A·§7 시간; `engine/stages/read.py:run` 분해 루프, `_execute_decompose`; `engine/lanes/file_adapter.py:dispatch`.

러너는 `read-a`를 디스패치하다가 `LanePending`을 받으면 즉시 반환합니다. `read-b` 요청은 아직 만들지 않습니다. 쓰기를 대체한 실제 제어 흐름 검사에서도 첫 호출은 read-a 한 개, 그 응답을 공급한 다음 호출에서 read-b 한 개가 나왔습니다.

따라서 셋의 최초 합은 6개가 아니라 **3개**입니다. 현재 엔진을 유지하면 최소 순서는 `A-a → 엔진 → A-b → 엔진 → B → 엔진 → C`입니다.

닫는 문안: **“분해를 A-a 3개와 A-b 3개로 나누고 각 응답 수집 뒤 러너를 재호출하며, 재시도·대기 런이 섞일 때의 배치 편입 규칙과 시간 추정을 이에 맞춘다.”**

**MY-10 · HIGH — Workflow 완료와 응답 파일 완료를 혼동하며 재발주 좌표도 불완전하다.**  
좌표: 메모 §3 null 재배치; `bundle/t40_lanes.workflow.js:RESULT`, `results.filter(Boolean)`, `dropped`(38–40행).

`wrote:false`는 RESULT 스키마상 허용되지만 truthy 객체라 ‘완료’로 셉니다. 필수 필드를 모두 가진 보고로 재현했습니다. 또한 파일을 쓴 뒤 StructuredOutput 단계에서 실패하여 null이 되는 경우, 메모대로 같은 좌표를 재발주하면 이미 있는 응답을 다시 쓸 수 있습니다.

`dropped`에는 run이 없습니다. R0/R1/R2는 같은 `lane_id`를 사용하므로 어느 런의 실패인지 결과 자체로 식별할 수 없습니다. 중복 응답 경로 입력도 거부하지 않아 같은 파일의 동시 작성 경로가 열려 있습니다.

닫는 문안: **“상태 키를 `(run_id,lane_id)`로 하고 응답 경로 중복을 거부하며, 완료·재발주는 실제 파일의 존재·파싱·결속 검증 후 결정하고 기존 응답은 덮어쓰지 않는다.”**

**MY-11 · HIGH — 모델 검증 절차가 증거를 정확히 식별하지 못하며 실패 증거를 삭제한다.**  
좌표: 메모 §3 첫 배치 검증; `contracts/stages/read.yaml:lane.effort_evidence`, `round_trip_binding`; T14 §2 ⒝.

JSONL의 `"model"` 검색 건수는 실호출 대조가 아닙니다. 요청 문자열·반향·메타데이터를 구별할 이벤트/필드 좌표가 없고, 임의의 다른 모델이나 모델 증거 부재에 대한 전량 대조 규칙도 불완전합니다.

특히 ‘즉시 중단 · **응답 삭제** · 재발주’는 P-12의 시점 증거를 없앱니다. T14도 살아 있는 좌표의 응답 삭제를 보호 규율의 명시 해제가 필요한 행동으로 다뤘습니다. 잘못된 모델로 생성된 응답 역시 실패 증거입니다.

닫는 문안: **“런·레인별 실제 호출 이벤트의 model·effort를 기대값과 대조하고 미상·불일치는 소비 전에 중단하며, transcript와 응답을 보존한 채 재발주 처분을 정한다.”**

**MY-12 · MED — 보존 계획이 실패 표본과 호출 증거를 빠뜨린다.**  
좌표: 메모 §6 1·2·4; §2 외부 구동 경로·§3 transcript.

보존 대상은 ‘완주한 런 3건’인데 설계 자체가 조기 중단·대기를 허용합니다. 실패한 런의 요청·응답·판정서까지 결과 표의 근거로 영구 보존한다는 규칙이 없습니다. 외부 구동 스크립트·Workflow 실제 실행본·args·호출 transcript도 런 폴더 복사에 자동 포함되지 않습니다. `run.yaml.engine.commit`은 이 외부 실행층을 결박하지 않습니다.

닫는 문안: **“성공·실패·대기 전 런의 증거와 실제 사용한 외부 스크립트·args·transcript를 해시 목록으로 함께 보존하고, 원장 추가분의 보존 시점도 명시한다.”**

**MY-13 · MED — 섀도 원장의 기능 범위와 예상 행 수를 사실보다 좁고 확정적으로 적었다.**  
좌표: 메모 §2 섀도 원장·§8 ⓓ; `engine/paths.py:shadow_ledger_root`; `engine/stages/read.py:append_screening_ledger`.

`shadow_root`는 ‘합성 픽스처용 우회’가 아닙니다. 두 함수의 문언은 **일반적인 누적 루트 명시 지정이며 테스트 격리는 사용자 하나**라고 명시합니다. 생산 원장을 선택하는 판단 자체는 허용되는 운영 선택입니다.

또 6→9는 세 런 모두 메모를 가진 채 종결할 때의 예상입니다. 조기 대기는 추가하지 않고, 메모 없는 조기 예외는 append 함수가 행을 만들지 않습니다.

닫는 문안: **“생산 원장은 이번 실측의 명시적 운영 선택이며, 누적량은 메모를 보유한 종결 런 수로 산출하고 6→9는 세 런 모두 해당할 때의 예상으로 표기한다.”**

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합** | **REVISE** | 같은 절차·27항목·표본 단위·통합 계수의 피복 불완전 |
| **B 계측 커밋** | **PASS — 검증한 정적 범위** | blob·부모·전체 diff·프로필·Sonnet aliases 일치. 실제 Workflow 호출은 미검증 |
| **C 구동 정합** | **REVISE** | 서명·lanes_dir는 맞음. 배치 생성·exit·종결/대기 구별은 MY-8·9 |
| **D 법 이동** | **규약 값 변경 없음 확인; §1 해석은 REVISE** | 경계·부착 순위 유지. 변경된 입력의 허용 근거와 잡음 방향 주장은 MY-1·2 |
| **E 임계 집행** | **REVISE** | MY-3~7. 정상 기준 산출의 조기/완주 축 동일성은 확인 |
| **F 레인 스크립트** | **REVISE** | MY-10~12. 명시 프롬프트에 타 런 응답을 제공하는 코드는 없음 |
| **G 결정 공백** | **REVISE** | 항목 대응·표본 단위·회차 선택·실패/재발주·증거 보존이 실행 후 선택으로 남음 |

A의 요소별 피복은 다음과 같습니다.

| 재정 요소 | 피복 |
|---|---|
| 3런 및 R0/R1/R2 좌석 구성 | **covered** — 현재 커밋 기준 |
| 같은 소재·원천 | **partially** — 사본 정본화 원천은 일치, 외부 투입물 미검증 |
| 같은 절차 문서·계약 값만 다른 비교 | **partially** — MY-1 |
| Workflow `{model, effort}` 하드 지정·fork 금지 | **partially** — 호출 옵션 존재, 실행 증거·재발주 규칙 미완 |
| ① 기계 지표와 잡음 폭 | **partially** — 식 자체는 맞으나 추출·범위 문제 |
| ① 27항목 열위 ≤3 | **partially** — 임계는 있음, 비교 단위 대응 규칙은 **missing** |
| ② 종속항 anchor 분포 | **covered — anchor_state 조합 계수라는 해석 범위** |
| ② 종속항 표본 10건·오답 ≤1 | **partially** — MY-4 |
| 미달 시 결과 표 재상신·자동 현행 유지 금지 | **covered** |
| Owner 발췌 두 건·CP1 전체 재독 제외 | **covered**, 발췌 구성 규칙은 미완 |
| M2b-1·2 뒤 실행·`partial/read` | **covered** |

§8 자기 신고의 격은 **ⓐⓑⓒⓗⓙⓚⓛ는 운영 재량**, **ⓔ는 명시한 대로 별도 재정 필요**, **ⓕ는 재정 이행**으로 봅니다. ⓒ의 증거 자산 반입과 ⓓ의 생산 원장 사용 자체를 금지하는 근거는 찾지 못했습니다. 다만 ⓓ의 사실 설명은 MY-13, ⓖ의 ‘재정 문언 이행’ 분류는 MY-1, ⓘ의 ‘단순 표본 구현 재량’ 분류는 MY-4로 뒤집습니다. ⓚ의 런 표기는 원장이 맹검을 명하지 않았으므로 독립적인 위반으로 판정하지 않았습니다.

**검증 경로와 출력**

모든 셸 명령의 cwd는 지정 사본이었습니다. Python은 전부 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`으로 실행했습니다.

| 실행 명령·경로 | 출력 확인 — 마지막 줄 또는 마지막 결과 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 마지막 줄 `1880ae8ec6a43b66611ef298a0ae1569a3077708`; 마커 4필드 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `3a4818be06a1fb66a123bd1fce368ed8036603fcbb6b3dbbd841d7073a6b9de2  bundle/T40-MEASURE-DESIGN.md` |
| `git ls-tree HEAD contracts/stages/read.yaml` | `ea238e574d3cc7a71ae0547a1a4556b92e6dfc63` |
| `git ls-tree origin/t40-r1 contracts/stages/read.yaml` | `003f16ced570089d70428286af46bb9922141c34` |
| `git ls-tree origin/t40-r2 contracts/stages/read.yaml` | `745cc34c7b86e6b8786e198efb4740440c95e99c` |
| `git diff HEAD origin/t40-r1`、`git diff HEAD origin/t40-r2` | 전체 diff에서 각각 해당 좌석 두 값만 변경 |
| `git diff --numstat HEAD origin/t40-r1` 및 R2 | 둘 다 마지막 줄 `2	2	contracts/stages/read.yaml` |
| `git diff d4e6ca2 HEAD -- reader/procedure/` | 파일별 후속 판독 포함. 경계 3행·element 7행·부착 순위 4행은 구/신 바이트 동일 |
| `…/python bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory` | exit 0, 마지막 줄 `]`; 아래 계수와 일치 |
| `…/python -c`에서 JSON 독립 재계수·SHA 재산출 | 마지막 줄 `envelope_digest 90dca50a682181f3bfc738aa75e46ef1bbf83bf548067be2617f73e69d39c8c4` |

독립 재계수 결과는 **163항목 = component 56·grounding 56·fact 14·implication 20·positioning 7·figure_note 10**, 전체 anchor **51/5**, 종속 addition anchor **45/5**, 레인 **6**, mismatch·rejected·retry **각 0**, 출구 검사 **13행 전부 pass·위반 0**입니다. 원천은 **298,507 B**, SHA-256 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`였습니다. PATENT_META 값도 기준 런과 일치했습니다.

추가 반증은 다음 방식으로 실행했습니다. 아래 대체 실행은 실제 레인 호출이나 파일 쓰기를 하지 않았습니다.

| 호출한 실물 함수·대체 범위 | 마지막 출력 또는 핵심 결과 |
|---|---|
| `lane_profiles('.')` 직접 호출. 브랜치는 `git show`로 읽은 YAML을 로더 반환값에만 주입 | 두 부모 모두 `1880ae8…`; R1은 decompose/synthesize xhigh, R2는 ground-dependent sonnet/high |
| `LaneResponse.mismatches`에 계약 aliases 대조 | Sonnet 라벨·API ID·`[1m]`·`sonnet` 모두 False, `claude-opus-4-8` True |
| `plan_decompose`, `plan_grounding`, `LaneRequest.input_digest` | 마지막 결과: R2에서 지문이 바뀐 좌표는 종속 접지 batch-0·1 두 개 |
| 기준 payload로 `decompose_only_spec`, `assemble_spec`, `early_convergence_row` 재계산 | `current code early/full axes equal True` |
| `check_lane_log_shape`에 Sonnet 배정 행 대입 | `sonnet shaped log pass 0` |
| `continue_envelope_state` 실제 기준 봉투 검증 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `read.run`의 쓰기 함수·진입/종결 검사를 대체하고 pending 어댑터로 제어 흐름 관찰 | 최초 pending은 read-a 하나, 다음 pending은 read-b 하나 |
| `cmd_read`에 early/full 반환값 대입 | `exit 11 does not imply awaiting or nontermination` |
| `metrics`에 실행별 조기 실패/통과 행 대입 | `read-a failure overwritten by read-b pass` |
| Node AsyncFunction으로 Workflow 본문 구문 검사·agent/pipeline 대체 | `all RESULT required fields present; false wrote still counted complete` |

조기·완주 수렴 축은 기준 파일끼리도 동일했고 현행 조립기 재계산에서도 동일했습니다: element-set **1**, tree-edges **1/11**, dependent-set **1**, addition-attachment **0.6724137931034483**. 이는 MY-6의 **최초 회차 선택 결함을 해소하지 않습니다.**

**[미검증]**

- 외부 스테이징 원본 TXT·도면 20개·MAPPING 부재는 사본 밖이므로 확인하지 않았습니다. 사본의 정본화 특허 본문만 해시를 확인했습니다.
- 최초 무쓰기 제어 흐름 검사는 사본의 `figures-raw` 부재 때문에 진입 지문 검사에서 멈췄습니다. 이후 배치 순서 검사에서는 그 진입 검사와 종결 검사를 명시적으로 대체했습니다. 실제 런 재개 성공 시험으로 주장하지 않습니다.
- Workflow 도구가 현재 도구 목록에 없어 실제 `agent()` 기동, 모델/effort transcript 형식, 세션 문맥 주입, 실제 파일 접근 경계는 검증하지 못했습니다. Node 검사는 구문·분기 검사입니다.
- 브랜치 파일은 checkout 없이 메모리로 검증했습니다. 해당 브랜치의 실물 worktree에서 실행한 것은 아닙니다.
- 실제 봉투 발행 후 파일을 쓰는 재호출, 생산 원장 append, 동시 파일 쓰기 시험은 수행하지 않았습니다.
- 09-01 CLI 기동 사실·실호출 effort·시간·실제 토큰 사용량·가용 메모리는 이 사본의 확인 자료만으로 검증하지 못했습니다. 요청서 크기는 확인했습니다.

**읽은 파일**

- 상류: `docs/decisions/ruling-20260905-05-T40.md` 전문, `docs/SPEC.md` 해당 §8.4 행, `contracts/run-kinds.yaml`, `contracts/stages/read.yaml` 지정 블록.
- 봉투·종결: `ruling-20260901-05-T14.md`, `ruling-20260901-08-T17.md`, `ruling-20260905-03-T38.md`, `contracts/schemas/approval-envelope.schema.json`, `bundle/baseline-convergence-continue.md`.
- 대상: `bundle/T40-MEASURE-DESIGN.md`, `bundle/t40_drive.py`, `bundle/t40_lanes.workflow.js`, `bundle/t40_metrics.py`.
- 구현: `engine/stages/source.py`, `engine/stages/read.py`, `engine/stages/__init__.py`, `engine/lanes/plan.py`, `engine/lanes/contract.py`, `engine/lanes/file_adapter.py`, `engine/paths.py`, `engine/gitpin.py`, `reader/lib/convergence.py`, `reader/lib/run_checks.py`, `reader/lib/rules.py`, `tools/run_worktree.py`의 관련 앵커.
- 절차: `reader/procedure/` 전체 변경 diff와 관련 본문·HISTORY, 구 핀의 `10-decompose.md`; 규약 로더가 읽은 `reader/reader-rules.yaml`.
- 기준 런: `run.yaml`, `00-source/patent.md`, 두 convergence JSON, material-spec JSON, lane-log JSON, 분해·접지·통합 응답 JSON 6개, synthesize 요청서의 계약·지시·절차 부분 및 요청서 6개의 전체 바이트 계측.
- 보조: `.audit-sandbox`, `.gitignore`, 사본의 `ledgers/shadow/screening.jsonl`, `D-20260905-02-pdm2b-seats.md` 관련 기록.

파일·임시물·캐시를 만들지 않았으며, 실제 실측 레인은 시작하지 않았습니다.