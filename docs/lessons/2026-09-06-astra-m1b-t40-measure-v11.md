# 독립 감수 원문 — M1b 설계 도전 11차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v11 · 판정 REVISE(MED 2) · 특별 요청 판정 「[가설] 등재 후 착수 = 불가」

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `462d25157169831a5b5e819bc1fb13150b7d882d2a3976af0476a96f0fc94307` · 16166 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v11/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 07:48:01 → 08:00 · **USAGE = input 3,092,108(cached 2,914,432) · output 19,831(reasoning 4,395)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `960a123` · `bundle/T40-MEASURE-DESIGN.md` v11 sha256 `fb0f0915…` · v1~v10 동봉 · 지표 v11). 폐쇄 = **이전 44건 closed 43 · partially 1(NH-1 → NI-1) · open 0**(NH-2 닫힘). **B·C·E·F PASS**.

**판정 = REVISE · 2건(MED 2) · 기각 0 · 발주자 귀책.** **NI-1 MED**: 요청 결속이 두 갈래(`sha256(request.md) = request_digest` 와 `request.json.input_digest = 로그 = 응답`)로 끊겨 있고 `request.md` 에서 입력 지문을 **재계산**하지 않음 · `request_digest` 가 비면 첫 검사 생략 · dispatch 증거 미대조 → donor 요청 JSON·MD·응답·로그를 한 묶음으로 넣으면 적격(6/8/4/8). **NI-2 MED**: 같은 run_id 아래 **원천 지문**(`run.yaml#patent.source_sha256` ↔ 조기·완주 `source_digest` ↔ 명세 `patent.source_digest` ↔ 봉인 `patent.md` 실제 sha)이 대조되지 않음 → run_id 만 바꾼 실물 donor 명세(component 43 · 원천 `40f1905b…`)가 정상 수용. **특별 요청 판정 = 불가**(잔여를 [가설] 로 등재해도 타 런·다른 원천 계수가 임계값에 들어가는 경로가 남는다).

지적 열거 = NI-1, NI-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 10**. **전부 수용 → 지표 v12(요청 MD 지문 재계산 = JSON = 로그 = 응답 · request_digest 필수 · dispatch 증거 대조 · 원천 지문 사슬 5점 + 선등록 소재 지문 상수) → M1b 12차 도전(지적 `NJ-*`)**. 도전자의 「불가」 판정을 받아 Owner 질문은 올리지 않는다(방어 잔여를 [가설] 로 두는 안은 도전자가 근거 부적격으로 판정).

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 44건은 closed 43 · partially 1(NH-1) · open 0입니다.** NH-2의 baseline 우회는 닫혔습니다. 그러나 요청 결속과 원천 지문 대조에 남은 누락으로 **타 런 계수가 정상 임계 지표로 출력되는 반례**를 재현했습니다. 새 지적은 **NI-1·NI-2, 모두 MED**입니다.

사본 마커의 path·pin·order·disposable과 HEAD `960a123ac3528dc7b5ed540f534a75cebdf5c6f4`가 일치했습니다. 메모 SHA-256은 `fb0f09159a4eb10f139f8be168a32bbc045e4ec7ca626dbcd6534703556b7ded`입니다.

**A — 원장 정합·폐쇄표: REVISE**

폐쇄는 각 원 지적의 범위로 판정했습니다. 범위로 묶은 행은 해당 ID **각각**의 판정입니다.

| 이전 지적 | v11 판정 | 확인 근거 |
|---|---|---|
| MY-1~2 | closed | 고정 핀·절차 동일성 확인, 잡음 방향 미확정 |
| MY-3~4 | closed | 기준 27단위·Owner 판정, 종속 청구항 10개 표본 |
| MY-5~7 | closed | 수확 제외, 조기 6축·회차, 검사 배열·findings 보존 |
| MY-8~9 | closed | 종료 분류와 A-a→엔진→A-b 순서 |
| MY-10~13 | closed | 완료 구별·실호출 확인·이동 보존·전 런 증거·원장 설명 |
| MZ-1~3 | closed | 병합 후보 재사용, 미실행 제외, 스냅샷 필수·baseline 우회 차단 |
| MZ-4~6 | closed | 예외 분류, 최신 부적격 N/A, 검사 귀속 추정·상신 목록 |
| MZ-7~9 | closed | 부모 기준 numstat, 발주 상한·증거, Map·정규 경로 |
| NA-1~3 | closed | 로그 없는 최신 시도 N/A, 예외 경계, 조회·발주 분리 |
| NA-4~7 | closed | 필수 형태 검증, 다중 기록 설명 정정, 경로 결속, 판정 불가 처분 |
| NB-1~3 | closed | 기록 실패→14, 발주 전건 검사, 조기 검증 경계 |
| NC-1~3 | closed | 실제 enter의 SystemExit→14, 조기 단일 읽기, 수치 범위 검증 |
| ND-1~2 | closed | finding 계약 검증, 계수 바이트 자체의 SHA 대조 |
| NE-1~2 | closed | 완주 공통 검증, finding 필수 필드·타입 검증 |
| NF-1 | closed | 완주 run_id 필수·대상 대조 |
| NG-1~2 | closed | 명세 run_id 대조, 실행본 버전 표기 일치 |
| **NH-1** | **partially** | 지정 두 반례는 차단됐으나 요청 결속 잔여 — NI-1 |
| NH-2 | closed | baseline 기준 런 한정·옵션 상호 배타·조기 run_id/phase 대조 |

T40 §1·§4·§5의 3런·좌석 구성, `partial/read`, 지정 3런의 봉투 대행, exact-match·청구항 실패의 봉투 배제는 정합합니다. G-12를 집행 완료로 주장하지 않습니다.

§8의 격도 유지됩니다. **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕⓖⓝ는 명시된 범위의 재정 문언 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**입니다. 아래 수정은 새로운 좌석 값이나 임계의 재정이 필요하지 않습니다.

**지적 목록**

**NI-1 · MED — 요청 결속이 두 갈래로 끊겨 있으며, 요청서까지 섞으면 타 런 통합 계수를 적격으로 받는다.**

좌표: 메모 **§5 추출기 설명·㉣·§9 D/G**; [t40_metrics.py:234](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:234)의 요청 검증, 238행의 조건부 `request_digest` 대조, 283행 적격 판정.

구현은 다음을 각각 확인하지만 **두 관계를 연결하지 않습니다.**

- `sha256(request.md) = 로그 request_digest`
- `request.json.input_digest = 로그 input_digest = 응답 input_digest`

계약의 `compute_input_digest(digest_source(request.md))`를 재계산하지 않습니다. 또 `request_digest`가 없거나 빈 값이면 첫 검사도 건너뜁니다. 대상 런의 dispatch 증거와 요청 지문을 대조하는 경로도 없습니다.

실제 CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행하고 `open/isfile/walk`만 메모리로 대체했습니다. 대상의 run.yaml·조기·완주·명세는 정상으로 유지했습니다. donor는 실물 `openai-us20260147854a1-cim-fp-3`의 `read-a/synthesize/retry-1/batch-0`입니다.

| 대입 | v11 결과 |
|---|---|
| 정상 대상 요청서 + donor 응답·로그 — 10차 지정 반례 | **exit 4** |
| donor 요청 JSON·MD·응답 원본과 로그 행을 함께 대입 | **exit 0 · eligible true · na=[]** |
| 대상 MD + donor JSON·응답·로그, `request_digest`만 대상 MD의 실제 SHA로 설정 | **exit 0 · eligible true · na=[]** |
| 직전 사례에서 `request_digest` 삭제 | **exit 0 · eligible true · na=[]** |

수용된 통합 계수는 다음과 같습니다.

```text
REAL_DONOR_WHOLE_LANE_BUNDLE exit 0
synth {'fact': 6, 'implication': 8, 'positioning': 4, 'figure_note': 8}
eligible True na []
```

정상 대상 계수는 **3/20/7/10**입니다. 대상 요청 지문 `f8e83add0d259a34…`와 donor 반향 `50e87df90895fdd5…`는 다릅니다. 같은 대상 요청·donor 응답을 실제 `load_response`에 주면 **LaneStaleResponseError**입니다. donor 원본 MD의 재계산 지문과 로그 입력 지문 불일치도 추출기가 놓쳤습니다.

**고치는 문안:** “실측 파일 레인의 request_digest를 필수로 하고 요청 MD에서 입력 지문을 재계산하여 JSON·로그·응답과 대조하며, 대상 dispatch의 run/lane/입력 지문까지 결속해 불일치는 exit 4, 적격 소비 미입증은 ㉣ N/A로 처리한다.”

**NI-2 · MED — 같은 run_id 아래 서로 다른 원천 지문을 가진 판정서·명세를 정상 수용한다.**

좌표: 메모 **§0′·§2 소재·§5 ㉠㉡㉢㉥·§9 D**; [t40_metrics.py:124](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:124)의 run.yaml 로딩, 조기·완주 검증, [명세 검증:193](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:193).

다음 기존 필드가 서로 대조되지 않습니다.

`run.yaml#patent.source_sha256` ↔ 조기·완주 `source_digest` ↔ 명세 `patent.source_digest`

각 필드 하나만 다른 SHA로 바꾼 네 사례가 **모두 exit 0·na=[]**였습니다. 원천 지문은 출력에서도 빠집니다.

추가로 실물 donor 명세에서 **최상위 run_id만 대상 ID로 바꾸고**, 원천 지문과 내용은 그대로 공급했습니다. 명세 전체 스키마 오류는 0이었고, 결과는 다음과 같습니다.

```text
REAL_DONOR_SPEC_RELABELLED_ONLY exit 0
component 43
anchor {'spec=found|figure=found': 43}
dependent {'spec=found|figure=found': 21}
na []
```

명세의 원천 지문은 `sha256:40f1905b78c990134…`, 대상 run.yaml·판정서는 `sha256:64d5d6271d2921e9…`였습니다. **불일치 증거가 입력에 그대로 남아 있는데도**, 정상 대상의 component **56**, 전체 anchor **51/5**, 종속항 anchor **45/5**가 다른 소재의 값으로 바뀝니다.

이는 NG-1의 run_id 검사가 회귀했다는 뜻이 아닙니다. **이름의 일치만으로 원천 결속까지 충족했다고 볼 수 없다는 별도 반례**입니다.

**고치는 문안:** “run.yaml·조기·완주·명세의 원천 지문을 필수 대조하고 봉인된 patent.md의 실제 SHA 및 선등록 소재 지문과 연결하여, 불일치는 계수 전 exit 4로 거부하고 검증한 지문을 출력에 보존한다.”

두 지적은 입력 혼입·불일치 방어의 반례입니다. 정상 엔진이 이런 혼입을 생성했다고 주장하지 않습니다.

**B — 계측 커밋 셋: PASS**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base→각 팔은 `read.yaml` **2/2**만 변경됩니다. 절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.

`lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였습니다. Sonnet aliases도 일치합니다. 기준 요청서 **6/6 재렌더 바이트 동일**입니다.

`d4e6ca2→6d92cad` numstat 재실측도 §0′와 일치했습니다.

| 파일 | 추가/삭제 |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py / lanes/contract.py | 713/126 · 46/1 · 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

검사·재시도 변경은 후속 요청의 발생과 `defects`에 닿습니다. 최초 요청 동일성으로 한정한 메모의 설명이 맞습니다.

**C — 구동 v6: PASS**

메모리 시험에서 정상·대기·실패·모순은 기대한 **0/11/12/13/14**, LanePending은 **10**이었습니다. 실제 `enter`의 worktree 부재·잘못된 런 이름은 모두 **14**입니다. 엔진 예외 뒤 종결 포인터는 13, 증거 기록 실패가 겹치면 14, 스냅샷 실패도 14였습니다.

축 0 문서는 별도 보존됐고, 실행 attempt 1 스냅샷은 attempt 2에서도 유지됐습니다. 조회는 쓰기 0, 발주 1~3회 성공, 4회째 **15·무기록**, 기존 배치 충돌은 **14·무기록**입니다.

**v6에는 `_next_dispatch`가 없으므로 후계인 `cmd_dispatch`를 시험했습니다.** 모든 쓰기·복사는 메모리 객체로 대체했습니다. 봉투 미리보기의 러너 검증 결과는 `(True, '계속 봉투 유효(판정서 지문 결속 확인)')`입니다.

**D — 지표 v11: REVISE**

| 입력 | 확인한 방어 | 잔여 |
|---|---|---|
| run.yaml | 필수 ID·디렉터리 이름 대조·baseline 제한 | 원천 지문 미대조 |
| 첫 조기 | ID·phase·실행·6축·형태·sidecar 검증 | 원천 지문 미대조 |
| 완주 | ID·phase·공통 형태 검증·파일 SHA 출력 | 원천 지문 미대조 |
| 명세 | ID·items 배열 검증 | 다른 원천의 명세 수용 |
| lane-log/요청/응답 | 요청 존재·일부 지문·응답 반향 대조 | 요청 본문 입력 지문 재계산·필수 요청 SHA·대상 dispatch 결속 누락 |

10차 지정 반례의 결과는 **REAL_DONOR_VALID_TARGET_REQUEST→4**, **WHOLE_BUNDLE_WRONG_DIRECTORY→4**, **실측 런 baseline→4**, **baseline+first-early→3**입니다. baseline 모드의 잘못된 조기 run_id·phase도 각각 4였습니다.

조기·완주 형태/수치 회귀 **44건 전부 exit 4**였습니다. 합법적인 완주 미실행은 수용했고, 최신 로그 없는 시도·mismatch·rejected는 N/A였습니다. 스냅샷 부재·SHA 불일치·빈 sidecar·깨진 JSON도 4였습니다.

ND-2의 읽기 사이 교체 반례는 **N/A**로 닫혔습니다. 다만 현재 통합 응답은 사슬 검증과 계수에서 **총 두 번 읽습니다**. 계수용 읽기도 그 바이트의 SHA를 다시 대조하므로, 원 지적의 잘못된 계수 수용은 재현되지 않았습니다.

정상 기준값은 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 3/20/7/10·조기 검사 2행·완주 13행**으로 일치했습니다.

**E — 발췌 v4: PASS**

생성 CLI는 실행하지 않았습니다. 지정 함수를 import한 **5→1 병합에서 다섯 단위 모두 M99를 후보로 받았습니다.** 자동 열위가 없습니다. 자기 대조는 implication 20/20·positioning 7/7입니다.

표본은 **CL-2·4·7·9·12·14·16·19·21·24**, 인용 locator는 **27/27 해소**됐습니다. 인용 부재·단락 미해소·접지 부재의 판정 불가, 표본 유지·② 보류·재상신 처분은 정합합니다.

**F — Workflow v4: PASS**

Node에서 실제 본문의 `agent/pipeline`을 대체했습니다. 정상 호출 옵션은 opus/max·sonnet/high였습니다. `toString`·`constructor`·`/./`·`//`·`..`·미지 effort·요청/응답 중복·교차·런 좌표 불일치·dispatch 중복은 **호출 0회에서 거부**됐습니다.

`wrote:false`는 wrote 계수 0, null은 run·lane_id·dispatch_id를 포함한 dropped 행이었습니다. 소비 전 실호출 확인·이동 보존 절차도 정합합니다.

**G — 결정 공백: REVISE**

열위·결측·표본·봉투·재발주 상한의 처분은 선등록되어 있습니다. 남은 것은 **어느 요청과 원천에 속한 값을 적격 지표로 인정하는지의 집행 공백**입니다. 현재 추출표는 NI-1·2의 불일치를 정상 수치로 내므로 총괄의 별도 수동 판단 없이 재정 근거로 사용할 수 없습니다.

**검증 경로**

아래 `PY`는 지정 사본 cwd에서 실행한 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 하네스는 모두 `PY -c …`로 전경 실행했습니다.

| 명령·실행 경로 | 마지막 출력 또는 판정 줄 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `960a123ac3528dc7b5ed540f534a75cebdf5c6f4` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `fb0f09159a4eb10f… bundle/T40-MEASURE-DESIGN.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader/lib …` | `90 35 reader/lib/run_checks.py` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 0, 마지막 줄 `}` |
| `PY -c …runpy.run_path("bundle/t40_metrics.py", run_name="__main__")…` — 파일 접근 메모리 대체 | `METRICS_CHAIN_TESTS_DONE` — NI-1의 적격 수용 재현 |
| 같은 CLI 경로, 판정서 변형 44건 | `VERDICT_REGRESSIONS 44 exit4 44 unexpected []` |
| 같은 CLI 경로, donor 명세의 ID만 대상화 | `RELABELLED_SPEC_SCHEMA_ERRORS 0` — component 43·na=[] |
| `PY -c …classify/cmd_read/snapshot_first_early/cmd_dispatch…` | `DRIVE_MEMORY_TESTS_DONE` |
| `PY -c …candidates/comp_texts_fn/sample_indices…` | `EXCERPTS_MEMORY_TESTS_DONE` |
| `PY -c …lane_profiles/render_request_md/_dispatch…` | `COMMIT_AND_REQUEST_TESTS_DONE` — 요청 6/6 동일 |
| `node -e …` — 실제 Workflow 본문 대체 실행 | `WORKFLOW_STUB_TESTS_DONE` |
| 봉투 stdout 미리보기→`continue_envelope_state` | `ENVELOPE_VALIDATOR (True, '계속 봉투 유효(판정서 지문 결속 확인)')` |

**[미검증]**

- 외부 스테이징 TXT·도면 20개는 접근하지 않았습니다. 사본 정본화 원문은 **298,507 B**, SHA `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`입니다.
- 실제 Workflow API·transcript/journal 이벤트 구조·실제 effort·문맥 독립성은 검증하지 않았습니다.
- source/read 전체 쓰기 실행, 조기 루프 전체 재연, 실제 봉투 발행·재개·원장 append는 하지 않았습니다.
- 시간·토큰·메모리 추정과 Owner 의미 판독은 검증하지 않았습니다.

**읽은 파일**

- T40 원장 전문, 결정문 §17 추기 전체, T14·T17·T38, SPEC 지정 G행, 1·2차 도전 원문과 3~10차 지적·처분 관련 절.
- `run-kinds.yaml`, `read.yaml` 지정 블록, approval-envelope·convergence 스키마, material-spec 스키마, 로더가 사용하는 reader-rules.
- 설계 v3·v11, v10→v11 diff, bundle 스크립트 5종.
- `read.py` 지정 함수·조기/출구 루프·기록 경로, `source.py:run`, lanes의 plan·contract·file_adapter, paths, convergence·run_checks·report의 관련 구현.
- 기준 런 run.yaml·원문·판정서·명세·로그·요청/응답, cim-fp-3 명세·통합 요청/응답·로그, 지정 Git 커밋·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 허용된 Python 인터프리터 이용 외에 정본 리포를 읽지 않았으며 실측 레인을 시작하지 않았습니다.

**특별 요청 판정: 불가 — 잔여를 [가설]로 등재하는 것만으로는 타 런·다른 원천의 계수가 정상 임계값으로 들어가는 경로가 제거되지 않아, 현재 결과 표의 ①② 재정 근거 적격성이 확보되지 않습니다.**