# 독립 감수 원문 — M1b 설계 도전 43차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v45(재정 T50 ① C = 비교·집계 층 전수 정비 · 42차 ON-1·ON-2 · 막힌 축 감사 AX-1·AX-a~e 반영) · 판정 REVISE(MED 3) · **새 종류의 규칙 요구: 없음(8연속)** · **`U_r`=6 `B_r`=0 `L_r`=7**(42차 6/0/1 · 41차 6/0/2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-09 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `4bd6f50ba171ca4ed3784b0b06ce507d17eda7293e41a7ffb27e305f7f738cf2` · 22,071 B). 레인 = `~/projects/workspaces/pd-lanes/astra-m1b-t40v45/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③ · L-052 ⑩) · START 05:48:50 · 종료 06:08:29 · **19분 39초** · EXIT 0 · USAGE `input=4,024,574 cached=3,868,800 output=29,268 reasoning=8,560`. 사본 재핀 `df6553744701be6fa2d720614fe2609cde7077e3`(`verify/repin-gate.sh`) · 메모 v45 `b14e21fcc7246ef3` · PO 정본 `38de16c5056111c2` · 대장 `0553bcabf6333296` · 회귀표 207 `15e97ea9bdb61fb8` · 지문표 `376b638fce3d8ff6` · bundle 729 · SPEC `dee3dfe0dfcf5f8b`(18,020 B · `SPEC_HASHES 32건 전건 일치` · `COORD_CHECK bad=0` · 위험 어휘 신규 0).

**판정 = REVISE · 3건(MED 3 · HIGH 0) · 기각 0 · 발주자 귀책.** `Satisfied=11 Violated=1 Unexamined=0` · 갈래 ⑴ 3 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · 심사 ①②③⑤ 성립 · **④ 검증 근거 불성립** · 보조 행 `mismatch=2 unmet=3 unreviewed=0`.

**★ 다섯째 물음이 나왔다.** 총괄이 SPEC ⒜ 에서 「재정 T50 ① 의 네 물음이 전부 참인데 승인된다 — 부족한 것을 문장으로 적으라」고 발주했고, 게이트가 답했다: **「차이를 지우거나 의무를 이행했다고 인정하는 증서가, 실제 정상·오류 완료와 효과 순서 및 합성에서 기존 I 의 보존을 정당화하는가?」** 그리고 **그것이 `PO-GATE-01` 문언에서 도출되므로 새 종류의 규칙 요구가 아니라고 판정했다**(8연속).

**★ 총괄 반례 다섯은 전건 재현됐고, 총괄 주장 하나는 좁혀졌다.** P1·P1b 는 SITE 까지 `0/0/0 · grid 0` 으로 전체 승인 반례가 맞다. **그러나 `P2` 는 SITE `mismatch=3` 이다** — 기존 `write_closed` 의 `seal` 자리 소실·새 helper 안의 `seal`·helper 호출을 검출한다. 그래서 게이트는 P2 를 **「`AX-a` 의 구조 승인 반례이지만 전체 검사 묶음의 승인 반례는 아니다」**로 판정하고 `L_r` 에서 제외했다. **총괄 문서 `M1A-COUNTEREXAMPLE-20260909.md` §4 ⒟ 의 「후보가 만든 새 스코프가 자기 의무를 만들고 자기가 이행했다」는 구조 층에서만 성립한다** — 총괄이 SITE 를 함께 재지 않고 문서를 썼다.

**★ 게이트가 직접 만든 전체 승인 반례 `Q3`.** `write_closed` 의 마지막 한 줄 `machine.seal()` → `{**{}, (1, 2): machine.seal()}`. 빈 mapping 확장·정확한 tuple 키·단일 Call 값이라는 허용 조건을 만족한다. 구조·SITE·grid **전부 0** · `required/checked 25,501/25,501` · 동결 순회 `48,480→48,486` 인데 위반 0 · 추가 연산 occurrence **18** · 국소 증서 있음. 실행에서 `DICT_UPDATE` 자리의 오류가 E2 를 반환해 **E1 identity 가 소실**된다. **총괄이 독립 재현했다.**

**★ 가장 값나가는 발견 = 필수 양성 네 건의 충돌.** `R13-read/write-positive-dict/set` 네 후보에 대해 **`finalize()` 반환 직후 추가된 컨테이너 연산에서만** 오류를 주입하니 read 둘은 cleanup 이 생략되고 write 둘은 원예외 identity 가 소실됐다. 네 후보는 구조·SITE·grid 전건 승인 상태다. 게이트의 결론 = **「`B_r=0` 은 양성군의 의미 건전성을 뜻하지 않는다 · 「정상 protocol 양성」을 「관련 오류 경로까지 보존하는 생산 산출물 양성」으로 승격한 근거가 빠졌다」**. 그리고 **「이 충돌은 총괄이 상신할 구체 근거이며, 도전자가 양성 목록이나 오류 전제를 임의 변경해 해결하지 않는다」**고 못 박았다.

**★ `L_r` 이 1 → 7 로 늘었다.** 목록 = P1·P1b(2) + Q3(1) + 기존 read/write × Dict/Set 필수 양성(4). P2·Q2 는 SITE 가 거부해 제외 · 국소 `import`/`except` 예제와 거부된 후보도 제외. 게이트의 제한 = **「L 의 증가는 검사 범위 확대를 포함하므로 잔여 결함 총량의 증가율로 해석하지 않는다」**.

**★ `AX-a`~`AX-e` 판정** — `AX-c`(`historical_missing` 단독 주입 → `STRUCT-HISTORY` 위반 1) **닫힘** · `AX-d`(finally guard 5복제본 각각 거부) **닫힘** · `AX-b` 대체로 수리(다만 `t40_evidence_r14.py:23` 이 호환 별칭을 일반 `difference` 로 합산 — 기준 자기정합으로만 읽어야 한다) · `AX-a` **미폐쇄**(owner 비교가 국소 증서에 의존) · `AX-e` **미폐쇄**(같은 투영 상등이 차이를 면제).

**★ 감사자가 남긴 미확인 칸의 답** — SITE 입력 A·B 는 각각 `0/0/0`. **SITE 재고의 검출 범위가 막힌 축 감사에서 다룬 선언 의미보다 좁다.**

**★ 진전 판정(재정 T50 ③) — 비감소 셋 모두 · 상신 조건 충족.** `U_r` 은 41·42·43차 **세 판 연속 6**(단위 전체 폐쇄 0) · `B_r` 은 하한 0 · `L_r` 은 2→1→**7**. 게이트가 스스로 「T50 ③ 의 두 판 연속 비감소 상신 조건은 충족됐다」고 적었다. **⑽ ⓑ 자문 트리거도 발동**(컴포넌트 D · `PO-GATE-01` 승인 근거 부류 **8회 연속**)이며 게이트는 T50 ② 의 외부 자문 미실시 처분을 그대로 유지했다.

**발주자 오류 242 — 번들에 법 트리 디렉터리가 빠졌다.** 게이트 [미검증] = 「`bundle/law-ad4c6c3/` 디렉터리는 동봉돼 있지 않았다. 법 62파일은 사본의 핀 git 객체를 읽어 기준 SHA 와 대조했다」. 원인 = `verify/build-bundle.sh` 가 실행본을 옮길 때 `[ -d "$f" ] && continue` 로 **디렉터리를 통째로 건너뛴다**. 판정 영향 없음(게이트가 대체 경로를 찾아 대조하고 그 사실을 적었다). 수리 = 디렉터리도 복사 · 매니페스트를 `find -type f` 기준으로 · 번들 검사에 **법 62파일 계수** 추가. **교훈: 번들 검사는 「필수 파일이 있는가」만 보고 「필수 디렉터리가 있는가」는 안 봤다.**

**처분 = OO-1·OO-2·OO-3 셋 다 수용(공학).** **이행 = Owner 재정 뒤 결정** — 재정 T50 ③ 의 비감소 상신 조건이 충족됐고, 필수 양성 충돌은 게이트가 **명시적으로 총괄 상신 사항**이라 적었기 때문이다. `DISPOSITIONS` 등재 **105/12/117**.

지적 열거 = OO-1, OO-2, OO-3

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE  
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 43회 · PO-GATE-01 승인 근거 부류 8회 연속). T50 ②의 외부 자문 미실시 처분은 유지한다.  
새 종류의 규칙 요구: 없음. 다섯째 물음은 **“차이를 지우거나 의무를 이행했다고 인정하는 증서가, 실제 정상·오류 완료와 효과 순서 및 합성에서 기존 I의 보존을 정당화하는가?”**이며 PO-GATE-01 문언에서 도출된다.  
`U_r`=6 `B_r`=0 `L_r`=7  
비감소: **셋 모두**. `U_r`은 41·42·43차 세 판 연속 6이며 단위 전체 폐쇄가 없다. `B_r`은 하한 0을 유지한다. `L_r`은 2→1→7이며, 이번에는 필수 양성 자체의 오류 경로까지 검사해 잘못된 승인을 추가 발견했다.

**`Satisfied=11 Violated=1 Unexamined=0`. 지적 3건, 모두 갈래 ⑴이다.** 상류 도출 누락·새 보증 요구·ⓑ 대장 누락 반례는 각각 0이다. ④ 검증 근거가 불성립하므로, 제시된 PASS 문장은 충족되지 않는다.

`L_r=7`은 **구조·SITE·격자를 모두 통과하면서 기존 성질을 깨뜨린 서로 다른 생산 후보**의 수다. 구조 검사만 통과하고 SITE가 거부한 P2와 별도 helper 후보는 이 수에 넣지 않았다. 국소 증서만 시험한 합성 예제도 제외했다.

읽기 전용 조건에 따라 판정문은 이 응답으로 납품한다. 소스 변이와 증거 출력은 메모리에서 처리했다.

**동봉 반례 재현**

다섯 입력 모두 발주 수치대로 재현됐다. 재현 실패에 따른 반려 사유는 없다.

| 입력 | STRUCTURAL 검사/위반 | 스코프 | required/checked | CLI TRAVERSAL expected |
|---|---:|---:|---:|---:|
| 원본 | 261/0 | 544 | 25,501/25,501 | 48,480 |
| P1: `seal()`을 Dict 값으로 포장 | **261/0** | 544 | 25,501/25,501 | 48,482 |
| P1b: `append(result)`를 Dict 값으로 포장 | **261/0** | 544 | 25,501/25,501 | 48,482 |
| P2: `seal()`을 지역 helper로 이동 | **261/0** | 545 | **25,504/25,504** | 48,486 |
| P2b: helper에서 `seal()` 두 번 | 260/**17** | 545 | 25,504/25,499 | 48,492 |
| P1d: 컨테이너 안 Call 두 개 | 260/**15** | 544 | 25,500/25,499 | 48,488 |

P1·P1b는 SITE `mismatch/unmet/unreviewed=0/0/0`, grid=0까지 확인했다. **P2는 SITE mismatch=3**이다. 기존 `write_closed`의 `seal` 자리 소실, 새 helper 안의 `seal`, helper 호출을 검출한다. 따라서 P2는 AX-a의 구조 승인 반례이지만 전체 검사 묶음의 승인 반례는 아니다.

원본 AST 집계도 `total=133 supported=77 unsupported=56`으로 일치했다.

**OO-1 · MED — PO-GATE-01 / I-A·I-C·I-S에 연결된 I-R·I-F·I-P 보존 / T3·P6·P7 및 연결 P2 / 갈래 ⑴ / SITE-14·54, 필수 양성의 SITE-32 / 최소 trace: E1 확정 → 기존 호출 완료 → 추가 컨테이너 연산의 E2 → E1 반환 소실 또는 cleanup 생략 / 관측: 투영 상등이 추가 연산과 순회 차이를 함께 면제 / 고치는 문안: “국소 재작성 증서는 제거되는 실행 차이의 정상·오류 완료와 호출자 합성을 정당화해야 한다. 정상 protocol 증서로 오류 보존 의무를 면제하지 않는다. 필수 양성의 승인 요구와 그 의미 보존 근거를 함께 검증한다.”**

[local_certificate()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_comparison.py:102)는 투영 상등과 재작성 발동을 검사한다. [semantic_delta()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_operations.py:405)는 그 증서, 기준 잔여 0, 추가 연산의 `protocol_safe=True`를 조건으로 problems를 빈 목록으로 돌려준다.

그러나 [Graph.operation()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_control.py:277)은 안전한 내장 protocol에도 ambient 오류 간선을 남긴다. **오류 간선의 존재와 그 오류가 원결과를 보존한다는 승인 근거는 다르다.**

직접 만든 전체 승인 반례 Q3는 `write_closed`의 마지막 한 줄만 다음과 같이 바꾼 것이다.

```python
# 원본
machine.seal()

# Q3
{**{}, (1, 2): machine.seal()}
```

Q3는 빈 mapping 확장·정확한 tuple 키·단일 Call 값이라는 허용 조건을 만족한다.

| Q3 관측 | 결과 |
|---|---|
| 구조·SITE·grid | **261/0 · 0/0/0 · 0** |
| required/checked | **25,501/25,501** |
| 실제 동결 순회 비교 | **48,480→48,486**, 위반 0 |
| 연산 비교 | 기준 잔여 0, 추가 연산 occurrence **18**, 국소 증서 있음 |
| 원본 실행 | E1 identity 유지, `enter, write, close` |
| 후보 실행 | `seal()` 반환 뒤 **DICT_UPDATE** 오류 주입에서 E2 반환, E1 identity 소실 |

실행에는 실제 생산 함수와 메모리 IO 하네스를 사용했다. 오류는 추가된 opcode 자리에서만 주입했다. 원본은 그 자리에 도달하지 않는다. P1의 BUILD_MAP, P1b의 append 이후 BUILD_MAP에서도 같은 방식으로 원결과 소실을 확인했다.

음성 대조도 유지됐다. `{machine.seal(): (1, 2)}`는 **위반 8**이다. 실제 `seal()`은 `self`를 반환하므로 키 위치에 필요한 `NoneType` 반환 근거가 없다. 국소 시험에서도 미상 Call의 키/Set 원소 사용, 미상·비해시 키, Call 두 개, 비어 있지 않은 미상 mapping 확장은 투영되지 않았다. **허용 경계가 존재한다는 사실은 그 안의 의미 보존을 증명하지 않는다.**

동결 순회 비교도 같은 문제를 공유한다. [traversal_comparison()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_comparison.py:136)은 실제 동결 기준을 읽지만, 투영이 같으면 개수 차이를 면제한다. 별도로 CLI `TRAVERSAL expected`는 후보 순회의 자기 기대값이다. 이 출력의 차이 0을 동결 기준 동치의 증거로 사용할 수 없다.

**필수 양성에서 발견한 추가 네 건**

`R.positives()`의 지정 19항은 모두 승인됐다. 그중 기존 read/write Dict·Set 양성 네 후보에 대해 **`finalize()` 반환 직후 추가된 컨테이너 연산에서만** 오류를 주입했다.

| 기존 필수 양성 | 추가 실패 자리 | 독립 실행 결과 |
|---|---|---|
| R13-read-positive-dict | BUILD_MAP | `read, close`→`read`; cleanup 생략, MemoryError 반환 |
| R13-read-positive-set | BUILD_SET | 동일 |
| R13-write-positive-dict | BUILD_MAP | 원예외 identity 소실, machine=`BusinessResultFinalized` |
| R13-write-positive-set | BUILD_SET | 동일 |

원본에는 해당 추가 실패 자리가 없으며 기존 결과를 유지했다. 네 후보는 앞서 재실행한 구조·SITE·grid에서 모두 승인됐다.

따라서 **`B_r=0`은 양성군의 의미 건전성을 뜻하지 않는다.** “정상 protocol 양성”을 “관련 오류 경로까지 보존하는 생산 산출물 양성”으로 승격한 근거가 빠졌다. 이 네 후보를 조용히 거부하면 기존 필수 양성 승인 요구와 충돌한다. 반대로 추가 오류를 제외하면 기존 전제를 변경한다. 이 충돌은 총괄이 상신할 구체 근거이며, 도전자가 양성 목록이나 오류 전제를 임의 변경해 해결하지 않는다.

**OO-2 · MED — PO-GATE-01 / I-A·I-S에 연결된 호출·완료·원결과 보존 / T3·P6·P7 / 갈래 ⑴ / SITE-14·54 및 그 승인 비교 / 최소 trace: helper 정의 → import 또는 except 이름 재결속 → helper 호출을 원본 호출로 투영 → 실제로 다른 객체 호출 또는 미결속 오류 / 관측: `_expanded=True`, 국소 증서 있음, 연산 위반 0인데 실행은 TypeError/UnboundLocalError / 고치는 문안: “helper 확장은 Python의 실제 이름 결속·삭제와 호출 frame의 관련 오류까지 보존 근거에 포함한다. Name(Store) 부재를 재결속 부재로 대체하지 않고, owner 비교 성공을 독립 의미 근거 없이 새 스코프 이행으로 승격하지 않는다.”**

[expand_helpers()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_control.py:160)의 무인자·decorator·본문 형태·재귀·명시 대입·standalone·정의 순서·중단 조건을 각각 공격했다. 통상적인 위반 예제는 모두 확장되지 않았다.

하지만 **나머지 일곱 조건을 만족하고 ‘재결속 없음’만 깨는** 다음 국소 후보는 확장됐다.

```python
# 기준
def owner():
    import builtins as _h
    tick()

# 후보
def owner():
    def _h():
        tick()
    import builtins as _h
    _h()
```

실측은 `certificate=True`, `semantic_delta=0`이다. 기준은 `tick` 후 정상 반환하고, 후보는 `tick` 없이 **TypeError**를 낸다. `import` 별칭은 `ast.Name(Store)`가 아니기 때문이다.

같은 방식으로 `except Exception as _h`가 이름을 결속하고 handler 종료에서 삭제하는 후보도 시험했다. 기준은 `tick` 후 반환했지만 후보는 **UnboundLocalError**를 냈다. 이 역시 증서 있음·연산 위반 0이었다.

두 예제는 **국소 증서의 전제 검사 반례**다. 고정 생산 9모듈의 전체 승인 반례로 세지 않았다.

생산 후보에서는 P2와 별도 Q2를 확인했다. Q2는 `remember`의 append를 `_remember_once()`로 옮긴 것이다. 둘 다 구조 검사는 통과하고, 추가 helper frame 진입의 오류 주입에서 원결과를 잃는다. 둘 다 SITE가 3건으로 거부하므로 `L_r`에서는 제외했다.

AX-a의 새 경로는 이제 무조건 checked가 아니다. [owner_ok](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_dominance.py:273)에 의존한다. **문제는 그 owner 비교가 위 국소 증서에 의존한다는 점이다.** P2에서 새 세 의무가 required와 checked에 함께 들어가는 현상은 재현됐으며, 의미 근거의 폐쇄로 인정할 수 없다.

**OO-3 · MED — PO-GATE-01 / I-A·I-C·I-S의 승인 근거 및 미해결 비승인 / T3·P6·P7, 재정 T50 ① / 갈래 ⑴ / SITE-14·32·54의 승인 공통부 / 최소 trace: 동결 검사기·어휘 재고 일치 → 역사 pending=0 → U1~U6 근거 미완 상태에서 승인 / 관측: 가족 검사 ID가 자리별 의미 집행을 구속하지 않고 독립 미해결 근거는 승인 조건 밖 / 고치는 문안: “독립 의미와 기존 I에서 도출한 근거별 검증을 후보와 승인 결정에 결부한다. 어휘 재고·가족 시험·역사 pending의 성공을 그 검증으로 대체하지 않는다.”**

비교 재고는 직접 재열거해 **12모듈·5,905자리·선택 차집합 0·AST 서명 차이 0·일반 미검증 5,387자리**를 확인했다. 저작자의 “같은 검사기 소스에서 명시한 구문 부류를 두 번 열거한 결과의 일치”라는 한정은 정확하다.

그러나 가족 ID는 자리별 의미를 구속하지 않는다.

| 표본 | 연결된 가족 검사 | 직접 확인한 공백 |
|---|---|---|
| `t40_control.py:185` 재결속 검사 | S73·S77·S84·S88 | import 별칭·except 대상 재결속을 놓쳐도 확장·증서 성공 |
| `t40_comparison.py:45` 빈 mapping 조건 | S83·S85·S86·S87 | Q3가 조건을 만족하면서 추가 오류로 원결과 소실 |
| `t40_structure.py:392` pending 검사 | S81·S83·S85·S87 | 역사 관계 pending만 검사; U1~U6 전체 근거를 검사하지 않음 |

[verify_authority()](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_comparison_census.py:171)는 검사기 바이트와 선택된 구문 재고를 동결값에 대조한다. **동결된 구현의 의미 건전성을 검사하는 함수는 아니다.**

[구조 승인 조건](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:391)은 `missing/extra`, `semantic_proof_pending`, `historical_missing`을 확인한다. 반면 지배 보고의 `independent_proof_obligations`·`proof_status`는 U1~U6 미완성을 표시하면서도 별도 비승인 조건이 아니다. 따라서 ON-2는 미폐쇄다.

**AX-a~e와 SITE 판정**

| 좌표 | 판정 |
|---|---|
| AX-a | 후보 grammar 검사와 owner 의존은 연결됐다. P2와 helper 증서 반례 때문에 **전체 의미 폐쇄는 아님**. |
| AX-b | 활성 `compare()`는 후보 AST inventory와 양방향 사건 차이를 본다. 해당 결손은 수리됐다. 다만 `t40_evidence_r14.py:23`은 아직 호환 별칭을 일반 `difference`로 합산한다. 그 수는 기준 자기정합으로만 읽는다. |
| AX-c | `historical_missing` 단독 주입이 **STRUCT-HISTORY 위반 1**로 이어졌다. 지정 집행 공백은 닫혔다. |
| AX-d | finally guard **5복제본 각각**의 우회 간선 주입을 재실행해 모두 거부했다. 지정 복제본 누락은 닫혔다. 전체 finally 의미 정리로 확대하지 않는다. |
| AX-e | 동결 기대값은 생겼다. 그러나 같은 투영 상등으로 차이를 면제하므로 **독립 승인 근거로는 미폐쇄**다. |
| SITE 입력 A·B | 각각 **0/0/0**. SITE 재고의 검출 범위가 감사에서 다룬 선언 의미보다 좁다. grid의 10·3은 구조 검사를 다시 호출한 결과다. |

기존 최소 입력도 원본부터 다시 실행했다. ON-1은 **16**, AX-1 A는 **10**, B는 **3**으로 거부됐다. A에서는 동결 순회 **48,480→48,478** 차이 위반도 발생했다. 이 세 입력의 폐쇄를 해당 부류 전체 폐쇄로 읽지 않는다.

**세 수의 독립 도출**

`U_r`은 검사기의 목록을 복사하지 않고, 구체 실행에서 기존 I에 대한 승인 결론까지 필요한 연결을 다시 셌다.

| 단위 | 필요한 근거 | 이번 전체 폐쇄 |
|---|---|---|
| U1 | 구체 연산의 정상·오류 완료를 추상 transfer가 보존 | 미폐쇄. 추가 연산의 정상 protocol과 오류 보존을 잇는 근거가 없음 |
| U2 | 순차·분기·반복·handler·finally·with의 완료 합성 | 미폐쇄. 컨테이너 오류 뒤 원결과·cleanup 보존 반례 확인 |
| U3 | 실제 callable 결속·암묵 호출·지연·재개의 호출자 합성 | 미폐쇄. import/except 재결속 및 helper frame 공백 확인 |
| U4 | 포착·저장·정리 자체 오류에서 원결과 유지 | 미폐쇄. append 뒤·finalize 뒤·seal 뒤의 E2 반례 확인 |
| U5 | 동결 기준 산출물이 연결 I를 만족한다는 승인 근거 | 미폐쇄. 바이트 동일성·유한 증인 외 전체 근거가 부족하며 필수 양성의 오류 경로도 반증됨 |
| U6 | 비교 성공이면 후보의 연결 I가 보존된다는 충분성 | 미폐쇄. 전체 검사 승인 반례 7개 확인 |

**전체 폐쇄 0개이므로 `U_r=6`이다.** 도출 기준을 바꾸거나 항목을 추가해서 6이 된 것이 아니다. 여섯 단위는 검증 가능한 의미 모델·합성 근거 또는 산출물별 증명으로 닫을 수 있는 의무다. 다만 이번에 드러난 필수 양성의 의미 충돌을 그대로 두면 승인 근거를 완성할 수 없다.

`B_r=0`은 다음 범위에서 판단했다.

- 지정 19항을 직접 재실행해 비승인 0.
- S48을 포함한 국소 코드 양성 9항을 직접 재실행해 모두 유지.
- 고정 PO에서 양성·legacy 연결을 독립 추출: **147개, 중복 제외 49 ID**, 제출 대응과 차이 0.
- 나머지 legacy/API·EQ-R1/R2·호환 범위는 동봉 실행 원자료와 고정 metadata를 대조했다.

범위는 19항만 보던 때보다 넓어졌다. 그러나 **B의 범위 충족과 양성 의미의 타당성은 별개**다. 초기 S48 12/13 실패와 수리 뒤 13/13도 동봉 자료에서 확인했고, 최종 helper 양성은 직접 재실행했다.

`L_r=7`의 목록은 다음과 같다.

| 포함 | 산출물 수 |
|---|---:|
| P1·P1b | 2 |
| 직접 만든 Q3 | 1 |
| 기존 read/write × Dict/Set 필수 양성 | 4 |
| **합계** | **7** |

동일 후보의 여러 오류 주입은 중복 계상하지 않았다. P2·Q2는 구조만 승인되고 SITE가 거부하므로 제외했다. 국소 import/except 예제와 거부된 Q1·P2b·P1d도 제외했다.

**PO Violated는 계속 1인데, B는 0이고 L은 7이다.** 하나의 메타 의무 아래 여러 잘못된 승인이 존재하며, 필수 양성 승인 유지가 의미 건전성의 진전과 일치하지 않는 지점이다. L의 증가는 검사 범위 확대를 포함하므로 잔여 결함 총량의 증가율로 해석하지 않는다. T50 ③의 두 판 연속 비감소 상신 조건은 충족됐다.

**PO 12 심사**

변이 후보의 결함은 승인 검사기의 PO-GATE-01에 계상했다. 고정 생산 원본의 다른 PO 위반으로 중복 계상하지 않았다.

| PO / I | 상태 | 근거 |
|---|---|---|
| PO-EXEC-01 / I-A | Satisfied | 공통 지연 실행·인자 실패·선행 증표 배선 및 메모리 시험 확인 |
| PO-RESULT-01 / I-R | Satisfied | 원본의 업무·observer·진단 실패에서 identity 보존 확인 |
| PO-FAIL-01 / I-F | Satisfied | 첫째·후속 업무 실패 이후 금지 효과 0 |
| PO-STATE-01 / I-A | Satisfied | Skip/NA 승격 금지, 미완료 봉인·봉인 뒤 효과 거부 확인 |
| PO-IO-01 / I-C | Satisfied | 원본/sandbox IO 처분 구분, 무증표 parsing 거부 확인 |
| PO-PROFILE-01 / I-C | Satisfied | 미지 판본 거부, current/legacy 정상 수용 유지 |
| PO-PRESERVE-01 / I-P | Satisfied | 고정 원본의 결과 확정·close·공개 배선과 기존 FI 증거 유지 |
| PO-ENV-01 / I-E | Satisfied | 성공·실패 환경 왕복 및 복원 실패의 명시 관측 재현 |
| PO-RESOURCE-01 / I-X | Satisfied | 자원 역할표·미상 처분·자원 출처 배선과 고정 증거 확인 |
| PO-ISOLATE-01 / I-X | Satisfied | 보호 집합·출력 경계·sandbox 선검사와 기존 격리 증거 유지 |
| PO-SEMANTIC-01 / I-S | Satisfied | 생산·registry·기존 201 metadata 불변, 호환·EQ 원자료 대조 |
| PO-GATE-01 / I-A·I-C·I-S | **Violated** | OO-1~3: 잘못된 승인, helper 전제 결손, 전체 근거의 승인 결부 공백 |

**`Satisfied=11 Violated=1 Unexamined=0`.** PO를 심사하지 않은 항목은 없다. PO-GATE-01 내부의 미해결 증명 여섯 단위는 그 PO의 위반 근거이며 PO `Unexamined` 수와 다르다.

보조 행 심사는 **`mismatch=2 unmet=3 unreviewed=0`**이다. 직접 승인 반례가 있는 SITE-14·54를 mismatch로, 전체 승인·합성 근거가 남은 SITE-14·32·54를 unmet으로 센다. 검사기의 재고 출력 0/0/0과 구별한 독립 심사 수다.

**남은 목록:** PO-GATE-01, OO-1~3, SITE-14·32·54의 승인·합성 근거, U1~U6, 필수 양성 네 후보의 승인 요구와 오류 의미 보존 사이의 충돌.

| 심사 대상 | 판정 |
|---|---|
| ① 도출의 완전성 | 성립. 발견은 기존 PO/I·P/T에서 도출됨 |
| ② 신뢰·입력·부작용 경계 | 성립. 고정 경계와 선등록 대응 유지 |
| ③ 기제의 집행과 합성 | 고정 생산 원본의 기존 배선·관측 범위에서 성립 |
| ④ 검증 근거 | **불성립** |
| ⑤ 미충족·불명확 처분 | 성립. 기존 다섯 처분 유지; 승인 검사 결손은 ④에 계상 |

**검증 경로**

아래 `<PY>`는 사본 cwd에서의  
`PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B -`이다. `sys.path[0]`은 사본의 `bundle`로 지정했다. `R.write`·`R15.put` 등 시험 산출물 저장 함수는 메모리 처리로 대체했다.

| 명령·호출 | 마지막 출력·확인 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | path/pin/order/disposable 및 `df655374…` 일치 |
| `<PY>` 지정 지문·전체 스크립트표 SHA 대조 | 지정 5개 지문 일치, **186/186**, 불일치·미동봉 0 |
| `<PY> ST.check(W)` — 다섯 메모리 후보 | 위반 **0·0·0·17·15** |
| `<PY> R.static(...)` — 원본·ON-1·A·B | 위반 **0·16·10·3** |
| `<PY> R.static(...)` — P1·P1b·Q3 | 구조·SITE·grid **전부 0** |
| `<PY>` 추가 opcode/frame 오류 주입 | 원본 E1 보존, 후보 E2 또는 원결과 소실 |
| `<PY>` 필수 Dict/Set 양성 오류 주입 | read cleanup 생략 2건, write identity 소실 2건 |
| `<PY>` helper 경계·실제 실행 | import/except: 증서 있음·연산 위반 0, TypeError/UnboundLocalError |
| `<PY> R15.finally_copies(); E.sinks()` | 복제본 **5/5 거부**, 집계 sink **5/5 거부** |
| `<PY> C.collect()` | **12 / 5905 / 차이 0 / 서명 차이 0 / 일반 5387** |
| `<PY> R.positives(); E.local_positives()` | **19 B_r=0**, S48 포함 국소 양성 **9항 통과** |
| `<PY>` 메모리 불변식 시험 | **17건 FAIL 0** |
| `<PY>` 고정 PO 양성 연결 독립 추출 | **147 연결·49 ID·차이 0·nonpass 0** |
| `<PY> H.CASES()` 및 기준 metadata 대조 | **207**, 기존 201 변경 0, 신규 S85~S90 |
| `git ls-tree`·`git show origin/t40-base:<path>` | 법 **62파일**, 목록·개별 SHA 차이 0 |
| 계측 브랜치 diff | R1 effort 두 곳, R2 model/effort만 변경 |
| `<PY>` 불변 절·registry·compile 대조 | §5′.10 **22,350B / 33598684cfd07c2a**, registry 동일, J118·SITE68, 134파일 정상/-O compile 성공 |
| 최종 SHA·git 상태·캐시 확인 | **186/186**, 추적 변경 0, `__pycache__` 0 |

**[미검증]**

전체 회귀 207·FI 76·실제 EQ-R1/R2의 디스크 실행은 다시 수행하지 않았다. 이 부분은 동봉 로그·JSON·고정 metadata·지문으로 심사했다. 오류 경로 실험은 실제 생산 함수에 대한 메모리 IO 및 지정 opcode/frame 오류 주입이며, 네이티브 allocator를 실제 고갈시킨 시험은 아니다.

`bundle/law-ad4c6c3/` 디렉터리는 동봉돼 있지 않았다. 법 62파일은 격리 사본의 핀 git 객체를 읽어 기준 SHA와 대조했다. 따라서 실행본 디렉터리 자체의 재검증으로 표현하지 않는다.

일반 5,387자리 전체의 개별 데이터 흐름·판정 도달, 지원 transfer·호출·완료 합성 전체의 증명은 수행되지 않았다. 원격 Workflow·실측·Owner 발췌 판독도 수행하지 않았다. 정본 리포는 지정 Python 인터프리터 사용 외에는 접근하지 않았으며 파일을 쓰지 않았다.