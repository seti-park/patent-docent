# 독립 감수 원문 — M1b 설계 도전 35차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v37(진입점 × 의무 격자 · 34차 OF-1~7 반영) · 판정 REVISE(MED 5) · **T45 ③ 상신 조건 성립**

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `d09ac39fbd7b45227dde001e2e9d221bdff1bb964bc5c85a4923a50a515ba109` · 22896 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v35/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · Monitor(17:13 기동 · 17:4x 종료 · USAGE 는 레인 STATUS). 사본 재핀 `c9362f6` · 메모 v37 `2e1c2a7f6ddd4fe0` · 대장 `33f03a6ed65b7780`(68행 + 격자 8×7) · 회귀표 v16(165) · bundle 75. 이번 기동 = T44 자동(34차 조건) · **T45 ③ 문턱 판**.

**판정 = REVISE · 5건(MED 5 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 6차 · 발주·검수 총괄).** 지문 전건 일치 · 정적 `0/0/0 grid=0` · 심사 ① 성립 · ②~⑤ 불성립 · 갈래 ⑴ 5 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **격자 대조 = 빠진 진입점·의무 열 반례 0**(8행 = 실제 진입점 · 56칸 일치) · 격자 도달성은 순서 변이(`grid=1`)는 잡고 분기 지배(`if False:` 안 호출 · `grid=0`)는 못 잡음(J54 공개 한계 · 지적으로 안 셈). **진행도(행 단위) = `mismatch=10 unmet=10 unreviewed=0` — 31~35차 = 12 → 12 → 9 → 10 → 10 · 두 회차 연속 비감소 → 재정 T45 ③ 상신 조건 성립.** 34차 10행 중 3 닫힘(09·27·63) · 7 잔여(40·46·49·55·56·58·65) · 새 3(50·51·54). A 폐쇄표 closed 132 · partially 6(NZ-3 · OA-3 · OC-3 · OE-3 · OF-1 · OF-4) · open 0 · OF-2·3·5·6·7 closed. **OG-1 · P2·P6·P7·T3 · SITE-46·54·55·56**: 환경 실패 뒤 영수증 보존 연결 **앞의** 오류 처리 두 곳(후검출 포인터 비JSON 파싱 · traceback 지문 재독 PermissionError)이 다시 실패하면 영수증 보존을 건너뜀. **OG-2 · P2·P6·P7 · SITE-40·65**: sandbox 결과 순서가 `environment_fault → require_runner_output(파싱) → is_io_fault` 라 sandbox 포인터 비JSON 이면 IO 판별 전 JSONDecodeError → `mismatch`(infeasible 이어야). **OG-3 · P3·P7 · SITE-58**: `R.external("termination", …, RunPaths(run_root, W))` — `RunPaths` 가 인자 평가로 경계 **앞에서** 실행 · 계약 읽기 실패가 exit 16(종결 근거 있음)으로. **OG-4 · P1·P7 · SITE-49**: source 핀 조회 `GitUnavailable → StageEnvironmentError` 를 `driver_boundary` 가 안 받음(OSError·ValueError·UnicodeError 만) → traceback 종료. **OG-5 · P7 · SITE-50·51**: 대기 요청 `request.json = {}` 이면 `req["model"]` KeyError 가 `driver_boundary` 밖으로 · 격자 「해당 없음」 사유(구동 중단 14 고정) 불성립.

**게이트 소견(발주문이 요구)**: 「현재 방식이 수렴한다고 판정할 근거는 부족하다. 격자는 실제로 배선 누락을 잡았고 이전 3행을 닫았지만, **오류를 처리하는 코드가 다시 실패하는 경로 · 외부 함수에 들어가기 전 인자 평가 · 같은 의무의 두 번째 실행 단계**에서 3행이 추가됐다. 남은 결손은 표의 크기보다 오류 경계의 합성에 있다. 네 선택지 중 가장 근거가 있는 것은 **자리 축소·대장화** — 같은 의무를 따로 집행하는 경로 수를 줄이고, 호출 결과 보존과 실패 처분을 공통 경계에 모으는 조건에서. 제한된 다음 판도 오류 전이·처분 경계를 한정해 확인한다면 정당. 별도 탐색 단계는 수집·검수·재정 허가 분리 + 탐색 산출물 비승격 조건. 보류·중단은 Owner 판단.」

**총괄 처분 = 전부 수용(공학) · 이행 보류 — 재정 T45 ③ 상신(결정 브리핑 T47).** 31~35차 행 이동: 31차 12 → 32차 12(7 폐쇄 · 5 잔여 · 새 7) → 33차 9(7 폐쇄 · 5 잔여 · 새 4) → 34차 10(4 폐쇄 · 5 잔여 · 새 5) → 35차 10(3 폐쇄 · 7 잔여 · 새 3). 다섯 회차의 새 지적 26건 중 형태: 「같은 의무의 다른 자리」 9 · 「자료/환경 역할 뒤집힘」 8 · 「오류 처리 자체의 재실패·순서 역전·인자 평가」 6 · 「법 내부 대체 경로」 3. 발주자 오류 누계 219 → **224**.

지적 열거 = OG-1, OG-2, OG-3, OG-4, OG-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 35회)

**OG-1~5, MED 5건, 갈래 ⑴ 5건이다.** 대장 누락 반례 0, 도출 누락 0, 새 보증 요구 0. 행 단위 진행도는 **`mismatch=10 unmet=10 unreviewed=0`**이다. 34차와 같으므로 **T45 ③의 두 회차 연속 비감소에 따른 Owner 상신 조건이 성립한다.**

마커의 path·pin·order와 detached HEAD `c9362f6`이 일치했다. 먼저 확인한 사용자 지정 지문도 모두 일치했다. 메모 `2e1c2a7f6ddd4fe0`, 대장 `33f03a6ed65b7780`을 대상으로 판정했다. 파일 쓰기는 하지 않았다.

**격자부터 대조한 결과**

실제 구동기 서브커맨드 6개, 지표기 진입, `replay()`가 격자의 8행과 대응한다. 지표기의 baseline·실측 분기는 함수 내부에서 따로 대조했다. 폐쇄된 replay CLI도 확인했다. 고정 범위에서 **빠진 진입점이나 별도의 의무 열이라는 반례는 발견하지 않았다.** 56칸은 적용 31칸·해당 없음 25칸으로 일치한다.

다만 다음 두 주장은 구별해야 한다.

- [t40_sites.py:292](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_sites.py:292)는 확장한 호출 목록에서 첫 효과와 의무 함수의 위치를 비교한다. source의 준비 검사를 `seal_source` 뒤로 옮긴 메모리 변이에서는 `grid=1`로 검출했다.
- 분기 지배를 증명하지는 않는다. 준비 검사를 `if False:` 아래로 옮긴 메모리 변이는 `grid=0`이었다. `around/ordered`도 호출열의 존재·순서를 검사하므로, 선행 오류가 후행 영수증 보존을 건너뛰는 경우나 두 번째 sandbox 단계의 순서를 보증하지 않는다.

이는 J54가 공개한 한계다. CFG 증명을 새로 요구하는 지적으로 세지 않았다. 아래 OG는 **현행 코드에서 이미 약속한 의무가 끊기는 구체 경로**다. 특히 lanes·dispatch의 자원 역할 칸에 적힌 “실패는 구동 중단14로 고정”이라는 해당 없음 사유는 OG-5에서 성립하지 않는다.

**OG-1 — MED · ⑴ P2·P6·P7·T3 집행 위반 · SITE-46·54·55·56**

좌표: 메모 §5′.1 T3·§5′.4·§5′.11, [t40_drive.py:352](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:352) `run_engine.checked`, `finish_outcome`:404, `cmd_read`:444, [t40_resources.py:301](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_resources.py:301) `runner_output_markers`. 격자 `read × receipt/postflight`의 합성 문제다.

환경 실패 뒤 영수증을 보존하는 정상 연결은 생겼다. 그러나 그 연결 **앞의 오류 처리 두 곳**이 다시 실패하면 영수증을 건너뛴다.

1. 러너가 IO 예외를 낸 뒤 `checked()`가 포인터를 후검출한다. 포인터가 쓰다 남은 비JSON이면 `json.loads()`의 예외가 원래 outcome을 대신한다. `cmd_read` 외곽으로 빠져 `receipt_post → write_receipt`를 호출하지 않는다.
2. 예외 outcome의 traceback을 `record_text()`로 기록한 뒤 `finish_outcome()`이 같은 파일을 다시 열어 지문을 계산한다. 이 재독의 `PermissionError`는 실패 플래그로 바뀌지 않고 재발생한다. 역시 영수증 보존보다 먼저 탈출한다.

실제 wrapper·명령 함수를 사용하고 러너 실패·파일 입출력을 메모리로 대체한 관측:

```text
POSTFLIGHT_PARSE exit=14 calls=['runner', 'exc'] actual_writes=0
TRACEBACK_REHASH exit=14
calls=['traceback-written', 'traceback-rehash', 'outer-exc']
actual_writes=0
```

두 경우 모두 post 채집과 영수증 기록 호출은 0이다. 두 번째 시험은 `environment_fault=true`와 원래 traceback을 가진 outcome을 공급했다.

**잘못된 효과:** exit14 자체는 맞지만, 소비기가 읽어야 할 호출 outcome이 구조화된 영수증에 도착하지 않는다. SITE-54의 “실패는 False…재예외 금지”도 직접 깨진다. 자유문 exc 파일은 해당 outcome의 대체 입력이 아니다.

S45는 정상적인 환경 outcome 전달, post 채집 실패, 영수증 쓰기 실패를 다룬다. **후검출 파싱 실패와 traceback 지문 재독 실패가 보존 진입을 막는 경우**는 덮지 않는다.

**수정 문안:** “원래 outcome을 유지한 채 후검출·traceback 처리 실패를 별도 기록하고, 가능한 호출 영수증 보존을 시도한 뒤 exit14로 종료한다.”

SITE-67의 `preserve_receipt()`는 호출되었을 때의 채집·기록 실패 분리를 수행한다. 이번 반례는 그 앞의 연결이므로 SITE-67을 중복 계수하지 않았다.

**OG-2 — MED · ⑴ P2·P6·P7 집행 위반 · SITE-40·65**

좌표: 메모 §5′.4·§5′.11, [t40_replay.py:323](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:323), `runner_output_markers`:301. 격자 `replay × io_order/postflight`의 **sandbox 단계**다.

원본 영수증의 결속 → IO 선판별 → 파싱 순서는 고쳐졌다. 하지만 sandbox 결과에서는 다음 순서가 남아 있다.

```text
child_result
→ environment_fault 검사
→ require_runner_output(포인터 JSON 파싱)
→ is_io_fault(res)
```

따라서 자식이 유효한 JSON으로 `io_fault=true`를 반환했더라도, sandbox 포인터가 비JSON이면 IO 판별 전에 `JSONDecodeError`가 난다. replay 외곽의 `ValueError` 경계는 이를 기본 `mismatch`로 반환한다.

실제 `replay()`를 실행하되 쓰기·하위 프로세스·결속 입력을 메모리 대역으로 공급한 관측:

```text
SANDBOX_IO_POINTER disposition=mismatch replayed=0
pointer_reads=1 actual_writes=0
REASON Expecting property name enclosed in double quotes…
```

**잘못된 처분:** 이미 확인된 sandbox IO가 `infeasible`이 아닌 자료 `mismatch`가 된다. 실패 자원도 sandbox로 알려져 있다.

S47은 **원본** IO와 비JSON의 조합을 시험한다. S44·S46도 이 sandbox IO와 포인터 파싱 실패의 조합을 지지하지 않는다. 격자의 최초 호출 순서가 정상이라는 사실로 두 번째 단계까지 닫히지 않는다.

**수정 문안:** “sandbox 결과의 환경·IO 표식을 보조 산출물 파싱보다 먼저 infeasible로 분리하고, 이후 파싱 실패도 실제 sandbox 자원 역할로 처분한다.”

**OG-3 — MED · ⑴ P3·P7 집행 위반 · SITE-58**

좌표: 메모 §2·§5′.4·§5′.11, [t40_drive.py:551](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:551) `cmd_retire`. 격자 `retire × resource_role`의 적용 범위다.

```python
R.external("termination", rs._run_is_terminated,
           RunPaths(run_root, W), ...)
```

`RunPaths(...)`는 Python 인자 평가 때문에 **`R.external`에 들어가기 전에** 실행된다. 이 생성자가 source/read/freeze 계약을 읽다가 실패하면 외부 자원 경계가 그 실패를 받지 못한다. 일반 `BaseException` 분기로 들어가 exit16을 낸다.

실제 `RunPaths`의 `contracts/stages/source.yaml` 읽기에만 `PermissionError`를 주입한 관측:

```text
RETIRE_CONTRACT exit=16 hits=1 actual_writes=0
[t40_drive] 종결 판정 불가(러너 가드): PermissionError…
```

**잘못된 처분:** 종결 근거를 확인하지 못한 법 자원 실패가, 종결 근거가 있을 때의 같은 ID 재실측 거부 코드16으로 분류된다. 기대는 효과 전 `처분=검수 불능`·14다. 삭제나 보존 쓰기는 발생하지 않았다.

S41은 정상 종결 거부와 git 선검증·내부 조회 실패를 다룬다. 외부 호출의 **인자 생성 실패**는 덮지 않는다.

**수정 문안:** “RunPaths 생성도 외부 자원 경계 안에서 수행하고, 종결 조회의 자원 실패는14, 종결 근거를 확인한 경우만16으로 종료한다.”

**OG-4 — MED · ⑴ P1·P7 집행 위반 · SITE-49**

좌표: 메모 §5′.4·§5′.11, [t40_drive.py:144](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:144) `cmd_source`, `driver_boundary`:93, `engine/stages/source.py`의 `_engine_pin`. 격자 `source × resource_role`의 연결 문제다.

source의 출력 경계·준비 검사는 추가됐다. 하지만 그 뒤 실제 source 핀 조회가 실패하면:

```text
gitpin.resolve_repo
→ GitUnavailable
→ source._engine_pin의 StageEnvironmentError
→ driver_boundary 밖으로 탈출
```

`driver_boundary`는 `OSError·ValueError·UnicodeError`만 받는다. 법이 감싸서 전달한 `StageEnvironmentError`는 여기에 포함되지 않는다.

실제 `cmd_source → seal_source → source.run → _engine_pin` 경로에서 git 조회 결과만 rc128로 대체한 관측:

```text
SOURCE_PIN escaped=StageEnvironmentError
cause=GitUnavailable git_hits=1 actual_writes=0
```

**잘못된 처분:** 선검증 후 실제 핀 조회가 실패하는 지원 오류 경로에서 `처분=검수 불능`·14로 분류되지 않는다. CLI에도 같은 경계가 있어 미처리 traceback 종료로 이어진다.

S42·S43의 출력 링크·준비 상태 검사는 이 법 예외의 전달을 시험하지 않는다. source의 핀 조회가 실패를 전파한다는 격자 사유는 맞지만, **구동기가 그 실패를 약속한 처분으로 받는 연결**은 없다.

**수정 문안:** “source 핀 적재가 전달하는 StageEnvironmentError와 원인 사슬을 구동 경계에서 보존하여 처분=검수 불능·14로 종료한다.”

**OG-5 — MED · ⑴ P7 집행 위반 · SITE-50·51**

좌표: 메모 §5′.4·§5′.11, [t40_drive.py:155](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:155) `pending_coords`, `cmd_lanes`, `cmd_dispatch`. 격자 두 진입점의 `resource_role=해당 없음` 사유와도 어긋난다.

대기 요청의 `request.json`이 유효한 JSON `{}`이면 JSON 파싱은 성공한다. 이후 `req["model"]`에서 `KeyError`가 나며, `driver_boundary`가 이를 받지 않는다. 배열 등 다른 최상위 형태에서는 `TypeError`도 같은 경로다.

실제 두 명령과 `pending_coords()`에 메모리 요청 `{}`를 공급한 관측:

```text
REQUEST_SHAPE lanes escaped=KeyError key='model' actual_writes=0
REQUEST_SHAPE dispatch escaped=KeyError key='model' actual_writes=0
```

**잘못된 처분:** 대장이 명시한 “요청 자료 결측·손상”이 접두가 있는 구동 중단14로 분류되지 않는다. 이번 반례에서는 `PENDING=0`이나 발주 파일이 생성되지는 않았다.

S40은 `scandir` 실패를 전파하는 경로를 닫았다. 그 사실은 전량 열거 후 **개별 요청의 형태 오류**까지 분류한다는 근거가 아니다.

**수정 문안:** “좌표를 추가하기 전에 요청 객체와 필수 필드를 검증하고, 형태·필드 실패는 완료 출력과 발주 기록 전에 처분=검수 불능·14로 종료한다.”

**남은 자리와 진행도**

68행의 담당 함수·자원·명시 오류 경로·선후·근거를 대조했다. 미심사 행은 없다. 이는 모든 입력 조합을 실행했다는 뜻은 아니다.

| 구분 | SITE 행 |
|---|---|
| 34차 10행 중 해당 경로 폐쇄 | 09·27·63 |
| 34차에서 잔여 | 40·46·49·55·56·58·65 |
| 이번 추가 미충족 | 50·51·54 |
| 미심사 | 없음 |

```text
미충족:
SITE-40 SITE-46 SITE-49 SITE-50 SITE-51
SITE-54 SITE-55 SITE-56 SITE-58 SITE-65

mismatch=10 unmet=10 unreviewed=0
```

같은 행의 복수 반례는 한 번만 셌다. 공용 역할표 SITE-26과 호출되지 못한 보존 함수 SITE-67을 소비 행과 중복 계수하지 않았다. SITE-54는 자신의 “재예외 금지”가, SITE-65는 자신의 후검출 처분이 직접 깨져 포함했다.

정적 계수는 다음과 같다.

```text
rows=68 extracted=1622
mismatch=0 unmet=0 unreviewed=0 grid=0
```

차이는 selector 누락이 아니라 **배정된 오류 경로·순서·처분의 미집행**이다. 역방향에서 찾은 외부 인자 평가, 법의 예외 포장, sandbox 후검출, 요청 형태 오류는 기존 행의 적용 범위 안이다. 대장 누락으로 중복 제출하지 않는다.

31~35차는 **12 → 12 → 9 → 10 → 10**이다. 전부 갈래 ⑴이어도 이번에는 T45 ③의 상신 조건을 함께 적용해야 한다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 성립 | 상류 의무의 도출 누락 반례 없음 |
| ② 신뢰·입력·부작용 경계 | 불성립 | 호출 영수증 보존 조건 T3의 잔여. 이번에 새 외부 쓰기 반례는 없음 |
| ③ 기제의 집행과 합성 | 불성립 | 후검출·진단 실패가 보존을 선점하고, sandbox IO와 인자 평가가 경계를 우회 |
| ④ 검증 근거 | 불성립 | 지정 회귀는 존재하지만 OG의 오류 조합·분기를 지지하지 못함 |
| ⑤ 미충족 상태의 처분 | 불성립 | sandbox IO→mismatch, 법 조회 실패→16, 지원 오류의 미처리 예외 종료 |

**A 폐쇄표**

`closed`는 기존 지적의 구체 경로 폐쇄다. 같은 SITE에 다른 OG가 생겼다는 이유만으로 모두 재개방하지 않았다.

| 지적 | 상태 | 대조 결과 |
|---|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed | 선등록·계수·발췌·기존 구동 통제 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed | 기존 종료·원장·결측·식별 연결 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed | 지문·스키마·요청/응답 결속 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed | 검사 집합·형태·소비·상태 연결 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed | 정합·법·렌더·재시도 연결 유지 |
| NU-1~4·NV-1~3·NW-1~5·NX-1~4·NY-1~4 | closed | 기존 지정 반례의 폐쇄 유지 |
| NZ-1·2·4·5 | closed | NZ-2 원본 선판별 잔여는 SITE-09·S47로 폐쇄 |
| NZ-3 | partially | 실패 처분 잔여 — OG-2~5 |
| OA-1·2·4·5 | closed | 결속·보존·봉인 집합·캐시 억제 유지 |
| OA-3 | partially | 법/환경 실패의 외곽 처분 잔여 — OG-2~4 |
| OB-1 | closed | SITE-02·03, C93·C86~89 — 결속 뒤 선판별 |
| OB-2 | closed | SITE-01·04~06, C94·S09·S11 — 공통 집합·후보 선검사 |
| OB-3 | closed | SITE-07~10, C95~97·S12 — 지정 자료/법 경계 |
| OB-4 | closed | SITE-11, S13 — evidence 보호·겹침 검사 선행 |
| OC-1·4·5 | closed | SITE-52·60·63/S21·S22, SITE-44/S17, SITE-15·57/S25·S26 |
| OC-2 | closed | S23·S37의 실패 분리와 SITE-27/S44의 refused 잔여 폐쇄 |
| OC-3 | partially | SITE-40 — sandbox IO의 후검출 파싱 선점, OG-2 |
| OD-1~5 | closed | 지정 출력·반대 역할·법 열거·git 봉투·내부 IO 경로 폐쇄 유지 |
| OE-1·2 | closed | SITE-55·56/S35의 원장 경계, SITE-23/S36의 절차 메타 오류 |
| OE-3 | partially | 선검증·refused 검출은 보강됐으나 후검출/보존/종결 조회 합성 잔여 — OG-1~3 |
| OE-4 | closed | 지정 13행 내부 포착 IO와 34차 필수 ENOENT·원본 파싱 순서 잔여는 S39·S46·S47로 폐쇄 |
| OE-5 | closed | SITE-50·51/S40의 scandir·부분 목록 경로 폐쇄. 요청 형태 오류는 OG-5로 구별 |

OF는 격자 연결까지 따로 대조했다.

| 지적 | 상태 | SITE · 격자 칸 · 회귀 |
|---|---|---|
| OF-1 | partially | SITE-58, retire×환경·후검출·자원 역할, S41. git 실패 뒤 진행은 폐쇄했지만 RunPaths 인자 실패의 처분 잔여 — OG-3 |
| OF-2 | closed | SITE-49, source×출력 경계, S42. source 첫 쓰기 전 공용 경계 연결 |
| OF-3 | closed | SITE-27·40·55·65, read/retire/metrics/replay×후검출, S44. 실제 `refused` 표식 포함 |
| OF-4 | partially | SITE-46·56·67, read×영수증 보존, S45. 정상 환경 outcome 전달은 폐쇄, 보존 진입 전 실패 잔여 — OG-1 |
| OF-5 | closed | SITE-40·55·68, read×자원 역할 및 소비 IO 판별, S46. 필수 request.md ENOENT를 IO로 보존 |
| OF-6 | closed | SITE-09·40, metrics/replay×IO 선판별, S47. **원본** 결속 → bound_fault → 포인터 파싱 |
| OF-7 | closed | SITE-63, source×준비 검사, S43. dispatch의 같은 준비 의무도 추가됨 |

**MY~OF 합계: closed 132 · partially 6 · open 0.**

직전 partially 8개 중 NZ-2·OC-2·OD-2·OE-4는 닫혔다. NZ-3·OA-3·OC-3·OE-3은 잔여가 있고, OF-1·4가 partially다.

**선검증과 러너 실물 대조**

세 핀의 `engine/paths.py`와 `engine/gitpin.py`는 각각 바이트 동일했다.

| 실제 내부 조회 | 선검증 대조 |
|---|---|
| `shadow_ledger_root → worktree_of`: `git -C realpath(repo) rev-parse --git-dir` | 동일 |
| 이어지는 `--git-common-dir` | 동일 |
| linked 분기의 `--git-common-dir` 재조회 | 동일 |
| linked 주 작업 트리 `isdir` | 선검증은 git-dir·common·main을 명시 stat하여 실패 분리 |
| source `resolve_pin`: 리포 isdir·common 조회·`status --porcelain -z`·HEAD·worktree 판별 | 실패를 정상 대체 값으로 접는 shadow 경로와 다름. 법은 실패를 전파하지만 구동 처분 연결에 OG-4 |

실제 함수의 하위 프로세스를 메모리로 관측해 비linked 2조회, linked 3조회의 **인자·capture/text 옵션·순서가 일치**함을 확인했다. shadow 조회의 선검증 누락 반례는 없다.

후검출은 `git-unavailable`, linked의 `main-worktree`, worktree 내부 원장 위치, `refused`, outcome 환경 표식과 실제 git 실패 봉투를 포함한다. 남은 문제는 표식 목록보다 **그 표식을 채집·파싱·전달하는 과정 자체의 실패**다.

**검증 경로**

Python은 모두 지정 인터프리터에 `PYTHONDONTWRITEBYTECODE=1`과 `-B`를 적용했다. 메모리 시험은 표준입력으로 실행했고 파일로 저장하지 않았다.

| 명령·검증 경로 | 마지막 출력·관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `c9362f6ac5698e86a73dcb51107f0114a3a9bf4e` · 마커 일치 |
| `hashlib.sha256` 지정 파일 대조 | 사용자 지정 지문 일치, v35·v36 지문도 일치 |
| SHA 목록의 동봉 파일 전량 대조 | `MANIFEST checked 15 mismatches []` |
| `t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | **`mismatch=0 unmet=0 unreviewed=0 grid=0`**, exit0 |
| `bundle/r6-grid-before.log` 판독 | `mismatch=0 unmet=0 unreviewed=0 grid=10` · `GRID_BEFORE_EXIT=4` |
| 격자 메모리 변이 | 준비 검사 후행 `grid=1`; `if False` 안 호출 `grid=0` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 파일 6개만 변경 · 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff d4e6ca2 origin/t40-base -- reader/procedure` | 출력 없음 |
| base→r1 및 base→r2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| 핀 계약을 `git show`로 공급한 실제 `lane_profiles()` | r0·r1·r2 모두 `registry_equal True` |
| 실제 shadow 함수 ↔ 선검증 조회 관측 | linked False/True 모두 `same_args True`, `same_root True` |
| `t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `처분=부적격 · 기준 런은 --law-tree … 필수`, **exit4** |
| 핀 법 62파일을 `git show`로 메모리 공급한 실제 `metrics()` | `complete`, 총163, component56, grounding56, fact14, implication20, positioning7, figure_note10 |
| 위 기준 검수 완료 | `MEMORY_BASELINE_DONE law_files=62 virtual_reads=80 actual_writes=0` |
| 실제 `CASES()` ↔ 회귀표 ID·최종 판정 열 | 165개, L13/F7/C95/X2/S48, ID 일치, **PASS165/FAIL0** |
| 발췌기 import·출력 메모리 대체 | 27단위, 종속항 N24, CL-2·4·7·9·12·14·16·19·21·24, `actual_writes=0` |
| 마지막 HEAD·주요 지문·`git diff --name-only` | 핀·지문 유지, `DIFF_TRACKED (empty)` |

기준 런 법의 비절차 파일은 사본과 바이트 동일함을 먼저 확인했다. 발췌 시험은 기준 자료를 각 입력에 공급한 **발췌 규칙 검증**이며 R0/R1/R2의 실측 결과 비교가 아니다.

**[미검증]**

- 165개 디스크 회귀는 재실행하지 않았다. 하네스·ID·기대·첨부 결과를 대조하고 OG 경로는 별도 메모리 시험으로 확인했다.
- 생산 실측, 실제 sandbox 쓰기, 디스크 source/read/dispatch/seal/retire는 실행하지 않았다. 메모리 시험에서는 경계·입력·실패를 선택적으로 대체했으며, 실제 디스크 장애의 종단 재현을 주장하지 않는다.
- `bundle/T40-VERIFY.log`는 동봉되지 않았다. 수정 전 격자 실패는 별도 `r6-grid-before.log`에서 확인했다. SHA 목록의 저작·갱신 보조 파일 14개도 부재하여 검증하지 못했다. 사용자 지정 운영·회귀 스크립트의 지문 불일치는 없었다.
- 실호출 모델/effort transcript, 외부 스테이징 실물, Owner의 정성 판정은 이번 검증 결과가 아니다.

**읽은 파일**

상류는 T40·T42·T43·T44·T45·T46 재정, D-02 §17 추기 38~53, 자문 4회차 답신, 31~34차 감수 원문을 읽었다. 대상은 v37 메모의 지정 절, 대장 JSON과 격자, J01~J60, resources·sites·drive·receipts·replay·metrics·excerpts·envelope·workflow, 회귀 본체·r4/r5/r6의 관련 사례, 회귀표·지문표·수정 전 격자 로그다.

법과 실물은 SPEC의 지정 G 항목, run-kinds·read 계약·승인 봉투 스키마, paths·gitpin·source/read 러너, 레인 contract·file_adapter·plan, convergence·run_checks 및 기준 런의 원천·run.yaml·명세·판정서·레인·원장 자료를 대조했다. 정본 리포는 읽지 않았고 허용된 인터프리터만 사용했다.

**게이트의 소견**

현재 방식이 수렴한다고 판정할 근거는 부족하다. 격자는 실제로 source·retire·dispatch의 배선 누락을 잡았고, 이번에도 이전 3행을 닫았다. 그러나 **오류를 처리하는 코드가 다시 실패하는 경로, 외부 함수에 들어가기 전 인자 평가, 같은 의무의 두 번째 실행 단계**에서 3행이 추가됐다. 남은 결손은 표의 크기보다 오류 경계의 합성에 있다.

Owner의 네 선택지 중 지금 가장 근거가 있는 것은 **자리 축소·대장화**다. 같은 의무를 따로 집행하는 경로 수를 줄이고, 호출 결과 보존과 실패 처분을 공통 경계에 모으는 조건에서다. **제한된 다음 판**도 이번 오류 전이와 처분 경계를 명시적으로 한정해 확인한다면 정당하다. **별도 탐색 단계**는 수집·검수·재정 허가를 분리하고 탐색 산출물을 채택 근거로 승격하지 않는 조건에서 가능하다. **보류·중단**은 추가 폐쇄의 가치가 비용을 정당화하지 못한다고 Owner가 판단할 때 가능하다.

이는 선택을 대신하는 재정이 아니라, **10 → 10과 결손 형태에 근거한 게이트 관측**이다. PASS 전 실측 착수 금지는 유지된다.