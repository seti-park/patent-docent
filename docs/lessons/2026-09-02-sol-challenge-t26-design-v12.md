# 독립 감수 원문 — 재정 T26 집행 설계 v12 의 M1b 설계 도전(11차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v12/final.txt` 의 sha256 `1f461b73c8522b2a526c38bb44172d1939d5297711a9de5b3f481eedee917e7d` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 18분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 11차 심사** — v11(10차 FAIL · AD-1~AD-3) → **v12** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`7d01009` · 10차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 3건(HIGH 1 · MED 2 · BLOCKER 0) · 새 재정 사항 0 · AD-2 closed · AD-1·AD-3 partially · 그 밖 전건 closed.** 값 8,190 칸은
열한 번째로 일치. **AE-1**: 표 T-V 가 「필드 하나씩」이지 「제약 하나씩」이 아니다 — 한 토큰 아래 여러 제약(집합 상등 · 길이 · 고유 · 타입 · 부분 문자열 셋)이
겹쳐 검사 하나를 빼도 전건 통과(예: `read.schema → read.__ghost__` 치환은 길이·고유·convergence 를 유지해 집합 상등 검사가 없어도 T-V 를 통과) ·
**AE-2**: 생성 명령 둘째 줄 `test "$(git diff … | wc -l)" = 0` 은 명령 치환 안의 파이프 실패를 삼킨다(`set -e` 미발동 · 실측 `substitution_pipeline_failure_survived=yes`) ·
**AE-3**: 정본 블록이 `$MAIN/.venv/bin/python` 을 고정하는데 B-0 성공 시험의 `MAIN` 은 시험용 클론이라 `.venv` 가 없고(`venv_tracked=no`), `BASE` 가
전체 해시인지 7자인지 미정.

지적 열거 = AE-1, AE-2, AE-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§17** 에 있다.
셋 전부 **수용**(공학 · 규율 11 ③) — **v13** 에 반영하고 12차 도전에 냈다. v13 = 검증기 진단 코드를 **제약 ID**(모듈 상수 `CONSTRAINT_IDS` · 독립 제약
하나 = ID 하나)로 · 표 T-V 를 제약 ID 단위(각 행 = 그 제약만 깨는 변조 · 약 60행)로 재작성 · B-0 시험이 `CONSTRAINT_IDS` 와 표의 양방향 상등 +
각 변조의 그 ID 위반 실재를 검사 · 생성 명령 둘째 줄을 `git diff --quiet` 로 · `PYTHON_BIN` 매개 추가 · B-0 의 `BASE` 는 `git rev-parse --short=7` · ⒟ 역프로브.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

v12는 값 격자와 AD-2를 바로잡았지만, 그대로 M3에 넘길 수는 없습니다. AD-1의 독립 제약 결속이 여전히 불완전하고, AD-3 셸 블록에는 파이프 오류를 삼키는 자리와 B-0 시험용 클론의 Python 경로 공백이 남습니다.

## AD-1~AD-3 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AD-1 | **partially** | T‑V가 필드별 토큰 검사로 개선됐지만, 한 필드에 여러 독립 제약이 있는 경우를 분리하지 못한다. AE-1 |
| AD-2 | **closed** | `judged_at` 열, 3행만 `entry`, 행별 허용 키 집합, 미지 키 거부가 G1과 T-13에 모두 명시됐다. |
| AD-3 | **partially** | `set -euo pipefail`, `trap`, 생성기 파이프 상태, 마지막 `EXIT=0` 검사는 생겼다. 그러나 사전조건 파이프 오류가 삼켜지고, B-0 정상 클론에는 지정 Python이 없다. AE-2·AE-3 |

## 지적 목록

### AE-1 · HIGH · 설계 §2.8 검증기·표 T‑V·T-7 ③

T‑V는 “필드 하나씩”이지 “독립 제약 하나씩”이 아닙니다. 같은 토큰 아래 여러 제약이 겹쳐 있어 일부 검사를 빼도 모든 음성 시험을 통과할 수 있습니다.

구체적인 누락 가능성:

- `check_ids`: 중복 13항·빈 문자열·convergence 삭제만 있다. `read.schema → read.__ghost__`처럼 길이 12·고유·비공 문자열·convergence 포함을 유지하는 치환이 없다. 따라서 `set(check_ids) == expected_check_ids` 검사를 빼도 T‑V 전건을 통과한다.
- `$comment`: 빈 문자열과 `"T28"` 삭제만 있다. `"T26 §3 ②"` 또는 `"T29"` 검사만 빼도 전건 통과한다.
- `provenance.engine_path`: 원소 둘만 심는다. 단일 상대경로는 절대경로 검사를 빼면 통과한다.
- `expected_counts`: `total`만 float를 심는다. 예를 들어 `"escalate/null": 1023.0`은 Python 값 등식상 `1023`과 같으므로 개별 계수의 `type is int` 검사를 빼도 통과한다.
- `exceptions[0].cells`도 list/원소 타입/비공/집합 등식이 같은 토큰에 묶여 제약별 결속이 아니다.

즉 AB-1의 “값·형식 제약 전부 검사”는 여전히 수락 시험으로 증명되지 않습니다.

닫는 법: 필드 토큰 대신 제약 ID를 진단 코드로 두고, 각 제약만 단독으로 깨지는 변조를 하나씩 둬야 합니다. 예:

- `check_ids.expected_set`: 정상 id 하나를 `read.__ghost__`로 치환
- `$comment.contains.T26`, `.T28`, `.T29`: 각각 하나만 제거
- `provenance.engine_path.absolute`: 원소 하나인 상대경로
- `expected_counts.escalate/null.type`: 값은 같은 float
- 컨테이너 타입, 원소 타입, 고유성, 길이, 정확 집합을 각각 별도 변조

### AE-2 · MED · 설계 §2.8 생성 명령 둘째 줄

다음 줄은 내부 `git diff` 파이프의 실패를 fail-fast하게 전달하지 않습니다.

```bash
test "$(git diff --name-only "$BASE" HEAD -- engine contracts reader | wc -l)" = 0
```

명령 치환은 `test`의 인자일 뿐입니다. `git diff`가 nonzero여도 `wc -l`이 `0`을 출력하면 바깥 `test`가 성공하고 `set -e`가 발동하지 않습니다.

실측:

> `FINAL substitution_pipeline_failure_survived=yes`  
> `FINAL substitution_test_rc=0`

닫는 법: 파이프를 없애고 다음처럼 직접 상태를 검사하십시오.

```bash
git diff --quiet "$BASE" HEAD -- engine contracts reader
```

또는 먼저 별도 assignment로 받아 그 assignment의 실패를 `set -e`가 보게 해야 합니다. B-0에도 “diff 하위 명령 자체 실패” 역프로브를 추가해야 합니다.

### AE-3 · MED · 설계 §2.8 B-0 전체 블록 시험·§6

전체 블록은 Python을 다음 위치로 고정합니다.

```bash
"$MAIN/.venv/bin/python"
```

그런데 성공 시험의 `MAIN`은 “시험용 클론”입니다. `.venv/`는 Git에 들어 있지 않으므로 정상적인 `git clone` 또는 worktree에는 이 파일이 없습니다.

실측:

> `FINAL venv_tracked=no`

또한 생성기는 `HEAD` 앞 7자와 `--base-commit`을 비교하는데 B-0의 `BASE=<그 클론 HEAD>`가 전체 해시인지 7자리인지 정해지지 않았습니다. 전체 해시를 넘기면 그 비교는 실패합니다.

M3는 가상환경을 복사·심볼릭 링크할지, 원 리포 Python을 쓸지, 블록에 새 매개를 넣을지 임의 선택해야 합니다.

닫는 법:

```bash
PYTHON_BIN="${PYTHON_BIN:-$MAIN/.venv/bin/python}"
```

을 정본 블록에 추가하고, B-0은 `PYTHON_BIN=<정본 리포의 절대 .venv/bin/python>`을 명시하십시오. B-0의 `BASE`도 `git rev-parse --short=7 HEAD` 결과로 고정해야 합니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1·§2.2·§2.6·G1/G2 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·`select_failure_row`; 전수 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | §2.3·G2~G4·`_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | **partially** | 값은 맞지만 골든 검증·생성 수락면이 AE-1~AE-3 |
| T26 §3③ 양방향 관문·세 심기 | covered | G1~G6·변조 ⑴~⑷ |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | **partially** | 전수 값은 일치하지만 독립 골든 절차가 AE-1~AE-3 |
| T28 §3② β 표지 | **partially** | 술어·2,048칸은 맞으나 exception 검증 결속이 AE-1 |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2; 주입·레인 계수 실물 일치 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 12 id | **partially** | 명세는 정확하지만 exact-set 검사를 빼도 T‑V가 통과하는 AE-1 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ entry 표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미룬 것은 [T31 §3①](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:258)과 맞습니다. T32를 그 소라운드에 합치는 것도 [T32 §3⑤](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:304)가 허용합니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, R8/R9, 미지 id fail-closed, B-0 분리, 승인 상수는 공학 재량 또는 원장값의 기록입니다. AE-1~AE-3도 새 Owner 재정 없이 설계를 보수할 수 있습니다.

## B. 오늘의 표 불변

v12 11행 모형과 HEAD를 직접 8,190칸 대조한 결과 틀린 칸은 없습니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v12 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`입니다. §2.2 손검산은 정확합니다.

[`worst_status`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 여전히 미지 값을 0으로 취급합니다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

그러나 v12는 `select_failure_row()`가 모든 후보를 먼저 `terminal_action()`으로 검증하도록 했습니다. 따라서 R6대로 구현하면:

- `then` 없는 `retry(n)`
- `then: retry(n)`
- 비-retry 행의 `then`
- 미지 terminal action

모두 `worst_status` 전에 `StageError`가 되어 B-5의 런타임 fail-closed는 성립합니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β, 부분집합 우선, T-1/T-2가 실제 러너 전역을 사용 |
| B-2 | closed | 공식 영역 12 id·8,190칸, input-digest 별도 진입 반증 |
| B-3 | **partially** | `99fad78` 독립 생성 원리는 맞지만 검증·생성 수락면이 AE-1~AE-3 |
| B-4 | closed | `phases` 없이 판정점별 정확 등식 |
| B-5 | closed | 세 잘못된 `then` 형태를 관문·런타임 모두 거부 |
| B-6 | closed | kind 셋·upstream 호출자 0·`deferred/test_bound` |
| B-7 | closed | pytest와 7관문의 plain/`-O` 명령이 명시됨 |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | 패치 대상이 [`engine.stages.read.run_read_checks`](/home/laptop/projects/patent-docent/engine/stages/read.py:1743) |
| V-2 | closed | `-I`·repo 선삽입·모듈/패키지 provenance 6검사 |
| V-3 | closed | retry-1은 1회차·3 레인으로 구별 |
| V-4 | closed | phase 형식·우주·유령 phase 거부 |
| V-5 | closed | 판정점 `{early,exit}` 유일성과 출구 12-id 우주 |
| V-6 | closed | 실행 가능한 고정 predicate |
| V-7 | closed | T-11 ⑤ 종단 어휘 상등 |
| V-8 | closed | StageError 세 칸과 두 순서가 정확 |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전에 절대화 |
| N-2 | closed | 12개 phase 전건 실측·정본 통과 |
| N-3 | closed | B-0 병합 → 골든 → B 순서와 저작 좌석 고정 |
| N-4 | closed | `_exit_retry_eligible` 명명·직접 시험 |
| N-5 | closed | T-12 계약↔엔진 상수 다리 |
| N-6 | closed | `exit` 필수·`early` iff |
| N-7 | closed | 다섯 문언 모두 구체화 |

W·X·Y·Z·AA·AC는 다시 열리지 않았습니다. X-1은 AD-2 보수로 closed입니다. AB-1은 AE-1 때문에 여전히 partially입니다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”이라는 결론은 맞습니다.

- [`decompose_only_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- tail은 입력 `decompose` 객체를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 같은 `decomposes[canonical_run]`을 씁니다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 두 조립 모두 claims를 deepcopy하고 같은 `rewrite_claims`를 적용합니다([read.py:532](/home/laptop/projects/patent-docent/engine/stages/read.py:532)).
- [`SpecIndex.build`](/home/laptop/projects/patent-docent/reader/lib/spec_io.py:52)는 여러 최상위 값을 색인하지만, 수렴 6축은 claims에서 만든 independent/dependent/elements/additions만 읽습니다([convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)).
- 후속 조립으로 달라질 수 있는 `applicant_interest.material_id`는 여섯 축이 읽지 않습니다.

메모리 검증:

> `FINAL base_status=pass base_fail=[] injected_status=fail injected_fail=['independent-count'] other_nonpass=['addition-attachment:measured']`

따라서 출구 전용 실패 페이로드는 제시할 수 없습니다. T-1의 `read_stage.run_read_checks` 패치는 실제 러너의 유일한 출구 호출점에 닿으며, 원 검사기가 `independent-count` 실패를 만들므로 T28 §3③을 충족합니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest 영역 밖 값은 T29 승인 |
| ③ | 맞다 | 키 이름은 T29가 설계에 위임 |
| ④ | 맞다 | T-11 ⑤가 엔진·관문 어휘를 잇는다 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 공식 우주 밖 무효 입력이며 StageError는 fail-closed |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 진입 가드가 early·exit 목록을 실제로 읽고 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 검사기 자체의 `independent-count`를 fail로 만듦 |
| ⑪ | 맞다 | 표지 대상은 T28이 명한 술어 하나 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류가 허용됨 |
| ⑬ | 맞다 | 판정점·검사 id 우주 고정은 형식 규율 |
| ⑭ | 맞다 | `-I`와 6검사는 실제 import tree를 증명함. AE-2·AE-3은 바깥 셸/B-0 하네스 결함 |
| ⑮ | 맞다 | B-0을 골든 앞에 분리하는 순서 판단은 옳음. 하네스 실행 공백은 AE-3 |
| ⑯ | 맞다 | R9는 정본 선언을 바꾸지 않는 형식 대조 |
| ⑰ | 맞다 | 승인 3/8은 원장값이며 T-11 ⑥이 두 상수를 잇는다 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | AD-2 보수로 `judged_at`과 미지 기계 키까지 G1 골격에 포함 |
| ⑳ | 맞다 | 주입은 `independent-count`만 fail로 만들고 검사 id는 convergence 하나 |

자기 신고 중 새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 근거 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·`judged_at`·행별 허용 키 집합까지 고정 |
| G2 | covered | 선언↔행 차집합 양쪽 0·선언 중복 거부 |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1 |
| G4 | covered | phase 형식·우주·exit 필수·early iff |
| G5 | covered | input-digest entry·halt·points 부재·재시도 제외 |
| G6 | covered | R6 전항 |

열거 수는 16종이 아니라 **⑴~㉝ 33종**입니다. 원장과 과거 도전의 필수 심기는 포함됩니다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 미지 기계 키: ㉜
- `judged_at` 이동: ㉝

문언대로 G1~G6를 구현하면 그 관문들이 통과시키는 T26/T28/T29 범위 변조는 찾지 못했습니다. AE-1은 이 관문이 아니라 골든 검증기의 음성 시험 결속 결함입니다.

## G. M3 결정 공백

최소 두 곳입니다.

1. 정본 생성 블록의 `git diff | wc -l` 오류 전파 결함을 그대로 복사할지, `git diff --quiet`로 고쳐 정본 리터럴을 어길지(AE-2).
2. B-0 시험용 클론에 없는 `$MAIN/.venv/bin/python`을 어떻게 공급할지, 그리고 `BASE`를 전체 해시와 7자리 중 무엇으로 넘길지(AE-3).

AE-1은 선택 공백이라기보다 누락 구현을 수락할 수 있는 검증 공백입니다. 모두 Owner 재정이 아니라 v13에서 닫을 공학 오류입니다.

## 검증 경로

- HEAD·불변성:

  `git rev-parse --short=12 HEAD`

  > `7d01009742e5`

  도전 중 예고된 문서 전용 커밋이 들어왔습니다.

  `git diff --name-only 3ace14b HEAD -- engine contracts reader tests tools | wc -l`

  > `0`

  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`

  > `0`

  `git status --short | wc -l`

  > `0`

- `_failure_verdict` 전수 호출 + 독립 v12 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 국면·선언:

  > `FINAL exit_count=12 exit_unique=True entry=['read.input-digest'] point_ids=['early', 'exit'] early=['read.dependency-parse', 'read.claim-inventory', 'read.convergence'] all_exit=True phase_universe=['early', 'exit']`

- T-1 주입:

  > `FINAL base_status=pass base_fail=[] injected_status=fail injected_fail=['independent-count'] other_nonpass=['addition-attachment:measured']`

- T-2 레인 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- 셸 성공·생성기 실패·마커 실패:

  > `FINAL success_rc=0`  
  > `FINAL producer_failure_rc=7`  
  > `FINAL marker_failure_rc=1`

- 사전조건 명령 치환의 파이프 실패:

  `bash -c 'set -euo pipefail; test "$(false | wc -l)" = 0; echo FINAL substitution_pipeline_failure_survived=yes'`

  > `FINAL substitution_pipeline_failure_survived=yes`

- 시험용 클론의 인터프리터 전제:

  `git ls-files --error-unmatch .venv/bin/python`

  > `FINAL venv_tracked=no`

- 제안 신설물:

  > `FINAL proposed_files_absent_rc=0`

## [미검증]

- `generate.py`, `validate_manifest.py`, 두 신규 시험, manifest, `check_failure_table.py`가 아직 없어 실제 실행하지 못했습니다.
- detached worktree·시험용 클론·정본 생성 블록 전체는 파일을 만들므로 실행하지 않았습니다.
- 전체 pytest와 관문 plain/`-O`도 캐시·임시 산출 가능성 때문에 실행하지 않았습니다.
- T-1/T-2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았습니다. 주입과 레인 계획은 메모리에서 검증했습니다.
- AE-1의 변조는 검증기 부재 때문에 문언상 술어와 T‑V 수락 조건을 대상으로 반증했습니다.
- 리포에는 아무것도 쓰지 않았고 작업 트리는 끝까지 깨끗했습니다.