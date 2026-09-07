# 독립 감수 원문 — M1b 설계 도전 32차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v34(31차 OC-1~5 반영) · 판정 REVISE(HIGH 1 · MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `7483076e141d8602e368aca024f890764e3c802221ddfda19b9d1dd0e7a8935a` · 20506 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v32/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③ · 저작 좌석 astra xhigh 와 같은 모델 · Owner 인지) · `setsid nohup` · Monitor(13:13 기동 · 13:4x 종료 · USAGE 는 레인 STATUS). 사본 `pd-m1b-t40` 재핀 detached `81bf994` · 메모 v34 `9ce2ba52a620d2a1` · 대장 `8b2e0629ea3e2c66` · 회귀표 v13(143) · bundle 67. **이번 기동 = 재정 T44 자동 기동**(31차 조건 충족) · 판정 방법 = T45 ② + 진행도 비교 의무(31차 기준선 12/12/0).

**판정 = REVISE · 5건(HIGH 1 · MED 4) · 기각 0 · 발주자 귀책(저작 astra xhigh 3차 · 발주·검수 총괄).** 지문 13 일치 · 정적 0/0/0 · 심사 ① 충족 · ②~⑤ 미충족 · 갈래 ⑴ 5 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0. **진행도(행 단위) = `mismatch=12 unmet=12 unreviewed=0` — 31차 12/12/0 대비 비감소**(31차 12행 중 7 폐쇄 · 5 잔여 + 새 불일치 7 = 12 · SITE-03·08·21·22·23·27·30·33·36·40·55·56). A 폐쇄표 closed 117 · partially 4(NZ-3 · OA-3 · **OC-2 · OC-3**) · open 0 · OC-1·4·5 closed. **OD-1 HIGH · P5 · SITE-55·56**: 구동기 `cmd_read` 의 출력 검사가 런 루트까지라 호출 전 존재하는 `runs/<id>/10-read` 링크를 안 보고, 러너 `ensure_read_dirs` 가 `claim-trees`·`lanes` 를 링크 대상(밖)에 만든다(메모리 관측 `outside_mkdir_intents=[…/claim-trees, …/lanes]` · 어댑터 `write_request` 까지 3 목적지). **OD-2 MED · P7 · SITE-27·30·33**: OC-2 가 법 적재 실패를 검수 불능으로 묶으면서 **법 함수가 처리하는 자료의 실패까지** 검수 불능이 됨(완주 판정서 JSON 손상 · `request.json#response_schema={}` · `#slices=1` · `material-spec.json#patent=1` → 전부 `처분=검수 불능` · 부적격이어야). **OD-3 MED · T1·P7 · SITE-03·22·23**: 법 파일 수집 `law_files`·`law_tree_files` 의 `os.walk` 에 `onerror` 없음 → 디렉터리 열거 실패가 「법 파일 일부 빠진 정상 반환」 → 지문 불일치 = 부적격(법 판독 불능이 법 불일치로 변환). **OD-4 MED · T1·P7 · SITE-08·21·36**: 대조기 안의 `main_root_of`·sandbox `git_head`·`main_root_of` 조회 실패(`_git` None)가 값 불일치 = `mismatch` 로(조회 불능 ≠ 불일치 · 지표기 앞단만 S23 으로 분리됨). **OD-5 MED · P6·P7 · SITE-40**: 러너가 출구 원천 재독 OSError 를 **내부에서 잡아** halt 4행으로 반환하고 `run_engine` 직렬화에 `io_fault` 가 없어 sandbox 안 IO 실패가 `mismatch` 로(S24 는 밖으로 나온 예외만 시험).

**총괄 진단(세 회차 OC→OD 의 결)**: P7 처분 분류 지적이 29·30·31·32차 네 회차 연속이다 — 형태는 매번 「자료 vs 환경(법·git·sandbox·하위 프로세스) 역할이 **호출 단위 kind 인자**로 배정돼 있어, 외부 함수(러너·렌더러·Rules·os.walk)가 그 안에서 반대 역할의 실패를 내면 뒤집힌다」. 호출 단위 kind 는 이 결손 형태를 없애지 못한다 — **자원 단위 역할**(어느 경로·어느 하위 프로세스가 자료인가 법인가를 열기 전에 정하고, 예외를 잡는 자리가 「무엇을 읽다 났나」를 예외의 발생 자원으로 판정)로 바꿔야 한다. v35 발주문에 구조 지침으로 넣는다(저작자 판단 · J 로 기록).

**T44 판정 = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 0 ✓ · ⓒ 갈래 ⑴ ✓ → 자동 기동 조건 충족.** **T45 ③ 진행도 조건 = 「세 수가 두 회차 연속 줄지 않으면 상신」 — 31→32 비감소 1회. 33차도 비감소면 상신.** Owner 에게 채팅으로 고지(재정 아님).

**처분 = 전부 수용(공학) · 이행 = v35 저작(astra xhigh 4차 · 같은 작업장).** 수정 문안(도전자 원문) — OD-1 「구동기 read 는 러너의 첫 부작용 전에 런 내부 쓰기 대상과 기존 조상을 원래 worktree 경계에 결속하여 검사하고, 링크 탈출은 무쓰기 거부한다」 · OD-2 「중첩 자료 형태를 접근 전에 검증하고, 종결 가드·요청 재구성의 자료 실패와 법 적재 실패를 분리하여 각각 부적격과 검수 불능으로 전달한다」 · OD-3 「법 디렉터리 확인과 열거는 IO 오류를 보존하고, 완전한 집합을 얻지 못하면 지문·집합 비교 전에 BindingInfeasible 또는 검수 불능으로 종료한다」 · OD-4 「대조기의 원본·sandbox 루트와 HEAD 조회는 실패를 별도로 전달하고, 성공한 값만 비교하며 조회 불능은 infeasible 로 반환한다」 · OD-5 「sandbox 러너가 내부에서 포착한 IO 실패도 하위 결과에 보존하여 outcome 비교 전에 infeasible 로 분리하고, T43 선판별은 원본 실측 기록에만 적용한다」. 발주자 오류 누계 202 → **207**.

지적 열거 = OD-1, OD-2, OD-3, OD-4, OD-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 32회)

**OD-1~5: HIGH 1 · MED 4 · 전부 갈래 ⑴.** 도출 누락 0 · 새 보증 요구 0 · ⓑ 대장 누락 반례 0이다. 다만 ⓐ 대장↔코드 연결과 ⓒ 집행·근거·처분에서 **12행이 미충족**이다. PASS 전 실측 착수 금지는 유지된다.

사본 마커의 path·pin·order와 HEAD `81bf99419b477885545ce9fdd04753f54b584d58`가 일치했다. 메모 `9ce2ba52a620d2a1`, 대장 `8b2e0629ea3e2c66` 및 발주에 열거한 스크립트·회귀표·지문표 **13개 파일의 sha16 전부 일치**했다. 지문 불일치 지적은 없다.

정본 리포는 읽지 않았고 허용된 Python 인터프리터만 사용했다. 파일 생성·수정·삭제, checkout·worktree·stash, 배경 실행은 하지 않았다. 아래 주입 시험의 출력·쓰기 목적지는 모두 메모리 대역이다.

**OD-1 — HIGH · ⑴ P5 집행 위반 · SITE-55·56**

좌표: 메모 §5′.3·§5′.5 P5·§5′.11, [t40_drive.py:395](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:395) `cmd_read`, 같은 파일 `run_engine`:335, [engine/paths.py:418](/home/laptop/projects/workspaces/pd-m1b-t40/engine/paths.py:418) `ensure_read_dirs`, [engine/stages/read.py:1681](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1681) `run`.

`cmd_read()`의 출력 검사는 **런 루트까지**다. 호출 전부터 존재하는 `runs/<run_id>/10-read` 링크는 검사하지 않는다. 이어지는 실제 러너는 `ensure_read_dirs()`에서 `claim-trees`와 `lanes`를 만들며, 이 효과는 `verify_declared_inputs()`보다 먼저 발생한다.

`10-read → /memory/protected`라는 고정된 링크 해석을 메모리에서 주입했다. 실제 `run_engine → read.run → ensure_read_dirs`를 연결하고 mkdir만 기록하자:

```text
ACTUAL_RUN_ENGINE root_boundary_pass=True
outside_mkdir_intents=['/memory/protected/claim-trees',
                      '/memory/protected/lanes']
```

실제 `FileLaneAdapter.write_request()`까지 별도로 연결한 시험에서도 외부 mkdir·`request.json`·`request.md` 쓰기 목적지 **3개**를 관측했다. 어댑터의 경계는 이미 외부로 해석된 lanes 루트를 기준으로 삼으므로 이를 되돌리지 못한다.

동시 교체·hardlink 반례가 아니다. §5′.3은 구동기의 효과를 승인된 실측 worktree의 런 산출물로 제한하고, 부적격 입력도 P5를 면제하지 않는다고 명시한다. SITE-55의 외부 러너 호출과 SITE-56의 진입 경계에 이미 배정된 자원이므로 **대장 누락이 아니라 기존 행의 집행 단절**이다.

S22는 증거 출력·sidecar와 그 조상을 시험한다. 러너가 쓰는 런 내부 자식 경로는 덮지 않는다.

- **잘못된 부작용:** 경계 거부 전에 승인된 런 밖으로 디렉터리·요청 파일을 생성할 수 있다.
- **수정 문안:** “구동기 read는 러너의 첫 부작용 전에 런 내부 쓰기 대상과 기존 조상을 원래 worktree 경계에 결속하여 검사하고, 링크 탈출은 무쓰기 거부한다.”

**OD-2 — MED · ⑴ P7 집행 위반 · SITE-27·30·33**

좌표: 메모 §5′.4·§5′.5 P7·§5′.11, [t40_metrics.py:443](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:443), [t40_metrics.py:673](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:673), [t40_metrics.py:785](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:785), 모두 `metrics()`.

OC-2의 법 적재 실패 분류는 추가됐지만, **법 함수가 처리하는 자료의 실패까지 검수 불능으로 묶였다.**

| 행 | 도달 가능한 자료 반례 | 실제 결과 |
|---|---|---|
| SITE-27 | 포인터가 종결을 선언하지 않는 상태에서 완주 판정서 JSON 손상 | `_run_is_terminated()`의 자료 판독 오류를 넓은 예외 경계가 잡아 검수 불능 |
| SITE-30 | `request.json#response_schema={}` | `LaneContractError`를 검수 불능 |
| SITE-30 | `request.json#slices=1` | 렌더 과정의 `TypeError`를 검수 불능 |
| SITE-33 | `material-spec.json#patent=1` | 스키마 검증 전 `.get()`의 `AttributeError`가 최상위 검수 불능 경계로 유출 |

정상 기준 런의 메모리 법 대조가 통과한 뒤, 읽는 자료만 바꾸어 실제 `metrics()`를 호출했다. 모두 exit 4이지만 접두가 다음과 같았다.

```text
REQUEST_DATA response_schema: 처분=검수 불능 · LaneContractError(...)
REQUEST_DATA slices: 처분=검수 불능 · TypeError(...)
TERMINATION_DATA: 처분=검수 불능 · ... JSON 파싱 오류 ...
SPEC_PATENT_SCALAR: 처분=검수 불능 · ... AttributeError ...
```

마지막 사례의 접두는 직접 함수 호출에서 나온 예외를 현재 CLI의 외곽 처리와 동일하게 분류한 결과다. 원인 예외 자체는 실제 `metrics()`에서 발생했다.

S23의 RunPaths·원장 루트·절차 문서·Rules.load 실패 시험은 유효하다. 그러나 이들이 **자료를 처리하다 실패하는 반대쪽 분기**는 시험하지 않는다. C90의 판정서 `[]`도 종결 포인터가 먼저 참인 경로여서 위 종결 가드 반례를 대신하지 못한다.

- **잘못된 처분:** 표에 부적격 사유를 남기고 보존해야 할 손상 자료가 “환경 수리 뒤 재검수·결과 표 제외”로 바뀐다.
- **수정 문안:** “중첩 자료 형태를 접근 전에 검증하고, 종결 가드·요청 재구성의 자료 실패와 법 적재 실패를 분리하여 각각 부적격과 검수 불능으로 전달한다.”

**OD-3 — MED · ⑴ T1·P7 집행 위반 · SITE-03·22·23**

좌표: 메모 §5′.1·§5′.4·§5′.11, [t40_receipts.py:117](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:117) `law_files`, 같은 파일 `bind_receipts`:465, [t40_metrics.py:142](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:142) `law_tree_files` 및 `metrics()`의 기준 법 집합 대조.

법 파일 수집 두 함수의 `os.walk()`에는 `onerror`가 없다. 따라서 디렉터리 열거 실패가 예외로 전달되지 않고 **일부 법 파일이 빠진 정상 반환값**이 된다.

실제 `os.walk()`를 유지하고 `os.scandir(<사본>/contracts)`에만 `PermissionError`를 주입했다.

```text
LAW_SCAN contracts rc_files=47 normal=63 sha_changed=True raised=False
LAW_BIND_SCAN ValueError is_infeasible=False
영수증 법 파일 지문 ≠ 현재 worktree(OA-1)
```

전체 기준 런 `metrics()`에서도 같은 열거 실패를 주입하자:

```text
BASELINE_LAW_SCAN exit=4
[t40_metrics] 처분=부적격 · --law-tree 와 런 리포의 법 파일 집합이 다르다(NT-5) ...
BASELINE_LAW_SCAN_DONE writes=0
```

법을 바꾸거나 삭제하지 않았다. **법을 열거할 수 없었던 것**이 법 불일치로 변환됐다. SITE-03의 “법 읽기 실패는 BindingInfeasible”, SITE-22의 “파일 집합 확정 → 지문”, SITE-23의 법 IO 경로가 모두 끊긴다.

C79·C89는 실제 법 불일치를 확인한다. S17은 자료 채집 함수의 열거 오류를 확인한다. 어느 것도 이 법 수집 경계의 오류 보존을 입증하지 않는다.

- **잘못된 처분:** 검수 환경의 법 판독 불능을 자료 부적격으로 기록한다.
- **수정 문안:** “법 디렉터리 확인과 열거는 IO 오류를 보존하고, 완전한 집합을 얻지 못하면 지문·집합 비교 전에 BindingInfeasible 또는 검수 불능으로 종료한다.”

**OD-4 — MED · ⑴ T1·P7 집행 위반 · SITE-08·21·36**

좌표: 메모 §5′.4·§5′.8·§5′.11, [t40_replay.py:175](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:175) 및 같은 파일 233·235행 `replay`, [t40_receipts.py:90](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:90) `_git`·`git_head`·`main_root_of`.

지표기 앞단의 조회 불능은 S23대로 분리됐다. 그러나 대조기 안에는 여전히 다음 연결이 남아 있다.

- 원본 `main_root_of()` 조회 실패 → “링크된 worktree가 아니다” → 기본 `mismatch`.
- sandbox `git_head()` 조회 실패로 `None` → 핀과 직접 비교 → `mismatch`.
- sandbox `main_root_of()` 조회 실패 → 루트 불일치 → `mismatch`.

공용 `_git()`은 실행 OSError 또는 비정상 종료를 `None`으로 반환한다. 위 호출부는 그 실패와 유효한 조회 결과의 불일치를 구별하지 않는다.

실제 `replay()`의 파일·하위 실행을 메모리 대역으로 연결하고 해당 조회 반환만 바꾼 결과:

```text
REPLAY_QUERY normal disposition=None replayed=1
REPLAY_QUERY origin-root-query disposition=mismatch replayed=0
REPLAY_QUERY sandbox-head-query disposition=mismatch replayed=0
REPLAY_QUERY sandbox-root-query disposition=mismatch replayed=0
```

SITE-21은 대조기 진입점까지 포함하며 “조회 성공 확인 → 핀 비교”를 약속한다. SITE-08·36에 배정된 호출식은 이를 지키지 않는다. S23은 앞단 지표기의 조회 실패를 시험하므로 이 후속 조회를 덮지 않는다.

- **잘못된 처분:** 검수 중 Git 조회 불능을 원본 자료의 부적격으로 승격한다.
- **수정 문안:** “대조기의 원본·sandbox 루트와 HEAD 조회는 실패를 별도로 전달하고, 성공한 값만 비교하며 조회 불능은 infeasible로 반환한다.”

**OD-5 — MED · ⑴ P6·P7 집행 위반 · SITE-40**

좌표: 메모 §5′.4·§5′.8·§5′.11, [t40_replay.py:289](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:289) `replay` 및 `DRIVER`, [t40_drive.py:339](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:339) `run_engine`, [engine/stages/read.py:1985](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1985) `run`.

새 검사는 하위 `returncode`·JSON·객체·`io_fault`를 결과 비교보다 먼저 확인한다. 그러나 러너는 **출구 원천 재독의 OSError를 내부에서 잡아** `read.source-digest` 실패 행을 만들고 `halt·4행`으로 반환한다.

그 반환을 `run_engine()`이 다음처럼 축약한다.

```text
{"kind":"return","status":"halt","reason_label":null,"rows":4}
```

`io_fault`가 없다. `DRIVER`는 상세 반환값 `_res`를 버린다. 따라서 원본 영수증이 정상 결과인 경우 sandbox의 환경 실패가 `mismatch`가 된다.

실제 출구 재독 예외 처리 AST를 메모리에서 실행하고, 실제 행·판정 생성 및 `run_engine()`의 직렬화를 연결해 위 반환을 확인했다. 이를 실제 `replay()`의 하위 결과로 공급한 결과:

```text
REAL_EXIT_REREAD_HANDLER halt rows=4
REAL_RUN_ENGINE_SERIALIZED ... io_flag=False
REPLAY_CAUGHT_HALT4 disposition=mismatch replayed=0
```

S24의 `sandbox-io`는 `read_text`를 첫 호출부터 실패시켜 **밖으로 나온 예외**를 시험한다. 두 번째 재독에서 잡히는 경로는 덮지 않는다. F의 L04는 **원본 실측**에 같은 결함을 주입하는 사례다. sandbox에서만 생긴 오류의 처분 근거가 될 수 없다.

- **잘못된 처분:** 원본에 결함이 없어도 검수 환경의 IO 실패가 자료 불일치가 된다. 이것을 T43 재실측으로 바꾸는 것도 허용되지 않는다.
- **수정 문안:** “sandbox 러너가 내부에서 포착한 IO 실패도 하위 결과에 보존하여 outcome 비교 전에 infeasible로 분리하고, T43 선판별은 원본 실측 기록에만 적용한다.”

**남은 자리와 진행도**

63행 모두 담당 함수·자원·오류 경로·순서와 근거를 대조했다. 미심사 행은 **없다**.

| 31차 미충족 행 | 이번 확인 |
|---|---|
| SITE-15·57 | pending/.next 봉인 차단 및 봉인 실패 분류 연결 확인 — S25·S26 |
| SITE-24 | 법·스키마 판독 실패의 명시적 역할 확인 |
| SITE-44 | 요청 열거 stat·scandir 오류의 자료/환경 역할 확인 — 확장 S17 |
| SITE-52·60·63 | sidecar·counter 선검사, 목적지 집합, retire 순서·재진입 차단 확인 — S19~22·S25 |
| SITE-21 | 앞단 수정은 유효하나 대조기의 후속 조회 실패가 남음 — OD-4 |
| SITE-27·30·33 | S23의 환경 경로는 닫혔으나 자료 오류 분기가 잘못됨 — OD-2 |
| SITE-40 | S24의 경로는 닫혔으나 러너 내부에서 잡힌 sandbox IO가 남음 — OD-5 |

미충족 행은 다음 **12개**다.

```text
SITE-03 SITE-08 SITE-21 SITE-22 SITE-23 SITE-27
SITE-30 SITE-33 SITE-36 SITE-40 SITE-55 SITE-56
```

```text
mismatch=12 unmet=12 unreviewed=0
```

31차 `12/12/0`에서 **7행 폐쇄·5행 잔여**, 다른 51행에서 **7행 불일치·44행 충족**이다. 동일 행에 여러 반례가 있어도 한 번만 셌다. 진행도는 31차 대비 감소하지 않았다. T45 ③의 연속 비감소 판정에 제공하는 이번 입력은 **12/12/0**이다.

정적 결과 `0/0/0`과의 차이는 selector 부재가 아니라 **배정된 호출의 실패 전달·자식 자원 경계·검사 선후가 행의 의무를 충족하지 않는 것**이다. 역방향에서 확인한 외부 러너 효과도 SITE-55·56에 배정돼 있어 별도의 “대장 누락”으로 중복 계수하지 않았다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 충족 | 고정 범위에서 상류 의무의 미배정 반례 없음. J01~39의 설계 선택 자체를 재개방하지 않음 |
| ② 신뢰·입력·부작용 경계 | 미충족 | 런 내부 출력 탈출, 법 열거·조회 불능 처리 — OD-1·3·4 |
| ③ 기제의 집행과 합성 | 미충족 | 호출부→외부 함수→결과 분류 사이 역할·경계 단절 — OD-1~5 |
| ④ 검증 근거 | 미충족 | S22~24의 실제 주입 경로가 위 잔여 경로를 덮지 않음 |
| ⑤ 미충족 상태의 처분 | 미충족 | 자료 부적격과 검수 불능이 양방향으로 뒤집힘 — OD-2~5 |

T44 자동 기동 조건의 도출 누락 0·새 보증 요구 0·갈래 ⑴만이라는 세 항목은 충족한다. 진행도 상신 규칙은 별도로 적용해야 한다.

**A 폐쇄표**

`closed`는 해당 과거 반례의 폐쇄다. 관련 성질 전체의 무결성을 뜻하지 않는다.

| 지적 | 상태 | 이번 대조 근거·잔여 |
|---|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed | 상태·계수·발췌 연결 유지, 기준값·발췌 메모리 재현 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed | 원장·결측·발췌 정의 및 해당 기제 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed | 요청·응답·원천 지문 연결 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed | 상태·소비 적격성·생성 관계 검사 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed | 기존 반례의 거부·종결·재시도·법 대조 유지. 새 오류 역할은 OD로 분리 |
| NU-1~4·NV-1~3 | closed | 비대칭 재시도·접지 그룹·첫 관측 결속 유지 |
| NW-1~5·NX-1~4·NY-1~4 | closed | 기존 루트·정규화·권한·경로·T43 반례 폐쇄 유지 |
| NZ-1·2·4·5 | closed | SITE-21의 무잠금 조회, SITE-02~06·09의 결속·선판별, SITE-58~63의 보존·시도 분리. S05~07·C84~87·S19~22 |
| NZ-3 | partially | 처분 전달 잔여 OD-2~5 |
| OA-1·2·4·5 | closed | 공용 결속·보존·봉인 집합·캐시 억제의 기존 반례 폐쇄 유지 |
| OA-3 | partially | 중첩 자료와 법·sandbox 실패 역할 잔여 OD-2~5 |
| OB-1 | closed | SITE-02·03, 공용 `bind_receipts` 뒤 선판별 — C93 |
| OB-2 | closed | SITE-01·04~06, 후보 선검사와 공통 집합 — C94·S09·S11 |
| OB-3 | closed | SITE-07~10, 원래 네 역할 반례 — C95~97·S12 |
| OB-4 | closed | SITE-11, evidence 전체 보호와 표식보다 앞선 겹침 검사 — S13 |
| OC-1 | closed | SITE-52·60·63, counter 읽기 전·sidecar 복사 전·목적지 집합 검사 — S21·S22 |
| OC-2 | partially | SITE-24와 지정 환경 주입은 닫힘 — S23. SITE-21·27·30·33 잔여 OD-2·4 |
| OC-3 | partially | SITE-40의 rc·JSON·밖으로 나온 IO 예외는 닫힘 — S24. 잡힌 IO 반환은 OD-5 |
| OC-4 | closed | SITE-44, requests_present의 stat·walk 오류 역할 — 확장 S17 |
| OC-5 | closed | SITE-15·57·63, 준비 검사 뒤 봉인·명령/CLI 오류 분류 — S25·S26 |

MY~OC 합계 **closed 117 · partially 4 · open 0**. NZ-3·OA-3의 잔여는 아직 닫히지 않았다.

**검증 경로**

모든 Python 실행은 사본 cwd에서 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B`로 수행했다.

| 명령·호출 경로 | 관측·마지막 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 마커 3항 일치·`81bf99419b477885545ce9fdd04753f54b584d58` |
| 대상 13개 파일 SHA-256 계산 | 발주 sha16 전부 일치 |
| `bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `rows=63 extracted=1393` → **`mismatch=0 unmet=0 unreviewed=0`** |
| 대장 요약 생성 결과와 메모 비교 | `SUMMARY_VIEW_EQUAL True` |
| `git log`·`git ls-tree`·`git diff --numstat` | base 부모 `6d92cad`; R1·R2 부모 base. R1·R2는 각각 read.yaml의 지정 값만 변경 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 출력 없음 — 기준 절차 동일 |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 문서 6개 복원. 마지막 행 `0 139 reader/procedure/HISTORY.md` |
| `git show origin/t40-{base,r1,r2}:contracts/stages/read.yaml` → 실제 `lane_profiles()` | R0·R1·R2의 네 좌석이 `registry()`와 일치 |
| `bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 4 · 마지막 줄 “처분=부적격 · 기준 런은 --law-tree … 필수” |
| `git show origin/t40-base:<경로>` 62개 법 파일 → 메모리 법 → 실제 `metrics(..., baseline=True)` | **`MEMORY_BASELINE_DONE writes=0 law_files=62`** |
| `t40_excerpts` import → 실제 `ex1/ex2`, 출력만 StringIO | **`EXCERPTS_DONE actual_writes=0 documents=2`** |
| `CASES()`와 회귀표 ID·부류 대조 | 143개·ID 동일·L13/F7/C95/X2/S26·표의 FAIL 0 |
| OD 메모리 주입: 실제 함수·법/자료 읽기 대역·하위 결과 대역 | 위 지적별 관측. 마지막 재검사 **`REPLAY_ROLES_DONE actual_writes=0`** |

기준 런은 `complete`, 명세 **163개**, component **56개**, 종속항 **24개**, additions **50개**였다. grounding은 `found/found=51`, `found/not-depicted=5`; 종속항 접지는 각각 45·5였다. synth 계수는 fact 3·implication 20·positioning 7·figure_note 10이며, 레인 shape/digest 검사 수는 각각 6으로 재현됐다.

발췌는 **27단위**이며, 종속항 표본은 `CL-2·4·7·9·12·14·16·19·21·24`였다. 기준 자료로 실행한 판정 불가 기계 표시 수는 0이었다. R0/R1 실측의 내용 품질을 판정한 것은 아니다.

**[미검증]**

143개 디스크 회귀는 재실행하지 않았다. 사례 정의·주입 위치·검사 조건과 제출 회귀표를 대조했으며, 표의 PASS를 이번 독립 실행 결과로 취급하지 않았다. 실측 모드, 실제 sandbox 생성·삭제, 실제 레인 호출·Workflow 서비스 실행도 하지 않았다.

OD-1의 외부 효과는 실제 러너·어댑터 호출의 **쓰기 의도**를 메모리로 관측했다. OD-5는 실제 예외 처리 부분·결과 직렬화·대조기 분기를 나누어 연결한 시험이며, 디스크를 쓰는 전체 러너 재실행은 아니다.

**읽은 파일**

- 원장·선행 심사: T40 §§1·4·5, `bundle/ruling-T42.md`, `bundle/ruling-T43.md`, T44·T45·T46, D-02 §17 추기 38~47, `ADVICE-REPLY-4.md`, 30·31차 감수 원문.
- 대상: `T40-MEASURE-DESIGN.md` v34의 지정 절, `T40-SITES-LEDGER.json` 63행과 selector, `T40-DESIGN-JUDGMENTS.md`, `T40-SCRIPT-SHA256.txt`, `T40-REGRESS-TABLE.md`, 발주에 열거된 Python 스크립트와 Workflow.
- 계약·실물: SPEC §8.4 G-1~3·G-12, run-kinds·read 계약·approval-envelope 스키마, `engine/stages/read.py`, `engine/paths.py`, 레인 contract·file_adapter·plan, `reader/lib/convergence.py`·`run_checks.py` 및 호출되는 규칙·검증 코드.
- 자료: 기준 런의 원천·run.yaml·판정서·포인터·명세·레인 로그·요청/응답·봉투와 대상 원장 행, `git show`로 읽은 세 계측 브랜치의 계약 및 기준 법 파일.