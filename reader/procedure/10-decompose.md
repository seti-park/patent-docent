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

#### ★ 경계 규약 (수렴의 전제 — 반드시 지켜라)

`read.convergence`는 두 독립 실행의 `text_verbatim`을 **문자열로** 비교한다. 따라서 같은 구성요소를 **어디서 끊었는가**가 한 글자라도 다르면 그 둘은 다른 원소로 세어진다. 아래 규약이 없으면 두 실행은 같은 특허를 같은 깊이로 읽고도 수렴하지 못한다.

**2026-08-18 실측** — 이 규약이 없던 상태로 실특허 1건을 두 번 독립 독해한 결과 element 집합 Jaccard가 **0.59**였다(임계 0.95). 원인의 절반이 아래 ①이었고(교정 시 0.75로 상승) 나머지가 ②였다. 두 실행 다 "바이트 그대로"를 지켰다 — 규약이 없었을 뿐이다.

| # | 규약 | 이유 |
|---|---|---|
| ① | **선두 등위접속사(`and`·`or`)와 그 뒤 공백은 element에 포함하지 않는다.** 열거의 마지막 항이 `and a heat spreader …`라면 element는 `a heat spreader …`부터다 | 접속사는 **열거의 문법**이지 구성요소의 일부가 아니다. 포함 여부가 갈리면 같은 구성요소가 두 문자열이 된다 |
| ② | **선행 구성요소를 수식하는 후치 수식절은 새 element가 아니라 그 구성요소의 `children`이다.** `…, the first format and the second format being flexible`처럼 앞에서 도입된 대상을 한정하는 절이 여기 해당한다 | 형제로 올리면 트리의 층이 하나 사라지고(②의 관계 트리 상실), 두 실행이 같은 절을 서로 다른 층에 놓는다 |
| ③ | **끝 구분자(`;`·`,`·`.`)는 element에 포함하지 않는다.** 열거 항의 끝은 구분자 **앞**이다 | 구분자는 열거의 문법이며 ①과 같은 이유다 |
| ④ | 위 셋을 적용한 뒤에도 **남은 문자열은 원문의 연속 부분문자열이어야 한다.** 잘라낸 자리를 메우려고 글자를 더하거나 고치지 마라 | `read.verbatim`은 바이트로 대조한다. 규약은 **어디서 자르는가**를 정할 뿐 무엇을 쓰는가를 바꾸지 않는다 |

**임계 0.95는 아직 재정되지 않았다**(`reader-rules.yaml#convergence.open_question`). 위 규약을 지킨 뒤에도 수렴하지 않는다면 그것은 네 잘못이 아니라 **절차 신호**이며, Owner에게 올라간다(SPEC §1.4). 억지로 맞추려고 다른 실행을 추측하지 마라 — 추측해서 맞춘 수렴은 아무것도 반증하지 못한다.

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
