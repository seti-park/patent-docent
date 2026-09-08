# 독립 감수 원문 — M1b 설계 도전 41차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v43(의미 계약·완료 합성 · 자문 6회차 반영 · 재정 T49 문언) · 판정 REVISE(MED 2) · **새 종류의 규칙 요구: 없음(6연속)** · PO 1 → 1 · **T49 ② 신설 지표 첫 계측 `U_r`=6 `B_r`=0 `L_r`=2**

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `8158bd3ba796a87e6892a55e3ececa4e877e442485271fdd19322b38bf82d7ce` · 19769 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v41/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③ · L-052 ⑩) · START 22:45:35 · 종료 23:01 · EXIT 0 · USAGE `input=3,947,670 cached=3,740,160 output=22,658 reasoning=7,437`. 사본 재핀 `2bcf05484aa36582fd6a965b5d9529627f695fda`(신설 `verify/repin-gate.sh` 로 정본 `git -C … rev-parse HEAD` 에서만 취득) · 메모 v43 `bdf1930167fd4032` · PO 정본 `015eaee7a0e3ae5b` · 대장 `0553bcabf6333296` · 회귀표 196 `3986a1ccf650f21e` · 지문표 `2c45df17c7f972d9` · bundle 526. **SPEC 지문 22항은 신설 `verify/check-spec-hashes.sh` 로 번들 실물과 전건 대조**(손으로 옮겨 적던 자리를 기계가 막는다).

**판정 = REVISE · 2건(MED 2 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 13차 · 발주·검수 총괄).** 지문표 157항 중 동봉 124 일치·불일치 0·미동봉 33 · **PO 증거 21/21** · 생산 9모듈이 동결 입력과 바이트 동일(v40→v43 네 회차째) · `derive_inputs()` 재도출 일치 · 정적 `0/0/0 grid 0` · `STRUCTURAL 259/0` · `DOMINANCE 544/24413/24413 차집합 0` · 오라클 `900/900 불일치 0 거부 0 · 음성 대조 516 검출` 재실행 · 경계 거부 122 재현 · 13,440 변이 기록 전행 미검출 0 · 회귀 196 FAIL 0 · 기존 191 metadata·기대·registry 불변 · §5′.10 `22,350 B · 33598684cfd07c2a` 동일 · 심사 ①②③⑤ 성립 · **④ 검증 근거 불성립** · 갈래 ⑴ 2 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」(여섯 회차 연속)** · **PO `Satisfied=11 Violated=1 Unexamined=0`** · 보조 행 단위 `mismatch=2 unmet=3 unreviewed=0` · 미충족 SITE 14·32(+ 54) · A 폐쇄표 **MY~OL closed 151 · partially 3(OH-4·OI-3·OJ-1) · open 0** · **OL-1 과 총괄 M1A 증인은 closed**(S75·S76·S77·S79 및 생산 read/write 증인).

**★ 41차의 핵심 = 총괄이 13차 회수 때 관측한 「검출 기제 6:10」이 그대로 확인됐다.** 40차 반례(`Dict` 병합)는 닫혔지만, 게이트가 **새 구문도 새 연산도 없이** 잘못된 승인 둘을 찾았다 — **기존 호출의 순서만 바꾼 것**이다. 낯선 것 거부(`Unsupported new native protocol completion`)가 발동하는 조건은 **원본에 없던 연산 서명이 생기는 것**이고, 변이 시험은 거의 항상 그 조건을 만든다. 반면 호출 순서만 바꾼 산출물은 연산 재고와 서명 다중집합이 원본과 같아 그 검사에 걸리지 않는다. 게이트의 문장 = 「총괄의 6:10 은 해당 변이들의 정당한 비승인 근거이지만, **승인 건전성이나 부류 폐쇄의 근거로 충분하지 않다**」. 자문 6회차가 「`{**()}` 라는 특정 모양을 금지하는 것이 아니라 공통 의미 규칙을 구현하라」고 한 것과 같은 지점을 다른 방향에서 짚었다.

**OM-1 MED · PO-GATE-01(I-A·I-C·I-S) · SITE-14·32 · 갈래 ⑴ — 효과 순서만 바꾼 산출물 둘을 승인했다.** `t40_receipts.py` 의 `read_closed`(181)·`write_closed`(293)에서 `machine.seal()` 을 `machine.finalize(result)` 직후로 옮기면 — 즉 `cleanup = machine.tail('restore', …)` 보다 **앞**으로 — 실행은 `read` 만 남고 cleanup 없이 `TransitionError` 를 반환한다(원본은 `read, close` · cleanup=E2 · E1 반환). 그런데 정적 결과는 **원본과 완전히 같다**(`0/0/0` · `grid 0` · `STRUCTURAL 259/0` · `DOMINANCE 24413/24413 차 0 · unsupported 0`). 원인 셋 — ⑴ native 연산 84개와 서명 다중집합이 같아 `semantic_delta` 가 차이를 거부하지 않는다 · ⑵ `t40_dominance.py:81` 의 `prerequisites()` 가 `unwrap/finalize/require/require_completion/remember` 를 고르고 **`tail` 을 선행 의무로 선택하지 않는다** · ⑶ 구조 검사는 `finalize` 가 `tail` 보다 앞 행인지만 보고 **cleanup→seal 순서는 강제하지 않는다**. 게이트의 진단 = **「CFG 가 이미 표현한 순서 차이가 승인 질의에서 빠진 것」** · **새 평가기 추가 문제가 아니라 이미 정의된 성질을 승인 질의로 옮기는 구현의 결손**. 고치는 문안 = 「기존 I 의 상태별 효과 순서를 승인 의무로 도출하고, 모든 관련 정상·오류 완료에서 cleanup·봉인·반환의 순서와 결과 보존을 검사한다. 연산 재고의 동일성이나 일부 선행 호출의 지배만으로 승인하지 않는다」.

**OM-2 MED · PO-GATE-01(I-A·I-C·I-S) · T3·P6·P7 · SITE-54 및 승인 공통부 · 갈래 ⑴ — 미해결 증명이 승인 결정에 연결되지 않는다.** `t40_dominance.py:158` 이 재도출되지 않은 관계를 `reopened_by_semantics=True · semantic_status=Unexamined` 로 남기면서도 대상 사건이 있으면 `checked` 에 넣고, `t40_structure.py:484` 의 CLI 종료는 `bool(problems)` 만 본다. 그래서 **원본에서 `pending=1` 인데 `STRUCTURAL 259/0`** 이다. 원본에서 직접 재현된 관계 = `capture` 의 `failure = None` 저장 → `completion:raise`. 게이트의 구분 = **「미해결 사실을 보고하는 것과 미해결 상태의 승인을 거부하는 것은 별개」이며 T49 는 후자를 요구한다** · 다만 **거부만 추가해 원본을 막으면 `B_r` 가 증가하므로 그것만으로는 닫히지 않는다**. 이는 저작자의 `NOT_READY` 인용이 아니라 코드 경로 독립 확인이다(T45 ② 「저작자의 자기 판정은 근거가 아니다」 준수).

**T49 ② 신설 지표의 첫 계측 — 이전 회차 동등 계측값이 없으므로 감소 추세는 주장할 수 없다.** `U_r`=6 은 저작자 JSON 항목 수가 아니라 **게이트가 독립 기준 의미와 기존 불변식에서 도출한 여섯 증명 단위**다(T49 ② 의 「검사기 구현이 아니라 독립 기준에서 도출」 준수) — U1 구체 값·연산의 정상/오류 완료를 추상 transfer 가 보존 · U2 순차·분기·반복·handler·finally·with 의 완료 합성 · U3 실제 호출 결속과 암묵 호출·지연 본체·재개의 효과 합성 · U4 포착·저장·정리 과정 자체의 오류에서도 원결과·보존 상태 유지 · U5 동결 기준 산출물이 기존 I 를 만족한다는 승인 근거 · U6 비교 검사의 성공이 후보의 모든 관련 I 를 보존한다는 근거. 저작자가 보고한 재개방 관계 1개는 **U4 의 증인 하나**일 뿐이다. `B_r`=0 은 제출 원본·기존 명시 코드 양성 4종·current 6·legacy 1·정상 읽기 3·R13 정상 Dict/Set 을 **재실행한 승인 결과 기준**이며 저작자 자기 판정을 비승인으로 세지 않았다. `L_r`=2 는 read·write 두 산출물을 각각 한 건으로 센 값이고 **결함 부류는 하나**다.

**게이트가 총괄의 네 물음에 준 답** — ① **6:10 은 불충분**(10건의 거부는 유효하고 생산 후보에도 적용되는 코드지만, 원본의 기존 서명에는 발동하지 않고 재고를 유지한 순서 변경도 통과한다). ② 평가기 22·다섯 항목 차집합 0 은 **소유자·오류 경로·계약 필드의 연결 완결성이지 실제 의미와의 일치가 아니다** — CPython 대조에서 표본 밖 불일치를 찾았다: `t40_sink(**{"x": 1, "x": 2})` 는 CPython 이 정상 완료해 `effects=['tail']` 을 남기는데 모델은 `DICT_MERGE.protocol_safe=False` 로 정상 후속을 제거했다(원인 = `t40_operations.py:259` 의 추상 병합이 **사전 구성에서 덮어쓴 키까지 쌍 목록에 보존**한 뒤 호출 키워드 중복으로 셈). 안전한 변경의 비승인이라 별도 위반·`B_r` 로 세지 않았으나 **계약 필드 완성·오류 간선 존재가 의미 정확성의 증명이 아님을 보이는 관측**이다. ③ **실행 관측은 독립적**(표준 라이브러리만 import · 검사기 등록표·값 추상화·기대값을 읽지 않음)이나 유한 구문 생성기와 표시된 효과만 관측하는 한계가 있고 관측 단어는 주로 `t40_mark` 이며 예외는 정적으로 `AnyBaseException` 으로 합쳐진다. ④ **`B_r`=0**.

**T44 판정** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ 2건 전부 ✓ · 새 규칙 요구 없음 ✓ → **자동 기동 조건 성립**. **비감소 상신 조건은 T48 ③·T49 로 이미 처분됐으므로(자문 수령·재정 완료) 재상신하지 않고 14차 저작으로 간다.** ⑽ ⓑ 자문 트리거는 판정문에 발동 명기됐다(컴포넌트 D · PO-GATE-01 승인 근거 부류 6회 연속) — **직전 자문이 이 부류를 정확히 겨눠 6회차로 회신됐고 재정 T49 가 그 처분이므로 새 자문을 다시 청하지 않는다.** 트리거의 뜻은 「같은 부류가 굳었다」이고, 그 대응은 이미 진행 중이다.

**총괄 관측 — 지표의 층이 하나 바뀌었다.** 38·39·40차 세 지적은 「지원한다고 등록해 놓고 그 구성의 **실패 의미**를 구현하지 않았다」는 한 형태였고, 매 회차 검사기가 한 단계씩 일반화했다(자리 열거 → 규칙 → 등록 기본값 뒤집기 → 의미 계약·완료 합성). 41차 지적 둘은 **그 축에서 벗어난다** — OM-1 은 새 구문·새 연산이 없고, OM-2 는 의미 모델이 아니라 **판정 결과를 종료 코드로 옮기는 배선**이다. 즉 남은 구멍은 「어떤 문법을 아직 모르는가」가 아니라 **「이미 아는 것을 승인 질의에 넣었는가」**다. PO Violated 가 네 회차 1 로 평평한 것은 지표의 포화이며, T49 ② 가 신설한 셋이 그 아래에서 실제로 무엇이 남았는지를 처음 보여 줬다(`U_r`=6). 게이트도 같은 말을 했다 — **「평평한 PO 수는 남은 구멍의 수나 수렴을 나타내지 않는다」**.

**처분 = 수용(공학) · 이행 = 14차 저작(astra xhigh · 좌석 M3).**

지적 열거 = OM-1, OM-2

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 41회 · PO-GATE-01 승인 근거 부류 6회 연속)
새 종류의 규칙 요구: 없음
`U_r`=6 `B_r`=0 `L_r`=2

**`Satisfied=11 Violated=1 Unexamined=0`.** 새 지적은 모두 갈래 ⑴이며, 상류 도출 누락·새 보증 요구·ⓑ 대장 누락 반례는 각각 0이다.

**기존 호출의 순서만 바꿔 cleanup을 생략시키는 산출물 두 개를 검사기가 승인했다.** 새 구문·새 연산이 없어도 발생한다. 따라서 총괄의 **6:10은 해당 변이들의 정당한 비승인 근거이지만, 승인 건전성이나 부류 폐쇄의 근거로 충분하지 않다.**

보조 행 지표는 **`mismatch=2 unmet=3 unreviewed=0`**이다. 직접 반례가 있는 검증 배선 SITE-14·32를 mismatch로, 여기에 미해결 증명의 승인 처리가 남은 SITE-54를 더해 unmet으로 셌다. 검사기의 재고 출력 `0/0/0`과 구별한다.

**고정 범위 확인**

격리 마커의 path·pin·order/disposable 및 HEAD `2bcf05484aa36582fd6a965b5d9529627f695fda`가 일치했다. 메모 `bdf1930167fd4032`, 지문표 `2c45df17c7f972d9`, 대장 `0553bcabf6333296`, PO `015eaee7a0e3ae5b`도 일치한다.

지문표 **157항 중 동봉 124항 일치·불일치 0·미동봉 33항**이다. PO 현재 증거 해시는 **21/21 일치**했다. 생산 9모듈은 동결 입력과 바이트 동일하고, JSON 표현을 정규화한 `derive_inputs()` 재도출도 동결 입력과 일치했다.

`bundle/ADVICE-REPLY-6.md`는 없어서 [보존된 자문 전문](/home/laptop/projects/workspaces/pd-m1b-t40/docs/lessons/2026-09-08-astra-advice-t40-po-gate-01.md)을 읽었다. PO 구 문언과 T49의 차이는 지적으로 세지 않았다.

**지적**

**OM-1 · MED — PO-GATE-01 / 연결 I-A·I-C·I-S의 승인 건전성, 실행 증인에서 원결과·cleanup·봉인 순서 의무 훼손 / P2·T3(SITE-14), P4·T2(SITE-32) / 갈래 ⑴ / 최소 trace: 업무 E1 → finalize(E1) → seal → tail 거부 → close 생략 → TransitionError 반환 / 관측: 두 산출물 모두 대장·격자·구조·지배 위반 0 / 고치는 문안: “기존 I의 상태별 효과 순서를 승인 의무로 도출하고, 모든 관련 정상·오류 완료에서 cleanup·봉인·반환의 순서와 결과 보존을 검사한다. 연산 재고의 동일성이나 일부 선행 호출의 지배만으로 승인하지 않는다.”**

[read_closed](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:181)의 다음 부분을 메모리에서만 바꿨다.

```python
# 원본
machine.finalize(result)
if handle is not None:
    cleanup = machine.tail('restore', lambda: handle.close())
machine.seal()

# 변이
machine.finalize(result)
machine.seal()
if handle is not None:
    cleanup = machine.tail('restore', lambda: handle.close())
```

[write_closed](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:293)에서도 기존 `machine.seal()` 하나를 `machine.finalize(result)` 직후로 옮겼다. 나머지 본문은 보존했다.

| 독립 실행 | 원본 | 승인된 변이 |
|---|---|---|
| read E1·close E2 | `read, close`; business=E1; cleanup=E2; E1 반환 | **`read`만**; business=E1; cleanup 없음; **TransitionError 반환** |
| write E1 | `enter, write, close`; business=E1; E1 반환 | **`enter, write`만**; business=E1; cleanup 없음; **TransitionError 반환** |

두 변이 모두 환경 복원은 성공했고, 변경을 되돌린 대조는 원본 관측으로 복귀했다. 동봉 증인 함수와 별도로 작성한 메모리 하네스에서도 실제 생산 `Machine`·`F.execute`·입출력 wrapper를 사용해 재현했다.

각 변이의 정적 결과는 동일했다.

```text
sites: mismatch=0 unmet=0 unreviewed=0 extracted=3772
grid=0
STRUCTURAL checks=259 violations=0
DOMINANCE scopes=544 required=24413 checked=24413
difference=0 extra=0 unsupported=0
TRAVERSAL 48480/48480 difference=0
```

핵심은 **CFG가 이미 표현한 순서 차이가 승인 질의에서 빠진 것**이다.

- read 원본과 변이의 native 연산은 각각 84개이고 서명 다중집합도 같다. 따라서 `semantic_delta`는 차이를 거부하지 않는다.
- `handle is not None ∧ result is not None`에서 tail을 차단하면, seal 도달은 **원본 False → 변이 True**다.
- 그러나 [prerequisites()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_dominance.py:81)는 `unwrap/finalize/require/require_completion/remember` 등을 고르고 **tail을 이 선행 의무로 선택하지 않는다**.
- 구조 검사는 finalize가 tail보다 앞 행인지 확인하지만, 이 사례의 cleanup→seal 순서는 강제하지 않는다.

새 평가기를 추가하는 문제에 한정되지 않는다. **이미 정의된 성질을 승인 질의로 옮기는 구현의 결손**이다.

**OM-2 · MED — PO-GATE-01 / I-A·I-C·I-S의 미해결 증명 비승인 의무 / T3·P6·P7 / 갈래 ⑴ / SITE-54 및 승인 공통부 / 최소 trace: 재증명 미해결 관계 보유 → checked에 포함 → violations 없음 → 정적 성공 반환 / 관측: 원본에서 pending=1인데 STRUCTURAL 259/0 / 고치는 문안: “미해결 증명은 승인 결정에 직접 연결한다. 원본·필수 양성의 기존 의무를 충족하는 산출물 결속 증거를 제공한 뒤 승인하며, checked·해시 동일성·자기 비교를 증명 충족으로 대체하지 않는다.”**

이는 저작자의 `NOT_READY`를 인용한 판정이 아니다. 코드 경로를 독립 확인했다.

[역사 의무 처리](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_dominance.py:158)는 재도출되지 않은 관계를 `reopened_by_semantics=True`, `semantic_status=Unexamined`로 남기면서, 대상 사건이 있으면 `checked`에 넣는다. 이것이 승인 위반으로 연결되지 않고, [CLI 종료](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:484)는 `bool(problems)`만 사용한다.

원본에서 직접 재현된 관계는 `capture`의 `failure = None` 저장→`completion:raise`다. **미해결 사실을 보고하는 것과 미해결 상태의 승인을 거부하는 것은 별개**이며, T49는 후자를 요구한다. 거부만 추가해 원본을 막으면 `B_r`가 증가하므로 그것만으로도 폐쇄되지 않는다.

**이번 판의 네 물음**

| 물음 | 독립 판단 |
|---|---|
| ① 6:10은 충분한가 | **불충분.** 10건의 거부는 유효하지만 기준선과 다른 연산 서명에 대한 거부다. 생산 후보에도 적용되는 코드이므로 “시험에서만 켜지는 장치”는 아니다. 다만 원본의 기존 서명에는 발동하지 않으며, OM-1처럼 재고를 유지한 순서 변경도 통과한다. |
| ② 평가기 22·다섯 항목 차집합 0은 무엇인가 | 소유자·오류 경로·계약 필드의 연결 완결성이다. 실제 의미와의 일치는 별도다. 아래 CPython 대조에서 표본 밖 불일치를 확인했다. |
| ③ 오라클은 독립적인가 | 실행 관측 모듈은 표준 라이브러리만 import하며 검사기 등록표·값 추상화·기대값을 읽지 않는다. **실행 관측은 독립적**이다. 다만 유한 구문 생성기와 표시된 효과만 관측하는 한계가 있다. |
| ④ `B_r=0`인가 | 확인한 원본·필수 코드 양성은 승인됐고, 기존 양성 실행·동봉 전체 회귀에서도 비승인을 발견하지 못했다. 아래 재실행과 동봉 증거를 구분해 **0**으로 판정한다. |

다섯 항목 중 **Dict 구성→호출 키워드 병합의 정상 완료 계약**을 CPython과 대조했다.

```python
t40_sink(**{"x": 1, "x": 2})
t40_mark("tail", None)
```

CPython은 정상 완료하고 `effects=['tail']`을 남겼다. 반면 모델은 `DICT_MERGE.protocol_safe=False`로 정상 후속을 제거하여 **그 효과 단어와 정상 완료를 포함하지 못했다**.

원인은 [추상 병합](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_operations.py:259)이 사전 구성에서 덮어쓴 키까지 쌍 목록에 보존한 뒤, 이를 호출 키워드 중복으로 세는 데 있다. 이 사례는 필수 양성 목록의 항목이 아니며, 안전한 변경의 비승인 자체를 별도 위반이나 `B_r`에 더하지 않았다. **계약 필드 완성·오류 간선 존재가 의미 정확성의 증명이 아님을 보여 주는 관측**이다.

동시에 다음 개선도 직접 확인했다.

| 식 | CPython 효과·완료 | 모델 포함 |
|---|---|---|
| `{**(), 0: mark(...)}` | payload 전 TypeError | True |
| `{[]: mark(...)}` | payload 뒤 TypeError | True |
| `{**{}, 0: mark(...)}` | payload·tail 정상 완료 | True |

오라클 **900건·불일치 0·거부 0·오류 삭제 음성 대조 516건 검출**을 재실행했고 결과 JSON은 동봉본과 완전히 같았다. 도메인은 20개 구문×11개 값, 선택 필드 투영, 배치 경계·명시 합성 사례로 만든 표현식 300개×문맥 3개다. 정적 분석 구간의 `eval/exec` 차단도 재현됐다.

그러나 관측 단어는 주로 `t40_mark` 호출이며, 예외는 정적으로 `AnyBaseException`으로 합쳐진다. 호출 객체의 실제 결속·암묵 효과·상태 슬롯 identity·모든 지연 재개를 검증하는 오라클은 아니다. OM-1의 생산 상태 전이는 별도 검증이 필요하다.

**`U_r·B_r·L_r` 도출**

`U_r`는 저작자의 JSON 항목 수를 옮기지 않았다. **구체 실행을 기존 I에 대한 승인으로 연결하는 데 필요한 다음 여섯 증명 단위**로 셌다. 숨은 결함의 총수를 뜻하지 않는다.

| 단위 | 독립적으로 요구되는 근거 | 미해결 판단 |
|---|---|---|
| U1 | 구체 값·연산의 정상/오류 완료를 추상 transfer가 보존 | 위 사전 덮어쓰기 사례에서 실제 정상 경로 누락 |
| U2 | 순차·분기·반복·handler·finally·with의 완료 합성 | 계약 문구·일부 효과 단어 대조 외에 전체 지원 조합의 합성 근거 없음 |
| U3 | 실제 호출 결속 및 암묵 호출·지연 본체·재개의 효과 합성 | 지역 반환 형태·별도 CFG 재고가 호출 시점의 효과·결과 합성을 대신하지 못함 |
| U4 | 포착·저장·정리 과정 자체의 오류에서도 원결과·보존 상태 유지 | SITE-54의 저장 전 오류 완료 관계가 독립 재실행에서도 미해결 |
| U5 | 동결 기준 산출물이 기존 I를 만족한다는 승인 근거 | 동일 분석기로 기준선과 자신을 비교하는 성공 외에 결부된 증명 검증 경로 부족 |
| U6 | 비교 검사의 성공이 후보의 모든 관련 I를 보존한다는 근거 | OM-1: 모델에 표현된 cleanup→seal 차이가 승인 질의에서 누락 |

따라서 **`U_r=6`**이다. 저작자가 보고한 재개방 관계 **1개는 U4의 증인 하나**이며, 전체 미해결 승인 근거 수가 아니다.

**`B_r=0`**의 근거는 다음과 같다.

- 제출 원본: 구조·대장·격자·지배 승인.
- 기존 명시 코드 양성 4개: IO `False or`, close의 살아 있는 조건문, stopped의 `False or`, finalize의 살아 있는 조건문을 전체 정적 경계에서 재실행하여 모두 0.
- R13의 정상 Dict·Set을 read/write 각각 재실행하여 승인 및 원본 실행 관측 유지.
- current 양성 6·legacy 양성 1·정상 읽기 3 재실행 성공.
- 기존 **191개 metadata·기대·registry 불변**, 전체 196개 동봉 결과 FAIL 0 및 R1/R2 동치 증거의 해시 확인.

이는 **검사기의 실제 승인 결과 기준**이다. 저작자의 납품 자기 판정 `NOT_READY`를 원본 비승인 한 건으로 더하지 않았다.

**`L_r=2`**는 서로 다른 산출물인 read 순서 변이와 write 순서 변이를 각각 한 건으로 센 값이다. 같은 변이의 재실행·복구 대조를 중복 계상하지 않았다. **결함 부류는 하나다.**

PO Violated는 **38차 1 → 39차 1 → 40차 1 → 41차 1**이다. 그런데 이번에는 지정 반례 폐쇄와 함께 **새 잘못된 승인 2건**이 확인됐다. 평평한 PO 수는 남은 구멍의 수나 수렴을 나타내지 않는다. `U_r·B_r·L_r`의 이전 회차 동등 계측값은 없으므로 감소 추세를 주장할 수도 없다.

**PO 12 심사**

다른 11개 PO는 고정 생산 원본의 기제·기존 증거·아래 반례 시도로 심사했다. 승인된 메모리 변이의 결함은 검사기 의무에 계상했으며, 생산 원본의 실행 결함으로 중복 계상하지 않았다.

| PO / I | 상태 | 최소 반례 시도와 근거 |
|---|---|---|
| PO-EXEC-01 / I-A | Satisfied | 미지 profile·인자 실패 뒤 업무 진입 시도. Admit 선행과 지연 경계가 실행을 차단함. |
| PO-RESULT-01 / I-R | Satisfied | 원본 read E1→close E2, 업무 결과→observer 실패. 원 객체와 부수 오류가 분리 보존됨. |
| PO-FAIL-01 / I-F | Satisfied | 첫째·둘째 효과 실패 후 다음 단계 시도. stopped·단계 guard에서 후속 효과 0. |
| PO-STATE-01 / I-A | Satisfied | Skip/NA의 Success 대체, 미완료 seal, 봉인 뒤 tail 시도. 전이 거부·효과 0. |
| PO-IO-01 / I-C | Satisfied | 원본/sandbox IO 후 parsing 시도. 각각 io-fault/infeasible, 동일 증표 없는 parsing 거부. |
| PO-PROFILE-01 / I-C | Satisfied | 결측·잘못된 타입·미지 판본·Admit 대체 16건 거부. current 6·legacy 1 양성 유지. |
| PO-PRESERVE-01 / I-P | Satisfied | 보존 단계·close 실패 후 공개/소비 시도. 생산 상태기계·Complete 검사와 기존 FI가 미완료 소비를 차단함. |
| PO-ENV-01 / I-E | Satisfied | 복원 실패 및 성공/실패 환경 왕복. 원결과 보존, 다른 복원 항목 계속 시도, 실패 명시. |
| PO-RESOURCE-01 / I-X | Satisfied | 자료/sandbox 역할 중첩과 출처 없는 오류. sandbox 환경 역할 우선, 미상은 판정 불가. |
| PO-ISOLATE-01 / I-X | Satisfied | 원본과 같은/내부 sandbox 제출. 삭제·생성 전에 거부. 보호 집합·출력 경계 배선 확인. |
| PO-SEMANTIC-01 / I-S | Satisfied | validation 실패의 정상 승격 차단. 기존 기대·registry·생산 바이트 및 동봉 legacy/current/API/R1/R2 동치 유지. |
| PO-GATE-01 / I-A·I-C·I-S | **Violated** | **OM-1·OM-2.** 효과 순서 위반 산출물 승인 및 미해결 증명 비승인 의무 미집행. |

**남은 목록:** PO-GATE-01; SITE-14·32의 승인 검증 배선, SITE-54의 미해결 관계 처리; U1~U6. PO 단위 Unexamined는 없다.

**심사 대상 다섯**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 성립 | 새 반례는 기존 I·PO로 환원됨. 상류에 없는 규칙 불필요. |
| ② 신뢰·입력·부작용 경계 | 성립 | T1~T4·registry·68행/56칸 확인. R1/R2 변경은 지정 좌석 계약 값뿐. |
| ③ 기제의 집행과 합성 | 성립 | 고정 생산 원본의 경계·결과 보존·fail-stop·소비·복원 기제와 관측 부합. |
| ④ 검증 근거 | **불성립** | 승인된 두 산출물이 기존 효과 순서 의무를 깨뜨림. 미해결 근거도 승인 결정과 분리됨. |
| ⑤ 미충족·불명확 처분 | 성립 | 다섯 처분·사람 복구 절차·정상 수용 유지. 정적 증명 비승인 결손은 ④/PO-GATE에 계상. |

**A 폐쇄표**

`closed`는 기존 지정 반례의 폐쇄이며 전체 승인기의 건전성을 뜻하지 않는다.

| 지적 | 판정 | 구조·회귀·FI 연결 |
|---|---|---|
| MY~OG 143건 | closed 유지 | 기존 처분·기대·생산 바이트 연속성 유지 |
| OH-1~3 | closed | 닫힌 파일 효과·IO-clear·profile 기제; 재조립 실패 후 후속 copy 0, 진단 실패 뒤 normalization 0, 미지 profile 읽기 0 재현 |
| OI-1·2 | closed | S63/S64; 완료 결측·Admit 대체 공개 0, 읽기/close 실패의 원결과·cleanup 보존 |
| OH-4 | **partially** | 기존 변이 폐쇄 유지; 전체 승인 근거에 OM-1·2 잔여 |
| OI-3 | **partially** | 기존 IO·close 변이 폐쇄 유지; 새 효과 순서 변이 승인 |
| OJ-1 | **partially** | 지정 두 trace의 S66/S67/S68 폐쇄 유지; 선행 의무 도출의 충분성에 OM-1 잔여 |
| OK-1·2 | closed 유지 | 비교 단락·전체 선언 입장 검사, S70~S74 및 동봉 FI 연속성 |
| OL-1 | **closed** | native Dict 병합 오류 완료; **S75·S77·S79** 및 생산 read/write 증인. 독립 재실행 구조 위반 **6·7**, 정상 Dict 짝 **0·0** |
| 총괄 M1A 증인 | closed | Set 구성 실패; **S76** 및 생산 read/write 증인에서 구조 위반 **5·6**, 정상 Set 짝 유지 |

MY~OL 합계 **closed 151·partially 3·open 0**. 40차 미충족 SITE-14·32는 지정 OL-1이 닫혔지만, **OM-1의 새 승인 반례로 검증 근거가 계속 미충족**이다.

**검증 경로**

`<PY>`는 사본 cwd에서 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B`이다. Python 작업은 `<PY> -c` 메모리 하네스로 실행했다. 산출 저장은 메모리에서 받았고, 실제 파일 쓰기는 audit hook으로 차단했다.

| 명령·호출 | 마지막 출력·확인 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 지정 마커·HEAD 일치 |
| 지문표 전항 SHA 대조 | `total 157 matched 124 missing 33 mismatch []` |
| PO `evidence_hashes` 대조 | 21항·불일치 0 |
| `S.compare`·`S.grid_compare`·`ST.check` | 원본 및 OM-1 두 변이 모두 `0/0/0`, grid 0, `259/0` |
| OM-1 독립 생산 메모리 하네스 | 두 변이 close 생략·TransitionError; 복구 대조 원본과 동일 |
| `O.run()`·`R.contract_boundaries()` | `900/900 refused=0 mismatches=0 erased=516`; 경계 거부 122 |
| `W.run('after')` | `read=6 write=5 reproduced=2 … FAIL=0` |
| 독립 Dict 계약 대조 | 덮어쓰기 사례 `runtime return ['tail']`, `included=False` |
| 기존 코드 양성 4종 | 각 `structural/mismatch/unmet/unreviewed/grid=0` |
| 메모리 불변식·R10 profile/read·R12 의미 | 불변식 17 FAIL 0; 음성 16·양성 7; read 실패 9·정상 3; 의미 36 FAIL 0 |
| `M.profiles()`·`M12.points()` | 20부류·후보 329·표현식 자리 672·곱 13,440; 동봉 부류 동일 |
| 동봉 변이 JSON 전행 대조 | 13,440행·미검출 0 |
| `H.CASES()`·동결 metadata | 기존 191 변경 0·전체 196·registry 동일 |
| 생산 소스·`derive_inputs()` | 9/9 바이트 동일·정규화 후 입력 동일 |
| 계측 세 커밋 diff | R1 decompose/synthesize effort만; R2 ground-dependent model/effort만 |
| §5′.10 바이트 대조 | **22,350 B·33598684cfd07c2a**, v42와 동일 |
| 동봉 Python `compile(..., 'exec')` | 124파일·파일 생성 없음 |
| 최종 상태·캐시·핵심 지문 | 추적 변경 0·캐시 0·지정 지문 유지 |

**[미검증]**

읽기 전용 조건에 따라 **회귀 196·FI 76의 전체 디스크 실행, 실제 R1/R2 동치 재실행, 전체 불변성 스크립트·디스크 `py_compile`은 실행하지 않았다.** 해당 부분은 동봉 원자료·로그·해시와 코드로 심사했다. 메모리 시험은 물리 디스크 내구성 검증이 아니다.

13,440 변이는 도메인을 재산출하고 기록 전행을 확인했지만, 전건 CFG 실행을 반복하지 않았다. 총괄 16종 전체의 6:10도 전건 재계측한 수로 보고하지 않는다. 미동봉 33개 보조 스크립트의 내용은 추정하지 않았다.

실측·원격 Workflow·Owner 발췌 판독은 수행하지 않았다. 정본 리포의 생산 자료를 읽거나 쓰지 않았고, 지정 인터프리터만 사용했다.

**④와 PO-GATE-01이 불성립하므로 고정 PASS 문장은 충족되지 않는다. 실측 착수 금지를 유지한다.**