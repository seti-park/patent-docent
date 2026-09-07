# 독립 감수 원문 — M1b 설계 도전 31차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v33(집행 자리·자원 대장 · 재정 T45·T46) · 판정 REVISE(HIGH 1 · MED 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `992f5c7baa295e5886736f1cb6df26f3d7b2049fc1464f54af22055329f3c1ea` · 18985 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v31/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(재정 T46 ③ · 저작 좌석 astra xhigh 와 같은 모델임을 Owner 인지 하에 유지 · 발주문에 고지) · `setsid nohup` · 감시 = Monitor STATUS EXIT= + FINAL 바이트(12:09 기동 · 12:4x 종료 · USAGE input 6,031,586(cached 5,651,200) · output 28,876). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `619e76b` · 마커 3항 일치 · 메모 v33 sha16 `e39a03405f1cf8f7` · 대장 `58bb52a611e43213` · 스크립트 10 + 회귀표 v12(137) + 지문 파일 + 판단 목록 J01~J34 + ruling T44~T46 + 자문 3·4회차 · bundle 66 파일). **이번 기동 = 재정 T45 ① 직접 효력** · 판정 방법 = T45 ② 양방향 대조(ⓐ 대장 행 → 코드 · ⓑ 코드 → 대장 · ⓒ 의무 공백) + 남은 자리 목록 + 진행도 3수.

**판정 = REVISE · 5건(HIGH 1 · MED 4) · 기각 0 · 발주자 귀책(저작 = astra xhigh · 발주·검수 = 총괄).** 지문 13개 전부 일치 · 정적 대조 `mismatch=0 unmet=0 unreviewed=0` 재현 · 심사 대상 ① 충족 · ②~⑤ 미충족 · **갈래 ⑴ 5 · ⑵ 0 · ⑶ 0 · 대장 누락 반례 0**(모든 지적이 기존 SITE 행의 집행 불일치) · **게이트 진행도(행 단위) `mismatch=12 unmet=12 unreviewed=0`** — 이것이 T45 ③ 진행도의 **첫 기준선**이다(저작기의 정적 0/0/0 과 비교하지 말 것 · 게이트 명시). **OC-1 HIGH · P5 · SITE-52·60·63**: 구동기 출력 파일(retire 의 `dispatch-counter.json` · 첫 스냅샷 sidecar `.json.sha256`)이 호출 전 존재하는 심볼릭 링크면 어휘·조상 링크·realpath 검사 없이 `"w"` 로 열어 허용 범위 밖에 쓴다(메모리 관측 `RETIRE_COUNTER_ALIAS exit=0 protected_changed=True`) — 고정 디렉터리·dispatch 목적지 검사가 개별 출력 파일을 덮지 않는다 · S18~S20 은 「쓰기 성공 + 외부 대상 변경」을 시험하지 않는다. **OC-2 MED · P7 · SITE-21·24·27·30·33**: `git_head` None · `git status` rc 128 · RunPaths 계약 적재 PermissionError · 원장 루트 해석 실패 · 절차 문서 렌더 PermissionError · `Rules.load` PermissionError 가 전부 `die()` 기본 `부적격` — 조회 불능과 유효 조회 결과 불일치가 분리되지 않아 환경 수리 대상 런이 결과 표 부적격 행으로 들어간다. **OC-3 MED · P7 · SITE-40**: `replay()` 가 하위 프로세스 returncode·`io_fault` 를 환경 판별에 쓰지 않고 stdout JSON 을 영수증과 바로 비교 → import 실패·sandbox IO 가 `mismatch`(검수 중 sandbox 실패 = 검수 불능이어야). **OC-4 MED · P7 · SITE-44**: `requests_present()` 에 역할 인자·`onerror` 가 없어 `os.scandir` PermissionError 가 빈 집합 → `mismatch` · S17 시험 대상에서 빠짐. **OC-5 MED · T3·P7 · SITE-15·57**: `cmd_seal` 이 `manifest_write` 의 PermissionError·후보 판독 ValueError 를 분류 없이 traceback exit 1 로 · §5′.2 「pending/.next 는 봉인 전 거부」 의무가 `cmd_seal → manifest_write → evidence_files` 경로에 없음(`require_attempt_ready` 미호출 · 메모리 관측 `SEAL_pending ready=rejected exit=0 manifest_writes=1`).

**T44 판정(재정 T44 §1 ② + §3 보정 · T45 ③) = ⓐ 도출 누락 0 ✓ · ⓑ 새 보증 요구 0 ✓ · ⓒ 갈래 전부 ⑴ ✓ → 자동 기동 조건 충족.** 진행도 3수의 「두 회차 연속 비감소」 조건은 이번이 첫 측정(12/12/0)이라 판정 불가 — 32차 결과와 비교한다. 세 회차 연속 축(28~30차 T3·P5·P6·P7)은 T45 ③ 로 재검토 신호로 격하됐고 T45 ① 처분(대장)이 집행됐으므로 별도 상신 대상이 아니다.

**처분 = 전부 수용(공학) · 이행 = v34 저작(좌석 = gpt-6-astra xhigh 3차 발주 · Owner 09-07 10:0x 지정 좌석 계승 · 같은 작업장 `pd-author-t40v33`).** 수정 문안(도전자 문안 그대로) — OC-1 = 「counter·스냅샷·sidecar 를 포함한 구동기 출력마다 어휘·조상 링크·realpath 를 첫 부작용 전에 검사하고, 허용 자원 밖의 목적지는 무쓰기 거부한다」 · OC-2 = 「조회 불능과 유효한 조회 결과의 불일치를 분리하고, 계약·절차·규칙 적재 및 원장 루트 해석 실패는 발생 경계에서 `검수 불능` 으로 전달한다」 · OC-3 = 「하위 프로세스 실패·결과 판독 불능·sandbox IO 를 outcome 동치 비교 전에 `infeasible` 로 분리하고, 정상적으로 얻은 실행 결과만 영수증과 비교한다」 · OC-4 = 「`requests_present` 에도 자료·환경 역할, 오류를 삼키지 않는 메타 조회·walk 경계를 적용하고 sandbox 호출에서 환경 역할을 전달한다」 · OC-5 = 「seal 진입에서 pending/.next 를 봉인 쓰기 전에 거부하고, 후보 판독·봉인 기록 실패를 §5′.4 의 명시적 처분과 종료 코드로 반환한다」. **총괄 교훈**: 저작자(astra xhigh)의 대장은 「함수·selector 의 존재」를 배선으로 적었고 게이트는 「그 자리의 실행 의미」를 대조했다 — 대장 행의 「검증 근거」 열에 회귀 사례 ID 가 있어도 그 사례가 **그 오류 경로**를 덮는지는 별개(OC-4 · S17 에 `requests_present` 부재). 발주자 오류 누계 197 → **202**(OC 5).

지적 열거 = OC-1, OC-2, OC-3, OC-4, OC-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 31회)

마커의 path·pin·order와 detached HEAD `619e76beb0f803a54a210028b84eb33c16518c7c`를 먼저 확인했다. 메모·대장·스크립트 9종·회귀표·지문표 **13개 모두 발주문의 sha16과 일치**했다. 지문 불일치 지적은 없다.

정적 대조는 `rows=63 extracted=1139`, 마지막 줄은 **`mismatch=0 unmet=0 unreviewed=0`**이었다. §5′.11 요약 표도 JSON에서 생성한 표와 정확히 일치했다. 그러나 함수의 존재와 배정이 보호·오류 처분의 집행까지 보증하지는 않았다.

아래 시험은 실제 함수 또는 해당 함수의 AST 원문 분기를 실행하되 파일 쓰기·복사·삭제·하위 실행은 메모리 대역으로 받았다. **디스크에 반례를 만들거나 실측·재조립을 실행하지 않았다.**

**OC-1 · HIGH · 갈래 ⑴ P5 집행 위반 · SITE-52·60·63 — 구동기 출력의 파일 별칭을 통과시켜 허용 범위 밖에 쓴다.**

좌표: 메모 §5′.2·§5′.3·§5′.11; [snapshot_first_early](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:232), [cmd_retire의 counter 읽기](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:450), [counter 쓰기](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:497).

두 자원에서 같은 단절을 확인했다.

- **retire의 counter:** 정상 evidence 디렉터리 안의 `dispatch-counter.json`만 외부 JSON을 가리키는 링크로 둔다. `require_attempt_ready()`는 이 파일을 검사하지 않는다. `cmd_retire()`는 링크를 따라 읽고, 보존·pending 기록 뒤 같은 경로를 `"w"`로 열어 대상 런의 키를 제거한다. 메모리 파일시스템에서 **외부 대상 변경 → 런 삭제 → current=2·pending 해제 → exit 0**까지 진행했다.
- **첫 스냅샷 sidecar:** `first-early-r0.json`은 없고 `.json.sha256`만 외부 파일을 가리키는 링크인 경우다. `snapshot_first_early()`는 sidecar에 경계 검사를 적용하지 않고 `"w"`로 연 뒤 정상 반환한다.

관측:

```text
RETIRE_COUNTER_ALIAS exit=0 protected_changed=True
SNAPSHOT_SIDECAR_ALIAS … /memory/protected/ledger.txt … returned=normal
```

이는 동시 교체나 hardlink 반례가 아니다. 호출 전에 존재하는 심볼릭 링크다. 고정 디렉터리 검사와 dispatch의 목적지 검사는 **retire·snapshot의 개별 출력 파일**을 보호하지 않는다.

S18은 dispatch 경계를 시험한다. S19·S20은 retire의 IO 실패와 pending 생존을 시험하지만, **쓰기 자체는 성공하면서 외부 대상을 바꾸는 경우**를 시험하지 않는다. 후속 봉인 거부도 이미 발생한 쓰기를 되돌리지 못한다.

**수정 문안:** “counter·스냅샷·sidecar를 포함한 구동기 출력마다 어휘·조상 링크·realpath를 첫 부작용 전에 검사하고, 허용 자원 밖의 목적지는 무쓰기 거부한다.”

**OC-2 · MED · 갈래 ⑴ P7 집행 위반 · SITE-21·24·27·30·33 — 법·환경 실패를 자료 부적격으로 분류하는 호출부가 남았다.**

좌표: 메모 §5′.4·§5′.11; [metrics의 법 조회](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:375), [종결 가드·원장 해석](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:438), [요청 재구성·렌더](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:668), [최종 검사 적재](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:782).

| 자리 | 공급한 환경 실패 | 실제 처분 |
|---|---|---|
| SITE-21·24 | `git_head()`가 조회 실패로 `None` 반환 | `부적격`: 다른 법으로 실행했다고 표시 |
| SITE-21·24 | `git status` returncode 128·인덱스 읽기 실패 | `부적격`: 법이 핀과 다르다고 표시 |
| SITE-27 | `RunPaths`의 계약 적재 `PermissionError` | `부적격`: 종결 판정 불가 |
| SITE-27 | 원장 루트 해석 함수의 실패 | `부적격`: 원장 루트 해석 실패 |
| SITE-30 | 법 절차 문서를 읽는 렌더러의 `PermissionError` | `부적격`: 요청 재구성·렌더 실패 |
| SITE-33 | `Rules.load()`의 `PermissionError` | `부적격`: READ 검사 재실행 불능 |

앞의 두 경우는 `metrics()` 진입부터 메모리 실행했다. 뒤의 네 경우는 원문의 `try/except` AST를 그대로 실행했다. 모두 exit 4였지만 접두가 잘못됐다.

공통 결속 함수의 `BindingInfeasible`이나 SITE-25의 정상적인 법 적재 포장은 이 호출부들을 구제하지 못한다. 앞에서 `die()`가 기본 `부적격`으로 종료한다. 따라서 환경을 수리하고 재검수해야 할 런이 **결과 표의 부적격 행**으로 들어가거나, 총괄이 자유문을 읽고 처분을 다시 선택해야 한다.

S05·C79는 조회의 무변경성과 실제 법 변경을, S08·C95는 특정 스키마 경계를 지지한다. 위 호출부 전체의 오류 역할을 지지하지는 않는다.

**수정 문안:** “조회 불능과 유효한 조회 결과의 불일치를 분리하고, 계약·절차·규칙 적재 및 원장 루트 해석 실패는 발생 경계에서 `검수 불능`으로 전달한다.”

**OC-3 · MED · 갈래 ⑴ P7 집행 위반 · SITE-40 — 하위 Python의 환경 실패가 재조립 불일치가 된다.**

좌표: 메모 §5′.4·§5′.11; [replay의 하위 실행 결과 처리](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:286).

`replay()`는 하위 프로세스의 `returncode`와 재실행 결과의 `io_fault`를 환경 판별에 사용하지 않는다. stdout 마지막 줄을 JSON으로 읽은 뒤 영수증의 outcome과 바로 비교한다.

결속된 원본 영수증은 정상 `pending`인 상태에서 다음 두 결과를 각각 공급했다.

```text
CHILD_IMPORT_FAILURE disposition=mismatch replayed=0
CHILD_SANDBOX_IO disposition=mismatch replayed=0
```

첫 경우는 import 실패·returncode 1·빈 stdout, 둘째는 sandbox에서 발생한 `PermissionError`·`io_fault=true`다. 둘 다 `호출 결과가 영수증과 다르다`로 반환됐다.

이 IO는 **검수 중 sandbox의 실패**이므로 `검수 불능`이어야 한다. 원본 실측의 IO 증거가 아니므로 T43 재실측 근거도 아니다. SITE-40은 오류 경로에 “환경 실패”를 적어 놓고 처분을 `부적격` 하나로 배정했다. F 7건은 원본 실측의 IO 결함 시험이어서 이 경계를 대신 증명하지 못한다.

**수정 문안:** “하위 프로세스 실패·결과 판독 불능·sandbox IO를 outcome 동치 비교 전에 `infeasible`로 분리하고, 정상적으로 얻은 실행 결과만 영수증과 비교한다.”

**OC-4 · MED · 갈래 ⑴ P7 집행 위반 · SITE-44 — 요청 열거 함수는 환경 오류를 빈 집합으로 삼킨다.**

좌표: 메모 §5′.4·§5′.11; [requests_present](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:187), [replay의 요청 집합 대조](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:299).

`responses_present()`와 `lane_tree_state()`에는 역할 인자와 `onerror=walk_error`가 있지만, 같은 행의 `requests_present()`에는 둘 다 없다. 실제 `os.walk()`가 사용하는 `os.scandir()`에 `PermissionError`를 공급하면:

```text
REQUEST_SCAN_PERMISSION signature=(lanes_root) returned=[] raised=False
```

요청이 있는 sandbox에서 이 결과를 받으면 호출부는 환경 실패를 인식하지 못하고 영수증과 요청 집합이 다르다는 `mismatch`를 낸다.

SITE-44가 인용하는 S17은 `artifact_state`, `lane_tree_state`, `ledger_rows`, `responses_present`, `_bind_first_early`를 시험한다. **`requests_present`는 빠져 있다.** “동일 채집 함수 사용”이라는 구조 논거 역시 오류를 보존한다는 증거가 아니다.

**수정 문안:** “`requests_present`에도 자료·환경 역할, 오류를 삼키지 않는 메타 조회·walk 경계를 적용하고 sandbox 호출에서 환경 역할을 전달한다.”

**OC-5 · MED · 갈래 ⑴ T3·P7 집행 위반 · SITE-15·57 — 봉인 진입점의 상태 검사와 실패 처분이 배선되지 않았다.**

좌표: 메모 §5′.2의 시도 자원 행·§5′.4·§5′.11; [cmd_seal](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:413), [manifest_write](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:380).

첫째, `manifest_write()`의 `PermissionError` 또는 후보 판독의 `ValueError`를 `cmd_seal()`이 그대로 내보낸다. CLI 외곽에도 분류 경계가 없다. 대장은 두 행의 처분을 `검수 불능`으로 적었지만 관측은 다음과 같다.

```text
SEAL_FAILURE PermissionError escaped=PermissionError disposition_prefix=False systemexit=False
SEAL_FAILURE ValueError escaped=ValueError disposition_prefix=False systemexit=False
```

즉 CLI에서는 분류된 처분 대신 traceback·exit 1로 끝나는 경로다.

둘째, §5′.2는 **“pending 또는 .next는 봉인/자료 소비 전에 거부”**한다고 정했다. 그러나 `cmd_seal → manifest_write → evidence_files`에는 `require_attempt_ready()`가 없다. 같은 메모리 입력에 대해 준비 검사는 거부하면서 봉인은 성공했다.

```text
SEAL_pending ready=rejected exit=0 manifest_writes=1
SEAL_.next ready=rejected exit=0 manifest_writes=1 staging_listed=False
```

후속 `metrics()`·`bind_receipts()`의 pending 거부는 살아 있다. 이 지적은 pending 자료가 최종 검수를 통과한다는 주장이 아니다. **중도 상태에서 봉인을 쓰지 않는다는 선행 의무와 봉인 실패의 코드 처분**이 해당 진입점에 없다는 지적이다.

S11·C86은 봉인 집합과 봉인 후 변조를 시험한다. S19·S20의 재진입 시험 대상은 read·retire·검수이며 seal은 아니다.

**수정 문안:** “seal 진입에서 pending/.next를 봉인 쓰기 전에 거부하고, 후보 판독·봉인 기록 실패를 §5′.4의 명시적 처분과 종료 코드로 반환한다.”

**남은 자리와 진행도**

63행 모두 행의 의미·담당 함수·selector·호출부·근거를 대조했다. 미심사 행은 **없음**이다. 이는 63행의 모든 상태 조합을 디스크에서 실행했다는 뜻은 아니다.

| 구분 | SITE |
|---|---|
| 미충족 — OC-1 | 52·60·63 |
| 미충족 — OC-2 | 21·24·27·30·33 |
| 미충족 — OC-3 | 40 |
| 미충족 — OC-4 | 44 |
| 미충족 — OC-5 | 15·57 |
| 대조 완료·추가 지적 없음 | 01~14·16~20·22~23·25~26·28~29·31~32·34~39·41~43·45~51·53~56·58~59·61~62 |

**심사 진행도: `mismatch=12 unmet=12 unreviewed=0`**

계수 단위는 중복을 제거한 **대장 행**이다. `mismatch`는 보호·역할·선후·처분의 의미 불일치가 있는 행, `unmet`은 그로 인해 필수 의무가 미충족인 행이다. 위 12행은 두 조건에 모두 해당한다.

ⓑ 역방향에서는 등재된 자리와 별개인 **대장 누락 반례는 0건**이다. 발견한 별칭·외부 함수·DRIVER 결과·상태 경로의 문제는 기존 행의 ⓐ 집행 불일치와 ⓒ 의무 공백으로 집계했다. 정적 계수와 다른 이유는 selector 존재·필수 문자열 검사가 실행 의미를 판정하지 않기 때문이다.

**심사 대상 ①~⑤**

| 대상 | 판정 | 근거 |
|---|---|---|
| ① 도출의 완전성 | 충족 | T40·T42·T43에서 P/T·절차 의무로의 새 도출 누락 없음. T45의 심사 방법과 T46의 수용 판단 유지 |
| ② 신뢰·입력·부작용 경계 | 미충족 | 핀·선등록·기준 소재 대응은 확인했으나 출력 파일 별칭과 봉인 상태 경계가 미완 |
| ③ 기제의 집행과 합성 | 미충족 | OC-1~5. 공용 함수가 있어도 모든 자원이 그 경계를 거치지 않음 |
| ④ 검증 근거 | 미충족 | 137건의 구성·표는 일치하지만 위 자원·호출·오류 경로를 지지하지 못함 |
| ⑤ 미충족 상태의 처분 | 미충족 | 환경→부적격, 오류→빈 집합, 봉인 오류→미분류 예외 경로가 남음 |

**갈래 집계: ⑴ 5건 · ⑵ 0건 · ⑶ 0건.** J01~J34의 설계 선택을 다시 열지 않았다.

**A 폐쇄표**

`closed`는 기존 지적의 구체적인 결함이 닫혔다는 뜻이다. 같은 성질 전체의 충족을 뜻하지 않는다.

| 기존 지적 | 판정 | 근거·잔여 |
|---|---|---|
| MY-1~13·MZ-1~9·NA-1~7·NB-1~3 | closed | 기존 상태·계수·발췌 연결 유지, 기준값·발췌 메모리 재현 |
| NC-1~3·ND-1~2·NE-1~2·NF-1·NG-1~2 | closed | 기존 원장·결측·발췌 정의와 해당 기제 유지 |
| NH-1~2·NI-1~2·NJ-1·NK-1·NL-1 | closed | 요청·응답·원천 지문 연결 유지 |
| NM-1~2·NN-1~4·NO-1~4·NP-1~3 | closed | 상태·소비 적격성·생성 관계 검사 유지 |
| NQ-1~3·NR-1~6·NS-1~6·NT-1~5 | closed | 거부 행·종결·재시도·별도 법 트리 검사 유지 |
| NU-1~4·NV-1~3 | closed | 비대칭 재시도·접지 그룹·첫 관측 결속 유지 |
| NW-1~5·NX-1~4·NY-1~4 | closed | 기존 루트·정규화·권한·경로·T43 반례의 폐쇄 유지 |
| NZ-1·2·4 | closed | SITE-21의 무잠금 조회, SITE-02·09의 선판별, SITE-58~63의 보존·시도 분리. S05~07·C84~85·S19~20 |
| NZ-3 | partially | 처분 필드는 있으나 OC-2~5의 역할 전달이 미완 |
| NZ-5 | closed | 문언상 제외 범위와 공용 봉인·결속 검사 유지. SITE-02~06 |
| OA-1 | closed | 두 소비 진입점의 공용 결속. SITE-02·03, C88·89·93 |
| OA-2 | closed | 삭제 전 런·증거 보존과 대조. SITE-59·63, S06·19·20 |
| OA-3 | partially | 기존 자료 형태·스키마 경계는 닫힘. 남은 역할 분류는 OC-2~5 |
| OA-4 | closed | 후보 선검사와 봉인·대조·소비 공통 집합. SITE-01·04~06, C91·92·94·S09·11 |
| OA-5 | closed | import 전 캐시 억제 유지. SITE-17~20·40·55, S10 |
| **OB-1** | **closed** | **SITE-02·03·10·13·63 — C93·C86~89·S19.** `bind_receipts()` 성공 뒤에만 T43 선판별 |
| **OB-2** | **closed** | **SITE-01·04~06 — C94·S11·C91~92.** 후보 열기 전 검사와 선택 집합 일치 |
| **OB-3** | **closed** | **SITE-07~10 — C95~97·S12.** 지정했던 봉투 스키마·run.yaml 중첩형·halt findings·영수증 IO 경계 연결 |
| **OB-4** | **closed** | **SITE-11 — S13.** evidence 전체·dispatch·retired·LANE_DIR 보호를 표식보다 먼저 적용 |

합계는 **closed 114 · partially 2 · open 0**이다. MY~NY 102건은 30차 폐쇄표와 현행 기제의 연결을 대조한 것이며, 옛 반례 102개를 모두 재실행하지 않았다. C97은 먼저 다른 정합 검사에서 거부될 수 있으므로, 해당 타입 가드의 근거에는 함수 본문 대조도 사용했다.

**검증 경로**

모든 명령은 지정 사본에서 실행했다. 아래 `〈PY〉`는 실제 사용한 공통 접두다.

```text
PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python -B
```

| 명령·시험 | 확인 결과·마지막 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | path·pin·order 일치, 마지막 줄 `619e76beb0f803a54a210028b84eb33c16518c7c` |
| `sha256sum`으로 지정 13파일 대조 | 전부 지정 sha16 일치. 후반 재확인도 동일 |
| `〈PY〉 bundle/t40_sites.py --ledger bundle/T40-SITES-LEDGER.json --code bundle/` | exit 0, `mismatch=0 unmet=0 unreviewed=0` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | procedure 6파일만. 마지막 행 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` | `2 2 contracts/stages/read.yaml` |
| 같은 명령의 `origin/t40-r2` 대조 | `2 2 contracts/stages/read.yaml` |
| `git ls-tree`·`git show`로 세 핀과 계약 대조 | 지정 blob·부모 관계 일치, registry 좌석 R0·R1·R2 모두 일치 |
| `〈PY〉 bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit 4, `처분=부적격 · 기준 런은 --law-tree … 필수다…` |
| `〈PY〉 -` — `git show origin/t40-base:<경로>`의 법 62파일을 메모리에 제공하여 기준 `metrics()` 실행 | `MEMORY_BASELINE_DONE writes=0 law_files=62` |
| `〈PY〉 -` — `t40_excerpts` import 후 출력만 메모리로 수집 | `EXCERPTS_MEMORY_DONE outputs=2 actual_writes=0` |
| `〈PY〉 -` — 실제 retire·seal·replay 함수와 오류 분기의 메모리 대역 시험 | `RETIRE_ALIAS_PROBE_DONE actual_writes=0`, `ROLE_BOUNDARY_PROBES_DONE actual_writes=0`, `LAW_BRANCH_PROBES_DONE actual_writes=0`, `REQUEST_SCAN_PROBE_DONE actual_writes=0`, `PRODUCER_BOUNDARY_PROBES_DONE actual_writes=0` |
| 회귀 `CASES()` 구성과 납품 표 직접 계수 | `HARNESS_CASES 137 {'L': 13, 'F': 7, 'C': 95, 'X': 2, 'S': 20}` · `TABLE_CASES 137 FAIL_rows=0` |

기준 런은 **complete·항목 163·component 56**, 종류별 **56/56/14/20/7/10**, 통합 응답 **fact 3·implication 20·positioning 7·figure_note 10**, 조기·완주 attempt **1·1**로 재현됐다. 발췌는 **27단위**, 종속항 24개에서 인덱스 **`[0,2,5,7,10,12,14,17,19,22]`**의 10표본이었다.

F 파생 C는 **14건**이며, 부적격 8건 `C08·09·10·29·69·83·88·89`, 재실측 6건 `C74~77·84·85`라는 정정도 확인했다.

**[미검증]**

- 137건 회귀의 실제 디스크 재실행. 납품 표와 하네스·주입 경계를 읽었으며, 이번 독립 실행 결과로 주장하지 않는다.
- 외부 스테이징 TXT·도면 실물. 기준 런의 봉인 원문·source report와 선등록값의 대응까지 확인했다.
- 실제 Workflow의 model·effort transcript와 Owner 발췌 판정. 아직 실행할 단계가 아니다.
- 동시 파일 교체·hardlink·모든 런타임 효과의 완전한 증명. OC-1은 이 한계에 기대지 않는 기존 심볼릭 링크 반례다.

읽은 파일은 T40·T42·T43·T44·T45·T46 재정, D-02 §17 관련 추기, 자문 4회차 회신, 28~30차 보고서 관련 원문, 메모 v33의 지정 절과 대장 63행, J01~J34, 지정 스크립트 9종·회귀표·지문표, SPEC 지정 항목, run-kinds/read 계약·승인 봉투 스키마, `engine/stages/read.py`의 실행·종결 경로, `engine/paths.py`, 레인 contract·file_adapter, convergence·run_checks, 기준 런의 지표 입력 산출물이다. 핀 법 62파일은 별도로 바이트 대조했다.

이번에는 도출 누락·새 보증 요구 없이 갈래 ⑴만 남았다. 다음 처분에는 **T44 §3의 T45 ③ 보정**을 적용한다. 위 행 단위 3수를 다음 심사에서도 같은 기준으로 비교해야 하며, 저작기의 정적 `0/0/0`과 감소 여부를 비교해서는 안 된다. **실측 착수 조건은 충족되지 않았다.**