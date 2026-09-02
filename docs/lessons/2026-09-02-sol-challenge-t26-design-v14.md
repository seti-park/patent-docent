# 독립 감수 원문 — 재정 T26 집행 설계 v14 의 M1b 설계 도전(13차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v14/final.txt` 의 sha256 `75b02bf306b68b841afb24fa3951869fcb85559c446675ef1ef7691fcaadb2eb` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 24분 · resume 없이 1차 완주 · 2026-09-02 23:57 기동 → 09-03 00:21 종료). **ROUTING M1b 설계 도전의 13차 심사** — v13(12차 FAIL · AF-1~AF-3) →
**v14** 에 대한 것. 도전 중 총괄이 문서 전용 커밋(`2d55128` · 12차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다.

**판정 = FAIL · 지적 2건(HIGH 1 · MED 1 · BLOCKER 0) · 새 재정 사항 0 · AF-2·AF-3 closed · AF-1 partially · 그 밖 전건 closed.** 값 8,190 칸은
열세 번째로 일치. **AG-1**: 표 T-V 가 아직 독립 제약 전부를 열거하지 않는다 — `exceptions[0]` 이 dict 인지(`[17]` 통과) · 경로 배열 원소의 str 타입 ·
셀 문자열 갈래가 정확히 `"StageError"` 인지(`"NotStageError"` 통과) · 표에 `subset_of_cells` 가 ID 열에 남아 집합이 단일하지 않음 · `<k>` 표기가 실제 ID
문자열이 아님 · 필드 간 선행조건 DAG 미명시. **AG-2**: G1 이 `condition`·`note` 를 선택 키로 허용해 1행 `condition` 삭제가 관문·T-13·T-10 전부 통과 —
T26 ⒜ ① 「조건 문장은 사람용 설명으로 남긴다」와 어긋남.

지적 열거 = AG-1, AG-2

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§19** 에 있다.
둘 다 **수용**(공학 · 규율 11 ③) — **v15** 에 반영하고 14차 도전에 냈다. v15 = ID 셋 추가(`exception.item.type` · 경로 배열 `items.str` · `cells.value.sentinel`) ·
`subset_of_cells` 를 표에서 제거(함의 설명만) · `<k>` 를 다섯 슬러그 × 2 = 열 개 ID 문자열로 전개(`COUNT_KEY_SLUGS`) · **선행조건 DAG** 절 · G1 이 모든 행에
`condition`·`note` 를 비공 str 로 필수(정본 10행 전부 둘을 든다 — 총괄 실측) · 변조 ㉟㊱.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

## AF-1~AF-3 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AF-1 | **partially** | predicate/cells 분리, 정확한 진단 집합, `reader_path.type`, 전 expected-count 키, 컨테이너/길이 분리 등 기존 반례는 고쳤다. 그러나 독립 타입·값 제약과 T‑V 변조가 아직 빠져 있다(AG-1). |
| AF-2 | **closed** | 미커밋 생성기·검증기를 clone에 복사하고 임시 커밋한 뒤 그 7자리 HEAD를 `BASE`로 쓰는 절차가 provenance ⓓ·ⓕ와 정합한다. |
| AF-3 | **closed** | R2/G2가 `early_phase_spec.judged_here`를 우주에 포함하고 세 선언 집합을 정확히 대조한다. 정본도 세 집합이 일치했다. |

## 지적 목록

### AG-1 · HIGH · 설계 §2.8 검증기·표 T‑V·B-0/T-7 ③

T‑V가 아직 검증기의 독립 제약 전부를 열거하지 않습니다.

구체적으로 빠진 수락면은 다음과 같습니다.

- `exceptions`가 list이고 길이 1인지는 보지만 `exceptions[0]`이 dict인지 검사하는 `exception.item.type`이 없습니다. `exceptions: [17]`은 기존 두 제약을 모두 만족합니다. M3는 예외, 무시, `exception.keys.exact`에 타입을 합칠지 임의 선택해야 합니다.
- `engine_path`·`reader_path`는 컨테이너 type과 len1은 나뉘었지만 원소의 str 타입과 절대경로가 다시 한 ID에 묶였습니다. `[17]` 변조가 없습니다.
- 셀 값의 문자열 갈래는 정확히 `"StageError"`여야 하지만 `cells.value.type` 변조는 정수만 시험합니다. 모든 문자열을 StageError로 취급하는 검증기와 `cells["1024:1"] = "NotStageError"`가 T‑V를 통과할 수 있습니다.
- 표의 제약-ID 열에 `exception.cells.subset_of_cells`가 실제로 적혀 있으면서 같은 칸과 아래 문장은 “ID를 두지 않는다”고 합니다. `CONSTRAINT_IDS == T-V ID 집합`의 문서상 집합이 단일하지 않습니다.
- `expected_counts.<k>.*`도 실제 `CONSTRAINT_IDS` 문자열 열 개가 아니라 `<k>` 표기로 남아 있습니다.

이는 AF-1의 “독립 제약 하나 = ID 하나, T‑V와 정확 상등”을 아직 끝내지 못한 것입니다. 특히 잘못된 `exceptions[0]` 처리는 T28 β 표지의 구조적 유효성을 어떤 진단으로 거부할지 결정하지 못하게 합니다.

닫는 법:

1. `exception.item.type`, `provenance.{engine_path,reader_path}.items.str`, `cells.value.string_sentinel` 같은 독립 ID와 단일 변조를 추가합니다.
2. `"StageError" → "__bogus__"` 변조를 넣고 정확히 sentinel ID 하나만 요구합니다.
3. `exception.cells.subset_of_cells`를 T‑V 표의 ID 열에서 완전히 제거하고 “다른 제약이 함의한다”는 설명만 별도로 둡니다.
4. `<k>`를 실제 열 개의 ID 문자열로 전개해 `CONSTRAINT_IDS`를 그대로 옮겨 적을 수 있게 합니다.
5. 필드 간 선행조건 DAG도 명시해 타입 실패 뒤 어떤 하위 검사를 생략하는지 고정합니다.

### AG-2 · MED · 설계 §2.2·§2.7 G1/T-13 · T26 §2⒜①

T26은 조건 문장을 사람용 설명으로 남기라고 했고, v14 §2.2도 `condition`·`note`를 각 행에 맞게 옮긴다고 합니다. 그러나 G1과 T-13은 승인 기계 키만 필수이고 `{condition, note}`는 선택 키로 허용합니다.

따라서 1행에서 `condition`만 삭제한 변조는 다음을 모두 통과합니다.

- G1: 승인 기계 키를 모두 포함하고 허용 키의 부분집합이다.
- G2~G6: `condition`을 보지 않는다.
- T-13: G1과 같은 키 규칙이다.
- T-10: 다른 열 행들에 `condition`이 남아 있으므로 전체 사용 키 합집합은 변하지 않는다.
- 개정 시험들은 condition needle 조회를 폐기한다.

직접 식을 계산한 결과도 다음과 같습니다.

> `FINAL g1_accepts_condition_delete=True mutant_keys=['action', 'checks', 'note', 'points', 'then']`

닫는 법: 모든 failure 행의 `condition`을 필수 비공 문자열로 G1에 넣고, 삭제 및 비문자열 변조를 `--self-test`와 T-13에 추가하십시오. `note`도 정말 전 행 필수라면 같은 규칙을 적용하고, 아니라면 §2.2 문언을 선택 필드라고 고쳐야 합니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 ID 키·조건 설명 존치 | **partially** | §2.1·§2.2·§2.6의 ID 키는 맞지만 G1이 `condition` 삭제를 허용한다(AG-2). [T26 원문](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-01-T24-T27.md:177) |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·`select_failure_row`; 전수 불일치 0. |
| T26 §2⒜③ 완전성·정확 등식·실제 부분집합 | covered | §2.1 R2/R8/R9·§2.3·G2/G3/G4. 조기 선언도 포함한다. |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11. |
| T26 §3② 오늘 표 불변 | covered | §2.8 T-7가 manifest 키가 아닌 독립 우주를 전수하고 런타임 값과 대조한다. |
| T26 §3③ 양방향 관문·세 심기 | covered | ⑴·⑵·⑶/⑷/㉑이 필수 세 종류를 덮는다. |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10의 7관문 정정 마커. |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11. |
| T28 §3① 8,190칸 값 불변 | covered | §2.8 T-7 ②; 실측 불일치 0. |
| T28 §3② β 표지 2,048칸 | **partially** | 정상 표본의 술어·집합은 맞지만 표지 객체 타입 수락면이 AG-1로 불완전하다. |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2; 주입 결과와 3개 retry-1 레인을 실측했다. |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3. |
| T29 §3① 골든 12 ID | covered | §2.8 exact set·T-7·T-12. |
| T29 §3② 진입 예외 반증 | covered | T-3. |
| T29 §3③ 진입 표지·halt·출구 제외 | covered | §2.4·G5. |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1. |
| T30 §3② checks xor kind | covered | R4·G1. |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9. 실측 호출자 0. |
| T30 §3④ SPEC 문서화 | covered | §2.10. |

T31을 B 뒤 소라운드로 미룬 판단과 T32를 그 소라운드에 합치는 판단은 각각 원장과 맞습니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, 미지 ID fail-closed, 승인 상수, provenance 거부, B-0 분리는 공학 재량 또는 원장값의 기록입니다. AG-1·AG-2 모두 새 Owner 재정 없이 수정할 수 있습니다.

## B. 오늘의 표 불변

전수 결과는 정확합니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v14 모형 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`입니다. §2.2 손검산과 §3 대표 칸에서 틀린 출력 칸은 찾지 못했습니다.

`worst_status()`는 실제로 미지 값을 0으로 취급합니다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

그러나 v14는 모든 후보의 `terminal_action()`을 먼저 호출하도록 명시합니다. 따라서 다음은 `worst_status()` 도달 전에 `StageError`여야 합니다.

- `then` 없는 `retry(n)`
- `then: retry(n)`
- 비-retry 행의 `then`
- 미지 terminal action

이 선검증 순서가 지켜지면 R6은 맞습니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β의 부분집합 검사가 서명 검사보다 앞이고 T-1/T-2가 올바른 전역을 패치한다. |
| B-2 | closed | 출구 12 ID·8,190칸·input-digest 진입 예외가 분리됐다. |
| B-3 | **partially** | 99fad78 트리에서 값을 만드는 독립성은 섰고 AF-2도 닫혔다. 다만 manifest 수락면이 AG-1로 아직 완결되지 않았다. |
| B-4 | closed | `phases` 교집합 없이 판정점별 등식이 정확히 선다. |
| B-5 | closed | 잘못된 `then` 세 형태와 미지 action을 관문·런타임 모두 fail-closed 처리한다. |
| B-6 | closed | kind 3종·upstream 호출자 0·이연 결속이 정확하다. |
| B-7 | closed | pytest 및 7관문 plain/`-O` 명령이 명시됐다. |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역 패치. |
| V-2 | closed | `-I`, 명시 repo, provenance 6검사가 기준 트리 import를 묶는다. |
| V-3 | closed | retry-1은 정확히 3개 레인이다. |
| V-4 | closed | phase 형식·우주·유령 phase 거부. |
| V-5 | closed | 판정점 유일성·출구 12-ID 우주 고정. |
| V-6 | closed | 실행 가능한 고정 predicate와 독립 β 식. |
| V-7 | closed | T-11 ⑤ 종단 어휘 상등. |
| V-8 | closed | StageError 세 칸과 두 순서를 정확히 분리했다. |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전에 절대화한다. |
| N-2 | closed | 12개 phase 전건이 실측되어 있다. |
| N-3 | closed | B-0 → 임시 clone/commit → B-0 병합 → 골든 → B 순서가 완결됐다. |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 시험이 명명됐다. |
| N-5 | closed | T-12 계약↔엔진 상수 다리. |
| N-6 | closed | early iff와 거짓 양성 차단. |
| N-7 | closed | 다섯 문언 모두 구체화됐다. |

W~AD는 AG-1의 수락면 계열인 AD-1만 다시 부분적으로 연결됩니다. AE-1은 AF-1/AG-1로 `partially`; 나머지는 다시 열리지 않았습니다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞습니다.

- [`decompose_only_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- tail은 입력 `decompose` 객체를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 같은 `decomposes[canonical_run]`을 사용합니다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 두 조립 모두 claims를 deepcopy하고 같은 `rewrite_claims`를 적용합니다([read.py:528](/home/laptop/projects/patent-docent/engine/stages/read.py:528)).
- `SpecIndex`는 items/figures도 인덱싱하지만 수렴 여섯 축의 실제 helper는 claims에서 만든 independent/dependent/elements/additions만 사용합니다([convergence.py](/home/laptop/projects/patent-docent/reader/lib/convergence.py:49)).
- 최종 claims가 `applicant_interest.material_id` 때문에 바이트 동일하지는 않았지만 여섯 축은 모두 통과했습니다.

> `FINAL same_claims=False same_items=False status=pass axes=[('independent-count', 'pass'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

따라서 올바른 출구 전용 실패 페이로드는 제시할 수 없습니다.

T-1의 검사층 주입은 T28 §3③의 실제 러너 경로를 충족합니다. 실제 호출점은 [read.py:1743](/home/laptop/projects/patent-docent/engine/stages/read.py:1743) 하나이고, 독립항 복제 시 정상 corpus에서 실패 검사는 convergence 하나였습니다.

> `FINAL failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량. |
| ② | 맞다 | input-digest 영역 밖 값은 T29 승인. |
| ③ | 맞다 | `judged_at` 이름은 T29가 설계에 위임. |
| ④ | 맞다 | T-11 ⑤가 엔진·관문 종단 어휘를 대조한다. |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존한다. |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율. |
| ⑦ | 맞다 | 미지 ID는 공식 영역 밖 무효 입력이고 StageError는 fail-closed다. |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값이다. |
| ⑨ | 맞다 | early 목록은 진입 가드가 실제로 읽으며 why가 실행 결정과 대조만의 차이를 밝힌다. |
| ⑩ | 맞다 | 독립항 복제는 `independent-count`만 fail로 만든다. |
| ⑪ | 맞다 | T28 표지는 원장이 정한 술어 하나에만 단다. |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용된 재량이다. |
| ⑬ | 맞다 | 판정점·검사 ID 우주 고정은 정상 값 공간을 바꾸지 않는 형식 규율이다. |
| ⑭ | 맞다 | 실제 생성 경로의 `-I`와 provenance 6검사는 기준 트리 import를 충분히 묶는다. AG-1은 사후 manifest 형식 검증 문제다. |
| ⑮ | 맞다 | B-0 분리는 필요하고 AF-2의 clone 조립으로 순환이 닫혔다. |
| ⑯ | 맞다 | R9는 정본 선언이 이미 만족하는 등식을 검사한다. |
| ⑰ | 맞다 | 승인 3/8 집합은 원장값이고 T-11 ⑥이 두 상수를 잇는다. |
| ⑱ | 맞다 | 선언 중복 금지는 형식 규율이다. |
| ⑲ | 맞다 | 기계 필드 골격은 원장값 기록이다. 다만 산문 `condition`의 필수성은 AG-2로 별도 누락됐다. |
| ⑳ | 맞다 | 주입은 convergence 한 검사, independent-count 한 축만 실패시킨다. |

새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 이유 |
|---|---|---|
| G1 | **partially** | 기계 골격·행 순서·kind·xor는 고정하지만 `condition` 삭제를 통과시킨다(AG-2). |
| G2 | covered | entry/exit/judged_here 우주와 조기 세 벌 상등을 모두 본다. |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1을 집행한다. |
| G4 | covered | phase 형식·우주·exit 필수·early iff를 집행한다. |
| G5 | covered | input-digest entry·halt·points 부재를 집행한다. |
| G6 | covered | R6 전항을 집행한다. |

열거는 16종이 아니라 **㉞까지 34종**입니다. 원장의 필수 심기와 1차 도전 요구는 포함합니다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 조기 선언 전용 ghost: ㉞

관문이 통과시키는 구체적 변조는 **1행 `condition` 삭제**입니다.

## G. M3 결정 공백

두 곳이 남습니다.

1. `exceptions[0]`·path 원소·셀 문자열 sentinel의 타입/값 위반을 어느 제약 ID로 보고할지, 아니면 다른 제약과 묶을지(AG-1).
2. §2.2의 “condition을 옮긴다”와 G1의 “condition은 선택 키” 중 어느 쪽을 따를지(AG-2).

둘 다 Owner 재정이 아니라 설계자가 고쳐야 할 공학 공백입니다. 그러나 현재 v14 그대로는 M3가 임의 선택하거나 반려하게 되므로 FAIL입니다.

## 검증 경로

- HEAD·보호 경로·작업 트리:

  ```bash
  git status --short
  git diff --name-only 22429e4 HEAD -- engine contracts reader tests tools
  printf 'FINAL head='; git rev-parse --short=12 HEAD
  ```

  > `FINAL head=2d551289eb1d`

  도전 중 허용된 docs 전용 커밋이 들어왔고, 앞의 두 명령 출력은 비었습니다.

- 8,190칸 전수: `READ_CHECK_IDS + ENGINE_READ_CHECK_IDS`의 모든 비공집합과 repeated 0/1을 만들어 `_failure_verdict`를 직접 호출하고 v14 모형과 비교했습니다.

  ```bash
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c '<mask 1..4095 × repeated 0/1 전수 호출>'
  ```

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 선언·국면:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c '<read.yaml entry/exit/judged_here/points/phases 집합 계산>'
  ```

  > `FINAL exit_count=12 exit_unique=True entry=['read.input-digest'] judged=['read.claim-inventory', 'read.dependency-parse', 'read.convergence'] points=['early', 'exit'] early=['read.claim-inventory', 'read.convergence', 'read.dependency-parse'] judged_eq_points=True judged_eq_phases=True all_exit=True phase_universe=['early', 'exit']`

- T-1 주입의 검사 결과:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c '<정상 corpus peer의 독립항 하나 복제 후 run_read_checks>'
  ```

  > `FINAL failed=['read.convergence'] axes=[('independent-count', 'fail'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

- 재시도 레인 계획:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c '<attempt=1 plan_grounding + plan_synthesis>'
  ```

  > `FINAL rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- `worst_status`:

  > `FINAL known=halt unknown_only=ok mixed=escalate`

- 셸·격리 전제:

  > `FINAL invalid_base_rc=128`  
  > `FINAL isolated=1 no_user_site=1 safe_path=True`  
  > `FINAL protected_diff_count=0`

- G1 조건 삭제 논리:

  > `FINAL g1_accepts_condition_delete=True mutant_keys=['action', 'checks', 'note', 'points', 'then']`

- 좌표 검증에는 `nl -ba … | sed -n …`으로 [read.py](/home/laptop/projects/patent-docent/engine/stages/read.py:1476), [convergence.py](/home/laptop/projects/patent-docent/reader/lib/convergence.py:86), [read.yaml](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:217), [test_m21](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:60)을 직접 열었습니다.

## [미검증]

- `generate.py`, `validate_manifest.py`, 신규 두 시험, manifest, `check_failure_table.py`는 아직 없으므로 실행하지 못했습니다.
- B-0 clone/worktree/임시 commit/생성 명령 블록은 파일을 만들므로 read-only 규율상 실행하지 않았습니다.
- 전체 pytest 및 관문 plain/`-O`는 캐시·임시 산출 가능성 때문에 실행하지 않았습니다.
- T-1/T-2의 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았습니다. 검사층 주입 결과와 레인 계획은 메모리에서 검증했습니다.
- 리포에는 아무것도 쓰지 않았고 최종 작업 트리는 깨끗했습니다.