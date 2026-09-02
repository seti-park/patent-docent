# 지적 처분 원장 (재정 2026-09-02 T27)

**지위 — 총괄 문서다. 원장이 아니다.** 재정의 상류 정본은 `docs/decisions/ruling-*.md` 이고
(`CLAUDE.md` §0 · 규율 9), 이 파일은 그 재정과 커밋이 이미 정한 처분을 **지적 하나에 한 행씩**
옮겨 적는 자리다. 여기 적힌 값이 원장·D 문서와 어긋나면 **원장·D 문서가 이긴다** — 이 표는
포인터를 들 뿐 처분을 창설하지 않는다.

**왜 이 자리가 필요했나.** 감수 원문은 `docs/lessons/` 에 전문 보존되고 재정은
`docs/decisions/` 에 가는데, *「지적 N → 처분 + 사유 + 포인터」* 를 한 행씩 적는 자리가 없었다.
실제 처분 기록이 **커밋 메시지**(`39286ca`·`c3fe549`)에만 남았고 — 검색이 안 되고 고칠 수도
없는 곳이다 — 그 결과 **지적 둘이 사유 없이 사라졌다**(sol 지적 1 앞절반 · sol 지적 4 뒷절반).
ROUTING §5 ⑼ *「처분 없이 사라진 지적은 없어야 한다」* 를 강제하는 기계가 이 리포에 없었다.
원장 = `ruling-20260902-01-T24-T27.md` **§T27**.

**처분 어휘는 넷뿐이다** — `수용` · `부분 수용` · `기각` · `이연`. 다른 값은 관문이 잡는다.
격은 감수 원문이 붙인 것(BLOCKER / HIGH / MED / LOW)을 그대로 옮기고, 원문이 격을 붙이지
않았으면 `—` 다. 사유는 한 줄이고 포인터는 **처분이 실제로 적힌 자리**(원장 파일 § · D 문서 § ·
커밋 해시)를 가리킨다 — 둘 중 하나라도 비면 관문이 실패한다.

**관문** = `tools/check_dispositions.py`. 상태 `등재` 파일의 **총괄 머리말 열거**와 아래 §1
처분표를 **양방향 차집합 0** 으로 대조한다. 규격 정본 = `docs/SPEC.md` §8.3 11항.

**`RULINGS-LEDGER.md` §2 의 「감수 원문」 표와 이 표는 층이 다르다.** 그 표는 **파일 단위**의
색인이며 회수분의 **격**(`complete`·`recovered`·`partial`)을 든다(재정 2026-08-19 S8). 이 표는
**지적 단위**의 처분을 든다. 파일이 리포에 도착했는가와 그 안의 지적이 닫혔는가는 다른 사건이고,
전자가 있어도 후자는 새어 나갔다.

**★ 관문이 주장하지 않는 것.** 머리말의 열거가 감수 원문의 지적을 **빠짐없이** 담았는지는
기계가 모른다. 그것은 **반입 시점의 사람**이 지킨다(원장 T27 ⒜ ① — 지적을 앞/뒷절반으로
쪼개는 판단도 주의가 가장 높은 그 순간에 일어난다).

---

## §0 등재 현황 — `docs/lessons/` 전 파일

상태 어휘는 둘이다. **`등재`** = 머리말에 지적 id 를 열거하고 §1 에 처분 행을 갖는다.
**`선행 종결`** = PD-M1 종결 이전의 감수로, 지적 단위 처분이 **그 시기의 총괄 문서**(PD-M1
종결 판정표·D 문서)에서 이미 닫혔다 — 포인터가 필수이고 §1 에 행을 갖지 않는다.

★ 재정 T27 ⒞ 는 소급 대상을 *「기존 감수 원문 4~5건」* 으로 적었다. 그 수가 가리키는 것은
**PD-M2 시기(2026-09-01 이후) 반입분**이며, PD-M1 시기 12건은 종결 판정표가 지적 단위 처분을
이미 실었으므로 `선행 종결` 로 두고 그 포인터를 적는다.

| 파일 | 상태 | 포인터 |
|---|---|---|
| 2026-08-17-sol-audit-m0-full.md | 선행 종결 | `D-20260817-01-sol-audit-m0.md` §1~§4 · 전량 처분표 = `D-20260817-02-spec-revision-m05.md` §2 · M20·M21 = `D-20260818-01-m06-enforcement.md` §3 |
| 2026-08-17-sol-audit-m05-full.md | 선행 종결 | `D-20260817-02-spec-revision-m05.md` §7.1 처분 분류 · A군 13건 집행 = `D-20260818-01-m06-enforcement.md` §2 |
| 2026-08-18-sol-audit-m06-full.md | 선행 종결 | `D-20260818-01-m06-enforcement.md` §5.1·§5.2 |
| 2026-08-18-sol-audit-m1-full.md | 선행 종결 | `D-20260818-03-m1-audit.md` §1 처분 요약·§2 · 이행 = `D-20260818-04-m1-close.md` §1 |
| 2026-08-18-sol-audit-m15-full.md | 선행 종결 | `D-20260818-04-m1-close.md` §5 · 부분 8건 잔여 = `D-20260819-01-m16-close.md` §2 |
| 2026-08-19-sol-audit-m17-full.md | 선행 종결 | `D-20260819-02-m17-close.md` §7.1~§7.7 · 잔여 보수 = `D-20260819-03-m18-close.md` §2 |
| 2026-08-19-sol-audit-m17-Aprime-recovered.md | 선행 종결 | `D-20260819-02-m17-close.md` §7.1(A′ 의 지적과 그 처분) · 격 `partial(events)` = `RULINGS-LEDGER.md` §2 감수 원문 표 |
| 2026-08-19-sol-audit-m17-C1prime-recovered.md | 선행 종결 | `D-20260819-02-m17-close.md` §7.2 · 격 `partial(events)` = `RULINGS-LEDGER.md` §2 감수 원문 표 |
| 2026-08-19-sol-audit-m17-C2prime-recovered.md | 선행 종결 | `D-20260819-02-m17-close.md` §7.5·§7.6(C′-2 지적의 처분) · 격 `recovered(resume)` = `RULINGS-LEDGER.md` §2 |
| 2026-08-19-sol-audit-m17-D-recovered.md | 선행 종결 | `D-20260819-02-m17-close.md` §7.7 · 격 `recovered(resume)` = `RULINGS-LEDGER.md` §2 |
| 2026-08-19-sol-audit-m18-full.md | 선행 종결 | `D-20260819-03-m18-close.md` §5 P-11 항목별 판정표·§6 신규 지적과 그 처분 |
| 2026-08-31-sol-audit-m19-full.md | 선행 종결 | `D-20260831-01-m19-close.md` §5·§6 · 종결 요건 대조표 = 같은 문서 §10 |
| 2026-09-01-fable-advice-g6-defect-ownership.md | 등재 | — |
| 2026-09-01-opus-audit-g6-implementation.md | 등재 | — |
| 2026-09-01-opus-audit-t17-repair.md | 등재 | — |
| 2026-09-01-sol-audit-halt-ordering.md | 등재 | — |
| 2026-09-01-sol-review-g6-retry-budget.md | 등재 | — |
| 2026-09-02-opus-audit-round-a.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design.md | 등재 | — |

**계수** — `등재` **7** · `선행 종결` **12** · 합 **19**(`docs/lessons/` 전 파일).

---

## §1 처분표

| 파일 | 지적 id | 격 | 처분 | 사유 | 포인터 |
|---|---|---|---|---|---|
| 2026-09-01-fable-advice-g6-defect-ownership.md | V | — | 수용 | 판정 (c) = 「(a) + 출구 존치」 → 재정 T16 ⓐ 그대로 채택. 자문의 근거 하나(「유일한 탐지기」·「탐지조차 안 되는 결함으로 격하」)는 뒤에 반증되었으나 **처분은 유지**되고 근거만 세 격으로 교체되었다(총괄 정정 — 자문 본문 무접촉) | `ruling-20260901-07-T16.md` §2 ⒜ · `D-20260901-01-pdm2-split.md` §10 · 그 파일 말미 총괄 추기 절 |
| 2026-09-01-opus-audit-g6-implementation.md | X-1 | BLOCKER | 수용 | `vacuous_pass` 를 첫등장순 보존 중복제거 — 조기 국면이 같은 검사를 실행 수만큼 싣는데 두 행이 함께 공허하면 `uniqueItems` 위반으로 판정서가 아예 안 쓰였다 | 커밋 `39286ca` 메시지(BLOCKER 2) · 닫힘 판정 = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | X-2 | BLOCKER | 수용 | 미분류 청구항 문언을 정본 명세가 아니라 자기 명세에서 든다(`extras.unclassified_detail` 신설) — 비정본의 ID 를 정본에서 찾아 빈 문언이 났다. ★ 명명된 시나리오만 닫혔고 뿌리는 신규 지적 `Y-1` 로 이어졌다 | 커밋 `39286ca` · 판정 `partially-closed` = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | X-3 | HIGH | 수용 | `unclassified_dependents` 를 덮어쓰기 → 합집합 누적. 정본 신고분이 소실·오귀속됐다 | 커밋 `39286ca` · 판정 = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | B-1 | HIGH | 수용 | 예산 거부 경로가 무시험이었다(두 거부를 지워도 전건 통과). 반증 시험 신설 | 커밋 `39286ca` 메시지(HIGH 2) · 프로브 P-A = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | A-1 | MED | 수용 | 계약이 `read.convergence` 를 `phases: [exit]` 로 적었는데 실물은 조기에도 돈다. 시험이 계약과 코드를 상호 대조하도록 고쳤다(상수 재기입 제거) | 커밋 `39286ca` 메시지(MED 5) · 프로브 P-I = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | C-1 | MED | 수용 | 수렴을 한 번도 실행하지 않고 통과하던 시험 — 갈림 표본 + `executed` 단언 | 커밋 `39286ca` · 프로브 P-J2 = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | C-2 | MED | 수용 | Owner '계속' 봉투의 적용 범위가 청구항 소유 실패까지 조용히 넓어진 것 → 재정 T17 로 처분(`ENVELOPE_SCOPE` 단일 진원 + `10-read/phase-gate.json` 신설) | `ruling-20260901-08-T17.md` · 커밋 `39286ca` |
| 2026-09-01-opus-audit-g6-implementation.md | B-2 | MED | 수용 | 되먹임 비누설 시험이 상대 실행의 검사 소견 전달을 잡지 못했다 — 두 실행이 함께 실패하는 표본으로 공백을 메웠다 | 커밋 `39286ca` · 프로브 P-K = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | D-1 | MED | 수용 | Q7 후계 가드가 세탁 가능했다 — `failure` 행에 `points` 태깅 + 판정점 정확 상등 대조 | 커밋 `39286ca` · 프로브 P-B·P-B2 = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-g6-implementation.md | C-3 | LOW | 수용 | 계약이 halt 를 정한 행이 `repeated` escalate 뒤에 서 있었다. ★ 감사는 `read.schema` 하나를 지목했으나 결함은 계열이라 `read.source-digest` 도 함께 고쳤다(확대 집행) — 그 확대가 뒤에 sol 감사의 반대 판정을 불렀다 | 커밋 `39286ca` · 판정 `closed(확대 집행)` = `2026-09-01-opus-audit-t17-repair.md` §2 · 반대 판정 = `2026-09-01-sol-audit-halt-ordering.md` |
| 2026-09-01-opus-audit-g6-implementation.md | A-2 | LOW | 수용 | 러너가 읽지 않던 선언을 결속했다(`assembler_inputs`/`spec_fields` 분리 · `checks`·`scope`·`repairs` 를 행동에 · `binding_status` 합집합 강제). ★ 원문 판정표는 `A-2/A-3` 를 한 행으로 묶었고 처분도 하나다 | 커밋 `39286ca` · 잔여 = `Y-3`(`2026-09-01-opus-audit-t17-repair.md` §3) |
| 2026-09-01-opus-audit-g6-implementation.md | A-3 | LOW | 수용 | `A-2` 와 한 행의 같은 처분 — 러너가 읽지 않던 선언의 결속. ★ 원문 판정표가 `A-2/A-3` 로 묶어 적은 자리를 id 하나에 한 행이라는 이 표의 서식에 맞춰 나눈 것이며 값은 나누지 않았다 | 커밋 `39286ca` · 잔여 = `Y-3`(`2026-09-01-opus-audit-t17-repair.md` §3) |
| 2026-09-01-opus-audit-g6-implementation.md | E-2 | LOW | 수용 | 반증된 전제(「유일한 탐지기」)를 코드 주석·시험 docstring·원장 색인 행 셋에서 정정했다. 원장 원문은 무접촉 — 그건 원장이고 셋은 아니다 | 커밋 `39286ca` · 잔존 1곳 = `Y-5`(`2026-09-01-opus-audit-t17-repair.md` §3·§6 ⑶) |
| 2026-09-01-opus-audit-g6-implementation.md | F-2 | LOW | 수용 | 직전 커밋 메시지의 시험 계수가 기준선·증분 둘 다 오기였다(커밋 메시지는 고칠 수 없다). ★ 그 처분으로 이후 메시지는 계수를 적지 않는다 | 커밋 `39286ca` · 판정 = `2026-09-01-opus-audit-t17-repair.md` §2 |
| 2026-09-01-opus-audit-t17-repair.md | Y-1 | BLOCKER | 수용 | 짝 필드 `text_status`(`verbatim` 또는 `absent`) 신설 + 고정 토큰 «문언 없음» — 스키마가 양방향 강제하고 `minLength: 1` 은 유지되며 항목은 목록에 남는다(신호 보존). 소급 없음 | `ruling-20260901-09-T18-T20.md` §T18 · `ruling-20260901-10-T21.md`(T18 개정) · 커밋 `c3fe549` |
| 2026-09-01-opus-audit-t17-repair.md | Y-2 | MED | 수용 | 조건 ②(역반증) 시험이 상신 축만 돌아 「좁힘이 과했는가」를 구조적으로 드러낼 수 없었다 → T19 = `exact-match` 축 배제의 **사후 추인 + 절차 위반 등재**, 시험은 두 축으로 | `ruling-20260901-09-T18-T20.md` §T19 · 커밋 `c3fe549` |
| 2026-09-01-opus-audit-t17-repair.md | Y-3 | MED | 수용 | A-2/A-3 를 처분한 커밋이 만든 새 무결속 선언 — `blocked_by_vocabulary` + `binding_status` 신설, 시험이 실물·코드와 정확히 상등 대조 | 커밋 `c3fe549` 메시지 「감사 잔여」 |
| 2026-09-01-opus-audit-t17-repair.md | Y-4 | LOW | 수용 | 도달 불능 라벨 삭제 → 불변식 위반 시 `RunnerContractError`. 「있는 척」을 제거했다 | 커밋 `c3fe549` 메시지 「감사 잔여」 |
| 2026-09-01-opus-audit-t17-repair.md | Y-5 | LOW | 수용 | E-2 정정의 마지막 한 곳(`fable-advice:69`)이 자문 원문이 아니라 총괄 자신의 추기였다 — 총괄 추기 절 **안**에서 정정하고 자문 본문은 무접촉 | 커밋 `c3fe549` · `2026-09-01-fable-advice-g6-defect-ownership.md` 말미 총괄 추기 절 |
| 2026-09-01-opus-audit-t17-repair.md | Y-6 | LOW | 수용 | 판정서 서식으로는 불가함을 실측으로 확인(항목·최상위 양쪽 `additionalProperties: false`) → 상신 회부 → 재정 T23 이 `unclassified_dependents.items.reported_by` 를 신설 | `ruling-20260901-11-T22-T23.md` §T23 · 커밋 `c3fe549`(렌더 고지) · 커밋 `aa9a734`(T23 집행) |
| 2026-09-01-sol-audit-halt-ordering.md | 1a | MED | 수용 | halt 단독 행 검사(`read.source-digest`)가 출구 재시도 루프를 탄다 → 재정 T25 「하나라도 halt·무재시도면 즉시 탈출」. 라운드 A 집행 + 「하나라도」 술어는 라운드 A′(감사 A-3) | `ruling-20260902-01-T24-T27.md` §T25 · 커밋 `aa9a734` · `D-20260902-01-round-a.md` §5 A-3 |
| 2026-09-01-sol-audit-halt-ordering.md | 1b | MED | 수용 | 출구 `read.source-digest` 가 메모리 캡처본을 다시 해시해 디스크 변경을 못 잡는다는 반증이 맞다 → 재정 T24 출구 재독(디스크에서 다시 읽어 대조) + 진단 3항 | `ruling-20260902-01-T24-T27.md` §T24 · 커밋 `aa9a734` |
| 2026-09-01-sol-audit-halt-ordering.md | 2 | MED | 수용 | 두 갈래 — 레인 로그 2종의 실패 조건이 계약에 없다 → 재정 T22 전용 실패 행(집행 `aa9a734`) · 복수 동시 실패의 우선순위가 코드에만 있다 → 재정 T26 실패표 재구성(채택 · **미착수** — M1b 설계 도전 FAIL 로 Owner 재정 대기) | `ruling-20260901-11-T22-T23.md` §T22 · `ruling-20260902-01-T24-T27.md` §T26 · 커밋 `aa9a734` · `D-20260902-02` §3 |
| 2026-09-01-sol-audit-halt-ordering.md | 3 | MED | 수용 | `HALT_CHECKS` 수기 표 폐기 → `contract_halt_partitions()` 로 계약 `failure[]` 에서 파생 · 공허 시 skip 아닌 fail · 역대조 시험에 「계약이 halt 라 하지 않았다」는 전제 검사 추가 | 커밋 `c3fe549` 메시지 「감사 잔여」 · `tests/test_m22_early_payload_assembly.py`(`contract_halt_partitions` · `test_repeat_escalation_still_applies_where_the_contract_did_not_say_halt`) |
| 2026-09-01-sol-audit-halt-ordering.md | 4a | LOW | 수용 | `read.input-digest` 가 표에서 빠진 문제는 표의 계약 파생으로 자동 해소(진입 갈래에 실재함을 실행 확인) | 커밋 `c3fe549` 메시지 「감사 잔여」 · `tests/test_m22_early_payload_assembly.py`(진입·판정 두 갈래 분할 시험) |
| 2026-09-01-sol-audit-halt-ordering.md | 4b | LOW | 수용 | `verify_declared_inputs` 실패 행 → `read.input-digest` 전용 실패 행(`halt` · 「환경 오류」) 이 T26 격자에서 구조로 서면 함수 리팩터로 halt 가 조용히 바뀌는 경로가 닫힌다. 이행 = 라운드 B(T26 · 미착수) | `ruling-20260902-01-T24-T27.md` §T27 §1 · 라운드 B 커밋(병합 뒤 총괄이 해시 보완) |
| 2026-09-01-sol-review-g6-retry-budget.md | R | — | 수용 | 판정점별 유한 예산(조기 `retry(1)` + 정본 후속 `retry(1)`) → 재정 T16 ⒝ 예산(조기 = 레인별 1 · 후속 1) | `ruling-20260901-07-T16.md` §2 ⒝ · §3 부속 2 |
| 2026-09-01-sol-review-g6-retry-budget.md | C-a | — | 수용 | 조건 (a) 「분해 소유 검사를 조기 지점으로 옮겨 분해 레인에 되먹인다」 → T16 ⓐ (c) = 조기 이동 **+ 출구 존치** 로 채택(출구 행을 없애는 「(a) 순수형」만 기각 — 그 순수형은 총괄의 해석이었다) | `ruling-20260901-07-T16.md` §2 ⒜ · §5 |
| 2026-09-01-sol-review-g6-retry-budget.md | C-b | — | 기각 | 조건 (b) 「분해→수렴→tail 전체 재개방」 — 청구항 결함 하나에 레인 6회 · 재개방 조건·횟수·`attempt` 리셋이라는 새 경계 · 귀속 지연 | `ruling-20260901-07-T16.md` §5 |
| 2026-09-02-opus-audit-round-a.md | A-1 | HIGH | 수용 | 재정 T19 §3 이 벌한 형태의 **두 번째 발생** · 발주문이 변조 문자열을 지정했다(총괄 귀책). 수리 = 변조 앵커를 청구항 본문 안으로 + 위반 시 조기 판정 행이 실제로 달라지는 **양성 대조군** | `D-20260902-01-round-a.md` §5 · 라운드 A′ 발주문 §1 A-1 · A′ 커밋 |
| 2026-09-02-opus-audit-round-a.md | A-2 | MED | 수용 | SPEC §1.5 「범위 표지가 문언의 일부다」 가 이미 입법 · §4 ★ 상신(조기 합집합)이 어느 쪽으로 나도 표지는 필요. 수리 = §10 절 머리 한 문장 + 시험을 생산 가능한 상태로. **렌더 재량이나 CP1 표면이라 Owner 사후 확인**(§6-5) | `D-20260902-01-round-a.md` §5 · A′ §1 A-2 |
| 2026-09-02-opus-audit-round-a.md | A-3 | MED | 수용 | 원장 T25 ⒜ 문언 위반 · 발주문 §2.4 가 그 코드를 지정했다(총괄 귀책). 수리 = 즉시 탈출 판별을 **실패 검사별** halt 행 조회의 `any` 로 + 단위·통주 시험. ★ T26 골든은 **이 수리 뒤 커밋**에서 생성하므로 감사가 경고한 「회귀 vs 의도된 교정」 충돌이 생기지 않는다 | `D-20260902-01-round-a.md` §5 · A′ §1 A-3 · `D-20260902-02` §2 B-3 |
| 2026-09-02-opus-audit-round-a.md | A-4 | MED | 수용 | 이 라운드가 새로 연 실패 모드 · 원장 T24 ⒞ 가 지목한 계기(편집기 저장) 그 자체. 수리 = `OSError` → `read.source-digest` 실패 행 + 진단 `actual` 에 「읽을 수 없음」 + 삭제 시험 | `D-20260902-01-round-a.md` §5 · A′ §1 A-4 |
| 2026-09-02-opus-audit-round-a.md | A-5 | LOW | 수용 | 「강제의 범위를 실제보다 넓게 말했다」 계열. 수리 = `FAILURE_NEEDLES` 에 `claim-inventory`·`상신 축` 추가 | `D-20260902-01-round-a.md` §5 · A′ §1 A-5 |
| 2026-09-02-opus-audit-round-a.md | A-6 | LOW | 수용 | 값은 T26 ⒜③ 소관이라 무접촉 유지 · 표지는 **YAML 주석 한 줄**(파싱 결과 무변경 · `test_retry_budget_is_unchanged_by_the_split` 무영향) | `D-20260902-01-round-a.md` §5 · A′ §1 A-6 |
| 2026-09-02-opus-audit-round-a.md | A-7 | LOW | 부분 수용 | enum ↔ `read_runs` 결속은 **시험 한 줄**(재량 · A′). `canonical_selection.read_run` 을 같은 enum 으로 묶는 것은 스키마 값 공간 → **상신**(§6-5 · 총괄 의견 = 묶는다 · 행위시법) | `D-20260902-01-round-a.md` §5 · A′ §1 A-7 · 같은 문서 §6-5 |
| 2026-09-02-opus-audit-round-a.md | A-8 | LOW | 수용 | 커밋 후 총괄 소관. 그 커밋에서 `HANDOFF-NEXT.md` §0 재작성 · §2 정정 마커 · §5 순서도 갱신 | `D-20260902-01-round-a.md` §5 A-8 · 커밋 `f46698e`(그 표의 「이 커밋」) |
| 2026-09-02-sol-challenge-t26-design.md | B-1 | BLOCKER | 이연 | 처분 원문은 「이연 → 재정 상신」이다. 상류 두 재정(P-4 · T26 §3 ②)이 충돌하는 자리 — 총괄이 어느 쪽을 접어도 재정 침범. 선택지·추천 = §3 ★1 | `D-20260902-02-t26-design-challenge.md` §2 · 상신 = 같은 문서 §3 ★1 |
| 2026-09-02-sol-challenge-t26-design.md | B-2 | BLOCKER | 부분 수용 | 처분 원문은 「부분 수용 — 앞절반 수용 · 뒷절반 재정 상신」이다. 앞절반(분모 12 · 8,190칸 전수 · 총괄이 `read.source-digest` 와 레인 로그 2종을 빠뜨렸다)은 설계 오류 → v2. 뒷절반(「오늘의 표」의 영역에 진입 검사가 드는가)은 T26 §3 ② 의 해석 = 재정 → §3 ★2 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 · 상신 = 같은 문서 §3 ★2 |
| 2026-09-02-sol-challenge-t26-design.md | B-3 | BLOCKER | 수용 | 검증 설계 원리 위반 — 총괄이 §5-4 에서 스스로 의심하고도 「제어 흐름이 다르니 된다」고 판단했다. v2 = **기준 커밋 골든 동결**: 공식 검사 id 목록 · 비공집합 × repeated 전건의 `(action, reason_label)` · 기준 커밋 해시 · 생성 절차를 픽스처 파일로 리포에 넣고 시험은 그 파일만 읽는다. ★ 기준 커밋 = **라운드 A′ 뒤 커밋** | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 |
| 2026-09-02-sol-challenge-t26-design.md | B-4 | BLOCKER | 수용 | 원장 등식을 바꾸는 것은 허용되지 않는다. v2 = 통합 행을 **판정점 기준으로 분리** · 관문은 교집합 없이 원장 식 그대로 · `phase` 는 「그 판정점에서 실제 실행되는가」만 별도 검증. 행 분리는 (조치, 라벨) 표를 바꾸지 않으며 골든(B-3)이 그것을 증명한다 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.1 · §2.5 |
| 2026-09-02-sol-challenge-t26-design.md | B-5 | HIGH | 수용 | 총괄이 §5-5 에서 관문만 보고 「닫혔다」고 판단했다. v2 = `terminal_action()` 이 `action: retry(n)` 에 유효 `then` 필수 · `then` 어휘 3종 · `worst_status` 호출 **전** 검증 · 위반 시 `StageError` · 두 변조 시험 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.4 |
| 2026-09-02-sol-challenge-t26-design.md | B-6 | HIGH | 부분 수용 | 처분 원문은 「부분 수용 — 뒷절반 수용 · 앞절반 해석 상신」이다. 뒷절반: v2 = upstream 행에 **식별 키만** · 호출자 만들지 않음 명시 · binding `deferred/test_bound`. 앞절반: 「`checks` 의무는 검사 실패 행에만, 세 행은 `kind`」 는 원장 문언의 해석이라 **Owner 확인** → §3 ★3 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.1 · 상신 = 같은 문서 §3 ★3 |
| 2026-09-02-sol-challenge-t26-design.md | B-7 | MED | 수용 | v2 수용 기준 = 전수 pytest(plain · `PYTHONOPTIMIZE=1`) · 기존 5 + 신설 1 관문 plain · 같은 6 관문 `-O` · 각 명령과 기대 exit | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 |

**행 수 = 45**(`등재` 7파일의 지적 전건).

---

## §2 이 표에 아직 서지 못한 것 — 처분 대기

**처분이 기록에 없거나 총괄이 id 를 세우지 않은 지적은 이 표에 넣지 않는다.** 값을 지어내는
것이 비어 있는 것보다 나쁘기 때문이다(처분 어휘 4종 중 하나를 저작자가 고르면 그것은 기록이
아니라 창작이다). 아래는 발주자·총괄이 처분 또는 id 를 정한 뒤 §1 로 올라간다.

| 파일 | 자리 | 무엇 | 무엇이 비었나 |
|---|---|---|---|
| 2026-09-01-opus-audit-t17-repair.md | §6 소견 ⑴ | 레인이 정본 트리에서 `git apply -R` 로 역프로브를 도는 방식은 안전하지 않다 — 프로브 레인에 정본 트리 쓰기 권한을 주지 말 것(권고) | **처분 기록** — `docs/decisions/` 전문 검색에서 이 소견의 처분을 찾지 못했다(D 문서·원장·`D-20260902-02` §5 발주문 골격 개정 ⑹~⑻ 어디에도 없다). 원문이 id 도 붙이지 않았다 |
| 2026-09-01-opus-audit-t17-repair.md | §6 소견 ⑵ | 규율 10 의 판별선은 「파일」이 아니라 「저자·절」이어야 한다 | **id** — 처분은 있다(재정 T20 = 규율 10 개정 + 다섯째 관문). 원문이 id 를 붙이지 않았고, 원문에 없는 id 를 세우는 것은 총괄 재량이라(Owner 사후 확인 대상) 저작 레인이 정하지 않는다 |

**세우지 않기로 이미 정해진 것** — 같은 파일 §4 Q2 의 판정 3건(총괄 자기 계상에 대한 감사자의
채점이지 지적이 아니다)과 §6 소견 ⑶(E-2 전파 전수 — 그 잔여는 `Y-5` 로 이미 §1 에 서 있다).
