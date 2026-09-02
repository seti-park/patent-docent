# 자문 원문 — 재정 T26 집행 설계 v3 의 3차 도전 준비도 · 판정 REVISE

## ★ 이 절은 총괄 저작이며 자문 원문이 아니다 (2026-09-02 · 머리말)

**규율 10 의 이행 — 아래 「자문 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(원문 파일
`fable-advice-t26-v3/out.txt` 의 sha256 `8366063ddf4f435ccd20579f69dfe099dc06afddff5fc1e17062bacfbe5c91d4` 와 `---` 아래가 동일).

**좌석 = fable xhigh 자문**(ROUTING §5 ⑽ — M1a 의 구성요소 · 판정 + 논거 · 결정 없음). **트리거 = ⑽ ⓑ 「같은 문제가 2회 저항」** —
재정 T26 의 집행 설계가 M1b 설계 도전에서 두 번 FAIL(v1 B-1~B-7 · v2 V-1~V-8)을 받아 v3 을 쓴 뒤, 3차 도전 전에 불렀다.
호출 = `claude -p --model claude-fable-5-1 --effort xhigh`(LANE-RUNTIME 「Fable 좌석 호출 경로」 · 훅 차단 환경변수 2종 확인) ·
**자료 인라인 단발**(2차 판정 전문 + 설계 v3 전문 = 63,920 B · 도구·파일 접근 없음) · 배경 실행 + `EXIT=` 마커 · 약 7분 · EXIT=0.

**판정 = REVISE · V-1~V-8 은 전부 closed(V-2·V-4 조건부) · 새 결함 N-1~N-7(HIGH 3 · MED 3 · LOW 1) · 새 재정 사항 0.**
끊긴 지점 셋 — ① 생성기가 `os.chdir` 뒤 상대 `--out` 을 쓰면 골든이 임시 트리에 떨어진다(N-1) ② R9 의 전제(정본 12건 `phases`)를
설계가 미실측(N-2) ③ 생성기 저작 좌석·시점이 라운드 순서에 없어 B 가 골든 없이 시작한다(N-3). 그 밖 N-4(재시도 적격 헬퍼 명명) ·
N-5(계약↔상수 양방향 다리 시험) · N-6(R9 거짓 양성) · N-7(문언 5건).

지적 열거 = N-1, N-2, N-3, N-4, N-5, N-6, N-7

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260902-02-t26-design-challenge.md` **§8** 에 있다.
일곱 건 전부 **수용**(공학 수정 · 규율 11 ③ 재량) — **v4** 에 반영했고 자문의 말대로 재자문 없이 3차 도전에 냈다.
자문이 「실물 확인 필요」로 남긴 넷(T-1 wrapper 치환 방식 · `reader` 네임스페이스 패키지 · `dispatched_ids` 형태 · 12건 `phases`)은
총괄이 실측해 v4 §1 에 적었다.

---

# 자문 원문 (fable xhigh · 이 아래는 자문가 저작)

ADVICE: REVISE

# 자문 판정 — T26 설계 v3 · 3차 M1b 도전 준비도

자문 좌석(fable xhigh) · 트리거 ⓑ(같은 문제 2회 저항) · 도구·파일 미사용 · 인라인 자료(2차 판정 전문 · v3 전문)만으로 판단. 리포 실물이 필요한 판단은 「실물 확인 필요」로 표시한다. 결정은 총괄이 내린다.

## 1. V-1~V-8 폐쇄 판정

| 지적 | 판정 | 사유 |
|---|---|---|
| V-1 | closed | 패치 대상이 `engine.stages.read` 모듈 전역으로 옮겨졌다. :1743 은 호출 시점에 그 전역을 찾으므로 주입이 닿는다. wrapper 가 convergence 행을 fail 로 만드는 정확한 방식(status 필드 치환인지 finding 추가만으로 되는지)은 실물 확인 필요 — 좌표 문제가 아니라 저작 세부다. |
| V-2 | closed(논리) · 단 같은 절에 새 결함 N-1 | 스크립트 모드의 `sys.path[0]` 은 스크립트 디렉터리(`<main>/tests/fixtures/read-failure-grid`)이고 `<main>` 자체는 경로에 없다(editable 없음 · 스크립트 모드는 cwd 를 넣지 않음). `insert(0, repo)` 뒤가 첫 import 라면 `engine`·`reader` 는 `$TMP` 에서 온다. 정규 패키지는 `__path__` 가 하위 모듈 탐색을 결정하므로 ⓐⓑ 두 파일 검사가 두 패키지 트리 전체를 덮는다. 남는 구멍은 하나 — `engine/__init__.py`·`reader/__init__.py` 가 없어 네임스페이스 패키지이고 ∧ PYTHONPATH 에 `<main>` 이 있으면 두 트리가 합쳐질 수 있다: 실물 확인 필요. 값 위험은 없다(두 커밋 diff 0) — 원장의 절차 요건 문제. 보강 한 줄: `python -I` 로 실행 · insert 전 `sys.modules` 에 두 패키지 부재 확인 · `engine.__path__` 가 단일이고 repo 아래. |
| V-3 | closed | `/retry-1/` 정확히 3 · task 집합 {ground-independent, ground-dependent, synthesize} · T-1 은 `/retry-` 0 · 「회차 1」과 「행 3」 구별 — 도전자 실측과 일치. `dispatched_ids` 가 `/retry-1/<task>` 형태 문자열을 돌려주는지는 실물 확인 필요(:157). |
| V-4 | closed(조건부) | R9 = 도전자 처방 그대로(list·비공·중복 없음·⊆ {early, exit} + retry 행 ⊇ points) · 변조 ⒄. 유령 phase 는 ⊆ 에서 걸린다. 조건 = 정본 12건 phases 실물이 전부 ⊆ {early, exit} — 설계가 미실측(N-2). |
| V-5 | closed | R8 + `_retry_checks` 유일성 · 우주 = 출구 12 id · input-digest 거부 · 진입 가드 · 변조 ⒅ · T-5/T-6. 관문·런타임 양쪽에서 막는다. |
| V-6 | closed | eval 가능한 정확한 식 · 생성기와 T-7 이 같은 식. mask 해독은 manifest 의 `check_ids` 순서로 한다는 한 줄을 덧붙여라(id 는 집합 상등만 대조하므로 상수 순서와 달라도 깨지지 않게). |
| V-7 | closed | T-11 ⑤ — importlib 적재 · 집합 상등 · 정확히 3값. 관문 파일에 `__main__` 가드가 있어야 적재가 실행을 일으키지 않는다(저작 세부). |
| V-8 | closed | 3 StageError 칸(mask 1024·2048·3072 · r=1) 명시 · 6,144+3+1,020+1,023 = 8,190 · 격자 순서와 동률 해소 순서 분리. 가드 `ids ∩ READ_CHECK_IDS = ∅` 와 lane-log 2 id 가 `ENGINE_READ_CHECK_IDS` 라는 사실이 정합한다. |

## 2. 엄격한 도전자가 v3 에서 새로 찾을 것

**N-1 · HIGH · §2.8 생성 명령** — 생성기가 `os.chdir(repo)` 한 뒤 상대 경로 `--out tests/fixtures/read-failure-grid/manifest.json` 을 쓰면 파일은 `<main>` 이 아니라 `$TMP` 아래로 간다. 99fad78 에 그 디렉터리가 없으면 쓰기 오류, 있으면 `git worktree remove` 가 untracked 파일로 거부하거나 `--force` 시 파일이 사라진다. 어느 쪽이든 골든 커밋이 나오지 않는다. 닫기: `out = realpath(--out)` 을 chdir **전에** 고정하고 provenance 요약에 절대경로를 찍는다(또는 chdir 을 없애고 계약은 ⓒ 로 명시 적재 — 엔진이 cwd 상대 경로를 읽는지 실물 확인 필요).

**N-2 · HIGH · R9 의 전제 미실측** — 총괄이 §5 ④ 에서 도전자에게 「정본 12건 phases 가 전부 ⊆ {early, exit} 인가」를 물었다. 이는 §2.11 「정본 exit 0」 의 전제인데 설계가 스스로 재지 않았다. 하나라도 다른 값이면 R9 가 정본을 거부해 수락 명령 전체가 깨지고, 그때 우주를 넓히는 것은 값 공간 판단이 된다(§4). 닫기: 12건 값을 §1 표에 적는다(grep 한 번).

**N-3 · HIGH · 생성기 저작 좌석·시점 부재** — §2.8 은 「총괄이 라운드 B 발주 전에 실행 · 별도 커밋」이라 하지만 `generate.py` 는 신설 파일이고 누가 언제 쓰는지 없다. sol-coder 가 B 에서 쓰면 골든이 B 앞에 존재할 수 없다(순환). 닫기: 「생성기 = B 앞 소발주(좌석 M3 · 첨부 §2.8) → 총괄 실행·골든 커밋 → 라운드 B」 한 줄로 순서 고정.

**N-4 · MED · T-4 의 피검 대상 없음** — {convergence}·{verbatim, convergence} 는 레인 페이로드로 도달 불능(§1)이라 T-4 는 함수 단위여야 하는데 §2.6 은 부분집합 검사를 루프에 인라인했다. 닫기: `_exit_retry_eligible(contract, failing) -> bool` 같은 헬퍼를 명명하고 루프가 그것을 부르게 한다.

**N-5 · MED · 계약 ↔ 엔진 상수 12 id 다리 없음** — 관문은 엔진을 모르고(계약↔행), T-7 ① 은 골든↔상수를 본다. `checks_before_exit` 에 `read.__ghost__` 를 **추가하고** 그 행도 더하면 G1~G6 전부 통과한다. 이를 잡는 것은 「계약 출구 id 집합 == `READ_CHECK_IDS ∪ ENGINE_READ_CHECK_IDS` 양방향」 시험뿐인데 좌표가 없다(:853 이 양방향인지 실물 확인 필요). 닫기: 그 시험 좌표 명시(:853 확장 또는 T-7 ⑦ 신설).

**N-6 · MED · R9 는 phases 의 거짓 양성을 안 잡는다** — `read.source-digest` 에 `phases: [early, exit]` 를 넣어도 통과한다(총괄이 §5 ① 에서 스스로 던진 질문 · 설계에 답이 없다). 닫기: `exit ∈ phases(id)` 는 12건 전부 필수, `early ∈ phases(id) ⇔ id ∈ points[early].checks` — 관문이 계약만으로 판정할 수 있다. 정본이 이를 만족하는지는 N-2 실측과 함께 본다.

**N-7 · LOW** — ⓐ T-11 ④ 「결함 3종」 미지정 → ⑴⑽⒄ 로 명명. ⓑ T-9 grep 범위(`engine/` 전체 · 기대 0) 명시. ⓒ `_failure_verdict` 가 빈 후보를 받으면 StageError 임을 명시. ⓓ T-2 는 `/retry-` 포함 id 전체가 정확히 3 이고 전부 `/retry-1/` 임을 함께 검사(retry-2 부재). ⓔ T-1 wrapper 의 행 치환 방식 한 줄.

## 3. sol-coder 가 만날 결정 공백

- **임의 선택 또는 blocked 가 되는 자리**: N-3(생성기를 내가 쓰는가) · N-1(스펙대로 쓰면 깨진다 — 임의 수정 또는 반려) · N-4(헬퍼 유무) · N-5(설계에 없는 시험을 더할지) · N-7 ⓐⓑⓒ.
- **실물 의존이라 저작 중 드러날 것**: T-1 wrapper 의 행 치환 · `run_read_checks` 시그니처 · 생성기가 12 id 실패 행을 만들 때의 `CheckRow` 생성자. 코드에서 읽히므로 blocked 사유는 아니나 첨부에 한 줄씩 있으면 낫다.

## 4. 규율 11 — 신설 항목의 성격

- **⑬ R8 · `_retry_checks` 우주 · 미지 id StageError = 공학 재량.** 정상 12 id 영역의 (조치, 라벨) 값은 한 칸도 안 바뀌고, 바뀌는 것은 무효 선언의 처분(조용한 첫 일치 → 거부)뿐이다. input-digest 배제는 T29 ⓐ 의 귀결이지 새 판단이 아니다. E ⑦ 판정과 같은 선상.
- **R9 = 조건부 공학.** 정본 phases 가 이미 ⊆ {early, exit} 이면 형식 규율이다. 아니면 정본의 유효 선언을 거부하는 것이므로 phases 어휘 정의를 상신해야 한다 → N-2 가 분기점.
- **⑭ provenance 거부 = 공학.** 원장 절차 요건(「99fad78 트리에서 돈다」)을 검사로 집행하는 것이며 값 공간과 무관하다.
- 진입 가드의 early 등식 강제는 E ⑨ 판정대로 공학.

새 Owner 재정이 필요한 항목은 없다. N-2 실측이 어긋날 때만 예외다.

## 5. 판정

**REVISE.** 끊긴 지점은 세 곳이다. ① §2.8 생성 명령이 그대로는 골든 파일을 `<main>` 에 남기지 못한다(N-1). ② §2.11 「정본 exit 0」 의 전제인 12건 phases 를 설계가 실측하지 않았다(N-2). ③ 생성기 저작이 라운드 순서에 없어 B 가 골든 없이 시작한다(N-3). 여기에 sol-coder 가 임의 선택할 자리 N-4·N-5·N-7 이 남아 있고, 총괄 자신의 §5 ⑤ 기준으로 그 자체가 FAIL 사유다.

근거의 참·거짓을 다투는 항목(상신 사유)은 없다. V-1~V-8 은 v3 에서 사실상 닫혔으므로, N-1~N-7 을 반영한 v4 는 3차 도전에 그대로 내도 된다.
