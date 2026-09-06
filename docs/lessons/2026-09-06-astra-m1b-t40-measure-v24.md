# 독립 감수 원문 — M1b 설계 도전 24차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v25 · 판정 REVISE(HIGH 1 · MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `32c929dbd9585b7ce5f66e92a3c8a7ad2850fd10448d16298a58a85c53e696e1` · 16011 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v24/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(17:27 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `d711f25` · 마커 3항 일치 · 메모 v25 sha256 `b1372a1d…` · v1~v24 + 회귀표 v5 + 자문 봉투·회신 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 24회」 명기. 폐쇄 = **이전 86건 closed 75 · partially 11 · open 0**(NU-2·3·4 closed · NU-1 partially). **B·C·E·F PASS**(19회 연속). 회귀표 83 사례는 도전자 재실행에서도 전건 PASS · 러너가 못 만드는 L 부모 없음 · 동시 청구항 실패·read.schema 출구 실패·refused 경로도 수용 확인.

**판정 = REVISE · 3건(HIGH 1 · MED 2) · 기각 0 · 발주자 귀책.** **NV-1 MED**: 거부 행을 소비열과 대기 요청 양쪽에서 제외해 **재시도 요청에 대한 반향 거부로 예외 종결한 합법 자료를 「예산이 남았는데 재시도 요청이 없다」로 오거부** — 더 나쁘게 그 거부 행을 지우면 통과(정직한 기록이 벌 받는 자리). **NV-2 MED**: 그룹 내부 순서만 보고 국면 사이 순서(분해 → 접지 → 통합)는 존재로만 판정 → lane-log 배열 순서를 뒤바꾼 생성 불가능한 자료를 정상 완료로 수용. **NV-3 HIGH**: 첫 스냅샷 S 를 같은 런의 후속 E(재시도 뒤 1.0 pass)로 바꾸고 sidecar 를 맞추면 통과 — `S.attempt ≤ E.attempt` 로는 S 가 **최초 관측**인지 알 수 없어 첫 exact-match 실패(0.92 fail)가 임계용 출력에서 사라진다(MY-6·MZ-3·NS-2 미폐쇄의 직접 증거).

**처분 = 전부 수용 · 그러나 v26 은 보류.** Owner 육성(17:3x 「멤돈다 싶으면 말해줘. Astra pro도 있으니」 → 총괄 판독 「맴돈다」 → 「지금 만들자」)으로 **자문 2회차 봉투**(`~/projects/workspaces/advice/t40-metrics-closure-20260906/t40-metrics-closure-20260906-1742/` · 재실행 오라클(replay) 건전성 · 위협 모델 축소 · 권고 순서)를 24차 판정 전에 발행했다. NV-1~3 셋은 모두 **재실행 오라클이 구조적으로 닫는 부류**(재실행은 거부 행·소비 순서·첫 E 를 러너가 다시 만든다)이므로, 같은 방식의 패치(v26)로 25차를 띄우지 않고 자문 회신을 받아 방식을 정한 뒤 v26 을 쓴다. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 24**. 다음 = 자문 회신 처분 → v26 → **M1b 25차 도전(지적 `NW-*`)**.

지적 열거 = NV-1, NV-2, NV-3

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 24회)

**MY~NU 86건: closed 75 · partially 11 · open 0.** 회귀표 83건은 전건 PASS를 재현했습니다. 그러나 합법적 재시도 거부 자료의 오거부, 생성 불가능한 소비 순서의 수용, 최초 스냅샷의 후속 판정 대체가 남았습니다. **실측 착수 불가**입니다.

외부 자문은 `ADVICE-REPLY.md`와 §17상 이미 회신·반영됐습니다. 대기 중으로 판단하지 않았으며 계수는 이어갑니다.

**A — 원장 정합·MY~NU 폐쇄표: REVISE**

`partially`는 지정 반례의 수정과 원문이 요구한 불변식의 폐쇄를 구별한 판정입니다.

| 회차 | closed | partially | open |
|---|---|---|---|
| MY | MY-1~5·7~13 | MY-6 | — |
| MZ | MZ-1·2·4~9 | MZ-3 | — |
| NA | NA-1~7 | — | — |
| NB | NB-1~3 | — | — |
| NC | NC-1~3 | — | — |
| ND | ND-1~2 | — | — |
| NE | NE-1~2 | — | — |
| NF | NF-1 | — | — |
| NG | NG-1~2 | — | — |
| NH | NH-1~2 | — | — |
| NI | NI-1~2 | — | — |
| NJ | NJ-1 | — | — |
| NK | NK-1 | — | — |
| NL | NL-1 | — | — |
| NM | NM-1~2 | — | — |
| NN | NN-1·2·4 | NN-3 | — |
| NO | NO-3 | NO-1·2·4 | — |
| NP | NP-1~3 | — | — |
| NQ | NQ-1~3 | — | — |
| NR | NR-2~6 | NR-1 | — |
| NS | NS-1·3~6 | NS-2 | — |
| NT | NT-1·4·5 | NT-2·3 | — |
| NU | NU-2·3·4 | NU-1 | — |

잔여는 합법적 재시도 예외·소비 사슬 → NV-1·2, 최초 관측 회차 결속 → NV-3입니다.

§8의 격 구분은 유지 가능합니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 이행입니다. ⓘ의 청구항 단위와 ⓚ의 기준 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표시는 구현 재량입니다. G-12는 여전히 미집행입니다. 이번 운영을 `source → read`에 한정하는 것과 엔진 전역의 종료선·비게시 강제는 구별해야 합니다.

**지적 목록 — HIGH 1 · MED 2**

**NV-1 · MED — 재시도 거부 행을 반복에서 지워 합법적 예외 종결을 거부한다.**

좌표: 메모 §5 조기 루프 재구성·§9 D①④; [t40_metrics.py:early_loop_check](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:233), 특히 258·261·338·339행.

거부 행은 소비열에서 제외됩니다. 동시에 `rowed`에 있다는 이유로 대기 요청에서도 제외됩니다. 따라서 **실재하는 재시도 요청과 그 거부 사건이 모두 반복 복원에서 사라집니다.**

R1의 ID·`partial/read`·`530b096`·xhigh 프로필로 다음 자료를 실제 러너에서 생성했습니다.

1. a0에서 종속항 하나 제거 → 청구항 실패 → a1 대기.
2. a1에 잘못된 반향 공급 → `LaneStaleResponseError`.
3. 러너가 a0·b0 소비 행과 a1 거부 행, 메모 2건의 원장 행, `terminated:true` 포인터를 기록.

가드는 `(True, 'shadow_pointer')`였습니다. 추출 결과는 다음과 같습니다.

```text
CLAIM_PENDING       → 0 in-progress
CLAIM_RETRY_STALE   → 4 “예산이 남았는데 재시도 요청이 없다”
EXACT_RETRY_STALE   → 4 “예산 남은 실행이 있고 재시도 요청이 없다”
```

더 나쁜 대조도 성립했습니다. **청구항 재시도의 실제 거부 행 하나만 삭제하면** 같은 요청·응답·포인터·원장을 수용합니다.

```text
REJECT_LOG_PRESENT → 4
REJECT_LOG_DELETED → 0 terminated-incomplete
```

정직하게 남긴 거부 기록이 있을 때 실패하고, 그 기록을 지웠을 때 통과합니다. 재시도 예산 소진과 재시도 실행 중 예외 종결을 구별해야 합니다.

**고치는 문안:** “조기 반복에 재시도 요청의 소비·대기·거부·예외 중단을 구별해 결속하고, 예외 종결을 예산 소진으로 요구하지 않으며 실제 거부 행의 삭제도 결측으로 거부한다.”

**NV-2 · MED — 그룹 내부 순서만 검사하여 국면 사이의 불가능한 소비 순서를 수용한다.**

좌표: 메모 §5 소비 사슬·기록 접두부; [t40_metrics.py:tail_chain_check](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:349), 특히 393~398행.

접지 그룹 내부의 순서는 검사하지만, 그 그룹이 분해 뒤에 기록됐는지, 통합이 접지 뒤에 기록됐는지는 검사하지 않습니다. 선행 소비 행의 **존재**가 선행 **순서**의 증거가 됩니다.

실제 R1 정상 완료 자료에서 다른 파일·행 필드·지문을 유지하고 lane-log 배열 순서만 바꿨습니다.

```text
ORDER_CONTROL             → 0 complete
SYNTH_BEFORE_DECOMPOSE     → 0 complete
GROUND_BEFORE_READ_B       → 0 complete
```

첫 변형은 마지막 통합 행을 로그 맨 앞으로 옮겼습니다. 둘째는 접지 세 행을 read-b 분해 행 앞으로 옮겼습니다. 두 순서 모두 `read.run`의 조기 루프와 `_execute_canonical_tail`이 생성할 수 없습니다.

이는 실제 러너가 그 순서로 실행했다는 주장이 아니라, **생성 불가능한 순서로 바꾼 증거를 정상 완료 지표로 승인한다는 반증**입니다.

**고치는 문안:** “lane-log 전체를 분해 반복 완료→접지 그룹→통합→후속 재시도의 허용 소비 순서와 대조하여 그룹 내부뿐 아니라 국면·회차 사이의 순서 역전도 exit 4로 거부한다.”

**NV-3 · HIGH — 첫 스냅샷을 후속 조기 판정으로 바꿔도 임계용 지표로 수용한다.**

좌표: 메모 §2 첫 스냅샷·§5 ㉠; [t40_metrics.py:metrics](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:900).

현재 회차 대조는 `S.attempt ≤ E.attempt`입니다. 이것으로는 **S가 최초 관측 판정인지** 확인할 수 없습니다.

실제 R1에서 L14와 같은 exact-match 재시도 경로를 생성했습니다. 구동기의 실제 `snapshot_first_early`가 보존한 S와 현재 E는 다음과 같았습니다.

| 자료 | attempt | dependent-set |
|---|---:|---|
| 실제 첫 스냅샷 S | 1 | **0.92 · fail** |
| 재시도 후 현재 E | 2 | **1.0 · pass** |

이후 **S를 현재 E로 교체하고 sidecar SHA를 그 바이트에 맞췄습니다.** 현재 E·완주 판정서·요청·응답·로그·봉투는 바꾸지 않았습니다.

```text
SNAPSHOT_CONTROL         → 0 complete, early attempt=1, 0.92/fail
SNAPSHOT_REPLACED_BY_E2   → 0 complete, early attempt=2, 1.0/pass
```

단순 SHA 불일치나 타 런 혼입은 거부합니다. 그러나 같은 런의 후속 판정으로 최초 측정을 대체하면 **첫 exact-match 실패가 임계용 출력에서 사라집니다.** 이는 MY-6·MZ-3·NS-2의 회차 결속이 아직 닫히지 않았다는 직접 증거입니다.

**고치는 문안:** “S를 재구성한 조기 실행 이력과 구동기의 최초 관측 시점에 결속하여 후속 E 대체를 거부하고, 최초 관측을 입증할 수 없으면 후속 값을 임계에 쓰지 않는다.”

**B~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| B 계측 커밋 셋 | **PASS** | 부모·절차 tree·팔 전체 diff·numstat·프로필·기준 요청 재렌더 일치 |
| C 구동 v6 | **PASS — 메모리 검증 범위** | 실제 enter 실패→14, 분류식, 기록 실패, 발주 상한, 무변경 조회, 스냅샷 보존 확인 |
| D 지표 v25·회귀표 v5 | **REVISE** | NV-1~3 |
| E 발췌 v4 | **PASS — 확인 범위** | 27단위·자동 열위 없음·5→1 후보 재사용·표본과 인용 해소 확인 |
| F Workflow v4 | **PASS — Node 대체 실행 범위** | 사전 거부 12종, 모델·effort 옵션, wrote/null 구별 확인 |
| G 결정 공백 | **REVISE** | 합법적 실패 자료와 최초 측정의 처분이 구현과 어긋남 |

새 좌석 값이나 임계의 재정을 요구하는 지적은 없습니다. 기존 재정과 러너에 맞춰 외부 검증층을 수정할 사항입니다.

**D — NU 수정 의미·회귀표의 증명 범위**

| 지적 | 판정 | 직접 확인한 내용 |
|---|---|---|
| NU-1 | **partially** | 비대칭 재시도 L16과 회차·순서 변형 C62·67은 수정됨. 두 실행 동시 청구항 실패와 순차 재시도도 통과. 재시도 거부 종결은 NV-1 |
| NU-2 | **closed — 원문 지정 범위** | 마지막 소비 read-a 분해의 claims, 동일 source/rules의 `ReadView`, profiles·attempt를 사용해 기대 좌표 재도출. `defects=None` 차이는 문안에만 닿고 좌표에는 영향 없음. 그룹별 세 기록 형태와 C63·64 확인 |
| NU-3 | **closed** | 러너 ⑥의 blocked_by·early_passed·in_scope·applied·entered 식과 일치. 봉투로 진입한 경우 결속 확인. 봉투 작성 직후 아직 재개하지 않은 대기 게이트도 수용 |
| NU-4 | **closed — 증거 수집 범위** | 실제 구동 함수로 dispatch 필드·좌표별 call_no·counter·스냅샷·early-noconv를 생성. L03 문안, L10→NS-3, L14→NR-1 대응 수정 확인 |

회귀표는 **18개 L 부모와 65개 C 변형, 총 83건**입니다. 이번 재실행에서 러너가 생성하지 못하는 L 부모는 발견하지 못했습니다. 다만 전체 구동의 동치 시험은 아닙니다. `enter`는 cwd 이동·worktree 검사를 생략하고, `Fx.run`은 `cmd_read` 전체 대신 `read.run`을 호출합니다. 재사용한 세 증거 함수는 절대경로를 사용하므로 이 결속에서 필드 의미가 달라지지 않았습니다.

추가 경로도 확인했습니다.

- **동시 청구항 실패:** a0·b0 모두 실패→a1 대기→a1 소비·b1 대기→상신→봉투→완료. 각 관측점 모두 수용.
- **exact-match 재시도에서 새 청구항 실패:** 예산 소진 뒤 5행·수렴 미실행 상신 자료를 수용.
- **`read.schema` 출구 실패:** 통합 항목에 금지 속성 공급→후속 재시도→`halt`, 13행 → `terminated-failure`.
- **응답 짝 없음:** FileLaneAdapter에 다른 lane_id를 공급하면 `load_response`가 먼저 `LaneContractError`를 내며 로그는 빈 배열입니다. 이를 `record(req,None)` 경로의 실측 증명으로 세지 않았습니다. C33은 손상 변형입니다.
- **refused:** 진입 후 원장 루트 해석을 실패시키고 깨진 응답을 공급해 `terminated:true·memo_count:0·root_source:refused`를 생성했습니다. 루트 해석 복구 후 `terminated-incomplete`로 수용됐습니다.

대응 지적 열은 현재 실행과 부합합니다. **83건 PASS가 NV-1~3까지 피복한다는 뜻은 아닙니다.**

**검증 경로**

모든 명령은 지정 사본에서 실행했습니다. `PY`는 다음 약칭입니다.

```text
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python
```

메모리 시험은 `PY -c '<하네스와 시험 본문>'`으로 실행했습니다. 파일 I/O는 dict·BytesIO로, 회귀표의 서브프로세스는 동일 DRIVER·봉투 본문의 메모리 실행으로 대체했습니다. 러너·FileLaneAdapter·검사·구동 증거 함수는 실제 본문을 사용했습니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `d711f25e1650b66c981eea314be4e4a64281fafd` — path·pin·order·disposable 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `b1372a1d863a742b87bd28e1496eaafef8fa56854585d476fa1263732af6fbac` |
| `git log -1 --format='%H %P'` 세 ref | base 부모 `6d92cad`; R1·R2 부모 `ad4c6c3` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만, 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git ls-tree` 기준·base 절차 | 모두 `d7717eb8750115a49e81ec7803790093b98c40ec` |
| base→R1/R2 전체 diff·numstat | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | §0′ 비절차 16파일 수치 전부 일치 |
| `git diff --stat 6d92cad HEAD -- engine contracts reader` | 빈 출력 |
| Git YAML → `lane_profiles()` | R1 분해·통합만 xhigh; R2 종속 접지만 sonnet/high |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | **exit 4**, `기준 런은 --law-tree … 필수다` |
| 기준 원본 + Git 절차 메모리 법 → `metrics` | `BASELINE 0 … complete … 163 … component_count:56` |
| 기준 요청 JSON → `LaneRequest` → `render_request_md` | `REQUEST_RERENDER_BYTES_EQUAL 6` |
| `CASES()`의 L 생성·C 변형 → `metrics` | **`CASES 83 FAIL 0 []`** |
| 옵션 부재·스냅샷 부재·SHA 불일치·타 런 S | 모두 exit 4 |
| 재시도 거부 원본·거부 행 삭제 대조 | `REJECT_LOG_PRESENT … 4`; `REJECT_LOG_DELETED … 0 terminated-incomplete` |
| 로그 순서만 변경 | `SYNTH_BEFORE_DECOMPOSE … 0 complete` |
| 최초 S를 E2로 교체 | `SNAPSHOT_REPLACED_BY_E2 … 0 complete` |
| 실제 enter·분류·기록 실패 | `ACTUAL_ENTER_MISSING (14, 'EXIT_CODE=14')`; `CLASSIFY 7 True`; `EXCEPTION_RECORD False` |
| `cmd_dispatch` 4회·`cmd_lanes` | `DISPATCH [0, 0, 0, 15] LANES 0 UNCHANGED True` |
| 실제 스냅샷 함수·회귀 수집 | `SNAPSHOT_NOCONV 1 PRESERVED True`; `REGRESS_EARLY_NOCONV 1` |
| `shadow_ledger_root`의 linked-worktree 분기 | `('/memory/main', 'main-worktree-resolved')` |
| 발췌 함수 import·5→1 병합 | `['M99', 'M99', 'M99', 'M99', 'M99'] NO_AUTOMATIC_INFERIOR` |
| `node --input-type=module -`·agent/pipeline 대체 | `WORKFLOW_REJECT 12 / 12`; wrote·not_written·dropped 각각 1 |

기준 계수는 **163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 일치했습니다. 표본은 **CL-2·4·7·9·12·14·16·19·21·24**, 인용 locator **27개 전부 해소**됐습니다.

`run_repo`와 법 트리 분리도 확인했습니다. `RunPaths`와 원장 해석에는 런 리포가, 코드·계약·규칙·절차에는 별도 법 트리가 전달됩니다. 메모리 기준 추출의 원장은 `/memory/baseline/ledgers/…`였고 `/memory/baseline/law/…`가 아니었습니다.

**[미검증]**

- 실제 Workflow 모델 호출·transcript/journal 이벤트 구조·문맥 격리·실호출 effort는 검증하지 않았습니다. Node 시험은 본문 분기·옵션 검사입니다.
- 물리 worktree 생성·source 봉인·생산 원장 append·동시 쓰기는 실행하지 않았습니다.
- 사본에 없는 도면 바이트는 source-report의 파일명·지문 목록으로 진입 검사에 공급했습니다. 도면의 물리적 봉인 검증으로 주장하지 않습니다.
- 메모리 법의 실행 코드·계약은 사본과 바이트 동일한 범위이며 절차는 `git show origin/t40-base:<경로>`로 공급했습니다. 실제 ad4c6c3 worktree 실행은 아닙니다.
- 외부 스테이징 TXT·도면, 시간·토큰·메모리 추정, 09-01 CLI의 실호출 effort는 미검증입니다.

**읽은 파일**

- 원장: T40 §1·§4·§5, `D-20260905-02-pdm2b-seats.md` §17 추기 전량, SPEC §8.4 지정 행, T14·T17·T38.
- 도전 기록: 1·2차 원문, 3~23차 지적·고치는 문안·폐쇄 및 검증 관련 절.
- 대상: 설계 v25, v24 대조, 구동·지표·회귀·발췌·Workflow·봉투 6종, 회귀표, 자문 봉투·회신.
- 계약·구현: 지정 run-kinds/read 계약과 승인·수렴·재료 스키마, `read.py`·`source.py`·`paths.py`·`gitpin.py`·진입 검사, 레인 plan/contract/file_adapter, ReadView, convergence/run_checks/report의 관련 경로.
- 기준 런: run.yaml, 원천·source-report, 조기·완주 판정서, 명세, 봉투, 원장·포인터, 레인 요청·응답·로그.

파일·임시물·캐시를 어디에도 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.