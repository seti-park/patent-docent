# 독립 감수 원문 — M1b 설계 도전 34차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v36(법 밖 폐쇄 · 33차 OE-1~5 반영) · 판정 REVISE(HIGH 2 · MED 5)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `113e0b19fc5020dbc87bef096424949cbc04ab793fd6ff918dcb665cd1552df9` · 22251 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v34/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(T46 ③) · Monitor(15:54 기동 · 16:2x 종료 · USAGE 는 레인 STATUS). 사본 재핀 `1b00e85` · 메모 v36 `e9caa2a7e0e55800` · 대장 `b0218a75b1c6aaef`(66행) · 회귀표 v15(157) · bundle 72. 이번 기동 = T44 자동(33차 조건 충족 · 진행도 감소).

**판정 = REVISE · 7건(HIGH 2 · MED 5) · 기각 0 · 발주자 귀책(저작 astra xhigh 5차 · 발주·검수 총괄).** 지문 16 일치 · 정적 0/0/0 · 심사 ① 성립 · ②~⑤ 불성립 · 갈래 ⑴ 7 · 도출 누락 0 · 새 보증 0 · 대장 누락 반례 0. **진행도(행 단위) = `mismatch=10 unmet=10 unreviewed=0` — 12 → 12 → 9 → 10 · 비감소 1회 → 35차도 비감소면 T45 ③ 상신.** 33차 9행 중 4 닫힘(23·42·50·51) · 5 잔여(09·27·40·55·56) · 새 5(46·49·58·63·65). A 폐쇄표 closed 123 · partially 8 · open 0 · OD-3·OE-1·OE-2·OE-5 closed · OE-3·OE-4 partially · NZ-2 가 새 순서 반례로 partially. **선검증 목록 ↔ 러너 실제 조회 대조 = 인자 누락 0**(비linked 2회 · linked 3회 argv 일치) — 그러나 같은 판정을 하는 `retire` 호출에는 봉투 미연결(OF-1) · 호출 뒤 디렉터리 조회 실패의 산출 표식 `refused` 가 후검출에서 빠짐(OF-3). **OF-1 HIGH · P3·P6·T3 · SITE-58**: `cmd_retire` 가 종결 가드 `_run_is_terminated` 를 직접 호출(선검증·봉투 없음) → 내부 git rc128 이면 법이 원장 위치를 worktree 안으로 바꿔 「비종결」 → 종결된 런을 재실측 대상으로 삭제·시도 갱신. **OF-2 HIGH · P5 · SITE-49**: `cmd_source` 출력 경계가 런 루트까지 → `00-source` 가 밖을 가리키는 링크면 `source.run` 첫 쓰기가 worktree 밖. **OF-3 MED · P2·P7 · SITE-27·40·55·65**: 선검증 성공 뒤 포인터 기록 시점의 `isdir(main_root)` 실패 → 법이 `root_source="refused"` 로 포착 → 후검출 표식에 `refused` 없음 · 지표기는 refused 허용 · 대조기 원시 포인터 검사가 refused 의 root·ledger 대조 생략. **OF-4 MED · P2·P6·T3 · SITE-46·56**: `run_engine` 이 `environment_fault=true` 를 돌려줘도 `cmd_read` 가 `write_receipt` 전에 예외 → 호출 영수증 소실(exc 파일 + exit 14 만). **OF-5 MED · P2·P6 · SITE-40·55**: `annotate()` 가 모든 `FileNotFoundError` 를 IO 사건에서 제외 → 필수 `request.md` 의 `_bare_sha256_file` ENOENT 가 IO 표식 없는 검사 실패로. **OF-6 MED · P6·P7 · SITE-09**: 두 소비기가 `bind_receipts` 뒤 IO 선판별보다 먼저 `require_runner_output()` 으로 포인터 JSON 파싱 → 결속된 IO 예외가 있는데 포인터 비JSON 이면 `mismatch/부적격`(선판별 순서 역전). **OF-7 MED · P6·P7·T3 · SITE-63**: `cmd_source` 가 `require_attempt_ready` 미호출 → pending/.next 재진입에서 같은 ID 원천 작성.

**총괄 진단**: 일곱 중 셋(OF-1·OF-2·OF-7)이 **구동기 서브커맨드(source · retire)가 다른 서브커맨드(read · seal)에 붙인 의무(선검증 · 출력 경계 · 준비 검사)를 지나지 않는다**는 형태 — 28차부터 반복된 「같은 성질을 집행해야 하는 자리가 여럿인데 한 자리에만 넣었다」다. 대장은 자리를 행으로 열거하지만, **「진입점 × 의무」 격자의 빈 칸**을 기계가 검사하지 않는다(정적 대조는 selector 존재만). v37 = 진입점(구동기 서브커맨드 6 · 지표기 · 대조기 함수) × 의무(선검증 · 출력 경계 · 준비 검사 · 영수증 보존 · IO 선판별 순서 · 후검출) **격자를 대장에 두고 `t40_sites.py` 가 호출 그래프 도달성으로 빈 칸을 FAIL 로** 내게 한다. 진행도 비감소 1회 — 35차도 비감소면 상신(결정 브리핑 · 선택지 넷).

**처분 = 전부 수용(공학) · 이행 = v37 저작(astra xhigh 6차 · T44 자동).** 수정 문안(도전자 원문) — OF-1 「retire 의 종결 가드에도 동일 환경 선검증과 내부 실패 봉투를 적용하고, 조회 실패는 보존·이동·삭제 전에 검수 불능으로 중단한다」 · OF-2 「source 도 첫 부작용 전에 실제 출력 목적지와 기존 하위 항목·조상을 승인된 worktree 에 결속해 검사하고, 링크 위반은 무쓰기 거부한다」 · OF-3 「법의 메타 조회 실패가 만드는 refused 경로까지 발생 원인 또는 실제 산출 표식으로 보존·검출하여, 원본은 검수 불능·sandbox 는 infeasible 로 값 비교 전에 분리한다」 · OF-4 「환경 실패 outcome 도 채집 가능한 pre·post 와 함께 호출 영수증에 보존한 뒤 exit14 로 중단하고, 기록 실패 자체를 별도로 표시한다」 · OF-5 「FileNotFoundError 제외를 합법적 부재를 허용하는 조회 자리에 한정하고, 필수 자원의 내부 포착 FileNotFoundError 는 IO 사건으로 보존한다」 · OF-6 「결속된 환경·IO 기록의 선판별을 비필수 산출물 파싱 오류가 가로막지 않도록 순서를 정하고, 알려진 IO 가 없는 자료의 포인터 오류는 기존 부적격 처분을 유지한다」 · OF-7 「source 도 첫 부작용 전에 require_attempt_ready 를 호출하여 pending/.next 가 남은 같은 ID 재진입을 exit14 로 중단한다」. 발주자 오류 누계 212 → **219**.

지적 열거 = OF-1, OF-2, OF-3, OF-4, OF-5, OF-6, OF-7

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE  
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 34회)

**OF-1~7: HIGH 2 · MED 5 · 전부 갈래 ⑴.** 도출 누락 0 · 새 보증 요구 0 · ⓑ 대장 누락 반례 0. ⓐ 연결 불일치와 ⓒ 집행·근거 공백은 중복 제거 **10행**이다.

마커의 path·pin·order와 HEAD `1b00e85fa690f98eaf97b79814d252bbeb2080ba`가 일치했다. 메모 `e9caa2a7e0e55800`, 대장 `b0218a75b1c6aaef`를 포함해 발주에 지문이 명시된 **16개 파일 모두 일치**했다. 지문 불일치 지적은 없다.

정본 리포는 읽지 않고 지정된 인터프리터만 사용했다. 파일 생성·수정·삭제, checkout·worktree·stash, 배경 실행은 하지 않았다. 아래 실행 관측에서 쓰기·삭제는 모두 메모리 대역이다.

**선검증 목록과 실제 러너 조회 대조**

`engine/paths.py`·`engine/gitpin.py`는 사본과 세 계측 핀에서 바이트가 같았다. `shadow_ledger_root(repo, None)`의 실제 호출 순서를 `runner_environment()`와 대조했다.

| 실제 법의 조회 | v36 선검증 대조 |
|---|---|
| `base = realpath(repo)` | 같은 기준 경로 |
| `worktree_of(base)` → `git -C base rev-parse --git-dir` | 동일 |
| 이어서 `--git-common-dir` | 동일 |
| linked 분기의 `git_common_dir(base)` 재조회 | 동일 |
| linked 분기의 `isdir(main_root)` → `stat` | 선검증은 직접 `stat`하며 오류를 전파 |
| git-dir·common·main의 경로 해석 | 선검증도 realpath로 결속하며 디렉터리 확인을 추가 |

메모리 호출 관측에서 **비linked 2회·linked 3회의 argv와 `capture_output=True, text=True`가 일치**했다.

`gitpin.resolve_pin()`에는 별도로 `isdir(repo)`·common 조회·`status --porcelain -z`·HEAD·worktree 판별이 있다. 이는 `source`의 핀 결속 경로이며 READ의 원장 루트 조회 집합과 구별했다.

조회 **목록 자체의 Git 인자 누락은 발견하지 않았다.** 그러나 같은 원장 판정을 하는 `retire` 호출에는 이 봉투가 연결되지 않았다(OF-1). 또한 호출 전 성공 이후 발생하는 디렉터리 조회 실패의 실제 산출 표식 `refused`가 후검출에서 빠진다(OF-3). 따라서 선검증·후검출의 합성은 아직 닫히지 않았다.

**OF-1 — HIGH · ⑴ P3·P6·T3 집행 위반 · SITE-58**

좌표: 메모 §2·§5′.3·§5′.11, [t40_drive.py:507](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:507) `cmd_retire`, `engine/stages/read.py:1094` `_run_is_terminated`.

`cmd_retire()`는 520행에서 실제 종결 가드를 직접 호출한다. `R.external("termination", …)`이나 동일 환경 선검증이 없다.

포인터·완주 판정서가 없고 **주 원장에만 종결 근거가 있는 런**에서 내부 git 조회를 rc128로 실패시키면, 법의 `GitUnavailable` 포착이 원장 위치를 worktree 안으로 바꾼다. 그곳의 원장 부재가 비종결로 반환된다.

실제 종결 가드와 실제 `cmd_retire()`를 연결하고 부작용만 메모리로 바꾼 관측:

```text
정상 git: (True, 'shadow_ledger')
git rc128: (False, None)

RETIRE_GIT_FALLBACK exit 0
ops ['mkdir', 'copy', 'remove-run']
current 2 pending False
```

**잘못된 효과:** 종결된 런을 같은 ID 재실측 대상으로 처리하고 런 삭제·시도 갱신까지 진행한다. T43의 “종결 기록이 남은 결함 런은 … 새 런 ID와 T40 §5 봉투 범위 확장” 조건을 우회한다.

S06·S07은 정상 조회의 비종결/종결을 시험한다. 새 S29·S37의 실제 git 실패 주입은 이 `retire` 호출을 덮지 않는다.

**수정 문안:** “retire의 종결 가드에도 동일 환경 선검증과 내부 실패 봉투를 적용하고, 조회 실패는 보존·이동·삭제 전에 검수 불능으로 중단한다.”

**OF-2 — HIGH · ⑴ P5 집행 위반 · SITE-49**

좌표: 메모 §5′.3·§5′.5 P5·§5′.11, [t40_drive.py:144](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:144) `cmd_source`, `seal_source`:127, `engine/stages/source.py:646`, `engine/paths.py:415`.

`cmd_source()`의 출력 경계 검사는 **런 루트까지만** 한다. 실제 `source.run()`은 `00-source` 아래의 기존 링크를 검사하지 않고 디렉터리 생성과 파일 쓰기를 수행한다.

호출 전부터 `00-source → 외부의 빈 디렉터리`인 상태를 메모리로 표현했다. 실제 `cmd_source → seal_source → source.run`과 실제 진입 검사를 실행하고 핀 조회·파일시스템 효과만 대체했다.

```text
SOURCE_ALIAS
boundary_targets=[…/runs/__t40_memory_source__]
first_write:
  …/runs/__t40_memory_source__/00-source/patent.md
  → /__t40_memory_protected__/patent.md
actual_writes=0
```

`patent.md`가 아직 없으면 기존 원천 지문 검사와 재투입 거부를 통과한다. 이후 첫 쓰기가 이미 승인된 worktree 밖이다. 동시 교체나 hardlink 반례가 아니다.

SITE-49는 해당 외부 호출·`00-source` 자원·출력 경계를 이미 담고 있다. 그러나 “source.run의 파일 효과는 핀 법에 귀속”이라는 구조 논거는 §5′.3의 허용 효과를 집행하지 않는다. L01·X01도 이 링크 경로를 시험하지 않는다.

**수정 문안:** “source도 첫 부작용 전에 실제 출력 목적지와 기존 하위 항목·조상을 승인된 worktree에 결속해 검사하고, 링크 위반은 무쓰기 거부한다.”

**OF-3 — MED · ⑴ P2·P7 집행 위반 · SITE-27·40·55·65**

좌표: 메모 §5′.4·§5′.11, [t40_resources.py:256](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_resources.py:256) `fallback_markers`, `external_scope`:166, `engine/paths.py:211`, `engine/stages/read.py:2244` `_write_shadow_pointer`.

선검증 성공 뒤, 러너의 포인터 기록 시점에만 주 작업 트리 `stat`가 실패하면 다음 경로가 열린다.

```text
isdir(main_root)
→ OSError를 False로 바꿈
→ ShadowLedgerRootError
→ _write_shadow_pointer가 포착
→ root_source="refused", root=None, ledger=None, error=…
```

실제 포인터 작성 함수의 해당 `stat`만 실패시킨 관측:

```text
REFUSED_STAT hits 1 source refused
io_events 0 git_faults 0 markers []
```

현재 관측기는 open·스트림·git 프로세스를 관측하지만 이 메타 실패를 기록하지 않는다. `fallback_markers()`에도 `refused`가 없다.

법의 “정상 경로에서는 도달 불능” 주석에는 **두 해석 사이 상태 유지라는 조건**이 명시돼 있다. v36이 다루는 일시 실패에서는 선검증 성공만으로 그 조건을 증명할 수 없다.

**잘못된 처분:** 지표기는 `refused`를 허용하며, 대조기의 원시 포인터 검사는 `refused`의 root·ledger 대조를 건너뛴다. sandbox에서 발생하면 환경 실패가 아닌 산출물 `mismatch`로 흐를 수 있다. S38은 git 실패·회복을 시험하지만 이 디렉터리 조회 실패는 덮지 않는다.

**수정 문안:** “법의 메타 조회 실패가 만드는 refused 경로까지 발생 원인 또는 실제 산출 표식으로 보존·검출하여, 원본은 검수 불능·sandbox는 infeasible로 값 비교 전에 분리한다.”

**OF-4 — MED · ⑴ P2·P6·T3 집행 위반 · SITE-46·56**

좌표: 메모 §2·§5′.1 T3·§5′.4, [t40_drive.py:455](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:455) `cmd_read`.

`run_engine()`이 `environment_fault=true`와 실패 표식을 정상적으로 돌려줘도, `cmd_read()`는 즉시 예외를 던진다. **`receipt_post → write_receipt`에 도달하기 전**이다. 외곽 경계는 자유문 `exc` 파일과 exit14만 남긴다.

pre 채집이 성공하고 결과·증거 저장 대역도 정상인 상태에서 실제 `cmd_read()`를 호출한 관측:

```text
ENV_RECEIPT_LOST exit 14
calls ['exc']
receipt_post=0 write_receipt=0
```

**잘못된 효과:** 실패를 검출했지만 그 호출의 구조화된 실행 기록을 버린다. 일시 git 실패 후 포인터가 정상으로 회복한 경우, 소비기가 읽어야 할 `outcome.environment_fault`가 영수증에 도착하지 않는다. `exc`는 봉인 대상이지만 환경 실패 선판별의 입력이 아니다.

S38의 회복 시험은 `run_engine()` 반환 표식을 확인한다. 실제 `cmd_read()`가 그 표식을 영수증으로 전달하는 연결은 시험하지 않는다. SITE-46의 명시 순서와 T42의 “호출마다 영수증”이 끊긴다.

**수정 문안:** “환경 실패 outcome도 채집 가능한 pre·post와 함께 호출 영수증에 보존한 뒤 exit14로 중단하고, 기록 실패 자체를 별도로 표시한다.”

**OF-5 — MED · ⑴ P2·P6 집행 위반 · SITE-40·55**

좌표: 메모 §5′.4·§5′.11, [t40_resources.py:83](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_resources.py:83) `annotate`, `t40_drive.py:366` `run_engine.read_text`, `engine/stages/read.py:1452·1471·1583`.

`annotate()`는 **모든 `FileNotFoundError`를 IO 사건에서 제외**한다. 별도 보존은 `read_stage.read_text` 경로에만 있다.

그런데 실제 `check_lane_log_digest_value()`의 필수 `request.md` 읽기는 `_bare_sha256_file()`을 사용한다. 여기서 발생한 `FileNotFoundError`는 법 내부에서 실패 소견으로 바뀌며, `read_text` 보존 경로를 지나지 않는다.

같은 필수 파일·같은 실제 검사에 예외 종류만 바꿔 주입했다.

```text
CAUGHT_REQUEST PermissionError
hits 1 status fail events 1 finding ['lane-log.digest-file-unreadable']

CAUGHT_REQUEST FileNotFoundError
hits 1 status fail events 0 finding ['lane-log.digest-file-unreadable']
```

**잘못된 효과:** 필수 자료 읽기 실패가 IO 표식 없는 검사 실패로 반환된다. 원본에서는 T43 근거를 잃고, sandbox에서는 IO 선판별을 지나 outcome/post 비교로 흐를 수 있다.

종결 근거의 합법적 부재를 제외하는 판단은 유지할 수 있다. 문제는 그 제외가 필수 요청서 읽기까지 확장된 것이다. S39는 `PermissionError`만 주입한다.

**수정 문안:** “FileNotFoundError 제외를 합법적 부재를 허용하는 조회 자리에 한정하고, 필수 자원의 내부 포착 FileNotFoundError는 IO 사건으로 보존한다.”

**OF-6 — MED · ⑴ P6·P7 집행 위반 · SITE-09**

좌표: 메모 §5′.4·§5′.8·§5′.11, [t40_replay.py:228](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:228), `t40_metrics.py:434`, `t40_resources.py:270`.

두 소비기는 `bind_receipts()` 뒤 **IO 선판별보다 먼저** `require_runner_output()`을 호출한다. 이 함수는 포인터 JSON을 파싱하며 `JSONDecodeError`를 그대로 전파한다.

영수증·MANIFEST·현재 attempt·run_id·법·run.yaml 결속이 유효하고 outcome에 IO 예외가 있는 자료에서 포인터만 비JSON이면, 알려진 실측 IO보다 포인터 파싱 오류가 먼저 처분된다.

결속 함수도 대체하지 않고 **실제 `bind_receipts()`와 실제 `replay()`**를 메모리 파일 계층에서 연결했다. 법 조회 성공 값과 환경만 대체했고 sandbox 실행은 금지했다.

```text
REAL_BIND_POINTER_ORDER
bound=1 io=True disposition=mismatch replayed=0 actual_writes=0

REASON Expecting property name enclosed in double quotes:
line 1 column 2 (char 1)
```

**잘못된 처분:** 결속된 IO 예외가 있는데 `io-fault/재실측` 대신 `mismatch/부적격`이다. 이것은 손상 포인터를 적격으로 인정하라는 요구가 아니다. SITE-09가 정한 **결속·정합 완료 뒤 IO 선판별 순서**의 위반이다.

S39의 정상 포인터와 C84·C85의 기존 선판별 사례는 새 포인터 파싱 경계를 덮지 않는다.

**수정 문안:** “결속된 환경·IO 기록의 선판별을 비필수 산출물 파싱 오류가 가로막지 않도록 순서를 정하고, 알려진 IO가 없는 자료의 포인터 오류는 기존 부적격 처분을 유지한다.”

**OF-7 — MED · ⑴ P6·P7·T3 집행 위반 · SITE-63**

좌표: 메모 §2·§5′.11, [t40_drive.py:144](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:144) `cmd_source`, `t40_receipts.py:321` `require_attempt_ready`.

SITE-63은 진입점에 **구동기 source**를 포함하고, `pending` 또는 `.next` 재진입의 구동 중단을 명시한다. 그러나 `cmd_source()`는 준비 검사를 호출하지 않는다.

retire가 런 삭제 뒤 current 교체에 실패한 상태는 S19가 직접 만드는 지원 오류 상태다. 이때 런 폴더는 없고 pending 또는 `.next`가 남을 수 있다. `source` 재호출은 준비 상태를 읽지 않고 같은 ID의 원천 작성으로 진행한다.

```text
SOURCE_UNREADY pending exit 0 ready_checks 0 calls ['source-write']
SOURCE_UNREADY .next   exit 0 ready_checks 0 calls ['source-write']
```

위 관측은 실제 `cmd_source()`에 쓰기 대역을 연결한 것이다. 준비 검사 대역은 호출되면 거부하도록 두었지만 호출되지 않았다.

**잘못된 효과:** 복구 미완 상태에서 같은 ID의 런을 다시 만든다. SITE-63의 진입점 열과 실제 기제가 불일치한다. S19·S20·S25는 read·retire·소비·seal을 시험하며 source를 덮지 않는다.

**수정 문안:** “source도 첫 부작용 전에 require_attempt_ready를 호출하여 pending/.next가 남은 같은 ID 재진입을 exit14로 중단한다.”

**남은 자리와 진행도**

66행의 담당 함수·자원·오류 경로·순서와 검증 근거를 대조했다. **미심사 행은 없다.**

| 구분 | SITE 행 |
|---|---|
| 33차 미충족 9행 중 해당 오류 경로가 닫힘 | 23·42·50·51 |
| 33차에서 잔여 | 09·27·40·55·56 |
| 이번 추가 미충족 | 46·49·58·63·65 |
| 미심사 | 없음 |

```text
미충족:
SITE-09 SITE-27 SITE-40 SITE-46 SITE-49
SITE-55 SITE-56 SITE-58 SITE-63 SITE-65

mismatch=10 unmet=10 unreviewed=0
```

같은 행의 복수 반례는 한 번만 셌다. 공용 역할 기제 SITE-26의 selector를 소비 행과 중복 계수하지 않았다. SITE-65는 별도로 신설된 **후검출 의무 자체**가 실패하므로 포함했다.

역방향에서 확인한 source의 외부 쓰기, retire의 내부 git, 러너 내부 메타·IO 효과는 기존 행의 진입점·자원 범위에 이미 있다. 따라서 **대장 누락으로 중복 제출하지 않는다.**

31차 `12/12/0` → 32차 `12/12/0` → 33차 `9/9/0` → 이번 **`10/10/0`**이다. **비감소 1회**이며, 지금은 T45 ③의 두 회차 연속 비감소 조건이 성립하지 않는다. 다음 판도 비감소면 상신 대상이다. 이번 지적은 전부 갈래 ⑴이므로 T44 자동 기동 조건은 충족한다.

**심사 대상 ①~⑤**

| 심사 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 성립 | 상류에서 누락된 새 성질·절차 의무는 발견하지 않음. 지적은 기존 P/T 적용 자리의 미집행 |
| ② 신뢰·입력·부작용 경계 | 불성립 | source 외부 쓰기, 호출 영수증 소실, 복구 미완 재진입 |
| ③ 기제의 집행과 합성 | 불성립 | retire 봉투 미연결, refused 미검출, 필수 ENOENT 탈락, 선판별 순서 역전 |
| ④ 검증 근거 | 불성립 | 지정 사례는 존재하나 위 오류 경로·생산자→소비자 연결을 지지하지 못함 |
| ⑤ 미충족 상태의 처분 | 불성립 | 종결 런 retire 성공, 환경 실패의 mismatch, 원본 IO의 부적격 전환 |

**A 폐쇄표**

`closed`는 기존 지적의 구체 경로가 닫혔다는 뜻이다. 같은 넓은 성질의 다른 경로는 OF로 구별했다.

| 지적 | 상태 | 이번 대조 |
|---|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed | 선등록·계수·발췌·발주 통제 유지 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed | 기존 오류 종료·원장·결측·식별 결속 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed | 요청·응답·원천 지문과 스키마 연결 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed | 검사 집합·형태·소비 적격성·상태 연결 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed | 기존 종결·재시도·법·렌더 경로 유지 |
| NU-1~4·NV-1~3 | closed | 비대칭 재시도·접지 그룹·첫 관측 유지 |
| NW-1~5·NX-1~4·NY-1~4 | closed | 기존 정규화·권한·경로·IO 사례 유지 |
| NZ-1·4·5 | closed | 무잠금 조회·시도·봉인 유지 |
| NZ-2 | partially | 새 포인터 파싱이 결속 뒤 IO 선판별을 선점 — OF-6 |
| NZ-3 | partially | 환경·자료·재실측 처분 잔여 — OF-3·5·6 |
| OA-1·2·4·5 | closed | 결속·보존 사본·공통 봉인 집합·캐시 억제 유지 |
| OA-3 | partially | 외부 메타 실패가 처분 경계 전에 소실 — OF-3 |
| OB-1 | closed | SITE-02·03, C93·C86~89: 공용 결속 유지 |
| OB-2 | closed | SITE-01·04~06, C94·S09·S11: 공통 집합·후보 선검사 |
| OB-3 | closed | SITE-07~10, C95~97·S12: 원래 자료/법 반례 폐쇄 |
| OB-4 | closed | SITE-11, S13: evidence 전체 보호·겹침 검사 선행 |
| OC-1 | closed | SITE-52·60·63, S21·S22: 기존 counter·sidecar·목적지 경계 |
| OC-2 | partially | S23·S37의 지정 실패는 폐쇄, SITE-27의 메타 실패 잔여 — OF-3 |
| OC-3 | partially | SITE-40, S24·S33·S38·S39 외의 내부 실패 잔여 — OF-3·5 |
| OC-4 | closed | SITE-44, 확장 S17: 요청 열거 오류 전파 |
| OC-5 | closed | SITE-15·57·63, S25·S26: seal 준비 검사·실패 분류 |
| OD-1 | closed | SITE-55·56, S27: 기존 READ 내부 링크 경로 |
| OD-2 | partially | S29~31의 반대 역할은 폐쇄, SITE-27 메타 실패 잔여 — OF-3 |
| OD-3 | **closed** | SITE-03·22·23, S28·S36: walk 및 절차 stat/listdir 오류 전파 |
| OD-4 | closed | SITE-08·21·36, S32: 직접 git 성공 봉투 뒤 비교 |
| OD-5 | closed | SITE-40, S33: 기존 원천 IO·UnicodeDecodeError 경로 |
| OE-1 | **closed** | SITE-55·56, S35: 주 원장 말단·조상 경계와 realpath 역할 결속 |
| OE-2 | **closed** | SITE-23, S36: 절차 메타 오류를 법 실패로 전파 |
| OE-3 | **partially** | SITE-27·40·42·55·64·65, S29·S37·S38. 실제 git 실패는 보강됐으나 refused·기록 전달·retire 연결 잔여 — OF-1·3·4 |
| OE-4 | **partially** | SITE-09·40·55·66, S39. 13행 PermissionError 소비는 폐쇄, 필수 ENOENT와 새 파싱 순서 잔여 — OF-5·6 |
| OE-5 | **closed** | SITE-50·51, S40: pending 전량 열거 성공 전 완료·발주 금지 |

**MY~OE 합계: closed 123 · partially 8 · open 0.** 기존 partially 6개 중 OD-3이 닫혔다. NZ-2는 새 선판별 순서 반례로 partially가 됐다.

**검증 경로**

모든 Python 실행은 지정 인터프리터에 `PYTHONDONTWRITEBYTECODE=1`과 `-B`를 적용했다.

| 명령·경로 | 마지막 출력 또는 관측 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `1b00e85fa690f98eaf97b79814d252bbeb2080ba` · 마커 3조건 일치 |
| `hashlib.sha256`으로 지정 16파일 대조 | 16/16 일치 |
| `bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | `rows=66 extracted=1606` → **`mismatch=0 unmet=0 unreviewed=0`**, exit0 |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 파일 6개만 변경 · 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` | `2 2 contracts/stages/read.yaml` |
| 같은 명령의 `origin/t40-r2` | `2 2 contracts/stages/read.yaml` |
| `git diff d4e6ca2 origin/t40-base -- reader/procedure` | 출력 없음 |
| 세 핀의 read.yaml을 `git show`로 읽고 실제 `lane_profiles()` 호출 | r0·r1·r2 모두 `registry_equal True` |
| 세 핀의 paths.py·gitpin.py 바이트 대조 | `PIN_PATHS_GITPIN_EQUAL True` |
| `bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `처분=부적격 · 기준 런은 --law-tree … 필수`, **exit4** |
| `git show origin/t40-base:<경로>`의 62파일을 메모리 법으로 공급해 실제 `metrics()` 호출 | `complete · 163 · component 56 · E attempt 1 · full attempt 1` |
| 위 기준 검수의 마지막 관측 | `MEMORY_BASELINE_DONE actual_writes=0 law_files=62` |
| 실제 `CASES()`와 회귀표 ID 대조 | `157 {'L':13,'F':7,'C':95,'X':2,'S':40} … ids_equal True FAIL_rows 0` |
| 발췌기 import 후 기준 자료를 각 입력에 공급, 출력만 메모리 대체 | 27단위 · 종속항 N=24 · 표본 CL-2·4·7·9·12·14·16·19·21·24 · `actual_writes=0` |

정적 `0/0/0`과 심사 `10/10/0`의 차이는 **selector의 존재가 아니라, 그 selector에 배정된 자원·오류·순서의 실제 미집행**이다.

**[미검증]**

- 157사례 전체의 디스크 회귀는 재실행하지 않았다. 사례 수·ID·기대와 첨부 결과표를 대조하고, 지적 경로는 별도 메모리 시험으로 확인했다.
- 생산 실측, 실제 sandbox 재조립, 디스크 source/read/retire/dispatch/seal은 실행하지 않았다. 메모리 시험의 쓰기·삭제 관측은 실제 파일 변경 성공을 주장하지 않는다.
- Workflow 실호출 모델·effort transcript, Owner의 ①② 정성 판정, 외부 스테이징 실물은 이번 검증 결과가 아니다.
- 동시 교체·hardlink·법 변경을 새 보증으로 요구하지 않았다.

**읽은 파일**

상류는 T40·T44·T45·T46 재정, `bundle/ruling-T42.md`·`ruling-T43.md`, D-02 §17 추기 38~51, `ADVICE-REPLY-4.md`, 31~33차 감수 원문을 읽었다. 대상은 메모 v36과 관련 이전판, 대장 JSON, 설계 판단 J01~J52, resources·drive·receipts·replay·metrics·sites·excerpts·envelope·workflow, 회귀 본체·r4·r5·결과표·지문표다.

법과 실물은 SPEC §8.4의 지정 항목, run-kinds·read 계약·approval-envelope 스키마, `engine/paths.py`·`gitpin.py`·`stages/read.py`·`stages/source.py`·`stages/__init__.py`, 레인 contract·file_adapter·plan, convergence·run_checks 및 기준 런의 run.yaml·원천·판정서·명세·레인 요청/응답·원장 자료를 대조했다. **PASS 전 실측 착수 금지는 유지된다.**