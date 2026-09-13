# 레인 산출 계약 — JSON 형태와 금지 사항

레인은 요청 디렉터리에 **`response.json` 한 파일**을 쓴다. 그 밖의 파일을 쓰지 않는다.

```json
{
  "lane_id": "read-a/decompose/batch-0",
  "model": "opus-5",
  "effort": "max",
  "payload": { }
}
```

- `lane_id`는 요청의 값을 **그대로** 옮긴다. 다르면 응답이 거부된다.
- `model`·`effort`에는 **실제로 돌아간 값**을 적는다. 요청과 다르면 러너가 레인 기록에 `mismatch: true`로 남기고 결함으로 보고한다 — **조용한 대체 금지**. 요청과 다른 티어로 돌 수밖에 없었다면 그 사실이 기록되는 편이 낫다.
- `payload`는 요청의 `response_schema`를 통과해야 한다. 위반하면 응답 자체가 거부된다(부분 채택 없음).

---

## 1. `decompose`

```json
{
  "claims": {
    "independent": [ { "id": "CL-1", "type": "independent", "text_verbatim": "…",
                       "elements": [ { "id": "CL-1/e1", "text_verbatim": "…",
                                       "material_id": "M1", "children": [] } ] } ],
    "dependents":  [ { "id": "CL-5", "depends_on": ["CL-1"], "dependency_type": "single",
                       "text_verbatim": "…",
                       "additions": [ { "id": "CL-5/a1", "attaches_to": "CL-1/e2",
                                        "text_verbatim": "…", "material_id": "M3" } ] } ],
    "applicant_interest": [ { "claim": "CL-1", "signal": "…EN…", "material_id": "M6" } ]
  },
  "items": [ { "id": "M1", "kind": "component", "status": "active", "superseded_by": null,
               "claim_ref": "CL-1/e1", "label_en": "…", "text_verbatim": "…" } ],
  "screening_memo": { "direction": "clear", "reason": "…KR…" },
  "review_requests": [ { "target": "CL-5/a1", "reason": "…KR — 무엇이 확실치 않고 무엇을 보면 판가름나는가…" } ]
}
```

★ `drop_signal`은 이 레인의 산출이 **아니다**(재정 P-A). 조기 판단은 `screening_memo`로 **기록만** 하며 러너를 세우지 않는다. `direction` ∈ `clear` · `concern`.

## 2. `ground-independent` · `ground-dependent`

```json
{ "items": [ { "id": "M4", "kind": "grounding", "status": "active", "superseded_by": null,
               "component": "M2",
               "anchor_state": { "spec": "found", "figure": "not-depicted" },
               "spec_refs": [ { "locator": "[0042]", "quote": "…" } ],
               "figure_refs": [],
               "search_note": "…KR…" } ],
  "review_requests": [ { "target": "M4", "reason": "…KR — 무엇이 확실치 않고 무엇을 보면 판가름나는가…" } ] }
```

배열의 모든 원소는 `kind: "grounding"`이다. 다른 kind를 섞으면 응답이 거부된다.

## 3. `synthesize`

```json
{
  "items": [ { "id": "M5", "kind": "fact", "origin": "figure-sourced", "…": "…" },
             { "id": "M6", "kind": "implication", "numeric_refs": ["M31"], "…": "…" },
             { "id": "M7", "kind": "positioning", "numeric_refs": [], "…": "…" },
             { "id": "M8", "kind": "figure_note", "…": "…" } ],
  "figures": [ { "id": "FIG-2", "numerals": ["210"], "caption_quote": "…",
                 "raw_path": "00-source/figures-raw/fig-02.png", "asset_path": null } ],
  "drop_signal": { "stage": "final", "verdict": "go", "reason": "…KR…" },
  "review_requests": []
}
```

`review_requests` 는 세 작업 공통의 Owner 판독 요청 배열이다(재정 T58 ③ · T59 — 각 절차 문서의 「Owner 판독 요청」 절). 원소 = `{ "target", "reason"(KR), "refs"?: [ { "locator", "quote" } ] }`. 요청이 없으면 위처럼 **빈 배열**로 낸다.

★ 이 레인이 만들 수 있는 `fact` 의 `origin` 은 **`derived` · `figure-sourced` 둘뿐**이다(재정 P-B). `quoted` · `bibliographic` 은 엔진의 수확기가 전수로 만들며, 네가 만들면 `value.harvest-parity` 가 실패시킨다. `implication` · `positioning` 은 **`numeric_refs` 가 필수**이며(빈 배열 허용) 수확 목록의 ID 만 가리킨다.

---

## 4. 항목 ID 규율 (전 작업 공통)

- 항목 ID는 `M<n>` 한 문법뿐이며 **런 안에서 유일**하다. 두 레인이 같은 번호를 쓰면 조립에서 충돌한다 — 요청의 지시가 번호 대역을 지정하면 그 대역 안에서 쓴다.
- **재사용·재번호 금지.** 같은 `M7`이 다른 재료를 가리키는 순간 인용이 조용히 어긋난다.
- `status`는 신규 항목이면 언제나 `"active"`, `superseded_by`는 `null`이다. 생애 상태를 여기서 조작하지 마라 — 철회·교체는 개정 경로의 일이다.

## 5. 금지 사항

| 금지 | 이유 |
|---|---|
| 인용을 다듬어 적기(공백 접기·따옴표 치환·줄바꿈 제거) | `read.verbatim`은 정규화 없이 바이트 비교한다. 다듬은 인용은 **없는 문장**과 같다 |
| 원문에 없는 수치를 적기 | `read.value-derivation`이 스팬·산식으로 대조한다. 유효한 인용 옆의 날조된 수치가 이 검사의 반증 대상이다 |
| 접지 실패를 누락으로 처리하기 | 예외 상태(`no-anchor-found`·`not-depicted`)로 신고한다. 감춘 예외는 은폐다 |
| 파생의 파생 | `derivation.inputs[].ref`는 `origin: "quoted"`만 가리킨다(깊이 1) |
| 본문에 **구조 표지 어형이 하나도 없는** 종속항에 `unclassified` 선언 | 표지는 규칙이 못 읽는 구조를 위한 것이지 읽기 귀찮은 구조를 위한 것이 아니다. `parse.unclassified-not-an-escape`가 잡는다. ★ 판정 기준은 **인용 어형의 파싱 가능성이 아니라 본문의 구조 표지 유무**다 — `of claim 1`로 평범하게 인용하는 Markush 종속항의 선언은 **옳고, 통과한다**. 같은 디렉터리 `10-decompose.md` §2가 그 기준의 정본 서술이다 |
| `origin: "quoted"`·`"bibliographic"` fact 만들기 | 원문 스팬 수치와 서지 수치는 **엔진이 전수 수확**한다. 레인이 만들면 `value.harvest-parity`가 수확기 재실행 결과와 대조해 실패시킨다(재정 P-B) |
| 값 필드에 한글 | 값 언어는 EN 단일. 예외는 `drop_signal.reason`과 `grounding.search_note` **둘뿐**이다 |
| 다른 실행(`read-a`↔`read-b`)의 산출 참조 | 독립성이 깨지면 수렴 검사가 아무것도 반증하지 못한다 |
| 스레드·훅·독자 반응을 고려한 취사선택 | 재료는 이 스레드가 아니라 이 특허의 함수다(D14) |
| `response.json` 밖의 파일 쓰기 | 산출 자리는 하나다. 승인 봉투는 **어떤 경우에도** 작업 레인이 쓰지 않는다(SPEC §1.2 C3) |

## 6. 자주 틀리는 자리

| 혼동 | 정답 |
|---|---|
| `grounding.component`가 element id인가 | **아니다.** component **항목의 `M<n>`**이다 |
| `value_span`이 원천 파일 오프셋인가 | **아니다.** `quote` 문자열 **내부의** 문자 오프셋(0-based, end exclusive) |
| `attaches_to`가 종속항 id를 가리킬 수 있는가 | **아니다.** 항상 독립항 element id다 |
| `figures[].asset_path`를 채우는가 | **아니다.** 영구히 `null`이다 |
| `figures[].numerals`가 본문 숫자 대조 대상인가 | **아니다.** 도면부호는 수치 사실이 아니다. 쓰려면 `fact` 항목으로 별도 등재한다 |
| 접지가 없으면 그 구성요소를 빼는가 | **아니다.** 빼면 `read.coverage`가 잡는다. 예외로 신고한다 |
