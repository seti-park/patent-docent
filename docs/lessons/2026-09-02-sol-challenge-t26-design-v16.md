# 독립 감수 원문 — 재정 T26 집행 설계 v16 의 M1b 설계 도전(15차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v16/final.txt` 의 sha256 `85594c151609d4d7c8e22c6a01b221232ce343a527c70b43f86eaab58e381df9` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 20분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 15차 심사** — 설계 **v16** 에 대한 것. 도전 중 총괄이 문서 전용 커밋을
넣을 수 있음을 발주문이 고지했고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다.

**판정 = FAIL · 지적 3건(HIGH 1 · MED 1 · LOW 1) · 새 재정 사항 0 · AH-1~AH-4 전건 closed · AG-1 partially.** 값 8,190 칸은 열다섯 번째로 일치. **AI-1**: `$comment` 「비공 str」 제약에 ID·변조·순서 없음 · **AI-2**: 「표 T-V 행 순서 = 평가 순서」 선언이 2열 배치·DAG 와 충돌 · **AI-3**: DAG 「`.eq` 열 개」는 실제 다섯. v17 = 「비공」 직접 검사 삭제(세 `contains` 가 함의 — 함의 목록에 명시) · 그 문언 삭제 + DAG 절이 순서의 유일 정본 · 문언 정정.

지적 열거 = AI-1, AI-2, AI-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§21** 에 있다.
전부 **수용**(공학 · 규율 11 ③) — 다음 판에 반영했다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## AH-1~AH-4 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AH-1 | **closed** | `manifest.type`과 `[]` 단일 변조가 생겼고, DAG가 `manifest.type → top.keys.exact`로 시작한다. |
| AH-2 | **closed** | `expected_counts.keys.exact`가 고정 `COUNT_KEY_SLUGS` 키 집합만 보도록 바뀌었고, 계수 재계산은 모든 `cells` 제약 통과 뒤로 밀렸다. |
| AH-3 | **closed** | `exception.cell_count.eq`가 `cell_count == 2048` 하나로 단일화됐다. 중복 셀 변조는 `exception.cells.unique`만 깨뜨린다. |
| AH-4 | **closed** | §1이 실물과 같은 `tests/test_m21_retry_budget_by_judgment_point.py:33 import test_m2_read as m2`로 고쳐졌다. |

AH 네 건은 좁은 의미에서 닫혔다. 그러나 AG-1이 요구한 “제약 ID·단일진단·선행순서의 단일 정본”은 아래 AI-1~AI-3 때문에 여전히 **partially**다.

## 지적 목록

### AI-1 · HIGH · 설계 §2.8 검증기 항목·표 T-V·선행조건 DAG

`$comment`의 “비공 문자열” 제약에 독립 ID·변조·선행순서가 없다.

검사 항목은 `$comment`를 “비공 str”로 요구하지만 T-V에는 다음만 있다.

- `comment.type`
- `comment.contains.T26`
- `comment.contains.T28`
- `comment.contains.T29`

`comment.nonempty`는 없으며, “ID를 두지 않는 함의 제약” 목록에도 들어 있지 않다. 따라서 `$comment = ""`에서 M3는 다음 중 하나를 골라야 한다.

- 별도 `comment.nonempty`를 추가해 `CONSTRAINT_IDS == T-V ID 집합`을 깨뜨림
- 비공 여부를 `comment.type`에 합쳐 “독립 제약 하나 = ID 하나”를 깨뜨림
- 직접 비공 검사를 생략해 검사 항목 문언을 어김
- 세 `contains` 진단을 모두 내거나 첫 하나만 내도록 임의 선택

닫는 법: `comment.nonempty` ID와 빈 문자열 단일 변조를 추가하고, DAG를 `comment.type → comment.nonempty → {comment.contains.T26,T28,T29}`로 명시한다. 또는 “비공” 직접 검사를 삭제하고 세 부분 문자열 제약이 이를 함의한다고 ID 없는 제약 절에 명시해야 한다.

### AI-2 · MED · 설계 §2.8 표 T-V의 “행 순서”·선행조건 DAG

T-V의 행 순서를 평가 순서라고 선언했지만 실제 2열 배치는 명시 DAG와 충돌한다.

대표적으로:

- T-V에서는 `cells.value.type`이 `cells.keys.exact`보다 먼저 보이지만 DAG는 `cells.type → cells.keys.exact → 각 값 type`이다.
- T-V에서는 `provenance.reader_path.items.str`이 `reader_path.type`·`len1`보다 먼저 보이지만 DAG는 `type → len1 → items.str → absolute`다.

`reader_path = 17` 같은 T-V 밖 입력에서는 표 순서를 따르면 원소 순회 중 예외가 날 수 있고, DAG를 따르면 `provenance.reader_path.type` 위반 하나를 반환한다. M3가 어느 문언을 정본으로 삼을지 결정해야 한다.

닫는 법: “T-V 행 순서가 평가 순서” 문언을 삭제하고 DAG만 정본이라고 명시하거나, T-V를 1열·ID당 1행으로 다시 배열해 실제 선행순서와 일치시킨다.

### AI-3 · LOW · 설계 §2.8 `expected_counts` DAG

DAG는 “`.eq` 열 개”라고 하지만 실제 열거는 다섯 슬러그마다 `type` 하나와 `eq` 하나다. 즉 `.eq`는 **5개**, 전체 ID가 10개다.

닫는 법: “`.eq` 열 개”를 “다섯 `.eq`” 또는 “다섯 `type` + 다섯 `eq`”로 고친다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① ID 키·조건 설명 존치 | covered | §2.1·§2.2·G1·T-13. 모든 행의 `condition`·`note` 필수 비공 str. |
| T26 §2⒜② 조치 격자·동률 순서 | covered | §2.2·§2.6 `select_failure_row`; 8,190칸 불일치 0. |
| T26 §2⒜③ 완전성·정확 등식·실제 부분집합 | covered | R2·R8·R9, §2.3, G2~G4. `phases` 교집합 없이 정확 등식이다. |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11. |
| T26 §3② 오늘 표 불변 | **partially** | 값 대조는 정확하지만 필수 manifest 검증 명세에 AI-1~AI-3 결정 공백이 있다. |
| T26 §3③ 양방향 관문·세 심기 | covered | §2.7 ⑴·⑵·⑶/⑷/㉑. |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10에서 7관문 정정 마커를 요구한다. |
| T26 §3⑤ 전수·전 관문 2모드 | covered | §2.11의 pytest 및 7관문 plain/`-O`. |
| T28 §3① 8,190칸 값 불변 | **partially** | 런타임 값 시험은 완전하지만 그 골든의 수락 검증기 명세가 AI-1~AI-3으로 단일하지 않다. |
| T28 §3② β 표지 2,048칸 | covered | 고정 술어·집합·cell_count 정의가 정확하다. |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2. 전역 패치와 3개 retry-1 레인이 실물과 맞는다. |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3와 부분집합 선검사. |
| T29 §3① 골든 12 ID 정확 | covered | §2.8 `check_ids` 계층·T-7·T-12. |
| T29 §3② 진입 예외 반증 | covered | T-3. |
| T29 §3③ 진입 표지·halt·출구 제외 | covered | §2.4·G5. |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1. |
| T30 §3② `checks` xor `kind` | covered | R4·G1. |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9. 실물 호출자 0. |
| T30 §3④ SPEC 문서화 | covered | §2.10. |

T31을 B 뒤 소라운드로 미룬 판단은 원장과 같다. T32를 그 소라운드에 합치는 것도 T32 §3⑤가 허용한다. `screening_memos[].read_run` 무접촉 판단도 맞다.

원장 밖 요소인 `judged_at`, 승인 상수, 미지 ID fail-closed, provenance 검사, B-0 분리, 엄격한 manifest 진단 ID는 공학적 집행이다. AI-1~AI-3도 새 Owner 재정이 아니라 설계 수정 사항이다.

## B. 오늘의 표 불변

직접 `_failure_verdict()`를 8,190칸 전수 호출하고 v16 모형과 비교했다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v16 모형 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`이다.

§2.2 손검산과 §3 대표 칸에서 **틀린 출력 칸은 찾지 못했다**. 계산도 맞다.

- schema/source-digest 중 하나 이상: `(4095−1023)×2 = 6144`
- 둘 다 없고 `repeated=0`: `1023`
- 둘 다 없고 `repeated=1`: lane-log 전용 3칸은 `StageError`, 나머지 `1020`
- convergence 비트와 `repeated=1`: `2¹¹ = 2048`

[`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 값을 0으로 취급한다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

v16은 `select_failure_row()`가 모든 후보의 `terminal_action()`을 먼저 검사하도록 명시한다. 따라서 `then` 없는 `retry(n)`, `then: retry(n)`, 비-retry 행의 `then`, 미지 action은 `worst_status()` 전에 `StageError`가 된다. 이 순서가 구현되면 R6은 정확하다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β·부분집합 선검사·T-1/T-2가 정합하며 `repeated ∧ convergence`는 출구에서 도달 불능이다. |
| B-2 | closed | 출구 12 ID·8,190칸과 input-digest 진입 예외가 분리됐다. |
| B-3 | **partially** | 값은 `99fad78` 트리에서 독립 생성되지만 필수 검증기 제약 정본이 AI-1~AI-3으로 아직 단일하지 않다. |
| B-4 | closed | `phases` 없이 판정점별 정확 등식이 선다. |
| B-5 | closed | 세 잘못된 `then` 형태와 미지 action을 관문·런타임 모두 fail-closed 처리한다. |
| B-6 | closed | kind 3종, upstream 호출자 0, `deferred/test_bound`가 명확하다. |
| B-7 | closed | pytest·7관문 plain/`-O` 수락 명령이 있다. |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역을 패치한다. |
| V-2 | closed | `-I`, 명시 repo, provenance 6검사와 패키지 `__path__` 단일성. |
| V-3 | closed | 후속 재시도 1회차는 정확히 3개 레인이다. |
| V-4 | closed | phase 형식·우주·유령 phase 거부. |
| V-5 | closed | 판정점 `{early, exit}` 유일성과 출구 12-ID 우주를 고정한다. |
| V-6 | closed | 실행 가능한 predicate와 독립 β 계산. |
| V-7 | closed | T-11 ⑤가 엔진·관문 종단 어휘를 연결한다. |
| V-8 | closed | 예외 3칸과 격자/동률 순서를 정확히 구별한다. |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 `chdir` 전에 절대화한다. |
| N-2 | closed | 12개 phase 전건이 기재됐고 재실측과 일치한다. |
| N-3 | closed | B-0 → 병합 → 골든 커밋 → B 순서가 명시됐다. |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 좌표가 있다. |
| N-5 | closed | T-12 계약↔엔진 상수 양방향 다리. |
| N-6 | closed | early iff와 거짓 양성 차단. |
| N-7 | closed | 다섯 문언 모두 구체화됐다. |

W~AH의 기존 개별 반례는 다시 열리지 않았다. AG-2와 AH-1~AH-4는 closed지만, AG-1의 더 넓은 단일제약 명세는 AI-1~AI-3 때문에 여전히 **partially**다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 [`assemble_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출한다.
- tail은 입력 `decompose` 객체를 그대로 반환한다([read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구 모두 `decomposes[canonical_run]`을 사용한다([read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 양쪽 모두 claims를 deepcopy한 뒤 같은 `rewrite_claims`를 적용한다([read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:528)).
- 수렴 여섯 축은 claims에서 구축한 independent/dependent/elements/additions만 읽는다([convergence.py](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)).

수확까지 포함해 재현한 조기·출구 claims 차이는 한 필드뿐이었다.

> `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')] status=pass ...`

그 필드는 수렴축 밖이다. 따라서 출구에서만 convergence를 떨어뜨리는 정상 레인 페이로드는 없다.

T-1의 검사층 주입은 T28 §3③의 “실제 러너 경로”를 충족한다. 실제 출구 호출은 [read.py:1743](/home/laptop/projects/patent-docent/engine/stages/read.py:1743) 한 곳이고 이 모듈 전역을 호출 시 읽는다. 독립항 복제를 적용한 검사 결과도 다음과 같았다.

> `FINAL baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량. |
| ② | 맞다 | input-digest의 영역 밖 값은 T29 승인 사항. |
| ③ | 맞다 | `judged_at` 이름은 원장이 설계에 위임했다. |
| ④ | 맞다 | T-11 ⑤가 종단 어휘 두 벌을 대조한다. |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존한다. |
| ⑥ | 맞다 | 비-retry `then` 금지는 fail-closed 형태 규율이다. |
| ⑦ | 맞다 | 미지 ID는 공식 영역 밖 무효 입력이며 정상 12-ID 값을 바꾸지 않는다. |
| ⑧ | 맞다 | `action: halt`는 T29 §3③이 관문에 직접 요구한 값이다. |
| ⑨ | 맞다 | early 목록은 진입 가드가 실제 읽어 승인 상수와 대조하므로 `runner_reads`가 성립한다. |
| ⑩ | 맞다 | 패치 전역과 독립항 복제 형태가 실물에 맞는다. `CheckContext`의 다른 필드는 보존하라는 문언도 있다. |
| ⑪ | 맞다 | T28이 정한 convergence 술어에만 표지를 단다. |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용된 재량이다. |
| ⑬ | 맞다 | 판정점·ID 우주 고정은 형식 규율이다. |
| ⑭ | 맞다 | `-I`와 provenance 6검사는 실제 생성 import가 기준 트리에서 왔음을 묶는다. |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 먼저 세우기 위해 필요하며 clone 조립도 명시됐다. |
| ⑯ | 맞다 | R9는 HEAD가 이미 만족하는 선언 등식이다. |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이며 T-11 ⑥이 상수 두 벌을 연결한다. |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율이다. |
| ⑲ | 맞다 | 승인 골격은 모든 failure 기계 필드를 포함하고 산문 둘만 내용 자유다. |
| ⑳ | 맞다 | 주입은 convergence 한 검사와 independent-count 한 축만 실패시킨다. |

AI-1~AI-3은 이 자기 신고들의 Owner 분류를 뒤집는 재정 문제가 아니라, §2.8 내부 명세의 공학적 결정 공백이다.

## F. 관문 §2.7

| 관문 | 판정 | 이유 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·kind·xor·condition/note 존재와 타입을 고정한다. |
| G2 | covered | entry/exit/judged_here 우주와 조기 세 선언 집합을 양방향 대조한다. |
| G3 | covered | `phases` 없는 정확 등식, 승인 3/8 집합, 엄격 int 예산을 집행한다. |
| G4 | covered | phase 형식·우주·exit 필수·early iff를 집행한다. |
| G5 | covered | input-digest의 entry 표지·halt·points 부재·재시도 제외를 집행한다. |
| G6 | covered | R6 전항을 집행한다. |

열거는 16종이 아니라 **36종**이다. 원장 필수 심기와 1차 도전 요구가 모두 포함됐다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- `judged_here` ghost: ㉞
- condition 삭제·note 타입: ㉟·㊱

G1~G6의 선언 범위 안에서 통과하는 계약 변조는 찾지 못했다. AI-1~AI-3은 `check_failure_table.py`가 아니라 별도 manifest 검증기/T-V의 결함이다.

## G. M3 결정 공백

세 곳이 남는다.

1. 빈 `$comment`를 `comment.nonempty`, `comment.type`, 세 `contains` 중 무엇으로 진단할지(AI-1).
2. T-V 물리 행 순서와 명시 DAG 중 어느 것을 실제 평가 순서로 삼을지(AI-2).
3. `expected_counts`의 `.eq`가 다섯인지 열인지 문언을 교정해 해석할지(AI-3).

Owner 재정은 필요 없지만, 현재 첨부대로면 M3가 임의 선택하거나 blocked 반려해야 하므로 PASS가 아니다.

## 검증 경로

- HEAD·보호 경로:

  ```bash
  git status --short
  git diff --name-only 5e24820 HEAD -- engine contracts reader tests tools
  git rev-parse --short=12 HEAD
  ```

  앞 두 명령은 빈 출력. 마지막 줄:

  > `5e248206336d`

- 8,190칸 전수: `READ_CHECK_IDS + ENGINE_READ_CHECK_IDS`의 모든 비공집합과 repeated 0/1을 만들어 `_failure_verdict()`를 직접 호출하고 v16 모형과 비교했다.

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 선언·국면·코드 상수:

  > `FINAL exit_count=12 exit_unique=True exit_matches_code=True entry=['read.input-digest'] points=['early', 'exit'] judged_eq_phases=True judged_eq_early_point=True all_exit=True phase_universe=['early', 'exit']`

- 재시도 레인 계획:

  > `FINAL rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- 조기/출구 claims와 수렴축:

  > `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')] status=pass axes=[('independent-count', 'pass'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

- T-1 검사층 주입:

  > `FINAL baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

- `worst_status`:

  > `FINAL known=halt unknown_only=ok mixed=escalate`

- 골든 기준 트리:

  ```bash
  git rev-parse 99fad78
  git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l
  ```

  마지막 출력:

  > `0`

- 시험 import 좌표:

  > `33:import test_m2_read as m2  # noqa: E402`

## [미검증]

- v16은 리포 파일이 아니라 첨부 전문이므로 설계 § 좌표는 첨부를 기준으로 판정했다.
- `generate.py`, `validate_manifest.py`, manifest, `check_failure_table.py`, 신규 시험은 아직 없어 실행하지 못했다.
- B-0 clone/worktree/임시 커밋과 생성 명령은 파일을 만들므로 read-only 규율상 실행하지 않았다.
- T-1/T-2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았다. 동일 검사 입력과 레인 계획은 메모리에서 검증했다.
- 전체 pytest와 관문 plain/`-O`는 캐시·임시 파일 가능성 때문에 실행하지 않았다.
- 리포에는 아무것도 쓰지 않았고, 마지막 작업 트리와 보호 경로 diff는 빈 출력이었다.