# 독립 감수 원문 — 재정 T26 집행 설계 v4 의 M1b 설계 도전(3차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v4/final.txt` 의 sha256 `519c9aeef299e641a824289b8d966f1a2acce0535c7187a58e32d2c9dd9a6d71` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 25분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 3차 심사** — v2(2차 FAIL · V-1~V-8) → 자문(fable xhigh · REVISE ·
N-1~N-7) → **v4** 에 대한 것. 도전 중 총괄이 문서 전용 커밋 `4e1f05c`(감수 원문 3건 반입)를 넣었고 도전자는 코드 경로
(`engine contracts reader tests tools`)가 `663c77e` 와 diff 0 임을 확인해 진행했다 — 발주문이 그 가능성을 고지했다.

**대상** = 총괄 저작 설계 메모 `T26-DESIGN-v4.md`(세션 스크래치 · 50,912 B) · 기준 커밋 `663c77e`(→ 문서 커밋 `4e1f05c`) · 골든 기준 트리 `99fad78`.

**판정 = FAIL · 지적 4건(BLOCKER 1 · HIGH 1 · MED 1 · LOW 1) · 새 재정 사항 0 · 이전 지적 B-1~B-7 · V-1~V-8 · N-1~N-7 은 전건 closed(B-5 만
partially — W-2 로 이어진다).** 값 8,190 칸은 세 번째로 일치했다(`MISMATCHES 0`). 새로 찾은 것 — **W-1**: 승인된 출구 재시도 8종이 독립
정답지에 결속되지 않아, exit 목록에서 검사 하나를 빼고 그 행을 비-retry `escalate` 로 갈라 두면 관문 전종·골든·T-12 를 전부 통과하면서
실제 재디스패치가 1→0 으로 줄어든다(T28 이 승인한 실동작 변경은 convergence 하나뿐). **W-2**: 조기 상신축 갈래가 `action` 을 직접 써서
`terminal_action()` 의 런타임 fail-closed 를 우회한다. **W-3**: 선언 배열의 중복을 아무도 검사하지 않는다. **W-4**: 문서 계수 충돌(18/20).

지적 열거 = W-1, W-2, W-3, W-4

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§9** 에 있다.
넷 전부 **수용**(공학 수정 · 규율 11 ③) — **v5** 에 반영하고 4차 도전에 냈다. v5 의 핵심 = 승인 재시도 집합을 **엔진 상수(진입 가드) + 관문 상수(G3)**
로 고정(원장 T26 ⒜ ③ · T28 β · T25 가 정한 값의 기록 — 값을 아는 자리가 둘 더 생기며 G5 의 `halt` 와 같은 격 · §4 ⑰ 자기 신고) ·
`_gate_escalation_verdict()` 가 `terminal_action()` 을 지나게 · 선언 배열 중복 검사 · 자기 시험 변조 24종.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

8,190칸의 `(조치, 라벨)`은 v4와 HEAD가 전부 일치합니다. 그러나 승인된 출구 재시도 8종을 독립적으로 고정하지 않아 실제 재디스패치를 몰래 줄이는 변조가 모든 관문·골든 대조를 통과하며, 조기 상신 분기는 `terminal_action()`을 우회합니다. 선언 id 중복과 문서 계수 충돌도 남았습니다.

## 지적 목록

### W-1 · BLOCKER · 설계 §2.3 · §2.7 G3 · §2.9 T-2/T-4/T-12 · [read.py:1754](/home/laptop/projects/patent-docent/engine/stages/read.py:1754)

출구 재시도 8종이 독립적인 정답지에 결속되지 않았습니다. G3는 `retry_budget.points[exit].checks`와 `points: [exit]` retry 행을 서로 비교할 뿐, 승인된 정확한 8종과 대조하지 않습니다.

다음 변조가 G1~G6, T-12, 8,190칸 골든을 모두 통과합니다.

1. exit 목록에서 `read.value-derivation` 삭제.
2. 9행을 나눠 `read.value-derivation` 전용 비-retry `action: escalate` 행으로 변경.
3. 나머지 네 검사는 기존 retry 행에 유지.

그러면 `read.value-derivation` 단독 실패의 최종 `(escalate, None)`은 같아서 골든이 green이지만, 실제 후속 재디스패치는 1회에서 0회로 바뀝니다. T28이 승인한 실동작 변경은 convergence 하나뿐인데 다른 검사의 행동도 바꿀 수 있습니다. T-2는 pointer-resolve 한 종만, T-4는 12종 중 일부만 양성으로 검사하므로 이 변조를 잡지 못합니다.

실측 모형:

> `MUTANT_ACCEPTED True REMOVED_RETRY read.value-derivation`

닫는 법:

- G3 또는 독립 시험에 승인된 정확한 집합을 고정하십시오.
  - early = `{claim-inventory, dependency-parse, convergence}`
  - exit = 설계 §2.3의 정확한 8종
- T-4를 출구 12종 전부에 대해 `eligible=True` 정확히 8종, `False` 정확히 4종으로 확장하십시오.
- exit 목록과 failure 행을 함께 바꾸는 위 변조를 관문 자기시험에 추가하십시오.

### W-2 · HIGH · 설계 §2.6 조기 게이트 · `failure_row_of_kind` · §2.9 T-8 · [read.py:1650](/home/laptop/projects/patent-docent/engine/stages/read.py:1650)

조기 상신축 분기가 R6의 런타임 fail-closed 경로를 우회합니다.

설계는 `failure_row_of_kind(contract, "gate-escalation")`의 결과에서 `action`을 직접 status로 쓰도록 명시합니다. 그런데 `failure_row_of_kind`는 0행/중복만 검사하고 `terminal_action()`을 호출하지 않습니다. 따라서 도달 가능한 gate-escalation 행에 다음 오류가 있으면:

```yaml
action: escalate
then: halt
```

G6는 거부하지만, 관문을 거치지 않은 런타임은 금지된 `then`을 무시하고 `escalate`를 반환합니다. 미지 action도 같은 경로에서 `StageError` 대신 그대로 흘릴 수 있습니다. T-8은 `terminal_action()` 직접 호출만 검사하므로 호출자 우회를 잡지 못합니다. 이는 B-5의 런타임 조건을 다시 엽니다.

닫는 법:

```python
entry = failure_row_of_kind(contract, "gate-escalation")
status = terminal_action(entry)
```

로 고정하고, 실제 조기 상신축 러너 경로에서 비-retry `then` 및 미지 action을 심어 `StageError`를 확인하십시오.

### W-3 · MED · 설계 §2.7 G2/G4 · §2.9 T-12 · [read.yaml:333](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:333) · [read.yaml:540](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:540)

`checks_on_entry`와 `checks_before_exit` 선언 id의 유일성을 검사하지 않습니다. G2와 T-12가 집합으로만 대조하므로 `read.schema` 선언을 똑같이 한 번 더 붙이면:

- 선언 행 수: 13
- 고유 id 수: 12
- R9: 통과
- T-12 집합 다리: 통과

실측:

> `DUPLICATE_MUTANT_ACCEPTED_BY_SPECIFIED_DECLARATION_CHECKS True`

이는 “출구 12 검사 정확히”를 다중집합 차원에서 보장하지 못하며, 중복된 두 선언의 `criterion`·`implemented_by`가 달라졌을 때 어느 선언이 정본인지도 정하지 않습니다.

닫는 법: G2가 두 선언 배열 각각에 대해 list/행 형식/id 문자열/중복 없음/정확한 개수를 검사하게 하고, entry·exit 중복 변조를 자기시험에 추가하십시오. T-12와 manifest 시험도 `len(ids) == len(set(ids)) == 12`를 명시해야 합니다.

### W-4 · LOW · 설계 §2.10 · §2.7 `--self-test`

설계 §2.7은 변조 20종을 열거하고 §2.11도 20종을 요구하지만, §2.10은 SPEC에 “자기 시험 18종”을 쓰라고 명합니다. M3가 지시를 그대로 따르면 문서가 실행물보다 좁아집니다.

닫는 법: §2.10의 `18종`을 `20종`으로 정정하십시오.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 키 조회 |
| T26 §2⒜② 격자·계약 순서 | covered | §2.2·§2.6. 전수 값 일치 |
| T26 §2⒜③ 완전성·재시도 정확 등식·부분집합 | partially | 내부 등식은 정확하나 승인된 8종이 독립 고정되지 않음(W-1), 선언 중복 허용(W-3) |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | covered | 99fad78 골든 절차와 T-7. 전수 모형 불일치 0 |
| T26 §3③ 양방향 관문·세 심기 | partially | 필수 세 단일 변조는 포함. 동시 일관 변조와 선언 중복을 통과시킴(W-1/W-3) |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 불변 | covered | §2.8 T-7; 직접 전수 일치 |
| T28 §3② β 표지 | covered | 실행 가능한 predicate, 2,048칸 |
| T28 §3③ 실제 러너 음성·양성 대조 | covered | T-1 패치 좌표와 T-2 레인 3행이 실물과 정합 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3. 단 다른 8종의 독립 고정은 W-1 |
| T29 §3① 골든 id 12개 | partially | 생성 절차는 12개를 내지만 시험·계약 다리는 집합 중복을 거부하지 않음(W-3) |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 행·표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 B 뒤로 분리하고 T32를 그 소라운드에 합친 범위 판단은 원장과 맞습니다. `screening_memos[].read_run`도 범위 밖으로 유지합니다.

`judged_at`, R8/R9, fail-closed 미지 id, provenance 거부, B-0 좌석은 공학·운영 재량입니다. W-1의 정확한 8종도 새 재정 사항이 아니라 이미 T26/T28이 정한 값을 검증에 고정하는 일입니다.

## B. 오늘의 표 불변

판정값 자체는 PASS입니다.

| 결과 | 직접 재계산 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |

v4 11행 의미와 HEAD `_failure_verdict`의 전수 대조:

> `MISMATCHES 0 []`

v4 손검산에서 새로 틀린 칸은 없습니다. 과거 누락됐던 세 칸은 `mask=1024, 2048, 3072`, `repeated=1`이며 v4가 모두 `StageError`로 바로잡았습니다.

R6가 모든 후보의 terminal을 먼저 검증한 뒤 `worst_status`를 호출한다면 `order.get(미지값, 0)`은 정상 `_failure_verdict` 경로에서 도달하지 않습니다. 다만 gate-escalation 직접 분기는 그 검증 자체를 호출하지 않으므로 W-2가 남습니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β, convergence exit 제외, 정확한 모듈 전역 주입, 0회/3행 대조가 섬 |
| B-2 | closed | 골든 영역 12개·8,190칸, input-digest 진입 시험 분리 |
| B-3 | closed | 값은 detached `99fad78` 구현에서 생성하고 B 구현은 동결 파일만 읽음 |
| B-4 | closed | 판정점별 행 분리, 등식에서 `phases`를 사용하지 않음 |
| B-5 | partially | 선택기 자체는 fail-closed이나 도달 가능한 gate-escalation 호출자가 우회함(W-2) |
| B-6 | closed | kind 3종, upstream 호출자 없음, deferred/test_bound |
| B-7 | closed | pytest와 관문 7종 모두 2모드. W-4는 문서 계수 오류 |

### V-1~V-8

| 지적 | 판정 | 사유 |
|---|---|---|
| V-1 | closed | `read_stage.run_read_checks` 패치가 러너 전역에 닿음 |
| V-2 | closed | `-I`, repo 선삽입, 모듈·계약·HEAD·path·clean 검사가 기준 트리를 결속 |
| V-3 | closed | retry 회차 1과 레인 행 3을 구별 |
| V-4 | closed | 유령 phase는 R9의 부분집합 검사와 변조 ⒄에서 거부 |
| V-5 | closed | 판정점 `{early, exit}` 유일성과 출구 12-id 우주를 런타임·관문에서 규정 |
| V-6 | closed | predicate가 정수 비트식으로 실행 가능 |
| V-7 | closed | T-11 ⑤가 관문·엔진 terminal 집합을 대조 |
| V-8 | closed | 세 StageError 칸과 격자/동률 순서를 정정 |

### N-1~N-7

| 지적 | 판정 | 사유 |
|---|---|---|
| N-1 | closed | `out`을 chdir 전에 절대경로로 고정 |
| N-2 | closed | 12건 phases를 실측했고 R9를 전부 만족 |
| N-3 | closed | B-0 → 골든 커밋 → B 순서가 명시됨 |
| N-4 | closed | `_exit_retry_eligible` 헬퍼와 함수 시험이 생김 |
| N-5 | closed | 유령 id+행은 T-12가 잡음. W-3은 별개의 중복 문제 |
| N-6 | closed | `exit` 필수와 early iff 규칙·변조 ⒆⒇ |
| N-7 | closed | 다섯 세부가 모두 구체화됨 |

## D. 출구 convergence 도달 가능성

설계의 사실 주장은 맞습니다.

- `decompose_only_spec`은 출구와 같은 `assemble_spec`을 호출합니다. [read.py:980](/home/laptop/projects/patent-docent/engine/stages/read.py:980)
- tail은 입력 `decompose` 객체를 그대로 반환하며, 러너는 조기에서 쓴 `decomposes[canonical_run]`을 tail에 전달합니다. [read.py:830](/home/laptop/projects/patent-docent/engine/stages/read.py:830), [read.py:1678](/home/laptop/projects/patent-docent/engine/stages/read.py:1678)
- 양쪽 조립은 claims를 deepcopy하고 같은 `rewrite_claims`를 호출합니다. [read.py:528](/home/laptop/projects/patent-docent/engine/stages/read.py:528)
- 최종 조립의 `claims.applicant_interest[].material_id`는 실제로 달라질 수 있습니다. 직접 조립 결과는 `CLAIMS_OBJECT_EQUAL False`였습니다.
- 그러나 convergence 6축은 독립항·종속항·element 문언·트리·종속 서명·addition 부착만 사용하며 applicant-interest, items, figures를 판정에 사용하지 않습니다. [convergence.py:104](/home/laptop/projects/patent-docent/reader/lib/convergence.py:104)

직접 조립 대조의 마지막 출력:

> `CONVERGENCE pass [('independent-count', 'pass'), ('element-set', 'pass'), ('tree-edges', 'pass'), ('dependent-count', 'pass'), ('dependent-set', 'pass'), ('addition-attachment', 'measured')]`

따라서 유효한 레인 페이로드만으로 “조기 통과 후 출구 convergence만 실패”시키는 형태는 없습니다. T-1의 검사층 finding 주입은 올바른 시험 형태이고, `engine.stages.read.run_read_checks`는 실제 출구 호출점 :1743이 참조하는 전역입니다.

새 루프에서는 부분집합 검사가 서명 비교보다 앞이므로 convergence가 든 첫 실패에서 바로 나가며 `repeated_signature`가 설정되지 않습니다. `repeated ∧ convergence` 2,048칸의 도달 불능 표지는 맞습니다.

## E. 자기 신고 ①~⑯

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | input-digest의 표 밖 값은 T29 승인 |
| ③ | 맞다 | 키 이름은 위임됐고 test_bound가 실물과 맞음 |
| ④ | 맞다 | v4 T-11 ⑤가 두 terminal 어휘 집합을 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 틀렸다 | 형태 규율이라는 분류는 맞지만, gate-escalation 런타임이 `terminal_action`을 우회함(W-2) |
| ⑦ | 맞다 | 미지 id는 무효 선언의 fail-closed 처분이며 공식 12-id 값은 불변 |
| ⑧ | 맞다 | `action: halt`는 T29 §3③의 명시값 |
| ⑨ | 맞다 | 진입 가드가 early·exit `checks`를 실제 읽으므로 `runner_reads`가 정직해짐 |
| ⑩ | 맞다 | 패치 대상·finding 추가 방식 모두 실물과 맞음 |
| ⑪ | 맞다 | T28이 요구한 술어에만 도달 불능 표지를 둠 |
| ⑫ | 맞다 | T32는 T31 소라운드에 합칠 수 있음 |
| ⑬ | 맞다 | 판정점·검사 우주 고정은 무효 계약 형식의 fail-closed 처리 |
| ⑭ | 맞다 | 6검사와 `-I`는 기준 트리 provenance를 충분히 확인 |
| ⑮ | 맞다 | B-0 분리는 골든을 B보다 앞에 세우는 운영 선택 |
| ⑯ | 맞다 | R9 등식은 이미 존재하는 정본 국면을 기계 대조하는 것 |

새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 설명 |
|---|---|---|
| G1 | covered | failure 행의 checks 유일성, kind 사전, xor |
| G2 | partially | 양방향 집합은 맞지만 선언 배열의 중복을 잃음(W-3) |
| G3 | partially | 두 계약면의 내부 등식은 정확하나 승인된 8종의 독립 기준이 없음(W-1) |
| G4 | covered | 유령 phase·거짓 early·exit 누락을 거부 |
| G5 | covered | entry 표지·halt·points 부재·retry 목록 배제를 검사 |
| G6 | covered as gate | 세 terminal 형태를 거부. 런타임 호출자 우회는 W-2 |

필수 심기는 모두 들어 있습니다.

- 행 없는 검사: ⑴
- 검사 없는 행 및 `read.__ghost__`: ⑵
- 재시도 목록↔행 불일치: ⑶·⑷
- 출구 전용 행의 거짓 `points: [early]`: ⑽

하지만 다음 두 변조가 통과합니다.

- exit 목록과 retry 행을 함께 바꿔 `read.value-derivation` 재시도를 제거하는 변조: G1~G6, T-12, 골든 모두 통과(W-1).
- 동일한 `read.schema` 출구 선언을 한 번 더 붙이는 변조: G2/G4/T-12 통과(W-3).

따라서 관문 설계는 FAIL입니다.

## G. M3 결정 공백

다음은 M3가 그대로 구현할 때 충돌하거나 임의로 보완해야 하는 자리입니다.

- R6는 런타임 전건 fail-closed를 말하지만 gate-escalation 분기는 `action` 직접 사용을 지시합니다. M3가 어느 문장을 우선할지 골라야 합니다(W-2).
- “출구 12개 정확히”와 G2/T-12의 set 대조 사이에서 선언 중복을 거부할지 정해져 있지 않습니다(W-3).
- SPEC 자기시험 계수가 18과 20으로 충돌합니다(W-4).
- 승인된 exit 8종을 관문 안에 독립 상수로 둘지, 계약 내부 등식만 검사할지 정하지 않으면 수락 체계가 W-1 변조를 허용합니다.

모두 공학 설계 보완 사항이며 새 재정은 필요하지 않습니다.

## 검증 경로

- 초기 기준 확인  
  `git status --short && git rev-parse --short HEAD && git rev-parse HEAD^{tree}`  
  초기 마지막 출력: `0cf666a351c95e5685bf4eb09a4e47c96c2caaff`

- 기준 트리 무변경  
  `git diff --name-only 99fad78 663c77e -- engine contracts reader | wc -l`  
  마지막 출력: `0`

- HEAD 전수 호출 + v4 모형 전수 대조  
  `.venv/bin/python -c '<mask 1..4095 × repeated 0/1>'`  
  출력:
  - `COUNTS [(('StageError',), 3), (('escalate', '국면 간 변이 재현 — 코드 결함 의심'), 1020), (('escalate', None), 1023), (('halt', None), 6144)]`
  - `BETA 2048 ...`
  - 마지막 출력: `MISMATCHES 0 []`

- R8/R9 정본 대조  
  마지막 출력: `R8_R9_VIOLATIONS []`

- retry 레인 계획 직접 생성  
  마지막 출력: `RETRY_LANE_ROWS 3 ('ground-independent', 'read-a/ground-independent/retry-1/batch-0') ('ground-dependent', 'read-a/ground-dependent/retry-1/batch-0') ('synthesize', 'read-a/synthesize/retry-1/batch-0')`

- monkeypatch 전역 도달성  
  출력: `M2_PATCH_REACHES False`, `READ_STAGE_PATCH_REACHES True`  
  마지막 출력: `PATCH_VERIFICATION_DONE True`

- `python -I` provenance 경로 모형  
  마지막 출력: `PROVENANCE_PATHS_OK True`

- 조기·최종 조립 convergence 대조  
  마지막 출력: `CONVERGENCE pass ...`

- W-1 변조 모형  
  출력: `MUTANT_G1_G6 (True, True, True, True, True, True)`  
  마지막 출력: `MUTANT_ACCEPTED True REMOVED_RETRY read.value-derivation`

- W-3 중복 선언 모형  
  출력: `DUPLICATE_DECL count 13 unique 12 R9 True T12_SET_BRIDGE True`  
  마지막 출력: `DUPLICATE_MUTANT_ACCEPTED_BY_SPECIFIED_DECLARATION_CHECKS True`

- 종료 상태  
  도중 총괄이 문서 전용 커밋 `4e1f05c`를 반입했습니다.  
  `git diff --name-only 663c77e HEAD -- engine contracts reader tests tools | wc -l`  
  마지막 출력: `0`; 작업 트리 clean.

## [미검증]

- `generate.py`, manifest, `check_failure_table.py`, `test_m24_failure_grid_golden.py`는 아직 없어 실제 실행하지 못했습니다.
- read-only 규율 때문에 detached worktree 생성·manifest 기록·전체 pytest·관문 실행은 하지 않았습니다.
- T-1/T-2 전체 러너 통주는 파일을 만드는 하네스라 실행하지 않았습니다. 패치 도달성, CheckRow 동작, 레인 계획 수는 메모리에서 따로 검증했습니다.
- 도전 중 외부 총괄이 문서 커밋을 반입했으나 코드 영역은 `663c77e`와 diff 0입니다.