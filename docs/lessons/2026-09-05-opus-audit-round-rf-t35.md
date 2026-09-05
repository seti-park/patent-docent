# 독립 감수 원문 — 좁은 재감사 3(라운드 RF `2d01e91` + 재정 T35 집행 `4bb2579` + 기록 `a48a97f`·`f807ad8`) · opus max · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`raw.json` 의 `.result` 를 `jq -r` 로 꺼낸 `out.txt` · sha256 `6414ec81348dca7133228baef50686addf1a4b54e4dc3d0137d3e16910a2b981` 와 `---` 아래가 동일 · 31651 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/opus-audit-round-rf-t35/`.

**좌석 = opus max**(ROUTING v2.1 §3 M9 · sol 저작 → opus). CLI 직구동 `claude -p --model claude-opus-5 --effort max --output-format json`(환경변수 2종 · usage 보존 — 81턴 · 35.8분 · 출력 96,524 토큰(사고 46,492) · 캐시 읽기 11,612,636 · 캐시 생성 255,171 · 청구 $10.77) · `setsid nohup` 분리 · 13:17:42 → 13:53:57 · EXIT=0 · stderr 0 B. 발주문 = drafts `AUDIT-ORDER-round-rf-t35.md`(M1b astra 3차 도전 MD-1~MD-6 반영판 · 여섯 질문 · 지적 ID `RG-*` · PASS = 신규 지적 0 + 폐쇄표 전건 closed · **감사 중 정본 커밋 금지 — 지켜졌다**: 시작·종료 HEAD `f807ad8` · status 0행). 사본 = 홈 fs `~/projects/workspaces/pd-audit-round-rf-t35`(detached `f807ad8` · 마커 3검증 일치 · 개시부터 status 한 줄) · basetemp·`TMPDIR` 홈 fs `pd-audit6-basetemp`(종료 시 삭제) · 사본 원상 · `/tmp` 무접촉.

**판정 = FAIL · 지적 3건(MED 1 · LOW 2) · 새 재정 사항 0.** **값·집행은 네 라운드 연속 닫혔다** — RF-1·3·4·5·6·7·8 closed · **RF-2 partially**(⒜ 주석·변조 H 는 완전 폐쇄 · §13 정정 마커 약속 미이행) · T35 ⑴⑵ 조건 전건 closed · MB-1~7 · MC-1~6 · MD-1~6 전건 closed · 명령되지 않은 hunk 0(26 중 25 대응 + MD-5 예고분 · MD-5 = 등가·무해·불필요 · 총괄 판단에 동의 · 되돌릴 필요 없음) · 두 커밋 반경 겹침 0 · 실런 판독본 3건 전후 sha256 동일 · 감사자 독립 재현 = pytest 두 모드 810 · 관문 7종 두 모드 · 변조 12종(엔진 10 · 스키마 2) + 변조 H + 축 (i) 2종 전부 지정 사례만 붉음 · 형태표 30사례 전건 일치 · **37,060 입력 전수로 10-b 본문 공백 0·예외 0·순서 위반 0 · 서명 다섯({G}·{I}·{I,T}·{T}·{A})만 관측** · `TMPDIR` 처방 실측(`mkdtemp` 가 tmpfs → 홈 fs). **RG-1**(MED · 총괄 기록): RF-2 처분이 약속한 §13 정정 마커(「없음」은 계약 단독 변조 공간 안의 답 — 한정어 복원)가 없고 HANDOFF 16차 줄도 무한정 「⒜ 고유 변조 없음」 그대로 — 변조 H 가 실재하므로 그 문장은 거짓 · RF-7 로 같은 줄을 편집하면서 남김. **RG-2**(LOW · 발주자 1차): 비해시 중복 검사(`_has_duplicate_values`)는 두 호출점 모두 허용값 검사에 가려 **도달 불능**이라 `set()` 판본으로 원복해도 810 전건 초록 · `I14` 픽스처는 이름이 가리키는 속성을 태우지 못함 · 골격 ⒀ 「원복해도 전건 초록」 재발(RF-1 형태) · **M1b medium 3런이 놓친 한 건**(§21 소견의 예고). **RG-3**(LOW · 발주자): 발주문 §1 `96f7582` 괄호의 문구 중복(MD-6 정정 과정의 잔재 · 사실 오류 없음). 남은 것 = RG-1 마커 2줄 · RG-2 헬퍼 단위 시험 1줄 · 골격 「금지 문자열 조건은 반경 파일·함수로 한정」 · 사후 확인 ⓡⓢⓣ(ⓣ 후반부는 이 감사의 축 (ii) 직접 재현으로 근거 보강) · T36 ⑶ 이관 · 골격 ⑿ 추기 사후 확인. [미검증] 6.

지적 열거 = RG-1, RG-2, RG-3

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-04-t31-t32.md` **§22** 에 있다. **전부 수용** → RG-1·RG-3 = 이 커밋(§13·HANDOFF 마커 · 발주문 drafts) · RG-2 = 라운드 RG(sol-coder · 시험 1건 · M1b astra high 경유) · 골격 ⒀ 추기(금지 문자열 조건 범위) · 그 뒤 **좁은 재감사 4(RH · RG 폐쇄만 · 축소 범위)** → PASS 면 종결 상신.

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

모든 검증을 마쳤다. 보고한다.

---

# 좁은 재감사 3 — 라운드 RF(`2d01e91`) + 재정 T35 집행(`4bb2579`) · 기록 커밋 `a48a97f`·`f807ad8`

**판정 = FAIL · 신규 지적 3건(MED 1 · LOW 2) · 새 재정 사항 0.** **값과 집행은 이번에도 닫혔다** — RF-1·3·4·5·6·7·8 closed · T35 ⑴⑵ 조건 전건 closed · MB-1~7 · MC-1~6 · MD-1~6 전건 closed · 명령되지 않은 hunk 0(26 hunk 중 25 대응 + MD-5 예고분 1) · 두 커밋 반경 겹침 0 · 실런 판독본 3건 전후 sha256 동일 · 전체 스위트 두 모드 `810 passed` exit 0 · 관문 7종 두 모드 `FAILS=0`. **FAIL 의 원인은 하나** — **RF-2 가 `partially`**다. 처분표가 「이 커밋 — §13 정정 마커」를 약속했는데 §13 의 그 줄은 **바이트 동일**이고 마커가 없다. 나머지 둘은 이 라운드 발주문의 설계 결함(비해시 중복 검사에 판별 시험 0)과 발주문 문언 중복이다.

## ① Preflight

```
사본 .audit-sandbox   path=/home/laptop/projects/workspaces/pd-audit-round-rf-t35
                      pin=f807ad8cc7a321a9f96b9eac35e69712507a4691
                      order=AUDIT-round-rf-t35-20260905 · disposable=true
사본 HEAD             f807ad8cc7a321a9f96b9eac35e69712507a4691  (## HEAD (no branch))
사본 git status       ?? .audit-sandbox            ← 개시부터 한 줄
정본 HEAD             f807ad8cc7a321a9f96b9eac35e69712507a4691  (개시 = 종료 · 감사 중 커밋 0)
정본 트리             cc0433a94735fa594c70e1d4651f8170d3c4065f  (사본 트리와 동일)
정본 status 행 수     0
```

마커 3검증(`path`·`pin`·`order`) 전건 일치. 정본은 감사 시작·종료 시점 모두 `f807ad8`이며 status 0행 — 「감사 중 정본 커밋 금지」 지켜졌다.

## ② RF-1 ~ RF-8 폐쇄표

| ID | 판정 | 근거(실출력) |
|---|---|---|
| **RF-1** | **closed** | 허용 실행값 검사 **세 자리** 각각이 판별된다 — A1(split 선별 `all` 삭제) → `I05`·`I07`·`I10`~`I13` 붉음 / A2(규격 밖 계수 `any` 삭제) → `I05`·**`I06`**·`I07`·`I10`~`I13` / A3(전건 일치 `all` 삭제) → **`I06`**. `I05`(`["read-c"]`)는 A1·A2 로, `I06`(`["read-c","read-d"]`)는 A2·A3 로 각각 붉는다 |
| **RF-2** | **partially** | ⒜ 주석·변조 H 는 **완전히 닫혔다**(아래 ④) · 총괄이 §13 에 약속한 정정 마커가 **없다** · HANDOFF 16차 줄도 무한정 「⒜ 고유 변조 없음」 유지 → **RG-1** |
| **RF-3** | **closed** | §13 재정정 실물(기제 = 「자원 경합 **가설**」) · **정정 문단 본문 859B 바이트 동일** · **원 문단 712B 바이트 동일**(「자원 경합 가설」 보존) · 골격 ⑾ 추기가 옳은 처방임을 실측(아래 ⓓ) |
| **RF-4** | **closed** | A9(규격 밖 줄을 배타 `else` 로 원복) → `I1T01` 붉음 · A7(줄·표 순서 뒤집기) → `I1T01` 붉음. 혼재에서 줄 1 + 표 행 1 이 **둘 다** 나고 순서가 단언된다 |
| **RF-5** | **closed** | A4(계수의 중복 검사 삭제) · A5(전건 일치의 `not _has_duplicate_values` 삭제) → 각각 `I08`·`I15` 붉음 |
| **RF-6** | **closed** | A6(`N` → `len(early_unclassified)`) → `I07`(항목 2·N 1) · `I1T01`(항목 2·N 1) 붉음 |
| **RF-7** | **closed** | HANDOFF:24 = 「**일시 실패 4건**([미확인] → 정정 → **재정정 RF-3** · §13)」 — 낡은 [미확인] 소멸 |
| **RF-8** | **closed** | 골격 ⒀ 개정 실물 — 두 방향(ⓐ 변조 = 전 초록·후 붉음 / ⓑ 새 시험 = 전 붉음·후 초록) + 「순수 등가 수리는 등가 증명」 + 「대조가 태우는 것이 **커밋의 실질 변경분**인지」. 이 라운드 발주문 F5 가 행마다 (i)/(ii)/등가를 표기해 개정판에 맞는다 |

**MB·MC·MD 폐쇄표** — MB-1~MB-7 · MC-1~MC-6 · MD-1~MD-6 **전건 closed**. 핵심만: MB-1(SUMMARY 행 실측 일치) · MB-2 ⓐⓑⓓ(A8 로 우선 가드 판별 · `A03` 0건 = 전건 일치 · 30사례 고유 ID) · MB-5·MC-5(행위시법 시험에 `git show`·메모리 복원 **부재** — 데이터 흐름상 `load_schema()` 한 번 · `iter_errors` **전량** 비교) · MB-6(A7) · MC-1(§18·§20 표가 행마다 축 표기) · MC-3(`I2-01` 은 회귀로 분류 · 판별은 `I07`·`I1T01`) · MC-6(30사례가 node ID 로 사례별 식별) · MD-1~6(이 발주문 자체의 정정 — ③ⓕ·Q3·Q5 에서 확인).

## ③ T35 ⑴⑵ 집행 조건표

| 조건 | 판정 | 실출력 |
|---|---|---|
| ⓐ `$ref` 결속 | **closed** | `screening_memos[].read_run` 키 = `['$comment', '$ref']` — `type`·`minLength` **부재**. `$defs.read_run.$comment` 가 `reported_by.items`·`canonical_selection.read_run`·`screening_memos[].read_run` **셋 다** 든다. 리터럴 `"read-a"` = **1회**(`$defs` 279행) |
| ⓑ reject 픽스처 | **closed** | `iter_errors` **전량 1건** · 경로 `screening_memos/0/read_run` · schema_path `properties/screening_memos/items/properties/read_run/**enum**`. accept 원본과 **정규화 diff 한 자리**(`read-a`→`read-c`). 새 accept 오류 0. 관문 = `SUMMARY: cases=50 REJECT_OK 33/33 ACCEPT_OK 15/15 VALIDATOR_SCOPE 2/2 schemas=5` (전체 행 · 문자열 일치) |
| ⓒ `maxItems: 2` | **closed** | 실재 + `$comment`. **확장-enum 차별 시험이 진짜 `maxItems` 를 문다** — 확장 enum·`maxItems` 있음 → `keywords=['maxItems']` / **`maxItems` 삭제 → `keywords=[]`** → 시험 붉음(B1). 오늘 enum 에서 길이 3 은 **전후 모두 reject**(전: `['enum']` · 후: `['maxItems','enum']`) — 레인이 §19 표에 실출력으로 남겼고(「오늘 enum 둘·길이 3 \| REJECT, `enum` \| REJECT, `enum`+`maxItems`」) 감사자가 독립 재현했다 |
| ⓓ 참조 셋 · 행위시법 | **closed** | 기존 T32 시험 **네 자리 전부** 개정(함수명 `three_references` · `$comment` 정확 일치 · `len(refs) != 2` → `!= 3` · 메모 역방향 단언 → 순방향 `expected_screening_memo`). 실런 6파일: 메모 값 전건 enum 안 · 거부 집합 = {`cim-fp-3` 최종 판정서} 하나 · 그 오류 전량이 `required`(`text_status`·`reported_by`) · `enum`·`maxItems` 위반 **0** · `runs/**` 무접촉. **기준이 이동하지 않는다** — `git show`·`before_t35`·`deepcopy(schema)` grep `tests/` 무일치(exit 1) |
| ⓔ SPEC 한 줄 | **closed** | 「값 공간의 정본은 …」 문단 **바로 뒤** 신설 문단 · ⑴⑵ · 행위시법 P-U1 · 재정 좌표 — 실물과 일치 |
| ⓕ 재정 원장 문언 | **closed** | §2 표·§4 가 집행과 전건 일치. **§3 추인 목록 11 항목이 원장 지정 좌표에 각각 대응**(마커 **9줄** — ⓖⓗ 합승 1 · ⓙⓚ 합승 1 · ⓝ+ⓟ(⒀ 신설) 합승 1 · ⓟ 는 원장이 두 문서를 지정하므로 2곳). 절 소속도 전건 일치(ⓛ→`ruling-20260902-02` §5 · ⓙⓚ→`D-04` §4 · ⓟ→`D-04` §12 + `D-20260902-02` §5 · ⓖⓗ→`D-03` §8). **줄 수 11 을 요구하면 오탐**임을 확인 |

**「T32 원장을 고치지 않고 T35 파일이 든다」는 이 리포 규율에 맞는다.** 승계가 **세 자리**에 남아 있다 — ⑴ `RULINGS-LEDGER.md`(색인 정본) T35 행이 「T32 「참조 둘」 → 「참조 셋」」을 명시 ⑵ §3 미결 두 행이 **상신 당시 문안을 보존한 채** T35 포인터로 바뀜 ⑶ `ruling-20260902-02` 자신도 §5 에 「§5 ② 상신은 재정 T35 ⑴ 로 닫혔다」를 든다. 마커가 없는 곳은 T32 §3 ① 한 자리인데, 그것은 **당시의 집행 조건**(과거 사실)이고 현행 불변식은 시험이 든다. 지적으로 세지 않는다.

## ④ 변조표 · 형태표

**Q1 ⓐ 엔진 변조 10종** (`tests/test_m22_…` 40 시험 기준선 = `40 passed`)

| 변조 | 지운 자리 | 붉은 시험 |
|---|---|---|
| A1 | split 선별의 `all(reporter in allowed_reporters)` | `I05`·`I07`·`I10`·`I11`·`I12`·`I13` (6 failed) |
| A2 | 규격 밖 계수의 `any(reporter not in allowed_reporters)` | `I05`·**`I06`**·`I07`·`I10`~`I13` (7 failed) |
| A3 | 전건 일치의 `all(reporter in allowed_reporters)` | **`I06`** (1 failed) |
| A4 | 규격 밖 계수의 `_has_duplicate_values` | `I08`·`I15` (2 failed) |
| A5 | 전건 일치의 `not _has_duplicate_values` | `I08`·`I15` (2 failed) |
| A6 | `N` → `len(early_unclassified)` | `I07`·`I1T01` (2 failed) |
| A7 | 줄·표 출력 순서 뒤집기 | `I1T01` (1 failed) |
| A8 | 귀속 없음 우선 가드(`else`) 제거 | `G01`·`G03`~`G09` (8 failed) |
| A9 | RF-4 원복(규격 밖 줄을 배타 `else` 로) | `I1T01` (1 failed) |
| **A10** | 비해시 중복 검사 → `set()` 기반 | **없음** — `40 passed` · **전체 `810 passed`** · 관문 7종 `FAILS=0` → **RG-2** |

**축 (i) 직접 재현 — 같은 새 시험 × 구 구현/구 스키마(`a90a021`)**

```
test_m22 × 구 구현 : 3 failed, 37 passed
  FAILED …attribution_shape_table[I08-duplicate-a]
  FAILED …attribution_shape_table[I15-duplicate-b]
  FAILED …attribution_shape_table[I1T01-invalid-then-one-table-row]
test_m24_read_run_vocabulary_binding × 구 스키마 : 2 failed, 3 passed
  FAILED …test_read_run_has_one_definition_three_references_and_one_literal
  FAILED …test_reported_by_max_items_survives_a_third_enum_value
합 = 5 failed, 40 passed   /  신 구현·신 스키마 = 45 passed
```

**`D-04` §18 의 총괄 자기 진술과 정확히 일치한다** — A-차별 셋(`I08`·`I15`·`I1T01`)만 붉고 나머지 27 사례는 회귀(`I05`·`I06`·`I07`·`I2-01` 포함). 스키마 변조 둘도 판별(B1 `maxItems` 삭제 → `max_items` 시험만 · B2 자유 문자열 원복 → `three_references` 시험만).

**변조 H 재현 — RF-2 ⒜ 주석의 실증**

```
계약 6행 action: escalate→halt  +  관문 동결 사본 APPROVED_FAILURE_TABLE 6행  (협조 편집)
  ① T22 단언              FAILED  ("T22 루프 뒤 합류 행이 무재시도 escalate가 아니다: {… 'action': 'halt' …}")
  ② 형제 골격 시험        1 passed
  ③ 관문 plain / -O       EXIT=0 / EXIT=0
  ④ 관문 --self-test      SELF-TEST mutations=36 rejected=36 · EXIT=0
계약 단독 변조(주석 후반 주장)
  T22 + 형제 골격 시험 둘 다 FAILED · 관문 G1 EXIT=1 ("6행 기계 필드 기대 action='escalate' 실제 'halt'")
```

주석 문언이 실물과 **한 글자도 어긋나지 않는다**. T22 대상 함수 `test_ledger_exclusions_derive_exit_retry_independently` 의 **AST 는 구·신 판 동일**(레인의 `T22_FUNCTION_AST_EQUAL=True` 검증).

**형태표 30사례 — 감사자 독립 재현**

`missing`/`invalid N`/`rows`/`agreement` 네 계수와 `I1T01` 의 `line<table` 순서까지 **§20 레인 실출력과 전건 일치**(30/30 OK · 본문 공백 0). 특히 요구된 셋 — `["read-a","read-a"]`(`I08`) = 규격 밖 1·전건 일치 0 · `[read-a]+[a,b,c]`(`I1T01`) = 규격 밖 1 + 표 1행 + 줄이 표보다 앞 · `["read-c","read-d"]`(`I06`) = 규격 밖 1·표 0.

**Q1 ⓑ 완비·배타 논증** (분석 범위 = 미분류 항목이 객체이고 `reported_by` 가 임의 JSON 값인 공간)

갈래 구조는 `if G → 줄 / else → (I? 줄) + (T 표 elif A 줄)` 이다.
- **G 참** → 줄 1개. 비지 않음.
- **G 거짓** → 모든 항목의 `reported_by` 가 truthy.
  - 항목 0건: `I=0` · `T=[]` · `all([])=True` → **A**. 비지 않음.
  - `I>0` → 규격 밖 줄. 비지 않음.
  - `I=0` → 모든 항목이 `list ∧ len<3 ∧ 전건 허용값 ∧ 무중복`, truthy 이므로 `len ∈ {1,2}`. 길이 1 이 하나라도 있으면 **T**(표), 전부 길이 2 면 A 술어가 정의상 참이므로 **A**. 어느 쪽이든 비지 않음.
- **배타** — `A` 술어 참 ⟹ 모든 항목의 규격 밖 술어가 거짓 ⟹ `I=0`. 즉 **A 는 I·T 와 상호 배타**이고, `I`·`T` 는 RF-4 처분대로 **의도적 동시 출력**이다.

**실측 뒷받침**: 33종 원자값 × 크기 0~3 = **37,060 입력 조합** 전수 — **본문 공백 0 · 예외 0 · 순서 위반 0**. 관측된 서명은 정확히 다섯 `{G}`(18,781) `{I}`(14,410) `{I,T}`(3,784) `{T}`(70) `{A}`(15) — `{I,A}`·`{T,A}`·`{}` 는 **한 건도 없다**. 논증과 실측이 일치한다.

**빈 객체 둘의 중복 검사**: 구현은 해시 가능성을 가정하지 않는다(`value in values[:index]`). 다만 **도달 불능**이다 → RG-2.

**실런 판독본 3건 전후 sha256** (같은 입력·같은 계약으로 재렌더)

| 런 | 구 구현(`a90a021`) | 신 구현(HEAD) | 디스크 원본(무접촉) |
|---|---|---|---|
| `gdm-…agent-memory` | `121db73a08e15685` | `121db73a08e15685` | `b135e50c…` 불변 |
| `…cim-fp-2` | `804c78d306665171` | `804c78d306665171` | `c82cbee2…` 불변 |
| `…cim-fp-3` | `6a9ce78aa08c3139` | `6a9ce78aa08c3139` | `4ea28cb6…` 불변 |

10-b 개정은 실런 판독본을 **한 바이트도 바꾸지 않는다**.

**Q1 ⓓ `TMPDIR` 처방의 실측**

```
TMPDIR 미지정 → tempfile.gettempdir() = /tmp
  mkdtemp("patent-docent-law-") → /tmp/…  ·  fs = tmpfs (1.5G · RAM 뒷받침)
TMPDIR 지정   → /home/laptop/…/pd-audit6-basetemp/tmp
  mkdtemp("patent-docent-law-") → 홈 fs   ·  fs = ext4 (/dev/sdd 1007G)
```

`law_repo()` 는 `tempfile.mkdtemp` 를 쓰므로 `--basetemp` 만으로는 tmpfs 를 벗어나지 못한다. **골격 ⑾ 추기는 옳은 처방이다.**

## ⑤ 신규 지적 — `RG-1` ~ `RG-3`

### RG-1 · **MED** · RF-2 처분이 약속한 §13 정정 마커가 없다 — 무한정 주장이 기록에 그대로 살아 있다
**귀책 = 총괄 처분·기록.**
**좌표** `docs/decisions/D-20260903-04-t31-t32.md:559`(§13) · `HANDOFF-NEXT.md:24`(16차) vs 약속 문언 `D-04:708`(§15 RF-2 행 「어떻게 닫나」).
**재현**
```
$ diff <(git show f40bfb6:docs/…/D-20260903-04-t31-t32.md | grep "감사자 ⒜ 고유 변조 = 없음") \
       <(grep "감사자 ⒜ 고유 변조 = 없음" docs/…/D-20260903-04-t31-t32.md)
  → 출력 없음 (바이트 동일 · 96f7582 전후 무변경)
$ grep -rn "계약 단독" docs/ HANDOFF-NEXT.md
  → §15 RF-2 행(708) · ⒝ 처분(716) · 발주자 오류 목록(720) · DISPOSITIONS(246) · 감사 원문. §13 에는 0건.
$ sed -n '24p' HANDOFF-NEXT.md
  → "… + 감사자 ⒜⒝ · … · ⒜ 고유 변조 없음). 기록 = D-20260903-04 §13(… 일시 실패 4건([미확인] → 정정 → 재정정 RF-3 …"
```
**왜 결함인가** RF-2 의 처분표는 **세 가지**를 약속했다 — ⑴ 「§13 **정정 마커**(「계약 단독 변조 안에서 없음」으로 **한정 복원**) · 커밋 메시지는 고칠 수 없으니 여기 기록」 ⑵ HANDOFF 17차 ⑶ RF ② T22 주석. **⑵⑶ 은 됐고 ⑴ 이 안 됐다.** §13:559 는 여전히 *"**감사자 ⒜ 고유 변조 = 없음**(`action: halt` · `then` 추가 · `points` 추가 셋 다 형제 골격 시험 · 관문 plain · self-test 가 함께 붉음)"* 으로, RF-2 가 지적한 **바로 그 무한정 형태**다 — 그리고 변조 H 가 실재하므로(④) 이 문장은 **거짓**이다. HANDOFF 16차 줄도 마찬가지인데, **그 줄은 같은 커밋 `96f7582` 가 RF-7 처분으로 편집했다** — 편집자가 그 줄 안에 있으면서 다른 무한정 주장을 그대로 두었다.
**같은 계열의 반복이라는 점이 격을 정한다.** §13·§15 를 함께 읽는 사람만 진실에 닿고, 「라운드 RE 에서 무슨 일이 있었나」를 §13 에서 조회하는 다음 라운드는 반증된 문장을 읽는다. 이것은 RF-3 처분이 §13 의 다른 문단에 대해 **정확히 올바르게** 한 일(재정정 마커 + 두 판본 바이트 보존)을 같은 절의 다른 줄에는 하지 않은 것이다. 신설된 골격 ⒁ 의 마지막 문장(*"총괄은 그 한정어를 기록·커밋·HANDOFF 에서 떨어뜨리지 않는다"*)은 **앞을 향한 규범**이며, 이미 떨어진 한정어를 복원하지 않는다.
**닫는 법** §13:559 에 `[정정 2026-09-05 · 재감사 2 RF-2]` 마커 한 줄(「‘없음’은 **계약 단독 변조** 공간 안의 답이다 — 계약+관문 사본 협조 편집(변조 H)에서는 T22 만 붉는다」) · HANDOFF 16차 줄 같은 처리. 구 문언은 지우지 않는다.

### RG-2 · **LOW** · 「비해시 중복 검사」는 원복해도 810 전건 초록이고, 그 이름을 단 픽스처는 그 자리에 닿지 못한다
**귀책 = 발주자(수락 조건 설계) 1차 · 저작 레인(사례 이름).**
**좌표** `engine/render/material_spec_md.py:96-98`(`_has_duplicate_values`) · `tests/test_m22_unclassified_render_notice.py` `I14-duplicate-unhashable-objects` · 발주문 v2 §1 F2 ⓒ · `D-04` §16 MB-2 「어떻게 닫나」 · 커밋 `2d01e91` 메시지(「중복 검사는 해시 가능성을 가정하지 않는다(MB-2 ⓒ)」).
**재현**
```
변조 A10:  return any(value in values[:index] …)  →  return len(set(values)) != len(values)
  tests/test_m22…            40 passed
  전체 스위트                810 passed  (exit 0)
  관문 7종                   FAILS=0
계측(37,060 입력 · 25,958 호출):
  받은 인자 종류 7  ·  해시 불가 원소를 포함한 호출 0  ·  read-a/read-b 밖 원소를 포함한 호출 0
```
**왜 결함인가** 두 호출점 모두 **허용값 검사에 가려 구조적으로 도달 불능**이다 — 계수 갈래는 `or` 사슬에서 `any(reporter not in allowed_reporters …)` 가 앞서고, 전건 일치 갈래는 `and` 사슬에서 `all(reporter in allowed_reporters …)` 가 앞선다. 어느 쪽이든 통과하면 원소는 전부 `"read-a"`/`"read-b"` 문자열이므로 **해시 가능하다.** 따라서 `set()` 판본과 현행 판본은 **도달 가능한 값 공간 전체에서 관측 동일**이고, 방어는 죽은 코드다. `I14-duplicate-unhashable-objects` 는 이름이 가리키는 속성을 태우지 못하고 **허용값 검사로** 규격 밖 1건이 된다(A1·A2·A4 어느 변조에서도 초록).
발주문 v2 F2 ⓒ 는 *"결함 주장이 아니라 **명시 요구**"* 라 적어 단락 평가 사실을 알고 있었지만, 수락 조건을 **렌더 층의 `[{}, {}]`** 로만 두었다 — 그 입력은 정의상 이 검사에 닿지 않는다. 그래서 요구는 구현됐으나 **시험은 0**이고, 골격 ⒀ 자신의 문언(*"「수리를 원복해도 전건 초록」이면 그 수리는 검증되지 않은 것이다"*)이 다시 위반됐다. **RF-1 과 같은 형태의 재발**이며, 이 라운드의 주제가 바로 그것이다.
**격 근거** 코드는 어느 판본이든 옳고 오늘 산출에 영향이 0 이라 LOW. 판별은 한 줄이면 선다 — 헬퍼 단위 시험 `_has_duplicate_values([{}, {}]) is True`(`set()` 판본은 `TypeError`).
**부기** `D-04` §21 파일럿 종결 소견은 *"감사가 발주자 오류를 새로 잡으면 그것이 medium 의 누락이다"* 라 적었다. **이것이 그 한 건이다**(M1b 3런 medium 이 F2 ⓒ 의 수락 설계를 통과시켰다).

### RG-3 · **LOW** · 이 발주문 §1 의 `96f7582` 괄호가 같은 문구를 두 번 든다
**귀책 = 발주자.**
**좌표** 재감사 3 발주문 §1 말미(MD-6 정정 과정에서 생긴 중복).
**재현**
```
"96f7582(다섯 파일 — 감사 원문 반입 + §13 재정정 · 골격 ⒀ 개정·⑾ 추기·⒁ 신설 · HANDOFF 정정 · DISPOSITIONS
          — §13 재정정 · 골격 ⒀ 개정·⑾ 추기·⒁ 신설 · HANDOFF 정정)"
```
**왜 결함인가** 사실 오류는 없고(양쪽 문구가 같은 참을 말한다) 판정도 바꾸지 않는다. 다만 발주문이 *"MD 폐쇄 = 이 문서 자체의 좌표·문언 정정 — 감사자는 남은 오기가 있으면 지적하라"* 고 명시 요구했고, 이 중복은 **그 정정 작업 자체가 남긴 것**이므로 보고한다. 「다섯 파일」 계수는 실측과 맞다(`HANDOFF-NEXT.md` · `D-20260902-02` · `D-20260903-04` · `DISPOSITIONS.md` · `docs/lessons/2026-09-05-opus-audit-round-re.md`).

## ⑥ Q3 ~ Q6

### Q3 명령되지 않은 hunk — **0건**(26 hunk 중 25 대응 + MD-5 예고분 1)

**반경 겹침 0** — `comm -12 <(…2d01e91|sort) <(…4bb2579|sort)` = **빈 출력**(교집합 0행). 실측 명령을 그대로 돌렸다.

| 커밋 | hunk | 대응 |
|---|---|---|
| `2d01e91` | `mspec @@ -95,0 +96,5` | v2 F2 ⓒ `_has_duplicate_values` ✔ |
| | `@@ -485,0 +491,9` / `-489,13 +503,2` / `-503,3 +506,2` / `-507,6 +509,17` / `-514,6 +527,4` | 3차 A① 갈래 사슬(RF-4·RF-5) + F2 ⓐ 우선 주석 ✔ |
| | `test_m22 @@ -231,5 +231,87` / `-237,14 +319,15` / `-252,14 +335,24` | A② 판별 픽스처 + F2 ⓓ 30사례 + F3 순서 단언 ✔ |
| | `test_m24_failure @@ -262,0 +263,4` | A③ T22 주석(문언 일치) ✔ |
| | **`test_m24_failure @@ -129,2 +129,2`** | **반경 밖 — MD-5**(아래) |
| `4bb2579` | schema 4 hunk · SPEC 1 · accept 신설 · manifest 1 · reject 신설 · 시험 7 hunk | B①~B④ + F4 + F6 전건 대응 ✔ |

**MD-5 판정 — 반경 위반은 실재하고, 귀책은 발주자이며, 변경은 등가·무해·불필요다.**
- **등가**: `_check_row` 가 돌려주는 값은 `type(row) is dict` **True**(yaml.safe_load 산출). `copy.deepcopy(d) == copy.deepcopy(dict(d))` **True** · 별개 객체. `dict` 서브클래스가 아니므로 `dict(d)` 가 벗길 것도 없다.
- **반경**: 3차 파트 A 는 그 파일을 「**주석만**」으로 못박았다. 함수 AST 대조 — T22 대상 함수 `test_ledger_exclusions…` **동일**, 두 줄이 든 `test_terminal_action_and_gate_escalation_fail_closed` **상이**. 즉 두 줄은 T22 함수 **밖**이고 선언 반경 **밖**이다.
- **필요성 = 없음. 그러나 레인에게 선택지가 없었다.** v2 §2 의 수락 조건이 `grep -rn 'git show\|deepcopy(schema)\|before_t35' tests/` → **exit 1(무일치)** 이고, `a90a021` 판 같은 파일 129·130 행에 `copy.deepcopy(schema)` 가 **실재했다**. 파일 전체가 아니라 `tests/` 전체를 훑는 조건이라 무관한 자리를 함께 물었다. 발주자의 형상 조건이 반경 위반을 **유도**한 것이다.
- **결론**: 총괄 판단(등가·무해·불필요 · 되돌리지 않고 감사에 넘김)에 **동의한다**. 되돌릴 필요 없다. MD-5 는 **closed** — 새 지적으로 세지 않는다. 다만 「`tests/` 전체 문자열 grep」이라는 수락 조건은 **다음 발주문에서 파일·함수 범위로 좁혀야 한다**(형상 조건이 반경을 침범한 실물 사례 · Q6 「남은 것」).
- **MC-5 판정은 문자열 부재가 아니라 데이터 흐름으로 했다**: `test_existing_run_reports_obey_read_run_enum_without_new_t35_rejections` 는 `load_schema()` **1회** → `Draft202012Validator(schema)` **1개** → 6파일 검증 → 고정 상수와 비교. 이전 스키마의 메모리 복원·비교 경로가 **함수 안에 존재하지 않는다**. `iter_errors` 는 `sorted(...)` 로 **전량** 수집되어 집합 비교되고 `next(...)` 첫 오류만 보는 자리가 없다. ✔

### Q4 총괄 기록 — **전건 사실**(신규 지적 0 · RG-1 은 §13 이므로 ②에 계상)

| 항목 | 판정 |
|---|---|
| `D-04` §18 재현표 | **감사자 독립 재현으로 전건 일치** — pytest plain `810 passed`(186.56s) · `-O` `810 passed, 1 warning`(233.82s) 둘 다 exit 0 · 관문 7종 두 모드 `FAILS=0` · SUMMARY 행 문자열 동일 · self-test `mutations=36 rejected=36` · `"read-a"` 리터럴 1 · 금지 문자열 grep 무일치 exit 1 · 무접촉 diffstat 빈 출력 · status 9항(7 M + 2 ??) · `comm -12` 0 |
| 축 (i) 직접 재현 | **일치** — 「구 구현에서 A-차별 3 + B (i) 2 만 붉음」 = `5 failed, 40 passed` · 신 = `45 passed` (④) |
| 축 (ii)·변조 H 를 레인 실출력만으로 수락 | **정직하게 고지됨**(§18 「총괄이 재실행하지 않았다 — 재감사 3 대상」 · HANDOFF ⓣ). 감사자가 **전부 직접 재현했고 전건 일치**했다 |
| 발주자 오류 12건 | **사실** — ⑴⑵ 는 `final.blocked-1.txt`(cim-fp-3 required 2건 실출력 · `SPEC_T32_COUNT 0`), ⑶ 은 `final.blocked-2.txt`(복제 원본의 `screening_memos` 가 `[]`), ⑷~⑿ 는 §16·§17 MB/MC 표와 대응. 「셋은 레인 blocked · 아홉은 M1b」 계수 맞음 |
| §19 = `final-3.txt` | **정규화 후 완전 일치**(170줄 = 170줄) · sha256 `b7766b7790a019aa…` 헤더와 일치 |
| §20 = `final-4.txt` | **정규화 후 완전 일치**(226줄 = 226줄) · sha256 `a40c2bdaec62e70d…` 헤더와 일치 · `final.txt` 와 동일 해시 |
| §21 MD 처분 · 파일럿 종결 소견 | 실물 · MD-5 총괄 판단 기재 · 러너 함정(`setsid`) 경위 · 누적 19건/기각 0 |
| 커밋 메시지 넷 | 검증 가능한 주장 전건 참. `2d01e91` 「코드 무변경(AST 동일)」은 **T22 단언 주석**에 걸린 한정 주장이고 그 함수 AST 는 실제로 동일하다(파일 AST 는 MD-5 두 줄로 상이 — §21 이 사후 기록) |
| HANDOFF 18차·추기 | 좌표 5종 전건 실재(`AUDIT-ORDER-round-rf-t35.md` · `pd-lanes/astra-m1b-audit3/` · `pd-lanes/opus-audit-round-rf-t35/` · 사본 · `SPEC-round-rf-t35-fix4.v1.md`) · 리포 안 문서 4종 실재 · MD-1 정정(§18·§19·§20) 반영됨 |
| RULINGS-LEDGER T35 집행 포인터 | 실물 — 「**T35 집행 = `4bb2579`**(라운드 RF `2d01e91` 과 한 worktree · 4차 정정 · M1b 도전 2회 경유)」 · §3 두 미결 행은 상신 문안 보존 + T35 포인터 |
| `D-20260902-02` §5 ⑿ 추기 | 실물 · 문언 정확(`setsid nohup bash <launch.sh> … &` · `STATUS` 의 `EXIT=` 로 회수) |
| DISPOSITIONS | MD 6행 + §0 등재 1행 + 행 수 정정 20차(159→165) · 관문 `check_dispositions` 두 모드 exit 0 |

### Q5 유효 발주문(3차 + v2 대체 조항 합성판)

- **§15 처분 넷 + ⒜ 를 완전히 옮겼다** — RF-1(A② 표 `[c,d]`·`[c]` 행) · RF-4(A① 혼재 + A② 표) · RF-5(A① 중복 + A② 표) · RF-6(A② N≠항목 수 두 행) · ⒜(A③ 문언 — 실물 주석과 **일치**). 재정 T35 ⑴⑵ 도 B①~B④ 에 완전히 옮겨졌다.
- **차별 대조(v2 F5)가 개정판 ⒀ 에 맞다** — 15행 전부 종류 `(i)`/`(ii)`/`등가` + 고정 대상 + 변경 축이 명시됐고(MC-1), 「등가 증명 항목 없음」 오기는 폐기되고 A③ 이 등가 항목으로 분류됐다(MB-3).
- **각 지적·조건의 폐쇄를 실제로 가른다** — 내가 돌린 변조 10종·스키마 변조 2종·축 (i) 2종 전부가 지정된 사례를 정확히 붉혔다. **형상 조건만 남은 지적은 없다** — `git status` 항목 수·`--stat` 계수는 남아 있으나 RF-1·4·5·6·⒜·T35 ⑴⑵ 각각에 행위 판별이 별도로 붙어 있다. **예외 하나가 F2 ⓒ 다**(→ RG-2).
- **⒁ 적용 ✔** — A③ 이 탐색 공간을 「계약 + 관문 동결 사본 협조 편집」으로 명시했고, 비교 집합 셋(**T22 단언 · 형제 골격 시험 · 관문 plain·`-O`·self-test**)이 v2 F5 A③ 에 적혀 있다. 「전체 스위트의 다른 넷은 별개」라는 경계도 지켜졌다.
- **MD-1~MD-6 이 이 발주문에 반영됐다** — §1 표가 §18·§19·§20 을 정확히 지시하고 `RULINGS-LEDGER` 를 기록 반경에 넣었으며(MD-1), 부모 커밋이 열에 기재됐고, Q5 가 「유효 발주 = 합성판」으로 다시 쓰였으며(MD-2), Q1 ⓐ 가 세 자리를 명시하고(MD-3), 30사례·분석 범위·완비 논증 요구가 들어갔고(MD-4), MD-5 예외가 §1 과 Q3 에 명시됐으며, `96f7582` 계수가 「다섯 파일」로 고쳐졌다(MD-6). SUMMARY 전체 행 인용 · T36 「항목별 좌표 대응 · 마커 줄 수 9」 · 핀 치환 · PASS 정의(partially/open·[미검증])도 반영됐다. **남은 오기는 RG-3 하나**.

### Q6 종결 자격

**PD-M2a 라운드 B 계열의 값과 집행은 감사상 닫혀 있다** — T24~T35 집행 · 동결 골든 · 관문 7종 두 모드 · 심은 결함 36/36 거부 · 검증기 12/12 + 42/42 · 명령되지 않은 hunk 0 · 실런 판독본 3건 전후 바이트 동일 · 두 커밋 반경 겹침 0. **그러나 「PASS」는 아니다**(신규 지적 3 · RF-2 `partially`), 계열 종결의 판정은 Owner 의 것이다. **네 라운드 연속으로 코드의 값을 바꾸는 지적은 0 이고, 지적은 전부 「고쳤다」의 증명 방식과 기록의 정합이다.**

**남은 것**(발주문이 든 넷 외에):
1. **RG-1** — §13:559 · HANDOFF 16차 줄의 한정어 복원(마커 2줄).
2. **RG-2** — `_has_duplicate_values` 헬퍼 단위 시험 1줄. 또는 도달 불능 방어임을 주석에 명기.
3. **형상 수락 조건이 반경을 침범하는 경로** — `grep -rn … tests/` 처럼 **파일 집합 전체**를 훑는 무일치 조건은 무관한 자리의 편집을 유도한다(MD-5 실물). 골격에 「금지 문자열 조건은 반경 파일·함수로 한정한다」 한 줄 값어치가 있다.
4. **Owner 사후 확인 ⓡ·ⓢ·ⓣ 열려 있음** — ⓡ(재감사 2 처분 · ⒀ 개정·⑾ 재추기·⒁ 신설) · ⓢ(M1b 상설화 방침 · 강등 없음 판정) · ⓣ(두 커밋을 한 worktree·한 레인으로 저작하고 반경별로 가른 것 · 축 (ii) 를 레인 실출력만으로 수락한 것 — **이번 감사가 축 (ii) 전건을 직접 재현했으므로 ⓣ 후반부의 근거는 보강됐다**).
5. **T36 ⑶ LANE-RUNTIME 함정 편입** — L-049·L-050 이관 때(재정으로 이연 · 리포 밖).
6. **골격 ⑿ 추기(`setsid`)** — 규율 11 재량 집행분이며 사후 확인 대상으로 아직 안 걸림.

## ⑦ [미검증]

1. **`freeze._render_parity` 의 하류 전파** — 혼재·중복 상태에서 무엇을 하는지 재지 않았다. 발화 조건을 만들려면 스키마 검증을 우회한 인공 산출물이 필요하고 그것은 러너를 거치지 않는 입력이다(전임 RE 감사와 같은 이유).
2. **10-b 완비 논증의 범위 밖** — `convergence_early["unclassified_dependents"]` 가 **리스트가 아닌** 경우(문자열·객체)와 항목이 **객체가 아닌** 경우는 발주문이 정한 분석 범위 밖이라 논증·실측 모두 하지 않았다.
3. **일시 실패(flaky) 재현** — 두 모드 각 1회씩만 돌렸고(각 810 passed) 동시 실행 재현 실험은 하지 않았다(2.9 GB 기계 금지 사항). RF-3 의 「자원 경합 가설」은 이번에도 반증도 입증도 되지 않았다.
4. **레인 `events*.jsonl` 의 내용 대조** — `final*.txt` 5종의 sha256 과 §19·§20 전문 일치만 확인했고 이벤트 로그 자체는 열지 않았다.
5. **M1b astra 3런의 USAGE 계수** — §16·§17·§21 이 든 토큰·벽시계 수치는 리포 밖 러너 산출이라 대조하지 않았다.
6. **기억 `duplicate-session-instance-trap` 정정** — 리포 밖이라 발주문 지시대로 대조하지 않았다.

---

**종료 조건**

```
$ git rev-parse HEAD          f807ad8cc7a321a9f96b9eac35e69712507a4691
$ git status --short          ?? .audit-sandbox          [행 수 1]
$ find . -name __pycache__    0        $ find . -name '*.pyc'   0
$ ls -d …/pd-audit6-basetemp  0항 (삭제됨)
$ ls -d /tmp/patent-docent-law-*   0   (/tmp 무접촉)
정본 /home/laptop/projects/patent-docent  HEAD f807ad8 · 트리 cc0433a · status 0행 (개시와 동일)
```

임시 변조 15종(엔진 10 · 스키마 2 · 계약+관문 협조 편집 1 · 축 (i) 체크아웃 2)은 전부 원상 복구했고, 사본 트리 해시가 정본과 같음을 확인했다.

VERDICT: FAIL
