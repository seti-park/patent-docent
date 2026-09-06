# 독립 감수 원문 — M1b 설계 도전 26차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v27 · 판정 REVISE(HIGH 3 · MED 1)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `383996af289e649aac343ae793bffc61e32913d647471e0dd7fd2c05063fba67` · 17134 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v26/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(23:30 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `8a02348` · 마커 3항 일치 · 메모 v27 sha256 `c8b9f249…` · v1~v26 + 스크립트 9종 + 회귀표 v7 + 자문 봉투·회신 1·2회차 + 재정 T42 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 26회」와 **「재정 T42 이후 재조립 방식 자체에 대한 두 번째 연속 REVISE — T42 §2 재상신 요건 충족」** 명기. 폐쇄 = **이전 94건 closed 87 · partially 7 · open 0**(NW-1 첫 호출 루트 불일치·역할 교체 = 수정 · NW-2 결함 경로 대조 생략 = 제거 · NW-3·4 closed · NW-1·2·5 partially = NX-1~3 잔여). **B·E·F PASS**(B 21회 연속 · C 는 이번 REVISE — 결함 재현에 필요한 영수증 이력 부족). 도전자가 스테이징 실물을 직접 읽어 `MAPPING.md` 판단과 20 도면 매니페스트 재현을 확인 · 선등록표 = 원장·메모 일치 · 회귀표 101 행(L 20 · C 77 · X 2 · S 2) 기록 확인(독립 재실행은 아님).

**판정 = REVISE · 4건(HIGH 3 · MED 1) · 기각 0 · 발주자 귀책.** **NX-1 HIGH**: traceback 호출 사슬 주입은 ⑴ 파일 객체 `write()` 중 실패를 재현하지 못하고(`open`·일부 `os.*` 만 감쌈) ⑵ 같은 행의 두 번째 호출 실패를 첫 호출에서 발화시켜 성공 접두부(첫 요청의 request.json·md)를 지우고 ⑶ `engine/paths.py` 마지막 행 생략 규칙이 위치를 합친다 — outcome 이 예외 종류만 대조하므로 다른 위치의 실패를 같은 재현으로 읽을 수 있다. **NX-2 HIGH**: 실제 OSError 문언은 경로가 문자열 중간에 들어가는데 JSON 정규화 `_sub` 는 접두 일치만 치환 → 원본·재생 판정서의 `findings[].expected` 불일치 · halt 문언 `.strip()` 이 공백을 바꿈 · 비JSON 분기는 무조건 `replace` 라 「경계 일치만」 약속과 다름. **NX-3 HIGH**: `sandbox_prepare` 가 realpath 해석 뒤 `islink` 를 봐서 표식 있는 대상을 가리키는 링크가 통과 · 영수증 `pre.responses` 의 좌표를 어휘 검증 없이 `join` 해 `../` 로 sandbox 밖에 응답을 쓸 수 있다. **NX-4 MED**: `check_axes_consistent`(NS-1·NT-1 축 상태·escalations·소견 재도출)가 B-03 대체 대상인데 「전 검사」로 남아 있다는 사실을 대응표에 명시하지 않았다.

**처분 = NX-2·3·4 수용(공학 · v28) · NX-1 은 재정 T43 대기.** NX-1 의 근본 선택 — IO 결함 런을 정확히 재현하려면 구동기가 실측 중 원시 IO 일지를 남겨야 하고(큰 수술), 대안은 결함 런을 재조립 불가(exit 4)로 두고 **재실측**하는 것(§5 의 결함 = N/A·재상신 경로와 같은 귀결 · 오라클에서 결함 재현·면제를 통째로 제거). T42 §2 요건(재조립 방식 자체 2연속 REVISE)에 따라 결정 브리핑 T43 으로 상신. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 28**. 다음 = **재정 T43 → v28 → M1b 27차(지적 `NY-*`)**.

지적 열거 = NX-1, NX-2, NX-3, NX-4

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 26회)

**재정 T42 이후 재조립 방식 자체에 대한 두 번째 연속 REVISE다. T42 §2의 재상신 요건이 충족됐다.** 외부 자문 대기 건은 없으며, 이번 판으로 실측을 시작할 수 없다.

공유 클론·linked worktree 구조와 비교군·봉투 권한 검사는 개선됐다. 그러나 **IO 결함의 위치·성공 접두부를 재현하지 못하고, 실제 OSError 문언은 정규화 뒤에도 달라지며, sandbox 밖 쓰기 경로가 남는다.**

**A — MY~NW 폐쇄 판정: closed 87 · partially 7 · open 0**

`closed`는 기존 지적의 구체적 결함이 수정됐다는 뜻이다. 이번 좌석에서 과거 반례 전부를 물리적으로 재실행했다는 뜻은 아니다. 회귀 오라클의 적격화 의무는 NX-1~3 때문에 부분 폐쇄로 남긴다.

| 회차 | closed | partially |
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

NW-1의 **첫 정상 호출 루트 불일치와 포인터 역할 교체**는 수정됐다. 다만 경로 정규화의 동치 문제는 NX-2로 남는다. NW-2의 **결함 경로 대조 생략**은 제거됐고, NV-3의 S 결속도 최종 공통 경로에 있다. 따라서 이전의 손상 수용 반례들은 닫혔지만, 결함 재현 자체는 완결되지 않았다.

§8의 격 구분은 타당하다. ⓞ에서 정규화 방식·필드 설계는 구현 재량이지만, **T42의 동치·격리와 T40의 비교군·봉투 권한 의무는 재량이 아니다.** G-12는 여전히 미집행이나, 이 발주의 `partial/read` 및 READ 뒤 운영 종료가 그 공백을 넘는 권한을 만들지는 않는다.

**NX-1 · HIGH — traceback 호출 사슬만으로는 실패한 IO와 성공 접두부를 재현할 수 없다.**

좌표: 메모 §2·§5·§9 C/D; [t40_replay.py:install_fault](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:85), `traceback_chain`, `replay`의 outcome 비교; `t40_drive.py:run_engine/finish_outcome`; 회귀 DRIVER.

실제 함수 본문에 파일·디렉터리 IO만 메모리 대역으로 공급해 세 반례를 확인했다.

- **쓰기 중 실패를 주입하지 못한다.** 실제 `engine.stages.write_json()`의 `json.dump()`가 호출하는 파일 객체 `write()`에서 OSError를 발생시켰다. 기록 사슬의 마지막은 `engine/stages/__init__.py:78:write_json`이었다. 같은 사슬을 `install_fault`에 주고 재실행하면 **정상 반환**한다. 주입기는 `open`과 일부 `os.*`만 감싸며 파일 객체의 `read/write/flush/close`는 감싸지 않는다.
- **같은 행의 두 번째 호출이 첫 번째에서 발화한다.** 실제 `FileLaneAdapter.dispatch()`에서 두 번째 접지 요청의 디렉터리 생성에 PermissionError를 주었다. 원본은 첫 요청의 `request.json`·`request.md`를 남겼다. 재주입은 첫 요청에서 발화하여 **두 파일 모두 남기지 않았다**. 사슬은 동일한 `dispatch:48 → write_request:80`이며 대상 경로·발생 차수가 없다.
- **`engine/paths.py`의 마지막 행 생략 규칙도 위치를 합친다.** `ensure_read_dirs()`의 두 번째 `makedirs(lanes)` 실패가 재생에서는 첫 번째 `makedirs(claim-trees)`에서 발화했다.

앞의 두 경우는 정직한 IO 이력을 재현하지 못해 거부한다. 세 번째처럼 파일 산출물이 모두 없는 경우에는 디렉터리 성공 접두부가 비교 대상에 없고, outcome도 **예외 종류만** 대조하므로 다른 위치의 실패를 같은 재현으로 읽을 수 있다.

L04~L08·L18·L19의 합성 주입은 대부분 상위 함수 진입에서 짧은 예외를 내므로 이 차이를 검증하지 않는다. 마지막 연쇄 예외 절을 선택하는 규칙 자체는 맞지만, 그 선택만으로 IO 연산·대상·발생 차수가 복구되지는 않는다.

**고치는 문안:** “결함 영수증에 원시 IO 연산·역할별 대상 경로·발생 차수·성공한 쓰기 접두부를 보존하고, 파일 객체 IO까지 정확히 한 번 재현하여 예외 위치·종류·문언과 post를 함께 대조한다.”

**NX-2 · HIGH — 경로를 포함한 실제 OSError 소견은 정규화 뒤에도 불일치한다.**

좌표: 메모 §5 정규화·halt 4행; [t40_receipts.py:normalize](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:44), `t40_replay.py:_translate`; `engine/stages/read.py:1986` 출구 재독.

러너의 실제 소견 생성식은 다음과 같다.

```python
actual = f"(읽을 수 없음: {exc})"
```

`PermissionError(13, "Permission denied", "/원본/.../patent.md")`를 사용하면 경로는 문자열 **중간**에 들어간다. `_translate`는 이를 sandbox 경로로 바꾸지만 JSON 정규화의 `_sub`는 문자열 전체가 루트와 같거나 **루트로 시작할 때만** 치환한다. 따라서 원본·재생 판정서의 `findings[].expected`가 달라진다.

메모리 대조 결과는 **`HALT_OSERROR_PATH_NORMALIZED_EQUAL False`**였다. 경로 없는 회귀 문구는 이 결함을 드러내지 않는다. halt 문언 추출의 `.strip()`도 예외 문언의 앞뒤 공백을 보존하지 않는다.

반대로 비JSON 분기는 무조건 `replace(r, tok)`를 사용하므로, 메모가 약속한 **경로 경계 일치만**이라는 규칙과도 다르다.

**고치는 문안:** “예외 경로와 문언을 구조화해 보존하고, JSON 소견 내부와 텍스트에도 동일한 경계 보존 치환을 적용하며 실제 errno·filename 포함 예외로 정규화 동치를 회귀한다.”

**NX-3 · HIGH — sandbox 경계 검사가 응답 복사 경로까지 보호하지 않는다.**

좌표: 메모 §5·§8 ⓞ; [t40_replay.py:sandbox_prepare](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:134), `replay`의 `pre.responses` 공급; `t40_receipts.py:load_receipts`.

두 경로를 메모리 대역으로 확인했다.

1. `sandbox_prepare`는 먼저 `realpath(sandbox)`를 구한 뒤 **해석된 대상에** `islink`를 호출한다. `/audit/alias → /audit/owned`이고 대상에 표식이 있으면 링크를 거부하지 않고 대상에 `rmtree`를 호출한다. 결과는 `None`과 `rmtree('/audit/owned')`였다. 보호 대상과의 realpath 겹침 거부는 정상 작동했다.
2. 영수증 `pre.responses`의 키를 레인 좌표로 검증하지 않고 `os.path.join(..., *lid.split("/"))`에 넣는다. `lid = "../"*8 + "victim"`을 공급한 실제 `replay` 본문은 sandbox `/audit/sb` 밖의 **`/audit/victim/response.json`에 쓰기를 시도**했다. 이 경로에는 별도의 포함 관계 검사가 없다.

두 번째 시험은 Git·러너·상태 오라클을 대체했으므로 전체 실측 자료의 최종 수용 증명은 아니다. **후속 대조 전에 sandbox 밖 `open(..., "wb")`에 도달한다는 경계 반례**다. 외부 영수증 동시 위조를 탐지 약속 밖으로 두더라도, 그 입력으로 sandbox 밖에 쓰는 것은 T42의 격리 의무 밖으로 뺄 수 없다.

**고치는 문안:** “입력 sandbox 경로의 링크를 해석 전에 거부하고, 영수증 좌표를 계약 어휘로 검증한 뒤 모든 복사 대상의 realpath가 sandbox 내부임을 쓰기 직전에 확인한다.”

**NX-4 · MED — B-03의 대체 완료 범위와 실제 잔존 구현을 구분하지 않았다.**

좌표: 메모 §5·§9 D②; `ADVICE-REPLY-2.md` B-03; [t40_metrics.py:check_axes_consistent](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:159).

`early_loop_check`·`tail_chain_check`·`check_gate`는 제거됐다. 그러나 B-03이 대체 대상으로 명시한 **NS-1·NT-1의 축 상태·escalations·소견 생성 관계 재도출**은 `check_axes_consistent()`에 남아 현재 E·S·full 모두에서 재조립 전에 실행된다. 단순한 스키마·타입 검사가 아니다.

이 잔존 함수에서 이번에 새로운 오판을 재현한 것은 아니다. 문제는 이를 “전 검사”로 부르면서 B-03의 대체 이행으로 묶는 것이다. T42가 점진 대체를 허용하므로, 아직 남긴 중복 구현을 정확히 밝히면 된다.

**고치는 문안:** “B-03 대응표에 NS-1·NT-1 생성 관계 재도출을 아직 유지한 중복 검사로 명시하고, 해당 경로의 재조립 적격화 뒤 대체한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| A 원장·폐쇄·격 | REVISE | 기존 94건 처분은 위 표. T42 동치·격리 미충족이며 재상신 요건 도달 |
| B 계측 커밋 | PASS | 부모·전체 팔 diff·절차 tree·blob·numstat·좌석 대응 일치 |
| C 구동 v8 | REVISE | 공용 호출·분류·증거 실패 14는 확인. 정확한 결함 재현에 필요한 영수증 이력은 부족, NX-1 |
| D 지표·재조립·회귀 | REVISE | NX-1~4. 101행 PASS 기록이 이 반례들을 덮지 못함 |
| E 발췌 v4 | PASS | 27 고정 단위·후보 제시·명시 채점·판정 불가 처분 유지, 메모리 자기 대조 일치 |
| F Workflow v4 | PASS | Node 대역에서 하드 지정·사전 거부·보고 분기 확인. 실호출 증거는 미검증 |
| G 결정 공백 | REVISE | T42 §2 재상신 필요. 결함 재현 실패를 임의 면제하거나 다른 실측값으로 대체할 수 없음 |

B에서 `6d92cad → t40-base`는 절차 6파일만 바뀌었다. R1·R2는 각각 `read.yaml` **2/2**이며 지정 좌석만 달랐다. 절차 tree는 기준 핀과 같은 `d7717eb8750115a49e81ec7803790093b98c40ec`이다. §0′의 `d4e6ca2 → 6d92cad` 계약·엔진·리더 **16개 비절차 파일 numstat도 전부 일치**했다. 최초 요청의 동일성과 재시도 `defects`에 영향을 주는 계약 차이를 구별한 문안은 타당하다.

C에서는 `run_engine`의 절대 `run_root`·`repo=W`·어댑터 `repo=W`, `seal_source`의 `partial/read`·도면 디렉터리 인자를 확인했다. 분류 결과는 **0/11/12/13/14**, 예외 종결은 **13**, 실제 `enter` 실패와 영수증 기록 실패는 **14**였다. 발주 상한 **15**·충돌 **14**는 무기록이며, `lanes` 조회도 무기록이다. 미수렴 보존 → 첫 유효 스냅샷 → 기존 스냅샷 유지도 확인했다.

D의 선등록표는 **세 런 ID·전체 핀·네 좌석·partial/read·봉투 육성·근거 위치·허용 축·소재 지문이 원장과 메모에 일치**했다. X01은 잘못된 선등록 핀, X02는 잘못된 Owner 문구로 거부된다는 회귀 기록도 해당 검사와 맞는다. C78은 권한 검사보다 먼저 영수증의 봉투 원본 지문에서 거부된다.

공유 클론의 공용 `.git`과 linked worktree는 러너 코드상 `main-worktree-resolved`를 낸다. 역할 교체는 정규화 지문에 남는다. 응답 원본과 영수증 지문이 다르면 거부하지만, **교체와 호출 사이 버전 미보존의 원인은 구별하지 못한다**. 현재 문언처럼 둘을 함께 보고하는 것이 맞다. S는 첫 관측 영수증의 `post.first_early`와 같은 호출의 E raw에 결속되며, 결함 경로의 조기 반환 면제는 제거됐다.

회귀표는 실제 **L 20·C 77·X 2·S 2 = 101행**, 전건 PASS로 기록돼 있다. 픽스처의 공유 클론·R0 핀 worktree·`seal_source`·대기 요청 공급 방식은 개선됐다. **러너가 만들 수 없는 L 부모는 이번 검토에서 확인하지 못했다.** 다만 반복 IO·파일 객체 IO·경로 포함 예외·링크·좌표 탈출을 시험하지 않아 오라클 적격화는 미완이다.

**검증 경로**

아래 `PY`는 모두 지정 사본에서 실행한  
`PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`이다. 메모리 시험은 `PY - <<'PY' … PY`로 실행했으며 파일을 만들지 않았다.

| 명령·직접 호출 경로 | 출력 인용 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `8a023489e130628f5d7d29d023450b16ade89bff` — path·pin·order·disposable 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `c8b9f2495b20c600c9af76277f4334f73bf2b0803450ae3626b52bdc5913e83e` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | 마지막 행 `0 139 reader/procedure/HISTORY.md` |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 `…r2` | 각각 `2 2 contracts/stages/read.yaml` |
| `git log -1 --format='%H %P'` 세 ref | base 부모 `6d92cad…`; 두 팔 부모 `ad4c6c3…` |
| `git show` 계약 → 실제 `lane_profiles()` → `registry()` 대조 | `REGISTRY r2 True True` — 세 런 모두 참 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | exit **4**, `기준 런은 --law-tree <t40-base 체크아웃> 이 필수다` |
| `git show origin/t40-base:reader/procedure/*`를 메모리 법으로 공급 → 실제 `metrics(..., baseline=True)` | `complete`, **163**, component **56**, synth **3/20/7/10**, 종속 anchor **45/5** |
| 비절차 법 `git diff` 별도 확인 | `LAW_NON_PROCEDURE_DIFF EMPTY` |
| 실제 metrics에 런·파일 IO 대역 공급 | `FIRST_EARLY_MISSING 4`; `FIRST_EARLY_DIGEST_MISMATCH 4` |
| 실제 `write_json` 쓰기 실패 → `install_fault` | `WRITE_FAULT_ORIGINAL=OSError REPLAY=NORMAL_RETURN` |
| 실제 `FileLaneAdapter.dispatch` 두 번째 요청 실패 → 재주입 | `SECOND_REQUEST_FAULT_REPLAY_FILES []` — 원본은 첫 요청 2파일 |
| `_translate` → `normalize` | `HALT_OSERROR_PATH_NORMALIZED_EQUAL False` |
| 포인터 역할 교체 → `normalize` | `ROLE_SWAP_DETECTED True` |
| `sandbox_prepare` 링크 입력·삭제 대역 | `None OPS [('rmtree', '/audit/owned'), ('mkdir', '/audit/owned')]` |
| 실제 replay 응답 복사 구간·메모리 IO | `TRAVERSAL_DEST_OUTSIDE_SANDBOX True WRITE_OBSERVED True` |
| 구동기 분류·진입·영수증 대역 | `RECEIPT_WRITE_FAILURE_EXIT 14` |
| 발주·조회·스냅샷 대역 | `DISPATCH_CAP 15 WRITES []`; `SNAPSHOT_NOCONV_THEN_FIRST_PRESERVED True True True` |
| `candidates`·`comp_texts_fn`·`sample_indices` | `EXCERPT_SELF 27`; **CL-2·4·7·9·12·14·16·19·21·24** |
| `node --input-type=module -`로 Workflow 본문, `agent/pipeline` 대역 | 정상 `claude-opus-5/max`; 잘못된 라벨·비정규 경로·중복·좌표 불일치는 호출 **0** |
| 회귀표 행·코드 AST 확인 | `REGRESSION_ROWS 101 {'L': 20, 'C': 77, 'X': 2, 'S': 2} ALL_RECORDED_PASS True` |

도면과 원천은 이번에 **스테이징 실물을 읽어** 검증했다.

| 대상 | 실측 |
|---|---|
| 원본 TXT | **298,572 B**, SHA `0c207938…c2228` |
| 실제 `source.canonicalize` 결과 | **298,507 B**, SHA `64d5d627…154e` |
| `figures-normalized-20/` | **20개**, 비도면 **0**, 매니페스트 `sha256:ffeb6fb122c9082f5c895135860456d36d8b305f150966e18fe366676dd12c34` |
| 기존 `figures-normalized/` | **21개**, 비도면 `MAPPING.md`, 매니페스트 `sha256:bb81e454…f0e0ba` |

따라서 `MAPPING.md`가 현재 `source.figures-manifest`에서 실패한다는 판단과, 20개 전용 디렉터리가 기준 매니페스트를 재현한다는 판단은 맞다.

**[미검증]**

- 실제 clone·worktree 생성, sandbox 쓰기, source 물리 봉인, replay/metrics 실측 CLI 및 회귀 101건 재실행은 하지 않았다. 회귀 PASS는 제출된 결과이며 독립 재현으로 표시하지 않았다.
- L04~L08·L18·L19의 실제 traceback 사본은 없었다. 러너의 원시 IO 자리와 실제 함수 본문의 메모리 반례로 검토했다.
- sandbox 탈출 시험의 Git·러너·상태 대역은 **쓰기 경계 검증용**이다. 완전한 실측 자료의 최종 수용 시험이 아니다.
- Workflow 실제 호출·transcript·journal·실제 모델 및 effort 증거는 확인하지 않았다.
- 과거 MY~NV 반례 전수 및 비용·시간 추정은 재실행·실측하지 않았다.

**읽은 파일**

원장 T40 §1·§4·§5, D-02 §17 처분과 추기, T14·T17·T38, SPEC 지정 G행, run-kinds·read 계약·승인 스키마를 읽었다. 설계 v27과 이전 판 관련 부분, MY~NW 도전·처분, 자문 1·2회차 관련 부분과 T42, 동봉 실행 스크립트·회귀표를 대조했다.

실물은 `engine/stages/read.py`·`source.py`·`__init__.py`, `engine/paths.py`, 레인 `plan.py`·`contract.py`·`file_adapter.py`, `reader/lib/convergence.py`·`run_checks.py`, 기준 런의 메타·원천·판정서·명세·요청·응답·원장 자료 및 지정 스테이징 원천·도면을 읽었다.

파일·임시물·캐시를 만들지 않았다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았다.