# 독립 감수 원문 — M1b 설계 도전 29차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v31(연역 명세 · 28차 반영) · 판정 REVISE(HIGH 4 · MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `6394ad6ea0d79b4734f6453622a93d8f7837ea82f250e9f3d78d7e4a78b62f6e` · 19359 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v29/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = Monitor STATUS EXIT= + FINAL 바이트(04:21 기동 · 04:4x 종료 · USAGE input 4,939,300(cached 4,524,416) · output 22,580). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `ed011a1` · 마커 3항 일치 · 메모 v31 sha256 `4d2fde27…` · v1~v30 + 스크립트 9종 + 회귀표 v10(113) + 자문 1~3회차 + 재정 T42·T43 + SPEC v29 동봉). Owner 육성 「29차: A」(채팅 · D-02 추기 35) 로 기동. 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 29회」와 **「재조립 방식 자체의 신뢰 입력·격리·처분 합성을 다시 REVISE — Owner 재정 상신 대상 · 자문 3회차의 도출 방식은 유지할 수 있다」** 명기. **심사 대상 ① 도출의 완전성 = 충족(처음)** · ②~⑤ 미충족 · 도출 누락 0 · 새 보증 요구 0 · **갈래 전부 ⑴** · ⓔ 문언 수정 닫힘 · MY~NY 102 closed 유지 · **NZ-1·NZ-2 closed · NZ-3·4·5 partially**(합계 closed 104 · partially 3 · open 0) · T1·T2·T4 확인 · P2 정규화·환경 동치 확인 · P3·P4 확인 · 기준 런 메모리 재현 일치 · 도면 20 전량 해시 일치 · F 파생 C 는 12건이며 부적격 6(C08·C09·C10·C29·C69·C83) / 재실측 6(C74~C77·C84·C85)으로 갈린다(「전부 탐지 증거 아님」 일괄 설명 정정).

**판정 = REVISE · 5건(HIGH 4 · MED 1) · 기각 0 · 발주자 귀책.** **OA-1 HIGH · P1·P6**: T43 선판별이 영수증을 「이 런의 실행 기록」으로 결속하기 **전**에 선다 — `load_receipts` 가 영수증 `run_id` 를 대상 런과 대조하지 않고, 법 HEAD·파일 지문·`pre.run_yaml` 대조는 대조기의 선판별 뒤 → R0 대상에 R2 영수증(FOREIGN_RUN) · R2 법 HEAD 와 다른 run.yaml 지문(FOREIGN_LAW) 둘 다 부적격이어야 하는데 R0 의 「재실측」 근거가 됨. **OA-2 HIGH · P6·P7**: `retire` 가 결함 런 폴더를 보존 없이 `rmtree` — 상류 T43 「결함 런 폴더·영수증은 증거로 보존」 위반 · S06 도 `run_gone=True` 를 성공 조건으로 삼음 · `retest_history` 에 예외 종류·재정 좌표가 구조화되지 않음. **OA-3 MED · P7**: 처분 분류가 끝까지 유지되지 않음 — 법 스키마 읽기 PermissionError 가 공용 `read_bytes` 의 기본 `die()`(부적격)로 끝나 「검수 불능」에 도달 못 함 · 반대로 완주 판정서가 JSON 배열 `[]` 이면 `_halt4_signature` 가 AttributeError → 최상위 경계 「검수 불능」(자료 형태 위반인데 표에서 빠짐). **OA-4 HIGH · T3**: 봉인 목록과 소비 입력의 집합이 다름 — 봉인기는 파일 이름에 `-r0-` 가 든 발주 파일만, 소비기(`dispatch_records`)는 `dispatch/*.json` 전부를 본문 run_id 로 → 봉인 뒤 `extra.json` 추가가 대조를 통과하고 소비됨 · `--receipts evidence/alternate` 를 주면 봉인은 `evidence/calls` 를 대조하고 소비는 alternate 에서 → 봉인 밖 영수증 근거 재실측 · `manifest_verify` 가 목록의 `../outside.txt` 를 경계 없이 읽음. **OA-5 HIGH · P5**: 쓰기 자리 열거가 **Python import 캐시**를 빠뜨림 — 실행파일에 bytecode 쓰기 금지 설정이 없고 회귀 하네스만 `PYTHONDONTWRITEBYTECODE=1` 을 넣어 시험 환경의 보호가 운영 기동에 이어지지 않음(지표기 진입에서 bundle `__pycache__` 쓰기 요청 3건 관측 · sandbox 준비 전) · 「하위 호출 = `law_status` 하나」도 부정확(영수증·러너 경로 해석의 git 조회).

**처분 = 전부 수용(공학 · v32) — 갈래 전부 ⑴ · 새 보증 요구 0 · 「방식 자체 재REVISE → Owner 상신」 약속대로 30차 기동 전에 채팅으로 묻되, 매 회차 같은 질문이 반복되므로 상설 규약(도출 누락 0 · 새 보증 요구 0 · 갈래 ⑴ 만이면 총괄 기동 · 그 밖은 상신)을 함께 상신한다.** OA-1 = 지표기·대조기 모두 영수증 적재 직후 **결속 검사**(영수증 `run_id` = 대상 런 · 법 HEAD = 선등록 핀 = worktree HEAD · 법 파일 지문 = 현재 worktree · `pre.run_yaml` = 현재 run.yaml 지문 · attempt 일치)를 **T43 선판별보다 앞에** · `load_receipts(run_id=)` · 회귀 C88(다른 런 영수증 → 부적격) · C89(다른 법 HEAD → 부적격). OA-2 = `retire` 가 런 폴더 전체를 `retired/…/run/` 으로 **먼저 이동·보존 확인** 뒤에만 새 작업장 · attempts 원본 사본 · `retest_history` 항목에 `io_faults[{call, exc_type, exc_msg}]` · `reason` · `ruling` 구조화 · S06 = `run_preserved` 확인. OA-3 = `read_bytes`·`parse_json` 에 `kind` 인자 — 법·스키마·규칙·계약 적재 경로는 「검수 불능」 · 자료 파일은 「부적격」 · `_halt4_signature`·`_halt4_bound` 가 비객체 JSON 을 None 으로(형태 위반은 뒤 검사가 부적격으로) · 회귀 C90(완주 판정서 `[]` → 부적격) · S08(법 스키마 읽기 실패 → 검수 불능). OA-4 = 봉인·대조·소비가 **같은 함수 `evidence_files(evidence, run, run_id)`** 로 발주 파일을 본문 run_id 로 고르고 · `manifest_verify` 목록 경로는 어휘(`calls/…`·`dispatch/…`·고정 이름)와 realpath 가 evidence 안임을 읽기 전에 검사 · 지표기는 `--receipts` 의 basename 이 `calls` 이고 부모가 봉인 디렉터리임을 요구(exit 3) · 회귀 C91(봉인 뒤 `dispatch/extra.json` → 부적격 「MANIFEST」) · C92(MANIFEST 에 `../outside` → 부적격) · S09(`--receipts evidence/alternate` → exit 3). OA-5 = 다섯 스크립트 첫 줄 `import sys; sys.dont_write_bytecode = True`(import 전) · 메모 §5′.3 에 런타임 부작용(bytecode 캐시 · 하위 git 조회 목록) 행 · S10(플래그 없는 환경에서 지표기 기동 → `__pycache__` 생성 0). 정정 = F 파생 C 12건의 두 갈래 표 · §5′.3 하위 호출 목록. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 36**. 다음 = **v32(코드 + 메모) → 회귀 전건 → Owner 채팅 상신(30차 기동 + 상설 규약) → 30차(`OB-*`)**.

지적 열거 = OA-1, OA-2, OA-3, OA-4, OA-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 29회)

**재조립 방식 자체의 신뢰 입력·격리·처분 합성을 다시 REVISE한다. 총괄의 Owner 재정 상신 대상이다.** 자문 3회차의 도출 방식은 유지할 수 있으나, 아래 연결 5건이 남아 실측 착수 조건은 충족하지 못한다.

지적은 **HIGH 4·MED 1, 전부 갈래 ⑴**이다. 도출 누락과 새 보증 요구는 확인하지 못했다. 마커의 path·pin·order 및 disposable, HEAD `ed011a175c68d21ffb9c0e5de0a31498a0b90e10`을 확인했고, 메모와 제시된 실행파일 해시는 모두 일치했다. 모든 검증은 읽기 또는 메모리 대역으로 수행했다.

**지적 목록**

**OA-1 · HIGH · ⑴ P1·P6 위반 — 선판별 전에 영수증을 ‘이 런의 실행 기록’으로 결속하지 않는다.**

좌표: 메모 §5′.5 P1·P6, §5′.8; [metrics:370](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:370), [receipts:load_receipts](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:216), [replay:155](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:155).

`load_receipts()`는 형식·번호·attempt·IO 플래그의 일부 정합을 검사하지만, 영수증 `run_id`를 대상 런과 대조하지 않는다. 영수증의 법 HEAD·파일 지문과 `pre.run_yaml` 대조는 대조기의 **T43 선판별 뒤**에 있다.

실제 `metrics()`·`replay()`에 메모리 파일을 공급했다. 파일 읽기와 worktree 조회는 대역이며, 영수증 적재·MANIFEST 대조·선판별 본문은 실제 함수다. 봉인 전 혼입이라는 회귀 C와 같은 조건에서:

```text
FOREIGN_RUN exit 4 … 처분=재실측
FOREIGN_RUN REPLAY io-fault replayed 0
FOREIGN_LAW exit 4 … 처분=재실측
FOREIGN_LAW REPLAY io-fault replayed 0
SANDBOX_CALLS 0
```

첫 경우는 R0 대상에 R2 `run_id`의 영수증, 둘째는 R2 법 HEAD와 다른 `run.yaml` 지문의 영수증이다. 둘 다 **자료 부적격**이어야 하지만 R0의 재실측 근거가 된다.

끊긴 연결은 **“봉인된 영수증 → 이 런의 결함 기록”**이다. P6의 조기 도달성은 고쳐졌지만, T43에서도 유지해야 하는 P1 식별이 그 앞에 서지 않았다.

**수정 문안:** “전 영수증의 run_id·attempt·법 핀/지문·run.yaml 결속을 대상 런과 확인한 직후 T43을 선판별하며, 이 결속에는 산출물 파싱·재실행 성공을 요구하지 않는다.”

**OA-2 · HIGH · ⑴ P6·P7 위반 — `retire`가 결함 런 폴더를 보존하지 않고 삭제한다.**

좌표: T43 §1①, 메모 §2·§6⑵·§8ⓣ; [drive:cmd_retire](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:383), [삭제:417](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:417), 회귀 S06.

상류는 **“결함 런 폴더·영수증은 증거로 보존”**하도록 한다. 그러나 `cmd_retire()`가 옮기는 것은 `evidence_files()`의 외부 증거와 배치 파일이다. 런 폴더의 `run.yaml`·원천·요청·응답·부분 산출물을 보존하는 단계 없이 `shutil.rmtree(run_root)`를 호출한다.

실제 함수에서 종결 가드를 비종결로 대입하고 모든 쓰기·이동·삭제를 메모리 대역으로 관측했다.

```text
RETIRE_EXIT 0
RETIRE_MOVED ['calls/r0-001.json', 'MANIFEST-sha256-r0.txt']
RUN_BYTES_PRESERVED False False
```

S06도 보존본의 존재를 검사하지 않고 **`run_gone=True`**를 성공 조건으로 삼는다. 영수증의 해시는 삭제한 원본 바이트를 대신하지 못한다.

또한 `retest_history`에는 `io_fault_calls`만 있고 예외 종류·재정 좌표가 구조화되지 않는다. §2가 요구하는 연결 이력 전부를 “그대로” 출력한다는 P7 설명도 과하다.

**수정 문안:** “retire는 결함 런 폴더 전체와 해당 시도의 증거·attempts 원본을 함께 보존하고 보존 완료를 확인한 뒤 새 작업장을 열며, 호출별 예외 종류·승인 좌표를 연결 이력에 남긴다.”

**OA-3 · MED · ⑴ P7 위반 — 처분 필드는 생겼지만 자료 오류와 환경 오류의 분류가 끝까지 유지되지 않는다.**

좌표: 메모 §5′.4·§8ⓢ; [metrics:read_bytes·validators](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:90), [replay:_halt4_signature](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:93), metrics 최상위 예외 경계.

실제 `validators()`의 법 스키마 읽기에 `PermissionError`를 공급하면:

```text
SCHEMA_PERMISSION exit 4
[t40_metrics] 처분=부적격 · convergence.schema.json 읽기 실패: PermissionError(...)
```

법·계약 적재 실패는 메모가 지정한 **검수 불능**이다. 공용 `read_bytes()`의 기본 `die()`가 먼저 종료하여 환경 경계까지 도달하지 않는다.

반대 방향도 있다. 완주 판정서가 유효한 JSON 배열 `[]`이면 `_halt4_signature()`는 `c.get()`에서 `AttributeError`를 낸다. 이는 최상위 경계에서 **검수 불능**으로 분류된다. 자료 형태 위반인데 결과 표에서 빠지는 경로다.

끊긴 연결은 **“예외 발생 위치 → 정해진 다음 절차”**다. 접두 문자열만으로 이 분류가 보증되지는 않는다.

**수정 문안:** “자료 파싱·형태 위반과 법/환경 접근 실패를 발생 경계에서 구별하고, 보조 판별 함수도 자료 형태 위반을 환경 예외로 내보내지 않는다.”

**OA-4 · HIGH · ⑴ T3 미충족 — 봉인 목록과 실제 소비 입력의 집합이 다르다.**

좌표: 메모 §5′.1 T3·§5′.2·§5′.7ⓔ; [receipts:evidence_files·manifest_verify](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:254), [metrics:dispatch_records](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:290), metrics 영수증 적재 블록.

봉인기는 발주 파일 이름에 `-r0-` 같은 문자열이 들어간 경우만 수집한다. 소비기는 `dispatch/*.json` 전부를 읽고 **본문의 run_id**로 선택한다. 따라서 봉인 뒤 같은 `evidence/dispatch/`에 `extra.json`을 추가하면:

```text
UNSEALED_DISPATCH before [] after []
consumed {'read-a/decompose/batch-0': ['aaaaaaaa…']}
listed ['calls/r0-001.json']
```

MANIFEST는 그대로이며, 추가 파일이 봉인 대조를 통과한 뒤 발주 증거로 소비된다. 이는 ⓔ의 “MANIFEST까지 모두 함께 바뀐 자료”가 아니다.

영수증 경로에도 같은 분리가 있다. `--receipts`를 `evidence/alternate`로 주면 그곳을 읽으면서 봉인은 여전히 `evidence/calls`를 대조한다. 실제 함수 실행에서 **MANIFEST 문제 목록 `[]` + 봉인 밖 영수증에 근거한 재실측**을 확인했다.

입력 범위의 추가 단절도 있다. `manifest_verify()`는 목록의 `../outside.txt`를 경계 검사 없이 읽으며, 메모리 시험에서 해시가 맞으면 문제 목록 `[]`를 반환했다.

**수정 문안:** “봉인·대조·소비가 동일한 입력 목록을 사용하도록 결속하고, 소비 파일의 봉인 포함 여부와 목록 경로의 어휘·realpath 경계를 읽기 전에 검사한다.”

**OA-5 · HIGH · ⑴ P5 위반 — 쓰기 자리 열거가 Python import 캐시를 빠뜨린다.**

좌표: 메모 §5′.3·§5′.5 P5; [metrics:41](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:41), replay의 최상위 import, regress `run_metrics()`.

실행파일에는 import 전에 bytecode 쓰기를 금지하는 설정이 없고, 메모도 지표기 기동의 필수 조건으로 이를 고정하지 않는다. 회귀 하네스는 별도로 `PYTHONDONTWRITEBYTECODE=1`을 넣는다. 이 시험 환경의 보호가 운영 기동의 성질로 이어지지 않는다.

실제 지표기 진입을 실행하되 Python loader의 캐시 기록을 **쓰기 직전에 가로채** 관측했다. 디스크에는 쓰지 않았다.

```text
EXACT_METRICS_ENTRY exit 4 cache_write_intents_in_bundle
['bundle/__pycache__/t40_replay.cpython-314.pyc',
 'bundle/__pycache__/t40_receipts.cpython-314.pyc',
 'bundle/__pycache__/t40_drive.cpython-314.pyc']
EXACT_RUNTIME_PROBE_DONE actual_writes=0
```

부적격 종료 전이며 sandbox 준비 전이다. **“소스에 파일 쓰기 호출 없음 → 실행 시 파일 쓰기 없음”**이라는 P5 논거가 성립하지 않는다.

**수정 문안:** “지표기·독립 대조기의 import 전부터 bytecode 쓰기를 금지하고, 런타임 및 하위 프로세스를 포함한 부작용 목록으로 P5를 검증한다.”

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | **충족** | 상류 요구는 P1~P7 또는 절차 책임에 배정된다. 좁혀진 ⓔ는 B-04 채택 범위와 맞는다. 실제 집행 결손은 OA에 분리했다. |
| ② 신뢰·입력·부작용 경계 | **미충족** | T1·T2·T4 대응은 확인. T3의 실제 소비 집합은 OA-4, 보존은 OA-2, 런타임 쓰기는 OA-5. |
| ③ 기제의 집행과 합성 | **미충족** | 선판별 자체는 앞에 섰으나 P1→P6 연결이 OA-1. 처분과 보존 합성에도 OA-2·3. |
| ④ 검증 근거 | **미충족** | L 13의 적정 처리 기록은 존재한다. S06은 런 보존을 입증하지 않으며, P5 열거 논거도 불완전하다. |
| ⑤ 미충족·불명확 상태의 처분 | **미충족** | 정상 대상 일괄 거부 구현은 아니다. 그러나 잘못된 재실측·보고 분류 및 증거 삭제가 남는다. |

상류 요구의 배정은 다음과 같다.

| 상류 요구 | 받는 성질·절차 |
|---|---|
| 같은 소재·절차, 승인된 세 팔·법 핀·Workflow 하드 지정 | P1, §0′·§3 |
| 호출별 일지, 동일 법·입력의 재실행, 응답 바이트 유지 | T3·P2 |
| 종결·대기·실패의 정확한 해석 | P3 |
| 세 런 한정 대행 봉투, 허용 축·육성·근거·판정서 결속 | P4 |
| 원본 비변조·생산 원장 격리 | P5 |
| IO 결함 지표 미발행·보존·재실측·필요시 새 ID 재정 | P6·P7, §2 |
| 선등록 임계·잡음 폭·Owner 판독·결측·결과 표·재상신 | P7, §5 |
| 착수 전 PASS·방식 지적 재상신·자문 | §5′.6 |

제외 ⓐ~ⓖ는 명시된 범위에서 문언상 설명된다. 특히 **ⓔ의 문언 수정은 닫혔다.** 보존된 봉인과 충돌하는 자료까지 면제하는 문장이 아니다. 다만 그 경계를 실제로 집행한다는 T3 주장은 OA-4로 아직 닫히지 않았다. P5는 ⓔ의 자료에도 적용된다.

**기제·구조적 논거**

- **P1 등식 사슬:** 선등록표의 세 런·핀·좌석·소재·봉투 권한은 원장과 일치했다. 정상 검수의 대응 사슬은 있으나 T43 조기 반환 경로에서 영수증 결속이 빠진다.
- **P2 정규화·환경:** 시각 두 키 제거, 경계에서만 역할 토큰 치환, 원시 포인터 검사를 확인했다. 대표 `run_id`·종결·축 값/status·escalations·봉투 육성·계수 보존도 확인했다. 공유 clone 아래 linked worktree는 러너의 `main-worktree-resolved` 판정과 맞는다.
- **P3·P4:** 종결 가드 재사용과 상태별 계수 제한, 봉투의 독립 권한 검사를 확인했다. P4는 재조립 통과 사실을 권한 증명으로 대신하지 않는다.
- **P5 쓰기 열거:** clone 앞 `_inside`, 런 자식 목적지, 응답·봉투 기록과 봉투 삭제의 검사는 확인했다. Git status의 optional lock 수정도 있다. 런타임 캐시가 목록 밖에 남는다. 또한 하위 호출까지 포함하면 `law_status` 하나뿐이라는 설명은 정확하지 않다. 영수증·러너 경로 해석에도 Git 조회가 있다.
- **P6 첫 분기:** 정상 결함 영수증에서는 부분 기록 `[`를 읽지 않고 재실측하며 sandbox 호출은 0이었다. `_halt4_bound`는 raw 지문이 맞을 때만 호출을 반환했다. 이 사실은 OA-1의 **판별 근거 식별**을 대신하지 않는다.
- **P7:** 기준 지표·발췌·표본 규칙은 재현됐다. 처분 전달과 제외 시도 보존에는 OA-2·3이 남는다.

모든 P에 시험 사례는 배정돼 있다. 그러나 **시험 ID의 존재와 성질 전체의 입증은 구별해야 한다.**

회귀표와 `CASES()`는 **113행 = L 13·F 7·C 84·X 2·S 7**, ID 집합과 PASS 113 기록이 일치했다. L 13은 전부 exit 0 기록이다. P별 증명 열에 있던 없는 ID C05·C35·C81의 직접 인용도 정정됐다.

**F 부모 파생 C의 현재 수는 12건**이다. C01이 L02로 이동하고 C84·C85가 추가된 결과다.

| 실제 처분 | 사례 | 증거의 뜻 |
|---|---|---|
| 부적격 | C08·C09·C10·C29·C69·C83 | 해당 손상·결측·모순의 거부 근거로 구별 가능 |
| 재실측 | C74~C77·C84·C85 | 개별 변조 탐지 근거가 아님. 특히 C84·C85는 선판별 순서의 근거 |

따라서 “F 파생 C 11건 전부가 개별 탐지 증거가 아니다”라는 일괄 설명은 현재 코드·표와 맞지 않는다.

**A 폐쇄표**

`closed`는 기존 ID가 지적한 구체적 결함의 폐쇄다. P 전체 보증이나 과거 반례 전건의 이번 독립 재실행을 뜻하지 않는다.

| 지적군 | closed | partially / open |
|---|---|---|
| MY | 1~13 | — |
| MZ | 1~9 | — |
| NA | 1~7 | — |
| NB | 1~3 | — |
| NC | 1~3 | — |
| ND | 1~2 | — |
| NE | 1~2 | — |
| NF | 1 | — |
| NG | 1~2 | — |
| NH | 1~2 | — |
| NI | 1~2 | — |
| NJ | 1 | — |
| NK | 1 | — |
| NL | 1 | — |
| NM | 1~2 | — |
| NN | 1~4 | — |
| NO | 1~4 | — |
| NP | 1~3 | — |
| NQ | 1~3 | — |
| NR | 1~6 | — |
| NS | 1~6 | — |
| NT | 1~5 | — |
| NU | 1~4 | — |
| NV | 1~3 | — |
| NW | 1~5 | — |
| NX | 1~4 | — |
| NY | 1~4 | — |

MY~NY **102건 closed** 판정을 유지한다. 기존 지적 표제·28차 폐쇄 근거·§5′.10과 현 기제를 대조했다. §5′.10의 보존 인용문도 v29에 그대로 존재했다.

| NZ | 판정 | 기제·사례와 잔여 |
|---|---|---|
| NZ-1 | **closed** | `law_status`·replay/receipts `_git`의 플래그, S05 인덱스 불변 기록. OA-5는 별도의 런타임 쓰기 누락이다. |
| NZ-2 | **closed** | 전 호출 선판별, `_halt4_bound`, C84·C85 및 이번 `[` 메모리 재현. 새로 드러난 식별 합성은 OA-1. |
| NZ-3 | **partially** | `disposition`·`die(kind)`·다음 절차 표는 구현. 분류 경계는 OA-3. |
| NZ-4 | **partially** | attempt·번호 초기화·종결 가드·S06·S07·C87은 존재. 결함 런 보존과 이력 완결은 OA-2. |
| NZ-5 | **partially** | ⓔ 문언·봉인 시점/책임·`cmd_seal`·C86은 구현. 봉인 대상과 소비 대상 결속은 OA-4. |

합계 **closed 104·partially 3·open 0**이다. 신규 OA-1~5는 별도다.

**검증 경로**

모든 명령의 cwd는 지정 사본이다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B`다. 메모리 시험 본문은 표준입력으로 전달했으며 파일로 저장하지 않았다.

| 명령·직접 검증 경로 | 마지막 출력 또는 핵심 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `ed011a175c68d21ffb9c0e5de0a31498a0b90e10` |
| `sha256sum bundle/T40-MEASURE-DESIGN.md …` | 제시 해시 전부 일치. 회귀표 `69ded53e1097825e…` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | 절차 6파일만, 마지막 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git log -1`·`git ls-tree` 세 ref | base 부모 `6d92cad`; 절차 tree `d7717eb8…`; 계약 blob `ea238e5…/003f16c…/745cc34…` |
| `git diff --numstat d4e6ca2 6d92cad -- <§0′ 16파일>` | 메모 수치 일치, 마지막 `90 35 reader/lib/run_checks.py` |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 4, `기준 런은 --law-tree … 이 필수다` |
| `git show origin/t40-base:<경로>` 62파일 → 메모리 법 → 실제 `metrics(..., baseline=True)`·`lane_profiles()` | `complete · 163 · component 56 · E/full 1/1`; `REGISTRY r0/r1/r2 True`; 마지막 `MEMORY_BASELINE_DONE writes=0 law_files=62` |
| 실제 영수증 적재·봉인·선판별에 메모리 파일 공급 | foreign run/law도 재실측; 마지막 `RECEIPT_BOUNDARY_PROBES_DONE writes=0` |
| 실제 `cmd_retire()`·`validators()`에 메모리 대역 | `RUN_BYTES_PRESERVED False False`; 마지막 `RETIRE_DISPOSITION_RUNTIME_PROBES_DONE writes=0` |
| 실제 지표기 진입 + loader 캐시 쓰기 차단·관측 | bundle 캐시 요청 3건; `EXACT_RUNTIME_PROBE_DONE actual_writes=0` |
| 실제 `manifest_verify()` ↔ `dispatch_records()` | 봉인 밖 발주 소비; `MANIFEST_CONSUMER_BINDING_DONE writes=0` |
| `_halt4_bound`·정규화·루트 해석·발췌 순수 함수 | 결속 2/미결속 None; 의미 보존 True; `SEMANTIC_PROBES_DONE writes=0` |
| Node `AsyncFunction`으로 Workflow 본문 실행, `agent/pipeline` 대역 | 정상 `claude-opus-5/max`; 잘못된 모델·경로·중복은 호출 0; `WORKFLOW_DONE writes=0` |
| 스테이징 원문 정본화·도면 전량 해시·구동 분류 | 298,572→298,507 B, 등록 지문 일치; 도면 20·MANIFEST 일치; 분류 `[0,11,12,13,14]`; `SOURCE_DRIVE_DONE writes=0` |
| `CASES()`·회귀표 ID/처분 대조 | `TABLE 113 113 … PASS 113 ID_EQUAL True`; `TABLE_DISPOSITIONS_DONE` |

기준 런의 통합 계수는 fact/implication/positioning/figure_note **3/20/7/10**, 전체 anchor **51/5**, 종속항 anchor **45/5**였다. 발췌 단위는 **27**, 표본은 **CL-2·4·7·9·12·14·16·19·21·24**로 메모와 일치했다.

**[미검증]**

- clone·worktree 생성, sandbox 디스크 재실행, 회귀 113건 전건 재실행, 실제 `retire`·`seal-evidence`는 수행하지 않았다. S05~S07은 제출된 디스크 시험 기록과 시험 본문을 대조했다.
- 메모리 시험의 파일·환경·종결 가드 대역은 위 검증 경로에 명시했다. 전체 실측 런을 생성한 통합 시험으로 주장하지 않는다.
- 과거 1~27차 반례 전건을 다시 실행하지 않았다. 폐쇄표는 선행 판정·현재 기제·이번 직접 검증을 종합했다.
- 실제 Workflow 모델 호출·transcript·effort 증거와 향후 봉인·결과 커밋·Owner 판독 결과는 아직 검증 대상 실물이 없다.

**읽은 파일**

원장 T40·T42·T43·T14·T17·T38, D-02 §17 추기 31~34; 메모 v31 §0′~§9와 v29·v30 관련 부분; 자문 2회차 B-04·3회차 회신 및 질문·상황·접근 문서; 28차 원문과 MY~NY 지적·폐쇄 기록; drive·replay·receipts·metrics·regress·excerpts·envelope·Workflow 및 회귀표; SPEC 지정 행, run-kinds·read 계약·승인 봉투 스키마; read·paths·gitpin·lane contract/file_adapter·convergence·run_checks·source와 검증 중 적재한 규칙·스키마; 기준 런 메타·원천·판정서·명세·요청·응답·원장, 지정 스테이징 TXT와 도면 20파일.

**Owner 범위 재정 대상:** 이번 심사에서 새 보증 요구 ⑶은 없다. OA-1~5는 현재 승인된 성질·전제의 집행 범위 안에 있다.