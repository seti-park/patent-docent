# 독립 감수 원문 — M1b 설계 도전 4차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v4 · 판정 REVISE(HIGH 1 · MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `a0c2810563c47ca3a964099bee0364b5c29d2dfc03fd732a18ec2907f81f0c23` · 16908 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v4/`(첫 기동 05:59:49 는 발주문의 지적 ID 접두가 `NA-*` 로 남아 있어 1분 뒤 중단(EXIT=143 · `…-aborted-idfix/`) · 접두 `NB-*` 로 고쳐 06:01:01 재기동).

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 06:01:01 → 06:11 · **USAGE = input 2,532,869(cached 2,371,456) · output 17,151(reasoning 2,538)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `8c58170` · `bundle/T40-MEASURE-DESIGN.md` v4 sha256 `9676eaeb…6659` · v3 동봉 · 스크립트 v4 5종). 폐쇄 = **MY closed 10 · partially 3 / MZ closed 6 · partially 3 / NA closed 4 · partially 3 · open 0**. 닫힌 것: NA-1(깨진 retry 응답 → 최신 시도 N/A · 실제 `_dispatch` 재현) · NA-5 · NA-6(요청/응답 중복·교차·좌표 결속 거부 · 호출 0) · NA-7(발췌 2 판정 불가 처분 = 타당 · §8 ⓝ 재정 문언 이행 인정) · 조기 JSON 손상 세 경로 → 14 · phase=full 모순 → 14 · `lanes` 조회 무변경. B(계측 커밋 · 6/6 재렌더 동일) · E(발췌) · F(Workflow) = PASS(확인 범위).

**판정 = REVISE · 3건(HIGH 1 · MED 2) · 기각 0 · 전부 발주자 귀책 · BLOCKER 0.** **NB-1 HIGH**: 「전 구간 단일 예외 경계」가 `enter(run)`(try 밖)과 `_record_exception` 의 `makedirs`·번호 계산(자체 try 밖)을 덮지 못함 — enter 의 OSError 미포착 · 증거 makedirs PermissionError 미포착 · 증거 쓰기 실패 + 종결 포인터 true 가 13(선언은 14). **NB-2 MED**: `cmd_dispatch` 가 개별 args·counter 를 먼저 쓰고 배치 파일 충돌을 뒤에 검사 → 같은 배치 이름 재실행 2회로 exit 14 인데 회차 1→3 소진 · 이름 바꾼 발주가 exit 15. **NB-3 MED**: 6축 id 일치가 지표 존재를 보증하지 않음(`dependent_count` 삭제 · `element-set.jaccard` 삭제 → 수용 `na=[]`) · 최상위 null · axes null 원소 · 읽기 PermissionError → 미포착(exit 4 밖). 그 외 메모 §0′ 열거에 `reader/lib/__init__.py` 4/0 누락(B 절 관찰).

지적 열거 = NB-1, NB-2, NB-3

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 3**. **전부 수용 → 설계 메모 v5 + 구동·지표 스크립트 v5 → M1b 5차 도전(지적 `NC-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**MY 10 closed·3 partially / MZ 6 closed·3 partially / NA 4 closed·3 partially입니다. open은 없습니다.** 최신 통합 실패의 N/A 처리, 세 경로의 조기 JSON 손상 처리, Workflow 사전 거부, 발췌 2의 판정 불가 처분은 개선됐습니다. 그러나 **예외 경계·실패한 발주의 회차 계수·스냅샷 결측 검증**에 실행 반례가 남습니다.

사본 마커의 path·pin·order·disposable이 지정값과 일치했습니다. HEAD는 `8c58170613915f1bebd1af7741f1110f543f8488`, 메모 SHA-256은 `9676eaeb3430a4bc7f28c82578d854554a954620a99b184680b6749602ab6659`입니다.

**A — 원장 정합·폐쇄표: REVISE**

| 1차 | 판정 | v4 확인·잔여 |
|---|---|---|
| MY-1 | closed | 고정 핀·기준 절차 tree 동일·최초 요청 6개 재렌더 동일 |
| MY-2 | closed | 잡음 폭의 확대·축소 방향을 미확정으로 정정 |
| MY-3 | closed | 기준 27단위 고정·후보 재사용·Owner 명시 판정·자동 열위 없음 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부·청구항별 집계 |
| MY-5 | closed | 통합 fact=3·최신 실패 시 이전 통합값으로 후퇴하지 않음 |
| MY-6 | partially | 회차·6축·스냅샷 보존 개선. 계수·축 값 결측 검증 잔존: NB-3 |
| MY-7 | closed | 검사 배열·findings 보존·실행 귀속은 추정으로 표시 |
| MY-8 | partially | 정상 분류와 phase 모순 수정. 예외 경계 잔존: NB-1 |
| MY-9 | closed | 실제 러너의 A-a→A-b pending 순서 재확인 |
| MY-10 | partially | 조회 무변경·Workflow 거부 개선. 실패한 발주의 회차 소진: NB-2 |
| MY-11 | closed | 소비 전 실호출 대조·dispatch별 이동 보존 절차 명시 |
| MY-12 | closed | 실패·대기 포함 전 런과 외부 실행층 보존 명시 |
| MY-13 | closed | 생산 원장은 운영 선택·증가량은 메모 보유 종결 런 수 |

| 2차 | 판정 | v4 확인·잔여 |
|---|---|---|
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 제시 |
| MZ-2 | closed | 축 0 별도 보존·첫 실행 판정 채택·결측 재상신 명시 |
| MZ-3 | partially | 필수 스냅샷·결속 대조 개선. 판독·형태·값 검증 잔존: NB-3 |
| MZ-4 | partially | 러너 상수·정상 분류 일치. 예외 경계 잔존: NB-1 |
| MZ-5 | closed | 디스크의 최신 시도에 로그 행이 없으면 N/A |
| MZ-6 | closed | 중복 검사 행·추정 귀속·findings·escalations 확인 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 한정 확인 |
| MZ-8 | partially | 고유 ID·상한 구현. 실패한 발주도 예산 차감: NB-2 |
| MZ-9 | closed | `toString`·`constructor`·비정규 경로·중복 사전 거부 |

| 3차 | 판정 | v4 확인·잔여 |
|---|---|---|
| NA-1 | closed | 실제 `LaneContractError` 뒤 로그 6행 유지→최신 retry N/A |
| NA-2 | partially | 손상 JSON 세 경로·full/대기 모순 수정. NB-1 잔존 |
| NA-3 | partially | `lanes` 4회 조회 쓰기 0·기존 args 불변. NB-2 잔존 |
| NA-4 | partially | run_id·5축·빈 sidecar·깨진 JSON 거부. NB-3 잔존 |
| NA-5 | closed | 다중 기록 불가능 주장을 삭제. 실제 러너에서 다중 기록 재확인 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치가 호출 전에 거부됨 |
| NA-7 | closed | search_note 표시·대조 불가 처분·표본 유지·보류/재상신 명시 |

§8의 **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕ는 재정 문언 이행**, **ⓖ는 §0′에 한정한 동일화 이행**으로 판단합니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정의 이행과 후보 표시 재량**입니다.

**ⓝ도 재정 문언 이행으로 인정합니다.** 대조할 인용이 없는 표본을 임의의 정답·오답으로 만들거나 교체하지 않고, 채택 근거 부족으로 재상신하는 처분입니다. 오답 임계를 바꾸는 처분으로 볼 근거는 찾지 못했습니다.

**지적 목록 — HIGH 1 · MED 2**

**NB-1 · HIGH — ‘전 구간 단일 예외 경계’가 진입과 예외 기록 실패를 덮지 못한다.**

좌표: 메모 §2·§9 C; [t40_drive.py:cmd_read](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:225), [_record_exception](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:215).

`enter(run)`은 바깥 `try`보다 먼저 실행됩니다. `_record_exception()`의 `makedirs`·번호 계산도 자체 `try` 밖입니다. 바깥 예외 처리부가 다시 `_record_exception()`을 호출하므로, 증거 디렉터리 오류가 반복되면 미포착 예외로 끝납니다.

쓰기 함수와 진입·엔진 결과를 메모리 대입한 결과:

| 대입 | 실제 결과 |
|---|---|
| `enter`에서 `OSError` | **미포착 OSError** |
| 엔진 `StageError` 뒤 증거 `makedirs`에서 `PermissionError` | **미포착 PermissionError** |
| 엔진 `StageError`·종결 포인터 true·예외 파일 쓰기 실패 | **exit 13** — 선언은 증거 기록 실패=14 |

반면 **조기 JSON `{broken`은 정상 반환·LanePending·StageError 뒤 모두 exit 14**였습니다. NA-2의 그 반례는 닫혔지만, “exit 1 경로 없음”과 “증거 기록 실패=14”는 아직 성립하지 않습니다.

고치는 문안: **“진입부터 예외 기록까지 경계 안에 두고, 기록 함수의 디렉터리 생성·번호 계산·쓰기는 재예외를 내지 않으며, 증거 기록 실패가 한 번이라도 있으면 종료 코드는 14로 고정한다.”**

**NB-2 · MED — 기존 배치 파일 충돌을 거부하면서 이미 회차와 새 args를 기록한다.**

좌표: 메모 §2·§3·§8 ⓜ; [t40_drive.py:cmd_dispatch](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:122).

개별 dispatch args와 counter를 먼저 쓰고, **그 뒤에** `lanes-<run>-<batch>.json`의 존재를 확인합니다. 같은 배치 이름으로 명령을 다시 실행하면 exit 14지만, 사용할 배치 파일에 반영되지 않은 발주가 예산에 포함됩니다.

실제 `cmd_dispatch`의 파일 접근만 dict/StringIO로 대체했습니다. pending 좌표는 하나로 유지했습니다.

| 호출 | 종료 | 누적 회차 | 새 개별 args |
|---|---:|---:|---:|
| `dispatch r0 A` | 0 | 1 | 1 |
| `dispatch r0 A` | **14** | **2** | **1** |
| `dispatch r0 A` | **14** | **3** | **1** |
| 안내대로 이름 변경: `dispatch r0 B` | **15** | 3 | 0 |

원래 `lanes-r0-A.json`은 c1 그대로였습니다. **두 번의 거부가 추가 호출 예산을 전부 소진했습니다.** `lanes` 조회 네 번은 쓰기 0으로 확인했으므로 조회 분리는 해결됐습니다.

고치는 문안: **“배치 파일·개별 args 충돌과 좌표별 상한을 모두 검사한 뒤 발주를 확정하며, 거부된 발주는 회차를 소비하지 않고 부분 기록 실패의 복구 처분도 고정한다.”**

**NB-3 · MED — 6축 이름의 일치가 필수 지표의 존재를 보증하지 않으며, 일부 판독 오류는 exit 4 밖으로 빠진다.**

좌표: 메모 §5 ㉠·§9 D; [t40_metrics.py:metrics](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:79), `axes_of`.

정상 기준 판정서를 복제해 수정하고 **그 수정본에 맞는 sidecar SHA**를 공급했습니다.

| 입력 | 실제 결과 |
|---|---|
| `dependent_count` 삭제, 6축 ID 유지 | **수용·`na=[]`·dependent 계수 `None`** |
| `element-set.jaccard` 삭제, 6축 ID 유지 | **수용·`na=[]`** |
| 스냅샷 JSON 최상위 `null` | **미포착 AttributeError** |
| axes에 `null` 원소 추가 | **미포착 AttributeError** |
| SHA 계산 단계에서 스냅샷 읽기 `PermissionError` | **미포착 PermissionError** |

run_id 부재·타 런·phase 불일치·executed=false·5축·빈 sidecar·SHA 불일치·문법이 깨진 JSON은 모두 exit 4였습니다. 남은 반례는 **손상·결측 입력에 대한 추출기 방어 시험**이며, 정상 러너가 이런 판정서를 생성한다는 주장은 아닙니다.

고치는 문안: **“스냅샷의 읽기·해시·형태 검증을 하나의 exit 4 경계로 묶고, 축 ID뿐 아니라 실행 여부의 타입·축 중복·비교에 필요한 계수 쌍과 수치·status의 존재 및 타입도 검증한다.”**

**B — 계측 커밋·동일성: PASS, 확인한 정적 범위**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base↔각 팔은 `read.yaml` **2 additions/2 deletions**뿐입니다. 절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.

`lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였습니다. 기준 요청서 **6/6 바이트 동일**, 최초 분해 계획의 요청 필드도 동일했습니다.

`d4e6ca2→6d92cad` 재실측:

| 파일 | additions/deletions |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py | 19/0 · 69/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |
| reader/lib/__init__.py | **4/0** |

메모의 주요 수치는 맞습니다. 마지막 `reader/lib/__init__.py` 변경은 메모 열거에 빠져 있습니다.

동일성을 후속 요청으로 확대할 수 없습니다. 실제 `plan_decompose(..., attempt=1, defects=...)`에서 **소견이 렌더 본문에 들어가고 입력 지문이 바뀜**을 확인했습니다. 검사·예산 차이는 재시도 발생 여부와 그 소견에 닿습니다.

**C — 구동: REVISE**

분류기의 정상 0·11·12·13·14, 예외 뒤 종결 포인터 true→13/false→14, **phase=full인 대기 모순→14**를 확인했습니다. 실제 러너에서 A-a→A-b→분해 retry 순서도 재현했습니다.

네 번째 호출의 조기 기록은 실제로 `(False,0,0) → (True,1,6)`이었습니다. 스냅샷 함수는 축 0을 별도 보존하고 최초 실행 attempt 1을 유지했습니다. `_next_dispatch`는 v4에서 제거됐으며 발주 계수는 `cmd_dispatch`로 이동했습니다. 잔여는 NB-1·2입니다.

exit 14는 엔진 비종결을 뜻하지 않습니다. T38의 종결 근거 세 가지는 러너 `_run_is_terminated`가 별도로 판정합니다.

**D — 지표: REVISE**

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다. 조기 검사 2행·완주 13행·findings 0도 일치했습니다.

실제 `_dispatch`·`FileLaneAdapter`·`load_response`에 깨진 retry 응답을 공급한 결과:

```text
ACTUAL_MALFORMED_DISPATCH LaneContractError LOG_ROWS 6
MALFORMED_LATEST_RETRY read-a/synthesize/retry-1/batch-0 None False False
```

최신 시도의 로그 행이 없어도 디스크 좌표를 선택하고 `synth_counts=None`으로 처리합니다. **NA-1은 닫혔습니다.** 잔여는 NB-3입니다.

**E — 발췌: PASS, 확인한 설계·함수 범위**

발췌 1의 메모상 규칙은 v3와 같습니다. 기준 자기 대조 **27/27**, 후보 풀 역순에서도 결과 동일, 5→1 병합에서는 다섯 단위 모두 `M20`을 후보로 받았습니다. 자동 열위는 없습니다.

표본은 **CL-2·4·7·9·12·14·16·19·21·24**, 기준 표본 locator는 **27/27 해소**됐습니다. M63을 no-anchor 상태로 바꾼 자료는 **스키마 오류 0·coverage pass**였습니다. v4 본문은 anchor_state·search_note를 표시하고 인용 부재·단락 미해소·접지 부재를 판정 불가로 다룹니다. **보류·재상신은 타당하며 NA-7은 닫혔습니다.**

**F — Workflow: PASS, Node 대체 실행 범위**

`toString`·`constructor`·`/./`·`//`·`..`·미지 effort·중복 좌표·중복 dispatch·요청/응답 중복·교차·좌표 불일치는 모두 **agent 호출 0회에서 거부**됐습니다. 정상 두 입력은 기대 모델/effort로 전달됐고, wrote=false는 wrote_true에 포함되지 않았습니다. null 보고에는 run·lane_id·dispatch_id가 남았습니다.

실호출의 model·effort 확인과 거부물 이동 보존은 절차상 명시돼 있습니다. 실제 Workflow 증거 형식과 이동 실행은 아래 미검증 범위입니다.

**G — 결정 공백: REVISE**

발췌 2의 처분 공백은 닫혔습니다. 그러나 **실패한 발주의 부분 기록·소진 회차를 어떻게 처리할지**, **필수 지표가 없는 스냅샷을 어떻게 차단할지**가 구현과 선언 사이에 남습니다. NB-1~3을 해결하기 전에는 실측 착수 조건을 충족하지 못합니다.

**검증 경로**

모든 cwd는 지정 사본입니다. `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 전경 `PY -c '…'`로 실행했고, 시험 코드는 파일로 저장하지 않았습니다.

| 명령·실행 경로 | 마지막 출력 줄 또는 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `8c58170613915f1bebd1af7741f1110f543f8488` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `9676eaeb3430a4bc…ab6659  bundle/T40-MEASURE-DESIGN.md` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` — 위 표 재계수 |
| `git diff --stat origin/t40-base HEAD -- engine reader/lib contracts` | 빈 출력 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 줄 `}`, exit 0·`na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`·exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`·exit 4 |
| `PY -c '…cmd_read/classify/실제 snapshot·dispatch 메모리 대입…'` | `DRIVE_MEMORY_ONLY_COMPLETE` — NB-1·2 출력 포함 |
| `PY -c '…metrics 입력·실제 _dispatch/파일 어댑터 대입…'` | `METRICS_MEMORY_ONLY_COMPLETE` — 최신 retry N/A·NB-3 출력 포함 |
| `PY -c '…git show 절차 blob→render_request_md; candidates/comp_texts_fn/sample_indices…'` | `NO_EXCERPT_GENERATOR_EXECUTED_ALL_CHECKS_IN_MEMORY` |
| `node -e '…Workflow 본문·agent/pipeline 대체…'` | `WORKFLOW_BODY_MEMORY_ONLY_NO_REAL_AGENT_CALLS` |
| `PY -c '…실제 read.run·snapshot·봉투 stdout 검증…'` | `RUNNER_SNAPSHOT_ENVELOPE_MEMORY_ONLY_COMPLETE` |
| 봉투 `--write` 없는 stdout→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |

**[미검증]**

- 외부 스테이징 TXT·도면 20개는 열지 않았습니다. 사본 원천 SHA는 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`, PATENT_META 차이는 `[]`였습니다.
- 실제 Workflow 호출·문맥 격리·transcript/journal 이벤트 형식·실제 이동 보존·동시 쓰기는 실행하지 않았습니다.
- 실제 러너 시험은 진입·종결 가드, 출력·원장 함수를 대체했습니다. 실제 source/read 재개나 생산 원장 기입 성공 시험은 아닙니다.
- **v3 발췌 스크립트 원본은 제공 사본·HEAD에 없어 코드 바이트 무변경은 검증하지 못했습니다.** 메모의 발췌 1 규칙 무변경과 v4 함수의 동작을 확인했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 원장 전문, `D-20260905-02-pdm2b-seats.md` §17 추기, MY·MZ·NA 도전 문서, SPEC §8.4 지정 행, T14·T17·T38.
- 계약: `run-kinds.yaml`, `stages/read.yaml` 지정 블록, `approval-envelope.schema.json`, 관련 material-spec 스키마.
- 대상: 설계 메모 v3·v4, 구동·지표·발췌·Workflow·봉투 스크립트 5종.
- 구현: `read.py`·`source.py` 지정 흐름, `lanes/plan.py`·`contract.py`·`file_adapter.py`, `paths.py`, `read_view.py`, `convergence.py`·`run_checks.py`·`report.py`·`coverage.py` 관련 함수.
- 실물: 기준 run.yaml·source-report·patent.md·material-spec·조기/완주 판정서·lane-log·요청 JSON/MD 6개·분해/통합 응답·계속 봉투, 지정 커밋의 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.