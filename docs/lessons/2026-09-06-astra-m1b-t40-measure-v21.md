# 독립 감수 원문 — M1b 설계 도전 21차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v22 · 판정 REVISE(HIGH 1 · MED 5)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `e00d15510ee115210febf0f58175d01f2b9a07bcac452d1bd13d404248d2cfb6` · 21723 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v21/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `65551a4` · 마커 3항 일치 · 메모 v22 sha256 `db17fc8d…` · v1~v21 + 회귀표 v2 + 자문 봉투·회신 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 21회」 명기(L-055 조항 이행). 폐쇄 = **이전 71건 closed 62 · partially 9 · open 0**. **B·C·E·F PASS**(16회 연속). 회귀표 55 사례는 도전자 재실행에서도 전건 PASS.

**판정 = REVISE · 6건(HIGH 1 · MED 5) · 기각 0 · 발주자 귀책.** **NS-1 HIGH**: 스냅샷의 상세 축(`convergence_detail.axes`) 값만 바꾸고 보고 축·status 를 두면 모순 축 값이 R1 정상 지표로 출력됨 — 러너는 같은 axis_rows 를 상세·보고에 넣고 status 는 policy·threshold·계수/Jaccard 에서 나온다. **NS-2 MED**: NR-1 의 대소 조건은 지웠지만 각 판정점 회차의 결속(예산·요청 좌표·S≤E)이 없어 attempt 999·S 2 > E 1 이 통과. **NS-3 MED**: mismatch 소비 행을 예외 종결에만 허용 → `_dispatch` 가 기록 후 반환하고 `LaneAssignmentError` 는 정본 후속 뒤라 그 사이 LanePending 이 합법인데 거부. **NS-4 MED**: 재제조한 L 행에도 러너 경로와 다른 부모(포인터 root 필드 None · 대기 런의 미도착 요청 부재 · 청구항 검사 checked 6 복사 · E 2 런의 8행 부재). **NS-5 MED**: 포인터 `appended` 필수·bool 미검증 → 결측·문자열로 NR-4 원장 대조 우회. **NS-6 MED**: `--law-tree` 문서가 허용한 d4e6ca2 worktree 는 09-01 엔진(가드 함수 없음)이라 실행 불가 · 지정 트리 검증이 디렉터리 존재뿐.

지적 열거 = NS-1, NS-2, NS-3, NS-4, NS-5, NS-6

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 21**. **전부 수용 → 지표 v23 + 회귀표 v3**(판정서 내부 정합 재도출(NS-1) · 회차 상한 결속(예산 · retry 발번 · S≤E)(NS-2 · 러너 실측: 청구항 재시도는 조기 수렴 회차를 올리지 않아 등식이 아니라 상한) · mismatch 행은 대기·예외 종결 양쪽 허용·완주와만 공존 불가(NS-3) · **회귀표 L 행을 실제 `read.run` + `FileLaneAdapter` 실행으로 생성**(응답 조작 · IO 결함 주입 · 실측과 같은 다단 호출: 1차 상신 대기 → `t40_envelope.py` 봉투 → 2차 · 61 사례 전건 PASS)(NS-4) · 포인터 필수 필드 7 + 타입(NS-5) · `--law-tree` 내용 핀 = 절차 문서 5 파일 sha256 + 실행 코드·계약 바이트 동일 · d4e6ca2 worktree 문안 제거(NS-6)) → **M1b 22차 도전(지적 `NT-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 21회)

**이전 71건의 폐쇄 판정은 closed 62 · partially 9 · open 0입니다.** 외부 자문은 동봉 회신과 §17 처분표상 이미 회신·반영됐습니다. 계수는 이어갑니다.

회귀 55사례는 메모리 재실행에서 전건 PASS였습니다. 그러나 **서로 모순되는 수렴 축 값을 R1의 정상 실측값으로 출력하는 통로**가 남았습니다. 회차 검증·합법 상태 구별·회귀 부모·포인터·법 트리에도 잔여가 있어 착수 근거로 사용할 수 없습니다.

**A — MY~NR 폐쇄표**

`partially`는 기존 지정 변형의 차단과 원 지적의 요구 전체 충족을 구별한 판정입니다.

| 회차 | closed | partially | 잔여 |
|---|---|---|---|
| MY | MY-1~5·7~13 | MY-6 | 축 값·판정·회차의 정합: NS-1·2 |
| MZ | MZ-1·2·4~9 | MZ-3 | 선등록 회차 결속: NS-2 |
| NA | NA-1~7 | — | 지정 반례 차단 |
| NB | NB-1~3 | — | 지정 반례 차단 |
| NC | NC-1~3 | — | 지정 반례 차단 |
| ND | ND-1~2 | — | 소견 형태·검증 바이트 재사용 유지 |
| NE | NE-1~2 | — | 판정서·finding 스키마 검증 유지 |
| NF | NF-1 | — | 완주 run_id 결속 |
| NG | NG-1~2 | — | 명세 run_id·판본 표기 |
| NH | NH-1~2 | — | 왕복 결속·baseline 제한 |
| NI | NI-1~2 | — | 요청 지문·원천 지문 사슬 |
| NJ | NJ-1 | — | 원천 부재 거부 |
| NK | NK-1 | — | 필수 필드 결측 거부 |
| NL | NL-1 | — | 집합 전량 결측 거부 |
| NM | NM-1~2 | — | 검사·로그 결측 및 원천 단일 읽기 |
| NN | NN-1·2·4 | NN-3 | 합법적 mismatch 대기 오거부: NS-3 |
| NO | NO-3 | NO-1·2·4 | 대기·생성 불가능 상태·포인터: NS-1·3·5 |
| NP | NP-1~3 | — | 지정 실패·소비·종결 반례 차단 |
| NQ | NQ-1~3 | — | 거부 형식·원장 종결·소견 합계 |
| NR | NR-3·5·6 | NR-1·2·4 | NS-2~5 |

§8의 격 구분은 유지할 수 있습니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 이행입니다. ⓘ의 청구항 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표시는 구현 재량입니다.

**지적 목록 — HIGH 1 · MED 5**

**NS-1 · HIGH — 같은 판정서 안에서 모순되는 축 값을 정상 임계 지표로 출력한다.**

좌표: 메모 §5 ㉠·생성 불변식; [t40_metrics.py:validate_verdict](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:133), `axes_of`; `reader/lib/convergence.py:check`, `run_checks.py:to_convergence_payload`.

정확한 R1 ID·핀·partial/read·xhigh 요청 재렌더·dispatch 결속을 가진 메모리 대조군은 `complete`로 통과했습니다. 여기서 **스냅샷의 `convergence_detail.axes[tree-edges].jaccard`만 1.0으로 바꾸고 sidecar를 갱신**했습니다. 보고 축·상신 목록·status는 원본을 유지했습니다.

```text
R1_POSITIVE_CONTROL 0 complete
R1_WRONG_AXIS_ACCEPTED 0 complete gdm-wo2026128750a1-t40-r1
출력 축: jaccard=1.0, status=escalate, threshold=0.95
출력 상신: tree-edges, jaccard=0.09090909090909091, threshold=0.95
```

러너의 수렴 검사는 **동일한 `axis_rows`를 상세와 보고에 넣습니다.** 이 두 값이 다른 판정서는 해당 생성 코드가 만들지 않습니다. 또한 1.0≥0.95인데 escalate인 것도 정책과 모순입니다.

별도 반례에서는 **독립항 계수 `[1,999]`와 exact-match `pass`**도 `complete`로 수용했습니다. 현재 검사는 수치의 타입·범위만 확인하며, 계수·status·정책·보고 사이의 관계를 검증하지 않습니다. 이는 ①의 실제 비교값을 바꿉니다.

**고치는 문안:** “S·E·full의 상세 축과 보고 축을 동일하게 대조하고, 고정 규칙의 policy·threshold 및 계수/Jaccard로부터 status·상신 목록·수렴 실패 소견의 정합을 검증하여 모순은 계수 전 exit 4로 거부한다.”

**NS-2 · MED — NR-1의 대소 조건은 지웠지만, 각 판정점의 회차 검증은 구현하지 않았다.**

좌표: 메모 §5·§9 D①; [t40_metrics.py:306](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:306), 325·368행; `read.run:early_convergence_attempt`, `tail_attempt`.

실제 `read.run`의 첫 조기 수렴에 실패를 주입한 시험은 다음처럼 통과했습니다.

```text
ACTUAL_RETRY_RUNNER ok
ACTUAL_COUNTERS 2 1
ACTUAL_RETRY_METRICS 0 complete
```

따라서 **이전의 합법 완료 오거부는 수정됐습니다.** 그러나 NR-1 원문은 대소 조건 제거에 더해 **각자의 회차·예산·요청 좌표 검증**을 요구했습니다. v22는 실행 회차에 사실상 `int ≥1`만 요구합니다.

```text
FULL_ATTEMPT_999       0 complete
E_S_ATTEMPT_999        0 complete
S_ATTEMPT_AFTER_E      0 complete
```

마지막 사례는 S=2·현재 E=1입니다. 서로 다른 조기/출구 계수를 비교한 반례가 아니라 **같은 조기 판정점의 보존본과 현재본**을 뒤집은 사례입니다. 재시도 없는 요청·로그를 그대로 둔 회차 999도 통과했습니다.

**고치는 문안:** “조기·출구 회차는 각각 계약 예산과 해당 분해·후속 요청/소비 좌표에 결속하고 S의 최초 관측 회차와 현재 E의 관계를 검증하되, 조기와 출구 사이의 대소 조건은 두지 않는다.”

**NS-3 · MED — mismatch 행을 예외 종결에만 허용하여 러너가 실제로 남기는 대기 상태를 거부한다.**

좌표: 메모 §5 ‘거부·불일치·응답 짝 없음’; [t40_metrics.py:448](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:448); `read._dispatch`, `read.run:2040`.

실제 `FileLaneAdapter`와 `read.run`에 read-a 분해 응답의 모델 불일치를 주고 read-b 응답을 미도착으로 뒀습니다. 파일 출력은 메모리로 받았습니다.

```text
RUNNER_EXCEPTION LanePending … read-b/decompose/batch-0
REAL_POINTER terminated=False, appended=False, memo_count=0
REAL_ROWS [('read-a/decompose/batch-0', True)]
ACTUAL_MISMATCH_PENDING_METRICS 4
```

거부 사유는 “consumed·mismatch 행은 예외 종결 런에만”입니다.

`_dispatch`는 mismatch 응답을 기록하고 반환합니다. **`LaneAssignmentError` 검사는 정본 후속 실행 뒤**에 있으므로 그 전에 다른 레인이 `LanePending`을 내면 비종결 포인터와 mismatch 소비 행이 함께 남습니다. 반향 거부·응답 짝 없음의 즉시 예외 경로를 mismatch에 일괄 적용할 수 없습니다.

이 반례는 불일치 모델을 채택하라는 뜻이 아닙니다. **정직하게 남은 불일치·대기 증거를 손상으로 오분류**한다는 뜻입니다. §3의 소비 전 실호출 확인 절차는 별도로 유지해야 합니다.

**고치는 문안:** “반향 거부·응답 짝 없음과 mismatch 소비의 중단 위치를 구별하여, mismatch 뒤 LanePending·조기 대기는 불일치 이력과 사유별 N/A로 보존하고 정상 통합 지표의 적격성은 부여하지 않는다.”

**NS-4 · MED — 재제조한 L행에도 실제 생성 경로와 다른 부모가 남아 있다.**

좌표: 메모 §5·§9 D②; [t40_regress.py:Fx.to_pending_synth](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_regress.py:78), `to_claim_fail_wait`, `synth_early`, `l15`; `T40-REGRESS-TABLE.md`.

55사례의 기대 결과는 재현했습니다. 그러나 다음 부모는 **러너 경로의 증명**이 되지 않습니다.

| 부모 | 실제 불일치 |
|---|---|
| L02·L13·L14 | `root_source/root/ledger=None`으로 제조. 정상 `_write_shadow_pointer`는 미기입 대기에서도 원장 위치를 채움 |
| L13 | 청구항 실패→분해 재시도 대기인데 접지·통합 요청서가 이미 존재하고, 실제 미도착 `decompose/retry-1` 요청은 없음 |
| L13~L15 | `synth_early`가 청구항 검사들의 checked를 기준 input-digest의 **6**으로 복사하고 순서도 재배열 |
| L15 | E·S만 attempt 2로 바꾸고 재시도 요청·소비 행은 만들지 않음 |

실제 청구항 실패→재시도 대기의 산출은 다음이었습니다.

```text
ACTUAL_CLAIM_FAIL_PENDING ['read-a/decompose/retry-1/batch-0']
검사 순서·checked:
input-digest 1
claim-inventory 25 / dependency-parse 24
claim-inventory 25 / dependency-parse 24
ACTUAL_E5_METRICS 0 in-progress
```

실제 E=2/full=1 런에는 분해 `retry-1` 소비 행 두 개가 추가되어 **8행**이 있었지만 L15는 기존 **6행** 그대로입니다.

NR-2에서 요구한 청구항 실패↔수렴 실행 및 E 존재 관계는 수정됐습니다. `to_exception_terminated`의 full 부재·메모 2·종결 포인터라는 핵심 조합도 해당 후반 예외 경로와 맞습니다. 다만 **모든 L행을 검증된 합법 부모로 삼았다는 주장은 아직 성립하지 않습니다.**

**고치는 문안:** “L행은 실제 read.run의 판정·요청·로그·포인터 기록을 함께 수집해 만들고, 회차·검사 순서/checked·도달 전 요청 부재를 확인한 부모에서만 C행을 파생한다.”

**NS-5 · MED — `appended`의 필수·bool 검증이 없어 NR-4의 원장 대조를 우회한다.**

좌표: 메모 §5 포인터 무결성; [t40_metrics.py:262](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:262); `read._write_shadow_pointer`.

C39·C40은 정상적으로 exit 4였습니다. 하지만 필수 필드 검증은 완결되지 않았습니다.

```text
PTR_APPENDED_ABSENT         0 complete
PTR_APPENDED_STRING         0 complete
PTR_REQUIRED_ROOTS_ABSENT   0 complete
```

추가로 완주 판정서 없는 예외 종결 자료에서 `appended`를 삭제하고 memo_count를 999로 바꾸면, 실제 원장 memos는 2인데도 다음처럼 통과합니다.

```text
NO_APPENDED_MC999 (0, 'terminated-incomplete')
```

대조가 `appended is True`에 걸려 있지만 그 필드 자체의 존재·타입을 요구하지 않기 때문입니다. **대기 포인터 잔존 예외와 종결 포인터 손상은 구별해야 합니다.**

**고치는 문안:** “존재하는 포인터의 생성 필수 필드와 appended의 정확한 bool 타입을 먼저 검증하고, 종결 시 memo_count·appended·원장 메모 관계를 검사하되 비종결 잔존 포인터와 기준 런 역사적 다중행의 예외는 유지한다.”

**NS-6 · MED — `--law-tree`의 문서상 허용 판과 실제 실행 가능한 판이 다르며, 지정 판도 확인하지 않는다.**

좌표: 메모 §5 법 트리·§9 D③; [t40_metrics.py:215](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:215), `law`.

문서는 기준 런의 `d4e6ca2` worktree 또는 `ad4c6c3`를 허용합니다. 절차 디렉터리 tree는 실제로 같습니다. 그러나 **검증 코드의 판은 같지 않습니다.**

d4e6ca2의 engine·reader·contracts를 Git blob에서 메모리로 적재하여 실행한 결과:

```text
HISTORICAL_D4_LAW
exit 4: module 'engine.stages.read' has no attribute '_run_is_terminated'
```

09-01 판에는 뒤에 도입된 G-5 함수가 없습니다. 반면 ad4c6c3 절차와 현재 동일한 엔진·검사 코드 조합에서는 기준 추출과 요청 재렌더가 통과했습니다.

지정 트리 검사는 `reader/lib`·`engine` 디렉터리 존재뿐입니다. **Git 핀이 없는 메모리 트리도 `complete`로 수용**했고, 실행 코드·계약·절차가 선등록 판인지 검증하지 않았습니다. 실측 모드의 `--law-tree` 지정은 exit 4로 차단되어 이 제한은 맞습니다.

**고치는 문안:** “기준 추출용 검증 코드·계약·절차 조합을 실행 검증된 판으로 고정하고 그 핀/내용을 확인하며, d4e6ca2 절차 동일성과 d4e6ca2 엔진 실행 가능성을 구별해 지원하지 않는 호출 문안을 제거한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| A 원장 정합·폐쇄·격 | **REVISE** | 재정 해석은 유지 가능하나 지표·증거 집행에 위 잔여 |
| B 계측 커밋 셋 | **PASS** | 부모·전체 diff·blob·절차 tree·numstat·프로필·최초 요청 확인 |
| C 구동 v6 | **PASS — 정적·메모리 범위** | 분류·실제 enter 실패·증거 실패·스냅샷·조회/발주·상한 확인 |
| D 지표 v22·회귀표 v2 | **REVISE** | NS-1~6 |
| E 발췌 v4 | **PASS — 확인 범위** | 27단위·병합 후보 재사용·청구항 표본·판정 불가 처분 |
| F Workflow v4 | **PASS — 대체 실행 범위** | 사전 거부·하드 옵션·wrote/null 구별·보존 절차 |
| G 결정 공백 | **REVISE** | 모순 지표·오거부·법 트리 실패를 실행 중 사람이 선택적으로 우회해야 하는 상태 |

NR별로 보면 **NR-1은 오거부 수정만 완료**, **NR-2는 일부 생성 관계와 후반 예외 부모 수정**, **NR-3은 재렌더 결속 완료**, **NR-4는 정상 appended=true 경로의 계수 대조만 완료**입니다. **NR-5는 §2·§5 문언 일치**, **NR-6은 마커 3항 일치**로 닫혔습니다. NS-6은 NR-3 수정과 함께 추가된 법 트리 운용의 문제입니다.

새 좌석 값·임계 재정을 요구하는 지적은 없습니다. 기존 원장과 생성 코드에 맞춘 수정으로 닫을 수 있습니다.

**B — 직접 대조 결과**

- HEAD `65551a44db7dca15d8826bf42235c11d2e0ec1df`, 마커 path·pin·order·disposable 일치.
- 메모 SHA-256 `db17fc8d030c795f3214969474541be498c13c3e42119ddc07a4f0249c7c8d8f`.
- base 부모 `6d92cad`, R1·R2 부모 `ad4c6c3`.
- `6d92cad→base`는 절차 6파일뿐. R1·R2는 각각 read.yaml **2/2**뿐.
- d4e6ca2와 base의 절차 tree는 `d7717eb8750115a49e81ec7803790093b98c40ec`.
- read.yaml blob은 base `ea238e5…`, R1 `003f16c…`, R2 `745cc34…`.
- §0′의 계약·엔진·리더 **16파일 numstat 전부 일치**. `read.yaml 321/31`, `read.py 713/126`, `reader/lib/__init__.py 4/0` 포함.
- `lane_profiles()`는 R1 분해·통합만 xhigh, R2 종속 접지만 sonnet-5/high로 산출.
- 기준 요청 **6/6 재렌더 바이트 동일**, 신규 최초 분해 요청의 차이 필드 `[]`. 재시도 defects는 본문·지문을 변경합니다.

기준값도 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 재현됐습니다.

**D — 회귀표의 범위와 추가할 행**

동봉 C행의 대응은 다음과 같습니다. **55행 전건 PASS가 MY~NR 지정 반례 전수를 포함한다는 뜻은 아닙니다.**

| 동봉 행 | 대응 |
|---|---|
| C01~02 | 자문 A-01·NQ-2 원장 무결성 |
| C03~07 | 자문 A-02 요청/응답 메타·세 행 형식 |
| C08~13 | 자문 A-03 생성·파생 조건 |
| C14·21 | A-04·NQ-3 소견 집계 |
| C15~16 | A-05·MZ-2·NR-5 스냅샷 결측 |
| C17~20·29~30 | NO-2·NP-1 판정서 존재·검사 집합 |
| C22~23 | NP-2 mismatch 소비 응답 |
| C24~28 | NO-4·NN-2·NQ-1 타입·중복·거부·원천 |
| C31~38 | NR-2·NR-3 |
| C39~40 | NR-4 |

표에 직접 없는 이전 부류는 별도 메모리 시험으로 보완했습니다. 판정서 필수 필드·타입 98건, 명세 필수 필드 11건, 원천/명세 결속 2건, 집합 결측 3건, 명세 내부 필드 4건, 로그 필드 17건, 이전 요청·dispatch·스냅샷·최신 통합 결측 11건, **합계 146건은 모두 기대한 exit 4**였습니다. 원천·추출기 통합 응답·조기 문서의 단일 읽기도 확인했습니다. 구동·발췌·Workflow 반례는 각각의 실제 함수/본문으로 따로 재시험했습니다.

회귀표에는 최소한 다음 문안을 넣어야 합니다.

| 행 | 생성·변형과 기대 |
|---|---|
| L13 교체 | 실제 청구항 실패→해당 분해 retry 요청 대기; checked·순서·포인터·요청 접두부를 함께 보존 |
| L15 교체 | 실제 조기 재시도 E=2/full=1; 재시도 소비 좌표와 첫 실행 스냅샷 포함 |
| L16 추가 | mismatch 분해 소비→다음 분해 LanePending; 불일치 이력·N/A 보존 |
| C41 추가 | S 상세 축과 보고 축 불일치→exit 4 |
| C42 추가 | count 쌍 불일치와 pass 공존→exit 4 |
| C43 추가 | 조기/출구 회차 999 또는 요청 좌표 없는 회차 증가→exit 4 |
| C44 추가 | S 회차가 현재 E보다 뒤→exit 4 |
| C45 추가 | appended 부재·비bool 및 원장 대조 우회→exit 4 |
| C46 추가 | 선등록하지 않은 법 트리·지원하지 않는 엔진 판→명시적 거부 |

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY - <<'PY' … PY`로 전경 실행했습니다. `/memory/t40`는 사전 안의 경로 문자열이며 실제 디렉터리를 만들지 않았습니다.

| 명령·호출 경로 | 마지막 출력 또는 판정 줄 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `65551a44db7dca15d8826bf42235c11d2e0ec1df` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `db17fc8d030c795f3214969474541be498c13c3e42119ddc07a4f0249c7c8d8f` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | 절차 외 지정 16파일 전부 메모와 일치 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | **exit 4** — 기준 런은 `--law-tree` 필수 |
| 위 명령에서 `--baseline` 생략 | **exit 4** — `--first-early` 경로 필수 |
| `--baseline --first-early …` 병용 | **exit 3** — 함께 쓸 수 없음 |
| `t40_regress.CASES()`; 파일 입출력을 dict/StringIO/BytesIO로 대체 | `MEMORY_REGRESSION 55 FAIL 0` |
| 이전 부류 추가 변형 146건→`metrics()` | `SUPPLEMENT_UNEXPECTED []` |
| 실제 `read.run`·FileLaneAdapter, 첫 조기 실패 주입 | `ACTUAL_RETRY_METRICS 0 complete` |
| 실제 mismatch 소비→다음 LanePending | `ACTUAL_MISMATCH_PENDING_METRICS (4, …)` |
| R1 요청·로그·응답 xhigh, MD max 유지 | **exit 4** — 재생성한 요청 MD와 저장 MD 불일치 |
| R1 정합 대조군의 S 축만 변경 | `R1_WRONG_AXIS_ACCEPTED 0 complete … jaccard: 1.0` |
| d4e6ca2 모듈·계약 Git blob 메모리 적재 | **exit 4** — `_run_is_terminated` 없음 |
| `classify`·`classify_after_exception` 대입 | `DRIVER_CLASSIFY 9 / 9` |
| 실제 `enter`의 worktree 부재·잘못된 run | 각각 `EXIT_CODE=14` |
| 종결 포인터 true + 증거 기록 실패 | `EXIT_CODE=14` |
| `snapshot_first_early`: 미실행→실행→후속 변경 | `SNAPSHOT_NOCONV_THEN_FIRST_KEEP 1 True` |
| 실제 `cmd_lanes`·`cmd_dispatch`, 쓰기 메모리 대체 | 조회 무변경; 4차 발주 exit 15·무변경; 충돌 exit 14·무변경 |
| `candidates`·`comp_texts_fn`: 5→1 병합 | `['M99', 'M99', 'M99', 'M99', 'M99']`; 자동 열위 없음 |
| `sample_indices`·기준 원문 단락 대조 | CL-2·4·7·9·12·14·16·19·21·24, `LOCATORS 27 / 27` |
| `node --input-type=module`, Workflow의 agent/pipeline 대체 | `toString`·`constructor`·`/./` 모두 `calls:0`; wrote=false와 null 별도 집계 |
| 봉투 stdout→메모리→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

v6에는 발주문이 지목한 `_next_dispatch`가 없습니다. 해당 기능의 실제 구현인 **`cmd_dispatch` 전체**를 시험했습니다. 발췌 스크립트의 쓰기 진입점 `ex1/ex2`는 실행하지 않았습니다.

**[미검증]**

- 실제 계측 worktree 생성·source 봉인·유료 레인 호출·봉투 발행·생산 원장 append는 하지 않았습니다.
- 회귀 생성기의 원래 `--work` 파일 쓰기·서브프로세스 경로는 실행하지 않았습니다. 55사례의 생성 함수와 추출 함수는 메모리 파일 계층으로 실행했습니다.
- 실제 Workflow transcript/journal 구조·실호출 effort·문맥 격리·시간·비용은 확인하지 않았습니다.
- 외부 스테이징 TXT·도면 20파일은 읽지 않았습니다. 사본의 봉인 원문과 기준 산출물을 사용했습니다.
- `read.run` 시험의 진입 지문 가드와 일부 실패/봉투 조건은 명시적으로 대체했습니다. 실제 운영 런 재개 성공의 증명으로 확대하지 않습니다.
- 파일 존재 조합만으로 기록 실패와 사후 삭제의 모든 이력을 구별했다는 보증은 하지 않습니다.

**읽은 파일**

T40 §1·§4·§5, D-20260905-02 §17 및 추기, 1~20차 도전의 지적·처분·검증 부분, SPEC §8.4 지정 행, T14·T17·T38, run-kinds/read 계약과 approval-envelope·convergence 스키마를 읽었습니다.

대상은 설계 v3·v22와 관련 과거 판본 대조, 구동·지표·회귀·발췌·Workflow·봉투 스크립트, 회귀표, ADVICE-PROMPT/REPLY입니다. 구현은 `read.py`, `source.py`, `plan.py`, `contract.py`, `file_adapter.py`, `paths.py`, `ReadView`, `convergence.py`, `run_checks.py`, `report.py`의 관련 생성·판정 경로를 읽었습니다. 기준 런의 run.yaml·봉인 원문·판정서·명세·요청/응답·로그·포인터·사본 원장 및 지정 Git blob을 대조했습니다.

파일·임시물·캐시를 쓰지 않았고, 정본 리포는 허용된 Python 인터프리터 사용 외에 읽지 않았습니다. 실측은 시작하지 않았습니다.