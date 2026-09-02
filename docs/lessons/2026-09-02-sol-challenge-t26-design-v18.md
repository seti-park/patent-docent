# 독립 감수 원문 — 재정 T26 집행 설계 v18 의 M1b 설계 도전(17차) · 판정 PASS

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v18/final.txt` 의 sha256 `eb3458b18d333b363a473654f33cb4fc7ae794d5d92d103b6d747a4940ab69f6` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 01:25~01:40 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 17차 심사** — 설계 **v18** 에 대한 것. 정본 HEAD `9d2246b` ·
도전 중 총괄 커밋 없음(도전자 실측 `status_rows=0 · protected diff 0`).

**판정 = PASS · 지적 0 · 결정 공백 0 · 새 재정 사항 0 · AJ-1 closed(AG-1 잔여도 함께) · B~AI 전건 closed.** 값 8,190 칸은 열일곱 번째로 일치
(`mismatches=0 · beta=2048 · StageError 3칸 = (1024,1)(2048,1)(3072,1)`). 도전자가 **[미검증]** 으로 남긴 것 6항 — §2.8 의 70개 ID 는 첨부 전문에서 정적 대조 ·
B-0 산출물(생성기·검증기·manifest·관문·신규 시험)은 아직 존재하지 않아 미실행 · 골든 생성·T-1/T-2 실러너·pytest·관문은 read-only 규율상 미실행. 이것들은
라운드 B-0·B 와 그 뒤 opus max 감사가 실물로 검증한다.

지적 열거 = 없음

처분 행은 서지 않는다 — 지적이 없으므로 `DISPOSITIONS.md` §1 에 이 파일의 행이 없다(관문 G3 · 열거 「없음」 ↔ 행 0). 기록은 `D-20260902-02-t26-design-challenge.md` **§23**.
**이 PASS 로 T26 §3 ①(PASS 전 착수·커밋 금지)이 해제된다** — 라운드 B-0(골든 생성기) 발주 가능. 설계 PASS 판 = v18(리포 밖 · 라운드 B 발주문 첨부로 들어온다).

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: PASS

## AJ-1 우선 판정

**AJ-1: closed.**

v18의 세 정본을 독립 전사해 대조한 결과:

> `FINAL inspection=70 tv=70 dag=70 i-t=[] t-i=[] d-t=[] t-d=[] tree=['provenance.tree_head.eq']`

- 검사 항목: `provenance.tree_head.eq` 하나만 존재
- T-V: 정수 `17` 변조를 그 ID 하나로 진단
- DAG: `tree_head: eq 하나`라고 명시
- 비문자열을 포함한 모든 비상등값을 `.eq`로 보고하며 별도 `.type`을 만들지 않는다고 명시

따라서 M3가 타입 ID를 새로 만들거나 진단을 합칠지 고를 여지가 없다. AG-1의 잔여도 함께 닫혔다.

ID 없는 함의 제약도 다섯 건으로 전부 설명된다: `check_ids.has_convergence`, `check_ids.len12`, `comment.nonempty`, `exception.cells.len2048`, `exception.cells.subset_of_cells`.

## 지적 목록

**없음.** 새 `AK-*` 지적을 세울 반례나 결정 공백을 찾지 못했다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·판단 |
|---|---|---|
| T26 §2⒜① ID 키·조건 설명 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회, G1·T-13 |
| T26 §2⒜② 조치 격자·동률 순서 | covered | §2.2·§2.6. 격자와 계약 순서를 분리하고 전수값도 일치 |
| T26 §2⒜③ 완전성·정확 등식·실제 부분집합 | covered | R2·R8·R9, §2.3, G2~G4, `_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | covered | §2.8 골든·T-7·99fad78 생성 순서 |
| T26 §3③ 양방향 관문·세 심기 | covered | §2.7 ⑴·⑵·⑶/⑷/㉑ |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10의 4→5→6→7 및 여섯→일곱 마커 |
| T26 §3⑤ 전수·전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | covered | §2.8 T-7 전수 대조 |
| T28 §3② β 표지 2,048칸 | covered | §2.8 고정 술어·집합·`cell_count` |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3·G4 및 부분집합 선검사 |
| T29 §3① 골든 12 ID 정확 | covered | §2.8 `check_ids.expected_set`, T-7·T-12 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ 진입 표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② `checks` xor `kind` | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미루는 것은 T31 §3①과 같고, T32를 그 소라운드에 합치는 것은 T32 §3⑤가 허용한다. `screening_memos[].read_run` 무접촉도 §5②를 따른다.

원장에 직접 없는 `judged_at`, 미지 ID fail-closed, 승인 상수, provenance 검증, B-0 분리, manifest 진단 ID는 각각 위임된 이름 또는 원장값을 집행하는 형식·검증 장치다. 새 값 공간을 입법한 요소는 없다.

## B. 오늘의 표 불변

HEAD의 [`_failure_verdict()`](/home/laptop/projects/patent-docent/engine/stages/read.py:1937)를 8,190칸 직접 호출하고 v18 격자를 별도 계산했다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v18 ↔ HEAD 불일치 | 0 |

> `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

§2.2 손검산과 §3 대표 칸에서 틀린 칸은 없다.

- schema/source-digest 포함: `(4095−1023)×2 = 6,144`
- 둘 다 없고 `repeated=0`: `1,023`
- 둘 다 없고 `repeated=1`: lane-log 전용 3칸은 `StageError`, 나머지 `1,020`
- convergence 비트와 `repeated=1`: `2¹¹ = 2,048`

[`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)의 미지 값은 실제로 0 취급이다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

그러나 v18은 모든 후보의 `terminal_action()`을 먼저 검증한다. 잘못된 `then`, 비-retry의 `then`, 미지 action은 `worst_status()`에 도달하기 전에 `StageError`가 되므로 R6은 fail-closed다.

## C. 과거 지적 폐쇄

### B-1~B-7

| ID | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β, 부분집합 선검사, T-1/T-2가 정합하며 반복 convergence는 출구에서 도달 불능 |
| B-2 | closed | 출구 12 ID 골든과 input-digest 진입 예외를 분리 |
| B-3 | closed | 99fad78 구현에서 B보다 먼저 골든을 생성·커밋하며, AJ-1도 닫혀 수락 검증기 명세가 단일함 |
| B-4 | closed | `phases` 교집합 없이 판정점별 정확 등식 |
| B-5 | closed | 잘못된 `then` 세 형태와 미지 action을 관문·런타임 양쪽에서 거부 |
| B-6 | closed | kind 3종, upstream 호출자 0, `deferred/test_bound` 명시 |
| B-7 | closed | pytest와 7관문 전부 plain·`-O` |

### V-1~V-8

| ID | 판정 | 사유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역 패치 |
| V-2 | closed | `-I`, 명시 repo, provenance 6검사, 패키지 `__path__` 단일성 |
| V-3 | closed | 후속 1회차가 정확히 3개 `/retry-1/` 레인 |
| V-4 | closed | phase 타입·우주·유령 phase 거부 |
| V-5 | closed | 판정점 `{early, exit}` 유일성 및 출구 12-ID 우주 |
| V-6 | closed | 실행 가능한 predicate와 독립 고정식 |
| V-7 | closed | T-11 ⑤가 엔진·관문 종단 어휘를 연결 |
| V-8 | closed | 3개 예외 칸 및 격자/동률 순서 구별 |

### N-1~N-7

| ID | 판정 | 사유 |
|---|---|---|
| N-1 | closed | `out`을 `chdir` 전에 절대화 |
| N-2 | closed | 12개 phase 전건을 §1에 적었고 실측 일치 |
| N-3 | closed | B-0 병합 → 골든 커밋 → B 순서 고정 |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 시험점 |
| N-5 | closed | T-12 계약↔엔진 상수 양방향 다리 |
| N-6 | closed | early iff와 거짓 양성 차단 |
| N-7 | closed | 다섯 문언 모두 구체화 |

B~AI의 다른 지적을 다시 여는 변경은 없었다.

## D. 출구 convergence 도달 가능성

설계의 “조기 통과 후 출구 convergence 실패는 정상 레인 페이로드만으로 도달 불능”은 맞다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출한다.
- [`_execute_canonical_tail()`](/home/laptop/projects/patent-docent/engine/stages/read.py:830)은 입력 `decompose` 객체를 그대로 반환한다.
- 조기와 출구 모두 `decomposes[canonical_run]`을 사용한다.
- 양쪽 모두 claims를 deepcopy한 후 같은 `rewrite_claims()`를 거친다.
- [`convergence.check()`](/home/laptop/projects/patent-docent/reader/lib/convergence.py:86)의 여섯 축은 `SpecIndex`의 claims-derived independent/dependent/elements/additions만 읽는다.

수확까지 포함한 메모리 재현:

> `FINAL claim_diff_count=1 diffs=[('claims.applicant_interest[0].material_id', 'M11', 'M15')] baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

유일한 차이는 수렴축 밖이다. 따라서 제시할 “출구에서만 실패시키는 정상 페이로드”는 없다.

T-1은 실제 러너의 유일한 출구 호출점 [`read.py:1743`](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)이 조회하는 모듈 전역을 패치한다. 실제 서명도 `run_read_checks(ctx)`다. 그러므로 검사층 주입을 쓰면서도 `run_with_payloads`의 실제 러너 제어 흐름·재디스패치 판정을 통과하며 T28 §3③을 충족한다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest 영역 밖 값은 T29 승인 |
| ③ | 맞다 | `judged_at` 이름은 원장이 설계에 위임 |
| ④ | 맞다 | T-11 ⑤가 종단 어휘 두 벌을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 fail-closed 형식 |
| ⑦ | 맞다 | 미지 ID는 공식 12-ID 영역 밖 무효 입력이며 정상 값 공간 불변 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③이 관문에 직접 요구 |
| ⑨ | 맞다 | early 목록을 진입 가드가 실제 읽고 승인 상수와 대조 |
| ⑩ | 맞다 | 패치 전역·독립항 복제·컨텍스트 보존이 실물 서명과 일치 |
| ⑪ | 맞다 | 도달 불능 표지는 T28의 convergence 술어에만 부착 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용된 재량 |
| ⑬ | 맞다 | 판정점·ID 우주 고정은 형식 규율 |
| ⑭ | 맞다 | `-I`와 provenance 6검사가 기준 트리 import를 결속 |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 먼저 독립 커밋하기 위해 필요 |
| ⑯ | 맞다 | R9는 HEAD 선언이 이미 만족 |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이며 T-11 ⑥이 두 상수를 연결 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격이 failure 기계 필드를 전부 덮고 산문 둘만 내용 자유 |
| ⑳ | 맞다 | 독립항 복제는 convergence 한 검사·independent-count 한 축만 새로 실패 |

재정이 필요한 결정 공백은 없다.

## F. 관문 §2.7

| 관문 | 판정 | 집행 범위 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·kind·xor·산문 존재/타입 |
| G2 | covered | entry/exit/judged_here 우주, 차집합 양쪽 0, 선언 중복 |
| G3 | covered | `phases` 없는 정확 등식, 승인 3/8 집합, 엄격 int 예산 |
| G4 | covered | phase 형식·우주·exit 필수·early iff |
| G5 | covered | input-digest의 entry 표지·halt·points 부재·재시도 제외 |
| G6 | covered | R6 종단 어휘와 `then` 규율 |

§2.7 열거는 **36종**이다. 필수 역심기와 1차 도전 요구는 다음처럼 직접 포함된다.

- 행 없는 검사: ⑴
- 검사 없는 행 및 `read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 조기 선언 유령: ㉞
- 산문 필수성·타입: ㉟·㊱

G1~G6의 선언 범위에서 원장 위반인데 통과하는 변조는 찾지 못했다.

## G. M3 결정 공백

**없음.**

특히 다음 선택이 모두 고정돼 있다.

- `tree_head=17`의 진단 ID와 평가 순서
- B-0의 세 산출물·검증기 적재 경로·clone 조립
- B-0 병합과 골든 커밋 및 라운드 B의 선후관계
- invalid `then`, 미지 ID, 중복 판정점의 처분
- T-1 주입 대상·주입 방식·기대 축
- T31/T32의 범위와 `screening_memos` 무접촉

## 검증 경로

주요 읽기 전용 명령과 마지막 출력은 다음과 같다.

- HEAD·보호 경로:

  ```bash
  git status --short
  git diff --name-only 9d2246b HEAD -- engine contracts reader tests tools
  git diff --name-only 663c77e HEAD -- engine contracts reader
  git rev-parse --short=12 HEAD
  ```

  > `FINAL status_rows=0 protected_9d_rows=0 protected_663_rows=0 head=9d2246b4d995`

- 기준 트리:

  ```bash
  git rev-parse 99fad78
  git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l
  ```

  > `99fad78c318875af99aa87083c029d2c6724e240`  
  > `0`

- 계약 선언 전수 적재:

  > `FINAL entry=['read.input-digest'] points=[('early', 1, ...), ('exit', 1, 'checks_before_exit')] ...`

  실측 phase 12건은 §1 목록과 전부 일치했다.

- 8,190칸 직접 호출:

  > `FINAL total=8190 beta=2048 mismatches=0 ... stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 후속 레인 계획:

  > `FINAL rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- 조기/출구 claims와 T-1 주입:

  > `FINAL claim_diff_count=1 ... baseline_failed=[] injected_failed=['read.convergence'] axes=[('independent-count', 'fail'), ...]`

- manifest 제약 정본 차집합:

  > `FINAL inspection=70 tv=70 dag=70 i-t=[] t-i=[] d-t=[] t-d=[] tree=['provenance.tree_head.eq']`

- 좌표 확인:

  ```bash
  rg -n '^retry_budget:|^checks_on_entry:|^checks_before_exit:|^failure:' contracts/stages/read.yaml
  rg -n '^def decompose_only_spec|^def assemble_spec|^def _failure_entry_for|^def _halts_immediately|^def _failure_verdict' engine/stages/read.py
  ```

  요청된 주요 좌표는 각각 `217`, `333`, `540`, `693` 및 `506`, `980`, `1893`, `1929`, `1937`로 실물과 일치했다.

## [미검증]

- v18은 리포 파일이 아니라 첨부 전문이므로 §2.8의 70개 ID는 첨부에서 직접 전사해 정적 대조했다.
- `generate.py`, `validate_manifest.py`, manifest, `check_failure_table.py`와 신규 시험은 아직 존재하지 않아 실행할 수 없었다.
- B-0 clone/worktree/골든 생성은 파일 쓰기를 수반하므로 실행하지 않았다.
- T-1/T-2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았다. 대신 함수 서명·패치 도달점·컨텍스트·검사 결과·레인 계획을 메모리에서 검증했다.
- 전체 pytest와 관문 plain·`-O`는 read-only 규율상 실행하지 않았다.
- 리포에는 아무것도 쓰지 않았고 최종 작업 트리와 보호 경로 diff는 빈 출력이다.