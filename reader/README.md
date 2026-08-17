# `reader/` — 독해층 이식 단위

이 디렉터리는 **patent-docent 와 patent-historian 이 공유하는 이식 단위**다(헌장 D14).
특허 1건을 읽어 만든 **재료 명세**의 계약·규칙·검증기가 한 덩어리로 여기 산다.

판별식은 한 줄이다 — **"historian 이 이 파일 없이 재료 명세를 해석할 수 있는가."**
답이 아니오면 그 파일은 이식 단위 안에 있어야 한다(SPEC §2.1 · 재정 2026-08-18 N8 ①).

## 1. 구성

| 경로 | 내용 |
|---|---|
| `schemas/material-spec.schema.json` | **재료 명세 스키마 정본**(프로젝트 간 계약). 사본은 어디에도 없다 |
| `reader-rules.yaml` | 독해층 규칙 계약 — 청구항 인벤토리·종속 인용 어형·항목 생애주기·수치 문법·수렴 축 |
| `lib/` | 결정론 검증기 일체(아래 §2) |
| `procedure/` | D5 5단계 절차 문서·프롬프트 (M2 범위) |
| `READER-VERSION` | 구현 버전 semver 한 줄 |

## 2. `lib/` — 검사 11종

| 모듈 | 검사 id | 무엇을 반증하는가 |
|---|---|---|
| `schema_check.py` | `read.schema` | 스키마 위반 |
| `source_digest.py` | `read.source-digest` | 인용 검사의 **기준점**이 바뀐 것(불변식 I1 — 어긋나면 아래 전부 무효) |
| `verbatim.py` | `read.verbatim` | 원문을 다듬어 인용하거나 지어낸 문장 |
| `pointers.py` | `read.pointer-resolve` | 유령 링크·오타 ID·자기참조·참조 순환 |
| `coverage.py` | `read.coverage` | 읽지 않고 넘어간 구성요소, 접지 1건이 둘을 덮는 것 |
| `dependency_parse.py` | `read.dependency-parse` | 다중 종속의 논리 형태를 잃거나 잘못 적은 것 |
| `derivation.py` | `read.value-derivation` | 인용문 옆의 날조 수치·정규화값 오기·파생 사슬로 흐린 원천 |
| `inventory.py` | `read.claim-inventory` | 청구항이 통째로 빠진 것 |
| `convergence.py` | `read.convergence` | 독해가 재현되지 않는 것(1회성 추론) |
| `freeze_integrity.py` | `freeze.id-monotonic` · `freeze.payload-immutable` | 항목 삭제·재번호, 같은 ID 아래의 조용한 내용 교체 |

보조 모듈: `report.py`(판정 서식) · `rules.py`(규칙 로더) · `normalize.py`(수치 정규화 표) ·
`value_grammar.py`(수치 문법) · `spec_io.py`(로드·인덱싱) · `run_checks.py`(오케스트레이터).

**검사가 판정하는 것은 "독해가 옳은가"가 아니다.** 판정하는 것은
**"독해가 자기 산출물에 대해 거짓말을 하지 않았는가"**뿐이다(D6 규율 ③ · SPEC §2.6).
전 검사를 통과한 명세도 여전히 얕거나 초점이 틀릴 수 있으며, 그 판단은 체크포인트 1 의
Owner 몫이다.

## 3. 쓰는 법

```python
from reader.lib import CheckContext, Rules, load_schema, load_spec
from reader.lib import run_read_checks, run_freeze_checks, to_convergence_payload

spec = load_spec("runs/<run-id>/10-read/material-spec.json")
ctx = CheckContext(
    spec=spec,
    source_text=open("runs/<run-id>/00-source/patent.md", encoding="utf-8").read(),
    rules=Rules.load(),
    schema=load_schema(),
    peer_spec=load_spec("runs/<run-id>/10-read/material-spec.read-b.json"),  # 독립 2회차
)
rows = run_read_checks(ctx)                       # verdict-check-row/v0 행 9개
payload = to_convergence_payload(rows, spec)      # 10-read/convergence.json 본문
ok = all(row.status == "pass" for row in rows)
```

- 검사는 **읽기 전용**이다. 어떤 검사도 인스턴스를 변형하지 않는다.
- `peer_spec` 이 없으면 `read.convergence` 는 `checked: 0` 으로 나오고 행의
  `vacuous: "empty-target"` 이 그 사실을 자동으로 날인한다 — 2회차 없는 런이 수렴 통과로
  보이지 않는다(재정 N5).
- 동결 검사는 `run_freeze_checks(ctx)` 이며 `prior_spec` 에 직전 동결본 `v<N-1>` 을 준다.

## 4. 이식 규율

1. **의존은 표준 라이브러리 + `yaml` + `jsonschema` 뿐이다.** `lib/**` 는 `contracts/**` ·
   `engine/**` · `docs/**` 를 import 하지도 읽지도 않는다 — historian 이 `reader/` 만
   스냅샷해도 동작해야 하기 때문이다(SPEC §6.2 판별식 1).
2. **출력 채널을 모른다.** 트윗·슬롯·스레드 같은 개념이 이 디렉터리에 등장하면 그것은 결함이다.
3. **탐지 패턴은 코드가 아니라 `reader-rules.yaml` 에 있다**(SPEC §4.8 격리 요건 2항).
   판정 규칙의 입법은 재정 사항이고(D7), 규칙이 코드에 박히면 재정 없이 조용히 바뀐다.
4. 이식은 스냅샷 + `PORTED-FROM.md`(원천 커밋 SHA 핀)다. 심링크·서브모듈로 잇지 않는다.
5. **상호 체크**: 독해층을 수정하는 작업은 상대 리포의 `READER-VERSION` 을 먼저 확인한다.
   어긋남을 발견하면 자동 동기화하지 말고 Owner 에게 상신한다.

## 5. 다른 곳에 사는 계약과의 접점

두 곳은 `reader/` 밖에 있고, 이식 단위는 그것들을 **읽지 않는다**. 대신 **테스트가 대조**한다.

| 바깥 계약 | 접점 | 대조 장치 |
|---|---|---|
| `contracts/l0-format.yaml` §9 `numeric` | 수치 정규화·MATCH_KEY | `tests/test_m1_reader.py::test_normalization_table_matches_l0_contract` |
| `contracts/schemas/verdict-check-row.schema.json` | 판정 행 8키 서식 | `…::test_check_row_validates_against_verdict_check_row_schema` |
| `contracts/schemas/convergence.schema.json` | `10-read/convergence.json` 본문 | `…::test_convergence_payload_validates_against_contract` |

사본이 아니라 대조로 묶는 이유는 사본이 반드시 낡기 때문이다. 대조가 깨지면 **바깥 계약이
정본이고 `reader/` 쪽이 결함**이다.

## 6. 검증

```bash
.venv/bin/pytest tests/test_m1_reader.py -q
```

`lib/**` 에는 `assert` 를 쓰지 않는다 — `python3 -O` 에서 전부 제거되어 망가진 코드가 공허
통과한다(CLAUDE.md §3). 그 규율 자체를 `…::test_no_assert_in_library_sources` 가 AST 로 본다.
