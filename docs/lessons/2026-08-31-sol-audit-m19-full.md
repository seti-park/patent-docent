# PD-M1.9 분할 감수 4의뢰 — 원문 보존 (핀 `df1373e`)

```
date: 2026-08-31
pin: df1373e0a4f196ad650a02dfb9cfa61f79db7e5c
order: PD-M19-P11
lanes: A′(read-only) · C′-1(read-only) · C′-2(read-only) · D(workspace-write)
model: gpt-5.6-sol · model_reasoning_effort=xhigh
격: 전건 complete (1차 완주 · resume 미사용)
```

**이 파일의 지위 — 재정 N7.** 외부 감수 산출은 **원문 그대로** 보존한다. 아래 네 절은 Sol 이
낸 **최종 판정문 전문**이며 총괄이 한 글자도 고치지 않았다. 처분표·요약은 이 원문을 가리키는
포인터일 뿐이다(`docs/decisions/D-20260831-01-m19-close.md`). 압축 보존은 M0 에서 지적 2건의
문언을 영구히 잃게 만들었다.

**★ 보존 경로를 구별해 적는다.** A′·C′-2·D 는 래퍼가 남긴 `--output-last-message` 파일에서
직접 회수했다. **C′-1 은 그 파일이 `/tmp` 에서 사라져 rollout jsonl 에서 발굴했다**
(`~/.codex/sessions/2026/08/31/rollout-2026-08-31T17-56-38-…jsonl`). **격은 그대로
`complete` 다** — 재정 S8 부칙의 `partial(events)` 는 *판정이 중도에 끊긴* 경우를 가리키는데,
C′-1 은 정상 완주해 최종 판정문을 발행했고(래퍼가 `EXIT=0` 확인 후 회수해 보고했다) 사라진
것은 **총괄의 보관 사본**뿐이다. 발굴로 되찾은 것도 그 완주분의 전문이다.

**★ C′-1 의 보관 사고는 발주 미준수에서 왔다.** 발주문은 레인별 고유 스크래치 접두
(`m19-c1`)를 지정했는데 C′-1 레인은 래퍼 기본 접두(`sol-*`)를 썼다. 같은 시각 **다른 세션의
sol 레인**도 같은 기본 접두를 쓰고 있었고, `/tmp/sol-final.*` 자리에 남은 것은 그 타 세션의
산출이었다. 직전 라운드(`D-20260819-03` §8 ④)가 겪은 **덮어쓰기 사고와 같은 계열**이며, 그
처분으로 도입한 고유 접두 규정이 **한 레인에서 지켜지지 않았다.** 회수는 성공했으나 이번에도
운이 절반이었다(rollout 이 살아 있었다). 다음 발주는 접두 준수를 레인 보고의 필수 항목으로
올려야 한다.

---

## 의뢰 A′ — 기계적 확인 (read-only · setsid · EXIT=0)

**격 = `complete`** · 보존 경로 = $FINAL 직접 회수 · 원문 16,476 B

### FINAL (원문 그대로)

# 1. VERDICT: FAIL

exclusions 동결·이연 사유와 무관하게 FAIL이다.

- 현재 테스트 464건이 수집되지만 [CLAUDE.md](/home/laptop/projects/workspaces/pd-audit-m19/A1/CLAUDE.md:118)는 `452 passed`로 낡았다.
- 실제 READ 보고 행은 13개인데 [docs/SPEC.md](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:416)는 계속 12개라고 서술한다.
- §8.3 관문표는 lane-binding 도구를 4시나리오로 적지만 실제 도구는 7종을 주장·검증한다. 직전 NEW BLOCKER와 같은 문서↔실물 범위 불일치다.
- 필수 전수 시험과 lane-binding 2회는 읽기 전용 환경의 임시 디렉터리 부재로 완료하지 못했다. 따라서 “plain/-O 464 passed, 관문 8회 exit 0”도 이 환경에서 재현되지 않았다.

## 리포·HEAD·커밋 고정

원문 출력:

```text
$ pwd
/home/laptop/projects/workspaces/pd-audit-m19/A1

$ git rev-parse HEAD
df1373e0a4f196ad650a02dfb9cfa61f79db7e5c

$ git log --oneline 2eb30de..HEAD
df1373e feat(재정 Q1): 레인 로그 지문 값 대조를 새 검사 id로 신설 — read.lane-log-digest-value
74ea28b docs(재정 Q2·Q4·§3): 배제 봉투 PD-M4 동결 선언 + 첫 번호 소수 결함 종결 + 빈도 실측 등재
c76b616 docs(계측 동결): PD-M1.9 착수 전 4항 확정 — 감수 산출을 보기 전에 박는다
84219bc docs(원장): 2026-08-31 재정 Q1~Q4 등재 — 원문 축자 전사 + 색인
95d6eea docs(D-20260819-03 §4~§8): 감수 판정표 · 신규 지적 7건의 처분 · 종결 가부 권고
88f7d77 fix(감수 처분): 배제가 진짜 수치를 먹지 않게 — S7 조건의 이행 충실화 + 문언 정정
20a06a7 docs(감수): M1.8 분할 감수 4의뢰 원문 보존 — 새 실행 체제의 첫 적용
```

HEAD 일치, 커밋 수 7개다. 종료 시 `git status --short` 출력은 비어 있었다.

# 2. 필수 확인 1 — 전수 시험

## Plain

```text
$ ./.venv/bin/pytest tests/ -q
...
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-a1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/A1']
```

실제 종료코드: `1`

요청한 마지막 줄 원문:

```text
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-a1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/A1']
```

## `PYTHONOPTIMIZE=1`

```text
$ PYTHONOPTIMIZE=1 ./.venv/bin/pytest tests/ -q
...
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-a1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/A1']
```

실제 종료코드: `1`

마지막 줄 원문도 동일하다.

테스트 실행과 분리해 쓰기를 차단한 수집만 보조 실측했다.

```text
$ PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS="-s -p no:cacheprovider --collect-only" ./.venv/bin/pytest tests/ -q
464 tests collected in 1.82s
EXIT=0
```

따라서 `464 passed` 자체는 이번 환경에서 입증하지 못했지만, 현재 테스트 노드는 464개이며 `CLAUDE.md:118`의 `452 passed`는 현재 트리 계수와 맞지 않는다. 신설 [tests/test_m19_digest_value.py](/home/laptop/projects/workspaces/pd-audit-m19/A1/tests/test_m19_digest_value.py:114)만 정확히 12개 테스트를 추가한다.

# 3. 필수 확인 2 — 관문 4종 종료코드

| 관문 | plain | `python3 -O` |
|---|---:|---:|
| `check_spec_refs.py` | 0 | 0 |
| `check_schema_enforcement.py` | 0 | 0 |
| `check_validator_enforcement.py` | 0 | 0 |
| `check_lane_binding.py` | 2 | 2 |

총괄 주장인 8회 전부 exit 0은 재현되지 않았다. 6회는 0, lane-binding 2회는 환경 오류 2다.

## `check_spec_refs.py`

Plain 판정 원문:

```text
PASS  K1  절 참조 해소  (해소 669 · 면제 0 · 결함 0)
PASS  K2  계약 파일 현황  (해소 36 · 면제 0 · 결함 0)
PASS  K3  스키마 이름 일치  (해소 14 · 면제 6 · 결함 0)
PASS  K4  조항 참조 범위  (해소 599 · 면제 0 · 결함 0)
PASS  K5  폐지 토큰 부재  (해소 0 · 면제 25 · 결함 0)
PASS  K6  계약 파일 파싱  (해소 17 · 면제 0 · 결함 0)
PASS  K7  스키마 메타 검증  (해소 5 · 면제 0 · 결함 0)
PASS  K8  코어·확장 경계  (해소 8 · 면제 0 · 결함 0)
RESULT: PASS
EXIT=0
```

`python3 -O`도 같은 K1~K8 출력이었다.

```text
RESULT: PASS
EXIT=0
```

§8.3의 K1~K8 서술과 실행물은 이 부분에서는 일치한다.

## `check_schema_enforcement.py`

Plain:

```text
SUMMARY: cases=37 REJECT_OK 23/23 ACCEPT_OK 12/12 VALIDATOR_SCOPE 2/2 schemas=4
        스키마가 강제하는 것만 위에서 증명되었다. validator-scope 2건 = 스키마를 통과하는 무효 인스턴스 (구현됨 1 / 미구현 1):
          - validator-scope/material-spec.self-reference.json → read.pointer-resolve (구현됨 — tests/test_m1_reader.py::test_self_referencing_derivation_input_is_rejected)
          - validator-scope/metrics-row.completion-proxy-999.json → feedback.row-consistency (미구현)
EXIT=0
```

`python3 -O`:

```text
SUMMARY: cases=37 REJECT_OK 23/23 ACCEPT_OK 12/12 VALIDATOR_SCOPE 2/2 schemas=4
        스키마가 강제하는 것만 위에서 증명되었다. validator-scope 2건 = 스키마를 통과하는 무효 인스턴스 (구현됨 1 / 미구현 1):
          - validator-scope/material-spec.self-reference.json → read.pointer-resolve (구현됨 — tests/test_m1_reader.py::test_self_referencing_derivation_input_is_rejected)
          - validator-scope/metrics-row.completion-proxy-999.json → feedback.row-consistency (미구현)
EXIT=0
```

## `check_validator_enforcement.py`

Plain:

```text
RESULT: PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족
        이 도구가 증명한 것은 검증기가 거부하는 것뿐이다. 계약의 옳음도, 스키마의 집행도 증명하지 않는다.
EXIT=0
```

`python3 -O`:

```text
RESULT: PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족
        이 도구가 증명한 것은 검증기가 거부하는 것뿐이다. 계약의 옳음도, 스키마의 집행도 증명하지 않는다.
EXIT=0
```

## `check_lane_binding.py`

Plain:

```text
ENVIRONMENT ERROR: 임시 작업장을 만들 수 없다 — FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-a1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/A1']. 쓸 수 있는 임시 디렉터리를 TMPDIR 로 지정하라(예: TMPDIR=/dev/shm)
레인 왕복 시점 결속 — 변조 실증 (재정 2026-08-19 P-12 · S4)
  리포: /home/laptop/projects/workspaces/pd-audit-m19/A1
EXIT=2
```

`python3 -O`:

```text
ENVIRONMENT ERROR: 임시 작업장을 만들 수 없다 — FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-a1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/A1']. 쓸 수 있는 임시 디렉터리를 TMPDIR 로 지정하라(예: TMPDIR=/dev/shm)
레인 왕복 시점 결속 — 변조 실증 (재정 2026-08-19 P-12 · S4)
  리포: /home/laptop/projects/workspaces/pd-audit-m19/A1
EXIT=2
```

# 4. 필수 확인 3 — 문서 서술 ↔ 실행물

## (a) 전수 시험 계수

불일치다.

- [CLAUDE.md:118](/home/laptop/projects/workspaces/pd-audit-m19/A1/CLAUDE.md:118): `전수 시험 = 452 passed`
- 수집 실측: `464 tests collected`
- 신설 테스트 파일: 정확히 12개

전수 실행은 환경 문제로 완료하지 못했으므로 `464 passed`까지는 확인하지 못했다. 다만 452라는 현재 문서 계수는 현재 테스트 집합과 명백히 어긋난다.

## (b) `checks_before_exit`

직접 계수 원문:

```text
COUNT=12
01 read.schema
02 read.source-digest
03 read.verbatim
04 read.pointer-resolve
05 read.coverage
06 read.dependency-parse
07 read.value-derivation
08 read.bibliography
09 read.claim-inventory
10 read.convergence
11 read.lane-log-shape
12 read.lane-log-digest-value
```

따라서 [contracts/stages/read.yaml:338](/home/laptop/projects/workspaces/pd-audit-m19/A1/contracts/stages/read.yaml:338)의 블록과 [docs/SPEC.md:4550](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:4550)의 “`checks_before_exit`는 12행”은 일치한다.

하지만 `convergence.json`의 전체 판정 행 수는 별개다. 구현 등재부를 합친 실측:

```text
ACTUAL_FULL_ROW_COUNT=13
01 read.input-digest
02 read.schema
03 read.source-digest
04 read.verbatim
05 read.pointer-resolve
06 read.coverage
07 read.dependency-parse
08 read.value-derivation
09 read.bibliography
10 read.claim-inventory
11 read.convergence
12 read.lane-log-shape
13 read.lane-log-digest-value
```

[engine/stages/read.py:1558](/home/laptop/projects/workspaces/pd-audit-m19/A1/engine/stages/read.py:1558)도 `entry_row + READ 10종 + 엔진 2종`을 실제로 조립한다.

## (c) exclusions 계수

실측 원문:

```text
TOTAL=7 ENCLOSING=5 TOKEN_CONDITION=2
1. figure-numeral | token-condition
2. fp-format-triple | enclosing-pattern
3. bit-slice | enclosing-pattern
4. figure-or-table-number | enclosing-pattern
5. subscript-index | enclosing-pattern
6. figure-or-table-number-list | enclosing-pattern
7. row-column-coordinate | token-condition
```

이는 다음과 정확히 일치한다.

- [contracts/glossary.md:178](/home/laptop/projects/workspaces/pd-audit-m19/A1/contracts/glossary.md:178): 봉투 5 + 토큰 조건 2 = 목록 7
- [reader/reader-rules.yaml:1490](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/reader-rules.yaml:1490)의 census
- 로더도 [reader/lib/rules.py:467](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/lib/rules.py:467)에서 봉투를, [reader/lib/rules.py:512](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/lib/rules.py:512)에서 선행 문맥 조건을 별도로 컴파일한다.

## (d) `read.lane-log-digest-value` 범위

실제 구현 범위는 [engine/stages/read.py:1215](/home/laptop/projects/workspaces/pd-audit-m19/A1/engine/stages/read.py:1215)~1294에서 다음으로 한정된다.

- 각 로그 행의 `request_digest`
- `lanes_root/<lane_id>/request.md`
- 값 불일치, 파일 부재, 파일 읽기 실패
- `null`인데 파일이 실재하는 위장
- 칸 부재·빈 문자열은 `deferred_to_shape`
- `lanes_root` 자체가 올바른 루트인지는 검사하지 않음

`input_digest`나 `response_digest`의 파일 값은 이 검사에서 대조하지 않는다.

범위가 정확한 문언:

- [contracts/glossary.md:62](/home/laptop/projects/workspaces/pd-audit-m19/A1/contracts/glossary.md:62)
- [contracts/stages/read.yaml:433](/home/laptop/projects/workspaces/pd-audit-m19/A1/contracts/stages/read.yaml:433)
- [docs/SPEC.md:402](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:402)
- [docs/SPEC.md:432](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:432)
- [docs/SPEC.md:466](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:466)

과장된 문언은 [docs/SPEC.md:1832](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:1832)다.

> “그 지문들이 가리키는 파일과 실제로 같은가”

직전 행이 요청 입력 지문·응답 지문·요청 파일 지문의 “3항”을 열거하므로, 이 복수형은 신설 검사가 세 지문 모두의 파일 값을 대조하는 것으로 읽힌다. 구현은 오직 `request_digest ↔ request.md`만 본다.

# 5. 필수 확인 4 — lane-binding 자기 주장

정적 계수 원문:

```text
NUMBERED_SCENARIOS=①,②,③,④,⑤,⑥,⑦
NUMBERED_COUNT=7
HAS_6B=True
ASSERT_AST_NODES=0
"\nRESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 · "
"지문 위조 거부 · null 위장 거부 · 정당한 면제 보존 7종 전건 일치"
```

실제 구분:

1. ① 정상 소비
2. ② 낡은 응답 거부
3. ③ `response.json` 사후 교체 탐지
4. ④ 절차 문서 변조 후 구 응답 거부
5. ⑤ `request_digest` 위조 거부
6. ⑥ `null` 위장 거부
7. ⑦ 정상 값 대조·비공허 확인

여기에 ⑥-b 정당한 면제 보존이 별도 대조군으로 추가된다. RESULT의 일곱 문구는 모두 코드상 검증 경로가 있다. `assert` AST 노드는 0개다.

다만 도구 docstring에는 자기 검증 범위를 넘어선 문장이 있다. [tools/check_lane_binding.py:42](/home/laptop/projects/workspaces/pd-audit-m19/A1/tools/check_lane_binding.py:42)는 ⑤⑥⑦이 M-C, 즉 소비 후 `request.md` 교체까지 닫아 “셋 다 기계 판정으로 옮겨졌다”고 말한다. 하지만 `probe_digest_value()`는 요청 파일을 교체하지 않는다. 요청 파일에 하는 변경은 ⑥-b에서의 삭제뿐이다([tools/check_lane_binding.py:443](/home/laptop/projects/workspaces/pd-audit-m19/A1/tools/check_lane_binding.py:443)). 실제 요청 파일 교체 반증은 별도 pytest인 [tests/test_m19_digest_value.py:270](/home/laptop/projects/workspaces/pd-audit-m19/A1/tests/test_m19_digest_value.py:270)에만 있다.

# 6. FINDINGS

- **BLOCKER — READ 보고 행 수가 실행물보다 작게 서술됨.** [docs/SPEC.md:416](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:416), [docs/SPEC.md:1824](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:1824), [docs/SPEC.md:1969](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:1969)는 `convergence.json` 판정 행을 12개라고 적지만 실제 조립은 13개다. 특히 1824는 “거기에 넷이 더해진다”고 하면서 바로 아래 표에 다섯 행을 싣는다.

- **BLOCKER — §8.3 관문표에 직전 NEW BLOCKER와 같은 범위 불일치가 남음.** [docs/SPEC.md:4488](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:4488)는 lane-binding을 “네 시나리오”로, [CLAUDE.md:143](/home/laptop/projects/workspaces/pd-audit-m19/A1/CLAUDE.md:143)는 “세 시나리오”로 설명한다. 실제 도구 RESULT는 7종이며 코드도 ①~⑦과 ⑥-b를 수행한다. 바로 다음 [docs/SPEC.md:4490](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:4490)의 “좁게도 넓게도 적지 않는다”는 자기 선언과도 충돌한다.

- **MAJOR — 전수 시험 계수가 다시 낡음.** [CLAUDE.md:118](/home/laptop/projects/workspaces/pd-audit-m19/A1/CLAUDE.md:118)의 `452 passed`와 현재 464개 수집이 불일치한다. 이번 신설 파일이 정확히 12개 테스트를 추가했지만 문서 정정이 이를 따라가지 못했다.

- **MAJOR — 신설 검사의 범위를 복수 지문 전체로 과장.** [docs/SPEC.md:1832](/home/laptop/projects/workspaces/pd-audit-m19/A1/docs/SPEC.md:1832)의 “그 지문들이 가리키는 파일”은 구현보다 넓다. 구현은 `request_digest ↔ request.md` 하나만 대조한다.

- **MINOR — 반증 도구 docstring이 도구 자체가 수행하지 않는 M-C 요청 파일 교체까지 실증한 것처럼 말함.** [tools/check_lane_binding.py:42](/home/laptop/projects/workspaces/pd-audit-m19/A1/tools/check_lane_binding.py:42). 기능과 별도 pytest는 존재하지만 해당 관문 도구 자체에는 그 변조 단계가 없다.

- **BLOCKER(검증 상태) — 필수 실행 증거 미완료.** 전수 시험 2회는 종료 1, lane-binding 2회는 종료 2였다. 원인은 모두 인용한 `No usable temporary directory found` 환경 오류다. 이 항목은 코드 실패와 구분하지만, 요청된 “plain/-O 동일 pass 및 관문 8회 exit 0”을 실측 승인할 수 없게 한다.

# 7. exclusions 관련 — 이연

아래는 현행 규칙 파일 자체가 이미 인정하는 반례이며, 재정 Q4에 따라 수정 요구·최종 판정 근거로 쓰지 않는다.

- **이연 — 과잉 배제 가능성:** [reader/reader-rules.yaml:1189](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/reader-rules.yaml:1189)의 `at least 12 <3:0>` 사례. `bit-slice` 봉투가 진짜 `12`를 함께 삼킬 수 있다.
- **이연 — 누락:** [reader/reader-rules.yaml:1220](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/reader-rules.yaml:1220)의 `FIGS. 3 and 4 illustrate …` 꼬리 번호.
- **이연 — 누락:** [reader/reader-rules.yaml:1459](/home/laptop/projects/workspaces/pd-audit-m19/A1/reader/reader-rules.yaml:1459)의 `Rows 0 and 1.` 복합 어형.

세 항목 모두 “등재하고 고치지 않음”으로 처리했으며 FAIL 판정에는 사용하지 않았다.

---

## 의뢰 C′-1 — 수확·배제 재계수 + 신설 검사 실동작 (read-only · setsid · EXIT=0)

**격 = `complete`** · 보존 경로 = ★ 보존본은 rollout 발굴분 — 판정 자체는 완주분이다(아래 주 참조) · 원문 23,140 B

### FINAL (원문 그대로)

# 판정: FAIL

기능 구현 자체는 대부분 정상입니다. 그러나 Q4의 “이 라운드에서 exclusions 판정 필드를 한 줄도 바꾸지 않았다”는 핵심 감수 주장이 지정 범위 `2eb30de..df1373e`에서 사실이 아닙니다.

## Findings

### F-1 — BLOCKER: Q4 값 공간 무변경 증명이 잘못된 커밋 경계를 사용함

처분 문서는 감수 범위를 `2eb30de..<신규 핀>`으로 명시합니다([D-20260831-01-m19-close.md:54](/home/laptop/projects/workspaces/pd-audit-m19/C1/docs/decisions/D-20260831-01-m19-close.md:54)). 그런데 Q4 증명은 더 늦은 `84219bc..HEAD`만 비교하고([같은 파일:152](/home/laptop/projects/workspaces/pd-audit-m19/C1/docs/decisions/D-20260831-01-m19-close.md:152)), “이 라운드가 … 한 줄도 바꾸지 않았다”고 결론 냅니다([같은 파일:136](/home/laptop/projects/workspaces/pd-audit-m19/C1/docs/decisions/D-20260831-01-m19-close.md:136)).

지정된 전체 범위의 실제 비교 결과:

```text
$ python3 - <<'PY'  # exact exclusion logic-field comparison, 2eb30de vs HEAD
base_exclusion_count = 7
head_exclusion_count = 7
figure-or-table-number-list.pattern:
  - '(?i)\\b(?:figures?|figs?|tables?)\\.?\\s*\\*{0,2}\\s*\\d+\\b\\*{0,2}(?:\\s*(?:,\\s*and|,|and)\\s*\\*{0,2}\\d+\\b\\*{0,2}(?!\\s*\\*{0,2}\\s*[A-Za-z°%µ×]))+'
  + '(?i)\\b(?:figures?|figs?|tables?)\\.?\\s*\\*{0,2}\\s*\\d+\\b\\*{0,2}(?:\\s*(?:,\\s*and|,|and)\\s*\\*{0,2}\\d+\\b\\*{0,2}(?!\\.\\d|\\s*\\*{0,2}\\s*[A-Za-z°%µ×]))+'
row-column-coordinate.match:
  - 'enclosing-pattern'
  + None
row-column-coordinate.pattern:
  - '(?i)\\b(?:rows?|columns?|cols?)\\s*\\*{0,2}\\d+\\*{0,2}\\b(?!\\.\\d)'
  + None
row-column-coordinate.preceding_pattern:
  - None
  + '(?i)\\b(?:rows?|columns?|cols?)\\s*\\*{0,2}\\s*$'
row-column-coordinate.condition:
  - None
  + ['소수점 없는 정수', '단위 없음', '그 수 **바로 앞**이 `preceding_pattern` 에 걸림(행·열 낱말이 수 앞에 온다)']

[exit_code=0]
```

현재 값은 [reader-rules.yaml:1268](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/reader-rules.yaml:1268) 및 [reader-rules.yaml:1397](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/reader-rules.yaml:1397)에 있습니다.

변경은 Q4가 선언되기 전 커밋 `88f7d77`에서 이루어졌고, `84219bc..df1373e`만 보면 실제로 다음 한 줄뿐입니다.

```text
$ git diff 84219bc..df1373e -- reader/reader-rules.yaml | grep -E '^[-+].*(pattern|condition):'
+    release_condition: >-
```

따라서 “Q4 선언 이후 다시 변경됐다”는 의미의 동결 위반은 아닙니다. 하지만 이번 감수의 고정 범위는 `2eb30de..df1373e`이며, 그 전체 범위에서 판정 필드가 바뀌었는데도 좁은 중간 기준점을 택해 “이 라운드 무변경”이라고 보고한 것은 사실과 다릅니다. 발주문이 명시한 FAIL 조건인 “값이 실제로 바뀌었는데 안 바뀌었다고 주장”에 해당합니다.

### F-2 — 비차단 문서 불일치: harvest.py 머리말이 현행 구현을 봉투 규칙으로 잘못 설명함

[harvest.py:24](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/lib/harvest.py:24)는 `Row 0` 같은 행·열 좌표도 “스캔 전에 통째로 표시”하는 구간 규칙이라고 설명합니다. 실제 코드는 이를 후보 생성 뒤 토큰 조건으로 처리합니다([harvest.py:117](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/lib/harvest.py:117), [harvest.py:373](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/lib/harvest.py:373)). 실행 동작과 YAML은 후자가 맞습니다.

## 1. `read.lane-log-digest-value` 실동작

초기 `.venv` 실행과 지시된 시스템 fallback은 사전 지정된 `TMPDIR=/dev/shm/pd-m19-c1`가 존재하지 않아 모두 수집 전에 실패했습니다.

```text
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/dev/shm/pd-m19-c1', '/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m19/C1']
[exit_code=1]
```

같은 실행 안에서 해당 임시 디렉터리를 만든 뒤 `.venv`를 다시 사용한 실제 출력:

```text
$ .venv/bin/pytest tests/test_m19_digest_value.py -q
............                                                             [100%]
=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:469
  /home/laptop/projects/workspaces/pd-audit-m19/C1/.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:469: PytestCacheWarning: could not create cache path /home/laptop/projects/workspaces/pd-audit-m19/C1/.pytest_cache/v/cache/nodeids: [Errno 30] Read-only file system: '/home/laptop/projects/workspaces/pd-audit-m19/C1/pytest-cache-files-zhhtjhml'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
12 passed, 1 warning in 0.40s

[exit_code=0]
```

`check_lane_binding.py`의 실제 출력:

```text
$ python3 tools/check_lane_binding.py --repo .
레인 왕복 시점 결속 — 변조 실증 (재정 2026-08-19 P-12 · S4)
  리포: /home/laptop/projects/workspaces/pd-audit-m19/C1

== ① 정상 — 요청 지문을 반향한 응답은 소비된다 ==
  [ok] 요청 지문이 레인 로그에 남는다
        기대 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
        실측 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
  [ok] 응답이 그 지문을 반향했다
        기대 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
        실측 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
  [ok] digest_ok
        기대 : True
        실측 : True
  [ok] 응답 지문 = 소비한 response.json 파일 바이트의 sha256
        기대 : 042325ef5d6f1dda36aeeceecc95b20b3fd86cf1a7b603ab61efb79aed597ea1
        실측 : 042325ef5d6f1dda36aeeceecc95b20b3fd86cf1a7b603ab61efb79aed597ea1
  [ok] 요청 지문 = 레인이 읽은 request.md 파일 바이트의 sha256
        기대 : 5e540f365cd38b7d4192323cd6084eb701af092b045fd730f2830a774d7013cc
        실측 : 5e540f365cd38b7d4192323cd6084eb701af092b045fd730f2830a774d7013cc
        참고 : `sha256sum 10-read/lanes/read-a/decompose/batch-0/response.json` 로 대조 가능

== ② 낡은 응답 — 요청이 갱신되었는데 옛 응답이 남아 있다 ==
  요청 변경: 수확 목록 1행 | `M2001` | frame width | `12.0` | mm | → | `M2001` | frame width | `12.5` | mm |
  구 판 지문 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
  신 판 지문 : 33070b159b26b0e0e9f6885bcae6202e0bf1bae5137cfaaa5596c4ef7d3262de
  [ok] 요청 내용이 바뀌면 입력 지문이 바뀐다
        기대 : 두 지문이 다르다
        실측 : 두 지문이 다르다
  [ok] 낡은 응답은 러너가 거부한다
        기대 : LaneStaleResponseError
        실측 : LaneStaleResponseError
        상세 : LaneStaleResponseError (반향 a7f2c5dd5be36c3d… ≠ 요청 33070b159b26b0e0…)
  [ok] 거부 사실이 레인 로그에 남는다(rejected · digest_ok)
        기대 : rejected=True digest_ok=False
        실측 : rejected=True digest_ok=False
  [ok] 거부 행이 반향된 옛 지문을 지목한다
        기대 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
        실측 : a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687

== ③ 응답 사후 교체 — 소비한 뒤 파일이 바뀌었다 ==
  로그가 지목한 소비본 : 042325ef5d6f1dda36aeeceecc95b20b3fd86cf1a7b603ab61efb79aed597ea1
  현재 파일의 sha256   : 8d998563912226ee7f0084f13afd90aa11a8a910d0fc2ceda82c584274eea62d
  [ok] 런이 소비한 응답과 현재 파일이 다름을 지문이 드러낸다
        기대 : 두 지문이 다르다
        실측 : 두 지문이 다르다
        뜻   : 로그의 response_digest 가 정본을 지목하므로, 같은 자리에 응답이 두 번 쓰여도
               런이 어느 쪽을 읽었는지 사후에 판정된다(감수 OOS-02 의 처분).

== ④ 절차 문서 변조 — 요청 필드는 그대로인데 프롬프트가 달라졌다 ==
  [ok] 절차 판 A 의 정상 왕복
        기대 : 소비되었다
        실측 : 소비되었다
  요청 필드 변경: 없음(두 요청의 필드는 한 글자도 다르지 않다)
  절차 변조 전 request.md : 31,262 B · 지문 a7f2c5dd5be36c3d1fb423f9d214283c141e7afe8c15338777fbf17372504687
  절차 변조 후 request.md : 31,413 B · 지문 6b56edff661d4d248d2e4f237c3268b275b4c73f161072150cfe82388a7a345a
  [ok] 절차 본문이 바뀌면 입력 지문이 바뀐다
        기대 : 두 지문이 다르다
        실측 : 두 지문이 다르다
  [ok] 절차 변조 뒤 구 응답은 러너가 거부한다
        기대 : LaneStaleResponseError
        실측 : LaneStaleResponseError
        상세 : LaneStaleResponseError (반향 a7f2c5dd5be36c3d… ≠ 요청 6b56edff661d4d24…)
  구 규격(요청 필드 정규 JSON) 지문 A : 6b30ad26e38876d32807311393411f3252b0d6cafd6b30c9cbc2df735b1757b4
  구 규격(요청 필드 정규 JSON) 지문 B : 6b30ad26e38876d32807311393411f3252b0d6cafd6b30c9cbc2df735b1757b4
  [ok] 구 규격이었다면 두 요청이 같은 지문을 들었다(= 구 응답이 통과했다)
        기대 : 두 지문이 같다
        실측 : 두 지문이 같다
        뜻   : 구 규격은 절차 문서를 경로 문자열로만 쟀으므로 본문 변조가 지문에 닿지 않았다.
               2026-08-19 감수 D 가 실측한 그 창(29,046 B ↔ 39,152 B, 지문 동일)을
               재정 S4 가 닫았고, 위 거부가 그 처분의 실행 반증이다.

== ⑦ 정상 — 로그의 요청 지문이 그 자리의 파일과 같다 ==
  로그가 적은 지문 : 5e540f365cd38b7d4192323cd6084eb701af092b045fd730f2830a774d7013cc
  파일의 sha256    : 5e540f365cd38b7d4192323cd6084eb701af092b045fd730f2830a774d7013cc
  [ok] 정직한 왕복은 값 검사를 통과한다
        기대 : pass
        실측 : pass
  [ok] 통과가 공허하지 않다(값 대조를 실제로 했다)
        기대 : digest_verified=1
        실측 : digest_verified=1
        참고 : `sha256sum digest-value/10-read/lanes/read-a/decompose/batch-0/request.md` 로 제3자가 같은 대조를 한다

== ⑤ 위조값 — 로그의 지문만 ffff…ffff 로 바꾼다(파일은 그대로) ==
  [ok] 위조값은 값 검사가 거부한다
        기대 : fail
        실측 : fail
  [ok] 거부 사유가 값 불일치로 지목된다
        기대 : ['lane-log.digest-value-mismatch']
        실측 : ['lane-log.digest-value-mismatch']
  [ok] ★ 같은 위조를 형태 검사는 지금도 통과시킨다(검사 id 를 나눈 근거)
        기대 : []
        실측 : []
        뜻   : 2026-08-19 감수 D 의 M-D 가 `pass checked=5 violations=0` 으로 통과했던 자리다.
               형태와 값은 다른 주장이며, 한 행이 둘을 지면 어느 쪽이 통과시켰는지 판정문에서 사라진다.

== ⑥ null 위장 — 요청 파일을 쓴 행의 지문을 null 로 바꾼다 ==
  request.md 실재 여부 : True
  [ok] null 위장은 제외로 새지 않는다
        기대 : fail
        실측 : fail
  [ok] 거부 사유가 면제 위장으로 지목된다
        기대 : ['lane-log.digest-null-disguise']
        실측 : ['lane-log.digest-null-disguise']
  [ok] 위장 행을 정당한 면제로 세지 않는다
        기대 : exempt_verified=0
        실측 : exempt_verified=0
  [ok] ★ 같은 위장을 형태 검사는 지금도 면제로 센다(검사 id 를 나눈 근거)
        기대 : []
        실측 : []
        뜻   : 면제의 자격은 **선언이 아니라 사실**이다 — 요청 파일이 그 자리에 없을 때만 면제다.
               감수 D 의 M-E 는 `exempt` 계수만 하나 늘리고 통과했다.

== ⑥-b 정당한 면제 — 요청 파일이 정말 없는 행은 통과한다 ==
  [ok] 요청 파일이 없는 행의 null 은 면제로 통과한다
        기대 : pass
        실측 : pass
        뜻   : 재정 2026-08-31 Q1 이 *"`None` 면제의 현행 축소분을 되돌리지 마라"* 로 명한 자리다.
               신설 검사는 면제를 없앤 것이 아니라 그 **자격을 사실로** 판정한다.

RESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 · 지문 위조 거부 · null 위장 거부 · 정당한 면제 보존 7종 전건 일치
        이 도구가 증명한 것은 러너가 낡은 응답을 거부하고 소비본을 지목한다는 것, 그리고
        레인 로그의 요청 지문이 그 자리의 파일을 지목한다는 것뿐이다. 그 밖은 증명하지 않는다.

[exit_code=0]
```

독립 fixture 결과:

```text
(a) forged 64-hex digest
  status = fail
  rules = ['lane-log.digest-value-mismatch']
  extras = {'digest_verified': 0, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}
(b) null while request.md exists
  status = fail
  rules = ['lane-log.digest-null-disguise']
  extras = {'digest_verified': 0, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}
(c) null while request.md is absent
  status = pass
  rules = []
  extras = {'digest_verified': 0, 'exempt_verified': 1, 'deferred_to_shape': 0, 'lanes_root_present': True}
(d) shape on value-forged but shape-complete journal
  status = pass
  rules = []
  extras = {'lane_tasks': {'read-a': ['decompose', 'synthesize'], 'read-b': ['decompose']}, 'request_digest_exempt': 0}
(e1) changed lanes_root + digest matching alternate root
  status = pass
  rules = []
  extras = {'digest_verified': 1, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}
(e2) lane_id swapped A->B, digest left as A
  status = fail
  rules = ['lane-log.digest-value-mismatch']
  extras = {'digest_verified': 0, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}
(e3) lane_id swapped A->B + digest changed to match B
  status = pass
  rules = []
  extras = {'digest_verified': 1, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}
(e4) request.md and logged digest changed consistently
  status = pass
  rules = []
  extras = {'digest_verified': 1, 'exempt_verified': 0, 'deferred_to_shape': 0, 'lanes_root_present': True}

[exit_code=0]
```

판정:

- (a) 위조값은 실제 FAIL입니다([read.py:1275](/home/laptop/projects/workspaces/pd-audit-m19/C1/engine/stages/read.py:1275)).
- (b) 파일이 있는데 `null`이면 실제 FAIL입니다([read.py:1233](/home/laptop/projects/workspaces/pd-audit-m19/C1/engine/stages/read.py:1233)).
- (c) 파일이 없는 `null`은 면제로 PASS합니다([read.py:1246](/home/laptop/projects/workspaces/pd-audit-m19/C1/engine/stages/read.py:1246)).
- (d) shape는 `request_digest`의 존재·공백 여부만 보고 값은 비교하지 않습니다([read.py:1093](/home/laptop/projects/workspaces/pd-audit-m19/C1/engine/stages/read.py:1093)). 신설 검사는 중복이 아닙니다.
- (e) `lanes_root` 교체, `lane_id`+digest 동시 교체, 파일+digest 동시 교체는 통과합니다. 함수가 선언하는 범위도 “전달받은 root 아래 현재 파일과 로그 값의 일치”뿐입니다([read.py:1199](/home/laptop/projects/workspaces/pd-audit-m19/C1/engine/stages/read.py:1199)). Q1 값 대조의 설계 범위 밖이며 별도 정본·시점 앵커가 필요합니다.

## 2. `exclusions_freeze` 로더 영향

[reader/lib/rules.py:461](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/lib/rules.py:461)는 `numeric_harvest.exclusions`만 꺼내 컴파일합니다. `exclusions_freeze`를 읽는 전용 경로는 없습니다.

직접 제거 전후 비교:

```text
removed_key_present = True
compiled_behavior_equal = True
envelope_count = 5
token_preceding_count = 1
freeze_attribute_exists = False

[exit_code=0]
```

따라서 `exclusions_freeze`는 메타데이터이며, 조용히 배제를 켜거나 끄는 부작용은 없습니다.

## 3. S7 수확 및 rc-0005 연결

네 입력의 실제 출력:

```text
$ python3 - <<'PY'  # direct harvest probes
'FIG. 3 and 4.5 mm'
  harvested = [('4.5 mm', 'mm')]
  skipped = [('FIG. 3', 'figure-or-table-number'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다')]
'a column 12 mm wide'
  harvested = [('12 mm', 'mm')]
  skipped = [('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다')]
'each column 5 mm'
  harvested = [('5 mm', 'mm')]
  skipped = [('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다')]
'a row 60 mm'
  harvested = [('60 mm', 'mm')]
  skipped = [('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다'), ('(부재)', 'patent 블록에 서지 필드 값이 없다')]

[exit_code=0]
```

모두 보존됩니다. 좌표 조건이 단위를 가진 후보를 즉시 제외 대상 밖으로 보내는 분기는 [harvest.py:393](/home/laptop/projects/workspaces/pd-audit-m19/C1/reader/lib/harvest.py:393)에 있습니다.

rc-0005는 장식 파일이나 하드코딩 복제가 아닙니다. 테스트가 [samples.json](/home/laptop/projects/workspaces/pd-audit-m19/C1/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:1)을 직접 읽고([test_m17_rules.py:587](/home/laptop/projects/workspaces/pd-audit-m19/C1/tests/test_m17_rules.py:587)), `harvest_numeric_facts()`를 호출한 뒤 golden의 `expect_values`·`expect_skipped`와 비교합니다([test_m17_rules.py:589](/home/laptop/projects/workspaces/pd-audit-m19/C1/tests/test_m17_rules.py:589)).

실행 출력:

```text
$ .venv/bin/pytest tests/test_m17_rules.py -q -k 'harvest_exclusion_counterexample_golden or exclusion_golden_carries'
................                                                         [100%]
=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:469
  /home/laptop/projects/workspaces/pd-audit-m19/C1/.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:469: PytestCacheWarning: could not create cache path /home/laptop/projects/workspaces/pd-audit-m19/C1/.pytest_cache/v/cache/nodeids: [Errno 30] Read-only file system: '/home/laptop/projects/workspaces/pd-audit-m19/C1/pytest-cache-files-i7fejqty'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
16 passed, 23 deselected, 1 warning in 0.55s

[exit_code=0]
```

## 4. 빈도 재계수

마크다운 강조와 옥스퍼드 쉼표를 포함한 YAML 기재 정규식으로 원천을 전수 스캔한 결과:

```text
characters = 293068
bytes = 293362
listing_matches = 37
whitespace_word_tail_count = 10
```

후행 낱말 10건의 원문 문맥과 분류:

```text
01 listing#01 next_word='illustrate' class=figure-number leak
   FIGS. **15**, **16**, **17**, **18** illustrate schemes for handling mantissa of data with a lower FP point precision in a col
02 listing#02 next_word='illustrate' class=figure-number leak
   FIGS. **20**, **21**, **22** illustrate schemes for handling exponents of data with various FP formats in a column cel
03 listing#03 next_word='illustrate' class=figure-number leak
   FIGS. **23**, **24**, **25** illustrate schemes for handling mantissas of data with various FP formats in a column cel
04 listing#05 next_word='illustrate' class=figure-number leak
   FIGS. **34**, **35**, **36**, and **37** illustrate schemes for aligning the mantissas, in accordance with some aspects of the pre
05 listing#06 next_word='illustrate' class=figure-number leak
   FIGS. **46**, **47**, **48** illustrate exemplary double-bitcell designs for scan operations, in accordance with some
06 listing#07 next_word='illustrate' class=figure-number leak
   FIGS. **61**, **62**, **63**, and **64** illustrate various schemes to optimize resources in the CIM macro, in accordance with som
07 listing#11 next_word='depict' class=figure-number leak
   FIGS. **7** and **8** depict enlarged views of exemplary column cell **220** in the CIM macro **101**. In CIM m
08 listing#18 next_word='illustrates' class=figure-number leak
   FIGS. **17** and **18** illustrates examples of mantissa computation between the activation value in FP8 (1-4-3)
09 listing#27 next_word='wordline' class=genuine quantity preserved
   FIG. **41**, **32** wordline signals wl0, wl1, . . . wl31 are provided to the column cells **220** in the com
10 listing#29 next_word='can' class=figure-number leak
   FIGS. **2** and **3** can include a first set of bitcells storing the first weight value and a second set of bi
```

원천 좌표는 각각 [patent.md:94](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:94), [96](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:96), [97](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:97), [102](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:102), [111](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:111), [122](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:122), [228](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:228), [248](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:248), [279](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:279), [287](/home/laptop/projects/workspaces/pd-audit-m19/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:287)입니다.

결론은 총괄의 정정과 정확히 일치합니다.

- 나열형: 37회
- 낱말 후행: 10건
- 도면 번호 누수: 9건
- 진짜 수량 보존: 1건 (`FIG. **41**, **32** wordline signals…`)

같은 특허에서 FIG. 32 자체도 3회 확인됐습니다: `FIGS. **32**-**33**`, 독립 캡션 `FIG. **32**`, 본문 참조 `FIG. **32**`.

미확인 항목은 없습니다. 리포 작업트리도 최종적으로 변경되지 않았습니다.

---

## 의뢰 C′-2 — 재정 이행 충실성 + 요구사항표 판정 (read-only · setsid · EXIT=0)

**격 = `complete`** · 보존 경로 = $FINAL 직접 회수 · 원문 16,345 B

### FINAL (원문 그대로)

# 판정: FAIL

실행 구현은 정상입니다. 전수 시험은 **464 passed**, 관문 8회는 전부 **exit 0**이었습니다. 그러나 재정 이행 문서가 실제 집행 범위를 축소 기록하고 있으며, Q3의 시험 수 정정도 현재 실측과 어긋납니다. 따라서 재정 이행 충실성 기준으로 PASS를 줄 수 없습니다.

주요 결함은 다음 세 가지입니다.

1. `check_lane_binding.py`는 실제로 7개 시나리오를 집행하지만, SPEC은 4개, CLAUDE는 3개라고 기록합니다. SPEC 자신이 이런 축소 기록을 blocker로 정의합니다. [SPEC.md:4488](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4488), [SPEC.md:4490](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4490), [CLAUDE.md:143](/home/laptop/projects/workspaces/pd-audit-m19/C2/CLAUDE.md:143), [check_lane_binding.py:609](/home/laptop/projects/workspaces/pd-audit-m19/C2/tools/check_lane_binding.py:609)
2. Q3이 요구한 전수 시험 수 정정이 `452 passed`에 멈췄습니다. 현재 실측은 `464 passed`입니다. [CLAUDE.md:118](/home/laptop/projects/workspaces/pd-audit-m19/C2/CLAUDE.md:118), [D-20260831-01-m19-close.md:117](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/decisions/D-20260831-01-m19-close.md:117)
3. 처분 기록의 신규 핀 칸이 여전히 비어 있습니다. 이번 발주가 `df1373e`로 범위를 명시했기 때문에 감수 자체의 범위는 식별 가능하지만, 처분 기록의 자체 규칙은 미이행입니다. [D-20260831-01-m19-close.md:59](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/decisions/D-20260831-01-m19-close.md:59)

## 1. 재정 Q1~Q4 이행 충실성

| 재정 | 판정 | 근거 |
|---|---|---|
| Q1 | **미달** | 신설 검사의 구현·분리·반증 효과는 충실하다. 다만 SPEC·CLAUDE·P-12 반증 셀이 실제 7개 관문 시나리오와 신설 시험을 반영하지 못했다. |
| Q2 | **충실** | 상태, 결함 서술, 측정값, 재상신 조건이 모두 보존·갱신됐다. |
| Q3 | **미달** | 5항 중 시험 수 정정이 현재 실측과 불일치하고 처분 기록의 신규 핀이 비어 있다. |
| Q4 | **충실** | Owner의 “6종” 문언은 보존하면서 실제 7항목 전부를 명시적으로 동결했다. 동결 범위는 모호하지 않고 위반도 없다. |
| 과잉 | **없음** | 범위 밖 구현 확대나 Q4 동결 대상 변경은 확인되지 않았다. |

### 원장 전사

외부 발주 총괄 문서도 읽을 수 있었습니다. 다음 대조는 차이가 없었습니다.

```text
diff -u \
  <(sed -n '29,112p' /home/laptop/projects/PD-M19-PROMPT.md) \
  <(sed -n '46,129p' docs/decisions/ruling-20260831-01-Q1-Q4.md)

diff_exit=0
```

따라서 원장 §2는 외부 문서 §2의 축자 전사입니다. 원장도 축자 전사임을 명시합니다. [PD-M19-PROMPT.md:29](/home/laptop/projects/PD-M19-PROMPT.md:29), [ruling-20260831-01-Q1-Q4.md:23](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/decisions/ruling-20260831-01-Q1-Q4.md:23)

### Q1 상세

값 대조는 별도 검사 `read.lane-log-digest-value`로 섰습니다.

- ID·엔진 등재부: [read.py:91](/home/laptop/projects/workspaces/pd-audit-m19/C2/engine/stages/read.py:91)
- 파일을 직접 여는 값 대조: [read.py:1162](/home/laptop/projects/workspaces/pd-audit-m19/C2/engine/stages/read.py:1162)
- 형제 검사와 별도 결과 행: [read.py:1552](/home/laptop/projects/workspaces/pd-audit-m19/C2/engine/stages/read.py:1552)
- 계약: [read.yaml:433](/home/laptop/projects/workspaces/pd-audit-m19/C2/contracts/stages/read.yaml:433)
- 용어집: [glossary.md:62](/home/laptop/projects/workspaces/pd-audit-m19/C2/contracts/glossary.md:62)

`CHECK_REGISTRY` 대신 `ENGINE_READ_CHECK_IDS`를 둔 것은 문언 회피가 아닙니다. `CHECK_REGISTRY`의 함수들은 파일시스템을 받지 못하지만 신설 검사는 `request.md`를 읽어야 합니다. 대체 등재부는 실제 출력 행 기대값에도 사용됩니다. [read.py:95](/home/laptop/projects/workspaces/pd-audit-m19/C2/engine/stages/read.py:95), [test_m2_read.py:1638](/home/laptop/projects/workspaces/pd-audit-m19/C2/tests/test_m2_read.py:1638)

용어집 시험을 read-only 메모리에서 뒤집어 신설 ID만 제거해 실행한 결과:

```text
engine_registry_contains= True
mutated_occurrences= 0
FLIP_RESULT=FAIL_AS_EXPECTED
contracts/glossary.md 에 등재되지 않은 검사 id: ['read.lane-log-digest-value']
```

즉 [test_m1_corpus.py:288](/home/laptop/projects/workspaces/pd-audit-m19/C2/tests/test_m1_corpus.py:288)은 실제로 `ENGINE_READ_CHECK_IDS`까지 훑으며, 요구 효과를 냅니다.

다만 문서에는 아직 구 3·4시나리오만 남아 있고, P-12 셀도 새 검사와 `tests/test_m19_digest_value.py`를 인용하지 않습니다. [SPEC.md:4620](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4620) 이 문서 전사 미달 때문에 Q1 전체는 **미달**입니다.

### Q2 상세

`open_question ③`은 “상신 대기”에서 “재정 종결”로 갱신됐습니다. [reader-rules.yaml:1362](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1362)

동시에 결함 자체는 삭제되지 않았습니다.

> `Table 2.5 mm of clearance` → 수확 0건 … 진짜 `2.5 mm`가 침묵으로 소실

[reader-rules.yaml:1365](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1365)

재상신 조건도 판별식으로 고정됐습니다.

```text
(?i)(?:figs?|figures?|tables?)\.?\s*\*{0,2}\d+\.\d
```

[reader-rules.yaml:1392](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1392)

따라서 종결된 것은 “고칠 것인가”이며, “결함이 존재하는가”는 기록에 남습니다.

### Q3 상세

재정의 범위 5항 [ruling:87](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/decisions/ruling-20260831-01-Q1-Q4.md:87) 중:

1. Q1 검사 구현·반증: 이행
2. Q2 원장·규칙 갱신: 이행
3. CLAUDE 시험 수 정정: **미이행 — 452 기록, 실제 464**
4. 직전 보수의 범위 고정 재감수: 이 보고에서 수행
5. 종결 가부 판정표: 이 보고에서 수행하나, 리포의 신규 핀 칸은 공란

따라서 전부 집행됐다고 할 수 없어 **미달**입니다.

### Q4 상세

Owner 원문의 “6종”은 고치지 않았고, scope가 실제 대상을 명확히 했습니다.

> 재정의 「6종」은 낡은 계수이며, 동결의 실제 범위는 이 목록의 항목 전부다.  
> 실측 … 항목은 7

[reader-rules.yaml:1063](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1063)

금지·허용·예외·해제 조건도 재정과 일치합니다. [reader-rules.yaml:1076](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1076), [reader-rules.yaml:1080](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1080), [reader-rules.yaml:1083](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1083), [reader-rules.yaml:1089](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/reader-rules.yaml:1089)

동결 직전 `84219bc`와 현재를 파싱 비교한 결과:

```text
old_count= 7 new_count= 7
guard_signature_equal= True
```

따라서 “6”을 역사적 문언으로 보존하면서 “목록 전부 = 7”을 고정한 처리는 옳습니다. 동결 범위는 모호하지 않으며 좁힘·넓힘도 없었습니다.

## 2. 직전 보수 확인

| 보수 | 판정 | 근거 |
|---|---|---|
| 요구사항표 반증 셀 갱신 | 확인 | [SPEC.md:4583](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4583), [SPEC.md:4606](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4606) |
| SPEC 집계 문단 재작성 | 확인 | 16행과 34안건의 차이를 설명한다. [SPEC.md:4624](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4624) |
| D-20260819-02 §5.1 후속 정정 | 확인 | “8/5” 과계수를 실측으로 정정한다. [D-20260819-02-m17-close.md:195](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/decisions/D-20260819-02-m17-close.md:195) |
| Q5 ④ 부착 순위 NCA | 확인 | [10-decompose.md:74](/home/laptop/projects/workspaces/pd-audit-m19/C2/reader/procedure/10-decompose.md:74) |
| `is_pinned_harvest_drift` oracle 조임 | 확인 | 고정 ID·좌표·예상값을 대조한다. [test_m16_bibliography.py:117](/home/laptop/projects/workspaces/pd-audit-m19/C2/tests/test_m16_bibliography.py:117) |
| N14-12·P-5 재정 원문 고정 | 확인 | 계약 내용과 원장 원문을 별도 대조한다. [SPEC.md:4594](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4594) |
| P-7 좌표 정정 | 확인 | accept/reject/accept 세 픽스처와 실제 스키마 관문이 연결됐다. [SPEC.md:4618](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4618) |
| P-B 진짜 값 보존 | 확인 | 보존·배제 golden과 실제 수확기 시험이 존재하고 통과한다. [SPEC.md:4612](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4612) |

다만 커밋 연대에 관한 발주문의 표현은 저장소 이력과 다릅니다. 다섯 보수 전부가 `2eb30de` 이후에 들어간 것은 아닙니다.

- 요구사항표·집계·Q5 보수: `4172fd0` — `2eb30de`의 조상
- oracle 보수: `1017f4d` — `2eb30de`의 조상
- D 후속 정정: `2eb30de` 자체
- 실제 후속 P-B 보수: `88f7d77`

따라서 이번에 확인한 것은 “현재 HEAD에서 보수가 실재하고 작동한다”는 사실이며, “다섯 보수가 모두 핀 이후 커밋이다”라는 이력 명제는 사실이 아닙니다.

P-12의 나머지 절반은 **런타임으로는 완결**됐습니다. 기존 요청 파일 지문 결속에 더해 값 위조·`null` 위장·사후 교체가 새 검사에서 막힙니다. [test_m19_digest_value.py:147](/home/laptop/projects/workspaces/pd-audit-m19/C2/tests/test_m19_digest_value.py:147) 다만 공식 요구사항표 반증 셀이 이를 반영하지 않아 요구사항 판정은 부분 해소입니다.

관련 집중 시험:

```text
.....................................                                    [100%]
37 passed, 1 warning in 2.32s
```

## 3. 요구사항표 34안건 판정

분모는 지시대로 안건 ID 34개입니다. 취소선 P-9와 “M1 관할이 아닌 생존 지적”은 제외했습니다.

| ID | 판정 | 앵커 |
|---|---|---|
| N14-1 | 해소 | [SPEC:4583](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4583) |
| N14-2 | 해소 | [SPEC:4584](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4584) |
| N14-3 | 해소 | [SPEC:4585](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4585) |
| N14-4 | 해소 | [SPEC:4586](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4586) |
| N14-5 | 해소 | [SPEC:4587](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4587) |
| N14-6 | 해소 | [SPEC:4588](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4588) |
| N14-7 | 해소 | [SPEC:4589](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4589) |
| N14-8 | 해소 | [SPEC:4590](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4590) |
| N14-9 | 해소 | [SPEC:4591](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4591) |
| N14-10 | 해소 | [SPEC:4592](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4592) |
| N14-11 | 해소 | [SPEC:4593](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4593) |
| N14-12 | 해소 | [SPEC:4594](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4594) |
| N14-13 | 해소 | Owner 재정에 의한 범위 제외·무변경이 반증됨. [SPEC:4595](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4595) |
| N14-14 | 해소 | [SPEC:4596](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4596) |
| P-1 | 해소 | [SPEC:4606](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4606) |
| P-2ⓐ | 해소 | [SPEC:4607](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4607) |
| P-2ⓑ | 해소 | [SPEC:4608](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4608) |
| P-3 | 해소 | [SPEC:4609](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4609) |
| P-4 | 해소 | [SPEC:4610](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4610) |
| P-A | 해소 | [SPEC:4611](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4611) |
| P-U4 | 해소 | [SPEC:4611](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4611) |
| P-B | 해소 | [SPEC:4612](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4612) |
| P-C | 해소 | [SPEC:4613](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4613) |
| P-U1 | 해소 | [SPEC:4614](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4614) |
| P-8 | 해소 | [SPEC:4614](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4614) |
| P-U2 | 해소 | [SPEC:4615](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4615) |
| P-U3 | 해소 | [SPEC:4616](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4616) |
| P-U5 | 해소 | [SPEC:4617](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4617) |
| P-5 | 해소 | [SPEC:4618](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4618) |
| P-6 | 해소 | [SPEC:4618](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4618) |
| P-7 | 해소 | [SPEC:4618](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4618) |
| P-12 | **부분 해소** | 구현·시험은 완결됐지만 셀이 구 4시나리오만 인용한다. [SPEC:4620](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4620) |
| P-14 | 해소 | [SPEC:4621](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4621) |
| P-11 | 해소 | 이번 감수가 고정 핀·항목별 표·재정 대조를 제공한다. [SPEC:4622](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4622) |

같은 자에 따른 변화:

| 라운드 | 해소 | 부분 해소 | 미해소 |
|---|---:|---:|---:|
| PD-M1.7 | 19 | 14 | 1 |
| PD-M1.8 | 30 | 4 | 0 |
| **PD-M1.9** | **33** | **1** | **0** |

SPEC의 `16행`은 표의 반증 실재 여부를 세는 행 단위 분모이고, 위 `34`는 구현 해소 여부를 세는 안건 ID 분모입니다. 현재 문단은 그 구별을 명시하므로 두 수가 다른 것 자체는 결함이 아닙니다. [SPEC.md:4624](/home/laptop/projects/workspaces/pd-audit-m19/C2/docs/SPEC.md:4624)

## 4. 전수 시험과 관문

`/dev/shm` 경로가 격리된 실행 사이에 유지되지 않아, 같은 셸에서 디렉터리를 준비한 뒤 지시된 TMPDIR로 실행했습니다.

```text
$ mkdir -p /dev/shm/pd-m19-c2 &&
  env TMPDIR=/dev/shm/pd-m19-c2 ./.venv/bin/pytest tests/ -q

................................                                         [100%]
=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:469
  PytestCacheWarning: cache could not write path .../.pytest_cache/v/cache/nodeids:
  [Errno 30] Read-only file system

464 passed, 1 warning in 89.72s (0:01:29)
```

경고는 저장소가 read-only라 `.pytest_cache`를 쓸 수 없다는 내용이며 시험 실패가 아닙니다.

관문은 plain과 `-O`에서 각각 실행했습니다.

| 관문 | plain | `-O` | 실제 종결 출력 |
|---|---:|---:|---|
| `check_spec_refs.py` | 0 | 0 | `RESULT: PASS` |
| `check_schema_enforcement.py` | 0 | 0 | `SUMMARY: cases=37 REJECT_OK 23/23 ACCEPT_OK 12/12 VALIDATOR_SCOPE 2/2 schemas=4` |
| `check_validator_enforcement.py` | 0 | 0 | `RESULT: PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족` |
| `check_lane_binding.py` | 0 | 0 | `RESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 · 지문 위조 거부 · null 위장 거부 · 정당한 면제 보존 7종 전건 일치` |

즉 총괄의 **관문 8회 전부 exit 0** 주장은 맞습니다. 전수 시험 수 주장만 `452`가 아니라 **464**입니다. 작업 트리는 감수 종료 시에도 clean한 detached HEAD `df1373e`였습니다.

---

## 의뢰 D — 변조 반증 (workspace-write + --add-dir · setsid · EXIT=0)

**격 = `complete`** · 보존 경로 = $FINAL 직접 회수(사본 내부) · 원문 10,671 B

### FINAL (원문 그대로)

FAIL

핀 커밋은 `df1373e0a4f196ad650a02dfb9cfa61f79db7e5c`로 일치했습니다. 재정 Q1의 단독 위조 3종은 닫혔지만, 실제 저장된 `lane-log.json` 변조가 자동 재검사되지 않고 `lane_id` 경로 이탈도 허용되어 전체 판정은 FAIL입니다.

## 주요 findings

1. BLOCKER — 실제 `lane-log.json` 변조를 운영 경로가 검사하지 않습니다.

   관문은 “실제 파일·실제 러너 경로”라고 주장하지만([check_lane_binding.py:307](/home/laptop/projects/workspaces/pd-audit-m19/D/tools/check_lane_binding.py:307)), 실제로는 디스크 로그가 아니라 `journal.rows`의 복사본만 바꿉니다([check_lane_binding.py:355](/home/laptop/projects/workspaces/pd-audit-m19/D/tools/check_lane_binding.py:355), [check_lane_binding.py:381](/home/laptop/projects/workspaces/pd-audit-m19/D/tools/check_lane_binding.py:381)). 실측 생성 파일 9개 중 `lane-log.json`은 0개였습니다.

   생산 러너도 인메모리 저널을 먼저 검사하고([read.py:1558](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1558)), 실제 로그는 그 뒤 `finally`에서 씁니다([read.py:1617](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1617), [read.py:1663](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1663)).

   전체 FileLaneAdapter 런에서 디스크 로그를 `ffff…ffff`로 바꾼 실측:

   - 변조 전 보고: `pass`, `checked=5`, `violations=0`
   - 디스크 `lane-log.json` 변조 후 기존 `convergence.json`: 여전히 `pass`
   - 로그를 수동으로 다시 읽어 함수를 호출한 경우에만 `lane-log.digest-value-mismatch`

   즉 검사 함수 자체는 잡지만, 저장된 런을 재검사하는 배선/도구가 없습니다. 실제 로그 변조는 **NOT DETECTED**입니다.

2. BLOCKER — `lane_id` 어휘·루트 경계가 집행되지 않습니다.

   계약은 `"<read_run>/<task>[/retry-<n>]/batch-<k>"`를 정본으로 선언합니다([read.yaml:166](/home/laptop/projects/workspaces/pd-audit-m19/D/contracts/stages/read.yaml:166)). 그러나 `LaneRequest`는 비어 있지 않은지만 검사하고([contract.py:158](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/lanes/contract.py:158)), `lane_dir()`는 분절을 그대로 `os.path.join`합니다([contract.py:418](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/lanes/contract.py:418)).

   `lane_id="../../escaped/batch-0"` 실측:

   - 설정 루트: `…/configured/lanes`
   - 실제 기록: `…/escaped/batch-0`
   - `within_root=False`
   - `read.lane-log-digest-value`: `pass`, `digest_verified=1`

   FileLaneAdapter가 루트 밖에 요청 파일을 쓰고도([file_adapter.py:78](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/lanes/file_adapter.py:78)) 아무 검사도 거부하지 않았습니다.

3. HIGH — 로그와 파일의 동시 위조는 통과합니다.

   `request.md`에 `## [AUDIT COMBINED FILE+LOG TAMPER]`를 추가하고 로그 값을 재계산한 `84d4481bb9e2fd9323097e7101f4819b921b9e2e656d8edb9bbdaafbb9c60ae5`로 바꾸자 `pass`, `digest_verified=1`이었습니다.

   구현은 현재 파일 해시와 현재 로그 문자열의 단순 동등만 봅니다([read.py:1262](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1262), [read.py:1275](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1275)). 신뢰된 이전 지문이나 로그 봉인이 없어 내용 무결성이 아니라 내부 일관성만 증명합니다. 코드도 루트의 정당성은 증명하지 않는다고 명시합니다([read.py:1199](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1199)).

## 임무 0 — 함정 F 실측

| 항목 | 실제 명령·출력 | 프로세스 rc | 후속 확인 |
|---|---|---:|---|
| A 작업공간 쓰기 | `touch probe.wtest && echo "rc=$?"` → `rc=0` | 0 | 삭제 완료 |
| B `.git` 쓰기 | `touch .git/.wtest && echo "rc=$?"` → `rc=0` | 0 | 삭제 완료 |
| C 되돌리기 | README 첫 줄 `# patent-docent` → `# patent-docent [MISSION-0-C-WRITE-PROBE]`; `git checkout -- README.md` → `rc=0` | 0 | 직접 읽은 첫 줄 `# patent-docent`; 작업 파일과 `HEAD` SHA-256 모두 `8b865385f45c745c696ae7e797d2ba8865acdb737af1af91a6c34d2ef1e410e8`; `cmp` rc=0 |
| D 인덱스 조작 | `git add -N .` → `rc=0` | 0 | 직후 porcelain 출력 없음 |

따라서 **“함정 F 처방이 이 세션에서 실제로 작동한다”**고 판정합니다.

## 변조표

| 대상 검사/파일 | 기준선 | 변조 내용 | 변조 후 | 탐지자 |
|---|---|---|---|---|
| digest-value / 실제 임시 `lane-log.json` | `pass`, checked=1, verified=1 | `request_digest` `b8e859…b7149` → `ffff…ffff` 64자 | `fail`, violations=1 | `lane-log.digest-value-mismatch` |
| digest-value / 실제 로그 | 동일 | `request_digest` → JSON `null`, 실제 `request.md` 존치 | `fail` | `lane-log.digest-null-disguise` |
| digest-value / 실제 `request.md` | 동일 | 끝에 `## [AUDIT M-C POST-CONSUMPTION SWAP]` 추가, 로그 불변 | `fail` | `lane-log.digest-value-mismatch` |
| digest-value / 로그+파일 | 동일 | 파일에 `## [AUDIT COMBINED FILE+LOG TAMPER]` 추가 + 로그를 `84d448…0ae5`로 재계산 | `pass`, verified=1 | **NOT DETECTED** |
| digest-value / `lanes_root` | 동일 | 빈 `wrong-empty-root`로 전환 | `fail` | `lane-log.digest-file-missing` |
| digest-value / `lanes_root` | 동일 | `wrong-shadow-root`로 전환하고 동일 파일 복제 | `pass`, verified=1 | **NOT DETECTED** — 명시된 범위 밖 |
| digest-value / `lane_id` | 동일 | `batch-0` → `batch-9`, 대상 파일 없음 | `fail` | `lane-log.digest-file-missing` |
| digest-value / `lane_id` | 동일 | `batch-0` → `batch-9` + 동일 파일 배치 | `pass`, verified=1 | **NOT DETECTED** |
| FileLaneAdapter / `lane_id` | 정상 ID는 루트 안 기록·검사 pass | `../../escaped/batch-0` | 루트 밖 기록, 검사 `pass` | **NOT DETECTED** |
| 면제 보존 | 파일 존재·지문 값 → pass | 파일 삭제 + `request_digest:null` | `pass`, `exempt_verified=1` | 정상 면제 보존 |
| 관문 시나리오 ⑤ / [read.py:1275](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1275) | 관문 exit 0 | `if actual != …` → `if False and actual != …` | exit 1, 반증 실패 2건 | `check_lane_binding.py` ⑤ |
| 관문 시나리오 ⑥ / [read.py:1235](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1235) | exit 0 | `if present` → `if False and present` | exit 1, 반증 실패 3건 | `check_lane_binding.py` ⑥ |
| 관문 시나리오 ⑦ / [read.py:1287](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1287) | verified=1, exit 0 | `verified += 1` → `verified += 0` | exit 1, 공허 통과 적발 | `check_lane_binding.py` ⑦ |
| P-12·S4 / [contract.py:463](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/lanes/contract.py:463) | 낡은 응답·절차 변조 구응답 거부, exit 0 | 지문 불일치 조건을 `False and …`로 무력화 | exit 1, 실패 3건 | 시나리오 ②·④ |
| 문서·계약 관문 / [read.yaml:433](/home/laptop/projects/workspaces/pd-audit-m19/D/contracts/stages/read.yaml:433) | K1~K8 PASS | 신설 검사 ID 행을 닫히지 않은 YAML 배열로 변경 | exit 1, K6 결함 1 | `K6 계약 파일 파싱` |
| 스키마 관문 / [material-spec.schema.json:178](/home/laptop/projects/workspaces/pd-audit-m19/D/reader/schemas/material-spec.schema.json:178) | 37/37 일치 | scalar의 required에서 `approximate` 삭제 | exit 1, reject 22/23 | `material-spec.value-type-missing-approximate.json` |
| 검증기 관문 / [derivation.py:612](/home/laptop/projects/workspaces/pd-audit-m19/D/reader/lib/derivation.py:612) | 42/42 일치 | parity 직전 `expected = actual.copy()`로 차집합 소거 | exit 1, 2/42 불일치 | `value.harvest-parity` 코퍼스 |
| 실제 종료 로그 / [read.py:1617](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1617) | 저장 보고 `pass`, checked=5 | 종료 후 디스크 로그 첫 행을 `ffff…ffff`로 변경 | 저장 보고 그대로 `pass` | **NOT DETECTED**; 수동 재로딩 때만 탐지 |

각 추적 파일 변조 뒤 `git checkout -- <파일>`과 `git diff --exit-code -- <파일>`을 실행했으며 복원 rc는 전부 0이었습니다.

## 기존 회귀와 결과 공존

- P-12 낡은 응답 거부와 S4 절차 본문 변조 거부는 clean 기준선에서 모두 작동했습니다.
- 신설 검사 무력화와 P-12 무력화가 각각 관문 exit 1을 냈으므로 시나리오가 공허하지 않습니다.
- 결과 행 공존 실측은 `read.lane-log-shape = fail(2)`와 `read.lane-log-digest-value = pass(0)`가 직렬화 뒤에도 두 행 그대로 유지됐습니다. 기존 결과를 덮어쓰는 문제는 없습니다. 배선은 [read.py:1558](/home/laptop/projects/workspaces/pd-audit-m19/D/engine/stages/read.py:1558), 직렬화는 [run_checks.py:121](/home/laptop/projects/workspaces/pd-audit-m19/D/reader/lib/run_checks.py:121)에 있습니다.

검증 결과:

- 전수 기준선: `464 passed in 101.03s`
- 최종 관련 회귀: `73 passed in 5.20s`
- 최종 관문 4종: 모두 exit 0
- `check_lane_binding.py`: `RESULT: PASS … 7종 전건 일치`

## 배제 봉투 동결 — 이연

동결 대상은 수정하지 않았습니다.

- `numeric_harvest.exclusions`: 7항, SHA-256 `6d758de115966c3925a1a0bff4fd84f4a6a48337691af79df86e3d872067b90c`
- `git diff -- reader/reader-rules.yaml`: 없음
- golden 및 실특허 재현: `16 passed`

현행 반례 두 건은 재확인했지만 지시대로 **이연**합니다.

- `FIGS. 3 and 4 illustrate…`에서 둘째 도면 번호 `4`가 수치로 남음([samples.json:56](/home/laptop/projects/workspaces/pd-audit-m19/D/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:56)).
- `Rows 0 and 1.`이 좌표가 아니라 값 집합 `0 and 1`로 수확됨([samples.json:80](/home/laptop/projects/workspaces/pd-audit-m19/D/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:80)).

처분: **이연**. 해제 조건은 `numeric.exhaustive`와 `numeric.unreviewed-use` 구현 및 실물 런 1회 통과입니다([reader-rules.yaml:1089](/home/laptop/projects/workspaces/pd-audit-m19/D/reader/reader-rules.yaml:1089)). 이것들은 FAIL 근거로 사용하지 않았습니다.

## 최종 clean 확인

실제 최종 명령:

```text
$ git status --porcelain
```

stdout 0바이트, 프로세스 rc=0입니다. 작업 트리와 인덱스 모두 clean입니다.

---
