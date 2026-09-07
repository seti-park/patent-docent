# 독립 감수 원문 — M1b 설계 도전 37차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v39(불변식 구현 결손 셋 폐쇄 · 36차 OH-1~4 반영) · 판정 REVISE(MED 3) · **새 종류의 규칙 요구: 없음** · PO 10 → 6

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `100f0e2d23afc608b84b88a3f5981ac11b3295feb1646de147ed2387b67f816d` · 17904 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v37/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · Monitor(02:20 기동 · 02:5x 종료 · USAGE 는 레인 STATUS). 사본 재핀 `e4bba1f` · 메모 v39 `bf2edc844529b790` · PO 정본 `2f84c33685ecdac3` · 대장 `e256e3be3cdec5b2` · 회귀표 179 · bundle 207. 이번 기동 = T44 자동(36차 조건) · 판정 방법 = PO 12 S/V/U + ⓐⓑⓒ + 「새 종류의 규칙 요구」.

**판정 = REVISE · 3건(MED 3 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 9차 · 발주·검수 총괄).** 지문 26 일치(미동봉 32 · 불일치 0) · 정적 0/0/0/grid 0 · STRUCTURAL 256/0 · 심사 ① 성립 · ②~⑤ 불성립 · 갈래 ⑴ 3 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」(두 회차 연속)** · **PO 진행도 = `Satisfied=6 Violated=6 Unexamined=0` — 36차 2/10/0 대비 Violated 10 → 6 감소(비감소 조건 불성립)** · 보조 행 단위 `5/5/0`(36차 9행 중 7 폐쇄 · 03·32 에 다른 trace · 새 09·14·61). **A 폐쇄표 MY~OG = closed 143 · partially 0 · open 0**(NZ-3·OA-3·OE-3·OF-4·OG-1 잔여 전부 폐쇄) · OH-1·OH-2 closed · OH-3·OH-4 partially. 게이트의 첫 물음 답 = 「직접 쓰기·사본 쓰기는 실제로 `write_closed` 에 모였고 후채집에는 같은 IO-clear 객체가 전달되며 공동 profile 상태표도 존재한다. 남은 것 = **입장 검사와 완료 검사의 구분 · 읽기 결과와 닫기 실패의 분리 · 정적 검사의 실제 지배 조건**」. **OI-1 MED · I-A·I-C·I-P · SITE-03·14**: `receipt_admit` 이 영수증 명령의 허용 판본(정수 4/5)을 요구하지 않아 `current5`·`baseline`·`envelope-v0` 같은 다른 용도 profile 도 Admit 통과 · `check_profile:63` 의 「outcome·execution 둘 다 None 이면 입장 검사」 반환 때문에 완료 객체 결측 영수증이 `profile=Success → publish → Sealed`(후속 `load_receipts` 는 거부 · 그러나 완료 증표 없는 파일을 공개하고 정상 반환). **OI-2 MED · I-R · SITE-32·61**: 직접 읽기(`author_input.read` · `read_bytes` · `copy_file_closed`)가 `with …: return handle.read()` 형태라 read 실패 E1 을 `Captured` 로 확정하기 전에 `__exit__` 의 close 실패 E2 가 원결과 슬롯을 차지(E1 은 `__context__` 에만). **OI-3 MED · PO-GATE-01**: 선언된 문법 안에서 두 변이(`io_gate` 의 `if RC.is_io_fault(outcome)` → `if False and …` · close 뒤 `result.unwrap()` → `if False: result.unwrap()`)가 구조·대장 검사 모두 0 — 검사기가 `unwrap` 존재 6개와 위치는 보지만 성공 해제가 반환을 **실제로 지배**하는지, 증표 생성이 IO 거부 조건 **뒤에서만** 가능한지는 안 봄.

**게이트 소견(요지)**: 「분류 체계는 이번 공격에서도 닫혀 있었다 · 구현도 실제로 전진(쓰기 소멸자 경로·후채집 독자 허가 폐쇄) · 남은 결손은 공동 함수의 존재보다 **그 함수가 받는 전이의 구별과 결과 확정 시점** — 입장 검사 결과가 완료 증표가 될 수 있고 · 읽기 결과가 닫기보다 늦게 확정되며 · 검사기가 호출 존재를 실제 지배로 센다.」 [미검증] 에 **`r9-probes.py` 미동봉**(S59·S60 의 실제 의존 · 총괄 bundle 복사 패턴이 `r*-probes.py` 를 빠뜨림 → 발주자 오류 · 실행본 디렉터리에도 복사 누락 → 즉시 보정).

**T44 판정** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ · 새 규칙 요구 없음 ✓ · **PO Violated 10 → 6 감소** → 자동 기동.

**처분 = 전부 수용(공학) · 이행 = v40 저작(astra xhigh 10차).** 수정 문안(도전자 원문) — OI-1 「공동 검사에 명령과 검사 단계(Admit/Complete)를 명시하고, 영수증 Admit 은 정수 4/5 만, current5 Complete 는 outcome·execution·전체 완료 증표를 필수로 요구한다」 · OI-2 「직접 읽기도 read 의 반환·예외를 close 보다 먼저 확정하고, close 결과는 별도 cleanup 슬롯에 기록하여 원 읽기 결과를 대체하지 못하게 한다」 · OI-3 「IO 증표 발급과 ClosedFile 반환까지의 경로에서 거부 조건 및 각 Success 해제가 실제로 지배함을 검사하고, 실행 불가능 분기 속 호출은 증거로 세지 않는다」. 발주자 오류 누계 228 → **232**(OI 3 + probes 미동봉 1).

지적 열거 = OI-1, OI-2, OI-3

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE  
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 37회)  
새 종류의 규칙 요구: 없음

**지적 3건 모두 기존 불변식의 구현 위반 또는 증거 부족이다.** 진행도는 **`Satisfied=6 Violated=6 Unexamined=0`**이다. 36차의 Violated 10에서 감소했으므로 이번 비감소 조건은 성립하지 않는다.

사본 path·pin·order/disposable과 HEAD `e4bba1f63a3ac3b03f8a81e4837c7326cba8999b`를 확인했다. 메모 v39·v38·회귀표·지문표의 지정 지문은 일치했다. 지문표 대상은 **동봉 26개 일치·미동봉 32개·불일치 0개**다.

이번 첫 물음에 대한 답은 다음과 같다. 직접 쓰기와 사본 쓰기는 실제로 `write_closed`에 모였고, 후채집에는 같은 IO-clear 객체가 전달된다. 공동 profile 상태표도 존재한다. 그러나 **입장 검사와 완료 검사의 구분, 읽기 결과와 닫기 실패의 분리, 정적 검사의 실제 지배 조건**이 남아 있어 PASS 문장은 성립하지 않는다.

**OI-1 · MED — 공동 profile 검사가 다른 명령의 profile과 미완료 영수증의 공개를 허용한다.**

- 위반: **I-A·I-C·I-P / PO-EXEC·STATE·PROFILE·PRESERVE-01**.
- P7·T3, 갈래 **⑴**, **SITE-03·14**.
- 좌표: [t40_consume.py:45](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_consume.py:45) `check_profile`; [t40_receipts.py:367](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:367) `receipt_admit`, `write_receipt:398`.

첫째 최소 trace:

```text
write_receipt(version='current5' 또는 'baseline' 또는 'envelope-v0')
→ 전역 profile 이름으로 Admit 성공
→ intent 기록 → 영수증 기록·close
→ 완료 상태표 검사 없이 성공
→ intent 제거 → 정상 경로 반환
```

`receipt_admit`은 영수증 명령의 허용 판본인 정수 4/5를 요구하지 않는다. 공용 함수에 명령을 전달하지 않아 다른 용도의 profile도 통과한다.

둘째 최소 trace:

```text
정수 version=5
→ outcome·execution 두 객체 결측
→ write_receipt의 완료 검사
→ check_profile:63의 “둘 다 None이면 입장 검사” 반환
→ profile=Success → publish → Sealed
```

저작자의 정상 `make_receipt()`에서 **outcome과 execution만 제거**하고 실제 writer를 메모리 파일 대역으로 실행했다.

```text
CURRENT_MISSING_COMPLETION
writer_success=True
receipt-publication=Sealed
published=True
loader_accept=False
environment=True
actual_writes=0
```

다른 용도의 세 profile도 writer 성공·공개를 재현했다. 후속 `load_receipts`는 거부했다. 따라서 잘못된 지표의 최종 승격을 주장하는 것은 아니다. **완료 증표가 없는 파일을 공개하고 정상 작성 결과로 반환한 것**이 위반이다.

S60의 정상 6조합·비정상 192조합은 재현했지만, 그 시험은 outcome 객체가 있는 상태에서 stage를 변형한다. 두 완료 객체가 함께 없어서 입장 검사로 되돌아가는 경로와 명령 간 profile 혼입을 덮지 않는다.

**수정 문안:** “공동 검사에 명령과 검사 단계(Admit/Complete)를 명시하고, 영수증 Admit은 정수 4/5만, current5 Complete는 outcome·execution·전체 완료 증표를 필수로 요구한다.”

**OI-2 · MED — 읽기 실패 뒤 close 실패가 원결과 슬롯을 차지한다.**

- 위반: **I-R / PO-RESULT-01**.
- P2·P4·P7, 갈래 **⑴**, **SITE-32·61**.
- 좌표: [t40_consume.py:102](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_consume.py:102) `author_input.read`; [t40_receipts.py:175](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:175) `read_bytes`, 이를 사용하는 `copy_file_closed`.

최소 trace:

```text
허용된 작성 입력 또는 사본 입력
→ handle.read에서 E1
→ E1을 Captured로 확정하기 전에 with.__exit__
→ close에서 E2
→ 바깥 capture가 E2를 원결과로 확정
```

실제 `io.BufferedReader`와 메모리 `RawIOBase`의 read·close에 각각 별도 예외를 주입했다.

```text
author_input:
trace=['read_failure','close_failure']
first_captured=False
second_captured=True
io=Failure(close E2)
environment=True

copy_file_closed:
first_captured=False
second_captured=True
later_write=0
environment=True
actual_writes=0
```

**E1은 E2의 `__context__`에는 남는다.** 소실 범위는 독립된 원결과 슬롯이다. 원 읽기 실패와 cleanup 실패를 별도 `Captured`로 보존한다는 I-R의 구조가 이 경로에는 없다.

쓰기의 `write_closed`는 첫 실패를 먼저 확정하고 cleanup을 분리한다. 읽기는 여전히 `with …: return handle.read()`여서 같은 보장이 성립하지 않는다. FI 45의 기존 기대는 모두 재현했지만, 이 읽기·닫기 이중 실패는 포함되지 않았다.

**수정 문안:** “직접 읽기도 read의 반환·예외를 close보다 먼저 확정하고, close 결과는 별도 cleanup 슬롯에 기록하여 원 읽기 결과를 대체하지 못하게 한다.”

**OI-3 · MED — 선언된 정적 분석 범위에서도 IO 거부와 close 성공 증표의 지배를 확인하지 못한다.**

- 위반: **PO-GATE-01**, 관련 **I-A·I-C·I-S**의 증거 의무.
- P2·P7, T45 ②·자문 §12 F, 갈래 **⑴**.
- 자리: **SITE-09·14의 검사 증거**.
- 좌표: [t40_structure.py:404](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:404) `closed_file_checks`; [t40_structure.py:416](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:416) `capability_checks`.

지정 OH-4 변이는 검출됐다.

```text
raw_only = False and (not C.has_io_clear(clear, outcome))
→ structural=1
→ sites exit4, grid=1
```

그러나 다음 두 변이는 검출되지 않았다. 모두 파일을 수정하지 않고 검사기의 읽기 입력만 바꿨다.

| 최소 변이 | 구조 검사 | 대장 검사 |
|---|---:|---|
| `io_gate`의 `if RC.is_io_fault(outcome)`을 `if False and RC.is_io_fault(outcome)`으로 변경 | 0 | `0/0/0 grid=0`, exit0 |
| close 다음 `result.unwrap()`을 `if False: result.unwrap()`으로 변경 | 0 | `0/0/0 grid=0`, exit0 |

두 번째 변이의 실행 결과도 메모리로 확인했다.

```text
close 실패
→ unwrap 미실행
→ ClosedFile 반환 성공
→ file-publication 내부 상태는 Failed
```

파일 검사는 `unwrap` **6개 존재**와 close 뒤 생성자 위치를 확인하지만 성공 해제가 반환을 실제로 지배하는지는 확인하지 않는다. IO 검사는 증표 생성자가 하나인지 확인하지만 그 생성이 IO 거부 조건 뒤에서만 가능한지는 확인하지 않는다.

이는 선언된 `io_gate`·`write_closed`와 `if` 문법 안의 반례다. 일반 Python 별칭·동적 코드의 형식 증명을 요구하지 않는다. 원본 코드의 IO·fail-stop 위반으로 중복 계수하지 않고 **검사 증거의 결손**으로 판정했다.

**수정 문안:** “IO 증표 발급과 ClosedFile 반환까지의 경로에서 거부 조건 및 각 Success 해제가 실제로 지배함을 검사하고, 실행 불가능 분기 속 호출은 증거로 세지 않는다.”

**PO 독립 판정**

| PO | 상태 | 독립 근거와 반례 탐색 결과 |
|---|---|---|
| PO-EXEC-01 | **Violated** | lazy 인자 실패와 지원 진입 거부는 재현. 영수증 명령에 다른 profile을 주어도 쓰기가 실행됨 — OI-1 |
| PO-RESULT-01 | **Violated** | runner·외부 observer·writer의 원결과 보존 FI는 재현. 직접 읽기의 E1→close E2에서 원 슬롯 분리 실패 — OI-2 |
| PO-FAIL-01 | **Satisfied** | first/later effect FI, 실제 writer의 BufferedWriter flush 실패를 재현. `step`의 stop과 순차 unwrap이 후속 업무를 차단하며 cleanup만 별도로 실행 |
| PO-STATE-01 | **Violated** | Skip/NA·미완료 seal·봉인 후 tail 거부는 재현. 완료 객체 없는 current5가 profile Success·Sealed로 공개됨 — OI-1 |
| PO-IO-01 | **Satisfied** | 원본/child 거부·증표 없는 파싱 거부·OH-2 진단 실패 후 정규화0 재현. 실제 후채집과 소비 stage는 같은 객체를 요구 |
| PO-PROFILE-01 | **Violated** | 정상6·비정상192 및 미지 profile 거부는 확인. 명령별 허용 집합과 Admit/Complete 구별 결손 — OI-1 |
| PO-PRESERVE-01 | **Violated** | 직렬화/write/flush/fsync/close 실패의 intent 유지 재현. 완료 정보 결측을 공개 전 거부하지 못함 — OI-1 |
| PO-ENV-01 | **Satisfied** | 환경 성공/실패·복원 자체 실패 FI와 실제 지원 진입8개 복원 재현. 확보 항목별 복원·검증이 유지됨 |
| PO-RESOURCE-01 | **Satisfied** | 자원 역할표·sandbox 우선순위·미상 거부 및 외부 실패 원인 전달 확인. BufferedWriter 실패는 환경 실패로 보존됨 |
| PO-ISOLATE-01 | **Satisfied** | 보호 집합 선검사·목적지 경계·링크 거부와 관련 음성 증거 확인. 새 원본 침범 반례 없음 |
| PO-SEMANTIC-01 | **Satisfied** | 기준 검수 complete, 좌석3핀, 발췌27/표본10, 봉투 검증, 정규화·기존 회귀 기대의 연속성 확인. 새 지표·권한·임계 변경 반례 없음 |
| PO-GATE-01 | **Violated** | SITE68·격자56·회귀 metadata 연속성 확인. 선언된 문법 안의 두 의미 무효화 변이가 검사0 — OI-3 |

**`Satisfied=6 Violated=6 Unexamined=0`**

Satisfied는 명시된 지원 범위와 구조·증거를 함께 심사한 판정이다. 디스크 실측이나 임의 Python 전체의 증명을 뜻하지 않는다.

보조 진행도는 **`mismatch=5 unmet=5 unreviewed=0`**이다.

- 남은 PO: **EXEC·RESULT·STATE·PROFILE·PRESERVE·GATE-01**.
- 미충족 SITE: **03·09·14·32·61**.
- SITE-09는 검사 증거 결손이며, 원본 IO 분기의 실행 위반은 아니다. SITE-14는 구현·증거 결손을 한 번만 셌다.
- ⓑ **대장 누락 반례 0**. 발견한 호출은 기존 SITE에 배정돼 있다.
- 도출 누락0·새 보증 요구0·지적 전부 갈래⑴.
- 36차 미충족9행 중 **7행 폐쇄**, 03·32에는 다른 최소 trace가 남았다. 신규 미충족은 09·14·61이다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | **성립** | 새 반례 모두 기존 I/PO로 환원 |
| ② 신뢰·입력·부작용 경계 | **불성립** | 영수증 command/profile 거부 전에 허용되지 않은 쓰기·공개 |
| ③ 기제의 집행과 합성 | **불성립** | 읽기 결과와 cleanup 혼합, 입장 검사로 완료 검사 대체 |
| ④ 검증 근거 | **불성립** | FI45는 재현됐으나 새 오류 조합을 덮지 않으며 정적 지배 검사에 공백 |
| ⑤ 미충족 상태의 처분 | **불성립** | 미완료 영수증 writer가 정상 경로를 반환하고 공개 표식을 제거 |

`.incomplete`·IO-clear·legacy4/current5가 **여섯 번째 처분을 추가한 반례는 없다**. OI-1은 기존 공개·거부 전이의 잘못된 선택이다. 후속 소비기는 해당 자료를 거부했다.

**A 폐쇄표**

`closed`는 기존 지정 반례의 폐쇄다. 같은 자리에서 발견한 OI를 자동 면제하지 않는다.

| 기존 지적 | 판정 |
|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed 유지 |
| NU-1~4·NV-1~3·NW-1~5·NX-1~4·NY-1~4 | closed 유지 |
| NZ-1~5·OA-1~5 | closed。NZ-3·OA-3의 OH-1 쓰기 실패 처분 잔여 폐쇄 |
| OB-1~4·OC-1~5·OD-1~5 | closed 유지 |
| OE-1~5·OF-1~7·OG-1~5 | closed。OE-3·OF-4·OG-1의 OH-2 후채집 잔여 폐쇄 |

**MY~OG: closed143 · partially0 · open0.** 35차 미충족10행의 지정 경로도 모두 폐쇄됐다.

| 36차 지적 | 이번 판정 | 구조·회귀·FI 대조 |
|---|---|---|
| OH-1 | **closed** | 공급 파일이 `write_closed` 사용. 실제 BufferedWriter 실패에서 원 예외 보존·later0 재현. S58 공급6종 기록과 writer FI 대조 |
| OH-2 | **closed** | `carry_io_clear`→`receipt_post`→완료 검사 전달. 진단 실패에서 정규화0·semantic Skip 재현. S59·생산 FI 연결 |
| OH-3 | **partially** | 지정 projection 3종·미지 작성 profile trace는 폐쇄. 정상6/비정상192 재현. 명령·검사 단계 구별에는 OI-1 |
| OH-4 | **partially** | 지정 변이 structural1, 생산16/모형29 분리 확인. 다른 두 직접 지배 변이는 검사0 — OI-3 |

**검증 경로**

Python은 지정 인터프리터에 `PYTHONDONTWRITEBYTECODE=1`·`-B`를 적용했다. 메모리 시험은 표준입력으로 실행했고 파일로 저장하지 않았다.

| 명령·경로 | 마지막 출력 또는 핵심 관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 지정 마커·`e4bba1f63a3ac3b03f8a81e4837c7326cba8999b` 일치 |
| 지문표 전량 대조 | `matched=26 absent=32 mismatches=[]` |
| `bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `rows=68 extracted=3753`; **`mismatch=0 unmet=0 unreviewed=0 grid=0`**, exit0 |
| `t40_structure.check('bundle')` | **`STRUCTURAL checks=256 violations=0`** |
| OH-4 및 추가 메모리 변이 | 지정 변이1; IO_GATE·CLOSE_UNWRAP 각각0 |
| `git diff --numstat 6d92cad origin/t40-base` | 절차6파일만 변경; 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base→R1 / base→R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| 핀 계약을 `git show`로 공급한 실제 `lane_profiles()` | `SEATS r0 True`, `r1 True`, `r2 True` |
| 지정 기준 런 `t40_metrics.py … --baseline`, 법 인자 없음 | 요구대로 **exit4·부적격** |
| 핀 법62파일 메모리 공급 후 실제 `metrics(..., baseline=True)` | **complete·component56**, 법 가상 읽기80·환경True·쓰기0 |
| FI 함수별 메모리 재실행 | **production16 FAIL0·model29 FAIL0** |
| 실제 지원 진입 거부·복원 | **8/8** |
| 공동 current5 상태표 독립 대조 | **valid6·invalid_rejected192** |
| `CASES()` ↔ 호환 기준 metadata | 기존165·174 모두 변경0, registry 동일 |
| 회귀표 ↔ 현재 사례 ID·판정 | **179행·ID 일치·PASS179** |
| 동봉 v15 회귀표의 최종 판정 열 대조 | 기존157행 변경0 |
| §5′.10 v32·v37·v38 대조 | 22,350바이트 동일·sha16 `33598684cfd07c2a` |
| SITE·격자 역사 대조 | **68행 원문·56칸 historical 동일** |
| 발췌기 import·렌더 결과 메모리 수집 | **27단위**, N24·표본10·CL-2/4/7/9/12/14/16/19/21/24 |
| 봉투 `--write` 없는 미리보기→실제 러너 검증기 | **`(True, '계속 봉투 유효(판정서 지문 결속 확인)')`** |
| 최종 HEAD·tracked diff·생성물 검색 | HEAD 유지·diff 빈 출력·해당 생성물 없음 |

FI의 자문 §8 **명목 13지점은 모두 연결**돼 있다. 생산16행에서는 원 identity·후속 효과·상태·실제 소비 거부·환경을 실행 코드로 확인했다. 기존29행의 모형 값은 분리돼 있다. 이 태그 수정은 인정한다. 다만 45개 성공이 OI-1·2의 조합을 덮는 증거는 아니다.

**[미검증]**

- 디스크 회귀179건, 실제 R0/R1/R2의 legacy/current 재조립 실행쌍은 재실행하지 않았다. 하네스·metadata·결과표·동치 JSON을 대조했다. 기존165 전체의 구판 실제 관측열과 신판 관측열의 바이트 동일성까지 확인한 것은 아니다.
- `r9-probes.py`는 미동봉32개 중 하나이며, **S59·S60이 사용하는 실제 의존 파일**이다. `t40_regress_r9.probes()`는 `FileNotFoundError`를 재현했다. 해당 핵심 trace는 별도 메모리 시험으로 재검증했으나 동봉 하네스 전체의 실행 가능성을 주장하지 않는다.
- S58의 실제 재조립 공급6종은 첨부 기록·호출 코드를 확인했다. 이번 독립 실행은 공통 writer와 실제 BufferedWriter 실패 경계까지다.
- 봉투·발췌의 현행 서식·규칙은 검증했지만 이관 전 스크립트 전체와의 바이트/AST 동치는 확인하지 못했다.
- 생산 실측, `replay()` 실효과 실행, 구동기 디스크 쓰기, Workflow 모델 호출, 외부 스테이징 실물과 Owner 정성 판정은 실행하지 않았다.

**읽은 파일**

상류는 T40·T42~T47 재정, 자문5회차 발주문 전문, D-02 §17 추기54~61, 35·36차 감수 원문이다. 설계·증거는 R9 보고서와 전후 로그, R8 보고서·R8/R9 architecture, v39 지정 절과 이전 판 대조 절, PO12·SITE68·SITE→PO·격자, 지문표·회귀표·R8/R9 fault/compat/profile/static/immutability 자료 및 관련 시험 코드다.

생산 코드는 flow→consume→drive→replay/metrics→receipts/resources→structure/sites→envelope/excerpts 순서로 읽었다. SPEC 지정 G 항목, 핀 계약, read·paths·gitpin·lane plan과 기준 런 산출물을 대조했다. 정본 프로젝트 파일은 읽지 않았으며 허용된 인터프리터를 사용했다.

**소견**

새 반례는 모두 기존 I의 위반으로 환원된다. **분류 체계는 이번 공격에서도 닫혀 있었다.** 구현도 실제로 전진했다. 쓰기 소멸자 경로와 후채집의 독자 IO 허가는 닫혔다.

남은 결손은 공동 함수의 존재보다 **그 함수가 받는 전이의 구별과 결과 확정 시점**에 있다. 입장 검사 결과가 완료 증표가 될 수 있고, 읽기 결과가 닫기보다 늦게 확정되며, 검사기는 호출 존재를 실제 지배로 세는 자리를 남겼다. 따라서 관측된 감소는 **10→6**이지만, 구현과 증거의 폐쇄는 아직 성립하지 않는다. 이는 게이트 관측이며 재정이 아니다.