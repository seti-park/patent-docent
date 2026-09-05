# 독립 감수 원문 — M1b 설계 도전 9차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v9 · 판정 REVISE(MED 1 · LOW 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `30915c272f4de5e744a680a8f7b57edfa805df2ad2a4a40b91ded909c67cdd1c` · 16118 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v9/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 07:16:04 → 07:26 · **USAGE = input 2,781,634(cached 2,608,640) · output 17,386(reasoning 1,879)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `961a9a3` · `bundle/T40-MEASURE-DESIGN.md` v9 sha256 `def1527e…` · v1~v8 동봉 · 지표 v9). 폐쇄 = **이전 40건 전건 closed · open 0**(NF-1 = 타 런 완주 판정서·run_id 누락 → exit 4). **B·C·E·F PASS**.

**판정 = REVISE · 2건(MED 1 · LOW 1) · 기각 0 · 발주자 귀책.** **NG-1 MED**: `material-spec.json` 의 `run_id` 를 대조하지 않아 타 런 명세(실물 `openai-us20260147854a1-cim-fp-3` · component 43 · anchor 43)를 대상 런의 ①② 임계 지표로 수용(`na=[]`) · 출력에도 미보존. **NG-2 LOW**: 메모 §3 Workflow 「v3」 · §5 지표 「v8」 표기가 §9·첨부본(v4·v9)과 불일치.

지적 열거 = NG-1, NG-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 8**. **전부 수용 → 지표 v10(명세서 `run_id` 필수·대조·`spec_run_id` 출력 · lane-log 의 lane_id 소속도 대조) + 설계 v10(버전 표기 정정) → M1b 10차 도전(지적 `NH-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 40건은 원 지적 범위에서 모두 closed입니다.** NF-1의 타 런 완주 판정서·`run_id` 누락 반례는 exit 4로 닫혔습니다. 그러나 **다른 런의 `material-spec.json`을 대상 런의 구성요소·anchor 지표로 수용하는 반례**가 남았습니다. 새 지적은 **NG-1 MED·NG-2 LOW**입니다.

사본 path·pin·order·disposable과 HEAD `961a9a37b4f2a50de22127fe27e0db00ba2e020d`가 일치했습니다. 메모 SHA-256도 지정값 `def1527e55d95d41…`과 일치했습니다.

**A — 원장 정합·이전 지적 폐쇄: REVISE**

폐쇄는 각 원 지적의 범위로 판정했습니다. NF-1은 완주 **판정서** 결속으로 닫고, 명세서 결속 누락은 NG-1로 구별합니다.

| 지적 | v9 판정 | 확인 근거 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree·요청 6/6 동일 |
| MY-2 | closed | 잡음 폭 확대·축소 방향 미확정 명시 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | closed | 수확 제외·최신 적격 통합 응답 계수 |
| MY-6 | closed | 첫 실행 조기 판정·6축·계수 쌍 |
| MY-7 | closed | 중복 검사 행·findings 보존 |
| MY-8 | closed | 정상·대기·실패·예외 분류 |
| MY-9 | closed | A-a→엔진→A-b 순서 |
| MY-10 | closed | 반환/파일 완료 구별·중복 거부·무덮어쓰기 |
| MY-11 | closed | 소비 전 실호출 확인·dispatch별 이동 보존 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 보존 |
| MY-13 | closed | 생산 원장 사용을 운영 선택으로 명시 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 |
| MZ-2 | closed | 축 0 별도 보존·결측 판정 불가·재상신 |
| MZ-3 | closed | 조기 스냅샷 필수·런/국면/실행/지문 대조 |
| MZ-4 | closed | 실제 상수·예외 경계·상태 모순 처리 |
| MZ-5 | closed | 최신 부적격 N/A·지문과 계수의 바이트 결속 |
| MZ-6 | closed | 검사 귀속 추정·findings·escalations 보존 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 일치 |
| MZ-8 | closed | dispatch 증거·추가 호출 상한·거부 무차감 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로 거부 |
| NA-1 | closed | 로그 없는 최신 디스크 시도 선택→N/A |
| NA-2 | closed | 스냅샷 예외·반환 phase 모순 처리 |
| NA-3 | closed | 조회 무쓰기·확정 발주만 계수 |
| NA-4 | closed | 조기 식별자·필수 축·계수·판독 오류 처리 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 거부 |
| NA-7 | closed | 인용 부재 등의 판정 불가·표본 유지·재상신 |
| NB-1 | closed | 진입·증거 기록 실패→14 |
| NB-2 | closed | 발주 전건 검사·거부 무차감·부분 기록 복구 처분 |
| NB-3 | closed | 조기 형태·필수 지표 검증 경계 |
| NC-1 | closed | 실제 `enter`의 SystemExit 2/3→14 |
| NC-2 | closed | 조기 단일 읽기·검사 변환 경계 |
| NC-3 | closed | bool·음수·NaN·범위 밖 수치 거부 |
| ND-1 | closed | findings 필수 배열·원소 계약 검증 |
| ND-2 | closed | 통합 응답 단일 읽기·동일 바이트 계수 |
| NE-1 | closed | 조기·완주 공통 검증기·지정 반례 거부 |
| NE-2 | closed | finding 필수 필드·타입 검증 |
| NF-1 | closed | 완주 run_id 대조·누락 거부·출력 보존 |

**closed 40 · partially 0 · open 0.**

T40 §1·§4·§5의 3런 구성, 좌석 변경 범위, `partial/read`, 봉투 대상 3런 한정, exact-match·청구항 실패의 봉투 배제는 정합합니다. G-12를 집행 완료로 주장하지도 않습니다.

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛⓜ 운영 재량**, **ⓔ T40 §5 승인**, **ⓕⓖⓝ 명시된 범위의 재정 문언 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**입니다. A의 REVISE는 신규 Owner 재정 요구가 아니라 결과 귀속 결함 때문입니다.

**지적 목록**

**NG-1 · MED — 명세서의 런 식별자를 대조하지 않아 타 런의 임계 지표를 정상 수용한다.**

좌표: 메모 **§5 ㉡·㉢·㉥·결과 표, §9 D·G**; [t40_metrics.py:183](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:183) `metrics`의 명세 로딩·계수 부분.

완주 판정서는 173행에서 `run_id`를 대조하지만, 명세서는 JSON을 읽은 뒤 곧바로 항목을 셉니다. **명세서의 `run_id`는 검사하지 않고 출력에도 보존하지 않습니다.**

실제 CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행했습니다. 정상 조기 스냅샷·일치 sidecar·정상 완주 판정서·lane-log·응답을 유지하고 **명세서 읽기만 메모리로 대체**했습니다.

| 명세서 대입 | 명세 전체 스키마 오류 | CLI 결과 |
|---|---:|---|
| 정상 기준 명세 | 0 | 정상 추출 |
| 기준 명세의 `run_id`만 `…-t40-r2`로 변경 | 0 | **exit 0·`na=[]`** |
| 기준 명세의 `run_id` 삭제 | 1 | **exit 0·`na=[]`** |
| 실물 `openai-us20260147854a1-cim-fp-3` 명세 원본 | 0 | **exit 0·`na=[]`·타 런 계수 수용** |

마지막 사례의 출력은 다음과 같습니다.

```text
REAL_DONOR openai-us20260147854a1-cim-fp-3 schema_errors 0
target gdm-wo2026128750a1-agent-memory
component 43
anchors {'spec=found|figure=found': 43}
dependent {'spec=found|figure=found': 21}
na []
```

정상 대상 값은 component **56**, 전체 anchor **51/5**, 종속항 anchor **45/5**입니다. 혼입 후에도 조기·완주 `_run_id`는 모두 정상 대상 런을 가리킵니다. 따라서 **판정서 식별자가 정상인 결과 안에서 ①·② 임계에 직접 쓰이는 칸들이 타 런 값으로 바뀝니다.**

전체 스키마 검사만으로도 닫히지 않습니다. 실제 donor와 `run_id`만 변경한 명세 모두 스키마 오류가 0입니다. 정상 러너가 이런 혼입을 생성한다는 주장이 아니라, 추출기가 문서 혼입을 정상 결과와 구별하지 못한다는 실행 반례입니다.

**고치는 문안:** “명세서의 `run_id`를 필수 문자열로 검증하고 `run.yaml#run_id`와 대조하여 부재·불일치를 계수 전 exit 4로 거부하며, 검증한 명세 식별자를 출력에 보존한다.”

**NG-2 · LOW — 실행본 버전 표기가 메모 안에서 서로 다르다.**

좌표: [메모 §3:67](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md:67), [§5:94](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md:94), §9; 첨부 스크립트의 버전 선언.

§3은 Workflow **v3**, §5는 지표 **v8**이라고 적지만, §9와 첨부본은 각각 **v4·v9**입니다. 본문에 최신 검증 규칙은 들어 있으므로 기능 회귀로 판정하지는 않습니다. 다만 실행본 식별 문구는 정정해야 합니다.

**고치는 문안:** “§3의 Workflow 버전을 v4, §5의 지표 추출기 버전을 v9로 정정하여 §9와 첨부본에 일치시킨다.”

**B — 계측 커밋 셋: PASS, 정적·메모리 검증 범위**

부모 관계는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base→각 팔은 `contracts/stages/read.yaml` **2/2**만 바뀝니다. 절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`이며, §0′의 절차·계약 blob도 일치했습니다.

`d4e6ca2→6d92cad` 재실측:

| 파일 | 추가/삭제 |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py / lanes/contract.py | 713/126 · 46/1 · 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

`lane_profiles`는 R1 분해·통합만 xhigh, R2 종속 접지만 sonnet/high를 반환했습니다. 기준 좌석·reader-rules·material-spec 스키마도 동일합니다.

절차 읽기를 base blob으로 대체한 기준 요청 재렌더는 **6/6 바이트 동일**, 신규 최초 분해 요청의 차이 필드는 **`[]`**였습니다. 동일 retry 좌표에 finding을 추가하면 지문이 바뀝니다. 최초 요청 동일성을 재시도까지 확대하지 않은 문구가 맞습니다.

**C — 구동 v6: PASS, 메모리 대체 실행 범위**

- 실제 `enter`의 worktree 부재·잘못된 런 이름: **14**, SystemExit 증거 보존.
- 정상 **0**, pending **10**, 조기 escalation **11**, exact-match·claim-checks **12**, 종결 실패 **13**, 모순 **14**.
- 예외 뒤 종결 포인터 true→**13**, false→**14**.
- 증거 기록 실패는 종결 포인터가 true여도 **14**. 기록 함수는 재예외 없이 false를 반환.
- 정상·pending·엔진 예외 뒤 스냅샷 실패: 모두 **14**.
- 축 0 문서는 별도 보존하고, 후속 attempt 2에도 최초 실행 attempt **1 유지**.
- 발주 `A,A,A,B,C,D`: 종료 **0,14,14,0,0,15**, 회차 **1,1,1,2,3,3**. 거부 시 쓰기 0.
- `lanes` 네 번 조회: 쓰기 **0**.

`_next_dispatch`는 현 파일에 없습니다. 실제 계수 경로인 `cmd_dispatch`를 시험했습니다. exit 14를 엔진 비종결로 단정하지 않는 설명도 T38과 맞습니다.

**D — 지표 v9: REVISE**

NF-1 재시험은 다음과 같습니다.

| 완주 판정서 입력 | 결과 |
|---|---|
| 정상 | exit 0·조기/완주 `_run_id` 보존 |
| 타 런 `run_id` | exit 4 |
| `run_id` 삭제 | exit 4 |
| `run_id` 숫자·배열·객체 | 각각 exit 4 |

이전 회귀 시험에서 조기·완주 모두 `axes=null`, 축 제거·중복, bool·음수 계수, NaN·2.0·bool Jaccard, 잘못된 checks, findings 부재·null·객체·문자열·잘못된 원소를 **exit 4**로 거부했습니다. 정상 finding은 통과했고, 완주 `executed=false + axes=[]`도 통과했습니다.

최신 디스크 synthesize 시도의 로그 부재·mismatch·rejected·지문 불일치·깨진 JSON은 모두 **`synth_counts=None`, `eligible=False`**였습니다. 정상 최신 시도만 계수했습니다. 읽기 사이 응답 교체 모사에서도 **읽기 1회·fact 3 유지**였습니다.

실제 `_dispatch`·파일 어댑터의 깨진 retry 응답은 **`LaneContractError`, 로그 6행 유지**였습니다. mismatch 응답은 반환되지만 `ok=False, mismatch=True, rejected=False`로 기록됐습니다. 최신 실패를 디스크 좌표로 판별하는 처분은 닫혔습니다.

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**, 조기 검사 **2행**, 완주 **13행**으로 일치했습니다. D의 잔여는 **NG-1**입니다.

**E — 발췌 v4: PASS, 함수·설계 검증 범위**

`ex1/ex2`는 실행하지 않았습니다. 지정 함수들을 import하여 확인했습니다.

- 자기 대조 **27/27**, 후보 풀 역순에서도 **27/27 동일**.
- 5→1 병합: **`[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]`**.
- 표본: **CL-2·4·7·9·12·14·16·19·21·24**.
- 표본 locator **27/27 해소**.

자동 열위는 제거됐습니다. `anchor_state`·`search_note` 표시, 판정 불가·표본 유지·보류/재상신 규칙도 정합합니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

실제 본문에서 `agent/pipeline`을 대체했습니다. `toString`·`constructor`·미지 라벨, `/./`·`//`·`..`, 미지 effort, 좌표·dispatch 중복, 요청/응답 중복·교차·좌표 불일치는 모두 **호출 0회에서 거부**됐습니다.

정상 호출의 model·effort·label 전달을 확인했습니다. true/false/null 보고는 **wrote 1·not_written 1·dropped 1**로 구별하며 null 행에도 run·lane_id·dispatch_id가 남습니다. 문서의 버전 표기만 NG-2입니다.

**G — 결정 공백: REVISE**

새 Owner 재정이 필요한 선택지는 발견하지 못했습니다. 그러나 **명세서 혼입을 추출 실패로 처분하지 않는 공백**이 있습니다. NG-1이 닫히기 전에는 결과 표의 ①·② 지표가 해당 런의 산출이라는 전제가 성립하지 않습니다.

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 전경 `PY -c '…'`로 실행했고, 쓰기 함수는 dict/StringIO로 대체하거나 거부했습니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `961a9a37b4f2a50de22127fe27e0db00ba2e020d` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `def1527e55d95d41833f065e40d0908f0314a825215ae38fad5b289748bc324f` |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md`；절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base→R1/R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `}`；exit 0·`na=[]` |
| 위 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`；exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`；exit 4 |
| CLI `runpy.run_path`·`open/isfile` 대체·판정서/명세 주입 | `METRICS_V9_CLI_REGRESSION_AND_SPEC_BINDING_COMPLETE` |
| 구동 함수·dict/StringIO 증거 대체 | `DRIVE_V6_MEMORY_ONLY_COMPLETE` |
| `git show` 절차→재렌더·발췌 함수 import | `REQUESTS_EXCERPTS_MEMORY_ONLY_COMPLETE` |
| `node -e '…'`·Workflow 본문·agent/pipeline 대체 | `WORKFLOW_V4_MEMORY_ONLY_COMPLETE 14` |
| 최신 디스크 좌표·응답 읽기 대체·실제 `_dispatch` | `SYNTH_SINGLE_READ_LATEST_DISK_COMPLETE` |
| 봉투 stdout 미리보기→실제 `continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 조기 결속·중복 검사 배열 시험 | `ENVELOPE_AND_EARLY_BINDING_COMPLETE` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**[미검증]**

- 실제 Workflow 호출·문맥 격리·transcript/journal 실물 형식·거부물 이동·동시 쓰기.
- source 실행·`read.run` 전체 재개·생산 원장 append. 구동의 엔진 반환/예외는 대체했습니다.
- 외부 원천 TXT·도면. 사본 원천은 **298,507 B·SHA `64d5d627…154e`**, `PATENT_META` 차이는 `[]`였습니다.
- 이전 구동·발췌·Workflow 원본과의 바이트 무변경. 제공된 v6/v4/v4의 본문과 동작을 검증했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort.

**읽은 파일**

- 상류: T40 전문(§1·§4·§5 포함), 좌석 결정문 §17 추기 포함, 1·2차 도전 원문 및 3~8차 지적·처분·검증 부분, SPEC 지정 행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence 스키마, reader-rules·material-spec 스키마.
- 대상: 설계 v3 전문, v3→v9·v8→v9 대조, bundle 스크립트 5종.
- 구현: read의 조기 루프·기록 시점·종결·LaneJournal·dispatch·봉투, source.run, lanes의 plan·contract·file_adapter, paths, read_view, convergence·run_checks·report 관련 함수.
- 실물: 기준 런 run.yaml·원천·명세·조기/완주 판정서·lane-log·요청 6개·통합 응답, donor `cim-fp-3` 명세, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았고, 배경 작업·실측 레인·worktree 작업을 시작하지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다.