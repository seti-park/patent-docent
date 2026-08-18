# sol 독립 감수 원문(회수분) — M1.7 분할 감수 C′-1 · 1차 사망 세션 (2026-08-19 00:0x)

**STATUS: partial(events) — 원세션이 최종 VERDICT(4,967자)를 발화한 뒤 사망, resume 불필요**

**보존 근거.** 재정 2026-08-18 **N7 ①** — 외부 감수 산출물은 **원문 그대로** `docs/lessons/` 에 보존한다. 이 파일은 **하네스 결함으로 사망한 1차 감수 세션에서 사후 회수한 원문**이다.

| 항목 | 값 |
|---|---|
| 의뢰 | C′-1 (격리 사본 `pd-audit-m17/C1`) |
| 감수자 | GPT-5.6-sol, reasoning effort max |
| 원세션 ID | `01a0156a-eed1-7880-a160-7ab3fd9650f2` |
| rollout | `~/.codex/sessions/2026/08/19/` |
| 실행시간 | 약 8분 41초 (521s) |
| 샌드박스 | `read-only` |
| **사망 사유** | `timeout` CAP **600초** 직격 (구 `sol-auditor.md` 기본값). `--output-last-message` 는 턴 정상 완료 시에만 기록되므로 `$FINAL` 은 **0바이트**였다. |
| 회수 경로 | **rollout 이벤트 발굴** — 원세션 rollout 에서 최종 VERDICT(4,967자)를 그대로 추출(사망 직전 발화 완료). resume 미사용. |
| 판정 발행 주체 | **원세션 Sol 자신** — 아래 본문은 원세션 발화 그대로다(resume 재추론 아님) |

**★ 격의 명시.** 이 판정은 **완주 판정이 아니다.** 조사가 중단된 상태에서 확보된 것이므로 미확인 항목이 남아 있을 수 있다. 완주분(동일 의뢰 재실행, CAP 2400)은 `2026-08-19-sol-audit-m17-full.md` 를 참조하라 — 두 판정이 어긋나면 **완주분이 우선**한다.

---

## Sol 발화 원문 (시간순, 구분선으로 분리)

먼저 지정된 핀만 확인하겠습니다. 일치할 때에만 문서·JSON을 읽어 독립 재계수를 진행하고, 테스트나 검사기는 실행하지 않겠습니다.

---

핀은 요청값과 정확히 일치합니다. 이제 `quoted` 13건의 원자료와 §12 배제 라벨 구조를 기계적으로 뽑은 뒤, 각 locator의 원문 문단을 직접 대조하겠습니다.

---

초기 판독상 `quoted`는 13건이며, M87–M89만 좌표·표 번호 조각으로 보입니다. 다만 결론을 고정하기 전에, 7개 배제 사유 각각의 표본을 원문에서 확인하고 특히 `boundary-right`의 `5b/4b/3b/2b`가 실제 공학량인지 별도로 판정하겠습니다.

---

배제 표는 독립 파싱 결과 실제로 89구간이며 라벨별 소계도 렌더와 일치합니다. 경계 표본에서는 `boundary-left`가 형식·신호 식별자만 버린 반면, `boundary-right`는 예상대로 진짜 exponent bit-width인 `5b/4b/3b/2b`를 버렸습니다. 이 네 건은 요청대로 행위시법상 결함 수에는 넣지 않되, 처분 자체는 의미론적으로 부당하다고 구분해 적겠습니다.

---

VERDICT (P-B): 부분 해소  
핀 대조: HEAD=`fca126bc278f5ae4ba5a08f26b3297cb9f12b682` (일치)

전수 수확·CP1 노출·역참조 격리는 작동하지만, 정답지에 활성 `fact` 아티팩트 3건이 남아 있다. 역참조가 피해를 막았다는 것은 정답지 자체를 정화하지 않으므로 `해소`가 아니라 `부분 해소`로 판정한다.

검사기·테스트 스위트는 실행하지 않았고 파일 읽기와 기계 계수만 수행했다.

## quoted 총수: 13

`value_span`은 `source.quote` 안의 반개구간 `[start,end)`이다. 13건 모두 `unit: null`이다.

| 항목 ID | value_raw | unit | locator | value_span | 판정 | 원문 문맥(인용) |
|---|---:|---|---|---:|---|---|
| M87 | `2` | `null` | `[0186]` | `117:118` | `ARTIFACT` | “beyond those listed in **Tables 1 and 2**.” — 두 번째 표 번호 |
| M88 | `0` | `null` | `[0140]` | `36:37` | `ARTIFACT` | “e.g., in **Row 0** and Col 0 of the CIM macro” — 행 좌표 |
| M89 | `0` | `null` | `[0140]` | `46:47` | `ARTIFACT` | “e.g., in Row 0 and **Col 0** of the CIM macro” — 열 좌표 |
| M90 | `2, 3, 4, or 5` | `null` | `[0068]` | `108:121` | `GENUINE` | “activation values with different counts of exponent bits, such as **2, 3, 4, or 5**” |
| M91 | `60` | `null` | `[0189]` | `180:182` | `GENUINE` | “the common cell **220** can include **60 columns** and 60 rows” |
| M92 | `60` | `null` | `[0189]` | `195:197` | `GENUINE` | “can include 60 columns and **60 rows**” |
| M93 | `60` | `null` | `[0189]` | `217:219` | `GENUINE` | “where number **60** is the least common multiple…” |
| M94 | `5, 4, 3, and 2` | `null` | `[0189]` | `259:273` | `GENUINE` | “least common multiple of number **5, 4, 3, and 2**.” — 지원 exponent 폭에 따른 셀 크기 산정 인수 |
| M95 | `2, 3, 4, or 5` | `null` | `[0068]` | `98:111` | `GENUINE` | “weight values with multiple possible exponent widths, including **2, 3, 4, or 5 bits**.” |
| M96 | `12` | `null` | `[0189]` | `33:35` | `GENUINE` | “the common cell **220** includes **12 columns** and 12 rows” |
| M97 | `12` | `null` | `[0189]` | `48:50` | `GENUINE` | “includes 12 columns and **12 rows**” |
| M98 | `12` | `null` | `[0189]` | `70:72` | `GENUINE` | “where number **12** is the least common multiple…” |
| M99 | `4, 3, and 2` | `null` | `[0189]` | `112:123` | `GENUINE` | “least common multiple of number **4, 3, and 2**.” — exponent 폭에 따른 산정 인수 |

소계: `GENUINE 10` / `ARTIFACT 3` / `UNDECIDABLE 0`.

## 총괄 주장 대조

- 아티팩트 총수 주장 `3` vs 실측 `3` — 일치. `3/13 = 23.08%`이므로 표시한 23%도 맞다.
- 항목 식별도 정확하다.
  - M87 `[0186]` = `Tables 1 and 2`의 뒤 표 번호 `2`
  - M88 `[0140]` = `Row 0`
  - M89 `[0140]` = `Col 0`
- 총괄이 놓친 아티팩트: 없음.
- 총괄이 과잉 계상한 아티팩트: 없음.
- 통주 2도 별도 재계수했다. `quoted 30` 중 통주2 M87–M109가 아티팩트 23건, M110–M116이 진짜 7건이었다. 앵커는 `[0186]`의 `FP8 (1-5-2)` 파편, `[0165]`의 `Act 0 <6:3>`·`Wdata 0 <4:2>` 파편, `[0183]`의 `Table 2`, `[0188]`의 `C.sub.j−1`·`FIG. 1` 등이다. 따라서 `23/30 = 76.67%`, 즉 77% 주장도 일치한다.
- 다만 총괄 문서의 포괄적 표현인 “배제가 진짜를 먹지 않았다”는 사실 그대로는 아니다. `[0189]`의 `5b, 4b, 3b, 2b` 네 exponent bit-width가 `boundary-right`로 기각됐다. 요청의 행위시법 지시에 따라 이번 런의 결함으로는 계상하지 않았다.

## 배제 표본 검사

89구간을 독립 파싱한 소계도 렌더와 일치한다: `34 + 30 + 9 + 7 + 4 + 3 + 2 = 89`.

| 사유 라벨 | 표본 | 정당한가 | 근거 |
|---|---|---|---|
| `figure-numeral` | `[0128]` `101` — “CIM macro **101** configured…”<br>`[0188]` `2860` — “A first multiplexer **2860** selects…”<br>`[0189]` `220` — “the common cell **220** includes 12 columns…” | 예 | 모두 구성요소·도면부호다. 열·행 수 `12`, `60`은 별도로 살아남았다. |
| `boundary-left` | `[0186]` `8` — “**FP8** format”<br>`[0149]` `1` — “Step **S1**”<br>`[0217]` `0` — “bitcells **BC0** and BC1” | 예 | 각각 형식명·단계 식별자·비트셀 식별자의 내부 숫자다. 표본 및 같은 계열에서 진짜 공학량 누락은 찾지 못했다. |
| `coordinate-triple` | `[0186]` `(1-5-2)` — “FP8 **(1-5-2)**”<br>`[0186]` `(1-2-3)` — “FP6 **(1-2-3)**”<br>`[0183]` `(1-4-3)` — “FP8 **(1-4-3) format**” | 예 | FP 형식의 3항 표기 전체다. 개별 독립 수치 사실로 읽지 않는 것이 맞다. |
| `figure-or-table-number` | `[0186]` `Tables 1` — “**Tables 1 and 2**”<br>`[0188]` `FIG. 28` — “**FIG. 28** illustrates…”<br>`[0183]` `FIG. 60` — “Table 2 (in **FIG. 60**)” | 표본 배제는 예, 포괄성은 불완전 | 모두 표·도면 식별자다. 다만 첫 표본에서 뒤 항 `and 2`를 못 잡아 M87이 생겼다. |
| `boundary-right` | `[0189]` `5` — “exponents with **5b**”<br>`[0189]` `4` — “**4b**”<br>`[0189]` `2` — “**2b**” | 아니오 — 진짜 공학량 | exponent bit-width다. 같은 문장의 `3b`도 동일하다. Q4의 비소급 조건 때문에 이번 결함에는 넣지 않았지만, 의미론적으로는 부당한 배제다. |
| `bit-slice` | `[0165]` `0 <6:3>` — “Act **0 <6:3>**”<br>`[0165]` `0 <4:2>` — “Wdata **0 <4:2>**”<br>`[0165]` `<4:2>` — “W0 **<4:2>**” | 예 | 피연산자 번호와 비트 위치 범위로 구성된 신호·슬라이스 식별자다. 독립 물리량이 아니다. |
| `subscript-index` | `[0188]` `.sub.j−1` — “carry-out bit **C.sub.j−1**”<br>`[0188]` `.sub.j−1` — “carry-in bit **CIN.sub.j−1**” | 예 | 이전 단계 신호를 가리키는 아래첨자 인덱스다. |

## 역참조 오염 여부: 없음

활성 `implication`·`positioning` 12항목에서:

- `numeric_refs`가 비어 있지 않은 항목: 6
- 참조 edge: 16
- 서로 다른 대상: 12
- 대상 집합: `{M90, M93, M94, M95, M98, M99, M104, M105, M106, M107, M108, M109}`
- `ARTIFACT` 집합 `{M87, M88, M89}`과의 교집합: `∅`

참조 관계도 JSON과 일치한다: `M111→M107`, `M112→M90/M95`, `M113→M98/M99/M93/M94/M104/M105/M106/M108`, `M117→M109`, `M118→M90/M95/M107`, `M121→M109`.

따라서 잔여 노이즈는 서사에 닿지 않았다. 다만 이는 피해 격리의 성공이지, M87–M89가 활성 `fact`인 상태 자체의 해소는 아니다.

## OUT-OF-SCOPE

- Q4 적용 후 다음 런에서 `5b/4b/3b/2b`가 실제로 `unit: b`와 함께 수확되는지는 재생성 산출물이 없어 검증하지 않았다.

NEW BLOCKER: 없음