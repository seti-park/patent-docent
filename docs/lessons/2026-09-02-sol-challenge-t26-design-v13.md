# 독립 감수 원문 — 재정 T26 집행 설계 v13 의 M1b 설계 도전(12차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v13/final.txt` 의 sha256 `9e6fb1f111cf7855d0109d5ac50fbf6604a8540e17e579fdd98d6b72d85a41b7` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 19분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 12차 심사** — v12(11차 FAIL · AE-1~AE-3) → **v13** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`7b35e78` · `22429e4` — 11차 원문 반입과 그 표 안 파이프 문자 정정)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다.

**판정 = FAIL · 지적 3건(HIGH 1 · MED 2 · BLOCKER 0) · 새 재정 사항 0 · AE-2·AE-3 closed · AE-1 partially · 그 밖 전건 closed.** 값 8,190 칸은
열두 번째로 일치. **AF-1**: 표 T-V 가 아직 「제약 하나만 깨고 그 제약만 보고되는」 결속이 아니다 — 복합 변조(predicate+cells 동반) · 누락 제약
(`reader_path.type` · 비공 문자열) · 한 키만 보는 전칭(`expected_counts` 한 키) · 기대가 「ID 포함」이라 β 집합 검사를 빼고 진단만 덧붙이는 구현이 통과.
**AF-2**: B-0 수락 시점에 세 산출물은 worktree 미커밋 — 시험용 clone 에는 생성기·검증기가 없어 블록 전체 시험이 파일 부재로 실패(`b0_artifacts_tracked_at_head=0`).
**AF-3**: G1~G6 이 조기 선언 `early_phase_spec.judged_here`(read.yaml:311)를 읽지 않아 `judged_here += [read.__ghost__]` 가 관문 전종 통과 — T26 ⒜ ③
「선언된 모든 검사」 우주에서 조기 선언 누락(존치 시험 :853 은 잡으나 관문 주장이 더 넓다 — Y-3 계열).

지적 열거 = AF-1, AF-2, AF-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§18** 에 있다.
셋 전부 **수용**(공학 · 규율 11 ③) — **v14** 에 반영하고 13차 도전에 냈다. v14 = 검증기를 **필드별 층위 평가**(구조 → 원소 → 고유 → 값 · 앞 층 위반이면
뒤 층 미평가)로 규정해 한 변조 = 정확히 한 ID · 기대 = `set(위반 ID) == {target}` · 표 T-V 재작성(복합 변조 제거 · 누락 ID 추가 · `expected_counts` 키별
매개 · tree_head nibble 반전 · 고립 불가 제약 둘은 함의하는 제약에 흡수) · 시험용 clone 조립 절차 고정(두 파일 복사 + clone 안 임시 커밋) · G2 우주에
`judged_here` + 세 벌 상등 + 변조 ㉞. 13차 기동 직후 §2.8 호출자 절의 낡은 「그 ID 로 시작하는 문장」 문구를 발견해 레인을 PID 로 죽이고 고쳐 재기동했다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

v13은 AE-2와 AE-3을 닫았지만 AE-1은 여전히 부분 폐쇄입니다. 추가로 양방향 관문이 조기 선언을 빠뜨린 결함과, B-0의 미커밋 산출물이 시험용 clone에 존재하지 않는 실행 공백을 찾았습니다.

## AE-1~AE-3 우선 판정

| 지적 | 판정 | 이유 |
|---|---|---|
| AE-1 | **partially** | `CONSTRAINT_IDS`와 제약별 ID는 도입됐지만 T‑V에 복합 변조·누락 제약·한 키만 보는 전칭 검사가 남았다. AF-1 |
| AE-2 | **closed** | `git diff --quiet`가 직접 실행되어 없는 ref가 rc 128로 전체 블록을 중단한다. |
| AE-3 | **closed** | `PYTHON_BIN` 주입과 7자리 `BASE`가 명시됐다. 단, clone에 B-0 신설물이 없다는 별도 공백은 AF-2다. |

## 지적 목록

### AF-1 · HIGH · 설계 §2.8 검증기·표 T‑V·T-7 ③

T‑V가 아직 “제약 하나만 깨고 그 제약만 보고되는” 결속을 만들지 못합니다.

가장 직접적인 통과 구현은 다음과 같습니다.

- `exception.cells.set` 변조는 `predicate`와 `cells`를 함께 바꿉니다.
- 검증기에서 실제 β 셀 집합 검사를 삭제하고, `predicate` 불일치 때 `exception.predicate.eq`와 `exception.cells.set` 두 진단을 함께 내게 해도 됩니다.
- T‑V는 목표 ID가 “있다”만 보므로 `exception.predicate.eq` 행과 `exception.cells.set` 행이 모두 통과합니다.
- 이후 predicate는 정상 문자열로 두고 β cells만 다른 2,048칸 집합으로 바꾸면 검증기가 이를 통과시킵니다. T28 §3②가 공허해집니다.

그 밖에도:

- `provenance.reader_path.type` ID가 없습니다. 문자열 `"/"`는 `len == 1`이고 순회 원소 `"/"`도 절대경로라, 타입 검사를 생략한 구현이 `.len1`·`.absolute`를 통과시킬 수 있습니다.
- `expected_counts.value.type`은 `"escalate/null"` 하나만 float로 바꿉니다. `halt/null` 등 다른 키만 타입 검사에서 빠뜨려도 전건이 통과합니다.
- `check_ids`와 exception cells의 “비공 문자열”은 별도 제약 ID가 없습니다.
- `cells.value.shape`의 `["halt"] / 정수`는 컨테이너 타입과 길이라는 두 제약 및 두 변조를 한 칸에 묶었습니다.
- `provenance.tree_head.eq = 현재 HEAD`는 B-0 정상 표본이 현재 clone HEAD에서 생성되면 무변조가 될 수 있습니다.

닫는 법:

1. 모든 변조는 다른 필드를 그대로 둔 채 한 제약만 깨야 합니다. 특히 β cells 변조에서는 predicate를 고정하십시오.
2. 기대를 “목표 ID 포함”이 아니라 `reported_constraint_ids == {target_id}`로 고정하십시오.
3. `reader_path.type`, 비공 문자열, value 컨테이너/길이처럼 독립 제약마다 ID를 분리하십시오.
4. 전칭 조건은 모든 `expected_counts` 키 등을 매개변수화해 각각 변조하십시오.
5. tree SHA는 `required_tree_head`의 한 nibble을 결정론적으로 뒤집어 반드시 다른 40자리 SHA를 만드십시오.
6. `CONSTRAINT_IDS` 자체도 tuple·문자열·중복 없음·표와 길이까지 대조하십시오.

### AF-2 · MED · 설계 §2.8 B-0 승격 순서·생성 블록·§6

B-0 수락 시점에는 세 산출물이 `round-b0` worktree에 **미커밋** 상태입니다. 그런데 전체 블록 시험의 `MAIN`은 “시험용 clone”이고 블록은 다음 파일을 clone 안에서 실행합니다.

```bash
"$MAIN/tests/fixtures/read-failure-grid/generate.py"
```

일반적인 `git clone`은 원 worktree의 미커밋 파일을 복사하지 않습니다. 현 HEAD에도 B-0 세 파일은 추적되어 있지 않습니다. 따라서 clone을 만드는 방법만 구현하면 정상 시험은 생성기 부재로 실패합니다. M3는 파일을 복사할지, 임시 commit을 만들지, 현재 worktree를 `MAIN`으로 쓸지 임의 선택해야 합니다.

닫는 법: B-0 시험용 clone 조립 절차를 고정하십시오. 예를 들면 `--no-hardlinks` clone을 만든 뒤 현재 B-0 worktree의 `generate.py`·`validate_manifest.py`를 정확한 경로에 복사하고 실재를 검사한 다음 블록을 실행하도록 명시하면 됩니다. 변조는 그 clone 안에서만 수행해야 합니다.

### AF-3 · MED · 설계 §2.1 R2·§2.7 G2/G4·`read.yaml:286-314`

T26은 “계약에 선언된 모든 검사(진입·조기·출구)”와 failure checks 합집합의 양방향 차집합 0을 관문에 요구합니다. 그러나 G1~G6는 별도 조기 선언인 [`early_phase_spec.judged_here`](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:311)를 읽지 않습니다.

다음 변조는 G1~G6의 명시 입력을 전혀 바꾸지 않습니다.

```yaml
early_phase_spec:
  judged_here:
    - read.claim-inventory
    - read.dependency-parse
    - read.convergence
    - read.__ghost__
```

failure 행에는 `read.__ghost__`가 없으므로 전체 선언 기준 차집합은 `{read.__ghost__}`지만 관문은 통과합니다. 존치 pytest인 [`test_claim_check_phase_meanings_and_exit_rows_are_declared`](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:853)가 이를 잡는다고 해도, T26 §3③이 요구한 **관문** 구현 누락은 치유되지 않습니다. Y-3과 같은 “다른 시험은 잡지만 관문 주장이 더 넓은” 결함입니다.

닫는 법: G2 또는 G4에 다음을 추가하고 self-test에 위 변조를 넣으십시오.

```text
set(early_phase_spec.judged_here)
  == set(retry_budget.points[id=early].checks)
  == {id | early ∈ checks_before_exit[id].phases}
```

`judged_here` 자체도 list·비공 문자열·중복 없음으로 검사하고, R2 선언 우주에 포함해야 합니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1·§2.2·§2.6·G1 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·`select_failure_row`; 전수 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | **partially** | exit/entry와 retry 등식은 맞지만 조기 선언이 G2에서 빠짐(AF-3) |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | **partially** | 값 모형은 전건 일치. 골든 수락면과 B-0 실행이 AF-1·AF-2 |
| T26 §3③ 양방향 관문·세 심기 | **partially** | 기존 세 심기는 있으나 조기 전용 행 없는 검사 변조가 통과(AF-3) |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | **partially** | 전수 모형은 일치하나 골든 확정 절차가 AF-1·AF-2 |
| T28 §3② β 표지 | **partially** | 술어·2,048칸은 맞지만 β 집합 검사를 제거한 검증기가 T‑V를 통과(AF-1) |
| T28 §3③ 실제 러너 음성·양성 | covered | T-1/T-2; 주입 대상·3 레인 계수 일치 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 12 id | **partially** | exact-set 설계는 맞지만 B-0 골든 절차가 AF-2 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ entry 표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9; 실측 0 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미룬 판단과 T32를 그 소라운드에 합치는 판단은 원장과 맞습니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, 미지 id fail-closed, 승인 상수, provenance 거부, B-0 분리는 공학 재량 또는 원장값 기록입니다. AF-1~AF-3은 새 Owner 재정 없이 고칠 수 있습니다.

## B. 오늘의 표 불변

8,190칸 전수 결과는 v13과 정확히 같습니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v13 ↔ HEAD 불일치 | 0 |

§2.2 손검산에서 새로 틀린 칸은 없습니다. `StageError` 세 칸은 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`입니다.

[`worst_status`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)는 미지 값을 0으로 취급하지만, v13의 `select_failure_row`가 모든 후보를 `terminal_action()`으로 먼저 검증합니다. 따라서 다음 네 형태는 `worst_status`에 도달하기 전에 `StageError`여야 합니다.

- `then` 없는 `retry(n)`
- `then: retry(n)`
- 비-retry 행의 `then`
- 미지 terminal action

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β 루프 순서와 T-1/T-2가 정확함 |
| B-2 | closed | 출구 12 id·8,190칸, input-digest 별도 진입 |
| B-3 | **partially** | 기준 트리 생성 원리는 맞지만 골든 수락·B-0 경로가 AF-1·AF-2 |
| B-4 | closed | `phases` 교집합 없이 판정점별 정확 등식 |
| B-5 | closed | 잘못된 `then` 세 형태와 미지 action을 관문·런타임 모두 거부 |
| B-6 | closed | kind 3종·upstream 호출자 0·이연 결속 |
| B-7 | closed | pytest와 7관문의 plain/`-O` 명령 명시 |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks` 전역을 패치 |
| V-2 | closed | `-I`·명시 repo·provenance 6검사 |
| V-3 | closed | retry-1 정확히 3 레인 |
| V-4 | closed | phase 형식·우주·유령 phase 거부 |
| V-5 | closed | 판정점 유일성·출구 12-id 우주 |
| V-6 | closed | 실행 가능한 고정 predicate |
| V-7 | closed | T-11 ⑤ 종단 어휘 상등 |
| V-8 | closed | StageError 세 칸과 두 순서가 정확 |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전에 절대화 |
| N-2 | closed | 12개 phase 전건 실측 |
| N-3 | **partially** | B-0→골든→B 순서는 섰지만 미커밋 B-0 파일을 clone에 공급하는 단계가 없음(AF-2) |
| N-4 | closed | `_exit_retry_eligible` 함수 단위 시험 |
| N-5 | closed | T-12 계약↔엔진 상수 다리 |
| N-6 | closed | `early` iff와 거짓 양성 차단. AF-3은 별도 조기 선언 누락 |
| N-7 | closed | 다섯 문언 전부 구체화 |

W~AD는 다시 열리지 않았습니다. 다만 AD-1은 AE-1/AF-1 계열로 계속 `partially`이고, AD-3은 AE-2·AE-3 범위에서는 닫혔습니다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 출구 convergence 실패는 레인 페이로드만으로 도달 불능”은 맞습니다.

- [`decompose_only_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- tail은 입력 `decompose` 객체를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구가 같은 `decomposes[canonical_run]`을 씁니다.
- 두 조립 모두 claims를 deepcopy하고 같은 `rewrite_claims`를 적용합니다([read.py:532](/home/laptop/projects/patent-docent/engine/stages/read.py:532)).
- 수렴 여섯 축은 [`SpecIndex`](/home/laptop/projects/patent-docent/reader/lib/spec_io.py:52)가 claims에서 만든 independent/dependent/elements/additions만 읽습니다([convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)).
- 실제 조기·최종 claims 객체는 `applicant_interest.material_id` 때문에 바이트 동일하지 않을 수 있지만, 실측 수렴 결과는 pass이고 여섯 축이 그 차이를 읽지 않습니다.

따라서 출구 전용 실패 페이로드는 제시할 수 없습니다.

T-1은 올바른 대체 형태입니다. [`run_read_checks`의 엔진 호출점](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)은 하나이고, 그 모듈 전역을 패치한 wrapper가 peer 독립항을 복제하면 검사기 자신이 `independent-count`만 fail로 냅니다. 이후 러너의 출구 판정·무재시도·escalate 경로는 실제 경로입니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest 영역 밖 값은 T29 승인 |
| ③ | 맞다 | `judged_at` 이름은 T29가 설계에 위임 |
| ④ | 맞다 | T-11 ⑤가 두 종단 어휘를 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 공식 영역 밖 무효 입력이고 StageError는 fail-closed |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 성공 진입에서 early·exit 목록을 실제로 읽고 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 `independent-count`만 fail로 만듦 |
| ⑪ | 맞다 | 표지 대상은 T28이 정한 술어 하나 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류 허용 |
| ⑬ | 맞다 | 판정점·검사 id 우주 고정은 형식 규율 |
| ⑭ | 맞다 | `-I`와 provenance 6검사는 기준 트리 import를 검증 |
| ⑮ | 맞다 | B-0 분리 판단 자체는 옳음. clone 구성은 AF-2 |
| ⑯ | 맞다 | R9는 현재 정본 선언을 바꾸지 않음 |
| ⑰ | 맞다 | 승인 3/8은 원장값이며 T-11 ⑥이 상수를 연결 |
| ⑱ | 맞다 | 선언 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 실패표 상수는 원장값 기록 |
| ⑳ | 맞다 | 주입은 convergence 한 검사·independent-count 한 축 실패 |

새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 이유 |
|---|---|---|
| G1 | covered | 11행·순서·기계 필드·행별 허용 키 고정 |
| G2 | **partially** | entry/exit 선언은 보지만 `early_phase_spec.judged_here`를 선언 우주에서 누락(AF-3) |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1 |
| G4 | covered | 명시된 R9 범위에서는 phase 형식·우주·early iff를 집행 |
| G5 | covered | input-digest entry·halt·points 부재 |
| G6 | covered | R6 전항 |

v13 열거는 16종이 아니라 **⑴~㉝ 33종**입니다. 원장의 필수 심기와 과거 요구는 포함합니다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶·⑷·㉑
- 출구 전용 행의 거짓 `points: [early]`: ⑽

그러나 `early_phase_spec.judged_here += [read.__ghost__]`는 G1~G6을 통과합니다. 이것이 AF-3의 관문 반례입니다.

## G. M3 결정 공백

최소 두 곳입니다.

1. T‑V의 누락·복합 제약을 한 ID로 묶을지 새 ID를 추가할지, 복합 변조에서 어떤 진단들을 내야 하는지(AF-1).
2. B-0 수락 전에 시험용 clone에 아직 커밋되지 않은 생성기·검증기를 어떻게 공급할지(AF-2).

AF-3은 임의 선택보다 직접적인 집행 누락입니다. 따라서 v13을 그대로 M3에 넘길 수 없습니다.

## 검증 경로

- 최종 HEAD·불변성:

  ```bash
  git rev-parse --short=12 HEAD
  git status --short | wc -l
  git diff --name-only 7d01009 HEAD -- engine contracts reader tests tools | wc -l
  git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l
  ```

  > `22429e4fb537`  
  > `FINAL status_rows=0`  
  > `FINAL protected_diff_rows=0`  
  > `FINAL golden_core_diff_rows=0`

- `_failure_verdict` 전수 호출 + 독립 v13 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 국면·선언:

  > `FINAL exit_count=12 exit_unique=True entry=['read.input-digest'] point_ids=['early', 'exit'] early=['read.claim-inventory', 'read.dependency-parse', 'read.convergence'] all_exit=True early_iff=True phase_universe=['early', 'exit']`

- T-1 주입:

  > `FINAL base_status=pass injected_status=fail failed_axes=['independent-count'] other_nonpass=['addition-attachment:measured']`

- 조기 조립본↔최종 조립본:

  > `FINAL early_full_status=pass nonpass=['addition-attachment:measured'] claims_equal=False`

- T-2 레인 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- 셸 역프로브:

  > `FINAL invalid_base_rc=128`  
  > `FINAL producer_failure_rc=7`  
  > `FINAL python_bin_executable=yes`

- `worst_status`:

  > `FINAL known=halt unknown_only=ok mixed=escalate`

- T‑V 누락 타입 반례:

  > `FINAL reader_path_mutant='/' len1=True iter_item='/' item_absolute=True`  
  > `FINAL untested_count_float_equal=True tested_key_unchanged_type=int`

- 조기 선언 관문 반례:

  > `FINAL early_ghost_rowless=['read.__ghost__'] g1_g6_named_inputs_unchanged=True`

- B-0 파일 가용성:

  > `FINAL b0_artifacts_tracked_at_head=0`

## [미검증]

- `generate.py`, `validate_manifest.py`, 두 신규 시험, manifest, `check_failure_table.py`는 아직 없어 실행하지 못했습니다.
- B-0 전체 블록·clone·detached worktree는 파일을 만들므로 read-only 규율상 실행하지 않았습니다.
- 전체 pytest와 관문 plain/`-O`는 캐시·임시 산출 가능성 때문에 실행하지 않았습니다.
- T-1/T-2 완성 실러너 통주는 런 디렉터리를 쓰므로 실행하지 않았습니다. 검사 주입과 레인 계획은 메모리에서 검증했습니다.
- 리포에는 아무것도 쓰지 않았고 최종 작업 트리는 깨끗합니다.