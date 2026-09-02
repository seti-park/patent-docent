# 독립 감수 원문 — 재정 T26 집행 설계 v9 의 M1b 설계 도전(8차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v9/final.txt` 의 sha256 `dafc3f4b2bb06285e06b27e05c5f8b6da60248047f0d1a046b642e4c11be3fdf` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 22분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 8차 심사** — v8(7차 FAIL · AA-1~AA-4) → **v9** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`1fdb2c7` · 7차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 2건(MED 2 · BLOCKER·HIGH 0) · 새 재정 사항 0 · AA-1~AA-3 closed · AA-4 partially(AB-2) · 그 밖 전건 closed.**
값 8,190 칸은 여덟 번째로 일치. **AB-1**: 검증기 「검사 항목 전부」가 값 필드를 다 덮지 않는다 — Z-2 처분이 고정하라 한 `exceptions.rule` 과 `meaning` ·
`$comment` · `cell_key` · `generator` · `generation_command` 는 존재만 검사 · 계수에 `type is int` 없음 · `provenance` 키 집합 미고정.
**AB-2**: `python -I` 는 스크립트 디렉터리를 `sys.path` 에서 빼므로 형제 `validate_manifest.py` 를 `import` 로 부를 수 없고(검증기는 `99fad78` 트리에도
없다) 설계가 적재 방식을 적지 않았다 → M3 임의 선택.

지적 열거 = AB-1, AB-2

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§14** 에 있다.
둘 다 **수용**(공학 · 규율 11 ③) — **v10** 에 반영하고 9차 도전에 냈다. v10 = 검증기가 manifest 의 **모든 값 필드**에 고정 리터럴 또는 형식을 붙인다
(최상위 10키 · `provenance` 8키 · `exceptions[0]` 6키 · `type is int`) · 생성기와 T-7 은 `importlib.util.spec_from_file_location` 으로
`Path(__file__).with_name("validate_manifest.py")` 를 적재(코드 명시) · B-0 시험이 공개 `python -I` 명령을 서브프로세스로 실행 · 음성 시험 ⓗⓘⓙ 추가.
9차 기동 직후 총괄이 §6 의 낡은 「ⓐ~ⓖ」를 발견해 레인을 죽이고 고쳐 재기동했다(그 과정에서 `pkill -f` 자기매칭으로 총괄 셸이 함께 죽는 함정 C 를
한 번 밟았다 — LANE-RUNTIME 「함정 C」 그대로).

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

8,190칸 값·계수·11행 격자·도달 불능 주장은 맞습니다. 그러나 v9의 새 manifest 검증기 명세가 T28의 `exceptions.rule`을 비롯한 여러 필드 값을 검사하지 않고, `python -I`에서 형제 검증기를 로드하는 배선도 빠졌습니다. 그대로 M3에 넘기면 구현 선택이 갈립니다.

## AA-1~AA-4 우선 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| AA-1 | closed | `check_ids`를 list·비공 str·`len == len(set) == 12`로 검사한 뒤 승인 집합과 양방향 대조한다. 13항 중복 변조도 지정됐다. |
| AA-2 | closed | `cells` 키 집합을 `{1..4095}:{0|1}`과 정확히 대조하고, exception 셀도 2,048개·중복 없음·정확한 집합으로 고정한다. |
| AA-3 | closed | T-7이 `base_commit == "99fad78"` 및 `tree_head == 99fad78c318875af99aa87083c029d2c6724e240`을 외부 인자로 고정한다. |
| AA-4 | partially | 공유 피검 함수 `validate_manifest()`와 세 호출자는 정해졌다. 하지만 필수 `-I` 실행에서 그 형제 파일을 불러오는 경로가 없다(AB-2). |

## 지적 목록

### AB-1 · MED · 설계 §2.8 `validate_manifest`·T-7 · [T28 §3②](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:118) · [Z-2 처분](/home/laptop/projects/patent-docent/docs/decisions/D-20260902-02-t26-design-challenge.md:238)

검증기의 “검사 항목 전부” 목록이 manifest의 모든 필드 값을 덮지 않습니다.

특히 Z-2 처분은 `exceptions[0].rule`을 고정하라고 명했지만, 상세 검증 목록은 다음만 검사합니다.

- 정확한 키 집합
- `id`
- `predicate`
- `cells`
- `cell_count`

`rule`과 `meaning`의 값은 보지 않습니다. 따라서 정상 manifest에서 이것만 바꾼 변조가 상세 검증 술어를 통과합니다.

```python
mutant["exceptions"][0]["rule"] = (
    "read.schema ∈ 실패 집합 → 재디스패치 0회"
)
mutant["exceptions"][0]["meaning"] = 17
```

β 셀 2,048개와 값 격자는 그대로이므로 T-7 런타임 대조도 이를 잡지 않습니다. 그런데 원장은 예외 표기 자체를 시험이 읽으라고 명합니다.

같은 누락은 최상위의 `$comment`, `cell_key`, `generator`, `generation_command`에도 있습니다. 존재만 강제되고 값·형식은 검사되지 않습니다. `expected_counts`와 `cell_count`도 `type(value) is int`가 없어 정수와 같은 float가 허용될 수 있으며, `provenance` 내부는 정확한 키 집합을 고정하지 않습니다.

닫는 법:

- `exceptions.rule`을 T28 문언과 정확히 대조하고 `meaning`도 고정 문자열 또는 최소 비공 문자열로 검사한다.
- `$comment`, `cell_key`, `generator`, `generation_command` 각각의 형식과 고정값을 명시한다.
- `expected_counts.*`와 `cell_count`는 `type(v) is int`로 검사한다.
- `provenance` 내부 키 집합도 정확히 고정한다.
- 위 필드 각각 또는 한 번의 동반 변조를 B-0·T-7 음성 시험에 추가한다.

이 때문에 Z-2는 여전히 `partially`입니다.

### AB-2 · MED · 설계 §2.8 생성기 ②·검증기 호출자 셋·§6 B-0

v9는 새 `validate_manifest.py`를 생성기와 T-7이 공유한다고 했지만, 필수 실행 방식은 다음과 충돌합니다.

- 생성기는 `<main>/tests/fixtures/read-failure-grid/generate.py`에 있다.
- 검증기도 그 형제 파일이다.
- `python -I`는 스크립트 디렉터리와 cwd를 `sys.path`에서 제거한다.
- 설계가 추가하는 경로는 detached `99fad78` 리포 루트뿐이다.
- `validate_manifest.py`는 `99fad78` 트리에 존재하지 않는다.
- `tests/fixtures/read-failure-grid`는 패키지가 아니며 디렉터리명에도 `-`가 있다.

실측:

> `FINAL isolated=1 safe_path=True sys_path=['/usr/lib/python314.zip', '/usr/lib/python3.14', '/usr/lib/python3.14/lib-dynload', '/home/laptop/projects/patent-docent/.venv/lib/python3.14/site-packages']`

따라서 평범한 `import validate_manifest`는 공개된 생성 명령에서 성립하지 않습니다. M3는 임의로 `sys.path`를 더 넣거나, `importlib`로 파일을 적재하거나, 검증 로직을 복제해야 합니다.

닫는 법:

- 예를 들어 `Path(__file__).with_name("validate_manifest.py")`를 `importlib.util.spec_from_file_location`으로 적재한다고 생성기·T-7 양쪽에 명시한다.
- 검증기는 엔진을 import하지 않는다는 조건을 유지한다.
- B-0 시험이 함수 직접 호출만 하지 말고, 문서에 적힌 정확한 `python -I generate.py ...` 명령을 서브프로세스로 실행해 `EXIT=0`을 확인한다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 |
| T26 §2⒜② 조치 격자·계약 순서 | covered | §2.2·§2.6; 전수 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | §2.3, G2~G4, `_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | partially | 값 모형은 맞지만 골든 검증·생성 경로가 AB-1·AB-2로 미완성 |
| T26 §3③ 양방향 관문·세 심기 | covered | G1~G6와 ⑴~㉛ |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | partially | 값은 전건 일치하지만 공개 생성 명령의 공유 검증기 배선이 비어 있음 |
| T28 §3② β 표지 | partially | predicate·셀 집합은 맞으나 `rule` 표기를 바꾼 manifest가 통과(AB-1) |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 12 id | covered | 길이·중복·집합·셀 우주 고정 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 키·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미룬 것과 T32를 그 소라운드에 합친 것은 각각 T31 §3①과 T32 §3⑤에 맞습니다. `screening_memos[].read_run` 무접촉 판단도 맞습니다.

`judged_at`, R8/R9, fail-closed, B-0, 승인 상수, 검증기 자체는 공학 재량입니다. AB-1·AB-2 역시 새 Owner 값 재정이 아니라 검증·배선 보수입니다.

## B. 오늘의 표 불변

HEAD `_failure_verdict`와 독립 11행 모형을 직접 전수 대조했습니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v9 모형↔HEAD 불일치 | 0 |

`StageError`는 `1024:1`, `2048:1`, `3072:1`입니다. §2.2 손검산에서 틀린 칸은 찾지 못했습니다.

R6도 논리상 맞습니다. 현재 [`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 값을 0으로 취급합니다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

하지만 v9는 `select_failure_row()`가 모든 후보의 `terminal_action()`을 먼저 검증하게 하므로 정상 신설 경로에서는 그 fail-open 동작에 도달하지 않습니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β·부분집합 우선·실제 모듈 패치·0/3 레인 대조가 선다 |
| B-2 | closed | 공식 12 id, 8,190키, input-digest 진입 예외가 분리됐다 |
| B-3 | partially | 값은 `99fad78` 구현에서 독립 생성하지만 manifest 생성·기록 수락면이 AB-1·AB-2로 미완성 |
| B-4 | closed | 8·9행 분리, `phases` 없는 정확 등식 |
| B-5 | closed | `then` 없는 retry·retry인 then·비-retry의 then을 관문과 런타임이 거부 |
| B-6 | closed | kind 3종, upstream 호출자 0, deferred/test_bound |
| B-7 | closed | pytest와 관문 전종 두 모드 |

### V-1~V-8

| 지적 | 판정 |
|---|---|
| V-1 | closed |
| V-2 | closed — engine/reader 출처는 `-I`·경로 삽입·6검사로 결속됨. AB-2는 새 형제 검증기 로딩 문제 |
| V-3 | closed |
| V-4 | closed |
| V-5 | closed |
| V-6 | closed |
| V-7 | closed |
| V-8 | closed |

### N-1~N-7

| 지적 | 판정 |
|---|---|
| N-1 | closed |
| N-2 | closed — R9 위반 0 재실측 |
| N-3 | closed — B-0→골든→B 소유·순서 자체는 명확 |
| N-4 | closed |
| N-5 | closed |
| N-6 | closed |
| N-7 | closed |

W-1~W-4, X-1~X-3, Y-1~Y-5는 v9에서 다시 열리지 않았습니다. Z-1은 `closed`, Z-2는 `partially`입니다. Z-2가 요구한 `rule` 고정이 상세 검증 목록에서 다시 빠졌습니다(AB-1).

## D. 출구 convergence 도달 가능성

“조기 통과 뒤 레인 페이로드만으로 출구 convergence를 실패시키는 것은 도달 불능”은 맞습니다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 [`assemble_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 그대로 호출합니다.
- tail은 입력 `decompose`를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 같은 `decomposes[canonical_run]`을 사용합니다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 양쪽 모두 claims를 deepcopy하고 동일한 `rewrite_claims`를 적용합니다([read.py:532](/home/laptop/projects/patent-docent/engine/stages/read.py:532)).
- 6축은 [`SpecIndex`](/home/laptop/projects/patent-docent/reader/lib/spec_io.py:36)의 claims 구조만 사용합니다.
- `peer_spec`의 실제 읽기는 [`convergence.py:94`](/home/laptop/projects/patent-docent/reader/lib/convergence.py:94)와 [:105](/home/laptop/projects/patent-docent/reader/lib/convergence.py:105)뿐입니다.

직접 조립·주입 결과:

> `FINAL convergence_status=pass failed_axes=[] claims_equal=False injected_status=fail changed_axes=['independent-count'] peer_reads=[('reader/lib/convergence.py', 94), ('reader/lib/convergence.py', 105)]`

따라서 T-1의 peer 독립항 복제는 검사기 자신이 `independent-count`를 fail로 만들고, 다른 검사에는 영향을 주지 않습니다. [`read_stage.run_read_checks`](/home/laptop/projects/patent-docent/engine/stages/read.py:1743) 패치는 실제 러너 호출점에 닿습니다.

부분집합 검사를 서명보다 먼저 두면 convergence가 든 집합은 첫 회차에 탈출합니다.

> `FINAL repeated_and_convergence_reachable=False`

T28 §3③의 실제 러너 시험 형태로 적절합니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | T29 승인 값 |
| ③ | 맞다 | 키 이름은 T29가 설계에 위임 |
| ④ | 맞다 | T-11⑤가 terminal 두 벌을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 공식 12-id 밖의 무효 입력이며 fail-closed는 값 공간 변경이 아님 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③의 명시값 |
| ⑨ | 맞다 | early·exit 목록을 가드가 실제 읽고 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 실제 exact-match 축을 실패시킴 |
| ⑪ | 맞다 | 표지 대상 자체는 T28 술어 하나가 맞음. 다만 표기 문언의 강제는 AB-1로 틀림 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류는 허용됨 |
| ⑬ | 맞다 | 판정점·검사 id 우주 고정은 계약 형식 규율 |
| ⑭ | 맞다 | 실행된 뒤의 engine/reader 출처 증명에는 6검사와 `-I`가 충분. AB-2는 실행 전 검증기 로딩 문제 |
| ⑮ | 맞다 | B-0 분리는 골든을 B 앞에 세운다 |
| ⑯ | 맞다 | R9는 현재 정본 실물과 일치 |
| ⑰ | 맞다 | 승인 3/8은 원장값이며 T-11⑥이 두 상수를 맞춤 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격은 원장값의 독립 오라클 |
| ⑳ | 맞다 | 주입 결과 `independent-count`만 fail |

새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 근거 |
|---|---|---|
| G1 | covered | 11행·행 분할·순서·action·then·label·points 고정 |
| G2 | covered | 선언↔행 차집합 양쪽 0, 선언 배열 중복 거부 |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1 고정 |
| G4 | covered | phase 형식·우주·exit 필수·early iff |
| G5 | covered | input-digest 표지·halt·points 부재·재시도 제외 |
| G6 | covered | 세 잘못된 `then` 형태 거부 |

⑴~㉛은 원장의 필수 심기와 1차 반례를 모두 포함합니다.

- 행 없는 검사: ⑴
- 검사 없는 행과 `read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶⑷
- 거짓 `points: [early]`: ⑽
- 동시 일관 변조: ㉑
- 선언 중복: ㉒㉓
- 행 병합·순서: ㉕㉖
- upstream action: ㉗
- 예산 값·타입: ㉙~㉛

G1~G6가 통과시키는 T26/T28/T29/T30 계약축 변조는 찾지 못했습니다. AB-1은 이 관문이 아니라 별도 manifest 수락면을 통과하는 변조입니다.

## G. M3 결정 공백

두 곳이 남습니다.

1. 앞 절의 “`rule` 고정”과 §2.8의 “검사 항목 전부” 상세 목록 중 무엇을 따를지. 상세 목록대로면 T28 표기 변조를 통과시키고, 앞 문장까지 구현하면 설계에 없는 추가 검사들을 어디까지 확장할지 골라야 합니다.
2. `python -I` 아래에서 main 트리의 형제 `validate_manifest.py`를 어떻게 공유할지. `importlib` 적재, 별도 `sys.path`, 모듈 위치 변경 중 하나를 M3가 임의 선택해야 합니다.

하나라도 있으면 FAIL이라는 기준에 따라 발주 불가입니다.

## 검증 경로

- 최종 상태:

  `git rev-parse --short=7 HEAD` → `1fdb2c7`  
  `git status --short` → 빈 출력  
  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`

  > `0`

  시작 HEAD는 `c6c3202`였고, 검토 중 예고된 문서 전용 `1fdb2c7`이 들어왔습니다. 대상 코드·계약 diff는 0입니다.

- 기준 커밋:

  `git rev-parse 99fad78`

  > `99fad78c318875af99aa87083c029d2c6724e240`

- HEAD `_failure_verdict` 전수 호출 + 독립 11행 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 halt_null=6144 escalate_null=1023 escalate_repeat=1020 stage_error=3`

- 국면·선언 실측:

  > `FINAL point_ids=['early', 'exit'] point_unique=True exit_count=12 exit_unique=True entry_ids=['read.input-digest'] code_counts=(10,2) code_unique=(True,True) r9_violations=[]`

- 조기/출구 조립과 T-1 주입:

  > `FINAL convergence_status=pass failed_axes=[] claims_equal=False injected_status=fail changed_axes=['independent-count'] peer_reads=[('reader/lib/convergence.py', 94), ('reader/lib/convergence.py', 105)]`

- 후속 레인 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-dependent', 'ground-independent', 'synthesize'] all_retry1=True`

- 예산 타입:

  > `FINAL max_retries={'True': ('bool', 'RunnerContractError'), '1.0': ('float', 'RunnerContractError'), "'1'": ('str', 'RunnerContractError'), '0': ('int', 0), '-1': ('int', -1), '1': ('int', 1)}`

- `-I` 경로:

  > `FINAL isolated=1 safe_path=True sys_path=['/usr/lib/python314.zip', '/usr/lib/python3.14', '/usr/lib/python3.14/lib-dynload', '/home/laptop/projects/patent-docent/.venv/lib/python3.14/site-packages']`

- v9 상세 검증 목록의 미검사 값 필드 대조:

  > `FINAL unchecked_value_fields=['$comment', 'cell_key', 'exceptions.meaning', 'exceptions.rule', 'generation_command', 'generator']`

- 신설물 부재:

  > `tests/test_m24_failure_grid_golden.py=absent`

## [미검증]

- `generate.py`, `validate_manifest.py`, manifest, T-7, `check_failure_table.py`는 아직 없어 실제 실행하지 못했습니다.
- 따라서 AB-1의 통과 변조는 구현 실행 결과가 아니라 v9에 적힌 검증 술어를 그대로 모델링한 결과입니다.
- 공개 생성 명령의 detached worktree 통주는 쓰기 금지 때문에 실행하지 않았습니다.
- 전체 pytest와 관문 plain/`-O`도 캐시·임시 파일을 만들 수 있어 실행하지 않았습니다.
- T-1/T-2의 완성된 신설 시험은 없으므로 실제 파일 기반 통주는 못 했고, 호출 좌표·조립 결과·주입된 검사 행·레인 계획을 메모리에서 각각 검증했습니다.