# 독립 감수 원문 — M1b 설계 도전 8차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v8 · 판정 REVISE(MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `bccb54b69c88a295d01ac97fa292f1dfa154bf9fdb6b98d2595ea48300dad644` · 15238 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v8/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 07:03:00 → 07:13 · **USAGE = input 3,061,937(cached 2,888,832) · output 16,629(reasoning 1,861)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `957cd34` · `bundle/T40-MEASURE-DESIGN.md` v8 sha256 `ff60e1de…fef9` · v1~v7 동봉 · 지표 v8). 폐쇄 = **이전 39건 전건 closed · partially 0 · open 0**. **B·C·E·F PASS** · D 만 REVISE(조기·완주 공통 검증기 · 7차 반례 전부 exit 4 · 스키마 탐색이 worktree 배치에서 옳은 파일 선택 확인).

**판정 = REVISE · 1건(MED 1) · 기각 0 · 발주자 귀책.** **NF-1 MED**: 완주 판정서의 `run_id` 를 `run.yaml#run_id` 와 대조하지 않고 출력에서도 지움 → 다른 런(`t40-r2`)의 완주 판정서를 대상 런 결과로 수용(`na=[]`) · `run_id` 삭제도 수용.

지적 열거 = NF-1

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 7**. **수용 → 지표 v9(완주 판정서 `run_id` 필수 문자열 · run.yaml 대조 · 부재·불일치 exit 4 · `_run_id` 출력 보존) + 설계 v9 → M1b 9차 도전(지적 `NG-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 39건은 원 지적 범위에서 모두 closed입니다.** 7차의 완주 형태·수치 반례와 finding 계약 반례는 닫혔습니다. 새 지적은 **NF-1 · MED 1건**입니다. 다른 런의 완주 판정서를 대상 런의 결과로 수용하는 결속 누락이 남았습니다.

사본 path·pin·order·disposable과 HEAD `957cd3492268d2e486746c48320355e489bc2c98`가 일치했습니다. 메모 SHA-256도 `ff60e1deec9aa87b3079c9da993b17f00634e7075ce08c7939206db88debfef9`로 일치했습니다.

**A — 원장 정합·폐쇄표: REVISE**

폐쇄는 원 지적의 범위로 판단했습니다. MZ-3의 **조기 스냅샷 결속**, NE-1의 **완주 형태·수치 검증**은 닫혔으며, 완주 문서의 런 귀속 누락은 NF-1로 구별합니다.

| 지적 | v8 판정 | 확인 근거 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree·최초 요청 6/6 동일 |
| MY-2 | closed | 잡음 폭 확대·축소 방향 미확정 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | closed | 수확 fact 제외·최신 부적격 N/A·계수 바이트 결속 |
| MY-6 | closed | 첫 실행 조기 판정·6축·계수 쌍 검증 |
| MY-7 | closed | 검사 배열·findings 보존 |
| MY-8 | closed | 진입·예외·종결·대기 분류 |
| MY-9 | closed | A-a→엔진→A-b 순서 |
| MY-10 | closed | 완료 구별·경로 거부·기존 응답 보존 |
| MY-11 | closed | 소비 전 실호출 확인·dispatch별 이동 보존 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 보존 |
| MY-13 | closed | 생산 원장은 운영 선택·누적량 조건부 표기 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 제시 |
| MZ-2 | closed | 축 0 별도 보존·첫 실행 판정 유지·결측 재상신 |
| MZ-3 | closed | 조기 스냅샷 필수·런/국면/실행/지문 대조 |
| MZ-4 | closed | 실제 상수·예외 경계·상태 모순 처리 |
| MZ-5 | closed | 최신 부적격 N/A·같은 응답 바이트로 지문과 계수 |
| MZ-6 | closed | 중복 검사·귀속 추정·findings·escalations 보존 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 일치 |
| MZ-8 | closed | dispatch별 증거·추가 호출 상한·거부 무차감 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로 거부 |
| NA-1 | closed | 로그 없는 최신 디스크 시도도 선택하여 N/A |
| NA-2 | closed | 스냅샷·후처리 경계와 phase 모순 처리 |
| NA-3 | closed | 조회 무쓰기·발주 확정만 계수 |
| NA-4 | closed | 조기 식별자·축·sidecar·판독 오류 처리 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 거부 |
| NA-7 | closed | 인용 부재 등의 판정 불가·표본 유지·재상신 |
| NB-1 | closed | 진입 실패·증거 기록 실패→14 |
| NB-2 | closed | 발주 전건 검사·거부 무차감·부분 기록 복구 처분 |
| NB-3 | closed | 조기 필수 축·계수·수치 검증 경계 |
| NC-1 | closed | 실제 `enter`의 SystemExit 2/3→14 |
| NC-2 | closed | 조기 스냅샷 단일 읽기·변환 경계 |
| NC-3 | closed | bool·음수·범위 밖·NaN 거부 |
| ND-1 | closed | findings 필수 배열과 원소 계약 검증 |
| ND-2 | closed | 통합 응답 단일 읽기·동일 바이트 계수 |
| NE-1 | closed | 조기·완주 공통 검증기·지정 반례 전부 거부 |
| NE-2 | closed | finding 필수 필드·타입·문자열 제약 검증 |

**closed 39 · partially 0 · open 0.**

T40 §4·§5의 3런 구성, `partial/read`, 봉투 대상 3런 한정, exact-match·청구항 실패의 봉투 배제는 정합합니다. G-12를 집행 완료로 읽지 않았습니다.

§8의 격도 타당합니다. **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕⓖⓝ는 명시된 범위의 재정 문언 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**입니다. A의 REVISE는 새로운 재정 요구가 아니라 아래 결과 귀속 결함 때문입니다.

**지적 목록**

**NF-1 · MED — 완주 판정서의 런 식별자를 대조하지 않고, 출력에서도 지운다.**

좌표: 메모 **§5 추출기 설명·결과 표**, **§9 D·G**; [t40_metrics.py:166](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:166)의 `metrics/full`, [validate_verdict:58](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:58), `axes_of`.

조기 문서는 `run.yaml#run_id`와 대조하지만, 완주 경로는 객체·`phase=full`·축·checks·findings만 검사합니다. **완주 문서의 `run_id`가 다른 런이거나 없어도 수용합니다.** 이후 `axes_of`는 그 식별자를 출력하지 않으므로, 완주 검사와 findings는 대상 런의 결과처럼 묶입니다.

정상 조기 스냅샷과 일치 sidecar를 유지하고 완주 문서의 식별자만 바꿨습니다.

| 완주 문서 변경 | 완주 전체 스키마 검사 | v8 추출 |
|---|---:|---|
| `run_id=gdm-wo2026128750a1-t40-r2` | 오류 0 | 정상 반환·`na=[]`·대상 런에 귀속 |
| `run_id` 삭제 | 오류 1 | 정상 반환·`na=[]` |

실제 CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행한 마지막 출력입니다.

```text
ACTUAL_CLI_WRONG_FULL_RUN exit=0 target=gdm-wo2026128750a1-agent-memory donor=gdm-wo2026128750a1-t40-r2 na=[] donor_identity_in_full=False
```

**SHA가 출력된다는 사실은 런 귀속 대조를 대신하지 않습니다.** 다른 팔의 정상 판정서도 스키마를 통과하므로, 전체 스키마 검사만 추가해도 첫 반례는 남습니다. 정상 러너가 이런 파일을 생성한다는 주장이 아니라, 문서 혼입을 정상 결과와 구별하지 못한다는 실행 반례입니다.

**고치는 문안:** “완주 판정서의 `run_id`를 필수 문자열로 검증하고 `run.yaml#run_id`와 대조하여 부재·불일치는 동일한 exit 4 경계에서 거부하며, 검증한 식별자를 완주 출력에도 보존한다.”

**B — 계측 커밋 셋: PASS, 정적·메모리 검증 범위**

부모 관계는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base→각 팔 diff는 `contracts/stages/read.yaml` **2/2**뿐입니다.

절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. 절차 5개 blob과 read.yaml 3개 blob도 §0′와 일치했습니다.

`d4e6ca2→6d92cad` numstat 재실측:

| 파일 | 추가/삭제 |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

`lane_profiles` 직접 호출은 R1 분해·통합만 xhigh, R2 종속 접지만 sonnet/high였습니다. 규칙·material-spec 스키마도 동일했습니다.

기준 요청 재렌더 **6/6 바이트 동일**, 신규 최초 분해 요청의 차이 필드는 `[]`입니다. 같은 재시도 좌표에 finding을 추가하면 본문과 지문이 바뀌므로, 최초 요청 동일성을 재시도까지 확대하지 않은 설명이 맞습니다.

**C — 구동 v6: PASS, 메모리 대체 실행 범위**

실제 `enter`를 유지하고 `REPO`를 사본으로, 증거 쓰기를 메모리로 대체했습니다.

- worktree 부재·잘못된 런 이름: 모두 **14**, SystemExit 증거 보존.
- 정상 종결 **0**, pending **10**, 조기 escalation **11**, exact-match·claim-checks **12**, 종결 실패 **13**, 상태 모순 **14**.
- 예외 뒤 종결 포인터 true→**13**, false→**14**.
- 증거 기록 실패는 종결 포인터가 true여도 **14**.
- 축 0 문서는 별도 보존하고, 후속 attempt 2에도 최초 실행 attempt **1 유지**.
- 발주 `A,A,A,B,C,D`: 종료 **0,14,14,0,0,15**, 누적 회차 **1,1,1,2,3,3**. 거부 시 쓰기 0.
- `lanes` 네 번 조회: 쓰기 **0**.

`_next_dispatch`는 현 파일에 없습니다. 실제 계수 경로인 `cmd_dispatch`를 시험했습니다. T38의 종결 판정과 구동 exit 14를 구별한 설명도 정합합니다.

**D — 지표 v8: REVISE**

지정 반례의 결과는 다음과 같습니다. 조기·완주 모두 같은 `validate_verdict`를 실제로 호출합니다.

| 대입 | 조기 | 완주 |
|---|---:|---:|
| `axes=null` | 4 | 4 |
| 축 하나 제거 | 4 | 4 |
| 계수 `[true,true]` | 4 | 4 |
| 계수 `[-1,-1]` | 4 | 4 |
| Jaccard NaN / 2.0 | 각각 4 | 각각 4 |
| `check_id=[]` | 4 | 4 |
| `findings=[{}]` | 4 | 4 |
| finding `message=null` | 4 | 4 |
| finding `locus` 누락 | 4 | 4 |
| 정상 finding | 통과 | 통과 |
| `executed=false`, `axes=[]`, 빈 계수 쌍 | 필수 조기 축 조건상 거부 | 통과 |

스키마 탐색은 `.worktrees/<run-id>/runs/<run-id>` 배치를 메모리로 구성하고, worktree와 외부 루트 양쪽에 스키마가 있다고 대입했습니다. **세 번째 탐색에서 해당 worktree의 `contracts/schemas/convergence.schema.json`을 선택**했습니다. 실제 worktree 생성 시험은 아닙니다.

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**, 조기 검사 **2행**, 완주 **13행**으로 일치했습니다.

최신 디스크 synthesize 좌표에 로그 없음·mismatch·지문 불일치·깨진 JSON을 각각 넣으면 모두 **`synth_counts=None`, `eligible=False`**였습니다. 정상 최신 시도만 계수했습니다. 읽기 사이 교체 모사에서도 응답 읽기는 **1회**, fact **3**을 유지했습니다.

실제 `_dispatch`와 파일 어댑터에 깨진 최신 retry 응답을 넣은 결과도 **`LaneContractError`, 로그 6행 유지**였습니다. 따라서 로그 밖 최신 실패를 디스크 좌표로 잡는 수정은 닫혔습니다. 잔여는 **NF-1**입니다.

**E — 발췌 v4: PASS, 함수·설계 검증 범위**

`ex1/ex2`는 실행하지 않았습니다. 지정된 순수 함수들을 import했습니다.

- 자기 대조 **27/27**, 후보 풀 역순에서도 **27/27 동일**.
- 5→1 병합: `[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]`.
- 표본: **CL-2·4·7·9·12·14·16·19·21·24**.
- 표본 locator **27/27 해소**.

자동 열위는 제거됐습니다. `anchor_state`·`search_note` 표시와 판정 불가·표본 유지·재상신 처분도 원장과 맞습니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

본문을 Node에서 실행하고 `agent/pipeline`을 대체했습니다. `toString`·`constructor`·`/./`·미지 effort·좌표/dispatch 중복·요청/응답 중복·교차·좌표 불일치는 모두 **호출 0회에서 거부**됐습니다.

정상 model·effort 전달과 true/false/null 보고를 확인했습니다. 결과는 **wrote 1·not_written 1**, null 행에도 run·lane_id·dispatch_id가 남았습니다. 실호출 확인·이동 보존은 실행 절차로 명시돼 있습니다.

**G — 결정 공백: REVISE**

새로운 Owner 재정이 필요한 선택지는 발견하지 못했습니다. 그러나 **타 런 완주 문서의 혼입을 추출 실패로 처분하지 않는 공백**이 있습니다. NF-1이 닫히기 전에는 결과 표의 런별 귀속을 충분히 보증할 수 없습니다.

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 전경 `PY -c '…'`로 수행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `957cd3492268d2e486746c48320355e489bc2c98` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `ff60e1deec9aa87b3079c9da993b17f00634e7075ce08c7939206db88debfef9` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md`、절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base→R1/R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `}`, exit 0·`na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`, exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`, exit 4 |
| `metrics`의 `open/isfile` 대체·판정서/sidecar 주입 | `METRICS_V8_REQUIRED_COUNTEREXAMPLES_COMPLETE` |
| 완주 run_id 변경·CLI `runpy.run_path`·읽기만 대체 | 위 `ACTUAL_CLI_WRONG_FULL_RUN … na=[] …` |
| 통합 응답 읽기·`os.walk` 최신 좌표 대체 | `SYNTH_SINGLE_READ_LATEST_DISK_COMPLETE` |
| 구동 함수·dict/StringIO 증거 대체 | `DRIVE_V6_MEMORY_ONLY_COMPLETE` |
| `git show` 절차→재렌더·발췌 함수 import | `REQUESTS_EXCERPTS_MEMORY_ONLY_COMPLETE` |
| `node -e '…Workflow 본문…'`·agent/pipeline 대체 | `WORKFLOW_V4_MEMORY_ONLY_COMPLETE` |
| 봉투 stdout 미리보기→실제 `continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**[미검증]**

- 실제 Workflow 호출·문맥 격리·transcript/journal 실물 형식·거부물 이동·동시 쓰기.
- source 실행·`read.run` 전체 재개·생산 원장 append. 구동의 엔진 반환/예외는 대체했습니다.
- 외부 원천 TXT·도면. 사본 원천은 **298,507 B·SHA `64d5d627…154e`**, `PATENT_META` 차이는 `[]`였습니다.
- 이전 구동·발췌·Workflow 원본과의 바이트 무변경. 제공된 v6/v4/v4의 본문과 동작을 확인했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort.

**읽은 파일**

- 상류: T40 §1·§4·§5 포함 전문, 좌석 결정문 §17 추기 포함, MY~NE 도전 원문의 지적·처분·검증 부분, SPEC 지정 행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence 스키마, reader-rules·material-spec 스키마 대조.
- 대상: 설계 v3·v8 전문, v7→v8 차이, bundle 스크립트 5종.
- 구현: read의 조기 루프·판정서 기록·종결·LaneJournal·dispatch·봉투, source.run, lanes의 plan·contract·file_adapter, paths, read_view, convergence·run_checks·report 관련 함수.
- 기준 런: run.yaml·patent.md·material-spec·조기/완주 판정서·lane-log·요청 JSON/MD 6개·통합 응답, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았고 배경 작업이나 실측 레인을 시작하지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다.