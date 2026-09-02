# D5 독해론 5단계 — 절차 개요

**지위.** 이 폴더(`reader/procedure/`)는 독해 레인이 읽는 **절차 정본**이다. 러너는 각 요청의 `request.md`에 해당 절차 문서를 인라인으로 실어 보낸다 — 링크로만 주면 레인마다 열람 여부가 갈리고, 그 순간 두 독립 실행이 같은 절차를 따랐다는 보장이 사라진다(수렴 검사의 전제). 개정 이력·실측 근거·정정 마커는 같은 폴더의 `HISTORY.md` 에 두고 요청서에는 실지 않는다 — 절차 문서는 **현행 규약만** 적는다.

**이식 단위 안에 있다.** `reader/`는 patent-historian과 공유하는 이식 단위다(D14). 따라서 이 문서들은 **특허를 읽는 일**만 말하고 출력 채널(X 스레드·트윗 수·훅)을 모른다. 서사·형식을 아는 문장이 여기 들어오면 그것은 결함이다 — 재료는 이 스레드가 아니라 이 특허의 함수여야 한다.

---

## 1. 다섯 단계와 산출물

| D5 단계 | 작업(task) | 절차 문서 | 산출 |
|---|---|---|---|
| ① 청구항 구성요소 전 분해 | `decompose` | `10-decompose.md` | `claims` · `items[kind: component]` · 조기 `drop_signal` |
| ② 관계 트리 도식화 | `decompose` | `10-decompose.md` | 위와 같은 산출에서 러너가 `10-read/claim-trees/`를 만든다 |
| ③ 3중 접지 | `ground-independent` / `ground-dependent` | `20-grounding.md` | `items[kind: grounding]` |
| ④ 유기적 통합 | `synthesize` | `30-synthesis.md` | `items[kind: implication]` |
| ⑤ 포지셔닝 | `synthesize` | `30-synthesis.md` | `items[kind: positioning]` · `items[kind: fact]` · `figures` · 최종 `drop_signal` |

산출 JSON의 형태와 금지 사항은 `40-output-contract.md`가 정본이다.

## 2. 독립 2회 실행

같은 절차를 두 번 독립으로 돈다(`read-a`·`read-b`). **두 실행은 서로의 산출을 보지 않는다.** 같은 세션의 재생성은 독립 실행이 아니다.

이것이 품질 장치가 아니라 **안정성 장치**라는 점을 오해하지 마라. 두 독해가 다른 청구항 트리를 낳는다면 그 소재에 대한 독해는 재현되지 않는 것이고, 이후 모든 결정론 검사의 기준점이 흔들린다. 그래서 수렴 미달은 "누가 틀렸는가"가 아니라 **절차 신호**로 Owner에게 올라간다.

정본 재료는 `read-a`의 산출이며 `read-b`는 수렴 비교 전용이다. 그렇다고 `read-b`를 대충 하면 비교가 무의미해진다.

## 3. 무엇을 보지 않는가

독해는 서사·훅을 **모르는 상태**에서 수행된다. 다음은 이 레인의 금지 열람이다(`contracts/stages/read.yaml#must_not_read`).

- `20-design/**` (블루프린트) · `40-compose/**` (초안, 재료 반려서 제외) · `50-gate/**` · `65-critique/**` · `ledgers/anchors/**`

블루프린트나 초안을 본 독해 레인은 "쓰기 좋은 재료"를 향해 편향된다.

## 4. 무엇이 너를 검사하는가

산출은 결정론 검사 **9종**을 통과해야 한다(`reader/lib/`). 검사가 판정하는 것은 "독해가 옳은가"가 아니라 **"독해가 자기 산출물에 대해 거짓말을 하지 않았는가"**뿐이다.

| 검사 | 네가 실패하는 전형적인 방식 |
|---|---|
| `read.schema` | 필수 필드 누락 · `origin` 부속 필드 혼입 |
| `read.source-digest` | 네 잘못이 아니다 — 원천이 도중에 바뀌었다는 신호이며, 이것이 실패하면 아래 전부가 무의미하다(불변식 I1) |
| `read.verbatim` | 원문을 **다듬어** 인용(공백·따옴표·줄바꿈 한 글자라도 다르면 실패) |
| `read.pointer-resolve` | 유령 ID · 오타 · 자기참조 · 순환 |
| `read.coverage` | 접지 없는 구성요소 · 두 구성요소가 같은 component 항목 공유 |
| `read.dependency-parse` | `depends_on` 배열이 원문 인용 어형과 어긋남 |
| `read.value-derivation` | 인용문 옆의 **날조된 수치** · 정규화값 오기 · 파생의 파생 |
| `read.claim-inventory` | 원천 청구항 **누락** · 유령 청구항 |
| `read.convergence` | 두 실행의 트리·종속 구조 불일치 |

★ **인용은 복사한다. 옮겨 적지 않는다.** 원천에는 NBSP·보이지 않는 문자가 섞여 있고, `read.verbatim`은 정규화 없이 바이트 비교한다. 눈으로 옮겨 적은 인용은 반드시 실패하며 **그 실패가 정상 동작이다**.

## 5. 실패했을 때

러너는 재시도 1회를 준다. 재시도 요청의 `request.md`에는 **직전 판의 결함 목록**(좌표·실측·기대)이 붙는다. 같은 자리를 같은 방식으로 다시 적으면 그 재시도는 낭비다. 두 번째도 실패하면 Owner에게 올라간다.
