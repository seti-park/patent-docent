# 독립 감수 원문 — M1b 설계 도전(gpt-6-astra high) · 재감사 5(RI · M9 fable xhigh 첫 적용) 발주문 · 판정 REVISE

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `74c4c2b26e0c0453ea82d7888957532ef6f5f7223d677149cfd7c10ece739ee9` · 10845 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-m2a1-audit/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 16:26:44 → 16:3x · **USAGE = input 1,250,745(cached 1,160,320) · output 10,877(reasoning 1,130)**. 사본 `~/projects/workspaces/pd-m1b-m2a1-audit`(detached `088f2fd` · `bundle/` = 발주문·SPEC v3·레인 보고). 읽기 전용 · pytest·관문 0건.

**판정 = REVISE · 2건(MED 2) · 기각 0 · 전부 발주자 귀책.** **MI-1**: Q5 가 M1b 원문 바이트 대조 대상을 `D-04` §28·§29(총괄 처분 요약)로 지정 — 원문은 `docs/lessons/2026-09-05-astra-m1b-{m2a1,m2a1v2}.md` 끝에 보존(둘 다 `exact_embedded=True` 실측) → 대조 좌표 정정(**MD-1 계열 대조 좌표 혼용 재발**). **MI-2**: Q1ⓒ 경로표에 **⑨ 전 접지 게이트 미진입 조기 반환**(`if not entered: return` · 플래그 거짓 → `finally` 가 저널 기록)과 **게시 뒤 일반 예외**(`_validate_convergence`·산출물 쓰기 실패 · 플래그 참 → 무덮어쓰기)가 빠짐 → 경로를 계수가 아니라 이름으로 고정. 확인 = 커밋·부모·반경·절 번호·819 = 811 + 8(정적 전개)·식별자 4·Q4 무접촉·구 트리 `5f4afe9` 와 `f3bd05b` 의 `read.py` blob 동일(`bff4f34`)·레인 보고 = §31(정규화 뒤 일치)·**allowlist BLOCKER 없음**(편집·삭제는 `python3` 파일 API · 원복은 `git checkout --`) · 권고 = allowlist 수행 문안 추가 · PASS 정의를 「BLOCKER/HIGH/MED 신규 0 · LOW 열거」로 · 필수 재현 [미검증] 시 처분 명시.

지적 열거 = MI-1, MI-2

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§32**. **전부 수용 + 권고 3 반영** → 발주문 정정판으로 fable xhigh 감사 발주.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

**마커 3검증 + 정본 HEAD**

```text
$ pwd
/home/laptop/projects/workspaces/pd-m1b-m2a1-audit

$ cat .audit-sandbox
path=/home/laptop/projects/workspaces/pd-m1b-m2a1-audit
pin=088f2fdb5e56a1733a315e1ee8aa812ed185ec21
order=M1B-m2a1-audit-20260905
disposable=true

$ git rev-parse HEAD
088f2fdb5e56a1733a315e1ee8aa812ed185ec21

$ git -C /home/laptop/projects/patent-docent rev-parse HEAD
088f2fdb5e56a1733a315e1ee8aa812ed185ec21

$ git status --short
?? .audit-sandbox
?? bundle/
```

`path=cwd`·`pin=HEAD`·`order=이번 M1b 발주` 일치. `bundle/`은 제공된 감사 입력이다.

**판정 = REVISE · 지적 2건(MED 2) · 모두 발주자 귀책.** 끊긴 곳은 Q5의 원문 대조 위치와 Q1의 경로 전사다. allowlist 때문에 실행이 불가능하다는 BLOCKER는 확인되지 않았다.

**MI-1 · MED — Q5가 처분 요약을 원문 바이트 대조 대상으로 지정한다**

좌표: [감사 발주문 Q5](/home/laptop/projects/workspaces/pd-m1b-m2a1-audit/bundle/AUDIT-ORDER-round-m2a1.md:28).

요구는 다음과 같다.

```text
§28·§29 의 M1b 원문 = 각 FINAL(바이트)
```

그러나 [D-04 §28](/home/laptop/projects/workspaces/pd-m1b-m2a1-audit/docs/decisions/D-20260903-04-t31-t32.md:1353)과 §29는 **총괄 저작 처분 요약**이며, 각각 `원문 = docs/lessons/…`로 다른 파일을 가리킨다. 해당 절 자체를 `FINAL`과 비교하면 불일치한다.

실제 원문 보존 위치를 바이트로 대조한 출력:

```text
m2a1   final_bytes=13791 exact_embedded=True suffix_exact=True
m2a1v2 final_bytes=12357 exact_embedded=True suffix_exact=True
```

검증 경로: Q5 → D-04 §28·§29 → 지정 lessons 파일의 도전 원문 → 각 레인의 `FINAL`. 두 원문 모두 lessons 파일 끝에 바이트 그대로 보존돼 있다. **MD-1 계열의 대조 좌표 혼용 재발**이다.

고치는 문안 한 줄: **“§28·§29는 MG·MH 처분을 대조하고, 원문 바이트 대조는 각 `docs/lessons/2026-09-05-astra-m1b-{m2a1,m2a1v2}.md`의 도전 원문과 해당 레인 `FINAL` 사이에서 수행한다.”**

**MI-2 · MED — Q1 경로표에 ⑨ 전 조기 반환이 빠졌다**

좌표: [감사 발주문 Q1ⓒ](/home/laptop/projects/workspaces/pd-m1b-m2a1-audit/bundle/AUDIT-ORDER-round-m2a1.md:24).

발주문은 게시 전 경로를 `예외·LanePending`, 게시 뒤를 `검사 실패·재독 StageError·정상`으로 열거한다. 실제로는 **예외 없이 ⑨ 전에 반환하는 경로**가 있다.

[read.py 실출력](/home/laptop/projects/workspaces/pd-m1b-m2a1-audit/engine/stages/read.py:1738):

```text
1738  if not entered:
...
1748      return {
...
1884  _finish_lane_log(paths, journal)
1885  lane_log_published = True
...
1974  if not lane_log_published:
1975      _finish_lane_log(paths, journal)
```

접지 게이트 미진입 반환은 플래그가 거짓인 채 `finally`로 들어가 로그를 기록한다. 예외도 `LanePending`도, 게시 뒤 정상 완료도 아니다. 기존 시험 [test_grounding_requires_convergence_verdict_or_envelope](/home/laptop/projects/workspaces/pd-m1b-m2a1-audit/tests/test_m2_read.py:2765)에 관련 경로가 있지만, 전체 스위트 실행만으로 Q1의 **경로별 로그 보존 실측**을 대신할 수는 없다.

또한 게시 뒤 일반 예외도 가능하다. `read.py:1907`의 검증 및 이후 산출물 쓰기 실패는 재독 `StageError`와 별개이며 플래그 참 상태로 `finally`에 진입한다.

검증 경로: `run()`의 반환·예외 지점 전수 판독 → 최초 게시 위치 → `finally` 조건 대조. 나열된 경로는 모두 실재하지만 **완전한 경로표는 아니다**. 사용자 기준의 “경로 넷”도 괄호를 풀면 다섯 항목이므로, 계수보다 개별 경로명으로 고정해야 한다.

고치는 문안 한 줄: **“Q1ⓒ에 ⑨ 전 접지 게이트 미진입 조기 반환과 게시 뒤 일반 예외를 추가하여, 전자는 저널 기록·후자는 기록본 무덮어쓰기를 직접 재현하되 원장·포인터 정책은 변경하지 않는다.”**

**나머지 사실 전제 실측**

커밋·부모 출력:

```text
0f00dc762241244dace6d0d90ad39668eee5f839
parent=f3bd05b16cbbcd71577392c8115d173f7615120a

088f2fdb5e56a1733a315e1ee8aa812ed185ec21
parent=0f00dc762241244dace6d0d90ad39668eee5f839
```

| 항목 | 확인 결과 |
|---|---|
| `0f00dc7` 반경 | `docs/SPEC.md` +1/−1, `engine/stages/read.py` +60/−4, 새 시험 +266/−0. **3파일 +327/−5** |
| `088f2fd` 반경 | `HANDOFF-NEXT.md` +6/−1, D-04 +133/−0 |
| 절 번호 | D-04 §28·§29 처분, §30 회수, §31 레인 보고 실재. HANDOFF 23차, SPEC §8.4 B-1 실재 |
| 재정 | `ruling-20260831-05-T2-T6.md` **§2가 T3**. 먼저 게시·기록본 검사·검사 한 벌·실패 경로 유의 문언 일치 |
| 전체 시험 수 | 소스·매개변수·JSON/YAML 데이터 정적 전개 **819 = 811 + 8** |
| 지정 식별자 | `_load_recorded_lane_log`·`lane_log_published`·`_install_lane_log_mutation`·`RequestWritingReplayAdapter` 모두 실재 |
| Q4 무접촉 | v3 목록과 일치. 지정 경로의 `f3bd05b → 0f00dc7` diff 빈 출력. 세 정책 식별자의 논리 변경 없음 |
| 커밋 메시지 | `0f00dc7` 메시지에 시험 계수 없음 |

정적 계수는 별표 전개도 포함했다.

```text
COUNT_KEY_SLUGS=5
_count_mutations=10
TV_MUTATIONS=70
STATIC functions=470 expanded=819 base=811 m25=8
```

새 시험 이름과 분류도 일치한다.

| 시험 함수 | 건수·분류 |
|---|---|
| `test_disk_digest_mutation_drives_value_check_and_is_preserved` | 1 · ⓐ 새 시험 |
| `test_disk_read_run_mutation_drives_only_shape_check` | 1 · ⓑ 새 시험 |
| `test_exception_before_exit_check_still_records_the_journal` | 1 · ⓒ1 회귀 |
| `test_reread_defects_are_stage_errors_and_are_not_repaired` | 4 · ⓒ3 새 시험 |
| `test_normal_completion_publishes_once_and_matches_memory_rows` | 1 · ⓓ 회귀 |

파라미터 이름은 `damage`, 값은 `null`, `non-dict-row`, `broken-json`, `deleted`다. **5함수·8시험**, 재독 오류 네 건을 회귀로 오분류하지 않았다.

**질문별 판별력·대조 축**

- **Q1:** 게시→플래그→재독→두 검사 순서는 실제 코드와 일치한다. `_finish_lane_log`가 실패하면 참 대입에 도달하지 않아 `finally`가 다시 시도한다는 설명도 맞다. 경로 완전성은 MI-2.
- **Q2:** 값 검사 인자만 원복·형태 검사 인자만 원복·`finally` 재덮기라는 **3종이 v3 §2(ii)와 일치**한다. 고안 변조 공간도 ⑨·재독 헬퍼·`finally`로 명시돼 골격 ⒁의 요구를 충족한다.
- **Q2 훅:** `payload` 참조와 깊은 복사본을 관측하고, 변조 함수는 파일을 재독한 별도 객체를 바꾼다. 메모리 저널을 변조하는 배선이 아니다. 어댑터는 실제 `FileLaneAdapter.write_request()`를 호출하며 지문 함수는 `request.md` 바이트의 SHA-256을 반환한다. 이번에는 요청 파일을 생성해 해시를 재현하지 않았다.
- **Q3:** `6 붉음/2 초록`과 실패 사유 분류는 §30·§31 및 시험 단언과 맞는다. §30의 구 트리는 `5f4afe9`, Q3는 `f3bd05b`지만 두 `read.py` blob은 **동일한 `bff4f3454999151034a222d0ca365089a355e47e`**이고 관련 코드·시험·계약 경로 diff도 없다.
- **Q4:** `read.py`의 네 hunk는 플래그·게시/검사·조건부 finally·재독 헬퍼로 v3 ①②에 대응한다. 무접촉 판정은 코드 커밋 `0f00dc7`에 적용해야 한다. 기록 커밋까지 합치면 D-04·HANDOFF 변경은 당연히 존재한다.
- **Q5:** 원문 위치만 MI-1로 수정하면 대조 가능하다.

**경로·전사·감사자 좌석**

drafts의 발주문·SPEC와 bundle 사본은 각각 바이트 일치했다. 레인 보고도 다음과 같다.

```text
bundle 보고 = final.txt: True
bytes=5161
sha256=85edec1d717494eb372d3ba194f2eef9ee9760a05184ae9916c12d0fa3e99549

D-04 §31 추출=5162 bytes
끝 개행 정규화 뒤 일치=True
```

정규화는 양쪽 끝의 CR/LF를 제거하고 LF 하나를 붙였다. 내용 바이트의 전사 누락은 없다.

향후 M9 사본도 이미 존재하며 읽기 실측 결과가 발주문과 맞았다.

```text
path=/home/laptop/projects/workspaces/pd-audit-round-m2a1
pin=088f2fdb5e56a1733a315e1ee8aa812ed185ec21
order=AUDIT-round-m2a1-20260905
HEAD=088f2fdb5e56a1733a315e1ee8aa812ed185ec21
status: ?? .audit-sandbox
```

같은 fable 모델이라는 점은 발주문에 명시돼 있다. 총괄 문언 불신, Q1 직접 재현, Q2 보고값 인용 금지, Q3 독립 대조, Q5 실측 비교를 함께 요구하므로 **문언상 독립 실측 강제는 충분**하다.

**allowlist·재현 명령·종료 조건**

[LANE-RUNTIME:291](/home/laptop/.claude/agents/LANE-RUNTIME.md:291)과 [러너 템플릿:12](/home/laptop/projects/workspaces/patent-docent-session-drafts/fable-audit-runner.template.sh:12)의 allowlist는 사용자 제시 목록과 일치한다.

| 요구 행위 | 허용된 수행 경로 |
|---|---|
| 임시 파일 편집 | `python3`의 파일 읽기·쓰기 |
| 구현 원복 | 사본 cwd에서 `git checkout -- engine/stages/read.py` |
| basetemp 생성 | `mkdir` |
| 생성물 삭제 | `python3`의 `Path.unlink()`·`shutil.rmtree()` |
| pytest·관문 | 허용된 venv Python과 `env` |

**발주문에는 `rm -rf`, `mv`, `patch`, `tee` 실행 요구가 없다.** 삭제 요구 자체도 허용된 Python으로 수행 가능하므로 BLOCKER가 아니다. 다만 첫 M9 호출의 시행착오를 줄이려면 다음 문안을 추가하는 편이 좋다.

> “임시 편집·삭제는 allowlist의 `python3` 파일 API로 수행하고, 추적 파일 원복은 사본에서 `git checkout --`를 사용한다.”

지정 venv Python, Q3의 `git show` 대상, Q4의 `diff-tree` 명령, 관문 7개 파일과 self-test 진입점은 실재한다. preflight와 종료 status 조건도 동일하다.

`PASS = 신규 지적 0(LOW는 막지 않음)`은 예외를 적용하면 이해 가능하지만, **“PASS = BLOCKER/HIGH/MED 신규 지적 0, LOW는 열거”**로 쓰면 계수 해석이 명확하다. 필수 재현이 미검증인 경우의 PASS 허용 여부도 명시하면 좋다.

**관측·제한**

pytest·관문·임시 변조 실행 **0건**. 파일 수정·`/tmp` 접근·정본 쓰기 없음. 실행 결과의 색과 시간은 재측정하지 않았으며, 위 시험 계수는 정적 실측이다.

종료 시 사본·정본 HEAD는 시작과 같고, 사본 status도 두 입력 항목 그대로이며 `__pycache__=0`이었다.

`USAGE: STATUS에서 MODEL=gpt-6-astra, EFFORT=high, MODE=read-only 확인. 현재 EV의 turn.completed usage는 아직 없음. input/cached/output/reasoning 수치는 종료 후 러너 관측값으로 첨부해야 함.`

VERDICT: REVISE