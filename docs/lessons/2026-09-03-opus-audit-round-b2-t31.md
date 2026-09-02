# 독립 감수 원문 — 합본 감사(B″ `00dd3f8` + T31 `933c6ca` + T32 `794c639`) · 판정 FAIL

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-03 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(감사 stdout 전문 · `opus-audit-round-b2-t31/out.txt` 의 sha256 `e755bd9c647f1e4c35815ca1992d76b75efa11747daa30bb413d66c24c872e56` 와 `---` 아래가 동일 · 28,508 B).

**좌석 = opus max**(ROUTING M9 · 세 커밋 저작 = sol-coder). CLI 직구동 `claude -p --model claude-opus-5 --effort max`(환경변수 2종 실측) · `setsid` 배경 + `EXIT=` 마커 · 07:18 → 07:46(약 28분) · EXIT=0 · stderr 0 B. 발주문 = `AUDIT-ORDER-round-b2-t31.md`(여섯 질문 · 지적 ID `RD-*` · **감사 중 정본 커밋 금지 — 지켜졌다**: 시작·종료 HEAD `7355cf2` · status 0행 · 감사자 §1). 사본 = **홈 fs** `~/projects/workspaces/pd-audit-round-b2-t31`(detached `7355cf2` · 마커 3검증 일치) · basetemp 도 홈 fs(tmpfs 사고 재발 방지) · 감사 뒤 사본 원상 · 잔재 0.

**판정 = FAIL · 지적 6건(MED 1 · LOW 5) · 새 재정 사항 0.** **값·집행은 전건 닫혔다** — RC-1~RC-5·RC-7·[미검증] ⑤ 전건 closed(RC-6 partially → RD-6) · T31 §3 ①~④·§5 ① · T32 §3 ①~⑤·§5 ③ 전건 ✅ · 명령되지 않은 hunk 0(34 hunk 전건 대응) · 정합 편집 4종 + 우회 3종에서 조용한 통과 0 — **도출식이 뚫리는 「4자리+1」 편집에서도 동결 골든 T-7 이 붉었다**(RB-1 「단일 실패점」 우려를 실측으로 해소). RC-1 은 재감사 [미검증] ④(porcelain T·U·디렉터리 rename·재생성)까지 닫혔고 수정 전 붉음도 감사자가 직접 재현했다. **RD-1**(MED · 발주자 반경 귀책 1차): 렌더의 호환 기본값이 `convergence_early` 부재 시 **최종 판정서로 갈음**해, `reported_by` 없는 행위시법 산출물(실런 `cim-fp-3`)에서 CP1 이 근거 없이 「전건 일치」를 선언한다 — T31 발주 반경이 `test_m2_read.py` 의 render 호출점을 빼 레인이 반경 안에서 낼 수 있는 답이 기본값뿐이었다. **RD-2**(LOW): 「조기 판정서 없음 — 구 판 산출」 갈래가 러너에서 도달 불가(`load_json` 부재 예외)인데 SPEC 이 표면 성질로 적는다. **RD-3**(LOW): 도출식 시험의 T22 결속에 발화 불가 연언(`"retry" in row`). **RD-4**(LOW · 발주자): T32 accept 픽스처가 기존 accept 와 바이트 동일 복제 — 판별력 0 인데 계수 증가를 조건 ② 증거로 인용. **RD-5**(LOW · 총괄 처분·반경): §5 ③ 이 스키마에서 지운 문장이 `reader/lib/run_checks.py:138-140` docstring 에 그대로 · 폴백 우회 시험에 표지 없음 · 폴백 타는 호출점 둘 잔존. **RD-6**(LOW · 총괄): RC-6 재정정이 RB-2 귀책 라벨을 원문(「설계(발주자)」)과 달리 인용. Q6 = 값·집행은 감사상 닫혔으나 지적 0 이 아니므로 PASS 아님 · 남은 것 5항(RD · 사후 확인 6묶음 · **발주문 골격 미개정** · B″ 별건 감사 대체의 검증 완료 · 재감사 [미검증] ① 수리 기제).

지적 열거 = RD-1, RD-2, RD-3, RD-4, RD-5, RD-6

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-04-t31-t32.md` **§9** 에 있다. **전부 수용** → 라운드 **RD**(sol-coder · RD-1~RD-5) + RD-6 총괄 재재정정(이 커밋) + 발주문 골격 개정(`D-20260902-02` §5 ⑽⑾ · 이 커밋).

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

모든 실측을 마쳤다. 임시 변조·사본·basetemp 전부 정리했고 사본 status 는 `?? .audit-sandbox` 한 줄이다.

---

# 좌석 M9 적대 감사 보고 — 합본(B″ `00dd3f8` + T31 `933c6ca` + T32 `794c639`)

## 1. preflight 실출력

| 항목 | 실출력 |
|---|---|
| 마커 `path=` | `/home/laptop/projects/workspaces/pd-audit-round-b2-t31` — 실제 cwd 와 일치 |
| 마커 `pin=` | `7355cf2432a92de148b812ec778d75437f97df03` = 사본 `git rev-parse HEAD` **일치** |
| 마커 `order=` / `disposable=` | `AUDIT-round-b2-t31-20260903` / `true` |
| 사본 status | `?? .audit-sandbox` (1행) |
| 정본 HEAD (시작·종료) | `7355cf2432a92de148b812ec778d75437f97df03` — **감사 중 커밋 없음** |
| 정본 tree / status | `8dbcf8233b155294781ffb8ddf35b6a0e6230139` / **0행** |
| 기준선 pytest | plain `773 passed in 168.37s` · `PYTHONOPTIMIZE=1` `773 passed, 1 warning in 208.78s` |
| 시험 수 추적(`--collect-only`) | `00dd3f8` **765** → `933c6ca` **768**(+3) → `794c639` **773**(+5: 시험 2 + 매니페스트 3) → `7355cf2` **773** |
| 관문 7종 | plain·`-O` **전건 rc=0** |

---

## 2. RC-1 ~ RC-7 · [미검증] ⑤ 폐쇄표

| ID | 판정 | 실측 근거 |
|---|---|---|
| **RC-1** | **closed** | 독립 프로브로 사본에 실제 `git mv` → 미러 후 clone 에 **옛 경로 부재 · 새 경로 실재 · status `''` · 파일 차집합 0**. [미검증] ④ 도 함께 닫았다 — `T`(타입 변경 파일→심링크) ✅ · `U`(`UU` 실충돌) ✅ · 디렉터리 이름 변경(파일 2건 R) ✅ · **rename 후 옛 경로 재생성**(`R` + `??` 동시) ✅. **`C` 는 재현 불가** — `git status` 는 `--find-copies-harder` 를 노출하지 않아 `status.renames=copies` 를 켜도 `A` 로만 났다(코드 갈래 `"R" in code` 가 복사에서 unlink 를 건너뛰는 것은 정적으로 옳다). **수정 전 붉음도 내가 직접 재현**(총괄이 재현하지 않았다고 적은 자리) — unlink 6줄을 되돌리면 `1 failed, 2 passed`(`assert not (clone/old).exists()`) |
| **RC-2** | **closed** | 재작성 도출식의 세 항이 **원장 문언과 축자 일치**: T29 §2 ⒜ 가 「출구 12 검사 = `READ_CHECK_IDS` 10 + `ENGINE_READ_CHECK_IDS` 2」를 **표로 열거**한다(우주 정의가 코드 우연이 아니라 재정) · T24 ⒜ 「`halt` 그대로」+T25 ⒜ · T28 ⒜ β · T22(원장 `RULINGS-LEDGER.md` §2 = *「두 검사가 출구 재시도 루프 **종료 후** 합류」* · `action: escalate` · `retry(n)` 없음 · `points` 없음). **정합 편집 4종을 다시 심어 전건 붉음 확인**(아래 §4) |
| **RC-3** | **closed** | `grep "출구 독해 검사"` → SPEC·contracts 에 **0건**(감사 원문·처분표의 인용만 남음). 새 문언이 `SPEC:385`·`:1316` 두 곳에 실재하고 산식이 맞다(12−1−1−2=8) |
| **RC-4** | **closed** | 생성기 기대 집합이 계약 `checks_before_exit`(YAML · 12항 실측)에서, 실제 `check_ids` 는 `READ_CHECK_IDS + ENGINE_READ_CHECK_IDS`(파이썬 상수)에서 온다 — **두 층**. `validate_manifest:255` 는 여기에 리터럴 `12` 까지 겹친다. 항등식 성질 소멸 |
| **RC-5** | **closed** | `grep -rn "/home/laptop/projects/patent-docent" tests/ tools/ engine/ reader/ contracts/` → 남은 것은 `${MAIN:-…}` 재정의 기본값 3곳 + 박제된 `manifest.json` provenance 뿐(재감사가 「결박 아님」으로 판정한 것) |
| **RC-6** | **partially** | `§1` 에 `[재정정 2026-09-03 · 재감사 RC-6]` 실재하고 6건을 개별 열거한다. 다만 그 열거가 감사 원문의 라벨과 한 자리 어긋난다 → **RD-6** |
| **RC-7** | **closed** | `tests/conftest.py` 신설. 단독 실행 실측 — golden `73 passed` · contract `10 passed` · generator `89 passed` · 신설 `test_m24_read_run_vocabulary_binding` `3 passed` · `test_m22` `8 passed`. `python -m pytest` 와 venv `pytest` 스크립트 **양쪽** 초록. `test_m16` 의 기존 삽입은 `if REPO not in sys.path` 로 가려 **이중 삽입 없음** |
| **[미검증] ⑤** | **closed** | 정본 계약 11행 중 `upstream-defect` 행을 지우고 `--self-test` → plain·`-O` 양쪽 `정본 계약이 승인 골격과 다르다 — self-test 미실행` + G1 두 줄 + `EXIT=1`, **`SELF-TEST mutations=` 줄 0회**(변조 36종 미실행) · **트레이스백 0줄** |

---

## 3. 원장 집행 조건 대조

### T31 §3 ①~④ · §5 ①

| # | 조건 | 실측 마지막 출력 | 판정 |
|---|---|---|---|
| ① | 발주 = 라운드 B 병합 뒤 | B 병합 `1d29c8b` 커밋 시각 < T31 커밋 `933c6ca` | ✅ |
| ② | 0건 한 줄 / n건 n행 + 귀속 열 · 픽스처는 실런 형태 | `test_m22_unclassified_render_notice.py` `8 passed in 0.06s`(신설 3 포함). 실런 3건은 셋 다 `unclassified_dependents` 키 보유 — **다만 전부 `[]`** | ✅(단서 = §7 ①) |
| ③ | SPEC §1.5 + 좌표 | `docs/SPEC.md:534` 신설 행에 `재정 2026-09-02 T31 §2 ⒜·§3 ③` · `check_spec_refs` `RESULT: PASS` rc=0 | ✅ |
| ④ | 스키마 diff 0(**T31 커밋 단위**) | `git diff --stat 933c6ca^ 933c6ca -- contracts/schemas reader/schemas` → **빈 출력** · T31∩T32 파일 겹침 **0** | ✅ |
| §5 ① | A-2 문언이 블록을 가리킨다 | `material_spec_md.py:450` `두 실행이 갈린 신고는 아래 10-b 블록에 있다.` | ✅ |

**Q2ⓐ — 「갈린 신고」 정의의 공백은 없다.** 합집합 동일성 키가 `(claim, dependency_type, text_verbatim)`(`run_checks.py:236-249`)이고, 스키마가 `text_status` ⟺ `text_verbatim == «문언 없음»` 을 `allOf/if-then` 으로 **양방향 결속**한다(`:165-186`). 따라서 ⑴ 두 실행이 같은 문언을 신고 → 한 행 `reported_by` 2개(일치) ⑵ **같은 청구항을 서로 다른 문언으로 신고 → 두 행, 각각 `reported_by` 1개 → 둘 다 블록에 실린다** ⑶ `text_status` 만 갈리는 경우는 **스키마가 만들 수 없다**. `reported_by` 는 `minItems: 1` 이고 실행이 둘이므로 길이 ∈ {1,2} — 분할이 완전하다. SPEC §1.5 신설 행도 정의를 `reported_by`가 한 실행만 든 항목으로 **명시**한다.

**Q2ⓑ — 렌더가 조기 판정서를 받는 경로.** `read.py:1941` `convergence_early=load_json(paths.convergence_early_json)`. `load_json`(`engine/stages/__init__.py:82`)은 `open()` 그대로라 **부재 시 `FileNotFoundError`** 다. 러너에서 부재는 불가능하다 — `write_json(paths.convergence_early_json, …)`(`:1637`)이 `while True` 루프 본문에서 **무조건** 돌고 렌더는 그 하류다. 그러나 그 사실이 「구 판 산출」 갈래를 **러너에서 도달 불가**로 만든다 → **RD-2**.

### T32 §3 ①~⑤ · §5 ③

| # | 조건 | 실측 마지막 출력 | 판정 |
|---|---|---|---|
| ① | 정의 1 · 참조 2 · 리터럴 1 | `grep -c '"read-a"'` = **1**(`:277`) · `$defs.read_run` `:276` · `$ref` `:98`·`:161` **2곳** | ✅ |
| ② | 무효 2 REJECT · 유효 1 ACCEPT | `SUMMARY: cases=48 REJECT_OK 32/32 ACCEPT_OK 14/14 VALIDATOR_SCOPE 2/2 schemas=5` · 두 무효본 **각각 위반 정확히 1건**, 경로 `$.canonical_selection.read_run`, 메시지 `'read-c' is not one of ['read-a','read-b']` / `'' is not one of …` · 기준선 대비 diff **1줄** | ✅ |
| ③ | 러너 판정서 통과 | `test_runner_convergence_reports_validate_against_shared_read_run_enum` 이 `m21.run_with_payloads` → `m2.run_read_stage`(**실제 러너**)를 돌려 `paths.convergence_early_json`·`convergence_json` 을 디스크에서 읽어 물린다. 손으로 쓴 사본 아님 | ✅ |
| ④ | `runs/**` 무접촉 · `$comment` 기록 | `git diff --stat 00dd3f8^ 7355cf2 -- runs` → **빈 출력** · 구 문언이 `[정정 T32] …` 절로 보존 · §5 ③ ⑴⑵⑶ **실물 대조 전건 참**: 스키마에 `provenance` 속성 없음(`additionalProperties: false`) · 러너 두 호출점(`:1631`·`:1889`) 모두 `canonical_read_run=canonical_run` 명시 전달 · 실런 3건의 `provenance.read_runs` = `['read-a:canonical','read-b:convergence-peer']` | ✅ |
| ⑤ | `screening_memos[].read_run` 무접촉 | `{'type': 'string', 'minLength': 1}` 그대로(`:232`) · T32 diff 에 그 자리 없음 | ✅ |

**Q3ⓔ — 폴백 처분(총괄) 판정 = 「적정하되 모자람」.** 러너는 정말 항상 명시 전달한다(두 호출점 실측). 처분의 **결정**은 옳다 — 붉은 시험이 러너가 타지 않는 경로를 재현하고 있었고, `reader/` 이식 단위를 여기서 건드리지 않은 것도 옳다. 모자란 것은 **기록**이다 → **RD-5**.

---

## 4. Q1 우회 재시도 표

`read.lane-log-shape` escalate 행으로 옮기는 11행 유지 정합 편집(계약 2자리 + 엔진 1 + 관문 2).

| 심은 편집 | 관문 7종 | `--self-test` | 도출식 모듈 |
|---|---|---|---|
| `read.coverage` | **전건 rc=0** | `36/36` EXIT=0 | **`2 failed, 8 passed`** (도출식 + 골격) |
| `read.bibliography` | **전건 rc=0** | `36/36` EXIT=0 | **`2 failed, 8 passed`** |
| `read.pointer-resolve` | **전건 rc=0** | `36/36` EXIT=0 | **`2 failed, 8 passed`** |
| **claim 2종**(8행 `points: [early, exit]`→`[early]` + 4자리) | **전건 rc=0** · `failure_rows=11 early_retry=3 exit_retry=6` | `36/36` EXIT=0 | **`1 failed, 9 passed`** (도출식 **하나만**) |

**우회 시도 — 「4자리+1」.** 착지 지점을 골격 시험이 보는 lane-log 행이 아니라 **`read.source-digest` halt 행**으로 옮기고(계약 2 + 엔진 1 + 관문 2), 여기에 **시험의 배제 상수 `HALT_EXIT_CHECKS` 까지 동반 편집**했다.

| 시도 | 관문 7종 | 붉는 것 |
|---|---|---|
| halt 착지 · 시험 상수 무편집 | 전건 rc=0 (`exit_retry=7`) | **3** — 도출식 · 골든 T-7 · 생성기 매니페스트 |
| **halt 착지 + `HALT_EXIT_CHECKS` 동반(4자리+1)** | 전건 rc=0 (`exit_retry=7`) | **2** — 도출식은 **초록으로 돌아가지만** 골든 T-7 `test_every_golden_cell_matches_runtime` 과 생성기 `test_normal_generation_manifest` 가 **셀 계수 차**(`halt/null 7168 ≠ 6144`)로 붉는다 |
| 검사 id 개명(계약+등재부+관문 동반) | `check_validator_enforcement` **rc=2**(환경 오류) | **65 failed** — 폭발 |

**우회는 성립하지 않는다.** 도출식이 뚫려도 **동결 골든 8,190칸**이 두 번째 오라클로 선다. 이것은 RB-1 처분의 「단일 실패점」 우려(재감사 Q5)에 대한 실측 답이다 — 단일이 아니다.

**Q1ⓒ — 생성기 기대 집합은 「다른 층」이 맞다.** 계약 YAML(`checks_before_exit` 12항) vs 파이썬 상수 2개. 한쪽만 변조하면 `check_ids.expected_set` 위반으로 생성기가 파일을 안 쓴다(재감사 실측). **둘을 함께 바꾸면 생성기 자기검증은 통과한다** — 위 표에서 생성기는 매니페스트를 **실제로 산출했고**, 붉힌 것은 골든과의 대조다. 이것은 **설계 경계이지 결함이 아니다**: 생성기는 「매니페스트가 오늘의 두 층과 맞다」만, 골든은 「오늘의 두 층이 승인된 동결값과 맞다」를 증명한다. 각 도구가 하나의 주장만 든다는 이 리포의 규율 그대로다.

---

## 5. 신규 지적

### RD-1 · MED · 렌더의 호환 기본값이 **최종 판정서를 조기 판정서로 갈음**해, CP1 승인면이 근거 없이 「전건 일치」를 선언한다
**귀책 = 발주자(반경 설계) 1차 · 저작 레인(선택한 형태) · 총괄(수용 시 미기록).**
**좌표** `engine/render/material_spec_md.py:30`(`_CONVERGENCE_EARLY_UNSET`) · `:107-110` · `:482-484` · 소비자 `tests/test_m2_read.py:2043-2044`·`:2521`.
**재현(실런 산출물)**
```
$ python -c "render(spec, convergence_json, {...}, repo)"   # 구 3인자 호출 = 기존 직접 호출
runs/openai-us20260147854a1-cim-fp-3 →
  ## 10-b. ★ 조기 합집합 — 두 실행이 갈린 미분류 신고 (재정 T31)
  갈린 신고 없음 — 두 실행의 미분류 신고가 전건 일치
  ---- 같은 런의 미분류 항목 수 = 1  (그 항목엔 reported_by 도 text_status 도 없다)
```
**기제** `convergence_early` 를 주지 않으면 `convergence_early = convergence`(최종 판정서)로 **조용히 갈음**된다. 최종 국면의 미분류 항목은 `read.py:1836` 이 `extras["read_run"] = canonical_run` 하나만 붙이므로 **전건 `reported_by` 길이 1** — 즉 갈음이 일어나면 정본 실행의 미분류 목록 **전부**가 「두 실행이 갈렸다」로 실린다. 반대로 `reported_by` 가 아예 없는 행위시법 산출물(위 실런)에서는 길이 0 → 필터에서 빠지고 **「전건 일치」라는 적극적 주장**이 나간다.
**왜 결함인가** T31 은 **승인 표면의 변경**이라 재정 사항이었다(원장 §2 ⒞). 그 표면에 「없음/일치」를 선언하는 자리가 **데이터 부재와 데이터 일치를 구별하지 못하고**, 출처가 조기 판정서가 아닐 수 있다는 사실이 기본값 뒤에 숨는다. 오늘 러너 산출에는 영향이 0이다(러너는 항상 명시 전달). 값 공간은 무변경이다. 고치는 비용은 기본값을 `None`(또는 필수 키워드)으로 두고 `test_m2_read.py` 두 호출점에 `convergence_early=None` 을 적는 두 줄인데, **T31 발주 반경이 `test_m2_read.py` 를 뺐다** — 레인이 반경 안에서 낼 수 있는 답이 이 기본값이었다.

### RD-2 · LOW · 「조기 판정서 없음 — 구 판 산출」 갈래가 러너에서 도달 불가인데 SPEC 은 그것을 CP1 표면의 성질로 적는다
**귀책 = 저작 레인 / 총괄 처분(D-04 §4 에서 검토하고 수용).**
**좌표** `engine/stages/read.py:1941` · `engine/stages/__init__.py:82` · `docs/SPEC.md:534` · 발주문 `SPEC-round-t31.md` §1 T31 ⓐ 「(예외 금지)」.
**재현** `load_json` = `open(path)` 그대로 → 부재 시 `FileNotFoundError`. 러너는 `os.path.isfile` 가드 없이 부른다. 리포에 재렌더 도구는 없다(`grep -rln "material_spec_md" tools/` → 0). 따라서 **어떤 런도 이 한 줄을 낼 수 없다**.
**왜 적는가** 발주문이 명시로 「예외 금지」를 걸었는데 그것이 **함수 층에서만** 참이고 시스템 층에서는 거짓이다. SPEC §1.5 는 *「조기 판정서가 없는 구 판은 부재 안내를 내고」* 라고 **표면 성질**로 적어, 발화할 수 없는 강제를 문서가 서술한다 — 이 리포가 FAIL 을 받았던 「강제의 범위를 실제보다 넓게 말하는」 형태의 거울상이다. 비용은 `load_json(...) if os.path.isfile(...) else None` 한 줄.

### RD-3 · LOW · 도출식 시험의 T22 결속에 **발화 불가 연언**이 하나 섞였다
**귀책 = 저작 레인(B″) · 처분(무검증 수용).**
**좌표** `tests/test_m24_failure_table_contract.py:263-266`.
**재현** `if row.get("action") != "escalate" or "retry" in row or "points" in row:` — 계약 `failure` 행의 키 전수는 `['action','checks','condition','judged_at','kind','note','points','reason_label','then']` 이고 **`retry` 키는 어느 행에도 없다**. 게다가 형제 시험 `test_approved_failure_skeleton_matches_contract_exactly:277` 이 `set(row) == machine_keys | {"condition","note"}` 로 **키 집합을 정확 일치**로 고정하므로 `retry` 키는 **존재할 수 없다**. 즉 `"retry" in row` 는 항상 False.
**왜 결함인가** 그 연언은 T22 의 핵심(*「`retry(n)` 을 적지 않는 것이 이 재정의 핵심」*)을 검사하는 것처럼 보이지만 실제 강제는 `action != "escalate"` 하나가 다 한다(계약은 재시도를 `action: "retry(1)"` 로 적는다). **RC-4 가 지적한 「형태만 남은 제약」과 같은 과**이고, 이번엔 B″ 가 새로 넣었다. `"points" in row` 는 살아 있다(lane-log 행에 `points` 를 붙이면 발화).

### RD-4 · LOW · T32 의 accept 픽스처가 기존 accept 와 **바이트 동일한 복제**여서 판별력이 0인데, 그 계수 증가가 조건 ② 의 증거로 인용된다
**귀책 = 발주자(설계).**
**좌표** `tests/fixtures/schema-enforcement/accept/convergence.canonical-read-run-read-a.json` · 매니페스트 `:276-282` · `D-20260903-04` §2 T32 ② 행.
**재현** `diff accept/convergence.unclassified-text-absent.json accept/convergence.canonical-read-run-read-a.json` → **차이 0**. 두 파일은 같은 스키마 변경에서 동시에만 붉으므로 새 파일이 기존 파일이 못 잡는 것을 하나도 잡지 못한다.
**왜 결함인가** 발주문이 *「기존 accept 인스턴스 하나를 복제해 그 필드만 바꿔라」* 라고 썼는데 accept 쪽은 바꿀 필드가 이미 `read-a` 라 **복제만 남았다**. 원장 T32 §3 ② 가 요구한 「유효 ACCEPT」의 양성 대조는 기존 인스턴스가 이미 제공하고 있었다. `D-04` §2 가 `ACCEPT_OK 14/14`(13→14)를 조건 충족의 증거로 인용하는데, 그 +1 은 증거를 더하지 않는다. 격은 낮으나 RC-4 와 같은 과다.

### RD-5 · LOW · §5 ③ 이 스키마에서 지운 문장이 `reader/` docstring 에 그대로 살아 있고, 폴백을 대조하던 유일한 시험은 표지 없이 우회됐다
**귀책 = 총괄 처분(반경·기록) · 발주자(무접촉 지정).**
**좌표** `reader/lib/run_checks.py:138-140`(docstring) · `:168`(폴백) · `tests/test_m1_reader.py:1231` · 남은 호출점 `tests/test_m1_reader.py:1191`·`tests/test_m2_read.py:2520`.
**재현**
```
to_convergence_payload(rows, spec)  →  canonical_selection.read_run = 'read-a-0f1c2d3'   # 새 enum 위반
docstring: "생략하면 provenance.read_runs[0] 에서 읽는다 — … 그 값이 곧 정본이다"
```
`provenance.read_runs[0]` 은 파이프라인 전체에서 **항상 역할 접미형**(`read.py:574-576`)이므로 폴백은 **계약이 거부하는 값만** 낸다. 원장 §5 ③ 이 스키마 `$comment` 에서 바로잡은 것이 정확히 이 오해인데, **같은 문장을 든 두 자리 중 한 자리만 고쳤다.**
**왜 결함인가** ⑴ `test_convergence_payload_validates_against_contract` 는 이름이 주장하는 범위(“판정서 조립이 계약을 만족한다”)보다 **좁은 것**을 증명하게 됐는데 그 사실을 적은 주석이 한 줄도 없다 ⑵ 폴백을 타는 호출점 **두 곳이 남았고 어느 것도 스키마에 물리지 않는다** — T32 의 「fail-closed 부수 이득」이 한 번 발화하고 꺼졌다 ⑶ `D-04` §5 백로그는 **코드**(`:168`)만 든다. ⑴은 `reader/` 무접촉을 지키면서 `tests/` 한 줄로 닫힌다.

### RD-6 · LOW · RC-6 재정정이 감사 원문의 귀책 라벨 하나를 바꿔 인용한다
**귀책 = 총괄.**
**좌표** `docs/decisions/D-20260903-03-round-b.md` §1 말미 `[재정정 2026-09-03 · 재감사 RC-6]`.
**재현** 재정정문 = *「**감사 원문의 귀책은** … RB-2 발주자(총괄) …」*. 감사 원문 `docs/lessons/2026-09-03-opus-audit-round-b.md:199` = **`**귀책 = 설계(발주자).**`**. 나머지 다섯은 원문과 맞는다.
**왜 적는가** RC-6 자체가 *「정정 문언이 감사의 귀책을 다시 좁게 센다」* 였고, 그 정정이 **원문을 인용한다고 선언한 자리**에서 한 라벨을 바꾼다. **다만 실질은 방어된다** — 감사 원문 RB-2 본문이 근거로 `SPEC-round-b0.md` 발주문을 명시로 들고(`설계 v18 AF-2` 와 함께), 이 리포에서 설계자·발주자·총괄은 같은 사람이다. 그래서 격은 LOW 이고 「사실 오류」보다 **인용 충실성**의 문제다.

---

## 6. Q4 · Q5 · Q6 판정

### Q4 — 명령되지 않은 hunk: **없음** (세 커밋 34 hunk 전건 대응)

| 커밋 | hunk | 명한 것 |
|---|---|---|
| B″ | `SPEC:385`·`:1315` (2) | §8 RC-3 「B″ ③」 |
| B″ | `tests/conftest.py` 신설 (1) | §8 RC-7 「B″ ⑥」 |
| B″ | `generate.py` 4 hunk | §8 RC-4 「B″ ④」 — 앞 셋(시그니처·return·언팩)은 넷째의 기계적 전제 |
| B″ | `test_m24_failure_table_contract.py:62` (1) | §8 RC-5 「B″ ⑤」 |
| B″ | `test_m24_failure_table_contract.py` 236·243·245 (3) | §8 RC-2 「B″ ②」 |
| B″ | `test_m24a` 6 hunk | §8 RC-1 「B″ ①」(`source_root` 주입 4 + unlink 1 + 경계 시험 3건 1) |
| B″ | `check_failure_table.py` 2 hunk | §8 [미검증] ⑤ 「B″ ⑦」 |
| T31 | `SPEC:534` (1) | 원장 T31 §3 ③ |
| T31 | `material_spec_md.py` 6 hunk | T31 §2 ⒜(import·센티넬·인자·기본값·A-2 문언 = §5 ①·10-b 블록) |
| T31 | `read.py:1934` (1) | T31 렌더 호출 — 발주문 「한 hunk 만」 · 실측 `grep -c '^@@'` = **1** |
| T31 | `test_m22` 5 hunk | T31 §3 ②(헬퍼 인자 2 + 분할 경계 문언 2 + 신설 시험 3건) |
| T32 | 스키마 3 hunk | T32 §3 ① ⓐⓑⓒ + §5 ③ |
| T32 | 픽스처 3 신설 + 매니페스트 1 | T32 §3 ② |
| T32 | `test_m1_reader.py:1231` (1) | `D-04` §4 총괄 처분(GAPS) |
| T32 | `test_m24_read_run_vocabulary_binding.py` 8 hunk | T32 §3 ①②③ |

**`conftest.py` 부작용 = 없음.** `tests/__init__.py` 부재 · 리포에 conftest 는 이 하나 · 리포 루트에 `test_*.py` 없음(이름 가림 불가) · `test_m16:34` 는 `if REPO not in sys.path` 로 가려 **이중 삽입 없음**. 단독 실행 5파일 초록(`python -m pytest`·venv `pytest` 양쪽) · 전체 스위트 두 모드 `773 passed`.

### Q5 — 총괄 기록의 정확성

| 항목 | 판정 |
|---|---|
| `D-03` §9 재현표(765·765 · 단독 73/10/89 · 관문 7종 두 모드 · self-test 36/36 · 골든 diff 0) | **전건 일치** — `--collect-only` 로 `00dd3f8` = **765** 확인, 단독 실행 73/10/89 실측 |
| `D-03` §9 양성 대조 RC-2 ⓐ(`1 failed, 9 passed`) | **전건 일치** — 내가 다시 심어 `1 failed, 9 passed` · 관문 `failure_rows=11 early_retry=3 exit_retry=6` rc=0 |
| `D-03` §9 양성 대조 RC-2 ⓑ(`2 failed, 8 passed` · `exit_retry=7`) | **전건 일치** |
| `D-03` §9 [미검증] ⑤ 대조(판정 문구 · EXIT=1 · 트레이스백 0) | **전건 일치**(두 모드) |
| `D-03` §9 RC-1 행 — *「수정 전 붉음은 레인 실출력으로 확인 · 총괄은 재현하지 않았다」* | **정직하고, 이제 닫혔다** — 내가 unlink 를 되돌려 `1 failed, 2 passed` 재현 |
| `D-03` §9 총괄 실수 기록(`git checkout` 으로 레인 미커밋 관문 hunk 동반 삭제 → 역적용 +7/−6 = 13행) | **참** — 커밋 diff 실측 `-6/+7`, `--stat` `13 +++++--` |
| `D-04` §1 경위(06:57 `1 failed, 772 passed` · 07:07 `773 passed`) | **정합** — `794c639` 수집 773 · 폴백 값 `read-a-0f1c2d3` 실측 재현 |
| `D-04` §2 조건 대조표 11행 | **전건 일치** — 특히 `cases=48 REJECT_OK 32/32 ACCEPT_OK 14/14`(계수는 맞으나 accept +1 의 증거력은 0 → RD-4) |
| `D-04` §3 재현(773·773 · 관문 7종 · grep 1 · 보호 경로 diff 0 · `read.py` hunk 1 · 11파일) | **전건 일치** — 11파일·겹침 0·hunk 1 실측 |
| `D-04` §4 「조기 판정서는 CP1 렌더 시점에 항상 실재한다」 | **참**(코드 경로 실측) — 다만 그 참임이 「부재 갈래」를 도달 불가로 만든다는 함의는 적히지 않았다 → RD-2 |
| `D-04` §4 tmpfs 사고 — 「발주문 §3 이 병렬 실행 금지를 적지 않았다(**발주자 오류**)」 | **참** — `SPEC-round-t31.md` §3 은 호출별 즉시 삭제만 명하고, 오히려 basetemp 를 **`/tmp`(1.5 GB tmpfs)** 로 지정했다. 자기 귀책을 정확히 짚었다 |
| `D-04` §5 백로그 2건 | **정확하되 좁다** — 폴백 **코드**만 들고 docstring·미피복 호출점은 안 든다 → RD-5 |
| **「발주자 오류」로 적히지 않은 것** | ⑴ T31 발주 반경이 `test_m2_read.py` 의 render 호출점을 빼서 레인이 호환 기본값을 발명할 수밖에 없었던 것(RD-1) ⑵ accept 픽스처 지시가 복제만 낳은 것(RD-4) ⑶ `reader/` 무접촉 지시가 docstring 정정까지 막은 것(RD-5) |
| 정본 무접촉 | **지켜졌다** — 시작·종료 HEAD `7355cf2` · tree `8dbcf82` · status 0행 |

### Q6 — 종결 자격

**PD-M2a 라운드 B 계열의 값과 집행은 감사상 닫혔다.** 원장 T31 ①~④·T32 ①~⑤·§5 ①③ 전건 충족, RC-1~RC-5·RC-7·[미검증] ⑤ closed, 정합 편집 4종·우회 3종 어디서도 조용한 통과가 없었고 골든이 두 번째 오라클로 실재한다. **다만 「지적 0」이 아니므로 PASS 는 아니다.**

**남은 것**(백로그 2건 외):

1. **RD-1 ~ RD-6** — 전부 값 공간 무변경(규율 11 ③ 공학·기록). RD-1 만 승인 표면에 닿으므로 우선.
2. **Owner 사후 확인 대기 6묶음** — `D-03` §8 RC-2 규율 11 판단 · `D-04` §4 셋(GAPS 처분 · `read.py` 렌더 hunk · tmpfs 발주자 오류) · 원장 §5 ①(A-2 임시 표지를 A 에서 붙인 것이 재량 범위였는가) · §5 ④(라운드 C 총괄 재량 넷).
3. **발주문 골격 개정이 아직 문서가 아니다** — 「두 full 순차 · basetemp 는 worktree 안」은 `D-04` §4 산문에만 있고 재사용되는 발주문 골격(`D-20260902-02` §5 8항)에 반영되지 않았다. 같은 사고가 두 라운드 연속으로 났다.
4. **B″ 자체는 별건 재감사를 받지 않았다** — 이 합본이 그것을 대신했고(§8 근거), 그 결정 자체는 이 보고가 검증했다(RC 전건 실측).
5. **재감사 [미검증] ①** (도출식 8종 각각이 정본 후속 재시도로 실제 고쳐지는가 = 수리 기제)은 여전히 열려 있다 — B″ 는 형식면만 닫았다.

---

## 7. [미검증]

1. **n건 갈린 신고의 실런 근거.** 실런 조기 판정서 3건은 `unclassified_dependents` 키를 갖되 **전부 빈 배열**이다(레인 보고는 「키를 가졌다」까지만 적었다). n행 표 경로를 실제로 밟은 런은 없고, 픽스처는 스키마 형태를 따른 합성물이다. 합집합 로직 자체는 `test_m22_early_payload_assembly` 가 따로 본다.
2. **porcelain `C`.** `git status` 가 `--find-copies-harder` 를 노출하지 않아 실물로 심지 못했다(`status.renames=copies` + 대용량 파일 복제로도 `A` 만 났다). 코드 갈래(`"R" in code` 가드로 복사원 보존)는 읽어 확인했다.
3. **`rename → 옛 경로 재생성` 의 순서 의존.** clone·차집합 0 으로 통과했으나, 그것은 오늘 git 이 `R` 레코드를 `??` 보다 먼저 내보내기 때문이다. 미러 루프는 레코드 순서에 의존하며 그 순서를 단언하는 시험은 없다.
4. **RD-1 의 전파 반경.** `render()` 직접 호출 2자리만 확인했다. 하류 스테이지(`freeze._render_parity`)가 판독본 바이트를 다시 보므로, RD-1 이 실제 런에서 발화하면 그쪽 판정도 함께 움직인다 — 발화 조건이 없어 재지 않았다.
5. **`-O` 아래 개별 심기.** 정합 편집 4종·우회 3종은 plain 에서만 돌렸다. 전체 스위트는 두 모드에서 `773 passed` 로 확인했다.
6. **골든 8,190칸의 값 자체.** T-7 이 오늘 값과 일치한다는 것만 봤고, 그 값이 참인지는 재지 않았다(직전 두 감사와 같은 이유 · 관문 표 T-7 행이 명시로 배제).
7. **historian 상호 체크 · `reader/schemas/` 계약면.** 세 커밋의 `reader/schemas` diff 0 이므로 발화 조건이 아니다.
8. **`D-04` §1 의 시각들**(06:34 발주 ~ 07:15 커밋)은 커밋 타임스탬프(`933c6ca` 07:15 · `794c639` 07:16)와 정합하나, 06:46 tmpfs 고갈 등 중간 시각은 레인 보고 외의 사료로 대조하지 않았다.

**FAIL 의 사유는 좁고, 그 무게중심은 이번에도 발주·설계 쪽이다.** 값과 집행은 전건 닫혔고 우회는 실패했다 — 도출식이 뚫리는 자리에서도 동결 골든이 붙잡았으니 RB-1 의 「단일 실패점」 우려는 실측으로 해소됐다. 남은 여섯 중 하나(RD-1)만 승인 표면에 닿는데, 그것은 **T31 발주 반경이 `render()` 의 다른 호출점을 빼는 바람에 레인이 반경 안에서 낼 수 있는 답이 호환 기본값뿐이었던** 결과다. 그 기본값이 실런 산출물 하나 위에서 「두 실행의 미분류 신고가 전건 일치」라는, 데이터가 뒷받침하지 않는 문장을 승인 화면에 실었다. 나머지 다섯은 전부 **한 줄에서 두 줄** 거리다.

VERDICT: FAIL
