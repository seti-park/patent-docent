# D-20260913-03 — READ 부분 런 2 구동 설계 (총괄 저작 · 재정 T58 ②④ · T59 · T60 집행)

**지위.** 총괄 문서(원장 아님). 재정 T60(구동 = `좌석 M1a` 직접 · 전 레인 CLI 직접 호출 · 결정론 파이썬 구동기)의 설계 공백을 닫는다. 구동기 코드는 이 문서를 정본으로 `좌석 M3` 가 저작한다.

## §1 이름 정정 — 「예행 런 2」가 아니라 **READ 부분 런 2**

재정 P-9 · `contracts/run-kinds.yaml` 은 예행 런(`rehearsal`)을 「strip 산출까지 완전 리허설 · 게시만 제외」로 정의한다. design·figures·compose·gate 가 아직 없으므로 이번 런은 예행 런이 아니다. 재정 T40 ③ 이 만든 **`run_kind: partial`**(비게시 · 발주가 정한 스테이지에서 멈춤 · `partial_until` 필수 · 앵커 원장 편입 없음)이 정확히 이 런의 종류다. **이번 런 = `partial` · `partial_until: freeze`**(CP1 봉투를 freeze 가 소비해 `review_adjudicated[]` 전건 덮기 검사까지 실제로 돈다). 재정 T58 ④·T60 의 「예행 런 2」는 통칭이며 뜻은 같다. 09-01 런이 `rehearsal` 로 적힌 것은 행위시법으로 그대로 둔다.

**런 ID** = `gdm-wo2026128750a1-agent-memory-2`(SPEC §7.1 · 같은 특허·같은 각도의 둘째 런 = `-2` 접미). **소재** = 09-01 스테이징 그대로(`~/projects/workspaces/docent-rehearsal-01-source/input-raw/WO2026-128750A1.txt` sha256 `0c207938…c2228` · 도면 20). **법** = 기동 시점 `main` HEAD(T58 좌석 · T59 판정지 포함) → `.worktrees/<run_id>` detached · `run.yaml#engine.commit` 결박(P-U1).

## §2 무엇이 새로운가 — 09-01 런과의 차이 셋

| | 09-01 런 | 이번 런 |
|---|---|---|
| 레인 좌석 | opus-5 max/high/low/max | **fable-5.1 low(분해·통합) · opus-5 low(접지 둘)** — T58 ② |
| 레인 호출 | 대화창이 Workflow `agent()` 로 | **구동기가 `claude -p` CLI 를 서브프로세스로** — T60 · fable 은 이 경로만 effort 보존 |
| CP1 판독본 | 기계 목록 §7·§8·§10~§12 | + **§8-b Owner 판독 요청**(레인 자기 신고) · 봉투 `review_adjudicated[]` — T59 |

## §3 구동기 — `tools/drive_partial_read.py`(결정론 파이썬 · 정본 리포 안 · 측정 도구 아님)

**쓰는 곳** = worktree 안 `runs/<run_id>/**`(엔진 산출 · 엔진이 쓴다) · `<worktree>/evidence/**`(구동기 영수증) · 섀도 원장은 엔진 기본(주 작업 트리 `ledgers/shadow/screening.jsonl` · P-U4 — 09-01 과 같은 명시 운영 선택). **읽는 곳** = 계약·엔진·절차 문서(worktree 의 법). 정본 리포 `main` 트리에는 원장 행 외 쓰지 않는다.

**명령**(각각 결정론 · 재진입 안전 · 실패 = 비영 종료코드 + 사유 한 줄 · 자동 재시도 없음)

| 명령 | 하는 일 |
|---|---|
| `init <run_id>` | `git worktree add --detach .worktrees/<run_id> main` · `source` 스테이지(`engine/stages/source.py#run` · `run_kind=partial` · `partial_until=freeze` · 소재 지문 대조 — 어긋나면 정지) |
| `step <run_id>` | `read` 스테이지 1회 진입(`engine/stages/read.py#run` · `FileLaneAdapter`) → `LanePending` 이면 대기 좌표 전건을 **순차로** 레인 호출(§4) → 응답 파일 → 다시 진입. 반복 상한 12. 종료 = 조기 수렴 상신(exit 11) · 봉투 불가 대기(12) · CP1 대기(20) · 종결 실패(13) · 판정 불능(14) — T40 구동기의 종료 코드 어휘를 그대로 쓴다 |
| `lanes <run_id>` | 무변경 조회 — 대기·완료 좌표 · 영수증 요약 |
| `continue <run_id> --quote-file <f>` | 조기 수렴 **상신 축 미달**에만(T17) Owner 육성 인용으로 `convergence_continue` 봉투(판정서 sha256 결속) — 그 밖의 미달은 봉투 불가 |
| `cp1 <run_id>` | CP1 판독본 경로 · `review_requests` 건수 · §8-b 첫 줄들 · 봉투 서식(`review_adjudicated[]` 채울 target 목록)을 출력 — Owner 에게 낼 것 |
| `approve <run_id> --quote-file <f> --adjudicated <json>` | Owner 육성 원문 + 항목별 판정으로 `15-frozen/approval-v<N>.md` 작성(`recorded_by: orchestrator` · target 해시 결속 · `decision` 이진) |
| `freeze <run_id>` | `freeze` 스테이지 1회(`approval-valid` 항 ④ 포함) · `partial_until` 도달 = 종결 |
| `seal <run_id>` | `evidence/MANIFEST-sha256.txt`(영수증·응답·판정서 지문) |

## §4 레인 호출 규격 — 한 좌표 = `claude -p` 한 번

```
env MEMORY_HOOKS=off CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 \
claude -p --setting-sources project --disable-slash-commands --strict-mcp-config --model <api-id> --effort <effort> \
  --output-format json --json-schema <봉투 스키마 JSON 문자열> \
  --permission-mode dontAsk --permission-prompts none --tools "" \
  < <lane_dir>/request.md > <evidence>/calls/<lane_id>.raw.json
```

- **~~`--bare`~~ → `--setting-sources project` + 중립 cwd + `--disable-slash-commands --strict-mcp-config`** [정정 2026-09-13 13:5x · 실측] — `--bare` 는 키체인 읽기도 건너뛰어 구독 로그인이 풀린다(`Not logged in` · LANE-RUNTIME 함정 S). 대체 조합의 실측(stream-json `system/init`) = 훅 0 · 플러그인 0 · MCP 0 · 스킬 0 · 도구 0 · 자동 메모리 = 중립 cwd 의 빈 디렉터리. 레인은 요청서 하나만 본다(요청서 밖 파일 접근 금지 · 도구 0). 구조화 출력 자리 = json 결과의 `structured_output`(실측).
- **모델 ID** = 계약 라벨의 첫 alias(`read.yaml#lane.model_identity.labels`: `fable-5.1 → claude-fable-5-1` · `opus-5 → claude-opus-5`). effort = `sub_lanes[].effort`. 둘 다 **플래그로만** 지정(프롬프트 문구 금지 · SPEC §1.4 레인 규약 1).
- **`--json-schema`** = 응답 봉투 `{lane_id, model, effort, input_digest, payload}` 에 `engine/lanes/plan.py` 의 해당 작업 payload 스키마를 넣은 것(구동기가 좌표마다 생성). CLI 층에서 형태를 강제하고 엔진 검증은 그대로 둔다(이중).
- **응답 파일 작성 = 구동기**(레인이 파일을 쓰지 않는다 · 도구 0). `payload` 와 `input_digest` 는 레인 출력 그대로 옮기고 **`lane_id` 는 구동기가 아는 좌표를 쓴다**(레인 반향은 영수증에만 — 2026-09-13 step 3 실측: 레인이 「read-a」만 적어 엔진이 거부·런 종결 · 정정) · 입력 지문 반향이 요청과 다르면 응답을 쓰지 않는다(지문은 레인이 요청서 표에서 옮겨 적은 값 — P-12 시점 결속 유지). **`model` 은 CLI 출력 `modelUsage` 의 주 키(출력 토큰 최대)**로 쓴다 — 레인의 자기 신고보다 등급이 높은 관측(공식 문서: json 결과의 per-model 비용 분해 · `system/init.model`). 요청 ID 와 다르면 그 값을 그대로 적어 러너가 `mismatch` 로 남기게 한다(조용한 대체 금지). **`effort` 는 요청 플래그 값**(출력에 노출되지 않음 — 문서·실측 일치 · `read.yaml#lane.effort_evidence` 대로 구동기가 권위 원천).
- **영수증** `evidence/calls/<lane_id>.json` = 요청 파일 지문 · 응답 파일 지문 · 요청 {model, effort} · 관측 `modelUsage` 전건 · `is_error` · `num_turns` · `total_cost_usd` · `duration_ms` · `session_id` · stderr 꼬리 · 벽시계. 원시 출력 `.raw.json` 보존.
- **한도** — 서브프로세스 벽시계 상한 900초 · stdin 10 MB 상한 확인(문서) · 팬아웃은 엔진이 정하되 구동기는 **순차 실행**(RAM 2.9 GB · 함정 J) · 좌표당 호출 상한 3(엔진 재시도 예산과 별개 · 초과 = 15 · 사람이 본다).
- **실패 처분** — `is_error` 또는 시간 초과 = 응답 파일을 쓰지 않고 영수증만 남김 → 다음 `step` 이 같은 좌표를 다시 대기로 낸다(상한 안) · 스키마 불합격(CLI 가 거부하거나 엔진이 거부) = 러너 `rejected` 행 · IO 결함(`io_fault`) = 정지 · 사람 확인(T43 규약).
- **첫 배치 실호출 검증**(SPEC §1.4 레인 규약 3) = 첫 좌표의 영수증에서 `modelUsage` 주 키 == 요청 ID 를 확인한 뒤 계속 · 불일치면 정지·상신.

## §5 순서(엔진이 이끈다 · 구동기는 따른다)

`init` → `step`(분해 read-a·read-b 2 좌표 · fable low) → 엔진 조기 수렴 판정 → [상신 축 미달이면 Owner 「계속」 → `continue`] → `step`(접지 ≤ 9 좌표 · opus low · 엔진이 낸 만큼) → `step`(통합 1 · fable low) → **CP1 대기(exit 20)** → `cp1` 출력을 Owner 께(판독본 `10-read/material-spec.md` 전문 + §8-b) → Owner 육성(승인/반려 · `review_adjudicated[]` 전건 · 「판정 불가」 허용) → `approve` → `freeze` → `seal` → 결과 기록(결정문 추기 · HANDOFF). **반려면** 지시문을 담은 봉투 뒤 재분해는 새 시도(엔진 재시도 어휘)로 — 구동기가 판단하지 않는다.

## §6 쓰지 않는 것 · 바뀌지 않는 것

검수원(`t40_metrics` 등 9모듈 · 좌석 비교용 · 「가설」 출하 상태) · Workflow `agent()` 경로 · 지표·임계표 · 계측 브랜치 핀 셋. 바뀌지 않는 것 = 엔진·계약·절차 문서(이번 런의 법은 `main` HEAD 그대로) · 09-01 런 산출 · CP1 질문 문구 · 봉투 이진 결정.

## §7 비용·시간 추정(실측은 영수증이 정본)

분해 2(fable low · 요청서 ≈ 1.3 MB ≈ 330k 입력) + 접지 ≤ 9(opus low) + 통합 1(fable low) ≈ 입력 4M 토큰 안 · 벽시계 1~2시간(레인당 10~25분 [미확인]) · Owner CP1 판독 시간 별도.

## §8 Owner 몫

⑴ 조기 수렴 상신 축 미달 시 「계속」 한 줄(있을 때만) ⑵ CP1 판독본 읽기 · 승인/반려 육성 ⑶ §8-b 요청 전건에 `confirmed / defect / undecided` 답(요청 0 건이면 없음). 총괄이 판독본을 아티팩트로도 띄운다(감시 없음).

## §9 구동기 저작(M3) 성공 판정

⑴ 위 명령 8 이 있고 각각 결정론·재진입 안전 ⑵ 레인 호출이 §4 규격의 플래그 전건으로 조립되고(시험이 인자 목록을 고정) 응답 파일의 `model` 이 `modelUsage` 주 키에서 오며 `effort` 가 요청값 ⑶ 스텁 실행기(실제 CLI 를 부르지 않는 가짜 `claude`)로 09-01 런의 요청서 픽스처에 대해 왕복이 성립하고 러너가 응답을 소비 ⑷ 영수증·MANIFEST 서식 ⑸ 실패 처분(is_error · 시간 초과 · 상한 초과 · IO 결함) 각각 시험 ⑹ 봉투 작성이 스키마와 `approval-valid` 항 ④ 를 통과하는 픽스처와 실패하는 픽스처(빠짐 · 유령 · defect+approved) ⑺ 실제 모델 호출 0(시험) · 관문 14 · 전체 시험 통과.
