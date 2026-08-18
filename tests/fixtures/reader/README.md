# reader 픽스처 코퍼스 — 정답을 아는 가공 특허

**전부 가공 데이터다.** 이 디렉터리의 특허는 픽스처 전용으로 지어낸 것이며, 실재 특허가 아니고
실재 특허를 인용하지도 않는다. 번호 `XX0000000A1` · 출원인 `Example Devices, Inc.` · 발명자 2인
(`Dana R. Example` · `Jordan L. Fixture`) · 우선권 번호 `XX-2024-000101` · IPC/CPC 코드는 전부 예시
전용 더미다(`docs/SPEC.md` §2.7).

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
| `base/material-spec.json` | 정상 인스턴스(`spec_version: 1`, `status: draft`). 검사 12종을 **전부 통과**해야 한다 |
| `base/peer-read.json` | 독립 2회차 READ. 항목 ID 배정 순서와 라벨 문언이 다르고 청구항 문언·트리·종속 구조는 같다 — 수렴 6축을 통과한다 |
| `base/material-spec.rev2.json` | 정상 개정본(`spec_version: 2`). 항목을 하나도 지우지 않고, 단일 승계 1벌과 2차 승계(A→B→C) 1벌을 담는다 |
| `manifest.json` | ★ 정답 원장. 러너 계약·하한(`floors`, 래칫)·케이스 목록·근거 |
| `invalid/*` | 변조본. 각 판은 자기 `role` 의 base 에서 **한 곳만** 다르다 |

## 원천이 담고 있는 것 (base/patent.md)

- 서지면 10행(`## Bibliographic data`): 공개번호 · **공보 종별** · 출원인 · **발명자 2인** ·
  **우선권 주장 1건** · 3일자 · **IPC 1건 · CPC 2건**. ★ 굵게 표기한 5행은 2026-08-18 이행에서
  더한 것이다 — 재정 P-2 ⓐ 가 서지 6종을 필수로 만들면서 `read.bibliography` 가 그 값들을
  원천의 **바이트 정확 부분문자열**로 대조하게 되었는데, 구 서지면에는 대조할 자리가 없었다.
  값을 지어내고 검사만 통과시키는 대신 원천에 그 자리를 만들었다(그 사실은 `manifest.json`
  의 `$comment` 에도 적혀 있다). 삽입 지점이 Description 앞이므로 이행에서 `spec_refs[].span`
  의 바이트 오프셋 전량이 +223 이동했고 `patent.source_digest` 도 재계산되었다.
- 독립항 2벌(장치 청구항 1, **방법 청구항 7 — 마크다운 강조 번호 `**7**.` 형식**). 청구항 1 은
  중첩 element 를 갖는다.
- 종속항 6벌: 단일 종속(2·6·8) · `claims 1 and 2`(4) · `claim 1 or claim 2`(5) ·
  `any one of claims 4 to 6`(9). `reader-rules.yaml#dependency_citation.forms` 의 rank 1·3·4·5 를
  각각 때린다.
- 취소 청구항 1건(`3. (canceled)`) — 인벤토리 면제 경로.
- 도면 캡션 2건, `[0041]`~`[0051]` 문단 로케이터 11건.
- **`[0051]` 좌표 표현 문단**(2026-08-18 추가). FP 3항 표기 `FP8 (1-5-2)`·`FP6 (1-3-2)` ·
  비트 슬라이스 `Act 0 <6:3>` · 아래첨자 인덱스 `C.sub.j−1` · 도면/표 번호 `FIG. 1`·`Table 2` 를
  한 문단에 모았고, **M30 의 접지 인용으로 등재되어 있다**. 이 문단이 접지 안에 있는 것이
  요점이다 — 봉투 배제(`reader-rules.yaml#numeric_harvest.exclusions` 의
  `match: enclosing-pattern` 4종)가 꺼지면 기준선에 `1-5`·`1-3`·`0`·`<6`·`3`·`1`·`1`·`2`
  여덟 건의 `[누락]` 이 생겨 **무변조 코퍼스가 즉시 깨진다**. 문서 서술이 아니라 기준선이
  그 규칙을 붙잡는 자리다. 문단은 원천 **끝에** 붙였으므로 기존 `spec_refs[].span` 은
  하나도 이동하지 않았고, `patent.source_digest` 만 재계산되었다.
- 수치 7종: 스칼라(`0.08 mm`) · 범위(`0.05 to 0.10 mm`) · 부등호(`at least 12 mm`) ·
  공차(`50 ±5 %`) · 집합(`320, 340, 360 °C`) · 날짜(서지) · 식별자(서지).
  `value_type` 7분기를 전부 실측한다.

## 쓰는 법

`manifest.json` 의 `base` 4자리를 읽어 정상 조합을 만들고, 케이스마다 `role` 이 지목한 한 자리를
그 케이스 파일로 대체한 뒤 검사 12종을 돌린다. 판정은 두 방향 모두를 본다.

1. `expect_fail` 의 검사가 **전부 실패**했는가 (검사가 그 결함을 실제로 잡는가)
2. 그 밖의 검사가 **전부 통과**했는가 (검사가 관할 밖을 넘보지 않는가)

## 알려진 계약의 구멍 (이 코퍼스가 드러낸 것)

| # | 구멍 | 상태 |
|---|---|---|
| 1 | `read.schema` 에 배정된 케이스가 **0건**이다. "전 변조본이 스키마를 통과해야 한다"와 "검사 11종 각각에 최소 1건"은 동시에 만족될 수 없다 — 스키마가 거부하는 판은 정의상 이 코퍼스에 들어올 수 없다. 스키마 집행의 실증은 `tests/fixtures/schema-enforcement/` 가 맡는다 | 설계상 공백. 정정하려면 두 코퍼스의 경계를 재정으로 못 박아야 한다 |
| 2 | ~~`implication.derived_from[]` 의 순환을 금지하는 문언이 없다~~ → **처분됨(2026-08-18)**. 스키마 `$comment (8)` 과 SPEC §2.8 표 8행이 비순환 간선을 **4종의 합집합**(`derivation.inputs[].ref` ∪ `implication.derived_from[]` ∪ `superseded_by` ∪ `grounding.component`)으로 다시 쓰였다. **코드가 이미 옳았고 계약이 낡았던 사례** | `invalid/pointer-derived-from-cycle.json` 이 이제 문언에 근거를 갖는다 |
| 3 | ~~`role: source` 케이스의 `patent.source_digest` 어긋남을 담을 자리가 없다~~ → **처분됨(2026-08-18)**. 검사 11종째 `read.source-digest` 가 신설되어 불변식 I1(SPEC §2.2)에 집행자가 생겼고, 원천이 바뀌면 다이제스트가 어긋난다는 사실이 감춰지지 않고 판정문에 드러난다 | `invalid/inventory-source-extra-claim.md` 의 `expect_fail` 이 그 사실을 선언한다 |
| 4 | ~~`dependency_type: "alternative-form"` 은 현행 파싱 규칙 5종으로 **도달 불능**이다~~ → **처분됨(2026-08-18)**. 재정 P-1 이 그 값을 enum 에서 **폐기**하고 `unclassified`(구조 미분류)를 신설했다. 구 픽스처 `invalid/dependency-type-alternative-form.json` 은 전제가 무너져 폐기했다 — 이제 스키마가 먼저 거부하므로 "스키마를 통과한 뒤에도 검증기가 잡는다"를 증명할 수 없고, 그것은 이 코퍼스의 정의 밖이다 | 같은 규칙 계열의 실제 위험(면제 표지를 회피 통로로 쓰는 경로)을 시험하는 `invalid/dependency-type-unclassified-escape.json` 으로 교체되었다. 폐기 근거는 `manifest.json` 의 해당 케이스 `basis` 에 남긴다 |
| 5 | ~~커버리지는 고아 `component` 항목을 보지 못한다~~ → **처분됨(2026-08-18)**. 청구항 쪽 대상만 훑던 탓에 청구항이 통째로 빠지면 셀 대상도 함께 빠져 통과했다(코퍼스 제작 중 참조 구현으로 실측·보고) | 검증기에 `coverage.no-orphan-component` 가 신설되어 닫혔다. `invalid/inventory-dependent-claim-deleted.json` 의 `expect_fail` 이 그 규칙의 존재를 붙잡는다 — 규칙이 사라지면 이 판이 즉시 불일치로 울린다 |
| 6 | ~~`verbatim` 과 `claim-inventory` 의 관할이 겹친다~~ → **처분됨(2026-08-18)**. 개별 청구항 구간 한정은 `read.claim-inventory` 단독이고 `read.verbatim` 은 청구항 절 전체를 범위로 본다 — 규칙 문언(`reader-rules.yaml#claim_inventory.rules.inventory.text-in-own-claim` 의 `why`)이 배정한 그대로 구현이 축소되었다 | `invalid/inventory-cross-claim-text.json` 의 `expect_fail` 은 규칙 문언을 따랐고, 코퍼스를 구현에 맞춰 굽히지 않은 채 버틴 동안 구현이 규칙 쪽으로 왔다 |
| 7 | ~~`read.bibliography` 에 배정된 케이스가 **0건**이다(2026-08-18 신설)~~ → **처분됨(2026-08-18)**. 서지 확장으로 검사는 `checked: 10` 으로 돌았으나 **거부하는 것을 보인 판이 없었다** — 통과만 있고 반증이 없는 검사는 이 리포가 반복해서 벌해 온 형태다 | 변조본 2건 신설로 닫혔다: `invalid/bibliography-fabricated-inventor.json`(`bib.inventors-in-source` — 원천 대조 갈래) · `invalid/bibliography-earliest-priority-mismatch.json`(`bib.earliest-priority` — 자기 정합 갈래). 검사의 두 갈래를 각각 한 건씩 때린다. 케이스 신설분(이 2건 + `pointer-numeric-ref-dangling`)에 맞춰 `floors.min_cases` 를 36 → 39 로 함께 올렸다 |
| 8 | **러너 계약에 "상신"을 적을 자리가 없다.** 재정 P-3 이 수렴 축을 세 층으로 갈랐다 — `exact-match`(실패) · `escalation-trigger`(**상신**) · `measure-only`(측정만). `expect_fail`은 실패/통과 두 값의 세계라서 가운데 층을 표현하지 못하고, 빈 배열도 허용하지 않는다. 그 결과 `convergence-element-split`·`convergence-element-reparented` 두 판은 **상신을 유발하는 것이 정답인데 도구는 불일치로 읽는다** | 미해소. 픽스처가 아니라 **도구**의 문제다. 두 케이스에 `expect_escalate`(실측된 상신 축)를 데이터로 선언해 두었으므로, `tools/check_validator_enforcement.py`가 그 필드를 판정 행의 `extras.axes[].status == "escalate"`와 대조하면 닫힌다. 그때까지 `expect_fail`의 구 선언을 **일부러 남겨** 도구가 울리게 둔다 — 통과하도록 기대를 지우면 이 판들은 아무것도 증명하지 않는 파일이 된다 |
| 9 | ~~기준선의 `quoted` fact 좌표가 수확기의 좌표와 다르다~~ → **처분됨(2026-08-18)**. 재정 P-B 이후 `origin: quoted` fact 는 수확기의 산출이고 그 `source.quote` 는 **접지 인용문 전체**인데, 구 코퍼스의 M13~M18 은 사람이 고른 **발췌**를 들고 있어 7건 중 7건이 짝지어지지 않았다 | **접지를 넓혀** 닫았다(수확 범위를 넓히는 쪽이 아니다 — 접지되지 않은 문장의 수치는 원천 대조로 뒷받침되지 않는다). M32·M34 의 인용을 같은 문장의 수치 서술까지 넓히고, M30 에 `[0048]` 인용을 하나 더 달고, M13~M18 의 좌표·값을 수확 산출로 교체했다. `value.harvest-parity` 위반 26 → 1 |
| 10 | **`value.harvest-parity` 가 항목 `status` 를 보지 않는다.** 대조 대상이 `kind == "fact"` 전량이라 `retracted`·`superseded` 항목까지 수확 산출과 짝지으려 든다. 그런데 수확기는 접지 인용과 서지면만 읽으므로 물러난 항목에 대응하는 산출을 낼 수 없고, append-only 규율은 그 항목을 `items[]` 에서 지우지 못하게 한다 — **결과적으로 수확 소유 fact 는 한 번 등재되면 영원히 철회·승계될 수 없다.** 스키마 `$comment (14)` 의 생애주기 규율과 정면으로 충돌한다 | 미해소(검증기 몫). 재현 표본 2건이 코퍼스 안에 있다 — `base` 의 **M24**(`retracted`, 청구항에서 읽은 수치라 접지 밖이다)가 기준선의 마지막 `value.harvest-parity` 위반 1건이고, `rev2` 의 **M14 → M46 승계**가 같은 형태다. 처방은 `_check_harvest_parity` 의 대조 집합을 `status == "active"` 로 좁히는 것이며, 그것이 재정 P-B 의 "명세가 담은 그 집합" 의 자연스러운 독해다(물러난 항목은 명세가 더는 주장하지 않는다) |
| 11 | ~~**우선권 주장의 관할과 날짜를 아무도 보지 않는다.**~~ → **처분됨(2026-08-18)**. sol 독립 감수 P-2 ⓐ 가 실특허 런에서 실측했다 — 우선권 관할을 전부 `KR` 로 바꿔도 `read.bibliography` 는 `pass`·`checked=16` 이었다. 총괄 재현이 절반을 정정했으나(날짜를 전부 `1900-01-01` 로 바꾸면 `bib.earliest-priority` 가 운다) **두 날짜를 정합적으로 함께 위조하면 통과한다**는 잔여 구멍이 남았다 | 근접 대조 2종 신설로 닫혔다(`bib.priority-jurisdiction-in-source`·`bib.priority-year-in-source`, 창 폭은 `reader-rules.yaml#bibliography.priority_window` 가 소유). 코퍼스 표본 2건: `invalid/bibliography-priority-jurisdiction-out-of-window.json`(원천에 실재하는 `IP` 를 창 밖에 두어 **전역 대조가 아님**을 반증) · `invalid/bibliography-priority-year-coherent-forgery.json`(정합 위조 — `read.value-derivation` 파급 2건을 manifest 에 선언). 실특허 런의 감수 재현은 `tests/test_m16_bibliography.py` 가 맡는다 |
| 12 | **좌표 표현이 수치로 읽혔다.** 통주 2 의 실특허 산출에서 `origin: quoted` 30건 중 **23건이 오파싱 아티팩트**였다 — FP 3항 표기 `FP8 (1-5-2)` 가 `range` 로 9건, 비트 슬라이스 `Act 0 <6:3>` 가 `inequality`+`scalar` 로 8건, 도면·표 번호가 4건, 아래첨자 인덱스가 2건. 게다가 `(1-5-2)` 의 **셋째 필드는 기록조차 없이 사라졌다**(경계 기각이 `continue` 하나였다) | **처분됨(2026-08-18)**. 봉투 패턴 배제 4종 신설(`match: enclosing-pattern` — 토큰이 아니라 **구간**을 먼저 표시한다) + 경계 기각의 `boundary-left`·`boundary-right` 기록. 코퍼스 쪽 표본 2벌 — 무변조 `base` 의 `[0051]` 접지(배제가 꺼지면 기준선이 깨진다) · `invalid/harvest-coordinate-artifact.json`(배제된 조각을 손으로 fact 로 올린 역방향 판) |

## 규율

- 값 언어는 **EN** 단일이며, `extensions.docent.drop_signal.reason` 과 `grounding.search_note` 만
  KR 이다(재정 R2 · 자리는 재정 P-2 ⓑ 의 층 분리로 최상위에서 확장 블록으로 옮겼다).
- 변조본을 새로 더할 때는 **base 에서 한 곳만** 바꾸고 `manifest.json` 에 그 한 곳을 적는다.
  등재하지 않은 고아 픽스처는 검산에서 실패한다.
