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
| 2026-09-02-sol-challenge-t26-design-v7.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v8.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v9.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v10.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v11.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v12.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v13.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v14.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v15.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v16.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v17.md | 등재 | — |
| 2026-09-02-sol-challenge-t26-design-v18.md | 등재 | — |
| 2026-09-03-opus-audit-round-b.md | 등재 | — |
| 2026-09-03-opus-audit-round-b-prime.md | 등재 | — |
| 2026-09-03-opus-audit-round-b2-t31.md | 등재 | — |
| 2026-09-05-opus-audit-round-rd.md | 등재 | — |
| 2026-09-05-opus-audit-round-re.md | 등재 | — |
| 2026-09-05-astra-m1b-rf-t35.md | 등재 | — |
| 2026-09-05-astra-m1b-fix4.md | 등재 | — |
| 2026-09-05-astra-m1b-audit3.md | 등재 | — |
| 2026-09-05-opus-audit-round-rf-t35.md | 등재 | — |
| 2026-09-05-astra-m1b-rg.md | 등재 | — |
| 2026-09-05-astra-m1b-audit4.md | 등재 | — |
| 2026-09-05-opus-audit-round-rg.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a1.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a1v2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a1-audit.md | 등재 | — |
| 2026-09-05-fable-audit-round-m2a1.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a2v2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a2-audit.md | 등재 | — |
| 2026-09-05-fable-audit-round-m2a2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a3.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a3v2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2a3-audit.md | 등재 | — |
| 2026-09-05-astra-m1b-m2b1.md | 등재 | — |
| 2026-09-05-astra-m1b-m2b1v2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2b2.md | 등재 | — |
| 2026-09-05-astra-m1b-m2b2v2.md | 등재 | — |
| 2026-09-05-fable-audit-round-m2a3.md | 등재 | — |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | 등재 | — |
| 2026-09-06-astra-m1b-m2b1v3.md | 등재 | — |
| 2026-09-06-astra-m1b-m2b2v3.md | 등재 | — |
| 2026-09-06-astra-m1b-m2b2v4.md | 등재 | — |

**계수** — `등재` **32** · `선행 종결` **12** · 합 **44**(`docs/lessons/` 전 파일). **[정정 2026-09-06 · M1b 4차(M2b-2) 반입]** 직전 판 31/12/43. **[정정 2026-09-06 · M1b 3차 두 원문 반입]** 직전 판 29/12/41. **[정정 2026-09-06 · 자문 회신 반입]** 직전 판 28/12/40. **[정정 2026-09-03 · 합본 감사 반입]** 직전 판 27/12/39. **[정정 2026-09-03 · B′ 재감사 반입]** 직전 판 26/12/38. **[정정 2026-09-03 · 라운드 B 감사 반입]** 직전 판 25/12/37. **[정정 2026-09-03]** 아래 구 문언 「등재 7 · 선행 종결 12 · 합 19」는 라운드 C 반입(`852cdd`) 시점의 계수이며, 그 뒤 도전 원문 v2~v18 반입이 이 줄을 따라가지 않았다 — 오류 수정(규율 11 ③). 관문 G1 은 집합 상등을 보고 이 계수는 보지 않는다.

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
| 2026-09-02-sol-challenge-t26-design-v7.md | Z-1 | MED | 수용 | G3 예산 등식이 타입을 안 봐 `true`/`1.0` 이 통과(런타임·`test_m17` 은 `type is int` 로 거부 — 판정이 갈림) — v8 = G3 에 `type(max_retries) is int` 를 등식 앞에 · 변조 ㉚㉛ · T-11 ④ 직접 변조 | `D-20260902-02-t26-design-challenge.md` §12 |
| 2026-09-02-sol-challenge-t26-design-v7.md | Z-2 | MED | 수용 | T-7 ④ 가 manifest 의 predicate 를 `eval` 해 같은 manifest 의 cells 와 비교하는 자기참조 오라클(동반 변조 자기일관 통과) — v8 = 시험 코드 고정 식으로 β 집합 독립 산출 · `exceptions` 길이·id·rule·predicate 문자열 고정값 대조 · B-0 시험에 동반 변조 | `D-20260902-02-t26-design-challenge.md` §12 |
| 2026-09-02-sol-challenge-t26-design-v8.md | AA-1 | HIGH | 수용 | T-7 ① 이 `check_ids` 를 집합으로만 대조 — 중복 + 13번째 비활성 축 목록이 값·계수·β 전부 통과 — v9 = 검증기 `len == len(set) == 12` 선행 · 음성 시험 ⓐ | `D-20260902-02-t26-design-challenge.md` §13 |
| 2026-09-02-sol-challenge-t26-design-v8.md | AA-2 | HIGH | 수용 | T-7 이 셀 키 우주를 고정하지 않아 `1024:1` 삭제 + 영역 밖 `0:1` 삽입이 통과 — v9 = 검증기 키 집합 == 정답 우주 양방향 · 값 형식 · `exceptions[0].cells` 정확히 2,048 · 음성 시험 ⓑ | `D-20260902-02-t26-design-challenge.md` §13 |
| 2026-09-02-sol-challenge-t26-design-v8.md | AA-3 | MED | 수용 | T-7 ⑥ 이 `base_commit`·`tree_head` 자기일관만 봄 — v9 = 검증기에 리터럴 `99fad78` + `git rev-parse 99fad78` 전체 해시를 호출자가 넘겨 대조 · 음성 시험 ⓒ | `D-20260902-02-t26-design-challenge.md` §13 |
| 2026-09-02-sol-challenge-t26-design-v8.md | AA-4 | MED | 수용 | Z-2 처분의 「B-0 시험에 동반 변조」가 피검 함수 없음(T-7 은 B 에서 생김) — v9 = `validate_manifest.py` 를 B-0 산출물로 · 생성기 자기 검증 · B-0 시험 · B 의 T-7 이 같은 검증기 호출 | `D-20260902-02-t26-design-challenge.md` §13 |
| 2026-09-02-sol-challenge-t26-design-v9.md | AB-1 | MED | 수용 | 검증기가 값 필드를 다 덮지 않음(`rule`·`meaning`·`$comment`·`cell_key`·`generator`·`generation_command` 존재만 · 계수 `type is int` 없음 · `provenance` 키 미고정) — v10 = 모든 값 필드에 리터럴/형식 · 음성 시험 ⓗⓘⓙ | `D-20260902-02-t26-design-challenge.md` §14 |
| 2026-09-02-sol-challenge-t26-design-v9.md | AB-2 | MED | 수용 | `python -I` 아래에서 형제 `validate_manifest.py` 적재 방식 부재 → M3 임의 선택 — v10 = `importlib.util.spec_from_file_location(Path(__file__).with_name(…))` 코드 명시 · stdlib 만 import · B-0 시험이 공개 `-I` 명령을 서브프로세스로 실행 | `D-20260902-02-t26-design-challenge.md` §14 |
| 2026-09-02-sol-challenge-t26-design-v10.md | AC-1 | MED | 수용 | T-7 의 `with_name` 이 `tests/validate_manifest.py` 를 가리킴(파일 부재) — v11 = 호출자별 경로 · `is_file()` 선검사 · B-0 시험 파일을 `tests/test_m24a_failure_grid_generator.py` 로 고정해 T-7 경로식을 미리 실행 | `D-20260902-02-t26-design-challenge.md` §15 |
| 2026-09-02-sol-challenge-t26-design-v10.md | AC-2 | MED | 수용 | `cell_key` 정본이 본문·예시(`**`)에서 다르고 `generation_command` 가 「네 줄」·「블록 그대로」·물리 6줄 — v11 = 정본을 각각 한 자리로 · 생성 명령을 정확히 네 줄로 재작성 | `D-20260902-02-t26-design-challenge.md` §15 |
| 2026-09-02-sol-challenge-t26-design-v10.md | AC-3 | MED | 수용 | 골든 커밋 열거에 검증기 누락 · B-0 미커밋 산출의 main 승격 절차 부재 — v11 = B-0 병합 커밋(세 파일 · C′ 절차) → main 에서 생성 → 골든 커밋(manifest) → 라운드 B | `D-20260902-02-t26-design-challenge.md` §15 |
| 2026-09-02-sol-challenge-t26-design-v10.md | AC-4 | LOW | 수용 | T-7 이 「§2.8 ①~⑥」을 가리키나 목록은 ①~③ + 총괄 검수 ④ — v11 = T-7 = §2.8 시험 ①~③ | `D-20260902-02-t26-design-challenge.md` §15 |
| 2026-09-02-sol-challenge-t26-design-v10.md | AC-5 | LOW | 수용 | `assemble_spec :505-556` → `:506-561` — v11 §1 정정 | `D-20260902-02-t26-design-challenge.md` §15 |
| 2026-09-02-sol-challenge-t26-design-v11.md | AD-1 | HIGH | 수용 | 검증기 음성 시험이 여러 필드 동반 변조 + 「위반 ≥ 1」만 요구 — 검사 하나를 빼도 전건 통과 — v12 = 위반 문장에 필드 경로 토큰 · 표 T-V 한 필드씩 · 각 시험은 그 토큰의 위반 실재 | `D-20260902-02-t26-design-challenge.md` §16 |
| 2026-09-02-sol-challenge-t26-design-v11.md | AD-2 | MED | 수용 | G1 골격 상수에 `judged_at` 부재 · 열거 밖 기계 키 추가 통과 — v12 = 상수에 `judged_at` 열 · 행별 허용 키 집합 정확 일치 · 변조 ㉜㉝ · T-13 | `D-20260902-02-t26-design-challenge.md` §16 |
| 2026-09-02-sol-challenge-t26-design-v11.md | AD-3 | MED | 수용 | 생성 명령이 fail-fast 아님 · 마지막 줄 미검사 · B-0 시험이 생성기 단독만 — v12 = `set -euo pipefail` + `trap` + `EXIT=0` 대조 · 환경변수 매개 · B-0 시험이 블록 전체 서브프로세스 ⒜⒝⒞ | `D-20260902-02-t26-design-challenge.md` §16 |
| 2026-09-02-sol-challenge-t26-design-v12.md | AE-1 | HIGH | 수용 | 표 T-V 가 필드 단위라 한 토큰 아래 여러 제약이 겹쳐 검사 하나를 빼도 전건 통과 — v13 = 제약 ID(`CONSTRAINT_IDS`) 진단 · 표를 제약 ID 단위로 · 양방향 상등 + 각 ID 위반 실재 | `D-20260902-02-t26-design-challenge.md` §17 |
| 2026-09-02-sol-challenge-t26-design-v12.md | AE-2 | MED | 수용 | 생성 명령 둘째 줄(`test "$(git diff … 파이프 wc -l)" = 0`)이 명령 치환 안의 파이프 실패를 삼킴 — v13 = `git diff --quiet` · B-0 ⒟ 무효 ref 역프로브 | `D-20260902-02-t26-design-challenge.md` §17 |
| 2026-09-02-sol-challenge-t26-design-v12.md | AE-3 | MED | 수용 | 시험용 클론에 `.venv` 없음 · `BASE` 자릿수 미정 — v13 = `PYTHON_BIN` 매개(기본 main `.venv`) · B-0 은 정본 `.venv` 절대경로 · `BASE=git rev-parse --short=7` | `D-20260902-02-t26-design-challenge.md` §17 |
| 2026-09-02-sol-challenge-t26-design-v13.md | AF-1 | HIGH | 수용 | T-V 가 「제약 하나만 깨고 그 제약만 보고」 결속이 아님(복합 변조 · 누락 ID · 한 키 전칭 · 「ID 포함」 기대) — v14 = 층위 평가 · `set(위반 ID) == {target}` · 표 재작성 | `D-20260902-02-t26-design-challenge.md` §18 |
| 2026-09-02-sol-challenge-t26-design-v13.md | AF-2 | MED | 수용 | B-0 산출물이 미커밋이라 시험용 clone 에 생성기·검증기가 없음 — v14 = clone 조립 절차(두 파일 복사 + clone 안 임시 커밋 · BASE 7자) | `D-20260902-02-t26-design-challenge.md` §18 |
| 2026-09-02-sol-challenge-t26-design-v13.md | AF-3 | MED | 수용 | 관문이 조기 선언 `early_phase_spec.judged_here` 를 안 읽어 유령 id 추가가 통과 — v14 = R2 우주에 judged_here · 세 벌 상등 · 변조 ㉞ | `D-20260902-02-t26-design-challenge.md` §18 |
| 2026-09-02-sol-challenge-t26-design-v14.md | AG-1 | HIGH | 수용 | T-V 에 누락 ID(`exceptions[0]` dict · 경로 원소 str · 셀 문자열 sentinel) · `subset_of_cells` 잔재 · `<k>` 미전개 · DAG 미명시 — v15 = ID 셋 추가 · 잔재 제거 · 슬러그 열 개 전개 · 선행조건 DAG 절 | `D-20260902-02-t26-design-challenge.md` §19 |
| 2026-09-02-sol-challenge-t26-design-v14.md | AG-2 | MED | 수용 | G1 이 `condition`·`note` 를 선택 키로 허용(1행 `condition` 삭제 통과) — v15 = 모든 행에 둘을 비공 str 로 필수(정본 10행 전부 실측) · 변조 ㉟㊱ · T-13 동기 | `D-20260902-02-t26-design-challenge.md` §19 |
| 2026-09-02-sol-challenge-t26-design-v15.md | AH-1 | HIGH | 수용 | 최상위 manifest 타입 제약 부재(`[]` → 예외 또는 ID 병합) — v16 = `manifest.type` ID · 변조 `[]` · DAG 뿌리 | `D-20260902-02-t26-design-challenge.md` §20 |
| 2026-09-02-sol-challenge-t26-design-v15.md | AH-2 | HIGH | 수용 | `expected_counts.keys.exact` 가 cells 재계산 의존인데 DAG 는 `.eq` 만 cells 뒤 — v16 = keys.exact 를 `COUNT_KEY_SLUGS` 고정 집합으로 · `.eq` 는 cells 층 전부 뒤 | `D-20260902-02-t26-design-challenge.md` §20 |
| 2026-09-02-sol-challenge-t26-design-v15.md | AH-3 | MED | 수용 | `exception.cell_count.eq` 정의 둘(len 연쇄 vs 고정값) — v16 = `cell_count == 2048` 단일 · `len(cells)==2048` 은 unique+set 함의 | `D-20260902-02-t26-design-challenge.md` §20 |
| 2026-09-02-sol-challenge-t26-design-v15.md | AH-4 | LOW | 수용 | §1 import 좌표 오류 — v16 = `tests/test_m21…:33 import test_m2_read as m2` | `D-20260902-02-t26-design-challenge.md` §20 |
| 2026-09-02-sol-challenge-t26-design-v16.md | AI-1 | HIGH | 수용 | `$comment` 「비공」 제약에 ID·변조·순서 없음 — v17 = 직접 검사 삭제 · 세 `contains` 가 함의(함의 목록 명시) · DAG `comment.type → contains 셋` | `D-20260902-02-t26-design-challenge.md` §21 |
| 2026-09-02-sol-challenge-t26-design-v16.md | AI-2 | MED | 수용 | 「T-V 행 순서 = 평가 순서」가 2열 배치·DAG 와 충돌 — v17 = 문언 삭제 · DAG 절이 순서의 유일 정본 | `D-20260902-02-t26-design-challenge.md` §21 |
| 2026-09-02-sol-challenge-t26-design-v16.md | AI-3 | LOW | 수용 | DAG 「`.eq` 열 개」 vs 실제 다섯 — v17 = type 다섯 + eq 다섯 = 열 ID 로 문언 정정 | `D-20260902-02-t26-design-challenge.md` §21 |
| 2026-09-02-sol-challenge-t26-design-v17.md | AJ-1 | MED | 수용 | `provenance.tree_head` 의 제약·선행순서가 검사 항목·T-V·DAG 세 정본 사이에서 불일치(DAG 「각 키: type」 vs 표의 `.eq` 하나 → M3 가 진단 ID 임의 선택) — v18 = DAG provenance 가지를 키별로 명시 재작성 · `tree_head` 는 `.eq` 하나 · T-V 변조 정수 `17` | `D-20260902-02-t26-design-challenge.md` §22 |
| 2026-09-03-opus-audit-round-b.md | RB-1 | HIGH | 수용 | 출구 재시도 8종이 계약·엔진 상수·관문 상수 세 사본에만 결박 — 정합 편집(8행 points → early 만 + 두 상수 축소)이 관문 7종·self-test·pytest 761 전건 통과하며 claim 2종의 출구 재시도를 지움. 설계 W-1 처분이 「독립 정답지」 대신 사본을 늘린 것 — B′ = 원장 도출식 다리 시험 set(EXIT_RETRY_CHECK_IDS) == set(READ_CHECK_IDS) − {{source-digest, convergence}}(reader/lib 상수 = 독립 정본) + SPEC 에 도출식 한 줄 + 발주문 양성 대조(RB-1 재현 편집이 빨개짐 실측) | `D-20260903-03-round-b.md` §6 |
| 2026-09-03-opus-audit-round-b.md | RB-2 | MED | 수용 | B-0 단위 시험의 clone 원천이 정본 main 절대경로 리터럴 — 작업 트리의 엔진 변조(골든 1,020칸 어긋남)에도 86 passed(발주자 오류 · SPEC-round-b0 v2 §2 문언) — B′ = clone 원천 REPO_ROOT + 작업 트리 델타 미러(status --porcelain -uall) + PYTHON_BIN = sys.executable + 반증 실측 | `D-20260903-03-round-b.md` §6 |
| 2026-09-03-opus-audit-round-b.md | RB-3 | MED | 수용 | 설계 v18 §2.9 T-4 행 「exit 목록에서 verbatim 을 빼면 T-2 가 떨어진다」 거짓 — T-2 는 pointer-resolve 만 지킨다(설계 귀책 · W-1 충분성 논거에 쓰임) — 설계 v19 부록(리포 밖)에 정정 · 행위 결속은 RB-1 처분의 8종 균일 도출식이 대체 | `D-20260903-03-round-b.md` §6 |
| 2026-09-03-opus-audit-round-b.md | RB-4 | LOW | 수용 | D-03 §1 「발주자 오류 0건(이 라운드)」 — 설계 귀책 2건(RB-1·RB-3)이 있으므로 사실 아님 · 「레인이 부딪힌 결정 공백 0」과 혼동 — [정정] 마커 | `D-20260903-03-round-b.md` §1 |
| 2026-09-03-opus-audit-round-b.md | RB-5 | LOW | 수용 | CLAUDE.md §6 관문표 일곱째 행에 「주장하지 않는 것」(값의 참·거짓 = T-7 · 종단 어휘 상등 = T-11 ⑤ · 승인 집합 상등 = T-11 ⑥) 부재 — B′ 문서 hunk | `D-20260903-03-round-b.md` §6 |
| 2026-09-03-opus-audit-round-b.md | RB-6 | LOW | 수용 | 생성기 자기 검증이 expected_check_ids=set(manifest[check_ids]) 로 항진식(Z-2 형) — B′ = READ_CHECK_IDS ∪ ENGINE_READ_CHECK_IDS 실상수 전달(골든 무접촉 · 값 불변) | `D-20260903-03-round-b.md` §6 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-1 | MED | 수용 | 델타 미러가 이름 변경(git mv)에서 옛 경로를 clone 에 남기고 clone 을 「깨끗」으로 신고(unlink 미호출 · 조용한 어긋남 — RB-2 원 결함의 축소판) — B″ ① 옛 경로 unlink + rename 경계 단위 시험 | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-2 | MED | 수용 | 도출식 후건(halt·β 를 뺀 전부가 재시도 대상)이 어느 재정에도 없고 lane-log 2종 배제가 ENGINE_READ_CHECK_IDS 소속이라는 우연에 기댐 — B″ ② 도출식을 「출구 12검사(T29 우주 · 정확히 12 단언) − source-digest(T24·T25) − convergence(T28 β) − lane-log 2종(T22 루프 뒤 합류)」 명시 배제 3집합으로 재작성(각 집합에 재정 좌표) · 새 검사는 T29 우주 단언과 골든이 재정을 강제하므로 기본값 입법 아님(§8 판단 · Owner 사후 확인) | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-3 | LOW | 수용 | SPEC §1.4·§1.16 문장이 정의 없는 「출구 독해 검사 10종」에 기댐 — B″ ③ 명시 도출식 문언으로 교체 | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-4 | LOW | 수용 | RB-6 처방이 항진식을 한 단계 위로 옮겼을 뿐(check_ids 도 같은 두 상수에서 조립) — B″ ④ 생성기 기대 집합을 계약 checks_before_exit 선언 id(다른 층)에서 취함 | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-5 | LOW | 수용 | test_m24_failure_table_contract.py:62 관문 서브프로세스 인터프리터 절대경로 잔존 — B″ ⑤ sys.executable | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-6 | LOW | 수용 | D-03 §1 RB-4 정정 문언의 귀책 계수가 §6 과 다름 — 이 커밋에서 ID 별 귀책으로 재정정 | `D-20260903-03-round-b.md` §1 |
| 2026-09-03-opus-audit-round-b-prime.md | RC-7 | LOW | 수용 | test_m24* 세 모듈이 test_m16 의 sys.path 부작용에 의존해 단독 실행 불가(선재 · B′ 신설 아님) — B″ ⑥ tests/conftest.py 부트스트랩(없으면 신설 · 있으면 추가) | `D-20260903-03-round-b.md` §8 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-1 | MED | 수용 | 렌더 호환 기본값이 convergence_early 부재 시 최종 판정서로 갈음 — reported_by 없는 행위시법 산출물에서 CP1 이 근거 없이 「전건 일치」 선언(T31 발주 반경이 test_m2_read.py 호출점을 빼 레인이 기본값을 발명 — 발주자 귀책) — 라운드 RD ① 기본값 None + test_m2_read 두 호출점 명시 + 귀속 정보 없는 항목이 있으면 「귀속 정보 없음 — 구 판 산출」(일치 선언 금지) + 양성 대조 | `D-20260903-04-t31-t32.md` §9 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-2 | LOW | 수용 | 「조기 판정서 없음 — 구 판 산출」 갈래가 러너에서 도달 불가(load_json 부재 예외)인데 SPEC 이 표면 성질로 서술 — 라운드 RD ② read.py 호출부 isfile 가드 한 줄 + SPEC 문언을 「러너 경로에서는 발생하지 않고 구 산출 재렌더·픽스처용」으로 | `D-20260903-04-t31-t32.md` §9 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-3 | LOW | 수용 | 도출식 시험 T22 결속의 발화 불가 연언 `"retry" in row`(계약은 action 값으로 재시도를 적고 골격 시험이 키 집합을 고정) — 라운드 RD ③ action 이 retry( 로 시작하지 않음 + then 부재로 교체 + 양성 대조 | `D-20260903-04-t31-t32.md` §9 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-4 | LOW | 수용 | T32 accept 픽스처가 기존 accept 와 바이트 동일 복제(판별력 0 · 발주문 「복제해 그 필드만」 지시가 accept 쪽에선 복제만 낳음 — 발주자 귀책) — 라운드 RD ④ read-b 정본 지정 인스턴스로 교체(둘째 enum 값 양성 대조) + D-04 §2 인용 정정 | `D-20260903-04-t31-t32.md` §9 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-5 | LOW | 수용 | §5 ③ 이 스키마에서 지운 「provenance.read_runs[0] 이 곧 정본」 문장이 run_checks.py:138-140 docstring 에 잔존 · 폴백 우회 시험(test_m1_reader:1231)에 좁아진 주장의 표지 없음 · 폴백 타는 호출점 둘(test_m1_reader:1191 · test_m2_read:2520) — 라운드 RD ⑤ docstring 실물 정정(reader/ · docstring 만 · AST 동일 실증) + 시험 주석 + 두 호출점도 canonical 명시 · 백로그 문언 확장 | `D-20260903-04-t31-t32.md` §9 |
| 2026-09-03-opus-audit-round-b2-t31.md | RD-6 | LOW | 수용 | RC-6 재정정이 RB-2 귀책을 원문 「설계(발주자)」 대신 「발주자(총괄)」로 인용 — 이 커밋에서 원문 라벨로 재재정정 | `D-20260903-03-round-b.md` §1 |
| 2026-09-05-opus-audit-round-rd.md | RE-1 | MED | 수용 | RD-3 의 교체 단언 not startswith(retry() 가 action == escalate 와 연언되어 다시 항진식 — 발주문 §1 ③·처분표 §9 가 그 술어를 문언으로 지정(발주자 1차 귀책) — 라운드 RE ① 죽은 연언 삭제 + 이 단언이 고유하게 무는 변조를 실측해 시험 주석에 기재 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-rd.md | RE-2 | LOW | 수용 | RD-3 양성 대조(action retry(1) + then escalate)가 수리 전 단언으로도 붉어 폐쇄 증거가 아니다 — 가르는 변조는 then 단독(발주자 귀책) — 발주문 골격 ⒀ 신설(차별 대조 = 수리 전 초록·수리 후 붉음) + 라운드 RE 의 양성 대조를 전부 차별 대조로 지정 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-rd.md | RE-3 | LOW | 수용 | 10-b 갈래 사슬(귀속 없음·전건 일치·갈린 신고)에 else 가 없어 reported_by 길이 3 이상·문자열에서 블록 본문이 비어 승인자가 읽을 것이 없다(오늘 런은 스키마 enum+uniqueItems 가 막음) — 라운드 RE ② else 갈래 신설 + 「블록은 언제나 한 줄을 낸다」 시험 + convergence_early 형 표기 dict 또는 None(감사자 ⒝) · 혼재 시 표 억눌림은 실런 정의역 밖이라 현행 유지·기록 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-rd.md | RE-4 | LOW | 수용 | RD-2 의 isfile 가드가 어떤 시험으로도 판별되지 않고(가드 삭제 후 775 초록) 발화하면 갓 돈 런에 「구 판 산출」 거짓 출처를 내며 SPEC 의 「재렌더」 도구는 실물 0(발주자·총괄 처분 귀책) — 라운드 RE ③ 가드 제거·러너는 조기 판정서 부재를 실패로(구 판 갈래는 render() 직접 호출 전용) + 부재 시 실패 시험 + SPEC §1.5 문언에서 재렌더 삭제 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-rd.md | RE-5 | LOW | 수용 | D-04 §10 재현표의 git status 분해 「M 10 · D 1 · ?? 1」 은 합 12 로 앞의 11 과 모순 · 실물 M 9(총괄 기록) — 이 커밋에서 정정 마커로 고침 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-rd.md | RE-6 | LOW | 수용 | 9817bec 의 §5 편집이 폴백 항목 말미의 「제거는 reader 이식 단위 변경 · READER-VERSION 상호 체크 · N15」 단서를 둘째 항목(출구 재시도 행위 시험) 말미로 옮겨 거짓 문장을 만들었다(총괄 기록) — 이 커밋에서 원 자리로 되돌림 | `D-20260903-04-t31-t32.md` §12 |
| 2026-09-05-opus-audit-round-re.md | RF-1 | MED | 수용 | RE-3 의 허용 실행값 확장(전건 일치·갈린 신고 갈래가 read-a·read-b 외 값을 거절)은 실질 수리인데 두 곳을 원복해도 전건 초록 — 발주문 §2 의 RE-3 대조가 길이 3 만 지정해 그 조건을 태우지 않음(골격 ⒀ 위반 · 발주자 1차) — 라운드 RF ① 판별 픽스처(read-c·read-d → 규격 밖 1·전건 일치 0 · [read-c] → 규격 밖 1·표 0) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-2 | MED | 수용 | 감사자 ⒜ 「고유 변조 없음」은 발주문이 탐색 공간을 계약 단독 변조로 못박아 구조적으로 결정된 답(관문 G1 이 계약 기계 필드 전량을 동결 사본과 대조) · 실제 고유 관할 = 계약과 관문 사본의 협조 편집(변조 H) · 총괄이 레인의 「계약」 한정어를 §13·커밋·HANDOFF 에서 떨어뜨림 — §13·HANDOFF 정정(이 커밋) + 라운드 RF ② T22 단언 위 주석(고유 관할 · 계약 단독 변조는 G1 이 항상 잡음) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-3 | MED | 수용 | §13 정정이 든 기제 「같은 작업 트리에서의 동시 pytest 간섭」이 코드로 뒷받침되지 않음 — law_repo 는 tempfile.mkdtemp(tmpfs /tmp) · 시험은 리포 트리에 쓰지 않음 · 공유 자원은 머신 수준(tmpfs 1.5 GB · RAM 2.9 GB)이라 다른 worktree 둘이어도 같은 경합 — §13 재정정(확인된 것 = 중복 인스턴스 실재·시각 겹침 · 기제 = 머신 수준 자원 경합 가설) + 기억 파일 정정 + 골격 ⑾ 추기(TMPDIR 도 홈 fs) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-4 | LOW | 수용 | 혼재(정상 길이 1 항목 + 규격 밖 항목)에서 갈린 신고 표만 나고 규격 밖 항목이 한 마디 없이 사라짐(수리 전후 동일 · 처분 §12 가 이 혼재를 세지 않음) — 라운드 RF ③ 규격 밖 항목이 하나라도 있으면 표와 함께 「규격 밖 N건」 줄을 낸다 | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-5 | LOW | 수용 | reported_by [read-a, read-a] 가 「두 실행의 미분류 신고가 전건 일치」를 거짓 선언 — 허용값 소속은 넣고 서로 다름은 넣지 않아 uniqueItems 이탈이 통과(오늘은 스키마가 막음) — 라운드 RF ④ 서로 다름 조건(중복 = 규격 밖) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-6 | LOW | 수용 | 전역성 시험의 「N 이 맞음」 단언이 판별력 0(케이스 둘 다 항목 1건 · N 을 len 으로 바꿔도 초록) — 라운드 RF ⑤ N ≠ 항목 수인 픽스처(길이 3 두 건 → N=2 · [a,b]+[read-c] → N=1) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-7 | LOW | 수용 | HANDOFF §0 16차 줄이 정정 뒤에도 「일시 실패 4건 [미확인]」으로 남아 두 줄 아래 ⓠ 와 모순(총괄 기록) — 이 커밋에서 정정 | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-opus-audit-round-re.md | RF-8 | LOW | 수용 | 골격 ⒀ 이 「변조 = 수리 전 초록·수리 후 붉음」 한 방향만 정의하고 이 라운드가 쓴 새 시험 방향(수리 전 붉음·후 초록)은 정의 밖 · 발주문 §2 머리(갈린다)와 RE-1 항목(동일)이 모순(발주자) — ⒀ 문언 개정(두 방향 + 순수 등가 수리는 등가 증명으로 대신함을 명시 · 이 커밋) | `D-20260903-04-t31-t32.md` §15 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-1 | HIGH | 수용 | 발주문 수락 계수가 실물과 다름 — 기존 reject 32(발주문 33) · 신설 뒤 cases=50 REJECT_OK 33/33 ACCEPT_OK 15/15(발주문 34/34 는 합계 불일치) · 지정 문자열은 관문 마지막 줄 아님 · 「accept 전부 빈 메모」는 convergence accept 2건으로 한정(발주자) — 4차 정정 발주에 계수·문구·범위 정정 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-2 | HIGH | 수용 | 「귀속 없음 현행 유지」의 실제 술어 not entry.get(reported_by) 는 null·false·0·빈 문자열·빈 객체도 귀속 없음인데 이들은 동시에 규격 밖(list 아님) — 우선 규칙 미지정(발주자) — 4차 정정: 귀속 없음 술어가 하나라도 참이면 귀속 없음만 출력 · 규격 밖·표·일치는 그 조건이 거짓일 때만 · 빈 전체 집합은 전건 일치 명문화 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-3 | MED | 수용 | 변조 H 는 주석 변경의 차별 대조가 아니라 주석 주장의 실증 · §4 「등가 증명 항목 없음」이 ⒀ 개정판 위반 · A② 새 시험의 「수리 전 붉음」은 중복·혼재 케이스만 성립(나머지는 보충 시험)(발주자) — 4차 정정: 대조마다 코드 판본·시험 판본·변조를 고정 · H 는 「등가 확인 + 주장 실증」으로 분류 · 케이스별 수리 전 색 명시 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-4 | HIGH | 수용 | 3차 정정(6파일 행위시법 · SPEC 좌표 · cases 50)이 재정 원장 §2·§4 와 재감사 3 초안 §1·Q2 에 전파되지 않음(발주자·총괄 기록) — 원장 정정 마커(이 커밋) + 초안 정정 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-5 | MED | 수용 | 영속 시험의 수리 전 기준을 git show HEAD 로 지정하면 커밋 뒤 자기 비교로 퇴화(발주자) — 4차 정정: 행위시법 시험은 이동 기준 없이 「현행 스키마 아래 6파일의 거부 집합 = 알려진 집합(cim-fp-3 convergence.json · required text_status·reported_by) · read_run·maxItems 키워드 위반 0」으로 고정 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-6 | MED | 수용 | RF-4 「규격 밖 줄 먼저 · 표 이어서」의 순서를 판별하는 대조가 없음(순서만 뒤집은 판본이 통과)(발주자) — 4차 정정: 혼재 시험에 줄 위치 < 표 머리 위치 단언 + 순서 뒤집기 변조 대조 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-rf-t35.md | MB-7 | LOW | 수용 | D-04 §15 가 약속한 T36 원장 ⓠ 행의 RF-3 주석이 원장에 없음(총괄 기록) — 이 커밋에서 원장 §3 ⓠ 행에 추기 | `D-20260903-04-t31-t32.md` §16 |
| 2026-09-05-astra-m1b-fix4.md | MC-1 | HIGH | 수용 | 4차 F5 차별 대조표가 코드 판본 축과 시험 판본 축을 구별하지 않고 변조 8종에 같은 색을 강제 — B⑴·B⑵·Aⓔ 는 「같은 새 시험 × 구·신 구현」(붉음→초록) · 순서 뒤집기는 HEAD 에 동시 출력이 없어 적용 불가(발주자) — v2: 행마다 종류 (i) 같은 새 시험 × 구·신 구현 / (ii) 같은 신 시험 × 변조 구현 / 등가 · 고정 대상 · 변경 축 명시 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-fix4.md | MC-2 | MED | 수용 | 귀속 없음 우선·미분류 0건 명문화 시험은 분기점 HEAD 에서도 초록인 보충·회귀 시험인데 「수리 전 붉음」으로 분류(발주자) — v2: A-회귀(보충)와 A-차별(i)로 분리 · 우선 가드 제거는 (ii) 변조 Aⓕ 로 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-fix4.md | MC-3 | MED | 수용 | Aⓑ 「길이 3 두 건 붉음」은 정상 계수 2 = 변조 2 라 N 치환을 판별하지 못함(발주자) — v2: 판별 사례 = [a,b]+[c] · [a]+[a,b,c] · 길이 3 두 건은 회귀 사례 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-fix4.md | MC-4 | LOW | 수용 | F1 이 MB-1 범위 정정(빈 메모 전제 = convergence accept 2파일 · 12 는 필드 부재)을 빠뜨림 · SUMMARY 지정 문자열은 접두부(전체 행은 schemas=5 접미)(발주자) — v2: 3차 B② 문언 대체 명시 · 접두부 대조 + 전체 행 인용 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-fix4.md | MC-5 | LOW | 수용 | 수락의 grep -n git show tests/ 는 비재귀(exit 2) · 3차 행위시법 시험은 deepcopy 로 이전 스키마를 메모리 복원해 비교하고 next 로 첫 오류만 봄(F4 미충족)(발주자·레인) — v2: grep -rn 무일치 exit 1 · 복원 비교 제거 · iter_errors 전량이 required 인지 단언 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-fix4.md | MC-6 | LOW | 수용 | 「형태표 25종」은 도전자 1차 원문의 계수 오류(묶인 입력 전개 시 구체 30사례)이고 정정판이 그 계수를 수락에 그대로 씀(도전자·발주자) — v2: 고유 case ID 30사례(G 9 · I1 15 · I2 1 · I1→T 1 · A 3 · T 1) 명시 · 사례별 식별 | `D-20260903-04-t31-t32.md` §17 |
| 2026-09-05-astra-m1b-audit3.md | MD-1 | MED | 수용 | 재감사 3 발주문이 재현표를 §16 · 레인 보고를 §17 로 지정 — 실물은 §18 재현표 · §19 3차 보고 · §20 4차 보고(final-4.txt 정규화 동일) · 기록 커밋 반경에 RULINGS-LEDGER.md 누락(발주자) — 발주문 §1·Q4 좌표 정정 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-astra-m1b-audit3.md | MD-2 | MED | 수용 | Q5 가 4차 v2 로 대체된 3차 발주문을 독립 수락 기준으로 다시 심판하게 함 — 유효 발주(3차 + v2 대체)를 심판하고 보존된 구 문언은 정정 누락일 때만 신규로(발주자) — Q5 문언 정정 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-astra-m1b-audit3.md | MD-3 | MED | 수용 | RF-1 변조를 「허용값 조건 두 곳 삭제」로 지정했으나 현행 구현은 세 자리(singleton 선별 · 규격 밖 계수 · 전건 일치)(발주자) — Q1 ⓐ 세 자리 명시 · I05·I06 각각 보고 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-astra-m1b-audit3.md | MD-4 | LOW | 수용 | 「형태 17종」·「25종」 낡은 계수 잔존(현행 = 고유 ID 30사례) · 「아무 입력」의 분석 범위(reported_by JSON 값 · 항목은 객체) 미명시 · 표본 30 은 완비 증명이 아님(발주자) — Q1 ⓑ 문언 정정 · 완비 논증 요구를 별도 항목으로 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-astra-m1b-audit3.md | MD-5 | MED | 수용 | 발주문이 T22 파일을 「주석만」으로 전제했으나 RF 커밋에는 다른 시험 두 줄 deepcopy(schema)→deepcopy(dict(schema)) 변경이 있음 — 발주자의 파일 전체 grep 수락 조건이 유도한 무해한 기계 정리(T22 함수 AST 동일) · MC-5 검사는 행위시법 함수의 데이터 흐름으로 한정(발주자·레인) — 발주문에 예외 사실 명시 · Q3 에서 반경·필요성 판정 요구 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-astra-m1b-audit3.md | MD-6 | LOW | 수용 | 96f7582 는 「문서 넷」이 아니라 감사 원문 반입 포함 다섯 파일(발주자) — 문언 정정 | `D-20260903-04-t31-t32.md` §21 |
| 2026-09-05-opus-audit-round-rf-t35.md | RG-1 | MED | 수용 | RF-2 처분이 약속한 §13 정정 마커(「없음」은 계약 단독 변조 공간 안의 답 — 한정어 복원)가 없고 HANDOFF 16차 줄도 무한정 「⒜ 고유 변조 없음」 그대로 — 변조 H 실재로 그 문장은 거짓(총괄 기록) — 이 커밋에서 §13·HANDOFF 16차에 정정 마커(구 문언 보존) | `D-20260903-04-t31-t32.md` §22 |
| 2026-09-05-opus-audit-round-rf-t35.md | RG-2 | LOW | 수용 | 비해시 중복 검사 _has_duplicate_values 는 두 호출점 모두 허용값 검사에 가려 도달 불능 — set() 판본으로 원복해도 810 전건 초록 · I14 픽스처는 그 속성을 태우지 못함(골격 ⒀ 재발 · 발주자 수락 설계 1차 · M1b medium 3런이 놓친 한 건) — 라운드 RG: 헬퍼 단위 시험(빈 객체 둘 → True · set 판본은 TypeError) + 도달 불능 방어임을 시험 docstring 에 명기 | `D-20260903-04-t31-t32.md` §22 |
| 2026-09-05-opus-audit-round-rf-t35.md | RG-3 | LOW | 수용 | 재감사 3 발주문 §1 의 96f7582 괄호가 같은 문구를 두 번 듦(MD-6 정정 잔재 · 사실 오류 없음)(발주자) — drafts 발주문 정정(이 커밋에서 기록) | `D-20260903-04-t31-t32.md` §22 |
| 2026-09-05-astra-m1b-rg.md | ME-1 | LOW | 수용 | RG 발주문 §2 (ii) 가 신 시험 고정 × 엔진 변조로 적혔으나 실질 변경분이 시험 추가라 ⒀ 축은 「같은 set() 변조 × 구 시험 → 신 시험」이어야 하고 네 칸 기대 결과가 없었다(발주자) — 발주문 §2 를 네 칸 표로 재작성 + 보강 단언(비인접·역순·리스트 원소) | `D-20260903-04-t31-t32.md` §23 |
| 2026-09-05-astra-m1b-audit4.md | MF-1 | LOW | 수용 | Q1ⓑ 가 ME-1 의 네 칸 축(같은 set() 변조 × 구 시험 d29c8a2 초록 → 신 시험 붉음)을 감사자 직접 재현으로 요구하지 않음(발주자) — 발주문 정정 | `D-20260903-04-t31-t32.md` §26 |
| 2026-09-05-astra-m1b-audit4.md | MF-2 | LOW | 수용 | 감사 대상 커밋 메시지 6173b96 의 「레인 보고 전문은 §24」는 §25 의 오기 · 정정 마커 없음(총괄 기록) — D-04 §24 말미 정정 마커 + 발주문 Q3 명시 | `D-20260903-04-t31-t32.md` §26 |
| 2026-09-05-astra-m1b-audit4.md | MF-3 | LOW | 수용 | 발주문 「단언 셋」 — 실물은 ME-1 보강 뒤 8단언(발주자) — 발주문 정정 | `D-20260903-04-t31-t32.md` §26 |
| 2026-09-05-astra-m1b-audit4.md | MF-4 | LOW | 수용 | 백로그 좌표 run_checks.py:168 은 현재 주석 행 · 폴백은 :171(발주자) — 발주문 정정 · D-04 §5 좌표는 「:168 근방」으로 읽되 이 마커로 기록 | `D-20260903-04-t31-t32.md` §26 |
| 2026-09-05-astra-m1b-m2a1.md | MG-1 | BLOCKER | 수용 | G-5 가드(shadow_pointer.terminated)가 조기 상신 뒤 T17 승인 봉투 재진입을 StageError 로 끊음 — 종결·LanePending·봉투 대기의 상태 전이·원장 기입 시점이 미정의(발주자 · 「신규 재정 0」 전제 거짓) — G-5 를 라운드에서 분리 · 설계 메모 + Owner 상신(decision-brief) | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1.md | MG-2 | HIGH | 수용 | 사후 변조 시험이 response_digest 를 바꾸면 값 검사 관할 밖(발주자) — v2: 실재 request.md 행의 request_digest 를 파일만 재독·변조 · 메모리 저널 불변 · lane-log.digest-value-mismatch 단언 | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1.md | MG-3 | HIGH | 수용 | 검사 뒤 finally 재기록이 변조 탐지 경로에서 검사본을 덮음 · 검사 실패 뒤 로그 보존·재독 오류 미명시(발주자) — v2: 출구에서 게시한 로그는 검사 뒤 덮지 않고 미게시 경로만 finally 기록 · 실패·재독 오류 각각 단언 | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1.md | MG-4 | HIGH | 수용 | 포인터 없는 구 런 실재 · append 뒤 포인터 기록 실패 경로 · 단독 판정 필드 없음(발주자) — G-5 설계 메모의 상신 항목(구 런·기입 실패 처분)으로 | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1.md | MG-5 | MED | 수용 | 「digest-value 또는 shape」 수락이 한 검사만 디스크를 읽어도 통과 · G-5 행 수 불변은 내용 편집 미검출(발주자) — v2: 두 검사 배선 각각 원복 대조 · G-5 는 메모로 | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1.md | MG-6 | LOW | 수용 | §2 (i) ⓐ 자기 정정 문장 · 대조 축 표 · 환경 문안 ⑾⑿ 미전사(발주자) — v2 정리 | `D-20260903-04-t31-t32.md` §28 |
| 2026-09-05-astra-m1b-m2a1v2.md | MH-1 | HIGH | 수용 | 「게시 뒤 덮지 않음」과 「로그 보존」이 외부 삭제 훅에서 충돌 · 보존 보장 범위 미한정(발주자) — v3: 손상 = 바이트 보존 + StageError · 삭제 = 부재 확인 + StageError · 자동 복원 금지 · 보장은 try 진입 뒤 | `D-20260903-04-t31-t32.md` §29 |
| 2026-09-05-astra-m1b-m2a1v2.md | MH-2 | HIGH | 수용 | ⓒ 실패 경로를 통째로 회귀로 분류 — 재독 오류 → StageError 는 새 시험(구 붉음 → 신 초록)(발주자) — v3: ⓒ1 회귀 · ⓒ2 ⓐ 포함 · ⓒ3 새 시험 | `D-20260903-04-t31-t32.md` §29 |
| 2026-09-05-astra-m1b-m2a1v2.md | MH-3 | MED | 수용 | 검사 서명을 rows 전용으로 바꾸는 선택지가 기존 직접 호출 시험 14곳을 깨 반경 초과(발주자) — v3: LaneJournal 서명 유지 · 재독 rows 를 별도 LaneJournal 에 담아 전달 | `D-20260903-04-t31-t32.md` §29 |
| 2026-09-05-astra-m1b-m2a1v2.md | MH-4 | MED | 수용 | 파싱은 되나 list[dict] 가 아닌 재독 본문(null · [0])의 처분 부재(발주자) — v3: 검사 진입 전 형태 검사 → StageError · 손상 바이트 보존 | `D-20260903-04-t31-t32.md` §29 |
| 2026-09-05-astra-m1b-m2a1v2.md | MH-5 | LOW | 수용 | 골격 ⑿ 전사 불완전(setsid 분리 · EXIT 회수)(발주자) — v3 §3 보완 | `D-20260903-04-t31-t32.md` §29 |
| 2026-09-05-astra-m1b-m2a1-audit.md | MI-1 | MED | 수용 | 재감사 5 발주문 Q5 가 M1b 원문 바이트 대조 대상을 D-04 §28·§29(처분 요약)로 지정 — 원문은 lessons 파일 끝(발주자 · MD-1 계열 재발) — 대조 좌표를 lessons 원문 ↔ FINAL 로 정정 | `D-20260903-04-t31-t32.md` §32 |
| 2026-09-05-astra-m1b-m2a1-audit.md | MI-2 | MED | 수용 | Q1ⓒ 경로표에 ⑨ 전 접지 게이트 미진입 조기 반환(플래그 거짓 → finally 기록)과 게시 뒤 일반 예외(플래그 참 → 무덮어쓰기) 누락(발주자) — 경로를 이름으로 고정해 추가 | `D-20260903-04-t31-t32.md` §32 |
| 2026-09-05-fable-audit-round-m2a1.md | RI-1 | LOW | 수용 | 플래그를 게시 앞에 세우는 변조(V6)를 새 시험 8건이 못 잡음 — 게시 쓰기 일시 실패 창의 finally 폴백 소실 · T3 목적 불변(발주자) — ⓓ1 꼴 시험 1건을 라운드 M2a-2 발주문 ⑤ 로 이월 | `D-20260903-04-t31-t32.md` §33 |
| 2026-09-05-fable-audit-round-m2a1.md | RI-2 | LOW | 수용 | DISPOSITIONS MG-1 격 HIGH 는 원문·§28 BLOCKER 의 전사 오기(총괄 기록) — 이 커밋에서 셀 정정 · 정정 마커 | `D-20260903-04-t31-t32.md` §33 |
| 2026-09-05-fable-audit-round-m2a1.md | RI-3 | LOW | 수용 | D-04 §32 「M1b 8런 누계 40」은 37 의 계수 오기(총괄 기록) — §32 정정 마커 | `D-20260903-04-t31-t32.md` §33 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-1 | BLOCKER | 수용 | 종결 판정의 「판정 불가」(손상·형태 위반·읽기 오류·루트 거부·JSONL 손상행)를 근거 부재와 같은 비종결로 처리해 재호출을 허용 — T38 밖 값(발주자) — v2: 판정 불가 = fail-closed StageError(총괄 재량 · 사후 확인 ⓦ) | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-2 | MED | 수용 | awaiting 을 모든 포인터에 상시 null 로 싣는 확대는 T38 문언 밖 · ⓔ 회귀 분류 충돌(발주자) — v2: 조기 상신 포인터에만 싣고 그 밖은 필드 부재 유지 | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-3 | HIGH | 수용 | ⓓ 변조에서 m22 봉투 4시험 「여전히 초록」 기대는 거짓 — 첫 호출 참 포인터 → 두 번째 호출 가드 StageError 로 붉음(발주자 · MG-1 기제 재누락) — v2 대조표 정정 | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-4 | HIGH | 수용 | 정상 통주 뒤 ensure_read_dirs 는 목록·mtime 불변이라 「가드 뒤로 이동」 변조를 지정 관측량으로 판별 불가(발주자) — v2: 호출 계수 0(디렉터리 생성·레인 dispatch·append·writer) + 파일 집합·바이트·mtime 병용 | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-5 | MED | 수용 | 「포인터 있으면 그 값으로 즉시 반환」 오판정이 ⓐ~ⓕ 를 통과 — 참 포인터 단독 · 거짓 포인터+동일 ID 원장 행 배치 부재(발주자) — v2: ⓖⓗ 추가 | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2.md | MJ-6 | LOW | 수용 | 「시험 ③ⓐ」는 ④ⓐ 의 절 번호 오기(발주자) — v2 정정 | `D-20260903-04-t31-t32.md` §34 |
| 2026-09-05-astra-m1b-m2a2v2.md | MK-1 | HIGH | 수용 | ⓗ 배치가 convergence.json 을 남겨 정상 구현이 근거 ⑵ 에서 차단 — 「근거 = 원장」 단언이 정상 구현부터 붉음(발주자) — v3: 판정서도 삭제 · 원장 행만 유지 | `D-20260903-04-t31-t32.md` §35 |
| 2026-09-05-astra-m1b-m2a2v2.md | MK-2 | HIGH | 수용 | ⓘ 「원장 손상행」 사례는 참 포인터가 남아 ⑴ 종결 재호출로 끝나 「판정 불가」에 도달 불가(발주자) — v3: 근거별 독립 사례 ⓘ1(포인터 손상) · ⓘ2(원장 손상 · 포인터·판정서 제거 · 손상행 앞/뒤) | `D-20260903-04-t31-t32.md` §35 |
| 2026-09-05-astra-m1b-m2a2v2.md | MK-3 | MED | 수용 | 원장 행의 비객체·run_id 누락/자료형 위반 처분 미정 · 부재/유효한 비참/판정 불가 세 갈래 미명시(발주자) — v3 §1 ① 분기표 | `D-20260903-04-t31-t32.md` §35 |
| 2026-09-05-astra-m1b-m2a2v2.md | MK-4 | MED | 수용 | ⓓ 최종 포인터 단언에 awaiting null 잔존 — MJ-2 부분 폐쇄(발주자) — v3: awaiting not in pointer | `D-20260903-04-t31-t32.md` §35 |
| 2026-09-05-astra-m1b-m2a2v2.md | MK-5 | LOW | 수용 | §2 「구는 원장 2행」은 ⓖ 1행·ⓘ 3줄 사례에 안 맞음 — 계수 대상 혼용(발주자) — v3: 「구 구현은 재호출을 차단하지 않는다」 · 행 수는 사례별 | `D-20260903-04-t31-t32.md` §35 |
| 2026-09-05-astra-m1b-m2a2-audit.md | ML-1 | MED | 수용 | 재감사 6 발주문 Q2 고안 변조 예시 6종 중 4종은 기존 시험이 이미 잡는 자리 — 미피복 경계(비참 판정서 · 접두만 같은 run_id · 판정서/읽기 오류 · 루트 거부)로 정정(발주자) | `D-20260903-04-t31-t32.md` §38 |
| 2026-09-05-astra-m1b-m2a2-audit.md | ML-2 | MED | 수용 | Q1① 원장 형태 프로브에 포인터·판정서 제거 조건 부재 — 앞 근거 단락으로 원장 검사 실행 증거가 안 됨(발주자 · MK-2 계열 재발) — 독립 배치 + 기대 문언 | `D-20260903-04-t31-t32.md` §38 |
| 2026-09-05-astra-m1b-m2a2-audit.md | ML-3 | LOW | 수용 | Q3 실행 집합(m26 + ⑤ = 16노드)이 §36 계수(두 파일 24노드 · 13/11)와 불일치(발주자) — 두 파일 전건으로 정정 | `D-20260903-04-t31-t32.md` §38 |
| 2026-09-05-astra-m1b-m2a2-audit.md | ML-4 | LOW | 수용 | §36 「read.py +176/−10 · m26 10함수」는 +177/−9 · 11함수 의 오기(총괄 기록) — 정정 마커 | `D-20260903-04-t31-t32.md` §38 |
| 2026-09-05-fable-audit-round-m2a2.md | RJ-1 | MED | 수용 | 근거 ⑶ 원장 행의 생산 경로(링크된 worktree · shadow_root=None · P-U1 배치) 미피복 — D7(구 폴백 해석기)·D6(shadow_root None 이면 ⑶ 생략) 변조가 스위트 생존 · D7 은 주 원장 2행 = G-5 증상 재현(발주자 · 시험 공백) — 수리 라운드 M2a-3: worktree 배치 재호출 시험 1건 | `D-20260903-04-t31-t32.md` §39 |
| 2026-09-05-fable-audit-round-m2a2.md | RJ-2 | LOW | 수용 | 「다른 run_id 행 = 유효한 비참」 음성 사례 부재 — D2 접두 일치 · D2b 아무 행 생존(발주자) — M2a-3: 무관 id·접두 id 행 심고 가드 통과 1건 | `D-20260903-04-t31-t32.md` §39 |
| 2026-09-05-fable-audit-round-m2a2.md | RJ-3 | LOW | 수용 | 비참 판정서(phase != full) 배치 부재 — D1 생존 · 실물 위반 없음(발주자) — M2a-3: phase early 판정서 단독 배치 가드 통과 1건 | `D-20260903-04-t31-t32.md` §39 |
| 2026-09-05-fable-audit-round-m2a2.md | RJ-4 | LOW | 수용 | 판정 불가 분기 중 판정서 손상·형태 / 읽기 오류 / 루트 거부 3종 미피복 — D3·D4·D5 생존 · ⓦ 핀 절반(발주자) — M2a-3: 3건 추가(ⓦ 뒤집히면 기대값 반전) | `D-20260903-04-t31-t32.md` §39 |
| 2026-09-05-fable-audit-round-m2a2.md | RJ-5 | LOW | 수용 | _write_shadow_pointer 의 refused 기록 분기가 run() 에서 도달 불능(ⓦ 부수 효과 · 결함 아님) — ⓦ 사후 확인에 병기(docstring 정정 또는 거부 기록 유지 = Owner) · 코드 무변경 | `D-20260903-04-t31-t32.md` §39 |
| 2026-09-05-astra-m1b-m2a3.md | MM-1 | HIGH | 수용 | ⓙ 임시 법 리포(make_law_repo = contracts + READER-VERSION)에 절차 문서 reader/procedure/*.md 가 없어 READ 통주가 LaneContractError 로 끊김 · run_read_stage 는 shadow_root=None 을 격리 루트로 덮어씀(발주자) — v2: fixture 안에서 worktree 에 reader/ 보충 + 임시 커밋 · read_stage.run 직접 호출 · ⓜ3 동일 보충 | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3.md | MM-2 | MED | 수용 | ⓦ 반전 시 기대값 목록이 ⓜ 셋뿐이고 「진행」으로 뭉뚱그림 — ⓜ2 IsADirectoryError 누출 · ⓜ3 dispatch 뒤 루트 예외 · 기존 ⓘ1~3 문언·근거 변경 누락(발주자) — v2: ⓦ 의존 목록 + 반전 표 | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3.md | MM-3 | LOW | 수용 | RJ-4 「판정서 손상/형태」의 형태 분기(비객체 · phase 비 str) 누락 · D3 전사 축약(발주자) — v2: ⓜ1 파라미터 3 · D3 전체 | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3.md | MM-4 | LOW | 수용 | §4 가 「헬퍼 호출만·시험 추가만」을 검사 못 함(발주자) — v2: m26 hunk 추가만(−0) · m2·m16 불변 diff 대조 · 다른 시험 파일 변경 면제 없음 | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3.md | MM-5 | LOW | 수용 | read.run() 서명 좌표 :1477 은 구판(발주자 · MB·MD 계열) — v2: :1622(repo :1628 · shadow_root :1629) | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3.md | MM-6 | LOW | 수용 | 골격 ⑿ 「발주문 원본 홈 fs 보존」 미전사(발주자 · MH-5 계열) — v2 §3 | `D-20260903-04-t31-t32.md` §40 |
| 2026-09-05-astra-m1b-m2a3-audit.md | MO-1 | LOW | 수용 | 재감사 7 발주문 Q3 「FINAL 부재」는 오기 — 중단 레인의 FINAL 은 0바이트로 실재 · 완료 보고 없음(발주자 · MD-1·MI-1 계열) — 문안 정정 + 변조별 실패 집합 표·비겹침 문안 보강 | `D-20260903-04-t31-t32.md` §44 |
| 2026-09-05-astra-m1b-m2b1.md | MP-1 | HIGH | 수용 | m16 삭제 좌표 `:744~747` 은 ② 고아 원장 검출이고 ③ 생산 지문은 `:749~752`(발주자 좌표 오기) — v2: 삭제 = `:722~723`·`:749~752` 만 · `:744~747` 보존 · docstring 「아래 ③」 → 헬퍼 종료 지문 검사 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-2 | HIGH | 수용 | 조상 `With` 판정이 `with` 안 지연 함수 정의·헬퍼 인자 위치의 `shadow_root=None` 호출을 통과(발주자 규칙 결함) — v2: 보호 = `With.body` 직계 · FunctionDef/Lambda/ClassDef 경계 불통과 · context 식·인자 위치 제외 · 음성 칸 (f)(g) 추가 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-3 | MED | 수용 | 안 보는 축 목록 불완전 — 엔진 별칭·재바인딩·동적 전달(`m26:186`) 미탐 · 헬퍼 `as g` 오탐 · 동명 사칭 오인식(발주자) — v2: 헬퍼·관문 docstring 에 세 사각 명기 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-4 | MED | 수용 | ⓙ 교체 범위 `:388~402` 가 주 트리 equality(`:392~395`)·`expected_ledger` 정의(`:398`)까지 지움 — 헬퍼 ② 는 tmp 포함만 봐 증명력 하락(발주자) — v2: 둘 보존 · 헬퍼와 중복되는 격리·지문 보호만 교체 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-5 | MED | 수용 | §2 P′ 의 편집 상태 미명시 — ①ⓑ 만 적용하면 기존 4 호출도 offender 라 P′ 초록 불가(발주자) — v2: 순서 = 편집 전 P → ①~④ 완료 → P(offender = 프로브 하나) → P′ · 동일 python·옵션 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-6 | MED | 수용 | §4 AST 스크립트가 worktree `.venv` 상대 경로·`assert` 사용(CLAUDE.md §3 위반 · `-O` 공허) · 전 docstring 제거라 지정 함수 밖 docstring 변경 허용(발주자) — v2: 절대 python · 명시 비교+exit · `--numstat` 삭제 0 + hunk 범위 `_write_shadow_pointer` docstring 안 · 「docstring 제외 구조 상등」으로만 보고 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-7 | MED | 수용 | 헬퍼 `finally` 에서 `pytest.fail` 이 본문 예외를 덮음 — 「본문 예외 그대로 전파」와 모순(발주자) — v2: 지문 같으면 본문 예외 전파 · 다르면 원장 변경 실패 우선(본문 예외 = `__context__`) | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1.md | MP-8 | LOW | 수용 | 헬퍼 docstring 지시문 「세 시험이 4중 보호를 세 벌 짰다」 거짓 — ⓙ만 완전 · m16 부분 · ⓜ3 지문 없음(발주자) — v2: 「흩어져 있거나 빠져 있던 보호를 공통 헬퍼로 완성」 | `D-20260905-02-pdm2b-seats.md` §5 |
| 2026-09-05-astra-m1b-m2b1v2.md | MQ-1 | HIGH | 수용 | v2 ⒜ 「처음 만나는 With 가 헬퍼」와 「다른 With 는 통과」 상충 — 전자대로면 pytest.raises 안의 정당한 호출 둘이 offender · (b) 칸이 중첩을 안 재 잘못된 구현도 통과(발주자) — v3: 헬퍼 아닌 With 는 건너뛰고 첫 헬퍼 With 까지 탐색 · body 진입 필수 · (b) 에 중첩 pytest.raises | `D-20260905-02-pdm2b-seats.md` §6 |
| 2026-09-05-astra-m1b-m2b1v2.md | MQ-2 | MED | 수용 | §4 hunk 경계 오기 — :2253 직전 삽입의 구 좌표는 2252,0 · 2253,0 은 따옴표 뒤라 docstring 밖 주석 삽입이 세 검사 통과(발주자) — v3: 헤더 `@@ -2252,0 +2253,N @@` 고정 · 일반식 old_count 0 · 2241 ≤ old_start ≤ 2252 | `D-20260905-02-pdm2b-seats.md` §6 |
| 2026-09-05-astra-m1b-m2b1v2.md | MQ-3 | HIGH | 수용 | GeneratorExp 지연 평가가 경계 목록에 없어 블록 안 생성기 + 블록 밖 next() 가 ⒜⒝⒞ 통과(발주자) — v3: GeneratorExp 전체를 경계(과잉 엄격) · 음성 칸 (h) · 신설 10 · 853 | `D-20260905-02-pdm2b-seats.md` §6 |
| 2026-09-05-astra-m1b-m2b2.md | MR-1 | BLOCKER | 수용 | LaneRequest.__post_init__ 필드 정합 검사가 m16 지문 민감도 시험(한 필드만 변조)과 충돌 · 기존 시험 무수정 조건과 양립 불가(발주자) — v2: 정합 검사를 __post_init__ 에서 제거(어휘 fullmatch + 루트 포함만 · T4 문언 그대로) · 정합은 조립 자리 단일(plan.py) 구조 보장 · 안 보는 축에 명기 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-2 | HIGH | 수용 | partial.promotion_to_publish 「불가 — 새 런」 은 T40 이 정하지 않은 승격 정책(입법 · 규율 11)(발주자) — v2: 키 제거 · 별도 상신 후보로 기록 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-3 | HIGH | 수용 | 시험 (g) 임시 법 리포 편집 뒤 미커밋 → _engine_pin StageHaltError 로 넓은 raises 통과 · partial_until 미지정으로도 통과(발주자) — v2: commit_law 로 커밋 · partial_until='read' 전달 · 문언 「run_kind 어휘 위반」 단언 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-4 | HIGH | 수용 | containment(realpath) 검사만 제거한 변조를 가르는 시험 없음(발주자) — v2: 중간 디렉터리 symlink → 루트 밖 음성(「루트 밖」 사유) + 루트 자체 symlink 양성 · 로그 finding 사유는 어휘 위반/루트 밖 구분 보존 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-5 | MED | 수용 | re `$` 가 끝 개행 앞 일치 · 「공백 불가」가 정규식만으로 확정 안 됨(발주자) — v2: fullmatch 명시 · 끝 개행·탭·공백 음성 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-6 | MED | 수용 | check_lane_log_digest_value 는 메모리 저널 입력이라 파일 변조가 검사에 닿지 않음 · 구 코드도 digest-file-missing 으로 fail(발주자) — v2: _load_recorded_lane_log 재독 · 사유 토큰 단언이 차별 대조 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2.md | MR-7 | MED | 수용 | SPEC :26 을 §6.7 현황표로 오기(실제 서두 계약 목록 · §6.7 현황표 :4114 는 무변경) · §8.2 제목·도입 「두 종류」 문언 반경 밖(발주자) — v2: 좌표 정정 · :4487 :4489 편집 허용 | `D-20260905-02-pdm2b-seats.md` §7 |
| 2026-09-05-astra-m1b-m2b2v2.md | MS-1 | HIGH | 수용 | 가드 위치 문언 상충(①「⓪ 직후」· ②「_engine_pin 앞」· ④(g)「_engine_pin 통과 뒤」)(발주자) — v3: `_engine_pin` 직후 · 승계 확인·입력 읽기 전으로 통일 | `D-20260905-02-pdm2b-seats.md` §8 |
| 2026-09-05-astra-m1b-m2b2v2.md | MS-2 | HIGH | 수용 | 「수리 전 음성 전건 붉음」에 구 서명이 partial_until 을 안 받아 TypeError 로 붉는 칸(c)(f)(g)·구 계약에 partial 이 없어 준비 실패하는 (g) 포함 — 구멍 실증 아님(발주자) — v3: 대조를 (ii)-A 기존 API 칸 / (ii)-B 가드 부재 기준판 칸으로 분리 · TypeError·준비 실패는 세지 않음 | `D-20260905-02-pdm2b-seats.md` §8 |
| 2026-09-05-astra-m1b-m2b2v2.md | MS-3 | MED | 수용 | 「산출 0」의 배치 조건(입력·법 리포 = run_root 밖) 미명시 · (c) 산출 0 단언 없음(발주자) — v3: 배치 조건 + (a)~(c) 각각 run_root 부재/빈 단언 | `D-20260905-02-pdm2b-seats.md` §8 |
| 2026-09-05-astra-m1b-m2b2v2.md | MS-4 | MED | 수용 | 로그 위조 「구 코드도 fail」이 Replay 어댑터(지문 null · 면제) 경로에서 불성립(발주자) — v3: FileLaneAdapter 실왕복의 비null 지문 행 · 변조 전 pass / 구판 digest-file-missing + 토큰 부재 / 수리 후 토큰 | `D-20260905-02-pdm2b-seats.md` §8 |
| 2026-09-05-astra-m1b-m2b2v2.md | MS-5 | LOW | 수용 | containment 제거 시 「symlink 칸만 붉음」 거짓 — 로그 symlink 음성도 붉음(발주자) — v3: 둘 붉음 · 어휘 음성·루트 symlink 양성 초록으로 문언 정정 · §0 :7 의 「:26 = §6.7」 잔재 정정 | `D-20260905-02-pdm2b-seats.md` §8 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | A-01 | HIGH | 수용 | 정적 관문의 실행 경계 블랙리스트가 `TypeAlias.value`·`AnnAssign.annotation` 지연 평가를 통과시킨다(자문 축약 재현)(발주자) — v4: 「즉시 평가 (부모 노드, 필드) 닫힌 허용 목록」으로 규칙 전환 · 목록 밖은 전부 offender · 음성 (i)(j)(l) · 양성 (k) `AnnAssign.value` | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | A-02 | HIGH | 수용 | 헬퍼가 검증한 트리와 실제 엔진 호출의 원장 대상 사이에 결속 없음 · 빈 `*trees` 허용(발주자) — v4: 트리 ≥1 · 블록 동안 `read_stage.shadow_screening_ledger` 를 감싸 해석 결과를 검증(tmp 안 · 생산과 samefile 아님 · `shadow_root=None` 은 기대 원장 집합 소속) · 위반은 쓰기 전 `pytest.fail` · 음성 (ⅲ)(ⅶ) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | A-03 | HIGH | 수용 | `<tmp>/main/ledgers` symlink → 생산이면 진입 ①②③ 통과 뒤 ④ 가 쓴 뒤에 잡는다(발주자) — v4: 진입 ③′ 기대 원장 realpath 가 tmp 안 + 존재 시 `samefile` 부정 · 쓰기 전 차단은 A-02 감싸기 자리 · `finally` 지문의 보증 문언을 「전후 바이트 변경 탐지」로 한정 · 음성 (ⅵ) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | A-04 | HIGH | 수용 | 정적 관문이 한 시험 함수 안 통주 뒤에 돌아 다른 시험의 선행 기입을 봉쇄하지 않는다(발주자) — v4: 시험 전용 두 층 = `tests/conftest.py` `pytest_sessionstart` 정적 관문(UsageError · 수집 전) + 세션 autouse `read_stage.append_screening_ledger` 감싸기(생산 원장 해석 시 `pytest.fail` · 기입 전) · 함수는 `tests/ledger_guard.py` 로 · 엔진 pytest 인식 분기·허가 객체는 **이연**(시험 전용 대안 부족 확인 시 Owner 재정) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | A-05 | MED | 수용 | 헬퍼 음성 2칸으로 4중 보호 각 분기 독립 검증 불가(발주자) — v4: 음성 9칸(외부 트리 · 빈 트리 · 외부 주 트리에 연결된 tmp worktree · tmp 안 생산 자리 · 원장 symlink · 결속 위반 · 지문 동일+본문 예외 보존 · 지문 변경+`__context__` · 변경 탐지) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | B-01 | HIGH | 수용 | 정규식 형태 검사만으로 T4 「계약 어휘 검증」 전부 집행 주장 불가 — `other/unknown/batch-0` 통과(발주자) — v4: `read_run`·`task` **소속 검사** 추가(`READ_RUNS`·`LANE_TASKS` 상수 = `contract.py` · 정본 = 스키마 `$defs.read_run` enum · `read.yaml#lane.sub_lanes[].id` · 다리 시험 2) · 필드 정합은 여전히 조립 자리 보장(MR-1) · B-2 마커 문언 = 형태+소속+루트 포함 | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | B-02 | HIGH | 수용 | `lane_dir` 디렉터리 포함 검사는 말단 `request.md` symlink 를 보호하지 않는다(발주자) — v4: `lane_file(root, lane_id, name)` 신설(최종 경로 realpath 포함) · 호출 5자리(`read.py` 로그 검사 · file_adapter 3 · replay_adapter 1) · 말단 symlink 음성 · 로그 대조 = 루트 밖 파일(mode 000 · 지문 일치) → 「루트 밖」 finding · `PermissionError` 없음(열지 않았다) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-advice-m2b-gate-and-values.md | C-01 | MED | 수용 | 반복 결함(좌표 오기 · 문언 상충 · 잘못된 이유의 붉음 · 허가 초과)의 뿌리 = 권한·좌표·순서·대조를 잇는 단일 기준 부재(발주자) — v4: 두 발주문 §0′ **변경별 증명표**(재정 원문 · 기준 blob · 앵커 · 허용 입력 전후 · 최소 반례 · 기준판 · 기대 실패 사유 · 실출력 칸) · 골격 ⒃ 후보로 등재(Owner 재정 뒤 ROUTING 성문화) | `D-20260905-02-pdm2b-seats.md` §9 |
| 2026-09-06-astra-m1b-m2b1v3.md | MT-1 | HIGH | 수용 | autouse 세션 픽스처는 수집 뒤 설치돼 모듈 import 시 기입(explicit shadow_root · 비None 통과)을 못 막는다 — 자문 A-04 잔존(발주자) — v5: append 감싸기를 `pytest_sessionstart` 설치·`pytest_sessionfinish` 복원 · 모듈 최상위 프로브(가짜 생산 자리) 대조 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b1v3.md | MT-2 | MED | 수용 | (a)·프로브는 `def _probe()` 안이라 규칙상 `FunctionDef.body` 즉시 offender — 기대 사유 「블록 밖」 불일치(발주자) — v5: 사유 `허용 목록 밖 (FunctionDef.body)` · 「블록 밖」은 Module 도달 시만 · 모듈 최상위 None 칸 신설 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b1v3.md | MT-3 | MED | 수용 | R1 허용 목록 제거로 (g) 는 반전 안 됨(헬퍼 인자 위치 분기 별도) · R4 우선순위 뒤집기 = ValueError 전파 → 시험 실패이지 「초록」 아님(발주자) — v5: R1 반전 = (f)(h)(i)(j)(l) · (ii)-M 표에 「관문/헬퍼 관측」과 「고정 시험 판정」 열 분리 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b1v3.md | MT-4 | MED | 수용 | 훅 제거 + 시험 0 프로브 단독 = exit 5(NO_TESTS_COLLECTED) · ⑸ 삭제 뒤 ⑺ R5 에 프로브 재설치 없음 · P′ 초록 명령 미지정(발주자) — v5: R5 = 프로브 재설치 → 훅 있음 exit 4 / 없음 exit 5 → 재삭제 · P′ = m2 선택 실행 exit 0 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b1v3.md | MT-5 | MED | 수용 | 자문 A-05 「보호 하나씩 제거」에 ②·③ 제거 대조 누락(발주자) — v5: R2a ② 제거 → (ⅳ) 토큰 `주 트리`→`원장 실경로` · R2b ③ 제거 → (ⅴ) 진입 허용 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v3.md | MU-1 | HIGH | 수용 | 로그 ⑷ 「PermissionError 부재 = 열지 않음」 불성립 — 구 코드 `except OSError` 가 `digest-file-unreadable` finding 으로 흡수(발주자 · 자문 B-02 잔존) — v5: chmod 제거 · `_bare_sha256_file` 호출 계수(완성본 0 · 구 코드/V7 제거 1 + pass) | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v3.md | MU-2 | HIGH | 수용 | V6 만 제거해도 로그 ⑶ 은 V7 이 「루트 밖(말단)」 으로 계속 fail — 「둘 초록」 거짓(발주자) — v5: V6 제거 검출 = 직접 lane_dir 반환 + 로그 ⑶ 토큰 디렉터리→말단 변화 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v3.md | MU-3 | MED | 수용 | 대조표가 엔진 입력 허용과 고정 시험 PASS/FAIL 을 같은 색으로 혼용 · V2 다섯 칸 ↔ (ii)-B 세 칸 불일치 · 정합 미검사 양성은 양판 PASS(발주자 · C-01 잔존) — v5: 두 열 분리 · V2 실출력 칸 = (a)(b)→(ii)-A · (c)(f)(g)→(ii)-B | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v3.md | MU-4 | LOW | 수용 | 6곳 목록은 맞으나 지정 grep 이 비재귀·read.py:1536 미포착·비아티팩트 혼입(발주자) — v5: `grep -rn` 세 상수 + `lane_dir(` · 결과 분류표(import·정의·문언·디렉터리 준비·조립 6) | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v3.md | MU-5 | LOW | 수용 | m16 은 lane_id·read_run·task 를 각각 하나씩 변조 — 「read-b/decompose + synthesize 짝」은 기존 시험 아님(발주자 사실 오기) — v5: 문언 정정 · 그 짝은 m27 양성 예시로 | `D-20260905-02-pdm2b-seats.md` §10 |
| 2026-09-06-astra-m1b-m2b2v4.md | MW-1 | LOW | 수용 | grep 총계 「21행」 오기 — 실측 23(조립 6 좌표는 맞음)(발주자) — v6: 23 = import 5 · 정의 7 · 문언 4 · 준비 1 · 조립 6 | `D-20260905-02-pdm2b-seats.md` §11 |
| 2026-09-06-astra-m1b-m2b2v4.md | MW-2 | LOW | 수용 | §0′ V5 기준판 칸이 색으로 적혀 「입력 허용」으로만 읽힘 — MU-3 잔존(발주자) — v6: 관측(요청 생성/예외 유지) · 고정 시험(FAIL/PASS) 문언으로 | `D-20260905-02-pdm2b-seats.md` §11 |
| 2026-09-06-astra-m1b-m2b2v4.md | MW-3 | LOW | 수용 | (ii)-A 제외 목록의 이관 목적지 오기 — 다리 시험을 (ii)-B/(ii)-M 으로 지목(발주자) — v6: (c)(f)(g)→(ii)-B · 말단 직접→(ii)-M V7 · 다리→(ii)-D | `D-20260905-02-pdm2b-seats.md` §11 |

**행 수 = 260**(`등재` 57파일의 지적 전건). **[정정 2026-09-06 · 42차]** 직전 판 **257** — M1b 4차(M2b-2 v5) 원문 반입(MW 3 · LOW) · 전부 수용.

**행 수 = 257**(`등재` 56파일의 지적 전건). **[정정 2026-09-06 · 41차]** 직전 판 **247** — M1b astra high 3차 도전 두 원문 반입(M2b-1 MT 5 · M2b-2 MU 5) · 전부 수용.

**행 수 = 247**(`등재` 54파일의 지적 전건). **[정정 2026-09-06 · 40차]** 직전 판 **239** — 자문 회신(m2b-gate-and-values · 두 라운드 합본) 원문 반입(A 5 · B 2 · C 1) · 전부 수용 · 엔진 동적 강제는 이연.

**행 수 = 239**(`등재` 53파일의 지적 전건). **[정정 2026-09-05 · 39차]** 직전 판 **234** — M1b astra high 2차 도전(라운드 M2b-2 v2) 원문 반입(MS 5) · 전부 수용 · 자문 트리거 ⓑ.

**행 수 = 234**(`등재` 52파일의 지적 전건). **[정정 2026-09-05 · 38차]** 직전 판 **227** — M1b astra high 도전(라운드 M2b-2 발주문 v1) 원문 반입(MR 7) · 전부 수용.

**행 수 = 227**(`등재` 51파일의 지적 전건). **[정정 2026-09-05 · 37차]** 직전 판 **224** — M1b astra high 2차 도전(라운드 M2b-1 v2) 원문 반입(MQ 3) · 전부 수용 · 자문 트리거 ⓑ.

**행 수 = 224**(`등재` 50파일의 지적 전건). **[정정 2026-09-05 · 36차]** 직전 판 **216** — M1b astra high 도전(라운드 M2b-1 발주문 v1) 원문 반입(MP 8) · 전부 수용.

**행 수 = 216**(`등재` 49파일의 지적 전건). **[정정 2026-09-05 · 35차]** 직전 판 **216**(행 수 불변) — 좁은 재감사 7(fable xhigh 3회째 · PASS · 신규 0) 원문 반입(등재 행만).

**행 수 = 216**(`등재` 48파일의 지적 전건). **[정정 2026-09-05 · 34차]** 직전 판 **215** — M1b astra high 도전(재감사 7 발주문) 원문 반입(MO 1) · 수용.

**행 수 = 215**(`등재` 47파일의 지적 전건). **[정정 2026-09-05 · 33차]** 직전 판 **215**(행 수 불변) — M1b astra high 2차 도전(M2a-3 v2) PASS 원문 반입(지적 0 · 등재 행만).

**행 수 = 215**(`등재` 46파일의 지적 전건). **[정정 2026-09-05 · 32차]** 직전 판 **209** — M1b astra high 도전(M2a-3 발주문 v1) 원문 반입(MM 6) · 전부 수용.

**행 수 = 209**(`등재` 45파일의 지적 전건). **[정정 2026-09-05 · 31차]** 직전 판 **204** — 재감사 6(fable xhigh 2회째 · FAIL · MED 1 LOW 4) 원문 반입(RJ 5) · 전부 수용.

**행 수 = 204**(`등재` 44파일의 지적 전건). **[정정 2026-09-05 · 30차]** 직전 판 **200** — M1b astra high 도전(재감사 6 발주문) 원문 반입(ML 4) · 전부 수용.

**행 수 = 200**(`등재` 43파일의 지적 전건). **[정정 2026-09-05 · 29차]** 직전 판 **195** — M1b astra high 2차 도전(M2a-2 발주문 v2) 원문 반입(MK 5) · 전부 수용.

**행 수 = 195**(`등재` 42파일의 지적 전건). **[정정 2026-09-05 · 28차]** 직전 판 **189** — M1b astra high 도전(M2a-2 발주문 v1) 원문 반입(MJ 6) · 전부 수용.

**행 수 = 189**(`등재` 41파일의 지적 전건). **[정정 2026-09-05 · 27차]** 직전 판 **186** — 재감사 5(fable xhigh 첫 적용 · PASS · LOW 3) 원문 반입(RI 3) · 전부 수용 · **RI-2 정정: MG-1 격 셀 `HIGH` → `BLOCKER`**(원문 `FINAL:35`·§28 과 일치시킴 · 도입 `cd63ace` 의 전사 오기).

**행 수 = 186**(`등재` 40파일의 지적 전건). **[정정 2026-09-05 · 26차]** 직전 판 **184** — M1b astra high 도전(재감사 5 발주문) 원문 반입(MI 2) · 전부 수용.

**행 수 = 184**(`등재` 39파일의 지적 전건). **[정정 2026-09-05 · 25차]** 직전 판 **179** — M1b astra high 2차 도전(M2a-1 v2) 원문 반입(MH 5) · 전부 수용.

**행 수 = 179**(`등재` 38파일의 지적 전건). **[정정 2026-09-05 · 24차]** 직전 판 **173** — M1b astra high 도전(라운드 M2a-1 발주문) 원문 반입(MG 6) · 전부 수용.

**행 수 = 173**(`등재` 36파일의 지적 전건). **[정정 2026-09-05 · 23차]** 직전 판 **169** — M1b astra high 도전(재감사 4 발주문) 원문 반입(MF 4) · 전부 수용.

**행 수 = 169**(`등재` 35파일의 지적 전건). **[정정 2026-09-05 · 22차]** 직전 판 **168** — M1b astra high 도전(라운드 RG 발주문) 원문 반입(ME 1) · 수용.

**행 수 = 168**(`등재` 34파일의 지적 전건). **[정정 2026-09-05 · 21차]** 직전 판 **165** — 좁은 재감사 3 원문 반입(RG 3) · 전부 수용.

**행 수 = 165**(`등재` 33파일의 지적 전건). **[정정 2026-09-05 · 20차]** 직전 판 **159** — M1b astra 3차 도전 원문 반입(MD 6) · 전부 수용.

**행 수 = 159**(`등재` 32파일의 지적 전건). **[정정 2026-09-05 · 19차]** 직전 판 **153** — M1b astra 2차 도전 원문 반입(MC 6) · 전부 수용.

**행 수 = 153**(`등재` 31파일의 지적 전건). **[정정 2026-09-05 · 18차]** 직전 판 **146** — M1b astra 설계 도전 원문 반입(MB 7) · 전부 수용.

**행 수 = 146**(`등재` 30파일의 지적 전건). **[정정 2026-09-05 · 17차]** 직전 판 **138** — 라운드 RE 좁은 재감사 2 원문 반입(RF 8) · 전부 수용.

**행 수 = 138**(`등재` 29파일의 지적 전건). **[정정 2026-09-05 · 15차]** 직전 판 **131** — 라운드 RD 좁은 재감사 원문 반입(RE 6) · 전부 수용.

**행 수 = 131**(`등재` 28파일의 지적 전건). **[정정 2026-09-03 · 합본 감사]** 직전 판 **125** — B″+T31+T32 합본 감사 원문 반입(RD 6)으로 여섯 늘었다.

**행 수 = 125**(`등재` 27파일의 지적 전건). **[정정 2026-09-03 · B′ 재감사]** 직전 판 **118** — 좁은 재감사 원문 반입(RC 7)으로 일곱 늘었다.

**행 수 = 118**(`등재` 26파일의 지적 전건). **[정정 2026-09-03 · 라운드 B 감사]** 직전 판 **112** — opus max 합본 감사 원문 반입(RB 6)으로 여섯 늘었다.

**행 수 = 112**(`등재` 25파일의 지적 전건). **[정정 2026-09-03 · 16·17차]** 직전 판 **111** — 16차 도전 원문 반입(AJ 1)으로 하나 늘었고, 17차(PASS · 지적 0 · `-v18.md`)는 `등재` 파일은 늘리되 행을 더하지 않는다.

**행 수 = 111**(`등재` 23파일의 지적 전건). **[정정 2026-09-03 · 15·16차]** 직전 판 **104** — 14차(AH 4)·15차(AI 3) 도전 원문 반입으로 일곱 늘었다.

**행 수 = 104**(`등재` 21파일의 지적 전건). **[정정 2026-09-03 · 14차]** 직전 판 **102** — 13차 도전 원문 반입(AG 2)으로 둘 늘었다.

**행 수 = 102**(`등재` 20파일의 지적 전건). **[정정 2026-09-02 · 13차]** 직전 판 **99** — 12차 도전 원문 반입(AF 3)으로 셋 늘었다.

**행 수 = 99**(`등재` 19파일의 지적 전건). **[정정 2026-09-02 · 12차]** 직전 판 **96** — 11차 도전 원문 반입(AE 3)으로 셋 늘었다.

**행 수 = 96**(`등재` 18파일의 지적 전건). **[정정 2026-09-02 · 11차]** 직전 판 **93** — 10차 도전 원문 반입(AD 3)으로 셋 늘었다.

**행 수 = 93**(`등재` 17파일의 지적 전건). **[정정 2026-09-02 · 10차]** 직전 판 **88** — 9차 도전 원문 반입(AC 5)으로 다섯 늘었다.

**행 수 = 88**(`등재` 16파일의 지적 전건). **[정정 2026-09-02 · 9차]** 직전 판 **86** — 8차 도전 원문 반입(AB 2)으로 둘 늘었다.

**행 수 = 86**(`등재` 15파일의 지적 전건). **[정정 2026-09-02 · 8차]** 직전 판 **82** — 7차 도전 원문 반입(AA 4)으로 넷 늘었다.

**행 수 = 82**(`등재` 14파일의 지적 전건). **[정정 2026-09-02 · 7차]** 직전 판 **80** — 6차 도전 원문 반입(Z 2)으로 둘 늘었다.

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
