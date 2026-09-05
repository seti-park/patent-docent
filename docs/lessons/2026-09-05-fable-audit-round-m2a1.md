# 독립 감사 원문 — 재감사 5(RI · 라운드 M2a-1 `0f00dc7` + 기록 `088f2fd`·`c7b97f1`) · **M9 = claude-fable-5-1 xhigh 첫 적용** · 판정 PASS

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`out.txt` = `jq -r .result raw.json` · sha256 `a489556ac0a91e81f08386e8c3703d0484015e88a4e866a740c1bf128d5cdd6b` · 9952 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/fable-audit-round-m2a1/`(`brief.md` = 안내문 + 발주문 · `raw.json` · `usage.json` · `stderr.log` · `status`).

**좌석 = `좌석 M9` · `claude-fable-5-1` xhigh · CLI `claude -p` · 도구 `Bash,Read` + allowlist(LANE-RUNTIME 「M9 감사 호출 꼴」) · `MEMORY_HOOKS=off` · `setsid nohup`** · 16:36:17 → 16:54:48(18.5분) · **54턴 · `end_turn` · 세션 한도 중단 없음(resume 불요)** · **USAGE = input 578 · cache_create 139,173(1h) · cache_read 1,582,118 · output 55,240(thinking 27,318) · `total_cost_usd` 5.95**. 사본 `~/projects/workspaces/pd-audit-round-m2a1`(detached `c7b97f1` · 마커 3검증) · basetemp 홈 fs `pd-audit8-basetemp`(감사자가 삭제) · 종료 조건 충족(status 1줄 · `__pycache__` 0). 발주문 = drafts `AUDIT-ORDER-round-m2a1.md`(M1b astra high 도전 MI-1·MI-2 반영판).

**판정 = PASS · BLOCKER/HIGH/MED 0 · LOW 3 · 필수 재현 [미검증] 0.** 감사자가 **직접** 재현한 것 = Q1 일곱 경로(9행 · 신·구 두 구현 · 원장Δ/포인터 신구 동일) · `_finish_lane_log` 실패 2꼴(MH-1 ⓐ 정합) · Q2 구현 변조 **13종**(발주 3 + 고안 10) · Q3 네 칸(구 `6 failed, 2 passed` · 사유 일치) · Q5 재현표 전 칸 · 원문 3건 바이트 · 레인 보고 sha256. **RI-1**(LOW · 발주자): 플래그를 게시 **앞**에 세우는 변조(V6)를 8시험이 못 잡음 — 게시 쓰기 일시 실패 창에서 `finally` 폴백이 사라지나 T3 목적은 불변 · **ⓓ1 꼴 시험 1건 추가 권고 → 라운드 M2a-2 발주문 ⑤ 에 편입**. **RI-2**(LOW · 총괄 기록): DISPOSITIONS MG-1 격 `HIGH` 는 원문·§28 의 **BLOCKER** 전사 오기 → 정정. **RI-3**(LOW · 총괄 기록): §32 「M1b 8런 누계 40」은 **37** 의 오기 → 정정 마커. 관측 = 관문 실행이 `tests/fixtures/read-failure-grid/__pycache__` 를 남김(`PYTHONDONTWRITEBYTECODE=1` 을 뚫음 · LANE-RUNTIME 함정 후보 · 백로그).

지적 열거 = RI-1, RI-2, RI-3

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§33**. **전부 수용**(RI-1 이월 · RI-2·RI-3 이 커밋에서 정정).

---

# 감사 원문 (claude-fable-5-1 xhigh · M9 첫 적용 · 이 아래는 감사자 저작)

**독립 감사 판정 — 재감사 5(RI) · 좌석 M9(claude-fable-5-1 xhigh) · 대상 `0f00dc7` + 기록 `088f2fd`·`c7b97f1`**

**① preflight**

```
.audit-sandbox: path=/home/laptop/projects/workspaces/pd-audit-round-m2a1 · pin=c7b97f15a5672b1f990628df0c30c5599309ea11 · order=AUDIT-round-m2a1-20260905 · disposable=true
git rev-parse HEAD = c7b97f15a5672b1f990628df0c30c5599309ea11 (detached · branch 출력 없음)
git status --short = "?? .audit-sandbox" 한 줄
정본 /home/laptop/projects/patent-docent HEAD = c7b97f1 (읽기만 · 감사 중 변동 없음)
```

**② Q1 — 재정 T3 문언 이행 · 경로별 재현표**

ⓐ 순서 실재: `read.py:1884` `_finish_lane_log(paths, journal)` → `:1885` `lane_log_published = True` → `:1886` `recorded = _load_recorded_lane_log(paths)` → `:1890`·`:1892` 두 검사 모두 `recorded` 수신. `journal` 은 1870행 이후 게시(`:1884`)와 `finally`(`:1975`)에만 나타나고 `record*` 호출 0건. 두 검사 함수는 `journal.rows` 만 읽는다(코드 확인).
ⓑ 검사 하나 유지: diff 에 `check_id`·`READ_CHECK_IDS` 변경 없음 · `contracts/`·`reader/`·`lib` 무접촉 · 새 판정 행 없음. `_load_recorded_lane_log` 는 판정 행이 아니라 `StageError` 를 내는 적재기(MH-4 주문)로, 기각안 ⓑ(별도 재검 배선)가 아니다.
ⓒ 일곱 경로 — 전부 **내가 직접 실행**(프로브 스크립트 · `test_m2_read` 하네스 · `write_json` 감쌈 · 신·구 두 구현에 같은 프로브). 표의 「원장Δ/포인터」는 신·구 **동일**했다(9경로 전건).

| 경로 | 재현 방법 | 결과(신) | lane-log 쓰기 횟수(신) | 디스크 최종 내용(신) | 원장Δ / 포인터 terminated |
|---|---|---|---|---|---|
| ⑴a ⑨ 전 예외 | id-map 쓰기에 예외 주입 | `BeforeExit` 전파 | 1(`finally`) | = 메모리 저널 | 1 / true (구와 동일) |
| ⑴b `LaneAssignmentError` | `model_override` haiku-imposter | `LaneAssignmentError` 전파 | 1(`finally`) | = 메모리 저널 | 1 / true (동일) |
| ⑵ `LanePending` | 접지 `response.json` 삭제 후 재생 어댑터 | `LanePending` 2건 전파 | 1(`finally`) | = 메모리 저널 | 0 / false (동일) |
| ⑶ 접지 게이트 미진입 조기 반환 | read-b `element_two` 변형(m2 시험 ① 배치) | `escalate` · `phase_gate.entered=false` · 접지 발송 0 | 1(`finally`) | = 메모리 저널 | 1 / true (동일) |
| ⑷ 게시 뒤 검사 실패 | 첫 게시 직후 디스크 `request_digest`→`f×64` | `escalate` | 1(⑨) | = **변조본**(위조 지문 실재) | 1 / true (동일) |
| ⑸ 게시 뒤 재독 `StageError` | 첫 게시 직후 파일을 `null` 로 | `StageError` 전파 | 1(⑨) | 파일 내용 `null` 그대로 | 1 / true (동일) |
| ⑹a 게시 뒤 일반 예외 | `_validate_convergence` 에 `RuntimeError` 주입 + 디스크 표식 | `RuntimeError` 전파 | 1(⑨) | = 변조본(표식 보존) | 1 / true (동일) |
| ⑹b 게시 뒤 산출물 쓰기 실패 | `convergence.json` 쓰기에 `OSError` 주입 + 표식 | `OSError` 전파 | 1(⑨) | = 변조본(표식 보존) | 1 / true (동일) |
| ⑺ 정상 | 무변조 | `ok` | 1(⑨) | = 메모리 저널 | 1 / true (동일) |

구 구현(`f3bd05b`)은 ⑷·⑸ 에서 `status=ok` 로 통과했고(변조 미탐지) ⑹a·⑹b 에서 `finally` 가 썼다 — 차별의 실물.

ⓓ `_finish_lane_log` 자체 실패: 첫 lane-log 쓰기만 `OSError` → 시도 2 · 성공 1 · `finally` 가 메모리 저널을 기록 · 원장 1행·포인터 기록 · 원 `OSError` 전파. 전부 `OSError` → 시도 2 · 파일 부재 · `finally` 의 재시도 예외가 원장·포인터 기입을 건너뜀(구 구현도 같은 구조). MH-1 ⓐ 「try 진입 뒤 기록 가능한 경로에 한한다」와 **정합**.

**③ Q2 — 새 시험의 실질 · 구현 변조표**(전건 내가 직접 가하고 `git checkout --` 원복 · 각 변조 뒤 blob `d5d70eb` 복귀 확인)

| 변조 | 결과 | 붉은 시험 |
|---|---|---|
| (ii)-1 값 검사 인자 → 메모리 `journal` | `1 failed, 7 passed` | ⓐ digest_mutation |
| (ii)-2 형태 검사 인자 → 메모리 `journal` | `1 failed, 7 passed` | ⓑ read_run_mutation |
| (ii)-3 플래그 제거 → `finally` 항상 재덮기 | `7 failed, 1 passed` | ⓐ ⓑ ⓒ3×4 ⓓ (ⓒ1 만 초록) |
| V1 재독을 `journal` 로 대체(게시 유지) | `6 failed, 2 passed` | ⓐ ⓑ ⓒ3×4 |
| V2 행 단위 `isinstance(dict)` 제거 | `1 failed` | ⓒ3[non-dict-row] |
| V3 최상위 `isinstance(list)` 제거 | `1 failed` | ⓒ3[null] |
| V4 재독 결함 → 빈 `LaneJournal` 반환 | `4 failed` | ⓒ3×4 |
| V5 게시를 검사 뒤로 이동 | `6 failed, 2 passed` | ⓐ ⓑ ⓒ3×4 |
| **V6 플래그를 게시 앞에 세움** | **`8 passed`** | **없음 → RI-1** |
| V7 `finally` 조건 반전 | `8 failed` | 전건 |
| V8 부재 시 `finally` 자동 복원 | `1 failed` | ⓒ3[deleted] |
| V9 재독 `StageError` 삼키고 메모리 폴백 | `4 failed` | ⓒ3×4 |
| V10 검사 통과 뒤 ⑩ 직전 재게시 | `1 failed` | ⓓ normal_completion |

훅 `_install_lane_log_mutation`: `payload` 참조만 저장하고 `mutate` 는 `load_json(path)` 로 새 객체를 고친다 — 메모리 rows 무접촉(코드 확인 · ⓐ 시험이 사후에 `memory_rows == original_rows` 단언). ⓐ 접지 행 실물: `RequestWritingReplayAdapter` 가 `FileLaneAdapter.write_request` 로 `read-a/ground-independent/batch-0/request.md` 를 실제로 썼고, 독립 `sha256sum` = `ce7c4db7…0259` = 로그의 `request_digest`.

**④ Q3 — 차별 대조 (i)**: `git show f3bd05b:engine/stages/read.py` 를 덮어(blob `bff4f34` 확인) 새 시험 8건 실행 → **`6 failed, 2 passed`** · 붉은 사유 = ⓐ `값 검사가 잡지 못했다: pass, []` · ⓑ `형태 검사가 잡지 못했다: pass, set()` · ⓒ3 4건 모두 `DID NOT RAISE StageError` · 초록 = ⓒ1 · ⓓ. 원복 뒤 `git diff --stat` 빈 출력 · blob `d5d70eb`. 네 칸 전부 발주문 기대와 일치.

**⑤ 신규 지적**(BLOCKER/HIGH/MED **0** · LOW 3)

- **RI-1 · LOW · 귀책 발주자** — 좌표 `read.py:1884~1885`. 플래그를 게시 **앞**으로 옮기는 변조(V6)를 8시험이 잡지 못한다(`8 passed`). 영향은 게시 쓰기가 일시 실패하는 좁은 창에서 `finally` 폴백이 사라지는 것뿐이며 T3 의 목적(사후 변조 탐지 · 검사본 보존)은 깨지지 않는다. 발주문 ③ 시험 목록이 게시 자체의 실패 경로를 들지 않았다. 후속 라운드에서 ⓓ1 꼴 시험 1건 추가를 권고.
- **RI-2 · LOW · 귀책 총괄 기록** — `docs/decisions/DISPOSITIONS.md:287` MG-1 격 `HIGH`. 원문 `pd-lanes/astra-m1b-m2a1/FINAL:35` 와 `D-04` §28 은 **BLOCKER**. 어휘표에 `BLOCKER` 가 있으므로 관문이 못 잡는 전사 오류. 도입 커밋 `cd63ace`(대상 밖 상류)이나 `c7b97f1` 의 살아 있는 상태다. 오류 수정 재량.
- **RI-3 · LOW · 귀책 총괄 기록** — `D-04` §32 「M1b 8런 누계 = 지적 40(MB7 MC6 MD6 ME1 MF4 MG6 MH5 MI2)」. 괄호 합은 **37** 이고 DISPOSITIONS 행 실측도 MB7·MC6·MD6·ME1·MF4·MG6·MH5·MI2 = 37.

**⑥ Q4·Q5**

Q4: `diff-tree` = `docs/SPEC.md` · `engine/stages/read.py` · `tests/test_m25_lane_log_disk_record.py` 세 파일. `read.py` hunk 4개 = 플래그 초기화(②) · ⑨ 블록(①) · `finally` 조건(②) · `_load_recorded_lane_log`(① MH-4) — 대응 없는 hunk 없음. `contracts tools runs reader tests/fixtures docs/decisions HANDOFF-NEXT.md` diff 빈 출력. `append_screening_ledger`·`_write_shadow_pointer`·`terminated` 는 diff 에 문맥 줄로만 등장. 커밋 메시지에 시험 계수 없음(「재독 결함 4종」은 손상 종류 수이며 시험 수가 아니다 — 위반 아님으로 판단 · 기록만).

Q5: §30 재현표 ↔ 내 실측 — plain `819 passed in 139.57s` · `-O` `819 passed, 1 warning in 139.82s` · 수집 819 = 811 + 8 · 관문 7종 두 모드 `FAILS=0` · `--self-test mutations=36 rejected=36` exit 0 · 구 `6 failed, 2 passed` · `read.py` numstat +60/−4 · `5f4afe9`↔`f3bd05b` 의 `read.py` blob 동일 `bff4f34` — 전 칸 일치. §31 ↔ `final.txt`: sha256 `85edec1d…9549` · 앞뒤 개행 정규화 뒤 동일. M1b 원문 3건(`m2a1`·`m2a1v2`·`m2a1-audit`) ↔ 각 `FINAL`: 제목 줄 뒤 구분 개행 1개를 빼면 바이트 동일. §28 MG(BLOCKER1·HIGH3·MED1·LOW1) · §29 MH(HIGH2·MED2·LOW1) · §32 MI(MED2) · 전부 수용 — FINAL 과 일치(DISPOSITIONS 격 1건만 RI-2). `SPEC.md` B-1 마커 문언 = 코드 실물. HANDOFF 23차 좌표(`ruling-20260905-03-T38.md` · drafts `AUDIT-ORDER-round-m2a1.md`·`fable-audit-runner.template.sh`·`SPEC-round-m2a2.md` · LANE-RUNTIME:291 「M9 감사 호출 꼴」) 전부 실재. `check_dispositions` plain·`-O` 모두 `RESULT: PASS` exit 0. MI-1·MI-2 정정은 내가 받은 발주문에 반영돼 있었다.

**⑦ [미검증]** — §30 의 병합 절차(worktree cwd 사고·회복)와 레인 실행 환경(`.pytest-basetemp` 삭제 등)은 사본에서 재현할 수 없어 **최종 상태만** 확인했다. §30·§31 의 소요 시간 수치는 대조 대상이 아니다. 필수 재현(Q1 경로 · Q2 변조표 · Q3 네 칸)에 미검증 항목은 없다.

**관측(지적 아님)**: 관문 실행이 `tests/fixtures/read-failure-grid/__pycache__` 를 남겼다(gitignore 대상 · `PYTHONDONTWRITEBYTECODE=1` 을 뚫음 · 삭제함 · LANE-RUNTIME 함정 후보). `/tmp` 에는 러너 자신의 `claude-1000` 외 새 항목 없음.

**원상 복구·종료 조건 실출력**

```
임시 변조 전건 git checkout -- 원복 · read.py blob = d5d70eb02cf498ae4046ab4da5f7f506146b9a91
basetemp /home/laptop/projects/workspaces/pd-audit8-basetemp 삭제 → exists = False
HEAD = c7b97f15a5672b1f990628df0c30c5599309ea11
git status --short = "?? .audit-sandbox" (1줄)
__pycache__ = 0 · *.pyc = 0
```

VERDICT: PASS
