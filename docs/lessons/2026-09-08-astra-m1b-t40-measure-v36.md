# 독립 감수 원문 — M1b 설계 도전 36차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v38(불변식 I · 증명 의무 PO · 상태기계 · 재정 T47 · 자문 5회차 발주문 구현) · 판정 REVISE(HIGH 1 · MED 3) · **새 종류의 규칙 요구: 없음**

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-08 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `35d649258625be8eb4c360335007ea6f64182b814fbe1544ba05712af9e152d7` · 18376 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v36/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · Monitor(00:42 기동 · 01:2x 종료 · USAGE 는 레인 STATUS). 사본 재핀 `da846c3` · 메모 v38 `3efce46680aad255` · PO 정본 `bc8dc3d4c40f0951` · 대장 `3e446c2a2ab13685` · 회귀표 v16(174) · bundle 187. 이번 기동 = 재정 T47 ①② 효력(자문 5회차 발주문 → astra xhigh 8차 구현 → 36차) · **판정 방법 = PO 12 Satisfied/Violated/Unexamined + ⓐⓑⓒ + 「새 종류의 규칙 요구」**.

**판정 = REVISE · 4건(HIGH 1 · MED 3) · 기각 0 · 발주자 귀책(저작 astra xhigh 8차 · 발주·검수 총괄).** 지문 24 일치(지문표의 저작 보조 25 파일은 미동봉 · 불일치로 안 셈) · 정적 `0/0/0 grid=0` · `STRUCTURAL checks=211 violations=0` 재현 · 심사 ① 성립 · ②~⑤ 불성립 · 갈래 ⑴ 4 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0 · **「새 종류의 규칙 요구: 없음」 — 「확인한 반례는 기존 I-A·I-R·I-F·I-C·I-P·I-X·I-S 의 구현 위반 또는 증거 부족으로 환원된다」(자문 5회차 최상위 원칙의 첫 충족).** **PO 진행도(새 기준선 · 재정 T47) = `Satisfied=2 Violated=10 Unexamined=0`**(Satisfied = PO-ENV-01 · PO-ISOLATE-01) · 보조 행 단위 `mismatch=9 unmet=9 unreviewed=0`(35차 10행 중 8 폐쇄 · 2 잔여(46·56) + 새 7 = SITE-03·10·11·32·37·38·39·46·56). A 폐쇄표 closed 138 · partially 5(NZ-3 · OA-3 · OE-3 · OF-4 · OG-1) · open 0 · OC-3·OF-1·OG-2~5 closed. **OH-1 HIGH · I-R·I-F·I-P·I-X·I-S · SITE-11·37·38·39**: 재조립기의 표식·run.yaml·응답·봉투 공급이 `open(...).write(...)` 로 파일을 열어 **소멸자 flush 실패**가 원 예외로 포착되지 않고 다음 `copy_input_tree` 가 실행됨(`trace=['flush_failure','later_copy'] disposition=mismatch original_preserved=False`) · `TrackedFile`·`write_closed` 의 FI-WRITE/FLUSH/FSYNC/CLOSE 는 이 파일 생명주기를 지나지 않음. **OH-2 MED · I-C · SITE-46·56**: `io_gate` 가 `diagnostic_failure` 로 거부한 뒤 `receipt_post` 가 별도 조건식으로 파싱 허가를 재계산해 JSON 정규화 1회 실행(금지 전이의 표현). **OH-3 MED · I-A·I-C · SITE-03·10·32**: current5 의 `projection` stage 가 허용 집합에는 있으나 필수 성공·outcome 정합 검사에서 빠져 `projection=Failure/Skip/NotApplicable` 이 승인됨 · `author_input('unknown-v9')` 가 profile 거부 **전에** 파일을 읽음(I-A 「없는 조합은 실행 0」 위반). **OH-4 MED · PO-GATE-01 증거 의무**: `receipt_post.raw_only` 허가 조건을 무효화하는 변이에 구조 검사·대장 검사 모두 0(현재 생산 helper 의 IO 허가 조건이 검사 밖) · FI 29 의 일부 행(`later=0` · `artifact_consumable=False` · 최종 상태)이 생산 경로 관측이 아닌 모형 상수.

**게이트 소견(원문 요지)**: 「이번 반례는 새 규칙을 요구하지 않는다 — 분류 체계의 폐쇄에는 전진. 그러나 실행 경계의 이름을 공유하는 것과 파일 생명주기·파싱 허가·profile 완료 증표를 실제로 공유하는 것은 아직 다르다. 다음 수리는 새 예외 목록보다 **모든 파일 효과의 명시적 종료 · IO-clear 증표의 끝까지 전달 · profile 상태표의 생산·소비 공동 집행**으로 설명돼야 한다. 현재 관측 = 불변식 집합은 반례를 수용하지만 구현과 증거는 아직 그 집합을 만족하지 못한다.」

**T44 판정(§3 보정 · T47 새 기준선)** = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ · **새 종류의 규칙 요구 없음** ✓ → 자동 기동. 진행도 기준선 = **PO 2/10/0(36차)** · 두 회차 연속 비감소 판정은 Violated 수로 37차부터.

**처분 = 전부 수용(공학) · 이행 = v39 저작(astra xhigh 9차 · 자문 5회차 발주문 §11·§13 원칙 유지 · OH-1~4 를 새 예외 분기가 아니라 게이트 소견의 셋으로 닫는다).** 수정 문안(도전자 원문) — OH-1 「재조립기의 표식·run.yaml·응답·봉투 공급은 공통 닫힌 파일 전이를 사용하며, close 성공 증표 전에는 다음 효과를 실행하지 않는다」 · OH-2 「후채집은 해당 호출의 IO-clear 증표를 받아 의미 채집 여부를 결정하고, 증표가 없으면 원시 바이트만 보존한다」 · OH-3 「작성 profile 은 IO 전 Admit 에서 확인하고, current5 는 outcome 별 필수·금지 stage 상태표 전체와 대조한다」 · OH-4 「정적 검사의 미분석 경로를 명시하고, PO 증거는 실제 생산 경로의 실패·후속 효과·소비 결과를 관측한 것과 모형 시험을 구분한다」. 발주자 오류 누계 224 → **228**.

지적 열거 = OH-1, OH-2, OH-3, OH-4

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 36회)
새 종류의 규칙 요구: 없음

**확인한 반례는 기존 I-A·I-R·I-F·I-C·I-P·I-X·I-S의 구현 위반 또는 증거 부족으로 환원된다.** 불변식 집합 밖의 새 보증은 요구하지 않는다. 그러나 보존·파싱·profile 경계가 아직 합성되지 않아 PASS 문장은 성립하지 않는다.

마커의 path·pin·order/disposable과 HEAD `da846c3f97fd470ece910ffae9e10235dfafdecb`를 확인했다. v38·PO·대장과 동봉된 지문표 대상 **24개는 모두 일치**했다. 지문표에만 있는 저작 보조 파일 25개는 부재하며, 이를 지문 불일치로 세지는 않았다.

**지적 목록**

**OH-1 · HIGH — 재조립 파일의 소멸자 flush 실패가 원결과와 fail-stop 경계를 빠져나간다.**

- 위반: **I-R·I-F·I-P·I-X·I-S / PO-RESULT·FAIL·PRESERVE·RESOURCE·SEMANTIC-01**. P2·P7, 갈래 **⑴**.
- 자리: **SITE-11·37·38·39**.
- 좌표: [t40_replay.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:77) `sandbox_prepare`, `_reconstruct:241·270·279`의 `open(...).write(...)`; [t40_resources.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_resources.py:176) `TrackedFile`.
- 최소 trace:

  `허용된 sandbox → write가 버퍼에 성공 → 임시 파일 객체 소멸 중 flush 실패 → 원 예외 미포착 → 다음 copy_input_tree 실행`

실제 `io.BufferedWriter`와 메모리 RawIO에 flush 실패를 주입했다. **실제 `R.bind`·`external_scope`·`TrackedFile`을 유지해도** 다음 결과였다.

```text
trace=['flush_failure', 'later_copy']
disposition=mismatch
original_preserved=False
environment=True
actual_writes=0
```

후속 자료 오류를 공급하면 첫 환경 IO 실패가 사라지고 `mismatch`가 된다. 소유 표식에서도 flush 실패 뒤 `sandbox_prepare()`가 정상 준비를 뜻하는 `None`을 반환했다.

`write_closed`의 FI-WRITE/FLUSH/FSYNC/CLOSE는 이 파일 생명주기를 통과하지 않는다. 명시적 `write` 호출이 대장에 있다는 사실도 소멸자 실패를 포착하지 못한다.

**고치는 문안:** “재조립기의 표식·run.yaml·응답·봉투 공급은 공통 닫힌 파일 전이를 사용하며, close 성공 증표 전에는 다음 효과를 실행하지 않는다.”

---

**OH-2 · MED — IO-clear 거부 뒤 `raw_post`가 독자적으로 파싱을 다시 허용한다.**

- 위반: **I-C / PO-IO-01**, 관련 PO-GATE-01. P2·P7·T3, 갈래 **⑴**.
- 자리: **SITE-46·56**.
- 좌표: [t40_drive.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:553) `_read_command:553~568`; [t40_receipts.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:257) `receipt_post`.
- 최소 trace:

  `업무 ValueError 확정 → traceback 생성 실패 → diagnostic_failure=True → io_gate 거부 → receipt_post의 raw_only=False → artifact JSON 정규화`

`_project_business`의 실제 진단 생성 위치에 실패를 넣어 outcome을 만들었다. `io_gate`는 거부했지만 `receipt_post`는 JSON 정규화를 **1회 실행**했다. 원 업무 예외는 보존됐다.

원인은 `io_gate`가 `diagnostic_failure`를 차단 조건으로 삼는 반면, `receipt_post:259`가 별도 조건식으로 파싱 허가를 재계산하기 때문이다. 현재 오류가 최종 적격 결과로 승인됐다는 주장은 아니다. **실패 후 금지된 파싱 전이가 이미 표현된다**는 반례다.

**고치는 문안:** “후채집은 해당 호출의 IO-clear 증표를 받아 의미 채집 여부를 결정하고, 증표가 없으면 원시 바이트만 보존한다.”

---

**OH-3 · MED — 유한 profile의 입장 조건과 완료 상태 제약이 불완전하다.**

- 위반: **I-A·I-C / PO-EXEC·STATE·PROFILE-01**. P7·T3, 갈래 **⑴**.
- 자리: **SITE-03·10·32**.
- 좌표: [t40_receipts.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:377) `load_receipts:377~400`; [t40_consume.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_consume.py:24) `author_input`.

첫째 최소 trace:

`current5 · return/Success · observation=Success → projection=Failure → load_receipts 승인`

저작자의 `make_receipt()`에 `projection`만 추가한 메모리 대조 결과:

```text
CURRENT_PROJECTION Failure admitted True
CURRENT_PROJECTION Skip admitted True
CURRENT_PROJECTION NotApplicable admitted True
```

`projection`은 허용 stage 집합에 있지만 필수 성공·outcome 정합 검사에서 빠졌다. 후속 소비 코드에도 이 상태를 다시 검사하는 자리가 없다. **최종 metrics 완주를 재현했다는 뜻은 아니며**, 선언된 current 상태 정합 검사가 모순을 승인한다는 반례다.

둘째 최소 trace:

`author_input('unknown-v9', path) → open/read 1회 → profile 거부`

명시적 인자인 작성 profile을 거부하기 전에 파일을 읽는다. 이는 I-A의 “없는 조합은 실행0으로 거부” 및 architecture의 Admit 조건과 맞지 않는다. S55는 거부 여부만 확인한다.

**고치는 문안:** “작성 profile은 IO 전 Admit에서 확인하고, current5는 outcome별 필수·금지 stage 상태표 전체와 대조한다.”

---

**OH-4 · MED — 구조·FI 증거가 실제로 확인한 범위보다 넓은 명제를 지지한다고 적혔다.**

- 위반: **I-A·I-C·I-S / PO-GATE-01**의 증거 의무. P2·P7, T45 ②·자문 §8·§12 F, 갈래 **⑴**.
- 자리: **SITE-46·56**의 검사 증거. 추가 미충족 행으로 중복 계산하지 않았다.
- 좌표: [t40_structure.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_structure.py:255) `check`; [t40_invariant_tests.py](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_invariant_tests.py:37) `machine_fault` 등.
- 최소 변이 trace:

  `receipt_post.raw_only = False and (기존 조건식) → IO 차단 무효 → 구조 검사0 → 대장 검사0`

파일을 고치지 않고 읽기 대역에서만 변이했다.

```text
STATIC_RAW_POST_FALSE structural 0 mismatch 0 unmet 0 unreviewed 0
```

이는 임의 Python 전체의 형식 증명을 요구하는 지적이 아니다. **현재 생산 helper의 IO 허가 조건**이 검사 밖인데, 그 경로도 구조적으로 닫혔다고 판단한 증거 공백이다. OH-2가 원본 코드에서 같은 공백의 실제 반례다.

FI 29개에는 자문 §8의 13개 명목 지점이 모두 있다. 다만 일부 행의 `later=0`, `artifact_consumable=False`, 최종 상태는 생산 경로 관측이 아닌 상수·별도 모형 값이다. 예를 들어 `machine_fault`의 `later` 목록은 실행 효과에 연결되지 않는다. 재현 성공은 인정하지만 **29행 모두가 생산 경로에서 다섯 항목을 실관측했다는 주장**은 인정하지 않는다.

**고치는 문안:** “정적 검사의 미분석 경로를 명시하고, PO 증거는 실제 생산 경로의 실패·후속 효과·소비 결과를 관측한 것과 모형 시험을 구분한다.”

**PO 독립 판정**

아래 상태는 각 PO의 담당 의무별 판정이다. 같은 I를 공유한다는 이유만으로 모든 PO를 자동으로 같은 상태로 만들지는 않았다.

| PO | 상태 | 독립 심사 근거 |
|---|---|---|
| PO-EXEC-01 | **Violated** | lazy 인자 포착과 FI-ARG는 재현. 작성 profile의 입장 전 IO가 남음 — OH-3 |
| PO-RESULT-01 | **Violated** | runner·observer 원 객체 보존은 확인. 재조립 파일의 원 flush 예외는 실행 기록에서 소실 — OH-1 |
| PO-FAIL-01 | **Violated** | Machine·dispatch의 명시 실패 정지는 확인. 소멸자 실패 뒤 후속 복사1 — OH-1 |
| PO-STATE-01 | **Violated** | NA require·미완료 seal·봉인 후 tail 거부 재현. current projection 모순 승인 — OH-3 |
| PO-IO-01 | **Violated** | 원본·child IO gate와 토큰 거부 재현. raw_post의 독자 허가가 거부를 뒤집음 — OH-2 |
| PO-PROFILE-01 | **Violated** | legacy 탐지 실패·미지 버전·기존 current 음성 사례 재현. 완료 상태표와 작성 Admit 결손 — OH-3 |
| PO-PRESERVE-01 | **Violated** | 영수증의 직렬화/write/flush/fsync/close 실패 및 intent 유지 재현. 재조립 공급 파일은 닫힌 전이 밖 — OH-1 |
| PO-ENV-01 | **Satisfied** | 정상·업무 실패의 환경 복원, 복원 실패의 명시 관측, 지원 진입 거부8개 재현. 확보된 항목별 복원 구조가 원결과 소거를 막음 |
| PO-RESOURCE-01 | **Violated** | 역할 해석·sandbox 우선순위는 확인. 포착되지 않은 환경 flush 실패가 후속 자료 `mismatch`로 대체됨 — OH-1 |
| PO-ISOLATE-01 | **Satisfied** | 보호 집합 선검사·목적지 경계·링크 거부 구조와 기존 음성 증거 확인. OH-1의 쓰기는 허가된 sandbox 내부이며 원본 침범 반례는 아님 |
| PO-SEMANTIC-01 | **Violated** | B 계수·좌석·발췌·봉투 정상 의미는 확인. 환경 실패를 자료 불일치로 투영하는 경로 잔존 — OH-1 |
| PO-GATE-01 | **Violated** | SITE68·격자56·기존165 연속성은 확인. 현재 helper의 허가 조건 무효화가 검사0 — OH-4 |

**진행도: `Satisfied=2 Violated=10 Unexamined=0`.**

보조 행 단위는 **`mismatch=9 unmet=9 unreviewed=0`**이다. 정적 도구의 출력 `0/0/0`과 구별한다. 여기서 mismatch는 종전과 같이 **대장에 적힌 의무와 실제 집행의 불일치**다.

- 남은 PO: EXEC·RESULT·FAIL·STATE·IO·PROFILE·PRESERVE·RESOURCE·SEMANTIC·GATE-01.
- 미충족 SITE: **03·10·11·32·37·38·39·46·56**.
- ⓑ **대장 누락 반례: 0**. 발견된 호출·자원은 기존 SITE에 배정돼 있다.
- 도출 누락0 · 새 보증 요구0 · 지적 전부 갈래⑴.
- 새 기준선과 T45 ③ 카운터 확정은 총괄의 몫이다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 이유 |
|---|---|---|
| ① 도출의 완전성 | **성립** | 발견한 모든 반례를 기존 I/PO로 분류할 수 있다. 상류 의무의 새 종류를 요구하지 않는다 |
| ② 신뢰·입력·부작용 경계 | **불성립** | 자원 실패 관측과 profile 입장 경계 결손 |
| ③ 기제의 집행과 합성 | **불성립** | 파일 소멸자 실패·raw_post 재파싱이 공통 구조를 빠져나감 |
| ④ 검증 근거 | **불성립** | FI 재현과 정상 호환 증거는 있으나, 실패 생명주기와 생산 helper의 조건을 덮지 못함 |
| ⑤ 미충족·불명확 처분 | **불성립** | 환경 실패가 후속 자료 `mismatch`로 바뀔 수 있음 |

`.incomplete`·IO-clear·legacy4/current5 자체가 **여섯 번째 처분을 만든 반례는 없다**. intent는 준비·소비를 차단하는 내부 상태이고, 기존 구동14·검수 부적격4·사람 복구 절차에 연결된다. 문제는 처분 종류의 추가보다 기존 처분을 잘못 선택하는 경로다.

**A 폐쇄표 — MY~OG**

`closed`는 기존 지정 반례의 폐쇄를 뜻한다. 신규 OH 경로까지 자동 면제하지 않는다.

| 기존 지적 | 상태 |
|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed 유지 |
| NU-1~4·NV-1~3·NW-1~5·NX-1~4·NY-1~4 | closed 유지 |
| NZ-1·2·4·5 / NZ-3 | closed / **partially — OH-1 처분 합성** |
| OA-1·2·4·5 / OA-3 | closed / **partially — OH-1 환경 실패 경계** |
| OB-1~4·OC-1·2·4·5·OD-1~5 | closed 유지 |
| OC-3 | **closed** — child별 IO gate 뒤 파싱 |
| OE-1·2·4·5 / OE-3 | closed / **partially — OH-2 후관측 합성** |
| OF-1 | **closed** — 종결 조회의 인자 전체가 lazy factory 안 |
| OF-2·3·5·6·7 / OF-4 | closed / **partially — OH-2 관측·보존 연결** |
| OG-1 | **partially** — 원결과·보존 선점은 개선됐으나 raw_post의 재파싱 잔여 |
| OG-2~5 | **closed** — child IO 순서·lazy 인자·공통 예외 처분·요청 형태 검사 |

**MY~OG: closed138 · partially5 · open0.** 직전 partially6 중 OC-3·OF-1은 닫혔고, NZ-3·OA-3·OE-3·OF-4는 잔여가 있다.

35차 미충족10행의 이동은 다음과 같다.

| SITE | 현재 | PO·회귀·FI 연결 |
|---|---|---|
| 40 | 닫힘 | IO/RESULT/ENV · S50 · FI-CHILD-IO |
| 46·56 | **잔여** | PRESERVE/RESULT/ENV · S49·S56·보존 FI는 확인했으나 OH-2 |
| 49 | 닫힘 | EXEC/ENV/ISOLATE · S42·S53 · 공통 driver 경계 |
| 50·51 | 닫힘 | STATE/SEMANTIC · S51 · 실제 `{}` 요청을 두 명령 모두 exit14로 재현 |
| 54 | 닫힘 | RESULT/PRESERVE · S49 · FI-DIAGNOSTIC·생성 바이트 지문 |
| 55 | 닫힘 | RESULT/ENV · S49 · observer 성공/실패 FI |
| 58 | 닫힘 | EXEC/STATE · S51 · FI-ARG |
| 65 | 닫힘 | IO/ENV · S49·S50 · IO-clear 뒤 후검출 |

기존10행 중 **8행 폐쇄·2행 잔여**, 신규 미충족7행을 더해 현재9행이다.

**검증 경로**

Python은 지정 인터프리터에 `PYTHONDONTWRITEBYTECODE=1`·`-B`를 적용했다. 메모리 시험은 표준입력으로 실행했으며 파일로 저장하지 않았다.

| 명령·경로 | 마지막 출력 또는 핵심 관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 지정 마커·`da846c3f…` 일치 |
| 지문표 전량 대조 | `matched=24 absent=25 mismatches=[]` |
| `t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `mismatch=0 unmet=0 unreviewed=0 grid=0` |
| `t40_structure.check('bundle')` | `STRUCTURAL checks=211 violations=0` |
| raw_post 허가 조건 메모리 변이 | `structural 0 mismatch 0 unmet 0 unreviewed 0` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차6파일만 · 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base→R1 / base→R2 대조 | 각각 `2 2 contracts/stages/read.yaml` |
| 핀 계약을 메모리 공급한 실제 `lane_profiles()` | `SEATS r0 True`, `r1 True`, `r2 True` |
| 지정 기준 런 CLI, `--law-tree` 없음 | 요구대로 **exit4 · 부적격** |
| 핀 법62파일 메모리 공급, 실제 `metrics(..., baseline=True)` | **complete · 총163 · component56 · environment=True** |
| FI 함수17 + 가상 파일시스템 적용12 | 합계29의 기존 기대 재현 · 실제 쓰기0 |
| 실제 지원 진입 거부·복원 | `checks=8/8` |
| 실제 `CASES()` ↔ compatibility baseline | **165개 metadata 전체 동일**, registry 동일, 총174 |
| 회귀표 판독 | **174행 · PASS174 · FAIL0** |
| SITE·격자 역사 대조 | 원 행68 보존 · historical56칸 동일 |
| §5′.10 바이트 대조 | 동일 · sha16 `33598684cfd07c2a` |
| 발췌기 import·출력 메모리 대역 | 27단위 · 표본10 · CL-2·4·7·9·12·14·16·19·21·24 |
| 봉투 `--write` 없는 미리보기 → 실제 러너 검증기 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 최종 HEAD·tracked diff·캐시/코어 검색 | HEAD 유지 · diff 빈 출력 · 해당 생성물 없음 |

기존165 보존은 **ID 존재만 확인한 것이 아니다**. 부류·부모·기대·근거를 포함한 metadata가 동일했다. 다만 구판의 실제 관측열 전체와 신판 관측열의 바이트 동일성을 독립 확인한 것은 아니다.

자문 §8의 명목13지점은 모두 FI에 연결된다. 직렬화·write·flush/fsync/close는 실제 영수증 writer를 메모리 파일 대역으로 실행했다. 그러나 재조립의 임시 파일 소멸자와 진단 실패 후 raw_post 합성은 해당 FI 경로에 포함되지 않았고, 이번 반례로 드러났다.

**[미검증]**

- 디스크 회귀174건과 R0/R1/R2의 실제 legacy/current 재조립 실행쌍은 재실행하지 않았다. 하네스·기대·표·동치 JSON을 대조했다.
- 생산 실측, `replay()` 실효과 실행, 구동기 디스크 쓰기 명령, Workflow 모델 호출은 실행하지 않았다.
- 미동봉 저작 보조25파일과 PO가 가리키는 미동봉 실행 로그의 지문은 검증하지 못했다.
- 봉투·발췌의 현행 규칙·서식은 검증했지만, 이관 전 생산 스크립트 전체와의 바이트/AST 동치는 독립 확인하지 못했다.
- 초기 가상FS 대역은 `lstat` 미구현으로 실패하고 종료139를 냈다. 대역을 수정한 재실행은12건 모두 성공했다. 그 중간 실패는 생산 결함으로 계산하지 않았다.
- 실제 디스크 장애의 종단 결과, 외부 스테이징 실물, 실호출 model/effort 증거, Owner 정성 판정은 이번 검증 결과가 아니다.

**읽은 파일**

상류는 T40·T42~T47 재정, 자문5회차 발주문 전문, D-02 §17 추기54~59, 35차 감수의 지적·폐쇄표·검증·소견을 읽었다. 설계·증거는 R8-REPORT·ARCHITECTURE, v38 지정 절과 v37 대조 절, PO12, SITE68·SITE→PO·격자, 회귀표174, R8 fault/compat/profile/static/immutability/final JSON과 해당 시험 코드를 확인했다.

코드는 flow→consume→drive→replay/metrics→receipts/resources→structure/sites→envelope/excerpts 순으로 읽었다. 법·실물은 SPEC 지정 G 항목, read/run-kinds·봉투/수렴 계약, read·paths·gitpin·lane plan의 관련 함수, 기준 런 원천·명세·판정서·요청/응답·포인터·원장을 대조했다. 정본 리포의 프로젝트 파일은 읽지 않았고 허용된 인터프리터를 사용했다.

**소견**

이번 반례는 새 규칙을 요구하지 않는다. 그 점에서 자문5회차가 요구한 **분류 체계의 폐쇄**에는 전진이 있다. 그러나 실행 경계의 이름을 공유하는 것과 파일 생명주기·파싱 허가·profile 완료 증표를 실제로 공유하는 것은 아직 다르다.

다음 수리는 새 예외 목록보다 **모든 파일 효과의 명시적 종료, IO-clear 증표의 끝까지 전달, profile 상태표의 생산·소비 공동 집행**으로 설명돼야 한다. 현재 관측은 “불변식 집합은 반례를 수용하지만 구현과 증거는 아직 그 집합을 만족하지 못한다”이다. 이는 게이트 관측이며 재정이 아니다. **PASS 전 실측 착수 금지는 유지된다.**