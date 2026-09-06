# 독립 감수 원문 — M1b 설계 도전 22차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v23 · 판정 REVISE(MED 5)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `fe67fc77ed6d2dbf879ea499a1daf6a72975a3b123c93fc69192cbab8692eff4` · 19191 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v22/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(15:46 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `857fc49` · 마커 3항 일치 · 메모 v23 sha256 `e2b9dff7…` · v1~v22 + 회귀표 v3 + 자문 봉투·회신 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 22회」 명기(L-055 조항 이행). 폐쇄 = **이전 77건 closed 65 · partially 12 · open 0**. **B·C·E·F PASS**(17회 연속). 회귀표 61 사례는 도전자 재실행에서도 전건 PASS — 그러나 **실제 러너 산출물에서 출발한 추가 반례 5건이 통과**.

**판정 = REVISE · 5건(MED 5) · 기각 0 · 발주자 귀책.** **NT-1**: fail 축 ↔ 수렴 소견의 대응을 `bool(fail_axes) == conv_fail` 하나로 축소 — 소견 rule 을 상신 축으로 바꿔도 · fail 축 셋에 소견 하나여도 수용(도전자 대조군 R1_WRONG_FINDING · R1_THREE_FAIL_ONE_FINDING). **NT-2**: 청구항 재시도의 상한 논리를 출구 회차에도 적용 — 실행된 full 의 attempt 는 코드상 `tail_attempt + 1` 인데 상한만 보아 2→1 변형을 정상·terminated-failure 로 수용. **NT-3**: 비완료 상태에서 lane-log 를 `[]` 로 지워도 미소비 응답으로 받고, `if rows:` 가 거짓이 되어 예산·발번·S≤E 검사 전체가 생략(attempt 999 통과). **NT-4**: 회귀표 L 행이 러너를 돌리지만 기준 런 lanes 디렉터리 전체(요청서 포함)를 복사해 시작 — 도달 전 요청 4개 잔존 · 발주 기록을 완성 로그에서 역제조 · L01~L11 이 baseline 모드 · L03 생성 근거 문안 불일치 · 61 행은 MY~NS 전수가 아님. **NT-5**: 법 트리 내용 핀에 `reader/reader-rules.yaml`·`reader/schemas/material-spec.schema.json`·`reader/READER-VERSION` 이 빠졌고 코드·계약 비교가 한 방향(도전자 LAW_UNPINNED_3FILES 통과).

**총괄이 22차 뒤 스스로 발견한 지적 밖 오류 1**: v23 까지 기준 런의 `--law-tree` 추출을 실제 디스크에서 한 번도 실행하지 않았다 — 실행하니 원장 루트를 법 트리(체크아웃)에서 찾아 「포인터 appended=true 인데 원장에 대상 run_id 행이 없다」 exit 4. 기준 런의 원장은 main 에 있다 → v24 에서 run_repo(런 산출물·원장·RunPaths)와 법 트리(코드·계약·규칙·절차)를 분리. 재현: `git archive ad4c6c3 engine reader contracts` 트리를 법으로 → complete · 163 · component 56 · E 1 · full 1.

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 22**. **전부 수용 → 지표 v24 + 회귀표 v4**(read.convergence 소견을 fail 축에서 재도출 — rule·locus·found·expected·개수·순서(NT-1) · E.attempt == 수렴을 실행한 완료 반복 수(retry 요청의 결함 블록으로 판독) · full.attempt == 1 + synthesize 최대 발번 · 예산·S≤E 는 lane-log 유무와 독립(NT-2) · 소비 사슬(분해 batch-0 둘 · retry-k ⇒ 반복 k−1 완료 · 접지 그룹 전부 아니면 전무 · synthesize ⇒ 접지 · 후속 ⇒ 게이트 · 완주 ⇒ 마지막 synthesize)을 lane-log 부재·빈 배열·부분 삭제에 같은 규칙으로(NT-3) · **회귀표 v4 = 원천 + 빈 lanes 에서 러너를 실측 호출 단위로 반복 호출 · 대기 요청에만 공급 · 발주 기록·스냅샷은 호출 시점 수집 · L·C 전부 실측 모드 · L00 기준 런 원본 + 별도 법 트리 · 대응 지적 열 · 75 사례 PASS**(NT-4) · 법 트리 핀 = engine/·reader/(procedure 제외 · 규칙·스키마·버전 포함)·contracts/ 파일 집합 양방향 상등 + 바이트 동일 · run_repo 분리(NT-5)) → **M1b 23차 도전(지적 `NU-*`)**.

지적 열거 = NT-1, NT-2, NT-3, NT-4, NT-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 22회)

**MY~NS 77건: closed 65 · partially 12 · open 0.** 외부 자문은 동봉 회신과 §17 추기상 이미 회신·반영됐습니다. 계수는 이어갑니다.

**회귀표 61사례는 전건 PASS를 재현했습니다.** 그러나 실제 러너 산출물에서 출발한 추가 반례가 통과합니다. 지적은 **NT-1~5, 모두 MED**입니다. 실측 착수 근거로 사용할 수 없습니다.

**A — 원장 정합·이전 지적 폐쇄**

`partially`는 지정 변형의 수정과 원문이 요구한 불변식 전체의 폐쇄를 구별한 판정입니다.

| 회차 | closed | partially |
|---|---|---|
| MY | MY-1~5·7~13 | MY-6 |
| MZ | MZ-1·2·4~9 | MZ-3 |
| NA | NA-1~7 | — |
| NB | NB-1~3 | — |
| NC | NC-1~3 | — |
| ND | ND-1~2 | — |
| NE | NE-1~2 | — |
| NF | NF-1 | — |
| NG | NG-1~2 | — |
| NH | NH-1~2 | — |
| NI | NI-1~2 | — |
| NJ | NJ-1 | — |
| NK | NK-1 | — |
| NL | NL-1 | — |
| NM | NM-1~2 | — |
| NN | NN-1·2·4 | NN-3 |
| NO | NO-3 | NO-1·2·4 |
| NP | NP-1~3 | — |
| NQ | NQ-1~3 | — |
| NR | NR-3~6 | NR-1·2 |
| NS | NS-3·5 | NS-1·2·4·6 |

잔여는 수렴 소견 정합(NT-1), 회차 결속(NT-2), 비완료 상태의 소비 증거 결측(NT-3), 회귀 부모의 생성 경로(NT-4), 법 트리 핀(NT-5)입니다.

§8의 격 구분은 유지 가능합니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 이행입니다. ⓘ의 청구항 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이고, 인덱스·후보 제시·런 표시는 구현 재량입니다.

G-12는 여전히 미집행입니다. 이번 구동을 `source → read`에서 멈추는 운영 범위와, 종료선·비게시가 엔진 전역에서 강제된다는 주장을 구별해야 합니다.

**NT-1 · MED — fail 축과 수렴 소견의 대응을 불리언 하나로 축소했다.**

좌표: 메모 §5 생성 불변식·§9 D①; [t40_metrics.py:129](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:129), 특히 161~163행; `convergence._compare_count/_compare_sets`.

상세==보고, 고정 policy·threshold, 값에서 status 재도출, 상신 목록 대조는 수정됐습니다. **현재 고정 규칙에서는 재도출 의미도 러너와 같습니다.** 다만 마지막 검사는 다음 관계뿐입니다.

```python
bool(fail_axes) == conv_fail
```

실제 R1 ID·핀 메타데이터·partial/read·xhigh 프로필과 재렌더된 요청을 가진 대조군을 생성했습니다. read-b 종속항 문언 끝 한 글자를 제거해 실제 `dependent-set` 실패를 만들고, 분해 재시도와 봉투를 거쳐 완료한 자료입니다.

```text
R1_CONTROL 0 complete gdm-wo2026128750a1-t40-r1 530b096146e1b7a42f05ffe242e8eccaec2c4d16
R1_WRONG_FINDING 0 complete
R1_THREE_FAIL_ONE_FINDING 0 complete 1
```

두 변형은 각각 다음과 같습니다.

- S의 유일한 수렴 finding에서 `rule`만 `dependent-set → tree-edges`로 변경. 실제 fail 축은 dependent-set인데 상신 축의 소견으로 바뀌어도 수용합니다.
- S의 두 count 쌍을 `[1,999]`, `[24,999]`로 바꾸고 상세·보고 count 축 status도 fail로 맞춤. **fail 축 셋에 finding 하나**인데 수용합니다.

두 경우 모두 sidecar는 변경 바이트에 맞췄습니다. 러너의 두 비교 함수는 해당 fail 축마다 소견을 추가하므로 이 조합은 생성하지 않습니다. NS-1의 “수렴 실패 소견 정합”은 부분 폐쇄입니다.

**고치는 문안:** “고정 축에서 재도출한 fail 축별 소견의 rule·locus·개수 및 표현 가능한 found/expected를 생성 규칙과 대조하고, fail 유무만 같은 모순 판정서는 exit 4로 거부한다.”

**NT-2 · MED — 청구항 재시도의 상한 논리를 출구 회차에도 적용해 실제 재시도를 숨길 수 있다.**

좌표: 메모 §5 회차 결속·§9 D①; [t40_metrics.py:165](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:165), 595행 이하; `read.run:tail_attempt`.

L13의 설명은 **조기 회차에 대해서는 맞습니다.** 청구항 실패 재시도는 분해 발번을 올리지만 수렴이 보류됐으므로 조기 수렴 attempt를 올리지 않습니다.

그러나 출구는 다릅니다. 실행된 full의 attempt는 코드상 `tail_attempt + 1`이고, 후속 레인 발번도 같은 `tail_attempt`를 사용합니다. 현재 검사는 양쪽 모두 아래 상한만 확인합니다.

```text
attempt − 1 ≤ 해당 작업의 최대 retry 발번
```

실제 R1 러너에서 조기 재시도와 출구 schema 재시도를 거쳐 정상 완료한 대조군은 **E=2, full=2, 소비 로그 12행**이었습니다. full의 attempt만 1로 낮추자:

```text
R1_WRONG_FULL_ATTEMPT 0 complete 1
```

출구 실패로 종결한 L03 계열에서도 **2→1 변형을 `terminated-failure`로 수용**했습니다. 재시도 없는 첫 판정처럼 기록한 full을 정상 증거로 받습니다.

**고치는 문안:** “조기 회차는 청구항 재시도와 수렴 실행을 구별해 결속하고, 실행된 full 회차는 최종 정본 후속 소비 좌표의 tail 발번+1과 대조하며, 계약 상한·S≤E 검사는 로그 유무와 독립적으로 수행한다.”

**NT-3 · MED — 비완료 상태에서 이미 소비됐어야 할 로그를 전량 삭제해도 미소비 응답으로 받아들인다.**

좌표: 메모 §5 전 상태 공통 검사·§9 D④; [t40_metrics.py:569](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:569), 590·596행.

실제 `gen_measure_pending`은 분해 둘과 접지 셋을 소비한 뒤 synthesize에서 대기합니다. 원본은 **소비 로그 5행, 수렴 실행 E, 유효 S**를 가집니다.

그 로그 파일의 내용만 `[]`로 바꿨습니다.

```text
PENDING_PRODUCER ... LanePending ... ROWS 5
EMPTY_LOG_WITH_EXECUTED_E 0 in-progress
EMPTY_LOG_S_E_ATTEMPT999 0 in-progress 999
```

첫 변형은 삭제된 소비 행 전부를 `unconsumed_responses`로 취급하면서 조기 지표를 계속 출력합니다. 두 번째는 같은 자료에서 S·E의 attempt를 함께 999로 바꾼 것입니다. **`if rows:`가 거짓이 되어 예산·발번·S≤E 검사 전체가 생략됩니다.**

현재 E가 생성됐다는 사실은 적어도 양쪽 분해 소비가 있었다는 근거입니다. 접지 배치 일부가 미도착해 미소비 응답이 남는 합법 상태와 구별할 수 있는 결측입니다.

**고치는 문안:** “비완료 상태도 현재 판정점까지 필수로 소비된 요청·로그의 최소 집합을 확인하고, 그 이후 배치의 미소비 응답만 허용하며, 로그 파일 부재·빈 배열·부분 삭제를 같은 결측 규칙으로 검사한다.”

**NT-4 · MED — L행은 러너를 돌리지만, 도달 전 요청이 없는 신규 런의 생성 경로는 아직 재현하지 않는다.**

좌표: 메모 §5 회귀표·§9 D②③; [t40_regress.py:63](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_regress.py:63), `write_dispatch`, `snapshot`, `CASES`; `T40-REGRESS-TABLE.md`.

판정·로그·포인터를 러너가 생성하도록 바꾼 것은 확인했습니다. 그러나 `Fx.__init__`은 기준 런의 **lanes 디렉터리 전체**를 복사하고 로그·포인터 두 파일만 제거합니다. 요청서도 선공급됩니다.

L12 청구항 실패→분해 재시도 대기를 실행한 뒤에도 다음 **후속 요청서 4개**가 남았습니다.

```text
read-a/ground-dependent/batch-0/request.md
read-a/ground-dependent/batch-1/request.md
read-a/ground-independent/batch-0/request.md
read-a/synthesize/batch-0/request.md
```

이번 신규 실측에서는 그 시점에 발주될 수 없는 요청입니다. NS-4 원문이 요구한 **“도달 전 요청 부재”**가 닫히지 않았습니다.

또한 다음 제한이 남습니다.

- `write_dispatch`는 실제 발주 사건 대신 **완성된 lane-log에서 역으로 발주 기록을 제조**합니다.
- L01~L11은 baseline 모드입니다. 현재 E·S 및 실측 dispatch 검증을 함께 통과했다는 증명이 아닙니다.
- 표의 L03 생성 근거는 여전히 “분해 element text_verbatim 변경”이지만, 실제 생성기는 **통합 응답의 figure 참조를 FIG-99로 변경**합니다.
- 61행은 **L 14 + C 47**이며, MY~NS 지정 반례 전수를 포함한 표가 아닙니다.

**고치는 문안:** “L은 원천과 빈 lanes에서 시작해 실제 pending 요청에만 응답을 공급하고 발주·스냅샷을 호출 시점에 수집하며, 도달 전 요청 부재를 검증한 실측 모드 부모에서 C를 파생하고 표의 생성 근거·지적 대응을 실제 실행과 일치시킨다.”

**NT-5 · MED — 법 트리 내용 핀에서 검증에 쓰는 파일들이 빠져 있다.**

좌표: 메모 §5 법 트리·§9 D①; [t40_metrics.py:270](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:270); `validators`, `Rules.load`, `load_schema`.

절차 5파일 핀과 engine·reader/lib·contracts 비교는 추가됐습니다. 그러나 다음 파일은 비교 밖입니다.

```text
reader/reader-rules.yaml
reader/schemas/material-spec.schema.json
reader/READER-VERSION
```

별도 메모리 법 트리에서 규칙에 주석 추가, 재료 스키마 `$comment` 변경, 리더 버전을 `9.9.9`로 변경했습니다. 대상 원장 근거를 유지한 대조 결과:

```text
LAW_UNPINNED_3FILES complete 56
```

이는 의미 변경으로 오계수를 만들었다는 주장이 아니라, **선등록 조합과 다른 내용이 핀 검사를 통과한다는 직접 반증**입니다. 코드·계약 비교도 지정 법 트리를 한 방향으로 순회하므로 파일 집합의 완전한 동일성 검사는 아닙니다.

렌더 경로는 구별해야 합니다. `render_request_body`가 직접 여는 파일은 `prompt_path`의 절차 문서입니다. 응답 스키마·지시·원천 조각은 요청 객체에서 들어갑니다. 위 누락 파일은 주로 **검증 법과 산출 메타데이터**의 입력이며, 절차 외 추가 렌더 파일이라고 부를 근거는 없습니다.

**고치는 문안:** “기준 추출에 쓰는 코드·계약·규칙·재료 스키마·리더 버전·절차의 파일 집합과 바이트를 양방향 내용 핀으로 검증하고, 지원 조합 밖이면 적재 전에 exit 4로 거부한다.”

**B~G 판정**

| 항목 | 판정 | 직접 확인·잔여 |
|---|---|---|
| A 원장·폐쇄·격 | REVISE | 재정 해석 유지 가능. 위 12건 부분 폐쇄 |
| B 계측 커밋 셋 | PASS | 부모·전체 팔 diff·절차 tree·16파일 numstat·프로필·요청 재렌더 확인 |
| C 구동 v6 | PASS — 메모리 범위 | 분류·진입 실패·증거 실패·스냅샷·조회/발주·상한 확인 |
| D 지표 v23·회귀표 v3 | REVISE | NT-1~5 |
| E 발췌 v4 | PASS — 확인 범위 | 27단위·병합 후보 재사용·표본·인용 해소·판정 불가 처분 |
| F Workflow v4 | PASS — 대체 실행 범위 | 사전 거부·하드 옵션·wrote/null 구별 |
| G 결정 공백 | REVISE | 모순·결측 증거를 정상 지표로 받는 통로와 불완전한 법 핀 잔존 |

새 좌석 값이나 임계 재정을 요구하는 지적은 없습니다. 기존 원장과 생성 코드에 맞춘 수정 사항입니다.

**D — 추가 생성 경로와 NS별 판단**

- **NS-1:** 상세·보고·status·상신·fail 유무는 수정. 축별 실패 소견은 NT-1.
- **NS-2:** L13의 조기 상한 이유는 맞음. 출구 회차와 빈 로그 우회는 NT-2·3.
- **NS-3:** mismatch 뒤 LanePending 허용은 수정. L10·L11과 full 공존 거부를 확인했습니다.
- **NS-4:** 실제 러너 호출·판정·로그·포인터 생성은 확인. 신규 런의 기록 순서는 NT-4.
- **NS-5:** 필수 7필드·appended bool·정수 memo_count 및 기존 지정 변형은 닫혔습니다.
- **NS-6:** d4e6ca2 엔진 지원 문안 제거·절차 핀은 수정. 전체 검증 법의 내용 핀은 NT-5.

조기 exact-match 실패는 **예산이 남은 read-a·read-b의 decompose를 각각 재발주**합니다. 실측에서는 read-a retry-1 대기 후 read-b retry-1 대기를 거쳐 **E=2/full=1/로그 8행**으로 완료했고, 지표도 수용했습니다.

`read.schema` 출구 실패는 통합 응답 항목에 최종 스키마가 금지하는 속성을 넣어 생성했습니다. 후속 접지 셋과 통합을 retry-1로 공급한 뒤 **13행·schema fail·halt**, 추출은 `terminated-failure`였습니다.

`refused`는 고정된 정상 루트에서는 진입 가드 때문에 도달하지 않습니다. 진입 후 루트 판정을 실패시키고 첫 응답을 깨진 JSON으로 공급하면 러너가 **terminated=true·memo_count=0·root_source=refused** 포인터를 생성합니다. 가드는 `(True, 'shadow_pointer')`, 추출기는 별도 원장 무결성 검사에서 exit 4였습니다. **refused 필드 허용이 모든 refused 자료의 N/A 수용을 뜻하지는 않습니다.** 이를 통상 루트의 오거부로 확대해 지적하지 않았습니다.

**D — C행과 기존 지적의 대응**

| 회귀표 C행 | 직접 대응하는 지적·부류 |
|---|---|
| C01·02 | A-01·NQ-2 원장 판독·기입 관계 |
| C03·04·06·07 | A-02 요청/응답 effort·거부·mismatch |
| C08~13·29 | A-03·NO-2·NP-1 생성·파생 불변식 |
| C14·21 | A-04·NQ-3 소견 합계·결측 |
| C15~18·30·31·34·36·37 | A-05·NR-2·NR-5 조기/완주 존재·실행 관계 |
| C19·20·24~26·28 | NM-1·NN-2·NN-4·NO-4·NP-1 및 원천 결속 |
| C22·23·27 | NP-2·NQ-1 소비·거부 |
| C32·33·38~40 | NR-2·3·4 |
| C41·42 / C43~45 / C46~48 / C49 | NS-1 / NS-2 / NS-5 / NS-6 |

회귀표 밖에서 스냅샷 식별·SHA·형태·수치, finding 형태, 완주/명세 식별, 요청·dispatch·원천 결속, 집합 전량 결측 등 **기존 변형 50개를 추가 실행해 모두 exit 4**를 확인했습니다. 최신 synthesize의 `LaneContractError`도 실제로 생성해 **9행 로그·terminated-incomplete·synth_counts=None**을 확인했습니다. C·E·F 지적은 별도 함수·Node 시험으로 확인했습니다. 이것을 동봉 회귀표 자체의 전수 피복으로 기록해서는 안 됩니다.

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY -c '<하네스와 명시한 호출>'`로 실행했습니다.

하네스는 파일 I/O를 dict·BytesIO로, `Fx.run`의 프로세스 경계를 동일 DRIVER의 메모리 실행으로 대체했습니다. 러너·FileLaneAdapter·검사·봉투 본문은 실제 코드를 사용했습니다. 가상 리포 원장은 메모리 루트로 해석했고, 사본에 없는 도면 바이트는 진입 검사용 파일명·지문 목록만 source-report에서 대입했습니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 결과 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `857fc491e4f218401b14580b13b3fe181c7c4754` — path·pin·order·disposable 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `e2b9dff7d6f9189a260a1a50dcb945dc7bbfb95f7d548661b7a2cf8c61bf171b` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만. 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git ls-tree` 기준·base의 절차 | 모두 `d7717eb8750115a49e81ec7803790093b98c40ec` |
| 세 ref에 `git log -1 --format='%H %P'` | base 부모 6d92cad, R1·R2 부모 ad4c6c3 |
| base→R1/R2 전체 diff·numstat | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | §0′의 비절차 16파일 수치 전부 일치 |
| Git YAML→`lane_profiles()` | R1 분해·통합만 xhigh, R2 종속 접지만 sonnet-5/high |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 4: `기준 런은 --law-tree <t40-base 체크아웃> 이 필수다` |
| 원본 기준 산출물+ad4c6c3 절차의 메모리 법→`metrics(..., baseline=True)` | `BASELINE 0 complete 163 56 …` |
| 기준 요청 JSON→`LaneRequest`→`render_request_md` | `REQUEST_RERENDER_BYTES_EQUAL 6` |
| `CASES()`의 61개 build→`metrics` | `CASES 61 FAIL 0` |
| 기존 변형 50개 추가 대입 | `HISTORICAL_MUTANTS 50 NOT_EXIT4 []` |
| 스냅샷·원천·통합 응답 open 계수 | `SINGLE_READ 0 1 1 1` |
| `cmd_read` 실제 enter 실패 | `ACTUAL_ENTER r0 14`, `ACTUAL_ENTER bogus 14` |
| `classify`·`classify_after_exception`·예외 기록 실패 | 기대 분기 일치, `CMD_READ evidence-fail 14 EXIT_CODE=14` |
| `cmd_dispatch` 4회·`cmd_lanes` 반복 | `DISPATCH [0, 0, 0, 15] QUERY_COUNTER_UNCHANGED True` |
| `snapshot_first_early` 미실행→실행→현재본 변경 | `NONCONV_NOT_SNAPSHOT True`, `SNAPSHOT_KEPT True` |
| `candidates/comp_texts_fn` 5→1 병합 | `['M9', 'M9', 'M9', 'M9', 'M9']` — 자동 열위 없음 |
| 발췌 자기 대조·표본 인용 locator | `IMP_SELF 20`, `LOCATORS 27 27` |
| Node에서 Workflow 본문·agent/pipeline 대체 | 사전 거부 10종 모두 calls=0; 정상 wrote/notWritten/dropped=`1/1/1` |
| `--baseline --first-early absent.json` | exit 3: `함께 쓸 수 없다` |
| `metrics`에 first-early 옵션 없음 | `NO_FIRST_EARLY_OPTION 4` |

v6에는 `_next_dispatch`가 없습니다. 그 책임을 옮긴 `cmd_dispatch`와 무변경 조회를 시험했습니다.

기준값은 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10·조기 2행/완주 13행**으로 재현했습니다. 표본은 **CL-2·4·7·9·12·14·16·19·21·24**입니다.

**[미검증]**

- 실제 Workflow/API 호출, transcript·journal의 실물 형식과 실제 모델·effort·문맥 격리.
- 외부 원시 TXT·도면 20개 바이트 및 새 `source.run`의 물리 봉인·Git 핀 집행.
- 실제 worktree의 쓰기·재진입·원장 append·프로세스별 import 격리. 메모리 실행 결과를 그 시험으로 주장하지 않습니다.
- 비용·시간·토큰 추정과 Owner의 내용 판독.

**읽은 파일**

원장 T40 §1·4·5, D-20260905-02 §17와 추기, SPEC §8.4 지정 행, T14·T17·T38, run-kinds·read 계약과 approval-envelope 스키마; 1~21차 감수의 지적·수정 문안·관련 검증절; 설계 v3·v22·v23, bundle 구동·지표·회귀·발췌·Workflow·봉투와 회귀표·자문 봉투/회신; `read.py`·`source.py`·`plan.py`·`contract.py`·`file_adapter.py`·`paths.py` 및 convergence·run_checks·report·rules·spec_io·inventory·schema_check 관련 구현; 기준 런 메타데이터·원천·판정서·명세·원장·요청/응답 자료와 지정 Git blob을 읽었습니다.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았고, 실측 레인은 시작하지 않았습니다.