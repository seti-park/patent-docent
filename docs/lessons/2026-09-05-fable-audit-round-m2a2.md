# 독립 감사 원문 — 재감사 6(RJ · 라운드 M2a-2 `1573591` + 기록 `d043abf`·`0189bdc`) · M9 = claude-fable-5-1 xhigh(2회째) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`out.txt` = `jq -r .result raw.json` · sha256 `bf10c6860dacd87f20b321f3e35b55ebaa332cd5d366b7062d7b375ca2f4f800` · 16866 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/fable-audit-round-m2a2/`(`brief.md` · `raw.json` · `usage.json` · `status`).

**좌석 = `좌석 M9` · `claude-fable-5-1` xhigh · CLI `claude -p` · allowlist · `MEMORY_HOOKS=off` · `setsid nohup`** · 18:00:22 → 18:39:45(**39.3분**) · **66턴 · `end_turn` · 절단 없음** · **USAGE = input 1,062 · cache_create 208,551 · cache_read 4,088,219 · output 92,420(thinking 44,687) · `total_cost_usd` 9.82**. 사본 `~/projects/workspaces/pd-audit-round-m2a2`(detached `0189bdc`) · basetemp 홈 fs `pd-audit9-basetemp`(감사자가 비움) · 종료 조건 충족. 발주문 = drafts `AUDIT-ORDER-round-m2a2.md`(M1b astra high ML-1~4 반영판).

**판정 = FAIL · MED 1 · LOW 4 · BLOCKER/HIGH 0 · 필수 재현 [미검증] 0.** **구현 결함 0** — 재정 T38 ①②③ 은 코드에 정확히 옮겨졌고(Q1 전건 · 발주 변조 7종 + V6 전건 검출 · 차별 대조 13/11 재현 · 생산 배치 프로브에서도 정상 코드는 옳게 동작), FAIL 은 **시험 공백**(발주자 귀책) 때문. 감사자가 고안 변조 **8종**(D1~D7 · 결합본)을 얹어 **6종이 대상 121건 · 결합본이 전체 835 를 생존**함을 실측. **RJ-1 MED**: 근거 ⑶(원장 행)의 **생산 경로**(링크된 worktree · `shadow_root=None` · P-U1 표준 배치)가 미피복 — D7(가드 해석기를 구 폴백 `shadow_root or repo` 로) 변조에서 재호출이 조용히 진행되어 **주 원장 2행 = G-5 증상 그대로**(정상 코드는 차단) · D6(`shadow_root is None` 이면 ⑶ 생략) 결합본 835 생존 → 시험 1건(임시 법 리포 + worktree · `repo=<worktree>, shadow_root=None` 통주 → 포인터·판정서 삭제 → 재호출 `StageError` · 주 원장 1행). **RJ-2 LOW**: 「다른 run_id 행 = 유효한 비참」 음성 사례 부재(D2 접두 일치 · D2b 아무 행 생존) → `<RUN_ID>-x`·무관 id 행 심고 가드 통과 1건. **RJ-3 LOW**: 비참 판정서(`phase != "full"`) 배치 부재(D1 생존 · 실물 위반 없음). **RJ-4 LOW**: 판정 불가 분기 중 판정서 손상·형태 / 읽기 오류 / 루트 거부 3종 미피복(D3·D4·D5 생존 · ⓦ 의 핀이 절반) → ⓦ 확정과 함께 3건. **RJ-5 LOW(ⓦ 설계 귀결)**: `_write_shadow_pointer` 의 `refused` 기록 분기가 `run()` 에서 도달 불능(가드가 거부를 먼저 판정 불가로 닫음) — 결함 아님 · **ⓦ 사후 확인에 병기**(docstring 정정 또는 거부 기록 유지 여부 = Owner). **ⓦ 판단** = fail-closed 는 T38 ③ 참 조건을 바꾸지 않는 오류 처리(S2 재량에 든다) · 대가 둘 = 쓰다 만 포인터 하나가 사람이 치울 때까지 그 런을 막음 · RJ-5 거부 기록 소실.

지적 열거 = RJ-1, RJ-2, RJ-3, RJ-4, RJ-5

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§39**. RJ-1~4 수용 → **수리 라운드 M2a-3(시험만 · 엔진 무접촉)** · RJ-5 수용 → ⓦ 상신에 병기.

---

# 감사 원문 (claude-fable-5-1 xhigh · M9 2회째 · 이 아래는 감사자 저작)

**감사 보고 — 재감사 6(RJ) · 라운드 M2a-2 `1573591` · 좌석 M9(fable xhigh 2회째)**

**① preflight**

```
path=/home/laptop/projects/workspaces/pd-audit-round-m2a2
pin=0189bdc180f7f1f7a7d8b758829c4a26c0ad1978   order=AUDIT-round-m2a2-20260905   disposable=true
HEAD=0189bdc180f7f1f7a7d8b758829c4a26c0ad1978   pin==HEAD: True
git status --short → "?? .audit-sandbox" (1줄)
정본 HEAD=0189bdc… · 정본 status 빈 출력 · 감사 중 정본 무접촉(읽기만)
생산 원장 ledgers/shadow/screening.jsonl = 6행 · sha256 e2350e0d…5df2 (사본·정본 동일 · 시작=종료)
git diff-tree 1573591 → docs/SPEC.md · engine/stages/read.py · tests/test_m25_… · tests/test_m26_…
blob: 0d078db:read.py=d5d70eb · 1573591:read.py=88b4c9d · numstat read.py 177/9
```

**② Q1 — 재정 T38 세 항목의 이행(전부 내가 직접 실측)**

| 재정 | 확인 항목 | 실측 |
|---|---|---|
| ③A 세 근거 · 읽기만 | AST 호출 목록: `_termination_error`={StageError} · `_load_termination_json`={open(path, encoding) · json.load} · `_run_is_terminated`={open(ledger, encoding) · json.loads · shadow_screening_ledger · isinstance×6 · .get×3} — 쓰기·append·makedirs 호출 0 · `open` 모드 인자 없음(읽기) | 적합 |
| ③A 세 갈래 | 부재=`FileNotFoundError`→센티널 / 유효 비참=`terminated:false`·`phase!="full"`·다른 run_id → 다음 근거 / 판정 불가=파싱·비객체·비bool·비str·OSError·UnicodeError·`ShadowLedgerRootError`·손상행·비객체 행·run_id 비str → `StageError`. `.get()` 은 세 곳 모두 `isinstance(…, dict)` 뒤 | 코드 분기로 실재 |
| ③A ML-2 독립 배치 | 정상 통주 → 포인터·`convergence.json` 삭제 → 격리 원장에 `null` / `[]` / `42` / `{"run_id": null}` 1행 추가 → 재호출 | 4건 모두 `StageError` · 문언에 「종결 판정 불가」·`shadow_ledger`·run_id·원장 경로 전부 실림(missing=[]) · 원장 sha256 불변 · 사유=「2행이 객체가 아님(NoneType/list/int)」 / 「run_id가 누락됐거나 문자열이 아님」 · AttributeError 0 |
| ②A 부작용 전 | `run()` 선행문: `RunPaths` → `load_yaml(run.yaml)` → `run_id` → `_run_is_terminated` → `raise StageError` → `contract` → `ensure_read_dirs()`(L1669) → … `try:`(L1723). 가드는 try 밖 | 자리 적합 |
| ②A 계수기(내 것) | 종결 런 재호출 중 `ensure_read_dirs`=0 · `dispatch`=0 · `append_screening_ledger`=0 · `write_json`=0 · `_finish_lane_log`=0 · `_write_shadow_pointer`=0 · `builtins.open` 쓰기 모드=0 · 런 루트 전체(집합·sha256·mtime) 불변 · 원장 sha 불변 · lane-log mtime 불변 · 신규 파일 [] | 부작용 0 |
| ①A 조기 상신=대기 | 첫 호출 `escalate` → 원장 파일 부재(0행) · 포인터 `terminated:false` + `awaiting:"convergence_continue"` · `convergence.json` 부재(`convergence-early.json` 실재) → 봉투 → 두 번째 호출 가드 통과 `ok` · dispatch=[decompose×2, ground-independent, ground-dependent, synthesize] · gate `blocked_by=convergence-escalation · entered=True · applied=True` → 원장 정확히 1행 · 최종 포인터 `terminated:true` · `awaiting` 키 부재 → 세 번째 호출 `StageError`(근거=shadow_pointer) · 원장 여전히 1행 | m22 상신 축 배치로 직접 확인 |
| ①A LanePending 포인터 | 키 = appended·ledger·memo_count·root·root_source·run_repo·terminated(7개) · `awaiting` 부재 | 적합 |
| ①A 문언·원장 | `git diff 0d078db 1573591 -- docs/decisions ledgers …` 빈 출력(P-U4 「한 행」 무개정) · 6행 sha 동일 | 적합 |

**③ Q2 — 변조표(발주 7종 + V6 + 고안 8종 · 대상 파일 = m26·m25·m22 봉투·m22 게이트·m16·m2 = 121노드 · M4 와 D 결합본은 전체 835)**

| 변조 | 변경 코드 | 예상 검출점 | 실측 |
|---|---|---|---|
| M1 가드 호출 제거 | `already_terminated, termination_evidence = False, None` | ⓐ | **12 failed**(ⓐⓑⓒⓖⓗ·ⓘ1×3·ⓘ2×2·ⓘ3×2) · ⓓⓔⓕ 초록 |
| M2 근거 ⑵ 제거 | `convergence = _TERMINATION_EVIDENCE_ABSENT` | ⓑ · ⓐⓒ 초록 | **1 failed = ⓑ**(문언 누락 `convergence.json` · 실제 근거=shadow_ledger) |
| M3 근거 ⑶ 제거 | `ledger_evidence=…` 직후 `return False, None` | ⓒ | **6 failed**(ⓒⓗ·ⓘ2×2·ⓘ3×2) · ⓐⓑⓖ 초록 |
| M4 조기 상신 `terminated=False` 제거 | 해당 줄 삭제 | ⓓ + 기존 6건 | **전체 835 중 7 failed** = ⓓ(「조기 상신 대기에 원장 행이 생겼다」) + m22 봉투 4 + `test_m2_read.py::test_grounding_requires_convergence_verdict_or_envelope` + `test_m22_phase_gate_binding.py::test_verdict_artifact_keys_equal_actual_phase_gate_keys` — 6건 전부 `read.py:1663 StageError 종결한 런 재호출 … 근거=shadow_pointer` |
| M5 가드를 `ensure_read_dirs()` 뒤로 | 가드 블록 이동 | ⓐ 계수 | **1 failed = ⓐ** 「실제 {'ensure_read_dirs': 1, …}」 |
| M6 포인터 값 즉시 반환 | `return bool(pointer_terminated), …` | ⓗ | **1 failed = ⓗ**(`DID NOT RAISE StageError`) |
| M7 판정 불가 → 그 근거 거짓 | 로더 2예외→센티널 · 포인터/판정서 형태→기본값 · 루트 거부→False · 손상행/비객체/비str→`continue` · 읽기 오류→False(16+/71−) | ⓘ 전건 · ⓐ~ⓗ 초록 | **7 failed = ⓘ1×3·ⓘ2×2·ⓘ3×2**(전부 「판정 불가 문언 누락 … 종결한 런 재호출」) |
| V6 플래그를 게시 앞으로 | 두 줄 교환 | ⑤ 만 | **1 failed = `test_first_lane_log_publish_oserror_falls_back_to_memory_journal`**(「기대 총 2회 호출, 실제 1회」) · m25 나머지 8 초록 |
| D1 ⒜ 비참 판정서 | `if phase == "full":` → `if True:`(str 검사 유지) | 없음 예상 | **121 passed(생존)** · 프로브: `{"phase":"early"}` 단독 → 정상=진행 / 변조=`StageError 종결재호출` |
| D2 ⒝ 접두 일치 | `==` → `.startswith(run_id)` | 없음 예상 | **121 passed(생존)** · 프로브: `<RUN_ID>-x` 행만 → 정상=진행(행 2) / 변조=`StageError`(정당한 런 차단) |
| D2b 아무 행이나 종결 | `if True: found = True` | 없음 예상 | **121 passed(생존)** · 「다른 run_id 행」 음성 사례가 스위트에 전무 |
| D3 ⒞ 판정서 손상·형태→부재 | 판정서 로더를 `try/except StageError`+형태 위반→센티널 | 없음 예상 | **121 passed(생존)** · 프로브: `{broken` 판정서(포인터·원장 없음) → 정상=판정불가 / 변조=진행 후 판정서 덮어씀 |
| D4 ⒞ 읽기 오류→부재 | 로더 `(OSError, UnicodeError)`→센티널 | 없음 예상 | **121 passed(생존)** · 프로브: 포인터 자리가 디렉터리 → 정상=판정불가 / 변조=진행 뒤 `IsADirectoryError` 누출 |
| D5 ⒞ 루트 거부→비종결 | `except ShadowLedgerRootError: return False, None` | 없음 예상 | **121 passed(생존)** · 프로브(bare clone 의 detached worktree · `shadow_root=None` · 새 런): 정상=가드 `StageError 판정불가(원장 루트 판정 거부)` · dispatch 0 · 포인터 없음 / 변조=레인 5건 dispatch 뒤 `finally` 에서 `ShadowLedgerRootError` |
| D6 `shadow_root is None` 이면 ⑶ 생략 | `ledger_evidence` 직후 조건 반환 | 없음 예상 | **121 passed(생존)** · 프로브(임시 주 작업 트리 법 리포 · `shadow_root=None` · 원장 행만): 정상=`StageError 종결재호출`(행 1 유지) / 변조=**진행 · 행 2** |
| D7 가드 해석기를 구 폴백으로 | `shadow_screening_ledger(paths.repo, shadow_root)` → `os.path.join(shadow_root or paths.repo, *SHADOW_LEDGER_RELATIVE)` | 없음 예상 | **121 passed(생존)** · 프로브(주 트리 + 링크된 worktree 에서 런 · `shadow_root=None` · 첫 런 `root_source=main-worktree-resolved` · 주 원장 1행 · worktree 고아 원장 없음 → 포인터·판정서 삭제 → 재호출): 정상=`StageError 종결재호출`(행 1) / 변조=**진행 · 주 원장 2행 = G-5 증상 그대로** |
| D1+D2+D3+D4+D5+D6 결합본 | 위 6종 동시(18+/19−) | — | **전체 835 passed**(어느 시험도 못 잡음) |

모든 변조는 `git checkout -- engine/stages/read.py` 로 원복했고 매 회 `git diff --stat` 빈 출력 · 원복 blob `88b4c9d` 를 확인했다. 프로브 전건에서 생산 원장(정본·사본) sha 불변.

**④ Q3 — 차별 대조 (i)**

`git show 0d078db:engine/stages/read.py > engine/stages/read.py`(blob 실측 `d5d70eb0…` 일치) · m26+m25 두 파일 · AST 계수 = m26 11함수 15노드 + m25 6함수 9노드 = 24노드.

```
13 failed, 11 passed in 13.21s
붉음 13 = ⓐ ⓑ ⓒ ⓓ ⓖ ⓗ · ⓘ1[null|broken-json|non-bool] · ⓘ2[before|after] · ⓘ3[None|malformed1]
초록 11 = ⓔ ⓕ · m25 9건(⑤ test_first_lane_log_publish_oserror_falls_back_to_memory_journal 포함)
사유: 12 × "Failed: DID NOT RAISE StageError" · 1 × "조기 상신 대기에 원장 행이 생겼다: [{'final_verdict': None, …}]"(ⓓ)
원복 뒤 git diff --stat 빈 출력 · blob 88b4c9d
```

§36 의 집합·계수와 동일. ⑤ 가 구 구현에서 초록 = 엔진 무변경 확인.

**⑤ 신규 지적**

- **RJ-1 · MED · 귀책 발주자** — 근거 ⑶(섀도 원장 행)의 **생산 경로가 시험에 미피복**. 좌표 `engine/stages/read.py:1147`(`shadow_screening_ledger(paths.repo, shadow_root)`) · `tests/test_m26_terminated_run_guard.py` 전건이 `m2.run_read_stage`(explicit `shadow_root`) 경유. 재현: D6·D7 변조가 대상 121건 생존, D6 은 결합본으로 전체 835 생존. D7 은 이 리포의 실제 구 결함(`shadow_root or repo` 폴백 · `engine/paths.py` docstring)을 가드에만 되살린 꼴이며, 재정 P-U1 의 표준 배치(링크된 worktree · `shadow_root=None`)에서 **재호출이 조용히 진행되어 주 원장에 2행**을 남긴다(정상 코드는 차단 · 내 프로브 실출력). 실물 코드는 옳다. 다만 T38 ③ ⑶ 이 덮기로 한 「append 뒤 포인터 실패」 경로의 회귀 보호가 격리 루트에서만 성립하고, 스위트는 G-5 증상 재발을 잡지 못한다. 격 근거 = Q2 규정(못 잡는 변조의 격은 T38 목적 「원장 오염 방지」를 깨는지) · 선례 MJ-5(오판정이 발주 시험을 통과 = MED). 처방 = m16 `test_worktree_run_grows_the_main_repo_ledger` 꼴로 임시 법 리포(contracts+reader 복사)·링크된 worktree 에서 `repo=<worktree>, shadow_root=None` 명시 통주 → 포인터·판정서 삭제 → 재호출 `StageError` · 주 원장 1행(내 프로브 약 30줄).
- **RJ-2 · LOW · 발주자** — ⑶ 「다른 run_id 의 행 = 유효한 비참」(MK-3 분기표) 음성 사례 부재. D2(접두)·D2b(아무 행) 생존. 시험은 격리 빈 원장만 쓰므로 판별식 자체가 핀되지 않았다. 생산 원장은 이미 4 run_id 6행이라 D2b 꼴 회귀는 첫 런에서 크게 실패(조용한 오염이 아님)하므로 LOW. `<RUN_ID>-x` · 무관 id 행을 심은 뒤 가드 통과 시험 1건 권고.
- **RJ-3 · LOW · 발주자** — ⑵ 비참 판정서(`phase != "full"`) 배치 부재(D1 생존). 엔진은 `convergence.json` 을 `phase="full"`(`read.py:2063`)로만 쓰고 조기본은 `convergence-early.json` 이므로 실물 위반·T38 ③ 문언 위반 없음.
- **RJ-4 · LOW · 발주자** — 판정 불가 분기 중 **판정서 손상·형태 / 읽기 오류(OSError·UnicodeError) / 루트 거부** 3종이 미피복(D3·D4·D5 생존 · ⓘ1~ⓘ3 은 포인터·원장만). ⓦ(fail-closed)의 핀이 절반만 있다. Owner 가 ⓦ 를 뒤집으면 기대값이 바뀌는 자리이므로 ⓦ 확정과 함께 3건 추가 권고.
- **RJ-5 · LOW · 발주자(ⓦ 설계 귀결)** — `_write_shadow_pointer` 의 `refused` 기록 분기(`read.py:2265~2272` · docstring 「판정이 거부로 끝났다면 그 사실 자체가 기록 대상」)가 `run()` 에서 **도달 불능**이 됐다. 가드가 같은 해석기를 먼저 불러 거부를 판정 불가로 닫으므로(D5 CLEAN: dispatch 0 · `10-read/lanes/shadow-ledger.json` 없음), 거부 사유는 예외 문언에만 남고 런 폴더에는 남지 않는다. 구 코드에서는 LanePending 회차에 한해 포인터가 `root_source: refused` 를 남겼다. 결함이 아니라 ⓦ 의 부수 효과이며, ⓦ 사후 확인에 병기할 사항(docstring 정정 또는 거부 기록 유지 여부).

관측(신규 아님): `tests/fixtures/read-failure-grid/__pycache__` 가 전체 pytest(plain) 중에 `PYTHONDONTWRITEBYTECODE=1` 을 뚫고 생성됨(백로그 ⑻ 재확인 · 삭제). D5 프로브의 `10-read/` 실재는 하네스 `write_lane_responses` 가 미리 만든 `10-read/lanes/` 이며 가드의 부작용이 아니다(run_source 직후 `10-read` 부재 실측 · Q1② 트리 스냅샷 불변).

**⑥ Q4 · Q5**

Q4 — 반경: 라운드 커밋 파일 4개 = 발주문 §1 그대로. `read.py` hunk 7개 = 센티널 상수 / 새 함수 3 / `run()` 가드+`load_yaml` 선행 / `terminated`·`awaiting` 초기화와 주석 / 조기 상신 `terminated=False`+`awaiting` / `finally` 주석+`awaiting=` 인자 / `_write_shadow_pointer` 키워드+조건부 필드 — 전부 v3 §1 ①②③ 대응. 값 공간 접촉 = `awaiting` 필드(조기 상신 포인터에만) · 조기 상신 append 제거, 둘뿐. `contracts tools runs reader tests/fixtures docs/decisions HANDOFF-NEXT.md ledgers` diff 빈 출력. ⑤ 는 구 blob 에서도 초록(엔진 무변경). 커밋 메시지에 시험 계수 없음. 기존 시험 기대값 변경 0(m22 봉투 4시험·m2 시험은 원장 행 수를 단언하지 않음 — 코드로 확인).

Q5 — §36 ↔ 실측: plain `835 passed in 149.45s` · `-O` `835 passed, 1 warning in 145.39s` · 관문 7종 두 모드 exit 0(FAILS=0) · `check_failure_table --self-test` exit 0 · 차별 대조 13/11 동일 · `+177/−9` · 11함수 15노드(ML-4 정정 마커와 일치) · m25 +36 · `__pycache__` 관측 동일. §37 ↔ `final.txt`: sha256 `1e0c13a2…06cbb` 일치 · 끝 개행 정규화 뒤 본문 동일. M1b 원문 3건(m2a2 · m2a2v2 · m2a2-audit) ↔ `FINAL`: 정규화 뒤 전부 동일(sha `8aa65073…` · `2f7d3588…` · `8fa71c32…`). §34 MJ-1~6 격(B1·H2·M2·L1) · §35 MK-1~5(H2·M2·L1) · §38 ML-1~4(M2·L2) ↔ 원문·DISPOSITIONS 행 일치. MJ-1 의 「수용」은 제안 처방(보충 재정)이 아니라 재량 경로였으나 §34 가 그 사실을 명시하고 MK 가 확인했으므로 기록 결함 아님. `SPEC.md` G-5 행 마커 「[집행 라운드 M2a-2 · 2026-09-05 · 재정 T38]」 ↔ 코드 실물 정합. HANDOFF 25차 좌표(drafts `AUDIT-ORDER-round-m2a2.md`·`.v1.md` · `fable-audit-runner.template.sh` · `fable-audit-brief-preamble.md` · 사본 · `pd-audit9-basetemp`) 실재. RULINGS-LEDGER T38 행 · `D-20260905-01` 등재 마커 실재. **ⓦ 판단**: fail-closed 는 T38 ③ 의 참 조건(세 근거 OR)을 바꾸지 않는다 — 읽을 수 있는 모든 상태의 분류는 그대로이고, 읽을 수 없는 상태에 「진행 대신 오류」를 더했을 뿐이며 값 공간(필드·스키마·실패표)도 무접촉이다. 재정 S2(`ruling-20260819-03-S1-S9.md` §2 S2 「공학 집행·기록·시험·오류 수정은 재량 + 사후 확인」)의 오류 처리 재량에 든다고 본다. 다만 Owner 가 ⓦ 를 볼 때 두 대가를 함께 봐야 한다 — 쓰다 만(0바이트) 포인터 하나가 사람이 치울 때까지 그 런을 막는다는 점(파일·사유는 문언에 실린다), 그리고 RJ-5 의 거부 기록 소실.

**⑦ [미검증]**

- D1~D5·D7 의 **개별** 전체 835 생존(개별은 대상 121건만 · D1~D6 결합본만 전체 835). D7 은 대상 121 + worktree 프로브만.
- §34·§35·§38 의 USAGE 토큰 수치·소요 시간(레인 STATUS 미대조).
- 레인 보고 §37 (ii) 표의 값은 인용하지 않았고 위 ③ 이 내 실출력이다.

Q1·Q2·Q3 의 필수 재현은 전부 실측했다.

**종료 조건**

```
HEAD=0189bdc180f7f1f7a7d8b758829c4a26c0ad1978 · git status --short = "?? .audit-sandbox"(1줄) · git diff --stat 빈 출력
read.py blob=88b4c9d(원복) · basetemp pd-audit9-basetemp 항목 0 · __pycache__ 0 · .pytest-basetemp 0 · /tmp 무접촉
생산 원장 sha e2350e0d…5df2 (사본·정본 · 시작=종료) · 정본 HEAD 0189bdc · 정본 status 빈 출력
```

판정 근거 요약: 재정 T38 ①②③ 은 코드에 정확히 옮겨졌고(Q1 전건 실측 · 발주 변조 7종+V6 전건 검출 · 차별 대조 13/11 재현), 실물 코드는 생산 배치 프로브에서도 옳게 동작한다. FAIL 은 구현 결함이 아니라 **RJ-1(MED · 발주자 귀책 · 시험 공백)** 하나 때문이며, 처방은 worktree·`shadow_root=None` 배치의 재호출 시험 1건이다.

VERDICT: FAIL
