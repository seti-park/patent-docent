# patent-docent — 세션 작업 규약

이 엔진은 특허 한 건을 깊게 읽고, 일반 독자용 영어 X 스레드를 만든다.
이 문서는 에이전트가 이 리포에서 일할 때 지킬 것만 담는다. 설계와 값은 헌장과 스펙에 있다. 이 문서는 그것을 옮겨 적지 않고 가리킨다.
절 번호(§0 ~ §6)와 규율 번호(1 ~ 11)는 코드 주석이 인용한다. 번호를 바꾸지 않는다.

## 0. 헌장 우선

- 정본은 `docs/CHARTER.md`(D1 ~ D15)다. 스펙 · 계약 · 코드 · 프롬프트 · 이 문서가 헌장과 충돌하면 헌장이 이긴다.
- 충돌을 찾으면 스스로 맞추지 않는다. Owner 에게 올린다.
- 설계 근거로 헌장을 인용할 때는 조항 번호를 함께 적는다. 예: `(D8)`.
- `docs/SPEC.md` 는 헌장의 공학 전개다. 스펙이 헌장을 넘으면 스펙의 결함이다.
- 재정은 원장을 거쳐 문서에 닿는다. 순서는 재정 → 원장 등재(`docs/decisions/ruling-*.md`) → 문서 반영이다. 원장과 문서가 어긋나면 원장이 이긴다(재정 N6 · 제도 = `docs/decisions/RULINGS-LEDGER.md`).

## 1. 절대 규율

위반은 결함이다.

| # | 규율 | 근거 |
|---|---|---|
| 1 | **단방향.** 펜(COMPOSE)은 재료 명세를 고치지 않는다. 재료 결함은 `40-compose/<variant>/material-defect.md` 로 READ 에 반려한다. READ 가 명세를 개정(`spec_version` +1)한 뒤 다시 쓴다. | D6 ② |
| 2 | **성분 역참조.** 본문의 기술 주장은 모두 재료 항목 ID(`M<n>`)로 거슬러 갈 수 있어야 한다. 근거가 필요 없는 서사는 `[narrative]` 로 스스로 표시한다. | D6 ① |
| 3 | **게이트는 글을 고치지 않는다.** 게이트는 결함과 지시문만 낸다. 대체 문장을 쓰지 않는다. 게이트 레인에는 쓰기 권한을 주지 않는다. | D8 |
| 4 | **펜 프롬프트에는 긍정형만.** 펜에게는 스코프 선언과 도슨트 정체성만 준다. 금지 목록은 검증 쪽 프롬프트에만 둔다. 금지를 열거하면 그 금지가 오히려 떠오르기 때문이다. | D8 |
| 5 | **자문 층은 점수를 내지 않는다.** L2 · 소견 · 계기에 숫자 등급을 붙이지 않는다. 점수는 그것을 맞추려는 쓰기를 부른다. | D8 · D15 |
| 6 | **게이트 관할을 넓히지 않는다.** 게이트는 정답이 있는 범위만 본다. 원천 대조 · 입법된 문언 · 사후 반응이다. 「좋은 글인가」는 게이트가 아니라 자문이나 결함 카탈로그다. | D7 |
| 7 | **카탈로그 · 앵커 등재는 Owner 재정으로만.** `contracts/lexicon/*.yaml` 과 `ledgers/anchors/` 에 스스로 항목을 더하지 않는다. 재정 기록은 `docs/decisions/` 에 둔다. | D7 · D13 · D15 |
| 8 | **최종 판정은 새 눈이 한다.** 점수와 수정 이력을 모르는 별도 심급이 마지막을 본다. 그 심급이 볼 수 있는 것은 수정 루프 시작 전에 동결한 것뿐이다. 예외는 심판 대상인 최종 초안 하나다. | D8 · D15 · N1 |
| 9 | **재정은 원장을 거친다.** 재정을 문서에 바로 옮기지 않는다. 원문과 재구성본을 구별해 표시한다. | N6 |
| 10 | **감수자 · 자문가가 쓴 절은 고치지 않는다.** 경계는 파일이 아니라 저자다. 감수 산출은 받는 즉시 `docs/lessons/` 에 전문으로 둔다. 처분표와 요약은 그 원문을 가리킬 뿐이다. 내 추기는 별도 절로 두고, 절 머리에 저자를 적는다. 저자 표시가 없는 추기는 관문이 막는다(`tools/check_lesson_authorship.py` · 규격 = SPEC §8.3 10항 · 개정 경위 = `docs/decisions/ruling-20260901-09-T18-T20.md` T20). | N7 · T20 |
| 11 | **값 공간을 바꾸는 판단은 먼저 올린다.** 검사 · 게이트가 집행하는 값(임계값 · 어형 · 정답 집합)을 바꾸는 판단은 재정 사항이다. `[가설]` 태그도, 되돌리기 쉽다는 사실도 면제가 아니다. 공학 집행 · 기록 · 시험 · 오류 수정은 재량이고 사후 확인으로 충분하다. 판별선은 「그 판단이 검사의 판정 공간을 바꾸는가」 하나다(출처 = `docs/decisions/ruling-20260819-03-S1-S9.md` §2 S2). | S2 |

## 2. reader 이식 단위

- `reader/` 는 자매 프로젝트(patent-historian)와 나누는 이식 단위다. `reader/schemas/material-spec.schema.json` 이 두 프로젝트의 계약이다.
- 이식은 스냅샷과 `PORTED-FROM.md`(원천 커밋 SHA)로 한다. 심링크나 서브모듈로 잇지 않는다.
- 상대 리포와 `reader/READER-VERSION` 이 어긋나면 자동으로 맞추지 않는다. Owner 에게 올린다.
- 스키마 0.x 는 미동결이다. 변경은 자유지만 무엇을 왜 바꿨는지 적는다(스키마 `$comment` · SPEC §6.3 · 커밋). 상대가 처음 이식하기 직전에 1.0.0 으로 동결한다. 그 뒤 하위 호환을 깨는 변경은 major 증가와 상대 리포 상신이 필요하다(재정 N15).
- 계약 파일의 자리: 이식 단위에 속하면 `reader/schemas/`, 파이프라인 전용이면 `contracts/` 다(재정 N8).

## 3. 검증 규약

- 시험은 pytest 로 쓴다. 실행: `python3 -m pytest tests/ -q`. 의존성은 `requirements-dev.txt` 에 있다.
- 라이브러리 · 도구 코드에서는 `assert` 를 쓰지 않는다. `python3 -O` 가 `assert` 를 지워 망가진 코드가 통과하기 때문이다(2026-08-16 실측). 명시 비교와 종료 코드로 쓴다.
- 시험 모듈의 `assert` 는 괜찮다. pytest 가 AST 를 다시 써서 `-O` 에서도 살아남는다. 다만 서브프로세스의 종료 코드는 시험 안에서도 명시 비교로 본다.
- 게이트를 고치면 회귀 스위트를 돌린다. 심은 결함 100% 검출과 golden 100% 통과가 조건이다.
- 「다 했다」는 증거가 아니다. 실제 파일과 실제 출력으로 확인한다.

## 4. git 규약

- `git add -A` · `git add .` 을 쓰지 않는다. 바꾼 파일을 이름으로 add 하고, 커밋 전에 `git status` 로 확인한다.
- 커밋은 논리 단위로 나눈다.
- 기본 가지는 `main` 이다. 원격 추가와 push 는 Owner 가 정한다.
- 런 작업장 `runs/` 는 git 에 싣지 않는다(`.gitignore`). 런 산출은 리포 밖에 보관한다.

## 5. 정본 위치

| 관심사 | 정본 |
|---|---|
| 헌장 | `docs/CHARTER.md` |
| 공학 스펙 · 계약 파일 현황 | `docs/SPEC.md`(현황 = §6.7 · 대조 = `tools/check_spec_refs.py`) |
| 재정 원장 | `docs/decisions/RULINGS-LEDGER.md` · `docs/decisions/ruling-*.md` |
| 지적 처분 | `docs/decisions/DISPOSITIONS.md`(관문 `tools/check_dispositions.py`) |
| 감수 원문 | `docs/lessons/` |
| 단계 I/O 계약 | `contracts/stages/*.yaml`(source · read · freeze · design · figures · compose · gate · probe · critique · ship) |
| 재료 명세 스키마(프로젝트 간 계약 · 단일 진원) | `reader/schemas/material-spec.schema.json` |
| 형식 수치 · L0 규칙 | `contracts/format-parameters.yaml` · `contracts/l0-format.yaml` |
| 런 종류 · 조정 파라미터 | `contracts/run-kinds.yaml` · `contracts/parameters.yaml`(변경은 재정으로만) |
| 화행 술어 · 결함 카탈로그 · 점수 린트 | `contracts/lexicon/`(등재는 재정으로만) |
| 앵커 · 회귀 · 섀도 원장 | `ledgers/anchors/` · `ledgers/regression/` · `ledgers/shadow/screening.jsonl` |
| 런 결박 판정 | `engine/gitpin.py`(러너와 도구가 같은 함수를 쓴다) |

## 6. 구현 상태

- 무엇이 실물이고 무엇이 예정인지는 `docs/SPEC.md` §6.7 과 `contracts/glossary.md` §2.2 가 정본이다. 「검사가 있다」고 말하기 전에 두 곳을 확인한다. 강제 범위를 실제보다 넓게 말하는 것이 이 리포가 감수에서 FAIL 을 받은 꼴이다.
- 구현 이력은 `docs/IMPLEMENTATION-HISTORY.md` 에 있다.
- 문서 · 계약 · 검증기 · 러너 · 감수 원문 · 처분 원장 · 실패표를 고쳤으면 아래 관문 일곱을 모두 돌린다. 모두 exit 0 이어야 한다. plain 과 `python3 -O` 양쪽에서 돌린다(규격 = SPEC §8.3).
- 일곱 도구는 각자 주장 하나만 증명한다. 하나의 통과를 다른 하나의 증거로 쓰지 않는다.

| 도구 | 증명하는 주장 |
|---|---|
| `tools/check_spec_refs.py` | 문서 · 계약의 참조가 맞는다 |
| `tools/check_schema_enforcement.py` | 스키마가 의미 불변식을 실제로 강제한다 |
| `tools/check_validator_enforcement.py` | 스키마 밖의 불변식을 검증기가 실제로 거부한다 |
| `tools/check_lane_binding.py` | 레인 왕복의 변조(낡은 응답 · 사후 교체 · 지문 위조)가 잡힌다 |
| `tools/check_lesson_authorship.py` | `docs/lessons/` 의 추기 절이 저자를 밝힌다 |
| `tools/check_dispositions.py` | `docs/decisions/DISPOSITIONS.md` 가 `docs/lessons/` 와 빠짐없이 맞는다 |
| `tools/check_failure_table.py` | READ 실패표의 골격 · 재시도 등식 · 종단 어휘가 맞는다 |
