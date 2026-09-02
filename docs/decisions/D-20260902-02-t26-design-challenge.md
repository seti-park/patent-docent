# D-20260902-02 — 재정 T26 집행 설계의 M1b 설계 도전 — 판정 FAIL 의 처분과 상신

**지위.** 총괄 문서(원장 아님) · **감수 처분 + 상신 3건**(§3 ★) + 발주문 골격 개정(§5). 원장 = `ruling-20260902-01-T24-T27.md` §T26.

**선행.** 라운드 A 집행 `aa9a734` · 총괄 저작 설계 메모 `T26-DESIGN.md`(세션 스크래치 · 23,295 B · **리포에 없다** — PASS 를 받은 판만 라운드 B 발주문의 첨부로 들어온다).

**감수 원문** = `docs/lessons/2026-09-02-sol-challenge-t26-design.md`(전문 보존 · 규율 10). 좌석 = sol xhigh(ROUTING M1b) · 읽기 전용 · 약 20분. **판정 = FAIL · 지적 7건(BLOCKER 4 · HIGH 2 · MED 1).** 재정 T26 §3 ① 에 따라 **라운드 B 착수·커밋 금지 상태**다.

---

## §1 무엇이 틀렸나 — 한 화면

도전자의 첫 문장이 요지다 — *「출구 판정에 실제로 들어오는 12개 검사만 모델링하면 새 격자는 현행과 동일했습니다. 그러나 설계의 전수 시험은 그중 9개만 검사하고, P-4와 충돌하는 α를 채택하며, 원장이 명한 재시도 집합의 정확한 등식을 `phases` 교집합으로 약화합니다.」*

셋으로 갈라 읽는다.

| 무리 | 지적 | 성질 |
|---|---|---|
| **상류 충돌 — 총괄이 정할 수 없다** | B-1(α/β · P-4) · B-2 뒷절반(`read.input-digest` 가 「오늘의 표」의 영역인가) · B-6 앞절반(「각 행에 `checks`」의 범위) | **재정 상신**(§3) |
| **설계 오류 — 총괄이 고친다** | B-2 앞절반(분모 9 → 12) · B-3(오라클이 개정 계약을 공유) · B-4(`phases` 교집합) · B-5(런타임 선택기 fail-closed 아님) · B-6 뒷절반(`upstream-defect` 호출자 없음) · B-7(수용 기준 불완전) | **수용 → 설계 v2**(§2) |
| **총괄 자기 신고 7개 공격 지점의 판정** | 맞다 3(§5-1 · §5-6 · §5-7) · 틀렸다 3(§5-3 · §5-4 · §5-5) · 재정 필요 1(§5-2) | §4 자기 계상 |

**총괄이 검증한 것** — 도전자의 좌표 전건을 정본에서 다시 열었다: P-4 원문(`ruling-20260818-03-P1-P11.md:38` — *「retry(1)→escalate 경로를 조기 지점으로 이동」*) · `read.yaml:700-706`(convergence 행 `points: [early]` + *「접지 지출 이후로 미루지 않는다(재정 P-4)」*) · SPEC `:492` · T16 `:39`(청구항 검사 2종만) · T2(`ruling-20260831-05-T2-T6.md:30` — 재요리 경로 PD-M5 이연) · `READ_CHECK_IDS` 10 + `ENGINE_READ_CHECK_IDS` 2 = 출구 12 · 진입 `read.input-digest` 1 = 선언 13. **전부 도전자가 말한 대로다.**

---

## §2 처분표 — B-1 ~ B-7

| id | 격 | 무엇 | 처분 | 사유 | 포인터 |
|---|---|---|---|---|---|
| **B-1** | BLOCKER | 설계 §2.3 의 **α**(`read.convergence` 출구 재시도 허용)는 P-4 원문(*「retry(1)→escalate 경로를 조기 지점으로 이동」*)·계약 note·SPEC 과 맞지 않는다. 현행 러너가 모든 출구 실패를 재시도하는 것은 α 의 근거가 아니라 **P-4 위반 실물**. 그러나 β 로 고치면 재시도 횟수·(같은 서명 재현 시) 라벨이 바뀌어 T26 §3 ② 「오늘의 표 불변」과 충돌 | **이연 → 재정 상신** | 상류 두 재정(P-4 · T26 §3 ②)이 충돌하는 자리 — 총괄이 어느 쪽을 접어도 재정 침범. 선택지·추천 = §3 ★1 | §3 ★1 |
| **B-2** | BLOCKER | 설계 S1 전수 시험의 분모가 9 — 출구 `_failure_verdict` 에 들어올 수 있는 검사는 **12**(`READ_CHECK_IDS` 10 + 레인 로그 2). 12 로 8,190칸 대조 시 불일치 0(도전자 실측). 진입 `read.input-digest` 까지 13 으로 잡으면 2,048칸이 달라진다(현행 verbatim 폴백 `(escalate, None)` vs 새 격자 `(halt, "환경 오류")`) | **부분 수용** — 앞절반 수용 · 뒷절반 재정 상신 | 앞절반(분모 12 · 8,190칸 전수 · 총괄이 `read.source-digest` 와 레인 로그 2종을 빠뜨렸다)은 설계 오류 → v2. 뒷절반(「오늘의 표」의 영역에 진입 검사가 드는가)은 T26 §3 ② 의 해석 = 재정 → §3 ★2 | v2 §2.6 · §3 ★2 |
| **B-3** | BLOCKER | 구 구현 복제 오라클과 새 구현이 **같은 개정 계약**에서 `action`·`then`·`reason_label` 을 읽어 오늘의 값을 고정하지 못한다(`read.schema.then` 을 바꾸면 둘이 함께 바뀌어 S1 은 계속 green) — CLAUDE.md 가 경고한 「시험과 구현이 같은 기대값을 읽는」 형태 | **수용** | 검증 설계 원리 위반 — 총괄이 §5-4 에서 스스로 의심하고도 「제어 흐름이 다르니 된다」고 판단했다. v2 = **기준 커밋 골든 동결**: 공식 검사 id 목록 · 비공집합 × repeated 전건의 `(action, reason_label)` · 기준 커밋 해시 · 생성 절차를 픽스처 파일로 리포에 넣고, 시험은 그 파일만 읽는다. ★ 기준 커밋 = **라운드 A′ 뒤 커밋**(A-3 수리로 `{schema, source-digest}` 즉시 탈출이 실물이 된 뒤) — 라운드 A 감사가 경고한 「회귀 vs 의도된 교정」 충돌을 이렇게 피한다 | v2 §2.6 |
| **B-4** | BLOCKER | `phases` 교집합은 원장 ⒜ ③ 의 등식(판정점 checks == 그 판정점을 신고한 `retry(n)` 행들의 checks 합집합)을 약화 — 행이 실제로는 적용되지 않는 판정점을 신고해도 관문이 통과 | **수용** | 원장 등식을 바꾸는 것은 허용되지 않는다. v2 = 통합 행을 **판정점 기준으로 분리**(`claim-inventory`·`dependency-parse` → `points: [early, exit]` · verbatim 계열 5종 → `[exit]` · schema → `[exit]` · convergence → B-1 재정에 따라 `[early]` 또는 `[early, exit]`) · 관문은 교집합 없이 원장 식 그대로 · `phase` 는 「그 판정점에서 실제 실행되는가」만 별도 검증. 행 분리는 (조치, 라벨) 표를 바꾸지 않는다 — 골든(B-3)이 그것을 증명한다 | v2 §2.1 · §2.5 |
| **B-5** | HIGH | 관문은 `then` 없는 `retry(n)` 을 거부하지만 런타임 선택기는 fail-closed 가 아니다 — `worst_status` 의 `order.get(status, 0)` 이 잘못된 terminal 을 0 으로 취급해 조용히 무시 | **수용** | 총괄이 §5-5 에서 관문만 보고 「닫혔다」고 판단했다. v2 = `terminal_action()` 이 `action: retry(n)` 에 유효 `then` 필수 · `then ∈ {halt, reject-upstream, escalate}` · `worst_status` 호출 **전** 검증 · 위반 시 `StageError` · 두 변조 시험 | v2 §2.4 |
| **B-6** | HIGH | 원장은 「각 행에 `checks`」를 명했는데 설계는 세 행(반복 · `gate-escalation` · `upstream-defect`)을 `kind` 예외로 둔다 — 원장 문언을 조용히 좁혔다. 또 `upstream-defect` 는 **수신 코드가 없고 T2 가 PD-M5 로 이연**한 경로인데 설계가 단독 조회·`runner_reads` 분류를 적어 coder 가 T2 위반 또는 거짓 선언 중 하나를 고르게 된다 | **부분 수용** — 뒷절반 수용 · 앞절반 해석 상신 | 뒷절반: v2 = upstream 행에 **식별 키만** · 호출자 만들지 않음 명시 · binding `deferred/test_bound`. 앞절반: 「`checks` 의무는 검사 실패 행에만, 세 행은 `kind`」 는 원장 문언의 해석이라 **Owner 확인** → §3 ★3 | v2 §2.1 · §3 ★3 |
| **B-7** | MED | S2 가 신설 관문만 plain·`-O` — 원장 §3 ⑤ 는 전수 시험 + 관문 전종 | **수용** | v2 수용 기준 = 전수 pytest(plain · `PYTHONOPTIMIZE=1`) · 기존 5 + 신설 1 관문 plain · 같은 6 관문 `-O` · 각 명령과 기대 exit | v2 §2.6 |

**닫힘의 판정자** — 이 처분표는 총괄의 것이고 닫힘은 **재도전 PASS** 가 정한다(§3 ① 은 조건부 PASS 를 두지 않는다). v2 는 재정 3건이 나기 전에는 확정할 수 없다 — α/β 가 계약 행(`points`)·재시도 목록·골든의 값을 정한다.

---

## §3 ★ 상신 3건 — Owner 재정이 필요한 자리

### ★1 B-1 — `read.convergence` 의 출구 재시도 (α / β)

**무엇이 문제인가.** 재정 P-4(2026-08-18)는 수렴 검사의 `retry(1)→escalate` 경로를 **조기 지점으로 옮겼다**(*「접지 지출 이후로 미루지 않는다」*). 계약도 그렇게 적혀 있다(`read.yaml:702` `points: [early]`). 그런데 **오늘의 러너는 출구 실패를 종류 불문 재시도**하므로 출구에서 convergence 가 실패하면(조기에 통과한 뒤 출구 재검사에서 갈리는 경우) 꼬리 레인을 한 번 더 돌린다 — 계약이 `[early]` 만 신고한 행을 출구에서도 재시도하는 **P-4 위반 실물**이다. T26 ⒜ ③ 이 재시도 목록을 명시적으로 적게 만들면 이 자리를 **어느 쪽으로든 결정**해야 한다.

| | **α — 출구 재시도 허용** | **β — P-4 대로 출구 재시도 없음 (총괄 추천)** |
|---|---|---|
| 뜻 | 계약 행을 `points: [early, exit]` 로 넓히고 P-4 를 개정(「조기 지점으로 이동」 → 「조기 지점 추가」) | 계약 `[early]` 유지 · 출구 재시도 목록에서 convergence 제외 · 출구 convergence 실패 = 즉시 `escalate` |
| 오늘의 행동 | **불변**(러너가 이미 이렇게 돈다) | **바뀐다** — 출구 convergence 단독 실패 시 재디스패치 1회가 사라지고 바로 상신. 같은 서명 재현 라벨(「국면 간 변이 재현」)이 이 경로에서는 안 나온다 |
| 상류 | P-4 개정 필요(재정) | P-4 유지 · **T26 §3 ② 「오늘의 표 불변」에 명시 예외 1칸**(재정) |
| 비용 | 원장 개정 1건 + 골든 그대로 | 골든에 예외 1칸 표기 + 시험 1건(출구 convergence 실패 → 재디스패치 0회) |
| 논리 | 조기에 통과한 수렴이 출구에서 깨졌다면 꼬리 레인(접지·통합)이 명세를 바꾼 것 — 재시도가 고칠 수 있다는 가정 | 조기 통과 뒤 출구에서 깨진 수렴은 **비정상 신호**이고 P-4 의 취지(접지 지출 뒤에 재시도 비용을 더 쓰지 않는다)가 정확히 이 자리를 겨눴다. 사람이 봐야 한다 |

**총괄 추천 = β.** 사유 셋 — ⑴ Owner 가 이미 P-4 로 정했고 계약·SPEC 이 그렇게 적혀 있다. 지켜지지 않은 것은 코드다 — 코드를 원장에 맞추는 쪽이 원장을 코드에 맞추는 쪽보다 이 리포의 규율(원장이 상류)에 맞는다 ⑵ 출구 convergence 실패는 실런 3건에 전례가 없고 이론상 「조기 통과 → 출구 실패」는 정본 실행 하나만 남은 뒤라 peer 와의 비교 자체가 조기 값의 재사용이다 — 재시도로 달라질 것이 없다 ⑶ α 는 P-4 개정이라 재정 문언을 고치는 일이고 β 는 예외 1칸 표기다 — 비용이 작다. **단 β 는 오늘의 행동을 바꾸므로 T26 §3 ② 의 예외를 Owner 가 명시해야 한다.** 그 예외 문언 제안: *「T26 골든에서 `read.convergence` 가 출구 실패 집합에 든 칸의 재시도 여부는 P-4 의 이행이며 회귀가 아니다 — (조치, 라벨) 은 불변이고 재시도 횟수만 0 이 된다」*.

### ★2 B-2 뒷절반 — 「오늘의 표」의 영역에 `read.input-digest` 가 드는가

**무엇이 문제인가.** T26 §3 ② 는 *「오늘의 판정표 불변 증명」* 을 명했다. `_failure_entry_for` 는 함수라 `{read.input-digest}` 를 넣으면 답을 낸다(verbatim 폴백 → `escalate`). 그러나 **그 입력은 도달 불능**이다 — 진입 지문 실패는 `verify_declared_inputs` 가 진입에서 잡아 halt 하고 출구 함수에 오지 않는다. 새 격자는 이 검사에 전용 `halt · 환경 오류` 행을 둔다(T27 §1 의 sol 지적 4b 처분). **관측 가능한 행동은 오늘도 내일도 halt** 로 같고, 함수 수준의 답만 `escalate → halt` 로 바뀐다.

| | **ⓐ 영역 = 출구 12 검사 (총괄 추천)** | **ⓑ 영역 = 선언 13 검사 전부** |
|---|---|---|
| 뜻 | 골든은 8,190칸(2¹²−1 × 2). `read.input-digest` 는 진입 예외 경로로 **별도 반증**(진입 실패 → halt · 출구 함수 미도달) | 골든 16,382칸. 2,048칸이 달라지므로 T26 은 **값 공간 변경**이 되어 새 재정 없이 진행 불가 |
| 근거 | 「표」는 판정이 실제로 일어나는 자리의 표다. 도달 불능 입력의 함수값은 행동이 아니다 | 원장 문언 「전수」의 문자 그대로 |
| 비용 | 진입 경로 시험 1건 추가 | T26 재정 개정 + 골든 2배 |

**총괄 추천 = ⓐ.** 그리고 격자에서 `read.input-digest` 행이 서는 것은 T27 §1 이 「사유 없이 사라졌다」고 적은 sol 지적 4b 의 처분(**수용**)이므로, ⓐ 는 그 처분과 정합한다.

### ★3 B-6 앞절반 — 「각 행에 `checks`」의 범위

원장 ⒜ ① *「행에 검사 id 를 키로 단다 — 각 행에 `checks: [...]` 명시 키」*. 실패표에는 검사 실패가 아닌 행이 셋 있다 — 「같은 실패 서명 재현」(반복) · `gate-escalation`(조기 국면 게이트 상신) · `upstream-defect`(하류 반려 수신 · 호출자 없음 · T2 PD-M5). 이 셋에 `checks` 를 달 수 없다(검사가 아니다).

| | **ⓐ `checks` 는 검사 실패 행에만 · 세 행은 `kind: <식별자>` (총괄 추천)** | **ⓑ 세 행도 `checks` 를 단다(빈 목록 또는 가상 id)** |
|---|---|---|
| 뜻 | 원장 문언을 「검사 실패 행」으로 읽고 나머지 셋은 별 키. 관문 ⒜ 는 `checks` 행만 대조 · `kind` 행은 「검사 없는 행」 심기와 구별 | 문자 그대로. `checks: []` 는 관문 ⒜ 의 「검사 없는 행」 심기와 구별 불가 → 관문 약화 |
| 비용 | 원장 해석 1줄 기록 | 관문 설계가 자기모순 |

**총괄 추천 = ⓐ.** 도전자도 *「`kind` 라는 키 자체는 공학적 해법이 될 수 있다」* 고 했고 요구한 것은 **명시**다.

### 함께 걸린 상신(다른 문서) — `D-20260902-01-round-a.md` §4 ★(CP1 에 조기 합집합을 그릴지) · §6-5(A-2 범위 표지 사후 확인 · A-7 `canonical_selection.read_run` enum 구속).

---

## §4 총괄 자기 계상

| # | 무엇 | 왜 적나 |
|---|---|---|
| 1 | **분모를 셌는데 틀렸다**(9 vs 12). `READ_CHECK_IDS` 를 열어 보지 않고 기억으로 세었다 — `read.source-digest` 와 T22 가 직전 라운드에 만든 레인 로그 행 2 종을 빠뜨렸다 | 정본 실측 강제(발주문 필수 5항)를 **설계 메모에는** 적용하지 않았다. 설계도 발주문이다 |
| 2 | **오라클 공유 상수를 스스로 의심하고도 넘어갔다**(§5-4). 「제어 흐름이 다르다」는 답은 「값의 정본이 다르다」가 아니다 | 검증 설계 원리의 문장을 알고도 그 적용을 자기 설계에서 면제했다. **골든은 기준 커밋에서 동결하고 시험은 파일만 읽는다** — 이 리포가 rc-0004/0005 에서 이미 한 방식 |
| 3 | **α 를 골랐다** — P-4 원문을 읽지 않고 T16 의 출구 존치 결정(청구항 검사 2종)을 convergence 에 유추 적용했다 | 상류 원문 미독 → 재정 상신 대신 재량 선택. 결과적으로 설계 도전이 잡았으니 제도는 작동했다. **설계 도전 좌석의 값이 실측으로 하나 더 섰다** |
| 4 | **관문만 보고 런타임을 안 봤다**(B-5) · **호출자 없는 경로에 실행 의미를 적었다**(B-6) | 「선언과 실물의 어긋남」을 잡는 리포에서 총괄이 선언(`runner_reads`)을 먼저 적고 실물(수신 코드 없음 · T2 이연)을 뒤에 확인하지 않았다 |

---

## §5 발주문 골격 개정 — 이 라운드와 라운드 A 감사가 함께 요구한 것

두 감수(라운드 A 감사 A-1·A-3 · 이 도전 B-2·B-3)가 같은 결함 계열을 잡았다 — **총괄이 정본을 열지 않고 값을 적었다**. 발주문 필수 5항에 다음을 더한다(세션 기억 `delegation-criteria` · 리포는 여기가 기록):

- **⑹ 반증 시험의 변조는 「무엇이 읽는지」를 실측한 뒤 지정한다** — 변조 위치·문자열을 발주문이 정할 때, 그 변조가 판정 경로가 **실제로 읽는 구간**에 드는지를 코드로 확인하고 그 좌표를 발주문에 적는다. 양성 대조군(조건을 위반하면 시험이 실제로 빨개진다)을 성공 판정 기준에 넣는다(라운드 A A-1 · T19 §3 계열 2회 발생).
- **⑺ 원장 문언 ↔ 발주문 지정값 대조를 레인 보고 항목으로 명시한다** — 레인은 「실물과 어긋난 좌표」만 신고해 왔다. 원장 §3 집행 조건의 **양화사·범위 문언**(「하나라도」·「전수」·「정확히 같다」)이 발주문의 코드 문장으로 옮겨질 때 떨어지지 않았는지를 레인이 대조·신고한다(라운드 A A-3 · 이 도전 B-4).
- **⑻ 설계 메모도 발주문이다** — 정본 실측 강제(집합의 크기 · 검사 id 목록 · 호출자 존재)는 설계 메모에도 적용한다(B-2 · B-6).
- **⑼ 역프로브·변조 반증·되돌림이 있는 발주는 발주자가 만든 격리 사본(worktree 또는 `--no-hardlinks` 클론)에서만 돈다. 레인에 정본 트리 쓰기 권한을 주지 않는다** — 감수 레인의 규격(SPEC §8.3 9항 ⓐ · 재정 S5 · Q9 ⓐ)이 **저작 레인의 역프로브**에도 같은 이유로 적용된다: 되돌림 실패가 정본에 닿을 경로 자체를 없앤다. 레인 보고는 실행 트리의 경로를 적는다(발주문에 적히면 보고에 남고, 남으면 대조할 수 있다). **[추기 2026-09-02 · 총괄 저작]** 이 항은 라운드 C 병합 뒤 `S-1`(`opus-audit-t17-repair` §6 소견 ⑴)의 처분으로 더한 것이다 — `D-20260902-03-round-c.md` §3. 위 ⑹~⑻ 은 이 문서 작성 시점(도전 FAIL 직후)의 것이고 ⑼ 만 뒤에 왔다.

---

## §6 다음

1. Owner 재정 ★1·★2·★3 → 원장 등재(`ruling-20260902-02-T28…` · N6) → `RULINGS-LEDGER.md` §2. **[추기 2026-09-02]** 났다 — **T28 = β · T29 = ⓐ · T30 = ⓐ**(+ CP1 = T31 ⓐ · `canonical_selection.read_run` = T32 ⓐ) · 원장 등재 커밋 `b3144d5`.
2. 설계 v2 확정(§2 처분 + 재정 값) → **M1b 재도전**(sol xhigh · PASS 필요) → 라운드 B 발주(sol-coder) → opus max 감사(라운드 A′ 합본). **[추기 2026-09-02]** 재도전은 **FAIL(V-1~V-8 · §7)** 이었고, 같은 상신 2회 저항이라 **자문(fable xhigh · ROUTING ⑽ ⓑ)** 을 거쳤다 — **REVISE(N-1~N-7 · §8)**. v4 로 **3차 도전** 중.
3. 라운드 C(T27) 는 이 문서와 무관하게 진행 중 — 이 문서의 B-1~B-7 처분이 `DISPOSITIONS.md` 에 행으로 오른다.

---

## §7 2차 도전(설계 v2) 지적 V-1 ~ V-8 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v2.md`. 판정 FAIL · 8건 · **새 재정 사항 0**(도전자 자신이 「Owner 재정이 새로
필요한 자기 신고 항목은 없다」고 적었다). 값은 맞았고(8,190 칸 `MISMATCHES 0`) 집행 정밀도가 틀렸다. 여덟 건 전부 **수용** — 공학 수정이라
규율 11 ③ 재량이며 v3 에 반영했다.

| ID | 격 | 지적 요지 | 처분 | v3 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **V-1** | BLOCKER | T-1 의 `monkeypatch.setattr(m2, "run_read_checks", …)` — `m2` 는 `tests.test_m2_read` 모듈이라 러너(`engine.stages.read` 전역)에 닿지 않는다(실측 `PATCH_REACHES_RUNNER False`) | **수용** | T-1 대상 = `import engine.stages.read as read_stage` 후 `read_stage.run_read_checks` 전역 패치 · 원본 보존 · 출구 전용 호출 자리 :1743 명시 |
| **V-2** | BLOCKER | 골든 생성 명령이 `99fad78` 트리의 모듈을 import 한다는 보장이 없다(`cd <tmp>` 는 `sys.path` 를 바꾸지 않는다) | **수용** | 생성기 `--repo` 명시 인자 · `sys.path[0]` 삽입 뒤에만 import · **provenance 4검사**(read 모듈 경로 · run_checks 모듈 경로 · 계약 경로 · `git rev-parse HEAD`) 실패 시 파일 미작성 exit 1 · manifest `provenance` 블록 · 시험 ⑥ |
| **V-3** | HIGH | T-2 「`/retry-` 레인 1」 — 정본 후속 1회차는 레인 로그 **3행**(ground-independent · ground-dependent · synthesize) | **수용** | T-2 = `/retry-1/` 정확히 3 · task 집합 고정 · 「회차 1 / 행 3」 구별 · T-1 은 `/retry-` 0 |
| **V-4** | HIGH | G4 가 `phases: [exit, __ghost_phase__]` 를 통과시킨다(⊇ 한 방향만) | **수용** | R9 신설 — 모든 `checks_before_exit[].phases` list·비공·중복 없음·⊆ {early, exit} + 기존 ⊇ · 변조 ⒄ 추가 · 정본 12건 실물이 전부 ⊆ 임을 총괄 실측 |
| **V-5** | HIGH | 판정점 id 중복 처리 · `_retry_checks` 미지 id 우주(12/13) 미정 → M3 임의 선택 | **수용** | R8 신설 — 판정점 = 정확히 {early, exit} 각 1행(관문 G3 + 진입 가드 `RunnerContractError`) · 우주 = 출구 12 id · `read.input-digest`·중복 거부 · 변조 ⒅ · T-5/T-6 확장 |
| **V-6** | HIGH | manifest `predicate` 가 정수 mask 에 쓸 수 없는 표현(`TypeError`) | **수용** | `repeated == 1 and (mask & (1 << check_ids.index("read.convergence"))) != 0` 로 고정 · 생성기·T-7 이 같은 식을 `eval` · `cell_count` 2,048 |
| **V-7** | MED | 자기 신고 ④ 「T-11 이 종단 어휘 상등을 대조」는 사실이 아니다 | **수용** | T-11 ⑤ 신설 — `importlib` 로 관문 적재 · `TERMINAL_ACTIONS` 집합 == 엔진 상수 == {halt, reject-upstream, escalate} |
| **V-8** | MED | §2.2 손검산이 lane-log-only 3칸(`StageError`)을 누락 · 「격자 순 halt → escalate → reject」는 `worst_status` 순서(halt > reject-upstream > escalate)와 반대 | **수용** | 손검산에 3칸 예외 명시(mask 1024·2048·3072) · **격자 순서(ⓐ)와 동률 해소 순서(ⓑ)를 분리 서술** — 행 배열은 ⓑ 이며 ⓐ 를 따른 것이 아님을 적었다. 행 순서 자체는 바꾸지 않았다(값 불변 증명 유지) |

**자문 트리거.** 같은 상신(T26 설계)에 2번째 FAIL 이다 — ROUTING §5 ⑽ ⓑ. v3 은 자문(fable xhigh · 자료 인라인 단발)을 거친 뒤 3차
도전에 나간다. 자문 원문도 `docs/lessons/` 에 전문 보존한다.

**[정정 2026-09-02] §2 B-7 행의 「기존 5 + 신설 1 관문 · 같은 6 관문 `-O`」** 는 그 행을 쓴 시점(라운드 C 이전)의 계수다. 라운드 C(`852dcdd`)가
여섯째 관문 `check_dispositions.py` 를 세웠으므로 라운드 B 의 수락 기준은 **기존 6 + 신설 1 = 7 관문**(plain · `-O`)이다 — v2 §2.11 · v3 §2.11 이
그렇게 적는다. 구 문언은 지우지 않는다.


---

## §8 자문(fable xhigh · v3) 지적 N-1 ~ N-7 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-fable-advice-t26-design-v3.md`. 좌석 = ROUTING §5 ⑽ 자문(판정 + 논거 · 결정 없음) · 트리거 ⓑ(같은 상신 2회 저항).
판정 = **REVISE** · V-1~V-8 은 전부 `closed`(V-2·V-4 조건부) · 새 결함 7건(HIGH 3 · MED 3 · LOW 1) · **새 재정 사항 0**. 전부 **수용**(공학 수정 ·
규율 11 ③) — **v4** 에 반영하고, 자문의 말대로(*「N-1~N-7 을 반영한 v4 는 3차 도전에 그대로 내도 된다」*) 재자문 없이 3차 도전에 냈다.

| ID | 격 | 지적 요지 | 처분 | v4 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **N-1** | HIGH | 생성기가 `os.chdir(repo)` 뒤 상대 `--out` 을 쓰면 골든이 `$TMP` 에 떨어진다(99fad78 에 디렉터리가 없으면 쓰기 오류 · 있으면 worktree 제거가 거부) | **수용** | `out = realpath(--out)` 을 맨 먼저 고정 · `python -I` 실행 · provenance 요약에 절대경로 |
| **N-2** | HIGH | R9 의 전제(정본 12건 `phases` ⊆ {early, exit})를 설계가 스스로 재지 않았다 | **수용** | §1 「국면 실물」 행 — 12건 값 전부 실측 기재(전부 ⊆ · 전부 `exit` · `early` 셋 = early 목록과 일치) |
| **N-3** | HIGH | 생성기 저작 좌석·시점 부재 — sol-coder 가 B 에서 쓰면 골든이 B 앞에 존재할 수 없다(순환) | **수용** | **라운드 B-0**(`좌석 M3` sol-coder · 생성기 + 단위 시험) → 총괄 실행·골든 커밋 → 라운드 B. 총괄이 직접 쓰지 않는 이유 = 교차 벤더 감사 유지 |
| **N-4** | MED | T-4 의 피검 대상이 루프 인라인이라 도달 불능 집합을 함수 단위로 시험할 수 없다 | **수용** | `_exit_retry_eligible(contract, failing) -> bool` 헬퍼 · 루프가 그것을 부르고 T-4 가 그것을 시험 |
| **N-5** | MED | 계약 출구 id 집합 ↔ 엔진 상수의 양방향 다리 시험 좌표 없음 — `read.__ghost__` 를 `checks_before_exit` 에 더하고 행도 더하면 G1~G6 전부 통과 | **수용** | **T-12 신설** — `{checks_before_exit ids} == READ_CHECK_IDS ∪ ENGINE_READ_CHECK_IDS`(양방향) · `{checks_on_entry ids} == {read.input-digest}` · 각 판정점 `checks` ⊆ 출구 집합 |
| **N-6** | MED | R9 가 `phases` 거짓 양성(`read.source-digest` 에 `early`)을 안 잡는다 | **수용** | R9 확장 — `exit ∈ phases(id)` ∀12 · `early ∈ phases(id) ⇔ id ∈ points[early].checks` · 변조 ⒆⒇(20종) |
| **N-7** | LOW | ⓐ T-11 ④ 「결함 3종」 미지정 ⓑ T-9 grep 범위 ⓒ `_failure_verdict` 빈 후보 ⓓ T-2 retry-2 부재 ⓔ T-1 wrapper 치환 방식 | **수용** | ⓐ = 변조 ⑴⑽⒄ · ⓑ = `engine/` 의 `failure_row_of_kind(` 호출 리터럴 0(사전 상수는 호출 아님) · ⓒ = `select_failure_row([])` → StageError · ⓓ = `/retry-` 전부 3이고 전부 `/retry-1/` · ⓔ = `row.add(...)` 한 건(status 는 findings 유무의 속성) |

자문이 「실물 확인 필요」로 남긴 넷은 총괄이 실측해 v4 §1 에 적었다 — T-1 wrapper 치환(`CheckRow.status` 속성 · `add` 5인자) · `reader/__init__.py`
부재(네임스페이스 패키지 → provenance ⓔ `__path__` 단일성) · `dispatched_ids` 형태(`plan.py:295` `{read_run}/{task}/retry-{n}/batch-{b}`) · 12건 `phases`.

**규율 11 자기 점검(자문 §4 와 일치).** R8 · `_retry_checks` 우주 · 미지 id StageError · provenance 거부 · R9 = 전부 **공학**(정상 12 id 영역의
(조치, 라벨) 값은 한 칸도 안 바뀐다 · 정본이 R9 를 이미 만족함을 실측). B-0 좌석 선택은 ROUTING §5 「소규모 편집의 판정」(교차 벤더 필요 → 위임).


---

## §9 3차 도전(설계 v4) 지적 W-1 ~ W-4 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v4.md`. 판정 FAIL · 4건(BLOCKER 1 · HIGH 1 · MED 1 · LOW 1) · **새 재정 사항 0** ·
B-1~B-7 · V-1~V-8 · N-1~N-7 은 **전건 closed**(B-5 만 partially → W-2). 값 8,190 칸은 세 번째로 일치. 넷 전부 **수용** → **v5** → 4차 도전.

| ID | 격 | 지적 요지 | 처분 | v5 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **W-1** | BLOCKER | G3 는 exit 목록과 `points: [exit]` 행을 **서로** 비교할 뿐 승인된 8종과 대조하지 않는다 — exit 목록에서 `read.value-derivation` 을 빼고 9행을 나눠 그 검사만 비-retry `escalate` 행으로 두면 G1~G6 · T-12 · 골든 전부 통과하면서 실제 재디스패치 1→0(도전자 모형 `MUTANT_ACCEPTED True`) | **수용** | 엔진 상수 `EARLY_RETRY_CHECK_IDS`(3) · `EXIT_RETRY_CHECK_IDS`(8) + 진입 가드(계약 목록 ≠ 상수 → `RunnerContractError` · 디스패치 전) · 관문 G3 상수 `APPROVED_RETRY_CHECKS`(원장 T26 ⒜ ③ · T28 β · T25 좌표 주석) · T-11 ⑥ 두 상수 상등 · T-4 를 출구 12종 전부(True 8 · False 4) · T-5 에 동시 변조 · 자기 시험 ㉑. **규율 11 자기 점검** — 값을 아는 자리가 둘 더 생기지만 그 값은 원장이 이미 정한 것의 기록이다(G5 `halt` 와 같은 격 · v5 §4 ⑰) |
| **W-2** | HIGH | 조기 상신축 갈래가 `failure_row_of_kind(…, "gate-escalation")` 의 `action` 을 그대로 status 로 써서 `terminal_action()` 을 우회 — 그 행에 `then: halt` 나 미지 action 이 있으면 관문(G6)은 거부하지만 런타임은 흘린다 | **수용** | `_gate_escalation_verdict(contract)` = `terminal_action(entry), entry.get("reason_label")` — 세 갈래 전부가 `terminal_action()` 을 지난다 · T-8 에 함수 단위 변조(`then: halt` · `action: __bogus__` → `StageError`) + 상신축 러너 경로가 있으면 그것도 · 자기 시험 ㉔ |
| **W-3** | MED | `checks_on_entry`·`checks_before_exit` 선언 배열의 중복 미검사 — `read.schema` 선언 복제 시 13행/12 id 로 G2·R9·T-12 통과 | **수용** | G2 = 두 배열 각각 list · dict 행 · `id` 비공 문자열 · 중복 없음 · T-12 `len(ids) == len(set(ids))` · 자기 시험 ㉒㉓ |
| **W-4** | LOW | §2.10 「자기 시험 18종」 vs §2.7·§2.11 20종 | **수용** | 계수는 §2.7 표 한 자리에만(지금 24) · §2.10·§2.11 은 그 표를 가리키고 SPEC 산문에 수를 적지 않는다(T5 계열) |

**세 번째 FAIL 에 대한 총괄 자기 점검.** 세 판정의 지적 수는 7 → 8 → 4 이고 격의 무게는 내려간다(BLOCKER 4 → 2 → 1). 값(8,190 칸)은
세 번 다 일치했고 남는 것은 **검증 체계의 구멍**(우회 변조 · 우회 호출자 · 다중집합)이다. ROUTING ⑽ ⓑ 자문은 2차 뒤에 한 번 거쳤고
자문이 v4 를 「그대로 내도 된다」고 했으나 3차가 W-1 을 찾았다 — 자문도 도전자도 각각 다른 것을 보았고 둘 다 필요했다. 4차 도전은
W-1~W-4 폐쇄와 「v5 가 이전 지적을 다시 열었는가」만 보게 발주문을 좁혔다.


---

## §10 4차 도전(설계 v5) 지적 X-1 ~ X-3 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v5.md`. 판정 FAIL · 3건(BLOCKER 1 · HIGH 1 · MED 1) · **결정 공백 0 · 새 재정 사항 0** ·
W-1~W-4 · B · V · N 전건 closed. 값 8,190 칸은 네 번째 일치. 셋 전부 **수용** → **v6** → 5차 도전.

| ID | 격 | 지적 요지 | 처분 | v6 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **X-1** | BLOCKER | 관문이 `failure[]` 의 **행 분할**을 고정하지 않는다 — T22 §3 ① 이 명한 lane-log 두 전용 행을 `checks: [shape, digest-value]` 한 행으로 병합해도 R1·R2·G3~G6 전부 참이고 8,190칸 값도 같다(`MERGED_GRID_MISMATCHES 0`). 재량이 아니라 Owner 재정(T22)의 집행 누락 | **수용** | G1 = 관문 상수 `APPROVED_FAILURE_TABLE`(11행 · 순서 · `checks` 집합 또는 `kind` · action · then · reason_label · points · 각 행에 재정 좌표)과 **정확 일치**. `condition`·`note` 산문 둘만 자유. T-13(importlib 다리 · lane-log 두 id 가 서로 다른 singleton 행) · `test_m23` 개정 · 변조 ㉕(병합) ㉖(순서 교환) |
| **X-2** | HIGH | v5 T-1 이 `element-set` 에 finding 을 더하는데 그 축은 **escalation-trigger** 다 — 검사기는 그 축 미달에 finding 을 내지 않으므로 행 fail·축 전부 pass 의 자기모순 판정서가 되어 T28 §3 ③ 「실제 러너 경로에서 exact-match 실패」를 정직하게 실증하지 못한다 | **수용** | wrapper 가 `ctx.peer_spec` 사본에 독립항 하나를 복제한 `CheckContext` 로 원래 `run_read_checks` 를 부른다 → 검사기 자신이 `independent-count`(exact-match) fail + finding(도전자 실측 `COHERENT_EXACT_MATCH True`). 시험은 판정서 `axes[]` 의 `independent-count: fail` 기록까지 본다. 총괄 자기 신고 ⑩ 을 「틀렸다」로 정정 |
| **X-3** | MED | `upstream-defect` 행의 `reject-upstream` 이 관문·시험·골든 어디에도 고정되지 않아 `action: halt` 로 바꿔도 통과 — 호출자 0 이라 오늘 실동작은 안 바뀌지만 PD-M5 이연 처분의 **계약 변경**이며 허용한 재정이 없다 | **수용** | X-1 의 골격 고정이 kind 행 셋의 action·then·label 을 함께 덮는다 · 변조 ㉗(`halt`) ㉘(`gate-escalation` 라벨 삭제) |

**네 번째 FAIL 에 대한 총괄 자기 점검.** 값은 네 번 다 맞았고 지적은 7 → 8 → 4 → 3 이며 이번 셋은 전부 **「관문이 무엇을 고정하지 않는가」**
한 계열이다(행 분할 · kind action · 주입 축의 진실성). v6 은 그 계열을 한 번에 닫는 형태 — **승인 실패표의 기계 필드 전체를 관문 상수로**
— 를 택했다. 대가 = 관문이 계약의 사본을 든다. 그것이 「같은 상수」 함정인가를 v6 §4 ⑲ 에 자기 신고했다: 함정은 시험이 **구현**의 상수를
복사해 구현 변화를 따라가는 것이고, 여기 상수는 **원장값**이며 계약이 그것을 따라와야 한다 — 방향이 반대다. 도전자가 이 논거를 치라.
또 하나 — 4차 발주문은 「tools 불변」이라 적었으나 그 시각 라운드 C′ 레인이 `tools/check_dispositions.py` 를 고치고 있었고 총괄이 도전 중
병합했다(총괄 귀책 · 도전자가 정직하게 적었다). 5차 발주문은 그 사실을 고지했다.


---

## §11 5차 도전(설계 v6) 지적 Y-1 ~ Y-5 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v6.md`. 판정 FAIL · 5건(HIGH 1 · MED 2 · LOW 2 · **BLOCKER 0**) · 새 재정 0 · X-1·X-3 closed ·
X-2 partially(Y-1) · B·V·N·W 전건 closed(W-4 만 Y-4 로 재개방). 값 8,190 칸은 다섯 번째 일치. 다섯 전부 **수용** → **v7** → 6차 도전.

| ID | 격 | 지적 요지 | 처분 | v7 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **Y-1** | HIGH | T-1 안에 폐기된 v5 지시(「`original(ctx)` 뒤 `element-set` finding 수동 추가」)와 v6 의 새 지시(peer 독립항 복제)가 공존 — M3 가 앞 문장을 구현하면 X-2 의 자기모순 판정서가 재현 | **수용** | T-1 행을 지우고 **한 절차**(①~④)만으로 다시 썼다. 총괄 귀책 — v6 패치가 「치환 방식」 문장만 갈고 앞의 주입 문장을 남겼다 |
| **Y-2** | MED | `test_m21` :533/:733 을 둘 다 `retry-repeat` 조회로 바꾸라 했는데 :533 은 **원천 다이제스트 행**(`"원천 다이제스트" in condition`) 시험 — 그대로면 기대 라벨이 어긋나 시험이 깨진다 | **수용** | :533 → `failure_rows_for_checks(contract, {"read.source-digest"})` 정확히 1행 · :733 → `failure_row_of_kind(contract, "retry-repeat")` 로 분리 · §1 좌표표도 같이 정정 |
| **Y-3** | MED | G1~G6 이 `retry_budget.points[].max_retries` 를 보지 않는다 — `early.max_retries: 1→2` 가 관문 관측면 불변으로 통과(도전자 실측 `runtime_budget_changed=True`). 존치 `test_m17_lanes.py:164` points_binding 이 잡으므로 수락 체계 전체의 구멍은 아니지만 G3 가 재시도 결속을 주장한다 | **수용** | G3 — 각 판정점 p: `{n : action == retry(n) ∧ p ∈ points}` == `{max_retries(p)}` · 변조 ㉙ `early.max_retries: 2` |
| **Y-4** | LOW | W-4(계수 충돌)가 재발 — §0·§2.11 「28종」 · §2.10 「지금 24」 · 「§2.7 한 곳만 정본」 선언을 스스로 위반 | **수용** | 계수 리터럴을 **전부** 걷어냈다. §2.7 열거만 정본 · 수락 문언은 「§2.7 열거 전건 · 관문 출력이 세는 수」. 총괄 귀책(두 번째) |
| **Y-5** | LOW | T-12 의 「유령 id + 유령 행은 이 시험만 잡는다」는 v6 에서 거짓 — G1 골격 정확 일치가 먼저 잡는다. T-12 자체(계약↔엔진 상수 다리)는 유효·필요 | **수용** | 목적 문언을 「관문 YAML 오라클과 **독립적인** 계약↔엔진 상수 다리」로 정정 |

**다섯 번째 FAIL 에 대한 총괄 자기 점검.** BLOCKER 가 처음으로 0 이다. 다섯 중 둘(Y-1 · Y-4)은 **패치식 개정의 잔재**이고 그것이 두 판 연속으로
났다(v5 W-4 → v6 Y-4 · v6 X-2 정정 → Y-1). 대책 = v7 은 개정 뒤 **모순 탐색 grep**(폐기 문구 `original(ctx)` · 계수 리터럴 · 좌표 매핑 `:533/:733`)을
돌려 잔재 0 을 확인한 뒤 냈다(대응표의 인용은 예외). Y-3 은 관문이 「주장하는 범위」와 「실제로 보는 것」의 어긋남 — 이 리포의 지배적 결함 계열
(「강제의 범위를 실제보다 넓게 말했다」)이며 관문 설계 문서에서도 같은 형태로 났다.


---

## §12 6차 도전(설계 v7) 지적 Z-1 · Z-2 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v7.md`. 판정 FAIL · 2건(MED 2 · BLOCKER 0 · HIGH 0) · 새 재정 0 · Y-1·Y-2·Y-4·Y-5 closed ·
Y-3 partially(Z-1) · B·V·N·W·X 전건 closed. 값 8,190 칸은 여섯 번째 일치. 둘 다 **수용** → **v8** → 7차 도전.

| ID | 격 | 지적 요지 | 처분 | v8 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **Z-1** | MED | G3 의 Y-3 보수가 값의 집합 등식만 적고 `max_retries` 의 **타입**을 규정하지 않는다 — PyYAML `true`→bool · `1.0`→float 이고 `{1} == {True} == {1.0}` 이라 통과. 런타임 `_retry_budget()`(:754) 과 존치 `test_m17` 은 `type(v) is int` 로 거부하므로 관문·런타임의 계약 유효성 판정이 갈린다(도전자 실측 `bool_and_float_pass_literal_G3_set_equality=True runtime_rejects=True`) | **수용** | G3 — `type(p["max_retries"]) is int`(`isinstance` 금지 · bool 통과)를 등식 **앞**에 · 변조 ㉚ `true` ㉛ `1.0` · T-11 ④ 직접 YAML 변조에 ㉚ 포함(파서 실물 경로). 음수·0 은 현행 `_retry_budget` 도 통과시키므로 **손대지 않는다**(값 공간 = 재정 사항 — v8 §5 에 도전 대상으로 적음) |
| **Z-2** | MED | T-7 ④ 가 manifest 의 `predicate` 를 `eval` 해 **같은 manifest** 의 `cells` 와 비교 — predicate 와 cells 를 함께 틀리면(schema 비트) 2,048칸·자기일관으로 통과(`equals_required_beta=False symmetric_difference=2048`). `exceptions` 길이·`id`·`rule` 도 미대조 | **수용** | T-7 ④ — 기대 셀은 **시험 코드의 고정 식**(`read.convergence` 리터럴은 시험 코드에 · `check_ids` 순서만 manifest)으로 독립 산출 → manifest `cells` 와 양방향 · 2,048 · `len(exceptions) == 1` · `id == "T28-beta"` · `rule`·`predicate` 문자열 고정값 대조. manifest 의 `predicate` 는 **기록**으로 남는다. B-0 생성기 시험에 동반 변조(자기일관 사본이 통과하면 검사가 자기참조) 추가. 총괄 오라클도 β 집합을 독립 계산 |

**여섯 번째 FAIL 에 대한 총괄 자기 점검.** BLOCKER·HIGH 가 0 이고 남은 것은 **관문·시험이 「같은 것을 두 벌로」 보지 않은 자리** 둘 — 관문이 런타임과
다른 타입 판정(Z-1) · 시험이 피검물의 술어로 피검물을 검산(Z-2). 둘 다 이 리포의 검증 설계 원리([[verification-design-principles]] — 「시험과 구현이 같은
상수를 쓰면 전건 green 이어도 계약은 깨져 있다」)의 변형이다. 7차 발주문은 Z-1·Z-2 폐쇄와 재개방 여부만 묻는다.


---

## §13 7차 도전(설계 v8) 지적 AA-1 ~ AA-4 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v8.md`. 판정 FAIL · 4건(HIGH 2 · MED 2 · BLOCKER 0) · 새 재정 0 · Z-1 closed · Z-2 partially ·
그 밖 전건 closed. 값 8,190 칸은 일곱 번째 일치. 넷 전부 **골든 manifest 의 수락면(T-7)** — 한 계열이다. 넷 전부 **수용** → **v9** → 8차 도전.

| ID | 격 | 지적 요지 | 처분 | v9 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AA-1** | HIGH | T-7 ① 이 `check_ids` 를 양방향 **집합**으로만 대조 — `read.pointer-resolve` 자리를 둘째 `read.verbatim` 으로 바꾸고 13번째에 붙여도 값·계수·β 전부 통과(두 검사가 같은 9행) → T29 「12 정확히」 위반 | **수용** | 검증기 — `check_ids` list · 비공 str · **`len == len(set) == 12`** 뒤에 집합 상등 · 음성 시험 ⓐ |
| **AA-2** | HIGH | T-7 이 셀 **키 우주**를 고정하지 않음 — `1024:1` 삭제 + `0:1` 삽입(둘 다 StageError)이 총수·계수·값·β 전부 유지 · M3 가 manifest 키를 순회하면 통과 | **수용** | 검증기 — `cells` dict · **키 집합 == `{m:r : m∈1..4095, r∈{0,1}}` 양방향** · 값 형식(종단 어휘 + str|None 또는 `"StageError"`) · `exceptions[0].cells` list·str·중복 없음·정확히 2,048 · T-7 ② 는 정답 우주를 **시험이 생성해** 순회 · 음성 시험 ⓑ |
| **AA-3** | MED | T-7 ⑥ 이 `provenance.tree_head` 와 manifest 자신의 `base_commit` 접두 관계만 봄 — 둘을 현재 HEAD 로 함께 바꿔도 통과 | **수용** | 검증기 인자로 리터럴 `"99fad78"` 과 `git rev-parse 99fad78` **전체 해시**(`99fad78c318875af99aa87083c029d2c6724e240`)를 호출자가 넘긴다 · 음성 시험 ⓒ |
| **AA-4** | MED | Z-2 처분이 「B-0 시험에 동반 변조」를 명했으나 B-0 범위에 그 변조를 거부할 **피검 함수가 없다**(T-7 은 B 에서 생김) → M3 임의 선택 | **수용** | **`tests/fixtures/read-failure-grid/validate_manifest.py` 를 B-0 산출물로** — 순수 함수 · 엔진 무import · 형식·우주·β·provenance 전항. 호출자 셋 = 생성기(생성 직후 자기 검증 · 위반이면 파일 미작성 `EXIT=1`) · B-0 시험(변조 사본 ⓐ~ⓖ) · 라운드 B T-7(같은 검증기 + 런타임 값 대조) |

**일곱 번째 FAIL 에 대한 총괄 자기 점검.** 6차가 T-7 의 자기참조 하나(Z-2)를 지적했을 때 총괄은 **그 한 줄만** 고쳤고, 7차는 같은 수락면의 나머지
구멍 넷을 한 번에 냈다. 대책 = 지적 한 점이 아니라 **그 면 전체**를 닫는다 — manifest 의 모든 필드를 한 검증기가 형식·우주·계수·β·provenance 로
덮고, 그 검증기를 세 호출자가 공유한다. 같은 형태가 3·4차(관문이 고정하지 않은 것 → 승인 표 전체를 상수로)에서도 났다 — 「한 점을 고치면 옆 점이
난다」는 것이 이 도전 반복의 지배적 패턴이며 [[design-challenge-loop-lessons]] 에 적었다.


---

## §14 8차 도전(설계 v9) 지적 AB-1 · AB-2 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v9.md`. 판정 FAIL · 2건(MED 2 · BLOCKER·HIGH 0) · 새 재정 0 · AA-1~AA-3 closed · AA-4 partially ·
그 밖 전건 closed. 값 8,190 칸은 여덟 번째 일치. 둘 다 **수용** → **v10** → 9차 도전.

| ID | 격 | 지적 요지 | 처분 | v10 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AB-1** | MED | v9 검증기 목록이 manifest 의 **값**을 다 검사하지 않는다 — Z-2 처분이 명한 `exceptions.rule` 고정이 상세 목록에서 빠졌고(`rule`·`meaning` 변조가 통과) `$comment`·`cell_key`·`generator`·`generation_command` 는 존재만 · `expected_counts`·`cell_count` 에 `type is int` 없음 · `provenance` 내부 키 집합 미고정(도전자 실측 `unchecked_value_fields=[…6개]`) | **수용** | 최상위 10키 · `provenance` 8키 · `exceptions[0]` 6키 **전부**에 고정 리터럴 또는 형식(`rule`·`meaning`·`cell_key`·`generator`·`generation_command` 문자열 상등 · `$comment` 부분 문자열 3종 · 계수 `type is int` · `generated_at` ISO-8601) · 음성 시험 ⓗ(rule/meaning) ⓘ(`$comment`·`cell_key`·`generation_command`) ⓙ(float 계수 · provenance 여분 키) |
| **AB-2** | MED | `python -I` 는 스크립트 디렉터리·cwd 를 `sys.path` 에서 빼고 설계가 추가하는 경로는 `99fad78` 트리 루트뿐 — 형제 `validate_manifest.py` 는 그 트리에 없으므로 `import validate_manifest` 가 성립하지 않는다(도전자 실측 `sys_path=[stdlib, venv site-packages]`) → M3 가 `sys.path` 추가·`importlib`·로직 복제 중 임의 선택 | **수용** | 생성기·T-7 이 **`importlib.util.spec_from_file_location("validate_manifest", Path(__file__).with_name("validate_manifest.py"))`** 로 적재(설계에 코드 블록) · 검증기는 stdlib 만 import · B-0 시험이 공개 `python -I generate.py …` 명령을 **서브프로세스로** 실행해 `EXIT=0`·파일 생성·검증기 통과를 확인 |

**여덟 번째 FAIL 에 대한 총괄 자기 점검.** 7차 뒤 「면 전체를 닫는다」고 적고서 검증기 항목을 **키의 존재**까지만 적고 **값**을 빠뜨렸다 — 같은 면에서
한 겹 더 깊은 자리였다. 검증기 항목을 적을 때의 규칙 = 필드마다 **「무엇과 같아야 하는가」**(리터럴 · 형식 · 재계산)를 적고, 「있어야 한다」만 적은 필드가
하나라도 남으면 그것이 다음 지적이다. AB-2 는 `-I` 의 부작용을 V-2 처분에서 스스로 도입하고 그 결과를 형제 파일 적재에 적용하지 않은 것 — 한 결정의
파생 효과를 끝까지 따라가지 않았다. 9차 기동 직후 §6 의 낡은 열거(「ⓐ~ⓖ」)를 발견해 레인을 죽이고 재기동했다 — 그때 `pkill -f <패턴>` 이 총괄 자신의
셸을 잡아 명령이 중도 사망했다(LANE-RUNTIME 「함정 C」 · 패턴 매칭 대신 PID 를 잡아야 했다).


---

## §15 9차 도전(설계 v10) 지적 AC-1 ~ AC-5 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v10.md`. 판정 FAIL · 5건(MED 3 · LOW 2 · BLOCKER·HIGH 0) · 새 재정 0 · AB-1·AB-2 partially ·
그 밖 전건 closed. 값 8,190 칸은 아홉 번째 일치. **다섯 전부 문서 내부 정합** — 경로 하나 · 리터럴 둘 · 커밋 열거 · 참조 번호 · 좌표. 다섯 전부 **수용** → **v11** → 10차 도전.

| ID | 격 | 지적 요지 | 처분 | v11 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AC-1** | MED | 「생성기와 T-7 둘 다 `Path(__file__).with_name("validate_manifest.py")`」— T-7 의 `__file__` 은 `tests/test_m24_failure_grid_golden.py` 라 `tests/validate_manifest.py` 를 가리킨다(도전자 실측) → 필수 pytest 가 파일 부재로 실패 | **수용** | 호출자별 경로 — 생성기 `with_name` · T-7 과 B-0 시험 `Path(__file__).parent / "fixtures" / "read-failure-grid" / "validate_manifest.py"` · 각각 `is_file()` 선검사 · **B-0 시험 파일 위치를 `tests/test_m24a_failure_grid_generator.py` 로 고정**(선택지 제거)해 T-7 경로식이 B-0 에서 이미 실행된다 |
| **AC-2** | MED | `cell_key` 가 본문(`이 파일의`)과 manifest 예시(`**이 파일의**` — JSON 안의 `**` 는 문자)에서 다르고, `generation_command` 는 「네 줄」·「블록 그대로」·물리 6줄(논리 5명령)로 어긋남 → 정확 상등을 요구하면서 정답이 둘 | **수용** | `cell_key` 정본 = manifest 예시 하나(강조 제거 · 본문은 「예시와 바이트 동일」로 가리킴) · 생성 명령 블록을 **정확히 네 줄**(주석·빈 줄 없음)로 재작성하고 `generation_command` = 그 네 줄을 `\n` 으로 이은 문자열(끝 개행 없음) · 생성기·검증기 상수 두 벌의 상등은 B-0 시험이 대조 |
| **AC-3** | MED | 골든 커밋 열거가 「생성기 + 시험 + manifest」로 검증기를 빠뜨렸고, B-0 레인은 worktree 에서 커밋하지 않는데 그 산출을 main 으로 어떻게 올리는지 없음 → T-7 이 적재할 파일이 없거나 열거를 임의 확장 | **수용** | 순서 명시 — ① 레인 저작(worktree · 무커밋) ② 총괄 재현 → worktree 커밋 → main 리베이스 → ff = **B-0 병합 커밋**(생성기 + 검증기 + 시험 셋 · C′ 절차) ③ 총괄이 main 에서 생성 명령 → **골든 커밋**(manifest) ④ 라운드 B 는 골든 커밋에서 시작 — §2.8·§2.11·§6 세 자리를 같은 문장으로 |
| **AC-4** | LOW | T-7 이 「§2.8 ①~⑥」을 수행한다고 하나 §2.8 시험 목록은 ①~③ 이고 ④ 는 총괄 스크래치 검수 | **수용** | T-7 = §2.8 시험 ①~③ · ④ 는 골든 커밋 시 총괄 수락 단계로 분리 명시 |
| **AC-5** | LOW | `assemble_spec :505-556` 은 정의 :506 · 반환 :561 | **수용** | §1 좌표 `:506-561` |

**아홉 번째 FAIL 에 대한 총괄 자기 점검.** BLOCKER·HIGH 는 다섯 판 연속 0 이고 이번 다섯은 전부 **문서가 자기 자신과 어긋난 자리**다 — 같은 값을
두 곳에 적어 둔 것(리터럴 · 경로 · 열거 · 참조 번호)이 개정을 거치며 갈라졌다. Y-4 와 같은 계열이며 규모가 커진 문서(80 KB)에서 패치식 개정이 반복될 때
피할 수 없는 형태다. 대책 = **값은 한 자리에만** 두고 다른 자리는 그 자리를 가리킨다(계수에 적용한 규칙을 리터럴·경로·열거에도) · 개정 뒤 모순 탐색
grep 의 패턴 목록에 이번 다섯을 더했다.


---

## §16 10차 도전(설계 v11) 지적 AD-1 ~ AD-3 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v11.md`. 판정 FAIL · 3건(HIGH 1 · MED 2) · 새 재정 0 · AC-1~AC-5 closed · X-1·AB-1 은 AD 로 partially.
값 8,190 칸은 열 번째 일치. 셋 전부 **수용** → **v12** → 11차 도전.

| ID | 격 | 지적 요지 | 처분 | v12 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AD-1** | HIGH | 음성 시험 ⓗⓘⓙ 가 여러 필드를 **함께** 바꾸고 「위반 ≥ 1」만 요구 — `meaning` 검사를 빼도 `rule` 검사가 가리고, `generator` 검사를 통째로 빼면 열거된 모든 음성 시험을 그대로 통과. 「모든 값 필드 검사」 주장이 수락 시험으로 반증되지 않는다 | **수용** | 검증기 위반 문장 = `<필드 경로 토큰>: <설명>` · **표 T-V**(최상위 10키 · provenance 8키 · exceptions 6키 · cells 키/값 · check_ids 세 변조 — 한 필드씩) · 각 시험은 **그 토큰으로 시작하는 위반이 있다**를 검사 · B-0 시험과 라운드 B T-7 ③ 이 같은 표를 쓴다 |
| **AD-2** | MED | `APPROVED_FAILURE_TABLE` 열거 필드가 `checks/kind`·`action`·`then`·`reason_label`·`points` 뿐인데 3행에는 `judged_at: entry` 가 필수 — 열거 projection 만 비교하면 `unapproved_machine_field` 추가가 통과하고, 「산문 둘 외 전부」로 비교하면 `judged_at` 처리를 M3 가 만들어야 한다 | **수용** | 상수에 **`judged_at` 열**(3행 `"entry"` · 나머지 None) · **행별 실제 키 집합 == 승인 기계 키 ∪ {condition, note} 의 부분집합이면서 승인 기계 키 전부 포함** · 변조 ㉜(미지 키) ㉝(`judged_at` 이동) · T-13 동기 |
| **AD-3** | MED | 생성 명령 네 줄이 줄 사이 `&&` 도 `set -e` 도 없어 첫 줄 사전조건 실패 뒤에도 진행하고 마지막 `git worktree remove` 성공으로 rc 0 · 셋째 줄이 `EXIT=0` 을 검사하지 않음 · B-0 시험은 생성기 단독만 실행(`sequential_failure_then_success_rc=0`) | **수용** | 블록을 `set -euo pipefail` + `trap`(worktree 정리) + `OUT="$(… \| tee /dev/stderr)"; test "${OUT##*$'\n'}" = "EXIT=0"` 로 재작성 · `MAIN`·`BASE`·`OUT_PATH` 환경변수로 매개(기본값 = 실제 실행) · B-0 시험이 블록 전체를 `bash -c` 서브프로세스로 ⒜ 성공 ⒝ 사전조건 실패(rc≠0 · 파일 부재) ⒞ 생성기 실패(rc≠0 · worktree 잔재 0). 줄 수는 산문에 적지 않는다(Y-4 계열 재발 방지) |

**열 번째 FAIL 에 대한 총괄 자기 점검.** 값은 열 번 맞았고, 남는 지적은 판마다 **수락 체계가 「주장」을 「반증」으로 바꾸지 못한 자리**다 — 이번엔
음성 시험이 검사의 존재를 증명하지 못하는 형태(동반 변조 · 개수 기준). 검증기든 관문이든 「X 를 검사한다」고 적으면 「X 만 바꾼 입력이 X 의 이름으로
떨어진다」는 시험이 붙어야 그 문장이 산다 — [[verification-design-principles]] 「심은 결함 100% 검출」의 필드 단위 적용. 이 규칙을 v12 표 T-V 로 성문화했다.


---

## §17 11차 도전(설계 v12) 지적 AE-1 ~ AE-3 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v12.md`. 판정 FAIL · 3건(HIGH 1 · MED 2) · 새 재정 0 · AD-2 closed · AD-1·AD-3 partially ·
그 밖 전건 closed. 값 8,190 칸은 열한 번째 일치. 셋 전부 **수용** → **v13** → 12차 도전.

| ID | 격 | 지적 요지 | 처분 | v13 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AE-1** | HIGH | 표 T-V 가 「필드 하나씩」이지 「**제약** 하나씩」이 아니다 — `check_ids` 토큰 아래 길이·고유·비공·convergence·집합 상등이 겹쳐 있어 `read.schema → read.__ghost__` 치환(다른 넷 유지)이 없으면 집합 상등 검사를 빼도 통과 · `$comment` 부분 문자열 셋 중 하나만 빼도 통과 · `expected_counts` 개별 계수 float · `provenance.engine_path` 단일 상대경로 등 | **수용** | 진단 코드 = **제약 ID**(검증기 상수 `CONSTRAINT_IDS` · 독립 제약 하나 = ID 하나 · 타입·길이·고유·집합 상등·부분 문자열 하나·리터럴 상등 각각 별개) · 표 T-V 를 제약 ID 단위로 재작성(각 행 = 그 제약만 깨는 변조) · B-0 시험이 `set(CONSTRAINT_IDS) == 표의 ID 집합`(양방향)과 각 변조의 그 ID 위반 실재를 검사 · 라운드 B T-7 ③ 도 같은 표 |
| **AE-2** | MED | `test "$(git diff --name-only … \| wc -l)" = 0` — 명령 치환은 `test` 의 인자일 뿐이라 `git diff` 가 nonzero 여도 `wc -l` 이 `0` 을 내면 통과 · `set -e` 미발동(도전자 실측) | **수용** | 둘째 줄을 `git diff --quiet "$BASE" HEAD -- engine contracts reader` 로(차이 → exit 1 · git 오류 → ≥ 2 · 파이프·치환 없이 `set -e` 가 직접 본다) · B-0 ⒟ `BASE=deadbeef0` 역프로브(rc ≠ 0 · 파일 부재) |
| **AE-3** | MED | 정본 블록이 `$MAIN/.venv/bin/python` 을 고정 — B-0 성공 시험의 `MAIN` 은 시험용 클론이라 `.venv` 가 없다(`git ls-files .venv/bin/python` → 미추적) · 생성기는 HEAD 앞 7자와 비교하는데 B-0 의 `BASE` 가 전체 해시인지 미정 | **수용** | `PYTHON_BIN="${PYTHON_BIN:-$MAIN/.venv/bin/python}"` 매개 추가(기본값 = 실제 실행) · B-0 공통 환경 `PYTHON_BIN=/home/laptop/projects/patent-docent/.venv/bin/python` · `BASE=$(git -C <클론> rev-parse --short=7 HEAD)`(⒝ 는 `HEAD~1` 의 7자) |

**열한 번째 FAIL 에 대한 총괄 자기 점검.** 10차의 「한 필드씩」을 11차가 「한 제약씩」으로 한 겹 더 내렸다 — 음성 시험의 단위는 필드가 아니라 **검사 코드가
분기하는 단위**여야 검사 하나의 부재를 드러낸다. AE-2 는 셸 의미(명령 치환 안의 파이프 실패는 `set -e` 밖)를 총괄이 실측 없이 적은 자리이고, AE-3 은
「시험용 클론」이라는 말을 쓰면서 그 클론에 무엇이 없는지(`.venv`)를 따라가지 않은 자리다. 둘 다 「매개화한 명령을 시험이 실제로 돌릴 때 무엇이 필요한가」를
끝까지 실행해 보지 않은 결과 — 발주 전에 총괄이 그 블록을 시험용 클론에서 한 번 돌려 봤어야 했다.


---

## §18 12차 도전(설계 v13) 지적 AF-1 ~ AF-3 의 처분 — 2026-09-02 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v13.md`. 판정 FAIL · 3건(HIGH 1 · MED 2) · 새 재정 0 · AE-2·AE-3 closed · AE-1 partially ·
그 밖 전건 closed. 값 8,190 칸은 열두 번째 일치. 셋 전부 **수용** → **v14** → 13차 도전.

| ID | 격 | 지적 요지 | 처분 | v14 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AF-1** | HIGH | T-V 의 `exception.cells.set` 변조가 predicate 와 cells 를 함께 바꾸고 기대가 「ID 포함」이라, β 집합 검사를 지우고 predicate 불일치 때 두 진단을 함께 내는 구현이 통과 → T28 §3 ② 공허 · `reader_path.type` 등 누락 ID · `expected_counts` 한 키만 · `cells.value.shape` 에 두 제약 | **수용** | **층위 평가**(필드마다 구조 → 원소 → 고유 → 값 · 앞 층 위반이면 뒤 층 미평가 · 필드 간 의존도 같은 원리)로 한 변조 = 정확히 한 ID · 기대 = **`set(위반 ID) == {target}`** · 표 재작성 — 복합 변조 제거(β cells 변조는 predicate 고정) · 누락 ID 추가(`reader_path.type` · `*.items.nonempty` · `cells.value.type/len2` 분리 · `*.type` 전부) · `expected_counts.<k>.*` 다섯 키 각각 · tree_head nibble 반전 · 고립 불가 제약(`has_convergence`·`len12`·`subset_of_cells`)은 함의하는 제약에 흡수 · `CONSTRAINT_IDS` 자체 형식 검사 |
| **AF-2** | MED | 「시험용 clone」에 B-0 세 산출물이 없다 — 일반 `git clone` 은 worktree 미커밋 파일을 복사하지 않고 HEAD 에도 없다 → 정상 시험이 생성기 부재로 실패 · M3 임의 선택 | **수용** | clone 조립 ①~④ 고정 — `git clone --no-hardlinks` → 두 파일 복사 → clone 안 `git add` + 임시 커밋(provenance ⓕ 깨끗함) → `BASE` = 그 커밋 7자 · 정본 무접촉 |
| **AF-3** | MED | G1~G6 이 `early_phase_spec.judged_here` 를 읽지 않아 `judged_here += [read.__ghost__]` 가 관문 전종 통과 — T26 ⒜ ③ 의 우주(진입·조기·출구)에서 조기 선언 누락 · 존치 :853 이 잡지만 관문 주장이 더 넓다 | **수용** | R2 우주 = entry ∪ exit ∪ `judged_here` · `set(judged_here) == set(points[early].checks) == {id : early ∈ phases(id)}` 세 벌 상등 · list·비공 str·중복 없음 · 변조 ㉞ |

**열두 번째 FAIL 에 대한 총괄 자기 점검.** AF-1 은 AD-1(필드 단위) → AE-1(제약 단위) → AF-1(정확 상등 + 층위)로 세 판에 걸쳐 내려온 같은 계열 —
「검사가 실재함을 시험이 증명한다」는 요건을 총괄이 매번 한 겹씩만 좁혔다. 이번에 **층위 평가**라는 구조로 「한 변조 = 한 ID」를 검증기 쪽에서
보장하게 한 것이 계열을 끝내는 형태라고 본다. AF-2 는 AE-3(클론에 `.venv` 없음)과 같은 형태 — 「시험용 클론」이라는 말의 실물을 끝까지 따라가지
않았다. AF-3 은 G2 의 우주를 적을 때 계약을 전수로 훑지 않고 세 선언 중 둘만 든 것.


---

## §19 13차 도전(설계 v14) 지적 AG-1 · AG-2 의 처분 — 2026-09-03 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v14.md`. 판정 FAIL · 2건(HIGH 1 · MED 1) · 새 재정 0 · AF-2·AF-3 closed · AF-1 partially ·
그 밖 전건 closed. 값 8,190 칸은 열세 번째 일치. 둘 다 **수용** → **v15** → 14차 도전.

| ID | 격 | 지적 요지 | 처분 | v15 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AG-1** | HIGH | T-V 가 독립 제약 전부를 열거하지 않는다 — `exceptions[0]` 의 dict 여부(`[17]` 이 type·len1 통과) · `engine_path`·`reader_path` 원소의 str 타입(`.absolute` 와 한 ID) · 셀 값 문자열 갈래의 정확한 `"StageError"`(`"NotStageError"` 통과) · 표의 ID 열에 `exception.cells.subset_of_cells` 가 남아 「ID 를 두지 않는다」와 모순 · `expected_counts.<k>.*` 가 실제 ID 문자열이 아님 · 필드 간 선행조건 미명시 | **수용** | ID 추가 `exception.item.type` · `provenance.engine_path.items.str` · `provenance.reader_path.items.str` · `cells.value.sentinel`(각 단일 변조) · `subset_of_cells` 행 제거(함의 설명은 표 밖) · `<k>` → 슬러그 다섯(`halt_null`·`escalate_null`·`escalate_repeat`·`stage_error`·`total`) × {type, eq} = 열 개 ID 문자열 · 슬러그↔키 대응 상수 `COUNT_KEY_SLUGS` · **선행조건 DAG** 절(필드 안 · 필드 사이) |
| **AG-2** | MED | G1·T-13 이 `condition`·`note` 를 선택 키로 두어 1행 `condition` 삭제가 G1~G6·T-13·T-10 전부 통과 — T26 ⒜ ① 「조건 문장은 사람용 설명으로 남긴다」·§2.2 「각 행에 옮긴다」와 어긋남(도전자 실측 `g1_accepts_condition_delete=True`) | **수용** | G1 — 각 행 키 집합 == 승인 기계 키 ∪ {condition, note} **정확히** · 둘은 비공 str(내용 자유) — 정본 10행 전부 둘을 든다(총괄 실측) · 변조 ㉟(condition 삭제) ㊱(note 정수) · T-13 동기 |

**열세 번째 FAIL 에 대한 총괄 자기 점검.** AG-1 은 AF-1 의 잔여 — 표를 다시 쓰면서 제거했다고 적은 행을 실제로는 남겼고(`subset_of_cells`), 「모든 필드」를
훑는다면서 `exceptions[0]` 자체의 타입과 셀 문자열 갈래의 값을 빠뜨렸다. 검증기 항목을 적을 때 **컨테이너 → 원소 → 값** 세 층을 필드마다 기계적으로
묻는 절차가 없었다 — v15 의 DAG 절이 그 절차다. AG-2 는 원장 문언(「사람용 설명으로 남긴다」)을 관문 규칙으로 옮기지 않은 것 — 산문이라고 「자유」로
분류한 것이 「없어도 된다」로 읽혔다.


---

## §20 14차 도전(설계 v15) 지적 AH-1 ~ AH-4 의 처분 — 2026-09-03 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v15.md`. FAIL · 4건(HIGH 2 · MED 1 · LOW 1) · 새 재정 0 · AG-2 closed · AG-1 partially. 값 8,190 칸 열네 번째 일치. 넷 전부 **수용** → **v16**.

| ID | 격 | 지적 요지 | 처분 | v16 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AH-1** | HIGH | 최상위 manifest 의 타입 제약이 없다 — `[]` 가 오면 `.keys()` 예외 · 타입과 키 집합을 한 ID 에 합치거나 문서 밖 진단(셋 다 계약 위반) | **수용** | `manifest.type` ID · 변조 `[]` · DAG 뿌리 `manifest.type → top.keys.exact → 각 필드` |
| **AH-2** | HIGH | `expected_counts.keys.exact` 가 `cells` 재계산에 의존하는데 DAG 는 `.eq` 만 뒤로 둠 → `cells.value.sentinel` 변조가 `keys.exact` 도 떨어뜨려 `set(reported) == {target}` 위반 | **수용** | `keys.exact` 를 `COUNT_KEY_SLUGS` 의 고정 다섯 키와의 상등으로 재정의(`cells` 무관) · `.eq` 다섯은 `cells` 층 전부(type · keys.exact · 값 제약) 통과 뒤에만 |
| **AH-3** | MED | `exception.cell_count.eq` 정의가 둘 — 검사 항목 「`== len(cells) == 2048`」 vs 표 「고정값 2048 만」 → 셀 복제 변조에서 두 ID 함께 실패 | **수용** | `cell_count == 2048` 고정값만 · `len(cells) == 2048` 은 `unique` + `set` 이 함의(함의 목록에) |
| **AH-4** | LOW | §1 `import tests.test_m2_read as m2` 는 실물 `tests/test_m21…:33 import test_m2_read as m2` | **수용** | 좌표 정정 |

---

## §21 15차 도전(설계 v16) 지적 AI-1 ~ AI-3 의 처분 — 2026-09-03 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v16.md`. FAIL · 3건(HIGH 1 · MED 1 · LOW 1) · 새 재정 0 · AH 전건 closed · AG-1 partially. 값 8,190 칸 열다섯 번째 일치. 셋 전부 **수용** → **v17** → 16차 도전.

| ID | 격 | 지적 요지 | 처분 | v17 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AI-1** | HIGH | `$comment` 「비공 str」 제약에 ID·변조·순서가 없고 함의 목록에도 없다 → `""` 에서 M3 가 넷 중 임의 선택 | **수용** | 「비공」 직접 검사 **삭제** · 세 `contains` 가 비공을 함의한다고 「ID 를 두지 않는 제약」에 명시 · DAG `comment.type → {contains.T26, T28, T29}` |
| **AI-2** | MED | 「표 T-V 행 순서 = 평가 순서」 선언이 2열 배치 및 명시 DAG 와 충돌(`cells.value.type` 이 `keys.exact` 앞에 보임 등) | **수용** | 그 문언 삭제 · **DAG 절이 평가 순서의 유일 정본**이라고 표 머리와 층위 평가 문장에 명시 |
| **AI-3** | LOW | DAG 「`.eq` 열 개」 — 실제 다섯(type 다섯 + eq 다섯 = 열 ID) | **수용** | 문언 정정 |

**열다섯 번째 FAIL 에 대한 총괄 자기 점검.** 14·15차의 일곱 건은 전부 §2.8 검증기 절 **안**의 정합(타입 뿌리 · 의존 순서 · 이중 정의 · 함의 누락 · 계수 단어)이다.
BLOCKER 는 3차 이후 0 · HIGH 는 「M3 가 임의 선택하게 되는 자리」 하나씩. 지적 수 7 → 8 → 4 → 3 → 5 → 2 → 4 → 2 → 5 → 3 → 3 → 3 → 2 → 4 → 3 — 수렴이 더디다. 총괄이
매 판 지적된 점만 고치고 검증기 절 전체를 **세 표(검사 항목 · T-V · DAG)의 차집합**으로 재검산하지 않은 것이 원인이고, 16차 발주문 §5 는 도전자에게 바로 그
차집합을 내게 했다. 15차에서 도전자가 열어 준 「§2.8 검증기 절을 하나의 정본 형태(제약 ID 표 하나에 순서·정의·변조를 함께)」로 재작성하는 것이 다음 판의 대책 후보다.

## §22 16차 도전(설계 v17) 지적 AJ-1 의 처분 — 2026-09-03 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v17.md`. FAIL · 1건(MED 1) · 새 재정 0 · AI-1~AI-3 전건 closed · AG-1 은 이 한 건 때문에 partially. 값 8,190 칸 열여섯 번째 일치. **수용** → **v18** → 17차 도전.

| ID | 격 | 지적 요지 | 처분 | v18 에서 어떻게 닫았나 |
|---|---|---|---|---|
| **AJ-1** | MED | `provenance.tree_head` 의 제약·선행순서가 세 정본 사이에서 불일치 — 검사 항목·T-V 에는 `provenance.tree_head.eq` 하나뿐인데 DAG 는 「각 키: type → …」로 읽혀 별도 type 단계가 있는 듯하고 `.eq` 가 DAG 에 명시되지 않아, `tree_head = 17` 에서 M3 가 ① 표에 없는 `.type` 신설 ② type 위반도 `.eq` 로 보고 ③ 둘을 한 ID 로 합침 중 임의 선택 | **수용** | DAG 의 provenance 가지를 **키별로 명시** 재작성(`provenance.type → provenance.keys.exact → {tree_head.eq, read_module.type→absolute, …, generated_at.type→iso}`) · `tree_head` 에는 별도 type 제약이 없고 비문자열을 포함한 모든 비상등값을 `.eq` 하나로 보고한다고 명시 · T-V 의 `tree_head` 변조를 nibble 반전 대신 **정수 `17`** 로 바꿔 해석을 직접 고정 |

## §23 17차 도전(설계 v18) — PASS · 도전 루프 종결 — 2026-09-03 추기 (총괄 저작)

원문 = `docs/lessons/2026-09-02-sol-challenge-t26-design-v18.md`. **PASS · 지적 0 · 결정 공백 0 · 새 재정 0.** AJ-1 closed(AG-1 잔여도 함께) · B-1~B-7 · V-1~V-8 · N-1~N-7 전건 closed · 자기 신고 ①~⑳ 전건 「맞다」 · 관문 §2.7 G1~G6 covered(열거 36종) · 출구 convergence 도달 불능 재확인 · 값 8,190 칸 열일곱 번째 일치. 처분 행 없음.

**도전자가 [미검증] 으로 남긴 것**(원문 마지막 절) — §2.8 의 70개 ID 는 첨부 전문 정적 대조 · B-0 산출물 미존재로 미실행 · 골든 생성·T-1/T-2 실러너·pytest·관문은 read-only 규율상 미실행. 이 여섯은 설계의 결함이 아니라 **설계 도전이라는 심급의 경계**이며, 라운드 B-0·B 의 총괄 재현과 opus max 감사(A′·C′·B-0·B 합본)가 실물로 닫는다.

**효력.** T26 §3 ①(PASS 전 착수·커밋 금지 · 조건부 PASS 없음 — 재정 T28~T32 §5)이 해제된다. 착수 순서는 설계 §2.8·D-02 §8 N-3 그대로 — **B-0**(골든 생성기 · sol-coder · worktree `round-b0`) → 총괄 재현·병합 → 총괄이 main 에서 생성 명령 블록 실행(`99fad78` 트리) → 골든 manifest 커밋 → **라운드 B**(설계 v18 첨부 · C-5 반경 고지) → opus max 감사 → 병합(관문 6→7) → T31·T32 소라운드.

**총괄 자기 점검 — 17회의 비용과 원인.** 지적 수 7 → 8 → 4 → 3 → 5 → 2 → 4 → 2 → 5 → 3 → 3 → 3 → 2 → 4 → 3 → 1 → 0. BLOCKER 는 3차 이후 0 · 값(8,190 칸)은 1차부터 한 번도 틀리지 않았다 — 열일곱 판 중 열여섯 판의 지적은 **검증 체계의 구멍**(우회 변조 · 우회 호출자 · 다중집합 · 골든 수락면 · 검증기 절 내부 정합)이었다. 수렴이 더뎠던 원인은 §21 자기 점검 그대로다: 매 판 지적된 점만 고치고 면 전체를 재검산하지 않았다. 그것을 끊은 것은 16차 발주문 §5 가 도전자에게 세 표의 **차집합**을 직접 내게 한 것과, v18 이 DAG 를 키별로 전부 다시 쓴 것이다. 같은 교훈은 세션 기억 `design-challenge-loop-lessons` 에 있다. 자문(fable xhigh · ⑽ ⓑ)은 2차 뒤 1회 썼다.

