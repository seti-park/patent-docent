# 독립 감수 원문 — M1b 설계 도전 2차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v2 · 판정 REVISE(BLOCKER 1 · HIGH 5 · MED 3)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `5625046f71e7dd79ff37a6a4bdef66d2e271b2b8693c14fdc58ee55fd595b1c8` · 21982 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v2/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 05:15:58 → 05:27 · **USAGE = input 2,740,134(cached 2,594,560) · output 19,614(reasoning 4,909)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `6c87ff2` · `bundle/T40-MEASURE-DESIGN.md` v2 sha256 `4d4efb90…7813` · v1 동봉 · 스크립트 5종 · `origin/t40-base` `ad4c6c3` · `t40-r1` `530b096` · `t40-r2` `00e0bed`). 도전자가 확인한 것: 절차 디렉터리 tree 가 기준 핀과 동일(`d7717eb8…`) · 팔 diff 2/2 · 기준 요청서 6개의 현행 `render_request_md` 재렌더가 base 절차 blob 으로 **바이트 동일** · A-a→A-b 순서가 실제 제어 흐름과 일치 · 종속항 표본 CL-2·4·7·9·12·14·16·19·21·24 · 인용 locator 27개 전부 원문 단락 해소 · 봉투 도구 미리보기 → 러너 검증기 통과.

**판정 = REVISE · 9건(BLOCKER 1 · HIGH 5 · MED 3) · 기각 0 · 전부 발주자 귀책 · MY-1~13 = closed 6 · partially 7.** **MZ-1 BLOCKER**: 짝짓기 실패를 자동 열위로 계수(5→1 병합 사례 = 기본 열위 4 · R1 추가 0 · Owner 구제 통로 없음) · 「27항목」 분모를 실행 후 R0 항목 수(`active` 만)로 바꾼 해석은 미승인. **MZ-2 HIGH**: 첫 조기 판정서에 수렴 6축이 없을 수 있다(청구항 검사 실패 → `executed=False · axes=[]` 로 판정서 기록 → 재시도 요청 LanePending → 구동기가 그것을 첫 스냅샷으로 잡음) · 재시도 응답 선공급 시 한 호출 안에서 두 번 기록 · 12·13 으로 멈춘 런의 결측값 처분 미완. **MZ-3 HIGH**: `--first-early` 가 다른 런·국면 파일을 무경고 수용 · 부재 시 가변 파일로 후퇴. **MZ-4 HIGH**: 메모·docstring 의 `escalation`·`exact-match` 는 실제 `blocked_by` 값(`convergence-escalation` · `convergence-exact-match`)이 아님 · `cmd_read` 가 LanePending 만 잡아 StageError 는 exit 1 · status ok + 대기 포인터 모순도 0. **MZ-5 HIGH**: lane-log `ok` 는 채택 표시가 아니라 왕복 상태(mismatch 응답 = `ok=False · rejected=False` 인데 payload 반환) → 마지막 synthesize 가 부적격이면 추출기가 이전 시도 값을 현재로 보고 · 응답 sha ↔ `response_digest` 대조 없음. **MZ-6 MED**: 검사 행에 `read_run` 이 없고(`to_row_dict` 가 extras 를 뺌) findings 미출력 · `_escalations` 는 `convergence_report.escalations` 에 있음. **MZ-7 MED**: 베이스 증명의 대조 기준은 `origin/main`(10 파일)이 아니라 부모 `6d92cad`(6 파일) · `read.yaml` 은 d4e6ca2 이후 321/31 변경 · `convergence.schema.json` 변경 — 「엔진 변경은 프롬프트에 닿지 않는다」는 무조건 성립하지 않음(재시도 요청의 defects). **MZ-8 HIGH**: 반복 재발주의 증거 좌표(dispatch id · 같은 목적지 충돌 · 같은 label 재사용)와 상한 없음. **MZ-9 MED**: Workflow 사전 거부가 `/./` 경로 동등성과 상속 속성 라벨(`constructor`·`toString`)을 통과시킴.

지적 열거 = MZ-1, MZ-2, MZ-3, MZ-4, MZ-5, MZ-6, MZ-7, MZ-8, MZ-9

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기**. **전부 수용 → 설계 메모 v3 + 스크립트 개정 → M1b 3차 도전(지적 `NA-*`)** — BLOCKER 가 있으므로 재도전 없이 착수하지 않는다.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**MY-1~13 중 closed 6건, partially 7건입니다.** 절차 복원·좌석 커밋·분해 배치 수정은 확인했습니다. 그러나 **발췌의 자동 열위 계수, 최초 조기 판정의 축 부재, 예외 종료 및 실패 재시도의 지표 선택**이 남아 있어 실측을 시작할 수 없습니다.

사본 path·pin·order·disposable 일치, HEAD `6c87ff2f631c8248de849b8a44f0e0b2dcba7ee7`, 메모 SHA-256 `4d4efb906ca952725a0660441676ebd84f290c940f101123d6c4998856c27813`을 확인했습니다.

**A — MY-1~13 폐쇄표**

| 1차 지적 | 판정 | v2 확인 및 잔여 |
|---|---|---|
| MY-1 같은 절차·고정 핀 | **closed** | 절차 디렉터리 tree가 기준 핀과 동일. 고정 베이스 위 R1/R2도 확인. 증명 문구의 과장은 MZ-7 |
| MY-2 잡음 폭 방향 단정 | **closed** | 확대·축소 미확정으로 정정 |
| MY-3 비교 단위·짝짓기·채점 | **partially** | 결정론 짝짓기는 구현했으나 분모 변경과 자동 열위가 Owner 판독을 대체함. MZ-1 |
| MY-4 종속항 표본 단위 | **closed** | 종속 청구항 10개, 항 내 additions 전부, 청구항별 오답 집계. 기준 표본 일치 |
| MY-5 통합 계수 | **partially** | 정상 기준 런 fact=3으로 수정. 실패한 마지막 재시도에서는 이전 응답으로 후퇴. MZ-5 |
| MY-6 수렴 축·회차·타입 | **partially** | 6축·count 쌍 명시. 최초 문서가 축 0개인 경로와 스냅샷 결속 미해결. MZ-2·3 |
| MY-7 검사 행 덮어쓰기 | **partially** | 배열 보존은 해결. 실제 러너 산출에는 실행 귀속이 없으며 findings도 추출에서 빠짐. MZ-6 |
| MY-8 종료 코드 | **partially** | 정상 반환값 분류는 수정. 예외는 6종 밖으로 빠짐. MZ-4 |
| MY-9 read-b 미생성 | **closed** | A-a→엔진→A-b 순서가 실제 제어 흐름과 일치 |
| MY-10 Workflow 완료·중복·재발주 | **partially** | `wrote:false`·null 보고 개선. 경로 동등성과 모델 라벨 사전 거부에 구멍. MZ-9 |
| MY-11 실호출 증거·삭제 | **partially** | 소비 전 확인·이동 보존으로 개선. 호출별 증거 결속과 반복 거부 보존 규칙 미완. MZ-8 |
| MY-12 실패 런·외부 실행층 보존 | **closed** | 세 런 전체, 실행 스크립트·args·transcript·MANIFEST 포함으로 범위 수정 |
| MY-13 섀도 원장 설명 | **closed** | 일반 루트 지정과 운영 선택을 구별하고, 증가량을 메모 보유 종결 런 수로 수정 |

**지적 목록 — BLOCKER 1 · HIGH 5 · MED 3**

**MZ-1 · BLOCKER — 짝짓기 실패를 내용 열위로 계수하며, 병합 항목을 Owner가 구제할 통로도 불완전하다.**

좌표: 메모 §5 ㉤·§8 ⓚ; [t40_excerpts.py:greedy](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_excerpts.py:48), `ex1`.

같은 근거를 가진 R0 내용 5개를 R1 항목 하나가 모두 담는 메모리 사례에서, 탐욕 일대일 대응은 한 쌍만 만들었습니다. 결과는 **기본 열위 4, R1 추가 항목 0**입니다. 내용의 누락·열위를 판독하지 않고 임계 3을 넘깁니다. 이미 소비된 병합 항목은 “R1 추가 항목에서 지목”하는 예외로도 처리할 수 없습니다.

또한 재정의 **27항목을 실행 후 R0 항목 수로 바꾸는 해석**은 승인되어 있지 않습니다. 구현은 그중 `active`만 취하므로 메모의 “항목 전부”와도 다릅니다. §8 ⓚ의 “재량·Owner 사후 확인”으로 이 변경을 닫을 수 없습니다.

**고치는 문안:** “비교 단위는 기준 런의 27개 내용 단위로 고정하고, 기계 짝짓기는 후보 제시만 하며 분할·병합·누락을 포함한 열위는 Owner가 각 단위에 명시 판정한다; 대응 미확정은 자동 열위로 세지 않고 채택 판정을 보류한다.”

**MZ-2 · HIGH — ‘첫 조기 판정서’에는 수렴 6축이 없을 수 있다.**

좌표: 메모 §2 스냅샷·§5 ㉠; [t40_drive.py:snapshot_first_early](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:117); `engine/stages/read.py:run` 조기 루프.

실제 러너는 청구항 검사 실패 시 수렴을 보류하면서 판정서를 씁니다. 쓰기 함수를 메모리로 대체한 실행 결과는 **`executed=False, attempt=0, axes=[]`**였습니다. 다음 재시도 요청에서 `LanePending`이 발생하면 구동기는 이 문서를 영구적인 첫 스냅샷으로 잡습니다. 이후 정상 수렴해도 임계용 스냅샷에는 축이 없습니다.

재시도 응답이 이미 공급된 조건에서는 한 번의 `read.run()` 안에서 문서가 두 번 기록되어, 호출 뒤 스냅샷으로는 최초 문서를 회수하지 못하는 것도 확인했습니다. 정상 신규 발주에서 재시도 응답이 없는 경우와 구별해야 합니다.

R0가 12·13으로 멈춰 필요한 지표가 없는 경우도 `w`와 ①②의 처분이 완결되지 않았습니다. “상태 열에 기록”만으로 결측값의 판정 의미가 정해지지 않습니다.

**고치는 문안:** “최초 조기 문서를 원본으로 보존하되 수렴 미실행·필수 지표 부재는 N/A로 명시하고 해당 비교를 판정 불가로 재상신하며, 후속 판정으로 대체하려면 그 선택 규칙을 실측 전에 확정한다.”

**MZ-3 · HIGH — `--first-early`가 다른 런·다른 국면의 파일도 무경고로 받는다.**

좌표: 메모 §2·§5 ㉠; [t40_metrics.py:metrics](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:28).

`run_id=unrelated`, `phase=full`, `attempt=2`인 메모리 파일을 `first_early`로 주어도 **`warnings=[]`**로 추출됩니다. 존재하지 않는 명시 스냅샷은 경고만 남기고 가변 `convergence-early.json`으로 후퇴합니다. 계산한 SHA를 출력하는 것은 런·회차·사전 보존 지문과의 대조가 아닙니다.

**고치는 문안:** “실측 런의 `--first-early`는 필수로 하고 run_id·phase·선등록 회차 조건·보존 SHA를 대조하여 불일치나 부재 시 지표 추출을 실패시키며 다른 파일로 후퇴하지 않는다.”

**MZ-4 · HIGH — 종료 코드 6종은 실제 구동 경로를 덮지 못한다.**

좌표: 메모 §2·§4; [t40_drive.py:classify](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:128), `cmd_read`.

정상 반환 경로에서는 실제 상수 `convergence-escalation`→11, `convergence-exact-match`→12가 맞습니다. **메모와 구동 docstring의 `escalation`·`exact-match`는 실제 필드값이 아닙니다.**

더 큰 문제는 `cmd_read`가 `LanePending`만 잡는다는 것입니다. 진입 `StageError` 대입 결과는 **미포착 예외→프로세스 exit 1**이었습니다. JSON 읽기 오류도 `classify`의 14가 되지 않습니다. 예외가 러너 `finally` 뒤 발생한 경우에는 실제 종결 포인터가 있어도 13으로 보고하지 않습니다. 반환 `status=ok`와 대기 포인터가 충돌하는 반례도 14 대신 0입니다.

**고치는 문안:** “실제 `blocked_by` 어휘를 그대로 쓰고 모든 예외를 증거와 함께 포착하여 종결 근거가 확인되면 13, 상태 모순·판정 불능이면 14로 고정하며 예외 뒤 자동 재호출하지 않는다.”

**MZ-5 · HIGH — 마지막 synthesize가 실패하면 이전 응답을 현재 통합 산출처럼 보고한다.**

좌표: 메모 §5 ㉣·§9 D; [t40_metrics.py:metrics/synth](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:68); `engine/stages/read.py:_dispatch`, `LaneJournal.record`.

정상 재시도에서 마지막 `ok`·비거부 행을 고르는 것은 확인했습니다. 그러나 `ok`는 **채택된 최종 산출 표시가 아니라 모델·effort 일치 여부를 포함하는 왕복 상태**입니다.

실제 `_dispatch`에 mismatch 응답을 주면 payload를 반환하면서 `ok=False, rejected=False`를 기록합니다. 이전 성공 synthesize 뒤 이런 재시도가 붙은 로그를 추출기에 주면, 추출기는 **현재 실패 재시도를 건너뛰고 `batch-0`의 fact=3 등을 보고**했습니다. 실패 런까지 결과 표에 싣는 설계에서는 이전 시도의 값임을 숨기는 결과입니다. 읽은 응답 SHA와 로그의 `response_digest` 대조도 없습니다.

**고치는 문안:** “마지막 실제 소비 synthesize 시도와 최종 채택 상태를 먼저 결정하고 응답 지문을 로그와 대조하며, 마지막 시도가 부적격이면 최종 통합 지표는 N/A로 두고 이전 시도 계수는 회차별 참고값으로만 싣는다.”

**MZ-6 · MED — 검사 배열은 살렸지만 실행 귀속·실패 내용·상신 목록은 제대로 추출하지 못한다.**

좌표: 메모 §5 ㉠; `reader/lib/run_checks.py:to_convergence_payload`; [t40_metrics.py:axes_of](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:18), `early_checks/full_checks`.

실제 조기 루프의 read-a 실패·read-b 통과를 넣었을 때 두 행은 남았지만 **둘 다 `read_run=None`**이었습니다. `CheckRow.extras.read_run`은 `to_row_dict()`에서 이미 빠지므로 추출기의 `dict(c)`로 복원되지 않습니다. 실패 내용은 판정서 최상위 `findings`에 있지만 추출기는 이를 내보내지 않습니다.

또 `_escalations`는 `convergence_detail`에서 읽으므로 기준 런도 `None`입니다. 실제 tree-edges 상신 목록은 `convergence_report.escalations`에 있습니다.

**고치는 문안:** “원본 검사 배열과 findings를 함께 보존하고 현행 러너의 선언된 검사 순서로 실행 귀속을 별도 명시하며, 상신 목록은 `convergence_report.escalations`에서 추출한다.”

**MZ-7 · MED — 커밋 증명표와 ‘변경 없음’ 진술의 범위가 실제보다 넓다.**

좌표: 메모 §0′·§1·§8 ⓖ.

요구한 `git diff --numstat origin/main origin/t40-base`는 절차 6파일 외에 **HANDOFF 및 docs 3파일**, 총 10파일을 출력했습니다. 절차 6파일만인 비교의 기준은 현재 `origin/main=6c87ff2`가 아니라 **고정 부모 `6d92cad`**입니다.

`d4e6ca2` 이후 `read.yaml`도 실제로 **321 additions/31 deletions**이며 `convergence.schema.json`도 변경됐습니다. 좌석 값·reader-rules·material-spec 스키마의 동일성을 계약·스키마 전체의 동일성으로 확대하면 안 됩니다. 재시도 예산·검사 변경은 재시도 여부와 요청서 `defects` 내용에 영향을 줄 수 있으므로 “엔진 변경은 레인 프롬프트에 닿지 않는다”도 무조건 성립하지 않습니다.

**고치는 문안:** “베이스 변경 증명은 부모 `6d92cad`와 대조하고, 동일성은 절차 본문·좌석 값·reader-rules·material-spec 스키마 및 동일 입력의 최초 요청에 한정하며 현행 검사·재시도 계약 차이를 별도 열거한다.”

**MZ-8 · HIGH — 반복 재발주의 증거 좌표와 종료 조건이 없다.**

좌표: 메모 §3 실호출 검증·§6·§8 ⓜ; Workflow `label`과 결과 행.

같은 레인이 두 번 불일치하면 두 응답 모두 **`evidence/rejected/<run>/<lane_id>/`**라는 같은 목적지로 갑니다. 재발주 회차·호출 ID·기존 목적지 충돌 처분이 없습니다. 재발주는 같은 `label`도 재사용합니다. 따라서 어느 `agent-*.jsonl`·journal 호출이 어느 요청과 거부 응답에 대응하는지, 두 번째 거부를 어디에 보존할지 총괄이 현장에서 정해야 합니다.

null·모델 불일치 재발주도 상한 없이 반복 가능합니다. 이것은 엔진의 계약 재시도 예산과 다른 추가 호출입니다.

**고치는 문안:** “각 발주에 고유 dispatch_id를 부여하여 요청·응답 SHA와 transcript·journal 이벤트를 결속하고 거부물은 dispatch_id별 무덮어쓰기 경로에 보존하며, 추가 호출 상한과 초과 시 중단·재상신 처분을 선등록한다.”

**MZ-9 · MED — Workflow의 ‘모르는 라벨·중복 경로 사전 거부’는 완전하지 않다.**

좌표: 메모 §3; [t40_lanes.workflow.js:사전검사](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_lanes.workflow.js:21).

Node에서 실제 본문을 실행하고 `agent`만 대체했습니다.

- `/memory/response.json`과 `/memory/./response.json`은 같은 파일인데 두 호출이 통과했습니다.
- `model_label="constructor"` 또는 `"toString"`은 객체 상속 속성을 통해 검사에 통과하여 **`model`이 function인 호출**을 만들었습니다.
- 정상적인 중복 문자열·일반 미지 라벨·빈 effort는 호출 전에 거부됐습니다.

현재 구동기가 생성하는 통상 입력에서는 앞의 반례가 나오지 않지만, 스크립트가 선언한 사전 거부 범위에는 미달합니다.

**고치는 문안:** “모델은 own-property allowlist로 확인하고 응답 경로는 정규화·실경로 기준으로 중복 및 런·레인 좌표 결속을 검증한 뒤 디스패치한다.”

**A~G 판정**

| 항목 | 판정 | 확인한 범위와 잔여 |
|---|---|---|
| **A 원장 정합** | **REVISE** | T40 §5 봉투 대행은 닫힘. 27항목·열위 정의를 사후 확인으로 바꾸는 것은 미승인 |
| **B 계측 커밋·절차 호환성** | **실물 정합 확인 / 증명 문구 REVISE** | 절차 복원과 팔 diff는 맞음. 최초 요청 프롬프트 동일성 확인. MZ-7 |
| **C 구동·종결** | **REVISE** | 정상 반환의 0/10/11/12/13/14 분기 확인. 예외·스냅샷 경로 미완 |
| **D 지표 추출** | **REVISE** | 기준 계수·6축·정상 재시도 선택 확인. 스냅샷 결속·실패 시도·검사 메타데이터 잔여 |
| **E 발췌 결정론·채점** | **REVISE** | 같은 입력에는 결정론적. 그 사실이 의미 대응과 열위 계수의 정당성을 보증하지 않음 |
| **F Workflow·실호출 검증** | **REVISE** | 정상 사전 거부·보고 분기 확인. 실호출 자료 형식 미검증, 반복 발주 증거 좌표 미완 |
| **G 결정 공백** | **REVISE** | 분모·병합 판독·축 부재·실패 지표·반복 발주의 처분이 남음 |

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛ 및 이동 보존 자체인 ⓜ는 운영 재량**, **ⓔ는 T40 §5로 승인**, **ⓕ는 재정 문언 이행**, **ⓘ는 표본 단위 이행·인덱스는 구현 재량**으로 봅니다. **ⓖ는 절차 동일화라는 범위에서는 이행**이며 MZ-7처럼 설명을 좁혀야 합니다. **ⓚ는 분리해야 합니다.** 런 이름 표시와 후보 짝짓기는 재량이나, 27항목의 분모와 열위의 정의를 바꾸는 것은 사후 확인으로 처리할 수 없습니다.

C의 **12 처분 자체는 T38과 충돌하지 않습니다.** 엔진 포인터는 `terminated:false`, `awaiting:convergence_continue`로 남고 원장에는 추가하지 않으며, 운영자는 그 런을 더 호출하지 않습니다. 이를 성공 종결이나 봉투 가능한 상태로 고쳐 적어서는 안 됩니다.

봉투 도구는 기준 판정서에 대해 **stdout 미리보기만 생성**한 후 러너 검증기에 메모리로 공급하여 `(True, '계속 봉투 유효(판정서 지문 결속 확인)')`를 확인했습니다. 이는 서식·지문 검증입니다. 도구 자체는 런 3개와 청구항 검사 전량을 검사하지 않으므로, T40 §5의 권한 범위는 **정확한 런 지정과 실제 코드 11 확인을 합친 운영 절차**가 지켜야 합니다.

**검증 경로**

모든 명령의 cwd는 지정 사본이었습니다. 아래 `PY`는 전부 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`으로 실행했습니다. 메모리 시험은 `PY - <<'PY' … PY` 형식이며 대체한 함수 범위를 함께 적습니다.

| 실행 명령 또는 메모리 호출 경로 | 마지막 출력·결과 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `6c87ff2f631c8248de849b8a44f0e0b2dcba7ee7` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `4d4efb906ca952725a0660441676ebd84f290c940f101123d6c4998856c27813  bundle/T40-MEASURE-DESIGN.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **빈 출력** |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 `… origin/t40-r2` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat origin/main origin/t40-base` | 총 10파일. 마지막 줄 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만. 마지막 줄 `0 139 reader/procedure/HISTORY.md` |
| `git log -1 --format='%H %P'`를 세 계측 ref에 실행 | R1·R2 부모 모두 `ad4c6c32ee7b601c1f110c7b3bfa04f31660c147`; base 부모 `6d92cad54fb830f3db8316f61bbe991dbc17eec8` |
| `git ls-tree`로 기준·base의 `reader/procedure` 대조 | 둘 다 tree `d7717eb8750115a49e81ec7803790093b98c40ec` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory` | exit 0, 마지막 줄 `]`; 계수는 아래와 일치 |
| `git show` YAML을 `load_stage_contract` 반환값으로 공급하여 `lane_profiles` 실행 | R1 분해·통합만 xhigh, R2 종속 접지만 sonnet/high |
| 기준 요청 JSON 6개→현행 `render_request_md`; 절차 읽기만 base blob으로 대체 | **6개 모두 `bytes_equal True`** |
| 현행 `ReadView`·`plan_decompose`로 최초 요청 신규 생성 | `fresh decompose differing fields []`, `fresh decompose digest equal True` |
| `greedy`·`comp_texts`·`sample_indices` import 후 기준 런 자기 대조 | implication 20/20, positioning 7/7, 비동일 짝 0 |
| 실제 `classify`에 반환값·gate·pointer를 메모리 대입; `cmd_read`의 엔진 호출만 예외로 대체 | `cmd_read StageError uncaught StageError => process exit 1, not 14` |
| 실제 `read.run` 조기 루프; 진입 가드·출력 함수 대체, 분해 응답·검사 실패 주입 | `FIRST_DOCUMENT_CAN_HAVE_ZERO_AXES; PRELOADED_RETRY_OVERWRITES_BEFORE_DRIVER_SNAPSHOT` |
| `metrics`의 파일 로더를 메모리 자료로 대체 | `wrong snapshot accepted full 2 []`; `findings emitted False` |
| 실제 `_dispatch` mismatch 응답→그 로그 형태를 `metrics`에 공급 | `MISMATCH_CAN_REPORT_OLD_SYNTH` |
| `greedy`에 5→1 병합 사례 공급 | `default_inferior 4 R1_extra_available_for_owner_override 0` |
| `node --input-type=module -`로 Workflow 본문 실행, `agent/pipeline` 대체 | `{"model_label":"toString","calls":1,"modelType":"function","error":null}` |

기준 런 재계수는 **163항목**, component **56**, 전체 anchor **51/5**, 종속항 anchor **45/5**, synthesize **fact 3·implication 20·positioning 7·figure_note 10**, 조기 검사 **2행**, 완주 검사 **13행**입니다. 수렴 Jaccard는 element-set **1**, tree-edges **0.090909…**, dependent-set **1**, addition-attachment **0.672413…**입니다.

종속항 표본은 **CL-2·4·7·9·12·14·16·19·21·24**였고, 해당 발췌의 명세서 인용 locator **27개 모두 원문 단락으로 해소**됐습니다. 자기 대조의 positioning 점수는 공유 인용 개수이므로 **2점 6개·3점 1개**입니다. 메모의 “전건 점수 1.0”은 implication에만 맞습니다.

절차 호환성 조사에서는 실행 코드의 절·앵커 파싱이나 `HISTORY.md` 읽기 경로를 찾지 못했습니다. `render_request_body`가 읽은 절차 파일은 **10·20·30 세 문서**뿐입니다. 절차 외 인라인 대상인 요청 필드·응답 스키마·지시문·원천 조각까지 포함해 기준 요청 6개의 재렌더 바이트가 일치했습니다. 이것은 **같은 입력의 요청 동일성**이며, 실제 새 런의 후속 산출·재시도 요청까지 같다는 보증은 아닙니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING 부재는 접근하지 않았습니다. 사본 원문은 **298,507 B**, SHA-256 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`입니다. `PATENT_META`의 제공 필드는 기준 런과 일치하며 원천 경로·SHA는 source가 생성하는 추가 필드입니다.
- Workflow 실호출은 하지 않았습니다. `transcriptDir`, agent 파일과 journal의 실제 이벤트 구조, effort 옵션의 실호출 기록, 문맥 격리 여부는 확인 자료가 없습니다. Node 시험은 구문·분기 시험입니다.
- 브랜치는 checkout 없이 blob을 메모리로 읽었습니다. 실제 worktree에서 source/read를 쓰기 실행하거나 봉투 발행·재개·원장 append를 시험하지 않았습니다.
- 조기 루프 시험은 진입 지문·종결 가드와 출력 함수를 대체했습니다. 실제 런 재개 성공 시험으로 주장하지 않습니다.
- 시간·토큰·가용 메모리 추정과 09-01 CLI의 실제 effort는 검증하지 않았습니다.

**읽은 파일**

- 원장: `ruling-20260905-05-T40.md` 전문, `D-20260905-02-pdm2b-seats.md` §17, 1차 감수 원문, SPEC §8.4 지정 행, T14·T17·T38 전문.
- 계약: `contracts/run-kinds.yaml`, `contracts/stages/read.yaml`의 lane·retry_budget·phase_gates·failure, `approval-envelope.schema.json`.
- 대상: 설계 메모 v2 전문, v1 관련 대조 부분, bundle 스크립트 5종, 기준 봉투.
- 구현: `engine/stages/read.py`·`source.py`, `engine/lanes/plan.py`·`contract.py`·`file_adapter.py`, `engine/paths.py`, `engine/read_view.py`, `reader/lib/convergence.py`·`run_checks.py`·`report.py`의 관련 함수와 호출 경로.
- Git 자료: 지정 커밋의 부모·tree·blob·전체 팔 diff, 기준→base의 계약·엔진·규칙·스키마 변경, 절차 blob.
- 기준 런: `run.yaml`, `patent.md`, 조기·완주 판정서, material-spec, lane-log, 요청·응답 자료, 요청서 6개 전체 재렌더 대조.

파일·임시물·캐시를 만들지 않았고, 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다. 실측 레인은 시작하지 않았습니다.