# 독립 감사 원문 — PD-M2b 합본 감사(fable xhigh · M9 4회째 · 라운드 M2b-2 `b0c4fb6` + M2b-1 `1bf24f1`) · 판정 PASS(LOW 6)

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 두 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(1차 응답 `out.txt` sha256 `99eb041acf4d10365903cc7e51dfadc0f418e3baa5de1eff3d1ed04a683618e0` · 276 B · 2차(재접속) 응답 `out2.txt` sha256 `8699d5754cf6e1d9c1c5abdb7c716a5f7e33975ba76c0afba67a8253da444e5f` · 20,539 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/fable-audit-round-m2b/`(brief.md = 발주문 v2 · runner.sh · runner-resume.sh · resume-prompt.md · raw.json · raw2.json · usage.json · usage2.json).

**좌석 = `좌석 M9` · `claude-fable-5-1` xhigh · `claude -p` 단발 · Bash allowlist** · 사본 `~/projects/workspaces/pd-audit-round-m2b`(detached `6ae5bc6` · `.audit-sandbox` · alternates 없음). **1차 세션(03:46 → 04:06 · 59턴 · 19.8분 · $12.50 · 출력 86,564 · 캐시 읽기 4.22M)** 은 우회표·최소 변조·관문·다리 시험·프로브 실측을 마친 뒤 전체 pytest 를 **배경으로** 띄우고 「알림을 기다리겠다」는 276 B 응답으로 턴을 끝냈다 — 단발 모드는 그것을 최종 결과로 회수해 종료됐고 배경 pytest 는 39% 에서 죽었다(**LANE-RUNTIME 함정 N** · 이 사건에서 신설). **2차 = `--resume` 재접속(04:08 → 04:17 · 4턴 · 9.2분 · $1.28)** — 총괄 지시문(`resume-prompt.md` · 배경 금지 · 전경 `timeout` 600000 · 앞 실측 반복 금지)으로 전체 plain 을 전경 완주(**909 passed**)하고 판정 전문을 냈다. 합계 63턴 · 29분 · $13.78. 다른 세션의 pytest 3개(patent-quant · 각 676 MB)가 내내 돌아 「다른 pytest 가 돌면 기다린다」는 지키지 못했다(감사자 명시).

**판정 = PASS · 신규 BLOCKER/HIGH/MED 0 · LOW 6 · 근거 누락·허가 이탈 0 · 진위 쟁송 0 · 우회표 `[미검증]` 0 · 전체 plain 909(독립 실측).** Q1ⓐ 정적 관문 우회 26 프로브(거부 사유 전건 규칙과 일치 · 안 보는 축 5 는 층 3 이 잡음) · 층 2/3 동적 프로브 15(**D10 = `request.config._pd_original_append` 직접 호출만 세 층 전부 우회 → RL-5**) · (ii)-M R1~R6 전건 발주문 표와 일치(R1′ 관측 열만 발주문 오기 → RL-4) · Q2ⓐ 값 공간 변경 13건 전수표 전건 근거 있음(T40 ③ · 자잘 ⓐ · T4 · 자문 ⓔ·B-01·B-02 · P-U1/P-U2 · 규율 11 ③) · `READ_RUNS`·`LANE_TASKS` = 정본 사본(다리 4/4) · Q2ⓒ `lane_id` 우회 16 + containment 7(말단 **hardlink** 는 경로상 루트 안 · 약속 밖 관측) · 로그 ⑷ 호출 계수 0/1 독립 재측정 · Q2ⓓ V2·V5·V6·V7·다리 4 재현 전건 일치 · Q2ⓔ `run_kind`·`partial_until` 후속 소비·분기 **없음**(G-12 문언 정확). **LOW 6**: RL-1 DISPOSITIONS B-02 행 「5자리」(실물 6) · RL-2 §0 계수 「34/12/46」(실물 59/12/71 — 정정 체인이 틀린 기저에 +1 씩) · RL-3 「행 수 273」 = 데이터 272 + 헤더 · RL-4 v6 R1′ 관측 열 「(g) 통과」(실측 거부 유지 · 사유만 변경) · RL-5 conftest 가 원본을 `session.config._pd_original_append` 에 보관 → 시험이 직접 호출하면 세 층 우회(발주문 ⓪ⓒ 가 그 자리를 예시로 지정 · sol 저작 + 총괄 발주문) · RL-6 `lane_file` 이 `name="."` 통과 · NUL 은 `ValueError`(호출자가 상수만 넘겨 실효 없음). 관측: hardlink 경계 · 커밋 메시지의 칸 수 13·9·2.

지적 열거 = RL-1, RL-2, RL-3, RL-4, RL-5, RL-6

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§16**. RL-1~3 = 기록 정정(이 커밋) · RL-4 = 발주문 문언 정정(drafts v7) · RL-5·RL-6·hardlink 문서화 = **이연**(처분 어휘 · 다음 코드 라운드 · 값 공간 0 · 시험 환경/방어 다듬기).

---

# 감사 원문 1차 (claude-fable-5-1 xhigh · 03:46 → 04:06 · 판정 없이 종료된 응답 · 이 아래는 감사자 저작)

전체 plain 스위트가 31% 진행 중이며 메모리도 버티고 있습니다(가용 458 MB). 남은 것은 이 결과 하나뿐이라 배경 작업 종료 알림을 기다린 뒤 basetemp 삭제 · 종료 조건 실출력 · 판정 전문을 한 번에 적겠습니다.


---

# 감사 원문 2차 (claude-fable-5-1 xhigh · `--resume` · 04:08 → 04:17 · 이 아래는 감사자 저작)

# PD-M2b 합본 감사 판정(좌석 M9 · fable xhigh 4회째 · 발주문 v2)

**판정 요약.** 신규 BLOCKER/HIGH/MED 0 · LOW 6(기록 3 · 발주문 문언 1 · 저작 2) · 근거 누락·허가 이탈 0 · 근거 진위 쟁송 0 · 우회표 `[미검증]` 0 · 전체 plain 909 passed(독립 실측). 세션 경위 하나를 먼저 적는다: 첫 전체 스위트를 배경으로 띄웠다가 단발 모드 종료로 39% 에서 끊겼고(하네스 teardown · OOM 아님), 재접속 뒤 전경 실행으로 완주했다. 다른 프로젝트의 pytest 3개(patent-quant-analysis · 4시간 이상 · 각 676 MB)가 내내 돌고 있어 「다른 pytest 가 돌면 기다린다」를 끝까지 지키지 못했고, 총괄 재현과 같은 경합 조건에서 돌렸음을 명시한다. 킵얼라이브 `CronCreate` 는 이 세션에 그 도구가 없어 걸지 못했다.

## ① Preflight (실출력)

```
.audit-sandbox: path=/home/laptop/projects/workspaces/pd-audit-round-m2b · pin=6ae5bc68f7f2e5a09e6a00731d9a1c9be61017ee · order=AUDIT-round-m2b-20260906 · disposable=true
HEAD = 6ae5bc68f7f2e5a09e6a00731d9a1c9be61017ee (detached) · git status --short = "?? .audit-sandbox" 한 줄
정본 HEAD = 6ae5bc68f7f2e5a09e6a00731d9a1c9be61017ee (읽기만)
생산 원장 정본·사본 sha256 = e2350e0d20d138a797153048a411cfd95c324bc2294fc977b061a61b1bb75df2 · 6행 (시작 · 종료 동일)
python = .venv 3.14.4 · pgrep '[p]ytest' exit 0 → 3 프로세스(patent-quant-analysis · 나와 무관) · 가용 메모리 480 MB
f788604 ↔ HEAD 의 engine/contracts/tests/tools/reader/ledgers diff = 빈 출력 (완성본 = HEAD 파일)
```

## ② 실측표

### Q1ⓐ 우회표 · 층 1 = 정적 관문(`direct_engine_ledger_calls` 합성 파일 26)

| 프로브 | 관문 | 사유 |
|---|---|---|
| S01 `type Later = read_stage.run(…, shadow_root=None)` (자문 A-01) | 거부 | 허용 목록 밖 (TypeAlias.value) |
| S02 `x: read_stage.run(…)` 주석 (자문 A-01) | 거부 | 허용 목록 밖 (AnnAssign.annotation) |
| S03 lambda 본문 | 거부 | Lambda.body |
| S04 기본 인자 | 거부 | arguments.defaults |
| S05 데코레이터 | 거부 | FunctionDef.decorator_list |
| S06 클래스 본문 | 거부 | ClassDef.body |
| S07 `**{"shadow_root": None}` | 거부 | shadow_root 없음 |
| S08 모듈 최상위 walrus | 거부 | 블록 밖 |
| S09 헬퍼 `as g` 별칭 + body 호출(양성) | 통과 | 오탐 없음 |
| S10 async def 본문 | 거부 | AsyncFunctionDef.body |
| S11/S12/S14/S25 IfExp · f-string · for 본문 · try finalbody(양성 즉시평가) | 통과 | 정상 |
| S13 match guard | 거부 | match_case.guard |
| S19 `ExitStack.enter_context(헬퍼)` 뒤 호출 | 거부 | FunctionDef.body(보수적 오탐 · 정직) |
| S20 `yield read_stage.run(…)` | 거부 | Yield.value |
| S22 헬퍼 인자 위치 (g) | 거부 | 헬퍼 인자 위치 |
| S23 맨 이름 헬퍼(양성) · S24 헬퍼+raises 한 with(양성) | 통과 | 정상 |
| S26 DictComp | 거부 | DictComp.value |
| **S15 `functools.partial`** · **S16 `append = read_stage.append…`** · **S17 getattr** · **S18 모듈 별칭 `rs`** · **S21 런타임 None 변수** | **통과(미탐)** | 문서화된 안 보는 축 → 층 3 이 잡는가는 아래 D 표 |

층 1 구멍의 실물: 구 관문(`3865645` 의 `_direct_engine_ledger_calls`)에 프로브 `def _probe(): read_stage.run(…, shadow_root=None)` 를 두면 `[]`(통과), 신 관문은 `허용 목록 밖 (FunctionDef.body)`.

### Q1ⓐ 우회표 · 층 2(헬퍼) · 층 3(세션 거부) — `tests/test_zz_audit_dyn.py` 18 passed · 가짜 생산 = `<basetemp>/fakeprod`(git 리포) 의 `ledgers/shadow/screening.jsonl` · 두 층 모두 같은 파일에 monkeypatch(realpath 확인) · 실제 생산 원장 무접촉

| 프로브 | 잡은 층 | 가짜 원장 행 |
|---|---|---|
| D01 헬퍼 안 · 다른 repo 로 해석(A-02) | 층 2 결속 감싸기(기입 전 · 토큰 `결속`) | 0 |
| D02a `main/ledgers` → 가짜 생산 symlink · 헬퍼 진입(A-03) | 층 2 진입 ③′ `원장 실경로` | 0 |
| D02b 같은 symlink · 별칭 호출 · 헬퍼 없음 | 층 3 세션 거부(기입 전) | 0 |
| D03 `main/ledgers/shadow` symlink · 헬퍼 진입 | 층 2 ③′ | 0 |
| D04 말단 `screening.jsonl` symlink · 헬퍼 진입 | 층 2 ③′(realpath) | 0 |
| D05a 말단 **hardlink**(realpath 무력) · 헬퍼 진입 | 층 2 ③′ samefile | 0 |
| D05b 말단 hardlink · 별칭 · 헬퍼 없음 | 층 3 samefile | 0 |
| D06 `functools.partial(shadow_root=None)` · repo=가짜 생산 리포 | 층 3 | 0 |
| D07 모듈 별칭 `rs.append_screening_ledger` | 층 3 | 0 |
| D08 `getattr` 동적 전달 | 층 3 | 0 |
| D09 import 시 잡은 `original_append` 동적 전달 | 층 3(잡힌 객체가 `guarded` 자체) | 0 |
| **D10 `request.config._pd_original_append(…)` 원본 직접 호출** | **어느 층도 못 잡음** | **1** |
| D11 헬퍼 안 직접 `open(…, "ab")` | 층 2 finally 지문 · 쓴 뒤 탐지(문서화된 축) | 1 |
| D12 런타임 None 변수 | 층 3 | 0 |
| D13 가짜 생산의 링크 worktree · 헬퍼 진입 / 별칭·헬퍼 없음 | 층 2 ② `주 트리` / 층 3(main-worktree-resolved) | 0 |
| D14 헬퍼 안 `os.replace` | 층 2 finally 지문 · 쓴 뒤 탐지 | 1 |
| D15 헬퍼 안 · repo=가짜 생산 리포 · None | 층 2 결속 감싸기 | 0 |

### Q1ⓓ 프로브2(모듈 최상위 explicit `shadow_root=<가짜 루트>` · 시험 함수 0)
완성본: 수집 오류 `Failed: 시험 환경에서 생산 섀도 원장 기입 거부: …/fakeprod/…/screening.jsonl` · exit 2 · 가짜 0행.

### Q1ⓑ (ii)-M 재현표 (기준 blob `tests/ledger_guard.py` = `226f82e8730fcde730d988fa75afafbb7bbdbeca` · `tests/conftest.py` = `b0313450d3b85acb617921c240fd305f7fa3d0b2` · 레인 보고 복원 해시와 일치 · 변조 = `python3` 문자열 치환 · 복원 = `git checkout --` · 매 행 복원 해시 = 기준 해시)

| 행 | 변조(unified hunk 요지) | 변조 해시 | 실행 | 관측 | 고정 시험 판정 | 발주문 표와 |
|---|---|---|---|---|---|---|
| R1 | `_none_call_reason`: `if (type(parent), field) not in _ALLOWED_PARENT_FIELDS:` → `if False:` | `8bc33a7c` | `pytest tests/test_m2_read.py -k closed_allowlist` | (f)(h)(i)(j)(l) 통과 · (g) `헬퍼 인자 위치` 유지 · (a)(e) 거부되되 사유 `블록 밖` · (b)(c)(d)(k)(o) 무변화 | (a)(f)(h)(i)(j)(l) FAIL · (e)(g) PASS = 6 failed 7 passed | 일치 |
| R1′ | `if field == "items":` → `if False:` | `ccfcf004` | 같음 | **(g) 여전히 거부**(def 안 = `허용 목록 밖 (FunctionDef.body)` · 모듈 최상위 = `블록 밖`) | (g) FAIL(토큰) = 1 failed 12 passed | 판정 열 일치 · **관측 열 「(g) 통과」는 발주문 오기(RL-4)** |
| R2 | ③′ `pytest.fail("원장 실경로…")` → `pass` | `f403f08a` | `-k production_guard` | (ⅵ) 진입 허용 | (ⅵ) FAIL = 1 failed 8 passed | 일치 |
| R2a | ② `pytest.fail("주 트리…")` → `pass` | `e66395c0` | 같음 | (ⅳ) ③′ 가 `원장 실경로` 로 대신 거부 | (ⅳ) FAIL(토큰 `주 트리`) = 1/8 | 일치 |
| R2b | ③ `pytest.fail("생산 자리…")` → `pass` | `beff7e7d` | 같음 | (ⅴ) 진입 허용 | (ⅴ) FAIL = 1/8 | 일치 |
| R3 | `read_stage.shadow_screening_ledger = bound` → `pass` | `caa35a8f` | 같음 | (ⅶ) 해석 정상 반환 | (ⅶ) FAIL = 1/8 | 일치 |
| R4 | `finally:` → `except BaseException: 원복; raise` + 지문 검사를 정상 경로로 | `59c2e246` | 같음 | (ⅸ) `ValueError: body` 전파 · 지문 미보고 | (ⅸ) FAIL · (ⅷ) PASS = 1/8 | 일치 |
| R5 | conftest `offenders = ledger_guard.direct_engine_ledger_calls()` → `offenders = []` (프로브1 재설치) | `e42b4c26` | 프로브 단독 / m2 ④ | 훅 있음 exit 4(`UsageError … test_zz_m2b1_probe.py:9 … FunctionDef.body`) · 훅 제거 exit 5 | m2 ④ FAIL(1 failed) · 복원 뒤 exit 4 · 프로브 삭제 | 일치 |
| R6 | `read_stage.append_screening_ledger = guarded` → `pass` (프로브2 존재 · 가짜 0행) | `a819bcc0` | `-k session_guard` / 프로브2 단독 | (m) 가짜 파일 1행 기입 · 프로브2 단독 exit 5 + 1행 | (m) FAIL (n) PASS · 복원 뒤 프로브2 exit 2 · 0행 · (m)(n) 2 passed | 일치 |

Q1ⓒ: `ledger_guard.py`·`conftest.py`·m27 두 파일·`test_m2_read.py` 신설 범위(1783~2103)·m16/m26 변경 hunk 에 맨 `assert` 0. 신설 24칸 `-O` 24 passed · plain 24 passed. Q1ⓔ: (ⅸ) 완성본 PASS(`__context__` = ValueError) · R4 로 뒤집힘 실측 · (ⅳ)=② 적중(R2a 만 붉힘) · (ⅴ)=③ 만 적중(R2b 만 붉힘 · R2 는 (ⅳ)(ⅴ) 무변화). Q1ⓕ: `git diff --numstat 3865645 1bf24f1 -- engine/stages/read.py` = `7 0` · `-U0` hunk 하나 `@@ -2264,0 +2265,7 @@` · `AST-EQUAL(docstring 제외)` exit 0 · 대상판 blob `ccd1e912` = HEAD blob · sha256 `c837114b…` 동일.

### Q2ⓐ 값 공간 변경 전수표(`4dfe341..b0c4fb6`)

| # | 변경 | 근거 | 판정 |
|---|---|---|---|
| 1 | `run-kinds.yaml#run_kind_enum` + `partial` | T40 ③ 문언 그대로 | 허가 안 |
| 2 | `kinds.partial`(publishes false · requires_defense_layers false · terminates_at declared · `terminates_at_field` · `terminates_at_enum` 13 · anchor_ledger excluded · deliverables []) | T40 ③(비게시 · 종료 스테이지 필수 · 앵커 편입 없음 · 통주 리포트 무의무) · 13종 = SPEC §1.3~§1.15 제목 실측 상등(자문 ⓔ) | 허가 안 |
| 3 | `enforcement_run_kind` 블록 | T40 자잘 ⓐ | 허가 안 |
| 4 | `source.run` 가드: enum 대조 / partial 은 `partial_until ∈ enum` / 비partial 의 값 거부 / `partial` 블록 부재 `StageError` | 자잘 ⓐ / T40 ③ 필수 / 자문 ⓔ(공학 집행) / 오류 처리 재량(규율 11 ③ · fail-closed) · 수용 입력 축소 없음 | 허가 안 |
| 5 | `partial_until` 을 `run.yaml`·조기 보고에 항상 기입(null) | T40 ③ + 선언된 부재 관례(P-U2) · 기록 필드 | 공학 |
| 6 | `paths.run_kinds_contract(repo)` | P-U1 행위시법 | 공학 |
| 7 | `LANE_ID_PATTERN` fullmatch(`__post_init__`·`lane_dir`·`lane_file`) | T4 「계약 어휘 검증」(read.yaml form · retry 1부터 · batch 0부터) | 허가 안 |
| 8 | `READ_RUNS`·`LANE_TASKS` 소속 검사 | 자문 B-01(T4 문언 안) · **정본 사본**: 스키마 enum · `sub_lanes[].id` · `read_stage.run` 기본값 · `plan.TASKS is` 와 상등 · 넷 중 하나만 바꿔도 다리 시험 붉음(실측 4/4 · 복원 PASS) | 허가 안 · 새 값 집합 아님 |
| 9 | `lane_dir` realpath 루트 포함 | T4 「루트 포함 강제」 | 허가 안 |
| 10 | `lane_file` 말단 포함 + `name` 검사(`/`·`..`·빈값) | 자문 B-02(T4 안) · name 은 상수 호출뿐 | 허가 안 |
| 11 | `read.py` finding 규칙 `lane-log.digest-path-contract`(기존 검사 안 · 새 check id·실패표 행 없음) | 자문 ⓔ(기존 CheckRow finding) | 공학 |
| 12 | `read.yaml` 어휘 4키 · 검사 서술 한 구절 · SPEC 11자리 + G-12 · CLAUDE.md | T4 · T40 ③(SPEC C9·§8.2·§8.4 갱신 동반) · 자문 ⓕ | 문서 |
| 13 | 어댑터 2 → `lane_file` · `plan.TASKS = LANE_TASKS` | B-02 · 단일 진원 | 공학 |

스키마·실패표·좌석 `sub_lanes` model/effort 변경 0(diff 실측). 근거 열 빈 행 0 · 허가 범위 이탈 0 · 제시 근거의 진위를 다툴 사항 0 → 상신 분리 사항 없음.

Q2ⓑ: 독립 프로브(원천 파일 부재 + 승계 루트 부재 + 위반 kind) 전건 `StageError`(가드 문언) · `run_root` 부재 · 유효 kind 면 다음 예외가 승계 확인이라 가드가 원천 읽기·승계·`ensure_source_dirs` 앞임을 실측. m27 (a)(b)(c)(f)(g)(e)(i)(j) 10 passed · (g) `type is StageError`(`StageHaltError` 는 하위형이나 정확형 단언 통과) · 구 법 트리 rehearsal ok · `partial_until: null` 키 실재.

### Q2ⓒ `lane_id` 우회표(엔진 직접 호출)

| 시도 | 결과 |
|---|---|
| U1 아랍-인도 숫자 `batch-٠` · U2 키릴 `е` · U3 NUL 종단 · U4 백슬래시 · U5 `retry-0` · U6 대문자 · U7 `./` · U8 `../` 삽입 · U9 전각 슬래시 · U10 CR · U14 빈값 · U15 None · U16 `batch-00` | 전부 `어휘 위반(형태)` |
| U11 `read-c` · U12 `decompose-x` | `어휘 위반(소속)` |
| C1 중간 디렉터리 symlink(`lane_dir` · `lane_file`) | `루트 밖(디렉터리)` |
| C2 말단 symlink: `lane_dir` 통과(설계) · `lane_file` | `루트 밖(말단)` |
| C3 말단 **hardlink** → 밖 inode | 통과(경로상 루트 안 · samefile True · 「루트 포함」 약속 밖 · 관측) |
| C4 말단 symlink → 루트 안 파일 · C5 루트 자체 symlink · C6 루트 끝 슬래시 · C7 미존재 루트 | 통과(정상) |
| name `../x` · `sub/x` · `..` · `x/` · 빈값 | `어휘 위반 · name` |
| name `.` | **통과**(디렉터리 경로 반환 · RL-6) · name NUL → `ValueError`(RL-6) |
| 잔존 `lane_dir(` 호출 = `file_adapter.py:79`(makedirs 뒤 쓰기는 `lane_file`) · `os.path.join(.*lane` = `paths.py` lanes_dir 2 · `contract.py:458`(lane_dir 내부) · `read.py:2036`(id map basename) | lane_id 기반 맨 join 잔존 0 |
| 로그 ⑷ `_bare_sha256_file` 호출 계수(독립 monkeypatch) | 완성본 **0** + `fail` + `루트 밖(말단)` · V7 제거판 **1** + `pass` |

### Q2ⓓ 재현표(완성본 = HEAD 파일 · 기준 `source.py` `9d28d845` · `contract.py` `de1824fa`)

| 행 | 변조 hunk | 변조 해시 | 관측 | 고정 시험 판정 | 복원 |
|---|---|---|---|---|---|
| V2 | `_engine_pin` 직후 가드 블록 32행 제거 | `e503d5d4`(레인 변조 해시와 동일 · 후속 수리가 블록 안뿐이므로) | (c) `run.yaml run_kind: partial · partial_until: bogus-stage` · (f) `rehearsal · read` · (g) 지운 `partial` 기록 · (a) `bogus` · 조기 보고도 동일 | m27 run_kind 6 failed 4 passed | `9d28d845` |
| V5 | 소속 `if` → `if False` | `102ae602` | 소속 음성 3 `LaneRequest` 생성 · 형태 음성(`../x` · `retry-0`) 거부 유지 | 소속 3 FAIL · 29 PASS(정합 양성 PASS) | `de1824fa` |
| V6 | `lane_dir` realpath `if` → `if False` | `841c8de6` | 직접 중간 symlink 경로 반환 · 로그 ⑶ 여전히 fail 이되 토큰 디렉터리 False · 말단 True | 직접 칸 · 로그 ⑶ FAIL = 2/30 | `de1824fa` |
| V7 | `lane_file` realpath `if` → `if False` | `1ab2b893` | 직접 말단 symlink 경로 반환 · 로그 ⑷ `pass` · findings [] · 호출 1 | 말단 직접 · 로그 ⑷ FAIL = 2/30 | `de1824fa` |
| D | 스키마 enum `read-c` / `read.yaml` `synthesise` / `READ_RUNS` `read-c` / `read_stage.run` 기본값 `read-c` | `5b01e990` / `a4d043ea` / `cb495521` / `85a3e632` | — | 다리 시험 각각 FAIL(단언 4 각각) → 복원 PASS | 기준 해시 |

Q2ⓔ: `rg 'run_kind|partial_until' reader tools engine/stages/read.py engine/stages/freeze.py` 빈 출력 · `publishes|requires_defense|terminates_at|anchor_ledger` 의 엔진·도구·reader 소비 = `source.py` 가드뿐 · `run.yaml` 소비자 = `read.py:1663`(run_id) · `freeze.py:330`(run_id) · `:517`(frozen 목록) → **후속 소비·분기 없음**. 총괄 진술(종료선 초과 차단·`publishes: false` 강제 코드 없음)은 참이고 SPEC G-12 문언은 그 부재를 정확히 적었다.

## ③ 신규 지적

| ID | 격 | 좌표 | 재현 | 귀책 |
|---|---|---|---|---|
| RL-1 | LOW | `D-20260905-02` §10 정정 마커 「DISPOSITIONS 행은 6 이 맞다」 ↔ `DISPOSITIONS.md:378` B-02 행 「호출 5자리(read.py 1 · file_adapter 3 · replay 1)」 · 실물 6(file_adapter :52 :84 :86 :104 · replay :44 · read.py :1539) | `grep -n '| B-02 |' docs/decisions/DISPOSITIONS.md` | 총괄 기록 |
| RL-2 | LOW | `DISPOSITIONS.md:124` §0 계수 「등재 34 · 선행 종결 12 · 합 46」 ↔ 표 실물 등재 59 · 선행 종결 12 · 합 71(= `docs/lessons` 71파일 · §1 마커 자신도 「등재 59파일」). 정정 체인이 틀린 기저에 +1 씩 얹힘 · 관문은 계수를 안 봄 | 표 행 상태 계수 | 총괄 기록 |
| RL-3 | LOW | §1 「행 수 = 273」 = 데이터 행 272 + 헤더 1(처분 셀 272 · 「지적 전건」 문언과 1 차이) | `| ` 시작 줄 273 중 헤더 1 | 총괄 기록 |
| RL-4 | LOW | M2b-1 발주문 v6 §2 (ii)-M R1′ 관측 열 「(g) 통과」 · 실측은 거부 유지(사유만 `FunctionDef.body`/`블록 밖` 으로 변경) · 판정 열 「(g) FAIL」 은 맞음 | R1′ 표 | 총괄 발주문 |
| RL-5 | LOW | `tests/conftest.py:40` 원본을 `session.config._pd_original_append` 에 보관 → 시험이 `request.config._pd_original_append(…, shadow_root=None)` 로 세 층 전부 우회(D10 · 가짜 생산 1행). 발주문 ⓪ⓒ 가 그 자리를 예시로 지정 · 「안 보는 축」 문서화 없음. 처분 후보 = 클로저 보관 또는 docstring 명기(값 공간 아님) | D10 | sol 저작 · 총괄 발주문 병기 |
| RL-6 | LOW | `contract.py#lane_file` 이 `name="."` 통과(디렉터리 경로 반환) · `name` 에 NUL 은 `os.path.realpath` `ValueError`(LaneContractError 아님). 호출자 셋이 상수만 넘겨 실효 없음 | Q2ⓒ N 행 | sol 저작 |

관측(지적 아님): 말단 hardlink 는 경로상 루트 안이라 미검출(약속 밖 · 문서화 후보) · `1bf24f1` 메시지의 칸 수 13·9·2 는 총계가 아니며 낡을 수 없는 자리(T5 취지 밖 · 「계수 없는 메시지」 관행과는 어긋남) · `/tmp/sol-coder-round-m2b2` 는 레인 잔존물(내 것 아님 · 미접촉) · 이 하네스가 배경 출력을 `/tmp/claude-1000/` 에 쓴 것은 하네스 소관.

## ④ Q3 · Q4 · Q5

**Q3.** 결합 트리 전체 plain **909 passed · exit 0**(4:50 · 다른 pytest 3개 경합 중 · 전경 실행). m27 42 passed 가 conftest 두 훅 아래서 통과(`source.run` 은 append 무관 · 간섭 없음). m16·m26 의 파일 어댑터 왕복·헬퍼 블록은 전체 스위트 안에서 초록. `read.py` 두 라운드 접촉 = `:75`/`:1536`(M2b-2) 와 `:2265`(M2b-1 docstring) · AST 상등.

**Q4.** D-02 §9~§15 ↔ 원문 8+1건: DISPOSITIONS 10파일 57행이 각 `지적 열거` 와 ID·격·「수용」 전건 일치 · 관문 7종 plain·`-O` 전부 exit 0 · `--self-test` 0. 레인 보고 ↔ 실물: `final.txt` 883/883 · `final2.txt` 885/885 BLOCKED(청결) · M2b-1 909/909 · 총괄 §13·§14 서술과 일치 · 복원 해시 `226f82e8`·`b0313450` 은 내 기준 해시와 일치. 총괄 재현 885/909 두 모드 ↔ 내 plain 909(`-O` 전체는 내 실측 아님). HANDOFF 첫 화면 좌표(레인 디렉터리 · drafts 발주문 · basetemp) 실재. 커밋 메시지 총계 없음. §13 「환경 사고 2」 ↔ `repro-opt.*` 분리 재실행 · `stderr2.log` ENOSPC · `report-artifacts/` 6 diff + 보고 실물 정합. 정정 마커: §9 「5자리」→6 은 실물 6 으로 맞고 DISPOSITIONS 주장은 틀림(RL-1) · v5 「21행」→v6 23 은 `4dfe341` grep 23 · 분류 5+7+4+1+6 정합. 자문 REPLY.md 는 lesson 에 축약 없이 전문 보존(47행 전건 포함).

**Q5.** PASS 조건 전건 충족(신규 BLOCKER/HIGH/MED 0 · 우회표 미검증 0 · 근거 누락·허가 이탈 0 · 진위 쟁송 0). G-4 `partial` · B-2 `lane_id` · 백로그 ⑼ 는 감사상 닫힌 상태. 남은 것 = G-1~G-3 좌석(T40 ①② · 비교 실측 뒤) · G-12(재정) · 자문 ⓑ(이연) · **RL-5 보관 방식**(재량) · **RL-6 name 검사**(재량) · **RL-1~3 기록 정정** · **RL-4 발주문 문언** · hardlink 경계 문서화.

## ⑤ `[미검증]`

- `-O` 전체 스위트(발주문이 plain 1모드만 요구 · 총괄 885/909 두 모드는 인용값).
- `b0c4fb6` 시점 885 자체(체크아웃 안 함 · 레인 `repro-final.status` 인용).
- DISPOSITIONS 이전 마커(264 등)가 같은 헤더 포함 관례였는지(이력 미확인).
- 총괄 「하니스 배경 Bash OOM」의 직접 증거(간접 정합만).
- 첫 배경 스위트가 39% 에서 끊긴 원인(세션 종료 teardown 추정 · 전경 재실행은 완주).

## 종료 조건 실출력

```
basetemp /home/laptop/projects/workspaces/pd-audit12-basetemp 삭제 → 없음
__pycache__ 0 (관문이 남긴 tests/fixtures/read-failure-grid/__pycache__ 삭제)
합성 모듈·프로브 tests/test_zz_* 없음 · 임시 변조 전건 git checkout 복원(해시 상등)
git status --short = "?? .audit-sandbox" 한 줄 · HEAD 6ae5bc68f7f2e5a09e6a00731d9a1c9be61017ee
생산 원장 정본·사본 sha256 e2350e0d20d138a797153048a411cfd95c324bc2294fc977b061a61b1bb75df2 · 6행 (전후 동일)
```

VERDICT: PASS
