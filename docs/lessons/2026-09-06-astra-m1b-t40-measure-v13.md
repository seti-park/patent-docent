# 독립 감수 원문 — M1b 설계 도전 13차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v13 · 판정 REVISE(MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `b59107af13b6e21d8204847ae3d5997d3945928b6fed69de74261bae407c67a9` · 13956 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v13/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 08:20:01 → 08:32 · **USAGE = input 3,101,708(cached 2,920,832) · output 20,156(reasoning 3,301)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `5109ef3` · v13 sha256 `5abeefdf…` · v1~v12 동봉 · 지표 v13). 폐쇄 = **이전 47건 closed 46 · partially 1(MZ-2 → NK-1) · open 0**(NJ-1 닫힘). **B·C·E·F PASS**(8회 연속).

**판정 = REVISE · 1건(MED) · 기각 0 · 발주자 귀책.** **NK-1 MED**: 명세 검증이 run_id·원천 지문·items 배열까지만 — `claims`·`dependents`·`additions`·`anchor_state` 결측을 `.get(…, {})` 기본값이 정상 0건·빈 분포로 바꿈(실물 기준 런에서 `claims` 만 제거 → exit 0 · 종속항 0 · na=[]).

지적 열거 = NK-1

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 12**. **수용 → 지표 v14(명세를 `reader/schemas/material-spec.schema.json` 전체로 jsonschema 검증 · 조기·완주 판정서도 `convergence.schema.json` 전체로 검증 · 위반 exit 4 — 필드 결측 계열을 개별 검사가 아니라 계약 스키마 전체 대조로 닫는다) → M1b 14차 도전(지적 `NL-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 47건은 closed 46건 · partially 1건(MZ-2) · open 0건입니다.** NJ-1의 원천 파일 부재·비파일·읽기 실패는 모두 닫혔습니다. 그러나 **명세의 필수 필드가 없어도 정상적인 0건·빈 분포로 출력하는 결측 통로**가 남았습니다. 신규 지적은 **NK-1 · MED**입니다.

사본 마커 path·pin·order·disposable과 HEAD `5109ef39df5716a76535121479815749dc44ddf8`이 일치했습니다. 메모 SHA-256도 지정값 `5abeefdf3fcbb9bbde474cf51b59fbbcf2b638bea9bef6d8d8febdd8675ee5c5`와 일치합니다.

**A — 이전 지적 폐쇄표**

범위로 묶은 판정은 해당 ID 각각에 적용합니다.

| 이전 지적 | v13 판정 | 근거 |
|---|---|---|
| MY-1~2 | closed | 절차 tree·고정 핀 동일, 잡음 방향 미확정으로 한정 |
| MY-3~4 | closed | 기준 27단위·Owner 명시 판정, 종속 청구항 10개 표본 |
| MY-5~7 | closed | 수확 제외, 조기 6축·스냅샷, 검사 배열·findings 보존 |
| MY-8~9 | closed | 종료 분류 및 실제 read-a→read-b 요청 순서 |
| MY-10~13 | closed | 완료 구별·이동 보존·전 런 증거·원장 누적 설명 |
| MZ-1 | closed | 5→1 병합에서 같은 후보를 다섯 단위에 재사용 |
| **MZ-2** | **partially** | 수렴 미실행 제외는 닫힘. **필수 지표 결측을 N/A로 처리한다는 요구는 NK-1로 잔존** |
| MZ-3~6 | closed | 스냅샷 결속·baseline 제한, 예외 분류, 최신 부적격 N/A, 검사 귀속 추정 |
| MZ-7~9 | closed | 부모 기준 증명, 발주 상한, Map·정규 경로 거부 |
| NA-1~3 | closed | 로그 없는 최신 시도 N/A, 예외 경계, 조회·발주 분리 |
| NA-4~7 | closed | 판정서 필수 형태, 다중 기록 설명, 경로 결속, 발췌 판정 불가 처분 |
| NB-1~3 | closed | 증거 실패→14, 발주 전건 검사, 판정서 검증 경계 |
| NC-1~3 | closed | 실제 enter 오류→14, 스냅샷 동일 바이트 처리, 수치 범위 |
| ND-1~2 | closed | findings 필수·계약 검증, 계수할 응답 바이트의 SHA 대조 |
| NE-1~2 | closed | 완주 공통 검증, finding 계약 검증 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조, 실행본 버전 표기 |
| NH-1~2 | closed | 요청·응답·디렉터리 결속, baseline 우회 차단 |
| NI-1~2 | closed | 요청 MD 재계산·dispatch 대조, 원천 지문 사슬 |
| NJ-1 | closed | patent.md 부재·비파일·읽기 실패→4, 실제 바이트 지문 출력 |

MZ-2의 판정은 **조기 수렴 반례의 회귀 때문이 아닙니다.** 원문이 요구한 “필수 지표 부재는 N/A”의 이행 범위를 명세 계수까지 대조한 결과입니다.

T40 §1·§4·§5의 팔 구성, `partial/read`, 봉투 대행 범위, exact-match·청구항 실패의 봉투 배제는 정합합니다. §8의 격도 다음과 같이 유지됩니다.

- **ⓐⓑⓒⓓⓗⓙⓛⓜ:** 운영 재량.
- **ⓔ:** T40 §5 승인. 지정 3런과 exit 11 확인을 결합해야 함.
- **ⓕⓖⓝ:** 명시한 범위의 재정 문언 이행. 다만 ⓕ의 결측 처리 구현은 NK-1.
- **ⓘ:** 표본 단위는 재정 이행, 인덱스는 구현 재량.
- **ⓚ:** 27단위·Owner 판정은 재정 이행, 후보 제시·런 표기는 재량.

**지적 목록**

**NK-1 · MED — 명세의 필수 필드 결측을 정상적인 0건·분포 값으로 바꾼다.**

좌표: [메모 §5 결측 규칙·㉢·㉥](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md:89), [t40_metrics.py:metrics 명세 계수](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:240), [material-spec 스키마](/home/laptop/projects/workspaces/pd-m1b-t40/reader/schemas/material-spec.schema.json:436).

명세 검증은 run_id·원천 지문·`items` 객체 배열까지만 확인합니다. 이후에는 다음 기본값이 결측을 숨깁니다.

```python
m.get("claims", {}).get("dependents", [])
cl.get("additions", [])
i.get("anchor_state") or {}
```

정상 요청·응답·로그·dispatch·판정서·원천을 가진 메모리 R0에서 **명세 필드만 제거**하고 실제 CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행했습니다.

| 제거한 필드 | v13 결과 |
|---|---|
| `claims` | exit 0 · 종속항 0 · additions 0 · 종속 분포 `{}` |
| `claims.dependents` | exit 0 · 종속항 0 · additions 0 · 종속 분포 `{}` |
| 종속항 각각의 `additions` | exit 0 · 종속항 24 · additions 0 · 종속 분포 `{}` |
| grounding 각각의 `anchor_state` | exit 0 · 전체 분포 `spec=None\|figure=None: 56` · 종속분 50 |

**네 사례 모두 `synth_eligible=true`, `na=[]`였습니다.** 같은 자료를 실제 명세 스키마로 검사하면 각각 필수 필드 위반입니다.

합성 런 구성에 의존하는 현상도 아닙니다. **실물 기준 런에서 명세를 읽는 한 번만 가로채 `claims`를 제거**하고 나머지 파일은 그대로 읽은 CLI 실행의 마지막 출력은 다음과 같습니다.

```text
REAL_BASELINE_CLI_ONE_FIELD_REMOVED exit 0 intercepted 1 dependent_claims 0 dependent_dist {} na []
```

원천 지문이 맞는다는 사실은 명세의 종속항 목록·접지 상태가 존재한다는 증거가 아닙니다. 현재 결과는 결측을 정상 관측값으로 내보내므로, §5의 판정 불가·재상신 경로가 작동하지 않습니다.

**고치는 문안:** “명세 계수 전에 claims·dependents·additions와 계수 대상 항목의 kind·component·anchor_state 등 필수 필드 및 형태를 계약과 대조하고, 결측·손상은 exit 4로 거부하며 정상적인 빈 집합과 구별한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합. 필수 지표 결측 처리의 이행은 NK-1 |
| **B 계측 커밋 셋** | **PASS** | 부모·tree·blob·전체 팔 diff·프로필·numstat 일치 |
| **C 구동 v6** | **PASS** | 종료 분류·진입 오류·증거 실패·스냅샷·조회·발주 상한 확인 |
| **D 지표 v13** | **REVISE** | NJ-1 및 지정 회귀 사례는 차단. 명세 결측은 정상 수용 |
| **E 발췌 v4** | **PASS** | 병합 후보 재사용, 자동 열위 없음, 표본·판정 불가 처분 정합 |
| **F Workflow v4** | **PASS** | Node 대체 실행에서 지정 사전 거부·wrote/null 구별 확인 |
| **G 결정 공백** | **REVISE** | 결측을 정상 분포로 공급하는 잔여. 기존 계약의 구현 수정으로 닫을 수 있음 |

C·E·F의 검증 범위는 아래 대체 실행까지입니다. 실제 Workflow 호출을 검증했다는 뜻은 아닙니다.

**B — 커밋·동일성 직접 검증**

base 부모는 `6d92cad`, R1·R2 부모는 모두 `ad4c6c3`입니다. 기준과 base의 절차 tree는 동일한 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.

`6d92cad → base`는 절차 6파일만 변경합니다. 두 팔은 각각 **`2 2 contracts/stages/read.yaml`**만 변경하며, `lane_profiles()`도 R1의 decompose·synthesize만 xhigh, R2의 ground-dependent만 sonnet-5/high로 산출했습니다.

§0′의 `d4e6ca2 → 6d92cad` 열거를 재실측한 결과도 일치합니다.

| 파일 | 추가/삭제 |
|---|---:|
| `contracts/stages/read.yaml` | 321/31 |
| `contracts/schemas/convergence.schema.json` | 42/7 |
| `contracts/run-kinds.yaml` | 24/2 |
| `engine/stages/read.py` · `source.py` | 713/126 · 46/1 |
| `engine/lanes/contract.py` | 67/1 |
| `engine/lanes/plan.py` · `file_adapter.py` · `replay_adapter.py` | 2/7 · 6/4 · 2/2 |
| `engine/paths.py` · `stages/__init__.py` | 19/0 · 69/0 |
| `engine/render/material_spec_md.py` | 85/1 |
| `reader/lib/run_checks.py` · `convergence.py` · `dependency_parse.py` | 90/35 · 32/5 · 30/1 |
| `reader/lib/__init__.py` | 4/0 |

reader-rules·material-spec 스키마 diff는 없었습니다. 계측 base의 절차 blob을 공급한 현행 요청서 재렌더는 **6/6 바이트 동일**, 입력 지문 재계산도 **6/6 동일**했습니다. 이 결과는 **같은 입력의 최초 요청서**에 대한 확인이며, 변경된 검사·재시도·defects까지 동일하다는 보증은 아닙니다.

**D — v13 회귀 확인**

| 사례 | 결과 |
|---|---|
| 정상 기준 런 `--baseline` | exit 0 · `na=[]` · synth 적격 |
| 정상 메모리 R0 실측 모드 | exit 0 · `na=[]` · synth 적격 |
| patent.md 부재 / 비파일 / 읽기 실패 / 바이트 변경 | 모두 exit 4 |
| first-early 옵션 부재 / 파일 부재 / sidecar 불일치·빈 값 | 모두 exit 4 |
| 조기·완주 run_id·phase 불일치 | 모두 exit 4 |
| 축 중복·bool 실행값·bool/음수 계수·bool/NaN/범위 밖 Jaccard | 시험 사례 모두 exit 4 |
| checks 손상·findings 부재·finding 필수 키 부재 | 모두 exit 4 |
| 완주 `executed=false, axes=[]` | 수용 |
| 명세 run_id·원천 지문 불일치 | exit 4 |
| dispatch 부재·지문 불일치, request_digest 부재 | exit 4 |
| `REAL_DONOR_WHOLE_LANE_BUNDLE` | exit 4 — MD 입력 지문 재계산 불일치 |
| `REAL_DONOR_SPEC_RELABELLED_ONLY` | exit 4 — 명세 원천 지문 불일치 |
| 최신 synthesize 로그 없음 / mismatch | `synth_counts=null` · 부적격 · N/A |
| 응답 SHA 불일치 | exit 4 |

donor는 실물 `openai-us20260147854a1-cim-fp-3` 자료를 사용했습니다. 전체 레인 묶음 사례에는 누락된 역사적 `request_digest`를 donor MD의 실제 SHA로 채워 재계산 검사까지 도달시켰으며, 부재 사례는 별도로 시험했습니다.

기준 계수는 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·synthesize fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다. 실제 원천은 **298,507 B**, SHA-256은 `64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`였습니다.

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY - <<'PY' … PY`로 실행했습니다.

| 명령·실물 호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `5109ef39df5716a76535121479815749dc44ddf8` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `5abeefdf3fcbb9bb…675ee5c5` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **빈 출력** |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · exit 0 |
| `runpy.run_path` CLI + 명세 단일 읽기 대체 | `REAL_BASELINE_CLI_ONE_FIELD_REMOVED exit 0 intercepted 1 dependent_claims 0 dependent_dist {} na []` |
| `classify`·`classify_after_exception`에 반환·gate·pointer 대입 | 모순·판독 불능→14, 조기 상신→11, 봉투 불가→12 |
| 실제 `enter` 오류를 `cmd_read`로 호출 | `EXIT_CODE=14` |
| 증거 기록 실패와 종결 포인터를 함께 대입 | `EXIT_CODE=14` |
| `snapshot_first_early` 복사·쓰기를 메모리로 대체 | `SNAP_PRESERVED True SIDECAR_MATCH True` |
| `cmd_dispatch`의 counter·args를 메모리로 대체 | `DISPATCH4 15 unchanged True` |
| `cmd_lanes` 조회 | `LANES_READ_ONLY True` |
| 실제 `read.run`, 진입 검사·출력만 대체 | 첫 pending read-a, 공급 뒤 pending read-b |
| `candidates`·`comp_texts_fn`·`sample_indices` 직접 호출 | `MERGE_5_TO_1 [['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| 기준 표본·원문 단락 조회 | CL-2·4·7·9·12·14·16·19·21·24 · `LOCATORS 27 resolved 27` |
| `node --input-type=module -`, 실제 Workflow 본문의 agent/pipeline 대체 | `toString`·`constructor`·`/./` 모두 calls 0; `WORKFLOW_V4_REGRESSION_DONE` |
| 봉투 stdout 미리보기→`continue_envelope_state` 메모리 공급 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `git status --porcelain --untracked-files=no` | **빈 출력** |

v6에는 **`_next_dispatch`가 없습니다.** 현재 발주 구현인 `cmd_dispatch`를 시험했습니다. 배치 파일 충돌은 **14·무기록**, 총 세 번 발주 뒤 네 번째는 **15·회차 불변**이었습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다. 정본화 원천은 사본의 실제 바이트로 검증했습니다.
- 실제 Workflow 모델 호출·transcript/journal 형식·effort 증거·문맥 격리는 시험하지 않았습니다. Node 시험은 본문 분기와 옵션 확인입니다.
- 실측 worktree 생성, source 봉인, 봉투 쓰기·재개, 생산 원장 append는 하지 않았습니다. 러너 시험의 진입 검사·쓰기 함수 대체 범위를 실제 재개 성공으로 주장하지 않습니다.
- 시간·토큰·가용 메모리 추정과 역사적 CLI의 실호출 effort는 검증하지 않았습니다.

**읽은 파일**

- 원장·이력: T40 전문, `D-20260905-02-pdm2b-seats.md` §17 및 추기, 1·2차 도전 원문과 3~12차 관련 지적·처분, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v13, v12→v13 대조, bundle 스크립트 5종.
- 구현: read·source 러너, lane plan·contract·file_adapter, paths, convergence·run_checks·report의 지정 함수와 호출 경로.
- 실물: 기준 run.yaml·원천·판정서·명세·레인 로그·요청/응답 6건, donor 명세·통합 요청/응답·로그, 지정 커밋의 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 실행 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.