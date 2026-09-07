# 독립 감수 원문 — M1b 설계 도전 33차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v35(자원 단위 역할 · 32차 OD-1~5 반영) · 판정 REVISE(HIGH 1 · MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `dd0a085d3496ae0545aebcad0603ee6e0a802b242ca0817186c0a6896f6fbf6a` · 19567 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v33/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · Monitor(14:43 기동 · 15:1x 종료 · USAGE 는 레인 STATUS). 사본 재핀 `a1d5e2a` · 메모 v35 `e7fe570f887335bc` · 대장 `370231f780ae14ae` · `t40_resources.py` `11d6a18a55fb1972` · 회귀표 v14(151) · bundle 70. 이번 기동 = T44 자동(32차 조건 충족) · **T45 ③ 문턱 판**.

**판정 = REVISE · 5건(HIGH 1 · MED 4) · 기각 0 · 발주자 귀책(저작 astra xhigh 4차 · 발주·검수 총괄).** 지문 15 일치 · 정적 0/0/0 · 심사 ① 충족 · ②~⑤ 미충족 · 갈래 ⑴ 5 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0. **진행도(행 단위) = `mismatch=9 unmet=9 unreviewed=0` — 31차 12 → 32차 12 → 33차 9 · 감소 → T45 ③ 두 회차 연속 비감소 조건 불성립 → 상신 없음 · T44 자동 기동.** 32차 12행 중 7 충족(SITE-03·08·21·22·30·33·36) · 5 잔여(23·27·40·55·56) · 새 4(09·42·50·51). A 폐쇄표 closed 120 · partially 6(NZ-3 · OA-3 · OC-2 · OC-3 · OD-2 · OD-3) · open 0 · OD-1·4·5 closed. 게이트 총평: 「자원 단위 역할은 자료·법 예외 분기를 상당 부분 바로잡았다. 남은 것 = **외부 함수가 오류를 성공 값으로 바꾸는 경로 · 메타 조회가 오류를 부재로 바꾸는 경로 · 기록된 내부 IO 를 소비기가 제외하는 경로**」. **OE-1 HIGH · P5 · SITE-55·56**: `read_output_boundary` 가 런 내부는 전량 검사하지만 러너가 마지막에 append 하는 **주 작업 트리 원장 `ledgers/shadow/screening.jsonl`** 은 검사하지 않음 — 그 파일이 밖을 가리키는 링크면 원장 밖 append(`_opened` 는 어휘 절대 경로만 역할표 대조). **OE-2 MED · P1·P7·T1 · SITE-23**: 기준 법 절차 집합 `os.listdir(pdir) if os.path.isdir(pdir) else []` — `isdir` 가 PermissionError 를 삼켜 빈 집합 → 「기준 절차와 다르다」 부적격(검수 불능이어야). **OE-3 MED · P2·P7 · SITE-27·40·42·55**: 러너 안 `shadow_ledger_root → worktree_of → gitpin.git_out` 의 git 실패를 러너가 `GitUnavailable` 로 포착해 `(repo, "git-unavailable")` 정상 반환 — `external_scope()` 는 파일·JSON·YAML 경계만 관측하고 외부 함수 내부 git 은 봉투를 안 지남 · 예외가 밖으로 안 나와 `origin()` 기회 없음 · **S29 guard-env 는 실제 git 실패가 아니라 함수 통째 교체**. **OE-4 MED · P6·P7 · SITE-09**: 러너가 내부 포착 IO 를 `return` outcome 에 기록하게 됐지만(4차) 원본 선판별 `is_io_fault` 는 `kind ∈ {exception, pending}` 만 · `_halt4_bound` 는 4행만 → `check_lane_log_digest_value` 의 `request.md` OSError 포착(13행 반환)은 T43 선판별에서 탈락. **OE-5 MED · P7·T3 · SITE-50·51**: 구동기 `pending_coords()` 의 `os.walk` 에 `onerror` 없음 → scandir 실패가 「대기 0건」 → `cmd_dispatch` 가 빈 배치·counter 기록.

**총괄 진단**: 셋 중 둘(OE-3 · OE-4)이 **핀 커밋의 러너(법) 내부 동작**에서 난다 — 러너가 git 실패를 대체 경로로 삼키고, 내부 포착 IO 를 13행 반환에 싣는다. 검수원은 법을 고칠 수 없다(T1 · 법 = 커밋 트리). 따라서 v36 은 ⓐ 러너 호출 **전** 환경 선검증(같은 경로에서 git 조회 성공 확인 · 원장 루트 해석 결과가 `git-unavailable` 아닌지) ⓑ 러너 호출 **후** 산출물에서 대체 경로 표식(`POINTER_ROOT_SOURCE git-unavailable` 등) 검출 → 검수 불능 ⓒ 선판별을 「영수증 outcome 에 io_fault/io_caught 가 참이면 행 수와 무관」으로 — 러너를 고치지 않고 밖에서 닫는다. 저작자가 「법 변경 없이는 못 닫는다」고 판단하는 항목이 있으면 `[총괄 확인]` 으로 남기고 법은 건드리지 않는다(그 경우 = 새 보증·범위 재정 후보 → Owner).

**처분 = 전부 수용(공학) · 이행 = v36 저작(astra xhigh 5차 · T44 자동).** 수정 문안(도전자 원문) — OE-1 「read 의 첫 러너 부작용 전에 생산 원장 말단과 기존 조상도 공용 출력 경계로 검사하고, 허용 자리 밖으로 해석되는 링크는 무쓰기 거부한다」 · OE-2 「절차 디렉터리의 메타 조회 실패를 부재·빈 집합으로 접지 않고 법 자원 실패로 전파한 뒤, 열거 성공 값만 핀과 비교한다」 · OE-3 「선언된 외부 함수 내부의 git 조회 실패도 대체 경로 반환 전에 관측·전파하여, 검수 및 sandbox 에서는 성공 값 비교보다 먼저 검수 불능으로 종료한다」 · OE-4 「결속·정합 검사를 마친 원본 영수증의 실제 내부 포착 IO 도 반환 행 수와 무관하게 T43 선판별에 포함하고, sandbox IO 와 구분해 재실측으로 종료한다」 · OE-5 「pending 좌표 열거의 메타·scandir 실패를 전파하고, 열거가 전량 성공하기 전에는 완료 표시나 발주 기록을 만들지 않으며 실패는 구동 중단으로 처분한다」. 발주자 오류 누계 207 → **212**.

지적 열거 = OE-1, OE-2, OE-3, OE-4, OE-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 33회)

**지적 5건 — HIGH 1 · MED 4 · 갈래 ⑴ 5 · 도출 누락 0 · 새 보증 요구 0 · 대장 누락 반례 0.**

마커의 path·pin·order가 발주와 일치하고, HEAD는 `a1d5e2a95ed5da681f74e57968ae8c493d323dd4`다. 메모·대장·스크립트·회귀표 등 지정된 **15개 sha16도 전부 일치**한다.

자원 단위 역할은 OD의 자료·법 예외 분기를 상당 부분 바로잡았다. 그러나 **외부 함수가 오류를 성공 값으로 바꾸는 경로**, **메타 조회가 오류를 부재로 바꾸는 경로**, **기록된 내부 IO를 소비기가 제외하는 경로**는 남았다. 역할표와 선언표의 일치만으로 이 경로들이 닫히지는 않는다.

**OE-1 — HIGH · ⑴ P5 집행 위반 · SITE-55·56**

좌표: 메모 §5′.3·§5′.5 P5·§5′.11, [t40_drive.py:325](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:325)의 `read_output_boundary`·`run_engine`·`cmd_read`, `t40_resources.py:_opened`, [read.py:1046](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1046)의 `append_screening_ledger`.

`read_output_boundary()`는 런 내부를 전량 검사하지만, 러너가 마지막에 append하는 **주 작업 트리의 `ledgers/shadow/screening.jsonl`**은 검사하지 않는다. 이 파일이 호출 전에 허용 자리 밖의 파일을 가리키는 링크여도 런 경계 검사는 통과한다.

`shadow_screening_ledger()`는 원장 경로를 조립해 반환하고, 실제 append는 그 경로를 그대로 연다. 새 `_opened()` 역시 어휘상 절대 경로를 역할표와 대조하므로, 등록된 `main/ledgers` 아래라는 사실만으로 외부 대상을 향한 열기를 허용한다. 동시 교체나 hardlink가 필요하지 않다.

실제 경계 함수와 실제 원장 append를 메모리 파일시스템으로 연결한 관측:

```text
LEDGER_ALIAS boundary=passed append_calls=1 resolved_outside=True memory_bytes=160
LEDGER_ALIAS_PROBE_DONE actual_writes=0
```

**잘못된 부작용:** 승인된 생산 원장 밖으로 append한다. 사후 지문 비교나 최종 거부로 이미 발생한 쓰기를 되돌릴 수 없다.

S27은 런 내부 여섯 경로를 시험한다. SITE-55·56에 명시된 **주 작업 트리 원장**의 이 오류 경로는 덮지 않는다. 기존 OD-1의 `10-read` 반례는 닫혔지만 두 행의 출력 의무는 아직 미충족이다.

**수정 문안:** “read의 첫 러너 부작용 전에 생산 원장 말단과 기존 조상도 공용 출력 경계로 검사하고, 허용 자리 밖으로 해석되는 링크는 무쓰기 거부한다.”

**OE-2 — MED · ⑴ P1·P7 집행 위반, T1 확인 경로 미충족 · SITE-23**

좌표: 메모 §5′.4·§5′.11, [t40_metrics.py:386](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:386)의 `metrics` 기준 법 절차 대조.

기준 법의 절차 집합은 다음 식으로 만든다.

```python
os.listdir(pdir) if os.path.isdir(pdir) else []
```

`os.path.isdir()`가 `PermissionError`를 삼키면 빈 집합이 된다. 그다음은 조회 실패 처분이 아니라 **“기준 절차와 다르다”는 유효 값 비교의 부적격 분기**다. `R.walk_error`까지 도달하지 않는다.

정상 기준 런을 실제 `metrics(..., baseline=True)`로 재현한 메모리 법에서, `reader/procedure`의 `stat`에만 경로가 있는 `PermissionError(13, …)`를 주입했다.

```text
[t40_metrics] 처분=부적격 · --law-tree 의 reader/procedure 가 기준 런 생성 판(d4e6ca2)과 다르다(NS-6): 차이 [...]
PROCEDURE_STAT exit=4 actual_writes=0
```

**잘못된 처분:** 읽을 수 없는 법을 자료 불일치로 보고한다. 요구 처분은 `검수 불능`이며, 자료를 결과 표에 부적격으로 싣는 경로와 다르다.

S28은 `engine/stages`의 실제 `scandir` 실패를 시험한다. 별도 절차 핀 검사에 있는 이 메타 조회는 시험하지 않는다.

**수정 문안:** “절차 디렉터리의 메타 조회 실패를 부재·빈 집합으로 접지 않고 법 자원 실패로 전파한 뒤, 열거 성공 값만 핀과 비교한다.”

**OE-3 — MED · ⑴ P2·P7 집행 위반 · SITE-27·40·42·55**

좌표: 메모 §5′.4 외부 선언·결과 봉투, [t40_resources.py:159](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_resources.py:159)의 `external_scope`, `t40_metrics.py:metrics` 477·490행, `t40_replay.py:replay` 241·320행, `t40_drive.py:run_engine`, [engine/paths.py:202](/home/laptop/projects/workspaces/pd-m1b-t40/engine/paths.py:202).

실제 외부 함수의 다음 경로가 남았다.

```text
shadow_screening_ledger
→ shadow_ledger_root
→ worktree_of / engine.gitpin.git_out
→ git 조회 rc≠0
→ GitUnavailable
→ shadow_ledger_root가 포착
→ (repo, "git-unavailable") 정상 반환
```

`EXTERNAL_RESOURCES`에는 git이 환경으로 선언돼 있다. 하지만 `external_scope()`는 파일·JSON·YAML 경계만 관측한다. 외부 함수 내부의 git 결과는 새 `R.process`·`git_value` 봉투를 통과하지 않는다. 예외도 함수 밖으로 나오지 않아 `origin()`이 판정할 기회가 없다.

실제 외부 함수의 하위 git 결과만 실패로 대체한 관측:

```text
EXTERNAL_GIT_FAILURE returned=…/.worktrees/gdm-x-y/ledgers/shadow/screening.jsonl subprocess_calls=1 io_events=0
```

실제 러너의 후반 경로에서도 확인했다.

```text
CAUGHT_DIGEST {"kind":"return","status":"ok","reason_label":null,"rows":13}
RUNNER_INTERNAL_GIT injected=2 io_fault=None io_events=0
POINTER_ROOT_SOURCE git-unavailable
RUNNER_INTERNAL_GIT_PROBE_DONE actual_writes=0 virtual_writes=13
```

기준 런 검수에서는 같은 내부 조회 실패를 주입해도 `complete·163·56`이 반환됐다. 링크된 실측 구조에서는 대체 원장이 worktree 안으로 바뀌며, sandbox에서만 발생하면 오류 표시 없는 반환값이 outcome 비교를 통과하고 이후 원장·포인터 산출물 차이가 `mismatch`로 처리되는 코드 경로다.

**잘못된 처분:** 환경 조회 실패가 사라지거나 자료 불일치가 된다. SITE-42의 근거인 “`shadow_screening_ledger` 실패→infeasible”도 실제 함수의 포착·대체 반환에는 성립하지 않는다.

특히 **S29 `guard-env`는 실제 git 실패를 주입하지 않는다.** `shadow_screening_ledger` 전체를 `PermissionError`를 던지는 함수로 교체한다. S32도 검수 스크립트의 직접 git 조회를 시험하며 이 내부 경로를 덮지 않는다.

**수정 문안:** “선언된 외부 함수 내부의 git 조회 실패도 대체 경로 반환 전에 관측·전파하여, 검수 및 sandbox에서는 성공 값 비교보다 먼저 검수 불능으로 종료한다.”

**OE-4 — MED · ⑴ P6·P7 집행 위반 · SITE-09**

좌표: 메모 §2·§5′.4·§5′.8, [t40_receipts.py:504](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:504)의 `is_io_fault`, `t40_replay.py:_halt4_bound` 119행·`replay` 229행, `t40_metrics.py:metrics` 431행.

새 러너는 내부에서 포착된 IO도 `return` outcome에 기록한다. 그런데 원본 실측의 선판별은 다음 두 경우만 받는다.

- `is_io_fault`: `kind ∈ {exception, pending}`인 경우.
- `_halt4_bound`: 출구 원천 재독 실패 서명과 `rows=4`인 경우.

실제 `check_lane_log_digest_value()`는 `request.md` 읽기의 `OSError`를 포착해 실패 행으로 만든다. 이 경로는 **13행 반환**이므로 둘 다 빠진다.

실제 검사·러너·직렬화를 메모리에서 연결하고 해당 파일 읽기에만 오류를 주입했다.

```text
CAUGHT_DIGEST {"kind":"return","status":"escalate","reason_label":null,"rows":13,"io_fault":true,"io_caught":true}
IO_CHECK 6 events 6 is_io_fault False
T43_INPUT receipt_io=False halt_bound=None
CAUGHT_DIGEST_PROBE_DONE actual_writes=0 virtual_writes=8
```

완주 판정서의 raw 지문을 해당 receipt post에 결속해도 `rows=13`이라 선판별되지 않는다.

**잘못된 처분·순서:** 구동기가 기록한 실측 IO가 있는데 재실측으로 종료하지 않고 후속 검수·재조립으로 진행할 수 있다. [T43 §1 ①](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/ruling-T43.md:17)의 “호출 영수증에 IO 예외가 있거나”라는 조건을 4행 서명으로 제한할 근거가 없다.

S33은 **sandbox의 4행 반환**을 시험한다. F 7도 이 원본 13행 내부 포착 경로를 덮지 않는다. J43의 봉투 선택을 재개방하는 지적이 아니라, 새로 보존한 실제 IO 기록이 P6 집행에서 탈락하는 반례다.

**수정 문안:** “결속·정합 검사를 마친 원본 영수증의 실제 내부 포착 IO도 반환 행 수와 무관하게 T43 선판별에 포함하고, sandbox IO와 구분해 재실측으로 종료한다.”

**OE-5 — MED · ⑴ P7·T3 집행 위반 · SITE-50·51**

좌표: 메모 §2·§5′.3·§5′.4·§5′.11, [t40_drive.py:154](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:154)의 `pending_coords`·`cmd_lanes`·`cmd_dispatch`.

`pending_coords()`는 `os.walk(root)`에 `onerror`를 전달하지 않는다. 실제 `scandir`가 권한 오류를 내면 빈 목록 또는 부분 목록을 정상 반환한다. `cmd_lanes()`는 이를 완료 조회처럼 보고하고, `cmd_dispatch()`는 그 목록으로 기록 단계에 들어간다.

실제 `os.walk` 내부의 `scandir`만 실패시킨 관측:

```text
PENDING_SCAN returned=[] scandir_calls=1
PENDING=0
LANES_SCAN exit=0
```

같은 실패를 실제 `cmd_dispatch()`에 연결하고 쓰기만 메모리로 대체했다.

```text
DISPATCH=0 -> …/lanes-r0-batch.json
DISPATCH_SCAN exit=0 virtual_files=2
DISPATCH_SCAN_PROBE_DONE actual_writes=0
```

**잘못된 처분·부작용:** 조회 불능을 “대기 0건”으로 표시하며, counter·빈 배치 파일까지 성공 기록한다. 하위 일부 디렉터리만 실패하면 불완전한 목록으로 발주를 확정한다.

SITE-50의 “쓰기 호출 없음”은 조회 완전성의 증거가 아니다. S17은 `t40_receipts.requests_present()`를 보강했으며, 구동기의 별도 열거 함수는 덮지 않는다.

**수정 문안:** “pending 좌표 열거의 메타·scandir 실패를 전파하고, 열거가 전량 성공하기 전에는 완료 표시나 발주 기록을 만들지 않으며 실패는 구동 중단으로 처분한다.”

**남은 자리와 진행도**

63행의 담당 함수·자원·오류 경로·선후 및 근거를 대조했다. **미심사 행은 없다.** 미충족 행은 다음 9개다.

```text
SITE-09 SITE-23 SITE-27 SITE-40 SITE-42
SITE-50 SITE-51 SITE-55 SITE-56
```

| 구분 | 행 |
|---|---|
| 32차 미충족 12행 중 이번에 충족 | SITE-03·08·21·22·30·33·36 |
| 32차에서 잔여 | SITE-23·27·40·55·56 |
| 다른 51행에서 이번 반례 확인 | SITE-09·42·50·51 |
| 미심사 | 없음 |

```text
mismatch=9 unmet=9 unreviewed=0
```

같은 행에 복수 반례가 있어도 한 번만 셌다. 공용 역할 기제의 selector를 각 소비 행과 중복 계수하지 않았다.

정적 결과 `0/0/0`과의 차이는 **selector 존재 여부가 아니라 배정된 오류·부작용 경로의 미집행**이다. 역방향에서 확인한 외부 원장 효과·내부 git·러너 내부 IO도 기존 행의 자원과 오류 범위에 포함되므로 “대장 누락”으로 중복 제출하지 않는다.

31차 `12/12/0` → 32차 `12/12/0` → 이번 **`9/9/0`**이다. 이번에는 감소했으므로 T45 ③의 **두 회차 연속 비감소 상신 조건은 성립하지 않는다.** 도출 누락 0·새 보증 요구 0·갈래 ⑴만이라는 T44 자동 기동 조건은 충족한다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 충족 | 고정 범위에서 상류 의무의 미배정 반례 없음. 수용된 설계 선택 자체를 재개방하지 않음 |
| ② 신뢰·입력·부작용 경계 | 미충족 | 원장 출력 경계, 법 조회 실패, 불완전한 좌표 열거 — OE-1·2·5 |
| ③ 기제의 집행과 합성 | 미충족 | 외부 함수의 실패 소실, 기록 생산→T43 소비 단절 — OE-3·4 |
| ④ 검증 근거 | 미충족 | S27~33 및 L01의 주입·검증 경로가 해당 잔여 의무를 덮지 않음 |
| ⑤ 미충족 상태의 처분 | 미충족 | 검수 불능→부적격/성공, 실측 IO→선판별 누락 — OE-2~5 |

**A 폐쇄표**

`closed`는 **해당 과거 반례의 폐쇄**다. 같은 SITE에 이번 다른 반례가 없다는 뜻은 아니다.

| 지적 | 상태 | 대조 근거·잔여 |
|---|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed | 선등록·계수·발췌·발주 통제의 기존 연결 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed | 오류 종료·원장·결측·식별 결속 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed | 요청·응답·원천 지문과 스키마·검사 재실행 연결 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed | 검사 집합·행 형태·소비 적격성·상태 연결 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed | 기존 종결·재시도·법·렌더 대조 유지. 새 오류 경로는 OE로 분리 |
| NU-1~4·NV-1~3 | closed | 비대칭 재시도·접지 그룹·첫 관측 결속 유지 |
| NW-1~5·NX-1~4·NY-1~4 | closed | 기존 정규화·권한·경로·IO 기록 반례의 폐쇄 유지 |
| NZ-1·2·4·5 | closed | 무잠금 조회, 결속 뒤 선판별, 봉인·시도·보존 연결 유지 |
| NZ-3 | partially | 처분 전달 잔여 OE-2·3·5 |
| OA-1·2·4·5 | closed | 영수증 결속·런 보존·공통 봉인 집합·캐시 억제 유지 |
| OA-3 | partially | 외부·메타 오류가 처분 경계 전에 사라짐 — OE-2·3 |
| OB-1 | closed | SITE-02·03 — 공용 `bind_receipts` 뒤 선판별, C93·C86~89 |
| OB-2 | closed | SITE-01·04~06 — 공통 집합·후보 선검사, C94·S09·S11 |
| OB-3 | closed | SITE-07~10 — 원래 네 자료/법 반례, C95~97·S12 |
| OB-4 | closed | SITE-11 — evidence 전체 보호·겹침 검사 선행, S13 |
| OC-1 | closed | SITE-52·60·63 — counter·sidecar·목적지 전건 선검사, S21·S22 |
| OC-2 | partially | S23 지정 경로는 폐쇄. SITE-27의 실제 내부 git 잔여 — OE-3 |
| OC-3 | partially | SITE-40의 rc·JSON·외부 IO 및 내부 4행 IO는 폐쇄, S24·S33. 내부 git 실패 소실은 OE-3 |
| OC-4 | closed | SITE-44 — 요청 열거 stat·scandir 양 역할, 확장 S17 |
| OC-5 | closed | SITE-15·57·63 — 준비 검사 뒤 봉인·실패 분류, S25·S26 |
| OD-1 | closed | SITE-55·56 — 기존 런 내부 링크 반례, S27. 별도 원장 출력은 OE-1 |
| OD-2 | partially | SITE-08·30·33의 자료 형태·반대 역할은 폐쇄, S29~31. SITE-27의 실제 환경 분기 잔여 — OE-3 |
| OD-3 | partially | SITE-03·22의 법 walk 실패는 폐쇄, S28. SITE-23의 절차 메타 조회 잔여 — OE-2 |
| OD-4 | closed | SITE-08·21·36 — 직접 git 조회 봉투 선판정, S32 |
| OD-5 | closed | SITE-40 — sandbox 내부 포착 원천 IO·UnicodeDecodeError, S33 |

MY~OD 합계 **closed 120 · partially 6 · open 0**. 요청한 NZ-3·OA-3·OC-2·OC-3의 잔여는 자원 단위 역할 도입 뒤에도 전부 닫히지 않았다.

**검증 경로**

모든 Python 실행은 사본 cwd에서 다음 인터프리터로 수행했다.

```text
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B
```

| 명령·호출 경로 | 관측·마지막 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 마커 일치 · 마지막 줄 `a1d5e2a95ed5da681f74e57968ae8c493d323dd4` |
| 지정 15파일 SHA-256 계산 | 발주 sha16 전부 일치 |
| `bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `rows=63 extracted=1544` → **`mismatch=0 unmet=0 unreviewed=0`** |
| `t40_sites.markdown(ledger)`와 메모 대조 | `SUMMARY_VIEW_EQUAL True` |
| `git log`·`git ls-tree` | base 부모 `6d92cad`, R1·R2 부모 base; 절차 tree `d7717eb8750115a49e81ec7803790093b98c40ec` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만 변경 · 마지막 행 `0 139 reader/procedure/HISTORY.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 출력 없음 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 마지막 줄 `2 2 contracts/stages/read.yaml` |
| 세 브랜치 계약 `git show` → 실제 `lane_profiles()` | 네 좌석이 각각 `registry()`와 일치 · `PROFILE_BLOBS_DONE actual_writes=0` |
| `bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 4 · `처분=부적격 · 기준 런은 --law-tree … 필수다` |
| base 법 62파일 `git show` → 메모리 법 → 실제 기준 `metrics()` | `MEMORY_BASELINE_DONE writes=0 law_files=62` |
| `t40_excerpts` import → 실제 `ex1/ex2`, 출력은 StringIO | `EXCERPTS_DONE actual_writes=0 documents=2` |
| `CASES()` 정의와 제출 회귀표 대조 | 151개·ID 동일·L13/F7/C95/X2/S34·표의 FAIL 0 |
| OE 메모리 주입 | 각 지적의 관측 블록. 실제 파일 쓰기 0 |

기준 런은 **complete·명세 163·component 56**으로 재현했다. 명세 종류별 계수는 component 56·grounding 56·fact 14·implication 20·positioning 7·figure_note 10, synth 계수는 fact 3·implication 20·positioning 7·figure_note 10이다.

발췌는 기준 자료를 R0/R1/R2 입력 대역으로 사용해 **27단위**, 종속항 표본 **CL-2·4·7·9·12·14·16·19·21·24**, 판정 불가 기계 표시 0을 재현했다. 실제 R0/R1의 내용 품질 판정은 아니다.

**[미검증]**

151개 디스크 회귀는 재실행하지 않았다. 사례 정의·주입 위치·검사 조건과 제출 표를 대조했으며, 표의 PASS를 이번 독립 실행 결과로 취급하지 않았다. 실측 CLI, 실제 sandbox 생성·삭제, 쓰기 명령, Workflow·레인 실호출도 실행하지 않았다.

OE-1은 실제 출력 경계와 append의 합성 시험이다. OE-3·4의 러너 시험은 기존 기준 자료로 후반 경로에 도달하도록 종결 가드·진입 지문 검사·계속 봉투 판정을 대역화했고, 실제 검사·반환 직렬화와 쓰기 의도를 메모리에서 관측했다. 전체 실측이나 디스크 재조립의 완료를 주장하지 않는다.

파일 생성·수정은 없었다. 정본 리포는 읽지 않았으며 허용된 Python 인터프리터만 사용했다.

**읽은 파일**

- 원장·선행 심사: T40 §§1·4·5, `bundle/ruling-T42.md`, `bundle/ruling-T43.md`, T44·T45·T46, D-02 §17 추기 38~49, `ADVICE-REPLY-4.md`, 31·32차 원문 및 28~30차 관련 지적·폐쇄표.
- 설계·대장: v35 지정 절, `T40-SITES-LEDGER.json` 63행·selector·역할 선언, `T40-DESIGN-JUDGMENTS.md`, 스크립트 지문표·회귀표.
- 구현·근거: `t40_resources.py`, `t40_drive.py`, `t40_replay.py`, `t40_receipts.py`, `t40_metrics.py`, `t40_sites.py`, `t40_regress.py` 관련 사례·주입 코드, `t40_regress_r4.py`, 발췌·봉투·Workflow.
- 계약·실물: SPEC §8.4 G-1~3·G-12, run-kinds·read 계약·approval-envelope 스키마, `engine/stages/read.py`, `engine/paths.py`, `engine/gitpin.py`, 레인 contract·file_adapter·plan, convergence·run_checks 및 호출되는 규칙·검증 코드, 기준 런 산출물과 메모리 법으로 읽은 핀 파일.