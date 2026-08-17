# 계약층 식별자 사전 (glossary)

**지위.** 이 파일은 **식별자 사전**이지 개념 사전이 아니다. 개념·용어의 정본은 `docs/SPEC.md` §0.5 용어표이며, 여기 있는 것은 기계가 문자열로 주고받는 **이름들**의 목록이다 — 검사 id, 계약 라인, 산출물 경로, ID 문법, 상태·처분 어휘. 둘이 어긋나면 개념은 §0.5가, 이름은 이 파일이 각각 정본이다.

**왜 이름을 따로 모으는가.** M0.5 재감수 B-07이 실측한 실패가 근거다 — 같은 목록(숫자 화이트리스트)을 세 자리가 서로 다른 키 이름으로 적어 두어 **셋을 동시에 만족하는 로더가 존재할 수 없었다.** 이름의 표류는 개념의 표류보다 조용하고, 조용한 만큼 늦게 발견된다.

**갱신 규율.** 새 검사·새 산출물·새 계약 라인을 만들면 이 표에 등재한다. 등재하지 않은 이름을 코드가 쓰기 시작하면, 그 이름은 계약이 아니라 관습이 된다.

---

## 1. 계약 라인 (`<name>/vN`)

계약 라인은 소비자가 즉시 거부 판정을 내리는 식별자다. 값이 다르면 그 인스턴스는 읽지 않는다.

| 계약 라인 | 선언 파일 | 무엇의 계약인가 |
|---|---|---|
| `material-spec/v0` | `reader/schemas/material-spec.schema.json` | **재료 명세 — 프로젝트 간 계약(D14).** 유일하게 리포 밖(historian)과 공유된다 |
| `reader-rules/v0` | `reader/reader-rules.yaml` | 독해층 규칙 — 청구항 인벤토리 파싱·종속 인용 어형·항목 생애주기·수치 문법·수렴 축 |
| `stage-contract/v0` | `contracts/stages/*.yaml` | 스테이지 I/O 계약(서식 = `docs/SPEC.md` §1.2) |
| `convergence/v0` | `contracts/schemas/convergence.schema.json` | READ 결정론 검사 보고서 |
| `approval-envelope/v0` | `contracts/schemas/approval-envelope.schema.json` | 체크포인트 승인 봉투 |
| `verdict-check-row/v0` | `contracts/schemas/verdict-check-row.schema.json` | 게이트 판정 행 서식(재정 N5) |
| `metrics-row/v0` | `contracts/schemas/metrics-row.schema.json` | 지표 원장 행 |
| `l0-format/v0` | `contracts/l0-format.yaml` | L0 규칙 목록·문장 계수·숫자 문법 |
| `format-parameters/v0` | `contracts/format-parameters.yaml` | 형식 파라미터 시트 |
| `parameters/v0` | `contracts/parameters.yaml` | 조정 가능 파라미터 4종 |
| `run-kinds/v0` | `contracts/run-kinds.yaml` | 예행/게시 런 정의·전제조건 |
| `speech-acts/v1` | `contracts/lexicon/speech-acts.yaml` | 화행 술어 3종 |
| `defect-catalog/v0` | `contracts/lexicon/defect-catalog.yaml` | 결함 카탈로그 |
| `score-lint/v1` | `contracts/lexicon/score-lint.yaml` | 점수 금지 린트 패턴 |

**버전 축의 구별**(혼동 지점이다).

| 축 | 예 | 어디에 | 언제 오르는가 |
|---|---|---|---|
| 계약 라인 | `material-spec/v0` | 인스턴스 `schema` 필드 | 하위호환 파괴. **단 `0.x` 미동결 기간은 예외** — 자유이며 기록만 남긴다(재정 N15) |
| 구현 버전 | `reader_version: "0.4.0"` | 인스턴스 필드 + `reader/READER-VERSION` | 필드 추가·검사 강화 = minor · 버그 수정 = patch |
| 인스턴스 버전 | `spec_version: 2` | 인스턴스 필드 | 동결 스탬프. 개정 시 +1 단조 증가 |

---

## 2. 검사 id

검사 id는 `<스테이지>.<검사>` 형태이며, 판정 행(`verdict-check-row/v0`)의 `check_id`가 이 값을 그대로 싣는다.

### 2.1 구현된 것 (M1)

| 검사 id | 구현 | 무엇을 반증하는가 |
|---|---|---|
| `read.schema` | `reader/lib/schema_check.py` | 인스턴스가 계약 스키마 밖 |
| `read.verbatim` | `reader/lib/verbatim.py` | 원문을 다듬어 인용하거나 없는 문장을 지어냄 |
| `read.pointer-resolve` | `reader/lib/pointers.py` | 유령 참조·오타 ID·자기참조·순환 |
| `read.coverage` | `reader/lib/coverage.py` | 청구항 일부를 읽지 않고 넘어감 · 접지 1건이 여럿을 덮음 |
| `read.dependency-parse` | `reader/lib/dependency_parse.py` | 다중 종속의 논리 형태를 잃거나 잘못 적음 |
| `read.value-derivation` | `reader/lib/derivation.py` | 인용문 옆에 날조한 수치 · 정규화값 오기 · 파생 사슬로 원천 흐림 · 범위를 스칼라로 뭉갬 |
| `read.claim-inventory` | `reader/lib/inventory.py` | 원천 청구항이 통째로 누락됨 |
| `read.convergence` | `reader/lib/convergence.py` | 독해가 재현되지 않음(문언·트리·종속 구조) |
| `freeze.id-monotonic` | `reader/lib/freeze_integrity.py` | 개정이 항목 ID를 지우거나 재번호 |
| `freeze.payload-immutable` | `reader/lib/freeze_integrity.py` | 개정이 기존 항목의 **내용**을 조용히 바꿈 |
| `source.digest-recorded` | `engine/stages/source.py` | 다이제스트가 원천과 다름 |
| `source.claims-section` | `engine/stages/source.py` | 청구항 구간을 찾을 수 없음 |
| `source.figures-manifest` | `engine/stages/source.py` | 도면 부재·정렬 불능 |
| `source.run-id` | `engine/stages/source.py` | 런 ID 문법 위반·디렉터리 불일치 |
| `source.exhibit-candidates` | `engine/stages/source.py` | 형식 전제 미충족(도면 부재 또는 후보 < 트윗 하한) |
| `freeze.approval-valid` | `engine/stages/freeze.py` | 봉투 부재·실효·ack 집합 불일치 |
| `freeze.digest-match` | `engine/stages/freeze.py` | 원천 다이제스트 불일치 |
| `freeze.readonly` | `engine/stages/freeze.py` | 동결본이 쓰기 가능 |
| `freeze.render-parity` | `engine/stages/freeze.py` | KR 판독본이 항목을 빠뜨림 |

### 2.2 계약에만 있고 아직 구현이 없는 것

이 목록이 짧아지는 것이 로드맵의 진척이다. **여기 있는 id를 "검사가 있다"고 말하지 마라** — 그것이 M0.6 재감수가 과장 보고로 판정한 종류의 서술이다.

| 검사 id | 소관 | 정본 서술 |
|---|---|---|
| `run.publish-preconditions` | M4 | `contracts/run-kinds.yaml` · SPEC §4.4 |
| `format.*` · `citation.*` · `numeric.exhaustive` · `annotation.*` | M4 | `contracts/l0-format.yaml` |
| `gate.no-rewrite` · `gate.final-eyes` | M4·M6 | SPEC §4.7·§1.10 |
| `gate.no-score` · `critique.no-score` | M4·M8 | `contracts/lexicon/score-lint.yaml` |
| `design.spec-digest` · `compose.spec-digest` | M5 | SPEC §7.3 (재정 N11) |
| `design.anchors-adjudicated-only` · `critique.anchors-adjudicated-only` | M5·M8 | SPEC §1.7·§1.12 |
| `feedback.window` · `feedback.row-consistency` · `feedback.corrects-resolve` | M10 | SPEC §1.15 |

---

## 3. ID 문법

| 대상 | 문법 | 규율 |
|---|---|---|
| 재료 항목 | `^M[0-9]+$` | 런 내 순번. **추가 전용** — 재사용·재번호 금지 |
| 항목 전역 참조자 | `<run_id>#<item_id>` | historian 인덱스가 조립한다. 스키마에는 필드가 없다(SPEC §9.0 E1) |
| 청구항 | `^CL-[0-9]+$` | 원천 청구항 번호와 일치 |
| 구성요소 | `^CL-[0-9]+/e[0-9]+(/e[0-9]+)*$` | 중첩 시 경로가 길어진다 |
| 부가 한정 | `^CL-[0-9]+/a[0-9]+$` | 종속항의 분해 단위 |
| 도면 | `^FIG-[A-Za-z0-9-]+$` | 원천 표기 `FIG. 3` → `FIG-3` |
| 런 | `^[a-z0-9]+-[a-z0-9]+-[a-z0-9-]+$` | `<assignee-slug>-<pubnum>-<topic-slug>`. 생성 후 불변 |
| 다이제스트 | `^sha256:[0-9a-f]{64}$` | 소문자 hex 64자, `sha256:` 접두 |
| 정규화 십진 | `^-?(?:0\|[1-9][0-9]*)(?:[.][0-9]*[1-9])?$` | 선행 `+`·선행 0 패딩·후행 0·과학표기 금지 |
| 재정 원장 | `ruling-YYYYMMDD-nn-<안건범위>.md` | Owner의 문서 |
| 처분 기록 | `D-YYYYMMDD-nn-<slug>.md` | 총괄(opus-director)의 문서 — 원장이 아니다 |

---

## 4. 어휘 (닫힌 집합)

| 축 | 값 | 정본 |
|---|---|---|
| 항목 종류 | `component` · `grounding` · `fact` · `implication` · `positioning` · `figure_note` | material-spec 스키마 |
| 항목 상태 | `active` · `retracted` · `superseded` | material-spec 스키마 |
| 상태 전이 | `active → retracted` · `active → superseded` (**단방향, 종단에서 복귀 없음**) | `reader/reader-rules.yaml#item_lifecycle` |
| 명세 상태 | `draft` · `frozen` · `revised` | material-spec 스키마 |
| 수치 출처 | `quoted` · `derived` · `figure-sourced` · `bibliographic` (**상호 배타**) | material-spec 스키마 |
| 수치 타입 | `scalar` · `range` · `inequality` · `tolerance` · `set` (+ `approximate` 불리언, 직교) | material-spec 스키마 `$defs/value_type` |
| 부등호 방향 | `at-least` · `at-most` · `greater-than` · `less-than` | 동상 |
| 접지 상태 | spec: `found` · `no-anchor-found` / figure: `found` · `not-depicted` | material-spec 스키마 |
| 종속 형태 | `single` · `multiple-and` · `multiple-or` · `alternative-form`(**현행 파싱 규칙으로 도달 불능**) | `reader/reader-rules.yaml#dependency_citation` |
| drop 단계·판정 | stage: `early` · `final` / verdict: `go` · `drop-proposed` | material-spec 스키마 |
| 실패 조치 | `retry(n)` · `escalate` · `halt` · `reject-upstream` | SPEC §1.2 C6 |
| escalate 사유 | `형식 전제 미충족`(source) · `안도감 부적합`(read/D4) | 재정 N12 |
| 검사 상태 | `pass` · `fail` | `verdict-check-row/v0` |
| 공허 종류 | `none` · `empty-ruleset` · `empty-target` | `verdict-check-row/v0` (**파생값 — 신고값이 아니다**) |
| 승인 결정 | `approved` · `rejected` (**조건부 승인 제도 없음**) | `approval-envelope/v0` |
| 런 종류 | `rehearsal` · `publish` | `run-kinds/v0` |
| 출처 태그 | `[물리]` · `[전승]` · `[가설]` | 재정 N-D11 (`format-parameters.yaml` · `reader-rules.yaml` 공용) |
| 처분 어휘 | `해소` · `부분 해소` · `유보` | `docs/decisions/D-*.md` |

---

## 5. 산출물 경로 (런 내부)

전체 트리는 `docs/SPEC.md` §7.2가 정본이다. 아래는 M1이 실제로 만드는 것과 그 정본 관계만 추린 것이다.

| 경로 | 산출 스테이지 | 정본 관계 |
|---|---|---|
| `00-source/patent.md` | `source` | **원천 정본.** 이후 어떤 스테이지도 수정하지 못한다 |
| `00-source/patent.sha256` | `source` | 원천의 핀 |
| `00-source/source-report.json` | `source` | 조기 보고(재정 N12) — 도면 수·전시물 후보 수·산정 근거 |
| `10-read/material-spec.json` | `read` | 작업본(`status: draft`) |
| `10-read/material-spec.md` | `read` | `.json`의 **결정론 렌더**. CP1 주 표면 |
| `10-read/convergence.json` | `read` | 검사 보고서(`convergence/v0`) |
| `15-frozen/material-spec.v<N>.json` | `freeze` | **동결본.** 0444. 하류가 읽는 유일한 재료 |
| `15-frozen/approval-v<N>.md` | 오케스트레이터 | 승인 봉투. **작업 레인은 쓰지 않는다**(SPEC §1.2 C3) |

---

## 6. 자주 틀리는 자리

| 혼동 | 정답 |
|---|---|
| `value_span`이 원천 파일 오프셋인가 | **아니다.** `quote` 문자열 **내부의** 문자 오프셋(0-based, end exclusive) |
| `spec_refs[].span`은 무엇인가 | 원천 파일 바이트 오프셋. `quote`가 정본이고 `span`은 **실패 시 위치 지목용 힌트**다 — 둘이 어긋나면 `quote`가 이긴다 |
| `grounding.component`가 element id인가 | **아니다.** `component` **kind 항목의 `M<n>`**이다. 사슬 = element/addition → `material_id` → component 항목 → grounding |
| `attaches_to`가 무엇을 가리키는가 | **항상 element id.** 종속의 종속이라도 최종적으로 독립항 element를 가리킨다 |
| `figures[].asset_path` | 동결본에서 **영구히 `null`**. 도면↔자산 매핑의 정본은 `30-figures/assets/manifest.json` 하나(M0 감수 M21) |
| `figures[].numerals`가 숫자 대조 대상인가 | **아니다.** 도면부호는 본문에 등장할 이유가 없다. 쓰려면 `fact` 항목으로 별도 등재 |
| `vacuous`를 손으로 적는가 | **아니다.** `ruleset_size`·`checked`에서 파생된다 |
| `superseded_by`가 `active`를 가리켜야 하는가 | **아니다(M1에서 교체됨).** 사슬을 따라간 **종단**이 `active`면 된다. 구 규칙은 2차 승계에서 동결본 수정을 강요했다(SPEC §9.27) |
| 값 언어 | **EN 단일.** 예외 2곳뿐 — `drop_signal.reason`·`grounding.search_note`(KR) |
| `derivation.inputs[].ref`가 무엇을 가리킬 수 있는가 | **`origin: "quoted"`인 `fact`만**(깊이 1). 원문 스팬을 들고 있는 origin은 그것 하나다(재정 N9, 재감수 M-01) |
