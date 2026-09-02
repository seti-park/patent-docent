# 독립 감수 원문 — 재정 T26 집행 설계 v15 의 M1b 설계 도전(14차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v15/final.txt` 의 sha256 `490152e94d78996f6c4463f2e1ee63f213a25aa19ffc58ec6367c6f295c8ddc7` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 20분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 14차 심사** — 설계 **v15** 에 대한 것. 도전 중 총괄이 문서 전용 커밋을
넣을 수 있음을 발주문이 고지했고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다.

**판정 = FAIL · 지적 4건(HIGH 2 · MED 1 · LOW 1) · 새 재정 사항 0 · AG-2 closed · AG-1 partially.** 값 8,190 칸은 열네 번째로 일치. **AH-1**: 최상위 manifest 의 타입 제약 부재(`[]` 를 넘기면 `.keys()` 예외 · 타입과 키 집합이 한 ID 에 합쳐지거나 문서 밖 진단) · **AH-2**: `expected_counts.keys.exact` 가 `cells` 재계산에 의존하는데 DAG 는 `.eq` 만 `cells` 뒤로 → 셀 sentinel 변조가 두 ID 를 함께 떨어뜨림 · **AH-3**: `exception.cell_count.eq` 정의가 둘(`== len(cells) == 2048` vs 고정값) · **AH-4**: §1 import 좌표 오류(`:33 import test_m2_read as m2`). v16 = `manifest.type` ID + DAG 뿌리 · `keys.exact` 를 고정 키 집합으로 · `cell_count == 2048` 단일화 · 좌표 정정.

지적 열거 = AH-1, AH-2, AH-3, AH-4

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§20** 에 있다.
전부 **수용**(공학 · 규율 11 ③) — 다음 판에 반영했다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## AG-1·AG-2 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AG-1 | **partially** | 13차가 직접 요구한 `exception.item.type`, path 원소 문자열, 셀 sentinel, 실제 count ID 전개, `subset_of_cells` 제거는 반영됐다. 그러나 최상위 manifest 타입 제약이 빠졌고(AH-1), `cells → expected_counts` 의존성이 DAG에서 누락됐으며(AH-2), `cell_count` 제약 정의가 T‑V와 충돌한다(AH-3). 따라서 “제약 하나 = ID 하나 = 정확히 한 진단”은 아직 서지 않는다. |
| AG-2 | **closed** | G1·T-13이 모든 11행에 `condition`·`note`를 필수 비공 문자열로 요구한다. HEAD 현행 10행도 전부 두 필드를 가진다고 실측했다. `prose_only`는 러너 비소비 분류이므로 존재·형식 검증과 충돌하지 않는다. |

## 지적 목록

### AH-1 · HIGH · 설계 §2.8 검증기·T‑V·선행조건 DAG

최상위 manifest의 독립 타입 제약이 없다.

`validate_manifest(manifest: dict, ...)`의 타입 힌트는 런타임 전제 검사가 아니다. JSON 최상위가 `[]`이면 호출자는 그대로 list를 넘긴다. 그런데 T‑V에는 `top.keys.exact`만 있고 `manifest.type`이 없다.

따라서 M3는 다음 중 하나를 임의 선택해야 한다.

- `.keys()` 호출 실패를 예외로 방치
- list를 `top.keys.exact`로 보고하여 타입과 키 집합 제약을 한 ID에 합침
- 문서에 없는 별도 타입 진단을 추가

첫째는 “위반 목록을 반환”한다는 함수 계약을 깨고, 둘째는 AG-1의 독립 제약 규칙을 깨며, 셋째는 `CONSTRAINT_IDS == T‑V ID 집합`을 깨뜨린다. `exceptions[0]`에 `exception.item.type`을 추가한 논리와 같은 결함이 최상위에 남았다.

닫는 법: `manifest.type` ID와 `manifest=[]` 단일 변조를 추가하고 DAG를 `manifest.type → top.keys.exact → 각 최상위 필드`로 시작해야 한다.

### AH-2 · HIGH · 설계 §2.8 `expected_counts` 검사 항목·T‑V `cells.value.*`·DAG

`expected_counts.keys.exact`는 `cells`에서 조치/라벨 키를 재계산하는 제약인데, DAG는 `.eq`만 “`cells` 층 전부 통과 후”로 둔다. `keys.exact`의 `cells` 선행조건이 빠졌다.

예를 들어 T‑V의

```text
cells["1024:1"] = "__bogus__"
```

변조는 목표상 `cells.value.sentinel` 하나만 보고해야 한다. 그러나 문서대로 `expected_counts.keys.exact`를 동시에 평가하면 재계산 키에 `__bogus__`가 추가되어 그 ID도 함께 실패하거나, 비정상 sentinel 처리 중 예외가 난다. `cells.value.action_vocab`·`label_type` 변조도 같은 문제를 가진다.

즉 올바른 검증기를 문언 그대로 구현해도 T‑V의 `set(reported_ids) == {target}`가 깨진다.

닫는 법: `expected_counts.keys.exact`와 모든 `.eq`를 `cells.type`, `cells.keys.exact`, 모든 셀 값 제약의 성공 뒤로 옮겨야 한다. 또는 `keys.exact`를 `COUNT_KEY_SLUGS`의 고정 키 집합과 대조하는 독립 제약으로 재정의하고 “cells에서 재계산” 문언을 삭제해야 한다.

### AH-3 · MED · 설계 §2.8 exceptions 검사 항목·T‑V `exception.cells.unique`·DAG

`exception.cell_count.eq`의 정의가 두 개다.

- 검사 항목: `cell_count == len(cells) == 2048`
- T‑V 설명: `cell_count.eq`는 `len(cells)`가 아니라 고정값 2048과 비교하므로, 셀 중복 변조에서 깨지지 않는다.
- DAG: `cell_count`와 `cells`를 독립 가지로 둔다.

T‑V의 첫 셀 복제 변조는 `cell_count=2048`, `len(cells)=2049`이므로 전자의 연쇄 등식은 거짓이고 `exception.cells.unique`와 `exception.cell_count.eq`가 함께 실패한다.

실측 계산:

> `FINAL target_only_if_fixed=True prose_cell_count_eq=False`

닫는 법: 다음 중 하나로 단일화해야 한다.

- `exception.cell_count.eq := cell_count == 2048`만 검사하고 길이 일치는 `cells.unique + cells.set`이 함의한다고 명시하거나,
- `cell_count.eq`를 전체 `exception.cells` 가지 성공 뒤에만 평가하도록 DAG를 바꾼다.

### AH-4 · LOW · 설계 §1 시험 좌표

설계는 `tests/test_m21_retry_budget_by_judgment_point.py`가 `import tests.test_m2_read as m2`를 쓴다고 적었지만 실물은 tests 디렉터리를 `sys.path`에 넣은 뒤 다음처럼 import한다.

> `33:import test_m2_read as m2  # noqa: E402`

모듈이 시험 모듈이라는 결론은 맞지만 좌표와 import 이름은 틀렸다.

닫는 법: §1을 `tests/test_m21_retry_budget_by_judgment_point.py:33 import test_m2_read as m2`로 고친다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 ID 키·조건 설명 존치 | covered | §2.1·§2.2·G1·T-13. AG-2 폐쇄. |
| T26 §2⒜② 조치 격자·계약 동률 순서 | covered | §2.2·§2.6 `select_failure_row`; 전수 불일치 0. |
| T26 §2⒜③ 완전성·정확 등식·실제 부분집합 | covered | R2·R8·R9, §2.3, G2~G4. `phases`로 등식을 약화하지 않는다. |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11. |
| T26 §3② 오늘 표 불변 | **partially** | 값 모델과 T‑7 런타임 대조는 맞지만 골든 검증 명세가 AH-1~AH-3으로 자기일관적이지 않다. |
| T26 §3③ 양방향 관문·세 필수 심기 | covered | §2.7 ⑴·⑵·⑶/⑷/㉑. |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10의 7관문 정정 마커. |
| T26 §3⑤ 전수·전 관문 2모드 | covered | §2.11에 pytest 및 7관문 plain/`-O`. |
| T28 §3① 8,190칸 값 불변 | **partially** | 전수 값은 일치하지만 해당 골든의 필수 검증기/T‑V 구현에 AH-1~AH-3 공백이 있다. |
| T28 §3② β 표지 2,048칸 | **partially** | 술어·집합은 정확하다. 다만 exception 구조의 exact-one 수락 계약이 AH-1·AH-3으로 불완전하다. |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T‑1/T‑2. 패치 대상·3개 retry-1 레인이 실물과 맞는다. |
| T28 §3④ convergence 제외·등식 | covered | §2.3·출구 루프·G3. |
| T29 §3① 골든 12 ID 정확 | covered | §2.8 `check_ids` 제약·T‑7·T‑12. |
| T29 §3② 진입 예외 반증 | covered | T‑3. |
| T29 §3③ 진입 표지·halt·출구 재시도 제외 | covered | §2.4·G5. |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1. |
| T30 §3② `checks` xor `kind` | covered | R4·G1. |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T‑9. 호출자 0 실측. |
| T30 §3④ SPEC 문서화 | covered | §2.10. |

T31을 B 뒤 소라운드로 미룬 것은 원장과 일치한다. T32를 그 소라운드에 합치는 것도 T32 §3⑤가 허용한다. `screening_memos[].read_run` 무접촉 판단도 맞다.

원장 밖 요소인 `judged_at`, 미지 ID fail-closed, 승인 상수, provenance 검사, B‑0 분리, 엄격한 진단 ID는 공학적 집행 또는 이미 정해진 값을 기록하는 장치다. 새 Owner 재정은 필요 없다. AH-1~AH-3은 설계자가 고쳐야 할 공학 결함이다.

## B. 오늘의 표 불변

8,190칸 전수 결과:

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v15 모형 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`이다.

설계 §2.2 손검산과 §3 대표 칸에서 틀린 출력 칸은 찾지 못했다. 수식도 정확하다.

- schema/source 중 하나 이상 포함: `(4095−1023)×2 = 6144`
- 둘 다 없고 `repeated=0`: `1023`
- 둘 다 없고 `repeated=1`: lane-log 전용 3칸은 `StageError`, 나머지 `1020`
- convergence 비트와 `repeated=1`: `2¹¹ = 2048`

[`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 값을 0으로 취급한다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

하지만 v15는 모든 후보의 `terminal_action()`을 먼저 호출한다. 따라서 `then` 없는 `retry(n)`, `then: retry(n)`, 비-retry 행의 `then`, 미지 action은 `worst_status()` 전에 `StageError`가 된다. 이 순서가 지켜지는 한 R6은 맞다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β, 부분집합 선검사, T‑1/T‑2가 모두 정합한다. |
| B-2 | closed | 출구 12 ID·8,190칸과 input-digest 진입 예외가 분리됐다. |
| B-3 | **partially** | 99fad78에서 독립 값을 생성하는 절차는 섰으나 필수 manifest 수락 명세가 AH-1~AH-3으로 미완이다. |
| B-4 | closed | `phases` 교집합 없이 판정점별 정확 등식이 선다. |
| B-5 | closed | 세 잘못된 `then` 형태와 미지 action을 관문·런타임 모두 fail-closed 처리한다. |
| B-6 | closed | kind 3종, upstream 호출자 0, `deferred/test_bound`가 명확하다. |
| B-7 | closed | pytest·7관문 plain/`-O` 명령이 모두 명시됐다. |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역 패치. |
| V-2 | closed | `-I`, 명시 repo, provenance 6검사와 단일 `__path__`. |
| V-3 | closed | 재시도 1회차는 정확히 3개 레인. |
| V-4 | closed | phase 우주·형식·유령 phase 거부. |
| V-5 | closed | 판정점 `{early, exit}` 유일성과 출구 12-ID 우주 고정. |
| V-6 | closed | 실행 가능한 고정 predicate와 독립 β 계산. |
| V-7 | closed | T‑11 ⑤가 엔진·관문 종단 어휘를 연결한다. |
| V-8 | closed | StageError 세 칸과 두 종류 순서를 정확히 구별한다. |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 `chdir` 전에 절대화. |
| N-2 | closed | 12개 phase 전건이 기재됐고 재실측과 일치. |
| N-3 | closed | B‑0 → 병합 → 골든 커밋 → B 순서가 명시됐다. |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 좌표. |
| N-5 | closed | T‑12 계약↔엔진 상수 양방향 다리. |
| N-6 | closed | early iff와 거짓 양성 차단. |
| N-7 | closed | 다섯 문언이 모두 구체화됐다. |

W~AE는 다시 열리지 않았다. AF-2·AF-3도 closed다. AF-1은 AG-1을 거쳐 여전히 **partially**다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 쓴다.
- tail은 입력 `decompose`를 그대로 반환한다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 동일한 `decomposes[canonical_run]`을 사용한다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 양쪽 모두 claims를 복사한 후 같은 `rewrite_claims`를 적용한다([read.py:528](/home/laptop/projects/patent-docent/engine/stages/read.py:528)).
- 수렴 여섯 축은 claims에서 구축된 independent/dependent/elements/additions만 읽는다([convergence.py](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)).

실측상 조기·출구 claims의 차이는 하나뿐이었다.

> `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')]`

그 차이는 수렴 축 밖이며 여섯 축은 모두 통과했다.

> `FINAL axes=[('independent-count', 'pass'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

따라서 출구에서만 convergence를 떨어뜨리는 정상 레인 페이로드는 제시할 수 없다.

T‑1의 검사층 주입은 T28 §3③의 “실제 러너 경로”를 충족한다. 패치하는 전역은 출구의 유일한 [`run_read_checks()` 호출](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)에서 읽힌다. 동일한 독립항 복제를 메모리에서 검사기에 적용한 결과:

> `failed=['read.convergence']`  
> `FINAL axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량. |
| ② | 맞다 | input-digest 값은 T29가 승인한 영역 밖 값. |
| ③ | 맞다 | `judged_at` 이름은 원장이 설계에 위임. |
| ④ | 맞다 | 현 v15의 T‑11 ⑤가 종단 어휘 두 벌을 대조한다. |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존한다. |
| ⑥ | 맞다 | 비-retry `then` 금지는 fail-closed 형태 규율. |
| ⑦ | 맞다 | 미지 ID는 공식 영역 밖 무효 입력이며 정상 12-ID 값 공간을 바꾸지 않는다. |
| ⑧ | 맞다 | `action: halt`는 T29 §3③의 명시값. |
| ⑨ | 맞다 | early 목록은 진입 가드가 실제 읽어 승인 상수와 대조한다. `runner_reads`가 과장되지 않았다. |
| ⑩ | 맞다 | T‑1의 전역 패치와 독립항 복제 형태가 실물에 맞는다. |
| ⑪ | 맞다 | T28 표지는 원장이 정한 convergence 술어에만 단다. |
| ⑫ | 맞다 | T32를 T31 소라운드에 합치는 것은 허용된 재량. |
| ⑬ | 맞다 | 판정점·ID 우주 고정은 형식 규율이다. |
| ⑭ | 맞다 | `-I`와 provenance 6검사는 기준 트리에서 값이 나왔음을 충분히 묶는다. AH는 사후 manifest 검증 문제다. |
| ⑮ | 맞다 | B‑0 분리는 골든이 B보다 먼저 서기 위해 필요하고 clone 조립도 명시됐다. |
| ⑯ | 맞다 | R9는 HEAD가 이미 만족하는 선언 등식. |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이며 T‑11 ⑥이 상수 두 벌을 연결한다. |
| ⑱ | 맞다 | 선언 중복 금지는 형식 규율. |
| ⑲ | 맞다 | 승인 골격은 모든 기계 필드를 포함하고 condition/note만 산문으로 남긴다. |
| ⑳ | 맞다 | 주입은 convergence 한 검사, independent-count 한 축만 실패시킨다고 실측됐다. |

자기 신고 안에는 새 Owner 재정 공백이 없다. 남은 것은 §2.8의 공학 명세 공백이다.

## F. 관문 G1~G6

| 관문 | 판정 | 이유 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·kind·xor·condition/note 존재와 타입을 고정한다. |
| G2 | covered | entry/exit/judged_here 우주와 조기 세 선언 집합을 양방향 대조한다. |
| G3 | covered | `phases` 없이 정확 등식, 승인 3/8 집합, 엄격 int 예산을 집행한다. |
| G4 | covered | phase 형식·우주·exit 필수·early iff를 집행한다. |
| G5 | covered | input-digest의 entry 표지·halt·points 부재·재시도 제외를 집행한다. |
| G6 | covered | R6의 전 항목을 집행한다. |

열거는 16종이 아니라 **36종**이다. 원장 필수 심기와 1차 도전 요구가 모두 들어 있다.

- 행 없는 검사: ⑴
- 검사 없는 행 및 `read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 조기 선언 전용 ghost: ㉞
- condition 삭제·note 타입: ㉟·㊱

G1~G6이 주장하는 범위 안에서 통과하는 변조는 찾지 못했다. AH-1~AH-3은 이 관문이 아니라 별도 manifest 검증기/T‑V의 결함이다.

## G. M3 결정 공백

세 곳이 남는다.

1. 최상위 non-dict manifest를 어떤 ID로 반환할지, 혹은 예외로 둘지(AH-1).
2. 셀 값 제약이 실패했을 때 `expected_counts.keys.exact`를 평가할지 건너뛸지(AH-2).
3. `exception.cell_count.eq`가 고정값 2048만 뜻하는지, `len(cells)`와의 직접 등식도 뜻하는지(AH-3).

모두 Owner 재정이 아니라 설계 수정 사항이지만, 현재 문언대로라면 M3가 blocked 반려하거나 임의 선택해야 하므로 PASS가 될 수 없다.

## 검증 경로

- HEAD·보호 경로:

  ```bash
  git status --short
  git diff --name-only 2d55128 HEAD -- engine contracts reader tests tools
  git rev-parse --short=12 HEAD
  ```

  앞 두 명령은 빈 출력. 도중 허용된 docs 전용 커밋이 들어와 마지막 줄은:

  > `5e248206336d`

- 8,190칸 전수: `READ_CHECK_IDS + ENGINE_READ_CHECK_IDS`의 모든 비공집합과 repeated 0/1을 만들어 [`_failure_verdict()`](/home/laptop/projects/patent-docent/engine/stages/read.py:1937)를 직접 호출하고 v15 모형과 대조했다.

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 선언·phase·산문 필드:

  > `FINAL phases={'read.schema': ['exit'], 'read.source-digest': ['exit'], ..., 'read.convergence': ['early', 'exit'], 'read.lane-log-shape': ['exit'], 'read.lane-log-digest-value': ['exit']}`

  같은 실행에서 `exit_count=12`, `exit_unique=True`, 세 early 집합 상등, `all_exit=True`, `condition_note_rows=10/10`을 확인했다.

- 조기/출구 claims 차이와 축:

  > `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')]`

- T‑1 주입을 검사층에서 재현:

  > `failed=['read.convergence']`  
  > `FINAL axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

- 재시도 레인 계획:

  > `FINAL rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- `worst_status`:

  > `FINAL known=halt unknown_only=ok mixed=escalate`

- upstream 호출자:

  > `FINAL upstream_literal_callers=0 hits=[]`

- `cell_count` 모순 계산:

  > `FINAL target_only_if_fixed=True prose_cell_count_eq=False`

- 격리 전제:

  > `FINAL isolated=1 no_user_site=1 safe_path=True user_site_enabled=False sys_path=[...]`

- 패키지 경로:

  > `FINAL engine_paths=['/home/laptop/projects/patent-docent/engine'] reader_paths=['/home/laptop/projects/patent-docent/reader']`

- 시험 import 좌표:

  > `33:import test_m2_read as m2  # noqa: E402`

## [미검증]

- v15 자체는 리포 파일이 아니라 첨부 전문이므로 설계 § 좌표는 첨부를 기준으로 판정했다.
- `generate.py`, `validate_manifest.py`, manifest, `check_failure_table.py`, 신규 시험은 아직 없어 실행하지 못했다.
- B‑0 clone/worktree/임시 커밋/골든 생성은 파일을 만들기 때문에 read-only 규율상 실행하지 않았다.
- T‑1/T‑2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았다. 동일 검사층 입력과 레인 계획은 메모리에서 검증했다.
- 전체 pytest 및 관문 plain/`-O`는 캐시·임시 파일 가능성 때문에 실행하지 않았다.
- 리포에는 아무것도 쓰지 않았고, 마지막 `git status --short`와 보호 경로 diff는 빈 출력이었다.