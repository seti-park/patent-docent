# 독립 감수 원문 — M1b 설계 도전 23차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v24 · 판정 REVISE(MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `1a6c32a57ab9a9f07197c5a8531ed18db2cb194175d6a2bbdf97a4cfdef37153` · 17788 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v23/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(16:42 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `fa3c931` · 마커 3항 일치 · 메모 v24 sha256 `2b56f0fb…` · v1~v23 + 회귀표 v4 + 자문 봉투·회신 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 23회」 명기. 폐쇄 = **이전 82건 closed 71 · partially 11 · open 0**(NT-1·NT-5 closed · NT-2·3·4 partially). **B·C·E·F PASS**(18회 연속). 회귀표 75 사례는 도전자 재실행에서도 전건 PASS — 그러나 **실제 R1 러너가 정상 완료한 자료를 거부하고 그 회차를 잘못 고친 자료를 수용하는 반례**가 남았다.

**판정 = REVISE · 4건(MED 4) · 기각 0 · 발주자 귀책.** **NU-1**: v24 가 read-a·read-b 의 같은 retry 발번을 한 반복으로 묶고 첫 요청의 결함 블록으로 수렴 실행 여부를 정했다 — `retry-1` 은 그 실행 자신의 재시도 번호라서, 청구항 재시도(a1)와 exact-match 재시도(b1)가 이어진 정상 완료(E 2 · full 1 · 8행)를 거부하고 E 를 1 로 낮춘 자료를 수용(도전자 ASYM_* 대조군). **NU-2**: 접지 그룹의 분모를 삭제 자료에서 가져와 좌표·행·발주 기록 동반 삭제를 놓쳤고, 반향 거부와 응답 짝 없음을 같은 부분 허용으로 묶어 거부 행 + 정상 소비 행의 생성 불가능한 혼합을 수용. **NU-3**: phase-gate 를 `entered=true` 하나로 받아 blocked_by 를 exact-match 로 바꾼 모순 게이트를 정상 완료로 승인. **NU-4**: 회귀 증거를 「구동기와 같은 규칙」이라 했지만 발주 기록의 call_no·batch·dispatch_id 필드 의미가 실제 `cmd_dispatch` 와 다르고 `early-noconv-*` 보존이 없었다 · L03 문안(예산 소진 halt ≠ 실제 escalate 반환) · L02→NS-3 · L13→NR-1 대응 오류.

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 23**. **전부 수용 → 지표 v25 + 회귀표 v5**(조기 루프를 실행별 발번·lane-log 소비 순서·재시도 요청의 결함 블록으로 재구성 — 청구항 재시도 실행은 직전 반복 실행만 · exact-match 재시도는 예산 남은 실행 전부의 접두 · 대기 요청은 현재 E 와 맞물림 · 재시도 없는 실패는 예산 소진에서만(NU-1) · 후속 기대 좌표를 정본 분해 응답 + `plan_grounding`/`lane_id_for` 로 재도출 · 그룹 기록 접두부 셋(정상 소비/반향 거부 하나/소비 접두 + 짝 없음)을 각각 대조(NU-2) · phase-gate 의 blocked_by·early_passed·envelope.in_scope/applied·entered 를 러너 생성식에서 재도출 · 봉투 진입이면 현재 봉투 결속 확인(NU-3) · **회귀표 v5 = 발주 기록·스냅샷을 구동기 `t40_drive.py` 의 실제 함수(`cmd_dispatch`·`snapshot_first_early`·`pending_coords`)로 수집 · 신규 L16(비대칭 재시도)·L17(접지 반향 거부) · C62~C67 · 문안·대응 열 정정 · 83 사례 PASS**(NU-4)) → **M1b 24차 도전(지적 `NV-*`)**.

지적 열거 = NU-1, NU-2, NU-3, NU-4

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 23회)

**MY~NT 82건: closed 71 · partially 11 · open 0.** 회귀표 75건은 전건 PASS를 재현했지만, 실제 R1 러너가 정상 완료한 자료를 거부하고 그 회차를 잘못 고친 자료를 수용하는 반례가 남았습니다. **실측 착수 불가**입니다.

외부 자문은 `ADVICE-REPLY.md`와 §17 추기상 이미 회신·반영됐습니다. 계수는 이어갑니다.

**A — 원장 정합·폐쇄표: REVISE**

`partially`는 지정 변형의 수정과 원문이 요구한 생성·결속 불변식의 폐쇄를 구별한 판정입니다.

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
| NT | NT-1·5 | NT-2·3·4 | — |

잔여 대응은 회차 결속·합법 상태 오거부 → NU-1, 소비 증거·상태 생성 관계 → NU-2·3, 회귀 증거의 구동기 동치 주장 → NU-4입니다.

§8의 격 구분은 유지 가능합니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 이행입니다. ⓘ의 청구항 단위와 ⓚ의 기준 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표시는 구현 재량입니다.

G-12는 미집행입니다. 이번 구동을 `source → read`에서 멈추는 운영 범위는 성립하지만, 종료선과 비게시가 엔진 전역에서 강제된다는 뜻은 아닙니다.

**NU-1 · MED — 실행별 retry 발번을 조기 루프의 공통 반복 번호로 오인한다.**

좌표: 메모 §5 회차 등식·§9 D①; [t40_metrics.py:213](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:213)의 `decompose_iterations`, `early_iterations_check`, 특히 249행의 첫 요청 선택; [read.py:1815](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1815)의 실행별 재시도 선택.

`retry-1`은 **그 실행 자신의 재시도 번호**입니다. 그런데 v24는 read-a와 read-b의 같은 발번을 한 반복으로 묶고, 정렬상 첫 요청의 결함 블록으로 그 반복의 수렴 실행 여부를 결정합니다.

R1 ID·`partial/read`·`530b096` 메타데이터·xhigh 프로필을 적용하고, 빈 lanes에서 다음 경로를 생성했습니다.

| 실제 조기 루프 | 공급·검사 결과 | 다음 요청 |
|---|---|---|
| a0·b0 | a0에서 CL-25 제거, b0에서 종속항 문언 끝 한 글자 제거. 청구항 실패로 수렴 미실행 | a1만 |
| a1·b0 | a1 정상 복구. 첫 수렴이 dependent-set 실패 | 예산이 남은 b1만 |
| a1·b1 | b1 정상 복구. 두 번째 수렴은 상신 축만 미달 | 봉투 → 후속 → 정상 완료 |

a1의 결함은 `read.claim-inventory`, b1의 결함은 `read.convergence`입니다. **동일한 retry-1이 서로 다른 루프에서 생성됐습니다.**

실측 결과:

```text
ASYM_PENDING: E=1, 소비 로그 3행
→ exit 4: 마지막 완료 반복의 수렴 실행 여부 False ≠ 현재 executed=True

ASYM_COMPLETE: status=ok, E=2, full=1, 소비 로그 8행
→ exit 4: attempt=2 ≠ 재도출한 수렴 실행 수 1

ASYM_LOWERED_E_2_TO_1 0 complete
```

마지막 변형은 정상 완료 자료의 **현재 E.attempt만 2→1로 변경**했습니다. 올바른 자료를 거부하고 잘못된 회차를 수용합니다. L13과 L14를 따로 통과시킨 것으로 두 재시도 원인이 이어지는 경로까지 증명할 수 없습니다.

**고치는 문안:** “조기 루프는 실행별 발번·소비 순서·각 재시도 요청의 원인을 함께 사용해 재구성하고, 서로 다른 시점의 동일 retry 번호를 합치지 않으며 비대칭 재시도의 정상 E와 그 회차 변형을 대조한다.”

**NU-2 · MED — 접지 그룹의 완전성과 예외 기록 형태를 잘못 정의한다.**

좌표: 메모 §5 소비 사슬·§9 D①④; [t40_metrics.py:262](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:262)의 `tail_chain_check`, 특히 274·290행; [read.py:302](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:302)의 `_dispatch`; [plan.py:699](/home/laptop/projects/workspaces/pd-m1b-t40/engine/lanes/plan.py:699)의 `plan_grounding`.

두 통로를 재현했습니다.

- **그룹의 분모도 삭제 자료에서 가져옵니다.** R1의 정상 통합 대기 자료는 접지 셋을 소비했습니다. `ground-dependent/batch-1`의 요청·응답 디렉터리, 로그 행, 발주 기록을 함께 제거하자 남은 둘을 전량으로 간주했습니다.

  ```text
  R1_PENDING_CONTROL 0 in-progress
  CUT_GROUND_COORD   0 in-progress
  ```

  정본 분해와 `plan_grounding`으로 세 좌표를 재도출할 수 있는데도 결측을 놓칩니다.

- **반향 거부와 응답 짝 없음을 같은 부분 허용 조건으로 묶습니다.** 접지 batch-1에 낡은 반향을 공급하면 실제 FileLaneAdapter는 예외를 던지고 `_dispatch`는 **그 그룹의 거부 행 하나만** 남깁니다. 같은 요청을 가진 정상 대조군의 ground-independent 소비 행 하나를 이 로그에 추가해도 통과했습니다.

  ```text
  GROUND_STALE_CONTROL          0 terminated-incomplete
  GROUP_CONSUMED_PLUS_REJECTED  0 terminated-incomplete
  ```

  반향 거부는 `adapter.dispatch()`가 반환하기 전에 발생하므로, 같은 배치에 정상 소비 행과 공존하지 않습니다. `record(req,None)`이 남길 수 있는 소비 접두부와는 다른 경로입니다.

**고치는 문안:** “정본 분해와 plan_grounding으로 기대 접지 그룹을 재도출하고, 정상 소비·반향 거부·응답 짝 없음의 배치별 기록 접두부를 각각 대조하여 좌표 동반 결측과 생성 불가능한 혼합 행을 거부한다.”

**NU-3 · MED — 접지 진입 근거를 `entered=true` 하나로 받아들인다.**

좌표: 메모 §4·§5 소비 사슬·§9 D④; [t40_metrics.py:614](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:614)의 phase-gate 판독과 `tail_chain_check`; [read.py:1874](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1874)의 게이트 생성식.

정상 R1 완료 자료의 게이트는 상신 축 미달·유효 봉투 적용으로 `entered=true`였습니다. **`blocked_by`만 `convergence-exact-match`로 변경**했습니다.

```text
GATE_BLOCKED_EXACT_ENTERED 0 complete
{'entered': True, 'blocked_by': 'convergence-exact-match'}
```

러너는 exact-match 차단이면 `early_passed=false`, 봉투 범위 밖이므로 `envelope_applied=false`, 따라서 `entered=false`로 생성합니다. 이 모순은 T17·T40 §5의 봉투 범위와 직접 관계됩니다.

이는 러너가 실제로 금지된 진입을 했다는 주장이 아닙니다. **그렇게 기록된 모순 증거를 추출기가 정상 완료 지표로 승인한다는 반증**입니다.

**고치는 문안:** “게이트의 blocked_by·early_passed·봉투 적용·entered를 러너 생성식과 현재 판정에 대조하고, exact-match·청구항 차단과 entered=true의 공존은 exit 4로 거부한다.”

**NU-4 · MED — 회귀 증거를 구동기와 같은 규칙으로 수집한다는 주장이 과하다.**

좌표: 메모 §5 회귀표·§9 D②③; [t40_regress.py:134](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_regress.py:134)의 `collect_dispatch`·`snapshot_if_first`, `MAP`·`CASES`; [T40-REGRESS-TABLE.md:10](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-REGRESS-TABLE.md:10)의 L03.

빈 lanes 시작과 대기 요청 공급은 수정됐습니다. 판정서·로그·포인터도 러너가 생성합니다. 그러나 외부 증거는 여전히 축약 제조입니다.

같은 첫 synthesize 발주를 두 함수로 비교했습니다.

| 필드 | 회귀 수집기 | 실제 `cmd_dispatch` |
|---|---|---|
| `call_no` | 5: 러너 호출 수 | 1: 해당 좌표의 첫 발주 |
| `batch` | 0: 레인 batch 번호 | `compare`: 발주 배치명 |
| `dispatch_id` | `regress-006` | `compare-r0-read-a_synthesize_batch-0-c1` |

회귀 기록에는 `run·task·model_label·effort·request_md·response_json`도 없습니다. 또 L12의 수렴 미실행 판정은 실제 `snapshot_first_early`가 `early-noconv-*`로 보존하지만 회귀 수집기는 남기지 않습니다.

```text
L12_NOCONV_ARCHIVE_COUNT 0
```

문안·대응 열에도 수정이 필요합니다.

- **L03:** 생성 근거는 “예산 소진 halt”지만 실제 반환은 `escalate`입니다. 동일 실패 서명 재현 분기가 예산 검사보다 먼저 처리됩니다.
- **L02 → NS-3:** L02에는 mismatch 행이 없습니다. 해당 반례는 L10이 직접 담당합니다.
- **L13 → NR-1:** L13은 E=1/full=1입니다. 과거 `E≤full` 오거부를 직접 반증하는 부모는 E=2/full=1인 L14입니다.

75건 PASS 자체는 재현됐습니다. 다만 그것이 위 문안과 구동 증거의 동치까지 검증하지는 않습니다.

**고치는 문안:** “발주·스냅샷 증거는 실제 구동 함수를 재사용하거나 필드 의미와 보존 동치를 시험하고, 축약 모형은 그 범위를 명시하며 L03 처분과 지적 대응 열을 실제 실행에 맞춘다.”

**B~G 판정**

| 항목 | 판정 | 근거·잔여 |
|---|---|---|
| B 계측 커밋 셋 | **PASS** | 부모·전체 diff·절차 tree·numstat·프로필·기준 요청 재렌더 확인 |
| C 구동 v6 | **PASS — 메모리 범위** | 실제 enter 실패, 분류, 예외 기록 실패, 발주 상한, 무변경 조회, 스냅샷 확인 |
| D 지표 v24·회귀표 v4 | **REVISE** | NU-1~4 |
| E 발췌 v4 | **PASS — 확인 범위** | 기준 27단위, 5→1 후보 재사용, 표본·인용 해소, 판정 불가 처분 |
| F Workflow v4 | **PASS — Node 대체 실행 범위** | 사전 거부 12종, 하드 옵션, wrote/null 구별 |
| G 결정 공백 | **REVISE** | 정상 자료와 손상 자료의 처분이 생성 규칙과 어긋남 |

새 좌석 값이나 임계 재정을 요구하는 지적은 없습니다. 고정된 원장·러너에 맞춰 외부 검증층을 수정할 사항입니다.

**D — NT별 수정 의미와 추가 생성 경로**

| 지적 | 판정 | 확인 |
|---|---|---|
| NT-1 | **closed** | count·set 실패 소견의 rule·locus·found·expected가 실제 비교 함수와 일치. C50·51 거부. `threshold-missing`도 실제 생성 소견과 대조 성공 |
| NT-2 | **partially** | full 등식, 청구항 단독·exact-match 단독 재시도는 수정. 두 원인이 이어지는 비대칭 경로는 NU-1 |
| NT-3 | **partially** | 빈 로그·단일 행 삭제는 거부. 기대 그룹과 예외 기록 형태·게이트 정합은 NU-2·3 |
| NT-4 | **partially** | 도달 전 요청 선공급은 제거. 외부 증거 동치와 문안·대응 열은 NU-4 |
| NT-5 | **closed** | 법 파일 집합 양방향 비교·바이트 비교, 절차 핀, run_repo/법 트리 분리 확인 |

`convergence.unknown-axis`도 실제로 생성해 보았습니다. 추출기는 고정 6축 밖이라 exit 4로 거부합니다. 선등록 법에는 미지 축이 없으므로 이를 지원해야 할 합법 상태로 확대하지 않았습니다.

추가로 다음을 실제 러너 본문으로 생성했습니다.

- **read.schema 출구 실패:** 통합 항목에 최종 스키마 금지 속성을 공급 → 후속 retry-1 → `halt`, 검사 13행, 소비 로그 10행, full attempt 2 → `terminated-failure`.
- **retry-1 출구 원천 재독 실패:** full은 `executed=false·attempt=0·4행`, 마지막 synthesize 발번은 1 → 정상적으로 `terminated-failure`. full 등식의 실행 조건과 충돌하지 않습니다.
- **refused:** 진입 후 원장 루트 판정을 실패시키고 첫 응답을 깨진 JSON으로 공급 → 러너가 `terminated=true·memo_count=0·root_source=refused`를 기록. 가드는 `(True, 'shadow_pointer')`. 루트 해석을 복구한 뒤 추출은 `terminated-incomplete`였습니다.
- **mismatch 뒤 LaneAssignmentError:** L11에서 후속 소비 뒤, full 기록 전 예외 종결을 재현했습니다. 이 부모 자체의 행 형태는 합법입니다.

회귀표의 C행 대응은 대체로 실제 변형과 일치합니다. A-01 원장, A-02 왕복 메타·거부, A-03 생성·파생 관계, A-04 소견 합계, A-05 스냅샷 부재 및 C50~61의 NT 지정 변형을 확인했습니다. **전수 피복으로 판정하지 않습니다.**

**검증 경로**

모든 cwd는 지정 사본입니다. 아래 `PY`는 다음 명령의 약칭입니다.

```text
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python
```

메모리 하네스는 파일 I/O를 dict·BytesIO로, `Fx.run`의 서브프로세스 경계를 동일 `DRIVER` 본문의 메모리 실행으로 대체했습니다. 러너·FileLaneAdapter·검사·봉투 본문은 실제 코드를 사용했습니다. 사본에 없는 도면 바이트는 진입 검사용 파일명·지문 목록만 source-report에서 공급했습니다.

| 명령·호출 경로 | 마지막 출력 또는 핵심 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `fa3c931711b04738ff7ece0b066bf0323d94f775` — path·pin·order·disposable 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `2b56f0fb8ddfcc24b4c6991dd64cc2185149b1e8b0e9b1dac3a0dbc0c7828c5d` |
| `git log -1 --format='%H %P'` 세 ref | base 부모 `6d92cad`, R1·R2 부모 `ad4c6c3` |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만, 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git ls-tree` 기준·base 절차 | 모두 `d7717eb8750115a49e81ec7803790093b98c40ec` |
| base→R1/R2 전체 diff·numstat | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader` | §0′ 비절차 16파일 수치 전부 일치, 마지막 비절차 행 `90 35 reader/lib/run_checks.py` |
| Git YAML → `lane_profiles()` | R1 분해·통합만 xhigh, R2 종속 접지만 sonnet-5/high 및 aliases 확인 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | **exit 4**, `기준 런은 --law-tree … 필수다` |
| 기준 원본 + Git 절차 메모리 법 → `metrics` | `BASELINE 0 … complete … 163 … component_count:56` |
| 기준 요청 JSON → `LaneRequest` → `render_request_md` | `REQUEST_RERENDER_BYTES_EQUAL 6` |
| `PY -c '<메모리 하네스 + CASES build/mutate → metrics>'` | `CASES 75 FAIL 0 []` |
| 기존 스냅샷·형태·수치·식별·원천 변형 추가 | `HISTORICAL_MUTANTS 25 NOT_EXIT4 []` |
| first-early 옵션 없음·파일 부재·SHA/식별 불일치 | `NO_FIRST_EARLY_OPTION 4`, 관련 추가 변형 전부 exit 4 |
| 비대칭 재시도 실제 생성 → E만 2→1 | `ASYM_LOWERED_E_2_TO_1 0 complete` |
| 실제 반향 거부 그룹에 소비 행 추가 | `GROUP_CONSUMED_PLUS_REJECTED 0 terminated-incomplete` |
| 법 규칙·스키마·버전 변경, 파일 삭제 | 각각 exit 4, `법 파일 집합이 다르다` 등 |
| run_repo/법 트리 및 linked-root 분기 | `ROOT_SEPARATION True True`; `main-worktree-resolved` |
| `classify`·`classify_after_exception` | `CLASSIFY 7 True`; `CLASSIFY_AFTER_EXCEPTION 4 True` |
| 실제 enter 실패·증거 기록 실패 | `ACTUAL_ENTER … 14 EXIT_CODE=14`; `RECORD_EXCEPTION_NO_RETHROW False` |
| `cmd_dispatch` 4회·`cmd_lanes` | `DISPATCH [0, 0, 0, 15] QUERY_UNCHANGED True` |
| `snapshot_first_early` | `SNAPSHOT_KEPT True`; `NONCONV_NOT_SNAPSHOT True PRESERVED 1` |
| `candidates/comp_texts_fn` 5→1 병합 | `['M9', 'M9', 'M9', 'M9', 'M9']` |
| `sample_indices`·표본 locator 대조 | CL-2·4·7·9·12·14·16·19·21·24, `LOCATORS 27 27` |
| Node에서 Workflow 본문·agent/pipeline 대체 | 사전 거부 12종 모두 calls=0; `WORKFLOW_RESULT 1 1 1 REJECT_FAILS []` |

기준 계수는 **163항목·component 56·전체 anchor 51/5·종속항 anchor 45/5·통합 fact 3/implication 20/positioning 7/figure_note 10**으로 재현했습니다.

**[미검증]**

- 실제 Workflow/API 호출, transcript·journal 실물과 실제 모델·effort·문맥 격리.
- 외부 원시 TXT·도면 20개의 바이트, 새 `source.run`의 물리 봉인·Git 핀 집행.
- 실제 worktree 쓰기·원장 append·프로세스별 import 격리. 메모리 실행으로 대체했습니다.
- 비용·시간·토큰 추정과 Owner 내용 판독.

**읽은 파일**

T40 §1·4·5, D-20260905-02 §17·추기, SPEC 지정 행, T14·T17·T38, run-kinds·read 계약·approval-envelope 스키마; 1~22차 감수의 지적·수정 문안·관련 검증절; 설계 v24와 관련 이전 판본, bundle 구동·지표·회귀·발췌·Workflow·봉투·회귀표·자문 봉투와 회신; `read.py`·`source.py`·`plan.py`·`contract.py`·`file_adapter.py`·`paths.py`, convergence·run_checks·rules·report 관련 구현; 기준 런 메타데이터·원천·판정서·명세·원장·요청/응답 및 지정 Git blob.

물리 파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았고, 실측 레인은 시작하지 않았습니다.