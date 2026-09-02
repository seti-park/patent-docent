# 독립 감수 원문 — 재정 T26(실패표 재구성) 집행 설계의 M1b 설계 도전 · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-final` 의 sha256 `e5e8832ac1023a27137d38ec43d08f9f5d31c5bc1ba14ae1f1d1a7996c37f8e2` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `sol-auditor` · `codex exec --sandbox read-only`
· 배경 실행 + `EXIT=` 마커 폴링 · 약 20분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전** —
재정 T26 §3 ① *「M1b 설계 도전(sol xhigh) PASS 전 착수·커밋 금지」* 의 이행이다. 도전자의 일은
승인이 아니라 반증이라고 발주문에 적었고(*「틀린 칸을 찾으려고 읽어라」*), 조건부 PASS 는 없다고
못 박았다.

**대상** = 총괄 저작 설계 메모 `T26-DESIGN.md`(세션 스크래치 · 23,295 B — **리포에 없다**. 이
판정을 받아 v2 로 개정되며, PASS 를 받은 판이 라운드 B 발주문의 첨부로 리포에 들어온다) · 기준
커밋 **`aa9a734`**(라운드 A 집행분). 원장 원문(`ruling-20260902-01-T24-T27.md` §T26 · `ruling-20260901-11-T22-T23.md`)은 도전자가 리포 안에서 직접 읽었다.

**읽기 전용 준수** — 래퍼가 `git status --porcelain` 0행 · HEAD `aa9a734` 일치를 확인하고,
총괄이 정본 트리 지문 `5a62d4f0c14570be44da51967950bfe902e8c42b` 불변 · `git status` 0행을 다시
확인했다. 도전자의 전수 모형은 정본 밖에서 돌았다.

**판정 = FAIL · 지적 7건(BLOCKER 4 · HIGH 2 · MED 1).** 총괄이 설계 §5 에서 스스로 신고한 공격
지점 7개 중 도전자는 **3개를 「틀렸다」**(§5-3 phases 거름 · §5-4 오라클 · §5-5 격자 어휘), **1개를
「재정 필요」**(§5-2 α/β), 3개를 「맞다」로 판정했다. 총괄이 못 본 것 = **S1 의 분모**(9 가 아니라
12 — `read.source-digest` 와 레인 로그 검사 2종을 빠뜨렸다 · B-2) 와 **`upstream-defect` 의 호출자
부재**(T2 가 PD-M5 로 이연 · B-6).

지적 열거 = B-1, B-2, B-3, B-4, B-5, B-6, B-7

처분은 지적 처분 원장 `docs/decisions/DISPOSITIONS.md`(재정 T27) 에 행으로 서고, 사유의 전문은
`D-20260902-02-t26-design-challenge.md` 에 있다. 요지만 적으면 — **B-1 = 재정 상신**(α/β 는 P-4 와
T26 §3 ② 사이의 상류 충돌이라 총괄이 정할 수 없다) · **B-2 = 앞절반 수용**(분모 12 · 8,190칸
전수) **+ 뒷절반 재정 상신**(`read.input-digest` 가 「오늘의 표」의 영역인가) · **B-3 수용**(기준
커밋 골든 동결 — 이 리포의 검증 원리 그대로) · **B-4 수용**(통합 행을 판정점 기준으로 분리 ·
교집합 폐기) · **B-5 수용**(`terminal_action()` fail-closed · `StageError`) · **B-6 수용 + 해석
상신**(`kind` 3행 · 호출자 없음 명시 · `checks` 의무의 범위) · **B-7 수용**.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

출구 판정에 실제로 들어오는 12개 검사만 모델링하면 새 격자는 현행과 동일했습니다. 그러나 설계의 전수 시험은 그중 9개만 검사하고, P-4와 충돌하는 α를 채택하며, 원장이 명한 재시도 집합의 정확한 등식을 `phases` 교집합으로 약화합니다. 그대로 착수할 수 없습니다.

## 지적 목록

### B-1 · BLOCKER · 설계 §2.3 α · P-4/T16 · `read.yaml:700-706`

`read.convergence`의 출구 재시도를 허용하는 α 독법은 상류 문언과 맞지 않습니다.

P-4 원문은 `retry(1)→escalate 경로를 조기 지점으로 이동`한다고 명시합니다. 현행 계약과 SPEC도 “조기 수렴 지점이며 접지 지출 이후로 미루지 않는다”고 적습니다([P-4 원문](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-03-P1-P11.md:38), [read.yaml](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:700), [SPEC](/home/laptop/projects/patent-docent/docs/SPEC.md:492)). T16의 출구 재시도 근거는 청구항 검사 2종에 관한 것이지 convergence가 아닙니다([T16](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260901-07-T16.md:39)).

현행 러너가 모든 출구 실패를 재시도하는 것은 α의 근거가 아니라 P-4 위반 실물입니다. 하지만 β로 고치면 재시도 횟수뿐 아니라 같은 서명 재현 시의 라벨도 바뀔 수 있어 T26 §3②와 충돌합니다.

닫는 법: 착수를 멈추고 다음 중 하나를 새 재정으로 명시해야 합니다.

- P-4를 유지해 β를 택하고, 현행 위반 교정이 T26의 표 불변 조건에 대한 명시적 예외임을 적는다.
- P-4를 개정해 α와 출구 convergence 재시도를 명시적으로 승인한다.

### B-2 · BLOCKER · 설계 §2.6 S1·§3 · `read.py:1799-1915`

S1의 분모가 틀렸습니다. 출구 `_failure_verdict`에 들어올 수 있는 검사 ID는 9개가 아니라 12개입니다.

- `READ_CHECK_IDS`: 10개
- 엔진 소관 lane-log 검사: 2개
- 비공집합 × repeated 2 = `(2^12−1)×2 = 8,190`

제안된 격자를 이 8,190칸에 대조하면 불일치는 0입니다. 그러나 S1의 1,022칸은 `read.source-digest`와 lane-log 두 검사를 포함한 전체 표를 증명할 수 없습니다.

더구나 원장 문언대로 진입 검사 `read.input-digest`까지 포함한 13개 선언 검사로 계산하면 16,382칸 중 2,048칸이 달라집니다. 대표 반례:

- `{read.input-digest}`, `repeated=False`
  - 현행 `_failure_entry_for`: 기본 verbatim 갈래 → `(escalate, None)`
  - 새 격자: input-digest 전용 halt 행 → `(halt, "환경 오류")`
- `{read.input-digest}`, `repeated=True`
  - 현행: 반복 행 → `(escalate, "국면 간 변이 재현 — 코드 결함 의심")`
  - 새 격자: halt → `(halt, "환경 오류")`

설계 §3이 이를 “표 밖 확장”이라고 부른 것은 T26 §3②의 전수 조건과 맞지 않습니다.

닫는 법:

1. `_failure_verdict`의 공식 입력 영역을 12개 출구 검사로 한정할 권한이 있는지 재정으로 확정한다.
2. 확정된다면 8,190칸 전수를 고정하고 `read.input-digest`는 진입 예외 경로로 별도 반증한다.
3. 13개 전부가 표의 영역이라면 이 변경은 값 공간 변경이므로 새 재정 없이는 진행할 수 없다.

### B-3 · BLOCKER · 설계 §2.6 S1·S4

구 구현 복제 오라클은 오늘의 값을 고정하지 않습니다. 구 오라클과 새 구현이 모두 개정된 동일 계약에서 `action`·`then`·`reason_label`을 읽기 때문입니다.

예를 들어 `read.schema.then`을 `halt`에서 `escalate`로 바꾸면 구 오라클과 새 구현이 함께 `escalate`를 내므로 S1은 계속 green입니다. R5의 condition 문언 존치는 조치와 라벨의 공유를 끊지 않습니다. S4는 값 변조가 출력에 반영됨을 보일 뿐, 그 변조 때문에 S1이 실패하도록 만들지 않습니다.

이는 이 리포가 이미 경고한 “시험과 구현이 같은 기대값을 읽는” 형태입니다([CLAUDE.md](/home/laptop/projects/patent-docent/CLAUDE.md:127)).

닫는 법: 기준 커밋의 결과를 새 계약과 독립된 골든으로 동결하십시오. 최소한 다음이 고정되어야 합니다.

- 공식 검사 ID 목록
- 모든 비공집합 × repeated의 예상 `(action, reason_label)`
- 기준 커밋과 생성 절차

구 제어 흐름을 남겨도 조치·라벨은 개정 계약에서 읽으면 안 됩니다.

### B-4 · BLOCKER · 설계 §2.3 R6·§2.5 ⒝ · T26 §2⒜③

`phases` 교집합은 원장이 명한 “정확히 같다”를 약화합니다.

현재 통합 행은 7개 검사를 한 행에 두고 `points: [early, exit]`를 신고합니다. 그중 5개는 exit 전용입니다. 설계는 이를 phase로 잘라 early 대조에서 숨깁니다. 결과적으로 행이 실제로는 적용되지 않는 판정점을 신고해도 관문이 통과합니다.

원장은 다음 등식을 명했습니다.

`판정점 checks == 그 판정점을 신고한 retry(n) 행들의 checks 합집합`

교집합을 더한 식을 명하지 않았습니다([T26](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-01-T24-T27.md:183)).

닫는 법: 통합 행을 판정점 기준으로 분리하십시오.

- `claim-inventory`, `dependency-parse`: `points: [early, exit]`
- 나머지 verbatim 계열 5종: `points: [exit]`
- convergence: B-1 재정 결과에 따라 `[early]` 또는 `[early, exit]`
- schema: `[exit]`

그 뒤 관문은 교집합 없이 원장 식을 그대로 비교해야 합니다. phase는 별도로 “그 판정점에서 실제 실행되는가”만 검증해야 합니다.

### B-5 · HIGH · 설계 §2.4 `terminal_action`·`select_failure_row` · `__init__.py:101-113`

관문 ⒞만 보면 `then` 없는 `retry(n)`과 `then: retry(n)`을 모두 금합니다. 둘 다 `terminal_action == retry(n)`이 되어 terminal 어휘 밖이기 때문입니다.

그러나 런타임 선택기의 실패 방식은 정해지지 않았습니다. 현행 `worst_status`는 알 수 없는 값에 `order.get(status, 0)`을 적용하므로:

- 잘못된 retry 후보 하나뿐이면 `worst_status == "ok"`가 됩니다.
- 다른 escalate 후보와 섞이면 잘못된 후보가 조용히 무시됩니다.
- 이후 어느 행을 반환할지는 설계에 없습니다.

닫는 법: `terminal_action()` 자체가 다음을 검사하고 `StageError`를 내도록 명시하십시오.

- `action: retry(n)`이면 유효한 terminal `then` 필수
- `then`은 `halt|reject-upstream|escalate` 중 하나
- terminal action은 `worst_status` 호출 전에 검증
- `then` 없는 retry와 `then: retry(n)` 변조 시험 추가

### B-6 · HIGH · 설계 §2.1 `kind`·§2.4 upstream·§2.7 binding

원장은 “각 행에 `checks`”를 명했지만 설계는 세 행을 `kind` 예외로 둡니다. 반복 행에는 별도 식별자가 필요한 만큼 `kind`라는 키 자체는 공학적 해법이 될 수 있습니다. 다만 현재 설계는 원장 문언을 “각 검사 실패 행”으로 조용히 좁히고 있습니다.

특히 `upstream-defect`는 “READ 진입 전 사건”인 실행 경로가 아닙니다. 현행 리포에는 수신 코드가 없으며, T2가 그 집행을 PD-M5로 명시 이연했습니다([T2](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260831-05-T2-T6.md:30)). 그런데 설계는 단독 조회와 `runner_reads` 분류를 적어 coder가 다음 중 하나를 골라야 합니다.

- 수신 코드를 새로 구현해 T2 범위를 위반
- 구현하지 않아 `runner_reads` 선언을 거짓으로 둠

닫는 법: T26에서는 upstream 행에 식별 키만 추가하고 호출자는 만들지 않는다고 명시하십시오. binding도 `deferred/test_bound`로 분류해야 합니다. 아울러 `checks` 의무가 검사 행에만 적용된다는 해석은 원장 정합 절에 명시하고, 그 해석이 허용되지 않으면 재정으로 보완해야 합니다.

### B-7 · MED · 설계 §2.6 · T26 §3⑤

S2는 신설 관문만 plain·`-O`로 실행합니다. 원장 §3⑤는 전수 시험과 관문 전종의 plain·`-O`를 요구합니다.

닫는 법: 수용 기준에 다음을 명시하십시오.

- 전수 pytest
- 기존 5개 관문 + 신설 관문 모두 plain
- 같은 6개 관문 모두 `python3 -O`
- 각 명령과 예상 exit code

## A. 원장 정합 — FAIL

| 설계 요소 | 집행하는 원장 | 판정 |
|---|---|---|
| `checks` 키, R1·R2·R4·R5 | §2⒜①·③ | 방향은 맞음 |
| 격자와 계약 순서 | §2⒜② | 12개 출구 검사에 대해서는 현행 표와 일치 |
| 반복 행을 후보로 추가 | §2⒜② | 맞음 |
| 명시적 재시도 부분집합·러너 subset 검사 | §2⒜③, T25 흡수 | 방향은 맞으나 B-1·B-4로 값이 미확정 |
| 양방향 관문·심기 | §2⒜③, §3③ | 완전성은 맞으나 재시도 등식은 약화됨 |
| S1 차분 시험 | §3② | B-2·B-3 때문에 불충족 |
| CLAUDE 정정 마커 | §3④ | 맞음 |
| 전수+관문 plain·`-O` | §3⑤ | B-7로 불완전 |
| source/freeze needle 존치 | T26 §4 반영처 | 맞음. READ만 범위다 |
| `kind` 사전 | 원장에 없음 | 구조적 재량 가능성이 있으나 “각 행 checks”와의 충돌을 먼저 닫아야 함 |
| `phases` 교집합 | 원장에 없음 | 원장 등식을 바꾸므로 허용 불가 |
| α | 원장에 없음 | 재시도·라벨 값 공간 변경 가능성이 있어 재정 사항 |
| binding_status 확대 | 원장에 없음 | 공학 재량이나 실제 소비 경로와 일치해야 함 |

§3①에 따라 이번 판정이 FAIL인 동안 착수·커밋은 금지됩니다.

## B. 오늘의 표 불변 — FAIL

- 출구에서 실제 `_failure_verdict`로 들어오는 12개 검사에 한정하면 새 순서와 격자는 8,190칸 전부 현행과 같습니다.
- 설계 S1의 1,022칸은 그 전수가 아닙니다.
- 진입 검사까지 포함하면 2,048칸이 달라집니다.
- 현행 모든 `retry(n)` 행에는 `then`이 있으므로 정상 계약에서는 `worst_status`가 retry를 직접 보지 않습니다.
- `then` 없는 retry 행은 관문에서는 거부되지만 런타임 선택기는 fail-closed가 아닙니다.
- 설계 §3의 `input-digest` “표 밖 확장”은 T26 §3② 아래 허용되지 않습니다.

## C. 설계 §5의 7개 공격점

1. **§5-1 동시 불가 — 맞다(현행 코드 한정).**  
   조기 게이트는 claim → exact-match → escalation의 `elif` 사슬이라 하나만 선택합니다([read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:1594)). 반려 수신은 동시 후보가 아니라 아예 미구현·이연 상태입니다. 미래에 동시 후보가 생기면 `halt > reject-upstream`은 T26이 직접 명한 순위입니다.

2. **§5-2 α/β — 결정 공백이라 재정 필요.**  
   P-4 문언상 β가 맞지만, β는 오늘 러너의 재시도와 경우에 따라 라벨을 바꿉니다. B-1처럼 상류 간 충돌을 새 재정으로 해소해야 합니다.

3. **§5-3 phases 거름 — 틀렸다.**  
   `points[].phase` 추가만으로도 부족합니다. row-level `points`가 그 행의 모든 `checks`에 적용된다는 문제를 행 분할로 제거해야 합니다.

4. **§5-4 오라클 — 틀렸다.**  
   제어 흐름은 다르지만 조치·라벨 정본을 공유하므로 현재 표를 고정하지 못합니다.

5. **§5-5 격자 어휘 — 틀렸다(관문은 맞고 런타임은 미완성).**  
   관문 ⒞는 두 잘못된 retry 형태를 거부합니다. 다만 선택기에서 같은 검증을 요구하지 않아 `order.get(..., 0)` 경로가 남습니다.

6. **§5-6 source/freeze 범위 — 맞다.**  
   T26의 반영처는 READ이고, 공통 `failure_entry`는 두 스테이지가 계속 사용하므로 존치가 맞습니다.

7. **§5-7 T22 시험 — 맞다.**  
   verbatim 행 변조가 lane-log 처분을 움직이지 않는다는 부정 대조는 새 키 조회에서도 같은 성질을 증명합니다. R1과 결합하면 각 lane-log ID의 전용 행 결속도 유지됩니다.

## D. 설계가 말하지 않은 결정점 — FAIL

coder가 임의 선택하게 되는 자리는 최소 세 곳입니다.

- `read.input-digest`를 `_failure_verdict`의 공식 입력 영역에 넣을지, 진입 예외 전용으로 둘지
- 잘못된 terminal action을 `StageError`로 거부할지, `worst_status`가 0으로 취급하게 둘지
- 이연된 `upstream-defect`에 실제 호출자를 만들지, 선언만 둘지

B-1의 convergence 출구 재시도까지 포함하면 결과에 영향을 주는 공백이 네 곳입니다.

## E. 관문 설계 — FAIL

- ⒜의 양방향 차집합은 checker ID 완전성 자체는 구현합니다. 단, 허용된 `kind` 행과 “검사 없는 행”의 구별을 명시해야 합니다.
- ⒝는 `phases` 교집합 때문에 원장의 정확한 등식이 아닙니다.
- 자기 실증 5종은 원장이 요구한 세 결함 종류를 명목상 덮습니다.
  - 행 없는 검사: ⑴
  - 검사 없는 행: ⑵
  - 재시도 불일치: ⑶·⑷ 양방향
- 다만 ⑵의 변조를 “`checks: [read.__ghost__]`인 새 검사 행 추가”처럼 정확히 써야 합니다.
- 추가로 `exit` 전용 검사가 든 행에 `points: [early]`를 거짓으로 붙인 변조를 심어야 합니다. 현 설계는 phase 교집합 때문에 이 결함을 통과시킵니다.
- R3·R4와 terminal-action 검증도 자기 실증 분기가 없습니다. 원장 최소 세 심기와 별개로, 설계가 새로 주장한 관문 기능을 검증하려면 추가해야 합니다.

## [미검증]

- `T26-DESIGN.md` 파일은 기준 커밋에 없어서 첨부 전문을 기준으로만 좌표를 잡았습니다.
- 신설 관문과 새 선택기 구현이 아직 없으므로 S1·S2 자체는 실행할 수 없었습니다.
- 기준 HEAD가 설계가 지정한 `aa9a734`이고 작업 트리는 깨끗함을 확인했습니다. 현행 코드와 제안 알고리즘의 조합 비교는 별도 전수 모형으로 검산했습니다.
