# 독립 감수 원문 — M1b 설계 도전(gpt-6-astra high) · 재감사 6(RJ · 라운드 M2a-2 · M9 fable xhigh 2회째) 발주문 · 판정 REVISE

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `8fa71c320121993508d91fe52bc9f187dfb957b002922b75d425dc15b7a5186b` · 14141 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-m2a2-audit/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 17:50:20 → 17:58:07 · **USAGE = input 1,091,245(cached 1,004,416) · output 11,019(reasoning 1,410)**. 사본 `~/projects/workspaces/pd-m1b-m2a2-audit`(detached `d043abf` · `bundle/` = 발주문 v1 · SPEC v3 · 레인 보고 · 안내문). 읽기 전용 · pytest·관문 0건(시험 색은 정적 분석).

**판정 = REVISE · 4건(MED 2 · LOW 2) · 기각 0 · 전부 발주자 귀책(ML-4 는 총괄 기록).** **ML-1 MED**: Q2 「고안 변조」 예시 6종 중 4종은 기존 시험이 이미 잡는 자리(순서 뒤집기 → ⓐ · 상시 null → ⓓⓔ · `load_yaml` 앞 → `UnboundLocalError` · 손상행 건너뛰기 → ⓘ2) — 고안의 값이 없다 · 진짜 미피복 = **비참 판정서(`phase != "full"`) 배치 없음 · 접두만 같은 다른 run_id 음성 사례 없음** · 판정서 오류/읽기 오류/루트 거부 → 정정. **ML-2 MED**: Q1① 원장 형태 프로브(`null`·`[]`·`42`·`{"run_id":null}`)에 포인터·판정서 제거 조건이 없어 앞 근거에서 단락 — 원장 검사 실행 증거가 아님(MK-2 계열 재발) → 독립 배치 + 기대 문언. **ML-3 LOW**: Q3 「m26 전건 + m25 ⑤」는 16노드(13/3)인데 §36 계수는 두 파일 24노드(13/11) → 두 파일 전건으로. **ML-4 LOW**: §36 「`read.py` +176/−10 · 10함수」는 **+177/−9 · 11함수** 의 오기 → 정정 마커. 확인 = 커밋·부모·blob·835 정적 전개·m26 11함수 15노드 표·6건 목록·T38 1:1·ⓦ 질문 적절(S2 좌표 덧붙이면 좋음)·allowlist 정합·레인 보고·M1b 원문 2건 바이트 동일.

지적 열거 = ML-1, ML-2, ML-3, ML-4

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§38**. **전부 수용** → 발주문 정정판(v2)으로 fable xhigh 감사 발주(사본 재핀 = 이 기록 커밋).

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

**마커 3검증 + 정본 HEAD**

읽기 전용 실출력:

```text
MARKER_PATH_REALPATH_MATCH = True
MARKER_PIN_HEAD_MATCH = True
MARKER_ORDER_MATCH = True
HEAD = d043abf2b4e4d7f238cea3e10f5eb634945aaa8c
CANONICAL_HEAD = d043abf2b4e4d7f238cea3e10f5eb634945aaa8c
```

- 사본: `/home/laptop/projects/workspaces/pd-m1b-m2a2-audit`
- 마커: `order=M1B-m2a2-audit-20260905`, `disposable=true`
- 정본: `/home/laptop/projects/patent-docent` — 시작·종료 HEAD 동일.
- 사본 상태: 시작·종료 모두 `?? .audit-sandbox`, `?? bundle/`. 추적 파일 diff 없음.
- 실제 M9용 사본 `pd-audit-round-m2a2`도 확인했다. 지정 pin·order와 HEAD가 일치하며 상태는 `?? .audit-sandbox` 한 줄이다.

**판정: REVISE — MED 2 · LOW 2.** 끊긴 곳은 원장 오류 프로브의 도달성 지정과 고안 변조의 추가 판별력이다. 아래 시험 색은 **코드·시험 정의의 정적 분석**이며, pytest 실행 결과가 아니다.

**ML-1 · MED — 고안 변조 예시 여섯 중 넷은 이미 새 시험이 잡는다**

좌표: [감사 발주문 Q2](/home/laptop/projects/workspaces/pd-m1b-m2a2-audit/bundle/AUDIT-ORDER-round-m2a2.md:23).

근거 실출력:

```text
m26:81   (m2.RUN_ID, evidence, "종결한 런 재호출") 문언 검사
m26:136  _expect_terminated_error(..., "shadow_pointer")
m26:208  terminated is True or "awaiting" in pointer 검사
m26:226  terminated is False or "awaiting" in pointer 검사
m26:288  position = ["before", "after"]
read.py:1652~1655  run_id 추출 뒤 판정 함수 호출
```

여섯 예시를 구체적인 코드 변경으로 해석한 예상 결과는 다음과 같다.

| 고안 예시 | 구체적인 변경·예상 결과 |
|---|---|
| 근거 순서 뒤집기 | 세 근거를 ⑶→⑵→⑴로 탐색하면 정상 완료 런에서 원장이 먼저 선택된다. **ⓐ부터 붉음**: 기대 근거 `shadow_pointer` 불일치. 포인터 손상도 원장 참에 가려져 ⓘ1이 붉어진다. |
| 판정서 `phase` 검사 제거 | 형태 검사는 유지하고 `if phase == "full":`을 무조건 참으로 바꾸면 **m26은 초록 예상**. 판정서를 남기는 배치는 모두 정상 완료의 `full`이고, 유효한 비참 판정서 배치가 없다. 단, “⑵ 분기 전체 제거”라면 지정 변조와 중복이며 ⓑ가 잡는다. |
| 원장 run_id 접두 일치 | `row_run_id == run_id`를 `row_run_id.startswith(run_id)`로 바꾸면 **m26은 초록 예상**. 같은 ID 양성 사례만 있고 접두만 같은 다른 ID 음성 사례가 없다. |
| `awaiting` 상시 `null` | 조기 포인터까지 null이면 **ⓓ 붉음**. 조기 값은 보존하고 나머지에 null을 추가해도 **ⓓ 최종 포인터·ⓔ 붉음**. |
| 가드를 `load_yaml` 앞으로, run_id 없이 | 호출 블록만 옮기면 `run_id`가 아직 바인딩되지 않아 **첫 READ 호출에서 `UnboundLocalError`**. 빈 문자열을 임의 주입하는 변형도 run_id 문언 단언 등에 걸린다. |
| 원장 손상행 건너뛰기 | JSON 파싱 예외에서 `continue`하면 **ⓘ2 두 노드 붉음**. 기대는 `종결 판정 불가`인데 동일 ID 행으로 `종결한 런 재호출`이 된다. 형태 위반까지 건너뛰면 ⓘ3도 붉다. |

따라서 순서 변경·상시 null·손상행 건너뛰기만 선택해도 “고안 ≥3”을 충족하지만, 기존 시험의 알려진 검출점을 반복하게 된다. 추가 탐색의 판별력이 약하다. 접두 일치와 비참 판정서 사례에는 실제 탐색 가치가 있다.

검증 경로: 각 변경을 `read.py`의 분기에 대응시킨 뒤, m26의 입력 배치와 최초 실패 단언을 추적했다. 전체 스위트에서의 생존까지 주장하지는 않는다.

고치는 문안 한 줄: **“고안 ≥3은 지정 변조·기존 단언의 단순 반복을 제외하고, 비참 판정서·접두만 같은 다른 run_id·판정서 오류/읽기 오류/루트 거부 등 미피복 경계를 대상으로 변경 코드·예상 검출점·실측을 적는다.”**

**ML-2 · MED — Q1의 원장 형태 위반 프로브에 앞선 근거 제거 조건이 빠졌다**

좌표: [감사 발주문 Q1①](/home/laptop/projects/workspaces/pd-m1b-m2a2-audit/bundle/AUDIT-ORDER-round-m2a2.md:22).

발주문은 `null`, `[]`, `42`, `{"run_id": null}`을 격리 원장에 넣고 직접 실행하라고 하지만, 원장 판정에 도달시키는 배치와 기대 문언을 고정하지 않는다.

근거 실출력:

```text
read.py:1120~1121  pointer_terminated → return True, pointer_evidence
read.py:1143~1144  phase == "full" → return True, convergence_evidence
read.py:1159       원장 open
read.py:1172       not isinstance(row, dict)
read.py:1180       not isinstance(row_run_id, str)
```

정상 통주 뒤 원장에만 해당 행을 넣으면 참 포인터에서 반환한다. 포인터만 지워도 full 판정서에서 반환한다. 모두 `StageError`는 발생하지만 **원장 형태 검사를 실행했다는 증거가 아니다**. MK-2의 도달성 누락 계열이 감사자 독립 프로브 문안에 남았다.

앞선 두 근거를 제거한 배치라면 실제 구현은 네 입력 모두 `StageError`를 낸다. 앞의 셋은 비객체, 마지막은 비문자열 run_id 분기에 해당하며 `AttributeError`로 새지 않는다.

검증 경로: `read.py:1121 → 1144 → 1159`의 단락 반환과 m26 ⓘ3의 `:311~312` 두 파일 삭제를 대조했다.

고치는 문안 한 줄: **“원장 형태 프로브는 포인터·convergence.json을 제거한 독립 배치에서 각 입력별 `StageError`와 ‘종결 판정 불가·shadow_ledger·run_id·원장 경로’를 확인하고 원장 바이트 불변을 단언한다.”**

**ML-3 · LOW — Q3의 실행 집합은 §36의 13실패·11통과 집합과 다르다**

좌표: [감사 발주문 Q3](/home/laptop/projects/workspaces/pd-m1b-m2a2-audit/bundle/AUDIT-ORDER-round-m2a2.md:24), [D-04 §36](/home/laptop/projects/workspaces/pd-m1b-m2a2-audit/docs/decisions/D-20260903-04-t31-t32.md:1532).

근거 실출력:

```text
Q3:  m26 전건 + m25 ⑤
§36: 새 시험 두 파일 복사
      초록 11 = ⓔ · ⓕ · m25 9건
AST: m26 15노드, m25 전체 9노드
```

Q3 문언대로 **m26 15 + ⑤ 1**을 실행하면 기대는 **13실패·3통과**다. §36의 **13실패·11통과**는 **m26 15 + m25 전체 9**의 결과다. 발주문 자체가 13/11을 직접 강제하지는 않지만, 집합 차이를 설명하지 않고 §36과 계수를 대조시킨다.

붉은 사례 분류와 사유 계열은 맞다. ⓓ는 첫 조기 상신의 원장 1행에서 실패하고, 나머지 12노드는 구 구현의 재호출 미차단으로 기대 `StageError`를 얻지 못한다.

검증 경로: 두 파일의 AST 파라미터 전개와 §36의 초록 목록 대조.

고치는 문안 한 줄: **“Q3는 m26·m25 두 파일 전건 24노드를 구 구현에 실행하여 13실패·11통과를 확인한다(⑤만 선택하면 13실패·3통과).”**

**ML-4 · LOW — §36에 증감 수와 함수 수 오기가 실재한다**

좌표: [D-04 §36](/home/laptop/projects/workspaces/pd-m1b-m2a2-audit/docs/decisions/D-20260903-04-t31-t32.md:1528), 감사 발주문 Q5의 기록 대조 대상.

근거 실출력:

```text
§36 기록: read.py +176/−10 · m26 10함수 15노드

git diff-tree --no-commit-id --numstat -r 1573591:
1    1  docs/SPEC.md
177  9  engine/stages/read.py
36   0  tests/test_m25_lane_log_disk_record.py
318  0  tests/test_m26_terminated_run_guard.py

AST m26: TOTAL 11 15
```

정확한 값은 **read.py +177/−9**, **m26 11함수·15노드**다. 사용자 판정 기준의 “10함수”도 정정해야 한다. 총합 **+532/−10**과 레인 보고의 stat은 맞는다.

이는 발주문이 만든 구현 결함이 아니라 **Q5가 검출해야 할 총괄 기록 오류**다. LOW이므로 이것만으로 M9 FAIL을 요구할 근거는 없다.

검증 경로: 커밋 numstat, m26 AST 함수·파라미터 계수, §36·§37 대조.

고치는 문안 한 줄: **“§36의 ‘+176/−10·10함수’를 ‘+177/−9·11함수’로 정정 마커를 남기고, 기존 문언은 기록으로 보존한다.”**

**나머지 사실 전제·판별 기준 확인**

커밋·부모 실출력:

```text
1573591b28e803c4fe7c979cf95822817724ed50
  parent 0d078db38922d9a75fb4198ca213d63a2331d374
d043abf2b4e4d7f238cea3e10f5eb634945aaa8c
  parent 1573591b28e803c4fe7c979cf95822817724ed50
OLD_READ_BLOB=d5d70eb02cf498ae4046ab4da5f7f506146b9a91
STATIC_FUNCTIONS=482
STATIC_NODES=835
BASE=819
```

m26 이름·파라미터는 다음과 같다. 공통 경로는 `tests/test_m26_terminated_run_guard.py`다.

| 사례 | 함수 이름 | 파라미터 |
|---|---|---|
| ⓐ | `test_terminated_rerun_is_rejected_before_every_side_effect` | 없음 |
| ⓑ | `test_legacy_run_without_pointer_uses_full_convergence` | 없음 |
| ⓒ | `test_run_with_only_ledger_row_is_rejected` | 없음 |
| ⓓ | `test_early_escalation_waits_without_ledger_then_finishes_once` | 없음 |
| ⓔ | `test_lane_pending_pointer_has_no_awaiting_marker` | 없음 |
| ⓕ | `test_new_run_with_no_termination_evidence_passes_guard` | 없음 |
| ⓖ | `test_true_pointer_alone_rejects_rerun` | 없음 |
| ⓗ | `test_false_pointer_still_falls_through_to_matching_ledger_row` | 없음 |
| ⓘ1 | `test_indeterminate_pointer_is_fail_closed` | `null`, `broken-json`, `non-bool` |
| ⓘ2 | `test_indeterminate_ledger_jsonl_is_fail_closed` | `before`, `after` |
| ⓘ3 | `test_indeterminate_ledger_row_shape_is_fail_closed` | `None`, `{"owner_decision": None}` |

11함수에서 **8 + 3 + 2 + 2 = 15노드**다. 전체 835는 시험 모듈을 실행하지 않고 AST·JSON·YAML 자료를 전개해 확인했다.

조기 상신 `terminated=False` 제거에서 붉는 **기존 6건**의 목록도 맞다.

```text
test_m22_continue_envelope_scope.py::
  test_envelope_does_not_carry_an_early_claim_failure
  test_envelope_still_carries_the_escalation_axis
  test_envelope_remains_blocked_on_the_exact_match_axis
  test_phase_gate_records_why_the_envelope_did_not_apply
test_m2_read.py::
  test_grounding_requires_convergence_verdict_or_envelope
test_m22_phase_gate_binding.py::
  test_verdict_artifact_keys_equal_actual_phase_gate_keys
```

첫 조기 반환이 참 포인터를 남기고 두 번째 호출이 가드에서 중단되는 경로다. 새 ⓓ를 합치면 지정 7건이다.

- **Q1 대응:** ①=T38③A, ②=T38②A, ③=T38①A로 1:1이다. `_load_termination_json:1069`, `_run_is_terminated:1092`, `_termination_error:1059`, `_TERMINATION_EVIDENCE_ABSENT:107`, `CONTINUE_CHECKPOINT:147` 모두 실재한다. 상수 값은 `"convergence_continue"`다.
- **읽기만·부작용 전:** 판정 함수와 적재 헬퍼의 `open`은 기본 읽기 모드다. 가드는 `load_yaml`·run_id 추출 뒤, `ensure_read_dirs:1669` 앞, `try:1723` 밖이다. Q1의 호출 계수와 파일 집합·바이트·mtime 병용은 실행 가능한 검증이다. 최종 해시 일치만으로 중간 무쓰기를 증명하는 것은 아니므로 코드·호출 검증을 함께 유지해야 한다.
- **지정 변조:** Q2 일곱 종은 집행 SPEC v3 §2(ii)의 일곱 종과 일치한다. RI-1 V6는 별도 여덟 번째 변조이며, 새 ⑤의 호출 2회 단언이 이를 잡는다. 구→신에서 ⑤는 초록→초록인 회귀다.
- **반경:** `1573591`은 위 네 파일뿐이다. `read.py` hunk는 판정 함수·진입 순서·조기 상태·포인터 인자/필드에 대응한다. 기존 시험 기대값 변경은 없다. ⑤를 위한 엔진 변경도 없다. Q4 무접촉 경로 diff는 빈 출력이다. `d043abf`의 기록 변경은 별도 대상이므로 Q4와 충돌하지 않는다.
- **좌표:** D-04 §34·§35·§36·§37은 각각 `:1514`, `:1520`, `:1526`, `:1538`에 실재한다. HANDOFF 25차와 SPEC §8.4 G-5 집행 마커도 실재한다. 구현 커밋 메시지에 시험 계수는 없다.

생산 원장은 사본·정본 모두 다음과 같다.

```text
ROWS=6
SHA256=e2350e0d20d138a797153048a411cfd95c324bc2294fc977b061a61b1bb75df2
```

drafts의 SPEC v1·v2·v3, 두 M1b 레인의 `FINAL`, sol 레인의 `final.txt`가 모두 실재한다. 대조 실출력:

```text
SPEC_BUNDLE_EQUAL=True
LANE_BUNDLE_EQUAL=True
SECTION37_NORMALIZED_EQUAL=True
FINAL_EQUAL m2a2=True
FINAL_EQUAL m2a2v2=True
LANE_SHA=1e0c13a2d6279a3f80340be119958cdb22c87a41288c80ee6424e1116ee06cbb
```

**ⓦ·감사 좌석·종료 규약**

Q5의 ⓦ 질문은 적절하다. “참 조건을 바꾸지 않는 오류 처리인지”를 감사하고, 바뀐다면 권한 문제를 지적하라는 범위다. 감사자에게 fail-open 선택이나 Owner 추인을 대신하라고 요구하지 않는다. MK 원문 `:143`과 §35 `:1522`의 **“종결의 참 조건을 바꾸지 않는 오류 처리 = S2 공학 집행 재량”**이라는 근거는 Q5에 의미상 반영됐다. S2 직접 좌표를 덧붙이면 더 명확하지만, 권한 위임 결함으로 판정하지 않는다.

안내문 `:3`, 발주문 `:30`, 실재 러너 템플릿의 allowlist가 서로 맞는다. `python3` 파일 API·`git checkout --`·`cp`로 요구된 임시 편집·삭제·원복을 수행할 수 있다. 관문 7개 파일과 venv Python도 실재한다.

2.9 GB에서 전체 스위트 두 모드 순차 요구는 현실적이다. 재감사 5의 **18.5분 완주**와 이번 레인의 순차 실행 기록이 뒷받침한다. 이번 감사의 전체 소요 시간을 보장하는 수치는 아니다.

첫 최종 응답 한 번에 전문 출력 요구, preflight·종료 상태 한 줄, basetemp 삭제, 캐시 제거가 명시돼 있다. PASS 정의도 **BLOCKER/HIGH/MED 신규 0·LOW 열거**, **Q1·Q2·Q3 필수 재현 미검증 시 FAIL**로 명확하다.

이번 도전은 파일 수정·pytest·관문·임시 변조 실행 **0건**, `/tmp` 접근·정본 쓰기 **0건**이다. 종료 시 사본 `__pycache__=0`이다. USAGE 관련해서는 레인 `STATUS`의 `MODEL=gpt-6-astra`, `EFFORT=high`, `MODE=read-only`를 관측했다. 완료 usage 이벤트의 토큰 수치는 아직 확인할 수 없다.

VERDICT: REVISE