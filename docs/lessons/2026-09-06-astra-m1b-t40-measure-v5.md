# 독립 감수 원문 — M1b 설계 도전 5차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v5 · 판정 REVISE(MED 3)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `15bb1ab567cabcd07c414c3480f27fb52d9fb462825524b094d6d88e61c338d0` · 16555 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v5/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 06:16:35 → 06:28 · **USAGE = input 2,952,174(cached 2,787,968) · output 18,774(reasoning 3,506)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `f21236d` · `bundle/T40-MEASURE-DESIGN.md` v5 sha256 `29578689…efb2` · v4 동봉 · 구동·지표 v5 · 발췌·Workflow v4). 폐쇄 = **MY 11/2 · MZ 7/2 · NA 5/2 · NB 1/2(closed/partially) · open 0**. 4차 지정 반례 전건 닫힘(enter OSError · 증거 makedirs · 증거 쓰기+종결 · 손상 조기 JSON 세 경로 = 14 · dispatch A,A,A,B,C,D = 0/14/14/0/0/15 · counter 기록 실패 14 + 복구 규칙 검증 · NB-3 지정 반례 전부 exit 4). B·E·F PASS(확인 범위). 정상 분류·기준 계수·6/6 재렌더·발췌 27/27·표본·Workflow 거부 재확인.

**판정 = REVISE · 3건(MED 3) · 기각 0 · 전부 발주자 귀책 · BLOCKER/HIGH 0.** **NC-1 MED**: 실제 `enter` 의 진입 실패는 `fail()` → `SystemExit(2/3)` 인데 `cmd_read` 의 `except SystemExit: raise` 가 그대로 내보냄 → worktree 부재 = exit 2 · 증거 0(선언 「진입 실패 = 14」 위반). **NC-2 MED**: SHA 검증 뒤 `sha(early_src)` 재독과 검사 배열 변환이 exit 4 경계 밖 → 두 번째 읽기 PermissionError · `checks=null` TypeError 미포착. **NC-3 MED**: `isinstance(x, int)` 가 bool 을 받고 jaccard 의 유한성·0~1 범위 미검사 → `[true,true]`·`[-1,-1]`·`jaccard=true/2.0/NaN` 수용(`[True,True]==[1,1]` 이라 비교까지 통과).

지적 열거 = NC-1, NC-2, NC-3

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 4**. **전부 수용 → 설계 메모 v6 + 구동·지표 v6 → M1b 6차 도전(지적 `ND-*`)**. 도전자 [미검증] 「v3 메모 원본이 bundle·Git 에 없다」 = 총괄 사실 — 메모 판본은 리포 밖(drafts)에만 있고 bundle 에는 직전 판만 동봉한다(v6 bundle 에 v1~v5 전부 동봉으로 정정).

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**폐쇄 판정은 MY 11 closed·2 partially / MZ 7 closed·2 partially / NA 5 closed·2 partially / NB 1 closed·2 partially입니다. open은 없습니다.** 4차의 지정 반례는 모두 수정됐습니다. 그러나 실제 진입 실패의 종료 코드, 검증 뒤 재독 오류, 잘못된 수치형 수용에 **MED 3건**이 남습니다.

격리 마커의 path·pin·order·disposable과 HEAD `f21236d184678f49b92f7786bbfc4676fe9bbf2f`가 일치했습니다. 메모 SHA-256도 `29578689e62b4892f69432d81a7767b55fe8eeb5dc5a1e8994dc9c1fff99efb2`로 일치합니다. 실측은 착수하지 않았습니다.

**A — 원장 정합·이전 지적 폐쇄: REVISE**

| 지적 | v5 판정 | 확인·잔여 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree 동일·최초 요청 6/6 동일 |
| MY-2 | closed | 잡음 폭의 확대·축소 방향 미확정 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정·자동 열위 제거 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | closed | 통합 fact=3·최신 실패는 N/A |
| MY-6 | partially | 6축·회차 보존 수정. 수치 검증 잔여: NC-3 |
| MY-7 | closed | 검사 배열·findings 보존·귀속은 추정 표시 |
| MY-8 | partially | 정상 분류 수정. 진입 실패의 코드 잔여: NC-1 |
| MY-9 | closed | A-a→A-b 순서가 러너 제어 흐름과 일치 |
| MY-10 | closed | 완료 구별·Workflow 거부·발주 거부 시 무차감 |
| MY-11 | closed | 소비 전 실호출 대조·dispatch별 이동 보존 명시 |
| MY-12 | closed | 성공·실패·대기 전 런과 외부 실행층 보존 |
| MY-13 | closed | 생산 원장은 운영 선택·증가량은 메모 보유 종결 런 수 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 |
| MZ-2 | closed | 축 0 별도 보존·첫 실행 판정 채택·N/A 처분 |
| MZ-3 | partially | 필수 스냅샷·결속 대조 수정. NC-2·3 잔여 |
| MZ-4 | partially | 실제 상수·예외 분류 수정. NC-1 잔여 |
| MZ-5 | closed | 로그에 없는 최신 synthesize 실패도 N/A |
| MZ-6 | closed | 중복 검사 행·추정 귀속·findings·escalations 확인 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 확인 |
| MZ-8 | closed | dispatch별 증거·상한·거부 시 회차 불변 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로를 호출 전에 거부 |
| NA-1 | closed | 실제 `LaneContractError` 뒤 최신 retry 선택·N/A |
| NA-2 | partially | 손상 조기 JSON 세 경로는 14. NC-1 잔여 |
| NA-3 | closed | 조회 무쓰기·확정 발주만 계수·충돌 무차감 |
| NA-4 | partially | 지정 결측 반례는 4. NC-2·3 잔여 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 사전 거부 |
| NA-7 | closed | 인용 부재 등의 판정 불가·표본 유지·재상신 명시 |
| NB-1 | partially | 기존 세 반례 모두 14. 실제 `enter`의 `SystemExit` 잔여 |
| NB-2 | closed | A,A,A,B 및 전건 검사·부분 기록 실패 처분 확인 |
| NB-3 | partially | 지정 반례 모두 4. 재독 경계·수치형 잔여 |

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕ는 재정 문언 이행**, **ⓖ는 §0′ 범위에 한정한 동일화 이행**으로 판단합니다. **ⓘ는 표본 단위 이행과 인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행과 후보 표시 재량**, **ⓝ는 판정 근거 부족 시 재상신하는 문언 이행**입니다.

`partial/read`와 비게시의 운영 범위도 원장과 맞습니다. G-12의 미집행을 해결했다는 보증으로 확대할 수는 없습니다.

**지적 목록 — MED 3건**

**NC-1 · MED — 실제 `enter`가 내는 진입 실패는 여전히 예외 경계를 빠져나간다.**

좌표: 메모 §2·§9 C; [구동 `enter`](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:61), [`cmd_read`](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:277).

`enter`는 worktree가 없으면 `fail()`→`SystemExit(2)`를 냅니다. `cmd_read`의 `except SystemExit: raise`가 이를 그대로 내보냅니다. **진입을 try 안으로 옮겼지만 실제 진입 실패 종류 하나를 명시적으로 제외했습니다.**

실제 `enter`를 유지하고 `REPO`·파일 존재 판정만 메모리에 대입했습니다.

```text
ACTUAL_ENTER_MISSING_WORKTREE 2 EXC_FILES 0
ACTUAL_ENTER_BAD_RUN 3 EXC_FILES 0
```

유효한 런 이름 `r0`의 worktree 부재도 **exit 2·예외 증거 없음**입니다. 메모의 “진입 실패=14”, “어떤 예외도 13/14”와 어긋납니다.

고치는 문안: **“`cmd_read` 내부의 `enter`가 발생시키는 `SystemExit`도 진입 실패로 기록하여 14로 변환하고, 최종 종료 호출만 예외 경계 밖에 둔다.”**

**NC-2 · MED — 스냅샷 검증 뒤의 재독·변환이 exit 4 경계 밖에 남아 있다.**

좌표: 메모 §5 ㉠·§9 D; [지표 `metrics`](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:109).

80행에서 SHA를 검증한 뒤, 109행에서 `sha(early_src)`로 **같은 파일을 다시 읽습니다. 이 재독은 try 밖**입니다. 검사 배열 변환도 다음 행에서 경계 밖으로 실행됩니다.

정상 판정서와 일치하는 sidecar를 공급한 결과:

```text
SECOND_SHA_PERMISSION ESCAPED PermissionError snapshot sha read
CHECKS_NULL ESCAPED TypeError 'NoneType' object is not iterable
```

첫 SHA 읽기 실패는 4로 고쳐졌지만, **두 번째 SHA 읽기 실패는 미포착**입니다. “읽기·해시·파싱·형태 검증이 하나의 exit 4 경계”라는 주장은 아직 성립하지 않습니다.

고치는 문안: **“스냅샷 바이트를 한 번 읽어 같은 바이트로 해시·파싱·출력을 구성하고, 검사 배열의 형태 검증과 변환까지 exit 4 경계 안에 둔다.”**

**NC-3 · MED — 불리언·음수 계수와 유효 범위 밖 Jaccard를 정상 지표로 수용한다.**

좌표: 메모 §5 ㉠·§9 D; [지표 수치 검사](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:100); `convergence.schema.json#$defs/convergence_detail`.

`isinstance(x, int)`는 Python의 `bool`도 받습니다. Jaccard 검사 역시 불리언을 수치로 받으며 유한성·범위를 검사하지 않습니다. 각 수정본에 맞는 sidecar SHA를 공급했습니다.

| 대입 | 결과 |
|---|---|
| `independent_count=[true,true]` | 수용·`na=[]` |
| `independent_count=[-1,-1]` | 수용·`na=[]` |
| `element-set.jaccard=true` | 수용·`na=[]` |
| `element-set.jaccard=2.0` | 수용·`na=[]` |
| `element-set.jaccard=NaN` | 수용·`na=[]` |

계약의 계수는 비음수 정수이며 Jaccard는 0~1입니다. 특히 **`[True,True] == [1,1]`과 `abs(True-1.0) <= 0`이 모두 참**이므로, 불리언이 실제 비교에서도 정상 계수·값으로 통과할 수 있습니다.

고치는 문안: **“계수 쌍은 불리언을 제외한 비음수 정수, Jaccard는 불리언을 제외한 유한한 0~1 수치만 허용하고 위반은 exit 4로 종료한다.”**

NC-2·3은 손상 입력에 대한 방어 반례입니다. 정상 러너가 그런 판정서를 생성한다는 주장은 아닙니다.

**B — 계측 커밋 셋: PASS, 확인한 정적 범위**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base↔각 팔은 `contracts/stages/read.yaml` **2 additions/2 deletions**뿐입니다.

절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였고 Sonnet aliases도 확인했습니다.

`d4e6ca2→6d92cad` 재실측:

| 파일 | additions/deletions |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py | 19/0 · 69/0 |
| **reader/lib/__init__.py** | **4/0** |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

기준 요청 **6/6 재렌더 바이트 동일**, 최초 분해 요청 필드도 동일했습니다. 반면 실제 `plan_decompose(..., attempt=1, defects=...)`에서는 소견이 본문에 들어가고 지문이 바뀌었습니다. 최초 요청 동일성을 후속 요청 전체로 확대하지 않은 v5의 한정은 맞습니다.

**C — 구동 v5: REVISE**

4차 지정 반례는 전부 닫혔습니다.

| 반례 | v5 결과 |
|---|---:|
| `enter`의 `OSError` | 14 |
| 엔진 예외 뒤 증거 `makedirs`의 `PermissionError` | 14 |
| 증거 쓰기 실패 + 종결 포인터 true | 14 |
| 손상 조기 JSON: 정상 반환 / LanePending / StageError 뒤 | 각각 14 |

정상 분류 0·10·11·12·13·14, 예외 뒤 종결 포인터 true→13/false→14, phase=full인 대기 모순→14를 확인했습니다.

발주 전건 검사도 수정됐습니다.

| 호출 | 종료 | 회차 | 새 파일 쓰기 |
|---|---:|---:|---:|
| A | 0 | 1 | 3 |
| A 재호출 | 14 | 1 | 0 |
| A 재호출 | 14 | 1 | 0 |
| B | 0 | 2 | 3 |
| C | 0 | 3 | 3 |
| D | 15 | 3 | 0 |

`lanes` 네 번 조회는 쓰기 0이었습니다. 뒤 좌표의 상한 초과도 앞 좌표를 기록하지 않고 15였습니다. args 기록 후 counter 기록 실패는 **14**였으며, 메모의 복구 규칙대로 args를 보존하고 counter를 올린 뒤 다음 발주가 c2로 진행됐습니다. **NB-2는 closed**입니다.

스냅샷 함수는 축 0 문서를 별도 보존하고 최초 실행 attempt 1을 유지했습니다. `_next_dispatch`는 현재 파일에 없으며 계수는 `cmd_dispatch`로 이동했습니다. 잔여는 NC-1입니다.

**D — 지표 v5: REVISE**

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다. 조기 검사 2행·완주 13행·findings 0도 일치했습니다.

4차 지정 입력인 **dependent_count 삭제, element-set.jaccard 삭제, 최상위 null, axes null 원소, 축 중복, 첫 읽기 PermissionError는 전부 exit 4**였습니다. run_id·phase·executed 타입·SHA 불일치도 4였습니다.

실제 `_dispatch`·`FileLaneAdapter`·`load_response`에 깨진 retry 응답을 공급했습니다.

```text
ACTUAL_MALFORMED_DISPATCH LaneContractError LOG_ROWS 6
MALFORMED_LATEST_RETRY read-a/synthesize/retry-1/batch-0 None False False
```

로그 행이 없는 최신 디스크 좌표를 선택하고 `synth_counts=None`으로 처리합니다. 이전 성공값으로 후퇴하지 않습니다. N/A→판정 불가·재상신 처분도 명시돼 있습니다. 잔여는 NC-2·3입니다.

**E — 발췌 v4: PASS, 설계·함수 확인 범위**

`ex1`·`ex2` 생성 명령은 실행하지 않았습니다. 지정 함수들을 import하여 메모리에서 확인했습니다.

- 자기 대조 **27/27**, 후보 풀 역순에서도 동일.
- 5→1 병합 결과: `[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]`.
- 표본: **CL-2·4·7·9·12·14·16·19·21·24**.
- 표본의 인용 locator **27/27 해소**.

`anchor_state`·`search_note` 표시와 판정 불가·표본 유지·보류/재상신 규칙은 원장과 어긋나지 않습니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

본문을 Node에서 실행하고 `agent/pipeline`을 대체했습니다. `toString`·`constructor`·`/./`·`//`·`..`·미지 effort·중복 좌표/dispatch·요청/응답 중복·교차·좌표 불일치는 모두 **호출 0회에서 거부**됐습니다.

정상 입력은 기대 모델·effort로 전달됐습니다. true/false/null 보고 세 건에서 `wrote_true=1`이고, null 행에는 run·lane_id·dispatch_id가 남았습니다. 소비 전 실호출 확인과 이동 보존 절차도 명시돼 있습니다.

**G — 결정 공백: REVISE**

새로운 Owner 재정이 필요한 선택지는 찾지 못했습니다. 그러나 **진입 실패의 2/3, 검증 후 미포착 예외, 잘못된 수치의 정상 수용**이 선등록한 오류 처분과 다릅니다. NC-1~3을 닫기 전에는 이 메모의 종료·추출 규칙대로 실측을 완결한다고 판정할 수 없습니다.

**검증 경로**

모든 cwd는 지정 사본입니다. `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`이며, 메모리 시험은 전경 `-c`로 실행했습니다.

| 명령·검증 경로 | 마지막 출력 또는 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `f21236d184678f49b92f7786bbfc4676fe9bbf2f` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `29578689e62b4892…f99efb2  bundle/T40-MEASURE-DESIGN.md` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base↔R1/R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` — 위 표 재계수 |
| `git diff --stat origin/t40-base HEAD -- engine reader/lib contracts` | 빈 출력 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}`, exit 0·`na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`·exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`·exit 4 |
| `PY -c '…구동 반환·gate·pointer·쓰기 대체…'` | `DRIVE_READ_MEMORY_ONLY_COMPLETE` |
| `PY -c '…실제 cmd_dispatch·dict/StringIO 파일 대체…'` | `DISPATCH_MEMORY_ONLY_COMPLETE` |
| `PY -c '…스냅샷과 일치 sidecar·읽기 오류 대입…'` | `METRICS_SNAPSHOT_MEMORY_ONLY_COMPLETE` |
| `PY -c '…git show blob 재렌더·발췌 함수…'` | `NO_EXCERPT_GENERATOR_EXECUTED_ALL_CHECKS_IN_MEMORY` |
| `node -e '…Workflow 본문·agent/pipeline 대체…'` | `WORKFLOW_BODY_MEMORY_ONLY_NO_REAL_AGENT_CALLS` |
| `PY -c '…snapshot·실제 _dispatch·봉투 stdout 검증…'` | `SNAPSHOT_LATEST_ENVELOPE_MEMORY_ONLY_COMPLETE` |
| 봉투 미리보기→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**[미검증]**

- **설계 메모 v3 원본은 제공 bundle과 조회한 Git 이력에서 찾지 못했습니다.** v4·v5와 3차 도전·처분 기록을 대조했습니다. 이전 스크립트 원본도 없어 발췌·Workflow의 **v4 대비 바이트 무변경**은 증명하지 못했습니다.
- 실제 Workflow 호출·문맥 격리·transcript/journal 형식·거부물 이동·동시 쓰기는 실행하지 않았습니다.
- `read.run` 전체 재개와 source 실행·생산 원장 기록은 하지 않았습니다. 구동 시험은 엔진 반환/예외·파일 접근을 대체했고, 최신 통합 실패 시험은 실제 `_dispatch`와 파일 어댑터를 사용했습니다.
- 외부 원천 TXT·도면은 열지 않았습니다. 사본 원천은 298,507 B·SHA `64d5d627…154e`, 메타 차이는 `[]`; 원본 SHA와 도면 20개는 보관 source-report의 기록까지 확인했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 §1·§4·§5 포함 전문, 좌석 결정문 §17 추기 포함, MY·MZ·NA·NB 도전 문서, SPEC §8.4 지정 행, T14·T17·T38.
- 계약: `run-kinds.yaml`, `stages/read.yaml` 지정 블록, `approval-envelope.schema.json`, `convergence.schema.json`.
- 대상: 메모 v4·v5, 구동·지표·발췌·Workflow·봉투 스크립트 5종.
- 구현: `read.py` 지정 흐름·LaneJournal·종결/봉투 함수, `source.py#run`, `lanes/plan.py`·`contract.py`·`file_adapter.py`, `paths.py`, `convergence.py`·`run_checks.py`·`report.py` 관련 부분.
- 실물: 기준 run.yaml·source-report·patent.md·material-spec·조기/완주 판정서·lane-log·요청 JSON/MD 6개·통합 응답, 지정 커밋의 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았고 배경 작업도 시작하지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다.