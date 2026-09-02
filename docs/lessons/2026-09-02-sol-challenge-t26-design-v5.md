# 독립 감수 원문 — 재정 T26 집행 설계 v5 의 M1b 설계 도전(4차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v5/final.txt` 의 sha256 `64465ef9bb9bd2c71687f199e8ca89f50aef1ca63700e86526aea94ed12f485e` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 26분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 4차 심사** — v4(3차 FAIL · W-1~W-4) → **v5** 에 대한 것.
도전 중 총괄이 라운드 C′ 병합(`867b95b`)과 문서 커밋(`39a6438`)을 넣어 HEAD 가 `4e1f05c` 에서 움직였다 — 도전자는 발주문의
「코드 경로 diff 0」 전제가 `tools/check_dispositions.py`·그 시험 두 파일에서 깨졌음을 **숨기지 않고** 적고, T26 대상 경로
(`engine contracts reader` · READ 시험 파일 · `check_failure_table.py`)는 diff 0 임을 확인해 진행했다. 총괄 귀책 — 발주문이
「tools 불변」이라 적었으나 그 시각 C′ 레인이 돌고 있었다. 5차 발주문은 그 사실을 고지했다.

**판정 = FAIL · 지적 3건(BLOCKER 1 · HIGH 1 · MED 1) · 결정 공백 0 · 새 재정 사항 0 · W-1~W-4 전건 closed · B·V·N 전건 closed.**
값 8,190 칸은 네 번째로 일치. 새로 찾은 것 — **X-1**: 관문이 **행 분할**을 고정하지 않아 T22 §3 ① 의 lane-log 두 전용 행을
하나로 병합해도(11행 → 10행) 관문 전종·골든을 통과한다. **X-2**: T-1 이 finding 을 더하는 `element-set` 축은 exact-match 가 아니라
**escalation-trigger** 다(exact-match 축 = independent-count · dependent-count · dependent-set) — 자기모순 판정서. **X-3**: `upstream-defect`
행의 `reject-upstream` 이 어디에도 고정되지 않아 `halt` 로 바꿔도 통과(PD-M5 이연 처분의 계약 변경).

지적 열거 = X-1, X-2, X-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§10** 에 있다.
셋 전부 **수용**(공학 수정 · 규율 11 ③) — **v6** 에 반영하고 5차 도전에 냈다. v6 의 핵심 = 관문 G1 이 **승인 실패표 골격 전체**
(11행 · 순서 · 키 · action · then · reason_label · points — 산문 두 키만 자유)를 상수로 들고 정확 일치를 대조한다(원장값의 기록 ·
각 행에 재정 좌표 · §4 ⑲ 자기 신고) · T-1 은 peer spec 사본에 독립항을 복제해 검사기 자신이 `independent-count` 를 fail 로 내게 한다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## W-1~W-4 폐쇄 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| W-1 | closed | 승인 집합을 엔진·관문 상수로 고정하고 진입 가드, T-4의 12종 전수 8/4 분류, T-5 동시 변조, T-11⑥, T-12를 결합했다. 계약 목록+행 동시 변조는 관문과 런타임 모두 거부한다. |
| W-2 | closed | `_gate_escalation_verdict()`가 `terminal_action()`을 사용한다. 실제 상신축 러너 시나리오도 [test_m2_read.py:2727](/home/laptop/projects/patent-docent/tests/test_m2_read.py:2727)에 있으므로 T-8의 조건은 러너 경로 시험을 요구하는 쪽으로 확정된다. |
| W-3 | closed | G2와 T-12가 선언 배열의 행 형식·id 문자열·중복·길이를 다중집합 차원에서 검사하며 ㉒㉓도 있다. |
| W-4 | closed | 실행·SPEC 사이의 18/20 충돌은 없어졌고 변조 목록은 24종으로 일치한다. SPEC에는 숫자를 복제하지 않는다는 지시도 있다. |

그러나 다음 새로운 결함 때문에 PASS는 불가하다.

## 지적 목록

### X-1 · BLOCKER · 설계 §2.2 행 6·7 · §2.7 G1/G2/G6 · §2.9 `test_m23` 개정

관문은 T22가 정한 두 레인 로그 검사의 **각자 전용 실패 행**을 보장하지 않는다.

T22는 두 검사에 전용 행을 각각 세우고 처분의 출처가 “자기 행”임을 시험하도록 명했다. 이는 재량이 아니라 판정 공간을 정한 Owner 재정이다. [T22 §2⒜](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260901-11-T22-T23.md:48), [T22 §3①](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260901-11-T22-T23.md:89)

다음 변조는 v5의 G1~G6을 모두 통과한다.

```yaml
checks:
  - read.lane-log-shape
  - read.lane-log-digest-value
action: escalate
```

즉 기존 두 행을 하나로 합쳐 11행을 10행으로 만든다.

- R1: 각 id는 여전히 정확히 한 번 등장
- R2: 합집합 불변
- G3/G4/G5: 무관
- G6: 유효한 비-retry `escalate`
- 8,190칸 `(조치, 라벨)`: 두 행의 값이 같아 불일치 0
- 계획된 `test_lane_log_verdicts_come_from_their_own_failure_rows`: 두 id가 같은 행을 찾아도 verbatim 행과는 독립이므로 통과 가능

실측 모형:

> `MERGED_LANE_ROWS 10 (True, True, True, True, True, True)`  
> `MERGED_GRID_MISMATCHES 0 []`

닫는 법:

- G1에 `failure[]`의 정확한 검사 행 분할을 고정한다. 최소한 두 lane-log id는 서로 다른 singleton `checks` 행이어야 한다.
- 더 안전하게는 검사 행 8개의 `checks` 집합 분할과 kind 행 3종, 총 11행을 정확히 대조한다.
- `test_m23`에서 두 조회 결과의 행 위치가 서로 다르고 각 `checks == [해당 id]`인지 검사한다.
- 두 lane-log 행 병합 변조를 자기시험에 추가한다.

### X-2 · HIGH · 설계 §2.9 T-1 · [reader-rules.yaml:780](/home/laptop/projects/patent-docent/reader/reader-rules.yaml:780) · [convergence.py:258](/home/laptop/projects/patent-docent/reader/lib/convergence.py:258) · [run_checks.py:253](/home/laptop/projects/patent-docent/reader/lib/run_checks.py:253)

T-1이 exact-match 실패를 주입한다면서 `element-set`에 finding을 직접 추가한다. 그러나 `element-set`은 `exact-match`가 아니라 `escalation-trigger` 축이다.

직접 확인:

> `ELEMENT_SET_POLICY escalation-trigger`  
> `EXACT_MATCH_AXES ['dependent-count', 'dependent-set', 'independent-count']`  
> `T1_LOCUS_IS_EXACT_MATCH False`

실제 검사기는 `element-set` 미달 시 `row.add()`를 호출하지 않고 `escalations[]`에만 적는다. 반면 설계의 wrapper는 이미 계산이 끝난 행에 finding만 추가한다. 그러면:

- `checks[].status == fail`
- finding은 존재
- `convergence_detail.axes[].status`는 전부 기존 `pass`
- `convergence_report.axes`도 기존 `pass`

인 자기모순 판정서가 된다. 이는 T28 §3③의 “실제 러너 경로에서 출구 convergence exact-match 실패”를 정직하게 실증하지 않는다.

닫는 법: wrapper가 `ctx.peer_spec`의 복사본에 독립항 하나를 복제해 `independent-count`를 실제로 어긋나게 한 뒤, 수정된 `CheckContext`로 원래 `run_read_checks()`를 호출하게 하라. 그러면 검사기 자신이 다음을 낸다.

> `FAILING_AXES [('independent-count', 'exact-match', 'fail')]`  
> `FINDINGS [('independent-count', 'claims.독립항')]`  
> `COHERENT_EXACT_MATCH True`

시험은 반환 status뿐 아니라 판정서에 exact-match 축 `fail`이 실제로 기록됐는지도 확인해야 한다.

### X-3 · MED · 설계 §2.2 행 11 · §2.7 G1/G6 · §2.9 T-9 · [read.yaml:760](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:760)

`upstream-defect` 행의 현재 조치 `reject-upstream`이 어떤 관문·시험에도 고정되지 않는다.

다음 변조가 G1~G6을 모두 통과한다.

```yaml
kind: upstream-defect
action: halt
```

G6은 `halt`도 유효 terminal로 받는다. T-9는 행 존재·kind·호출자 0만 보고, 골든은 kind 행을 영역에 포함하지 않는다. 실측 모형:

> `UPSTREAM_ACTION_HALT (True, True, True, True, True, True)`  
> `MUTANTS_ACCEPTED True`

현재 호출자가 0이라 당장 실행값은 안 바뀌지만, PD-M5에 이연된 미래 수신 처분을 `reject-upstream → halt`로 바꾸는 계약 변경이다. 이를 허용한 재정은 없다.

닫는 법:

- G1/G6에 kind별 승인 조치를 고정한다: `retry-repeat=escalate`, `gate-escalation=escalate`, `upstream-defect=reject-upstream`.
- 또는 T-9가 upstream 행의 정확한 action과 금지된 `then` 부재까지 검사하게 한다.
- `upstream-defect.action: halt` 변조를 자기시험에 추가한다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·§2.6. 공식 8,190칸 값은 HEAD와 전건 일치 |
| T26 §2⒜③ 완전성·재시도 등식·부분집합 | covered | G2/G3, 승인 집합 고정, 런타임 subset 검사 |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | covered | 99fad78 골든 절차와 T-7; 전수 모형 불일치 0 |
| T26 §3③ 양방향 관문·세 심기 | partially | 필수 세 심기는 포함하지만 T22 전용 행 병합 및 upstream 조치 변조를 통과시킴(X-1/X-3) |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 불변 | covered | §2.8 T-7; 직접 전수 일치 |
| T28 §3② β 표지 | covered | 실행 가능한 술어, 2,048칸 |
| T28 §3③ 실제 러너 음성·양성 | partially | 패치 위치·레인 계수는 맞지만 주입 축이 exact-match가 아님(X-2) |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3·승인 집합 |
| T29 §3① 골든 id 12개 | covered | §2.8·T-7·T-12, 선언 중복도 거부 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 행·표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9. 직접 grep 0 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |
| T26 §2⒝가 흡수한 T22 전용 2행 | partially | 표에는 두 행이 있으나 관문·시험이 병합 변조를 허용(X-1) |

T31을 B 뒤 소라운드로 분리하고 T32를 그 소라운드에 합치는 판단은 원장과 맞다. `screening_memos[].read_run`도 범위 밖으로 유지했다.

원장이 직접 명하지 않은 `judged_at`, R8/R9, 미지 id fail-closed, provenance 검사, B-0, helper 이름, 승인 상수 복제는 공학·운영 재량이다. X-1은 재량이 아니라 T22 집행 누락이고, X-3은 기존 계약값 보존 문제다. 새 Owner 재정은 필요하지 않다.

## B. 오늘의 표 불변

값 판정은 PASS다.

| 결과 | 직접 재계산 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |

v5 11행과 HEAD 전수 대조:

> `MISMATCH_COUNT 0`  
> 마지막 출력: `MISMATCH_SAMPLE []`

§2.2 손검산에 현재 틀린 칸은 없다. 세 `StageError` 칸은 정확히 다음이다.

- mask 1024, repeated=1: `lane-log-shape`
- mask 2048, repeated=1: `lane-log-digest-value`
- mask 3072, repeated=1: 두 lane-log id

R6가 모든 후보의 `terminal_action()`을 먼저 검증하므로 정상 `_failure_verdict`에서는 `worst_status.order.get(미지값, 0)`에 미지 terminal이 도달하지 않는다. W-2 수정으로 조기 상신축도 같은 fail-closed 경로를 탄다.

단, X-1의 행 병합처럼 `(조치, 라벨)`을 바꾸지 않는 구조 위반은 골든으로 잡히지 않는다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β, 출구 convergence 제외, 부분집합 우선, 실제 모듈 패치와 0/3 레인 대조가 명시됨. X-2는 새 시험 진실성 결함 |
| B-2 | closed | 출구 12 id·8,190칸, input-digest 진입 시험 분리 |
| B-3 | closed | 값은 99fad78 구현에서 생성한 동결 파일이고 B는 파일만 읽음 |
| B-4 | closed | 판정점별 행 분리, `phases` 없는 정확 등식 |
| B-5 | closed | 모든 도달 가능한 READ 선택 경로가 `terminal_action()`을 통과 |
| B-6 | closed | kind 3종, upstream 호출자 0, deferred/test_bound |
| B-7 | closed | pytest와 7개 관문 모두 2모드 |

### V-1~V-8

| 지적 | 판정 | 사유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 패치가 러너 전역에 도달 |
| V-2 | closed | `-I`, repo 선삽입, 모듈·패키지 경로·HEAD·clean 검증 |
| V-3 | closed | `/retry-1/` 정확히 3행과 세 task |
| V-4 | closed | phase 우주·중복·부분집합 검증 |
| V-5 | closed | 판정점 `{early, exit}` 유일성과 12-id 우주 |
| V-6 | closed | 실행 가능한 비트식 |
| V-7 | closed | T-11⑤ terminal 어휘 상등 |
| V-8 | closed | 세 StageError와 두 순서 구별 |

### N-1~N-7

| 지적 | 판정 | 사유 |
|---|---|---|
| N-1 | closed | chdir 전 절대 `out` 고정 |
| N-2 | closed | 12개 phases 실측, R9 통과 |
| N-3 | closed | B-0 → 골든 커밋 → B 순서 |
| N-4 | closed | `_exit_retry_eligible()` 명명 |
| N-5 | closed | T-12 계약↔엔진 양방향 다리 |
| N-6 | closed | `exit` 필수, early iff |
| N-7 | closed | 다섯 세부가 명시됨. X-2는 wrapper 좌표가 아니라 주입 의미의 새 결함 |

## D. 출구 convergence 도달 가능성

설계의 “레인 페이로드로 도달 불능” 주장은 맞다.

- `decompose_only_spec()`은 출구와 같은 `assemble_spec()`을 호출한다. [read.py:980](/home/laptop/projects/patent-docent/engine/stages/read.py:980)
- tail은 입력 `decompose`를 그대로 반환하고, 러너는 조기에 쓴 `decomposes[canonical_run]`을 넘긴다. [read.py:830](/home/laptop/projects/patent-docent/engine/stages/read.py:830), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)
- 양쪽 모두 claims를 deepcopy한 뒤 같은 `rewrite_claims()`를 호출한다. [read.py:528](/home/laptop/projects/patent-docent/engine/stages/read.py:528)
- `SpecIndex` 자체는 items·figures도 인덱싱하지만 수렴 6축은 청구항 수·문언·트리·종속 서명·addition 부착만 소비한다. [convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)
- 후속 조립으로 `applicant_interest.material_id`는 달라질 수 있으나 6축은 이를 읽지 않는다.

직접 조립:

> `CLAIMS_OBJECT_EQUAL False`  
> 마지막 출력: `CONVERGENCE pass [('independent-count', 'pass'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

따라서 올바른 T-1 형태는 출구 검사층 주입이다. 다만 v5의 수동 finding 추가가 아니라, 출구 wrapper에서 peer spec을 복제·변형하여 실제 exact-match 축을 검사기 자체가 실패시키는 형태여야 한다(X-2).

부분집합 검사를 서명 비교보다 앞에 두면 convergence가 포함된 실패는 첫 관측에서 탈출하므로 `repeated_signature`가 서지 않는다. `repeated ∧ convergence` 2,048칸의 도달 불능 표지는 맞다.

## E. 자기 신고 ①~⑱

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest 표 밖 값은 T29 승인 |
| ③ | 맞다 | `judged_at` 이름은 위임된 공학 선택 |
| ④ | 맞다 | T-11⑤가 terminal 두 벌을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지와 런타임 우회가 모두 닫힘 |
| ⑦ | 맞다 | 미지 id는 공식 12-id 영역 밖 무효 입력의 fail-closed 처분 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 조기 가드가 early·exit 목록을 실제로 읽고 승인 상수와 대조하므로 `runner_reads`가 사실임 |
| ⑩ | 틀렸다 | 모듈 패치 위치는 맞지만 `element-set`을 exact-match finding으로 위조함(X-2) |
| ⑪ | 맞다 | T28 술어에만 도달 불능 표지를 둠 |
| ⑫ | 맞다 | T32는 T31 소라운드에 합칠 수 있음 |
| ⑬ | 맞다 | 판정점·검사 우주 고정은 무효 계약의 fail-closed 형식 |
| ⑭ | 맞다 | provenance 6검사와 `-I`는 설계상 충분함. 실제 생성기는 아직 없어 실행 미검증 |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 앞에 세우는 순환 해소 |
| ⑯ | 맞다 | R9는 정본 국면을 기계 대조하며 실측상 새 입법이 아님 |
| ⑰ | 맞다 | 승인 집합은 원장값의 기록이며 T-4의 고정 8/4와 T-11⑥이 두 상수의 동반 표류를 막음 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |

## F. 관문 G1~G6

| 관문 | 판정 | 설명 |
|---|---|---|
| G1 | partially | id 유일성·kind 사전·xor는 맞지만 T22 전용 행의 분리와 정확한 11행 분할을 보장하지 않음(X-1) |
| G2 | covered | 선언 양방향 차집합과 배열 중복을 검사 |
| G3 | covered | 정확 등식·판정점 유일성·승인 집합을 모두 검사 |
| G4 | covered | 유령 phase, 거짓 early, exit 누락을 거부 |
| G5 | covered | input-digest 표지·halt·points 부재·retry 제외 |
| G6 | partially | terminal 형태는 완전하지만 kind별 승인 action을 고정하지 않아 upstream action 변경을 허용(X-3) |

필수 심기는 모두 포함된다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- W-1 동시 일관 변조: ㉑
- 선언 중복: ㉒㉓

그러나 다음 변조가 통과한다.

1. lane-log 두 전용 행을 하나로 병합 — G1~G6 전부 true, 골든 불일치 0.
2. `upstream-defect.action`을 `reject-upstream → halt`로 변경 — G1~G6 전부 true.

따라서 관문 설계는 FAIL이다.

## G. M3 결정 공백

새로운 Owner 판단이나 M3의 임의 선택이 필요한 결정 공백은 찾지 못했다. §2.2가 목표 행과 값을 명시하고, W-2의 조건부 문구도 기존 상신축 러너 시험이 실재하므로 실제 경로 시험으로 확정된다.

다만 X-2는 공백이 아니라 **잘못 고정된 지시**이고, X-1/X-3은 명세는 맞지만 수락 체계가 위반 구현을 통과시키는 결함이다. 어느 경우든 그대로 발주할 수 없다.

## 검증 경로

- 초기 기준 확인  
  `git status --short && git rev-parse --short HEAD && git rev-parse HEAD^{tree} && ...`  
  출력: `4e1f05c`, 트리 `e25975bf8cff57b73705f67c27e50d767d0a845f`; 마지막 출력 `0`.

- 99fad78 기준 코드 무변경  
  `git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l`  
  마지막 출력: `0`.

- HEAD `_failure_verdict` 전수 호출  
  `.venv/bin/python -c '<12 id · mask 1..4095 · repeated 0/1>'`  
  출력에 `COUNTS ... 6144/1023/1020/3`, `BETA 2048`; 마지막 출력: `TOTAL 8190`.

- v5 11행 독립 모형과 HEAD 대조  
  `.venv/bin/python -c '<11행 후보·격자·tie-break 모형>'`  
  출력: `MISMATCH_COUNT 0`; 마지막 출력: `MISMATCH_SAMPLE []`.

- 선언·국면 실측  
  `.venv/bin/python -c '<read.yaml entry/exit/phases/R9 검사>'`  
  출력: `R9 True ...`; 마지막 출력: `POINT_IDS ['early', 'exit']`.

- 후속 레인 수  
  `.venv/bin/python -c '<payloads_with_dangling_reference + plan_grounding/plan_synthesis>'`  
  마지막 출력: `RETRY_LANE_ROWS 3 [('ground-independent', 'read-a/ground-independent/retry-1/batch-0'), ('ground-dependent', 'read-a/ground-dependent/retry-1/batch-0'), ('synthesize', 'read-a/synthesize/retry-1/batch-0')]`.

- monkeypatch 도달성  
  `.venv/bin/python -c '<m2 전역과 read_stage 전역을 각각 메모리 패치>'`  
  출력: `M2_PATCH_REACHES False`, `READ_STAGE_PATCH_REACHES True`; 마지막 출력: `PATCH_VERIFICATION_DONE True`.

- `python -I` provenance 경로 모형  
  `.venv/bin/python -I -c '<repo 선삽입·__path__·__file__ 검사>'`  
  마지막 출력: `PROVENANCE_PATHS_OK True`.

- 조기·최종 조립 대조  
  `.venv/bin/python -c '<decompose_only_spec vs assemble_spec · convergence.check>'`  
  마지막 출력: `CONVERGENCE pass [...]`.

- T-1 축 확인  
  `.venv/bin/python -c '<reader-rules convergence 축→policy 대조>'`  
  마지막 출력: `T1_LOCUS_IS_EXACT_MATCH False`.

- 실제 exact-match 주입 모형  
  `.venv/bin/python -c '<peer 독립항 복제 후 convergence.check>'`  
  마지막 출력: `COHERENT_EXACT_MATCH True`.

- 관문 변조 모형  
  `.venv/bin/python -c '<v5 G1~G6 + lane 병합/upstream action 변조>'`  
  출력: `MERGED_LANE_ROWS 10 (...)`, `UPSTREAM_ACTION_HALT (...)`; 마지막 출력: `MUTANTS_ACCEPTED True`.

- lane 병합 전수 값 대조  
  `.venv/bin/python -c '<정본 행 vs lane 병합 행 8,190칸>'`  
  마지막 출력: `MERGED_GRID_MISMATCHES 0 []`.

- 신설물 존재 여부  
  `for p in ...; do test -e ...; done`  
  마지막 출력: `ABSENT tools/check_failure_table.py`.

## [미검증]

- `generate.py`, manifest, `test_m24_failure_grid_golden.py`, `check_failure_table.py`는 아직 없어 실제 실행하지 못했다.
- read-only 규율 때문에 detached worktree 생성, 골든 기록, 전체 pytest, 관문 실행, 파일 생성형 실제 러너 통주는 하지 않았다.
- 검토 시작 시 HEAD는 요청대로 `4e1f05c`였다. 종료 직전 외부에서 HEAD가 `39a6438`로 바뀌어 `tests/test_tools_check_dispositions.py`, `tools/check_dispositions.py` 두 파일이 달라졌다. 이는 요청의 “HEAD가 다르면 전체 `engine contracts reader tests tools` diff 0” 전제를 깨므로 숨길 수 없다.
- 다만 T26 대상인 `engine/contracts/reader`, 지정된 READ 시험 파일들과 `tools/check_failure_table.py`는 `4e1f05c..39a6438` diff 0이고 작업트리는 clean이다. 해당 확인의 마지막 출력은 `0`이다.