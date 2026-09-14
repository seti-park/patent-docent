# 레인 요청 — probe-grade/v2/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `probe-grade` |
| 작업 | `v2` |
| 모델 | `opus-5` |
| effort | `low` |
| 배치 | `0` |
| 절차 문서 | `engine/probe/procedure-grader.md` |
| 입력 지문 | `ff20dc4372bbc5ccb393a32ecdf0f40cabd66095f6d0148c6bc5a493a97529b8` |

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
    "grades": {
      "items": {
        "additionalProperties": false,
        "properties": {
          "evidence": {
            "minLength": 1,
            "type": "string"
          },
          "grade": {
            "enum": [
              "hit",
              "partial",
              "miss"
            ]
          },
          "probe_id": {
            "enum": [
              "p0",
              "p1",
              "p2",
              "p3",
              "p4"
            ]
          },
          "question_id": {
            "enum": [
              "Q7"
            ]
          }
        },
        "required": [
          "probe_id",
          "question_id",
          "grade",
          "evidence"
        ],
        "type": "object"
      },
      "maxItems": 4,
      "minItems": 4,
      "type": "array"
    },
    "restatement": {
      "items": {
        "additionalProperties": false,
        "properties": {
          "judgement": {
            "enum": [
              "aligned",
              "drifted",
              "inverted"
            ]
          },
          "probe_id": {
            "enum": [
              "p0",
              "p1",
              "p2",
              "p3",
              "p4"
            ]
          }
        },
        "required": [
          "probe_id",
          "judgement"
        ],
        "type": "object"
      },
      "maxItems": 5,
      "minItems": 5,
      "type": "array"
    }
  },
  "required": [
    "grades",
    "restatement"
  ],
  "title": "lane-response/probe-grade",
  "type": "object"
}
```

## 이 요청의 지시

## 런 표지

| 항목 | 값 |
|---|---|
| run_id | `gdm-wo2026128750a1-agent-memory-3` |
| variant | `v2` |
| 모델 채점 표적 | 1 |
| 프로브 | 5 |

너는 계기의 채점자다. 스레드를 보지 않는다 — 「원천 조각」의 채점 입력(프로브 답변 + 동결 항목의 EN 값 + 훅 논지)만 본다.

## 과제

① `60-probe/v2/grading-input.json#targets[]` 의 표적마다, 각 프로브 답변이 `item_values` 와 합치하는지 `hit | partial | miss` 로 판정하고 근거로 삼은 **답변 구간**을 `evidence` 에 인용한다(`not-stated` 답변은 `miss` 다 — 전달되지 않았다는 뜻이며 프로브의 잘못이 아니다).

② `restatements[]` 의 프로브마다 세 문장 재서술이 `thesis_en` 과 정합하는지 `aligned | drifted | inverted` 로 판정한다.

## 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — 답변마다 grades 1 행, 프로브마다 restatement 1 행. 총평은 쓰지 않는다.

## 원천 조각

### `60-probe/v2/grading-input.json`

```text
{
  "restatements": [
    {
      "a_restatement": [
        "The thread describes AI memory systems as a specific technical architecture: memory objects are extracted from user interactions and stored with metadata in a datastore, not a transcript.",
        "When queried, the system retrieves relevant memories by comparing query embeddings to stored objects, keeps the highest-scoring subset by relevance, and allows memories to be corrected, merged, or refined as new information arrives.",
        "Users can request explicit forgetting or schedule automatic deletion after a set period, and the system uses these memories to inform both what the agent says and what actions it performs."
      ],
      "probe_id": "p0"
    },
    {
      "a_restatement": [
        "When an AI agent claims to 'remember' you, it is actually performing a computational loop that combines your query with memory objects retrieved from a datastore, feeding both through a sequence model to generate a response.",
        "These memory objects are created when the model predicts what is worth retaining from interactions, are structured with metadata like timestamps, and are retrieved by scoring against query embeddings using similarity measures such as cosine similarity.",
        "The system addresses agent forgetting through explicit deletion commands, time-based expiration with automatic maintenance cycles, and memory correction over time—described as a concrete architecture rather than marketing language."
      ],
      "probe_id": "p1"
    },
    {
      "a_restatement": [
        "AI agent memory is a structural architecture, not marketing: the system creates memory objects from user interactions and stores them with metadata including timestamps and interaction summaries.",
        "The system retrieves stored memories by comparing query embeddings to memory value embeddings using measures like cosine similarity, keeps a top subset, orders them by timestamp, and updates or merges memory objects when new input matches prior records.",
        "Users can delete memories immediately with 'forget that' or queue them for deletion after a set period with 'forget this after three months,' which solves the problem of memoryless agents requiring repeated input of the same details."
      ],
      "probe_id": "p2"
    },
    {
      "a_restatement": [
        "AI memory systems for agents operate as a loop of querying a datastore of your past interactions through a sequence model, though agents still forget and require users to re-enter details.",
        "The memory datastore consists of memory objects—containers with interaction data and metadata created when a model extracts what's worth remembering—retrieved for relevance to your current query using embedding similarity.",
        "Stored memories are corrected and updated when new input matches prior objects and can be deleted either explicitly or automatically on schedule, presenting a technical architecture rather than marketing hype."
      ],
      "probe_id": "p3"
    },
    {
      "a_restatement": [
        "Memory is described as an architectural mechanism, not marketing—memory objects store values (text, image, or audio) and metadata including timestamp, what triggered its storage, and interaction summary.",
        "When queried, the system scores stored memory objects for relevance by comparing query embeddings to memory value embeddings using cosine similarity, selects a top subset, and orders them by timestamp.",
        "The system manages the memory lifecycle: new matching input replaces or updates existing memories (or aligned objects merge), \"forget that\" commands delete immediately, time-specific deletion is queued (like \"forget after three months\"), and a maintenance cycle auto-deletes expired objects."
      ],
      "probe_id": "p4"
    }
  ],
  "targets": [
    {
      "answers": [
        {
          "answer": "The problem is that agents forget, requiring users to re-enter details repeatedly. What is different is the described technical architecture with memory objects from interactions, retrieved by relevance, corrected over time, and deletable on request.",
          "answer_kind": "stated",
          "probe_id": "p0",
          "quoted_span": "When an AI agent says it \"remembers\" you, is that architecture or marketing? Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response."
        },
        {
          "answer": "The problem is that memoryless agents force users to repeatedly re-enter information. This system's approach is different because it uses a memory datastore architecture where query and retrieved memory data flow through a sequence model—an architectural solution rather than marketing language.",
          "answer_kind": "stated",
          "probe_id": "p1",
          "quoted_span": "Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response."
        },
        {
          "answer": "The problem is that memoryless agents forget, requiring users to reenter the same details. It claims to be different by implementing a structured datastore of memory objects containing your interactions with metadata, rather than just a transcript of chats.",
          "answer_kind": "stated",
          "probe_id": "p3",
          "quoted_span": "Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response. This datastore is not a transcript of your chats. Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from."
        },
        {
          "answer": "The problem is that agents forget and users must re-enter the same details repeatedly. This system is claimed to be different by being a described architecture using memory objects made from interactions (some on explicit request), retrieved by relevance, corrected over time, and deleted when requested.",
          "answer_kind": "stated",
          "probe_id": "p4",
          "quoted_span": "When an AI agent says it \"remembers\" you, is that architecture or marketing? Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response."
        }
      ],
      "item_values": {
        "asserted_effect": "The specification asserts that a user-specific, agent-curated interaction memory lets a task start from a single interaction, supports asynchronous execution of previously instructed tasks, reduces runtime load by pre-processing memories offline, and gives the user control over what is remembered and forgotten.",
        "background_problem": "Agents without memory force users to re-enter the same details across sessions, and the alternative of wiring the agent to external data sources gives the user an all-or-nothing access choice with data the agent does not curate.",
        "delta": "No performance numbers are given; the claimed difference is structural: memory objects generated from prior interactions with the user, retrieved by relevance and fed into a sequence model input, rather than raw history or uncurated external sources."
      },
      "kind": "positioning",
      "material_id": "M116",
      "question_en": "What problem with memoryless agents is this system meant to solve, and what does it claim is different about its approach?",
      "question_id": "Q7"
    }
  ],
  "thesis_en": "This GDM Holding filing, with Demis Hassabis among the named inventors, claims a per-user datastore of curated memory objects that the model reads at every query, writes by itself, and erases when you ask."
}
```

## 절차 (정본 = engine/probe/procedure-grader.md)

# 채점 절차 — `probe-grade/<variant>`

정본 서술 = `docs/SPEC.md` §5.3(채점 분리 · 모델 채점 출력 규약 · 프로브 A 의 채점) · `docs/CHARTER.md` D9. 이 문서는 요청서에 인라인되어 레인이 읽는 절차다. 산문은 KR, 값·필드는 EN 이다.

## 1. 정체성

너는 계기의 **채점자**다. 프로브가 아니다. 스레드를 보지 않는다 — 스레드를 보면 프로브 답변 대신 스레드를 후하게 읽어 주는 편향이 들어온다. 네가 보는 것은 「원천 조각」의 채점 입력 하나뿐이다: 표적마다 **동결 항목의 EN 값**(`item_values`)과 **프로브 답변들**, 그리고 프로브마다 **세 문장 재서술**과 블루프린트의 **훅 논지**(`thesis_en`).

수치·청구항 구성요소·도면부호는 러너가 결정론으로 이미 판정했고 여기에 오지 않는다. 네게 오는 것은 서술 kind(`grounding` · `implication` · `positioning`)뿐이다.

## 2. 답변 채점 (`grades[]`)

답변 하나마다 `item_values` 와 대조해 셋 중 하나로 판정한다.

| grade | 뜻 |
|---|---|
| `hit` | 답변이 항목의 요지를 담는다 — 표현이 달라도 뜻이 같다 |
| `partial` | 요지의 일부만 담거나, 담되 뜻을 좁히거나 넓혔다 |
| `miss` | 요지가 없거나 뒤집혔다. `not-stated` 답변은 `miss` 다(전달되지 않았다는 뜻이며 프로브의 잘못이 아니다) |

`evidence` 에는 판정 근거로 삼은 **답변 구간**을 인용한다(`answer` 또는 `quoted_span` 에서). 자연어 총평은 쓰지 않는다 — 그것은 소견의 관할이다.

## 3. 재서술 채점 (`restatement[]`)

프로브마다 세 문장 재서술이 `thesis_en` 과 정합하는지 셋 중 하나로 판정한다: `aligned`(같은 논지) · `drifted`(관련은 있으나 다른 질문에 답한다) · `inverted`(논지가 뒤집혔다). 이 축은 도달률에 합산되지 않는다.

## 4. 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — 입력의 답변마다 `grades` 1 행, 프로브마다 `restatement` 1 행. 빠짐도 초과도 러너가 거부한다.
