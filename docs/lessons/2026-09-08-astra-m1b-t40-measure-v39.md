# 독립 감수 원문 — M1b 설계 도전 39차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v41(지배 검사의 적용 범위 일반화 · 38차 OJ-1 반영) · 판정 REVISE(MED 2) · **새 종류의 규칙 요구: 없음(4연속)** · PO 1 → 1(**비감소 1회**)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `8d3affbcc83587985896dadc1fa58b5f641e43a5b2a65e9aa02ed1e16e1ea050` · 14932 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v39/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · START 12:41:01 · EXIT 0 · USAGE `input=6,353,027 cached=6,128,512 output=25,664 reasoning=7,737`. 사본 재핀 `22567d4` · 메모 v41 `358dfc37c698fb79` · PO 정본 `569e28c29d6fcbbd` · 대장 `3a3d59045d274923` · 회귀표 186 `760c734a61e724b8` · 지문표 `9556765964b9ba33` · bundle 380. 이번 기동 = T44 자동(38차 조건) · **R10·R11 증거 전량 동봉**(38차 미동봉의 보정) · PO 증거 지문 **15/15 일치**.

**판정 = REVISE · 2건(MED 2 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 11차 · 발주·검수 총괄).** 지문표 80항 중 동봉 47 일치 · 미동봉 33 · 불일치 0 · 정적 `0/0/0 grid 0` · `STRUCTURAL checks=259 violations=0` · `DOMINANCE scopes=297 required=23392 checked=23392 difference=0 extra=0 unsupported=0` · 변이 `after 1107 detected 1107 undetected 0 domain_equal True` · FI 72(P 42 · M 30) · 심사 ①②③⑤ 성립 · **④ 검증 근거 불성립** · 갈래 ⑴ 2 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」(네 회차 연속)** · **PO 진행도 = `Satisfied=11 Violated=1 Unexamined=0` — 38차 1 과 같아 비감소 1회** · 보조 행 단위 `mismatch=2 unmet=2 unreviewed=0` · 미충족 SITE **14·32**(38차 58 은 폐쇄). **A 폐쇄표 MY~OG closed 143 · partially 0 · open 0** 유지 · OH-1~3·OI-1~2 closed · **OH-4·OI-3 partially** · **OJ-1 partially(지정 두 trace 는 closed)**.

**게이트의 첫 물음 답** = 「⑴ **규칙화는 진전했다** — 모든 추출 scope 에 같은 `Graph`·도달 판정식을 적용하며 OJ 두 함수를 더한 자리 목록이 아니다. ⑵ **입력 도출도 재현됐다** — `derive_inputs(bundle, CODE_FILES, COMMAND_STAGES)` 의 직렬화가 동결 입력과 전부 일치. 다만 `COMMAND_STAGES` 는 검사기의 명시 상수이고 선행 연산 어휘도 규칙으로 정의되어, 코드에서 뽑은 것은 **그 규칙의 적용 자리와 제어 관계**다. ⑶ **변이 도메인은 제한돼 있다** — 생성기는 terminal guard·Boolean 피연산자·선행 연산을 순회하고 형식은 `false-and` 672 · `dead-branch` 435 **둘뿐**이다. OJ 좌표를 모른다는 주장은 맞지만 **연쇄 비교는 생성하지 않는다**. ⑷ **문법 거부에 구멍이 남았다** — 직접 배치한 금지 문법 11 종은 거부하지만 **클래스 본문에 넣으면 조용히 통과**한다. 따라서 `23,392/23,392 · 차집합 0` 은 **추출된 모델 내부의 검사 완료**를 뜻하지, 그 모델이 Python 의 지원 제어 의미를 빠짐없이 반영한다는 근거가 아니다.」

**OK-1 MED · PO-GATE-01 · SITE-14·32 · 갈래 ⑴ — 연쇄 비교의 단락 평가를 순차 실행으로 해석한다.** 원인은 `t40_control.py:211` 의 `Graph.expression` — `BoolOp`·`IfExp` 에는 분기 처리가 있으나 **`Compare` 는 일반 자식 순회**라 마지막 호출이 실행된다고 계산한다. ⑴ `t40_receipts.py:191` 의 `machine.finalize(result)` → `0 > 1 > machine.finalize(result)`: 「open 성공 → read E1 → `0 > 1` 이 False → finalize 미실행 → tail('restore') 거부 → close 미실행 → TransitionError」 · 효과가 `read, close` → `read` 로 · 업무 슬롯 E1 → `None` · 상태 `Failed` → `read:Failure` · 반환 원 E1 → `TransitionError`. ⑵ `t40_receipts.py:323` 의 마지막 `result.unwrap()` → `0 > 1 > result.unwrap()`: 「write·flush·fsync 성공 → close E1 → unwrap 단락 → ClosedFile 반환」 · 원본은 E1 을 반환했는데 변이는 **`ClosedFile(path='memory', size=3)` 을 정상 반환**했다(내부 기계는 `Failed` 이나 외부 실행은 `Sealed`). 두 변이 모두 `STRUCTURAL 259/0` · `0/0/0 grid 0` · `DOMINANCE 차집합 0`. **일반 별칭·데이터 흐름·동적 코드가 필요한 반례가 아니다 — 상수 두 개와 Python 연쇄 비교의 평가 규칙만 썼다.** 고치는 문안 = 「지원 표현식의 실제 평가 순서와 단락 경로를 CFG 에 반영하고, **해석하지 않는 표현식은 위치 있는 위반으로 거부한다**」.

**OK-2 MED · PO-GATE-01 · SITE-32 · 갈래 ⑴ — 클래스 본문은 금지 문법 검사에서 빠진다.** `t40_control.py:101` 의 `direct` 가 `ClassDef` 에서 순회를 멈추고 `functions()` 가 클래스 본문을 scope 로 등록하지 않으며 `statement()` 도 클래스를 건너뛴다. 죽은 분기에 `class Hidden: assert False`(또는 `match None: case _: pass`)를 넣으면 — 직접 배치 `structural 2 · grid 2 · unsupported 1` ↔ **클래스 안 `0 · 0 · 0`**. 「죽은 코드에서도 미지원 문법을 거부한다」는 **현재 검사 의무 자체가 실행에서 깨진다**는 반례다. 고치는 문안 = 「문법 적격성 검사는 실행 가능성과 독립적으로 **선언 영역 전체를 순회**하고, 클래스 본문 등 **별도 해석하지 않는 영역은 명시적으로 거부한다**」.

**T44 판정** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ · 새 규칙 요구 없음 ✓ → 자동 기동. **다만 PO Violated 는 1 → 1 로 비감소 1회다**(T45 ③·T47 상신 조건 = 두 회차 연속 비감소 · 이번은 1회이므로 아직 상신 아님).

**총괄 관측(다음 판의 방향)**: 38차 이후 **모든 지적이 `PO-GATE-01` 하나에 모인다** — 생산 코드는 v40 이래 바이트 불변이고 설계 본체는 안정됐다. 남은 것은 **검사기가 자기 주장을 어디까지 증명하느냐**뿐이다. 그런데 지적의 자리는 매 회차 더 깊은 Python 문법 구석으로 내려간다(BoolOp → **Compare** → **ClassDef**). 자리별로 대응하면 다음 회차에 또 다른 구석이 나온다 — **PO 단위 진행도(Violated 수)가 1 에서 포화되어 더는 수렴을 재지 못하는 것**도 같은 사정이다. 게이트가 준 두 문안이 모두 **「해석하지 않는 것은 거부한다」** 인 것이 답이다: 통과를 기본값으로 두고 아는 것을 막는 방식(블랙리스트)에서, **해석 가능한 것만 통과시키고 나머지를 전부 위반으로 내는 방식(화이트리스트)** 으로 뒤집어야 순회가 끝난다. 12차 발주문의 핵심을 그것으로 잡는다.

**처분 = 전부 수용(공학) · 이행 = v42 저작(astra xhigh 12차).**

지적 열거 = OK-1, OK-2

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 39회)
새 종류의 규칙 요구: 없음

**`Satisfied=11 Violated=1 Unexamined=0`.** 지적 2건은 모두 **PO-GATE-01의 검출 근거 부족**, 갈래 ⑴이다. 현재 생산 코드의 실행 위반으로 중복 계상하지 않았다. 대장 누락 반례 0·상류 도출 누락 0·새 보증 요구 0이다.

38차의 Violated 1 → 이번 1이므로 **비감소 1회**다. 새 규칙 요구 없음은 4회 연속이다.

**고정 범위 확인**

마커의 path·pin·order·disposable과 HEAD `22567d412da7b56f889943fc9e062e8a98010a40`이 일치했다. 메모 `358dfc37c698fb79`, 지문표 `9556765964b9ba33`, 대장 `3a3d59045d274923`, PO `569e28c29d6fcbbd`도 일치한다.

지문표 80항 중 **동봉 47항 일치·미동봉 33항·내용 불일치 0**이다. PO의 현재 증거 지문은 **15/15 일치**했다. 생산 9모듈은 R11 동결 입력과 바이트 동일하다.

**이번 판의 첫 물음에 대한 답**

- **규칙화는 진전했다.** 모든 추출 scope에 같은 `Graph`·도달 판정식을 적용한다. OJ 함수 두 개를 추가한 자리 목록은 아니다.
- **입력 도출도 재현됐다.** `derive_inputs(bundle, CODE_FILES, COMMAND_STAGES)`의 JSON 직렬화 결과가 동결 입력과 전부 일치했다. 다만 `COMMAND_STAGES`는 검사기의 명시 상수이고, 선행 연산의 어휘도 `unwrap/finalize/require/require_completion/remember` 및 슬롯 규칙으로 정의한다. 코드에서 추출한 것은 그 규칙의 적용 자리와 제어 관계다.
- **변이 도메인은 제한돼 있다.** 생성기는 terminal guard·Boolean 피연산자·선행 연산을 순회한다. 형식은 `false-and` 672건과 `dead-branch` 435건뿐이다. OJ 좌표를 모른다는 주장은 맞지만, 아래 연쇄 비교는 생성하지 않는다.
- **문법 거부에는 구멍이 남았다.** 직접 배치한 금지 문법 11종은 거부하지만, 클래스 본문에 넣은 금지 문법은 조용히 통과한다.

따라서 의무 **23,392/23,392·차집합 0**은 추출된 모델 내부의 검사 완료를 뜻한다. 그 모델이 Python의 지원 제어 의미를 빠짐없이 반영한다는 근거는 아래 반례로 깨진다.

**OK-1 · MED — 연쇄 비교의 단락 평가를 순차 실행으로 해석한다**

**PO/I:** PO-GATE-01 검출 의무, 실행 증인은 I-R·I-P 위반 / **P/T:** SITE-14의 P2·T3, SITE-32의 P4·T2에 배정된 검증 근거 / **갈래:** ⑴ / **자리:** SITE-14·32 / **최소 trace:** 선행 호출을 연쇄 비교의 마지막 피연산자로 이동 → Python이 앞 비교에서 단락 → 선행 증표 없이 cleanup 또는 성공 반환 / **관측:** 두 변이 모두 구조·대장·격자 0 / **고치는 문안:** “지원 표현식의 실제 평가 순서와 단락 경로를 CFG에 반영하고, 해석하지 않는 표현식은 위치 있는 위반으로 거부한다.”

원인은 [t40_control.py:211](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_control.py:211)의 `Graph.expression`이다. `BoolOp`·`IfExp`에는 분기 처리가 있지만, `Compare`는 일반 자식 순회로 처리하여 마지막 호출이 실행된다고 계산한다.

① [read_closed:191](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:191)의 한 문장만 바꿨다.

```python
machine.finalize(result)
# →
0 > 1 > machine.finalize(result)
```

최소 실행:

```text
open 성공 → read E1 → 0 > 1이 False → finalize 미실행
→ tail('restore') 거부 → close 미실행 → TransitionError
```

| 관측 | 원본 | 변이 |
|---|---|---|
| 효과 | `read, close` | `read` |
| 읽기 업무 슬롯 | E1 | `None` |
| 파일 기계 상태 | `Failed` | `read:Failure` |
| 반환 오류 | 원 E1 | `TransitionError` |
| 환경 복원 | True | True |

E1은 변이에서도 실행의 `failures` 목록에 남는다. 소실된 것은 **읽기 업무 슬롯의 선확정·cleanup 실행·정상적인 실패 종결**이다.

② [write_closed:323](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:323)의 마지막 `result.unwrap()`만 바꿨다.

```python
entered = False
0 > 1 > result.unwrap()
return ClosedFile(path, len(raw))
```

최소 실행:

```text
write·flush·fsync 성공 → close E1
→ unwrap 단락 → ClosedFile 반환
```

원본은 E1을 반환했다. 변이는 **`ClosedFile(path='memory', size=3)`을 정상 반환**했다. 내부 파일 기계는 `Failed`이며 E1을 보존하지만, 외부 실행은 `Sealed`가 됐다.

두 변이 모두 다음 결과였다.

```text
STRUCTURAL checks=259 violations=0
mismatch=0 unmet=0 unreviewed=0 grid=0
DOMINANCE scopes=297 required=23392 checked=23392
difference=0 extra=0 unsupported=0
```

일반 별칭·데이터 흐름·동적 코드가 필요한 반례가 아니다. 상수 두 개와 Python 연쇄 비교의 평가 규칙만 사용했다.

**OK-2 · MED — 클래스 본문은 금지 문법 검사에서 빠진다**

**PO/I:** PO-GATE-01, I-A·I-C·I-S를 뒷받침하는 미분석 거부 의무 / **P/T:** P4·T2의 검증 근거 / **갈래:** ⑴ / **자리:** SITE-32 / **최소 trace:** 죽은 분기의 클래스 본문에 `Assert` 또는 `Match` → 순회 중 클래스에서 중단 → 별도 클래스 본문 scope 없음 → `unsupported=0` / **관측:** 구조·대장·격자 모두 0 / **고치는 문안:** “문법 적격성 검사는 실행 가능성과 독립적으로 선언 영역 전체를 순회하고, 클래스 본문 등 별도 해석하지 않는 영역은 명시적으로 거부한다.”

`read_closed`에 다음을 삽입했다.

```python
if False:
    class Hidden:
        assert False
```

`assert False` 대신 다음을 넣어도 같았다.

```python
match None:
    case _: pass
```

[direct:101](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_control.py:101)는 `ClassDef`에서 순회를 멈추고, `functions()`는 클래스 본문 자체를 scope로 등록하지 않는다. `statement()`도 클래스를 건너뛴다.

| 배치 | structural | grid | unsupported |
|---|---:|---:|---:|
| 죽은 분기에 직접 `Assert` | 2 | 2 | 1 |
| 죽은 분기의 클래스 안 `Assert` | 0 | 0 | 0 |
| 죽은 분기의 클래스 안 `Match` | 0 | 0 | 0 |

이 지적은 죽은 문장이 업무 오류를 일으킨다는 주장이 아니다. **죽은 코드에서도 미지원 문법을 거부한다는 현재 검사 의무가 실제 검사 실행에서 깨진다**는 반례다.

**PO 12개 판정**

Satisfied는 고정 지원 범위의 코드와 확인한 증거를 합친 판정이다. 변이 실행의 오류를 원본 생산 PO에 중복 계상하지 않았다.

| PO / I | 상태 | 독립 확인·최소 공격 결과 |
|---|---|---|
| PO-EXEC-01 / I-A | **Satisfied** | 미지 author profile은 환경 확보 효과 0으로 거부. 인자 실패 FI와 lazy 호출 경계를 확인했다. |
| PO-RESULT-01 / I-R | **Satisfied** | 원본 read E1＋close E2에서 업무·cleanup 슬롯과 객체 identity가 분리 보존됐다. author/copy/bytes 모두 재현했다. |
| PO-FAIL-01 / I-F | **Satisfied** | 첫 효과 실패 뒤 second 진입을 직접 시도했으나 거부·후속 효과 0. 파일 단계 FI도 통과했다. |
| PO-STATE-01 / I-A | **Satisfied** | Skip·NA·Failure의 Success 증표 대체를 각각 거부. 미완료 봉인·Admit 대체 공격도 차단됐다. |
| PO-IO-01 / I-C | **Satisfied** | 원본 IO는 `io-fault`, sandbox IO는 `infeasible`; 파싱 0. 다른 identity의 IO-clear도 파싱을 허가하지 않았다. |
| PO-PROFILE-01 / I-C | **Satisfied** | 명령·Admit/Complete·판본을 공동 표로 검사. 완료 결측과 다른 용도 profile을 거부하며 정상 조합은 수용했다. |
| PO-PRESERVE-01 / I-P | **Satisfied** | 원본 close 실패는 성공 반환을 막는다. 직렬화·write·flush·fsync·close FI에서 intent 유지·미완료 소비 거부를 재현했다. |
| PO-ENV-01 / I-E | **Satisfied** | 실패 복원 FI와 실제 cwd 변경을 포함한 성공/실패 왕복을 재현. 원결과·hook·법 namespace·cache·ContextVar 복원이 확인됐다. |
| PO-RESOURCE-01 / I-X | **Satisfied** | 중첩 자원에서 sandbox 역할 우선, 출처 없는 오류는 판정 불가. 원 오류 보존과 기존 처분 연결을 확인했다. |
| PO-ISOLATE-01 / I-X | **Satisfied** | 보호 대상과 겹치는 sandbox는 삭제·생성 효과 0으로 거부. 출력 선검사와 retire 보존→삭제 순서를 검토했다. |
| PO-SEMANTIC-01 / I-S | **Satisfied** | 실제 baseline 검수 `complete`·component 56. 소재 변조는 부적격. 발췌 27단위·고정 표본·봉투 schema 재현. 기존 182 기대·registry 및 동봉 EQ 비교 근거 확인. |
| PO-GATE-01 / 메타 의무 | **Violated** | 자동 변이 전건은 검출하지만 OK-1·2를 승인한다. 제어 의미와 문법 순회의 결손이다. |

**진행도:** `Satisfied=11 Violated=1 Unexamined=0`.

**보조 행 단위:** 독립 의미 심사 `mismatch=2 unmet=2 unreviewed=0`. SITE-14·32의 **검증 근거 배선**에 대한 수치이며, 정적 재고 출력 `0/0/0`과 구별한다.

**남은 목록:** Violated = `PO-GATE-01`; Unexamined 없음; 미충족 SITE = **14·32**. 38차 SITE-58의 stopped 잔여는 닫혔다. SITE-32는 새 검출 반례가 남고, SITE-14에는 새 검출 반례가 생겼다.

ⓐ 68행의 코드·증거·처분 배정과 SITE→PO 연속성을 확인했다. ⓑ **대장 누락 반례 0**이다. ⓒ 남은 공백은 위 두 행의 필수 검출 근거다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | **성립** | 새 반례 모두 기존 I/PO의 증거 부족으로 환원된다. |
| ② 신뢰·입력·부작용 경계 | **성립** | registry·세 핀의 차이·자원 및 출력 경계를 확인했다. |
| ③ 기제의 집행과 합성 | **성립** | 현재 생산 코드의 선확정·fail-stop·IO 증표·복원이 실행을 제한한다. |
| ④ 검증 근거 | **불성립** | 지원 제어 의미의 무효화와 금지 문법을 검사기가 승인한다. |
| ⑤ 미충족·불명확 처분 | **성립** | 다섯 처분·미완료 소비 거부·사람의 복구 절차가 유지된다. |

따라서 **PASS 문장 전체는 성립한다고 판정할 수 없다.**

**A 폐쇄표**

`closed`는 기존 지정 반례의 폐쇄이며 새 반례의 면제가 아니다.

| 기존 지적 | 이번 판정 |
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

**MY~OG = closed 143·partially 0·open 0.**

| 지적 | 판정 | 구조·회귀·FI 연결 |
|---|---|---|
| OH-1 | closed | `write_closed` 소유. 재조립 공급·표식 실패에서 원 오류 보존·후속 copy 0 재현. |
| OH-2 | closed | 동일 IO-clear 전달. 진단 실패 뒤 normalization 0 재현. |
| OH-3 | closed | Admit 선행·공동 완료 표. 미지 profile 읽기 0과 잘못된 projection 거부. |
| OH-4 | **partially** | 기존 변이 검출·P/M 분리는 확인. OK-1·2가 검출 근거에 남는다. |
| OI-1 | closed | S63·생산 FI: 완료 결측 publication 0·소비 거부. |
| OI-2 | closed | S64·읽기 FI: 업무 E1·cleanup E2·후속 0. |
| OI-3 | **partially** | 지정 두 변이는 검출됐으나 OK-1의 연쇄 비교는 미검출. |
| OJ-1 | **partially — 지정 두 trace는 closed** | 공통 CFG, S66/S67, FI-R11-STOPPED/READ와 자동 변이 전건으로 기존 stopped·dead-finalize는 검출. 선언 범위 전체의 보증에는 OK-1·2 잔여. |

**검증 경로**

`<PY>` = 사본 cwd에서 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B`. 인라인 하네스·변이·출력은 메모리에만 두었다.

| 명령·경로 | 마지막 출력 또는 핵심 관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 마커 일치, HEAD `22567d412da7b56f889943fc9e062e8a98010a40` |
| bundle에서 `sha256sum -c T40-SCRIPT-SHA256.txt` | 동봉 47 일치·미동봉 33·내용 불일치 0; exit 1 |
| `<PY> -c` → `structure.check`, `sites.compare/grid_compare` | `checks=259 violations=0`; 68행·3772자리·`0/0/0 grid=0` |
| `<PY> -c` → `derive_inputs`·`audit` | 동결 입력 JSON 동일; `297 / 23392 / 23392 / difference=0`; 동봉 의무 목록 동일 |
| `<PY> -c` → `variants` 전건·`compare_function` | `after 1107 detected 1107 undetected 0 domain_equal True` |
| `<PY> -c` → `grammar_rows`의 파일 출력 메모리화 | `rejected 11 positive=2 domain_attacks=2 actual_writes=0` |
| `<PY> -c` → OK-1 두 변이의 전체 검사·`compile/exec` | 검사 전부 0; 읽기 `business=None`; 쓰기 `ClosedFile` 정상 반환 |
| `<PY> -c` → OK-2 세 배치 비교 | 직접 Assert 거부; 클래스 안 Assert·Match는 전부 0 |
| `<PY> -c` → FI `main()`의 IO 메모리화 | `fault_cases=72 FAIL=0 production-observed=42 model=30` |
| `<PY> -c` → R9/R10 프로브 | OH 지정 trace 폐쇄; OI 지정 변이 structural/grid 각각 `11/11`, `5/5` |
| `<PY> -c` → `CASES()`·호환 기준 대조 | `existing=182 metadata_unchanged=182 total=186 registry_unchanged=True` |
| `<PY> -c` → 실제 baseline `metrics()`·핀 절차 바이트 메모리 공급 | `complete`, component 56, 환경 True, 실제 쓰기 0 |
| `<PY> -c` → 발췌 render·봉투 preview/schema | 27단위; 표본 CL-2·4·7·9·12·14·16·19·21·24; schema 오류 0 |
| `git diff`·세 핀 부모·법 파일 대조 | R1/R2는 각 read.yaml `2/2`; base는 절차 복원만. 법 62파일 확인 |
| v40↔v41 §5′.10 바이트 대조 | 동일, `22,350 B · 33598684cfd07c2a` |

**[미검증]**

- 디스크 픽스처를 만드는 **회귀 186 전건과 R1/R2 EQ 실행은 이번에 재실행하지 않았다.** 동봉 표·로그·코드 지문·기대 메타데이터와 비교 방식을 확인했다.
- 수정 전 검사기 1,107건은 재실행하지 않았다. 동봉 before 로그와 JSON 전행 동일성 및 검출 162·미검출 945를 확인했다.
- 미동봉 33항의 내용은 추정하지 않았다. 저작 작업장·정본을 읽는 불변성 검사 스크립트도 실행하지 않았다.
- FI의 파일 효과·일부 법/metadata 및 cwd는 메모리 대역을 사용했다. cwd·환경 성공/실패 왕복은 별도로 실제 변경·복원도 확인했다.
- 원격 Workflow 실호출·실측 3런·Owner 판독·전원 장애·동시 경로 교체는 수행하지 않았다. 정본 리포를 읽거나 수정하지 않았다.