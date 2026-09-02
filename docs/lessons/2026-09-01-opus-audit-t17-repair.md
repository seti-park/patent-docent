# 독립 감수 원문 — G-6 지적 처분 + 재정 T17 집행 (`39286ca`) · 판정 FAIL

## ★ 총괄 머리말 (2026-09-02 · 이 절은 총괄 저작이며 감수자·자문가가 쓴 절이 아니다)

지적 열거 = Y-1, Y-2, Y-3, Y-4, Y-5, Y-6, S-1, S-2
`Y-*` 는 아래 감사 원문 §3 신규 지적표가 붙인 것이다. §2 의 13건은 **직전 감사(`2026-09-01-opus-audit-g6-implementation.md`)의 지적에 대한 닫힘 판정**이라 그 파일의 열거에 서고 이 파일에 다시 서지 않는다. §4 Q2 의 판정 3건(총괄 자기 계상에 대한 감사자의 채점)과 §6 소견 3건에는 원문이 id 를 붙이지 않아 이 열거에 들지 않는다 — 소견 ⑶ 의 잔여는 `Y-5` 로 이미 서 있고, 소견 ⑵(규율 10 의 판별선)는 재정 T20 으로 닫혔으며, 소견 ⑴(역프로브가 정본 트리를 공유하는 방식)은 처분 기록을 찾지 못했다. 뒤의 둘은 `docs/decisions/DISPOSITIONS.md` §2 처분 대기에 적혀 있다.
**[추기 2026-09-02 · 총괄 저작]** 위 문단의 마지막 문장은 라운드 C 반입 시점의 것이다. 병합 뒤 총괄이 §6 소견 ⑴·⑵ 에 id **`S-1`·`S-2`** 를 세웠다(원문에 없는 id — Owner 사후 확인 대상) — `S-1` 의 처분(수용 · 발주문 골격 ⑼ 격리 사본)은 `docs/decisions/D-20260902-03-round-c.md` §3 이 처음 적고, `S-2` 는 재정 T20 으로 이미 닫혀 있던 것에 id 만 붙였다. 두 행은 `DISPOSITIONS.md` §1 에 있다.
이 절은 재정 T27 의 소급 등재로 2026-09-02 에 삽입되었다. 아래 제목 줄부터는 반입 당시(2026-09-01)의 문면 그대로다.

## 반입 당시의 문면 — 이하 원 파일 그대로 (이 제목 줄 한 줄만 2026-09-02 총괄 삽입 · 저자 경계는 원 파일의 표기를 따른다)

**규율 10 의 이행 — 전문 보존.** 좌석 = **opus max**(교차 벤더: 저작이 sol-coder 였다).
발주문 = 총괄 · 읽기 전용 준수는 총괄이 트리 지문으로 확인(`132eaed8339d2e3c` 감사 전후 동일 · `git status` 0행).

---

# 감사 판정 — G-6 지적 처분 + T17 집행(`39286ca`) · 좌석 opus max

## 1. 판정

**`FAIL`**

지적 13건 중 **11건은 실제로 닫혔다** — 반증 프로브 11종을 전부 돌렸고 구현을 뒤집으면 시험이 빨개진다. T17 집행 조건 ①③④ 도 실증됐고, 소급 없음도 실물 판정서로 확인했다. 이 라운드는 대체로 성공했다.

그런데 **X-2 의 수리가 같은 계열의 세 번째 중단을 새로 열었다.** `unclassified` 종속항의 `text_verbatim` 이 **빈 문자열이거나 없으면** 조기 판정서가 `convergence/v0` 를 위반해 `RunnerContractError` 로 죽는다 — X-1·X-2 와 **완전히 같은 증상**(판정서가 아예 안 쓰인다 → 봉투가 결속할 대상도 사라진다). 그리고 그중 둘은 **직전 커밋에서는 완주하던 입력**이다.

```
########## PRE (ad6d379) ##########          ########## POST (39286ca) ##########
who=read-a  RUN OK status=escalate           who=read-a  RAISED: RunnerContractError
            early exists=True                            (@unclassified_dependents/0/text_verbatim):
who=read-b  RUN OK status=escalate                       '' should be non-empty
            early exists=True                who=read-b  RAISED: 같은 예외
```

직전 라운드가 FAIL 을 받은 사유는 「명령된 것의 부재」가 아니라 「명령되지 않은 부작용」이었다. **같은 양식이 반복됐고, 이번에는 수리 자체가 그 부작용의 원인이다** — X-2 의 오귀속과 X-3 의 덮어쓰기가 각각 이 계열을 **가리고 있었고**, 둘을 고치자 가려져 있던 것이 드러났다.

| id | 격 | 무엇 |
|---|---|---|
| **Y-1** | **BLOCKER** | `unclassified` + 빈/부재 `text_verbatim` → 조기 판정서 미기입 · 런 중단. **PRE 통과 → POST 중단**(2변형) + X-2 잔여(1변형) |
| **Y-2** | MED | T17 집행 조건 **②(역반증)가 실제로는 충족되지 않았다.** 시험이 상신 축만 돌아 「좁힘이 과했는가」를 구조적으로 못 드러낸다. 커밋 메시지는 통과했다고 적었다 |
| **Y-3** | MED | 같은 커밋이 A-2/A-3 를 처분하면서 **새 무결속 선언 블록을 하나 더 만들었다** — `verdict_artifact_keys` 9키 무대조 · 코드 `blocked_by` 어휘 5종 중 3종이 계약에 없다 |
| **Y-4** | LOW | `PHASE_GATE_NO_VERDICT` 분기는 **도달 불능**(`engine/stages/read.py:1600-1601`) |
| **Y-5** | LOW | E-2 정정이 **한 곳 더 남았고 그 자리는 자문 원문이 아니라 총괄 자신의 추기다**(§5 ⑵·⑶) |
| **Y-6** | LOW | 조기 판정서는 CP1 표면인데 합집합 목록이 같은 청구항을 두 행으로 싣고 **어느 실행인지 말하지 않는다** |

---

## 2. 13건의 닫힘 판정

프로브는 전부 격리 사본에서 「구현을 뒤집고 → 시험을 돌리고 → `git checkout -- .` 으로 되돌리고 → 더러움 0 확인」의 4단이다.

| id | 판정 | 근거 (좌표 · 재현) |
|---|---|---|
| **X-1** | **closed** | 전 러너 재현: 두 실행 공허(`payload_set(dependency_type="unclassified")` ×2) → PRE `RAISED … has non-unique elements` / POST `vacuous_pass=['read.dependency-parse']` 1건, 판정서 기입. 프로브 **P-D**(`run_checks.py:174` dedupe 제거) → `test_both_runs_vacuous_dependency_parse_still_writes_the_verdict` 실패 |
| **X-2** | **partially-closed** | 명명된 시나리오(유령 ID 가 정본에 없음)는 닫혔다 — PRE `RAISED` / POST `RUN OK`. 프로브 **P-F**(`dependency_parse.py:167` 을 `""` 로) → 3건 실패. **그러나 뿌리는 안 닫혔다** = **Y-1** |
| **X-3** | **closed** | 프로브 **P-E**(합집합 → 덮어쓰기 복원) → `test_canonical_unclassified_report_is_not_overwritten_by_the_peer` 실패(`정본 read-a가 신고한 CL-3 기대 목록에 남음, 실제 []`) |
| **B-1** | **closed** | 프로브 **P-A**(`_retry_budget` 의 `raise` 2경로 → `return 1`) → `2 failed`. 직전 라운드에 **495 전건 통과**하던 자리다 |
| **A-1** | **closed** | 계약이 `phases: [early, exit]` 로 교정됐고(`read.yaml:587`), 시험이 상수 재기입 대신 **계약↔계약↔코드 등재부**를 대조한다. 프로브 **P-I**(다시 `[exit]`) → `checks_before_exit early 집합과 early_phase_spec.judged_here 가 갈렸다` 로 실패. *잔여(경미)*: `judged_here == set(EARLY_CLAIM_CHECK_IDS) \| {"read.convergence"}` 에서 뒤 항은 여전히 리터럴이다 |
| **C-1** | **closed** | 프로브 **P-J2**(`test_m2_read.py:2529` 표본을 구 `multiple-or` 로 복원) → `수렴 미달 표본에서 수렴이 실제로 돌지 않았다: {'executed': False …}` 로 실패. m17:126 은 표본을 안 바꾸고 주석만 고쳤는데 **그 시험은 분해 재시도를 원하므로 옳다** |
| **C-2** | **closed**(재정 T17 로) | §4 참조 |
| **B-2** | **closed** | 프로브 **P-K**(되먹임에 상대 실행 소견 방송) → `read-a 재시도 요청서에 read-b 검사 소견 표지가 누설됐다`. 직전 라운드의 P8 이 통과했던 공백(상대가 성해서 소견 0건)을 **두 실행이 함께 실패하는 표본**으로 메웠다 |
| **D-1** | **closed** | 프로브 **P-B**(무관한 `retry(2)` 행) → `points 신고가 없다` · 프로브 **P-B2**(그 행에 `points:[early]` 를 달아 정합 세탁 시도) → `early 기대=[2], 조치=[1, 2]`. 직전 라운드에 `1 passed` 로 세탁되던 자리다 |
| **C-3** | **closed(확대 집행)** | 프로브 **P-C**(`repeated` 를 다시 앞으로) → **2 failed**. 감사는 `read.schema` 하나를 지목했으나 `read.source-digest` 도 같은 자리였고 함께 고쳤다 — **확대가 옳다**(계약이 halt 를 정한 행이 계열이었다) |
| **A-2/A-3** | **closed** | `placeholders` 를 `assembler_inputs`/`spec_fields` 로 갈랐고 시험이 `inspect.signature(assemble_spec)` 와 대조한다. `binding_status` 는 **분류가 실키 집합과 정확히 같아야** 통과한다(누락·유령 둘 다 실패). `scope`·`repairs`·`checks` 가 실제로 행동에 결속됐다. **다만 같은 격의 새 구멍을 열었다 = Y-3** |
| **E-2** | **partially-closed** | 지목된 셋 전부 정정 확인 — `run_checks.py:55-63`(구 근거(반증됨) 명기) · `test_m21:571`(docstring 교체) · `RULINGS-LEDGER.md:34`(정정 포인터 삽입). 원장 원문 2곳은 옳게 무접촉. **잔존 1곳 = Y-5** |
| **F-2** | **closed** | 이 커밋 메시지에 시험 계수가 없다. 실측 **509 passed**(plain · `-O` 양쪽) |

---

## 3. 신규 지적

### **Y-1 (BLOCKER) — `unclassified` 의 빈 문언이 조기 판정서를 못 쓰게 한다**

**뿌리.** `reader/lib/dependency_parse.py:163-170` 이 미분류 항목을 `unclassified_detail` 에 넣을 때 `dependent.get("text_verbatim") or ""` 를 쓴다. 그 값이 `""` 면 `run_checks.py:231-238` 이 그대로 `unclassified_dependents` 에 싣고, 계약이 `minLength: 1` 로 거부한다(`convergence.schema.json`). 조기 국면에는 `read.schema` 가 없으므로(`phases: [exit]`) **아무것도 먼저 막지 못한다.** `text_verbatim` 이 아예 **없어도** 같다.

**재현 3변형**(전부 실제 러너 `run_read_stage`):

```
① read-a(정본)가 CL-3 을 unclassified + text_verbatim="" 로 신고
   PRE  ad6d379 → RUN OK  status=escalate · early exists=True · unclassified_dependents=[]
   POST 39286ca → RAISED RunnerContractError (@unclassified_dependents/0/text_verbatim)
② read-b(비정본)가 CL-3 을 같은 형태로 신고
   PRE  ad6d379 → RUN OK  status=escalate · early exists=True
   POST 39286ca → RAISED (같은 예외)
③ read-b 가 유령 CL-9 를 unclassified + text_verbatim="" 로 신고
   PRE  = POST = RAISED     ← 회귀가 아니라 X-2 의 잔여
```

**왜 결함인가.** ①② 는 **회귀**다 — 직전 커밋에서 완주하던 입력이 이제 예외로 죽는다. PRE 가 옳았다는 뜻이 아니다: ① 은 X-3 의 덮어쓰기가, ② 는 X-2 의 정본 조회가 각각 빈 문언을 **가리고 있었다**. 두 가림막을 걷자 뿌리가 드러났고, 직전 감사의 격 눈금으로는 **HIGH(조용히 틀림) → BLOCKER(런 중단)** 로 한 칸 나빠졌다.

③ 이 특히 나쁜 이유는 **X-2 가 라우팅하려던 바로 그 결함의 가장 자연스러운 형태**이기 때문이다. 레인이 유령 종속항을 지어내면 그것에 실을 원문이 없고, 그때 나오는 값이 `""` 이거나 키 부재다. 수리 주석은 *"명세를 아는 자리가 문언도 읽는다"* 라고 적었지만, **그 자리가 읽을 것이 없을 때**를 처리하지 않았다.

**발화 범위(숨기지 않는다).** 리포의 실특허 3런은 전부 안전하다 — `dependents` 의 최소 `text_verbatim` 길이가 WO 106 B · `'854` 141 B 이고, `'854` 의 유일한 미분류 CL-9 는 194 B 다. **WO 는 미분류 0건이므로 T6 의 READ 부분 시험은 이 자리를 건드리지 않는다.** 즉 이것은 레인 오작동 경로다 — 그런데 조기 국면의 존재 이유가 정확히 레인 오작동의 조기 포착이고, 직전 감사도 X-1 을 *"실특허 2건에서는 발화하지 않는다"* 고 적으면서 BLOCKER 로 매겼다. 같은 눈금을 쓴다.

**처분은 제안하지 않는다.** 「빈 문언을 어떻게 실을 것인가」는 `convergence/v0` 의 `minLength: 1` 을 건드리거나 목록에서 항목을 빼는 일이고, 둘 다 **판정서 서식의 값 공간**이다 — 규율 11 상 재정 사항으로 보인다. 직전 감사가 X-1·X-2 에 대해 같은 이유로 처분을 유보한 것과 같은 자리다.

### **Y-2 (MED) — T17 조건 ②(역반증)가 충족되지 않았다**

**좌표** = `tests/test_m22_continue_envelope_scope.py:88-118` · 커밋 메시지 *"과잉 여부를 재는 자리가 조건 ② 이고 통과했다"*.

T17 §3 ② 의 문언은 **"같은 봉투로 「수렴 미달」은 여전히 통과함을 보인다"** 다. 이 리포에서 「수렴 미달」은 두 축을 덮는 우산어다(계약 실패표가 `exact-match 축 미달` 과 `상신 축 미달` 을 따로 적어 구별한다). 그런데 역반증 시험은 **상신 축 하나만** 돌린다. exact-match 축의 실측은 이렇다:

```
프로브: read-b 가 CLAIM_3 끝점만 가른다 → dependent-set 0.95 미달(exact-match, fail)
        1차 실행 후 유효 봉투 발행 → 2차 실행
PRE  ad6d379 : grounding lanes dispatched = ['ground-independent','ground-dependent','synthesize', ×2]
POST 39286ca : grounding lanes dispatched = []
```

**즉 「수렴 미달」의 절반은 더 이상 통과하지 않는다.** 조건 ② 는 좁힘이 과했는지를 드러내라고 만든 자리인데, 시험이 그 절반을 아예 돌지 않으므로 **구조적으로 드러낼 수 없다** — 자기가 정한 범위를 자기가 확인하는 순환이다. 프로브 **P-H2**(게이트를 공집합 판정으로) 로 확인하면 그 시험은 **상신 축이 막혔을 때만** 빨개진다.

부수 관찰: `PHASE_GATE_ESCALATION = ENVELOPE_SCOPE[0]`(`read.py:131`)이라 **상신 축은 정의상 항상 범위 안**이다. 단일 진원으로는 좋은 형태지만, 그 결과 조건 ② 는 「과잉」 방향에서 위반 자체가 표현 불가능해진다.

### **Y-3 (MED) — A-2/A-3 를 처분한 커밋이 같은 격의 새 무결속 선언을 만들었다**

**좌표** = `contracts/stages/read.yaml:428-441`(`verdict_artifact_keys` 9키) · `engine/stages/read.py:124-130`(`blocked_by` 어휘 5종).

- `verdict_artifact_keys` 를 읽는 코드·시험 **0건**(`grep -rn "verdict_artifact_keys" --include=*.py` → 무매치). 지금은 9키가 실물과 정확히 일치하지만 **그 일치를 유지시키는 기제가 없다.**
- 코드가 발행하는 `blocked_by` 값은 `none`·`claim-checks`·`no-verdict`·`convergence-exact-match`·`convergence-escalation` 5종인데, 계약이 드는 것은 `applies_to`/`not_applies_to` 의 **3종뿐**이다. `none`·`no-verdict` 는 계약 어디에도 없다.
- 새 산출물 `10-read/phase-gate.json` 에 스키마가 없다(`contracts/schemas/` 4파일 무변경).

**왜 결함인가.** 이 커밋은 `binding_status` 를 신설하고 *"읽히지 않는 선언을 읽히는 것처럼 두지 않는다"* 를 시험으로 강제했다(`test_retry_contract_declarations_are_bound_or_classified` — 분류가 실키 집합과 **정확히 상등**이어야 한다). **그 강제의 적용 범위가 `retry_budget` 과 `early_phase_spec` 두 블록으로 한정되어 있어, 같은 파일에 새로 생긴 `phase_gates[].verdict_artifact_keys` 는 그물 밖이다.** 이 리포 자신의 문언: *"두 벌이 생기면 한 벌은 반드시 낡는다."*

**경감 요인** — 경로 자체는 계약 결속이다. `paths.phase_gate_json` 이 `self.path("phase-gate.json")` 를 쓰므로 계약 `outputs` 에서 선언이 빠지면 `PathContractError` 가 난다(코드 리터럴 경로가 아니다). 결속이 없는 것은 **내용 형태**다.

### **Y-4 (LOW) — 도달 불능 분기**

`engine/stages/read.py:1600-1601` 의 `elif early_row is None: blocked_by = PHASE_GATE_NO_VERDICT`. 루프 불변식상 `claim_failures` 가 비면 `early_row` 는 반드시 설정되고(`read.py:1524-1531`, `early_convergence_row` 는 `CheckRow` 를 반환하며 `None` 을 낼 수 없다 — `read.py:1006-1014`), 비지 않으면 첫 분기가 먹는다. 라벨 `no-verdict` 와 그 사유 문자열(`read.py:1078`)은 **어떤 런에서도 발행되지 않는다.**

### **Y-6 (LOW) — CP1 표면의 무귀속 이중 행**

`convergence-early.json` 은 CP1 표면이다(`read.yaml#owner_checkpoint.surfaces`). 합집합 뒤 두 실행이 같은 청구항을 **다른 문언으로** 신고하면 그 목록에 같은 `claim` 이 두 행 선다. 스키마가 `additionalProperties: false` 라 실행 귀속 필드를 붙일 수 없으므로 **Owner 는 어느 행이 정본인지 알 수 없다.** 손실보다는 낫고 계약 제약이 원인이지만, CP1 상신 때 그 사실을 고지하지 않으면 재정 T14 가 명한 「감수하고 넘어가는 것의 명기」와 같은 자리가 빈다.

---

## 4. Q2 — 총괄 자기 계상 3건의 판정

### ① 봉투 범위에서 `exact-match` 축도 함께 뺀 것 → **결과는 적정 · 절차는 과함 · 근거 하나는 거짓**

**결과가 적정한 이유.** T17 ⒝ 가 세운 판별선은 「고칠 수 있는 레인이 있는가」다. exact-match 축 미달에는 **조기 수렴 재시도 레인이 있다**(`read.py:1568-1580` — 양쪽에 같은 소견을 보내 재분해). 상신 축 미달에는 없다(판정 행을 `fail` 로 만들지 않으므로 재시도가 발화하지 않는다). **그 선을 그대로 적용하면 exact-match 는 범위 밖이 맞다.** ⒜ 의 문언 *"상신 축 미달에만"* 도 배타형이다.

**절차가 과한 이유.** 원장 문건이 **세 자리에서 서로 다르게** 적혀 있다:

| 자리 | 문언 |
|---|---|
| 제목 | *"'계속' 봉투의 적용 범위를 **수렴 미달**로 좁힌다"* |
| §0 (Owner 가 채택한 ⓐ 의 문언) | *"봉투를 **수렴 미달**에만 적용하도록 좁힌다 — **청구항 실패**는 봉투로 못 넘긴다"* |
| §2 ⒜ (발주자 원안) | *"조기 수렴 판정의 **상신 축 미달**에만 적용한다"* |

**Owner 육성은 `(a)` 한 글자이고 그 `(a)` 가 가리키는 문언은 청구항 실패만 배제한다.** exact-match 배제는 §2 ⒜ 에서 처음 등장하며 그 절은 `text_status: 혼합` 이 밝힌 대로 **발주자 원안**이다. 집행자는 이 두 번째 축소를 **인지했고**(커밋 메시지가 *"청구항 실패 밖의 두 번째 축소"* 라고 직접 적는다) 그럼에도 상신하지 않았다. 규율 11 의 판별선(*"그 판단이 검사의 판정 공간을 바꾸는가"*)에 정면으로 걸리고, CLAUDE.md ★ 절이 H5·H6 사례로 성문화한 형태와 같다 — **되돌리기가 싸다는 것도, 상위 문언이 그럴듯하게 읽힌다는 것도 면제가 아니다.** 효력은 사후에 줄 수 있으나 절차는 사후에 만들 수 없다.

**근거 하나가 거짓인 이유** = Y-2. 「과잉 여부는 조건 ② 가 쟀다」는 주장은 성립하지 않는다.

**실무 귀결(Owner 가 알아야 할 것).** 좁힘 뒤 exact-match 조기 실패에는 **Owner 가 진행시킬 수단이 남아 있지 않다.** 예산 소진 → `escalate` 이고, 봉투는 안 먹으며, 남는 길은 소재 변경·절차 수정·새 런뿐이다. 그것이 의도한 설계인지 아닌지는 재정 사항이라 감수자가 정할 자리가 아니다.

### ② 사유를 `10-read/phase-gate.json` 으로 뺀 것 → **사유는 성립(실증함) · 스키마 부재는 모자람**

**사유를 반증 시도했고 실패했다 — 즉 사유가 옳다.** 프로브 **P-L**: 게이트 판정을 `convergence-early.json` 에 실어 다시 쓰게 하면

```
Failed: 상신 축의 유효 봉투 기대 ground-independent 발송, 실제 ['decompose','decompose']
```

**봉투가 실제로 실효된다.** 봉투는 판정서 파일의 SHA-256 에 결속되는데(`read.yaml#phase_gates[].envelope_binding`) 게이트 판정은 봉투를 읽은 **뒤에** 정해지므로, 그것을 같은 파일에 쓰면 봉투 발행 전후로 지문이 갈린다. 분리는 필수다. **파일 분리 판단 = 적정.**

**스키마·형태 결속의 부재 = 모자람** — Y-3.

### ③ `unclassified_dependents` 합집합 + 3튜플 dedupe → **적정**

정보를 지우지 않고, 정본 행이 먼저 서고, 같은 신고는 한 행으로 접힌다. `dependency_type` 이 `const: "unclassified"` 라 실질 키는 `(claim, text)` 이고 그것이 옳은 동일성이다. 실행 귀속을 못 붙이는 것은 스키마 `additionalProperties: false` 라는 **계약 제약**이지 설계 태만이 아니며, 붙이려면 재정이 필요하다. 잔여 = Y-6(고지 의무).

---

## 5. Q3 — T17 집행 조건 4종

| 조건 | 판정 | 근거 |
|---|---|---|
| ① 반증 | **충족** | 프로브 **P-G**(`envelope_in_scope = True` 로 원복) → `test_envelope_does_not_carry_an_early_claim_failure` · `test_phase_gate_records_why_the_envelope_did_not_apply` 2건 실패. 유효 봉투 + 청구항 실패에서 접지 레인 **0건** 실측 |
| ② 역반증 | **불충족** | **Y-2.** 상신 축만 잰다 — exact-match 축은 PRE 통과 → POST 차단인데 시험이 없다 |
| ③ 판정문에 사유 | **충족** | `phase-gate.json.reason` 이 차단 사유·재정 근거·처분을 문장으로 싣고 `outcome["gate_note"]` 가 같은 문자열이다. 실측: *"조기 수렴 exact-match 축 미달이 접지 진입을 막았다. 재정 2026-09-01 T17에 따라 … 처분: 조기 수렴 재시도 — 예산 소진 시 계약 실패표(escalate). 계속 봉투 유효(판정서 지문 결속 확인)"* — **봉투가 유효하다는 사실까지 함께 적어** *"봉투가 있는데 왜 안 되나"* 를 코드로 되짚지 않게 한다 |
| ④ 전수 + 관문 | **충족** | `509 passed` (plain 169s · `PYTHONOPTIMIZE=1` + `-O` 194s, 양쪽 동일). 관문 4종 × plain/`-O` = **8회 전부 EXIT=0** |
| **★ 소급하지 않음** | **충족** | WO 런 판정서 실물 대조: `read.convergence` 행 **status = pass**, 미달 축은 `tree-edges` **하나**이고 정책은 `escalation-trigger`. exact-match 3축(`independent-count`·`dependent-count`·`dependent-set`)은 전부 pass. **좁힘 뒤에도 그 봉투는 범위 안이며 동결본 v1 은 그대로 선다.** 커밋이 `runs/` 를 한 바이트도 건드리지 않았다 |

---

## 6. §3 — 소견 3건

### ⑴ 레인이 리포에서 `git apply -R` 로 역프로브를 도는 방식 — **안전하지 않다. 22초 과도 상태는 원인이 아니라 증상이다.**

미커밋 수리와 프로브 패치가 **같은 트리를 공유**하면 세 가지가 동시에 열린다.

1. **되돌리기가 수리까지 지운다.** `git checkout -- .` 은 프로브 패치와 미커밋 수리를 구별하지 못한다. 이번에 감독이 본 「수리 영구 소실」은 오판이었지만, **같은 트리에서는 그것이 언제든 진짜가 될 수 있다** — 감독의 경보는 잘못된 전제 위에서 옳은 방향을 가리켰다.
2. **관찰자가 진실을 말할 수 없다.** `git status` 한 장으로는 「프로브 중」과 「수리 유실」이 같은 모양이다. 그래서 22초를 60초로 늘려도 답이 안 나온다 — 관측 창의 문제가 아니라 **상태 공간이 겹친 문제**다.
3. **프로브가 죽으면 트리가 패치된 채 남는다.** 그 위에서 커밋이 나면 2026-07-26 오염 트리 사고와 같은 계열이다(사용자 전역 규약 ③ 이 `git add -A` 를 금지한 근거).

**권고.** 프로브 레인에 **정본 트리 쓰기 권한을 주지 않는다.** `git worktree add` 또는 `git clone --no-hardlinks` 로 별도 트리를 받고 거기서만 패치·되돌림을 한다 — 이번 감사가 그렇게 했고(격리 클론 3벌), 되돌림 실패가 정본에 닿을 경로 자체가 없다. 이것은 SPEC §8.3 9항 ⓐ 가 **감수 레인**에 이미 요구하는 규격이며, 그 규격이 감수에 필요한 이유는 역프로브에도 그대로 적용된다. 「검사자에게 쓰기를 주면 격리 사본에서만」이라는 재정 Q9 ⓐ 의 논리와 같다.

### ⑵ 규율 10 — **이 건은 규율 10 사안이 아니다. 판별을 「파일 단위」로 해서 답이 갈렸다.**

문제의 문장이 어디 있는지가 결정적이다.

```
docs/lessons/2026-09-01-fable-advice-g6-defect-ownership.md:69
  "⇒ 자문이 옳다. 총괄의 (a) 순수형은 그 계열의 유일한 탐지기를 없앨 뻔했다."
```

이 줄은 **자문의 말이 아니다.** 그 파일의 마지막 절은 `## ★ 총괄의 독립 확인 (2026-09-01 · 추기)` 이고, 그 절은 **파일 생성 커밋 `10f86a7` 부터 총괄이 직접 쓴 것**이다. 「유일한 탐지기」라는 표현은 자문 본문 어디에도 없다 — 자문은 *"탐지조차 안 되는 결함으로 격하된다"* 라고 썼고, 그것을 「유일한 탐지기」로 요약해 재정 T16 §2 ⒜ 로 올린 것이 총괄이다.

**규율 10(재정 N7)이 보호하는 것은 「감수 산출」이다.** 총괄이 같은 파일에 붙인 자기 추기는 감수 산출이 아니다. 따라서 그 추기 안의 **반증된 문장을 고치는 것은 규율 11 ③ 의 오류 수정 = 재량**이고, 되돌린 결과는 반증된 전제를 **`docs/lessons/` 안에 총괄 자신의 목소리로** 남겨 둔 것이다 — E-2 가 지적한 형태 그대로다.

**다만 감독의 되돌림은 기본값으로는 옳았다.** 제안 문안(`PROPOSED-fable-advice-correction.md`)은 정정을 **파일 맨 끝**에 붙이는 형태라 「자문 본문을 고치는 것인가 추기를 고치는 것인가」가 흐렸고, 흐리면 보수적으로 가는 것이 맞다. 그리고 「정정이니까」를 열어 두면 다음 편집자가 무엇이 정정인지를 스스로 정하게 된다 — 그 걱정은 정당하다.

**권고 셋.**
- 자문 본문은 **한 글자도** 건드리지 않는다.
- 정정은 **추기 절 안** 또는 추기 절 바로 뒤의 **새 추기**로 넣고, 머리에 「이 절은 총괄 저작이며 자문 원문이 아니다」를 명시한다.
- 규율 10 문언을 「파일」이 아니라 **「저자·절」** 로 다시 적는 것을 상신 대상으로 둔다. 지금 문언(*"감수 산출은 원문 그대로 보존한다"*)은 총괄 추기가 같은 파일에 사는 현재 관행을 다루지 못한다.

### ⑶ E-2 전파 전수 — **8곳 중 정정 필요 자리는 4곳이었고 3곳이 닫혔다. 남은 1곳이 위의 그 줄이다.**

`grep -rn "유일한 탐지기"` (+ `그 오염은 분해 산출에 나타나지 않는다`) 전수:

| 좌표 | 상태 | 정당한가 |
|---|---|---|
| `reader/lib/run_checks.py:56` | **정정됨** — *"구 근거(반증됨)"* + 세 격 재기술 + 「오늘 탐지량 0」 명기 | — |
| `tests/test_m21_…:571` | **정정됨** — docstring 교체 | — |
| `docs/decisions/RULINGS-LEDGER.md:34` | **정정됨** — 원 문언 뒤에 *"★ 정정 2026-09-01 — 이 전제는 반증되었다"* + 포인터 | — |
| `docs/decisions/ruling-20260901-07-T16.md:55, 96` | 무접촉 | **정당** — 원장 원문. 고치면 재정 N6 위반 |
| `docs/decisions/D-20260901-01-pdm2-split.md:206, 214, 220` | 무접촉 | **정당** — 정정 문서 자신(인용·반증·대체표) |
| `docs/lessons/2026-09-01-opus-audit-g6-implementation.md:39, 221-225` | 무접촉 | **정당** — 감수 원문(규율 10) |
| **`docs/lessons/2026-09-01-fable-advice-g6-defect-ownership.md:69`** | **무접촉** | **부당** — 위 ⑵. 자문 원문이 아니라 **총괄 추기**이며, 반증된 전제가 살아 있는 유일한 비원장·비감수 자리다 |

---

## 7. [미검증] — 숨기지 않는 것

1. **실특허 통주를 다시 돌리지 않았다.** 레인 응답이 없어 재생 경로만 가능하고 그 경로는 열지 않았다. WO·`'854` 에 대해서는 **저장된 산출물 대조**만 했다(미분류 분포·조기 판정서 축 상태·`text_verbatim` 최소 길이). Y-1 의 실특허 발화 여부는 그 대조에 근거한 추론이다.
2. **`phase-gate.json` 의 하류 소비자를 판단할 수 없다.** `grep` 상 소비자 0건이지만 `design`·`figures`·`compose`·`gate` 모듈이 아직 없어 **미래 소비자에 대한 판정은 불가**하다. 지금은 「사람이 읽는 기록」이 유일한 용도다.
3. **레인 왕복 지문 층(P-12)과 조기 재시도 증가의 상호작용을 재지 않았다.** `check_lane_binding` 7시나리오 exit 0 만 확인했다 — 직전 감사와 같은 미검증 자리다.
4. **`escalate_on_repeat.signature` 를 `prose_only` 로 분류한 것의 실질을 대조하지 않았다.** 계약이 선언한 서명 `(check_id, rule, locus)` 와 러너가 실제로 계산하는 서명이 같은지는 열어 보지 않았다. 분류가 「읽히지 않음」이라 정직하긴 하나, 그 선언이 **틀려 있어도** 아무도 모른다.
5. **역프로브 13종 중 내가 재현한 것은 11종**(P-A~P-L, P-H 는 P-H2 로 대체)이다. 커밋이 말한 13종의 목록이 없어 나머지는 대조 불가.
6. **`_execute_canonical_tail` 의 `tail_defects` 와 `id_maps` 누적**은 이번에도 열지 않았다(직전 감사 §5 ⑦ 과 같은 자리).
7. **격리 사본을 감수자가 직접 만들었다.** SPEC §8.3 9항 ⓐ 는 사본을 **발주자**가 만들게 하는데 발주문에 사본 지시가 없었고 리포 쓰기가 금지되어 있어, `/tmp/pd-audit-t17`(대상 `39286ca`) · `/tmp/pd-audit-t17-pre`(직전 `ad6d379`) · `/tmp/pd-audit-t16pre`(T16 이전 `9e4cdee`) 3벌을 직접 만들고 마커 `.audit-sandbox` 를 직접 썼다. **직전 감사와 같은 미준수다.** 두 라운드 연속이므로 발주 규격 쪽을 손보는 편이 낫다.
8. **첫 C-1 프로브를 잘못 겨눴다** — `test_m2_read.py` 에 같은 문자열이 3곳 있어 첫 치환이 1895행을 맞았고 `1 passed` 가 나왔다. 좌표를 잡아 다시 돌려(P-J2) C-1 이 닫혔음을 확인했다. 기록으로 남긴다.

---

## 8. 읽기 전용 준수

```
$ git -C /home/laptop/projects/patent-docent status --porcelain    →  (빈 출력)
$ git rev-parse --short HEAD                                       →  39286ca
$ git ls-files -s | sha256sum   →  e056e6d8e29b7b2a12bb8c7060ceef9096efbdceae00052063e38b93869f8e95
```

정본에서 실행한 것은 `git`·`grep`·`sed -n`·`ls`·`find` 읽기와, `runs/**/*.json` 을 여는 python 한 줄뿐이다. **pytest·프로브·관문은 전부 `/tmp` 클론에서 돌렸고**(`.pytest_cache`·`__pycache__` 를 정본에 남기지 않기 위해), 파일 생성·수정·`git` 쓰기는 하지 않았다. 프로브 사본의 되돌림은 매회 `git checkout -- .` 후 `git status --porcelain` 더러움 **0** 으로 확인했다.
EXIT=0
