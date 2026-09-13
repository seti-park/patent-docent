# patent-docent

특허 1건을 깊게 읽고, 그 독해에서 일반 대중용 무료 X 스레드(EN)를 만드는 엔진. 이름은 미술관 도슨트에서 왔다 — 관람객을 미술사학자로 만들려 하지 않고, 작품 앞의 10분을 만족스럽게 만드는 역할이다. 독자는 학습자가 아니라 투자자-팬이고, 엔진이 최적화하는 것은 교육의 성공이 아니라 공유 충동이다. 핵심 독트린은 **"투자자의 질문에, 기술로 답한다"** — 훅은 투자자-팬의 불안에 조응하되, 답은 특허 물증에 근거한 기술 서사뿐이며 종목 추천·가격 전망·매수매도 함의는 절대 금지다. 구조는 주방 분리형이다: 독해(READ)가 **재료 명세**를 만들고, Owner가 그것을 승인·동결한 뒤에야 집필(펜)이 시작되며, 펜은 재료를 수정할 수 없고 본문의 모든 기술 주장은 재료 항목 ID로 역참조된다. 자매 프로젝트 **patent-historian**(복수 특허 교차 분석·전문가용·유료)과는 재료 명세 스키마를 계약으로 공유한다.

- **헌장(정본)**: [`docs/CHARTER.md`](docs/CHARTER.md) — D1~D15, 모든 판정에 우선
- **공학 스펙**: [`docs/SPEC.md`](docs/SPEC.md) — 스테이지 계약·스키마·모듈 로드맵
- **재정 원장(상류)**: [`docs/decisions/RULINGS-LEDGER.md`](docs/decisions/RULINGS-LEDGER.md) — 재정 → 원장 → 문서 순서이며 원장이 헌장·스펙의 상류다
- **작업 규약**: [`CLAUDE.md`](CLAUDE.md)

상태: **M1(READ 모듈) 완료** — 문서·계약 14종에 더해 **결정론 검사 10종의 실구현**(`reader/lib/`)과 **READ 실행 경로**(`engine/`, CP1 KR 표면 렌더까지)가 실물로 있다. T64(2026-09-13)로 **설계·펜·L0 게이트**(`design` · `compose` · `gate` 의 L0 층 + strip + round-trip · 구동기 `design`·`compose`·`gate-l0`·`strip`)가, T65 ③(같은 날)으로 **도면 자산층 v1**(`figures` — 크롭 전용 프레이밍 렌더 + 포인터 선택 · `format.stop-shape` 가동 · 구동기 `figures` · `compose --variant --round` 회차 재펜)이 더해졌다. T67 ②(같은 날 · M6-a)로 **L1 국소 대조**(opus-5 high × k 독립 실행 다수결 · 화행 플래그 3종 · `gate.no-rewrite` 레인 산출 확장 · `final-eyes-brief.json` 루프 개시 전 핀 · 국소 수정 루프 캡 3 `revisions/r<n>/` · CP2 봉투 `70-ship/checkpoint2.md` · 구동기 `gate-l1`·`revise`·`cp2`·`approve-ship` · 명령 19)가 더해졌다. T69 ⑥(같은 날 · M4/M8-a · M7-a)로 **L2 자문 메모**(fable-5.1 high 1회 · 점수 금지 린트 `gate.no-score` 가동 · 펜 자유 리비전 1회 `revisions/free-r1/` · 위상 봉쇄)와 **계기**(`probe` — 질문 생성 opus-5 low → haiku-4.5 × `probe.n` 독립 프로브 → 채점 분리(결정론 3 kind + opus-5 low 모델 채점) → annotation-index 역참조 국소화 → `60-probe/<v>/score.json` 판정 키 없음 · 정족수 5/5 · 검사 5 · 구동기 `gate-l2`·`revise-free`·`probe` · 명령 22)가 더해졌다. 파이프라인의 나머지(최종 심급·자작물 템플릿·소견·출하)는 미구현이며, 게이트 판정문은 그 미가동 층을 `inactive_layers[]` 로 명기한다. 무엇이 실물이고 무엇이 예정인지의 정본은 [`docs/SPEC.md` §6.7](docs/SPEC.md)과 [`contracts/glossary.md`](contracts/glossary.md) §2이며, 커밋 전 검사기가 그 표와 리포 실물을 대조한다.

첫 런은 **예행 런**(비게시)이며, 게시 런은 전 방어층 가동·도면 사용권 재정·템플릿 동결이 충족될 때 열린다.

**`reader/`는 이식 단위다.** 자매 프로젝트가 이 디렉터리를 스냅샷하면 스키마·규칙 계약·검사기가 한 덩어리로 따라간다 — 심링크·서브모듈로 잇지 않는다. 상세 = [`reader/README.md`](reader/README.md).
