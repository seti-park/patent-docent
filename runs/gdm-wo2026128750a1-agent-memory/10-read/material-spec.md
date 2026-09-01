# CP1 판독본 (KR 틀 · EN 값) — `gdm-wo2026128750a1-agent-memory` (판 1)

상태 `draft` · 스키마 `material-spec/v0` · reader `0.8.0`

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
- `CL-2/a2` (부착: `CL-1/e2`) → **M8** — wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality

### 종속항 `CL-3` — `single` (인용: CL-2)

> The method of claim 2, wherein:

the first data modality comprises audio data, and wherein the second data modality comprises image data;

the first data modality comprises text data, and wherein the second data modality comprises image data; or

the first data modality comprises text data, and wherein the second data modality comprises audio data.

- `CL-3/a1` (부착: `CL-1/e2`) → **M9** — the first data modality comprises audio data, and wherein the second data modality comprises image data
- `CL-3/a2` (부착: `CL-1/e2`) → **M10** — the first data modality comprises text data, and wherein the second data modality comprises image data
- `CL-3/a3` (부착: `CL-1/e2`) → **M11** — the first data modality comprises text data, and wherein the second data modality comprises audio data

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
- `CL-5/a2` (부착: `CL-1/e2/e1`) → **M14** — based on the generated one or more values indicating that at least a portion of the input is to be stored:
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

- `CL-9/a1` (부착: `CL-1/e1`) → **M20** — receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information
- `CL-9/a2` (부착: `CL-1/e2/e1`) → **M21** — deleting, by the machine-learned agent system, the specified information from the interaction memory datastore

### 종속항 `CL-10` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9)

> The method of any of the preceding claims, comprising:

receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval; and

queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval.

- `CL-10/a1` (부착: `CL-1/e1`) → **M22** — receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval
- `CL-10/a2` (부착: `CL-1/e2/e1`) → **M23** — queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval

### 종속항 `CL-11` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10)

> The method of any of the preceding claims, wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects.

- `CL-11/a1` (부착: `CL-1/e2`) → **M24** — wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects

### 종속항 `CL-12` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11)

> The method of any of the preceding claims, comprising:

filtering the plurality of memory objects to obtain the one or more memory values, wherein the filtering comprises: 

computing one or more relevance measures for the plurality of memory objects based on the query; and

returning a subset of the plurality of memory objects based on the relevance measure.

- `CL-12/a1` (부착: `CL-1/e2`) → **M25** — filtering the plurality of memory objects to obtain the one or more memory values
- `CL-12/a2` (부착: `CL-1/e2`) → **M26** — computing one or more relevance measures for the plurality of memory objects based on the query
- `CL-12/a3` (부착: `CL-1/e2`) → **M27** — returning a subset of the plurality of memory objects based on the relevance measure

### 종속항 `CL-13` — `single` (인용: CL-12)

> The method of claim 12, wherein the one or more relevance measures comprise:

a respective score generated based on distance between a query embedding and a respective memory value embedding; or

a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model.

- `CL-13/a1` (부착: `CL-1/e2`) → **M28** — a respective score generated based on distance between a query embedding and a respective memory value embedding
- `CL-13/a2` (부착: `CL-1/e2`) → **M29** — a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model

### 종속항 `CL-14` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13)

> The method of any of the preceding claims, wherein the one or more memory values each comprise a respective string, and wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values.

- `CL-14/a1` (부착: `CL-1/e2`) → **M30** — wherein the one or more memory values each comprise a respective string
- `CL-14/a2` (부착: `CL-1/e2`) → **M31** — wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values

### 종속항 `CL-15` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14)

> The method of any of the preceding claims, comprising:

inputting at least a portion of the output to the machine-learned sequence processing model; generating, based on processing the output using the machine-learned sequence processing model, the response to the query;

wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data.

- `CL-15/a1` (부착: `CL-1/e3`) → **M32** — inputting at least a portion of the output to the machine-learned sequence processing model
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

- `CL-18/a1` (부착: `CL-1/e1`) → **M37** — receiving input data associated with a timestamp
- `CL-18/a2` (부착: `CL-1/e2/e1`) → **M38** — creating a current memory object comprising:
- `CL-18/a3` (부착: `CL-1/e2/e1`) → **M39** — the timestamp
- `CL-18/a4` (부착: `CL-1/e2/e1`) → **M40** — a current memory value based on the input data
- `CL-18/a5` (부착: `CL-1/e2/e1`) → **M41** — matching the current memory object to a prior memory object
- `CL-18/a6` (부착: `CL-1/e2/e1`) → **M42** — replacing, in the interaction memory datastore, the prior memory object with the current memory object

### 종속항 `CL-19` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18)

> The method of any of the preceding claims, comprising:

receiving input data associated with a timestamp;

matching at least a portion of the input data to a prior memory object;

updating, in the interaction memory datastore, the prior memory object based on the portion of the input data.

- `CL-19/a1` (부착: `CL-1/e1`) → **M43** — receiving input data associated with a timestamp
- `CL-19/a2` (부착: `CL-1/e2/e1`) → **M44** — matching at least a portion of the input data to a prior memory object
- `CL-19/a3` (부착: `CL-1/e2/e1`) → **M45** — updating, in the interaction memory datastore, the prior memory object based on the portion of the input data

### 종속항 `CL-20` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19)

> The method of any of the preceding claims, wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action.

- `CL-20/a1` (부착: `CL-1/e5`) → **M46** — wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action

### 종속항 `CL-21` — `single` (인용: CL-20)

> The method of claim 20, wherein the query indicates a configuration parameter that controls an operation of the computing system, and wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter.

- `CL-21/a1` (부착: `CL-1/e1`) → **M47** — wherein the query indicates a configuration parameter that controls an operation of the computing system
- `CL-21/a2` (부착: `CL-1/e5`) → **M48** — wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter

### 종속항 `CL-22` — `single` (인용: CL-21)

> The method of claim 21 , wherein the configuration parameter is associated with at least one of:

data access by the computing system;

data retention by the computing system; or

data communication by the computing system.

- `CL-22/a1` (부착: `CL-1/e1`) → **M49** — wherein the configuration parameter is associated with at least one of:
- `CL-22/a2` (부착: `CL-1/e1`) → **M50** — data access by the computing system
- `CL-22/a3` (부착: `CL-1/e1`) → **M51** — data retention by the computing system
- `CL-22/a4` (부착: `CL-1/e1`) → **M52** — data communication by the computing system

### 종속항 `CL-23` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-23/a1` (부착: `CL-1/e1`) → **M53** — One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations

### 종속항 `CL-24` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> A computing system, comprising:

one or more processors; and

one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-24/a1` (부착: `CL-1/e1`) → **M54** — one or more processors
- `CL-24/a2` (부착: `CL-1/e1`) → **M55** — one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations

### 종속항 `CL-25` — `all-preceding` (인용: CL-1, CL-2, CL-3, CL-4, CL-5, CL-6, CL-7, CL-8, CL-9, CL-10, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20, CL-21, CL-22)

> A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.

- `CL-25/a1` (부착: `CL-1/e1`) → **M56** — A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations

## 3. 유기적 통합 그림 (D5 ④)

- **M127** (claim · inferred) — Independent claim CL-1 covers only the read path. Its five steps are receive a query, access memory data, input a structure built from query plus memory, generate an output, output a response; every write-side operation that makes such a store exist at all — deciding what to remember, extracting it, storing it, forgetting it, consolidating it, updating it — is pushed into dependent claims 5 to 10 and 17 to 19. At its broadest the monopoly therefore reads on a system that only consumes a user-specific memory datastore populated by some other actor.
  - 근거 항목: M57, M58, M60, M61, M62
  - 인용: “accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user”
  - 인용: “after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values”
- **M128** (spec · inferred) — The unit of the invention is the memory object, not the memory value. Retrieval, consolidation, splitting, expiry and permission tiering all operate on the object and its metadata, while the sequence processing model only ever consumes values extracted out of objects. The description names the value an information bottleneck relative to the interactions behind it, which states plainly why the container exists: the object is where the engineering lives, and the value is the lossy thing the object is built to defend.
  - 근거 항목: M59, M64, M72, M73
  - 인용: “a memory object can be a data container that stores one or more memory values (e.g., strings, images, audio, etc.) along with relevant metadata”
  - 인용: “a memory value may operate as an information bottleneck as compared to the full record of interactions that support the memory value”
- **M129** (spec · inferred) — The support record is what makes a memory revisable rather than merely replaceable. Claim 18 matches a current object to a prior object and replaces it; claim 19 matches part of an input to a prior object and updates it. The description shows the second path only working because the object retains the interactions that produced its value: the vegetarian-to-pescatarian example turns an apparent contradiction into a refinement instead of an overwrite. Notably, FIG. 2 draws only a value slot and a metadata slot per object, so the mechanism that carries this argument is described at [0167] to [0172] but not depicted.
  - 근거 항목: M97, M98, M100, M101
  - 인용: “This can stabilize the evolution of memories over time by anchoring new memories in context of prior support.”
  - 인용: “the support record can be used to generate more nuanced memories that can reconcile the memory record”
- **M130** (spec · inferred) — FIG. 8, FIG. 9 and FIG. 10 encode a three-way choice about where conflict resolution happens, and the disclosure deliberately declines to settle it. FIG. 8 writes without reading the current store, which is cheap and defers every contradiction to query time. FIG. 9 writes in view of the current store, which consolidates early but costs more as the store grows and can propagate its own intermediate errors. FIG. 10 runs the cycle with no new input at all, purely as maintenance. The contribution disclosed here is the placement decision itself, not one placement.
  - 근거 항목: M69, M70, M71, M92
  - 인용: “This can offload the conflict resolution/interpretation task to a runtime execution of one or more models for processing a given query.”
  - 인용: “Runtime queries can be processed in full view of all retrieved memories.”
- **M131** (spec · inferred) — Forgetting is implemented as staged lossy re-encoding rather than deletion — video to sampled frames, frames to a single frame, frame to a textual summary — and the same ladder is then reused as an access-control hierarchy, with each permission level seeing memory obfuscated to a further stage. Because degraded versions are retained alongside the intact ones, a single mechanism yields both storage decay and a tiered privacy view served to external systems.
  - 근거 항목: M76, M77, M78, M79
  - 인용: “The schedule can be based on a time at which the memory was last accessed.”
  - 인용: “Although a schedule of forgetting memory information by memory model 105 may be understood in terms of time, it is also to be understood that a schedule can also correspond to a hierarchy of permissions.”
  - 인용: “Interaction memory datastore 110 can store multiple versions of memory content, with various levels of noise or obfuscation applied, to enable retrieval and use of various qualities of memory data.”
- **M132** (claim · inferred) — The most distinctive disclosed mechanisms are unclaimed. Graduated forgetting and the permission ladder, the support record and the reconciliation it enables, the typed knowledge-graph edges between memory objects, and the splitting of an overgrown object into sub-objects all appear nowhere in claims 1 to 25. What is claimed is the generic read path plus store, forget, timed forget, consolidate, replace and update. The claim scope and the technical centre of gravity of the disclosure are offset, which is the shape of a filing that expects continuations.
  - 근거 항목: M76, M78, M92, M101
  - 인용: “consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset”
  - 인용: “the system may manage memory object size by splitting large memory objects into smaller, distinct memory objects”
  - 인용: “A gradual memory rolloff may also provide for improved resource utilization.”
- **M133** (claim · inferred) — Claims 20 to 22 turn the memory into a consent actuator. The response is an API call; the query indicates a configuration parameter governing an operation of a computing system; that parameter is one of data access, data retention or data communication. Read against the browser pop-up scenario, the agent answers privacy prompts on the user's behalf from remembered preferences — so the same datastore that itself raises a data-retention question is claimed as the instrument that answers data-retention questions.
  - 근거 항목: M102, M103, M104, M105, M106, M108
  - 인용: “wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action”
  - 인용: “data access by the computing system”
  - 인용: “A machine-learned agent system 100 could respond to the interface features on the behalf of a user in near real-time to reduce a latency of loading the underlying content.”
- **M134** (claim · inferred) — Relevance is claimed disjunctively — an embedding-distance score or a sequence output from a second model — and claim 13 expressly allows that second model to be the same model as the generator. The retriever/generator separation is therefore not a claim limitation: an implementation that prompts one language model both to rank candidate memories and to answer the query still falls within claims 12 and 13.
  - 근거 항목: M81, M82, M83, M84, M85
  - 인용: “a respective score generated based on distance between a query embedding and a respective memory value embedding”
  - 인용: “a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model”
- **M135** (spec · inferred) — The floor of the invention is string concatenation. Claim 14 permits every memory value to be a string and the memory data to be the string of those strings; the worked example makes memory data literally a three-line bulleted list of dietary and budget preferences prepended to a prompt. Whatever is novel therefore cannot lie in how the memory is consumed — it must lie in which strings come to exist and how they are maintained over time.
  - 근거 항목: M86, M87, M80
  - 인용: “the one or more memory values each comprise a respective string, and wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values”
  - 인용: “memory data 308 can include a concatenated string of the memory values contained in the memory objects”
- **M136** (claim · inferred) — Timestamp ordering is conflict resolution relocated into the prompt. Claim 11 orders the combined memory values by the timestamps of their objects, and the description explains that the ordering alone carries the recency signal even when the timestamps themselves are not rendered. This is the read-time counterpart of the FIG. 8 write-time choice: whichever end declines to resolve the contradiction, the ordering of the list is what the model is left to arbitrate with.
  - 근거 항목: M80, M87
  - 인용: “the ordered combination ordered based on corresponding timestamps of the plurality of memory objects”
  - 인용: “This ordering allows the machine-learned agent system to prioritize more recent context when making inferences.”
- **M137** (claim · inferred) — Multimodality is claimed as a pair, not as a general capacity. Claim 2 requires the memory data to rest on one object in a first modality and a second object in a second modality, and claim 3 enumerates exactly three admissible pairs: audio with image, text with image, text with audio. Video, sensor, location and document data are all disclosed as storable memory values, and video is expressly used in the wearable-device examples, yet none of them appears in the claimed pairs. The claimed multimodal scope is narrower than the disclosed one.
  - 근거 항목: M63, M65, M66, M67
  - 인용: “the interaction memory datastore comprises multimodal data, and wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality”
  - 인용: “Interaction memory datastore 110 can be multimodal.”
  - 인용: “Video data can include a combination of image data and audio synchronized over time.”
- **M138** (spec · stated) — The specification states that storing a memory in the modality in which the interaction happened preserves signals that transcription or captioning destroys: cadence, tone, inflection and background noise on the audio side; environment, lighting, colour, mood, facial expression and body posture on the image side. This is the stated reason the store must not collapse into a text log, and the reason a multimodal model is wanted to read memories directly rather than read a description of them.
  - 근거 항목: M63, M65, M66, M67
  - 인용: “These audio recordings can capture rich contextual information that may be lost in the transcription, such as cadence, tone, inflection, background noise, etc.”
  - 인용: “The image data (e.g., video frames, still image captures) can capture rich contextual information that may be lost in captioning, such as environmental information, lighting, colors, mood, facial expressions, body posture, etc.”
  - 인용: “An example agent system can leverage a multimodal machine-learned model to process multimodal memories directly to leverage the benefits of the rich context in the native memory modality.”
- **M139** (claim · inferred) — Claims 15 and 16 recite a hidden reasoning pass as a claim element. The model output holds a plurality of predictions for analytical content analysing the query against the memory data; that output is fed back into the same model to produce the response; and the analytical content is not exposed on the user interface. Chain-of-thought over retrieved memory is thus claimed together with a non-exposure limitation, so the hiding of the intermediate reasoning is itself part of what is asserted, not an implementation detail.
  - 근거 항목: M88, M89, M90, M91
  - 인용: “wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data”
  - 인용: “The raw outputs may not be surfaced to the user.”
- **M140** (claim · inferred) — The claim set carries antecedent-basis defects that a national-phase examiner will raise. Claim 16 recites the plurality of predictions for analytical content while depending on any of the preceding claims, although that antecedent arises only in claim 15. Claims 4, 11 and 12 recite the one or more memory values and the plurality of memory objects, while claim 1 recites only one or more memory objects and never introduces memory values at all. The any-of-the-preceding-claims style is EPO-shaped drafting, and these are its ordinary casualties.
  - 근거 항목: M68, M80, M81, M91
  - 인용: “16. The method of any of the preceding claims, wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query.”
  - 인용: “retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query”
- **M141** (spec · inferred) — Vestigial context-management vocabulary survives inside the memory framing. [0054] stores information as a context value in a memory object of the context datastore; [0143] calls the invention a dynamic context datastore; [0144] speaks of context objects and structured context management. Most consequentially, summary paragraph [0018] describes the analytical content as an analysis of the query with respect to the context data where claim 15 says memory data. The disclosure was rewritten from a context framing into a memory framing and the summary was left unconformed to the claim it summarises.
  - 근거 항목: M88, M90
  - 인용: “This piece of information can be stored (e.g., as a string) as a context value in a memory object of the context datastore.”
  - 인용: “the output includes a plurality of predictions for analytical content that includes an analysis of the query with respect to the context data”
- **M142** (spec · inferred) — Recall need not be responsive to the query. The description allows the recall cycle to run offline in advance and to hold a cached snapshot of top-K memory values that is inserted into inputs generally. Claim 1 requires only that memory data be accessed, not that the access be triggered by or scoped to the query, so a system that maintains a rolling memory preamble and never performs a per-request lookup still reads on the independent claim.
  - 근거 항목: M58, M68
  - 인용: “general recall of baseline information applicable to multiple different queries can be recalled offline and cached by memory model 105 to improve latency at runtime”
  - 인용: “memory model 105 can maintain a cached memory snapshot of top-K memory values”
- **M143** (spec · inferred) — The word user is defined so broadly — account, sub-account, individual, corporation, legal entity, administrator, or another computer-implemented agent — that user-specific becomes an addressing rule rather than a privacy boundary. The description layers memories across a personal profile, a business profile and a shared account-level memory, and lets employees of a corporate user reach memory linked to the corporate account. The scoping in claim 1 therefore says where a memory is filed, not who is protected from it.
  - 근거 항목: M57, M58
  - 인용: “one user can be a corporate entity associated with a corporate account”
  - 인용: “In this manner, for instance, multiple overlapping memories can be stored and accessed as desired.”
- **M144** (claim · inferred) — The apparatus claims are deployment-agnostic boilerplate. Claims 23 to 25 are the standard media, system and computer-program-product triplet referring back to the method of any preceding claim, and the hardware disclosure behind them is generic — processor(s) 51 with memory 52 holding instructions 54 on the device side, processor(s) 61 with memory 62 holding instructions 64 on the server side. Both the datastore and the model system are expressly allowed to sit locally or remotely, so nothing in the claims requires on-device memory and the set reads equally on a wholly server-side deployment.
  - 근거 항목: M109, M110, M111, M112
  - 인용: “One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims.”
  - 인용: “Interaction memory datastore 110 can be implemented locally to machine-learned agent system 100 (e.g., on a same device or system) or remotely from machine-learned agent system 100 (e.g., on a different device or system).”
- **M145** (effects · inferred) — The asserted benefit chain runs: fewer turns, therefore fewer inputs parsed and outputs rendered, therefore lower latency and load, therefore less energy, therefore less carbon and heat pollution. The first two links are memory-specific and argued from the mechanism. The last two are generic energy-efficiency boilerplate attached at the end, tied to no memory-specific measurement, and would read identically in any filing about making inference cheaper.
  - 근거 항목: M58, M60, M68
  - 인용: “This can provide efficient use of computational resources by avoiding the processing of additional inputs and rendering of additional outputs for a given task.”
  - 인용: “increased energy efficiency can provide for less energy to be used to perform a given task”
  - 인용: “An amount of heat pollution in an environment (e.g., by the processors/storage locations) can be reduced by implementing more energy-efficient training or inference operations.”
- **M146** (effects · inferred) — There is no quantitative performance evidence anywhere in the document. Exhaustive numeric harvesting over the grounded specification spans and the bibliographic face returned only drawing reference numerals and the filing metadata — no benchmark, no latency figure, no accuracy or storage measurement, no comparison against any baseline. Every efficiency assertion is accordingly structural and argumentative: the disclosure claims that fewer interactions and pre-processed memory objects will cost less, and never says how much less.
  - 근거 항목: M58, M68, M92
  - 인용: “This can reduce latency in response to queries by reducing a complexity of an inference task.”
  - 인용: “This reduces the computational load on the machine-learned model during online inference, as the system can respond by processing concise, relevant information instead of large amounts of raw data (e.g., such as a full transcript of all prior interactions).”

## 4. 포지셔닝 (D5 ⑤)

- **M147**
  - 배경 문제: Agent systems without a memory capability make the user re-enter the same information across turns and across sessions, and must interrupt with follow-up prompts whenever a request omits a detail the user believes it has already given. The specification's own examples are a calendar entry at a dentist during a lunch break, where neither the dentist nor the lunch interval can be resolved, and a request that omits a previously stated dietary restriction.
  - 주장 효과: The specification asserts that an intelligently managed, dynamic interaction memory datastore lets the system begin execution from a single interaction where a traditional system would have to come back for details, avoiding the processing of additional inputs and the rendering of additional outputs for the task.
  - 차이: No measurement is offered on either side. The stated difference is structural: context that the compared systems must re-solicit synchronously is instead retrieved from a user-specific store assembled out of prior interactions. The saving is argued in counts of interactions, not in time, tokens or cost.
  - 인용: “Without a memory of useful context, traditional agent devices may require entry of the same information multiple times over the same or multiple sessions in order to perform the same or similar tasks.”
  - 인용: “an example machine-learned agent system, leveraging a memory according to the present disclosure, can initiate execution with a single interaction”
- **M148**
  - 배경 문제: The alternative the specification names is exposing the agent to external application programming interfaces that fetch context from third-party data sources. It argues three defects: such sources were never curated by the agent against this user's interactions, the agent cannot keep them fresh, and they bundle sensitive material with the useful material — the dietary restriction that lives inside a health or medical-communication application.
  - 주장 효과: Memory grounded in what the user gave the agent directly over a history of interactions is asserted to give improved control over stored contextual information: the user can withhold, can permit a limited purpose, and can instruct the system to forget afterwards.
  - 차이: Structural. The unit at which permission is granted moves from the data source to the individual memory object, replacing an all-or-nothing grant over a whole application with per-memory admission. No comparative figure of any kind is given, and the argument that the store stays fresher is asserted rather than demonstrated.
  - 인용: “Under traditional approaches to enabling external data sources, the user may be faced with an all-or-nothing choice, which may be undesirable in some circumstances.”
  - 인용: “The user can decline to provide information that the user does not wish to share, or the user can instruct the agent system to use the information for limited purposes and subsequently forget.”
- **M149**
  - 배경 문제: Even when an external source holds the datum, it may not be contextualised for the particular interaction. The specification's illustration is a request to call Blake where the user has both a best friend and a dentist of that name: the contact list contains the answer and still cannot select it, so the system must interrupt to ask.
  - 주장 효과: Interaction-derived memory is asserted to carry the disambiguating context a generic external source lacks, and thereby to avoid a class of interruption the specification describes in physiological terms — arrested auditory and visual attention, diverted gaze, interrupted utterance, and the switching cost of returning to the abandoned task.
  - 차이: Structural, and unusually the delta is argued in human rather than computational currency. The switching cost is called a measurable interval, but no interval is measured; it is invoked as a category of harm the memory avoids, not as a quantity the memory reduces by some amount.
  - 인용: “a user may have a best friend named Blake”
  - 인용: “a switching cost can refer to a measurable interval of time required for the human brain to switch from performing any other task to the task of responding to the follow-up event”
- **M150**
  - 배경 문제: Existing systems render configuration prompts at the moment a browser loads a web resource — typically for the data-handling parameters of an analytics system — and generally require the user to perceive and answer the prompt synchronously, at that moment, before the underlying content is usable.
  - 주장 효과: The specification asserts that preferences parsed and stored at an earlier time let the agent answer such prompts asynchronously on the user's behalf in near real time, completing the task without initiating a synchronous interaction event when the task actually arises, and reducing the latency between the triggering event and the executed response.
  - 차이: Structural, and this is the document's strongest stated delta: it claims the arrangement provides a mechanism for controlling a computing device that would not be possible without the datastore — a difference in kind rather than degree. It remains an assertion; no latency measurement accompanies it, and the sentence making the claim still uses the superseded term context datastore.
  - 인용: “Generally, existing systems require synchronous perception of and response to the prompt (e.g., inputting a configuration parameter).”
  - 인용: “In this manner, for instance, the task can be completed without initiating a synchronous interaction event at the time of the task performance.”
  - 인용: “example implementations provide a mechanism for controlling a computing device that would not be possible if the machine-learned agent system did not implement an intelligently managed, dynamic context datastore as described herein”
- **M151**
  - 배경 문제: The naive way to give a model memory is to prepend the raw history — an exhaustive record of prior interactions, a full transcript — to the query. The specification argues this is both expensive at inference time and, for a particular task, sometimes less reliable or accurate than a curated input.
  - 주장 효과: Pre-processing interactions offline into structured, high-quality memory objects holding key features and metadata is asserted to reduce the runtime computational load, to lower latency by reducing the complexity of the inference task, and to move the curation work onto a time-shifted schedule away from peak demand.
  - 차이: Structural, plus an unquantified scheduling claim. Both the accuracy assertion and the load assertion are stated without figures for either the transcript baseline or the curated alternative, so what is offered is a mechanism and a direction of effect, not a magnitude.
  - 인용: “for obtaining an inference for a particular task can sometimes be less reliable or accurate than inputting clean, curated, and condensed data for the same query”
  - 인용: “Example machine-learned agent systems can reduce a computational load at runtime through pre-processing and storage of high-quality memory data objects.”
- **M152**
  - 배경 문제: The formal BACKGROUND section recites only what a machine-learned model is — a computer receives inputs, processes them with a parameterised model, obtains feedback, updates parameters, and is said to learn. It identifies no prior memory or context-management system and cites no document at all.
  - 주장 효과: Every comparative assertion in the filing is instead made in the detailed description against a baseline the applicant characterises there: some traditional agent systems that lack a memory capability, and some possible alternative approaches that expose external data-source interfaces.
  - 차이: The delta is defined against an applicant-drawn baseline rather than against identified art. The only external literature cited anywhere in the disclosure supports the generic model machinery — transformer, mixture-of-experts, tokenisation, the applicant's own Gemma, PaliGemma and Gemini papers — and none of it is offered as prior art for the memory mechanism. An examiner's characterisation of the closest art is therefore entirely unanticipated by the document.
  - 인용: “A computer can receive input(s).”
  - 인용: “some traditional agent systems that lack a memory capability may lead to interruptions or prompts to process additional inputs and render additional outputs to perform a task”
- **M153**
  - 배경 문제: The filing does not position itself against a rival memory architecture. It positions the memory layer against its own model stack operated without one: the sequence processing model is treated throughout as a supplied component, reached through machine-learned model system(s) 118 and described generically at FIG. 12 to FIG. 17, and the surrounding platform, training and inference chapters are shared boilerplate rather than contributed matter.
  - 주장 효과: The asserted contribution is the layer around that model — generating, curating, retrieving, updating and forgetting user-specific memory objects — so as to condition an otherwise unmodified sequence processing model on what the user said before.
  - 차이: No change to model architecture, training or parameters is claimed. Claim 1 requires only that the model process an input data structure built from the query and the memory data, so the entire delta sits in what enters the prompt and in how that content is maintained between prompts. The timing supports the reading: priority 2024-12-11 from US provisional 63/730,845, PCT filing exactly one Paris year later on 2025-12-11, publication 2026-06-18 as WO2026-128750A1 — a memory-layer filing made from inside an established model programme rather than alongside a model result.
  - 인용: “Machine-learned model system(s) 118 can manage and perform execution of one or more machine-learned models based on inputs received from machine-learned agent system 100.”
  - 인용: “inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data”

## 5. 구성요소와 3중 접지 (D5 ③)

| 구성요소 | 청구항 좌표 | 라벨(EN) | 접지 |
|---|---|---|---|
| **M1** | `CL-1/e1` | receiving a query associated with a user | **M57** (명세서 found · 도면 found) |
| **M2** | `CL-1/e2` | accessing memory data from an interaction memory datastore associated with the user | **M58** (명세서 found · 도면 found) |
| **M3** | `CL-1/e2/e1` | interaction memory datastore comprising memory objects generated from prior interactions | **M59** (명세서 found · 도면 found) |
| **M4** | `CL-1/e3` | inputting an input data structure based on the query and the memory data to a sequence processing model | **M60** (명세서 found · 도면 found) |
| **M5** | `CL-1/e4` | generating an output by processing the input data structure with the sequence processing model | **M61** (명세서 found · 도면 found) |
| **M6** | `CL-1/e5` | outputting a response to the query based on the output | **M62** (명세서 found · 도면 found) |
| **M7** | `CL-2/a1` | interaction memory datastore comprising multimodal data | **M63** (명세서 found · 도면 found) |
| **M8** | `CL-2/a2` | memory data based on first and second memory objects of first and second data modalities | **M64** (명세서 found · 도면 found) |
| **M9** | `CL-3/a1` | audio first modality with image second modality | **M65** (명세서 found · 도면 found) |
| **M10** | `CL-3/a2` | text first modality with image second modality | **M66** (명세서 found · 도면 found) |
| **M11** | `CL-3/a3` | text first modality with audio second modality | **M67** (명세서 found · 도면 found) |
| **M12** | `CL-4/a1` | retrieving memory values from the datastore based on relevance to the query | **M68** (명세서 found · 도면 found) |
| **M13** | `CL-5/a1` | processing an interactive-session input with a machine-learned model to generate values | **M69** (명세서 found · 도면 found) |
| **M14** | `CL-5/a2` | condition that the generated values indicate a portion of the input is to be stored | **M70** (명세서 found · 도면 found) |
| **M15** | `CL-5/a3` | extracting the portion of the input | **M71** (명세서 found · 도면 found) |
| **M16** | `CL-5/a4` | storing the portion as a memory value in a memory object in the datastore | **M72** (명세서 found · 도면 found) |
| **M17** | `CL-6/a1` | storing metadata associated with the memory value in the memory object | **M73** (명세서 found · 도면 found) |
| **M18** | `CL-7/a1` | portion comprising text, image, or audio data | **M74** (명세서 found · 도면 found) |
| **M19** | `CL-8/a1` | portion corresponding to an explicit instruction to remember information | **M75** (명세서 found · 도면 found) |
| **M20** | `CL-9/a1` | receiving input data indicating an instruction to forget specified information | **M76** (명세서 found · 도면 found) |
| **M21** | `CL-9/a2` | deleting the specified information from the interaction memory datastore | **M77** (명세서 found · 도면 found) |
| **M22** | `CL-10/a1` | receiving an instruction to forget specified information after a specified interval | **M78** (명세서 found · 도면 found) |
| **M23** | `CL-10/a2` | queuing the specified information for deletion after the specified interval | **M79** (명세서 found · 도면 found) |
| **M24** | `CL-11/a1` | memory data as a timestamp-ordered combination of memory values | **M80** (명세서 found · 도면 found) |
| **M25** | `CL-12/a1` | filtering the memory objects to obtain the memory values | **M81** (명세서 found · 도면 found) |
| **M26** | `CL-12/a2` | computing relevance measures for the memory objects based on the query | **M82** (명세서 found · 도면 found) |
| **M27** | `CL-12/a3` | returning a subset of the memory objects based on the relevance measure | **M83** (명세서 found · 도면 found) |
| **M28** | `CL-13/a1` | relevance score from distance between query embedding and memory value embedding | **M84** (명세서 found · 도면 found) |
| **M29** | `CL-13/a2` | relevance as sequence output from a second sequence processing model | **M85** (명세서 found · 도면 found) |
| **M30** | `CL-14/a1` | each memory value comprising a respective string | **M86** (명세서 found · 도면 found) |
| **M31** | `CL-14/a2` | memory data as a string comprising the respective memory value strings | **M87** (명세서 found · 도면 found) |
| **M32** | `CL-15/a1` | inputting a portion of the output back to the sequence processing model | **M88** (명세서 found · 도면 found) |
| **M33** | `CL-15/a2` | generating the response by processing the output with the sequence processing model | **M89** (명세서 found · 도면 found) |
| **M34** | `CL-15/a3` | output comprising predictions for analytical content analyzing the query against the memory data | **M90** (명세서 found · 도면 found) |
| **M35** | `CL-16/a1` | analytical-content predictions not exposed on the user interface | **M91** (명세서 found · 도면 found) |
| **M36** | `CL-17/a1` | consolidating aligned memory objects into a single memory object | **M92** (명세서 found · 도면 found) |
| **M37** | `CL-18/a1` | receiving input data associated with a timestamp | **M93** (명세서 found · 도면 found) |
| **M38** | `CL-18/a2` | creating a current memory object | **M94** (명세서 found · 도면 found) |
| **M39** | `CL-18/a3` | the timestamp within the current memory object | **M95** (명세서 found · 도면 found) |
| **M40** | `CL-18/a4` | current memory value based on the input data | **M96** (명세서 found · 도면 found) |
| **M41** | `CL-18/a5` | matching the current memory object to a prior memory object | **M97** (명세서 found · 도면 found) |
| **M42** | `CL-18/a6` | replacing the prior memory object with the current memory object | **M98** (명세서 found · 도면 found) |
| **M43** | `CL-19/a1` | receiving timestamped input data for updating | **M99** (명세서 found · 도면 found) |
| **M44** | `CL-19/a2` | matching a portion of the input data to a prior memory object | **M100** (명세서 found · 도면 found) |
| **M45** | `CL-19/a3` | updating the prior memory object based on the portion of the input data | **M101** (명세서 found · 도면 found) |
| **M46** | `CL-20/a1` | response comprising instructions controlling an API to cause an action | **M102** (명세서 found · 도면 found) |
| **M47** | `CL-21/a1` | query indicating a configuration parameter controlling a system operation | **M103** (명세서 found · 도면 found) |
| **M48** | `CL-21/a2` | instructions causing the system to assign a value for the configuration parameter | **M104** (명세서 found · 도면 found) |
| **M49** | `CL-22/a1` | configuration parameter associated with at least one listed aspect | **M105** (명세서 found · 도면 not-depicted) |
| **M50** | `CL-22/a2` | data access by the computing system | **M106** (명세서 found · 도면 not-depicted) |
| **M51** | `CL-22/a3` | data retention by the computing system | **M107** (명세서 found · 도면 not-depicted) |
| **M52** | `CL-22/a4` | data communication by the computing system | **M108** (명세서 found · 도면 not-depicted) |
| **M53** | `CL-23/a1` | non-transitory computer-readable media storing processor-executable instructions | **M109** (명세서 found · 도면 found) |
| **M54** | `CL-24/a1` | one or more processors | **M110** (명세서 found · 도면 found) |
| **M55** | `CL-24/a2` | media storing instructions executable by the processors of the computing system | **M111** (명세서 found · 도면 found) |
| **M56** | `CL-25/a1` | computer program product comprising processor-executable instructions | **M112** (명세서 found · 도면 not-depicted) |

- **M57** ← 구성요소 M1
  - 명세서 `[0431]`: “At 2102, example method 2100 includes receiving, by a machine-learned agent system, a query associated with a user.”
  - 명세서 `[0065]`: “Input interface(s) 102 can receive inputs (e.g., from a user). Query 104 can be based on data from input interfaces 102.”
  - 도면 `FIG-1` (도면부호 100, 102, 104): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 도면 `FIG-21` (도면부호 2100, 2102): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M58** ← 구성요소 M2
  - 명세서 `[0432]`: “At 2104, example method 2100 includes accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user.”
  - 명세서 `[0066]`: “Machine-learned agent system 100 can issue a memory query 108 to interaction memory datastore 110.”
  - 명세서 `[0067]`: “Machine-learned agent system 100 can obtain memory data 114 based on memory response 112”
  - 도면 `FIG-1` (도면부호 100, 105, 106, 108, 110, 112, 114): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 도면 `FIG-21` (도면부호 2104): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M59** ← 구성요소 M3
  - 명세서 `[0432]`: “In some implementations, the interaction memory datastore includes one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user.”
  - 명세서 `[0066]`: “Interaction memory datastore 110 can contain stored contextual information catalogued and stored over prior interactions with the user.”
  - 명세서 `[0053]`: “For instance, the machine-learned agent system can process the content of an interaction with the user and selectively generate memory objects that encapsulate salient features of the interaction.”
  - 도면 `FIG-2` (도면부호 110, 202-1, 202-M, 204-1, 204-M, 206-1, 206-M): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M60** ← 구성요소 M4
  - 명세서 `[0434]`: “At 2106, example method 2100 includes inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory”
  - 명세서 `[0067]`: “Machine-learned agent system 100 can output input data structure 116 based on memory data 114.”
  - 명세서 `[0105]`: “Input data structure 116 can be or include a data object configured for input to machine-learned model system(s) 118.”
  - 도면 `FIG-1` (도면부호 100, 114, 116, 118): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 도면 `FIG-21` (도면부호 2106): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M61** ← 구성요소 M5
  - 명세서 `[0435]`: “At 2108, example method 2100 includes generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output.”
  - 명세서 `[0068]`: “Machine-learned model system 118 can process input data structure 116 to generate output data structure 120.”
  - 도면 `FIG-1` (도면부호 116, 118, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 도면 `FIG-21` (도면부호 2108): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M62** ← 구성요소 M6
  - 명세서 `[0436]`: “At 2110, example method 2100 includes outputting, by the machine-learned agent system, and based on the output, a response to the query.”
  - 명세서 `[0069]`: “Machine-learned agent system 100 can output response 122 based on output data structure 120.”
  - 명세서 `[0069]`: “Output interface(s) 124 can render, transmit, or execute data from response 122.”
  - 도면 `FIG-1` (도면부호 100, 104, 120, 122, 124): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 도면 `FIG-21` (도면부호 2110): “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M63** ← 구성요소 M7
  - 명세서 `[0100]`: “Interaction memory datastore 110 can be multimodal.”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M64** ← 구성요소 M8
  - 명세서 `[0432]`: “the memory data can be based on a first memory object associated with a first data modality and a second memory object associated with a second data modality”
  - 도면 `FIG-2` (도면부호 202-1, 202-M, 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M65** ← 구성요소 M9
  - 명세서 `[0432]`: “For example, the first data modality can include audio data, and wherein the second data modality can include image data.”
  - 명세서 `[0162]`: “interaction memory datastore 110 can store image data in association with audio data”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M66** ← 구성요소 M10
  - 명세서 `[0163]`: “interaction memory datastore 110 can store image data in association with text data”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M67** ← 구성요소 M11
  - 명세서 `[0164]`: “interaction memory datastore 110 can store audio data in association with text data”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M68** ← 구성요소 M12
  - 명세서 `[0437]`: “retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query”
  - 도면 `FIG-3` (도면부호 106, 110): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M69** ← 구성요소 M13
  - 명세서 `[0438]`: “processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values”
  - 도면 `FIG-8` (도면부호 802, 118): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M70** ← 구성요소 M14
  - 명세서 `[0439]`: “The values can indicate that at least a portion of the input is to be stored.”
  - 도면 `FIG-8` (도면부호 804, 118): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M71** ← 구성요소 M15
  - 명세서 `[0439]`: “The machine-learned agent system (e.g., 100) can extract a portion of the input (e.g., using memory model 105)”
  - 도면 `FIG-8` (도면부호 105, 804): “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M72** ← 구성요소 M16
  - 명세서 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
  - 도면 `FIG-2` (도면부호 204-1, 202-1, 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M73** ← 구성요소 M17
  - 명세서 `[0440]`: “storing, by the machine-learned agent system, metadata associated with the memory value in the memory object”
  - 도면 `FIG-2` (도면부호 206-1, 204-1, 202-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M74** ← 구성요소 M18
  - 명세서 `[0441]`: “the portion includes at least one of: text data, image data, or audio data”
  - 도면 `FIG-2` (도면부호 110, 204-1): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M75** ← 구성요소 M19
  - 명세서 `[0442]`: “the portion corresponds to an explicit instruction to remember information”
  - 도면 `FIG-4` (도면부호 402, 105): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M76** ← 구성요소 M20
  - 명세서 `[0443]`: “receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information”
  - 도면 `FIG-10` (도면부호 1002, 105): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M77** ← 구성요소 M21
  - 명세서 `[0443]`: “Memory model 105 can then cause the identified memory objects to be deleted from interaction memory datastore 110.”
  - 도면 `FIG-10` (도면부호 105, 110, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M78** ← 구성요소 M22
  - 명세서 `[0444]`: “receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval”
  - 도면 `FIG-10` (도면부호 1002, 110): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M79** ← 구성요소 M23
  - 명세서 `[0444]`: “queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval”
  - 명세서 `[0444]`: “The deletion can be performed immediately or scheduled for a later time.”
  - 도면 `FIG-10` (도면부호 110, 804): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M80** ← 구성요소 M24
  - 명세서 `[0445]`: “the memory data includes an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects”
  - 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M81** ← 구성요소 M25
  - 명세서 `[0446]`: “filtering the plurality of memory objects to obtain the one or more memory values”
  - 도면 `FIG-3` (도면부호 108, 110): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M82** ← 구성요소 M26
  - 명세서 `[0446]`: “The filtering process can involve computing one or more relevance measures (e.g., similarity scores, distance metrics, or probabilities) for each memory object”
  - 도면 `FIG-3` (도면부호 108, 106): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M83** ← 구성요소 M27
  - 명세서 `[0446]`: “The filtering process can then return a subset of the memory objects”
  - 도면 `FIG-3` (도면부호 302, 304, 306): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M84** ← 구성요소 M28
  - 명세서 `[0447]`: “the one or more relevance measures include a respective score generated based on distance between a query embedding and a respective memory value embedding”
  - 도면 `FIG-2` (도면부호 110): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M85** ← 구성요소 M29
  - 명세서 `[0447]`: “a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model”
  - 도면 `FIG-13` (도면부호 4, 6): “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”
- **M86** ← 구성요소 M30
  - 명세서 `[0448]`: “the one or more memory values each include a respective string”
  - 도면 `FIG-2` (도면부호 204-1, 204-M): “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M87** ← 구성요소 M31
  - 명세서 `[0448]`: “the memory data includes a string including the one or more respective strings from the one or more memory values”
  - 도면 `FIG-3` (도면부호 308): “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M88** ← 구성요소 M32
  - 명세서 `[0449]`: “inputting at least a portion of the output to the machine-learned sequence processing model”
  - 도면 `FIG-1` (도면부호 120, 118): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M89** ← 구성요소 M33
  - 명세서 `[0449]`: “generating, based on processing the output using the machine-learned sequence processing model, the response to the query”
  - 도면 `FIG-1` (도면부호 122, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M90** ← 구성요소 M34
  - 명세서 `[0449]`: “the output includes a plurality of predictions for analytical content that includes an analysis of the query with respect to the memory data”
  - 도면 `FIG-1` (도면부호 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M91** ← 구성요소 M35
  - 명세서 `[0450]`: “the plurality of predictions for analytical content are not exposed on a user interface associated with the query”
  - 명세서 `[0117]`: “The raw outputs may not be surfaced to the user.”
  - 도면 `FIG-1` (도면부호 124, 122): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M92** ← 구성요소 M36
  - 명세서 `[0020]`: “In some implementations, the example method includes consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset.”
  - 명세서 `[0299]`: “Memory model 105 may consolidate related memory objects, merging redundant or overlapping information to reduce storage overhead.”
  - 도면 `FIG-10` (도면부호 704, 110, 105): “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 통합(consolidation)은 FIG-10의 메모리 유지보수 사이클(704) 안에서 memory model 105 가 interaction memory datastore 110 에 대해 수행하는 동작으로 표현된다. '통합' 자체에 고유 도면부호는 없어 상위 요소 부호만 등재했다.
- **M93** ← 구성요소 M37
  - 명세서 `[0021]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
  - 도면 `FIG-5` (도면부호 500): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M94** ← 구성요소 M38
  - 명세서 `[0021]`: “In some implementations, the example method includes creating a current memory object.”
  - 명세서 `[0246]`: “Memory model 105 can interact with machine-learned model system(s) 118 to generate values for a new memory object 402 based on input 400.”
  - 도면 `FIG-4` (도면부호 402, 400, 105): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M95** ← 구성요소 M39
  - 명세서 `[0021]`: “In some implementations, the current memory object includes the timestamp.”
  - 명세서 `[0256]`: “Memory model 105 can cause memory object 402 to store time data associated with the memory.”
  - 도면 `FIG-4` (도면부호 402): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 타임스탬프는 메모리 객체 402 내부의 필드(created/lastUpdated)로 표현될 뿐 고유 도면부호를 갖지 않아, 이를 포함하는 객체 부호 402 만 등재했다.
- **M96** ← 구성요소 M40
  - 명세서 `[0021]`: “In some implementations, the current memory object includes a current memory value based on the input data.”
  - 명세서 `[0246]`: “For example, memory model 105 can use machine-learned model system(s) 118 to predict a memory value “prefers vegetarian” based on the input.”
  - 도면 `FIG-4` (도면부호 402, 400): “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 메모리 값(memory value)은 FIG-4 에서 객체 402 내부 값으로 표현되며 별도 도면부호가 없다. FIG-2 의 204-1…204-M 이 일반형 부호이나, 본 종속항의 '현재 메모리 값'에 직접 조응하는 것은 FIG-4 의 402 이므로 402·400 만 등재했다.
- **M97** ← 구성요소 M41
  - 명세서 `[0021]`: “In some implementations, the example method includes matching the current memory object to a prior memory object.”
  - 명세서 `[0089]`: “Memory model 105 can query interaction memory datastore 110 to retrieve relevant entries for new information and update the relevant entries based on the new information.”
  - 도면 `FIG-5` (도면부호 500, 402): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 매칭 동작 자체에는 도면부호가 없다. FIG-5 에서 신규 입력 500 이 선행 메모리 객체 402 에 대응되는 관계로 표현되므로 두 부호를 등재했다.
- **M98** ← 구성요소 M42
  - 명세서 `[0021]`: “In some implementations, the example method includes replacing, in the interaction memory datastore, the prior memory object with the current memory object.”
  - 명세서 `[0263]`: “The updated memory object 502 can be stored in interaction memory datastore 110.”
  - 도면 `FIG-5` (도면부호 502, 402, 110): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M99** ← 구성요소 M43
  - 명세서 `[0022]`: “In some implementations, the example method includes receiving input data associated with a timestamp.”
  - 명세서 `[0453]`: “For example, at 2108, the machine-learned agent system (e.g., 100) receives input data (e.g., 500 in Figure 5) associated with a timestamp.”
  - 도면 `FIG-5` (도면부호 500): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M100** ← 구성요소 M44
  - 명세서 `[0022]`: “In some implementations, the example method includes matching at least a portion of the input data to a prior memory object.”
  - 명세서 `[0453]`: “The system then matches at least a portion of the input data to a prior memory object (e.g., 402 in Figure 4).”
  - 도면 `FIG-5` (도면부호 500, 402): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 매칭 동작 자체에는 도면부호가 없어, 입력 500 과 선행 메모리 객체 402 의 부호를 등재했다.
- **M101** ← 구성요소 M45
  - 명세서 `[0022]`: “In some implementations, the example method includes updating, in the interaction memory datastore, the prior memory object based on the portion of the input data.”
  - 명세서 `[0453]`: “Based on this match, the system updates (e.g., as in Figure 5), in the interaction memory datastore (e.g., 110), the prior memory object (e.g., 402) based on the portion of the input data (e.g., 500).”
  - 도면 `FIG-5` (도면부호 502, 402, 110): “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M102** ← 구성요소 M46
  - 명세서 `[0023]`: “In some implementations of the example method, the response includes instructions configured to control an application programming interface to cause a computing system to perform an action.”
  - 명세서 `[0120]`: “For instance, response 122 can include an application programming interface call generated based on output data structure 120.”
  - 도면 `FIG-1` (도면부호 122, 124, 120): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M103** ← 구성요소 M47
  - 명세서 `[0024]`: “the query indicates a configuration parameter that controls an operation of the computing system”
  - 명세서 `[0455]`: “For example, the query (e.g , 104) might indicate a configuration parameter that controls an operation of the computing system.”
  - 도면 `FIG-1` (도면부호 104, 102): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 탐색 기록: 구성 파라미터 자체에는 도면부호가 없다. 그것을 지시하는 질의 104(및 입력 인터페이스 102)의 부호를 등재했다.
- **M104** ← 구성요소 M48
  - 명세서 `[0024]`: “the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter”
  - 명세서 `[0455]`: “The system then generates an output (e.g., 120) that includes instructions (e.g., in response 122) configured to control an API call (e.g., via output interface 124) to cause the computing system to assign a value for the configuration parameter.”
  - 도면 `FIG-1` (도면부호 120, 122, 124): “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
- **M105** ← 구성요소 M49
  - 명세서 `[0456]`: “In some implementations of example method 2100, the configuration parameter is associated with at least one of: data access by the computing system, data retention by the computing system, or data communication by the computing system.”
  - 탐색 기록: FIG-1(100·104·110·118·122·124)과 FIG-18~FIG-21 캡션 및 부호를 확인했으나, 구성 파라미터의 연관 대상(데이터 접근·보유·통신)을 표시한 도면부호는 없다. 명세서 [0025]·[0132]~[0135]·[0456] 본문에만 서술된다.
- **M106** ← 구성요소 M50
  - 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data access by the computing system.”
  - 명세서 `[0456]`: “For example, the configuration parameter (e.g., a setting within an analytics system for a web-based resource) might relate to data access permissions.”
  - 탐색 기록: FIG-1 및 FIG-18~FIG-21 의 부호를 확인했으나 '데이터 접근' 구성 파라미터를 지시하는 도면부호는 존재하지 않는다.
- **M107** ← 구성요소 M51
  - 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data retention by the computing system.”
  - 명세서 `[0295]`: “The system may provide users with configurable parameters to control the time-based forgetting mechanism, allowing them to customize the system's memory retention policies.”
  - 탐색 기록: FIG-1·FIG-10(704·1002·904·804) 등 유지보수 사이클 도면을 확인했으나 '데이터 보유' 구성 파라미터에 부여된 도면부호는 없다.
- **M108** ← 구성요소 M52
  - 명세서 `[0025]`: “In some implementations of the example method, the configuration parameter is associated with data communication by the computing system.”
  - 탐색 기록: FIG-1(124)·FIG-18(49) 등 통신 관련 부호를 확인했으나, 이들은 인터페이스·네트워크 자체의 부호이며 '데이터 통신' 구성 파라미터에 조응하는 도면부호는 없다.
- **M109** ← 구성요소 M53
  - 명세서 `[0026]`: “In an aspect, the present disclosure provides an example one or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
  - 명세서 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
  - 도면 `FIG-18` (도면부호 52, 54, 62, 64): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”
- **M110** ← 구성요소 M54
  - 명세서 `[0027]`: “In some implementations, the example computing system includes one or more processors.”
  - 명세서 `[0415]`: “Computing device 50 can include one or more processors 51 and a memory 52.”
  - 도면 `FIG-18` (도면부호 51, 61): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”
- **M111** ← 구성요소 M55
  - 명세서 `[0027]`: “In some implementations, the example computing system includes one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising any implementation of the example method.”
  - 명세서 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
  - 도면 `FIG-18` (도면부호 52, 54, 62, 64): “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”
- **M112** ← 구성요소 M56
  - 명세서 `[0028]`: “In an aspect, the present disclosure provides an computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method.”
  - 탐색 기록: FIG-18~FIG-20 의 컴퓨팅 장치 부호(50·51·52·53·54·60~65·98·99)와 전 도면 캡션을 확인했으나, '컴퓨터 프로그램 제품'이라는 청구 범주에 조응하는 도면부호는 없다. 해당 aspect 는 [0028] 본문에만 기재된다.

## 6. 수치 사실 — 3분류 (재정 N9)

기계가 **무엇을 보증했는가**가 갈래마다 다르다. 갈래를 섞어 보면 승인은 형식이 된다.

### 6.1 원문 스팬 수치 (`quoted` · `bibliographic`)

- 원문 스팬 수치: **11건** — M113, M114, M115, M116, M117, M118, M119, M120, M121, M122, M123
- 서지 복사: M120, M121, M122, M123 (`patent` 블록에서 결정론 복사)

- **M113** — numeric value at [0439] · `204-1` → `204-1`
  - 원천 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
- **M114** — numeric value at [0439] · `202-1` → `202-1`
  - 원천 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
- **M115** — numeric value at [0415] · `53` → `53`
  - 원천 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
- **M116** — numeric value at [0415] · `50` → `50`
  - 원천 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
- **M117** — numeric value at [0415] · `50` → `50`
  - 원천 `[0415]`: “Computing device 50 can include one or more processors 51 and a memory 52.”
- **M118** — numeric value at [0418] · `63` → `63`
  - 원천 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
- **M119** — numeric value at [0418] · `60` → `60`
  - 원천 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
- **M120** — bibliographic field patent.number · `WO2026-128750A1` → `WO2026-128750A1`
  - 원천 ``: “”
- **M121** — bibliographic field patent.dates.priority · `2024-12-11` → `2024-12-11`
  - 원천 ``: “”
- **M122** — bibliographic field patent.dates.filing · `2025-12-11` → `2025-12-11`
  - 원천 ``: “”
- **M123** — bibliographic field patent.dates.publication · `2026-06-18` → `2026-06-18`
  - 원천 ``: “”

### 6.2 파생 수치 (`derived`) — 산식과 원천 스팬을 나란히

_파생 수치 없음. 승인 봉투의 `derived_fact_ack` 는 빈 배열로 적는다._


### 6.3 도면 유래 수치 (`figure-sourced`) — 기계 검증 불가

- **M124** — memory objects returned by the interaction memory datastore in the single recall cycle worked through in FIG. 3 (302, 304, 306) · `3` → `3`
  - 도면 `FIG-3` · `machine_verifiable: false` — **기계 검증 불가**
- **M125** — operation blocks in the method flow chart of FIG. 21 (2102 receiving the query, 2104 accessing memory data, 2106 inputting the input data structure, 2108 generating the output, 2110 outputting the response) · `5` → `5`
  - 도면 `FIG-21` · `machine_verifiable: false` — **기계 검증 불가**
- **M126** — constituent slots drawn inside each memory object in FIG. 2 (memory value(s) 204-x and memory metadata 206-x), against the larger attribute set the description gives a memory object · `2` → `2`
  - 도면 `FIG-2` · `machine_verifiable: false` — **기계 검증 불가**

## 7. ★ 사람 검증 필요 목록 (재정 R1)

도면에서 읽은 값은 기계가 대조할 원문 스팬이 없다. **검사가 통과시켰다는 사실이 값이**
**옳다는 뜻이 아니다.** 아래 목록은 봉투의 `manual_verification_ack[]` 와 정확히 일치해야 한다.

- **M124** — memory objects returned by the interaction memory datastore in the single recall cycle worked through in FIG. 3 (302, 304, 306) · 값 `3` · 도면 `FIG-3` (도면부호 302, 304, 306) · 사유 `figure-sourced`
- **M125** — operation blocks in the method flow chart of FIG. 21 (2102 receiving the query, 2104 accessing memory data, 2106 inputting the input data structure, 2108 generating the output, 2110 outputting the response) · 값 `5` · 도면 `FIG-21` (도면부호 2102, 2104, 2106, 2108, 2110) · 사유 `figure-sourced`
- **M126** — constituent slots drawn inside each memory object in FIG. 2 (memory value(s) 204-x and memory metadata 206-x), against the larger attribute set the description gives a memory object · 값 `2` · 도면 `FIG-2` (도면부호 202-1, 204-1, 206-1) · 사유 `figure-sourced`

## 8. ★ 접지 예외 (재정 R3)

접지 전량이 원칙이므로 예외는 날조하거나 숨기지 않고 드러낸다. **예외가 많으면 그것이**
**소재 신호다.**

- **M105** (구성요소 M49) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: FIG-1(100·104·110·118·122·124)과 FIG-18~FIG-21 캡션 및 부호를 확인했으나, 구성 파라미터의 연관 대상(데이터 접근·보유·통신)을 표시한 도면부호는 없다. 명세서 [0025]·[0132]~[0135]·[0456] 본문에만 서술된다.
- **M106** (구성요소 M50) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: FIG-1 및 FIG-18~FIG-21 의 부호를 확인했으나 '데이터 접근' 구성 파라미터를 지시하는 도면부호는 존재하지 않는다.
- **M107** (구성요소 M51) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: FIG-1·FIG-10(704·1002·904·804) 등 유지보수 사이클 도면을 확인했으나 '데이터 보유' 구성 파라미터에 부여된 도면부호는 없다.
- **M108** (구성요소 M52) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: FIG-1(124)·FIG-18(49) 등 통신 관련 부호를 확인했으나, 이들은 인터페이스·네트워크 자체의 부호이며 '데이터 통신' 구성 파라미터에 조응하는 도면부호는 없다.
- **M112** (구성요소 M56) — 명세서 `found` · 도면 `not-depicted`
  - 탐색 기록: FIG-18~FIG-20 의 컴퓨팅 장치 부호(50·51·52·53·54·60~65·98·99)와 전 도면 캡션을 확인했으나, '컴퓨터 프로그램 제품'이라는 청구 범주에 조응하는 도면부호는 없다. 해당 aspect 는 [0028] 본문에만 기재된다.

## 9. drop 신호 (D4 — 최종)

- 단계: `final` · 판정: `go`
- 사유: 안도감 적합. 이 문서는 서사가 설 자리를 셋 갖는다. ① 독립항 CL-1 이 읽기 경로만 덮고 쓰기·망각·통합이 전부 종속항과 명세서로 흩어져 있어 '무엇을 주장했고 무엇을 주장하지 않았는가'의 대비가 선명하다 — 점진적 망각/권한 계층, 지지 기록, 지식그래프 간선, 객체 분할이 청구항에 없다는 사실이 그 자체로 기사 한 절이 된다. ② FIG-8/9/10 이 충돌 해소를 쓰기 시점에 둘지 읽기 시점에 둘지를 삼분한 채 명세서가 판정을 유보하므로, 설계 선택을 그대로 서술할 수 있다. ③ 청구항 20~22 가 기억을 '동의 응답기'로 전환하는 대목은 기억 저장소가 스스로 야기하는 프라이버시 문제를 같은 저장소로 답하게 하는 구조라 논평 여지가 크다. 접지 측 도면 10건이 전부 해소되고 실시례(채식→페스카테리안, 건축가, 쿠키 팝업)가 구체적이어서 인용 재료도 충분하다. 성능 수치가 전무한 것(수확 결과가 도면부호와 서지뿐)은 약점이지만, 이 건의 델타는 애초에 구조적 델타이므로 수치 부재를 그대로 적시하면 되고 그것이 기사를 무르게 하지 않는다.

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
| `read-a` | `clear` | 권리 관심이 '사용자별 상호작용 기억 저장소'라는 한 구성에 뚜렷하게 모여 있고, 그 위에 기억하기(명시적 기억 지시)·잊기(즉시 삭제와 지정 시간 뒤 예약 삭제)·기억의 통합과 갱신·관련성 기반 회수·데이터 접근/보존/통신 설정값 제어가 층층이 쌓인다. 대화형 AI가 '나를 기억하지 못한다'와 '너무 많이 기억한다'는 두 불만은 일반 독자가 이미 체감하는 문제이고, 청구항이 그 둘을 같은 저장소의 쓰기·삭제 규칙으로 함께 다루므로 '아, 그래서 이렇게 되는구나'의 안도감을 줄 서사가 설 것으로 본다. |
| `read-b` | `clear` | 권리 관심이 '사용자별 상호작용 기억 저장소'라는 한 구성에 뚜렷하게 걸려 있고, 그 구성을 둘러싼 종속항들이 일반 독자의 일상 경험과 그대로 겹친다 — 기억해 달라는 명시 지시(CL-8)·잊어 달라는 지시와 즉시 삭제(CL-9)·일정 시간 뒤 삭제 예약(CL-10)·중복 기억의 통합과 갱신(CL-17~19)·텍스트/이미지/음성이 뒤섞인 다중모달 기억(CL-2·3)이 청구항 문언 층위에서 이미 서사 단위로 읽힌다. 게다가 CL-20~22가 응답이 API를 통해 데이터 접근·보존·통신 설정값을 배정하도록 나아가, '에이전트가 나를 기억한다'와 '그 기억을 내가 통제한다'가 한 권리 안에 붙어 있다 — 서사의 갈등축과 해소축이 원천 안에 함께 있어 '아, 그렇구나'가 설 자리가 넉넉하다. |

두 관찰의 방향이 `clear` 로 일치했다.

## 12. ★ 수치 인벤토리 — 전수 수확 (재정 P-B)

수치는 접지 스팬과 서지면에서 **전수 기계 수확**되었고, 중요분은 LLM 의 중요도
판단이 아니라 함의·포지셔닝이 실제로 참조했는가(`numeric_refs`)로 **역참조 도출**된다.

**수확 정답지 11건(kind fact · origin ∈ {quoted, bibliographic} · status active) — 참조 11건 표시, 미참조 0건 접힘**

_카운트를 상시 표기하는 이유: 카운트가 없으면 미참조분 접힘이 은폐가 된다._

역참조 총 11건 중 **0건이 이 정답지 밖**이다. 정답지 밖 참조는 수확기 소유가 아닌 수치(`derived`·`figure-sourced`)이거나
철회·대체된 항목이며, 위 계수에 들지 않는다.

### 12.1 참조된 수치 (함의·포지셔닝의 근거)

- **M113** — numeric value at [0439] · `204-1` → `204-1`
  - 원천 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
  - 이 수치를 참조한 항목: M128, M146
- **M114** — numeric value at [0439] · `202-1` → `202-1`
  - 원천 `[0439]`: “The extracted portion is then stored as a memory value (e.g., 204-1 in Figure 2) in a memory object (e.g., 202-1 in Figure 2) in the interaction memory datastore (e.g., 110).”
  - 이 수치를 참조한 항목: M128, M146
- **M115** — numeric value at [0415] · `53` → `53`
  - 원천 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
  - 이 수치를 참조한 항목: M144, M146
- **M116** — numeric value at [0415] · `50` → `50`
  - 원천 `[0415]`: “Memory 52 can store data 53 and instructions 54 which can be executed by processor(s) 51 to cause computing device 50 to perform operations.”
  - 이 수치를 참조한 항목: M144, M146
- **M117** — numeric value at [0415] · `50` → `50`
  - 원천 `[0415]`: “Computing device 50 can include one or more processors 51 and a memory 52.”
  - 이 수치를 참조한 항목: M144, M146
- **M118** — numeric value at [0418] · `63` → `63`
  - 원천 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
  - 이 수치를 참조한 항목: M144, M146
- **M119** — numeric value at [0418] · `60` → `60`
  - 원천 `[0418]`: “Memory 62 can store data 63 and instructions 64 which can be executed by processor(s) 61 to cause server computing system(s) 60 to perform operations.”
  - 이 수치를 참조한 항목: M144, M146
- **M120** — bibliographic field patent.number · `WO2026-128750A1` → `WO2026-128750A1`
  - 이 수치를 참조한 항목: M146, M153
- **M121** — bibliographic field patent.dates.priority · `2024-12-11` → `2024-12-11`
  - 이 수치를 참조한 항목: M146, M153
- **M122** — bibliographic field patent.dates.filing · `2025-12-11` → `2025-12-11`
  - 이 수치를 참조한 항목: M146, M153
- **M123** — bibliographic field patent.dates.publication · `2026-06-18` → `2026-06-18`
  - 이 수치를 참조한 항목: M146, M153

### 12.2 미참조 수치 0건 (접힘 — 숨김이 아니다)

<details>
<summary>미참조 0건 펼치기</summary>

_미참조 수치 없음 — 수확분 전량이 함의·포지셔닝의 근거로 쓰였다._


</details>

★ 미참조 수치를 본문이 처음 인용하면 CP2 에 **"미검토 수치 사용" 플래그**가 자동
첨부된다(재정 P-B). 무검토 게시 경로는 없다 — 모든 수치는 CP1 검토 또는 사용 시 검토다.

### 12.3 수확하지 못한 토큰 82건 (숨기지 않고 센다)

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
| `figure-numeral` | 77 |
| `figure-or-table-number` | 5 |

<details>
<summary>전건 82건 펼치기</summary>

| 위치 | 토큰 | 사유 |
|---|---|---|
| `[0431]` | `2102` | figure-numeral |
| `[0431]` | `2100` | figure-numeral |
| `[0065]` | `102` | figure-numeral |
| `[0065]` | `104` | figure-numeral |
| `[0065]` | `102` | figure-numeral |
| `[0432]` | `2104` | figure-numeral |
| `[0432]` | `2100` | figure-numeral |
| `[0066]` | `100` | figure-numeral |
| `[0066]` | `108` | figure-numeral |
| `[0066]` | `110` | figure-numeral |
| `[0067]` | `100` | figure-numeral |
| `[0067]` | `114` | figure-numeral |
| `[0067]` | `112` | figure-numeral |
| `[0066]` | `110` | figure-numeral |
| `[0434]` | `2106` | figure-numeral |
| `[0434]` | `2100` | figure-numeral |
| `[0067]` | `100` | figure-numeral |
| `[0067]` | `116` | figure-numeral |
| `[0067]` | `114` | figure-numeral |
| `[0105]` | `116` | figure-numeral |
| `[0105]` | `118` | figure-numeral |
| `[0435]` | `2108` | figure-numeral |
| `[0435]` | `2100` | figure-numeral |
| `[0068]` | `118` | figure-numeral |
| `[0068]` | `116` | figure-numeral |
| `[0068]` | `120` | figure-numeral |
| `[0436]` | `2110` | figure-numeral |
| `[0436]` | `2100` | figure-numeral |
| `[0069]` | `100` | figure-numeral |
| `[0069]` | `122` | figure-numeral |
| `[0069]` | `120` | figure-numeral |
| `[0069]` | `124` | figure-numeral |
| `[0069]` | `122` | figure-numeral |
| `[0100]` | `110` | figure-numeral |
| `[0162]` | `110` | figure-numeral |
| `[0163]` | `110` | figure-numeral |
| `[0164]` | `110` | figure-numeral |
| `[0439]` | `100` | figure-numeral |
| `[0439]` | `105` | figure-numeral |
| `[0439]` | `110` | figure-numeral |
| `[0443]` | `105` | figure-numeral |
| `[0443]` | `110` | figure-numeral |
| `[0299]` | `105` | figure-numeral |
| `[0246]` | `105` | figure-numeral |
| `[0246]` | `118` | figure-numeral |
| `[0246]` | `402` | figure-numeral |
| `[0246]` | `400` | figure-numeral |
| `[0256]` | `105` | figure-numeral |
| `[0256]` | `402` | figure-numeral |
| `[0246]` | `105` | figure-numeral |
| `[0246]` | `118` | figure-numeral |
| `[0089]` | `105` | figure-numeral |
| `[0089]` | `110` | figure-numeral |
| `[0263]` | `502` | figure-numeral |
| `[0263]` | `110` | figure-numeral |
| `[0453]` | `2108` | figure-numeral |
| `[0453]` | `100` | figure-numeral |
| `[0453]` | `500` | figure-numeral |
| `[0453]` | `402` | figure-numeral |
| `[0453]` | `110` | figure-numeral |
| `[0453]` | `402` | figure-numeral |
| `[0453]` | `500` | figure-numeral |
| `[0120]` | `122` | figure-numeral |
| `[0120]` | `120` | figure-numeral |
| `[0455]` | `104` | figure-numeral |
| `[0455]` | `120` | figure-numeral |
| `[0455]` | `122` | figure-numeral |
| `[0455]` | `124` | figure-numeral |
| `[0456]` | `2100` | figure-numeral |
| `[0415]` | `52` | figure-numeral |
| `[0415]` | `54` | figure-numeral |
| `[0415]` | `51` | figure-numeral |
| `[0415]` | `51` | figure-numeral |
| `[0415]` | `52` | figure-numeral |
| `[0418]` | `62` | figure-numeral |
| `[0418]` | `64` | figure-numeral |
| `[0418]` | `61` | figure-numeral |
| `[0439]` | `Figure 2` | figure-or-table-number |
| `[0439]` | `Figure 2` | figure-or-table-number |
| `[0453]` | `Figure 5` | figure-or-table-number |
| `[0453]` | `Figure 4` | figure-or-table-number |
| `[0453]` | `Figure 5` | figure-or-table-number |

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
| `tree-edges` | `escalation-trigger` | 0.0909 | 0.95 | `escalate` |
| `dependent-count` | `exact-match` | - | - | `pass` |
| `dependent-set` | `exact-match` | 1.0000 | 1.0 | `pass` |
| `addition-attachment` | `measure-only` | 0.6724 | - | `measured` |

### 13.1 상신 축 — Owner 판단 대상

- `tree-edges` — 실측 0.09090909090909091 < 임계 0.95

### 13.2 갈린 항목

- `tree-edges`
  - 정본에만: A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interacti …
  - 정본에만: A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interacti …
  - 정본에만: A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interacti …
  - 정본에만: A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interacti …
  - 정본에만: A computer-implemented method, comprising:

receiving, by a machine-learned agent system, a query associated with a user;

accessing, by the machine-learned agent system, memory data from an interacti …
  - 비교본에만: A computer-implemented method, comprising: | accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user
  - 비교본에만: A computer-implemented method, comprising: | generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an ou …
  - 비교본에만: A computer-implemented method, comprising: | inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memor …
  - 비교본에만: A computer-implemented method, comprising: | outputting, by the machine-learned agent system, and based on the output, a response to the query
  - 비교본에만: A computer-implemented method, comprising: | receiving, by a machine-learned agent system, a query associated with a user
- `addition-attachment`
  - 정본에만: a respective score generated based on distance between a query embedding and a respective memory value embedding | accessing, by the machine-learned agent system, memory data from an interaction memor …
  - 정본에만: a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or diffe …
  - 정본에만: based on the generated one or more values indicating that at least a portion of the input is to be stored: | wherein the interaction memory datastore comprises one or more memory objects that were gen …
  - 정본에만: computing one or more relevance measures for the plurality of memory objects based on the query | accessing, by the machine-learned agent system, memory data from an interaction memory datastore assoc …
  - 정본에만: creating a current memory object comprising: | wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the mac …
  - 정본에만: filtering the plurality of memory objects to obtain the one or more memory values | accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the …
  - 정본에만: generating, based on processing the output using the machine-learned sequence processing model, the response to the query | outputting, by the machine-learned agent system, and based on the output, a  …
  - 정본에만: returning a subset of the plurality of memory objects based on the relevance measure | accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with  …
  - 정본에만: wherein the configuration parameter is associated with at least one of: | receiving, by a machine-learned agent system, a query associated with a user
  - 정본에만: wherein the one or more memory values each comprise a respective string | accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user
  - 비교본에만: a respective score generated based on distance between a query embedding and a respective memory value embedding | wherein the interaction memory datastore comprises one or more memory objects that we …
  - 비교본에만: a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or diffe …
  - 비교본에만: based on the generated one or more values indicating that at least a portion of the input is to be stored | wherein the interaction memory datastore comprises one or more memory objects that were gene …
  - 비교본에만: computing one or more relevance measures for the plurality of memory objects based on the query | wherein the interaction memory datastore comprises one or more memory objects that were generated base …
  - 비교본에만: creating a current memory object comprising | wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the mach …
  - 비교본에만: filtering the plurality of memory objects to obtain the one or more memory values | wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or mo …
  - 비교본에만: generating, based on processing the output using the machine-learned sequence processing model, the response to the query | generating, by the machine-learned agent system and based on processing the  …
  - 비교본에만: returning a subset of the plurality of memory objects based on the relevance measure | wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or …
  - 비교본에만: wherein the one or more memory values each comprise a respective string | wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior i …

## 14. 도면

- `FIG-1` — “Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-01.png` · 도면부호 100, 102, 104, 105, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124
- `FIG-2` — “Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-02.png` · 도면부호 110, 202-1, 202-M, 204-1, 204-M, 206-1, 206-M
- `FIG-3` — “Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-03.png` · 도면부호 105, 106, 108, 110, 300, 302, 304, 306, 308
- `FIG-4` — “Figure 4 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-04.png` · 도면부호 105, 118, 400, 402
- `FIG-5` — “Figure 5 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-05.png` · 도면부호 105, 110, 118, 402, 500, 502
- `FIG-8` — “Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-08.png` · 도면부호 100, 105, 110, 118, 704, 802, 804, 806
- `FIG-10` — “Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-10.png` · 도면부호 100, 105, 110, 118, 704, 804, 904, 1002
- `FIG-13` — “Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-13.png` · 도면부호 2, 3, 4, 5, 6, 7
- `FIG-18` — “Figure 18 is a block diagram of an example networked computing system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-18.png` · 도면부호 51, 52, 54, 61, 62, 64
- `FIG-21` — “Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.”
  - 원본 `00-source/figures-raw/fig-21.png` · 도면부호 2100, 2102, 2104, 2106, 2108, 2110
- **M154** (FIG-1) — The whole data path of machine-learned agent system 100 in one line. Input interface(s) 102 yield query 104; memory model 105 runs recall cycle 106, issuing memory query 108 to interaction memory datastore 110 and taking back memory response 112, from which memory data 114 is composed; memory data 114 is packed into input data structure 116 and handed to machine-learned model system(s) 118, which returns output data structure 120; response 122 is derived from that and emitted through output interface(s) 124. The five steps of independent claim CL-1 are read off this path. · 도면부호 100, 102, 104, 105, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124
- **M155** (FIG-2) — The interior of interaction memory datastore 110: memory objects 202-1 through 202-M, each holding one or more memory values 204-1 through 204-M together with respective memory metadata 206-1 through 206-M. Only these two slots per object are drawn, so the support record and the inter-object graph edges that the description relies on for reconciliation and updating are not depicted here. · 도면부호 110, 202-1, 202-M, 204-1, 204-M, 206-1, 206-M
- **M156** (FIG-3) — One recall cycle 106 worked through end to end. Memory model 105 queries interaction memory datastore 110 with input 300 and receives three memory objects 302, 304 and 306 — a budget preference, a vegetarian diet and a low-sodium diet, each carrying tags, creation and update dates, a confidence value and a support list. Memory data 308 is what survives the reduction: a three-line concatenation of the memory values alone, with all metadata dropped. · 도면부호 105, 106, 108, 110, 300, 302, 304, 306, 308
- **M157** (FIG-4) — Creation of a new memory object 402 out of input 400. Memory model 105 calls machine-learned model system(s) 118 to predict a memory value from the input, tags for later retrieval, a support object holding the original content and its timestamp, and a confidence value — set low in the worked example precisely because a single supporting interaction stands behind the inference. · 도면부호 105, 118, 400, 402
- **M158** (FIG-5) — Revision of memory object 402 into updated memory object 502 on a later input 500. The prior support record and the new statement are given to a machine-learned model together, and what comes back is a firmer memory value, a raised confidence value and an extended support record; the updated object is written back into interaction memory datastore 110. This is the update path of claim 19, as against the replacement path of claim 18. · 도면부호 105, 110, 118, 402, 500, 502
- **M159** (FIG-8) — A memory update cycle 704 that writes without first reading the store. Cached input(s) 802 go to machine-learned model system(s) 118 for a judgement about what is worth remembering; memory data update(s) 804 come back; memory model 105 parses them and executes memory data write 806 into interaction memory datastore 110. Nothing already stored is consulted, so every contradiction is left for query time to settle. · 도면부호 100, 105, 110, 118, 704, 802, 804, 806
- **M160** (FIG-10) — The maintenance variant of memory update cycle 704, running on no new user input at all. Memory model 105 sends memory update request(s) 1002 together with current memory data 904 read out of interaction memory datastore 110, so that machine-learned model system(s) 118 can return memory data update(s) 804 that prune, consolidate, split or progressively degrade what is already stored. · 도면부호 100, 105, 110, 118, 704, 804, 904, 1002
- **M161** (FIG-13) — The generic sequence processing model 4 that the agent system treats as a supplied part. Input(s) 2 are tokenised and embedded into input sequence 5, prediction layer(s) 6 emit output sequence 7, and output(s) 3 are formed from it. This is both the model that consumes input data structure 116 and the model that claim 13 allows to double as the second sequence processing model scoring memory relevance. · 도면부호 2, 3, 4, 5, 6, 7
- **M162** (FIG-18) — The generic networked deployment behind the apparatus claims: a client-side computing device with processor(s) 51 and memory 52 storing instructions 54, and a server computing system with processor(s) 61 and memory 62 storing instructions 64, joined over a network alongside a model development platform system and third-party systems. Either side can host the agent system, the interaction memory datastore and the model system, which is why the claims impose no locality. · 도면부호 51, 52, 54, 61, 62, 64
- **M163** (FIG-21) — The flow chart of method 2100, whose five blocks map one to one onto the five steps of independent claim CL-1: receiving the query at 2102, accessing memory data from the interaction memory datastore at 2104, inputting the input data structure at 2106, generating the output at 2108, and outputting the response at 2110. No writing, forgetting or maintenance step appears in this flow. · 도면부호 2100, 2102, 2104, 2106, 2108, 2110

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
| **M52** | 구성요소 | active | - |
| **M53** | 구성요소 | active | - |
| **M54** | 구성요소 | active | - |
| **M55** | 구성요소 | active | - |
| **M56** | 구성요소 | active | - |
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
| **M103** | 3중 접지 | active | - |
| **M104** | 3중 접지 | active | - |
| **M105** | 3중 접지 | active | - |
| **M106** | 3중 접지 | active | - |
| **M107** | 3중 접지 | active | - |
| **M108** | 3중 접지 | active | - |
| **M109** | 3중 접지 | active | - |
| **M110** | 3중 접지 | active | - |
| **M111** | 3중 접지 | active | - |
| **M112** | 3중 접지 | active | - |
| **M113** | 수치 사실 | active | - |
| **M114** | 수치 사실 | active | - |
| **M115** | 수치 사실 | active | - |
| **M116** | 수치 사실 | active | - |
| **M117** | 수치 사실 | active | - |
| **M118** | 수치 사실 | active | - |
| **M119** | 수치 사실 | active | - |
| **M120** | 수치 사실 | active | - |
| **M121** | 수치 사실 | active | - |
| **M122** | 수치 사실 | active | - |
| **M123** | 수치 사실 | active | - |
| **M124** | 수치 사실 | active | - |
| **M125** | 수치 사실 | active | - |
| **M126** | 수치 사실 | active | - |
| **M127** | 기술적 함의 | active | - |
| **M128** | 기술적 함의 | active | - |
| **M129** | 기술적 함의 | active | - |
| **M130** | 기술적 함의 | active | - |
| **M131** | 기술적 함의 | active | - |
| **M132** | 기술적 함의 | active | - |
| **M133** | 기술적 함의 | active | - |
| **M134** | 기술적 함의 | active | - |
| **M135** | 기술적 함의 | active | - |
| **M136** | 기술적 함의 | active | - |
| **M137** | 기술적 함의 | active | - |
| **M138** | 기술적 함의 | active | - |
| **M139** | 기술적 함의 | active | - |
| **M140** | 기술적 함의 | active | - |
| **M141** | 기술적 함의 | active | - |
| **M142** | 기술적 함의 | active | - |
| **M143** | 기술적 함의 | active | - |
| **M144** | 기술적 함의 | active | - |
| **M145** | 기술적 함의 | active | - |
| **M146** | 기술적 함의 | active | - |
| **M147** | 포지셔닝 | active | - |
| **M148** | 포지셔닝 | active | - |
| **M149** | 포지셔닝 | active | - |
| **M150** | 포지셔닝 | active | - |
| **M151** | 포지셔닝 | active | - |
| **M152** | 포지셔닝 | active | - |
| **M153** | 포지셔닝 | active | - |
| **M154** | 도면 주석 | active | - |
| **M155** | 도면 주석 | active | - |
| **M156** | 도면 주석 | active | - |
| **M157** | 도면 주석 | active | - |
| **M158** | 도면 주석 | active | - |
| **M159** | 도면 주석 | active | - |
| **M160** | 도면 주석 | active | - |
| **M161** | 도면 주석 | active | - |
| **M162** | 도면 주석 | active | - |
| **M163** | 도면 주석 | active | - |

## 16. 절차 이력

| 항목 | 값 |
|---|---|
| 독립 실행 | read-a:canonical, read-b:convergence-peer |
| 정본 실행 | `read-a` |
| 정본 지정 규칙 | `declaration-order` · 내용맹 `True` |
| 산출 시각 | 2026-09-01T02:59:58Z |
| 엔진 커밋 | `d4e6ca2d54c2ba6c3a9caf0c92042af0554a0676` |

분해는 **두 독립 실행**이 돌았고, 접지 이후는 **정본 1개**만 돌았다(재정 P-4).
정본 지정은 선언 순서이며 **내용을 보지 않는다** — 수렴 통과는 두 독해가 동치라는
선언이므로 정본 선택에 판정자가 없고, 남는 요구는 재현성뿐이기 때문이다. 두 실행은
서로의 산출을 보지 않는다 — 같은 세션의 재생성은 독립 실행이 아니다.
