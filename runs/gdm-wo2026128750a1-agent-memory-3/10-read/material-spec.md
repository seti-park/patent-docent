# CP1 판독본 (KR 틀 · EN 값) — `gdm-wo2026128750a1-agent-memory-3` (판 1)

상태 `draft` · 스키마 `material-spec/v0` · reader `0.9.0`

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
- §8-b 요청은 `review_adjudicated[]` 로 **전건** 답한다 — 요청 target 집합 = 판정 target 집합
  (`freeze.approval-valid` · 재정 T59 ②). `defect` 가 있으면 결정은 `rejected` 다. `undecided` 채 승인은 허용된다(재정 T59 ④).
- **작업 레인은 봉투를 쓰지 않는다.** 봉투는 오케스트레이터가 Owner 응답 후 기록한다(SPEC §1.2 C3).
- 무응답은 무기한 대기다. 시간 초과 자동 진행 경로는 없다(재정 R8).

## 1. 특허

| 항목 | 값 |
|---|---|
| 번호 | WO2026-128750A1 |
| 제목 | DYNAMIC INTERACTION MEMORY DATASTORE FOR MACHINE-LEARNED AGENT SYSTEMS |
| 관할 · 공보 종별 | `WO` · `A1` |
| 출원인 (런 ID 유래 단수) | GDM HOLDING LLC |
| 출원인 목록 | GDM HOLDING LLC |
| 발명자 목록 | HASSABIS, Demis · THOTA, Chandrasekhar · CHI, Ed Huai-hsin · WAYNE, Gregory Duncan |
| 날짜 | 우선 2024-12-11 · 출원 2025-12-11 · 공개 2026-06-18 |
| 우선권 주장 1 | 63/730,845 · 2024-12-11 · `US` |
| 분류 IPC | G06F 16/41 |
| 분류 CPC | G06F 16/41 |
| 원천 | `00-source/patent.md` |
| 원천 다이제스트 | `sha256:64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e` |

**최우선일 대조** — `dates.priority` 2024-12-11 ↔ 우선권 목록 최소 2024-12-11 → 일치

이 대조는 `read.bibliography#bib.earliest-priority` 가 산식으로 이미 판정했다.
여기 다시 놓는 이유는 CP1 이 **기계가 무엇을 보증했는가**를 사람이 재확인하는
자리이기 때문이다(C18 최우선일의 정확성 요건 — 재정 P-2 ⓐ).

## 2. 청구항 골격 (D5 ① 전 분해 · ② 관계 트리)

### 독립항 `CL-1`

> A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user, wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user;

inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data;

generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output; and

outputting, by the machine-learned agent system, and based on the output, a response to the query.

- `CL-1/e1` → **M1** — receiving, by a machine-learned agent system, a query associated with a user
- `CL-1/e2` → **M2** — accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user
  - `CL-1/e2/e1` → **M3** — wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user
- `CL-1/e3` → **M4** — inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data
- `CL-1/e4` → **M5** — generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output
- `CL-1/e5` → **M6** — outputting, by the machine-learned agent system, and based on the output, a response to the query

### 종속항 `CL-2` — `single` (인용: CL-1)

> The method of claim 1 , wherein the interaction memory datastore comprises multimodal data, and wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality.

- `CL-2/a1` (부착: `CL-1/e2/e1`) → **M7** — wherein the interaction memory datastore comprises multimodal data
- `CL-2/a2` (부착: `CL-1/e2/e1`) → **M8** — wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality

### 종속항 `CL-3` — `single` (인용: CL-2)

> The method of claim 2, wherein:

the first data modality comprises audio data, and wherein the second data modality comprises image data;

the first data modality comprises text data, and wherein the second data modality comprises image data; or

the first data modality comprises text data, and wherein the second data modality comprises audio data.

- `CL-3/a1` (부착: `CL-1/e2/e1`) → **M9** — the first data modality comprises audio data, and wherein the second data modality comprises image data
- `CL-3/a2` (부착: `CL-1/e2/e1`) → **M10** — the first data modality comprises text data, and wherein the second data modality comprises image data
- `CL-3/a3` (부착: `CL-1/e2/e1`) → **M11** — the first data modality comprises text data, and wherein the second data modality comprises audio data

### 종속항 `CL-4` — `single` (인용: CL-1)

> The method of claim 1 , comprising:

retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query.

- `CL-4/a1` (부착: `CL-1/e2`) → **M12** — retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query

### 종속항 `CL-5` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4)

> The method of any of the preceding claims, comprising:

after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values; and 

based on the generated one or more values indicating that at least a portion of the input is to be stored:

extracting, by the machine-learned agent system, the portion; and

storing, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore.

- `CL-5/a1` (부착: `CL-1/e2/e1`) → **M13** — after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values
- `CL-5/a2` (부착: `CL-1/e2/e1`) → **M14** — based on the generated one or more values indicating that at least a portion of the input is to be stored
- `CL-5/a3` (부착: `CL-1/e2/e1`) → **M15** — extracting, by the machine-learned agent system, the portion
- `CL-5/a4` (부착: `CL-1/e2/e1`) → **M16** — storing, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore

### 종속항 `CL-6` — `single` (인용: CL-5)

> The method of claim 5, comprising:

storing, by the machine-learned agent system, metadata associated with the memory value in the memory object.

- `CL-6/a1` (부착: `CL-1/e2/e1`) → **M17** — storing, by the machine-learned agent system, metadata associated with the memory value in the memory object

### 종속항 `CL-7` — `single` (인용: CL-5)

> The method of claim 5, wherein the portion comprises at least one of: text data, image data, or audio data.

- `CL-7/a1` (부착: `CL-1/e2/e1`) → **M18** — wherein the portion comprises at least one of: text data, image data, or audio data

### 종속항 `CL-8` — `single` (인용: CL-5)

> The method of claim 5, wherein the portion corresponds to an explicit instruction to remember information.

- `CL-8/a1` (부착: `CL-1/e2/e1`) → **M19** — wherein the portion corresponds to an explicit instruction to remember information

### 종속항 `CL-9` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8)

> The method of any of the preceding claims, comprising:

receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information; and

deleting, by the machine-learned agent system, the specified information from the interaction memory datastore.

- `CL-9/a1` (부착: `CL-1/e2`) → **M20** — receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information
- `CL-9/a2` (부착: `CL-1/e2`) → **M21** — deleting, by the machine-learned agent system, the specified information from the interaction memory datastore

### 종속항 `CL-10` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9)

> The method of any of the preceding claims, comprising:

receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval; and

queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval.

- `CL-10/a1` (부착: `CL-1/e2`) → **M22** — receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval
- `CL-10/a2` (부착: `CL-1/e2`) → **M23** — queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval

### 종속항 `CL-11` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10)

> The method of any of the preceding claims, wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects.

- `CL-11/a1` (부착: `CL-1/e2`) → **M24** — wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects

### 종속항 `CL-12` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11)

> The method of any of the preceding claims, comprising:

filtering the plurality of memory objects to obtain the one or more memory values, wherein the filtering comprises: 

computing one or more relevance measures for the plurality of memory objects based on the query; and

returning a subset of the plurality of memory objects based on the relevance measure.

- `CL-12/a1` (부착: `CL-1/e2/e1`) → **M25** — filtering the plurality of memory objects to obtain the one or more memory values
- `CL-12/a2` (부착: `CL-1/e2/e1`) → **M26** — computing one or more relevance measures for the plurality of memory objects based on the query
- `CL-12/a3` (부착: `CL-1/e2/e1`) → **M27** — returning a subset of the plurality of memory objects based on the relevance measure

### 종속항 `CL-13` — `single` (인용: CL-12)

> The method of claim 12, wherein the one or more relevance measures comprise:

a respective score generated based on distance between a query embedding and a respective memory value embedding; or

a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model.

- `CL-13/a1` (부착: `CL-1/e2/e1`) → **M28** — a respective score generated based on distance between a query embedding and a respective memory value embedding
- `CL-13/a2` (부착: `CL-1/e2/e1`) → **M29** — a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model

### 종속항 `CL-14` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13)

> The method of any of the preceding claims, wherein the one or more memory values each comprise a respective string, and wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values.

- `CL-14/a1` (부착: `CL-1/e2`) → **M30** — wherein the one or more memory values each comprise a respective string
- `CL-14/a2` (부착: `CL-1/e2`) → **M31** — wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values

### 종속항 `CL-15` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14)

> The method of any of the preceding claims, comprising:

inputting at least a portion of the output to the machine-learned sequence processing model; generating, based on processing the output using the machine-learned sequence processing model, the response to the query;

wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data.

- `CL-15/a1` (부착: `CL-1/e5`) → **M32** — inputting at least a portion of the output to the machine-learned sequence processing model
- `CL-15/a2` (부착: `CL-1/e5`) → **M33** — generating, based on processing the output using the machine-learned sequence processing model, the response to the query
- `CL-15/a3` (부착: `CL-1/e4`) → **M34** — wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data

### 종속항 `CL-16` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15)

> The method of any of the preceding claims, wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query.

- `CL-16/a1` (부착: `CL-1/e4`) → **M35** — wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query

### 종속항 `CL-17` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16)

> The method of any of the preceding claims, comprising:

consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset.

- `CL-17/a1` (부착: `CL-1/e2/e1`) → **M36** — consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset

### 종속항 `CL-18` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17)

> The method of any of the preceding claims, comprising:

receiving input data associated with a timestamp;

creating a current memory object comprising:

the timestamp; and

a current memory value based on the input data;

matching the current memory object to a prior memory object; and 

replacing, in the interaction memory datastore, the prior memory object with the current memory object.

- `CL-18/a1` (부착: `CL-1/e2/e1`) → **M37** — receiving input data associated with a timestamp
- `CL-18/a2` (부착: `CL-1/e2/e1`) → **M38** — creating a current memory object comprising:

the timestamp; and

a current memory value based on the input data
- `CL-18/a3` (부착: `CL-1/e2/e1`) → **M39** — matching the current memory object to a prior memory object
- `CL-18/a4` (부착: `CL-1/e2/e1`) → **M40** — replacing, in the interaction memory datastore, the prior memory object with the current memory object

### 종속항 `CL-19` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18)

> The method of any of the preceding claims, comprising:

receiving input data associated with a timestamp;

matching at least a portion of the input data to a prior memory object;

updating, in the interaction memory datastore, the prior memory object based on the portion of the input data.

- `CL-19/a1` (부착: `CL-1/e2/e1`) → **M41** — receiving input data associated with a timestamp
- `CL-19/a2` (부착: `CL-1/e2/e1`) → **M42** — matching at least a portion of the input data to a prior memory object
- `CL-19/a3` (부착: `CL-1/e2/e1`) → **M43** — updating, in the interaction memory datastore, the prior memory object based on the portion of the input data

### 종속항 `CL-20` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19)

> The method of any of the preceding claims, wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action.

- `CL-20/a1` (부착: `CL-1/e5`) → **M44** — wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action

### 종속항 `CL-21` — `single` (인용: CL-20)

> The method of claim 20, wherein the query indicates a configuration parameter that controls an operation of the computing system, and wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter.

- `CL-21/a1` (부착: `CL-1/e1`) → **M45** — wherein the query indicates a configuration parameter that controls an operation of the computing system
- `CL-21/a2` (부착: `CL-1/e5`) → **M46** — wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter

### 종속항 `CL-22` — `single` (인용: CL-21)

> The method of claim 21 , wherein the configuration parameter is associated with at least one of:

data access by the computing system;

data retention by the computing system; or

data communication by the computing system.

- `CL-22/a1` (부착: `CL-1/e1`) → **M47** — wherein the configuration parameter is associated with at least one of:

data access by the computing system;

data retention by the computing system; or

data communication by the computing system

### 종속항 `CL-23` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-23/a1` (부착: `CL-1/e1`) → **M48** — One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims

### 종속항 `CL-24` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> A computing system, comprising:

one or more processors; and

one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-24/a1` (부착: `CL-1/e1`) → **M49** — one or more processors
- `CL-24/a2` (부착: `CL-1/e1`) → **M50** — one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims

### 종속항 `CL-25` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-25/a1` (부착: `CL-1/e1`) → **M51** — A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims

## 3. 유기적 통합 그림 (D5 ④)

- **M107** (spec · stated) — The memory is not a transcript but a set of structured containers, each holding a value plus metadata, so that recall can filter on attributes rather than re-reading raw history.
  - 근거 항목: M59, M68, M81
  - 인용: “a memory object can be a data container that stores one or more memory values”
- **M108** (spec · stated) — Storing memories in the modality in which they were received (audio, image) is meant to preserve context that a text transcription would discard.
  - 근거 항목: M58, M60, M61
  - 인용: “These audio recordings can capture rich contextual information that may be lost in the transcription”
- **M109** (spec · stated) — Keeping the supporting interactions alongside a memory value lets a later contradicting input refine the memory instead of simply overwriting it.
  - 근거 항목: M59, M69, M93
  - 인용: “new information can serve to refine and build more nuanced memories rather than noisily overcorrecting based on limited information”
- **M110** (spec · stated) — Timestamps and optional expiration times on memory objects are the mechanism by which forgetting after an interval is implemented during maintenance cycles.
  - 근거 항목: M73, M74, M72
  - 인용: “Memory objects exceeding their expiration time may be automatically deleted during scheduled maintenance operations.”
- **M111** (spec · stated) — Because the memory is built from conversation, the same conversational channel doubles as the control surface for erasing or limiting it.
  - 근거 항목: M73, M71
  - 인용: “the user can also use the same interaction mechanism to limit, erase, or otherwise modify the memory of the machine-learned agent system”
- **M112** (effects · stated) — Extracting memories offline from cached interactions is positioned as shifting compute away from query time, so runtime inference reads condensed objects rather than raw history.
  - 근거 항목: M64, M70, M66
  - 인용: “by pre-processing user interactions offline, the system can create high-quality memory data objects containing key features and metadata”
- **M113** (spec · stated) — The response can itself be an API call, so recalled memory conditions actions taken on a device, not only text returned to the user.
  - 근거 항목: M57, M99, M100
  - 인용: “response 122 can include an application programming interface call generated based on output data structure 120”
- **M114** (spec · inferred) — The disclosure deliberately leaves open where conflict resolution happens: offline consolidation against existing memories, or at runtime with all retrieved memories in view.
  - 근거 항목: M64, M67, M71
  - 인용: “Runtime queries can be processed in full view of all retrieved memories.”
- **M115** (spec · stated) — Ordering recalled values by timestamp is how recency is communicated to the model for resolving conflicting memories.
  - 근거 항목: M75, M82, M78
  - 인용: “This ordering allows the machine-learned agent system to prioritize more recent context when making inferences.”

## 4. 포지셔닝 (D5 ⑤)

- **M116**
  - 배경 문제: Agents without memory force users to re-enter the same details across sessions, and the alternative of wiring the agent to external data sources gives the user an all-or-nothing access choice with data the agent does not curate.
  - 주장 효과: The specification asserts that a user-specific, agent-curated interaction memory lets a task start from a single interaction, supports asynchronous execution of previously instructed tasks, reduces runtime load by pre-processing memories offline, and gives the user control over what is remembered and forgotten.
  - 차이: No performance numbers are given; the claimed difference is structural: memory objects generated from prior interactions with the user, retrieved by relevance and fed into a sequence model input, rather than raw history or uncurated external sources.
  - 인용: “the user may be faced with an all-or-nothing choice, which may be undesirable in some circumstances”
  - 인용: “can initiate execution with a single interaction”

## 5. 구성요소와 3중 접지 (D5 ③)

| 구성요소 | 청구항 좌표 | 라벨(EN) | 접지 |
|---|---|---|---|
| **M1** | `CL-1/e1` | receiving a user-associated query by the agent system | **M52** (명세서 found · 도면 found) |
| **M2** | `CL-1/e2` | accessing memory data from the user's interaction memory datastore | **M53** (명세서 found · 도면 found) |
| **M3** | `CL-1/e2/e1` | datastore comprising memory objects generated from prior interactions | **M54** (명세서 found · 도면 found) |
| **M4** | `CL-1/e3` | inputting a query-and-memory input data structure to a sequence processing model | **M55** (명세서 found · 도면 found) |
| **M5** | `CL-1/e4` | generating an output by processing the input data structure | **M56** (명세서 found · 도면 found) |
| **M6** | `CL-1/e5` | outputting a response to the query based on the output | **M57** (명세서 found · 도면 found) |
| **M7** | `CL-2/a1` | datastore comprising multimodal data | **M58** (명세서 found · 도면 found) |
| **M8** | `CL-2/a2` | memory data based on memory objects of two data modalities | **M59** (명세서 found · 도면 found) |
| **M9** | `CL-3/a1` | audio and image modality pair | **M60** (명세서 found · 도면 found) |
| **M10** | `CL-3/a2` | text and image modality pair | **M61** (명세서 found · 도면 found) |
| **M11** | `CL-3/a3` | text and audio modality pair | **M62** (명세서 found · 도면 found) |
| **M12** | `CL-4/a1` | retrieving memory values by relevance to the query | **M63** (명세서 found · 도면 found) |
| **M13** | `CL-5/a1` | processing session input with a model to generate values | **M64** (명세서 found · 도면 found) |
| **M14** | `CL-5/a2` | condition: values indicate a portion of input is to be stored | **M65** (명세서 found · 도면 found) |
| **M15** | `CL-5/a3` | extracting the portion | **M66** (명세서 found · 도면 found) |
| **M16** | `CL-5/a4` | storing the portion as a memory value in a memory object | **M67** (명세서 found · 도면 found) |
| **M17** | `CL-6/a1` | storing metadata with the memory value | **M68** (명세서 found · 도면 found) |
| **M18** | `CL-7/a1` | portion comprises text, image, or audio data | **M69** (명세서 found · 도면 found) |
| **M19** | `CL-8/a1` | portion corresponds to an explicit remember instruction | **M70** (명세서 found · 도면 found) |
| **M20** | `CL-9/a1` | receiving a forget instruction | **M71** (명세서 found · 도면 found) |
| **M21** | `CL-9/a2` | deleting specified information from the datastore | **M72** (명세서 found · 도면 found) |
| **M22** | `CL-10/a1` | receiving a delayed forget instruction | **M73** (명세서 found · 도면 found) |
| **M23** | `CL-10/a2` | queuing information for deletion after the interval | **M74** (명세서 found · 도면 found) |
| **M24** | `CL-11/a1` | memory data as timestamp-ordered combination of memory values | **M75** (명세서 found · 도면 found) |
| **M25** | `CL-12/a1` | filtering memory objects to obtain memory values | **M76** (명세서 found · 도면 found) |
| **M26** | `CL-12/a2` | computing query-based relevance measures | **M77** (명세서 found · 도면 found) |
| **M27** | `CL-12/a3` | returning a relevance-based subset of memory objects | **M78** (명세서 found · 도면 found) |
| **M28** | `CL-13/a1` | relevance score from embedding distance | **M79** (명세서 found · 도면 found) |
| **M29** | `CL-13/a2` | relevance as sequence output of a second sequence processing model | **M80** (명세서 found · 도면 found) |
| **M30** | `CL-14/a1` | memory values each comprise a string | **M81** (명세서 found · 도면 found) |
| **M31** | `CL-14/a2` | memory data as a string of the memory value strings | **M82** (명세서 found · 도면 found) |
| **M32** | `CL-15/a1` | feeding a portion of the output back to the sequence processing model | **M83** (명세서 found · 도면 found) |
| **M33** | `CL-15/a2` | generating the response by processing the output | **M84** (명세서 found · 도면 found) |
| **M34** | `CL-15/a3` | output comprises predictions for analytical content about query and memory data | **M85** (명세서 found · 도면 found) |
| **M35** | `CL-16/a1` | analytical content predictions not exposed on the user interface | **M86** (명세서 found · 도면 found) |
| **M36** | `CL-17/a1` | consolidating aligned memory objects into a single memory object | **M87** (명세서 found · 도면 found) |
| **M37** | `CL-18/a1` | receiving timestamped input data | **M88** (명세서 found · 도면 found) |
| **M38** | `CL-18/a2` | creating a current memory object with timestamp and current memory value | **M89** (명세서 found · 도면 found) |
| **M39** | `CL-18/a3` | matching current memory object to a prior memory object | **M90** (명세서 found · 도면 found) |
| **M40** | `CL-18/a4` | replacing the prior memory object with the current one | **M91** (명세서 found · 도면 found) |
| **M41** | `CL-19/a1` | receiving timestamped input data | **M92** (명세서 found · 도면 found) |
| **M42** | `CL-19/a2` | matching a portion of input data to a prior memory object | **M93** (명세서 found · 도면 found) |
| **M43** | `CL-19/a3` | updating the prior memory object from the input portion | **M94** (명세서 found · 도면 found) |
| **M44** | `CL-20/a1` | response comprises API-controlling instructions causing an action | **M95** (명세서 found · 도면 found) |
| **M45** | `CL-21/a1` | query indicates a configuration parameter of the computing system | **M96** (명세서 found · 도면 found) |
| **M46** | `CL-21/a2` | instructions cause assignment of a configuration parameter value | **M97** (명세서 found · 도면 found) |
| **M47** | `CL-22/a1` | configuration parameter concerns data access, retention, or communication | **M98** (명세서 found · 도면 found) |
| **M48** | `CL-23/a1` | non-transitory media storing instructions performing the method | **M99** (명세서 found · 도면 found) |
| **M49** | `CL-24/a1` | one or more processors | **M100** (명세서 found · 도면 found) |
| **M50** | `CL-24/a2` | media storing instructions causing the system to perform the method | **M101** (명세서 found · 도면 found) |
| **M51** | `CL-25/a1` | computer program product with instructions performing the method | **M102** (명세서 found · 도면 not-depicted) |

- **M52** ← 구성요소 M1
  - 명세서 `[0065]`: “Input interface(s) 102 can receive inputs (e.g., from a user). Query 104 can be based on data from input interfaces 102.”
  - 도면 `FIG-1` (도면부호 102, 104): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M53** ← 구성요소 M2
  - 명세서 `[0066]`: “Machine-learned agent system 100 can issue a memory query 108 to interaction memory datastore 110.”
  - 도면 `FIG-1` (도면부호 100, 108, 110): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M54** ← 구성요소 M3
  - 명세서 `[0066]`: “Interaction memory datastore 110 can contain stored contextual information catalogued and stored over prior interactions with the user.”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M55** ← 구성요소 M4
  - 명세서 `[0067]`: “Machine-learned agent system 100 can output input data structure 116 based on memory data 114.”
  - 도면 `FIG-1` (도면부호 114, 116): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M56** ← 구성요소 M5
  - 명세서 `[0068]`: “Machine-learned model system 118 can process input data structure 116 to generate output data structure 120.”
  - 도면 `FIG-1` (도면부호 116, 118, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M57** ← 구성요소 M6
  - 명세서 `[0069]`: “Machine-learned agent system 100 can output response 122 based on output data structure 120.”
  - 도면 `FIG-1` (도면부호 120, 122): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M58** ← 구성요소 M7
  - 명세서 `[0100]`: “Interaction memory datastore 110 can be multimodal. For example, one or more queries can include data of a first modality and one or more queries can include data of a second modality.”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M59** ← 구성요소 M8
  - 명세서 `[0159]`: “A memory object can include data of a first modality and data of a second modality. Different modalities can be stored in different memory objects and linked through metadata.”
  - 도면 `FIG-2` (도면부호 202-1, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M60** ← 구성요소 M9
  - 명세서 `[0162]`: “interaction memory datastore 110 can store image data in association with audio data, such as a video recording recorded during an interaction session and a voice recording recorded during the interaction session.”
  - 도면 `FIG-2` (도면부호 110, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M61** ← 구성요소 M10
  - 명세서 `[0163]`: “interaction memory datastore 110 can store image data in association with text data, such as image data from a video recording recorded during an interaction session and a transcription from a voice recording recorded during the interaction session.”
  - 도면 `FIG-2` (도면부호 110, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M62** ← 구성요소 M11
  - 명세서 `[0164]`: “interaction memory datastore 110 can store audio data in association with text data. Audio data (e.g., music) and text data (e.g., comments on the music) can be stored as multimodal memories in interaction memory datastore 110.”
  - 도면 `FIG-2` (도면부호 110, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M63** ← 구성요소 M12
  - 명세서 `[0090]`: “For example, memory model 105 can initiate similarity search operations to retrieve a number of relevant stored memories for a particular query.”
  - 도면 `FIG-1` (도면부호 105, 106, 110): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M64** ← 구성요소 M13
  - 명세서 `[0088]`: “memory model 105 can invoke a machine-learned model input (e.g., after one or more inputs are received) that causes a machine-learned model to predict whether there is anything in the query that is to be remembered.”
  - 도면 `FIG-8` (도면부호 802, 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M65** ← 구성요소 M14
  - 명세서 `[0439]`: “The values can indicate that at least a portion of the input is to be stored.”
  - 도면 `FIG-8` (도면부호 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M66** ← 구성요소 M15
  - 명세서 `[0088]`: “Predicting new information to remember can include generating a portion or excerpt of content to remember.”
  - 도면 `FIG-8` (도면부호 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M67** ← 구성요소 M16
  - 명세서 `[0282]`: “Memory model 105 can execute a memory data write 806 to add or update memory data objects in interaction memory datastore 110.”
  - 도면 `FIG-8` (도면부호 806): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M68** ← 구성요소 M17
  - 명세서 `[0054]`: “Additional metadata may be stored in the memory object, such as a timestamp, the type of trigger used for storing the memory, a summary of the interaction during which the memory value was received, or other attributes.”
  - 도면 `FIG-2` (도면부호 206-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M69** ← 구성요소 M18
  - 명세서 `[0154]`: “A memory value can be extracted or excerpted from an interaction. For example, a visual memory can be stored by saving all or part of one or more images associated with an interaction session. A textual memory can be stored by saving all or part of one or more messages or documents associated with an interaction session. An audio memory can be stored by saving all or part of one or more audio files or streams associated with an interaction session.”
  - 도면 `FIG-2` (도면부호 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M70** ← 구성요소 M19
  - 명세서 `[0054]`: “An example explicit trigger may occur when a user instructs the machine-learned agent system to remember a particular piece of information, such as the user’s favorite architect.”
  - 도면 `FIG-7` (도면부호 702): “Figure 7 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M71** ← 구성요소 M20
  - 명세서 `[0293]`: “Explicit forgetting may be triggered by user commands such as “forget that,” “delete this conversation,” or “forget information related to [topic].””
  - 도면 `FIG-10` (도면부호 1002): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M72** ← 구성요소 M21
  - 명세서 `[0443]`: “Memory model 105 can then cause the identified memory objects to be deleted from interaction memory datastore 110.”
  - 도면 `FIG-10` (도면부호 1002, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M73** ← 구성요소 M22
  - 명세서 `[0057]`: “The user can instruct the machine-learned agent system to forget information after three months.”
  - 도면 `FIG-10` (도면부호 1002): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M74** ← 구성요소 M23
  - 명세서 `[0295]`: “Memory objects exceeding their expiration time may be automatically deleted during scheduled maintenance operations.”
  - 도면 `FIG-10` (도면부호 1002, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M75** ← 구성요소 M24
  - 명세서 `[0165]`: “In some implementations, the memory data includes an ordered combination of one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects.”
  - 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M76** ← 구성요소 M25
  - 명세서 `[0446]`: “the machine-learned agent system (e.g., 100) can use a memory query”
  - 도면 `FIG-3` (도면부호 302, 304, 306): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M77** ← 구성요소 M26
  - 명세서 `[0446]`: “The filtering process can involve computing one or more relevance measures (e.g., similarity scores, distance metrics, or probabilities) for each memory object”
  - 도면 `FIG-1` (도면부호 106, 108): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M78** ← 구성요소 M27
  - 명세서 `[0179]`: “The top-K most similar memory objects can be retrieved, where K is a configurable parameter.”
  - 도면 `FIG-3` (도면부호 302, 304, 306): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M79** ← 구성요소 M28
  - 명세서 `[0179]`: “A vector embedding of the pre-processed query can be compared to vector embeddings of values within memory objects stored in the database. This comparison can use similarity metrics like cosine similarity to identify memory objects semantically related to the query.”
  - 도면 `FIG-2` (도면부호 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M80** ← 구성요소 M29
  - 명세서 `[0447]`: “the one or more relevance measures include a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model.”
  - 도면 `FIG-13` (도면부호 4, 6): “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”
- **M81** ← 구성요소 M30
  - 명세서 `[0053]`: “a memory object can be a data container that stores one or more memory values (e.g., strings, images, audio, etc.) along with relevant metadata.”
  - 도면 `FIG-2` (도면부호 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M82** ← 구성요소 M31
  - 명세서 `[0182]`: “concatenating multiple textual memory values into a string representation for insertion into a prompt”
  - 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M83** ← 구성요소 M32
  - 명세서 `[0117]`: “A second input data structure can contain the generated analysis along with an instruction to generate a final response based on the analysis.”
  - 도면 `FIG-1` (도면부호 116, 118): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M84** ← 구성요소 M33
  - 명세서 `[0117]`: “A second output data structure can contain the final response. Machine-learned agent system 100 can generate response 122 based on the second output data structure, which was based on the first output data structure.”
  - 도면 `FIG-1` (도면부호 120, 122): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M85** ← 구성요소 M34
  - 명세서 `[0117]`: “For example, a first input data structure can contain an instruction to generate a thorough analysis of query 104 in view of memory data 114. Output data structure 120 can contain the generated analysis.”
  - 도면 `FIG-1` (도면부호 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M86** ← 구성요소 M35
  - 명세서 `[0117]`: “The raw outputs may not be surfaced to the user. For example, only a response 122 might be output to output interface(s) 124.”
  - 도면 `FIG-1` (도면부호 122, 124): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M87** ← 구성요소 M36
  - 명세서 `[0020]`: “In some implementations, the example method includes consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 요약 [0020]이 통합(consolidating) 한정을 문언 그대로 조응한다. 도면은 방법 흐름도 FIG-21 에 귀속하며, 흐름도는 도면부호를 갖지 않아 numerals 를 빈 배열로 둔다(절차 §5 ⓒ).
- **M88** ← 구성요소 M37
  - 명세서 `[0021]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: [0021]과 [0022]에 같은 문장이 두 번 나온다. 이 항목은 CL-18 계열이므로 교체(replacing) 서사를 여는 [0021]을 인용했다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M89** ← 구성요소 M38
  - 명세서 `[0021]`: “In some implementations, the example method includes creating a current memory object. In some implementations, the current memory object includes the timestamp. In some implementations, the current memory object includes a current memory value based on the input data.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 타임스탬프·현재 메모리 값 두 하위 한정이 한 문단에 연속하므로 세 문장을 최소 단위로 함께 인용했다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).
- **M90** ← 구성요소 M39
  - 명세서 `[0021]`: “In some implementations, the example method includes matching the current memory object to a prior memory object.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: FIG-21 은 도면부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M91** ← 구성요소 M40
  - 명세서 `[0021]`: “In some implementations, the example method includes replacing, in the interaction memory datastore, the prior memory object with the current memory object.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: FIG-21 은 도면부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M92** ← 구성요소 M41
  - 명세서 `[0022]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: CL-19 계열이므로 갱신(updating) 서사를 여는 [0022]를 인용했다([0021]에 동일 문장이 있으나 그것은 CL-18 계열이다). FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).
- **M93** ← 구성요소 M42
  - 명세서 `[0022]`: “In some implementations, the example method includes matching at least a portion of the input data to a prior memory object.”
  - 명세서 `[0453]`: “The system then matches at least a portion of the input data to a prior memory object”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 요약 [0022]와 상세 [0453]이 같은 한정을 조응한다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M94** ← 구성요소 M43
  - 명세서 `[0022]`: “In some implementations, the example method includes updating, in the interaction memory datastore, the prior memory object based on the portion of the input data.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 상세 대응은 [0453]이고 갱신 사례 도면으로는 FIG-5 도 후보이나, 청구항 한정이 방법 단계이므로 방법 흐름도 FIG-21 에 귀속했다. 흐름도는 부호가 없어 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M95** ← 구성요소 M44
  - 명세서 `[0023]`: “In some implementations of the example method, the response includes instructions configured to control an application programming interface to cause a computing system to perform an action.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 응답 출력 단계의 상세는 [0454]에 있다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M96** ← 구성요소 M45
  - 명세서 `[0024]`: “the query indicates a configuration parameter that controls an operation of the computing system”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: [0024] 한 문단이 두 한정(질의의 구성 파라미터 지시 / API 를 통한 값 배정)을 담으므로 조응이 보이는 최소 단위로 앞부분만 잘랐다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).
- **M97** ← 구성요소 M46
  - 명세서 `[0024]`: “the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: [0024]의 뒷부분이 이 한정에 조응한다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).
- **M98** ← 구성요소 M47
  - 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data access by the computing system. In some implementations of the example method, the configuration parameter is associated with data retention by the computing system. In some implementations of the example method, the configuration parameter is associated with data communication by the computing system.”
  - 도면 `FIG-21` (도면부호 ): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 청구항의 3택 열거(접근·보존·통신)가 [0025]의 세 문장에 1:1 로 대응하므로 세 문장을 함께 인용했다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).
- **M99** ← 구성요소 M48
  - 명세서 `[0026]`: “In an aspect, the present disclosure provides an example one or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
  - 도면 `FIG-19` (도면부호 ): “Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 매체 범주항의 도면 조응은 계산 장치 블록도(FIG-19)의 메모리·명령 요소다. 도면부호를 등재하면 그 정수가 수치 수확 정답지에서 배제되고 본문 부호와 도면 실물 부호의 일치를 이 조각만으로는 확인할 수 없으므로, numerals 를 빈 배열로 두고 캡션 인용으로 조응을 진다(절차 §5 ⓒ).
- **M100** ← 구성요소 M49
  - 명세서 `[0027]`: “In some implementations, the example computing system includes one or more processors.”
  - 도면 `FIG-19` (도면부호 ): “Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 프로세서 구성요소는 FIG-19 의 계산 장치 블록도에 표현되어 있으나, M2064 와 같은 이유(수확 배제 확대 · 실물 부호 대조 불가)로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M101** ← 구성요소 M50
  - 명세서 `[0027]`: “In some implementations, the example computing system includes one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising any implementation of the example method.”
  - 도면 `FIG-19` (도면부호 ): “Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 메모리·명령 요소는 FIG-19 에 표현되어 있으나 M2064·M2065 와 같은 이유로 numerals 는 빈 배열이다(절차 §5 ⓒ).
- **M102** ← 구성요소 M51
  - 명세서 `[0028]`: “In an aspect, the present disclosure provides an computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
  - 탐색 기록: 도면 캡션 전량(Figure 1~21)을 확인했으나 「컴퓨터 프로그램 제품」을 블록·요소로 그린 도면은 없다. FIG-19·FIG-20 은 장치와 응용/중앙 지능 층을 그릴 뿐 프로그램 제품 범주를 별도 요소로 표현하지 않는다.

## 6. 수치 사실 — 3분류 (재정 N9)

기계가 **무엇을 보증했는가**가 갈래마다 다르다. 갈래를 섞어 보면 승인은 형식이 된다.

### 6.1 원문 스팬 수치 (`quoted` · `bibliographic`)

- 원문 스팬 수치: **4건** — M103, M104, M105, M106
- 서지 복사: M103, M104, M105, M106 (`patent` 블록에서 결정론 복사)

- **M103** — bibliographic field patent.number · `WO2026-128750A1` → `WO2026-128750A1`
  - 원천 ``: “”
- **M104** — bibliographic field patent.dates.priority · `2024-12-11` → `2024-12-11`
  - 원천 ``: “”
- **M105** — bibliographic field patent.dates.filing · `2025-12-11` → `2025-12-11`
  - 원천 ``: “”
- **M106** — bibliographic field patent.dates.publication · `2026-06-18` → `2026-06-18`
  - 원천 ``: “”

### 6.2 파생 수치 (`derived`) — 산식과 원천 스팬을 나란히

_파생 수치 없음. 승인 봉투의 `derived_fact_ack` 는 빈 배열로 적는다._


### 6.3 도면 유래 수치 (`figure-sourced`) — 기계 검증 불가

_도면 유래 수치 없음._


## 7. ★ 사람 검증 필요 목록 (재정 R1)

도면에서 읽은 값은 기계가 대조할 원문 스팬이 없다. **검사가 통과시켰다는 사실이 값이**
**옳다는 뜻이 아니다.** 아래 목록은 봉투의 `manual_verification_ack[]` 와 정확히 일치해야 한다.

_해당 없음. 봉투에는 빈 배열로 적는다(생략은 누락과 '없음'을 구별하지 못한다)._


## 8. ★ 접지 예외 (재정 R3)

접지 전량이 원칙이므로 예외는 날조하거나 숨기지 않고 드러낸다. **예외가 많으면 그것이**
**소재 신호다.**

- **M102** (구성요소 M51) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: 도면 캡션 전량(Figure 1~21)을 확인했으나 「컴퓨터 프로그램 제품」을 블록·요소로 그린 도면은 없다. FIG-19·FIG-20 은 장치와 응용/중앙 지능 층을 그릴 뿐 프로그램 제품 범주를 별도 요소로 표현하지 않는다.

## 8-b. ★ Owner 판독 요청 — 레인 자기 신고 (재정 T58 ③)

레인이 스스로 확신이 서지 않는다고 가리킨 자리다. **자기 신고는 반향이다**(SPEC §9.34) —
여기 없다고 확실한 것이 아니고, 여기 있다고 틀린 것이 아니다. 봉투 `review_adjudicated[]` 로 전건 답한다.

### `CL-4` — dependent · `single` · depends_on CL-1
> The method of claim 1 , comprising:

retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query.
- **read-a/decompose** 의 이유: 「the one or more memory values」 는 CL-1 에 선행 도입이 없어(CL-1 은 memory objects·memory data 만 든다) 부착점을 CL-1/e2 로 두었다 — 선행사 결여를 Owner 가 어떻게 볼지에 따라 부착점이 달라진다.
- 부가 `CL-4/a1` (부착 `CL-1/e2`): “retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query”
- 답 자리: `{target: CL-4, verdict: confirmed|defect|undecided}`

### `CL-4/a1` — addition · `CL-4` · attaches_to `CL-1/e2` · **M12** · retrieving memory values by relevance to the query
> retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query
- **read-b/decompose** 의 이유: 'the one or more memory values'가 CL-1에 선행 근거가 없어 부착점을 memory data를 도입한 CL-1/e2로 골랐다 — 부착점이 확실치 않다.
- 종속항 `CL-4` 전문: “The method of claim 1 , comprising:

retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query.”
- 부착점 `CL-1/e2` · 부가 문언: “retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query”
- 답 자리: `{target: CL-4/a1, verdict: confirmed|defect|undecided}`

### `CL-5/a2` — addition · `CL-5` · attaches_to `CL-1/e2/e1` · **M14** · condition: values indicate a portion of input is to be stored
> based on the generated one or more values indicating that at least a portion of the input is to be stored
- **read-a/decompose** 의 이유: 「based on … to be stored:」 조건절을 독립 addition 으로 쪼갰다(평면 분할 ⓑ) — 순수 연결구로 보아 a3·a4 에 흡수해야 한다면 경계가 달라진다.
- **read-b/decompose** 의 이유: 'based on the generated one or more values indicating … to be stored:' 조건 도입구를 extracting 항에 붙여 하나의 addition으로 두고 storing을 형제로 쪼갰다 — 조건구를 두 항 모두에 남겨야 하는지 경계가 확실치 않다.
- 종속항 `CL-5` 전문: “The method of any of the preceding claims, comprising:

after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values; and 

based on the generated one or more values indicating that at least a portion of the input is to be stored:

extracting, by the machine-learned agent system, the portion; and

storing, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore.”
- 부착점 `CL-1/e2/e1` · 부가 문언: “based on the generated one or more values indicating that at least a portion of the input is to be stored”
- 두 실행의 차이: `addition-attachment` 축 — 정본에만 `based on the generated one or more values indicating that at least a portion of the input is to be s … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …`, 비교본에만 `based on the generated one or more values indicating that at least a portion of the input is to be s … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …`
- 답 자리: `{target: CL-5/a2, verdict: confirmed|defect|undecided}`

### `CL-11` — dependent · `all-preceding` · depends_on CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10
> The method of any of the preceding claims, wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects.
- **read-a/decompose** 의 이유: 「the plurality of memory objects」·「the one or more memory values」 모두 CL-1 에 선행사가 없다 — 부착점 CL-1/e2 가 맞는지, 선행사 결여를 결함으로 기록할지 Owner 판단이 필요하다.
- 부가 `CL-11/a1` (부착 `CL-1/e2`): “wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects”
- 답 자리: `{target: CL-11, verdict: confirmed|defect|undecided}`

### `CL-15/a1` — addition · `CL-15` · attaches_to `CL-1/e5` · **M32** · feeding a portion of the output back to the sequence processing model
> inputting at least a portion of the output to the machine-learned sequence processing model
- **read-a/decompose** 의 이유: 출력을 모델에 되먹이는 단계를 응답 산출(CL-1/e5) 밑에 두었으나 출력 생성(CL-1/e4) 밑도 가능하다 — 재귀 단계가 어느 요소를 한정하는지 Owner 가 보면 판가름난다.
- 종속항 `CL-15` 전문: “The method of any of the preceding claims, comprising:

inputting at least a portion of the output to the machine-learned sequence processing model; generating, based on processing the output using the machine-learned sequence processing model, the response to the query;

wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data.”
- 부착점 `CL-1/e5` · 부가 문언: “inputting at least a portion of the output to the machine-learned sequence processing model”
- 두 실행의 차이: `addition-attachment` 축 — 정본에만 `inputting at least a portion of the output to the machine-learned sequence processing model | outputting, by the machine-learned agent system, and based on the output, a response to the query`, 비교본에만 `inputting at least a portion of the output to the machine-learned sequence processing model | generating, by the machine-learned agent system and based on processing the input data structure usi …`
- 답 자리: `{target: CL-15/a1, verdict: confirmed|defect|undecided}`

### `CL-16` — dependent · `all-preceding` · depends_on CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15
> The method of any of the preceding claims, wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query.
- **read-b/decompose** 의 이유: 'the plurality of predictions for analytical content'의 선행 근거가 CL-15에만 있는데 어형은 all-preceding이라 CL-1~CL-15 전부를 채웠다 — 실질 인용이 CL-15뿐인지 Owner가 보면 판가름난다.
- 부가 `CL-16/a1` (부착 `CL-1/e4`): “wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query”
- 답 자리: `{target: CL-16, verdict: confirmed|defect|undecided}`

### `CL-23` — dependent · `all-preceding` · depends_on CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22
> One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.
- **read-a/decompose** 의 이유: 매체항이 「the method of any of the preceding claims」로 방법항 CL-1~CL-22 를 되받는다고 읽어 all-preceding 으로 두었다(T13) — Owner 가 이 인용 범위(CL-22 까지) 를 확인하면 판가름난다.
- **read-b/decompose** 의 이유: 매체항이 'the method of any of the preceding claims'로 되받으므로 depends_on을 방법항 CL-1~CL-22로 채웠다 — 카테고리 전환형은 T13에 따라 all-preceding으로 두었으니 그 범위 해석이 맞는지 봐 주면 판가름난다.
- 부가 `CL-23/a1` (부착 `CL-1/e1`): “One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims”
- 답 자리: `{target: CL-23, verdict: confirmed|defect|undecided}`

### `CL-24` — dependent · `all-preceding` · depends_on CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22
> A computing system, comprising:

one or more processors; and

one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims.
- **read-a/decompose** 의 이유: 선행 청구항에 매체항 CL-23 이 있으나 「the method of」 이므로 CL-23 을 depends_on 에서 뺐다 — 이 배제가 맞는지 Owner 가 보면 판가름난다.
- **read-b/decompose** 의 이유: 'the method of'가 방법항만 가리킨다고 읽어 CL-23(매체항)을 depends_on에서 뺐다 — CL-23을 포함시켜야 하는지가 확실치 않다.
- 부가 `CL-24/a1` (부착 `CL-1/e1`): “one or more processors”
- 부가 `CL-24/a2` (부착 `CL-1/e1`): “one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims”
- 답 자리: `{target: CL-24, verdict: confirmed|defect|undecided}`

### `CL-25` — dependent · `all-preceding` · depends_on CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22
> A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.
- **read-a/decompose** 의 이유: CL-24 와 같은 이유로 CL-23·CL-24 를 인용 범위에서 뺐다 — 방법항만 인용한다는 독해의 확인이 필요하다.
- **read-b/decompose** 의 이유: 같은 이유로 CL-23·CL-24(매체·시스템항)를 depends_on에서 뺐다 — 방법항만 인용한다는 독해가 맞는지 확인이 필요하다.
- 부가 `CL-25/a1` (부착 `CL-1/e1`): “A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims”
- 답 자리: `{target: CL-25, verdict: confirmed|defect|undecided}`

### `M66` — grounding · 대상 **M15** (`CL-5/a3` · extracting the portion) · 명세서 `found` · 도면 `found`
> extracting, by the machine-learned agent system, the portion
- **read-a/ground-dependent** 의 이유: CL-5/a3 「extracting the portion」의 조응으로 [0088] 을 들었으나 이 문단은 추출을 「remember 할 내용의 발췌 예측」으로 서술해 청구항 어형과 다르다. [0439] 의 재서술이 더 가까울 수 있어 어느 쪽을 정본 인용으로 둘지 판단을 요청한다.
- 명세서 `[0088]`: “Predicting new information to remember can include generating a portion or excerpt of content to remember.”
- 도면 `FIG-8` (도면부호 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- 답 자리: `{target: M66, verdict: confirmed|defect|undecided}`

### `M80` — grounding · 대상 **M29** (`CL-13/a2` · relevance as sequence output of a second sequence processing model) · 명세서 `found` · 도면 `found`
> a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model
- **read-a/ground-dependent** 의 이유: CL-13/a2 의 「second machine-learned sequence processing model」이 도면상 별개 블록으로 표현되지 않는다 — FIG-13 의 모델 4·예측층 6 을 부호로 들었으나 이것이 「두 번째」 모델인지는 도면으로 판가름나지 않는다. [0447] 문언과 FIG-13 을 함께 보아 부호 부착의 타당성을 확인해 주기 바란다.
- 명세서 `[0447]`: “the one or more relevance measures include a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model.”
- 도면 `FIG-13` (도면부호 4, 6): “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”
- 답 자리: `{target: M80, verdict: confirmed|defect|undecided}`

### `M99` — grounding · 대상 **M48** (`CL-23/a1` · non-transitory media storing instructions performing the method) · 명세서 `found` · 도면 `found`
> One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims
- **read-a/ground-dependent** 의 이유: 범주항 3건(CL-23·CL-24·CL-25)은 방법 한정이 아니라 청구 범주 전환이라 도면 자리가 관례적이다 — 장치 도면(FIG-19)에 붙이는 것이 맞는지 도면 예외로 두는 것이 맞는지 Owner 가 한 번 정해 주면 M2065·M2066·M2067 이 같은 기준으로 정렬된다.
- 명세서 `[0026]`: “In an aspect, the present disclosure provides an example one or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
- 도면 `FIG-19` (도면부호 ): “Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.”
- 탐색 기록: 매체 범주항의 도면 조응은 계산 장치 블록도(FIG-19)의 메모리·명령 요소다. 도면부호를 등재하면 그 정수가 수치 수확 정답지에서 배제되고 본문 부호와 도면 실물 부호의 일치를 이 조각만으로는 확인할 수 없으므로, numerals 를 빈 배열로 두고 캡션 인용으로 조응을 진다(절차 §5 ⓒ).
- 답 자리: `{target: M99, verdict: confirmed|defect|undecided}`

### `M102` — grounding · 대상 **M51** (`CL-25/a1` · computer program product with instructions performing the method) · 명세서 `found` · 도면 `not-depicted` (§8 에도 있음)
> A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims
- **read-a/ground-dependent** 의 이유: 컴퓨터 프로그램 제품(CL-25)을 도면 미표현으로 신고했으나, FIG-19·FIG-20 의 응용/명령 블록을 그 조응으로 볼 여지가 있다 — 두 도면 실물의 블록 표기를 보면 not-depicted 유지 여부가 판가름난다.
- 명세서 `[0028]`: “In an aspect, the present disclosure provides an computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
- 탐색 기록: 도면 캡션 전량(Figure 1~21)을 확인했으나 「컴퓨터 프로그램 제품」을 블록·요소로 그린 도면은 없다. FIG-19·FIG-20 은 장치와 응용/중앙 지능 층을 그릴 뿐 프로그램 제품 범주를 별도 요소로 표현하지 않는다.
- 답 자리: `{target: M102, verdict: confirmed|defect|undecided}`

### `M114` — implication · basis `spec` · confidence `inferred`
> The disclosure deliberately leaves open where conflict resolution happens: offline consolidation against existing memories, or at runtime with all retrieved memories in view.
- **read-a/synthesize** 의 이유: FIG-8 방식(기존 기억 미참조)과 FIG-9 방식(기존 기억 참조)을 「의도적으로 열어 둔 선택」으로 읽었는데, 명세서는 두 접근의 장단만 나열할 뿐 선택을 열어 둔다고 명시하지 않으므로 [0291]을 보고 inferred 유지 여부를 판가름해 달라.
- 근거 인용: “Runtime queries can be processed in full view of all retrieved memories.”
- 파생 원천: **M64** · **M67** · **M71**
- 답 자리: `{target: M114, verdict: confirmed|defect|undecided}`

## 9. drop 신호 (D4 — 최종)

- 단계: `final` · 판정: `go`
- 사유: 대화형 에이전트가 사용자별 기억을 쌓고·잊고·정정하는 구조는 일반 독자가 자기 경험(같은 말 반복 입력, 잊어달라는 요청)에 바로 잇댈 수 있어 안도감 서사가 성립한다. 성능 수치는 없으나 구조적 차이(사용자 발화로 만든 기억 객체 · 지원 기록 · 만료 기반 망각)가 명확하다.

## 10. ★ 미분류 종속 구조 (재정 P-1)

Markush·조건부·수단항·카테고리 전환은 typed operator 입법을 범위에서 **제외**했고,
대신 `unclassified` 표지 + 이 목록 + 판정 행 계수 셋으로 침묵을 막는다.
**이 목록의 항목은 결함이 아니다** — 구조 미분류라는 사실의 표지이며, 종속 형태
판정(`parse.set-equals`·`parse.type-agrees`)의 대상에서 빠졌다는 뜻이다. 전문은
이미 보존되어 있으므로(재정 R1) 여기서 사람 눈이 마지막 심급이 된다.
이 목록은 정본 실행 `read-a` 의 신고다. 두 실행이 갈린 신고는 아래 10-b 블록에 있다.

_미분류 종속항 없음 — 전 종속항이 5종 어형으로 파싱되었다._


## 10-b. ★ 조기 합집합 — 두 실행이 갈린 미분류 신고 (재정 T31)

갈린 신고 없음 — 두 실행의 미분류 신고가 전건 일치

## 11. ★ 맹검 스크리닝 메모 — 두 실행 병기 (재정 P-A · P-U4)

분해 직후 `read-a`·`read-b` 가 **각자** 적은 1차 판단이다. 상신이 아니었고 런을
세우지 않았으며, 최종 서사 평가 레인에는 비공개였다(앵커링 방지). 둘 다 싣는 이유는
**두 독립 관찰의 일치/불일치 자체가 신호**이기 때문이다 — 한 건으로 합치면 그 신호가
소멸한다.

| 실행 | 방향 | 근거 요지 |
|---|---|---|
| `read-a` | `clear` | 「AI 비서가 나와의 과거 대화를 기억하고, 잊으라면 잊는다」라는 한 문장으로 전달되는 소재이며 종속항의 remember·forget·타이머 삭제·기억 통합·설정 변경 API 가 일반 독자에게 익숙한 장면을 준다. 다만 독립항 1 은 메모리 조회 후 모델 입력이라는 매우 넓은 골격이라 「무엇이 새로운가」 축은 접지 뒤 재확인이 필요하다. |
| `read-b` | `clear` | 권리 관심이 '대화를 기억했다가 다음 질문에 쓰는 AI 비서'라는 한 구성에 뚜렷하고, 기억하라·잊어라·일정 시간 뒤 잊어라(CL-8~10) 같은 종속항이 일반 독자에게 바로 와닿는 서사 재료라 안도감 있는 스레드가 설 것 같다. |

두 관찰의 방향이 `clear` 로 일치했다.

## 12. ★ 수치 인벤토리 — 전수 수확 (재정 P-B)

수치는 접지 스팬과 서지면에서 **전수 기계 수확**되었고, 중요분은 LLM 의 중요도
판단이 아니라 함의·포지셔닝이 실제로 참조했는가(`numeric_refs`)로 **역참조 도출**된다.

**수확 정답지 4건(kind fact · origin ∈ {quoted, bibliographic} · status active) — 참조 0건 표시, 미참조 4건 접힘**

_카운트를 상시 표기하는 이유: 카운트가 없으면 미참조분 접힘이 은폐가 된다._

역참조 총 0건 중 **0건이 이 정답지 밖**이다. 정답지 밖 참조는 수확기 소유가 아닌 수치(`derived`·`figure-sourced`)이거나
철회·대체된 항목이며, 위 계수에 들지 않는다.

### 12.1 참조된 수치 (함의·포지셔닝의 근거)

_참조된 수치 없음._


### 12.2 미참조 수치 4건 (접힘 — 숨김이 아니다)

<details>
<summary>미참조 4건 펼치기</summary>

- **M103** — bibliographic field patent.number · `WO2026-128750A1` → `WO2026-128750A1`
- **M104** — bibliographic field patent.dates.priority · `2024-12-11` → `2024-12-11`
- **M105** — bibliographic field patent.dates.filing · `2025-12-11` → `2025-12-11`
- **M106** — bibliographic field patent.dates.publication · `2026-06-18` → `2026-06-18`

</details>

★ 미참조 수치를 본문이 처음 인용하면 CP2 에 **"미검토 수치 사용" 플래그**가 자동
첨부된다(재정 P-B). 무검토 게시 경로는 없다 — 모든 수치는 CP1 검토 또는 사용 시 검토다.

### 12.3 수확하지 못한 토큰 36건 (숨기지 않고 센다)

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
| `figure-numeral` | 36 |

<details>
<summary>전건 36건 펼치기</summary>

| 위치 | 토큰 | 사유 |
|---|---|---|
| `[0065]` | `102` | figure-numeral |
| `[0065]` | `104` | figure-numeral |
| `[0065]` | `102` | figure-numeral |
| `[0066]` | `100` | figure-numeral |
| `[0066]` | `108` | figure-numeral |
| `[0066]` | `110` | figure-numeral |
| `[0066]` | `110` | figure-numeral |
| `[0067]` | `100` | figure-numeral |
| `[0067]` | `116` | figure-numeral |
| `[0067]` | `114` | figure-numeral |
| `[0068]` | `118` | figure-numeral |
| `[0068]` | `116` | figure-numeral |
| `[0068]` | `120` | figure-numeral |
| `[0069]` | `100` | figure-numeral |
| `[0069]` | `122` | figure-numeral |
| `[0069]` | `120` | figure-numeral |
| `[0100]` | `110` | figure-numeral |
| `[0162]` | `110` | figure-numeral |
| `[0163]` | `110` | figure-numeral |
| `[0164]` | `110` | figure-numeral |
| `[0164]` | `110` | figure-numeral |
| `[0090]` | `105` | figure-numeral |
| `[0088]` | `105` | figure-numeral |
| `[0282]` | `105` | figure-numeral |
| `[0282]` | `806` | figure-numeral |
| `[0282]` | `110` | figure-numeral |
| `[0443]` | `105` | figure-numeral |
| `[0443]` | `110` | figure-numeral |
| `[0446]` | `100` | figure-numeral |
| `[0117]` | `100` | figure-numeral |
| `[0117]` | `122` | figure-numeral |
| `[0117]` | `104` | figure-numeral |
| `[0117]` | `114` | figure-numeral |
| `[0117]` | `120` | figure-numeral |
| `[0117]` | `122` | figure-numeral |
| `[0117]` | `124` | figure-numeral |

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
| `addition-attachment` | `measure-only` | 0.2794 | - | `measured` |

### 13.2 갈린 항목

- `addition-attachment`
  - 정본에만: a respective score generated based on distance between a query embedding and a respective memory val … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: a respective sequence output generated by processing the query and one or more respective memory val … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: after receiving an input during an interactive session, processing, by the machine-learned agent sys … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: based on the generated one or more values indicating that at least a portion of the input is to be s … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: computing one or more relevance measures for the plurality of memory objects based on the query | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: creating a current memory object comprising:

the timestamp; and

a current memory value based on th … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: extracting, by the machine-learned agent system, the portion | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: filtering the plurality of memory objects to obtain the one or more memory values | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: inputting at least a portion of the output to the machine-learned sequence processing model | outputting, by the machine-learned agent system, and based on the output, a response to the query
  - 정본에만: matching at least a portion of the input data to a prior memory object | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: matching the current memory object to a prior memory object | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: receiving input data associated with a timestamp | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: replacing, in the interaction memory datastore, the prior memory object with the current memory obje … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: returning a subset of the plurality of memory objects based on the relevance measure | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: storing, by the machine-learned agent system, metadata associated with the memory value in the memor … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: storing, by the machine-learned agent system, the portion as a memory value in a memory object in th … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: the first data modality comprises audio data, and wherein the second data modality comprises image d … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: the first data modality comprises text data, and wherein the second data modality comprises audio da … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 정본에만: the first data modality comprises text data, and wherein the second data modality comprises image da … | wherein the interaction memory datastore comprises one or more memory objects that were generated ba …
  - 비교본에만: a respective score generated based on distance between a query embedding and a respective memory val … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: a respective sequence output generated by processing the query and one or more respective memory val … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: after receiving an input during an interactive session, processing, by the machine-learned agent sys … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: based on the generated one or more values indicating that at least a portion of the input is to be s … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: computing one or more relevance measures for the plurality of memory objects based on the query | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: creating a current memory object comprising:

the timestamp; and

a current memory value based on th … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: filtering the plurality of memory objects to obtain the one or more memory values | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: inputting at least a portion of the output to the machine-learned sequence processing model | generating, by the machine-learned agent system and based on processing the input data structure usi …
  - 비교본에만: matching at least a portion of the input data to a prior memory object | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: matching the current memory object to a prior memory object | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: receiving input data associated with a timestamp | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: replacing, in the interaction memory datastore, the prior memory object with the current memory obje … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: returning a subset of the plurality of memory objects based on the relevance measure | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: storing, by the machine-learned agent system, metadata associated with the memory value in the memor … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: storing, by the machine-learned agent system, the portion as a memory value in a memory object in th … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: the first data modality comprises audio data, and wherein the second data modality comprises image d … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: the first data modality comprises text data, and wherein the second data modality comprises audio da … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: the first data modality comprises text data, and wherein the second data modality comprises image da … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …
  - 비교본에만: updating, in the interaction memory datastore, the prior memory object based on the portion of the i … | accessing, by the machine-learned agent system, memory data from an interaction memory datastore ass …

## 14. 도면

- `FIG-1` — “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-01.png` · 도면부호 102, 104, 105, 106, 108, 110, 114, 116, 118, 120, 122, 124
- `FIG-2` — “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-02.png` · 도면부호 110, 202-1, 204-1, 206-1
- `FIG-3` — “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-03.png` · 도면부호 302, 304, 306, 308
- `FIG-7` — “Figure 7 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-07.png` · 도면부호 702
- `FIG-8` — “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-08.png` · 도면부호 802, 804, 806
- `FIG-10` — “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-10.png` · 도면부호 1002, 804
- `FIG-13` — “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-13.png` · 도면부호 4, 6
- `FIG-19` — “Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-19.png` · 도면부호 
- `FIG-21` — “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-21.png` · 도면부호 
- **M117** (FIG-1) — Overall agent pipeline from input interfaces and query through the memory model, recall cycle, datastore query and response, memory data, input data structure, model system, output data structure, response, and output interfaces. · 도면부호 102, 104, 105, 106, 108, 110, 114, 116, 118, 120, 122, 124
- **M118** (FIG-2) — Structure of the interaction memory datastore as a set of memory objects, each holding memory values and memory metadata. · 도면부호 110, 202-1, 204-1, 206-1
- **M119** (FIG-3) — Example recall cycle in which three retrieved memory objects are condensed into memory data for the model input. · 도면부호 302, 304, 306, 308
- **M120** (FIG-7) — Communication sequence in which a trigger starts a memory update cycle before a later query drives a recall cycle and model inference. · 도면부호 702
- **M121** (FIG-8) — Memory update cycle in which cached inputs are sent to the model system, memory data updates are returned, and a memory data write is executed. · 도면부호 802, 804, 806
- **M122** (FIG-10) — Memory maintenance cycle in which a memory update request with current memory data drives the model to produce memory data updates independent of new input. · 도면부호 1002, 804
- **M123** (FIG-13) — Generic sequence processing model that turns inputs into an input sequence and uses prediction layers to emit an output sequence. · 도면부호 4, 6
- **M124** (FIG-19) — Example computing device in which each application carries its own machine learning library and models and talks to device components through an API. · 도면부호 
- **M125** (FIG-21) — Flowchart of the claimed method: receive query, access memory data, input data structure to sequence model, generate output, output response. · 도면부호 

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
| **M44** | 구성요소 | active | - |
| **M45** | 구성요소 | active | - |
| **M46** | 구성요소 | active | - |
| **M47** | 구성요소 | active | - |
| **M48** | 구성요소 | active | - |
| **M49** | 구성요소 | active | - |
| **M50** | 구성요소 | active | - |
| **M51** | 구성요소 | active | - |
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
| **M87** | 3중 접지 | active | - |
| **M88** | 3중 접지 | active | - |
| **M89** | 3중 접지 | active | - |
| **M90** | 3중 접지 | active | - |
| **M91** | 3중 접지 | active | - |
| **M92** | 3중 접지 | active | - |
| **M93** | 3중 접지 | active | - |
| **M94** | 3중 접지 | active | - |
| **M95** | 3중 접지 | active | - |
| **M96** | 3중 접지 | active | - |
| **M97** | 3중 접지 | active | - |
| **M98** | 3중 접지 | active | - |
| **M99** | 3중 접지 | active | - |
| **M100** | 3중 접지 | active | - |
| **M101** | 3중 접지 | active | - |
| **M102** | 3중 접지 | active | - |
| **M103** | 수치 사실 | active | - |
| **M104** | 수치 사실 | active | - |
| **M105** | 수치 사실 | active | - |
| **M106** | 수치 사실 | active | - |
| **M107** | 기술적 함의 | active | - |
| **M108** | 기술적 함의 | active | - |
| **M109** | 기술적 함의 | active | - |
| **M110** | 기술적 함의 | active | - |
| **M111** | 기술적 함의 | active | - |
| **M112** | 기술적 함의 | active | - |
| **M113** | 기술적 함의 | active | - |
| **M114** | 기술적 함의 | active | - |
| **M115** | 기술적 함의 | active | - |
| **M116** | 포지셔닝 | active | - |
| **M117** | 도면 주석 | active | - |
| **M118** | 도면 주석 | active | - |
| **M119** | 도면 주석 | active | - |
| **M120** | 도면 주석 | active | - |
| **M121** | 도면 주석 | active | - |
| **M122** | 도면 주석 | active | - |
| **M123** | 도면 주석 | active | - |
| **M124** | 도면 주석 | active | - |
| **M125** | 도면 주석 | active | - |

## 16. 절차 이력

| 항목 | 값 |
|---|---|
| 독립 실행 | read-a:canonical, read-b:convergence-peer |
| 정본 실행 | `read-a` |
| 정본 지정 규칙 | `declaration-order` · 내용맹 `True` |
| 산출 시각 | 2026-09-13T05:41:04Z |
| 엔진 커밋 | `eb884936425687c5053cb40556f39a49a5f29952` |

분해는 **두 독립 실행**이 돌았고, 접지 이후는 **정본 1개**만 돌았다(재정 P-4).
정본 지정은 선언 순서이며 **내용을 보지 않는다** — 수렴 통과는 두 독해가 동치라는
선언이므로 정본 선택에 판정자가 없고, 남는 요구는 재현성뿐이기 때문이다. 두 실행은
서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.
