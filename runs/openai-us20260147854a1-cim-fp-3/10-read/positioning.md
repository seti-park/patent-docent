# 포지셔닝 (D5 ⑤)

## M118

- 배경 문제: The background section describes accelerators that convert between a high precision software format and a fixed low precision datapath, where every conversion step costs scaling, rounding and saturation logic, and where a new low bit format forces a new pipeline or a dedicated core.
- 주장 효과: The specification asserts that a compute engine driven by a mode decoding unit executes vector matrix and matrix matrix operations across a range of compact numeric formats without requiring separate conversion pipelines or dedicated cores for each format.
- 차이: The stated difference is structural rather than a measured speed or power figure: the same half adder, full adder and multiplexer fabric inside the column cell is re-selected per arithmetic mode, and the supported exponent widths are enumerated as two, three, four and five bits.
- 인용: “Each conversion step requires additional scaling, rounding, and saturation logic, which adds area, power, and latency to already dense compute fabrics, and can introduce cumulative quantization errors that degrade numerical behavior over many layers.”
- 인용: “As new low-bit formats and variants are introduced to improve efficiency (such as different 8-bit or sub-8-bit floating-point encodings), fixed conversion pipelines and format-specific data paths become increasingly difficult to adapt, limiting the flexibility of the hardware to support evolving models and deployment scenarios.”
- 인용: “optimized hardware can execute vector-matrix and matrix-matrix operations more efficiently, across a range of compact numeric formats without requiring separate conversion pipelines or dedicated cores for each format”

## M119

- 배경 문제: A compute in memory array holds its weights in place, so changing the weight matrix normally competes with the multiply that is using it, and the array idles while the next matrix is loaded.
- 주장 효과: The specification asserts that a memory cell built from two bitcells supports a double buffer scheme in which the next matrix of weight values is loaded while the previous one is still in use, and that a write operation is therefore performed concurrently with the vector matrix multiplication in the same column cell.
- 차이: The stated difference is a second bitcell per memory cell that shares the bitline but is addressed by its own wordline, with a weight select signal deciding which bank is written and which bank is read; no throughput figure is asserted for the overlap.
- 인용: “the CIM macro **101** can support for a double-buffer scheme (e.g., each memory cell having double bitcells) allowing concurrent loading of the next matrix of weight values while the previous weight values are still in use for the VMM computation.”
- 인용: “Accordingly, the write operation can be performed concurrently with the VMM operation in the same column cell of the CIM macro.”

## M120

- 배경 문제: The disclosure's own first exponent scheme spends three half adders and three full adders per column cell because the activation and weight exponent bits are added in two stages.
- 주장 효과: The specification asserts that adding the exponent bits directly instead of in two stages reduces the same computation to two half adders and two full adders per column cell, and it states an array level saving for a thirty two element vector against a thirty two by thirty two weight matrix.
- 차이: The stated difference is one fewer half adder and one fewer full adder in every column cell, obtained by restructuring where the least significant and most significant exponent positions are handled rather than by changing the numeric format.
- 인용: “As discussed above with respect to FIG. **9**, three half adders (which are coupled to the memory cells) are used along with three full adders for exponent computation between Act 0 in FP8 (1-4-3) and Wdata 0 in FP6 (1-3-2). As shown in FIG. **14**, logic circuits for this exponent computation may be reduced to 2 half adders and 2 full adders, where exponent bits of the activation value and the weight value can be added directly rather than in a two-stage operation described in FIG. **9**.”
- 인용: “As such, to perform the VMM operation for the 1×32 vector of activation values and the 32×32 matrix of weight values, 64×64 number of half adders and full adders can be saved.”

## M121

- 배경 문제: Building one cell that serves several floating point formats means that, in any single mode, some bitcells and some adders are carrying values that the mode does not need.
- 주장 효과: The specification concedes that redundancy or waste exists, asserts that it is not critical because the bitcells and their appended logic are a small portion of the power, performance and area budget, and asserts that storing a zero weight is simple to implement and lets unused sections be power gated for leakage.
- 차이: The stated difference from a per format design is a trade rather than an elimination: area and stored zeros are spent to keep one layout, and the supported format list is widened instead of the datapath being duplicated.
- 인용: “There may be redundancy or waste when supporting flexible FP formats. For example, weight value of “0” is stored in the CIM macro **101** in bitcells, and flexible option are provided in computation methods and logic circuit designs.”
- 인용: “The advantages of storing the weight value “0” includes straightforward design, easy to implement, and power gating for unused sections to save leakage power.”
- 인용: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”

## 출원인 관심 신호

_등재된 신호가 없다._
