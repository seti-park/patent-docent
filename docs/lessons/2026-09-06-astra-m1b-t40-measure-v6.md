# 독립 감수 원문 — M1b 설계 도전 6차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v6 · 판정 REVISE(MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `a42656715f36cf10dc65150fc20d8487ec08671307fbe44729b8dd2e1a8de609` · 16485 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v6/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 06:32:10 → 06:44 · **USAGE = input 3,895,055(cached 3,565,440) · output 18,198(reasoning 2,544)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `82b75ee` · `bundle/T40-MEASURE-DESIGN.md` v6 sha256 `4506d419…2c1d` · v1~v5 동봉 · 구동·지표 v6 · 발췌·Workflow v4). 폐쇄 = **이전 지적 35건 중 closed 33 · partially 2(MY-5·MZ-5 — ND-2 로 좁혀짐) · open 0**. 5차 지정 반례 전건 닫힘(실제 `enter` SystemExit → 14 + 증거 · 단일 읽기 · `checks=null`·bool·음수·범위 밖·NaN → 4). **B·C·E·F PASS**(확인 범위) · D 만 REVISE.

**판정 = REVISE · 2건(MED 2) · 기각 0 · 전부 발주자 귀책.** **ND-1 MED**: v6 가 선언한 「findings 형태 검증」이 구현에 없음 — `findings` null/{}/[null]/문자열/부재 전부 수용(계약은 필수 배열 · finding 객체). **ND-2 MED**: synthesize 응답의 지문(`sha(resp)`)과 계수(`load(resp)`)가 **서로 다른 읽기** → 읽기 사이 교체 모사에서 지문 일치·적격인데 fact 0 계수(해시한 바이트 ≠ 계수한 바이트).

지적 열거 = ND-1, ND-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 5**. **전부 수용 → 지표 스크립트 v7 + 설계 메모 v7 → M1b 7차 도전(지적 `NE-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 지적 35건은 closed 33건·partially 2건·open 0건입니다.** 5차 NC-1~3의 원 반례는 닫혔습니다. 다만 통합 응답의 지문과 계수가 서로 다른 바이트에서 나올 수 있어 MY-5·MZ-5는 완전 폐쇄로 판정하지 못합니다. 새 지적은 **MED 2건**입니다.

사본 마커의 path·pin·order·disposable과 실제 HEAD `82b75ee8dc38cc870125c69f67f11e945422d051`이 일치했습니다. v6 SHA-256은 `4506d419ba3cf8423e45f830597bc0347a9419fcaf33bdf596f6f3a1a5292c1d`입니다.

**A — 원장 정합·폐쇄표: REVISE**

폐쇄는 원 지적의 범위를 기준으로 판정했습니다. NC-2의 스냅샷 재독·검사 배열 변환은 수정됐으며, v6가 추가로 약속한 `findings` 형태 검증 누락은 ND-1로 구별합니다.

| 지적 | v6 판정 | 확인·잔여 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree·최초 요청 6/6 동일 |
| MY-2 | closed | 잡음 폭 방향 미확정으로 한정 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정·자동 열위 없음 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | **partially** | 수확 fact 혼입·최신 실패 후퇴는 수정. 계수한 응답의 지문 결속은 ND-2 |
| MY-6 | closed | 6축·회차·계수 쌍·수치 범위 검증 확인 |
| MY-7 | closed | 검사 배열·findings 보존·귀속 추정 표시 |
| MY-8 | closed | 실제 진입 실패까지 14로 변환 |
| MY-9 | closed | A-a→A-b 순서가 러너 제어 흐름과 일치 |
| MY-10 | closed | 완료 구별·경로 거부·발주 거부 시 무차감 |
| MY-11 | closed | 소비 전 실호출 대조·dispatch별 이동 보존 명시 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 보존 명시 |
| MY-13 | closed | 생산 원장은 운영 선택·누적량은 메모 보유 종결 런 수 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 제시 |
| MZ-2 | closed | 축 0 별도 보존·최초 실행 판정 유지·N/A 처분 |
| MZ-3 | closed | 필수 스냅샷·런/국면/실행/축/지문 대조 확인 |
| MZ-4 | closed | 실제 상수·정상 분류·예외 경계 확인 |
| MZ-5 | **partially** | 최신 부적격 시도는 N/A. 해시한 바이트와 계수한 바이트가 갈리는 ND-2 |
| MZ-6 | closed | 중복 검사·추정 귀속·findings·escalations 확인 |
| MZ-7 | closed | 부모 대조·numstat·동일성 범위 확인 |
| MZ-8 | closed | dispatch별 증거·상한·거부 시 회차 불변 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로 사전 거부 |
| NA-1 | closed | 로그 없는 최신 디스크 시도도 선택하여 N/A |
| NA-2 | closed | 진입·스냅샷·후처리 예외 및 phase 모순 처리 |
| NA-3 | closed | 조회 무쓰기·확정 발주만 계수 |
| NA-4 | closed | 런 식별자·필수 축/계수·형태 오류 거부 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 사전 거부 |
| NA-7 | closed | 인용 부재 등의 판정 불가·표본 유지·재상신 명시 |
| NB-1 | closed | 실제 진입 실패·증거 기록 실패 모두 14 |
| NB-2 | closed | 발주 전건 검사·거부 무기록·부분 기록 복구 처분 |
| NB-3 | closed | 지정 형태·계수·수치 반례 거부 |
| NC-1 | closed | 실제 `enter`의 SystemExit 2/3→14·증거 생성 |
| NC-2 | closed | 스냅샷 읽기 1회·`checks=null`→4 |
| NC-3 | closed | bool·음수 계수·범위 밖 Jaccard·NaN→4 |

§8의 격은 유지됩니다. **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕ는 재정 문언 이행**, **ⓖ는 §0′ 범위에 한정한 동일화 이행**입니다. **ⓘ는 표본 단위 이행과 인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행과 후보 표시 재량**, **ⓝ는 근거 부족 시 재상신하는 문언 이행**입니다.

`partial/read`, 봉투 대상 3런, exact-match·청구항 실패의 봉투 배제는 원장과 맞습니다. G-12의 미집행이 해결됐다는 뜻으로 확대하지 않았습니다.

**지적 목록 — MED 2건**

**ND-1 · MED — 약속한 `findings` 형태 검증이 없다.**

좌표: 메모 §5 추출기 설명·§9 D; [t40_metrics.py:123](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:123), `metrics/early_findings`.

v6는 “checks·findings 형태 검증”을 선언하지만, 구현은 checks만 객체 배열인지 확인하고 findings는 `e.get("findings")`로 복사합니다. 실제 계약은 findings를 필수 배열로 선언하고 원소를 finding 객체로 제한합니다.

정상 기준 판정서를 복제하여 각 수정본에 맞는 sidecar를 공급했습니다.

| 대입 | 실행 결과 |
|---|---|
| `findings=null` | 수용·`early_findings=None`·`na=[]` |
| `findings={}` | 수용·`early_findings={}`·`na=[]` |
| `findings=[null]` | 수용·`early_findings=[None]`·`na=[]` |
| `findings="lost findings"` | 수용·문자열 그대로 출력·`na=[]` |
| findings 삭제 | 수용·`early_findings=None`·`na=[]` |

검사 실패 내용의 결측·손상을 정상 추출과 구별하지 못합니다. 이는 정상 러너가 이런 문서를 생성한다는 주장이 아니라, **v6가 명시한 검증 범위의 실행 반례**입니다.

고치는 문안: **“스냅샷 findings는 필수 배열이며 각 원소가 계약의 finding 형태를 만족하는지 같은 exit 4 경계에서 검증하고, 부재·null·형태 위반은 추출 실패로 종료한다.”**

**ND-2 · MED — 통합 응답의 해시와 계수를 다른 읽기에서 만들어 잘못된 계수를 적격으로 보고한다.**

좌표: 메모 §5 ㉣; [t40_metrics.py:184](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:184), `metrics/synth_attempts`.

184행은 `sha(resp)`로 응답을 읽고 로그 지문과 대조합니다. 다음 행은 `load(resp)`로 **같은 경로를 다시 읽어** kind를 셉니다. 두 번째 읽기의 바이트는 지문 대조 대상이 아닙니다.

파일 쓰기 없이 `t40_metrics.open`만 대체했습니다. 첫 읽기에는 기준 응답 원본을, 두 번째 읽기에는 그 원본에서 fact 항목을 제거한 JSON을 반환했습니다.

```text
SYNTH_REPLACED_AFTER_SHA reads ['rb', 'r'] digest_match True eligible True fact 0 na []
HASHED_FACT 3 COUNTED_BYTES_MATCH_LOG False
```

**지문을 확인한 응답에는 fact 3건이 있지만, 적격 통합 지표에는 fact 0건이 실립니다.** MZ-5의 “응답 지문과 로그 대조”가 실제 계수에까지 결속되지 않았습니다. ND-2는 읽기 사이 교체를 모사한 반례이며, 실제 동시 변경이 발생했다고 주장하지 않습니다.

고치는 문안: **“각 synthesize 응답을 바이트로 한 번 읽어 그 바이트의 SHA를 로그와 대조하고 동일 바이트를 파싱·계수하며, 읽기·파싱·지문 대조 실패는 해당 시도 부적격·㉣ N/A로 처리한다.”**

**B — 계측 커밋 셋: PASS, 확인한 정적 범위**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base↔각 팔은 `contracts/stages/read.yaml` **2 additions/2 deletions**뿐입니다.

절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였고 aliases도 일치했습니다.

§0′의 `d4e6ca2→6d92cad` 열거는 재실측과 맞습니다.

| 파일 | additions/deletions |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

규칙·material-spec 스키마도 동일했습니다. 기준 요청 **6/6 재렌더 바이트 동일**, 최초 분해 요청 차이 필드 `[]`입니다. 실제 finding을 넣은 재시도 요청에서는 **소견이 본문에 들어가고 지문이 바뀌었습니다.** 최초 요청 동일성을 재시도까지 확대하지 않은 문언은 타당합니다.

**C — 구동 v6: PASS, 메모리 대체 실행 범위**

실제 `enter`를 유지하고 `REPO`를 사본으로, 증거 쓰기를 메모리로 바꿨습니다.

```text
ACTUAL_ENTER r0 14 EXC_FILES 1 SYSTEMEXIT_IN_EVIDENCE True
ACTUAL_ENTER bad-run 14 EXC_FILES 1 SYSTEMEXIT_IN_EVIDENCE True
```

정상 분류 0·10·11·12·13·14, 예외 뒤 포인터 true→13/false→14, 대기 포인터와 full 국면의 모순→14를 확인했습니다. 실제 기록 함수의 디렉터리 생성·파일 쓰기 실패는 종결 포인터가 true여도 **14**였습니다. 스냅샷 실패도 정상 반환·pending·엔진 예외 뒤 모두 **14**였습니다.

| 발주 | 종료 | 회차 | 새 파일 쓰기 |
|---|---:|---:|---:|
| A | 0 | 1 | 3 |
| A 반복 | 14 | 1 | 0 |
| A 반복 | 14 | 1 | 0 |
| B | 0 | 2 | 3 |
| C | 0 | 3 | 3 |
| D | 15 | 3 | 0 |

뒤 좌표의 상한 초과는 **15·쓰기 0**, 뒤 args 충돌은 **14·쓰기 0**, `lanes` 4회 조회는 **쓰기 0**입니다. `_next_dispatch`는 현 파일에 없으며 계수 경로인 `cmd_dispatch`를 시험했습니다.

스냅샷은 축 0 문서를 별도 보존하고 최초 실행 attempt 1을 유지했습니다. exit 14는 엔진 비종결을 뜻하지 않으며 T38의 세 종결 근거는 `_run_is_terminated`가 판정합니다.

**D — 지표 v6: REVISE**

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**, 조기 검사 2행·완주 13행으로 일치했습니다.

| 5차 반례 | v6 결과 |
|---|---|
| `SECOND_SHA_PERMISSION` | **읽기 1회·정상 추출**. 두 번째 읽기가 없어 오류 주입점에 도달하지 않음 |
| `CHECKS_NULL` | exit 4 |
| `[true,true]`, `[-1,-1]` | 각각 exit 4 |
| `jaccard=true/2.0/NaN` | 각각 exit 4 |

런·국면·SHA 불일치, executed=1, 축 누락·중복·null 원소, 계수·Jaccard 누락도 모두 **4**였습니다.

최신 디스크 시도는 올바르게 선택합니다. 로그 없음·mismatch·지문 불일치는 모두 **`synth_counts=None`**이고, 정상 최신 시도만 계수합니다. 실제 `_dispatch`와 파일 어댑터에 깨진 retry 응답을 넣었을 때도 **`LaneContractError·LOG_ROWS 6`**으로, 로그 밖 최신 실패가 존재하는 경로를 확인했습니다.

검사 fail/read-a·pass/read-b 두 행과 finding 1건도 보존됐습니다. 남은 것은 ND-1·2입니다.

**E — 발췌 v4: PASS, 설계·함수 확인 범위**

생성 함수 `ex1/ex2`는 실행하지 않았습니다. `candidates/comp_texts_fn/sample_indices`를 import하여 확인했습니다.

- 자기 대조 **27/27**, 후보 풀 역순에서도 동일.
- 5→1 병합: **`[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]`**.
- 표본: **CL-2·4·7·9·12·14·16·19·21·24**.
- 표본 locator **27/27 해소**.

자동 열위는 없습니다. `anchor_state`·`search_note` 표시와 판정 불가·표본 유지·보류/재상신 규칙도 원장과 맞습니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

본문을 Node에서 실행하고 `agent/pipeline`만 대체했습니다. `toString`·`constructor`·`/./`·`//`·`..`·미지 effort·좌표/dispatch 중복·요청/응답 중복·교차·좌표 불일치는 모두 **호출 0회에서 거부**됐습니다.

정상 입력은 지정 model·effort로 전달됐습니다. true/false/null 보고에서 `wrote_true=1`, `not_written=1`이며 null 행에도 run·lane_id·dispatch_id가 남았습니다. 실호출 검증·이동 보존 절차는 명시돼 있습니다.

**G — 결정 공백: REVISE**

새로운 Owner 재정이 필요한 선택지는 발견하지 못했습니다. 그러나 **손상 findings의 정상 수용과 지문이 결속하지 않은 통합 계수의 적격 처리**가 선등록한 검증·N/A 처분과 어긋납니다. 이 상태의 결과 표를 ①② 재정 근거로 사용할 수 있다고 판정하지 않습니다.

**검증 경로**

모든 cwd는 지정 사본입니다. `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 전경 `PY -c '…'`로 실행했으며 아래에 호출 함수와 대체 범위를 명시합니다.

| 명령·실행 경로 | 마지막 출력 또는 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `82b75ee8dc38cc870125c69f67f11e945422d051` |
| `sha256sum bundle/T40-MEASURE-DESIGN*.md` | v6 `4506d419ba3cf842…5292c1d`; v1~v5 존재·해시 확인 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base↔R1/R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` — 위 표 재계수 |
| `git diff --stat origin/t40-base HEAD -- engine reader/lib contracts` | 빈 출력 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}`, exit 0·`na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`·exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`·exit 4 |
| `PY -c '…metrics·일치 sidecar·open/isfile 대체…'` | `METRICS_SNAPSHOT_MEMORY_ONLY_COMPLETE` — ND-1 포함 |
| `PY -c '…metrics·통합 응답의 연속 읽기 바이트 대체…'` | `SYNTH_MEMORY_ONLY_COMPLETE` — ND-2·최신 시도 N/A 포함 |
| `PY -c '…실제 enter/classify/snapshot·메모리 증거…'` | `DRIVE_READ_MEMORY_ONLY_COMPLETE` |
| `PY -c '…cmd_dispatch·dict/StringIO 파일 대체…'` | `DISPATCH_MEMORY_ONLY_COMPLETE` |
| `PY -c '…git show 절차→재렌더·발췌 함수…'` | `NO_EXCERPT_GENERATOR_EXECUTED_ALL_CHECKS_IN_MEMORY` |
| `node -e '…Workflow 본문·agent/pipeline 대체…'` | `WORKFLOW_BODY_MEMORY_ONLY_NO_REAL_AGENT_CALLS` |
| 봉투 stdout 미리보기→실제 `continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**[미검증]**

- 실제 Workflow 호출·문맥 격리·transcript/journal 형식·거부물 이동·동시 쓰기는 실행하지 않았습니다. ND-2는 메모리로 읽기 사이 교체를 모사했습니다.
- source 실행·`read.run` 전체 재개·생산 원장 기록은 하지 않았습니다. 구동 시험은 엔진 반환/예외를 대체했고 `_dispatch`·파일 어댑터·봉투 검증기는 직접 실행했습니다.
- 외부 원천 TXT·도면은 열지 않았습니다. 사본 원천은 **298,507 B·SHA `64d5d627…154e`**, PATENT_META 차이는 `[]`였습니다.
- 이전 스크립트 원본과의 **발췌·Workflow 바이트 무변경**은 증명하지 않았습니다. 현재 제공된 v4 본문과 함수 동작을 확인했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 전문, 좌석 결정문 §17 추기 포함, MY·MZ·NA·NB·NC 도전 원문, SPEC §8.4 지정 행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence 스키마, reader-rules·material-spec 스키마 대조.
- 대상: 설계 v3·v6, v5→v6 차이, 전 판본 해시, 스크립트 5종.
- 구현: read의 조기 루프·판정서 기록·종결·LaneJournal·dispatch·봉투 경로, source.run, lanes의 plan·contract·file_adapter, paths, read_view, convergence·run_checks·report 관련 함수.
- 기준 런: run.yaml·source-report·patent.md·material-spec·조기/완주 판정서·lane-log·요청 JSON/MD 6개·통합 응답, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았고 배경 작업이나 실측 레인을 시작하지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다.