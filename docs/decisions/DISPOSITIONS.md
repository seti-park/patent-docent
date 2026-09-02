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

**[추기 2026-09-02 · 감사 C-6]** 관문이 보지 않는 것은 그것만이 아니다 — **포인터가 실재하는가 · 사유가 뜻이 통하는가 ·
`선행 종결` 이 사실인가**도 기계가 모르며 사람이 지킨다(관문은 비공백만 본다 — `이연 / TBD / TBD` 는 통과한다).
**[정정 2026-09-02 · 감사 C-1]** 「처분을 창설하지 않는다」에는 예외 하나가 있다 — 재정 T27 ⒞ 가 소급 등재분의 처분을
**등재 시점에 사유와 함께 적으라** 했으므로 그 행(`sol-audit-halt-ordering` 4b)은 이 표가 처분을 처음 적은 자리다. 그 값을 정한 것은
총괄 발주문이고(실체는 재정 T29 ⓐ 가 확정) Owner 사후 확인 대상이다(`D-20260902-03` §2 ⑸).

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
| 2026-09-02-sol-challenge-t26-design-v2.md | 등재 | — |
| 2026-09-02-fable-advice-t26-design-v3.md | 등재 | — |
| 2026-09-02-sol-audit-round-c.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v4.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v5.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v6.md | 등재 | — |

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
| 2026-09-01-opus-audit-t17-repair.md | S-1 | — | 수용 | §6 소견 ⑴ — 레인이 정본 트리에서 `git apply -R` 로 역프로브를 도는 방식. 감수 레인 규격(SPEC §8.3 9항 ⓐ · 재정 S5 · Q9 ⓐ 「검사자에게 쓰기를 주면 격리 사본에서만」)의 적용 범위를 **저작 레인의 역프로브까지** 발주문이 명시한다 → 발주문 골격 **⑼** 신설. 값 공간이 아니라 실행 환경 규약(규율 11 ③). ★ id 는 원문에 없고 총괄이 세웠다(사후 확인) · 처분도 이 자리가 처음이다 | `D-20260902-03-round-c.md` §3 · `D-20260902-02-t26-design-challenge.md` §5 골격 ⑼ |
| 2026-09-01-opus-audit-t17-repair.md | S-2 | — | 수용 | §6 소견 ⑵ — 규율 10 의 판별선은 「파일」이 아니라 「저자·절」. 재정 T20 이 규율 10 을 개정하고 다섯째 관문 `check_lesson_authorship.py` 를 세워 **이미 집행**되었다 — 이 자리에 비어 있던 것은 처분이 아니라 id 였다. ★ id 는 원문에 없고 총괄이 세웠다(사후 확인) | `ruling-20260901-09-T18-T20.md` §T20 · `D-20260902-03-round-c.md` §3 |
| 2026-09-01-sol-audit-halt-ordering.md | 1a | MED | 수용 | halt 단독 행 검사(`read.source-digest`)가 출구 재시도 루프를 탄다 → 재정 T25 「하나라도 halt·무재시도면 즉시 탈출」. 라운드 A 집행 + 「하나라도」 술어는 라운드 A′(감사 A-3) | `ruling-20260902-01-T24-T27.md` §T25 · 커밋 `aa9a734` · `D-20260902-01-round-a.md` §5 A-3 |
| 2026-09-01-sol-audit-halt-ordering.md | 1b | MED | 수용 | 출구 `read.source-digest` 가 메모리 캡처본을 다시 해시해 디스크 변경을 못 잡는다는 반증이 맞다 → 재정 T24 출구 재독(디스크에서 다시 읽어 대조) + 진단 3항 | `ruling-20260902-01-T24-T27.md` §T24 · 커밋 `aa9a734` |
| 2026-09-01-sol-audit-halt-ordering.md | 2 | MED | 수용 | 두 갈래 — 레인 로그 2종의 실패 조건이 계약에 없다 → 재정 T22 전용 실패 행(집행 `aa9a734`) · 복수 동시 실패의 우선순위가 코드에만 있다 → 재정 T26 실패표 재구성(채택 · **미착수** — M1b 설계 도전 FAIL 로 Owner 재정 대기). **[추기 2026-09-02]** 도전이 남긴 재정 세 자리는 T28~T30 으로 닫혔고 설계 v2 → M1b 재도전으로 간다 — T26 §3 ①(PASS 전 착수·커밋 금지)은 그대로 살아 있다 | `ruling-20260901-11-T22-T23.md` §T22 · `ruling-20260902-01-T24-T27.md` §T26 · 커밋 `aa9a734` · `D-20260902-02` §3 · 재정 T28~T30 = `ruling-20260902-02-T28-T32.md` |
| 2026-09-01-sol-audit-halt-ordering.md | 3 | MED | 수용 | `HALT_CHECKS` 수기 표 폐기 → `contract_halt_partitions()` 로 계약 `failure[]` 에서 파생 · 공허 시 skip 아닌 fail · 역대조 시험에 「계약이 halt 라 하지 않았다」는 전제 검사 추가 | 커밋 `c3fe549` 메시지 「감사 잔여」 · `tests/test_m22_early_payload_assembly.py`(`contract_halt_partitions` · `test_repeat_escalation_still_applies_where_the_contract_did_not_say_halt`) |
| 2026-09-01-sol-audit-halt-ordering.md | 4a | LOW | 수용 | `read.input-digest` 가 표에서 빠진 문제는 표의 계약 파생으로 자동 해소(진입 갈래에 실재함을 실행 확인) | 커밋 `c3fe549` 메시지 「감사 잔여」 · `tests/test_m22_early_payload_assembly.py`(진입·판정 두 갈래 분할 시험) |
| 2026-09-01-sol-audit-halt-ordering.md | 4b | LOW | 수용 | `verify_declared_inputs` 실패 행 → `read.input-digest` 전용 실패 행(`halt` · 「환경 오류」) 이 T26 격자에서 구조로 서면 함수 리팩터로 halt 가 조용히 바뀌는 경로가 닫힌다. 이행 = 라운드 B(T26 · 미착수). **[추기 2026-09-02]** 재정 T29 ⓐ 가 이 행의 자리를 확정했다 — `read.input-digest` 는 진입 예외 경로(`halt` · 「환경 오류」 · 별도 시험)이고 「오늘의 표」 12검사 밖이다 | `ruling-20260902-01-T24-T27.md` §T27 §1 · 재정 T29 = `ruling-20260902-02-T28-T32.md` · 라운드 B 커밋(병합 뒤 총괄이 해시 보완) · **[정정 2026-09-02 · 감사 C-1]** 이 처분은 `852dcdd` 반입 시점에 **이 표가 처음 적었다**(원장 T27 ⒞ 「처분은 등재 시점에 사유와 함께 적는다」의 이행 · 값은 총괄 발주문 `order-round-c-t27.md` 가 정했고 실체는 재정 T29 ⓐ 가 뒤에 확정). 「이미 정한 처분만 옮긴다」의 예외 — Owner 사후 확인 대상(`D-20260902-03` §2 ⑸) |
| 2026-09-01-sol-review-g6-retry-budget.md | R | — | 수용 | 판정점별 유한 예산(조기 `retry(1)` + 정본 후속 `retry(1)`) → 재정 T16 ⒝ 예산(조기 = 레인별 1 · 후속 1) | `ruling-20260901-07-T16.md` §2 ⒝ · §3 부속 2 |
| 2026-09-01-sol-review-g6-retry-budget.md | C-a | — | 수용 | 조건 (a) 「분해 소유 검사를 조기 지점으로 옮겨 분해 레인에 되먹인다」 → T16 ⓐ (c) = 조기 이동 **+ 출구 존치** 로 채택(출구 행을 없애는 「(a) 순수형」만 기각 — 그 순수형은 총괄의 해석이었다) | `ruling-20260901-07-T16.md` §2 ⒜ · §5 |
| 2026-09-01-sol-review-g6-retry-budget.md | C-b | — | 기각 | 조건 (b) 「분해→수렴→tail 전체 재개방」 — 청구항 결함 하나에 레인 6회 · 재개방 조건·횟수·`attempt` 리셋이라는 새 경계 · 귀속 지연 | `ruling-20260901-07-T16.md` §5 |
| 2026-09-02-opus-audit-round-a.md | A-1 | HIGH | 수용 | 재정 T19 §3 이 벌한 형태의 **두 번째 발생** · 발주문이 변조 문자열을 지정했다(총괄 귀책). 수리 = 변조 앵커를 청구항 본문 안으로 + 위반 시 조기 판정 행이 실제로 달라지는 **양성 대조군** | `D-20260902-01-round-a.md` §5 · 라운드 A′ 발주문 §1 A-1 · A′ 커밋 `99fad78`(병합 뒤 총괄이 해시 보완 · 2026-09-02) |
| 2026-09-02-opus-audit-round-a.md | A-2 | MED | 수용 | SPEC §1.5 「범위 표지가 문언의 일부다」 가 이미 입법 · §4 ★ 상신(조기 합집합)이 어느 쪽으로 나도 표지는 필요. 수리 = §10 절 머리 한 문장 + 시험을 생산 가능한 상태로. **렌더 재량이나 CP1 표면이라 Owner 사후 확인**(§6-5) | `D-20260902-01-round-a.md` §5 · A′ §1 A-2 |
| 2026-09-02-opus-audit-round-a.md | A-3 | MED | 수용 | 원장 T25 ⒜ 문언 위반 · 발주문 §2.4 가 그 코드를 지정했다(총괄 귀책). 수리 = 즉시 탈출 판별을 **실패 검사별** halt 행 조회의 `any` 로 + 단위·통주 시험. ★ T26 골든은 **이 수리 뒤 커밋**에서 생성하므로 감사가 경고한 「회귀 vs 의도된 교정」 충돌이 생기지 않는다 | `D-20260902-01-round-a.md` §5 · A′ §1 A-3 · `D-20260902-02` §2 B-3 |
| 2026-09-02-opus-audit-round-a.md | A-4 | MED | 수용 | 이 라운드가 새로 연 실패 모드 · 원장 T24 ⒞ 가 지목한 계기(편집기 저장) 그 자체. 수리 = `OSError` → `read.source-digest` 실패 행 + 진단 `actual` 에 「읽을 수 없음」 + 삭제 시험 | `D-20260902-01-round-a.md` §5 · A′ §1 A-4 |
| 2026-09-02-opus-audit-round-a.md | A-5 | LOW | 수용 | 「강제의 범위를 실제보다 넓게 말했다」 계열. 수리 = `FAILURE_NEEDLES` 에 `claim-inventory`·`상신 축` 추가 | `D-20260902-01-round-a.md` §5 · A′ §1 A-5 |
| 2026-09-02-opus-audit-round-a.md | A-6 | LOW | 수용 | 값은 T26 ⒜③ 소관이라 무접촉 유지 · 표지는 **YAML 주석 한 줄**(파싱 결과 무변경 · `test_retry_budget_is_unchanged_by_the_split` 무영향) | `D-20260902-01-round-a.md` §5 · A′ §1 A-6 |
| 2026-09-02-opus-audit-round-a.md | A-7 | LOW | 부분 수용 | enum ↔ `read_runs` 결속은 **시험 한 줄**(재량 · A′). `canonical_selection.read_run` 을 같은 enum 으로 묶는 것은 스키마 값 공간 → **상신**(§6-5 · 총괄 의견 = 묶는다 · 행위시법). **[추기 2026-09-02]** 상신 절반은 **재정 T32 ⓐ** 로 닫혔다(단일 `$defs` 결속 · 행위시법 · 매니페스트 사례) — 집행은 라운드 B 또는 T31 소라운드에 동반(★ 미착수). 같은 값 공간의 둘째 자리 `screening_memos[].read_run` 은 T32 가 다루지 않았고 별도 상신 중이다 | `D-20260902-01-round-a.md` §5 · A′ §1 A-7 · 같은 문서 §6-5 · 재정 T32 = `ruling-20260902-02-T28-T32.md` §T32 · 잔여 상신 = 같은 파일 §5 ② |
| 2026-09-02-opus-audit-round-a.md | A-8 | LOW | 수용 | 커밋 후 총괄 소관. 그 커밋에서 `HANDOFF-NEXT.md` §0 재작성 · §2 정정 마커 · §5 순서도 갱신 | `D-20260902-01-round-a.md` §5 A-8 · 커밋 `f46698e`(그 표의 「이 커밋」) |
| 2026-09-02-sol-challenge-t26-design.md | B-1 | BLOCKER | 이연 | 처분 원문은 「이연 → 재정 상신」이다. 상류 두 재정(P-4 · T26 §3 ②)이 충돌하는 자리 — 총괄이 어느 쪽을 접어도 재정 침범. 선택지·추천 = §3 ★1. **[추기 2026-09-02]** 이연이 풀렸다 — **재정 T28 = β**(수렴 출구 무재시도 · P-4 존치 · `[early]` 존치 · 출구 수렴 실패 = 즉시 `escalate` · T26 §3 ② 에 예외 1칸 추기). 처분 어휘 `이연` 은 상신 당시의 것이라 그대로 두고 해소를 여기 적는다 | `D-20260902-02-t26-design-challenge.md` §2 · 상신 = 같은 문서 §3 ★1 · **재정 T28** = `ruling-20260902-02-T28-T32.md` §T28 |
| 2026-09-02-sol-challenge-t26-design.md | B-2 | BLOCKER | 부분 수용 | 처분 원문은 「부분 수용 — 앞절반 수용 · 뒷절반 재정 상신」이다. 앞절반(분모 12 · 8,190칸 전수 · 총괄이 `read.source-digest` 와 레인 로그 2종을 빠뜨렸다)은 설계 오류 → v2. 뒷절반(「오늘의 표」의 영역에 진입 검사가 드는가)은 T26 §3 ② 의 해석 = 재정 → §3 ★2. **[추기 2026-09-02]** 뒷절반은 **재정 T29 = ⓐ** 로 닫혔다(오늘의 표 = 출구 12검사 · 골든 8,190칸 · `read.input-digest` 는 진입 예외 경로 + 별도 시험 + `halt · 환경 오류` 행) | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 · 상신 = 같은 문서 §3 ★2 · **재정 T29** = `ruling-20260902-02-T28-T32.md` §T29 |
| 2026-09-02-sol-challenge-t26-design.md | B-3 | BLOCKER | 수용 | 검증 설계 원리 위반 — 총괄이 §5-4 에서 스스로 의심하고도 「제어 흐름이 다르니 된다」고 판단했다. v2 = **기준 커밋 골든 동결**: 공식 검사 id 목록 · 비공집합 × repeated 전건의 `(action, reason_label)` · 기준 커밋 해시 · 생성 절차를 픽스처 파일로 리포에 넣고 시험은 그 파일만 읽는다. ★ 기준 커밋 = **라운드 A′ 뒤 커밋** = **`99fad78`**(병합 뒤 총괄이 해시 보완 · 2026-09-02 — 라운드 C `852dcdd` 는 `engine/`·`contracts/stages/`·`reader/` 무접촉이라 골든 값이 같다 · `D-20260902-03` §4) | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 · 기준 커밋 = `D-20260902-03-round-c.md` §4 |
| 2026-09-02-sol-challenge-t26-design.md | B-4 | BLOCKER | 수용 | 원장 등식을 바꾸는 것은 허용되지 않는다. v2 = 통합 행을 **판정점 기준으로 분리** · 관문은 교집합 없이 원장 식 그대로 · `phase` 는 「그 판정점에서 실제 실행되는가」만 별도 검증. 행 분리는 (조치, 라벨) 표를 바꾸지 않으며 골든(B-3)이 그것을 증명한다 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.1 · §2.5 |
| 2026-09-02-sol-challenge-t26-design.md | B-5 | HIGH | 수용 | 총괄이 §5-5 에서 관문만 보고 「닫혔다」고 판단했다. v2 = `terminal_action()` 이 `action: retry(n)` 에 유효 `then` 필수 · `then` 어휘 3종 · `worst_status` 호출 **전** 검증 · 위반 시 `StageError` · 두 변조 시험 | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.4 |
| 2026-09-02-sol-challenge-t26-design.md | B-6 | HIGH | 부분 수용 | 처분 원문은 「부분 수용 — 뒷절반 수용 · 앞절반 해석 상신」이다. 뒷절반: v2 = upstream 행에 **식별 키만** · 호출자 만들지 않음 명시 · binding `deferred/test_bound`. 앞절반: 「`checks` 의무는 검사 실패 행에만, 세 행은 `kind`」 는 원장 문언의 해석이라 **Owner 확인** → §3 ★3. **[추기 2026-09-02]** 앞절반은 **재정 T30 = ⓐ** 로 닫혔다(`checks` 는 검사 실패 행에만 · `kind` ∈ {`retry-repeat`, `gate-escalation`, `upstream-defect`} 각 정확히 1행 · `checks` xor `kind`) | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.1 · 상신 = 같은 문서 §3 ★3 · **재정 T30** = `ruling-20260902-02-T28-T32.md` §T30 |
| 2026-09-02-sol-challenge-t26-design.md | B-7 | MED | 수용 | v2 수용 기준 = 전수 pytest(plain · `PYTHONOPTIMIZE=1`) · 기존 5 + 신설 1 관문 plain · 같은 6 관문 `-O` · 각 명령과 기대 exit | `D-20260902-02-t26-design-challenge.md` §2 · v2 §2.6 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-1 | BLOCKER | 수용 | T-1 의 monkeypatch 대상 `m2`(= `tests.test_m2_read` 모듈)는 러너에 닿지 않는다(도전자 실측 `PATCH_REACHES_RUNNER False`) — v3 = `engine.stages.read` 모듈 전역 패치 | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-2 | BLOCKER | 수용 | 골든 생성이 `99fad78` 모듈을 import 한다는 보장 없음 — v3 = `--repo` 인자 · `sys.path[0]` · provenance 검사 실패 시 생성 거부(v4 = 6검사 + `-I` + 절대 `out`) | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-3 | HIGH | 수용 | 정본 후속 1회 재시도 = 레인 로그 3행(접지 2 + 통합 1) — v3 T-2 = `/retry-1/` 정확히 3 · task 집합 고정 | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-4 | HIGH | 수용 | G4 가 유령 phase 를 통과 — v3 R9 = `phases` ⊆ {early, exit} · 변조 ⒄(v4 에서 `exit` 필수 · `early` ⇔ early 목록으로 확장) | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-5 | HIGH | 수용 | 판정점 id 중복·미지 id 우주 미정 → M3 임의 선택 — v3 R8 = 판정점 정확히 {early, exit} 각 1행 · 우주 = 출구 12 id · 변조 ⒅ | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-6 | HIGH | 수용 | manifest predicate 가 정수 mask 에 쓸 수 없는 표현(`TypeError`) — v3 = `eval` 가능한 비트 식으로 고정 · 생성기·시험 공유 | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-7 | MED | 수용 | T-11 에 종단 어휘 두 벌(엔진·관문) 상등 검사 부재 — v3 T-11 ⑤ 신설 | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-sol-challenge-t26-design-v2.md | V-8 | MED | 수용 | §2.2 손검산이 lane-log-only 3칸(`StageError`)을 누락 · 「격자 순」 서술이 `worst_status` 순서와 반대 — v3 = 3칸 예외 명시 · 격자 순서/동률 해소 순서 분리 서술(행 순서 불변) | `D-20260902-02-t26-design-challenge.md` §7 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-1 | HIGH | 수용 | 생성기가 `os.chdir(repo)` 뒤 상대 `--out` 을 쓰면 골든이 `$TMP` 에 떨어진다 — v4 = `out = realpath(--out)` 을 chdir 전에 고정 · `python -I` · provenance 요약에 절대경로 | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-2 | HIGH | 수용 | R9 의 전제(정본 12건 `phases` ⊆ {early, exit})를 설계가 미실측 — v4 §1 「국면 실물」 행에 12건 값 전부 기재(전부 ⊆ · 전부 `exit` 포함 · `early` 셋 = early 목록) | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-3 | HIGH | 수용 | 생성기 저작 좌석·시점이 라운드 순서에 없어 B 가 골든 없이 시작 — v4 = 라운드 B-0(sol-coder · 생성기 + 시험) → 총괄 실행·골든 커밋 → 라운드 B | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-4 | MED | 수용 | T-4 피검 대상이 루프 인라인 — v4 = `_exit_retry_eligible(contract, failing)` 헬퍼 명명 · T-4 가 함수 단위로 부른다 | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-5 | MED | 수용 | 계약 출구 id 집합 ↔ 엔진 상수의 양방향 다리 시험 좌표 없음(유령 id + 유령 행이 관문 전부 통과) — v4 T-12 신설 | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-6 | MED | 수용 | R9 가 `phases` 거짓 양성(`read.source-digest` 에 `early`)을 안 잡는다 — v4 R9 = `exit` 필수 · `early ∈ phases ⇔ id ∈ points[early].checks` · 변조 ⒆⒇ | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-fable-advice-t26-design-v3.md | N-7 | LOW | 수용 | 문언 5건 — T-11 ④ 결함 = ⑴⑽⒄ 명명 · T-9 grep 범위(`engine/` 의 `failure_row_of_kind(` 호출 리터럴) · `_failure_verdict` 빈 후보 StageError · T-2 retry-2 부재 · T-1 wrapper 치환 = `row.add` 한 건 | `D-20260902-02-t26-design-challenge.md` §8 |
| 2026-09-02-sol-audit-round-c.md | C-1 | HIGH | 수용 | `852dcdd` 반입 시점 4b 행의 처분 `수용` 이 선행 출처 없이 이 표에서 처음 적혔다 — 원장 T27 ⒞ 「처분은 등재 시점에 사유와 함께 적는다」의 이행이었으나 값은 총괄 발주문이 정했고(실체는 재정 T29 ⓐ 가 뒤에 확정) 「이미 정한 처분만 옮긴다」는 자기 서술과 충돌했다. 처분 = 4b 행·머리에 `[정정]` 마커 + Owner 사후 확인 등재(`D-20260902-03` §2 ⑸) | `D-20260902-03-round-c.md` §6 |
| 2026-09-02-sol-audit-round-c.md | C-2 | MED | 수용 | G4 가 격 열을 읽지 않아 `CRITICAL` 이 통과(SPEC 11항 「①~④ 대조」보다 실물이 좁다) — 라운드 C′(sol-coder) 에서 격 어휘 대조 + 자기 시험 추가 | `D-20260902-03-round-c.md` §6 · 집행 `867b95b`(라운드 C′) |
| 2026-09-02-sol-audit-round-c.md | C-3 | MED | 수용 | 표 파서가 데이터 행 열 수를 헤더와 대조하지 않는다(7셀 통과 · 5셀 `IndexError` 로 `EXIT=` 없이 사망) — C′ 에서 arity 대조 · 부족/초과 exit 1 + 마커 | `D-20260902-03-round-c.md` §6 · 집행 `867b95b`(라운드 C′) |
| 2026-09-02-sol-audit-round-c.md | C-4 | LOW | 수용 | `select_table` 이 문서 어느 곳의 동일 헤더든 받아 §0/§1 밖 decoy 표로 정식 절을 비울 수 있다 — C′ 에서 §0/§1 제목 아래 첫 표로 결속 | `D-20260902-03-round-c.md` §6 · 집행 `867b95b`(라운드 C′) |
| 2026-09-02-sol-audit-round-c.md | C-5 | MED | 부분 수용 | 사실 인정 — C 발주문은 B 가 아니라 A′ 반경을 고지했고 T26·T27 은 둘 다 `docs/SPEC.md` 를 반영처로 든다. 그러나 C 가 B 앞에 병합되어(`852dcdd` → B 미착수) 병렬이 순차로 바뀌었으므로 T27 §3 ④ 의 목적(동시 편집 충돌 방지)은 순차로 충족된다. 「고지」 의무는 B 발주문이 든다(C 와 겹치는 SPEC §8.3 7항·관문표를 C 병합본 위에서 고친다고 적는다). C 발주문 문면은 소급 수정하지 않는다 | `D-20260902-03-round-c.md` §6 |
| 2026-09-02-sol-audit-round-c.md | C-6 | LOW | 수용 | 「관문이 주장하지 않는 것」 문언이 열거 완전성만 들고 포인터 실재성·사유 의미·`선행 종결` 사실성을 빠뜨렸다 — DISPOSITIONS 머리·SPEC 11항·CLAUDE.md 는 이 커밋에서 추기 · 도구 docstring 은 C′ | `D-20260902-03-round-c.md` §6 · 집행 `867b95b`(라운드 C′) |
| 2026-09-02-sol-challenge-t26-design-v4.md | W-1 | BLOCKER | 수용 | 승인된 출구 재시도 8종이 독립 정답지에 결속되지 않아 「exit 목록 − 검사 하나 + 그 행을 비-retry escalate 로 분리」 변조가 관문·골든·T-12 전부 통과하며 재디스패치 1→0 — v5 = `EXIT_RETRY_CHECK_IDS`·`EARLY_RETRY_CHECK_IDS` 엔진 상수 + 진입 가드 · 관문 G3 승인 집합 상수 · T-4 출구 12종 전부 · 변조 ㉑ | `D-20260902-02-t26-design-challenge.md` §9 |
| 2026-09-02-sol-challenge-t26-design-v4.md | W-2 | HIGH | 수용 | 조기 상신축 갈래가 `failure_row_of_kind` 의 `action` 을 직접 써서 `terminal_action()` 을 우회(B-5 런타임 조건 재개방) — v5 = `_gate_escalation_verdict()` 가 `terminal_action()` 경유 · T-8 확장 · 변조 ㉔ | `D-20260902-02-t26-design-challenge.md` §9 |
| 2026-09-02-sol-challenge-t26-design-v4.md | W-3 | MED | 수용 | `checks_on_entry`·`checks_before_exit` 선언 배열의 중복을 검사하지 않는다(13행/12 id 통과) — v5 = G2 선언 형식·중복 검사 · T-12 `len == len(set)` · 변조 ㉒㉓ | `D-20260902-02-t26-design-challenge.md` §9 |
| 2026-09-02-sol-challenge-t26-design-v4.md | W-4 | LOW | 수용 | §2.10 「자기 시험 18종」 vs §2.7·§2.11 20종 계수 충돌 — v5 = 계수는 §2.7 표 한 자리만 · 문서 산문에 수를 적지 않는다 | `D-20260902-02-t26-design-challenge.md` §9 |
| 2026-09-02-sol-challenge-t26-design-v5.md | X-1 | BLOCKER | 수용 | 관문이 행 분할을 고정하지 않아 T22 §3 ① 의 lane-log 두 전용 행을 하나로 병합(11→10행)해도 관문 전종·골든 통과 — v6 = G1 이 승인 실패표 골격 전체(순서·키·action·then·label·points)를 상수로 정확 일치 · T-13 · `test_m23` 두 조회 다른 행 · 변조 ㉕㉖ | `D-20260902-02-t26-design-challenge.md` §10 |
| 2026-09-02-sol-challenge-t26-design-v5.md | X-2 | HIGH | 수용 | T-1 이 finding 을 더한 `element-set` 은 escalation-trigger 축(exact-match 축 = independent-count·dependent-count·dependent-set) — 자기모순 판정서. v6 = wrapper 가 peer spec 사본에 독립항을 복제해 검사기 자신이 `independent-count` fail · 판정서 축 `fail` 기록까지 검사 | `D-20260902-02-t26-design-challenge.md` §10 |
| 2026-09-02-sol-challenge-t26-design-v5.md | X-3 | MED | 수용 | `upstream-defect` 행의 `reject-upstream` 이 어디에도 고정되지 않아 `halt` 로 바꿔도 통과(PD-M5 이연 처분의 계약 변경) — v6 = G1 골격 고정이 kind 행 action·then·label 을 덮는다 · 변조 ㉗ | `D-20260902-02-t26-design-challenge.md` §10 |
| 2026-09-02-sol-challenge-t26-design-v6.md | Y-1 | HIGH | 수용 | T-1 에 폐기된 v5 지시(`element-set` finding 수동 추가)와 새 지시가 공존 — 총괄의 패치 잔재. v7 = T-1 행을 한 절차만 남겨 재작성 | `D-20260902-02-t26-design-challenge.md` §11 |
| 2026-09-02-sol-challenge-t26-design-v6.md | Y-2 | MED | 수용 | `test_m21` :533 은 원천 다이제스트 행 시험인데 `retry-repeat` 조회로 바꾸라 적었다 — v7 = :533 → `failure_rows_for_checks(contract, {"read.source-digest"})` · :733 → `failure_row_of_kind(…, "retry-repeat")` | `D-20260902-02-t26-design-challenge.md` §11 |
| 2026-09-02-sol-challenge-t26-design-v6.md | Y-3 | MED | 수용 | 관문이 `max_retries` 를 보지 않아 `early.max_retries: 2` 가 관문 관측면 불변으로 통과(존치 `test_m17` 이 잡지만 관문 구멍) — v7 = G3 에 `{n} == {max_retries}` 결속 · 변조 ㉙ | `D-20260902-02-t26-design-challenge.md` §11 |
| 2026-09-02-sol-challenge-t26-design-v6.md | Y-4 | LOW | 수용 | 계수 리터럴(24/28)이 §0·§2.10·§2.11 에 다시 들어가 W-4 재발 — 총괄의 패치 잔재. v7 = 리터럴 전부 제거 · §2.7 열거만 정본 · 관문 출력이 센다 | `D-20260902-02-t26-design-challenge.md` §11 |
| 2026-09-02-sol-challenge-t26-design-v6.md | Y-5 | LOW | 수용 | T-12 「유령 행은 이 시험만 잡는다」가 v6 에서 거짓(G1 골격이 먼저 잡는다) — v7 = 목적 문언을 「관문 오라클과 독립적인 계약↔엔진 상수 다리」로 | `D-20260902-02-t26-design-challenge.md` §11 |

**행 수 = 80**(`등재` 13파일의 지적 전건). **[정정 2026-09-02 · 6차]** 직전 판 **75** — 5차 도전 원문 반입(Y 5)으로 다섯 늘었다.

**행 수 = 75**(`등재` 12파일의 지적 전건). **[정정 2026-09-02 · 5차]** 직전 판 **72** — 4차 도전 원문 반입(X 3)으로 셋 늘었다.

**행 수 = 72**(`등재` 11파일의 지적 전건). **[정정 2026-09-02 · 4차]** 직전 판 **68** — 3차 도전 원문 반입(W 4)으로 넷 늘었다.

**행 수 = 68**(`등재` 10파일의 지적 전건). **[정정 2026-09-02 · 3차]** 직전 판은 **47**(7파일)이었다 — 감수 원문 3건 반입(설계 v2 도전 V 8 · 자문 N 7 · 라운드 C 감사 C 6)으로 21 늘었다. 아래 구 문언은 그대로 둔다.

**행 수 = 47**(`등재` 7파일의 지적 전건). **[정정 2026-09-02]** 반입 시점(`852dcdd`)은 **45** 였다 — §2 처분 대기 2건이 `S-1`·`S-2` 로 올라와 둘이 늘었다. 구 계수를 지우지 않는 이유는 이 리포의 관례다(닫힌 것도 어떻게 닫혔는지를 남긴다).

---

## §2 이 표에 아직 서지 못한 것 — 처분 대기

**처분이 기록에 없거나 총괄이 id 를 세우지 않은 지적은 이 표에 넣지 않는다.** 값을 지어내는
것이 비어 있는 것보다 나쁘기 때문이다(처분 어휘 4종 중 하나를 저작자가 고르면 그것은 기록이
아니라 창작이다). 아래는 발주자·총괄이 처분 또는 id 를 정한 뒤 §1 로 올라간다.

**★ 2026-09-02 — 아래 두 줄은 §1 로 올라갔다(`S-1` · `S-2`).** 처분·사유 = `D-20260902-03-round-c.md` §3.
행은 포인터로 바꾸되 지우지 않는다 — 반입 당시 무엇이 비어 있었는지가 곧 이 자리의 사료다. 지금 처분 대기는 **0건**이다.

| 파일 | 자리 | 무엇 | 무엇이 비었나 |
|---|---|---|---|
| 2026-09-01-opus-audit-t17-repair.md | §6 소견 ⑴ | **★ 닫힘 → §1 `S-1`**(2026-09-02 · `D-20260902-03-round-c.md` §3 · 수용 · 발주문 골격 ⑼). 아래는 반입 당시 문안 그대로다 — 레인이 정본 트리에서 `git apply -R` 로 역프로브를 도는 방식은 안전하지 않다 — 프로브 레인에 정본 트리 쓰기 권한을 주지 말 것(권고) | **처분 기록** — `docs/decisions/` 전문 검색에서 이 소견의 처분을 찾지 못했다(D 문서·원장·`D-20260902-02` §5 발주문 골격 개정 ⑹~⑻ 어디에도 없다). 원문이 id 도 붙이지 않았다 |
| 2026-09-01-opus-audit-t17-repair.md | §6 소견 ⑵ | **★ 닫힘 → §1 `S-2`**(2026-09-02 · `D-20260902-03-round-c.md` §3 · 수용 — 재정 T20 으로 이미 집행 · id 만 보완). 아래는 반입 당시 문안 그대로다 — 규율 10 의 판별선은 「파일」이 아니라 「저자·절」이어야 한다 | **id** — 처분은 있다(재정 T20 = 규율 10 개정 + 다섯째 관문). 원문이 id 를 붙이지 않았고, 원문에 없는 id 를 세우는 것은 총괄 재량이라(Owner 사후 확인 대상) 저작 레인이 정하지 않는다 |

**세우지 않기로 이미 정해진 것** — 같은 파일 §4 Q2 의 판정 3건(총괄 자기 계상에 대한 감사자의
채점이지 지적이 아니다)과 §6 소견 ⑶(E-2 전파 전수 — 그 잔여는 `Y-5` 로 이미 §1 에 서 있다).
