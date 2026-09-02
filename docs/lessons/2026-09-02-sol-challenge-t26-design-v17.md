# 독립 감수 원문 — 재정 T26 집행 설계 v17 의 M1b 설계 도전(16차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v17/final.txt` 의 sha256 `f7118d6ec4e6e916cd47daca3f6ed78b5fb2ad1a4ac35a42791f82251e0c68ad` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 01:06~01:23 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 16차 심사** — 설계 **v17** 에 대한 것. 발주문 §5 는 도전자에게 §2.8 검증기 절의
세 표(검사 항목 · T-V · DAG)의 차집합을 직접 내게 했다.

**판정 = FAIL · 지적 1건(MED 1) · 새 재정 사항 0 · AI-1~AI-3 전건 closed · AG-1 은 AJ-1 때문에 partially.** 값 8,190 칸은 열여섯 번째로 일치. **AJ-1**: `provenance.tree_head` 의
제약·선행순서가 세 정본 사이에서 불일치 — 검사 항목·T-V 에는 `provenance.tree_head.eq` 하나뿐인데 DAG 가 「각 키: type → …」로 읽혀 `tree_head` 에도 별도 type 단계가 있는 듯하고
DAG 에 `.eq` 가 명시되지 않아, `tree_head = 17` 변조에서 M3 가 진단 ID 를 임의 선택하게 된다. v18 = DAG provenance 가지를 키별로 명시 재작성(`tree_head` 는 `.eq` 하나 ·
비문자열을 포함한 모든 비상등값을 `.eq` 로 보고 · 별도 `.type` 없음) · T-V 의 `tree_head` 변조를 nibble 반전 대신 정수 `17` 로.

지적 열거 = AJ-1

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§22** 에 있다.
**수용**(공학 · 규율 11 ③) — v18 에 반영했다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## AI-1~AI-3 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AI-1 | closed | `$comment`의 직접 `nonempty` 검사를 삭제했고, 세 `contains` 제약이 비공성을 함의한다고 ID 없는 제약에 명시했다. DAG도 `comment.type → {contains.T26,T28,T29}`로 일치한다. |
| AI-2 | closed | T-V 물리 행 순서를 평가 순서로 삼는 문언을 삭제하고 DAG만 유일 정본으로 정했다. |
| AI-3 | closed | `expected_counts`를 “다섯 type + 다섯 eq = 열 ID”로 바로잡았다. |

AI 세 건 자체는 닫혔다. 다만 더 넓은 AG-1의 “모든 제약 ID·단일진단·선행순서의 단일 정본”은 아래 AJ-1 때문에 여전히 partially다.

## 지적 목록

### AJ-1 · MED · 설계 §2.8 검증기 항목·T-V·선행조건 DAG

`provenance.tree_head`의 제약과 선행순서가 세 정본 사이에서 일치하지 않는다.

- 검사 항목과 T-V에는 `provenance.tree_head.eq`만 있다.
- T-V 변조도 “첫 nibble 반전”으로 이 equality를 겨눈다.
- 그런데 DAG는 `provenance: type → keys.exact → 각 키: type → …`라고 하여 `tree_head`에도 별도 type 단계가 있는 것으로 읽힌다.
- 동시에 그 DAG에는 `provenance.tree_head.eq`가 명시적으로 들어 있지 않다.

따라서 `tree_head = 17`에서 M3는 다음 중 하나를 골라야 한다.

1. 표에 없는 `provenance.tree_head.type`을 추가한다.
2. type 위반도 `provenance.tree_head.eq`로 보고해 “각 키: type” 문언을 무시한다.
3. type과 eq를 한 ID에 합쳐 “독립 제약 하나 = ID 하나”의 해석을 임의로 정한다.

AJ-1을 닫는 법:

- DAG의 provenance 가지를 다음처럼 명시적으로 다시 쓴다.

  `provenance.type → provenance.keys.exact → {tree_head.eq, read_module.type→absolute, …, generated_at.type→iso}`

- `tree_head`에는 별도 type 제약이 없고, 비문자열을 포함한 모든 비상등값은 `provenance.tree_head.eq` 하나로 보고한다고 명시한다.
- 가능하면 T-V의 `tree_head.eq` 단일 변조를 nibble 반전 대신 정수 `17`로 바꿔 이 해석을 직접 고정한다.

값 표를 바꾸는 결함은 아니지만, 현재 첨부 그대로라면 M3가 진단 ID와 DAG를 임의 선택해야 하므로 PASS가 아니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① ID 키·조건 설명 | covered | §2.1·§2.2·G1·T-13. 검사 행은 `checks`, 사건 행은 T30에 따라 `kind`; `condition`·`note`는 필수 비공 str. |
| T26 §2⒜② 조치 격자·동률 순서 | covered | §2.2·§2.6. 격자와 계약 행 순서를 분리했고 전수 불일치 0. |
| T26 §2⒜③ 완전성·정확 등식·실제 부분집합 | covered | R2·R8·R9, §2.3, G2~G4, T-4. `phases` 교집합 없이 정확 등식이다. |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11. |
| T26 §3② 오늘 표 불변 | partially | 값은 정확하지만 필수 골든 검증기의 선행순서/진단 정본에 AJ-1 결정 공백이 있다. |
| T26 §3③ 양방향 관문·세 심기 | covered | §2.7 ⑴·⑵·⑶·⑷·㉑. |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10에서 7관문 정정 마커를 요구한다. |
| T26 §3⑤ 전수·전 관문 2모드 | covered | §2.11에 pytest 2모드와 7관문 plain/`-O`가 있다. |
| T28 §3① 8,190칸 값 불변 | partially | 런타임 값 대조는 전수지만 골든 수락 검증기 명세가 AJ-1로 아직 단일하지 않다. |
| T28 §3② β 표지 2,048칸 | covered | §2.8의 고정 술어·집합·`cell_count`가 정확하다. |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2. 패치 전역과 레인 3행이 실물과 맞는다. |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3·G4와 부분집합 선검사. |
| T29 §3① 골든 12 ID 정확 | covered | §2.8 `check_ids.expected_set`, T-7·T-12. |
| T29 §3② 진입 예외 반증 | covered | T-3가 `_failure_verdict` 0회를 계측한다. |
| T29 §3③ 진입 표지·halt·출구 제외 | covered | §2.4·G5. |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1. |
| T30 §3② `checks` xor `kind` | covered | R4·G1. |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9. |
| T30 §3④ SPEC 문서화 | covered | §2.10. |

T31을 B 뒤 소라운드로 미루고 T32를 그 소라운드에 합치는 판단은 각각 원장 T31 §3과 T32 §3⑤에 맞는다. `screening_memos[].read_run` 무접촉도 맞다.

`judged_at`, 미지 ID fail-closed, 승인 상수, provenance 검증, B-0 분리는 원장값을 집행하는 공학 요소다. AJ-1도 Owner 재정이 아니라 설계 내부 정합 수정이다.

## B. 오늘의 표 불변

HEAD [`_failure_verdict()`](/home/laptop/projects/patent-docent/engine/stages/read.py:1937)를 8,190칸 직접 호출하고 v17의 11행·격자·동률 순서를 별도 모델링했다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v17 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`이다.

§2.2 손검산과 §3 대표 칸에서 틀린 칸은 찾지 못했다.

- schema/source-digest 중 하나 이상: `(4095−1023)×2 = 6,144`
- 둘 다 없고 `repeated=0`: `1,023`
- 둘 다 없고 `repeated=1`: lane-log 전용 3칸은 `StageError`, 나머지 `1,020`
- convergence 비트와 `repeated=1`: `2¹¹ = 2,048`

[`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 값을 0으로 취급한다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

v17은 `select_failure_row()`가 모든 후보의 `terminal_action()`을 먼저 검증하도록 명시한다. 따라서 `then` 없는 `retry(n)`, `then: retry(n)`, 비-retry 행의 `then`, 미지 action은 `worst_status()` 전에 `StageError`가 된다. R6은 이 순서로 구현될 때 정확하다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β·부분집합 선검사·T-1/T-2가 정합하고 `repeated ∧ convergence`는 출구에서 도달 불능이다. |
| B-2 | closed | 출구 12 ID·8,190칸과 input-digest 진입 예외가 분리됐다. |
| B-3 | partially | 골든 값은 `99fad78` 트리에서 독립 생성되지만 필수 검증기의 제약/DAG 단일 정본이 AJ-1로 미완이다. |
| B-4 | closed | `phases` 없이 판정점별 정확 등식이 선다. |
| B-5 | closed | 잘못된 `then` 세 형태와 미지 action을 관문·런타임 모두 fail-closed 처리한다. |
| B-6 | closed | kind 3종, upstream 호출자 0, `deferred/test_bound`가 명확하다. |
| B-7 | closed | pytest와 7관문 모두 2모드 명령이 있다. |

### V-1~V-8

| 지적 | 판정 | 사유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역을 패치한다. |
| V-2 | closed | `-I`, 명시 repo, provenance 6검사와 패키지 `__path__` 단일성. |
| V-3 | closed | 후속 재시도 1회차가 정확히 3개 레인이다. |
| V-4 | closed | phase 형식·우주·유령 phase 거부. |
| V-5 | closed | 판정점 `{early, exit}` 유일성과 출구 12-ID 우주 고정. |
| V-6 | closed | 실행 가능한 predicate와 독립 β 계산. |
| V-7 | closed | T-11 ⑤가 엔진·관문 종단 어휘를 연결한다. |
| V-8 | closed | 3개 예외 칸과 격자/동률 순서를 정확히 구별한다. |

### N-1~N-7

| 지적 | 판정 | 사유 |
|---|---|---|
| N-1 | closed | `out`을 `chdir` 전에 절대화한다. |
| N-2 | closed | 12개 phase 전건을 기재했고 재실측과 일치했다. |
| N-3 | closed | B-0 → 병합 → 골든 커밋 → B 순서가 고정됐다. |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 좌표가 있다. |
| N-5 | closed | T-12 계약↔엔진 상수 양방향 다리. |
| N-6 | closed | early iff와 거짓 양성 차단. |
| N-7 | closed | 다섯 문언 모두 구체화됐다. |

W~AH의 기존 개별 반례는 다시 열리지 않았다. 다만 AG-1의 넓은 “모든 제약과 DAG의 단일 정본”은 AJ-1로 partially다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 `assemble_spec()`을 호출한다.
- tail은 입력 `decompose` 객체를 그대로 반환한다.
- 조기와 출구 모두 `decomposes[canonical_run]`에서 출발한다.
- 양쪽 모두 claims를 deepcopy한 뒤 같은 [`rewrite_claims()`](/home/laptop/projects/patent-docent/engine/stages/read.py:483)를 적용한다.
- 수렴 여섯 축은 [`SpecIndex`](/home/laptop/projects/patent-docent/reader/lib/spec_io.py:36)로 claims의 수·문언·트리·종속 서명·addition 부착만 읽는다.

수확까지 포함한 메모리 재현 결과:

> `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')] baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

유일한 차이는 수렴축 밖의 `applicant_interest.material_id`다. 정상 레인 페이로드로 출구에서만 convergence를 떨어뜨릴 수 없다.

T-1은 실제 러너가 호출하는 [출구 `run_read_checks()` 자리](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)의 모듈 전역을 패치하고, 원래 검사기를 다시 호출한다. 따라서 T28 §3③의 “실제 러너 경로”를 충족한다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량. |
| ② | 맞다 | input-digest 영역 밖 값은 T29가 승인했다. |
| ③ | 맞다 | `judged_at` 이름은 원장이 설계에 위임했다. |
| ④ | 맞다 | T-11 ⑤가 종단 어휘 두 벌을 대조한다. |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존한다. |
| ⑥ | 맞다 | 비-retry `then` 금지는 fail-closed 형식 규율이다. |
| ⑦ | 맞다 | 미지 ID는 공식 12-ID 영역 밖의 무효 입력이며 정상 값 공간을 바꾸지 않는다. |
| ⑧ | 맞다 | `action: halt`는 T29 §3③이 관문에 직접 요구한다. |
| ⑨ | 맞다 | early 목록은 진입 가드가 실제 읽어 승인 상수와 대조하므로 `runner_reads`가 성립한다. |
| ⑩ | 맞다 | 패치 전역과 독립항 복제 형태가 실물에 맞는다. |
| ⑪ | 맞다 | 도달 불능 표지를 T28 술어에만 단다. |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용된 재량이다. |
| ⑬ | 맞다 | 판정점·ID 우주 고정은 형식 규율이다. |
| ⑭ | 맞다 | `-I`와 provenance 6검사는 값 모듈이 기준 트리에서 왔음을 결속한다. AJ-1은 이 분류가 아니라 manifest 진단 DAG 문제다. |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 먼저 세우기 위해 필요하다. |
| ⑯ | 맞다 | R9는 HEAD가 이미 만족하는 선언 등식이다. |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이며 T-11 ⑥이 두 상수 벌을 연결한다. |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율이다. |
| ⑲ | 맞다 | 승인 골격은 failure 기계 필드를 모두 포함하고 산문 둘만 자유다. |
| ⑳ | 맞다 | 주입은 convergence 한 검사와 independent-count 한 축만 실패시킨다. |

AJ-1은 Owner 재정 공백이 아니라 §2.8 내부 명세 오류다.

## F. 관문 §2.7

| 관문 | 판정 | 이유 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·kind·xor·산문 존재/타입을 고정한다. |
| G2 | covered | entry/exit/judged_here 우주와 조기 세 선언 집합을 양방향 대조한다. |
| G3 | covered | `phases` 없는 정확 등식, 승인 3/8 집합, 엄격 int 예산을 집행한다. |
| G4 | covered | phase 형식·우주·exit 필수·early iff를 집행한다. |
| G5 | covered | input-digest의 entry 표지·halt·points 부재·재시도 제외를 집행한다. |
| G6 | covered | R6 전항을 집행한다. |

열거는 16종이 아니라 36종이다. 필수 심기와 1차 도전 요구가 모두 들어 있다.

- 행 없는 검사: ⑴
- 검사 없는 행 및 `read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- `judged_here` 유령: ㉞
- condition 삭제·note 타입: ㉟·㊱

G1~G6의 선언 범위 안에서 관문이 통과시키는 T26/T28/T29/T30 위반 변조는 찾지 못했다. AJ-1은 별도 manifest 검증기 문제다.

## G. M3 결정 공백

한 곳이 남는다.

- `provenance.tree_head`의 비문자열/비상등 값을 `provenance.tree_head.eq`로 진단할지, 문언대로 별도 `.type` ID를 만들지, 그리고 `.eq`를 DAG 어디에 놓을지 M3가 정해야 한다(AJ-1).

Owner 재정은 필요 없지만, 그대로 넘기면 M3가 임의 선택하거나 blocked 반려해야 한다.

## 검증 경로

- HEAD·작업 트리·보호 경로:

  ```bash
  git status --short
  git diff --name-only 5e24820 HEAD -- engine contracts reader
  git rev-parse --short=12 HEAD
  ```

  마지막 실측:

  > `status_rows=0`  
  > `protected_diff_rows=0`  
  > `head=9d2246b4d995`

  도전 중 HEAD는 허용된 원문·인계 문서 반입으로 전진했지만 T26 보호 경로 diff는 0이다.

- `_failure_verdict()` 직접 8,190칸 호출:

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- v17 11행 모델과 HEAD 독립 대조:

  > `FINAL cells=8190 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} first=[]`

- 선언·국면·코드 상수:

  > `FINAL exit_count=12 exit_unique=True exit_matches_code=True entry=['read.input-digest'] points=['early', 'exit'] judged_eq_phases=True judged_eq_early_point=True all_exit=True phase_universe=['early', 'exit']`

- 재시도 레인 계획:

  > `FINAL rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- 조기/출구 claims 및 T-1 검사층 주입:

  > `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')] baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

- 기준 트리:

  ```bash
  git rev-parse 99fad78
  git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l
  ```

  > `99fad78c318875af99aa87083c029d2c6724e240`  
  > `0`

## [미검증]

- v17은 리포 파일이 아니라 첨부 전문이므로 § 좌표와 T-V/DAG 차집합은 첨부를 기준으로 정적 판정했다.
- `generate.py`, `validate_manifest.py`, manifest, `check_failure_table.py`, 신규 시험은 아직 없어 실행하지 못했다.
- B-0 clone/worktree/생성 명령은 파일을 만들므로 read-only 규율상 실행하지 않았다.
- T-1/T-2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았다. 동일 검사 입력·패치 도달점·레인 계획은 메모리에서 검증했다.
- 전체 pytest와 관문 plain/`-O`는 캐시·임시 파일 가능성 때문에 실행하지 않았다.
- 리포에는 아무것도 쓰지 않았으며 마지막 작업 트리와 `engine contracts reader` diff는 빈 출력이었다.