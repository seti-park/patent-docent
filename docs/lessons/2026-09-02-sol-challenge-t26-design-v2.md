# 독립 감수 원문 — 재정 T26 집행 설계 v2 의 M1b 설계 도전(재도전) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v2/final.txt` 의 sha256 `a8b8ec7b6e5f547da26a37b353e08e88d12ecc9fc91a1c7fd4ebbfd99ed9e835` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 ·
배경 실행 + `EXIT=` 마커 · 약 17분 · resume 없이 1차 완주 · 정본 트리 지문 `0cf666a351c95e5685bf4eb09a4e47c96c2caaff`
감수 전후 불변 · `git status` 0행). **ROUTING M1b 설계 도전의 2차 심사** — 1차 도전(`2026-09-02-sol-challenge-t26-design.md` · FAIL B-1~B-7)이
연 재정 T28 β · T29 ⓐ · T30 ⓐ(`ruling-20260902-02-T28-T32.md`)를 반영한 설계 **v2** 에 대한 것이다. 발주문은 ROUTING M1b 강제 문구
(*계획서의 주장 중 자료로 검증 가능한 것은 직접 검증하고 검증 경로를 명시*)를 실었고 도전자는 8,190 칸 전수 재계산 · monkeypatch
도달 여부 · 레인 로그 행 수 · G4 술어를 **실행으로** 반증했다.

**대상** = 총괄 저작 설계 메모 `T26-DESIGN-v2.md`(세션 스크래치 · 40,632 B — 리포에 없다. 이 판정을 받아 **v3** 으로 개정되었고,
PASS 를 받는 판이 라운드 B 발주문의 첨부로 리포에 들어온다) · 기준 커밋 **`663c77e`** · 골든 기준 트리 `99fad78`.

**판정 = FAIL · 지적 8건(BLOCKER 2 · HIGH 4 · MED 2) · 새 재정 사항 0.** 값은 맞았다 — 도전자가 독립 모델로 HEAD 와 8,190 칸을
대조해 `MISMATCHES 0`, 네 계수(6,144 · 1,023 · 1,020 · 3)와 β 표지 2,048 칸을 재현했고, 총괄의 「출구 convergence 실패는 페이로드로
도달 불능」 주장을 코드 좌표 여섯으로 확인했다. 틀린 것은 **집행 정밀도**다 — T-1 의 monkeypatch 대상이 시험 모듈 `m2` 여서 러너에
닿지 않는다(V-1) · 골든 생성기가 `99fad78` 모듈을 import 한다는 보장이 없다(V-2) · 후속 1회 재시도는 레인 로그 1행이 아니라 3행(V-3) ·
G4 가 유령 phase 를 통과시킨다(V-4) · 판정점 id 중복과 미지 id 우주가 미정(V-5) · manifest predicate 가 실행 불능 표현(V-6) · T-11 이
종단 어휘 두 벌의 상등을 안 본다(V-7) · §2.2 손검산이 lane-log-only 3칸을 누락하고 「격자 순」 서술이 틀렸다(V-8).

지적 열거 = V-1, V-2, V-3, V-4, V-5, V-6, V-7, V-8

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§7** 에 있다.
여덟 건 전부 **수용**(공학 수정 · 규율 11 ③ 재량) — v3 에 반영되었고, ROUTING §5 ⑽ ⓑ(같은 상신 2회 저항)에 따라 v3 은
자문(fable xhigh)을 거친 뒤 3차 도전에 나간다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

11행 격자의 핵심 값은 맞고, HEAD와 제안 알고리즘은 8,190칸 전부 일치했습니다. 그러나 T28 필수 러너 시험이 잘못된 대상을 패치하고, 양성 대조군의 레인 로그 계수가 틀렸으며, 골든 생성이 `99fad78` 코드에서 실행된다는 보장이 없습니다. 관문이 통과시키는 변조와 M3 결정 공백도 남아 있습니다.

## 지적 목록

### V-1 · BLOCKER · 설계 §2.9 T-1 · [test_m21:37](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:37) · [test_m2_read.py:65](/home/laptop/projects/patent-docent/tests/test_m2_read.py:65) · [read.py:1743](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)

`monkeypatch.setattr(m2, "run_read_checks", wrapper)`는 러너를 패치하지 않습니다. 이 시험 파일에서 `m2`는 `test_m2_read` 모듈이고, 러너는 `engine.stages.read`가 import한 별도 전역 `run_read_checks`를 호출합니다.

실측:

> `PATCH_REACHES_RUNNER False M2_PATCHED True`

따라서 T-1은 convergence 실패를 주입하지 못하고 T28 §3③을 증명하지 못합니다.

닫는 법: `engine.stages.read` 모듈을 `read_stage`로 import하고, 원본을 보존한 뒤 `monkeypatch.setattr(read_stage, "run_read_checks", wrapper)`로 패치한다고 설계에 명시해야 합니다.

### V-2 · BLOCKER · 설계 §2.8 생성 명령 · D-02 B-3 · T28~T32 §5⑤

제시된 명령은 생성기가 `99fad78` 트리의 모듈을 import한다는 것을 보장하지 않습니다.

```text
cd <tmp> &&
<main>/.venv/bin/python <main>/tests/fixtures/read-failure-grid/generate.py ...
```

파이썬은 스크립트 디렉터리를 import 시작점으로 삼으며, 단순히 `cd <tmp>` 했다고 `<tmp>`의 `engine`이 선택되지는 않습니다. 생성기가 `__file__` 기준으로 리포 루트를 넣으면 오히려 `<main>`의 구현을 읽습니다. 현재 설계에는 import된 `engine.stages.read.__file__`가 `<tmp>` 아래인지 확인하는 조건도 없습니다.

이는 원장 문언 “생성 절차가 `99fad78` 트리에서 돈다”와 B-3 독립성을 보장하지 못합니다.

닫는 법:

- detached worktree 루트를 생성기에 명시 인자로 넘긴다.
- 그 루트를 `sys.path[0]`에 넣은 뒤에만 모듈을 import한다.
- `read.__file__`, 계약 경로, `git rev-parse HEAD`가 모두 detached `99fad78` 트리인지 검사하고 아니면 생성 거부한다.
- 이 provenance 검사를 생성 명령의 출력과 픽스처에 남긴다.

### V-3 · HIGH · 설계 §2.9 T-2 · [plan.py:704](/home/laptop/projects/patent-docent/engine/lanes/plan.py:704) · [test_m21:50](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:50)

T-2의 “`/retry-` 레인 1”은 틀렸습니다. 이 하네스의 canonical-tail 1회 재시도는 다음 세 레인 로그 행을 만듭니다.

- `ground-independent`
- `ground-dependent`
- `synthesize`

실측:

> `RETRY_LANE_ROWS 3 ground-independent 1 ground-dependent 1 synthesize 1`

재시도 회차는 하나지만 레인 로그 행은 3개입니다. T28 §3③은 횟수를 레인 로그 행으로 읽으라고 명합니다.

닫는 법: 이 픽스처에서는 `/retry-1/` 행을 정확히 3개로 고정하고 세 task의 정확한 집합도 검사하십시오. “tail 재시도 회차 1개”와 “레인 로그 행 3개”를 구별해 적어야 합니다.

### V-4 · HIGH · 설계 §2.7 G4 · [read.yaml:540](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:540) · [test_m21:853](/home/laptop/projects/patent-docent/tests/test_m21_retry_budget_by_judgment_point.py:853)

G4는 `phases`를 한 방향으로만 검사합니다. 예를 들어 `read.schema.phases`를 다음처럼 바꿔도 G1~G6이 모두 통과합니다.

```yaml
phases: [exit, __ghost_phase__]
```

각 retry 행의 `phases ⊇ points`는 여전히 참이고, `{early, exit} ⊆ 사용된 phases`도 참입니다. 존치 시험 :853도 `early`와 `exit`의 포함 여부만 보므로 유령 값을 잡지 않습니다.

실측한 설계 술어 결과:

> `G4_AS_SPECIFIED_PASSES True UNKNOWN_PHASES ['__ghost_phase__']`

닫는 법: 모든 `checks_before_exit[].phases`에 대해 list/비어 있지 않음/중복 없음과 `phases ⊆ retry_budget.points[].id`를 검사하고, 유령 phase 변조를 self-test에 추가해야 합니다. retry 행의 `phases ⊇ points`는 그 뒤의 별도 조건으로 유지합니다.

### V-5 · HIGH · 설계 §2.6 `_retry_checks` · §2.7 G3 · [read.py:754](/home/laptop/projects/patent-docent/engine/stages/read.py:754)

다음 두 계약 오류의 처분이 정해지지 않았습니다.

1. 같은 `retry_budget.points[].id`가 두 번 선언된 경우 첫째 사용/합집합/거부 중 무엇인지.
2. `_retry_checks`가 말하는 “미지 id”의 정확한 우주가 출구 12개인지, 진입 `read.input-digest`까지 포함한 13개인지.

현행 `_retry_budget`는 첫 일치 행을 반환합니다. G3에는 판정점 id의 유일성·정확한 집합을 검사한다는 문언이 없습니다. M3가 임의 선택하게 됩니다.

닫는 법: 판정점은 정확히 `{early, exit}`, 각각 정확히 한 행이라고 명시하고 관문·런타임 양쪽에서 검사하십시오. `_retry_checks` 허용 검사 우주는 `READ_CHECK_IDS ∪ ENGINE_READ_CHECK_IDS`의 출구 12개로 명시하고, `read.input-digest`와 중복 id는 거부해야 합니다.

### V-6 · HIGH · 설계 §2.8 manifest `exceptions[].predicate`

다음 predicate는 정수 mask에 쓸 수 없는 표현입니다.

```text
check_ids.index('read.convergence') in mask
```

실행하면:

> `PREDICATE_ERROR TypeError argument of type 'int' is not a container or iterable`

M3가 문자열을 무시할지, 별도 문법으로 해석할지 결정해야 합니다.

닫는 법: predicate를 다음처럼 정확히 고정하십시오.

```python
repeated == 1 and (
    mask & (1 << check_ids.index("read.convergence"))
) != 0
```

테스트와 생성기가 이 동일한 비트 정의로 2,048개 키를 산출하게 해야 합니다.

### V-7 · MED · 설계 §4④ · §2.9 T-11

자기 신고 ④의 “T-11이 엔진과 관문의 `TERMINAL_ACTIONS` 상등을 대조한다”는 사실이 아닙니다. T-11 명세에는 정본/자기시험/plain·`-O`/임시 YAML 3종만 있고 두 어휘 셋의 상등 검사가 없습니다.

`reject-upstream`은 8,190칸 골든에도 나타나지 않으므로 이 누락은 골든으로도 보완되지 않습니다.

닫는 법: 테스트가 엔진 상수와 관문 상수를 독립적으로 읽어 정확히 같은 세 값인지 대조한다고 T-11에 명시하십시오. 관문 자체는 계속 엔진을 import하지 않아도 됩니다.

### V-8 · MED · 설계 §2.2 손검산·순서 설명 · [read.py:1937](/home/laptop/projects/patent-docent/engine/stages/read.py:1937) · [__init__.py:101](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)

§2.2에는 두 사실 오류가 있습니다.

- “schema/source-digest가 없고 repeated=True면 4행”은 lane-log-only 3칸에서 틀립니다. 정확한 반례는 mask `1024`, `2048`, `3072`의 `repeated=1`; 모두 가드가 `StageError`를 냅니다.
- “격자 순 halt → escalate → reject”는 실제 격자와 반대입니다. `worst_status`는 `halt > reject-upstream > escalate`입니다. 현재 11행 순서는 halt → escalate → reject이며, 이것은 격자 순이 아닙니다.

R6 자체는 올바릅니다. `terminal_action()`이 모든 후보를 검증한 뒤에만 `worst_status`를 호출하므로 `order.get(미지값, 0)` 경로는 정상 구현에서 도달하지 않습니다.

닫는 법: 손검산에 lane-log-only 3칸 예외를 명시하고, 행 순서는 “동률 tie-break 순서”와 “조치 격자 순서”를 분리해 설명하십시오. 필요하면 reject 행을 escalate 행들 앞으로 옮기되 row 4가 다른 escalate 행보다 앞이라는 조건은 유지해야 합니다.

---

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회 |
| T26 §2⒜② 격자+계약 순서 | covered | §2.2·§2.6. 8,190칸 값은 일치. 설명 오류는 V-8 |
| T26 §2⒜③ 완전성·재시도 정확 등식·부분집합 | partially | G2/G3와 출구 subset은 맞으나 판정점 유일성·id 우주가 비어 있음(V-5) |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | partially | 값·계수는 맞지만 기준 트리 생성 보장이 없음(V-2) |
| T26 §3③ 양방향 관문+세 심기 | covered | self-test ⑴~⑷가 세 필수 심기를 덮음 |
| T26 §3④ 관문 계수 정정 마커 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | partially | 알고리즘은 전건 일치, 골든 provenance는 V-2 |
| T28 §3② 예외 표지 | partially | 2,048 계수는 맞으나 predicate가 실행 불능(V-6) |
| T28 §3③ 실제 러너 0회+양성 1회 | partially | 주입 대상 오류(V-1), 로그 행 수 오류(V-3) |
| T28 §3④ exit에서 convergence 제외+등식 | covered | §2.3·G3 |
| T29 §3① 골든 id 12개 | covered | §2.8 literal 목록+양방향 집합 대조 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 행/표지/halt/출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

추가 설계 중 `judged_at`, 결속 분류, fail-closed 미지 id, 조기 가드, 골든 디렉터리 위치는 공학 재량입니다. 새 재정 사항은 아닙니다. 다만 V-2·V-5처럼 그 재량의 정확한 실행값이 빠진 곳은 보충해야 합니다.

T31을 라운드 B 뒤로 분리한 판단은 T31 §2⒜와 일치합니다. T32를 T31 소라운드에 합치는 것도 T32 §3⑤가 허용한 총괄 재량입니다.

## B. 오늘의 표 불변

판정: 값 자체는 PASS, 설계 문서·골든 절차는 FAIL입니다.

직접 전수 호출 결과:

| 결과 | 계수 |
|---|---:|
| `halt, None` | 6,144 |
| `escalate, None` | 1,023 |
| `escalate, 반복 라벨` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 술어 | 2,048 |

제안 11행을 독립적으로 모델링해 HEAD와 비교한 결과:

> `MISMATCHES 0 []`

틀린 손검산 칸은 `repeated=1`이면서 실패 집합이 lane-log 두 id의 비공집합인 세 칸입니다. §2.8과 §3은 이 세 칸을 맞게 적었지만 §2.2 손검산만 틀렸습니다.

## C. B-1~B-7 폐쇄

| 1차 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | partially | β 루프 순서는 맞아 `repeated ∧ convergence`가 도달 불능. 그러나 필수 T-1/T-2가 V-1·V-3으로 깨짐 |
| B-2 | closed | 출구 12개·8,190칸, input-digest 별도 진입 경로가 T29와 일치 |
| B-3 | partially | 고정 파일·기준 해시·전 칸 값 구조는 맞으나 생성기가 실제 `99fad78` 모듈을 읽는다는 보장이 없음(V-2) |
| B-4 | partially | G3 등식은 `phases` 없이 정확히 섬. G4가 유령 phase를 통과시킴(V-4) |
| B-5 | closed | `then` 없는 retry, `then: retry(n)`, 비-retry의 `then`을 관문과 런타임 모두 거부 |
| B-6 | closed | kind 3종, upstream 식별 키만, 호출자 0, deferred/test_bound |
| B-7 | closed | pytest 2모드와 관문 7종 2모드가 §2.11에 명시됨 |

## D. 출구 convergence 도달 가능성

사실 주장은 맞습니다.

- `decompose_only_spec`은 같은 `assemble_spec`을 씁니다: [read.py:980](/home/laptop/projects/patent-docent/engine/stages/read.py:980), [read.py:995](/home/laptop/projects/patent-docent/engine/stages/read.py:995).
- 조기 canonical 입력은 `decomposes[canonical_run]`입니다: [read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495).
- tail은 입력받은 같은 `decompose` 객체를 그대로 반환하고 최종 조립도 그것을 씁니다: [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680), [read.py:1694](/home/laptop/projects/patent-docent/engine/stages/read.py:1694).
- 양쪽 모두 claims를 deepcopy한 뒤 같은 `rewrite_claims`를 적용합니다: [read.py:528](/home/laptop/projects/patent-docent/engine/stages/read.py:528).
- 분해 항목이 항상 첫 lane이라 claims의 component 매핑은 후속 payload와 무관합니다.
- 후속 synthesis 때문에 달라질 수 있는 `applicant_interest.material_id`는 `SpecIndex`와 6축이 읽지 않습니다.
- 6축은 청구항 수·문언·트리·종속 서명·addition 부착만 읽습니다: [convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104).

따라서 현재 코드에서 “조기 exact-match 통과 후 출구 convergence만 실패”시키는 레인 페이로드는 없습니다.

검사층 주입이라는 시험 형태는 타당하며 실제 `run()` 경로 조건도 충족할 수 있습니다. 다만 v2의 패치 좌표는 V-1 때문에 틀렸습니다. `engine.stages.read.run_read_checks`를 정확히 패치하면 T-1의 형태는 원장을 충족합니다.

부분집합 검사가 서명 검사보다 앞이면 convergence가 든 첫 실패에서 즉시 루프를 나가므로 `repeated_signature`가 설정되지 않습니다. 따라서 `repeated=True ∧ convergence`는 실제 출구 경로에서 도달 불능입니다.

## E. 자기 신고 ①~⑫

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 위치는 원장이 정하지 않은 공학 재량 |
| ② | 맞다 | T29가 input-digest를 골든 밖으로 승인 |
| ③ | 맞다 | 키 이름을 T29가 v2에 위임했고 test_bound가 실물과 맞음 |
| ④ | 틀렸다 | T-11에 엔진/관문 terminal 어휘 상등 검사가 없음(V-7) |
| ⑤ | 맞다 | 공식 12-id 영역에서 row 4 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 기존 유효 행의 값을 바꾸지 않는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 선언/구현 불일치라는 무효 입력이며 fail-closed 예외는 공학 재량. 정상 12-id 판정 공간 변경이 아님 |
| ⑧ | 맞다 | T29 §3③이 관문에 `action: halt` 대조를 직접 명함 |
| ⑨ | 맞다 | 조기 가드는 목록을 실행 결정에 쓰지는 않지만 런타임에서 실제 읽어 대조함. §2.5의 why가 그 경계를 정직하게 밝힘 |
| ⑩ | 틀렸다 | 주입 층의 선택은 맞지만 적힌 `m2` 패치 대상은 러너에 닿지 않음(V-1) |
| ⑪ | 맞다 | T28이 요구한 표지는 그 술어 하나. 다른 기존 도달 불능은 표지 대상 아님. 단 predicate 표현은 V-6 |
| ⑫ | 맞다 | T31은 B 뒤, T32는 B/T31 중 총괄 재량이므로 T31 소라운드 선택 가능 |

Owner 재정이 새로 필요한 자기 신고 항목은 없습니다. 남은 문제는 공학 설계 오류와 결정 공백입니다.

## F. 관문 G1~G6

| 관문 | 판정 | 설명 |
|---|---|---|
| G1 | covered | 검사 id 유일성, kind 사전, xor |
| G2 | covered | 선언 검사↔행 checks 양방향 차집합 0 |
| G3 | partially | `phases` 없이 정확 등식은 맞음. 판정점 id 유일성은 빠짐(V-5) |
| G4 | missing | 유령 phase와 비-retry 행의 추가 phase를 거부하지 못함(V-4) |
| G5 | covered | T29의 entry 표지·halt·출구 제외 |
| G6 | covered | R6의 세 잘못된 형태를 모두 거부 |

16종은 원장이 요구한 세 심기를 모두 덮습니다.

- 행 없는 검사: ⑴
- 검사 없는 행: ⑵ `read.__ghost__`
- 재시도 목록↔행 불일치: ⑶·⑷
- 1차 도전 E의 거짓 `points:[early]`: ⑽

그러나 `read.schema.phases`에 `__ghost_phase__`를 추가하는 변조는 관문과 존치 시험을 모두 통과합니다. 따라서 관문 설계는 FAIL입니다.

## G. M3가 만날 결정 공백

최소 다음이 남습니다.

- 골든 생성기가 detached `99fad78` 모듈을 import하도록 만드는 정확한 경로·검증 방식(V-2).
- `_retry_checks`의 미지 id 우주와 중복 판정점 처리(V-5).
- 실행 불가능한 exception predicate의 실제 문법(V-6).
- T-1의 잘못된 monkeypatch 좌표를 그대로 따를지 교정할지(V-1).
- “재시도 1회”를 로그 1행으로 볼지 현재 실물 3행으로 볼지(V-3).

따라서 이 설계를 그대로 M3에 넘길 수 없습니다.

## 검증 경로

주요 실행 명령과 마지막 출력입니다.

- `git status --short && git rev-parse --short HEAD && git rev-parse HEAD^{tree}`  
  마지막 출력: `0cf666a351c95e5685bf4eb09a4e47c96c2caaff`

- `git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l`  
  마지막 출력: `0`

- HEAD `_failure_verdict` 12-id 비공집합×repeated 전수 호출  
  마지막 출력: `TOTAL 8190`

- 제안 11행 알고리즘과 HEAD 전수 대조  
  마지막 출력: `MISMATCHES 0 []`

- 하네스 payload의 canonical-tail 레인 수 계산  
  마지막 출력: `RETRY_LANE_ROWS 3 ground-independent 1 ground-dependent 1 synthesize 1`

- `m2.run_read_checks` 메모리 패치가 러너 전역에 닿는지 대조  
  마지막 출력: `PATCH_REACHES_RUNNER False M2_PATCHED True`

- G4 술어에 유령 phase를 메모리 주입  
  마지막 출력: `G4_AS_SPECIFIED_PASSES True UNKNOWN_PHASES ['__ghost_phase__']`

- manifest predicate 직접 평가  
  마지막 출력: `PREDICATE_ERROR TypeError argument of type 'int' is not a container or iterable`

- 신설 대상 파일 존재 확인  
  마지막 출력: `ABSENT tests/test_m24_failure_grid_golden.py`

- 종료 후 `git status --short`  
  마지막 출력: `(clean; no output)`

## [미검증]

- `tools/check_failure_table.py`, 골든 manifest/generator, `test_m24_failure_grid_golden.py`는 아직 존재하지 않아 실제 실행할 수 없었습니다.
- 전체 pytest와 관문은 임시 파일·리포를 만드는 실행이므로 “리포에 아무것도 쓰지 말라”는 이번 read-only 규율 아래 실행하지 않았습니다.
- 실제 골든 생성 worktree도 만들지 않았습니다. 따라서 V-2는 제시된 명령·Python import 경로와 부재한 provenance 조건을 정적 검증한 결과입니다.
- 리포에는 아무것도 쓰지 않았고 작업 트리는 끝까지 깨끗했습니다.