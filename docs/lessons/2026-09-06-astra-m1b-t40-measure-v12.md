# 독립 감수 원문 — M1b 설계 도전 12차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v12 · 판정 REVISE(MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `8dc3f4ed7b2547913480a00cd58201d904aba5b3af6a51bab4c930a5f9420fde` · 13404 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v12/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 08:04:47 → 08:17 · **USAGE = input 2,512,864(cached 2,358,400) · output 19,913(reasoning 4,230)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `bede71c` · `bundle/T40-MEASURE-DESIGN.md` v12 sha256 `19983ea8…` · v1~v11 동봉 · 지표 v12). 폐쇄 = **이전 46건 closed 45 · partially 1(NI-2 → NJ-1) · open 0**(11차 donor 반례 전건 차단). **B·C·E·F PASS**(7회 연속).

**판정 = REVISE · 1건(MED) · 기각 0 · 발주자 귀책.** **NJ-1 MED**: 원천 바이트 검사가 `if os.path.isfile(pm)` 안 → `00-source/patent.md` **부재**면 검사 생략 후 `source_digest = EXPECTED_SOURCE` 를 무조건 출력(변경·읽기 실패는 exit 4 인데 부재만 통과).

지적 열거 = NJ-1

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 11**. **수용 → 지표 v13(patent.md 부재·비파일·읽기 실패 = exit 4 · 실제 바이트 sha 일치 시에만 source_digest 출력) → M1b 13차 도전(지적 `NK-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 46건은 closed 45건 · partially 1건(NI-2) · open 0건입니다.** 11차 donor 반례는 차단됐습니다. 그러나 **원천 파일이 없어도 정상 지표와 원천 지문을 출력하는 경로**가 남았습니다. 착수 판정은 REVISE입니다.

사본 마커의 path·pin·order·disposable 및 HEAD `bede71c9272068c566419cc4af6c38fb838cb504`가 일치했습니다. 메모 SHA-256은 `19983ea8781c55678b64051c5f8053f74a3dbca1b0a756769bc8c1fe03e0aaa2`입니다.

**A — 원장 정합·이전 지적 폐쇄표**

범위로 묶은 행의 판정은 해당 ID 각각에 적용됩니다.

| 이전 지적 | v12 판정 | 확인 근거 |
|---|---|---|
| MY-1~2 | closed | 절차 tree·고정 핀 일치, 잡음 방향 미확정으로 한정 |
| MY-3~4 | closed | 기준 27단위·Owner 명시 판정, 종속 청구항 10개 표본 |
| MY-5~7 | closed | 수확 제외, 조기 6축·스냅샷, 검사 배열·findings 보존 |
| MY-8~9 | closed | 종료 분류 및 실제 read-a→read-b 요청 순서 |
| MY-10~13 | closed | 완료 구별·이동 보존·전 런 증거·원장 누적 설명 |
| MZ-1~3 | closed | 5→1 병합 후보 재사용, 미실행 제외, 스냅샷 필수·baseline 제한 |
| MZ-4~6 | closed | 예외 분류, 최신 부적격 N/A, 검사 귀속 추정·상신 목록 |
| MZ-7~9 | closed | 부모 기준 numstat, 발주 상한, Map·정규 경로 거부 |
| NA-1~3 | closed | 로그 없는 최신 시도 N/A, 예외 경계, 조회·발주 분리 |
| NA-4~7 | closed | 필수 형태 검증, 다중 기록 설명, 경로 결속, 판정 불가 처분 |
| NB-1~3 | closed | 증거 실패→14, 발주 전건 검사, 판정서 검증 경계 |
| NC-1~3 | closed | 실제 enter 오류→14, 스냅샷 단일 읽기, 수치 범위 검증 |
| ND-1~2 | closed | findings 필수·계약 검증, 계수할 응답 바이트의 SHA 대조 |
| NE-1~2 | closed | 완주 공통 검증, finding 계약 검증 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조, 실행본 버전 표기 |
| NH-1~2 | closed | 요청·응답·디렉터리 결속, baseline 우회 차단 |
| NI-1 | closed | MD 입력 지문 재계산, request_digest 필수, 실제 dispatch 자료 대조 |
| **NI-2** | **partially** | 지문 5점 변경·donor 명세는 거부하지만 원천 파일 부재는 수용 — NJ-1 |

T40 §1·§4·§5의 팔 구성, `partial/read`, 지정 3런의 봉투 대행 및 exact-match·청구항 실패의 봉투 배제는 정합합니다. G-12를 집행 완료로 주장하지도 않습니다.

§8의 격은 **ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량**, **ⓔ는 T40 §5 승인**, **ⓕⓖⓝ는 명시한 범위의 재정 문언 이행**입니다. **ⓘ는 표본 단위 이행·인덱스 구현 재량**, **ⓚ는 27단위·Owner 판정 이행·후보 표시 재량**입니다.

**지적 목록**

**NJ-1 · MED — 필수 원천 파일이 없어도 원천 결속을 통과한 정상 결과처럼 출력한다.**

좌표: [메모 §2·§5·§9 D/G](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md), [t40_metrics.py:164](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:164)의 `metrics()` 원천 검사 및 168행 `source_digest`.

원천 바이트 검사는 `if os.path.isfile(pm)` 안에 있습니다. 파일이 없으면 검사를 생략하고 다음을 무조건 출력합니다.

```python
out["source_digest"] = EXPECTED_SOURCE
```

실측 R0 이름으로 결속한 메모리 런에서 정상 요청·응답·로그·dispatch·조기 스냅샷·완주 판정서·명세를 유지하고, **`00-source/patent.md`만 제거**했습니다. 실제 CLI 본문을 실행한 결과입니다.

```text
MISSING_PATENT_MD exit 0
synth {'fact': 3, 'implication': 20, 'positioning': 7, 'figure_note': 10}
eligible True component 56 na []
source_digest sha256:64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e
```

같은 파일의 바이트 변경과 읽기 실패는 exit 4입니다. **부재일 때만 원천 바이트 대조가 해제됩니다.** 따라서 메모가 선언한 `sha256(patent.md)`까지의 결속 사슬을 완성하지 않고도 결과 표에 정상 지표를 공급합니다.

**고치는 문안:** “`00-source/patent.md`의 부재·비파일·읽기 실패는 exit 4로 거부하고, 실제 읽은 바이트의 SHA가 나머지 원천 지문 및 선등록 값과 일치한 경우에만 검증한 `source_digest`를 출력한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합하나 NI-2의 원천 결속 이행이 미완 |
| **B 계측 커밋 셋** | **PASS** | 부모·tree·blob·전체 팔 diff·프로필·numstat 일치 |
| **C 구동 v6** | **PASS — 확인 범위** | 종료 분류·진입 오류·증거 실패·스냅샷·조회·발주·상한 확인 |
| **D 지표 v12** | **REVISE** | 지정 donor·지문 변경 반례는 차단. 원천 부재는 NJ-1 |
| **E 발췌 v4** | **PASS — 확인 범위** | 병합 후보 재사용, 자동 열위 없음, 표본·판정 불가 처분 정합 |
| **F Workflow v4** | **PASS — 정적·대체 실행 범위** | 지정 라벨·경로 반례 사전 거부, wrote/null 구별 |
| **G 결정 공백** | **REVISE** | 필수 원천 부재를 정상 성공으로 처리하는 잔여. NJ-1은 구현 수정으로 닫을 수 있음 |

**D — 지정 반례 및 회귀 결과**

모두 실제 `t40_metrics.py` CLI 본문을 `runpy.run_path(..., run_name="__main__")`로 실행했습니다. 파일 접근만 메모리로 대체했습니다.

| 사례 | v12 결과 |
|---|---|
| 정상 실측 모드 대조군 | exit 0 · eligible true · `na=[]` |
| `REAL_DONOR_WHOLE_LANE_BUNDLE` | **exit 4** — MD 재계산 입력 지문 불일치 |
| 위 사례의 `request_digest` 삭제 | **exit 4** — request_digest 부재 |
| donor 묶음에 일치 dispatch까지 공급 | **exit 4** — MD 재계산 불일치 |
| 정상 대상 요청 + donor 응답·로그 | **exit 4** — 요청 JSON과 로그 입력 지문 불일치 |
| `REAL_DONOR_SPEC_RELABELLED_ONLY` | **exit 4** — 명세 원천 지문 불일치 |
| 원천 지문 5점 각각 단독 변경 | **5/5 exit 4** |
| dispatch 기록 부재 / 입력 지문 불일치 | 각각 **exit 4** |
| `--first-early` 부재 / sidecar 불일치 | 각각 **exit 4** |
| 실측 런의 `--baseline` / 두 옵션 병용 | **exit 4 / exit 3** |
| 디렉터리 이름과 run_id 불일치 | **exit 4** |
| 조기·완주 run_id, 축·계수·수치·findings 손상 | 시험한 사례 모두 **exit 4** |
| 완주 `executed=false, axes=[]` | 정상 수용 |
| 최신 synthesize 로그 부재 / mismatch | **synth_counts=null · eligible false · N/A** |
| 응답 SHA 불일치 | **exit 4** |
| **원천 파일 부재** | **exit 0 · eligible true · `na=[]` — NJ-1** |

donor는 실물 `openai-us20260147854a1-cim-fp-3`의 `read-a/synthesize/retry-1/batch-0`입니다. 이 역사적 로그에는 `request_digest`가 없어, 전체 묶음 시험에서는 donor MD의 실제 SHA를 채워 **형태 검사를 넘어 재계산 검사까지 시험**했고, 삭제 사례는 별도로 실행했습니다.

`recompute_input_digest`는 계약 `compute_input_digest(digest_source(md))`와 같은 뜻입니다. 기준 요청서 **6/6**에서 두 재계산 값과 request.json이 일치했고, 계측 base 절차를 공급한 현행 재렌더도 **6/6 바이트 동일**했습니다.

정상 발주 흐름도 확인했습니다. 실제 `pending_coords`·`cmd_dispatch`가 만든 A-a 1건→A-b 1건→B 3건→C 1건의 기록을 추출기에 공급하면 **exit 0·eligible true**입니다. 실제 `read.run`은 첫 호출에 read-a, 응답 공급 뒤 두 번째 호출에 read-b를 요청했습니다. dispatch 기록 필수화와 A-a 흐름의 충돌은 확인되지 않았습니다.

**B — 직접 재실측**

- base 부모는 `6d92cad`, R1·R2 부모는 모두 `ad4c6c3`입니다.
- 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.
- `6d92cad → base`는 절차 6파일뿐입니다. 두 팔은 각각 `2/2 contracts/stages/read.yaml`만 변경합니다.
- R1은 decompose·synthesize의 effort만 xhigh, R2는 ground-dependent만 sonnet-5/high입니다. `lane_profiles`와 Sonnet aliases도 직접 확인했습니다.

`d4e6ca2 → 6d92cad`의 메모 열거는 재실측과 일치합니다.

| 파일 | 추가/삭제 |
|---|---:|
| contracts/stages/read.yaml | 321/31 |
| contracts/schemas/convergence.schema.json | 42/7 |
| contracts/run-kinds.yaml | 24/2 |
| engine/stages/read.py · source.py | 713/126 · 46/1 |
| engine/lanes/contract.py | 67/1 |
| engine/lanes/plan.py · file_adapter.py · replay_adapter.py | 2/7 · 6/4 · 2/2 |
| engine/paths.py · stages/__init__.py | 19/0 · 69/0 |
| engine/render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py · convergence.py · dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

이 변경은 재시도 여부·defects·판정서에 닿습니다. 동일성 주장을 **같은 입력의 최초 요청서**로 한정한 문안은 맞습니다.

**검증 경로**

모든 명령은 지정 사본에서 실행했습니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 시험은 `PY - <<'PY' … PY`로 실행했으며 파일을 만들지 않았습니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 마지막 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `bede71c9272068c566419cc4af6c38fb838cb504` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `19983ea8781c55678b64051c5f8053f74a3dbca1b0a756769bc8c1fe03e0aaa2` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **빈 출력** |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 R2 | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · **exit 0 · synth_eligible=true** |
| 요청 6개 → 계약 재계산·재렌더 | `REQUEST_6_VALIDATED 6` |
| 구동 반환·gate·pointer 대입 | `CLASSIFY CONTRADICTION_PHASE 14 AFTER_EXCEPTION 14` |
| 실제 enter 오류·증거 실패·LanePending | `EXIT_CODE=14` / `EXIT_CODE=14` / `EXIT_CODE=10` |
| 스냅샷 쓰기·복사를 메모리로 대체 | `SNAP_PRESERVED True SIDECAR_MATCH True` |
| 실제 발주 전건 검사·상한 | `OVER_LIMIT exit 15 unchanged True` |
| 실제 read.run, 진입·종결 가드 및 출력 대체 | `REAL_EARLY True 1 6` |
| `candidates`·`comp_texts_fn`의 5→1 사례 | `[['M10'], ['M10'], ['M10'], ['M10'], ['M10']] automatic_inferior_counter=False` |
| `sample_indices`·원문 단락 대조 | `RESOLVED 27 / 27` |
| `node --input-type=module -`로 Workflow 본문, agent/pipeline 대체 | `toString`·`constructor`·`/./` 모두 **calls=0** |
| 봉투 CLI 미리보기 → 실제 `continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 실제 `_dispatch`에 모델 mismatch 응답 | `returned 1 ok False rejected False mismatch True` |

v6에는 **`_next_dispatch`가 없습니다.** 그 기능을 담당하는 `cmd_dispatch`를 시험했습니다. 발췌 스크립트의 `ex1/ex2`는 실행하지 않았습니다.

기준 계수는 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 3/20/7/10**, 조기 검사 2행·완주 13행입니다. 표본은 **CL-2·4·7·9·12·14·16·19·21·24**이며 인용 locator 27개가 전부 해소됐습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다. 사본의 정본화 원천과 `PATENT_META` 일치만 확인했습니다.
- Workflow 실호출, 실제 transcript/journal 형식·model·effort·문맥 격리는 검증하지 않았습니다. Node 시험은 본문 분기 시험입니다.
- 실제 worktree의 source/read 쓰기 실행, 봉투 발행·재개, 생산 원장 append·동시 쓰기는 하지 않았습니다. read 제어 흐름 시험은 진입·종결 가드와 출력 경로를 대체했습니다.
- 시간·비용·토큰·가용 메모리 추정은 검증하지 않았습니다.
- 전 판본 메모가 동봉된 것은 확인했으며, 이번 상세 대조는 v3·v11·v12 및 선행 처분·지적 관련 부분입니다.

**읽은 파일**

- 원장: T40 전문, `D-20260905-02-pdm2b-seats.md` §17 추기 포함, SPEC §8.4 지정 행, T14·T17·T38, 선행 감수 1·2차 및 3~11차 관련 지적.
- 계약: `run-kinds.yaml`, `read.yaml` 지정 블록, approval-envelope·convergence 스키마.
- 대상: 설계 메모 v3·v11·v12, bundle 스크립트 5종.
- 구현: `engine/stages/read.py`·`source.py`, `engine/lanes/plan.py`·`contract.py`·`file_adapter.py`, `engine/paths.py`, `reader/lib/convergence.py`·`run_checks.py`·`report.py`의 관련 함수.
- 실물: 기준 런 run.yaml·원천·조기/완주 판정서·명세·요청/응답 6개·lane-log, donor 명세·통합 요청/응답·로그, 지정 Git 커밋의 부모·tree·blob·diff.

정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았습니다. 파일·임시물·캐시를 만들지 않았고, 실측 레인은 시작하지 않았습니다.