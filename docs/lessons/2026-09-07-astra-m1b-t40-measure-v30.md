# 독립 감수 원문 — M1b 설계 도전 30차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v32(연역 명세 · 28·29차 반영) · 판정 REVISE(HIGH 3 · MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `b4e1a17dd400ea31ea06e0294bdd5bdd6616b08cc7ae07726e5a74f64fbd08f9` · 22919 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v30/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = Monitor STATUS EXIT= + FINAL 바이트(08:35 기동 · 09:0x 종료 · USAGE input 5,786,560(cached 5,504,128) · output 23,854). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `0990f64` · 마커 3항 일치 · 메모 v32 sha256 `4baa56cf…` · v1~v31 + 스크립트 9종 + 회귀표 v11(121) + 자문 1~3회차 + 재정 T42·T43 + SPEC v30 동봉). Owner 육성 「30차: A / 규약: 채택」(재정 T44 · D-02 추기 37) 로 기동. 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 30회」와 **「재조립 방식 자체의 신뢰 입력·격리·처분 합성을 다시 REVISE — Owner 재정 상신 대상 · 채택된 상설 규약을 적용하더라도 T3 와 P5 의 연결 문제가 세 회차에 걸쳐 이어졌다」** 명기. **심사 대상 ① 도출의 완전성 = 충족** · ②~⑤ 미충족 · 도출 누락 0 · 새 보증 요구 0 · **갈래 전부 ⑴** · ⓔ 문언상 제외 확정(NZ-5 제외 문구 closed) · MY~NY 102 closed 유지 · NZ-1·2·4 closed · NZ-3·5 partially · **OA-1·3·4 partially · OA-2·5 closed**(합계 closed 107 · partially 5 · open 0) · T1·T2·T4 확인 · P2 정규화·환경 동치 새 단절 없음 · P4 책임 분리 유지 · 기준 런 메모리 재현 일치 · `registry()` 원장 일치 · F 파생 C 는 **14건**(부적격 8 = C08·C09·C10·C29·C69·C83·C88·C89 / 재실측 6 = C74~C77·C84·C85 — 메모 §9 12건·발주문 11건은 낡음).

**판정 = REVISE · 4건(HIGH 3 · MED 1) · 기각 0 · 발주자 귀책.** **OB-1 HIGH · T3·P6(P1→P6 합성)**: 메모는 「지표기와 독립 대조기 모두 attempt·MANIFEST 까지 결속한 뒤 선판별」이라 했지만 `replay()` 에는 `manifest_verify`·`load_attempts` 호출이 없다 — 봉인 없는 영수증·낡은 attempt 영수증이 독립 대조기에서 「재실측」 근거로 승격(NO_MANIFEST·STALE_ATTEMPT → io-fault · manifest_reads 0). **OB-2 HIGH · T3·§5′.2 입력 경계**: 「봉인·대조·소비가 같은 `evidence_files()`」가 아직 아니다 — `manifest_verify` 는 `dirname(RECEIPTS)/dispatch` 를, 소비기 `dispatch_records` 는 별도 전역 `EVIDENCE_DISPATCH`(CLI 로 바꿀 수 있음)를 순회하고 둘의 일치 검사가 없어 다른 디렉터리의 발주 기록이 소비됨(ALTERNATE_DISPATCH) · 목록 밖 `dispatch/*.json` 후보는 run_id 를 알아내려 realpath 경계 확인 **전에** 연다(UNLISTED_LINK read_before_rejection True · C92 는 목록에 적힌 경로만 덮음). **OB-3 MED · P7·§5′.4**: 역할별 처분 분류가 모든 경계에 전달되지 않음 — 승인 봉투 **스키마** 읽기는 kind 생략(부적격이어야 할 것이 아니라 검수 불능이어야 함) · `run.yaml#engine: 1` 은 중첩 형태 검사 전 `.get()` → 검수 불능(자료 형태 = 부적격이어야) · halt 판정서 `findings: 1` → `_halt4_signature` TypeError → 검수 불능 · 영수증 파일 PermissionError 는 ValueError 만 잡아 검수 불능(자료 판독 실패 = 부적격이어야). **OB-4 HIGH · P5**: `sandbox_prepare` 의 보호 집합이 6 경로(run_dir · repo · main_orig · receipts_dir · first_early · ledger)뿐 — 외부 evidence 루트·`dispatch/`·`retired/` 가 빠져 소유 표식이 있는 `evidence/dispatch` 를 sandbox 로 지정하면 원본 발주 증거 **삭제 단계에 도달**(WRITE_INTENTS delete_tree evidence/dispatch) · 소유 표식은 「원본과 겹치면 무삭제」 상위 조건을 면제하지 않는다.

**T44 판정(재정 T44 §1 ②) = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 요구 0 ✓ · ⓒ 갈래 전부 ⑴ ✓ — 그러나 「같은 성질 P/전제 T 가 세 회차 연속」 조건에 걸린다**: T3(28 NZ-5 → 29 OA-4 → 30 OB-1·OB-2) · P5(28 NZ-1 → 29 OA-5 → 30 OB-4) · P6(28 NZ-2 → 29 OA-1 → 30 OB-1) · P7(28 NZ-3 → 29 OA-3 → 30 OB-3) — 네 축이 세 회차 연속 → **자동 기동 불가 · Owner 상신.** 도전자도 같은 판정(「채택된 상설 규약을 적용하더라도 … 세 회차」).

**처분 = 전부 수용(공학) · 이행 = Owner 재정 뒤(집행 주체·경로가 재정 사항).** 수정 문안(도전자 문안 그대로 v33 의 요구 사항) — OB-1 = 「두 진입점은 동일한 결속 함수를 사용하여 calls 경계·현재 attempt·MANIFEST·런·법 결속을 완료한 영수증만 T43 선판별에 전달한다」(공용 `bind_receipts(run_dir, receipts_dir, run, run_id)` 를 `t40_receipts` 에 두고 지표기·대조기가 같은 함수 호출 · C93 = 대조기 CLI 에 봉인 없는 영수증 → mismatch) · OB-2 = 「봉인·대조·소비는 경계 검사를 마친 공통 파일 집합만 사용하고, dispatch 경로를 봉인 디렉터리에 결속하며 모든 탐색 후보의 어휘·realpath 를 열기 전에 검사한다」(`--evidence-dispatch` 는 `dirname(RECEIPTS)/dispatch` 와 realpath 동일 요구(exit 3) · `evidence_files` 가 후보를 열기 전 어휘·realpath·lexists 조상 검사 · `dispatch_records` 가 `evidence_files` 의 집합에서만 읽음 · C94·S11) · OB-3 = 「모든 읽기·파싱 경계에 법/자료 역할을 전달하고, 중첩 자료 형태를 접근 전에 검증하여 자료 예외가 검수원 예외 경계로 새지 않게 한다」(봉투 스키마 kind=검수 불능 · run.yaml 중첩 형태 검사 · `_halt4_signature` 원소 타입 검사 · 영수증 OSError → ValueError 로 포장 → 부적격 · C95~C97 · S12) · OB-4 = 「sandbox 준비 전에 봉인 evidence 전체와 별도 소비 입력·보존 시도 경로를 보호 집합에 포함하고, 표식 유무와 무관하게 원본과의 겹침을 무삭제로 거부한다」(`sandbox_prepare(protected=[…, evidence 루트, dispatch, retired, LANE_DIR])` · 겹침 검사가 표식 검사보다 앞 · S13) · 정정 = F 파생 C 14건(8/6) · 발주문 11건 문구. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 38**. 다음 = **Owner 상신(T44 세 회차 연속 · 선택지 = A 총괄 v33 → 31차 / B 자문 4회차 / C v33 저작을 M3 sol-coder 에 발주 / D 실측 먼저(PASS 조건 변경 재정)) → 재정대로**.

지적 열거 = OB-1, OB-2, OB-3, OB-4

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 30회)

**① 도출의 완전성은 충족한다. 그러나 ②~⑤는 미충족이다.** 지적은 **OB-1~4, HIGH 3·MED 1, 모두 갈래 ⑴**이다. 도출 누락과 새 보증 요구는 없다.

**재조립 방식 자체의 신뢰 입력·격리·처분 합성을 다시 REVISE한다 — Owner 재정 상신 대상이다.** 채택된 상설 규약을 적용하더라도 T3와 P5의 연결 문제가 세 회차에 걸쳐 이어졌다. 기존 자문이 대기 중이라는 뜻은 아니며, 이번 판정에 따른 상신이다. PASS 전 실측 착수 금지는 유지된다.

**사본·지문 확인**

첫 명령 `cat .audit-sandbox; git rev-parse HEAD`에서 다음을 확인했다.

```text
path=/home/laptop/projects/workspaces/pd-m1b-t40
pin=0990f649ae0f865d211df9b6096b0279d26c4a09
order=M1B-t40-measure-v32-20260907
disposable=true
0990f649ae0f865d211df9b6096b0279d26c4a09
```

경로·핀·발주 마커 모두 일치한다. 메모 v32·v31과 발주에 제시된 스크립트 지문도 모두 일치했다. 지문 불일치 지적은 없다. 회귀표 지문은 `e828afc735ed1ec22…`이다.

정본 리포는 읽지 않았다. 허용된 Python 인터프리터만 빌렸으며, 파일 생성·수정·삭제, checkout·worktree·stash, 배경 실행은 하지 않았다.

**OB-1 — HIGH · ⑴ T3 미충족, P1→P6 합성 위반**

좌표: 메모 §5′.1·§5′.5 P6·§5′.8, [t40_replay.py:136](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:136), [t40_receipts.py:218](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:218).

메모는 **지표기와 독립 대조기 모두** 현재 attempt와 MANIFEST까지 결속한 뒤 T43 선판별에 들어간다고 명시한다. 지표기는 그렇게 하지만, `replay()`에는 `manifest_verify`, `load_attempts`, `current_attempt` 호출이 없다.

`load_receipts()`가 보장하는 attempt 조건은 **적재한 영수증끼리 같은 시도라는 것**이다. `attempts-<r>.json#current`와 같은지는 보장하지 않는다. 대조기는 run_id·법 HEAD·법 파일·run.yaml을 대조한 직후 IO 분기로 들어간다.

실제 `load_receipts()`와 `replay()`를 메모리 파일·법 조회 대역으로 연결한 결과:

```text
NO_MANIFEST io-fault replayed 0 manifest_reads 0 attempts_reads 0
STALE_ATTEMPT io-fault replayed 0 manifest_reads 0 attempts_reads 0
FOREIGN_RUN mismatch replayed 0 manifest_reads 0 attempts_reads 0
FOREIGN_LAW mismatch replayed 0 manifest_reads 0 attempts_reads 0
SANDBOX_CALLS 0
```

다른 런·다른 법의 영수증을 거부하는 OA-1 수정은 작동한다. 그러나 봉인이 없는 영수증도 독립 대조기에서 **재실측 근거로 승격**된다. 현재 attempt 조회도 없다. 지표기의 선행 검사는 §6에서 별도로 제출하는 독립 대조 결과의 누락을 대신하지 못한다.

- **잘못된 처분:** T3를 만족하지 않은 자료를 `mismatch`로 거부하지 않고 `io-fault`로 처분한다.
- **수정 문안:** “두 진입점은 동일한 결속 함수를 사용하여 calls 경계·현재 attempt·MANIFEST·런·법 결속을 완료한 영수증만 T43 선판별에 전달한다.”

**OB-2 — HIGH · ⑴ T3 및 §5′.2 입력 경계 미충족**

좌표: 메모 §5′.1·§5′.2·§5′.7 ⓔ, [t40_metrics.py:295](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:295), [t40_metrics.py:832](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:832), [t40_receipts.py:257](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:257).

“봉인·대조·소비가 같은 `evidence_files()`로 같은 집합을 본다”는 연결이 아직 성립하지 않는다.

`manifest_verify()`는 `dirname(RECEIPTS)/dispatch`를 대상으로 삼는다. 반면 소비기 `dispatch_records()`는 별도 전역 `EVIDENCE_DISPATCH`를 직접 순회하며, CLI에서 이 경로를 바꿀 수 있다. 두 경로의 일치 검사가 없고, 소비기는 `evidence_files()`를 호출하지 않는다.

메모리에서 실제 봉인 대조와 소비 함수를 호출하자, 봉인 디렉터리의 검사는 문제 없이 끝났지만 다른 디렉터리의 발주 기록이 소비되었다.

```text
ALTERNATE_DISPATCH manifest [] consumed {'read-a/decompose/batch-0': ['bbbb…']}
```

이는 **해당 계층의 봉인·소비 불일치 재현**이다. 전체 지표기의 최종 통과까지 실행했다는 뜻은 아니다.

또한 목록 경로의 realpath 검사는 **MANIFEST에 적힌 파일에만** 적용된다. 이후 `evidence_files()`는 목록 밖 `dispatch/*.json`도 run_id를 알아내려고 먼저 연다. 메모리에서 그 후보의 realpath를 evidence 밖으로 지정했을 때:

```text
UNLISTED_LINK read_before_rejection True
problems ['봉인 뒤에 생긴(MANIFEST 에 없는) 증거 파일: dispatch/extra.json']
```

최종 거부는 하지만, “밖이면 읽지 않는다”는 입력 경계는 이미 넘었다. C92는 **목록에 적힌 경로**를 검증하며 이 탐색 경로를 덮지 않는다.

- **잘못된 처리:** 소비할 발주 바이트의 봉인 여부가 보장되지 않고, 목록 밖 후보는 외부 경계를 확인하기 전에 읽는다.
- **수정 문안:** “봉인·대조·소비는 경계 검사를 마친 공통 파일 집합만 사용하고, dispatch 경로를 봉인 디렉터리에 결속하며 모든 탐색 후보의 어휘·realpath를 열기 전에 검사한다.”

**OB-3 — MED · ⑴ P7 및 §5′.4 처분 분류 위반**

좌표: 메모 §5′.4·§5′.5 P7, [t40_metrics.py:323](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:323), [t40_metrics.py:376](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:376), [t40_metrics.py:751](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:751), [t40_replay.py:95](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:95).

OA-3의 `kind` 추가와 최상위 비객체 JSON 처리는 유효하다. 하지만 입력의 역할에 따른 분류가 모든 경계에 전달되지는 않았다.

| 끊긴 경계 | 실제 처리 | §5′.4가 요구하는 처리 |
|---|---|---|
| 승인 봉투 **스키마** 읽기·파싱 | `kind` 생략으로 부적격 | 검수 불능 |
| `run.yaml`의 `engine: 1` | 중첩 형태 검사 전 `.get()` → 최상위 검수 불능 | 자료 형태 실패 → 부적격 |
| halt 모양 판정서의 `findings: 1` | `_halt4_signature()` 반복 중 `TypeError` → 검수 불능 경계 | 자료 형태 실패 → 부적격 |
| 영수증 파일 `PermissionError` | `ValueError`만 잡아 최상위 검수 불능 | 명시된 자료 판독 실패 → 부적격 |

메모리 경계 시험의 출력:

```text
CONVERGENCE_SCHEMA exit4 처분=검수 불능
APPROVAL_SCHEMA exit4 처분=부적격
HALT_FINDINGS_INTEGER TypeError => outer disposition=infeasible
RUN_YAML_ENGINE_INTEGER exit4 처분=검수 불능
RECEIPT_READ_FAILURE exit4 처분=검수 불능
DISPOSITION_PROBES_DONE writes=0
```

승인 스키마 시험은 실제 751행의 읽기 식을 추출해 해당 읽기 경계에 실패를 주입한 것이다. 전체 실행의 앞선 법 지문 검사를 생략한 국소 시험임을 구분한다.

- **잘못된 처분:** 같은 exit 4 안에서 “표에 싣고 자료 보존”과 “표에서 제외하고 환경 수리”가 뒤집힌다. 총괄이 접두를 그대로 따르면 오처분하고, 고치려면 다시 해석해야 한다.
- **수정 문안:** “모든 읽기·파싱 경계에 법/자료 역할을 전달하고, 중첩 자료 형태를 접근 전에 검증하여 자료 예외가 검수원 예외 경계로 새지 않게 한다.”

**OB-4 — HIGH · ⑴ P5 위반**

좌표: 메모 §5′.3·§5′.5 P5·§5′.7 ⓔ, [t40_replay.py:54](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:54), [t40_replay.py:190](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:190).

쓰기 자리 목록과 `_inside` 추가는 확인했다. 그러나 첫 삭제 전에 보호하는 **원본 집합**이 불완전하다.

`replay()`가 `sandbox_prepare()`에 넘기는 것은 다음 여섯 경로다.

```text
run_dir, repo, main_orig, receipts_dir, first_early, ledger_path
```

외부 evidence 디렉터리 전체와 그 아래 `dispatch/`, `retired/`는 포함되지 않는다. 따라서 원본 주 작업 트리 밖에 있는 `evidence/dispatch`에 소유 표식이 존재하고 이를 sandbox로 지정하면, 다른 보호 경로와 겹치지 않아 삭제 단계에 도달한다.

실제 `replay()`→`sandbox_prepare()`를 호출하되 삭제·생성·쓰기를 모두 메모리 기록으로 대체했다.

```text
PROTECTED_EVIDENCE_ROOT False PROTECTED_DISPATCH False
WRITE_INTENTS [
 ('delete_tree', '/memory/t40/evidence/dispatch'),
 ('mkdir', '/memory/t40/evidence/dispatch'),
 ('write', '/memory/t40/evidence/dispatch/.t40-replay-sandbox')]
FINAL infeasible sandbox 공유 클론 실패
SANDBOX_EVIDENCE_PROBE_DONE actual_writes=0
```

클론 실패는 시험을 멈추기 위해 대체한 반환이다. 그 전에 원본 발주 증거 삭제가 요청됐다는 점이 반증이다. 이후 자식 목적지의 `_inside` 검사는 이 삭제를 막지 못한다. 소유 표식도 **원본 자료와 겹치면 무삭제**라는 P5의 상위 조건을 면제하지 않는다.

- **잘못된 부작용:** 검수 불능으로 끝나는 실행이 원본 증거를 먼저 삭제할 수 있다.
- **수정 문안:** “sandbox 준비 전에 봉인 evidence 전체와 별도 소비 입력·보존 시도 경로를 보호 집합에 포함하고, 표식 유무와 무관하게 원본과의 겹침을 무삭제로 거부한다.”

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | **충족** | T40 §4의 비교 조건·선등록·임계·결측·Owner 판정은 P1·P7, §5 봉투는 P4, T42 재조립·격리는 P2·P5, T43 결함 처분·보존은 P6·P7 및 §2, 게이트·상신은 §5′.6으로 연결된다. 새 도출 누락은 없다. |
| ② 신뢰·입력·부작용 경계 | **미충족** | T1·T2·T4의 현재 자료 대조는 성립한다. T3의 독립 대조기·소비 집합 연결은 OB-1·2, 원본 보호 범위는 OB-4에서 끊긴다. |
| ③ 기제의 집행과 합성 | **미충족** | 담당 기제 자체가 전혀 없는 P는 없다. 그러나 “결속 완료→P6”와 “첫 쓰기 전 P5”가 두 진입점 전체에서 성립하지 않는다. OB-1·4. |
| ④ 검증 근거 | **미충족** | 제출표의 L 13·전체 121 PASS 기록과 사례 연결은 확인했다. 그러나 그 기록이 OB-1~4의 경계를 검증하지 않으며, P1·P5·P6의 구조적 논거도 해당 연결에서 끊긴다. |
| ⑤ 미충족·불명확 상태의 처분 | **미충족** | 정상 상태를 일괄 거부하는 구현은 아니다. `retire` 보존도 개선됐다. 다만 OB-1·3 때문에 부적격/재실측/검수 불능이 명세대로 갈리지 않는다. |

T1~T4 중 특히 T3의 **구체적인 봉인 시점·대조 절차가 T42 원문에 직접 적혀 있는 것은 아니다.** 메모도 이를 밝혔으며, 지정된 영수증을 신뢰 입력으로 사용하기 위한 구현 절차로 채운 것은 타당하다. 문제는 그 절차의 실제 집행이다.

§5′.7 ⓐ~ⓖ에서 새 보증 축소는 발견하지 않았다. 특히 ⓔ는 B-04의 **외부 봉인까지 모두 함께 바뀐 자료**로 좁혀졌으므로 문언상 제외가 맞다. NZ-5의 **제외 문구 문제는 닫혔다.** 다만 MANIFEST와 어긋나는 자료를 실제로 거부하는 연결은 OB-1·2 때문에 아직 닫히지 않았다. P5는 이 제외 자료에도 적용되며, OB-4의 반례를 범위 밖으로 돌릴 수 없다.

구조적 논거 네 가지의 판정은 다음과 같다.

| 논거 | 판정 |
|---|---|
| P1 등식 사슬 | 지표기의 정상 경로는 확인했다. 독립 대조기의 현재 attempt·봉인 고리가 빠져 전체 주장은 불성립한다. |
| P2 정규화 보존 | 경로 경계 치환·역할 구분·정규화 전 검사와 메모리 의미 보존 시험에서 새 단절을 발견하지 않았다. |
| P5 쓰기 자리·하위 프로세스 | clone 앞·자식 목적지·봉투 삭제 검사, Git 플래그, bytecode 억제는 확인했다. 첫 삭제의 보호 집합이 불완전해 전체 논거는 불성립한다. |
| P6 첫 분기 | 정상 결속 자료의 부분 기록 `[`보다 앞서 실행됨을 확인했다. 그러나 독립 대조기에서는 “T3를 통과한 뒤”라는 전제가 없다. |

P4는 재조립 성공만으로 권한을 인정하지 않는다. 별도 봉투 권한 식이 run_id·육성·근거 위치·대상 지문·허용 축·청구항 실패를 검사한다. 이 책임 분리는 유지된다.

**회귀 근거의 정정**

`CASES()`와 표의 ID를 직접 대조했다.

```text
TABLE 121 121 ID_EQUAL True COUNTS {'L': 13, 'F': 7, 'C': 89, 'X': 2, 'S': 10} PASS121
L_EXIT0 13
```

각 P의 증명 의무에 기재된 사례는 표에서 확인된다. 다만 **F 부모 파생 C는 현재 14건**이다. 메모 §9의 12건과 발주의 11건은 갱신이 필요하다.

- **부적격 8:** C08·C09·C10·C29·C69·C83·**C88·C89**. 기록된 거부 사유가 해당 손상·결속 실패를 구별한다.
- **재실측 6:** C74·C75·C76·C77·C84·C85. 개별 변조 탐지의 증거로 셀 수 없고, T43 선판별·결함 런 처분의 근거다.

따라서 “F 파생 C 전부가 개별 탐지 증거가 아니다”도 정확하지 않다. v32의 두 갈래 구분은 맞지만 수량이 낡았다. 이는 ④의 근거 표 정정이며 별도의 보증 축을 추가한 지적은 아니다.

C86·C91·C92의 `noseal` 경로는 **복제→재봉인→변조** 순서임을 코드에서 확인했다. 복제 경로 보정 차이를 탐지한 것으로 오인했던 문제는 수정됐다.

**A 폐쇄표**

`closed`는 해당 기존 지적의 구체적인 결함이 닫혔다는 뜻이다. 같은 P에 새 연결 결함이 발견되지 않았다는 뜻은 아니다.

| 기존 지적 | 판정 | 폐쇄 근거·잔여 |
|---|---|---|
| MY-1~13 · MZ-1~9 · NA-1~7 · NB-1~3 | closed | §5′.10의 기존 검사 연결, 상태·지표·발췌 경로 및 기준 런 추출 확인 |
| NC-1~3 · ND-1~2 · NE-1~2 · NF-1 · NG-1~2 | closed | 기존 원장·계수·결측·발췌 정의 유지 |
| NH-1~2 · NI-1~2 · NJ-1 · NK-1 · NL-1 | closed | 요청·응답·원천 지문 연결과 정본화 대조 유지 |
| NM-1~2 · NN-1~4 · NO-1~4 · NP-1~3 | closed | 상태별 추출, 소비 적격성, 판정서·명세 생성 관계 유지 |
| NQ-1~3 · NR-1~6 · NS-1~6 · NT-1~5 | closed | 거부 행·종결 가드·재시도·스냅샷·별도 법 트리 검사 유지 |
| NU-1~4 · NV-1~3 | closed | 비대칭 재시도·접지 거부·첫 관측 결속 유지 |
| NW-1~5 · NX-1~4 · NY-1~4 | closed | 루트 환경·역할 정규화·법 결속·봉투 권한·기존 경로 반례·T43 처분 유지. 새 보호 대상 누락은 OB-4로 구분 |
| NZ-1 | closed | Git 조회의 `--no-optional-locks`, 쓰기 자리 보강, S05 |
| NZ-2 | closed | 결함 선판별이 산출물 파싱·재실행보다 앞섬. C84·C85 및 이번 `[` 메모리 시험 |
| NZ-3 | **partially** | 접두·disposition은 추가됐으나 역할별 예외 분류가 OB-3에서 미완 |
| NZ-4 | **closed** | 같은 ID 재시도의 물리적 증거 분리·런 보존은 OA-2와 S06·S07로 보강됨. 독립 소비기의 현재 시도 확인 누락은 OB-1 |
| NZ-5 | **partially** | ⓔ 문언은 closed. 봉인 기준의 실제 적용은 OB-1·2 |
| OA-1 | **partially** | 다른 런·다른 법 결속은 C88·C89 및 메모리 시험으로 closed. 두 검수기 전체의 attempt·MANIFEST 연결은 OB-1 |
| OA-2 | **closed** | `copytree`→런 전체 sha 대조→`run-preserved.json`→원본 삭제, 구조화 이력. S06·S07 |
| OA-3 | **partially** | 최상위 비객체 JSON·일부 법 스키마 처리는 closed. 중첩 형태·남은 역할 분류는 OB-3 |
| OA-4 | **partially** | 본문 run_id 선택·목록 경로 검사·지표기 calls basename은 closed. 소비 경로·목록 밖 탐색·독립 진입점은 OB-1·2 |
| OA-5 | **closed** | 다섯 스크립트의 import 전 bytecode 억제, S10 및 이번 실제 진입점 캐시 쓰기 대역 관측 |

집계는 **closed 107·partially 5·open 0**이다. MY~NY 102건은 이전 폐쇄 판단과 현행 기제 대조를 유지한 것이며, 102개 옛 반례를 이번에 전부 재실행한 것은 아니다.

OA-2의 제출 디스크 시험 기록은 다음과 같다.

```text
S06: exit=0 before=1 retired_dirs=1 moved=True run_preserved=True
history_structured=True calls_left=0 current=2 io_fault_calls=[1]
run_gone=True next_attempt=2 next_call=1

S07: exit=16 evidence_unchanged=True run_kept=True
```

이로써 이전 실패 런을 복사·대조하지 않고 삭제하던 구체적인 보존 문제는 닫혔다.

**검증 경로**

Python 메모리 시험은 모두 사본 cwd에서 다음 형태로 전경 실행했다. 본문은 도구 호출 기록의 heredoc이며 파일로 저장하지 않았다.

```bash
PYTHONDONTWRITEBYTECODE=1 \
/home/laptop/projects/patent-docent/.venv/bin/python -B - <<'PY'
# 실제 함수를 import하고 필요한 파일·Git·쓰기 경계만 메모리 대역으로 교체
PY
```

| 명령·검증 대상 | 출력 또는 마지막 출력 줄 |
|---|---|
| `sha256sum`으로 메모·대상 파일 대조 | 발주된 지문 전부 일치 |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **출력 없음** — 기준 생성 판과 절차 동일 |
| `git diff --numstat 6d92cad origin/t40-base` | 마지막 줄 `0 139 reader/procedure/HISTORY.md`; 차이는 절차 파일 6개 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 `2 2 contracts/stages/read.yaml` |
| §0′의 구 기준 비교 `git diff --numstat d4e6ca2 6d92cad` | 마지막 줄 `90 35 reader/lib/run_checks.py`; 메모의 16파일 대조 |
| `git log`·`git ls-tree` | base `ad4c6c3`, 부모 `6d92cad`; r1 `530b096`, r2 `00e0bed` 및 트리 확인 |
| 실제 기준 CLI, `--law-tree` 없음 | exit 4, 아래 인용 |
| `git show origin/t40-base:<경로>`의 법 62파일을 메모리 트리로 제공해 실제 `metrics(..., baseline=True)` | `MEMORY_BASELINE_DONE writes=0 law_files=62` |
| 원본 소재 정본화·도면 지문·구동 분류 함수 | `SOURCE_AND_DRIVE_DONE writes=0` |
| 정규화·루트 판정·halt 지문 결속 | `SEMANTIC_PROBES_DONE writes=0` |
| 실제 Workflow 본문, Node에서 `agent/pipeline` 대체 | `WORKFLOW_DONE writes=0` |
| 봉인된 IO 영수증 + lane-log `[` | `P6_AND_READ_BOUNDARY_DONE writes=0` |
| 실제 스크립트 진입점, 캐시 쓰기 함수만 기록 대역 | `BYTECODE_ENTRY_DONE actual_writes=0` |
| OB-1·2의 실제 함수 연결 시험 | `RECEIPT_AND_CONSUMER_PROBES_DONE writes=0` |
| OB-3 분류 경계 시험 | `DISPOSITION_PROBES_DONE writes=0` |
| OB-4 sandbox 보호 집합 시험 | `SANDBOX_EVIDENCE_PROBE_DONE actual_writes=0` |

기준 CLI는 실제로 다음 명령을 실행했다.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B \
bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline
```

마지막 출력:

```text
[t40_metrics] 처분=부적격 · 기준 런은 --law-tree <t40-base 체크아웃> 이 필수다(절차 문서 09-01 판 · NR-3 재렌더 대조)
```

메모리 법으로 실행한 기준 추출은 `complete`, 총 163, component 56, grounding 56, fact 14, implication 20, positioning 7, figure_note 10을 재현했다. 조기·완주 attempt는 1·1이었다. 발췌 27단위와 종속항 표본 `CL-2·4·7·9·12·14·16·19·21·24`도 확인했다.

`registry()`는 메모 §2·§4와 T40 §5의 런 ID·핀·partial/read·좌석·소재 및 도면 지문·봉투 범위·육성·근거 위치·허용 축과 대조했다. 세 핀의 계약 좌석 비교는 모두 `True`였다.

부분 기록 시험에서는 다음을 확인했다.

```text
PARTIAL_LOG exit4 lane_log_reads0 처분=재실측 ... attempt1
P6_SANDBOX_CALLS0
```

정규화 시험은 run_id·terminated·축 값/status·escalations·봉투 의미·계수를 보존했고, 유사 접두 경로를 치환하지 않았다. 원문 NUL은 정규화 우회 토큰으로 받아들이지 않았다. 원본과 sandbox의 루트 판정은 모두 `main-worktree-resolved`였다. halt 판정서 raw 지문을 바꾸면 `_halt4_bound()`의 결속 결과가 사라졌다.

지표기 자체의 파일 쓰기 호출은 없었다. 다만 하위 Git 조회를 “`law_status` 하나”라고 할 수는 없다. 영수증 모듈을 통한 `git_head`·`main_root_of` 조회도 있으며, v32의 세 조회 정정과 `--no-optional-locks`를 확인했다.

**[미검증]**

- 121건 전체 회귀를 이 좌석에서 재실행하지 않았다. 표의 결과와 생성 코드·사례 대응을 검토했다.
- 디스크 sandbox 재조립, clone·worktree 생성, `retire`, `seal-evidence`, 쓰기가 필요한 발췌 명령은 실행하지 않았다. S06·S07 등은 제출된 디스크 결과다.
- 메모리 시험은 특정 경계를 직접 검증한다. 실제 파일시스템에서의 전체 실행 결과로 확대하지 않았다.
- 실제 모델 호출·Workflow transcript, 향후 세 실측 런, Owner 채점, 향후 봉인과 결과 커밋은 검증하지 않았다.
- 기존 MY~NY 102개 반례의 전건 재실행은 하지 않았다.

**읽은 파일·범위**

- 상류: `ruling-20260905-05-T40.md` §1·§4·§5, `bundle/ruling-T42.md`, `bundle/ruling-T43.md`, D-02 §17 추기 31~36, `ADVICE-REPLY-3.md`, `ADVICE-REPLY-2.md` B-04, 28·29차 판정 원문.
- 설계: `T40-MEASURE-DESIGN.md` §5′.1~10을 먼저 읽고 §0′·§2~6·§8·§9 대조.
- 계약: `docs/SPEC.md` §8.4 관련 G 항목, T14·T17·T38, `contracts/run-kinds.yaml`, `contracts/stages/read.yaml`, 승인 봉투 스키마.
- 도구: `t40_drive.py`, `t40_replay.py`, `t40_receipts.py`, `t40_metrics.py`, `t40_regress.py`, `t40_excerpts.py`, `t40_envelope.py`, `t40_lanes.workflow.js`, `T40-REGRESS-TABLE.md`.
- 실물: `engine/stages/read.py`, `engine/paths.py`, `engine/gitpin.py`, 레인 contract·file_adapter, `reader/lib/convergence.py`·`run_checks.py`, 기준 런의 원천·보고서·판정서·명세·요청·응답·로그·포인터·원장 대상 자료. 계측 법은 `git show`로만 읽었다.

**Owner 범위 재정 대상**

새 보증 요구는 없다. OB-1~4는 이미 채택된 T3·P5·P6·P7의 집행 문제다. 필요한 처분은 보증 범위 확대가 아니라, 이번 **재조립 방식 자체 재REVISE의 상신과 기존 명세 연결의 완결**이다.