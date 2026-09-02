# 감사 원문 보존 — G-6 구현 독립 감수 (2026-09-01)

## ★ 총괄 머리말 (2026-09-02 · 이 절은 총괄 저작이며 감수자·자문가가 쓴 절이 아니다)

지적 열거 = X-1, X-2, X-3, B-1, A-1, C-1, C-2, B-2, D-1, C-3, A-2, A-3, E-2, F-2
id 와 순서는 아래 감사 원문의 지적 요약표가 붙인 것이다. 원문은 `A-2/A-3` 를 **한 행**으로 묶었고(그래서 원문의 계수는 13건이다) 처분도 하나인데, 처분표는 id 하나에 한 행이라 `A-2`·`A-3` 로 나누어 같은 값을 싣는다 — 나눈 것은 표기이지 처분이 아니다. `C-0`·`C-0b`·`C-4` 처럼 §2 안의 소절 번호는 지적이 아니므로 열거에 들지 않는다. 처분은 `docs/decisions/DISPOSITIONS.md` §1 에 행으로 선다.
이 절은 재정 T27 의 소급 등재로 2026-09-02 에 삽입되었다. 아래 제목 줄부터는 반입 당시(2026-09-01)의 문면 그대로다.

## 반입 당시의 문면 — 이하 원 파일 그대로 (이 제목 줄 한 줄만 2026-09-02 총괄 삽입 · 저자 경계는 원 파일의 표기를 따른다)

**규율 10 의 이행.** 판정 = **FAIL**(BLOCKER 2 · HIGH 2 · MED 5 · LOW 4).

**좌석** = **opus max**(교차 벤더 — 저작이 sol 이므로 감사는 opus, ROUTING §3 M9).
상설 레인에 그 좌석이 없어 **메인 세션이 CLI 로 직접 호출**했다
(`claude -p --model claude-opus-5 --effort max` · 배경 분리 + 마커 폴링).

**대상 커밋** = `ad5e471` · **읽기 전용 준수 확인** — 총괄이 감사 전후 트리 지문을 대조했다
(`6b100e082389924b` 동일 · `git status` 0행).

---

감사 완료. 정본은 손대지 않았고(`git status` 빈 상태 유지), 모든 실행은 격리 사본에서 했다.

---

# 감사 판정 — G-6 구현(`ad5e471`) · 좌석 opus max

## 1. 판정

**`FAIL`** — 이 커밋이 **런을 중단시키는 회귀 2건**을 들여왔다(`X-1`·`X-2`). 조기 국면이 같은 `check_id` 행을 **두 벌** 싣게 되면서, 그 payload 를 만드는 `to_convergence_payload` 가 ⑴ `vacuous_pass` 에 중복을 넣고(`uniqueItems: true` 위반) ⑵ 비정본 실행의 `unclassified` 청구항 ID 를 **정본 명세에서** 조회해 빈 문언을 싣는다(`minLength: 1` 위반). 둘 다 `_validate_convergence` 에서 `RunnerContractError` 로 터지며, **`convergence-early.json` 이 아예 쓰이지 않는다** — 판정서가 없으므로 P-U3 봉투가 결속할 대상도 사라진다. 부모 커밋에서는 같은 입력이 정상 진행했다.

재정 T16 이 명한 여섯은 **전부 실물이 있다**(§2 A). 문제는 명령된 것의 부재가 아니라 **명령되지 않은 부작용**이다.

| id | 격 | 무엇 |
|---|---|---|
| **X-1** | **BLOCKER** | 두 실행의 `read.dependency-parse` 가 함께 공허(`checked==0`)면 `vacuous_pass` 중복 → 런 중단 |
| **X-2** | **BLOCKER** | 비정본의 `unclassified` ID 가 정본 claims 에 없으면 `text_verbatim: ""` → 런 중단 |
| **X-3** | HIGH | `unclassified_dependents` 가 **마지막 행(비정본)** 으로 덮인다 — 정본 신고분 소실 · 문언 오귀속 |
| **B-1** | HIGH | 「계약에 없으면 상한을 지어내지 않고 거부」 규율이 **무시험** — 두 거부 경로를 통째로 지워도 495 전건 통과 |
| **A-1** | MED | 계약이 `read.convergence: phases: [exit]` 라 적었는데 그 검사는 **조기에 돈다**. 같은 파일 `judged_here` 는 반대로 적었고, **신설 시험이 거짓 쪽을 못박는다** |
| **C-1** | MED | `test_convergence_runs_before_grounding` 이 이제 **수렴을 한 번도 실행하지 않은 채** 통과한다 |
| **C-2** | MED | Owner '계속' 봉투가 **청구항 소유 실패**까지 통과시킨다(적용 범위의 조용한 확대 · 무시험) |
| **B-2** | MED | 비누설 시험이 **상대 실행의 검사 소견 전달**을 잡지 못한다 |
| **D-1** | MED | Q7 후계 가드가 **세탁 가능** — 조치 표에 무관한 `retry(2)` 한 줄이면 조기 예산 2배가 통과 |
| **C-3** | LOW | `repeated` 가 `read.schema` 의 `halt` 를 앞지른다(계약은 halt, 실물은 escalate) |
| **A-2/A-3** | LOW | `early_phase_spec.placeholders` · `retry_budget.points[].{scope,checks,repairs}` 는 **러너가 읽지 않는 선언**이고 대부분 무결속 |
| **E-2** | LOW | 반증된 전제(「유일한 탐지기」)가 **코드·시험·원장 색인 3곳**에 정정 포인터 없이 살아 있다 |
| **F-2** | LOW | 커밋 메시지 계수 오기 — 실측 `484 → 495 (+11)`, 메시지는 `479 → +16` |

---

## 2. A~F

### A. 주장 대 실물 — **여섯 전부 실물이 있다**

| 재정 항목 | 좌표 | 판정 |
|---|---|---|
| ① 조기 등재 + 출구 존치 | `reader/lib/run_checks.py:48-63`(`EARLY_CLAIM_CHECK_IDS`·`run_early_claim_checks`) · `engine/stages/read.py:1466-1475` · `READ_CHECK_IDS` 에 두 검사 **그대로 존치**(`run_checks.py:38,44`) · 계약 `phases: [early, exit]`(`read.yaml:470,502`) | **구현됨** |
| ② 판정점별 예산 | `read.py:748-772`(`_retry_budget(contract, point)`) · `1402-1403` · `decompose_attempt: dict[str,int]` `1425` · `tail_attempt` `1576` | **구현됨** |
| ③ 조기 관문 순서 + 수렴 보류 | `read.py:1487-1495`(`if not claim_failures:` 로 수렴 실행을 가둔다) · `1497-1501`(행 순서) | **구현됨** — 프로브 P2·P4 가 반증 |
| ④ 분해 전용 명세 = 파이프라인 소유 | 계약 `early_phase_spec`(`read.yaml:275-306`) · `read.py:974-997`(`decompose_only_spec` → **같은** `assemble_spec`) | **구현됨** (단 A-2) |
| ⑤ 두 실패의 뜻 성문화 | 계약 `phase_meaning` ×2(`read.yaml:479-483, 506-511`) · 등재부 주석 `run_checks.py:48-60` | **구현됨** |
| ⑥ 되먹임 비누설 | `read.py:1521-1524`(각 실행 자신의 Finding 만) · 수렴 분기 `1536-1539` | **구현됨** — 수렴 소견은 `jaccard=…` 뿐이라 내용 누설 채널이 없다(`reader/lib/convergence.py:258-264`) |

**주장만 있고 구현이 없는 자리는 찾지 못했다.** 다만 **계약이 사실과 다르게 적힌 자리**가 하나 있다.

**A-1 — `read.convergence` 의 `phases` 가 거짓이고, 신설 시험이 그 거짓을 못박는다.**
`read.yaml:512-513` 이 `read.convergence: phases: [exit]` 로 적었다. 그 블록 머리말은 *"phases 가 그 호출점을 든다"* 고 선언한다. 그런데 `read.convergence` 는 **재정 P-4 이래 조기 관문에서 돈다** — 같은 파일 `early_phase_spec.judged_here`(`read.yaml:298-301`)가 그것을 명시하고, 실물 산출도 그렇다:

```
checks  = ['read.input-digest', 'read.claim-inventory', 'read.dependency-parse',
           'read.claim-inventory', 'read.dependency-parse']      ← 청구항 실패 시
# 정상 런에서는 마지막에 'read.convergence' 가 붙는다(test_v1d 가 그것을 잰다)
```

한 계약 파일이 같은 검사의 호출점을 **두 말로** 적었다. 그리고 `test_claim_check_phase_meanings_and_exit_rows_are_declared:517-521` 이 `early_declared != set(EARLY_CLAIM_CHECK_IDS)` 이면 실패하도록 써서 — `read.convergence` 에 `early` 를 **붙이면 시험이 깨진다**. 이 리포가 반복해 벌해 온 형태다(*"강제의 범위를 실제보다 좁게 말했다"* — SPEC §8.3 7항).

**A-2 — `early_phase_spec.placeholders` 는 산출 형태와 대응하지 않고, 시험이 그 대응을 재지 않는다.** 실측:

```
actual top-level keys : ['claims','extensions','figures','items','patent','provenance',
                         'reader_version','run_id','schema','spec_version','status']
declared - actual     : ['groundings', 'harvest', 'synthesis']    ← 셋 다 산출 키가 아니다
actual - declared     : ['extensions', 'figures']                 ← 실제 자리표시는 이 둘
```
`placeholders` 가 든 셋은 `assemble_spec` 의 **인자 이름**이지 명세 필드가 아니다. `test_decompose_only_spec_matches_early_phase_contract` 는 `carries` 만 대조하고 `placeholders` 는 **한 줄도 읽지 않는다** — `figures == []`·`drop_signal == {}` 는 시험에 손으로 박혀 있다.

**A-3 — 계약의 나머지 선언 필드는 러너가 읽지 않는다.** `_retry_budget` 이 읽는 것은 `id`·`max_retries` **둘뿐**이다(`read.py:761-772`). `scope`·`repairs`·`checks`·`failure_means`·`escalate_on_repeat.signature`·`feedback_discipline` 은 전부 산문이다. 특히 **조기 검사 집합이 계약 두 곳에 적혀 있다** — `retry_budget.points[0].checks` 와 `early_phase_spec.judged_here` — 그런데 시험이 결속하는 것은 뒤엣것뿐이다. 이 리포 자신의 문언: *"두 벌이 생기면 한 벌은 반드시 낡는다."*

---

### B. 시험의 반증력 — 프로브 8건, **6건 살아 있고 2건이 비었다**

| 프로브 | 무엇을 뒤집었나 | 결과 |
|---|---|---|
| **P1′** | 조기 재시도의 **표적성** 제거(결함 실행만 → 전 실행) | ✅ `test_v1a` · `test_retry_budget_is_unchanged_by_the_split` 실패 |
| **P2** | **수렴 보류** 제거 | ✅ `test_v1c` · m17 ⓓ 실패 |
| **P3a′** | `_retry_budget` 의 **거부 2경로**를 기본값 1 로 대체 | ❌ **495 passed** — 무시험 |
| **P3b** | 러너가 조기 상한 +1 | ✅ 실패(단 B-3) |
| **P4** | 조기 관문 **행 순서** 뒤집기 | ✅ `test_v1d` 실패 |
| **P5** | `READ_CHECK_IDS` 에서 두 검사 제거(**출구 존치** 폐지) | ✅ `test_claim_check_phase_meanings…` 실패 |
| **P6** | **같은 서명 재현 → 즉시 상신** 제거 | ✅ `test_v6` 실패 |
| **P7b** | 조기 상한 1→2 + 조치 표에 **무관한** `retry(2)` 행 | ❌ Q7 후계 시험 **통과** |
| **P8** | 되먹임에 **상대 실행의 검사 소견** 동봉 | ❌ **18 passed** |
| **P8b** | 되먹임에 상대 실행의 **맹검 메모** 동봉 | ✅ 비누설 시험 실패(표지 팔은 살아 있다) |

**B-1(HIGH) — 「코드가 상한을 지어내지 않는다」가 무시험이다.** `read.py:756-772` 의 두 `raise RunnerContractError` 를 전부 `return 1` 로 바꿔도:

```
495 passed in 96.52s (0:01:36)
```

이 규율은 SPEC §1.4 가 *"계약이 그 판정점을 선언하지 않으면 러너는 기본값을 지어내지 않고 거부한다"* 로 적었고, 함수 docstring 이 `convergence.threshold-missing` 을 선례로 인용한다. **그 선례는 시험이 있다**(`tests/test_m1_reader.py:1450`). 이쪽은 없다. 재정이 명한 항목은 아니나, **문서가 있다고 말하는 강제가 실물에 없다** — M0.6 FAIL 사유의 형태다.

**B-2(MED) — 비누설 시험이 핵심 채널을 비껴간다.** P8 은 `claim_failures` 전건의 소견을 **모든** 재시도 실행에 방송하도록 바꾼 것인데 18건이 그대로 통과했다. 이유는 시험 표본에서 **상대(read-a)가 성하기 때문**이다 — 소견이 0건이라 방송해도 아무것도 늘지 않는다. `Finding.found` 는 위반 청구항의 `text_verbatim` 을 **200자까지** 싣는다(`reader/lib/report.py:26-30`). 즉 상대가 실패하는 순간 그 채널은 진짜 누설 통로가 되는데, 시험은 그 배치를 만들지 않는다. 표지 팔(P8b)은 살아 있으나 그것이 막는 것은 **맹검 메모**이고, 그 경로는 T16 이전에도 열려 있지 않았다.

**B-3(정밀) — `test_v3` 의 초과 단언은 도달 불능이다.** P3b 에서 실제로 터진 것은

```
engine.lanes.contract.LanePending: 레인 응답 미도착 1건: read-b/decompose/retry-2/batch-0
```

즉 `if len(attempts) > budgets["early"]` · `retry_two` 두 단언은 **하네스가 응답을 안 깔아서** 먼저 죽는 바람에 한 번도 평가되지 않는다. 시험은 실패하므로 반증력은 있으나, **실패 사유가 시험이 적은 사유가 아니다.** 같은 파일 `run_with_payloads` docstring 이 *"'러너가 발송하지 않았다'가 응답 부재에 떠밀린 결과가 아님을 증명한다"* 고 선언하는데, 초과 방향에서는 정확히 그 부재에 떠밀린다. (V-6 은 `attempts=(0,1,2)` 를 깔아 이 함정을 피했다 — 설계는 알고 있었다.)

---

### C. 조용한 동작 변화

**C-0 — `convergence_detail.attempt` 의 의미 변화는 소비자를 깨뜨리지 않는다. [확인]**

| 소비자 후보 | 실측 |
|---|---|
| 스키마 | `contracts/schemas/convergence.schema.json:330` = `{"type":"integer","minimum":0}` 뿐. `$comment` 에 의미 서술 **없음** → 낡을 문언이 없다 |
| 렌더 | `attempt` 를 읽는 렌더 코드 **0건**(`engine/`·`reader/` grep) |
| 다른 검사 | `convergence_detail` 을 읽는 검사 **0건** |
| 기존 런 산출물 | `runs/**/convergence*.json` 은 값만 들고 있고 재파싱 경로가 없다 |
| 문서 | `SPEC.md:1949` 예시(`"attempt": 1`) — 새 의미와도 정합 · 계약 `read.yaml:181-188` 이 개정됨 |

두 값 다 `>= 0` 정수라 계약도 만족한다. **소비자 파괴 없음.**

**C-0b — `tests/test_m2_read.py` 표본 교체는 단언을 약화시키지 않았다. 오히려 강화됐다. [확인]**
diff 상 바뀐 줄은 각 시험당 **payload 한 줄 + docstring** 뿐이고 단언은 한 자도 안 바뀌었다. 그리고 `outcome["rows"]` 가 2행 → 6행으로 늘었으므로

```python
if failing != ["read.convergence"]:
```

는 이제 **청구항 4행이 전부 통과했음**까지 함께 단언한다. 보고의 주장은 사실이다.

**그러나 — C-1(MED): 같은 표본이 남은 두 시험에서 조용히 뜻을 잃었다.**
`multiple-or` 표본은 두 시험에서 교체됐는데 **다른 두 곳에는 그대로 남았다**: `tests/test_m17_lanes.py:126` 과 `tests/test_m2_read.py:2528`, 둘 다 주석 `# exact-match 축을 가른다` 를 달고. 실측:

```
status = escalate
실패 행 = ['read.dependency-parse']
checks  = ['read.input-digest','read.claim-inventory','read.dependency-parse',
           'read.claim-inventory','read.dependency-parse']
convergence executed = False | attempt = 0
```

`test_convergence_runs_before_grounding` — 이름이 *convergence* 이고 docstring 이 *"수렴 미달인 런이 접지를 다 돌고 나서 멈춘다"* 인 시험이, 이제 **수렴을 한 번도 실행하지 않은 채** 통과한다. 대조군 팔(수렴 통과 → 접지 진행)은 살아 있으나 **음성 팔은 수렴을 재지 않는다.** 교체가 「깨진 곳만」 적용되고 「뜻이 바뀐 곳」은 지나쳤다.

**C-2(MED) — Owner '계속' 봉투의 적용 범위가 조용히 넓어졌다.** `read.py:1552-1556` 은 `envelope_ok` 면 `claim_failures` 가 있어도 후속으로 떨어진다. 실측:

```
2차(봉투 있음) status = escalate
  접지·통합 발송 = ['ground-dependent', 'ground-independent', 'synthesize']
```

체크포인트 이름은 여전히 `convergence_continue` 인데, 이제 **청구항 소유 실패**까지 통과시킨다. 완화 요인은 있다 — 봉투가 **청구항 실패 행이 실린 판정서의 지문**에 결속되므로 Owner 는 그 실패를 보고 서명한다. 그래도 T16 이 명한 확대가 아니고 **시험이 한 건도 없다**.

**C-3(LOW) — `repeated` 가 `read.schema` 의 `halt` 를 앞지른다.** `read.py:1752-1756` 에서 `if repeated:` 가 `if "read.schema" in ids:` **앞**에 선다. 계약은 `read.schema 실패 → retry(1) → halt` 인데, 같은 서명으로 두 번 실패하면 `escalate` 가 나간다. `halt`(런 상태 무효)와 `escalate`(정지 + 상신)는 다른 처분이다. T16 §6 ⑤ 는 우선순위를 정하지 않았다.

**C-4(정보) — `outcome["rows"]` 가 조기 실패 경로에서 2 → 6 행.** `engine/`·`tools/` 안에 이 키의 소비자는 **없다**(시험만 읽는다). 파괴 없음.

---

### D. Q7 이 지키려던 것 — **기계로 집행된다. 다만 가드가 세탁 가능하다.**

**집행은 실재한다.** 계약의 조기 상한만 1→2 로 올리면(P7):

```
Failed: 러너의 상한이 조치 표가 선언한 값 밖이다 — 코드가 예산을 늘렸거나 계약 두 곳이
갈렸다: early=2, 조치=[1]        ← tests/test_m17_lanes.py:204
```

즉 «계약 두 곳(`retry_budget.points[].max_retries` ↔ `failure[].action` 의 `retry(n)`) 의 일치» 는 실제로 잰다. **문서 주장뿐이 아니다.**

**D-1(MED) — 그러나 그 대조는 「집합 소속」이지 「판정점 대응」이 아니다.** 조치 표에 **아무 조건으로든** `retry(2)` 한 줄을 더하고 조기 상한을 2 로 올리면:

```
===== PROBE P7b =====
.                                                                        [100%]
1 passed in 1.07s          ← test_retry_budget_is_unchanged_by_the_split
```

Q7 후계로 지목된 바로 그 시험이 **예산 2배를 통과시킨다.** 전수 실행에서는 5건이 깨지지만(`490 passed`) 전부 `LanePending` — 즉 하네스가 `attempts=(0,1)` 만 깔아서 우연히 걸린 것이고, 붙잡은 것은 가드가 아니라 비계다. V-6 처럼 회차를 더 깔면 그 안전망은 사라진다.

**총량 자체는 늘었고, 그것은 재정이 승인한 것이다** — 구 전역 1회 → 조기 2(레인별 1×2) + 출구 1 = **최대 3**. `test_v3` 가 그 천장을 계약에서 도출해 잰다(`ceiling = len(READ_RUNS)*early + exit`). 몰래 늘어난 것이 아니다.

---

### E. 출구 행 존치가 지금 무엇을 잡는가 — **탐지로는 0 이다**

총괄의 정정(`D-20260901-01` §10)은 맞다. 그 크기를 재면 이렇다.

**실측 ①** — 두 검사는 `material_id` 를 읽지 않는다:
```
reader/lib/dependency_parse.py:0
reader/lib/inventory.py:0
reader/lib/spec_io.py: (SpecIndex 에도 0건)
```

**실측 ②** — `material_id` 를 지우고 비교하면 조기 claims 와 최종 claims 는 **완전히 같다**:
```
claims (material_id 제외) 동일 = True
early material_id = ['M1','M2','M3','M11']
full  material_id = ['M15','M3','M1','M2']      ← 실제로 갈리는 것은 이 필드뿐
```

두 검사의 판정은 `(claims − material_id, source_text, rules)` 의 함수이고, 세 입력이 전부 국면 간 불변이다. **⇒ 조기가 통과한 런에서 출구 행의 판정은 조기 행과 항상 같다. 오늘 그 행이 잡을 수 있는 것은 없다.** 「아무것도 잡지 않는다」가 답이다.

**그래도 출구 행이 하는 일은 셋 있다** — 탐지가 아니라 다른 격이다:

1. **기록** — 최종 판정서(`convergence.json`, CP1 표면)에 청구항 2행이 남는다. 지우면 CP1 이 그 두 검사의 판정을 못 본다.
2. **봉투 우회 경로의 재보고** — Owner '계속' 봉투로 조기 실패를 지나온 런에서 그 실패가 출구에 다시 서고 최종 처분을 만든다(C-2 참조 · 실측됨).
3. **미래 결합 대비** — 정정이 말한 「보험」. `assemble_spec` 이 뒷날 claims 문언을 건드리면 그때 잡는다. **오늘의 크기는 0 이고, 그것이 이 항목의 정확한 답이다.**

**E-2(LOW) — 반증된 전제가 정정 뒤에도 세 곳에 그대로 있다.** 정정은 `D-20260901-01` §10 한 곳에만 적혔고, 다음 셋은 「유일한 탐지기」/`material_id` 오염 서사를 **정정 포인터 없이** 그대로 든다:

- `reader/lib/run_checks.py:56-60` — **코드 주석**. *"…material_id 를 전량 재작성하고 … 그 오염은 분해 산출에 나타나지 않는다(재정 T16 §2 ⒜)"*
- `tests/test_m21_retry_budget_by_judgment_point.py:510` — *"국면 간 변이의 유일한 탐지기가 사라진다"*
- `docs/decisions/RULINGS-LEDGER.md:33` — 색인 행이 *"출구 행이 **유일한 탐지기**다"*

원장 원문(`ruling-20260901-07-T16.md`)은 고칠 수 없으니 그대로가 맞다. 위 셋은 원장 원문이 아니다.

---

### F. 놓친 결함

#### **X-1 (BLOCKER) — 조기 payload 의 중복 행이 `vacuous_pass` 를 깨뜨린다**

**뿌리**: `to_convergence_payload`(`reader/lib/run_checks.py:167-169`)가 `vacuous_pass` 를 `checks[]` 에서 **중복 제거 없이** 파생하는데, 스키마는 `uniqueItems: true` 다(`convergence.schema.json:41`). T16 이전에는 조기 payload 에 검사가 한 종류씩만 들어와 문제가 될 수 없었다.

**발화 조건**: 두 실행의 같은 검사가 **함께 공허**. `read.dependency-parse` 는 `checked` 를 **분류된 종속항만** 센다(`dependency_parse.py:143,176`) — 그 파일 자신이 *"전 종속항이 미분류면 checked == 0 이 되고 … **그것이 정상 동작이다**"* 라고 적었다.

- 종속항이 **없는** 특허 → 둘 다 공허 → 중단
- 종속항이 **전부 `unclassified`**(Markush·조건부·수단항·카테고리 전환 — 재정 P-1 이 명한 정상 사용) → 둘 다 공허 → 중단

**전 러너 재현**(같은 입력, 부모 커밋 대조):

```
########## PRE (ad5e471^) ##########
convergence-early.json exists = True
  phase        = early
  checks ids   = ['read.input-digest', 'read.convergence']
  vacuous_pass = []
########## POST (ad5e471) ##########
RAISED: RunnerContractError | early 수렴 보고서가 convergence/v0 를 위반한다
        (@vacuous_pass): ['read.dependency-parse','read.dependency-parse'] has non-unique elements
convergence-early.json exists = False
```

**회귀임이 확정됐다.** 부모에서는 조기 관문을 통과해 판정서를 냈고, 이 커밋에서는 **판정서도 못 내고** 예외로 죽는다.

#### **X-2 (BLOCKER) — 비정본의 `unclassified` ID 를 정본 명세에서 조회한다**

`to_convergence_payload:221-224` 가 `read.dependency-parse` 행을 만나면 `_unclassified_rows(source, …)` 를 부르는데, `source` 는 **정본 실행의 명세 하나**다. 이제 그 자리에 **비정본 실행의 행**도 온다. 정본에 없는 ID 는 `claim.get("text_verbatim", "")` → `""` → 스키마 `minLength: 1` 위반.

**전 러너 재현**(read-b 만 유령 종속항 `CL-9` 를 `unclassified` 로 선언):

```
########## PRE (ad5e471^) ##########
READ status = escalate
  unclassified_dependents = []
########## POST (ad5e471) ##########
RAISED: RunnerContractError | early 수렴 보고서가 convergence/v0 를 위반한다
        (@unclassified_dependents/0/text_verbatim): '' should be non-empty
```

**이것이 특히 나쁜 이유**: 이 시나리오는 T16 이 라우팅하려고 만든 **바로 그 결함 계열**(분해가 유령 종속항을 등재)이다. 그 결함에 표적 재시도를 주는 대신 러너가 죽는다. `'854` 는 이미 `unclassified` 1건을 들고 있고 두 실행이 **CL-9 에서 갈렸던** 특허다 — 재현에서 멀지 않다.

#### **X-3 (HIGH) — `unclassified_dependents` 의 실행 귀속이 조용히 틀린다**

X-2 와 같은 뿌리인데 **터지지 않고 틀린다.** `for row in rows:` 가 마지막 `read.dependency-parse` 행(= 비정본)으로 덮어쓴다:

```
정본이 미분류 1건을 신고, 비정본은 0건 → 보고서: []
비정본만 미분류 1건 → 보고서: [{'claim':'CL-3','dependency_type':'unclassified',
                              'text_verbatim':'정본 read-a 의 CL-3 문언'}]  ← 문언은 read-a 의 것
```

**정본의 미분류 신고가 지워지고**, 비정본의 ID 가 **정본의 문언을 달고** 실린다. 이 필드는 스키마 `$comment` 가 *"CP1 표면이 전건을 렌더한다 … 침묵을 막는 목록"* 이라 적은 자리다. 침묵을 막으라고 만든 칸이 조용히 틀린다.

**세 결함의 공통 뿌리 하나**: 「정의는 하나, 호출점은 둘」을 검사 실행 층에서는 옳게 구현했는데, **보고서 조립 층(`to_convergence_payload`)은 여전히 「검사 id 당 행 하나 · 명세 하나」를 전제**한다. 조기 payload 만 그 전제를 깼다.

#### **F-2 (LOW) — 커밋 메시지의 계수가 틀렸다**

```
PRE  collected: 484 tests collected     PRE  full: 484 passed
POST collected: 495 tests collected     POST full: 495 passed
신설 파일: 11 tests collected
```

메시지의 `495 passed(479 -> +16)` 에서 **기준선 479 와 증분 +16 이 둘 다 틀렸다**(실측 `484 → +11`). 신설 11건은 전부 새 파일에서 왔고 m17·m2 는 개정만 했다. B-3(백로그) 이 말하는 구조적 낡음의 새 실례다.

**관문은 주장대로다.** 네 도구 × plain/`-O` = 8회 전부 `EXIT=0`.

---

## 3. 직접 실행한 명령과 출력

전량은 위 §2 에 인용했다. 핵심만 다시 모은다.

```
$ cd /tmp/pd-audit-t16 && .venv/bin/python -m pytest tests/ -q
495 passed in 86.41s (0:01:26)                                   ← 기준선

$ 프로브 P3a′ (_retry_budget 의 거부 2경로 → return 1)
495 passed in 96.52s (0:01:36)                                   ← 무시험 확정

$ 프로브 P8 (되먹임에 상대 실행 소견 동봉)
18 passed in 6.74s                                               ← 비누설 시험 공백

$ 프로브 P7b (조기 상한 2 + 무관한 retry(2) 행)
1 passed in 1.07s   (test_retry_budget_is_unchanged_by_the_split)

$ 관문 4종 × plain/-O
check_spec_refs plain EXIT=0 / -O EXIT=0
check_schema_enforcement plain EXIT=0 / -O EXIT=0
check_validator_enforcement plain EXIT=0 / -O EXIT=0
check_lane_binding plain EXIT=0 / -O EXIT=0
```

**격리 사본 규격** — 발주문이 *"(사본에서)"* 로 명시 허가했으나 SPEC §8.3 9항 ⓐ 는 사본을 **발주자가** 만들게 한다. 그 요건은 지켜지지 않았다: 사본과 마커를 **감수자가 직접 만들었다**. 숨기지 않고 적는다.

```
$ git clone --no-hardlinks /home/laptop/projects/patent-docent /tmp/pd-audit-t16   # 규격 ①
$ git checkout ad5e471 && cat .audit-sandbox                                        # 규격 ④(감수자 작성)
path=/tmp/pd-audit-t16
pin=ad5e471ee53f2146fd8d408a22dc488509200349
order=audit-T16-opus-max
disposable=true
$ realpath /tmp/pd-audit-t16   →  /tmp/pd-audit-t16          (2) 일치
$ git rev-parse HEAD           →  ad5e471…0349               (3) 일치
```
부모 대조용 두 번째 사본 = `/tmp/pd-audit-t16-pre`(`ad5e471^ = 9e4cdee`).

---

## 4. 원상 복구 증명

```
$ cd /tmp/pd-audit-t16 && git checkout -- . && git status --porcelain
?? .audit-sandbox                      ← 감수자가 만든 마커(추적 밖) 외 변경 0

$ diff BASELINE.sha256 AFTER.sha256 && echo "SHA256 IDENTICAL"
SHA256 IDENTICAL — 원상 복구 확인
88a2c083f5f0a62000f32235939fdacf0df8879ba0427ee21ddc7752cfec6a2b  engine/stages/read.py
01cefbd0ffd40c288a51f7f2b02761abba77b24d5705ed4b5a337e0477b5aa91  reader/lib/run_checks.py
05cf6f3e4d48655713da7e481d6bc4d9c12e69f105cbc9883280ab3e6c6e5577  reader/lib/__init__.py
04500646b3fff5569282a392a69bb11da6e9cd9f64ec2c054e767a44e0dbc567  contracts/stages/read.yaml
9ddaa084c0da9656d10f3c8f865f8d5ee152c42887337b75dc930c26c70ff11e  tests/test_m17_lanes.py
34cf0a4d60cd0de43df17e9ccd9972826b5eeebbd3010bbc64bbb41c20e94c2b  tests/test_m2_read.py
6fdf663279a6afdbacec6776dee126a72a60b852c0e5a601807f244f48104580  tests/test_m21_retry_budget_by_judgment_point.py
```

**정본**(`/home/laptop/projects/patent-docent`)은 감사 내내 무변경이며, 7파일 전부 `ad5e471` blob 과 해시 동일이다:

```
$ git status --porcelain     →  (빈 출력)
$ 작업본 sha256 ↔ git show ad5e471:<path> sha256
OK  engine/stages/read.py … OK  tests/test_m21_retry_budget_by_judgment_point.py   (7/7 OK)
```

`git add`·커밋·push 는 하지 않았다. 정본에서 실행한 명령은 `git`·`grep`·`sed -n`·`ls` 읽기뿐이다(pytest 도 정본에서 돌리지 않았다 — `.pytest_cache`·`__pycache__` 를 남기지 않기 위해).

---

## 5. 숨기지 않는 것

1. **X-1·X-2 의 처분을 제안하지 않았다.** 뿌리는 `to_convergence_payload` 의 「검사 id 당 행 하나 · 명세 하나」 전제이고, 그것을 어떻게 풀지(행에 `read_run` 을 붙일지 · 조기 payload 를 실행별로 나눌지 · `vacuous_pass` 를 dedupe 할지)는 **판정 서식 `verdict-check-row/v0` 의 값 공간에 닿는다** — 규율 11 상 재정 사항으로 보인다. 감수자가 고를 자리가 아니다.
2. **실특허 2건에서는 X-1 이 발화하지 않는다.** 실측: `'854` = `dependency-parse checked=16 vacuous='none'`, `WO2026128750A1` = `checked=24 vacuous='none'`. 다만 `'854` 는 `unclassified` 1건을 들고 있어 **X-2·X-3 쪽에는 가깝다**. T6 이 지목한 `WO2026128750A1` READ 부분 시험에서 이 자리가 어떻게 되는지는 **[미검증]** — 원천 청구항의 미분류 분포를 열어 보지 않았다.
3. **`test_v4`('854 무회귀)의 반증력을 뒤집어 보지 않았다.** §2 E 의 실측(claims 가 `material_id` 외 완전 동일)에 비추면 이 시험은 **오늘 어떤 입력으로도 실패할 수 없다** — 그것이 무회귀 시험의 성질이므로 결함으로 세지 않았으나, 「반증하는가」의 답은 엄밀히 *"미래의 조립기 변경에 대해서만"* 이다.
4. **`escalate_on_repeat.signature` 의 설계 선택(`found` 제외)을 반증하지 않았다.** 서명에 값을 넣지 않는 근거(*"항목 ID 재번호가 회차마다 다른 값을 낸다"*)는 그럴듯하나, 그 결과 **다른 원인의 같은 좌표 실패**가 「재현」으로 오분류될 수 있는지는 재지 않았다. **[미검증]**
5. **`docs/SPEC.md` 개정분의 전 문장을 실물과 대조하지는 않았다.** §1.4·§1.16·§8.4 의 신설·개정 블록은 읽었고 A-1 을 그 대조에서 찾았으나, `check_spec_refs.py` 가 잡지 않는 산문 층 전수는 보지 않았다.
6. **레인 로그·요청 지문 층은 이 감사의 범위 밖으로 두었다.** `check_lane_binding` 7시나리오가 exit 0 인 것만 확인했고, 조기 재시도가 늘린 왕복이 P-12 결속에 미치는 영향은 별도로 재지 않았다. **[미검증]**
7. **시간·범위상 프로브는 9건에서 멈췄다.** 특히 `_execute_canonical_tail` 의 `tail_defects` 되먹임 내용과 `id_maps` 누적이 재시도 회차 간에 어떻게 겹치는지는 열어 보지 않았다.
