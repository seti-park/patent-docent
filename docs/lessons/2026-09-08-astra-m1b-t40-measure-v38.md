# 독립 감수 원문 — M1b 설계 도전 38차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v40(전이 구별·읽기 선확정·지배 검사 · 37차 OI-1~3 반영) · 판정 REVISE(MED 1) · **새 종류의 규칙 요구: 없음(3연속)** · PO 6 → 1

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `de45ca40bf87cfa1fd43eab412440a6bd5024783fadc0a9bb8cefff88705cda2` · 19582 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v38/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · START 09:26:44 · EXIT 0 · USAGE `input=4,603,351 cached=4,339,456 output=20,332 reasoning=5,048`. 사본 재핀 `9aae3b2` · 메모 v40 `fb12cc8f1e61961c` · PO 정본 `e703c5e3a6b48813` · 대장 `b431275e6369d641` · 회귀표 182 `16796e678dc9d9c4` · 지문표 `47c59c2636f2ed0d` · bundle 218. 이번 기동 = T44 자동(37차 조건) · 판정 방법 = PO 12 S/V/U + ⓐⓑⓒ + 「새 종류의 규칙 요구」.

**판정 = REVISE · 1건(MED 1 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 10차 · 발주·검수 총괄).** 지문 동봉 34 일치(미동봉 34 · 불일치 0) · 정적 `mismatch=0 unmet=0 unreviewed=0 grid=0` · `STRUCTURAL checks=260 violations=0` · FI 메모리 재현 `70 FAIL 0 P 41 M 29` · 심사 ①②③⑤ 성립 · **④ 검증 근거 불성립** · 갈래 ⑴ 1 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」(세 회차 연속)** · **PO 진행도 = `Satisfied=11 Violated=1 Unexamined=0` — 37차 6 대비 Violated 6 → 1 감소(비감소 조건 불성립)** · 보조 행 단위 `mismatch=2 unmet=2 unreviewed=0`(정적 집행 증거 미충족 · 지정 실행 반례 재개방 아님) · 미충족 SITE **32·58**. **A 폐쇄표 MY~OG = closed 143 · partially 0 · open 0** 유지 · OH-1·OH-2·OH-3 closed · OH-4 partially · OI-1·OI-2 closed · OI-3 partially. 37차 미충족 5행 중 SITE-03·09·14·61 폐쇄. 게이트의 첫 물음 답 = 「공동 함수는 명령·단계를 **명시 인자**로 받고(값 유무 추론 없음) · 읽기도 `read_closed` 로 원결과를 먼저 확정하며 · 지정된 두 변이는 검출된다. 남은 것 = **지배 검사가 선언 범위 전체가 아니라 일부 함수에만 적용된다**」.

**OJ-1 MED · PO-GATE-01 · SITE-58·32**: 같은 선언 범위 안에서 두 변이가 구조·대장 검사를 모두 통과한다. ⑴ `t40_structure.py:241` 의 `Machine.step` 검사는 조건식에 `self.stopped` 문자열이 있고 거부 본문이 실행을 끝내는지는 보지만 **stopped 가 실제 거부 조건으로 작동하는지**는 안 본다 — `t40_flow.py:107` 을 `if False and self.stopped or …` 로 바꾸면 첫 실패 뒤 `second` 효과가 실행되는데(`mutant … second_admitted True effects ['second']`) 검사는 `structural=0 mismatch=0 unmet=0 unreviewed=0 grid=0`. ⑵ `t40_structure.py:417` 의 `read_closed` 검사는 `finalize` 가 `tail` 보다 앞 **행**인지는 보지만 **cleanup 진입 전에 반드시 실행되는지**는 안 본다 — `t40_receipts.py:191` 의 `machine.finalize(result)` 를 `if False:` 로 감싸면 `business None · state read:Failure · return_error TransitionError` 로 읽기 업무 슬롯·cleanup 실행·종료 상태가 깨지는데 역시 전부 0. 두 변이는 명시적 제외 범위(일반 별칭·동적 코드·동시 교체)를 요구하지 않는 **상수 단락 평가와 죽은 분기**이며 두 함수 다 선언된 분석 대상이다. 게이트는 「현재 생산 코드에서 해당 변이의 실행 결함이 발생한다고 판정한 것은 아니다」라고 범위를 스스로 좁혔다.

**T44 판정** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ · 새 규칙 요구 없음 ✓ · **PO Violated 6 → 1 감소** → 자동 기동.

**처분 = 수용(공학) · 이행 = v41 저작(astra xhigh 11차).** 수정 문안(도전자 원문) — OJ-1 「선언된 검사 대상 전체에서 실패 거부 조건과 원결과 확정이 다음 효과·cleanup 을 실제로 지배함을 동일한 제어 흐름 규칙으로 검사하고, 해석하지 못하는 문법은 거부한다」. 게이트 소견 = 「다음 수리는 OJ 문자열 두 개를 추가하는 방식이 아니라 **이미 선언한 의무 전체에 같은 지배 의미를 집행하는 것**이어야 한다」.

**[미검증] 과 발주자 오류 둘** — ⑴ **SPEC 4행의 핀이 낡았다**: `9f82552`(v40 반입 **첫 시도** 시점의 HEAD)로 적혔고 실제 사본 핀·HEAD 는 `9aae3b2975b41f8502bc7ab4ff866b13f82dbd4c` 였다. 게이트가 `cat .audit-sandbox; git rev-parse HEAD` 3검증으로 잡아 실제 값으로 진행했으므로 판정에 영향은 없다. 총괄의 기동 전 점검(추기 64)은 **있어야 할 값의 존재만 grep 했고 실제 적힌 값을 보지 않아** 이것을 놓쳤다. ⑵ **R10 증거 미동봉**: `intake-v40.sh` 가 `R10-*` 산출물을 실행본으로 복사하지 않아 bundle 에 `r10-before/after/before-static.log` 3개만 들어갔다 — `R10-REPORT.md`·`R10-ARCHITECTURE.md` 및 PO 정본 `evidence_hashes` 12 중 10 이 부재. SPEC 읽기 순서 §3 이 `bundle/R10-REPORT.md` 를 **첫 자료**로 지목했는데 없었다. 게이트는 추정하지 않고 [미검증]으로 분리한 뒤 동봉 코드와 메모리 실행으로 증거를 다시 얻었으므로 판정은 성립한다(추기 62 의 probes 미동봉과 **같은 계열의 재발**). 보정 = 저작 작업장에서 R10 산출물 31 + 저작본 `regress-run.log` 를 실행본에 반입 → `evidence_hashes` **12/12 일치**(실행본 168 → 200 파일 · 낡은 `regress-run.log` 는 `regress-run.stale-0907.log` 로 보존). 그 밖의 [미검증] = 182 회귀 독립 디스크 재실행 안 함(표·기대 메타데이터·비교 코드는 확인) · 실제 R1/R2 legacy4/current5/metrics API 전 경로 미재실행 · 스테이징 원천·원격 Workflow 실호출·SIGKILL·전원 상실·동시 교체 미시험. 발주자 오류 누계 234 → **237**(OJ 1 + 낡은 핀 1 + R10 미동봉 1).

지적 열거 = OJ-1

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 38회)
새 종류의 규칙 요구: 없음

**PO 진행도: `Satisfied=11 Violated=1 Unexamined=0`.** 36차·37차의 Violated **10 → 6 → 1**로 감소했다. 이번 판의 비감소 조건은 성립하지 않는다. 대장 누락 반례는 **0**이다.

OI-1의 명령·단계 혼동과 OI-2의 읽기 원결과 소실은 폐쇄됐다. OI-3의 지정된 두 변이도 검출된다. 그러나 **같은 검사 범위 안에서 stop 조건과 읽기 결과 확정을 무효화한 새 변이 두 개가 구조·대장 검사 모두를 통과한다.** 남은 결손은 기존 PO-GATE-01의 증명 부족이다. 현재 생산 코드에서 해당 변이의 실행 결함이 발생한다고 판정한 것은 아니다.

**반입·지문 확인**

최초 `cat .audit-sandbox; git rev-parse HEAD` 결과, 실제 HEAD와 마커 pin은 모두 **`9aae3b2975b41f8502bc7ab4ff866b13f82dbd4c`**였다. 발주문에 적힌 `9f82552`와 다르다. path·order·disposable은 지정값이었다. 사본의 D-02 §17 추기63 정정과 커밋 이력에서 반입 보완·중단된 기동의 재개 기록을 확인했다.

심사 대상 메모·PO·대장·회귀표·스크립트 지문표의 sha16은 각각 **`fb12cc8f1e61961c`·`e703c5e3a6b48813`·`b431275e6369d641`·`16796e678dc9d9c4`·`47c59c2636f2ed0d`**로 일치했다. 스크립트 지문표는 **동봉 34개 일치·불일치 0·미동봉 34개**였다. 미동봉과 지문 불일치를 구별했다.

`R10-REPORT.md`를 비롯한 R10 보고서·결과 JSON은 동봉되지 않았다. 이 때문에 저작자의 R10 결과 파일을 확인했다고 처리하지 않았으며, 아래 실행 증거는 동봉 코드와 메모리 대역으로 다시 얻었다.

**OJ-1 · MED — 지배 검사가 공통 상태기계와 읽기 선확정 의무까지 집행되지 않는다**

- **위반:** `PO-GATE-01` — 정본 연결 I-A·I-C·I-S의 누락·우회 검사 의무. 새 변이의 실행 결과는 기존 I-A·I-F·I-R 위반으로 환원된다.
- **P/T:** P2·P7, 읽기 원결과 보존에서는 P4도 관련. T1~T4에 새 전제를 요구하지 않는다. 직접 심사 근거는 T45 ②·자문5회차 §12 F.
- **갈래:** ⑴.
- **자리:** **SITE-58·SITE-32**. 대장 누락이 아니라 배정된 의무의 검사 부족이다.

첫 번째 좌표는 [t40_structure.py:241](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:241)의 `Machine.step` 검사다. 조건식에 `self.stopped`라는 문자열이 있고 거부 본문이 실행을 끝내는지는 검사하지만, **stopped가 실제 거부 조건으로 작동하는지**는 검사하지 않는다.

[t40_flow.py:107](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_flow.py:107)에 다음 변이를 메모리에서 적용했다.

```python
# 원본
if self.stopped or self.state in ...

# 변이
if False and self.stopped or self.state in ...
```

최소 trace는 다음과 같다.

```text
first 효과가 E1로 실패
→ stopped=True, index=1, state=first:Failure
→ stopped 거부항은 False로 무효
→ step(second) 허용
→ second 효과 실행
```

독립 실행 결과:

```text
current first_identity True stopped True second_admitted False effects []
mutant  first_identity True stopped True second_admitted True  effects ['second']
```

그런데 변이의 검사 결과는 다음과 같았다.

```text
structural=0 mismatch=0 unmet=0 unreviewed=0 grid=0
```

두 번째 좌표는 [t40_structure.py:417](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:417)의 `read_closed` 검사다. `finalize`가 `tail`보다 앞선 행에 있는지는 보지만, **cleanup 진입 전에 반드시 실행되는지**는 보지 않는다.

[t40_receipts.py:191](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:191)에 다음 변이를 메모리에서 적용했다.

```python
# 원본
machine.finalize(result)

# 변이
if False: machine.finalize(result)
```

최소 trace와 실행 결과:

```text
read가 E1로 실패하여 Captured 생성
→ finalize 죽은 분기
→ business=None
→ tail('restore') 선행조건 거부
→ close 미실행
→ read:Failure 상태에서 TransitionError 반환
```

```text
READ_MUTANT ['read']
read_raw_kept True
business None
state read:Failure
return_error TransitionError
environment True
```

E1 객체는 실행의 `failures` 목록에 남는다. 따라서 “원 예외가 어디에서도 보존되지 않는다”고 과장하지 않는다. 깨진 것은 **읽기 업무 슬롯의 선확정·cleanup 실행·종료 상태**다. 이 변이 역시 다음 결과로 통과했다.

```text
structural=0 mismatch=0 unmet=0 unreviewed=0 grid=0
```

두 변이는 일반 별칭 분석·동적 코드·동시 교체 같은 명시적 제외 범위를 요구하지 않는다. R10이 다룬 **상수 단락 평가와 죽은 분기**이며, `Machine.step`과 `read_closed`는 선언된 분석 대상이다. 현재 생산 코드가 올바른 것과 그 의무의 무효화를 검사기가 검출하는 것은 별개다.

**고치는 문안:** “선언된 검사 대상 전체에서 실패 거부 조건과 원결과 확정이 다음 효과·cleanup을 실제로 지배함을 동일한 제어 흐름 규칙으로 검사하고, 해석하지 못하는 문법은 거부한다.”

**PO 12개 판정**

Satisfied는 고정된 지원 범위에서 코드 구조와 확인한 증거를 합친 판정이다. 회귀 개수만으로 정하지 않았으며, 변이 코드의 실행 위반을 원본 생산 코드의 PO에 중복 계상하지 않았다.

| PO | 상태 | 독립 근거와 공격 결과 |
|---|---|---|
| PO-EXEC-01 | **Satisfied** | 유한 진입·선행 증표 뒤 lazy thunk에서 인자와 효과를 실행한다. 미지 profile은 IO 전에 거부됐고 인자 평가 실패 FI에서 후속 효과가 차단됐다. |
| PO-RESULT-01 | **Satisfied** | `capture`의 예외 본문은 원 객체 대입 하나다. 현재 `read_closed`는 read 결과를 먼저 확정한다. author/copy/bytes의 read E1＋close E2에서 업무 E1·cleanup E2가 분리 보존됐다. |
| PO-FAIL-01 | **Satisfied** | 현재 `Machine.step`은 첫 실패 뒤 다음 효과를 거부한다. 독립 first/second trace에서 `effects=[]`. 생산 FI에서도 실패 뒤 업무 효과가 이어지지 않았다. |
| PO-STATE-01 | **Satisfied** | 정확한 Success와 stage/index를 요구한다. 명령·Admit·Complete가 명시 인자이며, 완료 객체 결측과 Admit 대체로 publication 성공을 만들지 못했다. |
| PO-IO-01 | **Satisfied** | 원본·child가 공용 pipeline을 사용한다. 같은 불변 IO-clear 객체의 전달을 확인했고 다른 identity에서는 parsing이 0이었다. 후채집 진단 실패에서도 정규화 0을 재현했다. |
| PO-PROFILE-01 | **Satisfied** | 공동 상태표를 생산·소비 양쪽이 집행한다. 정상 6·비정상 192 조합 및 R10 추가 profile 경계를 확인했다. 영수증의 다른 용도 profile은 쓰기 전에 거부됐다. |
| PO-PRESERVE-01 | **Satisfied** | intent 예약과 직렬화·write·flush·fsync·close·공개가 구별된다. 완료 결측은 공개 0·Failed·소비 거부였다. 파일 단계 FI에서 미완료 자료가 정상 소비로 승격되지 않았다. |
| PO-ENV-01 | **Satisfied** | 환경 확보·복원·복원 관측이 실행 경계에 있고 원결과와 별도 슬롯을 쓴다. 복원 실패 FI 및 다른 실패 조합에서 환경 판정과 원 객체 보존을 확인했다. |
| PO-RESOURCE-01 | **Satisfied** | 자원 역할 증표가 호출보다 앞서며 sandbox/법과 자료 실패를 구별한다. 공급·읽기 경계의 원 오류 보존과 기존 처분 연결을 확인했다. |
| PO-ISOLATE-01 | **Satisfied** | 출력 권한·보호 집합 검사가 보존·삭제보다 앞선다. 기존 격리 의무와 registry를 대조했고, 핀 법 62파일 및 사본의 관련 법 파일 동일성을 확인했다. 디스크 retire 재실행은 하지 않았다. |
| PO-SEMANTIC-01 | **Satisfied** | 핀 법을 메모리로 공급한 실제 baseline 검수가 성공했다. 봉투 v0 schema·발췌 27단위·표본 규칙을 재현했다. 기존 165의 기대 메타데이터와 registry가 유지됐고, 동봉 EQ 증거의 비교 방식도 확인했다. |
| PO-GATE-01 | **Violated** | OI-3 지정 두 변이는 검출하지만 OJ-1의 두 변이는 구조·대장 검사 모두 0이다. 선언된 분석 범위에 남은 의무를 문자열·행 순서만으로 승인한다. |

**합계:** `Satisfied=11 Violated=1 Unexamined=0`.

**보조 행 단위:** 독립 의미 심사 `mismatch=2 unmet=2 unreviewed=0`. 이는 저작 검사기의 출력 `0/0/0`과 구별한다. SITE-32·58의 **정적 집행 증거**가 미충족이며, 그 자리의 기존 지정 실행 반례를 재개방한 수치는 아니다.

**남은 목록:** Violated `PO-GATE-01`; Unexamined 없음; 미충족 SITE **32·58**.

ⓐ SITE 68행·PO 12개·대응표의 의무 연속성을 확인했다. ⓑ 적용 효과·파싱·하위 실행 중 새로 발견한 **미배정 반례는 0**이다. ⓒ 원본 실행에서 OI-1·2의 선행 증표·원결과·처분 공백은 닫혔으나, 이를 지배 검사로 보증한다는 주장에는 OJ-1이 남는다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | **성립** | 새 trace가 기존 I/PO로 환원된다. 상류 의무를 위해 새 규칙을 도입할 반례는 없다. |
| ② 신뢰·입력·부작용 경계 | **성립** | 현 생산 코드의 명령/profile 거부·자원 역할·출력 보호·원본/child 경계를 확인했다. 새 무배정 효과는 없다. |
| ③ 기제의 집행과 합성 | **성립** | 현재 코드에서 명시적 입장/완료 검사, read 선확정, 별도 cleanup, IO-clear 전달이 실제 실행을 제한한다. |
| ④ 검증 근거 | **불성립** | 두 유효한 의무 무효화 변이를 검사기가 승인한다. R10 원본 증거 파일도 일부 미동봉이다. |
| ⑤ 미충족·불명확 처분 | **성립** | 완료 결측은 공개되지 않으며 미완료 intent는 소비를 막는다. `.incomplete`·IO-clear·profile이 여섯 번째 처분을 만든 반례는 없다. |

따라서 PASS 문장 전체를 승인할 수 없다.

**A 폐쇄표**

`closed`는 기존 지적의 지정 반례가 닫혔다는 뜻이다. 새 지적의 면제 사유로 쓰지 않았다.

| 기존 지적 | 38차 판정 |
|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed 유지 |
| NU-1~4·NV-1~3·NW-1~5·NX-1~4·NY-1~4 | closed 유지 |
| NZ-1~5·OA-1~5 | closed 유지 |
| OB-1~4·OC-1~5·OD-1~5 | closed 유지 |
| OE-1~5·OF-1~7·OG-1~5 | closed 유지 |

**MY~OG: closed=143·partially=0·open=0.**

35차 미충족 **SITE-40·46·49·50·51·54·55·56·58·65**의 지정 trace는 폐쇄 유지다. 당시 partially 여섯 **NZ-3·OA-3·OC-3·OE-3·OF-1·OF-4**도 closed 유지다. OJ-1의 SITE-58은 새 검사 반례다.

| 지적 | 38차 판정 | 구조·회귀·FI 근거 |
|---|---|---|
| OH-1 | **closed** | 실제 `write_closed` 소유, 공급·표식 쓰기 실패의 원 객체·기존 처분·환경 보존 재현 |
| OH-2 | **closed** | 동일 IO-clear 전달, S59 identity 검사, 후채집 실패에서 정규화 0 |
| OH-3 | **closed** | 기존 상태표에 명령·Admit/Complete 구별 추가. 정상·비정상 profile 및 OI-1 경계 재현 |
| OH-4 | **partially** | 기존 변이는 검출하지만 선언 범위의 지배 검사에는 OJ-1 잔여 |
| OI-1 | **closed** | 다른 용도 profile은 쓰기 0. 완료 객체 결측은 공개 0·Failed·소비 거부. S63 및 메모리 profile 시험 |
| OI-2 | **closed** | author/copy/bytes 모두 read 원결과 선확정·close 별도 슬롯. S64의 읽기 9조합 및 원 E1＋E2 trace |
| OI-3 | **partially** | 지정 `io-false-and`·`close-dead-unwrap`은 각각 structural=1·grid=1. S65 추가 변이도 검출하지만 OJ-1 두 변이는 미검출 |

37차 미충족 5행 중 **SITE-03·09·14·61은 폐쇄**다. **SITE-32는 기존 읽기 trace가 폐쇄됐지만 새 정적 증거 결손이 남는다.**

**검증 경로**

아래 Python 실행은 모두 지정 인터프리터 `/home/laptop/projects/patent-docent/.venv/bin/python`에 `PYTHONDONTWRITEBYTECODE=1`·`-B`를 적용하고 사본에서 수행했다. 표의 `<PY>`는 이 접두를 뜻한다. 메모리 시험은 코드를 파일로 저장하지 않았다.

| 명령·검증 경로 | 마지막 출력 또는 판정에 사용한 관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 실제 pin/HEAD `9aae3b2975b41f8502bc7ab4ff866b13f82dbd4c`; 발주문의 HEAD와 차이 확인 |
| bundle에서 `sha256sum -c T40-SCRIPT-SHA256.txt` | exit 1: 동봉 34 일치·미동봉 34·내용 불일치 0 |
| `<PY> bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `rows=68 extracted=3772`; **`mismatch=0 unmet=0 unreviewed=0 grid=0`** |
| `<PY> bundle/t40_structure.py bundle` | **`STRUCTURAL checks=260 violations=0`** |
| `<PY> bundle/t40_probes_r10.py` | OI-1 공개 차단, OI-2 원/cleanup 분리; 마지막 OI-3 두 변이 각각 **structural=1·grid=1** |
| `<PY> bundle/t40_probes_r9.py` | 마지막 OH4 `structural=1 … detected=True`; 앞선 OH1~3 폐쇄 trace 재현 |
| `<PY>` 메모리에서 `t40_probes_r10.mutation_case`＋변경 모듈 `compile/exec` | OJ 두 변이 검사 전부 0. 마지막 출력 `READ_MUTANT … business None … return_error TransitionError environment True` |
| `<PY>` 원 FI29＋생산 witness16＋R10 생산25를 메모리 IO로 실행 | **`FI_MEMORY cases 70 FAIL 0 P 41 M 29`**; `MEMORY_ARTIFACTS 3 actual_writes=0` |
| `<PY> bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | **exit 4**: `[t40_metrics] 처분=부적격 · 기준 런은 --law-tree <t40-base 체크아웃> 이 필수다(절차 문서 09-01 판 · NR-3 재렌더 대조)` |
| `git ls-tree/show origin/t40-base`로 법 62파일을 메모리에 공급하고 실제 baseline `metrics()` 실행 | `BASELINE_SUCCESS True environment True law_reads 28 actual_writes=0` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 5파일 수정＋HISTORY 삭제만. 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 **`2 2 contracts/stages/read.yaml`** |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 출력 없음 |
| `git ls-tree origin/t40-base contracts/stages/read.yaml` | blob **`ea238e574d3cc7a71ae0547a1a4556b92e6dfc63`** |
| 세 핀의 부모 확인 | `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3` |
| 회귀 registry와 R8 호환 기준 비교 | 현재 182개, 기존 165 기대 메타데이터 변경 0, registry 동일 |
| 메모 v32·v39·v40 §5′.10 바이트 비교 | 모두 동일, **22,350 bytes·sha16 `33598684cfd07c2a`** |
| `t40_excerpts` import 후 출력 핸들만 메모리로 교체 | **27단위**, 표본 `CL-2·4·7·9·12·14·16·19·21·24`; 환경 정상·실제 쓰기 0 |
| `t40_envelope.main`을 `--write` 없이 호출하고 실제 parser/schema로 검증 | preview exit 0, **schema_errors=0**, `approval-envelope/v0`, `convergence_continue` |
| Python 소스 `compile()` 및 종료 시 상태 확인 | 동봉 `t40_*.py` 96개 문법 확인. 시작·종료 `git status --short` 동일, 캐시 생성 없음 |

FI 70건은 모두 같은 수준의 실물 관측으로 세지 않았다. **생산 관측 P41·모형 M29**를 분리했다. 자문 §8의 인자 평가·업무·직렬화·쓰기·flush/close·진단·cleanup·환경 복원·legacy 판별·parsing·validation·첫 효과·후속 효과 13지점에 대응하는 주입을 확인했다. 원 identity·후속 효과·종료 상태·소비 가능성·환경 판정도 해당 경로의 실제 관측과 모형 열을 구별했다. 업무가 시작되지 않는 profile 거부 사례를 업무 원 객체 보존의 실측으로 세지 않았다.

기준 런의 재계수는 **total 163, component 56, grounding 56, fact 14, implication 20, positioning 7, figure_note 10**으로 일치했다. 법 함수나 의미 검증기를 성공값으로 바꾸지 않고, 핀 파일 접근만 메모리로 공급했다.

**[미검증]**

- **R10 원본 증거 미동봉:** `R10-REPORT.md`·`R10-ARCHITECTURE.md`를 읽지 못했다. PO의 evidence hash 12개 중 동봉 2개는 일치했고 10개는 없었다. 부재 항목은 `regress-run.log`, `R10-FAULT-RESULTS.json`, `R10-PROFILE-RESULTS.json`, `R10-READ-FAULTS.json`, `R10-STATIC-MUTATIONS.json`, `R10-PROFILE-EQUIVALENCE.json`, `r10-sites-final.log`, `r10-structure-final.log`, `r10-invariants-final.log`, `R10-COMPAT-BASELINE.json`이다.
- **전체 182 회귀를 독립 디스크 실행하지 않았다.** 표의 182 PASS, 기존 165 기대 메타데이터 보존, 동봉 R8/R9 EQ 자료와 비교 코드는 확인했다. 이를 “현재 182건 독립 재실행 PASS”라고 보고하지 않는다.
- **실제 R1/R2의 legacy4/current5/metrics API 전 경로를 재실행하지 않았다.** 동봉 EQ 증거와 구현을 심사했으며 실측 모드·`replay()`·구동기 쓰기 명령은 실행하지 않았다.
- 스테이징 원천 전체, 원격 Workflow의 실제 모델·effort 호출, Owner의 최종 발췌 판독은 이번 실행 관측에 포함되지 않는다. SIGKILL·전원 상실·동시 교체도 시험하지 않았다.

이 한계와 별도로, PO-GATE-01은 **직접 재현한 반례로 Violated**다. 다른 PO는 명시한 코드 검토·직접 관측·기존 증거의 범위에서 판정했으며, 미동봉 자료의 내용을 추정하지 않았다.

**읽은 파일**

상류는 T40 §1·4·5, T42·T43, T44~T47, 자문5회차 발주문 전문, D-02 §17 관련 추기와 반입 정정, 35·36·37차 감수 원문이다.

설계·증거는 v40 지정 절과 이전 판 보존 대조 부분, R8/R9 보고서·구조 문서, R10 전후 로그, PO·SITE 대장·대응표·격자·지문표·회귀표, 동봉 R8/R9 fault/compat/profile/static/immutability 자료다.

구현은 `t40_flow`→`t40_consume`→`t40_drive`→`t40_replay`·`t40_metrics`→`t40_receipts`·`t40_resources`, 구조 검사 `t40_structure`·`t40_dominance`·`t40_sites`, 이관된 `t40_envelope`·`t40_excerpts`와 Workflow를 읽었다. 관련 invariant·profile·회귀·probe·witness 코드, SPEC §8.4 지정 항목, contracts, `engine/stages/read.py`·`engine/paths.py`·`engine/gitpin.py`, 기준 런 자료도 대조했다. 정본 리포는 읽지 않았고 지정 Python 인터프리터만 사용했다.

**소견**

이번 새 반례는 모두 기존 I의 위반 또는 그 검사 증거 부족으로 환원된다. 새 종류의 규칙 요구가 없다는 관측은 이어지며, 실행 구조의 결손은 실제로 줄었다.

다만 지배 분석이 일부 함수에만 적용되고 공통 상태기계·읽기 선확정에는 문자열과 행 순서 검사가 남아 있다. 다음 수리는 OJ 문자열 두 개를 추가하는 방식이 아니라 **이미 선언한 의무 전체에 같은 지배 의미를 집행하는 것**이어야 한다. 불변식 분류의 수렴 근거는 강화됐지만, 구현과 독립 게이트 증거의 폐쇄는 아직 완료되지 않았다.