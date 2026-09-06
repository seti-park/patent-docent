# 독립 감수 원문 — M1b 설계 도전 25차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v26 · 판정 REVISE(BLOCKER 1 · HIGH 4)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `7a311eb896cf267d43ca73350115bc4aa1834c89a8e1f8aef28863193a55a3f2` · 23106 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v25/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 감시 = STATUS EXIT= + FINAL 바이트(22:02 기동). 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `652f525` · 마커 3항 일치 · 메모 v26 sha256 `4ecf994b…` · v1~v25 + 스크립트 9종 + 회귀표 v6 + 자문 봉투·회신 1·2회차 + 재정 T42 동봉). 도전자가 첫 줄에 「⑽ ⓑ 발동 · 컴포넌트 D · 연속 REVISE 25회」 명기 — **재정 T42 이후 재조립 방식 자체에 대한 첫 REVISE**(T42 §2 재상신 기준 = 2회 연속 · 미달). 폐쇄 = **이전 89건 closed 72 · partially 17 · open 0**(NV-1 closed · NV-2·3 partially — IO 결함 경로 · 이전 partially 16건도 대부분 NW-1·NW-2 잔여). **B·C·E·F PASS**(20회 연속). 기준 런 재계수(163 · 56 · fact 3·implication 20·positioning 7·figure_note 10 · 45/5) 일치 확인 · `produced_at` 로 봉투 SHA 가 매번 달라진다는 반례는 불성립 확인.

**판정 = REVISE · 5건(BLOCKER 1 · HIGH 4) · 기각 0 · 발주자 귀책.** **NW-1 BLOCKER**: 재조립 sandbox 가 contracts·engine·reader 만 복사한 git 없는 트리라 러너의 원장 루트 판정이 `git-unavailable` 로 서고, 실측 linked worktree 의 `main-worktree-resolved` 와 어긋나 **정상 첫 LanePending 부터 post 대조가 실패** — 회귀표의 L 부모도 같은 복사 트리여서 이끼리 일치한 것이 동치의 증명이 아니었다. 반대로 정규화가 두 루트를 같은 `<ROOT>` 로 접어 포인터의 run_repo↔root 역할 교체가 지문에 남지 않았다. **NW-2 HIGH**: IO 결함을 만나면 대조기가 즉시 반환해 최종 산출물·원장·레인 트리·첫 관측 S 결속 검사를 생략 — 결함 런에서 S 축값 1.0→0.99 변조·소비 순서 역전·attempt 999·lane-log 비움이 전부 `terminated-incomplete` 로 통과하고 검증되지 않은 S 숫자가 출력됨 · 반대로 최초 patent.md 읽기 예외(try/finally 진입 전 · 종결 기록 없음)는 「finally 가 종결을 남긴다」는 잘못된 추상화로 오거부. **NW-3 HIGH**: R0/R1/R2 이름·선등록 커밋·좌석·partial/read 의 대응을 검사하지 않아 R1 ID 로 R0 법(좌석 max)에서 정직하게 완주한 결과가 R1 로 통과 · run.yaml 을 publish/ship 으로 바꾼 자료도 complete 수용. **NW-4 HIGH**: 봉투의 서식·판정서 지문 결속 4항만 검사하고 T40 §5 의 세 런 범위·Owner 문구·근거 위치를 검사하지 않아 `owner_quote="승인한 적 없음"` 봉투를 실제 소비시킨 런이 complete 로 통과. **NW-5 HIGH**: `--sandbox` 가 기존 디렉터리면 겹침 검사 없이 `rmtree` — `--sandbox run_dir` 이면 원본 36 파일이 먼저 지워진다(메모리 대역 확인).

**처분 = 전부 수용 → 설계 메모 v27 · 구동기 v8 · 지표 v27 · 재조립 대조기 v2 · 영수증 v2 · 회귀표 v7(101 사례).** NW-1 = sandbox 를 원본 주 작업 트리의 `git clone --shared --no-checkout` + 핀 커밋의 `git worktree add --detach` 로 실측과 같은 구조로 만들고(법 = 커밋 트리 · 루트 판정 사유 동일) · 정규화를 역할 토큰(`<RUN_REPO>`·`<MAIN>`)으로 · 회귀 픽스처도 같은 구조(정본 공유 클론 + R0 핀 worktree + 구동기 `seal_source`) · C73 역할 교체 거부. NW-2 = **면제 대신 재현** — 영수증의 traceback(지문 입증)에서 러너 호출 사슬을 읽어 sandbox 의 같은 자리(첫 IO 원시 호출)에 같은 예외를 주입하고, 출구 재독 halt 4행은 소견 문언의 OSError 를 러너 출구 재독 자리에 주입 → 결함 호출도 정상 규칙으로 대조 · 결함 뒤 호출도 재현(포인터 기록 매 호출 실패 L07 6/6) · 재현 안 되면 불일치 · 미종결 IO 예외(try 진입 전 · L19)도 같은 방식 · 입증 못한 숫자는 출력되지 않음(C74~C77). NW-3 = 선등록표 `t40_drive.registry()`(런 ID·핀·좌석 4·run_kind·봉투 권한·소재 지문) 하나로 run.yaml·HEAD·`git status` 법 실물·계약 좌석·영수증 법 HEAD 를 재조립 전에 대조(X01 · C72 · C79). NW-4 = 봉투 권한 전 검사(3 런 ∧ 이 런 · 육성 원문 · channel·located_at · target 이 현재 E 또는 S 에 결속 · 그 판정서가 exact-match 실패 0 ∧ 상신 축 ⊆ {element-set, tree-edges} ∧ 청구항 실패 0)(X02 · C78). NW-5 = `sandbox_prepare`: realpath 겹침·/tmp·심볼릭 링크 거부 · 소유 표식 `.t40-replay-sandbox` 없는 기존 디렉터리는 지우지 않음(S01·S02). **총괄 자기 발견 1(수리 중)**: 도면 정본화 디렉터리 `figures-normalized/` 에 도면 아닌 `MAPPING.md` 가 있어 현재 엔진의 `source.figures-manifest` 가 실패한다(기준 런 09-01 엔진은 20 도면만 실었다) → 실측 `source r0` 가 exit 1 로 멈출 자리 → 도면 20 파일 하드링크 전용 디렉터리 `figures-normalized-20/` 로 구동기 상수 변경 · 매니페스트 지문이 기준 런과 같음을 지표기가 대조. 처분 행·사유 = `docs/decisions/DISPOSITIONS.md` · `D-20260905-02-pdm2b-seats.md` **§17 추기 27**. 다음 = **M1b 26차 도전(지적 `NX-*`)**.

지적 열거 = NW-1, NW-2, NW-3, NW-4, NW-5

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · 연속 REVISE 25회)

v26의 재조립 오라클은 아직 실측의 판정 근거로 사용할 수 없습니다. **linked worktree에서 생성한 정상 기록을 거부하며, IO 결함 경로에서는 첫 관측 S·회차·소비 기록의 손상을 수용합니다.** 지정된 비교군의 법·좌석과 T40 봉투 권한을 재조립 밖에서 검증하는 의무도 빠져 있습니다.

외부 자문 2회차는 **회신·반영 완료** 상태입니다. T42의 방식 전환을 확인했으며 계수는 이어집니다. 이번은 T42 이후 재조립 방식 자체에 대한 첫 REVISE입니다. 실측 착수 요건은 충족하지 못했습니다.

**A — MY~NV 폐쇄 판정: closed 72 · partially 17 · open 0**

`closed`는 해당 지적의 구체적 결함이 수정됐다는 뜻입니다. `partially`는 기존 반례의 수정은 인정하지만, 그 지적이 요구한 상태별 검증 또는 오라클 적격화가 아래 반례 때문에 완결되지 않았다는 뜻입니다. 전건을 이번 좌석에서 물리적으로 재실행했다는 뜻은 아닙니다.

| 회차 | closed | partially | 잔여 근거 |
|---|---|---|---|
| MY | 1~5, 7~13 | 6 | 결함 경로의 최초 관측·임계값 결속, NW-2 |
| MZ | 1, 3~9 | 2 | 결함 경로의 S와 N/A 처분, NW-2 |
| NA | 1~7 | — | 기존 예외 경계·발주·발췌 수정 |
| NB | 1~3 | — | 진입·기록 실패 및 발주 사전검사 |
| NC | 1~3 | — | 실제 진입 실패 14, 읽기 경계·타입 검사 |
| ND | 1~2 | — | finding 형태·검증한 응답 바이트로 계수 |
| NE | 1~2 | — | 완주 변환 경계·finding 계약 |
| NF | 1 | — | 완주 run_id 결속 |
| NG | 1~2 | — | 명세 run_id·버전 표기 |
| NH | 1~2 | — | 입력 결속·baseline 적용 범위 |
| NI | 1~2 | — | 요청·원천 지문 결속 |
| NJ | 1 | — | 필수 원천 파일 |
| NK | 1 | — | 명세 필수 필드 |
| NL | 1 | — | 집계 대상 결측 |
| NM | 1~2 | — | 검사 행·원천 재독 경계 |
| NN | 1~2, 4 | 3 | 정상 대기의 오거부, NW-1·2 |
| NO | 3 | 1~2, 4 | 대기 오거부·손상된 미완 기록 수용, NW-1·2 |
| NP | 1~3 | — | 검사 집합·mismatch 소비·포인터 실패 구별 |
| NQ | 1~3 | — | 거부 행·원장 단독 종결·소견 대응 |
| NR | 1, 3~6 | 2 | 생성 방식은 개선됐지만 실제 실측 환경의 부모 적격화 미완, NW-1 |
| NS | 1, 3, 5~6 | 2, 4 | 회차·최초 관측 및 부모 적격화, NW-1·2 |
| NT | 1, 5 | 2~4 | 결함 경로의 회차·소비 기록 우회, 실측 환경 동치 미완 |
| NU | 1 | 2~4 | 결함 경로의 기록 결측, 봉투 권한, 회귀 대응표 |
| NV | 1 | 2~3 | 일반 경로는 거부하지만 IO 결함 경로에서는 순서·S 변조 통과, NW-2 |

특히 **MZ-3의 타 런 S는 exit 4로 거부**합니다. **NV-1은 실제 분해 `retry-1` 반향 거부를 별도로 생성해 확인**했습니다. 정직한 거부 기록은 수용하고 그 행을 삭제하면 거부했습니다. 이를 아래 NV-2·3의 잔여와 구별합니다.

**지적 목록**

**NW-1 · BLOCKER — 실제 worktree의 원장 루트 해석을 재현하지 못한다.**

좌표: 메모 §2·§5·§8ⓞ·§9 D①④, [t40_replay.py:67](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:67)의 sandbox 구성·`DRIVER`, [t40_receipts.py:25](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:25)의 `_walk`, [engine/paths.py:161](/home/laptop/projects/workspaces/pd-m1b-t40/engine/paths.py:161)의 `shadow_ledger_root`.

재조립은 `contracts·engine·reader`만 복사하고 Git worktree 구조를 구성하지 않습니다. `DRIVER`도 원장 루트 지정 없이 러너를 호출합니다. 따라서 실제 실측의 포인터는 `root_source=main-worktree-resolved`, Git 없는 재조립 트리는 `git-unavailable`입니다. 이 필드는 정규화 대상이 아니므로 **정상 첫 LanePending부터 post 대조가 실패**합니다.

실제 루트 판정·포인터 생성 함수를 유지하고 Git 메타데이터만 메모리 대입한 결과입니다.

```text
LINKED_FIRST_PENDING 4
call=1, diff=['10-read/lanes/shadow-ledger.json']
ROOT_SOURCES main-worktree-resolved git-unavailable
```

현재 L 부모와 재조립 트리는 모두 Git 없는 복사 트리입니다. 이끼리 일치하는 것은 §2의 linked worktree 동치를 증명하지 않습니다.

반대 방향의 문제도 있습니다. worktree와 주 작업 트리를 **모두 같은 `<ROOT>`로 축약**하므로 `run_repo`와 `root·ledger`의 역할을 뒤바꾼 포인터가 동일하게 정규화됩니다.

```text
NORMALIZED_ROOT_ROLE_SWAP_EQUAL True
```

이는 B-02가 요구한 **일대일 경로 대응과 법 트리·주 작업 트리 역할 보존**에 어긋납니다. `root_source`를 제거해서 첫 문제를 덮으면 안 됩니다.

**고치는 문안:** “법 worktree와 주 작업 트리·원장 루트를 서로 다른 역할로 결속하고, 격리된 재조립 환경에서 동일한 루트 판정 사유를 재현하며 실제 linked worktree 부모의 정상 대조와 역할 교체 거부를 적격화한다.”

**NW-2 · HIGH — IO 결함을 만나면 남은 증거 대조를 생략하여 손상을 합법적 미완으로 받는다.**

좌표: 메모 §2·§5·§9 D①⑤, [t40_replay.py:128](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:128)의 fault 반환, [t40_metrics.py:653](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:653)의 fault 수용.

IO 예외를 재현하지 못하면 대조기는 즉시 반환합니다. 그 뒤에 있는 **최종 원본 산출물·원장·레인 트리·첫 관측 S 결속 검사**는 실행되지 않습니다. 지표기는 `complete`만 금지하고, 앞 호출 재현과 종결 근거가 있으면 이 결과를 받습니다. IO 예외 분기는 해당 호출이 마지막 영수증인지도 요구하지 않습니다.

실제 T40 R0 ID·`partial/read`·base 법을 사용하고, 명세 기록에 `PermissionError`를 주입해 러너가 만든 부모에서 확인했습니다. 영수증은 수정하지 않았습니다.

| 대입 | 결과 |
|---|---|
| 무변조 결함 부모 | `0 · terminated-incomplete · early element-set=1.0` |
| S의 상세·보고 축을 함께 `1.0→0.99`, sidecar 갱신 | **`0 · terminated-incomplete · early=0.99 · first_early_bound=None`** |
| 마지막 통합 소비 행을 맨 앞으로 이동 | **`0 · terminated-incomplete`** |
| complete로 승격 시도 | **exit 4 — 승격 금지** |

추가로 같은 명세 기록 실패 부류에서 다음도 통과했습니다.

```text
FINAL_PROBE FULL_ATTEMPT_999 0 terminated-incomplete
FINAL_PROBE LOG_EMPTY 0 terminated-incomplete
```

따라서 **complete 승격 차단은 작동**합니다. 그러나 “손상은 exit 4”와 “결함 지표 N/A”는 작동하지 않습니다. 경고·`na`에 결함을 적으면서 검증되지 않은 S의 숫자를 그대로 출력합니다. 이것은 외부 영수증까지 함께 위조한 시험이 아닙니다.

오거부도 남습니다. 러너의 최초 `patent.md` 읽기에 IO 예외를 주면 `try/finally` 진입 전이라 종결 기록이 없을 수 있습니다. 이 실제 경로를 지표기는 다음 잘못된 추상화로 거부했습니다.

```text
IO 예외 영수증이 있는데 런이 종결되지 않았다
(러너 finally 는 예외 뒤 종결을 기록한다)
```

§2의 진입 예외·미관측 N/A 처분과도 맞지 않습니다. 출구 재독 halt 4행 서명 역시 현재 원본 판정서에서 읽은 약한 서명으로 동일한 대조 생략 경로에 들어갑니다.

**고치는 문안:** “IO 결함의 면제 범위를 입증된 실패 지점으로 제한하고 모든 호출 이력과 원본 영수증 결속·S를 별도 검증하며, 입증하지 못한 지표는 실제 N/A로 출력하고 finally 진입 전 예외를 종결 필수 경로와 구별한다.”

**NW-3 · HIGH — ‘같은 법으로 재현됨’이 ‘지정된 비교군의 법으로 실행됨’을 대신한다.**

좌표: 메모 §2·§5의 여섯 부류 ⑴, [t40_metrics.py:300](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:300), [t40_receipts.py:93](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_receipts.py:93)의 입력 필드.

실측 모드는 자기 트리를 법으로 삼지만, **R0/R1/R2 이름과 선등록 커밋·좌석·`partial/read`의 대응**을 검사하지 않습니다. `engine_commit·run_kind·partial_until`은 출력에 옮깁니다. baseline의 엄격한 내용 핀 검사는 이 대응 검사의 대체물이 아닙니다.

R1의 실제 런 ID와 `partial/read`를 사용하되 R0 법으로 정직하게 실행·기록한 결과입니다.

```text
R1_ON_R0_LAW 0 complete ad4c6c32ee7b601c1f110c7b3bfa04f31660c147
ACTUAL_R1_PROFILES:
decompose=max, ground-independent=high,
ground-dependent=low, synthesize=max
```

응답·로그·영수증의 사후 위조 없이 **xhigh 비교군이 아닌 결과가 R1으로 통과**합니다. 별도 메모리 시험에서는 `run.yaml`의 `run_kind/partial_until`을 `publish/ship`으로 바꾼 자료도 complete로 받았습니다.

이는 §5가 명시적으로 막겠다고 한 런·좌석·법 혼입입니다. 재조립할 때 현재 트리를 그대로 복사하면 이 잘못도 그대로 재현됩니다.

**고치는 문안:** “재조립 전에 run 이름·run_id·partial/read·선등록 커밋·법 내용·좌석 프로필의 R0/R1/R2 대응을 독립 검증하고 그 실행 입력을 호출 영수증에 결속한다.”

**NW-4 · HIGH — T40 대행 봉투의 권한 검사가 전 검사에 없다.**

좌표: 메모 §4·§5의 부류 ⑷·§8ⓔ, [t40_replay.py:105](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:105)의 봉투 공급, `t40_metrics.metrics`, `engine.stages.read.continue_envelope_state`.

봉투 원시 바이트와 영수증의 SHA가 같다는 검사는 있습니다. 러너의 일반 봉투 형식·승인·판정서 지문 검사도 있습니다. 그러나 **T40 §5의 세 런 범위와 Owner 문구·근거 위치를 검사하는 별도 전 검사**는 없습니다. B-02·B-03이 재실행 밖에 남기라고 지정한 의무입니다.

실제 T40 R0 부모의 허용 escalation 지점에서 봉투를 만든 뒤, 다음 두 필드만 바꾸고 **그 봉투를 실제 후속 호출에서 소비**시켰습니다.

```text
owner_quote = "승인한 적 없음"
located_at = "unrelated-note"

T40_R0_WRONG_AUTHORITY 0 complete partial
```

판정서 지문은 유지했고, 이후 영수증은 실제 소비된 잘못된 봉투를 그대로 기록했습니다. 재조립은 같은 봉투를 다시 받아 같은 완료를 만듭니다.

**고치는 문안:** “봉투 소비 전에 T40의 허용 런·차단 사유·Owner 원문·근거 위치·원본 E 지문을 독립 검증하고, 일반 봉투 유효성이나 재실행 일치를 대행 권한의 증명으로 사용하지 않는다.”

**NW-5 · HIGH — sandbox 경로가 원본과 겹치면 원본 증거부터 삭제한다.**

좌표: 메모 §5·§8ⓞ의 sandbox 격리, [t40_replay.py:76](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_replay.py:76).

대조기는 sandbox가 기존 디렉터리이면 곧바로 `shutil.rmtree(sb)`를 실행합니다. `/tmp` 접두 검사 외에 원본 런·법 트리·영수증·원장과의 겹침을 막는 검사가 없습니다.

`--sandbox`에 대상 `run_dir`을 지정하는 상황을 **메모리 파일시스템에서만** 실행했습니다.

```text
SANDBOX_INPUT_OVERLAP KeyError
ORIGINAL_SURVIVORS 0 OF 36
RUN_YAML_EXISTS False PATENT_EXISTS False
```

`KeyError`는 삭제 뒤 없는 파일을 읽으려던 메모리 대역의 예외입니다. 실제 디스크에서 삭제를 실행한 결과가 아닙니다. 중요한 것은 소스 복사 전에 원본 36개가 모두 제거되는 코드 경로입니다.

**고치는 문안:** “sandbox는 원본 런·리포·영수증·원장과 realpath 기준으로 분리된 전용 폐기 디렉터리임을 삭제 전에 검증하며, 소유 표식 없는 기존 디렉터리는 삭제하지 않는다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| **A 원장 정합·폐쇄·격** | **REVISE** | 재정 해석의 큰 틀은 유지됐으나 T40 §4·§5 및 T42의 검증 의무 집행이 NW-1~4에서 실패 |
| **B 계측 커밋 셋** | **PASS** | 부모·diff·절차 tree·16파일 numstat·실제 프로필·기준 요청 재렌더 확인 |
| **C 구동 v7** | **PASS — 메모리 검증 범위** | 공용 pre/post 호출, 시드 가드, 증거 실패 14, 예외 반환 경로, 분류·발주·조회·스냅샷 확인 |
| **D 지표·재조립·영수증·회귀표** | **REVISE** | NW-1~5 |
| **E 발췌 v4** | **PASS — 순수 함수 검증 범위** | 5→1 병합의 후보 재사용, 27단위, 표본 결정론·판정 불가 처분 |
| **F Workflow v4** | **PASS — Node 대체 실행 범위** | 사전 거부 12종 및 모델·effort 옵션 확인 |
| **G 결정 공백** | **REVISE** | 루트 대응·sandbox 경계·결함별 증거 면제와 N/A·비교군 및 봉투 권한 검사가 선결되지 않음 |

§8의 격은 대체로 맞습니다. ⓐⓑⓒⓓⓗⓙⓛⓜ은 재량, ⓔ는 T40 §5의 한정된 권한, ⓕⓖⓝ은 재정 문언 이행입니다. ⓘ의 청구항 단위와 ⓚ의 27단위·Owner 판독은 재정에서 오고 인덱스·후보 제시는 구현 재량입니다. ⓞ의 방식 선택은 T42에서 왔습니다. **정규화·sandbox·결함 서명을 구현 재량으로 분류했다고 해서 T42의 동치·격리 의무까지 재량이 되지는 않습니다.** G-12의 유보를 이번 source/read 운용으로 해결했다고 확대 해석하지 않았습니다.

**D의 요구별 판단**

- **B-02 성립 조건 넷:** 같은 코드·법의 재실행은 부분 충족입니다. 현재 법과 선등록 비교군의 동일성이 빠졌고(NW-3), 초기 환경의 Git·원장 루트가 다릅니다(NW-1). 호출·도착 기록은 정상 경로에서 대조하지만 IO 예외에서 중단됩니다(NW-2). 원시 응답·봉투는 SHA로 결속되지만 봉투 권한은 별도 검사가 필요합니다(NW-4).
- **비결정 요소:** `assemble_spec`의 `provenance.produced_at`, 원장 `recorded_at`, `_divergence`의 정렬 및 해시 시드 사용처를 확인했습니다. **조기 판정서에 produced_at이 있어 봉투 SHA가 매번 달라진다는 반례는 성립하지 않았습니다.** 이번에 직접 확인한 추가 환경 차이는 `root_source`입니다. 정규화의 역할 소거는 NW-1입니다.
- **응답 교체와 버전 미보존:** 응답 파일에 공백을 추가하고 소비 로그의 응답 SHA도 함께 바꾸되 영수증은 유지하면 exit 4였습니다. 다만 현재 구현은 과거 응답 버전을 보관하지 않으므로 **‘사후 교체’와 ‘호출 사이 버전 미보존’을 구별하지 못합니다.** 둘을 함께 거부하는 동작입니다.
- **영수증 자체:** 정상 경로의 S 변조·결함 영수증 삭제는 거부했습니다. 외부 영수증까지 전부 함께 위조한 자료는 선등록된 약속 밖입니다. 이번 NW-2~4는 그런 시험이 아닙니다. 정직한 영수증이 있어도 검사를 생략하거나, 잘못된 입력을 충실히 재현해서 통과합니다.
- **B-03 이행:** `early_loop_check·tail_chain_check·check_gate`와 잘못된 공통 회차 추정은 제거됐습니다. 반면 축·소견 재도출과 5/6/13·halt 4행의 생성 규칙은 여전히 전 검사에 남아 있습니다. 따라서 “생성 관계의 손 재구성을 모두 제거했다”는 판정은 불가합니다. 확인된 잘못된 잔존 추상화는 NW-2의 **IO 예외이면 finally가 종결을 남긴다는 조건**입니다.
- **B-04 범위:** 여섯 부류의 문언은 T40의 비교·권한·결측 처분을 포괄합니다. NW-2의 S·회차·로그 손상, NW-3의 잘못된 비교군, NW-4의 권한 없는 봉투를 “손으로 만든 변형”이라는 이유로 약속 밖에 둘 수 없습니다.
- **88행의 적격화:** 표는 **L 19 + C 69 = 88**입니다. 선택한 L01·L14·L17·L18과 C68~C71은 메모리 재실행에서 기대 결과를 냈습니다. 그러나 linked worktree 부모와 IO 결함 뒤 손상 조합을 덮지 않습니다. 또한 **C71은 L17의 최초 `ground-dependent/batch-1` 거부 행을 삭제**합니다. 표의 “NV-1 재시도 거부”와 정확히 같지 않습니다. 별도로 실제 분해 재시도 거부를 생성해 NV-1의 수정은 확인했습니다. 검사한 부모에서 판정서·로그를 손으로 제조하는 과거 방식은 발견하지 않았습니다.

**검증 경로와 출력**

모든 Python 메모리 시험은 사본 cwd에서 다음 형식으로 실행했습니다.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
/home/laptop/projects/patent-docent/.venv/bin/python - <<'PY'
# 감사 대상 모듈 import
# 파일 IO는 dict/BytesIO, DRIVER subprocess는 같은 본문의 메모리 exec로 대체
# 대상 함수 실행 및 결과 출력
PY
```

가상 경로 `/MEM`은 딕셔너리의 키일 뿐 실제 디렉터리를 만들지 않았습니다. 러너·계획기·어댑터·직렬화 본문은 유지했습니다. linked worktree 시험에서는 Git 메타데이터 조회를 대입하고 실제 루트·포인터 생성 함수를 실행했습니다.

| 검증 경로 | 마지막 출력 또는 결과 줄 |
|---|---|
| 최초 `cat .audit-sandbox; git rev-parse HEAD` 및 cwd 대조 | `652f525df46750dbf992390d97775f73be73c9c7` — path·pin·order 일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `4ecf994b0d3e55853a9162fd0722c43c6ac21a46df9a6f49b39462cf484bc569` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | **출력 없음** |
| `git ls-tree d4e6ca2 reader/procedure` 및 base 대조 | 양쪽 tree `d7717eb8750115a49e81ec7803790093b98c40ec` |
| `git diff --numstat 6d92cad origin/t40-base` | 마지막 `0 139 reader/procedure/HISTORY.md` — 절차 6파일만 변경 |
| `git diff --numstat origin/t40-base origin/t40-r1` 및 r2 | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- engine contracts reader`와 §0′ 대조 | 열거한 16파일의 증감 일치; 마지막 `90 35 reader/lib/run_checks.py` |
| Git의 read.yaml을 메모리로 공급해 `lane_profiles` 호출 | R0 `max/high/low/max`, R1 `xhigh/high/low/xhigh`, R2 종속 접지 `sonnet/high` |
| `bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | **exit 4**, `기준 런은 --law-tree <t40-base 체크아웃> 이 필수다…` |
| `git show origin/t40-base:<경로>`로 메모리 법 구성 후 기준 런 `metrics` | `BASELINE complete 163 56` |
| 기준 요청 6개 `render_request_md` | `REQUEST_RERENDER_BYTES_EQUAL 6` |
| 첫 S 부재·타 런 대입 | 각각 **exit 4**, `first-early 스냅샷이 없는데 완주 판정서가 있다…` / `조기 판정서 run_id ≠ 런…` |
| `classify` 반환·gate·pointer 대입 | `CLASSIFY 7 7` |
| `classify_after_exception` 대입 | `CLASSIFY_AFTER_EXCEPTION 4 / 4` |
| 실제 `enter` 실패·시드 미설정·영수증 쓰기 실패 | 각각 `EXIT_CODE=14` |
| `_record_exception` 증거 경로 실패 | `RECORD_EXCEPTION_FAILURE False` |
| `cmd_dispatch` 4회 및 `cmd_lanes` | `DISPATCH [0,0,0,15] LANES 0 UNCHANGED True` |
| 정상 재조립 부모 | `MEM_L01 0 complete … final_match=True, first_early_bound=True` |
| 실제 NV-1 재시도 거부 및 행 삭제 | `ACTUAL_NV1_RETRY_REJECT 0 terminated-incomplete` / `ACTUAL_NV1_DELETED 4` |
| 응답 원본+소비 SHA 동시 교체 | **exit 4**, `응답 원본 바이트가 영수증 지문과 다르다(교체 · 또는 호출 사이 버전 미보존)` |
| 발췌 `candidates/comp_texts_fn/sample_indices` | `MERGE_5_TO_1 ['M99','M99','M99','M99','M99']`; `EXCERPT_SELF_ACTUAL_SCORE 27 27` |
| Workflow 본문 Node 실행, `agent/pipeline` 대체 | `WORKFLOW_REJECT 12 / 12 RESULTS 1 1 1` |

base 부모는 `6d92cad`, r1·r2 부모는 모두 `ad4c6c3`으로 확인했습니다. base의 절차 증감은 순서대로 **1/1·35/3·4/2·9/1·2/1·0/139**입니다. `6d92cad→HEAD`의 `engine·contracts·reader` 차이는 없었습니다.

기준 런의 재계수는 명세 **163**, component **56**, 통합 응답 **fact 3·implication 20·positioning 7·figure_note 10**, 종속 접지 분포 **45/5**와 일치했습니다. 원장 조회는 사본의 `run_repo`, 재렌더 법은 메모리의 base 트리로 분리했습니다. 발췌 표본은 **CL-2·4·7·9·12·14·16·19·21·24**였으며, 5→1 병합을 자동 열위로 계수하지 않았습니다.

**[미검증]**

- 전체 88행의 물리 실행과 “약 7분”을 재측정하지 않았습니다. 제출 표·생성 코드를 읽고 위 선택 사례와 추가 반례를 메모리로 실행했습니다.
- 실제 worktree 생성·sandbox 쓰기·생산 원장 append·물리 봉인·심볼릭 링크·동시 파일 교체는 실행하지 않았습니다.
- 사본에 기준 런의 `figures-raw` 실물이 없어, 러너 시험의 도면 해시 열거만 `source-report.json`의 파일명·지문 목록으로 대체했습니다. 원본 도면 바이트의 봉인을 검증한 것은 아닙니다.
- 메모리 DRIVER 실행은 새 Python 프로세스의 완전한 import·환경 격리 시험이 아닙니다.
- 실제 Workflow 호출, transcript/journal의 실물 형태, 실제 모델·effort·파일 접근 격리, 비용·시간·메모리는 검증하지 않았습니다. pre 응답 SHA는 호출 직전의 파일 읽기이며, 실제 소비와 사이에 동시 변경이 없는지도 물리적으로 시험하지 않았습니다.
- 외부 스테이징 TXT·도면 원본은 읽지 않았습니다.

**읽은 파일**

- 상류: `ruling-20260905-05-T40.md` §1·§4·§5, `D-20260905-02-pdm2b-seats.md` §17 및 추기, T14·T17·T38, `docs/SPEC.md` 해당 조항, `run-kinds.yaml`, `read.yaml`, `approval-envelope.schema.json`.
- 도전 기록: `2026-09-06-astra-m1b-t40-measure.md` 및 `-v2.md`~`-v24.md`의 지적·폐쇄·처분 부분. 1·2·24차는 본문을 상세 대조했습니다.
- 제출물: 설계 v26, v25 및 필요한 이전판 대조 부분, 구동·지표·재조립·영수증·회귀·발췌·봉투·Workflow 8종, 회귀표, 자문 질문·회신 1·2회차, `bundle/ruling-T42.md`.
- 실물: `engine/stages/read.py`, `source.py`, `engine/stages/__init__.py`, `engine/lanes/{plan,contract,file_adapter}.py`, `engine/paths.py`, `gitpin.py`, `reader/lib/{convergence,run_checks,rules}.py`, 관련 스키마·렌더 코드, 기준 런의 원천 텍스트·보고서·요청·응답·판정서·명세·봉투·포인터 및 사본 원장.

파일·임시 파일·캐시는 쓰지 않았습니다. 정본 리포는 허용된 Python 인터프리터 외에 읽지 않았고 실측 레인도 시작하지 않았습니다.