# reader 픽스처 코퍼스 — 정답을 아는 가공 특허

**전부 가공 데이터다.** 이 디렉터리의 특허는 픽스처 전용으로 지어낸 것이며, 실재 특허가 아니고
실재 특허를 인용하지도 않는다. 번호 `XX0000000A1` 와 출원인 `Example Devices, Inc.` 는 예시 전용
더미다(`docs/SPEC.md` §2.7).

## 무엇을 위한 것인가

M1 검증기(결정론 검사 6종 + 동결 검사)가 **실제로 무엇을 반증하는가**를 증명하기 위한 코퍼스다.
"검사가 통과했다"가 "검사가 무언가를 반증했다"를 뜻하지 않는다는 것이 M0.5·M0.6 의 교훈이므로
(`docs/SPEC.md` §2.6 말미), 각 검사마다 **그 검사만 실패시키는 표본**을 두어 관할을 데이터로 고정한다.

코퍼스는 **선언적**이다. 검사 코드에 의존하지 않으며, `manifest.json` 이 각 변조본의 정답
(`expect_fail`)과 변조 지점(`mutation`)과 문서 근거(`basis`·`traces`)를 적는다.

## 파일

| 경로 | 지위 |
|---|---|
| `base/patent.md` | 가공 원천 정본. 모든 인용의 기준점이며 `base/material-spec.json` 의 `patent.source_digest` 가 이 파일의 SHA-256 이다 |
| `base/material-spec.json` | 정상 인스턴스(`spec_version: 1`, `status: draft`). 검사 11종을 **전부 통과**해야 한다 |
| `base/peer-read.json` | 독립 2회차 READ. 항목 ID 배정 순서와 라벨 문언이 다르고 청구항 문언·트리·종속 구조는 같다 — 수렴 6축을 통과한다 |
| `base/material-spec.rev2.json` | 정상 개정본(`spec_version: 2`). 항목을 하나도 지우지 않고, 단일 승계 1벌과 2차 승계(A→B→C) 1벌을 담는다 |
| `manifest.json` | ★ 정답 원장. 러너 계약·하한(`floors`, 래칫)·케이스 목록·근거 |
| `invalid/*` | 변조본. 각 판은 자기 `role` 의 base 에서 **한 곳만** 다르다 |

## 원천이 담고 있는 것 (base/patent.md)

- 독립항 2벌(장치 청구항 1, **방법 청구항 7 — 마크다운 강조 번호 `**7**.` 형식**). 청구항 1 은
  중첩 element 를 갖는다.
- 종속항 6벌: 단일 종속(2·6·8) · `claims 1 and 2`(4) · `claim 1 or claim 2`(5) ·
  `any one of claims 4 to 6`(9). `reader-rules.yaml#dependency_citation.forms` 의 rank 1·3·4·5 를
  각각 때린다.
- 취소 청구항 1건(`3. (canceled)`) — 인벤토리 면제 경로.
- 도면 캡션 2건, `[0041]`~`[0050]` 문단 로케이터 10건.
- 수치 7종: 스칼라(`0.08 mm`) · 범위(`0.05 to 0.10 mm`) · 부등호(`at least 12 mm`) ·
  공차(`50 ±5 %`) · 집합(`320, 340, 360 °C`) · 날짜(서지) · 식별자(서지).
  `value_type` 7분기를 전부 실측한다.

## 쓰는 법

`manifest.json` 의 `base` 4자리를 읽어 정상 조합을 만들고, 케이스마다 `role` 이 지목한 한 자리를
그 케이스 파일로 대체한 뒤 검사 11종을 돌린다. 판정은 두 방향 모두를 본다.

1. `expect_fail` 의 검사가 **전부 실패**했는가 (검사가 그 결함을 실제로 잡는가)
2. 그 밖의 검사가 **전부 통과**했는가 (검사가 관할 밖을 넘보지 않는가)

## 알려진 계약의 구멍 (이 코퍼스가 드러낸 것)

| # | 구멍 | 상태 |
|---|---|---|
| 1 | `read.schema` 에 배정된 케이스가 **0건**이다. "전 변조본이 스키마를 통과해야 한다"와 "검사 10종 각각에 최소 1건"은 동시에 만족될 수 없다 — 스키마가 거부하는 판은 정의상 이 코퍼스에 들어올 수 없다. 스키마 집행의 실증은 `tests/fixtures/schema-enforcement/` 가 맡는다 | 설계상 공백. 정정하려면 두 코퍼스의 경계를 재정으로 못 박아야 한다 |
| 2 | ~~`implication.derived_from[]` 의 순환을 금지하는 문언이 없다~~ → **처분됨(2026-08-18)**. 스키마 `$comment (8)` 과 SPEC §2.8 표 8행이 비순환 간선을 **4종의 합집합**(`derivation.inputs[].ref` ∪ `implication.derived_from[]` ∪ `superseded_by` ∪ `grounding.component`)으로 다시 쓰였다. **코드가 이미 옳았고 계약이 낡았던 사례** | `invalid/pointer-derived-from-cycle.json` 이 이제 문언에 근거를 갖는다 |
| 3 | ~~`role: source` 케이스의 `patent.source_digest` 어긋남을 담을 자리가 없다~~ → **처분됨(2026-08-18)**. 검사 11종째 `read.source-digest` 가 신설되어 불변식 I1(SPEC §2.2)에 집행자가 생겼고, 원천이 바뀌면 다이제스트가 어긋난다는 사실이 감춰지지 않고 판정문에 드러난다 | `invalid/inventory-source-extra-claim.md` 의 `expect_fail` 이 그 사실을 선언한다 |
| 4 | `dependency_type: "alternative-form"` 은 현행 파싱 규칙 5종으로 **도달 불능**이다 | 규칙 파일이 스스로 데이터로 밝힌 사실(`unreachable_values`)이며, `invalid/dependency-type-alternative-form.json` 이 그 처리를 고정한다 |
| 5 | ~~커버리지는 고아 `component` 항목을 보지 못한다~~ → **처분됨(2026-08-18)**. 청구항 쪽 대상만 훑던 탓에 청구항이 통째로 빠지면 셀 대상도 함께 빠져 통과했다(코퍼스 제작 중 참조 구현으로 실측·보고) | 검증기에 `coverage.no-orphan-component` 가 신설되어 닫혔다. `invalid/inventory-dependent-claim-deleted.json` 의 `expect_fail` 이 그 규칙의 존재를 붙잡는다 — 규칙이 사라지면 이 판이 즉시 불일치로 울린다 |
| 6 | ~~`verbatim` 과 `claim-inventory` 의 관할이 겹친다~~ → **처분됨(2026-08-18)**. 개별 청구항 구간 한정은 `read.claim-inventory` 단독이고 `read.verbatim` 은 청구항 절 전체를 범위로 본다 — 규칙 문언(`reader-rules.yaml#claim_inventory.rules.inventory.text-in-own-claim` 의 `why`)이 배정한 그대로 구현이 축소되었다 | `invalid/inventory-cross-claim-text.json` 의 `expect_fail` 은 규칙 문언을 따랐고, 코퍼스를 구현에 맞춰 굽히지 않은 채 버틴 동안 구현이 규칙 쪽으로 왔다 |

## 규율

- 값 언어는 **EN** 단일이며, `drop_signal.reason` 과 `grounding.search_note` 만 KR 이다(재정 R2).
- 변조본을 새로 더할 때는 **base 에서 한 곳만** 바꾸고 `manifest.json` 에 그 한 곳을 적는다.
  등재하지 않은 고아 픽스처는 검산에서 실패한다.
