# 독립 감수 원문 — 막힌 심사 축 감사(`좌석 M9` · opus xhigh 폴백) · 「계산·기록은 됐는데 승인 판정에 도달하지 않는 값」 전수 · **`FOUND: 1`** · 재정 T48 ② A · T49 ③ B 의 집행

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-09 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`REPORT.md` · sha256 `3eff1ede2d9a711a76221603b9a399d37e05078f167742bf77e0bcf730a4d348` · 20,979 B). 레인 = `~/projects/workspaces/pd-lanes/fable-m9-blocked-axis/`.

**좌석 = `좌석 M9` · `claude-opus-5` xhigh** · START 01:30:44 · 종료 01:57 · **약 27분** · EXIT 0 · USAGE `cache_read=4,939,109 cache_creation=194,275 output=88,059(thinking 65,740)`. **원래 좌석은 `fable xhigh`(ROUTING §3 M9)였으나 쿼터 소진으로 즉시 `EXIT=1`(「You've reached your Fable limit」) — 격자가 정한 폴백 `opus xhigh` 로 재기동했다**(새 재정 불요 · 저작이 astra 이므로 벤더 겸직 아님). 대상 = 게이트 사본 `pd-m1b-t40`(핀 `87f66493…` · v44 번들 597 파일) · **read-only 감사 · 대상 트리 무변경 · 최소 입력은 사본에만 만들고 종료 시 삭제**.

**왜 이 감사가 따로 있었나.** 40차에서 「등록표를 거치지 않고 같은 자리에 닿는 정적 경로가 있는가」라는 축을 게이트에 실었더니 **벤더 내용 필터가 두 번 발동해 판정 자체가 나오지 않았다**(2차는 어휘를 전부 지웠는데도 감수자 자신의 추론 단계에서 발동). 그 축을 발주문에서 빼고서야 40차 판정이 성립했고 **그 축은 그 좌석에서 심사 불가로 남았다**. Owner 재정 T48 ② A 가 「그 축만 다른 좌석에」로 처분하고 T49 ③ B 가 시점을 41차 판정 뒤로 정했다. 41·42차를 거치며 축을 좁혔다 — 41차 `OM-2` 와 42차 `ON-1` 이 그 부류의 실물이었으므로, 물음을 **「계산·기록은 됐는데 승인 판정에 도달하지 않는 값이 또 어디에 있는가」**로 바꿔 씨앗 다섯을 주었다.

**★ `FOUND: 1` — `semantic_delta` 가 연산 재고의 차집합을 한 방향만 보고, 그 한 방향도 버린다.** `t40_operations.py:377-387`. 루프가 `candidate.operations` **만** 돌기 때문에 ⒜ **기준에만 있고 후보에서 사라진 연산**의 잔여(`inventory`)가 한 번도 읽히지 않고 `return` 에서 소멸하고, ⒝ 후보에만 있으면서 `protocol_safe is True` 인 것은 382행에서 폐기된다. 두 값 모두 `Graph.operation()`(`t40_control.py:276-290`)이 `line`·`column`·`signature` 까지 갖춰 `graph.operations` 에 **이미 적재해 둔 것**이다.

**최소 입력 둘 — 각각 한 곳만 고친다.** **A** = `t40_flow.py:26` 의 `@property` **한 줄 삭제**(`Captured.ok`) · **B** = `t40_receipts.py:297` 의 상수 기본값 **한 글자**(`mode='w'` → `'a'`). **입력 B 의 검사기 출력은 기준선과 한 글자도 다르지 않다**(`TRAVERSAL 48480/48480` · `DOMINANCE 24957/24957 pending 0` · `STRUCTURAL 260/0` · exit 0). 입력 A 는 순회 총계만 48478 로 떨어지고 위반 0 이다.

**실제로 깨지는 것은 검사기가 같은 런에서 통과 처리한 검사의 이름 그대로다.** 입력 A 에서 `Captured.ok` 가 property 를 잃어 **bound method** 가 되면 언제나 참이므로 실패가 성공으로 읽힌다 — `status=Failure` 인데 `ok_truthy=True` · `machine_state=work:Success` · `stopped=False`. 그런데 `t40_structure.py:238` 의 **`STRUCT-STATE Captured.ok 는 정확히 Success 하나`** 와 `:251` 의 **`STRUCT-FAIL 실패가 stop 상태를 만든다`** 가 그 런에서 통과했다. 238행이 `ok` 의 **본문만** 대조하고 데코레이터를 보지 않기 때문이다. 입력 B 는 발행 writer 가 truncate 에서 append 로 바뀌어 `ClosedFile(path, len(raw))` 가 실제 닫힌 파일과 어긋난다(`on_disk_len` 2 → 6).

**사정거리** — 9개 생산 모듈의 데코레이터 66개 중 **51개가 `Call` 이 아니어서 CFG 사건이 아니고**, 그중 `t40_structure` 가 이름을 대고 검사하는 16개를 빼면 **35개는 삭제해도 승인된다**. `@property` 넷(`Captured.ok`·`Environment.ok`·`Execution.state`·`Execution.environment_ok`)은 전부 입력 A 와 같은 **허용 방향** 파괴다. 상수 기본값은 54개 있고 전부 입력 B 와 같은 층이다.

**고치는 문안과 그 비용을 감사자가 함께 쟀다** — `t40_operations.py:382` 의 `elif row['protocol_safe'] is not True:` 를 `else:` 로 바꾸고 `return` 앞에 `inventory` 잔여를 problems 로 넣는다(어느 한쪽만 닫아도 입력 A·B 는 둘 다 잡힌다). **v44 무변경 사본 544 스코프 전부에서 `residual_reference_operations=0 new_safe_operations=0 unsupported=0` — 오탐 비용 0.**

**★ 「없다」도 실행으로 확인했다 — 이것이 이 감사의 절반이다.** 씨앗 ② **빈 결과가 승인으로 읽히는 경우 = 없다**(구문 오류를 심으면 exit 1 · 0바이트 파일은 위반 16 · 승인 경로에 시간·크기 예산이 없고 `_COMPARISONS` 는 1024 초과 시 **비우고 재계산**하지 건너뛰지 않는다). 씨앗 ③ **부분 결과를 전체로 쓰는 경우 = 없다**(부분성이 생기는 `except` 세 곳이 전부 `continue` 전에 `problems` 등재 · 스코프 목록은 양방향 집합). 씨앗 ⑤ **fail-open 대체 = 42차가 찾은 `t40_order.py:115` 외에 새것 없음**(나머지 셋은 fail-**closed** 이거나 빈 값이 될 수 없음을 각각 확인). 씨앗 ① 은 `OM-2` 하나뿐이고 이미 닫혔다.

**다음 회차 좌표 다섯(⒜~⒠) — 세 조건을 못 채워 `FOUND` 에 넣지 않았다.** ⒜ **비교 없이 `checked` 에 들어가는 집합 셋**(`t40_dominance.py:250-261` 의 `_expanded` 새 스코프는 **모든 사건을 `required` 에 넣고 곧바로 `checked` 에 넣는다** — 대조 0건 · `audit():234` 와 `compare_function:169` 도 무조건 `checked.add`. 감사자의 문장 = 「**「검사했다」가 아니라 「검사했다고 적었다」**」 · 반례를 **못 만든 것이지 없다고 확인한 것이 아니다**). ⒝ **`t40_order.inventory()` 는 후보를 한 번도 보지 않는다** — `t40_dominance.py:179` 가 기준 AST 로 부르므로 `inventory_difference` 는 **기준의 자기정합만** 재고 후보 증거가 아니다(544 스코프 × 매 런 계산되지만 후보 때문에 0 이 아니게 될 수 없다). ⒞ `report['historical_missing']` 이 CLI 판정에 닿지 않는다(읽는 것은 별도 도구뿐 · 지금은 동시에 위반이 나므로 반례 불가이나 결속이 바뀌면 즉시 위험). ⒟ `finally` 안 guard 는 최대 5회 전개되는데 `self.guards[key]` 는 **마지막 전개 하나만** 남아 나머지 복제본의 거부 지배가 계산되지 않는다. ⒠ **순회 총계 48480 에 기대값이 없다** — 입력 A 에서 48478 로 떨어졌는데 위반 0 이었고, 관문은 같은 트리 안의 자기정합만 본다. **대조할 상대(`R12-REPORT.md:25` 의 48480)는 이미 있다.**

**★ ⒝ 가 14차 주장의 뜻을 바꾼다.** 14차 보고와 42차 게이트가 모두 「손으로 쓴 재고와 차집합 0」을 순서 도출의 근거로 들었고 게이트는 그것을 「**선택 범위**의 검증」으로 한정했다. 이 감사는 한 단계 더 들어간다 — **그 재고 비교는 후보를 아예 보지 않는다.** 후보 승인의 근거로 쓸 수 없다.

**감사자가 스스로 적은 한계** — 「⑴의 세 조건을 채운 발견을 더 찾지 못한 것이 「없다」의 증명은 아니다 · §1 의 전수는 **승인 경로에 닿는 부정적 값의 목록**에 대한 전수이고 **「사건을 만들지 않는 편집」의 공간 자체는 전수하지 않았다** · 사정거리 35개 중 실제로 돌려 본 것은 2개」. 그 외 미심사 = `t40_sites.py`(SITE 68 재고 · **입력 A·B 가 SITE 대조에는 걸리는지 미확인 — 걸린다면 노출은 이 보고서보다 좁다 · 다음 회차가 반드시 채울 칸**) · 회귀·불변성·런타임 오라클 도구 · 생산 모듈 내용 · ROBDD 정확성 · ⒜ 의 `_expanded` 반례.

**처분 = `AX-1` 수용(공학) · 이행 = Owner 재정 뒤 결정**(42차 상신과 함께 올린다). **다음 회차 좌표 ⒜~⒠ 는 `AX-a`~`AX-e` 로 이연** — 반례가 없어서가 아니라 세 조건을 못 채워서다.

지적 열거 = AX-1

---

# 감수 원문 (claude-opus-5 xhigh · 이 아래는 감사자 저작)

FOUND: 1
METHOD: 9개 검사기 모듈(t40_structure/dominance/order/control/syntax/meaning/operations/proofs/bindings, 2,285행)에서 「부정적 값을 만드는 자리」를 전수 열거한 뒤 각각이 problems/violations/missing/pending 중 하나로 흐르는지 역추적하고, 흐르지 않는 자리마다 최소 입력을 만들어 실제 CLI(`t40_structure.py <후보디렉터리>`)로 승인을 관측했다.

---

## 0. 접지 확인

```
$ cat .audit-sandbox
path=/home/laptop/projects/workspaces/pd-m1b-t40
pin=87f66493f301b4e5c9bc159c1626ef7a76d32158
order=M1B-t40-measure-v44-20260909
disposable=true
$ git -C . rev-parse HEAD
87f66493f301b4e5c9bc159c1626ef7a76d32158
```

핀 일치. 대상 트리를 수정하지 않았고 커밋하지 않았다. 최소 입력은 전부
`pd-lanes/fable-m9-blocked-axis/scratch/` 안의 9개 생산 모듈 사본에만 만들었고
감사 종료 시 삭제했다(재현 절차는 §2.3에 전문으로 남긴다).

**기준선**(무변경 사본, 63초):

```
TRAVERSAL sources=10 expected=48480 visited=48480 missing=0 extra=0 declared_untraversed=0 actual_untraversed=0 difference=0
DOMINANCE scopes=544 required=24957 checked=24957 difference=0 extra=0 unsupported=0 pending=0 order_scopes=544
STRUCTURAL checks=260 violations=0        (exit 0)
```

---

## 1. 전수 방법 — 어떻게 「없다」를 확인했는가

승인 판정에 닿는 경로는 정확히 넷이다.

| 판정 경로 | 정본 |
|---|---|
| `problems` 비어 있음 | `t40_structure.py:495` `raise SystemExit(bool(problems))` |
| `dominance['violations']` | `t40_structure.py:384` — 전부 `problems`로 승격 |
| `dominance['missing']`·`['extra']` | `t40_structure.py:386` |
| `dominance['semantic_proof_pending']` | `t40_structure.py:387` (= 14차의 OM-2 처분) |

그래서 「부정적 값을 만드는 자리」를 열거하고 각각이 이 넷 중 하나에 도달하는지 봤다.
도달하는 것으로 확인한 자리(재보고하지 않는다):

- `t40_syntax.inspect()`의 `issues` 7종 → `audit():207-209`에서 `unsupported`와 `violations` **양쪽**에 등재.
- `Graph.__init__`의 `Unsupported`/`RecursionError` → `audit():235-239` 양쪽 등재 **+** `required`에만 넣어 `missing`으로 3중.
- 확장 스코프의 `Unsupported` → `audit():252-255` 양쪽 등재.
- `compare_function`의 5종(`semantic_delta` 산출 · 선행조건 비지배 · `required event missing` · `required operation is dead/missing` · `unreviewed event`) → 전부 `problems`.
- `t40_order.compare`의 `violations`·`inventory_difference` → `compare_function:183`을 거쳐 `problems`.
- 역사 의무의 `Unexamined` → `problems` **및** `semantic_proof_pending`(OM-2 처분이 실물임을 확인).
- `t40_structure`의 `require(...)` 260건 → `problems`.

**씨앗 ② (빈 결과가 승인으로 읽힘) — 이 검사기에 없다.** 실행으로 확인했다.
① 파일 판독 실패: `t40_envelope.py`에 구문 오류를 심으면 `check()`가 `problems` 1건을 들고
조기 반환하고, `LAST_REPORT`가 `{}`이라 `syntax_summary`가 `KeyError`로 죽는다 — **exit 1**.
② 빈 소스: `t40_envelope.py`를 0바이트로 만들면
`STRUCTURAL checks=258 violations=16` · `difference=13` · **exit 1**.
③ 승인 경로에 시간·크기 예산이 없다. `_COMPARISONS`(`t40_dominance.py:230`)는 1024 초과 시
**비우고 재계산**하지 절대 건너뛰지 않고, `lru_cache`(`instructions`/`parsed`)는 순수 메모다.
④ `prepare_gates`는 `at_prepared`가 비면 `set()`을 돌려주므로 `PREPARED[command] <= set()`이
6개 명령 전부에서 거짓 → 위반. 「아무것도 못 봤다」가 승인이 되지 않는다.

**씨앗 ③ (부분 결과를 전체로) — 없다.** 부분성이 생기는 유일한 자리는 위 `except` 3곳인데
전부 `continue` 전에 `problems`에 등재한다. 스코프 목록은 `set(reference)|set(current)` 양방향이고
어느 쪽에만 있어도(`required scope missing` / `unreviewed scope`) 위반이다.

**씨앗 ⑤ (fail-open 대체) — 전수로 훑었고 `t40_order.py:115` 외에 새것이 없다.**
`t40_order`·`t40_dominance`·`t40_structure`의 「한쪽이 없을 때 메우는」 자리는 넷뿐이다.
`t40_order.py:115`(42차 기지), `t40_dominance.py:116`
(`actual.guards.get(guard,(None,None))[0]` → `Graph.reach(start=None)`은 함수 **entry**에서 출발하므로
도달 집합이 넓어지고, 넓어짐은 `observed[target] and not reachable`을 더 자주 참으로 만든다 = fail-**closed**.
게다가 guard 이벤트 삭제 자체는 `entry` 질의의 `required event missing`이 잡는다),
`t40_dominance.py:137`(`or []` — `groups`는 `len>1`일 때만 만들어져 빈 리스트가 되지 않는다),
`t40_dominance.py:215`(`baseline['files'].get(...,{})` → `.get('sha256')`이 `None`이면 해시 불일치 = 위반).

**씨앗 ① (상태 표시가 집합 소속을 막지 않음) — `OM-2` 하나뿐이고 이미 닫혔다.**
`required`에 넣으면서 `checked`에 넣지 않는 자리는 지금 전부 동시에 `problems`도 낸다.
반대로 **비교 없이 `checked`에 넣는** 자리는 셋 남아 있다(§3 ⒜).

**씨앗 ④ (집계에서 사라짐) — 하나 찾았다. 아래가 그것이다.**

---

## 2. 발견 1 — `semantic_delta`가 연산 재고의 차집합을 한 방향만 보고, 그 한 방향도 `protocol_safe`로 비운다

### 2.1 파일·행

`t40_operations.py:377-387` (`semantic_delta`), `t40_dominance.py:110-112`에서 호출.

```python
inventory = collections.Counter(r['signature'] for r in reference.operations)   # 377
problems = []
for row in candidate.operations:                                                # 379  ← 후보만 돈다
    if inventory[row['signature']]:
        inventory[row['signature']] -= 1                                         # 381
    elif row['protocol_safe'] is not True:                                       # 382  ← 여기서 버린다
        problems.append({...})
return problems                                                                  # 387  ← inventory 잔여는 사라진다
```

### 2.2 삼킨 값이 무엇이고 어디서 계산됐는가

`Graph.operation()`(`t40_control.py:276-290`)이 **모든 명시 연산**을 `operation`·`detail`·
`expression`·`line`·`column`·`protocol_safe`·`signature`(= `sha256(kind:detail:ast.dump(operation_shape))`)로
계산해 `graph.operations`에 적재한다. `semantic_delta`는 그 두 다중집합의 차집합을 계산할 재료를
전부 손에 쥔 뒤 **두 값을 버린다**.

- **⒜ 기준에만 있고 후보에 없는 연산** — 루프가 `candidate.operations`만 돌기 때문에
  `inventory`에 남은 잔여가 **한 번도 읽히지 않는다**. 「모델된 연산이 후보에서 사라졌다」는
  사실은 `inventory` 안에 실물로 만들어졌다가 `return` 한 줄에서 소멸한다.
- **⒝ 후보에만 있는 연산 중 `protocol_safe is True`인 것** — `inventory[sig] == 0`이라는
  부정적 사실은 **계산되고**(381행 조건이 거짓으로 평가된다) 382행에서 폐기된다.

두 값 모두 `graph.operations` 안에 `line`/`column`까지 갖춘 채로 **기록되어 있고**,
`R13-MEANING-CENSUS.json`·`R13-SEMANTIC-CONTRACTS.md`가 그 계약을 문서로 들고 있다.
승인 판정에는 닿지 않는다.

이 차이는 **사건(event)이 아니다**. 데코레이터·기본값·시그니처는 `Call`이 아닌 한
`Graph.__init__`의 사건 종류(`call/store/Return/Raise/Yield/Break/Continue`) 어디에도 없으므로
지배 질의·`live` 검사·`t40_order`의 frontier가 전부 통과한다. 즉 **연산 층에서만 보이는 차이**이고,
연산 층의 유일한 관문이 `semantic_delta`다.

### 2.3 최소 입력 둘 — 각각 한 곳만 고친다

**입력 A — `t40_flow.py:26`의 `    @property` 한 줄 삭제** (`Captured.ok`).

```
    @property
    def ok(self):                          →    def ok(self):
        return self.status is Status.SUCCESS         return self.status is Status.SUCCESS
```

**입력 B — `t40_receipts.py:297`의 상수 기본값 한 글자**
(`def write_closed(path, raw, mode='w'):` → `mode='a'`).

재현:

```bash
cd /home/laptop/projects/workspaces/pd-m1b-t40/bundle
mkdir -p /tmp/t40cand && cp t40_metrics.py t40_replay.py t40_receipts.py t40_drive.py \
  t40_resources.py t40_flow.py t40_consume.py t40_envelope.py t40_excerpts.py /tmp/t40cand/
# 입력 A
python - <<'PY'
p='/tmp/t40cand/t40_flow.py'; s=open(p).read()
old="    @property\n    def ok(self):\n        return self.status is Status.SUCCESS\n"
new="    def ok(self):\n        return self.status is Status.SUCCESS\n"
if s.count(old)!=1: raise SystemExit(1)
open(p,'w').write(s.replace(old,new,1))
PY
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B t40_structure.py /tmp/t40cand
```

### 2.4 검사기 출력 원문

**입력 A**(마지막 세 줄, exit 0):

```
TRAVERSAL sources=10 expected=48478 visited=48478 missing=0 extra=0 declared_untraversed=0 actual_untraversed=0 difference=0
DOMINANCE scopes=544 required=24957 checked=24957 difference=0 extra=0 unsupported=0 pending=0 order_scopes=544
STRUCTURAL checks=260 violations=0
```

**입력 B**(마지막 세 줄, exit 0) — **기준선과 한 글자도 다르지 않다**:

```
TRAVERSAL sources=10 expected=48480 visited=48480 missing=0 extra=0 declared_untraversed=0 actual_untraversed=0 difference=0
DOMINANCE scopes=544 required=24957 checked=24957 difference=0 extra=0 unsupported=0 pending=0 order_scopes=544
STRUCTURAL checks=260 violations=0
```

스코프 단위 계측(입력 A, `t40_flow.py:Captured`):

```
events ref-cand: []                       ← 사건 차이 0
events cand-ref: []
ops lost  (ref-cand): [('DECLARE','@property\ndef ok(self): ...'), ('DECORATE','property'), ('LOOKUP','property')]
ops gained(cand-ref): [('DECLARE','def ok(self): ...')]
semantic_delta problems: []               ← ⒜가 3건, ⒝가 1건을 삼켰다
compare_function problems: []   required 6 checked 6
```

### 2.5 실제 동작이 깨는 불변식

**입력 A** — `Captured.ok`가 property를 잃어 **bound method**가 된다. 항상 참이다.

```
--- 기준선 ---  status=Failure ok_truthy=False machine_state=work:Failure stopped=True   (exit 0)
--- 입력 A ---  status=Failure ok_truthy=True  machine_state=work:Success stopped=False  (exit 9)
                BROKEN: Failure result reports ok-truthy
                BROKEN: failed step recorded as success -> state=work:Success stopped=False
```

깨진 불변식은 **검사기가 같은 런에서 통과 처리한 260건 중 두 건의 이름 그대로**다 —
`STRUCT-STATE Captured.ok는 정확히 Success 하나`(`t40_structure.py:238`)와
`STRUCT-FAIL 실패가 stop 상태를 만든다`(`t40_structure.py:251`). 238행은 `ok`의 **본문**만
(`self.status is Status.SUCCESS`) 대조하고 데코레이터를 보지 않는다. 그래서 fail-stop 전이 전체
(`Machine.step`의 `if result.ok:` · `Machine.require`의 `not result.ok` · `run_drive`의 실패 중단 ·
`entry`의 `result.unwrap()` 앞 분기)가 실패를 성공으로 읽는다.

**입력 B** — 발행 writer가 truncate에서 append로 바뀐다.

```
--- 기준선 ---  receipt.size=2 on_disk='BB'     on_disk_len=2   (exit 0)
--- 입력 B ---  receipt.size=2 on_disk='AAAABB' on_disk_len=6   (exit 9)
                BROKEN: republication did not replace the artifact
                BROKEN: ClosedFile(path, len(raw)) disagrees with the closed file
```

`ClosedFile(path, len(raw))`(`t40_receipts.py:320`)가 주장하는 발행 크기와 실제 닫힌 파일이 어긋난다.
검사기는 같은 런에서 `STRUCT-FILE 성공 반환은 닫힘 증표만`(`t40_structure.py:423`)을 통과 처리했다.
`t40_structure.writes()`(93-103행)도 이 `open`을 쓰기로 세지 않는다 — `open(path, mode, **options)`의
둘째 인자가 `Constant`가 아니라 `Name`이라 100행 조건이 거짓이다.

### 2.6 고치는 문안 한 줄

`t40_operations.py:382`의 `elif row['protocol_safe'] is not True:`를 `else:`로 바꾸고,
`return problems` 앞에
`problems += [{'reason':'modeled operation removed','signature':s,'evidence_tag':'model'} for s,n in inventory.items() for _ in range(n)]`
를 넣는다(⒜·⒝ 각각을 닫는다 — 어느 한쪽만 닫아도 입력 A·B는 둘 다 잡힌다).

**비용 실측**: v44 무변경 사본 544 스코프 전부에서
`residual_reference_operations=0 new_safe_operations=0 unsupported=0`.
기준선에서 이 강화의 오탐 비용은 0이다.

### 2.7 사정거리

이 구멍이 열어 주는 편집은 **CFG 사건을 만들지 않는 모든 편집**이다.
9개 생산 모듈의 데코레이터 66개 중 **51개가 `Call`이 아니다**(= 사건이 아니다).
그중 `t40_structure`가 이름을 대고 검사하는 것은 16개(`cmd_*`×6 · `run_engine` · `seal_source` ·
`envelope.main` · `excerpts.main/ex1/ex2` · `metrics.main` · `replay.main` · `write_receipt` ·
`author_input` · `author_output`)뿐이고 **나머지 35개는 삭제해도 이 검사기가 승인한다**.
그중 `@property` 4개(`Captured.ok`·`Environment.ok`·`Execution.state`·`Execution.environment_ok`)는
전부 입력 A와 같은 **허용 방향** 파괴다. 상수 기본값은 9개 모듈에 54개 있고 전부 입력 B와 같다.
함수 파라미터 이름·순서도 같은 층에 있다(`DECLARE` 서명만 바뀐다).

---

## 3. 확인은 했지만 ⑴의 세 조건을 채우지 못해 **세지 않은** 것

각각 「계산·기록되지만 판정에 닿지 않는」 값이 맞다. 불변식을 깨는 최소 입력을 만들지 못했으므로
FOUND에 넣지 않는다. 다음 회차의 좌표로 남긴다.

**⒜ 비교 없이 `checked`에 들어가는 집합 셋.**
`t40_dominance.py:250-261` — 후보에만 있는 새 스코프가 `_expanded`이고 owner가 기준에 있으면
그 스코프의 **모든 사건**을 `required`에 넣고 **곧바로 `checked`에 넣는다**(대조 0건).
`audit():234` — `location|grammar`도 무조건 `checked.add`. `compare_function:169` — 증서가 있으면
`checked.add`. 앞의 둘은 「검사했다」가 아니라 「검사했다고 적었다」이다.
`expand_helpers`의 유효성 조건(무인자·호출문 전용·정의 뒤·`direct()` 안의 맨 호출)이 실제로 촘촘해서
반례를 못 만들었다 — **못 만든 것이지 없다고 확인한 것이 아니다.**

**⒝ `t40_order.inventory()`는 후보를 한 번도 보지 않는다.**
`t40_dominance.py:179`가 `compare(order_reference, actual, reference)`로 부르므로
`inventory(fn)`의 `fn`은 **기준 AST**다. 즉 `inventory_difference`는 기준의 자기정합만 재고,
`ANALYSIS_SCOPE.effect_order`가 광고하는 "lexical inventory difference"는 후보 증거가 아니다.
544 스코프 × 매 런 계산되지만 후보 때문에 0이 아니게 될 수 없다.

**⒞ `report['historical_missing']`은 CLI 판정에 닿지 않는다.**
`t40_dominance.py:286`이 계산하고 보고서에 싣지만 `t40_structure.check()`는 읽지 않는다.
읽는 것은 별도 도구 `t40_immutability_r13.py:63`뿐이다. 지금은 `compare_function`이
역사 행을 빠짐없이 `required`에 넣으므로 이 값이 비지 않으려면 **동시에 위반이 있어야** 한다 —
그래서 현재 형태에서는 반례를 만들 수 없다. 결속이 바뀌면 즉시 위험해지는 자리다.

**⒟ `finally` 안 guard는 마지막 복제본만 질의된다.**
`t40_control.py:428` `self.guards[key]=(entry,f)`는 딕셔너리 대입인데, `Try`의 `finalbody`는
정상/return/raise/break/continue마다 최대 5회 전개된다(`442-451행`). `self.events[key]`는 5개
정점을 모두 갖는데 `self.guards[key]`는 **마지막 전개의 entry 하나**만 남는다.
`reject:` 질의는 그 하나에서만 출발한다. 나머지 복제본의 거부 지배는 계산되지 않는다.

**⒠ 순회 총계 48480은 인쇄되지만 회차 간 대조가 없다.**
`t40_syntax.inspect()`가 `expected`/`visited`를 계산하고 `syntax_summary`가 인쇄하는데,
관문은 **같은 트리 안의 DFS ↔ `ast.walk` 자기정합**뿐이다. 동결 기준의 48480과 대조하지 않는다.
입력 A에서 이 값이 48480 → **48478**로 떨어졌는데 `violations=0`이었다.
`R12-REPORT.md:25`가 48480을 문서로 들고 있으니 대조할 상대는 이미 있다.
(이것을 별건으로 세지 않은 이유: 검사기 안에 「기대값」이 없어서 「부정적 사실」이 계산되지 않는다.
계산되는 것은 현재 총계뿐이다.)

---

## 4. 내가 확인하지 못한 것

- **⑴의 세 조건을 채운 발견을 더 찾지 못한 것이 「없다」의 증명은 아니다.** §1의 전수는
  **승인 경로에 닿는 부정적 값의 목록**에 대한 전수이고, 「사건을 만들지 않는 편집」의 공간
  자체는 전수하지 않았다. 발견 1의 사정거리(§2.7)는 정적 열거로만 셌고 35개 데코레이터 중
  실제로 돌려 본 것은 2개다.
- **`t40_sites.py`(SITE 68 재고)를 심사하지 않았다.** `t40_structure`는 이 모듈에서 `CODE_FILES`
  상수만 가져오고 SITE 대조를 부르지 않는다. 즉 STRUCTURAL 판정의 일부가 아니라서 제외했다.
  발견 1의 입력 A·B가 **SITE 대조에는 걸리는지**는 확인하지 않았다 — 걸린다면 파이프라인
  전체의 노출은 이 보고서가 말하는 것보다 좁다. **이것은 다음 회차가 반드시 채워야 할 칸이다.**
- **`t40_regress_r14.py`·`t40_immutability_r13.py`·`t40_oracle_r13.py`(런타임 오라클)를 돌리지 않았다.**
  ⒞에서 `historical_missing`을 실제로 보는 것은 immutability 도구다. 이 도구들이 입력 A·B를
  잡는지 모른다.
- **`t40_metrics.py`(915행)·`t40_drive.py`·`t40_replay.py` 등 생산 모듈의 내용을 심사하지 않았다.**
  이 감사의 대상은 검사기이고 생산 모듈은 입력으로만 다뤘다.
- **`t40_*.bak.py` 42개와 R10~R14 산출 JSON은 읽지 않았다.** 597 파일 중 실제로 읽은 것은
  검사기 9개 모듈 + `R14-UNRESOLVED.md`·`ruling-T48/T49` 요지뿐이다.
- **`Boolean`(ROBDD)의 정확성을 검증하지 않았다.** `op`의 조기 반환과 캐시 상호작용을 읽고
  넘어갔을 뿐 반례를 찾지 않았다. BDD가 틀리면 `reach`/`frontiers`가 통째로 틀린다.
- **⒜의 `_expanded` 경로에 반례가 없다고 말할 수 없다.** 4가지 회피(중첩 함수 안 참조 · lambda 본문 ·
  GeneratorExp · 컴프리헨션)를 손으로 따라가 막힌 것을 확인했지만 실행으로 시험하지 않았다.
- **41차가 이미 확인한 것과 42차의 `t40_order.py:115`는 재검하지 않았다**(발주문 ⑸ 지시).

---

## 부록 — 실동작 검증 스크립트 전문 (scratch 삭제분)

`assert` 없이 명시 비교 + 비영 종료 코드로 쓴다(`python -O`에서도 살아남는다).

**입력 A** (`demo1.py <후보디렉터리>` · 기준선 exit 0 / 입력 A exit 9):

```python
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import t40_flow as F

def boom(): raise ValueError('business failed')

m = F.Machine('demo', ('work',))
result = m.step('work', boom)
truthy, status, state, stopped = bool(result.ok), result.status.value, m.state, m.stopped
print('status=%s ok_truthy=%s machine_state=%s stopped=%s' % (status, truthy, state, stopped))
bad = 0
if status == 'Failure' and truthy:
    print('BROKEN: Failure result reports ok-truthy'); bad += 1
if state != 'work:Failure' or stopped is not True:
    print('BROKEN: failed step recorded as success -> state=%s stopped=%s' % (state, stopped)); bad += 1
sys.exit(0 if bad == 0 else 9)
```

**입력 B** (`demo2.py <후보디렉터리>` · 기준선 exit 0 / 입력 B exit 9):

```python
import sys, os, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import t40_receipts as RC

write = RC.write_closed.__wrapped__          # entry/환경 shim만 우회한다
d = tempfile.mkdtemp(); p = os.path.join(d, 'artifact.json')
first  = write(p, 'AAAA')
second = write(p, 'BB')                      # 같은 산출물의 재발행
on_disk = open(p, encoding='utf-8').read()
print('receipt.size=%d on_disk=%r on_disk_len=%d' % (second.size, on_disk, len(on_disk)))
bad = 0
if on_disk != 'BB':
    print('BROKEN: republication did not replace the artifact'); bad += 1
if second.size != len(on_disk):
    print('BROKEN: ClosedFile(path, len(raw)) disagrees with the closed file'); bad += 1
sys.exit(0 if bad == 0 else 9)
```

**대상 트리 무결성** — 감사 종료 시점에 `bundle/BUNDLE-SHA256.txt` 596행 전건 `OK`.
`bundle/` 안의 어떤 파일도 수정하지 않았고 커밋하지 않았다. scratch는 비웠다.
