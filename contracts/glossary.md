# 계약층 식별자 사전 (glossary)

**지위.** 이 파일은 **식별자 사전**이지 개념 사전이 아니다. 개념·용어의 정본은 `docs/SPEC.md` §0.5 용어표이며, 여기 있는 것은 기계가 문자열로 주고받는 **이름들**의 목록이다 — 검사 id, 계약 라인, 산출물 경로, ID 문법, 상태·처분 어휘. 둘이 어긋나면 개념은 §0.5가, 이름은 이 파일이 각각 정본이다.

**왜 이름을 따로 모으는가.** M0.5 재감수 B-07이 실측한 실패가 근거다 — 같은 목록(숫자 화이트리스트)을 세 자리가 서로 다른 키 이름으로 적어 두어 **셋을 동시에 만족하는 로더가 존재할 수 없었다.** 이름의 표류는 개념의 표류보다 조용하고, 조용한 만큼 늦게 발견된다.

**갱신 규율.** 새 검사·새 산출물·새 계약 라인을 만들면 이 표에 등재한다. 등재하지 않은 이름을 코드가 쓰기 시작하면, 그 이름은 계약이 아니라 관습이 된다.

---

## 1. 계약 라인 (`<name>/vN`)

계약 라인은 소비자가 즉시 거부 판정을 내리는 식별자다. 값이 다르면 그 인스턴스는 읽지 않는다.

| 계약 라인 | 선언 파일 | 무엇의 계약인가 |
|---|---|---|
| `material-spec/v0` | `reader/schemas/material-spec.schema.json` | **재료 명세 — 프로젝트 간 계약(D14).** 유일하게 리포 밖(historian)과 공유된다. **두 층으로 갈린다**(재정 P-2 ⓑ) — 공유 코어 10키(사실면: 서지·청구항·도면·항목·내력)와 프로젝트 확장 블록(`extensions.<ns>`, 편집 판단). 라인은 `v0` 그대로다(`0.x` 미동결이므로 승격 사건이 아니다) |
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
| 구현 버전 | `reader_version: "0.8.0"` | 인스턴스 필드 + `reader/READER-VERSION` | 필드 추가·검사 강화 = minor · 버그 수정 = patch |
| 인스턴스 버전 | `spec_version: 2` | 인스턴스 필드 | 동결 스탬프. 개정 시 +1 단조 증가 |

---

## 2. 검사 id

검사 id는 `<스테이지>.<검사>` 형태이며, 판정 행(`verdict-check-row/v0`)의 `check_id`가 이 값을 그대로 싣는다.

### 2.1 구현된 것 (M1)

| 검사 id | 구현 | 무엇을 반증하는가 |
|---|---|---|
| `read.input-digest` | `engine/stages/__init__.py` | 선언 입력의 지문이 어긋난 채로 스테이지가 진행됨 — 불일치는 품질 결함이 아니라 **환경 오류**다(재정 P-C) |
| `read.schema` | `reader/lib/schema_check.py` | 인스턴스가 계약 스키마 밖 |
| `read.source-digest` | `reader/lib/source_digest.py` | **전제 검사** — `sha256(원천) != patent.source_digest`. 불변식 I1이 깨지면 아래 verbatim 계열이 전부 무효다(SPEC §2.2) |
| `read.verbatim` | `reader/lib/verbatim.py` | 원문을 다듬어 인용하거나 없는 문장을 지어냄 |
| `read.pointer-resolve` | `reader/lib/pointers.py` | 유령 참조·오타 ID·자기참조·순환 · **항목 ID 중복**(규칙 `pointer.item-id-unique` — 불변식 I5. 스키마가 표현하지 못하는 자리다) |
| `read.coverage` | `reader/lib/coverage.py` | 청구항 일부를 읽지 않고 넘어감 · 접지 1건이 여럿을 덮음 · **고아 `component`**(규칙 `coverage.no-orphan-component`) |
| `read.dependency-parse` | `reader/lib/dependency_parse.py` | 다중 종속의 논리 형태를 잃거나 잘못 적음 |
| `read.value-derivation` | `reader/lib/derivation.py` | 인용문 옆에 날조한 수치 · 정규화값 오기 · 파생 사슬로 원천 흐림 · 범위를 스칼라로 뭉갬 |
| `read.bibliography` | `reader/lib/bibliography.py` | 서지 확장 6종이 원천 대조 없이 기입됨(발명자·출원인·분류 코드·우선권 번호의 자유 기입) · **우선권 관할·연도가 그 번호 곁 원천 표기와 무관함**(근접 대조) · 최우선일이 우선권 목록과 어긋남(재정 P-2 ⓐ · 2026-08-18 sol 감수 부분 판정) |
| `read.claim-inventory` | `reader/lib/inventory.py` | 원천 청구항이 통째로 누락됨 |
| `read.convergence` | `reader/lib/convergence.py` | 독해가 재현되지 않음(문언·트리·종속 구조) |
| `read.lane-log-shape` | `engine/stages/read.py` | 레인 로그가 계약 실행 형태와 다름 — 비정본 실행이 접지·통합을 돌았음이 **로그의 있음**으로 드러난다(재정 P-4·P-U3) |
| `freeze.id-monotonic` | `reader/lib/freeze_integrity.py` | 개정이 항목 ID를 지우거나 재번호 |
| `freeze.payload-immutable` | `reader/lib/freeze_integrity.py` | 개정이 기존 항목의 **내용**을 조용히 바꿈 |
| `source.input-digest` | `engine/stages/__init__.py` | 외부 투입물이 지문 기록 없이 런에 들어옴(재정 P-C) |
| `source.digest-recorded` | `engine/stages/source.py` | 다이제스트가 원천과 다름 |
| `source.claims-section` | `engine/stages/source.py` | 청구항 구간을 찾을 수 없음 |
| `source.figures-manifest` | `engine/stages/source.py` | 도면 부재·정렬 불능 |
| `source.figures-manifest-digest` | `engine/stages/source.py` | 도면 **세트 전체**의 지문이 없어 도면 교체를 감지할 수 없음 — 원천 변경은 항상 새 런이다(재정 P-U2) |
| `source.run-id` | `engine/stages/source.py` | 런 ID 문법 위반·디렉터리 불일치 |
| `source.exhibit-candidates` | `engine/stages/source.py` | 형식 전제 미충족(도면 부재 또는 후보 < 트윗 하한) |
| `freeze.input-digest` | `engine/stages/__init__.py` | 동결 대상이 진입 시점에 선언된 것과 다름(재정 P-C) |
| `freeze.approval-valid` | `engine/stages/freeze.py` | 봉투 부재·실효·ack 집합 불일치 |
| `freeze.digest-match` | `engine/stages/freeze.py` | 원천 다이제스트 불일치 |
| `freeze.readonly` | `engine/stages/freeze.py` | 동결본이 쓰기 가능 |
| `freeze.render-parity` | `engine/stages/freeze.py` | **CP1 판독본이 항목의 EN 값을 빠뜨림** — 검사 대상은 항목 ID 의 존재가 아니라 **값의 바이트 존재**다(재정 P-U5). ID 만 보면 값이 요약·번역으로 바뀌어도 통과한다 |

### 2.2 계약에만 있고 아직 구현이 없는 것

이 목록이 짧아지는 것이 로드맵의 진척이다. **여기 있는 id를 "검사가 있다"고 말하지 마라** — 그것이 M0.6 재감수가 과장 보고로 판정한 종류의 서술이다.

| 검사 id | 소관 | 정본 서술 |
|---|---|---|
| `run.publish-preconditions` | M4 | `contracts/run-kinds.yaml` · SPEC §4.4 |
| `format.*` · `citation.*` · `numeric.exhaustive` · `annotation.*` | M4 | `contracts/l0-format.yaml` |
| `numeric.unreviewed-use` | M4 | `contracts/l0-format.yaml` §7 · SPEC §4.4.4 — **거부권 없는 자문 플래그**다(재정 P-B). 전수 수확이 넓힌 정답지의 대가를 받는 짝 규칙이며, 미참조(미검토) 수치를 본문이 처음 인용하면 CP2 봉투에 플래그가 붙는다 |
| `gate.no-rewrite` · `gate.final-eyes` | M4·M6 | SPEC §4.7·§1.10 |
| `gate.no-score` · `critique.no-score` | M4·M8 | `contracts/lexicon/score-lint.yaml` |
| `design.spec-digest` · `compose.spec-digest` | M5 | SPEC §7.3 (재정 N11) |
| `design.anchors-adjudicated-only` · `critique.anchors-adjudicated-only` | M5·M8 | SPEC §1.7·§1.12 |
| `probe.independence` · `probe.input-clean` · `probe.no-self-report` · `probe.target-coverage` · `probe.grader-separation` | M7 | SPEC §1.11 — **계기 5종.** ★ 2026-08-19 등재(누락 보수): SPEC §1.11이 이 다섯을 선언하는데 이 사전의 어느 절에도 없었다. 사전이 스스로 내건 갱신 규율("새 검사를 만들면 이 표에 등재한다")이 계기 계열에서만 지켜지지 않은 자리이며, 그 결과 §2.2 목록을 읽고 "M7에 무엇이 남았는가"를 세면 다섯이 빠졌다. **id 신설이 아니라 사전의 누락 보수다** — 이름은 SPEC이 이미 선언했고 여기 옮겨 적을 뿐이다. 정족수 판정 층(`engine/quorum.py`)은 구현되었으나 그것은 검사가 아니라 순수 함수이며 검사 id를 발행하지 않는다 |
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
| 종속 형태 | `single` · `multiple-and` · `multiple-or` · `unclassified`(**도달 가능** — Markush·조건부·수단항·카테고리 전환의 구조 미분류 표지) | `reader/reader-rules.yaml#dependency_citation` |
| drop 단계·판정 | stage: `early` · `final` / verdict: `go` · `drop-proposed` | material-spec 스키마 |
| 실패 조치 | `retry(n)` · `escalate` · `halt` · `reject-upstream` | SPEC §1.2 C6 |
| escalate 사유 | `형식 전제 미충족`(source) · `안도감 부적합`(read/D4) · `독해 프로파일 상신`(read/수렴 상신 축 미달 — 재정 P-3) · `환경 오류`(진입 지문 불일치 — 재정 P-C, 조치는 `halt`) | 재정 N12 · P-3 · P-C |
| 검사 상태 | `pass` · `fail` | `verdict-check-row/v0` |
| 수렴 축 정책 | `exact-match`(구조 사실 — 미달 = **법**, 판정 행 fail) · `escalation-trigger`(해석 여지 — 미달 = **상신**, fail 아님) · `measure-only`(**판정 제외**, 값만 기록) | `reader/reader-rules.yaml#convergence` · `convergence/v0` (재정 P-3) |
| 수렴 축 상태 | `pass` · `fail` · `escalate` · `measured` | `convergence/v0` — **검사 상태 2종과 다른 축이다**(판정 행의 pass/fail 과 혼동 금지, 재정 P-3) |
| 지표 수집 상태 | `collected` · `not-collected`(= **미수집**) | `metrics-row/v0` — 결측·공허 어휘와 구별한다(재정 P-7) |
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
| `10-read/convergence-early.json` | `read` | **조기 수렴 판정서**(`convergence/v0`, `phase: "early"`). 분해 직후 산출이며 접지 스테이지의 **선언 입력**이다(재정 P-4·P-U3) |
| `10-read/convergence-continue.md` | 오케스트레이터 | Owner **'계속' 봉투**(`approval-envelope/v0`). 재료가 아니라 **판정서 자체**에 결속된다 — `target.digest` == 판정서 파일의 SHA-256. **작업 레인은 쓰지 않는다**(재정 P-U3) |
| `10-read/convergence.json` | `read` | 검사 보고서(`convergence/v0`, `phase: "full"`) |
| `10-read/lanes/` | `read` | 레인 왕복 기록(지시·응답). `read.lane-log-shape` 가 이 형태를 판정한다 |
| `15-frozen/material-spec.v<N>.json` | `freeze` | **동결본.** 0444. 하류가 읽는 유일한 재료 |
| `15-frozen/approval-v<N>.md` | 오케스트레이터 | 승인 봉투. **작업 레인은 쓰지 않는다**(SPEC §1.2 C3) |

**런 밖의 원장 하나**(위 표와 층이 다르므로 따로 적는다).

| 경로 | 기록 스테이지 | 정본 관계 |
|---|---|---|
| `ledgers/shadow/screening.jsonl` | `read` | 맹검 스크리닝 메모의 **섀도 원장** — 런 디렉터리가 아니라 리포 루트에 누적된다. **재료 명세 계약면 밖**이며(재정 P-U4) 어떤 스키마 인스턴스에도 실리지 않는다. 한 행 = 메모 2건 + 최종 평가 + Owner 재정 |

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
| `FIG. 60`의 `60`도 도면부호 배제로 걸리는가 | **아니다 — 다른 배제다.** 도면부호(`figures[].numerals`)는 **부품**을 가리키고 도면·표 번호는 **그림 자체**를 가리키므로, 전자는 `figure-numeral`(집합 소속 3조건)이 잡고 후자는 봉투 배제 `figure-or-table-number`(`match: enclosing-pattern`)가 잡는다. 구 판은 후자를 잡지 못해 `FIG. 60`의 `60`이 스칼라 수치로 정답지에 올랐다(2026-08-18 통주 2 실측 4건). **한 지시가 두 번호를 드는 나열**(`Tables 1 and 2`)의 **뒤 항**은 또 다른 어형이라 그 봉투에 들지 않았고, **행·열 좌표**(`Row 0`·`Col 0`)는 도면부호 집합에도 토큰 경계에도 걸리지 않는 **두 방어 사이의 틈**이었다 — 그 셋이 재정 2026-08-19 S7의 건별 배제 대상(M87~M89)이며 `figure-or-table-number-list`와 `row-column-coordinate`가 신설되었다(사유 라벨은 앞의 것이 `figure-or-table-number`를 공유한다 — 잃은 자리의 **사유**가 같기 때문이다). **★ 계수 정정(2026-08-31 · 오류 수정 = 총괄 재량 · 규율 11 ③).** 구 문언은 *"봉투 배제는 현재 **6종**이다"* 였고 그것은 **낡은 수**다 — `row-column-coordinate` 는 신설 당일 후속 보수로 **봉투가 아니라 토큰 조건 규칙**이 되었는데(그 항목의 `form_change` — 봉투가 `a column 12 mm wide` 의 진짜 값을 삼켰다) 이 셀이 따라가지 않았다. **실측 = `match: enclosing-pattern` 5종 + 토큰 조건 규칙 2종(`figure-numeral` · `row-column-coordinate`) = 목록 항목 7.** 계수의 정본은 `reader/reader-rules.yaml#numeric_harvest.enclosing_exclusions.census` 이고 이 셀은 그것을 가리키는 사본이다(두 벌이 생기면 한 벌은 반드시 낡는다 — 이 정정이 그 실례다). 사유 라벨의 정본 = `reader/reader-rules.yaml#numeric_harvest.exclusions[].reason_label`. **★ 이 목록은 재정 2026-08-31 Q4 로 PD-M4 까지 동결되어 있다** — 선언 = 같은 파일 `numeric_harvest.exclusions_freeze` |
| `vacuous`를 손으로 적는가 | **아니다.** `ruleset_size`·`checked`에서 파생된다 |
| `superseded_by`가 `active`를 가리켜야 하는가 | **아니다(M1에서 교체됨).** 사슬을 따라간 **종단**이 `active`면 된다. 구 규칙은 2차 승계에서 동결본 수정을 강요했다(SPEC §9.27) |
| 값 언어 | **EN 단일.** 예외 2곳뿐 — `drop_signal.reason`·`grounding.search_note`(KR) |
| `derivation.inputs[].ref`가 무엇을 가리킬 수 있는가 | **`origin: "quoted"`인 `fact`만**(깊이 1). 원문 스팬을 들고 있는 origin은 그것 하나다(재정 N9, 재감수 M-01) |
| `drop_signal`이 최상위에 있는가 | **아니다(재정 P-2 ⓑ에서 이사했다).** 자리는 `extensions.docent.drop_signal` — drop은 사실이 아니라 **docent의 편집 판단**이고, 공유 코어는 두 프로젝트가 같은 의미로 읽는 사실면이다. historian은 이 블록을 기입하지 않는다. 경계는 `tools/check_spec_refs.py` K8이 집행한다 |
| `numeric_refs`가 무엇을 가리키는가 | **`kind: "fact"` 항목**(`M<n>`)이다. `implication`·`positioning`이 근거로 삼은 수치를 역참조하며, **중요분은 이 역참조로 도출된다** — LLM의 중요도 판단이 아니다(재정 P-B). 참조 무결은 `read.pointer-resolve`가 본다 |
| 원문 수치 `fact`를 누가 만드는가 | **엔진의 수확기**(`reader/lib/harvest.py`)다. 레인이 아니다 — `origin: "quoted"`·`bibliographic`은 접지 스팬에서 **전수 기계 수확**되고, 레인이 쓸 수 있는 것은 `derived`·`figure-sourced`뿐이다(재정 P-B) |
| CP1 판독본을 뭐라고 부르는가 | **"CP1 판독본(KR 틀 · EN 값)"**(재정 P-U5). 구 명칭 "KR 인간 판독본"은 폐기했다 — 장 제목·안내·라벨만 KR이고 인용·해설·함의의 EN 값은 그대로 실린다(파생 번역 금지) |
