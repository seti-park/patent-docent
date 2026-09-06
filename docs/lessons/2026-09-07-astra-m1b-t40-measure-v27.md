# 독립 감수 원문 — M1b 설계 도전 27차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v28 · 판정 REVISE(HIGH 2 · MED 2)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-07 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `4c317998690644c053d37d0660942b4894f63245b024d4dddf438028867016ab` · 18553 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v27/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(00:12 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `318b296` · 마커 3항 일치 · 메모 v28 sha256 `38649eb1…` · v1~v27 + 스크립트 9종 + 회귀표 v8 + 자문 1·2회차 + 재정 T42·T43 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 27회」와 **「재조립 방식 자체를 다시 REVISE — T43 ② 자문 3회차 조건 충족」** 명기. 폐쇄 = **이전 98건 closed 88 · partially 10 · open 0**(NX-4 closed · NX-1~3 partially → NY-1~3). **재정 T43 ① A 자체는 T42·T40 §4·§5 와 정합**하다고 판정(면제가 아니라 재실측 · 새 ID·봉투 범위는 별도 재정 요구). **B·E·F PASS**(B 22회 연속). 회귀표 103 행 기록 확인 · 정상 6호출 메모리 실행에서 S 결속·재조립 6/6 성립 확인 · 선등록표 = 원장 일치 · 스테이징 실물(TXT·도면 20) 직접 확인.

**판정 = REVISE · 4건(HIGH 2 · MED 2) · 기각 0 · 발주자 귀책.** **NY-1 HIGH**: 대조기 `replay()` 가 `run.yaml#run_id` 를 검증하지 않고 `.worktrees/<run_id>` 에 붙여 `git worktree add` 를 부른다 — 지표기 경유면 선등록 검사가 먼저 거부하지만 **독립 CLI 진입에는 그 보호가 없다**(`/audit/victim` · `../../../victim` → sandbox 밖 목적지) · `_inside` 가 존재하지 않는 대상을 가리키는 dangling 링크를 건너뛰어 True. **NY-2 HIGH**: 포인터의 run_repo·root·ledger 에 리터럴 `<RUN_REPO>`·`<MAIN>/ledgers/shadow/screening.jsonl` 을 적은 변조가 정규화 뒤 정상값과 같은 지문이 되어 **complete·in-progress 모두 통과**(실제 러너→영수증→replay→metrics 메모리 연결로 재현 · 영수증 무변경) — 역할 토큰이 달라도 리터럴과의 충돌은 막지 못한다. **NY-3 MED**: `IO_FAULT_TYPES` 유한 목록이 `NotADirectoryError`·`InterruptedError`·`BrokenPipeError` 등 OSError 하위형을 누락 → 실제 결함이 「재실측」 대신 일반 「재조립 불일치」로 끝남(승격은 아님). **NY-4 MED**: §2 재실측 규약이 종결 근거를 「원장 행·포인터」 둘로 열거 — 러너 가드는 `convergence.json#phase=full` 단독도 종결로 봄(최종 원장 append 실패 런을 실제로 만들어 확인) → 같은 ID 재개 가능으로 오판할 자리.

**처분 = 전부 수용(공학 · v29) + 재정 T43 ② 대로 자문 3회차.** NY-1 = 대조기 진입에서 run_id 계약 어휘(`^[a-z0-9]+-[a-z0-9]+-[a-z0-9-]+$` · SPEC §7.1)·선등록 대응 검증 · worktree 목적지 포함 모든 쓰기 목적지의 `_inside` 를 dangling 링크까지(`os.path.lexists`/`realpath(strict)` 대체) 해석 · S04·C81. NY-2 = 포인터 원시 필드(run_repo·root·ledger)를 역할별 실제 절대경로(realpath)와 **정규화 전에** 대조(지표기 전 검사 + 대조기) · 토큰을 원문에 나올 수 없는 형태(`\x00ROLE:RUN_REPO\x00` 계열 또는 구조화 치환)로 · C82. NY-3 = 구동기 `run_engine` 이 `isinstance(exc, OSError)` 를 outcome 에 결속(`io_fault: true/false`) · 대조기는 그 필드로 처분 · 목록은 보조 · C83. NY-4 = 메모 §2 재실측 규약을 `_run_is_terminated` 세 근거(포인터 · 완주 판정서 · 원장 행)로 · 완주 판정서만 남은 런도 새 ID 재정. **자문 3회차 봉투**(T43 ② · ROUTING ⑽ ⓑ) = 재조립 오라클의 수렴 판정 — 27회차 루프에서 잔여가 「방식」인지 「구현 잔재」인지 · 게이트 종결 규약 ③ 적용 여부 · v29 잔여 프로브. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 30**. 다음 = **v29 → 자문 3회차 봉투(Owner 수동) → 회신 처분 → 28차(`NZ-*`)**.

지적 열거 = NY-1, NY-2, NY-3, NY-4

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 27회)

**재조립 방식 자체를 다시 REVISE한다.** T43 ②에 따라 자문 3회차로 갈 조건이 충족됐다. 현재 대기 중인 외부 자문은 없다.

**A — MY~NX 선행 폐쇄 판정: closed 88 · partially 10 · open 0**

`closed`는 기존 지적의 구체적 결함이 수정됐다는 판정이다. 과거 반례 전부를 이번 좌석에서 물리적으로 재실행했다는 뜻은 아니다.

| 지적군 | closed | partially |
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
| NR | 1, 3~6 | 2 |
| NS | 1~3, 5~6 | 4 |
| NT | 1~3, 5 | 4 |
| NU | 1~3 | 4 |
| NV | 1~3 | — |
| NW | 3~4 | 1~2, 5 |
| NX | 4 | 1~3 |

폐쇄되지 않은 이유는 다음과 같다.

- **NX-1·NW-2:** 부정확한 결함 주입·면제 코드는 제거됐다. 그러나 IO 분류와 재실측 종결 판정에 NY-3·4가 남는다.
- **NX-2·NW-1:** errno·filename이 문장 중간에 든 OSError의 동치는 수정됐다. 다만 정규화 토큰 자체와 실제 경로가 충돌한다(NY-2).
- **NX-3·NW-5:** 입력 링크·겹침·무표식 디렉터리·레인 `../` 거부는 개선됐다. 런 ID를 통한 sandbox 밖 Git 생성 경로가 남는다(NY-1).
- **NR-2·NS-4·NT-4·NU-4:** 픽스처 구조·호출 경계는 개선됐지만, 아래 반례를 놓치는 오라클의 적격화까지 완료됐다고 할 수 없다.
- **NX-4:** `check_axes_consistent`를 유지한 중복 검사로 명시한 처분은 확인했다.

**T43 ① A 자체는 T42·T40 §4·§5와 정합한다.** 결함 런에서 지표를 내지 않고 재실측하도록 한 재정이며, 동치가 입증되지 않은 자료를 비교표에 승격하는 면제가 아니다. 새 ID와 봉투 범위도 총괄이 임의로 확장하지 못하도록 별도 재정을 요구한다. 문제는 그 처분의 구현·운영 문안이 아직 완결되지 않았다는 것이다.

§8의 격 구분도 유지할 수 있다. 다만 ⓞ의 구현 재량은 **T42의 동치·격리 의무와 T40의 비교군·봉투 권한 의무를 완화하지 못한다.**

**NY-1 · HIGH — 독립 대조기가 런 ID로 sandbox 밖 worktree 생성을 요청한다.**

좌표: 메모 §5·§6·§8 ⓞ; [t40_replay.py:replay](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:117), 145행의 `worktree add`, `_inside`.

`replay()`는 `run.yaml#run_id`를 검증하지 않고 다음 경로에 붙인다.

```python
os.path.join(".worktrees", run_id)
```

실제 함수 본문에서 파일·Git 실행만 메모리 대역으로 바꿔 확인했다.

| run_id | Git에 전달되는 생성 목적지 |
|---|---|
| `/audit/victim` | `/audit/victim` |
| `../../../victim` | `/audit/victim` |

sandbox는 `/audit/sb`였다. **Git 생성 요청 전에 이탈을 거부하지 않는다.** 시험은 목적지를 관측한 뒤 Git 대역에서 중단했으며 실제 생성은 하지 않았다.

지표기를 경유하면 선등록 검사가 이 입력을 먼저 거부한다. 그러나 메모와 대조기 자체가 제공하는 **독립 CLI에는 그 보호가 없다.** 영수증 동시 위조를 탐지 범위 밖으로 두더라도, 입력으로 sandbox 밖에 쓰는 것은 T42 격리 의무 밖으로 뺄 수 없다.

별도 함수 시험에서는 `_inside('/audit/sb', '/audit/sb/dangling')`도, 해당 경로가 **존재하지 않는 sandbox 밖 대상을 가리키는 링크**인 조건에서 `True`였다. `exists()`가 거짓인 링크를 건너뛰고 부모부터 계산하기 때문이다. 이는 helper 수준 반례이며, 정상 핀의 전체 실행에서 해당 링크가 생성된다는 주장은 아니다.

**고치는 문안 한 줄:** “독립 대조기 진입에서 런 ID·선등록 대응을 검증하고, Git worktree 목적지를 포함한 모든 쓰기 목적지의 전체 realpath를 dangling link까지 해석하여 sandbox 내부임을 쓰기 전에 확인한다.”

**NY-2 · HIGH — 실제 경로와 리터럴 정규화 토큰이 같은 지문이 되어 포인터 손상을 수용한다.**

좌표: 메모 §5 역할 보존 정규화; [t40_receipts.py:_sub/normalize](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:41); [t40_metrics.py:포인터 검사](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:385).

포인터의 다음 세 필드만 바꿨다.

| 필드 | 정상값 | 변조값 |
|---|---|---|
| `run_repo` | 실제 런 worktree 절대경로 | `<RUN_REPO>` |
| `root` | 실제 주 작업 트리 절대경로 | `<MAIN>` |
| `ledger` | 실제 원장 절대경로 | `<MAIN>/ledgers/shadow/screening.jsonl` |

정상값은 정규화하면서 오른쪽 문자열이 되고, 변조값은 이미 그 문자열이므로 그대로 남는다. 포인터 전 검사는 문자열 타입만 요구한다.

**실제 `read.run` → 영수증 → `replay` → `metrics` 본문을 메모리 파일시스템으로 연결해 수용을 재현했다.** 영수증은 변경하지 않았다.

```text
정상 부모: complete · replay.ok=True · replayed=6/6 · first_early_bound=True
포인터 변조: complete · replay.ok=True · replayed=6/6 · first_early_bound=True
```

첫 `LanePending` 상태에서도 같은 변조가 `in-progress`, `replay.ok=True`로 통과했다. 따라서 complete 전용 검사로도 닫히지 않는다.

기존 C73의 `run_repo↔root` 교환은 계속 잡힌다. **서로 다른 역할 토큰을 쓰는 것만으로 리터럴과의 충돌까지 방지되지는 않는다.**

**고치는 문안 한 줄:** “원시 포인터 경로를 역할별 실제 절대경로와 먼저 대조하고, 원문 리터럴과 충돌하지 않는 구조화 표현으로 정규화한다.”

**NY-3 · MED — IO 예외 목록이 `OSError` 계열 일부를 재실측 처분에서 누락한다.**

좌표: 메모 §2·§5; [t40_receipts.py:IO_FAULT_TYPES](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:25), `is_io_fault`; [t40_drive.py:run_engine](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_drive.py:279).

`is_io_fault()`는 예외 이름의 유한 목록만 검사한다. 다음은 모두 `OSError` 하위형이지만 `False`다.

```text
NotADirectoryError
InterruptedError
BrokenPipeError
```

사본의 일반 파일 아래를 디렉터리처럼 읽는 **실제 읽기 연산**에서도 `NotADirectoryError`를 얻었고, 분류 결과는 `False`였다.

실제 러너의 최초 `patent.md` 읽기에 `NotADirectoryError`를 주고 영수증·지표기까지 연결한 메모리 시험 결과:

```text
ACTUAL_IO_DISPOSITION NotADirectoryError is_io=False EXIT 4 REMEASURE_TAG False
```

대조기는 이 결함을 재실행하려다 일반적인 **“재조립 불일치·손상·교체…”**로 끝났다. T43이 정한 **“IO 결함 런·재실측”** 처분이 아니다.

이 반례에서 **complete 승격은 발생하지 않았다.** 지적은 IO 판별 및 처분 누락이며, 누락된 모든 예외가 정상 수용된다고 주장하지 않는다.

**고치는 문안 한 줄:** “구동기가 실제 포착한 예외의 `isinstance(exc, OSError)` 분류를 영수증에 결속하고, 대조기는 그 분류로 OSError 하위형 전부에 exit 4·재실측 처분을 적용한다.”

**NY-4 · MED — §2 재실측 규약이 종결 근거 셋 중 완주 판정서를 빠뜨린다.**

좌표: [메모 §2](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/T40-MEASURE-DESIGN.md:60); `engine/stages/read.py:_run_is_terminated`, `run`의 최종 원장 append.

메모는 새 ID가 필요한 종결 기록을 **“원장 행·포인터 terminated”**로 열거한다. T38 ③과 실제 가드는 **`convergence.json#phase=full` 단독 실재**도 종결로 판단한다.

실제 러너의 마지막 `append_screening_ledger`에 PermissionError를 주어 해당 상태를 만들었다. 판정서를 손으로 제조한 부모가 아니다.

```text
pointer_terminated False
ledger_exists False
full_phase full
```

실제 가드와 재호출 결과:

```text
GENERATED_APPEND_FAULT_GUARD (True, 'convergence.json')
GENERATED_APPEND_FAULT_REENTRY StageError True
```

이 결함 런은 지표기에서 정상적으로 **exit 4·IO 재실측** 처분을 받는다. 그런데 §2에 열거된 두 근거만 확인하면 같은 ID로 다시 돌 수 있다고 오판하게 된다.

**고치는 문안 한 줄:** “증거 보존·이동 전에 `_run_is_terminated`의 세 근거로 종결을 판정하고, 완주 판정서만 남은 경우도 새 런 ID와 T40 §5 범위 재정을 받은 뒤 재실측한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| A 원장·폐쇄·격 | REVISE | T43의 처분 자체는 정합. T42 동치·격리와 재실측 문안에 잔여 |
| B 계측 커밋 | PASS | 부모·전체 팔 diff·절차 tree·numstat·좌석 대응 일치 |
| C 구동 v8 | REVISE | 공용 호출·분류·기록 실패 14 확인. IO 분류 결속은 NY-3 |
| D 지표·재조립·회귀 | REVISE | NY-1~3. 정상 자료와 변조 자료를 모두 수용하는 반례 재현 |
| E 발췌 v4 | PASS | 무변경 확인. 27 고정 단위·후보 제시·표본·판정 불가 처분 유지 |
| F Workflow v4 | PASS | 무변경 확인. Node 대역에서 하드 지정·사전 거부·보고 분기 확인 |
| G 결정 공백·실행 분기 | REVISE | NY-4의 재실측 분기 수정 필요. T43 ②의 자문 3회차 조건 발동 |

B에서 `6d92cad → t40-base`는 절차 디렉터리 **6파일만** 변경됐다. R1·R2는 각각 `contracts/stages/read.yaml` **2/2**이며 지정한 좌석 값만 바뀌었다. 절차 tree는 `d7717eb8750115a49e81ec7803790093b98c40ec`이다. §0′의 `d4e6ca2 → 6d92cad` **비절차 16파일 numstat도 일치**했다. 엔진·계약 변경이 재시도 여부와 `defects` 요청에 영향을 줄 수 있다는 한정은 타당하다.

C에서 `run_engine`의 절대 `run_root`·`repo=W`·어댑터 `repo=W`를 확인했다. 정상 자료의 메모리 실행 순서는 **read-a 대기 → read-b 대기 → 조기 상신 → 접지 대기 → 통합 대기 → 정상 종결**이었다. 분류 0·11·12·13·14, 진입 실패 14, 영수증 기록 실패 14, 발주 상한 15·충돌 14의 무기록, `lanes` 무기록, 스냅샷 보존을 확인했다.

D의 추가 판단은 다음과 같다.

- **sandbox 구조:** 공용 Git 디렉터리가 `sandbox/main/.git`이고 linked worktree의 git-dir가 별도이므로, 러너 코드상 사유는 `main-worktree-resolved`다. 법 HEAD·파일 지문·run.yaml 결속도 확인했다. 실제 Git 생성은 실행하지 않았다.
- **정규화:** JSON·텍스트의 errno/filename 포함 문언 동치와 앞뒤 공백 보존은 통과했다. `/audit/main2`, `x/audit/main/y` 같은 비경계 접두도 보존됐다. 잔여는 NY-2다.
- **원본 응답:** 응답과 소비 로그를 함께 바꿔도 외부 영수증의 원시 SHA가 그대로라면 대조에서 걸린다. “교체”와 “호출 사이 버전 미보존”의 원인은 현재 자료만으로 구별하지 못하며, 둘을 함께 표시하는 현재 문언은 맞다.
- **첫 S:** 정상 6호출 메모리 실행에서 최초 관측 영수증·해당 호출 E 원시 바이트·S 결속이 성립했다. 부재 인자와 sidecar 불일치는 각각 exit 4였다.
- **선등록·봉투:** `registry()`의 세 ID·핀·네 좌석·partial/read·소재 지문·봉투 육성·근거·허용 축은 메모와 T40 §5에 일치한다. 봉투 권한 검사가 재조립 뒤에 있어도 지표 반환 전에는 실행된다. X01·X02의 기록된 거부 사유도 각각 잘못된 핀·권한 없는 문구에 대응한다.
- **B-03:** `early_loop_check`·`tail_chain_check`·`check_gate`는 제거됐다. 축·소견 중복 검사의 잔존은 명시됐다. 정적 정합·파생 필드 검사도 남아 있으므로, 전체 생성 관계 검사의 대체 완료로 읽어서는 안 된다.
- **B-04:** 여섯 부류의 범위는 T40의 비교 목적을 덮는다. 이번 sandbox 이탈과 정규화 충돌은 외부 영수증까지 모두 위조해야 생기는 반례가 아니다.

회귀표는 **103행 = L 13·F 7·C 78·X 2·S 3**, 전건 PASS로 기록돼 있다. `CASES()` 구성과도 일치한다. 정상 부모의 빈 lanes·대기 요청 공급·공용 구동 함수·공유 클론/핀 worktree 구조는 개선됐다. 이번 검토에서 러너가 만들 수 없는 L 부모는 추가로 확인하지 못했다.

다만 **F 부모에서 파생된 C**는 다음 10건이다.

`C01, C08, C09, C10, C29, C69, C74, C75, C76, C77`

특히 **C74~C77은 변조 여부와 무관하게 F 자체가 재실측 거부 대상**이다. 그 PASS는 결함 자료의 지표 비출력을 증명하며, S·순서·회차·로그 변조를 각각 탐지했다는 증거는 아니다. C75의 “결함 호출도 주입 재현” 설명도 현재 코드와 맞지 않는다.

**검증 경로**

모든 명령의 cwd는 지정 사본이었다. 아래 `PY`는 지정 인터프리터에 `PYTHONDONTWRITEBYTECODE=1`을 적용한 것이며, 재조립 메모리 시험에는 시작부터 `PYTHONHASHSEED=0`도 적용했다.

| 명령·직접 검증 경로 | 출력 인용 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | 마지막 줄 `318b296aa62cbb775c3dd0f9b5a51ecdbd054343` — path·pin·order·disposable 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `38649eb1e5fd171bb501a291bcaa66c42f1fa62379dd936fd05e08f6c2c6dc98` |
| `git diff --numstat 6d92cad origin/t40-base` | 마지막 줄 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 `…r2` | 각각 마지막 줄 `2 2 contracts/stages/read.yaml` |
| `git log -1 --format='%H %P'` 세 ref | base 부모 `6d92cad…`; 두 팔 부모 `ad4c6c3…` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --stat origin/t40-base HEAD -- engine contracts reader ':!reader/procedure'` | 빈 출력 |
| `git diff --stat 8a02348 HEAD -- bundle/t40_drive.py bundle/t40_excerpts.py bundle/t40_lanes.workflow.js` | 빈 출력 — v27 제출 시점 대비 세 실행본 무변경 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit **4**, 마지막 줄 `기준 런은 --law-tree … 이 필수다` |
| `git show origin/t40-base:reader/procedure/<파일>`을 메모리 법으로 공급 → 실제 `metrics(..., baseline=True)` | `complete`; **163**, component **56**, synth **3/20/7/10**, anchor **51/5·45/5** |
| `PY - …` 실제 러너·영수증·재조립·지표기, 메모리 파일시스템 | 정상·포인터 변조 모두 `complete`, `6/6`, S 결속 참; 마지막 줄 `END_ACTUAL_READ_REPLAY_METRICS_VIRTUAL_FS` |
| `PY - …` 실제 `replay()`의 Git 목적지 관측·`_inside`·토큰 충돌 | sandbox 밖 `/audit/victim`; 토큰 충돌 `True`; 마지막 줄 `END_BOUNDARY_PROBES_NO_DISK_WRITES` |
| `PY - …` 실제 러너 최종 원장 append 실패 | 가드 `(True, 'convergence.json')`, 재호출 `StageError`; 마지막 줄 `END_GENERATED_FULL_ONLY_IO_FAULT` |
| `PY - …` 구동기 분류·발주·영수증·예외 기록 대역 | `RECEIPT_FAILURE 14`, 상한 `15 WRITES []`, 충돌 `14 WRITES []`; 마지막 줄 `END_DRIVER_BOUNDARIES` |
| `PY - …` 실제 스냅샷·지표 입력 경계 | 부재 인자·지문 불일치 각 **4**, 보존 `True True True`; 마지막 줄 `END_FIRST_EARLY_PROBES` |
| `PY - …` `candidates`·`comp_texts_fn`·`sample_indices` | 자기 대응 **27**; 표본 **CL-2·4·7·9·12·14·16·19·21·24** |
| `node --input-type=module -` — Workflow 본문, `agent/pipeline` 대역 | 정상 `claude-opus-5/max`; 잘못된 라벨·경로·중복·좌표는 호출 **0**; 마지막 결과 `dropped:1` |

외부 스테이징 실물도 읽기만 하여 확인했다.

| 대상 | 직접 실측 |
|---|---|
| 원본 TXT | **298,572 B**, SHA `0c207938…c2228` |
| 실제 `source.canonicalize` 결과 | **298,507 B**, SHA `64d5d627…154e` |
| `figures-normalized-20/` | **20개**, 비도면 **0** |
| 실제 도면 매니페스트 | `sha256:ffeb6fb122c9082f5c895135860456d36d8b305f150966e18fe366676dd12c34` |
| `seal_source` 인자 대역 | 절대경로·`repo=W`·`partial/read`·20 도면 디렉터리 일치 |

**[미검증]**

- 실제 clone·worktree 생성, 디스크 sandbox 재실행, source 물리 봉인, 회귀 103건 전건 재실행은 하지 않았다. 제출된 회귀 PASS를 독립 재현으로 표시하지 않았다.
- 메모리 통합 시험은 파일 IO와 Git 환경·법 지문 조회·자식 프로세스 경계를 대체했다. 러너·계획기·어댑터·영수증·재조립 비교·지표 본문은 실제 함수를 사용했다. 부모 제조에서만 기준 응답을 새 요청 지문에 맞췄으며, 재조립에서는 응답 바이트를 재작성하지 않았다.
- dangling link는 helper 대역 시험이다. 실제 링크 생성이나 sandbox 밖 쓰기는 실행하지 않았다.
- Workflow 실호출, 실제 모델·effort transcript, 물리 문맥 격리, 비용·시간 추정은 검증하지 않았다.
- 과거 MY~NX 반례 전부를 이번에 재실행하지 않았다. 폐쇄표는 원문·처분·현재 구현·이번 직접 시험을 종합한 판정이다.

**읽은 파일**

- 원장·처분: T40 §1·§4·§5, D-20260905-02 §17, T14·T17·T38, T42·T43.
- 선행 감수: 1·2·25·26차 원문과 3~24차 지적 표제·처분·폐쇄 기록.
- 설계·자문: 메모 v28·v27 대조, `ADVICE-REPLY-2.md`, 회귀표와 생성 코드.
- 실행본: `t40_drive.py`, `t40_replay.py`, `t40_receipts.py`, `t40_metrics.py`, `t40_regress.py`, `t40_excerpts.py`, `t40_envelope.py`, Workflow 본문.
- 계약·러너: SPEC 지정 행, run-kinds·read 계약·승인 봉투 스키마, `engine/stages/read.py`·`source.py`·공통 함수, `engine/paths.py`, 레인 plan·contract·file_adapter, convergence·run_checks 및 검증 시 적재된 규칙·스키마.
- 실물: 기준 런 메타·원천·판정서·명세·요청·응답·원장, 지정 스테이징 TXT와 도면 20개, 사본 마커·Git tree/blob/diff.

파일·임시물·캐시를 만들지 않았고, 실측 레인은 시작하지 않았다.