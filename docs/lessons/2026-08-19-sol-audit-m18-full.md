# sol 독립 감수 원문 — M1.8 분할 감수 4의뢰 (2026-08-19 후속)

**보존 근거.** 재정 2026-08-18 **N7** — 외부 감수 산출물은 수령 즉시 **원문 그대로** `docs/lessons/` 에 보존한다. 처분표·요약은 이 원문을 가리키는 포인터일 뿐이다. 압축 보존은 M0 에서 지적 2건의 문언을 영구히 잃게 만들었다.

| 항목 | 값 |
|---|---|
| 핀 커밋 | `2eb30de81f0068a646820eadc1459af8ae1e84dd` (4의뢰 전건 대조 일치) |
| 감수자 | GPT-5.6-sol, reasoning effort **max** |
| 격리 사본 | `~/projects/workspaces/pd-audit-m18/{A,C1,C2,D}` — 핀 커밋의 완전 클론(`--no-hardlinks`) · `.venv` 사전 구축 · **마커 `.audit-sandbox`**(재정 S5) |
| 샌드박스 | A′·C′-1·C′-2 = `read-only` · D = `workspace-write`(재정 Q9 ⓐ) |
| 실행 형태 | **CAP 없음**(재정 S6 — 조항 폐지) · 배경 실행 + 파일 리다이렉션 + `EXIT=` 마커 + 폴링 |
| 격 | **4의뢰 전건 `complete`** — 1차 실행이 그대로 완주했다. 회수분 없음 |
| 판정 | A′ **FAIL** · C′-1 **FAIL(P-B 부분 해소)** · C′-2 **FAIL** · D **FAIL** |

**★ 이 라운드가 처음 증명한 것 셋.**

① **새 실행 체제가 작동했다.** 직전 라운드는 4의뢰가 **전건 1차에 죽었고**(하네스 10분 상한) 둘은 회수로만 판정을 얻었다. 이번엔 CAP 을 걸지 않고 배경 실행 + 폴링으로 돌려 **넷 다 1차에 완주**했다. 가장 긴 D 는 약 30분이었다 — **포그라운드였다면 죽었을 길이다.**
② **마커 preflight 가 실전에서 통과했다**(재정 S5 의 첫 적용). D 의뢰가 쓰기 모드 진입 전 3검증 실출력을 판정문에 실었고, 종료 시 사본이 clean 이며 핀이 불변이다.
③ **감수가 이 라운드 자신의 개정에서 결함을 찾아냈다.** C′-1 과 D 가 **독립으로 같은 결함**에 닿았다 — S7 신설 배제가 진짜 수치를 삼킨다. 재정 S7 이 승인 조건으로 내건 반례 요건이 바로 그 자리를 겨눴는데, 총괄이 세운 반례 표본이 그 형태를 덮지 못했다.

**경로 표기 주의.** 아래 판정문의 절대경로는 **격리 사본**(`/home/laptop/projects/workspaces/pd-audit-m18/<의뢰>/`)을 가리킨다. 정본 리포의 같은 상대경로로 읽으면 된다 — 사본은 핀 커밋의 완전 클론이므로 내용이 같다.

---

## 의뢰 A′ — 기계적 확인 (read-only · CAP 없음 · 약 521초)

### FINAL (원문 그대로 — `7445 B`)

# 판정: FAIL

## NEW BLOCKER — §8.3 관문 설명표가 실행물과 불일치

1. `check_spec_refs.py`는 실제로 **K1~K8**을 실행하지만 §8.3 표는 **K1~K7**만 열거합니다.

   - 실행물: [tools/check_spec_refs.py:3](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_spec_refs.py:3), [tools/check_spec_refs.py:177](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_spec_refs.py:177)
   - 불일치 표: [docs/SPEC.md:4482](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4482)
   - 동일한 낡은 설명: [docs/SPEC.md:3728](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:3728)

   실출력:

   ```text
   PASS  K8  코어·확장 경계  (해소 8 · 면제 0 · 결함 0)
   RESULT: PASS
   EXIT=0
   ```

2. `check_validator_enforcement.py`는 **기준선 12종 청정성**까지 판정하지만 §8.3 표는 변조본 및 하한 검사만 설명합니다.

   - 기준선이 도구의 명시적 검사임: [tools/check_validator_enforcement.py:21](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_validator_enforcement.py:21)
   - 누락된 §8.3 표: [docs/SPEC.md:4484](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4484)
   - 같은 SPEC의 다른 표는 P-14 기준선을 인정함: [docs/SPEC.md:4616](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4616)

범위 7의 필수 대조 대상 자체가 실행물의 증명 범위를 정확히 기록하지 않으므로 PASS로 종결할 수 없습니다.

## 실행 결과

### 1. 발주 핀

```text
$ git rev-parse HEAD
2eb30de81f0068a646820eadc1459af8ae1e84dd
```

발주 핀과 정확히 일치합니다.

### 2. 전수 테스트

무설정 명령은 테스트 시작 전에 임시 디렉터리 오류로 죽었습니다.

```text
$ .venv/bin/pytest tests/ -q
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/laptop/projects/workspaces/pd-audit-m18/A']
EXIT_CODE=1
```

이 실행의 통과·실패 테스트 수는 `NOT ASSESSED`입니다. 테스트가 수집되기 전에 종료됐기 때문입니다.

확인된 쓰기 가능 임시 루트로 재실행한 결과:

```text
$ TMPDIR=/dev/shm .venv/bin/pytest tests/ -q
.........                                                                [100%]
=============================== warnings summary ===============================
PytestCacheWarning: could not create cache path ... Read-only file system ...
441 passed, 1 warning in 89.20s (0:01:29)
EXIT=0
```

실제 집계는 **441 passed, 0 failed**로 총괄 수치와 일치합니다.

### 3. 관문 plain/`-O`

| 관문 | plain | `-O` |
|---|---:|---:|
| `check_spec_refs.py` | `EXIT=0` | `EXIT=0` |
| `check_schema_enforcement.py` | `EXIT=0` | `EXIT=0` |
| `check_validator_enforcement.py` | `EXIT=0` | `EXIT=0` |
| `check_lane_binding.py` — 기본 읽기 전용 환경 | `EXIT=2` | `EXIT=2` |
| `check_lane_binding.py` — `TMPDIR=/dev/shm` | `EXIT=0` | `EXIT=0` |

주요 실출력:

```text
# check_schema_enforcement.py — plain과 -O 동일
SUMMARY: cases=37 REJECT_OK 23/23 ACCEPT_OK 12/12 VALIDATOR_SCOPE 2/2 schemas=4
EXIT=0
```

```text
# check_validator_enforcement.py — plain과 -O 동일
RESULT: PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족
EXIT=0
```

```text
# check_lane_binding.py — 기본 환경, plain과 -O 동일
ENVIRONMENT ERROR: 임시 작업장을 만들 수 없다 — FileNotFoundError: [Errno 2] No usable temporary directory found in [...]
EXIT=2
```

따라서 총괄의 “8회 전부 exit 0”은 **기본 읽기 전용 환경에서는 재현되지 않았습니다: 6회 exit 0, 2회 exit 2**입니다. 다만 쓰기 가능한 `TMPDIR`을 제공하면 lane 관문도 plain/`-O` 모두 exit 0입니다.

### 4. JSON 기준선

`--json`은 exit 0이었고 실값은 다음과 같습니다.

```text
check_id                     checked  violations  vacuous
read.schema                        1           0  none
read.source-digest                 1           0  none
read.verbatim                     83           0  none
read.pointer-resolve             123           0  none
read.coverage                     24           0  none
read.dependency-parse              6           0  none
read.value-derivation             24           0  none
read.bibliography                 12           0  none
read.claim-inventory               9           0  none
read.convergence                   6           0  none
freeze.id-monotonic               89           0  none
freeze.payload-immutable          46           0  none
```

관련 JSON 원출력:

```json
"failures": [],
"vacuous": [],
"escalations": [],
"escalation_conflict": ""
```

```json
"cases": 42,
"floor_findings": [],
"mismatches": []
```

```text
EXIT=0
```

결론: 검사 **12종 전부 존재**, 모든 `violations=0`, 행별 `vacuous="none"`, 기준선 `vacuous=[]`. 변조본은 plain 출력의 **42/42**, JSON의 `cases=42` 및 `mismatches=[]`로 확인됐습니다.

### 5. 직전 A′ FAIL 사유

**해소가 실증됐습니다.**

- 종료 코드 규약은 [docs/SPEC.md:4474](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4474)의 `2 = 입력·환경 오류`입니다.
- 도구는 환경 오류를 `ENVIRONMENT ERROR`로 출력하고 exit 2로 끝냅니다: [tools/check_lane_binding.py:91](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_lane_binding.py:91).
- 임시 작업장 생성 예외를 잡는 구현은 [tools/check_lane_binding.py:413](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_lane_binding.py:413)입니다.
- 기본 환경의 plain/`-O` 모두 **exit 2**, 환경 오류 진단문 있음, **`Traceback` 없음**.
- `TMPDIR=/dev/shm`에서는 plain/`-O` 모두 다음과 같이 성공했습니다.

```text
RESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 4종 전건 일치
EXIT=0
```

임시 위치 확인:

```text
TMPDIR=/dev/shm
tempfile.gettempdir()=/dev/shm
```

도구는 `/dev/shm/lane-binding-*`에 작업장을 만들고 종료 시 삭제합니다([tools/check_lane_binding.py:420](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_lane_binding.py:420), [tools/check_lane_binding.py:429](/home/laptop/projects/workspaces/pd-audit-m18/A/tools/check_lane_binding.py:429)). 최종 잔존 검색 결과는 비어 있었습니다.

### 6. 작업트리 오염

```text
$ git status --porcelain
```

출력 없음. 실행 전후 모두 clean이며 사본을 더럽히지 않았습니다.

### 7. 관문 간 증거 혼용

다른 관문의 통과를 서로의 증거로 쓰는 서술은 발견하지 못했습니다. 오히려 SPEC은 이를 명시적으로 금지합니다.

> “네 도구는 각자 하나의 주장만 증명하며, 하나의 통과는 다른 하나의 증거가 아니다.”

앵커: [docs/SPEC.md:4478](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4478), 특히 runner와 앞의 세 관문을 분리한 [docs/SPEC.md:4485](/home/laptop/projects/workspaces/pd-audit-m18/A/docs/SPEC.md:4485).

## OUT-OF-SCOPE

- `OOS-01`: 무설정 pytest가 읽기 전용 환경에서 임시 디렉터리 문제로 traceback/exit 1을 냅니다. 이는 M1 READ 구현 실패가 아니라 pytest 실행환경 문제이며, `/dev/shm`을 지정하면 441건 전부 통과합니다.
- 그 밖의 신규 범위 밖 지적은 없습니다.

---

## 의뢰 C′-1 — P-B 재계수 · 배제 신설의 독립 검증 (read-only · CAP 없음)

### FINAL (원문 그대로 — `12061 B`)

## BLOCKER

**Verdict: FAIL — P‑B는 `부분 해소`.**

S7의 “순도는 P‑B 밖”이라는 기준은 그대로 적용했다. 실패 사유는 잔여 아티팩트가 아니라, 신설 배제가 **진짜 값을 삼켜 P‑B 첫 요건인 전수 수확을 깨는 반례 2건**이다.

- `figure-or-table-number-list`는 꼬리 정수 뒤의 소수점을 막지 않는다. [reader-rules.yaml:1192](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1192)의 `\d+\b`는 `4.5`의 `4`에서 끝날 수 있다. 직접 실행 결과:

  > 입력: `FIG. 3 and 4.5 mm of clearance remains`  
  > 신설 패턴 매치: `FIG. 3 and 4`  
  > 수확된 quoted 값: `[]`

  봉투와 조금이라도 겹친 후보 전체를 버리기 때문이다([harvest.py:243](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:243), [harvest.py:259](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:259)). 진짜 `4.5 mm`가 소실된다.

- `row-column-coordinate`는 정수 뒤의 단위를 막지 않는다. [reader-rules.yaml:1231](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1231)은 소수만 `(?!\.\d)`로 보호한다. 직접 실행 결과:

  > 입력: `a column 12 mm wide carries current`  
  > 신설 패턴 매치: `column 12`  
  > 수확된 quoted 값: `[]`

  진짜 치수 `12 mm`가 소실된다.

현 golden은 정수 `4 mm`와 “수→낱말” 어순만 다뤄 이 두 반례를 잡지 못한다([samples.json:24](/home/laptop/projects/workspaces/pd-audit-m18/C1/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:24), [samples.json:32](/home/laptop/projects/workspaces/pd-audit-m18/C1/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:32)).

## ① P‑B 다섯 요건 대조

기준 문언은 정확히 다섯이다([SPEC.md:4607](/home/laptop/projects/workspaces/pd-audit-m18/C1/docs/SPEC.md:4607)); S7도 같은 범위를 확정한다([ruling:130](/home/laptop/projects/workspaces/pd-audit-m18/C1/docs/decisions/ruling-20260819-03-S1-S9.md:130)).

| 요건 | 구현·반증 | 판정 |
|---|---|---|
| 접지 스팬 기반 전수 수확 | 스캔 범위 [reader-rules.yaml:854](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:854), 생성기 [harvest.py:98](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:98), 누락/추가 시험 [test_m1_reader.py:1789](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m1_reader.py:1789), [test_m1_reader.py:1834](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m1_reader.py:1834) | **부분 충족** — 위 진짜 값 손실 |
| 수확 소유권 | 소유 origin [harvest.py:63](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:63), quoted/bibliographic 생성 [harvest.py:374](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:374), [harvest.py:410](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/harvest.py:410), 소유권 집행 문언 [reader-rules.yaml:1414](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1414) | 충족 |
| `value.harvest-parity` | 정확 집합대조 [derivation.py:570](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/derivation.py:570), 누락·추가·변조 시험 위 두 함수 | 충족 |
| `numeric_refs` 역참조 | 스키마 필수 [material-spec.schema.json:619](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/schemas/material-spec.schema.json:619), [material-spec.schema.json:641](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/schemas/material-spec.schema.json:641), fact-kind 해소 [pointers.py:103](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/pointers.py:103), 시험 [test_m1_reader.py:1856](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m1_reader.py:1856), [schema test:429](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_contracts_schema_enforcement.py:429) | 충족 |
| CP1 전량 카운트 | 인벤토리 계산 [derivation.py:676](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/lib/derivation.py:676), 렌더 [material_spec_md.py:475](/home/laptop/projects/workspaces/pd-audit-m18/C1/engine/render/material_spec_md.py:475), 시험 [test_m2_read.py:2551](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m2_read.py:2551) | 충족 |

SPEC가 열거한 시험 이름은 모두 실제 정의다. 신설 배제 시험 6개는 [test_m17_rules.py:499](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:499)부터, 기존 보존 시험은 [test_m16_harvest_boundary.py:208](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m16_harvest_boundary.py:208)에 있다. 역참조 변조본도 실제 등록돼 있다([manifest.json:514](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/fixtures/reader/manifest.json:514)).

표적 pytest 결과는 다음과 같다.

> `27 passed in 1.12s`

즉 기존 시험은 통과하지만, 새 반례를 포함하지 않아 blocker를 발견하지 못한다.

## ② 패턴 직접 판정

`harvest_numeric_facts` 직접 실행 결과다.

| 입력 | 신설 패턴 | quoted 결과 |
|---|---|---|
| `Tables 1 and 2.` | 목록 전체 포착 | 없음; 봉투 배제 |
| `Row 0` / `Col 0` | 각각 전체 포착 | 없음; 좌표 배제 |
| `between 1 and 2` | 무매치 | `1 and 2` 보존 |
| `the gap is between 1 and 2 mm` | 무매치 | `1 and 2 mm` 보존 |
| `60 columns and 60 rows` | 무매치 | `60`, `60` 보존 |
| `FIG. 3 and 4 mm` | 신설 목록은 무매치; 기존 봉투가 `FIG. 3`만 포착 | `4 mm` 보존 |
| 자체: `FIG. 3 and 4.5 mm…` | `FIG. 3 and 4` 포착 | **진짜 값 소실** |
| 자체: `a column 12 mm wide…` | `column 12` 포착 | **진짜 값 소실** |
| 자체: `the column 12.5 mm wide…` | 무매치 | `12.5 mm` 보존 |
| 자체: `Rows 0 and 1.` | `Rows 0`만 포착 | `1` 아티팩트 잔류 |
| 자체: `FIGS. 7, 8, and 9.` | 전체 포착 | 없음 |
| 자체: `FIG. 3 and 4% efficiency…` | 신설 목록 무매치 | `4%` 보존 |

## ③ golden 실효성

두 golden 모두 놓여만 있지 않고 실제 엔진에 연결된다.

- `rc-0004`: [test_m17_rules.py:443](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:443)이 `samples.json`을 읽어 `Rules.structure_markers_in()`과 실제 dependency 검사를 실행한다. 기대값은 golden의 `expect_structures`·`expect_escape_check`에서 읽는다([samples.json:5](/home/laptop/projects/workspaces/pd-audit-m18/C1/ledgers/regression/golden/rc-0004-conditional-marker-counterexamples/samples.json:5)).
- `rc-0005`: [test_m17_rules.py:540](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:540)이 파일을 읽어 `harvest_numeric_facts()`와 `expect_values`·`expect_skipped`를 비교한다. 기대 결과는 시험 코드에 복제되지 않았다([samples.json:5](/home/laptop/projects/workspaces/pd-audit-m18/C1/ledgers/regression/golden/rc-0005-harvest-exclusion-counterexamples/samples.json:5)).
- 양방향 표본과 장부 등록도 검사한다([test_m17_rules.py:471](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:471), [test_m17_rules.py:571](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:571), [test_m17_rules.py:627](/home/laptop/projects/workspaces/pd-audit-m18/C1/tests/test_m17_rules.py:627), [cases.jsonl:4](/home/laptop/projects/workspaces/pd-audit-m18/C1/ledgers/regression/cases.jsonl:4)).

따라서 실행성은 PASS다. 다만 `rc-0005`의 표본 공간이 불충분하여 위 두 과광화 반례를 놓친다.

## ④ 현행 재수확

핀 산출은 고치거나 결함으로 세지 않았다. S7의 효과만 분리하려고 현행 규칙에서 신설 두 패턴만 메모리상 제외한 대조군과 비교했다.

> 신설 두 패턴 제외: `origin: quoted` 17건  
> 현행 전체 규칙: `origin: quoted` 14건  
> 제거 3, 변경 0, 추가 0

제거된 것은 정확히 다음 셋이다.

- M87: `[0186][117,118)`의 `2` — `Tables 1 and 2` 뒤 항([material-spec.json:2325](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/10-read/material-spec.json:2325))
- M88: `[0140][36,37)`의 `0` — `Row 0`([material-spec.json:2350](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/10-read/material-spec.json:2350))
- M89: `[0140][46,47)`의 `0` — `Col 0`([material-spec.json:2375](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/10-read/material-spec.json:2375))

현행 14건은 모두 exponent-width, 행·열 개수, LCM 값 등 공학량이며 아티팩트는 **0건**이다. 따라서 총괄의 **17 → 14, 정확히 M87~M89 셋** 주장은 PASS다.

참고로 핀 JSON 자체에는 active quoted가 13건이다. 현행 Q4 규칙이 `5b·4b·3b·2b` 네 건을 새로 수확하고 S7이 세 건을 제거해 현행 14가 된다. 이는 구 산출의 결함 계상이 아니다.

## ⑤ 원천 61구간 전수 판정

각 신설 regex를 원천 전체에 독립 `finditer`한 결과는 **30 + 31 = 61구간**이며, 실제 공학량은 **0건**이었다.

- `figure-or-table-number-list` 30건:  
  L94 `15,16,17`; L96 `20,21`; L97 `23,24`; L102 `34,35,36`; L111 `46,47`; L122 `61,62,63`([patent.md:94](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:94));  
  L201 `1,2`; L207 `1,2`; L231 `7,8`×2; L232 `7,8`; L236 `7,8`; L237 `8,10`×2; L251 `Tables 1 and 2`×2; L253 `FIGS. 3,7`; L254 `Tables 1 and 2`; L257 `FIGS. 2,4`([patent.md:201](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:201));  
  L262 `Tables 6,7`와 `FIGS. 63,64`; L275 `4,38`; L284 `3,8`; L288·290·291·296·302 `41,44`; L298 `41,43`; L337 `48,49`([patent.md:262](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:262)).

- `row-column-coordinate` 31건:  
  L201 `Col 0,1,2,31` + `Row 0,1,2,31`; L203 `Row 0`,`Col 0`; L206 동일; L217 `row 0`,`column 0`; L228 `row 0`,`column 0`×2; L242·264 각각 `row 0`,`column 0`; L268 `Row 0`,`Row 31`; L348 `Col0,Col1,Col2,Col 31,Row0,Row1,Row3,Row31`([patent.md:201](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:201), [patent.md:348](/home/laptop/projects/workspaces/pd-audit-m18/C1/runs/openai-us20260147854a1-cim-fp-3/00-source/patent.md:348)).

따라서 **이 특허 원천에 한정한 “61구간 전부 참조·좌표, 진짜 수치 0” 주장은 PASS**다. 그러나 일반 엔진의 전수성은 위 합성 반례 두 건 때문에 FAIL이다.

## OUT-OF-SCOPE

- 순도 잔여: `Rows 0 and 1.`은 `1`을 남기며, `FIGS. 15, 16, 17, 18 illustrate…`도 마지막 번호를 남길 수 있다. 규칙 파일도 이를 명시한다([reader-rules.yaml:1220](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1220), [reader-rules.yaml:1254](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1254)). S7상 순도 문제이므로 종결 차단 사유로 세지 않았다.
- 규칙의 “293,068 B” 표기는 단위가 틀렸다([reader-rules.yaml:1214](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1214)). 실측은 **293,068 characters / 293,362 bytes**다. 61구간 판정에는 영향 없다.
- `answer_scope`와 L0 정답지 문언의 자동 동치 시험은 규칙 파일 스스로 “아직 없다”고 기록한다([reader-rules.yaml:1381](/home/laptop/projects/workspaces/pd-audit-m18/C1/reader/reader-rules.yaml:1381)). 현재 값은 일치하며 P‑B 문언의 별도 요건은 아니므로 비차단이다.
- 전체 저장소 테스트 스위트는 **NOT ASSESSED**. P‑B 및 두 golden 관련 표적 27개만 실행했다.

`docs/decisions/D-*.md`의 자기 보고는 근거로 사용하지 않았다.

---

## 의뢰 C′-2 — 재정 S1~S9 이행 충실성 + 요구사항표 판정 (read-only · CAP 없음)

### FINAL (원문 그대로 — `23059 B`)

# VERDICT: FAIL

핀은 정확합니다.

> `git rev-parse HEAD` → `2eb30de81f0068a646820eadc1459af8ae1e84dd`  
> `git status --short` → 출력 없음  
> `git log c31fff5^..2eb30de -- runs` → 출력 없음

재정 P-11은 “전 항목 해소 = 종결”로 정합니다. 현재 S2·S4·S5가 미달이고, 34개 요구사항 판정 중 4개가 부분 해소이므로 M1을 종결할 수 없습니다. [P-11 원문](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260818-03-P1-P11.md:60)

## 신규 BLOCKER

1. **S4 요청 파일 지문 게이트가 실제 파일 오류를 면제한다.**  
   `_request_file_digest()`는 요청서를 쓰지 않는 어댑터뿐 아니라 파일 미존재·권한·읽기 오류 등 모든 `OSError`를 `None`으로 바꿉니다. 게이트는 그 `None`을 결함이 아니라 면제 건으로 셉니다. [구현](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:206), [게이트](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:1047)

   독립 재현 결과:

   > `digest=None`  
   > `request_digest_exempt=1`  
   > `request-file-digest findings=[]`

   따라서 파일 어댑터의 `request.md`가 사라지거나 읽히지 않아도 `lane-log.request-file-digest`가 실패하지 않습니다. 재정 S4의 “각 행이 요청 파일 바이트 지문을 들며 판정 항목이 된다”에 미달합니다. [재정 S4](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260819-03-S1-S9.md:100)

   또한 `None`을 통과값으로 추가한 것은 게이트 값 공간 변경인데 재정 근거가 없습니다. 총괄 자기점검의 4건 목록에도 빠졌습니다. [S2 기준](/home/laptop/projects/workspaces/pd-audit-m18/C2/CLAUDE.md:28), [자기점검 대상](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/D-20260819-03-m18-close.md:83)

2. **S5/Q9의 기계 강제 범위가 실제보다 넓게 서술됐다.**  
   마커 규격은 `path`, `pin`, `order`, `disposable=true` 네 필드입니다. [재정](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260819-03-S1-S9.md:112), [SPEC](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4501)  
   하지만 실제 preflight는 파일 존재, `path`, `pin`만 검사하고 `order`와 `disposable=true`는 검증하지 않습니다. [실제 3검증](/home/laptop/.claude/agents/sol-auditor.md:39)  
   그럼에도 SPEC은 “마커 3검증이 기계로 잡는 것은 규격 ④”라고 요약합니다. [과장 문언](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4506) 이는 M0.6이 FAIL 사유로 삼았던 강제 범위 과장과 같은 형태입니다.

3. **N14-12/P-5의 반증 시험은 정확한 재정 내용을 고정하지 않는다.**  
   P-5는 파일 단위·다각도 각각·흐름도 포함이라는 정확한 세 처분을 명합니다. [P-5 원문](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260818-03-P1-P11.md:62) 구현 계약에는 그대로 있습니다. [계약](/home/laptop/projects/workspaces/pd-audit-m18/C2/contracts/stages/source.yaml:103)  
   그러나 표가 인용한 시험은 필드의 truthiness와 `resolutions` 길이가 3인지까지만 검사합니다. [시험 본문](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:845) 세 처분을 임의의 다른 세 문장으로 바꿔도 통과하므로 해당 요구를 실제로 반증하지 못합니다.

4. **P-7의 “반증 미작성”은 사실이 아니다.**  
   표는 여전히 P-7 반증이 없다고 적습니다. [SPEC §8.4](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4613) 그러나 활성 manifest에는 이미 다음 세 표본이 있습니다.

   - 168h·offset 32h를 비표준 시점으로 보존하는 정상 표본
   - 같은 값에 `within_window: true`를 심어 거부시키는 ±24h 변조본
   - `not-collected` 어휘의 정상 표본

   [manifest](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/fixtures/schema-enforcement/manifest.json:167), [스키마 집행](/home/laptop/projects/workspaces/pd-audit-m18/C2/contracts/schemas/metrics-row.schema.json:91)

   직접 실행 결과도 각각 `accept / reject / accept`로 전건 기대 일치했습니다. 즉 없는 것은 반증이 아니라 **표의 인용**입니다.

## ① S1~S9 이행 충실성

| 재정 | 판정 | 근거 |
|---|---|---|
| S1 | 충실 | `ff23407`은 회수 원문 정확히 4파일만 추가했습니다. 네 파일의 격도 `partial(events)` 2건·`recovered(resume)` 2건으로 표시됩니다. [원장](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260819-03-S1-S9.md:58), [격 표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/RULINGS-LEDGER.md:66) |
| S2 | **미달** | 판별 기준 자체는 CLAUDE에 정확히 성문화됐습니다. 그러나 S4의 `None` 면제가 재정 없이 게이트 통과값을 늘렸고 자기점검에서 누락됐습니다. [CLAUDE](/home/laptop/projects/workspaces/pd-audit-m18/C2/CLAUDE.md:28), [예외 구현](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:206) |
| S3 | 충실 | 목록은 10개 그대로이고 바뀐 패턴은 정확히 세 앵커입니다. [목록](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/reader-rules.yaml:328), [`unresponsive to` 반례](/home/laptop/projects/workspaces/pd-audit-m18/C2/ledgers/regression/golden/rc-0004-conditional-marker-counterexamples/samples.json:8), [실행 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m17_rules.py:425) |
| S4 | **미달** | 전체 본문 해시·제3자 재계산·로그 판정·비소급은 구현됐지만, 실제 파일 오류가 면제로 통과합니다. [해시 구현](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/lanes/contract.py:188), [면제 게이트](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:996) |
| S5 | **미달** | 사본 규격은 문서화됐으나 “규격 ④를 기계가 잡는다”는 문언과 달리 `order`·`disposable`은 검증되지 않습니다. [SPEC](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4494), [실물](/home/laptop/.claude/agents/sol-auditor.md:32) |
| S6 | 충실 | 리포는 CAP 폐지와 배경 실행 형태의 외부 정본 포인터만 둡니다. 외부 정의에도 CAP 실행 변수 없이 배경 실행·리다이렉션·종료 마커·폴링이 있습니다. [SPEC](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4508), [외부 포인터](/home/laptop/.claude/agents/sol-auditor.md:135) |
| S7 | 충실 | 두 배제 모두 `[가설]`, 사유, `why`, 미결, 재정 S7 근거를 갖습니다. 반례 golden은 보존·배제 양방향을 실제 수확기에 투입합니다. [규칙 1](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/reader-rules.yaml:1189), [규칙 2](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/reader-rules.yaml:1228), [시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m17_rules.py:499) |
| S8 | 충실 | 부칙 4조가 원장, SPEC, RULINGS-LEDGER에 같은 내용으로 있고 회수 4건 모두 격이 표시됩니다. [원장](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260819-03-S1-S9.md:145), [SPEC](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4514), [LEDGER](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/RULINGS-LEDGER.md:71) |
| S9 | 충실 | 리포는 외부 `LEDGER.md`·git을 참조만 합니다. 외부에는 3단 변경 절차와 L-005가 있고 독립 git 이력도 확인했습니다. [리포 원장](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/RULINGS-LEDGER.md:33), [외부 원장](/home/laptop/.claude/agents/LEDGER.md:57) |

`과잉` 판정은 없습니다.

### S4 직접 재계산과 행위시법

테스트의 `probe_request()`를 렌더한 바이트를 `/dev/fd`로 `grep`에 넘겨 독립 계산했습니다.

> 선언 지문: `c69b7808529dde5681aa7645de25ce694221cffe56a4b587bc3f013daea84068`  
> `grep -v '^| 입력 지문 |' … | sha256sum`: `c69b7808529dde5681aa7645de25ce694221cffe56a4b587bc3f013daea84068`

렌더러는 지문 행 한 줄만 삽입하고, 제외 접두 충돌도 거부합니다. [렌더·제외 규칙](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/lanes/contract.py:281), [셸 시험 본문](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m16_lane_binding.py:187)

다만 샌드박스에 쓸 수 있는 임시 디렉터리가 없어 새 물리 파일을 작성한 뒤의 실행은 **NOT ASSESSED**입니다. 파일 어댑터 경로는 정적으로만 확인했습니다. [파일 어댑터](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/lanes/file_adapter.py:89)

참 요청서 없는 재생 어댑터의 제외 건수는 `request_digest_exempt`에 남아 조용하지 않습니다. 문제는 같은 `None`이 파일 오류에도 사용되어 두 원인을 구별하지 못한다는 것입니다. [현재 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m16_lane_binding.py:450)

행위시법은 지켜졌습니다. S 라운드 범위의 `git log … -- runs`와 경로 diff가 모두 빈 출력입니다.

## ② M1 요구사항표 34개 판정

직전 판정과 같은 계산법으로 N14 14개 + P 계열 20개를 셌습니다. P-5/P-6/P-7은 따로, 취소된 P-9와 표 밖 P-13도 직전 판정과 같이 별도 판정합니다.

**집계: 해소 30 · 부분 해소 4 · 미해소 0 · NOT ASSESSED 0**

| 행 | 판정 | 실재 앵커 |
|---|---|---|
| N14-1 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4578), [날조값 변조 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1080) |
| N14-2 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4579), [자기참조·순환 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1090) |
| N14-3 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4580), [파생의 파생 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:903) |
| N14-4 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4581), [누락·유령·정상 대조](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2201) |
| N14-5 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4582), [공유 material/역방향 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1263) |
| N14-6 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4583), [한글 `_en` 거부](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:884) |
| N14-7 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4584), [청구항 누락·0건 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:967) |
| N14-8 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4585), [정책 3종 실제 분기](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:750) |
| N14-9 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4586), [payload·전이·승계 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1008) |
| N14-10 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4587), [유형 불일치 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1062) |
| N14-11 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4588), [버전 연동 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:830) |
| N14-12 | **부분 해소** | 구현은 실재하지만 공통 반증 시험이 정확한 세 논점 내용을 고정하지 않습니다. [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4589), [시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:834) |
| N14-13 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4590), [판정 제외·별도 계수](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1700) |
| N14-14 | 해소 | 기록은 [D 문서](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/D-20260818-02-m1-read.md:127)에 있고, 독립 실행도 `pytest 9.1.1`, `Python 3.14.4`로 일치했습니다. |
| P-1 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4601), [회피 봉쇄 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1723) |
| P-2a | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4602), [서지 변조 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1749) |
| P-2b | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4603), [K8 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_tools_check_spec_refs.py:126) |
| P-3 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4604), [세 정책 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:750) |
| P-4 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4605), [조기 수렴 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2444), [내용맹 정본](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2479) |
| P-A/P-U4 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4606), [메모 2건](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:1653), [통합 레인 비공개](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:1784) |
| P-B | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4607), [추가·누락 수확 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m1_reader.py:1789), [S7 반례 실투입](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m17_rules.py:542) |
| P-C | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4608), [환경 오류 시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:1598), [새 런 강제](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2653) |
| P-U1/P-8 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4609), [worktree 시험군](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_tools_run_worktree.py:109) |
| P-U2 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4610), [본문 변경 표시](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m16_source_supersede.py:256), [상호 링크](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m16_source_supersede.py:346) |
| P-U3 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4611), [비정본 접지 부재](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2512), [진입 게이트](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2611) |
| P-U5 | 해소 | [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4612), [EN 값 대조](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:2255) |
| P-5 | **부분 해소** | 구현은 정확하지만 시험이 세 처분의 내용·단위 값을 비교하지 않습니다. [계약](/home/laptop/projects/workspaces/pd-audit-m18/C2/contracts/stages/source.yaml:96), [시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m2_read.py:845) |
| P-6 | 해소 | 5/5, 결원 불통과, 죽은 인스턴스만 재시도, 기계 강등 금지를 실제 함수에 물립니다. [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4613), [시험](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/test_m16_quorum.py:121) |
| P-7 | **부분 해소** | 구현과 활성 반증은 있지만 표가 이를 인용하지 않고 “미작성”이라고 오기합니다. [manifest](/home/laptop/projects/workspaces/pd-audit-m18/C2/tests/fixtures/schema-enforcement/manifest.json:167), [오기](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4613) |
| P-9 | 해소(이관) | M1 요구에서 취소되고 예행 계약으로 이관됐습니다. [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4614), [원장 P-15](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/decisions/ruling-20260819-01-P12-P15.md:34) |
| P-12 | **부분 해소** | 본문 결속은 섰지만 요청 파일 오류가 `None` 면제로 통과합니다. [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4615), [결함 구현](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:206) |
| P-13 | 해소 | 실재 런은 `openai-us20260147854a1-cim-fp-3`입니다. [단계·CP1](/home/laptop/projects/workspaces/pd-audit-m18/C2/runs/openai-us20260147854a1-cim-fp-3/TONGJU-REPORT.md:35), [12개 pass 행](/home/laptop/projects/workspaces/pd-audit-m18/C2/runs/openai-us20260147854a1-cim-fp-3/10-read/convergence.json:7), [핀](/home/laptop/projects/workspaces/pd-audit-m18/C2/runs/openai-us20260147854a1-cim-fp-3/run.yaml:47) |
| P-14 | 해소 | 기준선 12종·공허 0, 변조본 42건 전건 기대 일치였습니다. [표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4616), [도구 범위](/home/laptop/projects/workspaces/pd-audit-m18/C2/tools/check_validator_enforcement.py:21) |
| P-11 | 해소(제도 형식) | 이 판정문이 요구사항 34행, S1~S9 대조, 직전 미달, OOS 및 격을 분리해 제도 형식을 수행합니다. [요건](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4617) |

### 표 집계 문장

물리적 P 표의 계산은 맞습니다.

- 17행 중 취소 P-9를 빼서 16행
- P-2a/P-2b는 별도 행
- P-5/P-6/P-7은 물리적으로 한 행
- “요구 충족”이 아니라 “셀이 인용한 증거의 존재”만 셈

이 규칙은 문장 안에 명시돼 있고, 그 제한된 규칙으로는 `14 전부 실재 + 1 일부 + 1 제도`가 표와 일치합니다. [세는 규칙](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4619), [집계](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4621)

다만 의미상 설명은 부정확합니다. P-7 증거는 이미 실재하고, P-5 증거는 존재하지만 요구 전체를 반증하지 못합니다. 따라서 산술은 맞아도 증거 충실성 설명은 맞지 않습니다.

### 직전 P-13 유령 앵커 재검증

직전 앵커는 실제로 없습니다. [직전 잘못된 좌표](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/lessons/2026-08-19-sol-audit-m17-full.md:307)

독립 검사 결과:

> 직전 핀의 요구사항 판정표에서 고유 리포 경로 22개 검사  
> `missing=1`  
> 유일한 누락 = `runs/20260819-101806-a2fbddd2/reports/TONGJU-REPORT.md`

현재 사본, 전체 git 경로 이력, `/home/laptop/projects/workspaces/**`에서도 무검색이었습니다. 다른 직전 판정표 경로 앵커의 물리적 누락은 발견되지 않았습니다. P-13 판정은 실제 런과 `convergence.json`을 근거로 그대로 해소입니다.

## ③ 직전 미달 3건

| 직전 미달 | 이번 판정 | 근거 |
|---|---|---|
| Q5① 전제부 재검토 트리거 | **해소** | 규칙 파일에 긴 전제부·실질 한정 다수 실물을 만나면 규약대로 비요소 처리하고 상신하라는 트리거가 있습니다. [규칙](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/reader-rules.yaml:824), [절차](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/procedure/10-decompose.md:55) |
| Q5④ 후보 밖 NCA | **해소** | 현행 순위 ④는 선택을 후보 집합 안으로 제한하고, 유일 지배 후보가 없으면 원문 첫째로 폴백합니다. 선택과 배치의 층 구별 및 1차 판단의 부정확 판정도 보존됩니다. [절차](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/procedure/10-decompose.md:74), [개정 이력](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/procedure/10-decompose.md:76), [SPEC §9.33②](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:5510) |
| Q9 문언뿐인 격리 | **부분 해소** | `path`·`pin`에 의한 정본 경로 차단은 기계화됐습니다. 그러나 필수 마커 필드 `order`·`disposable`은 실제 preflight가 검사하지 않아 §8.3의 “규격④ 기계 강제” 문언과 완전히 일치하지 않습니다. [SPEC](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4504), [실물](/home/laptop/.claude/agents/sol-auditor.md:39) |

## 실행·검증 범위

실행한 것:

- S3·S7 관련 수집 시험: **18 passed**
- 요구사항표의 비임시파일 시험: **20 passed**
- 검증기 관문: 기준선 **12종**, 공허 0, 변조본 **42건**, 결과 `PASS`
- P-7 스키마 표본 3건: `accept / reject / accept` 기대 일치
- 렌더 요청 지문 셸 재계산 일치
- `OSError → None → 면제` 경로 독립 재현

실행하지 못한 것:

- 전체 pytest 및 `tmp_path` 의존 시험
- 새 물리 `request.md`를 작성하는 시험

읽기 전용 샌드박스에 `/tmp`, `/var/tmp`, 작업 디렉터리 중 쓸 수 있는 임시 경로가 없어 pytest 수집 단계에서 중단됐습니다. 이는 제품 시험 실패로 계상하지 않았습니다.

## OUT-OF-SCOPE

- 규칙 문서는 “6종 중 하나라도 없으면 로드에서 죽는다”고 쓴 직후 실제로는 “하나 이상 존재”만 본다고 적습니다. 실제 로더도 특정 6종 전부가 아니라 최소 1종만 요구합니다. [문서 모순](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/reader-rules.yaml:1265), [실제 로더](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/lib/rules.py:473)
- `check_lane_log_shape` docstring은 “판정 5항”이라 쓰지만 바로 아래에는 형태 3항 + 결속 3항, 총 6항을 열거합니다. [코드](/home/laptop/projects/workspaces/pd-audit-m18/C2/engine/stages/read.py:985)
- §8.4의 산출·DoD 문단은 현행 `reader_version`을 아직 `0.5.0`으로 적습니다. 실파일과 정본 이력은 `0.8.0`입니다. [낡은 문언 1](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4539), [낡은 문언 2](/home/laptop/projects/workspaces/pd-audit-m18/C2/docs/SPEC.md:4553), [실파일](/home/laptop/projects/workspaces/pd-audit-m18/C2/reader/READER-VERSION:1)

결론적으로 직전 Q5 두 미달은 닫혔지만 Q9은 부분 해소이고, 새로 확인된 S2/S4 게이트 면제 및 요구사항표 증거 결함 때문에 M1 종결은 **FAIL**입니다.

---

## 의뢰 D — 변조 반증 (workspace-write · 마커 3검증 통과 · 약 30분)

### FINAL (원문 그대로 — `8322 B`)

# 판정: FAIL

S4의 핵심 처분인 “절차 본문 변경 → 지문 변경 → 구 응답 거부” 자체는 PASS입니다. 하지만 이번 변조에서 신규 BLOCKER 두 계열이 확인됐습니다.

## NEW BLOCKER

1. `request_digest`의 값과 제외 사유가 검증되지 않습니다.

   - 64자리 위조값 `ffff…ffff`로 바꿔도 `read.lane-log-shape`가 `pass`, `violations=0`.
   - 실제 `FileLaneAdapter`가 `request.md`를 쓴 행을 `null`로 바꿔도 `pass`; `request_digest_exempt=1`만 증가합니다.
   - 검사기는 키 부재·빈 값만 실패시키고, `null`은 무조건 제외합니다. [read.py:1051](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/stages/read.py:1051), [read.py:1060](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/stages/read.py:1060), [read.py:1093](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/stages/read.py:1093)

2. S7 신설 배제가 진짜 수치를 삼킵니다.

   - `each column 5 mm wide…` → 값 `[]`, `column 5`를 좌표로 배제.
   - `a row 60 mm in length` → 값 `[]`, `row 60`을 좌표로 배제.
   - `FIG. 3 and 4.0 mm…` → 값 `[]`, `FIG. 3 and 4` 전체를 도면번호로 배제.
   - 원인은 `row-column-coordinate`가 정수 뒤 단위를 막지 않고, `figure-or-table-number-list`가 소수점 뒤 숫자를 막지 않는 패턴입니다. [reader-rules.yaml:1189](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/reader-rules.yaml:1189), [reader-rules.yaml:1228](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/reader-rules.yaml:1228)
   - 생산 `value.harvest-parity`도 같은 수확기를 정답 생성에 다시 쓰므로 이 손실을 스스로 발견하지 못합니다. [derivation.py:570](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/lib/derivation.py:570)

## 샌드박스 3검증 실출력

```text
/home/laptop/projects/workspaces/pd-audit-m18/D
path=/home/laptop/projects/workspaces/pd-audit-m18/D
pin=2eb30de81f0068a646820eadc1459af8ae1e84dd
order=M18-P11
disposable=true
2eb30de81f0068a646820eadc1459af8ae1e84dd
```

경로·핀·`order/disposable` 모두 일치했고, 직후 `git status --porcelain` 출력은 없었습니다.

## M-A~M-F 변조표

| 변조 | 판정 | 탐지자(규칙 ID) | 기준선 출력 | 변조 후 출력 |
|---|---|---|---|---|
| M-A 절차 본문만 변경 | DETECTED | `LaneStaleResponseError`; `_dispatch` 거부 행 | 지문 `a7f2c5dd…`, 정상 소비, `digest_ok=true` | 요청 필드는 동일하고 구 규격 해시도 `6b30ad26…`로 동일. 신 지문 `75db6c60…`; 예외 발생, `rejected=true`, `digest_ok=false`, 옛 반향 `a7f2c5dd…` 기록 |
| M-B 지문 행만 `000…000` 위조 | DETECTED—파일 단독 수동 재계산 | 문서화된 `grep -v '^| 입력 지문 |' … \| sha256sum` | 선언·재계산 모두 `a7f2c5dd…` → MATCH | 선언 `000…000`, 재계산 `a7f2c5dd…` → MISMATCH |
| M-C 소비 후 `request.md` 교체 | DETECTED—로그↔파일 대조 | `request_digest`와 현재 `sha256(request.md)` | 둘 다 `5e540f36…` | 로그 `5e540f36…`, 현재 파일 `31a0750d…` → MISMATCH |
| M-D 키 삭제 | DETECTED | `lane-log.request-file-digest` | `pass checked=5 violations=0 exempt=0` | `fail checked=5 violations=1`; “요청 파일 지문 칸 없음” |
| M-D 값만 `ffff…ffff`로 위조 | **NOT DETECTED** | 없음 | `pass checked=5 violations=0` | 그대로 `pass checked=5 violations=0 exempt=0` |
| M-E 실제 파일 어댑터 행을 `null` 위장 | **NOT DETECTED** | 없음; 제외 계수만 가시화 | 실제 파일·로그 SHA 모두 `ce617ea3…`; `pass`, `exempt=0` | 요청 파일은 그대로 존재하지만 로그 `null`; `pass`, `violations=0`, `request_digest_exempt=1` |
| M-F 정직한 왕복 | PASS | 정상 `_dispatch`·`read.lane-log-shape` | `FileLaneAdapter`, 5행, `pass`, `exempt=0` | 공식 레인 도구도 정상·낡은 응답·사후 교체·절차 변조 4종 전부 기대 일치 |

S4의 본문 결속은 [contract.py:188](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/lanes/contract.py:188)에서 렌더 본문으로 계산되고, 절차 본문은 [contract.py:358](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/lanes/contract.py:358)에 인라인됩니다. 반향 불일치는 payload 검사 전에 거부됩니다. [contract.py:460](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/lanes/contract.py:460), [read.py:225](/home/laptop/projects/workspaces/pd-audit-m18/D/engine/stages/read.py:225)

## 핵심 회귀표

| 변조 | 판정 | 탐지자(규칙 ID) | 기준선 출력 | 변조 후 출력 |
|---|---|---|---|---|
| R1 `single→unclassified`, 구조 표지 없음 | DETECTED | `parse.unclassified-not-an-escape` | `pass checked=6 violations=0` | `fail checked=5 violations=1`, locus `CL-2.dependency_type` |
| R1 `unresponsive to` | DETECTED—조건부로 오인 안 함 | 같은 규칙 | 기본 표지 `[]` | markers `[]`; 회피 가드가 실패 |
| R1 `in response to` | 정직한 사용 PASS | 조건부 앵커 | — | markers `["조건부"]`; `pass checked=5 violations=0` |
| R2 수치 삭제 | DETECTED | `value.harvest-parity` | `pass checked=24 violations=0` | `[누락]`, locus `harvest:[0048][17,24)` |
| R2 수치 변조 | DETECTED | `value.harvest-parity` 등 | 동일 | `[변조]` + `value.quoted-span` + `value.type-agrees`, 총 3건 |
| R2 수치 추가 | DETECTED | `value.harvest-parity` | 동일 | `[추가]`, locus `M44.value_raw` |
| R3 payload 변경 | DETECTED | `lifecycle.payload-frozen` | ID `pass/89`, payload `pass/46` | ID 통과, payload 위반 1건 `M1` |
| R3 `retracted→active` | DETECTED | `lifecycle.one-way` | 동일 | `retracted → active`, 기대 `전이 없음` |
| R3 순환 `M23→M44→M23` | DETECTED | `supersession.acyclic` | 동일 | `M23`, `M44` 출발점에서 위반 2건 |
| R4 발주 예시 3종 | PASS | 기존 golden | `7 passed` | `FIG. 3 and 4 mm`→`4 mm`; `between 1 and 2`→range; `60 columns/rows`→둘 다 보존 |
| R4 자체 반례 3종 | **FAIL—진짜 값 소실** | 생산 탐지자 없음; 확장 golden이 증명 | 기존 `7 passed` | 반례 추가 후 `3 failed, 7 passed`; 세 경우 모두 실제 값 `[]` |

R1 가드는 [dependency_parse.py:129](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/lib/dependency_parse.py:129), 교정 앵커는 [reader-rules.yaml:315](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/reader-rules.yaml:315)에 있습니다. R2의 3분류는 [derivation.py:577](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/lib/derivation.py:577), R3의 검사는 [freeze_integrity.py:134](/home/laptop/projects/workspaces/pd-audit-m18/D/reader/lib/freeze_integrity.py:134)에 구현돼 있습니다. R4 golden은 실제 수확기 출력과 기대값을 대조합니다. [test_m17_rules.py:540](/home/laptop/projects/workspaces/pd-audit-m18/D/tests/test_m17_rules.py:540)

## 최종 기준선

```text
check_validator_enforcement.py:
RESULT: PASS — 기준선 12/12 · 변조본 42/42 · 하한 충족

check_spec_refs.py:
K1–K8 전부 PASS, RESULT: PASS

python -O check_spec_refs.py:
K1–K8 전부 PASS, RESULT: PASS

check_lane_binding.py:
RESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 4종 전건 일치

pytest:
441 passed in 99.32s (0:01:39)

git diff --exit-code:
(출력 없음, exit 0)

git status --short:
(출력 없음)

git status --porcelain:
(출력 없음)
```

## 복원 규율·환경 편차

요구된 `git checkout -- <path>`는 모든 추적 파일 변조 뒤 먼저 시도했지만, 실제 환경의 `.git`은 발주 설명과 달리 쓰기 불가였습니다.

```text
fatal: Unable to create '/home/laptop/projects/workspaces/pd-audit-m18/D/.git/index.lock': Read-only file system
```

따라서 각 변조를 정확한 역패치로 복원하고 매번 `git diff --exit-code=0`을 확인했습니다. 최종 작업 트리는 완전히 깨끗합니다.

OUT-OF-SCOPE: 보관된 `runs/**/request.md` 일부는 신 S4 규칙으로 `NO-DIGEST-ROW` 또는 `MISMATCH`지만, S4는 기존 런에 소급하지 않는다고 명시합니다. [ruling S4:93](/home/laptop/projects/workspaces/pd-audit-m18/D/docs/decisions/ruling-20260819-03-S1-S9.md:93) 신규 범위 밖 결함으로 세지 않았습니다.

---

## 전달자 코멘트 (레인이 적은 것 — **Sol 판정 아님**)

**① D 의뢰의 마커 3검증 실출력**(쓰기 모드 진입 전, 총괄 레인이 실행).

```text
---MARKER---
path=/home/laptop/projects/workspaces/pd-audit-m18/D
pin=2eb30de81f0068a646820eadc1459af8ae1e84dd
order=M18-P11
disposable=true
---PIN---   (git rev-parse HEAD)
2eb30de81f0068a646820eadc1459af8ae1e84dd
---STATUS--- (git status --porcelain)
(출력 없음)
```

종료 시에도 `git status --porcelain` 이 빈 출력이고 핀이 불변이었다.

**② 환경 편차 1건 — 사본의 `.git` 은 쓰기 가능했으나 샌드박스가 막았다.**

발주는 사본의 `.git` 을 쓰기 가능하게 준비했고(직전 라운드 처방), 총괄 레인의 preflight 도 `test -w .git` → OK · `touch .git/.wtest` → **성공**으로 확인했다. 그런데 Sol 은 여전히 `.git/index.lock: Read-only file system` 을 맞았다.

원인은 파일 권한이 아니라 **codex `workspace-write` 샌드박스가 `.git` 을 기본적으로 쓰기 대상에서 제외**하는 것으로 보인다 — 호스트 파일시스템은 쓰기 가능한데 샌드박스 계층이 차단한다. **즉 직전 라운드의 "읽기 전용 `.git`" 사고는 사본 권한 조정으로 해소되지 않는다.** 다음 라운드에 `git checkout` 복원을 쓰게 하려면 codex 쪽 writable-root 에 `.git` 을 명시 포함해야 한다(`-c sandbox_workspace_write.writable_roots=[…]` 계열).

이번 회차에는 Sol 이 **역패치 복원**으로 우회했고 매 변조마다 `git diff --exit-code=0` 을 확인했으며, 최종 트리 청결이 총괄 레인 실측으로도 확인되었으므로 **결과의 무결성은 손상되지 않았다.** 이 사실을 적는 이유는 재정 S5 의 사본 규격 ②(`.git` 쓰기 가능)가 **발주자만으로는 충족될 수 없다**는 것이 이번에 드러났기 때문이다 — 규격의 절반이 감수 레인 쪽 호출 인자에 걸려 있다.

**③ 앵커 실재 확인**(총괄 레인이 독립으로 실행한 것만 적는다).

- `engine/stages/read.py:1051/1060/1093` — 실재. 각각 키 부재만 실패 · `None` 무조건 제외 · `request_digest_exempt` 산출. **D 의 NEW BLOCKER 1(값 검증 부재·null 무조건 제외)은 코드로 확인된다.**
- `reader/reader-rules.yaml:1189/1228`(신설 배제 2종 정의) · `derivation.py:570/577` · `dependency_parse.py:129` · `freeze_integrity.py:134` · `test_m17_rules.py:540` — 전건 실재.
- `engine/lanes/contract.py:188`(지문 = 렌더 본문의 sha256, 지문 행만 제외) · `:358`(절차 본문 인라인) — 실재. **S4 본문 결속 PASS 근거 확인.**
- C′-1 의 두 BLOCKER 를 레인이 패턴만 떼어 독립 재현: `FIG. 3 and 4.5 mm of clearance remains` → `FIG. 3 and 4` 매치(소수부 삼킴) · `a column 12 mm wide carries current` → `column 12` 매치(단위 앞 정수 삼킴). 대조군 `the column 12.5 mm wide` · `FIG. 3 and 4 mm` 는 무매치. **Sol 서술과 일치.**
