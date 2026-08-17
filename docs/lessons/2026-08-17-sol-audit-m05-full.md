# sol 독립 감수 원문 — M0.5 개정 (2026-08-17)

**보존 근거.** `D-20260817-02` §5 규율 1(감수 보고 전문 보존 의무). M0 감수를 처분표로만 압축 보존한 결과 M20·M21의 개별 문언이 복원 불가가 되었다. 그 재발을 막기 위해 이 보고는 **원문 그대로** 남긴다. 처분표는 이 파일을 가리킨다.

**감수자**: GPT-5.6-sol, reasoning effort max, read-only, 교차벤더 독립 감수
**대상**: HEAD `e49eb5c`, 범위 `91567d9^..e49eb5c` (M0.5 개정 5커밋)
**판정**: **FAIL** — BLOCKER 7 / MAJOR 9 / MINOR 3
**실행 비고**: 첫 실행 10분 초과 → 재시도 1회, 정상 완료. `python3 tools/check_spec_refs.py`는 K1~K7 전부 PASS였으나 지적 대부분이 이름·파일 존재·메타스키마보다 깊은 **의미 불변식**이라 검사 범위 밖. `pytest`는 모듈 부재로 미실행.

---

## R1~R12 반영 판정

R6·R10 = PASS. R5 = 대체로 반영(N-01). 나머지 9건(R1·R2·R3·R4·R7·R8·R9·R11·R12) = FAIL.

## BLOCKER

**B-01 첫 출하가 필수 심급 없이 진행** — `docs/SPEC.md:3355`(특히 3359, 3365~3369), `:3706`. MVP가 M6~M8을 빼고 L1 veto·화행 플래그·계기·final-eyes 없이 첫 런 출하. "전부 자문 층"이라는 설명이 같은 문장의 "L1은 veto"와 모순. `lexicon.forbidden` 삭제 후 대체 방어(speech-act flag)도 첫 런엔 없어 방어 0. 반증: R7·R9·D3·D8·D9 및 "M0.5 완료" 주장. 신뢰도 높음, M0 잔존.

**B-02 "전 구성요소 3중 접지"가 공허 통과** — `reader/schemas/material-spec.schema.json:175`(190~203), `:274`, `docs/SPEC.md:1417`. `additions`에 `minItems` 없음 → 전문 있는 종속항을 `additions: []`로 두면 schema·`read.coverage` 모두 통과(실제 Draft 2020-12 검증에서 PASS 확인). 복수 element가 같은 `material_id` 공유 → grounding 1건으로 전부 덮임. `component.claim_ref` 역조건 미검사. 부수: `alternative-form` enum이 파서 규칙(`SPEC:1267`)의 단일 어형 강제로 사실상 사용 불가. 반증: R1·R3·D5·D-02의 B2/B4 "해소". `97d9a90` 신규.

**B-03 final-eyes 고정 입력으로 veto (a)/(b) 실행 불가** — `docs/SPEC.md:703~708`, `contracts/l0-format.yaml:119`, `:173`, `SPEC:2409`. 입력 ③이 `l0-format.yaml`+`lexicon/*.yaml`뿐인데 `blueprint.json`·`run.yaml`·`parameters.yaml`이 필요. 읽으면 R4 입력 격리 위반, 안 읽으면 실행 불능. 반증: R4·D8·D15·D-02 B1 "해소". `a00df05` 신규.

**B-04 round-trip veto (c) 비가역 + 시점 불일치** — `SPEC:1952`, `:1996`, `:2003~2013`, `:2052~2069`, `:884`. `Text.[M1]`과 `Text. [M1]`이 strip·index 동일 → 원본 복원 불가. `frontmatter` JSON은 YAML lexical bytes 미보존. persisted `thread.json`은 CP2 뒤 `ship` 산출인데 final-eyes는 CP2 앞. 반증: R4(c)·D8·D-02 M16 "해소".

**B-05 usage-rights 선행조건이 실제 gate에 없음** — `SPEC:516~526`(특히 520), `:904`, `:3600~3602`, `:3872`, `:3068`. `figures.publish-gate`가 boolean만 보고 Owner 재정 존재 여부(필드·결정 ID·envelope)를 전혀 읽지 않아 crop-only 도면을 재정 전 출하 가능. 반증: R11·D12. `a00df05` 신규.

**B-06 R12/D15 환류 guard에 anchors 우회 경로** — `SPEC:934~937`, `:991`, `:453`, `:808`, `:1061`, `:3009~3033`. `metrics.jsonl` 직접 읽기만 차단, 미재정 `proposed`/`provisional` 필터·별도 proposal store 없음 → `metrics → feedback proposal → anchors → design/critique`로 재정 우회. 반증: R12·D13 "재정을 거쳐서만"·D15. 신뢰도 중상.

**B-07 `numeric_whitelist`가 서로 비호환인 3개 계약** — `SPEC:2355~2365`(`{key,rationale,added_by}`+CP2), `SPEC:3206~3210`(`{pattern,reason,approved_in}`+CP1), `contracts/schemas/approval-envelope.schema.json:58~69`. 단일 loader/envelope가 양쪽 동시 충족 불가. §4 내부에서도 `added_by:"owner"`와 "3개까지 런 단위 재량" 충돌. 반증: D8·D-02 B10 "해소". M0.5 approval schema가 세 번째 계약을 실물화.

## MAJOR

**M-01** R1 수치 provenance graph 미폐쇄 — `material-spec.schema.json:68~100`, `:327~363`, `:142~161`, `SPEC:1419~1429`. `ref` 자기참조 허용·acyclic 규칙 없음, origin 조건이 타 origin 부속 필드를 금지하지 않음, bibliographic root가 자유 입력 `patent` 블록과만 대조.

**M-02** R2 EN-only 값 정책 미집행 — `SPEC:1120~1132`, schema `:282`, `:365~389`. `_en` 필드가 단순 `string`, 6개 결정론 검사에 언어 검사 없음. 한국어 `label_en` PASS 확인.

**M-03** approval envelope 자기 승인 의미론 미강제 — `approval-envelope.schema.json:23~38`, `:77~103`, `SPEC:370~379`. `approved + directives` PASS(조건부 승인 허용), 반대로 Spec 필수 `drop_decision`은 property 부재 + `additionalProperties:false`로 거부. 두 반례 실제 validator로 확인.

**M-04** R9 `n=5`가 `n≥3`으로 완화 — `SPEC:786~793`, `contracts/parameters.yaml:11~15`. 신뢰도 중간, needs confirmation.

**M-05** metrics schema가 정정·시간·비율 무결성 미보장 — `metrics-row.schema.json:8~29`, `:54~56`, `:73~83`, `SPEC:947~972`. `entry_kind:"record", corrects:"mr-999999"` PASS, `offset_h:999 + within_window:true + completion_proxy:999` PASS.

**M-06** `numeric.exhaustive` 문법이 "모든 단위·특허번호"를 토큰화 못 함 — `l0-format.yaml:176~186`, `:194~202`. `micron`이 alias에만 있고 tokenizer 단위 목록엔 없어 도달 불가; `12 kg`·`$400`은 단위 유실 후 bare-number로만 포착; `US 2026/0147854 A1` 슬래시 형식 미포착. 반증: D8·D-02 M14 "해소".

**M-07** `format.new-term-budget`이 D7 밖의 자기 입법 — `l0-format.yaml:119~122`, `SPEC:2290~2305`, `CHARTER.md:95`. DESIGN이 쓴 `blueprint.new_terms[]`를 veto의 법으로 삼음. 신뢰도 중상, M0 잔존.

**M-08** 점수 금지 lint 우회 가능 — `SPEC:2442`, `§9.18(:3898)`. 별점·A~F·`N/100` 미포착.

**M-09** (needs confirmation) D13 "verbatim 전사" 로컬 검증 불가 — `D-20260817-02:11~14`, `:39`, `CHARTER.md:195~200`. 재정 원장 원문이 리포에 없어 byte 대조 대상 부재. D13 내용이 틀렸다는 판정은 아님.

## MINOR

**N-01** advisory `total_words`가 실제 total이 아님(tail 제외) — `l0-format.yaml:145~150`, `CHARTER.md:162~164`. tail 면제는 R6 결정이지 R5 총 단어수 결정이 아님.

**N-02** K2가 wildcard 예정 파일 부재를 검사하지 않음 — `SPEC:3074`, `:3099`, `tools/check_spec_refs.py:390~406`. 또한 도구 헤더(`:8`)가 존재하지 않는 `DESIGN §12.2`를 가리킴.

**N-03** 처분 기록의 MAJOR 수 자기모순 — `D-20260817-01:5`(MAJOR 10) vs `D-20260817-02:45`(M11~M21 = 11건) vs 같은 문서 `:76`(M12~M21 = MAJOR 10건).

---

## 질문 직답 (Sol 원문)

- **`format.slot-count`** = 합법(R6 + D11 `CHARTER.md:175` 수치 문언의 직접 집행).
- **`format.stop-shape`** = **D7 위반 아님, 유지가 타당**. D11(`:170`)이 "1트윗 = 1전시물 = 도면 1장 + 2문장 이하"라는 정답을 이미 입법했고 D7(`:97`) 서식지 ②에 해당. 갤러리 예외·post당 최대 4장(`:179`) 때문에 `fig >= 1` 구현도 합리적. **Sol은 §9.17(`SPEC:3890`)의 "신설 veto이므로 별도 Owner 확인 필요"라는 전제 자체에 동의하지 않는다** — 규칙 ID를 새로 만들 때마다 재확인받으라는 메타규칙은 헌장에 없다.
- 조항별: D1·D2 충돌 없음 / D4 = M-03으로 계약 파손 / D5 = B-02로 FAIL / D6 = B-04·B-07·M-03 / D7 = 두 신설 veto는 합법이나 M-07이 진짜 jurisdiction creep / D9 = B-01·M-04로 FAIL / D14 = needs confirmation / D15 = B-06·M-08·B-01로 FAIL / D3·D8·D12는 헌장 자체는 충실하나 Spec 집행이 불충실 / D10·D11 충실.

## 계약 정합 (Sol 원문)

SPEC §6.7 표(`SPEC:3072`)는 실물과 **일치**. 계약 라인 7종 모두 일치(`material-spec/v0`, `l0-format/v0`, `parameters/v0`, `speech-acts/v1`, `defect-catalog/v0`, `approval-envelope/v0`, `metrics-row/v0`). `if/then`이 `additionalProperties:false`로 무효화되지는 **않았다**(조건부 필드가 미리 선언됨) — 실제 문제는 단방향 강제와 `else`/교차검사 부재.

## 미처분 MAJOR 재도출 (Sol 원문)

Sol은 M20/M21의 옛 문언 추측·번호 재사용을 하지 않고 현재 산출물 기준으로 위 목록 전체를 재도출했다. 유보 항목 독립 판단 = M15 family/priority는 여전히 needs confirmation(확정 finding 미포함), M17 도면 0장은 `escalate` 안전 경로가 있어 MAJOR 아님, M18 score lint는 M-08로 재확인.

## 신규 결함 귀속 (git blame, Sol 원문)

- `97d9a90`(contracts) → B-02·M-01·M-02·M-03·M-05·M-06·N-01
- `a00df05`(spec) → B-03·B-05 (+B-06는 새 guard가 기존 anchor 경로를 못 닫음)
- `e49eb5c`(decisions) → M-09·N-03
- M0 잔존 → B-01·M-04·M-07·M-08

삭제 규칙 확인: `format.word-budget`·`lexicon.forbidden`은 활성 L0 목록에 없고 `retired:`에만 존재, `coverage.advisory`·구 raw-view 금지·percentile·moving median도 활성 규율로 남아 있지 않음(즉 **삭제 자체는 충실**). 다만 각각이 남긴 빈자리가 B-01·B-02·B-06·N-01로 이어짐.

## 결론 (Sol 원문)

**FAIL** — 특히 B-01~B-07은 M1 구현 착수 전 설계 계약에서 먼저 닫아야 한다.

---

## 총괄 실측 대조 (opus-director, 감수 후 독립 재현)

감수 주장 중 기계 판정 가능한 것을 직접 재현했다. **전건 실재 확인**:

| 지적 | 재현 방법 | 결과 |
|---|---|---|
| B-02 | `additions: []`인 종속항을 Draft202012Validator에 투입 | **PASS(통과)** — 결함 실재 |
| M-01 | `derivation.inputs[0].ref`를 자기 id로 설정 | **PASS** — 자기참조 허용 실재 |
| M-01b | `origin: quoted`에 `derivation` 동시 부여 | **PASS** — origin 배타성 부재 실재 |
| M-02 | `label_en`에 한국어 문자열 투입 | **PASS** — EN 미집행 실재 |
| M-03a | `decision: approved` + `directives[]` | **PASS** — 조건부 승인 허용 실재(R8 위반) |
| M-03b | `drop_decision` 필드 투입 | **거부** — SPEC 요구 필드를 스키마가 거부, 계약 파손 실재 |
| M-05 | `entry_kind: record` + dangling `corrects`, `offset_h: 999` + `within_window: true`, `completion_proxy: 999` | **PASS** — 무결성 부재 실재 |
| M-06 | `l0-format.yaml:184` value-unit 목록 확인 | `micron`·`kg` 부재, `micron`은 alias에만 존재 — 실재 |
| N-03 | 두 처분 기록의 MAJOR 수 대조 | `D-01: MAJOR 10` vs `D-02: MAJOR 11(M11~M21)` — 모순 실재 |

**총괄 판정**: 이 감수는 정확하다. M0.5는 이름·경로·메타스키마 층위에서는 정합하나(정합 검사기 K1~K7 PASS), **의미 불변식 층위에서 미완**이다. 정합 검사기가 통과한 것이 곧 계약이 집행된다는 뜻이 아니라는 사실 자체가 이번 라운드의 교훈이다.
