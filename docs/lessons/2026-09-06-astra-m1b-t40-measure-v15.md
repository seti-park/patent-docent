# 독립 감수 원문 — M1b 설계 도전 15차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v15 · 판정 REVISE(MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `f4bd4ac4b2c7bf5f47c9db494782fc1c42f3e4bad66903c260c82ffaf3570db5` · 15494 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v15/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 08:51:13 → 09:04 · **USAGE = input 4,272,745(cached 4,076,032) · output 20,433(reasoning 3,555)**. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `2219624` · v15 sha256 `5935cd9a…` · v1~v14 동봉 · 지표 v15). 폐쇄 = **이전 49건 closed 48 · partially 1(NJ-1 → NM-2) · open 0**(NL-1 세 반례 닫힘). **B·C·E·F PASS**(10회 연속).

**판정 = REVISE · 2건(MED 2) · 기각 0 · 발주자 귀책.** **NM-1 MED**: 재실행 대상 밖 검사 3종(`read.input-digest` · `read.lane-log-shape` · `read.lane-log-digest-value`)의 행 결측과 lane-log 행 결측(read-b 분해 행 제거 · synthesize 1행만)을 정상 수용 — 결속 검사가 「남은 행만」 순회 · 기존 `check_lane_log_shape` 는 같은 5행 로그를 즉시 실패시킴. **NM-2 MED**: 원천을 SHA 검증 뒤 **다시 읽는** 인자 평가(`open(pm).read()`)가 예외 경계 밖 → 두 번째 읽기 PermissionError = exit 1(회귀).

지적 열거 = NM-1, NM-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 14**. **전부 수용 → 지표 v16(완주 판정서 검사 id 집합 = 그 런의 법의 READ_CHECK_IDS 전건·행당 1 · 조기 = input-digest·convergence 필수 · lane-log 를 엔진의 shape·digest-value 검사로 재검사 · 실측 런은 dispatch 좌표 ↔ lane-log 행 양방향 대조 · 원천 바이트 1회 읽기로 SHA 와 재실행 입력 공유 · 전부 exit 4 경계) → M1b 16차 도전(지적 `NN-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 49건: closed 48 · partially 1(NJ-1) · open 0.** NL-1의 세 집합 결측 반례는 닫혔습니다. 그러나 **검사·레인 기록의 부분 결측을 정상 수용하는 통로**, **원천 재독 실패의 exit 4 이탈**이 남았습니다. 신규 **NM-1·NM-2, 모두 MED**입니다. 실측 착수는 불가합니다.

사본의 path·pin·order·disposable을 확인했습니다. HEAD는 `22196248fb1286aa4597e7405537f7f0a34ddf38`, 메모 SHA-256은 `5935cd9aa40fa6fa720a9c98f161b8086a3f0f5af5fe84962927525ad2545cf3`입니다.

**A — 이전 지적 폐쇄표**

범위 표기는 해당 ID 각각에 적용합니다.

| 이전 지적 | v15 판정 | 근거 |
|---|---|---|
| MY-1~2 | closed | 고정 핀·절차 동일성 확인, 잡음 방향 미확정으로 한정 |
| MY-3~4 | closed | 기준 27단위·Owner 명시 판정, 종속 청구항 10개 표본 |
| MY-5~7 | closed | 수확 제외·최신 시도 선택·6축·검사 배열 및 findings 보존 |
| MY-8~9 | closed | 종료 분류와 read-a→read-b 구동 순서 정합 |
| MY-10~13 | closed | 완료 구별·호출별 증거·전 런 보존·원장 누적 설명 |
| MZ-1 | closed | 5→1 병합 후보를 다섯 단위에서 재사용, 자동 열위 없음 |
| MZ-2 | closed | 미실행 판정 제외·결측 처분 명시, NL-1의 명세 결측 차단 |
| MZ-3~6 | closed | 스냅샷 결속·예외 분류·부적격 최신 통합 N/A·검사 귀속 추정 |
| MZ-7~9 | closed | 부모 기준 증명·발주 상한·Map 및 정규 경로 거부 |
| NA-1~3 | closed | 로그 없는 최신 시도 N/A·예외 경계·조회/발주 분리 |
| NA-4~7 | closed | 필수 형태·다중 기록 설명·경로 결속·발췌 판정 불가 처분 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 사전검사·판정서 검증 경계 |
| NC-1~3 | closed | 실제 enter 오류→14·스냅샷 동일 바이트 처리·수치 범위 |
| ND-1~2 | closed | findings 계약 검증·계수할 응답 바이트의 SHA 대조 |
| NE-1~2 | closed | 완주 공통 검증·finding 필수 형태 검증 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조·실행본 버전 표기 |
| NH-1~2 | closed | 개별 요청·응답 결속과 baseline 우회 차단 유지 |
| NI-1~2 | closed | 요청 MD 지문 재계산·dispatch 대조·원천 지문 사슬 |
| **NJ-1** | **partially** | 원천 부재·첫 읽기 실패는 차단. **새 재독의 읽기 실패는 NM-2** |
| NK-1 | closed | claims·dependents·additions·anchor_state 결측을 스키마로 거부 |
| NL-1 | closed | grounding·component 전량 제거와 dependents=[] 모두 exit 4 |

NM-1은 기존 개별 행 결속 검사의 회귀가 아니라, **검사할 행 자체가 사라지는 별도 결측 통로**입니다.

§8의 격은 유지됩니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 문언 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표기는 재량입니다. 다만 그 이행을 주장할 증거 검증에 아래 잔여가 있습니다.

**NM-1 · MED — 재실행 대상 밖의 검사 행과 레인 기록이 사라져도 정상 지표로 수용한다.**

좌표: 메모 §5 추출기·검사 배열·입력 결속 사슬·§9 D/G; [t40_metrics.py:91](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:91) `rerun_read_checks`, [319행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:319) `for r in rows`.

`run_read_checks`는 10종을 반환합니다. `read.convergence`를 제외하면 대조하는 것은 9종입니다. 완주 판정서의 다음 3종은 재실행·필수 존재 검사 대상이 아닙니다.

- `read.input-digest`
- `read.lane-log-shape`
- `read.lane-log-digest-value`

또한 레인 결속 검사는 **남아 있는 로그 행만** 순회합니다. 로그에서 사라진 좌표는 요청·응답·dispatch와 대조하지 않습니다.

기준 자료에 R0 식별자·partial/read·6행 조기 판정서·정상 dispatch·스냅샷 및 일치 sidecar를 공급한 메모리 런에서 실제 CLI 본문을 실행했습니다.

| 단독 변경 | v15 결과 |
|---|---|
| `read-b/decompose/batch-0` 로그 행 제거 | exit 0 · 로그 5행 |
| synthesize 로그만 남김 | exit 0 · 로그 **1행** |
| 완주 판정서에서 위 엔진 검사 3행 제거 | exit 0 · 완주 검사 10행 |
| 조기 판정서에서 청구항 검사 4행 제거, sidecar 일치 | exit 0 · 조기 검사 2행 |

**네 사례 모두 `synth_eligible=true`, `na=[]`였습니다.** 원천·명세와 임계 지표는 정상값으로 출력됐습니다. 첫 사례는 실제 기준 런에서도 로그 읽기만 대체하여 동일하게 재현했습니다.

같은 5행 로그를 기존 `check_lane_log_shape`에 공급하면 즉시 실패합니다.

> `lane-log.decompose-present`: 분해는 두 독립 실행 각각에 존재해야 한다 — 없으면 수렴 검사의 전제가 없다

정상 엔진이 불완전한 런을 생성한다는 주장이 아닙니다. **수집된 증거의 일부가 누락됐는데도 정상 판정서·명세와 함께 적격 자료로 보고하는 반례**입니다.

**고치는 문안:** “행위시법과 국면별 필수 검사 ID·중복 수를 확인하고, 레인 기록은 기존 shape·digest-value 검사 및 요청·dispatch 좌표와 대조하여 누락·불일치는 exit 4로 거부한다.”

**NM-2 · MED — 원천 재독이 예외 경계 밖에 추가되어 ‘읽기 실패=exit 4’가 회귀했다.**

좌표: 메모 §5 NJ-1·NL-1 설명; [t40_metrics.py:211](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:211), [288행](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:288).

211행에서 원천을 읽어 SHA를 검증한 뒤, 288행이 같은 원천을 다시 읽습니다.

```python
rerun_read_checks(..., open(pm, "rb").read().decode("utf-8"), ...)
```

이 읽기는 함수 인자를 평가하는 단계이므로 `rerun_read_checks` 내부의 예외 경계에 들어가지 않습니다. 바깥 명세 검증의 `try`도 이미 끝났습니다.

첫 읽기는 정상 바이트, 두 번째 읽기만 `PermissionError`로 대체하여 실제 CLI 본문을 실행한 결과:

```text
PermissionError: NM-2: second source read denied
```

**실제 프로세스 exit 1**, JSON 출력 없음입니다. exit 4라는 명시 처분과 다릅니다.

**고치는 문안:** “원천 바이트를 한 번 읽어 같은 바이트로 SHA 검증과 READ 재실행 입력을 만들고, 읽기·디코딩·재실행 준비 실패를 모두 exit 4 경계 안에서 처리한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석은 정합. 증거 결측 처리와 NJ-1 이행에 잔여 |
| **B 계측 커밋 셋** | **PASS** | 부모·tree·팔 diff·프로필·numstat·동일 입력 요청 재렌더 일치 |
| **C 구동 v6** | **PASS** | 종료 분류·실제 enter 실패·증거 실패·스냅샷·조회/발주·상한 확인 |
| **D 지표 v15** | **REVISE** | NL-1 차단. 검사·로그 집합 결측과 원천 재독 예외는 NM-1·2 |
| **E 발췌 v4** | **PASS** | 병합 후보 재사용·표본 결정론·판정 불가 처분 정합 |
| **F Workflow v4** | **PASS** | Node 대체 실행에서 지정 사전 거부·wrote/null 구별 확인 |
| **G 결정 공백** | **REVISE** | 불완전한 증거가 정상 자료로 넘어가는 통로가 남음. 기존 계약의 검증 구현으로 수정 가능 |

C·E·F의 PASS는 정적·메모리 검증 범위이며 실제 모델 호출의 검증은 아닙니다.

**B — 직접 대조 결과**

base 부모는 `6d92cad`, R1·R2 부모는 모두 `ad4c6c3`입니다. 기준과 base의 절차 tree는 같은 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다.

`6d92cad → base`는 절차 6파일뿐이고, 각 팔은 `2 2 contracts/stages/read.yaml`뿐입니다. 실제 `lane_profiles()`도 R1의 분해·통합만 xhigh, R2의 종속 접지만 sonnet-5/high로 산출했습니다.

§0′의 변경 열거 **16파일 전부 재실측과 일치**했습니다.

| 파일 | 추가/삭제 |
|---|---:|
| read.yaml · convergence 스키마 · run-kinds | 321/31 · 42/7 · 24/2 |
| read.py · source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| lanes/plan.py · file_adapter.py · replay_adapter.py | 2/7 · 6/4 · 2/2 |
| paths.py · stages/__init__.py | 19/0 · 69/0 |
| render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py · convergence.py · dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

base 절차 blob을 공급한 현행 요청서 재렌더는 **6/6 바이트 동일·입력 지문 동일**입니다. 검사·재시도 예산·소견은 재시도 발생 및 `defects`를 통해 후속 요청에 닿으므로, 동일성을 최초의 같은 입력으로 한정한 문안은 맞습니다.

**D — v15 재실행의 정확한 범위**

기준 런은 exit 0이며 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 3/20/7/10**, `na=[]`로 재현됐습니다.

| 재실행 검사 | 재실행 checked = 완주 기록 |
|---|---:|
| schema · source-digest | 1 · 1 |
| verbatim | 357 |
| pointer-resolve | 774 |
| coverage | 112 |
| dependency-parse | 24 |
| value-derivation | 25 |
| bibliography | 13 |
| claim-inventory | 25 |

9종은 모두 pass·findings 0이며 기록과 일치합니다. **완주 13행 전부를 재실행한 것은 아닙니다.**

`read.convergence`는 `peer_spec=None`에서 `extras.skipped=True`, checked 0으로 반환합니다. 기록의 checked 6과 비교하지 않는 것은 타당합니다. 다만 출력 `recheck`에는 `status=pass, checked=0`으로 보이므로 이를 수렴 재검증 성공으로 읽어서는 안 됩니다. 임계용 6축은 별도 조기 스냅샷에서 가져옵니다.

`repo_root_of`와 두 스키마 탐색은 메모리 worktree 배치에서 해당 worktree를 선택했습니다. 별도 CLI 프로세스에서는 실제 `reader.lib.run_checks.__file__`와 기본 명세 스키마 경로가 모두 지정 사본 아래였습니다. 사본과 계측 base의 `engine`·`reader/lib`·규칙·명세 스키마 diff도 없었습니다. **기준 런 검증은 현재 사본 트리에서의 재검사이며, 역사적 `d4e6ca2` 코드를 재기동한 것은 아닙니다.**

NL-1 세 사례는 기준 모드와 R0 실측 모드 모두 exit 4였습니다. CLI는 먼저 verbatim checked 불일치를 발견합니다. 해당 소유 검사를 별도로 호출한 결과도 다음과 같습니다.

| 결측 | 기존 검사 결과 |
|---|---|
| grounding 전량 | coverage 실패 56건 |
| component 전량 | pointer-resolve 실패 112건 |
| dependents=[] | claim-inventory 실패 24건 |

기존 형태·식별자·수치·findings·원천·요청/응답 SHA 반례 **54건은 모두 기대한 exit 4**였습니다. 최신 mismatch·로그 없는 최신 synthesize·계수 시점 응답 바이트 교체는 모두 통합 N/A였고, run_id만 바꾼 실물 donor 명세는 원천 지문 불일치로 거부됐습니다.

**검증 경로**

모든 명령은 지정 사본에서 실행했습니다. `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`입니다. 하네스는 파일로 저장하지 않고 `PY - <<'PY' … PY`로 실행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `22196248fb1286aa4597e7405537f7f0a34ddf38` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `5935cd9aa40fa6fa…2545cf3` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| base→R1 및 base→R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | 마지막 `}` · exit 0 |
| 요청 JSON→`LaneRequest`→base 절차로 `render_request_md` | `REQUEST_BYTES_AND_DIGEST 6 / 6` |
| `runpy.run_path(..., run_name='__main__')` + R0 메모리 파일 접근 | `MEASURE_ONLY_SYNTH_LOG exit 0 … 'lanes': 1, 'eligible': True, 'na': []` |
| 같은 CLI + 원천 두 번째 읽기 실패 | `PermissionError: NM-2: second source read denied` · exit 1 |
| 지표 회귀 하네스 | `REGRESSION 54 expected 54 unexpected []` |
| `classify`·`classify_after_exception` 대입 | `CLASSIFY_CASES 10 10` |
| 실제 `enter`→`cmd_read`, 증거 기록 대체 | r0 worktree 부재·잘못된 런 이름 모두 14 |
| 종결 포인터 true + 증거 기록 실패 | `CMD_READ RuntimeError evidence False exit 14 expected 14` |
| `cmd_dispatch` 쓰기를 dict/StringIO로 대체 | `DISPATCH D 15 UNCHANGED True` |
| `cmd_lanes` 조회 | `LANES_UNCHANGED True` |
| 스냅샷 복사·쓰기를 메모리로 대체 | `SNAPSHOT NOCONV True PRESERVED True SHA_MATCH True` |
| 실제 `_dispatch` mismatch 응답 | `ACTUAL_DISPATCH_MISMATCH 1 [(False, False, True)]` |
| `candidates`·`comp_texts_fn` | `MERGE_5_TO_1 [['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| `sample_indices`·원문 단락 조회 | `LOCATORS 27 RESOLVED 27` |
| `node --input-type=module -`, Workflow 본문·agent/pipeline 대체 | `toString`·`constructor`·`/./` 및 지정 중복·교차 사례 모두 calls 0 |
| 봉투 stdout 미리보기→`continue_envelope_state` | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| `git status --porcelain --untracked-files=no` | 빈 출력 |

v6에는 **`_next_dispatch`가 없습니다.** 현재 구현 `cmd_dispatch`를 시험했습니다. 기존 배치 충돌은 14·무기록, 세 번 발주 뒤 네 번째는 15·무기록이었습니다.

발췌 CLI는 실행하지 않았습니다. 표본은 **CL-2·4·7·9·12·14·16·19·21·24**입니다. 인용 부재·미해소·접지 부재를 판정 불가로 표시하고 표본을 교체하지 않는 v4 처분은 원장과 정합합니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다.
- 실제 Workflow 호출·transcript/journal 형식·model/effort 증거·문맥 격리는 검증하지 않았습니다.
- 실제 worktree 생성·source 봉인·봉투 쓰기/재개·생산 원장 append는 수행하지 않았습니다.
- 한 프로세스에서 서로 다른 reader 트리를 이미 import한 뒤 재사용하는 경우는 검증하지 않았습니다.
- 시간·비용·토큰·가용 메모리 추정은 검증하지 않았습니다.

**읽은 파일**

- 원장·이력: T40, `D-20260905-02-pdm2b-seats.md` §17·추기, 1~14차 지적 본문·처분, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v15, v14→v15 대조, bundle 스크립트 5종.
- 구현: read·source 러너, lane plan·contract·file_adapter, paths, reader의 convergence·run_checks·report·spec_io 및 관련 검사.
- 실물: 기준 run.yaml·원천·판정서·명세·로그·요청/응답, donor 명세, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.