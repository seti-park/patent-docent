# patent-docent 설계 스펙 (v0.1)

**지위.** 이 문서는 헌장(`docs/CHARTER.md`, D1~D15)의 **공학 전개**다. 헌장이 상위 정본이며, 이 스펙이 헌장과 충돌하면 헌장이 이긴다 — 충돌을 발견하면 임의로 조정하지 말고 Owner에게 상신한다.

**범위.** M0(부트스트랩) 산출물. 계약·스키마·로드맵까지이며 **모듈 코드는 이 발주에 포함되지 않는다**(후속 발주). 스펙 안의 JSON·YAML·의사코드는 구현이 아니라 계약의 예시다.

**작성.** 2026-08-17. 세 집필 레인(§0~§1 / §2~§4 / §5~§8)이 동일한 고정 규약 위에서 병렬 집필하고, §9와 조립·정합은 총괄이 수행했다.

---

## §0 문서 지위·범위·용어

### §0.1 이 문서의 지위

본 스펙(`docs/SPEC.md`)은 헌장(`docs/CHARTER.md`, D1~D15)의 **공학 전개**다. 헌장이 "무엇을·왜"를 재정하고, 스펙은 그것을 계약·스키마·검사 가능한 형태로 옮긴다.

| 층 | 문서 | 성격 | 개정 권한 |
|---|---|---|---|
| 0 | `docs/CHARTER.md` | 정본. 전 판정에 우선 | Owner 재정만. 조항 번호 재사용 금지 |
| 1 | `docs/SPEC.md` (본 문서) | 헌장의 공학 전개 | 헌장 범위 내에서 작업 레인 개정 가능 |
| 2 | `contracts/**`, `reader/schemas/**` | 기계 집행 가능한 계약 | 스펙 준거 |
| 3 | `engine/**`, `studio/**`, 프롬프트 | 구현 | 계약 준거 |

**충돌 처리 규율.** 스펙·계약·코드·프롬프트가 헌장과 충돌하면 헌장이 이긴다. 충돌을 발견한 레인은 **임의로 조정하지 말고 Owner에게 상신**하며, 재정 결과는 `docs/decisions/D-YYYYMMDD-nn-<slug>.md`로 남긴다. 이 규율은 헌장 서두에서 직접 온다.

스펙이 헌장을 **창작·확대·완화하는 것은 금지**한다. 헌장이 답하지 않는 사항 중 Owner 재정이 필요한 것은 결정하지 않고 `> [OPEN]` 블록으로 남기며, §9에 취합한다.

### §0.2 범위

**이번 발주의 범위 = 계약·스키마·로드맵까지.**

| 포함 | 불포함(후속 발주) |
|---|---|
| 스테이지 계약 서식과 전 스테이지의 I/O·검사·실패 처리 (§1) | 스테이지 러너 구현, 프롬프트 실문 |
| 재료 명세 스키마 v0 (§2) | 스키마 검증기·결정론 검사기 코드 |
| 주석층 표기 규약·strip 문법 (§3) | strip 파이프라인 구현 |
| 게이트 판정 데이터 모델 (§4) | L0/L1 규칙 구현, 회귀 스위트 데이터 |
| 계기·소견 프로토콜 (§5) | 프로브 실행기·채점자 레인 |
| 리포/런 레이아웃 (§6·§7) | 디렉토리 실물 부트스트랩 |
| 모듈 구현 로드맵과 모듈별 검증 계획 (§8) | 모듈 코드 |

따라서 본 문서에 등장하는 검사 이름(`read.convergence` 등)과 스크립트 성격은 **계약상의 이름과 판정 기준**이며, 실행 파일은 §8 로드맵의 각 모듈 발주에서 만든다. 본 문서의 예시 JSON/YAML은 계약 예시이지 구현이 아니다.

또한 다음은 이번 스펙의 범위 밖임을 명시한다.

- **템플릿 스튜디오**(도면 3종 템플릿 × 시안 3안 + 디자인 토큰 동결) — 헌장이 별도 발주로 지정했다(D12). 본 스펙은 **폴백 경로**(원본 크롭 + 최소 주석)만 계약한다.
- **X API 자동화** — v1 지표 수집은 수동 입력이다(D13).
- **patent-historian 쪽 구현** — 본 스펙은 재료 명세 스키마라는 계약면과 `reader-version` 상호 체크 규율만 다룬다(D14).

### §0.3 표기 규약

1. **헌장 근거 병기(1급 요건).** 헌장에서 온 판정은 예외 없이 조항 번호를 괄호로 병기한다 — 예: "게이트는 직접 글을 고치지 않는다(D8)". 병기가 없는 규범 문장은 **작업 레인의 재량 결정**임을 뜻하며, 재량 결정은 헌장 개정 없이 개정할 수 있다. 이 이분법이 추적성의 전부다.
2. **언어.** 문서 산문은 KR. 코드 식별자·스키마 키·파일 경로·스테이지 id·검사 id·정규식은 EN 원문 그대로 쓰고 번역하지 않는다.
3. **경로.** 리포 루트 기준 상대 경로로 쓴다. 런 산출물은 `runs/<run-id>/` 이하를 생략한 상대 경로로 쓴다(예: `10-read/material-spec.json`).
4. **고정값.** 경로·스테이지 id·스키마 키·필드명·검사 id는 고정값이다. 변경이 필요하다고 판단되면 변경하지 말고 `> [OPEN]`으로 남긴다.
5. **열린 논점.** 다음 형식을 쓴다.

   ```
   > [OPEN] <한두 문장으로 논점>
   > 추천: <작성 레인의 추천안>
   ```

   **★ 본문의 `> [OPEN]` 블록은 집필 시점의 논점 제기이며, 그 처분은 §9가 정본이다.** §9.0이 각 논점을 **[ENG-확정]**(총괄이 조립 단계에서 확정한 공학 결정 — 재정 불요)과 **[OWNER-대기]**(Owner 재정 필요)로 분류한다. 본문의 `[OPEN]`과 §9가 어긋나면 §9가 이긴다. 일부 논점은 본문에서 이미 **[ENG-확정]** 문단으로 대체되었다.
6. **번호.** 절은 `## §0`, 하위는 `### §0.3`. 표를 우선하고, 산문은 표가 담지 못하는 이유·귀결에만 쓴다.

### §0.4 SPEC 목차

| 절 | 제목 | 다루는 것 |
|---|---|---|
| §0 | 문서 지위·범위·용어 | 헌장과의 관계, 발주 범위, 표기 규약, 용어표 |
| §1 | 스테이지 계약 | 파이프라인 전경, 스테이지별 I/O·권한·검사·실패 처리, 체크포인트 2개, 교차표 |
| §2 | 재료 명세 스키마 v0 | `material-spec/v0` 전 필드, 결정론 검사 4종, 예시 인스턴스 |
| §3 | 주석층 표기 규약 | 주석 문법, strip 규칙, `thread.json`·`annotation-index.json` |
| §4 | 게이트 판정 데이터 모델 | `defect`/`flag`/`memo`, `verdict.json`, L0 규칙 목록, 회귀 스위트 |
| §5 | 계기·소견 프로토콜 | 프로브 A/B, 채점자 분리, `score.json`, 판별력 교정, 소견 메모 |
| §6 | 리포 디렉토리 레이아웃 | 리포 트리, 단일 진원 원칙, 이식 단위 경계 |
| §7 | 런 산출물 레이아웃 | `runs/<run-id>/` 트리, 런 ID 규칙, `run.yaml` |
| §8 | 모듈 구현 로드맵 | M1~M12, 의존 그래프, MVP cut, 모듈별 pytest 검증 계획 |
| §9 | 열린 설계 논점 | 전 절의 `[OPEN]` 취합 + Owner 재정 대기 목록 |

### §0.5 용어표

**계약 용어(고정).**

| 용어 | 표기 | 뜻 |
|---|---|---|
| 재료 명세 | material spec | READ 산출물. 기계 정본 = `material-spec.json`, 인간 판독본 = `material-spec.md`(KR) |
| 동결본 | frozen spec | 체크포인트 1 승인 후 버전 스탬프가 찍힌 읽기 전용 사본 |
| 재료 항목 | material item | 인용 단위. ID = `M<n>` |
| 블루프린트 | blueprint | DESIGN 산출물(레시피) |
| 펜 | pen | COMPOSE 담당 모델 레인 |
| 변주 | variant | 한 펜이 낸 한 판. ID = `v1`,`v2`,`v3` |
| 주석층 | annotation layer | 초안에 붙는 근거 표기 |
| 출하본 | shipped thread | 주석 strip 파생물 |
| 결함/플래그/메모 | defect / flag / memo | 게이트 판정 3종 (D7·D8) |

**보강 용어(본 스펙에서 정의).**

| 용어 | 표기 | 뜻 | 근거 |
|---|---|---|---|
| 도슨트 | docent | 엔진의 정체성. 관람객을 미술사학자로 만들지 않고 작품 앞의 10분을 만족스럽게 만든다 | D1 |
| 투자자-팬 | investor-fan | 독자상. 학습자가 아니며, 최적화 대상은 교육의 성공이 아니라 공유 충동이다 | D2 |
| 독해론 | reading procedure | D5의 5단계 절차(청구항 전 분해 → 관계 트리 → 3중 접지 → 유기적 통합 → 포지셔닝). 각 단계는 검증 가능한 중간 산출물을 남긴다 | D5 |
| 체크포인트 | Owner checkpoint | 파이프라인이 정지하고 Owner 재정을 받는 지점. v1은 2개(`material_approval`, `ship_approval`) | D6 |
| 표면 | surface | 체크포인트에서 Owner에게 실제로 제시되는 파일 목록. Owner는 표면만 보고 판정할 수 있어야 한다 | D6 |
| 승인 봉투 | confirm envelope | 체크포인트 통과를 증명하는 파일. 작업 레인은 쓰지 못하고 오케스트레이터가 Owner 응답 후 기록한다 | 재량 |
| 레인 | lane | 한 스테이지(또는 하위 심급)를 수행하는 격리된 모델 실행 단위. `{model, effort}` 쌍으로 지정 | 재량 |
| 심급 | instance / tier | 게이트 내부의 판정 층(L0/L1/L2)과 최종 심급(`gate.final-eyes`). 심급 간 맥락은 공유되지 않는다 | D8·D15 |
| 새 눈 | fresh eyes | 수정 이력·메모·점수를 입력으로 받지 않는 최종 심급 레인 | D8·D15 |
| 전달 표적 | transmission target | 블루프린트가 선언한, 독자에게 반드시 도달해야 하는 재료 ID 목록. 프로브 B 질문의 유일한 파생원 | D9 |
| 전달 충실도 | delivery fidelity | 계기의 측정 대상. "막힘 없이 읽히는가"이며 이해 퀴즈가 아니다 | D9 |
| 계기 | instrument | 스레드만 읽고 행동 프로브를 수행하는 Haiku n대. 자기보고 금지 | D9 |
| 소견 | opinion memo | Fable이 쓰는 비평 메모. 거부권 없음 | D9 |
| 재정 | adjudication | Owner의 구속력 있는 결정. 변주 선택·출하 승인·카탈로그 등재·앵커 fade 확정 | D9·D13·D15 |
| 결정론 검사 | deterministic check | LLM 판단 없이 문자열·포인터·집합 연산만으로 통과/실패가 갈리는 검사 | D6 규율 ③ |
| drop 신호 | drop signal | 안도감이 나올 수 없는 소재라는 독해 레인의 제안. 2단(조기·최종) | D4 |
| 반려 | reject-upstream | 펜이 재료 결함을 발견해 READ로 되돌리는 단방향 경로. 펜은 재료를 고치지 못한다 | D6 규율 ② |
| 자산층 | asset layer | 전량 선편집된 도면 산출물(`30-figures/assets/`). 1급 보존 대상 | D12 |
| 포인터 선택 | pointer selection | 출하 도면 선택을 자산층 참조만으로 표현하는 것(`selection.json`) | D12 |
| 골든 / 변조본 | golden / mutated | 회귀 원장의 두 표본군. 출하 확정본 / 결함을 의도적으로 심은 판 | D8 메타 |
| 앵커 원장 | anchor ledger | 보이스·취향 표본 장부. 독자 반응이 지배 | D13 |
| 회귀 원장 | regression ledger | 게이트·계기 검증 표본 장부. 독자 반응과 무관, 추가 전용 | D13 |
| 이식 단위 | ported unit | historian과 공유하는 `reader/` 디렉토리 전체. 자기 계약(스키마)을 들고 간다 | D14 |

---

## §1 스테이지 계약

### §1.1 파이프라인 전경

```
                                 ┌──────────── reject-upstream (D6 규율 ②) ────────────┐
                                 │        material-defect.md → spec_version + 1        │
                                 ▼                                                     │
  ┌────────┐   ┌──────┐   ★CP1   ┌────────┐   ┌────────┐   ┌─────────┐   ┌─────────┐   │
  │ source │──▶│ read │──[승인]──▶│ freeze │──▶│ design │──▶│ figures │──▶│ compose │───┘
  └────────┘   └──────┘          └────────┘   └────────┘   │ .prepare│   │ ×N 병렬 │
      │           │                   │            │       │ .select │   │  (D10)  │
   patent.md   material-        material-spec   blueprint  └─────────┘   └────┬────┘
   + sha256    spec.json         .v<N>.json      .json      assets/           │
               (draft)           (read-only)                selection.json    │
                                                                              ▼
                        ┌──────── 국소 수정 캡 3 (D8) ────────┐            ┌──────┐
                        │  defect → fix_directive → 펜 재작성  │◀───────────│ gate │
                        └─────────────────────────────────────┘            │L0/L1 │
                                                                           │  L2  │
                                                                           └──┬───┘
                                                                              ▼
                                            ┌───────┐   ┌──────────┐   ┌──────────────────┐
                                            │ probe │──▶│ critique │──▶│ gate.final-eyes  │
                                            │ (D9)  │   │ (Fable)  │   │ 이력·메모 미열람 │
                                            └───────┘   └──────────┘   └────────┬─────────┘
                                                                                ▼
                                                    ★CP2 ship_approval  ┌────────────────┐
                                                    변주 선택 + 출하 승인 │ (D9 재정 단계) │
                                                                        └───────┬────────┘
                                                                                ▼
                                                              ┌──────┐    ┌──────────┐
                                                              │ ship │───▶│ feedback │
                                                              └──────┘    │ +72h 수동 │
                                                            thread.md     └──────────┘
                                                            thread.json   앵커 / 회귀 원장
```

헌장 D6의 주방 분리 도식과의 대응은 다음과 같다. 헌장이 한 덩어리로 적은 `READ`는 스펙에서 `source`+`read`+`freeze` 셋으로 분해되고(원천 취득·독해·동결은 실패 양식이 서로 다르다), `계기 / 소견`은 `probe`+`critique`로 분해된다. 순서는 헌장 도식을 그대로 보존한다.

### §1.2 계약 서식과 공통 규칙

각 스테이지는 `contracts/stages/<id>.yaml` 한 파일을 갖는다(파일명 = 스테이지 id). 서식은 고정이다.

```yaml
id: read
lane: { model: opus-5, effort: high }     # 담당 레인
inputs: [...]                             # 경로 목록
may_read: [...]
must_not_read: [...]
outputs: [...]                            # 필수 산출
optional_outputs: [...]
checks_before_exit: [...]                 # 결정론 검사 명령
failure:                                  # 실패 처리
  - condition: ...
    action: retry(n) | escalate | halt | reject-upstream
owner_checkpoint: { id: ..., surfaces: [...], confirm_file: ... }   # 있는 스테이지만
```

**서식 확장 1건(재량).** `figures`는 두 하위 단계를 가지므로 `steps:` 키를 추가로 허용한다(§1.8). 그 밖의 확장은 두지 않는다.

**공통 규칙.**

| # | 규칙 | 근거 |
|---|---|---|
| C1 | `must_not_read`는 선언적 금지가 아니라 **레인 구성에서 물리적으로 차단**한다(도구 권한·작업 디렉토리 제한). 선언만으로 격리를 주장하지 않는다 | 재량(D6 주방 분리의 집행) |
| C2 | 게이트·계기·최종 심급 레인은 **쓰기 도구를 갖지 않는다**(read-only). 판정 레코드는 러너가 레인의 구조화 출력을 받아 기록한다 | D8 |
| C3 | 작업 레인은 어떤 경우에도 **승인 봉투 파일을 쓰지 않는다**. 봉투는 오케스트레이터가 Owner 응답 후 기록한다 | 재량(D9 재정 단독성의 집행) |
| C4 | 모든 스테이지는 진입 시 `run.yaml`의 `engine_commit`·`reader_version`을 확인하고, 산출물 `provenance`에 그대로 기록한다 | D14 |
| C5 | `checks_before_exit`가 하나라도 실패하면 스테이지는 산출을 확정하지 않는다. 부분 성공 확정은 금지 | 재량 |
| C6 | 실패 조치 어휘는 `retry(n)` / `escalate` / `halt` / `reject-upstream` 넷뿐이다. `escalate`의 수신자는 항상 Owner다 | 브리프 고정 |
| C7 | 재료 명세를 소비하는 모든 스테이지는 **동결본(`15-frozen/`)만** 읽는다. `10-read/`의 작업본을 읽는 것은 계약 위반이다 | D6 |
| C8 | 변주 간 교차 열람 금지. 한 변주 레인은 다른 변주의 어떤 산출물도 읽지 않는다(공정 비교) | D10 |

**레인 배정 요약(초기값, 재량).**

| 스테이지 | 레인 | 비고 |
|---|---|---|
| `source` | 도구 실행(비-LLM) | 다이제스트 계산만 |
| `read` | Opus 5 max × 2 (독립 실행) | 수렴 검사가 2회 실행을 요구(D6 규율 ③) |
| `freeze` | 도구 실행(비-LLM) | 결정론 |
| `design` | Fable | 훅·논지 판단 |
| `figures.prepare` / `.select` | 도구 실행 + Opus 5 high | 렌더는 결정론, 선택 판단은 LLM |
| `compose` | Opus 5 high / Opus 5 max / GPT-5.6-sol | 이종 펜 배정(D10) |
| `gate` L0 | 도구 실행(비-LLM) | 결정론 거부권 |
| `gate` L1 | Opus 5 high × k=3 | 다수결 |
| `gate` L2 | Fable | 자문 |
| `gate.final-eyes` | Opus 5 max (신규 세션) | 이력·메모 미열람 |
| `probe` | Haiku n=5 + 채점자 1 | 채점자는 별도 레인(D9) |
| `critique` | Fable | 소견(D9) |
| `ship` / `feedback` | 도구 실행 + Owner 입력 | |

---

### §1.3 `source`

**직무.** 원천 특허 정본과 도면 원본을 런 작업장에 고정하고, 이후 모든 인용 검증의 기준점이 되는 다이제스트를 확정한다(D6 규율 ③의 전제 — 부분문자열 검사는 고정된 원천 없이 성립하지 않는다).

| 항목 | 내용 |
|---|---|
| `id` | `source` |
| `lane` | 도구 실행(비-LLM) |
| `inputs` | Owner가 지정한 특허 식별자 또는 원문 파일 |
| `outputs` | `00-source/patent.md`, `00-source/patent.sha256`, `00-source/figures-raw/`, `run.yaml`(골격) |
| `may_read` | Owner 투입물, `docs/CHARTER.md` |
| `must_not_read` | — |
| `optional_outputs` | — |

**읽기 권한.** 제약이 없는 유일한 스테이지다. 대신 **쓰기 대상이 `00-source/`와 `run.yaml`로 한정**되며, 이후 어떤 스테이지도 `00-source/` 아래를 수정하지 못한다(읽기 전용 고정).

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `source.digest-recorded` | `patent.sha256`의 값이 `patent.md`의 실제 SHA-256과 일치 |
| `source.claims-section` | `patent.md`에 청구항 구간이 식별 가능한 경계로 존재(READ의 verbatim 검사가 이 구간을 대상으로 함) |
| `source.figures-manifest` | `figures-raw/` 파일 수 ≥ 1이고 파일명이 도면 번호로 정렬 가능 |
| `source.run-id` | `run.yaml`의 `run_id`가 `<assignee-slug>-<pubnum>-<topic-slug>` 형식이고 디렉토리명과 일치 |

**실패 처리.**

| 조건 | 조치 | 비고 |
|---|---|---|
| 원천 텍스트 취득 실패·문자 깨짐 | `halt` | 하류 전부가 무의미해진다 |
| 청구항 구간 경계 식별 실패 | `escalate` | 원천 형식 문제이므로 자동 복구 대상 아님 |
| 도면 0장 | `escalate` | D11·D12는 도면을 전제한다. 도면 없는 소재는 Owner 재정 사항 |
| `run_id` 형식 위반 | `halt` | 디렉토리 재생성 필요 |

> [OPEN] `patent.md` 생성 경로(원천 취득 도구)를 이 엔진 안에 둘지, 외부 산출물을 수동 투입할지 헌장은 규정하지 않는다.
> 추천: 엔진 밖 도구의 산출물을 수동 투입하고 `source`는 다이제스트·구조 검사만 책임진다. 취득 도구를 리포에 들이면 이식 단위(`reader/`) 경계가 흐려진다.

---

### §1.4 `read`

**직무.** 독해론 5단계를 실행해 재료 명세 초안을 만들고, 각 단계의 검증 가능한 중간 산출물을 남긴다(D5). 산출물의 형식 구조화와 검증 기계화가 결정론이 사는 자리다(D6). 이 스테이지가 "LLM 막연한 추론 1회"를 대체하는 지점이다.

| 항목 | 내용 |
|---|---|
| `id` | `read` |
| `lane` | Opus 5 max × 2 독립 실행(수렴 검사용) |
| `inputs` | `00-source/patent.md`, `00-source/patent.sha256`, `00-source/figures-raw/`, `run.yaml` |
| `outputs` | `10-read/material-spec.json`(`status: draft`), `10-read/material-spec.md`, `10-read/claim-trees/`, `10-read/grounding.md`, `10-read/positioning.md`, `10-read/drop-signal.md`, `10-read/convergence.json` |
| `optional_outputs` | — |
| `may_read` | `00-source/**`, `reader/procedure/**`, `reader/schemas/material-spec.schema.json`, `docs/CHARTER.md`, (반려 시) `40-compose/<variant>/material-defect.md` |
| `must_not_read` | `20-design/**`, `40-compose/**`(반려서 제외), `50-gate/**`, `65-critique/**`, `ledgers/anchors/**` |

**읽으면 안 되는 것의 이유.** 독해는 서사·훅을 모르는 상태에서 수행되어야 한다. 블루프린트나 초안을 본 독해 레인은 "쓰기 좋은 재료"를 향해 편향되며, 이는 재료 명세가 historian과의 계약(D14)이라는 사실과 정면으로 충돌한다 — 재료는 이 스레드가 아니라 이 특허의 함수여야 한다. 반려서(`material-defect.md`)만 예외적으로 읽는데, 그것이 단방향 반려 경로의 유일한 통신 수단이기 때문이다(D6 규율 ②).

**D5 5단계 ↔ 산출물 대응.**

| D5 단계 | 산출물 | 형태 |
|---|---|---|
| ① 청구항 구성요소 전 분해 | `claim-trees/`, `material-spec.json` `claims.independent[]`·`claims.dependents[]` | 독립항별 별도 트리, 종속항 부가 한정은 `attaches_to`로 골격 밑 층위 누적 |
| ② 관계 트리 도식화 | `claim-trees/` (표 또는 폴더 트리형) | 인간 판독용 |
| ③ 3중 접지 | `grounding.md`, `items[]` 중 `kind: grounding` | 구성요소 ↔ 명세서 문단 ↔ 도면부호 |
| ④ 유기적 통합 | `material-spec.md`(KR 렌더의 통합 그림 절) | |
| ⑤ 포지셔닝 | `positioning.md`, `items[]` 중 `kind: positioning` | 배경기술·효과 대비 |

**drop 신호 2단(D4).** `drop-signal.md`는 두 시점에 각각 기록된다 — ① 청구항 분해 직후 조기 신호 ② 포지셔닝 확정 후 최종. 스키마상 `drop_signal.stage ∈ {early, final}`이다(§2). 조기 신호가 `drop-proposed`면 그 시점에 즉시 `escalate`하며, 나머지 단계를 다 돌린 뒤 보고하지 않는다(비용 절약이 아니라, 하류 산출물이 Owner의 판단을 오염시키는 것을 막기 위함).

**종료 전 검사.** 결정론 검사 4종(§2.3)을 전부 통과해야 한다.

| 검사 id | 판정 기준 | 실패 시 |
|---|---|---|
| `read.verbatim` | 모든 `text_verbatim`·`quote`가 `00-source/patent.md`의 바이트 정확 부분문자열 | `retry(1)` → `escalate` |
| `read.pointer-resolve` | 모든 구조 ID 참조(`claim_ref`·`component`·`attaches_to`·`derived_from`·`figure`)가 실재 대상으로 해소 | `retry(1)` → `escalate` |
| `read.coverage` | 모든 청구항 element가 최소 1개 `grounding` 항목으로 접지 | `retry(1)` → `escalate` |
| `read.convergence` | 독립 2회 실행 비교: 독립항 수 동일 + element `text_verbatim` 집합 Jaccard ≥ 0.95 | `retry(1)` → 여전히 미달이면 `escalate` |
| `read.schema` | `reader/schemas/material-spec.schema.json` 검증 통과 | `retry(1)` → `halt` |

`read.convergence`의 의미는 품질이 아니라 **안정성**이다. 두 독립 실행이 다른 청구항 트리를 낳는다면 그 소재에 대한 독해는 재현되지 않는 것이고, 이후 모든 결정론 검사의 기준점이 흔들린다. 따라서 수렴 미달은 재료 품질 결함이 아니라 **절차 신호**로 처리해 Owner에게 올린다.

**실패 처리 종합.**

| 조건 | 조치 |
|---|---|
| `read.verbatim` / `pointer-resolve` / `coverage` 실패 | `retry(1)` → 재실패 시 `escalate` |
| `read.convergence` 미달 | `retry(1)` → 재실패 시 `escalate`(Owner 재정: 소재 변경 또는 절차 수정) |
| `drop-signal` = `drop-proposed`(early 또는 final) | `escalate` — 하류 진행 정지 |
| 원천 다이제스트가 `run.yaml` 기록과 불일치 | `halt` — 원천이 도중에 바뀐 런은 폐기 대상 |
| 반려 수신(`material-defect.md`) | 재요리: `spec_version` + 1로 개정, 항목은 append-only(§1.6) |

---

### §1.5 ★CP1 — `material_approval`

**부착 위치.** `read` 스테이지의 `owner_checkpoint`. 통과 봉투가 있어야 `freeze`가 진입한다.

```yaml
owner_checkpoint:
  id: material_approval
  surfaces:
    - 10-read/material-spec.md      # KR 인간 판독본 — 주 표면
    - 10-read/drop-signal.md
    - 10-read/positioning.md
    - 10-read/convergence.json      # 안정성 근거
  confirm_file: 15-frozen/approval-v<N>.md
  question: >
    이 재료만 읽고 이 특허가 무엇을 하는 물건인지, 그리고 투자자-팬의 어떤 질문에
    답할 수 있는지 말할 수 있는가? 말할 수 없다면 어느 항목이 비었는지 지적하라.
```

**표면은 KR 문서다.** 기계 정본은 `material-spec.json`이지만 Owner에게 제시되는 것은 `material-spec.md`다. `.md`는 `.json`의 결정론 렌더이며, 렌더가 원본 항목을 누락하면 `freeze.render-parity` 검사가 잡는다(§1.6).

**설계 귀결 — 별도 브리핑을 만들지 않는다.** 헌장은 "체크포인트 1의 재료 검토가 Owner 이해층을 겸한다 — 별도 브리핑은 두지 않는다"고 재정했다(D6). 이는 편의 판단이 아니라 구조적 선택이며, 다음 세 귀결을 낳는다.

1. **산출물 하나가 두 독자를 섬긴다.** `material-spec.md`는 하류 기계의 정답지이자 Owner의 이해 문서다. 따라서 이 문서의 품질 기준은 "Owner가 원천 특허를 다시 열지 않고 판정할 수 있는가"이며, 이는 스타일 요구가 아니라 **완결성 요구**다(빠진 항목은 곧 Owner가 볼 수 없는 항목이다).
2. **브리핑 전용 산출물을 신설하지 않는다.** 구 PAW의 `owner-briefing.md` / `owner-study-pack.md` 이원 구조는 이식하지 않는다. 두 문서로 나뉘는 순간 어느 쪽이 정본인지 다시 정해야 하고, 재료 명세와의 정합 검사가 두 배가 된다.
3. **이해 확인 퀴즈를 두지 않는다.** 헌장에 근거가 없고, 이해 측정은 계기(D9)의 관할이되 그 대상은 Owner가 아니라 독자다. Owner에 대한 측정은 재정 권한(D9)과 충돌한다.

**승인 봉투(`15-frozen/approval-v<N>.md`) 유효 요건(재량).**

| 필드 | 값 |
|---|---|
| `status` | `approved` \| `rejected` |
| `by` | `owner` |
| `spec_version` | 승인 대상 버전 `N` |
| `spec_digest` | 승인 시점 `10-read/material-spec.json`의 SHA-256 |
| `date` | 실제 날짜(플레이스홀더 불가) |
| `drop_decision` | `go` \| `drop` — `drop-signal.md`가 `drop-proposed`인 경우 필수 |

봉투의 `spec_digest`가 실제 파일과 다르면 승인은 **무효**다. 승인 후 재료가 조용히 바뀌는 경로를 봉쇄하는 장치다.

> [OPEN] `drop-proposed`에 대해 Owner가 `go`로 재정한 경우, 그 근거를 런 안(`approval-v<N>.md`)에만 남길지 `docs/decisions/`에도 등재할지 헌장은 규정하지 않는다.
> 추천: 런 봉투에 기록하고 `docs/decisions/`에는 등재하지 않는다. 소재별 1회성 판단이며 재사용되는 규범이 아니다.

---

### §1.6 `freeze`

**직무.** 승인된 재료 명세에 버전 스탬프와 다이제스트를 찍고 읽기 전용 사본을 만든다(D6). 이 스테이지 이후 재료는 하류 전체에 대해 불변이다.

| 항목 | 내용 |
|---|---|
| `id` | `freeze` |
| `lane` | 도구 실행(비-LLM) |
| `inputs` | `10-read/material-spec.json`, `10-read/material-spec.md`, `15-frozen/approval-v<N>.md` |
| `outputs` | `15-frozen/material-spec.v<N>.json` |
| `may_read` | `10-read/**`, `15-frozen/**`, `00-source/patent.sha256` |
| `must_not_read` | — (결정론 스테이지) |

**동결이 하는 세 가지.**

| 동작 | 내용 | 목적 |
|---|---|---|
| 버전 스탬프 | `spec_version: N`, `status: "frozen"` 기입 | 인용의 시점 고정 |
| 다이제스트 | 동결본의 SHA-256을 산출해 `run.yaml`에 기록. 하류 산출물은 이 값을 `spec_digest`로 복사 | 조용한 교체 탐지 |
| 읽기 전용화 | 파일 권한 `0444` + 러너의 쓰기 경로 목록에서 `15-frozen/` 제외 | 물리적 불변 |

**동결 이후 재료가 바뀌는 유일한 경로.** 반려 → 개정(`spec_version` + 1) 한 갈래뿐이다(D6 규율 ②). 어떤 하류 스테이지도 재료를 직접 수정하지 못하며, 펜이 결함을 발견해도 고치지 않고 `material-defect.md`를 써서 READ로 되돌린다. 개정 시 `15-frozen/material-spec.v<N+1>.json`이 **새 파일로** 생기고 `v<N>`은 지우지 않는다.

**개정이 기존 인용에 하는 일(항목 ID append-only 규율).**

| 상황 | 개정 후 항목 상태 | 그 항목을 인용한 문장의 처분 |
|---|---|---|
| 항목이 그대로 유지됨 | `active` | 유효. 아무 일도 일어나지 않는다 |
| 항목이 잘못된 것으로 판명 | `retracted` | **결함**. `citation.resolve`가 `retracted` 인용을 거부한다(§4) |
| 항목이 더 정확한 항목으로 교체됨 | `superseded`, `superseded_by: "M42"` | **결함**. 다만 `fix_directive`가 후속 ID를 명시할 수 있어 국소 수정으로 수렴하기 쉽다 |
| 항목이 신규 추가됨 | 새 ID `M<n+1>` | 기존 문장에 영향 없음 |

`M<n>`은 런 내 순번이며 **재사용·재번호가 금지**된다. 이유는 두 가지다. ① 주석층 인용이 개정 후에도 해소되어야 한다 — ID를 재사용하면 같은 `[M7]`이 다른 재료를 가리키게 되어 게이트가 조용히 통과시킨다. ② 개정된 재료를 인용한 문장을 게이트가 **정확히 지목**할 수 있어야 한다(D8 국소 수정 지시의 전제).

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `freeze.approval-valid` | `approval-v<N>.md`의 `status: approved`, `by: owner`, `spec_digest`가 실제 파일과 일치 |
| `freeze.digest-match` | 동결본의 `patent.source_digest`가 `00-source/patent.sha256`과 일치 |
| `freeze.readonly` | `15-frozen/material-spec.v<N>.json`의 권한이 쓰기 불가 |
| `freeze.render-parity` | `material-spec.md`에 모든 `items[].id`가 1회 이상 등장(KR 렌더 누락 탐지) |
| `freeze.id-monotonic` | 개정 시: `v<N-1>`의 모든 항목 ID가 `v<N>`에 존재하고, 삭제된 ID가 없음 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| 승인 봉투 부재·`status != approved` | `halt` |
| `spec_digest` 불일치(승인 후 재료 변경) | `halt` — 재승인 필요 |
| `freeze.digest-match` 실패(원천 다이제스트 불일치) | `halt` |
| `freeze.render-parity` 실패 | `reject-upstream`(→ `read`, 렌더 재생성) |
| `freeze.id-monotonic` 실패(항목 삭제·재번호) | `reject-upstream`(→ `read`) |

---

### §1.7 `design`

**직무.** 동결 재료로부터 레시피를 만든다 — 훅·논지·트윗 골격·도면 배치(D6). 독자는 학습자가 아니라 투자자-팬이므로(D2) 훅은 그 불안·질문에 조응하되, 답은 특허 물증에 근거한 기술 서사로만 하도록 골격을 짠다(D3).

| 항목 | 내용 |
|---|---|
| `id` | `design` |
| `lane` | Fable |
| `inputs` | `15-frozen/material-spec.v<N>.json`, `30-figures/assets/manifest.json`(선행 실행된 경우) |
| `outputs` | `20-design/blueprint.json`, `20-design/blueprint.md`(KR 요약) |
| `may_read` | `15-frozen/**`, `30-figures/assets/manifest.json`, `docs/CHARTER.md`, `ledgers/anchors/**` |
| `must_not_read` | `00-source/**`, `10-read/**`(작업본), `40-compose/**` |

**원천을 읽지 않는다.** 설계는 동결 재료만 본다(C7). 원천을 여는 순간 재료에 없는 사실이 블루프린트에 들어오고, 그 사실을 펜이 쓰면 `citation.resolve`가 잡지 못하는 무근거 주장이 생긴다(재료에 없으므로 인용할 ID 자체가 없다 → 펜은 `[narrative]`로 밀수하게 된다).

**블루프린트가 선언해야 하는 것(계약 수준).** 상세 스키마는 `contracts/schemas/blueprint.schema.json` 소관이며 §8 M5에서 확정한다. 계약상 필수 선언은 다음이다.

| 필드 | 내용 | 소비자 |
|---|---|---|
| `hook` | 투자자의 질문 형태 + T1 도면 지정 | `compose` |
| `slots[]` | 트윗별 `{slot ∈ hook\|stop\|pivot\|landing\|tail, exhibit, figure}` — 트윗 수는 강한 전시물 수의 종속변수(D11) | `compose`, `gate` |
| `transmission_targets[]` | 독자에게 도달해야 하는 재료 ID 목록 | `probe`(프로브 B 질문의 유일한 파생원, D9) |
| `new_terms[]` | 도입을 허용하는 신규 용어와 그 트윗 배정(트윗당 ≤ 1, D11) | `gate` `format.new-term-budget` |
| `figure_plan` | 트윗별 도면 지정(포스트당 ≤ 4, D11) | `figures.select`, `gate` |
| `numeric_whitelist` | 재료에 없어도 허용할 수치(예: 스레드 순번 `n/N`) — `run.yaml`에 추기 | `gate` `numeric.exhaustive` |

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `design.schema` | `blueprint.schema.json` 검증 통과 |
| `design.targets-resolve` | `transmission_targets[]`의 모든 ID가 동결본에 `active` 상태로 존재 |
| `design.slot-count` | `slots[]` 길이가 6~12이고 `hook`·`landing` 각 1개 존재(D11) |
| `design.figure-budget` | 트윗별 도면 수 ≤ 4, `figure_plan`의 모든 도면이 `assets/manifest.json`에 존재 |
| `design.spec-digest` | `blueprint.json`의 `spec_digest`가 현재 동결본과 일치 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| 스키마·슬롯·표적 해소 실패 | `retry(1)` → `escalate` |
| `transmission_targets`가 `retracted`/`superseded` 항목을 지목 | `retry(1)` — 개정본 기준으로 재작성 |
| 재료로 훅이 서지 않음(안도감 착지 불가 판단) | `escalate` — D4의 drop 재검토 사안이며 설계 레인이 단독 결정하지 않는다 |
| `spec_digest` 불일치 | `halt` |

---

### §1.8 `figures` (`prepare` / `select`)

**직무.** 원천 도면을 **전량** 편집해 자산층을 만들고(`prepare`), 출하 도면을 포인터로만 선택한다(`select`). 도면은 핵심 자산이며 선택분만 편집하면 재편집 왕복과 유실 위험이 생긴다(D12).

```yaml
id: figures
steps:
  - id: figures.prepare
    lane: { tool: headless-chromium, model: none }
    depends_on: [freeze]          # design에 의존하지 않음 → 일정상 선행 실행 가능
  - id: figures.select
    lane: { model: opus-5, effort: high }
    depends_on: [design, figures.prepare]
```

| 하위 단계 | 입력 | 산출 | 성격 |
|---|---|---|---|
| `figures.prepare` | `00-source/figures-raw/`, `15-frozen/material-spec.v<N>.json`(도면부호·캡션) | `30-figures/assets/fig-NN.png`, `30-figures/assets/manifest.json` | 전량 편집. 1200×675 @2x, HTML/CSS/SVG 조판 → 헤드리스 Chromium. matplotlib 금지(D12) |
| `figures.select` | `20-design/blueprint.json`, `30-figures/assets/manifest.json` | `30-figures/selection.json` | **포인터만.** 자산 파일을 복사·가공하지 않는다 |

**계약 순서와 실행 순서.** 헌장 도식의 순서는 `DESIGN → FIGURES`이며 계약 순서로 그대로 유지한다(D6). 다만 `figures.prepare`는 블루프린트에 의존하지 않으므로 **일정상 `design`과 병렬 또는 선행 실행이 가능**하다. 이는 전량 선편집 원칙의 자연 귀결이다(D12) — 무엇을 쓸지 모르는 상태에서 전부 편집하는 것이 원칙이므로, 설계를 기다릴 이유가 없다. `figures.select`만 `design` 완료를 기다린다.

**v1 렌더 경로 = 폴백만.** 템플릿 스튜디오는 별도 발주다(D12). 따라서 `figures.prepare`의 v1 구현은 **원본 크롭 + 최소 주석** 경로 하나뿐이며, 3종 템플릿·디자인 토큰·팔레트 확정은 이 스펙의 범위 밖이다(§0.2). 폴백 상비는 정직성 장치이므로, 스튜디오가 생긴 뒤에도 이 경로를 제거하지 않는다(D12).

**읽어도 되는 것 / 안 되는 것.**

| | `may_read` | `must_not_read` |
|---|---|---|
| `prepare` | `00-source/figures-raw/**`, `15-frozen/**`, `studio/**` | `20-design/**`(편집 편향 방지), `40-compose/**` |
| `select` | `20-design/blueprint.json`, `30-figures/assets/manifest.json`, `15-frozen/**` | `00-source/**`, `40-compose/**` |

`prepare`가 블루프린트를 읽지 않는 이유는 의존 부재의 형식적 귀결이 아니라 실질적 방어다 — 블루프린트를 본 편집 레인은 선택될 도면만 정성껏 편집하게 되고, 그 순간 "전량 선편집"은 이름만 남는다.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `figures.asset-completeness` | `figures-raw/`의 모든 도면에 대응하는 `assets/fig-NN.png`가 존재(전량 편집의 기계 확인) |
| `figures.render-spec` | 모든 자산이 1200×675, @2x(실제 픽셀 2400×1350) |
| `figures.manifest-parity` | `manifest.json`의 항목 수 = 자산 파일 수, 각 항목이 동결본 `figures[]`의 `id`로 해소 |
| `figures.selection-resolve` | `selection.json`의 모든 포인터가 `manifest.json`에 해소되고, 포스트당 ≤ 4 |
| `figures.no-copy` | `selection.json`이 파일 경로 복사본이 아니라 자산 ID 참조만 담음 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| 일부 도면 렌더 실패 | `retry(1)` → 재실패 시 `escalate`(누락 도면 목록 첨부). 부분 자산층으로 진행하지 않는다 |
| `figures.render-spec` 위반 | `retry(1)` → `halt` |
| `selection.json` 포인터 미해소 | `retry(1)` → `escalate` |
| 블루프린트가 지정한 도면이 자산층에 없음 | `reject-upstream`(→ `design`) |

**교정 원장.** 도면 선택·기각과 그 이유는 `ledgers/corrections.md`에 기록한다(D12). 기록 주체는 `figures.select`이며, Owner가 CP2에서 도면을 바꾼 경우 `ship`이 추기한다.

---

### §1.9 `compose`

**직무.** 동결 재료와 블루프린트만으로 주석층이 붙은 초안을 쓴다(D6·D8). 변주 n판을 이종 펜에 병렬 배정한다(D10).

| 항목 | 내용 |
|---|---|
| `id` | `compose` |
| `lane` | 변주별 이종 펜 — Opus 5 high / Opus 5 max / GPT-5.6-sol (D10 초기 배정) |
| `inputs` | `15-frozen/material-spec.v<N>.json`, `20-design/blueprint.json`, `30-figures/selection.json`, `30-figures/assets/manifest.json` |
| `outputs` | `40-compose/<variant>/thread.annotated.md` |
| `optional_outputs` | `40-compose/<variant>/material-defect.md` |
| `may_read` | 위 `inputs` 전부, `contracts/glossary.md` |
| `must_not_read` | **`00-source/**`**, `10-read/**`, `40-compose/<other-variant>/**`, `50-gate/**`(자기 변주의 현 라운드 지시 제외), `65-critique/**`, `contracts/lexicon/forbidden.yaml`, `contracts/lexicon/defect-catalog.yaml` |

**펜은 원천 특허를 보지 않는다.** 이것이 주방 분리의 핵심이다(D6). 펜이 볼 수 있는 사실의 우주는 동결 재료 `items[]`가 전부이며, 그래야 "본문의 모든 기술 주장이 재료 항목 ID로 역참조 가능"하다는 규율(D6 규율 ①)이 **구조적으로** 성립한다. 펜이 원천을 볼 수 있다면 역참조 불가능한 참사실이 생기고, 게이트는 그것을 환각과 구별할 방법이 없어진다 — 그리고 그것을 구별할 필요를 없애는 것이 이 설계의 목적이다.

**변주 병렬 = 공정 비교.** 모든 변주는 **같은 재료·같은 블루프린트**를 받는다(D10). 변주 간 교차 열람은 금지된다(C8) — 한 펜이 다른 펜의 판을 보면 토너먼트 표는 모델 비교가 아니라 순서 효과의 기록이 된다. 변주 수는 2~3이며 `run.yaml`의 펜 배정에 기록된다. 배치 단위 승률 70% 이상이 굳으면 주전 승격 + 변주 수 축소(D10) — 이 판정은 `ledgers/tournament.jsonl` 소관이며 §7·§8에서 다룬다.

**펜 프롬프트에 금지 목록을 넣지 않는다(D8).** 헌장은 "긍정형(스코프 선언 + 도슨트 정체성)만 담는다. 금지 열거는 검증 심급에만 둔다"고 재정했다. 근거는 프라이밍 효과이며, 여기서 긍정형으로 선언되는 정체성은 D1의 도슨트 비유 그대로다(D1). 계약 수준의 강제는 다음 두 장치다.

| 장치 | 내용 |
|---|---|
| **권한 차단** | `contracts/lexicon/forbidden.yaml`·`defect-catalog.yaml`을 펜 레인의 `must_not_read`에 둔다. 프롬프트가 그것을 인용하려면 파일을 읽어야 하므로 물리적으로 막힌다(C1) |
| **프롬프트 템플릿 린트** (`compose.prompt-lint`) | 펜 프롬프트 템플릿에 대해 부정 명령형 패턴 `/\b(do not\|don't\|never\|avoid\|금지\|하지 마)\b/i`와 금지 어휘 정본의 리터럴 문자열 출현을 검사해, 1건이라도 발견되면 스테이지 진입을 거부한다 |

린트가 검사하는 대상은 산출물이 아니라 **프롬프트 자체**라는 점이 중요하다 — 이 규율은 결과물에서 사후 확인할 수 없고 입력에서만 집행 가능하다.

**주석층 작성 의무.** 트윗·문장마다 근거 재료 ID를 `[M3,M7]`로 표기하고, 근거가 필요 없는 서사 조직은 `[narrative]`로 자기 신고한다(D8). 문법 정본은 §3이다. 태그 없는 문장은 L0 결함(`annotation.missing-tag`)이다.

**재료 반려(D6 규율 ②).** 펜이 재료 결함(사실 오류·접지 불가·필요한 사실 부재)을 발견하면 **재료를 고치지 않고** `40-compose/<variant>/material-defect.md`를 쓰고 정지한다. 반려서 필수 필드는 다음이다.

| 필드 | 내용 |
|---|---|
| `material_ids` | 문제가 된 항목 ID 목록 |
| `defect_kind` | `factual-error` \| `unresolvable-grounding` \| `missing-fact` |
| `evidence` | 재료 내부의 모순 지점(원천 인용 금지 — 펜은 원천을 보지 못한다) |
| `blocked_slots` | 이 결함 때문에 쓸 수 없는 블루프린트 슬롯 |

반려 경로는 **단방향**이다: `compose` → `read` → 개정(`spec_version` + 1) → `freeze` → 하류 재실행. 펜이 재료 명세를 편집하는 경로는 존재하지 않는다.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `compose.prompt-lint` | (진입 시) 펜 프롬프트에 부정 명령형·금지 어휘 리터럴 부재 |
| `compose.spec-digest` | 프런트매터 `spec_digest`가 현재 동결본과 일치 |
| `compose.annotation-syntax` | 주석 문법 파싱 성공(§3), 모든 문장에 태그 정확히 1개 |
| `compose.frontmatter` | `run_id`·`variant`·`pen`·`spec_version`·`spec_digest` 전부 존재 |

이 검사들은 게이트가 아니라 **스테이지 종료 조건**이다. 문법이 깨진 초안은 게이트에 도달하기 전에 되돌린다(게이트의 시간을 파싱 오류에 쓰지 않는다).

**실패 처리.**

| 조건 | 조치 |
|---|---|
| `compose.annotation-syntax` 실패 | `retry(2)` → `escalate` |
| `compose.spec-digest` 불일치 | `halt` — 동결본이 바뀐 채로 쓰인 판은 폐기 |
| `compose.prompt-lint` 실패 | `halt` — 프롬프트 수정 후 재개(D8 위반은 재시도로 해소되지 않는다) |
| 펜이 재료 결함 발견 | `reject-upstream`(→ `read`), `material-defect.md` 첨부 |
| 펜 레인 사망·응답 불가 | `retry(1)` → 해당 변주만 결번 처리, 잔여 변주 ≥ 2면 진행, < 2면 `escalate` |

> [OPEN] 재료 반려로 `spec_version`이 +1 된 경우, 이미 완성된 다른 변주의 초안을 폐기하고 전량 재작성할지, 영향받은 변주만 재작성할지 헌장은 규정하지 않는다.
> 추천: **전량 재작성.** 변주가 서로 다른 `spec_version` 위에 서 있으면 D10의 공정 비교 전제가 깨지고 토너먼트 기입이 오염된다. 비용은 있으나 장부 신뢰도가 우선한다.

---

### §1.10 `gate`

**직무.** 정답이 존재하는 범위에서만 판정한다(D7). 3층 + 최종 심급으로 구성되며, **어떤 경우에도 직접 글을 고치지 않는다**(D8).

| 항목 | 내용 |
|---|---|
| `id` | `gate` |
| `lane` | L0 = 도구 실행 / L1 = Opus 5 high × k=3 / L2 = Fable / `gate.final-eyes` = 신규 세션 Opus 5 max |
| `inputs` | `40-compose/<variant>/thread.annotated.md`, `15-frozen/material-spec.v<N>.json`, `20-design/blueprint.json`, `30-figures/selection.json`, `contracts/lexicon/forbidden.yaml`, `run.yaml` |
| `outputs` | `50-gate/<variant>/l0.json`, `l1.json`, `l2.md`, `verdict.json`, `annotation-index.json`, `thread.stripped.md` |
| `optional_outputs` | `50-gate/<variant>/revisions/r<n>/` |
| `may_read` | 위 `inputs`, `ledgers/regression/**` |
| `must_not_read` | `00-source/**`(재료 대조는 동결본 기준), `40-compose/<other-variant>/**` |

**쓰기 권한이 없다.** 게이트 레인은 read-only로 구성된다(C2). 판정 레코드는 러너가 레인의 구조화 출력을 받아 기록하며, 레인은 파일 시스템에 접근하지 않는다. `defect.fix_directive`는 "어디를·어느 재료로" 형식의 **지시문**이고 대체 문장을 제공하지 않는다 — 대체 문장을 쓰는 순간 게이트가 필자가 되고, 검사자 소견과 펜 집필의 관할선이 무너진다(D8).

**층별 관할과 거부권.**

| 층 | 관할 | 거부권 | 산출 | 근거 |
|---|---|---|---|---|
| **L0 결정론** | 스레드 규격·주석층 스키마·인용 ID 해소·금지 어휘 regex·숫자 전수 대조 | **있음** | `l0.json` (`defect[]`) | D8 |
| **L1 국소 대조** | 문장↔인용 재료 정합, `[narrative]` 신고 감사(기술 주장 밀수 검출) | **있음** | `l1.json` (`defect[]`, `flag[]`, `votes[]`) | D8 |
| **L1 의미 금지선** | 암시적 투자 조언 | **없음**(플래그) | `l1.json` `flags[]` → CP2 첨부 | D8·D3 |
| **L2 전역 판단** | 자문 비평 | **없음** | `l2.md` (`memo[]`, **점수 금지**) | D8 |
| **`gate.final-eyes`** | 출하 적격 최종 판정 | **있음** | `verdict.json` `final_eyes` | D8·D15 |

L1은 k=3 독립 실행 다수결이며 과반 일치 항목만 `defect`로 채택하고, 소수 의견은 `flag`로 강등해 기록한다. 판정 레코드의 필드 구조·`verdict.json` 스키마·L0 규칙 목록·숫자 전수 대조 알고리즘·회귀 스위트 형식은 **§4 소관**이다. 본 절은 위상과 계약만 다룬다.

**루프 위상(D8).**

```
  ┌─ 결함 경로 ────────────────────────────────────────────────┐
  │  l0/l1 defect[] ─▶ fix_directive ─▶ 펜 국소 수정 ─▶ 재판정  │
  │       ↑____________________________________________|       │
  │            캡 3회. 초과 = escalate (대개 재료 반려행)        │
  └────────────────────────────────────────────────────────────┘

  ┌─ 판단 경로 ────────────────────────────────────────────────┐
  │  l2 memo ─(1회)─▶ 펜 자유 리비전 ─(1회)─▶ 위상 봉쇄. 끝.     │
  └────────────────────────────────────────────────────────────┘

  ┌─ 최종 심급 ────────────────────────────────────────────────┐
  │  gate.final-eyes: 입력 = 출하 후보 + 동결 재료. 그것뿐.      │
  │  revisions/·l2.md·65-critique/·score.json 전부 must_not_read │
  └────────────────────────────────────────────────────────────┘
```

두 경로의 비대칭이 설계의 요점이다. 결함은 정답이 있으므로 수렴할 때까지 돌리되 캡을 둔다(수렴하지 않는다는 것 자체가 상류 결함 신호다). 판단은 정답이 없으므로 **1회 왕복으로 위상을 닫는다** — 열어두면 점수 추격 루프가 되고, 그것이 굿하트 가드가 막으려는 것이다(D15).

**최종 심급 = 새 눈.** `gate.final-eyes`는 수정 이력·L2 메모·계기 점수·소견을 모르는 별도 레인이다(D8·D15). 입력은 출하 후보 텍스트와 동결 재료뿐이다. "여러 번 고쳐서 여기까지 왔다"는 사실 자체가 판정을 무르게 만드는 것을 막는 장치다.

**국소 수정 라운드의 파일 규율(재량).** 라운드 `r<n>`은 `50-gate/<variant>/revisions/r<n>/`에 지시(게이트 산출)와 결과(펜 산출)를 함께 둔다. 채택된 라운드의 결과가 `40-compose/<variant>/thread.annotated.md`를 덮어쓰고, 직전 판은 `revisions/`에 보존된다. 즉 `40-compose/`의 파일은 항상 **현행 최신본**이다.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `gate.l0-clean` | `l0.json`의 `defects[]`가 빈 배열 |
| `gate.l1-clean` | `l1.json`의 `defects[]`가 빈 배열 (`flags[]`는 무관) |
| `gate.no-score` | `l2.md`·`verdict.json`에 점수 필드·점수 패턴 부재(§4의 린트) |
| `gate.no-rewrite` | 모든 `fix_directive`가 대체 문장을 포함하지 않음(지시문 형식 린트) |
| `gate.annotation-index` | `annotation-index.json`이 트윗→문장→인용 ID 전건을 담고, 초안 문장 수와 일치 |
| `gate.final-eyes-isolation` | 최종 심급 레인의 입력 목록에 `revisions/`·`l2.md`·`65-critique/`·`60-probe/`가 없음 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| L0/L1 결함 발생 | `fix_directive` 발행 → 국소 수정 라운드. 캡 3회 |
| 국소 수정 캡 3회 초과(수렴 실패) | `escalate` — 상류 결함 신호로 보고. 대개 재료 반려행(D8) |
| `gate.no-rewrite` 실패(게이트가 문장을 제공) | `halt` — D8 위반. 게이트 프롬프트 수정 후 재개 |
| `gate.no-score` 실패 | `halt` — D8·D15 위반 |
| `gate.final-eyes-isolation` 실패 | `halt` — 격리가 깨진 판정은 무효 |
| 최종 심급 부적격 판정 | `escalate` — 해당 변주 탈락 |
| **변주 전멸**(전 변주가 캡 초과 또는 최종 심급 탈락) | `escalate` — Owner 재정. 재료 반려인지 블루프린트 개정인지는 Owner가 정한다 |

> [OPEN] 변주 전멸 시 기본 복구 경로를 블루프린트 개정(설계 문제로 간주)으로 둘지 재료 반려(재료 문제로 간주)로 둘지 헌장은 규정하지 않는다.
> 추천: **블루프린트 개정 1회 → 재전멸 시 재료 반려**. 전 변주가 같은 지점에서 실패하면 공통 입력의 문제이고, 그중 개정 비용이 싼 쪽이 블루프린트다.

**[ENG-확정] `gate.final-eyes`의 지위와 산출 경로.** 집필 시점에 제기된 논점(독립 스테이지인가 / 최종 심급의 산출 경로가 런 레이아웃에 없다)은 헌장 범위 안의 공학 결정이므로 조립 단계에서 다음과 같이 확정했다(§9.0 E6).

- `gate.final-eyes`는 **`gate.yaml` 내부의 하위 심급**이다. 고정 스테이지 id 목록을 늘리지 않는다. 실행 순서상 `critique` 이후 `gate`로 재진입한다.
- 산출은 `verdict.json`의 `final_eyes` 객체에 담는다. **신규 경로를 만들지 않는다.**
- 근거: 최종 심급은 별도의 입력·산출 계약을 갖는 것이 아니라 **같은 판정의 마지막 층**이며, 그 특수성은 경로가 아니라 격리 규칙(`gate.final-eyes-isolation`)에 산다.

---

### §1.11 `probe`

**직무.** 스레드만 읽는 계기 n대로 **전달 충실도**를 측정한다(D9). 진짜 이해 퀴즈가 아니라 "막힘 없이 읽히는가"의 측정이다.

| 항목 | 내용 |
|---|---|
| `id` | `probe` |
| `lane` | 계기 = Haiku × n(기본 5) / 채점자 = 별도 레인 |
| `inputs` | `50-gate/<variant>/thread.stripped.md`(계기 입력 — 주석 제거본), `20-design/blueprint.json`의 `transmission_targets[]`, `15-frozen/material-spec.v<N>.json`(채점자 전용), `50-gate/<variant>/annotation-index.json`(국소화 전용) |
| `outputs` | `60-probe/<variant>/probe-<i>.json`, `60-probe/<variant>/score.json` |
| `may_read` | 계기 = 스레드 텍스트만 / 채점자 = 동결본 + 프로브 응답 + `annotation-index.json` |
| `must_not_read` | **계기**: `15-frozen/**`, `20-design/**`, `00-source/**`, `40-compose/**`(주석층 포함), 다른 계기의 응답 / **채점자**: `50-gate/<variant>/l1.json`·`l2.md`(게이트 판정 오염 방지) |

**계기와 채점자의 분리가 계약이다.** 채점은 Haiku가 하지 않는다(D9). 계기는 오직 두 산출만 낸다 — ① 핵심 주장 3문장 재서술(프로브 A) ② 표적 질문 답변(프로브 B). 자기보고(예: "이해했다/어려웠다")는 **금지**한다 — LLM 내성을 신뢰하지 않는다는 것이 헌장의 명시 판정이며, 행동 프로브만 쓴다(D9). 채점자는 동결 재료 명세를 정답지로 삼아 대조하고, 핵심 사실은 결정론 대조(정규화 문자열·수치 일치)로 처리한다.

**프로브 B 질문의 유일한 파생원.** 질문은 블루프린트의 `transmission_targets`(재료 ID 목록)에서만 파생한다(D9). 이것이 측정을 이해 퀴즈와 분리하는 장치다 — 스레드가 전달하려 하지 않은 사실을 물으면 그것은 스레드의 실패가 아니라 질문의 실패다.

**국소화.** 걸림 위치는 채점 결과 + 주석층 역참조로 특정한다(D9). `score.json`의 `per_target[].weakest_tweet`은 `annotation-index.json`을 역참조해 자동 지목되며, 사람이 고르지 않는다. 산출 형식과 판별력 교정 절차는 **§5 소관**이다.

**입력 텍스트에 관한 계약 주의.** `probe`는 `ship`보다 앞에 실행되지만 계기가 읽어야 하는 것은 **주석이 제거된 출하 후보 텍스트**다(계기가 `[M7]`을 보면 근거 표기가 힌트가 되어 측정이 무효화된다). 따라서 strip 함수는 `gate` 종료 시점에 실행된다(그 산출 중 `annotation-index.json`은 이미 `50-gate/<variant>/`에 놓인다).

**[ENG-확정] strip 산출물의 영속 경로.** 집필 시점에 실제 계약 누수가 발견되었다 — `70-ship/thread.md`는 CP2 승인 후에야 생기는데 `probe`·`critique`·`gate.final-eyes`는 그 이전에 같은 텍스트를 필요로 한다. 조립 단계에서 다음과 같이 확정했다(§9.0 E5).

- **`50-gate/<variant>/thread.stripped.md`를 신설**하고, strip을 `gate` 종료 산출로 승격한다. 변주마다 하나씩 존재한다.
- `ship`은 **승인된 변주의 그 파일을 `70-ship/thread.md`로 복사만** 한다 — 출하 단계에서 텍스트가 새로 생성되지 않는다는 뜻이며, 이것이 "게이트 후 무단 수정 봉쇄"(D8)를 경로 수준에서 보장한다.
- 파생 규율: `ship`의 종료 검사는 `70-ship/thread.md`와 승인 변주의 `thread.stripped.md`가 **바이트 동일**함을 확인한다. 불일치 = `halt`.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `probe.independence` | 각 `probe-<i>.json`이 서로 다른 세션에서 생성되었고 상호 참조가 없음 |
| `probe.input-clean` | 계기에 투입된 텍스트에 주석 태그·프런트매터·슬롯 헤더가 없음(정규식 부재 확인) |
| `probe.no-self-report` | 프로브 응답 스키마에 자기평가 필드가 없음(D9) |
| `probe.target-coverage` | `score.json`의 `per_target[]`이 블루프린트 `transmission_targets[]` 전건을 덮음 |
| `probe.grader-separation` | 채점 산출의 생성 레인 id가 계기 레인 id와 다름 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| `probe.input-clean` 실패(주석 유출) | `halt` — 측정 무효 |
| 계기 일부 응답 실패 | `retry(1)` → n ≥ 3 확보되면 진행, 미달이면 `escalate` |
| `probe.grader-separation` 실패 | `halt` |
| `delivery_fidelity`가 낮게 나옴 | **실패가 아니다.** 계기는 거부권이 없다(D7·D9). 결과는 CP2에 첨부되고 판정은 Owner가 한다 |
| 판별력 교정에서 golden ≈ 변조 | `escalate` — 프로브 재설계 신호(D9) |

---

### §1.12 `critique`

**직무.** Fable 소견 — 훅 조응·안도감 착지·도슨트 보이스에 대한 비평 메모를 쓴다. 계기 데이터를 반영한다(D9).

| 항목 | 내용 |
|---|---|
| `id` | `critique` |
| `lane` | Fable |
| `inputs` | 출하 후보 스레드 텍스트, `60-probe/<variant>/score.json`, `20-design/blueprint.json`, `15-frozen/material-spec.v<N>.json` |
| `outputs` | `65-critique/<variant>/memo.md` |
| `may_read` | 위 `inputs`, `ledgers/anchors/**`, `docs/CHARTER.md` |
| `must_not_read` | `00-source/**`, `50-gate/<variant>/revisions/**`(수정 이력), `40-compose/<other-variant>/**` |

**거부권이 없다.** 소견은 자문이다(D7). 메모가 아무리 부정적이어도 스테이지는 통과하며, 메모는 CP2 표면에 첨부되어 Owner 재정의 재료가 된다. **점수 발행 금지**가 여기에도 적용된다(D8·D15).

**L2 메모와 소견의 차이(계약상 구분).**

| | `50-gate/<variant>/l2.md` (L2) | `65-critique/<variant>/memo.md` (소견) |
|---|---|---|
| 주체 | 게이트 심급 | 자문 3역 중 Fable(D9) |
| 입력 | 초안 + 동결 재료 | 초안 + 동결 재료 + **계기 데이터** |
| 관점 | 전역 판단(D8) | 훅 조응·안도감 착지·도슨트 보이스(D9) |
| 후속 | 메모 1회 → 펜 자유 리비전 1회(위상 봉쇄) | 후속 리비전 없음. CP2 첨부로 종결 |

수정 이력을 읽지 않는 이유는 최종 심급과 같다 — 소견이 "여기까지 오느라 고생했다"를 반영하기 시작하면 자문의 가치가 사라진다(D15).

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `critique.no-score` | 메모에 점수·등급 패턴 부재 |
| `critique.probe-reflected` | 메모가 `score.json`의 최약 표적 최소 1건을 명시적으로 언급 |
| `critique.no-history` | 레인 입력 목록에 `revisions/`가 없음 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| `critique.no-score` 실패 | `retry(1)` → `halt` |
| `critique.probe-reflected` 실패 | `retry(1)` — 계기 데이터 반영은 D9의 명시 요구 |
| 레인 실패 | `retry(1)` → 소견 결번으로 CP2 진행(자문이므로 파이프라인을 막지 않는다) |

---

### §1.13 ★CP2 — `ship_approval`

**부착 위치.** `critique` 스테이지의 `owner_checkpoint`(실행 순서상 `gate.final-eyes` 재진입 이후). 통과 봉투가 있어야 `ship`이 진입한다.

```yaml
owner_checkpoint:
  id: ship_approval
  surfaces:
    - <출하 후보 스레드 텍스트: 변주별 전량>
    - 30-figures/selection.json          # 변주별 도면 배치
    - 50-gate/<variant>/l1.json          # flags[] — 암시적 투자 조언 등, 판정자 = Owner (D8)
    - 50-gate/<variant>/l2.md
    - 60-probe/<variant>/score.json      # 전달 충실도 + 최약 지점
    - 65-critique/<variant>/memo.md
    - 50-gate/<variant>/verdict.json     # final_eyes 포함
  confirm_file: 70-ship/checkpoint2.md
  question: >
    ① 어느 변주를 출하하는가(또는 전량 보류인가).
    ② 첨부된 flag(암시적 투자 조언 등)를 수용 가능하다고 판정하는가.
    ③ 도면 선택을 그대로 두는가, 바꾸는가.
```

**이 단계가 유일한 구속력 지점이다.** 게이트의 거부권은 "정답이 있는 것"에만 미치고(D7), 변주 선택과 출하 승인은 Owner 재정 단독 관할이다(D9). L1이 올린 의미 수준 플래그(암시적 투자 조언)는 **거부권 없는 플래그**로 여기에 첨부되며 판정 적격자는 Owner다(D8·D3).

**승인 봉투(`70-ship/checkpoint2.md`) 유효 요건(재량).**

| 필드 | 값 |
|---|---|
| `status` | `approved` \| `held` |
| `by` | `owner` |
| `selected_variant` | `v1` \| `v2` \| `v3` (approved인 경우 필수) |
| `flags_adjudicated` | 첨부된 각 `flag.id`에 대한 `accept` \| `reject` |
| `figure_overrides` | 도면 변경이 있을 경우 자산 ID 목록 |
| `spec_version` / `spec_digest` | 승인 시점 동결본 |
| `date` | 실제 날짜 |

**이중 기입(D10).** Owner의 선택 1회는 `ledgers/tournament.jsonl`(모델 토너먼트 표)과 취향 데이터(보이스 앵커 후보 + 결함 카탈로그 사료) 양쪽에 기입된다. 기입 주체는 `ship`이며, 앵커 등재는 잠정 가중치 입장이고 결함 카탈로그 등재는 Owner 재정으로만 확정된다(D7·D13·D15).

---

### §1.14 `ship`

**직무.** 승인된 변주를 출하 패키지로 파생한다. 출하본은 **주석 strip 파생물**이며, 게이트 통과 후 무단 수정을 봉쇄한다(D8).

| 항목 | 내용 |
|---|---|
| `id` | `ship` |
| `lane` | 도구 실행(비-LLM) |
| `inputs` | `70-ship/checkpoint2.md`, 승인 변주의 `40-compose/<variant>/thread.annotated.md`, `30-figures/assets/`, `30-figures/selection.json` |
| `outputs` | `70-ship/thread.md`, `70-ship/thread.json`, `70-ship/images/` |
| `may_read` | 위 `inputs`, `50-gate/<variant>/**`, `60-probe/<variant>/**`, `65-critique/<variant>/**` |
| `must_not_read` | `00-source/**` |
| 원장 기입 | `ledgers/tournament.jsonl`(선택 기입), `ledgers/anchors/`(잠정 가중치 입장), `ledgers/corrections.md`(도면 override 사유) |

**strip은 결정론 파생이다.** 출하본은 사람이 다시 쓰지 않는다 — 주석층·프런트매터·슬롯 헤더를 기계 규칙으로 제거한 결과가 그대로 출하본이다. strip 문법(정규식·헤더 처리·이스케이프 복원·빈 줄 정규화)과 **무손실 round-trip 검사**는 **§3 소관**이며 본 절에서 반복하지 않는다.

**무단 수정 봉쇄의 메커니즘.** 출하본이 승인 초안의 결정론 함수이므로, 출하본을 손대면 초안과의 round-trip이 깨진다. 즉 "게이트 통과 후 조용히 문장 하나 고치기"가 기계적으로 탐지된다(D8). `ship`은 출하 시점의 초안 다이제스트를 `thread.json`에 기록해 이 대조의 기준점을 남긴다.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `ship.approval-valid` | `checkpoint2.md`의 `status: approved`, `selected_variant` 존재, `spec_digest` 일치 |
| `ship.strip-roundtrip` | strip 결과가 원본에서 태그·헤더·프런트매터만 뺀 것과 **바이트 동일**(§3) |
| `ship.image-resolve` | `70-ship/images/`의 모든 파일이 `assets/`의 승인된 포인터에서 유래, 포스트당 ≤ 4 |
| `ship.flags-adjudicated` | 첨부된 모든 `flag.id`에 Owner 판정이 기록됨 |
| `ship.ledger-write` | `tournament.jsonl`에 이번 선택이 1행 추가되고 스키마 검증 통과 |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| 승인 봉투 부재·무효 | `halt` |
| `ship.strip-roundtrip` 실패 | `halt` — 무손실이 깨진 출하본은 D8 봉쇄를 무력화한다 |
| 도면 포인터 미해소 | `retry(1)` → `halt` |
| 미판정 flag 존재 | `halt` — CP2로 되돌아간다 |
| Owner가 `held` 판정 | `halt`(정상 종료) — 런은 열린 채 보관 |

---

### §1.15 `feedback`

**직무.** 게시 후 72h 시점의 실측을 두 장부에 입력한다(D13). v1 지표 수집은 **수동 입력**이다.

| 항목 | 내용 |
|---|---|
| `id` | `feedback` |
| `lane` | 도구 실행 + Owner 수동 입력 |
| `inputs` | Owner 수동 입력값(72h 스냅샷), `70-ship/thread.json`, `ledgers/metrics.jsonl`(최근 N개) |
| `outputs` | `90-feedback/metrics-72h.json`, `90-feedback/retro.md` |
| 원장 기입 | `ledgers/metrics.jsonl`(append), `ledgers/anchors/`(가중치 조정 + fade 제안), `ledgers/regression/`(등재 **제안**만) |
| `may_read` | `70-ship/**`, `ledgers/**`, `60-probe/<variant>/score.json` |
| `must_not_read` | `00-source/**`, `10-read/**` |

**입력 계약.**

| 필드 | 형태 | 규율 |
|---|---|---|
| `posted_at` | 게시 시각 | |
| `snapshot_at` | `posted_at + 72h` | 시점 고정(D13) |
| `raw_metrics` | Owner가 X에서 옮겨 적은 원시값 | **원시 조회수는 가중치 계산에 쓰지 않는다**(팔로워 규모 교란, D13) |
| `relative_percentile` | 최근 N개 이동 중앙값 대비 백분위 | 앵커 가중치의 유일한 입력 |
| `taste_market_divergence` | Owner 선택 변주가 시장에서 죽은 경우 표시 | 취향-시장 괴리 기록(D13) |

**산출 계약.**

| 산출 | 내용 | 확정 주체 |
|---|---|---|
| `metrics-72h.json` | 위 입력의 정규화 기록 | `feedback` |
| `retro.md` | 런 회고(무엇이 걸렸나·어느 재료가 전달에 실패했나) | `feedback` |
| 앵커 가중치 조정 | 상대 성과 기반. 표본 < 10이면 전원 잔류(콜드 스타트) | `feedback`(자동) |
| fade-out | **자동 제안까지만.** 배치 리뷰에서 Owner 재정으로 확정 | **Owner**(D13) |
| 회귀 원장 등재 | **제안까지만.** 인기로 물갈이하지 않음 | **Owner 재정**(D13·D15) |
| 계기 유효성 점검 | 계기 점수 ↔ 실반응 상관. 무상관이면 프로브 재설계 신호 | 배치 단위(D13) |

두 장부의 운영 규칙 상세(파일 형식·배치 리뷰 절차·fade 임계)는 §7·§8 소관이며, 본 절은 **입력·산출 계약**까지만 정한다.

**종료 전 검사.**

| 검사 id | 판정 기준 |
|---|---|
| `feedback.window` | `snapshot_at - posted_at`이 72h ± 허용 오차 내 |
| `feedback.no-raw-weighting` | 앵커 가중치 계산 입력에 `raw_metrics`가 쓰이지 않음(D13) |
| `feedback.fade-proposal-only` | fade 산출이 `proposed` 상태이며 확정 상태가 아님 |
| `feedback.ledger-append` | `metrics.jsonl`이 추가 전용으로 갱신됨(기존 행 변경 0) |

**실패 처리.**

| 조건 | 조치 |
|---|---|
| 72h 시점 미도래 | 정상 대기(실패 아님). 런은 `ship` 후 닫히고 `feedback`은 재개 실행 |
| Owner 입력 누락 | `halt`(대기) — 추정값 생성 금지 |
| `feedback.no-raw-weighting` 실패 | `halt` — D13 위반 |
| fade가 자동 확정됨 | `halt` — D13 명시 위반 |

> [OPEN] `feedback`이 런 파이프라인의 스테이지인지(런이 72h 열린 채 대기) 별도 배치 작업인지 헌장은 규정하지 않는다.
> 추천: 런은 `ship`에서 닫고 `feedback`은 `pipeline.yaml`의 재개(resume) 진입점으로 둔다. 72h 대기 상태의 런이 누적되면 오케스트레이터 상태 관리가 복잡해진다.

---

### §1.16 실패 처리 종합표

발주가 지목한 7개 실패 양식의 처리 위치를 한 표로 모은다.

| # | 실패 양식 | 탐지 위치 | 조치 | 근거 |
|---|---|---|---|---|
| 1 | 원천 다이제스트 불일치 | `read`(진입), `freeze.digest-match` | `halt` — 원천이 바뀐 런은 폐기 | D6 규율 ③ |
| 2 | 접지 검사 실패 | `read.pointer-resolve`, `read.coverage` | `retry(1)` → `escalate` | D5·D6 |
| 3 | 재독해 수렴 미달 | `read.convergence` | `retry(1)` → `escalate`(절차 신호) | D6 규율 ③ |
| 4 | drop 신호 발생(2단) | `read` 조기(청구항 분해 직후) / 최종(포지셔닝 후) | 즉시 `escalate`, 하류 정지 | D4 |
| 5 | 재료 반려(단방향) | `compose` → `material-defect.md` | `reject-upstream`(→ `read`) → `spec_version` + 1 → `freeze` → 하류 재실행. 펜은 재료를 고치지 못함 | D6 규율 ② |
| 6 | 게이트 국소 수정 캡 3회 초과 | `gate` 루프 카운터 | `escalate` — 상류 결함 신호, 대개 재료 반려행 | D8 |
| 7 | 변주 전멸 | `gate`(전 변주 캡 초과 또는 최종 심급 탈락) | `escalate` — 복구 경로는 Owner 재정(§1.10 `[OPEN]`) | D8·D10 |

**조치 어휘의 의미(고정).**

| 조치 | 뜻 |
|---|---|
| `retry(n)` | 같은 스테이지를 최대 n회 재실행. 입력 불변 |
| `escalate` | 파이프라인 정지 + Owner 상신. 자동 복구를 시도하지 않는다 |
| `halt` | 파이프라인 정지 + 런 상태 무효. 재개하려면 원인 제거가 선행 |
| `reject-upstream` | 상류 스테이지로 반려. 반려서가 유일한 통신 수단이며 방향은 단방향 |

---

### §1.17 스테이지 × 산출물 교차표

계약 누수 점검용이다. **W** = 쓰기, **R** = 읽기, **X** = 명시적 금지(`must_not_read`), 빈칸 = 무관.

> **감수 반영(2026-08-17, sol BLOCKER #8).** 초판은 이 표에서 `run.yaml`의 쓰기 권한을 `source`·`design`·`compose`(펜) 셋에 주었는데, 이는 §7.4가 선언한 불변식("한 경로에는 쓰기 소유자가 정확히 하나")을 정면으로 위반하고, 더 나쁘게는 **펜이 `numeric_whitelist`(게이트 면제 목록)를 스스로 편집할 수 있게** 만들었다 — 심판 조건을 피심판자가 고치는 구조다(D6 규율 ②·D8 위반). 쓰기 소유자를 `source` 단독으로 고정하고, 런 진행 중의 상태 필드 갱신은 러너만 수행한다. 화이트리스트 추기는 §4.4의 절차(CP2 전량 인쇄)를 따르며 펜의 손이 닿지 않는다.

| 산출물 | `source` | `read` | `freeze` | `design` | `figures` | `compose` | `gate` | `probe` | `critique` | `ship` | `feedback` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `run.yaml` | **W** | R | R | R | R | R | R | R | R | R | R |
| `00-source/patent.md` | **W** | R | | **X** | **X**(select) | **X** | **X** | **X** | **X** | **X** | **X** |
| `00-source/patent.sha256` | **W** | R | R | | | | | | | | |
| `00-source/figures-raw/` | **W** | R | | | R(prepare) | | | | | | |
| `10-read/material-spec.json` | | **W** | R | **X** | | **X** | | | | | **X** |
| `10-read/material-spec.md` | | **W** | R | | | | | | | | |
| `10-read/claim-trees/`, `grounding.md`, `positioning.md` | | **W** | R | | | | | | | | |
| `10-read/drop-signal.md` | | **W** | | | | | | | | | |
| `10-read/convergence.json` | | **W** | R | | | | | | | | |
| `15-frozen/material-spec.v<N>.json` | | | **W** | R | R | R | R | R(채점자) / **X**(계기) | R | | |
| `15-frozen/approval-v<N>.md` | | | **W**(오케스트레이터) | | | | | | | R | |
| `20-design/blueprint.json` | | **X** | | **W** | R(select) / **X**(prepare) | R | R | R(표적) / **X**(계기) | R | | |
| `20-design/blueprint.md` | | | | **W** | | | | | | | |
| `30-figures/assets/` + `manifest.json` | | | | R | **W**(prepare) | R | | | | R | |
| `30-figures/selection.json` | | | | | **W**(select) | R | R | | | R | |
| `40-compose/<v>/thread.annotated.md` | | | | | | **W** | R | **X**(계기) | | R | |
| `40-compose/<v>/material-defect.md` | | R | | | | **W** | | | | | |
| `50-gate/<v>/l0.json`,`l1.json`,`verdict.json` | | | | | | | **W** | **X**(채점자) | | R | |
| `50-gate/<v>/l2.md` | | | | | | R(리비전 1회) | **W** | **X** | **X**(final-eyes) | R | |
| `50-gate/<v>/annotation-index.json` | | | | | | | **W** | R(채점자, 국소화) | | | |
| `50-gate/<v>/revisions/r<n>/` | | | | | | **W**(결과) | **W**(지시) | | **X** | | |
| `60-probe/<v>/probe-<i>.json`, `score.json` | | | | | | | **X**(final-eyes) | **W** | R | R | R |
| `65-critique/<v>/memo.md` | | **X** | | | | | **X**(final-eyes) | | **W** | R | |
| `70-ship/checkpoint2.md` | | | | | | | | | | R(**W**=오케스트레이터) | R |
| `70-ship/thread.md`, `thread.json`, `images/` | | | | | | | | | | **W** | R |
| `90-feedback/metrics-72h.json`, `retro.md` | | | | | | | | | | | **W** |
| `ledgers/tournament.jsonl` | | | | | | | | | | **W** | R |
| `ledgers/anchors/` | | | | R | | | | | R | **W**(잠정 입장) | **W**(조정·fade 제안) |
| `ledgers/regression/` | | | | | | | R | R(교정) | | | **W**(제안만) |
| `ledgers/metrics.jsonl` | | | | | | | | | | | **W** |
| `ledgers/corrections.md` | | | | | **W**(select) | | | | | **W**(override) | |
| `contracts/lexicon/forbidden.yaml` | | | | | | **X** | R | | | | |
| `contracts/lexicon/defect-catalog.yaml` | | | | | | **X** | R | | | | |

**교차표에서 읽히는 계약 성질 4개.**

1. **`00-source/`의 독자는 `read`와 `figures.prepare` 둘뿐이다.** 나머지는 전부 명시적 금지다 — 주방 분리가 한 행으로 보인다(D6).
2. **`10-read/`(작업본)는 `freeze`에서 끊긴다.** 하류 전체는 `15-frozen/`만 읽는다(C7).
3. **`ledgers/`에 쓰는 스테이지는 `figures`·`ship`·`feedback` 셋뿐이고, 확정 권한은 전부 Owner에 있다**(D13·D15). `gate`·`probe`는 회귀 원장을 읽기만 한다.
4. **`gate.final-eyes`의 금지 열이 `l2.md`·`revisions/`·`65-critique/`·`60-probe/`에 걸쳐 있다** — 격리가 파일 단위로 표현된다(D8·D15).

> [OPEN] 승인 봉투(`15-frozen/approval-v<N>.md`, `70-ship/checkpoint2.md`)를 Owner가 직접 쓰는지 오케스트레이터가 Owner 응답을 받아 대필하는지, 그리고 무인 실행 플래그(구 PAW의 `--yes`)를 두는지 헌장은 규정하지 않는다.
> 추천: **오케스트레이터 대필 + 무인 플래그 없음.** v1은 체크포인트 2개짜리 유인 운영이고, D9가 재정을 Owner 단독 권한으로 못박았으므로 무인 우회로를 만들면 그 조항이 비게 된다.

---

## §2 재료 명세 스키마 v0

### §2.1 지위

재료 명세 스키마는 **엔진 내부 자료구조가 아니라 프로젝트 간 계약이다**(D14). patent-historian은 "재료 명세 N개를 모아 교차 분석"으로 정의되므로, 이 스키마가 흔들리면 historian의 정의가 흔들린다. 따라서 이 절의 변경 비용은 다른 절보다 한 자릿수 높다고 간주한다.

**정본 위치는 한 곳뿐이다.**

| 항목 | 값 |
|---|---|
| 스키마 정본 | `reader/schemas/material-spec.schema.json` |
| 사본 허용 | 없음. `contracts/schemas/`는 docent 전용 스키마만 둔다(§1 참조) |
| 이식 단위 | `reader/` 디렉터리 전체(스냅샷 + `PORTED-FROM.md` 원천 커밋 핀, D14) |
| 버전 파일 | `reader/READER-VERSION`(semver 한 줄) |

이식 단위가 자기 계약을 들고 간다. historian이 `reader/`를 스냅샷하면 스키마·검사 유틸·절차 문서가 한 덩어리로 따라가므로, 두 리포가 같은 스키마를 각자 편집해 갈라지는 실패 모드가 원천 봉쇄된다.

**버전 정책 (2축)**

| 축 | 표기 | 위치 | 증가 조건 |
|---|---|---|---|
| 계약 라인 | `schema: "material-spec/v0"` | 인스턴스 최상위 필드 | 하위호환을 깨는 변경 = 새 라인(`.../v1`). v0 소비자는 v1 인스턴스를 **거부**한다 |
| 구현 버전 | `reader_version: "0.1.0"` | 인스턴스 필드 + `READER-VERSION` | 필드 추가·검사 강화 = minor, 버그 수정 = patch, 계약 라인 변경 동반 = major |
| 인스턴스 버전 | `spec_version: 1` | 인스턴스 필드 | 동결 스탬프. 개정 시 +1 단조 증가(런 내부 값이며 계약과 무관) |

하위호환을 깨는 변경의 정의(계약 라인 major에 해당): 필드 삭제·의미 변경, 필수 필드 추가, enum 값 삭제, ID 문법 변경, 결정론 검사 판정 기준의 강화. **enum 값 추가와 선택 필드 추가는 minor**로 취급하되, 소비자가 `additionalProperties: false`로 닫혀 있으므로 소비자 쪽 reader_version이 낮으면 검증 실패한다 — 그래서 다음 규율이 있다.

**상호 체크 (D14)**: 독해층을 수정하거나 주로 사용하는 작업에서는 상대 리포의 `READER-VERSION`을 확인한다. 어긋남을 발견하면 **자동 동기화 금지, Owner 상신**. 도구는 `tools/check_reader_version.py`(§5 이하 모듈 로드맵 참조), 규율의 명문화 위치는 리포 `CLAUDE.md`다.

**과적합 금지 원칙**. 이 스키마는 v1 소재(Owner 지정 특허 1건)의 문맥에 맞춰지면 안 된다. 설계상 지킨 것:

1. `items[].kind` enum은 **기술 도메인에 중립**이다(구성요소·접지·사실·함의·포지셔닝·도면 주석). 재료·반도체·기계 어느 쪽에서도 같은 6종으로 분해된다.
2. 도메인 어휘를 필드명에 넣지 않는다. 값은 자유 텍스트, 구조는 도메인 무관.
3. `implication`에 투자 관련 필드를 두지 않는다(D3의 구조적 방어). 스키마가 닫혀 있으므로 "그냥 필드 하나 추가"로 우회할 수 없다.
4. 항목 ID는 런 내부 순번이며 **append-only**다(§2.4). 개정이 ID를 재사용하지 않으므로, historian이 시점 t에 수집한 `M7`은 시점 t+1에도 같은 대상이거나 명시적으로 `retracted`/`superseded`다 — 결코 다른 대상이 되지 않는다. 이것이 프로젝트 경계를 넘는 ID 안정성의 전부다.

> [OPEN] 항목 ID의 전역 참조자. 런 내부에서 `M7`은 유일하지만 historian은 N개 런을 섞으므로 전역 키가 필요하다. 추천: 정본 스키마는 건드리지 않고, 전역 참조자를 `<run_id>#<item_id>`(예: `openai-us20260147854a1-cim-fp#M7`)로 **스펙 문언에만** 규정하고 historian 인덱스가 이 규칙으로 조립하게 한다. v0 인스턴스에 전역 ID 필드를 추가하는 안은 계약을 넓히므로 비추천.

> [OPEN] `label_kr`·`statement_kr`의 언어 결속. 계약 필드명이 KR 전용으로 고정되어 있는데 historian은 전문가·유료 채널이라 EN 소비가 있을 수 있다. 추천: v0는 필드명 고정(브리프 준수)으로 두고, EN이 실제로 필요해지는 시점에 `label_en`을 **선택 필드**로 추가(minor)한다. 지금 이름을 바꾸면 계약 major다.

### §2.2 최상위 구조

정본 기계 산출 = `10-read/material-spec.json`(작업본) / `15-frozen/material-spec.v<N>.json`(동결본). 인간 판독본 `material-spec.md`(KR)는 렌더 파생물이며 계약이 아니다(§1 참조).

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `schema` | string(const `"material-spec/v0"`) | ✔ | 계약 라인 식별자. 소비자는 이 값이 다르면 즉시 거부 |
| `reader_version` | string(semver) | ✔ | 산출 시점의 독해층 버전 |
| `spec_version` | integer ≥ 1 | ✔ | 동결 버전 스탬프. 개정 시 +1 |
| `status` | enum `draft`\|`frozen`\|`revised` | ✔ | 생애주기 상태(아래 상태기계) |
| `run_id` | string | ✔ | `<assignee-slug>-<pubnum>-<topic-slug>`(§1 참조) |
| `patent` | object | ✔ | 특허 식별·날짜·원천 다이제스트 |
| `claims` | object | ✔ | D5 ①② 산출. §2.3 |
| `figures` | array | ✔ | 도면 목록. §2.5. 도면이 없는 특허면 빈 배열 |
| `items` | array | ✔ | 인용 단위 `M<n>`. §2.4. 최소 1개 |
| `drop_signal` | object | ✔ | D4 2단 신호. `{ stage, verdict, reason }` |
| `provenance` | object | ✔ | `{ read_runs[], produced_at, engine_commit }` |

`patent` 하위:

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `number` | string | ✔ | 공개/등록번호. 숫자 전수 대조의 정답지에 포함됨(§4.4) |
| `title` | string | ✔ | 원문 제목 |
| `assignee` | string | ✔ | 출원인 |
| `dates.priority` / `.filing` / `.publication` | string(`YYYY-MM-DD`) | ✔ / ✔ / ✔ | 날짜 사실. 해석은 담지 않는다(§2.3) |
| `source_digest` | string(`sha256:<64hex>`) | ✔ | `source_path` 파일의 다이제스트. **인용 검증의 기준점** |
| `source_path` | string | ✔ | 통상 `00-source/patent.md` |

**불변식**

| # | 불변식 | 위반 시 |
|---|---|---|
| I1 | `sha256(source_path 파일) == source_digest` | 검사 4종 전부 무효. READ 즉시 중단 |
| I2 | `spec_version`은 같은 `run_id` 안에서 단조 증가하며 건너뛰지 않는다 | 동결 실패 |
| I3 | `status: "frozen"` 인스턴스는 **읽기 전용**이며 `15-frozen/` 밖에 존재하지 않는다 | 파이프라인 계약 위반(§5 이하 참조) |
| I4 | 하류 스테이지(DESIGN·COMPOSE·GATE·PROBE)는 동결본만 읽는다. 작업본 참조 금지 | 단방향 규율 위반(D6 규율 ②) |
| I5 | `items[].id`는 인스턴스 안에서 유일하다 | 스키마 검증 실패 |

**상태기계**

| from | to | 계기 |
|---|---|---|
| — | `draft` | READ 개시 |
| `draft` | `frozen` | 체크포인트 1 승인(D6) → `spec_version` 스탬프 + 동결본 사본 생성 |
| `frozen` | `revised` | 펜의 재료 반려서(`40-compose/<variant>/material-defect.md`) 수리 → READ 재개(D6 규율 ②) |
| `revised` | `frozen` | 재승인. `spec_version` +1 |

**펜은 재료를 수정할 권한이 없다**(D6 규율 ②). 반려는 문서로 올라가고, 개정은 READ가 한다. 스키마 차원의 집행은 I3(읽기 전용)과 I4(동결본만 읽기)이며, 도구 차원의 집행은 스테이지별 `may_read`/`must_not_read`다(§5 이하 참조).

### §2.3 claims — D5 ①②의 구현

```
claims
  independent[]        # 독립항별 별도 트리 (D5 ①)
    id, type, text_verbatim, elements[]
      element: id, text_verbatim, material_id, children[]   # 재귀
  dependents[]
    id, depends_on, additions[]
      addition: id, attaches_to, text_verbatim, material_id
  applicant_interest[]  # 독립항별 관심 신호 (D5 승계 재정 ①)
    claim, signal, material_id
```

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `independent[].id` | `^CL-[0-9]+$` | ✔ | 청구항 번호와 일치 |
| `independent[].type` | const `"independent"` | ✔ | 중복이지만 명시적으로 둔다(historian이 항목 단위로 잘라 쓸 때 자기기술적) |
| `independent[].text_verbatim` | string | ✔ | 청구항 전문. 원천 부분문자열 |
| `elements[].id` | `^CL-[0-9]+/e[0-9]+(/e[0-9]+)*$` | ✔ | 중첩 시 경로가 길어진다(`CL-1/e2/e1`) |
| `elements[].material_id` | `^M[0-9]+$` | ✔ | 반드시 `kind: "component"` 항목을 가리킨다 |
| `elements[].children[]` | element[] | ✔(빈 배열 허용) | 구성요소 내부 하위 한정 |
| `dependents[].depends_on` | `^CL-[0-9]+$` | ✔ | 다중 종속은 §2.3 말미 참조 |
| `additions[].id` | `^CL-[0-9]+/a[0-9]+$` | ✔ | 부가 한정 단위 |
| `additions[].attaches_to` | element id | ✔ | **골격 밑 층위 누적의 구현체** |
| `applicant_interest[].material_id` | `^M[0-9]+$` | ✔ | `kind: "implication"` 항목을 가리킨다(관심 신호는 해석이므로) |

**`attaches_to`의 역할.** D5 ①은 "종속항의 부가 한정은 골격 밑 층위로 누적한다"고 규정한다. 이 스키마는 종속항을 **독립항 트리 안에 물리적으로 병합하지 않고** `attaches_to` 포인터로 부착한다. 이유 셋:

1. 다중 종속(claim 7 = "claim 1 or 5의")이면 물리 병합은 트리를 복제해야 한다. 포인터는 복제하지 않는다.
2. `text_verbatim`의 바이트 정확 검사(§2.6)를 유지하려면 원문 조각이 편집 없이 남아야 한다. 병합은 문장을 접합하며 원문을 훼손한다.
3. 렌더(D5 ② 관계 트리 도식)는 포인터를 따라 **표시 시점에** 누적 트리를 조립하면 된다. 정본은 얇게, 도식은 파생물로.

`applicant_interest`가 **D5 승계 재정 ①("청구항 = 법적 권리범위가 아니라 출원인 관심 신호")의 스키마 상 거처**다. 청구항 트리는 사실(원문 조각)만 담고, "출원인이 무엇에 관심을 걸었는가"라는 해석은 별도 배열에 격리되며 그 서술 본체는 `implication` 항목에 산다. 해석과 사실을 같은 노드에 섞지 않는 것이 요점이다 — 게이트가 대조할 수 있는 것은 사실 쪽뿐이기 때문이다(D7).

**날짜 의미론이 사는 곳.** D5 승계 재정 ②는 "우선일 = 본격 연구개발 개시의 최후 하한선이며 서랍-속-정답(gotcha) 독법 금지"다. 이 규범은 스키마에 **상태로 저장되지 않는다.**

| 무엇 | 어디에 남는가 | 왜 |
|---|---|---|
| 날짜 사실 | `patent.dates.*` | 원천에 있는 문자열. 정답이 존재한다 |
| 날짜 기반 서술 | `implication` 항목(`basis: "spec"\|"background"` 등, `confidence: "inferred"`, `evidence_quotes[]` 필수) | 서술은 근거 인용을 달고 다녀야 한다 |
| 독법 규범 자체 | `reader/procedure/`의 절차 문서·프롬프트 | 산출물이 아니라 **생성 규율**이기 때문 |

`priority_interpretation` 같은 필드를 두지 않는다. 두면 그 필드가 규범의 준수를 자기 신고하게 되고, 자기 신고는 검증되지 않는다(§3.4와 같은 이유).

**관할권 구분(D7)** — 이 지점을 명시적으로 못 박는다.

| 술어 | 정답 존재? | 처분 |
|---|---|---|
| "본문의 날짜 문자열이 동결 재료에 있는가" | 있음(원천과의 관계) | **게이트** L0 `numeric.exhaustive` |
| "우선일을 `2024-11-05`로 적었는데 원천이 그런가" | 있음 | **게이트** |
| "이 서술이 gotcha 독법인가(출원인이 이미 다 알고 서랍에 넣어뒀다는 함의를 흘리는가)" | **없음** | **게이트 아님** — L2 자문 메모·Fable 소견(D9) |
| "우선일을 하한선으로 정확히 해석했는가" | 없음(해석의 질) | **게이트 아님** — 자문 |

금지 독법의 집행을 게이트에 넣고 싶은 충동이 생기는 자리다. 넣지 않는다. 판정에 정답이 없는 술어를 결정론 층에 올리면 게이트가 **문언 아닌 정신을 외삽**하기 시작하며, 그 순간 거부권의 신뢰도가 무너진다(D7). 예외는 하나뿐이다: 특정 **문언**이 반복적으로 나쁘다고 판명되어 Owner 재정으로 `contracts/lexicon/forbidden.yaml` 또는 결함 카탈로그에 등재되면, 그 **문언만** L0가 집행한다(알려진 나쁨의 차단이며, 통과 ≠ 좋음).

**다중 종속 표기.** `depends_on`은 단수 문자열이다. 다중 종속 청구항은 `depends_on`에 주 종속 대상을 적고, 나머지 부착점은 각 `addition.attaches_to`로 표현한다(부가 한정 단위가 결국 어느 element에 붙는지가 실질이므로). 종속의 종속(claim 7 → claim 5 → claim 1)은 `depends_on: "CL-5"`로 적고 `attaches_to`는 최종적으로 독립항 element를 가리킨다 — 즉 `attaches_to`의 값 공간은 **항상 element id**다.

### §2.4 items[] — 인용 단위

`items[]`는 주석층이 인용하는 **유일한** 대상이다(D6 규율 ①). 본문의 모든 기술 주장은 `M<n>`으로 역참조되어야 하고, 역참조가 해소되지 않으면 L0 결함이다(§4.4 `citation.resolve`).

**공통 필드**

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `id` | `^M[0-9]+$` | ✔ | 런 내 순번. append-only |
| `kind` | enum(6종) | ✔ | `component`\|`grounding`\|`fact`\|`implication`\|`positioning`\|`figure_note` |
| `status` | enum `active`\|`retracted`\|`superseded` | ✔ | 생애 상태 |
| `superseded_by` | `^M[0-9]+$` \| null | ✔ | `status == "superseded"`일 때만 non-null |

**★ ID 규율 (고정)**

1. `M<n>`은 런 내 순번이며 **추가 전용(append-only)**이다. 다음 항목의 번호는 항상 `max(n)+1`이다.
2. **재사용·재번호 금지.** 개정에서 항목을 지우지 않는다.
3. 폐기는 `status: "retracted"`(근거가 잘못이었음 — 대체물 없음), 교체는 `status: "superseded"` + `superseded_by`(같은 대상에 대한 더 나은 항목이 생김)로 표시한다.
4. 폐기·교체 **사유**는 항목에 적지 않고 개정 봉투 `15-frozen/approval-v<N>.md`에 기록한다(스키마가 닫혀 있고, 사유는 계약 대상이 아니다).

**왜 이 규율이 필요한가.** 두 가지 실패를 막는다.

- **인용 해소의 시간 안정성.** 주석본(`thread.annotated.md`)은 동결본 `spec_version: N`을 인용한다. 재료가 N+1로 개정되었을 때 ID가 재사용되었다면, 같은 `[M12]` 태그가 **다른 대상**을 가리키게 되고 인용은 조용히 거짓이 된다. 조용한 거짓은 게이트가 검출할 수 없다(형식상 해소되기 때문). append-only는 이 실패를 **해소 실패**로 바꿔 시끄럽게 만든다.
- **개정된 재료를 인용한 문장의 지목 가능성.** 재료가 바뀌면 그 재료를 인용한 문장이 어디였는지 정확히 짚어야 국소 수정 지시가 나간다(D8 루프 위상). 지워진 ID는 짚을 수 없다. `retracted` 항목이 남아 있으면 `citation.resolve`가 "T4/S2가 `retracted` M12를 인용" 형태로 **좌표를 동반한** 결함을 낸다.
- 부수 효과: historian이 여러 시점의 명세를 모아도 ID 충돌·의미 표류가 생기지 않는다(§2.1의 과적합 금지 4항).

**kind별 필드**

| kind | 필드 | 비고 |
|---|---|---|
| `component` | `claim_ref`(element id 또는 addition id), `label_kr`, `text_verbatim` | 청구항 구성요소 1개 |
| `grounding` | `component`(component 항목의 `M<n>`), `spec_refs[]` = `{locator, quote, span}`, `figure_refs[]` = `{figure, numerals[], caption_quote}` | **D5 ③ 3중 접지의 한 행** |
| `fact` | `label_kr`, `value_raw`, `value_normalized`, `unit`, `source` = `{locator, quote}` | **§4.4 숫자 전수 대조의 정답지**. `label_kr`은 §9.0 E2로 v0 확정 전에 추가됨 |
| `implication` | `statement_kr`, `basis`(`claim`\|`spec`\|`background`\|`effects`), `derived_from[]`, `evidence_quotes[]`, `confidence`(`stated`\|`inferred`) | 투자 관련 필드 없음(D3) |
| `positioning` | `background_problem`, `asserted_effect`, `delta`, `quotes[]` | D5 ⑤ |
| `figure_note` | `figure`(FIG id), `what_it_shows_kr`, `numerals[]` | |

보조 규정:

- `grounding.component`는 **`component` kind 항목의 ID**를 가리킨다(청구항 element id가 아니다). element → `material_id` → component 항목 → grounding의 사슬로 접지가 성립하며, 커버리지 검사(§2.6)는 이 사슬을 역방향으로 센다.
- `spec_refs[].locator`는 원천의 사람이 읽는 좌표(`[0042]`, `col. 7 l. 12` 등), `span`은 `{start, end}` 바이트 오프셋(`source_path` 기준)이다. `quote`가 정본이고 `span`은 검사 실패 시 위치 지목용 힌트다 — 둘이 어긋나면 `quote`가 이긴다.
- `figure_refs[].figure`는 `figures[].id`로 해소되어야 한다.
- `implication.evidence_quotes[]`는 `confidence`와 무관하게 **최소 1개** 필수다. `stated`(명세서가 그렇게 말함)와 `inferred`(독해가 끌어냄)의 차이는 인용의 유무가 아니라 인용과 서술 사이 거리의 크기다.
- `implication`에는 투자 관련 필드를 두지 않는다. 스키마는 `additionalProperties: false`이므로 이 방어는 **문서 규범이 아니라 검증기 실패**로 집행된다(D3).

**개정 예시** — M5의 값을 오독했음이 재독해에서 드러난 경우:

```json
{
  "items": [
    {
      "id": "M5",
      "kind": "fact",
      "status": "superseded",
      "superseded_by": "M9",
      "label_kr": "유로 수력직경",
      "value_raw": "0.8 mm",
      "value_normalized": "0.8",
      "unit": "mm",
      "source": { "locator": "claim 5", "quote": "a hydraulic diameter of 0.8 mm" }
    },
    {
      "id": "M9",
      "kind": "fact",
      "status": "active",
      "superseded_by": null,
      "label_kr": "유로 수력직경(정정값)",
      "value_raw": "0.08 mm",
      "value_normalized": "0.08",
      "unit": "mm",
      "source": { "locator": "[0051]", "quote": "the hydraulic diameter is 0.08 mm" }
    }
  ]
}
```

M5는 남고 M9가 추가된다. `[M5]`를 인용했던 문장은 `citation.resolve`가 지목하며(§4.4), 수정 지시는 "T4/S2를 M9 내용으로 재서술"이 된다.

> [OPEN] `fact`에 의미 라벨이 없다. 고정 필드는 값·정규화값·단위·출처뿐이라 `[M5]`를 인용한 문장이 "그 숫자가 무엇의 숫자인지"를 재료에서 확인할 방법이 `source.quote` 문맥밖에 없다. 추천: `fact`에 `label_kr`(필수) 추가 — 계약 라인은 그대로 두고 v0 확정 전에 넣는 편이 싸다. 지금 결정하지 않으면 M1 구현 후 major 비용이 된다.

### §2.5 figures[]

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `id` | `^FIG-[A-Za-z0-9-]+$` | ✔ | 원천 표기(`FIG. 3` → `FIG-3`) |
| `numerals` | string[] | ✔ | 도면부호. **문자열**로 둔다(`"210a"` 같은 값이 있고, 숫자 대조 대상이 아니기 때문) |
| `caption_quote` | string | ✔ | 원천 캡션의 바이트 정확 인용 |
| `raw_path` | string | ✔ | `00-source/figures-raw/...` |
| `asset_path` | string \| null | ✔ | 편집 자산 경로. **READ 시점에는 null이 정상** |

`asset_path`가 nullable인 이유: 재료 명세는 체크포인트 1에서 동결되고 도면 편집(FIGURES 스테이지)은 그 뒤에 온다(D6 파이프라인). 동결 시점에 존재하지 않는 경로를 필수로 두면 READ가 거짓 경로를 쓰게 된다. **자산층의 정본은 `30-figures/assets/manifest.json`**이고(D12 전량 선편집·자산층 보존), `figures[].asset_path`는 편집이 끝난 뒤 채워질 수 있는 편의 사본이다. 포인터 해소 검사(§2.6)는 `asset_path`를 대상으로 삼지 않는다 — 구조 ID만 본다.

`numerals`는 숫자 전수 대조(§4.4)의 정답지에 **포함하지 않는다**. 도면부호는 본문에 등장할 이유가 없고, 등장한다면 그것 자체가 도슨트 실패다(D2 독자상). 본문에 도면부호를 쓰고 싶으면 `fact` 항목으로 별도 등재해야 한다.

### §2.6 결정론 검사 4종

D6 규율 ③의 구현이다. 규율 원문이 이 절의 헌법이다: **"독해 자체는 LLM 판단을 필요로 한다. 따라서 결정론은 절차 고정 + 산출물 형식 구조화 + 검증 기계화에 산다."** 다시 말해 이 4종은 "독해가 옳은가"를 판정하지 않는다. 판정하는 것은 **"독해가 자기 산출물에 대해 거짓말을 하지 않았는가"**뿐이다. 4종을 전부 통과한 명세도 여전히 얕거나 초점이 틀릴 수 있으며, 그 판단은 체크포인트 1의 Owner 몫이다(D6 — 재료 검토가 Owner 이해층을 겸한다).

실행 위치는 READ 스테이지의 `checks_before_exit`이며(§5 이하 참조), 산출은 `10-read/convergence.json`(4종)이다.

| # | 검사 | 대상 | 무엇을 반증하는가 | 판정 기준 | 실패 시 조치 |
|---|---|---|---|---|---|
| 1 | **verbatim 존재** | 모든 `text_verbatim`·`quote`·`caption_quote`·`evidence_quotes[]` | LLM이 원문을 **다듬어 인용**하거나 없는 문장을 지어낸 것 | `source_path` 파일의 **바이트 정확 부분문자열**. 청구항 `text_verbatim`은 청구항 구간 안에서 | 해당 항목 목록 반환, READ 재작업(자동 재시도 없음 — 재시도는 같은 오류를 재생산한다) |
| 2 | **포인터 해소** | `claim_ref`·`material_id`·`component`·`attaches_to`·`derived_from[]`·`figure`·`superseded_by`·`applicant_interest.claim` | 존재하지 않는 대상을 참조하는 유령 링크, 오타 ID | 각 참조가 실재 대상으로 해소 + **kind 제약** 충족(아래 표) | 실패 참조 목록 반환, READ 재작업 |
| 3 | **커버리지** | 독립항 트리의 모든 element(재귀) | 청구항 일부를 **읽지 않고 넘어간 것** | 각 element의 `material_id`(component 항목)를 `grounding.component`로 참조하는 항목이 **1개 이상** | 미접지 element 목록 반환. 필수 실패 |
| 4 | **재독해 수렴** | 독립 2회 READ의 청구항 트리 | 독해가 **재현되지 않는 것**(1회성 추론) | 독립항 수 동일 **그리고** element `text_verbatim` 집합 Jaccard ≥ 0.95 | 재실행 1회 → 여전히 미달이면 **Owner 에스컬레이션**(불안정 신호) |

**검사 2의 kind 제약**

| 참조 필드 | 해소 대상 | kind 제약 |
|---|---|---|
| `elements[].material_id`, `additions[].material_id` | `items[].id` | `component` |
| `applicant_interest[].material_id` | `items[].id` | `implication` |
| `grounding.component` | `items[].id` | `component` |
| `implication.derived_from[]` | `items[].id` | 제약 없음(모든 kind 허용) |
| `superseded_by` | `items[].id` | 동일 kind + `status: "active"` |
| `claim_ref` | element id 또는 addition id | — |
| `attaches_to` | element id | — |
| `figure`, `figure_refs[].figure` | `figures[].id` | — |

**검사 1 보조 규정.** 원천 `00-source/patent.md`는 생성 시 1회 NFC 정규화된 UTF-8로 고정한다(§1 참조). 검사는 그 위에서 추가 정규화 **없이** 바이트 비교한다. 공백 접힘·따옴표 치환 같은 "친절한" 정규화를 넣지 않는 이유: 정규화가 관대해질수록 검사가 반증할 수 있는 대상이 줄어든다. 원문이 줄바꿈을 포함하면 인용도 줄바꿈을 포함하면 된다(바이트 비교이므로 문제되지 않는다). 청구항 구간의 경계 표기는 원천 정본 생성 규약 소관이다(§1 참조).

**검사 3 보조 규정.** 필수 대상은 **독립항 element 전량**이다. 종속항 `additions[]`의 접지는 **권고**이며, 미접지 addition 목록은 `convergence.json`의 `coverage.advisory[]`로 내보내 체크포인트 1 표면에 노출한다(승인 판단은 Owner). 종속항 전량 접지를 필수로 걸면 부가 한정 수십 개짜리 특허에서 READ 비용이 폭발하는데, 그 비용이 도슨트 산출물의 품질로 환산된다는 근거가 없다.

**검사 4 보조 규정.** Jaccard는 element `text_verbatim` 문자열의 **집합**(중복 제거, 정규화 없음) 위에서 계산한다: `|A ∩ B| / |A ∪ B|`. 독립항 수 불일치는 Jaccard와 무관하게 즉시 실패다(트리 개수가 다르면 비교 자체가 무의미). 두 READ는 **독립 실행**이어야 하며(같은 세션의 재생성 금지), `provenance.read_runs[]`에 두 실행 식별자를 남긴다.

```json
{
  "schema": "convergence/v0",
  "run_id": "example-xx0000000a1-stacked-module",
  "checks": {
    "verbatim": { "pass": true, "checked": 14, "failures": [] },
    "pointer": { "pass": true, "checked": 21, "failures": [] },
    "coverage": { "pass": true, "required": 2, "grounded": 2, "missing": [], "advisory": ["CL-5/a1"] },
    "convergence": { "pass": true, "independent_count": [1, 1], "jaccard": 1.0, "attempt": 1 }
  }
}
```

**4종의 사각지대(정직하게 기록).** `fact.value_normalized`는 verbatim 검사의 대상이 아니다 — `value_raw`가 원문에 있어도 정규화값이 잘못 적히면 4종 전부를 통과한다. 이 값은 숫자 게이트의 정답지이므로(§4.4) 오류가 하류로 전파된다. 대응: 정규화 일관성(정규화 함수를 `value_raw`에 적용한 결과 == `value_normalized`, 단위 일치)은 **스키마 검증기 층**의 부가 검사로 둔다(M1 범위, §5 이하 참조). 검사 4종의 이름·정의는 건드리지 않는다.

### §2.7 예시 인스턴스

**아래는 전부 가공 예시다. 실재 특허가 아니며 실재 특허를 인용하지 않는다.** 번호 `XX0000000A1`, 출원인 `Example Devices, Inc.`는 예시 전용 더미다.

가공 원천 `00-source/patent.md`(발췌):

```text
## Claims

1. A stacked module comprising: a substrate having a first surface; and a heat spreader thermally coupled to the first surface, the heat spreader defining a fluid channel.

5. The stacked module of claim 1, wherein the fluid channel has a hydraulic diameter of 0.08 mm.

## Brief description of the drawings

FIG. 2 is a section view of the heat spreader.

## Description

[0041] Conventional assemblies stack a cold plate on top of the module, which adds one more thermal interface.

[0042] The heat spreader 210 is bonded to the first surface 112 of the substrate 110. In this arrangement the channel is formed within the spreader so that a separate cold plate is not required, and the thermal interface count is reduced by one.
```

가공 인스턴스 `15-frozen/material-spec.v1.json`:

```json
{
  "schema": "material-spec/v0",
  "reader_version": "0.1.0",
  "spec_version": 1,
  "status": "frozen",
  "run_id": "example-xx0000000a1-stacked-module",
  "patent": {
    "number": "XX0000000A1",
    "title": "Stacked module with an integrated fluid channel (fictional example)",
    "assignee": "Example Devices, Inc.",
    "dates": { "priority": "2024-03-11", "filing": "2025-03-10", "publication": "2026-01-15" },
    "source_digest": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
    "source_path": "00-source/patent.md"
  },
  "claims": {
    "independent": [
      {
        "id": "CL-1",
        "type": "independent",
        "text_verbatim": "A stacked module comprising: a substrate having a first surface; and a heat spreader thermally coupled to the first surface, the heat spreader defining a fluid channel.",
        "elements": [
          {
            "id": "CL-1/e1",
            "text_verbatim": "a substrate having a first surface;",
            "material_id": "M1",
            "children": []
          },
          {
            "id": "CL-1/e2",
            "text_verbatim": "a heat spreader thermally coupled to the first surface, the heat spreader defining a fluid channel.",
            "material_id": "M2",
            "children": []
          }
        ]
      }
    ],
    "dependents": [
      {
        "id": "CL-5",
        "depends_on": "CL-1",
        "additions": [
          {
            "id": "CL-5/a1",
            "attaches_to": "CL-1/e2",
            "text_verbatim": "wherein the fluid channel has a hydraulic diameter of 0.08 mm",
            "material_id": "M3"
          }
        ]
      }
    ],
    "applicant_interest": [
      {
        "claim": "CL-1",
        "signal": "권리 관심이 '냉각 유로를 별도 부품이 아니라 히트 스프레더 몸체 안에 두는 구성'에 걸려 있음. 유로의 치수는 독립항이 아니라 종속항에 있음.",
        "material_id": "M6"
      }
    ]
  },
  "figures": [
    {
      "id": "FIG-2",
      "numerals": ["110", "112", "210"],
      "caption_quote": "FIG. 2 is a section view of the heat spreader.",
      "raw_path": "00-source/figures-raw/fig-02.png",
      "asset_path": null
    }
  ],
  "items": [
    {
      "id": "M1",
      "kind": "component",
      "status": "active",
      "superseded_by": null,
      "claim_ref": "CL-1/e1",
      "label_kr": "제1 면을 갖는 기판",
      "text_verbatim": "a substrate having a first surface;"
    },
    {
      "id": "M2",
      "kind": "component",
      "status": "active",
      "superseded_by": null,
      "claim_ref": "CL-1/e2",
      "label_kr": "유로를 몸체에 품은 히트 스프레더",
      "text_verbatim": "a heat spreader thermally coupled to the first surface, the heat spreader defining a fluid channel."
    },
    {
      "id": "M3",
      "kind": "component",
      "status": "active",
      "superseded_by": null,
      "claim_ref": "CL-5/a1",
      "label_kr": "유로 수력직경 한정",
      "text_verbatim": "wherein the fluid channel has a hydraulic diameter of 0.08 mm"
    },
    {
      "id": "M4",
      "kind": "grounding",
      "status": "active",
      "superseded_by": null,
      "component": "M2",
      "spec_refs": [
        {
          "locator": "[0042]",
          "quote": "The heat spreader 210 is bonded to the first surface 112 of the substrate 110.",
          "span": { "start": 503, "end": 581 }
        }
      ],
      "figure_refs": [
        {
          "figure": "FIG-2",
          "numerals": ["210", "112"],
          "caption_quote": "FIG. 2 is a section view of the heat spreader."
        }
      ]
    },
    {
      "id": "M5",
      "kind": "fact",
      "status": "active",
      "superseded_by": null,
      "label_kr": "유로 수력직경",
      "value_raw": "0.08 mm",
      "value_normalized": "0.08",
      "unit": "mm",
      "source": { "locator": "claim 5", "quote": "a hydraulic diameter of 0.08 mm" }
    },
    {
      "id": "M6",
      "kind": "implication",
      "status": "active",
      "superseded_by": null,
      "statement_kr": "유로를 히트 스프레더 몸체 안에 형성한다는 것은 냉각판을 한 장 없애는 방향, 즉 부품 추가가 아니라 계면 제거로 열을 다루려는 설계로 읽힘.",
      "basis": "spec",
      "derived_from": ["M2", "M4"],
      "evidence_quotes": [
        "the channel is formed within the spreader so that a separate cold plate is not required"
      ],
      "confidence": "inferred"
    },
    {
      "id": "M7",
      "kind": "positioning",
      "status": "active",
      "superseded_by": null,
      "background_problem": "종래 조립은 모듈 위에 냉각판을 얹어 열저항 계면을 하나 더 만든다.",
      "asserted_effect": "계면 수가 하나 줄어든다고 명세서가 문언으로 주장한다.",
      "delta": "성능 수치의 개선 주장이 아니라 구조 단순화(부품 제거) 방향의 주장.",
      "quotes": [
        "Conventional assemblies stack a cold plate on top of the module, which adds one more thermal interface.",
        "the thermal interface count is reduced by one"
      ]
    },
    {
      "id": "M8",
      "kind": "grounding",
      "status": "active",
      "superseded_by": null,
      "component": "M1",
      "spec_refs": [
        {
          "locator": "[0042]",
          "quote": "the first surface 112 of the substrate 110",
          "span": { "start": 538, "end": 580 }
        }
      ],
      "figure_refs": [
        {
          "figure": "FIG-2",
          "numerals": ["110", "112"],
          "caption_quote": "FIG. 2 is a section view of the heat spreader."
        }
      ]
    }
  ],
  "drop_signal": {
    "stage": "final",
    "verdict": "go",
    "reason": "권리 관심이 한 구성에 뚜렷하고, 효과 주장이 명세서 문언으로 존재해 '안도감 착지'가 물증으로 가능함."
  },
  "provenance": {
    "read_runs": ["read-a-0f1c2d3", "read-b-9a8b7c6"],
    "produced_at": "2026-02-01T00:00:00Z",
    "engine_commit": "0000000"
  }
}
```

**검사 4종이 이 인스턴스에서 보는 것**

| 검사 | 이 인스턴스에서 |
|---|---|
| verbatim 존재 | 청구항 2건·element 3건·`quote` 5건·`caption_quote` 2건·`evidence_quotes` 1건 = 총 13개 문자열이 발췌 원천의 부분문자열인지 확인한다(예: `"a hydraulic diameter of 0.08 mm"`는 claim 5 안에 그대로 있다). |
| 포인터 해소 | `CL-1/e1→M1`·`CL-1/e2→M2`·`CL-5/a1→M3`(kind=component), `attaches_to: CL-1/e2` 실재, `applicant_interest→M6`(kind=implication), `M4.component→M2`·`M8.component→M1`, `M6.derived_from→[M2,M4]`, `figure→FIG-2` 총 11개 참조를 해소한다. |
| 커버리지 | 필수 대상은 `CL-1/e1`·`CL-1/e2` 2개. e2는 M4가, e1은 M8이 접지하므로 통과. `CL-5/a1`은 권고 대상이며 미접지이므로 `coverage.advisory`에 실려 체크포인트 1에 노출된다. |
| 재독해 수렴 | 두 번째 READ가 독립항 1개를 내고 element `text_verbatim` 집합이 같으면 Jaccard = 1.0. 두 번째 READ가 e2를 "heat spreader"와 "fluid channel"로 쪼개면 집합이 `{e1, e2}` vs `{e1, e2a, e2b}`가 되어 Jaccard = 1/4 → 즉시 실패, 재실행. |

**틀린 변형과 대조.** 위 인스턴스에서 한 글자만 바꾼 판을 보자.

```text
"quote": "The heat spreader 210 is bonded to the first surface 122 of the substrate 110."
                                                              ^^^  (112 → 122)
```

| 검사 | 반응 |
|---|---|
| verbatim 존재 | **실패.** 이 문자열은 원천에 없다. 보고: `M4.spec_refs[0].quote not found; span [412,488) reads "...first surface 112 of..."` — `span`이 위치 지목 힌트로 쓰이는 자리다. |
| 포인터 해소 | 통과(구조는 멀쩡하다). |
| 커버리지 | 통과. |
| 재독해 수렴 | 통과 가능(청구항 트리는 건드리지 않았다). |

한 글자짜리 부호 오기는 사람 눈으로 잡히지 않고, 도면 주석판(D12)으로 흘러들어가 독자에게 틀린 부호를 보여준다. 4종 중 **하나만** 이것을 잡는다는 사실이 각 검사를 개별 필수로 두는 이유다. 반대로, `value_normalized`를 `"0.08"` → `"0.8"`로 바꾸면 **4종 전부 통과한다**(§2.6 사각지대). 그 자릿수는 이후 본문에서 게이트의 정답지로 쓰이므로, 정규화 일관성 검사를 검증기 층에 두는 근거가 여기 있다.

### §2.8 JSON Schema 스켈레톤

`reader/schemas/material-spec.schema.json`의 초안이다. **완전 구현이 아니며**(kind별 세부 제약·조건부 필수의 일부는 검증기 코드로 보강한다) 다음 방침이 보이면 족하다: draft 2020-12, 전 객체 `additionalProperties: false`, ID 문법 `pattern` 고정, enum 폐쇄. 구현은 후속 발주(M1).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://patent-docent.local/reader/schemas/material-spec.schema.json",
  "title": "material-spec/v0",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema", "reader_version", "spec_version", "status", "run_id", "patent", "claims", "figures", "items", "drop_signal", "provenance"],
  "properties": {
    "schema": { "const": "material-spec/v0" },
    "reader_version": { "type": "string", "pattern": "^[0-9]+[.][0-9]+[.][0-9]+$" },
    "spec_version": { "type": "integer", "minimum": 1 },
    "status": { "enum": ["draft", "frozen", "revised"] },
    "run_id": { "type": "string", "minLength": 1 },
    "patent": { "$ref": "#/$defs/patent" },
    "claims": { "$ref": "#/$defs/claims" },
    "figures": { "type": "array", "items": { "$ref": "#/$defs/figure" } },
    "items": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/item" } },
    "drop_signal": { "$ref": "#/$defs/drop_signal" },
    "provenance": { "$ref": "#/$defs/provenance" }
  },
  "$defs": {
    "item_id": { "type": "string", "pattern": "^M[0-9]+$" },
    "claim_id": { "type": "string", "pattern": "^CL-[0-9]+$" },
    "element_id": { "type": "string", "pattern": "^CL-[0-9]+/e[0-9]+(/e[0-9]+)*$" },
    "addition_id": { "type": "string", "pattern": "^CL-[0-9]+/a[0-9]+$" },
    "figure_id": { "type": "string", "pattern": "^FIG-[A-Za-z0-9-]+$" },
    "quote_ref": {
      "type": "object",
      "additionalProperties": false,
      "required": ["locator", "quote"],
      "properties": {
        "locator": { "type": "string" },
        "quote": { "type": "string", "minLength": 1 },
        "span": {
          "type": "object",
          "additionalProperties": false,
          "required": ["start", "end"],
          "properties": { "start": { "type": "integer", "minimum": 0 }, "end": { "type": "integer", "minimum": 0 } }
        }
      }
    },
    "figure_ref": {
      "type": "object",
      "additionalProperties": false,
      "required": ["figure", "numerals", "caption_quote"],
      "properties": {
        "figure": { "$ref": "#/$defs/figure_id" },
        "numerals": { "type": "array", "items": { "type": "string" } },
        "caption_quote": { "type": "string" }
      }
    },
    "patent": {
      "type": "object",
      "additionalProperties": false,
      "required": ["number", "title", "assignee", "dates", "source_digest", "source_path"],
      "properties": {
        "number": { "type": "string" },
        "title": { "type": "string" },
        "assignee": { "type": "string" },
        "dates": {
          "type": "object",
          "additionalProperties": false,
          "required": ["priority", "filing", "publication"],
          "properties": {
            "priority": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
            "filing": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
            "publication": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" }
          }
        },
        "source_digest": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" },
        "source_path": { "type": "string" }
      }
    },
    "element": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "text_verbatim", "material_id", "children"],
      "properties": {
        "id": { "$ref": "#/$defs/element_id" },
        "text_verbatim": { "type": "string", "minLength": 1 },
        "material_id": { "$ref": "#/$defs/item_id" },
        "children": { "type": "array", "items": { "$ref": "#/$defs/element" } }
      }
    },
    "claims": {
      "type": "object",
      "additionalProperties": false,
      "required": ["independent", "dependents", "applicant_interest"],
      "properties": {
        "independent": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["id", "type", "text_verbatim", "elements"],
            "properties": {
              "id": { "$ref": "#/$defs/claim_id" },
              "type": { "const": "independent" },
              "text_verbatim": { "type": "string", "minLength": 1 },
              "elements": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/element" } }
            }
          }
        },
        "dependents": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["id", "depends_on", "additions"],
            "properties": {
              "id": { "$ref": "#/$defs/claim_id" },
              "depends_on": { "$ref": "#/$defs/claim_id" },
              "additions": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": ["id", "attaches_to", "text_verbatim", "material_id"],
                  "properties": {
                    "id": { "$ref": "#/$defs/addition_id" },
                    "attaches_to": { "$ref": "#/$defs/element_id" },
                    "text_verbatim": { "type": "string", "minLength": 1 },
                    "material_id": { "$ref": "#/$defs/item_id" }
                  }
                }
              }
            }
          }
        },
        "applicant_interest": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["claim", "signal", "material_id"],
            "properties": {
              "claim": { "$ref": "#/$defs/claim_id" },
              "signal": { "type": "string", "minLength": 1 },
              "material_id": { "$ref": "#/$defs/item_id" }
            }
          }
        }
      }
    },
    "figure": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "numerals", "caption_quote", "raw_path", "asset_path"],
      "properties": {
        "id": { "$ref": "#/$defs/figure_id" },
        "numerals": { "type": "array", "items": { "type": "string" } },
        "caption_quote": { "type": "string" },
        "raw_path": { "type": "string" },
        "asset_path": { "type": ["string", "null"] }
      }
    },
    "item_common": {
      "type": "object",
      "required": ["id", "kind", "status", "superseded_by"],
      "properties": {
        "id": { "$ref": "#/$defs/item_id" },
        "kind": { "enum": ["component", "grounding", "fact", "implication", "positioning", "figure_note"] },
        "status": { "enum": ["active", "retracted", "superseded"] },
        "superseded_by": { "oneOf": [{ "$ref": "#/$defs/item_id" }, { "type": "null" }] }
      }
    },
    "item": {
      "allOf": [
        { "$ref": "#/$defs/item_common" },
        {
          "oneOf": [
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "claim_ref", "label_kr", "text_verbatim"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "component" },
                "claim_ref": { "type": "string", "pattern": "^CL-[0-9]+/(e[0-9]+(/e[0-9]+)*|a[0-9]+)$" },
                "label_kr": { "type": "string", "minLength": 1 },
                "text_verbatim": { "type": "string", "minLength": 1 }
              }
            },
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "component", "spec_refs", "figure_refs"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "grounding" },
                "component": { "$ref": "#/$defs/item_id" },
                "spec_refs": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/quote_ref" } },
                "figure_refs": { "type": "array", "items": { "$ref": "#/$defs/figure_ref" } }
              }
            },
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "label_kr", "value_raw", "value_normalized", "unit", "source"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "fact" },
                "label_kr": { "type": "string", "minLength": 1 },
                "value_raw": { "type": "string", "minLength": 1 },
                "value_normalized": { "type": "string", "minLength": 1 },
                "unit": { "type": ["string", "null"] },
                "source": { "$ref": "#/$defs/quote_ref" }
              }
            },
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "statement_kr", "basis", "derived_from", "evidence_quotes", "confidence"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "implication" },
                "statement_kr": { "type": "string", "minLength": 1 },
                "basis": { "enum": ["claim", "spec", "background", "effects"] },
                "derived_from": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/item_id" } },
                "evidence_quotes": { "type": "array", "minItems": 1, "items": { "type": "string", "minLength": 1 } },
                "confidence": { "enum": ["stated", "inferred"] }
              }
            },
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "background_problem", "asserted_effect", "delta", "quotes"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "positioning" },
                "background_problem": { "type": "string", "minLength": 1 },
                "asserted_effect": { "type": "string", "minLength": 1 },
                "delta": { "type": "string", "minLength": 1 },
                "quotes": { "type": "array", "minItems": 1, "items": { "type": "string", "minLength": 1 } }
              }
            },
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "kind", "status", "superseded_by", "figure", "what_it_shows_kr", "numerals"],
              "properties": {
                "id": {}, "status": {}, "superseded_by": {},
                "kind": { "const": "figure_note" },
                "figure": { "$ref": "#/$defs/figure_id" },
                "what_it_shows_kr": { "type": "string", "minLength": 1 },
                "numerals": { "type": "array", "items": { "type": "string" } }
              }
            }
          ]
        }
      ]
    },
    "drop_signal": {
      "type": "object",
      "additionalProperties": false,
      "required": ["stage", "verdict", "reason"],
      "properties": {
        "stage": { "enum": ["early", "final"] },
        "verdict": { "enum": ["go", "drop-proposed"] },
        "reason": { "type": "string", "minLength": 1 }
      }
    },
    "provenance": {
      "type": "object",
      "additionalProperties": false,
      "required": ["read_runs", "produced_at", "engine_commit"],
      "properties": {
        "read_runs": { "type": "array", "minItems": 1, "items": { "type": "string" } },
        "produced_at": { "type": "string" },
        "engine_commit": { "type": "string" }
      }
    }
  }
}
```

스키마만으로 표현하지 않고 **검증기 코드에 맡기는 제약**(M1 범위): ① `superseded_by`의 non-null 조건이 `status == "superseded"`와 일치 ② 참조 무결성 전반(§2.6 검사 2) ③ 정규화 일관성 ④ ID 연속성(`M1..Mn` 빠짐 없음). JSON Schema로 억지 표현하면 스키마가 읽히지 않게 되고, 계약 문서로서의 가치가 떨어진다.

---

## §3 주석층 표기 규약

### §3.1 목적

주석층은 **한 장치로 두 가지 문제를 동시에 푼다**(D8).

| 문제 | 주석층의 해법 |
|---|---|
| **성분 역참조**(D6 규율 ①) — 본문의 모든 기술 주장은 재료 항목 ID로 역참조 가능해야 하고, 위반은 게이트 결함이다 | 펜이 집필 시점에 문장마다 `[M3,M7]`을 단다. 사후 재구성(누가 어느 재료를 근거로 썼는지 나중에 추정)이 아니라 **집필과 동시 기록**이므로 추정 오차가 없다 |
| **출하본 무단 수정 봉쇄**(D8) — 게이트를 통과한 판과 실제로 나가는 판이 달라질 여지 | 출하본은 주석본에서 **결정론 변환으로 파생**된다. 사람이 출하본을 직접 쓰지 않으므로, 게이트 통과본과 출하본의 차이는 strip 함수 하나로 완전히 설명된다 |

부수 산출로 계기 국소화(D9)가 소비하는 트윗→문장→재료 맵이 공짜로 나온다(§3.3).

핵심 성질: **주석본이 정본이고 출하본이 파생물이다.** 출하본을 손으로 고치면 주석본과 어긋나고, round-trip 검사가 그 어긋남을 잡는다(§3.3). 파일 = `40-compose/<variant>/thread.annotated.md`.

### §3.2 문법

```
---
run_id: openai-us20260147854a1-cim-fp
variant: v2
pen: { vendor: anthropic, model: opus-5, effort: max }
spec_version: 1
spec_digest: sha256:...
---

## T1 {slot: hook, fig: fig-03}
Sentence one of the hook. [M12]
A framing sentence with no factual load. [narrative]

## T2 {slot: stop, fig: fig-07}
...
```

**프런트매터** — YAML, 아래 5키 정확히(초과·누락 모두 위반).

| 키 | 값 | 의미 |
|---|---|---|
| `run_id` | string | 런 식별자 |
| `variant` | `v1`\|`v2`\|`v3` | 변주 ID(D10) |
| `pen` | `{vendor, model, effort}` | 펜 배정. 토너먼트 기입의 원천(D10) |
| `spec_version` | integer | 인용이 겨냥한 동결본 버전 |
| `spec_digest` | `sha256:<64hex>` | 그 동결본 파일의 다이제스트. **어느 재료를 보고 썼는지의 물증** |

`spec_digest`가 있어야 "재료가 개정된 뒤에 쓰인 초안인가"를 기계가 판정한다. 게이트는 현재 동결본의 다이제스트와 대조하고, 불일치면 `annotation.schema` 결함으로 즉시 반려한다(낡은 재료로 쓴 원고를 검사하는 것은 무의미하다).

**트윗 헤더** — `## T<n> {slot: <slot>, fig: <figspec>}`

| 요소 | 규칙 |
|---|---|
| `<n>` | 1부터 시작하는 연속 정수. 건너뛰기·중복 금지 |
| `slot` | enum `hook`\|`stop`\|`pivot`\|`landing`\|`tail` — D11의 5슬롯(포스터 훅 / 전시 스톱 / 반전 스톱 / 착지 / 꼬리)에 1:1 대응 |
| `fig` | `fig-NN`, 복수는 `+`로 연결(`fig-03+fig-04`), 없으면 `none`. **최대 4**(D11 이미지 상한) |
| 공백 | `{slot: ..., fig: ...}` 안의 공백은 콤마 뒤 1칸으로 고정(파서는 관대하게, 린트는 엄격하게) |

**인용 태그**

| 규칙 | 내용 |
|---|---|
| 개수 | 문장마다 **정확히 1개**. 0개 = `annotation.missing-tag`, 2개 이상 = `annotation.schema` |
| 위치 | 문장 종결부호 뒤, **줄 끝 직전**. 줄 중간 태그 금지 |
| 문법 | `[M<n>(,M<n>)*]` 또는 `[narrative]`. **태그 내부에 공백 없음**(`[M3, M7]`은 위반, `[M3,M7]`이 정답) |
| 태그 앞 공백 | 0개 이상 허용(strip 정규식이 `\s*`로 흡수한다). 관용은 여기까지 |
| 이스케이프 | 본문의 리터럴 `[`는 `\[`로 쓴다. strip 4단계에서 복원된다 |
| 줄 규약 | **문장 1개 = 줄 1개.** 태그가 줄 끝에 오는 문법의 필연적 귀결이다 |

`fig`가 `none`인데 본문이 도면을 지시하는 경우(예: "the figure below")는 문법 위반이 아니다 — 기계가 판정할 수 없는 의미 문제이므로 게이트가 아니라 자문 소관이다(D7, §4.1).

**문법 위반 → L0 규칙 대응표**

| 위반 | 걸리는 규칙 |
|---|---|
| 프런트매터 키 누락·초과, YAML 파싱 실패 | `annotation.schema` |
| `spec_digest` ≠ 현재 동결본 다이제스트 | `annotation.schema` |
| 헤더 형식 오류, `slot` enum 밖 값, `fig` 형식 오류 | `annotation.schema` |
| 트윗 번호 불연속·중복 | `annotation.schema` |
| 태그 2개 이상, 줄 중간 태그, 태그 내부 공백 | `annotation.schema` |
| 태그 없는 문장 | `annotation.missing-tag` |
| 태그의 `M<n>`이 동결본에 없음 / `retracted` 항목 인용 | `citation.resolve` |
| `fig` 항목 5개 이상 | `format.images-per-post` |
| 트윗 수가 6~12 밖 | `format.tweet-count` |
| 본문 트윗 길이 180~260자 밖 | `format.body-length` |
| 본문에 URL(꼬리 제외) | `format.no-link-in-body` |
| 해시태그 존재 | `format.hashtag-zero` |

규칙 정의는 §4.4에 있다. 문법 검사가 **`annotation.schema` 하나에 몰려 있는 이유**: 문법 위반은 원인이 무엇이든 파싱 실패로 귀결되며, 하위 검사(인용 해소·숫자 대조)를 신뢰할 수 없게 만든다. 따라서 `annotation.schema` 실패 시 나머지 L0 규칙은 **평가하지 않고** 결함 1건만 보고한다(연쇄 오보 방지).

### §3.3 strip 규칙

결정론 변환이다. 같은 입력에 같은 출력이 나와야 하며, 어떤 판단도 개입하지 않는다.

| 단계 | 동작 |
|---|---|
| ① | 프런트매터(`---` … `---`) 제거 → 메타로 보존 |
| ② | `## T<n> {...}` 헤더 제거 → `thread.json`의 구조 메타로 이동 |
| ③ | 인용 태그 정규식(아래 코드블록 `STRIP_TAG_RE`)을 빈 문자열로 치환(멀티라인) |
| ④ | `\[` → `[` (이스케이프 복원) |
| ⑤ | 트윗 사이 빈 줄 정규화(트윗 경계 = 빈 줄 1개) |

③의 정규식 정본은 다음이다. **표 셀 안에 두지 않는다** — 마크다운 표에서 교호 바 `|`가 셀 구분자와 충돌해 `\|`로 이스케이프되면, 문서를 그대로 옮겨 적은 구현이 `[M12|narrative]`라는 존재하지 않는 형태만 지우고 실제 태그를 출하문에 남긴다(감수 2026-08-17, sol BLOCKER #6 — 초판이 이 상태였다).

```
STRIP_TAG_RE = \s*\[(M\d+(,M\d+)*|narrative)\]$
```

순서는 고정이다. ③이 ④보다 앞서는 것이 중요하다 — 순서가 뒤집히면 이스케이프 복원으로 생긴 `[`가 태그로 오인될 수 있다.

**출하 전 최종 안전망.** strip 이후 산출물에 `\[(M\d+|narrative)` 패턴이 하나라도 남아 있으면 `ship`은 `halt`한다. 정규식이 틀려도 주석이 실린 채 게시되는 일만은 막는다.

**무손실 round-trip 검사** — 두 방향 모두 강제한다.

| 방향 | 검사 | 무엇을 반증 |
|---|---|---|
| 순방향 | `strip(annotated)`의 본문이 "참조 구현으로 태그·헤더·프런트매터만 제거한 결과"와 **바이트 동일** | strip이 본문을 슬쩍 고치는 것(공백 접힘·구두점 정리 등) |
| 역방향 | `thread.json` + `annotation-index.json`으로 재조립한 주석본이 원본 `thread.annotated.md`와 **바이트 동일** | 변환 과정의 정보 손실(태그·슬롯·도면 배정 유실) |
| 재조립 | `thread.json.tweets[].text`를 규정 순서로 이어붙인 것이 `thread.md`와 **바이트 동일** | 인간본과 기계본의 표류 |

역방향까지 요구하는 이유: 순방향만 보면 "태그를 통째로 버리는" 구현도 통과한다. 그러면 계기 국소화(D9)가 쓸 맵이 조용히 비어버린다.

**산출 3종**

`70-ship/thread.md` — 인간·게시용. 트윗 사이 빈 줄 1개, 그 외 원문 유지.

`70-ship/thread.json`:

```json
{
  "schema": "thread/v0",
  "run_id": "example-xx0000000a1-stacked-module",
  "variant": "v2",
  "spec_version": 1,
  "spec_digest": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
  "tweets": [
    {
      "n": 1,
      "slot": "hook",
      "figures": ["fig-03"],
      "text": "Sentence one of the hook.\nA framing sentence with no factual load.",
      "char_count": 71
    }
  ],
  "images": [
    { "figure": "fig-03", "asset_path": "30-figures/assets/fig-03.png", "tweet": 1 }
  ]
}
```

`50-gate/<variant>/annotation-index.json` — 계기 국소화(D9)가 소비한다. 트윗→문장→인용 ID 맵이 정확해야 "전달에 실패한 재료 → 해당 트윗 자동 지목"이 성립한다.

```json
{
  "schema": "annotation-index/v0",
  "run_id": "example-xx0000000a1-stacked-module",
  "variant": "v2",
  "spec_version": 1,
  "tweets": [
    {
      "n": 1,
      "slot": "hook",
      "sentences": [
        { "i": 1, "text": "Sentence one of the hook.", "citations": ["M12"], "narrative": false },
        { "i": 2, "text": "A framing sentence with no factual load.", "citations": [], "narrative": true }
      ]
    }
  ],
  "by_material": {
    "M12": [{ "tweet": 1, "sentence": 1 }]
  },
  "narrative_sentences": [{ "tweet": 1, "sentence": 2 }]
}
```

`by_material`은 역인덱스다. 계기 채점이 "M12가 전달되지 않았다"고 판정하면 `by_material["M12"]`가 곧 `weakest_tweet` 후보 좌표가 된다(D9, 상세는 §6 소관). `locus`의 좌표계(`{tweet, sentence}`)는 게이트 레코드(§4.2)와 **동일**하다 — 게이트·계기·수정 지시가 같은 좌표를 쓴다는 것이 국소화의 전제다.

> [OPEN] 트윗 **내부**의 의도적 빈 줄. D11은 "줄바꿈 스캔성"을 요구하는데 주석본 문법은 문장 1개 = 줄 1개이며 strip ⑤는 트윗 **사이** 빈 줄만 규정한다. 트윗 안에서 의미 단락을 빈 줄로 나누는 것을 허용할지가 미정이다. 추천: v0는 **금지**(트윗 내부 빈 줄 = `annotation.schema` 위반)하고, 스캔성은 문장 단위 줄바꿈으로 충족한다 — 허용하면 strip ⑤와 트윗 경계 판정이 모호해진다.

### §3.4 `[narrative]` 신고의 의미

`[narrative]`는 **"이 문장은 근거가 필요 없는 서사 조직이다"라는 집필자의 자기 신고**다. 전환·호명·질문 던지기·리듬 문장이 여기 속한다. 도슨트 문체(D1)에서 이런 문장은 필수적이며, 모든 문장에 재료를 강제하면 글이 목록이 된다.

**그 신고가 참인지는 신고자가 정하지 않는다.**

| 층 | `[narrative]`에 대해 무엇을 하는가 |
|---|---|
| L0 | **신고의 존재와 형식만** 본다. 태그가 있는가, 문법이 맞는가. 내용 판단 없음 |
| L1 | **신고를 감사한다.** `[narrative]`로 선언된 문장에 기술 주장이 숨어 있는지 검출한다(밀수 검출, D8). 검출되면 거부권 있는 결함 |
| L2 | 신고 남용의 인상은 메모로만(거부권 없음) |

밀수의 전형: `"This is the part investors keep asking about."`(진짜 서사) vs `"This is the part where the memory sits right next to the compute."`(기술 주장인데 `[narrative]`로 신고됨). 후자는 재료 인용이 필요하며, `[narrative]` 신고로 성분 역참조(D6 규율 ①)를 우회한 것이다.

**왜 L0가 못 하는가.** "이 문장이 기술 주장인가"는 문언 대조로 판정되지 않는다. 정답이 존재하되(원천과의 관계) 그 판정에 의미 이해가 필요한 부류이므로, D7의 첫 서식지에 속하지만 결정론 층에는 앉힐 수 없다 — 그래서 L1(거부권 있는 대조 층)이 맡고, 노이즈는 k-반복 다수결로 줄인다(§4.5).

**자기 신고를 신뢰하지 않는 구조**가 요점이다. 신고는 **감사 대상을 좁히는 장치**이지 면제 장치가 아니다. L1은 `annotation-index.json`의 `narrative_sentences[]`를 우선 감사 표본으로 삼는다.

`[narrative]` 비율에 임계를 걸어 거부하는 규칙은 **두지 않는다**. "서사 문장이 40%면 너무 많은가"에는 정답이 없다(D7). 비율은 L1의 감사 표본 우선순위와 L2 메모의 재료로만 쓰이며, 어떤 점수로도 발행되지 않는다(D15, §4.6).

---

## §4 게이트 판정 데이터 모델

### §4.1 관할권 지도

**이 절의 헌법은 D7이다: 게이트의 관할 = 정답이 존재하는 범위. 한 뼘도 넓게 만들지 않는다.**

정답의 세 서식지(D7):

| # | 서식지 | 접근 시점 | 게이트화 가능? |
|---|---|---|---|
| 1 | **원천과의 관계** — 재료 대조 | 출하 전 | 가능(L0: 문언 대조 / L1: 의미 대조) |
| 2 | **입법된 규칙** — Owner 재정으로 결정론화된 문언 | 출하 전 | 가능(L0). 기계는 **문언만** 집행하고 법의 정신을 외삽하지 않는다 |
| 3 | **사후 독자 반응** | 출하 후 | 불가능. 환류로만 존재(D13) |

그 밖은 전부 **자문**(플래그·소견, 거부권 없음) 또는 **결함 카탈로그**(알려진 나쁨만 차단, 통과 ≠ 좋음, 등재는 Owner 재정)다.

**분류표.** 이 엔진에서 "검사하고 싶어질 법한" 술어들을 처분한다. 표의 오른쪽 두 열이 이 스펙의 실질이다.

| # | 술어 | 정답의 서식지 | 처분 | 근거 |
|---|---|---|---|---|
| 1 | 본문의 모든 수치·날짜·단위·특허번호가 동결 재료에 있는가 | ① 원천 | **게이트 L0** `numeric.exhaustive` | D8 |
| 2 | 인용 `M<n>`이 동결본에 해소되는가 / `retracted`를 인용했는가 | ①+② | **게이트 L0** `citation.resolve` | D8 |
| 3 | 주석층 문법이 맞는가 | ② 입법 | **게이트 L0** `annotation.schema` | D8 |
| 4 | 티커 표기(`$XYZ`)가 있는가 | ② 입법 | **게이트 L0** `lexicon.forbidden` | D3·D7 |
| 5 | 트윗 수 6~12 / 본문 180~260자 / 해시태그 0 / 본문 링크 0 / 이미지 ≤4 | ② 입법 | **게이트 L0** `format.*` | D11 |
| 6 | 신규 용어가 트윗당 1개 이하이고 즉시 풀이가 붙었는가 | ② 입법(블루프린트 선언 기준) | **게이트 L0** `format.new-term-budget` | D11 |
| 7 | 문장이 인용한 재료의 내용과 실제로 합치하는가 | ① 원천 | **게이트 L1**(거부권) | D8 |
| 8 | `[narrative]` 신고에 기술 주장이 숨어 있는가 | ① 원천 | **게이트 L1**(거부권) | D8·§3.4 |
| 9 | 재료에 없는 고유명사(경쟁사·제품명)가 등장했는가 | ① 원천 | **게이트 L1**. v0는 L0 규칙을 두지 않는다(고정 규칙 목록에 없음) | D7 |
| 10 | 암시적 투자 조언인가("이 기술이면 다음 분기는…") | 의미 판단, 정답 부재 | **자문 flag**(거부권 없음) — 체크포인트 2 첨부, 판정자 = **Owner** | D8 명시 |
| 11 | **모든 트윗이 맥락 없이 단독 생존 가능한가**(D11) | **없음** | **자문 memo(L2)** — 게이트 아님 | D7·D11 |
| 12 | **안도감 착지가 되었는가**(D2) | **없음** | **자문** — L2 memo + Fable 소견(D9) | D2·D7 |
| 13 | 훅이 투자자의 질문에 조응하는가(D3) | 없음 | 자문 memo·소견 | D3 |
| 14 | 도면 선택이 "최강 전시물"인가(D12) | 없음(사후엔 환류) | 자문 + 환류 | D12·D13 |
| 15 | 우선일을 gotcha 독법으로 다뤘는가(D5) | 없음(해석의 질) | 자문 memo | §2.3 |
| 16 | AI 텔 문형이 있는가 | ② 입법된 문언에 한해 | **결함 카탈로그** 등재분만 L0 regex 집행. 미등재 문형은 자문 | D7 |
| 17 | 독자가 실제로 이해했는가 | 계기 프로브(대리 측정) | **계기**(D9) — 게이트 아님, 거부권 없음 | D9 |
| 18 | 스레드가 좋은 글인가 / 공유될 만한가 | ③ 사후 반응 | **환류**(D13). 출하 전 접근 불가 | D2·D13 |
| 19 | 변주 3판 중 무엇을 낼 것인가 | 재정 | **Owner**(체크포인트 2). 게이트·자문 모두 거부권 없음 | D9·D10 |

**#11이 이 표에서 가장 중요한 훈련이다.** "모든 트윗은 맥락 없이 단독 생존 가능해야 한다"는 D11의 형식 요구이므로 L0에 넣고 싶어진다. 그러나 **판정에 정답이 없다** — "단독 생존"의 경계선을 문언으로 쓸 수 없고, 어떤 프록시(대명사 개수, 접속사로 시작하는 문장 수)를 세워도 그것은 헌장이 말한 것이 아니라 프록시가 말하는 것이 된다. 프록시를 거부권 층에 올리면 펜은 **프록시를 만족시키는 글**을 쓰게 되고(D15 굿하트), 규칙은 원래 의도와 무관하게 굳는다. 따라서 #11은 L2 자문이다. 예외 경로는 하나뿐이다: 특정 프록시가 실제로 유효함이 회귀 표본에서 확인되고 Owner가 **문언으로 입법**하면, 그 문언만 L0가 집행한다(서식지 ②로의 이주).

**#12도 같다.** "안도감 착지"는 이 엔진의 존재 이유(D2)지만, 존재 이유를 게이트에 넣는 것과 게이트가 그것을 판정할 수 있는 것은 별개다. 중요한 것을 거부권 층에 올리려는 충동이 D7이 막는 바로 그 충동이다.

**관할 확대 절차(고정).** 새 술어를 게이트에 편입하려면 넷을 모두 갖춘다. 하나라도 없으면 자문이다.

1. 정답의 서식지 명시(①·② 중 무엇인가).
2. 판정식의 **문언화**(regex·수치 범위·집합 포함 관계 등, 외삽 없이 실행 가능한 형태).
3. **Owner 재정**(`docs/decisions/D-YYYYMMDD-nn-<slug>.md`).
4. **회귀 케이스 동반** — 심은 결함 + golden 양쪽(§4.8). 케이스 없는 규칙은 등재하지 않는다.

### §4.2 레코드 3종

공통 골격: `{ id, layer, rule, locus: { tweet, sentence } }`.

| 종류 | 발행 층 | 거부권 | 필수 추가 필드 | 소비처 |
|---|---|---|---|---|
| `defect` | L0, L1 | **있음** | `expected`, `observed`, `fix_directive` | 국소 수정 루프(캡 3회, D8) |
| `flag` | L1 | 없음 | `note` | **체크포인트 2 첨부. 판정자 = Owner** |
| `memo` | L2 | 없음 | `text` | 펜 자유 리비전 1회(D8). **점수 필드 금지** |

**공통 필드**

| 필드 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `id` | `^(d\|f\|m)-l[012]-[0-9]{3}$` | ✔ | 예: `d-l0-003`. `verdict.json` 안에서 유일 |
| `layer` | enum `l0`\|`l1`\|`l2` | ✔ | 발행 층 |
| `rule` | string | ✔ | L0는 규칙 이름(§4.4), L1은 `l1.citation-mismatch`·`l1.narrative-smuggling`·`l1.advice-implicit`, L2는 `l2.<주제 slug>` |
| `locus.tweet` | integer \| null | ✔ | 트윗 번호. 스레드 전역 규칙(예: `format.tweet-count`)은 null |
| `locus.sentence` | integer \| null | ✔ | 트윗 내 문장 번호. 트윗 전역이면 null |

좌표계는 `annotation-index.json`과 동일하다(§3.3). 게이트 결함 좌표를 그대로 계기·수정 지시에 넘길 수 있는 이유다.

**`defect` 추가 필드**

| 필드 | 의미 |
|---|---|
| `expected` | 규칙이 요구한 것(예: `"수치 토큰 ⊂ frozen fact 집합 ∪ whitelist"`) |
| `observed` | 실제로 관측된 것(예: `"0.9|mm"`) |
| `fix_directive` | **지시문.** "어디를·어느 재료로" 형식. **대체 문장 제공 금지**(§4.7) |

**`flag` 추가 필드**

| 필드 | 의미 |
|---|---|
| `note` | 무엇이 걸렸는지의 서술. 판정하지 않고 제시한다 |
| `origin` | `minority-vote`(§4.5 강등) \| `advisory-rule`(애초에 거부권 없는 규칙) |
| `votes` | `origin: "minority-vote"`일 때 `{k, for, against}` |

flag는 **루프를 돌리지 않는다.** 펜에게 가지 않고 체크포인트 2 봉투(`70-ship/checkpoint2.md`)로 직행한다. 판정 적격자는 Owner뿐이다(D8).

**`memo` 추가 필드**

| 필드 | 의미 |
|---|---|
| `text` | 비평 서술. **숫자 필드 없음, 본문 점수 표현 금지**(§4.6) |

### §4.3 verdict.json

`50-gate/<variant>/verdict.json`.

```json
{
  "schema": "gate-report/v0",
  "run_id": "example-xx0000000a1-stacked-module",
  "variant": "v2",
  "gate_version": "0.1.0",
  "spec_version": 1,
  "spec_digest": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
  "thread_digest": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
  "l0": {
    "pass": false,
    "defects": [
      {
        "id": "d-l0-001",
        "layer": "l0",
        "rule": "numeric.exhaustive",
        "locus": { "tweet": 4, "sentence": 2 },
        "expected": "numeric token in frozen fact set or run whitelist",
        "observed": "0.9|mm",
        "fix_directive": "T4/S2의 수치를 M5로 재서술하라. 재료에 없는 값이면 문장에서 수치를 제거하라."
      }
    ]
  },
  "l1": { "pass": true, "k": 3, "votes": [], "defects": [], "flags": [] },
  "l2": { "memos": [] },
  "decision": "revise",
  "revision_round": 1
}
```

| 필드 | 의미 |
|---|---|
| `gate_version` | 게이트 구현 버전. 회귀 스위트 강제 조건이 걸리는 대상(§4.8) |
| `spec_version`·`spec_digest` | 어느 동결 재료로 판정했는가 |
| `thread_digest` | 판정 대상 `thread.annotated.md`의 다이제스트. 판정 후 원고가 바뀌면 verdict 무효 |
| `revision_round` | 0부터. 캡 3회(D8) |

**`decision` enum**

| 값 | 조건 | 다음 행동 |
|---|---|---|
| `advance` | `l0.pass && l1.pass` | 계기·소견 스테이지로. flag·memo는 동반하되 진행을 막지 않는다 |
| `revise` | (`!l0.pass \|\| !l1.pass`) && `revision_round < 3` | 국소 수정 지시로 COMPOSE 복귀. `revision_round` +1 |
| `escalate` | 캡 초과, 또는 재료 자체가 결함으로 지목됨(재료 반려 신호), 또는 `spec_digest` 불일치 | **Owner 에스컬레이션.** 대개 재료 반려행(D8) |

`decision`은 **L0·L1만으로 결정된다.** L2 메모와 flag는 어떤 조합으로도 `decision`을 바꾸지 못한다 — 이것이 "거부권 없음"의 기계적 의미다. 최종 심급(이력·메모를 모르는 새 눈, D8)은 별도 스테이지이며 §5 이하 소관이다.

### §4.4 L0 규칙 카탈로그

전 규칙은 **결정론**이며 같은 입력에 같은 판정을 낸다. 실패 메시지 형식 = `<rule>: <locus> — expected <expected>, observed <observed>`.

| 규칙 | 판정식 | 실패 메시지 예 | 화이트리스트 |
|---|---|---|---|
| `format.tweet-count` | `6 ≤ N ≤ 12`(D11) | `format.tweet-count: thread — expected 6..12, observed 14` | 없음 |
| `format.body-length` | `stop`·`pivot`·`landing` 슬롯의 유니코드 코드포인트 수 180~260. **`hook`은 상한 260만 적용(하한 미적용) — §9.2 재정 전까지 잠정** | `format.body-length: T3 — expected 180..260, observed 271` | 없음. `tail`·`hook` 하한 제외 |
| `format.word-budget` | **계류(거부권 없음) — §9.1 Owner 재정 대기.** 스레드 전체 단어 수 400~600(D11)을 측정해 `verdict.json`에 기록하되 **결함을 발행하지 않는다**. 단어 = 공백 분할 토큰, `tail` 제외 | `format.word-budget: thread — observed 712 (advisory, no veto)` | 해당 없음 |
| `format.hashtag-zero` | `#` + 문자로 시작하는 토큰 0개(전 트윗, D11) | `format.hashtag-zero: T7 — expected 0, observed 2` | 없음 |
| `format.no-link-in-body` | URL 패턴이 `tail` 외 트윗에 0개(D11 링크 격리) | `format.no-link-in-body: T5 — expected 0, observed 1` | `tail` 슬롯 |
| `format.images-per-post` | 트윗별 `fig` 항목 수 ≤ 4(D11) | `format.images-per-post: T1 — expected <=4, observed 5` | 없음 |
| `format.new-term-budget` | 블루프린트 `new_terms[]`에 **선언된** 용어만 대상. 트윗별 최초 등장 수 ≤ 1 **그리고** 최초 등장 트윗 안에 선언된 `gloss` 문자열이 존재 | `format.new-term-budget: T4 — expected <=1 new term with gloss, observed 2` | 블루프린트 선언 밖 용어는 대상 아님 |
| `annotation.schema` | §3.2 문법 전량 + 프런트매터 5키 + `spec_digest` 일치 | `annotation.schema: T2/S3 — expected exactly one trailing tag, observed 2` | 없음 |
| `annotation.missing-tag` | 모든 문장에 태그 1개 이상 | `annotation.missing-tag: T6/S1 — expected [M..] or [narrative], observed none` | 없음 |
| `citation.resolve` | 모든 인용 ID가 동결본 `items[]`에 존재 **그리고** `status != "retracted"` | `citation.resolve: T4/S2 — expected active material id, observed M12 (retracted)` | 없음 |
| `lexicon.forbidden` | `contracts/lexicon/forbidden.yaml`의 regex 목록 전량 비매칭. 등재는 **Owner 재정으로만**(D7) | `lexicon.forbidden: T9/S2 — expected no match for lex-003 (ticker), observed "$XYZ"` | 항목별 `exempt_slots` |
| `numeric.exhaustive` | §4.4.1 | `numeric.exhaustive: T4/S2 — expected token in frozen facts, observed "0.9|mm"` | `run.yaml`의 `numeric_whitelist[]` |

`forbidden.yaml` 항목 서식(정본은 §1 참조): `{ id: lex-003, pattern: "...", flags: "i", rationale: "...", decision_ref: "D-20260817-01-ticker", exempt_slots: [] }`. `decision_ref` 없는 항목은 로드 시 거부한다 — **입법 없이 집행하지 않는다**(D7).

`format.new-term-budget`이 블루프린트 선언에만 의존하는 것이 핵심이다. "무엇이 독자에게 새로운 용어인가"는 정답이 없으므로(D7), 기계는 **선언된 목록**이라는 입법된 문언만 집행한다. 선언이 부실하면 그것은 DESIGN의 문제이고, 게이트가 대신 판단하지 않는다.

#### §4.4.1 숫자 전수 대조 알고리즘

D8이 명시적으로 요구하는 유일한 내용 검사다: **본문의 모든 수치·날짜·단위·특허번호가 재료 명세에 포함되어야 한다(화이트리스트 제외).** 환각 수치는 도슨트 산출물의 최악 실패이며, 이 검사가 그 최악을 결정론으로 막는다.

**대조 대상 집합(정답지)** — 전부 동결 재료 또는 입법된 문언이다.

| # | 출처 | 비고 |
|---|---|---|
| 1 | `items[]` 중 `kind == "fact"` && `status == "active"`의 `value_normalized` + `unit` | 주 정답지 |
| 2 | `patent.number` | 특허번호 |
| 3 | `patent.dates.priority` / `.filing` / `.publication` | 날짜 |
| 4 | `run.yaml`의 `numeric_whitelist[]` | 명시 항목만 |

②③은 브리프의 "동결 재료" 안에 들어 있는 값이다(§2.2). 재료가 아닌 곳에서 정답지를 끌어오지 않는다.

**절차**

```text
tokens  = tokenize(shipped_text)          # 출하 텍스트(strip 산출) 기준
keys    = { normalize(t) for t in tokens }
answers = facts ∪ patent_number ∪ patent_dates ∪ whitelist
unmatched = keys - answers
if unmatched: emit defect per token (locus = annotation-index 역참조)
```

대조 대상 텍스트는 **출하본**이다(주석본이 아니다). 주석 태그 안의 `M12`가 수치로 오인되는 것을 원천 차단한다.

**토큰화 정규식 후보** — 우선순위 순으로 시도하고, 매칭된 구간은 소비한다(긴 패턴 우선). 아래는 **예시이며 구현은 후속 발주(M4)**다.

| 순위 | 종류 | 패턴(후보) |
|---|---|---|
| 1 | 특허번호 | `\b[A-Z]{2}\s?\d{6,}(?:\s?[A-Z]\d?)?\b` |
| 2 | ISO 날짜 | `\b\d{4}-\d{2}-\d{2}\b` |
| 3 | 영문 날짜 | `\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+\d{4}\b` |
| 4 | 범위 | `\b\d+(?:\.\d+)?\s*(?:-|–|—|to)\s*\d+(?:\.\d+)?\s*[A-Za-zµ%°]*\b` |
| 5 | 백분율 | `\b\d+(?:\.\d+)?\s*%` |
| 6 | 배수 | `\b\d+(?:\.\d+)?\s*[x×]\b` |
| 7 | 수치+단위 | `\b\d[\d,]*(?:\.\d+)?\s*(?:nm|µm|um|mm|cm|m|GHz|MHz|W|mW|V|mV|A|mA|J|pJ|TOPS|GB|MB|Gb|bit|bits|°C|K)\b` |
| 8 | 연도 단독 | `\b(?:19|20)\d{2}\b` |
| 9 | 맨 숫자 | `\b\d[\d,]*(?:\.\d+)?\b` |

**정규화 규칙**

| 대상 | 규칙 |
|---|---|
| 천단위 구분 | `,` 제거 |
| 소수 | 후행 0 제거(`0.80` → `0.8`), 선행 0 보존(`0.8` 유지), `.8` → `0.8` |
| 유니코드 숫자 | ASCII로 정규화 |
| 단위 | 소문자화 + 별칭 사전(`um`→`µm`, `micron`→`µm`, `℃`→`°c`). 별칭 사전은 입법 대상이며 Owner 재정으로 확장 |
| 백분율 | `unit = "%"` |
| 배수 | `unit = "x"` |
| 범위 | 두 끝값으로 **분해**해 각각 대조. 추가로 범위 자체를 `a-b\|unit` 키로도 시도(재료가 범위를 한 항목으로 담은 경우) |
| 날짜 | `YYYY-MM-DD`로 환산. 연도 단독은 `YYYY\|year` |
| 특허번호 | 공백·하이픈 제거 + 대문자화 |
| 대조 키 | `f"{value_normalized}|{unit or ''}"` |

**매칭은 정확 일치만이다.** 근사 일치·반올림 허용을 넣지 않는다. "3.9를 4로 반올림해 써도 되는가"에는 정답이 없고(D7), 정답 없는 판단을 거부권 층에 넣으면 게이트가 문언 아닌 정신을 외삽하기 시작한다. 반올림이 필요하면 READ가 그 값을 `fact` 항목으로 등재해야 한다(재료를 고치는 것이 옳은 방향, D6 규율 ②).

**화이트리스트 정책**

| 항목 | 내용 |
|---|---|
| 위치 | `run.yaml`의 `numeric_whitelist[]`. 런 단위 |
| 형식 | `{ key: "1/9", rationale: "스레드 순번 표기", added_by: "owner" }` |
| 기본값 | **비어 있음.** 필요할 때만 명시 등재 |
| 전형 | 스레드 순번(`n/N`), 트윗 번호 표기 |
| 노출 | 화이트리스트 전체를 체크포인트 2 봉투에 **그대로 인쇄**한다. 화이트리스트는 게이트에 뚫는 구멍이므로 Owner가 매 런 눈으로 본다 |

> [OPEN] 화이트리스트 등재의 격. `run.yaml` 편집이 곧 게이트 완화이므로 `forbidden.yaml`처럼 Owner 재정(`decision_ref`)을 요구할지, 런 단위 재량으로 둘지가 미정이다. 추천: **런 단위 재량 + 체크포인트 2 전량 인쇄**(위 규정)로 시작하고, 화이트리스트가 3항목을 넘는 런이 나오면 그때 재정으로 승격.

### §4.5 L1 k-반복 다수결

| 항목 | 값 |
|---|---|
| k | 기본 3(홀수 유지) |
| 실행 | 동일 프롬프트·동일 입력으로 **독립 실행** k회 |
| 채택 | 과반(k=3이면 2표 이상) 일치 항목만 `defect`로 채택 |
| 강등 | 과반 미달 항목은 `flag`(`origin: "minority-vote"`, `votes: {k, for, against}`)로 기록 |
| 동일성 | 같은 `rule` + 같은 `locus`면 같은 항목으로 센다. 문언 표현의 차이는 무시 |
| 기록 | `l1.votes[]`에 회차별 원 판정을 보존(사후 감사용) |

**왜 다수결인가.** L1은 의미 판정이라 실행마다 흔들린다. 흔들림에는 두 성분이 있다: 표집 분산(같은 모델이 같은 입력에 다른 답을 내는 것)과 편향(모델이 특정 유형을 체계적으로 놓치거나 과검출하는 것). 다수결은 **분산만** 줄인다. 1회 실행의 우연한 오검출로 펜을 헛돌리는 것이 실제 비용이 크므로, 이 교환은 성립한다.

**한계 — 정직하게 기록한다.**

1. **편향은 줄지 않는다.** k회는 독립 표본이 아니라 같은 사전분포의 반복이다. 모델이 체계적으로 못 잡는 결함 유형은 k=99여도 못 잡는다. 이 성분은 회귀 스위트(§4.8)가 잡는다 — 그래서 두 기제가 모두 필요하다.
2. **희귀한 참 결함이 강등된다.** 1/3만 발견한 진짜 결함은 flag로 내려간다. 그래서 강등은 **삭제가 아니라 이동**이다 — flag는 체크포인트 2에서 Owner 눈앞에 놓인다(D8).
3. **k 증가는 수확 체감**이며 비용은 선형이다. k 상향은 회귀 표본에서 검출률 개선이 확인될 때만 한다.
4. **다수결은 판정의 질을 보증하지 않는다.** 세 번 다 틀릴 수 있다. 최종 심급이 별도로 있는 이유다(D8·D15).

### §4.6 L2 자문 — 점수 발행 금지의 기계적 집행

L2는 전역 판단 층이며 **비평 메모만** 낸다(D8). 산출 = `50-gate/<variant>/l2.md` + `verdict.json`의 `l2.memos[]`.

점수 금지는 규범 선언이 아니라 **세 겹의 기계 집행**이다(D8·D15).

| # | 기제 | 내용 |
|---|---|---|
| 1 | 스키마 폐쇄 | `contracts/schemas/gate-report.schema.json`의 memo 객체가 `additionalProperties: false`. 새 필드를 몰래 못 넣는다 |
| 2 | 숫자 필드 부재 | memo의 모든 속성이 `type: "string"`(또는 string 배열). `number`·`integer` 타입 필드가 **하나도 없다** |
| 3 | 린트 | L2 산출물(`l2.md` + memo 객체의 키·본문) 전체에 대해 `/score|rating|grade|점수|\d+\s*\/\s*10/` 매칭 시 **거부** |

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "layer", "rule", "locus", "text"],
  "properties": {
    "id": { "type": "string", "pattern": "^m-l2-[0-9]{3}$" },
    "layer": { "const": "l2" },
    "rule": { "type": "string" },
    "locus": {
      "type": "object",
      "additionalProperties": false,
      "required": ["tweet", "sentence"],
      "properties": {
        "tweet": { "type": ["integer", "null"] },
        "sentence": { "type": ["integer", "null"] }
      }
    },
    "text": { "type": "string", "minLength": 1 }
  }
}
```

**왜 이렇게까지 하는가**(D15 굿하트 가드). 점수가 존재하면 그 즉시 세 가지가 따라온다: ① 펜 프롬프트에 점수가 흘러들어가 점수 추격 루프가 생긴다 ② 변주 비교가 점수 정렬로 대체되어 Owner의 재정(D9·D10)이 형해화된다 ③ 점수가 낮은 판이 자동으로 버려지면서 **취향 데이터가 소실**된다(D10 이중 기입의 원천이 마르는 것). "측정지표가 목표가 되는 순간 좋은 지표이기를 멈춘다"(D15).

린트가 본문까지 보는 이유: 스키마는 `"text": "구조 8/10 수준"`을 막지 못한다. 자연어 안에 점수를 밀수하는 경로를 같이 닫는다. 린트 패턴의 확장(별점·A~F 등급 등)은 **Owner 재정**으로 한다 — 린트 자체가 입법된 문언이기 때문이다(D7).

L2의 위상도 봉쇄되어 있다: **메모 1회 → 펜 자유 리비전 1회**(D8). 리비전 결과에 다시 L2를 돌리지 않는다. 돌리면 그것이 곧 점수 없는 점수 추격 루프다.

### §4.7 게이트가 글을 고치지 않음의 집행

D8: **게이트는 어떤 경우에도 직접 글을 고치지 않는다**(검사자 소견 / 펜 집필의 관할선).

| # | 집행 기제 | 내용 |
|---|---|---|
| 1 | 레인 권한 | 게이트 레인은 **쓰기 도구 없음**(read-only). 유일한 예외로 `50-gate/<variant>/` 아래 판정 산출만 기록한다. `40-compose/`·`70-ship/`에 대한 쓰기는 스테이지 계약에서 금지(§5 이하 참조) |
| 2 | `fix_directive`의 형식 | "**어디를 · 어느 재료로**" 지시문. 대체 문장 리터럴 제공 금지 |
| 3 | 린트 | `fix_directive`에 따옴표로 감싼 5토큰 이상의 EN 문장이 들어 있으면 **경고**(초안 문장 밀수 의심) |

`fix_directive` 예시:

| 판정 | 좋은 지시문 | 나쁜 지시문(위반) |
|---|---|---|
| `numeric.exhaustive` | `T4/S2의 수치를 M5로 재서술하라. 재료에 없는 값이면 문장에서 수치를 제거하라.` | `T4/S2를 "The channel is 0.08 mm wide."로 바꿔라.` |
| `citation.resolve` | `T4/S2가 인용한 M12는 superseded다. M9로 재서술하라.` | (대체 문장 제공) |
| `annotation.missing-tag` | `T6/S1에 근거 재료 태그를 달거나, 서사 문장이면 [narrative]로 신고하라.` | (문장 대체) |

**왜 지시문인가.** 게이트가 문장을 써 주면 세 가지가 무너진다: ① 펜 토너먼트의 공정성(D10 — 어느 변주가 게이트 문장을 더 많이 받았는지가 교란 변수가 된다) ② 보이스의 일관성(검사자는 도슨트 보이스로 쓰지 않는다) ③ 책임 소재(누가 쓴 글인지 모호해지면 앵커 원장의 취향 데이터가 오염된다, D13). 지시문은 **무엇이 틀렸는지**를 말하고 **어떻게 쓸지**는 펜에게 남긴다.

수정 루프는 캡 3회이며 초과 시 `escalate`(대개 재료 반려행)다(D8·§4.3). 캡은 "지시문으로 안 되는 것은 지시문을 더 줘도 안 된다"는 판단이며, 반복 실패는 원고가 아니라 **재료의 문제**라는 신호로 읽는다.

### §4.8 회귀 스위트 (D8 메타)

golden(출하 확정본)과 변조본(결함을 심은 판)을 상비하고, **게이트를 수정할 때마다** 전량 돌린다. 원장은 `ledgers/regression/`이며 독자 반응과 무관하게 Owner 재정으로 큐레이션한다(D13 — 인기로 물갈이하면 커버리지가 붕괴한다).

```
ledgers/regression/
  golden/           # 출하 확정본 스냅샷 (+ 동결 재료 사본)
  mutated/          # 변조본
  cases.jsonl       # 케이스 원장
```

**`cases.jsonl` 스키마** — 각 행 1케이스.

| 필드 | 타입 | 의미 |
|---|---|---|
| `case_id` | string | 유일 식별자(예: `rc-0007`) |
| `base` | string | golden 스냅샷 경로 |
| `mutation` | object \| null | `{ type, locus }`. null이면 golden 케이스(변조 없음) |
| `mutation.type` | enum(아래) | 심은 결함의 종류 |
| `mutation.locus` | `{tweet, sentence}` | 심은 위치 |
| `expect` | object | `{ detector, must_detect }` |
| `expect.detector` | string | 이 결함을 잡아야 할 **규칙 이름**(§4.4 또는 `l1.*`) |
| `expect.must_detect` | boolean | 변조 케이스는 `true`, golden 케이스는 `false` |

```jsonl
{"case_id":"rc-0001","base":"golden/run-01/thread.annotated.md","mutation":null,"expect":{"detector":"*","must_detect":false}}
{"case_id":"rc-0007","base":"golden/run-01/thread.annotated.md","mutation":{"type":"ungrounded-number","locus":{"tweet":4,"sentence":2}},"expect":{"detector":"numeric.exhaustive","must_detect":true}}
{"case_id":"rc-0008","base":"golden/run-01/thread.annotated.md","mutation":{"type":"smuggled-claim-in-narrative","locus":{"tweet":6,"sentence":1}},"expect":{"detector":"l1.narrative-smuggling","must_detect":true}}
```

**mutation type enum**

| type | 심는 것 | 무엇을 반증하는가 |
|---|---|---|
| `hallucinated-claim` | 재료에 없는 기술 주장 문장 | L1 국소 대조가 살아 있는가 |
| `ticker` | `$XYZ` 형태 티커 표기 | `lexicon.forbidden`이 살아 있는가(D3) |
| `ungrounded-number` | 재료에 없는 수치 | `numeric.exhaustive`가 살아 있는가 |
| `smuggled-claim-in-narrative` | 기술 주장을 `[narrative]`로 신고 | `[narrative]` 감사가 살아 있는가(§3.4) |
| `retracted-citation` | `retracted` 항목 인용 | `citation.resolve`의 status 검사가 살아 있는가(§2.4) |

**게이트 수정 시 강제 조건(고정)**

| # | 조건 |
|---|---|
| 1 | 심은 결함 **100% 검출**(모든 `must_detect: true` 케이스가 지정 `detector`로 검출) |
| 2 | golden **100% 통과**(모든 golden 케이스가 결함 0건) |
| 3 | 신규 L0/L1 규칙 추가 시 케이스 **동반 필수**(§4.1 관할 확대 절차 4항) |
| 4 | 조건 1·2 충족 시에만 `gate_version` 상향 |

"게이트 수정"의 정의 = L0 규칙 구현·`forbidden.yaml`·L1 프롬프트·strip 구현·판정 임계값 중 하나라도 바뀌는 것. 검증은 pytest로 하고, **`assert` 기반 자체 검증 스크립트를 쓰지 않는다**(`python3 -O`에서 제거되어 망가진 코드가 공허 통과한다 — 2026-08-16 실측). 회귀 실패는 테스트 실패로 표면화한다.

**공용 인프라.** 계기(D9)의 판별력 교정 — golden 표본에서 점수가 높고 변조 표본에서 낮은지 확인하는 절차 — 이 같은 `golden/`·`mutated/`·`cases.jsonl`을 사용한다. 즉 이 디렉터리는 게이트만의 자산이 아니라 **검증 인프라 공용 자산**이다. 상세는 §6 소관(참조만).

> [OPEN] `superseded` 항목 인용의 처분. 고정 규칙은 `retracted` 인용만 defect로 규정하고 `superseded`는 침묵한다. `superseded`는 "더 나은 항목이 생겼다"이므로 인용이 곧 거짓은 아니지만 낡은 것은 맞다. 추천: **defect로 올리지 않고 L1 `flag`(`origin: "advisory-rule"`)로 첨부**해 체크포인트 2에서 Owner가 본다 — 거부권 확대 없이 가시성만 얻는 안이다.

---

## §5 계기·소견 프로토콜

계기(instrument)와 소견(critique)은 게이트가 아니다. 게이트가 관할하는 "정답이 존재하는 범위"(D7) 바깥에서, **거부권 없이** 관측치를 생산하는 자문 층이다(D9). 이 절은 그 관측 장치의 명세다.

### §5.1 설계 원리

**원리 1 — 자기보고 금지.** 모델에게 "이 스레드가 이해되었습니까"를 묻지 않는다. LLM의 자기 내성 보고는 신뢰하지 않는다는 것이 헌장의 전제다(D9). 계기는 **행동 프로브**만 쓴다: 모델에게 과제를 시키고, 그 **행동의 산출물**을 별도 심급이 채점한다. 프로브 모델은 자기 점수를 알지 못하고 발행하지도 않는다.

**원리 2 — 측정 대상은 전달 충실도이지 이해도가 아니다.** 측정량은 "이 스레드를 텍스트만 읽었을 때, 블루프린트가 전달하려던 것이 실제로 건너갔는가"다(D9). 독자상이 학습자가 아니라 투자자-팬이므로(D2), 특허 전반의 이해를 묻는 퀴즈는 애초에 목표가 아니다. 목표는 "막힘 없이 읽히는가"이며, 이는 **전달 표적의 도달률**로 조작적 정의된다.

**원리 3 — 측정 장치는 목표가 될 수 없다.** 계기 점수는 게이트 통과 조건이 아니고, 펜에게 점수를 올리라는 지시를 내리지 않는다(D15). §5.7이 이 제약의 기계적 집행을 규정한다.

| 구분 | 측정한다 | 측정하지 않는다 |
|---|---|---|
| 계기 | 블루프린트가 표적으로 선언한 재료의 도달률 | 특허에 대한 일반 이해도 |
| 계기 | 스레드 텍스트만으로 답할 수 있는가 | 프로브 모델의 사전 지식 |
| 계기 | 전달 실패의 **위치**(트윗) | 문장의 좋음/나쁨 |
| 소견 | 훅 조응·안도감 착지·도슨트 보이스 | 점수·등급(D15) |

### §5.2 프로브 A/B 명세

프로브는 `probe` 스테이지에서 n대 동시 실행한다(계기 = Haiku n대, 기본 n=5 — D9). 각 프로브는 독립 컨텍스트에서 1회만 호출되고, 서로의 출력을 보지 않는다.

**입력 격리(설계의 심장).** 프로브의 입력은 **출하 후보 스레드 텍스트뿐**이다. 재료 명세(동결본), 블루프린트, 주석층, 게이트 결과, 원천 특허 어느 것도 주지 않는다. 프로브가 재료를 보면 "스레드가 전달했는가"와 "프로브가 재료를 읽었는가"가 구분 불가능해져 측정이 붕괴한다. 이 격리는 스테이지 계약의 `must_not_read`로 집행한다(계약 서식은 §2.4 참조).

| 프로브 | 입력 | 과제 | 출력 |
|---|---|---|---|
| A | 스레드 텍스트 | 핵심 주장 3문장 재서술 | `a_restatement[3]` |
| B | 스레드 텍스트 + 표적 질문지 | 질문별 답변 + 근거 인용 | `b_answers[]` |

**프로브 B 질문지의 파생 규칙.** 질문은 블루프린트의 `transmission_targets`(전달 표적 = 재료 ID 목록, §2.5 참조)에서 파생한다. 표적 재료 ID 하나가 질문 하나로 대응한다.

- 질문 생성기는 **동결 재료 + `transmission_targets`**를 읽고 질문지를 만든다. 출하 후보 스레드는 보지 않는다 — 스레드를 보고 질문을 만들면 "스레드에 있는 것만 묻는" 자기 충족 측정이 된다.
- 질문지는 **런 단위**이며 변주 단위가 아니다. 변주들은 같은 재료·같은 블루프린트를 받으므로(D10 공정 비교) 같은 질문지로 재야 비교가 성립한다. 파일 = `60-probe/questions.json`(변주 디렉토리 바깥, 런 레벨).
- 질문은 표적 재료 하나만 겨냥한다(`target_material_id` 필수, 1:1). 두 재료를 합친 복합 질문은 실패 위치 국소화를 파괴하므로 금지한다.
- **표적 밖 재료를 묻는 질문은 무효다.** 동결 재료에 있으나 블루프린트가 전달 표적으로 선언하지 않은 항목을 묻는 순간, 그것은 전달 충실도 측정이 아니라 이해 퀴즈가 된다. 이 규칙이 §5.1 원리 2를 기계적으로 집행하는 장치다(D9). 질문 생성기는 `target_material_id ∈ transmission_targets`를 검사하고 위반 질문을 폐기한다.

**답변 규약.** 프로브 B의 각 답변은 두 필드를 필수로 갖는다.

- `answer_kind`: `stated`(스레드에서 답을 찾음) 또는 `not-stated`(스레드에 없음). `not-stated`는 1급 답변이며 오답이 아니다 — 이것이 "전달 안 됨"과 "프로브가 틀림"을 분리한다.
- `quoted_span`: `stated`일 때 근거가 된 스레드 원문 구간. 채점 전에 **결정론 검사**로 스레드 텍스트의 부분문자열인지 확인한다. 부분문자열이 아니면 그 답변은 프로브 환각으로 판정해 무효 처리하고 `not-stated`로도 세지 않는다(분모에서 제외 + `notes`에 기록).

**프로브 출력 서식** (`60-probe/<variant>/probe-<i>.json`, 스키마 = `contracts/schemas/probe-report.schema.json`):

```jsonc
{
  "schema": "probe-report/v0",
  "probe_id": "p3",
  "model": { "vendor": "anthropic", "model": "haiku-...", "effort": "low" },
  "input_digest": "sha256:...",          // 읽은 스레드 텍스트의 해시 — 무엇을 쟀는지의 증거
  "question_set_digest": "sha256:...",
  "a_restatement": ["...", "...", "..."],
  "b_answers": [
    { "question_id": "Q3", "target_material_id": "M12",
      "answer_kind": "stated", "answer": "...", "quoted_span": "..." },
    { "question_id": "Q4", "target_material_id": "M19",
      "answer_kind": "not-stated", "answer": null, "quoted_span": null }
  ],
  "produced_at": "..."
}
```

프로브 리포트에는 **점수 필드가 없다**(스키마 `additionalProperties: false`). 프로브는 자기 성적을 산출하지 않는다.

### §5.3 채점 분리

**채점자는 프로브가 아니다**(D9). 별도 레인이 동결된 재료 명세를 정답지로 삼아 대조한다. 채점자의 입력은 **프로브 답변 + 동결 재료 항목**이며, 스레드 원문은 주지 않는다 — 채점자가 스레드를 보면 프로브 답변 대신 스레드를 후하게 읽어주는 편향(관대한 해석)이 들어와 다시 자기보고와 같은 문제가 된다.

**결정론 대조와 모델 채점의 경계선**(고정 판별식):

| 표적 재료 `kind` | 채점 방식 | 대조 대상 | 근거 |
|---|---|---|---|
| `fact` | **결정론** | `value_normalized` + `unit` | 수치·날짜·단위는 정답이 문자열로 존재(D7의 "원천과의 관계") |
| `component` | **결정론** | `text_verbatim` 정규화 문자열 포함 여부 | 청구항 구성요소 라벨은 원문 고정 |
| `figure_note` | **결정론** | `numerals[]` 집합 일치 | 도면부호는 기호열 |
| `grounding` | 모델 | `spec_refs[].quote` 요지 | 접지 내용은 서술 |
| `implication` | 모델 | `statement_kr` 등가성 | 기술적 함의는 문장 |
| `positioning` | 모델 | `background_problem` / `delta` | 대비 서술 |

**정규화 규칙(결정론 경로).** NFKC 정규화 → 소문자 → 연속 공백 1개 → 문장부호 제거(수치의 소수점·하이픈은 보존) → 수치는 십진 표준형(`1,024` → `1024`, `2.50` → `2.5`, `12%` → `0.12` 병기) → 단위는 별칭 표(`nm`/`nanometer`) 적용. 정규화 표는 `reader/lib/`에 두어 게이트의 `numeric.exhaustive`(§2.5 참조)와 **같은 구현을 공용**한다. 두 벌을 두면 게이트와 계기가 서로 다른 수를 같다고 판정하는 사고가 난다.

**우선순위 불변식**: 결정론 대조가 판정한 항목은 모델 채점이 뒤집을 수 없다. 채점자에게는 그 항목이 아예 전달되지 않는다(입력 자체에서 제외).

**모델 채점 출력 규약**: 3값 `hit | partial | miss` + 판정 근거로 삼은 프로브 답변 구간 인용 필수. `partial` = 0.5로 환산한다. 채점자는 자연어 총평을 쓰지 않는다(소견의 관할 — D9).

**프로브 A의 채점**은 별도 축이다. 3문장 재서술이 블루프린트의 논지(thesis)와 정합하는지 모델 채점으로 `aligned | drifted | inverted` 3값 판정하고, `score.json`의 `restatement` 블록에 기록한다. 이 축은 도달률 계산에 합산하지 않는다 — 서로 다른 것을 재는 두 눈금을 하나의 수로 섞지 않는다.

### §5.4 국소화

"어느 재료가 전달에 실패했는가"에서 "어느 트윗이 문제인가"로 내려가는 경로는 **채점 결과 + `annotation-index.json` 역참조**다(D9). `annotation-index.json`은 strip 단계가 생산하는 트윗→문장→인용 재료 ID 맵이다(§2.4 참조).

국소화 알고리즘(결정론):

1. 표적 재료 `M12`의 도달률 `hit_rate`를 n대 프로브에 대해 계산한다(`hit`=1, `partial`=0.5, `miss`=0, 무효 답변은 분모 제외).
2. `annotation-index.json`에서 `M12`를 인용한 문장 집합을 역조회한다.
3. 그 문장들이 속한 트윗 중 도달 실패에 가장 크게 기여한 트윗을 `weakest_tweet`으로 지목한다. 후보가 복수면 (a) 인용 문장 수가 적은 트윗 (b) 트윗 번호가 큰 쪽(스레드 후반은 이탈 구간) 순으로 결정론 타이브레이크한다.
4. `M12`를 인용한 문장이 **하나도 없으면** `weakest_tweet: null` + `unrepresented: true`. 이는 펜의 실패가 아니라 **블루프린트가 표적으로 선언했으나 본문에 배치되지 않은 경우**이며, 소견과 체크포인트 2에 별도 항목으로 올린다.

**`score.json` 구조** (`60-probe/<variant>/score.json`):

```jsonc
{
  "schema": "probe-score/v0",
  "run_id": "openai-us20260147854a1-cim-fp",
  "variant": "v2",
  "probe_n": 5,
  "input_digest": "sha256:...",
  "question_set_digest": "sha256:...",
  "delivery_fidelity": 0.78,               // per_target hit_rate의 비가중 평균
  "per_target": [
    { "material_id": "M12", "kind": "fact", "method": "deterministic",
      "hit_rate": 1.0, "weakest_tweet": null, "unrepresented": false },
    { "material_id": "M19", "kind": "implication", "method": "model",
      "hit_rate": 0.4, "weakest_tweet": 6, "unrepresented": false },
    { "material_id": "M31", "kind": "positioning", "method": "model",
      "hit_rate": 0.0, "weakest_tweet": null, "unrepresented": true }
  ],
  "restatement": { "aligned": 4, "drifted": 1, "inverted": 0 },
  "invalidated_answers": [ { "probe_id": "p2", "question_id": "Q7", "reason": "quoted_span-not-substring" } ],
  "notes": "..."
}
```

- `delivery_fidelity`는 표적 간 **비가중 평균**이다(v0). 표적별 중요도 가중은 굿하트 유인을 키우므로 도입하지 않는다.
- `score.json`에는 **판정 필드가 없다**(`decision`·`pass`·`verdict` 키 금지, 스키마 `additionalProperties: false`). §5.7의 기계적 집행이다.

### §5.5 계기 교정(판별력)

계기는 자기 자신이 검증 대상이다. 교정 절차는 **회귀 스위트 인프라를 공용**한다(D9, §4.8 참조).

| 표본 | 기대 | 실패의 의미 |
|---|---|---|
| golden(출하 확정본) | `delivery_fidelity` 높음 | 정상 산출물에서 낮으면 프로브가 과민 |
| mutated(변조본, 특히 `smuggled-claim-in-narrative`·`ungrounded-number`) | 낮음 | 변조본에서 높으면 프로브가 무감 |

- 판정: 같은 질문지·같은 n으로 golden/mutated 쌍을 돌려 **golden 점수 > 변조 점수**를 확인한다. 미분리(부호가 뒤집히거나 같음) = **프로브 재설계 신호**이며, 프로브를 유지한 채 점수만 해석하는 것을 금지한다.
- 산출: `ledgers/regression/calibration/probe-<probe_version>.json`(표본별 점수·쌍별 차이·판정). 계기 코드나 질문 생성 규칙을 수정할 때마다 재실행한다.
- 변조본 중 **전달 충실도와 무관한 유형**(`ticker` 등 L0가 잡는 것)은 교정 표본에서 제외한다. 계기가 게이트의 일을 대신 하는지를 재면 두 장치의 관할이 섞인다(D7).

> [OPEN] 판별력의 최소 마진(golden − mutated 점수 차의 하한)을 수치로 고정할지. 추천: v0은 수치 임계 없이 **부호만** 확인하고(golden > mutated), 3개 런의 교정 데이터가 쌓인 뒤 Owner 재정으로 하한을 입법한다. 근거 없는 임계를 미리 박으면 그 자체가 굿하트 표적이 된다(D15).

> [OPEN] 채점자 레인의 모델 지정. 헌장은 "Haiku가 아닌 별도 채점자"까지만 정한다(D9). 추천: 결정론 경로는 코드, 모델 채점 경로는 펜·프로브와 다른 벤더 또는 다른 티어(예: 교차벤더 1대)로 두어 프로브와 채점자가 같은 편향을 공유하지 않게 한다.

### §5.6 소견(Fable)

소견 = `65-critique/<variant>/memo.md`, 담당 = Fable(D9). 게이트 L2의 비평 메모와 같은 위상(자문·거부권 없음)이며, 계기 데이터를 읽는다는 점이 다르다.

관점 3종(고정):

| 관점 | 묻는 것 | 근거 자료 |
|---|---|---|
| 훅 조응 | T1의 투자자 질문이 본문의 답과 같은 질문인가(D3) | 블루프린트 훅 선언 + 출하 후보 |
| 안도감 착지 | 착지 트윗이 안도감으로 끝나는가, 인용·스크린샷의 표적이 되는가(D2·D11) | 출하 후보 |
| 도슨트 보이스 | 관람객을 미술사학자로 만들려 하지 않는가(D1) | 출하 후보 + 앵커 원장 표본 |

규율:

- **점수 발행 금지**(D15). 등급·별점·10점 만점·백분율 어느 형태도 금지하며, `memo.md`는 L2와 동일한 점수 금지 린트를 통과해야 한다(§2.5 참조).
- 계기 데이터는 **관측치로 인용**한다("M19 도달률 0.4, 최약 트윗 6")가, 소견은 그 수를 올리라는 지시를 쓰지 않는다. 소견이 쓰는 것은 "왜 그 지점에서 막히는가"에 대한 서술이다.
- 소견은 대체 문장을 쓰지 않는다(게이트는 직접 글을 고치지 않는다 — D8의 관할선을 자문 층에도 동일 적용).
- 소견은 체크포인트 2 봉투에 첨부되어 Owner 재정의 입력이 된다(D9).

### §5.7 계기의 권한

**계기와 소견에는 거부권이 없다.** 구속력 있는 결정은 Owner 재정(체크포인트 2)뿐이다(D7·D9).

`delivery_fidelity`가 게이트 임계가 되지 않는 이유:

1. **관할 밖**(D7). 게이트의 관할은 정답이 존재하는 범위다. 전달 충실도는 "정답이 있는 대조"가 아니라 대리 모델의 행동에서 추정한 **추정량**이다. 추정량을 거부권 있는 규칙으로 승격시키는 순간 게이트는 정답 없는 영역으로 한 뼘 넓어진다.
2. **굿하트**(D15). 임계가 생기면 파이프라인의 유일한 합리적 전략은 프로브가 잘 답하는 글을 쓰는 것이 된다. 그것은 공유 충동(D2)이 아니라 프로브 친화 문체의 최적화다. 점수 추격 루프 금지가 헌장의 일반 원칙이다.
3. **최종 심급 분리**(D15). 최종 판정은 점수와 수정 이력을 모르는 별도 심급이 한다. 계기 점수가 상류 루프를 돌리면 이 분리가 무의미해진다.

기계적 집행:

| 집행 지점 | 방식 |
|---|---|
| `score.json` | 스키마에 `decision`·`pass`·`verdict`·`gate_*` 키 부재 + `additionalProperties: false` |
| `verdict.json` | 게이트 판정 산출은 `60-probe/`·`65-critique/`를 입력으로 읽지 않는다(스테이지 계약 `must_not_read`) |
| 루프 제어 | 계기 결과는 `compose` 재리비전을 트리거하지 못한다. 트리거 권한은 L0·L1 결함과 L2 메모 1회뿐(D8) |
| 펜 프롬프트 | 계기 점수를 펜에게 목표로 제시하지 않는다 |
| 최종 심급 | `gate.final-eyes` 레인의 입력에서 `score.json`·`memo.md` 제외 |

### §5.8 계기 유효성 점검

계기가 실제 세계와 아무 관계가 없을 가능성을 상시 열어 둔다(D13).

- **점검 단위 = 배치**(복수 런). 각 런의 `delivery_fidelity`와 72h 실반응(상대 성과 백분위, `ledgers/metrics.jsonl`)의 순위 상관을 계산한다. 원시 조회수는 쓰지 않는다(D13).
- 산출: `ledgers/regression/calibration/instrument-validity-<batch>.json` — 표본 목록·상관계수·해석 메모.
- **무상관이면 프로브를 재설계한다**(D13). 재설계 대상은 프로브 과제·질문 파생 규칙·채점 경계선이며, 점수 산식만 손보는 것은 재설계가 아니다.
- 주의: 이 점검은 계기의 유효성을 재는 것이지, 실반응을 예측하는 모델을 만드는 것이 아니다. 상관이 높다고 해서 계기가 게이트로 승격되지는 않는다(§5.7).
- 표본 부족 구간(런 수가 적은 초기)에는 상관을 계산하지 않고 관측치만 누적한다. 소표본 상관에 반응해 프로브를 흔드는 것이 무상관보다 위험하다.

> [OPEN] 유효성 점검의 배치 크기와 상관 임계. 추천: 배치 = 런 10건, 지표 = Spearman ρ, v0에서는 임계 없이 부호와 산점도만 Owner에게 보고하고, 데이터가 쌓인 뒤 "재설계 발동 조건"을 재정으로 입법한다.

---

## §6 리포 디렉토리 레이아웃

### §6.1 전체 트리 (고정)

```
patent-docent/
  CLAUDE.md                  # 세션 작업 규약 (reader-version 상호 체크 규율 명문화 — D14)
  README.md
  docs/
    CHARTER.md               # 헌장 정본 (D1~D15) — 최상위
    SPEC.md                  # 본 스펙
    decisions/               # Owner 재정 로그. 파일명 D-YYYYMMDD-nn-<slug>.md
    lessons/                 # 사후 교훈
  contracts/
    pipeline.yaml            # 스테이지 그래프·체크포인트·프로필
    stages/*.yaml            # 스테이지별 I/O 계약 (파일명 = 스테이지 id)
    schemas/                 # docent 전용 스키마 (JSON Schema draft 2020-12)
      annotation.schema.json
      thread.schema.json
      blueprint.schema.json
      gate-report.schema.json
      probe-report.schema.json
    lexicon/
      forbidden.yaml         # 금지 어휘 정본 (등재는 Owner 재정으로만)
      defect-catalog.yaml    # 결함 카탈로그 (등재는 Owner 재정으로만)
    invariants.md
    glossary.md
  reader/                    # ★ 이식 단위 (historian과 공유하는 독해층)
    READER-VERSION           # semver 한 줄
    README.md
    schemas/
      material-spec.schema.json   # ★ 두 프로젝트 간 계약 (단일 진원)
    procedure/               # D5 5단계 독해 절차 문서·프롬프트
    lib/                     # 결정론 검사 유틸 (verbatim·포인터 해소·수렴)
  engine/                    # docent 전용 러너·게이트·strip·프로브
  studio/                    # 도면 렌더 (HTML/CSS/SVG + 헤드리스 Chromium)
    templates/
    tokens/
  ledgers/
    anchors/                 # 앵커 원장 (D13)
    regression/              # 회귀 원장 (D13·D8 메타)
      golden/
      mutated/
      cases.jsonl
    tournament.jsonl         # 펜 토너먼트 기입 (D10)
    metrics.jsonl            # 72h 수동 입력 (D13)
    corrections.md           # 교정 원장 (D12 선택·기각 이유)
  runs/<run-id>/             # 런별 산출물
  tests/
  tools/                     # check_reader_version.py 등 개발자 도구
```

이 레이아웃의 경계는 네 개의 서로 다른 논리로 그어져 있다.

| 경계 | 가르는 기준 | 근거 |
|---|---|---|
| `reader/` ↔ `engine/` | historian이 그대로 쓸 수 있는가 | D14 (이식 단위) |
| `contracts/` ↔ 코드 | Owner 재정으로 입법된 문언인가 | D7 (게이트 관할권) |
| `ledgers/anchors/` ↔ `ledgers/regression/` | 독자 반응이 지배하는가 | D13 (두 장부) |
| `studio/` ↔ `engine/` | 미감 판정(Owner 선택)이 필요한가 | D12 (템플릿 스튜디오) |

### §6.2 `reader/`가 이식 단위라는 것의 의미

**재료 명세 스키마의 정본이 `reader/schemas/material-spec.schema.json`에 사는 이유는 단 하나다: 이식 단위가 자기 계약을 들고 간다.** 스키마가 `contracts/schemas/`에 있으면 historian은 코드는 복사하고 계약은 못 가져가거나, docent 전용 스키마 뭉치까지 통째로 끌고 가야 한다. 계약과 검사기가 한 디렉토리에서 함께 이동해야 "재료 명세 N개를 모아 교차 분석"이라는 historian의 정의(D14)가 성립한다.

**단일 진원 원칙**: `contracts/schemas/`에는 재료 명세 스키마의 사본을 두지 않는다. docent 전용 스키마(annotation·thread·blueprint·gate-report·probe-report)만 둔다. 사본이 생기면 두 파일이 갈라지는 것은 시간 문제이며, 그때 갈라진 쪽이 "계약"인지 아무도 모른다.

**이식 판별식(4문 1투표).** 새 파일을 `reader/`에 둘지 판단할 때 순서대로 묻는다.

1. **historian이 이 파일을 수정 없이 쓸 수 있는가?** 아니오 → `engine/`.
2. **이 파일이 출력 채널을 아는가?**(X 스레드·트윗 길이·EN·해시태그·이미지 수) 예 → `engine/`.
3. **이 파일이 재료 명세를 생산·검증·기술하는가?** 예 → `reader/` 후보.
4. **이 파일이 Owner 체크포인트·펜·게이트·계기를 아는가?** 예 → `engine/`.

**타이브레이크**: 애매하면 `engine/`에 둔다. 나중에 `reader/`로 승격하는 것은 값싸고(파일 이동 + MINOR 버전 증가), 잘못 이식된 파일을 회수하는 것은 비싸다(상대 리포에 이미 퍼진 계약을 되돌려야 한다).

배치 예시:

| 대상 | 위치 | 판별 |
|---|---|---|
| `material-spec.schema.json` | `reader/` | 계약 그 자체 (D14) |
| verbatim·포인터 해소·커버리지·수렴 검사기 | `reader/lib/` | 특허 독해 일반의 검사, 채널 무지 (D6 규율 ③) |
| D5 5단계 절차 문서·프롬프트 | `reader/procedure/` | 독해론은 특허 일반 (D5) |
| 수치 정규화 표 | `reader/lib/` | 재료의 `fact.value_normalized` 생성 규칙 = 계약의 일부 |
| drop 신호 **판정 기준** | `engine/` | "안도감이 나올 수 있는가"는 도슨트 독자상 의존 (D2·D4) |
| drop 신호 **스키마 필드**(`drop_signal`) | `reader/` | 필드는 계약, 채우는 기준은 소비자 몫 |
| 주석층 문법·strip | `engine/` | 스레드 채널 의존 (D8·D11) |
| 프로브·채점자 | `engine/` | 전달 충실도 = 도슨트 독자상 의존 (D9) |
| 게이트 L0 규칙 | `engine/` | 트윗 규격 의존 (D11) |
| 블루프린트 스키마 | `contracts/schemas/` | docent 전용 |

`drop_signal` 행이 경계선의 성격을 잘 보여준다: **스키마 필드는 계약에 남고, 그 필드를 어떤 기준으로 채우는지는 소비 프로젝트가 정한다.** historian은 같은 필드를 "교차 분석 가치 없음" 같은 자기 기준으로 채울 수 있다.

### §6.3 `READER-VERSION` · `PORTED-FROM.md` · 상호 체크

**semver 정책** (`reader/READER-VERSION`, 한 줄 `MAJOR.MINOR.PATCH`):

| 증가 | 조건 | 예 |
|---|---|---|
| MAJOR | 재료 명세의 하위호환 파괴 | 필수 필드 추가·삭제, 필드 의미 변경, `kind` 삭제, ID 규율 변경 |
| MINOR | 하위호환 확장 | optional 필드 추가, 새 `kind` 추가, 새 결정론 검사 추가 |
| PATCH | 계약 불변 | 검사기 버그 수정, 절차 문서 문구, 프롬프트 조정, 정규화 표의 별칭 추가 |

- 스키마 문자열 `schema: "material-spec/vN"`의 `N`은 **MAJOR와 연동**한다. MAJOR 증가 없이 `vN`이 바뀌거나 그 반대는 계약 위반이다.
- 런 산출물의 `reader_version`은 **생산 시점 값**을 기록한다. 동결본(`15-frozen/`)에 박힌 값은 이후 어떤 이유로도 갱신하지 않는다 — 그 재료가 어떤 계약 아래 만들어졌는지가 사후 감사의 기준점이다.
- MAJOR 증가는 historian 쪽 동시 상신 사안이다(§6.3 말미 프로토콜).

**`PORTED-FROM.md` 서식** (수신 측 리포의 `reader/PORTED-FROM.md`. docent가 원천일 때 docent에는 이 파일이 없다):

```yaml
# PORTED-FROM
source_repo: patent-docent
source_url: <git remote url>
source_commit: <40-hex full sha>     # 핀. 축약 sha 금지
source_path: reader/
reader_version: 0.1.0
schema_digest: sha256:...            # material-spec.schema.json 의 해시
ported_at: 2026-08-17
ported_by: <세션/작업자 식별>
local_modifications: none            # none 이 아니면 그 즉시 divergence
```

- `local_modifications`가 `none`이 아닌 상태는 **이식본이 갈라졌다는 선언**이다. 이 상태에서 재료 명세를 주고받는 것은 계약 위반이며 Owner 상신 사안이다.
- 재이식 시 이 파일을 덮어쓰지 않고 이력 블록을 **추가**한다(누가 언제 어느 커밋에서 가져왔는지가 사료다).

**`tools/check_reader_version.py` 상호 체크 프로토콜** (D14):

| 검사 | 내용 | 실패 시 |
|---|---|---|
| C1 | `READER-VERSION`이 유효 semver | exit 2 (입력 오류) |
| C2 | 스키마 파일 실제 digest ↔ `PORTED-FROM.schema_digest` | exit 3 (drift) |
| C3 | 로컬 `READER-VERSION` ↔ 상대 리포 `READER-VERSION` | exit 3 (drift) |
| C4 | `schema: material-spec/vN`의 N ↔ 로컬 MAJOR | exit 3 |
| C5 | 진행 중 런들의 `run.yaml.reader_version` MAJOR ↔ 로컬 MAJOR | exit 3 |

- **자동 동기화 금지**(D14). 이 도구에는 `--fix`·`--sync` 플래그를 **두지 않는다**. 플래그의 부재가 규율의 집행이다. drift 감지 시 출력은 차이 요약 + "Owner 상신 필요" 문구 + exit 3이며, 도구는 어떤 파일도 쓰지 않는다(read-only).
- 실행 시점: (a) `reader/` 수정 전후 (b) 재료 명세를 주로 사용하는 작업 착수 시 (c) 런 개시 시 러너가 자동 호출.
- 이 규율은 리포 `CLAUDE.md`에 명문화한다(D14 명시 요구).
- 구현 규약: `assert` 금지, 명시 비교 + 종료 코드(§8.3).

### §6.4 `contracts/lexicon/` — 등재는 재정으로만

`forbidden.yaml`(금지 어휘)과 `defect-catalog.yaml`(결함 카탈로그)은 **입법된 규칙**의 서식지다(D7의 정답 서식지 ②). 기계는 문언만 집행하고 법의 정신을 외삽하지 않는다. 따라서 **등재·완화·삭제는 전부 Owner 재정으로만** 한다(D7·D15).

**등재 절차**:

| 단계 | 행위자 | 산출 |
|---|---|---|
| 1. 후보 발생 | 게이트 flag / 소견 / 교정 원장 / 사후 교훈 | 후보 근거 링크 |
| 2. 상신 | 세션 | 재정 요청(패턴·근거·오탐 위험·범위) |
| 3. 재정 | **Owner** | `docs/decisions/D-YYYYMMDD-nn-<slug>.md` |
| 4. 등재 | 세션 | `lexicon/*.yaml` 항목 + `decision:` 필드 |
| 5. 회귀 케이스 추가 | 세션 | `ledgers/regression/` 변조본 1건 + `cases.jsonl` 행 |

5단계가 필수인 이유: 카탈로그 항목이 검출기를 실제로 발동시키는지 증명되지 않으면 죽은 문자가 된다. "알려진 나쁨만 차단한다"(D7)는 그 나쁨이 실제로 차단됨을 상시 증명해야 성립한다.

**`forbidden.yaml` 서식**:

```yaml
version: 3
entries:
  - id: fx-012
    kind: regex
    pattern: '(?i)\bprice target\b'
    applies_to: [thread.body]        # thread.body | thread.tail | all
    decision: D-20260817-01-forbidden-price-target   # ★ 필수. 없으면 스키마 위반
    rationale: "D3 투자 결론 금지의 문언화"
    added: 2026-08-17
    regression_case: rc-041          # ★ 필수. 검출 증명 케이스
```

**`defect-catalog.yaml` 서식**: 위와 동일 골격 + `detector`(어느 층이 잡는가: `L0` | `L1`) + `example`(걸려야 하는 문장) + `counter_example`(걸리면 안 되는 문장). `counter_example`이 오탐 회귀를 막는다.

**기계적 집행**: 두 파일의 스키마는 `decision`과 `regression_case`를 필수로 요구한다. 재정 없이 추가된 항목은 스키마 검증에서 떨어진다. "재정으로만"이 사람의 기억이 아니라 파서에 의해 지켜진다.

**재정 로그 서식**(`docs/decisions/D-20260817-01-forbidden-price-target.md`):

```
# D-20260817-01 — forbidden.yaml 등재: price target
date: 2026-08-17
decided_by: Owner
type: lexicon.forbidden
target_file: contracts/lexicon/forbidden.yaml
entry_id: fx-012
근거: <flag/메모/교훈 링크>
오탐 위험: <검토 요지>
effective_from: gate_version 1.3
```

### §6.5 `ledgers/` — 두 장부의 분리

두 장부는 **지배 원리가 다르다**(D13). 같은 디렉토리에 섞으면 인기 없는 표본을 정리하다 회귀 커버리지가 무너진다.

| 축 | `ledgers/anchors/` | `ledgers/regression/` |
|---|---|---|
| 표본의 뜻 | "좋은 글"(보이스·취향) | "올바른 산출물" |
| 지배 | 독자 반응 | 독자 반응과 **무관** |
| 물갈이 | fade-out 있음(보관 전환) | **인기로 물갈이 금지** |
| 성장 | 조정형 | 거의 추가 전용 |
| 확정 권한 | Owner 재정 | Owner 재정 |

**앵커 원장** — `ledgers/anchors/anchors.jsonl` + `ledgers/anchors/texts/<anchor_id>.md` + `ledgers/anchors/archive/`(fade 확정분 이동).

```jsonc
{ "anchor_id": "A-0007", "run_id": "openai-us20260147854a1-cim-fp", "variant": "v2",
  "pen": { "vendor": "anthropic", "model": "opus-5", "effort": "max" },
  "text_path": "ledgers/anchors/texts/A-0007.md",
  "posted_at": "2026-08-20T09:00:00Z",
  "state": "provisional" ,                 // provisional | active | faded
  "weight": 0.5,                            // 잠정 입장 가중치
  "performance": { "snapshot_h": 72, "window_n": 20,
                   "percentile": 0.62, "metric": "relative_to_rolling_median" },
  "owner_selected": true,
  "market_divergence": false,               // Owner 선택 변주가 시장에서 죽은 경우 true
  "fade": { "proposed_at": null, "reason": null, "decision": null },
  "regression_case_id": null }
```

규율:

- **원시 조회수 금지**(D13). 레코드 스키마에 `views`·`impressions`·`likes` 같은 절대량 필드를 두지 않는다(`additionalProperties: false`). 원시값은 `ledgers/metrics.jsonl`(72h 수동 입력)에만 존재하고, 앵커 원장은 그로부터 계산된 **백분위**만 받는다.
- **콜드 스타트**: `window_n < 10`이면 fade 제안기가 무조건 no-op이며 전원 잔류한다.
- **fade-out은 자동 제안 → Owner 재정 확정**. `fade.proposed_at`은 기계가 쓰고, `fade.decision`(재정 파일 ID)이 채워져야 `state: faded`로 전이하고 `archive/`로 이동한다. 소재-문체 교란 때문에 자동 확정은 금지다(D13).
- fade는 **삭제가 아니라 보관 전환**이다. `texts/`의 본문은 지우지 않는다.
- `market_divergence: true`(Owner 취향과 시장의 괴리)는 고급 데이터로 보존한다. 앵커에서는 독자가 이긴다(D13).

**회귀 원장** — `ledgers/regression/cases.jsonl`(§2.5 참조) + `golden/` + `mutated/` + `calibration/`.

- 각 golden 표본은 **자족 스냅샷**이다: `golden/<golden_id>/thread.annotated.md` + `material-spec.frozen.json` + `blueprint.json` + `meta.json`. 런 폴더가 프루닝돼도(§7.7) 회귀 스위트는 단독으로 재현 가능해야 한다.
- 추가 전용에 가깝다. 삭제는 "그 결함 유형이 더 이상 결함이 아니다"라는 재정을 요구한다.

**한 글이 두 장부에 동시 등재될 때의 표기**(D13):

- 앵커 레코드의 `regression_case_id`, 회귀 케이스의 `anchor_id`로 **상호 참조**한다. 본문 사본은 각 장부가 따로 보유한다(참조로 연결하면 한쪽 정리가 다른 쪽을 깨뜨린다).
- **상태는 독립**이다. 앵커에서 `faded`가 되어도 회귀 케이스는 그대로 살아 있다. 기계적 집행: fade 절차는 `ledgers/regression/` 하위에 **쓰기 권한이 없다**.
- 불변식(`contracts/invariants.md`에 등재): "앵커 원장의 어떤 상태 전이도 회귀 원장의 표본 수를 줄이지 않는다."

> [OPEN] fade-out 자동 제안의 발동 규칙(백분위 하한과 연속 횟수). 추천: `percentile < 0.25`가 **2회 연속** 관측된 앵커만 제안 대상으로 올리고(단 `window_n ≥ 10`), 최종 확정은 배치 리뷰의 Owner 재정. 초기 가중치·가중치 조정 폭도 같은 재정에서 함께 입법할 것을 제안한다.

### §6.6 `studio/` — 이번 발주 범위 밖

`studio/`는 도면 렌더의 서식지이며, **템플릿 스튜디오는 부트스트랩 후 별도 발주다**(D12). 이번 발주는 디렉토리 자리와 아래 규율의 기록까지이고, 템플릿·디자인 토큰의 저작은 포함하지 않는다.

| 항목 | 내용 | 근거 |
|---|---|---|
| 렌더 스택 | HTML/CSS/SVG 조판 → 헤드리스 Chromium → PNG **1200**×675 @2x(16:9 피드 안전 크롭) | D12 |
| 금지 | **matplotlib 금지** — 미감 천장 실증(구 차트 산출물 만족도 저조) | D12 |
| 별도 발주 | 3종 템플릿(도면 주석판/개념 다이어그램/수치 카드) × 시안 3안, Owner 선택 1~2라운드 후 토큰+CSS 동결 | D12 |
| 상비 | **폴백(원본 크롭 + 최소 주석)** — 정직성 장치. 폴백이 연승하면 시각 정체성 폐기를 데이터로 재정한다 | D12 |
| 팔레트 | 다크+앰버(#171A21 / #D19730)는 후보 중 하나일 뿐, 확정 아님 | D12 |
| 기록 | 선택·기각과 그 이유는 `ledgers/corrections.md`(교정 원장)에 | D12 |

**이번 발주에서 구현되는 것은 폴백 경로뿐이다**(M9, §8.4 참조). 폴백만으로 첫 런의 도면 자산이 완결되어야 하며, 템플릿이 도착하지 않아도 파이프라인이 멈추지 않는다. 이것이 폴백 상비가 "정직성 장치"인 두 번째 의미다 — 시각 정체성이 없어도 출하가 가능해야 그 정체성의 가치를 데이터로 잴 수 있다.

`studio/tokens/`는 동결 대상 산출물의 자리다(동결 후 수정은 재정 사안). `studio/templates/`는 시안이 도착하기 전까지 폴백 템플릿 1종만 갖는다.

---

## §7 런 산출물 레이아웃

### §7.1 런 ID 규칙

`<assignee-slug>-<pubnum>-<topic-slug>` (예: `openai-us20260147854a1-cim-fp`).

| 부분 | 규칙 |
|---|---|
| `assignee-slug` | 출원인 약칭, 소문자 `[a-z0-9]+` |
| `pubnum` | 공개·등록번호를 소문자화하고 구분자 제거(`US 2026/0147854 A1` → `us20260147854a1`) |
| `topic-slug` | 2~3 단어, 하이픈 연결. 소재의 각도를 나타낸다 |

- 전체 정규식: `^[a-z0-9]+-[a-z0-9]+-[a-z0-9-]+$`
- 같은 특허를 다른 각도로 다시 다루면 `topic-slug`가 달라지므로 충돌하지 않는다. 그래도 충돌하면 `-2` 접미를 붙인다.
- 런 ID는 생성 후 **불변**이다. 재료 명세·주석층 프런트매터·장부 레코드가 이 문자열을 참조한다.

### §7.2 트리 (고정)

```
runs/<run-id>/
  run.yaml                 # 런 메타: 특허 식별자·엔진 커밋·reader_version·펜 배정·숫자 화이트리스트
  00-source/
    patent.md              # 원천 정본
    patent.sha256          # 원천 다이제스트
    figures-raw/
  10-read/
    material-spec.json     # 작업본 (status: draft)
    material-spec.md       # KR 인간 판독 렌더 (체크포인트 1 표면)
    claim-trees/           # D5 ①② 중간 산출물
    grounding.md           # D5 ③
    positioning.md         # D5 ⑤
    drop-signal.md         # D4 2단 신호
    convergence.json       # 재독해 수렴 검사 결과
  15-frozen/
    material-spec.v<N>.json  # 동결본 (읽기 전용)
    approval-v<N>.md         # 체크포인트 1 봉투
  20-design/
    blueprint.json
    blueprint.md           # KR 요약
  30-figures/
    assets/                # ★ 전량 편집본 (1급 보존) fig-NN.png + manifest.json
    selection.json         # 포인터만
  40-compose/<variant>/
    thread.annotated.md
    material-defect.md     # (선택) 재료 반려서
  50-gate/<variant>/
    l0.json l1.json l2.md verdict.json     # verdict.json 안에 final_eyes 객체 (§1.10, §9.0 E6)
    thread.stripped.md     # ★ strip 산출 = 출하 후보 텍스트. probe·critique·final-eyes가 소비 (§9.0 E5)
    annotation-index.json  # 트윗→문장→인용 ID 맵 (strip 산출, 계기 국소화가 소비 — §2.4 참조)
    revisions/r<n>/        # 국소 수정 지시·결과
  60-probe/
    questions.json         # 표적 질문지 (런 단위 — §5.2)
    <variant>/probe-<i>.json score.json
  65-critique/<variant>/
    memo.md
  70-ship/
    thread.md thread.json images/ checkpoint2.md
  90-feedback/
    metrics-72h.json retro.md
```

번호에 간격을 둔 이유: 스테이지 삽입 여지.

### §7.3 `run.yaml` 필드 명세

```yaml
schema: run/v0
run_id: openai-us20260147854a1-cim-fp
created_at: 2026-08-18T02:10:00Z
status: active            # active | halted | shipped | abandoned

patent:
  number: US20260147854A1
  title: "..."
  assignee: "..."
  dates: { priority: 2024-11-05, filing: ..., publication: ... }
  source_path: 00-source/patent.md
  source_sha256: sha256:...        # patent.sha256 과 일치해야 함 (러너가 대조)

engine:
  commit: <40-hex>                 # 런 개시 시점 엔진 커밋 핀
  gate_version: "1.2"
reader_version: 0.1.0              # 런 개시 시점 reader/READER-VERSION 사본

pens:                              # D10 펜 토너먼트 배정
  - { variant: v1, vendor: anthropic, model: opus-5, effort: high }
  - { variant: v2, vendor: anthropic, model: opus-5, effort: max }
  - { variant: v3, vendor: openai,    model: gpt-5.6-sol, effort: high }

probe: { n: 5, model: haiku-... }
gate:  { k: 3, revision_cap: 3 }
figures: { render: fallback }      # fallback | studio

numeric_whitelist:                 # ★ §4.4(숫자 전수 대조)가 소비
  - { pattern: '^\d{1,2}/\d{1,2}$', reason: "스레드 순번 n/N", approved_in: approval-v1.md }
```

**숫자 화이트리스트 규율**: 화이트리스트는 L0 `numeric.exhaustive`(D8)를 합법적으로 우회하는 유일한 통로이므로, 항목은 **패턴 + 사유 + 승인 근거**를 모두 갖는다. 목록은 체크포인트 1 승인 봉투에 첨부되어 Owner 승인 대상이 되고, 이후 추가되는 항목은 체크포인트 2 전에 재승인을 받는다. 사유 없는 항목은 스키마 검증에서 떨어진다.

**핀 3종의 의미**: `source_sha256`(무엇을 읽었는가) · `engine.commit`(어떤 기계가 만들었는가) · `reader_version`(어떤 계약 아래 만들었는가). 사후에 산출물의 이상을 추적할 때 이 세 핀이 좌표계다.

### §7.4 디렉토리 소유권 표

**불변식**: 한 경로에는 **쓰기 소유자가 정확히 하나**다. 하류 스테이지는 상류 경로에 쓰지 않는다(D6 규율 ② 단방향). 러너는 스테이지 실행 시 write-scope를 검사하고 위반을 halt로 처리한다. (스테이지별 I/O 상세 계약은 §1 소관 — 여기서는 소유권만 고정한다.)

| 경로 | 쓰기(단일 소유) | 읽기 |
|---|---|---|
| `run.yaml` | `source`(생성), 러너(상태 필드만) | 전 스테이지 |
| `00-source/` | `source` | 전 스테이지 |
| `10-read/` | `read` | `freeze`, Owner(CP1) |
| `15-frozen/` | `freeze` | `design`·`figures`·`compose`·`gate`·`probe`·`critique`·`ship` |
| `20-design/` | `design` | `figures.select`·`compose`·`gate`·`probe`(질문 파생) |
| `30-figures/assets/` | `figures.prepare` | `figures.select`·`ship` |
| `30-figures/selection.json` | `figures.select` | `compose`·`ship` |
| `40-compose/<variant>/` | `compose`(해당 변주 펜) | `gate`·`ship` |
| `50-gate/<variant>/` | `gate` | `compose`(수정 지시 수령)·`probe`(annotation-index)·`ship`·Owner(CP2) |
| `60-probe/` | `probe` | `critique`·Owner(CP2) |
| `65-critique/<variant>/` | `critique` | Owner(CP2) |
| `70-ship/` | `ship` | `feedback`·장부 |
| `90-feedback/` | `feedback` | 장부 |

파생 규칙:

- 변주 디렉토리는 **변주 간에도 격리**된다. `compose` 레인 v2는 v1의 초안을 읽지 않는다(공정 비교 — D10).
- `gate`·`probe`·`critique` 레인은 `40-compose/`에 쓰기 권한이 없다. 게이트는 어떤 경우에도 직접 글을 고치지 않는다(D8).
- `gate` 산출은 `60-probe/`·`65-critique/`를 읽지 않는다(계기·소견의 무권한 — §5.7).

### §7.5 자산층 보존 규율 (D12)

**`30-figures/assets/`는 전량 편집본의 1급 보존처이고, `selection.json`은 포인터만 갖는다.**

- `figures.prepare`는 원천 도면을 **전량** 편집해 `assets/fig-NN.png` + `manifest.json`을 만든다. 선택 여부와 무관하다.
- `selection.json`은 `{ "slots": [ { "tweet": 1, "asset": "fig-03", "role": "hero" } ] }` 형태의 **포인터 집합**이며, 이미지 데이터를 담지 않는다.
- 선택이 바뀌어도 편집을 다시 하지 않는다. 포인터만 바뀐다.
- `assets/`의 파일은 런 수명 동안 **삭제·덮어쓰기 금지**. 재편집이 필요하면 새 파일(`fig-03.r2.png`)을 추가하고 manifest에 이력을 남긴다.

`manifest.json` 항목: `{ figure_id, source_raw_path, asset_path, sha256, renderer, template, fallback: true|false, edits: [...], rendered_at }`.

**교훈 승계 명시**: 이 규율은 구 프로젝트에서 **선택분만 편집**했다가 (a) 선택이 바뀔 때마다 편집으로 되돌아가는 왕복이 발생하고 (b) 중간 편집본이 유실되는 사고를 겪은 데서 온다(D12, 구 v3 C17 승계). "전량 선편집 + 자산층 보존 + 출하 선택은 포인터만"은 그 왕복을 구조적으로 없앤다. 도면이 핵심 자산이라는 전제(독자는 글보다 이미지부터 본다 — D12) 아래에서, 자산층 유실은 런 전체의 손실이다.

### §7.6 동결 디렉토리 `15-frozen/`의 불변 규율

체크포인트 1의 승인이 찍힌 재료가 이후 모든 판정의 정답지다(D6). 정답지가 움직이면 게이트·계기·감사 전부가 무의미해진다.

| 규율 | 내용 | 집행 |
|---|---|---|
| 읽기 전용 | 파일 모드 0444, write-scope는 `freeze`만 | 러너 검사 + 스테이지 계약 |
| 덮어쓰기 금지 | 기존 `material-spec.v1.json` 수정 금지 | 존재 시 freeze는 halt |
| 개정 = 새 파일 | 개정판은 `material-spec.v2.json` **추가** | `spec_version` 단조 증가 |
| 봉투 짝 | 동결본 N개 ↔ `approval-v<N>.md` N개 | 개수 불일치 = 계약 위반 |
| digest 대조 | 주석층 프런트매터 `spec_digest` ↔ 사용한 동결본 해시 | L0 검사 |
| 항목 ID | `M<n>`은 추가 전용, 재사용·재번호 금지(§2.3 참조) | 개정본 검사 |

개정 경로(D6 규율 ②): 펜이 재료 결함을 발견하면 `40-compose/<variant>/material-defect.md`로 **반려**하고, `read`가 명세를 개정한 뒤 새 버전으로 동결하고, 재요리는 새 동결본을 정답지로 다시 시작한다. 펜은 재료를 수정할 권한이 없다.

구 버전 동결본을 인용한 산출물이 남아 있어도 문제되지 않는다 — 그 산출물의 프런트매터가 어느 버전을 썼는지 명시하고, ID가 추가 전용이므로 인용은 계속 해소된다. 다만 `retracted` 항목 인용은 L0 결함이다(§2.5 참조).

### §7.7 런 폴더의 수명·보존 정책

**분류 원리**: 재생성 가능한가. LLM 산출물은 같은 입력으로도 같은 값이 나오지 않으므로 대부분 **재생성 불가**이며, 따라서 대부분이 보존 대상이다. 진짜 캐시는 원천에서 결정론적으로 다시 뽑을 수 있는 것뿐이다.

| 등급 | 대상 | 정책 |
|---|---|---|
| **1급 자산**(영구) | `run.yaml`, `00-source/patent.md`+`patent.sha256`, `15-frozen/*`, `30-figures/assets/*`, `40-compose/*/thread.annotated.md`, `70-ship/*`, `90-feedback/*` | 삭제 금지. 대외 게시물이거나 재생성 불가 |
| **2급 증거**(장기, 압축 가능) | `10-read/`의 중간 산출물, `50-gate/`, `60-probe/`, `65-critique/`, `revisions/` | 감사 증거. 아카이브 압축 허용, 삭제는 재정 사안 |
| **3급 캐시**(재생성 가능) | `00-source/figures-raw/`, 러너 임시 파일·로그 | 원천에서 재추출 가능. 만기 후 프루닝 |

**프루닝 선행 조건**: 회귀 원장에 등재된 런은 표본이 `ledgers/regression/golden/<golden_id>/`에 **자족 스냅샷으로 복제된 뒤에만** 2급·3급 정리 대상이 된다(§6.5). 회귀 스위트가 런 폴더를 참조하는 상태로 두면, 폴더 정리가 곧 게이트 커버리지 붕괴다.

`00-source/patent.md`를 1급으로 두는 이유: 모든 verbatim 검사와 숫자 대조의 기준점이며, 외부 원천이 사라지거나 바뀌어도 이 사본과 그 해시가 있어야 사후 재현이 가능하다.

> [OPEN] 3급 캐시의 만기(며칠 후 프루닝) 및 2급 증거의 압축 시점. 추천: 3급은 출하 후 90일, 2급은 출하 후 180일에 `.tar.zst` 압축(삭제는 하지 않음). 저장 압박이 실제로 관측되기 전에는 만기를 짧게 잡지 않는 편을 권한다 — 초기 런의 증거가 사후 교훈의 유일한 사료다.

---

## §8 모듈 구현 로드맵 M1~M12

### §8.1 의존 그래프와 크리티컬 패스

**크리티컬 패스 ① = M1**(재료 명세 스키마 + 검사기), **② = M2**(READ 스테이지). 이 둘이 늦으면 나머지 전부가 늦는다. 이유는 구조적이다: 재료 명세는 게이트의 정답지(D8)이자 계기의 정답지(D9)이자 historian과의 계약(D14)이므로, 스키마가 흔들리면 하류 세 층이 동시에 흔들린다.

```
[L0]  M1 reader 부트스트랩  ★크리티컬 ①        M3 주석층·strip
        │                                        │
[L1]  M2 READ  ★크리티컬 ②                       │
        │                                        │
[L2]  M4 L0 게이트 + 회귀 스위트  ◄──────────────┘        (M1, M3)
        │
[L3]  M5 DESIGN+COMPOSE (M2,M3)   M9 FIGURES (M2)   M11 historian I/F (M1)
        │
[L4]  M6 L1 (M4,M5)   M7 계기 (M4,M5)   M8 L2·소견 (M5)   M10 SHIP·환류 (M3,M9)
        │
[L5]  M12 오케스트레이션 (M2~M10)
```

간선 목록: `M1→M2`, `M1→M4`, `M1→M11`, `M3→M4`, `M2→M5`, `M3→M5`, `M2→M9`, `M4→M6`, `M5→M6`, `M4→M7`, `M5→M7`, `M5→M8`, `M3→M10`, `M9→M10`, `M2..M10→M12`.

| 모듈 | 내용 | 의존 |
|---|---|---|
| M1 | `reader/` 부트스트랩: material-spec 스키마 v0 + 검증기 + 결정론 검사 4종(verbatim·포인터·커버리지·수렴 비교기) + READER-VERSION | — |
| M2 | READ 스테이지 러너: D5 5단계 절차·중간 산출물·KR 렌더·drop 신호 2단·CP1 봉투·freeze(버전 스탬프·digest) | M1 |
| M3 | 주석층 문법 + strip 파이프라인 + thread.json/annotation-index (무손실 round-trip) | — (M2와 병행 가능) |
| M4 | L0 결정론 게이트 전 규칙 + 회귀 스위트 골격(golden/mutated/cases.jsonl) | M1, M3 |
| M5 | DESIGN 블루프린트 계약(슬롯·transmission_targets·new_terms 선언) + COMPOSE 펜 레인·토너먼트 배정 | M2, M3 |
| M6 | L1 국소 대조(k-반복 다수결) + flag 라우팅 + 루프 위상 제어(캡 3·escalate) + final-eyes 심급 | M4, M5 |
| M7 | 계기: 프로브 A/B + 별도 채점자 + 국소화 + 판별력 교정 | M4, M5 |
| M8 | L2 자문 메모 + 점수 금지 린트 + Fable 소견 | M5 |
| M9 | FIGURES: 전량 편집·자산층·포인터 선택·헤드리스 Chromium 렌더(1200×675 @2x) — 폴백 경로만 | M2 |
| M10 | SHIP + 환류: 출하 패키징·CP2 봉투·72h 수동 입력·앵커/회귀 두 장부·fade-out 자동 제안 | M3, M9 |
| M11 | historian 인터페이스: PORTED-FROM 생성기 + `tools/check_reader_version.py` 상호 체크 | M1 |
| M12 | 오케스트레이션: pipeline.yaml 실행기·상태·재개 | M2~M10 |

### §8.2 첫 런 최소 집합 (MVP cut)

**MVP = M1 · M2 · M3 · M4 · M5 · M9 · M10.**

M6~M8이 빠져도 파이프라인이 성립하는 이유는 그 셋이 전부 **자문 층**이기 때문이다(D7). 게이트의 거부권은 L0(결정론)에만 있고, L1은 거부권이 있으나 그 판정 대상(문장↔인용 정합, `[narrative]` 감사)은 없으면 없는 대로 Owner 검토로 대체 가능하다. L2·계기·소견은 애초에 거부권이 없으므로 부재가 파이프라인을 막지 않는다.

MVP 운영 시의 제약(명시하고 시작한다):

| 제약 | 내용 |
|---|---|
| 거부권 = L0만 | 결정론이 잡을 수 있는 것만 자동 차단된다 |
| `[narrative]` 밀수 미검출 | 서사 신고 뒤에 숨은 기술 주장은 Owner가 CP2에서 직접 본다 |
| 전달 충실도 관측치 없음 | 첫 런은 계기 없이 나간다. 대신 72h 실반응을 원점 데이터로 삼는다 |
| 소견 없음 | 훅 조응·착지 판단은 Owner 재정으로 흡수 |
| 최종 심급 부재 | `gate.final-eyes`는 M6 소관. MVP에서는 Owner가 마지막 눈이다 |

MVP는 **첫 런 1회의 조건**이지 정상 상태가 아니다. M6~M8은 첫 런 직후 착수한다 — 첫 런의 산출물이 곧 회귀·교정 표본의 원점이 되기 때문이다.

### §8.3 검증 규약 (로드맵 전체에 적용)

1. **모듈 테스트는 pytest.** 명령 형식 `pytest tests/test_<module>.py -q`. 전체는 `pytest -q`.
2. **독립 실행 검증 스크립트에서 `assert` 사용 금지.** `python3 -O`에서 assert 문이 전부 제거되어, 망가진 코드가 공허하게 통과한다(2026-08-16 실측). 검증은 **명시 비교 + 종료 코드**로 쓴다.

```python
# 금지
assert got == want

# 규약
if got != want:
    print(f"MISMATCH: got={got!r} want={want!r}", file=sys.stderr)
    sys.exit(1)
```

3. **종료 코드 규약**(`tools/`·러너 검사 스크립트 공통): `0` = 통과, `1` = 검증 실패, `2` = 입력·환경 오류, `3` = drift/상신 필요(자동 수정 없음).
4. **최적화 모드 회귀**: 검증 도구는 `python3 -O`로도 동일한 종료 코드를 내야 한다. M11이 이 동치성을 서브프로세스 테스트로 강제한다(`test_checker_behaves_identically_under_O`).
5. 산출물 스키마 검증은 JSON Schema draft 2020-12로 하고, **금지 필드는 `additionalProperties: false`로 집행**한다(점수 금지·원시 조회수 금지 등 — D15·D13).
6. 회귀 스위트는 "**변조본 검출 실패 = 테스트 실패**"로 설계한다(§8.5).

### §8.4 모듈 명세

각 모듈은 **산출 파일 · 완료 판정(DoD) · 검증 계획**을 갖는다. 검증 계획의 각 행은 "이 테스트가 없으면 무엇이 공허해지는가"를 기록한다.

#### M1 — `reader/` 부트스트랩 ★크리티컬 ①

- **산출**: `reader/schemas/material-spec.schema.json`, `reader/lib/verbatim.py`, `reader/lib/pointers.py`, `reader/lib/coverage.py`, `reader/lib/convergence.py`, `reader/lib/normalize.py`, `reader/READER-VERSION`, `reader/README.md`, `contracts/glossary.md` 초판
- **DoD**
  - §2.3의 예시 인스턴스가 스키마를 통과하고, 결정론 검사 4종을 전부 통과한다.
  - 검사 4종 각각에 대해 **실패해야 하는 변조 인스턴스**가 준비되어 실제로 실패한다.
  - `M<n>` 추가 전용 규율이 개정본 비교 검사로 집행된다.
  - `READER-VERSION` = `0.1.0`, 스키마 문자열 = `material-spec/v0`, 둘의 연동이 검사된다.
  - 수치 정규화 표가 `reader/lib/normalize.py` 한 곳에 있고, 게이트·계기가 이를 import한다(구현 이중화 금지).
- **검증**: `pytest tests/test_m1_reader.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_schema_validates_minimal_instance` | 최소 인스턴스가 거부되면 스키마가 과잉 제약 |
| `test_schema_rejects_unknown_kind` | `kind` 오타가 통과하면 kind 열거가 무의미 |
| `test_verbatim_rejects_single_char_edit` | quote를 한 글자 바꾼 변조본이 통과하면 verbatim 검사가 무의미 |
| `test_verbatim_accepts_exact_substring` | 정상 인용이 거부되면 검사가 실사용 불가 |
| `test_pointer_resolution_detects_dangling_attaches_to` | 존재하지 않는 `attaches_to`가 통과하면 포인터 해소 검사가 무의미 |
| `test_coverage_flags_ungrounded_element` | 접지 없는 청구항 element가 통과하면 커버리지 검사가 무의미 |
| `test_convergence_jaccard_below_threshold_fails` | 0.95 미만 쌍이 pass면 수렴 임계가 집행되지 않음 |
| `test_material_id_append_only_rejects_renumber` | 개정본이 `M7`을 다른 내용으로 재사용해도 통과하면 ID 규율 붕괴 |
| `test_reader_version_matches_schema_major` | 버전과 `material-spec/vN`이 어긋나도 통과하면 semver 정책이 문서로만 존재 |

#### M2 — READ 스테이지 러너 ★크리티컬 ②

- **산출**: `engine/stages/read.py`, `engine/stages/freeze.py`, `reader/procedure/*.md`(D5 5단계 절차·프롬프트), `engine/render/material_spec_md.py`(KR 렌더), `contracts/stages/read.yaml`, `contracts/stages/freeze.yaml`
- **DoD**
  - D5 5단계 각각이 중간 산출물을 남긴다(`claim-trees/`, `grounding.md`, `positioning.md`).
  - drop 신호가 2단(청구항 분해 직후 / 포지셔닝 확정 후)으로 산출된다(D4).
  - `convergence.json`이 독립 2회 실행 비교 결과를 담고, 미달 시 재실행 1회 → 여전히 미달이면 escalate.
  - `material-spec.md`(KR)가 CP1 검토 표면으로 충분하다 — 모든 `M<n>` 항목이 판독본에 나타난다(D6: CP1이 Owner 이해층을 겸한다).
  - `freeze`는 승인 봉투 없이는 실행되지 않으며, 동결본을 0444로 쓰고 digest를 기록한다.
- **검증**: `pytest tests/test_m2_read.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_read_emits_all_five_stage_artifacts` | 중간 산출물 누락이 통과하면 "검증 가능한 중간 산출물" 규율이 공허 |
| `test_read_rejects_source_digest_mismatch` | 원천이 바뀐 채 진행되면 모든 verbatim 검사의 기준점이 붕괴 |
| `test_drop_signal_emitted_at_both_stages` | 1단만 나와도 통과하면 D4 2단 신호가 실효 없음 |
| `test_kr_render_contains_every_material_id` | 판독본이 항목을 빠뜨려도 통과하면 CP1 검토 표면이 불완전 |
| `test_freeze_refuses_without_approval_envelope` | 봉투 없이 동결되면 체크포인트 1이 우회 가능 |
| `test_freeze_stamps_monotonic_spec_version` | 버전이 되감기면 정답지 동일성이 깨짐 |
| `test_freeze_writes_readonly_and_records_digest` | 동결본이 쓰기 가능하면 "동결"이 이름뿐 |
| `test_convergence_failure_escalates_after_one_retry` | 무한 재시도되면 불안정 신호가 은폐됨 |

#### M3 — 주석층 문법 + strip 파이프라인

- **산출**: `contracts/schemas/annotation.schema.json`, `contracts/schemas/thread.schema.json`, `engine/annotation/parse.py`, `engine/annotation/strip.py`, `engine/annotation/index.py`
- **DoD**
  - §2.4 문법(헤더·태그 위치·이스케이프)을 파싱하고, 위반을 `annotation.missing-tag` 등으로 보고한다.
  - strip 5단계가 결정론이며 **무손실 round-trip**이 바이트 동일로 검증된다.
  - `thread.json`(tweets[], images[])과 `annotation-index.json`(트윗→문장→인용 ID)을 산출한다.
  - `annotation-index.json`은 모든 문장을 포함한다(`[narrative]` 문장 포함) — 계기 국소화가 이를 소비한다(D9).
- **검증**: `pytest tests/test_m3_annotation.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_strip_roundtrip_is_byte_identical` | 무손실이 아니면 출하본이 초안의 파생물이라는 보장이 깨짐(D8) |
| `test_missing_tag_is_detected` | 태그 없는 문장이 통과하면 성분 역참조 규율이 공허(D6) |
| `test_tag_must_be_at_line_end` | 위치 자유를 허용하면 파서가 본문 대괄호와 태그를 혼동 |
| `test_escaped_bracket_survives_strip` | 이스케이프가 소실되면 본문이 변조됨 |
| `test_annotation_index_maps_every_sentence` | 누락 문장이 있으면 국소화가 특정 트윗을 영원히 못 지목 |
| `test_header_meta_moves_to_thread_json` | 헤더가 본문에 남으면 출하본이 게시 불가 |
| `test_multiple_figs_parse_and_cap_at_four` | 5장 이상이 통과하면 D11 이미지 상한이 미집행 |

#### M4 — L0 결정론 게이트 + 회귀 스위트 골격

- **산출**: `engine/gate/l0/*.py`(규칙별 모듈), `contracts/schemas/gate-report.schema.json`, `contracts/lexicon/forbidden.yaml`(초기 골격), `contracts/lexicon/defect-catalog.yaml`, `ledgers/regression/{golden,mutated}/`, `ledgers/regression/cases.jsonl`, `engine/regression/run_suite.py`
- **DoD**
  - §2.5의 L0 규칙 전부가 구현되고 각각 최소 1개의 검출 케이스를 갖는다.
  - `numeric.exhaustive`가 M1의 정규화 구현을 재사용한다(별도 구현 금지).
  - `verdict.json`이 스키마를 통과하며 `defect`는 `fix_directive`(지시문)만 갖고 대체 문장을 담지 않는다.
  - lexicon 항목은 `decision`·`regression_case` 필수 필드 없이는 로드되지 않는다(§6.4).
  - 회귀 스위트가 5종 mutation(`hallucinated-claim`·`ticker`·`ungrounded-number`·`smuggled-claim-in-narrative`·`retracted-citation`)을 각 1건 이상 보유한다.
- **검증**: `pytest tests/test_m4_l0_gate.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_tweet_count_out_of_range_rejected` | 6~12 범위가 미집행이면 D11 규격이 문서로만 존재 |
| `test_body_length_bounds_enforced` | 180~260자 규격 미집행 |
| `test_hashtag_and_body_link_rejected` | 해시태그 0·본문 링크 금지 미집행 |
| `test_forbidden_lexicon_regex_hits` | 입법된 문언이 실제로 차단되지 않음 |
| `test_lexicon_entry_without_decision_is_rejected` | 재정 없는 등재가 가능하면 D7·D15가 사람의 기억에만 의존 |
| `test_citation_to_retracted_item_rejected` | 철회 재료 인용이 통과하면 개정 규율이 공허 |
| `test_numeric_exhaustive_catches_ungrounded_number` | 무근거 숫자가 통과하면 숫자 전수 대조가 무의미 |
| `test_numeric_normalization_matches_unit_variants` | 표기 변형이 미매칭되면 오탐으로 게이트가 사용 불가 |
| `test_whitelist_covers_only_declared_patterns` | 화이트리스트가 광범위하면 L0 우회 통로가 열림 |
| `test_regression_suite_detects_all_mutations` | 변조본 하나라도 놓치면 게이트 수정이 안전하지 않음 |
| `test_regression_golden_all_pass` | golden 오탐이 있으면 스위트가 개발을 마비시킴 |

#### M5 — DESIGN 블루프린트 + COMPOSE 펜 레인

- **산출**: `contracts/schemas/blueprint.schema.json`, `engine/stages/design.py`, `engine/stages/compose.py`, `engine/pens/registry.py`, `contracts/stages/{design,compose}.yaml`, `ledgers/tournament.jsonl` 서식
- **DoD**
  - 블루프린트가 슬롯 배치(D11)·`transmission_targets`·`new_terms` 선언을 담고, 모든 재료 ID 참조가 동결본에서 해소된다.
  - 변주들이 **동일한** 동결 재료·블루프린트·도면 선택을 입력으로 받는다(D10 공정 비교).
  - 펜 프롬프트가 긍정형이다 — 금지 목록을 담지 않는다(D8, 린트로 집행).
  - 펜 배정이 `ledgers/tournament.jsonl`에 기입된다.
  - `compose` 레인은 상류 경로에 쓰기 권한이 없다(D6 단방향).
- **검증**: `pytest tests/test_m5_design_compose.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_transmission_targets_resolve_to_frozen_ids` | 미해소 표적이 있으면 계기 질문지가 생성 불가(D9) |
| `test_blueprint_declares_new_term_budget` | 선언 없으면 L0 `format.new-term-budget`의 기준이 없음 |
| `test_variants_receive_identical_inputs` | 입력이 다르면 토너먼트 비교가 무효(D10) |
| `test_pen_prompt_contains_no_prohibition_list` | 금지 열거가 들어가면 프라이밍 방지 규율이 공허(D8) |
| `test_pen_assignment_recorded_in_tournament_ledger` | 기입 누락 시 승률 데이터가 누적되지 않음 |
| `test_compose_cannot_write_upstream_paths` | 상류 쓰기가 가능하면 단방향 규율이 이름뿐 |
| `test_slot_values_match_charter_slots` | 슬롯 집합이 어긋나면 D11 구조가 미집행 |

#### M6 — L1 국소 대조 + 루프 위상 제어

- **산출**: `engine/gate/l1/*.py`, `engine/gate/loop.py`, `engine/gate/final_eyes.py`
- **DoD**
  - k=3 독립 실행 후 **과반 일치 항목만** `defect`로 채택하고, 소수 의견은 `flag`로 강등 기록한다.
  - 의미 수준 금지선(암시적 투자 조언)은 거부권 없는 `flag`로 CP2에 첨부된다(D8).
  - 수정 루프 캡 3회, 초과 시 `escalate`.
  - L2 메모 1회 → 펜 자유 리비전 1회로 위상 봉쇄.
  - `gate.final-eyes` 레인의 입력은 출하 후보 + 동결 재료뿐이다(이력·메모·점수 미제공 — D15).
- **검증**: `pytest tests/test_m6_l1.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_majority_vote_promotes_only_consensus_defects` | 1표 결함이 거부권을 가지면 노이즈가 파이프라인을 막음 |
| `test_minority_opinion_demoted_to_flag` | 소수 의견 소실 시 관측 데이터가 버려짐 |
| `test_smuggled_claim_in_narrative_detected` | `[narrative]` 뒤 기술 주장이 통과하면 자기 신고가 우회로가 됨 |
| `test_investment_hint_is_flag_not_defect` | 거부권이 붙으면 게이트가 정답 없는 영역으로 확장됨(D7) |
| `test_revision_cap_three_then_escalate` | 무한 루프 시 상류 결함이 은폐됨 |
| `test_l2_memo_round_is_single` | 메모 왕복이 반복되면 위상 봉쇄가 무효 |
| `test_final_eyes_input_excludes_history_and_scores` | 이력이 새면 최종 심급 분리가 무의미(D15) |
| `test_fix_directive_rejects_replacement_sentence` | 대체 문장이 허용되면 게이트가 글을 고치게 됨(D8) |

#### M7 — 계기(프로브 A/B + 채점자 + 국소화 + 교정)

- **산출**: `engine/probe/questions.py`, `engine/probe/run_probes.py`, `engine/probe/grade.py`, `engine/probe/localize.py`, `engine/probe/calibrate.py`, `contracts/schemas/probe-report.schema.json`, `contracts/stages/probe.yaml`
- **DoD**
  - 프로브 입력이 스레드 텍스트로 제한된다(계약 `must_not_read`로 집행 — §5.2).
  - 질문이 `transmission_targets`에서만 파생되고 1:1 대응한다.
  - `quoted_span` 부분문자열 검사가 프로브 환각을 무효 처리한다.
  - 채점이 §5.3 경계선대로 분리되고, 결정론 판정은 모델이 뒤집을 수 없다.
  - `score.json`이 스키마를 통과하고 판정 필드를 갖지 않는다(§5.7).
  - `weakest_tweet`이 `annotation-index.json` 역참조로 결정론적으로 산출된다.
  - golden/mutated 교정에서 golden > mutated가 확인된다(§5.5).
- **검증**: `pytest tests/test_m7_probe.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_probe_input_excludes_material_spec` | 프로브가 재료를 보면 전달 충실도 측정이 붕괴 |
| `test_probe_b_questions_derive_only_from_transmission_targets` | 표적 밖 질문이 섞이면 이해 퀴즈가 됨(D9) |
| `test_question_maps_to_single_material_id` | 복합 질문은 실패 국소화를 파괴 |
| `test_not_stated_is_distinct_from_wrong_answer` | 두 상태가 섞이면 "전달 실패"와 "프로브 오류"가 구분 불가 |
| `test_quoted_span_must_be_substring_of_thread` | 환각 근거가 통과하면 도달률이 부풀려짐 |
| `test_fact_targets_are_graded_deterministically` | 수치를 모델이 채점하면 정답 있는 대조를 포기하는 것 |
| `test_deterministic_verdict_not_overridden_by_model` | 모델이 뒤집으면 결정론 경계선이 무의미 |
| `test_grader_input_excludes_thread_text` | 채점자가 스레드를 보면 관대한 해석 편향이 유입 |
| `test_weakest_tweet_resolves_via_annotation_index` | 국소화가 손으로 지목되면 자동 지목 요건 미충족(D9) |
| `test_unrepresented_target_reports_null_tweet` | 미배치 표적을 펜 실패로 오귀속함 |
| `test_calibration_separates_golden_from_mutated` | 판별력이 없으면 점수 해석 자체가 불가(재설계 신호) |
| `test_score_json_has_no_decision_field` | 판정 필드가 있으면 계기가 게이트로 승격됨(D15) |

#### M8 — L2 자문 메모 + 점수 금지 린트 + 소견

- **산출**: `engine/gate/l2.py`, `engine/lint/no_score.py`, `engine/stages/critique.py`, `contracts/stages/critique.yaml`
- **DoD**
  - `gate-report.schema.json`의 memo 객체가 `additionalProperties: false` + 숫자 필드 부재.
  - 린트가 L2·소견 산출물의 키·본문에서 `/score|rating|grade|점수|\d+\s*\/\s*10/`를 거부한다.
  - 소견이 §5.6 관점 3종을 다루고 계기 데이터를 인용한다.
  - 자문 산출물은 `verdict.decision`을 바꿀 수 없다(쓰기 권한 부재).
- **검증**: `pytest tests/test_m8_advisory.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_memo_schema_rejects_numeric_fields` | 점수 필드가 들어가면 굿하트 미끼가 부활(D8·D15) |
| `test_score_lint_rejects_grade_patterns` | 본문 우회 표기("7/10")가 통과하면 스키마 방어가 반쪽 |
| `test_critique_memo_covers_three_lenses` | 관점 누락 시 소견이 임의 잡담이 됨 |
| `test_advisory_cannot_write_verdict` | 자문이 판정을 바꾸면 거부권 없음이 이름뿐(D7) |

#### M9 — FIGURES (폴백 경로만)

- **산출**: `engine/stages/figures_prepare.py`, `engine/stages/figures_select.py`, `engine/render/chromium.py`, `studio/templates/fallback/*`, `contracts/stages/figures.yaml`
- **DoD**
  - 원천 도면 **전량**에 대해 `assets/fig-NN.png` + `manifest.json`이 생성된다(D12).
  - `selection.json`이 포인터만 갖는다(이미지 데이터 없음).
  - 렌더 출력이 1200×675 CSS px @2x(실제 2400×1350)이다.
  - 렌더 경로에 matplotlib 의존이 없다(import 검사로 집행).
  - 템플릿 스튜디오 산출물 없이 **폴백만으로** 완주한다(원본 크롭 + 최소 주석).
- **검증**: `pytest tests/test_m9_figures.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_every_source_figure_has_asset` | 선택분만 편집되면 자산층 보존 규율이 붕괴(D12) |
| `test_selection_contains_pointers_only` | 사본이 들어가면 편집 왕복·유실 위험이 되살아남 |
| `test_asset_manifest_digest_matches_file` | 자산 변조가 검출되지 않음 |
| `test_render_output_is_1200x675_at_2x` | 규격 미달 이미지가 피드에서 잘림 |
| `test_render_path_has_no_matplotlib_import` | 금지 스택이 슬며시 유입됨(D12) |
| `test_fallback_produces_valid_png_without_templates` | 템플릿 미도착 시 파이프라인이 멈춤(폴백 상비의 실효 상실) |
| `test_asset_files_are_not_overwritten_on_reedit` | 재편집이 원본을 덮으면 이력 유실 |

#### M10 — SHIP + 환류

- **산출**: `engine/stages/ship.py`, `engine/stages/feedback.py`, `engine/ledgers/anchors.py`, `engine/ledgers/regression.py`, `engine/ledgers/fade.py`, `contracts/stages/{ship,feedback}.yaml`
- **DoD**
  - 출하 패키지(`thread.md`·`thread.json`·`images/`)가 주석 잔재 없이 생성된다.
  - CP2 봉투 없이는 출하 산출이 생성되지 않는다.
  - 72h 수동 입력이 `metrics.jsonl`에 들어가고, 앵커 원장은 **백분위만** 저장한다(D13).
  - `window_n < 10`이면 fade 제안이 발생하지 않는다.
  - fade 확정에는 재정 파일 ID가 필요하다.
  - 두 장부의 상호 참조가 해소되고, fade 절차가 회귀 원장에 쓰지 않는다.
- **검증**: `pytest tests/test_m10_ship_feedback.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_shipped_thread_has_no_annotation_residue` | 태그 잔재가 게시되면 strip 파생 규율이 실패 |
| `test_ship_blocked_without_checkpoint2_envelope` | 승인 없이 출하되면 CP2가 우회 가능 |
| `test_anchor_record_rejects_raw_view_count` | 원시 조회수가 들어가면 팔로워 규모 교란이 유입(D13) |
| `test_cold_start_under_ten_blocks_fade_proposal` | 소표본에서 fade가 돌면 표본이 조기 소멸 |
| `test_fade_requires_owner_decision_reference` | 자동 확정이 되면 소재-문체 교란이 취향 데이터를 오염(D13) |
| `test_fade_does_not_touch_regression_ledger` | 인기 물갈이가 회귀 커버리지를 붕괴시킴 |
| `test_dual_registration_cross_references_resolve` | 상호 참조가 끊기면 동시 등재 표기가 무의미 |
| `test_metrics_snapshot_window_is_72h` | 시점이 흔들리면 상대 성과 비교가 무효 |

#### M11 — historian 인터페이스

- **산출**: `tools/check_reader_version.py`, `tools/make_ported_from.py`, `reader/README.md`에 이식 절차 절 추가(파일 자체는 M1 산출), 리포 `CLAUDE.md`의 상호 체크 조항(부트스트랩 시 이미 존재 — 도구 사용법으로 보강)
- **DoD**
  - `PORTED-FROM.md`가 §6.3 서식대로 생성되고 **전체 40자 sha**를 핀한다.
  - 체크 C1~C5가 구현되고 종료 코드 규약(0/2/3)을 따른다.
  - `--fix`·`--sync` 류 플래그가 존재하지 않는다(D14 자동 동기화 금지의 집행).
  - 도구가 read-only다(파일 쓰기 없음).
  - `assert` 미사용, `python3 -O`에서 동일 동작.
- **검증**: `pytest tests/test_m11_historian_if.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_ported_from_records_full_commit_sha` | 축약 sha면 원천 핀이 모호해짐 |
| `test_version_check_exits_three_on_drift` | drift가 exit 0이면 상호 체크가 무의미 |
| `test_version_check_has_no_autofix_flag` | 자동 동기화 경로가 있으면 D14 규율이 우회 가능 |
| `test_version_check_writes_no_files` | 쓰기가 있으면 read-only 규율이 이름뿐 |
| `test_run_reader_version_major_must_match_local` | 계약 MAJOR 불일치 런이 조용히 진행됨 |
| `test_checker_behaves_identically_under_O` | `python3 -O`에서 검증이 사라지는 공허 통과(2026-08-16 실측)를 놓침 |

#### M12 — 오케스트레이션

- **산출**: `contracts/pipeline.yaml`, `engine/runner/*.py`, `engine/runner/state.py`
- **DoD**
  - 스테이지 순서가 계약(`source`→`read`→CP1→`freeze`→`design`→`figures`→`compose`→`gate`→`probe`→`critique`→CP2→`ship`→`feedback`)대로 실행된다.
  - 체크포인트에서 확인 파일이 나타날 때까지 정지한다.
  - 재개 시 완료 스테이지를 건너뛴다.
  - write-scope 위반을 halt로 처리한다(§7.4).
  - `compose`가 변주 수만큼 병렬 실행된다.
- **검증**: `pytest tests/test_m12_orchestrator.py -q`

| 테스트 | 반증 대상 |
|---|---|
| `test_stage_order_matches_contract` | 순서가 흔들리면 동결 전 요리 같은 사고가 가능 |
| `test_checkpoint_halts_until_confirm_file` | 정지하지 않으면 Owner 재정이 우회됨(D6) |
| `test_resume_skips_completed_stages` | 재실행이 산출물을 덮어써 증거가 소실 |
| `test_write_scope_violation_halts_run` | 단방향 규율이 런타임에서 미집행 |
| `test_parallel_variants_do_not_share_paths` | 변주 간 오염으로 토너먼트 비교가 무효(D10) |
| `test_pipeline_yaml_validates_against_contract_schema` | 계약 파일 오타가 런타임까지 살아남음 |

### §8.5 회귀 스위트 테스트 설계 (M4)

회귀 스위트는 게이트의 게이트다(D8 메타). 설계 원칙 3개:

1. **변조본 검출 실패 = 테스트 실패.** `cases.jsonl`의 각 행은 `expect.must_detect: true`를 갖고, 심은 결함을 지정 검출기가 잡지 못하면 pytest가 fail한다. "나중에 고치자" 상태를 xfail로 숨기지 않는다.
2. **golden 100% 통과 강제.** 출하 확정본에서 결함이 하나라도 나오면 fail한다. 오탐은 미검출만큼 치명적이다 — 오탐이 잦은 게이트는 사람이 무시하게 되고, 그 순간 게이트는 존재하지 않는다.
3. **자족성.** golden·mutated 표본은 자기 정답지(동결 재료·블루프린트)를 동봉한다(§6.5). 런 폴더 프루닝이 스위트를 깨뜨리면 안 된다.

| mutation type | 심는 것 | 잡아야 하는 검출기 |
|---|---|---|
| `hallucinated-claim` | 재료에 없는 기술 주장 문장 | L1 국소 대조 |
| `ticker` | 종목 티커 표기 | L0 `lexicon.forbidden` |
| `ungrounded-number` | 동결 재료에 없는 수치 | L0 `numeric.exhaustive` |
| `smuggled-claim-in-narrative` | `[narrative]` 태그 뒤의 기술 주장 | L1 신고 감사 |
| `retracted-citation` | `retracted` 항목 인용 | L0 `citation.resolve` |

게이트 코드 수정 시의 강제 조건: **심은 결함 100% 검출 + golden 100% 통과**. 둘 중 하나라도 깨지면 그 수정은 머지 대상이 아니다.

MVP 구간(M6 부재)에서는 L1 의존 케이스 2종(`hallucinated-claim`·`smuggled-claim-in-narrative`)이 미검출 상태다. 이를 xfail로 표시하지 말고 **`cases.jsonl`에 `status: pending-detector: L1`로 명시**하고, 스위트 리포트가 "미커버 케이스 2건"을 매 실행 출력하게 한다. 침묵하는 부재보다 시끄러운 부재가 안전하다.

### §8.6 병행 레인과 Owner 관여 지점

**병행 가능 레인**:

| 레인 | 모듈 | 착수 조건 |
|---|---|---|
| A (크리티컬) | M1 → M2 | 즉시 |
| B | M3 → M4 | M3는 즉시, M4는 M1 스키마 확정 후 |
| C | M9 | M2의 재료 `figures[]` 계약 확정 후 |
| D | M11 | M1 완료 후(짧음) |
| 합류 | M5 | M2·M3 완료 후 — 레인 A·B가 여기서 만난다 |
| 후속 | M6·M7·M8 | M4·M5 완료 후(상호 병행 가능) |
| 후속 | M10 | M3·M9 완료 후 |
| 마감 | M12 | M2~M10 |

M3가 M1과 무관하게 즉시 착수 가능한 것이 이 로드맵의 유일한 초기 병행 여지다(주석층 문법은 재료 스키마를 모른 채 정의된다 — 인용 ID는 문자열 토큰일 뿐이고, ID의 해소는 M4가 담당한다).

**Owner 관여 지점**:

| 지점 | 성격 | 관련 모듈 | 근거 |
|---|---|---|---|
| **CP1** 재료 승인 | 런 진행 차단 | M2 | D6 |
| **CP2** 변주 선택 + 출하 승인 | 런 진행 차단 | M10 | D6·D9 |
| lexicon 등재·완화·삭제 | 재정 | M4 | D7·D15 |
| 회귀 원장 큐레이션 | 재정 | M4·M10 | D13 |
| 앵커 fade 확정 | 재정(배치 리뷰) | M10 | D13 |
| reader drift 상신 | 재정 | M11 | D14 |
| 도면 템플릿 시안 선택·토큰 동결 | 재정(별도 발주) | studio | D12 |
| 펜 주전 승격(승률 70%) | 재정 | M5·M10 | D10 |
| 계기 판별력·유효성 임계 입법 | 재정 | M7 | D9·D13 |

CP1·CP2 외의 항목은 런을 멈추지 않는다 — 재정 전까지는 해당 기능이 **비활성**일 뿐이다(등재되지 않은 어휘는 차단되지 않고, 확정되지 않은 fade는 제안 상태로 남는다).

> [OPEN] 첫 런의 펜 배정 수(2판 vs 3판). 헌장은 2~3판을 허용한다(D10). 추천: 첫 런은 **2판**(Opus 5 high / Opus 5 max)으로 시작하고, 교차벤더 1(GPT-5.6-sol)은 파이프라인이 한 바퀴 돈 뒤 3판째로 투입한다 — 첫 런에서 벤더 어댑터 문제가 겹치면 실패 원인 분리가 어렵다.

> [OPEN] MVP 첫 런에 M11(historian 인터페이스)을 포함할지. 브리프의 MVP cut에는 없다. 추천: 포함하지 않되 **`reader/READER-VERSION` 파일 자체는 M1에서 만들고**, 상호 체크 도구는 historian 리포가 실제로 생기는 시점에 착수한다(현재는 상대가 없어 C3 검사가 공회전한다).

---

## §9 열린 설계 논점

본문 각 절의 `> [OPEN]` 블록은 **집필 시점의 논점 제기**다. **그 처분은 이 절이 정본이다.** 논점은 두 부류로 갈린다.

- **[ENG-확정]** (§9.0) — 헌장 범위 안의 공학 결정. 총괄이 조립 단계에서 확정했으며 Owner 재정을 기다리지 않는다. 본문과 이 절이 어긋나면 이 절이 이긴다.
- **[OWNER-대기]** (§9.1~§9.14) — 헌장이 답하지 않고 Owner 재정이 필요한 사항. **엔진은 재정 전까지 이 항목에 의존하는 기능을 확정 구현하지 않는다.** 각 항목은 논점 · 왜 지금 결정할 수 없는가 · 잠정 처리(추천안) 3부로 적는다. 잠정 처리는 "재정 전까지 엔진이 어떻게 행동하는가"이지 재정이 아니다.

---

### §9.0 [ENG-확정] 조립 단계에서 확정한 공학 결정

| # | 논점 | 확정 | 반영 위치 |
|---|---|---|---|
| E1 | 항목 ID의 전역 참조자 (historian은 N개 런을 섞는다) | 전역 참조자는 `<run_id>#<item_id>` (예: `openai-us20260147854a1-cim-fp#M7`). **스펙 문언에만 규정하고 정본 스키마에는 필드를 추가하지 않는다** — historian 인덱스가 이 규칙으로 조립한다. 계약을 넓히지 않는 쪽을 택했다 | §2.1 |
| E2 | `fact`에 의미 라벨 부재 — `[M5]`를 인용한 문장이 "그 숫자가 무엇의 숫자인지"를 재료에서 확인할 길이 없었다 | **`fact.label_kr` 필수 추가.** v0 확정 전이라 지금이 가장 싸다(M1 구현 후에는 계약 major 비용) | §2.4·§2.7·§2.8 반영 완료 |
| E3 | `superseded` 항목 인용의 처분 (고정 규칙은 `retracted`만 규정) | **defect 아님. L1 `flag`로 첨부**해 CP2에서 Owner가 본다. `superseded` 인용은 거짓이 아니라 낡은 것이므로 거부권을 확대하지 않는다 — 관할권을 한 뼘도 넓히지 않는다는 원칙(D7)의 적용 | §4.4 |
| E4 | 트윗 **내부**의 의도적 빈 줄 | **v0 금지**(`annotation.schema` 위반). 스캔성(D11)은 문장 단위 줄바꿈으로 충족한다. 허용하면 strip ⑤와 트윗 경계 판정이 모호해진다 | §3.2 |
| E5 | strip된 스레드 텍스트의 영속 경로 부재 — `70-ship/thread.md`는 CP2 후에 생기는데 `probe`·`critique`·최종 심급은 그 이전에 같은 텍스트가 필요하다 (**실제 계약 누수**) | **`50-gate/<variant>/thread.stripped.md` 신설**, strip을 `gate` 종료 산출로 승격. `ship`은 승인 변주의 그 파일을 복사만 하며, 바이트 동일성을 종료 검사로 확인한다 | §1.11·§7.2 반영 완료 |
| E6 | `gate.final-eyes`의 지위와 산출 경로 | **`gate.yaml` 내부 하위 심급**(고정 스테이지 id를 늘리지 않는다). 산출은 `verdict.json`의 `final_eyes` 객체 — 신규 경로 없음 | §1.10 반영 완료 |
| E7 | 숫자 화이트리스트 등재의 격 (`run.yaml` 편집이 곧 게이트 완화다) | **런 단위 재량 + 체크포인트 2에 전량 인쇄**로 시작. 화이트리스트가 3항목을 넘는 런이 나오면 그때 Owner 재정으로 승격 | §4.4 |
| E8 | `patent.md` 취득 경로를 엔진 안에 둘지 | **엔진 범위 밖.** 원천은 외부 도구(WIPS 명세서 추출 등)의 산출을 투입받는다. 엔진의 계약은 "원천을 받는다"에서 시작하며, `patent.sha256`으로 그 원천을 핀한다 | §1.3 |
| E9 | `drop-proposed`를 Owner가 `go`로 뒤집은 경우 근거의 등재 위치 | **양쪽에 남긴다** — 런 안(`approval-v<N>.md`)과 `docs/decisions/`. 재정은 리포 규약상 재정 로그에 남는다 | §1.5 |
| E10 | 변주 전멸 시 기본 복구 경로 | **블루프린트 개정 1회 → 재전멸 시 재료 반려.** 전 변주가 같은 지점에서 실패하면 공통 입력의 문제이고, 그중 개정 비용이 싼 쪽이 블루프린트다 | §1.10 |
| E11 | `feedback`이 런 스테이지인지(런을 72h 열어둠) 별도 배치 작업인지 | **별도 배치 작업.** 런은 `ship`에서 닫히고, 72h 지표는 배치 리뷰 때 런 폴더에 추기된다. 런을 사흘씩 열어두면 상태 관리가 파이프라인 전체를 오염시킨다 | §1.15 |
| E12 | 계기 판별력의 최소 마진을 수치로 고정할지 | **v0은 수치 임계 없이 부호만 확인**(golden > mutated). 근거 없는 임계를 미리 박으면 그 자체가 굿하트 표적이 된다(D15). 3개 런의 교정 데이터가 쌓인 뒤 재정으로 입법 | §5.5 |
| E13 | 채점자 레인의 모델 | **결정론 경로 우선**(핵심 사실), 모델 채점 경로는 **펜·프로브와 다른 계열**로 둔다(설정값 `probe.grader`). 프로브와 채점자가 같은 편향을 공유하지 않게 하는 것이 요건이고, 구체 모델은 구현 시점의 가용 레인으로 정하되 **실호출 모델을 런 메타에 기록**해 사후 검증 가능하게 한다 | §5.3 |
| E14 | 런 폴더 3급 캐시의 만기·2급 증거 압축 시점 | **3급 = 출하 후 90일, 2급 = 출하 후 180일에 압축(삭제 없음).** 저장 압박이 실제로 관측되기 전에 만기를 짧게 잡지 않는다 — 초기 런의 증거가 사후 교훈의 유일한 사료다 | §7.7 |
| E15 | MVP 첫 런에 M11(historian 인터페이스)을 포함할지 | **포함하지 않는다.** 단 `reader/READER-VERSION`은 M1에서 만든다(이미 존재). 상호 체크 도구는 historian 리포가 실제로 생기는 시점에 착수한다 — 현재는 상대가 없어 검사가 공회전한다 | §8.2 |
| E16 | 인용 태그 주변 공백 규정의 모호성 | **태그 내부 공백 금지**(`[M3, M7]`은 위반), **태그 앞 공백은 0개 이상 허용**(strip 정규식이 `\s*`로 흡수) | §3.2 |
| E17 | `grounding.component`의 값 공간(청구항 element id인가 `M<n>`인가) | **component kind 항목의 `M<n>`.** 커버리지 검사는 `element → material_id → grounding.component` 역인덱스로 정의한다 | §2.4·§2.6 |
| E18 | 숫자 전수 대조의 정답지 범위 — 특허번호·날짜는 `fact`가 아니라 `patent` 블록에 산다 | **`patent.number`와 `patent.dates.*`를 정답지에 포함**한다(동결 재료의 일부로 읽는다). READ가 미러 `fact`를 발행하는 대안은 중복이라 기각 | §4.4 |
| E19 | `figures[].asset_path`의 시점 문제 — 재료는 CP1에서 동결되는데 도면 편집은 그 뒤 스테이지다 | **nullable로 규정**하고 포인터 해소 검사 대상에서 제외한다. 자산층 정본은 `30-figures/assets/manifest.json` | §2.5 |

---

### §9.1 [OWNER] 트윗 수 × 트윗 길이 vs 단어 총량의 산술 충돌

**논점.** D11은 세 수치를 동시에 규정한다: 트윗 수 6~12 · 본문 트윗 180~260자 · 소비 시간 3~4분 ≈ 400~600단어. 그런데 EN 산문의 어절 길이를 공백 포함 5.5~6.0자로 잡으면 트윗당 30~47단어이고, 총량은 다음과 같다.

| 트윗 수 | 총 단어 (하한~상한) | 400~600단어 목표 |
|---|---|---|
| 6 | 약 180~284 | 미달 |
| 8 | 약 240~378 | 미달 |
| 10 | 약 300~473 | 부분 도달 |
| 12 | 약 360~567 | 도달 |

즉 400단어 하한은 **10~12트윗을 사실상 강제**한다. 그런데 같은 조항이 "초기 런은 보수적으로(적은 쪽)"라고 하고, 더 근본적으로 "**트윗 수 = 강한 전시물 수의 종속변수**(분량 채우기 분할 금지)"라고 한다. 단어 총량을 구속 조건으로 걸면 이 종속변수 원칙이 뒤집힌다 — 총량을 채우려고 전시물을 쪼개게 된다.

**왜 지금 결정할 수 없는가.** 어느 쪽이 불변항이고 어느 쪽이 파생 지표인지는 헌장 문언만으로 갈리지 않는다. "소비 시간 3~4분"이 불변항으로 명시되어 있는데, 도면 감상 시간을 소비 시간에 포함하면 단어 수가 적어도 3~4분이 성립하므로 충돌이 해소된다 — 그러나 그 해석은 Owner의 것이지 엔진의 것이 아니다.

**잠정 처리(추천).** L0는 **트윗 수(6~12)와 트윗 길이(180~260자)만 구속**하고, 단어 총량은 **L2 자문 지표**로 둔다. 소비 시간 불변항은 "도면 감상 포함"으로 해석한다. 근거: 종속변수 원칙이 총량보다 상위 서술이며, 총량을 게이트로 걸면 D11이 금지한 "분량 채우기 분할"을 게이트가 강제하는 자기모순이 생긴다.

### §9.2 [OWNER] T1 훅 트윗의 길이 규격

**논점.** D11의 180~260자 규정은 "본문 트윗"에 걸린다. T1(포스터 훅)과 꼬리 트윗이 여기 포함되는지 문언상 불분명하다. 훅은 스레드의 성패 그 자체이므로(D11) 짧고 강한 한 방이 유리할 수 있고, 꼬리는 링크·팔로우 안내라 짧다.

**잠정 처리(추천).** 훅 = **상한 260자만 적용(하한 없음)**, 꼬리 = 길이 규격 면제, 전시·반전·착지 슬롯 = 180~260자 전부 적용. L0 `format.body-length`의 적용 대상을 슬롯 enum으로 지정한다.

### §9.3 [OWNER] 종속항 구성요소의 접지 필수 범위

**논점.** D5 ①은 **전 청구항(독립+종속)**의 구성요소 전 분해를 요구하고, D5 ③은 "구성요소 ↔ 명세서 ↔ 도면부호"의 3중 접지를 요구한다. 두 조항을 이어 읽으면 종속항의 부가 한정까지 전량 접지해야 한다. 그러나 종속항 전량 접지는 READ 비용을 크게 키우는데, 그 비용이 도슨트 품질(D2 전달 충실도)로 환산된다는 근거는 없다 — 스레드에 실리는 것은 대개 독립항 골격이다.

**왜 지금 결정할 수 없는가.** "전 분해"와 "3중 접지"의 결합 범위는 헌장 해석이며, 비용-품질 교환의 판단은 Owner 몫이다.

**잠정 처리(추천).** **분해는 전 청구항 필수**(D5 ① 문언 그대로), **접지는 독립항 element 전량 필수 + 종속항 `additions[]`는 권고**로 두고, 미접지 종속 한정을 `coverage.advisory[]`로 CP1에 노출해 Owner가 건별로 승격하게 한다. 반대 재정이면 §2.6 커버리지 검사의 한 줄만 고치면 된다.

### §9.4 [OWNER] 재료 명세 서술 필드의 언어 정책

**논점.** 재료 명세는 두 역할을 겸한다: ① CP1에서 Owner가 읽는 KR 문서이자 Owner 이해층(D6) ② 펜이 EN 스레드를 쓸 때 소비하는 재료. 인용·원문(`text_verbatim`·`quote`)은 원문 그대로 EN이 확정이지만, 해설 필드(`label_kr`·`statement_kr`·`positioning`)의 언어는 정해지지 않았다. KR 단일이면 펜이 KR→EN 번역을 거쳐 번역투 위험이 생기고, EN 단일이면 CP1의 이해층 기능이 약해진다. 또한 historian은 전문가·유료 채널이라 EN 소비가 있을 수 있다.

**왜 지금 결정할 수 없는가.** **이 항목은 historian과의 스키마 계약(D14)에 직접 걸리므로 나중에 바꾸기 가장 비싼 결정이다.** 필드명을 나중에 바꾸면 계약 major다.

**잠정 처리(추천).** v0는 **KR 필드명 고정**(현행)으로 두되, EN이 실제로 필요해지는 시점에 `label_en`·`statement_en`을 **선택 필드로 추가(minor)**한다. 펜에게는 EN 필드가 있으면 EN을, 없으면 원문 인용을 주고 **KR 해설은 주지 않는다** — 번역투 유입 경로를 구조적으로 차단한다.

### §9.5 [OWNER] 금지 어휘 정본 v0의 부트스트랩

**논점.** D7은 "입법된 규칙"을 게이트의 정답 서식지로 삼고 등재는 **Owner 재정으로만** 한다고 못박았다. 그러면 최초 목록(`contracts/lexicon/forbidden.yaml` v0)도 재정 대상이다 — 엔진이 스스로 채우면 규율 위반이다.

**잠정 처리(추천).** 초안을 **제안서**로만 제출하고, 재정 전까지 `lexicon.forbidden`은 **빈 목록으로 통과**시키되 그 공허 통과를 verdict에 명시 기록한다. 제안 후보(D3의 절대 금지선과 1:1 대응, 6~8항): 티커 표기 패턴(`$XXXX`·`NASDAQ:XXXX`·`KRX:######`), 매수/매도/보유 동사, 목표가·가격 전망 어구, 수익률 약속 어구.

### §9.6 [OWNER] 결함 카탈로그의 초기 상태

**논점.** 결함 카탈로그는 "알려진 나쁨만 차단"하는 반증 전용 장치이고 등재는 재정으로만 한다(D7). 첫 런은 카탈로그가 빈 상태로 출발해야 하는가.

**잠정 처리(추천).** **빈 카탈로그로 출발한다.** 구 프로젝트의 AI 텔 목록을 미리 이식하지 않는다 — 새 독자상(D2)과 새 형식(D11)에서 무엇이 나쁨인지는 아직 표본이 없다. 첫 런 이후 Owner가 실물에서 수확해 재정으로 등재한다. 카탈로그가 비어 있다는 사실 자체를 verdict에 기록해 "통과 ≠ 좋음"을 가시화한다.

### §9.7 [OWNER] 원시 지표의 저장 정책

**논점.** D13은 상대 성과(최근 N개 이동 중앙값 대비 백분위)로 가중치를 조정하고 "**원시 조회수는 쓰지 않는다**(팔로워 규모 교란)"고 한다. 그런데 백분위를 계산하려면 각 글의 원시값이 어딘가에 있어야 한다. "쓰지 않는다"가 **저장 금지**인지 **판정·노출 금지**인지가 갈린다.

**잠정 처리(추천).** 원시값은 `ledgers/metrics.jsonl`에 **저장하되**, 앵커 가중치·게이트·프롬프트·보고서에는 **백분위만 노출**한다. 즉 판정 사용 금지로 읽는다. 저장 자체가 금지라면 백분위 계산이 불가능하므로 이 해석이 유일하게 성립한다고 판단하나, 명시 재정을 요청한다.

### §9.8 [OWNER] 프로브·다수결의 표본 수 (n, k)

**논점.** D9는 "계기 = Haiku n대", D8은 "L1 k-반복 다수결"이라고만 하고 수치를 주지 않았다. 비용과 노이즈 감소량의 교환이며 실측 없이는 최적값을 모른다.

**잠정 처리(추천).** **n=5, k=3**으로 시작한다(k는 과반 판정이 성립하는 최소 홀수). 첫 배치에서 프로브 분산과 L1 소수 의견 비율을 실측한 뒤 조정안을 상신한다.

### §9.9 [OWNER] 첫 런의 변주 수

**논점.** D10은 변주 2~3판과 초기 배정(Opus 5 high / Opus 5 max / 교차벤더 1)을 규정한다. 3판은 게이트·계기 비용을 3배로 만들고, 교차벤더 레인의 실가용성(인증·세션 한도)은 런타임 조건이다.

**집필 레인 간 이견이 있었다.** 한쪽은 "토너먼트 표의 첫 행이 두 벤더를 모두 담아야 이후 승률 판정이 의미를 갖는다"며 3판을, 다른 쪽은 "첫 런에서 벤더 어댑터 문제가 겹치면 실패 원인 분리가 어렵다"며 2판을 추천했다.

**잠정 처리(추천).** **첫 런 2판(Opus 5 high / Opus 5 max) → 2호 런부터 3판.** 운영 이력상 교차벤더 레인의 취약성이 실측된 바 있어, 파이프라인 첫 바퀴에서 변인을 하나 줄이는 편이 낫다고 판단한다. 교차벤더 레인이 실패하면 조용히 대체하지 말고 토너먼트 원장에 **결측으로 기록**한다.

### §9.10 [OWNER] "배치"의 정의와 상관 점검 표본

**논점.** D10(승률 70% 굳으면 주전 승격)과 D13(계기 점수↔실반응 상관, fade-out 배치 리뷰)이 모두 **배치 단위**로 작동하는데 배치가 몇 런인지 정해지지 않았다. 집필 레인은 10런을, 총괄 초안은 5런을 추천해 갈렸다.

**잠정 처리(추천).** 둘은 서로 다른 축이므로 분리한다 — **배치(Owner 리뷰 주기) = 5런**, **상관 점검 표본 = 누적 10건부터**(D13의 콜드 스타트 임계 10과 정합). 상관 지표는 Spearman ρ, v0에서는 임계 없이 부호와 산점도만 보고한다.

### §9.11 [OWNER] fade-out 자동 제안의 발동 규칙

**논점.** D13은 "임계 미달 시 fade-out, 자동 제안 → 배치 리뷰에서 Owner 재정 확정"까지 정하고 임계값은 주지 않았다.

**잠정 처리(추천).** `percentile < 0.25`가 **2회 연속** 관측된 앵커만 제안 대상으로 올린다(단 `window_n ≥ 10`). 확정은 배치 리뷰의 Owner 재정. 앵커의 초기 가중치와 조정 폭도 같은 재정에서 함께 입법할 것을 제안한다.

### §9.12 [OWNER] 재료 개정 시 이미 완성된 다른 변주의 처분

**논점.** 재료 반려로 `spec_version`이 +1 되면, 아직 그 재료를 인용하지 않은 다른 변주의 초안도 폐기하고 전량 재작성할지, 영향받은 변주만 재작성할지 헌장은 규정하지 않는다. 전량 재작성은 비용이 크고, 선별 재작성은 변주 간 "같은 재료" 전제(D10 공정 비교)를 흔든다.

**잠정 처리(추천).** **전량 재작성.** D10의 공정 비교는 "같은 재료·같은 블루프린트"가 전제이며, 서로 다른 `spec_version`으로 쓰인 변주를 나란히 놓고 고르는 것은 토너먼트를 오염시킨다. 다만 비용이 실제로 문제가 되면 재정으로 완화할 수 있다.

### §9.13 [OWNER] 승인 봉투의 작성 주체와 무인 실행 플래그

**논점.** 승인 봉투(`15-frozen/approval-v<N>.md`·`70-ship/checkpoint2.md`)를 Owner가 직접 쓰는지, 오케스트레이터가 Owner 응답을 받아 대필하는지, 그리고 무인 실행 플래그(구 프로젝트의 `--yes`)를 두는지가 미정이다. 체크포인트는 헌장이 명시한 두 곳(D6)이므로 그 우회 장치의 존부는 Owner 결정 사항이다.

**잠정 처리(추천).** **대필 허용 + 육성 인용 필수**(Owner의 실제 응답 문구를 봉투에 그대로 인용), **무인 실행 플래그는 두지 않는다.** 체크포인트 2는 출하 승인이고 D9는 "구속력 있는 결정은 이 단계뿐"이라 했으므로, 이를 건너뛰는 플래그는 헌장의 유일한 재정 지점을 무력화한다.

### §9.15 [OWNER] `gate.final-eyes`의 관할 술어 (감수 BLOCKER #1)

**논점.** 스펙은 최종 심급에 거부권을 주면서 그 술어를 "출하 적격 최종 판정"이라고만 적었다. 독립 감수는 이것이 **D7 관할권 원칙 위반**이라고 판정했다 — 이력·메모로부터의 격리(D15)는 편향을 없애지만 **관할권을 창설하지는 못한다**. 술어가 열거되지 않은 거부권은 문체·재미·전반 품질에 대한 거부로 흘러갈 수 있고, 그것은 정확히 D7이 금지한 것이다.

**왜 지금 결정할 수 없는가.** D8은 "최종 심급 = 이력·메모 모르는 새 눈"을 명시하지만 그 심급이 **무엇을 근거로 막을 수 있는지**는 말하지 않는다. 거부권의 범위는 헌장 해석이다.

**잠정 처리(추천).** final-eyes의 관할을 **열거 한정**한다 — ① 출하 후보 ↔ 동결 재료의 대조 재확인 ② 입법된 규칙(금지 어휘·형식)의 재확인. 그 둘로 좁히면 D7의 서식지 ①②에 정확히 앉는다. 전반 품질 인상은 거부가 아니라 **CP2에 첨부되는 소견**으로 보낸다.

### §9.16 [OWNER] 다중 종속항 표현과 수치 사실의 출처 결속 (감수 BLOCKER #4·#5)

**논점.** 독립 감수가 "가장 비싸게 물어뜯을 것"으로 꼽은 두 건이며, 둘 다 **historian 계약(D14)이 동결되기 전에 고치는 것이 압도적으로 싸다.**

1. **다중 종속항이 손실 표현이다.** `depends_on`이 스칼라 문자열이라 "청구항 1 또는 2에 있어서"류를 담지 못하고, 한 종속을 주 종속으로 삼고 나머지를 `attaches_to`로 인코딩하면 **의미가 변한다**. 종속항 `text_verbatim` 전문도 없어 마쿠쉬·조건부·수단항 관계가 불투명 문자열로만 남는다.
2. **수치 사실의 출처가 결속되지 않는다.** `fact.value_raw`가 `source.quote` 안에 실제로 존재할 것을 요구하지 않으므로, **실재하는 인용 + 날조된 수치**의 조합이 결정론 검사 4종을 전부 통과한다. 그 값이 곧 숫자 전수 대조(§4.4)의 정답지가 되므로, 게이트가 신뢰하는 기준 자체가 오염될 수 있다.

**잠정 처리(추천).** ① `depends_on`을 배열로 승격하고 종속항 `text_verbatim`을 필수화한다(v0 확정 전이므로 아직 minor). ② `fact`에 인용 내 수치 스팬(`source.value_span`)을 저장하고 `value_raw`를 그 스팬에서 **결정론적으로 파생**시킨 뒤, 검사 4종에 "파생 일치" 항목을 추가한다. 둘 다 M1 착수 전 스펙 개정으로 처리할 것을 권한다.

### §9.14 [OWNER] 특허 도면의 사용권

**논점.** D12는 도면을 핵심 자산으로 삼고 전량 편집·주석·재조판을 전제한다. 공개 특허 문헌 도면의 2차 편집물을 공개 게시하는 것에 대한 판단은 Owner(변리사)의 영역이다.

**잠정 처리(추천).** **첫 출하 전에 Owner 확인 1회.** 확인 전까지 자산층 생성·내부 검토는 진행하되 게시는 보류한다. 확인 결과를 `docs/decisions/`에 남긴다.
