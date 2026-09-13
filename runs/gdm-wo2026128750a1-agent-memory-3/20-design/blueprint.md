# 블루프린트 — `gdm-wo2026128750a1-agent-memory-3`

## 1. 표지

| 항목 | 값 |
|---|---|
| run_id | `gdm-wo2026128750a1-agent-memory-3` |
| spec_version | `1` |
| spec_digest | `sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407` |
| lane | model `claude-fable-5-1` · effort `high` · lane_id `design/blueprint/batch-0` |
| law_commit | `d8b4fb307ef0229f1aee47bc32d948cf1de15c7f` |

## 2. 훅

| 항목 | 값 |
|---|---|
| question_en | When an AI agent says it "remembers" you, is that a real architecture or just a marketing word? |
| figure | `FIG-1` |
| thesis_en | This GDM Holding filing, with Demis Hassabis among the named inventors, claims a per-user datastore of curated memory objects that the model reads at every query, writes by itself, and erases when you ask. |
| rationale_kr | 투자자-팬의 불안은 「에이전트 기억」이 실체 있는 구조인지 구호인지다(D3). FIG-1 은 질의(104)→기억 모델(105)→데이터스토어(110)→메모리 데이터(114)→입력 구조(116)→모델(118)→응답(122)까지 한 장에 루프 전체를 그리고 독립항 CL-1(M1~M6) 다섯 단계가 그대로 이 도면에 접지된다(M52~M57·M117). 스레드 전체가 이 한 장의 부품을 하나씩 확대하는 구성이므로 최강 도면이다. |

## 3. 슬롯

| 트윗 | slot | 전시 재료(ID · EN 값) | figures | point_en |
|---|---|---|---|---|
| T1 | `hook` | `M1` receiving a user-associated query by the agent system<br>`M2` accessing memory data from the user's interaction memory datastore<br>`M3` datastore comprising memory objects generated from prior interactions<br>`M4` inputting a query-and-memory input data structure to a sequence processing model<br>`M5` generating an output by processing the input data structure<br>`M6` outputting a response to the query based on the output<br>`M53`<br>`M117` Overall agent pipeline from input interfaces and query through the memory model, recall cycle, datastore query and response, memory data, input data structure, model system, output data structure, response, and output interfaces. | `FIG-1` | The independent claim is a five-step loop: receive a query, pull memory data from a datastore built from this user's past interactions, feed query plus memory into a sequence model, generate an output, and answer. Memory is a separate box in the diagram, not a longer prompt. |
| T2 | `stop` | `M3` datastore comprising memory objects generated from prior interactions<br>`M17` storing metadata with the memory value<br>`M30` memory values each comprise a string<br>`M54`<br>`M68`<br>`M81`<br>`M107` The memory is not a transcript but a set of structured containers, each holding a value plus metadata, so that recall can filter on attributes rather than re-reading raw history.<br>`M118` Structure of the interaction memory datastore as a set of memory objects, each holding memory values and memory metadata. | `FIG-2` | What sits in that box is not a transcript. Each memory object is a container holding a memory value (a string, image, or audio) plus metadata such as a timestamp, the trigger that stored it, and a summary of the conversation it came from. |
| T3 | `stop` | `M13` processing session input with a model to generate values<br>`M14` condition: values indicate a portion of input is to be stored<br>`M15` extracting the portion<br>`M16` storing the portion as a memory value in a memory object<br>`M19` portion corresponds to an explicit remember instruction<br>`M64`<br>`M65`<br>`M66`<br>`M67`<br>`M70`<br>`M112` Extracting memories offline from cached interactions is positioned as shifting compute away from query time, so runtime inference reads condensed objects rather than raw history.<br>`M120` Communication sequence in which a trigger starts a memory update cycle before a later query drives a recall cycle and model inference.<br>`M121` Memory update cycle in which cached inputs are sent to the model system, memory data updates are returned, and a memory data write is executed. | `FIG-8`, `FIG-7` | Who decides what gets stored? A model does. Cached inputs are sent to the model system, which predicts whether anything is worth remembering, extracts that portion, and writes it as a memory object; an explicit "remember this" from the user is one trigger, and the write can happen offline rather than at query time. |
| T4 | `stop` | `M12` retrieving memory values by relevance to the query<br>`M24` memory data as timestamp-ordered combination of memory values<br>`M26` computing query-based relevance measures<br>`M27` returning a relevance-based subset of memory objects<br>`M28` relevance score from embedding distance<br>`M63`<br>`M75`<br>`M77`<br>`M78`<br>`M79`<br>`M115` Ordering recalled values by timestamp is how recency is communicated to the model for resolving conflicting memories.<br>`M119` Example recall cycle in which three retrieved memory objects are condensed into memory data for the model input. | `FIG-3` | At query time the agent does not reread everything. It scores stored objects by relevance to the query, using embedding distance such as cosine similarity, returns a top subset, and orders the values by timestamp so the model sees recency. |
| T5 | `stop` | `M36` consolidating aligned memory objects into a single memory object<br>`M39` matching current memory object to a prior memory object<br>`M40` replacing the prior memory object with the current one<br>`M42` matching a portion of input data to a prior memory object<br>`M43` updating the prior memory object from the input portion<br>`M87`<br>`M90`<br>`M91`<br>`M93`<br>`M94`<br>`M109` Keeping the supporting interactions alongside a memory value lets a later contradicting input refine the memory instead of simply overwriting it.<br>`M125` Flowchart of the claimed method: receive query, access memory data, input data structure to sequence model, generate output, output response. | `FIG-21` | Memories can be corrected. New timestamped input is matched to a prior memory object and either replaces it or updates it, and aligned objects can be consolidated into one, so contradicting information refines a memory instead of noisily overwriting it. |
| T6 | `pivot` | `M20` receiving a forget instruction<br>`M21` deleting specified information from the datastore<br>`M22` receiving a delayed forget instruction<br>`M23` queuing information for deletion after the interval<br>`M71`<br>`M72`<br>`M73`<br>`M74`<br>`M110` Timestamps and optional expiration times on memory objects are the mechanism by which forgetting after an interval is implemented during maintenance cycles.<br>`M111` Because the memory is built from conversation, the same conversational channel doubles as the control surface for erasing or limiting it.<br>`M122` Memory maintenance cycle in which a memory update request with current memory data drives the model to produce memory data updates independent of new input. | `FIG-10` | The decisive detail: forgetting is claimed, not just remembering. "Forget that" deletes the specified information from the datastore, "forget this after three months" queues it for deletion after the interval, and expired objects are removed during maintenance cycles. The same chat that builds the memory is the control surface for erasing it. |
| T7 | `stop` | `M34` output comprises predictions for analytical content about query and memory data<br>`M35` analytical content predictions not exposed on the user interface<br>`M44` response comprises API-controlling instructions causing an action<br>`M85`<br>`M86`<br>`M113` The response can itself be an API call, so recalled memory conditions actions taken on a device, not only text returned to the user. | `FIG-1` | What the memory is for: the model first generates a hidden analysis of the query against the memory data that is never shown on screen, and the final response can be an API call that makes the device perform an action, so recalled memory conditions what the agent does, not only what it says. |
| T8 | `landing` | `M116` Agents without memory force users to re-enter the same details across sessions, and the alternative of wiring the agent to external data sources gives the user an all-or-nothing access choice with data the agent does not curate.<br>`M3` datastore comprising memory objects generated from prior interactions<br>`M12` retrieving memory values by relevance to the query<br>`M21` deleting specified information from the datastore<br>`M40` replacing the prior memory object with the current one | `FIG-1` | No benchmark numbers are claimed, and the filing says so by omission. What is claimed is a structural difference: memory objects generated from your own interactions, retrieved by relevance, corrected over time, and erased on request. That is a described architecture, not a slogan. |
| T9 | `tail` | `M103` bibliographic field patent.number<br>`M104` bibliographic field patent.dates.priority<br>`M106` bibliographic field patent.dates.publication |  | Pointer to the publication WO2026-128750A1 (priority 2024, published 2026) and an invitation to follow for the next patent walk-through. |

## 4. 전달 표적

| ID | kind | EN 값 |
|---|---|---|
| `M3` | `component` | datastore comprising memory objects generated from prior interactions |
| `M16` | `component` | storing the portion as a memory value in a memory object |
| `M12` | `component` | retrieving memory values by relevance to the query |
| `M21` | `component` | deleting specified information from the datastore |
| `M23` | `component` | queuing information for deletion after the interval |
| `M40` | `component` | replacing the prior memory object with the current one |
| `M116` | `positioning` | Agents without memory force users to re-enter the same details across sessions, and the alternative of wiring the agent to external data sources gives the user an all-or-nothing access choice with data the agent does not curate. |

## 5. 도면 계획

| 트윗 | figures | intent_kr |
|---|---|---|
| T1 | `FIG-1` | 전체 파이프라인 한 장 — 질의에서 응답까지의 루프 속에 기억 데이터스토어(110)가 별도 블록으로 들어 있음을 보인다. 독립항 다섯 단계가 이 도면에 그대로 접지된다. |
| T2 | `FIG-2` | 데이터스토어 내부 — 메모리 객체(202-1)가 값(204-1)과 메타데이터(206-1)를 담는 컨테이너 구조임을 보인다. 「대화 기록이 아니라 구조화된 객체」의 시각적 근거. |
| T3 | `FIG-8`, `FIG-7` | FIG-8 = 기억 갱신 사이클(캐시 입력 802 → 갱신 804 → 쓰기 806)로 「모델이 저장 여부를 판단하고 쓴다」를 보인다. FIG-7 = 트리거(702)가 갱신 사이클을 먼저 열고 나중 질의가 회상 사이클을 여는 순서. |
| T4 | `FIG-3` | 회상 사이클 예시 — 검색된 메모리 객체 셋(302·304·306)이 메모리 데이터(308)로 압축되는 모습. 「전부 다시 읽지 않고 관련 부분집합만」의 근거. |
| T5 | `FIG-21` | 청구 방법 흐름도 — 교체·갱신·통합 단계는 부호 없는 방법 흐름도에 귀속되어 있으므로 이 도면을 지정한다. 정정이 방법 단계로 청구되었음을 보이는 자리. |
| T6 | `FIG-10` | 기억 유지 사이클 — 새 입력 없이 갱신 요청(1002)만으로 모델이 갱신(804)을 내는 구조. 망각·만료가 별도 유지 사이클로 도는 결정적 물증(피벗). |
| T7 | `FIG-1` | FIG-1 의 오른쪽 절반(출력 구조 120 → 응답 122 → 출력 인터페이스 124)을 다시 가리켜 「숨은 분석은 120 에 머물고 122 만 밖으로 나가며 그것이 API 호출일 수 있다」를 보인다. |
| T8 | `FIG-1` | 첫 트윗의 도면으로 되돌아오는 북엔드 — 각 스톱에서 확대한 부품이 한 루프로 닫힘을 보이며 인용·스크린샷 표적이 되게 한다. |
| T9 |  | 꼬리 — 도면 없음. 링크와 팔로우만. |

## 6. 용어 메모 (작업 메모 · 게이트 무관 · 재정 N2)

| term_en | 트윗 | gloss_en |
|---|---|---|
| interaction memory datastore | T1 | A per-user store of memory objects built from prior conversations with the agent. |
| memory object | T2 | A container holding one or more memory values plus metadata such as a timestamp and the trigger that stored it. |
| memory update cycle | T3 | The pass in which cached inputs are sent to the model, which decides what to store and writes it. |
| recall cycle | T4 | The pass in which stored objects are scored for relevance to a query and a subset is condensed into memory data for the model. |
| expiration time | T6 | An optional time on a memory object after which it is deleted during maintenance. |

## 7. 허용 수치 제안 (run.yaml#numeric_whitelist 추기 · added_by run-discretion)

| pattern | rationale |
|---|---|
| `\b[1-9]/[1-9]\b` | Thread position marker n/N; the only number allowed that is not in the frozen material. |

## 8. 판정 행 (verdict-check-row/v0)

| check_id | ruleset | ruleset_version | ruleset_size | checked | violations | status | vacuous |
|---|---|---|---|---|---|---|---|
| design.input-digest |  |  |  | 3 | 0 | pass | none |
| design.schema |  |  |  | 1 | 0 | pass | none |
| design.spec-digest |  |  |  | 2 | 0 | pass | none |
| design.anchors-adjudicated-only |  |  |  | 0 | 0 | pass | empty-target |
| design.targets-resolve |  |  |  | 85 | 0 | pass | none |
| design.slot-count |  |  |  | 9 | 0 | pass | none |
| design.figure-budget |  |  |  | 19 | 0 | pass | none |

## 9. 미가동·부재

- 도면 자산층 부재 — 도면은 지정만(T64 ④)
- `format.stop-shape` 미가동(T64 ④)
