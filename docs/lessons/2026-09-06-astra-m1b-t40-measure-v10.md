# 독립 감수 원문 — M1b 설계 도전 10차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v10 · 판정 REVISE(MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `2998d6e8d504e5891d8bb9ba9a07a3c0d4ff27333204b7b3a248867db227c420` · 18660 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v10/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 07:30:44 → 07:43 · **USAGE = input 3,758,304(cached 3,572,352) · output 20,447(reasoning 3,394)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `283db73` · `bundle/T40-MEASURE-DESIGN.md` v10 sha256 `6cba3489…` · v1~v9 동봉 · 지표 v10). 폐쇄 = **이전 42건 closed 41 · partially 1(MZ-3 — NH-2 로 좁혀짐) · open 0**. **B·C·E·F PASS**.

**판정 = REVISE · 2건(MED 2) · 기각 0 · 발주자 귀책.** **NH-1 MED**: 레인 자료의 대상 런 결속 미완 — `read-a/`·`read-b/` 접두는 모든 런이 공유 · 추출기가 요청서 바이트·입력 지문을 읽지 않고 응답의 lane_id·반향 지문과 대조하지 않음 → 실물 타 런(cim-fp-3) 응답+lane-log 를 대상 요청 좌표에 두면 엔진은 `LaneStaleResponseError` 로 거부하는데 추출기는 「적격 소비」(6/8/4/8)로 보고 · 대상 디렉터리 ↔ run.yaml 대조도 없음. **NH-2 MED**: `--baseline` 이 기준 런에 제한되지 않고 `--first-early` 와 병용 가능 · baseline 모드에서 run_id·phase 대조 생략 → MZ-3 방어가 옵션 하나로 해제.

지적 열거 = NH-1, NH-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 9**. **전부 수용 → 지표 v11(입력 결속 사슬 전건: 디렉터리 이름 = run.yaml = 조기 = 완주 = 명세 run_id · lane-log 행마다 요청서 실재·`request.md` sha = request_digest · `request.json` input_digest = 행 = 응답 반향 · 응답 lane_id = 행 · 응답 sha = response_digest · synthesize 적격에 이 사슬 포함 · `--baseline` = 기준 런 id 한정 · `--first-early` 와 상호 배타 · baseline 에서도 run_id·phase 대조) → M1b 11차 도전(지적 `NI-*`)**. 이 국면의 잔여는 10회 연속 지표 추출기의 입력 방어이며 설계·계측 커밋·구동·발췌·Workflow 는 5회 연속 PASS — 11차가 PASS 가 아니면 ROUTING ⑸ ③(판정 불능이 아니라 방어 계층의 무한 후퇴)에 준해 **Owner 에게 「추출기 방어 잔여를 [가설] 로 등재하고 착수」 여부를 묻는다**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 42건은 closed 41 · partially 1(MZ-3) · open 0입니다.** NG-1의 타 런 명세 혼입은 exit 4로 닫혔습니다. 그러나 **타 런 lane-log·응답의 통합 계수를 정상 수용하는 경로**, **`--baseline`으로 실측 런의 스냅샷 검증을 우회하는 경로**가 남았습니다. 새 지적은 **NH-1 MED · NH-2 MED**입니다.

사본 마커 path·pin·order·disposable과 HEAD `283db73f627a6925faf931b1d7da2e571ecdd8cf`가 일치했습니다. 메모 SHA-256은 `6cba3489745050f1060878b3c12a12c8cd5f0433e0c7106d48e38642a74ba8ed`로 지정값과 일치했습니다.

**A — 원장 정합·폐쇄 판정: REVISE**

폐쇄는 원 지적의 범위로 판정했습니다. NG-1은 명세서 식별자 대조로 닫히며, 레인 자료의 결속 누락은 NH-1로 구별합니다. MZ-3은 일반 경로의 지정 반례가 닫혔지만, 같은 검증을 해제하는 옵션 조합이 남아 partially입니다.

| 지적 | v10 판정 | 근거 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree·요청서 6/6 동일 |
| MY-2 | closed | 잡음 폭 확대·축소 방향 미확정 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | closed | 수확 fact 제외·통합 응답 별도 계수 |
| MY-6 | closed | 실행된 첫 조기 판정 보존·6축·계수 쌍 |
| MY-7 | closed | 중복 검사 행·findings 보존 |
| MY-8 | closed | 성공·대기·실패·예외 분류 |
| MY-9 | closed | A-a→엔진→A-b 순서 |
| MY-10 | closed | 파일/반환 완료 구별·중복 거부·무덮어쓰기 |
| MY-11 | closed | 소비 전 실호출 확인·dispatch별 이동 보존 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 보존 |
| MY-13 | closed | 생산 원장 사용을 운영 선택으로 명시 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 |
| MZ-2 | closed | 축 0 별도 보존·결측 판정 불가·재상신 |
| **MZ-3** | **partially** | 일반 경로는 거부하지만 `--baseline`이 검증 해제 — NH-2 |
| MZ-4 | closed | 실제 상수·예외 경계·상태 모순 처리 |
| MZ-5 | closed | 최신 부적격 N/A·응답 지문과 계수의 동일 바이트 |
| MZ-6 | closed | 검사 귀속 추정·findings·escalations 보존 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 일치 |
| MZ-8 | closed | dispatch별 증거·추가 호출 상한·거부 무차감 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로 사전 거부 |
| NA-1 | closed | 로그 없는 최신 디스크 시도→N/A |
| NA-2 | closed | 스냅샷 예외·반환 phase 모순→14 |
| NA-3 | closed | 조회 무쓰기·발주 확정만 계수 |
| NA-4 | closed | run_id 부재·축 결측·판독 오류 거부 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 거부 |
| NA-7 | closed | 인용 부재 등의 판정 불가·표본 유지·재상신 |
| NB-1 | closed | 진입·증거 기록 실패→14 |
| NB-2 | closed | 발주 전건 검사·거부 무차감·부분 기록 복구 처분 |
| NB-3 | closed | 조기 형태·필수 지표 검증 경계 |
| NC-1 | closed | 실제 `enter`의 SystemExit 2/3→14 |
| NC-2 | closed | 조기 단일 읽기·변환까지 검증 경계 |
| NC-3 | closed | bool·음수·NaN·범위 밖 수치 거부 |
| ND-1 | closed | findings 필수 배열·원소 계약 검증 |
| ND-2 | closed | 통합 응답 단일 읽기·동일 바이트 계수 |
| NE-1 | closed | 완주 공통 검증·합법적 미실행 구별 |
| NE-2 | closed | finding 계약 위반 거부 |
| NF-1 | closed | 완주 run_id 대조·누락 거부·출력 보존 |
| NG-1 | closed | 실제 donor 명세·식별자 변경/삭제→4·`spec_run_id` 출력 |
| NG-2 | closed | 본문·첨부 실행본의 v6/v10/v4/v4 표기 일치 |

T40 §1·§4·§5의 3런 구성, 좌석 변경 범위, `partial/read`, 봉투 대상 3런 한정, exact-match·청구항 실패의 봉투 배제는 정합합니다. G-12를 집행 완료로 주장하지도 않습니다.

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛⓜ 운영 재량**, **ⓔ T40 §5 승인**, **ⓕⓖⓝ 명시된 범위의 재정 문언 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**입니다. 아래 결함을 고치는 데 새로운 좌석 값 재정은 필요하지 않습니다.

**지적 목록**

**NH-1 · MED — 입력의 대상 런 결속이 완결되지 않아 타 런 통합 산출을 적격 지표로 받는다.**

좌표: 메모 **§5 ㉣·결과 표·§9 D/G**; [t40_metrics.py:119](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:119) `metrics/run_id`, [레인 소속 검사:220](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:220), [응답 적격 판정:244](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:244).

`read-a/`·`read-b/`는 **모든 런이 공유하는 독해 실행 이름**입니다. 이 접두 검사로 런 소속은 증명되지 않습니다. 추출기는 요청서의 존재만 확인하고, 요청 바이트·입력 지문을 읽거나 응답의 `lane_id`·`input_digest`와 대조하지 않습니다.

실제 CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행했습니다. 파일 접근만 메모리로 대체했습니다.

- 대상의 정상 run.yaml·조기 스냅샷·일치 sidecar·완주 판정서·명세를 유지했습니다.
- 대상의 실제 통합 요청 필드와 계측 절차 blob으로 **유효한 `read-a/synthesize/retry-1/batch-0` 요청서**를 렌더했습니다.
- 그 좌표에 실물 `openai-us20260147854a1-cim-fp-3`의 **응답 원본 바이트와 lane-log 원본**을 공급했습니다.

```text
REAL_DONOR_VALID_TARGET_REQUEST 0
{'fact': 6, 'implication': 8, 'positioning': 4, 'figure_note': 8}
eligible True na []
```

정상 대상 계수는 **3/20/7/10**입니다. 대상 요청 지문은 `f8e83add0d259a34…`, donor 응답의 반향 지문은 `50e87df90895fdd5…`로 다릅니다. **추출기의 대상 요청서 읽기 횟수는 0**이었습니다. 같은 요청·응답을 실제 엔진 `load_response`에 넣으면 **`LaneStaleResponseError`**로 거부됩니다.

즉, **엔진이 소비할 수 없는 타 런 응답을 추출기는 “적격 소비” 지표로 보고합니다.** 응답 SHA와 donor 로그 SHA가 서로 맞는다는 사실만 확인했기 때문입니다.

결속의 다른 끝도 비어 있습니다. 대상 디렉터리를 `…-t40-r2`로 두고 기준 런 파일 묶음을 그대로 메모리 대입하면, run.yaml과 내부 문서끼리는 일치하므로 다음처럼 통과합니다.

```text
WHOLE_BUNDLE_WRONG_DIRECTORY 0
directory runs/gdm-wo2026128750a1-t40-r2
run_id gdm-wo2026128750a1-agent-memory na []
```

출력에 다른 run_id가 보이므로 이 두 번째 사례는 은폐가 아닙니다. 그러나 **호출자가 지정한 대상과의 대조를 총괄의 눈에 맡기는 통로**입니다.

**고치는 문안:** “기대 run_id를 run.yaml·대상 경로·dispatch 증거와 대조하고, 그 런의 요청 좌표·요청 SHA·입력 지문을 로그 및 응답의 lane_id·반향 지문·응답 SHA까지 연결해 검증하며, 귀속 불일치는 exit 4, 적격 소비 미입증은 ㉣ N/A로 처리한다.”

**NH-2 · MED — `--baseline` 예외가 기준 런에 제한되지 않으며 명시 스냅샷의 런·국면 검증도 해제한다.**

좌표: 메모 **§1·§2 스냅샷·§5 ㉠**; [t40_metrics.py:132](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:132), [156행 조건](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:156), CLI 옵션 처리.

docstring은 “`--baseline`은 기준 런에만”이라고 선언하지만 구현은 대상 런을 확인하지 않습니다. 두 옵션도 함께 허용합니다. 그 결과 `baseline=True`이면 명시한 스냅샷에 대해서도 run_id·phase 대조가 생략됩니다.

기준 자료를 **R1 경로·R1 run_id·`partial/read`로 정합하게 구성한 메모리 런**에서 실제 CLI 본문을 실행했습니다.

| 인자·입력 | 결과 |
|---|---|
| `--baseline`, 별도 스냅샷 없음 | **exit 0**, R1을 기준 런 경로로 추출 |
| `--baseline --first-early …`, 스냅샷 `run_id=unrelated`, `phase=full`, SHA 일치 | **exit 0 · warnings=[] · na=[]** |

```text
MEASUREMENT_BASELINE_WRONG_SNAPSHOT 0
target gdm-wo2026128750a1-t40-r1
early unrelated full warnings [] na []
```

일반 `--first-early` 경로에서는 같은 run_id·phase 불일치를 모두 exit 4로 거부합니다. **따라서 MZ-3의 방어가 옵션 하나로 해제됩니다.**

**고치는 문안:** “`--baseline`은 식별자가 확인된 09-01 기준 런에만 허용하고 `--first-early`와 상호 배타로 만들며, 조기 문서의 run_id·phase 대조는 기준 모드에서도 생략하지 않고 위반은 exit 4로 종료한다.”

**B — 계측 커밋 셋: PASS, 정적·메모리 검증 범위**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base→각 팔은 `contracts/stages/read.yaml` **2/2**만 변경됩니다.

절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. 절차 5개 blob과 read.yaml 3개 blob도 §0′와 일치했습니다. `lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였습니다. 기준 요청서 **6/6 재렌더 바이트 동일**, reader-rules·material-spec 스키마 diff도 없습니다.

`d4e6ca2→6d92cad` numstat 재실측은 다음과 같습니다.

| 파일 | 추가/삭제 |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py / lanes/contract.py | 713/126 · 46/1 · 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

최초 요청 동일성을 후속 재시도 요청까지 확대하지 않은 §0′의 한정도 맞습니다. 검사·예산 변경은 재시도 여부와 `defects`에 닿습니다.

**C — 구동 v6: PASS, 메모리 검증 범위**

정상·대기·실패·모순 분류가 기대한 0/11/12/13/14와 일치했습니다. `LanePending`은 10, 실제 `enter`의 worktree 부재·잘못된 런 이름은 14였습니다. 엔진 예외 뒤 종결 포인터는 13, 증거 기록 실패가 겹치면 14, 스냅샷 실패도 14였습니다.

스냅샷은 미실행 문서 별도 보존→실행 attempt 1 채택→후속 attempt 2에서 원본 유지였습니다. 메모리 발주는 1~3회 성공, 4회째 15·무기록, 배치 충돌 14·무기록, `lanes` 조회는 무변경이었습니다.

**v6에는 `_next_dispatch`가 없습니다.** 해당 기능의 후계인 `cmd_dispatch`를 직접 시험했습니다. 증거 경로는 `/memory`로 바꾸고 파일 쓰기·복사를 메모리 객체로 대체했습니다.

봉투 도구는 `--write` 없는 미리보기만 생성했고, 러너 검증기에 메모리 공급하여 `(True, '계속 봉투 유효(판정서 지문 결속 확인)')`를 확인했습니다. 권한 범위는 여전히 **지정 3런·exit 11 확인을 합친 운영 절차**가 담당합니다.

**D — 지표 v10: REVISE**

입력 다섯의 결속은 전부 닫히지 않았습니다.

| 입력 | 실제 대조와 잔여 |
|---|---|
| run.yaml | run_id 부재 거부. 기대 대상·디렉터리와의 대조 없음 — NH-1 |
| 조기 스냅샷 | 일반 모드는 run_id·phase·실행·6축·SHA 대조. baseline 우회 — NH-2 |
| 완주 판정서 | run_id 필수 문자열·대상 일치·phase full·형태 검증 |
| 명세 | run_id 필수 문자열·대상 일치·`spec_run_id` 출력 |
| lane-log/응답 | 공유 read-run 접두·응답 SHA 대조. 대상 요청·dispatch와 연결 없음 — NH-1 |

NG-1의 정상/식별자 변경/삭제/실물 donor는 각각 **0/4/4/4**였습니다. donor 명세 자체의 전체 스키마 오류는 0이므로 식별자 대조가 실제로 막은 것입니다.

정상 기준값은 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 3/20/7/10·조기 검사 2행·완주 13행**으로 일치했습니다. 조기·완주 형태/수치 회귀 32건은 모두 exit 4였습니다. 합법적인 완주 `executed=false, axes=[]`는 통과했습니다.

최신 디스크 시도에 로그가 없으면 그 좌표를 선택하고 N/A였습니다. mismatch·rejected·지문 불일치·파싱 실패도 N/A이며 이전 성공 값으로 후퇴하지 않았습니다. 조기 스냅샷과 통합 응답은 각각 한 번 읽었습니다. 버전 표기도 일치합니다.

**E — 발췌 v4: PASS, 함수·문언 확인 범위**

`candidates`·`comp_texts_fn`·`sample_indices`를 import하여 메모리로 시험했습니다. **5→1 병합에서 다섯 단위 모두 M99를 후보로 받았습니다.** 후보 소비·자동 열위가 없습니다.

기준 자기 대조는 implication **20/20**, positioning **7/7**입니다. 표본은 **CL-2·4·7·9·12·14·16·19·21·24**, 해당 인용 locator는 **27/27 해소**됐습니다. 인용 부재·단락 미해소·접지 부재의 판정 불가, 표본 유지, ② 보류·재상신 처분도 원장과 정합합니다. 발췌 생성 CLI는 실행하지 않았습니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

실제 본문에서 `agent/pipeline`을 대체했습니다. 정상 opus/max·sonnet/high는 기대 옵션으로 호출됐습니다. `toString`·`constructor`·`/./`·`//`·`..`·중복 요청·요청/응답 교차·런 좌표 불일치·dispatch 중복은 **호출 0회에서 거부**됐습니다.

`wrote:false`는 wrote 계수 0, null은 run·lane_id·dispatch_id를 가진 dropped 행이었습니다. 실호출 확인과 이동 보존 절차의 문언도 정합합니다.

**G — 결정 공백: REVISE**

결측·열위·표본·봉투·재발주 상한의 처분은 선등록되어 있습니다. 남은 공백은 **어느 런의 응답을 적격 계수로 인정할지**, **기준 런 예외를 어디까지 허용할지**의 집행입니다. 현재 추출기는 잘못된 자료를 N/A나 실패로 보내지 않고 정상 지표로 내므로, 총괄의 실행 중 수동 판단 없이 결과 표를 신뢰할 수 없습니다.

**검증 경로**

아래 `PY`는 전부 지정 사본 cwd에서의 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY -c …`로 실행했으며, 대체 지점을 함께 적습니다.

| 명령·실행 경로 | 마지막 출력 또는 판정 줄 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `283db73f627a6925faf931b1d7da2e571ecdd8cf` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `6cba3489745050f1… bundle/T40-MEASURE-DESIGN.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- …` | `90 35 reader/lib/run_checks.py` — 위 표와 일치 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `BASELINE exit 0 last_line '}'` |
| `PY -c …runpy.run_path("bundle/t40_metrics.py", run_name="__main__")` — `open/isfile/walk` 메모리 대체 | `REAL_DONOR_VALID_TARGET_REQUEST 0 … eligible True na []` |
| 같은 CLI 경로 — R1 자료·baseline 옵션 대입 | `… target gdm-wo2026128750a1-t40-r1 early unrelated full warnings [] na []` |
| 같은 CLI 경로 — 판정서 손상 회귀 | `VERDICT_REGRESSIONS 32 exit4 32 unexpected []` |
| `PY -c …lane_profiles/render_request_md…` — 계약·절차는 `git show` blob 공급 | `REQUEST_RERENDER 6 6` |
| `PY -c …classify/cmd_read/snapshot_first_early/cmd_dispatch…` — 쓰기 메모리 대체 | `DRIVE_MEMORY_TESTS_DONE` |
| `PY -c …candidates/comp_texts_fn/sample_indices…` | `EXCERPTS_MEMORY_TESTS_DONE` |
| `node -e …` — 실제 Workflow 본문·agent/pipeline 대체 | `WORKFLOW_STUB_TESTS_DONE` |
| 봉투 미리보기→`continue_envelope_state`; 실제 `_dispatch` mismatch 대입 | `DISPATCH_MISMATCH 1 {'ok': False, 'mismatch': True, 'rejected': False}` |

**[미검증]**

- 외부 스테이징 TXT·도면 20개는 접근하지 않았습니다. 사본 정본화 원문은 **298,507 B**, SHA `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`입니다.
- Workflow 실제 API 호출·transcript/journal 이벤트 구조·실제 effort·문맥 독립성은 확인하지 않았습니다. Node 결과는 분기·옵션 시험입니다.
- source/read 전체 쓰기 실행, 실제 봉투 발행·재개·원장 append, 조기 루프 전체 재연은 하지 않았습니다. 러너 해당 경로는 정적으로 읽고 지정 함수·입력 경계를 시험했습니다.
- 시간·토큰·가용 메모리 추정, 실제 Owner 의미 판독은 검증하지 않았습니다.
- 반례는 파일 혼입·옵션 오용을 메모리로 모사한 것입니다. 정상 엔진이 해당 혼입을 생성했다는 주장이 아닙니다.

**읽은 파일**

- 원장·감수: T40 전문, `D-20260905-02-pdm2b-seats.md` §17 추기 전체, T14·T17·T38, SPEC 지정 G행, 1·2차 도전 원문과 3~9차 지적·처분 관련 절.
- 계약: `contracts/run-kinds.yaml`, `contracts/stages/read.yaml` 지정 블록, `approval-envelope.schema.json`, `convergence.schema.json`, `reader/reader-rules.yaml`, `reader/schemas/material-spec.schema.json`.
- 대상: 설계 v3·v10, v9→v10 diff, bundle 스크립트 5종.
- 구현: `engine/stages/read.py` 지정 함수·조기/출구 루프·기록 경로, `source.py:run`, `engine/lanes/plan.py`·`contract.py`·`file_adapter.py`, `engine/paths.py`, `reader/lib/convergence.py`·`run_checks.py`·`report.py:to_row_dict`.
- 실물: 기준 런 run.yaml·원문·판정서·명세·lane-log·요청 6건·응답, cim-fp-3 명세·로그·통합 응답, cim-fp-2 로그·통합 응답, 지정 Git 커밋·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았고, 실측 레인은 시작하지 않았습니다.