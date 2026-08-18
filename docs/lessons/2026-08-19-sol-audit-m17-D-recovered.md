# sol 독립 감수 원문(회수분) — M1.7 분할 감수 D · 1차 사망 세션 (2026-08-19 00:09)

**STATUS: recovered(resume)**

**보존 근거.** 재정 2026-08-18 **N7 ①** — 외부 감수 산출물은 **원문 그대로** `docs/lessons/` 에 보존한다. 이 파일은 **하네스 결함으로 사망한 1차 감수 세션을 `codex exec resume` 으로 이어받아 회수한 판정**이다.

| 항목 | 값 |
|---|---|
| 의뢰 | D — 변조 반증(격리 사본 `pd-audit-m17/D`) |
| 감수자 | GPT-5.6-sol, reasoning effort max |
| 원세션 ID | `01a0156b-7d0b-7ec3-83f5-fa9cc396cbd8` |
| rollout | `~/.codex/sessions/2026/08/19/rollout-2026-08-19T00-09-21-01a0156b-7d0b-….jsonl` |
| 실행시간 | 원세션 약 9분 58초 (598s) |
| 원세션 샌드박스 | `workspace-write` (Q9-ⓐ 격리 사본 한정) |
| **사망 사유** | `timeout` CAP **600초** 직격 (구 `sol-auditor.md` 기본값). `--output-last-message` 는 턴 정상 완료 시에만 기록되므로 `$FINAL` 은 **0바이트**였다. |
| 회수 경로 | **`codex exec resume` 1회** — "추가 조사 중단, 확보된 근거만으로 즉시 최종 판정, 미확인은 미확인으로 명시" 지시 |
| 판정 발행 주체 | **resume 발행분** (원세션은 최종 판정을 내지 못하고 M4ⓑ 진행 중 사망) |

**★ resume 샌드박스에 관한 정직한 표기(중요).** 이 회수는 원세션의 `workspace-write` 가 아니라 **`-c sandbox_mode=read-only`** 로 수행했다. 사유: 회수 시점에 **동일 디렉터리 `pd-audit-m17/D` 에서 재실행 감수(CAP 2400)가 workspace-write 로 진행 중**이었고, 같은 트리에 두 번째 쓰기 세션을 붙이면 진행 중인 변조·원복 주기를 오염시킬 수 있었다. 회수는 새 조사가 아니라 판정 발행이므로 쓰기 권한이 필요 없다고 판단했다. 결과적으로 회수 판정은 **원세션이 이미 수행한 변조 실험의 결과에 근거**하며, 미수행분(M4ⓑ, M5–M8)은 Sol 스스로 **미확인**으로 명시했다.

**★ 격의 명시.** 이 판정은 **완주 판정이 아니다.** 조사가 중단된 상태에서 발행된 것이며 미확인 항목이 남아 있다. 완주분(동일 의뢰 재실행, CAP 2400)은 `2026-08-19-sol-audit-m17-full.md` 를 참조하라 — 두 판정이 어긋나면 **완주분이 우선**한다.

---

## FINAL(원문) — resume 세션의 `--output-last-message` 파일 그대로

NEW BLOCKER: 동일한 `input_digest` 아래 실제 인라인 절차가 바뀔 수 있습니다. 지문은 `prompt_path`만 해시하지만 [contract.py](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/lanes/contract.py:141), 요청서는 그 경로의 현재 내용을 다시 인라인합니다 [contract.py](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/lanes/contract.py:225). 실제 `_dispatch` 재진입에서 [request.md](/home/laptop/projects/workspaces/pd-audit-m17/D/runs/openai-us20260147854a1-cim-fp-3/10-read/lanes/read-b/decompose/retry-1/batch-0/request.md:178)가 재작성됐지만 지문 `8bcb…`는 그대로였습니다. 따라서 한 지문이 서로 다른 실제 프롬프트를 가리킬 수 있어 P-12의 시점 결속을 막습니다.

VERDICT: FAIL  
판정 이유: 위 NEW BLOCKER가 있으며, 중단 지시에 따라 M4ⓑ와 M5–M8은 미확인입니다.  
핀 대조: `HEAD=fca126bc278f5ae4ba5a08f26b3297cb9f12b682` — 일치  
샌드박스: 쓰기가 사본 안에서만 일어났는가 — 예 (`check_lane_binding.py`도 `TMPDIR=$PWD/runs`로 실행)

| # | 변조 | 판정 | 탐지자(규칙 id) | 기준선 출력 | 변조 후 출력 |
|---|---|---|---|---|---|
| M1ⓐ | [CL-2 `dependency_type`](/home/laptop/projects/workspaces/pd-audit-m17/D/tests/fixtures/reader/base/material-spec.json:101) → `unclassified` | DETECTED | [dependency_parse.py](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/lib/dependency_parse.py:128) `parse.unclassified-not-an-escape` | 직접 실행: `status=pass, checked=6, violations=0` | 직접 실행: `status=fail`, locus `CL-2.dependency_type`, 규칙 정확히 적중. 전체 하네스에서는 `read.convergence/dependent-set`도 함께 실패하여 “선언 검사만 실패”는 아님 |
| M1ⓑ | [Markush patterns](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/reader-rules.yaml:293)에 `at least one of` 추가 | DETECTED | 행동 변화 `parse.unclassified-not-an-escape`; 정책 가드 [test_m17_rules.py](/home/laptop/projects/workspaces/pd-audit-m17/D/tests/test_m17_rules.py:331) | 합성 청구항: `status=fail`, 규칙 적중 | `markers=["Markush"], status=pass`; 전용 테스트는 `Markush 어형이 2형태가 아니다`로 실패. 단, `check_validator_enforcement.py` 자체는 여전히 PASS |
| M2 | 시간 용법 `when`만 둔 `unclassified`; 역대조 `in response to` | DETECTED | `parse.unclassified-not-an-escape`; 근거 시험 [test_m17_rules.py](/home/laptop/projects/workspaces/pd-audit-m17/D/tests/test_m17_rules.py:228) | 원본 직접 실행 `status=pass` | `when`: `markers=[]`, `status=fail`, 규칙 1건. `in response to`: `markers=["조건부"]`, `status=pass`, 위반 0건 |
| M3ⓐ | quoted fact M17 삭제 | DETECTED | [derivation.py](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/lib/derivation.py:570) `value.harvest-parity` | `run_read_checks`: READ 10행 전부 pass | 실패 검사는 `read.value-derivation` 하나. `[누락]`, locus `harvest:[0047][41,57)`, expected `320, 340, 360 °C` |
| M3ⓑ | M13 `value_raw` `0.08`→`0.09` | DETECTED | `value.harvest-parity` `[변조]` | READ 10행 전부 pass | 실패 검사는 `read.value-derivation` 하나. `[변조]`를 구별함. 같은 행에서 `value.quoted-span`, `value.type-agrees`도 함께 적중 |
| M3ⓒ | 새 quoted fact M44 추가 | DETECTED | `value.harvest-parity` `[추가]` | READ 10행 전부 pass | 실패 검사는 `read.value-derivation` 하나. locus `M44.value_raw`, expected `(수확 결과에 없음)`, 메시지 `[추가]` |
| M4ⓐ | [response.json 입력 지문](/home/laptop/projects/workspaces/pd-audit-m17/D/runs/openai-us20260147854a1-cim-fp-3/10-read/lanes/read-b/decompose/retry-1/batch-0/response.json:5)을 다른 요청 지문으로 교체 | DETECTED | [load_response](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/lanes/contract.py:291) `LaneStaleResponseError`; [_dispatch](/home/laptop/projects/workspaces/pd-audit-m17/D/engine/stages/read.py:179) 거부 행 | 도구: `RESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 3종 전건 일치` | 독립 주입: `LaneStaleResponseError`; journal은 `rejected=true`, `digest_ok=false`, expected `8bcb…`, echoed `ec2b…` |
| M4ⓑ | 소비 뒤 같은 응답 payload 덮어쓰기 | **미확인 (NOT ASSESSED)** | 미확인 | 소비 시 digest `4b1e4971…` 확보 | `screening_memo.reason`에 `(사후 교체본)`을 심은 직후 중단됨. 현재 SHA-256 대조 출력은 확보하지 못함 |
| M5 | [lane-log.json](/home/laptop/projects/workspaces/pd-audit-m17/D/runs/openai-us20260147854a1-cim-fp-3/10-read/lanes/lane-log.json:1) `lane_id` 바꿔치기 | **미확인 (NOT ASSESSED)** | 미확인 | 미확인 | 실행하지 않음 |
| M6ⓐ | 비승인 `patent.marketing_verdict` 코어 삽입 | **미확인 (NOT ASSESSED)** | [check_spec_refs.py](/home/laptop/projects/workspaces/pd-audit-m17/D/tools/check_spec_refs.py:1) K8 예정 | 미확인 | 실행하지 않음 |
| M6ⓑ | 코어 삽입과 [core-surface.yaml](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/core-surface.yaml:1) 승인 동시 변경 | **미확인 (NOT ASSESSED)** | 미확인 | 미확인 | 실행하지 않음 |
| M7ⓐ | 우선권 관할 코드 근접 위조 | **미확인 (NOT ASSESSED)** | [bibliography.py](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/lib/bibliography.py:1) 예정 | 미확인 | 실행하지 않음 |
| M7ⓑ | 날짜·최우선일 정합 위조 | **미확인 (NOT ASSESSED)** | `bib.priority-year-in-source` 예정 | 미확인 | 실행하지 않음 |
| M7ⓒ | 관할 코드 32/33자 경계 | **미확인 (NOT ASSESSED)** | `bib.priority-jurisdiction-in-source` 예정 | 미확인 | 실행하지 않음 |
| M8ⓐ | 기존 ID payload 변경 | **미확인 (NOT ASSESSED)** | [freeze_integrity.py](/home/laptop/projects/workspaces/pd-audit-m17/D/reader/lib/freeze_integrity.py:1) 예정 | 미확인 | 실행하지 않음 |
| M8ⓑ | `retracted → active` | **미확인 (NOT ASSESSED)** | `freeze.payload-immutable` 예정 | 미확인 | 실행하지 않음 |
| M8ⓒ | A→B→A 승계 순환 | **미확인 (NOT ASSESSED)** | `freeze.payload-immutable` 예정 | 미확인 | 실행하지 않음 |

NOT DETECTED 항목의 해석:

- 확인 완료 범위에는 확정적인 `NOT DETECTED`가 없습니다.
- M1ⓑ에서는 전체 변조 코퍼스 도구가 규칙 확대를 놓쳤지만 전용 재정 테스트가 잡았습니다.
- “아마 탐지되지 않을” 것으로 명시된 M5는 실행하지 않았으므로 결론을 추정하지 않습니다.

사본 최종 상태(`git status`):

- 최종 명령은 중단 지시에 따라 실행하지 않았습니다.
- 마지막 확인 시점(M4ⓐ 원복 뒤)은 clean이었습니다.
- 그 뒤 M4ⓑ 변조가 [response.json](/home/laptop/projects/workspaces/pd-audit-m17/D/runs/openai-us20260147854a1-cim-fp-3/10-read/lanes/read-b/decompose/retry-1/batch-0/response.json:1)에 적용됐고, 즉시 중단 지시를 받아 **원복하지 않았습니다**. 따라서 이 파일의 미복구 변경은 남아 있는 것으로 판단됩니다.
- `git checkout -- <path>`는 매번 `fatal: Unable to create '…/.git/index.lock': Read-only file system`으로 실패했습니다. M1–M4ⓐ는 `apply_patch` 역변조 후 `git diff --exit-code` 또는 clean status로 원복을 확인했습니다.

OUT-OF-SCOPE:

- 동일 지문 아래 인라인 절차 변경 가능성: 위 NEW BLOCKER. 관찰상 `_dispatch`가 기존 `request.md`를 다시 썼지만 [request.json](/home/laptop/projects/workspaces/pd-audit-m17/D/runs/openai-us20260147854a1-cim-fp-3/10-read/lanes/read-b/decompose/retry-1/batch-0/request.json:1)의 지문은 유지됐습니다.
- `.git` 읽기 전용으로 지정 원복 명령이 작동하지 않은 것은 실행환경 제약이며 제품 결함 판정에는 포함하지 않았습니다.

NEW BLOCKER: **NB-01 — `input_digest`가 실제 인라인 절차 바이트를 결속하지 않아 동일 지문이 서로 다른 실제 요청서를 가리킬 수 있음.**