# D-20260903-01 — `/claude-api prompt-audit` 상신 · Owner 승인 · 집행 (총괄 저작)

**지위.** 총괄 문서(원장이 아니다). 재정 원장 = `ruling-20260903-01-T33.md`. 아래 §1 은 Owner 에게 낸 상신(감사 보고) **원문 전문**이며, 산출 시점의 좌표(`~/projects/workspaces/patent-docent-session-drafts/PROMPT-AUDIT-2026-09-03*`)를 그대로 든다. 제안 diff 두 벌은 그 디렉터리에 있고, 적용된 부분은 이 리포와 `~/.claude/agents` 의 git 이력이 든다.

## §0 처분·집행 순서

| 발견 | Owner 처분 | 집행 | 시점 |
|---|---|---|---|
| F7 (`CLAUDE.md` §6 → HANDOFF 포인터 + 관문표 · 구 본문 `docs/IMPLEMENTATION-HISTORY.md` 이동) | 승인 | `5b84fb7` | 즉시 |
| F3~F6 (`~/.claude/agents` 4파일 — effort 표 정합 · description · 폐지 흔적 · 금지 절 응축) | 승인 | agents 리포 커밋 `11d8707`(파일 4) · LEDGER 등재는 병렬 세션이 L-048 을 라이브로 쓰고 있어 **보류** — L-050 으로 등재 예정(nd-magnet 세션의 L-049 뒤) | 즉시 |
| F1·F2 (`reader/procedure/*.md` 이력 이동 · 현재형 재서술 · `HISTORY.md` 신설) | 승인 | **골든 manifest `47e437c` 뒤 · `8259075` 로 집행됨** | 이연 후 집행 — 아래 사유 |

**F1·F2 를 뒤로 미룬 사유(총괄 재량 · 사후 확인 대상 — [확인 2026-09-03 · 재정 T34 ⓓ]).** 설계 §2.8 의 골든 생성 명령 블록은 `git diff --quiet "$BASE" HEAD -- engine contracts reader` 를 사전조건으로 건다 — 경로 기준이라 `reader/procedure/*.md` 개정도 걸린다. F1·F2 를 지금 main 에 올리면 B-0 의 정상 경로 시험(같은 경로 무변경 확인)과 골든 생성이 그 자리에서 실패한다. 값(8,190칸)에는 영향이 없는 개정이지만 사전조건은 설계 PASS 판의 문언이므로 고치지 않고, **순서**를 바꾼다: B-0 병합 → 골든 생성·커밋 → F1·F2 적용. 승인은 났고 diff 는 검증되어 있다(worktree 적용 · 관문 6종 · pytest 591).

**함께 드러난 것 — 발주자 오류(B-0 발주문).** B-0 단위 시험의 「clone 의 `engine contracts reader` 가 `99fad78` 이후 무변경이 아니면 fail」 조항(총괄이 쓴 것)은 설계의 **생성 시점** 사전조건을 **상설 시험**으로 옮겨 적은 것이라, F1·F2 처럼 값에 무관한 `reader/` 개정이 main 에 오르는 순간 영구 실패한다. B-0 재현 시 이 조항을 좁히거나(세 정본 파일 · `engine/stages/read.py` · `reader/lib/run_checks.py` · `contracts/stages/read.yaml`) 빼야 한다 — 설계 §2.8 값 공간은 건드리지 않는다.

---

## §1 상신 원문 (2026-09-03 · 총괄 저작 · Owner 에게 낸 보고 전문)

# 프롬프트 감사 보고 — `/claude-api prompt-audit` (2026-09-03)

**적용하지 않았다.** 이 보고와 제안 diff 두 벌이 산출물이며, 리포·`~/.claude` 어느 파일도 고치지 않았다. 리포 쪽 제안은 임시 worktree 에서 적용 가능성만 검증했다(관문 6종 plain·`-O` 전건 exit 0 · pytest 591 passed · worktree 제거 · main `9d2246b` 무변경).

## 0. 범위와 전제

| 항목 | 전제 |
|---|---|
| 범위(요청에 지정 없음) | ① 레인 프롬프트 = `patent-docent/reader/procedure/{00,10,20,30,40}*.md`(러너가 요청서에 인라인) + `engine/lanes/contract.py`·`plan.py` 의 요청서 산문 ② 상설 레인 정의 = `~/.claude/agents/{sol-auditor,sol-coder,opus-coder,opus-supervisor,psy-subject}.md` ③ 세션 규약 = `~/.claude/CLAUDE.md` · `patent-docent/CLAUDE.md` · `~/.claude/hooks/compact-instructions.txt` · `~/.claude/agents/HOOK.txt`. 제외 = `ROUTING.md`·`LEDGER.md`·`LANE-RUNTIME.md`(규범·원장이며 프롬프트로 전송되지 않음) · `docs/**`(기록) · 기억 파일 · `runs/**`. `~/.claude/skills` 는 미조사 |
| 대상 모델 | 레인 = **Claude Opus 5**(`claude -p --model claude-opus-5 --effort max` · 계약 라벨 `opus-5`, 관측 식별자 `claude-opus-5[1m]`) · 레인 정의 파일 = frontmatter 모델(sol 래퍼 = `sonnet`, opus 레인 = `opus`, psy-subject = `haiku`) · 세션 규약 = Fable 5.1 |
| 비-Anthropic 표지 | `sol-coder`·`sol-auditor` 는 Codex CLI 로 **GPT-5.6 Sol** 을 구동한다. Sol 에게 가는 SPEC 본문·resume 프롬프트(`sol-auditor.md:197–198`)는 감사 대상에서 제외했고, Anthropic SDK 전환은 제안하지 않는다. 감사한 것은 **Claude 래퍼가 읽는 본문**만이다 |
| 방법 | 정적 읽기 + 신호 grep(대문자 압박·금지 밀도·이행 상대 어법·사고 서사·숫자 상한·think 지시·폐기 모델명) + 출처 조회(agents 리포 로그 `e4bd503`~`eac2375`, 절차 문서 편집일 08-18~09-01). 실행 회귀(A/B 런)는 하지 않았다 |
| 이 리포의 규율과의 관계 | 「구 문언을 지우지 않는다」 규율에 맞춰 제안은 전부 **삭제가 아니라 이동**이다(이동본 = `reader/procedure/HISTORY.md` · `docs/IMPLEMENTATION-HISTORY.md`, 원문 무수정). 그래도 절차 문서·CLAUDE.md 의 재구성은 Owner 확인 뒤 적용을 권한다(§4) |

## 1. 발견 요약 (확신 순)

| ID | 위치 | 패턴 | 확신 | 조치(diff) |
|---|---|---|---|---|
| F1 | `10-decompose.md:33,67,69,92–108,110,161,170,176,199,211` · `20-grounding.md:9,64` · `30-synthesis.md:73–79` · `40-output-contract.md:88` | 편집자용 문장·개정 이력·정정 마커가 **레인 요청서에 실린다**(독자 불일치) | 높음 | `HISTORY.md` 로 이동, 규약만 남김 |
| F2 | `10-decompose.md:174,187,224` · `20-grounding.md:76` · `30-synthesis.md:47` · `40-output-contract.md:87` | 이행 상대 어법(「구 규정은…폐지되었다. 이제…」·「폐기된 값」) | 높음 | 현재형 재서술 · 폐기 값 행 이동 |
| F3 | `~/.claude/agents/sol-coder.md:20` | 정합 결함 — sol-auditor effort 를 `max` 로 적음(정본은 xhigh · L-016) | 높음 | 수정 |
| F4 | `sol-auditor.md:3` · `opus-coder.md:3` · `opus-supervisor.md:3` | description 의 「use proactively」 | 중상 | 「…에 쓴다」 |
| F5 | `sol-auditor.md:14,54,60,150,154,157,167` · `opus-supervisor.md:13,36` · `opus-coder.md:20,21` · `sol-coder.md:59` | 폐지 개념의 흔적(CAP·구 항목)과 사고 서사 꼬리 | 중 | 규범 유지 · 서사는 원장 포인터로 |
| F6 | `sol-auditor.md:264–273` | 금지 절이 본문 규정을 3~5회째 재진술 | 중 | 5항으로 응축 |
| F7 | `patent-docent/CLAUDE.md:108–202` | 세션 규약 파일 §6 이 구현 상태 서사·정정 마커 ×3·`[OWNER-대기→해소]` 를 든다(95행 · 약 24 KB) | 중(재정 권고) | `HANDOFF-NEXT.md` §0 포인터 + 관문 6종 표 · 본문은 `docs/IMPLEMENTATION-HISTORY.md` 로 이동 |
| F8 | `opus-supervisor.md:42` | `DIRECTOR REPORT` 구명(L-014 개명 후 잔재) | 낮음 | diff 미포함 — 소비자 확인 후 |
| F9 | `patent-docent/CLAUDE.md:183–188` | 관문 명령을 `python3` 로 적고 실무는 `.venv/bin/python` | 낮음 | diff 미포함 — 시스템 python3 에 jsonschema·yaml 있음을 확인, 현재 동작 |
| F10 | `40-output-contract.md:79–93` · `CLAUDE.md` 규율 4 | 관찰 — 규율 4(펜 프롬프트 금지 목록 금지)의 문언은 펜(COMPOSE)만 다룬다. 독해 레인 계약의 금지표는 행마다 검사명·이유를 들어 「이유 있는 제약」으로 판정 | — | 변경 없음. 원칙을 독해 레인까지 넓힐지는 재정 사항 |

## 2. 발견 상세

### F1 — 편집자용 문장과 개정 이력이 매 요청마다 레인에게 실려 나간다 (높음)

**무엇.** 절차 문서는 「레인이 따를 현행 규약」과 「편집자가 알아야 할 어떻게 닫혔는가」를 한 파일에 든다. 후자의 예:

- `10-decompose.md:92–108` — `attaches_to` 순위 ④ 개정 이력 3단(구 문언 · 1차 개정 · 감수 미달 판정 · 2차 보수). 17행. 레인이 필요한 것은 :90 의 현행 규칙 한 행이다.
- `10-decompose.md:199` — *"규약을 고칠 때 이 블록을 함께 고쳐라"* — 편집자에게 하는 말.
- `10-decompose.md:104` · `20-grounding.md:64` · `30-synthesis.md:79` — *"지우면 다음 사람이 같은 판단을 다시 한다"* · *"다음 사람이 ⓐ를 재정 문언으로 읽지 않도록"* · *"다음 사람이 같은 처방을 다시 내지 않게"* — 전부 「다음 편집자」가 독자다.
- `10-decompose.md:33` · `30-synthesis.md:73–79` — 2026-09-01 실측 사고 서사(레인 응답 `M3068~M3070`, 총괄 상신 기각 경위).
- `10-decompose.md:161` — `[정정 2026-09-01]` 마커. 내용이 「이 문서가 두 말을 하는 상태로 나갔다」는 문서 자신의 결함 이력이다.

**왜 대상 모델에 낡았나.** ① Opus 5 는 이유가 붙은 규약 한 번으로 따른다. 규약이 왜 그 문언이 되었는지의 3단 이력은 준수율을 올리지 않고 주의만 나눈다. ② 「구 문언은 …였다」는 모델이 겪은 적 없는 이전 상태를 전제한다. 모델에게 그 문장은 잡음이거나, 더 나쁘게는 「그런 답도 있다」는 힌트다 — 이 리포의 규율 4 가 펜 프롬프트에 대해 말한 「코끼리를 생각하지 마」 프라이밍과 같은 기제다. ③ 「너」가 누구인지가 흐려진다. 같은 문서 안에서 「너의 작업」의 너는 레인이고, 「다음 사람」은 편집자다. ④ 비용은 매 요청에 실린다 — 절차 문서 5종 합계 71,420 B → 58,965 B(−17%), `10-decompose.md` 단독 35,137 → 25,152 B(−28%). 요청서 본문 전체가 입력 지문(S4)에 들어가므로 절차 문서를 고치면 지문이 바뀌고 **다음 런부터** 적용된다(P-U1 행위시법 · 현재 진행 런 없음).

**조치.** 이동본 `reader/procedure/HISTORY.md`(19 KB · 19절 H-1~O-2 · 원문 무수정 · 출처 행 번호 명기). `00-overview.md:3` 에 「이력은 HISTORY.md, 요청서에 실리지 않는다」 한 문장 추가. `contracts/stages/read.yaml#may_read` 의 `reader/procedure/**` 가 새 파일을 덮으므로 계약 변경 불요. **남긴 것** — 규약표의 「이유」 열에 든 실측(예: `:55` Jaccard 0.59 · `:63–65` 실측)은 규약의 근거이므로 유지했다. 백로그 B-3·재정 T5(문서는 수를 적지 않는다)가 이 수치들을 어떻게 다룰지는 T26 설계의 소관이다.

### F2 — 이행 상대 어법 (높음)

| 위치 | 원문 요지 | 제안 |
|---|---|---|
| `10-decompose.md:224` | *"구 규정은 … 즉시 escalate 로 처리해 파이프라인을 세웠다. 그 경로는 폐지되었다. 이제 …"* | 「조기 판단은 기록만 하고 러너는 계속 진행한다」 현재형 |
| `10-decompose.md:174` | *"구 문언은 조건부를 (if·when·in response to)로 예시했고, 그 둘은 재정으로 빠졌다"* | 「맨 when·if 는 표지가 아니다」만 남김 |
| `10-decompose.md:187` · `40-output-contract.md:87` | *"`alternative-form` 은 폐기되었다. 선언하면 스키마가 거부한다"* | 이동. 모델이 본 적 없는 값을 금지형으로 소개하는 것은 그 값을 프라이밍한다. 스키마가 이미 거부하므로 기계 방어선은 그대로다 |
| `20-grounding.md:76` | *"다만 그 이유가 바뀌었다(재정 P-B). … 이제 ⑤단계 레인이 고르는 것이 아니라"* | 「엔진이 전수 기계 수확한다」 현재형 |
| `30-synthesis.md:47` | *"왜 이렇게 바뀌었나. 구 규정은 ⑤단계 레인이 …"* | 「왜 기계가 수확하나」로 제목·본문을 현재형 |

### F3 — `sol-coder.md:20` effort 표 정합 결함 (높음)

sol-coder 는 *"sol-auditor 규격을 그대로 준용 — 여기 옮겨 적지 않는다(복사본은 낡는다)"*(`:14`)고 적고 바로 아래 표에서 sol-auditor effort 를 `max` 로 복사해 두었다. 정본 `sol-auditor.md:99,145` 는 L-016(2026-08-25) 이후 **xhigh**(발주문의 재정 기반 max 지정 시 max)다. 자기 경고의 실례. diff 에서 xhigh 로 고치고 예외 조건을 병기했다.

### F4 — description 「use proactively」 (중상)

세 레인의 `description` 이 「use proactively」로 끝난다. 이 관용구는 Claude Code 서브에이전트가 세션 모델의 **자동 위임**을 유도하도록 권장되던 시기의 것이다. 이 환경의 규범은 반대다 — 좌석은 `ROUTING.md` 판별식으로 정하고(HOOK.txt 「미독 발주 금지」), 오케스트레이션은 Workflow 기본·Agent 는 예외 3종이다(재정 2026-08-08). Fable 5.1 세션에게 「알아서 띄워라」는 문구는 그 규범과 충돌하는 압박이다. `psy-subject.md` 는 이미 반대 방향(「사용하지 말 것」)으로 적혀 있어 대조가 된다. 제안 = 「…에 쓴다」(언제 쓰는지의 절은 유지).

### F5 — 폐지 개념의 흔적과 사고 서사 꼬리 (중)

- `sol-auditor.md:150` 취소선 행 `~~timeout/CAP~~ 폐지` · `:154` *"CAP·RCAP 변수도 timeout 전개도 두지 않는다 … 조항이 남아 있는 것만으로 오해를 재생산했다"* — 폐지된 개념을 설명하기 위해 그 개념을 되살린다. 새 래퍼는 CAP 을 본 적이 없다. 제안 = 「시간 상한을 걸지 않는다. 끊는 주체는 하네스. 마감은 폴링 루프에서」 + LANE-RUNTIME 「함정 A」 포인터.
- `sol-auditor.md:54` 이탤릭 「구 항목은 … 내렸다 … 아래 절로 옮겼다」 — 파일 자신의 편집 이력. 제안 = 삭제(원장 L-004·LANE-RUNTIME 함정 F 가 이력을 든다).
- `sol-auditor.md:167` — 마커 preflight (3)에 이미 있는 대조 규정을 「2026-08-19 재정 ⑤ 이후 기계화됐다」는 서사로 다시 적는다. 한 문장으로 응축.
- 사고 ID 꼬리(`sol-auditor.md:14,157` · `opus-supervisor.md:13,36` · `opus-coder.md:20,21` · `sol-coder.md:59`) — *"2026-08-19 감수 3회 사망과 좀비 대기 셸 7개의 원인이었다"* 류. 이유(600초 상한·버퍼링·자기매칭)는 이미 같은 문장에 있으므로 꼬리는 편집자용이다. 원장 번호(L-019 등)는 남겼다.

**남긴 것.** `sol-auditor.md:203,205`(resume 가 샌드박스를 상속하지 않는다 — read-only 로 죽인 세션을 resume 했더니 쓰기가 성공했다)는 규칙의 **구체 근거**이므로 유지. `sol-coder.md:30,31,38` 의 Sol 실측(무언급 자기결정 100% · 무패치 보고 95.8% · B4 0.79)은 구동 대상 모델(Sol)의 성질이라 유지.

### F6 — 금지 절의 재진술 (중)

`sol-auditor.md` 에서 「배경 실행 의무」는 `:14,84,110,155,269` 다섯 곳, `--add-dir` 의무는 `:60–66,144,205,271` 네 곳, 마커 preflight 는 `:28–58,143,272` 세 곳에 있다. 마지막 금지 절(`:264–273`)은 이 셋을 한 번 더 요약한다. 반복은 Opus 5/Sonnet 5 에서 준수율을 올리지 않고, 두 판이 어긋날 때(F3 이 그 예) 어느 쪽이 정본인지를 흐린다. 제안 = 금지 절을 5항으로 응축하고 실행 형태·진입 조건은 해당 절 포인터로.

### F7 — `patent-docent/CLAUDE.md` §6 (중 · Owner 재정 권고)

§6(`:108–202`, 95행)은 M1.5·M1.8 변경표, 판 상향 근거, 전수 시험 계수와 `[정정 2회]`, 종결 선언의 순서 증명, 남은 여섯, T1~T6 좌표, 통주 3 결과, 관문 6종과 `[정정]`×2·`[추기]`·`[OWNER-대기→해소]` 를 든다. 이 파일은 **매 세션 맥락에 실리는 작업 규약**이고, 이 내용은 원장·인계문서의 것이다 — 문서 자신이 *"이 자리의 계수가 낡는 것은 세 번째다(4→5→6)"* 라고 적고 있고, `HANDOFF-NEXT.md` §0 이 이미 현재 상태의 정본이다(기억 규칙 「재개 진입점 = HANDOFF 첫 화면」). 또 `:177–178` 「다음 = M1 잔여 폐쇄 … 첫 런은 예행 런」은 같은 절 `:150–152` T1 차례와 어긋나는 낡은 문장이다(문서 자신이 :154 에서 그렇게 판정했다).

제안 = §6 을 ① HANDOFF §0 포인터 ② 「구현되었다의 경계」 문단(유지) ③ 관문 6종 표(도구 · 증명하는 주장 하나 · 층) 로 재구성. 구 본문은 `docs/IMPLEMENTATION-HISTORY.md` 로 전문 이동(무수정). 202 → 124 행, 42,348 → 18,579 B.

**왜 재정 권고인가.** 값 공간(규율 11)은 건드리지 않으나, 「닫힌 것도 어떻게 닫혔는지 남긴다」를 CLAUDE.md 에 **적용해 온 것이 Owner 의 선택**이었다. 이동이 그 규율을 만족하는지는 Owner 가 정할 일이다.

### F8·F9 — 낮음, diff 미포함

- `opus-supervisor.md:42` `DIRECTOR REPORT` — L-014 개명(opus-director → opus-supervisor) 후 남은 구명. `~/.claude/agents` 안에는 소비자가 없으나 기억·인계문서가 문자열을 들 수 있어 확인 후 변경.
- `CLAUDE.md:183–188` 관문 명령 `python3 tools/…` — 실무는 `.venv/bin/python`. 시스템 `python3` 에도 `jsonschema`·`yaml` 이 있어 현재 동작한다. 표기 통일은 선택.

## 3. 깨끗한 축 (조사했고 발견 없음)

- ALL-CAPS 압박(MUST/NEVER/ALWAYS) 0 · 「think step by step」·scratchpad 지시 0 · 폐기 모델명 0 · 숫자 상한 0(팬아웃 30 은 실제 한도) — 전 범위.
- `~/.claude/CLAUDE.md`(17행 · 포인터만) · `compact-instructions.txt` · `HOOK.txt` — 이상 없음.
- `engine/lanes/contract.py:306–361` 요청서 산문 · `plan.py:355–374`(재시도 블록) · `:768–789`(도면 등재) — 이유 있는 규정만. 재정 ID 태그(P-12·S4)는 짧아 유지. `plan.py:771–775` 의 사고 서사는 docstring(모델 미전송).
- 절차 문서의 금지표(`40-output-contract.md` §5) — 행마다 검사명과 이유. 유지.
- `psy-subject.md` `model: haiku` — 계측 전용 Owner 승인(2026-08-22). 변경 없음.

## 4. 산출물 좌표와 적용법 (적용은 Owner 확인 뒤)

| 파일 | 내용 | 적용 |
|---|---|---|
| `PROMPT-AUDIT-2026-09-03.md` | 이 보고 | — |
| `PROMPT-AUDIT-2026-09-03-patent-docent.diff` | 리포 8파일(신설 2) · 560행 | `cd ~/projects/patent-docent && git apply <diff>` 후 관문 6종 + pytest |
| `PROMPT-AUDIT-2026-09-03-agents.diff` | `~/.claude/agents` 4파일 · 146행 | `patch -p2 -d ~ < <diff>` (`a/home/.claude/…` → `~/.claude/…`) |

**검증(리포 diff).** 임시 worktree(`.worktrees/prompt-audit-check`, HEAD `9d2246b`)에 적용 → 관문 6종 plain·`-O` 12회 전건 exit 0 → `pytest tests/ -q` 591 passed(121 s) → worktree 제거 → main 작업 트리 변경 0. agents diff 는 정적 생성만 했다(그 리포는 건드리지 않았다).

**적용 시 함께 할 일.** ① 절차 문서 지문이 바뀌므로 진행 중 런이 없는 시점에 적용 ② `HANDOFF-NEXT.md` §3 이 관문 6종 계수를 들고 있으면 CLAUDE.md 표와 대조 ③ agents 리포는 자체 git 이므로 커밋은 Owner 규약대로.

## 5. 이 감사가 하지 않은 것

- 실행 회귀 없음 — 제안 문언으로 레인을 돌려 산출 차이를 재지 않았다. 절차 문서 변경의 실측은 다음 READ 런(T6 부분 시험)이 된다.
- `~/.claude/skills`·`memory-recall` 훅 문구·`ROUTING.md` 계열은 범위 밖으로 두었다.
- Sol 대상 SPEC 본문은 판정하지 않았다(비-Anthropic).
