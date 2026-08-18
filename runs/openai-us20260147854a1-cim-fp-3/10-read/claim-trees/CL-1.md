# 청구항 트리 — `CL-1`

> A hardware accelerator comprising: a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values; and a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, the first floating point format and the second floating point format being flexible, wherein a column cell of the CIM macro is configured to output a primitive product between an activation value and a weight value and comprises: a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit; a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder; a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder; and a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder, wherein the first multiplexer, the second multiplexer and the third multiplexer perform respective selections based on control signals according to the arithmetic mode.

## 골격 (독립항 element)와 누적 층위 (종속항 부가 한정)

- `CL-1/e1` → **M1** — a compute-in-memory (CIM) macro configured to perform a vector matrix multiplication (VMM) operation between a vector of activation values and a matrix of weight values
- `CL-1/e2` → **M2** — a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values
  - `CL-1/e2/e1` → **M3** — the first floating point format and the second floating point format being flexible
- `CL-1/e3` → **M4** — wherein a column cell of the CIM macro is configured to output a primitive product between an activation value and a weight value and comprises:
  - (종속 `CL-2`) `CL-2/a1` → **M23** — wherein the column cell further comprises a fourth multiplexer configured to output an exponent bit of the primitive product by selecting an output from the full adder, the sum bit from the half adder or the carry-in bit from the prior stage full adder
  - (종속 `CL-3`) `CL-3/a1` → **M24** — wherein the column cell further comprises a plurality of memory cells configured to store the weight value
  - (종속 `CL-4`) `CL-4/a1` → **M25** — wherein one of the plurality of memory cells comprises a bitcell configured to store the exponent bit of the weight value and provide the exponent bit of the weight value to the half adder
  - (종속 `CL-5`) `CL-5/a1` → **M26** — one of the plurality of memory cells comprises a first bitcell and a second bitcell
  - (종속 `CL-5`) `CL-5/a2` → **M27** — the first bitcell is addressed by a first wordline and the second bitcell is addressed by a second wordline different from the first wordline
  - (종속 `CL-6`) `CL-6/a1` → **M28** — wherein the first bitcell and the second bitcell share a bitline and are addressed by different wordlines
  - (종속 `CL-7`) `CL-7/a1` → **M29** — wherein the first bitcell is configured to store a first bit of the weight value and the second bitcell is configured to store a second bit of another weight value that is different from the weight value
  - (종속 `CL-8`) `CL-8/a1` → **M30** — wherein the first bitcell is configured to provide the first bit of the weight value to the half adder, the first bit being the exponent bit of the weight value
  - (종속 `CL-9`) `CL-9/a1` → **M31** — wherein the second bitcell is configured to concurrently update the second bit when the first bitcell is providing the first bit to the half adder
  - `CL-1/e3/e1` → **M5** — a half adder configured to add an exponent bit of the activation value and an exponent bit of the weight value and output a carry-out bit and a sum bit
    - (종속 `CL-10`) `CL-10/a1` → **M32** — wherein a number of exponent bits in the activation value comprises at least one of 2, 3, 4 and 5
    - (종속 `CL-11`) `CL-11/a1` → **M33** — wherein a number of exponent bits in the weight value comprises at least one of 2, 3, 4 and 5
  - `CL-1/e3/e2` → **M6** — a first multiplexer configured to select zero or a prior stage carry-out bit from a prior stage half adder and output a first selection to a full adder
  - `CL-1/e3/e3` → **M7** — a second multiplexer configured to select zero or the sum bit and output a second selection to the full adder
  - `CL-1/e3/e4` → **M8** — a third multiplexer configured to select zero or a carry-in bit from a prior stage full adder and output a third selection to the full adder
  - `CL-1/e3/e5` → **M9** — wherein the first multiplexer, the second multiplexer and the third multiplexer perform respective selections based on control signals according to the arithmetic mode

## 이 청구항을 인용하는 종속항

- `CL-2` — `single` (인용: CL-1)
- `CL-3` — `single` (인용: CL-1)
- `CL-10` — `single` (인용: CL-1)
- `CL-11` — `single` (인용: CL-1)
