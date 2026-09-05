# 독립 감수 원문 — 좁은 재감사(라운드 RD `87cf794` + 기록 `64e3a2c`) · opus max · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(감사 결과 `raw.json` 의 `.result` 를 `jq -r` 로 꺼낸 `out.txt` · sha256 `c9048e023ec4867665ff9c301124bd2ed5b5a2d7d3b7a12e2fc4b4377abd5383` 와 `---` 아래가 동일 · 30902 B). 레인 디렉터리 = **홈 fs** `~/projects/workspaces/pd-lanes/opus-audit-round-rd/`(`runner.sh` · `status` · `raw.json` · `out.txt` · `usage.json` · 골격 ⑿ 첫 적용).

**좌석 = opus max**(ROUTING §3 M9 · sol 저작 → opus · RD 커밋 저작 = sol-coder). CLI 직구동 `claude -p --model claude-opus-5 --effort max --output-format json`(환경변수 2종 `/proc` 실측 · LANE-RUNTIME F10 에 따라 `usage` 파일 보존 — 63턴 · 34.7분 · 출력 73,866 토큰(사고 33,926) · 캐시 읽기 5,697,732 · 캐시 생성 163,341 · 청구 $6.33) · `setsid` 배경 + `EXIT=` 마커 · 09:37:45 → 10:13:00 · EXIT=0 · stderr 0 B. 발주문 = drafts `AUDIT-ORDER-round-rd.md`(다섯 질문 · 지적 ID `RE-*` · **감사 중 정본 커밋 금지 — 지켜졌다**: 시작·종료 HEAD `64e3a2c` · tree 동일 · status 0행 · 감사자 ①). 사본 = 홈 fs `~/projects/workspaces/pd-audit-round-rd`(detached `64e3a2c` · 마커 3검증 일치) · basetemp 홈 fs `pd-audit4-basetemp`(종료 시 0항) · 사본 원상(`-uno` 0행) · 잔재 0.

**판정 = FAIL · 지적 6건(MED 1 · LOW 5) · 새 재정 사항 1(감사자 「새로 드러난 것」 ⒞ — `reported_by` 의 `maxItems: 2` 는 값 공간 축소라 총괄이 넣지 말고 상신).** **값·집행은 이번에도 닫혔다** — RD-1·RD-4·RD-5·RD-6 closed · RD-2·RD-3 partially · 명령되지 않은 hunk 0(20 hunk 전건 대응) · 실런 판독본 3건 전후 **바이트 동일** · 변조 10종 중 8종 붉음, 붉지 않은 둘(M7·M8)이 각각 RE-1·RE-4. **RE-1**(MED · 발주자 1차): RD-3 의 교체 단언 `not startswith("retry(")` 가 `action == "escalate"` 와 연언되어 **다시 항진식** — 발주문·처분표가 그 술어를 문언으로 지정했다. **RE-2**(LOW · 발주자): RD-3 양성 대조가 수리 전 단언으로도 붉어 폐쇄 증거가 아니다 — 가르는 변조는 `then` 단독. **RE-3**(LOW · 레인·발주자): 10-b 갈래 사슬에 `else` 가 없어 `reported_by` 길이 3 이상·문자열에서 **아무 줄도 나지 않는다**(오늘의 런은 스키마가 막아 닿지 않음). **RE-4**(LOW · 발주자·총괄 처분): RD-2 의 `isfile` 가드는 어떤 시험으로도 판별되지 않고, 발화하면 갓 돈 런에 「구 판 산출」이라는 거짓 출처를 낸다 · SPEC 의 「재렌더」 도구는 실물 0. **RE-5**(LOW · 총괄 기록): §10 재현표 `git status` 분해 `M 10` 은 `M 9` 의 오기. **RE-6**(LOW · 총괄 기록): `9817bec` 의 §5 편집이 폴백 항목의 「이식 단위 · READER-VERSION · N15」 단서를 둘째 항목으로 옮겨 거짓 문장을 만들었다. Q5 = 값·집행은 감사상 닫혔으나 지적 0 이 아니므로 PASS 아님 · 새로 드러난 것 셋(⒜ T22 단언의 고유 변조 미기재 ⒝ `convergence_early: Any` 형 표기 ⒞ `maxItems` 부재) · [미검증] 6(⑥ = 발주문의 「status 0행」과 마커 실재 요구가 충돌 — 발주자 오류).

지적 열거 = RE-1, RE-2, RE-3, RE-4, RE-5, RE-6

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-04-t31-t32.md` **§12** 에 있다. **전부 수용** → 라운드 **RE**(sol-coder · RE-1·RE-3·RE-4 + ⒜⒝) + RE-5·RE-6 총괄 정정(이 커밋) + 발주문 골격 ⒀(차별 대조 · 이 커밋) + ⒞ Owner 상신.

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

# 좁은 재감사 보고 — 라운드 RD (`87cf794` + `64e3a2c`) · `좌석 M9` opus max

---

## ① Preflight

**마커 3검증** (사본 루트 `.audit-sandbox` 실출력)

```
path=/home/laptop/projects/workspaces/pd-audit-round-rd     ← pwd 와 일치 ✔
pin=64e3a2cceb344b715c6a7c449d6f373af7af673b                ← git rev-parse HEAD 와 일치 ✔
order=AUDIT-round-rd-20260905
disposable=true                                              ✔
```

| 항목 | 실측 |
|---|---|
| 사본 HEAD | `64e3a2cceb344b715c6a7c449d6f373af7af673b`(detached) · 부모 사슬 `64e3a2c → 87cf794 → f709ad4 → 9817bec` ✔ |
| 사본 `git status --short` (개시) | `?? .audit-sandbox` 1행 |
| **정본 HEAD** | `64e3a2cceb344b715c6a7c449d6f373af7af673b` · tree `33d296414cb905d98ba9b413db3a9fd7ae1da59b` · branch `main` — **발주문 기재와 일치** ✔ |
| **정본 `git status --short`** | **0행** ✔ (감사 개시·종료 두 시점 모두. 감사 중 정본 커밋 없음) |
| 정본 `.worktrees/` | 무관한 런 worktree 3개(`gdm-…agent-memory` · `…cim-fp-2` · `…cim-fp-3`) · `round-rd` worktree·브랜치 제거됨 ✔ 무접촉 |
| 기준선 pytest | plain `775 passed in 131.16s` exit 0 · `PYTHONOPTIMIZE=1` `775 passed, 1 warning in 157.98s` exit 0 (순차 · basetemp 홈 fs) |
| 기준선 관문 7종 | plain·`-O` **전건 exit 0** |

`/tmp` 는 읽기(ls)만 했고 항목을 만들거나 지우지 않았다. basetemp 는 전부 `~/projects/workspaces/pd-audit4-basetemp/<라벨>` 아래에 호출별로 만들고 즉시 삭제했다(종료 시 0항).

---

## ② RD-1 ~ RD-6 폐쇄표

| ID | 판정 | 근거(실측) |
|---|---|---|
| **RD-1** | **closed** | ⑴ 실런 `runs/openai-us20260147854a1-cim-fp-3` 최종 판정서를 **구 3인자 호출** `render(spec, conv)` → 「전건 일치」 **0회** · 「조기 판정서 없음 — 구 판 산출」 **1회** ⑵ 러너 경로(실물 `convergence-early.json`) → 「전건 일치」 1회 · 「귀속 정보 없음」 0회(**오발화 없음**) ⑶ 실런 조기 판정서 3건 전부 `unclassified_dependents: []` — 빈 목록의 전건 일치는 참 ⑷ 변조 3종 전부 붉음(③표) |
| **RD-2** | **partially** | `read.py:1941-1946` 에 `isfile` 가드 실재 · SPEC §1.5 문언 교체 실재. 그러나 **그 가드를 통째로 지워도 775 시험 두 모드 전건 초록**(변조 M8) — 판별 수단 0. 새 SPEC 문언의 「구 산출 **재렌더**」 근거는 실물이 없다(`grep -rln material_spec_md tools/` → 0 · 비-tests 소비자는 `read.py` 하나) → **RE-4** |
| **RD-3** | **partially** | `"retry" in row` 는 사라졌다 ✔. 그러나 **교체된 연언이 다시 항진식**이다 — `action == "escalate"` 가 참이면 `not "escalate".startswith("retry(")` 는 항상 참. 그 연언을 삭제해도 무변조·M4·M5·M6 네 경우의 결과가 **전부 동일**하고 775 시험이 초록 → **RE-1**. §2 양성 대조는 수리 전 단언으로도 붉는다 → **RE-2** |
| **RD-4** | **closed** | 신설 `accept/convergence.canonical-read-run-read-b.json` 은 기존 accept 와 **정확히 두 자리**만 다르다(`canonical_selection.read_run` · `unclassified_dependents[0].reported_by`) · `cmp` exit 1. **판별력 실증** — 그 값을 `read-c` 로 바꾸면 `check_schema_enforcement` 가 REJECT(두 자리 각각 독립으로: `…/reported_by/items/enum` · `…/canonical_selection/read_run/enum`) → 둘째 enum 값의 양성 대조가 **실제로 성립**. manifest `basis` 문언 = 실물과 일치 |
| **RD-5** | **closed** | docstring 실물이 원장 `ruling-20260902-02` §5 ③ 의 3항(⑴ enum 부정합 ⑵ 러너 명시 전달 ⑶ 폴백 제거는 백로그)과 일치 · 구 문장 「그 값이 곧 정본이다」 소멸 · **docstring 걷어낸 AST `identical=True`** · `to_convergence_payload` 호출점 **8곳 전부** `canonical_read_run` 명시(엔진 2 · 시험 6 → 폴백 타는 호출자 **0**) · `test_m1_reader:1231` 주석 실재. 다만 백로그 개정의 부수 손상 → **RE-6** |
| **RD-6** | **closed** | `D-20260903-03` §1 의 `[재재정정 2026-09-03 · 합본 감사 RD-6]` 이 「구 인용 『발주자(총괄)』은 원문 라벨이 아니다 — 원문 `…-round-b.md:199` = 「설계(발주자)」」 로 서 있고, 그 199행 실물 = `**귀책 = 설계(발주자).**` — **일치** ✔ |

---

## ③ Q1 변조표 — 무엇을 심었고 무엇이 붉었나

| # | 변조 | 결과 | 붉은 시험 |
|---|---|---|---|
| M1 | `render()` 기본값을 다시 **갈음**으로(`if convergence_early is None: = convergence`) | **붉음** exit 1 | `test_m22::test_final_verdict_cannot_substitute_for_missing_early_verdict` · `::test_legacy_run_without_early_verdict_renders_notice_without_error` |
| M2 | 「귀속 정보 없음」 갈래 **삭제** | **붉음** exit 1 | `test_m22::test_legacy_early_item_without_attribution_does_not_declare_agreement` |
| M3 | 「전건 일치」 조건을 `== 2` → **`>= 1`** 로 완화 | **붉음** exit 1 | `test_m22::test_early_union_renders_only_split_reports_with_full_attribution` |
| M4 | 계약 lane-log 행 `action: retry(1)` **+** `then: escalate` | **붉음** | T22 단언 · 골격 시험 · 관문 self-test (3건) |
| M5 | **`then` 만** 추가(`action` 은 `escalate` 유지) | **붉음** | 같은 3건 |
| M6 | **`action: retry(1)` 만** | **붉음** | 같은 3건 |
| — | 정당한 행(무변조) | **초록** | 거짓 양성 0 ✔ |
| **M7** | T22 단언에서 **`startswith("retry(")` 연언만 삭제** | **★ 붉지 않음** — 775 시험 두 모드 초록, 그리고 M4·M5·M6 의 결과가 **전부 그대로** | **없음 → RE-1** |
| **M8** | `read.py` 의 **`isfile` 가드 통째 삭제**(RD-2 수리 원복) | **★ 붉지 않음** — 775 시험 초록 | **없음 → RE-4** |
| M9 | (참고) 구 T22 단언 복원 + M4 | **붉음** — 수리 전 단언도 §2 양성 대조를 잡는다 | → **RE-2** |
| M10 | (참고) 구 T22 단언 복원 + M5 | **초록** — M5 가 유일한 판별 변조인데 §2 는 이것을 명하지 않았다 | → **RE-2** |

**Q1 ⓐ⑶ 값 공간 전수 대조** (10-b 블록 실출력)

| 입력 | 산출 |
|---|---|
| `unclassified_dependents` 키 부재 / `[]` | 「전건 일치」(공허 참) |
| `reported_by` 키 부재 / `[]` | 「귀속 정보 없음」 — **둘을 같게 본다** |
| 전부 길이 2 | 「전건 일치」 |
| 전부 길이 1 / 길이2+길이1 혼재 | 갈린 신고 표(길이 1 행만) |
| 귀속부재 + 길이1 혼재 | 「귀속 정보 없음」 — **표가 억눌린다**(수리 전에는 표가 났다) |
| **길이 ≥3 · `reported_by` 가 문자열** | **★ 아무 줄도 나지 않는다**(수리 전에는 한 줄이 났다) → **RE-3** |

스키마는 길이 ≥3 을 막는다 — `maxItems` 선언은 **없지만** `items: enum ["read-a","read-b"]` + `uniqueItems: true` 가 상한을 2로 묶는다(실측: `read-c` REJECT · 중복 REJECT · `[]` REJECT · 키 부재 REJECT). 조기 판정서는 `write_json` 직전 `_validate_convergence` 를 거치므로 **오늘의 런은 그 구멍에 닿을 수 없다.**

---

## ④ 신규 지적 — `RE-1` ~ `RE-6`

### RE-1 · MED · RD-3 의 교체 단언이 **항진 연언을 다시 넣었다** — 고치라던 결함을 그 수리가 재현했다
**귀책 = 발주자(반경 · 술어를 문언으로 지정) 1차 · 총괄 처분(§9 가 같은 술어를 씀) · 저작 레인(충실 집행).**
**좌표** `tests/test_m24_failure_table_contract.py:264-269` · 발주문 `SPEC-round-rd.md` §1 ③ · `D-20260903-04` §9 RD-3 행.
**재현**
```python
row.get("action") == "escalate"
and not str(row.get("action", "")).startswith("retry(")   # ← 첫 연언이 참이면 항상 참
```
`and` 의 단락 평가상 둘째 연언은 `action` 이 문자열 `"escalate"` 일 때만 계산되고, 그때 `"escalate".startswith("retry(")` 는 항상 False 다. **어떤 입력으로도 판정을 바꿀 수 없다.** 실측 — 이 연언만 지우고 ⑴ 무변조 ⑵ M4 ⑶ M5 ⑷ M6 을 다시 돌리면 결과가 `passed / failed / failed / failed` 로 **완전히 동일**하고, 전체 775 시험이 초록이다.
**왜 결함인가** RD-3 의 문언 자체가 *「발화 불가 연언」·「형태만 남은 제약」* 이었다. 그 자리에서 죽은 연언 하나를 다른 죽은 연언으로 갈았다. 실제 판정은 예전처럼 `action == "escalate"` 가 다 하고, 새로 사는 것은 `"then" not in row` 하나뿐인데 그것마저 형제 시험 `test_approved_failure_skeleton_matches_contract_exactly`(키 집합 정확 일치)와 관문 self-test 가 **이미 독립으로 붉힌다**(M4·M5·M6 셋 다 3건이 붉었다). **격 — 전임이 같은 사안을 LOW 로 잡았으나, ⒜ 명시 수리 라운드에서 같은 결함이 재발했고 ⒝ 그 술어를 만든 것이 발주문·처분표의 문언이며 ⒞ 수락 명령이 그것을 걸러내지 못했다(RE-2). 세 겹이 겹쳐 MED 로 올린다.**
**고치는 비용** 연언 한 줄 삭제(`action == "escalate"` 가 이미 그것을 함의한다). `action` 이 문자열이 아닌 경우까지 막고 싶으면 `isinstance(row.get("action"), str)` 를 쓴다.

---

### RE-2 · LOW · 발주문 §2 의 **RD-3 양성 대조가 수리 전후를 구별하지 못한다** — 통과가 폐쇄의 증거가 아니다
**귀책 = 발주자 · 총괄 처분(§9 가 같은 변조를 「양성 대조」로 지정) · 총괄 기록(§10 이 그 통과를 폐쇄 증거로 인용).**
**좌표** `SPEC-round-rd.md` §2 RD-3 · `D-20260903-04` §9 RD-3 「어떻게 닫나」 말미 · §10 양성 대조 RD-3 문단.
**재현** `87cf794^` 의 **구 단언**(`row.get("action") != "escalate" or "retry" in row or "points" in row`)을 복원한 뒤 §2 가 명한 변조(`action: retry(1)` + `then: escalate`)를 걸면 → **`1 failed`**. 즉 수리를 하지 않아도 같은 양성 대조가 붉는다.
전후를 가르는 변조는 **`then` 만 추가**하는 것 하나다 — 구 단언 `1 passed` / 새 단언 `1 failed`(실측). 그 변조는 §2 에도 §4 에도 없다.
**왜 결함인가** 이 리포의 양성 대조는 *「고쳤다」를 증명하는 자리*다. 발주문이 고른 변조가 수리 이전 코드에도 붉으므로, 레인 보고 §11 의 「exit 1 · Failed: T22 …」 와 총괄 §10 의 인용은 **RD-3 의 폐쇄에 대해 아무것도 말하지 않는다**. 비용은 변조를 `then` 단독으로 바꾸거나 한 줄 더 얹는 것이다.

---

### RE-3 · LOW · RD-1 이 10-b 갈래 사슬의 **전역성**을 깨서, 승인 표면이 **아무 줄도 내지 않는** 상태가 생겼다
**귀책 = 저작 레인(선택한 형태) · 발주자(반경 ① 이 「else 는 어떻게 하나」를 적지 않음).**
**좌표** `engine/render/material_spec_md.py:484-497`.
**재현**
```
BEFORE(87cf794^)  reported_by = ["read-a","read-b","read-c"]  →  "갈린 신고 없음 — … 전건 일치"
AFTER (87cf794)   같은 입력                                    →  <<블록 본문 공백 — 아무 줄도 없다>>
```
수리 전 사슬은 `if not split_reports / else` 로 **전역**이었다. 수리 후 사슬은 `if missing_attribution / elif all(len==2) / elif split_reports` 이고 **`else` 가 없다.** `reported_by` 가 전부 비어 있지 않으면서(→ 첫 갈래 회피) 길이가 전부 2도 아니고(→ 둘째 회피) 길이 1인 항목도 하나 없으면(→ 셋째 회피) 10-b 는 제목만 남고 본문이 비어, 승인자가 **「검사가 무엇을 말했는가」를 읽을 수 없다.**
**닿을 수 있는가** 오늘은 아니다 — `write_json` 직전 `_validate_convergence` 가 서고, `enum{read-a,read-b}` + `uniqueItems` 가 길이를 2로 묶는다(실측 REJECT). **다만 그 갈래의 선언된 정의역이 「스키마를 만족하지 않는 행위시법 산출물」이다** — 「귀속 정보 없음」 갈래가 존재하는 이유가 정확히 그것이므로, 「스키마가 막는다」는 이 함수의 정의역 전체를 덮는 방어가 아니다. 그리고 **「블록은 언제나 한 줄을 낸다」를 고정하는 시험이 하나도 없다.** 비용 = `else` 한 갈래.
**같은 자리의 부수 변화(별건 아님 · 기록용)** 귀속 부재 항목과 갈린 신고가 **섞인** 조기 판정서에서, 수리 전에는 갈린 신고 표가 났으나 수리 후에는 「귀속 정보 없음」 한 줄만 나고 **표가 억눌린다**(실측). RD-1 의 의도 방향과 어긋나지는 않으나 승인 표면에서 정보가 하나 사라지는 것을 어디에도 적지 않았다.

---

### RE-4 · LOW · RD-2 의 수리에 **판별 수단이 하나도 없고**, 그 가드가 러너에서 **조용한 오표기**를 만든다
**귀책 = 발주자(§2 에 RD-2 양성 대조 없음 · §4 가 `hunk == 1` 형상만 봄) · 총괄 처분.**
**좌표** `engine/stages/read.py:1941-1946` · `docs/SPEC.md:534` · `SPEC-round-rd.md` §2·§4.
**재현 ⑴** 가드를 통째로 지워 수리 전 `convergence_early=load_json(...)` 로 되돌린 뒤 전체 스위트 → **775 passed, exit 0**. **어떤 시험도 수리본과 미수리본을 구별하지 못한다.** §4 의 RD-2 관련 명령은 `git diff … engine/stages/read.py | grep -c '^@@' → 1` 하나이고, 그것은 hunk **개수**만 세지 행위를 보지 않는다.
**재현 ⑵** 가드가 실제로 발화하는 유일한 상황(렌더 시점에 `convergence-early.json` 부재)에서 CP1 판독본은 「조기 판정서 없음 — **구 판 산출**」 을 낸다 — **갓 돈 런에 대해 「구 판」이라는 거짓 출처 주장**이다. 수리 전에는 같은 상태가 `FileNotFoundError` 로 크게 실패했다. RD-2 는 **큰 실패를 조용한 오표기로 바꿨고**, 그 자리를 무는 시험도 관문도 없다.
**재현 ⑶ (SPEC 문언)** 새 문언은 「부재 갈래는 구 산출 **재렌더**·픽스처를 위한 것」이라고 적는데, 리포에 재렌더 도구는 여전히 **0** 이다(`grep -rln "material_spec_md" tools/` → 0 · `render` 를 import 하는 비-tests 소비자는 `engine/stages/read.py` 하나 · `engine/render/__init__.py` 재수출). 픽스처 쪽은 참이다. 즉 RD-2 가 지적한 **「문서가 실물보다 넓게 말한다」가 절반 남았다.**
**왜 결함인가** RD-2 의 요지는 문서-실물 정합이었고, 그 수리가 ⒜ 검증 불가능하며 ⒝ 승인 표면에 새 거짓 진술 경로를 열었고 ⒞ 문서의 절반은 여전히 실물이 없다. 비용 = 부재 픽스처에서 러너 호출부를 한 번 도는 시험 1건, 또는 라벨을 「조기 판정서 파일 없음」처럼 출처를 주장하지 않는 문언으로.

---

### RE-5 · LOW · `D-04` §10 재현표의 `git status --short` 분해가 **틀렸고 같은 칸에서 자기모순**이다
**귀책 = 총괄 기록.**
**좌표** `docs/decisions/D-20260903-04-t31-t32.md` §10 총괄 재현표 마지막 행.
**재현** 기재 = `11항(M 10 · D 1 · ?? 1)` — 괄호 안 합은 **12** 로 앞의 **11** 과 모순된다. 실물 = **M 9 · D 1 · ?? 1 = 11**(§11 SCOPE CHECK 블록을 세어 확인 · 커밋 파일 목록 10건 + 삭제/신설 분리와 정합).
**왜 적는가** 총계는 맞고 실질 피해는 없다. 그러나 이 칸은 **「레인 보고와 총괄 재현이 같았다」를 주장하는 자리**이고, 그 주장의 근거 계수가 자기 안에서 어긋난다. 전임 감사가 RD-6 을 LOW 로 세운 것과 같은 격(인용·계수 충실성)이다.

---

### RE-6 · LOW · RD-5 ⓓ 백로그 개정이 **처분 문장을 엉뚱한 항목으로 옮겨** 거짓 문장을 만들었다
**귀책 = 총괄 기록.**
**좌표** `docs/decisions/D-20260903-04-t31-t32.md` §5 (편집 커밋 = `9817bec`).
**재현** `7355cf2` 판 §5 첫 bullet 말미:
> …러너는 항상 명시 전달하므로 실런 영향 0. **제거는 reader 이식 단위 변경(`READER-VERSION` 상호 체크 · N15 기록) — PD-M2 절차 문서 라운드 또는 historian 이식 전에 처리.**

`9817bec` 뒤 그 굵은 문장은 **둘째 bullet(「출구 재시도 8종 각각의 수리 기제」) 말미**로 옮겨 붙었다. 결과 — ⑴ 폴백 항목은 「남는 것은 **폴백 코드 자체의 제거**뿐이다」로 끝나고 **그 제거가 무엇에 걸려 있는지(이식 단위 · `READER-VERSION` 상호 체크 · N15)를 잃었다** ⑵ 둘째 항목은 「출구 재시도 검사별 행위 시험의 부재를 없애려면 reader 이식 단위 변경이 필요하다」로 읽히는데 **그것은 거짓이다**(그 시험들은 `reader/` 밖 `engine/`·`tests/` 사안이다).
**왜 적는가** RD-5 ⓓ 가 명한 실질(백로그 문언을 「코드 + 호출자 0」으로 확장)은 **이뤄졌다.** 이것은 그 편집의 부수 손상이고, 백로그는 종결 상신 뒤 다음 라운드의 좌표가 되는 문서라 틀린 전제가 그대로 다음 발주에 실린다.

---

## ⑤ Q2 · Q3 · Q4 · Q5 판정

### Q2 — 명령되지 않은 hunk: **없음** (20 hunk 전건 대응)

| 파일 | hunk | 대응 |
|---|---|---|
| `engine/render/material_spec_md.py` | **6** | RD-1 ①(센티넬 삭제 / 기본값 `None` / 갈음 블록 삭제 / `missing_attribution` 신설 / 첫 두 갈래 / `elif split_reports`) |
| `engine/stages/read.py` | 1 | RD-2 ② |
| `docs/SPEC.md` | 1 | RD-2 ② 문언 |
| `tests/test_m2_read.py` | 3 | RD-1 ①(`first`·`second` 에 `None`) · `:2529` 에 `None`+`canonical_read_run`(RD-1·RD-5 겸). **셋째 hunk의 `with_early` 신설은 발주문에 문언이 없으나 기계적 전제다** — 기본값이 `None` 이 되는 순간 `on_disk != first` 가 거짓이 되어 시험이 붉기 때문이며, 결과적으로 「디스크 판독본 = 실물 조기 판정서로 렌더한 것」이라는 **더 강한** 단언이 됐다 |
| `tests/test_m22_unclassified_render_notice.py` | 1 | RD-1 ① 시험 2건 |
| `tests/test_m24_failure_table_contract.py` | 1 | RD-3 ③ |
| accept 픽스처 · `manifest.json` | 2 + 2 | RD-4 ④ |
| `reader/lib/run_checks.py` | 1 | RD-5 ⑤ ⓐ |
| `tests/test_m1_reader.py` | 2 | RD-5 ⑤ ⓑⓒ |

**분기 재배열이 기존 「갈린 신고」 표 산출을 바꿨는가 — 실런에서는 아니다.** `87cf794^` 판을 나란히 import 해 같은 입력으로 렌더한 전후 대조:

| 입력 | 10-b 블록 | 판독본 전문 |
|---|---|---|
| T31 시험 3건 픽스처(전건 일치 · 갈린 신고 2행 · 조기 판정서 `None`) | **전부 동일** | — |
| 실런 조기 판정서 3건(`agent-memory` · `cim-fp-2` · `cim-fp-3`) | **전부 동일** | **바이트 동일**(116,891 / 99,309 / 95,696 B) |
| 구 3인자 호출(실런 3건) | **상이** — `갈린 신고 없음 … 전건 일치` → `조기 판정서 없음 — 구 판 산출` | **RD-1 의 의도된 변경** ✔ |
| 귀속부재+길이1 혼재 · 길이 ≥3 | **상이** | 앞은 의도 방향의 부작용 · 뒤는 **전역성 상실**(RE-3) |

### Q3 — 총괄 기록의 정확성: **대체로 정확 · 계수 오기 1 · 편집 부수 손상 1**

**§10 재현표 10행 — 내가 독립으로 다시 잰 것과 전건 일치.**

| 주장 | 내 실측 |
|---|---|
| pytest plain `775 passed` exit 0 | `775 passed in 131.16s` exit 0 ✔ |
| pytest `-O` `775 passed, 1 warning` exit 0 | `775 passed, 1 warning in 157.98s` exit 0 ✔ |
| 관문 7종 plain·`-O` 전건 exit 0 | 14회 호출 전건 exit 0 ✔ |
| `--self-test mutations=36 rejected=36` | `SELF-TEST mutations=36 rejected=36` exit 0 ✔ |
| `cmp` 기존 accept vs 신설 read-b → exit 1 | `differ: byte 957, line 38` exit 1 ✔ |
| docstring 걷어낸 AST `identical=True` | `True` ✔ |
| `read.py` hunk 수 = 1 | 1 ✔ |
| 보호 반경(`contracts` `tools` `runs` `read-failure-grid`) diff 없음 | 커밋 파일 목록에 전무 ✔ |
| `git status --short` 11항 | 11항 ✔ · **분해 `(M 10 · D 1 · ?? 1)` 은 틀렸다 → RE-5** |
| 병합 `c2c887b` → rebase(`f709ad4` 위) → ff | `c2c887b` 실재(부모 = `9817bec` ✔) · `git diff c2c887b 87cf794` = `HANDOFF-NEXT.md 1 +` 뿐 ✔ · rename 유사도 **R096** ✔ |

**§11 복구본 — 정합적이고, drafts 파일과 완전히 같다.**
- drafts `LANE-REPORT-round-rd.recovered.txt` 5,263 B · sha256 `c41077587c942d5d709eb6e017c2f26cc2e1f4f357185478ca95b431e32cdd08` — §10 기재 접두와 일치 ✔
- §11 본문(절 제목 제외) 5,262 B · **149행 / 149행 · 정규화 diff 0줄** — 발주문이 요구한 「정본 §11 과 같은 내용」 ✔
- **CHANGES `--stat` 산술 검증** — 레인 `10 files changed, 89 insertions(+), 85 deletions(-)`. 커밋(rename 인식) `91 insertions(+), 24 deletions(-)` 에서 rename 쌍(2 ins / 2 del)을 빼면 89 / 22, 여기에 삭제 픽스처 63행을 더하면 **89 / 85 · 10 files**(신설 read-b 는 미추적이라 stat 밖) — **정확히 일치** ✔
- **SCOPE CHECK 11행 = 커밋 파일 목록 10건 + rename 을 D+A 로 본 표현 차이** ✔
- VERIFIED 표의 관문 요약 문자열 6종을 하나씩 다시 돌려 대조 — `cases=48 REJECT_OK 32/32 ACCEPT_OK 14/14 VALIDATOR_SCOPE 2/2` · `기준선 12/12 · 변조본 42/42` · `40개 Markdown 파일 전건 통과` · `failure_rows=11 early_retry=3 exit_retry=8` · `RESULT: PASS` ×2 — **전건 일치** ✔
- §2 양성 대조 실출력(`agreement_count=0/1/0` · `early_unclassified_count=0`) — 내 재현과 일치 ✔

**커밋 메시지 두 건** — `87cf794`·`64e3a2c` 본문의 사실 주장은 전부 실물과 맞는다. 트레일러(`Co-Authored-By: Claude Fable 5.1`)는 직전 sol-coder 커밋 `794c639` 와 같은 관행이다. RD-1 을 「render 직접 호출 **2곳**」이라 적은 것은 **호출 자리(loci) 2** 를 뜻하며(`:2043-2044` 두 줄이 한 자리 · `:2521` 한 자리), 감사 원문의 좌표 표기와 같은 셈법이다 — 오기가 아니다.

**골격 ⑾ 추기 · ⑿ 신설**(`D-02` §5) — 문언이 §10 총괄 오류 2건과 정합하고, 구 문언을 지우지 않고 추기로 덧댔다 ✔.

**HANDOFF 14차** — 좌표 전부 실재: 사본 디렉터리 · drafts `AUDIT-ORDER-round-rd.md` · 레인 디렉터리 `~/projects/workspaces/pd-lanes/opus-audit-round-rd/` · basetemp `pd-audit4-basetemp` ✔. **「죽은 경로」 정정은 옳다** — 13차가 적은 두 좌표(`…/scratchpad/order-round-rd.md` · `…/scratchpad/sol-coder-round-rd/`)는 실제로 **부재**다(상위 `scratchpad/` 자체는 09-04 13:48 이후 새 파일로 다시 서 있으나, 13차가 지목한 항목은 없다).

**→ Q3 판정 = 정확하다. 계수 오기 1건(RE-5)과 백로그 편집 부수 손상 1건(RE-6)을 뺀다.**

### Q4 — 발주문 `SPEC-round-rd.md` 자체: **반경은 완전 · 수락은 절반이 판별하지 못한다**

**반경 ①~⑤ 는 §9 처분 다섯을 완전히 옮겼다** ✔ — 총괄 몫 둘(RD-4 의 `D-04` §2 인용 정정 · RD-5 ⓓ 백로그 문언)은 무접촉 반경(`docs/decisions/**`)에 걸려 레인에서 빠졌고, 둘 다 `9817bec` 에 실물로 서 있다(`[정정 2026-09-03 · 합본 감사 RD-4]` · `[확장 2026-09-03 · 합본 감사 RD-5]`) — 확인했다. 반경 ① ⓑ 는 §9 의 「없는」을 「**없거나 빈**」으로 넓혔는데 이는 코드와도 맞고 값 공간도 안 건드리는 정밀화다.
사소한 부정확 하나(지적 아님) — ⑤ 가 「**세** `to_convergence_payload` 호출에 `canonical_read_run` 명시」라 적었으나 `test_m1_reader:1231` 은 T32 라운드에서 이미 갖고 있었다(§9 는 「남은 **두** 호출점」으로 정확했다). 결과는 옳다.

**§4 수락 명령의 판별력 — 지적별로 갈린다.**

| 지적 | 수락 | 실제로 폐쇄를 판별하는가 |
|---|---|---|
| RD-1 | 전체 pytest exit 0 | **판별한다** — 시험 2건이 갈래를 문다(M1·M2·M3 전건 붉음) |
| RD-2 | `hunk == 1` + 전체 초록 | **판별하지 못한다** — 수리를 원복해도 전건 초록(**RE-4**) |
| RD-3 | §2 양성 대조 | **판별하지 못한다** — 수리 전 단언으로도 같은 변조가 붉음(**RE-2**) |
| RD-4 | `cmp` exit 1 | **부분 판별** — 「바이트 상이」는 보지만 「판별력이 생겼는가」는 보지 않는다. 무관한 필드 한 자만 달라도 통과한다. 실제로는 반경 ④ 가 바꿀 두 필드를 못 박아 결과가 옳았고, 내가 `read-c` 변조로 성립을 확인했다 |
| RD-5 | AST `identical=True` + 호출점 명시 | **판별한다** |

**§2 양성 대조 셋이 지적 다섯을 덮는가 — 아니다.** RD-2 는 대조가 **없고**(RE-4), RD-4 는 §4 `cmp` 가 대신하되 약하며, RD-3 의 대조는 있으나 **비어 있다**(RE-2). 실질로 대조가 성립한 것은 RD-1·RD-5 둘뿐이다.

### Q5 — 종결 자격: **아직 아니다**

**PD-M2a 라운드 B 계열의 값·집행은 이번에도 흔들리지 않았다.** T24~T32 집행 · 동결 골든 · 관문 7종 두 모드 · 심은 결함 36/36 거부 · 계약 변조 3종에서 거짓 음성 0 · 정당한 행에서 거짓 양성 0 — 내가 심은 열 가지 변조 중 여덟이 붉었고, 붉지 않은 둘은 **이번 라운드가 새로 만든 자리**(RE-1 · RE-4)다. 실런 3건의 판독본은 전후 바이트 동일이므로 자산층에 소급 영향도 0이다.

**그러나 이 감사는 지적 6건을 냈으므로 PASS 가 아니고, 계열 종결의 판정은 Owner 의 것이다.** 남은 것 —

1. **RE-1 ~ RE-6** — 전부 값 공간 무변경(규율 11 ③ 공학·기록·오류 수정). RE-1·RE-3·RE-4 는 각각 한두 줄, RE-5·RE-6 은 문서 한 문장.
2. 백로그 셋(`D-04` §5) — `run_checks.py:168` 폴백 제거(**reader 이식 단위 · `READER-VERSION` 상호 체크 · N15** — 이 단서가 지금 엉뚱한 항목에 붙어 있다 · RE-6) · 출구 재시도 8종 각각의 수리 기제 행위 시험 · `screening_memos[].read_run` 상신.
3. **그 밖에 새로 드러난 것 셋** — ⒜ **RD-3 이 물던 자리는 형제 시험 둘이 이미 전부 덮는다**(M4·M5·M6 셋 다 3건이 붉었다). 이 리포의 「각 도구는 하나의 주장만」 규율상 중복 자체는 결함이 아니나, T22 단언이 **고유하게** 무는 변조가 무엇인지는 아무도 적지 않았다 — 다음 라운드에서 그것을 적거나 단언의 자리를 재정의할 값어치가 있다. ⒝ **`convergence_early: Any` 라는 형 표기**가 센티넬 삭제 뒤에도 남았다(형제 인자는 `dict | None`). RD-1 의 요지가 「이 인자의 계약을 눈에 보이게 하라」였으므로 `dict | None` 이 맞다 — 오류 수정 격. ⒞ **`reported_by` 의 상한이 `maxItems` 가 아니라 `enum` 크기 + `uniqueItems` 의 우연한 곱으로만 서 있다.** 오늘 값이 둘이라 길이 2가 상한이지만, `read_run` enum 에 셋째 값이 들어오는 날 이 상한은 소리 없이 3이 되고 RE-3 의 구멍이 실물이 된다. `maxItems: 2` 는 **값 공간을 좁히는 판단**이므로 **재정 사항**이다(규율 11) — 총괄이 조용히 넣지 말 것.
4. Owner 사후 확인 ⓖ~ⓞ(HANDOFF 14차) · Owner 결정 1건(`screening_memos[].read_run` enum 결속) — 미처리 그대로.

---

## ⑥ [미검증]

1. **`final.txt` 원본과 복구본의 바이트 동일성** — §10 이 스스로 [미검증]이라 적었고 나도 잴 수 없다. 원본은 09-04 스크래치 소거로 사라졌다. 내가 확인한 것은 **복구본 = §11 절 = 149행 정규화 diff 0** 과 sha256 뿐이다.
2. **`events.jsonl`** — 복구되지 않았으므로 레인 실행의 턴 구조·resume 여부(§10 의 「1턴 완주 · resume 없음」)를 독립으로 대조하지 못했다. `status`·`runner.sh` 도 없다.
3. **RE-3 의 하류 전파** — 10-b 가 공백이 되는 상태에서 `freeze._render_parity` 가 무엇을 하는지는 재지 않았다. 발화 조건을 만들려면 스키마 검증을 우회한 인공 산출물이 필요한데, 그것은 러너를 거치지 않는 입력이라 「실런에서 무슨 일이 나는가」를 답하지 못한다.
4. **RE-4 ⑵ 의 실제 발화** — 렌더 직전에 조기 판정서를 지우는 경합을 실런에서 재현하지 않았다. 코드 경로 실측(`write_json` 무조건 · 접지 게이트 `isfile` 선행 · 렌더 하류)으로 창이 좁다는 것만 확인했다.
5. **감사 원문 대조의 범위** — RD-1~RD-6 원문과 §9 「어떻게 닫나」만 축자 대조했다. 전임 감사의 RC-*·[미검증] 항목은 전임이 closed 로 닫은 것으로 받아들였고 다시 세지 않았다.
6. **`.audit-sandbox` 와 「status 0행」의 충돌** — 발주문 §3 은 종료 시 `git status --short` **0행**을 요구하지만 preflight ① 은 그 마커의 실재를 요구하고, 마커는 추적 밖·gitignore 밖이라 두 조건이 동시에 성립하지 않는다. 발주자의 산출물을 지우지 않는 쪽을 택했다 — 아래가 종료 실출력이다.

```
$ git rev-parse HEAD
64e3a2cceb344b715c6a7c449d6f373af7af673b          ← 개시와 동일

$ git status --short
?? .audit-sandbox                                  ← 발주자가 둔 마커(개시 상태 그대로)

$ git status --short -uno                          ← 추적 파일 변경
[행 수 = 0]

$ find . -name "__pycache__" -o -name "*.pyc" | grep -v ^./.git | wc -l
0
$ ls -A ~/projects/workspaces/pd-audit4-basetemp/ | wc -l
0
```
임시 변조 10종(render 3 · 계약 3 · 시험 2 · read.py 1 · 픽스처 2)은 전부 `git checkout --` 로 되돌렸고, 대조용 임시 모듈(`engine/render/_before_rd.py`)과 작업 디렉터리(`.audit-scratch/`)는 삭제했다. 정본 리포는 HEAD·tree·status 가 개시와 같다.

---

**총평.** 값과 집행은 이번에도 버텼다 — RD-1 은 승인 표면에서 실제로 닫혔고(변조 셋이 전부 붉었다), RD-4·RD-5·RD-6 은 실물로 성립하며, 실런 판독본은 전후 바이트가 같다. FAIL 의 무게중심은 다시 **저작이 아니라 수리의 설계**다. RD-3 은 「죽은 연언을 없애라」는 지적에 대해 **발주문이 문언으로 지정한 술어가 다시 죽은 연언**이었고(RE-1), 그 폐쇄를 증명하기로 한 양성 대조는 **수리 전 코드로도 통과한다**(RE-2). RD-2 는 수리했다는 사실 자체가 **어떤 시험으로도 확인되지 않으며**(RE-4), RD-1 의 갈래 분리는 사슬의 전역성을 대가로 치렀다(RE-3). 여섯 중 넷이 「고쳤다」의 **증명 방식**에 관한 것이고, 이 리포가 스스로 세운 기준 — *「완료했다」는 주장은 증거가 아니다* — 이 이번에는 발주문 §2·§4 에 적용되지 않았다.

VERDICT: FAIL
