# HANDOFF — 다음 세션은 여기서 시작한다

**작성 2026-09-01 · 갱신 2026-09-05(22차) · HEAD 는 `git log -1` 로 본다(여기 적으면 낡는다).**
**이 문서는 총괄 저작이다**(감수 원문이 아니다 · 규율 10).

---

## 0. 첫 화면 — 지금 무엇을 해야 하나

**★ 09-05 22차 갱신 — 재정 T37: PD-M2a 라운드 B 계열 종결 선언(① A) · 사후 확인 ⓡ~ⓥ 추인(② A)**(`ruling-20260905-02-T37.md` · 브리핑 `43141fdb-…` 2판 배너). 열린 사후 확인 = **없음**. **좌석 규약 갱신(ROUTING v2.1 · agents `b1aa4ae` 실측 · T37 §3)**: **M1b = astra high** · **M9(sol·astra 저작 감사) = fable xhigh(CLI · allowlist · 폴백 opus xhigh) · opus max 퇴출(L-053)** · M3 sol-coder high · M2 astra medium(약정) — 이 계열의 감사 7회는 당시 정본 opus max 로 돌았다(기록).
**지금 할 일 = PD-M2 잔여 좌표로 이동.** 후보 순서(총괄 안 · 다음 세션이 실측 뒤 확정): **[추기 16:0x] G-5 상신 발행 — 문서 `docs/decisions/D-20260905-01-g5-termination.md` · 브리핑 아티팩트 `492e8207-6c09-4e3e-a697-c610ab1c5f9c`(drafts `OWNER-BRIEF-T38-g5-termination.html`) · 회신 서식 `T38: ① A / ② A / ③ A` · **Owner 결정 대기 1건(재정 셋 묶음)**.** **[추기 15:5x] M1b astra high(M2a-1 발주문) = REVISE 6 · **BLOCKER MG-1**: G-5 가드가 T17 봉투 재진입을 끊음 → **라운드 M2a-1 = B-1 만**(v2) · **G-5 = 설계 메모 → Owner 상신**(종결 정의 · 원장 기입 시점 · 구 런 처분 · §28).** ⑴ **[정정 15:4x] 로드맵 정본은 재정 T15 §1 ⒜·T1 — 다음 = PD-M2a 러너 무결성 = B-1(레인 로그 검사를 디스크 기록본으로 · T3) + G-5(종결 재진입 멱등 가드) · 신규 재정 0 → 라운드 M2a-1**(발주문 drafts `SPEC-round-m2a1.md` · M1b astra high 도전 15:42 기동 `pd-lanes/astra-m1b-m2a1/`) → PD-M2b(G-1~G-4 · B-2) → PD-M2c. 「절차 문서 라운드」라는 앞 문언은 총괄 오기 — T33 ① 은 `8259075` 로 이미 집행됐다. 백로그 ⑵⑶⑸ 는 M2a-1 뒤 또는 M2c 골든과 함께 ⑵ 백로그 ⑴ reader 폴백 제거는 이식 단위(READER-VERSION · N15) — 별건 ⑶ ⑷ flaky 관측 · ⑹ LANE-RUNTIME 편입(이관 때) · ⑺ LEDGER 셀 형식. 발주문은 **M1b astra high** 를 거쳐 집행 · 감사는 **fable xhigh**(LANE-RUNTIME 「Fable 좌석 호출 경로」 + L-053 allowlist 규격 재독 뒤). **Owner 결정 대기 = 없음.**

> [정정 2026-09-05 · 22차] 아래 21차 문단의 「지금 할 일 = Owner 상신」은 **끝났다**(T37). 경위 보존용으로 남긴다.

**★ 09-05 21차 갱신 — 좁은 재감사 4(RH · 축소 범위 · opus max · `docs/lessons/2026-09-05-opus-audit-round-rg.md`) = PASS · 신규 0 · RG-1~3 closed · Q4 종결 자격 충족.** 기록 = `D-20260903-04` **§27**(계열 종합 · 백로그 7).
**지금 할 일 = Owner 상신 — PD-M2a 라운드 B 계열 종결 선언**(`/decision-brief` 페이지 **발행 완료 15:3x · 아티팩트 `43141fdb-89bf-4870-b109-e5bae583835a` · drafts `OWNER-BRIEF-T37-round-b-closure.html`** · 회신 = 종결 선언 + 사후 확인 ⓡⓢⓣⓤⓥ 추인). 선언 시 → `ruling-20260905-02-T37.md`(종결 + 추인) · RULINGS-LEDGER §2 · HANDOFF 첫 화면을 **PD-M2 잔여**(절차 문서 라운드 · 백로그 §27 ⑴~⑺) 좌표로 다시 쓴다. **정본 커밋 금지 상태 아님**(감사 종료).

> [정정 2026-09-05 · 21차] 아래 20차 문단의 「지금 할 일 = 재감사 4」는 **끝났다**(PASS). 경위 보존용으로 남긴다.

**★ 09-05 20차 갱신 — 라운드 RG 병합 `6173b96`**(RG-2 헬퍼 단위 시험 · sol-coder 1턴 · M1b astra high ME-1 경유 · 총괄 재현 811·811 · 관문 7종 · 네 칸 대조표 직접 재현). 기록 = `D-20260903-04` **§24** · 레인 보고 **§25**.
**[추기 15:0x] M1b astra high(재감사 4 발주문) = REVISE 4(MF-1~4 · 전부 LOW · §26) → 발주문 정정 · `6173b96` 메시지 §24→§25 오기 마커.**
**지금 할 일 = 재감사 4(RH · 축소 범위)** — 발주문 drafts `AUDIT-ORDER-round-rg.md`(핀 = 이 커밋) → M1b astra high(`pd-lanes/astra-m1b-audit4/`) → opus max 발주(사본 `~/projects/workspaces/pd-audit-round-rg` · 레인 디렉터리 `pd-lanes/opus-audit-round-rg/` · 감사 중 정본 커밋 금지) → 회수(원문 `docs/lessons/2026-09-05-opus-audit-round-rg.md` · §26 처분) → **PASS 면 PD-M2a 라운드 B 계열 종결 상신(`/decision-brief`)** · FAIL 이면 라운드 RH. 세션이 끊겼다면 레인 디렉터리 `status`/`STATUS` 의 `EXIT=` 로 회수.

> [정정 2026-09-05 · 20차] 아래 19차 문단의 「지금 할 일 = 라운드 RG」는 **끝났다**(`6173b96`). 경위 보존용으로 남긴다.

**★ 09-05 19차 갱신 — 좁은 재감사 3(opus max · `docs/lessons/2026-09-05-opus-audit-round-rf-t35.md`) = FAIL 3건(MED 1 · LOW 2 · 처분 `D-20260903-04` **§22** · DISPOSITIONS 168행). 값·집행은 네 라운드 연속 닫혔다(RF 7/8 closed · T35 ⑴⑵ · MB·MC·MD 전건 · hunk 0 · 실런 판독본 바이트 동일 · 37,060 입력 전수 본문 공백 0). RG-1 §13·HANDOFF 한정어 마커 누락(이 커밋에서 정정) · RG-2 비해시 중복 검사가 도달 불능이라 원복해도 초록(시험 1줄 → 라운드 RG · **M1b medium 이 놓친 한 건**) · RG-3 발주문 문구 중복(정정). 골격 ⒀ 추기(금지 문자열 조건은 반경 파일·함수로).**
**[추기 14:3x] M1b astra high(라운드 RG 발주문) = REVISE 1(ME-1 · §23 · 대조 축 정정) → 반영 후 sol 레인 기동(14:31 · `pd-lanes/sol-coder-round-rg/`).**
**지금 할 일 = 라운드 RG**(sol-coder · worktree `round-rg` · 발주문 drafts `SPEC-round-rg.md` → **M1b astra high**(확정 좌석 · 레인 디렉터리 `pd-lanes/astra-m1b-rg/`) → 집행 → 총괄 재현 → 병합 → 기록) → **좁은 재감사 4**(RH · opus max · **축소 범위** = RG-1~RG-3 폐쇄 + RG hunk + 전체 스위트 1모드 + 관문 · 종료 조건 마커 한 줄 · 감사 중 정본 커밋 금지) → **PASS 면 PD-M2a 라운드 B 계열 종결 상신**. **Owner 사후 확인(열린 것)** — ⓡ ⓢ ⓣ(후반부 근거 보강) · **ⓤ 골격 ⑿ 추기(러너 setsid) · ⒀ 추기(금지 문자열 조건 범위)** · **ⓥ 재감사 4 를 축소 범위로 정한 것**.

> [정정 2026-09-05 · 19차] 아래 18차 문단의 「지금 할 일 = M1b 런 3/3 → 재감사 3 회수」는 **끝났다**(FAIL 3 → §22). 경위 보존용으로 남긴다.

**★ 09-05 18차 갱신 — 라운드 RF 병합 `2d01e91` + 재정 T35 집행 병합 `4bb2579`**(한 worktree · 4번 발주 · blocked 3 · M1b astra 도전 2회 반영 · 두 커밋 반경 겹침 0 · 총괄 재현 pytest 두 모드·관문 7종·SUMMARY 행·차별 대조 축 (i) 직접 재현 = 구 구현에서 A-차별 3 + B (i) 2 만 붉음). 기록 = `D-20260903-04` **§18**(재현표 · 발주자 오류 12건 — 셋은 레인 blocked · 아홉은 M1b 가 집행 전 포착 · 감사 포착 0) · **§19**(3차 보고) · **§20**(4차 보고).
**[추기 13:1x] M1b 런 3/3 = REVISE 6(MD-1~MD-6 · `docs/lessons/2026-09-05-astra-m1b-audit3.md` · §21 · 전부 발주자 귀책 · 강등 없음 · 첫 기동은 세션 재개로 사망 → `setsid` 재기동 · 골격 ⑿ 추기). 파일럿 3/3 종료 · **ROUTING v2.1 은 그 사이 M1b 를 astra high 로 확정(L-052 ⑩)** — 다음 M1b 부터 high · 약정 블록 불요. 발주문 정정 뒤 재감사 3 발주.**
**지금 할 일 = M1b 런 3/3(재감사 3 발주문 도전 · drafts `AUDIT-ORDER-round-rf-t35.md` · 레인 디렉터리 `pd-lanes/astra-m1b-audit3/`) → 정정 → 좁은 재감사 3**(`좌석 M9` opus max · `RG-*` · 사본 `~/projects/workspaces/pd-audit-round-rf-t35` · 레인 디렉터리 홈 fs `pd-lanes/opus-audit-round-rf-t35/` · 대상 = `2d01e91` + `4bb2579` + 기록 커밋 · **감사 중 정본 커밋 금지**) → 회수(원문 `docs/lessons/2026-09-05-opus-audit-round-rf-t35.md` · DISPOSITIONS · D-04 §21 처분) → **PASS 면 PD-M2a 라운드 B 계열 종결 상신** · FAIL 이면 라운드 RG. 세션이 끊겼다면 레인 디렉터리 `status`(`EXIT=`)·`raw.json`/`FINAL` 로 회수. **Owner 사후 확인(누적 · 열린 것)** — ⓡ(재감사 2 처분·합본 결정·⒀⒁⑾) · ⓢ(M1b 상설화 방침 · astra 런 1·2 강등 없음 판정) · **ⓣ RF·T35 두 커밋을 한 worktree·한 레인으로 저작하고 반경별로 가른 것 · 차별 대조 축 (ii) 는 레인 실출력만으로 수락한 것**.

> [정정 2026-09-05 · 18차] 아래 17차 문단과 그 추기들의 「지금 할 일 = 라운드 RF+T35 발주 → 회수」는 **끝났다**(`2d01e91` · `4bb2579`). 경위 보존용으로 남긴다.

**★ 09-05 17차 갱신 — 라운드 RE 좁은 재감사 2(opus max · `docs/lessons/2026-09-05-opus-audit-round-re.md`) = FAIL 8건(MED 3 · LOW 5 · 처분 `D-20260903-04` **§15** · DISPOSITIONS 146행). 값·집행은 닫혔다(RE-4·5·6 closed · hunk 0 · 실런 판독본 3건 전후 sha256 동일 · 감사자 plain 2회 초록). 다섯이 다시 증명 방식 — RF-1 허용 실행값 확장에 시험 0(원복해도 전건 초록) · RF-2 「고유 변조 없음」은 탐색 공간의 함수(실제 고유 관할 = 계약+관문 사본 협조 편집 · 변조 H) · RF-3 §13 기제 귀속 무근거(공유 자원은 머신 수준) · RF-4 혼재 침묵 · RF-5 `[a,a]` 거짓 일치 · RF-6 N 단언 판별력 0 · RF-7 16차 줄 · RF-8 골격 ⒀ 한 방향. 전부 수용 → 문서 넷은 이 커밋(§13 재정정 · ⒀ 개정 · ⑾ 추기 `TMPDIR` · **⒁ 신설** 탐색 공간 명시) · 코드 넷 + ⒜ 주석은 **라운드 RF**.**
**[추기 12:0x] M1b astra 설계 도전(런 1/3 · `docs/lessons/2026-09-05-astra-m1b-rf-t35.md`) = REVISE 7(MB-1~MB-7 · 전부 발주자 귀책 · §16 · 강등 없음)** — 대상 = RF+T35 발주문 3차(sol-coder 가 집행 중이었음 · 1·2차는 blocked 로 반려: 행위시법 산출물 · SPEC 좌표 · 빈 메모 accept). 다음 = 3차 회수 → **4차 정정 발주**(MB-1·2·3·5·6 · drafts `SPEC-round-rf-t35-fix4.md`) → 재감사 3. **방침(사후 확인 ⓢ)**: 이 리포의 발주문은 앞으로 M1b(astra medium)를 거친 뒤 집행한다.
**[추기 12:1x] 3차 레인 회수 = 구현·검증 완주 · 계수 모순(MB-1)에서 blocked(`final-3.txt`) · M1b 2차 도전(런 2/3 · `docs/lessons/2026-09-05-astra-m1b-fix4.md`) = REVISE 6(MC-1~MC-6 · §17 · 강등 없음) → 4차 정정 발주문 v2 로 **4차 sol 레인 기동(같은 worktree · 3차 산출 위)** · 레인 디렉터리 `pd-lanes/sol-coder-round-rf-t35/`(3차 사료 = `final-3.txt`·`events-3.jsonl`·`status-3`). 회수 → 두 커밋 → 병합 → M1b 런 3/3(재감사 3 발주문) → 재감사 3.**
**Owner 결정(육성 「전부 추천대로 진행 부탁해」 · 11:1x)** = ⑴ `screening_memos[].read_run` enum 결속 ⓐ · ⑵ `reported_by` `maxItems: 2` ⓐ · ⑶ LANE-RUNTIME 함정 편입은 L-049·L-050 이관 때 · ⑷ 사후 확인 ⓖ~ⓠ 추인 → **재정 T35·T36**(`ruling-20260905-01-T35-T36.md` · **이 커밋** · RULINGS-LEDGER §2 색인 + §3 두 행 → 포인터 · 각 D 문서 `[확인 · T36]` 마커 · **사후 확인 ⓖ~ⓠ 닫힘 — 열린 것은 ⓡ 만**).
**지금 할 일 = 라운드 RF + T35 합본 발주 → 회수**(sol-coder · worktree `round-rf-t35` · 발주문 drafts `SPEC-round-rf-t35.md` · 레인 디렉터리 홈 fs `~/projects/workspaces/pd-lanes/sol-coder-round-rf-t35/` · **반경 둘이 겹치지 않으므로 커밋은 둘**(RF · T35) · 차별 대조는 ⒀ 개정판 두 방향 · `TMPDIR` 홈 fs) → 병합 → **좁은 재감사 3**(opus max · `RG-*` · RF+T35 합본 · 종료 조건 마커 한 줄) → PASS 면 **PD-M2a 라운드 B 계열 종결 상신**. 세션이 끊겼다면 레인 디렉터리의 `status`(`EXIT=`)·`final.txt` 로 회수한다. **Owner 사후 확인(신규)** — **ⓡ 재감사 2 RF-1~RF-8 전부 수용 · RF 와 T35 를 한 worktree 에 합본한 결정 · 골격 ⒁ 신설·⒀ 개정·⑾ 추기**.

> [정정 2026-09-05 · 17차] 아래 16차 문단의 「지금 할 일 = 좁은 재감사 2 회수」는 **끝났다**(FAIL 8 → §15). 경위 보존용으로 남긴다.

**★ 09-05 16차 갱신 — 라운드 RE 병합(`573dcdc` · RE-1·RE-3·RE-4 + 감사자 ⒜⒝ · sol-coder 1턴 · 레인 디렉터리 홈 fs · 총괄 재현 pytest 두 모드·관문 7종·self-test · **차별 대조 셋 = 새 시험 2건이 수리 전 코드에서 붉고 수리 후 초록 · RE-1 은 한 줄 삭제** · ⒜ 고유 변조 없음 **[정정 2026-09-05 · RF-2 · RG-1 — 「계약 단독 변조 안에서」 한정 · 계약+관문 사본 협조 편집(변조 H)에서는 T22 만 붉음 · §13 정정 마커]**). 기록 = `D-20260903-04` **§13**(재현표 · 차별 대조 · **일시 실패 4건**([미확인] → 정정 → **재정정 RF-3** · §13) — plain 1회차만 · 재실행 전건 초록 · 명단 3건은 총괄이 `tail` 로 잃음 → 골격 ⑽ 추기) · **§14**(레인 보고 전문).**
**지금 할 일 = 좁은 재감사 2 회수**(`좌석 M9` opus max · 발주 = 이 커밋 직후 · 대상 = `573dcdc` 전 hunk + RE-1~RE-6 폐쇄 + §13·§14 · 지적 ID **`RF-*`** · 격리 사본 `/home/laptop/projects/workspaces/pd-audit-round-re`(clone · **이 커밋** 체크아웃 · `.audit-sandbox` 마커) · 발주문 = drafts `AUDIT-ORDER-round-re.md` · **레인 디렉터리 = 홈 fs `/home/laptop/projects/workspaces/pd-lanes/opus-audit-round-re/`**(`status` 의 `EXIT=` · `raw.json` → `jq -r .result` = 원문 · `usage.json`) · 종료 조건 = status 는 `?? .audit-sandbox` 한 줄 · **감사 중 정본 커밋 금지**). **세션이 끊겼다면**: `status` 에 `EXIT=` 가 있으면 회수(원문 → `docs/lessons/2026-09-05-opus-audit-round-re.md` · 규율 10 머리말 · `지적 열거 =` · DISPOSITIONS §0·§1 · D-04 §15 처분) · 없고 프로세스도 없으면 사망(재발주) · PASS 면 **PD-M2a 라운드 B 계열 종결 상신** · FAIL 이면 라운드 RF.
**Owner 결정 2건(한 재정)** = ⑴ `screening_memos[].read_run` enum 결속(추천 ⓐ) ⑵ `reported_by` `maxItems: 2`(추천 = 넣는다) — 자료 = 아티팩트 `b1d1ce3c-…` · drafts `OWNER-DECISION-read-run-enum.html`. **Owner 사후 확인(누적)** — ⓖ~ⓟ(15차) + **ⓠ 일시 실패 4건 — 중복 인스턴스(같은 대화의 데몬 배경 잡)의 동시 pytest 와 시각이 겹친 것은 확인 · 기제는 머신 수준 자원 경합 가설(§13 재정정 RF-3 — 「같은 worktree」 귀속은 근거 없음) · 재실행 전건 초록 위에서 병합** · 그 인스턴스는 커밋·잔재 0 보고 · Owner 가 그 배경 잡을 닫아야 한다 · 기억 `duplicate-session-instance-trap`.

> [정정 2026-09-05 · 16차] 아래 15차 문단의 「지금 할 일 = 라운드 RE 발주 → 회수」는 **끝났다**(`573dcdc`). 경위 보존용으로 남긴다.

**★ 09-05 15차 갱신 — 라운드 RD 좁은 재감사(opus max · `docs/lessons/2026-09-05-opus-audit-round-rd.md`) = FAIL 6건(MED 1 · LOW 5 · 처분 `D-20260903-04` **§12** · DISPOSITIONS 138행). 값·집행은 닫혔다(RD-1·4·5·6 closed · 명령되지 않은 hunk 0 · 실런 판독본 3건 전후 바이트 동일 · 변조 10종 중 8 붉음). 무게중심 = 「고쳤다」의 증명 방식 — RE-1 RD-3 교체 단언이 다시 항진식(발주자 술어 지정) · RE-2 RD-3 양성 대조가 수리 전에도 붉음 · RE-3 10-b 사슬 `else` 부재(길이 ≥3 에서 본문 공백) · RE-4 RD-2 가드가 판별 불가 + 발화 시 「구 판」 거짓 출처 · RE-5·RE-6 총괄 기록. 전부 수용 → RE-5·RE-6 이 커밋 · 골격 **⒀ 차별 대조** 신설(`D-20260902-02` §5) · 감사자 ⒞(`reported_by` `maxItems: 2`)는 값 공간 축소라 **Owner 상신 추가**.**
**지금 할 일 = 라운드 RE 발주 → 회수**(sol-coder · worktree `round-re` · 발주문 = drafts `SPEC-round-re.md` · 레인 디렉터리 = **홈 fs** `~/projects/workspaces/pd-lanes/sol-coder-round-re/` · 반경·양성 대조(전부 차별 대조 · 골격 ⒀) = `D-04` §12 「다음」 · ① RE-1 죽은 연언 삭제 + 고유 변조 기재 ② RE-3 `else` 갈래 + 전역성 시험 + `dict | None` ③ RE-4 가드 제거(러너는 부재를 실패로) + 부재 시 실패 시험 + SPEC 「재렌더」 삭제) → 총괄 재현(차별 대조 셋 = 수리 전 초록·수리 후 붉음 실출력) → 병합 → **좁은 재감사 2**(opus max · 지적 ID `RF-*` · 종료 조건은 「status = `?? .audit-sandbox` 한 줄」로) → PASS 면 **PD-M2a 라운드 B 계열 종결 상신**.
**Owner 결정 2건** = ⑴ `screening_memos[].read_run` enum 결속(`ruling-20260902-02` §5 ② · 추천 ⓐ) ⑵ **`unclassified_dependents[].reported_by` 에 `maxItems: 2`**(재감사 ⒞ · `RULINGS-LEDGER.md` §3 신설 행 · 추천 = 넣는다) — 둘 다 `convergence.schema.json` 의 read_run 값 공간이라 **한 재정으로 묶어** 올린다. 결정 자료(그림) = 아티팩트 `b1d1ce3c-…` · drafts `OWNER-DECISION-read-run-enum.html`. **Owner 사후 확인(누적)** — ⓖ~ⓞ(14차) + **ⓟ 재감사 RE-1~RE-6 전부 수용 · RE-4 처분을 「가드 제거·부재 = 실패」로 정한 것 · 골격 ⒀ 신설**.

> [정정 2026-09-05 · 15차] 아래 14차 문단의 「지금 할 일 = 좁은 재감사」는 **끝났다**(FAIL 6 → §12). 경위 보존용으로 남긴다.

**★ 09-05 14차 갱신 — 라운드 RD 병합(`87cf794` · RD-1~RD-5 · sol-coder 1턴 · 총괄 재현 pytest 두 모드·관문 7종 두 모드·self-test·cmp·AST·hunk 1·보호 반경 0 · 양성 대조 RD-1·RD-3·RD-4·RD-5). 기록 = `D-20260903-04` **§10**(재현표 · 총괄 오류 2건 — ① 레인 산출을 tmpfs 스크래치에만 둬 09-04 소거로 `final.txt` 유실 → 세션 transcript 에서 복구(drafts `LANE-REPORT-round-rd.recovered.txt` · 바이트 동일성 [미검증]) ② basetemp `.gitignore *` 조건을 골격 ⑾ 에 늦게 적음) · **§11**(레인 보고 복구본). 발주문 골격 = `D-20260902-02` §5 **⑾ 추기 · ⑿ 신설**(레인 디렉터리·발주문 원본은 홈 fs · 스크래치 금지). RD-6 은 `9817bec` D-03 §1.**
**지금 할 일 = 좁은 재감사**(`좌석 M9` opus max · sol 저작 → opus · 대상 = `87cf794` 전 hunk + RD-1~RD-6 폐쇄 + 이 커밋의 기록(D-04 §10·§11 · 골격 ⑾⑿ · 14차) · 지적 ID **`RE-*`** · 격리 사본 `/home/laptop/projects/workspaces/pd-audit-round-rd`(`git clone --no-hardlinks` · **이 커밋** 체크아웃 · 루트 `.audit-sandbox` 마커 path/pin/order/disposable) · 발주문 = drafts `AUDIT-ORDER-round-rd.md` · 레인 디렉터리 = **홈 fs** `/home/laptop/projects/workspaces/pd-lanes/opus-audit-round-rd/`(골격 ⑿ · `runner.sh`·`status`·`raw.json`·`out.txt`·`usage.json`) · 호출 = `claude -p --model claude-opus-5 --effort max --output-format json`(`CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000` · `MEMORY_HOOKS=off` · cwd = 사본) · basetemp 홈 fs `pd-audit4-basetemp` · **감사 중 정본 커밋 금지**). 회수 = 원문 `docs/lessons/2026-09-05-opus-audit-round-rd.md` 보존(규율 10 · `지적 열거 =` 한 줄 · 마커) + DISPOSITIONS §0·§1 + 처분(D-04 §12) → **PASS 면 PD-M2a 라운드 B 계열 종결 상신**(백로그 셋 = D-04 §5) · FAIL 이면 라운드 RE.
**Owner 사후 확인(누적 · 미확인)** — ⓖ RC-2 규율 11 판단 ⓗ B″ 감사 합본 결정 ⓘ B″ 총괄 실수 ⓙ GAPS 폴백 우회 ⓚ `read.py` 렌더 hunk ⓛ 원장 `ruling-20260902-02` §5 ①(A-2 임시 표지) · **ⓜ 합본 감사 RD-1~RD-6 전부 수용 처분**(`9817bec` · D-04 §9) **ⓝ 골격 ⑾ 추기·⑿ 신설**(규율 11 공학 재량) **ⓞ 레인 보고를 transcript 복구본으로 대체**(D-04 §10 ①). **Owner 결정 1건** = `screening_memos[].read_run` enum 결속(`ruling-20260902-02` §5 ② · 추천 ⓐ 같은 `$defs` 참조).

> [정정 2026-09-05 · 14차] 아래 13차 문단의 「지금 할 일 = 라운드 RD 발주 → 회수 → 병합」은 **끝났다**. 13차 문단과 그 아래 추기들의 스크래치 경로(`/tmp/claude-1000/…/scratchpad/…`)는 09-04 소거로 **전부 죽은 경로**다 — 발주문은 drafts `SPEC-round-*.md`·`AUDIT-ORDER-*.md`, 감사 원문은 `docs/lessons/`, RD 레인 보고는 drafts `LANE-REPORT-round-rd.recovered.txt`. 경위 보존용으로 남긴다.

**★ 09-03 13차 갱신 — 합본 감사(B″+T31+T32 · opus max · `docs/lessons/2026-09-03-opus-audit-round-b2-t31.md`) = FAIL 6건(MED 1 · LOW 5 · 처분 `D-20260903-04` §9 · DISPOSITIONS 131행). 값·집행은 전건 closed(RC 전건 · T31/T32 조건 전건 · 우회 3종 실패 — 골든이 둘째 오라클). RD-1 = 렌더 호환 기본값이 최종 판정서로 갈음 → CP1 「전건 일치」 무근거 선언(발주 반경 귀책). 전부 수용 → 라운드 RD 발주**(sol-coder · worktree `round-rd` · RD-1~RD-5 · 발주문 = drafts `SPEC-round-rd.md` · **basetemp 는 worktree 안 · 두 full 순차**(발주문 골격 ⑽⑾ 신설)). RD-6 · RD-4 인용 · 백로그 확장은 이 커밋. 회수 → 총괄 재현(양성 대조: 실런 `cim-fp-3` 구 호출 렌더 · RD-3 변조) → 병합 → **좁은 재감사**(RD 폐쇄) → PASS 면 **PD-M2a 라운드 B 계열 종결 상신**.
**[추기 07:52] 라운드 RD 를 발주했다** — worktree `.worktrees/round-rd`(브랜치 `round-rd` · `9817bec` 분기) · 발주문 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-rd.md`(= drafts `SPEC-round-rd.md` · §1 ①~⑤ · §2 양성 대조 셋 · **basetemp 는 worktree 안 `.pytest-basetemp/` · 두 full 순차**) · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-rd/`(`status` PID/START/EXIT · `final.txt`) · 예상 20~40분. 회수 = 총괄 재현(홈 fs basetemp) → 커밋 → rebase·ff → 좁은 재감사(opus max · RD 폐쇄 · 감사 중 정본 커밋 금지) → PASS 면 종결 상신.
**Owner 사후 확인(누적 · 미확인)** — ⓖ RC-2 규율 11 판단 ⓗ B″ 감사 합본 결정 ⓘ B″ 총괄 실수 ⓙ GAPS 폴백 우회 ⓚ `read.py` 렌더 hunk ⓛ 원장 `ruling-20260902-02` §5 ①(A-2 임시 표지를 A 에서 붙인 것) · §5 ④(라운드 C 재량 넷 — T34 ⓒ 로 이미 확인됨). **Owner 결정 1건** = `screening_memos[].read_run` enum 결속(§5 ② · 추천 ⓐ).

> [정정 2026-09-03 · 13차] 아래 12차 문단의 「지금 할 일 = 합본 감사 발주」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 12차 갱신 — T31·T32 소라운드 병합(T31 `933c6ca` · T32 `794c639` · sol-coder 1턴 + resume 1 · 총괄 재현 773·773 · 관문 7종). 기록 = `docs/decisions/D-20260903-04-t31-t32.md`(GAPS 처분 = 폴백 우회 한 줄 · tmpfs 사고 재발 · 백로그 2).**
**지금 할 일 = 합본 감사 발주**(opus max · 대상 = B″ `00dd3f8` + T31 `933c6ca` + T32 `794c639` · 격리 사본 + 마커 · **감사 중 정본 커밋 금지** · 지적 ID `RD-*`) → PASS 면 PD-M2a 라운드 B 계열 종결 상신 · FAIL 이면 지적 반입 → 수리.
**환경 규율 개정(발주문용)** — 두 full pytest 는 **순차** · basetemp 는 **worktree 안**(`<worktree>/.pytest-basetemp` · 홈 fs · 끝나면 삭제)으로 — tmpfs `/tmp` 는 clone 다수 시험(B-0 · 재감사)에 1.5 GB 로 부족하다(06:46 재발 · D-04 §4).
**Owner 사후 확인(신규)** — ⓙ GAPS 처분(폴백 우회 시험 한 줄 · `reader/` 폴백은 백로그) ⓚ `read.py` 렌더 호출 hunk 허용.

> [정정 2026-09-03 · 12차] 아래 11차 문단의 「지금 할 일 = T31·T32 소라운드 발주/회수」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 11차 갱신 — 라운드 B″ 병합(`00dd3f8` · RC-1~5·7 + [미검증] ⑤ · sol-coder 1턴 · 총괄 재현 765·765 · 단독 실행 3파일 · 양성 대조 셋). 기록 = `D-20260903-03` §9(총괄 실수 1건 — 되돌림이 레인 hunk 를 지워 재적용).**
**지금 할 일 = T31·T32 소라운드 발주**(`좌석 M3` sol-coder · worktree `round-t31` · 상류 = `ruling-20260902-02-T28-T32.md` T31 §2·§3(CP1 조기 합집합 블록 · `engine/render/material_spec_md.py` · 렌더 시험 · SPEC §1.5 · 스키마 diff 0) + T32 §2·§3(`contracts/schemas/convergence.schema.json` `$defs` 하나 · 참조 두 곳 · `check_schema_enforcement` 무효/유효 · 러너 판정서 양성 대조 · `runs/**` 무접촉 · `$comment` 기록) + §5 ①(A-2 임시 표지 문언을 블록을 가리키게) · §5 ③(`$comment` 어긋남 수정) · **§5 ② `screening_memos[].read_run` 은 재정 전 무접촉** · 설계 v18 ⑫). 발주문 골격 = `D-20260902-02` §5 ⑹~⑼ + 환경 규율 + 「감사 중 정본 커밋 금지」. 그 뒤 **감사 = B″ + 소라운드 합본**(opus max · sol 저작).
**[추기 06:34] T31·T32 소라운드를 발주했다** — worktree `.worktrees/round-t31`(브랜치 `round-t31` · `07dbd43` 분기) · 발주문 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-t31.md`(= drafts `SPEC-round-t31.md` · T31/T32 파일 분리 · §5 ①③ 포함 · `screening_memos` 무접촉 · 폴백 확인 항목) · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-t31/`(`status` PID/START/EXIT · `final.txt`) · 예상 30~60분. 회수 = 총괄 재현 → worktree 에서 **두 커밋**(T31 · T32) → rebase·ff → **합본 감사 발주**(opus max · B″ + T31 + T32 · 감사 중 정본 커밋 금지).
**Owner 사후 확인(신규)** — ⓘ B″ 총괄 실수(관문 hunk 되돌림·재적용 · §9).

> [정정 2026-09-03 · 11차] 아래 10차 문단의 「지금 할 일 = 라운드 B″ 발주/회수」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 10차 갱신 — B′ 좁은 재감사 = FAIL 7건(MED 2 · LOW 5 · `docs/lessons/2026-09-03-opus-audit-round-b-prime.md` · 처분 `D-20260903-03` §8 · DISPOSITIONS 125행). RB-1(HIGH)은 닫혔다 — 감사가 정합 편집을 6종으로 확장해도 도출식 시험이 전건 붉음(관문 7종은 초록). RC-1 = 델타 미러 rename 경계 · RC-2 = 도출식 배제 근거의 우연·후건 무재정 → 12 우주 − 명시 배제 3집합으로 재작성. 전부 수용 → 라운드 B″ 발주**(sol-coder · worktree `round-b-2` · 발주문 = drafts `SPEC-round-b-2.md` · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b-2/`). B″ 의 감사는 **T31·T32 소라운드 감사에 합본**(§8 근거 · Owner 가 다르게 보면 별건). 회수 = 총괄 재현(rename 경계 · 정합 편집 2종 양성 대조) → 병합 → **T31·T32 소라운드 발주**.
**[추기 05:59] 라운드 B″ 를 발주했다** — worktree `.worktrees/round-b-2`(브랜치 `round-b-2` · `eb1cee4` 분기) · 발주문 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-b-2.md`(= drafts `SPEC-round-b-2.md` · §1 ①~⑦ · §2 양성 대조 셋) · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b-2/`(`status` PID/START/EXIT · `final.txt`) · 예상 20~40분. 회수 = 총괄 재현(§4 + 양성 대조 셋 직접) → worktree 커밋 → rebase·ff → **T31·T32 소라운드 발주**(감사 합본).
**Owner 사후 확인(신규)** — ⓖ RC-2 처분의 규율 11 판단(「12 우주 단언 + 골든이 재정을 강제하므로 기본값 입법 아님 → 상신 불요」 · §8) ⓗ B″ 감사를 소라운드 감사에 합본한 결정.

> [정정 2026-09-03 · 10차] 아래 9차 문단의 「지금 할 일 = 좁은 재감사 발주」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 9차 갱신 — 라운드 B′ 병합(`3d599f6` · RB-1·2·5·6 + [미검증] ②·⑧ 수리 · sol-coder 1턴 · 총괄 재현 762·762 · 관문 7종 · 양성 대조 둘 직접 재현). 기록 = `D-20260903-03` §7. RB-3 = 설계 v19 부록 · RB-4 = §1 정정.**
**지금 할 일 = 좁은 재감사 발주**(opus max · 대상 = B′ `3d599f6` 의 hunk 전건 + RB-1~RB-6 폐쇄 판정 + [미검증] ②·⑧ · 격리 사본 + 마커 · **감사 중 정본 커밋 금지**) → PASS 면 **T31·T32 소라운드** 발주(설계 v18 §2 T31/T32 · `screening_memos[].read_run` 상신은 별건) · FAIL 이면 지적 반입 → B″.

> [정정 2026-09-03 · 9차] 아래 8차 문단의 「지금 할 일 = 라운드 B′ 발주/회수」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 8차 갱신 — opus max 합본 감사 = FAIL 6건(HIGH 1 · MED 2 · LOW 3 · `docs/lessons/2026-09-03-opus-audit-round-b.md` · 처분 `D-20260903-03` §6 · DISPOSITIONS 118행).** 값·집행·A′·C′ 이행은 전건 closed. RB-1(출구 재시도 8종의 독립 오라클 부재 — 정합 편집이 전 관문·전 시험 통과) · RB-2(B-0 시험이 정본 main 을 clone) · RB-3(설계 T-4 문언 거짓) · RB-4~6(LOW). **전부 수용 → 라운드 B′ 발주**(sol-coder · worktree `round-b-prime` · 발주문 = drafts `SPEC-round-b-prime.md` · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b-prime/` · 반경 = 시험 3파일 + 생성기 + CLAUDE.md 일곱째 행 + SPEC 두 자리 · **계약·엔진·관문·골든 무접촉**). 회수 = 총괄 재현(양성 대조 둘 포함) → 병합 → 좁은 재감사(opus max · RB-1~6 폐쇄 여부만) 또는 T31·T32 소라운드로.
**설계 v19 부록**(RB-3 정정 · RB-1 처분)은 drafts `T26-DESIGN-v19-addendum.md`. **[추기 04:33] 라운드 B′ 를 발주했다** — worktree `.worktrees/round-b-prime`(브랜치 `round-b-prime` · `815a67d` 분기) · 발주문 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/order-round-b-prime.md`(= drafts `SPEC-round-b-prime.md` · §2 ①~⑧ · 양성 대조 둘 필수) · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b-prime/`(`status` PID/START/EXIT · `final.txt`) · 예상 20~40분. 회수 = 총괄 재현(§4 + 양성 대조 둘 직접) → worktree 커밋 → rebase·ff → 좁은 재감사 발주(opus max · RB 폐쇄 여부 · 감사 중 정본 커밋 금지). 감사 발주문 교훈 = 「감사 중 정본 커밋 금지 또는 저자 대조」(D-03 §6 말미).

> [정정 2026-09-03 · 8차] 아래 7차 문단의 「지금 할 일 = opus max 감사 발주/회수」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 7차 갱신 — 라운드 B 가 병합됐다(`1d29c8b` · sol-coder 1턴 완주 · blocked 0 · 총괄 재현 전건 일치 · 관문 **7종** 두 모드 exit 0 · pytest 761). 기록 = `docs/decisions/D-20260903-03-round-b.md`.** 재정 T26·T28·T29·T30 의 집행 실물 = `contracts/stages/read.yaml#failure` 11행 · `engine/stages/read.py` 상수·진입 가드·`_failure_verdict` · `tools/check_failure_table.py`(일곱째 관문 · `--self-test` 36) · T-1~T-13 시험 · 골든 T-7.
**[추기 03:46] opus max 감사를 발주했다** — 사본 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/audit-round-b`(detached `94ca66f` · 마커 `.audit-sandbox` pin `94ca66f14efa8f1bce0ab6a16cea76dab90dbd2d`) · 발주문 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/AUDIT-ORDER-round-b.md`(= drafts `AUDIT-ORDER-round-b.md` · 여덟 질문 · 지적 ID `RB-*`) · 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/opus-audit-round-b/`(`runner.sh` · `status` PID/START/EXIT · `out.txt` = 감사 원문 · `err.txt`) · 호출 `claude -p --model claude-opus-5 --effort max`(환경변수 2종 · setsid) · 정본 트리 지문 감사 전 `de4e54c9e1c3fdf6ad454c36aee0c504ba771b83`(끝난 뒤 같은 값 + `git status` 0행 확인) · 예상 30~60분. 회수 = `out.txt` 전문 → `docs/lessons/2026-09-03-opus-audit-round-b.md`(머리말 · `지적 열거 =`) → DISPOSITIONS §0/§1 → FAIL 이면 B′ 수리 발주 · PASS 면 T31·T32 소라운드.
**지금 할 일 = 감사 회수**(위) — 발주 골격은 아래 그대로 —**(발주 골격)**(ROUTING M9 · sol 저작 → opus) — 합본 범위 A′ `99fad78` · C′ `867b95b` · B-0 `6f93519`+골든 `47e437c` · B `1d29c8b` · 격리 사본(`git clone --no-hardlinks` · detached · `.audit-sandbox` 마커 path/pin/order/disposable · SPEC §8.3 9항) · 호출 = `claude -p --model claude-opus-5 --effort max`(LANE-RUNTIME 「`claude -p` 레인 러너 환경변수 2종」 `CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000` · `MEMORY_HOOKS=off` · setsid 배경 + `EXIT=` 마커) · 발주문 골격 = `AUDIT-ORDER-round-c.md`(drafts) 형태 + 라운드 A 감사 교훈(A-1: 변조가 읽는 구간을 실측). FAIL → 지적 반입(규율 10 · `지적 열거 =` · DISPOSITIONS) → B′ 수리 · PASS → **T31·T32 소라운드** 발주(설계 §2 T31/T32 · `screening_memos[].read_run` 상신은 별건 유지).
**커밋 전 관문은 이제 7종이다** — `check_failure_table` 포함(`CLAUDE.md` §6 표 · 실패표를 고치면 발화).

> [정정 2026-09-03 · 7차] 아래 6차 문단의 「지금 할 일 = 라운드 B 발주/회수」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 6차 갱신 — 라운드 B-0 병합(`6f93519`) · 골든 manifest 커밋(`47e437c` · 8,190칸 · 오라클 불일치 0) · T33 ① 집행(`8259075` · 절차 문서 → `reader/procedure/HISTORY.md`)이 끝났다.** 경위·재현표·발주자 오류 4건 = `docs/decisions/D-20260903-02-round-b0.md`.
**[추기 02:38] 라운드 B 를 발주했다** — 레인 디렉터리 `/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b/`(`runner.sh` · `status` 첫 줄 PID · `events.jsonl` · `final.txt` · 발주문 = `order-round-b.md` = drafts `SPEC-round-b.md` · 79,579 B · 설계 §0~§3+§6 첨부) · worktree `.worktrees/round-b`(브랜치 `round-b` · `33e96f3` 분기) · 예상 1~2시간 · 세션이 죽었으면 `status` 의 `EXIT=` 와 `final.txt` 크기로 판별(EXIT=0 인데 0바이트 = 사망 · resume 1회 허용). 회수 뒤 = 총괄 재현(§4 수락 명령 · pytest 는 `--basetemp` 홈 fs) → worktree 커밋 → rebase·ff → opus max 감사 발주.
**지금 할 일 = 라운드 B 회수**(위) — 발주 골격은 아래 그대로 — `좌석 M3` sol-coder(sol high · workspace-write) · worktree `round-b`(HEAD 에서 분기) · 첨부 = 설계 v18 §2 전문(`~/projects/workspaces/patent-docent-session-drafts/T26-DESIGN-v18.md` §2.1~§2.11 · §6 골격) · **C-5 반경 고지** 동반(SPEC §8.3 7항·관문표 = C 병합본 기준) · D-02 §5 ⑹⑦⑧⑨ 골격 → 총괄 재현 → 병합(관문 6→7 · `tools/check_failure_table.py`) → **opus max 감사**(A′·C′·B-0·B 합본 · sol 저작 → opus) → T31·T32 소라운드.
**환경 규율(이 세션 실측)** — pytest 는 반드시 `--basetemp` 를 홈 fs 에(`/tmp` 는 tmpfs 1.5 GB · 02:07 레인 사망 원인) · `/tmp/pytest-of-laptop`·`/tmp` 전체 삭제 금지(nd-magnet 세션 게이트가 ~11:00 까지 돈다 · 가득 차면 그 세션에 먼저 알린다) · `pkill -f` 금지(PID 로).
**병렬 세션 조율(nd-magnet · `~/.claude/agents`)** — 그 세션이 `sol-auditor.md` 를 얇은 래퍼 + `bin/sol-audit.sh` 로 바꿨다(agents HEAD). **다음 sol 감수 발주 전에 그 본문 ②(preflight→run 배경→poll→finish)를 재독**하고 발주문 형태를 맞춘다(어긋나면 스크립트 쪽을 고친다). agents LEDGER 는 제3 세션(기억 체계 v2)이 L-048 을 라이브로 쓰는 중 → 커밋되면 **L-049(nd-magnet · `LEDGER-PENDING-L049-2026-09-03.md`) → L-050(이 세션 · T33 ③)** 순으로 총괄이 옮긴다. `~/.claude/CLAUDE.md` 9·15행 SessionStart 문구는 제3 세션 변경(Owner 확인 사항).
**★ Owner 사후 확인 — 전건 확인 완료(재정 T34 · 09-03 · `ruling-20260903-02-T34.md` · 육성 「Owner 사후 확인 항목들 확인 완료 했어」).** 아래 ⓓ~ⓕ 와 4차 ⓐ~ⓒ · 3차 잔여 ⓖ·ⓗ 가 추인됐다. **남은 Owner 결정 = 상신 1건**(`screening_memos[].read_run` enum 결속 · T32 §5 ② · 추천 ⓐ · `RULINGS-LEDGER.md` §3) — 사후 확인이 아니라 재정이 필요한 값 공간 판단이다.
**Owner 사후 확인(추가 · 확인됨)** — ⓓ T33 ① 을 골든 뒤로 미룬 순서 결정(총괄 재량 · `ruling-20260903-01-T33.md` §3 2) ⓔ B-0 fixture 의 상설 `99fad78` diff 조항 삭제(발주자 오류 정정 · D-02 §5 ⑶) ⓕ `/tmp` 삭제로 nd-magnet 게이트 30분 손실(D-02 §1 02:09).

> [정정 2026-09-03 · 6차] 아래 5차 문단의 「B-0 회수 …」·「F1·F2 는 골든 커밋 뒤에 적용한다」는 **끝났다**. 경위 보존용으로 남긴다.

**★ 09-03 5차 갱신 — T26 설계가 M1b 도전 17차에서 PASS 했다**(v18 · `docs/lessons/2026-09-02-sol-challenge-t26-design-v18.md` · 지적 0 · 결정 공백 0).
16차는 FAIL 1(AJ-1 MED · `-v17.md` · 처분 `D-20260902-02` §22) · 17차 기록 = 같은 문서 §23. **T26 §3 ①(PASS 전 착수·커밋 금지)이 해제되어 라운드 B-0 를 발주했다.**
지금 할 일 = ① **B-0 회수** — 좌석 M3 sol-coder(sol high · workspace-write) · worktree `.worktrees/round-b0`(브랜치 `round-b0` · 이 커밋에서 분기) ·
산출 = `tests/fixtures/read-failure-grid/generate.py` · `validate_manifest.py` · `tests/test_m24a_failure_grid_generator.py` · 레인 디렉터리 =
`/tmp/claude-1000/-home-laptop/a5006bbe-a0f2-432d-97d2-b3b14a2f84eb/scratchpad/sol-coder-round-b0/`(`runner.sh` · `status` 첫 줄 PID · `events.jsonl` · `final.txt`; 세션이 죽었으면 `status` 의 `EXIT=` 유무로 판별) ·
발주문 = `~/projects/workspaces/patent-docent-session-drafts/order-round-b0-generator.md`(B0_BASE 채운 판 = `SPEC-round-b0.md`) → 총괄이 §3 수락 명령 재현 → worktree 커밋 → main 에 rebase·ff 병합
② 총괄이 main 에서 설계 §2.8 「생성 명령」 블록 실행(`99fad78` 트리 · `PYTHON_BIN=.venv/bin/python`) → 골든 manifest 커밋 ③ **라운드 B** 발주(설계 v18 §2 전문 첨부 · C-5 반경 고지 = SPEC §8.3 7항·관문표) → opus max 감사(A′·C′·B-0·B 합본) → 병합(관문 6→7) ④ T31·T32 소라운드.
설계 PASS 판 = `~/projects/workspaces/patent-docent-session-drafts/T26-DESIGN-v18.md`(리포 밖 · B 발주문 첨부로 들어온다). 도전 비용 = 17회(감수 원문 v2~v18 + 자문 1).
**별건 — `/claude-api prompt-audit`**: Owner 가 F1~F7 을 승인했다(**재정 T33** · `ruling-20260903-01-T33.md` · 상신 전문 `D-20260903-01-prompt-audit.md`). **F7(`CLAUDE.md` §6 → `docs/IMPLEMENTATION-HISTORY.md`)과 F3~F6(agents 4파일)은 집행됐다.** **F1·F2(`reader/procedure/*.md` → `HISTORY.md`)는 골든 manifest 커밋 뒤에 적용한다** — 설계 §2.8 생성 사전조건이 `reader/` 경로 무변경을 요구하기 때문(D-01 §0). 적용 diff = drafts `PROMPT-AUDIT-2026-09-03-patent-docent.diff` 의 `reader/procedure/*` 부분(`git apply --include='reader/procedure/*'` · 검증 완료). **agents LEDGER L-049 등재 보류** — 병렬 세션(기억 체계 v2 게이트)이 `~/.claude/agents/LEDGER.md` L-048 을 라이브로 쓰고 있다. 조용해지면 등재. **B-0 재현 시 주의**: 발주문의 「clone 의 `engine contracts reader` 99fad78 이후 무변경 아니면 fail」 시험 조항은 상설 시험으로는 틀렸다(F1·F2 적용 순간 영구 실패) — 병합 전에 좁히거나 뺀다(D-01 §0).

> [정정 2026-09-03 · 5차] 아래 09-02 4차 문단은 16차 도전 **중** 문안이다 — 「4차 도전 결과 회수 → PASS 면 …」·「16차 도전 중(09-03 01:07)」·「§1(111행)」은 **낡았다**(지금 112행). 경위 보존용으로 남긴다.

**★ 09-02 4차 갱신 — 라운드 C 감사(FAIL 6건)와 그 수리 C′(`867b95b`)가 끝났고, T26 설계는 M1b 도전 세 번 FAIL
(v1 B-1~B-7 · v2 V-1~V-8 · v4 W-1~W-4) + 자문 REVISE(N-1~N-7) 를 거쳐 v5 로 4차 도전 중이다. **[추기] 4차도 FAIL(X-1~X-3 · 결정 공백 0 · `-v5.md`) → v6(관문이 승인 실패표 골격 전체를 상수로) → 5차도 FAIL(Y-1~Y-5 · BLOCKER 0 · 둘은 총괄 패치 잔재 · `-v6.md`) → v7 → 6차 FAIL(Z-1·Z-2 · MED 2 · `-v7.md`) → v8 → 7차 FAIL(AA-1~AA-4 · 골든 manifest 수락면 · `-v8.md`) → v9(검증기 `validate_manifest.py`) → 8차 FAIL(AB-1·AB-2 · MED 2 · `-v9.md`) → v10(검증기가 모든 값 필드 · `importlib` 적재) → 9차 FAIL(AC-1~AC-5 · 문서 내부 정합 · `-v10.md`) → v11 → 10차 FAIL(AD-1~AD-3 · `-v11.md`) → v12(한 필드 음성 시험 표 T-V · `judged_at` 골격 · fail-fast 생성 블록) → 11차 FAIL(AE-1~AE-3 · `-v12.md`) → v13(제약 ID 단위 T-V · `git diff --quiet` · `PYTHON_BIN`) → 12차 FAIL(AF-1~AF-3 · `-v13.md`) → v14(층위 평가 · `set(위반 ID) == {target}` · clone 조립 · `judged_here` 우주) → 13차 FAIL(AG-1·AG-2 · `-v14.md`) → v15 → **14차 FAIL(AH-1~AH-4 · `-v15.md`) → v16 → 15차 FAIL(AI-1~AI-3 · `-v16.md`) → v17 → 16차 도전 중(09-03 01:07).** 지적은 전부 §2.8 검증기 절의 내부 정합으로 좁혀졌다 — BLOCKER 는 3차 이후 0. 지금 할 일 =
① 4차 도전 결과 회수 → PASS 면 **라운드 B-0**(골든 생성기 · sol-coder · 발주문 초안 있음) → 총괄이 `99fad78` 트리에서
골든 생성·커밋 → **라운드 B**(설계 PASS 판 첨부) → opus max 감사(A′·C′·B-0·B 합본) → 병합(관문 6→7) · FAIL 이면 지적
처분 → v6 → 5차. ② Owner **사후 확인** 3건(아래).**

- **감수 원문 4건이 새로 반입됐다** — `docs/lessons/2026-09-02-sol-challenge-t26-design-v2.md`(2차 FAIL · V) ·
  `2026-09-02-fable-advice-t26-design-v3.md`(자문 REVISE · N — ROUTING ⑽ ⓑ 「같은 상신 2회 저항」) ·
  `2026-09-02-sol-challenge-t26-design-v4.md`(3차 FAIL · W) · `-v5.md`(4차 FAIL · X) · `-v6.md`(5차 FAIL · Y) · `-v7.md`(6차 FAIL · Z) · `-v8.md`(7차 FAIL · AA) · `-v9.md`(8차 FAIL · AB) · `-v10.md`(9차 FAIL · AC) · `-v11.md`(10차 FAIL · AD) · `-v12.md`(11차 FAIL · AE) · `-v13.md`(12차 FAIL · AF) · `-v14.md`(13차 FAIL · AG) · `-v15.md`(14차 · AH) · `-v16.md`(15차 · AI) · `2026-09-02-sol-audit-round-c.md`(C 감사 FAIL · C).
  처분 = `DISPOSITIONS.md` §1(111행) · 사유 = `D-20260902-02` §7~§21 · `D-20260902-03` §6.
- **설계 메모는 리포에 없다**(PASS 판이 B 발주문 첨부로 들어온다). 세션 스크래치가 `/tmp` 라 **내구 사본**을
  `~/projects/workspaces/patent-docent-session-drafts/` 에 두었다 — `T26-DESIGN.md`(v1) ~ `-v5.md` · 도전 발주문 v2~v5 ·
  `order-round-b0-generator.md`(B-0 초안 · `<B0_BASE>` 와 §2.8 첨부만 채우면 발주 가능) · `AUDIT-ORDER-round-c.md` ·
  `order-round-c-prime.md` · 총괄 오라클 `generate_failure_grid.py` + `failure-grid-HEAD.json`(8,190칸 · HEAD 트리 계산).
- **값은 세 번 다 맞았다** — 8,190칸 (조치, 라벨)은 도전자가 매번 독립 재계산해 HEAD 와 불일치 0. 남는 것은 검증
  체계의 구멍(우회 변조 · 우회 호출자 · 다중집합)이었고 v5 가 승인 재시도 집합을 **엔진 상수 + 관문 상수**로 고정했다.
- **라운드 C′ = `867b95b`** — `check_dispositions.py` 격 어휘 · 표 행 arity · §0/§1 결속 · 자기 시험 6→10종.

**★ 사람이 판단할 것(Owner)** — 상신 1건 유지: `screening_memos[].read_run`(T32 §5 ②). **사후 확인**(재량 집행 · 다르게
보면 되돌린다) — ⓐ **C-1**: `sol-audit-halt-ordering` 4b 의 처분 `수용` 을 `852dcdd` 반입 시점에 총괄 발주문이 정하고
처분표가 처음 적었다(T27 ⒞ 등재 시점 기재의 이행이지만 값은 총괄 판단 · 실체는 T29 ⓐ 가 확정 — `D-20260902-03` §2 ⑸ ·
대안 = 「이연 → T29」로 재기재) ⓑ `S-1`·`S-2` id + `S-1` 처분(§3) ⓒ 라운드 C 재량 넷(§2 ⑴~⑷ — 감사가 넷 다 「적정」).

> [정정 2026-09-02 · 4차] 아래 09-02 3차 문단은 라운드 C 감사·설계 재도전 **전** 문안이다 — 「C 는 교차 감사가 아직 없다」·
> 「설계 v2 → 재도전」은 **낡았다**. 경위 보존용으로 남긴다.

**★ 09-02 3차 갱신 — Owner 재정 5건이 났고(T28~T32) 라운드 B 가 풀렸다. 지금 할 일은
① T26 설계 v2 → M1b 재도전(PASS 필요) ② 라운드 C 의 sol 감사(별건) 둘이고, 병렬로 돈다.**

- **재정 T28~T32 = 원장 등재 커밋 `b3144d5`**(`docs/decisions/ruling-20260902-02-T28-T32.md` ·
  Owner 육성 `★1 β / ★2 ⓐ / ★3 ⓐ / 4 ⓐ / 5 ⓐ`). 한 줄씩 — **T28** 수렴 출구 무재시도(β · P-4 존치 ·
  T26 §3 ② 에 예외 1칸) · **T29** 오늘의 표 = 출구 12검사 · `read.input-digest` 는 진입 예외 경로 ·
  **T30** `checks` 는 검사 실패 행에만 · 세 행은 `kind` · **T31** CP1 에 조기 합집합 블록(B 뒤 소라운드) ·
  **T32** `canonical_selection.read_run` 을 단일 `$defs` enum 에(B 또는 T31 에 동반).
- **라운드 A′ = `99fad78`**(감사 지적 8건 수리 · sol-coder) · **라운드 C = `852dcdd`**(T27 지적 처분 원장
  `DISPOSITIONS.md` + 관문 여섯째 `check_dispositions.py` · opus-coder) — 둘 다 병합됐다. 총괄 기록 =
  `D-20260902-01` §5 · `D-20260902-03-round-c.md`. **★ C 는 교차 감사가 아직 없다** → sol 감사(M9) 별건
  발주(D-03 §4 — B 감사와 벤더가 같아 합본하지 않는다).
- **라운드 B(T26)** — 착수 순서는 그대로다: 설계 v2(재정 값 반영 · 골든 기준 커밋 **`99fad78`** · 8,190칸)
  → **M1b 재도전**(sol xhigh · PASS 필요 · 조건부 PASS 없음) → sol-coder 저작 → opus max 감사(A′ 합본)
  → 병합. **T26 §3 ①(PASS 전 착수·커밋 금지)은 살아 있다.**

**★ 사람이 판단할 것(Owner)** — 새 상신 **1건**: `screening_memos[].read_run` 을 T32 와 같은 enum 에
묶을지(`ruling-20260902-02-T28-T32.md` §5 ② · 총괄 추천 ⓐ · `RULINGS-LEDGER.md` §3). **사후 확인**(재량으로
집행한 것 — 다르게 보면 되돌린다): 같은 원장 §5 ①(A-2 CP1 표지 문언) · §5 ③(`$comment` 어긋남 수정) ·
§5 ④(라운드 C 재량 넷 = `D-20260902-03` §2) · **`S-1`·`S-2` id 신설 + `S-1` 처분**(`D-20260902-03` §3).

> [정정 2026-09-02 · 3차] 아래 09-02 2차 문단은 재정 T28~T32 **전** 문안이다 — 「Owner 재정 대기」·
> 「라운드 C 진행 중」·「사람이 판단할 것 = §3 상신표」는 **낡았다**. 경위 보존용으로 남긴다.

**★ 09-02 2차 갱신 — 라운드 A 는 끝났고 감사·설계 도전이 둘 다 FAIL 을 냈다. 지금은
① Owner 재정 대기 ② 수리(A′)·라운드 C 집행이 병렬로 돈다.**

- **라운드 A(T22·T23·T24·T25) 집행 = 커밋 `aa9a734`.** opus max 감사 = **FAIL · 지적 8건**
  (`docs/lessons/2026-09-02-opus-audit-round-a.md`) — 실체는 착지했고 **발주문 귀책 2건**(A-1 반증
  시험 무판별력 · A-3 T25 「하나라도」 축소). 처분 = `D-20260902-01-round-a.md` §5 · 수리는
  **라운드 A′**(sol-coder) 로 집행.
- **T26 설계 도전(M1b · sol xhigh) = FAIL · 지적 7건**(`docs/lessons/2026-09-02-sol-challenge-t26-design.md`).
  **재정 T26 §3 ① 에 따라 라운드 B 착수 금지 상태.** BLOCKER 넷 중 **B-1(α/β · P-4 충돌)** 과
  B-2 뒷절반(`read.input-digest` 의 영역) 은 **Owner 재정 사항** → 상신 중(`D-20260902-02-t26-design-challenge.md` §3).
  나머지는 설계 v2 로 흡수한 뒤 **재도전(PASS 필요)** → sol-coder → opus max.
- **라운드 C(T27 지적 처분 원장) = 진행 중** — opus-coder(M4) · 별도 worktree(`round-c` 브랜치).
  B 와 무관하므로 먼저 들어온다.

**★ 사람이 판단할 것(Owner)** — `D-20260902-02-t26-design-challenge.md` **§3 상신표**(α/β 가 핵심 ·
총괄 추천 = β) 와 `D-20260902-01-round-a.md` **§4 ★**(CP1 에 조기 합집합을 그릴지) · **§5 사후 확인
2건**(A-2 렌더 범위 표지 · T27 소급 범위 독법). 재정이 나면 원장 등재(N6) → 설계 v2 확정 → 재도전.

> [정정 2026-09-02 · 라운드 A 종결] 아래 09-02 1차 문단은 라운드 A 집행 **전** 문안이다 —
> 「지금 할 일 = 라운드 A 집행」·「사람이 판단할 것은 지금 없다」는 **낡았다**. 경위 보존용으로 남긴다.

**★ 09-02 갱신 — Owner 결정은 끝났다. 지금은 집행 중이다.** 결정 2건은 재정 **T24·T25**
로 닫혔고, 함께 구조 재구성 **T26**(실패표)·**T27**(지적 처분 원장)이 채택되었다
(`docs/decisions/ruling-20260902-01-T24-T27.md` · Owner 육성 `추천사항 받아들일게. 제안대로 진행 부탁해.`).

**지금 할 일 = 라운드 A 집행** — `T23 + T22 + T24 + T25 최소판` 을 sol-coder 1배치로 저작하고
opus max 가 감사한다(§5 순서). 그 뒤 라운드 B(T26 · M1b 도전 선행) · 라운드 C(T27 · B 와 병렬).

**사람이 판단할 것은 지금 없다.** 라운드 A 의 스펙은 재정 파일 T22~T25 의 §3 집행 조건이
전부 든다. 감사 결과가 재정 사항을 열면 그때 상신한다.

**손대면 안 되는 것** — `_failure_verdict()` 의 `read.source-digest` 분기 **위치**는 T24 가
「그대로」로 못 박았다. T24 는 검사에 **넘기는 것**(디스크 재독본)을 바꾸지 분기를 바꾸지 않는다.

**아래 §1 은 상신 당시 문안이다** — 결정은 그 세 안 어느 것도 아닌 넷째 안(ⓓ 출구 재독)으로
났다. 경위는 재정 파일 T24 §1~§2 에 있으니 §1 을 다시 읽을 필요는 없다.

---

## 1. 결정할 것 — `read.source-digest` 실패의 처분

### 1.1 이 검사가 무엇을 하나

특허 원문 파일이 **런 도중에 바뀌지 않았는지** 확인하는 검사다.
재료 명세에 적힌 해시값과 실제 원문의 해시값을 맞춰 본다.

### 1.2 그런데 실제로는 이렇게 돈다

```
러너가 원문 파일을 한 번 읽어 메모리에 문자열로 든다      (read.py:1435)
        ↓
그 문자열을 해시한다                                       (read.py:1436)
        ↓
그 해시값을 재료 명세에 직접 써 넣는다                     (read.py:525)
        ↓
검사가 같은 메모리 문자열을 다시 해시해서                  (source_digest.py:29)
방금 써 넣은 값과 비교한다
```

**자기가 적은 것을 자기가 확인한다. 그래서 항상 일치한다.**
디스크의 파일이 도중에 바뀌어도 이 검사는 모른다 — 그 역할은 **런 진입 시점의 다른
검사**(`read.input-digest`)가 이미 맡고 있다.

**그럼 왜 있나.** `patent-historian` 때문이다. 그쪽은 재료 명세와 원문을 **밖에서 받아**
검증한다. 거기서는 둘이 진짜 독립이라 이 비교에 의미가 있다.
**이 파이프라인 안에서만 항진명제다.**

### 1.3 무슨 일이 있었나

계약(`contracts/stages/read.yaml`)에 *"이 검사가 실패하면 `halt`"* 라고 적혀 있는데
코드가 안 지키고 있었다. 총괄이 지키게 고치면서 근거를 이렇게 적었다 —
*"원천이 바뀐 런은 폐기 대상이다."*

**두 독립 감사가 이 자리를 반대로 판정했다.**

| 감사 | 판정 | 근거 |
|---|---|---|
| **opus max** | **옳다** | 계약이 `halt` 를 정했다. 게다가 같은 결함이 두 검사에 있었는데 둘 다 고쳤으니 **확대가 옳다** |
| **sol** | **틀렸다** | 근거가 거짓이다. 이 파이프라인에서 그 검사가 실패한다면 원천 변경이 아니라 **조립·검사 코드의 결함**이다. 그리고 코드 결함이 의심될 때 무엇을 할지는 **재정 T16 §6 ⑤ 가 이미 정했다** — 즉시 상신, 사유 라벨까지 붙여서. 순서를 바꾸면서 **그 진단을 지웠다** |

**둘 다 사실은 맞게 봤다.** 계약이 `halt` 라고 적힌 것도 사실이고, 그 검사가 여기서
항진명제인 것도 사실이다. **갈린 것은 「계약 행 자체가 옳은가」다.**

### 1.4 오늘의 실질 차이 — 거의 없다

`halt` 와 `escalate` 를 **구별해 처리하는 하류 코드가 아직 없다.**
READ 를 부르는 비시험 호출자가 리포에 하나도 없어서 둘 다 재료 명세 없이 끝난다.
**실제 차이는 기록에 남는 단어와 사유 라벨뿐이다.**

**그런데도 지금 정하는 이유** — 하류(`design`·`compose`·`gate` 모듈)가 서면 그때는
이미 굳어 있어 못 바꾼다. 지금이 제일 싸다.

**말 뜻**: `halt` = *이 런은 무효다*. `escalate` = *멈추고 사람에게 올린다*.
정의는 `docs/SPEC.md` 에 있고 **두 처분의 격은 다르다**(런 폐기 vs 판단 요청).

### 1.5 선택지 셋

#### ⓐ `halt` 유지 + 근거 문언 교체 + 진단 사유 라벨 신설 — **총괄 추천**

계약의 **처분**은 `halt` 로 두고, 계약에 적힌 **이유**를 바꾼다.
그리고 sol 이 「지워졌다」고 한 진단을 **사유 라벨**로 되살린다.

```
계약 문언
  구: "원천이 도중에 바뀐 런은 폐기 대상이다"
  신: "명세가 신고한 지문과 원천이 어긋난다.
       이 파이프라인에서는 조립·검사 코드 결함을 뜻한다.
       (원천 자체의 변경은 진입 검사 read.input-digest 가 잡는다)"
  + reason_label 신설 (진단을 기록에 남긴다)
```

- **장점** — 두 감사를 다 살린다. 처분은 opus max 가 맞고 근거는 sol 이 맞는데, 이 안은
  **처분을 유지하면서 근거만 교체**한다. 그리고 **틀린 근거 문언이 계약에서 사라진다** —
  이번 라운드가 벌한 결함 계열(선언이 사실과 다름)을 하나 더 남기지 않는다.
- **단점** — 코드는 안 바뀌고 문서·계약만 바뀐다. 「고쳤다」는 실감이 적다.
  그리고 **`halt` 가 옳다는 판단은 여전히 검증되지 않는다** — 하류가 없어서 잴 수가 없다.

#### ⓑ `escalate` 로 바꾼다

sol 의 논지를 끝까지 따른다. 코드 결함 의심이니 재정 T16 이 정한 대로 즉시 상신하고,
진단 라벨이 자연스럽게 따라붙는다.

- **장점** — **진단이 저절로 남는다.** 별도 라벨을 만들 필요가 없고, 재정 T16 §6 ⑤ 와
  일관된다. 「코드 결함 의심」이라는 사유 문언이 이미 있다.
- **단점** — **계약 행도 함께 고쳐야 한다.** 안 고치면 계약은 `halt` 인데 코드는 `escalate` 라
  선언과 실물이 또 어긋난다. 그리고 **`halt` 가 하나 줄어든다** — `patent-historian` 이식 때
  그쪽은 이 검사가 진짜 의미를 갖는 자리라 **`halt` 가 맞을 가능성이 높은데**, 그때 다시
  올려야 한다.

#### ⓒ 지금 정하지 않고 historian 이식 때 함께 본다

현행(`halt`)을 동결한 채로 둔다.

- **장점** — 이 검사의 **진짜 쓸모가 historian 쪽에 있으므로**, 두 프로젝트를 같이 놓고
  정하는 편이 판단 근거가 많다.
- **단점** — **틀린 근거 문언이 계약에 남아 있다.** 이번 라운드가 벌한 것이 정확히
  「선언이 사실과 다른데 아무도 안 잡는다」이고, 그것을 알면서 남기는 셈이 된다.
  그리고 이식이 언제인지 정해져 있지 않다.

### 1.6 결정을 어디에 적나

**원장이 먼저다**(재정 N6). `docs/decisions/` 에 새 재정 파일을 만들고,
`RULINGS-LEDGER.md` **§3 미결 절의 그 행을 지우지 말고** 재정 파일을 가리키는
포인터로 바꾼다(닫힌 것도 어떻게 닫혔는지를 남긴다).

**읽을 것** — `docs/decisions/RULINGS-LEDGER.md` §3(같은 내용의 압축본) ·
감수 원문 2건 `docs/lessons/2026-09-01-opus-audit-t17-repair.md`(§2 C-3 행) ·
`docs/lessons/2026-09-01-sol-audit-halt-ordering.md`(지적 1).

---

## 2. 결정되었으나 아직 집행 안 된 것 — 재정 T22·T23

> [정정 2026-09-02 · 커밋 `aa9a734`] **집행되었다.** 이 절의 제목과 첫 문장은 낡았다 — T22·T23 은
> 라운드 A 로 코드에 들어갔고 감사(§0)가 실체 착지를 확인했다. 아래는 상신·결정 당시 문안이다.

**원장에만 있고 코드에는 없다.** 발주만 내면 된다.
원문 = `docs/decisions/ruling-20260901-11-T22-T23.md`(집행 조건 포함).

### T22 — 레인 로그 검사 2종에 전용 실패 행을 신설한다

`read.lane-log-shape` 와 `read.lane-log-digest-value` 는 계약 실패표에 행이 없어서
**무관한 `read.verbatim` 행의 처분을 빌려 쓰고 있다.** 게다가 빌려온 「재시도 1회」가
**실제로는 0회**다 — 두 검사는 출구 재시도 루프가 끝난 뒤 합류한다.

**채택**: `action: escalate` · **`retry(n)` 없음** · `points` 없음.

> **★ 집행자가 반드시 지킬 것** — `retry(n)` 을 적지 마라. 적으면 오늘 0회인 재시도를
> 계약이 **다시 허구로 선언**하고, 그것이 이 재정이 고치는 바로 그 형태다.

### T23 — 미분류 목록에 `reported_by` 를 신설한다

목록이 두 실행(`read-a`·`read-b`) 신고의 합집합인데, 갈리면 두 행이 서고
**어느 실행 것인지 말하지 않는다.** 이 목록은 **CP1 표면**, 곧 Owner 승인 화면에 뜬다.

**채택**: `reported_by` 배열(`enum: [read-a, read-b]` · `minItems: 1` · `uniqueItems`).

> **★ 딸린 조건** — `engine/render/material_spec_md.py` 의 *"귀속을 말하지 못한다"* 고지를
> **지운다.** 귀속이 들어가면 그 문장이 **거짓**이 된다.
>
> [정정 2026-09-02] 지워졌다(`aa9a734` · T23 ④). ★ 다만 원장 T23 §1 의 「CP1 목록 = 두 실행 합집합」은
> **실물과 달랐다**(full 판정서는 정본 실행의 신고만 든다 · SPEC 정정 단락) — 그래서 CP1 의
> `reported_by` 는 오늘 항상 한 값이고, 감사 A-2 가 그 자리에 **범위 표지**를 요구했다.

**둘 다 소급하지 않는다** — `runs/` 의 기존 3런은 그대로 선다(행위시법 P-U1).

---

## 3. 판단 기준 — 이 리포에서 무엇을 혼자 정하고 무엇을 올리나

**판별선은 하나다: 그 판단이 검사의 판정 공간을 바꾸는가**(규율 11).

| 성질 | 누구 | 예 |
|---|---|---|
| **값 공간**(임계값·어형·정답 집합·스키마 키·계약 실패 행) | **Owner 재정** | T18·T21·T22·T23 전부 |
| 오류 수정 · 공학 집행 · 기록 · 시험 | **총괄 재량** | 낡은 계수 정정 · 계약대로 코드 고치기 |

**세 가지 함정**(헌장 ★ 절):
「가설」 태그는 면제가 아니다 · **되돌리기가 싸다는 것도 면제가 아니다** ·
반대로 **오류 수정을 재정 기다리며 미루면 기록이 틀린 채로 남는다**.

**이번 세션에 실제로 걸렸다** — 총괄이 재정 T17 을 집행하며 봉투 범위에서 `exact-match`
축까지 뺐다. Owner 가 채택한 문언은 청구항 실패만 배제했는데, 총괄이 **자기가 쓴 더 좁은
원안**을 근거로 삼았고 **두 번째 축소임을 알면서도** 상신하지 않았다.
재정 T19 가 **효력은 추인하되 위반은 원장에 남겼다.**
> **효력은 사후에 줄 수 있으나 절차는 사후에 만들 수 없다.**

### 작업 가이드 — 이 일에는 이것을 연다

| 하려는 일 | 열 것 |
|---|---|
| 재정을 내리거나 찾는다 | `docs/decisions/RULINGS-LEDGER.md`(§2 색인 · §3 미결) → `ruling-*.md` |
| 감수 결과를 본다 | `docs/lessons/` **전문 보존**. 요약본을 만들지 마라 |
| 무엇이 실물이고 무엇이 예정인지 | `docs/SPEC.md` §6.7 · `contracts/glossary.md` §2.2 |
| 좌석(모델·effort)을 정한다 | `~/.claude/agents/ROUTING.md` — **여기서 정하지 않는다** |
| 레인이 죽거나 산출이 빈다 | `~/.claude/agents/LANE-RUNTIME.md` |
| 커밋 전 | 관문 **7종** plain·`-O` 전부 exit 0 (`CLAUDE.md` §6) — **[정정 2026-09-02 · 재정 T27]** 구 문언 「5종」. 여섯째 = `check_dispositions.py`(`852dcdd`). **[정정 2026-09-03 · 재정 T26]** 실패표 관문이 더해져 6→7 |
| 감수 원문을 반입한다 | `docs/lessons/` 전문 + **총괄 머리말에 `지적 열거 = …`** + `DISPOSITIONS.md` §0 행·§1 처분 행 — 관문 여섯째가 양방향 차집합을 잰다. **열거가 원문을 빠짐없이 담았는가는 사람 몫**(원장 T27 ⒜ ①) |
| 레인을 발주한다 | 발주문 골격 **⑹~⑼**(`D-20260902-02` §5) — 특히 ⑼ 역프로브·되돌림은 격리 사본에서만 |

**관문 목록은 손으로 열거하지 말고 `ls tools/check_*.py` 로 뽑아라.**
이번 세션에 다섯째가 새로 섰고, 문서에 「네 종」이라 적힌 자리가 두 판 연속 낡았던 전례가 있다.
**그리고 바로 위 칸이 세 번째 사례가 됐다** — 여섯째(`852dcdd`)가 선 뒤에도 「5종」으로 남아 있었다.
**[정정 2026-09-03 · 재정 T26]** `check_failure_table.py`가 일곱째로 섰다. 실패표(`contracts/stages/read.yaml#failure`)를 고치면 이 관문도 발화하며, 일곱 도구는 각자 하나의 주장만 증명한다.

---

## 4-2. 09-02 세션이 한 일 (커밋 `f46698e` → `867b95b`)

```
867b95b  라운드 C′ — C 감사 지적 C-2·C-3·C-4·C-6 수리 (sol-coder)
feaba3b  원장: 설계 v4 M1b 3차 도전 원문(FAIL W-1~W-4) + 처분 4행
4e1f05c  원장: 감수 원문 3건(v2 도전 FAIL · 자문 REVISE · C 감사 FAIL) + 처분 21행 + C-1/C-6 마커
663c77e  시험: 섀도 원장 시험 — 링크된 worktree 에서 주 트리 기대
005355a  기록: C 병합 뒤 총괄 후속 — D-03 · S-1/S-2 · 관문 6종 정정 · 인계 3차
b3144d5  원장: 재정 T28~T32 등재 + 색인
852dcdd  라운드 C — T27 집행 (opus-coder)
99fad78  라운드 A′ — A 감사 지적 8건 수리 (sol-coder)
f46698e  원장: A 감사·T26 도전 원문 + 처분 문서 2건
```

**이 세션의 형태 — 같은 설계가 세 번 FAIL 을 받았고 세 번 다 옳았다.** 값은 매번 맞았고 지적은 7 → 8 → 4 로 좁아졌다.
ROUTING ⑽ ⓑ 자문을 2차 뒤 한 번 거쳤고 자문이 「그대로 내도 된다」고 한 v4 를 3차 도전이 다시 떨어뜨렸다 — 자문과 도전자는
다른 것을 보았고 둘 다 필요했다. 재정 사항은 1차 도전이 연 셋(T28~T30) 뒤로 새로 생기지 않았다.

## 4. 이전 세션이 한 일 (커밋 5개 · `ad6d379` → `6544871`)

```
6544871  원장: 재정 T22·T23 + 원장 §3 미결 절 신설
c3fe549  집행: 재정 T18·T21·T19·T20 + 교차 감사 잔여 처분
7f1e763  원장: 재정 T21 — 자리표시를 고정 토큰으로
e145366  원장: 재정 T18~T20 + 교차 감사 원문 2건 보존
39286ca  수리: G-6 감사 지적 13건 처분 + 재정 T17 집행
```

**전수 548 통과**(plain · `PYTHONOPTIMIZE` 양쪽) · **관문 5종 × 2모드 전건 exit 0**.

### 이 세션의 형태 — 감사가 두 번 FAIL 을 냈고 두 번 다 옳았다

**1차**(커밋 `39286ca` 대상) — 13건 중 11건이 실제로 닫혔으나 **수리가 새 BLOCKER 를
열었다.** X-2·X-3 의 수리가 **가림막을 걷어내자** 밑에 있던 빈 문언 결함이 드러났고,
직전 커밋에서 완주하던 입력이 죽기 시작했다. 재정 T18·T21 이 그것을 처분했다.

**2차**(sol · 총괄이 직접 저작한 슬라이스) — 총괄이 「계약대로 고쳤다」고 한 자리의
**근거가 틀렸음**을 잡았다. 그것이 지금 §1 의 미결이다.

**배운 것 셋**

1. **선언과 실물이 어긋난 자리가 이 리포의 지배적 결함 계열이다.** 이번에만
   A-2·A-3·Y-3·T21·T22 가 전부 같은 형태였다 — 계약·문서가 무언가를 선언하는데
   **기계가 그것을 대조하지 않는다.** 새 선언을 쓸 때마다 *"이걸 누가 대조하나"* 를 물어라.
2. **「시험이 생겼다」는 닫힘의 증거가 아니다.** 495개가 전건 통과하는 아래에 런을
   중단시키는 블로커 둘이 있었다. **구현을 뒤집었을 때 시험이 실패하는지**를 봐야 한다.
3. **하위 에이전트의 자기 보고를 그대로 옮기지 마라.** 감독이 커밋본을 다시 읽으며
   **자기가 넣은 것을 총괄이 넣은 것으로 오귀속**하고 거기서 없는 실패 서사를 도출한 일이
   있었다. 총괄도 감독 보고를 확인 없이 옮겨 **「역반증 통과」라는 거짓 보고**를 Owner 에게
   했다(재정 T19 §3 에 등재). **전사가 아니라 실측으로.**

---

## 5. 다음 작업 — 결정 이후의 순서

```
[끝] 결정 → 재정 T24~T27 (09-02)
   ↓
[끝] 라운드 A : T23 + T22 + T24(출구 재독) + T25(halt 즉시 탈출 · 최소판)  = aa9a734
       sol-coder 1배치 → opus max 감사 FAIL(8건 · 실체 착지 · 발주문 귀책 2) → 원문 보존
   ↓
[끝] 라운드 A′ : 감사 지적 수리(A-1·A-3·A-4·A-5·A-6 + A-2 범위 표지 + A-7 결속 시험)  = 99fad78
       sol-coder → 총괄 재현 → 커밋 → 감사는 라운드 B 감사에 합본(같은 출구 판정 구역)
[끝] 라운드 C : T27 지적 처분 원장·관문 — M4 opus-coder · worktree `round-c`  = 852dcdd
       → [끝] sol 감사(M9) 별건 · 격리 사본(852dcdd 클론 + 마커 · workspace-write) = FAIL 6건 → 원문 4e1f05c
       → [끝] 라운드 C′ : C-2·C-3·C-4·C-6 수리 — sol-coder · worktree `round-c-prime`  = 867b95b (감사는 B 감사에 합본)
[끝] Owner 재정 T28~T32 (09-02)  = b3144d5 원장 등재 · 병합 뒤 총괄 후속 = 005355a · 663c77e
   ↓
[지금] 라운드 B : T26 — 설계 v2 → M1b 2차 FAIL(V) → v3 → 자문 REVISE(N) → v4 → M1b 3차 FAIL(W) → v5 → M1b 4차 FAIL(X) → v6 → M1b 5차 FAIL(Y) → v7 → M1b 6차 FAIL(Z) → v8 → M1b 7차 FAIL(AA) → v9 → M1b 8차 FAIL(AB) → v10 → M1b 9차 FAIL(AC) → v11 → M1b 10차 FAIL(AD) → v12 → M1b 11차 FAIL(AE) → v13 → M1b 12차 FAIL(AF) → v14 → M1b 13차 FAIL(AG) → v15 → 14차 FAIL(AH) → v16 → 15차 FAIL(AI) → **v17 → M1b 16차 도전 중**
       PASS → [B-0] 골든 생성기(sol-coder · 초안 order-round-b0-generator.md) → 총괄 99fad78 트리 생성 · 골든 커밋
       → [B] sol-coder(설계 PASS 판 첨부 · 골든 무접촉) → opus max 감사(A′·C′·B-0·B 합본) → 병합 (PD-M2a 첫 항목 · 관문 6→7)
[뒤] T31 소라운드 : CP1 조기 합집합 블록(engine/render/material_spec_md.py · SPEC §1.5) — B 뒤
[뒤] T32 : canonical_selection.read_run enum 결속(B 또는 T31 에 동반 · screening_memos 는 재정 뒤)
   ↓
PD-M2a 러너 무결성 : 백로그 B-1(로그 검사 시점 이동) → G-5(멱등 가드)
   ↓
PD-M2b : G-1·G-2·G-3(좌석) → B-2(lane_id 값 공간) → G-4
   ↓
PD-M2c : G-9 ∥ G-7 → G-8 · G-11 계통 소탕
   ↓
PD-M3 → PD-M5 → PD-M9 → PD-M4 → 예행 런
```

**묶을지 나눌지** — 묶는 것으로 결정되었다(재정 파일 §5 ④). **한 배치에 다 넣지 않는 이유**
= 직전 라운드의 수리가 새 BLOCKER 를 열었다 — 감사가 한눈에 볼 수 있는 크기로 자른다.

**예행 런은 아직 멀다** — 종료선이 strip 산출이라 `design`·`figures`·`compose`·`gate`
넷을 지나야 하고 **그 넷은 디렉터리조차 없다**. 「다음은 예행 런」이라 적힌 낡은 문장을
만나면 그것은 틀린 것이다(`CLAUDE.md` §6 에 정정 마커가 있다).

### 아직 안 닫힌 것 (기록만 · 지금 할 일 아님)

- **`phase-gate.json` 에 스키마가 없다** — 형태 결속이 시험 한 겹뿐이다.
- **`check_spec_refs.py` 가 `tools/` 등재 항목의 실재를 대조하지 않는다** — 문서가 **없는
  도구를 관문으로 선언해도 안 잡힌다.** 지금은 다 실재하므로 무해하다.
- **`text_status` 이름이 겹친다** — 새 스키마 필드(`verbatim`/`absent`)와 원장 머리말의
  `text_status`(`원문`/`재구성본`/`혼합`). 파일도 검사도 달라 충돌은 없으나 검색에서 헷갈린다.
- **커밋 메시지의 시험 계수 오기 1건** — 커밋 메시지라 고칠 수 없다. 이후 메시지에는
  계수를 적지 않는다. **★ `aa9a734` 에서 한 번 더 어겼다**(계수 `548 → 561` 을 적었다 —
  `D-20260902-01` §6-2 자기 계상). 그 뒤 커밋은 지킨다.
- **`patent-historian` 체크아웃이 없다** — CLAUDE.md §2 의 리더 상호 체크를 두 라운드 연속
  **수행하지 못했다**(감사 [미검증] 1). `reader/lib/run_checks.py` 의 새 하드 실패 모드가 이식
  상대에게 어떤 뜻인지 아무도 판정하지 않았다.
- 감사 자신의 `[미검증]` 목록 — 두 감수 원문의 마지막 절에 있다.
