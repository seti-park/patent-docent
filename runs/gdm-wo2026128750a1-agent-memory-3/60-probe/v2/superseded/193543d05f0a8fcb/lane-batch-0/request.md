# 레인 요청 — probe/v2/batch-0

| 항목 | 값 |
|---|---|
| 독립 실행 | `probe` |
| 작업 | `v2` |
| 모델 | `haiku-4.5` |
| effort | `low` |
| 배치 | `0` |
| 절차 문서 | `engine/probe/procedure-probe.md` |
| 입력 지문 | `5dca2060d0de5663161eb452998fbaec5dc8339a70ba3aa43ed3865a49f243c2` |

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
    "a_restatement": {
      "items": {
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 3,
      "minItems": 3,
      "type": "array"
    },
    "b_answers": {
      "items": {
        "additionalProperties": false,
        "else": {
          "properties": {
            "answer": {
              "type": "null"
            },
            "quoted_span": {
              "type": "null"
            }
          }
        },
        "if": {
          "properties": {
            "answer_kind": {
              "const": "stated"
            }
          }
        },
        "properties": {
          "answer": {
            "type": [
              "string",
              "null"
            ]
          },
          "answer_kind": {
            "enum": [
              "stated",
              "not-stated"
            ]
          },
          "question_id": {
            "enum": [
              "Q1",
              "Q2",
              "Q3",
              "Q4",
              "Q5",
              "Q6",
              "Q7"
            ]
          },
          "quoted_span": {
            "type": [
              "string",
              "null"
            ]
          },
          "target_material_id": {
            "enum": [
              "M116",
              "M12",
              "M16",
              "M21",
              "M23",
              "M3",
              "M40"
            ]
          }
        },
        "required": [
          "question_id",
          "target_material_id",
          "answer_kind",
          "answer",
          "quoted_span"
        ],
        "then": {
          "properties": {
            "answer": {
              "minLength": 1,
              "type": "string"
            },
            "quoted_span": {
              "minLength": 1,
              "type": "string"
            }
          }
        },
        "type": "object"
      },
      "maxItems": 7,
      "minItems": 7,
      "type": "array"
    }
  },
  "required": [
    "a_restatement",
    "b_answers"
  ],
  "title": "lane-response/probe",
  "type": "object"
}
```

## 이 요청의 지시

## 런 표지

| 항목 | 값 |
|---|---|
| run_id | `gdm-wo2026128750a1-agent-memory-3` |
| variant | `v2` |
| input_digest | `sha256:193543d05f0a8fcb7d46903989c606381655f6073796f8d29149f4b1a7264832` |
| question_set_digest | `sha256:3f3d920af8f8d9b06de88fd4dc9f0fba7cbe3a30c4a86822560a05279978afaa` |

너는 읽기 계기다. 「원천 조각」의 스레드 텍스트와 질문지만 본다. 다른 계기의 답도, 정답지도 없다.

## 과제

A. `50-gate/v2/thread.stripped.md` 을 읽고 핵심 주장을 **세 문장**으로 다시 말한다(`a_restatement`).

B. `60-probe/questions.json` 의 질문마다 답한다(`b_answers`) — 스레드에서 답을 찾았으면 `answer_kind: stated` 와 답과 근거가 된 **스레드 원문 구간**(`quoted_span` · 글자 그대로 복사)을, 스레드에 없으면 `answer_kind: not-stated` 와 `answer: null` · `quoted_span: null` 을 적는다. `not-stated` 는 정당한 답이다 — 없는 것을 지어내지 않는다.

## 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다.

## 원천 조각

### `50-gate/v2/thread.stripped.md`

```text
When an AI agent says it "remembers" you, is that architecture or marketing?
Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response.

This datastore is not a transcript of your chats.
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.

A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.
It is stored as a memory value in a memory object, and one trigger is you asking the agent to remember your favorite architect.

At query time the agent does not reread everything; it ranks stored objects by relevance to your query.
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.

Memories are corrected: new timestamped input is matched to the prior memory object it concerns, which is then replaced or updated.
Aligned objects can be consolidated into one, and a contradiction refines the matched memory rather than overcorrecting it.

Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.
Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.

The model first works through your query against the recalled memory data, and that working-out can stay off the screen.
What comes back can be an API call that makes a device act, so the memory shapes what the agent does, not only what it says.

No performance numbers are given.
What is claimed is structural: memory objects made from your interactions, some on your explicit request, retrieved by relevance, corrected over time, and deleted when you ask.
That is a described architecture, not a slogan.

The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.
Follow along for the next patent walk-through.
```

### `60-probe/questions.json`

```text
{
  "questions": [
    {
      "question_id": "Q1",
      "target_material_id": "M3",
      "question_en": "Where do the items in the agent's memory store come from in the first place?"
    },
    {
      "question_id": "Q2",
      "target_material_id": "M16",
      "question_en": "Once the system decides a piece of what you said is worth keeping, where does that piece end up?"
    },
    {
      "question_id": "Q3",
      "target_material_id": "M12",
      "question_en": "When you ask the agent something, how does it decide which of your stored memories to pull up?"
    },
    {
      "question_id": "Q4",
      "target_material_id": "M21",
      "question_en": "What does the system actually do to the stored information when you tell it to forget something?"
    },
    {
      "question_id": "Q5",
      "target_material_id": "M23",
      "question_en": "What happens if you ask the agent to forget something not now but after a set period of time?"
    },
    {
      "question_id": "Q6",
      "target_material_id": "M40",
      "question_en": "When new input matches a memory the system already holds, what does it do with the older one?"
    },
    {
      "question_id": "Q7",
      "target_material_id": "M116",
      "question_en": "What problem with memoryless agents is this system meant to solve, and what does it claim is different about its approach?"
    }
  ]
}
```

## 절차 (정본 = engine/probe/procedure-probe.md)

# 읽기 계기 절차 — `probe/<variant>`

이 문서는 요청서에 인라인되어 레인이 읽는 절차다. 산문은 KR, 값·필드는 EN 이다.

## 1. 정체성

너는 **읽기 계기**다. 스레드 한 편과 질문지 하나를 받는다. 그 밖의 것은 없다 — 배경 지식으로 답을 보충하지 않는다. 스레드에 없는 것은 「없다」가 답이다.

## 2. 과제 A — 재서술

스레드를 처음부터 끝까지 읽고 **핵심 주장을 세 문장**으로 다시 말한다(`a_restatement` · 정확히 3 · EN). 스레드가 말한 것을 스레드의 순서대로, 네 말로 적는다.

## 3. 과제 B — 질문 답변

질문지의 질문마다 하나씩 답한다(`b_answers` · 질문 수와 같은 수).

| 경우 | 적는 것 |
|---|---|
| 스레드에서 답을 찾았다 | `answer_kind: stated` · `answer` = 스레드가 말한 대로의 답(EN) · `quoted_span` = 근거가 된 **스레드 원문 구간을 글자 그대로** 복사 |
| 스레드에 없다 | `answer_kind: not-stated` · `answer: null` · `quoted_span: null` |

`quoted_span` 은 스레드 텍스트의 부분문자열이어야 한다 — 러너가 기계로 대조하며, 원문이 아닌 구간은 그 답변을 무효로 만든다. 요약하지 말고 복사하라. `not-stated` 는 정당한 답이며 「없다」를 지어낸 답으로 덮지 마라.

## 4. 응답

`payload` 하나를 응답 계약(`response_schema`)대로 낸다 — `a_restatement` · `b_answers` 둘뿐이다. 그 밖의 필드는 계약에 없다.
