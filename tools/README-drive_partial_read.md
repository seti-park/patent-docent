# `tools/drive_partial_read.py` — READ 부분 런 구동기 (재정 T60 · 설계 D-20260913-03) + 연장·설계·펜 (재정 T64)

`run_kind: partial` · `partial_until: freeze` 런을 명령 단위로 굴린다. 엔진이 이끌고 구동기는 대기 좌표를 `claude -p` 한 번씩으로 채운다. 판단하지 않는다. 실제 모델 호출은 `step` · `design` · `compose` 만 한다.

```
PY="PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B"
$PY tools/drive_partial_read.py [--repo R] [--worktree-root D] [--executor claude|stub] [--dry-run] <명령> <run_id> ...
```

| 명령 | 인자 | 하는 일 | 정상 종료 |
|---|---|---|---|
| `init` | `--source <patent.txt> --figures <dir> --patent-meta <yaml\|json> [--ref main] [--expect-sha256 <hex>]` | `git worktree add --detach <root>/<run_id> <ref>` → `source.run(partial · freeze)` | 0 |
| `step` | — | `read.run` 재진입(상한 12) → `LanePending` 좌표를 순차 호출 → 응답 파일 → 재진입 | 10 · 11 · 12 · 20 |
| `lanes` | — | 무변경 조회 — 좌표별 대기/완료 · 영수증 요약 | 0 |
| `continue` | `--quote-file <f> [--located-at] [--decided-at]` | 상신 축 미달(`phase-gate.json#blocked_by == convergence-escalation`)에만 `10-read/convergence-continue.md` | 0 |
| `cp1` | — | 판독본 경로 · `review_requests` 건수 · §8-b 첫 12줄 · `--adjudicated` JSON 초안(verdict 비움) | 0 |
| `approve` | `--quote-file <f> --adjudicated <json> [--decision approved\|rejected] [--manual-ack M1,M2] [--derived-ack ..] [--drop-decision go\|drop] [--directive ..]*` | `15-frozen/approval-v<N>.md`(N = 기존 최대 + 1) · 요청 target 차집합은 경고만 | 0 |
| `freeze` | — | `freeze.run(spec_version = 최신 봉투 N)` — `approval-valid` 항 ④ 포함 | 0 |
| `seal` | — | `evidence/MANIFEST-sha256.txt` = `evidence/**` + `10-read/*.json` + `15-frozen/*` + `20-design/**` + `40-compose/**` + `50-gate/**` | 0 |
| `extend` | `--quote-file <f> --until <stage> [--ruling <id>]* [--located-at] [--decided-at]` | 부분 런 종료선 연장 봉투 `15-frozen/extension-v<N>.md`(`extension-envelope/v0` · 재정 T64 ①) → `run.yaml#partial_until` 이동 + `extensions[]` 행. 전제 = `status: active` · `run_kind: partial` · `--until` 이 `terminates_at_enum` 안이고 현 종료선보다 뒤 · 법 트리(`--repo`)가 git 작업 트리이고 `runs/`·`evidence/`·`.worktrees/` 밖 변경 없음 | 0 · 위반 2 |
| `design` | — | `design.run` 재진입(상한 4) → `LanePending` 좌표(`20-design/lanes/design/blueprint[/retry-1]/batch-0`)를 `call_lane` 으로 채움 → 재진입. 전제 = `partial_until` 순번 ≥ `design`(아니면 13 「종료선」) | 0 · 10(호출 실패) · 13(escalate/halt/StageError) · 14 · 15(재진입 상한) |
| `compose` | — | `compose.run` 재진입(상한 8) → `LanePending` 좌표(`40-compose/lanes/compose/<v1\|v2\|v3>[/retry-<n>]/batch-0`)를 **순차** `call_lane` 으로 채움(한 번에 하나 · `--model claude-opus-5 --effort high\|xhigh\|max`) → 재진입. 좌표가 호출 상한 3 에 닿으면(15) 그 변주를 **결측**으로 러너에 신고하고 계속한다(생존 ≥ 1 → 0 · 토너먼트 결측 행). 전제 = `partial_until` 순번 ≥ `compose` · `20-design/blueprint.json` 실재(아니면 13 「design 먼저」) | 0(생존 ≥ 1) · 10(호출 실패) · 13(escalate/halt/reject-upstream · 사유 + 반려서 경로) · 14 · 15(재진입 상한) |
| `gate-l0` | `[--variant v]*` | `gate.run`(L0 결정론 · 재정 T64 ②) — 변주별 `50-gate/<v>/{l0.json, verdict.json, thread.stripped.md, thread.json, annotation-index.json}` · 변주별 한 줄 인쇄(`v1: l0 pass · defects 0 · advance`) · 같은 `thread_digest` 면 재계산 없음. 전제 = `partial_until` 순번 ≥ `gate` · 주석본 ≥ 1. 모델 호출 없음 | 0(기록 완료 · 결함 유무 무관) · 13(halt·StageError) · 14 |
| `strip` | `[--variant v]*` | 파싱 오류 0 인 변주에 strip 산출 3종(`50-gate/<v>/{thread.stripped.md, thread.json, annotation-index.json}`)만 · verdict 없이 · 열람 준비용(SPEC §3.3). 모델 호출 없음 | 0 · 13(종료선·주석본 없음·StageError) |

**종료 코드** — 0 정상 · 10 대기 좌표 남음(다시 `step`/`design`) · 11 상신 축 미달(`continue` 가능) · 12 봉투 불가 대기(사람) · 13 종결 실패(엔진 halt/escalate) · 14 판정 불능(io_fault · `modelUsage` 부재 · 첫 좌표 관측 모델 ≠ 요청) · 15 좌표 호출 상한 3 초과 · 20 CP1 대기 · 2 인자·환경 오류(stdin 10 MB 초과 포함).

**레인 호출 한 줄**(좌표마다 · 순차 · 벽시계 900초):
```
env MEMORY_HOOKS=off CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 claude -p --setting-sources project --disable-slash-commands --strict-mcp-config --model <aliases[0]> --effort <effort> \
  --output-format json --json-schema <evidence>/schemas/<lane>.json --permission-mode dontAsk --permission-prompts none --tools "" < request.md
```
응답 파일 `response.json` = `{lane_id, model, effort, input_digest, payload}` · `model` = CLI `modelUsage` 의 출력 토큰 최대 키 · `effort` = 요청 플래그 값 · 나머지 = 레인 출력 그대로. 레인 자기 신고는 영수증에만 남는다.

**영수증** `<worktree>/evidence/calls/<read-a__task__batch-0>.json` + `.raw.json`(원시 CLI 출력) · 이전 회차는 `.attempt-<k>` 로 보존:
```
{lane_id, request_md_sha256, response_json_sha256|null, requested:{model,effort,api_id},
 observed:{modelUsage, main_model}, lane_self_report:{model,effort}, is_error, num_turns,
 total_cost_usd, duration_ms, session_id, stderr_tail, started_at, ended_at, attempt, returncode, timed_out, note}
```

**실패 처분** — `is_error`·시간 초과 = 응답 미작성 · 영수증만 · `step` 은 10 으로 끝나고 다음 `step` 이 같은 좌표를 다시 부른다(회차 4 = 15). 응답 파일이 있는 좌표는 다시 부르지 않는다.

**자리** — worktree `<repo>/.worktrees/<run_id>` · 런 `<worktree>/runs/<run_id>` · 영수증 `<worktree>/evidence` · 법 = worktree. `--run-root`/`--evidence-dir` 는 자리를 직접 지정한다(그때 법 = `--repo`). `--dry-run` 은 명령줄만 인쇄하고 아무것도 쓰지 않는다. `--executor stub` 은 `<evidence>/stub-responses/<lane>.json` 을 되돌리는 시험용이다.
