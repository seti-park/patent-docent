# 레인 요청 — compose-r5/v2/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `compose-r5` |
| 작업 | `v2` |
| 모델 | `opus-5` |
| effort | `xhigh` |
| 배치 | `0` |
| 절차 문서 | `engine/pens/prompt-template.md` |
| 입력 지문 | `bde55508c7b0493d7485c2c3bba2cdabd95640421a90737517a03facdec1952f` |

**응답 규약.** 이 디렉터리에 `response.json` 을 쓴다. 형태는
`{"lane_id": ..., "model": ..., "effort": ..., "input_digest": ..., "payload": {...}}` 이고,
`model`·`effort` 에는 **실제로 돌아간 값**을 적는다 — 요청과 다르면 러너가
레인 기록에 결함으로 남긴다(조용한 대체 금지). `payload` 는 아래 응답 계약을
통과해야 하며, 위반은 응답 자체가 거부된다.

**★ 입력 지문 반향(필수 · 재정 P-12).** `input_digest` 에는 위 표의 값을
**그대로** 적는다. 계산하지 말고 옮겨 적어라 — 이 값은 네가 실제로 읽은 요청이
어느 판이었는지를 가리키는 시점 표지다. 요청이 갱신되면 지문이 바뀌므로, 옛
응답을 그대로 두면 러너가 그것을 **낡은 응답으로 거부한다**. 지문이 다르거나
빠진 응답은 소비되지 않으며, 거부 사실은 레인 기록에 남는다.

**★ 지문의 규격(재정 2026-08-19 S4).** 위 표의 값은 **이 요청서 본문 전체**의
sha256 이며 지문 행 자신만 빠진다. 절차 문서 본문도 원문 조각도 여기 실려 있으므로
전부 지문에 들어간다. 이 파일만으로 다시 계산할 수 있다 —
`grep -v '^| 입력 지문 |' request.md | sha256sum`.

## 응답 계약 (response_schema)

```json
{
  "oneOf": [
    {
      "additionalProperties": false,
      "properties": {
        "thread_annotated_md": {
          "minLength": 1,
          "type": "string"
        }
      },
      "required": [
        "thread_annotated_md"
      ],
      "type": "object"
    },
    {
      "additionalProperties": false,
      "properties": {
        "material_defect": {
          "additionalProperties": false,
          "properties": {
            "blocked_slots": {
              "items": {
                "minimum": 1,
                "type": "integer"
              },
              "type": "array"
            },
            "defect_kind": {
              "enum": [
                "factual-error",
                "unresolvable-grounding",
                "missing-fact"
              ]
            },
            "evidence": {
              "minLength": 1,
              "type": "string"
            },
            "material_ids": {
              "items": {
                "pattern": "^M[0-9]+$",
                "type": "string"
              },
              "minItems": 1,
              "type": "array"
            }
          },
          "required": [
            "material_ids",
            "defect_kind",
            "evidence",
            "blocked_slots"
          ],
          "type": "object"
        }
      },
      "required": [
        "material_defect"
      ],
      "type": "object"
    }
  ],
  "title": "lane-response/compose",
  "type": "object"
}
```

## 이 요청의 지시

## 런 표지 — 프런트매터에 그대로 옮겨 적는다

| 항목 | 값 |
|---|---|
| run_id | `gdm-wo2026128750a1-agent-memory-3` |
| variant | `v2` |
| pen | `{ vendor: anthropic, model: opus-5, effort: xhigh }` |
| spec_version | `1` |
| spec_digest | `sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407` |

너는 펜이다. 원천을 보지 않는다. 「원천 조각」 절의 동결 재료와 블루프린트만 본다.

## 시트 값 (contracts/format-parameters.yaml)

| 항목 | 값 |
|---|---|
| tweet_count | `6`~`12` |
| body_char_min | `180` (stop·pivot) |
| body_char_max | `260` |
| images_per_post_max | `4` |
| slot_enum | `hook, stop, pivot, landing, tail` |

길이 단위 = `weighted_characters` — X 가중 글자 수이며 코드포인트 수가 아니다(재정 R5).

| slot | min | max | exempt |
|---|---|---|---|
| hook | `None` | `260` | `False` |
| stop | `180` | `260` | `False` |
| pivot | `180` | `260` | `False` |
| landing | `None` | `260` | `False` |
| tail | `None` | `None` | `True` |

## 블루프린트 요약 (20-design/blueprint.json)

전문은 「원천 조각」 절의 `20-design/blueprint.json` 에 있다. 아래는 그 요약이다.

| 항목 | 값 |
|---|---|
| hook.question_en | When an AI agent says it "remembers" you, is that a real architecture or just a marketing word? |
| hook.thesis_en | This GDM Holding filing, with Demis Hassabis among the named inventors, claims a per-user datastore of curated memory objects that the model reads at every query, writes by itself, and erases when you ask. |
| hook.figure | `FIG-1` |
| transmission_targets | `M3, M16, M12, M21, M23, M40, M116` |

| T | slot | exhibit material_ids | point_en |
|---|---|---|---|
| T1 | `hook` | `M1, M2, M3, M4, M5, M6, M53, M117` | The independent claim is a five-step loop: receive a query, pull memory data from a datastore built from this user's past interactions, feed query plus memory into a sequence model, generate an output, and answer. Memory is a separate box in the diagram, not a longer prompt. |
| T2 | `stop` | `M3, M17, M30, M54, M68, M81, M107, M118` | What sits in that box is not a transcript. Each memory object is a container holding a memory value (a string, image, or audio) plus metadata such as a timestamp, the trigger that stored it, and a summary of the conversation it came from. |
| T3 | `stop` | `M13, M14, M15, M16, M19, M64, M65, M66, M67, M70, M112, M120, M121` | Who decides what gets stored? A model does. Cached inputs are sent to the model system, which predicts whether anything is worth remembering, extracts that portion, and writes it as a memory object; an explicit "remember this" from the user is one trigger, and the write can happen offline rather than at query time. |
| T4 | `stop` | `M12, M24, M26, M27, M28, M63, M75, M77, M78, M79, M115, M119` | At query time the agent does not reread everything. It scores stored objects by relevance to the query, using embedding distance such as cosine similarity, returns a top subset, and orders the values by timestamp so the model sees recency. |
| T5 | `stop` | `M36, M39, M40, M42, M43, M87, M90, M91, M93, M94, M109, M125` | Memories can be corrected. New timestamped input is matched to a prior memory object and either replaces it or updates it, and aligned objects can be consolidated into one, so contradicting information refines a memory instead of noisily overwriting it. |
| T6 | `pivot` | `M20, M21, M22, M23, M71, M72, M73, M74, M110, M111, M122` | The decisive detail: forgetting is claimed, not just remembering. "Forget that" deletes the specified information from the datastore, "forget this after three months" queues it for deletion after the interval, and expired objects are removed during maintenance cycles. The same chat that builds the memory is the control surface for erasing it. |
| T7 | `stop` | `M34, M35, M44, M85, M86, M113` | What the memory is for: the model first generates a hidden analysis of the query against the memory data that is never shown on screen, and the final response can be an API call that makes the device perform an action, so recalled memory conditions what the agent does, not only what it says. |
| T8 | `landing` | `M116, M3, M12, M21, M40` | No benchmark numbers are claimed, and the filing says so by omission. What is claimed is a structural difference: memory objects generated from your own interactions, retrieved by relevance, corrected over time, and erased on request. That is a described architecture, not a slogan. |
| T9 | `tail` | `M103, M104, M106` | Pointer to the publication WO2026-128750A1 (priority 2024, published 2026) and an invitation to follow for the next patent walk-through. |

| term_en | tweet | gloss_en |
|---|---|---|
| interaction memory datastore | T1 | A per-user store of memory objects built from prior conversations with the agent. |
| memory object | T2 | A container holding one or more memory values plus metadata such as a timestamp and the trigger that stored it. |
| memory update cycle | T3 | The pass in which cached inputs are sent to the model, which decides what to store and writes it. |
| recall cycle | T4 | The pass in which stored objects are scored for relevance to a query and a subset is condensed into memory data for the model. |
| expiration time | T6 | An optional time on a memory object after which it is deleted during maintenance. |

## 도면 헤더 — 트윗별 자산 표 (30-figures/selection.json · 30-figures/assets/manifest.json)

| T | slot | 자산 id | 원본 도면 |
|---|---|---|---|
| T1 | `hero` | `fig-01` | `FIG-1` |
| T2 | `exhibit` | `fig-02` | `FIG-2` |
| T3 | `exhibit` | `fig-08` | `FIG-8` |
| T3 | `exhibit` | `fig-07` | `FIG-7` |
| T4 | `exhibit` | `fig-03` | `FIG-3` |
| T5 | `exhibit` | `fig-21` | `FIG-21` |
| T6 | `exhibit` | `fig-10` | `FIG-10` |
| T7 | `exhibit` | `fig-01` | `FIG-1` |
| T8 | `exhibit` | `fig-01` | `FIG-1` |

각 트윗 헤더의 `fig` 는 이 표의 자산 id 를 `+` 로 잇는다(없으면 `none`).
본문 전시 스톱과 반전 스톱(stop · pivot)은 2 문장으로 쓴다(시트 `stop_shape.sentences_max` = `2`).
트윗당 자산 상한 = 시트 `images_per_post_max` = `4`.

## 국소 수정 — 라운드 2

이 판은 직전 판(「원천 조각」의 `40-compose/v2/thread.annotated.md` · 지문 `sha256:9701fec17daf420f5b5d1f1c7656971f40b9e7e28fae60a55f75bcbe0d2ccb84`)의 국소 수정이다. 아래 표의 좌표에 선 문장만 지시문대로 고쳐 쓴다. 다른 문장은 바이트 그대로 둔다. 태그·헤더·프런트매터 규약은 동일하다.

## 국소 수정 지시 표 (50-gate/<v>/revisions/r<n>/directives.json)

| id | layer | rule | locus | fix_directive |
|---|---|---|---|---|
| `d-l1-001` | `l1` | `l1.citation-mismatch` | T5/S1 | T5/S1 의 타임스탬프 한정에 그것을 담지하는 M37·M41 을 인용에 더하거나, 그 한정을 걷어내고 인용 항목이 실제로 담지하는 대조·교체·갱신만 남겨 재서술하라. |

## 원천 조각

### `15-frozen/material-spec.v1.json`

```text
{
  "claims": {
    "applicant_interest": [],
    "dependents": [
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-2/a1",
            "material_id": "M7",
            "text_verbatim": "wherein the interaction memory datastore comprises multimodal data"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-2/a2",
            "material_id": "M8",
            "text_verbatim": "wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-1"
        ],
        "id": "CL-2",
        "text_verbatim": "The method of claim 1 , wherein the interaction memory datastore comprises multimodal data, and wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-3/a1",
            "material_id": "M9",
            "text_verbatim": "the first data modality comprises audio data, and wherein the second data modality comprises image data"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-3/a2",
            "material_id": "M10",
            "text_verbatim": "the first data modality comprises text data, and wherein the second data modality comprises image data"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-3/a3",
            "material_id": "M11",
            "text_verbatim": "the first data modality comprises text data, and wherein the second data modality comprises audio data"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-2"
        ],
        "id": "CL-3",
        "text_verbatim": "The method of claim 2, wherein:\n\nthe first data modality comprises audio data, and wherein the second data modality comprises image data;\n\nthe first data modality comprises text data, and wherein the second data modality comprises image data; or\n\nthe first data modality comprises text data, and wherein the second data modality comprises audio data."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-4/a1",
            "material_id": "M12",
            "text_verbatim": "retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-1"
        ],
        "id": "CL-4",
        "text_verbatim": "The method of claim 1 , comprising:\n\nretrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-5/a1",
            "material_id": "M13",
            "text_verbatim": "after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-5/a2",
            "material_id": "M14",
            "text_verbatim": "based on the generated one or more values indicating that at least a portion of the input is to be stored"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-5/a3",
            "material_id": "M15",
            "text_verbatim": "extracting, by the machine-learned agent system, the portion"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-5/a4",
            "material_id": "M16",
            "text_verbatim": "storing, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4"
        ],
        "id": "CL-5",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nafter receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values; and \n\nbased on the generated one or more values indicating that at least a portion of the input is to be stored:\n\nextracting, by the machine-learned agent system, the portion; and\n\nstoring, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-6/a1",
            "material_id": "M17",
            "text_verbatim": "storing, by the machine-learned agent system, metadata associated with the memory value in the memory object"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-5"
        ],
        "id": "CL-6",
        "text_verbatim": "The method of claim 5, comprising:\n\nstoring, by the machine-learned agent system, metadata associated with the memory value in the memory object."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-7/a1",
            "material_id": "M18",
            "text_verbatim": "wherein the portion comprises at least one of: text data, image data, or audio data"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-5"
        ],
        "id": "CL-7",
        "text_verbatim": "The method of claim 5, wherein the portion comprises at least one of: text data, image data, or audio data."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-8/a1",
            "material_id": "M19",
            "text_verbatim": "wherein the portion corresponds to an explicit instruction to remember information"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-5"
        ],
        "id": "CL-8",
        "text_verbatim": "The method of claim 5, wherein the portion corresponds to an explicit instruction to remember information."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-9/a1",
            "material_id": "M20",
            "text_verbatim": "receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information"
          },
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-9/a2",
            "material_id": "M21",
            "text_verbatim": "deleting, by the machine-learned agent system, the specified information from the interaction memory datastore"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8"
        ],
        "id": "CL-9",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nreceiving, by the machine-learned agent system, input data indicating an instruction to forget specified information; and\n\ndeleting, by the machine-learned agent system, the specified information from the interaction memory datastore."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-10/a1",
            "material_id": "M22",
            "text_verbatim": "receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval"
          },
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-10/a2",
            "material_id": "M23",
            "text_verbatim": "queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9"
        ],
        "id": "CL-10",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nreceiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval; and\n\nqueuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-11/a1",
            "material_id": "M24",
            "text_verbatim": "wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10"
        ],
        "id": "CL-11",
        "text_verbatim": "The method of any of the preceding claims, wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-12/a1",
            "material_id": "M25",
            "text_verbatim": "filtering the plurality of memory objects to obtain the one or more memory values"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-12/a2",
            "material_id": "M26",
            "text_verbatim": "computing one or more relevance measures for the plurality of memory objects based on the query"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-12/a3",
            "material_id": "M27",
            "text_verbatim": "returning a subset of the plurality of memory objects based on the relevance measure"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11"
        ],
        "id": "CL-12",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nfiltering the plurality of memory objects to obtain the one or more memory values, wherein the filtering comprises: \n\ncomputing one or more relevance measures for the plurality of memory objects based on the query; and\n\nreturning a subset of the plurality of memory objects based on the relevance measure."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-13/a1",
            "material_id": "M28",
            "text_verbatim": "a respective score generated based on distance between a query embedding and a respective memory value embedding"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-13/a2",
            "material_id": "M29",
            "text_verbatim": "a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-12"
        ],
        "id": "CL-13",
        "text_verbatim": "The method of claim 12, wherein the one or more relevance measures comprise:\n\na respective score generated based on distance between a query embedding and a respective memory value embedding; or\n\na respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-14/a1",
            "material_id": "M30",
            "text_verbatim": "wherein the one or more memory values each comprise a respective string"
          },
          {
            "attaches_to": "CL-1/e2",
            "id": "CL-14/a2",
            "material_id": "M31",
            "text_verbatim": "wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13"
        ],
        "id": "CL-14",
        "text_verbatim": "The method of any of the preceding claims, wherein the one or more memory values each comprise a respective string, and wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e5",
            "id": "CL-15/a1",
            "material_id": "M32",
            "text_verbatim": "inputting at least a portion of the output to the machine-learned sequence processing model"
          },
          {
            "attaches_to": "CL-1/e5",
            "id": "CL-15/a2",
            "material_id": "M33",
            "text_verbatim": "generating, based on processing the output using the machine-learned sequence processing model, the response to the query"
          },
          {
            "attaches_to": "CL-1/e4",
            "id": "CL-15/a3",
            "material_id": "M34",
            "text_verbatim": "wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14"
        ],
        "id": "CL-15",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\ninputting at least a portion of the output to the machine-learned sequence processing model; generating, based on processing the output using the machine-learned sequence processing model, the response to the query;\n\nwherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e4",
            "id": "CL-16/a1",
            "material_id": "M35",
            "text_verbatim": "wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15"
        ],
        "id": "CL-16",
        "text_verbatim": "The method of any of the preceding claims, wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-17/a1",
            "material_id": "M36",
            "text_verbatim": "consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16"
        ],
        "id": "CL-17",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nconsolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-18/a1",
            "material_id": "M37",
            "text_verbatim": "receiving input data associated with a timestamp"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-18/a2",
            "material_id": "M38",
            "text_verbatim": "creating a current memory object comprising:\n\nthe timestamp; and\n\na current memory value based on the input data"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-18/a3",
            "material_id": "M39",
            "text_verbatim": "matching the current memory object to a prior memory object"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-18/a4",
            "material_id": "M40",
            "text_verbatim": "replacing, in the interaction memory datastore, the prior memory object with the current memory object"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17"
        ],
        "id": "CL-18",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nreceiving input data associated with a timestamp;\n\ncreating a current memory object comprising:\n\nthe timestamp; and\n\na current memory value based on the input data;\n\nmatching the current memory object to a prior memory object; and \n\nreplacing, in the interaction memory datastore, the prior memory object with the current memory object."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-19/a1",
            "material_id": "M41",
            "text_verbatim": "receiving input data associated with a timestamp"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-19/a2",
            "material_id": "M42",
            "text_verbatim": "matching at least a portion of the input data to a prior memory object"
          },
          {
            "attaches_to": "CL-1/e2/e1",
            "id": "CL-19/a3",
            "material_id": "M43",
            "text_verbatim": "updating, in the interaction memory datastore, the prior memory object based on the portion of the input data"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17",
          "CL-18"
        ],
        "id": "CL-19",
        "text_verbatim": "The method of any of the preceding claims, comprising:\n\nreceiving input data associated with a timestamp;\n\nmatching at least a portion of the input data to a prior memory object;\n\nupdating, in the interaction memory datastore, the prior memory object based on the portion of the input data."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e5",
            "id": "CL-20/a1",
            "material_id": "M44",
            "text_verbatim": "wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17",
          "CL-18",
          "CL-19"
        ],
        "id": "CL-20",
        "text_verbatim": "The method of any of the preceding claims, wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-21/a1",
            "material_id": "M45",
            "text_verbatim": "wherein the query indicates a configuration parameter that controls an operation of the computing system"
          },
          {
            "attaches_to": "CL-1/e5",
            "id": "CL-21/a2",
            "material_id": "M46",
            "text_verbatim": "wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-20"
        ],
        "id": "CL-21",
        "text_verbatim": "The method of claim 20, wherein the query indicates a configuration parameter that controls an operation of the computing system, and wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-22/a1",
            "material_id": "M47",
            "text_verbatim": "wherein the configuration parameter is associated with at least one of:\n\ndata access by the computing system;\n\ndata retention by the computing system; or\n\ndata communication by the computing system"
          }
        ],
        "dependency_type": "single",
        "depends_on": [
          "CL-21"
        ],
        "id": "CL-22",
        "text_verbatim": "The method of claim 21 , wherein the configuration parameter is associated with at least one of:\n\ndata access by the computing system;\n\ndata retention by the computing system; or\n\ndata communication by the computing system."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-23/a1",
            "material_id": "M48",
            "text_verbatim": "One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17",
          "CL-18",
          "CL-19",
          "CL-20",
          "CL-21",
          "CL-22"
        ],
        "id": "CL-23",
        "text_verbatim": "One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-24/a1",
            "material_id": "M49",
            "text_verbatim": "one or more processors"
          },
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-24/a2",
            "material_id": "M50",
            "text_verbatim": "one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17",
          "CL-18",
          "CL-19",
          "CL-20",
          "CL-21",
          "CL-22"
        ],
        "id": "CL-24",
        "text_verbatim": "A computing system, comprising:\n\none or more processors; and\n\none or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims."
      },
      {
        "additions": [
          {
            "attaches_to": "CL-1/e1",
            "id": "CL-25/a1",
            "material_id": "M51",
            "text_verbatim": "A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims"
          }
        ],
        "dependency_type": "all-preceding",
        "depends_on": [
          "CL-1",
          "CL-2",
          "CL-3",
          "CL-4",
          "CL-5",
          "CL-6",
          "CL-7",
          "CL-8",
          "CL-9",
          "CL-10",
          "CL-11",
          "CL-12",
          "CL-13",
          "CL-14",
          "CL-15",
          "CL-16",
          "CL-17",
          "CL-18",
          "CL-19",
          "CL-20",
          "CL-21",
          "CL-22"
        ],
        "id": "CL-25",
        "text_verbatim": "A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims."
      }
    ],
    "independent": [
      {
        "elements": [
          {
            "children": [],
            "id": "CL-1/e1",
            "material_id": "M1",
            "text_verbatim": "receiving, by a machine-learned agent system, a query associated with a user"
          },
          {
            "children": [
              {
                "children": [],
                "id": "CL-1/e2/e1",
                "material_id": "M3",
                "text_verbatim": "wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user"
              }
            ],
            "id": "CL-1/e2",
            "material_id": "M2",
            "text_verbatim": "accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user"
          },
          {
            "children": [],
            "id": "CL-1/e3",
            "material_id": "M4",
            "text_verbatim": "inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data"
          },
          {
            "children": [],
            "id": "CL-1/e4",
            "material_id": "M5",
            "text_verbatim": "generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output"
          },
          {
            "children": [],
            "id": "CL-1/e5",
            "material_id": "M6",
            "text_verbatim": "outputting, by the machine-learned agent system, and based on the output, a response to the query"
          }
        ],
        "id": "CL-1",
        "text_verbatim": "A computer-implemented method, comprising:\n\nreceiving, by a machine-learned agent system, a query associated with a user;\n\naccessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user, wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user;\n\ninputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data;\n\ngenerating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output; and\n\noutputting, by the machine-learned agent system, and based on the output, a response to the query.",
        "type": "independent"
      }
    ]
  },
  "extensions": {
    "docent": {
      "drop_signal": {
        "reason": "대화형 에이전트가 사용자별 기억을 쌓고·잊고·정정하는 구조는 일반 독자가 자기 경험(같은 말 반복 입력, 잊어달라는 요청)에 바로 잇댈 수 있어 안도감 서사가 성립한다. 성능 수치는 없으나 구조적 차이(사용자 발화로 만든 기억 객체 · 지원 기록 · 만료 기반 망각)가 명확하다.",
        "stage": "final",
        "verdict": "go"
      }
    }
  },
  "figures": [
    {
      "asset_path": null,
      "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-1",
      "numerals": [
        "102",
        "104",
        "105",
        "106",
        "108",
        "110",
        "114",
        "116",
        "118",
        "120",
        "122",
        "124"
      ],
      "raw_path": "00-source/figures-raw/fig-01.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-2",
      "numerals": [
        "110",
        "202-1",
        "204-1",
        "206-1"
      ],
      "raw_path": "00-source/figures-raw/fig-02.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-3",
      "numerals": [
        "302",
        "304",
        "306",
        "308"
      ],
      "raw_path": "00-source/figures-raw/fig-03.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 7 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-7",
      "numerals": [
        "702"
      ],
      "raw_path": "00-source/figures-raw/fig-07.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-8",
      "numerals": [
        "802",
        "804",
        "806"
      ],
      "raw_path": "00-source/figures-raw/fig-08.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-10",
      "numerals": [
        "1002",
        "804"
      ],
      "raw_path": "00-source/figures-raw/fig-10.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.",
      "id": "FIG-13",
      "numerals": [
        "4",
        "6"
      ],
      "raw_path": "00-source/figures-raw/fig-13.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.",
      "id": "FIG-19",
      "numerals": [],
      "raw_path": "00-source/figures-raw/fig-19.png"
    },
    {
      "asset_path": null,
      "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
      "id": "FIG-21",
      "numerals": [],
      "raw_path": "00-source/figures-raw/fig-21.png"
    }
  ],
  "items": [
    {
      "claim_ref": "CL-1/e1",
      "id": "M1",
      "kind": "component",
      "label_en": "receiving a user-associated query by the agent system",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "receiving, by a machine-learned agent system, a query associated with a user"
    },
    {
      "claim_ref": "CL-1/e2",
      "id": "M2",
      "kind": "component",
      "label_en": "accessing memory data from the user's interaction memory datastore",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "accessing, by the machine-learned agent system, memory data from an interaction memory datastore associated with the user"
    },
    {
      "claim_ref": "CL-1/e2/e1",
      "id": "M3",
      "kind": "component",
      "label_en": "datastore comprising memory objects generated from prior interactions",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the interaction memory datastore comprises one or more memory objects that were generated based on one or more prior interactions between the machine-learned agent system and the user"
    },
    {
      "claim_ref": "CL-1/e3",
      "id": "M4",
      "kind": "component",
      "label_en": "inputting a query-and-memory input data structure to a sequence processing model",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data"
    },
    {
      "claim_ref": "CL-1/e4",
      "id": "M5",
      "kind": "component",
      "label_en": "generating an output by processing the input data structure",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "generating, by the machine-learned agent system and based on processing the input data structure using the machine-learned sequence processing model, an output"
    },
    {
      "claim_ref": "CL-1/e5",
      "id": "M6",
      "kind": "component",
      "label_en": "outputting a response to the query based on the output",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "outputting, by the machine-learned agent system, and based on the output, a response to the query"
    },
    {
      "claim_ref": "CL-2/a1",
      "id": "M7",
      "kind": "component",
      "label_en": "datastore comprising multimodal data",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the interaction memory datastore comprises multimodal data"
    },
    {
      "claim_ref": "CL-2/a2",
      "id": "M8",
      "kind": "component",
      "label_en": "memory data based on memory objects of two data modalities",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the memory data is based on a first memory object associated with a first data modality and a second memory object associated with a second data modality"
    },
    {
      "claim_ref": "CL-3/a1",
      "id": "M9",
      "kind": "component",
      "label_en": "audio and image modality pair",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "the first data modality comprises audio data, and wherein the second data modality comprises image data"
    },
    {
      "claim_ref": "CL-3/a2",
      "id": "M10",
      "kind": "component",
      "label_en": "text and image modality pair",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "the first data modality comprises text data, and wherein the second data modality comprises image data"
    },
    {
      "claim_ref": "CL-3/a3",
      "id": "M11",
      "kind": "component",
      "label_en": "text and audio modality pair",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "the first data modality comprises text data, and wherein the second data modality comprises audio data"
    },
    {
      "claim_ref": "CL-4/a1",
      "id": "M12",
      "kind": "component",
      "label_en": "retrieving memory values by relevance to the query",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "retrieving, by the machine-learned agent system, and from the interaction memory datastore, the one or more memory values based on a relevance of the one or more memory values to the query"
    },
    {
      "claim_ref": "CL-5/a1",
      "id": "M13",
      "kind": "component",
      "label_en": "processing session input with a model to generate values",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "after receiving an input during an interactive session, processing, by the machine-learned agent system, the input using a machine-learned model to generate one or more values"
    },
    {
      "claim_ref": "CL-5/a2",
      "id": "M14",
      "kind": "component",
      "label_en": "condition: values indicate a portion of input is to be stored",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "based on the generated one or more values indicating that at least a portion of the input is to be stored"
    },
    {
      "claim_ref": "CL-5/a3",
      "id": "M15",
      "kind": "component",
      "label_en": "extracting the portion",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "extracting, by the machine-learned agent system, the portion"
    },
    {
      "claim_ref": "CL-5/a4",
      "id": "M16",
      "kind": "component",
      "label_en": "storing the portion as a memory value in a memory object",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "storing, by the machine-learned agent system, the portion as a memory value in a memory object in the interaction memory datastore"
    },
    {
      "claim_ref": "CL-6/a1",
      "id": "M17",
      "kind": "component",
      "label_en": "storing metadata with the memory value",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "storing, by the machine-learned agent system, metadata associated with the memory value in the memory object"
    },
    {
      "claim_ref": "CL-7/a1",
      "id": "M18",
      "kind": "component",
      "label_en": "portion comprises text, image, or audio data",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the portion comprises at least one of: text data, image data, or audio data"
    },
    {
      "claim_ref": "CL-8/a1",
      "id": "M19",
      "kind": "component",
      "label_en": "portion corresponds to an explicit remember instruction",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the portion corresponds to an explicit instruction to remember information"
    },
    {
      "claim_ref": "CL-9/a1",
      "id": "M20",
      "kind": "component",
      "label_en": "receiving a forget instruction",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information"
    },
    {
      "claim_ref": "CL-9/a2",
      "id": "M21",
      "kind": "component",
      "label_en": "deleting specified information from the datastore",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "deleting, by the machine-learned agent system, the specified information from the interaction memory datastore"
    },
    {
      "claim_ref": "CL-10/a1",
      "id": "M22",
      "kind": "component",
      "label_en": "receiving a delayed forget instruction",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "receiving, by the machine-learned agent system, input data indicating an instruction to forget specified information after a specified interval"
    },
    {
      "claim_ref": "CL-10/a2",
      "id": "M23",
      "kind": "component",
      "label_en": "queuing information for deletion after the interval",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "queuing, by the machine-learned agent system, the specified information for deletion from the interaction memory datastore after the specified interval"
    },
    {
      "claim_ref": "CL-11/a1",
      "id": "M24",
      "kind": "component",
      "label_en": "memory data as timestamp-ordered combination of memory values",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the memory data comprises an ordered combination of the one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects"
    },
    {
      "claim_ref": "CL-12/a1",
      "id": "M25",
      "kind": "component",
      "label_en": "filtering memory objects to obtain memory values",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "filtering the plurality of memory objects to obtain the one or more memory values"
    },
    {
      "claim_ref": "CL-12/a2",
      "id": "M26",
      "kind": "component",
      "label_en": "computing query-based relevance measures",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "computing one or more relevance measures for the plurality of memory objects based on the query"
    },
    {
      "claim_ref": "CL-12/a3",
      "id": "M27",
      "kind": "component",
      "label_en": "returning a relevance-based subset of memory objects",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "returning a subset of the plurality of memory objects based on the relevance measure"
    },
    {
      "claim_ref": "CL-13/a1",
      "id": "M28",
      "kind": "component",
      "label_en": "relevance score from embedding distance",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "a respective score generated based on distance between a query embedding and a respective memory value embedding"
    },
    {
      "claim_ref": "CL-13/a2",
      "id": "M29",
      "kind": "component",
      "label_en": "relevance as sequence output of a second sequence processing model",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model"
    },
    {
      "claim_ref": "CL-14/a1",
      "id": "M30",
      "kind": "component",
      "label_en": "memory values each comprise a string",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the one or more memory values each comprise a respective string"
    },
    {
      "claim_ref": "CL-14/a2",
      "id": "M31",
      "kind": "component",
      "label_en": "memory data as a string of the memory value strings",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the memory data comprises a string comprising the one or more respective strings from the one or more memory values"
    },
    {
      "claim_ref": "CL-15/a1",
      "id": "M32",
      "kind": "component",
      "label_en": "feeding a portion of the output back to the sequence processing model",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "inputting at least a portion of the output to the machine-learned sequence processing model"
    },
    {
      "claim_ref": "CL-15/a2",
      "id": "M33",
      "kind": "component",
      "label_en": "generating the response by processing the output",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "generating, based on processing the output using the machine-learned sequence processing model, the response to the query"
    },
    {
      "claim_ref": "CL-15/a3",
      "id": "M34",
      "kind": "component",
      "label_en": "output comprises predictions for analytical content about query and memory data",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the output comprises a plurality of predictions for analytical content that comprises an analysis of the query with respect to the memory data"
    },
    {
      "claim_ref": "CL-16/a1",
      "id": "M35",
      "kind": "component",
      "label_en": "analytical content predictions not exposed on the user interface",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query"
    },
    {
      "claim_ref": "CL-17/a1",
      "id": "M36",
      "kind": "component",
      "label_en": "consolidating aligned memory objects into a single memory object",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset"
    },
    {
      "claim_ref": "CL-18/a1",
      "id": "M37",
      "kind": "component",
      "label_en": "receiving timestamped input data",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "receiving input data associated with a timestamp"
    },
    {
      "claim_ref": "CL-18/a2",
      "id": "M38",
      "kind": "component",
      "label_en": "creating a current memory object with timestamp and current memory value",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "creating a current memory object comprising:\n\nthe timestamp; and\n\na current memory value based on the input data"
    },
    {
      "claim_ref": "CL-18/a3",
      "id": "M39",
      "kind": "component",
      "label_en": "matching current memory object to a prior memory object",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "matching the current memory object to a prior memory object"
    },
    {
      "claim_ref": "CL-18/a4",
      "id": "M40",
      "kind": "component",
      "label_en": "replacing the prior memory object with the current one",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "replacing, in the interaction memory datastore, the prior memory object with the current memory object"
    },
    {
      "claim_ref": "CL-19/a1",
      "id": "M41",
      "kind": "component",
      "label_en": "receiving timestamped input data",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "receiving input data associated with a timestamp"
    },
    {
      "claim_ref": "CL-19/a2",
      "id": "M42",
      "kind": "component",
      "label_en": "matching a portion of input data to a prior memory object",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "matching at least a portion of the input data to a prior memory object"
    },
    {
      "claim_ref": "CL-19/a3",
      "id": "M43",
      "kind": "component",
      "label_en": "updating the prior memory object from the input portion",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "updating, in the interaction memory datastore, the prior memory object based on the portion of the input data"
    },
    {
      "claim_ref": "CL-20/a1",
      "id": "M44",
      "kind": "component",
      "label_en": "response comprises API-controlling instructions causing an action",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the response comprises instructions configured to control an application programming interface to cause a computing system to perform an action"
    },
    {
      "claim_ref": "CL-21/a1",
      "id": "M45",
      "kind": "component",
      "label_en": "query indicates a configuration parameter of the computing system",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the query indicates a configuration parameter that controls an operation of the computing system"
    },
    {
      "claim_ref": "CL-21/a2",
      "id": "M46",
      "kind": "component",
      "label_en": "instructions cause assignment of a configuration parameter value",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter"
    },
    {
      "claim_ref": "CL-22/a1",
      "id": "M47",
      "kind": "component",
      "label_en": "configuration parameter concerns data access, retention, or communication",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "wherein the configuration parameter is associated with at least one of:\n\ndata access by the computing system;\n\ndata retention by the computing system; or\n\ndata communication by the computing system"
    },
    {
      "claim_ref": "CL-23/a1",
      "id": "M48",
      "kind": "component",
      "label_en": "non-transitory media storing instructions performing the method",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "One or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims"
    },
    {
      "claim_ref": "CL-24/a1",
      "id": "M49",
      "kind": "component",
      "label_en": "one or more processors",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "one or more processors"
    },
    {
      "claim_ref": "CL-24/a2",
      "id": "M50",
      "kind": "component",
      "label_en": "media storing instructions causing the system to perform the method",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising the method of any of the preceding claims"
    },
    {
      "claim_ref": "CL-25/a1",
      "id": "M51",
      "kind": "component",
      "label_en": "computer program product with instructions performing the method",
      "status": "active",
      "superseded_by": null,
      "text_verbatim": "A computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising the method of any of the preceding claims"
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M1",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "102",
            "104"
          ]
        }
      ],
      "id": "M52",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0065]",
          "quote": "Input interface(s) 102 can receive inputs (e.g., from a user). Query 104 can be based on data from input interfaces 102."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M2",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "100",
            "108",
            "110"
          ]
        }
      ],
      "id": "M53",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0066]",
          "quote": "Machine-learned agent system 100 can issue a memory query 108 to interaction memory datastore 110."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M3",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "110"
          ]
        }
      ],
      "id": "M54",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0066]",
          "quote": "Interaction memory datastore 110 can contain stored contextual information catalogued and stored over prior interactions with the user."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M4",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "114",
            "116"
          ]
        }
      ],
      "id": "M55",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0067]",
          "quote": "Machine-learned agent system 100 can output input data structure 116 based on memory data 114."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M5",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "116",
            "118",
            "120"
          ]
        }
      ],
      "id": "M56",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0068]",
          "quote": "Machine-learned model system 118 can process input data structure 116 to generate output data structure 120."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M6",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "120",
            "122"
          ]
        }
      ],
      "id": "M57",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0069]",
          "quote": "Machine-learned agent system 100 can output response 122 based on output data structure 120."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M7",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "110"
          ]
        }
      ],
      "id": "M58",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0100]",
          "quote": "Interaction memory datastore 110 can be multimodal. For example, one or more queries can include data of a first modality and one or more queries can include data of a second modality."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M8",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "202-1",
            "204-1"
          ]
        }
      ],
      "id": "M59",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0159]",
          "quote": "A memory object can include data of a first modality and data of a second modality. Different modalities can be stored in different memory objects and linked through metadata."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M9",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "110",
            "204-1"
          ]
        }
      ],
      "id": "M60",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0162]",
          "quote": "interaction memory datastore 110 can store image data in association with audio data, such as a video recording recorded during an interaction session and a voice recording recorded during the interaction session."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M10",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "110",
            "204-1"
          ]
        }
      ],
      "id": "M61",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0163]",
          "quote": "interaction memory datastore 110 can store image data in association with text data, such as image data from a video recording recorded during an interaction session and a transcription from a voice recording recorded during the interaction session."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M11",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "110",
            "204-1"
          ]
        }
      ],
      "id": "M62",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0164]",
          "quote": "interaction memory datastore 110 can store audio data in association with text data. Audio data (e.g., music) and text data (e.g., comments on the music) can be stored as multimodal memories in interaction memory datastore 110."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M12",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "105",
            "106",
            "110"
          ]
        }
      ],
      "id": "M63",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0090]",
          "quote": "For example, memory model 105 can initiate similarity search operations to retrieve a number of relevant stored memories for a particular query."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M13",
      "figure_refs": [
        {
          "caption_quote": "Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-8",
          "numerals": [
            "802",
            "804"
          ]
        }
      ],
      "id": "M64",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0088]",
          "quote": "memory model 105 can invoke a machine-learned model input (e.g., after one or more inputs are received) that causes a machine-learned model to predict whether there is anything in the query that is to be remembered."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M14",
      "figure_refs": [
        {
          "caption_quote": "Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-8",
          "numerals": [
            "804"
          ]
        }
      ],
      "id": "M65",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0439]",
          "quote": "The values can indicate that at least a portion of the input is to be stored."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M15",
      "figure_refs": [
        {
          "caption_quote": "Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-8",
          "numerals": [
            "804"
          ]
        }
      ],
      "id": "M66",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0088]",
          "quote": "Predicting new information to remember can include generating a portion or excerpt of content to remember."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M16",
      "figure_refs": [
        {
          "caption_quote": "Figure 8 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-8",
          "numerals": [
            "806"
          ]
        }
      ],
      "id": "M67",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0282]",
          "quote": "Memory model 105 can execute a memory data write 806 to add or update memory data objects in interaction memory datastore 110."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M17",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "206-1"
          ]
        }
      ],
      "id": "M68",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0054]",
          "quote": "Additional metadata may be stored in the memory object, such as a timestamp, the type of trigger used for storing the memory, a summary of the interaction during which the memory value was received, or other attributes."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M18",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "204-1"
          ]
        }
      ],
      "id": "M69",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0154]",
          "quote": "A memory value can be extracted or excerpted from an interaction. For example, a visual memory can be stored by saving all or part of one or more images associated with an interaction session. A textual memory can be stored by saving all or part of one or more messages or documents associated with an interaction session. An audio memory can be stored by saving all or part of one or more audio files or streams associated with an interaction session."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M19",
      "figure_refs": [
        {
          "caption_quote": "Figure 7 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-7",
          "numerals": [
            "702"
          ]
        }
      ],
      "id": "M70",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0054]",
          "quote": "An example explicit trigger may occur when a user instructs the machine-learned agent system to remember a particular piece of information, such as the user’s favorite architect."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M20",
      "figure_refs": [
        {
          "caption_quote": "Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-10",
          "numerals": [
            "1002"
          ]
        }
      ],
      "id": "M71",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0293]",
          "quote": "Explicit forgetting may be triggered by user commands such as “forget that,” “delete this conversation,” or “forget information related to [topic].”"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M21",
      "figure_refs": [
        {
          "caption_quote": "Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-10",
          "numerals": [
            "1002",
            "804"
          ]
        }
      ],
      "id": "M72",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0443]",
          "quote": "Memory model 105 can then cause the identified memory objects to be deleted from interaction memory datastore 110."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M22",
      "figure_refs": [
        {
          "caption_quote": "Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-10",
          "numerals": [
            "1002"
          ]
        }
      ],
      "id": "M73",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0057]",
          "quote": "The user can instruct the machine-learned agent system to forget information after three months."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M23",
      "figure_refs": [
        {
          "caption_quote": "Figure 10 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-10",
          "numerals": [
            "1002",
            "804"
          ]
        }
      ],
      "id": "M74",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0295]",
          "quote": "Memory objects exceeding their expiration time may be automatically deleted during scheduled maintenance operations."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M24",
      "figure_refs": [
        {
          "caption_quote": "Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-3",
          "numerals": [
            "308"
          ]
        }
      ],
      "id": "M75",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0165]",
          "quote": "In some implementations, the memory data includes an ordered combination of one or more memory values, the ordered combination ordered based on corresponding timestamps of the plurality of memory objects."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M25",
      "figure_refs": [
        {
          "caption_quote": "Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-3",
          "numerals": [
            "302",
            "304",
            "306"
          ]
        }
      ],
      "id": "M76",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0446]",
          "quote": "the machine-learned agent system (e.g., 100) can use a memory query"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M26",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "106",
            "108"
          ]
        }
      ],
      "id": "M77",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0446]",
          "quote": "The filtering process can involve computing one or more relevance measures (e.g., similarity scores, distance metrics, or probabilities) for each memory object"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M27",
      "figure_refs": [
        {
          "caption_quote": "Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-3",
          "numerals": [
            "302",
            "304",
            "306"
          ]
        }
      ],
      "id": "M78",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0179]",
          "quote": "The top-K most similar memory objects can be retrieved, where K is a configurable parameter."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M28",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "204-1"
          ]
        }
      ],
      "id": "M79",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0179]",
          "quote": "A vector embedding of the pre-processed query can be compared to vector embeddings of values within memory objects stored in the database. This comparison can use similarity metrics like cosine similarity to identify memory objects semantically related to the query."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M29",
      "figure_refs": [
        {
          "caption_quote": "Figure 13 is a block diagram of an example sequence processing model according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-13",
          "numerals": [
            "4",
            "6"
          ]
        }
      ],
      "id": "M80",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0447]",
          "quote": "the one or more relevance measures include a respective sequence output generated by processing the query and one or more respective memory values using a second machine-learned sequence processing model that is optionally the same as or different from the machine-learned sequence processing model."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M30",
      "figure_refs": [
        {
          "caption_quote": "Figure 2 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-2",
          "numerals": [
            "204-1"
          ]
        }
      ],
      "id": "M81",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0053]",
          "quote": "a memory object can be a data container that stores one or more memory values (e.g., strings, images, audio, etc.) along with relevant metadata."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M31",
      "figure_refs": [
        {
          "caption_quote": "Figure 3 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-3",
          "numerals": [
            "308"
          ]
        }
      ],
      "id": "M82",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0182]",
          "quote": "concatenating multiple textual memory values into a string representation for insertion into a prompt"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M32",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "116",
            "118"
          ]
        }
      ],
      "id": "M83",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0117]",
          "quote": "A second input data structure can contain the generated analysis along with an instruction to generate a final response based on the analysis."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M33",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "120",
            "122"
          ]
        }
      ],
      "id": "M84",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0117]",
          "quote": "A second output data structure can contain the final response. Machine-learned agent system 100 can generate response 122 based on the second output data structure, which was based on the first output data structure."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M34",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "120"
          ]
        }
      ],
      "id": "M85",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0117]",
          "quote": "For example, a first input data structure can contain an instruction to generate a thorough analysis of query 104 in view of memory data 114. Output data structure 120 can contain the generated analysis."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M35",
      "figure_refs": [
        {
          "caption_quote": "Figure 1 is a block diagram that illustrates aspects of a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-1",
          "numerals": [
            "122",
            "124"
          ]
        }
      ],
      "id": "M86",
      "kind": "grounding",
      "spec_refs": [
        {
          "locator": "[0117]",
          "quote": "The raw outputs may not be surfaced to the user. For example, only a response 122 might be output to output interface(s) 124."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M36",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M87",
      "kind": "grounding",
      "search_note": "요약 [0020]이 통합(consolidating) 한정을 문언 그대로 조응한다. 도면은 방법 흐름도 FIG-21 에 귀속하며, 흐름도는 도면부호를 갖지 않아 numerals 를 빈 배열로 둔다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0020]",
          "quote": "In some implementations, the example method includes consolidating, in the interaction memory datastore, a subset of the plurality of memory objects into a single memory object based on an alignment between the subset."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M37",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M88",
      "kind": "grounding",
      "search_note": "[0021]과 [0022]에 같은 문장이 두 번 나온다. 이 항목은 CL-18 계열이므로 교체(replacing) 서사를 여는 [0021]을 인용했다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0021]",
          "quote": "In some implementations, the example method includes receiving input data associated with a timestamp."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M38",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M89",
      "kind": "grounding",
      "search_note": "타임스탬프·현재 메모리 값 두 하위 한정이 한 문단에 연속하므로 세 문장을 최소 단위로 함께 인용했다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0021]",
          "quote": "In some implementations, the example method includes creating a current memory object. In some implementations, the current memory object includes the timestamp. In some implementations, the current memory object includes a current memory value based on the input data."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M39",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M90",
      "kind": "grounding",
      "search_note": "FIG-21 은 도면부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0021]",
          "quote": "In some implementations, the example method includes matching the current memory object to a prior memory object."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M40",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M91",
      "kind": "grounding",
      "search_note": "FIG-21 은 도면부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0021]",
          "quote": "In some implementations, the example method includes replacing, in the interaction memory datastore, the prior memory object with the current memory object."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M41",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M92",
      "kind": "grounding",
      "search_note": "CL-19 계열이므로 갱신(updating) 서사를 여는 [0022]를 인용했다([0021]에 동일 문장이 있으나 그것은 CL-18 계열이다). FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0022]",
          "quote": "In some implementations, the example method includes receiving input data associated with a timestamp."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M42",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M93",
      "kind": "grounding",
      "search_note": "요약 [0022]와 상세 [0453]이 같은 한정을 조응한다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0022]",
          "quote": "In some implementations, the example method includes matching at least a portion of the input data to a prior memory object."
        },
        {
          "locator": "[0453]",
          "quote": "The system then matches at least a portion of the input data to a prior memory object"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M43",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M94",
      "kind": "grounding",
      "search_note": "상세 대응은 [0453]이고 갱신 사례 도면으로는 FIG-5 도 후보이나, 청구항 한정이 방법 단계이므로 방법 흐름도 FIG-21 에 귀속했다. 흐름도는 부호가 없어 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0022]",
          "quote": "In some implementations, the example method includes updating, in the interaction memory datastore, the prior memory object based on the portion of the input data."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M44",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M95",
      "kind": "grounding",
      "search_note": "응답 출력 단계의 상세는 [0454]에 있다. FIG-21 은 부호 없는 흐름도이므로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0023]",
          "quote": "In some implementations of the example method, the response includes instructions configured to control an application programming interface to cause a computing system to perform an action."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M45",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M96",
      "kind": "grounding",
      "search_note": "[0024] 한 문단이 두 한정(질의의 구성 파라미터 지시 / API 를 통한 값 배정)을 담으므로 조응이 보이는 최소 단위로 앞부분만 잘랐다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0024]",
          "quote": "the query indicates a configuration parameter that controls an operation of the computing system"
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M46",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M97",
      "kind": "grounding",
      "search_note": "[0024]의 뒷부분이 이 한정에 조응한다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0024]",
          "quote": "the instructions are configured to control the application programming interface to cause the computing system to assign a value for the configuration parameter."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M47",
      "figure_refs": [
        {
          "caption_quote": "Figure 21 is a flow chart diagram illustrating an example method for using a machine-learned agent system according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-21",
          "numerals": []
        }
      ],
      "id": "M98",
      "kind": "grounding",
      "search_note": "청구항의 3택 열거(접근·보존·통신)가 [0025]의 세 문장에 1:1 로 대응하므로 세 문장을 함께 인용했다. FIG-21 은 부호 없는 흐름도(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0025]",
          "quote": "In some implementations of the example method, the configuration parameter is associated with data access by the computing system. In some implementations of the example method, the configuration parameter is associated with data retention by the computing system. In some implementations of the example method, the configuration parameter is associated with data communication by the computing system."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M48",
      "figure_refs": [
        {
          "caption_quote": "Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-19",
          "numerals": []
        }
      ],
      "id": "M99",
      "kind": "grounding",
      "search_note": "매체 범주항의 도면 조응은 계산 장치 블록도(FIG-19)의 메모리·명령 요소다. 도면부호를 등재하면 그 정수가 수치 수확 정답지에서 배제되고 본문 부호와 도면 실물 부호의 일치를 이 조각만으로는 확인할 수 없으므로, numerals 를 빈 배열로 두고 캡션 인용으로 조응을 진다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0026]",
          "quote": "In an aspect, the present disclosure provides an example one or more non-transitory computer-readable media storing instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M49",
      "figure_refs": [
        {
          "caption_quote": "Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-19",
          "numerals": []
        }
      ],
      "id": "M100",
      "kind": "grounding",
      "search_note": "프로세서 구성요소는 FIG-19 의 계산 장치 블록도에 표현되어 있으나, M2064 와 같은 이유(수확 배제 확대 · 실물 부호 대조 불가)로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0027]",
          "quote": "In some implementations, the example computing system includes one or more processors."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "found",
        "spec": "found"
      },
      "component": "M50",
      "figure_refs": [
        {
          "caption_quote": "Figure 19 is a block diagram of an example computing device according to example implementations of aspects of the present disclosure.",
          "figure": "FIG-19",
          "numerals": []
        }
      ],
      "id": "M101",
      "kind": "grounding",
      "search_note": "메모리·명령 요소는 FIG-19 에 표현되어 있으나 M2064·M2065 와 같은 이유로 numerals 는 빈 배열이다(절차 §5 ⓒ).",
      "spec_refs": [
        {
          "locator": "[0027]",
          "quote": "In some implementations, the example computing system includes one or more non-transitory computer-readable media storing instructions that are executable by the one or more processors to cause the computing system to perform operations, the operations comprising any implementation of the example method."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "anchor_state": {
        "figure": "not-depicted",
        "spec": "found"
      },
      "component": "M51",
      "figure_refs": [],
      "id": "M102",
      "kind": "grounding",
      "search_note": "도면 캡션 전량(Figure 1~21)을 확인했으나 「컴퓨터 프로그램 제품」을 블록·요소로 그린 도면은 없다. FIG-19·FIG-20 은 장치와 응용/중앙 지능 층을 그릴 뿐 프로그램 제품 범주를 별도 요소로 표현하지 않는다.",
      "spec_refs": [
        {
          "locator": "[0028]",
          "quote": "In an aspect, the present disclosure provides an computer program product comprising instructions that are executable by one or more processors to cause a computing system to perform operations, the operations comprising any implementation of the example method."
        }
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "bib_source": {
        "field": "patent.number"
      },
      "id": "M103",
      "kind": "fact",
      "label_en": "bibliographic field patent.number",
      "machine_verifiable": true,
      "origin": "bibliographic",
      "status": "active",
      "superseded_by": null,
      "unit": null,
      "value_normalized": "WO2026-128750A1",
      "value_raw": "WO2026-128750A1",
      "value_type": {
        "approximate": false,
        "kind": "identifier",
        "value": "WO2026-128750A1"
      }
    },
    {
      "bib_source": {
        "field": "patent.dates.priority"
      },
      "id": "M104",
      "kind": "fact",
      "label_en": "bibliographic field patent.dates.priority",
      "machine_verifiable": true,
      "origin": "bibliographic",
      "status": "active",
      "superseded_by": null,
      "unit": null,
      "value_normalized": "2024-12-11",
      "value_raw": "2024-12-11",
      "value_type": {
        "approximate": false,
        "kind": "date",
        "value": "2024-12-11"
      }
    },
    {
      "bib_source": {
        "field": "patent.dates.filing"
      },
      "id": "M105",
      "kind": "fact",
      "label_en": "bibliographic field patent.dates.filing",
      "machine_verifiable": true,
      "origin": "bibliographic",
      "status": "active",
      "superseded_by": null,
      "unit": null,
      "value_normalized": "2025-12-11",
      "value_raw": "2025-12-11",
      "value_type": {
        "approximate": false,
        "kind": "date",
        "value": "2025-12-11"
      }
    },
    {
      "bib_source": {
        "field": "patent.dates.publication"
      },
      "id": "M106",
      "kind": "fact",
      "label_en": "bibliographic field patent.dates.publication",
      "machine_verifiable": true,
      "origin": "bibliographic",
      "status": "active",
      "superseded_by": null,
      "unit": null,
      "value_normalized": "2026-06-18",
      "value_raw": "2026-06-18",
      "value_type": {
        "approximate": false,
        "kind": "date",
        "value": "2026-06-18"
      }
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M59",
        "M68",
        "M81"
      ],
      "evidence_quotes": [
        "a memory object can be a data container that stores one or more memory values"
      ],
      "id": "M107",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "The memory is not a transcript but a set of structured containers, each holding a value plus metadata, so that recall can filter on attributes rather than re-reading raw history.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M58",
        "M60",
        "M61"
      ],
      "evidence_quotes": [
        "These audio recordings can capture rich contextual information that may be lost in the transcription"
      ],
      "id": "M108",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Storing memories in the modality in which they were received (audio, image) is meant to preserve context that a text transcription would discard.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M59",
        "M69",
        "M93"
      ],
      "evidence_quotes": [
        "new information can serve to refine and build more nuanced memories rather than noisily overcorrecting based on limited information"
      ],
      "id": "M109",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Keeping the supporting interactions alongside a memory value lets a later contradicting input refine the memory instead of simply overwriting it.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M73",
        "M74",
        "M72"
      ],
      "evidence_quotes": [
        "Memory objects exceeding their expiration time may be automatically deleted during scheduled maintenance operations."
      ],
      "id": "M110",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Timestamps and optional expiration times on memory objects are the mechanism by which forgetting after an interval is implemented during maintenance cycles.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M73",
        "M71"
      ],
      "evidence_quotes": [
        "the user can also use the same interaction mechanism to limit, erase, or otherwise modify the memory of the machine-learned agent system"
      ],
      "id": "M111",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Because the memory is built from conversation, the same conversational channel doubles as the control surface for erasing or limiting it.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "effects",
      "confidence": "stated",
      "derived_from": [
        "M64",
        "M70",
        "M66"
      ],
      "evidence_quotes": [
        "by pre-processing user interactions offline, the system can create high-quality memory data objects containing key features and metadata"
      ],
      "id": "M112",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Extracting memories offline from cached interactions is positioned as shifting compute away from query time, so runtime inference reads condensed objects rather than raw history.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M57",
        "M99",
        "M100"
      ],
      "evidence_quotes": [
        "response 122 can include an application programming interface call generated based on output data structure 120"
      ],
      "id": "M113",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "The response can itself be an API call, so recalled memory conditions actions taken on a device, not only text returned to the user.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "inferred",
      "derived_from": [
        "M64",
        "M67",
        "M71"
      ],
      "evidence_quotes": [
        "Runtime queries can be processed in full view of all retrieved memories."
      ],
      "id": "M114",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "The disclosure deliberately leaves open where conflict resolution happens: offline consolidation against existing memories, or at runtime with all retrieved memories in view.",
      "status": "active",
      "superseded_by": null
    },
    {
      "basis": "spec",
      "confidence": "stated",
      "derived_from": [
        "M75",
        "M82",
        "M78"
      ],
      "evidence_quotes": [
        "This ordering allows the machine-learned agent system to prioritize more recent context when making inferences."
      ],
      "id": "M115",
      "kind": "implication",
      "numeric_refs": [],
      "statement_en": "Ordering recalled values by timestamp is how recency is communicated to the model for resolving conflicting memories.",
      "status": "active",
      "superseded_by": null
    },
    {
      "asserted_effect": "The specification asserts that a user-specific, agent-curated interaction memory lets a task start from a single interaction, supports asynchronous execution of previously instructed tasks, reduces runtime load by pre-processing memories offline, and gives the user control over what is remembered and forgotten.",
      "background_problem": "Agents without memory force users to re-enter the same details across sessions, and the alternative of wiring the agent to external data sources gives the user an all-or-nothing access choice with data the agent does not curate.",
      "delta": "No performance numbers are given; the claimed difference is structural: memory objects generated from prior interactions with the user, retrieved by relevance and fed into a sequence model input, rather than raw history or uncurated external sources.",
      "id": "M116",
      "kind": "positioning",
      "numeric_refs": [],
      "quotes": [
        "the user may be faced with an all-or-nothing choice, which may be undesirable in some circumstances",
        "can initiate execution with a single interaction"
      ],
      "status": "active",
      "superseded_by": null
    },
    {
      "figure": "FIG-1",
      "id": "M117",
      "kind": "figure_note",
      "numerals": [
        "102",
        "104",
        "105",
        "106",
        "108",
        "110",
        "114",
        "116",
        "118",
        "120",
        "122",
        "124"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Overall agent pipeline from input interfaces and query through the memory model, recall cycle, datastore query and response, memory data, input data structure, model system, output data structure, response, and output interfaces."
    },
    {
      "figure": "FIG-2",
      "id": "M118",
      "kind": "figure_note",
      "numerals": [
        "110",
        "202-1",
        "204-1",
        "206-1"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Structure of the interaction memory datastore as a set of memory objects, each holding memory values and memory metadata."
    },
    {
      "figure": "FIG-3",
      "id": "M119",
      "kind": "figure_note",
      "numerals": [
        "302",
        "304",
        "306",
        "308"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Example recall cycle in which three retrieved memory objects are condensed into memory data for the model input."
    },
    {
      "figure": "FIG-7",
      "id": "M120",
      "kind": "figure_note",
      "numerals": [
        "702"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Communication sequence in which a trigger starts a memory update cycle before a later query drives a recall cycle and model inference."
    },
    {
      "figure": "FIG-8",
      "id": "M121",
      "kind": "figure_note",
      "numerals": [
        "802",
        "804",
        "806"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Memory update cycle in which cached inputs are sent to the model system, memory data updates are returned, and a memory data write is executed."
    },
    {
      "figure": "FIG-10",
      "id": "M122",
      "kind": "figure_note",
      "numerals": [
        "1002",
        "804"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Memory maintenance cycle in which a memory update request with current memory data drives the model to produce memory data updates independent of new input."
    },
    {
      "figure": "FIG-13",
      "id": "M123",
      "kind": "figure_note",
      "numerals": [
        "4",
        "6"
      ],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Generic sequence processing model that turns inputs into an input sequence and uses prediction layers to emit an output sequence."
    },
    {
      "figure": "FIG-19",
      "id": "M124",
      "kind": "figure_note",
      "numerals": [],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Example computing device in which each application carries its own machine learning library and models and talks to device components through an API."
    },
    {
      "figure": "FIG-21",
      "id": "M125",
      "kind": "figure_note",
      "numerals": [],
      "status": "active",
      "superseded_by": null,
      "what_it_shows_en": "Flowchart of the claimed method: receive query, access memory data, input data structure to sequence model, generate output, output response."
    }
  ],
  "patent": {
    "applicants": [
      "GDM HOLDING LLC"
    ],
    "assignee": "GDM HOLDING LLC",
    "classifications": {
      "cpc": [
        "G06F 16/41"
      ],
      "ipc": [
        "G06F 16/41"
      ]
    },
    "dates": {
      "filing": "2025-12-11",
      "priority": "2024-12-11",
      "publication": "2026-06-18"
    },
    "inventors": [
      "HASSABIS, Demis",
      "THOTA, Chandrasekhar",
      "CHI, Ed Huai-hsin",
      "WAYNE, Gregory Duncan"
    ],
    "jurisdiction": "WO",
    "kind_code": "A1",
    "number": "WO2026-128750A1",
    "priority_claims": [
      {
        "date": "2024-12-11",
        "jurisdiction": "US",
        "number": "63/730,845"
      }
    ],
    "source_digest": "sha256:64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e",
    "source_path": "00-source/patent.md",
    "title": "DYNAMIC INTERACTION MEMORY DATASTORE FOR MACHINE-LEARNED AGENT SYSTEMS"
  },
  "provenance": {
    "engine_commit": "eb884936425687c5053cb40556f39a49a5f29952",
    "produced_at": "2026-09-13T05:41:04Z",
    "read_runs": [
      "read-a:canonical",
      "read-b:convergence-peer"
    ]
  },
  "reader_version": "0.9.0",
  "review_requests": [
    {
      "reason": "매체항이 「the method of any of the preceding claims」로 방법항 CL-1~CL-22 를 되받는다고 읽어 all-preceding 으로 두었다(T13) — Owner 가 이 인용 범위(CL-22 까지) 를 확인하면 판가름난다.",
      "target": "CL-23"
    },
    {
      "reason": "선행 청구항에 매체항 CL-23 이 있으나 「the method of」 이므로 CL-23 을 depends_on 에서 뺐다 — 이 배제가 맞는지 Owner 가 보면 판가름난다.",
      "target": "CL-24"
    },
    {
      "reason": "CL-24 와 같은 이유로 CL-23·CL-24 를 인용 범위에서 뺐다 — 방법항만 인용한다는 독해의 확인이 필요하다.",
      "target": "CL-25"
    },
    {
      "reason": "「the one or more memory values」 는 CL-1 에 선행 도입이 없어(CL-1 은 memory objects·memory data 만 든다) 부착점을 CL-1/e2 로 두었다 — 선행사 결여를 Owner 가 어떻게 볼지에 따라 부착점이 달라진다.",
      "target": "CL-4"
    },
    {
      "reason": "「the plurality of memory objects」·「the one or more memory values」 모두 CL-1 에 선행사가 없다 — 부착점 CL-1/e2 가 맞는지, 선행사 결여를 결함으로 기록할지 Owner 판단이 필요하다.",
      "target": "CL-11"
    },
    {
      "reason": "출력을 모델에 되먹이는 단계를 응답 산출(CL-1/e5) 밑에 두었으나 출력 생성(CL-1/e4) 밑도 가능하다 — 재귀 단계가 어느 요소를 한정하는지 Owner 가 보면 판가름난다.",
      "target": "CL-15/a1"
    },
    {
      "reason": "「based on … to be stored:」 조건절을 독립 addition 으로 쪼갰다(평면 분할 ⓑ) — 순수 연결구로 보아 a3·a4 에 흡수해야 한다면 경계가 달라진다.",
      "target": "CL-5/a2"
    },
    {
      "reason": "CL-13/a2 의 「second machine-learned sequence processing model」이 도면상 별개 블록으로 표현되지 않는다 — FIG-13 의 모델 4·예측층 6 을 부호로 들었으나 이것이 「두 번째」 모델인지는 도면으로 판가름나지 않는다. [0447] 문언과 FIG-13 을 함께 보아 부호 부착의 타당성을 확인해 주기 바란다.",
      "target": "M80"
    },
    {
      "reason": "CL-5/a3 「extracting the portion」의 조응으로 [0088] 을 들었으나 이 문단은 추출을 「remember 할 내용의 발췌 예측」으로 서술해 청구항 어형과 다르다. [0439] 의 재서술이 더 가까울 수 있어 어느 쪽을 정본 인용으로 둘지 판단을 요청한다.",
      "target": "M66"
    },
    {
      "reason": "컴퓨터 프로그램 제품(CL-25)을 도면 미표현으로 신고했으나, FIG-19·FIG-20 의 응용/명령 블록을 그 조응으로 볼 여지가 있다 — 두 도면 실물의 블록 표기를 보면 not-depicted 유지 여부가 판가름난다.",
      "target": "M102"
    },
    {
      "reason": "범주항 3건(CL-23·CL-24·CL-25)은 방법 한정이 아니라 청구 범주 전환이라 도면 자리가 관례적이다 — 장치 도면(FIG-19)에 붙이는 것이 맞는지 도면 예외로 두는 것이 맞는지 Owner 가 한 번 정해 주면 M2065·M2066·M2067 이 같은 기준으로 정렬된다.",
      "target": "M99"
    },
    {
      "reason": "FIG-8 방식(기존 기억 미참조)과 FIG-9 방식(기존 기억 참조)을 「의도적으로 열어 둔 선택」으로 읽었는데, 명세서는 두 접근의 장단만 나열할 뿐 선택을 열어 둔다고 명시하지 않으므로 [0291]을 보고 inferred 유지 여부를 판가름해 달라.",
      "target": "M114"
    }
  ],
  "run_id": "gdm-wo2026128750a1-agent-memory-3",
  "schema": "material-spec/v0",
  "spec_version": 1,
  "status": "frozen"
}
```

### `20-design/blueprint.json`

```text
{
  "escalation": null,
  "figure_plan": [
    {
      "figures": [
        "FIG-1"
      ],
      "intent_kr": "전체 파이프라인 한 장 — 질의에서 응답까지의 루프 속에 기억 데이터스토어(110)가 별도 블록으로 들어 있음을 보인다. 독립항 다섯 단계가 이 도면에 그대로 접지된다.",
      "tweet": 1
    },
    {
      "figures": [
        "FIG-2"
      ],
      "intent_kr": "데이터스토어 내부 — 메모리 객체(202-1)가 값(204-1)과 메타데이터(206-1)를 담는 컨테이너 구조임을 보인다. 「대화 기록이 아니라 구조화된 객체」의 시각적 근거.",
      "tweet": 2
    },
    {
      "figures": [
        "FIG-8",
        "FIG-7"
      ],
      "intent_kr": "FIG-8 = 기억 갱신 사이클(캐시 입력 802 → 갱신 804 → 쓰기 806)로 「모델이 저장 여부를 판단하고 쓴다」를 보인다. FIG-7 = 트리거(702)가 갱신 사이클을 먼저 열고 나중 질의가 회상 사이클을 여는 순서.",
      "tweet": 3
    },
    {
      "figures": [
        "FIG-3"
      ],
      "intent_kr": "회상 사이클 예시 — 검색된 메모리 객체 셋(302·304·306)이 메모리 데이터(308)로 압축되는 모습. 「전부 다시 읽지 않고 관련 부분집합만」의 근거.",
      "tweet": 4
    },
    {
      "figures": [
        "FIG-21"
      ],
      "intent_kr": "청구 방법 흐름도 — 교체·갱신·통합 단계는 부호 없는 방법 흐름도에 귀속되어 있으므로 이 도면을 지정한다. 정정이 방법 단계로 청구되었음을 보이는 자리.",
      "tweet": 5
    },
    {
      "figures": [
        "FIG-10"
      ],
      "intent_kr": "기억 유지 사이클 — 새 입력 없이 갱신 요청(1002)만으로 모델이 갱신(804)을 내는 구조. 망각·만료가 별도 유지 사이클로 도는 결정적 물증(피벗).",
      "tweet": 6
    },
    {
      "figures": [
        "FIG-1"
      ],
      "intent_kr": "FIG-1 의 오른쪽 절반(출력 구조 120 → 응답 122 → 출력 인터페이스 124)을 다시 가리켜 「숨은 분석은 120 에 머물고 122 만 밖으로 나가며 그것이 API 호출일 수 있다」를 보인다.",
      "tweet": 7
    },
    {
      "figures": [
        "FIG-1"
      ],
      "intent_kr": "첫 트윗의 도면으로 되돌아오는 북엔드 — 각 스톱에서 확대한 부품이 한 루프로 닫힘을 보이며 인용·스크린샷 표적이 되게 한다.",
      "tweet": 8
    },
    {
      "figures": [],
      "intent_kr": "꼬리 — 도면 없음. 링크와 팔로우만.",
      "tweet": 9
    }
  ],
  "hook": {
    "figure": "FIG-1",
    "question_en": "When an AI agent says it \"remembers\" you, is that a real architecture or just a marketing word?",
    "rationale_kr": "투자자-팬의 불안은 「에이전트 기억」이 실체 있는 구조인지 구호인지다(D3). FIG-1 은 질의(104)→기억 모델(105)→데이터스토어(110)→메모리 데이터(114)→입력 구조(116)→모델(118)→응답(122)까지 한 장에 루프 전체를 그리고 독립항 CL-1(M1~M6) 다섯 단계가 그대로 이 도면에 접지된다(M52~M57·M117). 스레드 전체가 이 한 장의 부품을 하나씩 확대하는 구성이므로 최강 도면이다.",
    "thesis_en": "This GDM Holding filing, with Demis Hassabis among the named inventors, claims a per-user datastore of curated memory objects that the model reads at every query, writes by itself, and erases when you ask."
  },
  "lane": {
    "effort": "high",
    "lane_id": "design/blueprint/batch-0",
    "model": "claude-fable-5-1"
  },
  "law_commit": "d8b4fb307ef0229f1aee47bc32d948cf1de15c7f",
  "new_terms": [
    {
      "gloss_en": "A per-user store of memory objects built from prior conversations with the agent.",
      "term_en": "interaction memory datastore",
      "tweet": 1
    },
    {
      "gloss_en": "A container holding one or more memory values plus metadata such as a timestamp and the trigger that stored it.",
      "term_en": "memory object",
      "tweet": 2
    },
    {
      "gloss_en": "The pass in which cached inputs are sent to the model, which decides what to store and writes it.",
      "term_en": "memory update cycle",
      "tweet": 3
    },
    {
      "gloss_en": "The pass in which stored objects are scored for relevance to a query and a subset is condensed into memory data for the model.",
      "term_en": "recall cycle",
      "tweet": 4
    },
    {
      "gloss_en": "An optional time on a memory object after which it is deleted during maintenance.",
      "term_en": "expiration time",
      "tweet": 6
    }
  ],
  "numeric_whitelist": [
    {
      "pattern": "\\b[1-9]/[1-9]\\b",
      "rationale": "Thread position marker n/N; the only number allowed that is not in the frozen material."
    }
  ],
  "overflow_proposal": null,
  "run_id": "gdm-wo2026128750a1-agent-memory-3",
  "schema": "blueprint/v0",
  "slots": [
    {
      "exhibit": {
        "material_ids": [
          "M1",
          "M2",
          "M3",
          "M4",
          "M5",
          "M6",
          "M53",
          "M117"
        ],
        "point_en": "The independent claim is a five-step loop: receive a query, pull memory data from a datastore built from this user's past interactions, feed query plus memory into a sequence model, generate an output, and answer. Memory is a separate box in the diagram, not a longer prompt."
      },
      "figures": [
        "FIG-1"
      ],
      "n": 1,
      "slot": "hook"
    },
    {
      "exhibit": {
        "material_ids": [
          "M3",
          "M17",
          "M30",
          "M54",
          "M68",
          "M81",
          "M107",
          "M118"
        ],
        "point_en": "What sits in that box is not a transcript. Each memory object is a container holding a memory value (a string, image, or audio) plus metadata such as a timestamp, the trigger that stored it, and a summary of the conversation it came from."
      },
      "figures": [
        "FIG-2"
      ],
      "n": 2,
      "slot": "stop"
    },
    {
      "exhibit": {
        "material_ids": [
          "M13",
          "M14",
          "M15",
          "M16",
          "M19",
          "M64",
          "M65",
          "M66",
          "M67",
          "M70",
          "M112",
          "M120",
          "M121"
        ],
        "point_en": "Who decides what gets stored? A model does. Cached inputs are sent to the model system, which predicts whether anything is worth remembering, extracts that portion, and writes it as a memory object; an explicit \"remember this\" from the user is one trigger, and the write can happen offline rather than at query time."
      },
      "figures": [
        "FIG-8",
        "FIG-7"
      ],
      "n": 3,
      "slot": "stop"
    },
    {
      "exhibit": {
        "material_ids": [
          "M12",
          "M24",
          "M26",
          "M27",
          "M28",
          "M63",
          "M75",
          "M77",
          "M78",
          "M79",
          "M115",
          "M119"
        ],
        "point_en": "At query time the agent does not reread everything. It scores stored objects by relevance to the query, using embedding distance such as cosine similarity, returns a top subset, and orders the values by timestamp so the model sees recency."
      },
      "figures": [
        "FIG-3"
      ],
      "n": 4,
      "slot": "stop"
    },
    {
      "exhibit": {
        "material_ids": [
          "M36",
          "M39",
          "M40",
          "M42",
          "M43",
          "M87",
          "M90",
          "M91",
          "M93",
          "M94",
          "M109",
          "M125"
        ],
        "point_en": "Memories can be corrected. New timestamped input is matched to a prior memory object and either replaces it or updates it, and aligned objects can be consolidated into one, so contradicting information refines a memory instead of noisily overwriting it."
      },
      "figures": [
        "FIG-21"
      ],
      "n": 5,
      "slot": "stop"
    },
    {
      "exhibit": {
        "material_ids": [
          "M20",
          "M21",
          "M22",
          "M23",
          "M71",
          "M72",
          "M73",
          "M74",
          "M110",
          "M111",
          "M122"
        ],
        "point_en": "The decisive detail: forgetting is claimed, not just remembering. \"Forget that\" deletes the specified information from the datastore, \"forget this after three months\" queues it for deletion after the interval, and expired objects are removed during maintenance cycles. The same chat that builds the memory is the control surface for erasing it."
      },
      "figures": [
        "FIG-10"
      ],
      "n": 6,
      "slot": "pivot"
    },
    {
      "exhibit": {
        "material_ids": [
          "M34",
          "M35",
          "M44",
          "M85",
          "M86",
          "M113"
        ],
        "point_en": "What the memory is for: the model first generates a hidden analysis of the query against the memory data that is never shown on screen, and the final response can be an API call that makes the device perform an action, so recalled memory conditions what the agent does, not only what it says."
      },
      "figures": [
        "FIG-1"
      ],
      "n": 7,
      "slot": "stop"
    },
    {
      "exhibit": {
        "material_ids": [
          "M116",
          "M3",
          "M12",
          "M21",
          "M40"
        ],
        "point_en": "No benchmark numbers are claimed, and the filing says so by omission. What is claimed is a structural difference: memory objects generated from your own interactions, retrieved by relevance, corrected over time, and erased on request. That is a described architecture, not a slogan."
      },
      "figures": [
        "FIG-1"
      ],
      "n": 8,
      "slot": "landing"
    },
    {
      "exhibit": {
        "material_ids": [
          "M103",
          "M104",
          "M106"
        ],
        "point_en": "Pointer to the publication WO2026-128750A1 (priority 2024, published 2026) and an invitation to follow for the next patent walk-through."
      },
      "figures": [],
      "n": 9,
      "slot": "tail"
    }
  ],
  "spec_digest": "sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407",
  "spec_version": 1,
  "transmission_targets": [
    "M3",
    "M16",
    "M12",
    "M21",
    "M23",
    "M40",
    "M116"
  ]
}
```

### `30-figures/assets/manifest.json`

```text
{
  "items": [
    {
      "asset_id": "fig-01",
      "asset_path": "30-figures/assets/fig-01.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-1",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:08ab5032979456b5ba5b0726f3be6d081b3de139d4b6c6b45b864d78c45c287a",
      "source_raw_path": "00-source/figures-raw/fig-01.png",
      "source_sha256": "sha256:7fae4a6d92c033d248834e953ef85f2862a74d324ce9500c4fb7bad1e08104d5",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-02",
      "asset_path": "30-figures/assets/fig-02.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-2",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:9dfe4df527048d0c2d8a5f543d9fd7787f4b0d8ffbd5b6c66b4d3085a5ad3aff",
      "source_raw_path": "00-source/figures-raw/fig-02.png",
      "source_sha256": "sha256:882555daab66d95f1273e6d2edb3e651b3c8b3b903eef2fa94d8f4dffb0f90fd",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-03",
      "asset_path": "30-figures/assets/fig-03.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-3",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:42985156c2600589250c5fd7acb78e2fa88e2d44896a3cba3b8ff403582debb7",
      "source_raw_path": "00-source/figures-raw/fig-03.png",
      "source_sha256": "sha256:9e69b8df96a278ee6372bfd6359d6b389d4f640d2fa04c216f4295f29f842955",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-07",
      "asset_path": "30-figures/assets/fig-07.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-7",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:c8664d29c24aa55c975fcde31159a3b1b9faf3ae874c4df2f294cec59dc3e394",
      "source_raw_path": "00-source/figures-raw/fig-07.png",
      "source_sha256": "sha256:ddfc822e61182c1e0db9bfc687eda089a746e3b5a43503d7f69b64e98c0af5ec",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-08",
      "asset_path": "30-figures/assets/fig-08.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        },
        {
          "basis": "source-report#figures[figure_number]",
          "from": "00-source/figures-raw/fig-08.png",
          "note": "동결본 raw_path 가 실재하지 않아 source-report 도면 번호 유일 일치 파일로 해소(재정 T66 ①) · 재료 무변경",
          "op": "raw-path-resolved",
          "to": "00-source/figures-raw/fig-08-09.png"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-8",
      "publishable": true,
      "rendered_at": "2026-09-13T12:12:39Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:5849f47075f6bcdac8fd33b91a2cc9177d594b7664b1deab5d816b95e006e979",
      "source_raw_path": "00-source/figures-raw/fig-08-09.png",
      "source_sha256": "sha256:d024d979092ae9be39735040104a242b0e6e9da26622825b880d87f28df402f3",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-10",
      "asset_path": "30-figures/assets/fig-10.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-10",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:eb13c1461a1ed83408ed8fbd41868b582dc3dc85d2a7b08e0805bcae40d2623e",
      "source_raw_path": "00-source/figures-raw/fig-10.png",
      "source_sha256": "sha256:2e795a6783df746ae1b6633d91ebfc9bbf77c172d9c20fb2c3be38a8de120046",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-13",
      "asset_path": "30-figures/assets/fig-13.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-13",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:081e0d63ba3fa94d291ae6ff5f1db83a3c64ab5181ce35a4bf1f1ff1f12f1fb2",
      "source_raw_path": "00-source/figures-raw/fig-13.png",
      "source_sha256": "sha256:2d74c5f3ea43d45d288b9e45e90ce13c0f8a87deb38a1c8639f7a4a9bcc982be",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-19",
      "asset_path": "30-figures/assets/fig-19.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        },
        {
          "basis": "source-report#figures[figure_number]",
          "from": "00-source/figures-raw/fig-19.png",
          "note": "동결본 raw_path 가 실재하지 않아 source-report 도면 번호 유일 일치 파일로 해소(재정 T66 ①) · 재료 무변경",
          "op": "raw-path-resolved",
          "to": "00-source/figures-raw/fig-19.jpg"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-19",
      "publishable": true,
      "rendered_at": "2026-09-13T12:12:39Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:e405072e8c2c249316fc86f8c79c0057419b65c6c78007a71a5dcfdf91a58b21",
      "source_raw_path": "00-source/figures-raw/fig-19.jpg",
      "source_sha256": "sha256:6ffd5fe3e3c2b1e900c729cb6dfac9b9f0fb62fd559ab150a69e2d727d1f2816",
      "template": "crop-only/v0"
    },
    {
      "asset_id": "fig-21",
      "asset_path": "30-figures/assets/fig-21.png",
      "edit_class": "crop-only",
      "edits": [
        {
          "note": "전장 프레이밍 · 오버레이 없음",
          "op": "crop-only-framing",
          "template": "crop-only/v0"
        }
      ],
      "fallback": true,
      "figure_id": "FIG-21",
      "publishable": true,
      "rendered_at": "2026-09-13T11:52:14Z",
      "renderer": "playwright-chromium-1148",
      "sha256": "sha256:868d84a1657f28e83c36b5e68edefb17c8edd51bea8571dcddfcfbcb71d4fc5b",
      "source_raw_path": "00-source/figures-raw/fig-21.png",
      "source_sha256": "sha256:da7888f92b14ed91ca48df927b034b1b7103e06f0a1790a395ec08227e6f417c",
      "template": "crop-only/v0"
    }
  ],
  "renderer": {
    "browser": "chromium-1148",
    "channel": "chromium",
    "device_scale_factor": 2,
    "engine": "playwright-chromium",
    "playwright": "1.49.1",
    "viewport": [
      1200,
      675
    ]
  },
  "run_id": "gdm-wo2026128750a1-agent-memory-3",
  "schema": "figures-manifest/v0",
  "spec_digest": "sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407",
  "spec_version": 1
}
```

### `30-figures/selection.json`

```text
{
  "blueprint_digest": "sha256:b0560db9485a826aca07e9caf2e1095921d331331ad20ab282bd402fb08b5846",
  "run_id": "gdm-wo2026128750a1-agent-memory-3",
  "schema": "figures-selection/v0",
  "slots": [
    {
      "asset": "fig-01",
      "role": "hero",
      "tweet": 1
    },
    {
      "asset": "fig-02",
      "role": "exhibit",
      "tweet": 2
    },
    {
      "asset": "fig-08",
      "role": "exhibit",
      "tweet": 3
    },
    {
      "asset": "fig-07",
      "role": "exhibit",
      "tweet": 3
    },
    {
      "asset": "fig-03",
      "role": "exhibit",
      "tweet": 4
    },
    {
      "asset": "fig-21",
      "role": "exhibit",
      "tweet": 5
    },
    {
      "asset": "fig-10",
      "role": "exhibit",
      "tweet": 6
    },
    {
      "asset": "fig-01",
      "role": "exhibit",
      "tweet": 7
    },
    {
      "asset": "fig-01",
      "role": "exhibit",
      "tweet": 8
    }
  ],
  "spec_digest": "sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407",
  "spec_version": 1
}
```

### `40-compose/v2/thread.annotated.md`

```text
---
run_id: gdm-wo2026128750a1-agent-memory-3
variant: v2
pen: { vendor: anthropic, model: opus-5, effort: xhigh }
spec_version: 1
spec_digest: sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407
---

## T1 {slot: hook, fig: fig-01}
When an AI agent says it "remembers" you, is that architecture or marketing?[narrative]
Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response.[M1,M2,M3,M4,M5,M6,M116]

## T2 {slot: stop, fig: fig-02}
This datastore is not a transcript of your chats.[M107,M118]
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.[M17,M30,M68,M81]

## T3 {slot: stop, fig: fig-08+fig-07}
A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.[M13,M14,M15,M64,M65,M66,M121]
It is stored as a memory value in a memory object, and one trigger is you asking the agent to remember your favorite architect.[M16,M19,M67,M70,M120]

## T4 {slot: stop, fig: fig-03}
At query time the agent does not reread everything; it ranks stored objects by relevance to your query.[M12,M26,M63,M77]
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.[M24,M27,M28,M75,M78,M79,M115,M119]

## T5 {slot: stop, fig: fig-21}
Memories are corrected: new timestamped input is matched to the prior memory object it concerns, which is then replaced or updated.[M39,M40,M42,M43,M90,M91,M93,M94]
Aligned objects can be consolidated into one, and a contradiction refines the matched memory rather than overcorrecting it.[M36,M87,M109]

## T6 {slot: pivot, fig: fig-10}
Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.[M20,M21,M22,M23,M71,M72,M73]
Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.[M74,M110,M111,M122]

## T7 {slot: stop, fig: fig-01}
The model first works through your query against the recalled memory data, and that working-out can stay off the screen.[M34,M35,M85,M86]
What comes back can be an API call that makes a device act, so the memory shapes what the agent does, not only what it says.[M44,M113]

## T8 {slot: landing, fig: fig-01}
No performance numbers are given.[M116]
What is claimed is structural: memory objects made from your interactions, some on your explicit request, retrieved by relevance, corrected over time, and deleted when you ask.[M3,M12,M19,M21,M40]
That is a described architecture, not a slogan.[M116]

## T9 {slot: tail, fig: none}
The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.[M103,M104,M106]
Follow along for the next patent walk-through.[narrative]
```

### `50-gate/v2/revisions/r2/directives.json`

```text
{
  "directives": [
    {
      "fix_directive": "T5/S1 의 타임스탬프 한정에 그것을 담지하는 M37·M41 을 인용에 더하거나, 그 한정을 걷어내고 인용 항목이 실제로 담지하는 대조·교체·갱신만 남겨 재서술하라.",
      "id": "d-l1-001",
      "layer": "l1",
      "locus": {
        "sentence": 1,
        "tweet": 5
      },
      "rule": "l1.citation-mismatch"
    }
  ],
  "final_eyes_brief_digest": "sha256:2fc300843299c85694e3fa2026a4e363e3b12696037970fd49670c383dfc2db8",
  "round": 2,
  "thread_digest": "sha256:9701fec17daf420f5b5d1f1c7656971f40b9e7e28fae60a55f75bcbe0d2ccb84"
}
```

## 절차 (정본 = engine/pens/prompt-template.md)

# 펜 절차 — `compose/<variant>`

정본 서술 = `docs/SPEC.md` §1.9(직무·주석층 작성 의무·재료 반려) · §3.2(주석 문법) · `docs/CHARTER.md` D1·D2·D3·D8·D11. 이 문서는 요청서에 인라인되어 펜이 읽는 절차이며, 산문은 KR 이고 값·필드·예문은 EN 이다. 이 문서는 긍정형만 담는다(D8).

## 1. 정체성 (D1)

patent-docent = 단일 특허 심층 독해 → 일반 대중용 무료 X 스레드(EN) 엔진.

도슨트 비유: 관람객을 미술사학자로 만들려 하지 않고, 작품 앞의 10분을 만족스럽게 만든다.

너는 그 도슨트다. 네 앞에 있는 것은 요청서의 「원천 조각」 절에 실린 동결 재료(`material-spec.v<N>.json`)와 블루프린트(`blueprint.json`)뿐이며, 네가 아는 사실의 우주는 재료의 `items[]` 가 전부다. 그 안의 ID(`M<n>`)만이 네가 쓸 수 있는 좌표다.

## 2. 독자 (D2)

독자는 학습자가 아니라 **투자자-팬**이다. 독자가 원하는 것:

1. 이해한 것 같은 느낌
2. 그로부터 오는 안도감
3. 남에게 보여주고 싶은 큐레이션 가치

따라서 최적화 대상은 교육의 성공이 아니라 **공유 충동**이다.

## 3. 논지 (D3)

「투자자의 질문에, 기술로 답한다.」

훅은 투자자-팬의 질문에 조응한다. 본문의 답은 특허 물증에 근거한 기술 서사다 — 예: "HBF는 마케팅 용어가 아니라 실제 준비 중인 기술이다"까지 말하고 멈춘다. 금융 용어·티커(`$XXX`)·주가·시장 사실의 서술은 훅의 직무다. 투자 결론은 독자가 스스로 내린다.

## 4. 용어 (재정 N2)

각 전시 스톱은 구성요소 하나를 다룬다. 그 구성요소를 설명하는 데 필요한 새 용어는 등장한 자리에서 한 줄로 풀어준다. 풀이 없는 용어를 쌓지 않는다.

블루프린트의 `new_terms[]` 는 설계가 남긴 작업 메모다 — 어느 트윗에서 어떤 용어를 한 줄로 풀지의 제안이며, 최종 판단은 너의 것이다.

## 5. 주석 문법 (SPEC §3.2)

초안은 **주석층이 붙은 마크다운** 한 편이다. 아래 형태 그대로 쓴다.

```
---
run_id: openai-us20260147854a1-cim-fp
variant: v2
pen: { vendor: anthropic, model: opus-5, effort: max }
spec_version: 1
spec_digest: sha256:...
---

## T1 {slot: hook, fig: fig-03}
Sentence one of the hook.[M12]
A framing sentence with no factual load.[narrative]

## T2 {slot: stop, fig: fig-07}
...
```


⑴ **프런트매터** — YAML. 5키 정확히: `run_id` · `variant` · `pen: {vendor, model, effort}` · `spec_version` · `spec_digest`. 값은 요청서의 「런 표지」 표에 있는 것을 **그대로** 옮겨 적는다. `spec_digest` 는 네가 어느 재료를 보고 썼는지의 물증이다.

⑵ **트윗 헤더** — `## T<n> {slot: <slot>, fig: <figspec>}`. `n` 은 1부터 이어지는 연속 정수다. `slot` 은 요청서 「시트 값」 표의 `slot_enum` 값 중 하나다. `fig` 는 `fig-NN` 을 `+` 로 잇거나(`fig-03+fig-04`) `none` 이다. 중괄호 안의 공백은 콤마 뒤 1칸이다.

⑶ **문장 하나 = 줄 하나.** 트윗 본문의 각 문장은 자기 줄에 선다. 트윗 안의 줄들은 붙어 있고, 트윗과 트윗 사이에 빈 줄 하나가 온다.

⑷ **인용 태그** — 문장마다 태그 정확히 1개. 문장 종결부호 바로 뒤, 줄 끝에 온다. 문법은 `[M3,M7]`(재료 ID 를 콤마로만 잇는다) 또는 `[narrative]` 이다. 태그 안은 콤마만 있고, 태그 앞은 종결부호가 곧바로 온다 — `Text.[M1]`.

⑸ **대괄호 이스케이프** — 본문에 리터럴 `[` 가 필요하면 `\[` 로 적는다. 출하본에서 복원된다.

## 6. `[narrative]` 의 뜻 (SPEC §3.4)

`[narrative]` 는 **"이 문장은 근거가 필요 없는 서사 조직이다"** 라는 너의 자기 신고다. 전환·호명·질문 던지기·리듬 문장이 여기 속한다. 도슨트 문체에서 이런 문장은 필수적이며, 모든 문장에 재료를 강제하면 글이 목록이 된다. 기술 주장은 재료 ID 로 인용한다 — 한 문장이 재료의 사실을 말하면 그 문장의 태그는 그 재료 항목의 ID 다.

## 7. 슬롯 아크와 길이 감각 (D11 ③)

스레드는 훅 → 전시 스톱들(반전 포함) → 착지 → 꼬리의 아크를 따른다. 훅 = 투자자의 질문 + 최강 도면(스레드의 성패 그 자체) · 전시 스톱 = 전시물 하나의 제시 · 반전 스톱 = 질문에 답하는 결정적 물증 · 착지 = 안도감 결론(인용·스크린샷의 표적) · 꼬리 = 링크·팔로우.

트윗의 순서·슬롯·전시 재료는 블루프린트 `slots[]` 가 정했다. 각 슬롯의 길이 범위(가중 글자 수)와 트윗 수의 범위는 요청서의 「시트 값」 표가 든다. 한 트윗은 맥락 없이 단독으로도 읽힌다(알고리즘은 중간 트윗을 홀로 노출한다).

## 7a. 도면 헤더 (SPEC §1.8 · §3.2 · 재정 N3)

도면은 선택 파일(`30-figures/selection.json`)이 트윗마다 정해 두었고, 요청서의 「도면 헤더」 표가 그것을 트윗별 자산 id(`fig-NN`)로 편다. 각 트윗 헤더의 `fig` 에는 그 표의 자산 id 를 `+` 로 이어 적는다(그 트윗에 배정된 자산이 없으면 `none`). 자산 하나는 원본 도면 하나의 전장 프레이밍이며 그 원본(`FIG-n`)은 표의 「원본 도면」 열에 있다 — 문장이 도면을 가리킬 때 그 도면의 `figure_note` 재료를 인용하면 헤더와 본문이 같은 그림을 본다. 전시 스톱과 반전 스톱은 본문을 두 문장으로 쓴다(시트 `stop_shape.sentences_max`) — 도면이 말하고 문장은 짚는다. 요청서에 「도면 헤더」 표가 없는 판에서는 모든 `fig` 가 `none` 이다.

## 8. 재료 반려 (SPEC §1.9 · D6 규율 ②)

재료 결함 — 사실 오류 · 접지 불가 · 필요한 사실 부재 — 을 만나면 초안 대신 **반려서**를 낸다. 반려서는 4필드다: `material_ids`(문제가 된 항목 ID 목록) · `defect_kind`(`factual-error` | `unresolvable-grounding` | `missing-fact`) · `evidence`(재료 **내부**의 모순 지점 — 너는 원천을 볼 수 없으므로 근거는 재료 안에서 든다) · `blocked_slots`(이 결함 때문에 쓸 수 없는 블루프린트 슬롯 번호). 재료 명세는 독해 스테이지가 개정한다 — 펜의 손은 재료에 닿지 않는다.

## 9. 국소 수정 (SPEC §1.10 · D8)

요청서에 「국소 수정 지시 표」가 있으면 이 판은 새 초안이 아니라 **직전 판의 국소 수정**이다. 표의 좌표(`T<n>/S<i>`)에 선 문장만 지시문(「어디를 · 어느 재료로」)대로 고쳐 쓰고, 그 밖의 모든 문장·태그·헤더·프런트매터는 직전 판(「원천 조각」의 `thread.annotated.md`)과 **바이트 그대로** 둔다. 태그·헤더 규약은 §5 그대로이며, 고친 문장의 근거도 재료 ID 로 인용한다. 판정 레코드의 좌표계는 트윗 번호와 트윗 안 문장 번호다.

## 9a. 자유 리비전 (SPEC §1.10 판단 경로 · §4.6 · D8)

요청서에 「L2 메모 표」가 있으면 이 판은 **직전 판의 자유 리비전**이다. 메모는 자문 심급의 관찰(전역 구조 · 논지 흐름 · 재료 사용의 균형)이며 지시가 아니다 — 메모를 읽고 **네 판단으로** 어디를 얼마나 고칠지 정한다. 고친 문장의 근거도 재료 ID 로 인용하고, 문법·헤더·프런트매터 규약은 §5 그대로다. 고칠 곳이 없다고 판단하면 직전 판(「원천 조각」의 `thread.annotated.md`)을 바이트 그대로 낸다. 이 리비전은 한 번뿐이며 그 결과에 메모가 다시 오지 않는다.

## 10. 응답

`payload` 하나를 응답 계약(요청서의 `response_schema`)대로 낸다 — 초안이면 `thread_annotated_md`(위 문법의 마크다운 전문 · 프런트매터부터 마지막 트윗까지), 반려면 `material_defect`(4필드). 둘 중 하나다.
