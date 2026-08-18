# D5 ④⑤ — 유기적 통합 + 포지셔닝 + 기술적 함의

**너의 작업(`synthesize`).** 분해된 골격 위에서 ④ 이 발명이 **하나의 물건으로서 무엇을 하는가**를 세우고, ⑤ 배경기술 대비 **무엇이 달라졌다고 주장하는가**를 세운다. 수치 사실과 도면 등재, 그리고 최종 drop 신호도 이 단계의 산출이다.

받는 조각은 셋이다 — `claims-section` · `description-paragraphs` · `figure-captions`.

---

## 1. 기술적 함의 (`kind: "implication"`) — D5 ④

```json
{ "id": "M6", "kind": "implication", "status": "active", "superseded_by": null,
  "statement_en": "Forming the channel inside the spreader body points at removing a cold plate rather than adding one.",
  "basis": "spec", "derived_from": ["M2", "M4"], "numeric_refs": ["M31"],
  "evidence_quotes": ["the channel is formed within the spreader so that a separate cold plate is not required"],
  "confidence": "inferred" }
```

- `basis` ∈ `claim` · `spec` · `background` · `effects` — **어디에서 왔는가**.
- `confidence` ∈ `stated`(문언으로 그렇게 적혀 있다) · `inferred`(우리가 이었다). 이 둘을 섞지 마라. 명세서가 말하지 않은 것을 `stated`로 적는 것이 가장 값비싼 거짓말이다.
- `derived_from`은 실재하는 항목 ID여야 하고, `evidence_quotes[]`는 원천의 바이트 정확 부분문자열이어야 한다.
- **`numeric_refs`(필수, 빈 배열 허용)** — 이 함의가 **근거로 삼은 수치 항목의 ID 목록**이다. 수치를 새로 만들지 않고, 요청 지시에 실린 **수확 목록**에서 골라 참조 ID로 적는다(재정 P-B). 근거 수치가 없는 함의면 빈 배열이다.

## 2. 포지셔닝 (`kind: "positioning"`) — D5 ⑤

```json
{ "id": "M7", "kind": "positioning", "status": "active", "superseded_by": null,
  "background_problem": "…", "asserted_effect": "…", "delta": "…",
  "numeric_refs": ["M31", "M44"], "quotes": ["…원문 그대로…"] }
```

세 필드는 **주장의 출처가 명세서**라는 사실을 유지한 채 적는다. `asserted_effect`는 "명세서가 그렇게 주장한다"이지 "그렇다"가 아니다. 성능 수치가 없으면 `delta`에 구조적 차이를 적고, 없는 수치를 만들지 않는다.

`numeric_refs`는 함의와 같은 규율이다(필수, 빈 배열 허용) — 포지셔닝이 근거로 든 수치를 **수확 목록에서 골라 참조 ID로** 적는다.

## 3. 수치 사실 (`kind: "fact"`) — ★ 원문 수치는 네가 만들지 않는다 (재정 P-B)

**수치 사실의 수확은 기계가 전수로 한다.** 접지 레인이 붙인 명세서 인용 스팬 전량과 서지 필드에서 엔진이 `origin: "quoted"`·`"bibliographic"` 항목을 **빠짐없이** 만들어 두었고, 그 목록이 이 요청의 지시에 실려 있다. **너는 그중에서 고른다** — 만들지 않는다.

| origin | 소유자 | 네가 할 일 |
|---|---|---|
| `quoted` | **엔진(수확기)** | 만들지 마라. `numeric_refs`로 **참조**한다 |
| `bibliographic` | **엔진(수확기)** | 만들지 마라. 참조한다 |
| `derived` | **너** | 산식으로 얻는 값은 네 몫이다(아래 규율 그대로) |
| `figure-sourced` | **너** | 도면 판독값은 기계가 수확할 수 없다. 네 몫이다 |

**왜 이렇게 바뀌었나.** 구 규정은 ⑤단계 레인이 "중요한 수치"를 골라 등재하게 했고, 그것은 **서사가 정답지를 고르는 구조**였다. 도면을 선택분만 편집하지 않는 이유(D12 전량 선편집)와 같은 논리로 수치도 전수 수확한다 — 선택이 생성보다 앞서면 선택되지 않은 것은 존재조차 하지 않게 되고, 나중에 필요해졌을 때 되돌아갈 자리가 없다. **고르는 일은 네가 아니라 `numeric_refs` 역참조가 한다.**

`origin: "quoted"`·`"bibliographic"` 항목을 네가 만들면 `read.value-derivation`의 `value.harvest-parity`가 **수확기 재실행 결과와 대조해 실패**시킨다. 조용히 통과하지 않는다.

아래 표는 네가 만드는 두 갈래(`derived`·`figure-sourced`)의 규율이며, 나머지 둘은 수확기가 같은 규율로 만든 것을 참고로 싣는다. origin 4갈래는 **상호 배타**다 — 한 항목이 다른 origin의 부속 필드를 함께 가질 수 없다.

| `origin` | 부속 필드 | `machine_verifiable` | 무엇이 보증되는가 |
|---|---|---|---|
| `quoted` | `source: {locator, quote, value_span}` | `true` | 원문 스팬과 값이 **바이트로** 일치 |
| `derived` | `derivation: {formula, inputs, rounding}` | `true` | 산식 **재계산**이 값과 일치 |
| `figure-sourced` | `figure_source: {figure, numerals, locator}` | `false` | **아무것도 보증되지 않는다**(사람이 본다) |
| `bibliographic` | `bib_source: {field}` | `true` | `patent` 블록에서 결정론 복사 |

- `value_span`은 **`quote` 문자열 내부의** 문자 오프셋이다(원천 파일 오프셋이 아니다).
- `derivation.inputs[].ref`는 **`origin: "quoted"`인 fact만** 가리킬 수 있다(깊이 1). 파생의 파생은 거부된다 — 원문 스팬까지의 거리가 무한해지면 재계산 대조가 사슬 어딘가에서 끊긴다.
- `formula`는 안전 산술식만 쓴다: 입력 이름 · 십진 리터럴 · `+ - * / ( )`.

### `value_type` — 7분기 판별 유니온

값의 표현 유형을 구조로 담는다. `value_raw`를 파싱한 결과와 같아야 하고, `value_normalized`는 그 렌더와 문자열로 같아야 한다.

| `kind` | 예 (`value_raw` → `value_type` → `value_normalized`) |
|---|---|
| `scalar` | `0.08 mm` → `{kind:"scalar", approximate:false, value:"0.08"}` → `0.08` |
| `range` | `0.05-0.10 mm` → `{kind:"range", low:"0.05", high:"0.1", low_inclusive:true, high_inclusive:true}` → `0.05-0.1` |
| `inequality` | `at least 5` → `{kind:"inequality", bound:"5", direction:"at-least"}` → `>=5` |
| `tolerance` | `100 ±5%` → `{kind:"tolerance", center:"100", tolerance:"5", tolerance_unit:"percent"}` → `100+-5%` |
| `set` | `4, 8, 16` → `{kind:"set", members:["4","8","16"]}` → `4;8;16` |
| `date` | `2024-03-11` → `{kind:"date", value:"2024-03-11"}` → `2024-03-11` |
| `identifier` | `XX0000000A1` → `{kind:"identifier", value:"XX0000000A1"}` → `XX0000000A1` |

- `approximate`는 kind와 **직교**한다. "about 0.08"은 `approximate: true`이고 렌더 앞에 `~`가 붙는다. "약 0.08"과 "0.08"은 다른 주장이다.
- **origin ↔ kind 결속**: `bib_source.field == "patent.number"`이면 `identifier`, 날짜 3종이면 `date`다. 순전히 숫자로 된 공개번호를 `scalar`로 적으면 정답지에 '수치'가 하나 늘어난다.
- 십진 표기 규율: 선행 `+` 금지 · 선행 0 패딩 금지 · 후행 0 금지(`0.80`→`0.8`) · 과학표기 전개 · **음의 0(`-0`) 금지**.
- 분수(`1/2`)와 혼합 단위 범위(`1 mm to 2 cm`)는 지원하지 않는다. **조용히 근사하지 말고** 그 값을 fact로 등재하지 마라.

## 4. 도면 (`figures[]` · `kind: "figure_note"`)

```json
{ "id": "FIG-2", "numerals": ["110", "210"], "caption_quote": "…원문 그대로…",
  "raw_path": "00-source/figures-raw/fig-02.png", "asset_path": null }
```

- `asset_path`는 **항상 `null`**이다. 도면↔자산 매핑의 정본은 편집 단계의 `manifest.json` 하나뿐이며, 동결본이 그 값을 들면 하류가 동결본을 고칠 수 있다는 뜻이 된다.
- `figure_note` 항목은 "이 도면이 무엇을 보여주는가"를 EN 한 문장으로 적는다.

## 5. 최종 drop 신호 (D4 2단 — 확정 재정은 CP1이 한다)

포지셔닝 확정 후 최종 판정을 낸다.

```json
{ "stage": "final", "verdict": "go", "reason": "…KR…" }
```

`drop-proposed`의 사유 표기는 **`안도감 부적합`** 계열이다 — 도면 부족 같은 **형식 전제 미충족**과는 판단의 종류가 다르며, 후자는 이미 `source` 단계에서 걸러진다.

**★ 이 신호도 상신이 아니라 제안이다(재정 P-A).** `drop-proposed`를 내도 러너는 멈추지 않고 CP1까지 간다 — drop의 구속력 있는 결정은 **재료 승인과 한 자리**에서 1회 내려지며, 그 결정은 승인 봉투의 `drop_decision`에 남는다. 따라서 네 판정은 **완전한 정보를 갖춘 Owner에게 올라가는 의견**이고, 그렇게 쓰면 된다.

**★ 분해 레인의 맹검 메모는 너에게 주어지지 않는다.** 앵커링을 막기 위해서다(재정 P-A). 그 메모와 네 최종 판정이 갈리는지 아닌지가 CP1에서 처음 대조되며, **갈린다는 사실 자체가 신호**다. 그러므로 없는 것을 추측해 맞추려 하지 마라.

## 6. 산출 형태

`40-output-contract.md`의 `synthesis` 절을 그대로 따른다. 필수 최상위 키는 `items` · `figures` · `drop_signal` 셋이다.
