# 독립 감수 원문 — M1b 설계 도전 7차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v7 · 판정 REVISE(MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `1e4812349e4e32f5f4cfe46bec63bc9779bed529a0985f09453627293c2a74b4` · 17503 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v7/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 06:47:28 → 06:58 · **USAGE = input 2,991,310(cached 2,798,720) · output 18,656(reasoning 3,095)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `d98ea3b` · `bundle/T40-MEASURE-DESIGN.md` v7 sha256 `185e3eb5…9d13` · v1~v6 동봉 · 지표 v7). 폐쇄 = **이전 37건 closed 36 · partially 1(ND-1 → NE-2 로 좁혀짐) · open 0**. ND-2 닫힘(교체 모사에서 응답 읽기 1회 · fact 3 유지). **B·C·E·F PASS**(확인 범위) · D 만 REVISE.

**판정 = REVISE · 2건(MED 2) · 기각 0 · 전부 발주자 귀책.** **NE-1 MED**: 완주 판정서 경로가 선언(「완주 판정서도 같은 형태 검증」)보다 좁음 — 축·계수·수치 검증 없음 · `axes_of`·`attribute_read_runs` 가 try 밖(`axes=null` → TypeError · 프로세스 exit 1 · 축 제거·bool·음수·NaN 수용 · `check_id=[]` TypeError). **NE-2 MED**: ND-1 「계약 finding 형태」를 「객체이기만 함」으로 축소 — `[{}]`·`message=null`·`locus` 누락 수용(계약 `$defs/finding` 은 6 필수 문자열).

지적 열거 = NE-1, NE-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 6**. **전부 수용 → 지표 v8(완주 판정서 = 조기와 같은 형태·수치 검증 + 합법적 미실행 구별 · findings 원소를 `convergence.schema.json#$defs/finding` 으로 jsonschema 검증) + 설계 v8 → M1b 8차 도전(지적 `NF-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 지적 37건은 closed 36건·partially 1건(ND-1)·open 0건입니다.** ND-2의 지문·계수 분리는 닫혔습니다. 새 지적은 **MED 2건**입니다. 완주 판정서 검증이 선언보다 좁고, findings 원소의 계약 형태 검증이 남아 있어 실측 착수에 PASS를 줄 수 없습니다.

사본 마커의 path·pin·order·disposable, 실제 작업 경로와 HEAD `d98ea3b104bbe3742dd80d629a5cc7ba689cde5f`가 일치했습니다. 메모 SHA-256은 `185e3eb57715096d1231b2626bf4f5ebf215f7750525e14599e3f91fdaf99d13`입니다.

**A — 원장 정합·이전 지적 폐쇄: REVISE**

폐쇄는 **원 지적의 범위**로 판정했습니다. v7이 새로 확대한 완주 검증 약속의 결함은 NE-1로, ND-1의 미이행 잔여는 NE-2로 구별합니다.

| 지적 | v7 판정 | 확인·잔여 |
|---|---|---|
| MY-1 | closed | 고정 핀·절차 tree·최초 요청 6/6 동일 |
| MY-2 | closed | 잡음 폭 확대·축소 방향 미확정으로 한정 |
| MY-3 | closed | 기준 27단위·Owner 명시 판정·자동 열위 제거 |
| MY-4 | closed | 종속 청구항 10개·항 내 additions 전부 |
| MY-5 | closed | 수확 fact 제외·최신 실패 N/A·계수 바이트의 지문 결속 확인 |
| MY-6 | closed | 첫 조기 판정·6축·계수 쌍·수치 검증 확인 |
| MY-7 | closed | 검사 배열·findings 보존·귀속 추정 구별 |
| MY-8 | closed | 진입·스냅샷·기록 실패와 정상 종료 분류 확인 |
| MY-9 | closed | A-a→엔진→A-b가 러너의 순차 dispatch 흐름과 일치 |
| MY-10 | closed | 완료 구별·경로 사전 거부·거부 발주 무차감 |
| MY-11 | closed | 소비 전 실호출 확인·dispatch별 이동 보존 명시 |
| MY-12 | closed | 성공·실패·대기 런과 외부 실행층 보존 명시 |
| MY-13 | closed | 생산 원장은 운영 선택·증가량은 메모 보유 종결 런 수 |
| MZ-1 | closed | 5→1 병합에서 다섯 단위 모두 같은 후보 제시 |
| MZ-2 | closed | 축 0 별도 보존·첫 실행 판정 유지·결측 재상신 |
| MZ-3 | closed | 필수 스냅샷·런/국면/실행/축/지문 대조 |
| MZ-4 | closed | 실제 상수·예외 경계·모순 상태 분류 확인 |
| MZ-5 | closed | 마지막 부적격 시도 N/A·동일 응답 바이트로 해시와 계수 |
| MZ-6 | closed | 중복 검사·추정 귀속·findings·escalations 보존 |
| MZ-7 | closed | 부모 대조·numstat·최초 요청 동일성의 범위 일치 |
| MZ-8 | closed | dispatch별 증거·상한·거부 시 회차 불변 |
| MZ-9 | closed | 상속 속성 라벨·비정규 경로 사전 거부 |
| NA-1 | closed | 로그 없는 최신 디스크 시도도 선택하여 N/A |
| NA-2 | closed | 진입·스냅샷·후처리 예외 및 phase 모순 처리 |
| NA-3 | closed | 조회 무쓰기·발주 확정 시 계수 |
| NA-4 | closed | 런 식별자·축/계수 결측·sidecar/JSON 오류 거부 |
| NA-5 | closed | 다중 기록 불가능 주장 삭제·보존 보증 범위 한정 |
| NA-6 | closed | 요청/응답 중복·교차·좌표 불일치 사전 거부 |
| NA-7 | closed | 인용 부재 등 판정 불가·표본 유지·재상신 명시 |
| NB-1 | closed | 실제 진입 실패·증거 기록 실패 모두 14 |
| NB-2 | closed | 배치 충돌 사전 검사·거부 무차감·부분 기록 복구 처분 |
| NB-3 | closed | 조기 스냅샷의 지정 형태·필수 지표 반례 거부 |
| NC-1 | closed | 실제 `enter`의 SystemExit 2/3→14·예외 증거 |
| NC-2 | closed | 조기 스냅샷 단일 읽기·검사 변환 오류→4 |
| NC-3 | closed | 조기 bool·음수 계수·범위 밖 Jaccard·NaN→4 |
| ND-1 | **partially** | 지정된 컨테이너 반례는 닫힘. 계약 finding의 필수 필드·타입 미검증: NE-2 |
| ND-2 | closed | 교체 모사에서도 응답 읽기 1회·fact=3 유지 |

T40 §4·§5의 3런 구성, `partial/read`, 봉투 대상 한정, exact-match·청구항 실패의 봉투 배제는 맞습니다. G-12의 미집행을 해결했다는 뜻으로 확대할 수는 없습니다.

§8의 격도 유지됩니다. **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕ는 재정 문언 이행**, **ⓖ는 §0′ 범위의 동일화 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**, **ⓝ는 근거 부족 시 재상신하는 문언 이행**입니다.

**지적 목록 — MED 2건**

**NE-1 · MED — 완주 판정서의 검증·변환은 선언한 exit 4 경계에 들어 있지 않다.**

좌표: 메모 §5 추출기 설명의 **“완주 판정서도 같은 형태 검증”**; [t40_metrics.py:134](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:134), `metrics/full`, `axes_of`, `attribute_read_runs`.

완주 경로는 최상위 객체와 checks/findings의 객체 배열 여부만 검사합니다. 축·계수·수치 검증은 없고, **`axes_of(c)`와 `attribute_read_runs(fchecks)`는 try 밖**인 142~143행에서 실행됩니다.

정상 조기 스냅샷과 일치 sidecar를 유지하고 완주 판정서만 바꾼 결과입니다.

| 완주 판정서 대입 | v7 결과 |
|---|---|
| `axes=null` | **미포착 TypeError** |
| 실행된 판정서에서 축 하나 제거 | **수용·`na=[]`** |
| `independent_count=[true,true]` | **수용·`na=[]`** |
| `independent_count=[-1,-1]` | **수용·`na=[]`** |
| Jaccard `NaN` 또는 `2.0` | **수용·`na=[]`** |
| 검사 행의 `check_id=[]` | **미포착 TypeError** |

`axes=null`은 실제 CLI 본문을 `runpy`로 실행해 **프로세스 exit 1**까지 확인했습니다. 같은 손상은 조기 스냅샷에서는 모두 exit 4입니다.

고치는 문안: **“완주 판정서도 국면·실행 상태에 맞는 축·계수·수치·검사 형태를 검증하고 출력 변환까지 동일한 exit 4 경계에 두며, 합법적 수렴 미실행과 손상을 구별한다.”**

**NE-2 · MED — ND-1의 ‘계약 finding 형태’를 ‘객체이기만 함’으로 축소했다.**

좌표: ND-1 원문의 고치는 문안; 결정문 §17 추기 5; 메모 §5; [t40_metrics.py:123](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:123)·139행; [convergence.schema.json:344](/home/laptop/projects/workspaces/pd-m1b-t40/contracts/schemas/convergence.schema.json:344).

v7은 배열·객체 여부까지는 약속대로 구현했습니다. 그러나 ND-1 원문은 **“각 원소가 계약의 finding 형태를 만족”**하도록 요구했습니다. 계약은 `check·rule·locus·found·expected·message`를 필수 문자열로 두고, `check·message`에는 최소 길이도 둡니다.

실제 계약 검증기와 추출기를 같은 원소에 대조했습니다.

| `findings` 대입 | 조기·완주 추출 | finding 계약 검증 |
|---|---|---|
| `[{}]` | **모두 수용·`na=[]`** | 필수 필드 오류 6건 |
| 필드 6개 중 `message=null` | **모두 수용·`na=[]`** | 타입 오류 1건 |
| `locus`만 누락 | **모두 수용·`na=[]`** | 필수 필드 오류 1건 |

빈 객체는 결함의 좌표·실측·기대·메시지가 전부 사라진 입력입니다. 이를 정상 findings로 출력하므로 **ND-1의 지정 반례 통과와 원 지적의 완전 폐쇄는 다릅니다.**

고치는 문안: **“조기·완주 findings의 각 원소를 `convergence.schema.json#$defs/finding`과 대조하여 필수 필드·타입·문자열 제약 위반도 exit 4로 거부한다.”**

두 지적 모두 **손상 입력에 대한 검증 반례**입니다. 정상 러너가 해당 손상을 생성한다거나 실제 런에서 발생했다는 주장은 아닙니다.

**B — 계측 커밋 셋: PASS, 확인한 정적·메모리 실행 범위**

부모는 `ad4c6c3←6d92cad`, `530b096←ad4c6c3`, `00e0bed←ad4c6c3`입니다. base↔각 팔은 `contracts/stages/read.yaml` **2 additions/2 deletions**뿐입니다.

절차 tree는 기준과 base 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`이며, §0′의 절차 5개 blob·read.yaml 3개 blob도 일치했습니다. `lane_profiles` 직접 호출에서 R1은 분해·통합만 xhigh, R2는 종속 접지만 sonnet/high였습니다.

`d4e6ca2→6d92cad` 재실측도 열거와 맞습니다.

| 파일 | additions/deletions |
|---|---:|
| read.yaml / convergence.schema / run-kinds | 321/31 · 42/7 · 24/2 |
| read.py / source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| run_checks.py / convergence.py / dependency_parse.py | 90/35 · 32/5 · 30/1 |
| material_spec_md.py | 85/1 |
| paths.py / stages/__init__.py / reader/lib/__init__.py | 19/0 · 69/0 · 4/0 |
| lanes/plan.py / file_adapter.py / replay_adapter.py | 2/7 · 6/4 · 2/2 |

규칙·material-spec 스키마 동일성도 확인했습니다. 기준 요청서 **6/6 재렌더 바이트 동일**, 신규 최초 분해 요청 차이 필드 `[]`입니다. 같은 재시도 좌표에서 finding을 추가하면 **본문에 소견이 들어가고 지문이 바뀝니다.** 최초 요청 동일성을 재시도까지 확대하지 않은 문언은 타당합니다.

**C — 구동 v6: PASS, 메모리 대체 실행 범위**

실제 `enter`를 유지하고 `REPO`를 사본으로, 증거 쓰기를 dict/StringIO로 대체했습니다.

```text
ACTUAL_ENTER r0 14 EXC_FILES 1 SYSTEMEXIT_IN_EVIDENCE True
ACTUAL_ENTER bad-run 14 EXC_FILES 1 SYSTEMEXIT_IN_EVIDENCE True
```

정상 종결→0, pending→10, 조기 escalation→11, 조기 exact-match·claim-checks→12, 종결 실패→13, 상태 모순→14를 확인했습니다. 예외 뒤 포인터 true→13/false→14이며, **스냅샷 실패·증거 기록 실패는 14**였습니다.

발주 `A,A,A,B,C,D`의 종료 코드는 **0,14,14,0,0,15**, 누적 회차는 **1,1,1,2,3,3**입니다. 거부된 발주는 새 파일을 만들지 않았고, `lanes` 네 번 조회는 쓰기 0입니다. `_next_dispatch`는 현 파일에 없으므로 실제 계수 경로인 `cmd_dispatch`를 시험했습니다.

스냅샷은 축 0 문서를 별도 보존하고 최초 실행 attempt 1을 유지했습니다. exit 14와 T38의 엔진 종결 여부를 구별한 설명도 맞습니다.

**D — 지표 v7: REVISE**

기준값은 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**, 조기 검사 2행·완주 13행으로 일치했습니다.

ND-1의 지정 반례 `null/{}/[null]/문자열/부재`는 **조기 5건·완주 5건 모두 exit 4**였습니다. 잔여는 원소 내부의 계약 형태인 NE-2입니다.

ND-2 재시험 결과는 다음과 같습니다.

```text
SYNTH_REPLACED_AFTER_SHA reads ['rb'] digest_match True eligible True fact 3 na []
```

두 번째 읽기에 fact를 제거한 응답을 공급하도록 했지만 **두 번째 읽기가 발생하지 않았습니다.**

최신 디스크 좌표 `read-a/synthesize/retry-1/batch-0`에 대해 로그 없음·mismatch·지문 불일치·깨진 JSON은 모두 **`synth_counts=None`, `eligible=False`**였고, 정상 최신 시도만 계수했습니다. 실제 `_dispatch`·파일 어댑터의 깨진 retry 응답도 **`LaneContractError`, 로그 6행 유지**로 확인했습니다.

검사 fail/read-a·pass/read-b 두 행과 finding 1건도 보존됩니다. 조기 스냅샷의 기존 수치·결측·단일 읽기 반례는 닫혔으며, 완주 경로의 잔여는 NE-1입니다.

**E — 발췌 v4: PASS, 설계·함수 확인 범위**

`ex1/ex2` 생성 함수는 실행하지 않았습니다. `candidates/comp_texts_fn/sample_indices`를 import하여 확인했습니다.

- 자기 대조 **27/27**, 후보 풀 역순에서도 **27/27 동일**.
- 5→1 병합: **`[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]`**.
- 표본: **CL-2·4·7·9·12·14·16·19·21·24**.
- 표본 locator **27/27 해소**.

자동 열위는 없습니다. `anchor_state`·`search_note` 표시, 인용 부재·단락 미해소·접지 부재의 판정 불가, 표본 유지·재상신 처분도 원장과 맞습니다.

**F — Workflow v4: PASS, Node 대체 실행 범위**

본문을 Node에서 실행하고 `agent/pipeline`을 대체했습니다. `toString`·`constructor`·`/./`·`//`·`..`·미지 effort·좌표/dispatch 중복·요청/응답 중복·교차·좌표 불일치는 모두 **호출 0회에서 거부**됐습니다.

정상 입력은 지정 model·effort로 전달됐습니다. true/false/null 보고는 **`wrote_true=1`, `not_written=1`**, null 행에는 run·lane_id·dispatch_id가 남았습니다. 실호출 확인과 거부물 이동 보존의 운영 규칙도 명시돼 있습니다.

**G — 결정 공백: REVISE**

새로운 Owner 재정이 필요한 선택지는 발견하지 못했습니다. 그러나 **손상 판정서가 정상 결과로 수용되거나 선언한 종료 코드 밖으로 빠지는 처분 공백**이 남습니다. NE-1·2가 닫히기 전에는 결과 표의 검증 범위를 메모대로 보증할 수 없습니다.

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 전경 `PY -c '…'`로 수행했습니다.

| 명령·실행 경로 | 마지막 출력 또는 핵심 판정 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `d98ea3b104bbe3742dd80d629a5cc7ba689cde5f` |
| `sha256sum bundle/T40-MEASURE-DESIGN*.md` | v7 `185e3eb57715096d…af99d13`; v1~v6 해시 확인 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| base↔R1/R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | `139 0 reader/procedure/HISTORY.md` — 위 변경표 재계수 |
| `git diff --stat origin/t40-base HEAD -- engine reader/lib contracts` | 빈 출력 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}`, exit 0·`na=[]` |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다(MZ-3)`·exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json`·exit 4 |
| `metrics`에 정상 sidecar·수정 판정서 공급, `open/isfile` 대체 | `METRICS_FINDINGS_AND_FULL_PARITY_MEMORY_COMPLETE` — 지정 10건은 4, 완주 손상은 수용/미포착 |
| `runpy.run_path`로 CLI 실행, 완주 `axes=null` 읽기만 대체 | `TypeError: 'NoneType' object is not iterable`·**프로세스 exit 1** |
| findings 원소를 추출기와 계약 검증기에 함께 공급 | `FINDING_OBJECT_CONTRACT_MEMORY_COMPLETE` — 조기·완주 수용, 계약 오류 |
| 통합 응답 연속 읽기 바이트 및 최신 디스크 좌표 대체 | `SYNTH_SINGLE_READ_AND_LATEST_DISK_MEMORY_COMPLETE` |
| 조기 스냅샷의 기존 형태·수치·재독 반례 | `PRIOR_SNAPSHOT_COUNTEREXAMPLES_COMPLETE` |
| 실제 enter·classify·snapshot·dispatch, 증거만 메모리 대체 | `DRIVE_MEMORY_ONLY_COMPLETE` |
| `git show` 절차→요청 재렌더·발췌 함수·검사 직렬화 | `REQUESTS_EXCERPTS_CHECKS_MEMORY_ONLY_COMPLETE` |
| `node -e '…Workflow 본문…'`·agent/pipeline 대체 | `WORKFLOW_BODY_MEMORY_ONLY_NO_REAL_AGENT_CALLS` |
| 봉투 stdout 미리보기→실제 `continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no` | 빈 출력 |

**[미검증]**

- 실제 Workflow 호출·문맥 격리·transcript/journal 실물 형식·거부물 이동·동시 쓰기는 실행하지 않았습니다.
- source 실행·`read.run` 전체 재개·생산 원장 append는 하지 않았습니다. 구동 시험의 엔진 반환/예외는 대체했고, `_dispatch`·파일 어댑터·봉투 검증기는 직접 실행했습니다.
- 외부 원천 TXT·도면은 열지 않았습니다. 사본 원천은 **298,507 B·SHA `64d5d627…154e`**, PATENT_META 차이는 `[]`이며 도면 20개는 보관 source-report의 기록까지 확인했습니다.
- 이전 구동·발췌·Workflow 스크립트 원본과의 **바이트 무변경**은 증명하지 않았습니다. 현재 제공된 v6/v4/v4 본문과 동작을 확인했습니다.
- 시간·토큰 환산·가용 메모리·09-01 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 전문, 좌석 결정문 §17 추기 포함, MY·MZ·NA·NB·NC·ND 도전 원문의 지적·처분·검증 부분, SPEC §8.4 지정 행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence 스키마, reader-rules·material-spec 스키마 대조.
- 대상: 설계 v3·v7 본문, v6→v7 차이, 전 판본 해시, bundle 스크립트 5종.
- 구현: read의 조기 루프·판정서 기록·종결·LaneJournal·dispatch·봉투 경로, source.run, lanes의 plan·contract·file_adapter, paths, read_view, convergence·run_checks·report 관련 함수.
- 기준 런: run.yaml·source-report·patent.md·material-spec·조기/완주 판정서·lane-log·요청 JSON/MD 6개·통합 응답, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 쓰지 않았으며 배경 작업이나 실측 레인을 시작하지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다.