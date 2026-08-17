# 레인 요청 — read-b/decompose/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `read-b` |
| 작업 | `decompose` |
| 모델 | `opus-5` |
| effort | `max` |
| 배치 | `0` |
| 절차 문서 | `reader/procedure/10-decompose.md` |

**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는
`{"lane_id": ..., "model": ..., "effort": ..., "payload": {...}}` 이고,
`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가
레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 `request.json` 의
`response_schema` 를 통과해야 하며, 위반은 응답 자체가 거부된다.

## 이 요청의 지시

청구항 구간 전량을 분해한다. 원천에 있는 **모든** 청구항이 대상이며, 하나라도 빠지면
`read.claim-inventory` 가 잡는다. 산출은 `claims`(독립·종속·출원인 관심)과
`items`(kind: component) 와 조기 `drop_signal` 이다.
이 요청은 독립 실행 `read-b` 의 것이며, 다른 실행의 산출을 보지 않는다.

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

### 종속항 (`additions[]`)

- 각 addition은 `{id, attaches_to, text_verbatim, material_id}`.
- `id` 문법은 `CL-5/a1`.
- `attaches_to`는 **항상 독립항 element id**다. 종속의 종속이라도 최종적으로 독립항 element를 가리킨다 — 부가 한정은 골격 밑에 층위로 누적된다.
- **`additions`는 비울 수 없다.** 전문이 있는 종속항을 빈 배열로 두면 "전 구성요소 3중 접지"가 접지할 것이 없어서 공허하게 통과한다.

### 종속 관계 (`depends_on` · `dependency_type`)

원문의 인용 어형을 그대로 읽는다.

| 원문 어형 | `depends_on` | `dependency_type` |
|---|---|---|
| `of claim 1` | `["CL-1"]` | `single` |
| `of claims 1 and 3` | `["CL-1", "CL-3"]` | `multiple-and` |
| `of claim 1 or claim 5` | `["CL-1", "CL-5"]` | `multiple-or` |
| `of claims 1 to 3` | `["CL-1","CL-2","CL-3"]` | `multiple-or` |

★ `alternative-form`은 **선언하지 마라.** 현행 파싱 규칙 5종은 그 값에 도달하지 못하며, 선언하면 `read.dependency-parse`가 반드시 실패한다(그것이 지금의 정직한 처리다 — 신설은 재정 사항).

## 3. component 항목 만들기

element·addition 하나마다 `kind: "component"` 항목을 **1:1로** 만든다.

```json
{ "id": "M1", "kind": "component", "status": "active", "superseded_by": null,
  "claim_ref": "CL-1/e1", "label_en": "substrate having a first surface",
  "text_verbatim": "a substrate having a first surface;" }
```

- `claim_ref`는 자기를 가리킨 element·addition의 id와 **역방향으로 일치**해야 한다.
- 두 element가 같은 component 항목을 공유할 수 없다. 공유하면 접지 1건이 둘을 덮는다.
- `label_en`은 EN이다. 한글이 한 글자라도 들어가면 거부된다.

## 4. 출원인 관심 신호 (`applicant_interest`)

권리 관심이 어디에 걸려 있는지를 `kind: "implication"` 항목으로 만들고, `claims.applicant_interest[]`가 그것을 가리킨다. 이 단계에서 함의 항목을 만들지 못하겠으면 **빈 배열로 둔다** — 지어내지 않는다. (④단계가 함의를 낸다.)

## 5. 조기 drop 신호 (D4 1단)

분해 직후, 이 소재가 일반 독자에게 **"아, 그렇구나"의 안도감**을 줄 수 있는지 1차 판단해 `drop_signal`을 낸다.

```json
{ "stage": "early", "verdict": "go", "reason": "권리 관심이 한 구성에 뚜렷하고 …" }
```

- `verdict`는 `go` 또는 `drop-proposed`. `reason`은 **KR**이다(값 언어 EN 정책의 예외 2곳 중 하나).
- `drop-proposed`를 내면 러너는 **그 자리에서 멈추고** 접지·통합을 돌리지 않는다. 비용 절약이 아니라, 하류 산출물이 Owner의 판단을 오염시키는 것을 막기 위함이다.
- 판단이 서지 않으면 `go`다. drop 제안은 **적극적 주장**이며 사유를 적을 수 있을 때만 낸다.

## 6. 산출 형태

`40-output-contract.md`의 `decompose` 절을 그대로 따른다. 필수 최상위 키는 `claims` · `items` · `drop_signal` 셋이다.
