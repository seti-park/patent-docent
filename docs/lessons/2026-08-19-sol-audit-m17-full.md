# sol 독립 감수 원문 — M1.7 분할 감수 4의뢰 (2026-08-19 후반)

**보존 근거.** 재정 2026-08-18 **N7 ①** — 모든 외부 감수·검증 산출물은 수령 즉시 **원문 그대로** `docs/lessons/`에 보존하고, 처분표·요약은 그 원문을 가리키는 포인터로만 존재한다.

| 항목 | 값 |
|---|---|
| 감수자 | GPT-5.6-sol, reasoning effort max, 교차벤더 독립 |
| 구동 | `sol-auditor` 레인 4건(Opus 래퍼가 codex CLI 구동) |
| **감수 핀** | `fca126bc278f5ae4ba5a08f26b3297cb9f12b682` — **4의뢰 전부 사본에서 `git rev-parse HEAD` 로 대조 확인** |
| 격리 사본 | `git clone --no-hardlinks` + 핀 체크아웃 + `.venv` 사전 구축, 의뢰별 전용 4벌 (재정 2026-08-19 **Q9 ⓐ**) |
| 샌드박스 | A′·C′-1·C′-2 = `read-only` · **D = `workspace-write`**(Q9 ⓐ의 첫 실전 적용 — 격리 사본 한정) |
| 상한 | A′ 1200s · 나머지 2400s (개정 `sol-auditor.md` 의 발주 지정 상한 ≤2400) |
| 적용 규율 | 재정 **P-11**(범위 고정) |

**★ 이 파일의 지위에 관한 정직한 표기.** 각 절의 「FINAL(원문)」 블록은 codex `--output-last-message` 가 남긴 **Sol 의 최종 메시지 파일 그대로**다(레인의 요약이 아니다). 레인이 덧붙인 앵커 확인·전달 코멘트는 별도로 표시한다. 직전 회차(`2026-08-18-sol-audit-m15-full.md`)는 레인의 전달본이 총괄이 수령한 최대 원문이었고, **이번 회차는 Sol 의 파일 자체를 회수했다** — 그 차이가 재정 N7 이 요구한 보존 등급의 개선이다.

**실행 비고.** 감수 착수 후 총괄이 문서 커밋 2건을 더 했다(`8b46e6a` §9.33 ② 추기 · `184002b` 관문 환경 오류 처분). 즉 **감수 대상은 핀 시점이고 현행 HEAD 는 그보다 앞서 있다** — 직전 회차와 같은 형태이며, 두 커밋 중 뒤엣것은 **이 감수(A′)의 지적에 대한 처분**이다.

---

## 의뢰 A′ — 기계적 확인 (CAP 1200 · read-only)

**VERDICT: FAIL** (관문 4종 중 `check_lane_binding.py` 만 exit 1 — 읽기 전용 샌드박스의 임시 디렉터리 부재)

### FINAL (원문 — `/tmp/sol-final.an4cS5`)

```text
VERDICT: FAIL

| # | 확인 | 판정 | 앵커(실출력) |
|---|---|---|---|
| A1 | 핀 지문 대조 | PASS | `fca126bc278f5ae4ba5a08f26b3297cb9f12b682` |
| A2 | 관문 4종 exit 0 (plain) | FAIL | `check_spec_refs=0`, `check_schema_enforcement=0`, `check_validator_enforcement=0`, `check_lane_binding=1`. 실패 출력: `FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m17/A']` |
| A3 | 관문 4종 exit 동일 (`-O`) | PASS | plain=`[0, 0, 0, 1]`, `-O`=`[0, 0, 0, 1]` |
| A4 | 기준선 청정 | PASS | 아래 §① 실출력: 검사 12종 전건 `viol=0` |
| A5 | 전주기 pytest 1회 | PASS | 최초 실행은 임시 디렉터리 오류로 exit 1. 지정된 fallback 결과: `412 passed, 1 warning in 83.53s (0:01:23)` — passed=412, failed=0, exit 0 |
| A6 | 통주 3 산출물 실재 | PASS | `{"expected_count": 6, "files": {"10-read/convergence.json": true, "10-read/lanes/lane-log.json": true, "10-read/material-spec.json": true, "10-read/material-spec.md": true, "TONGJU-REPORT.md": true, "run.yaml": true}, "missing": [], "present_count": 6}` |
| A7 | 통주 3 수치 대조 | PASS | `{"convergence": {"all_12_pass": true, "non_pass_ids": [], "pass_rows": 12, "rows": 12}, "engine": {"commit": "f0b4ca15b2129a1fe191f53d2e834de7b55c3039", "starts_with_f0b4ca1": true}, "lane_log": {"all_7_digest_ok_true": true, "digest_not_true_ids": [], "digest_ok_true": 7, "roundtrips": 7}}` |

A4 §① 실출력:

```text
== ① 기준선 — 무변조 코퍼스가 검사 12종을 통과하는가 ==
  [ok ] read.schema                checked=1    viol=0   vacuous=none
  [ok ] read.source-digest         checked=1    viol=0   vacuous=none
  [ok ] read.verbatim              checked=83   viol=0   vacuous=none
  [ok ] read.pointer-resolve       checked=123  viol=0   vacuous=none
  [ok ] read.coverage              checked=24   viol=0   vacuous=none
  [ok ] read.dependency-parse      checked=6    viol=0   vacuous=none
  [ok ] read.value-derivation      checked=24   viol=0   vacuous=none
  [ok ] read.bibliography          checked=12   viol=0   vacuous=none
  [ok ] read.claim-inventory       checked=9    viol=0   vacuous=none
  [ok ] read.convergence           checked=6    viol=0   vacuous=none
  [ok ] freeze.id-monotonic        checked=89   viol=0   vacuous=none
  [ok ] freeze.payload-immutable   checked=46   viol=0   vacuous=none
```

OUT-OF-SCOPE:

- pytest 종료 시 읽기 전용 파일시스템 때문에 `.pytest_cache` 생성 경고 1건: `PytestCacheWarning: could not create cache path ... [Errno 30] Read-only file system`

NEW BLOCKER: 없음```

### 레인의 앵커 확인 (전달자 코멘트 — Sol 판정 아님)

- `tools/check_lane_binding.py:276` = `workdir = tempfile.mkdtemp(prefix="lane-binding-")`, `:296` = `sys.exit(main())` — Sol 이 인용한 트레이스백 위치는 **실재한다**. 이 도구는 `tempfile.mkdtemp` 를 쓰는 유일한 관문이라, read-only 샌드박스에서 TMPDIR 이 없을 때만 나는 환경성 실패로 보인다.
- 핀은 레인이 독립으로 `git rev-parse HEAD` 를 돌려 동일 값 확인.

**총괄 처분** = 커밋 `184002b`. 지적은 타당하다 — SPEC §8.3 3항의 종료 코드 규약(`1` = 검증 실패 · `2` = 입력·환경 오류)을 이 도구가 어기고 있었고, 재정 H7 이 관문으로 올린 직후이므로 무게가 다르다. `mkdtemp` 을 `fail_env`(exit 2)로 감쌌고 회귀 반증을 붙였다. **로컬에서는 `/tmp` 가 쓸 수 있어 자연 재현되지 않는다** — 감수가 아니면 나오지 않았을 지적이다.

---

## 의뢰 C′-1 — P-B 잔여 아티팩트의 독립 재계수 (CAP 2400 · read-only)

**VERDICT (P-B): 부분 해소**

### FINAL (원문 — `/tmp/sol-final.Ucb80O`)

```text
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

NEW BLOCKER: 없음```

### 레인의 앵커 확인 (전달자 코멘트 — Sol 판정 아님)

인용 좌표(항목 ID · locator · 원문 인용구)가 전부 실재 내용으로 해소된다. 계수는 레인이 독립으로 재현했다.

**총괄의 확인 사항 두 가지(감수 판정을 조정하지 않는다).**

1. **판정 기준의 위치.** `부분 해소` 의 근거는 *"정답지에 활성 `fact` 아티팩트 3건이 남아 있다"* 이다. 그런데 요구사항표의 P-B 문언은 **전수 수확 · 수확 소유권 · `value.harvest-parity` · 역참조 · CP1 전량 카운트** 다섯을 요구하며 **"정답지 순도"를 명시 요건으로 들지 않는다.** 감수는 요건 문언보다 엄격한 기준을 적용했다. **총괄은 그 판정을 그대로 전달하며**(감수 판정 불간섭), 판정이 어느 기준 위에 섰는지만 기록한다 — 그 기준이 옳은지는 Owner 의 판단 영역이다.
2. **총괄 문서의 자기모순 적발.** 감수는 `D-20260819-01` §4.6 의 *"배제가 진짜를 먹지 않았다"* 를 **사실과 다르다**고 반박했다. 그 반박은 옳고, **실은 그보다 무겁다** — 같은 문서 §6 Q4 가 *"진짜 수치 넷이 … 아무 기록 없이 사라지고 있었다"* 고 적는다. 즉 한 문서가 같은 자리에 대해 **두 말을 한다**. 과거 처분 문서는 소급 수정하지 않으므로(RULINGS-LEDGER 의 M0 감수 건수 정정 선례) 정정을 여기와 `D-20260819-02` 에 남긴다.

---

## 의뢰 C′-2 · D — **산출 없이 사망** (기록)

**둘 다 최종 메시지를 남기지 못했다.** `--output-last-message` 파일이 **0바이트**다.

| 의뢰 | 실행 시간(총괄 실측) | `--output-last-message` | 상태 |
|---|---|---|---|
| A′ | **4분 45초** | **2,662 B — 판정 회수됨** | 완주 |
| C′-1 | **8분 41초** | **6,773 B — 판정 회수됨** | 완주 |
| C′-2 | **9분 55초** | 0 B | **사망** |
| D | **9분 58초** | 0 B | **사망** |

**★ 사망 시각이 캡을 가리키지 않는다 — 이것이 이 회차의 하네스 진단이다.** 총괄이 발주한 상한은 A′ `CAP=1200` · 나머지 `CAP=2400` 이었고, **실행 중 프로세스의 명령행이 `timeout 2400` 임을 총괄이 `ps` 로 직접 확인했다.** 그런데 죽은 둘은 **9분 55초·9분 58초**, 즉 **약 600초**에서 끊겼다. 발주 상한이 2400인데 600에서 죽었다면 **끊은 주체는 `timeout` 이 아니다.** 원인은 레인 밖(codex 또는 그 경유 계층)에 있으며, 총괄의 발주 파라미터로는 흡수되지 않는다.

**두 번째 사실 — `tee` 처방은 절반만 들었다.** 직전 라운드가 처방한 `tee` 는 적용되었으나 회수된 로그 크기가 최종 메시지와 거의 같았다(C′-1: 로그 6,774 B vs FINAL 6,773 B). 즉 codex 는 이 실행 형태에서 **진행분을 흘리지 않고 끝에 한 번에 낸다** — 그러므로 `tee` 는 **완주한 실행의 사본**을 남길 뿐 **중도 사망의 부분 전사를 만들지 못한다.** 직전 라운드의 처방이 겨냥한 실패 형태에 그 처방이 닿지 않는다는 것이 이번 실측이다.

**★ 그러나 D 는 변조를 실제로 수행했다.** 사망 시점의 격리 사본에 변경이 남아 있다 —

```
$ git -C /home/laptop/projects/workspaces/pd-audit-m17/D status --short
 M tests/fixtures/reader/base/material-spec.rev2.json
```

**재정 Q9 ⓐ 의 쓰기 모드가 실제로 작동했다는 물증**이며, 직전 라운드에서 `--sandbox read-only` 가 원천 봉쇄했던 그 능력이 이번에 처음 열렸다. 판정문은 잃었으나 **능력의 실증은 남았다.** 사본은 **삭제하지 않고 보존한다** — 회수·재개 레인이 그 좌표를 쓴다.

**판정 회수 경로.** `~/.codex/sessions/**/rollout-*.jsonl` 에 전 이벤트가 남으므로 죽은 두 세션의 판정도 회수 가능하다(Owner 재정으로 별도 레인이 수행 중). 회수분이 도착하면 이 파일에 **원문 그대로** 추기한다 — 재정 N7 의 보존 의무는 "총괄이 받은 것"에 걸리며, 늦게 받은 것도 받은 것이다.
