# 독립 감수 원문 — 재정 T26 집행 설계 v11 의 M1b 설계 도전(10차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v11/final.txt` 의 sha256 `2a8d24270271b638cb399914c49e3c63a1b2b5968952c2d0d38fd305b082561d` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 28분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 10차 심사** — v10(9차 FAIL · AC-1~AC-5) → **v11** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`3ace14b` · 9차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 3건(HIGH 1 · MED 2 · BLOCKER 0) · 새 재정 사항 0 · AC-1~AC-5 전건 closed · X-1·AB-1 은 AD 로 partially 재기재.**
값 8,190 칸은 열 번째로 일치. **AD-1**: 검증기 음성 시험이 여러 필드를 함께 바꾸고 「위반 ≥ 1」만 요구해, 검사 하나를 통째로 빼도(예: `generator`)
다른 검사가 가려 전건 통과 — 「모든 값 필드 검사」 주장이 수락 시험으로 반증되지 않는다. **AD-2**: G1 골격 상수 열거에 `judged_at` 이 없어 3행의 필수
키와 어긋나고, 열거 밖 기계 키 추가가 통과. **AD-3**: 생성 명령 네 줄이 fail-fast 가 아니다(첫 줄 사전조건이 실패해도 진행 · 마지막 줄 `EXIT=0` 미검사) ·
B-0 시험은 생성기 단독만 실행.

지적 열거 = AD-1, AD-2, AD-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§16** 에 있다.
셋 전부 **수용**(공학 · 규율 11 ③) — **v12** 에 반영하고 11차 도전에 냈다. v12 = 검증기 위반 문장을 **필드 경로 토큰**으로 시작하게 하고 음성 시험을
**한 필드씩**(표 T-V · 각 시험은 그 토큰의 위반 실재를 검사) · G1 상수에 `judged_at` 열 + 행별 허용 키 집합 정확 일치 + 변조 ㉜㉝ · 생성 명령 블록을
`set -euo pipefail` + `trap` + 마지막 줄 `EXIT=0` 대조로 재작성하고 환경변수(`MAIN`·`BASE`·`OUT_PATH`)로 매개해 B-0 시험이 블록 전체를 서브프로세스로
돌린다(성공 · 사전조건 실패 · 생성기 실패).

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

AC-1~AC-5 자체는 모두 닫혔고 8,190칸 값도 정확합니다. 그러나 골든 검증 시험의 공백, G1 골격의 `judged_at` 모순, 생성 명령의 fail-open 셸 구조가 새로 남았습니다.

## AC-1~AC-5 우선 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| AC-1 | closed | 생성기는 형제 경로, T-7/B-0은 `tests/fixtures/...` 경로를 사용한다. 세 계산 결과가 모두 같은 검증기 경로였다. |
| AC-2 | closed | `cell_key`는 예시 하나가 정본이고 강조 문자가 없어졌다. `generation_command`도 물리 네 줄 한 블록으로 유일해졌다. 실행 의미의 새 결함은 AD-3이다. |
| AC-3 | closed | B-0 세 파일 병합 → main에서 manifest 생성 → 골든 커밋 → B 시작 순서와 누적 네 파일이 명시됐다. |
| AC-4 | closed | T-7 범위가 §2.8 시험 ①~③으로 고쳐졌고 ④는 총괄 수락 단계로 분리됐다. |
| AC-5 | closed | `assemble_spec`가 정확히 `read.py:506-561`로 고쳐졌다. |

## 지적 목록

### AD-1 · HIGH · 설계 §2.8 검증기 단위 시험·T-7 ③

검증기가 약속한 모든 필드 검사를 시험이 독립적으로 결속하지 않습니다.

- `generator`를 바꾸는 음성 시험이 전혀 없습니다.
- `exceptions.id`, `cell_count`, provenance의 절대경로 필드와 `generated_at`도 단독 변조가 없습니다.
- ⓗ는 `rule`과 `meaning`을 함께, ⓘ는 `$comment`·`cell_key`·`generation_command`를 함께, ⓙ는 계수 타입과 provenance 여분 키를 함께 바꿉니다.
- 각 사본은 단지 “위반 ≥ 1”만 요구합니다. 따라서 예를 들어 `meaning` 검사를 구현하지 않아도 `rule` 검사가 ⓗ를 떨어뜨립니다. `generation_command` 검사를 빼도 ⓘ의 다른 두 검사가 가립니다.
- `generator` 검사를 통째로 빼는 구현은 열거된 모든 음성 시험을 그대로 통과합니다.

즉 AB-1의 “모든 값 필드가 검사된다”는 구현 누락을 수락 시험이 반증하지 못합니다.

닫는 법: 각 독립 제약마다 한 필드만 바꾸는 변조를 두고, 단순한 오류 개수 대신 해당 필드명의 진단이 포함됐는지 검사하십시오. 최소한 최상위 10키, provenance 8키, exception 6키의 값·형식 제약을 각각 단독으로 흔들어야 합니다.

### AD-2 · MED · 설계 §2.7 G1·T-13, §2.2 3행

G1의 `APPROVED_FAILURE_TABLE` 열거에서 `judged_at`이 빠졌는데, 같은 문장은 `condition`·`note`만 자유라고 합니다.

- 정본 3행에는 `judged_at: entry`가 반드시 있습니다.
- G1 상수의 열거 필드는 `checks/kind`, `action`, `then`, `reason_label`, `points`뿐입니다.
- 열거된 projection만 비교하면 다음 변조가 G1~G6의 관측값을 바꾸지 않습니다.

```yaml
failure:
  - checks: [read.schema]
    action: retry(1)
    then: halt
    points: [exit]
    unapproved_machine_field: halt
```

- 반대로 “산문 둘 이외의 모든 키”를 상수와 비교하면, 상수 열거에 없는 정본 `judged_at`을 어떻게 포함할지 M3가 별도 규칙을 만들어야 합니다.

T-10이 미분류 키를 잡을 가능성은 있지만, 그것은 G1이 주장하는 “승인 골격 전체 정확 일치”를 대신하지 않습니다.

닫는 법: `APPROVED_FAILURE_TABLE`에 `judged_at` 열을 명시적으로 포함해 3행만 `"entry"`, 나머지는 부재로 고정하십시오. 행별 허용 키 집합도 정확히 적고 알 수 없는 키 추가 변조를 `--self-test`와 T-13에 넣어야 합니다.

### AD-3 · MED · 설계 §2.8 생성 명령 정본

정본 네 줄은 fail-fast 명령이 아닙니다. 줄 사이가 `&&`로 이어지지 않고 `set -e`도 없습니다.

따라서 첫 줄의 핵심 사전조건:

```bash
test "$(git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l)" = 0
```

이 실패해도 둘째~넷째 줄이 계속 실행됩니다. 마지막 `git worktree remove`가 성공하면 전체 셸 상태는 0이 됩니다. 셋째 줄도 생성기 출력을 흘릴 뿐 “마지막 줄이 `EXIT=0`”인지 검사하지 않습니다. B-0 시험은 이 네 줄 전체가 아니라 생성기 단독 subprocess만 실행합니다.

실측한 셸 의미:

> `FINAL sequential_failure_then_success_rc=0`

닫는 법: 네 줄 정본 자체를 `set -e` 또는 줄간 `&&`로 fail-fast하게 만들고, 실패 시에도 worktree를 정리하는 `trap`을 두십시오. 생성기 출력을 보존하면서 마지막 줄의 `EXIT=0` 표지를 실제 비교해야 합니다. B-0은 생성기 단독 호출 외에 이 정본 블록 전체도 subprocess로 실행해 사전조건 실패·생성기 실패가 최종 nonzero인지 반증해야 합니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·이유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1·§2.2·§2.6·G1/G2 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·§2.6; 전수 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | §2.3·G2~G4·`_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | partially | 값은 맞지만 골든 수락면과 생성 정본이 AD-1·AD-3으로 완결되지 않음 |
| T26 §3③ 양방향 관문·세 심기 | covered | 필수 세 심기는 ⑴~⑷에 있다. AD-2는 그보다 강한 G1 “전체 골격” 주장 결함 |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11에 두 pytest 모드와 7관문 두 모드가 있음 |
| T28 §3① 8,190칸 한 칸도 불변 | partially | 계산·T-7 값 대조는 맞지만 독립 골든 수락 절차가 AD-1·AD-3 |
| T28 §3② β 표지 | partially | 고정 술어와 2,048 집합은 맞다. 다만 `exceptions`의 개별 필드 검사 누락을 음성 시험이 가리는 AD-1 |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2; 주입·3 레인 좌표가 실물과 일치 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 12 id | covered | 목록 유일성·12개·집합 상등·키 우주 |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ entry 표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·이연 | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤 소라운드로 미루고 T32를 그 소라운드에 합치는 판단은 각각 T31 §3①, T32 §3⑤와 맞습니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, R8/R9, B-0, provenance 검사, 승인 상수는 공학 재량 또는 원장값 기록입니다. AD-1~AD-3도 새 Owner 재정 없이 고칠 수 있는 공학 오류입니다.

## B. 오늘의 표 불변

전수 실측 결과 v11 모형과 HEAD의 틀린 칸은 없습니다.

| 결과 | 계수 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v11 ↔ HEAD 불일치 | 0 |

`StageError`는 `(mask, repeated) = (1024,1), (2048,1), (3072,1)`입니다. §2.2 손검산은 V-8의 누락을 정확히 고쳤습니다.

`worst_status` 자체는 여전히 미지 값을 0으로 취급합니다.

> `FINAL known=halt unknown_only=ok mixed=escalate`

그러나 v11의 `select_failure_row()`는 모든 후보를 먼저 `terminal_action()`으로 검증하므로 R6대로 구현하면 미지 terminal이 `worst_status`까지 도달하지 않습니다. `then` 없는 retry, `then: retry(n)`, 비-retry의 `then`도 관문과 런타임 양쪽에서 거부됩니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 이유 |
|---|---|---|
| B-1 | closed | β 부분집합 검사가 서명보다 앞이고 T-1/T-2가 실러너 경로를 사용 |
| B-2 | closed | 출구 12 id·8,190칸·input-digest 별도 진입 반증 |
| B-3 | partially | `99fad78` 독립 생성 원리는 맞지만 골든 검증 시험과 정본 명령이 AD-1·AD-3 |
| B-4 | closed | `phases` 없이 판정점별 정확 등식 |
| B-5 | closed | 세 잘못된 `then` 형태를 관문·런타임 모두 fail-closed |
| B-6 | closed | kind 3종·upstream 호출자 0·`deferred/test_bound` |
| B-7 | closed | pytest와 전 관문의 두 모드 명령이 완전함 |

### V-1~V-8

| 지적 | 판정 | 이유 |
|---|---|---|
| V-1 | closed | `engine.stages.read.run_read_checks`를 패치 |
| V-2 | closed | `-I`·repo 선삽입·6 provenance 검사로 대상 트리 고정 |
| V-3 | closed | `/retry-1/` 정확히 3행·세 task |
| V-4 | closed | phase 형식·우주·유령 phase 거부 |
| V-5 | closed | 판정점 유일성·정확한 12-id 우주 |
| V-6 | closed | 실행 가능한 고정 predicate |
| V-7 | closed | T-11 ⑤ 종단 어휘 상등 |
| V-8 | closed | StageError 3칸과 두 순서 구별 |

### N-1~N-7

| 지적 | 판정 | 이유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전에 절대화 |
| N-2 | closed | 12개 phase 전건 실측 |
| N-3 | closed | B-0 병합 → 골든 → B 순서가 명시됨 |
| N-4 | closed | `_exit_retry_eligible` 명명·직접 시험 |
| N-5 | closed | T-12 계약↔엔진 상수 양방향 다리 |
| N-6 | closed | `exit` 필수·`early` iff |
| N-7 | closed | 다섯 문언 모두 구체화됨 |

후대 지적 중 X-1의 “골격 전체 정확 일치”는 AD-2 때문에 `partially`, AB-1은 AD-1 때문에 `partially`입니다. 나머지 W·X·Y·Z·AA·AB 항목은 다시 열리지 않았습니다.

## D. 출구 convergence 도달 가능성

v11의 “레인 페이로드로 도달 불능” 결론은 맞습니다.

- [`decompose_only_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 [`assemble_spec`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 호출합니다.
- tail은 입력 `decompose` 객체를 그대로 반환합니다([read.py:899](/home/laptop/projects/patent-docent/engine/stages/read.py:899)).
- 조기와 출구는 같은 `decomposes[canonical_run]`을 씁니다([read.py:1495](/home/laptop/projects/patent-docent/engine/stages/read.py:1495), [read.py:1680](/home/laptop/projects/patent-docent/engine/stages/read.py:1680)).
- 양쪽 모두 claims를 deepcopy한 뒤 같은 `rewrite_claims`를 적용합니다([read.py:532](/home/laptop/projects/patent-docent/engine/stages/read.py:532)).
- 후속 조립으로 달라진 `applicant_interest.material_id`는 수렴 6축이 읽지 않습니다.
- `peer_spec`의 실물 읽기는 [`convergence.py:94`](/home/laptop/projects/patent-docent/reader/lib/convergence.py:94)와 [`:105`](/home/laptop/projects/patent-docent/reader/lib/convergence.py:105)뿐입니다.

메모리 조립·주입 결과:

> `FINAL base_status=pass base_fail=[] injected_status=fail injected_fail=['independent-count']`

따라서 출구에서만 convergence를 떨어뜨리는 레인 페이로드는 없습니다. T-1이 [`read.py:1743`](/home/laptop/projects/patent-docent/engine/stages/read.py:1743)의 모듈 전역 `run_read_checks`를 패치하는 형태는 실제 러너 경로이며 T28 §3③을 충족합니다.

상신축 러너 시험도 이미 [`test_m2_read.py:2727`](/home/laptop/projects/patent-docent/tests/test_m2_read.py:2727)에 있으므로 T-8의 조건문은 실물상 “러너 경로 시험도 추가”로 결정됩니다.

## E. 자기 신고 ①~⑳

| # | 판정 | 이유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | T29가 승인한 영역 밖 값 |
| ③ | 맞다 | 키 이름은 T29가 설계에 위임 |
| ④ | 맞다 | T-11 ⑤가 엔진·관문 어휘를 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 비-retry `then` 금지는 형태 규율 |
| ⑦ | 맞다 | 미지 id는 공식 우주 밖 무효 입력이며 StageError는 fail-closed |
| ⑧ | 맞다 | `action: halt`는 T29 §3③ 명시값 |
| ⑨ | 맞다 | 가드가 early·exit 목록을 실제 읽어 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 검사기 자체의 `independent-count`를 fail로 만듦 |
| ⑪ | 맞다 | 표지 대상은 T28 술어 하나 |
| ⑫ | 맞다 | T32의 T31 소라운드 합류가 허용됨 |
| ⑬ | 맞다 | 판정점·검사 id 우주 고정은 형식 규율 |
| ⑭ | 맞다 | `-I`와 6검사는 import된 엔진/reader가 대상 트리에서 왔음을 증명 |
| ⑮ | 맞다 | B-0 분리 및 승격 순서는 현재 완결됨 |
| ⑯ | 맞다 | R9는 현행 정본을 그대로 통과 |
| ⑰ | 맞다 | 승인 3/8은 원장값이고 T-11 ⑥이 두 상수를 잇는다 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 틀렸다 | “기계 필드 전체” 상수 열거에서 `judged_at`이 빠졌고 알 수 없는 키 거부 방식이 비어 있음(AD-2) |
| ⑳ | 맞다 | 주입은 실제로 `independent-count` 하나만 fail |

새 Owner 재정이 필요한 자기 신고 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 근거 |
|---|---|---|
| G1 | partially | 행 수·분할·순서·주요 필드는 고정하지만 `judged_at`과 허용 키 집합이 AD-2로 불완전 |
| G2 | covered | 선언↔행 차집합 양쪽 0·배열 중복 거부 |
| G3 | covered | 정확 등식·승인 3/8·엄격 int·예산 1 |
| G4 | covered | phase 형식·우주·exit 필수·early iff |
| G5 | covered | input-digest entry·halt·points 부재·재시도 제외 |
| G6 | covered | 세 잘못된 `then` 형태 거부 |

실제 열거는 16종이 아니라 ⑴~㉛ 31종입니다. 원장 필수 심기는 모두 있습니다.

- 행 없는 검사: ⑴
- 검사 없는 행·`read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶·⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽
- 동시 일관 변조: ㉑

다만 `unapproved_machine_field` 추가는 열거된 기계 필드 projection을 그대로 구현한 G1을 통과합니다. 이를 막도록 해석하면 `judged_at`의 상수 표현을 M3가 임의 보충해야 합니다.

## G. M3 결정 공백

최소 두 곳입니다.

1. `APPROVED_FAILURE_TABLE`에 열거되지 않은 `judged_at`을 골격 비교에 포함할지, G5 전용 필드로 projection에서 뺄지, 알 수 없는 추가 키는 어떻게 거부할지(AD-2).
2. `generation_command`를 바이트 정확히 복사해 fail-open 상태로 둘지, fail-fast하게 고쳐 정본 문자열을 위반할지(AD-3).

AD-1은 문언상 검사값은 정해졌지만, 누락 구현이 모든 수락 시험을 통과할 수 있는 검증 공백입니다. 이 셋은 Owner 판단이 아니라 설계 문언과 시험을 보수하면 닫힙니다.

## 검증 경로

- HEAD·불변성:

  `git rev-parse --short=12 HEAD`

  > `3ace14b71a6e`

  도전 중 예고된 문서 전용 커밋이 반입됐습니다.

  `git diff --name-only c57b887 HEAD -- engine contracts reader tests tools | wc -l`

  > `0`

  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`

  > `0`

  `git status --short`

  > 빈 출력

- 기준 해시:

  `git rev-parse 99fad78`

  > `99fad78c318875af99aa87083c029d2c6724e240`

- `_failure_verdict` 8,190칸 전수 호출 + 독립 v11 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 counts={('halt', None): 6144, ('escalate', None): 1023, ('escalate', '국면 간 변이 재현 — 코드 결함 의심'): 1020, 'StageError': 3} stage_cells=[(1024, 1), (2048, 1), (3072, 1)]`

- 선언·국면:

  > `FINAL exit_count=12 exit_unique=True entry_ids=['read.input-digest'] point_ids=['early', 'exit'] early=['read.claim-inventory', 'read.convergence', 'read.dependency-parse'] all_exit=True phase_universe=['early', 'exit']`

  계약↔코드 상수:

  > `FINAL exit_minus_code=[] code_minus_exit=[] exit_duplicates=[] entry=['read.input-digest'] early_minus_expected=[] expected_minus_early=[]`

- 검증기 경로 세 호출자:

  > `FINAL generator=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py t7=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py b0=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py expected=/home/laptop/projects/patent-docent/tests/fixtures/read-failure-grid/validate_manifest.py`

- 조립·주입:

  > `FINAL base_status=pass base_fail=[] injected_status=fail injected_fail=['independent-count']`

  원본 claims는 바이트 동일하지 않았고 `applicant_interest.material_id`가 `M11→M9`였지만 수렴 판정은 pass였습니다.

- T-2 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-independent', 'ground-dependent', 'synthesize'] ids=['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0'] all_retry1=True`

- `worst_status`:

  > `FINAL known=halt unknown_only=ok mixed=escalate`

- 셸 실패 전파:

  `bash -c 'false; true'`

  > `FINAL sequential_failure_then_success_rc=0`

- `peer_spec` 읽기:

  `rg -n 'ctx\\.peer_spec' reader/lib`

  > `reader/lib/convergence.py:105:    right = SpecIndex.build(ctx.peer_spec)`

- 신설물 존재:

  > `tools/check_failure_table.py=absent`

## [미검증]

- `generate.py`, `validate_manifest.py`, 두 신규 시험, manifest, `check_failure_table.py`가 아직 없어 실제 실행하지 못했습니다.
- detached `99fad78` worktree 생성은 쓰기 작업이므로 실행하지 않았습니다.
- 전체 pytest와 관문 plain/`-O`는 파일·캐시·임시 산출을 만들 수 있어 실행하지 않았습니다.
- T-1/T-2 완성 통주는 런 디렉터리를 쓰므로 실행하지 않았습니다. 조립·수렴 주입과 레인 계획은 메모리에서 검증했습니다.
- AD-2의 변조는 아직 관문 구현이 없어 설계에 열거된 G1~G6 술어를 기준으로 판정했습니다.