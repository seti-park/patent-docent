# 독립 감수 원문 — M1b 설계 도전 3차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v3 · 판정 REVISE(HIGH 3 · MED 3 · LOW 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `8ba0783ee4176a43ac73de50d379ed450e4eb7d350fce4a63c70f38a32e146af` · 21397 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v3/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 05:38:02 → 05:51 · **USAGE = input 2,754,881(cached 2,587,776) · output 22,289(reasoning 6,414)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `71ed982` · `bundle/T40-MEASURE-DESIGN.md` v3 sha256 `f0e1008d…2cc7` · v2 동봉 · 스크립트 v3 5종). 폐쇄 = **MY closed 9 · partially 4 · MZ closed 3 · partially 6**(27 단위 고정 · 자동 열위 제거 · 절차 동일성·부모 대조 · 검사 배열 · 상수는 닫힘). 도전자가 실제 러너로 확인한 것: pending 순차 공급 신규 런에서 재시도 뒤 한 호출 안 조기 판정서 2회 기록(축 0 → 6축 · 최초 유효 스냅샷 손실 없음) · 기준 요청 6개 재렌더 동일 · `plan_decompose(attempt=1, defects=…)` 가 소견을 요청 본문·지문에 넣음 · 기준 계수 전건 일치 · 발췌 1 자기 대조 27/27 · 5→1 병합 후보 제시 · locator 27/27.

**판정 = REVISE · 7건(HIGH 3 · MED 3 · LOW 1) · 기각 0 · 전부 발주자 귀책 · BLOCKER 0.** **NA-1 HIGH**: `_dispatch` 는 `LaneStaleResponseError` 만 거부 행을 남기고 깨진 JSON·스키마 위반(`LaneContractError`)은 행 없이 나가므로 「lane-log 마지막 synthesize 행」이 마지막 시도가 아님 → 이전 정상 응답(지문 일치)으로 후퇴. **NA-2 HIGH**: 스냅샷 호출이 예외 경계 밖(정상 반환 뒤·except 본문 안) → 조기 JSON 손상 시 세 경로 모두 exit 1 · `classify` 가 `phase=full` 모순 입력을 11 로. **NA-3 MED**: 회차 계수 시점이 `agent()` 호출이 아니라 미도착 목록 생성 → 완료 조회 3회로 실호출 0 인데 exit 15 · `lanes-r0.json` 덮임. **NA-4 MED**: `run.yaml` run_id 부재 시 타 런 판정서 통과 · 5축 판정서 통과 · 빈 sidecar/깨진 JSON 은 exit 4 아님. **NA-5 LOW**: 「신규 런은 한 호출 안 두 번 기록 없음」 주장은 틀림(재진입 재연으로 2회 기록 · 손실은 없음). **NA-6 MED**: 요청 경로 중복·요청/응답 교차 충돌 미거부. **NA-7 HIGH**: 합법적 `no-anchor-found`(`spec_refs=[]` · `search_note`) 표본의 채점 처분 공백 — 발췌 2 가 search_note 미표시 · 판정 칸 조응/오답만 · anchor 분포 비교가 그 경로를 항상 막지 않음(B=0 · R0=1 · R2=1 통과).

지적 열거 = NA-1, NA-2, NA-3, NA-4, NA-5, NA-6, NA-7

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 2**. **전부 수용 → 설계 메모 v4 + 스크립트 v4 → M1b 4차 도전(지적 `NB-*`)**. 게이트가 ⑽ ⓑ 자문 트리거를 명기하지 않았다(3회 REVISE · 매회 다수 폐쇄 · 잔여는 구현 견고성) — 기록.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**MY: closed 9 · partially 4. MZ: closed 3 · partially 6.** 27단위 고정과 자동 열위 제거는 닫혔습니다. 그러나 마지막 통합 실패의 이전 값 후퇴, 예외 분류 누락, 인용 없는 종속항 표본의 처분 공백이 남았습니다. 이 메모대로 실측을 시작할 수 없습니다.

대상 확인: 마커 path·pin·order·disposable 일치, HEAD `71ed982f69bcf850156d0294fa58dc6301c68f85`, 메모 SHA-256 `f0e1008d4583d011a828460f4155b7ec7e563f6ba9f2cd34dbf4a3cebe772cc7`.

**A — MY·MZ 폐쇄표와 원장 정합**

폐쇄는 원 지적의 범위를 기준으로 판정했습니다. 새로 발견한 별도 문제는 구별해 적었습니다.

| 1차 | 판정 | 근거·잔여 |
|---|---|---|
| MY-1 | closed | 절차 tree 동일, R0 고정 핀, 두 팔의 부모·변경 범위 확인 |
| MY-2 | closed | 잡음 폭 확대·축소 방향 미확정으로 정정 |
| MY-3 | closed | 기준 27단위 고정, 후보 재사용 가능, Owner 명시 판정, 자동 열위 제거 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부·청구항 단위 집계 확인. 인용 부재는 별도 NA-7 |
| MY-5 | partially | 수확 fact 혼입은 해결. 기록되지 않은 마지막 실패에서 이전 통합 값 선택: NA-1 |
| MY-6 | partially | 6축·계수 쌍·실행된 최초 스냅샷은 개선. 결속 검증 및 설명 잔여: NA-4·5 |
| MY-7 | closed | 배열·findings 보존, 실행 귀속을 추정값으로 구별 |
| MY-8 | partially | 정상 분기 개선. 스냅샷 예외가 종료 코드 밖으로 빠짐: NA-2 |
| MY-9 | closed | 실제 pending 순서 A-a→A-b 확인 |
| MY-10 | partially | wrote=false·null 구별과 응답 중복 거부는 해결. 조회/발주·요청 경로 잔여: NA-3·6 |
| MY-11 | closed | 소비 전 실호출 확인, dispatch별 이동 보존으로 수정. 실제 Workflow 기록 형식은 미검증 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 전부 보존하도록 범위 수정 |
| MY-13 | closed | 생산 원장을 운영 선택으로 명시, 증가량을 메모 보유 종결 런 수로 수정 |

| 2차 | 판정 | 근거·잔여 |
|---|---|---|
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 병합 후보 제시. 자동 열위 없음 |
| MZ-2 | partially | 축 0 제외·N/A 처분은 해결. 신규 런의 다중 기록 불가능 주장은 반증됨: NA-5 |
| MZ-3 | partially | 정상적인 부재·4항 불일치는 exit 4. 손상 입력·검증 전제 부재는 미완: NA-4 |
| MZ-4 | partially | 상수와 정상 예외 분류 개선. 예외 처리 바깥의 스냅샷 실패 잔존: NA-2 |
| MZ-5 | partially | 명시된 mismatch·rejected·digest 불일치는 N/A. 로그에 없는 마지막 실패는 후퇴: NA-1 |
| MZ-6 | closed | 검사 배열·추정 귀속·findings·실제 escalations 경로 확인 |
| MZ-7 | closed | 부모 `6d92cad` 대조와 주요 numstat 일치, 동일성 범위 한정 |
| MZ-8 | partially | 고유 ID·거부물 경로·상한은 있음. 조회 횟수와 호출 횟수 혼동: NA-3 |
| MZ-9 | partially | `toString`·`constructor`·`/./` 반례 거부. 요청 경로 중복·교차 충돌 통과: NA-6 |

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕ는 재정 문언 이행**, **ⓖ는 §0′에 한정한 동일화 이행**, **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정의 이행과 후보 표시 재량**으로 봅니다. 이 분류 자체를 뒤집을 근거는 찾지 못했습니다. 다만 그 분류가 NA-7의 미정 처분까지 승인하지는 않습니다.

**지적 목록 — HIGH 3 · MED 3 · LOW 1**

**NA-1 · HIGH — 마지막 synthesize 실패가 로그에 없으면 이전 정상 응답으로 다시 후퇴한다.**

좌표: 메모 §5 ㉣·§9 D; [t40_metrics.py:metrics](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:119), `engine/stages/read.py:_dispatch`, `FileLaneAdapter.dispatch`, `load_response`.

v3는 **lane-log의 마지막 synthesize 행**을 마지막 실제 시도로 간주합니다. 하지만 `_dispatch`가 거부 행을 추가하는 예외는 `LaneStaleResponseError`입니다. 깨진 JSON·스키마 위반 등의 `LaneContractError`는 행을 추가하지 않고 나갑니다.

실제 `_dispatch`와 파일 어댑터에 `synthesize/retry-1/batch-0`의 깨진 JSON을 메모리로 공급했습니다. 예외 뒤 로그는 6행 그대로이며 마지막 행은 `synthesize/batch-0`였습니다. 이를 추출기에 공급하자 다음처럼 나왔습니다.

`MALFORMED_LATEST_RETRY_REPORTS_OLD_SYNTH read-a/synthesize/batch-0 {'fact': 3, 'implication': 20, 'positioning': 7, 'figure_note': 10} True`

이는 단순한 지문 문제도 아닙니다. **이전 응답의 지문은 정확히 일치합니다.** 최신 실패가 선택 집합에서 빠지는 문제입니다.

고치는 문안: **“마지막 synthesize 시도는 요청·dispatch·예외 증거와 lane-log를 함께 대조해 정하고, 최신 시도의 적격 소비를 증명하지 못하면 ㉣은 N/A이며 이전 계수는 참고로만 싣는다.”**

**NA-2 · HIGH — ‘모든 예외 포착’이 스냅샷 처리에는 적용되지 않는다.**

좌표: 메모 §2 종료 코드; [t40_drive.py:cmd_read](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:202), `snapshot_first_early`, `classify`.

스냅샷 호출은 정상 반환 뒤에는 `try` 밖에 있고, `LanePending` 및 일반 예외 분기에서는 `except` 본문 안에 있습니다. 그곳의 새 예외는 같은 `except BaseException`이 잡지 못합니다.

조기 JSON을 `{broken`으로 대입하자 **정상 반환·LanePending·StageError 뒤 세 경로 모두 `JSONDecodeError`가 미포착**됐습니다. 특히 기존 스냅샷이 이미 있어도 현재 파일을 먼저 파싱하므로 실패합니다. 선언한 13/14 대신 프로세스 exit 1로 빠지는 경로가 남습니다.

또 `classify`는 `phase`를 출력만 합니다. 합성 모순 입력 `phase=full, status=halt, terminated=false, awaiting=convergence_continue, blocked_by=convergence-escalation`을 **11**로 분류했습니다. 이는 정상 러너 도달 경로를 입증한 시험은 아니지만, “상태 모순=14”라는 분류기의 약속에는 미달합니다.

고치는 문안: **“진입·엔진 호출·스냅샷·후처리를 하나의 예외 경계로 감싸고, 증거 기록 실패도 별도 진단하며, 11은 조기 반환과 대기·게이트 근거가 일관될 때만 허용한다.”**

**NA-3 · MED — 완료 확인용 `lanes` 조회가 호출 예산을 소진한다.**

좌표: 메모 §3 완료 판정·dispatch 상한·§6 args 보존; [t40_drive.py:_next_dispatch](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:97), `pending_lanes`, `write_lanes`.

계수 시점은 `agent()` 호출이 아니라 **미도착 목록 생성**입니다. 메모는 같은 `lanes` 명령을 완료 확인에도 사용합니다. 따라서 조회 결과를 바로 발주에 사용할지, 확인 뒤 다시 발주 목록을 만들지에 따라 사용 가능한 호출 수가 달라집니다.

쓰기만 메모리로 대체한 실제 `write_lanes`를 네 번 호출하자 **실제 agent 호출 0회에서 c1→c2→c3→exit 15**가 나왔습니다. 마지막 출력은 “호출 3회”였고 `lanes-r0.json`은 `[]`로 덮였습니다. 세 번의 목록 생성을 세 번의 실호출 증거로 쓸 수 없습니다.

고치는 문안: **“완료 조회는 무변경으로 분리하고, 발주 확정 시에만 회차를 증가시키며, 확정 args는 dispatch별 무덮어쓰기 파일로 보존한다.”**

**NA-4 · MED — 스냅샷 검증은 필수 전제가 없을 때 통과하거나 exit 4 밖으로 빠진다.**

좌표: 메모 §2·§5 ㉠; [t40_metrics.py:metrics](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:49).

정상적인 run_id·phase·executed·SHA 불일치는 모두 exit 4였습니다. 그러나 추가 반례는 다음과 같습니다.

- `run.yaml`에 `run_id`가 없으면 `if run_id` 때문에 타 런 판정서도 통과합니다.
- 축 하나를 제거한 **5축 판정서**가 `na=[]`로 통과합니다.
- 빈 sidecar는 `IndexError`, 깨진 JSON은 `JSONDecodeError`로 빠져 exit 4가 아닙니다.

SHA 일치는 파일의 완전성과 비교 지표의 존재를 대신하지 않습니다.

고치는 문안: **“런 식별자와 판정서 형태를 필수 검증하고 6축·계수·값의 결측을 명시하며, sidecar·JSON 판독 및 결속 실패는 모두 exit 4로 종료한다.”**

**NA-5 · LOW — ‘pending대로만 공급한 신규 런에는 한 호출 안 두 번 기록이 없다’는 사실 주장이 틀렸다.**

좌표: 메모 §2 스냅샷 문단; `engine/stages/read.py:run` 조기 루프.

실제 러너에 **그 호출이 요청한 pending 응답만 순차 공급**했습니다. 최초 read-a에서 CL-25 누락, 요청된 재시도에서 복구한 결과입니다.

| 호출 | 새 pending | 그 호출의 조기 기록 `(executed, attempt, axes 수)` |
|---|---|---|
| 1 | read-a/batch-0 | 없음 |
| 2 | read-b/batch-0 | 없음 |
| 3 | read-a/retry-1/batch-0 | `(False, 0, 0)` |
| 4 | 없음·상신 반환 | **`(False, 0, 0)` → `(True, 1, 6)`** |

재진입이 기존 응답부터 재연하므로 두 번 기록됩니다. **이 반례에서 최초 유효 스냅샷 손실은 없었습니다.** 앞의 축 0 문서는 직전 호출에서 보존할 수 있고, 마지막 문서가 최초 실행 판정입니다. 따라서 결함의 격은 기능 실패가 아니라 잘못된 보증 설명입니다.

고치는 문안: **“신규 런도 재진입 중 조기 판정서를 여러 번 기록할 수 있으며, 최초 실행 판정의 보존은 이전 호출 스냅샷과 pending 공급 순서의 불변식으로 설명한다.”**

**NA-6 · MED — Workflow는 요청 경로 중복과 요청·응답 교차 충돌을 거부하지 않는다.**

좌표: 메모 §3 사전 거부; [t40_lanes.workflow.js:사전검사](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_lanes.workflow.js:32).

`paths` 집합에는 응답 경로만 넣습니다. Node에서 본문을 실행한 결과:

- 같은 `request_md`를 두 좌표에 공급: **호출 2, error 없음**
- 한 레인의 `response_json`을 다른 레인의 `request_md`로 지정: **호출 2, error 없음**

반면 `toString`, `constructor`, `/./`, `//`, `..`, 미지 effort, 중복 dispatch·좌표·응답은 호출 전에 거부됐습니다. MZ-9의 기존 두 반례는 닫혔지만 메모가 선언한 경로 사전검사 전체는 닫히지 않았습니다.

고치는 문안: **“요청·응답 경로 각각의 중복과 두 집합의 교차 충돌을 거부하고, 경로가 해당 런·레인의 request.md/response.json 좌표와 결속되는지 확인한다.”**

**NA-7 · HIGH — 합법적인 ‘인용 없음’ 표본의 채점 처분이 비어 있다.**

좌표: 메모 §5 ㉦·§8 ⓘ·§9 G; [t40_excerpts.py:ex2](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_excerpts.py:126), `grounding_item.anchor_state/spec_refs/search_note`.

기준 명세의 표본 **CL-2 / M63**을 `spec=no-anchor-found`, `spec_refs=[]`, 유효한 `search_note`로 바꾼 메모리 자료는 **스키마 오류 0·coverage pass**였습니다. 런 실패 때문에 반드시 제외되는 입력이 아닙니다.

그런데 발췌 2는 `search_note`를 표시하지 않고, 판정 칸은 **조응/오답**뿐입니다. 인용이 없을 때 오답인지, 판정 불가인지, 다른 항목으로 표본을 바꿀지 정해져 있지 않습니다. anchor 임계가 이 경로를 항상 막지도 않습니다. 해당 조합이 `B=0, R0=1, R2=1`이면 분포 비교는 통과할 수 있습니다.

고치는 문안: **“인용 부재·원문 미해소로 대조할 수 없는 표본은 search_note와 함께 판정 불가로 표시하고, 표본 교체나 자동 정오답 처리 없이 ②를 보류·재상신한다.”**

**B — 계측 커밋·동일성: PASS, 확인한 정적 범위**

부모와 팔 변경은 메모대로입니다.

- base `ad4c6c3`의 부모는 `6d92cad`.
- R1 `530b096`, R2 `00e0bed`의 부모는 모두 base.
- base↔각 팔은 `contracts/stages/read.yaml` **2 additions / 2 deletions**뿐.
- 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`.
- 기준 요청서 **6개 재렌더 바이트 동일**, 새 `plan_decompose`의 최초 요청도 차이 필드 없음.
- R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high. Sonnet aliases도 확인했습니다.

`d4e6ca2→6d92cad` 재실측은 다음과 같습니다.

| 파일 | additions/deletions |
|---|---:|
| read.yaml | 321/31 |
| convergence.schema.json | 42/7 |
| run-kinds.yaml | 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py | 90/35 · 32/5 |
| dependency_parse.py | 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py | 19/0 · 69/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

추가로 `reader/lib/__init__.py`는 4/0입니다.

최초 요청 동일성을 후속 요청 동일성으로 확대할 수는 없습니다. 조기 검사·예산·실패 처분은 **어떤 재시도 요청이 생기는지**를 바꾸며, 검사 소견은 `_defect_block`을 통해 요청 본문과 지문에 들어갑니다. 실제 `plan_decompose(..., attempt=1, defects=...)`에서 소견 포함과 지문 변경을 확인했습니다. `contract/file_adapter` 변경은 주로 좌표 허용·경로 포함 검사이며, 같은 유효 입력의 렌더 본문 변경으로 나타나지 않았습니다.

**C — 구동: REVISE**

정상 입력의 0·11·12·13·14, 실제 pending 순서의 10, 상한 분기의 15는 확인했습니다. 스냅샷은 축 0을 별도 보존하고 최초 실행 attempt 1을 유지했습니다. 다만 NA-2·3·5가 남습니다.

예외 뒤 포인터 true→13, false→14도 확인했습니다. 이 분류기는 T38의 종결 근거 세 가지를 전부 판정하는 함수는 아닙니다. 최종 판정서나 원장만 남은 경우의 엔진 종결 여부는 `_run_is_terminated`가 별도로 결정합니다. **구동 exit 14를 엔진 비종결로 읽어서는 안 됩니다.**

**D — 지표: REVISE**

기준 런은 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다. 조기 2행, 완주 13행, findings 0, 6축과 escalations도 일치했습니다.

실제 `to_convergence_payload`의 중복 검사 두 행은 `fail/read-a`, `pass/read-b`로 추정 귀속됐고 findings 1건이 보존됐습니다. 명시된 mismatch·rejected·digest 불일치의 마지막 synthesize는 모두 N/A였습니다. 잔여는 NA-1·4입니다.

**E — 발췌: REVISE. 발췌 1은 폐쇄, 발췌 2에 결정 공백**

5→1 병합은 다섯 단위 모두 같은 후보 `M20`을 제시했습니다. 기준 자기 대조는 positioning 7/7·implication 20/20에서 자기 항목이 후보에 포함됐고, 후보 풀 순서를 뒤집어도 동일했습니다.

상위 3 절단은 후보의 우선 표시입니다. 전역 후보 밖 항목은 부록에 남고 다른 단위에서 사용된 항목도 본문 어딘가에 남습니다. 따라서 **검사한 범위에서 자동 열위나 항목 소실은 없습니다.** Owner가 다른 단위의 후보도 재사용할 수 있음을 더 명시하면 판독이 쉬워지지만, 이를 독립적인 차단 사유로 보지는 않습니다. ㉢ 하나라도 있으면 보류한다는 규칙도 타당합니다.

종속항 표본은 **CL-2·4·7·9·12·14·16·19·21·24**, 기준 표본의 locator **27/27**이 해소됐습니다. 그러나 정상 기준 표본에 없는 NA-7을 닫아야 합니다.

**F — Workflow·실호출 검증: REVISE**

기존 상속 속성·비정규 경로 반례와 wrote=false 보고 문제는 해결됐습니다. 요청 경로 검사는 NA-6이 남습니다.

배치별 실호출 확인, 미상·불일치의 소비 전 중단, dispatch별 이동 보존은 문언상 정합합니다. **실제 transcript/journal 이벤트 구조와 모델·effort 기록은 이번 Node 시험으로 검증하지 않았습니다.**

**G — 결정 공백: REVISE**

특히 인용 없는 표본의 ② 처분, 조회와 발주 계수의 경계, 로그에 없는 마지막 통합 실패의 지표 선택을 실행 전에 확정해야 합니다.

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY - <<'PY' … PY`로 전경 실행했으며, 파일 로더·쓰기 함수의 대체 범위를 병기합니다.

| 명령·실행 경로 | 마지막 출력 줄 또는 종료 결과 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `71ed982f69bcf850156d0294fa58dc6301c68f85` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `f0e1008d4583d011a828460f4155b7ec7e563f6ba9f2cd34dbf4a3cebe772cc7  bundle/T40-MEASURE-DESIGN.md` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` — 위 변경표 재계수 |
| `git diff --stat origin/t40-base HEAD -- engine reader/lib contracts` | 빈 출력 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 줄 `}`, exit 0, `na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)` — exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json` — exit 4 |
| `git show` 절차 blob을 `contract.open`에 대입, 기준 요청 6개 재렌더 | `RERENDER_BYTES_EQUAL 6 /6` |
| 실제 `read.run`·분해 계획·검사 사용, 진입/종결 가드·쓰기·원장 함수 대체, 요청된 pending만 공급 | `PENDING_ONLY_NEW_RUN_FINAL_CALL_EARLY_WRITES 2 FIRST_EXECUTED 1` |
| `cmd_read` 엔진 반환/예외와 조기 파일을 메모리 대입 | `SNAPSHOT_PARSE_FAILURE_ESCAPES_ALL_THREE_CMD_READ_PATHS` |
| `metrics` 파일 입력을 메모리 대입 | `SNAP missing_run_id ACCEPTED axes 6 na []` |
| 실제 `_dispatch`·파일 어댑터에 깨진 retry 응답 대입→그 로그를 추출 | `MALFORMED_LATEST_RETRY_REPORTS_OLD_SYNTH … True` |
| 실제 `write_lanes`, 모든 쓰기를 dict/StringIO로 대체 | 마지막 args `[]`, 네 번째 조회 exit 15, 실제 agent 호출 0 |
| `node --input-type=module -`, Workflow 본문·`agent/pipeline` 대체 | `WORKFLOW_BODY_MEMORY_ONLY_NO_REAL_AGENT_CALLS` |
| `candidates/comp_texts_fn/sample_indices` import, 메모리 후보·표본 대조 | `NO_EXCERPT_GENERATOR_EXECUTED_ALL_CHECKS_IN_MEMORY` |
| 합법적 no-anchor 표본을 스키마·coverage에 대입 | `NOANCHOR_DISTRIBUTION_THRESHOLD_B0_R0_1_R2_1 True OWNER_DISPOSITION_UNSPECIFIED` |
| 봉투 도구 `--write` 없이 stdout 생성→`continue_envelope_state` 메모리 대입 | `ENVELOPE_STDOUT_ONLY (True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 기준 원천·메타·요청 크기 재계수 | `REQUEST_BYTES 6 1353606`; 원천 298,507 B, 메타 차이 `[]` |

**[미검증]**

- 외부 스테이징 TXT와 도면 20개는 열지 않았습니다. 사본 원천 SHA는 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`로 확인했습니다. 외부 원본 SHA와 도면 수는 보관 source-report의 기록까지 확인했습니다.
- 실제 Workflow 호출, 문맥 격리, transcript/journal 형식, 실제 거부물 이동과 동시 쓰기는 실행하지 않았습니다.
- 메모리 러너 시험은 진입·종결 가드와 출력 함수를 대체했습니다. 실제 source/read 재개·봉투 발행·생산 원장 append의 성공 시험이 아닙니다.
- 시간·토큰 환산·가용 메모리 및 09-01 CLI의 실제 effort는 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 전문, `D-20260905-02-pdm2b-seats.md` §17 추기 포함, MY·MZ 도전 원문, SPEC §8.4 지정 행, T14·T17·T38.
- 계약: `run-kinds.yaml`, `stages/read.yaml` 지정 블록, `approval-envelope.schema.json`, 관련 `material-spec.schema.json`.
- 대상: 설계 메모 v3 전문, `t40_drive.py`, `t40_metrics.py`, `t40_excerpts.py`, `t40_lanes.workflow.js`, `t40_envelope.py` 전문.
- 구현: `read.py`·`source.py`의 지정 흐름, `lanes/plan.py`·`contract.py`·`file_adapter.py`, `paths.py`, `read_view.py`, `convergence.py`·`run_checks.py`·`report.py`·`coverage.py`의 관련 함수.
- 실물: 기준 run.yaml·source-report·patent.md·명세·조기/완주 판정서·lane-log·분해 응답·요청 JSON/MD 6개 및 지표 추출에 사용한 통합 응답, 지정 커밋의 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았고, 실측 레인은 시작하지 않았습니다.