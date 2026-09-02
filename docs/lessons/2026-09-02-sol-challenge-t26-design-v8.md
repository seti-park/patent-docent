# 독립 감수 원문 — 재정 T26 집행 설계 v8 의 M1b 설계 도전(7차) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-m1b-v8/final.txt` 의 sha256 `4cd2ff64da227dca6e0d59965090fa39337f474c9db6f6911808ca290cb9d166` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `codex exec --sandbox read-only --cd <정본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=`
마커 · 약 21분 · resume 없이 1차 완주). **ROUTING M1b 설계 도전의 7차 심사** — v7(6차 FAIL · Z-1·Z-2) → **v8** 에 대한 것. 도전 중 총괄이
문서 전용 커밋(`c6c3202` · 6차 원문 반입)을 넣었고 도전자는 T26 대상 경로 diff 0 을 확인해 진행했다(발주문이 고지).

**판정 = FAIL · 지적 4건(HIGH 2 · MED 2 · BLOCKER 0) · 새 재정 사항 0 · Z-1 closed · Z-2 partially · 그 밖 전건 closed(B-2·B-3 는 AA 로 partially 재기재).**
값 8,190 칸은 일곱 번째로 일치. 넷 전부 **골든 manifest 의 수락면**(T-7)이다 — **AA-1**: `check_ids` 를 집합으로만 대조해 중복 + 13번째 비활성 축
목록이 값·계수·β 전부 통과 · **AA-2**: 셀 키 우주를 고정하지 않아 `1024:1` 삭제 + 영역 밖 `0:1` 삽입이 통과 · **AA-3**: `base_commit`·`tree_head` 의
자기일관만 보고 `99fad78` 을 독립 고정하지 않음 · **AA-4**: Z-2 처분의 「B-0 시험에 동반 변조」가 무엇을 호출해 실패시킬지 없음(T-7 은 B 에서 생긴다).

지적 열거 = AA-1, AA-2, AA-3, AA-4

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§13** 에 있다.
넷 전부 **수용**(공학 · 규율 11 ③) — **v9** 에 반영하고 8차 도전에 냈다. v9 = manifest 수락면 전체를 **검증기 하나**(`validate_manifest.py` · B-0 산출 ·
엔진 무import · 최상위 키 집합 · 12 id 정확 · 키 우주 8,190 양방향 · β 2,048 고정 식 · provenance 리터럴 + 전체 해시 · 계수 재계산)로 닫고,
생성기(생성 직후 자기 검증 · 실패 시 파일 미작성) · B-0 시험(변조 사본 ⓐ~ⓖ) · 라운드 B 의 T-7 이 **같은 검증기**를 부르게 했다.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

VERDICT: FAIL

Z-1은 `closed`, Z-2는 `partially`입니다. 11행 격자와 8,190칸 값은 맞지만, v8의 β 보수는 manifest `check_ids`를 집합으로만 대조하여 중복·비활성 축 동반 변조를 통과시킵니다. 골든의 정확한 셀 키 우주와 기준 커밋 고정에도 공백이 남아 그대로 M3에 넘길 수 없습니다.

## Z-1·Z-2 우선 판정

| 지적 | 판정 | 근거 |
|---|---|---|
| Z-1 | closed | G3가 `type(max_retries) is int`를 등식 전에 검사하고, `true`·`1.0` 자기시험과 실제 YAML 변조를 모두 명시한다. `bool`·`float`·문자열 `"1"`은 관문·`_retry_budget`·존치 시험이 거부한다. 0·음수는 런타임이 int로 받지만 고정된 `retry(1)`과 예산 등식이 갈려 관문·존치 시험이 거부한다. |
| Z-2 | partially | manifest predicate를 평가하지 않고 시험 코드의 고정 convergence 비트식으로 계산하는 보수는 맞다. 그러나 `check_ids`가 정확히 12개인 순열인지 보지 않아 집합은 같지만 중복된 목록이 β·값·계수 전부를 통과한다(AA-1). 처분이 요구한 동반 변조 시험도 B-0에서 무엇을 호출해 실패시킬지 지정되지 않았다(AA-4). |

## 지적 목록

### AA-1 · HIGH · 설계 §2.8 `check_ids`·T-7 ①④ · [T29 §3①](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:169)

T-7 ①은 `check_ids`를 양방향 **집합**으로만 대조합니다. 따라서 길이와 중복을 고정하지 못합니다.

다음 변조를 실측했습니다.

- `read.pointer-resolve` 자리를 두 번째 `read.verbatim`으로 바꿈
- `read.pointer-resolve`는 목록 끝 13번째에 추가
- 실제 mask는 종전 12비트만 유지

두 검사는 같은 9행·같은 처분을 쓰므로 8,190개 키의 값은 한 칸도 바뀌지 않습니다. convergence 위치도 그대로라 β 2,048칸도 같습니다.

> `FINAL set_equal=True list_len=13 unique_len=12 value_mismatches=0 counts_equal=True beta_equal=True beta_count=2048`

즉 T-7 ①~⑥과 총괄 스크래치 값 오라클이 모두 통과하지만, T29가 명한 “검사 id 목록 = 위 12 정확히”가 깨집니다. 이는 Z-2의 “manifest에서는 순서만 읽는다”는 전제를 무너뜨리는 잔여 자기참조입니다.

닫는 법:

- `check_ids`가 JSON list인지 검사한다.
- 모든 원소가 비공 문자열인지 검사한다.
- `len(check_ids) == len(set(check_ids)) == 12`를 명시한다.
- 그 뒤에만 코드 상수 집합과 양방향 대조한다.
- 위 중복·13번째 비활성 축 변조를 음성 시험에 추가한다.

### AA-2 · HIGH · 설계 §2.8 T-7 ②③ · [T26 §3②](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-01-T24-T27.md:215) · [T28 §3①](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-02-T28-T32.md:117)

T-7은 셀 수 8,190과 manifest에 **있는** 셀의 실제 판정만 적고, 셀 키 집합 자체가 다음 정답 집합과 같은지는 명시하지 않습니다.

```python
{
    f"{mask}:{repeated}"
    for mask in range(1, 1 << 12)
    for repeated in (0, 1)
}
```

`1024:1`을 빼고 영역 밖 빈 집합 키 `0:1`을 넣어 보았습니다. 둘 다 `StageError`이므로 총수·계수·각 현존 셀 값·β 표지가 전부 유지됩니다.

> `FINAL count=8190 counts_unchanged=True present_values_match=True beta_unchanged=True missing=['1024:1'] extra=['0:1']`

M3가 manifest 키를 순회하면 이 변조를 통과시키고, 고정 range를 순회하면 거부합니다. 설계가 어느 쪽을 명하지 않은 결정 공백입니다.

닫는 법:

- top-level `cells`가 dict인지 검사한다.
- 키 집합을 위 정답 집합과 양방향 대조한다.
- mask는 정규 10진 표기 `1..4095`, repeated는 정확히 `0|1`만 허용한다.
- 누락·영역 밖 치환 변조를 T-7 음성 시험에 추가한다.
- `exceptions[].cells`도 list·문자열·중복 없음·정확히 2,048개를 명시한다.

### AA-3 · MED · 설계 §2.8 T-7 ⑥ · D-02 B-3 · T28~T32 §5⑤

T-7 ⑥은 `provenance.tree_head`와 manifest 자신의 `base_commit` 사이의 접두 관계만 봅니다. 정답 `99fad78`을 독립적으로 고정하지 않습니다.

현재 HEAD를 두 필드에 함께 적은 잘못된 manifest도 적힌 관계를 통과합니다.

> `FINAL canonical_required=99fad78 mutated_base=c6c320 mutated_tree_head=c6c3202e0c14acc78599fd59742f8b3ae00053de written_relation_passes=True`

생성 명령은 `99fad78`을 올바르게 고정하지만, 수락 시험은 그 provenance 주장을 독립적으로 검증하지 않습니다.

닫는 법:

- `base_commit == "99fad78"`을 리터럴로 대조한다.
- `provenance.tree_head == git rev-parse 99fad78` 전체 해시를 대조한다.
- 두 필드를 함께 다른 커밋으로 바꾼 변조를 음성 시험에 추가한다.

### AA-4 · MED · 설계 v8 대응표·§2.8·§5·§6 B-0 · [Z-2 처분](/home/laptop/projects/patent-docent/docs/decisions/D-20260902-02-t26-design-challenge.md:238)

Z-2 처분은 B-0 생성기 시험에 “predicate+cells 동반 변조”를 넣으라고 명합니다. 그러나 §6의 B-0 산출 시험 범위에는 인자·provenance 6종·정상 manifest 형식만 있고, 변조 manifest를 실제로 거부할 호출 대상이 없습니다.

T-7 소비자는 라운드 B에서 처음 생기므로 B-0 시험은 다음 중 하나를 임의로 골라야 합니다.

- 생성기에 별도 manifest validator를 신설
- 아직 없는 T-7을 앞당겨 작성
- 시험 코드가 자기 식을 다시 검사하는 공허한 단위 시험 작성
- 변조 시험을 라운드 B로 이동

닫는 법: 라운드 B의 `test_m24_failure_grid_golden.py`에 `_validate_beta_exception(manifest)` 같은 피검 헬퍼를 명시하고, 정상 manifest와 schema-bit predicate+cells 동반 변조가 같은 헬퍼를 각각 통과·거부하는 시험을 요구하십시오. 또는 그 validator를 B-0 산출물로 명시하고 T-7도 같은 validator를 호출하도록 범위를 고정해야 합니다.

## A. 원장 정합

| 원장 조건 | 판정 | 설계 좌표·사유 |
|---|---|---|
| T26 §2⒜① 검사 id 키 | covered | §2.1 R1/R4, §2.2, §2.6 |
| T26 §2⒜② 조치 격자·계약 순서 | covered | §2.2·§2.6; 8,190칸 값 불일치 0 |
| T26 §2⒜③ 완전성·정확 등식·부분집합 | covered | §2.3·G2~G4·`_exit_retry_eligible` |
| T26 §3① PASS 전 금지 | covered | 머리말·§0·§2.11 |
| T26 §3② 오늘 표 불변 | partially | 값은 맞지만 골든 id/셀 키 우주와 기준 커밋 검증이 불완전(AA-1~AA-3) |
| T26 §3③ 양방향 관문·세 심기 | covered | G1~G6, ⑴~㉛ |
| T26 §3④ 관문 계수 정정 | covered | §2.7·§2.10 |
| T26 §3⑤ 전수+전 관문 2모드 | covered | §2.11 |
| T28 §3① 8,190칸 한 칸도 불변 | partially | 값 모형은 전건 일치하나 정확한 셀 키 우주를 고정하지 않음(AA-1·AA-2) |
| T28 §3② β 표지 | partially | 고정 식은 맞지만 입력 id 목록의 multiplicity와 음성 시험 좌표가 열림(AA-1·AA-4) |
| T28 §3③ 실제 러너 음성·양성 | covered | §2.9 T-1/T-2 |
| T28 §3④ convergence 제외·등식 | covered | §2.3·G3 |
| T29 §3① 골든 id 12개 | partially | 집합만 같으면 중복 13항도 통과(AA-1) |
| T29 §3② 진입 예외 반증 | covered | T-3 |
| T29 §3③ input-digest 키·표지·halt·출구 제외 | covered | §2.4·G5 |
| T30 §3① kind 3종·각 1행 | covered | §2.1·G1 |
| T30 §3② checks xor kind | covered | R4·G1 |
| T30 §3③ upstream 호출자 0·deferred | covered | §2.1·§2.5·T-9 |
| T30 §3④ SPEC 문서화 | covered | §2.10 |

T31을 라운드 B 뒤로 분리하고 T32를 그 소라운드에 합친 판단은 각각 T31 §3①과 T32 §3⑤에 맞습니다. `screening_memos[].read_run` 무접촉도 맞습니다.

`judged_at`, R8/R9, 미지 id fail-closed, B-0, provenance 검사, 헬퍼와 승인 상수는 공학 재량입니다. AA-1~AA-4도 새 값 재정이 아니라 이미 정해진 골든 형식과 검증 경로를 완성하는 공학 수정입니다.

## B. 오늘의 표 불변

값 알고리즘은 PASS입니다.

| 결과 | 직접 재계산 |
|---|---:|
| `(halt, None)` | 6,144 |
| `(escalate, None)` | 1,023 |
| `(escalate, 반복 라벨)` | 1,020 |
| `StageError` | 3 |
| 합계 | 8,190 |
| β 표지 | 2,048 |
| v8 11행 모형↔HEAD 불일치 | 0 |

`StageError` 세 칸은 `1024:1`, `2048:1`, `3072:1`입니다. §2.2 손검산에서 틀린 칸은 찾지 못했습니다.

R6도 맞습니다. `select_failure_row`가 모든 후보의 `terminal_action()`을 먼저 검증하므로 미지 terminal은 [`worst_status()`](/home/laptop/projects/patent-docent/engine/stages/__init__.py:101)의 `order.get(..., 0)`에 도달하지 않습니다. 빈 후보도 `StageError`로 고정되어 있습니다.

다만 “골든 파일이 정확히 이 8,190개 입력 칸을 갖는다”는 증명은 AA-1·AA-2 때문에 아직 PASS가 아닙니다.

## C. 과거 지적 폐쇄

### B-1~B-7

| 지적 | 판정 | 사유 |
|---|---|---|
| B-1 | closed | β, 부분집합 우선, 실제 모듈 패치, 0/3 레인 대조가 선다 |
| B-2 | partially | 공식 영역을 출구 12 id로 정한 것은 닫혔으나 manifest가 정확히 12축·8,190키임을 못 고정한다(AA-1·AA-2) |
| B-3 | partially | 생성 절차와 라운드 순서는 독립적이나 T-7 provenance가 manifest 두 필드의 자기일관성만 본다(AA-3) |
| B-4 | closed | 8·9행 분리, `phases` 없는 정확 등식 |
| B-5 | closed | 세 잘못된 `then` 형태를 관문·런타임 모두 거부 |
| B-6 | closed | kind 3종, upstream 호출자 0, deferred/test_bound |
| B-7 | closed | pytest·관문 전종 두 모드 |

### V-1~V-8

| 지적 | 판정 |
|---|---|
| V-1 | closed — `read_stage.run_read_checks` 패치가 :1743에 닿음 |
| V-2 | closed — `-I`, repo 선삽입, 모듈·패키지·계약·HEAD·clean 검사 |
| V-3 | closed — 회차 1과 레인 3행 구별 |
| V-4 | closed — phase 형식·우주·중복 검사 |
| V-5 | closed — 판정점 유일성·출구 12-id 우주 |
| V-6 | closed — predicate 문자열은 실행 가능한 식 |
| V-7 | closed — terminal 어휘 상등 시험 |
| V-8 | closed — 세 StageError와 두 순서 구별 |

### N-1~N-7

| 지적 | 판정 |
|---|---|
| N-1 | closed |
| N-2 | closed — R9 위반 0 직접 재확인 |
| N-3 | closed — B-0→골든→B 순서 자체는 비순환 |
| N-4 | closed |
| N-5 | closed |
| N-6 | closed |
| N-7 | closed |

### W·X·Y 재개방

| 지적 | 판정 |
|---|---|
| W-1~W-4 | 전건 closed |
| X-1 | closed |
| X-2 | closed |
| X-3 | closed |
| Y-1 | closed |
| Y-2 | closed |
| Y-3 | closed — Z-1 타입 보수까지 완료 |
| Y-4 | closed |
| Y-5 | closed |

AA-1의 배열 multiplicity는 W-3의 계약 선언 배열 문제가 아니라 별도 manifest 배열 결함입니다.

## D. 출구 convergence 도달 가능성

“조기 통과 후 레인 페이로드만으로 출구 convergence를 실패시키는 것은 도달 불능”이라는 주장은 맞습니다.

- [`decompose_only_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:980)은 같은 [`assemble_spec()`](/home/laptop/projects/patent-docent/engine/stages/read.py:506)을 사용합니다.
- tail은 입력 `decompose`를 그대로 반환하고, 러너는 조기에 쓴 `decomposes[canonical_run]`을 넘깁니다.
- 양쪽 모두 claims를 deepcopy하고 동일한 `rewrite_claims`를 적용합니다.
- decompose가 재번호 입력의 첫 레인이어서 component 참조 매핑은 같습니다.
- 후속 합성이 바꾸는 `applicant_interest.material_id`는 convergence 6축이 읽지 않습니다.
- `peer_spec`을 읽는 코드는 [`convergence.py`](/home/laptop/projects/patent-docent/reader/lib/convergence.py:94)의 두 자리뿐입니다.

직접 조립에서는 claims 전체가 달랐지만 여섯 축은 모두 통과했습니다.

> `FINAL convergence_status=pass failed_axes=[] claims_equal=False`

peer 독립항 사본을 추가한 주입은 검사기 자체에서 `independent-count`만 fail로 만들었습니다.

> `FINAL base_convergence=pass injected_convergence=fail changed_ids=['read.convergence']`

따라서 T-1의 `engine.stages.read.run_read_checks` 패치는 실제 출구 호출점 :1743에 닿고 T28 §3③의 “실제 러너 경로”를 충족합니다. 새 루프가 부분집합 검사를 서명 비교보다 먼저 하면 convergence가 든 첫 실패에서 탈출하므로 `repeated_signature`가 서지 않습니다.

## E. 총괄 자기 신고 ①~⑳

| # | 판정 | 사유 |
|---|---|---|
| ① | 맞다 | 골든 위치는 공학 재량 |
| ② | 맞다 | T29 승인 값 |
| ③ | 맞다 | 키 이름은 원장이 설계에 위임 |
| ④ | 맞다 | T-11⑤가 두 terminal 어휘를 대조 |
| ⑤ | 맞다 | 4행 위치가 반복 라벨을 보존 |
| ⑥ | 맞다 | 모든 도달 가능한 선택 경로가 `terminal_action()`을 통과 |
| ⑦ | 맞다 | 공식 12-id 밖 무효 입력의 fail-closed |
| ⑧ | 맞다 | `action: halt`는 T29 §3③의 명시값 |
| ⑨ | 맞다 | early·exit checks를 진입 가드가 실제 읽어 승인 상수와 대조 |
| ⑩ | 맞다 | 독립항 복제가 검사기 자체의 exact-match 축을 실패시킴 |
| ⑪ | 맞다 | 표지 대상은 T28 술어 하나다. AA-1은 표지 종류가 아니라 manifest 축 multiplicity 결함 |
| ⑫ | 맞다 | T32는 T31 소라운드 합류 가능 |
| ⑬ | 맞다 | 무효 계약 형식 거부 |
| ⑭ | 맞다 | 생성 시점의 provenance 6검사와 `-I`는 충분. AA-3은 사후 T-7의 고정값 검증 결함 |
| ⑮ | 맞다 | B-0 분리 자체는 골든을 B 앞에 세움 |
| ⑯ | 맞다 | R9는 정본 실측을 대조 |
| ⑰ | 맞다 | 승인 3/8은 원장값이며 두 상수 상등 시험이 있음 |
| ⑱ | 맞다 | 선언 배열 중복 금지는 형식 규율 |
| ⑲ | 맞다 | 승인 골격은 원장값의 독립 오라클 |
| ⑳ | 맞다 | 주입은 `independent-count`를 fail로 만듦 |

새 Owner 재정이 필요한 항목은 없습니다.

## F. 관문 G1~G6

| 관문 | 판정 | 근거 |
|---|---|---|
| G1 | covered | 11행·분할·순서·action·then·label·points 고정 |
| G2 | covered | 선언↔행 차집합 양쪽 0, 선언 배열 중복 거부 |
| G3 | covered | 정확 등식·승인 3/8·엄격 int 타입·예산 1 고정 |
| G4 | covered | 유령 phase·거짓 early·exit 누락 거부 |
| G5 | covered | input-digest 표지·halt·points 부재·재시도 제외 |
| G6 | covered | `then` 없는 retry, retry인 then, 비-retry then 거부 |

⑴~㉛은 원장의 세 심기와 과거 반례를 포함합니다.

- 행 없는 검사: ⑴
- 검사 없는 행/`read.__ghost__`: ⑵
- 재시도 목록↔`retry(n)` 불일치: ⑶⑷
- 거짓 `points: [early]`: ⑽
- 동시 일관 변조: ㉑
- 선언 중복: ㉒㉓
- lane 행 병합: ㉕
- upstream action: ㉗
- 예산 값·타입: ㉙~㉛

G1~G6 자체가 통과시키는 T26 계약축 변조는 찾지 못했습니다. AA-1·AA-2는 `check_failure_table.py`가 아니라 T-7 골든 수락면을 통과하는 변조입니다.

## G. M3 결정 공백

Owner 재정 공백은 없지만 M3 공학 선택이 남습니다.

- `check_ids`를 집합만 비교할지, 정확히 12개인 순열로 검사할지
- manifest의 현존 셀을 순회할지, 정답 셀 키 집합을 먼저 생성할지
- `base_commit/tree_head` 자기일관성만 볼지, `99fad78`을 독립 고정할지
- Z-2 동반 변조 시험을 B-0의 어떤 피검 함수에 붙일지, 라운드 B로 옮길지

하나라도 있으면 FAIL이라는 기준에 따라 발주 불가입니다.

## 검증 경로

- 상태·대상 경로 불변:

  `git status --short` → 빈 출력  
  `git diff --stat edabe28 HEAD -- engine contracts reader tests tools` → 빈 출력  
  `git diff --name-only 99fad78 HEAD -- engine contracts reader | wc -l`

  > `0`

  검토 중 문서 전용 커밋이 들어와 최종 HEAD는:

  > `c6c3202`

- HEAD `_failure_verdict` 전수 호출 + 독립 v8 11행 모형:

  > `FINAL total=8190 beta=2048 mismatches=0 halt_null=6144 escalate_null=1023 escalate_repeat=1020 stage_error=3`

- Z-1 타입·값 모형:

  > `FINAL point_ids=['early', 'exit'] point_unique=True exit_ids=12 exit_unique=True r9_violations=[]`

  개별 결과는 `true`·`1.0`·`"1"` 모두 runtime/G3/test 거부, `0`·`-1`은 runtime 단독 수용이나 G3·존치 등식 거부였습니다.

- manifest 중복 축 변조:

  > `FINAL set_equal=True list_len=13 unique_len=12 value_mismatches=0 counts_equal=True beta_equal=True beta_count=2048`

- 셀 키 치환 변조:

  > `FINAL count=8190 counts_unchanged=True present_values_match=True beta_unchanged=True missing=['1024:1'] extra=['0:1']`

- provenance 동반 변조:

  > `FINAL canonical_required=99fad78 mutated_base=c6c320 mutated_tree_head=c6c3202e0c14acc78599fd59742f8b3ae00053de written_relation_passes=True`

- 조기/출구 조립:

  > `FINAL convergence_status=pass failed_axes=[] claims_equal=False`

- `peer_spec` 소비 AST 전수:

  > `FINAL peer_spec_reads=[('reader/lib/convergence.py', 94), ('reader/lib/convergence.py', 105)]`

- T-1 주입 모형:

  > `FINAL base_convergence=pass injected_convergence=fail changed_ids=['read.convergence']`

- 후속 재시도 레인 계획:

  > `FINAL retry_lane_rows=3 tasks=['ground-dependent', 'ground-independent', 'synthesize'] all_retry1=True`

- 신설물 부재:

  > `FINAL tools/check_failure_table.py=absent, tests/fixtures/read-failure-grid/generate.py=absent, tests/fixtures/read-failure-grid/manifest.json=absent, tests/test_m24_failure_grid_golden.py=absent`

## [미검증]

- 신설 생성기·manifest·T-7·관문은 아직 없어 실제 실행하지 못했습니다.
- 읽기 전용 규율 때문에 detached worktree 생성, 골든 기록, 전체 pytest, 관문 plain/`-O`, 파일 기반 T-1/T-2 통주는 실행하지 않았습니다.
- G1~G6은 구현물이 없어 설계 술어와 메모리 변조 모형으로 검증했습니다.
- v8 전문은 리포 파일이 아니라 발주문 첨부를 정본으로 읽었습니다. 6차 판정과 D-02 §12는 검토 중 문서 전용 커밋으로 반입되어 첨부와 대조했습니다.