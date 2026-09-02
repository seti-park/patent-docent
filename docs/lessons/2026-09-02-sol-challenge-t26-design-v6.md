# 독립 감수 원문 — 재정 T26 집행 설계 v6 의 M1b 설계 도전(5차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v6/final.txt` 의 sha256 `6fe39a8e9a62ae6d58336129518161ee72f9bdc0ac9f9012b5596b8db41e8de4` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 25분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 5차 심사** — v5(4차 FAIL · X-1~X-3) → **v6** 에 대한 것. 도전 중
총괄이 문서 전용 커밋(`35d7fa1` · 4차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 5건(HIGH 1 · MED 2 · LOW 2 · BLOCKER 0) · 새 재정 사항 0 · X-1·X-3 closed · X-2 partially(Y-1) · B·V·N·W 전건 closed(W-4 만 Y-4 로 재개방).**
값 8,190 칸은 다섯 번째로 일치. 다섯 중 **둘은 총괄이 v6 을 패치하다 남긴 잔재**다 — **Y-1**: T-1 에 폐기된 v5 지시(`element-set` finding 수동 추가)와
새 지시(peer 독립항 복제)가 공존 · **Y-4**: 계수 리터럴(24/28)이 §0·§2.10·§2.11 에 다시 들어가 W-4 가 재발. 나머지 — **Y-2**: `test_m21`
:533 은 원천 다이제스트 행 시험인데 `retry-repeat` 조회로 바꾸라고 적었다 · **Y-3**: 관문이 `max_retries` 를 보지 않아 `early.max_retries: 2`
가 관문 관측면 불변으로 통과(존치 `test_m17_lanes.py:164` 가 잡는다 — 관문 자체의 구멍) · **Y-5**: T-12 의 「이 시험만 잡는다」 문언이 v6 에서 거짓.

지적 열거 = Y-1, Y-2, Y-3, Y-4, Y-5

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§11** 에 있다.
다섯 전부 **수용**(문서 정밀도·관문 한 항 · 규율 11 ③) — **v7** 에 반영하고 6차 도전에 냈다. v7 은 T-1 행을 한 절차만 남겨 다시 썼고,
계수 리터럴을 전부 걷어냈으며(§2.7 열거만 정본 · 관문 출력이 센다), G3 에 예산 결속(`{n} == {max_retries}`)을 더했다. 총괄 자기 점검 —
**패치식 개정이 두 판 연속으로 잔재를 남겼다**(W-4 → Y-4 · X-2 → Y-1). v7 은 개정 뒤 모순 탐색 grep(폐기 문구 · 계수 리터럴 · 좌표 매핑)을 돌렸다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## X-1~X-3 폐쇄 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| X-1 | closed | G1의 `APPROVED_FAILURE_TABLE` 정확 일치, T-13의 11행·lane singleton 확인, `test_m23`의 서로 다른 행 확인, 변조 ㉕가 병합을 거부한다. |
| X-2 | partially | 의도한 새 주입은 실측상 정확히 `independent-count`만 실패시킨다. 그러나 T-1 앞부분에 v5의 “`original(ctx)` 뒤 `element-set` finding 수동 추가” 지시가 그대로 남아, 바로 뒤의 “손으로 더하지 않는다”와 충돌한다(Y-1). |
| X-3 | closed | G1이 `upstream-defect.action == reject-upstream`을 고정하고 T-13·변조 ㉗이 이를 독립 확인한다. |

## 지적 목록

### Y-1 · HIGH · 설계 §2.9 T-1

T-1 안에 폐기된 X-2 주입과 새 주입이 동시에 적혀 있다.

- 앞 문장: `original(ctx)` 실행 뒤 `element-set` finding을 손으로 추가.
- 뒤 문장: finding을 손으로 추가하지 않고 변형한 `peer_spec`으로 원 검사를 다시 실행.

뒤 문장에 “대체”라고 적혀 있어 의도는 읽히지만, M3가 앞 문장을 구현하면 X-2의 자기모순 판정서가 그대로 재현된다. 따라서 X-2는 완전 폐쇄가 아니다.

닫는 법: 앞의 `original(ctx)` 후 `element-set` finding을 추가한다는 문장 전부를 삭제하고, 다음 순서 하나만 남겨라.

1. `peer_spec = deepcopy(ctx.peer_spec)`
2. 첫 독립항 사본을 `claims.independent`에 추가
3. 나머지 `CheckContext` 필드를 보존해 `original(modified_ctx)` 호출
4. `read.convergence`만 fail, `independent-count` 축 fail, `/retry-` 0행을 대조

### Y-2 · MED · 설계 §2.9 「개정」 · [test_m21:533](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:533) · [test_m21:730](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:730)

`test_m21`의 `:533/:733 → failure_row_of_kind(..., "retry-repeat")` 지시는 첫 좌표에 대해 틀렸다.

- :533은 출구 원천 재독 실패 시험이며 `read.source-digest` 검사 행을 찾아야 한다.
- :733 부근만 반복 처분 행이므로 `kind: retry-repeat` 조회가 맞다.

그대로 구현하면 source-digest 결과의 기대 라벨을 반복 행 라벨로 읽어 정상 `halt, None` 결과와 충돌한다. M3는 지시를 어기거나 시험 실패를 받아야 한다.

닫는 법:

- :533은 `failure_rows_for_checks(contract, {"read.source-digest"})`로 정확히 한 행을 조회한다.
- :733은 `failure_row_of_kind(contract, "retry-repeat")`를 사용한다고 각각 분리해 적어라.

### Y-3 · MED · 설계 §2.7 G3 · [read.yaml:233](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:233) · [read.py:754](/home/laptop/projects/patent-docent/engine/stages/read.py:754)

G1~G6은 `retry_budget.points[].max_retries`를 보지 않는다. `early.max_retries: 1 → 2` 변조는 명시된 모든 관문 관측값을 그대로 유지하면서 런타임 예산을 2로 바꾼다.

실측:

> `FINAL g1_g6_observed_projection_unchanged=True runtime_budget_changed=True`

존치 시험 [test_m17_lanes.py:164](/home/laptop/projects/patent-docent/tests/test_m17_lanes.py:164)이 계약의 `retry(n)`과 `max_retries` 불일치를 잡으므로 전체 수락 체계의 완전 무방비는 아니다. 그러나 발주문은 “관문이 통과시키는 변조” 자체를 지적으로 보라고 했고, G3가 재시도 결속을 담당한다고 주장한다.

닫는 법: G3가 각 판정점에 대해 `points`를 신고한 `retry(n)`의 모든 `n` 집합이 정확히 `{max_retries}`인지 검사하게 하고, `early.max_retries: 2` 변조를 self-test에 추가하라.

### Y-4 · LOW · 설계 §0 · §2.7 · §2.10 · §2.11

W-4의 계수 충돌이 다시 열렸다.

- §0·§2.7·§2.11: 28종
- §2.10: “W-4 — 지금 24”

열거된 변조는 실제로 ⑴~㉘의 28종이다. “§2.7 한 곳만 정본”이라는 선언도 §0·§2.10·§2.11이 숫자를 다시 적어 스스로 위반한다.

닫는 법: §2.7의 실제 열거만 정본으로 남기고 다른 절의 `24`·`28` 리터럴을 모두 제거하라. 수락 문언은 “§2.7 열거 전건” 또는 관문이 출력한 동적 계수를 가리켜야 한다.

### Y-5 · LOW · 설계 §2.9 T-12

T-12의 “유령 id + 유령 행은 G1~G6을 모두 통과하며 이 시험만 잡는다”는 사실 주장이 v6에서는 더 이상 맞지 않는다. 유령 실패 행을 추가하면 11행 `APPROVED_FAILURE_TABLE`과 달라져 G1이 즉시 거부한다.

T-12 자체의 계약↔엔진 상수 다리는 여전히 유효하고 필요하다. 잘못된 것은 “이 시험만 잡는다”는 설명이다.

닫는 법: 해당 예시와 “이 시험만”을 삭제하고, T-12의 목적을 “관문 YAML 오라클과 독립적인 계약↔엔진 상수 다리”로 고쳐라.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회 |
| T26 §2⒜② 조치 격자·계약 순서 | covered | §2.2·§2.6. 전수 값 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | G2/G3, 승인 3/8 집합, `_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | covered | §2.8 골든 절차·T-7. 직접 8,190칸 일치 |
| T26 §3③ 양방향 관문·세 심기 | covered | 행 없는 검사 ⑴, 검사 없는 행 ⑵, 목록↔행 불일치 ⑶⑷. 단 관문 자체의 추가 구멍 Y-3 |
| T26 §3④ 관문 계수 정정 | covered | 관문 총수 7과 4→5→6→7 정정 지시 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | covered | §2.8·T-7, 직접 불일치 0 |
| T28 §3② β 표지 | covered | 실행 가능한 술어·2,048칸 |
| T28 §3③ 실제 러너 음성·양성 | partially | 의도한 새 주입은 맞지만 T-1에 폐기 지시가 공존(Y-1) |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3·승인 집합 |
| T29 §3① 골든 id 12개 | covered | §2.8·T-7·T-12 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 키·표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 정확히 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9; `engine/` 호출자 실측 0 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |
| T26 §2⒝ / T22 전용 두 행 | covered | G1·T-13·`test_m23`·변조 ㉕ |
| T31·T32 범위 분리 | covered | B 뒤 소라운드 및 T32 병합은 T31/T32가 허용. `screening_memos[].read_run` 무접촉 |

원장 밖 추가 요소 중 `judged_at`, R8/R9, 미지 id fail-closed, provenance 검사, B-0, helper 이름, 승인 상수는 공학·운영 재량이다. 새 Owner 재정이 필요한 값은 찾지 못했다.

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
| v6 모형↔HEAD 불일치 | 0 |

세 `StageError` 칸도 정확하다.

- `1024:1`: `read.lane-log-shape`
- `2048:1`: `read.lane-log-digest-value`
- `3072:1`: 두 lane-log id

§2.2 손검산에서 새로 틀린 칸은 찾지 못했다.

R6와 `worst_status()`의 관계도 맞다. 새 선택기는 후보 전부에 `terminal_action()`을 먼저 적용하므로 미지 terminal은 [worst_status의 `order.get(..., 0)`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)에 도달하지 않는다. 빈 후보도 `StageError`로 닫는다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β 선택·출구 convergence 제외·부분집합 우선은 확정됨. Y-1은 새 시험 문언 충돌 |
| B-2 | closed | 출구 12 id·8,190칸과 input-digest 진입 경로 분리 |
| B-3 | closed | 값은 `99fad78` 구현·계약에서 생성되고 B는 동결 manifest만 읽음 |
| B-4 | closed | 8·9행 분리, 등식에 `phases`를 섞지 않음 |
| B-5 | closed | `then` 없는 retry, retry인 `then`, 비-retry의 `then`을 관문·런타임 모두 거부 |
| B-6 | closed | kind 3종, upstream 호출자 0, deferred/test_bound |
| B-7 | closed | pytest와 7개 관문 모두 두 모드 |

### V-1~V-8

전건 `closed`.

| 지적 | 판정 | 핵심 근거 |
|---|---|---|
| V-1 | closed | `read_stage.run_read_checks` 패치가 러너 전역에 도달 |
| V-2 | closed | `-I`, repo 선삽입, 모듈·패키지·계약·HEAD·clean provenance |
| V-3 | closed | `/retry-1/` 3행·세 task |
| V-4 | closed | phase 우주·형식·중복 검사 |
| V-5 | closed | 판정점 `{early, exit}` 유일성·출구 12-id 우주 |
| V-6 | closed | 실행 가능한 비트 predicate |
| V-7 | closed | T-11⑤ terminal 어휘 상등 |
| V-8 | closed | 세 StageError 및 두 순서 구별 |

### N-1~N-7

| 지적 | 판정 | 사유 |
|---|---|---|
| N-1 | closed | chdir 전 절대 `out` |
| N-2 | closed | 12개 phases 실측·R9 통과 |
| N-3 | closed | B-0 → 골든 커밋 → B |
| N-4 | closed | `_exit_retry_eligible` 명명·함수 시험 |
| N-5 | closed | T-12 다리는 존치. 다만 예시 설명은 Y-5로 낡음 |
| N-6 | closed | exit 필수·early iff |
| N-7 | partially | 나머지 세부는 닫혔으나 T-1 wrapper 형태가 두 상반된 문장으로 다시 갈림(Y-1) |

### W-1~W-4 재개방 여부

| 지적 | 판정 |
|---|---|
| W-1 | closed |
| W-2 | closed |
| W-3 | closed |
| W-4 | open — 24/28 계수 충돌 재발(Y-4) |

## D. 출구 convergence 도달 가능성

“조기 통과 → 출구 convergence 실패는 유효 레인 페이로드만으로 도달 불능”이라는 주장은 맞다.

- `decompose_only_spec()`은 [같은 `assemble_spec()`을 호출](/home/laptop/projects/patent-docent/engine/stages/read.py:980)한다.
- tail은 입력 `decompose` 객체를 그대로 돌려주며, 러너는 같은 `decomposes[canonical_run]`을 전달한다.
- 양쪽 조립 모두 claims를 deepcopy한 뒤 [같은 `rewrite_claims()`](/home/laptop/projects/patent-docent/engine/stages/read.py:528)를 적용한다.
- 분해 payload가 항상 재번호 투입의 첫 레인이므로 component 참조의 재번호도 동일하다.
- 후속 조립으로 달라지는 `applicant_interest.material_id`는 수렴축이 읽지 않는다.
- [convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)의 6축은 청구항 수, element 문언·트리, 종속 서명, addition 부착만 소비한다.

직접 조립 결과:

> `EXIT_FROM_SAME_DECOMPOSE pass [...]`  
> `CLAIMS_OBJECT_EQUAL False`

따라서 제시할 “출구에서만 실패하는 올바른 레인 페이로드”는 없다.

의도한 T-1의 검사층 주입은 타당하다. 독립항 사본을 같은 id·문언으로 복제하면 리스트 길이만 늘고 집합형 축은 중복을 소거한다. 실측 결과:

> `FINAL injected_status=fail failed_axes=['independent-count'] other_failed=[]`

또한 `peer_spec`을 읽는 검사는 `read.convergence` 하나뿐이므로 실패 검사 집합도 `{read.convergence}` 그대로다. 다만 Y-1의 폐기 문장을 삭제해야 T28 §3③을 무조건 충족한다.

부분집합 검사를 서명 비교보다 먼저 하면 convergence가 처음 관측된 회차에서 즉시 탈출하므로 `repeated_signature`가 설정되지 않는다. β 표지 2,048칸은 맞다.

## E. 자기 신고 ①~⑳

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest 표 밖 값은 T29 승인 |
| ③ | 맞다 | `judged_at` 이름은 원장이 위임 |
| ④ | 맞다 | T-11⑤가 두 terminal 집합을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 모든 도달 가능한 선택 경로가 `terminal_action()`을 통과 |
| ⑦ | 맞다 | 미지 id는 공식 12-id 영역 밖 무효 입력의 fail-closed 처분 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 진입 가드가 early·exit 목록을 실제 읽고 승인 상수와 대조 |
| ⑩ | 틀렸다 | T-1에 폐기된 수동 `element-set` 지시가 남아 있음(Y-1) |
| ⑪ | 맞다 | 표지는 T28 술어 하나에만 둠 |
| ⑫ | 맞다 | T32를 T31 소라운드에 합칠 수 있음 |
| ⑬ | 맞다 | 판정점·검사 우주 고정은 무효 계약의 형식 거부 |
| ⑭ | 맞다 | 설계된 6검사와 `-I`는 provenance에 충분함. 실제 생성 실행은 미검증 |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 먼저 세움 |
| ⑯ | 맞다 | R9는 실측한 정본 국면의 대조 |
| ⑰ | 맞다 | 3/8 승인 집합은 원장값이며 T-4·T-11⑥이 동반 표류를 보강 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격 상수는 계약을 대조하는 독립 관문 오라클이다. 일부 무효과 순서의 배치는 공학적 보존이지만 새 판정값은 만들지 않음 |
| ⑳ | 맞다 | 독립항 사본은 실측상 `independent-count`만 fail; 검사 id는 convergence 하나 |

## F. 관문 G1~G6

| 관문 | 판정 | 설명 |
|---|---|---|
| G1 | covered | 정확한 11행·분할·순서·action·then·label·points로 X-1/X-3 차단 |
| G2 | covered | 양방향 차집합과 각 선언 배열의 형식·중복 검사 |
| G3 | partially | 검사 집합 등식·3/8 승인 집합은 맞으나 `max_retries`↔`retry(n)` 수치 결속을 보지 않음(Y-3) |
| G4 | covered | 유령 phase·거짓 early·exit 누락 차단 |
| G5 | covered | input-digest 표지·halt·points 부재·재시도 제외 |
| G6 | covered | 세 잘못된 terminal 형태를 거부하며 kind action은 G1이 고정 |

열거된 28종은 원장 필수 심기를 모두 포함한다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- W-1 동시 일관 변조: ㉑
- 선언 중복: ㉒㉓
- lane 행 병합: ㉕
- upstream action 변경: ㉗

새 통과 변조는 `early.max_retries: 1 → 2`다. G1~G6이 관찰하는 면은 그대로인데 `_retry_budget()`의 반환은 2가 된다. 존치 pytest가 잡더라도 관문 자체의 구멍이므로 Y-3이다.

비-id 필드의 결속은 다음과 같다.

- `checks_before_exit[].criterion`, `implemented_by`, `ruleset`, `phase_meaning` 등은 러너가 읽지 않는다. 문서·존치 시험 결속이다.
- `repairs`도 러너가 분기값으로 읽지 않지만 T-1/T-2 계열 시험이 실제 task 집합과 대조한다.
- `max_retries`는 러너가 직접 읽고 존치 `test_m17`이 `retry(n)`과 대조한다.
- `escalate_on_repeat`는 산문이고 실제 반복 판정은 코드·kind 행·시험에 결속된다.
- `checks`는 새 가드와 실제 출구 적격 판정이 읽는다.

## G. M3 결정 공백

새 Owner 재정 공백은 없다. 그러나 M3가 그대로는 구현할 수 없는 공학적 충돌이 남아 있다.

1. T-1에서 수동 `element-set` finding과 변형 peer 재실행 중 어느 지시를 따를지 골라야 한다(Y-1).
2. `test_m21:533`을 지시대로 `retry-repeat` kind 조회로 바꾸면 시험 의미가 깨지므로, M3가 임의로 source-digest 조회로 교정해야 한다(Y-2).
3. self-test 계수가 24와 28로 갈려 W-4와 같은 선택을 다시 요구한다(Y-4).

하나라도 있으면 FAIL이라는 기준에 따라 발주 불가다.

## 검증 경로

- 기준 상태 및 이동 확인  
  `git status --short && git rev-parse --short HEAD && git rev-parse HEAD^{tree}`  
  시작 출력: `39a6438`, 트리 `1c18966d94b842eb6dc05ed81c1a6936b17dfaf6`. 검토 중 문서 반입 뒤 마지막 출력:  
  > `FINAL head=35d7fa1 tree=149836c19f55b164259b18cd3875ed6013bfe914 clean=yes`

- 불변 경로 확인  
  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`  
  > `0`

- HEAD `_failure_verdict` 8,190칸 전수 호출  
  `.venv/bin/python -c '<12 id × mask 1..4095 × repeated 0/1>'`  
  > `FINAL total=8190 beta=2048 mismatches=0 halt=6144 esc_null=1023 esc_repeat=1020 stage_error=3`

- v6 11행 독립 모형 대조  
  `.venv/bin/python -c '<행 위치로 tie-break한 v6 모형>'`  
  > `FINAL corrected_model_cells=8190 mismatches=0`

- R8/R9 실측  
  `.venv/bin/python -c '<retry point·12 phases 전건 대조>'`  
  > `FINAL exit_ids=12 unique=12 early=['read.claim-inventory', 'read.convergence', 'read.dependency-parse'] violations=[]`

- 조기·출구 조립 및 X-2 주입  
  `.venv/bin/python -c '<decompose_only_spec·assemble_spec·peer 독립항 복제>'`  
  > `FINAL injected_status=fail failed_axes=['independent-count'] other_failed=[]`

- 후속 1회차 레인 계획  
  `.venv/bin/python -c '<plan_grounding + plan_synthesis, attempt=1>'`  
  > `FINAL retry_lane_rows=3 tasks=['ground-dependent', 'ground-independent', 'synthesize'] all_retry1=True`

- monkeypatch 도달성  
  `.venv/bin/python -c '<m2 전역과 read_stage 전역을 각각 메모리 치환 후 복구>'`  
  > `FINAL read_stage_patch_reaches=True m2_patch_reaches=False restored=True`

- 격리 import provenance 모형  
  `.venv/bin/python -I -c '<repo 선삽입·package path·module file 검사>'`  
  > `FINAL isolated_provenance_paths_ok=True`

- G3 예산 변조  
  `.venv/bin/python -c '<early.max_retries 1→2 · G1~G6 관측면/런타임 비교>'`  
  > `FINAL g1_g6_observed_projection_unchanged=True runtime_budget_changed=True`

- 존치 시험의 보완 여부  
  `.venv/bin/python -c '<test_m17 points_binding 식 재현>'`  
  > `FINAL preserved_test_m17_would_reject=True violations={'early': ({1}, {2})}`

- 신설물 부재 확인  
  `for p in generate.py manifest.json test_m24_failure_grid_golden.py check_failure_table.py; do ...; done`  
  마지막 출력:  
  > `ABSENT tools/check_failure_table.py`

초기 전수 비교 스크립트 한 번은 반복 kind 후보를 계약 위치 4가 아니라 append 위치로 tie-break한 도전자 모형 오류로 거짓 불일치 1,020을 냈다. 후보를 계약 행 위치로 정렬하도록 바로잡은 재실행 결과가 위 `mismatches=0`이다.

## [미검증]

- `generate.py`, manifest, `test_m24_failure_grid_golden.py`, `check_failure_table.py`는 아직 없어 실제 실행하지 못했다.
- read-only 규율 때문에 detached worktree 생성, 골든 기록, 전체 pytest, 관문 plain/`-O`, 파일 생성형 T-1/T-2 실러너 통주는 실행하지 않았다.
- v6 메모는 리포 파일이 아니라 첨부 전문으로만 읽었다.
- 검토 중 HEAD가 `39a6438 → 35d7fa1`로 이동했지만 이는 v5 감수 원문·처분 문서 반입이다. 종료 시 작업 트리는 clean이고 `99fad78..HEAD -- engine contracts reader` diff는 0이다.