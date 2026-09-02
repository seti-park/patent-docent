# 독립 감수 원문 — 라운드 B′(`3d599f6`) 좁은 재감사(RB-1~RB-6 폐쇄 판정) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(감사 stdout 전문 · `opus-audit-round-b-prime/out.txt` 의 sha256 `41494f7ea0b7b618e8e0934d47fa33c0c093a40f3e42c2fadc451ca8dff394f8` 와 `---` 아래가 동일 · 26,133 B).

**좌석 = opus max**(ROUTING M9 · 저작 = sol-coder). CLI 직구동 `claude -p --model claude-opus-5 --effort max`(환경변수 2종 실측) · `setsid` 배경 + `EXIT=` 마커 · 04:59 → 05:53(약 54분) · EXIT=0 · stderr 0 B. 발주문 = `AUDIT-ORDER-round-b-prime.md`(다섯 질문 · 지적 ID `RC-*` · **감사 중 정본 커밋 금지** — 지켜졌다: 감사 전후 정본 HEAD `4a3d6e5` 동일 · status 0행 · 감사자 §1 「발주자 오류 없음」). 사본 = `audit-round-b-prime`(detached `4a3d6e5` · 마커 3검증 일치) · 감사 뒤 사본 원상 복구 · `/tmp` 잔재 0(감사 중 총괄이 감사자의 미사용 basetemp 1개 276 MB 를 지웠다 — tmpfs 보호 · 실행 중인 것은 건드리지 않았다).

**판정 = FAIL · 지적 7건(MED 2 · LOW 5) · 새 재정 사항 0 · 값은 열아홉 번째로 일치.** **RB-1(HIGH)은 진짜로 닫혔다** — 감사가 4자리 정합 편집을 다시 심어 신설 도출식 시험 **하나만** 붉음을 확인하고, 직전 감사가 「막힌다」고 분석했던 나머지 6종(`read.schema` · verbatim 계열 5종)에도 11행 유지 정합 편집을 심어 **관문 7종이 여섯 전건 초록인데 도출식 시험이 여섯 전건 붉음**을 실측했다(직전 [미검증] ③ 을 실측으로 닫음 — 직전 감사의 분석은 틀렸고 B′ 의 다리가 그 자리까지 덮었다). RB-3·RB-4·RB-5 closed · [미검증] ②(순서 동반 치환 · before `73 passed` → after `1 failed`)·⑧ closed. **RB-2 partially** — 델타 미러 여덟 경계 중 **이름 변경**에서 옛 경로가 clone 에 남고 clone 이 「깨끗」으로 신고된다(**RC-1** · MED · 레인 귀책 · `unlink` 한 줄). **RC-2**(MED · 설계 귀책): 도출식의 후건(halt·β 를 뺀 전부가 재시도 대상)은 어느 재정에도 없고 lane-log 2종의 배제가 `ENGINE_READ_CHECK_IDS` 소속이라는 우연에 기댄다 — 오늘 값은 무변경(규율 11 ③ 분류 유효)이나 새 검사의 기본값을 입법하는 형태. RC-3(SPEC 「출구 독해 검사 10종」 정의 없음) · RC-4(RB-6 항진식이 한 단계 위로 옮겨졌을 뿐) · RC-5(형제 파일 `:62` 절대경로 잔존) · RC-6(RB-4 정정 문언의 귀책 계수가 §6 과 다름) · RC-7(`test_m24*` 세 모듈이 형제 모듈의 `sys.path` 부작용에 의존 · 선재).

지적 열거 = RC-1, RC-2, RC-3, RC-4, RC-5, RC-6, RC-7

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-03-round-b.md` **§8** 에 있다. **전부 수용** → 라운드 **B″**(sol-coder) + RC-6 은 이 커밋에서 정정. B″ 의 감사는 별건 재감사 대신 **T31·T32 소라운드의 감사에 합본**한다(§8 근거).

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

모든 실측을 마쳤다. 사본·정본 모두 원상 복구했다.

---

# 좌석 M9 적대 재감사 보고 — 라운드 B′ (`3d599f6` · 좁은 감사)

## 1. preflight 실출력

```
=== .audit-sandbox ===
path=/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-b-prime
pin=4a3d6e588423365c752dfac64010baef801b52f0
order=AUDIT-round-b-prime-20260903
disposable=true
=== 사본 HEAD ===  4a3d6e588423365c752dfac64010baef801b52f0
=== 사본 status ===  ?? .audit-sandbox   (1행)
=== 정본 HEAD ===  4a3d6e588423365c752dfac64010baef801b52f0
=== 정본 tree ===  586383355c14a28de6ac6b28140af4163145eb71
=== 정본 status 행 수 ===  0
```

마커 3검증 일치 · **정본 HEAD == `4a3d6e5`**(감사 종료 시점 재확인도 동일 · 정본 worktree 3개는 전부 무관한 특허 작업 디렉터리). 발주자 오류 없음.

**기준선(사본 HEAD)** — 관문 7종 plain·`-O` 전건 rc=0 · `--self-test` 두 모드 `mutations=36 rejected=36` `EXIT=0` · pytest plain `762 passed in 154.78s` · `PYTHONOPTIMIZE=1` `762 passed, 1 warning in 186.53s`. 골든 manifest `47e437c..3d599f6` diff 0 · 보호 경로(`contracts engine tools reader`) `8c05d13..3d599f6` diff 0 · 생성기 `assert` 0. §7 총괄 재현표와 전건 일치.

---

## 2. RB-1 ~ RB-6 폐쇄 판정표

| ID | 판정 | 재현 마지막 출력 줄 |
|---|---|---|
| **RB-1** | **closed** | 정합 4자리 편집 → 관문 7종 rc=0 (`exit_retry=6`) · self-test `36/36` · pytest **`1 failed, 761 passed in 154.68s`**(신설 도출식 시험만) |
| **RB-2** | **partially-closed** | 미커밋 변조 `1 failed, 85 passed in 11.16s` · 커밋 변조 `1 failed, 85 passed in 11.06s` — **그러나 이름 변경이 조용히 잘못 미러된다**(RC-1: `clone 에만 = ['reader/READER-VERSION']` · clone status `''`) |
| **RB-3** | **closed** | v19 부록 정정 1 문언 실측 확인 — `read.pointer-resolve` 제거 시 `FAILED …test_v2_exit_retry_repairs_phase_drift`, `read.schema` 제거 시 `FAILED …test_t25_read_schema_still_retries_once_before_halt` |
| **RB-4** | **closed** | `D-20260903-03` §1 에 `[정정 2026-09-03 · 감사 RB-4]` 실재 · 구 문언 보존 — 열거는 좁다(RC-6) |
| **RB-5** | **closed** | `CLAUDE.md:124` 세 항목이 SPEC §8.3 12항 셋과 지시 대상 동일 |
| **RB-6** | **closed(명령대로) · 지적 형태는 잔존** | 유령 주입 → 지금 `manifest 검증 실패: check_ids.expected_set` `EXIT=1` 파일 미작성 / 구 코드 `EXIT=0` 유령 박힌 manifest 작성. 그러나 양변이 같은 두 상수에서 나와 **항등식은 그대로**(RC-4) |
| **[미검증] ②** | **closed** | 자기일관 치환본 → B′ `1 failed, 72 passed`(순서 단언) / B′ 이전 **`73 passed`** — 직전 감사의 의심이 옳았다 |
| **[미검증] ⑧** | **closed** | `bash -x` 마지막 실행 줄 = L2 `git diff --quiet 99fad78 HEAD -- engine contracts reader` · `rc=1` · L3~L5 미실행 · worktree·출력 파일 0 |

---

## 3. Q1 우회 재시도 표

### ⓐ 감사가 쓴 정합 편집(claim 2종) + 도출식 자체 공격

| 편집 | 관문 7종 | `--self-test` | pytest |
|---|---|---|---|
| 4자리 정합 편집(계약 8행 `points` · exit `checks` · `EXIT_RETRY_CHECK_IDS` · 관문 상수 2곳) | 전건 rc=0 `exit_retry=6` | `36/36` EXIT=0 | **`1 failed, 761 passed`** — 신설 도출식 시험 **하나만** |
| 위 + `READ_CHECK_IDS` 에서 두 id 함께 삭제 | `check_validator_enforcement` **rc=2**(`ENVIRONMENT ERROR: … 알 수 없는 검사 id: read.dependency-parse`) · **`check_failure_table` 은 rc=0**(관문 G2 는 잡지 못한다 — YAML 만 읽는 설계 경계) | `36/36` EXIT=0 | **`159 failed, 531 passed, 72 errors`** — 도출식 시험 자체는 **`1 passed`** |

**「독립 오라클」의 성질.** `READ_CHECK_IDS` 를 함께 고치면 도출식 시험은 눈이 없다. 그러나 그것은 실행 등재부이므로 편집이 **159 실패 + 72 오류**로 폭발한다 — 다리는 「조용한 우회」를 「조용할 수 없는 우회」로 바꾼 것이고, W-1 이 요구한 것은 그것으로 충족된다. 다만 관문 G2 는 이 편집에 눈이 없고, 붉어진 관문은 `check_validator_enforcement` 뿐인데 그마저 FAIL 이 아니라 **환경 오류(rc=2)** 로 난다.

### ⓑ 나머지 6종 — 직전 감사 [미검증] ③ 을 실측으로 닫는다

11행·id 유일성을 유지하는 정합 편집(대상 id 를 `read.lane-log-shape` escalate 행으로 옮김)을 6종 각각에 심었다.

| 대상 | 관문 7종 | `--self-test` | pytest 실패 목록 |
|---|---|---|---|
| `read.schema` | **전건 rc=0** `exit_retry=7` | rc=1 (`ValueError` 사망) | 4 — `test_t25_read_schema_still_retries_once_before_halt` · `test_terminal_action_and_gate_escalation_fail_closed` · 관문 self-test 시험 · **도출식** |
| `read.verbatim` | **전건 rc=0** | rc=1 (사망) | 5 — `test_t25_a3_halt_predicate…` · `test_lane_log_verdicts…` · 관문 self-test 시험 · **도출식** · 골격 |
| `read.pointer-resolve` | **전건 rc=0** | `36/36` | 7 — `test_v2_exit_retry_repairs_phase_drift`(T-2) 외 · **도출식** · 골격 |
| `read.coverage` | **전건 rc=0** | `36/36` | **2** — **도출식** · 골격 |
| `read.value-derivation` | **전건 rc=0** | rc=1 (사망) | 5 — 진입 가드 · 정합 변조 거부 · 관문 self-test 시험 · **도출식** · 골격 |
| `read.bibliography` | **전건 rc=0** | `36/36` | **2** — **도출식** · 골격 |

**직전 감사의 「나머지 6종은 이 형태로 뺄 수 없다 — `len(rows) != 11` 리터럴이 잡는다」는 분석은 틀렸다.** 여섯 전부 11행을 유지한 채 뺄 수 있고 **관문 7종은 전건 초록**이다. 그 여섯을 실제로 붙잡는 것은 B′ 가 세운 **도출식 시험**이다(「골격」 실패는 내 변조 착지 지점이 lane-log 행이라 생긴 부작용 — 착지 지점을 `read.source-digest` halt 행으로 바꾸면 골격 대신 골든 T-7·생성기가 붉어지고 도출식은 그대로 붉다: `4 failed, 759 passed`). 즉 **RB-1 의 처분은 [미검증] ③ 이 열어 둔 자리까지 실제로 덮었다.** 부수 관찰 — 6종 중 3종에서 `--self-test` 가 판정이 아니라 `ValueError: list.remove(x): x not in list` **사망**으로 rc=1 을 낸다(관문 자체는 B′ 반경 밖·선재).

### ⓒ 도출식의 출처 — 재정 문언인가 총괄이 만든 것인가

원장 원문을 전건 대조했다.

| 도출식의 항 | 재정 근거 | 판정 |
|---|---|---|
| `read.source-digest` 제외 | T25 ⒜ *「실패한 검사 중 하나라도 그 계약 행이 `halt` 이고 `retry(n)` 이 없으면 …즉시 나온다」* + T24 「`halt` 그대로」 | **원장에 있다** |
| `read.convergence` 제외 | T28 ⒜ *「출구 재시도 목록 — `read.convergence` 를 **제외**한다」* | **원장에 있다(명시)** |
| **나머지 8종이 전부 재시도 대상이라는 후건** | T26 ⒜③ 는 *「실제 재시도 가능한 **부분집합**」* 만 요구한다. 「halt·β 를 뺀 전부」라는 문장은 **어느 재정에도 없다** | **총괄/레인의 재구성** |
| lane-log 2종 제외 | T22(출구 루프 뒤 합류) — 그러나 도출식은 그 근거를 쓰지 않고 두 검사가 `ENGINE_READ_CHECK_IDS` 에 산다는 **등재부 소속**으로 뺀다. 그 소속의 이유는 T22 와 무관하다(파일시스템 접근 — `read.py:107-124` 주석) | **우연의 일치**(RC-2) |

**규율 11 판별.** 오늘의 값은 무변경이다(HEAD 에서 도출식 시험 초록 · 8 = 8 · 골든 8,190칸 무접촉). 따라서 「기록·공학 집행」으로 본 총괄의 분류는 **맞다**. 다만 도출식은 *앞으로* 「`READ_CHECK_IDS` 에 더해지는 검사는 자동으로 출구 재시도 대상」이라는 **기본값을 입법**한다 — 재정이 세운 적 없는 규범이다(RC-2).

---

## 4. Q2 델타 미러 경계 표

독립 프로브(fixture 와 같은 순서로 clone → 미러 → 커밋 → clone·작업 트리 실물 대조)로 실측했다.

| 경계 | 결과 | 판정 |
|---|---|---|
| 기준선(깨끗) | 미러 1(`.audit-sandbox`) · clone status `''` · 차집합 0 | ✅ |
| **이름 변경(`git mv`)** | 미러 3 · clone status `''` · **`clone 에만 = ['reader/READER-VERSION']`** — 옛 경로가 남는다 | ❌ **조용한 어긋남 = RC-1** |
| 삭제(미스테이지 ` D`) | clone 에서 삭제 스테이지·커밋 · 차집합 0 | ✅ |
| 미추적 디렉터리(중첩 2파일) | `-uall` 로 파일 단위 열거 → 둘 다 미러 | ✅ |
| 심링크(정상 대상) | `symlink_to(os.readlink(...))` 로 링크 자체 복제 | ✅ |
| 심링크(끊어진 대상) | `is_file()` False → `is_symlink()` True 갈래로 복제 | ✅ |
| 무시 파일(`__pycache__/*.pyc`) | `--ignored` 미전달이라 git 이 애초에 열거하지 않음 → 미러 안 함 | ✅ (`if code != "!!"` 는 사문) |
| 공백 있는 경로 | `-z` 로 인용 없이 파싱 → 미러 | ✅ |
| 부분 스테이지(`MM` · index ≠ worktree) | **작업 트리** 내용을 미러 | ✅ (의도와 일치) |

**ⓓ `sys.executable`** — `PYTHON_BIN = sys.executable`(`:24`)이 `:184` 서브프로세스와 `:490` 생성 명령 환경에 그대로 들어간다. 같은 인터프리터를 **다른 경로 문자열**(`.venv/bin/python3`)로 부르면 `sys.executable = /home/laptop/projects/patent-docent/.venv/bin/python3` 이고 `86 passed in 11.57s` — 값이 실행 인터프리터를 따라간다. ✅

**ⓔ 정본 참조 잔존** — fixture 는 정본을 참조하지 않는다(`MAIN_REPO` 삭제 · `REPO_ROOT` clone 확인). 그러나 **형제 파일에 같은 결박이 남았다**: `tests/test_m24_failure_table_contract.py:62` `command = ["/home/laptop/projects/patent-docent/.venv/bin/python"]`(RC-5). `generate.py:20`·`validate_manifest.py:16`·`manifest.json` 의 `${MAIN:-…}` 는 재정의 가능한 기본값이자 박제된 생성 명령이므로 결박이 아니다.

**RB-2 원 결함 재현(대조군)** — 구 fixture(`8c05d13`) + 사본의 `reversed(rows)` 변조 → **`86 passed in 11.92s`**(맹목). 새 fixture 는 같은 상태에서 `1 failed, 85 passed`. 시험 수는 86 → 86 으로 불변.

---

## 5. 신규 지적

### RC-1 · MED · 델타 미러가 이름 변경을 조용히 잘못 미러한다 — 옛 경로가 clone 에 남는다
**귀책 = 저작 레인(B′).**
**좌표** `tests/test_m24a_failure_grid_generator.py:119-143` `_mirror_worktree_delta`.
**재현** `git mv reader/READER-VERSION reader/READER-VERSION-RENAMED` → 미러 후 clone 에 **옛·새 경로가 둘 다** 존재하고 `git -C clone status --porcelain` 은 `''`(깨끗)라 fixture 의 청결 단언이 통과한다. 실측 `clone 에만 = ['.audit-sandbox', 'reader/READER-VERSION']`.
**기제** rename 레코드에서 `deleted.add(old_relative)` 는 집합에만 넣고 **`target.unlink()` 를 옛 경로에 호출하지 않는다**. 파일이 clone 워크트리에 그대로 있으므로 뒤따르는 `git add -u -- <old>` 는 무효다.
**왜 결함인가** 처분표 §6 RB-2 행이 *「삭제는 삭제」* 를 명했고 rename 은 삭제+추가다. `engine/`·`reader/`·`contracts/` 아래에서 파일을 옮기면 생성기가 clone 의 **낡은 모듈**을 import 해 검증한다 — RB-2 가 잡은 *「자기가 무엇을 검증했는지 모른다」* 의 축소판이며, 실패가 조용하다는 성질까지 같다. 고치는 비용은 `else` 갈래 밖에서 옛 경로를 `unlink` 하는 한 줄이다.

### RC-2 · MED · 도출식의 「독립성」이 등재부 소속이라는 우연에 기대고, 그 후건은 재정 문언에 없다
**귀책 = 설계(발주자).**
**좌표** `tests/test_m24_failure_table_contract.py:236-245` · `docs/SPEC.md:385`·`:1315` · v19 부록 정정 2.
**재현** ⑴ 원장 전문 대조 — T26 ⒜③ 는 *「실제 재시도 가능한 부분집합」* 만 요구하고 「halt·β 를 뺀 전부」를 세우지 않는다(§3ⓒ 표). ⑵ lane-log 2종은 T22 를 근거로가 아니라 `ENGINE_READ_CHECK_IDS` 에 산다는 이유로 빠지는데, 그 소속의 사유는 *「디스크의 `request.md` 를 실제로 읽어야 하므로 이식 단위 등재부에 들어갈 수 없다」*(`engine/stages/read.py:107-124`)로 T22 와 무관하다.
**왜 결함인가** 두 결과가 따른다 — ⓐ 앞으로 **파일을 읽어야 하면서 출구 재시도 대상인** 검사가 생기면 도출식이 조용히 배제한다 ⓑ lane-log 검사가 어떤 사유로 `READ_CHECK_IDS` 로 옮겨지면 조용히 포함한다. 그리고 도출식은 재정이 세운 적 없는 **기본값**(READ 등재부에 더해지는 검사 = 출구 재시도 대상)을 입법한다. 오늘 값이 무변경이라 규율 11 ③ 분류는 유효하지만, 이 「우연」이 W-1 처분의 유일한 지지대다.

### RC-3 · LOW · SPEC 두 문장이 정의되지 않은 용어 「출구 독해 검사 10종」에 기댄다
**귀책 = 저작 레인(문서 hunk) / 설계 문언.**
**좌표** `docs/SPEC.md:385` · `:1315`.
**재현** `grep "독해 검사" docs/SPEC.md contracts/glossary.md` → B′ 가 넣은 두 문장이 전부. **같은 표 칸**(§1.16 3-d)이 *「출구 12검사」* 와 *「출구 독해 검사 10종」* 을 나란히 쓰는데 「독해」가 12 중 어느 10 을 가리키는지 정의가 없다.
**왜 결함인가** 계수 10 이 `reader/lib` 등재부와 맞는 것은 RC-2 의 우연이며, 그 우연이 정의 없는 용어에 감춰진다.

### RC-4 · LOW · RB-6 의 「항진식」은 형태 그대로 남았다 — 양변이 같은 두 상수에서 나온다
**귀책 = 직전 감사(처방) · 처분(무검증 수용).**
**좌표** `tests/fixtures/read-failure-grid/generate.py:157` · `:246`.
**재현** `check_ids = list(READ_CHECK_IDS + ENGINE_READ_CHECK_IDS)`(157) · `expected_check_ids = set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS)`(246). `set(list(A+B)) == set(A)|set(B)` 는 A·B 가 무엇이든 참인 **항등식**이므로 157 을 함께 고치지 않는 한 이 제약은 거짓이 될 수 없다.
**진전은 실재한다** — 157 만 변조(유령 1개 치환·`len` 12 유지)하면 지금 코드는 `manifest 검증 실패: check_ids.expected_set` `EXIT=1` 파일 미작성, 구 코드는 `EXIT=0` 로 유령이 박힌 manifest 를 쓴다. 즉 「생성 뒤 필드 변조」는 잡는다.
**왜 남는가** 직전 감사가 처방한 코드를 글자 그대로 집행한 결과다. 자기참조 오라클 성질이 사라진 것이 아니라 **한 단계 위로 옮겨졌을 뿐**이며, 처분표 §6 은 그것을 「닫는다」로 적는다.

### RC-5 · LOW · RB-2 의 「절대경로 기계 결박」이 형제 파일에 그대로 남았다
**귀책 = 처분 반경(총괄).**
**좌표** `tests/test_m24_failure_table_contract.py:62`.
**재현** `grep -rn "/home/laptop/projects/patent-docent" tests/ tools/ engine/ reader/` → `_run_gate` 가 관문 서브프로세스를 정본 venv 인터프리터로 돌린다.
**왜 결함인가** RB-2 는 *「부수로 `MAIN_REPO`·`PYTHON_BIN` 절대경로가 시험 스위트를 이 기계에 결박한다」* 고 적었고 처분은 `PYTHON_BIN = sys.executable` 인데, 같은 결박이 한 파일 옆에 남아 **시험을 돌리는 인터프리터와 관문을 돌리는 인터프리터가 갈린다** — 그 시험이 주장하는 plain/`-O` 두 모드 대조의 의미가 흐려진다.

### RC-6 · LOW · §1 RB-4 정정 문언이 감사의 발주자 귀책을 다시 좁게 센다
**귀책 = 총괄.**
**좌표** `docs/decisions/D-20260903-03-round-b.md` §1 말미.
**재현** 정정문은 *「설계 귀책 2건(RB-1 · RB-3)과 발주자 귀책 1건(RB-2)」* 을 든다. 감사 원문은 RB-5 의 귀책을 *「저작 레인(문서 hunk) / **설계(§2.10 반영처 지시)**」* 로 적었고, **같은 파일 §6** 의 「발주자 오류(총괄 귀책) — 이 감사가 낸 것」은 3건(⑴ 감사 발주문 ⑵ RB-2 ⑶ RB-4)을 든다.
**왜 결함인가** RB-4 의 요지가 *「이 라운드의 발주자 오류 계수가 사실이 아니다」* 였는데, 그것을 닫는 정정이 §6 과 다른 계수를 낸다. 격은 낮으나 형태가 같다.

### RC-7 · LOW · `test_m24*` 세 모듈이 형제 모듈의 `sys.path` 부작용에 의존해 단독 실행이 불가능하다
**귀책 = 선재(라운드 B 이전) — B′ 신설 아님.**
**좌표** `tests/test_m24_failure_grid_golden.py:15` · `tests/test_m24_failure_table_contract.py` · `tests/test_m24a_failure_grid_generator.py:19`.
**재현** `.venv/bin/pytest tests/test_m24a_failure_grid_generator.py` → `ERROR collecting … ModuleNotFoundError: No module named 'engine'` / `1 error in 0.25s`. `pytest tests/` 는 알파벳순으로 앞서는 `tests/test_m16_bibliography.py:34-35` 가 REPO 를 `sys.path` 에 넣어 준 덕에 통과한다.
**왜 적는가** B′ 가 세운 도출식 시험·순서 단언이 전부 이 세 모듈에 있어, *「이 시험 하나만 빨개진다」* 를 확인하려는 다음 사람이 가장 먼저 부딪힌다. 처분표 §7·레인 보고가 인용한 단일 파일 계수(`1 failed, 85 passed` 등)는 `python -m pytest` 로만 재현된다(내가 그 형태로 재현했고 계수는 전건 일치했다).

---

## 6. Q3 · Q4 · Q5 판정

### Q3 — RB-5 · RB-6 · [미검증] ②·⑧ 의 hunk

- **ⓐ CLAUDE.md 일곱째 행 ↔ SPEC §8.3 12항** — **같은 말이다.** 셋의 지시 대상이 일대일로 대응한다(골든 값의 참·거짓 = T-7 = `tests/test_m24_failure_grid_golden.py` · 종단 어휘 두 벌 상등 = T-11 ⑤ · 승인 집합 두 벌 상등 = T-11 ⑥). 다만 다섯째·여섯째 행이 든 `(규격 = SPEC §8.3 N항)` 포인터가 일곱째 행에는 없고, `T-7`·`T-11` 은 리포 밖 설계 메모에서만 정의된다.
- **ⓑ 생성기 자기 검증** — **실상수를 쓴다.** 유령 주입(len 12 유지) 시 `EXIT=1` · 파일 미작성. 구 코드 대조군은 `EXIT=0` 로 유령이 박힌 manifest 를 쓴다. 다만 RC-4.
- **ⓒ T-7 순서 단언** — **닫혔다.** 자기일관 치환본(`check_ids[0]↔[1]` + `cells` 8,190칸 + `exceptions[0].cells` 2,048칸 동반 치환)에서 B′ 는 `1 failed, 72 passed`(`골든 check_ids 순서가 원장 상수와 다르다`), B′ 이전은 **`73 passed`**. 직전 감사의 [미검증] ② 는 의심이 옳았고 지금 닫혔다.
- **ⓓ SPEC 문장 셋** — **실물과 맞다.** `bash -x` 로 마지막 실행 줄이 L2 임을 확인했고 L3~L5 는 실행되지 않았다(`worktree` 0 · 출력 파일 0 · `rc=1`).

### Q4 — 명령되지 않은 hunk: **없음**

`git diff 8c05d13 3d599f6 -U0` 의 **13개 hunk 전건**을 §6 처분과 대응시켰다.

| hunk | 명한 것 |
|---|---|
| `CLAUDE.md:124` | §6 RB-5 「B′ ⑤」 |
| `SPEC:385` · `:1315` | §6 RB-1 「B′ ②」 |
| `SPEC:4666` | §6 [미검증] ⑧ 「B′ ⑧」 |
| `generate.py` 4 hunk(시그니처·return·언팩·`expected_check_ids`) | §6 RB-6 「B′ ⑥」 — 앞 셋은 넷째의 기계적 전제 |
| `test_m24_failure_grid_golden.py` +3 | §6 [미검증] ② 「B′ ⑦」 |
| `test_m24_failure_table_contract.py` +12 | §6 RB-1 「B′ ①」 |
| `test_m24a` 6 hunk | §6 RB-2 「B′ ④」 |

**86건 이름 대조 — 누락 0.** 두 커밋의 `def` 목록 차분은 **신설 2**(`_worktree_delta` · `_mirror_worktree_delta`)뿐이고 삭제된 시험 함수는 없다. 상수·단언 토큰 계수도 전건 보존(`EXPECTED_COUNTS` 2/2 · `CONSTRAINT_IDS` 1/1 · `TV_MUTATIONS` 3/3 · `provenance` 28/28 · `python -I` 2/2 · `EXIT=0` 5/5 · `git diff --quiet` 1/1 · `base_commit` 4/4 · `tree_head` 3/3 · `reader_path`·`engine_path` 4/4). 시험 수 실측 86 → 86. 삭제된 `OUTPUT_NAMES`·`MAIN_REPO` 는 RB-2 처분이 명시로 요구한 것이다.

### Q5 — 총괄 기록의 정확성

| 항목 | 판정 |
|---|---|
| §7 총괄 재현표 | **전건 일치** — pytest `762`/`762 passed, 1 warning` · 관문 7종 두 모드 exit 0 · self-test `36/36` 두 모드 · 골든 diff 0 · 보호 경로 quiet 0 · 생성기 `assert` 0 |
| §7 양성 대조 RB-1 행 | **전건 일치** — `failure_rows=11 early_retry=3 exit_retry=6` exit 0 · self-test EXIT=0 · **T-7·m21 `92 passed`** · 도출식 모듈 **`1 failed, 9 passed`** · 되돌린 뒤 **`10 passed`** |
| §7 양성 대조 RB-2 행 | **전건 일치** — `1 failed, 85 passed` / 되돌린 뒤 `86 passed` |
| §7 「첫 시도에서 exit `checks` 인라인 목록을 빼먹어 관문이 G3 로 exit 1」 | **참** — 내가 8행만 고쳤을 때 관문 G3 가 승인 집합 차집합으로 exit 1 을 냈다. 자기 실패를 기록에 남긴 것은 옳다 |
| §6 「어떻게 닫나」 ↔ 실물 | **일치** — RB-1 ①②(도출식 다리 + SPEC 두 줄) · RB-2 ④(`REPO_ROOT` + 델타 미러 + `sys.executable`) · RB-5 ⑤ · RB-6 ⑥ · [미검증] ②⑦ ⑧⑧ 전건 실재. 「관문은 YAML 만 읽는 설계 경계 유지」도 참(`tools/` diff 0) |
| **RB-3 처분(8종 행위 시험 대신 도출식)** | **적정.** 도출식이 8종을 **균일하게** 묶고, 내가 심은 6종 정합 편집 전건에서 실제로 붉었다. 8종 각각의 행위 시험은 레인 로그 시나리오가 필요해 비용이 크고 이득은 도출식과 겹친다. **다만 단일 실패점이다** — 도출식 시험 한 건이 지워지면 여덟이 한꺼번에 방벽을 잃는다(행위 시험 여덟이었다면 독립적이었을 것) |
| **RB-4 정정 문언** | **부정확(좁다)** — RC-6 |
| **v19 부록 정정 1** | **실측과 맞다** — 「`read.pointer-resolve` 를 빼면 T-2 가」 → `FAILED test_v2_exit_retry_repairs_phase_drift` ✓ · 「`read.schema` 를 빼면 T25 시험이」 → `FAILED test_t25_read_schema_still_retries_once_before_halt` ✓. 둘 다 실제로 빼서 확인했다. 부수로 v18 이 지목했던 `read.verbatim` 은 T-2 를 떨어뜨리지 않는다는 RB-3 의 판정도 재확인했다 |
| 정본 무접촉 | **지켜졌다** — 감사 종료 시점 정본 HEAD `4a3d6e5` · status 0행 · 트리 `5863833…` |

---

## 7. [미검증]

1. **도출식이 재정 「의도」와 같은가.** 8종의 오늘 값이 T24·T25·T28 문언과 정합한다는 것은 원문 대조로 확인했으나, 「나머지 8종 전부가 정본 후속 재시도로 실제로 고쳐지는가」는 각 검사의 수리 기제를 손으로 재계산해야 하고 그렇게 하지 않았다(계약의 `why_this_can_be_repaired` 산문만 읽었다). RC-2 는 그 공백의 형식면만 짚는다.
2. **`READ_CHECK_IDS` 동반 편집의 159 실패 전건.** 폭발 규모(`159 failed, 531 passed, 72 errors`)와 대표 항목은 봤으나 전체 목록을 항목별로 귀속하지 않았다 — 「조용할 수 없다」는 결론에 필요한 만큼만 봤다.
3. **6종 정합 편집의 착지 지점 전수.** 두 형태(lane-log escalate 행 / source-digest halt 행)만 실측했다. 다른 착지 지점(예: convergence 행 + `phases`·early 목록 동반 개정)까지 열거하지는 않았다 — 그 경로는 G4·G2 를 함께 뚫어야 하므로 편집 면적이 훨씬 크다는 것만 정적으로 확인했다.
4. **델타 미러의 나머지 porcelain 코드.** `C`(복사 · `status.renames=copies` 필요) · `U`(미해결 병합) · `T`(타입 변경)는 코드를 읽어 갈래를 확인했을 뿐 실물로 심지 않았다. 시험 8종은 실측했다.
5. **`--self-test` 3종 사망(RC-1 아님).** 변조된 계약 위에서 관문 self-test 가 `ValueError` 로 죽는 것은 관측했으나, 그것이 정본 계약 위에서 발화할 수 있는 경로인지는 재지 않았다(관문은 B′ 반경 밖).
6. **`freeze`·`source` needle 유일성** · **historian 상호 체크** — 직전 감사와 같은 이유로 범위 밖(`reader/schemas/` diff 0).
7. **`4a3d6e5` 의 HANDOFF hunk.** `--stat`(2파일)과 §7 본문은 읽었으나 `HANDOFF-NEXT.md` 7행 diff 는 본문 대조하지 않았다.

---

## 판정

**RB-1 — 직전 라운드를 FAIL 시킨 HIGH — 는 진짜로 닫혔다.** 감사가 쓴 4자리 정합 편집이 이제 정확히 한 시험을 붉히고, 나는 그것을 나머지 6종으로 확장해 **직전 감사가 「막힌다」고 분석했으나 실제로는 뚫리던 자리 여섯**을 새로 뚫었는데 그 여섯도 전부 같은 도출식 시험에 걸렸다. 관문 7종은 여섯 전건에서 초록이었으니 **붙잡은 것은 오로지 B′ 가 세운 다리**다. [미검증] ② 도 before/after 실측(`73 passed` → `1 failed`)으로 닫혔고, ⑧ 은 `bash -x` 로 문장이 참임을 확인했다. 명령되지 않은 hunk 0건, 폐기된 단언 0건, §6·§7 기록은 내 실측과 계수까지 일치했다 — 총괄이 자기 첫 시도의 실패를 기록에 남긴 것을 포함해서다.

**FAIL 의 사유는 좁다. RB-2 의 처분이 자기가 없애려던 형태를 한 자리에 남겼다.** 델타 미러는 수정·추가·삭제·미추적·심링크·무시·공백·부분 스테이지 여덟 경계에서 옳게 돌지만, **이름 변경에서 옛 경로를 clone 에 남기고 그 clone 을 「깨끗하다」고 신고한다**(RC-1). 처분표 §6 이 스스로 *「삭제는 삭제」* 라 적은 그 문장이 rename 의 삭제 절반에 닿지 않았고, 실패가 조용하다는 성질은 RB-2 가 잡은 원 결함과 같다. 함께, RB-1 폐쇄의 유일한 지지대인 도출식은 그 후건이 어느 재정에도 없고 lane-log 2종의 배제가 등재부 소속이라는 우연에 기댄다(RC-2) — 오늘의 값은 옳지만 앞으로 조용히 틀릴 자리를 열어 둔 채 SPEC 이 그것을 정의 없는 용어로 적는다(RC-3).

값은 열아홉 번째로 맞았다. 지적은 이번에도 **검증 체계가 고정하지 않은 것**에서 났고, 이번에는 그 검증 체계가 바로 이 라운드가 만든 것이다.

VERDICT: FAIL
