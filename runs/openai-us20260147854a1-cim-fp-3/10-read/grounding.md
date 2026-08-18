# 3중 접지 (D5 ③)

접지 전량이 원칙이다(재정 R3). 예외는 아래 §2 에 전량 드러난다.

## 1. 접지 목록

### **M44** ← 구성요소 M1 (명세서 `found` · 도면 `found`)

- 명세서 `[0128]`: “For example, CIM macro **101** can support a Vector Matrix Multiplication (VMM) operation between a vector of activation values and a matrix of weight values.”
- 명세서 `[0136]`: “Each column of computing unit **222** in the CIM macro **101** drives a dot product operation during an VMM operation.”
- 도면 `FIG-2` (도면부호 101, 222, 220): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M45** ← 구성요소 M2 (명세서 `found` · 도면 `found`)

- 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
- 명세서 `[0063]`: “A mode decoding unit can supply an arithmetic mode that may reflect the floating-point formats chosen for activations and weights, allowing the accelerator to support multiple “flexible” low-precision formats without redesigning the datapath.”
- 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M46** ← 구성요소 M3 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- 명세서 `[0188]`: “FIG. **28** illustrates an exemplary design of the column cell **220** for handling exponents of the flexible FP data.”
- 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FP 포맷의 유연성 자체를 그리는 도면은 회로도가 아니라 Table 2(FIG. **60**) 이다 — [0057] 캡션과 [0183] 의 Table 2 지시를 대조해 FIG-60 을 도면 자리로 잡았고, 회로 쪽 조응은 FIG. **28**(flexible FP data) 으로 보완했다.

### **M47** ← 구성요소 M4 (명세서 `found` · 도면 `found`)

- 명세서 `[0137]`: “FIG. **3** illustrates a block diagram of an exemplary column cell **220**configured to produce a primitive product between an activation value and a weight value.”
- 명세서 `[0149]`: “Step S1: multiplying, by each column cell **220** of the CIM macro **101**, a corresponding activation value a.sub.i and a corresponding weight value w.sub.ik to produce an element-wise primitive product P.sub.ik=a.sub.i×w.sub.ik, with specific handling method for the signs, exponents and mantissas of the activation value a.sub.i and the weight value w.sub.ik.”
- 도면 `FIG-3` (도면부호 220, 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-2` (도면부호 220, 222): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”

### **M48** ← 구성요소 M5 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M49** ← 구성요소 M6 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 도면 `FIG-28` (도면부호 2862, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M50** ← 구성요소 M7 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 도면 `FIG-28` (도면부호 2860, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M51** ← 구성요소 M8 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M52** ← 구성요소 M9 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M53** ← 구성요소 M10 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M54** ← 구성요소 M11 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2862): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M55** ← 구성요소 M12 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2860): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M56** ← 구성요소 M13 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M57** ← 구성요소 M14 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “The resulting exponent bits of the primitive product include the sum bit S.sub.LSB from the half adder for the LSBs of the exponents of the activation value and the weight value, the exponent bits E.sub.j output from the fourth multiplexers **2866**, and the carry-in bit CIN.sub.MSB from the last stage full adder for the MSB of the exponent of the activation value and/or the MSB of the exponent of the weight value.”
- 명세서 `[0166]`: “The full adders can be connected in series, where each full adder can output an exponent bit of the primitive product and a carry-in bit for the next stage full adder.”
- 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M58** ← 구성요소 M15 (명세서 `found` · 도면 `found`)

- 명세서 `[0017]`: “For example, in the disclosed technology a system may be provided that performs vector-matrix multiplication using a compute device that generates portions of a floating-point product directly within memory structures.”
- 명세서 `[0072]`: “At the system level, the disclosed technology may be implemented in a compute device that can house the exponent-processing hardware described above, while a mode device provides the control mode based on the selected floating-point formats for activations and weights.”
- 도면 `FIG-1` (도면부호 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-2` (도면부호 101, 222): “FIG. **2** illustrates a representation of a block diagram of an example compute-in memory (CIM) macro, in accordance with some aspects of the present disclosure.”

### **M59** ← 구성요소 M16 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To compute the exponent of the primitive product, the exponent bit of the weight value and a corresponding exponent bit of the activation value can be provided to a corresponding half adder. The half adder can add the corresponding exponent bits of the activation value and the weight value to produce one sum bit S.sub.j and one carry-out bit C.sub.j.”
- 명세서 `[0165]`: “First, half adders (labeled as HA) can be used to add the exponent bits of the activation value Act 0 <6:3> to corresponding exponent bits of the weight value Wdata 0 <4:2> (simplified as W0 <4:2>). Each half adder can output a sum bit and a carry-out bit.”
- 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-9` (도면부호 830): “FIG. **9** illustrates a scheme for handling exponent bits in a column cell in the CIM macro, in accordance with some aspects of the present disclosure.”

### **M60** ← 구성요소 M17 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A second multiplexer **2862** selects zero or a prior stage carry-out bit C.sub.j−1 from a prior stage half adder and output a second selection to the full adder.”
- 도면 `FIG-28` (도면부호 2862, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M61** ← 구성요소 M18 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A first multiplexer **2860** selects zero or the sum bit S.sub.j produced by the half adder and output a first selection to a corresponding full adder.”
- 도면 `FIG-28` (도면부호 2860, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FIG. **28**([0188]) 의 멀티플렉서 번호 부여가 청구항 순서와 뒤바뀌어 있어, 기능 조응(무엇을 선택하는가)을 기준으로 문단을 붙였다 — 청구항의 first multiplexer(prior stage carry-out 선택) = 명세서 second multiplexer **2862**, 청구항의 second multiplexer(sum bit 선택) = 명세서 first multiplexer **2860** 이다. third multiplexer **2864** 는 양쪽이 일치한다.

### **M62** ← 구성요소 M19 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “A third multiplexer **2864** selects zero or a carry-in bit CIN.sub.j−1 from a prior stage full adder and output a third selection to the full adder.”
- 도면 `FIG-28` (도면부호 2864, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”

### **M63** ← 구성요소 M20 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 명세서 `[0063]`: “Within each column cell, a half adder may add selected exponent bits from the activation and weight, and a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2860, 2862, 2864, 2866): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M64** ← 구성요소 M21 (명세서 `found` · 도면 `found`)

- 명세서 `[0146]`: “In some embodiments, the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
- 명세서 `[0072]`: “This split can allow the compute device to focus on dense, fast arithmetic and the mode device to handle configuration and format-aware control.”
- 도면 `FIG-1` (도면부호 110): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator, in accordance with some aspects of the present disclosure.”

### **M65** ← 구성요소 M22 (명세서 `found` · 도면 `found`)

- 명세서 `[0186]`: “The compute engine **100** can support various FP formats (e.g., FP8, FP6, FP4), beyond those listed in Tables 1 and 2. For example, FP8 format includes FP8 (1-5-2), FP8 (1-4-3), FP8(1-3-4); FP6 format includes FP6 (1-3-2), FP6 (1-2-3); and FP4 format includes FP4 (1-2-1), FP (1-1-2). The activation values and weight values can be represented by any of these FP formats.”
- 명세서 `[0183]`: “Table 2 (in FIG. **60**) lists exemplary representations for the lower FP formats based on FP8 (1-4-3) for activation values and FP6 (1-3-2) for weight values during the VMM operation in the CIM macro **101**.”
- 도면 `FIG-60` (도면부호 ): “FIG. **60** illustrates a table describing schemes for handling weight values and activation values in various FP formats, in accordance with some aspects of the present disclosure.”
- 도면 `FIG-28` (도면부호 220, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data, in accordance with some aspects of the present disclosure.”
- 탐색 기록: FP 포맷의 유연성 자체를 그리는 도면은 회로도가 아니라 Table 2(FIG. **60**) 이다 — [0057] 캡션과 [0183] 의 Table 2 지시를 대조해 FIG-60 을 도면 자리로 잡았고, 회로 쪽 조응은 FIG. **28**(flexible FP data) 으로 보완했다.

### **M66** ← 구성요소 M23 (명세서 `found` · 도면 `found`)

- 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product: the output of the full adder, the sum output of the half adder, or a carry-in from an upstream stage.”
- 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
- 도면 `FIG-28` (도면부호 2866, 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M67** ← 구성요소 M24 (명세서 `found` · 도면 `found`)

- 명세서 `[0140]`: “a column cell **340**, e.g., in Row 0 and Col 0 of the CIM macro **101**, includes a plurality of memory cells, each memory cell having two bitcells (BC0 and BC1) to allow performing a write operation and a tensor (e.g., VMM) operation in one memory cell simultaneously.”
- 명세서 `[0140]`: “Each memory cell stores one bit of the weight value.”
- 도면 `FIG-3` (도면부호 340): “FIG. **3** illustrates an exemplary column cell in the CIM macro”

### **M68** ← 구성요소 M25 (명세서 `found` · 도면 `found`)

- 명세서 `[0065]`: “Further, one of these memory cells may serve as a bitcell dedicated to holding the exponent bit of the weight value and feeding this bit directly to the half adder.”
- 명세서 `[0188]`: “In FIG. **28**, each bitcell stores a corresponding exponent bit of the weight value.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M69** ← 구성요소 M26 (명세서 `found` · 도면 `found`)

- 명세서 `[0066]`: “a memory cell can be realized as a pair of bitcells”
- 명세서 `[0217]`: “each memory cell **4303** includes two bitcells BC0 and BC1”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M70** ← 구성요소 M27 (명세서 `found` · 도면 `found`)

- 명세서 `[0066]`: “where each bitcell may be addressed by its own wordline, enabling independent selection of two stored bits.”
- 명세서 `[0217]`: “where bitcell BC0 can be addressed by wordline wwl0 and bitcell BC1 can be address by wordline wwl1.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M71** ← 구성요소 M28 (명세서 `found` · 도면 `found`)

- 명세서 `[0066]`: “Further, paired bitcells may share a common bitline while still being controlled by different wordlines.”
- 명세서 `[0217]`: “The two bitcells BC0 and BC1 in each memory cell **4303** can share one bitline BL for writing or scanning the bits of weight values.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M72** ← 구성요소 M29 (명세서 `found` · 도면 `found`)

- 명세서 `[0067]`: “a first bitcell may hold a first bit of one weight value, and a second bitcell may hold a second bit of a different weight value.”
- 명세서 `[0218]`: “bitcell BC0 can store a first bit of a first weight value and bitcell BC1 can store a second bit of a second weight value that is different from the first weight value.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M73** ← 구성요소 M30 (명세서 `found` · 도면 `found`)

- 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
- 명세서 `[0089]`: “one exponent bit may be stored in a bitcell and delivered to the first half adder, second half adder, or a full adder depending on its exponent position.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M74** ← 구성요소 M31 (명세서 `found` · 도면 `found`)

- 명세서 `[0067]`: “Further, while the first bitcell is driving the exponent bit into the half adder, the second bitcell can be updated with a new bit of another weight value.”
- 명세서 `[0087]`: “while one bitcell is feeding its exponent bit into the adder chain, the further bitcell may be updated with a new exponent bit of a different weight.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M75** ← 구성요소 M32 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M76** ← 구성요소 M33 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M77** ← 구성요소 M34 (명세서 `found` · 도면 `found`)

- 명세서 `[0188]`: “To perform respective selections, the first multiplexer **2860**, the second multiplexer **2862**, the third multiplexer **2864** and the fourth multiplexer **2866** can be controlled by one or more control signals from the mode decoding unit **110** (in FIG. **1**) according to a corresponding arithmetic mode and associated FP formats of the activation values and the weight values.”
- 명세서 `[0063]`: “a set of multiplexers can steer carry bits and sum bits into a full adder based on mode-dependent control signals.”
- 도면 `FIG-28` (도면부호 2860, 2862, 2864, 110, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M78** ← 구성요소 M35 (명세서 `found` · 도면 `found`)

- 명세서 `[0095]`: “a mode decoding unit may be included to set an arithmetic mode for the CIM macro based on floating-point formats of the activation and weight.”
- 명세서 `[0146]`: “the compute engine **100** includes a mode decoding unit **110** (also referred to as a mode device) to provide a mode of operation to the CIM macro **101** for the tensor operation between the streaming operand and the stationary operand.”
- 도면 `FIG-1` (도면부호 110, 100, 101): “FIG. **1** illustrates a block diagram of an exemplary hardware accelerator”

### **M79** ← 구성요소 M36 (명세서 `found` · 도면 `found`)

- 명세서 `[0070]`: “the method may describe using a fourth multiplexer to choose between different exponent results produced inside the column cell. For example, the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage”
- 명세서 `[0188]`: “The exponent handling block **830** can also include a fourth multiplexer **2866**, which can be used to select the accumulation output Ex.sub.j from the full adder of the current stage, the first selection from the first multiplexer **2860** and the third selection from the third multiplexer **2864**to produce the carry-in bit CIN.sub.j for the next stage full adder and the exponent bit E.sub.j of the primitive product.”
- 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M80** ← 구성요소 M37 (명세서 `found` · 도면 `found`)

- 명세서 `[0070]`: “using a fourth multiplexer to choose between different exponent results produced inside the column cell. For example, the hardware may choose between the full-adder output, the half-adder sum, or a carry-in from a previous stage, and present that as the exponent bit of the primitive product.”
- 명세서 `[0064]`: “the column cell may include an additional multiplexer that can choose which signal represents the exponent bit of the primitive product”
- 도면 `FIG-28` (도면부호 2866, 830): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M81** ← 구성요소 M38 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “Methods disclosed herein may also include sourcing the exponent bit of the weight value directly from a dedicated bitcell inside the column, which can feed that bit to the half adder.”
- 명세서 `[0067]`: “The first bitcell can provide its stored bit as the exponent bit of the weight to the half adder.”
- 도면 `FIG-28` (도면부호 830, 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M82** ← 구성요소 M39 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “At the same time that the first bitcell is supplying a weight exponent bit to the half adder, the method may allow writing a new exponent bit for a different weight into a second bitcell.”
- 명세서 `[0087]`: “while one bitcell is feeding its exponent bit into the adder chain, the further bitcell may be updated with a new exponent bit of a different weight.”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M83** ← 구성요소 M40 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “For example, a second exponent bit may be written through a bitline shared with the first bitcell, simplifying the array wiring.”
- 명세서 `[0231]`: “a weight value to be written/updated (e.g., wgt_data) can be provided to a set of bit lines BL shared by the first set of bitcells BC0 and the second set of bitcells BC1”
- 도면 `FIG-43` (도면부호 4303): “FIG. **43** illustrates an exemplary double-bitcell design”

### **M84** ← 구성요소 M41 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “disclosed accelerator designs may support activation values with different counts of exponent bits, such as 2, 3, 4, or 5, by sizing and controlling the exponent logic accordingly.”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M85** ← 구성요소 M42 (명세서 `found` · 도면 `found`)

- 명세서 `[0068]`: “Similarly, the design may support weight values with multiple possible exponent widths, including 2, 3, 4, or 5 bits.”
- 명세서 `[0189]`: “Similarly, a shared column cell can be implemented to support activation values and weight values having exponents with 5b, 4b, 3b or 2b, where the common cell **220** can include 60 columns and 60 rows, where number 60 is the least common multiple of number 5, 4, 3, and 2.”
- 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

### **M86** ← 구성요소 M43 (명세서 `found` · 도면 `found`)

- 명세서 `[0071]`: “The method may also size the number of bitcells in the column based on the least common multiple of supported exponent bit widths for activations and weights”
- 명세서 `[0189]`: “the common cell **220** includes 12 columns and 12 rows, where number 12 is the least common multiple of number 4, 3, and 2. Each column has one memory cell, each memory cell having one bitcell.”
- 도면 `FIG-29` (도면부호 220): “FIGS. **28**-**29** illustrate exemplary column cells for handling exponent bits for various FP data”

## 2. 접지 예외

_예외 없음._

