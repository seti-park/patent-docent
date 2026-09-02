# 독립 감수 원문 — 라운드 A(재정 T22·T23·T24·T25 집행 · `aa9a734`) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(감사 stdout
전문 · 마지막 줄 `EXIT=0` 은 총괄 래퍼의 종료 마커다 · 원문 23,680 B).

**좌석 = opus max**(ROUTING **M9** 교차 벤더 — 저작이 sol-coder(GPT-5.6 Sol high) 였다). CLI 직구동
`claude -p --model opus --effort max` · `setsid` 배경 실행 + `EXIT=` 마커 + `/proc/<pid>` 폴링 ·
10:44 → 11:13(약 29분). 발주문 = 총괄(`AUDIT-ORDER-round-a.md` · 세션 스크래치).

**대상 커밋 = `aa9a734`**(19 파일 · 시험 561 · 관문 5종 × 2모드 exit 0). **읽기 전용 준수 확인** —
감사 전후 정본 트리 지문 `5a62d4f0c14570be44da51967950bfe902e8c42b` 동일 · `git status --porcelain`
0행(총괄 실측 · 감사자도 첫 줄에 같은 값을 신고했다). 프로브는 감사자의 클론
`/tmp/audit-round-a-x9` 에서만 돌았다.

**판정 = FAIL · 지적 8건(HIGH 1 · MED 3 · LOW 4).** 감사자의 요지 — *「네 재정의 실체는 전부
착지했다 … FAIL 의 사유는 구현이 틀렸다는 것이 아니라, 원장의 집행 조건 두 개가 「충족되었다」고
보고된 채 충족되지 않았다는 것」*. 두 자리(A-1 · A-3) 모두 **발주문 귀책**이며 저작 레인 귀책은
0건이다. A-1 은 재정 T19 §3 이 이미 벌한 형태(판별력 없는 반증 시험을 확인 없이 「통과」로 보고)의
**두 번째 발생**이다 — 총괄이 이번에도 시험이 **무엇을 흔드는지**를 실측하지 않고 변조 문자열을
발주문에 박았다.

지적 열거 = A-1, A-2, A-3, A-4, A-5, A-6, A-7, A-8

처분은 지적 처분 원장 `docs/decisions/DISPOSITIONS.md`(재정 T27) 에 행으로 서고, 사유의 전문은
`D-20260902-01-round-a.md` §5 에 있다. 요지 — **A-1 · A-3 · A-4 · A-5 · A-6 수용**(라운드 A′
수리 · sol-coder) · **A-2 수용**(CP1 §10 범위 표지 한 문장 — 렌더 재량 · Owner 사후 확인) · **A-7 부분
수용**(schema enum ↔ `read_runs` 결속 시험은 A′ · `canonical_selection.read_run` 의 enum 구속은
값 공간이라 상신) · **A-8 수용**(총괄 · 이 커밋의 인계문서 개정).

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

정본 리포는 손대지 않았다 — 감사 전후 트리 지문 `5a62d4f0c14570be44da51967950bfe902e8c42b` 동일, `git status` 0행. 모든 프로브는 `/tmp/audit-round-a-x9`(정본 클론)에서만 돌렸다.

---

# 판정 = **FAIL**

네 재정의 **실체는 전부 착지했다**. 561 passed(plain·`-O`)와 관문 5종 × 2모드 EXIT=0을 독립 재현했고, 되돌리기 프로브 6종 중 4종이 시험을 정확히 무너뜨렸다. **FAIL의 사유는 구현이 틀렸다는 것이 아니라, 원장의 집행 조건 두 개가 「충족되었다」고 보고된 채 충족되지 않았다는 것**이다 — 그중 하나는 이 리포가 **이미 재정 T19 §3으로 벌한 것과 정확히 같은 형태**다(*"역반증 시험이 … 구조적으로 재지 못한다. 총괄이 확인 없이 「통과」로 보고했다"*). 그것이 이번엔 T24 ②에서 재발했다.

두 자리 다 **발주문이 만든 것**이며 저작 레인의 이탈이 아니다.

---

## 1. 조건별 판정표

| 재정·조건 | 판정 | 근거 (좌표 · 재현) |
|---|---|---|
| **T22 ①** 처분이 자기 행에서 나온다 | **closed** | `read.py:1874-1907` 전용 분기 2. 프로브: 두 분기 삭제 → `1 failed, 2 passed in 0.22s`(`test_lane_log_verdicts_come_from_their_own_failure_rows`). 대조군(`read.verbatim` `then`→`halt`)이 움직이는 것까지 시험이 잰다 |
| **T22 ②** `retry(n)` 부재를 시험이 지키고 사유를 스스로 말한다 | **closed** | `read.yaml:743-759`. 프로브: `action: retry(1)` → `Failed: read.lane-log-shape 전용 행이 0회인 재시도를 선언했다: 'retry(1)'`. 전수로는 `3 failed, 558 passed` — **기존 `points_binding` 시험까지 함께 잡는다**(`test_m17_lanes.py::test_retry_budget_is_unchanged_by_the_split`). docstring이 「루프 밖 합류 → 0회」를 명시한다 |
| **T22 ③** `points` 부재가 `points_binding`과 무충돌 | **closed** | `1 passed, 560 deselected in 0.93s`(`test_retry_contract_declarations_are_bound_or_classified`) · 위 프로브가 역방향도 실증 |
| **T23 ①** 합집합 동일성 불변 + 귀속 | **closed** | dedupe 축 `(claim, dependency_type, text_verbatim)` 무변경(`run_checks.py:229-233`). 통주 실측: 같은 신고 → `[{"claim":"CL-3",…,"reported_by":["read-a","read-b"]}]` 1행 / 갈린 신고 → 2행 각 1원소 |
| **T23 ②** 스키마 거부 실증 | **closed** | 4제약 각각을 스키마에서 떼어내 4회 프로브 → 전부 `FAILED: 1/45 케이스가 기대와 어긋난다 (reject 29/30 · accept 13/13)` EXIT=1 |
| **T23 ③** 소급 방어 | **closed** | 실물 산출 `runs/openai-us20260147854a1-cim-fp-3/10-read/convergence.json`(미분류 1건 · 키 부재)을 현행 렌더에 물림 → 예외 없음, `'신고 실행:' 포함? False`. `runs/**`를 스키마로 검증하는 시험·도구는 없다(행위시법 보존) |
| **T23 ④** 고지 완전 제거 | **closed** | `grep -rn` 전수 — 코드·계약·SPEC 잔존 0. 남은 것은 원장 원문 2건과 `HANDOFF-NEXT.md`(→ A-8) |
| **T23 ⑤** 전수+관문 | **closed** | 561 passed / 관문 10줄 EXIT=0, 독립 재현 |
| **T24 ①** 출구 재독으로 halt | **closed** | 프로브: 재독을 메모리 사본으로 되돌림 → `2 failed`. 「무변조면 다른 출구 검사 불변」은 기존 548건 전건 통과가 진다 |
| **T24 ②** 재독은 출구에만 — **시험이 확인한다** | **open** | **→ A-1.** 조건을 위반해도(`run_early_claim_checks`에 디스크 재독 투입) **`561 passed`** |
| **T24 ③** `reader/lib` 무변경 | **closed(문언은 미충족)** | T24 귀속 변경 0. `reader/lib/run_checks.py`는 T23분이며 조건 문언(*"diff가 `reader/`를 건드리지 않는다"*)은 합본 라운드에서 문자 그대로는 만족 불가 — 보고에 명시되었어야 하나 안 되었다 |
| **T24 ④** 진단 3항 | **closed** | `source_digest.py:38-41`이 `extras["declared"]·["actual"]`을 실제로 채운다(`None` 아님). 런 산출물에도 남는다 — `convergence.json#findings`에 `expected`/`found`/`locus`/`rule` 전건 |
| **T25 ①** halt 행 실패 시 꼬리 레인 미발송 | **partially-closed** | 단독 실패는 닫혔다(프로브: 탈출 제거 → `read-a/ground-*/retry-1/…` 3건 재발송으로 실패). **복합 실패에서 깨진다 → A-3** |
| **T25 ②** `read.schema`의 `retry(1)→halt` 보존 | **closed** | `test_t25_read_schema_still_retries_once_before_halt` — 신설 시험이 재시도 정확히 1회를 잰다 |

---

## 2. 신규 지적

### A-1 · **HIGH** — T24 ②의 반증 시험이 반증하지 않는다 (전건 통과 아래의 공백)
**좌표** `tests/test_m21_retry_budget_by_judgment_point.py:106-119`(`MutateOnDecomposeAdapter`) · `:385-411` · 발주문 §2.3(변조 문자열을 지정한 자리)

발주문은 변조를 *"`patent.md` **끝에** 바이트를 덧붙인 뒤(숫자·단위가 없는 텍스트로 — 예 `\n<!-- mutated by test -->\n`)"*로 못 박았다. **그 변조는 조기 검사 어느 것도 읽지 않는 자리다** — 조기 검사는 `read.claim-inventory`·`read.dependency-parse` 둘뿐이고 둘 다 `find_claim_section()`이 잘라낸 **청구항 구간**만 본다(`reader/lib/inventory.py:54-73`). 문말 주석은 그 구간 밖이므로 **조기 판정 행은 어느 `source_text`를 쓰든 동일**하다. 즉 시험의 판별력이 0이다.

**재현**
```
① engine/stages/read.py:1509 의 조기 CheckContext 를 source_text → read_text(paths.patent_md) 로 (조건 ② 위반)
   .venv/bin/python -m pytest tests/ -q
   → 561 passed in 101.28s (0:01:41)          # 위반해도 전건 통과
② 위 위반 + 변조를 청구항 본문 안쪽으로 (25 cm3. → 25 cm3 (mutated).)
   → Failed: 분해 시점 원천 변경 최종 status 기대 halt, 실제 escalate
③ 같은 변조 · 정본 코드(조건 ② 준수)
   → 1 passed, 14 deselected in 1.54p
```
②가 원장 T24 ⒜가 예언한 오진(*"조기에 다시 읽으면 파일 변경이 분해 결함으로 오진된다"*)을 실물로 보여준다 — 그리고 시험은 그것을 잡을 수 있다. **못 잡게 만든 것은 변조 문자열 하나뿐**이다.

**왜 결함인가** 원장이 조건 ②에 붙인 술어가 *"시험이 확인한다"*이다. 확인하지 않는다. 그리고 이것은 **재정 T19 §3이 이미 처분한 형태의 두 번째 발생**이다. 수리는 한 줄(변조 앵커를 청구항 구간으로) + 조기 판정 행이 실제로 달라지는지의 양성 대조군 추가.

---

### A-2 · **MED** — CP1 판독본이 범위 표지 없이 항상 같은 귀속 한 값을 그린다
**좌표** `engine/render/material_spec_md.py:432-447`

출구 경로는 모든 행을 `canonical_run`으로 태그하므로(`read.py:1731-1732`) `convergence.json`의 `reported_by`는 **구조적으로 항상 `[정본]` 한 값**이다(총괄의 SPEC 「사실 정정」이 스스로 적은 사실). 그런데 판독본은 그 값을 항목마다 `신고 실행: read-a`로 찍으면서 **이 목록의 범위가 정본 실행 하나라는 말을 어디에도 하지 않는다** — 그 말을 하던 유일한 문단이 T23 ④로 삭제되었기 때문이다(구 문단도 「합집합」이라 틀렸으므로 삭제 자체는 옳다).

**결과** ⑴ 정보량 0의 줄이 전 항목에 붙는다 ⑵ 「`read-b`는 신고하지 않았다」로 읽힌다 — `read-b`는 애초에 이 판정서에서 **물어보지 않은** 실행이다. 이 리포는 같은 형태를 이미 입법했다: SPEC §1.5 `numeric_inventory` — *"**범위 표지가 문언의 일부다** — 구 문언 '전체 N건'은 어느 범위의 계수인지를 적지 않아 … 같은 문서 안의 두 수가 어긋난 채 읽혔다"*.

덧붙여 신설 렌더 시험은 `reported_by: ["read-a","read-b"]`를 먹인다(`tests/test_m22_unclassified_render_notice.py:38`) — **이 표면이 만들어낼 수 없는 상태**를 고정한 것이다.

총괄의 계류 상신(초안 §4 ★ 「CP1에 early 합집합을 그릴지」)은 이 지적을 **덮지 않는다**: Owner가 「그리지 않는다」로 재정해도 범위 표지는 여전히 필요하다. 수리는 절 머리 한 문장(*"이 목록은 정본 실행 <id>의 신고다. 두 실행이 갈린 신고는 `convergence-early.json`에 있다"*).

---

### A-3 · **MED** — T25의 「하나라도」가 단일 우선순위 행 조회로 축소되었다
**좌표** `engine/stages/read.py:1739-1741` · 발주문 §2.4(이 형태를 지정한 자리)

원장 T25 ⒜: *"**실패한 검사 중 하나라도** 그 계약 행이 `halt` 이고 `retry(n)` 이 없으면 …"*. 구현은 `_failure_entry_for`가 **우선순위로 고른 한 행**만 본다. `read.schema`(`action: retry(1)`)가 `read.source-digest`(`action: halt`)보다 앞서므로 **둘이 함께 실패하면 halt 행이 가려진다.**

**재현** (단위)
```
실패집합=['read.source-digest']              → 즉시 탈출? True
실패집합=['read.schema']                     → 즉시 탈출? False   (설계대로)
실패집합=['read.schema','read.source-digest'] → 즉시 탈출? False   ← 재정 위반
```
**재현** (통주 — 런 중 원천 변조 + 스키마 밖 키 1개)
```
Failed: A-3 확인 — halt 행(read.source-digest)이 실패했는데 정본 후속 레인이 다시 발송되었다:
['read-a/ground-independent/retry-1/batch-0', 'read-a/ground-dependent/retry-1/batch-0', 'read-a/synthesize/retry-1/batch-0']
```
원장 T24 ⒞가 고지한 바로 그 비용이다 — *"진짜 halt가 나야 할 자리에 재시도가 한 번 붙으면 레인 한 왕복을 버린다."* 최종 판정은 여전히 `halt`이므로 판정 오류는 아니고, **낭비 + 선언·실물 어긋남**이다.

**★ 라운드 B로 넘기는 주의** — T26 ⒜②의 `worst_status()` 격자는 이 자리를 **자동으로 고친다**. 그러면 T26 집행 조건 ②(*"오늘의 판정표 불변 증명"*)와 충돌한다. **이 한 칸은 「회귀」가 아니라 「의도된 교정」으로 골든 표에 명시**해야 한다. 명시하지 않으면 T26이 이 결함을 새 구조에 동결한다.

---

### A-4 · **MED** — 출구 재독이 IO 실패에 무방비다 (이번 라운드가 새로 연 통로)
**좌표** `engine/stages/read.py:1721`

`exit_source_text = read_text(paths.patent_md)`가 방어 없이 디스크를 친다. 파일이 사라진 순간에 걸리면 **`halt` 판정 + 진단 3항이 아니라 트레이스백으로 런이 죽는다.**

**재현**
```
Failed: A-4 확인 — 원천 삭제가 halt 판정이 아니라 예외로 터졌다:
FileNotFoundError: [Errno 2] No such file or directory: '…/00-source/patent.md'
```
T24 이전에는 출구가 디스크를 아예 읽지 않았으므로 **이 실패 모드는 이번 라운드가 만들었다**. 그리고 원장 T24 ⒞가 지목한 현실적 계기가 정확히 이것이다 — *"런 도중 원문 파일을 열어 저장하면 … **편집기의 자동 포맷도 포함된다**"*. 다수 편집기의 원자적 저장은 `write temp → rename`이라 **파일이 존재하지 않는 창**을 연다. 그 창에 걸리면 계약이 약속한 보호(폐기 판정 + 진단) 대신 스택 트레이스가 나온다. 수리는 `try/OSError` → `read.source-digest` fail 행 + 진단(`actual: "(읽을 수 없음: …)"`).

---

### A-5 · **LOW** — needle 유일성 시험이 자기 주장보다 좁다 (9개 중 7개)
**좌표** `tests/test_m23_lane_log_failure_rows.py:23-32`

시험 docstring은 *"**부분 문자열 조회의 모든 needle**이 정확히 한 행만 가리켜야"*라 말하는데, 목록은 `_failure_entry_for`의 7개뿐이다. 같은 표를 같은 방식으로 조회하는 **`read.py:1652 "claim-inventory"`·`:1658 "상신 축"`이 빠졌다.**

**재현** — `failure:` 맨 앞에 `condition: "가짜 행 — read.convergence 상신 축 관련 잡음" / action: halt` 한 행을 심고
```
--- 유일성 시험만 ---            1 passed in 0.14s          ← 통과한다
--- 실제 조회 ---  needle='상신 축' → condition='가짜 행 …' action='halt'   ← 가로채였다
```
전수로는 다른 시험 2건이 이 특정 변조를 잡으므로 실피해는 낮다. 그러나 **「강제의 범위를 실제보다 넓게 말했다」는 M0.6 재감수의 판정 요지 그 자체**이고, 시험 하나가 그 문장을 스스로 적고 있다. 수리 = `FAILURE_NEEDLES`에 2개 추가(둘 다 오늘 유일하므로 통과한다).

---

### A-6 · **LOW** — `retry_budget.points[id=exit].checks: checks_before_exit` 가 이제 거짓인데 그 좌표에 표지가 없다
**좌표** `contracts/stages/read.yaml:245-250`

계약은 출구 판정점이 `checks_before_exit` **전체**를 재시도한다고 선언하는데, T25 이후 러너는 `read.source-digest`를 제외한다. 사실 자체는 `failure:` 행 `note`와 SPEC 두 자리에 적혔으나, **계약이 정본이고 SPEC이 하류**라는 이 리포의 규율에서 정본 쪽 좌표에는 아무 표지가 없다. 발주문이 `retry_budget` 무접촉을 명했고 T26 ⒜③이 이 칸을 소유하므로 **이연이 옳다** — 다만 그 블록에 「T25가 이 선언의 예외를 만들었고 T26이 좁힌다」 한 줄 포인터는 라운드 B 전에 있어야 한다.

---

### A-7 · **LOW** — 독해 실행 id 어휘의 네 번째 사본이 무결속으로 생겼다
**좌표** `convergence.schema.json`(`reported_by` enum) ↔ `read.py:1398`(`read_runs` 기본 인자) ↔ `canonical_selection.read_run`(자유 문자열 `minLength 1`) ↔ `read.yaml`의 산문

총괄이 초안 §6-3에 **스스로 기록했다**(그 기록은 정확하다 · 재정 사항이라 손대지 않은 것도 옳다). 남는 문제는 둘 — ⑴ 넷을 잇는 관문이 **없다** ⑵ 주차지로 지목된 B-2·재정 T4는 **`lane_id`** 의 값 공간이라 다른 키다. 이 어휘는 자기 자리가 필요하다(T26 양방향 관문 또는 B-3 `extras` 등록부).

---

### A-8 · **LOW** — `HANDOFF-NEXT.md`가 끝난 일을 「지금 할 일」로 적고 있다
**좌표** `HANDOFF-NEXT.md:14`(*"지금 할 일 = 라운드 A 집행"*) · `:140`(*"결정되었으나 아직 집행 안 된 것 — 재정 T22·T23"*) · `:163`(삭제된 고지를 「딸린 조건」으로 인용)

발주문이 무접촉을 명했으므로 저작 레인 이탈이 아니라 **커밋 후 총괄 소관**이다. 적는 이유는 전례가 있어서다 — 직전 라운드 감수 C′-2가 P-5를 부분으로 채점한 사유가 정확히 *"상위 기록이 여전히 Owner 대기 상태로 남아 있다"*였다.

---

## 3. Q3 판정 — 발주자의 사실 정정

**⑴ 사실 주장은 참이다.** 코드로 확인했다.

| | 실물 |
|---|---|
| `convergence-early.json` | `early_rows = [entry_row, *early_claim_rows[canonical], *early_claim_rows[peer], early_row]`(`read.py:1534-1538`) → **두 실행 합집합** · 각 행은 자기 `read_run` 태그 |
| `convergence.json` | `run_read_checks(CheckContext(spec=canonical, …))` 단일 명세(`read.py:1722-1730`) + 전 행 `canonical_run` 태그 → **정본 신고만** |
| CP1 판독본 | `render(canonical, payload, …)`에서 `payload` = full → **full을 그린다** |

통주 실측이 뒷받침한다 — 두 실행이 갈린 신고를 내면 early에는 `[{CL-3 … ["read-a"]}, {CL-9 … ["read-b"]}]` 두 행이 서고, 그 런은 CP1에 도달하지도 않는다. **원장 T23 §1의 「CP1 목록 = 합집합」은 틀렸고 SPEC은 지금 참을 적고 있다.**

**⑵ 재량 분류 — 적정.** 사실 기록은 규율 11 ③이고, 값 공간(키·enum·필수)은 재정대로 두었으므로 규율 11 위반이 아니다. 그리고 **총괄은 「CP1에 early 합집합을 그릴지」를 실제로 상신했다**(초안 §4 ★ · 총괄 의견 + 편입 시점 제안 포함) — 헌장 §0의 상신 의무를 이행했다. *다만* 그 상신이 아직 리포 안에 없고(초안이 scratchpad에 있다), **상신의 계류가 A-2를 면제하지 않는다**: Owner가 어느 쪽으로 재정하든 오늘의 CP1 판독본에는 범위 표지가 없다.

---

## 4. Q5 여섯 판단

| # | 판단 | 판정 | 사유 |
|---|---|---|---|
| 1 | enum ↔ 자유 문자열 불일치를 관찰만 기록 | **적정** | 값 공간 변경은 재정 사항이고 기록은 정확하다. 다만 주차지가 어긋났다 → **A-7** |
| 2 | 진단 3항을 새 파일이 아니라 결과 dict에 | **적정** | *처음엔 모자람으로 봤다가 실측으로 뒤집었다* — 런 폴더에 `diagnostic` 파일은 없지만 `convergence.json#findings`가 `expected`/`found`/`locus`/`rule`을 이미 싣는다(실측 확인). 원장 ④의 「산출에 남는다」는 실물로 충족되고, 없는 것은 파일 경로 하나인데 그것은 고정값이다. 새 파일 = 런 레이아웃 = 계약 선언이라는 사유도 옳다 |
| 3 | `retry_budget` 무접촉 | **적정** | 발주문·T26 관할. **다만 그 블록의 선언이 오늘 거짓이다** → **A-6** |
| 4 | `to_convergence_payload` fail-closed(`ValueError`) | **적정** | 조용한 기본값 `[canonical]`이면 early 판정서가 **틀린 귀속**을 싣는다 — 침묵보다 나쁘다. 프로브로 하중을 확인했다: 엔진 태깅 2줄을 지우면 `19 failed, 542 passed`. 장식이 아니라 실제로 걸려 있다 |
| 5 | `reader/` 변경을 `run_checks.py` 하나로 · READER-VERSION 무상향 | **적정** | `material-spec.schema.json` 무접촉이므로 N15의 판 상향 사유가 아니고 T21 선례(`c3fe549`)와 같은 격이다. **리더** — `patent-historian` 체크아웃이 없어 CLAUDE.md §2의 상호 체크를 **수행하지 못했다**. 저작 레인이 보고했고 총괄이 초안 §7에 적었다. 그 「못 했다」가 리포 안 기록으로 남아야 한다(scratchpad는 사료가 아니다) |
| 6 | Q3 사실 정정을 재정 없이 기록 | **적정** | 위 §3 ⑵ |

**총괄이 감사에 넘긴 자기 관찰**(`repeated=True` + 레인 로그 단독 → 「같은 실패 서명」 행이 먼저 잡힌다) — **판단은 옳다. 도달 불능이다.** `repeated_signature`는 출구 루프 안에서만 True가 되고 그때 `failing`에는 반드시 루프 검사 실패가 들어 있는데, 루프 종료 후 `failing`은 **같은 `rows`** 위에서 재계산되므로 레인 로그 단독 집합이 될 수 없다. 다만 총괄이 초안 §6-4에 스스로 적었듯 **시험으로 고정하지 않고 감사에 넘긴 것**은 방어가 아니다 — 도달 불능이면 그 불변식을 한 줄로 잠글 수 있다(T26이 구조로 없애더라도 그때까지는 열려 있다).

---

## 5. Q6 — 저작 레인 GAPS 판정

| GAPS 항목 | 판정 |
|---|---|
| 시험 배치 3건(파일 선택) | **정당한 공학 재량.** 발주문이 *"파일은 새로 만들거나 …에 붙여도 된다"*로 명시 위임했다 |
| 무효 fixture 를 3~4건 중 **4건**으로 | **정당한 재량.** 발주문이 범위를 준 자리이고, 넓은 쪽을 골랐다 — 키 부재까지 포함한 것이 T23 ② 원문(빈 배열·미지 id·중복·**키 부재**)에 더 가깝다 |
| 렌더 시험 범위를 §10 절로 좁힘(`두 실행`이 §11 제목에 있어서) | **정당한 재량이며 옳다.** 전문 grep 이면 무관한 절 때문에 시험이 거짓 실패한다. 좁힌 사유를 명시했고 그 사유가 실물로 참이다 |
| 「발주문이 이미 확정해 판단하지 않은 것」 5건 | **분류가 정확하다.** 그중 **T25의 `_failure_entry_for` 우선순위 + `action == halt` 최소판**을 그대로 따른 것이 A-3인데, **이것은 blocked 반려 사유가 아니었다** — 결정 공백이 아니라 발주문이 **명시적으로 결정한 사항**이었고(§2.4가 코드를 문장 단위로 지정했다), 레인의 임무는 그것을 원장과 대조하는 것이 아니다. 같은 이유로 A-1의 변조 문자열도 발주문 지정값이다 |
| *"결과를 가르는 원장·발주문 불일치는 발견하지 않았다"* | **이 진술은 틀렸다** — A-1·A-3이 그 불일치다. 다만 **레인의 좌석 책임 밖**이다(발주문이 *"발주문이 실물과 어긋난 좌표·전제를 발견하면"*이라 적어 **실물 대조**만 요구했고, **원장 문언 대 발주문 문언**의 대조는 요구하지 않았다). 발주문의 결함이지 레인의 태만이 아니다 |

**총평** — GAPS는 정직하고 분류가 옳다. 저작 레인 귀책 지적 **0건**. 이번 라운드의 지적 8건은 **전부 발주문 또는 커밋 후 총괄 소관**이다.

---

## 6. Q2 — 명령되지 않은 부작용

**없다.** hunk 전건이 원장·발주문의 명시 항목에 대응한다. 확인한 것:

- **수집 시험 id 차분** — 기준선 548 → 대상 561, **신설 14 · 삭제 1**. 삭제 1건은 `test_unclassified_union_notice_states_the_attribution_limit`으로 T23 ④가 교체를 명한 그 시험이다. **몰래 지워진 시험 0건.**
- **`_failure_verdict` 동치** — `repeated` 갈래가 `entry["action"]` → `.get("then", .get("action"))`으로 바뀌었으나 「같은 실패 서명」 행에 `then`이 없어 결과 동일.
- **`extras` 누출 없음** — `to_row_dict()`가 `extras`를 싣지 않으므로 `read_run` 태그가 판정 행 서식에 새지 않는다(`reader/lib/report.py:103-114`).
- **행위시법 보존** — `runs/**`를 현행 스키마로 검증하는 시험·도구가 **없고**, 실물 산출(`cim-fp-3`)이 새 렌더 아래 예외 없이 그대로 선다. `runs/**` 무접촉.
- **조용한 거부·통과 전환 없음** — 새로 생긴 거부 경로는 `to_convergence_payload`의 fail-closed 하나이며 재정이 명한 것이다.

---

## 7. [미검증]

1. **`patent-historian` 상호 체크(CLAUDE.md §2)** — 체크아웃이 `/home/laptop/projects` 아래에 없다(직접 확인: `No such file or directory`). `reader/lib/run_checks.py`의 **새 하드 실패 모드**가 이식 상대에게 어떤 의미인지 판정하지 못했다. `reader/READER-VERSION` = `0.8.0` 무변경.
2. **A-3의 실특허 발화율** — `{read.schema, read.source-digest}` 동시 실패를 합성 표본으로만 재현했다. 실런 3건에는 전례가 없다. 「일어날 수 있다」는 증명했고 「얼마나 자주」는 못 쟀다.
3. **A-4의 편집기 창 폭** — 원자적 저장이 여는 무파일 창을 **논증했고 실측하지 않았다**. 삭제 시나리오로 실패 모드 자체는 실증했다.
4. **`escalate` + 별도 `reason_label` 로 needle 을 가로채는 A-5 변종** — `action: halt` 변종만 전수로 돌렸다(1건이 잡았다). 판별 불가능한 변종(같은 `action`, 다른 `reason_label`)은 전수를 돌리지 않았다. A-5 격을 LOW로 둔 근거가 그만큼 약하다.
5. **T24 ①의 「다른 출구 검사 결과가 한 건도 바뀌지 않는다」** — 기존 548건 전건 통과를 근거로 삼았고, 검사별 행 대조는 하지 않았다.

---

**처분 원장 등재용 요약** — `A-1`(HIGH · T24 ② 시험 무판별력) · `A-2`(MED · CP1 범위 표지) · `A-3`(MED · T25 「하나라도」 축소) · `A-4`(MED · 출구 재독 IO 무방비) · `A-5`(LOW · needle 7/9) · `A-6`(LOW · `retry_budget` exit 선언 표지) · `A-7`(LOW · 실행 id 어휘 네 번째 사본) · `A-8`(LOW · 인계문서 낡음). A-1·A-3은 **발주문 귀책**, A-8은 커밋 후 총괄 소관, 나머지는 라운드 A 산물.
EXIT=0
