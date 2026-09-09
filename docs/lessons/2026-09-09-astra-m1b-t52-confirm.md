# 독립 감수 원문 — T52 좁은 확인 판(gpt-6-astra high · read-only) · 물음 둘만 · `CONFIRM-A: 성립` · `CONFIRM-B: 전제 안`

## 총괄 머리말

이 절은 **총괄 저작**이며, 아래 「게이트 원문」은 무수정 원문 보존이다.

재정 T52 ② C 의 집행이다. 전체 판정이 아니라 **물음 둘만** 물었다 — ⒜ 16차가 보고한 원본 반례가 성립하는가(게이트가 **직접 재현** · 저작자·총괄 스크립트 금지 · 실패를 넣을 자리도 스스로 도출) ⒝ 그것이 **재정 전 전제** 안인가(설계 메모와 `R13-PROOF-OBLIGATIONS.json` 만을 근거로 · 명시가 없으면 「명시 없음」). **번들에서 재정 T52 문서와 브리핑을 일부러 뺐고 SPEC 에도 재정의 방향을 적지 않았다.**

레인 `astra-m1b-t52confirm` · START `2026-09-09 14:44:48` → EXIT 0 · **5분** · 번들 78 파일 · SPEC 5,321 B(위험 어휘 전건 0).

**결과 = 둘 다 확인됐고, 게이트가 총괄·저작자보다 넓게 쟀다.**

- **`CONFIRM-A: 성립`** — 게이트가 독립 하네스로 재현했고 주입 자리(`t40_flow.py:54` `CALL_KW` offset 46)를 **독립 도출**했다. 총괄 재현·저작자 보고와 같은 자리다. **「기존 호출·할당 오류 간선을 발동시킨 시험이지 없던 경로를 만든 것이 아니다」**로 판정했다. 생산 9모듈의 **파일 바이트·모듈 이름 결속·함수 코드 객체·명령열이 실행 전후 동일**함을 스스로 확인했다.
- **★ 범위가 넓어졌다** — 게이트가 **파일 읽기만의 현상이 아님**을 표본으로 보였다. `t40_consume.author_output('envelope-v0', …, preview=True)` 의 `render` 가 오류를 던지는 경로에서도 같은 손실이 났다(무주입은 최종 E1·업무 `Failure/E1`, 주입은 최종 `TransitionError`·업무에 직전 `prepare Success`·실패 목록 E1 없음). 총괄도 저작자도 이 표본을 안 쟀다. **다만 게이트는 전체 진입점으로 일반화하지 않았다.**
- **`CONFIRM-B: 전제 안`** — 문서가 **예외 클래스 목록이 아니라 「실패가 포함되는 연산 단계와 보존 의무」**로 적었고, `R13-PROOF-OBLIGATIONS.json:52–55` 의 `ambient failure preservation` 이 지원 범위를 **`all allocation/store/lookup/call/cleanup operation stages`** 로, 미해결을 **`resource/interrupt failures remain error edges; …`** 로 적으며 `new_exemption: false` 를 둔다. 설계 메모 §5′.14(462행)도 「기존 `PO-GATE-01` 의 증명 의무이며 새 면책으로 제외하지 않는다」로 못박는다. **자원·인터럽트 실패의 포함은 명시돼 있다.**
- **한정(게이트가 스스로 좁힌 것)** — **「모든 명령 경계마다 임의의 자원 실패가 가능하다」는 명시는 없다.** 명시 범위는 **열거된 할당·저장·조회·호출·정리 연산 단계**이며, 이번 `Captured` 생성은 할당·호출에 해당한다고 **해석**했다. 고갈 조건·인터럽트 전달 지점·예외 클래스의 완전 목록은 **명시 없음**이다.

**★ 게이트의 반대 논거를 그대로 받는다 — 이것이 16차 보완 발주의 문안을 바꾼다.**

> 이것은 **이미 확정된 E1 슬롯을 덮어쓴 사례가 아니라, E1 의 최초 확정이 실패하여 직전 성공을 확정한 사례**다. 따라서 근거로 삼을 때에는 「확정 후 불변」만이 아니라 문서의 **「업무 예외를 먼저 고정」** 의무까지 연결해야 한다.

즉 이 반례가 어긴 것은 I-R 의 **「확정 후 불변」** 조항이 아니라 그 앞의 **「업무 호출 반환·예외를 먼저 고정한다」**(§5′.12 I-R · 372행)이다. **재정 T52 ① 의 경계 문언을 설계 메모에 넣을 때 이 연결을 그대로 적는다.**

**처분 = `CONFIRM-A`·`CONFIRM-B` 전건 수용. 재정 T52 ① 의 전제가 확인됐으므로 그대로 집행한다.**

지적 열거 = CONFIRM-A, CONFIRM-B

**[미확인]으로 남은 것** = 실제 자원 고갈에서의 발생 조건·빈도 · 미시험 진입점의 결과 · **여섯 회차 전체의 바이트 동일성**(과거 원본·대조 지문이 번들에 없어 게이트가 독립 확인하지 못했다 — 좁은 번들의 대가이며 총괄이 작업장에서 별도 확인한다).

---

# 게이트 원문 (gpt-6-astra high · 이 아래는 감수자 저작 · 무수정)

CONFIRM-A: 성립  
  근거: 독립 메모리 하네스에서 `E1=OSError`로 다음 두 줄을 관측했다.

  - **무주입:** 최종 오류 `OSError`, **E1과 동일 객체**. `file-read.business=Failure/E1`, 실행 전체 `business=Failure/E1`, 실패 목록에 **E1 있음**. 환경 복원·별도 동일성 대조 성공. 순서: `open → read(E1) → finalize(Failure/E1) → close → seal(Failed) → 환경 복원 → E1 전달`.
  - **주입:** 최종 오류 `TransitionError`, **E1 아님**. `file-read.business=Success`이며 직전 `open` 결과와 동일 객체, **E1 없음**. 실행 전체 `business=Failure/TransitionError`, 실패 목록에도 **E1 없음**. 환경 복원·별도 동일성 대조 성공. 순서: `open → read(E1) → Captured 생성 호출 직전 MemoryError → finalize(open Success) → close → seal에서 TransitionError → 환경 복원 → TransitionError 전달`.

  관측 방법: **기존 호출·할당 오류 간선을 발동시킨 시험이다.** 원본 AST에서 “실패 결과를 생성하여 `result`에 대입하는 호출”을 찾아 [t40_flow.py:54](/home/laptop/projects/workspaces/pd-m1b-t52-confirm/bundle/t40_flow.py:54)의 `CALL_KW`, offset 46을 독립적으로 도출했다. 해당 호출 직전에 사전 생성한 `MemoryError`를 한 번 던졌다. 생성 호출이 실패하면 대입·실패 목록 기록에 도달하지 못하고, 원래의 예외 전파와 [read_closed의 finally](/home/laptop/projects/workspaces/pd-m1b-t52-confirm/bundle/t40_receipts.py:189)가 실행된다. 분기·반환값·지역변수·생산 함수는 치환하지 않았다. 다만 실제 할당기가 고갈된 실행을 관측한 것은 아니다. 생산 9모듈의 실행 전후 **파일 바이트, 모듈 이름 결속, 함수 코드 객체·명령열 모두 동일**했다. 재현 뒤 읽은 저작자 `u5()`도 이 국소 관측에는 건전하며, 호출하지 않았다.

  범위: **파일 읽기만의 현상은 아니다.** `t40_consume.author_output('envelope-v0', …, preview=True)`의 `render`가 E1을 던지는 표본도 확인했다. 무주입은 최종 E1·업무 `Failure/E1`·실패 목록 E1 있음, 주입은 최종 `TransitionError`·업무에 직전 `prepare Success`·실패 목록 E1 없음이었다. 두 경우 모두 환경 복원 성공. 순서는 `prepare → render(E1) → [주입] → finalize → seal → 환경 복원`이며, 파일 쓰기·보고 단계는 실행되지 않았다. 전체 진입점으로 일반화하지 않는다.

CONFIRM-B: 전제 안  
  근거: 문서는 폐쇄된 예외 클래스 목록 대신 **실패가 포함되는 연산 단계와 보존 의무**를 명시한다. [R13-PROOF-OBLIGATIONS.json:52–55](/home/laptop/projects/workspaces/pd-m1b-t52-confirm/bundle/R13-PROOF-OBLIGATIONS.json:52)의 `ambient failure preservation`은 지원 범위를 **“all allocation/store/lookup/call/cleanup operation stages”**, 미해결 내용을 **“resource/interrupt failures remain error edges; no proof yet that original result, cleanup, sealing and return invariants survive every such edge”**로 적고 `new_exemption: false`를 둔다. 따라서 **자원·인터럽트 실패의 포함은 명시되어 있다.** 설계 메모 [§5′.14, 462행](/home/laptop/projects/workspaces/pd-m1b-t52-confirm/bundle/T40-MEASURE-DESIGN.md:462)도 이를 **“기존 PO-GATE-01의 증명 의무이며 새 면책으로 제외하지 않는다”**고 한다. 원결과 의무는 [§5′.12 I-R, 372행](/home/laptop/projects/workspaces/pd-m1b-t52-confirm/bundle/T40-MEASURE-DESIGN.md:372)의 **“업무 호출 반환/예외를 먼저 고정 → 원 객체 identity와 종류는 이후 변경 불가. 진단·cleanup·출처 판정 오류는 별도 슬롯에만 추가한다”**이다.

  한정: 포함 범위는 **열거된 모든 할당·저장·조회·호출·정리 연산 단계의 자원·인터럽트 오류 간선**이다. 특정 IO 단계에만 한정되지 않는다. 이번 `Captured` 생성은 할당·호출에 해당한다고 해석했다. **“모든 명령 경계마다 임의의 자원 실패가 가능하다”는 명시는 없다.** 구체적인 고갈 조건·인터럽트 전달 지점·예외 클래스의 완전 목록도 명시 없음이다.

반대 논거: 이것은 **이미 확정된 E1 슬롯을 덮어쓴 사례가 아니라, E1의 최초 확정이 실패하여 직전 성공을 확정한 사례**다. 따라서 근거로 삼을 때에는 “확정 후 불변”만이 아니라 문서의 “업무 예외를 먼저 고정” 의무까지 연결해야 한다.

[미확인]: 실제 자원 고갈에서의 발생 조건·빈도, 미시험 진입점의 결과. 여섯 회차 전체의 바이트 동일성은 과거 원본·대조 지문이 번들에 없어 독립 확인하지 못했다.