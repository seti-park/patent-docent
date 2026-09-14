# 레인 요청 — gate-l2/v2/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `gate-l2` |
| 작업 | `v2` |
| 모델 | `gpt-6-astra` |
| effort | `high` |
| 배치 | `0` |
| 절차 문서 | `engine/gate/l2/procedure.md` |
| 입력 지문 | `2af9d22fc0abbfa68fb8a02027e436968ba19c18cd0ca388c4544e40883cc571` |

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
  "additionalProperties": false,
  "properties": {
    "memos": {
      "items": {
        "additionalProperties": false,
        "properties": {
          "locus": {
            "additionalProperties": false,
            "properties": {
              "sentence": {
                "minimum": 1,
                "type": [
                  "integer",
                  "null"
                ]
              },
              "tweet": {
                "minimum": 1,
                "type": [
                  "integer",
                  "null"
                ]
              }
            },
            "required": [
              "tweet",
              "sentence"
            ],
            "type": "object"
          },
          "rule": {
            "pattern": "^l2\\.[a-z][a-z0-9-]*$",
            "type": "string"
          },
          "text": {
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "rule",
          "locus",
          "text"
        ],
        "type": "object"
      },
      "type": "array"
    }
  },
  "required": [
    "memos"
  ],
  "title": "lane-response/gate-l2",
  "type": "object"
}
```

## 이 요청의 지시

## 런 표지

| 항목 | 값 |
|---|---|
| run_id | `gdm-wo2026128750a1-agent-memory-3` |
| variant | `v2` |
| spec_version | `1` |
| spec_digest | `sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407` |
| thread_digest | `sha256:f63ec80f7c674de2c8dcb293b2560099a4aa0d905960202a299a6bd7bbdbc1ec` |

너는 L2 자문 심급이다. 전역 판단의 메모만 낸다 — 글을 고치지 않고, 판정을 바꾸지 않으며, 점수를 매기지 않는다(D8·D15). 파일 시스템을 열지 않는다 · 필요한 것은 전부 「원천 조각」 절에 있다.

## 좌표계

`locus = {tweet, sentence}` 는 「원천 조각」의 `50-gate/v2/annotation-index.json` 의 `tweets[].n` · `sentences[].i` 와 같다(SPEC §3.3 · §4.2). 전역 메모(특정 문장이 아닌 구조·흐름)는 둘 다 `null` 로, 트윗 단위는 `sentence: null` 로 적는다. 주석본 원문은 `40-compose/v2/thread.annotated.md`, 재료 정답지는 `15-frozen/material-spec.v1.json`, 설계는 `20-design/blueprint.json` 이다.

## 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `memos[]` 이며 해당 없음은 빈 배열이다. `rule` 은 `l2.<slug>` 형태의 관점 표지이고 `text` 는 서술이다. 이 메모는 펜의 **자유 리비전 1회**의 데이터로 전달된다 — 펜은 네 판단으로 고칠지 말지를 정한다. 메모는 그 뒤 다시 돌지 않는다(위상 봉쇄).

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
This filing claims a loop: your query plus memory data from a per-user datastore of objects built from your past interactions, into a sequence model, out as a response.[M1,M2,M3,M4,M5,M6]

## T2 {slot: stop, fig: fig-02}
This datastore is not a transcript of your chats.[M107,M118]
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.[M17,M30,M68,M81]

## T3 {slot: stop, fig: fig-08+fig-07}
A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.[M13,M14,M15,M64,M65,M66,M121]
That portion is written as a memory value in a memory object, and a trigger can start this pass offline, ahead of any query.[M16,M67,M112,M120]

## T4 {slot: stop, fig: fig-03}
At query time the agent does not reread everything; it ranks stored objects by relevance to your query.[M12,M26,M63,M77]
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.[M24,M27,M28,M75,M78,M79,M115,M119]

## T5 {slot: stop, fig: fig-21}
Memories can be corrected: new timestamped input is matched to a prior memory object and either replaces it or updates it.[M39,M40,M42,M43,M90,M91,M93,M94]
Aligned objects can be consolidated into one; kept supporting interactions let a contradiction refine a memory, not overwrite it.[M36,M87,M109]

## T6 {slot: pivot, fig: fig-10}
Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.[M20,M21,M22,M23,M71,M72,M73]
Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.[M74,M110,M111,M122]

## T7 {slot: stop, fig: fig-01}
The model first analyzes your query against the memory data, and that analysis may stay off the query's interface.[M34,M35,M85,M86]
The response that does appear can be an API call that makes a device act, so memory shapes what the agent does, not just what it says.[M44,M113]

## T8 {slot: landing, fig: fig-01}
No performance numbers are given.[M116]
What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask.[M3,M12,M21,M40]
That is a described architecture, not a slogan.[M116]

## T9 {slot: tail, fig: none}
The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.[M103,M104,M106]
Follow along for the next patent walk-through.[narrative]
```

### `50-gate/v2/annotation-index.json`

```text
{
  "by_material": {
    "M1": [
      {
        "sentence": 2,
        "tweet": 1
      }
    ],
    "M103": [
      {
        "sentence": 1,
        "tweet": 9
      }
    ],
    "M104": [
      {
        "sentence": 1,
        "tweet": 9
      }
    ],
    "M106": [
      {
        "sentence": 1,
        "tweet": 9
      }
    ],
    "M107": [
      {
        "sentence": 1,
        "tweet": 2
      }
    ],
    "M109": [
      {
        "sentence": 2,
        "tweet": 5
      }
    ],
    "M110": [
      {
        "sentence": 2,
        "tweet": 6
      }
    ],
    "M111": [
      {
        "sentence": 2,
        "tweet": 6
      }
    ],
    "M112": [
      {
        "sentence": 2,
        "tweet": 3
      }
    ],
    "M113": [
      {
        "sentence": 2,
        "tweet": 7
      }
    ],
    "M115": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M116": [
      {
        "sentence": 1,
        "tweet": 8
      },
      {
        "sentence": 3,
        "tweet": 8
      }
    ],
    "M118": [
      {
        "sentence": 1,
        "tweet": 2
      }
    ],
    "M119": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M12": [
      {
        "sentence": 1,
        "tweet": 4
      },
      {
        "sentence": 2,
        "tweet": 8
      }
    ],
    "M120": [
      {
        "sentence": 2,
        "tweet": 3
      }
    ],
    "M121": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M122": [
      {
        "sentence": 2,
        "tweet": 6
      }
    ],
    "M13": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M14": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M15": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M16": [
      {
        "sentence": 2,
        "tweet": 3
      }
    ],
    "M17": [
      {
        "sentence": 2,
        "tweet": 2
      }
    ],
    "M2": [
      {
        "sentence": 2,
        "tweet": 1
      }
    ],
    "M20": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M21": [
      {
        "sentence": 1,
        "tweet": 6
      },
      {
        "sentence": 2,
        "tweet": 8
      }
    ],
    "M22": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M23": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M24": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M26": [
      {
        "sentence": 1,
        "tweet": 4
      }
    ],
    "M27": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M28": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M3": [
      {
        "sentence": 2,
        "tweet": 1
      },
      {
        "sentence": 2,
        "tweet": 8
      }
    ],
    "M30": [
      {
        "sentence": 2,
        "tweet": 2
      }
    ],
    "M34": [
      {
        "sentence": 1,
        "tweet": 7
      }
    ],
    "M35": [
      {
        "sentence": 1,
        "tweet": 7
      }
    ],
    "M36": [
      {
        "sentence": 2,
        "tweet": 5
      }
    ],
    "M39": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M4": [
      {
        "sentence": 2,
        "tweet": 1
      }
    ],
    "M40": [
      {
        "sentence": 1,
        "tweet": 5
      },
      {
        "sentence": 2,
        "tweet": 8
      }
    ],
    "M42": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M43": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M44": [
      {
        "sentence": 2,
        "tweet": 7
      }
    ],
    "M5": [
      {
        "sentence": 2,
        "tweet": 1
      }
    ],
    "M6": [
      {
        "sentence": 2,
        "tweet": 1
      }
    ],
    "M63": [
      {
        "sentence": 1,
        "tweet": 4
      }
    ],
    "M64": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M65": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M66": [
      {
        "sentence": 1,
        "tweet": 3
      }
    ],
    "M67": [
      {
        "sentence": 2,
        "tweet": 3
      }
    ],
    "M68": [
      {
        "sentence": 2,
        "tweet": 2
      }
    ],
    "M71": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M72": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M73": [
      {
        "sentence": 1,
        "tweet": 6
      }
    ],
    "M74": [
      {
        "sentence": 2,
        "tweet": 6
      }
    ],
    "M75": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M77": [
      {
        "sentence": 1,
        "tweet": 4
      }
    ],
    "M78": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M79": [
      {
        "sentence": 2,
        "tweet": 4
      }
    ],
    "M81": [
      {
        "sentence": 2,
        "tweet": 2
      }
    ],
    "M85": [
      {
        "sentence": 1,
        "tweet": 7
      }
    ],
    "M86": [
      {
        "sentence": 1,
        "tweet": 7
      }
    ],
    "M87": [
      {
        "sentence": 2,
        "tweet": 5
      }
    ],
    "M90": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M91": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M93": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ],
    "M94": [
      {
        "sentence": 1,
        "tweet": 5
      }
    ]
  },
  "narrative_sentences": [
    {
      "sentence": 1,
      "tweet": 1
    },
    {
      "sentence": 2,
      "tweet": 9
    }
  ],
  "run_id": "gdm-wo2026128750a1-agent-memory-3",
  "schema": "annotation-index/v0",
  "spec_version": 1,
  "tweets": [
    {
      "n": 1,
      "sentences": [
        {
          "citations": [],
          "i": 1,
          "narrative": true,
          "text": "When an AI agent says it \"remembers\" you, is that architecture or marketing?",
          "text_raw": "When an AI agent says it \"remembers\" you, is that architecture or marketing?"
        },
        {
          "citations": [
            "M1",
            "M2",
            "M3",
            "M4",
            "M5",
            "M6"
          ],
          "i": 2,
          "narrative": false,
          "text": "This filing claims a loop: your query plus memory data from a per-user datastore of objects built from your past interactions, into a sequence model, out as a response.",
          "text_raw": "This filing claims a loop: your query plus memory data from a per-user datastore of objects built from your past interactions, into a sequence model, out as a response."
        }
      ],
      "slot": "hook"
    },
    {
      "n": 2,
      "sentences": [
        {
          "citations": [
            "M107",
            "M118"
          ],
          "i": 1,
          "narrative": false,
          "text": "This datastore is not a transcript of your chats.",
          "text_raw": "This datastore is not a transcript of your chats."
        },
        {
          "citations": [
            "M17",
            "M30",
            "M68",
            "M81"
          ],
          "i": 2,
          "narrative": false,
          "text": "Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.",
          "text_raw": "Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from."
        }
      ],
      "slot": "stop"
    },
    {
      "n": 3,
      "sentences": [
        {
          "citations": [
            "M13",
            "M14",
            "M15",
            "M64",
            "M65",
            "M66",
            "M121"
          ],
          "i": 1,
          "narrative": false,
          "text": "A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.",
          "text_raw": "A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it."
        },
        {
          "citations": [
            "M16",
            "M67",
            "M112",
            "M120"
          ],
          "i": 2,
          "narrative": false,
          "text": "That portion is written as a memory value in a memory object, and a trigger can start this pass offline, ahead of any query.",
          "text_raw": "That portion is written as a memory value in a memory object, and a trigger can start this pass offline, ahead of any query."
        }
      ],
      "slot": "stop"
    },
    {
      "n": 4,
      "sentences": [
        {
          "citations": [
            "M12",
            "M26",
            "M63",
            "M77"
          ],
          "i": 1,
          "narrative": false,
          "text": "At query time the agent does not reread everything; it ranks stored objects by relevance to your query.",
          "text_raw": "At query time the agent does not reread everything; it ranks stored objects by relevance to your query."
        },
        {
          "citations": [
            "M24",
            "M27",
            "M28",
            "M75",
            "M78",
            "M79",
            "M115",
            "M119"
          ],
          "i": 2,
          "narrative": false,
          "text": "It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.",
          "text_raw": "It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp."
        }
      ],
      "slot": "stop"
    },
    {
      "n": 5,
      "sentences": [
        {
          "citations": [
            "M39",
            "M40",
            "M42",
            "M43",
            "M90",
            "M91",
            "M93",
            "M94"
          ],
          "i": 1,
          "narrative": false,
          "text": "Memories can be corrected: new timestamped input is matched to a prior memory object and either replaces it or updates it.",
          "text_raw": "Memories can be corrected: new timestamped input is matched to a prior memory object and either replaces it or updates it."
        },
        {
          "citations": [
            "M36",
            "M87",
            "M109"
          ],
          "i": 2,
          "narrative": false,
          "text": "Aligned objects can be consolidated into one; kept supporting interactions let a contradiction refine a memory, not overwrite it.",
          "text_raw": "Aligned objects can be consolidated into one; kept supporting interactions let a contradiction refine a memory, not overwrite it."
        }
      ],
      "slot": "stop"
    },
    {
      "n": 6,
      "sentences": [
        {
          "citations": [
            "M20",
            "M21",
            "M22",
            "M23",
            "M71",
            "M72",
            "M73"
          ],
          "i": 1,
          "narrative": false,
          "text": "Forgetting is claimed: \"forget that\" deletes the specified information, and \"forget this after three months\" queues it for deletion.",
          "text_raw": "Forgetting is claimed: \"forget that\" deletes the specified information, and \"forget this after three months\" queues it for deletion."
        },
        {
          "citations": [
            "M74",
            "M110",
            "M111",
            "M122"
          ],
          "i": 2,
          "narrative": false,
          "text": "Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.",
          "text_raw": "Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it."
        }
      ],
      "slot": "pivot"
    },
    {
      "n": 7,
      "sentences": [
        {
          "citations": [
            "M34",
            "M35",
            "M85",
            "M86"
          ],
          "i": 1,
          "narrative": false,
          "text": "The model first analyzes your query against the memory data, and that analysis may stay off the query's interface.",
          "text_raw": "The model first analyzes your query against the memory data, and that analysis may stay off the query's interface."
        },
        {
          "citations": [
            "M44",
            "M113"
          ],
          "i": 2,
          "narrative": false,
          "text": "The response that does appear can be an API call that makes a device act, so memory shapes what the agent does, not just what it says.",
          "text_raw": "The response that does appear can be an API call that makes a device act, so memory shapes what the agent does, not just what it says."
        }
      ],
      "slot": "stop"
    },
    {
      "n": 8,
      "sentences": [
        {
          "citations": [
            "M116"
          ],
          "i": 1,
          "narrative": false,
          "text": "No performance numbers are given.",
          "text_raw": "No performance numbers are given."
        },
        {
          "citations": [
            "M3",
            "M12",
            "M21",
            "M40"
          ],
          "i": 2,
          "narrative": false,
          "text": "What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask.",
          "text_raw": "What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask."
        },
        {
          "citations": [
            "M116"
          ],
          "i": 3,
          "narrative": false,
          "text": "That is a described architecture, not a slogan.",
          "text_raw": "That is a described architecture, not a slogan."
        }
      ],
      "slot": "landing"
    },
    {
      "n": 9,
      "sentences": [
        {
          "citations": [
            "M103",
            "M104",
            "M106"
          ],
          "i": 1,
          "narrative": false,
          "text": "The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.",
          "text_raw": "The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18."
        },
        {
          "citations": [],
          "i": 2,
          "narrative": true,
          "text": "Follow along for the next patent walk-through.",
          "text_raw": "Follow along for the next patent walk-through."
        }
      ],
      "slot": "tail"
    }
  ],
  "variant": "v2"
}
```

## 절차 (정본 = engine/gate/l2/procedure.md)

# L2 자문 절차 — `gate-l2/<variant>`

정본 서술 = `docs/SPEC.md` §1.10(층별 관할 · L2 행 · 판단 경로) · §4.6(점수 발행 금지의 기계적 집행) · `docs/CHARTER.md` D7 · D8 · D15. 이 문서는 요청서에 인라인되어 레인이 읽는 절차다. 산문은 KR, 값·필드는 EN 이다.

## 1. 정체성 (D8 · D15)

너는 L2 자문 심급이다. 관할은 **전역 판단** — 스레드 한 편이 하나의 글로서 어떻게 서 있는가다. 거부권이 없다 · 판정(`decision`)을 바꾸지 않는다 · 글을 고치지 않는다 · 대체 문장을 쓰지 않는다 · 점수·등급·별점·백분율·N/10 을 어떤 형태로도 적지 않는다. 네가 내는 것은 **비평 메모**이고, 그 메모는 펜에게 데이터로 건너가 펜이 자기 판단으로 한 번 고쳐 쓸 기회(자유 리비전 1회)의 재료가 된다. 그 뒤 너는 다시 불리지 않는다(위상 봉쇄 · D8).

정답이 있는 것은 네 관할이 아니다 — 문장↔재료 정합(L1) · 형식 규격(L0) · 수치 대조(L0)는 이미 판정되었고, 그 결과를 다시 세지 마라. 훅 조응 · 안도감 착지 · 도슨트 보이스는 **소견(critique)** 의 관점 3종이며 여기서 다루지 않는다.

## 2. 입력

「원천 조각」 절에 넷이 있다.

| 조각 | 용도 |
|---|---|
| `40-compose/<variant>/thread.annotated.md` | 대상 초안(§3.2 문법 · 문장마다 `[M<n>,…]` 또는 `[narrative]`) |
| `15-frozen/material-spec.v<N>.json` | 재료의 우주 — 초안이 **무엇을 쓰지 않았는가**를 볼 때만 참조한다 |
| `20-design/blueprint.json` | 설계 의도 — 슬롯 아크 · 전달 표적(`transmission_targets`) · 훅 논지 |
| `50-gate/<variant>/annotation-index.json` | 좌표계(`tweets[].n` · `sentences[].i`) |

원천 특허 · 다른 변주 · 이전 판정 · L1 로그 · 수정 이력은 제공되지 않는다.

## 3. 관점 — 「전역 구조 · 논지 흐름 · 재료 사용의 균형」

메모의 `rule` 은 `l2.<slug>` 형태의 관점 표지다. 아래 셋이 기본이며, 필요하면 같은 형태의 slug 를 새로 붙여도 된다(어휘는 닫혀 있지 않다 — 메모는 자문이지 판정이 아니다).

| rule | 묻는 것 |
|---|---|
| `l2.structure` | 슬롯 아크(훅 → 전시 스톱 → 반전 → 착지 → 꼬리)가 한 편의 글로 이어지는가. 트윗 하나가 홀로 노출되어도 서는가. 어느 트윗이 앞뒤 없이 떠 있는가 |
| `l2.thesis-flow` | 블루프린트의 훅 논지(`hook.thesis_en`)가 본문에서 실제로 전개되어 착지에 닿는가. 논지가 중간에 다른 질문으로 새는가. 반전 스톱이 정말 질문에 답하는 물증인가 |
| `l2.material-balance` | 전달 표적 재료가 본문에서 균형 있게 실렸는가 — 한 재료가 여러 트윗에 반복되거나, 표적인데 한 문장에 얇게 걸쳐 있거나, 표적이 아닌 재료가 지면을 차지하는가 |

## 4. 메모의 형식

- `locus` — 전역 메모는 `{tweet: null, sentence: null}`, 트윗 단위는 `{tweet: n, sentence: null}`, 문장 단위는 둘 다 채운다.
- `text` — **관찰과 그 근거**를 서술한다: 무엇이 어디에서 어떻게 읽히는가. 「T5 가 T4 의 전제를 반복해 T6 의 반전이 늦게 온다」처럼 위치와 현상을 함께 적는다.
- 서술에는 수치 등급이 없다. 「강하다/약하다」「앞이 무겁다」같은 상대 서술은 된다. 「8/10」「B+」「★★★」「85%」「score」「grade」「rating」「점수」는 러너의 린트(`gate.no-score`)가 잡아 **런을 세운다**(D15). 재료의 원문 표현(`automotive-grade`, `4x improvement`, `A-1`)을 인용하는 것은 점수가 아니다.
- 대체 문장을 쓰지 않는다. 「이렇게 바꿔라」가 아니라 「여기가 이렇게 읽힌다」까지가 네 몫이다. 고치는 판단은 펜의 것이다.
- 고칠 곳이 없다고 판단하면 `memos` 를 빈 배열로 낸다 — 억지로 채우지 마라.

## 5. 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `memos[]` 이며, 각 원소는 `rule` · `locus` · `text` 셋이다. id 는 러너가 붙인다.
