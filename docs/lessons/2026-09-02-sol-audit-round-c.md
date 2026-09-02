# 독립 감수 원문 — 라운드 C(재정 T27 집행 · `852dcdd`) sol 감사 · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감수 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「감수 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`sol-audit-round-c/final.txt` 의 sha256 `765e1aecdee407ed90cef76594d357baee97748d3e86f27ec379213bebe537bb` 와 `---` 아래가 동일).

**좌석 = sol**(GPT-5.6 Sol · reasoning xhigh · `좌석 M9` 적대 감사 · 교차 벤더 — 저작은 opus-coder(Opus high)). 실행 = `codex exec
--sandbox workspace-write --add-dir <사본>/.git --cd <사본>` · 계통 A 직접 구동 · 배경 실행 + `EXIT=` 마커 · 약 33분 · resume 없이 1차 완주.
**사본** = 정본의 `git clone` 을 `852dcdd` 에 체크아웃하고 루트에 `.audit-sandbox` 마커(`path`·`pin`·`order`·`disposable`)를 심은
격리 사본(재정 Q9 ⓐ · SPEC §8.3 9항) — 감수자가 마커 3검증 + `git rev-parse HEAD` 실출력을 보고 첫 절에 남겼다. **정본은 읽기만** —
총괄이 감사 전후 정본 트리 지문 `0cf666a351c95e5685bf4eb09a4e47c96c2caaff` 불변 · `git status` 0행을 확인했고, 감수자도 사후 절에
같은 값을 적었다. (감수자가 「`--add-dir` 미동반」이라 적은 것은 발주문 문면에 그 인자가 없다는 뜻이다 — 러너 실호출 문자열에는
있었고 감수자 자신이 사본 `.git` 쓰기 가능을 관측했다.)

**판정 = FAIL · 지적 6건(HIGH 1 · MED 3 · LOW 2).** T27 조건 8행 중 closed 5 · partially 2 · open 1. 결함 심기 27종 중 관문이
놓친 것 = 격 어휘(`CRITICAL` 통과 · C-2) · 표 행 arity(7셀 통과 · 5셀은 traceback 사망 · C-3) · 표 위치(§0/§1 밖 decoy 표 · C-4).
C-1 = `852dcdd` 시점 4b 행의 처분 `수용` 이 선행 출처 없이 처분표에서 처음 적혔다(「이미 정한 처분만 옮긴다」는 자기 서술과 충돌).
C-5 = T27 §3 ④ 「B 와 반경 비겹침을 두 발주문에 고지」가 실물과 어긋난다(C 발주문은 A′ 반경을 고지 · 두 재정 다 `docs/SPEC.md` 를
반영처로 든다). C-6 = 「관문이 주장하지 않는 것」 문언이 열거 완전성만 들고 포인터 실재성·사유 의미·선행 종결 사실성을 빠뜨린다.

지적 열거 = C-1, C-2, C-3, C-4, C-5, C-6

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-03-round-c.md` **§5** 에 있다. 요지 — **C-1 수용**
(기록 정정 + Owner 사후 확인 대상 등재) · **C-2·C-3·C-4 수용**(관문 수리 = 라운드 C′ · sol-coder) · **C-5 부분 수용**(사실 인정 · 단 C 가 B 앞에
병합되어 병렬이 순차가 되었으므로 「고지」는 B 발주문이 든다) · **C-6 수용**(문언 정정 4곳). Q4 총괄 재량 넷 = 전부 「적정」 · Q5 레인 이탈
3건 = 전부 「정당」 · Q7 후속 커밋 2건 = 정합.

---

# 감수 원문 (sol · 이 아래는 감수자 저작)

# 좌석 M9 판정 = FAIL

핵심 구조와 기준선은 대체로 작동하지만, `852dcdd` 시점에 출처 없는 `4b=수용` 처분이 먼저 적혔고(C-1), 관문에는 규격과 어긋나는 검증 누락·Markdown 표 우회·비정상 종료가 있습니다(C-2~C-4). T27 §3④의 병렬 발주 조건도 실물과 맞지 않습니다(C-5).

## 1. Preflight·사후 무결성

실출력:

```text
/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c
path=/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c
pin=852dcdd31add9ce048bd787a25e7c0049dfa6f99
order=AUDIT-round-c-20260902
disposable=true
path_match=yes
pin_match=yes
order_match=yes
disposable_match=yes
852dcdd31add9ce048bd787a25e7c0049dfa6f99
## HEAD (no branch)
?? .audit-sandbox
```

`--add-dir`은 미동반입니다. 쓰기 허용 범위는 감사 사본과 그 `.git`, `/tmp`뿐이며 정본은 읽기 전용이었습니다.

사후:

```text
audit_clone_tracked_diff_exit=0
852dcdd31add9ce048bd787a25e7c0049dfa6f99
?? .audit-sandbox
663c77e64fe49470916a346e7551c40d74f275a1
0cf666a351c95e5685bf4eb09a4e47c96c2caaff
```

정본 `git status --short`는 0행이었습니다. Q7용 `/tmp` 독립 클론도 시험 뒤 제거했습니다.

## 2. T27 조건별 판정

| 조건 | 판정 | 실물·좌표 | 재현과 마지막 출력 |
|---|---|---|---|
| ⒜① 총괄 머리말 열거 | **closed** | `등재` 7파일 모두 총괄 머리말 안 열거 1줄. [SPEC §8.3 11①](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/docs/SPEC.md:4635>) | 열거 계측 → `listed=7 exact_enumeration_lines=7` |
| ⒜② 처분표·4종·사유·포인터 | **partially-closed** | 45행 모두 형식상 4종·비공백·고유 쌍. 그러나 [4b 행](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/docs/decisions/DISPOSITIONS.md:100>)은 당시 `수용`의 선행 출처가 없고 포인터도 “현재 처분 없음”을 가리킴(C-1) | `disposition_rows=45 vocab_ok=45 reason_nonempty=45 pointer_nonempty=45 unique_pairs=45` |
| ⒜③ 관문·차집합 0 | **partially-closed** | 정상·요구된 G1~G4 변조는 잡음. 그러나 격 누락, 표 행 arity, §0/§1 위치 우회가 남음(C-2~C-4) | canon → `EXIT=0`; 결함표 참조 |
| ⒞ 소급 등재 | **closed** | 재정 작성 시점 `docs/lessons/*.md`는 17개 = PD-M1 12 + PD-M2 5. 집행 전 두 원문이 추가돼 19개 = `등재` 7 + `선행 종결` 12. 12건의 D 포인터 파일·인용 절도 실재 | `ruling_commit_d66462a_md=17`; `execution_parent_99fad78_md=19`; `registry=19 listed=7 closed=12` |
| §3① 열거됐으나 처분 없음 거부 | **closed** | self-test ⒜ 및 직접 변조 모두 G3 exit 1 | `EXIT=1` |
| §3② 전건 소급·canon 통과 | **closed** | 19파일 양방향 일치 | `EXIT=0` |
| §3③ CLAUDE 정정 마커 | **closed** | `852dcdd`에는 0건, `852→b3144d5→005355a`에서 총괄이 6종 마커를 삽입. [발주문 §2.6](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-c-t27.md:101>)이 이를 총괄 몫으로 명시했으므로 기록 순서상 정당 | `852_CLAUDE_mentions=0`; `005_CLAUDE_mentions=2` |
| §3④ 라운드 B와 양쪽 발주문 반경 고지 | **open** | 제공된 C 발주문은 B가 아니라 **A′** 반경을 고지. B 발주문 실물 없음. 더구나 T26·T27 반영처는 모두 `docs/SPEC.md`를 포함하므로 “파일 반경 비겹침” 자체가 문자 그대로 거짓(C-5) | `round_B_order_files=0` |

7/12 독법은 원장을 넘지도, 모자라지도 않습니다. 재정 당시의 “4~5건”은 실제로 PD-M2 5건이었고, 집행 전에 들어온 2건도 이미 열거를 가진 채 포함됐습니다. PD-M1 12건을 다시 1행씩 복제하지 않고 기존 종결 판정표를 가리킨 것도 중복 정본을 피하는 합리적 해석입니다.

## 3. 모든 diff hunk의 명령 근거

`git diff --unified=0 99fad78 852dcdd`는 총 11 hunk입니다.

| hunk | T27 근거 | 판정 |
|---|---|---|
| `SPEC.md:4567` 관문 5→6·발화 조건 | §3③·§4 T27 반영처 | 명령됨 |
| `SPEC.md:4576` 여섯째 관문 행 | ⒜③·§4 | 명령됨 |
| `SPEC.md:4629` 11항 신설 | ⒝ 규정급 문언·§4 | 명령됨. 두 머리말 함정과 계약 불요 설명은 공학 재량, 적정 |
| `DISPOSITIONS.md:+1..136` | ⒜②·⒞ | 파일 신설은 명령됨. §2 처분 대기는 합리적 재량. 단 4b 값은 C-1 |
| `fable-advice…:+3..10` | ⒜①·⒞ | 명령됨 |
| `opus-audit-g6…:+3..10` | ⒜①·⒞ | 명령됨. A-2/A-3 분리는 적정 |
| `opus-audit-t17…:+3..10` | ⒜①·⒞ | 명령됨. §2 대기 설명은 적정 |
| `sol-audit-halt…:+7..9` | ⒜①·⒞ | 기존 총괄 머리말 안 추가, 명령됨 |
| `sol-review-g6…:+3..10` | ⒜①·⒞ | 명령됨 |
| `tests/test_tools_check_dispositions.py:+1..346` | §3①과 CLAUDE §3 게이트 회귀 의무 | 필요한 공학 집행 |
| `tools/check_dispositions.py:+1..739` | ⒜③·§3①·§4 | 명령됨. 구현 결함은 C-2~C-4 |

lessons forensic 실측:

```text
lesson_added_lines=35
inserted_closing_headings=4
lesson_removed_or_modified_lines=0
RESULT: PASS — 19개 Markdown 파일 전건 통과 (R1·R2·R3)
EXIT=0
```

“추가 줄 전부가 머리말 안인가”에 대한 문자 그대로의 답은 **아니오**입니다. 27줄은 머리말 안이고, 새 머리말 4건의 닫는 제목 4줄과 뒤 빈 줄 4줄은 다음 절 경계입니다. 다만 이 4개 닫는 제목은 발주문이 명시적으로 허용했고 감수자 산문을 총괄 저작으로 삼키지 않게 하는 경계이므로 부작용 결함은 아닙니다. 감수자·자문가 원문 삭제·수정은 0줄입니다.

## 4. Q3 적대 결함 심기

자기시험 6종은 다음입니다.

- 열거된 id의 처분 행 삭제
- 열거 밖 id 행 추가
- 처분 `보류`
- §0 미등재 `.md` 추가
- 열거 줄 삭제
- 열거 줄 복제

빠진 클래스는 §0 유령·중복, 모든 G2 조건, 빈 사유·포인터, 중복 `(파일,id)`, 격, ID 문법, 머리말 밖 위치, 표 행 arity·절 위치, 입력 오류입니다. 별도 pytest가 G2·빈 셀·중복 일부를 보완하지만 C-2~C-4는 남습니다.

| 결함 | plain | `-O` | 결과 |
|---|---:|---:|---|
| ⓐ 새 `.md`, §0 미등재 | 1 | 1 | 검출 |
| ⓑ §0 유령 파일 | 1 | 1 | 검출 |
| ⓒ 열거 id 삭제, §1 존치 | 1 | 1 | 검출 |
| ⓓ §1 행 추가, 열거 없음 | 1 | 1 | 검출 |
| ⓔ `수용 ` | 0 | 0 | 미검출. Markdown 셀 외곽 공백 정규화로 판정—실질 어휘는 `수용` |
| ⓔ `수용됨` | 1 | 1 | 검출 |
| ⓕ 사유 빈칸 | 1 | 1 | 검출 |
| ⓕ 포인터 빈칸 | 1 | 1 | 검출 |
| ⓖ `(파일,id)` 중복 | 1 | 1 | 검출 |
| ⓗ `선행 종결` 포인터 없음 | 1 | 1 | 검출 |
| ⓘ 감수자 절 안으로 열거 이동 | 1 | 1 | 검출 |
| ⓙ 열거 줄 2개 | 1 | 1 | 검출 |
| ⓚ 상태 `등재됨` | 1 | 1 | 검출 |
| ⓛ `A-2/A-3` | 1 | 1 | 검출 |
| ⓛ 내부 공백 `A 2` | 1 | 1 | 검출 |
| ⓛ 전각 `Ａ-２` | 1 | 1 | 검출 |
| ⓜ 제목에 `추기`·`머리말` 없는 총괄 절 | 1 | 1 | 검출 |
| ⓝ 무변조·최적화 동치 | 0 | 0 | `Assert` AST 0, `__debug__` 0 |
| 추가: `이연 / TBD / TBD` | 0 | 0 | 의미 검증 경계, C-6 |
| 추가: `열거=없음` + 유일 행 삭제 | 0 | 0 | 문서에 명시된 사람 몫 경계 |
| 추가: 격 `CRITICAL` | 0 | 0 | **미검출, C-2** |
| 추가: 7셀 데이터 행 | 0 | 0 | **미검출, C-3** |
| 추가: 5셀 데이터 행 | 1 | 1 | 검출 아님—`IndexError`, `EXIT=` 없음, C-3 |
| 추가: 표를 §0/§1 밖으로 이동 | 0 | 0 | **미검출, C-4** |
| 추가: 열거 `V, V` | 0 | 0 | 명시된 집합 비교 의미상 중복 무시 |
| 추가: `선행 종결/TBD`로 재분류 후 행 삭제 | 0 | 0 | 의미 검증 경계, C-6 |

종료 코드 실측:

```text
canon plain/-O                  process_exit=0 last=EXIT=0
검증 실패 plain/-O             process_exit=1 last=EXIT=1
missing input plain/-O          process_exit=2 last=EXIT=2
bad argv plain/-O               process_exit=2 last=EXIT=2
5셀 데이터 행 plain/-O          process_exit=1 last=IndexError: tuple index out of range
```

`--self-test`는 임시 사본에서만 변조했습니다.

```text
selftest_process_exit=0 last=EXIT=0
input_digest_before=ef4a25fee8d0a1ba1f685595204f5699e99c9264496f8f02accee7ba9e031021
input_digest_after=ef4a25fee8d0a1ba1f685595204f5699e99c9264496f8f02accee7ba9e031021
selftest_temp_residue=0
```

기준선:

```text
여섯 관문 plain/-O: 전부 process_exit=0
24 passed in 4.23s
24 passed, 1 warning in 10.75s
587 passed in 173.09s
587 passed, 1 warning in 162.61s
```

## 5. 신규 지적

| ID | 격 | 좌표·재현 | 결함 |
|---|---|---|---|
| **C-1** | **HIGH** | [원장 T27 ⒞](</home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-01-T24-T27.md:253>)는 `현재 처분 없음`, [발주문 4b](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-c-t27.md:129>)와 [DISPOSITIONS 4b](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/docs/decisions/DISPOSITIONS.md:100>)는 `수용` | `852dcdd`에서 포인터는 처분 부재를 기록한 §1과 미래 커밋뿐이다. “이미 정한 처분만 옮긴다”는 문서가 처분을 처음 창설했다. 후속 Owner 재정 T29가 실체를 승인했지만 선행 절차 위반은 소급 소멸하지 않는다 |
| **C-2** | **MED** | [SPEC 11③·⑥](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/docs/SPEC.md:4637>), [G4 구현](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/tools/check_dispositions.py:349>); `격=CRITICAL` → `EXIT=0` | SPEC는 격을 BLOCKER/HIGH/MED/LOW/—로 한정하고 관문이 ①~④를 대조한다고 하지만 구현은 격 열을 읽지도 않는다 |
| **C-3** | **MED** | [표 파서](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/tools/check_dispositions.py:154>), [`Table.column`](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/tools/check_dispositions.py:95>); 7셀→0, 5셀→`IndexError` | 데이터 행 열 수를 헤더와 대조하지 않는다. 추가 셀은 조용히 통과하고 부족한 셀은 규약화된 `EXIT=1/2` 대신 traceback으로 죽는다 |
| **C-4** | **LOW** | [`select_table`](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/tools/check_dispositions.py:199>); §0/§1 제목을 무관 제목으로 교체 → `EXIT=0` | G1/G4가 “§0/§1 표”를 주장하지만 실제로는 문서 어느 곳의 동일 헤더든 받는다. decoy 표로 정식 절을 비울 수 있다 |
| **C-5** | **MED** | [T27 §3④](</home/laptop/projects/patent-docent/docs/decisions/ruling-20260902-01-T24-T27.md:263>), [C 발주 반경](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-c-t27.md:5>), 같은 발주 §2.5 | C 발주는 B가 아니라 A′와의 반경을 고지했고 B 발주문은 없다. T26·T27 모두 `docs/SPEC.md`를 반영처로 가져 “파일 반경 비겹침”도 사실이 아니다 |
| **C-6** | **LOW** | `이연/TBD/TBD`, `선행 종결/TBD` → 모두 `EXIT=0`; [도구 비주장 문언](</tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-c/tools/check_dispositions.py:9>) | 비공백 검사는 설계 경계지만, 네 문서의 “관문이 주장하지 않는 것”은 원문 열거 완전성만 든다. 포인터 실재성·사유 의미·`선행 종결` 사실성도 사람 몫임을 함께 밝혀야 강제 범위를 과장하지 않는다 |

## 6. Q4·Q5 판정

### Q4 총괄 재량

| 항목 | 판정 | 사유 |
|---|---|---|
| ⑴ 7건/12건 독법 | **적정** | 재정 당시 실제 분포가 5+12였고 집행 전 2건이 추가됨. 전 파일을 §0에 세우면서 옛 정본을 중복하지 않음 |
| ⑵ `R`·`C-a`·`C-b`·`V` | **적정** | 원문을 고치지 않고 총괄 머리말에서 표 식별자를 세운 기록 행위. 의미 설명도 바로 아래 남김 |
| ⑶ `S-1`·`S-2`, S-1 처분 | **적정** | id는 기록 재량. S-2는 T20의 기존 처분. S-1은 기존 격리 원칙의 저작 역프로브 적용으로 검사 값 공간을 바꾸지 않는 실행환경 규약이므로 규율 11상 총괄 재량 |
| ⑷ 제목 어형 함정 SPEC 성문화 | **적정** | R1 공허 통과를 실측한 오류 방지 규범이며 게이트 정답 집합을 바꾸지 않음 |

### Q5 저작 레인 이탈

| 이탈 | 판정 |
|---|---|
| A-2/A-3 분리 | **정당한 공학 재량**. `/`는 id 문법 밖이고 두 식별자를 한 행에 둘 수 없다. 처분 값은 하나로 유지 |
| 머리말 제목 어형 회피 | **정당한 오류 수정**. 보존 선언 삭제 시 현재 제목은 exit 1, 금지 어형을 넣으면 exit 0이 됨을 양 모드에서 재현 |
| §2 처분 대기 표 | **정당한 공학 재량**. ephemeral NOTES에만 남기면 T27이 막으려던 유실을 재현한다. 값을 만들지 않고 결핍 자체를 보존 |

R1 실증:

```text
current_title plain process_exit=1 last=EXIT=1
current_title -O process_exit=1 last=EXIT=1
forbidden_morphology plain process_exit=0 last=EXIT=0
forbidden_morphology -O process_exit=0 last=EXIT=0
```

## 7. Q6 선언 대 실물

- “열거가 원문을 빠짐없이 담았는지는 사람 몫”은 DISPOSITIONS 머리, SPEC 11항, 도구 docstring, 후속 CLAUDE에서 같은 뜻입니다.
- 파일 단위 `RULINGS-LEDGER §2`와 지적 단위 `DISPOSITIONS §1`의 층 구분도 DISPOSITIONS·SPEC·후속 CLAUDE가 일치합니다.
- `852dcdd` 계수 45행·7/12·자기시험 6종은 실물과 맞습니다. `005355a` 뒤에는 정정 마커와 함께 47행입니다.
- 예외는 C-2입니다. SPEC의 “①~④ 대조”가 실제 G4보다 넓습니다.
- C-6처럼 의미적 포인터·상태의 진실성도 사람 몫인데, 명시된 비주장 범위는 열거 완전성만 듭니다.
- 852의 CLAUDE 부재는 발주문이 총괄 후속으로 분리한 사항이고 `005355a`가 닫았으므로 그 자체는 위반으로 판정하지 않았습니다.

## 8. Q7 후속 커밋

`005355a`의 S-1/S-2 추가는 열거와 §1을 함께 45→47로 올렸고, 현재 정본 자료를 852 도구로 읽은 plain/`-O`는 모두 `EXIT=0`입니다. CLAUDE의 5→6 정정 마커와 여섯째 관문 설명도 실물 G1~G4에 맞습니다(C-2·C-6 제외).

`663c77e`의 섀도 원장 시험 정정은 적정합니다. 링크 worktree에서 구 시험과 신 시험을 같은 독립 클론으로 대조한 결과:

```text
005355a_linked_worktree_exit=1
663c77e_linked_worktree_exit=0
```

구 시험은 “현재 worktree 안 원장”을 기대해 실패했고, 신 시험은 “주 작업 트리 원장”을 기대합니다. 시험 축은 잘못된 경로 축에서 계약 축으로 교정됐습니다. 기대값은 엔진 함수를 재사용하지 않고 별도 `git rev-parse --git-common-dir`로 구하므로 구현과 같은 상수를 공유하는 항진식도 아닙니다. 생산 원장 전후 지문·격리 원장 실제 기입·무격리 호출 정적 검사라는 나머지 축도 유지됩니다.

## [미검증]

- 라운드 B 저작 발주문 원문은 정본·사본·제공된 scratchpad 어디에도 없었습니다. 따라서 “두 발주문 각각 고지”의 두 번째 문서를 직접 볼 수 없었고, 실물 부재 자체를 §3④ open/C-5로 판정했습니다.
- PD-M1 12파일은 각 포인터 파일과 인용 절의 실재까지 확인했지만, 그 12개 감사의 모든 지적을 원문부터 다시 재판정하지는 않았습니다. 이는 `선행 종결` 독법의 역사적 진실성을 완전히 재감수한 것은 아닙니다.