# 독립 감수 원문 — M1b 설계 도전 14차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v14 · 판정 REVISE(MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `5290e4e1ba42d10f1b2de37111e61d2bc8a5e269be89a09d8d3aa2c2d6faa91a` · 12740 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v14/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 08:34:59 → 08:47 · **USAGE = input 3,867,139(cached 3,673,216) · output 18,706(reasoning 2,840)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `f4d1744` · v14 sha256 `ccc6a8ea…` · v1~v13 동봉 · 지표 v14). 폐쇄 = **이전 48건 closed 47 · partially 1(MZ-2 → NL-1) · open 0**(NK-1 닫힘 · 스키마 전체 검증 작동 확인). **B·C·E·F PASS**(9회 연속).

**판정 = REVISE · 1건(MED) · 기각 0 · 발주자 귀책.** **NL-1 MED**: 스키마는 필드 존재·형태만 보증 — grounding 전량 제거 · component 전량 제거 · `dependents=[]` 는 스키마 오류 0 인데 정상 0건·빈 분포로 출력(`synth_eligible=true · na=[]`) · 같은 명세를 기존 검사에 넣으면 `read.coverage` 56 실패 · `read.pointer-resolve` 112 · `read.claim-inventory` 24 실패.

지적 열거 = NL-1

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 13**. **수용 → 지표 v15(계수 전 명세에 엔진 READ 검사(`reader.lib.run_read_checks`)를 재실행 → 전건 pass 필수 · 검사별 checked 계수가 완주 판정서의 기록과 일치해야 함 · 불일치·실패 = exit 4 — 명세 ↔ 판정서 결속을 재실행으로 닫는다) → M1b 15차 도전(지적 `NM-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 48건은 closed 47건 · partially 1건(MZ-2) · open 0건입니다.** NK-1의 필수 필드 제거 반례는 모두 닫혔습니다. 그러나 **스키마를 통과하는 집합 단위 결측을 정상 0건·빈 분포로 보고하는 통로**가 남았습니다. 신규 지적은 **NL-1 · MED**입니다.

사본 path·pin·order·disposable과 HEAD `f4d1744c62acc083f85a6d38945782a64fb4d956`이 일치했습니다. 메모 SHA-256은 `ccc6a8ea8f558ffbb077c91c1d995e3004d6c6958f1970c3d0ecdccfae239a6a`입니다.

**A — 이전 지적 폐쇄 판정**

범위 표기는 해당 ID 각각에 적용합니다.

| 이전 지적 | v14 판정 | 근거 |
|---|---|---|
| MY-1~2 | closed | 고정 핀·절차 동일성 확인, 잡음 방향 미확정으로 한정 |
| MY-3~4 | closed | 기준 27단위·Owner 명시 판정, 종속 청구항 10개 표본 |
| MY-5~7 | closed | 수확 제외·6축·스냅샷·검사 배열과 findings 보존 |
| MY-8~9 | closed | 종료 분류와 실제 read-a→read-b 요청 순서 확인 |
| MY-10~13 | closed | 완료 구별·증거 보존·전 런 보존·원장 누적 설명 |
| MZ-1 | closed | 5→1 병합 후보를 다섯 단위 모두에서 재사용 |
| **MZ-2** | **partially** | 수렴 미실행 제외는 닫힘. **필수 지표 결측 처리에 NL-1 잔존** |
| MZ-3~6 | closed | 스냅샷 결속·baseline 제한·예외 분류·최신 부적격 N/A·검사 귀속 |
| MZ-7~9 | closed | 부모 기준 증명·발주 상한·Map와 정규 경로 거부 |
| NA-1~3 | closed | 로그 없는 최신 시도 N/A·예외 경계·조회/발주 분리 |
| NA-4~7 | closed | 필수 형태 검증·다중 기록 설명·경로 결속·발췌 판정 불가 처분 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 검사·판정서 검증 경계 |
| NC-1~3 | closed | 실제 enter 오류→14·스냅샷 단일 읽기·수치 범위 |
| ND-1~2 | closed | findings 계약 검증·계수할 응답 바이트의 SHA 대조 |
| NE-1~2 | closed | 완주 공통 검증·finding 전체 형태 검증 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조·실행본 버전 표기 |
| NH-1~2 | closed | 요청·응답·디렉터리 결속·baseline 우회 차단 |
| NI-1~2 | closed | MD 지문 재계산·dispatch 대조·원천 지문 사슬 |
| NJ-1 | closed | 원천 부재·읽기 실패·바이트 변경 거부 |
| **NK-1** | **closed** | 지정 네 필드 제거 모두 계약 스키마 위반으로 exit 4 |

§8의 격은 유지됩니다. **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕⓖⓝ는 명시한 범위의 재정 문언 이행**입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표기는 구현·운영 재량입니다. 다만 **ⓕ의 결측 처리는 NL-1 때문에 구현상 미완**입니다.

**NL-1 · MED — 필수 필드는 검사하지만, 집계 대상 전체의 결측을 정상 관측값으로 수용한다.**

좌표: 메모 **§5 결측 규칙·㉡·㉢·㉥·§9 D/G**, [t40_metrics.py:248](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:248)의 명세 스키마 검증과 이어지는 계수, [267행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:267)의 component 기본값.

정상 기준 런의 **명세 읽기만 메모리로 대체**하고 실제 CLI 본문을 실행했습니다. 원천·조기/완주 판정서·요청·응답·로그는 그대로 유지했습니다.

| 명세에 가한 변경 | 전체 스키마 오류 | v14 CLI 출력 |
|---|---:|---|
| `items`에서 grounding 전량 제거 | 0 | exit 0 · 전체/종속 anchor 분포 `{}` |
| `items`에서 component 전량 제거 | 0 | exit 0 · `component_count=0` |
| `claims.dependents=[]` | 0 | exit 0 · 종속항 0 · 종속 anchor 분포 `{}` |

**세 사례 모두 `synth_eligible=true`, `na=[]`였습니다.**

이어 **R0 식별자·partial/read·정상 dispatch·스냅샷과 sidecar를 갖춘 메모리 worktree 배치**에서도 같은 결과를 재현했습니다. `--baseline` 예외 때문에 생기는 현상이 아닙니다.

같은 명세를 기존 등록 검사에 직접 공급하면 다음처럼 실패합니다.

| 변경 | 기존 검사 재실행 |
|---|---|
| grounding 전량 제거 | `read.coverage`: **56건 실패** |
| component 전량 제거 | `read.pointer-resolve`: **112건 실패** |
| 종속항 목록 비움 | `read.claim-inventory`: **24건 실패** |

첫 coverage 소견은 다음과 같습니다.

> `M1 를 접지하는 grounding 0건` — 기대: `grounding 1건 이상`

전체 스키마 검증은 실제로 작동합니다. 그러나 스키마는 **필드 존재·형태**를 검사할 뿐, grounding의 피복·참조 해소·원천 청구항의 전량 등재까지 보증하지 않습니다. 추출기는 현재 명세와 함께 읽은 정상 판정서 사이의 이 불일치를 발견하지 못합니다.

이는 정상 러너가 이런 명세를 생성한다는 주장이 아닙니다. **수집된 명세의 집합 단위 결측이 정상 판정서와 섞여도 임계용 관측값으로 출력되는 반례**입니다.

**고치는 문안:** “계수할 명세에 기존 coverage·pointer-resolve·claim-inventory 검사를 재실행하여 피복·참조·원천 등재를 확인하고, 기록 판정과 불일치하거나 집계 대상이 결측이면 exit 4로 거부하며 정상 0건으로 출력하지 않는다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합. 결측 처리 이행에 NL-1 잔존 |
| **B 계측 커밋 셋** | **PASS** | 부모·tree·전체 팔 diff·프로필·numstat 일치 |
| **C 구동 v6** | **PASS** | 종료 분류·실제 진입 오류·증거 실패·스냅샷·조회·발주 상한 확인 |
| **D 지표 v14** | **REVISE** | NK-1과 지정 회귀는 차단. 집합 단위 결측은 정상 수용 |
| **E 발췌 v4** | **PASS** | 병합 후보 재사용·자동 열위 없음·표본·판정 불가 처분 정합 |
| **F Workflow v4** | **PASS** | Node 대체 실행에서 사전 거부와 wrote/null 구별 확인 |
| **G 결정 공백** | **REVISE** | 결측을 정상 값으로 공급하는 처분 공백. 기존 검사 적용으로 수정 가능 |

C·E·F의 PASS는 아래 정적·메모리 검증 범위입니다. 실제 모델 호출의 검증을 뜻하지 않습니다.

**B의 직접 대조 결과**

base 부모는 `6d92cad`, R1·R2 부모는 모두 `ad4c6c3`입니다. 기준과 base의 절차 tree는 동일한 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.

`6d92cad → base`는 절차 6파일만 변경하고, 두 팔은 각각 **`2 2 contracts/stages/read.yaml`**만 변경합니다. 실제 `lane_profiles()`도 R1의 decompose·synthesize만 xhigh, R2의 ground-dependent만 sonnet-5/high로 산출했습니다.

§0′의 `d4e6ca2 → 6d92cad` 추가/삭제 열거는 **16파일 전부 일치**했습니다. read.yaml **321/31**, convergence 스키마 **42/7**, read.py **713/126**, `reader/lib/__init__.py` **4/0**, plan/file_adapter/replay_adapter **2/7·6/4·2/2**를 포함합니다.

base 절차 blob으로 현행 요청서를 재렌더한 결과는 **6/6 바이트 동일·입력 지문 6/6 동일**입니다. 동일 입력의 최초 요청에 대한 확인이며, 검사·재시도·`defects`까지 동일하다는 보증은 아닙니다.

**D의 수정·회귀 확인**

| 검증 | 결과 |
|---|---|
| 정상 기준 런 `--baseline` | exit 0 · `na=[]` · 통합 적격 |
| NK-1: claims/dependents/additions/anchor_state 제거 | **4건 모두 exit 4**, 계약 스키마 위반 메시지 |
| 조기·완주·명세의 최상위 필수 필드 각각 제거 | **18/18·18/18·11/11건 exit 4** |
| worktree 배치의 스키마 탐색 | 해당 worktree의 `contracts/schemas`와 `reader/schemas` 선택 |
| 스냅샷 부재·SHA·식별자·국면·수치·형태, 원천·요청·dispatch 결속 등 | **48사례 모두 기대 결과** |
| 최신 synthesize mismatch / 로그 없는 최신 좌표 | `synth_counts=null` · 부적격 · N/A |
| 통합 응답의 계수 시점 바이트 교체 | 변경 바이트의 SHA 불일치로 부적격·N/A |
| 타 소재 donor 명세의 run_id만 변경 | 원천 지문 불일치로 exit 4 |

기준 계수는 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다.

**검증 경로**

모든 명령은 지정 사본에서 실행했습니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 하네스는 `PY - <<'PY' … PY`로 실행했고 파일로 저장하지 않았습니다.

| 명령·실물 호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `f4d1744c62acc083f85a6d38945782a64fb4d956` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `ccc6a8ea8f558ffb…e239a6a` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **빈 출력** |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · exit 0 |
| `runpy.run_path(..., run_name='__main__')` + 명세 단일 읽기 대체 | `REAL_BASELINE_WHOLE_COLLECTION_REMOVED grounding exit 0` |
| 같은 CLI + R0 메모리 worktree·dispatch·스냅샷 | `MEASURE_COLLECTION_REMOVED grounding exit 0` |
| 위 명세→`CHECK_REGISTRY['read.coverage']` | `read.coverage fail violations 56` |
| 지표 회귀 하네스 | `REGRESSION 48 expected 48 unexpected []` |
| `classify`·`classify_after_exception` 메모리 대입 | `CLASSIFY_CASES 10 10` |
| 실제 `enter`→`cmd_read` | `ACTUAL_ENTER_MISSING_WORKTREE 14 ACTUAL_ENTER_BAD_RUN 14` |
| 증거 실패·종결 포인터 동시 대입 | `EVIDENCE_FAILURE_TERMINATED 14` |
| 발주 쓰기를 메모리로 대체 | `DISPATCH4 15 UNCHANGED True` |
| 스냅샷 복사·쓰기를 메모리로 대체 | `SNAP_NOCONV True PRESERVED True SIDECAR_MATCH True` |
| 실제 `read.run`, 진입·종결·쓰기만 대체 | 응답 공급 뒤 pending: `read-b/decompose/batch-0` |
| 실제 `_dispatch` mismatch 응답 대입 | `REAL_DISPATCH_MISMATCH 1 False False True` |
| `candidates`·`comp_texts_fn` 직접 호출 | `MERGE_5_TO_1 [['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| `sample_indices`·원문 단락 조회 | `LOCATORS 27 RESOLVED 27` |
| `node --input-type=module -` + 실제 Workflow 본문 | `toString`·`constructor`·`/./`: 모두 calls 0 |
| 봉투 stdout 미리보기→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `git status --porcelain --untracked-files=no` | **빈 출력** |

v6에는 **`_next_dispatch`가 없습니다.** 현재 구현인 `cmd_dispatch`를 시험했습니다. 세 번 발주 후 네 번째는 15·무기록, 기존 배치 충돌은 14·무기록, `lanes` 조회는 무변경이었습니다.

종속항 표본은 **CL-2·4·7·9·12·14·16·19·21·24**입니다. 발췌 생성 CLI는 실행하지 않았습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다. 사본 원천은 **298,507 B**, SHA-256 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`로 확인했습니다.
- 실제 Workflow 모델 호출·transcript/journal 형식·effort 증거·문맥 격리는 시험하지 않았습니다.
- 실측 worktree 생성·source 봉인·봉투 쓰기와 재개·생산 원장 append는 수행하지 않았습니다.
- 시간·토큰·가용 메모리 추정과 역사적 CLI의 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 원장·이력: T40, `D-20260905-02-pdm2b-seats.md` §17 및 추기, 1·2차 도전 원문과 3~13차 관련 지적·처분, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v14, v13→v14 diff, bundle 스크립트 5종.
- 구현: read·source 러너, lane plan·contract·file_adapter, paths, convergence·run_checks·report의 지정 함수와 호출 경로.
- 실물: 기준 run.yaml·원천·판정서·명세·로그·요청/응답, donor 명세, 지정 커밋의 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.