# sol 독립 감수 원문 — M1.5 (범위 고정 재감수, 2026-08-18 후반)

**보존 근거.** 재정 2026-08-18 **N7 ①** — 모든 외부 감수·검증 산출물은 수령 즉시 **원문 그대로** `docs/lessons/`에 보존하고, 처분표·요약은 그 원문을 가리키는 포인터로만 존재한다.

| 항목 | 값 |
|---|---|
| 감수자 | GPT-5.6-sol, reasoning effort max, read-only, 교차벤더 독립 |
| 구동 | `sol-auditor` 레인(Opus 래퍼가 codex CLI 구동) |
| 대상 | HEAD `245657d` (감수 착수 시 `c3b723d`, 진행 중 1커밋 이동 — 총괄이 통지) |
| **판정** | **FAIL** (범위 안 기준) |
| 적용 규율 | 재정 **P-11**(범위 고정) — **이번 재감수부터 적용** |
| 실행 비고 | 1차 호출 600s 무출력 타임아웃(0바이트 산출), 2700s 예산으로 재호출해 ~35분에 완주 |

**★ 이 파일의 지위에 관한 정직한 표기.** 아래는 `sol-auditor` 레인이 총괄에게 **전달한 형태 그대로**이며, 레인이 Sol의 판정을 구조화해 옮긴 것이다. 직전 라운드(`2026-08-18-sol-audit-m1-full.md`)는 Sol의 최종 메시지 전문을 그대로 실었으나 이번 회차는 레인의 전달본이 총괄이 수령한 최대 원문이다. **그 차이를 숨기지 않는다** — 재정 N7이 보존하라 한 것은 "총괄이 받은 것"이고, 그것이 요약 한 겹을 거쳤다면 그 사실 자체가 기록의 일부다.

---

## Verdict: FAIL (in-scope basis)

### 범위 안 — 부분(partial) 판정 8행, Sol은 이 전부가 종결을 막는다고 본다

| item | 판정 | Sol's evidence |
|---|---|---|
| N14-13 / P-1 | 부분 | Escape-guard unit tests pass both directions (`tests/test_m1_reader.py:1700`, `:1723`), but the ruling's "만나면 표지" did not execute on the real run: CL-10/11/19 are `comprises/is at least one of …` yet all typed `single`; `unclassified_dependents=[]`, dependency checked=17. The rule file itself concedes non-arrival: `reader/reader-rules.yaml:322` |
| P-2 ⓐ | 부분 | `reader/lib/bibliography.py:14` deliberately excludes dates from source collation and never checks per-priority jurisdiction. Sol mutated the real run: all priority dates → `1900-01-01` = pass/checked=16; all priority jurisdictions → `KR` = pass/checked=16. Inventor-mutation control correctly failed. |
| P-2 ⓑ | 부분 | K8 enforces only 7 hardcoded keys (`tools/check_spec_refs.py:132`). Sol planted `patent.marketing_verdict` — a plain project judgment — into the shared core with the `[공유 코어]` marker; exit 0 with findings=0 under both plain and `-O`. Enforces known names, not the boundary principle. |
| P-A / P-U4 | 부분 | `engine/stages/read.py:706` promises "한 행" but `:1149` appends in the `finally` of every runner call. Real ledger: 4 rows under one run_id, memo counts `1,2,2,2`; first row holds read-a only. |
| P-B | 부분 | Parity tests for planted/dropped numbers pass, but CP2 `numeric.unreviewed-use` is unimplemented (`D-20260818-04:31`, `SPEC.md:5431`). |
| P-U2 | 부분 | Overwrite refusal works (`test_m2_read.py:2614`), but `superseded-by-source-change` marking and old/new cross-links exist only in contract/comment (`contracts/stages/source.yaml:148`, `engine/stages/source.py:291`); production code does not record them. |
| P-6 | 부분 | Policy text correct in `contracts/parameters.yaml:56`, but no execution module or falsification for dead-instance retry / live-response preservation / recovery-failure escalation / correlated-sample exclusion. |
| P-9 | 부분 | Termination contract and first-class TONGJU exist (`contracts/run-kinds.yaml:14`), but the run ended at CP1 and never reached strip/CP2 (`TONGJU-REPORT.md:183`) — the "strip까지 완전 리허설" is unexecuted. |

### B-04 — 재발하지 않았다

Sol replayed READ from the pinned commit with the 5 committed responses in `/dev/shm`: exactly `decompose ×2 → ground ×2 → synthesize ×1`, 12 verdict rows and all deterministic artifacts matched; only `provenance.produced_at` differed. **No coordinator-computed value found outside the runner.**

Baselines reproduced: 247 passed; three gates exit 0 plain and `-O`; schema gate REJECT 23/23 + ACCEPT 12/12 + VALIDATOR_SCOPE 2/2; validator gate baseline 12/12 + mutants 39/39. `/tmp` failed at collection as an *environment* problem; `TMPDIR=/dev/shm` succeeded.

**All other in-scope rows** (N14-1..12, N14-14, P-3, P-4, P-C, P-U1/P-8, P-U3, P-U5, P-5, P-7, P-11, directives D/E, dispositions ⓐ–ⓓ) = **해소**.

### 총괄 정정 첨언에 대한 독립 재측정 — **정확함을 확인**

items 147 (component 43 / grounding 43 / fact 35 / implication 11 / positioning 3 / figure_note 12); fact 35 = quoted 30 + bib 4 + figure 1; quoted 30 = 7 genuine (`M110`–`M116`) + 23 artifacts (FP 3-term range 9 + bit-slice 8 + figure/table 6); `numeric_refs` = 5 items / 8 refs / 4 distinct targets; renumbering 4/4 exact.

**잔존 정직성 결함 2건**: `D-20260818-04:133`의 "여섯 중 넷"이 자기 표의 10행과 모순된다. 그리고 #8의 귀속 서술이 접지 레인의 범위 한정 측정과 총괄의 전역 재계수를 한 문장에 섞는다(`D:150`이 뒤에서 범위를 정정하기는 한다).

### M0.6 재대조: **16 해소 / 3 부분 / 5 미해소**

이번 라운드에 움직인 것 — M-07(부분→해소) · M-10(미해소→해소) · M-15(미해소→해소).
움직이지 않은 것 — B-02·M-02·M-06 부분; M-03·M-11·M-12·M-13·m-01 미해소.

### 범위 밖 지적 12건 — 그중 **하나가 BLOCKER급**

- **OOS-01 BLOCKER** — no request-freshness binding. Synthesis requests carry no payload/harvest-list digest, so after a request is refreshed a stale response's still-valid IDs can silently slide onto different facts with every check passing. The repo admits it at `TONGJU-REPORT.md:175`. **Undetectable semantic contamination path.** Owner escalation + next `engine/lanes` order.
- **OOS-02 MAJOR** — synthesis `response.json` overwritten in the worktree after completion: committed copy SHA-256 `472f…` (5 items / 8 refs, matches replay) vs. current worktree `b6ab…` (6 items / 16 refs, same request). Lane log carries no response digest/version, so the run cannot prove which was canonical.
- **OOS-03..OOS-05 MAJOR** — harvest answer-key noise (23/30 mis-parsed); `read.verbatim` does not separate claim vs. specification spans (self-grounding possible); lane `response_schema` too ID-centric to catch missing/mistyped `component` pre-assembly. **뒤 둘은 독립 검증 안 함(NOT VERIFIED)**.
- **OOS-06..OOS-09 MAJOR** — `effort` is a self-reported echo recorded as observation (`engine/stages/read.py:101`); colon handling in the boundary convention undecided; no convention for addition splitting vs. `attaches_to`; heterogeneous figure ID space (`FIG-28` vs `FIG-28-29`).
- **OOS-10..OOS-12 MINOR** — `if/when` over-detection; empirical basis for `addition-attachment` and the 0.95 interpretive axis still observational; model-identity vocabulary undecided.

### ANCHOR CHECK (레인이 HEAD `245657d`에서 좌표 실검)

인용된 좌표가 전부 실재 내용으로 해소된다 — `reader/reader-rules.yaml:322`는 실제로 Markush 미도달을 적고 있고, `tools/check_spec_refs.py`는 인용 행 근처에 `CORE_COMMENT_PREFIX = "[공유 코어]"`를 정의하며, `engine/stages/read.py:706`은 "한 행"이라 적는데 `:1149`는 `finally:` 안이고, `engine/stages/source.py:291`은 코드가 아니라 `#` 주석이어서 P-U2의 구현 공백을 확인해 주며, `TONGJU-REPORT.md:175`는 "★ 그리고 하나 더 — 요청서가 레인 작업 중 교체되었다" 표제다.

**P-B에 관한 문맥 주석 1건**: `D-20260818-04:31`은 CP2 `numeric.unreviewed-use`를 "미구현 — 소관 M4"로 적어 **스스로 M1 관할 밖임을 선언**한다. Sol은 그럼에도 부분으로 채점했다. 레인은 **Sol이 판정한 그대로 전달하고 판정을 조정하지 않았다.**

### Closing recommendation (Sol 문언)

in-scope items are NOT all resolved — **M1 must not close.** Separately, the new BLOCKER-class **OOS-01 requires Owner escalation under P-11** rather than automatic closure, though the FAIL verdict stands independently of it.
