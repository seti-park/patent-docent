# 독립 감수 원문 — M1b 설계 도전 16차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v16 · 판정 REVISE(MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `c87e7436a14593f9ac5e7d132d10d20ae6a6840a794daddd87618eb67b4aa569` · 18007 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v16/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 09:09:05 → 09:27 · **USAGE = input 5,131,394(cached 4,927,616) · output 27,151(reasoning 7,499)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `fbf7823` · v16 sha256 `7f78f51a…` · v1~v15 동봉 · 지표 v16). 폐쇄 = **이전 51건 closed 48 · partially 3(MZ-2 · NA-1 · NM-1) · open 0**(NM-2 닫힘 · NM-1 반례 4 중 3 닫힘). **B·C·E·F PASS**(11회 연속).

**판정 = REVISE · 4건(MED 4) · 기각 0 · 발주자 귀책.** **NN-1**: 조기 청구항 검사 4행 제거 반례가 그대로 통과(첫·끝 id 존재만 검사). **NN-2**: 접지 로그 행 + 응답 동반 결측 · 정상 행 중복을 수용(역방향 대조가 응답 있는 발주만 요구 · 재실행 lane-log 검사의 checked 를 기록과 미대조). **NN-3**: 정상 완료의 기록 요건을 모든 국면에 적용해 **합법적 대기·실패 자료를 거부**(조기 상신 대기 · 접지 retry 일부 도착 · NA-1 경로 · 출구 원천 재독 실패 full/halt 4행 → 전부 exit 4). **NN-4**: lane-log 필드 하나 결측(`requested_effort`)이 출력 변환에서 KeyError → exit 1.

지적 열거 = NN-1, NN-2, NN-3, NN-4

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 15**. **전부 수용 → 지표 v17 = 런 상태 인식 재설계**(포인터 terminated + 완주 판정서 형태로 state ∈ {complete, awaiting, terminated-failure} 판정 → 완전성 요건은 complete 에만 · 그 외 상태는 위조·혼입·손상만 거부하고 지표는 N/A · 조기 검사 id 다중집합 · lane-log 필드·타입 검증 · lane_id 유일 · 엔진 lane-log 검사 checked ↔ 기록 대조 · complete 에서 발주 좌표 전건 행 존재) → **M1b 17차 도전(지적 `NO-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 51건: closed 48 · partially 3(MZ-2·NA-1·NM-1) · open 0.** NM-2는 닫혔습니다. NM-1의 지정 반례 네 개 중 **세 개만 닫혔으며**, 조기 청구항 검사 4행 제거는 여전히 정상 수용합니다. 추가 결측 통로와 정상 중단 자료의 오거부를 확인했습니다. **신규 NN-1~4, 모두 MED. 실측 착수 불가입니다.**

사본 마커의 path·pin·order·disposable과 HEAD를 확인했습니다. HEAD는 `fbf78231c10221d578650a4f2b6d8e1b983ca2d1`, 메모 SHA-256은 `7f78f51a5e0876f40ff24e3944b759343df4803157ab81d7208c5b5b410870ff`입니다.

**A — 이전 지적 폐쇄표**

범위 표기는 해당 ID 각각에 적용합니다. 폐쇄는 기존 지적의 반례·처분 범위에 대한 판정입니다.

| 이전 지적 | v16 판정 | 근거 |
|---|---|---|
| MY-1~2 | closed | 고정 핀·절차 동일성·잡음 방향 한정 확인 |
| MY-3~4 | closed | 기준 27단위·Owner 명시 판정·종속 청구항 10개 |
| MY-5~7 | closed | 수확 제외·이전 통합값으로 후퇴하지 않음·6축·검사 배열 보존 |
| MY-8~9 | closed | 종료 분류·실제 read-a→read-b 순서 확인 |
| MY-10~13 | closed | 완료 구별·호출별 보존·전 런 보존·원장 누적 설명 |
| MZ-1 | closed | 5→1 병합 후보를 다섯 단위에서 재사용 |
| **MZ-2** | **partially** | 미실행 스냅샷 제외는 유지. 정상 대기·실패 자료의 부분 지표 추출은 NN-3으로 회귀 |
| MZ-3~6 | closed | 스냅샷 결속·예외 분류·최신 부적격 처리·검사 귀속 추정 유지 |
| MZ-7~9 | closed | 부모 기준 증명·발주 상한·Map·정규 경로 거부 |
| **NA-1** | **partially** | 최신 디스크 좌표 선택은 유지. 로그 없는 계약 거부 시도가 N/A 처리 전에 차단됨: NN-3 |
| NA-2~7 | closed | 예외 경계·조회/발주 분리·형태 검증·다중 기록 설명·경로 결속·발췌 처분 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 검사·판정서 검증 경계 |
| NC-1~3 | closed | 실제 enter 오류→14·스냅샷 동일 바이트 처리·수치 범위 |
| ND-1~2 | closed | findings 계약 검증·계수 바이트 자체의 SHA 대조 |
| NE-1~2 | closed | 조기·완주 공통 형태 검증·finding 검증 유지 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조·실행본 버전 표기 |
| NH-1~2 | closed | 개별 요청·응답 결속·baseline 우회 차단 |
| NI-1~2 | closed | 요청 MD 지문 재계산·dispatch 지문 대조·원천 지문 사슬 |
| NJ-1 | closed | 원천 부재·변경 거부·재읽기 경계 이탈 제거 |
| NK-1 | closed | 명세 필수 필드 결측 거부 |
| NL-1 | closed | grounding·component 전량 제거·dependents=[] 모두 exit 4 |
| **NM-1** | **partially** | 지정 반례 3/4 차단. 조기 검사 행 결측 및 레인 기록 완전성 잔여: NN-1·2 |
| **NM-2** | **closed** | 원천 읽기 1회. 두 번째 읽기 PermissionError가 발생할 재읽기 자체가 없음 |

§8의 격은 유지됩니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 문언 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표기는 재량입니다. 아래 잔여는 이 해석을 실행할 증거 검증의 결함입니다.

**NN-1 · MED — 15차의 조기 청구항 검사 4행 결측 반례가 그대로 통과한다.**

좌표: 메모 §5 `[NM-1]`·§9 D; [t40_metrics.py:285](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:285); `read.run`의 `early_rows`.

실측 조기 판정서는 수렴이 실행됐다면 다음 **6행**입니다.

- `read.input-digest` 1행
- `read.claim-inventory`·`read.dependency-parse` 각각 read-a/read-b의 2행
- `read.convergence` 1행

그러나 v16은 첫 번째와 마지막 ID의 존재만 검사합니다. R0 식별자·정상 명세·6행 로그·dispatch·일치하는 스냅샷 sidecar를 공급하고 청구항 검사 4행만 제거한 CLI 본문 실행 결과:

```text
NM1_REMOVE_EARLY_CLAIM_4
exit 0 · early_checks 2 · lanes 6 · eligible true · na []
```

수렴 행까지 제거하면 exit 4지만, 그것으로 **청구항 검사만 제거한 지정 반례**가 닫히지는 않습니다. 기준 런의 역사적인 2행 서식과 이번 실측의 6행 서식을 구별해야 합니다.

**고치는 문안:** “행위시법·수렴 실행 여부에 따라 조기 검사 행의 기대 순서와 ID별 개수를 대조하고, 실측의 실행별 청구항 검사 행 누락·중복은 exit 4로 거부한다.”

**NN-2 · MED — 완주 기록과 모순되는 접지 로그 결측·중복을 정상 수용한다.**

좌표: 메모 §5 레인 기록 완전성; [t40_metrics.py:130](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:130), [385행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:385).

역방향 대조는 **응답 파일이 현재 존재하는 dispatch만** 요구합니다. 또한 재실행한 lane-log 검사 두 종류의 `checked`를 완주 판정서 기록과 비교하지 않습니다.

완주 판정서·명세·dispatch를 그대로 둔 독립 반례입니다.

| 변경 | v16 결과 |
|---|---|
| `read-a/ground-dependent/batch-1` 로그 행만 제거 | exit 4 |
| 위 로그 행과 해당 `response.json`을 함께 결측으로 제공 | **exit 0 · 로그 5행 · eligible=true · na=[]** |
| 정상 접지 로그 한 행을 중복 추가 | **exit 0 · 로그 7행 · eligible=true · na=[]** |

두 정상 수용 사례 모두 완주 판정서의 lane-log 검사 기록은 **checked=6**입니다. 재실행은 각각 **5/5**, **7/7**을 출력하면서 모순을 허용합니다. 첫 사례에서도 명세의 종속항 anchor **45/5**는 정상 지표로 남습니다.

기존 shape 검사는 분해 양쪽과 정본 통합의 존재 등을 검사합니다. 그것만으로 접지 배치별 소비 증거의 완전성을 증명할 수 없습니다.

**고치는 문안:** “완주 런은 lane-log 두 검사의 재실행 checked를 기록과 대조하고, 소비 좌표의 중복·누락을 dispatch 및 요청 기록으로 확인하여 응답 파일 동반 결측도 exit 4로 거부한다.”

**NN-3 · MED — 정상 완료의 기록 요건을 모든 국면에 적용하여 합법적인 대기·실패 자료를 거부한다.**

좌표: 메모 §5 결측 규칙·㉣ `[NA-1]`; `full_check_ids`·`rerun_lane_log_checks`·dispatch 역대조; `read.run`, `FileLaneAdapter.dispatch`.

v16의 새 검증은 다음 실제 실행 흐름과 맞지 않습니다.

| 합법적인 실행 상태 | 실물 근거 | v16 추출 결과 |
|---|---|---|
| 조기 상신 대기 | 실제 러너: early 6행·`terminated=false`·`awaiting=convergence_continue`·분해 로그만 존재 | **exit 4**, “정본 실행이 통합에 닿지 않았다” |
| 접지 retry 배치 일부만 응답 도착 | 실제 `FileLaneAdapter`+`_dispatch`: `LanePending`, 해당 배치 journal **0행** | **exit 4**, “응답이 있는데 lane-log 행이 없다” |
| 최신 synthesize retry가 `LaneContractError`로 거부되어 행 없음 | 메모 ㉣ 자체가 인정한 NA-1 경로 | **N/A 처리 전에 exit 4** |
| 출구 원천 재독 실패 | 실제 러너: `full/halt`, 검사 **4행**, `executed=false`, 명세 없음 | **exit 4**, 기대 검사 13행과 불일치 |

마지막 사례는 러너 쓰기 함수를 메모리로 바꾸고 출구 원천 읽기에만 `PermissionError`를 넣어 직접 생성했습니다.

```text
ACTUAL_FULL_EXIT_SOURCE_ERROR halt full
['read.input-digest', 'read.source-digest',
 'read.lane-log-shape', 'read.lane-log-digest-value']
executed False spec None
```

따라서 **`read.input-digest + READ_CHECK_IDS + lane-log 2종`은 정상 검사 경로의 13행과 일치하지만, 모든 `phase=full` 문서의 필수 집합은 아닙니다.**

또한 **파일 도착은 배치 소비 완료가 아닙니다.** 파일 어댑터는 배치 일부가 미도착이면 이미 읽은 응답도 `_dispatch`에 반환하지 않습니다. 이 구별 없이 역대조를 강화하면 정상 pending을 누락으로 오판합니다.

**고치는 문안:** “게이트·종결 상태·실행된 검사 경로·배치 소비/거부 기록으로 기대 증거 집합을 정하고, 합법적인 미실행은 기존 지표와 사유별 N/A를 보존하되 근거 없는 결측만 exit 4로 거부한다.”

**NN-4 · MED — 로그 필드 하나의 결측이 출력 변환에서 exit 4 경계를 벗어난다.**

좌표: 메모 §5 입력 검증 실패 처분; [t40_metrics.py:393](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:393).

`lane-log`의 `requested_effort` 한 필드를 제거하면 새 엔진 검사까지 통과한 뒤, `try` 바깥의 출력 변환이 직접 첨자 접근으로 실패합니다.

기준 런의 로그 읽기만 메모리로 대체하고 **실제 CLI 진입점**을 실행한 결과:

```text
KeyError: 'requested_effort'
```

**프로세스 exit 1, JSON 출력 없음**입니다. R0 메모리 하네스에서도 `requested_model`·`requested_effort`·`actual_effort`·`ok`·`mismatch` 각각의 결측이 같은 미포착 `KeyError`를 냈습니다.

**고치는 문안:** “출력에 사용하는 lane-log 필드의 존재·타입을 검증하고 출력 변환까지 동일한 exit 4 예외 경계 안에 둔다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합. 증거 결측 처리와 N/A 이행에 잔여 |
| **B 계측 커밋 셋** | **PASS** | 부모·절차 tree·팔 diff·16파일 numstat·프로필·동일 입력 요청 재렌더 일치 |
| **C 구동 v6** | **PASS** | 종료 분류·실제 enter 실패·증거 실패·스냅샷·조회/발주·상한 확인 |
| **D 지표 v16** | **REVISE** | NM-2 폐쇄. NN-1~4 잔존 |
| **E 발췌 v4** | **PASS** | 병합 후보 재사용·27단위·표본 결정론·판정 불가 처분 정합 |
| **F Workflow v4** | **PASS** | Node 대체 실행에서 지정 사전 거부·wrote/null 구별 확인 |
| **G 결정 공백** | **REVISE** | 결측·미실행·미소비를 구별하는 집행 규칙이 미완. 실행 중 수작업 선택 없이 결과 표를 만들 수 없음 |

C·E·F의 PASS는 정적·메모리 검증 범위입니다.

**B — 직접 검증한 사실**

base 부모는 `6d92cad`, R1·R2 부모는 `ad4c6c3`입니다. 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `6d92cad → base`는 절차 6파일뿐이며, 각 팔은 `2 2 contracts/stages/read.yaml`뿐입니다.

§0′의 변경 열거 **16파일 전부** 재실측과 일치했습니다.

| 파일 묶음 | 추가/삭제 |
|---|---|
| read.yaml · convergence 스키마 · run-kinds | 321/31 · 42/7 · 24/2 |
| read.py · source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| lanes/plan.py · file_adapter.py · replay_adapter.py | 2/7 · 6/4 · 2/2 |
| paths.py · stages/__init__.py | 19/0 · 69/0 |
| render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py · convergence.py · dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

실제 `lane_profiles()`는 R1의 분해·통합만 xhigh, R2의 종속 접지만 sonnet-5/high로 산출했습니다. base 절차 blob을 공급한 요청서 재렌더는 **6/6 바이트·입력 지문 동일**입니다. 검사·재시도 예산·소견은 후속 요청의 발생 및 `defects`에 닿으므로 동일성을 “같은 입력의 최초 요청”으로 한정한 문안은 맞습니다.

**D — 지정 반례와 회귀 결과**

| 지정 시험 | 결과 |
|---|---|
| read-b 분해 로그 행 제거 | exit 4 |
| synthesize 로그 1행만 유지 | exit 4 |
| 완주 엔진 검사 3행 제거 | exit 4 |
| **조기 청구항 검사 4행 제거** | **exit 0 — 미폐쇄** |
| 조기 수렴 검사 행 제거 | exit 4 |
| 두 번째 원천 읽기 PermissionError | **읽기 1회·exit 0** — 두 번째 읽기가 없어 예외도 없음 |

기준 CLI는 **exit 0·163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact/implication/positioning/figure_note 3/20/7/10·`na=[]`**였습니다.

기존 식별자·형태·수치·findings·스키마·원천·요청/응답·dispatch 결속 반례 **54건은 모두 exit 4**였습니다. 통합 계수 시점의 응답 교체·읽기 실패도 부적격 N/A로 처리됐습니다. 이 결과와 별개로 **로그 없는 최신 계약 거부 시도의 N/A 경로는 NN-3으로 회귀**했습니다.

재검사 모듈의 실제 경로는 사본의 `reader/lib/run_checks.py`, `engine/stages/read.py`였습니다. 사본과 계측 base의 engine·reader/lib·규칙·명세 스키마 diff는 없었습니다. **기준 런의 재검사는 현재 사본 트리에서 수행한 것이며, 역사적 d4e6ca2 코드를 재기동한 것은 아닙니다.**

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 메모리 하네스는 `PY -c '…'` 또는 stdin으로 실행했으며 저장하지 않았습니다.

R0 반례는 기준 자료에 R0 식별자·partial/read·실제 청구항 검사로 만든 6행 조기 문서·dispatch 결속 필드를 공급하고, 파일 접근만 메모리로 대체했습니다. 스냅샷 변경 뒤에는 일치하는 sidecar를 공급했습니다. 검증 함수는 대체하지 않고 CLI 본문을 실행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `fbf78231c10221d578650a4f2b6d8e1b983ca2d1` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `7f78f51a5e0876f40ff24e3944b759343df4803157ab81d7208c5b5b410870ff` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| base→R1·R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · exit 0 |
| 요청 JSON→`LaneRequest`→base 절차로 `render_request_md` | `REQUEST_BYTES_AND_DIGEST 6 /6` |
| CLI 본문 + 조기 검사 4행 제거 | `exit 0 … early_checks 2 … eligible true … na []` |
| CLI 본문 + 접지 로그·응답 동반 결측 | `exit 0 … lanes 5 … shape_checked 5 … digest_checked 5` |
| CLI 본문 + 접지 로그 중복 | `exit 0 … lanes 7 … eligible true … na []` |
| 실제 파일 어댑터→`_dispatch`, 배치 일부 미도착 | `pending ['read-a/ground-dependent/retry-1/batch-0'] journal_rows 0` |
| 실제 러너, 출구 원천 읽기만 실패·출력 메모리화 | `halt full … executed False spec None` · 검사 4행 |
| 실제 CLI + 로그 `requested_effort` 제거 | `KeyError: 'requested_effort'` · **exit 1** |
| 지표 회귀 하네스 | `REGRESSION 54 expected_exit_4 unexpected []` |
| 실제 enter→`cmd_read`, 증거 기록 대체 | worktree 부재·잘못된 런 이름 모두 14 |
| 증거 기록 실패·종결 포인터 true | `ENGINE_EXCEPTION False 14` |
| `_record_exception`, 쓰기 실패 주입 | `False NO_RETHROW` |
| 스냅샷 복사·쓰기 메모리화 | `NOCONV True PRESERVED True SHA_MATCH True` |
| `cmd_dispatch`, 기록을 메모리화 | `DISPATCH D 15 UNCHANGED True` |
| 기존 배치 충돌 | `DISPATCH_COLLISION 14 UNCHANGED True` |
| `candidates`·`comp_texts_fn` | `MERGE_5_TO_1 [['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| 발췌와 동일한 점수·동점 규칙 | `EXACT_EXCERPT_SELF_MATCH 27 /27` |
| `sample_indices`·원문 단락 대조 | 표본 CL-2·4·7·9·12·14·16·19·21·24 · `LOCATORS 27 RESOLVED 27` |
| Node Workflow 본문·agent/pipeline 대체 | `toString`·`constructor`·`/./`·중복·교차·좌표 불일치 모두 calls 0 |
| 봉투 stdout 미리보기→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 최종 `git status --porcelain --untracked-files=no` | 빈 출력 |

**v6에는 `_next_dispatch`가 없습니다.** 현재 구현인 `cmd_dispatch`를 시험했습니다. 발췌 CLI는 실행하지 않았습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다.
- 실제 Workflow 모델 호출·transcript/journal 형식·실호출 effort·문맥 격리는 검증하지 않았습니다.
- 실제 worktree 생성·source 봉인·봉투 쓰기/재개·생산 원장 append는 수행하지 않았습니다. 러너 시험의 출력은 메모리로 대체했습니다.
- 서로 다른 법 트리를 한 Python 프로세스에 순차 import하는 재사용은 검증하지 않았습니다.
- 구동·발췌·Workflow의 이전 스크립트 원본과 바이트 비교는 하지 않았습니다. 현재 제공본의 동작을 재검증했습니다.
- 비용·시간·토큰·가용 메모리 추정은 검증하지 않았습니다.

**읽은 파일**

- 상류: T40 전문, `D-20260905-02-pdm2b-seats.md` §17·추기, 1·2차 도전 원문, 후속 지적·처분 관련 부분, 15차 원문, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v16, v15→v16 대조, bundle 스크립트 5종.
- 구현: read·source 러너, lane plan·contract·file_adapter, paths, reader의 convergence·run_checks·report·dependency_parse 관련 함수.
- 실물: 기준 run.yaml·원천·두 판정서·명세·로그·요청/응답 6벌, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.