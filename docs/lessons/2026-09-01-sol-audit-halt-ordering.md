# 독립 감수 원문 — `_failure_verdict` 분기 순서(총괄 저작분) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-01 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다.**

지적 열거 = 1a, 1b, 2, 3, 4a, 4b
id 는 아래 감수자가 붙인 지적 번호다. `1a`/`1b`·`4a`/`4b` 는 원장이 쪼갠 앞절반/뒷절반이며 그 분할은 `ruling-20260902-01-T24-T27.md` 가 든다(§T25 §1 = 지적 1 앞절반 · §T24 §1 = 지적 1 뒷절반 · §T27 §1 = 지적 4 뒷절반). 처분은 `docs/decisions/DISPOSITIONS.md` §1 에 행으로 선다(재정 T27 · 2026-09-02 소급 등재).

**좌석 = sol**(reasoning xhigh · `sol-auditor`). **교차 벤더 규칙의 적용** — 감사 대상 슬라이스
(`_failure_verdict` 의 `read.source-digest` 분기 이동 + `HALT_CHECKS` 표 시험)는 **총괄(Claude)이
직접 저작**했으므로 ROUTING §3 M9 에 따라 감사가 sol 로 갔다. 같은 커밋의 나머지는 sol-coder
저작이라 **opus max** 가 별도로 감사했다(`2026-09-01-opus-audit-t17-repair.md`).

**읽기 전용 준수** — 총괄이 `git status --porcelain` 0행으로 확인. 감수자는 정본에서 읽기만
하고 프로브는 별도 경로에서 돌렸다.

**★ 두 감사가 같은 자리를 반대로 판정했다.** opus max 는 이 확대 집행을 *"확대가 옳다"*
(closed · 확대 집행)로 보았고, sol 은 아래대로 **FAIL** 을 냈다. 그 차이 자체가 판단 재료이며
처분은 총괄이 별도로 상신한다 — **어느 한쪽을 골라 다른 쪽을 지우지 않는다.**

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

## SOL AUDIT REPORT

**STATUS:** complete
**VERDICT:** **FAIL**

### FINDINGS

**지적 1 — MED · `read.source-digest`의 `halt` 우선순위는 계약이 정한 것이 아니고, 애초에 halt 전용 검사가 재시도된다**
좌표: `engine/stages/read.py:1848`, `1714`(재시도 루프) · `contracts/stages/read.yaml:255`(exit 판정점 = `checks: checks_before_exit` 전체), `:709`(`read.source-digest` 행 = `action: halt` 단독, `retry(n)`·`points` 없음)

계약상 `read.source-digest`는 `retry(n)` 없이 `halt` 단독인데, 실제 exit 재시도 루프(`retry_budget.points[id=exit]`)는 실패 종류를 가리지 않고 `checks_before_exit` 전건에 `tail_budget`(1회)을 적용한다. 그 결과 이 검사는 첫 실패에서 즉시 halt하지 않고 후속 레인을 한 번 더 돌린 뒤 `repeated=True`가 될 수 있다 — `points_binding` 규칙은 `retry(n)` 행만 검사하므로 이 오라우팅을 잡지 않는다.

더 근본적인 반증: 분기 주석이 전제한 "원천이 도중에 바뀐 런" 진단이 실제 데이터 흐름과 맞지 않는다. `actual_digest`는 `source_text`(메모리 캡처본)에서 한 번 계산되고, `assemble_spec()`이 그 값을 `patent.source_digest`에 강제로 주입한 뒤(`read.py:523`), `read.source-digest` 검사는 다시 **같은 메모리 문자열**을 해시해 그 필드와 비교한다(`source_digest.py:29`). 디스크 원천이 진입 후 바뀌어도 이 검사는 검출하지 못한다 — 그 역할은 별도 경로(`checks_on_entry: read.input-digest`)가 이미 담당한다. 따라서 이 출구 행이 같은 서명으로 반복 실패한다면 원천 변경보다 **조립/검사 코드 결함**일 가능성이 높고, 이는 T16 §6 ⑤의 escalate 사유와 정확히 겹친다.

재현: `_failure_verdict(contract, [CheckRow(check_id="read.source-digest")], repeated=True)` → `("halt", None)`.

하류 확인: 이 리포에는 `read.run()`의 비시험 호출자가 없다. halt/escalate 모두 `read.py:1774`에서 `spec: None`으로 반환되고 CP1 재료 파일 작성 전에 끝난다. `SPEC.md:1332`가 두 조치의 의미를 구분해 정의하지만(escalate=Owner 상신 / halt=런 상태 무효), 그 차이를 실제로 집행하는 하류 코드는 아직 없다 — 오늘 존재하는 유일한 실차이는 반환 문자열과 `reason_label`뿐이다.

**지적 2 — MED · 복수 검사 동시 실패 시 우선순위, 그리고 미등재 검사(레인 로그 2종)의 처분을 코드가 계약 없이 자체적으로 만든다**
좌표: `engine/stages/read.py:1840`, `1862` · `contracts/stages/read.yaml:664`(failure 표)

현재 우선순위는 `read.schema` > `read.source-digest`(schema 없을 때) > `repeated` > `read.convergence` > 그 외(전부 `read.verbatim` 행을 대리 조회). `run_read_checks()`는 단락 없이 전 검사를 실행하므로 복수 동시 실패는 실재한다(코퍼스에 `dependency-parse + convergence`, `inventory + pointer + coverage + convergence` 등 확인). 그러나 계약의 `failure:` 표는 각 조건의 개별 처분만 선언하며 복수 조건 간 우선순위는 어디에도 없다. 공용 `worst_status()`(`engine/stages/__init__.py:101`)가 `halt > … > escalate` 순서를 갖고 있지만 READ는 이 함수를 쓰지 않는다.

더 구체적인 결함: 최종 `rows`에는 `read.lane-log-shape`·`read.lane-log-digest-value`도 포함되지만 계약 실패표에 이 둘의 조건이 없다. 실패 시 코드는 무관한 `read.verbatim` 행의 처분(`retry(1)→escalate`)을 그냥 빌려 쓴다. 게다가 이 두 행은 재시도 루프가 끝난 뒤 합류하므로 실제로는 재시도가 0회 집행된다.

재현: `_failure_verdict(contract, [CheckRow(check_id="read.lane-log-shape")], repeated=False)` → `("escalate", None)` (`read.verbatim` 행에서 빌린 값).

**지적 3 — MED · `HALT_CHECKS` 표 기반 두 시험 모두 세탁 가능하며, 표의 완전성은 전혀 보증하지 않는다**
좌표: `tests/test_m22_early_payload_assembly.py:138`(HALT_CHECKS), `144`(parametrize 시험), `164`(역대조 시험)

"전제부터 잰다" 가드는 표에 **이미 들어 있는** 각 행에만 작동한다. 표 자체의 완전성은 재지 않는다:
- `HALT_CHECKS`에서 `read.source-digest` 항목을 지워도 어떤 시험도 실패하지 않는다(파라미터 수만 준다).
- 계약에 새 halt 행을 추가해도 표가 따라갈 의무가 코드로 강제되지 않는다.
- 표를 비우면 pytest는 실패가 아니라 skip 처리한다.
- `_failure_verdict`를 직접 부르는 다른 시험이 이 리포에 없다.

역대조 시험(`test_repeat_escalation_still_applies_...`)은 이름보다 훨씬 약하다. 계약을 메모리상에서 변조해 `read.verbatim` 행의 최종 처분을 `then: halt`로 바꿔도 역대조는 여전히 통과한다(실측: `washed contract verbatim final=halt` / `inverse actual=('escalate', '국면 간 변이 재현 — 코드 결함 의심')`) — 왜냐하면 역대조가 실제로 지키는 것은 "`read.verbatim` 조회 자리에서 `repeated` 분기까지 도달해 같은 계약 행을 읽는다"는 것뿐이고, "계약이 halt라고 하지 않은 자리"라는 자기 전제도 T16의 escalate 값 자체도 독립적으로 검증하지 않는다.

**지적 4 — LOW · 계약의 세 번째 halt 행(`read.input-digest`)이 표에서 빠졌고, `_failure_verdict()`에 함수 단위 방어가 없다**
좌표: `contracts/stages/read.yaml:703` · `tests/test_m22_early_payload_assembly.py:138` · `engine/stages/read.py:1859`

계약의 halt 행은 셋이다: `read.schema` · `read.input-digest`(checks_on_entry) · `read.source-digest`. `HALT_CHECKS`에는 앞뒤 둘만 있다. 오늘은 `verify_declared_inputs()`가 findings 있는 행을 반환하지 않고 즉시 `StageEnvironmentError`를 던지므로 `read.input-digest`가 `_failure_verdict()`에 물리적으로 도달하지 않는다 — **현행 아키텍처에서는 안전**하다. 하지만 그 경로 분리를 보증하는 시험도, 함수 자체의 방어도 없다. 직접 호출하면: `("escalate", None)`(미반복) / `("escalate", "국면 간 변이 재현 — 코드 결함 의심")`(반복). `verify_declared_inputs()`가 훗날 예외 대신 fail 행을 반환하도록 리팩터되면 이 halt는 조용히 escalate로 바뀐다.

### [미검증]
- 실제 pytest 실행은 시도했으나 read-only 샌드박스에 사용 가능한 임시 디렉터리가 없어 `FileNotFoundError: No usable temporary directory`로 수집 전에 중단됨. 대신 순수 함수 프로브(`_failure_verdict` 직접 호출)와 `tools/check_validator_enforcement.py --json`(현재 기준선 PASS)으로 대체 확인.
- 리포 밖에 별도 배포된 오케스트레이터가 있는지는 확인 불가 — 이 체크아웃 안에서는 READ 상태(halt/escalate)를 소비하는 비시험 호출자를 찾지 못했다는 것까지만 확인.

### ANCHOR CHECK
`read.py:1848`(source-digest 분기 시작) · `1714`(재시도 루프의 failing 계산) · `read.py:523`(source_digest 강제 주입) · `read.yaml:255`(exit 판정점, `checks: checks_before_exit` — 예외 없음) · `read.yaml:709`(source-digest halt 행) · `read.yaml:703`(input-digest halt 행) · `source_digest.py`(동일 메모리 문자열 재해시 로직) · `SPEC.md:1332`(halt/escalate 정의) · `worst_status()` 위치(`engine/stages/__init__.py:101`) — 전부 직접 확인 완료, 인용 정확함. 나머지(테스트 파일 라인 138/144/164, D-1 관련)는 이번 요청 준비 단계에서 이미 원문 대조 완료.

### RECOVERY
해당 없음 — 턴이 정상 완료(`EXIT=0`), 회수 절차 불필요.

### SANDBOX
`read-only`(마커 불필요 — 정본 리포 직접, `--cd /home/laptop/projects/patent-docent`). 호출 문자열: `codex exec --model gpt-5.6-sol -c model_reasoning_effort=xhigh --sandbox read-only --skip-git-repo-check --cd /home/laptop/projects/patent-docent --json --output-last-message ... - < $SPEC`. `--add-dir` 미동반(read-only이므로 규정대로 생략). 실행 전후 `git status --short` 공백 확인 — 정본 무변경.
