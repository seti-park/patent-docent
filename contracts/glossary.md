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
| `blueprint/v0` | `contracts/schemas/blueprint.schema.json` | 설계 산출 `20-design/blueprint.json`(재정 T64 ② · M5-a). 러너 6키 + 레인 필드 · 수치는 시트 포인터 |
| `extension-envelope/v0` | `contracts/schemas/extension-envelope.schema.json` | 부분 런 종료선 연장 봉투 `15-frozen/extension-v<N>.md`(재정 T64 ① · 총괄 재량 — `approval-envelope/v0` 의 checkpoint enum 을 넓히지 않는다) |
| `thread/v0` | `contracts/schemas/thread.schema.json` | 구조화 출하 객체 `50-gate/<v>/thread.json`(재정 T64 ② · M3/M4-a · SPEC §3.3). `frontmatter_raw` 정본 + `tweets[].{text, weighted_char_count}` + `images[]` |
| `annotation-index/v0` | `contracts/schemas/annotation-index.schema.json` | 주석 인덱스 `50-gate/<v>/annotation-index.json`(재정 T64 ② · SPEC §3.3). 전 문장 + `by_material` 역인덱스 + `narrative_sentences` · `text_raw`(총괄 재량 ⓕ · optional) |
| `annotation/v0` | `contracts/schemas/annotation.schema.json` | 파서 산출(`engine/annotation/parse.py#parse`)의 직렬화 서식(재정 T64 ② · SPEC §3.2 문법의 데이터 형태). 파일 산출물이 아니라 구조의 계약 |
| `gate-report/v0` | `contracts/schemas/gate-report.schema.json` | 게이트 판정문 `50-gate/<v>/verdict.json`(재정 T64 ② · SPEC §4.3 전 필드 · memo 객체 §4.6 · `inactive_layers[]` 총괄 재량 ⓑ) |
| `figures-manifest/v0` | `contracts/schemas/figures-manifest.schema.json` | 도면 자산 매니페스트 `30-figures/assets/manifest.json`(재정 T65 ③ · M9-a · SPEC §1.8·§7.5). 항목 = §7.5 10키 + `asset_id`·`source_sha256`(총괄 재량 ⓒ) · `edit_class`↔`publishable` 대응(재정 R11)을 if/then 으로 집행 · `renderer` 실측 블록 |
| `figures-selection/v0` | `contracts/schemas/figures-selection.schema.json` | 출하 도면 선택 `30-figures/selection.json`(재정 T65 ③ · M9-a · SPEC §7.5). 슬롯 = `{tweet, asset, role}` **포인터만**(`additionalProperties: false` = `figures.no-copy` 의 스키마 몫) · `blueprint_digest` |

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
| `read.lane-log-digest-value` | `engine/stages/read.py` | 레인 로그가 적은 **요청 파일 지문의 값**이 그 자리의 `request.md` 와 다름 — 값 위조 · 소비 후 요청 파일 교체 · **면제(`null`)의 위장**(요청 파일이 실재하는데 면제를 주장) (재정 2026-08-31 Q1). **★ 형제 검사 `read.lane-log-shape` 와 관할이 갈린다** — 앞의 것은 **형태**(칸의 있음·빈 값 아님·면제의 명시)를 주장하고 이것은 **값**(sha256 일치)을 주장한다. 한 검사가 둘을 지면 어느 쪽이 통과시켰는지 판정문에서 사라진다는 것이 분리의 근거다(`CLAUDE.md` §6 — *"네 도구는 각자 하나의 주장만 증명한다"*). 칸 부재·빈 문자열은 **여기서 세지 않는다**(형태 검사의 소관 · 건수는 `deferred_to_shape` 에 남는다) |
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
| `design.input-digest` | `engine/stages/__init__.py` | 최신 동결본이 부재·지문 불일치·쓰기 가능인 채로 설계가 시작됨(재정 P-C · T64 ②) — 환경 오류 |
| `design.schema` | `engine/stages/design.py` | 블루프린트가 `blueprint/v0` 밖. 실패면 나머지 다섯은 평가하지 않는다(연쇄 오보 방지) |
| `design.targets-resolve` | `engine/stages/design.py` | `transmission_targets[]`·`slots[].exhibit.material_ids[]`(재량 ⓑ · 좌표 분리)가 동결본에 없거나 `active` 가 아님 |
| `design.slot-count` | `engine/stages/design.py` | 트윗 수가 시트 `tweet_count` 밖 · 슬롯 배치가 시트 `slot_placement`·`slot_enum` 을 어김 · `n` 불연속. 값은 전부 시트에서 읽는다 |
| `design.figure-budget` | `engine/stages/design.py` | 도면 참조가 해소되지 않음(매니페스트 있으면 그것 · 없으면 동결본 `figures[].id` — 재량 ⓐ · `extras.resolution_source`) · 트윗별 도면 수 > `images_per_post_max` · `figure_plan` ↔ `slots` 불일치 · 훅 도면이 T1 밖 |
| `design.spec-digest` | `engine/stages/design.py` | 블루프린트의 `spec_version`·`spec_digest` 가 현재 동결본과 다름(재정 N11). 재진입 시 기존 `blueprint.json` 에도 대조한다 |
| `design.anchors-adjudicated-only` | `engine/stages/design.py` | 레인에 제공된 앵커 목록(`20-design/anchors-provided.json`)에 미재정 항목이 섞임(재정 R12). 제공 0건은 `vacuous: empty-target` 이다 |
| `compose.input-digest` | `engine/stages/__init__.py` | 최신 동결본이 부재·지문 불일치이거나 `20-design/blueprint.json` 이 부재·다른 재료 판 위에 선 채로 펜이 시작됨(재정 P-C · T64 ③) — 환경 오류 |
| `compose.prompt-lint` | `engine/pens/lint.py` | (진입 시) 펜 프롬프트(템플릿 + 응답 계약 + 지시 블록 · 원천 조각·블루프린트 요약 제외)에 부정 명령형 `PROMPT_NEGATION_RE` 또는 화행 술어·결함 카탈로그 리터럴이 있음(D8). 판정 행 2 — `ruleset: prompt-negation` · `speech-acts+defect-catalog`(카탈로그 0항이면 `extras.defect_catalog.vacuous = empty-ruleset`). 1건 = `halt` |
| `compose.lane-verified` | `engine/stages/compose.py` | 변주 응답의 `model` 이 `read.yaml#model_identity` 의 `opus-5` 수용 집합 밖이거나 `effort` 가 계약 배정과 다름(재정 R10 · 토너먼트 기입 자격 없음 → `halt`). `extras.effort_evidence = requested-flag` |
| `compose.spec-digest` | `engine/stages/compose.py` | 프런트매터 `spec_digest` 가 `run.yaml#frozen[-1]` 과 동결본 실측 둘 다와 일치하지 않음(재정 N11 → `halt`) |
| `compose.annotation-syntax` | `engine/stages/compose.py` | `engine/annotation/parse.py#parse` 가 위반을 냄 — finding `rule` 은 §3.2 대응표의 `annotation.schema`·`annotation.missing-tag`, locus `T<n>/S<i>`. **선택이 있으면** 헤더 `fig` 자산 집합 ≠ `selection.json` 의 그 트윗 자산 집합도 위반(rule `annotation.schema` · 메시지 표지 `annotation.fig-selection-mismatch` · `extras.fig_selection_mismatch` — 새 L0 규칙 id 아님 · 재정 T65 ③). `retry(2)` → `escalate`(그 변주만) |
| `compose.frontmatter` | `engine/stages/compose.py` | 프런트매터 5키 정확히 · `run_id`·`variant`·`pen`(계약 배정)·`spec_version`·`spec_digest` 형식 중 하나라도 어긋남(→ `halt` · spec-digest 행을 따른다) |
| `figures.input-digest` | `engine/stages/__init__.py` | 최신 동결본 부재·지문 불일치·쓰기 가능이거나, 동결본 `figures[].raw_path` 가 가리키는 **실재** 원본의 sha256 이 `00-source/source-report.json#figures[]` 행과 다르거나 보고서가 모르는 파일인 채로 도면 편집이 시작됨(재정 T65 ③ · P-U2 · P-C) — 환경 오류. 원본 부재는 `extras.missing_raw`(누락은 `figures.asset-completeness` 몫) |
| `figures.asset-completeness` | `engine/stages/figures.py` | 동결본 `figures[]` 전량에 대응하는 `assets/fig-NN.png` 가 없음(원본 부재 · 렌더 실패 · 파일 부재 — `extras.missing`). `retry(1)` → `escalate`(누락 목록) |
| `figures.render-spec` | `engine/stages/figures.py` | 자산 PNG 의 IHDR 치수(`engine/figures/render.py#png_size`)가 렌더 뷰포트 × 배율(2400×1350)이 아님. `retry(1)` → `halt` |
| `figures.manifest-parity` | `engine/stages/figures.py` | 매니페스트 항목 수 ≠ 자산 파일 수 · 항목이 동결본 `figures[].id` 로 해소되지 않음 · 자산 파일 부재·중복 · `edit_class`·`publishable` 누락 |
| `figures.selection-resolve` | `engine/stages/figures.py` | 선택 포인터가 매니페스트 `asset_id` 에 해소되지 않음 · 트윗당 자산 수 > 시트 `images_per_post_max` · 블루프린트 지정 도면이 자산층에 없음(`selection.figure-not-in-assets` → `reject-upstream` → design) |
| `figures.publish-gate` | `engine/stages/figures.py` | 지목 자산에 `publishable != true` 가 있음(①) · `publish` 런이면 ② `run.yaml#figures.usage_rights_decision` 재정 파일 부재도(재정 R11 · B-05). partial·rehearsal 은 ①만(`extras.branch`) → `halt` |
| `figures.no-copy` | `engine/stages/figures.py` | 슬롯 행에 `tweet`·`asset`·`role` 밖의 키가 있거나 `asset` 값이 자산 id 문법(`fig-NN`)이 아님(경로·데이터 복사 의심) |
| `gate.input-digest` | `engine/stages/__init__.py` | 최신 동결본·블루프린트가 부재·지문 불일치이거나 `40-compose/<v>/thread.annotated.md` 가 변주 1개도 없는 채로 게이트가 시작됨(재정 P-C · T64 ②) — 환경 오류. `30-figures/selection.json` 부재는 `extras.absent_inputs`(T64 ④) |
| `run.publish-preconditions` | `engine/gate/l0/rules_run.py` | `run_kind: publish` 런이 `run-kinds.yaml#requirements` 3종(방어층 가동 · 도면 사용권 재정 · 템플릿 동결) 미충족인데 시작됨(재정 N10). partial·rehearsal 은 `checked 0`(`vacuous: empty-target`) |
| `format.tweet-count` | `engine/gate/l0/rules_format.py` | 트윗 수가 시트 `tweet_count` 밖 |
| `format.slot-count` | `engine/gate/l0/rules_format.py` | 시트 `slot_placement` 위반 — hook 수·위치 · landing 수 · tail 수·위치 · 나머지 슬롯이 `other.allowed` 밖(위반마다 결함 1) |
| `format.body-length` | `engine/gate/l0/rules_format.py` | 슬롯별 **가중 글자 수**(`engine/gate/l0/weighted_length.py` · 시트 `weighted_length`)가 시트 `length_by_slot` 범위 밖(exempt 슬롯 제외 · `extras.weighted_char_counts`) |
| `format.stop-shape` | `engine/gate/l0/rules_format.py` | stop·pivot 의 편집 자산(헤더 `fig` 자산 id → 매니페스트 항목 `asset_id` 의 `edit_class ∈ counted_edit_classes` · `engine/figures/asset_id_of`) < `edited_assets_min` 또는 문장 수(`engine/gate/sentence_count.py`) > `sentences_max`. **가동**(재정 T65 ③ · 매니페스트 실재 시) — 매니페스트가 없는 런에서는 `checked 0` · `extras.inactive_reason` 이고 러너가 `inactive_layers[]` 에 동적으로 적는다. 구 문언(T64 ④ 미가동): 매니페스트가 실재하면 가동 |
| `format.hashtag-zero` | `engine/gate/l0/rules_format.py` | `#`+문자 토큰 수 > 시트 `hashtags_max`(URL 안의 `#` 은 토큰이 아니다) |
| `format.no-link-in-body` | `engine/gate/l0/rules_format.py` | URL(`engine/stages/gate.py#URL_RE` 최소 어형 · 총괄 재량 ⓒ)이 시트 `link_isolation` 허용 슬롯 밖 트윗에 있음 |
| `format.images-per-post` | `engine/gate/l0/rules_format.py` | 헤더 fig 항목 수 > 시트 `images_per_post_max` |
| `annotation.schema` | `engine/gate/l0/rules_annotation.py` | 파서 `errors` 중 `annotation.schema` + 프런트매터 `spec_digest` ≠ 현재 동결본. 실패면 **나머지 L0 행을 내지 않는다**(§3.2 연쇄 오보 방지) |
| `annotation.missing-tag` | `engine/gate/l0/rules_annotation.py` | 파서 `errors` 중 태그 없는 문장 |
| `citation.resolve` | `engine/gate/l0/rules_citation.py` | 인용 M id 가 동결본에 없거나 `retracted`. `superseded` 는 결함이 아니라 flag(`origin: advisory-rule` · E3) |
| `numeric.exhaustive` | `engine/gate/l0/rules_numeric.py` | 출하본 수치 토큰(`l0-format.yaml#numeric.tokenizers` 로드 · rank 순 소비)의 MATCH_KEY 가 정답지(active fact 전 origin ∪ `patent.number` ∪ `patent.dates.*` ∪ `run.yaml#numeric_whitelist[].pattern` fullmatch) 밖. 정규화는 `reader.lib.normalize` 재사용 + 날짜·통화·범위·특허번호(파일 문언). locus = 인덱스 문장 좌표 |
| `numeric.unreviewed-use` | `engine/gate/l0/rules_numeric.py` | **거부권 없는 플래그**(veto: false · 재정 P-B). 출하본이 쓴 수치 키가 미참조 fact 에 속함 — 미참조 목록은 동결본에서 재계산(총괄 재량 ⓓ · `derivation.py#_numeric_inventory` 와 같은 규칙) |
| `gate.l0-clean` | `engine/stages/gate.py` | `l0.json#defects[]` 가 비어 있지 않음 |
| `gate.annotation-index` | `engine/annotation/index.py` · `engine/stages/gate.py` | 인덱스 문장 수 ≠ 초안 문장 수 · 인용 ID·narrative 가 초안과 다름 |
| `gate.no-rewrite` | `engine/stages/gate.py` | 러너 자기 산출 `fix_directive` 에 따옴표 속 5토큰 이상 EN 문장(SPEC §4.7 기제 3 · 탐지 범위의 한계도 그 절). 레인 프롬프트 산출에 대한 같은 린트는 M6 |
| `strip.roundtrip-forward` | `engine/annotation/strip.py` | `strip(annotated).stripped_md` 가 참조 구현(`_reference_strip` · 코드 공유 없음)과 바이트 다름 — strip 이 본문을 슬쩍 고침(SPEC §3.3 순방향 · id 는 총괄 재량 ⓔ) |
| `strip.roundtrip-reverse` | `engine/annotation/reassemble.py` | `thread.json` + `annotation-index.json` 으로 재조립한 주석본이 원본과 바이트 다름 — 변환의 정보 손실(§3.3 역방향 · ⓔ) |
| `strip.reassembly` | `engine/stages/gate.py` | `thread.json.tweets[].text` 를 이어붙인 것이 `thread.stripped.md` 와 바이트 다름 — 인간본·기계본 표류(§3.3 재조립 · ⓔ) |
| `strip.residual-tag` | `engine/stages/gate.py` | 출하본에 `\[(M\d+\|narrative)` 잔존(§3.3 안전망 · ⓔ) |

### 2.2 계약에만 있고 아직 구현이 없는 것

이 목록이 짧아지는 것이 로드맵의 진척이다. **여기 있는 id를 "검사가 있다"고 말하지 마라** — 그것이 M0.6 재감수가 과장 보고로 판정한 종류의 서술이다.

| 검사 id | 소관 | 정본 서술 |
|---|---|---|
| `gate.no-rewrite`(레인 산출 대상) · `gate.final-eyes` | M6 | SPEC §4.7·§1.10 — `gate.no-rewrite` 의 **러너 자기 산출** 린트는 T64 ②(M3/M4-a)로 §2.1 에 올라갔다. 남은 것은 레인(L1·최종 심급)이 낸 `fix_directive` 에 대한 같은 린트와 최종 심급 자체다. `gate.l1-clean` · `gate.final-eyes-isolation` · `gate.final-eyes-scope` 도 같은 자리(계약 `gate.yaml#checks_before_exit` 에 `status: inactive` 로 있다) |
| `gate.no-score` · `critique.no-score` | M4·M8 | `contracts/lexicon/score-lint.yaml` |
| `critique.anchors-adjudicated-only` | M8 | SPEC §1.12 — `design.anchors-adjudicated-only` 는 T64(M5-a)로 §2.1 에 올라갔다 |
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
| 도면 편집 등급 `edit_class` | `crop-only` · `self-authored` · `annotated-internal` · `recomposed-internal` (앞 둘 `publishable: true` · 뒤 둘 `false`) | `figures-manifest/v0` · SPEC §7.5(재정 R11). v1 실물은 `crop-only` 하나 |
| 도면 선택 역할 `role` | `hero`(T1 첫 자산) · `exhibit`(나머지) | `figures-selection/v0` · SPEC §7.5 |
| 토너먼트 결과 `outcome` | `drafted` · `missing` · `material-defect` · `redrafted`(회차 2 이상 · `round` 키 동반 · 재정 T65 ③ 재량 ⓔ) | `40-compose/tournament-rows.jsonl` |
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
| `15-frozen/extension-v<N>.md` | 오케스트레이터 | 부분 런 종료선 연장 봉투(`extension-envelope/v0` · 재정 T64 ①). 구동기 `extend` 가 쓰고 `run.yaml#partial_until`·`extensions[]` 를 함께 옮긴다. 계약 미선언 경로 — `engine/paths.py#RunPaths.extension` 이 `15-frozen/` 안에서 파생시킨다 |
| `20-design/blueprint.json` | `design` | **블루프린트**(`blueprint/v0`). 러너 6키(`schema`·`run_id`·`spec_version`·`spec_digest`·`lane`·`law_commit`) + 레인 필드. 검사 6종 전건 통과 뒤에만 쓴다 |
| `20-design/blueprint.md` | `design` | `.json` 의 **결정론 렌더**(KR 틀 · EN 값) + 판정 행 표 + 「미가동·부재」 절(T64 ④) |
| `20-design/design-report.json` | `design` | 판정 행 8키 배열 · findings · `lane`(model·effort·mismatch) · `law_commit` |
| `20-design/lanes/` | `design` | 설계 레인 왕복 기록(`design/blueprint[/retry-1]/batch-0/{request.json,request.md,response.json}`) |
| `20-design/escalation.json` | `design` | (선택) 상신 기록 — 레인의 `escalation` 또는 재시도 소진. 실재하면 러너는 재진입을 거부한다 |
| `20-design/anchors-provided.json` | `design` | (선택) 레인에 제공된 재정 앵커 목록 + 차단 건수 — `design.anchors-adjudicated-only` 의 대상 |
| `30-figures/assets/fig-NN.png` | `figures.prepare` | **전량 편집본**(1급 보존 · §7.5 삭제·덮어쓰기 금지 · 재편집은 `fig-NN.r2.png`). v1 = 순수 크롭 프레이밍 1200×675 @2x(`crop-only/v0` 템플릿 · 헤드리스 Chromium) |
| `30-figures/assets/manifest.json` | `figures.prepare` | 도면 자산 매니페스트(`figures-manifest/v0`) — 항목마다 `figure_id`↔`asset_id` 대응 · 원천 지문 · `edit_class`·`publishable` · `edits[]`(복합 시트 표기 포함) · `renderer` 실측 |
| `30-figures/assets/.render/` | `figures.prepare` | 렌더 입력(채운 템플릿 html · `jobs.json`). 계약 미선언 — `assets/` 안의 러너 산출물(재현 사료) |
| `30-figures/selection.json` | `figures.select` | 출하 도면 선택(`figures-selection/v0`) — **포인터만**. 블루프린트 `figure_plan` 의 결정론 사영(총괄 재량 ⓐ) · 검사 3 전건 통과 뒤에만 쓴다 |
| `30-figures/figures-report.json` | `figures` | 단계별(`figures.prepare` · `figures.select`) 판정 행 8키 + findings + 렌더 환경 실측 |
| `30-figures/corrections-rows.md` | `figures.select` | 교정 원장 행의 **런 안** 사본(총괄 재량 ⓓ — `ledgers/corrections.md` 의 쓰기 소유자는 `ship` · §1.17). v1 은 「선택 = 사영 · 기각 0」 |
| `40-compose/<v>/thread.annotated.md` | `compose` | 변주 `v` 의 **확정 초안**(주석층 · §3.2). 레인 바이트 그대로(끝 개행 하나만 정규화) · 검사 4 전건 통과 뒤에만 쓴다 · 전 변주 해소 뒤에 함께 쓴다(순서 효과 차단) |
| `40-compose/<v>/rounds/r<n>/` | `compose`(회차 n+1) | **직전 회차 보존**(`thread.annotated.md` + 그 좌표 `response.json` 사본 · 재정 T65 ③ 재량 ⓔ). 회차 좌표 = `compose-r<n>/<v>/batch-0`. `revisions/r<n>/`(§1.10 결함 지시 라운드)와 다른 자리 |
| `40-compose/<v>/material-defect.md` | `compose` | (선택) 재료 반려서 — YAML 프런트매터 4필드(`material_ids`·`defect_kind`·`evidence`·`blocked_slots`) + 본문 evidence. 실재 = 그 변주 `reject-upstream`(→ `read`) |
| `40-compose/lanes/` | `compose` | 펜 레인 왕복 기록(`compose/<v>[/retry-<n>]/batch-0/{request.json,request.md,response.json}`) |
| `40-compose/compose-report.json` | `compose` | 판정 행 8키 배열(진입 1 + 린트 2×변주 + 검사 4×변주) · findings · `variants` 상태 · `pens` · `comparison_axis` · `lanes` · `law_commit` |
| `40-compose/tournament-rows.jsonl` | `compose` | **런 안**의 토너먼트 행(append · 변주당 1행 · `outcome ∈ drafted\|missing\|material-defect` · `comparison_axis`·`taste_weight`). `ledgers/tournament.jsonl` 의 쓰기 소유자는 `ship` 뿐이므로(§1.17) 여기 쌓고 `ship` 이 옮긴다(총괄 재량 ⓐ · T64 집행 ②) |
| `50-gate/<v>/l0.json` | `gate` | L0 판정 블록 `{pass, defects, flags, checks}` — `verdict.json#l0` 과 같은 객체를 따로 저장한 파일. **계약 라인 없음**(총괄 재량 ⓐ · T64 집행 ③) |
| `50-gate/<v>/verdict.json` | `gate` | 판정문(`gate-report/v0`). L0 13 행 + `gate.input-digest` + strip 4 + `gate.l0-clean`·`gate.annotation-index`·`gate.no-rewrite` · `inactive_layers[]`(L1·L2·화행·최종 심급·`format.stop-shape`) · `decision` 은 가동 층만으로(총괄 재량 ⓑ) · `thread_digest` 로 재진입 판정 |
| `50-gate/<v>/thread.stripped.md` | `gate` | 출하 후보 텍스트(strip §3.3 ①~⑤). 예행 종료선의 실물(`run-kinds.yaml#kinds.rehearsal.terminates_at_artifact`) · `ship` 은 복사만 |
| `50-gate/<v>/thread.json` | `gate` | 구조화 출하 객체(`thread/v0`) — `frontmatter_raw` 정본 · `weighted_char_count` · `ship` 은 복사만(재감수 B-04) |
| `50-gate/<v>/annotation-index.json` | `gate` | 주석 인덱스(`annotation-index/v0`) — 계기 국소화(D9)·L1 감사 표본이 소비. `text_raw` 가 역방향 round-trip 의 전제(재량 ⓕ) |
| `50-gate/<v>/rounds/r<n>/` | `gate` | 주석본 지문이 바뀌어 재판정할 때 **직전 판정 산출 전량**을 옮겨 둔 자리(재정 T65 ③ 재량 ⓔ — 「덮어씀」을 보존으로) |

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
