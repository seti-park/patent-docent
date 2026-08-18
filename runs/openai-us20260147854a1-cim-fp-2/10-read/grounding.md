# 3중 접지 (D5 ③)

접지 전량이 원칙이다(재정 R3). 예외는 아래 §2 에 전량 드러난다.

## 1. 접지 목록

### **M44** ← 구성요소 M1 (명세서 `found` · 도면 `found`)

- 명세서 `[0128]`: “For example, CIM macro **101** can support a Vector Matrix Multiplication (VMM) operation between a vector of activation values and a matrix of weight values.”
- 도면 `FIG-2` (도면부호 101, 222, 220): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M45** ← 구성요소 M2 (명세서 `found` · 도면 `found`)

- 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
- 명세서 `[0063]`: “A mode decoding unit can supply an arithmetic mode that may reflect the floating-point formats chosen for activations and weights, allowing the accelerator to support multiple “flexible” low-precision formats without redesigning the datapath.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M46** ← 구성요소 M3 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”

### **M47** ← 구성요소 M4 (명세서 `found` · 도면 `found`)

- 명세서 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
- 명세서 `[0136]`: “In the kth column of computing unit **222**, a column cell **220** of ith row is configured to perform the multiplication operation between the activation value a.sub.i and the weight value w.sub.ik to output the primitive product P.sub.ik=a.sub.i×w.sub.ik.”
- 도면 `FIG-3` (도면부호 220): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M48** ← 구성요소 M5 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M49** ← 구성요소 M6 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M50** ← 구성요소 M7 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M51** ← 구성요소 M8 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M52** ← 구성요소 M9 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M53** ← 구성요소 M21 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M54** ← 구성요소 M22 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M55** ← 구성요소 M23 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M56** ← 구성요소 M24 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M57** ← 구성요소 M25 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
- 명세서 `[0166]`: “The full adders can be connected in series, where each full adder can output an exponent bit of the primitive product and a carry-in bit for the next stage full adder.”
- 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M58** ← 구성요소 M36 (명세서 `found` · 도면 `found`)

- 명세서 `[0017]`: “For example, in the disclosed technology a system may be provided that performs vector-matrix multiplication using a compute device that generates portions of a floating-point product directly within memory structures.”
- 명세서 `[0072]`: “At the system level, the disclosed technology may be implemented in a compute device that can house the exponent-processing hardware described above, while a mode device provides the control mode based on the selected floating-point formats for activations and weights.”
- 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M59** ← 구성요소 M37 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M60** ← 구성요소 M38 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M61** ← 구성요소 M39 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M62** ← 구성요소 M40 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M63** ← 구성요소 M41 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M64** ← 구성요소 M42 (명세서 `found` · 도면 `found`)

- 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
- 명세서 `[0017]`: “The mode device can determine how exponent behavior should be formed based on the floating-point formats chosen for the activations and weights, allowing the system to adapt to multiple low-precision numeric formats without redesigning the underlying arithmetic fabric.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M65** ← 구성요소 M43 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”

### **M66** ← 구성요소 M10 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
- 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product: the output of the full adder, the sum output of the half adder, or a carry-in from an upstream stage.”
- 도면 `FIG-28-29` (도면부호 2866, 2860, 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M67** ← 구성요소 M11 (명세서 `found` · 도면 `found`)

- 명세서 `[0161]`: “The column cell **220** includes memory cells for storing the bits of the weight value, one bit of the weight value corresponding to one memory cell.”
- 명세서 `[0140]`: “The number of memory cells in the column cell **340** is determined by the number of bits used by the weight value. Each memory cell stores one bit of the weight value.”
- 도면 `FIG-3` (도면부호 220, 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M68** ← 구성요소 M12 (명세서 `found` · 도면 `found`)

- 명세서 `[0185]`: “To compute the exponent of the primitive product, each memory cell stored a corresponding exponent bit of the weight value can be connected to a half adder (HA).”
- 명세서 `[0188]`: “each bitcell stores a corresponding exponent bit of the weight value”
- 명세서 `[0188]`: “the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder”
- 도면 `FIG-26` (도면부호 220): “FIGS. **26**, **27**A, **27**B, **27**C illustrate exemplary logic circuits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-28-29` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M69** ← 구성요소 M13 (명세서 `found` · 도면 `found`)

- 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1”
- 명세서 `[0215]`: “each memory cell in the CIM macro can include one, two or more bitcells”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”

### **M70** ← 구성요소 M14 (명세서 `found` · 도면 `found`)

- 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1, which can be accessed via separate wordlines wwl0 and wwl1.”
- 명세서 `[0217]`: “bitcell BC0 can be addressed by wordline wwl0 and bitcell BC1 can be address by wordline wwl1.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”

### **M71** ← 구성요소 M15 (명세서 `found` · 도면 `found`)

- 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
- 명세서 `[0066]`: “paired bitcells may share a common bitline while still being controlled by different wordlines.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”

### **M72** ← 구성요소 M16 (명세서 `found` · 도면 `found`)

- 명세서 `[0218]`: “bitcell BC0 can store a first bit of a first weight value and bitcell BC1 can store a second bit of a second weight value that is different from the first weight value.”
- 명세서 `[0218]`: “each memory cell **4303** can store two bits from two different weight values.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”

### **M73** ← 구성요소 M17 (명세서 `found` · 도면 `found`)

- 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
- 명세서 `[0185]`: “To compute the exponent of the primitive product, each memory cell stored a corresponding exponent bit of the weight value can be connected to a half adder (HA).”
- 도면 `FIG-7-8` (도면부호 220, 830): “FIGS. **7**-**8** illustrate an enlarged view of the column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M74** ← 구성요소 M18 (명세서 `found` · 도면 `found`)

- 명세서 `[0067]`: “while the first bitcell is driving the exponent bit into the half adder, the second bitcell can be updated with a new bit of another weight value.”
- 명세서 `[0218]`: “the first set of bitcells can perform a write operation and the second set of bitcells can perform a VMM operation.”
- 명세서 `[0228]`: “It is noted that write operation and VMM operation can be performed in parallel in two different bitcells.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-44` (도면부호 4400): “FIG. **44** illustrates a timing diagram of a CIM macro for a write operation, in accordance with some aspects of the present disclosure.”

### **M75** ← 구성요소 M19 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
- 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
- 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M76** ← 구성요소 M20 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
- 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M77** ← 구성요소 M26 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 명세서 `[0069]`: “the selection behavior of the multiplexers may be driven by control signals tied to an arithmetic mode.”
- 도면 `FIG-28-29` (도면부호 2860, 2862, 2864, 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M78** ← 구성요소 M27 (명세서 `found` · 도면 `found`)

- 명세서 `[0069]`: “In some implementations, an arithmetic mode may be determined from the floating-point formats used for the activation and the weight.”
- 명세서 `[0007]`: “The hardware accelerator can also have a mode decoding unit configured to provide an arithmetic mode of the VMM operation according to a first floating point format of the activation values and a second floating point format of the weight values, where the first floating point format and the second floating point format are flexible.”
- 명세서 `[0146]`: “the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101**”
- 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M79** ← 구성요소 M28 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
- 명세서 `[0070]`: “the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage, and present that as the exponent bit of the primitive product.”
- 도면 `FIG-28-29` (도면부호 2866, 2860, 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M80** ← 구성요소 M29 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The resulting exponent bits of the primitive product include the sum bit S.sub.LSB from the half adder for the LSBs of the exponents of the activation value and the weight value, the exponent bits E.sub.j output from the fourth multiplexers **2866**”
- 명세서 `[0070]`: “Further, the method may describe using a fourth multiplexer to choose between different exponent results produced inside the column cell.”
- 도면 `FIG-28-29` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M81** ← 구성요소 M30 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “Methods disclosed herein may also include sourcing the exponent bit of the weight value directly from a dedicated bitcell inside the column, which can feed that bit to the half adder.”
- 명세서 `[0188]`: “the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder”
- 도면 `FIG-7-8` (도면부호 220, 830): “FIGS. **7**-**8** illustrate an enlarged view of the column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-28-29` (도면부호 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M82** ← 구성요소 M31 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “At the same time that the first bitcell is supplying a weight exponent bit to the half adder, the method may allow writing a new exponent bit for a different weight into a second bitcell.”
- 명세서 `[0218]`: “the first set of bitcells can perform a write operation and the second set of bitcells can perform a VMM operation.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-44` (도면부호 4400): “FIG. **44** illustrates a timing diagram of a CIM macro for a write operation, in accordance with some aspects of the present disclosure.”

### **M83** ← 구성요소 M32 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “For example, a second exponent bit may be written through a bitline shared with the first bitcell, simplifying the array wiring.”
- 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design, in accordance with some aspects of the present disclosure.”

### **M84** ← 구성요소 M33 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b”
- 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M85** ← 구성요소 M34 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “the exponents of the activation values and weight values can have 5, 4, 3 or 2 bits”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b”
- 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M86** ← 구성요소 M35 (명세서 `found` · 도면 `found`)

- 명세서 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- 명세서 `[0192]`: “At step **3202**, a minimum number of exponent bits in each column cell is determined by finding the least common multiple among all the possible combination of exponent bits in the various FP formats supported by each column cell of the compute engine **100**.”
- 도면 `FIG-28-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-32-33` (도면부호 3200, 3202): “FIGS. **32**-**33** illustrate methods for utilizing resources of a hardware accelerator, in accordance with some aspects of the present disclosure.”

## 2. 접지 예외

_예외 없음._

