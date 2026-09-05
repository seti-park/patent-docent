# 독립 감수 원문 — M1b 설계 도전(gpt-6-astra high) · 좁은 재감사 7(RK · 라운드 M2a-3 · M9 fable xhigh 3회째) 발주문 · 판정 REVISE

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `cca049b4ab9c36c92115cc5c61e0f830023bf6ab1ec0b7ee3efeb330ac546504` · 12135 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-m2a3-audit/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 19:42:13 → 19:49:56 · **USAGE = input 1,143,551(cached 1,053,824) · output 10,879(reasoning 862)**. 사본 `~/projects/workspaces/pd-m1b-m2a3-audit`(detached `dee4a17` · `bundle/` = 발주문 v1(sha256 `98cfef9f…`) · SPEC v2 · 레인 보고 · 안내문). 읽기 전용 · pytest·관문 0건.

**판정 = REVISE · 1건(LOW) · 기각 0 · 발주자 귀책.** **MO-1 LOW**: Q3 의 「`FINAL` 부재」는 사실 전제 오기 — 중단 레인 `astra-m1b-m2a3v2-aborted-v1copy/` 에 `FINAL` 은 **0바이트로 실재**(항목 9 · STATUS 는 START 까지) · 정본 §41 「산출 없음」은 맞고 발주문 조건만 틀림(MD-1·MI-1·ML-4 계열) → 문안 정정. **권고 2(반영)**: ⓐ 변조별 **정확한 실패 집합** 표 — D7·D6 = {ⓙ, ⓜ3}(D6 도 ⓜ3 붉음 = 정적 추론 · `shadow_root=None` 이라 루트 해석 전 반환 → append 에서 거부 누출) · D2·D2b = {ⓚ} · D1 = {ⓛ} · D3 = {ⓜ1×3} · D4 = {ⓜ2} · D5 = {ⓜ3} · 「새 시험만 붉음」은 ⓜ3 실패를 허용(ⓜ3 도 새 시험) ⓑ 전체 plain 과 변조 실행 비겹침 한 줄. 확인 = 커밋·부모·반경(+307/−0 · 기존 함수 AST 동일 · 시험 6+헬퍼 2 · 17함수 23노드) · 843 = 835 + 8 정적 · 절 번호 · 새 시험 이름 6 · 원문 2건 바이트 포함 · §43↔final 정규화 동일 · RJ-1~4 판별 가능 · 축소 범위 정당(ⓥ 는 선례일 뿐 이번 추인 아님 · 발주문이 총괄 판단으로 명시) · allowlist 충족 · 메모리 현실적 · M9 사본 preflight 정상.

지적 열거 = MO-1

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§44**. 수용 → 발주문 정정판(v2)으로 fable xhigh 발주(사본 재핀 = 이 기록 커밋).

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

**마커 3검증 + 정본 HEAD — 읽기만**

```text
path=/home/laptop/projects/workspaces/pd-m1b-m2a3-audit
pin=dee4a172510300d3599daec1ebf23c81f7274fad
order=M1B-m2a3-audit-20260905
disposable=true

MARKER_PATH_REALPATH_MATCH=True
MARKER_PIN_HEAD_MATCH=True
MARKER_ORDER_MATCH=True

사본 HEAD 시작·종료 = dee4a172510300d3599daec1ebf23c81f7274fad
정본 HEAD 시작·종료 = dee4a172510300d3599daec1ebf23c81f7274fad

git status --short — 시작·종료 동일
?? .audit-sandbox
?? bundle/

git diff --stat HEAD — 빈 출력
```

대상 발주문 SHA256 = `98cfef9f69c2e9061d5fd119213046394dd4b47f3918bd487aec7721a1aae958`. drafts 판과 바이트 동일하다.

**REVISE — MO-1 LOW 1건.** 끊긴 곳은 Q3의 **`FINAL 부재`라는 사실 전제**다. D7의 ⓜ3 실패는 “새 시험만 붉음”과 논리적으로 충돌하지 않는다. ⓜ3도 이번에 추가한 시험이다.

pytest 수집·시험·관문·변조는 실행하지 않았다. 아래 실패 집합은 **소스 경로의 정적 판정**이며, 기존 실행 기록을 인용한 곳은 구별했다.

**MO-1 · LOW · 발주자 귀책 — 중단 레인의 ‘산출 없음’을 ‘FINAL 파일 부재’로 잘못 옮겼다**

- **좌표:** [발주문 Q3](/home/laptop/projects/workspaces/pd-m1b-m2a3-audit/bundle/AUDIT-ORDER-round-m2a3.md:24)의 `(STATUS · FINAL 부재)`.
- **근거 실출력:**

```text
aborted_entries=9
FINAL_exists=True
FINAL_size=0

EV
FINAL
PREFLIGHT
RUNNER
SPEC
SPEC-m1b-m2a3v2.md
STATUS
launch.log
launch.sh
```

[STATUS](/home/laptop/projects/workspaces/pd-lanes/astra-m1b-m2a3v2-aborted-v1copy/STATUS)는 다음과 같다.

```text
MODE=read-only
MODEL=gpt-6-astra
EFFORT=high
AUDIT_CD=/home/laptop/projects/workspaces/pd-m1b-m2a3
START=2026-09-05 18:55:48
```

- **검증 경로:** 레인 디렉터리 열거 → `FINAL.exists()`·`stat().st_size` → D-04 §41과 MN 원문 머리말의 “산출 없음” 대조. **빈 FINAL은 실재하지만 완료 보고는 없다.** 정본 기록의 “산출 없음”은 맞고 발주문의 부재 조건이 틀렸다. 중간 업데이트의 “10항”도 바로잡는다. 실제 자식 항목은 **9개**다.
- **영향:** 감사자가 올바른 중단 기록을 기록 불일치로 오판할 수 있다. 단, LOW 하나만으로 RK의 FAIL이 강제되는 것은 아니다.
- **고치는 문안 한 줄:** **“§41의 중단 기록을 레인 실물과 대조하라(STATUS의 시작·사본 경로 확인 · FINAL은 0바이트로 실재하며 완료 보고 없음).”**

MD-1·MI-1의 기록 대조 전제 혼용, MF-3·ML-4의 실물 계수·상태 오기와 같은 계열이다.

**사실 전제 대조**

| 항목 | 읽기 전용 실측 |
|---|---|
| 라운드 커밋 | `8ceea9050c9bb27cd923f38fd73b255f96215954` |
| 그 부모 | `274ff83a08b87cfba1f84fdfcbd82169619d11de` |
| 기록 커밋·부모 | `dee4a172510300d3599daec1ebf23c81f7274fad` · 부모 `8ceea9050c9bb27cd923f38fd73b255f96215954` |
| 라운드 반경 | `307 0 tests/test_m26_terminated_run_guard.py` 한 파일 |
| 기존 함수 | 기존 **모든 최상위 함수 AST 동일**. 기존 시험 11함수 본문·docstring 보존 |
| 추가 | 시험 6함수·8노드, 지원 헬퍼 2함수 |
| m26 최종 | 17시험 함수·23노드. 이전 11함수·15노드 |
| 전체 시험 수 | AST·JSON·YAML·별표 목록 전개로 **843 = 835 + 8**. 실행 통과 여부는 이번에 측정하지 않음 |
| 무접촉 반경 | `engine/ contracts/ reader/ docs/SPEC.md` 및 m2·m16 diff 빈 출력 |
| 기록 커밋 반경 | `HANDOFF-NEXT.md`와 D-04 두 파일 |
| 절 번호 | D-04 §39=1667행, §40=1675행, §41=1681행, §42=1687행, §43=1699행 |
| HANDOFF | 27차 표식과 M2a-3 병합·D7 ⓙ+ⓜ3 기록 실재 |
| 커밋 메시지 T5 | 시험 계수 없음 |

새 시험 이름 여섯도 §42와 일치한다.

| 기호 | 함수명 |
|---|---|
| ⓙ | `test_linked_worktree_rerun_uses_main_ledger_with_implicit_root` |
| ⓚ | `test_other_run_ids_in_ledger_do_not_terminate_new_run` |
| ⓛ | `test_nonfull_convergence_is_not_termination_evidence` |
| ⓜ1 | `test_indeterminate_convergence_is_fail_closed` — 파라미터 3개 |
| ⓜ2 | `test_shadow_pointer_read_error_is_fail_closed` |
| ⓜ3 | `test_unlocatable_ledger_root_is_rejected_before_dispatch` |

생산 원장은 사본·정본 모두 시작·종료 동일하다.

```text
6행
sha256=e2350e0d20d138a797153048a411cfd95c324bc2294fc977b061a61b1bb75df2
```

외부 경로도 실재한다. 집행 SPEC v2는 bundle↔drafts 바이트 동일하고, sol 레인에는 v1·v2 사본과 보고가 있다. §43↔`final.txt`는 끝 개행 정규화 후 동일하다.

```text
final.txt:
e36a4dccdabb9e9e602c7f38a48c7153c5e8d243b0b264e110811916fea53472

MM FINAL: 13646 B · lessons 도전 원문에 그대로 포함
924de0e112812a1acd76fd3c4076f24e77efe2597c05b09318923e2a559ad76a

MN FINAL: 10489 B · lessons 도전 원문에 그대로 포함
e80929d185eba081fecd86037da83aeca75fd23cfd6ce2afdf0009d8fb69a0ad
```

§40의 MM 6건 ID·격·수용 처분과 §41의 MN PASS·신규 0도 원문과 맞는다.

**Q1 변조 대응과 정확한 실패 집합**

발주문의 여덟 변조는 [전임 감사 원문 ③](/home/laptop/projects/workspaces/pd-m1b-m2a3-audit/docs/lessons/2026-09-05-fable-audit-round-m2a2.md:59)의 D1·D2·D2b·D3·D4·D5·D6·D7에 각각 대응한다. D3를 로더 예외만 제거하는 축약본으로 읽으면 안 되며, 발주문은 **전체**라고 명시해 MM-3 재발을 막았다.

아래는 **각 변조를 독립 적용하고 m26 23노드 전부를 실행할 때**의 기대다. 모든 행에서 기존 15노드는 초록이며, 열거하지 않은 새 노드도 초록이다.

| 변조 | 원문 변경 축 | 붉어야 할 새 시험의 정확한 집합 | 전체 기대 |
|---|---|---|---|
| D7 | 가드의 해석기를 `os.path.join(shadow_root or paths.repo, *SHADOW_LEDGER_RELATIVE)`로 교체 | **ⓙ, ⓜ3** | 2 failed / 21 passed |
| D6 | `ledger_evidence` 직후 `shadow_root is None`이면 `return False, None` | **ⓙ, ⓜ3** | 2 failed / 21 passed |
| D2 | `row_run_id == run_id` → `.startswith(run_id)` | ⓚ | 1 failed / 22 passed |
| D2b | 행 ID 비교 → `if True: found = True` | ⓚ | 1 failed / 22 passed |
| D1 | `phase == "full"` → `True`, 문자열 검사 유지 | ⓛ | 1 failed / 22 passed |
| D3 전체 | 판정서 로더 예외와 비객체·비문자열 phase를 부재로 처리 | ⓜ1[`{broken`], ⓜ1[`null`], ⓜ1[`{"phase": 0}`] | 3 failed / 20 passed |
| D4 | 로더의 `(OSError, UnicodeError)` → 부재 센티널 | ⓜ2 | 1 failed / 22 passed |
| D5 | `except ShadowLedgerRootError` → `return False, None` | ⓜ3 | 1 failed / 22 passed |

D7의 `2 failed, 21 passed`는 **§42에 보존된 총괄 실측**과 일치한다. D6의 두 실패는 이번 **정적 추론**이다. ⓜ3 역시 `shadow_root=None`이므로 D6이 루트 해석 전에 반환한다. 가드 통과 뒤 append의 루트 해석에서 거부가 누출되어 ⓜ3이 실패한다. 레인 D6 기록의 `1 failed, 15 passed, 7 deselected`는 이 노드를 선택하지 않았으므로 반증이 아니다.

**D7 문언 정정의 필요성:** “새 시험만 붉음”을 문자대로 읽으면 실패 집합이 새 8노드 안에 있다는 뜻이다. **ⓜ3 실패를 허용한다.** 따라서 이를 불가능한 수락 조건으로 지적하지 않는다. 다만 선택 실행과 전건 실행의 계수 혼동을 예방하도록 다음 보강은 권한다.

> **“각 변조는 m26 23노드 전건으로 실행한다. 기존 15는 모두 초록이며, 새 시험 실패 집합은 D7·D6={ⓙ,ⓜ3}, D2·D2b={ⓚ}, D1={ⓛ}, D3={ⓜ1 세 파라미터}, D4={ⓜ2}, D5={ⓜ3}이다.”**

이는 ML-3의 실행 집합 혼동과 MJ-3의 추가 실패 누락을 예방하는 문안이다.

**RJ-1~4 폐쇄를 판별할 수 있는가**

가능하다. 현재 발주문은 단순히 `StageError` 발생만 묻지 않고 근거·문언·부작용까지 지정한다.

- **RJ-1:** [ⓙ 실물](/home/laptop/projects/workspaces/pd-m1b-m2a3-audit/tests/test_m26_terminated_run_guard.py:382)은 두 번 모두 `read_stage.run(..., repo=worktree, shadow_root=None)`을 직접 호출한다. 포인터의 `root_source == "main-worktree-resolved"`, 주 원장 경로·1행, 고아 원장 부재를 확인한 뒤 포인터·판정서를 삭제한다. 재호출 뒤 바이트 불변과 `shadow_ledger` 문언을 확인하며, 생산 지문 비교는 `finally`에 있다. 필요한 reader 파일 네 개도 실제 open 추적 대상으로 명시되어 있다.
- **독립 생산 원장 측정:** 실행 전후 사본 및 정본의 고정 절대경로에 `sha256sum`을 적용하면 된다. 시험 내부 기본 해석기가 가리키는 사본 원장만으로 정본까지 검증했다고 간주하지 않아야 한다. 발주문의 독립 측정 요구는 실행 가능하다.
- **RJ-2:** 심은 두 행은 객체이고 `run_id`가 문자열이다. 현 판정 함수의 형태 검사를 통과한 후 ID 비교에 도달하므로, 잘못된 형태 때문에 성공하는 시험이 아니다.
- **RJ-3·4:** `_fresh_run_with_responses`가 `write_lane_responses` **전에** `10-read/` 부재를 검사한다. ⓜ1은 세 사유를 따로 검사하고, ⓜ2는 `IsADirectoryError` 누출을 통과로 인정하지 않는다. ⓜ3은 dispatch 0·포인터 부재를 확인한다.
- **ⓦ 표:** 새 ⓜ1~3과 기존 ⓘ1~3의 반전 후 문언·근거·부작용이 코드 경로와 맞는다. MM-1~4 및 MK-2·ML-2의 도달성 공백 재발은 발견하지 못했다.

**축소 범위·좌석·실행 규약**

축소 범위는 정당하다. 이번 커밋은 시험 추가만이고, §39와 전임 감사는 구현 적합성을 기록했다. 재감사 4 선례와 T37의 ⓥ 추인도 실재한다. 단, ⓥ는 **재감사 4의 추인 선례**이며 이번 RK를 Owner가 미리 추인했다는 뜻은 아니다. 발주문은 이번 축소를 총괄 판단으로 명시한다.

범위 밖 결함의 보고·재개 근거 규약, RJ-5의 코드 무변경·ⓦ 상신 병기, Q4의 “종결은 Owner의 것”은 명확하다. Q4는 감사상 종결 자격을 묻고 T39 선언을 넘기지 않는다. PASS 정의도 일치한다: 신규 BLOCKER/HIGH/MED 0, RJ-1~4 전건 closed, LOW 열거, Q1 변조표 미검증이면 PASS 불가.

실제 M9 사본도 별도로 읽어 확인했다.

```text
path=/home/laptop/projects/workspaces/pd-audit-round-m2a3
order=AUDIT-round-m2a3-20260905
pin=HEAD=dee4a172510300d3599daec1ebf23c81f7274fad
git status --short:
?? .audit-sandbox
```

따라서 현재 M1b 사본의 `?? bundle/`을 M9 preflight 위반으로 세면 안 된다.

안내문·러너 allowlist에는 `python3`, 지정 venv python, `git`, `cp`, `mkdir`, `env`, `bash`가 있다. Python 파일 API로 변조·임시물 삭제, `git checkout -- engine/stages/read.py`로 원복, 홈 fs basetemp 처리가 가능하다. 도구 부족에 따른 막힘은 없다.

지정 Python과 관문 7종 파일도 실재한다: `check_spec_refs`, `check_schema_enforcement`, `check_validator_enforcement`, `check_failure_table`, `check_lane_binding`, `check_lesson_authorship`, `check_dispositions`. 발주문의 환경 인자로 전체 plain 및 m26 명령을 구성할 수 있다. **실행하지 않았다.**

메모리 실측은 `MemTotal=2977412 kB`. 재감사 5의 18.5분·6의 39.3분 완주 기록과 이번 전체 plain 약 150~158초 기록을 보면, **전체 plain 1회와 변조 8회×m26을 순차 실행하는 범위는 현실적**이다. 전체·변조 실행을 겹치지 않는다는 한 줄을 덧붙이면 더 명확하다. 종료 조건은 임시 변조 원복, basetemp 정리, 알려진 `__pycache__` 삭제와 정합한다.

현재 M1b 러너의 `MODEL=gpt-6-astra`, `EFFORT=high`, 읽기 전용 설정과 `--json` 기록 경로를 확인했다. 최종 USAGE 이벤트는 아직 생성되지 않아 수치를 추정하지 않는다. 완료 시 러너의 EV에서 회수할 항목이다.

읽기 전용 유지. pytest·관문 실행 0건, `/tmp` 접근 0건, 파일 쓰기 0건.

VERDICT: REVISE