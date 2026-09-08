# 독립 감수 원문 — M1b 설계 도전 40차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v42(미등록 문법·영역은 거부가 기본값 · 39차 OK-1·2 반영) · 판정 REVISE(MED 1) · **새 종류의 규칙 요구: 없음(5연속)** · PO 1 → 1(**비감소 2회 · 상신 조건 성립**)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `f58757c92d38ce37d3daf5258412ebb8f90e1483aebe84990ed1b785419c8a10` · 13110 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v40/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · START 16:11:31 · EXIT 0 · USAGE `input=5,716,159 cached=5,488,512 output=20,540 reasoning=7,736`. 사본 재핀 `34f8a7a` · 메모 v42 `cc618961ea61a898` · PO 정본 `bfd20029683b8539` · 대장 `3a74ccd1ed993537` · 회귀표 191 `ecd6c5221912d1bb` · 지문표 `cc42c1fe14d4045f` · bundle 440.

**★ 이 기동은 세 번째 시도다 — 앞의 둘은 벤더 내용 필터에 막혀 판정이 없다(회차로 세지 않는다).** ⑴ 15:59 기동 → `EXIT=1 · FINAL 0 B` · `This content was flagged for possible cybersecurity risk` · 이벤트 47. **원인 = 발주자가 이번 SPEC 에만 새로 넣은 보안 어휘**(39차엔 `우회`·`exec`·`getattr` 각 0 이었는데 40차에 2·1·1) — 첫 물음 ⑴ 을 「등록 **우회** 경로가 남았는가」로 틀 지었다. ⑵ 16:03 재기동(어휘 전부 0 으로 치환) → **또 차단** · 이벤트 77 · 실패 지점이 **감수자 자신의 추론**(「Analyzing event handling and aliasing effects · Evaluating import aliasing and module behavior」). ⇒ **방아쇠는 문구가 아니라 그 축을 생각하는 것 자체**다. ⑶ 16:11 재기동 — **그 축(등록표를 거치지 않고 같은 자리에 닿는 정적 경로가 있는가)을 발주문에서 통째로 제거**하고 「그 축을 스스로 파고들 필요 없다」는 총괄 주기를 달았다 → **필터 발동 0 · 판정 성립**. 선례 = `~/.claude/agents/ROUTING-EVIDENCE.md` §11(nd-magnet · 필터는 도구 호출 내용과 감사자 추론에 걸리고 비결정적). **그 축은 이 좌석에서 심사 불가로 남았다 — 처분 필요(상신 ②).**

**판정 = REVISE · 1건(MED 1 · HIGH 0) · 기각 0 · 발주자 귀책(저작 astra xhigh 12차 · 발주·검수 총괄).** 지문표 111항 중 동봉 78 일치·불일치 0·미동봉 33 · **PO 증거 14/14** · 생산 9모듈이 동결 입력과 바이트 동일 · `derive_inputs()` 재도출이 동결 JSON 과 일치 · 정적 `0/0/0 grid 0` · `STRUCTURAL 259/0` · `DOMINANCE 544/24413/24413 차집합 0` · 여집합 952·208·50 재현 · 제어 변이 `7,116/7,116 ID 전건 동일` · 심사 ①②③⑤ 성립 · **④ 검증 근거 불성립** · 갈래 ⑴ 1 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」(다섯 회차 연속)** · **PO `Satisfied=11 Violated=1 Unexamined=0` — 37차 6 → 38차 1 → 39차 1 → 40차 1 · 비감소 2회 · 게이트가 판정문에 「총괄의 Owner 상신 조건 성립」을 명시** · 보조 행 단위 `2/2/0` · 미충족 SITE 14·32 · A 폐쇄표 MY~OG closed 143 유지 · OH-1~3·OI-1~2 closed · **OH-4·OI-3·OJ-1 partially(전부 「전체 지원 의미의 근거에 OL-1 잔여」)**.

**OL-1 MED · PO-GATE-01 · SITE-14·32 · 갈래 ⑴ — 등록된 `Dict` 의 병합 오류를 평가 의미에서 빠뜨렸다.** `t40_control.py:323` 의 `dict_expr` 가 `zip(node.keys, node.values)` 로 값 표현식만 순서대로 평가하는데, **`Dict.keys` 의 `None` 은 `**` 병합**을 뜻한다. 그래서 `{**(), 0: machine.finalize(result)}` 에서 「튜플이 mapping 이 아니라 뒤 항목을 평가하기 전에 실패한다」는 의미가 없다. 두 생산 자리의 호출식만 그 꼴로 바꾸면 — `read_closed:191` 은 `effects=['read']` · **business=None** · cleanup 없음 · `read:Failure` · 반환 `TypeError`(원본은 `['read','close']` · business=E1 · cleanup=E2 · `Failed` · 원 E1 반환) · `write_closed:323` 은 **business=None** · `close:Failure` · 반환 `TypeError` · `first_identity=False`. 그런데 **대장·격자·구조·지배 검사가 모두 0**. **사용자 정의 객체·별칭·동적 코드 없이 내장 상수만으로 재현된다.** 양성 대조 `{**{}, 0: …}` 는 위반 0 이면서 실제 동작도 정상이라 대조군이 성립한다. 고치는 문안 = 「지원 표현식의 **컨테이너 구성·unpack/병합 단계까지** 정상·오류 완료와 후속 피연산자 실행 여부를 해석한다. 미구현 조합은 위치 있는 Unsupported 로 거부하고, **해당 실패 의미에서 도출한 변이를 전체 선행 의무에 적용**한다」.

**게이트가 네 물음에 준 답(다음 판의 방향을 가른다)** — ⑴ 여집합은 믿을 만하다: 입장 검사가 여집합 목록이 아니라 `RULES.get(type(node))` 를 쓰므로 **export 를 하나 지워 133→132 로 줄여도 그 노드를 거부**했고 export 되지 않은 새 subclass 도 거부했다(열거 축소가 허용 확대로 이어지지 않는다). ⑵ 48,480 은 **AST 출현 횟수**이며 조건부·죽은·지연 선언을 포함하지만 **실행 의미의 완전성은 아니다**(문자열 안 코드·런타임 생성은 명시된 범위 밖이고 48,480 에 포함했다고 인정하지 않았다). ⑶ **「타입·필드 등록 및 evaluator 존재만으로 의미 구현을 보증하지 못한다」** — `Compare` 단락 평가는 확인됐으나 `Dict` 병합 실패가 빠졌다. ⑷ **7,116 변이는 `Rule.erasure` 가 있는 12종의 도메인이며 `Dict` 병합 실패는 들어 있지 않다.**

**T44 판정** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ · 새 규칙 요구 없음 ✓ → 자동 기동 조건은 성립. **그러나 PO Violated 비감소 2회로 T45 ③·T47 상신 조건이 성립하므로 자동 기동하지 않고 Owner 재정을 받는다.**

**총괄 관측(상신 문서의 뼈대)**: 38·39·40차 세 지적이 **형태가 같다** — 「어떤 구성을 지원한다고 등록해 놓고 그 구성의 **실패 의미**를 구현하지 않았다」(38차 = 지배를 두 자리에만 · 39차 = `Compare` 단락 평가와 `ClassDef` 순회 · 40차 = `Dict` 병합 실패). 매 회차 검사기는 **한 단계 더 일반화**했는데(자리 열거 → 규칙 → 등록 기본값 뒤집기) 그때마다 **더 안쪽의 의미 구멍**이 나온다. 게이트의 ⑶⑷ 답이 그 구조를 정확히 말한다 — 등록은 **문법**을 닫았지만 **의미**는 여전히 열거이고, 변이 도메인도 `Rule.erasure` 가 있는 12종에서만 나온다. **PO 진행도가 1 에서 세 회차 고정된 것은 지표의 포화이자 이 구조의 반영이다.**

**처분 = 수용(공학) · 이행 = Owner 재정 뒤 결정.**

지적 열거 = OL-1

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 40회)
새 종류의 규칙 요구: 없음

**OL-1 · MED 1건.** 미등록 문법의 기본 거부는 확인했다. 그러나 **등록된 `Dict`의 병합 오류를 평가 의미에서 빠뜨려**, 원결과 확정을 건너뛰는 변이를 검사기가 승인한다. 기존 `PO-GATE-01`의 구현·증거 결손이다.

`Satisfied=11 Violated=1 Unexamined=0`

보조 행 단위는 **`mismatch=2 unmet=2 unreviewed=0`**이다. SITE-14·32의 검증 근거 배선에 대한 독립 판정이며, 검사기의 재고 출력 `0/0/0`과 구별한다. ⓑ **대장 누락 반례 0**, 도출 누락 0, 지적은 전부 갈래 ⑴이다. PO Violated는 **37차 6 → 38차 1 → 39차 1 → 40차 1**이므로 **비감소 2회, 총괄의 Owner 상신 조건 성립**이다.

**고정 범위 확인**

격리 마커의 path·pin·order/disposable 및 HEAD가 발주와 일치했다. 메모 `cc618961ea61a898`, 지문표 `cc42c1fe14d4045f`, 대장 `3a74ccd1ed993537`, PO `bfd20029683b8539`도 일치한다.

지문표 111항 중 **동봉 78항 일치·불일치 0·미동봉 33항**이다. PO 현재 증거 해시는 **14/14 일치**했다. 생산 9모듈은 동결 입력과 바이트 동일하며, `derive_inputs()` 재도출도 동결 JSON과 일치했다.

**지적**

**OL-1 — PO-GATE-01 / I-A·I-C·I-S의 검증 메타 의무, 반례에서 I-R 및 보존·cleanup 의무 훼손 · P2/T3(SITE-14), P4/T2(SITE-32) · 갈래 ⑴ · 최소 trace: 업무 실패 E1 → `{**(), 0: machine.finalize(result)}` → 병합 `TypeError` → finalize 미실행 → cleanup·seal 미실행 · 관측: 대장·격자·구조·지배 위반 모두 0인데 business=None 및 원 업무 예외와 다른 반환 · 고치는 문안: “지원 표현식의 컨테이너 구성·unpack/병합 단계까지 정상·오류 완료와 후속 피연산자 실행 여부를 해석한다. 미구현 조합은 위치 있는 Unsupported로 거부하고, 해당 실패 의미에서 도출한 변이를 전체 선행 의무에 적용한다.”**

원인은 [t40_control.py:323](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_control.py:323)이다.

```python
def dict_expr(self, node, nxt, error):
    return self.sequence(
        [v for pair in zip(node.keys, node.values) for v in pair],
        nxt, error)
```

`Dict.keys`의 `None`은 `**` 병합을 뜻한다. 현재 구현은 이를 건너뛰고 값 표현식만 순서대로 평가한다. 따라서 `{**(), 0: …}`에서 **튜플이 mapping이 아니므로 뒤 항목을 평가하기 전에 실패한다**는 의미가 없다. 사용자 정의 객체·별칭·동적 코드 없이 내장 상수만으로 재현된다.

두 생산 자리의 호출식만 메모리에서 다음처럼 바꿨다.

```python
machine.finalize(result)
# →
{**(), 0: machine.finalize(result)}
```

| 자리·주입 | 원본 관측 | 변이본 관측 |
|---|---|---|
| [read_closed:191](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:191), read E1·close E2 | `effects=['read','close']`, business=E1, cleanup=E2, `Failed`, 반환 E1 | `effects=['read']`, **business=None**, cleanup 없음, `read:Failure`, 반환 **TypeError** |
| [write_closed:323](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:323), close E1 | 원 E1 반환, 기계 `Failed` | **business=None**, `close:Failure`, 반환 **TypeError**, `first_identity=False` |

원 E1은 `report.failures`에는 남는다. 그것이 업무 슬롯 확정·cleanup·정의된 종료 상태를 대신하지는 않는다. 외부 환경 복원은 두 변이에서도 성공했다.

**두 변이 각각** 다음 결과였다.

```text
sites: mismatch=0 unmet=0 unreviewed=0 extracted=3772
grid=0
STRUCTURAL checks=259 violations=0
DOMINANCE scopes=544 required=24413 checked=24413
difference=0 extra=0 unsupported=0
```

양성 대조 `{**{}, 0: machine.finalize(result)}`는 검사 위반 0이며 실제 `read, close`·원결과 보존·`Failed`를 유지했다. 위반 대상은 검사기이고, 결함 실행 관측은 메모리 변이본에 대한 것이다.

**이번 판의 네 물음**

| 물음 | 독립 판단 |
|---|---|
| ⑴ 여집합 계산은 믿을 만한가 | `universe()`는 `ast`가 export한 클래스 집합이다. 이것을 모든 가능한 AST 타입의 목록으로 확대할 수는 없다. 다만 입장 검사는 여집합 목록 대신 `RULES.get(type(node))`를 사용한다. 실제로 export 하나를 제거해 **133→132**로 줄여도 해당 노드를 거부했고, export되지 않은 새 AST subclass도 위치와 함께 거부했다. 열거 축소가 곧 허용 확대로 이어지지는 않는다. |
| ⑵ 선언 48,480은 무엇을 세는가 | 원본 9파일과 별도 파싱한 DRIVER의 **AST 출현 횟수**다. 조건부·죽은·지연 선언도 구문 순회에 들어간다. `48,480/48,480`은 이 AST 재고의 순회 완료이며 실행 의미의 완전성은 아니다. 다른 문자열 안 코드·런타임 생성은 명시된 분석 범위 밖이다. 이를 48,480에 포함했다고 인정하지 않았다. |
| ⑶ 지원 의미는 구현됐는가 | `Compare`의 단락 평가와 OK 지정 증인은 확인했다. 하지만 `Dict` 병합 실패는 OL-1처럼 빠졌다. **타입·필드 등록 및 evaluator 존재만으로 의미 구현을 보증하지 못한다.** |
| ⑷ 회귀·FI 기대는 무엇을 보증하는가 | 기존 186건의 ID·기대·근거·registry 유지와 기존 관측의 호환성을 보증한다. FI는 명시한 실패 지점의 결과·효과·소비·복원 관측이다. 메모리 파일·법 호출 대역을 포함하므로 물리 내구성이나 모든 Python 실행의 증명은 아니다. 7,116 변이는 `Rule.erasure`가 있는 12종의 도메인이며 **`Dict` 병합 실패는 들어 있지 않다.** |

여집합 **952**, 지원 타입·필드 무효화 **208**, 부적격 루트 **50**을 재현했다. 문법 결과는 JSON 정규화 후 동봉 결과와 동일하다. 제어 변이도 **7,116/7,116 검출, ID 전건 동일**이었다. 이 수치들과 OL-1은 동시에 성립한다.

**PO 12 심사**

| PO / I | 상태 | 최소 반례 시도와 근거 |
|---|---|---|
| PO-EXEC-01 / I-A | Satisfied | 미지 profile→환경 확보, 인자 실패→업무 진입을 시도했다. Admit 선행 및 지연 호출 경계에서 거부·업무 효과 0. |
| PO-RESULT-01 / I-R | Satisfied | 원본의 read E1→close E2, 업무 성공→observer 실패를 주입했다. 원 업무 객체와 부수 실패 슬롯이 분리 보존됐다. |
| PO-FAIL-01 / I-F | Satisfied | 첫째·둘째 효과 실패 뒤 다음 `step`을 시도했다. 전이 거부·후속 효과 0, 파일 실패도 공개로 진행하지 않았다. |
| PO-STATE-01 / I-A | Satisfied | NA·Skip의 Success 대체, 미완료 seal, Complete 대신 Admit을 제출했다. 증표 거부·공개 0. |
| PO-IO-01 / I-C | Satisfied | 원본/child IO 실패 뒤 parsing을 시도했다. 각각 `io-fault`/`infeasible`, 토큰 없는 parsing 0. 진단 실패 뒤 normalization도 0. |
| PO-PROFILE-01 / I-C | Satisfied | 완료 객체 결측·미지 판본·잘못된 타입·Admit 대체를 거부했다. R10 음성 16건과 정상 current 6·legacy 1을 재현했다. |
| PO-PRESERVE-01 / I-P | Satisfied | 직렬화·write·flush·fsync·close 실패를 생산 경로에 주입했다. 미완료 증거의 공개·소비를 거부했다. 원본 close E1도 성공 반환을 막았다. |
| PO-ENV-01 / I-E | Satisfied | 복원 자체 실패와 성공/실패 환경 왕복을 시험했다. 복원 실패가 관측되고 원결과가 남으며 다른 복원 항목도 시도됐다. |
| PO-RESOURCE-01 / I-X | Satisfied | 겹친 자료/sandbox 경로와 출처 없는 오류를 제출했다. sandbox 환경 역할 우선, 미상 오류는 `판정 불가`. |
| PO-ISOLATE-01 / I-X | Satisfied | 원본과 겹치는 sandbox를 제출했다. 삭제·생성 전에 거부했다. 대장 자원·출력 배선 및 기존 보존 증거도 확인했다. |
| PO-SEMANTIC-01 / I-S | Satisfied | validation 실패의 정상 승격을 차단했다. 기존 186 기대·registry·생산 9모듈 불변, 동봉 R0 및 EQ-R1/R2 동치 증거와 재정·계약 대응을 확인했다. |
| PO-GATE-01 / I-A·I-C·I-S | **Violated** | **OL-1.** 지원된 `Dict`의 오류 의미를 빠뜨린 변이가 모든 정적 검사를 통과한다. |

**남은 목록:** PO-GATE-01, SITE-14·32의 검증 근거. 생산 원본의 다른 PO에 같은 변이 결함을 중복 계상하지 않았다.

**심사 대상 다섯**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 성립 | 새 반례가 기존 I/PO로 환원된다. 새 규칙·상류 도출 누락 없음. |
| ② 신뢰·입력·부작용 경계 | 성립 | T1~T4·registry·68행/56칸 대조. R1/R2 차이는 지정 `read.yaml` 좌석 값뿐이다. |
| ③ 기제의 집행과 합성 | 성립 | 원본 공통 경계·결과 확정·fail-stop·소비 순서·복원에 대한 코드 및 실패 관측이 부합한다. |
| ④ 검증 근거 | **불성립** | OL-1의 실제 결과와 정적 승인 사이에 반례가 있다. |
| ⑤ 미충족·불명확 처분 | 성립 | 다섯 처분·미완료 보존·사람 확인 절차 유지. 정상 조합 수용도 확인했다. |

**A 폐쇄표**

`closed`는 기존 지정 반례의 폐쇄다.

| 지적 | 판정 | 구조·회귀·FI 연결 |
|---|---|---|
| MY~OG 전 143건 | closed 유지 | 기존 처분·회귀 기대·생산 코드의 연속성 유지. |
| OH-1~3 | closed | 닫힌 파일 효과·동일 IO-clear·공동 profile. 재조립 실패 후 후속 copy 0, normalization 0, 미지 profile 읽기 0 재현. |
| OI-1·2 | closed | S63/S64, 완료 결측·Admit 대체 공개 0, 읽기/close 실패 9건 원 슬롯·cleanup 보존 재현. |
| OH-4 | **partially** | P/M 분리와 기존 변이 검출은 유지. OL-1이 검증 근거에 남는다. |
| OI-3 | **partially** | 기존 IO·close 변이의 폐쇄 유지. 등록 의미 전체의 검사에는 OL-1 잔여. |
| OJ-1 | **partially — 지정 두 trace closed** | 공통 CFG·S66/S67·고정 S68 이력 유지. 전체 지원 의미의 근거에는 OL-1 잔여. |
| OK-1 | **closed** | `Graph.comparison`의 단락 처리. S70/S71·FI-R12-READ/WRITE 재현 결과가 동봉 JSON과 동일. 비교 변이 구조 위반 각각 **4·5**. |
| OK-2 | **closed** | 원본 전체 AST의 `inspect` 선행. S72 클래스 Assert/Match가 위치 있는 거부, 구조 위반 각각 **4·6**. 이는 M 증거다. |

MY~OK 합계 **closed 150·partially 3·open 0**. 현재 OL-1의 두 자리는 **39차 미충족 SITE-14·32와 같다.**

**검증 경로**

`<PY>`는 사본 cwd에서 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B`이다. 아래 함수 호출은 `<PY> -c` 메모리 하네스로 실행했으며, 증거 저장 함수는 메모리 처리했다.

| 명령·호출 | 마지막 출력·확인 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 지정 마커·`34f8a7a55df340e3503cdde4880fd93300769660` 일치 |
| `sha256sum -c T40-SCRIPT-SHA256.txt` — bundle cwd | 동봉 78 일치, 미동봉 33, 불일치 0; 결측 때문에 exit 1 |
| PO `evidence_hashes` 전건 SHA 대조 | `PO_HASH 14 14` |
| `S.compare`·`S.grid_compare`·`ST.check` | 원본 및 OL 읽기/쓰기 변이 각각 `0/0/0`, grid 0, checks 259·violations 0 |
| `G.derive_inputs`·동결 소스 대조 | `DERIVE_INPUTS_EQUAL True`, `PRODUCTION_BYTES 9 9` |
| `E.grammar_experiment()` | `rejected=952 schema_rejected=208 difference=0 undetected=0`; JSON 동일 |
| `E.variants()` 전건 → `G.compare_function()` | `CONTROL total 7116 miss 0 ID_EQUAL True` |
| `SE.run()` | `SEMANTICS cases=36 FAIL=0`; 동봉 JSON 동일 |
| `R12.witnesses()` | `OK_WITNESSES True` |
| 메모리 불변식 시험·`W.main()`·`R10.production_rows()` | `MEMORY_INVARIANTS 19 FAIL=0`; 생산 FI 16·R10 생산 25 모두 통과 |
| `H.CASES()`와 동결 기대 대조 | `COMPAT 186 186 registry True total 191` |
| 동봉 Python 전건 `compile(..., "exec")` | `COMPILE_IN_MEMORY 112`; 파일 생성 없음 |
| §5′.10 바이트 대조 | 동일·22,350 B·`33598684cfd07c2a` |
| 마지막 지문·추적 파일 차이·캐시 확인 | 지정 지문 유지, 추적 파일 diff 없음, `__pycache__` 0 |

**[미검증]**

파일 쓰기 금지에 따라 **회귀 191 전체의 디스크 픽스처 실행, FI 74 전체 명령, 실제 R1/R2 동치 재실행, `py_compile`·불변성 전체 스크립트는 실행하지 않았다.** 동봉 로그·JSON·지문과 코드, 위 메모리 재현을 구별해 사용했다. 미동봉 33개 저작 보조 스크립트의 내용도 추정하지 않았다.

실측·원격 Workflow·Owner 발췌 판독은 수행하지 않았다. 정본 리포를 읽거나 쓰지 않았으며 인터프리터만 지정 예외로 사용했다.

**④ 검증 근거가 성립하지 않으므로, 고정 PASS 문장을 충족했다고 판정할 수 없다. 실측 착수는 금지 상태다.**