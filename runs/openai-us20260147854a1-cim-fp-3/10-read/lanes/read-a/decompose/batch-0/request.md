# 레인 요청 — read-a/decompose/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `read-a` |
| 작업 | `decompose` |
| 모델 | `opus-5` |
| effort | `max` |
| 배치 | `0` |
| 절차 문서 | `reader/procedure/10-decompose.md` |
| 입력 지문 | `d7f06c70ae76b7a044c7110f4daa2d44f8946e4b359d600a0e775636559d00e2` |

**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는
`{"lane_id": ..., "model": ..., "effort": ..., "input_digest": ..., "payload": {...}}` 이고,
`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가
레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 `request.json` 의
`response_schema` 를 통과해야 하며, 위반은 응답 자체가 거부된다.

**★ 입력 지문 반향(필수 · 재정 P-12).** `input_digest` 에는 위 표의 값을
**그대로** 적는다. 계산하지 말고 옮겨 적어라 — 이 값은 네가 실제로 읽은 요청이
어느 판이었는지를 가리키는 시점 표지다. 요청이 갱신되면 지문이 바뀌므로, 옛
응답을 그대로 두면 러너가 그것을 **낡은 응답으로 거부한다**. 지문이 다르거나
빠진 응답은 소비되지 않으며, 거부 사실은 레인 기록에 남는다.

## 이 요청의 지시

청구항 구간 전량을 분해한다. 원천에 있는 **모든** 청구항이 대상이며, 하나라도 빠지면
`read.claim-inventory` 가 잡는다. 산출은 `claims`(독립·종속·출원인 관심)과
`items`(kind: component) 와 `screening_memo` 다.
맹검 스크리닝 메모는 **상신이 아니다** — 기록만 하며 네 메모가 런을 세우지 않는다(재정 P-A). 판단 방향(`clear`·`concern`) 하나와 근거 요지(KR) 하나를 적는다.
이 요청은 독립 실행 `read-a` 의 것이며, 다른 실행의 산출을 보지 않는다.

## 원천 조각

### `bibliographic-head`

```text
United States
Patent Application Publication: 20260147854
Kind Code: A1
Publication Date: May 28, 2026
Inventor(s): Cakir; Cagla et al.

## FLOATING POINT MULTIPLICATIONS

### Abstract

Systems, apparatuses, and methods are disclosed for improved matrix-vector operations in accelerators that may be useful or heavy AI training and inference workloads. The disclosed technology provides arrangements that permit more efficient computation by, for example, performing calculations without repeated conversion between numeric domains. In some implementations, a compute-in-memory (CIM) macro is configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values, and a mode decoding unit is configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values. A column cell of the CIM macro can be configured to output a product between an activation value and a weight value using a half adder and multiple multiplexers that provide selections to a full adder based on control signals.

Inventors: 

**Cakir; Cagla** (San Francisco, CA), **Erbagci; Burak** (San Jose, CA), **Conklin; Alexander Almela** (San Jose, CA), **DellaRova; Tracey** (Wake Forest, NC), **Fouda; Mohammed Elneanaei Abdelmoneem** (Irvine, CA), **Allegrucci; Jean-Didier** (Sunnyvale, CA)

Applicant: 

**OpenAI Opco, LLC** (San Francisco, CA)

Family ID: 

99885146

Assignee: 

**OpenAI Opco, LLC** (San Francisco, CA)

Appl. No.: 

[19/397827](tel:19/397827)

Filed: 

November 21, 2025

### Related U.S. Application Data

us-provisional-application US [63724151 20241122](tel:63724151 20241122)  
us-provisional-application US [63724153 20241122](tel:63724153 20241122)  
us-provisional-application US [63724157 20241122](tel:63724157 20241122)  
us-provisional-application US [63724161 20241122](tel:63724161 20241122)  

### Publication Classification

Int. Cl.:

**G06F17/16** (20060101)

U.S. Cl.:

CPC

**G06F17/16** (20130101); 

### Background/Summary

FIELD OF DISCLOSURE  
```

### `claims-section`

```text
**1**. A hardware accelerator comprising: a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein a column cell of the CIM macro is configured to output a primitive product between an activation value and a weight value and comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer and the third multiplexer perform respective selections based on control signals according to the arithmetic mode.   
**2**. The hardware accelerator according to claim 1, wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder.   
**3**. The hardware accelerator according to claim 1, wherein the column cell further comprises a plurality of memory cells configured to store the weight value.   
**4**. The hardware accelerator according to claim 3, wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder.   
**5**. The hardware accelerator according to claim 3, wherein: one of the plurality of memory cells comprises a first bitcell and a second bitcell, and the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline.   
**6**. The hardware accelerator according to claim 5, wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines.   
**7**. The hardware accelerator according to claim 5, wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value.   
**8**. The hardware accelerator according to claim 7, wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value.   
**9**. The hardware accelerator according to claim 8, wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder.   
**10**. The hardware accelerator according to claim 1, wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5.   
**11**. The hardware accelerator according to claim 1, wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5.   
**12**. A method for performing a vector matrix multiplication (VMM) operation in a compute-in-memory (CIM) macro between a vector of activation values and a matrix of weight values, the method comprising: adding, by a half adder in a column cell of the CIM macro, an exponent bit of an activation value and an exponent bit of a weight value to output a carry-out bit and a sum bit; selecting, by a first multiplexer in the column cell, zero or a prior stage carry-out bit from a prior stage half adder to output a first selection to a full adder; selecting, by a second multiplexer in the column cell, zero or the sum bit to output a second selection to the full adder; selecting, by a third multiplexer in the column cell, zero or a carry-in bit from a prior stage full adder to output a third selection to the full adder; and outputting an exponent bit of a primitive product between the activation value and the weight value.   
**13**. The method according to claim 12, further comprising: controlling the selections performed by the first multiplexer, the second multiplexer, and the third multiplexer based on control signals according to an arithmetic mode of the VMM operation.   
**14**. The method according to claim 13, further comprising: determining the arithmetic mode based on a first floating point format of the activation value and a second floating point format of the weight value.   
**15**. The method according to claim 12, further comprising: selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder; and outputting, by the fourth multiplexer in the column cell, an exponent bit of the primitive product.   
**16**. The method according to claim 12, further comprising: providing, by a first bitcell in the column cell, the exponent bit of the weight value to the half adder.   
**17**. The method according to claim 16, further comprising: writing, concurrently, a further exponent bit of a further weight value to a second bitcell in the column cell, wherein the further weight value is different from the weight value.   
**18**. The method according to claim 17, further comprising: writing the further exponent bit to the second bitcell through a bitline shared with the first bitcell.   
**19**. The method according to claim 12, wherein: a number of exponent bits in the activation value is at least one of 2, 3, 4, or 5; a number of exponent bits in the weight value is at least one of 2, 3, 4, or 5; and the method further comprises determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value.   
**20**. A system comprising: a compute device configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode device configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein the compute device comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer, and the third multiplexer perform respective selections based on control signals according to the mode.
```

## 절차 (정본 = reader/procedure/10-decompose.md)

# D5 ①② — 청구항 구성요소 전 분해 + 관계 트리

**너의 작업(`decompose`).** 청구항 구간 전량을 읽고, 각 청구항을 구성요소 단위로 **전부** 분해한다. 요약하지 않는다. 고르지 않는다. **전 분해**는 문언 그대로다.

받는 조각은 둘이다 — `claims-section`(청구항 구간 전문)과 `bibliographic-head`(서지 머리). 명세서 본문은 이 단계에서 주지 않는다. 분해는 청구항의 일이고, 본문을 함께 보면 분해가 요약으로 미끄러진다.

---

## 1. 청구항 하나도 빠뜨리지 않는다

원천 청구항 목록은 러너가 별도로 파싱해 **양방향으로 대조**한다(`read.claim-inventory`). 하나가 빠지면 남은 것들이 아무리 잘 접지되어 있어도 실패한다. 취소 청구항(`(canceled)`)은 등재 의무에서 면제된다.

- 독립항 → `claims.independent[]`, 종속항 → `claims.dependents[]`. 이 분류는 **원문이 다른 청구항을 인용하는가**로 결정된다. 인용하면 종속항이다.
- 청구항 ID는 `CL-<원천 번호>`다. 번호를 다시 매기지 않는다.

## 2. 구성요소 분해

### 독립항 (`elements[]`)

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

> **규약 ⑤·⑥은 2026-08-18 실특허 통주의 처분이다.** 두 독립 실행이 같은 청구항 20개를 같은 구조(독립 3·종속 17)로 읽었고 종속항 서명은 **완전히 일치**(1.0)했는데, 갈린 것은 위 두 자리뿐이었다. **둘 다 규약이 답을 갖지 않은 자리였고 두 실행 다 규율을 어기지 않았다.** 그러므로 이것은 검사를 고칠 일이 아니라 **절차를 고정할 일**이다(D6 규율 ③ — 결정론은 절차 고정 + 산출물 형식 구조화 + 검증 기계화에 산다). 같은 형태의 처분이 직전 라운드에도 있었다(규약 ①~④, 그때 실측은 0.59였다).

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
| ④ | 병렬한 여러 element에 **동시에** 걸리면 **원문 등장 순서상 첫 번째**를 고른다. 임의 선택을 금지하는 것이 목적이며, 첫 번째라는 것 자체에 의미는 없다 |

> **미결(재정 상신 대상).** ③은 정보 손실을 감수하는 규약이다. 종속항이 만든 구조를 다시 한정하는 부가 한정의 **참된 부착점은 addition**인데 계약은 `attaches_to`의 값 공간을 element로 한정한다(SPEC §2.3). 그리고 `read.convergence`의 `addition-attachment` 축은 **바로 이 미규정 구간을 재고 있다** — 그 축이 떨어지는 것이 "특허 독해가 재현되지 않았다"를 뜻하지 않을 수 있다. 임계 재정 시 이 구분을 함께 올린다.
- **`additions`는 비울 수 없다.** 전문이 있는 종속항을 빈 배열로 두면 "전 구성요소 3중 접지"가 접지할 것이 없어서 공허하게 통과한다.

### 종속 관계 (`depends_on` · `dependency_type`)

원문의 인용 어형을 그대로 읽는다.

| 원문 어형 | `depends_on` | `dependency_type` |
|---|---|---|
| `of claim 1` | `["CL-1"]` | `single` |
| `of claims 1 and 3` | `["CL-1", "CL-3"]` | `multiple-and` |
| `of claim 1 or claim 5` | `["CL-1", "CL-5"]` | `multiple-or` |
| `of claims 1 to 3` | `["CL-1","CL-2","CL-3"]` | `multiple-or` |

#### ★ `unclassified` — 구조 미분류 표지 (재정 P-A 계열 P-1)

Markush(`selected from the group consisting of …`)·조건부(`if`·`when`·`in response to`)·수단항(`means for`·`step for`)·**카테고리 전환**(인용 대상과 청구 카테고리가 갈리는 종속) 넷은 **본문의 구조**가 위 4어형 체계 밖이다. 이 넷을 만나면 `dependency_type: "unclassified"`를 선언한다.

**★ 판정 기준은 인용 어형이 아니라 본문 구조다.** Markush 종속항도 인용부는 대개 `of claim 1`로 평범하게 읽힌다 — 그래도 `unclassified`가 맞다. 표지가 가리키는 것은 "어느 청구항을 인용하는가"(그것은 `depends_on`이 담는다)가 아니라 **"이 종속항의 한정이 어떤 구조인가"**이며, 그 구조를 읽는 typed operator가 아직 입법되지 않았다는 사실이다(재정 P-1 — 입법은 실물 축적 시 건별 재정).

- 전문(`text_verbatim`)은 **이미 보존된다**(재정 R1). 표지는 손실을 만들지 않는다 — 나중에 typed operator가 입법되면 전문에서 다시 읽으면 된다.
- `unclassified`를 선언한 종속항은 `read.dependency-parse`의 **판정 대상에서 빠지고**, 판정 행에 별도로 계수되며, **CP1의 미분류 목록에 전건 노출**된다.
- **회피 통로로 쓰지 마라.** 본문에 **구조 표지 어형이 하나도 없는데** `unclassified`를 선언하면 검사가 그것을 잡아 **실패**시킨다(`parse.unclassified-not-an-escape`). 표지 어형 목록의 정본은 `reader/reader-rules.yaml#dependency_citation.unclassified.structure_markers`이며 `[가설]` 태그가 붙어 있다 — 실물이 쌓이면 재정으로 교정된다. 표지는 규칙이 못 읽는 구조를 위한 것이지 읽기 귀찮은 구조를 위한 것이 아니다.
- `depends_on`은 **여전히 채운다.** 어느 청구항을 인용하는지는 미분류 구조에서도 읽을 수 있고, 그것이 트리의 뿌리를 정한다.

★ `alternative-form`은 **폐기되었다**(재정 P-1이 `unclassified`로 흡수). 선언하면 스키마가 거부한다.

## 3. component 항목 만들기

element·addition 하나마다 `kind: "component"` 항목을 **1:1로** 만든다.

```json
{ "id": "M1", "kind": "component", "status": "active", "superseded_by": null,
  "claim_ref": "CL-1/e1", "label_en": "substrate having a first surface",
  "text_verbatim": "a substrate having a first surface" }
```

> **★ 예시가 §2 규약과 싸우던 자리다(2026-08-18 통주 실측 · 두 레인이 독립으로 지적).** 구 예시는 `text_verbatim` 에 끝 구분자 `;` 를 포함했는데, 그것은 §2 경계 규약 ③(끝 구분자는 element 에 포함하지 않는다)의 **정확한 반례**였다. 레인은 규약과 예시가 갈리면 어느 쪽을 따를지 스스로 정해야 했고, 그 선택이 갈리면 수렴이 깨진다. **예시는 규약의 사본이며, 사본은 반드시 낡는다** — 규약을 고칠 때 이 블록을 함께 고쳐라.

- `claim_ref`는 자기를 가리킨 element·addition의 id와 **역방향으로 일치**해야 한다.
- 두 element가 같은 component 항목을 공유할 수 없다. 공유하면 접지 1건이 둘을 덮는다.
- `label_en`은 EN이다. 한글이 한 글자라도 들어가면 거부된다.

## 4. 출원인 관심 신호 (`applicant_interest`)

권리 관심이 어디에 걸려 있는지를 `kind: "implication"` 항목으로 만들고, `claims.applicant_interest[]`가 그것을 가리킨다.

**이 단계에서는 언제나 빈 배열이다.** 재량이 아니라 구조다 — ⓐ 이 요청의 `items[]`는 `kind: "component"`로 한정되고 ⓑ 스키마는 `applicant_interest[].material_id`가 `implication` 항목을 가리킬 것을 요구하며 ⓒ `read.pointer-resolve`의 kind 제약이 그것을 집행한다. 따라서 decompose 레인이 이 배열을 채울 방법은 없다. 채우려 하면 포인터 해소가 실패한다.

> 구 문언은 "만들지 못하겠으면 빈 배열로 둔다"는 **재량 어법**이었고, 그것은 D5가 관심 신호를 ①단계 산출로 열거한 것과 실제 계약 사이의 어긋남을 가렸다(2026-08-18 실특허 스모크에서 레인이 지적). 할 수 없는 일을 "못 하겠으면"이라고 적으면, 레인은 자기가 게으른 줄 안다. 관심 신호의 실제 산출 단계는 ④(`synthesize`)다.

## 5. 맹검 스크리닝 메모 (D4 1단 — 재정 P-A · P-U4)

분해 직후, 이 소재가 일반 독자에게 **"아, 그렇구나"의 안도감**을 줄 수 있는지 1차 판단해 `screening_memo`를 낸다.

```json
{ "direction": "clear", "reason": "권리 관심이 한 구성에 뚜렷하고 …" }
```

- `direction`은 `clear`(서사가 설 것 같다) 또는 `concern`(서지 않을 것 같다). `reason`은 **KR**이다(값 언어 EN 정책의 예외 중 하나).
- 서식은 **스크리닝 판단 기록형**이다 — 판단 방향 하나 + 근거 요지 하나. 장문의 서사 기획을 쓰는 자리가 아니다.

**★ 이 메모는 상신이 아니다(재정 P-A).** 구 규정은 조기 `drop-proposed`를 즉시 `escalate`로 처리해 파이프라인을 세웠다. **그 경로는 폐지되었다.** 이제 조기 판단은 **기록만** 하고 러너는 계속 진행하며, drop의 구속력 있는 결정은 **체크포인트 1에서 재료 승인과 한 자리**로 내려진다. 부분 정보 위에서 두 번 판단하는 것보다 완전한 정보 위에서 한 번 판단하는 편이 낫다.

**★ 그러므로 부담 없이 적어라.** 네 메모가 런을 죽이지 않는다. `concern`을 적는 데 드는 비용은 0이고, 적지 않아 잃는 것은 신호다.

**★ 이 메모는 최종 서사 평가 레인(`synthesize`)에 전달되지 않는다.** 앵커링 방지이며, 두 판단이 독립이어야 축적물이 의미를 갖는다. 그리고 `read-a`·`read-b`가 **각자** 쓴 메모 둘이 CP1에 **나란히** 제시된다 — 두 독립 관찰의 일치/불일치 자체가 신호이기 때문이다(재정 P-U4).

**왜 이것을 남기는가.** 청구항만 본 맹검 판단 · 접지 후 최종 평가 · Owner 재정, 세 층이 함께 쌓인다. 그 축적물이 자매 프로젝트 patent-historian의 **스크리닝 능력에 대한 사전 훈련 데이터**다(헌장 D4).

## 6. 산출 형태

`40-output-contract.md`의 `decompose` 절을 그대로 따른다. 필수 최상위 키는 `claims` · `items` · `screening_memo` 셋이다.
