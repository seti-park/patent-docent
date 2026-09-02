# 독립 감수 원문 — 재정 T26 집행 설계 v7 의 M1b 설계 도전(6차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v7/final.txt` 의 sha256 `5aa01ef2637283773d9d4d57b60245d0ecedd312722ef40f0d0bfd9942e238d0` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 19분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 6차 심사** — v6(5차 FAIL · Y-1~Y-5) → **v7** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`edabe28` · 5차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 2건(MED 2 · BLOCKER 0 · HIGH 0) · 새 재정 사항 0 · Y-1·Y-2·Y-4·Y-5 closed · Y-3 partially(Z-1) · B·V·N·W·X 전건 closed.**
값 8,190 칸은 여섯 번째로 일치. **Z-1**: G3 의 예산 등식이 타입을 안 봐 PyYAML `true`/`1.0` 이 `{1} == {True} == {1.0}` 로 통과하는데
런타임 `_retry_budget()` 과 존치 `test_m17` 은 `type is int` 로 거부 — 관문·런타임 판정이 갈린다. **Z-2**: T-7 ④ 가 manifest 의 `predicate` 를
`eval` 해 같은 manifest 의 `cells` 와 비교하는 **자기참조 오라클** — schema 비트로 바꾼 predicate+cells 동반 변조가 2,048칸·자기일관으로 통과.

지적 열거 = Z-1, Z-2

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§12** 에 있다.
둘 다 **수용**(공학 · 규율 11 ③) — **v8** 에 반영하고 7차 도전에 냈다. v8 = G3 에 `type(max_retries) is int` 를 등식 앞에(변조 ㉚㉛ · T-11 ④
직접 변조에 포함) · T-7 ④ 는 시험 코드의 **고정 식**으로 β 집합을 독립 산출하고 `exceptions` 길이·`id`·`rule`·`predicate` 문자열을 고정값과 대조.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

핵심 11행 격자와 8,190칸 값은 맞습니다. 그러나 G3가 `max_retries`의 YAML 타입을 고정하지 않아 관문을 통과하는 변조가 남고, β 도달 불능 표지 시험은 manifest가 선언한 술어를 manifest 자신으로 검산하는 자기참조 오라클입니다. 둘 다 공학 수정 사항이며 새 Owner 재정은 필요하지 않습니다.

## Y-1~Y-5 폐쇄 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| Y-1 | closed | T-1에는 peer 독립항 복제 → 수정한 `CheckContext`로 원 검사 재호출이라는 절차 하나만 남았다. 수동 finding 추가 문언은 없다. |
| Y-2 | closed | :533은 `failure_rows_for_checks(..., {"read.source-digest"})`, :733은 `failure_row_of_kind(..., "retry-repeat")`로 정확히 분리됐다. 실물 시험 의미와 일치한다. |
| Y-3 | partially | `1→2` 변조는 G3가 잡는다. 그러나 `true`·`1.0`은 `{1} == {True} == {1.0}`인 Python 집합 동치 때문에 적힌 G3 식을 통과한다. 런타임과 존치 시험은 타입을 거부한다(Z-1). |
| Y-4 | closed | 자기시험 총수 리터럴은 제거됐고 §2.7 열거와 동적 출력만 정본이다. 열거 자체는 ⑴~㉙다. |
| Y-5 | closed | T-12는 이제 “이 시험만 잡는다”가 아니라 관문과 독립적인 계약↔엔진 상수 다리라고 정확히 기술한다. |

## 지적 목록

### Z-1 · MED · 설계 §2.7 G3 · [read.yaml:233](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:233) · [read.py:754](/home/laptop/projects/patent-docent/engine/stages/read.py:754) · [test_m17_lanes.py:198](/home/laptop/projects/patent-docent/tests/test_m17_lanes.py:198)

G3의 Y-3 보수는 값의 집합 등식만 적고 `max_retries`의 타입을 규정하지 않습니다.

PyYAML에서:

- `max_retries: true` → `bool`
- `max_retries: 1.0` → `float`
- Python에서는 `{1} == {True}` 및 `{1} == {1.0}`가 모두 참

따라서 두 변조 모두 적힌 G3 식

```text
{n : action == retry(n) ∧ p ∈ points} == {max_retries(p)}
```

을 통과합니다. 반면 현재 `_retry_budget()`은 `type(value) is int`가 아니면 `RunnerContractError`를 내고, 존치 시험도 같은 타입 검사를 합니다. 즉 관문과 런타임의 계약 유효성 판정이 다시 갈립니다.

실측:

> `FINAL bool_and_float_pass_literal_G3_set_equality=True runtime_rejects=True preserved_test_rejects=True`

닫는 법:

- G3에 `type(point["max_retries"]) is int`를 명시한다. `isinstance(..., int)`는 `bool`을 받으므로 안 된다.
- 그 타입 검사를 예산 집합 등식보다 먼저 수행한다.
- 자기시험에 `max_retries: true`와 `max_retries: 1.0`을 각각 추가한다.
- T-11의 임시 YAML 직접 변조에도 둘 중 하나를 넣어 자기시험 구현 자체의 공허 통과를 막는다.

### Z-2 · MED · 설계 §2.8 manifest·T-7 ④⑤ · [T28 §3②:118](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:118)

β 표지 시험이 표지의 의미를 독립적으로 검증하지 않습니다.

T-7 ④는 `exceptions[0].predicate`를 manifest에서 읽어 `eval`하고, 그 결과를 같은 manifest의 `cells`와 비교합니다. 따라서 predicate와 cells를 함께 잘못 만들면 통과합니다. 예를 들어 `read.convergence` 대신 `read.schema` 비트를 쓰면:

- 잘못된 집합도 2,048칸
- `cell_count`도 2,048
- manifest predicate 재평가 결과와 manifest cells는 정확히 일치
- 8,190칸 `(조치, 라벨)` 값에는 영향 없음
- 하지만 T28이 명한 β 칸과는 다름

실측:

> `FINAL wrong_marker_count=2048 self_check=True equals_required_beta=False symmetric_difference=2048`

또한 T-7은 `exceptions`가 정확히 한 건인지, `id`·`rule`·`predicate`가 T28의 고정값인지 명시적으로 대조하지 않습니다. 총괄의 스크래치 오라클도 §2.8 문언상 8,190칸 값만 대조하므로 이 오류를 보완하지 않습니다.

닫는 법:

- `exceptions` 길이 == 1을 검사한다.
- `id == "T28-beta"`와 규칙 문언을 고정한다.
- 기대 셀은 manifest의 predicate를 사용하지 말고 시험 코드가 독립적으로 다음 식으로 산출한다.

```python
repeated == 1 and (
    mask & (1 << check_ids.index("read.convergence"))
) != 0
```

- 독립 산출 집합과 manifest `cells`를 양방향 비교하고 정확히 2,048칸인지 본다.
- manifest의 `predicate`를 보존하려면 위 고정 문자열과 정확히 같은지도 별도로 검사한다.
- B-0 생성기 단위 시험에 “schema 비트로 바꾼 predicate+cells 동반 변조”를 넣는다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회 |
| T26 §2⒜② 조치 격자·계약 순서 | covered | §2.2·§2.6. 전수 값 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | partially | 집합 등식과 출구 부분집합은 정확하다. 다만 G3 예산 결속이 타입 차원에서 런타임과 다르다(Z-1). |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | covered | §2.8·T-7. 값 자체는 8,190칸 전부 일치 |
| T26 §3③ 양방향 관문·세 심기 | partially | 원장 필수 세 심기는 있다. 그러나 G3가 유효성 변조 두 종을 통과시킨다(Z-1). |
| T26 §3④ 관문 계수 정정 | covered | 관문 7종과 역사적 정정 마커를 §2.7·§2.10에 반영 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | covered | §2.8·T-7, 직접 불일치 0 |
| T28 §3② β 표지 | partially | 요구 집합은 실측 2,048칸이나 T-7이 그 의미를 독립 검증하지 않는다(Z-2). |
| T28 §3③ 실제 러너 음성·양성 | covered | T-1의 실제 모듈 전역 주입과 T-2의 `/retry-1/` 3행이 실물과 정합 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3·승인 집합. `points: [early]` 유지 |
| T29 §3① 골든 id 12개 | covered | §2.8·T-7·T-12 |
| T29 §3② 진입 예외 반증 | covered | T-3가 `StageEnvironmentError`와 `_failure_verdict` 0회를 계측 |
| T29 §3③ input-digest 키·표지·halt·출구 재시도 제외 | covered | §2.4·G5 |
| T30 §3① kind 정확히 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9. `engine/` 호출자 실측 0 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 라운드 B 뒤 소라운드로 분리한 것은 원장과 맞습니다. T32를 그 소라운드에 합치는 것도 T32 §3⑤가 허용한 총괄 재량입니다. `screening_memos[].read_run` 무접촉 역시 맞습니다.

원장 밖 추가 요소인 `judged_at`, R8/R9, 미지 id fail-closed, provenance 검사, B-0, 헬퍼 이름, 승인 상수는 공학·운영 재량입니다. Z-1·Z-2도 새 값의 재정이 아니라 이미 정해진 값과 형식을 정확히 검사하는 보수입니다.

## B. 오늘의 표 불변

값 판정은 PASS입니다.

| 결과 | 직접 재계산 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| T28 β 술어 | 2,048 |
| v7 11행 모형↔HEAD 불일치 | 0 |

세 `StageError` 칸도 설계와 같습니다.

- `1024:1` — `read.lane-log-shape`
- `2048:1` — `read.lane-log-digest-value`
- `3072:1` — 두 lane-log id

§2.2 손검산에서 틀린 칸은 찾지 못했습니다.

R6와 `worst_status()`의 관계도 맞습니다. 현재 `worst_status()`는 미지 값을 `order.get(status, 0)`으로 처리하지만, 새 선택기는 모든 후보의 `terminal_action()`을 먼저 검증하도록 고정했습니다. 따라서 유효 구현에서는 미지 terminal이 [worst_status](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)에 도달하지 않습니다. 빈 후보도 `StageError`입니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β, convergence 출구 목록 제외, 부분집합 우선, 실제 모듈 패치와 0/3 레인 대조가 모두 선다. |
| B-2 | closed | 출구 12 id·8,190칸과 input-digest 진입 예외가 분리됐다. |
| B-3 | closed | `(조치, 라벨)` 값은 `99fad78` 구현에서 만들어 동결하고 B는 파일만 읽는다. Z-2는 값 골든이 아니라 β 표지의 별도 자기참조 결함이다. |
| B-4 | closed | 8·9행을 분리했고 등식에 `phases`를 섞지 않는다. |
| B-5 | closed | retry의 `then` 부재·retry인 `then`·비-retry의 `then`을 관문과 모든 도달 가능한 런타임 선택 경로가 거부한다. |
| B-6 | closed | kind 3종, upstream 호출자 0, deferred/test_bound |
| B-7 | closed | pytest와 관문 7종 전부 두 모드 |

### V-1~V-8

| 지적 | 판정 | 사유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 패치가 :1743 전역 조회에 닿는다. |
| V-2 | closed | `-I`, repo 선삽입, 모듈·패키지·계약·HEAD·clean 검사 |
| V-3 | closed | 재시도 회차 1과 레인 로그 3행을 구별 |
| V-4 | closed | phase 우주·형식·중복·부분집합 검사 |
| V-5 | closed | 판정점 `{early, exit}` 유일성·출구 12-id 우주 |
| V-6 | closed | predicate 자체는 실행 가능한 비트식이다. Z-2는 그 식의 의미를 독립 검증하지 않는 새 결함이다. |
| V-7 | closed | T-11⑤ terminal 어휘 상등 |
| V-8 | closed | 세 StageError와 격자/동률 순서 구별 |

### N-1~N-7

| 지적 | 판정 | 사유 |
|---|---|---|
| N-1 | closed | chdir 전 절대 `out` 고정 |
| N-2 | closed | 12개 phases를 재실측했고 R9 위반 0 |
| N-3 | closed | B-0 → 골든 커밋 → B 순서가 명시됨 |
| N-4 | closed | `_exit_retry_eligible()` 헬퍼와 함수 시험 |
| N-5 | closed | T-12 계약↔엔진 양방향 다리 |
| N-6 | closed | exit 필수·early iff |
| N-7 | closed | 다섯 세부가 구체화됨 |

### W·X 재개방 여부

| 지적 | 판정 |
|---|---|
| W-1~W-4 | 전건 closed |
| X-1 | closed — G1 골격·T-13·`test_m23`가 lane 행 병합을 거부 |
| X-2 | closed — T-1이 실제 `independent-count` 실패를 검사기 자체에서 발생시킴 |
| X-3 | closed — upstream action을 G1·T-13이 `reject-upstream`으로 고정 |

## D. 출구 convergence 도달 가능성

“조기 통과 → 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞습니다.

- `decompose_only_spec()`은 출구와 같은 [assemble_spec](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- [tail 반환](/home/laptop/projects/patent-docent/engine/stages/read.py:899)은 입력 `decompose` 객체를 그대로 싣고, 러너는 [조기에 사용한 `decomposes[canonical_run]`](/home/laptop/projects/patent-docent/engine/stages/read.py:1678)을 넘깁니다.
- 조기·출구 조립 모두 claims를 deepcopy한 뒤 같은 [rewrite_claims](/home/laptop/projects/patent-docent/engine/stages/read.py:532)를 적용합니다.
- 분해 payload가 재번호 입력의 첫 레인이므로 claims의 component 참조에는 같은 매핑이 적용됩니다.
- 후속 조립으로 바뀔 수 있는 `applicant_interest.material_id`는 수렴 6축이 읽지 않습니다.
- [convergence.check](/home/laptop/projects/patent-docent/reader/lib/convergence.py:86)의 6축은 청구항 수·element 문언/트리·종속 서명·addition 부착만 소비합니다.
- `peer_spec`을 읽는 코드는 `reader/lib` 전체에서 convergence의 두 자리뿐이었습니다.

직접 조립 결과는 claims 객체 전체는 다르지만 수렴축은 모두 통과했습니다.

> `FINAL normal_exit=pass injected=fail failed_axes=['independent-count']`

T-1의 주입 형태도 맞습니다. `read_stage.run_read_checks`를 패치하면 조기 수렴에는 닿지 않고 출구의 실제 호출점 :1743에만 닿습니다. peer 독립항 사본 추가는 검사기 자체가 `independent-count`만 fail로 기록하며, 다른 검사들은 `peer_spec`을 읽지 않아 실패 검사 집합은 `{read.convergence}`입니다.

새 출구 루프에서 부분집합 검사를 서명 비교보다 먼저 하면 convergence가 포함된 첫 실패에서 바로 탈출합니다. 따라서 `repeated_signature`는 서지 않고 `repeated=True ∧ convergence` 2,048칸은 실제 출구 경로에서 도달 불능입니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest의 표 밖 값은 T29 승인 |
| ③ | 맞다 | `judged_at` 이름은 원장이 v2에 위임 |
| ④ | 맞다 | T-11⑤가 terminal 두 벌을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 모든 도달 가능한 선택 경로가 `terminal_action()`을 통과 |
| ⑦ | 맞다 | 미지 id는 공식 12-id 밖 무효 입력의 fail-closed 처분 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③이 관문에 명시한 값 |
| ⑨ | 맞다 | 진입 가드가 early·exit `checks`를 실제 읽어 승인 상수와 대조하므로 `runner_reads`가 사실이다. |
| ⑩ | 맞다 | T-1은 peer 독립항 복제로 검사기 자체의 exact-match 축을 실패시킨다. |
| ⑪ | 틀렸다 | manifest 예시는 T28 술어 하나만 들지만, T-7은 그 술어를 독립 검증하지 않아 다른 2,048칸 표지를 통과시킨다(Z-2). |
| ⑫ | 맞다 | T32는 T31 소라운드에 합칠 수 있음 |
| ⑬ | 맞다 | 판정점·검사 우주 고정은 무효 계약 형식의 거부 |
| ⑭ | 맞다 | provenance 6검사와 `-I`는 설계상 충분하다. 실제 생성 실행은 미검증이다. |
| ⑮ | 맞다 | B-0 분리는 골든을 B 앞에 세운다. |
| ⑯ | 맞다 | R9는 실측 정본 국면을 대조하며 새 국면 입법이 아니다. |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이며 엔진·관문 상등 시험이 있다. |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격은 원장값의 독립 관문 오라클이고 T-13·골든·개별 시험이 보강한다. |
| ⑳ | 맞다 | 독립항 사본은 실측상 `independent-count`만 fail시킨다. |

새 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 설명 |
|---|---|---|
| G1 | covered | 정확한 11행·분할·순서·action·then·label·points를 고정 |
| G2 | covered | 양방향 차집합과 두 선언 배열의 형식·중복을 검사 |
| G3 | partially | 재시도 등식·승인 3/8 집합·`1→2`는 잡지만 `true`·`1.0` 예산을 통과시킨다(Z-1). |
| G4 | covered | 유령 phase·거짓 early·exit 누락을 거부 |
| G5 | covered | input-digest 표지·halt·points 부재·재시도 제외 |
| G6 | covered | 세 잘못된 terminal 형태를 거부하고 kind action은 G1이 고정 |

§2.7의 ⑴~㉙은 원장 필수 심기와 과거 반례를 포함합니다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 동시 일관 변조: ㉑
- 선언 중복: ㉒㉓
- lane 행 병합: ㉕
- upstream action 변경: ㉗
- `max_retries: 2`: ㉙

관문이 통과시키는 새 변조는 `max_retries: true`와 `max_retries: 1.0`입니다. 존치 pytest가 이를 잡더라도, Y-3가 요구한 관문 자체의 예산 결속에는 구멍이므로 Z-1입니다.

## G. sol-coder 결정 공백

Owner 재정 공백은 없습니다. 그러나 M3가 임의 선택할 공학적 자리가 하나 남습니다.

- G3를 적힌 Python 집합 등식 그대로 구현하면 `true`·`1.0`을 허용합니다.
- 현재 `_retry_budget()`과 `test_m17`을 따라 엄격 타입 검사까지 넣으면 거부합니다.
- 정본 `max_retries: 1`에서는 어느 구현도 전체 수락 명령을 통과하므로, §2.7 자기시험만으로는 선택을 강제하지 못합니다.

Z-2는 선택 공백이라기보다 잘못 고정된 검증 방식입니다. T-7을 문언 그대로 구현하면 β 술어가 틀려도 자기일관성만으로 통과할 수 있습니다.

하나라도 있으면 FAIL이라는 기준에 따라 발주 불가입니다.

## 검증 경로

- 시작 상태:

  `git status --short && git rev-parse --short HEAD && git diff --stat 35d7fa1 HEAD -- engine contracts reader tests tools`

  시작 HEAD 마지막 출력:

  > `35d7fa1`

- 검토 중 문서 전용 커밋 반입 뒤 종료 상태:

  `git status --short`와 `git diff --stat 35d7fa1 HEAD -- engine contracts reader tests tools`는 빈 출력, `git rev-parse --short HEAD`:

  > `edabe28`

- 기준 트리 불변:

  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`

  > `0`

- HEAD `_failure_verdict` 8,190칸 전수 호출 + v7 독립 11행 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 halt=6144 esc_null=1023 esc_repeat=1020 stage_error=3`

- G3 YAML 타입 변조:

  > `FINAL bool_and_float_pass_literal_G3_set_equality=True runtime_rejects=True preserved_test_rejects=True`

- β 자기참조 표지 변조:

  > `FINAL wrong_marker_count=2048 self_check=True equals_required_beta=False symmetric_difference=2048`

- R9·판정점 실측:

  > `FINAL exit_ids=12 unique=12 point_ids=['early', 'exit'] r9_violations=[]`

- 조기/출구 조립 및 T-1 주입:

  > `FINAL normal_exit=pass injected=fail failed_axes=['independent-count']`

- `peer_spec` 소비 위치 AST 전수:

  > `FINAL peer_spec_attribute_reads=[('reader/lib/convergence.py', 94), ('reader/lib/convergence.py', 105)]`

- `CheckContext` 필드 실측:

  > `FINAL check_context_fields=('spec', 'source_text', 'rules', 'schema', 'peer_spec', 'prior_spec')`

- 후속 1회차 레인 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-dependent', 'ground-independent', 'synthesize'] all_retry1=True`

- 격리 import 경로 모형:

  > `FINAL isolated_current_tree_provenance_paths_ok=True`

- 신설물 부재:

  > `ABSENT tools/check_failure_table.py`

첫 전수 비교 실행에서는 도전자 모형이 반복 kind 후보를 계약 위치 4가 아니라 후보 배열 끝에 붙인 뒤 정렬하지 않아 거짓 불일치를 냈습니다. 계약 행 위치로 정렬해 재실행한 결과가 위 `mismatches=0`입니다.

## [미검증]

- `generate.py`, manifest, `test_m24_failure_grid_golden.py`, `check_failure_table.py`는 아직 없어 실제 실행하지 못했습니다.
- read-only 규율 때문에 detached worktree 생성·골든 기록·전체 pytest·관문 plain/`-O`·파일 생성형 T-1/T-2 통주는 실행하지 않았습니다.
- `99fad78` 실제 생성 절차는 실행하지 못했습니다. `99fad78..HEAD -- engine contracts reader` diff 0과 현재 트리의 `-I` 패키지 경로만 검증했습니다.
- G1~G6은 아직 구현물이 없으므로 설계에 적힌 술어를 메모리 모형에 대입해 변조를 검증했습니다.