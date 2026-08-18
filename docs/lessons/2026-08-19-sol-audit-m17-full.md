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

---

## 의뢰 C′-2 — 재정 Q1~Q9 분류 판정과 이행 충실성 (CAP 2400 · read-only)

**VERDICT: FAIL** · **NEW BLOCKER 2건**

**실행 비고 — 사망 원인이 여기서 확정되었다.** 이 의뢰는 **1차 시도가 약 600초에서 SIGTERM** 되고 **2차 시도를 detached 로 돌려 2400초 안에 완주**했다. 레인이 스스로 신고한 원인: *"첫 시도는 **내 하네스의 10분 상한**에 걸려 SIGTERM 됐고, 두 번째 실행을 detached 로 돌려 2400초 상한 안에 완주했다(codex 자체 실패 아님)."* 즉 **끊은 주체는 `timeout`(2400)도 codex 도 아니라 레인을 감싸는 도구 호출의 10분 상한**이며, 총괄이 `CAP` 으로 아무 값을 주어도 그 층은 흡수되지 않는다. 같은 원인이 A′(4분 45초 완주)·C′-1(8분 41초 완주)은 비껴갔고 C′-2·D(9분 55초·9분 58초)를 잡았다 — **완주와 사망을 가른 것은 의뢰의 난이도가 아니라 10분 선이었다.**

### FINAL (원문 — `/tmp/sol-final-c2.txt` · 18,015 B)

```text
VERDICT: FAIL  
핀 대조: `HEAD=fca126bc278f5ae4ba5a08f26b3297cb9f12b682` (일치)

테스트·검사기는 실행하지 않았다. 아래 판정은 문서·코드·시험 정의·산출물의 정적 대조 결과이며, 모든 경로는 작업 루트 기준이다.

## 물음 ① 상신·자기 보고의 편향

| 자리 | 판정 | 근거(앵커) |
|---|---|---|
| D-01 §6의 전체 프레이밍 | 축소·편향 | “M1 종결에 남은 두 물음”, “둘 다 총괄 관할 밖”이라고 문턱을 좁혔지만 같은 상신문에는 Q3~Q9도 존재한다. `docs/decisions/D-20260819-01-m16-close.md:204-206,258-318` |
| Q1 선택지 | 경도 유도, 선택지 누락은 아님 | 총괄 선호인 ⓐ만 바로 적용 가능한 패치까지 상세히 제시했으나, ⓑ와 양쪽 귀결·반론도 기록했다. `D-20260819-01-m16-close.md:208-245` |
| Q2 선택지 | 대체로 중립 | 유지/이관 양쪽과 귀결이 모두 제시됐다. `D-20260819-01-m16-close.md:247-256` |
| Q3 선택지 | 중립 | 순서 변경·진단 보강 등을 포함한 세 선택지를 구분했다. `D-20260819-01-m16-close.md:316-318` |
| Q4~Q6 선택지 | 불완전·편향 가능 | Q4는 사실상 단일 확장안, Q5는 네 쟁점의 존재만, Q6은 총괄 결론만 올렸다. 특히 과거 선택지 본문이 유실되어 Owner의 `(1)ⓐ·(2)ⓑ`가 정확히 무엇을 가리켰는지 현재 원장만으로 독립 검증할 수 없다. `D-20260819-01-m16-close.md:300-312`; `docs/decisions/ruling-20260819-02-Q1-Q9-H1-H10.md:116-118` |
| Q7 | 일부 누락 | Q7②만 ⓐ/ⓑ/ⓒ로 상신하고, 나중에 위임 처리한 Q7①·③의 선택지는 상신 단계에서 열거하지 않았다. `D-20260819-01-m16-close.md:258-260` |
| Q8 | 일부 누락 | ①·④만 핵심 선택지로 부각했고, 나중에 자체 처분한 ②와 “절반 재량”으로 가른 ③은 동등한 선택지로 상신하지 않았다. `D-20260819-01-m16-close.md:264-268` |
| Q9 | 강한 결론 유도 | ⓐ를 P-11을 지키는 유일한 안으로 두고 ⓑ는 반쪽, ⓒ는 독립성 포기, ⓓ는 형식적 감수로 서술했다. 반대 귀결을 숨기지는 않았지만 실질적으로 결론을 유도했다. `D-20260819-01-m16-close.md:287-296` |
| H5 | 상신 전 재정 관할 침범 | 총괄이 32/32 창과 4자리 연도를 스스로 확정했다. 이는 임계 확정에 해당한다. `D-20260819-01-m16-close.md:332`; `reader/reader-rules.yaml:1340-1363,1406-1410`; 관할선 `CLAUDE.md:23-24`, `docs/CHARTER.md:104-117` |
| H6 | 상신 전 재정 관할 침범 | 네 가지 둘러싼 구문 배제를 규칙으로 입법하여 수확 정답 집합을 바꿨다. `D-20260819-01-m16-close.md:333`; `reader/reader-rules.yaml:1033-1120` |
| H1~H4·H8~H10 | 재량 범위 | 기존 계약의 기계적 집행, 기록·시험·오류 수정 범주다. 다만 H5·H6과 함께 사후 일괄 추인되었다는 사실이 최초 월권을 소급해 없애지는 않는다. `D-20260819-01-m16-close.md:328-337`; `ruling-20260819-02-Q1-Q9-H1-H10.md:83-96` |
| H7 | 적정 상신 | 관문 승격을 `[OWNER-대기]`로 남겨 재정에 올렸다. `D-20260819-01-m16-close.md:334`; `ruling-20260819-02-Q1-Q9-H1-H10.md:44-45` |
| §3·§4 실측 표본 | 유리한 수치 왜곡 없음 | claims 129/fact 23, digest-ok 7건, convergence `0.8889→1.0`, 제외 89가 산출물과 맞는다. `D-20260819-01-m16-close.md:82-98`; `runs/20260819-101806-a2fbddd2/reports/TONGJU-REPORT.md:35-79,125-150`; 같은 run의 `10-read/lanes/lane-log.json:1-127` |
| D-02 Q5③ | 위임 범위 안 | flat-split 절차만 정했고 계약·스키마 값 공간이나 게이트를 바꾸지 않았다. `reader/procedure/10-decompose.md:87-105` |
| D-02 Q5④ | 주제는 위임 범위 안, 자기설명은 부정확 | “반대 방향이므로 모순 아님”이라는 설명과 달리 SPEC은 `attaches_to`의 단일 대상 선택과 요소 계층의 배치를 서로 다른 문제로 규정한다. 새 순위는 후보 밖 NCA 부모를 앞세울 수 있다. `D-20260819-02-m17-close.md:97-105`; `docs/SPEC.md:1542-1549,5467-5475`; `reader/procedure/10-decompose.md:69-80` |
| D-02 Q7①·③ | 위임 범위 안 | 접지 절차의 기록 방법만 정했고 스키마·게이트 판정 공간은 늘리지 않았다. `reader/procedure/20-grounding.md:53-72` |
| D-02 Q8② | 재량 범위 안 | 통합 요청서의 문맥을 보강했을 뿐 판정 항목은 추가하지 않았다. `engine/lanes/plan.py:502-528` |
| D-02 Q8③ | “절반 재량·절반 상신” 구분 타당 | 파일 무재작성은 I/O 구현 재량이지만, 요청 바이트 digest를 레인 로그 판정 항목으로 넣는 것은 계약·검사 관할 확장이라 상신 대상이다. `engine/lanes/file_adapter.py:61-105`; `docs/SPEC.md:5525-5531`; `D-20260819-02-m17-close.md:125-132` |
| D-02 Q9 자기보고 | 완료 과장 | D-02는 완료로 처리했으나 래퍼는 전달받은 `--sandbox`와 `--cd`를 그대로 사용한다. 정본 경로인지, 격리 사본인지, 두 경로가 다른지 검사하는 코드가 없다. `/home/laptop/.claude/agents/sol-auditor.md:41-69`; `D-20260819-02-m17-close.md:39` |
| D-02 §5 실패 기록 | 정성적 축소는 없음, 정량 검증 불가 | 세션 사망, 작성 레인 4개 유실, 미완료 3건과 영구 유실을 명시했다. 다만 원출력이 유실되어 “8 failures/실질 귀결 5건”은 독립 재계수할 수 없고, §7·§8도 비어 있다. `D-20260819-02-m17-close.md:170-193,222-230` |

## 물음 ② 이행 충실성

| 재정 | 충실/과잉/미달 | 근거(앵커) |
|---|---|---|
| Q1 = ⓑ 기각 | 충실 | Markush 구조 표지는 정확히 2형태다. 기각 취지와 기존 CP1 산출물 불소급 무효 귀결도 `open_question ④`에 기록됐다. `reader/reader-rules.yaml:293-296,351-369` |
| Q2 = ⓐ 이관 | 충실 | P-B 전체가 빠진 것이 아니라 `numeric.unreviewed-use`의 CP2 조각만 비-M1로 이관됐다. P-B의 나머지 다섯 요구는 남아 있다. `docs/SPEC.md:4578,4596-4597` |
| Q3 = ⓑ | 충실 | engine pin 검사가 entry 검사보다 앞선 기존 순서를 유지했다. 진단문도 원천 변경 시 P-U2 표시가 성립하지 않았음을 직접 말한다. `engine/stages/source.py:221-245,537-570` |
| Q4 = 승인 | 충실 | 추가 단위는 `b` 하나뿐이다. `bit/bits`는 기존 대안이며 별칭 확장은 없고, 순서상 `5 bits`는 계속 `bits`로 잡힌다. L0 계약도 함께 갔다. `reader/reader-rules.yaml:989-998`; `contracts/l0-format.yaml:323-326,351-361` |
| Q5① = ⓐ | 미달 | 절차에는 전제부 비요소, 규칙 ⑤와의 충돌 해소, 재검토 트리거가 있다. 그러나 같은 트리거를 rules 파일에도 유지하라는 문언과 달리 실제 `open_questions`에는 해당 전제부 트리거가 없다. `reader/procedure/10-decompose.md:49-55`; `reader/reader-rules.yaml:334-369` |
| Q5② = ⓑ | 과잉 | 맨 `\bwhen\b`·`\bif\b`는 제거됐고 새 목록은 파서가 아닌 regex 표지 목록이며, 대부분 조건구문이다. 그러나 원장은 정확한 10종을 “Owner 확인용 입법 초안”으로 남겼는데 확인 전에 운영 규칙이 됐다. 또한 `unless`는 자기보고와 달리 단일 토큰이다. `ruling-20260819-02-Q1-Q9-H1-H10.md:68`; `reader/reader-rules.yaml:285-311`; `D-20260819-02-m17-close.md:47-75` |
| Q5③ = 총괄 위임 | 충실 | flat-split 및 재검토 조건만 절차화했고 계약·스키마·판정 값 공간은 바꾸지 않았다. `reader/procedure/10-decompose.md:87-105` |
| Q5④ = 총괄 위임 | 미달 | 위임된 주제 안의 처분이지만 SPEC §9.33②의 구별을 지키지 않았다. 새 우선순위는 `attaches_to`의 대상 선택에 요소 계층 배치를 섞어 후보 밖 부모를 선택할 수 있다. `reader/procedure/10-decompose.md:69-80`; `docs/SPEC.md:1542-1549,5467-5475` |
| Q6 = 추인+근거 | 충실 | 픽스처 판을 일괄 올리지 않았다. 예컨대 base fixture는 여전히 `0.5.0`이다. 근거와 “대조 검사가 없다”는 사실도 명시됐다. `tests/fixtures/reader/base/material-spec.json:1-4`; `docs/SPEC.md:3812-3817` |
| Q7① = 총괄 위임 | 충실 | 두 문단을 모두 등재하고 불일치 표기를 요구한다. `reader/procedure/20-grounding.md:53-64` |
| Q7② = ⓐ | 충실 | 레인별 카운터는 좌표용으로 분리됐지만 양쪽 재시도가 같은 전역 `attempt`를 소비한다. 총 재시도 예산은 늘지 않았다. `engine/stages/read.py:1070-1084,1144-1149,1226-1233` |
| Q7③ = 총괄 위임 | 충실 | 빈 번호목록의 발견 사실·결과·주석만 절차화했다. `reader/procedure/20-grounding.md:68-72` |
| Q8① = 원칙 복원 | 충실 | 통합 요청서 하나에 각 접지 산출의 ID, 구성요소, 상태, 좌표가 실린다. `engine/lanes/plan.py:418-485,744-795`; 정적 시험 정의 `tests/test_m17_lanes.py:229-271` |
| Q8② = 명시 재정 없음 | 충실 | 요청 문맥 보강일 뿐 레인 로그나 검사기의 판정 관할을 늘리지 않았다. `engine/lanes/plan.py:502-528`; `tests/test_m17_lanes.py:292-365` |
| Q8③ = 명시 재정 없음 | 충실 | 무재작성은 구현 재량으로 처리하고, 로그 digest 추가는 관할 확장으로 보류했다. 갈림이 맞다. `engine/lanes/file_adapter.py:61-105`; `docs/SPEC.md:5525-5531` |
| Q8④ = 둘 다 등재+불일치 | 충실 | 접지·통합 양쪽 절차에 입법됐고, 양쪽 등재 시 도면부호 배제 집합이 넓어져 수확 정답지가 줄어든다는 귀결도 숨기지 않았다. `reader/procedure/20-grounding.md:53-66`; `reader/procedure/30-synthesis.md:93-100` |
| Q9 = ⓐ | 미달 | 문서상 격리 사본 한정일 뿐 기계적 경로 제한이 없다. `AUDIT_CD`에 정본을 넣고 쓰기 sandbox를 주면 정본 쓰기 경로가 열린다. `/home/laptop/.claude/agents/sol-auditor.md:41-69`; Owner 문언 `ruling-20260819-02-Q1-Q9-H1-H10.md:77` |
| H7 = 승격 승인 | 충실 | 필수 관문 4종째로 등재됐고 CLAUDE·SPEC·도구 docstring이 4종으로 개정됐다. `[OWNER-대기]`도 해소됐다. `CLAUDE.md:115-125`; `docs/SPEC.md:4478-4487`; `tools/check_lane_binding.py:3-14`; `tools/check_validator_enforcement.py:8-15` |
| H1~H6·H8~H10 추인 등재 | 충실 | 각 항목의 추인 사실이 원장에 개별 등재됐다. 이는 H5·H6의 최초 관할 침범과는 별개의 사후 효력 판정이다. `ruling-20260819-02-Q1-Q9-H1-H10.md:83-96` |

## 시험 3건의 개정 판정

1. `is_pinned_harvest_drift`: **시험 예외의 느슨화**다.  
   `[추가]`뿐 아니라 `[누락]`도 받아들이는 것 자체는 새 수확의 양방향 차이를 표현하지만, helper는 개수·좌표·예상 값 없이 임의의 `[추가]`/`[누락]`을 모두 면제한다. 따라서 향후 무관한 drift도 이 suite에서 숨길 수 있다. 생산 규칙의 느슨화라기보다 시험 oracle의 과도한 일반화다. `tests/test_m16_bibliography.py:105-121`

2. 실특허 기대값 `7→11`: **재정 변화의 정확한 기술**이다.  
   11개 항목의 정확한 목록을 고정하고, 새 4건의 `5b/4b/3b/2b` 단위도 각각 `b`로 검증한다. `tests/test_m16_harvest_boundary.py:312-360`

3. `boundary-right != 0` → `== 0`: **재정 변화의 정확한 기술**이다.  
   과거 우측 경계 때문에 탈락했던 네 항목이 `b` 승인 뒤 수확되므로 우측 경계는 0이어야 한다. 좌측 경계와 개별 수확값은 계속 구체적으로 고정돼 있다. `tests/test_m16_harvest_boundary.py:370-386`

H10 선례의 한계는 명확하다. 규칙 변화나 잘못된 픽스처 사실을 정확한 새 기대값으로 고치는 것은 허용되지만, 알려진 차이의 개수·좌표를 고정하지 않은 포괄 예외까지 정당화하지는 않는다. H10 자체는 잘못된 2023년을 실제 2024-01-05로 고치면서 우선순위 불일치를 유지한다. `tests/test_m1_reader.py:1766-1786`

## M1 요구사항표 판정

판정은 “구현 존재”뿐 아니라 §8.4가 요구하는 구현 앵커와 반증 시험의 원장 등재까지 포함한다. 시험은 실행하지 않고 정의만 대조했다. `docs/SPEC.md:4543-4545,4566-4568`

| 행 | 해소/부분/미해소/NOT ASSESSED | 근거(앵커) |
|---|---|---|
| N14-1 | 해소 | `reader/lib/derivation.py:401-424`; `tests/test_m1_reader.py:1080-1087` |
| N14-2 | 해소 | `tests/test_m1_reader.py:1090-1116` |
| N14-3 | 해소 | `tests/test_m1_reader.py:903-926` |
| N14-4 | 해소 | `engine/stages/freeze.py:403-411`; `tests/test_m2_read.py:2198` |
| N14-5 | 해소 | `tests/test_m1_reader.py:1263-1271` |
| N14-6 | 해소 | `reader/lib/derivation.py:719-744`; `tests/test_m1_reader.py:884-889` |
| N14-7 | 해소 | `reader/lib/inventory.py:109-135`; `tests/test_m1_reader.py:967-980` |
| N14-8 | 부분 해소 | 세 정책 시험은 존재하지만 요구사항표는 계속 “미작성”으로 기록한다. `tests/test_m1_reader.py:750-817`; `docs/SPEC.md:4556` |
| N14-9 | 해소 | `tests/test_m1_reader.py:1008-1059` |
| N14-10 | 해소 | `tests/test_m1_reader.py:1062-1077` |
| N14-11 | 해소 | `tests/test_m1_reader.py:830` |
| N14-12 | 해소 | `contracts/stages/source.yaml:96-119`; `tests/test_m2_read.py:834` |
| N14-13 | 부분 해소 | 배제·계수·escape 시험은 있으나 원장 셀이 미작성 상태이고 Q5② 미확인 초안이 live 규칙이다. `reader/lib/dependency_parse.py:116-183`; `tests/test_m1_reader.py:1700-1746`; `docs/SPEC.md:4561` |
| N14-14 | 해소 | 실행 환경 기록이 존재한다. `docs/decisions/D-20260818-02-m1-read.md:127-133` |
| P-1 | 부분 해소 | Q1 구현과 구체 시험은 있으나 요구사항표는 판정 배제/계수 시험을 미작성으로 기록한다. `tests/test_m1_reader.py:1700-1720`; `docs/SPEC.md:4572` |
| P-2a | 해소 | `tests/test_m1_reader.py:1749-1786`; `tests/test_m16_bibliography.py:162` |
| P-2b | 해소 | `tools/check_spec_refs.py:948`; `tests/test_tools_check_spec_refs.py:126,213` |
| P-3 | 부분 해소 | 정책 시험은 존재하지만 요구사항표의 미작성 표시는 갱신되지 않았다. `tests/test_m1_reader.py:750-817`; `docs/SPEC.md:4575` |
| P-4 | 부분 해소 | early/content-blind 관련 시험은 존재하지만 원장상 미작성이다. `tests/test_m2_read.py:1810,2441,2476,2509`; `docs/SPEC.md:4576` |
| P-A / P-U4 | 부분 해소 | 실행·shadow 시험은 있으나 요구사항표 증거 셀이 미해소다. `tests/test_m2_read.py:1650,1781`; `docs/SPEC.md:4577` |
| P-B | 부분 해소 | mutation·CP1 계수 시험은 생겼지만 표는 미작성 상태이고, 실특허 drift helper가 과도하게 넓다. `tests/test_m1_reader.py:1789-1868`; `tests/test_m2_read.py:2548-2579`; `docs/SPEC.md:4578` |
| P-C | 해소 | `engine/stages/__init__.py:345-373`; `tests/test_m2_read.py:1595,2650` |
| P-U1 / P-8 | 해소 | `tests/test_tools_run_worktree.py:109-238` |
| P-U2 | 부분 해소 | 실제 표시·crosslink 시험은 있으나 요구사항표가 여전히 미작성이다. `tests/test_m16_source_supersede.py:256-428`; `docs/SPEC.md:4581` |
| P-U3 | 부분 해소 | gate·absence 시험은 있으나 원장 셀이 미작성이다. `tests/test_m2_read.py:2509-2544,2608`; `docs/SPEC.md:4582` |
| P-U5 | 해소 | render parity 및 CP1 계수 시험이 존재한다. `tests/test_m2_read.py:2252,2548-2579` |
| P-5 | 부분 해소 | 구현·source 시험은 있으나 상위 기록이 여전히 Owner 대기 상태로 남아 있다. `tests/test_m2_read.py:834`; `CLAUDE.md:113` |
| P-6 | 부분 해소 | quorum 구현 시험은 광범위하게 존재하지만 요구사항표 및 Owner 대기 기록이 갱신되지 않았다. `tests/test_m16_quorum.py:92-413`; `docs/SPEC.md:4584`; `CLAUDE.md:113` |
| P-7 | 부분 해소 | 168h 스키마와 변이 자료는 있으나 형식적 증거 셀·대기 기록이 미해소다. `contracts/schemas/metrics-row.schema.json:21-135`; `docs/SPEC.md:4584`; `CLAUDE.md:113` |
| P-9 | 해소 | run-kind 계약과 이관 상태가 기록됐다. `contracts/run-kinds.yaml:15-42`; `docs/SPEC.md:4585` |
| P-12 | 해소 | lane-binding 계약의 정적 시험이 존재한다. `tests/test_m16_lane_binding.py:91-260` |
| P-13 | 해소 | 실제 run·CP1 및 수렴 산출이 존재한다. `runs/20260819-101806-a2fbddd2/reports/TONGJU-REPORT.md:35-79,125-150` |
| P-14 | 해소 | baseline이 등록된 행 전체를 동적으로 순회하며 corpus 시험도 존재한다. `tools/check_validator_enforcement.py:452-461`; `tests/test_m1_corpus.py:73-99` |
| P-11 | 미해소 | D-02의 최종 판정·종결 절이 비어 있고 §8.4 총괄도 여전히 `12/15 미완료`다. Q9 격리도 기계적으로 성립하지 않는다. `D-20260819-02-m17-close.md:222-230`; `docs/SPEC.md:4590`; `/home/laptop/.claude/agents/sol-auditor.md:41-69` |

`P-10`은 현재 §8.4에 독립 요구사항 행이나 좌표 자체가 없다(`docs/SPEC.md:4546-4588`). 내용을 추정해 새 요구사항으로 만들지 않고 분모에서 제외했다. `P-13`은 §8.4 독립 행은 아니지만 실제 산출 좌표가 있어 별도로 판정했다. `NOT ASSESSED` 항목은 없다.

## OUT-OF-SCOPE

- `tools/check_validator_enforcement.py:21,86,398`의 설명은 baseline을 “10종”, “READ 8 + FREEZE 2”라고 쓰지만 실제 등록은 `READ 10 + FREEZE 2 = 12`다. 실행은 동적 순회라 P-14 판정에는 영향이 없으나 docstring 계수는 낡았다. 실제 목록: `reader/lib/run_checks.py:33-51`; 규격: `docs/SPEC.md:4587`.

## NEW BLOCKER

- **Q9 격리 강제가 문언뿐이다.** 정본 realpath 차단, 허용 격리 루트 확인, 정본과 격리 사본의 상이성 검사가 없어 정본 쓰기 경로를 열 수 있다.
- **Q5②의 Owner 확인 전 입법 초안이 live 게이트 규칙으로 작동한다.** 확인되지 않은 10종이 `parse.unclassified-not-an-escape` 판정 공간을 바꾸므로 단순 문서 선반영이 아니다.```

---

## 의뢰 D — 변조 반증 8종 (CAP 2400 · **workspace-write** · 재정 Q9 ⓐ 첫 실전 적용)

**VERDICT: FAIL** · **NEW BLOCKER 1건**(범위 밖 추가 반증에서 발견)

**샌드박스 확인.** 쓰기는 격리 사본 안에서만 일어났다 — 감수 종료 후 `git status --porcelain` **빈 출력(clean)**, HEAD 불변, 정본 리포·홈 무접촉. **부수 사실 하나**: 사본의 `.git` 이 읽기 전용이라 `git checkout -- <path>` 복원이 매번 `Unable to create '.git/index.lock': Read-only file system` 으로 실패했고, Sol 은 **역패치로 바이트를 복원**한 뒤 `git diff --exit-code=0` 으로 확인하는 방식으로 대응했다.

**실행 비고.** 1차 호출은 발주대로 `timeout 2400` 을 걸었으나 **레인 Bash 도구의 상한 600초**에 걸려 10분에 SIGTERM(exit 143)됐고, `tee` 로 받은 `$LOG` 가 **파이프 버퍼링 때문에 0바이트**로 남아 부분 전사가 하나도 보존되지 않았다. 레인의 처방 제안 = `stdbuf -o0` + 리다이렉션. 2차를 백그라운드로 재실행해 완주했으며 **유효 감수 실행은 1회**다.

### 변조 8종의 결과 — **DETECTED 12 / NOT DETECTED 1 / 설계상 통과 1**

| # | 판정 | 탐지자 |
|---|---|---|
| M1ⓐ `unclassified` 회피 | DETECTED | `parse.unclassified-not-an-escape` |
| M1ⓑ Markush 어형 주입 | DETECTED | 회귀 시험 `test_markush_forms_were_not_widened`(K8 도구는 exit 0) |
| M2 시간 용법 `when` + **역대조** | DETECTED · 역대조 `in response to` 는 **정상 통과** | `parse.unclassified-not-an-escape` |
| M3ⓐⓑⓒ 누락·변조·추가 | DETECTED **3종 모두 구별** | `value.harvest-parity` |
| M4ⓐ 낡은 지문 | DETECTED | `LaneStaleResponseError` + 거부 행 기록 |
| M4ⓑ 사후 덮어쓰기 | DETECTED(자동 거부는 아니고 `response_digest` 대조로 드러남) | 로그 ↔ 파일 sha256 |
| **M5 lane-log `lane_id` 바꿔치기** | **NOT DETECTED** | **없음** |
| M6ⓐ 코어 키 재삽입 | DETECTED(plain·`-O` exit 1, K8 단독) | K8 |
| M6ⓑ 키 + 승인 목록 동시 등재 | K8 **설계상 통과** · 회귀 시험이 탐지 | `test_core_surface_closure` |
| M7ⓐⓑⓒ 관할·연도·경계값 | DETECTED — **33자 fail / 32자 pass** | `bib.priority-*-in-source` |
| M8ⓐⓑⓒ payload·역전이·순환 | DETECTED 3종 | `freeze.payload-immutable` |

**총괄이 예상한 M5 무탐지가 실측으로 확인되었다.** Sol 의 해석: Q7 ② 는 *"생성 시 올바른 좌표 기록"* 은 구현하나 **로그 자체의 사후 변조는 검증하지 않는다**. 다만 git 결박 저장소 안에서는 변경이 `git diff` 에 드러나므로 **Q7 ② 종결을 막는 결함으로 보지 않는다** — *"로그만 따로 반출하면 자체 진실성·디렉터리 결속이 없다"* 가 남는 관찰이다.

### FINAL (원문 — `/tmp/sol-final.cvxooE` · 9,659 B)

```text
NEW BLOCKER: P-12의 `input_digest`가 `request.md`에 인라인되는 **절차 문서 본문**을 결속하지 않습니다. 동일 지문으로 서로 다른 요청문이 성립하고 구 응답도 수용되는 것을 직접 재현했습니다. 상세는 아래에 적었습니다.

VERDICT: FAIL  
핀 대조: HEAD=`fca126bc278f5ae4ba5a08f26b3297cb9f12b682` (일치)  
샌드박스: 쓰기가 사본 안에서만 일어났는가 — 예

범위 고정 M1–M8 자체는 전부 평가했습니다. FAIL은 M4 추가 반증에서 발견한 NEW BLOCKER 때문입니다.

| # | 변조 | 판정 | 탐지자(규칙 id) | 기준선 출력 | 변조 후 출력 |
|---|---|---|---|---|---|
| M1ⓐ | CL-2를 `single→unclassified`.<br>복원 ✓ | DETECTED | `read.dependency-parse` / `parse.unclassified-not-an-escape` | 직접 실행: `pass checked=6 viol=0` | 직접 실행: `fail checked=5 viol=1`, locus=`CL-2.dependency_type`.<br>전체 도구에서는 `read.convergence`와 변조 케이스 9건도 base/peer 불일치로 동반 실패했다. |
| M1ⓑ | Markush에 `at least one of` 추가.<br>복원 ✓ | DETECTED | 직접 `dependency_parse`; `test_markush_forms_were_not_widened` | 합성 문장: markers=`[]`, `parse.unclassified-not-an-escape` 발생 | markers=`["Markush"]`, dependency 검사 `pass`로 반전. 전체 validator는 `exit 0`이지만 회귀 시험은 `1 failed`(허용 어형 2개 대신 3개)로 개정을 잡았다. |
| M2 | 시간 용법 `when`만 있는 CL-2를 `unclassified`; 이어 `in response to` 역대조.<br>복원 ✓ | DETECTED | `parse.unclassified-not-an-escape` | 무변조 dependency: `pass checked=6 viol=0` | `when`: markers=`[]`, `fail checked=5 viol=1`.<br>`in response to`: markers=`["조건부"]`, `pass checked=5 viol=0`. 정직한 사용은 벌받지 않았다. |
| M3ⓐ | quoted fact M16 삭제.<br>복원 ✓ | DETECTED | `read.value-derivation` / `value.harvest-parity` | READ 10종 전부 pass; value `checked=24 viol=0` | 실패 검사는 value 하나뿐. `value.harvest-parity`, locus=`harvest:[0048][17,24)`, 메시지 `[누락]`. |
| M3ⓑ | M17 `value_raw` 한 글자 변경, 좌표 유지.<br>복원 ✓ | DETECTED | `value.harvest-parity` `[변조]`; 같은 검사의 `value.quoted-span`, `value.type-agrees` | READ 10종 전부 pass | 실패 검사는 value 하나뿐, 위반 3건. parity가 locus `M17.value_raw`를 `[변조]`로 구별했다. |
| M3ⓒ | quoted fact M44 추가.<br>복원 ✓ | DETECTED | `read.value-derivation` / `value.harvest-parity` | READ 10종 전부 pass | 실패 검사는 value 하나뿐. locus=`M44.value_raw`, 메시지 `[추가]`. |
| M4ⓐ | 실제 retry 레인 응답에 다른 요청의 지문 `ec2b5064…` 주입.<br>복원 ✓ | DETECTED | `LaneStaleResponseError`; `LaneJournal.record_rejected` | 기대 지문 `8bcb6066…`; 응답 SHA/log `4b1e4971…` | `_dispatch`가 `LaneStaleResponseError`로 거부. 로그: `rejected=true`, `digest_ok=false`, `echoed_digest=ec2b5064…`. |
| M4ⓑ | 소비 뒤 `screening_memo.direction: clear→drop`로 response 덮어쓰기.<br>복원 ✓ | DETECTED | 로그 `response_digest` ↔ 현재 파일 sha256 대조 | 소비 시 `logged=current=4b1e4971…` | 덮어쓴 뒤 `logged=4b1e4971…`, 현재 SHA=`53394a…`: `MISMATCH`. 자동 거부 규칙은 아니지만 소비본과 현 파일의 차이는 명백히 남았다. |
| M5 | lane-log 행의 `batch-0→retry-1/batch-0`, 디렉터리 불변.<br>복원 ✓ | NOT DETECTED | 없음 | `check_lane_log_shape`: `pass checked=7 viol=0`; 공식 lane 도구 PASS | 여전히 `pass checked=7 viol=0`; 중복 lane ID도 무위반. 공식 도구도 자기 임시 시나리오만 검사해 PASS. 수동 디렉터리 대조에서만 로그 SHA와 해당 retry 파일 SHA의 불일치가 보였다. |
| M6ⓐ | `patent.marketing_verdict`를 `[공유 코어]`와 함께 재삽입.<br>복원 ✓ | DETECTED | `check_spec_refs.py` / K8 코어·확장 경계 | plain·`-O`: K1–K8 전부 PASS | plain·`-O` 모두 `exit 1`; 정확히 K8만 결함 1건, 경로=`properties.patent.properties.marketing_verdict`. |
| M6ⓑ | 같은 키와 core-surface 승인 항목을 함께 추가.<br>복원 ✓ | DETECTED | K8은 미탐지; `test_core_surface_closure[sol-marketing-verdict-*]`가 탐지 | plain·`-O`: K1–K8 PASS; 관련 최종 회귀 시험 PASS | K8 plain·`-O`는 예상대로 `exit 0`. 그러나 회귀 시험은 해당 plain/opt 2건을 실패시켰다(`2 failed, 6 passed`). |
| M7ⓐ | 관할 `US→IP`; `IP`는 원천의 다른 곳(`IPC`)에 존재.<br>복원 ✓ | DETECTED | `read.bibliography` / `bib.priority-jurisdiction-in-source` | base bibliography `pass checked=12 viol=0` | 실패 검사는 bibliography 하나뿐, 위반 1건. 전역 문자열 존재로는 통과하지 않았다. |
| M7ⓑ | priority 날짜와 earliest priority를 함께 `1900-01-01`로 위조.<br>복원 ✓ | DETECTED | `bib.priority-year-in-source` | bibliography `pass checked=12 viol=0` | bibliography에서 정확히 year 규칙이 실패하고 `bib.earliest-priority`는 통과했다. 원문 값 자체도 바뀌어 value 검사에서 `value.bibliographic`·`value.harvest-parity [변조]`가 동반 실패했다. |
| M7ⓒ | 실특허 우선권 번호에서 관할 시작점까지 33자/32자 경계 대조.<br>복원 ✓ | DETECTED | `bib.priority-jurisdiction-in-source` | 실특허 bibliography `pass checked=24 viol=0` | 거리 33: `fail checked=24 viol=1`.<br>거리 32: `pass checked=24 viol=0`. 32자 포함 경계가 그대로 집행된다. |
| M8ⓐ | rev2 M1의 `label_en` payload만 변경.<br>복원 ✓ | DETECTED | `freeze.payload-immutable` / `lifecycle.payload-frozen` | ID `pass checked=89`; payload `pass checked=46` | ID 검사는 유지. payload만 `fail checked=46 viol=1`, locus=`M1`. |
| M8ⓑ | M24 `retracted→active`.<br>복원 ✓ | DETECTED | `freeze.payload-immutable` / `lifecycle.one-way` | ID·payload 모두 pass | ID 검사는 유지. payload만 위반 1건, locus=`M24.status`, 기대=`retracted → (전이 없음)`. |
| M8ⓒ | M44 승계 대상을 M23으로 바꿔 M23→M44→M23 순환 생성.<br>복원 ✓ | DETECTED | `freeze.payload-immutable` / `supersession.acyclic` | ID·payload 모두 pass | ID 검사는 유지. 같은 acyclic 규칙이 M23·M44 각 출발점에서 2건 발생했다. |

`복원 ✓`는 다음 독립 변조 전에 역패치를 적용하고 해당 경로의 `git diff --exit-code=0`을 확인했다는 뜻입니다. 요청된 `git checkout -- <path>`도 매번 먼저 시도했지만, 격리 환경의 `.git`이 읽기 전용이라 모두 다음 오류로 실패했습니다.

```text
fatal: Unable to create '.../.git/index.lock': Read-only file system
```

따라서 Git 인덱스를 우회하거나 손대지 않고 역패치로 동일 바이트를 복원했습니다.

NOT DETECTED 항목의 해석:

- M5는 Q7②의 “생성 시 올바른 좌표 기록”은 구현하지만, 로그 자체의 사후 변조를 검증하지는 않습니다. Git에 결박된 신뢰 저장소라는 경계에서는 변경이 `git diff`에 드러나므로 Q7② 종결을 막는 결함으로 보지는 않습니다. 다만 로그만 따로 반출하면 자체 진실성·디렉터리 결속이 없습니다.
- M6ⓑ의 K8 통과는 H1이 승인한 화이트리스트 설계와 일치합니다. K8은 승인 목록 개정의 권한을 판정하지 않고 변경을 review-visible하게 만드는 검사입니다. 알려진 `marketing_verdict`는 별도 회귀 시험이 막지만, 임의의 새 키와 승인 목록을 함께 고치는 일반 행위는 인간 재정·코드 리뷰 경계에 의존합니다.
- M2 역대조와 M7의 32자 상태는 각각 정직한 conditional 표지와 창 내부 경계의 의도된 통과입니다.

최종 기준선 재실행:

- `check_validator_enforcement.py`: `PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족`
- `check_spec_refs.py` plain 및 `-O`: K1–K8 전부 PASS
- `check_lane_binding.py`: 정상 소비·낡은 응답 거부·사후 교체 탐지 전부 PASS
- 관련 회귀 시험: `24 passed`
- `git diff --exit-code`: `0`

사본 최종 상태(`git status --short`):

```text
(출력 없음 — clean)
```

OUT-OF-SCOPE:

- 지정된 M4ⓐ/ⓑ 외의 추가 반증에서, `input_digest`가 `request.md`의 절차 본문을 결속하지 않는 것을 발견했습니다. [contract.py](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/lanes/contract.py:42)는 `prompt_path`만 해시하고, [contract.py](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/lanes/contract.py:225)는 그 경로의 현재 본문을 요청문에 인라인합니다.
- 실물 fp-3 retry 레인에서 JSON 지문·재계산 지문·응답 반향은 모두 `8bcb60667334e4bdc1466a3f89f72cf251c5eb1dea6780c33b986fc5d68b6fd5`로 일치했지만, 보관 요청문 SHA는 `a282a9bc…`(29,046 bytes), 현재 절차로 다시 렌더한 SHA는 `a959e4cd…`(39,152 bytes)로 달랐습니다.
- 직접 `FileLaneAdapter` 경로에서는 요청문이 새 본문으로 바뀌어도 `request.json` 지문이 그대로였고, 구 응답이 `_dispatch`에서 수용됐습니다. `check_lane_binding.py`는 `instructions` 변경만 시험하므로 이 경우를 잡지 않습니다. 또한 READ 진입 검사는 원천 지문을 대조하지만 현재 HEAD와 `run.yaml#engine.commit`의 일치를 대조하지 않습니다.

NEW BLOCKER: P-12 요청 지문에 절차 문서 본문 또는 그 digest를 포함하거나, READ 진입에서 엔진 핀을 강제하지 않으면 **서로 다른 실제 프롬프트가 같은 지문을 공유하고 구 응답이 통과할 수 있습니다.**```
