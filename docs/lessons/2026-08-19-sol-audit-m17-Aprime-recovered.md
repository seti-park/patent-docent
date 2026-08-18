# sol 독립 감수 원문(회수분) — M1.7 분할 감수 A′ · 1차 사망 세션 (2026-08-19 00:0x)

**STATUS: partial(events) — 원세션이 최종 VERDICT 표를 발화한 뒤 사망, resume 불필요**

**보존 근거.** 재정 2026-08-18 **N7 ①** — 외부 감수 산출물은 **원문 그대로** `docs/lessons/` 에 보존한다. 이 파일은 **하네스 결함으로 사망한 1차 감수 세션에서 사후 회수한 원문**이다.

| 항목 | 값 |
|---|---|
| 의뢰 | A′ (격리 사본 `pd-audit-m17/A`) |
| 감수자 | GPT-5.6-sol, reasoning effort max |
| 원세션 ID | `01a0156b-3865-7841-8d50-88e8963cc6e1` |
| rollout | `~/.codex/sessions/2026/08/19/` |
| 실행시간 | 약 4분 45초 (285s) |
| 샌드박스 | `read-only` |
| **사망 사유** | `timeout` CAP **600초** 직격 (구 `sol-auditor.md` 기본값). `--output-last-message` 는 턴 정상 완료 시에만 기록되므로 `$FINAL` 은 **0바이트**였다. |
| 회수 경로 | **rollout 이벤트 발굴** — 원세션 rollout 에서 최종 VERDICT 표를 그대로 추출(사망 직전 발화 완료). resume 미사용. |
| 판정 발행 주체 | **원세션 Sol 자신** — 아래 본문은 원세션 발화 그대로다(resume 재추론 아님) |

**★ 격의 명시.** 이 판정은 **완주 판정이 아니다.** 조사가 중단된 상태에서 확보된 것이므로 미확인 항목이 남아 있을 수 있다. 완주분(동일 의뢰 재실행, CAP 2400)은 `2026-08-19-sol-audit-m17-full.md` 를 참조하라 — 두 판정이 어긋나면 **완주분이 우선**한다.

---

## Sol 발화 원문 (시간순, 구분선으로 분리)

지정된 격리 사본에서 먼저 HEAD 지문만 확인하겠습니다. 일치할 때에만 나머지 6개 항목을 계속 실행합니다.

---

A1은 기대값 `fca126bc278f5ae4ba5a08f26b3297cb9f12b682`와 정확히 일치했습니다. 이제 plain 관문 4종을 각각 실행하고 exit code와 원문 출력을 수집합니다.

---

plain 관문은 3종 exit 0, `check_lane_binding.py`만 임시 디렉터리 부재로 exit 1이었습니다. 기대값과 다르므로 그대로 기록하며, 동일한 4종을 `python3 -O`로 확인합니다.

---

`-O` 결과는 plain과 관문별로 동일했습니다: `0, 0, 0, 1`. A4용 §① 원문 12줄도 확보했습니다. 다음은 지정된 전주기 pytest를 1회 실행하며, 수집 단계의 환경 오류일 때만 안내된 `TMPDIR=/dev/shm` 재실행을 적용합니다.

---

pytest가 테스트 수집 전에 `No usable temporary directory`로 종료했습니다. 실행 조건에 따라 정확히 `TMPDIR=/dev/shm`을 붙여 재실행합니다.

---

재실행은 정상적으로 테스트를 진행 중이며 현재 약 34% 이상 완료되었습니다. 종료 요약이 나올 때까지 같은 세션을 이어서 확인합니다.

---

pytest 재실행은 exit 0으로 끝났고 요약은 `412 passed, 1 warning in 83.53s`입니다. 마지막으로 통주 3의 6개 파일 실재와 두 JSON의 구조를 Python 한 줄 명령으로 기계 집계한 뒤, 12행·7회·커밋을 대조합니다.

---

6개 산출물은 `present_count: 6`, `missing: []`로 전부 실재합니다. 구조 탐색 명령은 `convergence.json`이 객체가 아니라 배열이라 exit 1이었으므로, 배열/객체 양쪽을 처리하는 한 줄 명령으로 구조만 다시 확인합니다. 이 탐색 실패는 A6 판정에는 영향이 없습니다.

---

구조는 `checks` 12행(판정 키 `status`), `lane-log` 7행(키 `digest_ok`)이며 `run.yaml`에는 `engine.commit` 줄이 확인됐습니다. 이제 세 조건을 한 명령에서 수치·불일치 목록까지 집계합니다.

---

VERDICT: FAIL

| # | 확인 | 판정 | 앵커(실출력) |
|---|---|---|---|
| A1 | 핀 지문 대조 | PASS | `fca126bc278f5ae4ba5a08f26b3297cb9f12b682` |
| A2 | 관문 4종 exit 0 (plain) | FAIL | `check_spec_refs=0`, `check_schema_enforcement=0`, `check_validator_enforcement=0`, `check_lane_binding=1`. 실패 출력: `FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m17/A']` |
| A3 | 관문 4종 exit 동일 (`-O`) | PASS | plain=`[0, 0, 0, 1]`, `-O`=`[0, 0, 0, 1]` |
| A4 | 기준선 청정 | PASS | 아래 §① 실출력: 검사 12종 전건 `viol=0` |
| A5 | 전주기 pytest 1회 | PASS | 최초 실행은 임시 디렉터리 오류로 exit 1. 지정된 fallback 결과: `412 passed, 1 warning in 83.53s (0:01:23)` — passed=412, failed=0, exit 0 |
| A6 | 통주 3 산출물 실재 | PASS | `{"expected_count": 6, "files": {"10-read/convergence.json": true, "10-read/lanes/lane-log.json": true, "10-read/material-spec.json": true, "10-read/material-spec.md": true, "TONGJU-REPORT.md": true, "run.yaml": true}, "missing": [], "present_count": 6}` |
| A7 | 통주 3 수치 대조 | PASS | `{"convergence": {"all_12_pass": true, "non_pass_ids": [], "pass_rows": 12, "rows": 12}, "engine": {"commit": "f0b4ca15b2129a1fe191f53d2e834de7b55c3039", "starts_with_f0b4ca1": true}, "lane_log": {"all_7_digest_ok_true": true, "digest_not_true_ids": [], "digest_ok_true": 7, "roundtrips": 7}}` |

A4 §① 실출력:

```text
== ① 기준선 — 무변조 코퍼스가 검사 12종을 통과하는가 ==
  [ok ] read.schema                checked=1    viol=0   vacuous=none
  [ok ] read.source-digest         checked=1    viol=0   vacuous=none
  [ok ] read.verbatim              checked=83   viol=0   vacuous=none
  [ok ] read.pointer-resolve       checked=123  viol=0   vacuous=none
  [ok ] read.coverage              checked=24   viol=0   vacuous=none
  [ok ] read.dependency-parse      checked=6    viol=0   vacuous=none
  [ok ] read.value-derivation      checked=24   viol=0   vacuous=none
  [ok ] read.bibliography          checked=12   viol=0   vacuous=none
  [ok ] read.claim-inventory       checked=9    viol=0   vacuous=none
  [ok ] read.convergence           checked=6    viol=0   vacuous=none
  [ok ] freeze.id-monotonic        checked=89   viol=0   vacuous=none
  [ok ] freeze.payload-immutable   checked=46   viol=0   vacuous=none
```

OUT-OF-SCOPE:

- pytest 종료 시 읽기 전용 파일시스템 때문에 `.pytest_cache` 생성 경고 1건: `PytestCacheWarning: could not create cache path ... [Errno 30] Read-only file system`

NEW BLOCKER: 없음