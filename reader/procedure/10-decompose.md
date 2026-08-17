# D5 ①② — 청구항 구성요소 전 분해 + 관계 트리

**너의 작업(`decompose`).** 청구항 구간 전량을 읽고, 각 청구항을 구성요소 단위로 **전부** 분해한다. 요약하지 않는다. 고르지 않는다. **전 분해**는 문언 그대로다.

받는 조각은 둘이다 — `claims-section`(청구항 구간 전문)과 `bibliographic-head`(서지 머리). 명세서 본문은 이 단계에서 주지 않는다. 분해는 청구항의 일이고, 본문을 함께 보면 분해가 요약으로 미끄러진다.

---

## 1. 청구항 하나도 빠뜨리지 않는다

원천 청구항 목록은 러너가 별도로 파싱해 **양방향으로 대조**한다(`read.claim-inventory`). 하나가 빠지면 남은 것들이 아무리 잘 접지되어 있어도 실패한다. 취소 청구항(`(canceled)`)은 등재 의무에서 면제된다.

- 독립항 → `claims.independent[]`, 종속항 → `claims.dependents[]`. 이 분류는 **원문이 다른 청구항을 인용하는가**로 결정된다. 인용하면 종속항이다.
- 청구항 ID는 `CL-<원천 번호>`다. 번호를 다시 매기지 않는다.

## 2. 구성요소 분해

### 독립항 (`elements[]`)

- 각 element는 `{id, text_verbatim, material_id, children}`.
- `id` 문법은 `CL-1/e1`이고, 중첩되면 경로가 길어진다(`CL-1/e2/e1`).
- `text_verbatim`은 **원문 바이트 그대로**의 부분문자열이다. 전제부·연결어를 다듬지 마라.
- 하위 한정이 있으면 `children`으로 층을 만든다. 평평하게 펴면 ②의 관계 트리가 사라진다.

### 종속항 (`additions[]`)

- 각 addition은 `{id, attaches_to, text_verbatim, material_id}`.
- `id` 문법은 `CL-5/a1`.
- `attaches_to`는 **항상 독립항 element id**다. 종속의 종속이라도 최종적으로 독립항 element를 가리킨다 — 부가 한정은 골격 밑에 층위로 누적된다.
- **`additions`는 비울 수 없다.** 전문이 있는 종속항을 빈 배열로 두면 "전 구성요소 3중 접지"가 접지할 것이 없어서 공허하게 통과한다.

### 종속 관계 (`depends_on` · `dependency_type`)

원문의 인용 어형을 그대로 읽는다.

| 원문 어형 | `depends_on` | `dependency_type` |
|---|---|---|
| `of claim 1` | `["CL-1"]` | `single` |
| `of claims 1 and 3` | `["CL-1", "CL-3"]` | `multiple-and` |
| `of claim 1 or claim 5` | `["CL-1", "CL-5"]` | `multiple-or` |
| `of claims 1 to 3` | `["CL-1","CL-2","CL-3"]` | `multiple-or` |

★ `alternative-form`은 **선언하지 마라.** 현행 파싱 규칙 5종은 그 값에 도달하지 못하며, 선언하면 `read.dependency-parse`가 반드시 실패한다(그것이 지금의 정직한 처리다 — 신설은 재정 사항).

## 3. component 항목 만들기

element·addition 하나마다 `kind: "component"` 항목을 **1:1로** 만든다.

```json
{ "id": "M1", "kind": "component", "status": "active", "superseded_by": null,
  "claim_ref": "CL-1/e1", "label_en": "substrate having a first surface",
  "text_verbatim": "a substrate having a first surface;" }
```

- `claim_ref`는 자기를 가리킨 element·addition의 id와 **역방향으로 일치**해야 한다.
- 두 element가 같은 component 항목을 공유할 수 없다. 공유하면 접지 1건이 둘을 덮는다.
- `label_en`은 EN이다. 한글이 한 글자라도 들어가면 거부된다.

## 4. 출원인 관심 신호 (`applicant_interest`)

권리 관심이 어디에 걸려 있는지를 `kind: "implication"` 항목으로 만들고, `claims.applicant_interest[]`가 그것을 가리킨다. 이 단계에서 함의 항목을 만들지 못하겠으면 **빈 배열로 둔다** — 지어내지 않는다. (④단계가 함의를 낸다.)

## 5. 조기 drop 신호 (D4 1단)

분해 직후, 이 소재가 일반 독자에게 **"아, 그렇구나"의 안도감**을 줄 수 있는지 1차 판단해 `drop_signal`을 낸다.

```json
{ "stage": "early", "verdict": "go", "reason": "권리 관심이 한 구성에 뚜렷하고 …" }
```

- `verdict`는 `go` 또는 `drop-proposed`. `reason`은 **KR**이다(값 언어 EN 정책의 예외 2곳 중 하나).
- `drop-proposed`를 내면 러너는 **그 자리에서 멈추고** 접지·통합을 돌리지 않는다. 비용 절약이 아니라, 하류 산출물이 Owner의 판단을 오염시키는 것을 막기 위함이다.
- 판단이 서지 않으면 `go`다. drop 제안은 **적극적 주장**이며 사유를 적을 수 있을 때만 낸다.

## 6. 산출 형태

`40-output-contract.md`의 `decompose` 절을 그대로 따른다. 필수 최상위 키는 `claims` · `items` · `drop_signal` 셋이다.
