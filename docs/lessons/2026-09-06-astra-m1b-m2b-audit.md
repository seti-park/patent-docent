# 독립 감수 원문 — M1b 설계 도전(gpt-6-astra high) · PD-M2b 합본 감사 발주문 v1 · 판정 REVISE(HIGH 1 · MED 6 · LOW 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `7837c70ffb09d37e8b4db22c14c95697749ecc5482eb5b5c49ac7141ad14da03` · 10912 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-m2b-audit/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 03:36:07 → 03:4x · **USAGE = input 832,675(cached 739,712) · output 10,475(reasoning 2,558)**. 사본 `~/projects/workspaces/pd-m1b-m2b2`(재핀 detached `f788604` · `bundle/AUDIT-ORDER-round-m2b.md` v1 sha256 `e01b11d1…3c48a`). 대상 = fable xhigh(M9) 합본 감사 발주문 — 두 라운드 병합분(`b0c4fb6` · `1bf24f1`)의 첫 독립 실행 검증을 시키는 문서. 도전자는 M9 격리 사본(`pd-audit-round-m2b` · alternates 없음 · 정본과 공유 inode 0)과 생산 원장 6행도 확인했다.

**판정 = REVISE · 9건 · 기각 0 · 전부 발주자 귀책.** **MX-1 HIGH**: Q2ⓓ 「레인 diff 를 그대로 적용」 — `report-artifacts/*.diff` 여섯은 숫자형 hunk 0 의 축약 참고자료이고 V2 는 후속 수리 전 blob 기준 → M9 가 완성본에서 보호를 직접 제거해 독립 재현. **MX-2 MED**: M2b-1 레인은 변조 diff 미보존(복원 해시만) → 독립 재구성 + diff·명령·해시 보존 요구. **MX-3 MED**: 가짜 생산 자리 monkeypatch 가 세션층(`ledger_guard.production_ledger`)만 가리킴 — 헬퍼는 `engine_paths.shadow_screening_ledger` 를 읽음 → 두 층 같은 가짜 파일에 결속. **MX-4 MED**: Q1ⓕ 의 §4 검사가 `HEAD` 기준이라 청결 사본에서 자기 비교 → 기준판 `3865645` · 대상판 `1bf24f1`. **MX-5 MED**: Q2ⓔ 가 `run_kind` 후속 분기의 존재를 전제 — 실측 소비자 `read.py:1663` · `freeze.py:330 :517` 은 분기 없음 → 유무를 먼저 보고. **MX-6 MED**: `pgrep` allowlist 부재 + 자기매칭(함정 C) → `[p]ytest` 패턴 · allowlist 추가. **MX-7 MED**: 「근거 없는 변경 = 상신」이 ROUTING ⑸ ② 보다 넓음 → 근거 누락·허가 이탈 = FAIL 사유 · 근거 진위 쟁송 = 상신 분리. **MX-8 LOW**: m27 lane 시험 함수 수 「19」 → 15(파라미터 32). **MX-9 LOW**: 자문은 정적 판정이 아니라 축약 규칙의 실행 재현. 나머지 전제(커밋 부모 · 기록 §13·§14 · 좌표 · 호출 6곳 · conftest 두 훅 · 885/909)는 확인.

지적 열거 = MX-1, MX-2, MX-3, MX-4, MX-5, MX-6, MX-7, MX-8, MX-9

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§15**. **전부 수용 → 발주문 v2 → 재도전 없이 감사 발주**(선례 = 재감사 5·6·7 발주문 — M1b REVISE 를 정정 후 곧 발주 · 지적 전부가 발주문 문언·절차이며 도전자가 「고치는 문안 한 줄」을 줬다).

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

마커 3검증과 정본 HEAD는 일치합니다. 아래는 관문을 실행하지 않고 파일·Git 정보를 읽어 얻은 결과입니다.

```text
M1b 사본:
marker_exists=True  path_eq_realpath=True  pin_eq_HEAD=True
order=M1B-m2b-audit-20260906  disposable=true

M9 사본:
marker_exists=True  path_eq_realpath=True  pin_eq_HEAD=True
order=AUDIT-round-m2b-20260906  disposable=true
HEAD=f7886041cc2a83b2ed62316483ffd2d7292d5f8e (detached)
git status --short:
?? .audit-sandbox

정본:
HEAD=f7886041cc2a83b2ed62316483ffd2d7292d5f8e (main)
git status --short: 빈 출력
```

[대상 발주문](/home/laptop/projects/workspaces/pd-m1b-m2b2/bundle/AUDIT-ORDER-round-m2b.md)의 SHA-256은 지정값 `e01b11d16811f35cf18cb9eb06021cf03f1deaed9bf995386d9a91bd59a3c48a`와 같습니다. M9 사본은 실제 `.git` 디렉터리를 가지며 alternates가 없고, 객체 파일 3,008개에서 정본과 공유하는 inode는 0개였습니다. 정본·M9 사본의 생산 원장은 모두 **6행**, 지정 SHA-256 `e2350e0d20d138a797153048a411cfd95c324bc2294fc977b061a61b1bb75df2`입니다.

**판정은 REVISE입니다.** 가장 먼저 끊기는 곳은 Q2ⓓ의 “레인 diff를 그대로 적용”입니다.

**MX-1 · HIGH · 발주문 L16·L30(Q2ⓓ): 제공된 diff는 적용 가능한 패치가 아니다.**

- 근거 실출력: `report-artifacts/*.diff` **6개 모두 숫자형 unified hunk 0개**. [V2 파일](/home/laptop/projects/workspaces/pd-lanes/sol-coder-round-m2b2/report-artifacts/V2-guard-removed.diff:3)은 `@@ run(): immediately after _engine_pin`, `raise StageError(...)`를 사용한다. V5·V6·V7도 함수명 헤더와 축약 문자열이다.
- V2의 기준 blob은 `e69b0a7f…`지만 현재 `source.py`는 `9d28d845…`이다. V2 L8–9는 후속 수리 전의 무조건 `partial` 조회이며, 현재 코드는 `source.py:558`의 조건부 조회다.
- 검증 경로: diff 원문·hunk 형식 확인 → `git hash-object engine/stages/source.py` → 현재 가드 대조. **“그대로 적용”은 불가능하고, 그대로 복원한 과거 변조라는 주장도 성립하지 않는다.**
- 고치는 문안 한 줄: **“기존 `.diff`는 축약 참고자료이며, M9는 `f788604` 완성본에서 V2·V5·V6·V7의 지정 보호만 각각 제거하고 실제 unified diff·기준/변조/복원 해시를 보존해 독립 재현한다.”**

**MX-2 · MED · 발주문 L29(Q1ⓑ): M2b-1의 복원 해시만으로 변조 내용을 검증할 수 없다.**

- 근거 실출력: M2b-1 레인에는 `report-artifacts/`와 `.diff`가 없다. [final.txt](/home/laptop/projects/workspaces/pd-lanes/sol-coder-round-m2b1/final.txt)는 복원 해시 `226f82e8730fcde730d988fa75afafbb7bbdbeca`, `b0313450d3b85acb617921c240fd305f7fa3d0b2`를 보고하며 현재 파일과 일치한다.
- 그러나 이는 **복원된 바이트**만 확인한다. 실제로 어느 보호만 제거했는지는 확인하지 못한다. 원 발주문 §2 L96·L121은 변조 diff 보존까지 요구했다. 표를 보고 독립 재구성하는 일은 가능하지만 레인 변조와 동일하다고 인증할 수는 없다.
- 검증 경로: 레인 파일 목록 → 보고서 해시 → `git hash-object` → 원 발주문 §2.
- 고치는 문안 한 줄: **“R 계열은 레인 diff 미보존을 기록하고 §2 표로 독립 재구성하되, 각 변조의 실제 diff·실행 명령·관측/시험 판정·세 해시를 최종 응답에 남긴다.”**

**MX-3 · MED · 발주문 L29(Q1ⓐ): 가짜 생산 자리의 patch 대상이 한 층만 가리킨다.**

- 근거: [ledger_guard.py:91](/home/laptop/projects/workspaces/pd-m1b-m2b2/tests/ledger_guard.py:91)의 헬퍼는 `engine_paths.shadow_screening_ledger()`를 호출한다. [conftest.py:44](/home/laptop/projects/workspaces/pd-m1b-m2b2/tests/conftest.py:44)의 세션 거부층은 `ledger_guard.production_ledger()`를 호출한다.
- 발주문이 지정한 후자만 바꾸면 헬퍼의 생산 지문 대상은 가짜로 바뀌지 않는다. 기존 시험도 헬퍼용은 `test_m2_read.py:1971·2012·2056`, 세션용은 `:2077`에서 서로 다르게 patch한다. “실제 생산 원장 금지” 문언과 해시 측정은 있지만, 이 잘못된 배치를 대신 막아주지는 않는다.
- 검증 경로: 두 보호층의 생산 경로 조회 → 기존 음성 시험의 monkeypatch 대조.
- 고치는 문안 한 줄: **“헬퍼용 `engine_paths.shadow_screening_ledger`와 세션용 `ledger_guard.production_ledger`를 같은 가짜 파일에 결속하고, 실제 호출 대상·symlink 종착지도 홈 basetemp 아래임을 확인한 뒤 프로브를 실행한다.”**

**MX-4 · MED · 발주문 L29(Q1ⓕ): 참조한 §4의 `HEAD` 기준은 병합 후 사본에서 작동하지 않는다.**

- 원 발주문 §4 L128–133은 구현 중 작업 트리용으로 `git diff … HEAD`와 `git show HEAD:engine/stages/read.py`를 사용한다. 현재 청결한 `f788604`에서 그대로 재실행하면 diff는 없고 AST 비교는 자기 비교가 된다.
- 독립 정적 확인 결과는 다음과 같다.

```text
git diff --numstat 3865645 1bf24f1 -- engine/stages/read.py
7  0  engine/stages/read.py

@@ -2264,0 +2265,7 @@
read.py AST-EQUAL(docstring 제외)=True
```

- 검증 경로: 참조 스크립트의 기준판 → 부모/대상 커밋 간 diff·AST 대조.
- 고치는 문안 한 줄: **“Q1ⓕ 세 검사는 기준판 `3865645`, 대상판 `1bf24f1`로 실행하고, 대상 파일이 감사 HEAD의 파일과 동일함도 확인한다.”**

**MX-5 · MED · 발주문 L30(Q2ⓔ): `run_kind` 후속 분기를 존재하는 것으로 전제한다.**

- 근거 실출력: `rg -n 'run_kind|partial_until' reader studio tools engine/stages/read.py engine/stages/freeze.py`는 **빈 출력**이다.
- 실제 YAML 소비자는 [read.py:1663](/home/laptop/projects/workspaces/pd-m1b-m2b2/engine/stages/read.py:1663), [freeze.py:330](/home/laptop/projects/workspaces/pd-m1b-m2b2/engine/stages/freeze.py:330), [freeze.py:517](/home/laptop/projects/workspaces/pd-m1b-m2b2/engine/stages/freeze.py:517)이다. 각각 런 신원·동결 메타데이터를 처리하며 `run_kind`로 분기하지 않는다.
- 따라서 현재 답은 **“후속 소비·분기 없음”**이다. 이를 rehearsal/publish 중 하나로 분류하게 하면 사실과 다른 답을 유도한다. G-12의 강제 부재 서술은 이 실물과 맞는다.
- 고치는 문안 한 줄: **“`read.py:1663`, `freeze.py:330·517` 등 YAML 소비자를 추적해 `run_kind`·`partial_until`의 소비/분기 유무를 먼저 보고하고, 존재하는 경우에만 세 종류의 처리 차이를 비교한다.”**

**MX-6 · MED · 발주문 L3·L15: pytest 대기 명령이 자기매칭과 allowlist에 걸린다.**

- `pgrep`는 명시된 allowlist에 없다. `bash -c` 우회는 가능하지만 사용법이 명시되지 않았다.
- 읽기 전용 프로세스 조회 실출력:

```text
wrapper-self-match rows=3
self-match: 4 bash -c pgrep -af pytest :
```

- 즉 반환값이나 행 존재만 보고 기다리면 자신의 조회 래퍼 때문에 대기가 끝나지 않을 수 있다. [LANE-RUNTIME 함정 C](/home/laptop/.claude/agents/LANE-RUNTIME.md:69)가 같은 현상을 기록한다.
- 검증 경로: allowlist 대조 → 프로세스 목록 조회 → 래퍼 명령행 확인.
- 고치는 문안 한 줄: **“`bash -c` 안의 `pgrep -af '[p]ytest'`로 조회하고 조회 래퍼·자기 PID·조상을 제외한 실제 실행만 대기 대상으로 삼으며, 조회 실패를 실행 부재로 취급하지 않는다.”**

**MX-7 · MED · 발주문 L30·L33·L39: 근거 부재와 근거 진위 쟁송의 라우팅이 합쳐졌다.**

- [ROUTING §5 ⑸ ②](/home/laptop/.claude/agents/ROUTING.md:144)의 실제 문언은 **“근거의 참·거짓을 다투는 것은 REVISE 사유가 아니라 상신 사유다.”**
- 발주문의 “근거 없는 변경 하나라도 = 상신”은 적용 범위가 더 넓다. 근거 열 누락, 명백한 허가 범위 이탈, 제시된 근거의 진위 쟁송을 구별해야 한다. **FAIL과 상신을 함께 기록하는 것 자체는 모순이 아니다.**
- 검증 경로: 해당 조항 원문과 Q2ⓐ·PASS 조건의 직접 대조.
- 고치는 문안 한 줄: **“근거 누락·허가 범위 이탈은 좌표와 함께 FAIL 사유로 기록하고, 근거의 참·거짓에 관한 쟁송은 ⑸②에 따라 Owner 상신으로 분리하며 재정 전 PASS하지 않는다.”**

**MX-8 · LOW · 발주문 L23: m27 lane 시험 함수 수가 틀렸다.**

- AST 정적 집계 실출력:

```text
test_m27_run_kind_vocabulary.py: test_functions=10  cases=10
test_m27_lane_id_vocabulary.py:  test_functions=15  cases=32
```

- 검증 경로: 파일 AST의 `test_` 함수와 literal parametrization 집계. pytest 수집은 하지 않았다. “19 함수”는 사실 오기다.
- 고치는 문안 한 줄: **“`test_m27_lane_id_vocabulary.py`는 15개 시험 함수·파라미터 전개 32건이다.”**

**MX-9 · LOW · 발주문 L9: 자문을 정적 판정으로만 설명한 것은 원문과 다르다.**

- [자문 보존본 L9](/home/laptop/projects/workspaces/pd-m1b-m2b2/docs/lessons/2026-09-06-astra-advice-m2b-gate-and-values.md:9)와 D-02 §9는 **Python 3.13.5에서 축약 규칙을 구현해 반례를 실행 재현했다**고 기록한다. 봉투 `REPLY.md` 본문은 보존본에 그대로 포함되어 있다.
- 검증 경로: 자문 원문·봉투·처분 기록 대조. 완성된 합본 산출물에 대한 “첫 독립 실행 감사”라는 핵심 설명은 유지할 수 있다.
- 고치는 문안 한 줄: **“M1b는 읽기 전용 정적 도전이고 자문은 축약 규칙의 실행 재현이며, 완성된 합본 리포의 독립 실행 검증은 이번이 처음이다.”**

나머지 주요 전제는 확인됩니다. 커밋 부모 `b0c4fb6 ← 4dfe341`, `1bf24f1 ← 3865645`, 기록 §13·§14, `read.py:75·1536·2253` 부근, `lane_file` 외부 호출 6곳, conftest 두 훅이 실재합니다. M1b 원문 8건·자문·발주문 버전 경로도 존재합니다. **885/909 두 모드 수치는 기존 재현 로그와 일치**하며, 현재 합본 전체 plain의 기대값은 909입니다.

Q2ⓐ의 전수표는 부모/대상 diff와 원 발주문 §0′을 이용해 작성할 수 있습니다. `READ_RUNS`·`LANE_TASKS`는 계약 정본과 상등하고 다리 시험도 실제 상등을 검사합니다. plain 전체 1모드와 의심 시험 한정 `-O`, 홈 basetemp, `/tmp` 폴백 금지, 종료 청결 조건은 서로 양립합니다. LOW 열거와 우회표 `[미검증]` 금지도 명시되어 있습니다.

pytest·관문·변조는 실행하지 않았으며 파일 쓰기와 `/tmp` 접근도 하지 않았습니다. 종료 시 정본 HEAD·상태, 대상 발주문 해시, 양쪽 생산 원장 해시는 시작값 그대로입니다.

VERDICT: REVISE