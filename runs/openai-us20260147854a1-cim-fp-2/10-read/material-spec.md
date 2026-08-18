# CP1 판독본 (KR 틀 · EN 값) — `openai-us20260147854a1-cim-fp-2` (판 1)

상태 `draft` · 스키마 `material-spec/v0` · reader `0.5.0`

이 문서는 `10-read/material-spec.json` 의 **결정론 렌더**다. 기계 정본은 JSON 이고,
판정의 표면은 이 문서다. 렌더가 항목을 빠뜨리면 `freeze.render-parity` 가 잡는다.

## 0. 체크포인트 1 — 무엇을 판정하는가

> 이 재료만 읽고 이 특허가 무엇을 하는 물건인지, 그리고 투자자-팬의 어떤 질문에 답할 수 있는지 말할 수 있는가? 말할 수 없다면 어느 항목이 비었는지 지적하라.

### 승인 봉투 작성 안내

- 봉투 경로: `15-frozen/approval-v<N>.md` (프런트매터가 `approval-envelope/v0` 의 대상이다)
- 공통 필수 필드: `schema`, `checkpoint`, `run_id`, `target`, `decision`, `owner_quote`, `quote_provenance`, `decided_at`, `recorded_by`
- CP1 승인 추가 필수: `manual_verification_ack`, `derived_fact_ack`, `numeric_whitelist_printed`
- `target.digest` 는 승인 시점 대상 파일의 SHA-256 이다. 승인 후 재료가 바뀌면
  봉투는 **자동 실효**되고 `freeze` 가 `halt` 한다(재정 R8).
- `owner_quote` 는 Owner 가 **실제로 타이핑한 원문**이다. 시스템 요약의 인용은 무효다.
- 결정은 이진이다 — `approved` / `rejected`. **조건부 승인 제도는 없다.**
- `manual_verification_ack[]` 는 아래 §7 목록과, `derived_fact_ack[]` 는 §6.2 목록과
  **정확히 일치**해야 한다(`freeze.approval-valid`). 빈 목록·유령 ID 는 승인이 아니라 서명이다.
- **작업 레인은 봉투를 쓰지 않는다.** 봉투는 오케스트레이터가 Owner 응답 후 기록한다(SPEC §1.2 C3).
- 무응답은 무기한 대기다. 시간 초과 자동 진행 경로는 없다(재정 R8).

## 1. 특허

| 항목 | 값 |
|---|---|
| 번호 | US20260147854A1 |
| 제목 | FLOATING POINT MULTIPLICATIONS |
| 관할 · 공보 종별 | `US` · `A1` |
| 출원인 (런 ID 유래 단수) | OpenAI Opco, LLC |
| 출원인 목록 | OpenAI Opco, LLC |
| 발명자 목록 | Cakir; Cagla · Erbagci; Burak · Conklin; Alexander Almela · DellaRova; Tracey · Fouda; Mohammed Elneanaei Abdelmoneem · Allegrucci; Jean-Didier |
| 날짜 | 우선 2024-11-22 · 출원 2025-11-21 · 공개 2026-05-28 |
| 우선권 주장 1 | 63724151 · 2024-11-22 · `US` |
| 우선권 주장 2 | 63724153 · 2024-11-22 · `US` |
| 우선권 주장 3 | 63724157 · 2024-11-22 · `US` |
| 우선권 주장 4 | 63724161 · 2024-11-22 · `US` |
| 분류 IPC | G06F17/16 |
| 분류 CPC | G06F17/16 |
| 원천 | `00-source/patent.md` |
| 원천 다이제스트 | `sha256:40f1905b78c990134f5b115a268ed8d0658438da8bbfd4f03970c4132cbd12d5` |

**최우선일 대조** — `dates.priority` 2024-11-22 ↔ 우선권 목록 최소 2024-11-22 → 일치

이 대조는 `read.bibliography#bib.earliest-priority` 가 산식으로 이미 판정했다.
여기 다시 놓는 이유는 CP1 이 **기계가 무엇을 보증했는가**를 사람이 재확인하는
자리이기 때문이다(C18 최우선일의 정확성 요건 — 재정 P-2 ⓐ).

## 2. 청구항 골격 (D5 ① 전 분해 · ② 관계 트리)

### 독립항 `CL-1`

> A hardware accelerator comprising: a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein a column cell of the CIM macro is configured to output a primitive product between an activation value and a weight value and comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer and the third multiplexer perform respective selections based on control signals according to the arithmetic mode.

- `CL-1/e1` → **M1** — a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values
- `CL-1/e2` → **M2** — a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values
  - `CL-1/e2/e1` → **M3** — the first floating point format and the second floating point format being flexible
- `CL-1/e3` → **M4** — wherein a column cell of the CIM macro is configured to output a primitive product between an activation value and a weight value and comprises:
  - `CL-1/e3/e1` → **M5** — a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit
  - `CL-1/e3/e2` → **M6** — a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder
  - `CL-1/e3/e3` → **M7** — a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder
  - `CL-1/e3/e4` → **M8** — a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder
  - `CL-1/e3/e5` → **M9** — wherein the first multiplexer, the second multiplexer and the third multiplexer perform respective selections based on control signals according to the arithmetic mode

### 독립항 `CL-12`

> A method for performing a vector matrix multiplication (VMM) operation in a compute-in-memory (CIM) macro between a vector of activation values and a matrix of weight values, the method comprising: adding, by a half adder in a column cell of the CIM macro, an exponent bit of an activation value and an exponent bit of a weight value to output a carry-out bit and a sum bit; selecting, by a first multiplexer in the column cell, zero or a prior stage carry-out bit from a prior stage half adder to output a first selection to a full adder; selecting, by a second multiplexer in the column cell, zero or the sum bit to output a second selection to the full adder; selecting, by a third multiplexer in the column cell, zero or a carry-in bit from a prior stage full adder to output a third selection to the full adder; and outputting an exponent bit of a primitive product between the activation value and the weight value.

- `CL-12/e1` → **M21** — adding, by a half adder in a column cell of the CIM macro, an exponent bit of an activation value and an exponent bit of a weight value to output a carry-out bit and a sum bit
- `CL-12/e2` → **M22** — selecting, by a first multiplexer in the column cell, zero or a prior stage carry-out bit from a prior stage half adder to output a first selection to a full adder
- `CL-12/e3` → **M23** — selecting, by a second multiplexer in the column cell, zero or the sum bit to output a second selection to the full adder
- `CL-12/e4` → **M24** — selecting, by a third multiplexer in the column cell, zero or a carry-in bit from a prior stage full adder to output a third selection to the full adder
- `CL-12/e5` → **M25** — outputting an exponent bit of a primitive product between the activation value and the weight value

### 독립항 `CL-20`

> A system comprising: a compute device configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode device configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein the compute device comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer, and the third multiplexer perform respective selections based on control signals according to the mode.

- `CL-20/e1` → **M36** — a compute device configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values
  - `CL-20/e1/e1` → **M37** — a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit
  - `CL-20/e1/e2` → **M38** — a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder
  - `CL-20/e1/e3` → **M39** — a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder
  - `CL-20/e1/e4` → **M40** — a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder
  - `CL-20/e1/e5` → **M41** — wherein the first multiplexer, the second multiplexer, and the third multiplexer perform respective selections based on control signals according to the mode
- `CL-20/e2` → **M42** — a mode device configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values
  - `CL-20/e2/e1` → **M43** — the first floating point format and the second floating point format being flexible

### 종속항 `CL-2` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder.

- `CL-2/a1` (부착: `CL-1/e3`) → **M10** — wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder

### 종속항 `CL-3` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein the column cell further comprises a plurality of memory cells configured to store the weight value.

- `CL-3/a1` (부착: `CL-1/e3`) → **M11** — wherein the column cell further comprises a plurality of memory cells configured to store the weight value

### 종속항 `CL-4` — `single` (인용: CL-3)

> The hardware accelerator according to claim 3, wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder.

- `CL-4/a1` (부착: `CL-1/e3`) → **M12** — wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder

### 종속항 `CL-5` — `single` (인용: CL-3)

> The hardware accelerator according to claim 3, wherein: one of the plurality of memory cells comprises a first bitcell and a second bitcell, and the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline.

- `CL-5/a1` (부착: `CL-1/e3`) → **M13** — one of the plurality of memory cells comprises a first bitcell and a second bitcell
- `CL-5/a2` (부착: `CL-1/e3`) → **M14** — the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline

### 종속항 `CL-6` — `single` (인용: CL-5)

> The hardware accelerator according to claim 5, wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines.

- `CL-6/a1` (부착: `CL-1/e3`) → **M15** — wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines

### 종속항 `CL-7` — `single` (인용: CL-5)

> The hardware accelerator according to claim 5, wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value.

- `CL-7/a1` (부착: `CL-1/e3`) → **M16** — wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value

### 종속항 `CL-8` — `single` (인용: CL-7)

> The hardware accelerator according to claim 7, wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value.

- `CL-8/a1` (부착: `CL-1/e3`) → **M17** — wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value

### 종속항 `CL-9` — `single` (인용: CL-8)

> The hardware accelerator according to claim 8, wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder.

- `CL-9/a1` (부착: `CL-1/e3`) → **M18** — wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder

### 종속항 `CL-10` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5.

- `CL-10/a1` (부착: `CL-1/e3/e1`) → **M19** — wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5

### 종속항 `CL-11` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5.

- `CL-11/a1` (부착: `CL-1/e3/e1`) → **M20** — wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5

### 종속항 `CL-13` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: controlling the selections performed by the first multiplexer, the second multiplexer, and the third multiplexer based on control signals according to an arithmetic mode of the VMM operation.

- `CL-13/a1` (부착: `CL-12/e2`) → **M26** — controlling the selections performed by the first multiplexer, the second multiplexer, and the third multiplexer based on control signals according to an arithmetic mode of the VMM operation

### 종속항 `CL-14` — `single` (인용: CL-13)

> The method according to claim 13, further comprising: determining the arithmetic mode based on a first floating point format of the activation value and a second floating point format of the weight value.

- `CL-14/a1` (부착: `CL-12/e2`) → **M27** — determining the arithmetic mode based on a first floating point format of the activation value and a second floating point format of the weight value

### 종속항 `CL-15` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder; and outputting, by the fourth multiplexer in the column cell, an exponent bit of the primitive product.

- `CL-15/a1` (부착: `CL-12/e1`) → **M28** — selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder
- `CL-15/a2` (부착: `CL-12/e5`) → **M29** — outputting, by the fourth multiplexer in the column cell, an exponent bit of the primitive product

### 종속항 `CL-16` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: providing, by a first bitcell in the column cell, the exponent bit of the weight value to the half adder.

- `CL-16/a1` (부착: `CL-12/e1`) → **M30** — providing, by a first bitcell in the column cell, the exponent bit of the weight value to the half adder

### 종속항 `CL-17` — `single` (인용: CL-16)

> The method according to claim 16, further comprising: writing, concurrently, a further exponent bit of a further weight value to a second bitcell in the column cell, wherein the further weight value is different from the weight value.

- `CL-17/a1` (부착: `CL-12/e1`) → **M31** — writing, concurrently, a further exponent bit of a further weight value to a second bitcell in the column cell, wherein the further weight value is different from the weight value

### 종속항 `CL-18` — `single` (인용: CL-17)

> The method according to claim 17, further comprising: writing the further exponent bit to the second bitcell through a bitline shared with the first bitcell.

- `CL-18/a1` (부착: `CL-12/e1`) → **M32** — writing the further exponent bit to the second bitcell through a bitline shared with the first bitcell

### 종속항 `CL-19` — `single` (인용: CL-12)

> The method according to claim 12, wherein: a number of exponent bits in the activation value is at least one of 2, 3, 4, or 5; a number of exponent bits in the weight value is at least one of 2, 3, 4, or 5; and the method further comprises determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value.

- `CL-19/a1` (부착: `CL-12/e1`) → **M33** — a number of exponent bits in the activation value is at least one of 2, 3, 4, or 5
- `CL-19/a2` (부착: `CL-12/e1`) → **M34** — a number of exponent bits in the weight value is at least one of 2, 3, 4, or 5
- `CL-19/a3` (부착: `CL-12/e1`) → **M35** — the method further comprises determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value

## 3. 유기적 통합 그림 (D5 ④)

- **M122** (spec · stated) — The floating point multiplier is dissolved into the memory array: each column cell builds the exponent and the mantissa of one primitive product where the weight is stored, so the accelerator carries no separate exponent tree outside the array.
  - 근거 항목: M1, M4, M5
  - 인용: “reducing the need for external exponent trees, minimizing data movement, and enabling support for multiple low-precision numeric formats while maintaining high throughput during VMM operations”
- **M123** (claim · inferred) — Format agility is bought with zero-selection rather than with alternative datapaths: every exponent-stage multiplexer chooses between zero and a real sum, carry-out or carry-in bit, so a narrower format is run by driving the unused contributions to zero in the same wiring.
  - 근거 항목: M6, M7, M8, M9
  - 인용: “a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder”
  - 인용: “a multiplexer can be used to select zero or the bit stored in the bitcell associated with W0<4>, based on the FP format of weight value according to a control signal from the mode decoding unit”
- **M124** (claim · stated) — The mode decoding unit derives the arithmetic mode from the pair of declared floating point formats and emits the control signals that drive the multiplexers inside the column cell.
  - 근거 항목: M2, M9, M26, M27
  - 인용: “a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values”
  - 인용: “can be controlled by one or more control signals from the mode decoding unit”
- **M125** (claim · stated) — The activation format and the weight format are declared separately and may differ, so combinations that pair a wider activation with a narrower weight are ordinary operating points of the same hardware.
  - 근거 항목: M2, M3, M19, M20, M42, M43
  - 인용: “a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5”
  - 인용: “a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5”
  - 인용: “different combinations of formats for activations and weights to be employed to balance accuracy, memory bandwidth, and power consumption”
- **M126** (claim · stated) — The bitcell count of a column cell is fixed by the least common multiple of the exponent widths the cell must support, which makes cell sizing a stated arithmetic rule rather than a per-format design choice.
  - 근거 항목: M33, M34, M35
  - 인용: “determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value”
  - 인용: “a minimum number of exponent bits in each column cell is determined by finding the least common multiple among all the possible combination of exponent bits in the various FP formats supported by each column cell”
  - 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2”
- **M127** (spec · inferred) — Because a cell of fixed width is divided into groups, a narrower exponent yields more weight elements per cell, so lowering precision converts the same silicon into storage capacity and throughput instead of leaving it idle.
  - 근거 항목: M11, M35
  - 인용: “the number of groups (or elements) of weight values for a given activation value bit (per row) can be determined for each column cell, which is the least common multiple of exponent bits divided by the number of exponent bits of per element of the weight value”
  - 인용: “For the weight value having exponent with 3b and 2b, the memory cells can be arranged into 4 groups and 6 groups, respectively.”
  - 인용: “the storage capacity of weight values in one column cell can be increased and the throughput of the column cell can also be increased by pipelining the adder tree through overlapping executions of multiple operations instructions”
- **M128** (claim · stated) — Splitting each memory cell into two bitcells on separate wordlines but a shared bitline lets one bank be written while the other drives the multiplication, so a weight reload overlaps the vector matrix multiplication instead of interrupting it.
  - 근거 항목: M13, M14, M15, M16, M18, M31, M32
  - 인용: “the first bitcell and the second bitcell share a bitline and are addressed by different wordlines”
  - 인용: “the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder”
  - 인용: “perform, in parallel, a write operation to the first set of bitcells and the VMM operation in the second set of bitcells based on a weight select signal”
- **M129** (spec · stated) — Primitive products leave the column cells as mantissa bits that are shifted into alignment and summed by an adder tree in the integer domain, with the return to a higher-precision format deferred to a dequantization step outside the macro.
  - 근거 항목: M1, M4
  - 인용: “a functional block configured to align mantissa bits of primitive products generated by column cells in the computing unit by shifting the mantissa bits”
  - 인용: “an adder tree configured to output an accumulation value of the primitive products in an integer format by adding the shifted mantissa bits”
  - 인용: “aligning mantissa bits via shifting, accumulating shifted mantissa bits in an integer domain, dequantizing accumulated results into a higher-precision format”
- **M130** (spec · stated) — Subnormal operands are handled by replacing the implicit leading one with a bit derived from the exponent, so the same column cell circuits serve both normal and subnormal floating point numbers.
  - 근거 항목: M4
  - 인용: “the same logic circuits of the column cell **220** can handle both normal and subnormal FP numbers”
- **M131** (spec · stated) — The same double-bitcell storage that carries weights is reused as a scan chain for test and diagnosis, which the specification presents as leaving normal computation timing untouched.
  - 근거 항목: M11, M13
  - 인용: “using scan control signals to test or diagnose the weight-storage and compute paths while preserving normal performance characteristics”
- **M132** (spec · inferred) — The flexibility on offer is an enumerated table rather than an open range: Table 2 lists a finite set of activation and weight format pairs, and the exponent and mantissa widths the specification admits are likewise finite lists.
  - 근거 항목: M2, M3, M65
  - 인용: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats”
  - 인용: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits and the mantissas of the activation values and weight values can have 4, 3, 2 or 1 bit”

## 4. 포지셔닝 (D5 ⑤)

- **M133**
  - 배경 문제: Compact numeric formats force activations and weights back and forth between numeric domains, and the specification states that each conversion step adds scaling, rounding and saturation logic that costs area, power and latency and accumulates quantization error, while fixed conversion pipelines and format-specific datapaths become hard to adapt as new low-bit encodings appear.
  - 주장 효과: The specification asserts that a compute-in-memory macro operating under a mode decoding unit can execute vector matrix operations natively across a range of compact floating point formats, without separate conversion pipelines or a dedicated core per format, and while keeping a consistent external programming model.
  - 차이: The asserted difference is structural, not measured: one shared column-cell datapath is reconfigured by control signals derived from the declared formats, in place of per-format conversion pipelines and per-format datapaths. The specification offers no comparative performance figure for this difference.
  - 인용: “Each conversion step requires additional scaling, rounding, and saturation logic, which adds area, power, and latency to already dense compute fabrics, and can introduce cumulative quantization errors that degrade numerical behavior over many layers”
  - 인용: “As new low-bit formats and variants are introduced to improve efficiency (such as different 8-bit or sub-8-bit floating-point encodings), fixed conversion pipelines and format-specific data paths become increasingly difficult to adapt”
  - 인용: “The techniques described herein disclose accelerators, systems, methods, apparatus, and/or devices that perform operations natively supporting multiple, flexible numeric formats for activations and weights under the control of a mode decoding unit”
  - 인용: “without requiring separate conversion pipelines or dedicated cores for each format”
  - 인용: “preserving a consistent external programming model and avoiding significant redesign of underlying storage arrays, arithmetic structures, or dataflow for new or evolving numeric schemes”
  - 인용: “Reduced precision formats (i.e., reduced bit widths) can greatly increase computation speed and lower memory usage with minimal loss in accuracy, and thereby greatly improve the latency and throughput of a deep learning process in a neural network.”
- **M134**
  - 배경 문제: Supporting several exponent widths in one array invites either a cell built for the widest format, which wastes bitcells on narrow ones, or a separate cell design per format, which is the redesign of storage and arithmetic structures the specification sets out to avoid.
  - 주장 효과: The specification asserts that sizing a column cell to the least common multiple of the supported widths lets one cell serve every supported format by regrouping its bitcells, and states that this raises the storage capacity and the throughput of the cell.
  - 차이: The asserted difference is a sizing rule in place of a per-format cell: the cell's bit count follows from an arithmetic property of the supported width set, and a change of format becomes a regrouping of existing bitcells rather than a new array. No before and after measurement is given.
  - 인용: “preserving a consistent external programming model and avoiding significant redesign of underlying storage arrays, arithmetic structures, or dataflow for new or evolving numeric schemes”
  - 인용: “a minimum number of exponent bits in each column cell is determined by finding the least common multiple among all the possible combination of exponent bits in the various FP formats supported by each column cell”
  - 인용: “the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2”
  - 인용: “For the weight value having exponent with 3b and 2b, the memory cells can be arranged into 4 groups and 6 groups, respectively.”
  - 인용: “the storage capacity of weight values in one column cell can be increased and the throughput of the column cell can also be increased by pipelining the adder tree through overlapping executions of multiple operations instructions”
  - 인용: “each exponent bit corresponds to a full adder that can be configured to support flexible FP data with various possible combinations using multiplexers”
- **M135**
  - 배경 문제: Weight values resident in the array must be replaced between operations, and the specification frames the alternative to overlapping them as a macro that stalls for writes instead of computing.
  - 주장 효과: The specification asserts that two bitcells per memory cell, addressed by separate wordlines and sharing a bitline, let a write proceed in one bank in parallel with the vector matrix multiplication in the other, hiding weight-update latency behind ongoing computation.
  - 차이: The asserted difference is a doubled storage element rather than a faster one: the gain is claimed as reduced idle time and sustained utilization, and the specification quantifies neither the idle time removed nor the area added by the second bitcell.
  - 인용: “This concurrent access can improve bandwidth for weight updates and help keep the CIM macro busy with computation instead of stalling for writes”
  - 인용: “hide weight-update latency behind ongoing computation, supporting dynamic model updates, weight streaming, or multi-phase compute schedules”
  - 인용: “allowing concurrent loading of the next matrix of weight values while the previous weight values are still in use for the VMM computation”
  - 인용: “perform, in parallel, a write operation to the first set of bitcells and the VMM operation in the second set of bitcells based on a weight select signal”

## 5. 구성요소와 3중 접지 (D5 ③)

| 구성요소 | 청구항 좌표 | 라벨(EN) | 접지 |
|---|---|---|---|
| **M1** | `CL-1/e1` | compute-in-memory (CIM) macro performing the VMM operation between an activation vector and a weight matrix | **M44** (명세서 found · 도면 found) |
| **M2** | `CL-1/e2` | mode decoding unit providing the arithmetic mode from the activation and weight floating point formats | **M45** (명세서 found · 도면 found) |
| **M3** | `CL-1/e2/e1` | flexibility of the first and second floating point formats | **M46** (명세서 found · 도면 found) |
| **M4** | `CL-1/e3` | column cell of the CIM macro outputting a primitive product of an activation value and a weight value | **M47** (명세서 found · 도면 found) |
| **M5** | `CL-1/e3/e1` | half adder adding the activation and weight exponent bits into a carry-out bit and a sum bit | **M48** (명세서 found · 도면 found) |
| **M6** | `CL-1/e3/e2` | first multiplexer selecting zero or the prior stage carry-out bit into the full adder | **M49** (명세서 found · 도면 found) |
| **M7** | `CL-1/e3/e3` | second multiplexer selecting zero or the half adder sum bit into the full adder | **M50** (명세서 found · 도면 found) |
| **M8** | `CL-1/e3/e4` | third multiplexer selecting zero or the prior stage carry-in bit into the full adder | **M51** (명세서 found · 도면 found) |
| **M9** | `CL-1/e3/e5` | the three multiplexers selecting on control signals set by the arithmetic mode | **M52** (명세서 found · 도면 found) |
| **M10** | `CL-2/a1` | fourth multiplexer outputting the primitive product exponent bit by selecting among three sources | **M66** (명세서 found · 도면 found) |
| **M11** | `CL-3/a1` | plurality of memory cells in the column cell storing the weight value | **M67** (명세서 found · 도면 found) |
| **M12** | `CL-4/a1` | bitcell storing the weight exponent bit and feeding it to the half adder | **M68** (명세서 found · 도면 found) |
| **M13** | `CL-5/a1` | memory cell comprising a first bitcell and a second bitcell | **M69** (명세서 found · 도면 found) |
| **M14** | `CL-5/a2` | first and second bitcells addressed by different wordlines | **M70** (명세서 found · 도면 found) |
| **M15** | `CL-6/a1` | first and second bitcells sharing a bitline while addressed by different wordlines | **M71** (명세서 found · 도면 found) |
| **M16** | `CL-7/a1` | first and second bitcells storing bits of two different weight values | **M72** (명세서 found · 도면 found) |
| **M17** | `CL-8/a1` | first bitcell supplying the weight exponent bit to the half adder | **M73** (명세서 found · 도면 found) |
| **M18** | `CL-9/a1` | second bitcell updating concurrently while the first bitcell drives the half adder | **M74** (명세서 found · 도면 found) |
| **M19** | `CL-10/a1` | activation exponent bit count of 2, 3, 4 or 5 | **M75** (명세서 found · 도면 found) |
| **M20** | `CL-11/a1` | weight exponent bit count of 2, 3, 4 or 5 | **M76** (명세서 found · 도면 found) |
| **M21** | `CL-12/e1` | adding the activation and weight exponent bits in a half adder of the column cell | **M53** (명세서 found · 도면 found) |
| **M22** | `CL-12/e2` | first multiplexer selecting zero or the prior stage carry-out bit for the full adder | **M54** (명세서 found · 도면 found) |
| **M23** | `CL-12/e3` | second multiplexer selecting zero or the sum bit for the full adder | **M55** (명세서 found · 도면 found) |
| **M24** | `CL-12/e4` | third multiplexer selecting zero or the prior stage carry-in bit for the full adder | **M56** (명세서 found · 도면 found) |
| **M25** | `CL-12/e5` | outputting the exponent bit of the primitive product | **M57** (명세서 found · 도면 found) |
| **M26** | `CL-13/a1` | controlling the three multiplexer selections by control signals from the arithmetic mode | **M77** (명세서 found · 도면 found) |
| **M27** | `CL-14/a1` | determining the arithmetic mode from the activation and weight floating point formats | **M78** (명세서 found · 도면 found) |
| **M28** | `CL-15/a1` | fourth multiplexer selecting among the full adder output, the sum bit and the carry-in bit | **M79** (명세서 found · 도면 found) |
| **M29** | `CL-15/a2` | fourth multiplexer outputting the primitive product exponent bit | **M80** (명세서 found · 도면 found) |
| **M30** | `CL-16/a1` | first bitcell providing the weight exponent bit to the half adder | **M81** (명세서 found · 도면 found) |
| **M31** | `CL-17/a1` | concurrently writing another weight exponent bit into a second bitcell | **M82** (명세서 found · 도면 found) |
| **M32** | `CL-18/a1` | writing the further exponent bit through the bitline shared with the first bitcell | **M83** (명세서 found · 도면 found) |
| **M33** | `CL-19/a1` | activation exponent bit count of 2, 3, 4 or 5 | **M84** (명세서 found · 도면 found) |
| **M34** | `CL-19/a2` | weight exponent bit count of 2, 3, 4 or 5 | **M85** (명세서 found · 도면 found) |
| **M35** | `CL-19/a3` | sizing the bitcells of the column cell by the least common multiple of the possible exponent widths | **M86** (명세서 found · 도면 found) |
| **M36** | `CL-20/e1` | compute device performing the VMM operation between an activation vector and a weight matrix | **M58** (명세서 found · 도면 found) |
| **M37** | `CL-20/e1/e1` | half adder adding the activation and weight exponent bits into a carry-out bit and a sum bit | **M59** (명세서 found · 도면 found) |
| **M38** | `CL-20/e1/e2` | first multiplexer selecting zero or the prior stage carry-out bit into the full adder | **M60** (명세서 found · 도면 found) |
| **M39** | `CL-20/e1/e3` | second multiplexer selecting zero or the half adder sum bit into the full adder | **M61** (명세서 found · 도면 found) |
| **M40** | `CL-20/e1/e4` | third multiplexer selecting zero or the prior stage carry-in bit into the full adder | **M62** (명세서 found · 도면 found) |
| **M41** | `CL-20/e1/e5` | the three multiplexers selecting on control signals set by the mode | **M63** (명세서 found · 도면 found) |
| **M42** | `CL-20/e2` | mode device providing the VMM mode from the activation and weight floating point formats | **M64** (명세서 found · 도면 found) |
| **M43** | `CL-20/e2/e1` | flexibility of the first and second floating point formats | **M65** (명세서 found · 도면 found) |

- **M44** ← 구성요소 M1
  - 명세서 `[0128]`: “For example, CIM macro **101** can support a Vector Matrix Multiplication (VMM) operation between a vector of activation values and a matrix of weight values.”
  - 도면 `FIG-2` (도면부호 101, 222, 220): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M45** ← 구성요소 M2
  - 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
  - 명세서 `[0063]`: “A mode decoding unit can supply an arithmetic mode that may reflect the floating-point formats chosen for activations and weights, allowing the accelerator to support multiple “flexible” low-precision formats without redesigning the datapath.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M46** ← 구성요소 M3
  - 명세서 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
  - 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
  - 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
- **M47** ← 구성요소 M4
  - 명세서 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
  - 명세서 `[0136]`: “In the kth column of computing unit **222**, a column cell **220** of ith row is configured to perform the multiplication operation between the activation value a.sub.i and the weight value w.sub.ik to output the primitive product P.sub.ik=a.sub.i×w.sub.ik.”
  - 도면 `FIG-3` (도면부호 220): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M48** ← 구성요소 M5
  - 명세서 `[0188]`: “The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M49** ← 구성요소 M6
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M50** ← 구성요소 M7
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M51** ← 구성요소 M8
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M52** ← 구성요소 M9
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M53** ← 구성요소 M21
  - 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M54** ← 구성요소 M22
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M55** ← 구성요소 M23
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M56** ← 구성요소 M24
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M57** ← 구성요소 M25
  - 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
  - 명세서 `[0166]`: “The full adders can be connected in series, where each full adder can output an exponent bit of the primitive product and a carry-in bit for the next stage full adder.”
  - 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M58** ← 구성요소 M36
  - 명세서 `[0017]`: “For example, in the disclosed technology a system may be provided that performs vector-matrix multiplication using a compute device that generates portions of a floating-point product directly within memory structures.”
  - 명세서 `[0072]`: “At the system level, the disclosed technology may be implemented in a compute device that can house the exponent-processing hardware described above, while a mode device provides the control mode based on the selected floating-point formats for activations and weights.”
  - 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M59** ← 구성요소 M37
  - 명세서 `[0188]`: “The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M60** ← 구성요소 M38
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M61** ← 구성요소 M39
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M62** ← 구성요소 M40
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M63** ← 구성요소 M41
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M64** ← 구성요소 M42
  - 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
  - 명세서 `[0017]`: “The mode device can determine how exponent behavior should be formed based on the floating-point formats chosen for the activations and weights, allowing the system to adapt to multiple low-precision numeric formats without redesigning the underlying arithmetic fabric.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M65** ← 구성요소 M43
  - 명세서 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
  - 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
  - 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
- **M66** ← 구성요소 M10
  - 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
  - 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product: the output of the full adder, the sum output of the half adder, or a carry-in from an upstream stage.”
  - 도면 `FIG-28-29` (도면부호 2866, 2860, 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M67** ← 구성요소 M11
  - 명세서 `[0161]`: “The column cell **220** includes memory cells for storing the bits of the weight value, one bit of the weight value corresponding to one memory cell.”
  - 명세서 `[0140]`: “The number of memory cells in the column cell **340** is determined by the number of bits used by the weight value. Each memory cell stores one bit of the weight value.”
  - 도면 `FIG-3` (도면부호 220, 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M68** ← 구성요소 M12
  - 명세서 `[0185]`: “To compute the exponent of the primitive product, each memory cell stored a corresponding exponent bit of the weight value can be connected to a half adder (HA).”
  - 명세서 `[0188]`: “each bitcell stores a corresponding exponent bit of the weight value”
  - 명세서 `[0188]`: “the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder”
  - 도면 `FIG-26` (도면부호 220): “FIGS. **26**, **27**A, **27**B, **27**C illustrate exemplary logic circuits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-28-29` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M69** ← 구성요소 M13
  - 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1”
  - 명세서 `[0215]`: “each memory cell in the CIM macro can include one, two or more bitcells”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- **M70** ← 구성요소 M14
  - 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1, which can be accessed via separate wordlines wwl0 and wwl1.”
  - 명세서 `[0217]`: “bitcell BC0 can be addressed by wordline wwl0 and bitcell BC1 can be address by wordline wwl1.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- **M71** ← 구성요소 M15
  - 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
  - 명세서 `[0066]`: “paired bitcells may share a common bitline while still being controlled by different wordlines.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- **M72** ← 구성요소 M16
  - 명세서 `[0218]`: “bitcell BC0 can store a first bit of a first weight value and bitcell BC1 can store a second bit of a second weight value that is different from the first weight value.”
  - 명세서 `[0218]`: “each memory cell **4303** can store two bits from two different weight values.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- **M73** ← 구성요소 M17
  - 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
  - 명세서 `[0185]`: “To compute the exponent of the primitive product, each memory cell stored a corresponding exponent bit of the weight value can be connected to a half adder (HA).”
  - 도면 `FIG-7-8` (도면부호 220, 830): “FIGS. **7**-**8** illustrate an enlarged view of the column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M74** ← 구성요소 M18
  - 명세서 `[0067]`: “while the first bitcell is driving the exponent bit into the half adder, the second bitcell can be updated with a new bit of another weight value.”
  - 명세서 `[0218]`: “the first set of bitcells can perform a write operation and the second set of bitcells can perform a VMM operation.”
  - 명세서 `[0228]`: “It is noted that write operation and VMM operation can be performed in parallel in two different bitcells.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-44` (도면부호 4400): “FIG. **44** illustrates a timing diagram of a CIM macro for a write operation, in accordance with some aspects of the present disclosure.”
- **M75** ← 구성요소 M19
  - 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
  - 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
  - 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M76** ← 구성요소 M20
  - 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
  - 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M77** ← 구성요소 M26
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 명세서 `[0069]`: “the selection behavior of the multiplexers may be driven by control signals tied to an arithmetic mode.”
  - 도면 `FIG-28-29` (도면부호 2860, 2862, 2864, 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M78** ← 구성요소 M27
  - 명세서 `[0069]`: “In some implementations, an arithmetic mode may be determined from the floating-point formats used for the activation and the weight.”
  - 명세서 `[0007]`: “The hardware accelerator can also have a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, where the first floating point format and the second floating point format are flexible.”
  - 명세서 `[0146]`: “the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101**”
  - 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M79** ← 구성요소 M28
  - 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
  - 명세서 `[0070]`: “the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage, and present that as the exponent bit of the primitive product.”
  - 도면 `FIG-28-29` (도면부호 2866, 2860, 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M80** ← 구성요소 M29
  - 명세서 `[0188]`: “The resulting exponent bits of the primitive product include the sum bit S.sub.LSB from the half adder for the LSBs of the exponents of the activation value and the weight value, the exponent bits E.sub.j output from the fourth multiplexers **2866**”
  - 명세서 `[0070]`: “Further, the method may describe using a fourth multiplexer to choose between different exponent results produced inside the column cell.”
  - 도면 `FIG-28-29` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M81** ← 구성요소 M30
  - 명세서 `[0071]`: “Methods disclosed herein may also include sourcing the exponent bit of the weight value directly from a dedicated bitcell inside the column, which can feed that bit to the half adder.”
  - 명세서 `[0188]`: “the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder”
  - 도면 `FIG-7-8` (도면부호 220, 830): “FIGS. **7**-**8** illustrate an enlarged view of the column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-28-29` (도면부호 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M82** ← 구성요소 M31
  - 명세서 `[0071]`: “At the same time that the first bitcell is supplying a weight exponent bit to the half adder, the method may allow writing a new exponent bit for a different weight into a second bitcell.”
  - 명세서 `[0218]`: “the first set of bitcells can perform a write operation and the second set of bitcells can perform a VMM operation.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-44` (도면부호 4400): “FIG. **44** illustrates a timing diagram of a CIM macro for a write operation, in accordance with some aspects of the present disclosure.”
- **M83** ← 구성요소 M32
  - 명세서 `[0071]`: “For example, a second exponent bit may be written through a bitline shared with the first bitcell, simplifying the array wiring.”
  - 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- **M84** ← 구성요소 M33
  - 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b”
  - 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M85** ← 구성요소 M34
  - 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b”
  - 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M86** ← 구성요소 M35
  - 명세서 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 명세서 `[0192]`: “At step **3202**, a minimum number of exponent bits in each column cell is determined by finding the least common multiple among all the possible combination of exponent bits in the various FP formats supported by each column cell of the compute engine **100**.”
  - 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-32-33` (도면부호 3200, 3202): “FIGS. **32**-**33** illustrate methods for utilizing resources of a hardware accelerator, in accordance with some aspects of the present disclosure.”

## 6. 수치 사실 — 3분류 (재정 N9)

기계가 **무엇을 보증했는가**가 갈래마다 다르다. 갈래를 섞어 보면 승인은 형식이 된다.

### 6.1 원문 스팬 수치 (`quoted` · `bibliographic`)

- 원문 스팬 수치: **34건** — M87, M88, M89, M90, M91, M92, M93, M94, M95, M96, M97, M98, M99, M100, M101, M102, M103, M104, M105, M106, M107, M108, M109, M110, M111, M112, M113, M114, M115, M116, M117, M118, M119, M120
- 서지 복사: M117, M118, M119, M120 (`patent` 블록에서 결정론 복사)

- **M87** — numeric value at [0186] · `1-5` → `1-5`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M88** — numeric value at [0186] · `1-4` → `1-4`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M89** — numeric value at [0186] · `1-3` → `1-3`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M90** — numeric value at [0186] · `1-3` → `1-3`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M91** — numeric value at [0186] · `1-2` → `1-2`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M92** — numeric value at [0186] · `1-2` → `1-2`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M93** — numeric value at [0186] · `1-1` → `1-1`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M94** — numeric value at [0183] · `2` → `2`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M95** — numeric value at [0183] · `60` → `60`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M96** — numeric value at [0183] · `1-4` → `1-4`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M97** — numeric value at [0183] · `1-3` → `1-3`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M98** — numeric value at [0137] · `3` → `3`
  - 원천 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
- **M99** — numeric value at [0165] · `0` → `0`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M100** — numeric value at [0165] · `<6` → `<6`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M101** — numeric value at [0165] · `3` → `3`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M102** — numeric value at [0165] · `0` → `0`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M103** — numeric value at [0165] · `<4` → `<4`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M104** — numeric value at [0165] · `2` → `2`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M105** — numeric value at [0165] · `<4` → `<4`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M106** — numeric value at [0165] · `2` → `2`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M107** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- **M108** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- **M109** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- **M110** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
- **M111** — numeric value at [0186] · `5, 4, 3 or 2` → `5;4;3;2`
  - 원천 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
- **M112** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- **M113** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M114** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M115** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M116** — numeric value at [0189] · `4, 3, and 2` → `4;3;2`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M117** — bibliographic field patent.number · `US20260147854A1` → `US20260147854A1`
  - 원천 ``: “”
- **M118** — bibliographic field patent.dates.priority · `2024-11-22` → `2024-11-22`
  - 원천 ``: “”
- **M119** — bibliographic field patent.dates.filing · `2025-11-21` → `2025-11-21`
  - 원천 ``: “”
- **M120** — bibliographic field patent.dates.publication · `2026-05-28` → `2026-05-28`
  - 원천 ``: “”

### 6.2 파생 수치 (`derived`) — 산식과 원천 스팬을 나란히

_파생 수치 없음. 승인 봉투의 `derived_fact_ack` 는 빈 배열로 적는다._


### 6.3 도면 유래 수치 (`figure-sourced`) — 기계 검증 불가

- **M121** — count of VMM operating modes enumerated in Table 2 of FIG. 60 · `8` → `8`
  - 도면 `FIG-60` · `machine_verifiable: false` — **기계 검증 불가**

## 7. ★ 사람 검증 필요 목록 (재정 R1)

도면에서 읽은 값은 기계가 대조할 원문 스팬이 없다. **검사가 통과시켰다는 사실이 값이**
**옳다는 뜻이 아니다.** 아래 목록은 봉투의 `manual_verification_ack[]` 와 정확히 일치해야 한다.

- **M121** — count of VMM operating modes enumerated in Table 2 of FIG. 60 · 값 `8` · 도면 `FIG-60` (도면부호 ) · 사유 `figure-sourced`

## 8. ★ 접지 예외 (재정 R3)

접지 전량이 원칙이므로 예외는 날조하거나 숨기지 않고 드러낸다. **예외가 많으면 그것이**
**소재 신호다.**

_예외 없음 — 전 구성요소가 명세서·도면 양쪽에 접지되었다._


## 9. drop 신호 (D4 — 최종)

- 단계: `final` · 판정: `go`
- 사유: 안도감이 재료 안에 실물로 있음 — 배경(형식 변환 파이프라인의 면적·전력·지연과 누적 양자화 오차)이 명세서 문언으로 서술되고, 해법이 '0을 고르는 멀티플렉서'라는 하나의 그림으로 환원되며(FIG-28), 셀 폭이 최소공배수라는 산식으로 정해지는 대목은 일반 독자가 따라올 수 있는 구체다. 도면 12건 전건이 접지에 물려 있고 독립항 3개의 구성요소가 전부 접지되었다. 다만 성능 수치가 전무해 '얼마나 좋아졌는가'로는 쓸 수 없으므로, 서사는 구조적 차이(형식별 데이터패스 제거·LCM 사이징·이중 비트셀 중첩)로만 세워야 한다.

## 10. ★ 미분류 종속 구조 (재정 P-1)

Markush·조건부·수단항·카테고리 전환은 typed operator 입법을 범위에서 **제외**했고,
대신 `unclassified` 표지 + 이 목록 + 판정 행 계수 셋으로 침묵을 막는다.
**이 목록의 항목은 결함이 아니다** — 구조 미분류라는 사실의 표지이며, 종속 형태
판정(`parse.set-equals`·`parse.type-agrees`)의 대상에서 빠졌다는 뜻이다. 전문은
이미 보존되어 있으므로(재정 R1) 여기서 사람 눈이 마지막 심급이 된다.

_미분류 종속항 없음 — 전 종속항이 5종 어형으로 파싱되었다._


## 11. ★ 맹검 스크리닝 메모 — 두 실행 병기 (재정 P-A · P-U4)

분해 직후 `read-a`·`read-b` 가 **각자** 적은 1차 판단이다. 상신이 아니었고 런을
세우지 않았으며, 최종 서사 평가 레인에는 비공개였다(앵커링 방지). 둘 다 싣는 이유는
**두 독립 관찰의 일치/불일치 자체가 신호**이기 때문이다 — 한 건으로 합치면 그 신호가
소멸한다.

| 실행 | 방향 | 근거 요지 |
|---|---|---|
| `read-a` | `clear` | 권리 관심이 한 자리에 뚜렷함 — 열 하나의 셀 안에서 반가산기 1개와 멀티플렉서 3개의 선택을 제어신호로 바꿔 끼우는 것만으로 활성값·가중치의 부동소수점 지수 폭(2~5비트)이 서로 달라도 같은 회로가 곱셈을 처리한다는 구조가 청구항 1에 그대로 서 있고, 종속항 3~9가 그 셀 안의 비트셀 공유 비트라인·동시 갱신으로 '계산하면서 다음 가중치를 미리 적재한다'는 그림까지 붙여 준다. 일반 독자에게 '숫자 형식을 바꿀 때마다 변환하지 않는다'는 안도감 있는 한 문장으로 착지시킬 재료가 청구항만으로 확보됨. |
| `read-b` | `clear` | 독립항 3개가 같은 한 자리(컬럼 셀 안의 반가산기 + 멀티플렉서 3개 -> 전가산기)를 구조·방법·시스템으로 반복해 권리 관심이 한 구성에 뚜렷하게 모인다. 일반 독자에게는 '부동소수점 지수를 메모리 셀 안에서 그냥 더해 버려 도메인 변환을 없앤다'는 한 문장 서사가 서고, 종속항의 비트셀 공유 비트라인·동시 갱신과 지수 2~5비트 가변폭(최소공배수로 비트셀 수 산정)이 '왜 유연해지는가'의 구체 근거를 대므로 안도감으로 착지할 재료가 충분하다. |

두 관찰의 방향이 `clear` 로 일치했다.

## 12. ★ 수치 인벤토리 — 전수 수확 (재정 P-B)

수치는 접지 스팬과 서지면에서 **전수 기계 수확**되었고, 중요분은 LLM 의 중요도
판단이 아니라 함의·포지셔닝이 실제로 참조했는가(`numeric_refs`)로 **역참조 도출**된다.

**전체 34건 — 참조 3건 표시, 미참조 31건 접힘**

_카운트를 상시 표기하는 이유: 카운트가 없으면 미참조분 접힘이 은폐가 된다._

### 12.1 참조된 수치 (함의·포지셔닝의 근거)

- **M110** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
  - 이 수치를 참조한 항목: M125, M133
- **M111** — numeric value at [0186] · `5, 4, 3 or 2` → `5;4;3;2`
  - 원천 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
  - 이 수치를 참조한 항목: M126, M133, M134
- **M112** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 이 수치를 참조한 항목: M125, M133

### 12.2 미참조 수치 31건 (접힘 — 숨김이 아니다)

<details>
<summary>미참조 31건 펼치기</summary>

- **M87** — numeric value at [0186] · `1-5` → `1-5`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M88** — numeric value at [0186] · `1-4` → `1-4`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M89** — numeric value at [0186] · `1-3` → `1-3`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M90** — numeric value at [0186] · `1-3` → `1-3`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M91** — numeric value at [0186] · `1-2` → `1-2`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M92** — numeric value at [0186] · `1-2` → `1-2`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M93** — numeric value at [0186] · `1-1` → `1-1`
  - 원천 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M94** — numeric value at [0183] · `2` → `2`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M95** — numeric value at [0183] · `60` → `60`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M96** — numeric value at [0183] · `1-4` → `1-4`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M97** — numeric value at [0183] · `1-3` → `1-3`
  - 원천 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- **M98** — numeric value at [0137] · `3` → `3`
  - 원천 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
- **M99** — numeric value at [0165] · `0` → `0`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M100** — numeric value at [0165] · `<6` → `<6`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M101** — numeric value at [0165] · `3` → `3`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M102** — numeric value at [0165] · `0` → `0`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M103** — numeric value at [0165] · `<4` → `<4`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M104** — numeric value at [0165] · `2` → `2`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M105** — numeric value at [0165] · `<4` → `<4`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M106** — numeric value at [0165] · `2` → `2`
  - 원천 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- **M107** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- **M108** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- **M109** — numeric value at [0188] · `1` → `1`
  - 원천 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- **M113** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M114** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M115** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M116** — numeric value at [0189] · `4, 3, and 2` → `4;3;2`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M117** — bibliographic field patent.number · `US20260147854A1` → `US20260147854A1`
- **M118** — bibliographic field patent.dates.priority · `2024-11-22` → `2024-11-22`
- **M119** — bibliographic field patent.dates.filing · `2025-11-21` → `2025-11-21`
- **M120** — bibliographic field patent.dates.publication · `2026-05-28` → `2026-05-28`

</details>

★ 미참조 수치를 본문이 처음 인용하면 CP2 에 **"미검토 수치 사용" 플래그**가 자동
첨부된다(재정 P-B). 무검토 게시 경로는 없다 — 모든 수치는 CP1 검토 또는 사용 시 검토다.

### 12.3 수확하지 못한 토큰 33건

값 문법으로 파싱되지 않아 수확에서 빠진 토큰이다. 시끄럽게 실패하되 스테이지를
죽이지 않는다 — 수확은 검사가 아니다.

| 위치 | 토큰 | 사유 |
|---|---|---|
| `[0128]` | `101` | figure-numeral |
| `[0146]` | `100` | figure-numeral |
| `[0146]` | `110` | figure-numeral |
| `[0146]` | `101` | figure-numeral |
| `[0183]` | `101` | figure-numeral |
| `[0137]` | `220` | figure-numeral |
| `[0136]` | `222` | figure-numeral |
| `[0136]` | `220` | figure-numeral |
| `[0188]` | `2862` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2862` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0188]` | `110` | figure-numeral |
| `[0188]` | `830` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0161]` | `220` | figure-numeral |
| `[0140]` | `340` | figure-numeral |
| `[0217]` | `4303` | figure-numeral |
| `[0217]` | `4303` | figure-numeral |
| `[0217]` | `4303` | figure-numeral |
| `[0218]` | `4303` | figure-numeral |
| `[0146]` | `100` | figure-numeral |
| `[0146]` | `110` | figure-numeral |
| `[0146]` | `101` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0189]` | `220` | figure-numeral |
| `[0192]` | `3202` | figure-numeral |
| `[0192]` | `100` | figure-numeral |

## 13. 독해 프로파일 — 수렴 (재정 P-3)

**이 절은 결함 후보 목록이 아니다.** 두 독립 분해가 어떻게 갈렸는가의 기술이며,
갈림 자체가 실패를 뜻하지 않는다. 축은 세 층으로 읽는다 — `exact-match`(구조 사실:
법) · `escalation-trigger`(해석 여지: 미달 = 실패가 아니라 상신) · `measure-only`
(판정 제외·측정 전용).

| 축 | 정책 | 값 | 임계 | 상태 |
|---|---|---|---|---|
| `independent-count` | `exact-match` | - | - | `pass` |
| `element-set` | `escalation-trigger` | 1.0000 | 0.95 | `pass` |
| `tree-edges` | `escalation-trigger` | 1.0000 | 0.95 | `pass` |
| `dependent-count` | `exact-match` | - | - | `pass` |
| `dependent-set` | `exact-match` | 1.0000 | 1.0 | `pass` |
| `addition-attachment` | `measure-only` | 1.0000 | - | `measured` |

## 14. 도면

- `FIG-1` — “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-01.png` · 도면부호 100, 101, 110
- `FIG-2` — “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-02.png` · 도면부호 101, 220, 222
- `FIG-3` — “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-03.png` · 도면부호 220, 340
- `FIG-7-8` — “FIGS. **7**-**8** illustrate an enlarged view of the column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-07.png` · 도면부호 220, 830
- `FIG-9` — “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-09.png` · 도면부호 830
- `FIG-26` — “FIGS. **26**, **27**A, **27**B, **27**C illustrate exemplary logic circuits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-26.png` · 도면부호 220
- `FIG-28` — “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-28.png` · 도면부호 220, 830, 2860, 2862, 2864, 2866
- `FIG-28-29` — “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-29.png` · 도면부호 220, 830, 2860, 2862, 2864, 2866
- `FIG-32-33` — “FIGS. **32**-**33** illustrate methods for utilizing resources of a hardware accelerator, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-32.png` · 도면부호 3200, 3202
- `FIG-43` — “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-43.png` · 도면부호 4303
- `FIG-44` — “FIG. **44** illustrates a timing diagram of a CIM macro for a write operation, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-44.png` · 도면부호 4400
- `FIG-60` — “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-60.png` · 도면부호 
- **M136** (FIG-1) — Block diagram of the compute engine as a whole: an input buffer streams the activation vector into the digital compute-in-memory macro, while a mode decoding unit supplies the arithmetic mode and the surrounding logic handles control and dequantization. · 도면부호 100, 101, 110
- **M137** (FIG-2) — Block diagram of the compute-in-memory macro, resolving it into columns of computing units, each column holding rows of column cells whose primitive products feed one adder tree to form a dot product. · 도면부호 101, 220, 222
- **M138** (FIG-3) — Block diagram of a single column cell, the unit that turns one activation value and one weight value into a primitive product. · 도면부호 220, 340
- **M139** (FIG-7-8) — Enlarged view of the column cell, placing the exponent handling block beside the mantissa partial-product columns so the two datapaths can be read side by side. · 도면부호 220, 830
- **M140** (FIG-9) — Scheme for the exponent datapath, showing half adders adding the activation and weight exponent bits position by position and full adders chaining the carries into the exponent of the primitive product. · 도면부호 830
- **M141** (FIG-26) — Gate-level logic circuits inside a column cell, showing the primitives from which the half adder, full adder and selection functions are built. · 도면부호 220
- **M142** (FIG-28) — Column cell arranged for several floating point formats, showing the multiplexers around each full adder that select zero in place of a real sum, carry-out or carry-in bit. · 도면부호 220, 830, 2860, 2862, 2864, 2866
- **M143** (FIG-28-29) — The pair of exponent-handling column cell designs: the first surrounds each exponent full adder with multiplexers so one stage can serve several formats, and the second is a shared cell whose row and column count is the least common multiple of the supported exponent widths. · 도면부호 220, 830, 2860, 2862, 2864, 2866
- **M144** (FIG-32-33) — Two resource-sizing procedures, each starting from the least common multiple of the supported exponent or mantissa widths and deriving the number of weight element groups and the number of full adders per column cell. · 도면부호 3200, 3202
- **M145** (FIG-43) — Schematic of a stack of memory cells in which every memory cell holds two bitcells reached by separate wordlines and sharing one bitline. · 도면부호 4303
- **M146** (FIG-44) — Timing diagram of a write operation, showing the weight select signal choosing which bank of bitcells its wordlines activate while weight data moves on the bitlines. · 도면부호 4400
- **M147** (FIG-60) — Table 2, enumerating operating modes as pairs of an activation format and a weight format and giving, for each mode, the sign, exponent and mantissa bit assignment of the operands and of the primitive product. · 도면부호 

## 15. 항목 색인 (전량)

| 항목 | 종류 | 상태 | 승계 |
|---|---|---|---|
| **M1** | 구성요소 | active | - |
| **M2** | 구성요소 | active | - |
| **M3** | 구성요소 | active | - |
| **M4** | 구성요소 | active | - |
| **M5** | 구성요소 | active | - |
| **M6** | 구성요소 | active | - |
| **M7** | 구성요소 | active | - |
| **M8** | 구성요소 | active | - |
| **M9** | 구성요소 | active | - |
| **M10** | 구성요소 | active | - |
| **M11** | 구성요소 | active | - |
| **M12** | 구성요소 | active | - |
| **M13** | 구성요소 | active | - |
| **M14** | 구성요소 | active | - |
| **M15** | 구성요소 | active | - |
| **M16** | 구성요소 | active | - |
| **M17** | 구성요소 | active | - |
| **M18** | 구성요소 | active | - |
| **M19** | 구성요소 | active | - |
| **M20** | 구성요소 | active | - |
| **M21** | 구성요소 | active | - |
| **M22** | 구성요소 | active | - |
| **M23** | 구성요소 | active | - |
| **M24** | 구성요소 | active | - |
| **M25** | 구성요소 | active | - |
| **M26** | 구성요소 | active | - |
| **M27** | 구성요소 | active | - |
| **M28** | 구성요소 | active | - |
| **M29** | 구성요소 | active | - |
| **M30** | 구성요소 | active | - |
| **M31** | 구성요소 | active | - |
| **M32** | 구성요소 | active | - |
| **M33** | 구성요소 | active | - |
| **M34** | 구성요소 | active | - |
| **M35** | 구성요소 | active | - |
| **M36** | 구성요소 | active | - |
| **M37** | 구성요소 | active | - |
| **M38** | 구성요소 | active | - |
| **M39** | 구성요소 | active | - |
| **M40** | 구성요소 | active | - |
| **M41** | 구성요소 | active | - |
| **M42** | 구성요소 | active | - |
| **M43** | 구성요소 | active | - |
| **M44** | 3중 접지 | active | - |
| **M45** | 3중 접지 | active | - |
| **M46** | 3중 접지 | active | - |
| **M47** | 3중 접지 | active | - |
| **M48** | 3중 접지 | active | - |
| **M49** | 3중 접지 | active | - |
| **M50** | 3중 접지 | active | - |
| **M51** | 3중 접지 | active | - |
| **M52** | 3중 접지 | active | - |
| **M53** | 3중 접지 | active | - |
| **M54** | 3중 접지 | active | - |
| **M55** | 3중 접지 | active | - |
| **M56** | 3중 접지 | active | - |
| **M57** | 3중 접지 | active | - |
| **M58** | 3중 접지 | active | - |
| **M59** | 3중 접지 | active | - |
| **M60** | 3중 접지 | active | - |
| **M61** | 3중 접지 | active | - |
| **M62** | 3중 접지 | active | - |
| **M63** | 3중 접지 | active | - |
| **M64** | 3중 접지 | active | - |
| **M65** | 3중 접지 | active | - |
| **M66** | 3중 접지 | active | - |
| **M67** | 3중 접지 | active | - |
| **M68** | 3중 접지 | active | - |
| **M69** | 3중 접지 | active | - |
| **M70** | 3중 접지 | active | - |
| **M71** | 3중 접지 | active | - |
| **M72** | 3중 접지 | active | - |
| **M73** | 3중 접지 | active | - |
| **M74** | 3중 접지 | active | - |
| **M75** | 3중 접지 | active | - |
| **M76** | 3중 접지 | active | - |
| **M77** | 3중 접지 | active | - |
| **M78** | 3중 접지 | active | - |
| **M79** | 3중 접지 | active | - |
| **M80** | 3중 접지 | active | - |
| **M81** | 3중 접지 | active | - |
| **M82** | 3중 접지 | active | - |
| **M83** | 3중 접지 | active | - |
| **M84** | 3중 접지 | active | - |
| **M85** | 3중 접지 | active | - |
| **M86** | 3중 접지 | active | - |
| **M87** | 수치 사실 | active | - |
| **M88** | 수치 사실 | active | - |
| **M89** | 수치 사실 | active | - |
| **M90** | 수치 사실 | active | - |
| **M91** | 수치 사실 | active | - |
| **M92** | 수치 사실 | active | - |
| **M93** | 수치 사실 | active | - |
| **M94** | 수치 사실 | active | - |
| **M95** | 수치 사실 | active | - |
| **M96** | 수치 사실 | active | - |
| **M97** | 수치 사실 | active | - |
| **M98** | 수치 사실 | active | - |
| **M99** | 수치 사실 | active | - |
| **M100** | 수치 사실 | active | - |
| **M101** | 수치 사실 | active | - |
| **M102** | 수치 사실 | active | - |
| **M103** | 수치 사실 | active | - |
| **M104** | 수치 사실 | active | - |
| **M105** | 수치 사실 | active | - |
| **M106** | 수치 사실 | active | - |
| **M107** | 수치 사실 | active | - |
| **M108** | 수치 사실 | active | - |
| **M109** | 수치 사실 | active | - |
| **M110** | 수치 사실 | active | - |
| **M111** | 수치 사실 | active | - |
| **M112** | 수치 사실 | active | - |
| **M113** | 수치 사실 | active | - |
| **M114** | 수치 사실 | active | - |
| **M115** | 수치 사실 | active | - |
| **M116** | 수치 사실 | active | - |
| **M117** | 수치 사실 | active | - |
| **M118** | 수치 사실 | active | - |
| **M119** | 수치 사실 | active | - |
| **M120** | 수치 사실 | active | - |
| **M121** | 수치 사실 | active | - |
| **M122** | 기술적 함의 | active | - |
| **M123** | 기술적 함의 | active | - |
| **M124** | 기술적 함의 | active | - |
| **M125** | 기술적 함의 | active | - |
| **M126** | 기술적 함의 | active | - |
| **M127** | 기술적 함의 | active | - |
| **M128** | 기술적 함의 | active | - |
| **M129** | 기술적 함의 | active | - |
| **M130** | 기술적 함의 | active | - |
| **M131** | 기술적 함의 | active | - |
| **M132** | 기술적 함의 | active | - |
| **M133** | 포지셔닝 | active | - |
| **M134** | 포지셔닝 | active | - |
| **M135** | 포지셔닝 | active | - |
| **M136** | 도면 주석 | active | - |
| **M137** | 도면 주석 | active | - |
| **M138** | 도면 주석 | active | - |
| **M139** | 도면 주석 | active | - |
| **M140** | 도면 주석 | active | - |
| **M141** | 도면 주석 | active | - |
| **M142** | 도면 주석 | active | - |
| **M143** | 도면 주석 | active | - |
| **M144** | 도면 주석 | active | - |
| **M145** | 도면 주석 | active | - |
| **M146** | 도면 주석 | active | - |
| **M147** | 도면 주석 | active | - |

## 16. 절차 이력

| 항목 | 값 |
|---|---|
| 독립 실행 | read-a:canonical, read-b:convergence-peer |
| 정본 실행 | `read-a` |
| 정본 지정 규칙 | `declaration-order` · 내용맹 `True` |
| 산출 시각 | 2026-08-18T06:44:14Z |
| 엔진 커밋 | `83490945c222379fe90f94eecd40fb96fefdea93` |

분해는 **두 독립 실행**이 돌았고, 접지 이후는 **정본 1개**만 돌았다(재정 P-4).
정본 지정은 선언 순서이며 **내용을 보지 않는다** — 수렴 통과는 두 독해가 동치라는
선언이므로 정본 선택에 판정자가 없고, 남는 요구는 재현성뿐이기 때문이다. 두 실행은
서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.
