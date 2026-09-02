# D5 ①② — 청구항 구성요소 전 분해 + 관계 트리

**너의 작업(`decompose`).** 청구항 구간 전량을 읽고, 각 청구항을 구성요소 단위로 **전부** 분해한다. 요약하지 않는다. 고르지 않는다. **전 분해**는 문언 그대로다.

받는 조각은 둘이다 — `claims-section`(청구항 구간 전문)과 `bibliographic-head`(서지 머리). 명세서 본문은 이 단계에서 주지 않는다. 분해는 청구항의 일이고, 본문을 함께 보면 분해가 요약으로 미끄러진다.

---

## 1. 청구항 하나도 빠뜨리지 않는다

원천 청구항 목록은 러너가 별도로 파싱해 **양방향으로 대조**한다(`read.claim-inventory`). 하나가 빠지면 남은 것들이 아무리 잘 접지되어 있어도 실패한다. 취소 청구항(`(canceled)`)은 등재 의무에서 면제된다.

- 독립항 → `claims.independent[]`, 종속항 → `claims.dependents[]`. 이 분류는 **원문이 다른 청구항을 인용하는가**로 결정된다. 인용하면 종속항이다.
- 청구항 ID는 `CL-<원천 번호>`다. 번호를 다시 매기지 않는다.

## 2. 구성요소 분해

### 독립항 (`claims.independent[]`)

**독립항 하나는 `{id, type, text_verbatim, elements}`를 전부 갖는다 — 넷 다 필수다.**

```json
{ "id": "CL-1",
  "type": "independent",
  "text_verbatim": "A stacked module comprising:",
  "elements": [
    { "id": "CL-1/e1", "text_verbatim": "a substrate having a first surface",
      "material_id": "M1", "children": [] }
  ] }
```

- **★ `type` 은 빠뜨릴 수 없다.** 스키마가 `const: "independent"` 로 **필수**를 집행하며(`reader/schemas/material-spec.schema.json#$defs.claims.properties.independent.items.required`), 빠지면 `read.schema`가 `'type' is a required property`로 응답 전체를 실패시킨다. 값은 언제나 문자열 `"independent"` 하나뿐이다 — 고를 것이 없으므로 **적기만 하면 된다.**
- 종속항(`claims.dependents[]`)에는 `type`이 **없다.** 그쪽은 `dependency_type`이 그 자리를 진다 — 두 필드를 헷갈리지 마라.

- 각 element는 `{id, text_verbatim, material_id, children}`.
- `id` 문법은 `CL-1/e1`이고, 중첩되면 경로가 길어진다(`CL-1/e2/e1`).
- `text_verbatim`은 **원문 바이트 그대로**의 부분문자열이다. 전제부·연결어를 다듬지 마라.
- 하위 한정이 있으면 `children`으로 층을 만든다. 평평하게 펴면 ②의 관계 트리가 사라진다.

#### ★ 청구항 `text_verbatim`의 경계 규약

청구항 전문에도 같은 문제가 있고, 이쪽이 파급이 더 크다 — `read.convergence`의 `tree-edges` 축은 **청구항 전문을 최상위 element의 부모 문언으로** 쓰므로, 관례 하나가 갈리면 최상위 간선이 **전부** 어긋난다.

| # | 규약 |
|---|---|
| ① | **번호 접두를 포함하지 않는다.** `**1**. ` · `1. ` 같은 표기는 열거의 문법이지 청구항의 문언이 아니다. 전제부(`A hardware accelerator comprising:` 또는 인용구 `The method according to claim 12,`)부터 시작한다 |
| ② | **줄 끝 하드브레이크 공백과 후행 개행을 포함하지 않는다.** 마지막 마침표까지가 청구항이다 |
| ③ | 잘라낸 뒤에도 **원문의 연속 부분문자열**이어야 한다(element 규약 ④와 같다) |

#### ★ 경계 규약 (수렴의 전제 — 반드시 지켜라)

`read.convergence`는 두 독립 실행의 `text_verbatim`을 **문자열로** 비교한다. 따라서 같은 구성요소를 **어디서 끊었는가**가 한 글자라도 다르면 그 둘은 다른 원소로 세어진다. 아래 규약이 없으면 두 실행은 같은 특허를 같은 깊이로 읽고도 수렴하지 못한다.

**2026-08-18 실측** — 이 규약이 없던 상태로 실특허 1건을 두 번 독립 독해한 결과 element 집합 Jaccard가 **0.59**였다(임계 0.95). 원인의 절반이 아래 ①이었고(교정 시 0.75로 상승) 나머지가 ②였다. 두 실행 다 "바이트 그대로"를 지켰다 — 규약이 없었을 뿐이다.

| # | 규약 | 이유 |
|---|---|---|
| ① | **선두 등위접속사(`and`·`or`)와 그 뒤 공백은 element에 포함하지 않는다.** 열거의 마지막 항이 `and a heat spreader …`라면 element는 `a heat spreader …`부터다 | 접속사는 **열거의 문법**이지 구성요소의 일부가 아니다. 포함 여부가 갈리면 같은 구성요소가 두 문자열이 된다 |
| ② | **선행 구성요소를 수식하는 후치 수식절은 새 element가 아니라 그 구성요소의 `children`이다.** `…, the first format and the second format being flexible`처럼 앞에서 도입된 대상을 한정하는 절이 여기 해당한다 | 형제로 올리면 트리의 층이 하나 사라지고(②의 관계 트리 상실), 두 실행이 같은 절을 서로 다른 층에 놓는다 |
| ③ | **끝 구분자(`;`·`,`·`.`)는 element에 포함하지 않는다.** 열거 항의 끝은 구분자 **앞**이다 | 구분자는 열거의 문법이며 ①과 같은 이유다 |
| ④ | 위 셋을 적용한 뒤에도 **남은 문자열은 원문의 연속 부분문자열이어야 한다.** 잘라낸 자리를 메우려고 글자를 더하거나 고치지 마라 | `read.verbatim`은 바이트로 대조한다. 규약은 **어디서 자르는가**를 정할 뿐 무엇을 쓰는가를 바꾸지 않는다 |
| ⑤ | **순수 연결구는 element가 아니다.** 뒤따르는 열거를 도입하기만 하고 **자기 한정을 갖지 않는** 절(예: `wherein the compute device comprises:`)은 element로 만들지 않고, 그 열거 항목들을 **그 절이 되짚는 element의 `children`**으로 붙인다. 판정법 — 되짚는 주어(`the compute device`)와 열거 도입어(`comprises:`·`including:`·`wherein:`)를 걷어낸 뒤 **한정하는 술어가 하나도 남지 않으면** 순수 연결구다. 남으면(예: `wherein a column cell … is configured to output a primitive product … and comprises:`) element다 | 순수 연결구를 element로 만들면 **아무것도 한정하지 않는 component 항목**이 생기고, 그 빈 항목이 접지·커버리지의 대상이 되어 검사가 실체 없는 것을 세게 된다. **2026-08-18 실측**: 한 실행은 이 절을 생략하고 다른 실행은 element로 만들어, 18개 합집합 중 1개가 갈려 `element-set`이 **0.9444**로 임계(0.95)를 아슬하게 밑돌았다 |
| ⑥ | **여러 형제를 동시에 수식하는 후치 수식절은 그 형제들의 최소 지배 노드(nearest common ancestor)의 `children`이다.** 최소 지배 노드가 청구항 자체이면 최상위 element로 남긴다. 예: `wherein the first/second/third multiplexer perform respective selections …`은 세 멀티플렉서를 동시에 걸므로 그 셋을 지배하는 노드 밑으로 내린다 | 규약 ②는 **단일 대상**을 전제하고 다중 대상에 답하지 않았다. `attaches_to`에는 동점 규칙(아래 순위 ④)이 있으나 element 층위에는 대응이 없어, 두 실행이 각각 "최소 지배 노드"와 "원문 첫 번째 대상"을 골랐다. **2026-08-18 실측**: 이 한 자리가 `tree-edges`를 **0.5517**로 떨어뜨렸다 — 최상위 간선이 통째로 어긋나기 때문이다. 최소 지배 노드는 후보들 사이에서 **유일하게 결정되므로** 임의 선택이 아니다 |
| ⑦ | **전제부는 element가 아니다**(재정 2026-08-19 Q5 ① = ⓐ). 청구항의 첫 열거 도입까지의 문언(예: `A hardware accelerator comprising:` · 통주 3 CL-12의 실물 = `A method for performing a vector matrix multiplication (VMM) operation in a compute-in-memory (CIM) macro between a vector of activation values and a matrix of weight values, the method comprising:`)은 최상위 element들의 **부모 문언**이며 **그 자체를 element로 만들지 않는다.** **전제부에 한정 술어가 남아 있어도 마찬가지다** — 규약 ⑤의 판정법(걷어낸 뒤 한정 술어가 남으면 element)은 **열거 도중의 연결구**를 위한 것이고 전제부에는 적용하지 않는다 | 위 「청구항 `text_verbatim`의 경계 규약」이 적은 대로 `read.convergence`의 `tree-edges` 축은 **청구항 전문을 최상위 element의 부모 문언으로** 쓴다. 전제부를 element로 올리면 그 부모 문언 자체가 바뀌어 **최상위 간선이 통째로** 어긋난다 — 규약 ⑤·⑥이 막으려던 붕괴의 **더 큰 판**이다(⑥ 한 자리가 `tree-edges`를 0.5517로 떨어뜨렸다). **2026-08-19 실측**: 통주 3 레인이 CL-12에서 이 자리를 물어 왔다 — 규약 ⑤를 문자 그대로 적용하면 `for performing a vector matrix multiplication (VMM) operation …`이 한정 술어로 남아 전제부가 element가 되는데, §2 ①의 부모 문언 관례는 정반대를 명한다. **한정 술어 예외를 적지 않으면 규약 ⑤와 ⑦이 같은 자리에서 반대 답을 낸다** — ⑦의 둘째 문장이 그 충돌을 닫는다 |

> **[가설] 재검토 트리거 — 넓히지 말고 상신하라.** ⑦은 *전제부가 짧고 형식적이다*라는 가정 위에 서 있다. 전제부가 길고 **실질 한정을 여럿** 담은 실물(전제부 안에서 구성요소를 도입하고 그것을 다시 한정하는 형태)을 만나면, 레인은 **규약대로 비요소로 처리하고 그 사실을 상신한다.** 규약을 자의로 넓히지 마라 — 규약에 없는 처리를 레인이 보태면 그 순간 규약의 정본이 문서가 아니라 레인이 된다(D7). 그때의 경로는 **배치 리뷰 상신**이며, 재정은 같은 트리거를 규칙 파일의 `open_question`에도 남기라고 명했다(`reader/reader-rules.yaml` — 그쪽 소관).

**임계 0.95는 아직 재정되지 않았다**(`reader-rules.yaml#convergence.open_question`). 위 규약을 지킨 뒤에도 수렴하지 않는다면 그것은 네 잘못이 아니라 **절차 신호**이며, Owner에게 올라간다(SPEC §1.4). 억지로 맞추려고 다른 실행을 추측하지 마라 — 추측해서 맞춘 수렴은 아무것도 반증하지 못한다.

### 종속항 (`additions[]`)

- 각 addition은 `{id, attaches_to, text_verbatim, material_id}`.
- `id` 문법은 `CL-5/a1`.
- `attaches_to`는 **항상 독립항 element id**다. 종속의 종속이라도 최종적으로 독립항 element를 가리킨다 — 부가 한정은 골격 밑에 층위로 누적된다.

#### ★ `attaches_to` 선택 규약 (여럿이 그럴듯할 때)

여러 element가 후보일 때 무엇을 고르는지가 정해져 있지 않으면, 두 실행이 같은 독해를 하고도 `addition-attachment` 축이 떨어진다. 아래 순서로 **위에서부터** 적용해 첫 번째로 결정되는 것을 쓴다.

| 순위 | 규칙 |
|---|---|
| ① | 부가 한정이 **직접 수식·한정하는** element. 그 element의 문언이 부가 한정 안에 다시 등장하면 그것이 대상이다 |
| ② | 후보가 중첩 관계면 **더 깊은(더 구체적인) element**를 고른다. 층위 누적의 뜻이 그것이다 |
| ③ | 부가 한정이 **다른 종속항이 도입한 구조**를 다시 한정하면, 그 구조가 매달린 **독립항 element**를 고른다(계약이 addition을 부착점으로 허용하지 않으므로 여기서 층위 정보가 한 겹 소실된다 — 아래 미결) |
| ④ | 병렬한 여러 element에 **동시에** 걸리면, **후보 집합 안에서** 다른 후보 전부를 트리상 지배하는 element가 **유일하게 있으면 그것**을 고른다. 없으면 **원문 등장 순서상 첫 번째**를 고른다 |

- **`additions`는 비울 수 없다.** 전문이 있는 종속항을 빈 배열로 두면 "전 구성요소 3중 접지"가 접지할 것이 없어서 공허하게 통과한다.

#### ★ addition은 층위를 갖지 않는다 — 평면 분할로 쓴다 (재정 2026-08-19 Q5 ③ = 총괄 위임 · 처분 = 총괄)

상신된 논점은 **계약의 비대칭**이다 — element에는 있는 층위 표현(`children`)이 addition에는 없어, 내부에 후치 수식절을 든 종속항(통주 3의 CL-7·8·17)을 쪼갤 수 없다.

**처분은 비대칭을 유지하고 명문화하는 것이다.**

| # | 규약 | 이유 |
|---|---|---|
| ⓐ | **`additions`는 층위를 갖지 않는다.** `children`을 신설하지 않는다 | 아래 근거 셋 |
| ⓑ | **대신 평면 분할로 표현한다.** 종속항 안의 절이 **독립적 한정**을 가지면 **형제 addition으로 쪼갠다**(`CL-7/a1` · `CL-7/a2`) | 층을 만들 수 없다고 해서 한정을 뭉개라는 뜻이 아니다. 독립적 한정은 독립적 항목으로 선다 |
| ⓒ | 앞선 addition을 **한정하기만 하는 순수 수식절**은 그 addition의 `text_verbatim` 안에 **그대로 남긴다**. 쪼개지 않는다 | 쪼개면 아무것도 한정하지 않는 항목이 생긴다 — 경계 규약 ⑤가 element 층에서 막은 것과 같은 병이다 |

**근거 셋.**

- ⓐ **가리킬 좌표가 없다.** `attaches_to`의 값 공간은 **element id로 한정**되어 있고(SPEC §2.3) 그것은 계약이다. addition 내부에 층위를 만들어도 **그 층위를 가리킬 참조 좌표가 없다** — 층을 만들되 가리킬 수 없으면 그 층은 어떤 검사에도 보이지 않는다.
- ⓑ **`dependent-set`은 법이다.** 그 축은 `exact-match`(미달 = fail)이므로(재정 P-3) **입력 구조를 M1 종결 직전에 바꾸는 것은 감수 범위 밖의 새 표면을 만드는 일**이다. 서명은 `(text_verbatim, sorted(depends_on), dependency_type)` 3튜플이며(정본 = `reader/lib/convergence.py#_dependent_signatures`), addition 층위의 신설은 그 입력을 건드린다.
- ⓒ **표본이 셋뿐이다.** CL-7·8·17 세 건으로 계약을 바꾸는 것이 이 리포가 반복해서 경계해 온 **과적합**이다(어형 목록을 넓히지 않는 재정 Q1·Q5 ②와 같은 방향이다).

> **[가설] 재검토 트리거.** 평면 분할로 **표현할 수 없는** 실물 — 예컨대 하나의 수식절이 **두 addition을 동시에** 한정하는 형태 — 를 만나면 상신하라. 그때가 `children` 신설의 재정 경로가 열리는 시점이며, 그 전까지 총괄이 층위를 신설하면 그것은 재정 없는 계약 개정이다. 상신 경로는 **배치 리뷰**다.

### 종속 관계 (`depends_on` · `dependency_type`)

원문의 인용 어형을 그대로 읽는다.

| 원문 어형 | `depends_on` | `dependency_type` |
|---|---|---|
| `of claim 1` | `["CL-1"]` | `single` |
| `of claims 1 and 3` | `["CL-1", "CL-3"]` | `multiple-and` |
| `of claim 1 or claim 5` | `["CL-1", "CL-5"]` | `multiple-or` |
| `of claims 1 to 3` | `["CL-1","CL-2","CL-3"]` | `multiple-or` |
| `of any (one) of the preceding claims` | **이 청구항이 실제로 인용하는 선행 청구항**(선행 범위 밖 금지 · 빈 배열 금지) | `all-preceding` |

#### ★ `all-preceding` — 본문이 숫자를 말하지 않는 어형 (재정 2026-09-01 T11-ⓒ)

PCT 공보가 즐겨 쓰는 `any of the preceding claims` 계열이다. 위 표의 구 어형은 **전부 숫자를 요구**했기 때문에 이 어형이 규칙 밖이었고, WO2026-128750A1 부분 시험에서 그 한 자리가 `read.dependency-parse` 위반 15건 + `read.claim-inventory` 위반 15건(같은 15개를 원천 파서가 **독립항으로 오판**)을 냈다. 원장 = `docs/decisions/ruling-20260901-02-T11.md`.

**★ 기계는 `1..n-1`로 전개하지 않는다.** 본문이 숫자를 말하지 않는데 기계가 값을 만들면 그것은 **확인되지 않은 값을 정답지에 올리는 것**이다. 실물이 그 위험을 보인다 — 청구항 24는 `the operations comprising **the method** of any of the preceding claims`이고, 앞에 장치항이 섞여 있으면 "the method of"가 **방법항만** 가리킨다. 일괄 전개하면 장치항까지 인용한 것으로 **기계가 주장**한다.

**그러므로 `depends_on`을 채우는 것은 너다.** 검사(`parse.preceding-subset`)가 보는 것은 둘뿐이다.

| | 판정 |
|---|---|
| **통과** | `depends_on`이 `{CL-1 … CL-(n-1)}`의 **부분집합**이고 **비어 있지 않다** |
| **실패** | 선행 범위 **밖**의 번호가 하나라도 있다(자기 자신 · 후행 청구항 포함), 또는 **빈 배열** |

- 이 종속항들은 `unclassified`와 달리 **판정 대상에 그대로 남는다**(`checked`에 포함된다). 표지가 아니라 어형이다.
- **판단이 서지 않는 자리는 규약을 자의로 넓히지 말고 상신하라**(경로 = 배치 리뷰). 특히 **카테고리 전환형**(장치·매체·프로그램 청구항이 `the method of any of the preceding claims`로 방법항을 되받는 형태)에서 이 어형과 아래 `unclassified` 표지가 **같은 청구항에 동시에 해당**한다 — **그 우선순위는 재정 2026-09-01 T13이 정했다: `all-preceding`이 이긴다.** 아래 `unclassified` 절의 ★ 문단이 그 정본이다.

#### ★ `unclassified` — 구조 미분류 표지 (재정 P-A 계열 P-1)

Markush(`selected from the group consisting of …`)·조건부(**명확 구문만** — `in response to`·`only if` 등)·수단항(`means for`·`step for`)·**카테고리 전환**(인용 대상과 청구 카테고리가 갈리는 종속) 넷은 **본문의 구조**가 위 4어형 체계 밖이다. 이 넷을 만나면 `dependency_type: "unclassified"`를 선언한다.

**★ 카테고리 전환이 선행 청구항 전부를 인용하면 `all-preceding`이 이긴다**(재정 2026-09-01 **T13**). 장치·매체·컴퓨터프로그램제품 청구항이 `the operations comprising the method of any of the preceding claims`처럼 적혀 있으면 `dependency_type`은 **`all-preceding`**이다 — `unclassified`를 쓰지 마라.

- **왜인가.** 미분류는 **인용을 읽지 못하는** 구조를 위한 표지인데(위 문단의 "판정 대상에 남기면 규칙의 공백이 실제 결함과 같은 모양으로 계상된다"), 이 인용은 재정 T11-ⓒ 이후 **읽힌다.** 읽히는 인용에 미분류를 붙이면 `depends_on`이 아무 검사도 받지 않게 된다.
- **잃는 것을 적어 둔다.** 이 셋은 CP1의 미분류 목록에 오르지 않는다. 다만 잃는 것은 **태그이지 정보가 아니다** — 전문은 `text_verbatim`에 남고 판독본이 청구항을 싣는다.
- **강제되지 않는다.** 구조 표지가 있는데 미분류를 선언하지 **않은** 것을 잡는 검사는 없다(역방향 가드 부재 — Markush도 같다). 이 지침은 문서 지침이며, 강제 범위를 실제보다 넓게 말하지 않기 위해 그 사실을 함께 적는다.

**★ 조건부는 명확 구문으로만 인정한다 — 맨 `when`·`if`는 표지가 아니다**(재정 2026-08-19 Q5 ② = ⓑ). 위 괄호의 둘은 **대표 예**일 뿐이며 **목록의 정본은 `reader/reader-rules.yaml#dependency_citation.unclassified.structure_markers`다** — 이 문서에 목록을 복제하지 않는다(사본은 반드시 낡는다).

- **★ 귀결을 숨기지 않는다.** 목록이 좁아지면 회피 통로도 좁아지지만 **정직한 미분류 선언이 벌받을 여지가 는다** — 조건부 종속인데 명확 구문이 하나도 없으면 `unclassified` 선언이 `parse.unclassified-not-an-escape`에 걸린다. 그때 레인은 **집행 가능한 선언(`single` 등)을 하고 그 사실을 상신한다.** 검사를 통과시키려 **답을 고치는 것이 아니라 답을 고를 수 없었다는 사실을 기록**하는 것이며, 이 리포는 이미 Markush 자리에서 같은 규율을 세웠다(SPEC §9.33 ③ — 통주 레인이 `single`을 선언하고 상신했고, 그것을 "레인의 오분류"로 읽으면 다음 레인은 상신 대신 침묵을 배운다).
- **[가설] 재검토 트리거.** 명확 구문 없는 실물 조건부 종속항을 만나면 **어형을 자의로 넓히지 말고 그 실물을 상신하라**(경로 = 배치 리뷰. 규칙 파일의 `legislation_path`가 같은 것을 명한다).

**★ 판정 기준은 인용 어형이 아니라 본문 구조다.** Markush 종속항도 인용부는 대개 `of claim 1`로 평범하게 읽힌다 — 그래도 `unclassified`가 맞다. 표지가 가리키는 것은 "어느 청구항을 인용하는가"(그것은 `depends_on`이 담는다)가 아니라 **"이 종속항의 한정이 어떤 구조인가"**이며, 그 구조를 읽는 typed operator가 아직 입법되지 않았다는 사실이다(재정 P-1 — 입법은 실물 축적 시 건별 재정).

- 전문(`text_verbatim`)은 **이미 보존된다**(재정 R1). 표지는 손실을 만들지 않는다 — 나중에 typed operator가 입법되면 전문에서 다시 읽으면 된다.
- `unclassified`를 선언한 종속항은 `read.dependency-parse`의 **판정 대상에서 빠지고**, 판정 행에 별도로 계수되며, **CP1의 미분류 목록에 전건 노출**된다.
- **회피 통로로 쓰지 마라.** 본문에 **구조 표지 어형이 하나도 없는데** `unclassified`를 선언하면 검사가 그것을 잡아 **실패**시킨다(`parse.unclassified-not-an-escape`). 표지 어형 목록의 정본은 `reader/reader-rules.yaml#dependency_citation.unclassified.structure_markers`이며 `[가설]` 태그가 붙어 있다 — 실물이 쌓이면 재정으로 교정된다. 표지는 규칙이 못 읽는 구조를 위한 것이지 읽기 귀찮은 구조를 위한 것이 아니다.
- `depends_on`은 **여전히 채운다.** 어느 청구항을 인용하는지는 미분류 구조에서도 읽을 수 있고, 그것이 트리의 뿌리를 정한다.

## 3. component 항목 만들기

element·addition 하나마다 `kind: "component"` 항목을 **1:1로** 만든다.

```json
{ "id": "M1", "kind": "component", "status": "active", "superseded_by": null,
  "claim_ref": "CL-1/e1", "label_en": "substrate having a first surface",
  "text_verbatim": "a substrate having a first surface" }
```

- `claim_ref`는 자기를 가리킨 element·addition의 id와 **역방향으로 일치**해야 한다.
- 두 element가 같은 component 항목을 공유할 수 없다. 공유하면 접지 1건이 둘을 덮는다.
- `label_en`은 EN이다. 한글이 한 글자라도 들어가면 거부된다.

## 4. 출원인 관심 신호 (`applicant_interest`)

권리 관심이 어디에 걸려 있는지를 `kind: "implication"` 항목으로 만들고, `claims.applicant_interest[]`가 그것을 가리킨다.

**이 단계에서는 언제나 빈 배열이다.** 재량이 아니라 구조다 — ⓐ 이 요청의 `items[]`는 `kind: "component"`로 한정되고 ⓑ 스키마는 `applicant_interest[].material_id`가 `implication` 항목을 가리킬 것을 요구하며 ⓒ `read.pointer-resolve`의 kind 제약이 그것을 집행한다. 따라서 decompose 레인이 이 배열을 채울 방법은 없다. 채우려 하면 포인터 해소가 실패한다.

## 5. 맹검 스크리닝 메모 (D4 1단 — 재정 P-A · P-U4)

분해 직후, 이 소재가 일반 독자에게 **"아, 그렇구나"의 안도감**을 줄 수 있는지 1차 판단해 `screening_memo`를 낸다.

```json
{ "direction": "clear", "reason": "권리 관심이 한 구성에 뚜렷하고 …" }
```

- `direction`은 `clear`(서사가 설 것 같다) 또는 `concern`(서지 않을 것 같다). `reason`은 **KR**이다(값 언어 EN 정책의 예외 중 하나).
- 서식은 **스크리닝 판단 기록형**이다 — 판단 방향 하나 + 근거 요지 하나. 장문의 서사 기획을 쓰는 자리가 아니다.

**★ 이 메모는 상신이 아니다(재정 P-A).** 조기 판단은 **기록만** 하고 러너는 계속 진행한다. drop의 구속력 있는 결정은 **체크포인트 1에서 재료 승인과 한 자리**로 내려진다 — 부분 정보 위에서 두 번 판단하는 것보다 완전한 정보 위에서 한 번 판단하는 편이 낫다.

**★ 그러므로 부담 없이 적어라.** 네 메모가 런을 죽이지 않는다. `concern`을 적는 데 드는 비용은 0이고, 적지 않아 잃는 것은 신호다.

**★ 이 메모는 최종 서사 평가 레인(`synthesize`)에 전달되지 않는다.** 앵커링 방지이며, 두 판단이 독립이어야 축적물이 의미를 갖는다. 그리고 `read-a`·`read-b`가 **각자** 쓴 메모 둘이 CP1에 **나란히** 제시된다 — 두 독립 관찰의 일치/불일치 자체가 신호이기 때문이다(재정 P-U4).

**왜 이것을 남기는가.** 청구항만 본 맹검 판단 · 접지 후 최종 평가 · Owner 재정, 세 층이 함께 쌓인다. 그 축적물이 자매 프로젝트 patent-historian의 **스크리닝 능력에 대한 사전 훈련 데이터**다(헌장 D4).

## 6. 산출 형태

`40-output-contract.md`의 `decompose` 절을 그대로 따른다. 필수 최상위 키는 `claims` · `items` · `screening_memo` 셋이다.
