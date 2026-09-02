# 독립 감수 원문 — 재정 T26 집행 설계 v10 의 M1b 설계 도전(9차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v10/final.txt` 의 sha256 `9b9196315e2b39daf839afbe995f1b6f5a417e13aa023b6419cd9bc819927ac0` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 22분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 9차 심사** — v9(8차 FAIL · AB-1·AB-2) → **v10** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`c57b887` · 8차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 5건(MED 3 · LOW 2 · BLOCKER·HIGH 0) · 새 재정 사항 0 · AB-1·AB-2 partially · 그 밖 전건 closed. 다섯 전부 문서 내부 정합.**
값 8,190 칸은 아홉 번째로 일치. **AC-1**: T-7 의 `__file__` 은 `tests/test_m24_failure_grid_golden.py` 라 「생성기와 같은」 `with_name` 이
`tests/validate_manifest.py` 를 가리킨다(파일 부재 → pytest 실패) · **AC-2**: `cell_key` 정본이 본문과 예시(`**` 포함)에서 다르고 `generation_command` 가
「네 줄」·「블록 그대로」·물리 6줄로 어긋남 · **AC-3**: 골든 커밋 열거가 검증기를 빠뜨리고 B-0 worktree 미커밋 산출의 main 승격 절차가 없음 ·
**AC-4**: T-7 이 「§2.8 ①~⑥」을 가리키는데 목록은 ①~③ + 총괄 검수 ④ · **AC-5**: `assemble_spec :505-556` 은 `:506-561`.

지적 열거 = AC-1, AC-2, AC-3, AC-4, AC-5

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§15** 에 있다.
다섯 전부 **수용**(문서 정합 · 규율 11 ③) — **v11** 에 반영하고 10차 도전에 냈다. v11 = 호출자별 검증기 경로(생성기 `with_name` · T-7·B-0 시험은
`tests/` 에서 내려감 · B-0 시험 파일 위치를 `tests/test_m24a_failure_grid_generator.py` 로 고정해 T-7 과 같은 경로식을 미리 실행) · `cell_key`·
`generation_command` 정본을 각각 한 자리로(생성 명령 블록을 정확히 네 줄로 재작성) · B-0 병합 커밋(세 파일 · C′ 절차) → 골든 커밋(manifest) →
라운드 B 순서 명시 · T-7 = §2.8 시험 ①~③ · 좌표 정정.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

AB-1은 `partially`, AB-2도 `partially`입니다. 격자 값·계수·β·도달 불능·관문 본체는 맞지만, 골든 검증기 배선과 정본 문자열 및 B-0 산출물 승격 순서가 아직 M3의 임의 선택을 요구합니다.

## AB-1·AB-2 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AB-1 | partially | 모든 필드에 검사가 생긴 것은 맞다. 그러나 `cell_key`의 정확 리터럴이 본문과 manifest 예시에서 다르고, `generation_command`가 “네 줄”과 “블록 그대로”로 충돌한다(AC-2). |
| AB-2 | partially | 생성기에서는 `Path(__file__).with_name(...)`가 올바른 형제 파일을 가리킨다. 하지만 T-7의 `__file__`은 `tests/test_m24_failure_grid_golden.py`이므로 같은 코드는 `tests/validate_manifest.py`를 가리킨다(AC-1). |

## 지적 목록

### AC-1 · MED · 설계 §2.8 검증기 적재 방식·T-7

“생성기와 T-7 둘 다” 다음 코드를 쓴다는 명세가 T-7에서 틀립니다.

```python
Path(__file__).with_name("validate_manifest.py")
```

- 생성기 → `tests/fixtures/read-failure-grid/validate_manifest.py`: 맞음
- T-7 → `tests/validate_manifest.py`: 틀림
- 실제 검증기 위치 → `tests/fixtures/read-failure-grid/validate_manifest.py`

실측:

> `FINAL ... t7_with_name=/home/laptop/projects/patent-docent/tests/validate_manifest.py expected_validator=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py generator_with_name=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py`

그대로 구현하면 필수 pytest가 파일 부재로 실패합니다.

닫는 법: 호출자별 경로를 따로 고정하십시오.

- 생성기: `Path(__file__).with_name("validate_manifest.py")`
- T-7: `Path(__file__).parent / "fixtures" / "read-failure-grid" / "validate_manifest.py"`

두 경로를 각각 `is_file()`로 선검사하고, B-0 시험에서 생성기 subprocess와 T-7 적재 경로를 둘 다 실행해야 합니다.

### AC-2 · MED · 설계 §2.8 manifest 정본 리터럴

정확 상등을 요구하면서 정답 문자열이 하나로 정해지지 않았습니다.

1. 검증기 항목의 `cell_key`에는 `이 파일의`라고 되어 있지만 manifest 예시에는 `**이 파일의**`라고 되어 있습니다. JSON 코드 블록 안의 `**`는 실제 문자열 문자이므로 둘은 다릅니다.
2. `generation_command`는 “생성 명령 블록의 네 줄”이라고 했지만 블록은 물리적으로 6줄, 논리 명령으로 5개입니다. manifest 예시는 다시 “위 블록 그대로”라고 합니다.

따라서 M3는 어느 문자열을 상수로 둘지 골라야 하고, 반대쪽 문언과는 반드시 어긋납니다.

닫는 법: 두 값을 이스케이프까지 포함한 단일 정본 리터럴로 제시하고, 예시도 그 리터럴과 바이트 동일하게 고치십시오. `generation_command`는 포함할 명령들을 번호 목록 또는 `repr()` 가능한 단일 문자열로 고정해야 합니다.

### AC-3 · MED · 설계 §2.8·§2.11·§6 B-0 → 골든 커밋

B-0 산출물에는 `validate_manifest.py`가 포함되지만, 두 곳의 골든 커밋 열거는 반복해서 다음만 적습니다.

> 생성기 + 시험 + manifest

검증기가 빠져 있습니다. 더구나 B-0 레인은 `round-b0` worktree에서 커밋하지 않고, 이후 생성 명령은 `<main>/tests/.../generate.py`를 실행합니다. B-0의 미커밋 산출물을 main에 어떻게 승격하는지도 없습니다.

검증기를 제외하면 라운드 B의 T-7은 AC-1을 고쳐도 적재할 파일이 없습니다. 포함하면 명시된 커밋 열거를 임의로 넓혀야 합니다.

닫는 법: 순서를 다음처럼 명시하십시오.

1. B-0 diff를 총괄이 main에 적용
2. `generate.py`, `validate_manifest.py`, 단위 시험을 먼저 main에서 확인
3. manifest 생성
4. 네 종류 모두를 골든 커밋에 포함
5. 라운드 B가 그 커밋에서 시작

### AC-4 · LOW · 설계 §2.9 T-7

T-7은 “§2.8 ①~⑥”을 수행한다고 하지만 현재 §2.8의 시험 목록은 ①~④이고, ④는 총괄 스크래치 검수라 시험이 아닙니다. ⑤·⑥의 대상이 없습니다.

닫는 법: T-7의 실제 범위를 §2.8 시험 ①~③으로 고치고, 총괄의 외부 검수 ④를 별도 수락 단계로 유지하십시오.

### AC-5 · LOW · 설계 §1 실물 좌표

`assemble_spec :505-556`은 정확하지 않습니다. 함수 정의는 [read.py:506](/home/laptop/projects/patent-docent/engine/stages/read.py:506)이고 반환 블록은 561행까지입니다. 핵심 `rewrite_claims` 좌표 532~533은 맞습니다.

닫는 법: 범위를 `:506-561`로 고치십시오.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1·§2.2·§2.6·G1/G2 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·§2.6; 전수 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | §2.3·G2~G4·`_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | partially | 값은 맞지만 골든 적재·정본 문자열·커밋 순서가 AC-1~AC-3 |
| T26 §3③ 양방향 관문·세 심기 | covered | G1~G6·⑴~㉛ |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | partially | 명령은 모두 있으나 그 pytest에 속한 T-7이 AC-1로 실행 불능 |
| T28 §3① 8,190칸 한 칸도 불변 | partially | 값·모형은 전건 일치, 파일 수락 경로가 AC-1~AC-3 |
| T28 §3② β 표지 | partially | 술어·집합·계수는 맞지만 검증기 수락 경로와 정본 문자열이 미완 |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2; 실물 주입과 0/3 레인 정합 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 12 id | partially | 목록·유일성·우주는 맞지만 T-7 적재/커밋 경로가 끊김 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ entry 표지·halt·출구 재시도 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미룬 것과 T32를 그 소라운드에 합치는 것은 각각 T31 §3①과 T32 §3⑤에 맞습니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, R8/R9, 미지 id fail-closed, B-0, provenance 검사, 승인 상수, binding 분류는 공학 재량 또는 원장값의 기계적 기록입니다. AC-1~AC-4도 새 Owner 재정 없이 고칠 수 있는 공학 오류입니다.

## B. 오늘의 표 불변

HEAD `_failure_verdict`를 전수 호출하고 v10 11행 모형을 독립 실행한 결과입니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v10 모형↔HEAD 불일치 | 0 |

`StageError`는 정확히 `1024:1`, `2048:1`, `3072:1`입니다. §2.2 손검산과 §3 대표 칸에서 틀린 칸은 찾지 못했습니다.

현재 [worst_status](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 status를 0으로 취급합니다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

v10은 `select_failure_row()`가 모든 후보를 `terminal_action()`으로 먼저 검증하므로, R6 구현을 그대로 따르면 이 fail-open 경로에 도달하지 않습니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β·부분집합 우선·실러너 주입·양성 대조가 성립 |
| B-2 | closed | 출구 12개·8,190칸·input-digest 별도 경로 |
| B-3 | partially | `99fad78` 독립 생성 원리는 맞지만 골든 수락·승격 경로가 AC-1~AC-3 |
| B-4 | closed | `phases` 없이 정확 등식이 선다 |
| B-5 | closed | 세 잘못된 `then` 형태를 관문·런타임 모두 거부 |
| B-6 | closed | kind 3종·upstream 호출자 0·deferred/test_bound |
| B-7 | closed | 요구된 두 모드와 관문 전종 명령 자체는 명시됨 |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `read_stage.run_read_checks`를 패치 |
| V-2 | closed | `-I`·repo 선삽입·6 provenance 검사로 엔진 출처 고정 |
| V-3 | closed | `/retry-1/` 3행과 세 task 정확 |
| V-4 | closed | phase 우주·형식 검사 |
| V-5 | closed | 판정점 유일성·12-id 우주 |
| V-6 | closed | 실행 가능한 정확 predicate |
| V-7 | closed | T-11 ⑤ 종단 어휘 상등 |
| V-8 | closed | StageError 3칸·두 순서 구별 |

AC-1은 V-2의 엔진 출처 문제가 아니라 새 형제 검증기의 T-7 적재 좌표 문제입니다.

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전 절대화 |
| N-2 | closed | 12개 phase 전건 실측과 일치 |
| N-3 | partially | B-0이라는 좌석·시점은 생겼지만 검증기 승격·골든 커밋 포함이 AC-3로 불완전 |
| N-4 | closed | `_exit_retry_eligible` 명명·직접 시험 |
| N-5 | closed | T-12 계약↔엔진 상수 양방향 다리 |
| N-6 | closed | `early` iff·exit 필수 |
| N-7 | closed | 다섯 문언 모두 구체화됨 |

W·X·Y·Z는 다시 열리지 않았습니다. AA-1~AA-3도 closed이고, AA-4는 AC-1·AC-3 때문에 다시 `partially`입니다.

## D. 출구 convergence 도달 가능성

설계의 결론은 맞습니다.

- [decompose_only_spec](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 [assemble_spec](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- tail은 입력 `decompose`를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 같은 `decomposes[canonical_run]`을 사용합니다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 양쪽은 claims를 deepcopy한 뒤 같은 `rewrite_claims`를 호출합니다([read.py:532](/home/laptop/projects/patent-docent/engine/stages/read.py:532)).
- 완성 claims는 조기 claims와 바이트 동일하지는 않았습니다. `applicant_interest[0].material_id`가 `M11→M9`로 달랐습니다. 하지만 그 필드는 수렴 6축이 읽지 않습니다.
- [convergence.py](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)의 6축은 `independent`, `dependents`, `elements`, `element_parent`, `element_claim`, `claims`, `additions`만 사용합니다. 후속 산출이 바꾸는 수렴 관측 필드는 없습니다.
- `peer_spec`의 실제 읽기는 [convergence.py:94](/home/laptop/projects/patent-docent/reader/lib/convergence.py:94)와 [convergence.py:105](/home/laptop/projects/patent-docent/reader/lib/convergence.py:105)뿐입니다.

실측:

> `FINAL claims_equal=False base_status=pass base_failed=[] injected_status=fail changed_axes=['independent-count'] other_peer_reads=[]`

따라서 조기 통과 뒤 레인 페이로드만으로 출구 convergence를 실패시키는 페이로드는 없습니다. T-1의 검사층 주입은 [read.py:1743](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)의 실제 러너 호출점을 타며 T28 §3③을 충족합니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | T29 승인 값 |
| ③ | 맞다 | 키 이름은 T29가 설계에 위임 |
| ④ | 맞다 | T-11 ⑤가 두 종단 어휘를 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 공식 12-id 밖 무효 입력이며 StageError는 fail-closed |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 가드가 early·exit 목록을 실제 읽고 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 검사기 자체의 `independent-count`를 fail로 만듦 |
| ⑪ | 맞다 | 도달 불능 표지 대상은 T28 술어 하나 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용 |
| ⑬ | 맞다 | 판정점·검사 id 우주 고정은 형식 규율 |
| ⑭ | 맞다 | 실행된 생성기의 출처 증명에는 `-I`+6검사가 충분; AC-1은 T-7 적재 전 문제 |
| ⑮ | 맞다 | B-0 분리는 허용된 좌석 판단. 다만 산출물 승격 절차는 AC-3으로 불완전 |
| ⑯ | 맞다 | R9는 정본 실물과 일치 |
| ⑰ | 맞다 | 승인 3/8은 원장값이며 T-11 ⑥이 두 상수를 잇는다 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격은 원장값의 독립 오라클 |
| ⑳ | 맞다 | 주입은 실제로 `independent-count` 하나만 fail |

새 Owner 재정이 필요한 자기 신고 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 근거 |
|---|---|---|
| G1 | covered | 11행·분할·순서·action·then·label·points 고정 |
| G2 | covered | 선언↔행 차집합 양쪽 0·배열 중복 거부 |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1 |
| G4 | covered | phase 형식·우주·exit 필수·early iff |
| G5 | covered | input-digest entry·halt·points 부재·재시도 제외 |
| G6 | covered | 세 잘못된 `then` 형태 거부 |

v10은 16종이 아니라 ⑴~㉛ 31종을 열거합니다. 필수 심기는 모두 있습니다.

- 행 없는 검사: ⑴
- 검사 없는 행과 `read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶·⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 동시 일관 변조: ㉑
- 중복 선언: ㉒·㉓
- 행 병합·순서: ㉕·㉖
- 예산 값·타입: ㉙~㉛

명세된 G1~G6 축을 통과하는 계약 변조는 찾지 못했습니다. 이번 FAIL은 관문이 아니라 골든 검증기 수락·적재·승격면입니다.

## G. M3 결정 공백

최소 네 곳입니다.

1. T-7에서 검증기를 어느 경로로 적재할지(AC-1).
2. `cell_key`의 `**` 포함 여부와 `generation_command`의 실제 정본 문자열(AC-2).
3. B-0 worktree의 미커밋 검증기를 main으로 어떻게 승격하고 골든 커밋에 포함할지(AC-3).
4. T-7의 “§2.8 ①~⑥” 중 존재하지 않는 ⑤·⑥을 구현할지, ①~③만 따를지(AC-4).

모두 공학 보수 사항이지만, 현재 문언대로라면 M3가 임의 선택해야 하므로 FAIL입니다.

## 검증 경로

- 상태·불변성:

  `git rev-parse --short=7 HEAD` → `1fdb2c7`  
  `git status --short` → 빈 출력  
  `git diff --name-only 1fdb2c7 HEAD -- engine contracts reader tests tools | wc -l` → `0`  
  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l` → `0`

- 기준 해시:

  `git rev-parse 99fad78`

  > `99fad78c318875af99aa87083c029d2c6724e240`

- `_failure_verdict` 전수 호출 + 독립 11행 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 halt_null=6144 escalate_null=1023 escalate_repeat=1020 stage_error=3 stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 선언·국면:

  > `FINAL point_ids=['early', 'exit'] point_unique=True exit_count=12 exit_unique=True entry_ids=['read.input-digest'] code_counts=(10, 2) bridge=True early=['read.claim-inventory', 'read.convergence', 'read.dependency-parse'] early_expected=['read.claim-inventory', 'read.convergence', 'read.dependency-parse'] r9_violations=[]`

- 조립·주입:

  > `FINAL claims_equal=False base_status=pass base_failed=[] injected_status=fail changed_axes=['independent-count'] other_peer_reads=[]`

- 재시도 레인:

  > `FINAL retry_lane_rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] all_retry1=True repeated_and_convergence_reachable=False`

- `-I` 및 형제 경로:

  > `FINAL isolated=1 safe_path=True script_dir_present=False t7_with_name=/home/laptop/projects/patent-docent/tests/validate_manifest.py expected_validator=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py generator_with_name=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py`

- 신설물:

  > `generate.py=absent`  
  > `validate_manifest.py=absent`  
  > `manifest.json=absent`  
  > `tests/test_m24_failure_grid_golden.py=absent`  
  > `tools/check_failure_table.py=absent`

## [미검증]

- 신설 5개 파일이 아직 없으므로 생성기·검증기·T-7·관문을 실제 실행하지 못했습니다.
- detached `99fad78` worktree 생성은 쓰기 작업이므로 실행하지 않았습니다.
- 전체 pytest와 관문 plain/`-O`는 캐시·임시 파일을 만들 수 있어 실행하지 않았습니다.
- T-1/T-2 완성 시험은 아직 없어, 조립·검사기 주입·레인 계획을 메모리에서 각각 검증했습니다.
- AC-2~AC-4는 첨부된 v10 문언 자체의 상호 대조 결과입니다. v10 파일은 리포에 존재하지 않습니다.