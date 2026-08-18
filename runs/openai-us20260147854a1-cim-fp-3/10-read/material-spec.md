# CP1 판독본 (KR 틀 · EN 값) — `openai-us20260147854a1-cim-fp-3` (판 1)

상태 `draft` · 스키마 `material-spec/v0` · reader `0.6.0`

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

- `CL-12/e1` → **M10** — adding, by a half adder in a column cell of the CIM macro, an exponent bit of an activation value and an exponent bit of a weight value to output a carry-out bit and a sum bit
- `CL-12/e2` → **M11** — selecting, by a first multiplexer in the column cell, zero or a prior stage carry-out bit from a prior stage half adder to output a first selection to a full adder
- `CL-12/e3` → **M12** — selecting, by a second multiplexer in the column cell, zero or the sum bit to output a second selection to the full adder
- `CL-12/e4` → **M13** — selecting, by a third multiplexer in the column cell, zero or a carry-in bit from a prior stage full adder to output a third selection to the full adder
- `CL-12/e5` → **M14** — outputting an exponent bit of a primitive product between the activation value and the weight value

### 독립항 `CL-20`

> A system comprising: a compute device configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode device configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein the compute device comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer, and the third multiplexer perform respective selections based on control signals according to the mode.

- `CL-20/e1` → **M15** — a compute device configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values
  - `CL-20/e1/e1` → **M16** — a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit
  - `CL-20/e1/e2` → **M17** — a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder
  - `CL-20/e1/e3` → **M18** — a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder
  - `CL-20/e1/e4` → **M19** — a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder
  - `CL-20/e1/e5` → **M20** — wherein the first multiplexer, the second multiplexer, and the third multiplexer perform respective selections based on control signals according to the mode
- `CL-20/e2` → **M21** — a mode device configured to provide a mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values
  - `CL-20/e2/e1` → **M22** — the first floating point format and the second floating point format being flexible

### 종속항 `CL-2` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder.

- `CL-2/a1` (부착: `CL-1/e3`) → **M23** — wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder

### 종속항 `CL-3` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein the column cell further comprises a plurality of memory cells configured to store the weight value.

- `CL-3/a1` (부착: `CL-1/e3`) → **M24** — wherein the column cell further comprises a plurality of memory cells configured to store the weight value

### 종속항 `CL-4` — `single` (인용: CL-3)

> The hardware accelerator according to claim 3, wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder.

- `CL-4/a1` (부착: `CL-1/e3`) → **M25** — wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder

### 종속항 `CL-5` — `single` (인용: CL-3)

> The hardware accelerator according to claim 3, wherein: one of the plurality of memory cells comprises a first bitcell and a second bitcell, and the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline.

- `CL-5/a1` (부착: `CL-1/e3`) → **M26** — one of the plurality of memory cells comprises a first bitcell and a second bitcell
- `CL-5/a2` (부착: `CL-1/e3`) → **M27** — the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline

### 종속항 `CL-6` — `single` (인용: CL-5)

> The hardware accelerator according to claim 5, wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines.

- `CL-6/a1` (부착: `CL-1/e3`) → **M28** — wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines

### 종속항 `CL-7` — `single` (인용: CL-5)

> The hardware accelerator according to claim 5, wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value.

- `CL-7/a1` (부착: `CL-1/e3`) → **M29** — wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value

### 종속항 `CL-8` — `single` (인용: CL-7)

> The hardware accelerator according to claim 7, wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value.

- `CL-8/a1` (부착: `CL-1/e3`) → **M30** — wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value

### 종속항 `CL-9` — `unclassified` (인용: CL-8)

> The hardware accelerator according to claim 8, wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder.

- `CL-9/a1` (부착: `CL-1/e3`) → **M31** — wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder

### 종속항 `CL-10` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5.

- `CL-10/a1` (부착: `CL-1/e3/e1`) → **M32** — wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5

### 종속항 `CL-11` — `single` (인용: CL-1)

> The hardware accelerator according to claim 1, wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5.

- `CL-11/a1` (부착: `CL-1/e3/e1`) → **M33** — wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5

### 종속항 `CL-13` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: controlling the selections performed by the first multiplexer, the second multiplexer, and the third multiplexer based on control signals according to an arithmetic mode of the VMM operation.

- `CL-13/a1` (부착: `CL-12/e2`) → **M34** — controlling the selections performed by the first multiplexer, the second multiplexer, and the third multiplexer based on control signals according to an arithmetic mode of the VMM operation

### 종속항 `CL-14` — `single` (인용: CL-13)

> The method according to claim 13, further comprising: determining the arithmetic mode based on a first floating point format of the activation value and a second floating point format of the weight value.

- `CL-14/a1` (부착: `CL-12/e2`) → **M35** — determining the arithmetic mode based on a first floating point format of the activation value and a second floating point format of the weight value

### 종속항 `CL-15` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder; and outputting, by the fourth multiplexer in the column cell, an exponent bit of the primitive product.

- `CL-15/a1` (부착: `CL-12/e1`) → **M36** — selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder
- `CL-15/a2` (부착: `CL-12/e5`) → **M37** — outputting, by the fourth multiplexer in the column cell, an exponent bit of the primitive product

### 종속항 `CL-16` — `single` (인용: CL-12)

> The method according to claim 12, further comprising: providing, by a first bitcell in the column cell, the exponent bit of the weight value to the half adder.

- `CL-16/a1` (부착: `CL-12/e1`) → **M38** — providing, by a first bitcell in the column cell, the exponent bit of the weight value to the half adder

### 종속항 `CL-17` — `single` (인용: CL-16)

> The method according to claim 16, further comprising: writing, concurrently, a further exponent bit of a further weight value to a second bitcell in the column cell, wherein the further weight value is different from the weight value.

- `CL-17/a1` (부착: `CL-12/e1`) → **M39** — writing, concurrently, a further exponent bit of a further weight value to a second bitcell in the column cell, wherein the further weight value is different from the weight value

### 종속항 `CL-18` — `single` (인용: CL-17)

> The method according to claim 17, further comprising: writing the further exponent bit to the second bitcell through a bitline shared with the first bitcell.

- `CL-18/a1` (부착: `CL-12/e1`) → **M40** — writing the further exponent bit to the second bitcell through a bitline shared with the first bitcell

### 종속항 `CL-19` — `single` (인용: CL-12)

> The method according to claim 12, wherein: a number of exponent bits in the activation value is at least one of 2, 3, 4, or 5; a number of exponent bits in the weight value is at least one of 2, 3, 4, or 5; and the method further comprises determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value.

- `CL-19/a1` (부착: `CL-12/e1`) → **M41** — a number of exponent bits in the activation value is at least one of 2, 3, 4, or 5
- `CL-19/a2` (부착: `CL-12/e1`) → **M42** — a number of exponent bits in the weight value is at least one of 2, 3, 4, or 5
- `CL-19/a3` (부착: `CL-12/e1`) → **M43** — the method further comprises determining a number of bitcells in the column cell using a least common multiple among a plurality of possible number of exponent bits in the activation value and the weight value

## 3. 유기적 통합 그림 (D5 ④)

- **M110** (spec · stated) — The multiply itself is moved next to the stored weight: each column cell adds the exponent bits and forms the mantissa partial products beside the bitcell that holds the weight, so the floating point product exists before anything leaves the array.
  - 근거 항목: M1, M4, M44, M47
  - 인용: “directly perform vector matrix multiplication (VMM) between activation values and weight values stored in memory, rather than shuttling data back and forth to a separate arithmetic core”
  - 인용: “computations (e.g., VMM operations) can be directly performed within a memory array to minimize data movement”
- **M111** (claim · stated) — Format choice is not wiring but a control word: the mode decoding unit turns the pair of floating point formats into the select signals of the multiplexers, so one physical adder chain is re-aimed instead of a second one being built.
  - 근거 항목: M2, M9, M35, M45, M77
  - 인용: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 인용: “The arithmetic mode describes the data formats in the streaming operand, the stationary operand, the dot products (including exponents and shifted mantissas) output from the CIM macro **101** and the dequantized dot products output by the output register **108**.”
- **M112** (spec · stated) — The trick that makes one cell cover several formats is padding with zero rather than removing hardware: a bit position that a narrower format does not use is written or selected as zero, so the wide layout stays intact and stays correct.
  - 근거 항목: M3, M22, M46, M65
  - 인용: “To use the same design of column cell **220** as those in FIGS. **7**-**11** to perform element-wise multiplication between FP8 (1-4-3) and FP4 (1-2-1), 2 bits of the weight value in FP6 (1-3-2) format can be ignored by e.g., writing zero to the associated memory cell or using multiplexers.”
  - 인용: “For activation values in lower precisions, some of the bits in the FP8 (1-4-3) formats can be set as zero, similar to the approach described above for weight values in FP4 format.”
- **M113** (claim · inferred) — Sizing the cell by the least common multiple of the supported exponent widths is what turns leftover positions into extra elements instead of dead area, and it is also what makes the price of one more supported width visible.
  - 근거 항목: M43, M86, M32, M33
  - 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2.”
  - 인용: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 인용: “Accordingly, the storage capacity of weight values in one column cell can be increased and the throughput of the column cell can also be increased by pipelining the adder tree through overlapping executions of multiple operations instructions.”
- **M114** (claim · stated) — Doubling the bitcell converts weight loading from a stall into background work: two bitcells share one bitline but answer to different wordlines, so one bank can be written while the other one is multiplying.
  - 근거 항목: M26, M28, M29, M31, M69, M71, M72, M74
  - 인용: “Accordingly, the write operation can be performed concurrently with the VMM operation in the same column cell of the CIM macro.”
  - 인용: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
  - 인용: “The design of memory cell having two or more bitcells allows for storing more weight values, where one weight value can be used for the VMM operation and other weight values can be updated in a parallel operation.”
- **M115** (spec · stated) — The design leaves the floating point domain on purpose after the product: mantissas are shifted against the column maximum exponent and summed as integers, so a single adder tree serves every supported format.
  - 근거 항목: M1, M4
  - 인용: “a second part having a synthesizable (or custom) adder tree **426** (see FIG. **4**) that accumulates the element-wise product in the integer domain (e.g., INT 35 and INT5 in Table 1)”
  - 인용: “a mantissa alignment process can be performed first to convert the mantissas of the primitive products P.sub.ik from the FP format to INT format.”
- **M116** (spec · stated) — The same latches that hold weights are re-used as scan chain elements under a mode signal, so testability is bought by re-timing existing storage rather than by adding a second set of cells.
  - 근거 항목: M26, M27, M69, M70
  - 인용: “The combination of scan multiplexers **4711** and **4713**, scan clock clk_scan, and scan mode signal sm can allow memory cell **4703** to share the same storage elements for both functional and test purposes while isolating the routing and timing of the scan clock from the normal computation path.”
- **M117** (effects · stated) — The disclosure prices its own flexibility rather than hiding it: the extra multiplexers and the zeros stored in unused bitcells are named as overhead, and the argument is that the overhead sits in a part of the budget small enough to absorb it.
  - 근거 항목: M6, M7, M8, M9, M49, M50, M51, M52
  - 인용: “exponent computation for the primitive products can be optimized to support multiple FP format options with some overhead in the exponent handling or computation by using extra multiplexers and global control signals.”
  - 인용: “However, the potential redundancy or waste is not critical because the bitcells and their appended logic circuits are a small portion of the total power, performance and area (PPA) budget.”

## 4. 포지셔닝 (D5 ⑤)

- **M118**
  - 배경 문제: The background section describes accelerators that convert between a high precision software format and a fixed low precision datapath, where every conversion step costs scaling, rounding and saturation logic, and where a new low bit format forces a new pipeline or a dedicated core.
  - 주장 효과: The specification asserts that a compute engine driven by a mode decoding unit executes vector matrix and matrix matrix operations across a range of compact numeric formats without requiring separate conversion pipelines or dedicated cores for each format.
  - 차이: The stated difference is structural rather than a measured speed or power figure: the same half adder, full adder and multiplexer fabric inside the column cell is re-selected per arithmetic mode, and the supported exponent widths are enumerated as two, three, four and five bits.
  - 인용: “Each conversion step requires additional scaling, rounding, and saturation logic, which adds area, power, and latency to already dense compute fabrics, and can introduce cumulative quantization errors that degrade numerical behavior over many layers.”
  - 인용: “As new low-bit formats and variants are introduced to improve efficiency (such as different 8-bit or sub-8-bit floating-point encodings), fixed conversion pipelines and format-specific data paths become increasingly difficult to adapt, limiting the flexibility of the hardware to support evolving models and deployment scenarios.”
  - 인용: “optimized hardware can execute vector-matrix and matrix-matrix operations more efficiently, across a range of compact numeric formats without requiring separate conversion pipelines or dedicated cores for each format”
- **M119**
  - 배경 문제: A compute in memory array holds its weights in place, so changing the weight matrix normally competes with the multiply that is using it, and the array idles while the next matrix is loaded.
  - 주장 효과: The specification asserts that a memory cell built from two bitcells supports a double buffer scheme in which the next matrix of weight values is loaded while the previous one is still in use, and that a write operation is therefore performed concurrently with the vector matrix multiplication in the same column cell.
  - 차이: The stated difference is a second bitcell per memory cell that shares the bitline but is addressed by its own wordline, with a weight select signal deciding which bank is written and which bank is read; no throughput figure is asserted for the overlap.
  - 인용: “the CIM macro **101** can support for a double-buffer scheme (e.g., each memory cell having double bitcells) allowing concurrent loading of the next matrix of weight values while the previous weight values are still in use for the VMM computation.”
  - 인용: “Accordingly, the write operation can be performed concurrently with the VMM operation in the same column cell of the CIM macro.”
- **M120**
  - 배경 문제: The disclosure's own first exponent scheme spends three half adders and three full adders per column cell because the activation and weight exponent bits are added in two stages.
  - 주장 효과: The specification asserts that adding the exponent bits directly instead of in two stages reduces the same computation to two half adders and two full adders per column cell, and it states an array level saving for a thirty two element vector against a thirty two by thirty two weight matrix.
  - 차이: The stated difference is one fewer half adder and one fewer full adder in every column cell, obtained by restructuring where the least significant and most significant exponent positions are handled rather than by changing the numeric format.
  - 인용: “As discussed above with respect to FIG. **9**, three half adders (which are coupled to the memory cells) are used along with three full adders for exponent computation between Act 0 in FP8 (1-4-3) and Wdata 0 in FP6 (1-3-2). As shown in FIG. **14**, logic circuits for this exponent computation may be reduced to 2 half adders and 2 full adders, where exponent bits of the activation value and the weight value can be added directly rather than in a two-stage operation described in FIG. **9**.”
  - 인용: “As such, to perform the VMM operation for the 1×32 vector of activation values and the 32×32 matrix of weight values, 64×64 number of half adders and full adders can be saved.”
- **M121**
  - 배경 문제: Building one cell that serves several floating point formats means that, in any single mode, some bitcells and some adders are carrying values that the mode does not need.
  - 주장 효과: The specification concedes that redundancy or waste exists, asserts that it is not critical because the bitcells and their appended logic are a small portion of the power, performance and area budget, and asserts that storing a zero weight is simple to implement and lets unused sections be power gated for leakage.
  - 차이: The stated difference from a per format design is a trade rather than an elimination: area and stored zeros are spent to keep one layout, and the supported format list is widened instead of the datapath being duplicated.
  - 인용: “There may be redundancy or waste when supporting flexible FP formats. For example, weight value of “0” is stored in the CIM macro **101** in bitcells, and flexible option are provided in computation methods and logic circuit designs.”
  - 인용: “The advantages of storing the weight value “0” includes straightforward design, easy to implement, and power gating for unused sections to save leakage power.”
  - 인용: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”

## 5. 구성요소와 3중 접지 (D5 ③)

| 구성요소 | 청구항 좌표 | 라벨(EN) | 접지 |
|---|---|---|---|
| **M1** | `CL-1/e1` | compute-in-memory (CIM) macro performing a VMM between an activation vector and a weight matrix | **M44** (명세서 found · 도면 found) |
| **M2** | `CL-1/e2` | mode decoding unit deriving the arithmetic mode from the activation and weight floating point formats | **M45** (명세서 found · 도면 found) |
| **M3** | `CL-1/e2/e1` | flexibility of the first and second floating point formats | **M46** (명세서 found · 도면 found) |
| **M4** | `CL-1/e3` | column cell of the CIM macro outputting a primitive product of an activation value and a weight value | **M47** (명세서 found · 도면 found) |
| **M5** | `CL-1/e3/e1` | half adder summing the activation and weight exponent bits into a carry-out bit and a sum bit | **M48** (명세서 found · 도면 found) |
| **M6** | `CL-1/e3/e2` | first multiplexer selecting zero or the prior stage carry-out bit for the full adder | **M49** (명세서 found · 도면 found) |
| **M7** | `CL-1/e3/e3` | second multiplexer selecting zero or the sum bit for the full adder | **M50** (명세서 found · 도면 found) |
| **M8** | `CL-1/e3/e4` | third multiplexer selecting zero or the prior stage carry-in bit for the full adder | **M51** (명세서 found · 도면 found) |
| **M9** | `CL-1/e3/e5` | three multiplexers selecting under control signals set by the arithmetic mode | **M52** (명세서 found · 도면 found) |
| **M10** | `CL-12/e1` | adding the activation and weight exponent bits in a half adder of the column cell | **M53** (명세서 found · 도면 found) |
| **M11** | `CL-12/e2` | first multiplexer selecting zero or the prior stage carry-out bit | **M54** (명세서 found · 도면 found) |
| **M12** | `CL-12/e3` | second multiplexer selecting zero or the sum bit | **M55** (명세서 found · 도면 found) |
| **M13** | `CL-12/e4` | third multiplexer selecting zero or the prior stage carry-in bit | **M56** (명세서 found · 도면 found) |
| **M14** | `CL-12/e5` | outputting the exponent bit of the primitive product | **M57** (명세서 found · 도면 found) |
| **M15** | `CL-20/e1` | compute device performing a VMM between an activation vector and a weight matrix | **M58** (명세서 found · 도면 found) |
| **M16** | `CL-20/e1/e1` | half adder summing the activation and weight exponent bits into a carry-out bit and a sum bit | **M59** (명세서 found · 도면 found) |
| **M17** | `CL-20/e1/e2` | first multiplexer selecting zero or the prior stage carry-out bit for the full adder | **M60** (명세서 found · 도면 found) |
| **M18** | `CL-20/e1/e3` | second multiplexer selecting zero or the sum bit for the full adder | **M61** (명세서 found · 도면 found) |
| **M19** | `CL-20/e1/e4` | third multiplexer selecting zero or the prior stage carry-in bit for the full adder | **M62** (명세서 found · 도면 found) |
| **M20** | `CL-20/e1/e5` | three multiplexers selecting under control signals set by the mode | **M63** (명세서 found · 도면 found) |
| **M21** | `CL-20/e2` | mode device deriving the VMM mode from the activation and weight floating point formats | **M64** (명세서 found · 도면 found) |
| **M22** | `CL-20/e2/e1` | flexibility of the first and second floating point formats | **M65** (명세서 found · 도면 found) |
| **M23** | `CL-2/a1` | fourth multiplexer outputting the primitive product exponent bit | **M66** (명세서 found · 도면 found) |
| **M24** | `CL-3/a1` | plurality of memory cells storing the weight value | **M67** (명세서 found · 도면 found) |
| **M25** | `CL-4/a1` | memory cell bitcell holding the weight exponent bit and feeding the half adder | **M68** (명세서 found · 도면 found) |
| **M26** | `CL-5/a1` | memory cell made of a first bitcell and a second bitcell | **M69** (명세서 found · 도면 found) |
| **M27** | `CL-5/a2` | first and second bitcells addressed by different wordlines | **M70** (명세서 found · 도면 found) |
| **M28** | `CL-6/a1` | first and second bitcells sharing a bitline under different wordlines | **M71** (명세서 found · 도면 found) |
| **M29** | `CL-7/a1` | two bitcells holding bits of two different weight values | **M72** (명세서 found · 도면 found) |
| **M30** | `CL-8/a1` | first bitcell supplying the weight exponent bit to the half adder | **M73** (명세서 found · 도면 found) |
| **M31** | `CL-9/a1` | second bitcell updated while the first bitcell drives the half adder | **M74** (명세서 found · 도면 found) |
| **M32** | `CL-10/a1` | activation exponent bit count of 2, 3, 4 or 5 | **M75** (명세서 found · 도면 found) |
| **M33** | `CL-11/a1` | weight exponent bit count of 2, 3, 4 or 5 | **M76** (명세서 found · 도면 found) |
| **M34** | `CL-13/a1` | control signals steering the three multiplexer selections per arithmetic mode | **M77** (명세서 found · 도면 found) |
| **M35** | `CL-14/a1` | arithmetic mode determined from the two floating point formats | **M78** (명세서 found · 도면 found) |
| **M36** | `CL-15/a1` | fourth multiplexer selecting among full adder output, sum bit and carry-in bit | **M79** (명세서 found · 도면 found) |
| **M37** | `CL-15/a2` | fourth multiplexer outputting the primitive product exponent bit | **M80** (명세서 found · 도면 found) |
| **M38** | `CL-16/a1` | first bitcell providing the weight exponent bit to the half adder | **M81** (명세서 found · 도면 found) |
| **M39** | `CL-17/a1` | concurrent write of a further weight exponent bit into a second bitcell | **M82** (명세서 found · 도면 found) |
| **M40** | `CL-18/a1` | further exponent bit written through the shared bitline | **M83** (명세서 found · 도면 found) |
| **M41** | `CL-19/a1` | activation exponent bit count of 2, 3, 4 or 5 | **M84** (명세서 found · 도면 found) |
| **M42** | `CL-19/a2` | weight exponent bit count of 2, 3, 4 or 5 | **M85** (명세서 found · 도면 found) |
| **M43** | `CL-19/a3` | bitcell count from the least common multiple of the possible exponent bit counts | **M86** (명세서 found · 도면 found) |

- **M44** ← 구성요소 M1
  - 명세서 `[0128]`: “For example, CIM macro **101** can support a Vector Matrix Multiplication (VMM) operation between a vector of activation values and a matrix of weight values.”
  - 명세서 `[0136]`: “Each column of computing unit **222** in the CIM macro **101** drives a dot product operation during an VMM operation.”
  - 도면 `FIG-2` (도면부호 101, 222, 220): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M45** ← 구성요소 M2
  - 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
  - 명세서 `[0063]`: “A mode decoding unit can supply an arithmetic mode that may reflect the floating-point formats chosen for activations and weights, allowing the accelerator to support multiple “flexible” low-precision formats without redesigning the datapath.”
  - 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M46** ← 구성요소 M3
  - 명세서 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
  - 명세서 `[0188]`: “FIG. **28** illustrates an exemplary design of the column cell **220** for handling exponents of the flexible FP data.”
  - 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FP 포맷의 유연성 자체를 그리는 도면은 회로도가 아니라 Table 2(FIG. **60**) 이다 — [0057] 캡션과 [0183] 의 Table 2 지시를 대조해 FIG-60 을 도면 자리로 잡았고, 회로 쪽 조응은 FIG. **28**(flexible FP data) 으로 보완했다.
- **M47** ← 구성요소 M4
  - 명세서 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
  - 명세서 `[0149]`: “Step S1: multiplying, by each column cell **220** of the CIM macro **101**, a corresponding activation value a.sub.i and a corresponding weight value w.sub.ik to produce an element-wise primitive product P.sub.ik=a.sub.i×w.sub.ik, with specific handling method for the signs, exponents and mantissas of the activation value a.sub.i and the weight value w.sub.ik.”
  - 도면 `FIG-3` (도면부호 220, 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-2` (도면부호 220, 222): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
- **M48** ← 구성요소 M5
  - 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M49** ← 구성요소 M6
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2862, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M50** ← 구성요소 M7
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 도면 `FIG-28` (도면부호 2860, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M51** ← 구성요소 M8
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M52** ← 구성요소 M9
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M53** ← 구성요소 M10
  - 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M54** ← 구성요소 M11
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M55** ← 구성요소 M12
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M56** ← 구성요소 M13
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M57** ← 구성요소 M14
  - 명세서 `[0188]`: “The resulting exponent bits of the primitive product include the sum bit S.sub.LSB from the half adder for the LSBs of the exponents of the activation value and the weight value, the exponent bits E.sub.j output from the fourth multiplexers **2866**, and the carry-in bit CIN.sub.MSB from the last stage full adder for the MSB of the exponent of the activation value and/or the MSB of the exponent of the weight value.”
  - 명세서 `[0166]`: “The full adders can be connected in series, where each full adder can output an exponent bit of the primitive product and a carry-in bit for the next stage full adder.”
  - 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M58** ← 구성요소 M15
  - 명세서 `[0017]`: “For example, in the disclosed technology a system may be provided that performs vector-matrix multiplication using a compute device that generates portions of a floating-point product directly within memory structures.”
  - 명세서 `[0072]`: “At the system level, the disclosed technology may be implemented in a compute device that can house the exponent-processing hardware described above, while a mode device provides the control mode based on the selected floating-point formats for activations and weights.”
  - 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-2` (도면부호 101, 222): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
- **M59** ← 구성요소 M16
  - 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
  - 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
  - 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- **M60** ← 구성요소 M17
  - 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2862, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M61** ← 구성요소 M18
  - 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
  - 도면 `FIG-28` (도면부호 2860, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.
- **M62** ← 구성요소 M19
  - 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
  - 도면 `FIG-28` (도면부호 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- **M63** ← 구성요소 M20
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M64** ← 구성요소 M21
  - 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
  - 명세서 `[0072]`: “This split can allow the compute device to focus on dense, fast arithmetic and the mode device to handle configuration and format-aware control.”
  - 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- **M65** ← 구성요소 M22
  - 명세서 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
  - 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
  - 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
  - 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 탐색 기록: FP 포맷의 유연성 자체를 그리는 도면은 회로도가 아니라 Table 2(FIG. **60**) 이다 — [0057] 캡션과 [0183] 의 Table 2 지시를 대조해 FIG-60 을 도면 자리로 잡았고, 회로 쪽 조응은 FIG. **28**(flexible FP data) 으로 보완했다.
- **M66** ← 구성요소 M23
  - 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product: the output of the full adder, the sum output of the half adder, or a carry-in from an upstream stage.”
  - 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
  - 도면 `FIG-28` (도면부호 2866, 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M67** ← 구성요소 M24
  - 명세서 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
  - 명세서 `[0140]`: “Each memory cell stores one bit of the weight value.”
  - 도면 `FIG-3` (도면부호 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro”
- **M68** ← 구성요소 M25
  - 명세서 `[0065]`: “Further, one of these memory cells may serve as a bitcell dedicated to holding the exponent bit of the weight value and feeding this bit directly to the half adder.”
  - 명세서 `[0188]`: “In FIG. **28**, each bitcell stores a corresponding exponent bit of the weight value.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M69** ← 구성요소 M26
  - 명세서 `[0066]`: “a memory cell can be realized as a pair of bitcells”
  - 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M70** ← 구성요소 M27
  - 명세서 `[0066]`: “where each bitcell may be addressed by its own wordline, enabling independent selection of two stored bits.”
  - 명세서 `[0217]`: “where bitcell BC0 can be addressed by wordline wwl0 and bitcell BC1 can be address by wordline wwl1.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M71** ← 구성요소 M28
  - 명세서 `[0066]`: “Further, paired bitcells may share a common bitline while still being controlled by different wordlines.”
  - 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M72** ← 구성요소 M29
  - 명세서 `[0067]`: “a first bitcell may hold a first bit of one weight value, and a second bitcell may hold a second bit of a different weight value.”
  - 명세서 `[0218]`: “bitcell BC0 can store a first bit of a first weight value and bitcell BC1 can store a second bit of a second weight value that is different from the first weight value.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M73** ← 구성요소 M30
  - 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
  - 명세서 `[0089]`: “one exponent bit may be stored in a bitcell and delivered to the first half adder, second half adder, or a full adder depending on its exponent position.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M74** ← 구성요소 M31
  - 명세서 `[0067]`: “Further, while the first bitcell is driving the exponent bit into the half adder, the second bitcell can be updated with a new bit of another weight value.”
  - 명세서 `[0087]`: “while one bitcell is feeding its exponent bit into the adder chain, the further bitcell may be updated with a new exponent bit of a different weight.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M75** ← 구성요소 M32
  - 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M76** ← 구성요소 M33
  - 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M77** ← 구성요소 M34
  - 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
  - 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
  - 도면 `FIG-28` (도면부호 2860, 2862, 2864, 110, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M78** ← 구성요소 M35
  - 명세서 `[0095]`: “a mode decoding unit may be included to set an arithmetic mode for the CIM macro based on floating-point formats of the activation and weight.”
  - 명세서 `[0146]`: “the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
  - 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator”
- **M79** ← 구성요소 M36
  - 명세서 `[0070]`: “the method may describe using a fourth multiplexer to choose between different exponent results produced inside the column cell. For example, the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage”
  - 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
  - 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M80** ← 구성요소 M37
  - 명세서 `[0070]`: “using a fourth multiplexer to choose between different exponent results produced inside the column cell. For example, the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage, and present that as the exponent bit of the primitive product.”
  - 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product”
  - 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M81** ← 구성요소 M38
  - 명세서 `[0071]`: “Methods disclosed herein may also include sourcing the exponent bit of the weight value directly from a dedicated bitcell inside the column, which can feed that bit to the half adder.”
  - 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
  - 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M82** ← 구성요소 M39
  - 명세서 `[0071]`: “At the same time that the first bitcell is supplying a weight exponent bit to the half adder, the method may allow writing a new exponent bit for a different weight into a second bitcell.”
  - 명세서 `[0087]`: “while one bitcell is feeding its exponent bit into the adder chain, the further bitcell may be updated with a new exponent bit of a different weight.”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M83** ← 구성요소 M40
  - 명세서 `[0071]`: “For example, a second exponent bit may be written through a bitline shared with the first bitcell, simplifying the array wiring.”
  - 명세서 `[0231]`: “a weight value to be written/updated (e.g., wgt_data) can be provided to a set of bit lines BL shared by the first set of bitcells BC0 and the second set of bitcells BC1”
  - 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”
- **M84** ← 구성요소 M41
  - 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M85** ← 구성요소 M42
  - 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”
- **M86** ← 구성요소 M43
  - 명세서 `[0071]`: “The method may also size the number of bitcells in the column based on the least common multiple of supported exponent bit widths for activations and weights”
  - 명세서 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

## 6. 수치 사실 — 3분류 (재정 N9)

기계가 **무엇을 보증했는가**가 갈래마다 다르다. 갈래를 섞어 보면 승인은 형식이 된다.

### 6.1 원문 스팬 수치 (`quoted` · `bibliographic`)

- 원문 스팬 수치: **17건** — M87, M88, M89, M90, M91, M92, M93, M94, M95, M96, M97, M98, M99, M100, M101, M102, M103
- 서지 복사: M100, M101, M102, M103 (`patent` 블록에서 결정론 복사)

- **M87** — numeric value at [0186] · `2` → `2`
  - 원천 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M88** — numeric value at [0140] · `0` → `0`
  - 원천 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
- **M89** — numeric value at [0140] · `0` → `0`
  - 원천 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
- **M90** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
- **M91** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M92** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M93** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M94** — numeric value at [0189] · `5, 4, 3, and 2` → `5;4;3;2`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M95** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- **M96** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M97** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M98** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M99** — numeric value at [0189] · `4, 3, and 2` → `4;3;2`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M100** — bibliographic field patent.number · `US20260147854A1` → `US20260147854A1`
  - 원천 ``: “”
- **M101** — bibliographic field patent.dates.priority · `2024-11-22` → `2024-11-22`
  - 원천 ``: “”
- **M102** — bibliographic field patent.dates.filing · `2025-11-21` → `2025-11-21`
  - 원천 ``: “”
- **M103** — bibliographic field patent.dates.publication · `2026-05-28` → `2026-05-28`
  - 원천 ``: “”

### 6.2 파생 수치 (`derived`) — 산식과 원천 스팬을 나란히

- **M104** — cell count of the shared column cell sized by the least common multiple of the 4-bit, 3-bit and 2-bit exponent widths · `144` → `144`
  - 산식: `columns * rows` (깊이 1)
  - 입력 `columns` ← **M96** (`12`) — 원천 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 입력 `rows` ← **M97** (`12`) — 원천 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - ★ 이 값은 **원문 어디에도 문자열로 없다.** 계산의 결과다.
- **M105** — cell count of the shared column cell sized by the least common multiple of the 5-bit, 4-bit, 3-bit and 2-bit exponent widths · `3600` → `3600`
  - 산식: `columns * rows` (깊이 1)
  - 입력 `columns` ← **M91** (`60`) — 원천 인용: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 입력 `rows` ← **M92** (`60`) — 원천 인용: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - ★ 이 값은 **원문 어디에도 문자열로 없다.** 계산의 결과다.
- **M106** — growth factor in column cell area when the supported exponent widths are extended from three widths to four · `25` → `25`
  - 산식: `(wide_columns * wide_rows) / (narrow_columns * narrow_rows)` (깊이 1)
  - 입력 `wide_columns` ← **M91** (`60`) — 원천 인용: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 입력 `wide_rows` ← **M92** (`60`) — 원천 인용: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 입력 `narrow_columns` ← **M96** (`12`) — 원천 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 입력 `narrow_rows` ← **M97** (`12`) — 원천 인용: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - ★ 이 값은 **원문 어디에도 문자열로 없다.** 계산의 결과다.

### 6.3 도면 유래 수치 (`figure-sourced`) — 기계 검증 불가

- **M107** — operation modes tabulated in Table 2 of FIG. 60 · `8` → `8`
  - 도면 `FIG-60` · `machine_verifiable: false` — **기계 검증 불가**
- **M108** — weight-bit groups drawn inside the twelve-column shared cell of FIG. 29 · `3` → `3`
  - 도면 `FIG-29` · `machine_verifiable: false` — **기계 검증 불가**
- **M109** — multiplexers drawn per exponent stage in FIG. 28 · `4` → `4`
  - 도면 `FIG-28` · `machine_verifiable: false` — **기계 검증 불가**

## 7. ★ 사람 검증 필요 목록 (재정 R1)

도면에서 읽은 값은 기계가 대조할 원문 스팬이 없다. **검사가 통과시켰다는 사실이 값이**
**옳다는 뜻이 아니다.** 아래 목록은 봉투의 `manual_verification_ack[]` 와 정확히 일치해야 한다.

- **M107** — operation modes tabulated in Table 2 of FIG. 60 · 값 `8` · 도면 `FIG-60` (도면부호 ) · 사유 `figure-sourced`
- **M108** — weight-bit groups drawn inside the twelve-column shared cell of FIG. 29 · 값 `3` · 도면 `FIG-29` (도면부호 220) · 사유 `figure-sourced`
- **M109** — multiplexers drawn per exponent stage in FIG. 28 · 값 `4` · 도면 `FIG-28` (도면부호 220, 830, 2860, 2862, 2864, 2866) · 사유 `figure-sourced`

## 8. ★ 접지 예외 (재정 R3)

접지 전량이 원칙이므로 예외는 날조하거나 숨기지 않고 드러낸다. **예외가 많으면 그것이**
**소재 신호다.**

_예외 없음 — 전 구성요소가 명세서·도면 양쪽에 접지되었다._


## 9. drop 신호 (D4 — 최종)

- 단계: `final` · 판정: `go`
- 사유: 안도감 적합. 하나의 그림으로 이어진다 — 곱셈을 메모리 옆으로 옮기고, 포맷이 바뀌면 배선이 아니라 제어어를 바꾸며, 쓰지 않는 비트 자리는 없애는 대신 0을 채워 한 벌의 레이아웃을 지킨다. '지원 폭의 최소공배수로 셀을 잡는다'는 한 문장이 12와 60이라는 두 숫자로 곧바로 만져지고, 그 대가(멀티플렉서 증가·빈 비트셀에 저장된 0)를 명세서가 스스로 인정한다는 점에서 과장 없는 서사가 선다. 이중 비트셀은 '쓰는 동안 계산한다'는 일상 비유로 바로 옮겨지고, 도면도 FIG-1 전경에서 FIG-28/29 단면까지 축척이 이어져 전시물이 부족하지 않다.

## 10. ★ 미분류 종속 구조 (재정 P-1)

Markush·조건부·수단항·카테고리 전환은 typed operator 입법을 범위에서 **제외**했고,
대신 `unclassified` 표지 + 이 목록 + 판정 행 계수 셋으로 침묵을 막는다.
**이 목록의 항목은 결함이 아니다** — 구조 미분류라는 사실의 표지이며, 종속 형태
판정(`parse.set-equals`·`parse.type-agrees`)의 대상에서 빠졌다는 뜻이다. 전문은
이미 보존되어 있으므로(재정 R1) 여기서 사람 눈이 마지막 심급이 된다.

- **`CL-9`** (`unclassified`)
  - 전문: “The hardware accelerator according to claim 8, wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder.”

## 11. ★ 맹검 스크리닝 메모 — 두 실행 병기 (재정 P-A · P-U4)

분해 직후 `read-a`·`read-b` 가 **각자** 적은 1차 판단이다. 상신이 아니었고 런을
세우지 않았으며, 최종 서사 평가 레인에는 비공개였다(앵커링 방지). 둘 다 싣는 이유는
**두 독립 관찰의 일치/불일치 자체가 신호**이기 때문이다 — 한 건으로 합치면 그 신호가
소멸한다.

| 실행 | 방향 | 근거 요지 |
|---|---|---|
| `read-a` | `clear` | 권리 관심이 CIM 컬럼 셀의 지수부 가산 경로 한 곳(반가산기 + 멀티플렉서 3개 → 전가산기)에 뚜렷하게 모여 있고, 그 선택 신호가 활성값·가중치의 부동소수점 포맷(모드)으로 결정된다는 인과가 청구항만으로 끝까지 읽힌다. '포맷이 바뀌어도 회로를 갈아끼우지 않고 배선 선택만 바꾼다'는 한 문장으로 일반 독자에게 안도감을 줄 수 있고, 종속항(비트셀 2개·비트라인 공유·동시 기입·지수 비트 수 2~5·최소공배수 셀 수)이 그 서사의 구체 장면을 그대로 제공한다. |
| `read-b` | `clear` | 권리 관심이 '메모리 셀 안에서 지수부를 반가산기 1개와 멀티플렉서 3개로 더해 부동소수점 포맷을 바꿔 끼운다'는 한 구성(CL-1/e3 계열)에 뚜렷이 몰려 있고, 곱셈을 메모리 밖으로 꺼내지 않는다는 그림이 비전문 독자에게도 한 문장으로 서므로 서사가 설 것으로 봄. |

두 관찰의 방향이 `clear` 로 일치했다.

## 12. ★ 수치 인벤토리 — 전수 수확 (재정 P-B)

수치는 접지 스팬과 서지면에서 **전수 기계 수확**되었고, 중요분은 LLM 의 중요도
판단이 아니라 함의·포지셔닝이 실제로 참조했는가(`numeric_refs`)로 **역참조 도출**된다.

**수확 정답지 17건(kind fact · origin ∈ {quoted, bibliographic} · status active) — 참조 6건 표시, 미참조 11건 접힘**

_카운트를 상시 표기하는 이유: 카운트가 없으면 미참조분 접힘이 은폐가 된다._

역참조 총 12건 중 **6건이 이 정답지 밖**이다 — M107, M104, M105, M106, M108, M109. 정답지 밖 참조는 수확기 소유가 아닌 수치(`derived`·`figure-sourced`)이거나
철회·대체된 항목이며, 위 계수에 들지 않는다.

### 12.1 참조된 수치 (함의·포지셔닝의 근거)

- **M90** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
  - 이 수치를 참조한 항목: M112, M118
- **M93** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 이 수치를 참조한 항목: M113
- **M94** — numeric value at [0189] · `5, 4, 3, and 2` → `5;4;3;2`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
  - 이 수치를 참조한 항목: M113
- **M95** — numeric value at [0068] · `2, 3, 4, or 5` → `2;3;4;5`
  - 원천 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
  - 이 수치를 참조한 항목: M112, M118
- **M98** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 이 수치를 참조한 항목: M113
- **M99** — numeric value at [0189] · `4, 3, and 2` → `4;3;2`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
  - 이 수치를 참조한 항목: M113

### 12.2 미참조 수치 11건 (접힘 — 숨김이 아니다)

<details>
<summary>미참조 11건 펼치기</summary>

- **M87** — numeric value at [0186] · `2` → `2`
  - 원천 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- **M88** — numeric value at [0140] · `0` → `0`
  - 원천 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
- **M89** — numeric value at [0140] · `0` → `0`
  - 원천 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
- **M91** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M92** — numeric value at [0189] · `60` → `60`
  - 원천 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- **M96** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M97** — numeric value at [0189] · `12` → `12`
  - 원천 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- **M100** — bibliographic field patent.number · `US20260147854A1` → `US20260147854A1`
- **M101** — bibliographic field patent.dates.priority · `2024-11-22` → `2024-11-22`
- **M102** — bibliographic field patent.dates.filing · `2025-11-21` → `2025-11-21`
- **M103** — bibliographic field patent.dates.publication · `2026-05-28` → `2026-05-28`

</details>

★ 미참조 수치를 본문이 처음 인용하면 CP2 에 **"미검토 수치 사용" 플래그**가 자동
첨부된다(재정 P-B). 무검토 게시 경로는 없다 — 모든 수치는 CP1 검토 또는 사용 시 검토다.

### 12.3 수확하지 못한 토큰 89건 (숨기지 않고 센다)

수확 전 단계에서 갈린 자리를 **전부** 싣는다. 세 갈래에서 온다 — ① 좌표 표현 봉투
배제(FP 3항 표기·비트 슬라이스·도면/표 번호·아래첨자 인덱스) ② 토큰 경계 기각
(`cm3` 의 `3` 처럼 영숫자 토큰 내부) ③ 값 문법 파싱 실패. 시끄럽게 실패하되
스테이지를 죽이지 않는다 — 수확은 검사가 아니다.

사유 라벨의 정본은 `reader/reader-rules.yaml#numeric_harvest` 의
`exclusions[].reason_label` 과 `token_boundary.rejection_labels` 다.

★ **배제 구간 수와 사라진 수치 수는 다르다.** 봉투 하나가 여러 수확을 막을 수 있다
(예: `Act 0 <6:3>` 한 구간이 `0`·`<6`·`3` 셋을 막는다). 아래 소계는 **구간**을 센다.

| 사유 | 건수 |
|---|---|
| `figure-numeral` | 34 |
| `boundary-left` | 30 |
| `coordinate-triple` | 9 |
| `figure-or-table-number` | 7 |
| `boundary-right` | 4 |
| `bit-slice` | 3 |
| `subscript-index` | 2 |

<details>
<summary>전건 89건 펼치기</summary>

| 위치 | 토큰 | 사유 |
|---|---|---|
| `[0128]` | `101` | figure-numeral |
| `[0136]` | `222` | figure-numeral |
| `[0136]` | `101` | figure-numeral |
| `[0146]` | `100` | figure-numeral |
| `[0146]` | `110` | figure-numeral |
| `[0146]` | `101` | figure-numeral |
| `[0186]` | `100` | figure-numeral |
| `[0188]` | `220` | figure-numeral |
| `[0137]` | `220` | figure-numeral |
| `[0149]` | `220` | figure-numeral |
| `[0149]` | `101` | figure-numeral |
| `[0188]` | `2862` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2862` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0188]` | `110` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0183]` | `101` | figure-numeral |
| `[0188]` | `830` | figure-numeral |
| `[0188]` | `2866` | figure-numeral |
| `[0188]` | `2860` | figure-numeral |
| `[0188]` | `2864` | figure-numeral |
| `[0140]` | `340` | figure-numeral |
| `[0140]` | `101` | figure-numeral |
| `[0217]` | `4303` | figure-numeral |
| `[0217]` | `4303` | figure-numeral |
| `[0189]` | `220` | figure-numeral |
| `[0146]` | `100` | figure-numeral |
| `[0146]` | `110` | figure-numeral |
| `[0146]` | `101` | figure-numeral |
| `[0189]` | `220` | figure-numeral |
| `[0186]` | `8` | boundary-left |
| `[0186]` | `6` | boundary-left |
| `[0186]` | `4` | boundary-left |
| `[0186]` | `Tables 1` | figure-or-table-number |
| `[0186]` | `8` | boundary-left |
| `[0186]` | `8` | boundary-left |
| `[0186]` | `(1-5-2)` | coordinate-triple |
| `[0186]` | `8` | boundary-left |
| `[0186]` | `(1-4-3)` | coordinate-triple |
| `[0186]` | `8` | boundary-left |
| `[0186]` | `(1-3-4)` | coordinate-triple |
| `[0186]` | `6` | boundary-left |
| `[0186]` | `6` | boundary-left |
| `[0186]` | `(1-3-2)` | coordinate-triple |
| `[0186]` | `6` | boundary-left |
| `[0186]` | `(1-2-3)` | coordinate-triple |
| `[0186]` | `4` | boundary-left |
| `[0186]` | `4` | boundary-left |
| `[0186]` | `(1-2-1)` | coordinate-triple |
| `[0186]` | `(1-1-2)` | coordinate-triple |
| `[0188]` | `FIG. **28**` | figure-or-table-number |
| `[0137]` | `FIG. **3**` | figure-or-table-number |
| `[0149]` | `1` | boundary-left |
| `[0165]` | `0 <6:3>` | bit-slice |
| `[0165]` | `0 <4:2>` | bit-slice |
| `[0165]` | `0` | boundary-left |
| `[0165]` | `<4:2>` | bit-slice |
| `[0188]` | `.sub.j−1` | subscript-index |
| `[0188]` | `.sub.j−1` | subscript-index |
| `[0188]` | `FIG. **1**` | figure-or-table-number |
| `[0183]` | `Table 2` | figure-or-table-number |
| `[0183]` | `FIG. **60**` | figure-or-table-number |
| `[0183]` | `8` | boundary-left |
| `[0183]` | `(1-4-3)` | coordinate-triple |
| `[0183]` | `6` | boundary-left |
| `[0183]` | `(1-3-2)` | coordinate-triple |
| `[0140]` | `0` | boundary-left |
| `[0140]` | `1` | boundary-left |
| `[0188]` | `FIG. **28**` | figure-or-table-number |
| `[0217]` | `0` | boundary-left |
| `[0217]` | `1` | boundary-left |
| `[0217]` | `0` | boundary-left |
| `[0217]` | `0` | boundary-left |
| `[0217]` | `1` | boundary-left |
| `[0217]` | `1` | boundary-left |
| `[0217]` | `0` | boundary-left |
| `[0217]` | `1` | boundary-left |
| `[0218]` | `0` | boundary-left |
| `[0218]` | `1` | boundary-left |
| `[0189]` | `5` | boundary-right |
| `[0189]` | `4` | boundary-right |
| `[0189]` | `3` | boundary-right |
| `[0189]` | `2` | boundary-right |
| `[0231]` | `0` | boundary-left |
| `[0231]` | `1` | boundary-left |

</details>

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
| `addition-attachment` | `measure-only` | 0.7500 | - | `measured` |

### 13.2 갈린 항목

- `addition-attachment`
  - 정본에만: selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder | adding, by a half adder in a …
  - 정본에만: wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5 | a half adder configured to add an exponent bit of the activation value and an exponent bit of the we …
  - 정본에만: wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5 | a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight …
  - 비교본에만: selecting, by a fourth multiplexer in the column cell, an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder | selecting, by a first multip …
  - 비교본에만: wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5 | a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation …
  - 비교본에만: wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5 | a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation bet …

## 14. 도면

- `FIG-1` — “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-01.png` · 도면부호 100, 101, 102, 104, 106, 108, 110
- `FIG-2` — “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-02.png` · 도면부호 101, 220, 222
- `FIG-3` — “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-03.png` · 도면부호 220
- `FIG-9` — “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-09.png` · 도면부호 220, 830
- `FIG-28` — “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-28.png` · 도면부호 220, 830, 2860, 2862, 2864, 2866
- `FIG-29` — “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-29.png` · 도면부호 220
- `FIG-43` — “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-43.png` · 도면부호 4303
- `FIG-60` — “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-60.png` · 도면부호 
- **M122** (FIG-1) — The whole compute engine in one frame: an input buffer and a scale buffer feed a 32 by 32 digital compute in memory macro, a dequantization block turns the integer accumulations back into a wider floating point output, and a mode decoding unit sits to the side as the block that selects the arithmetic mode. · 도면부호 100, 101, 102, 104, 106, 108, 110
- **M123** (FIG-2) — The macro seen as a grid: thirty two rows of column cells receive one activation value each, thirty two columns of computing units receive one weight word each, and every column runs one dot product. · 도면부호 101, 220, 222
- **M124** (FIG-3) — One column cell opened up, split into a sign lane, an exponent lane and a mantissa lane, with the weight bits held in stacked double bitcells and the results handed to an exponent handling block and a mantissa handling block. · 도면부호 220
- **M125** (FIG-9) — The exponent path of the baseline mode: half adders sit under the weight bitcells and pass their sum and carry bits into a short chain of full adders, with the hand arithmetic written out beside the circuit. · 도면부호 220, 830
- **M126** (FIG-28) — The flexible version of the same exponent stage, where three multiplexers choose between zero and a real sum, carry or carry-in bit before the full adder, and a fourth multiplexer picks which of those signals leaves the stage as the product exponent bit. · 도면부호 220, 830, 2860, 2862, 2864, 2866
- **M127** (FIG-29) — The shared column cell drawn at full width: twelve weight bit columns against twelve activation bit rows, outlined into three groups so that the same silicon can hold three separate four-bit exponents. · 도면부호 220
- **M128** (FIG-43) — The double bitcell stack, where each memory cell carries two bitcells that share one bitline and are opened by two different write wordlines. · 도면부호 4303
- **M129** (FIG-60) — The mode table that the whole design is aimed at: eight rows pairing an activation format with a weight format, and showing which bit positions are forced to zero in each pairing. · 도면부호 

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
| **M110** | 기술적 함의 | active | - |
| **M111** | 기술적 함의 | active | - |
| **M112** | 기술적 함의 | active | - |
| **M113** | 기술적 함의 | active | - |
| **M114** | 기술적 함의 | active | - |
| **M115** | 기술적 함의 | active | - |
| **M116** | 기술적 함의 | active | - |
| **M117** | 기술적 함의 | active | - |
| **M118** | 포지셔닝 | active | - |
| **M119** | 포지셔닝 | active | - |
| **M120** | 포지셔닝 | active | - |
| **M121** | 포지셔닝 | active | - |
| **M122** | 도면 주석 | active | - |
| **M123** | 도면 주석 | active | - |
| **M124** | 도면 주석 | active | - |
| **M125** | 도면 주석 | active | - |
| **M126** | 도면 주석 | active | - |
| **M127** | 도면 주석 | active | - |
| **M128** | 도면 주석 | active | - |
| **M129** | 도면 주석 | active | - |

## 16. 절차 이력

| 항목 | 값 |
|---|---|
| 독립 실행 | read-a:canonical, read-b:convergence-peer |
| 정본 실행 | `read-a` |
| 정본 지정 규칙 | `declaration-order` · 내용맹 `True` |
| 산출 시각 | 2026-08-18T09:59:01Z |
| 엔진 커밋 | `f0b4ca15b2129a1fe191f53d2e834de7b55c3039` |

분해는 **두 독립 실행**이 돌았고, 접지 이후는 **정본 1개**만 돌았다(재정 P-4).
정본 지정은 선언 순서이며 **내용을 보지 않는다** — 수렴 통과는 두 독해가 동치라는
선언이므로 정본 선택에 판정자가 없고, 남는 요구는 재현성뿐이기 때문이다. 두 실행은
서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.
