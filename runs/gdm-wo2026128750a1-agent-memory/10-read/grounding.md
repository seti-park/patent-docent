# 3중 접지 (D5 ③)

접지 전량이 원칙이다(재정 R3). 예외는 아래 §2 에 전량 드러난다.

## 1. 접지 목록

### **M57** ← 구성요소 M1 (명세서 `found` · 도면 `found`)

- 명세서 `[0431]`: “At 2102, example method 2100 includes receiving, by a machine-learned agent system, a query associated with a user.”
- 명세서 `[0065]`: “Input interface(s) 102 can receive inputs (e.g., from a user). Query 104 can be based on data from input interfaces 102.”
- 도면 `FIG-1` (도면부호 100, 102, 104): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 도면 `FIG-21` (도면부호 2100, 2102): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M58** ← 구성요소 M2 (명세서 `found` · 도면 `found`)

- 명세서 `[0432]`: “At 2104, example method 2100 includes accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user.”
- 명세서 `[0066]`: “Machine-learned agent system 100 can issue a memory query 108 to interaction memory datastore 110.”
- 명세서 `[0067]`: “Machine-learned agent system 100 can obtain memory data 114 based on memory response 112”
- 도면 `FIG-1` (도면부호 100, 105, 106, 108, 110, 112, 114): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 도면 `FIG-21` (도면부호 2104): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M59** ← 구성요소 M3 (명세서 `found` · 도면 `found`)

- 명세서 `[0432]`: “In some implementations, the interaction memory datastore includes one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user.”
- 명세서 `[0066]`: “Interaction memory datastore 110 can contain stored contextual information catalogued and stored over prior interactions with the user.”
- 명세서 `[0053]`: “For instance, the machine-learned agent system can process the content of an interaction with the user and selectively generate memory objects that encapsulate salient features of the interaction.”
- 도면 `FIG-2` (도면부호 110, 202-1, 202-M, 204-1, 204-M, 206-1, 206-M): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M60** ← 구성요소 M4 (명세서 `found` · 도면 `found`)

- 명세서 `[0434]`: “At 2106, example method 2100 includes inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory”
- 명세서 `[0067]`: “Machine-learned agent system 100 can output input data structure 116 based on memory data 114.”
- 명세서 `[0105]`: “Input data structure 116 can be or include a data object configured for input to machine-learned model system(s) 118.”
- 도면 `FIG-1` (도면부호 100, 114, 116, 118): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 도면 `FIG-21` (도면부호 2106): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M61** ← 구성요소 M5 (명세서 `found` · 도면 `found`)

- 명세서 `[0435]`: “At 2108, example method 2100 includes generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output.”
- 명세서 `[0068]`: “Machine-learned model system 118 can process input data structure 116 to generate output data structure 120.”
- 도면 `FIG-1` (도면부호 116, 118, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 도면 `FIG-21` (도면부호 2108): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M62** ← 구성요소 M6 (명세서 `found` · 도면 `found`)

- 명세서 `[0436]`: “At 2110, example method 2100 includes outputting, by the machine-learned agent system, and based on the output, a response to the query.”
- 명세서 `[0069]`: “Machine-learned agent system 100 can output response 122 based on output data structure 120.”
- 명세서 `[0069]`: “Output interface(s) 124 can render, transmit, or execute data from response 122.”
- 도면 `FIG-1` (도면부호 100, 104, 120, 122, 124): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 도면 `FIG-21` (도면부호 2110): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M63** ← 구성요소 M7 (명세서 `found` · 도면 `found`)

- 명세서 `[0100]`: “Interaction memory datastore 110 can be multimodal.”
- 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M64** ← 구성요소 M8 (명세서 `found` · 도면 `found`)

- 명세서 `[0432]`: “the memory data can be based on a first memory object associated with a first data modality and a second memory object associated with a second data modality”
- 도면 `FIG-2` (도면부호 202-1, 202-M, 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M65** ← 구성요소 M9 (명세서 `found` · 도면 `found`)

- 명세서 `[0432]`: “For example, the first data modality can include audio data, and wherein the second data modality can include image data.”
- 명세서 `[0162]`: “interaction memory datastore 110 can store image data in association with audio data”
- 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M66** ← 구성요소 M10 (명세서 `found` · 도면 `found`)

- 명세서 `[0163]`: “interaction memory datastore 110 can store image data in association with text data”
- 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M67** ← 구성요소 M11 (명세서 `found` · 도면 `found`)

- 명세서 `[0164]`: “interaction memory datastore 110 can store audio data in association with text data”
- 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M68** ← 구성요소 M12 (명세서 `found` · 도면 `found`)

- 명세서 `[0437]`: “retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query”
- 도면 `FIG-3` (도면부호 106, 110): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M69** ← 구성요소 M13 (명세서 `found` · 도면 `found`)

- 명세서 `[0438]`: “processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values”
- 도면 `FIG-8` (도면부호 802, 118): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M70** ← 구성요소 M14 (명세서 `found` · 도면 `found`)

- 명세서 `[0439]`: “The values can indicate that at least a portion of the input is to be stored.”
- 도면 `FIG-8` (도면부호 804, 118): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M71** ← 구성요소 M15 (명세서 `found` · 도면 `found`)

- 명세서 `[0439]`: “The machine-learned agent system (e.g., 100) can extract a portion of the input (e.g., using memory model 105)”
- 도면 `FIG-8` (도면부호 105, 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M72** ← 구성요소 M16 (명세서 `found` · 도면 `found`)

- 명세서 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
- 도면 `FIG-2` (도면부호 204-1, 202-1, 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M73** ← 구성요소 M17 (명세서 `found` · 도면 `found`)

- 명세서 `[0440]`: “storing, by the machine-learned agent system, metadata associated with the memory value in the memory object”
- 도면 `FIG-2` (도면부호 206-1, 204-1, 202-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M74** ← 구성요소 M18 (명세서 `found` · 도면 `found`)

- 명세서 `[0441]`: “the portion includes at least one of: text data, image data, or audio data”
- 도면 `FIG-2` (도면부호 110, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M75** ← 구성요소 M19 (명세서 `found` · 도면 `found`)

- 명세서 `[0442]`: “the portion corresponds to an explicit instruction to remember information”
- 도면 `FIG-4` (도면부호 402, 105): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M76** ← 구성요소 M20 (명세서 `found` · 도면 `found`)

- 명세서 `[0443]`: “receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information”
- 도면 `FIG-10` (도면부호 1002, 105): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M77** ← 구성요소 M21 (명세서 `found` · 도면 `found`)

- 명세서 `[0443]`: “Memory model 105 can then cause the identified memory objects to be deleted from interaction memory datastore 110.”
- 도면 `FIG-10` (도면부호 105, 110, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M78** ← 구성요소 M22 (명세서 `found` · 도면 `found`)

- 명세서 `[0444]`: “receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval”
- 도면 `FIG-10` (도면부호 1002, 110): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M79** ← 구성요소 M23 (명세서 `found` · 도면 `found`)

- 명세서 `[0444]`: “queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval”
- 명세서 `[0444]`: “The deletion can be performed immediately or scheduled for a later time.”
- 도면 `FIG-10` (도면부호 110, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M80** ← 구성요소 M24 (명세서 `found` · 도면 `found`)

- 명세서 `[0445]`: “the memory data includes an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects”
- 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M81** ← 구성요소 M25 (명세서 `found` · 도면 `found`)

- 명세서 `[0446]`: “filtering the plurality of memory objects to obtain the one or more memory values”
- 도면 `FIG-3` (도면부호 108, 110): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M82** ← 구성요소 M26 (명세서 `found` · 도면 `found`)

- 명세서 `[0446]`: “The filtering process can involve computing one or more relevance measures (e.g., similarity scores, distance metrics, or probabilities) for each memory object”
- 도면 `FIG-3` (도면부호 108, 106): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M83** ← 구성요소 M27 (명세서 `found` · 도면 `found`)

- 명세서 `[0446]`: “The filtering process can then return a subset of the memory objects”
- 도면 `FIG-3` (도면부호 302, 304, 306): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M84** ← 구성요소 M28 (명세서 `found` · 도면 `found`)

- 명세서 `[0447]`: “the one or more relevance measures include a respective score generated based on distance between a query embedding and a respective memory value embedding”
- 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M85** ← 구성요소 M29 (명세서 `found` · 도면 `found`)

- 명세서 `[0447]`: “a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model”
- 도면 `FIG-13` (도면부호 4, 6): “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”

### **M86** ← 구성요소 M30 (명세서 `found` · 도면 `found`)

- 명세서 `[0448]`: “the one or more memory values each include a respective string”
- 도면 `FIG-2` (도면부호 204-1, 204-M): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M87** ← 구성요소 M31 (명세서 `found` · 도면 `found`)

- 명세서 `[0448]`: “the memory data includes a string including the one or more respective strings from the one or more memory values”
- 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M88** ← 구성요소 M32 (명세서 `found` · 도면 `found`)

- 명세서 `[0449]`: “inputting at least a portion of the output to the machine-learned sequence processing model”
- 도면 `FIG-1` (도면부호 120, 118): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M89** ← 구성요소 M33 (명세서 `found` · 도면 `found`)

- 명세서 `[0449]`: “generating, based on processing the output using the machine-learned sequence processing model, the response to the query”
- 도면 `FIG-1` (도면부호 122, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M90** ← 구성요소 M34 (명세서 `found` · 도면 `found`)

- 명세서 `[0449]`: “the output includes a plurality of predictions for analytical content that includes an analysis of the query with respect to the memory data”
- 도면 `FIG-1` (도면부호 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M91** ← 구성요소 M35 (명세서 `found` · 도면 `found`)

- 명세서 `[0450]`: “the plurality of predictions for analytical content are not exposed on a user interface associated with the query”
- 명세서 `[0117]`: “The raw outputs may not be surfaced to the user.”
- 도면 `FIG-1` (도면부호 124, 122): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M92** ← 구성요소 M36 (명세서 `found` · 도면 `found`)

- 명세서 `[0020]`: “In some implementations, the example method includes consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset.”
- 명세서 `[0299]`: “Memory model 105 may consolidate related memory objects, merging redundant or overlapping information to reduce storage overhead.”
- 도면 `FIG-10` (도면부호 704, 110, 105): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 통합(consolidation)은 FIG-10의 메모리 유지보수 사이클(704) 안에서 memory model 105 가 interaction memory datastore 110 에 대해 수행하는 동작으로 표현된다. '통합' 자체에 고유 도면부호는 없어 상위 요소 부호만 등재했다.

### **M93** ← 구성요소 M37 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
- 도면 `FIG-5` (도면부호 500): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M94** ← 구성요소 M38 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the example method includes creating a current memory object.”
- 명세서 `[0246]`: “Memory model 105 can interact with machine-learned model system(s) 118 to generate values for a new memory object 402 based on input 400.”
- 도면 `FIG-4` (도면부호 402, 400, 105): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M95** ← 구성요소 M39 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the current memory object includes the timestamp.”
- 명세서 `[0256]`: “Memory model 105 can cause memory object 402 to store time data associated with the memory.”
- 도면 `FIG-4` (도면부호 402): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 타임스탬프는 메모리 객체 402 내부의 필드(created/lastUpdated)로 표현될 뿐 고유 도면부호를 갖지 않아, 이를 포함하는 객체 부호 402 만 등재했다.

### **M96** ← 구성요소 M40 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the current memory object includes a current memory value based on the input data.”
- 명세서 `[0246]`: “For example, memory model 105 can use machine-learned model system(s) 118 to predict a memory value “prefers vegetarian” based on the input.”
- 도면 `FIG-4` (도면부호 402, 400): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 메모리 값(memory value)은 FIG-4 에서 객체 402 내부 값으로 표현되며 별도 도면부호가 없다. FIG-2 의 204-1…204-M 이 일반형 부호이나, 본 종속항의 '현재 메모리 값'에 직접 조응하는 것은 FIG-4 의 402 이므로 402·400 만 등재했다.

### **M97** ← 구성요소 M41 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the example method includes matching the current memory object to a prior memory object.”
- 명세서 `[0089]`: “Memory model 105 can query interaction memory datastore 110 to retrieve relevant entries for new information and update the relevant entries based on the new information.”
- 도면 `FIG-5` (도면부호 500, 402): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 매칭 동작 자체에는 도면부호가 없다. FIG-5 에서 신규 입력 500 이 선행 메모리 객체 402 에 대응되는 관계로 표현되므로 두 부호를 등재했다.

### **M98** ← 구성요소 M42 (명세서 `found` · 도면 `found`)

- 명세서 `[0021]`: “In some implementations, the example method includes replacing, in the interaction memory datastore, the prior memory object with the current memory object.”
- 명세서 `[0263]`: “The updated memory object 502 can be stored in interaction memory datastore 110.”
- 도면 `FIG-5` (도면부호 502, 402, 110): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M99** ← 구성요소 M43 (명세서 `found` · 도면 `found`)

- 명세서 `[0022]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
- 명세서 `[0453]`: “For example, at 2108, the machine-learned agent system (e.g., 100) receives input data (e.g., 500 in Figure 5) associated with a timestamp.”
- 도면 `FIG-5` (도면부호 500): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M100** ← 구성요소 M44 (명세서 `found` · 도면 `found`)

- 명세서 `[0022]`: “In some implementations, the example method includes matching at least a portion of the input data to a prior memory object.”
- 명세서 `[0453]`: “The system then matches at least a portion of the input data to a prior memory object (e.g., 402 in Figure 4).”
- 도면 `FIG-5` (도면부호 500, 402): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 매칭 동작 자체에는 도면부호가 없어, 입력 500 과 선행 메모리 객체 402 의 부호를 등재했다.

### **M101** ← 구성요소 M45 (명세서 `found` · 도면 `found`)

- 명세서 `[0022]`: “In some implementations, the example method includes updating, in the interaction memory datastore, the prior memory object based on the portion of the input data.”
- 명세서 `[0453]`: “Based on this match, the system updates (e.g., as in Figure 5), in the interaction memory datastore (e.g., 110), the prior memory object (e.g., 402) based on the portion of the input data (e.g., 500).”
- 도면 `FIG-5` (도면부호 502, 402, 110): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M102** ← 구성요소 M46 (명세서 `found` · 도면 `found`)

- 명세서 `[0023]`: “In some implementations of the example method, the response includes instructions configured to control an application programming interface to cause a computing system to perform an action.”
- 명세서 `[0120]`: “For instance, response 122 can include an application programming interface call generated based on output data structure 120.”
- 도면 `FIG-1` (도면부호 122, 124, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M103** ← 구성요소 M47 (명세서 `found` · 도면 `found`)

- 명세서 `[0024]`: “the query indicates a configuration parameter that controls an operation of the computing system”
- 명세서 `[0455]`: “For example, the query (e.g , 104) might indicate a configuration parameter that controls an operation of the computing system.”
- 도면 `FIG-1` (도면부호 104, 102): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 구성 파라미터 자체에는 도면부호가 없다. 그것을 지시하는 질의 104(및 입력 인터페이스 102)의 부호를 등재했다.

### **M104** ← 구성요소 M48 (명세서 `found` · 도면 `found`)

- 명세서 `[0024]`: “the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter”
- 명세서 `[0455]`: “The system then generates an output (e.g., 120) that includes instructions (e.g., in response 122) configured to control an API call (e.g., via output interface 124) to cause the computing system to assign a value for the configuration parameter.”
- 도면 `FIG-1` (도면부호 120, 122, 124): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”

### **M105** ← 구성요소 M49 (명세서 `found` · 도면 `not-depicted`)

- 명세서 `[0456]`: “In some implementations of example method 2100, the configuration parameter is associated with at least one of: data access by the computing system, data retention by the computing system, or data communication by the computing system.”
- 탐색 기록: FIG-1(100·104·110·118·122·124)과 FIG-18~FIG-21 캡션 및 부호를 확인했으나, 구성 파라미터의 연관 대상(데이터 접근·보유·통신)을 표시한 도면부호는 없다. 명세서 [0025]·[0132]~[0135]·[0456] 본문에만 서술된다.

### **M106** ← 구성요소 M50 (명세서 `found` · 도면 `not-depicted`)

- 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data access by the computing system.”
- 명세서 `[0456]`: “For example, the configuration parameter (e.g., a setting within an analytics system for a web-based resource) might relate to data access permissions.”
- 탐색 기록: FIG-1 및 FIG-18~FIG-21 의 부호를 확인했으나 '데이터 접근' 구성 파라미터를 지시하는 도면부호는 존재하지 않는다.

### **M107** ← 구성요소 M51 (명세서 `found` · 도면 `not-depicted`)

- 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data retention by the computing system.”
- 명세서 `[0295]`: “The system may provide users with configurable parameters to control the time-based forgetting mechanism, allowing them to customize the system's memory retention policies.”
- 탐색 기록: FIG-1·FIG-10(704·1002·904·804) 등 유지보수 사이클 도면을 확인했으나 '데이터 보유' 구성 파라미터에 부여된 도면부호는 없다.

### **M108** ← 구성요소 M52 (명세서 `found` · 도면 `not-depicted`)

- 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data communication by the computing system.”
- 탐색 기록: FIG-1(124)·FIG-18(49) 등 통신 관련 부호를 확인했으나, 이들은 인터페이스·네트워크 자체의 부호이며 '데이터 통신' 구성 파라미터에 조응하는 도면부호는 없다.

### **M109** ← 구성요소 M53 (명세서 `found` · 도면 `found`)

- 명세서 `[0026]`: “In an aspect, the present disclosure provides an example one or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
- 명세서 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
- 도면 `FIG-18` (도면부호 52, 54, 62, 64): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”

### **M110** ← 구성요소 M54 (명세서 `found` · 도면 `found`)

- 명세서 `[0027]`: “In some implementations, the example computing system includes one or more processors.”
- 명세서 `[0415]`: “Computing device 50 can include one or more processors 51 and a memory 52.”
- 도면 `FIG-18` (도면부호 51, 61): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”

### **M111** ← 구성요소 M55 (명세서 `found` · 도면 `found`)

- 명세서 `[0027]`: “In some implementations, the example computing system includes one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising any implementation of the example method.”
- 명세서 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
- 도면 `FIG-18` (도면부호 52, 54, 62, 64): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”

### **M112** ← 구성요소 M56 (명세서 `found` · 도면 `not-depicted`)

- 명세서 `[0028]`: “In an aspect, the present disclosure provides an computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
- 탐색 기록: FIG-18~FIG-20 의 컴퓨팅 장치 부호(50·51·52·53·54·60~65·98·99)와 전 도면 캡션을 확인했으나, '컴퓨터 프로그램 제품'이라는 청구 범주에 조응하는 도면부호는 없다. 해당 aspect 는 [0028] 본문에만 기재된다.

## 2. 접지 예외

- **M105** (구성요소 M49) — 명세서 `found` · 도면 `not-depicted`: FIG-1(100·104·110·118·122·124)과 FIG-18~FIG-21 캡션 및 부호를 확인했으나, 구성 파라미터의 연관 대상(데이터 접근·보유·통신)을 표시한 도면부호는 없다. 명세서 [0025]·[0132]~[0135]·[0456] 본문에만 서술된다.
- **M106** (구성요소 M50) — 명세서 `found` · 도면 `not-depicted`: FIG-1 및 FIG-18~FIG-21 의 부호를 확인했으나 '데이터 접근' 구성 파라미터를 지시하는 도면부호는 존재하지 않는다.
- **M107** (구성요소 M51) — 명세서 `found` · 도면 `not-depicted`: FIG-1·FIG-10(704·1002·904·804) 등 유지보수 사이클 도면을 확인했으나 '데이터 보유' 구성 파라미터에 부여된 도면부호는 없다.
- **M108** (구성요소 M52) — 명세서 `found` · 도면 `not-depicted`: FIG-1(124)·FIG-18(49) 등 통신 관련 부호를 확인했으나, 이들은 인터페이스·네트워크 자체의 부호이며 '데이터 통신' 구성 파라미터에 조응하는 도면부호는 없다.
- **M112** (구성요소 M56) — 명세서 `found` · 도면 `not-depicted`: FIG-18~FIG-20 의 컴퓨팅 장치 부호(50·51·52·53·54·60~65·98·99)와 전 도면 캡션을 확인했으나, '컴퓨터 프로그램 제품'이라는 청구 범주에 조응하는 도면부호는 없다. 해당 aspect 는 [0028] 본문에만 기재된다.
