# 독립 감사 원문 — 좁은 재감사 7(RK · 축소 범위 · 라운드 M2a-3 `8ceea90` + 기록 `dee4a17`·`9adabca`) · M9 = claude-fable-5-1 xhigh(3회째) · 판정 PASS

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`out.txt` = `jq -r .result raw.json` · sha256 `92091665de263c8deeb19ee3f3b02b81e3d85e6db3982b730fcfe74b79c5d96d` · 10087 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/fable-audit-round-m2a3/`.

**좌석 = `좌석 M9` · `claude-fable-5-1` xhigh · CLI · allowlist · `setsid nohup`** · 19:51:44 → 20:04:01(**12.3분**) · **25턴 · `end_turn`** · **USAGE = input 418 · cache_create 135,904 · cache_read 1,048,519 · output 37,312(thinking 18,327) · `total_cost_usd` 4.85**. 사본 `~/projects/workspaces/pd-audit-round-m2a3`(detached `9adabca`) · 축소 범위(전체 plain 1모드 · 변조 8종 × m26 23노드). 발주문 = drafts `AUDIT-ORDER-round-m2a3.md`(M1b MO-1 반영판).

**판정 = PASS · RJ-1~4 전건 closed · 신규 BLOCKER/HIGH/MED/LOW 0 · 재개 0.** 변조 8종(D7 · D6 · D2 · D2b · D1 · D3 전체 · D4 · D5) 을 감사자가 직접 가해 **실패 집합 8/8 이 발주문 기대와 정확히 일치**(D7·D6 = {ⓙ, ⓜ3} · D2·D2b = {ⓚ} · D1 = {ⓛ} · D3 = {ⓜ1×3} · D4 = {ⓜ2} · D5 = {ⓜ3}) · 기존 15노드 전 회 초록 · 정상 코드 23/23 · 동적 프로브로 ⓙ 의 생산 경로(`root_source=main-worktree-resolved` · 재호출 `(True, "shadow_ledger")`)·ⓜ1 세 사유 문언·ⓜ2 `StageError`(누출 아님)·ⓜ3 dispatch 0 실측 · ⓦ 반전 표 ↔ 코드·변조 실출력 정합 · 전체 plain `843 passed in 156.62s` · 관문 plain 0 · 생산 원장 sha 매회 독립 측정 동일 · 총괄 기록 §40~§44·HANDOFF·DISPOSITIONS 정합(중단 레인 항목 9 · `FINAL` 0바이트 실재 확인). **Q4 = PD-M2a 러너 무결성(B-1 + G-5) 은 감사상 닫힌 상태** · 남은 것 = ⓦ 사후 확인(T39 · Owner). 관측(지적 아님) = ⑴ `__pycache__` 누출 재확인(백로그 ⑻) ⑵ **m2 정적 관문 `_direct_engine_ledger_calls` 는 `shadow_root` 키워드 존재만 봐 `shadow_root=None` 을 통과시킨다** — MN 의 「생산 원장 보호 4중」 없이 같은 형태를 복제하면 정적 관문이 못 잡음 → **백로그 ⑼ 후보**.

지적 열거 = 없음

처분 = 없음(PASS). 사유·관측 기록 = `D-20260903-04-t31-t32.md` **§45**. **다음 = PD-M2a 러너 무결성 종결 상신(T39 · `/decision-brief` · ⓦ + RJ-5).**

---

# 감사 원문 (claude-fable-5-1 xhigh · M9 3회째 · 이 아래는 감사자 저작)

**감사 보고 — 좁은 재감사 7(RK · 축소 범위) · 라운드 M2a-3 `8ceea90` · 좌석 M9(fable xhigh 3회째)**

**① preflight**

```
path=/home/laptop/projects/workspaces/pd-audit-round-m2a3
pin=9adabca89234816fbaeed21f83d6194c25c9df98   order=AUDIT-round-m2a3-20260905   disposable=true
HEAD=9adabca89234816fbaeed21f83d6194c25c9df98   pin==HEAD: True
git status --short → "?? .audit-sandbox" (1줄)
정본 HEAD=9adabca · 정본 status 빈 출력 · 감사 중 정본 무접촉(읽기만)
생산 원장 ledgers/shadow/screening.jsonl = 6행 · sha256 e2350e0d…5df2 (사본·정본 동일 · 시작=종료 · 전체 plain · 변조 8회 · 프로브 전후 매회 독립 측정 전부 동일)
git diff-tree 8ceea90 → tests/test_m26_terminated_run_guard.py 한 파일 · numstat 307/0
read.py blob = 88b4c9d (시작 = 매 변조 원복 뒤 = 종료)
```

**② Q1 — RJ-1~4 폐쇄표(변조 8종 · 감사 원문 ③ 「변경 코드」 그대로 · m26 23노드 전건 · 매 회 원복 `git checkout --` → `git diff --stat` 빈 출력 · blob 88b4c9d 확인 · 전체 plain 과 순차)**

| 변조 | 변경 코드(내가 가함 · numstat) | 실출력 | 붉은 새 시험 | 기존 15 | 기대 표 |
|---|---|---|---|---|---|
| D7 | `ledger = shadow_screening_ledger(paths.repo, shadow_root)` → `os.path.join(shadow_root or paths.repo, *SHADOW_LEDGER_RELATIVE)` (1/1) | **2 failed, 21 passed** | ⓙ「DID NOT RAISE StageError; 재호출 뒤 주 원장 실제 2행」 · ⓜ3「dispatch 4회 뒤 append에서 누출 · ShadowLedgerRootError」 | 초록 | {ⓙ, ⓜ3} 일치 |
| D6 | `ledger_evidence` 직후 `if shadow_root is None: return False, None` (2/0) | **2 failed, 21 passed** | ⓙ「주 원장 실제 2행」 · ⓜ3「dispatch 4회 뒤 누출」 | 초록 | {ⓙ, ⓜ3} 일치(MO 정적 추론 실측 확인) |
| D2 | `row_run_id == run_id` → `.startswith(run_id)` (1/1) | **1 failed, 22 passed** | ⓚ `StageError 종결한 런 재호출 · 근거=shadow_ledger` | 초록 | {ⓚ} 일치 |
| D2b | `if True: found = True` (1/1) | **1 failed, 22 passed** | ⓚ 동일 문언 | 초록 | {ⓚ} 일치 |
| D1 | `if phase == "full":` → `if True:`(str 검사 유지) (1/1) | **1 failed, 22 passed** | ⓛ `StageError … 근거=convergence.json` | 초록 | {ⓛ} 일치 |
| D3 전체 | 판정서 로더 `try/except StageError`→센티널 + 비객체→센티널 + 비str phase→None (9/16) | **3 failed, 20 passed** | ⓜ1×3 전부「DID NOT RAISE StageError」 | 초록 | {ⓜ1×3} 일치 |
| D4 | 로더 `(OSError, UnicodeError)` → 센티널 (2/7) | **1 failed, 22 passed** | ⓜ2 `IsADirectoryError: … 10-read/lanes/shadow-ledger.json` 누출 | 초록 | {ⓜ2} 일치 |
| D5 | `except ShadowLedgerRootError: return False, None` (2/7) | **1 failed, 22 passed** | ⓜ3「dispatch 4회 뒤 append에서 누출」 | 초록 | {ⓜ3} 일치 |

8/8 이 발주문 기대 집합과 정확히 같고 기존 15노드는 전 회 초록. 정상 코드 m26 23/23 초록(전체 plain 안에서).

**동적 프로브(새 8노드 · 가드·해석기·포인터 쓰기 래핑 · 정상 코드)** — 실출력 요지:
- ⓐ **RJ-1 closed** — ⓙ 첫 통주: `_run_is_terminated(repo=<wt>, shadow_root=None)` → `(False, None)` · 해석기 `shadow_screening_ledger(repo=<wt>, shadow_root=None)` → `<main>/ledgers/shadow/screening.jsonl` · 포인터 페이로드 `root_source="main-worktree-resolved"` · `root=<main>` · 임시 주 원장 1행. 재호출: `_run_is_terminated(shadow_root=None)` → `(True, "shadow_ledger")`. `run_read_stage` 우회 실재(`read_stage.run` 직접 · 시험 416~422행, 455~461행). `reader/` 보충 목록 = 시험이 4파일 집합 상등을 단언하고 초록(`READER-VERSION` · `procedure/10·20·30`). 주 원장 sha 전후 동일(시험 475행 단언 · 초록). 생산 원장 sha = 내가 독립 측정 · 전후 동일. D7 붉는 사유 = 「주 원장 실제 2행」 = G-5 증상.
- ⓑ **RJ-2 closed** — 심은 2행은 객체 + `run_id` str(494~501행) → 형태 검사 통과 · 프로브 `_run_is_terminated` → `(False, None)`(판정 불가가 아니라 유효 비참) · 원장 3행 · D2·D2b 각각 붉음.
- ⓒ **RJ-3 closed** — `_fresh_run_with_responses` 126~128행 `10-read` 부재 확인이 129행 `write_lane_responses` 앞. 프로브 ⓛ `(False, None)` → 정상 종결 뒤 `phase: full` 덮어씀 단언. D1 붉음.
- ⓓ **RJ-4 closed** — ⓜ1 사유 실측: `{broken` → 「JSON 파싱 오류(Expecting property name…)」 / `null` → 「최상위가 객체가 아님(NoneType)」 / `{"phase": 0}` → 「phase가 문자열이 아님」(세 분기 각각). ⓜ2 → `StageError … 근거=shadow_pointer · 사유=읽기 오류([Errno 21] Is a directory…)`(누출 아님). ⓜ3 → 해석기 `ShadowLedgerRootError` → 가드 `StageError 종결 판정 불가 · 원장 루트 판정 거부` · dispatch 0 · 포인터 부재(시험 단언). D3·D4·D5 각각 해당 파라미터만 붉음. **ⓦ 반전 표**(docstring 8~18행) ↔ 코드 경로·변조 실출력 정합: ⓜ1 반전 = D3 결과(가드 통과·덮어씀) · ⓜ2 반전 = D4 결과(`IsADirectoryError`) · ⓜ3 반전 = D5 결과(dispatch 뒤 `ShadowLedgerRootError`) · ⓘ1 반전 = `_complete_run` 의 판정서 잔존 → `convergence.json` 근거 · ⓘ2·ⓘ3 반전 = 동일 ID 정상 행 잔존 → `shadow_ledger` 근거(재감사 6 M7 실측과 동일). MN 원문 표(m2a3v2 115~120행)와 행별 일치.

**③ 신규 지적** — BLOCKER/HIGH/MED **0**. LOW **0**. 재개 0.

관측(지적 아님 · 기록만): (i) `tests/fixtures/read-failure-grid/__pycache__` 가 전체 plain 중 `PYTHONDONTWRITEBYTECODE=1` 을 뚫고 생성(백로그 §33 ⑻ 재확인 · 삭제). (ii) m2 정적 관문 `_direct_engine_ledger_calls` 는 `shadow_root` **키워드 존재**만 보므로 ⓙ·ⓜ3 의 `shadow_root=None` 을 통과시킨다 — MM-1 이 예견하고 MN 이 「생산 원장 보호 4중」(tmp_path 격리 · git 주 트리 대조 · 기대≠생산 · `finally` 지문)으로 닫은 자리이며 실측 생산 원장 불변. 다음 사람이 그 4중 없이 같은 형태를 복제하면 정적 관문이 못 잡는다는 점만 백로그 후보로 둔다. (iii) `engine/stages/__pycache__` 1건은 내 `py_compile` 산물(삭제).

**④ Q2·Q3·Q4**

Q2 — `diff-tree 8ceea90` = m26 한 파일 · numstat 307/0 · AST: 구 최상위 함수 19(시험 11 + 헬퍼 8) **전부 동일** · 삭제·변경 0 · 추가 8(헬퍼 2 + 시험 6) · 비함수 문 16 → 22(추가만: `__doc__ +=` · import 5) · 모듈 docstring 원문 동일 · 시험 11 → 17 · 노드 15 → 23. `engine/ contracts/ reader/ docs/SPEC.md` m2·m16 무접촉(커밋 파일 1). 새 시험의 m2·m16 접촉 = 호출만(속성 대입 0 · `monkeypatch.setattr(m2.ReplayLaneAdapter, "dispatch")` 1건은 기존 ⓐ와 같은 꼴). 커밋 메시지 시험 계수 없음(「삭제 0」은 행 계수).

Q3 — §42 ↔ 실측: plain **`843 passed in 156.62s`**(835 + 8) · 관문 7종 plain `GATE_FAILS=0` · `check_failure_table --self-test` `mutations=36 rejected=36` exit 0 · D7 `2 failed, 21 passed` ⓙ+ⓜ3 동일 · 「함수 6 · 노드 8 → 17함수 23노드」 동일. §43 ↔ `final.txt`: sha256 `e36a4dcc…a53472` · 3608 B · 끝 개행 정규화 뒤 본문 동일. M1b 원문 ↔ `FINAL`: MM `924de0e1…`(13646 B) · MN `e80929d1…`(10489 B) · MO `cca049b4…`(12135 B) 세 건 모두 정규화 뒤 동일이며 바이트 포함. §40 ↔ MM 원문·DISPOSITIONS: MM-1 HIGH · MM-2 MED · MM-3~6 LOW · 전부 수용 일치. §41 ↔ MN: PASS · 「지적 열거 = 없음」 일치. §44 ↔ MO-1 LOW 수용 · 발주문 v1→v2 diff = 핀 `dee4a17`→`9adabca` · §1 행 추가 · Q1 실패 집합 표·비겹침 · Q3 「FINAL 0바이트 실재」 정정 — 반영 확인. §41 절차 오류 ↔ `astra-m1b-m2a3v2-aborted-v1copy/` 실물: 항목 **9**(EV·FINAL·PREFLIGHT·RUNNER·SPEC·SPEC-m1b-m2a3v2.md·STATUS·launch.log·launch.sh) · STATUS 마지막 줄 `START=2026-09-05 18:55:48` · `FINAL` **0바이트 실재** · `launch.log` 「Terminated」 · 완료 보고 없음 = 「산출 없음」 정합. HANDOFF 27차 좌표(drafts `AUDIT-ORDER-round-m2a3.md`·`.v1.md` · 사본 · `pd-audit10-basetemp` · 레인 `fable-audit-round-m2a3/brief.md` · `advice-bundle.sh`) 실재. `check_dispositions` exit 0 · RJ-1~5·MM·MO 행 실재. RULINGS-LEDGER T38 행 실재.

Q4 — **PD-M2a 러너 무결성(B-1 + G-5)은 감사상 닫힌 상태다.** 재감사 6 이 구현 적합(T38 ①②③)을 확정했고, 이 감사가 그 시험 공백 4건의 폐쇄를 변조 8종 × 23노드 실출력으로 확정했다. 남은 것 = ⓦ 사후 확인(fail-closed 추인 · 대가 둘 · RJ-5 `refused` 기록 도달 불능 병기 · 코드 무변경 확인) 1건 — Owner 의 T39 상신 사항. 위 관측 (ii) 는 백로그 후보. 그 외 백로그 = `D-04` §27 ⑴~⑺ + §33 ⑻.

**⑤ [미검증]**

- `-O` 모드 전체(843 passed, 1 warning) · 관문 7종 `-O` — 축소 범위 · 레인·총괄 보고값 인용.
- §40·§41·§44 의 USAGE·소요 시간(레인 STATUS·EV 미대조).
- 레인 §43 표의 계수(「1 failed, 15 passed, 7 deselected」)는 인용만 · 위 ② 가 내 실출력.

**종료 조건**

```
HEAD=9adabca89234816fbaeed21f83d6194c25c9df98 · git status --short = "?? .audit-sandbox"(1줄) · git diff --stat 빈 출력
read.py blob=88b4c9d(원복) · basetemp pd-audit10-basetemp 항목 0 · __pycache__ 0 · .pytest-basetemp 없음 · /tmp 무접촉(TMPDIR 전 실행 지정 · 정본 리포 쓰기 0)
생산 원장 sha e2350e0d…5df2 · 6행(사본·정본 · 시작=종료) · 정본 HEAD 9adabca · 정본 status 빈 출력
```

판정 근거 요약: RJ-1~4 **전건 closed** — 변조 8종 각각이 발주문 기대 실패 집합과 정확히 일치하고 기존 15노드는 전 회 초록, 정상 코드는 23/23. 신규 BLOCKER/HIGH/MED/LOW 0. 총괄 기록 §40~§44 · HANDOFF · DISPOSITIONS 은 원문·실물과 정합.

VERDICT: PASS
