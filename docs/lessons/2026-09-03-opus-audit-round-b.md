# 독립 감수 원문 — 라운드 B 합본(A′ `99fad78` · C′ `867b95b` · B-0 `6f93519` · 골든 `47e437c` · B `1d29c8b`) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(감사 stdout 전문 · `opus-audit-round-b/out.txt` 의 sha256 `c79dfc7eb49a9dd7318240f54438ab3da581c283e2d763e3d824dc51c1820275` 와 `---` 아래가 동일 · 40,859 B).

**좌석 = opus max**(ROUTING M9 교차 벤더 — 다섯 커밋의 저작이 전부 sol-coder(GPT-5.6 Sol high)). CLI 직구동 `claude -p --model claude-opus-5 --effort max`(환경변수 `CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000` · `MEMORY_HOOKS=off` 실측 확인) · `setsid` 배경 + `EXIT=` 마커 · 03:46 → 04:25(약 40분) · EXIT=0 · stderr 0 B. 발주문 = `AUDIT-ORDER-round-b.md`(여덟 질문 · 지적 ID `RB-*`). 사본 = `audit-round-b`(`git clone --no-hardlinks` · detached `94ca66f` · `.audit-sandbox` 마커 3검증 전건 일치 — 감사자 실출력 §1) · 감사 뒤 사본 worktree 1(자신) · `/tmp` 잔재 0.

**정본 무접촉 확인** — 감사 전후 `git status --porcelain` 0행. 감사 도중 총괄이 정본에 커밋 1개(`9143acb` · HANDOFF 추기 · 이 세션)를 얹어 트리 지문이 `de4e54c9…` → `bae1192d…` 로 바뀌었고, **감사자가 그것을 정확히 짚어 「지문이 아니라 status 0행 + 커밋 저자로 판정해야 한다」고 적었다**(§1). 발주문의 「전후 트리 지문 대조」 문언은 감사 중 총괄 커밋을 배제하지 않은 발주자 오류다 — 다음 감사 발주문은 「감사 중 정본 커밋 금지 또는 저자 대조」로 적는다.

**판정 = FAIL · 지적 6건(HIGH 1 · MED 2 · LOW 3) · 새 재정 사항 0.** 값·집행은 전건 closed — 재정 조건 T26 ⒜①②③·§3①~⑤ · T28 ①~④ · T29 ①~③ · T30 ①~④ · T24/T25 계승 전건 closed(⒜③ ⒝ 만 partially → RB-1) · 명령되지 않은 hunk 0 · 골든 8,190칸 `99fad78` 재생성 바이트 동일 · 결함 심기 ⓐ~ⓛ + 추가 20종 전건 검출(미검출 6종은 관문 밖 층이 든다) · A′·C′ 처분표 전건 이행 · provenance 우회 6종 전건 방어. **RB-1**(HIGH · 설계 귀책): 출구 재시도 8종이 계약·엔진 상수·관문 상수 세 사본에만 결박 — 셋을 함께 고치는 정합 편집(8행 `points` → `[early]` + 두 상수 축소)이 관문 7종·`--self-test`·pytest 761 을 전부 통과하며 출구 청구항 재시도를 1회 → 0회로 지운다. **RB-2**(MED · 발주자 귀책): B-0 시험 86건의 clone 원천이 정본 main 리터럴 — 작업 트리의 엔진 변조(골든 1,020칸 어긋남)에도 86 passed. **RB-3**(MED · 설계 귀책): 설계 v18 T-4 행 「verbatim 을 빼면 T-2 가 떨어진다」가 거짓(T-2 가 지키는 것은 pointer-resolve). **RB-4**(LOW · 총괄): D-03 「발주자 오류 0건」 사실 아님. **RB-5**(LOW): CLAUDE.md §6 일곱째 행에 「주장하지 않는 것」 부재. **RB-6**(LOW · B-0 레인): 생성기 자기 검증의 `check_ids.expected_set` 항진식. [미검증] 7항(§7) 중 ②(`check_ids` 순서 동반 치환)는 B′ 가 T-7 순서 단언으로 닫고, ⑦(-O pytest)은 총괄 재현이 이미 덮었다.

지적 열거 = RB-1, RB-2, RB-3, RB-4, RB-5, RB-6

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-03-round-b.md` **§6** 에 있다. **전부 수용** → 라운드 **B′**(sol-coder · 시험·문서 수리 · 값 공간 무변경) + 설계 v19 부록(RB-3 정정 · 리포 밖).

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

# 좌석 M9 적대 감사 보고 — 라운드 B 합본 (`1d29c8b` + `47e437c` + `6f93519` + `99fad78` + `867b95b`)

## 1. preflight 실출력

```
=== marker exists ===              YES
=== marker content ===
path=/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-b
pin=94ca66f14efa8f1bce0ab6a16cea76dab90dbd2d
order=AUDIT-round-b-20260903
disposable=true
=== realpath . ===                 /tmp/.../scratchpad/audit-round-b      ← path= 와 일치
=== git rev-parse HEAD ===         94ca66f14efa8f1bce0ab6a16cea76dab90dbd2d  ← pin= 과 일치
=== git status --porcelain ===     ?? .audit-sandbox
```
마커 3검증 전건 일치. 감사 종료 시점 사본도 `?? .audit-sandbox` 한 줄 · HEAD `94ca66f` · worktree 1개(사본 자신).

**정본 리포 — 읽기만 준수. 다만 총괄 세션이 감사 중 커밋을 하나 얹었으니 지문 대조 전에 읽어라.**

| 시점 | `git status --porcelain` 행 수 | HEAD | 트리 지문 |
|---|---:|---|---|
| 감사 개시 | **0** | `94ca66f` | `de4e54c9…`(발주문 값과 일치) |
| 감사 종료 | **0** | **`9143acb`** | **`bae1192d…`** |

차이의 원인은 내가 아니라 **총괄 세션 자신**이다 — `9143acb`(2026-09-03 03:47:02 · author `seti-park` · `Co-Authored-By: Claude Fable 5.1` · `Claude-Session: session_011sBzix…` = 이 감사를 발주한 세션) · `HANDOFF-NEXT.md` 1파일 2행 추가(「opus max 감사 발주 좌표」). `94ca66f` 는 여전히 HEAD 의 조상이다. 내가 정본에 건 명령은 `git rev-parse`·`git status`·`git log`·`git show`(읽기), `.venv/bin/python` 실행, 그리고 `tests/test_m24a_…` 가 스스로 도는 `git clone --no-hardlinks`(읽기) 뿐이다. **발주문의 「전후 트리 지문 대조」를 그대로 적용하면 위반이 아닌 것을 위반으로 읽는다** — 판정 근거는 지문이 아니라 `status` 0행 + 커밋 저자여야 한다.

기준선(사본): pytest **761 passed** · 관문 7종 × plain/`-O` 전부 exit 0 · `--self-test` **mutations=36 rejected=36**(두 모드).

---

## 2. Q1 — 재정 집행 조건 판정표

재현 명령의 마지막 출력 줄을 그대로 인용한다. 관문 = `python tools/check_failure_table.py`(마지막 두 줄 `failure_rows=11 early_retry=3 exit_retry=8` / `EXIT=0`).

### T26 (`ruling-20260902-01-T24-T27.md`)

| 조건 | 판정 | 좌표 | 재현 마지막 줄 |
|---|---|---|---|
| ⒜① 행에 검사 id 키 · 코드는 키로 찾는다 | **closed** | `read.yaml:710-782`(11행) · `__init__.py:142 failure_rows_for_checks` · `read.py` 에 `failure_entry(` 0회 | `failure_rows=11 early_retry=3 exit_retry=8` |
| ⒜② 순서는 조치 격자 + 계약 순서 | **closed** | `__init__.py:103 worst_status` · `:194 select_failure_row` | 골든 8,190/8,190 일치. 반증: `for row in rows` → `reversed(rows)` 로 뒤집으면 `MISMATCH_CELLS=1020/8190` |
| ⒜③ ⒜ 선언 우주 ↔ `checks` 합집합 차집합 **양쪽 0** | **closed** | 관문 G2 `:179-199` | 독립 재실측 `T26 declared_only=[] failure_only=[]` |
| ⒜③ ⒝ 판정점 목록 ↔ `retry(n)` 행 집합 **정확히 같다** | **partially-closed** | 관문 G3 `:201-239` | `early: list-union=([],[]) list-approved=([],[]) n=3` / `exit: … n=8` — **등식은 참이나 「8」이라는 값 자체가 상호 대조되는 사본 셋에만 결박된다 → RB-1** |
| §3 ① M1b PASS 전 착수·커밋 금지 | **closed** | `eb76f9d` 01:49(v18 PASS 반입) < `1d29c8b` 03:40 | `# 독립 감수 원문 … 판정 PASS` / `VERDICT: PASS` |
| §3 ② 오늘의 판정표 불변 증명 | **closed** | 골든 재생성 실측 | `normalized-identical: True \| lenA 260036 lenB 260036` |
| §3 ③ 양방향 관문 exit 0 + 세 결함 심어 exit 1 | **closed** | self-test 01·02(행 없는 검사/검사 없는 행) · 03·04·21(재시도 불일치) | `SELF-TEST mutations=36 rejected=36` |
| §3 ④ 관문 계수 정정 마커 | **closed** | `CLAUDE.md:114` · `IMPLEMENTATION-HISTORY.md` 「4→5→6→7」 · `SPEC §8.3 7항` | `RESULT: PASS`(`check_spec_refs`) |
| §3 ⑤ 전수 시험 + 관문 전종 2모드 | **closed** | — | `761 passed in 156.78s` · 7종×2 exit 0 |

### T28 · T29 · T30 (`ruling-20260902-02-T28-T32.md` §3)

| 조건 | 판정 | 재현 마지막 줄 / 근거 |
|---|---|---|
| **T28 ①** 8,190칸 한 칸도 안 바뀜 | **closed** | 내가 `99fad78` worktree 에서 재생성 → `cells`·`expected_counts`·`exceptions[0]` **전건 SAME**. `expected_counts = {"halt/null":6144,"escalate/null":1023,"escalate/국면 간 변이 재현 — 코드 결함 의심":1020,"StageError":3,"total":8190}` |
| **T28 ②** 예외 표기 1건 + 도달 불능 표지 · 시험이 읽는다 | **closed** | `exceptions[0].cell_count=2048` · T-7 이 `manifest["check_ids"].index("read.convergence")` 로 **고정 식** 독립 산출(manifest predicate 를 eval 하지 않는다 — Z-2 닫힘) |
| **T28 ③** 무재디스패치 시험 + 양성 대조군 | **closed** | `test_t28_…` green · 주입 제거 시 `1 failed`(양성 대조 성립). **단 양성 대조군 T-2 의 실제 보호 범위가 설계 진술과 다름 → RB-3** |
| **T28 ④** 계약 목록에서 convergence 제외 · 행 `points:[early]` · 관문 대조 | **closed** | 심기 x15 → `G3: exit 승인 집합 차집합: 승인에만=[], 계약에만=['read.convergence']` · x16 → `G1: 5행 기계 필드 …` |
| **T29 ①** 골든 12 id 정확 · 파일이 들고 시험이 상수와 차집합 0 | **closed** | `T29 exit universe == engine 12: True` · 검증기 `check_ids.expected_set`(len==12 + 집합 상등) |
| **T29 ②** 진입 반증 · `_failure_verdict` 호출 0회 | **closed** | `test_read_input_digest_halt_stays_on_the_entry_exception_path` — 실러너 경로 · 계수기. 반증: 진입 예외를 fail 행으로 강등 → `1 failed` |
| **T29 ③** 3행 `checks/halt/judged_at:entry` · 출구 목록 밖 · 관문 대조 | **closed** | `entry_only=[]` · 심기 e1/e2/13/14/15/16/33 전건 exit 1 |
| **T30 ①** kind 사전 3종 각 1행 | **closed** | `T30 kinds=['retry-repeat','gate-escalation','upstream-defect'] unique=True rows=11` |
| **T30 ②** `checks` xor `kind` | **closed** | `xor_ok=True` · 심기 j1 → `G1: 2행은 checks xor kind가 아니다` |
| **T30 ③** `upstream-defect` 키만 · 엔진 호출자 0 · `deferred/test_bound` | **closed** | `grep -rn 'failure_row_of_kind(.*upstream-defect' engine/ \| wc -l` → `0` · `failure_binding_status.deferred` 1행 |
| **T30 ④** SPEC 한 줄 + 재정 좌표 | **closed** | SPEC §1.16 3-c/3-d + 표 아래 문단 · `RESULT: PASS` |

### T24 · T25 (A′ 소관 · 라운드 B 가 계승)

| 조건 | 판정 | 근거 |
|---|---|---|
| T24 ① 출구 재독 반증 + 무변조 시 다른 검사 불변 | **closed** | `test_t24_tail_time_source_mutation_halts_without_retry` + 대조군 |
| T24 ② 재독은 출구에만(조기는 메모리 사본) | **closed** | `test_t24_decompose_time_mutation_does_not_change_early_verdict` — 청구항 본문 앵커 변조 + **양성 대조**(`run_early_claim_checks` 가 변조본에서 실제 fail) → A-1 재발 없음 |
| T24 ③ `reader/lib` 무변경 | **closed** | `git diff --stat f46698e 99fad78 -- reader/` = 0행 |
| T24 ④ 진단 3항 | **closed** | `{check_id, path, declared, actual}` 정확 일치 대조 |
| T25 ① halt 행 실패 시 재시도 0 | **closed** | 라운드 B 가 `_halts_immediately`(any) → `_exit_retry_eligible`(부분집합)로 **강화**. 반증: `return True` → `3 failed` |
| T25 ② 비-halt 재시도 존치 | **closed** | T-2 `/retry-1/` 정확히 3레인 |

**범위 밖 확인** — T31(`engine/render/` diff 0행) · T32(`contracts/schemas/`·`reader/schemas/` diff 0행)는 이 다섯 커밋에서 손대지 않았다. 재정 문언대로다.

---

## 3. Q3 — 결함 심기 표 (관문 `check_failure_table.py`)

발주문 지정 ⓐ~ⓛ **전건 검출**. 감사자 추가 20종 중 6종 미검출이며 그 성질을 각 행에 적었다.

| # | 심은 결함 | plain | `-O` | 검출 | 첫 오류 줄 |
|---|---|---:|---:|---|---|
| ⓐ1 | 행 순서 교환 4↔5 (동률 해소 순서) | 1 | 1 | ✅ | `G1: 4행 기계 필드 기대=…` |
| ⓐ2 | 행 순서 교환 6↔7 (**판정 무영향**) | 1 | 1 | ✅ | `G1: 6행 기계 필드 …` |
| ⓐ3 | 행 순서 교환 1↔2 (halt↔halt) | 1 | 1 | ✅ | `G1: 1행 기계 필드 …` |
| ⓑ | lane-log 두 행 병합 | 1 | 1 | ✅ | `G1: failure 행 수 기대 11, 실제 10` |
| ⓒ | `read.coverage` 분리(같은 action) | 1 | 1 | ✅ | `G1: … 실제 12` |
| ⓓ | 동시 일관 변조(bibliography) | 1 | 1 | ✅ | `G1: … 실제 12` |
| ⓔ1/ⓔ2 | `judged_at: entry` 를 convergence/source-digest 행에 | 1 | 1 | ✅ | `G1: 5행/2행 기계 필드 …` |
| ⓕ1 | `then` 없는 `retry(1)` | 1 | 1 | ✅ | `G1: 1행 기계 필드 …` |
| ⓕ2 | `then: retry(1)` | 1 | 1 | ✅ | 〃 |
| ⓕ3/ⓕ4 | 비-retry 행(kind/checks)에 `then` | 1 | 1 | ✅ | `G1: 10행/2행 …` |
| ⓖ1 | 미지 action `quarantine` | 1 | 1 | ✅ | `G1: 2행 …` |
| ⓖ2 | 미지 kind `downstream-defect` | 1 | 1 | ✅ | `G1: 11행 …` |
| ⓖ3 | 사전 밖 phase `mid` | 1 | 1 | ✅ | `G4: checks_before_exit[1] phases 위반: ['exit','mid']` |
| ⓖ4 | 미지 `then` 어휘 | 1 | 1 | ✅ | `G1: 1행 …` |
| ⓗ1~ⓗ5 | `condition`/`note` 빈문자열·int·list·null | 1 | 1 | ✅ | `G1: n행 condition/note가 비공 str이 아니다` |
| ⓘ1 | `max_retries: true`(yaml bool) | 1 | 1 | ✅ | `G3: exit.max_retries 타입이 int가 아니다: bool` |
| ⓘ2/ⓘ3 | `1.0` / `"1"` | 1 | 1 | ✅ | `… float` / `… str` |
| ⓙ1 | `checks` → `check`(단수 키) | 1 | 1 | ✅ | `G1: 2행은 checks xor kind가 아니다` |
| ⓙ2 | `checks` → `check_ids` | 1 | 1 | ✅ | `G1: 6행은 checks xor kind가 아니다` |
| ⓚ1 | 12행(유령 검사 id) | 1 | 1 | ✅ | `G1: … 실제 12` |
| ⓚ2 | 10행(행 삭제) | 1 | 1 | ✅ | `G1: … 실제 10` |
| ⓚ3 | 12행(승인 행 복제) | 1 | 1 | ✅ | 〃 |
| ⓛ | `-O` 전용 차이 | — | — | ✅ | **없음** — 정본·실패 프로브 양쪽에서 stdout **바이트 동일**, 종료 코드 동일 |
| x1 | 행 안 `checks` 순서 치환 | 1 | 1 | ✅ | `G1: 8행 기계 필드 …`(엔진은 집합으로 읽으니 관문이 **더 엄격** — 무해) |
| x2 | 행 `points` 순서 치환 | 1 | 1 | ✅ | 〃 |
| x6 | `reason_label` 문안 변경 | 1 | 1 | ✅ | `G1: 10행 기계 필드 …` |
| x10 | `retry(01)` 제로패딩 | 1 | 1 | ✅ | `G1: 1행 …` |
| x11 | `retry(2)` + `max_retries: 2` 동시 | 1 | 1 | ✅ | `G1: 1행 …`(승인 상수가 먼저 잡는다) |
| x12 | `checks_before_exit` id 중복 | 1 | 1 | ✅ | `G2: checks_before_exit id가 중복됐다` |
| x13 | `checks_on_entry` 에 유령 id | 1 | 1 | ✅ | `G2: 선언↔failure 차집합: 선언에만=['read.__ghost_entry__']` |
| x14 | `judged_here` 에서 convergence 제거 | 1 | 1 | ✅ | `G2: 조기 선언 세 벌 불일치` |
| x15 | 출구 목록에 convergence 복귀(T28 되돌리기) | 1 | 1 | ✅ | `G3: exit 승인 집합 차집합: … 계약에만=['read.convergence']` |
| x16 | convergence 행 `points:[early,exit]` | 1 | 1 | ✅ | `G1: 5행 …` |
| x17 | 검사 id 를 두 행에 중복 | 1 | 1 | ✅ | `G1: 6행 …` |
| x18 | `failure:` 키 통째 삭제 | 1 | 1 | ✅ | `G1: failure가 list가 아니다` |
| x19 | `checks: []` | 1 | 1 | ✅ | `G1: 2행 checks가 비공 문자열 고유 list가 아니다` |
| x20 | `checks` 원소 중복 | 1 | 1 | ✅ | `G1: 8행 …` |
| **x3** | `points[exit].checks` 순서 뒤집기 | 0 | 0 | ➖ | **값이 아니다** — 러너는 `set(checks)` 로 읽는다. 정상 |
| **x4/x5** | `condition`/`note` 임의 재작성 | 0 | 0 | ➖ | `prose_only` 선언 · `read.py` 에 needle 조회 0(`freeze/source` 는 자기 계약을 읽는다). 정상 |
| **x7** | `points[]` 행에 미승인 키 추가 | 0 | 0 | ➖ | 관문 밖이나 **시험 결속**(`test_m21:...:984` `verify("retry_budget.points[]", …)`) |
| **x8** | `points[early].scope` 뒤집기 | 0 | 0 | ➖ | `test_bound` 선언대로 시험이 잡는다(`test_m21:237` · `test_m17:222`) |
| **x9** | `failure_binding_status.runner_reads` 비우기 | 0 | 0 | ➖ | `test_m24…::test_failure_binding_status_classifies_exactly_the_used_keys` 가 잡는다 |

**⑴ `--self-test` 36종 ↔ 설계 §2.7 ⑴~㊱ — 일대일 완전 대응.** 36 라벨을 설계 열거와 손으로 맞췄고 대체·누락·합침이 없다(⑴=`01 missing declared check` … ㊱=`36 integer note`). ㉚은 파이썬 `True` 를 `yaml.safe_dump` → `max_retries: true` 로 내려 파서가 bool 로 되읽는 실물 경로를 탄다(실측: `safe_dump(True) -> 'max_retries: true'` · `reload type -> bool`). **빠진 결함 클래스는 관문의 여섯 주장 안에서는 발견하지 못했다** — 미검출 6종은 전부 다른 층이 든다.

**⑵⑶ 우회 경로 — 뚫린다. 이것이 RB-1 이다.** 관문 상수 + 계약 + 엔진 상수를 **함께** 고치는 정합 편집이 통과한다. 두 형태를 실측했다.

| 우회 형태 | 관문 7종×2 | `--self-test` | pytest 761 | 판정 |
|---|---|---|---|---|
| `read.bibliography` 를 9행에서 떼어 12행 신설 + 상수 둘 축소 | exit 0(`exit_retry=7`) | 36/36 | **1 failed** | 막힌다 — `test_approved_failure_skeleton_matches_contract_exactly` 의 `len(rows) != 11` **리터럴**이 유일한 방벽 |
| 8행(`claim-inventory`·`dependency-parse`) `points: [early, exit]` → `[early]` + 상수 둘 축소 (**11행 유지**) | **exit 0**(`exit_retry=6`) | **36/36** | **761 passed** | **뚫린다** |

두 번째 편집 아래 `_exit_retry_eligible({read.claim-inventory}) = False`(기준선 `True`) — 출구 청구항 실패가 재시도 1회 없이 즉시 상신된다. 골든 8,190칸은 (조치, 라벨)만 고정하므로 **구조상 재디스패치 횟수에 눈이 없다**.

**⑷ 규율 실측** — `grep -c assert tools/check_failure_table.py` = **0** · 종료 코드 `ok 0 / 검증 실패 1 / 파일 없음 2 / 최상위 list 2 / 파싱 실패 2 / 잘못된 인자 2 / --help 0` · `--self-test` 전후 `contracts/stages/read.yaml` sha256 **불변**(메모리 `deepcopy` 변조) · importlib 적재 시 끌려 들어오는 `engine`/`reader` 모듈 **0개** · `if __name__ == "__main__":` 가드 `:429` 존재.

---

## 4. Q4 — 판별력 표 (시험 × 변조)

| 시험 | 심은 변조 | 결과 | 비고 |
|---|---|---|---|
| **T-1** `test_t28_exit_convergence_failure_does_not_redispatch` | 주입(`monkeypatch.setattr(read_stage,"run_read_checks",wrapper)`) 제거 | 🔴 `1 failed` | 양성 대조 성립. 패치 대상이 **실제 출구 호출점**(`read.py:1826`)이 읽는 모듈 전역임을 확인 — 조기 게이트는 `run_early_claim_checks`(`:1593`)라 오염되지 않는다. wrapper 는 `peer_spec` 사본에 독립항을 복제하고 `return original(modified)` — finding 을 손으로 더하지 않는다. 판정서에 `independent-count: fail`, 나머지 exact-match 축 `pass` 기록 검사까지 든다 |
| T-1 | `_exit_retry_eligible` → `return True` | 🔴 `3 failed` | T28 β 되돌리기 검출 |
| T-1 | `<=` → `&`(양화사 약화) | 🟢 통과 / T-4 🔴 | 잡는 것은 T-4 |
| **T-2** `test_v2_exit_retry_repairs_phase_drift` | `read.verbatim` 정합 제거 | 🟢 **통과** | **설계 진술이 거짓 → RB-3.** 계측 실측 `EXIT_FAILING_SETS: [['read.pointer-resolve']]` — T-2 가 지키는 것은 `read.pointer-resolve` 하나다 |
| **T-3** `test_read_input_digest_halt_stays_on_the_entry_exception_path` | 진입 예외를 fail 행으로 강등 | 🔴 `1 failed` | 실러너 경로 · `_failure_verdict` 호출 계수 0 |
| **T-4** `test_t25_a3_halt_predicate_quantifies_each_failed_check` | `_exit_retry_eligible` → `True` / `&` | 🔴 / 🔴 | 출구 12 id 전건 열거. 단 기대값이 `EXIT_RETRY_CHECK_IDS` **상수**라 정합 편집에는 눈이 없다(RB-1) |
| **T-5** `test_coherent_retry_tamper_is_rejected_before_dispatch` | 진입 가드 호출(`read.py:1518`) 삭제 | 🔴 `1 failed` | 디스패치 0회도 함께 확인 |
| **T-7** 골든 | `select_failure_row` 를 `reversed(rows)` 로 | 🔴 **1,020/8,190칸 불일치**, 관문은 **exit 0** | 설계 경계 확인 — 관문은 값을 보지 않는다 |
| **T-7** | 계약 4행↔5행 실물 순서 교환 | 🔴 + 관문 **exit 1** + T-13 🔴 | 삼중 검출 |
| **T-7** | (자기참조 점검) | — | manifest 를 자기와 비교하지 않는다. 8,190회 **런타임 `_failure_verdict` 실호출** · 검증기 적재는 `Path(__file__).parent/"fixtures"/…` · β 는 **시험 코드의 고정 식**(manifest `predicate` 미평가) |
| **T-6** `test_retry_checks_rejects_…` | `_retry_checks` 유일성 강제 제거 | 🔴 `1 failed` | |
| **T-8** `test_terminal_action_and_gate_escalation_fail_closed` | `terminal_action` 검증 생략 | 🔴 `1 failed` (T-7 은 🟢 — 층 분리 정상) | |
| **T-11 ⑤** | 관문 `TERMINAL_ACTIONS` 에서 `reject-upstream` 제거 | 🔴 + 관문 exit 1 | |
| **T-12** | 엔진 `ENGINE_READ_CHECK_IDS` 에 유령 추가 | 🔴 `1 failed`, 관문 **exit 0** | 관문 오라클과 독립인 계약↔엔진 다리로 작동 |
| **T-13** | 계약 행 순서 교환 / 12행화 | 🔴 | `len(rows) != 11` 리터럴이 실질 방벽 |
| **T-9** | — | — | `grep` 실측 엔진 호출자 **0** |

`D-20260903-03` §2 ⑥「변조–읽는 구간」표는 내가 대조한 전 행에서 실물과 일치했다. §2 ⑧ 좌표 재실측표도 표본 전건 일치(`read.yaml:217/233/245/337/697/710-782` · `__init__.py:103/130/142/194/414` · `read.py:158/774/800/828/856/1518/1826/1842` · `SPEC:4552/4655/4700`). §2 ⑦ 양화사 6항도 내 독립 재실측과 같다(`declared_only=[] failure_only=[]` · `early/exit list-union=([],[])` · `entry_only=[]` · `kinds` 3종 unique).

---

## 5. 신규 지적

### RB-1 · HIGH · 출구 재시도 8종이 「독립 정답지」가 아니라 서로를 보는 사본 셋에만 결박됐다 — 정합 편집이 전 관문·전 시험을 통과한다
**귀책 = 설계(발주자).**
**좌표** `contracts/stages/read.yaml:245-250` · `engine/stages/read.py:117-134`(`EXIT_RETRY_CHECK_IDS`) · `tools/check_failure_table.py:24-37`(`APPROVED_RETRY_CHECKS`) · `tests/test_m21_…::test_t25_a3_halt_predicate_quantifies_each_failed_check`(기대값 = 엔진 상수) · 설계 v18 W-1 행.
**재현** ① 계약 8행 `points: [early, exit]` → `[early]` ② `EXIT_RETRY_CHECK_IDS` 에서 두 id 삭제 ③ 관문 `APPROVED_RETRY_CHECKS["exit"]` 과 `APPROVED_FAILURE_TABLE` 8행에서 같이 삭제 → 관문 7종 두 모드 exit 0(`exit_retry=6`) · `--self-test 36/36` · **`761 passed in 153.58s`**.
**왜 결함인가** ⑴ 실동작이 바뀐다 — `_exit_retry_eligible({read.claim-inventory})` 가 `True→False`, 출구 청구항 실패의 정본 후속 재시도 1회가 0회가 된다. 그 재시도의 존재 이유를 계약 자신이 `why_this_can_be_repaired` 에 「통합이 분해 산출에서 claims 를 **재복사**하므로」라 적었으니, 사라지는 둘이 바로 그 근거의 대상이다. ⑵ 골든 8,190칸은 (조치, 라벨) 함수만 고정하므로 재디스패치 횟수에 **구조상** 눈이 없다(T28 ⒟ 총괄 정밀화가 스스로 밝힌 성질). ⑶ SPEC `:385`·`:4700` 이 8종을 산문으로 열거하지만 `check_spec_refs.py` 는 그 산문을 계약과 대조하지 않는다 — 변조 뒤에도 `RESULT: PASS`. ⑷ 설계 W-1 은 이것을 **BLOCKER** 로 세우며 *「승인된 출구 재시도 8종이 독립 정답지에 결속되지 않았다」* 고 요구했는데, 처분은 **같은 값의 사본을 둘 더 만든 것**이고 T-11 ⑥·T-12·T-13 은 그 사본들끼리의 상등만 잰다. 사본 n 벌은 독립 오라클이 아니다.
**닫힌 자리도 함께 적는다(감사가 좁게 말하지 않기 위해)** — 나머지 6종은 이 형태로 뺄 수 없다. `read.schema`(1행)·verbatim 계열 5종(9행)은 `points` 가 `[exit]` 하나뿐이라 제거하려면 행을 쪼개야 하고 그 순간 `len(rows) != 11` 리터럴이 잡는다. early 쪽은 `set(EARLY_RETRY_CHECK_IDS) == set(EARLY_CLAIM_CHECK_IDS) | {CONVERGENCE_CHECK_ID}`(T-12)가 `reader/lib` 의 진짜 독립 상수에 묶는다. **뚫리는 자리는 정확히 두 검사**이며, `points` 가 둘인 유일한 재시도 행이 그 통로다.

### RB-2 · MED · B-0 단위 시험 86건이 작업 트리가 아니라 정본 main 을 검증한다
**귀책 = 설계(발주자).**
**좌표** `tests/test_m24a_failure_grid_generator.py:24 MAIN_REPO = "/home/laptop/projects/patent-docent"` · `:100-135 committed_clone`. 근거 = 설계 v18 AF-2 · `SPEC-round-b0.md` §「시험용 clone 조립」이 *「`git clone -q --no-hardlinks /home/laptop/projects/patent-docent <tmp>/clone`」* 을 문자 그대로 못박았다.
**재현** 사본에서 `engine/stages/__init__.py` 의 `select_failure_row` 를 `reversed(rows)` 로 바꾼다(골든 1,020칸이 어긋난다) → `pytest tests/test_m24a_failure_grid_generator.py` → **`86 passed in 10.44s`**. 같은 상태에서 `tests/test_m24_failure_grid_golden.py::test_every_golden_cell_matches_runtime` 은 `1 failed`.
**왜 결함인가** `EXPECTED_COUNTS` 상등 · `provenance` · 생성 명령 블록 ⒜⒝⒞⒟ · provenance 거부 6종이 전부 **정본 main 의 커밋된 HEAD** 위에서 돈다. 오늘 main HEAD 가 감사 핀과 같아 값이 우연히 맞을 뿐이고, worktree·클론에서 일하는 순간(= 이 리포의 표준 작업 형태) 이 86건은 **자기가 무엇을 검증했는지 모른다**. 「공허 통과」는 이 리포가 `python3 -O` assert 금지를 세울 때 든 바로 그 형태다. AF-2 의 사유(신설 3파일이 미커밋이라 clone 에 없다)는 B-0 병합(`6f93519`)으로 소멸했고 fixture 도 그 경우를 다루는데(`status` 가 비면 커밋 생략), clone **원천**만 정본으로 남았다. 부수로 `MAIN_REPO`·`PYTHON_BIN` 절대경로가 시험 스위트를 이 기계에 결박한다.

### RB-3 · MED · 설계 v18 이 T-2 의 보호 대상을 잘못 적었고, 그 문장이 W-1 처분의 충분성 논거로 쓰였다
**귀책 = 설계(발주자).**
**좌표** 설계 v18 §2.9 T-4 행 — *「exit 목록에서 `read.verbatim` 을 빼면 T-2 가 떨어진다」*.
**재현** ① 계측: `_exit_retry_eligible` 을 감싸 T-2 시나리오를 돌리면 `EXIT_FAILING_SETS: [['read.pointer-resolve']]` ② `read.verbatim` 을 계약·엔진·관문에서 정합 제거해도 T-2 초록 ③ `tests/test_m17_lanes.py:63` 의 docstring 이 스스로 *「정본 후속 검사를 실패시키는 payload 묶음(`read.pointer-resolve` 대상)」* 이라 적는다.
**왜 결함인가** 설계가 8종 중 어느 것에 행위 결속이 있는지를 한 칸 틀렸고, 그 칸이 W-1(BLOCKER) 을 닫았다고 판단한 근거 묶음에 들어 있다. 실제 행위 결속은 `read.schema`(`test_t25_read_schema_still_retries_once_before_halt`)와 `read.pointer-resolve`(T-2) 둘뿐이고 나머지 여섯은 구조 방벽(11행 리터럴)에만 기댄다. 「강제의 범위를 실제보다 넓게 말했다」계열이며, 이 리포가 감수에서 FAIL 을 받은 바로 그 형태다.

### RB-4 · LOW · `D-20260903-03` §1 의 「발주자 오류 0건(이 라운드)」 이 사실이 아니다
**귀책 = 발주자(총괄).**
**좌표** `docs/decisions/D-20260903-03-round-b.md` §1 말미.
**재현** RB-1·RB-3 이 설계 v18 귀책이고, 라운드 B 발주문이 설계 §2 전체를 첨부해 그대로 들여왔다.
**왜 결함인가** 라운드 A 가 FAIL 을 낸 사유가 *「원장 집행 조건 둘이 「충족」으로 보고된 채 충족되지 않은 것 — 둘 다 발주문 귀책」* 이었다. W-1 을 closed 로 선언한 것이 같은 형태다. 문장의 근거로 든 것(「레인이 blocked 를 내지 않았고 ⑦⑧⑥ 표가 채워졌다」)은 **레인이 부딪힌 결정 공백이 0**이라는 뜻이지 발주 산출물의 오류가 0이라는 뜻이 아니다 — 두 명제가 한 문장에 눌려 있다.

### RB-5 · LOW · `CLAUDE.md` §6 일곱째 행만 「관문이 주장하지 않는 것」을 적지 않는다
**귀책 = 저작 레인(문서 hunk) / 설계(§2.10 반영처 지시).**
**좌표** `CLAUDE.md:124`.
**재현** 같은 표의 다섯째 행은 *「그 밖의 저자 경계는 사람이 지킨다」*, 여섯째 행은 *「열거가 감수 원문을 빠짐없이 담았는가는 반입 시점의 사람 몫이다」* 를 든다. 일곱째 행은 `SPEC §8.3 12항`이 명시한 셋(값의 참·거짓 = T-7 · 종단 어휘 상등 = T-11 ⑤ · 승인 집합 상등 = T-11 ⑥)을 하나도 옮기지 않는다.
**왜 결함인가** 이 표는 CLAUDE.md 가 매 세션 로드하는 정본이고, 「실패표가 **정확하다**」만 읽는 사람은 골든 값까지 이 관문이 본다고 읽을 여지가 있다. 2026-08-19 감수 A′ 가 NEW BLOCKER 로 짚은 것이 정확히 이 표의 증명 범위 기재였다.

### RB-6 · LOW · 생성기의 자기 검증에서 `check_ids.expected_set` 이 항진식이다
**귀책 = 저작 레인(B-0).**
**좌표** `tests/fixtures/read-failure-grid/generate.py:246` — `expected_check_ids=set(manifest["check_ids"])`.
**재현** 검증기의 70 제약 중 `check_ids.expected_set`(집합 상등)은 이 호출에서 자기와 자기를 비교한다. 같은 제약을 T-7(`tests/test_m24_failure_grid_golden.py:63`)과 B-0 시험은 진짜 상수(`set(READ_CHECK_IDS)|set(ENGINE_READ_CHECK_IDS)`)로 넘긴다.
**왜 결함인가** 설계 §2.8 은 *「생성기: 파일을 쓰기 **전에** 자기 산출을 검증하고 위반이 있으면 파일을 쓰지 않는다」* 를 명했고, 자기참조 오라클은 Z-2 가 이미 사냥한 형태다. 실해는 작다(`len == 12` 는 살아 있고, 진짜 결속은 T-7 이 든다) — 그래서 LOW 이며, 고치려면 `set(run_checks_module.READ_CHECK_IDS) | set(read_stage.ENGINE_READ_CHECK_IDS)` 를 넘기면 된다(생성기는 그 둘을 이미 들고 있다).

---

## 6. Q2 · Q5 · Q6 · Q7 · Q8 판정

### Q2 — 명령되지 않은 부작용: **없음.** 다섯 커밋의 hunk 를 전수로 근거에 대응시켰다.

| 커밋 | hunk 군 | 명한 것 |
|---|---|---|
| `1d29c8b` | `read.yaml` 실패표 11행 재작성 | T26 ⒜①② · T29 §3 ③ · T30 ⒜ |
| | `read.yaml` exit `checks` 8종 명시 + `[정정]` 마커 | T26 ⒜③ · T28 ⒜ · A-6 처분 |
| | `read.yaml` `failure_binding_status` 신설 | A-3 계열(설계 T-10) |
| | `retry_budget.binding_status` `checks` 를 `test_bound`→`runner_reads` | **정당한 공학 재량** — 러너가 실제로 읽게 되었으니 분류가 따라간다(사실 정정) |
| | `__init__.py` `failure_rows_for_checks`/`failure_row_of_kind`/`terminal_action`/`select_failure_row` | T26 ⒜①② · B-5 fail-closed |
| | `read.py` 상수 2벌 · `_retry_checks` · `_validate_retry_contract` · `_exit_retry_eligible` · `_failure_verdict` 재작성 · `_gate_escalation_verdict` | W-1 · W-2 · N-4 · T25 · T28 |
| | `check_failure_table.py` 신설 | T26 ⒜③ |
| | 시험 7파일 | 설계 §2.9 T-1~T-13 |
| | 문서 5파일 | 설계 §2.10 |
| `47e437c` | manifest 1파일 | T26 §3 ② · T28 ⒟ · T29 §3 ① |
| `6f93519` | 3파일 | 설계 §2.8 · AA-4 |
| `99fad78` | 7파일 | A-1~A-7 처분 + Q5 불변식 |
| `867b95b` | 2파일 | C-2·C-3·C-4·C-6 처분 |

- **조용한 거부/통과 변화 없음.** 새 경로는 전부 **더 엄격**하다 — 구 `_failure_entry_for` 는 표에 없는 검사 id 를 verbatim 행으로 조용히 흡수했고 지금은 `StageError`; 구 `_halts_immediately`(source-digest 만) → `_exit_retry_eligible`(부분집합, convergence 추가). 반대 방향(덜 엄격해진 자리)은 찾지 못했다. 「오늘의 표」8,190칸이 한 칸도 안 움직인 것이 그 독립 증거다.
- **`runs/**` 무접촉.** 다섯 커밋 전부 `git diff --stat … -- runs/` 0행. 기존 산출물 4런은 새 실패표 아래서 그대로 선다(행위시법 P-U1) — 새 관문은 계약만 읽고, 진입 가드는 런 시점의 현행 계약을 본다.
- **폐기된 needle 시험의 보호는 전부 이전됐고 넓어졌다.** ⑴ needle 유일성 9개 → `test_every_declared_check_matches_exactly_one_contract_row` 가 **선언 13 id 전건** + 런타임 `failure_rows_for_checks` 가 `!= 1` 이면 `StageError`. ⑵ needle 목록↔코드 양방향 → `"failure_entry(" not in read.py` (더 강한 주장) + 관문 G2 의 선언↔행 양방향. ⑶ kind 3행 유일성 → `failure_row_of_kind` + G1 `kinds` 대조 + T-13. ⑷ lane-log 전용 행 분리 → T-13 의 「서로 다른 singleton 행」. **누락 없음.**

### Q5 — A′·C′ 이행: **처분표대로 닫혔다.**

| 지적 | 처분 | 실물 | 판정 |
|---|---|---|---|
| A-1 | 수용 | 변조 앵커가 청구항 본문 · **양성 대조**(변조본 위 조기 검사 실제 fail / 원본 전건 pass) · 조기 판정서 전 칸 대조 · `/decompose/retry-` 0 | **일치** |
| A-3 | 수용 | `any` → 라운드 B 가 부분집합으로 강화 · `test_t25_a3_any_halt_failure_stops_canonical_tail_retry`(복합 `{schema, source-digest}`) | **일치·강화** |
| A-4 | 수용 | `OSError` → `read.source-digest` 대리 행 + `actual: "(읽을 수 없음: …)"` · 삭제 어댑터 시험 | **일치** |
| A-5 | 수용 | needle 목록 확장 → 라운드 B 가 needle 자체를 폐기하고 **선언 13 id 전수**로 대체 | **일치·강화** |
| A-6 | 수용 | A′ 의 YAML 주석 → 라운드 B 에서 선언 자체가 참이 됨(명시 8종) + `[정정]` 마커 | **일치·소멸** |
| A-7 | **부분 수용** | enum↔`read_runs` 시험 = `test_m24_read_run_vocabulary_binding.py` 실재. 스키마 enum 은 T32 로 상신 → `canonical_selection.read_run` 은 **여전히 자유 문자열** | **일치**(「부분」이 실물과 맞다 · T32 는 T31 소라운드 소관) |
| A-8 | 수용 | HANDOFF §0 재작성 | 일치 |
| Q5 불변식 | — | `read.py:1976` `if repeated and not (…& set(READ_CHECK_IDS)): raise StageError` → 골든 `StageError: 3` 칸(레인 로그 단독 비공집합 3개)과 정확히 대응 | **일치** |
| C-2 격 어휘 | 수용 | `CRITICAL` → exit 1 · 빈 격 → exit 1 | **일치** |
| C-3 arity | 수용 | 7셀 → `G4 … §1 표 arity` exit 1 · 5셀 → 같은 규칙 exit 1(`IndexError` 사망 없음) | **일치** |
| C-4 §0/§1 결속 | 수용 | `first_table_in_section` · §2 decoy·§0 앞 decoy 둘 다 **무시**하고 정식 절만 읽는다(발주문이 고른 설계 그대로) | **일치** |
| C-6 문언 | 수용 | docstring 에 「포인터 실재·사유 의미·`선행 종결` 사실성도 사람이 지킨다 · `이연 / TBD / TBD` 는 통과한다」 명시 | **일치** |
| C-6 자기 시험 6→10 | 수용 | `RESULT: PASS — self-test 11건 전건 일치 (canon 1 + 심은 결함 10종)` | **일치** |

### Q6 — B-0·골든의 진위: **값은 참, provenance 는 견고, 시험 하네스는 RB-2.**

- **재생성 바이트 대조** — `git worktree add --detach … 99fad78` → `python -I generate.py --repo … --base-commit 99fad78` → `EXIT=0` · `cells=8190 beta=2048`. 커밋본과 `cells`·`expected_counts`·`exceptions[0]`(`cell_count`·`cells`·`rule`·`predicate`·`meaning`·`id`) **전건 SAME**, 정규화 비교 `normalized-identical: True`. 다른 것은 `provenance` 경로 6개와 `generated_at` 뿐 — 발주문이 예고한 그대로다.
- **provenance 우회 6종 시도, 전건 방어** — 심링크 `--repo`(realpath 해소 · 값 동일, 우회 아님) · 상대경로 `--repo`(isabs 거부) · 더러운 트리(`ⓕ status --porcelain 값='M engine/stages/read.py'`) · `stash` 로 감춤(감추면 트리가 정말 깨끗해지므로 우회가 아니다) · 미추적 잡파일(`ⓕ … '?? .tmpjunk/'` — gitignore 되지 않는 한 잡힌다) · 잘못된 `--base-commit`(`ⓓ base_commit 값=HEAD[:7]='99fad78', --base-commit='1d29c8b'`) · `sys.modules` 선적재(`사전 import 검사 실패`) · repo 안 `engine/` 을 밖으로 심링크(`ⓐ read_module 값=… repo=…` + `ⓔ engine.__path__`). **뚫은 것 없음.**
- **제약 ID 차집합** — `CONSTRAINT_IDS n = 70 unique: True` / `TV_MUTATIONS n = 70 unique: True` / `diff ids-tv: []` / `diff tv-ids: []`. M1b 17차의 「0」재실측 확인.
- **총괄 재량 ⓔ(fixture 조항 삭제) = 적정.** 논거를 검증했다: `git diff --quiet 99fad78 94ca66f -- engine contracts reader` → **rc 1** — 라운드 B 자신이 `engine`·`contracts` 를 고쳤으므로 그 상설 조항은 `reader/` 와 무관하게 **어차피 영구 실패**했다. 잃은 보호는 없다(값 결속은 `EXPECTED_COUNTS` 상등 + T-7 런타임 대조가 든다). 총괄이 든 `reader/` 논거는 좁게 맞았고 결론은 옳다. **다만 그 fixture 의 진짜 약점은 조항이 아니라 clone 원천이었다 → RB-2.** 부수로, manifest 에 박제된 `generation_command` 는 오늘의 HEAD 에서 둘째 줄(`git diff --quiet`)에 걸려 **재실행 불가**하다. 설계상 의도(생성 시점 사전조건)이지만, 재현을 시도하는 다음 사람은 설명 없는 실패를 본다.

### Q7 — 발주자 오류·총괄 재량: **과함 / 적정 / 모자람**

| 항목 | 판정 | 사유 |
|---|---|---|
| `D-02` §5 ⑴ 미커밋 worktree → 「커밋된 clone 위에서」 | **모자람** | 방향은 옳으나 clone **원천**을 정본 main 으로 못박아 86건이 대상 트리를 벗어났다(RB-2). `REPO_ROOT` 였어야 한다 |
| `D-02` §5 ⑵ 신설 파일 둘 → 셋 | **적정** | 단순 계수 정정 |
| `D-02` §5 ⑶ / T34 ⓔ fixture 조항 삭제 | **적정** | 위 Q6 참조. 조항은 라운드 B 자체에 의해 죽었고 값 결속은 다른 곳에 있다 |
| `D-02` §5 ⑷ / T34 ⓕ `/tmp/pytest-of-laptop` 삭제 | **적정** | 자기 귀책으로 인정하고 재발 방지(호출별 basetemp·홈 fs)를 규율로 세운 것이 옳다. 이 감사도 그 규율을 따랐다(`/tmp` 여유 997M 유지 · 종료 시 잔재 0) |
| `D-03` §1 CLAUDE.md §6 표 형식에 맞춘 §2.10 조정 | **적정** | T33 ② 로 §6 가 표 형식이 된 뒤의 사실 반영. 실물이 그 형식을 지킨다 |
| `D-03` §1 B-7 「5+1」 미편집 수용 | **적정** | `D-20260902-02:136` 에 이미 `[정정 2026-09-02]` 가 구 문언 보존 형태로 서 있다(실측). 재편집이 오히려 규율 3 위반 |
| T33 ① 을 골든 뒤로 미룬 순서 / T34 ⓓ | **적정** | 생성 명령 둘째 줄이 `-- engine contracts reader` 경로 기준이고 `reader/procedure/*.md` 가 그 아래다. 순서를 바꿨으면 골든 생성이 사전조건에서 죽었다 |
| T34 ⓐ~ⓗ 8건 추인 | **판단 자체는 적정** | ⓐ(4b `수용` 유지) — C-1 이 지적한 것은 절차이고 T34 는 효력만 추인하며 위반 사실을 원장에 남긴다: 「효력은 사후에 줄 수 있지만 절차는 사후에 만들 수 없다」와 정합. ⓑ~ⓗ 도 기록·해석 격이 맞다 |
| `D-03` §1 「발주자 오류 0건」 | **과함** | RB-4 |

### Q8 — 선언과 실물: **대체로 일치. 두 자리에 틈.**

일치 확인 — SPEC §1.2 C6(「READ 실패표의 키·선택 규칙은 §1.16」) · §1.4 `retry_budget`(early 3 · exit 8 열거) · §1.16 3-c(11행 · `checks` xor `kind` · 격자와 동률 해소가 **다른 순서**임을 명시) · 3-d(진입/출구 경계) · 표 아래 문단(`condition`·`note` 는 산문 · 검사 id 는 정확히 한 행 · 양방향 · `upstream-defect` = `deferred/test_bound`) · §8.3 7항(일곱 · 발화 조건에 실패표) · 관문표 7행 · 12항(G1~G6 표 + 「변조 수는 도구의 출력이 센다. 이 문서는 그 시험 계수를 복제하지 않는다」 = **T5 준수**) · `:4700` 「12행 유지 + 출구 재시도 8종」 병기 · `CLAUDE.md:114/124` · `HANDOFF §3` 6→7 마커 · `IMPLEMENTATION-HISTORY` 4→5→6→7 · `read.yaml:707` 「행 순서 자체가 값이다」 주석 · 관문 docstring. `contracts/glossary.md` ↔ 계약 검사 id **양방향 차집합 0**(13/13). 산문에 시험 계수를 적은 자리 없음(HANDOFF §0 의 `761`·`36` 은 현행 상태 정본의 소관이라 T5 대상이 아니다).

틈 둘 — ⑴ **RB-5**(CLAUDE.md 일곱째 행에 「주장하지 않는 것」 부재). ⑵ **RB-1 의 문서면** — SPEC `:385`·`:4700` 이 8종을 열거하는데 그 열거를 계약과 대조하는 기계가 없다. 관문·시험을 정합 변조하면 이 두 산문이 조용히 거짓이 되고 `check_spec_refs` 는 `RESULT: PASS` 를 낸다.

---

## 7. [미검증]

1. **T-7 이 요구하는 「골든 값의 참」 자체.** 8,190칸이 `99fad78` 트리에서 재현된다는 것과 HEAD 런타임이 그 표와 일치한다는 것은 실측했으나, **그 표가 T26·T28 의 의도와 같은가**는 재정 문언을 코드 없이 손으로 재계산해야 검증되고 그렇게 하지 않았다. 대표 칸(설계 §3)만 눈으로 대조했다. 다만 도전 17회가 매번 독립 재계산으로 일치시켰다는 기록이 있다.
2. **`manifest["check_ids"]` 의 순서.** 검증기는 집합 상등·중복 금지·`len==12` 만 보고 **순서를 고정하지 않는다**. 순서를 치환하고 `cells`·`exceptions[0].cells` 를 함께 치환한 자기일관 manifest 가 T-7 을 통과하는지 실측하지 않았다(설계는 「T-7 ② 의 런타임 값 대조가 순서 오류를 잡는다」고 답했고, 동반 치환 시에도 그러한지는 안 재봤다).
3. **8종 중 나머지 6종의 정합 우회.** `read.schema`·verbatim 계열 5종은 11행 리터럴·`points` 구조상 막힌다고 **분석**했으나, 각각을 실제로 심어 pytest 전수를 돌리지는 않았다(claim 계열 둘만 실측). 분석이 틀렸다면 RB-1 의 범위가 넓어진다.
4. **`freeze`·`source` 스테이지의 needle 조회.** 두 스테이지가 여전히 `failure_entry(contract, …)` 를 쓴다(10곳). 그 계약들이 자기 파일인지는 확인했으나(각 스테이지가 자기 `contract` 인자를 받는다), 그 needle 들의 유일성은 이 감사의 범위 밖이라 재지 않았다.
5. **정본 리포의 `9143acb` 내용.** `--stat`(HANDOFF-NEXT.md 1파일 2행)과 커밋 메시지·저자만 확인했고 본문 diff 는 읽지 않았다. 감사 범위 밖 커밋이다.
6. **historian 상호 체크.** `reader/READER-VERSION` 상대 리포 대조는 하지 않았다(이 다섯 커밋이 `reader/schemas/` 를 건드리지 않아 발화 조건이 아니다 — `git diff --stat … -- reader/schemas/` 0행으로 확인).
7. **`-O` 에서만 달라지는 자리**를 관문 밖(엔진·시험)에서는 전수로 재지 않았다. 관문은 두 모드 stdout 바이트 동일을 실측했고, pytest 는 plain 만 761 을 돌렸다(레인 보고의 `PYTHONOPTIMIZE=1` 761 은 재현하지 않았다 — 시간).

---

## 판정

값은 정확하다. 8,190칸이 `99fad78` 에서 바이트 단위로 재현되고, 이행되지 않은 재정 조건은 하나도 없으며, 지정된 결함 12종은 전건 검출되고, A′·C′ 수리는 내가 심은 결함 앞에서 실제로 붉어졌다. 저작 레인의 집행은 흠잡을 데를 찾지 못했다 — 명령되지 않은 hunk 0건, 몰래 약해진 양화사 0건, 폐기 시험의 보호 누락 0건, ⑥⑦⑧ 보고표 전건 일치.

FAIL 의 사유는 **검증 체계가 자기가 고쳤다고 선언한 것을 고치지 않은 데** 있다. 설계 v18 은 W-1 을 BLOCKER 로 세우며 *「독립 정답지에 결속되지 않았다」* 고 요구했는데, 처분은 같은 값의 사본을 둘 더 만든 것이었고 그 사본들끼리의 상등만 재는 다리를 놓았다. 세 벌을 함께 고치는 편집이 관문 7종 두 모드 · `--self-test` 36/36 · pytest 761 을 **전부 초록으로 통과하면서** 출구 청구항 재시도를 1회에서 0회로 지운다(RB-1). 그 처분의 충분성 논거 하나는 사실이 아니었고(RB-3 — T-2 가 지키는 것은 `verbatim` 이 아니라 `pointer-resolve` 다), 값의 독립 오라클이어야 할 B-0 시험 86건은 작업 트리가 아니라 정본 main 을 보고 있었다(RB-2 — 골든 1,020칸을 어긋내도 86 passed). 그리고 라운드 기록은 이 라운드의 발주자 오류를 0건으로 적었다(RB-4).

`D-20260902-02` §23 의 관찰이 다시 맞았다 — 값은 열여덟 번째로 맞았고, 지적은 이번에도 **검증 체계가 고정하지 않은 것**에서 났다.

VERDICT: FAIL
