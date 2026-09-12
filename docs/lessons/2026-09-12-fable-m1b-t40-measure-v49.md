# 독립 감수 원문 — M1b 설계 도전 45차(claude-fable-5-1 max · 재정 T54 종결선 판) · T40 ④ A 비교 실측 설계 메모 v49(19차 저작 `b7f8e47` · §5′.20 U5 증거 형식) · 판정 REVISE(MED 2 · LOW 1 · 기록 1) · **새 종류의 규칙 요구: 없음(10연속)** · **`U_r`=6 `B_r`=16 `L_r`=0** · **원본 승인: 아니오** · **「이 형식으로는 닫히지 않는다」 판명: 불성립(상신 사유)** · 지적 OQ-1 ~ OQ-4

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-12 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `753c5d9c8c75392159fe2fd579dc7729087034d5d07284b4358858014cff72b3` · 22,181 B). 레인 = `~/projects/workspaces/pd-lanes/fable-m1b-t40v49/` · 발주문 `BRIEF-m1b-t40-v49.md`(20,320 B · 위험 어휘 `sandbox 2` 뿐 · 약정 ⒁ M1b 블록 심사 3/3).

**좌석 = `좌석 M1b` · `claude-fable-5-1` max**(ROUTING v3 본좌석 · 약정 3/3) · START 23:30:06 · 종료 23:56:36 · **26분 30초** · EXIT 0 · `num_turns` 38 · USAGE `cache_creation=246,834 cache_read=1,045,286 output=68,221(thinking 41,222)` · `$8.62` · 세션 `d4e0a6a1-6a4f-4cdd-86e3-45df3b7241ab` · 남긴 파일 0 · 배경 작업 0 · 사본 `pd-m1b-t40-v49`(detached `b7f8e47d82fe9f6e6e9fa9c0aa7f47ebb83dff9e` · `git status` = `?? .audit-sandbox gate/ src/` 그대로). 첫 기동(21:26)은 Owner 지시로 23초 만에 중단했고(산출 0 · 추기 104) 이것은 23:30 재기동분이다.

**판정 = REVISE · 지적 4(MED 2 · LOW 1 · 기록 1) · 기각 0 · 발주자·저작 귀책.** `Satisfied=11 Violated=1 Unexamined=0` · 심사 ①②③⑤ 성립 · **④ 불성립** · 대장 누락 반례 0.

**★ 필수 줄 아홉이 전부 섰다.** ① `VERDICT: REVISE` ② ⑽ ⓑ 발동(컴포넌트 D · 같은 부류 10회 연속) ③ 새 규칙 요구 없음(「이 형식이 이미 받는 꼴의 규칙 셋과 CONNECT-I 전제 하나의 추가」) ④ `U_r`=6 `B_r`=16 `L_r`=0 ⑤ 비감소 — `U_r` **다섯 판 연속 6** · `L_r` 공허한 0 두 판째 ⑥ **원본 승인: 아니오**【직접 · `verify_baseline` 호출 issued False · derived 988/992 · `build(원본,원본)` approved False blockers ['U5']】 ⑦ **「이 형식으로는 닫히지 않는다」 판명: 불성립** — 「열린 전제 셋은 이 형식으로 원리상 못 쓰는 것이 아니라 **쓸 수 있었던 규칙을 안 쓴 것**이다 … 커널은 세 규칙 이름을 `OPEN_PREMISES` 로 하드코딩해 거부할 뿐 형식이 막지 않는다」 → 상신 사유 ⑧ 7회차 성공 조건 ⒜⒝ 미충족 · 실패 신호 ⒜(합성 프로브 3 국소 발급) ⒝ ⒞ 켜짐 ⑨ 저작자 재정 요청 ① 상신 사유 · ② 기각 · ③ 기각 · ④ 상신 사유.

**★ 판정의 중심 셋.** ⑴ **판명 불성립** — `parsing-site-coverage`(I-C)·`consumption-site-coverage`(I-P)는 「AST 자리 전수 열거 + 제외 목록 + 자리별 §5′ 문장」으로 지금 형식 그대로 쓸 수 있고, `semantic-equivalence`(I-S)는 부조건은 `P-SHAPE` 동결로 족하되 정당화가 두 프로필 계산 전체의 동치 증명이어야 해서 **차원이 다르다**(「아무도 쓰지 않았고 참인지도 [미검증]」). ⑵ **좁히기 실험【직접】** — 커널 `OPEN_PREMISES` 를 비우고 `open:*` 단계를 뺀 유도로 `verify_baseline` → `issued True` → `build(원본)` → **`U5 solved · approved True`**. 즉 재정 요청 ④(U5 의무를 「바깥 결과 정리」로 좁힘)대로면 원본은 실제로 승인된다. **그때 함께 승인되는 상태** = I-S/I-C/I-P 의미 전제 셋 미증명 · 포장 완료가 사실로만 기록 · `:310` 류 thunk 안 창 미관측 · **OQ-2 의 helper 후보 셋이 전체 승인에 이른다(L≥3)**. ⑶ **재정 요청 ①【직접 코드】** — `t40_resources.entry:437-440`·`t40_receipts.io_boundary:162-173` 은 `F.remember(exc)` 뒤 `raise failure(exc) from exc` → **business = 포장 · failures = [raw, raw, 포장] · 호출자 = 포장**. 18차 `preservation()` 자신이 셋 다 raw 일 때만 비위반으로 판정하므로 검사기 기준으로는 위반이고, T53 ⑴ 「업무 결과**나** 실패 목록에서 사라지면」의 자연 독해도 「어느 한쪽」이다. IO 오류는 §5′.18 이 Γ 안으로 명시한 부류. **「어느 한쪽」으로 재정되면 원본이 `R.entry` 2 + `io_boundary` 경유 자리에서 I-R 위반 → PO-RESULT-01 Violated → T53 이 예고한 「다음 반례」(원본 수리 재저울)가 된다.**

**★ 지적 넷.** **OQ-1 MED** — `CONNECT-I` 의 전제 집합에 「경계 thunk 안 최초 오류 보존」이 없고 ⑷ 이 시야 밖으로 뺐으며 `R.entry`·`driver_boundary` 보존표는 기록이지 증명이 아니다 → root 가 전제보다 강한 결론(문안: 전제 ⒠ 추가 또는 root 를 「바깥 결과 정리」로 낮추고 다른 이름). **OQ-2 MED** — H-bind 부조건 구멍: `super()`·`locals()`·`eval('a')` 를 본문에 둔 helper 프로브 셋이 국소 증서를 받았고 실행은 다르다(RuntimeError · 빈 dict) — 프레임 의존 내장을 놓쳤다(문안: H2 에 프레임 의존 이름 Load 금지). **OQ-3 LOW** — §5′.20 ⑶ 의 정당화 문장이 부조건 범위보다 넓다(P-DEFERRED 는 Attribute thunk 를 지연으로 봄 · `:310`·`:313`·`:328` 은 step 진입 전 평가). **OQ-4 기록** — 세 규칙은 커널 `OPEN_PREMISES:129,293-296` 이 이름으로 거부 · 처분은 T55.

**★ 재정 요청 4 의 게이트 소견.** ① 상신 사유(위) · ② 기각(`driver_boundary` 는 프로세스 경계 · 객체 동일성 물리적 불가 · 41~44차 Satisfied 근거 유지) · ③ 기각(「11형태 국소 미발급」 문언은 어느 재정문에도 없다 · 환경 4 국소 발급은 T52 ⑶ 을 어기지 않는다 · 단 H-bind 구멍은 OQ-2) · ④ 상신 사유(좁히기의 사실 = 위 ⑵).

**★ 직접 확인 범위.** 지문 전건 · guards 4 실행 · `verify_baseline` 직접 호출 · U5 세 경로 · 좁히기 실험 · H-bind 프로브 3 · 하네스 세 파일 diff · 회귀 표본 5 묶음 36건(`--src` 사본 · 19차 로그와 PASS/FAIL 전건 동일) · 검사기 재동결 차이가 검사기 파일 6 에만 있음. 물려받음 = 회귀 171 · 불변 37 · 거짓 유도 14 개별 · L 7 · 옛 대상 계열.

**★ 진전 판정(T50 ③)** — 43·44·45차 세 판 연속 비감소 · `U_r` 다섯 판 연속 6. **재정 T54 종결선 발동** — 「원본 승인: 아니오」 → 46차 저작 없이 **T55**. 다만 게이트가 「판명 불성립」을 상신 사유로 명기했으므로 T55 는 종결선의 전제(「아니오 = 닫히지 않는다 실측」)가 서지 않았다는 사실 위에서 선택지를 다시 연다.

**★ 좌석 약정 ⒁ 관측(M1b fable max · 심사 3/3 · 완료).** 26분 30초(ⓑ 40분 미만) · 기각 0(ⓒ) · 같은 컴포넌트 연속 REVISE 는 이 좌석 판으로 2(v3 심사 r1 PASS · 44차 REVISE · 45차 REVISE → ⓐ 「3회 연속」 미해당 · 프로젝트 루프로는 10회) · `num_turns` 38 · 자기 보고 「턴 약 13 · 도구 호출 약 32」 · 출력 68,221(사고 41,222) · $8.62. 세 판 합 = 132턴 · 57분 · $26.13 · 기각 0/0/0. **조절 상신 해당 없음 · 좌석 확정 재정은 Owner(약정 문안 · v3 7일 재검 09-19).**

**발주자 오류 247** — 45차 발주문에 자문 7회차 원문·결정문 추기 82·19차 발주문을 동봉하지 않아 게이트가 셋을 [미확인]으로 뒀다(판정 영향 = 「11형태 비승인」 문언의 출처를 게이트가 확인할 수 없어 재정 요청 ③ 을 재정문 grep 으로만 기각). 누계 247.

**처분 = OQ-1·OQ-2·OQ-3 수용(공학 · 이행 = T55 재정 뒤) · OQ-4 이연(상신 사유 → T55 안건).** `DISPOSITIONS` 등재 **107/12/119**.

지적 열거 = OQ-1, OQ-2, OQ-3, OQ-4

---

# 도전 원문 (claude-fable-5-1 max · 이 아래는 도전자 저작)

# 45차 판정문 — T40 ④ 설계 메모 v49 (`e484bf937fd69a25` · 267,196 B) · 좌석 M1b fable max · 재정 T54 종결선 판

VERDICT: REVISE
⑽ ⓑ 자문 트리거: 발동(컴포넌트 D · `PO-GATE-01` 승인 근거 부류 · 같은 부류 10회 연속 REVISE · 다만 T54 ① A 종결선이 46차를 두지 않으므로 처분은 T55)
새 종류의 규칙 요구: 없음 — 필요한 것은 이 형식이 이미 받는 꼴(AST 부조건 + §5′ 산문 정당화)의 규칙 셋과 `CONNECT-I` 전제 하나의 추가이지 새 보증이 아니다.
`U_r`=6 `B_r`=16 `L_r`=0
비감소: 41차 6/0/2 · 42차 6/0/1 · 43차 6/0/7 · 44차 6/16/0 · **45차 6/16/0** — `U_r` 은 **다섯 판 연속 6**(41~45차) · `B_r` 16 그대로 · `L_r` 0 은 승인 경로가 원본에도 닫혀 있어 생긴 **공허한 0** 이 두 판째다.
★ 원본 승인: **아니오** — 【직접】 `verify_baseline(원본 9모듈, R19-U5-DERIVATION.json)` 을 직접 호출해 `issued False · derived 988/992 · failed 4(open:×3, root) · errors 8` 을 얻었고 `t40_admission.build(원본,원본)` 이 `approved False · blockers ['U5']` 를 냈다(재생성 유도는 첨부와 바이트 동일).
★ 『이 형식으로는 닫히지 않는다』 판명: **불성립** — 열린 전제 셋은 이 형식으로 원리상 못 쓰는 것이 아니라 **쓸 수 있었던 규칙을 안 쓴 것**이다: 부조건은 보통의 AST 열거·형태 동결(`P-PARSE-SITES`·`P-CONSUMER-SITES`·`P-SHAPE-select_profile/_metrics_program/_halt4_bound`)로 적히고, 정당화는 이 형식이 `outer-result-boundary-lemma` 에서 이미 쓰는 §5′ 산문이다. 커널은 세 규칙 이름을 `OPEN_PREMISES` 로 **하드코딩해 거부**할 뿐 형식이 막지 않는다(근거 §1 ②⒝). T54 ① A 에 따라 아니오는 실측으로 간주되어 T55 로 가되, 이 불성립은 상신 사유로 명기한다.
자문 7회차 성공 조건: ⒜ 미충족(잘못된 전체 승인 0 은 서고 · B-select 2·C-select 2 의 국소 긍정 증명은 섰으나 H-bind 는 생산 자리 0 이고 부조건에 구멍 · OQ-2) · ⒝ 미충족(폐쇄 0/6) · 실패 신호: **⒜ 켜짐**(근거가 서지 않는 국소 증서 발급 — 합성 프로브 3 【직접】 · 최종 승인 도달 0) · **⒝ 켜짐**(`U`=6 재발) · **⒞ 상태로 켜짐**(원본·필수 16 전부 거부 상태 유지). 7회차 원문은 동봉되지 않아 [미확인]이며 44차 판정문의 조건 기술로 판정했다.
저작자 재정 요청 ①②③④: ① **상신 사유** · ② **기각** · ③ **기각** · ④ **상신 사유**(사실은 §1 ⑤).

**증거 강도.** 【직접】= 이 판이 읽고 실행해 확인 · 【물려받음】= 19차 산출·로그 · 【주장】= 저작자 문장. 저작자의 `NOT_READY`·「원본 승인: 아니오」는 근거로 쓰지 않았다.

## 1. 물음 다섯의 답

**물음 ① — 형식이 발주 요구를 충족하는가.** 【직접】 §5′.20 은 13,889 B `1364351646c69219` 이고 다섯 요구 중 넷이 선다: 유한·비순환(⑴ 앞 단계만 참조 · 커널 `UNRESOLVED_FORWARD_OR_CYCLIC_PREMISE` · 상한 8192) · 실제 바이트·AST 결부(`subject` = 9모듈 manifest + 전제 절 sha · 부조건은 `PC.trees(reference)` 에서 재계산) · 부조건 14 가 기계 술어이고 시야(`sees/does_not_see`)가 결과에 적힘 · 합성 단계 `CONNECT-I` 존재. `R19-PRECONDITIONS.md` 의 술어 14 는 `t40_baseline_preconditions.py` 의 함수·행 번호 14/14 일치(shape:302 · slot_stores:322 · no_dict_write:353 · active:366 · names_fixed:376 · no_own_slot:416 · module:432 · deferred:458 · owner_stages:492 · io_clear:509 · b_select:540 · c_select:552 · h_bind:563 · resources_entry:639) · 표본 셋(P-SLOT-STORES · P-DEFERRED · P-RENTRY)의 「보는 것/보지 않는 것」 문자열이 코드와 동일. **⑶ 은 부분 성립**: `side-condition`·boundary·driver·machine·io-clear·B/C-select 행은 파이썬 의미로 정당화됐다. 그러나 (a) `entry-outer-result` 행의 `R.entry`(2)·`driver_boundary`(7) 종류는 보존표에 「포장 / SystemExit 투영」을 **사실로 기록**할 뿐 보존을 정당화하지 않고(형식 스스로 「어느 쪽이 위반인지 정하지 않는다」고 적었다) (b) `owner-finalize-diagnostic` 의 「소유자의 모든 업무 호출은 capture 안에서 지연 실행」은 P-DEFERRED 가 보는 범위(capture/step/tail 인자가 Call 이 아닌가)를 넘는다 — `write_closed` 에서 P-DEFERRED 는 참이되 :310·:313·:328 의 thunk 는 `Attribute` 로 **step 진입 전에 평가**된다(【직접】 술어 실행 · T53 ⑵ 창 그대로) (c) `machine-lemma` 의 「stopped 는 되돌려지지 않는다」는 P-SHAPE-Machine 만으로는 안 서고 다른 모듈의 store 부재가 필요하다(grep 으로 0 【직접】 · 술어는 없음). 규칙 이름·동결 지문으로 정당화를 대체한 자리는 없으나 위 셋은 정당화 문장이 부조건보다 넓다(OQ-3).

**물음 ② — 「원본 승인: 아니오」와 판명의 진위.** ⒜ 【직접】 988 단계가 실제로 증명하는 것: 부조건 484 는 각각 원본 AST 의 사실(P-NO-OWN-SLOT 438 = 그 호출체 안에 execute/_ACTIVE/Execution 호출·슬롯 store 없음 · P-MODULE 10 · P-DEFERRED/OWNER-STAGES 10·10 · 전역 술어 6). boundary lemma 는 동결 형태 8 + 전역 4 에서 파이썬 예외 전파 의미로 따라 나오며 진정한 정리다 — **단 그 결론은 「thunk 가 전파시키는 완료가 그대로 슬롯·호출자에 간다」이지 「thunk 안에서 최초 오류가 살아남는다」가 아니다**. 진입 489 중 `none` 438 의 보존표 「감싼 경계에서 상속」은 P-NO-OWN-SLOT + 전파 의미로 성립 · `F.entry` 20 은 lemma 대로 성립 · `boundary-definition` 12 는 정의상 공허(형태 동결로 족함) · `R.entry` 2·`driver_boundary` 7 은 **기록이지 증명이 아님**(위 ①). 소유자 10 은 진입·P-DEFERRED·P-OWNER-STAGES·machine lemma 의 합집합일 뿐 새 정리를 더하지 않는다. 결정적 관찰: `CONNECT-I` 는 (a)(b)(c)(d) 를 전제로 root `connected-I`(I-A·I-C·I-S + I-R·I-F·I-P) 를 결론하는데 **경계 thunk 안 최초 오류 보존(제어 흐름 handler · 창 안 직접 평가 · `io_boundary`/`R.entry` 포장)은 전제에 없고 ⑷ 이 명시적으로 시야 밖으로 뺐다**. 즉 열린 전제 셋이 있었더라도 root 는 전제보다 강한 결론이다(OQ-1). ⒝ 전제별 한 줄: `parsing-site-coverage`(I-C) — **안 쓴 것**: 역직렬화 원시 호출 자리를 9모듈에서 전수 열거하고 `parse_after_io` thunk 안인지·제외 목록인지를 AST 로 검사하며 제외 자리마다 §5′ 문장을 두는 규칙은 지금 형식 그대로다(의미 분류는 제외 목록의 정당화로 옮겨진다). `consumption-site-coverage`(I-P) — **안 쓴 것**: artifact 읽기 자리 전수 + `require_attempt_ready → manifest_verify` 선행의 어휘 검사 + 자리별 정당화. `semantic-equivalence`(I-S) — **안 쓴 것이되 차원이 다르다**: 부조건은 `P-SHAPE` 동결로 족하나 정당화는 두 프로필 계산 전체의 동치 증명이어야 하고 그 참은 유한 증인(R10·S73/S74·207)으로만 시사된다 — 형식이 막는 것이 아니라 아무도 쓰지 않았고 참인지도 [미검증]이다. 저작자의 「AST 형태가 아니라 계산의 정리」 구분은 boundary lemma 자신에게도 걸리므로 원리 구분이 못 된다. ⒞ 【직접】 `U5` 노드 세 경로: 첨부 유도 → `unresolved · '§5′.20 derivation not issued: UNJUSTIFIED_SEMANTIC_RULE:…'` · 유도 없음(`_ATTACHED` 비움) → `unresolved · 'no U5 derivation submitted (§5′.20 form)…'` · 다른 대상(`t40_excerpts.py` 한 줄 추가) → `unresolved · 'TARGET_CONTEXT_OR_ASSUMPTIONS_MISMATCH'`. 상수가 아니다(`t40_admission.py:45-59,67,70`).

**물음 ③ — 재작성 4 발급.** 【직접 재실행】 io-False-or(`consume.py:227` B-select) · stopped-False-or(`flow.py:107` B-select · 자리 0 은 메서드 위치 차이로 미허가이나 합동 검사가 전체 AST 동일을 확인) · close-live-if(`receipts.py:319` C-select) · finalize-live-if(`receipts.py:191` C-select) = 국소 ISSUED · 경로 verified-full-context · **최종 DENIED · 차단 `U5` 하나**. B-select(`or` 좌→우 평가·마지막 값 전달·`bool(False)` 내장) · C-select(상수 test·스코프 없음·orelse 공집합) 는 건전하고 `CALLER-COMPOSITION` 의 「허가 재작성 적용 후 원본 AST 와 위치 제외 동일」이 합동을 보증한다. S48 미발급(H5 · 호출이 If 밖) ✔. 11형태 【직접 재실행】: 프로그램 유래 7 국소 NOT_ISSUED(H4 `import-normal-bind`/`handler-entry-bind,handler-exit-delete` · 후평가 truth 는 B-select 첫 피연산자) · 환경 모의 4 국소 ISSUED·최종 DENIED · **최종 승인 0 → L 0**. 환경 4 의 국소 발급은 T52 의 귀결이 맞다(추가 프레임·분기 opcode 실패는 해석기 유래 · 관계의 시야 ⑷ 밖). **그러나 H-bind 부조건에는 구멍이 있다** 【직접】: `super()`·`locals()`·`eval('a')` 를 본문에 둔 helper 세 프로브가 모두 국소 증서를 받았고(H-bind holds True), 실행하면 인라인은 `B.m`/`{'a':7}` 인데 helper 는 `RuntimeError: super(): no arguments`/`{}` 이다 — 프로그램 유래 완료 차이다. ⑸ 정당화 「전역/내장은 같은 조회라 같은 객체를 본다」는 프레임 의존 내장을 놓쳤다. 지금은 `U5` 가 최종을 막아 L 이 아니지만 **④ 로 U5 를 좁히면 이 셋은 전체 승인에 이른다**(OQ-2).

**물음 ④ — 하네스 수리·이중 계상.** 【직접 diff】 `t40_regress_r14.py`·`_r15.py`·`t40_witnesses_r13.py` 의 `need/require` 조건은 동일하고 위치만 뒤로 갔다(원본 `structural==0` 요구 · 양성 승인 요구 6). 추가된 것은 자료 열(`order_violation_detected` · `approval_requirements`)과 인쇄 줄뿐 · 기대·판정 열 무변경. 【직접 재실행】 묶음 12·13·14 에서 S80 본체(`seal-before-cleanup detected 2/2 · original structural [1,1]`) · S85 본체(ON-1 17 · AX-1-A 11 · AX-1-B 4 · `3/3 rejected with class reason`) · S83 본체가 실행된 뒤 마지막 승인 요구에서 FAIL — `R19-HARNESS-REPAIR.md` 인용문·`r19-harness-after-*.log` 와 글자 단위로 같다. `structural` 2→1 【직접】: `t40_structure.py:401-407` 이 `dominance.audit:327` 의 `'R16 unresolved semantic dependency closure'` 위반이 이미 있을 때 `require` 를 evidence 로 바꾸고 `structural_count_r18/r19` 둘을 보고한다 — 계수 정의 변경이 아니라 한 의무의 이중 계상 제거이며 옛 계수 병기. S90 【직접】: `R18→R19-COMPARISON-EXPECTED.json` 차이(586/2206/49)는 전부 검사기 파일 6(kernel·preconditions·admission·dominance·structure·census)에 있고 생산 9모듈은 0 — 「검사기가 저작자 동결 이후 안 바뀌었다」는 검사의 회차별 재동결이지 생산 기대의 약화가 아니다(초기 FAIL 로그 보존 확인).

**물음 ⑤ — 세 수와 재정 요청.** `U1~U6` 독립 도출은 §2. 재정 요청: **①** 【직접 코드】 `t40_resources.entry:437-440` 은 `F.remember(exc)` 뒤 `raise failure(exc) from exc` · `t40_receipts.io_boundary:162-173` 도 `F.remember(exc)` 뒤 포장을 `from exc` 로 던진다. 흐름: 안쪽 `F.entry`(중첩 capture)가 raw 를 failures 에 넣고 unwrap 으로 재던짐 → handler 가 raw 를 다시 remember(failures 에 raw 둘) → 포장이 바깥 경계 capture 에 잡혀 **business = 포장(`__cause__`=raw) · failures = [raw, raw, 포장] · 호출자 = 포장**. 18차 `preservation()` 은 셋 다 raw 일 때만 비위반으로 판정했으므로 검사기 자신의 기준으로는 위반이고, T53 ⑴ 「업무 결과**나** 실패 목록에서 … 사라지면」의 자연 독해도 「어느 한쪽」이다. IO 오류는 §5′.18 이 Γ 안으로 명시한 「입출력 오류」다. 「어느 한쪽」이면 원본이 `R.entry` 2 + `io_boundary` 경유 자리 전부에서 I-R 위반 → PO-RESULT-01 이 Violated 로 뒤집히고 T53 이 예고한 「다음 반례」(원본 수리 재저울)가 된다. 재정 문언 해석이므로 **상신 사유**. **②** `driver_boundary` 는 business/failures 에 raw 를 두고(형태 동결 【직접】) 호출자(셸)에는 종료 코드만 줄 수 있다 — T53 ⑴ 이 이름 짓는 그릇은 업무 결과·실패 목록이고 프로세스 경계에서 객체 동일성은 물리적으로 불가능하며 STRUCT-ENTRY 설계로 41~44차가 PO-RESULT-01 을 Satisfied 로 세웠다 → **기각**(새 사실 없음). **③** `gate/` 의 재정문 어디에도 「11형태 국소 미발급」 문언이 없고(grep 0 · 44차는 관측으로만 적었다) 이 발주문 자체가 「최종 승인에 이르면 L」로 기준을 못박았다 · 환경 4 의 국소 발급은 T52 ⑶ 을 어기지 않는다(제외를 승인 근거로 쓴 것이 아니라 관계의 시야 밖) → **기각**. 다만 그 발급을 낸 H-bind 규칙의 구멍은 별도 지적(OQ-2). **④** 【직접 실험】 커널의 `OPEN_PREMISES` 를 비우고 `open:*` 단계를 뺀 유도로 `verify_baseline` → `issued True · derived 989 · failed []` → `build(원본)` → `U5 solved · approved True · route identity`. 즉 「바깥 결과 정리」로 좁히면 **원본은 실제로 승인된다**. 그때 함께 승인되는 상태: I-S/I-C/I-P 의미 전제 셋 미증명(PO-GATE-01 문언의 「의미 모델 또는 결부 증명」 결손 유지) · ① 의 포장 완료가 보존표에 사실로만 기록 · :310 류 thunk 안 창 미관측(P-DEFERRED 가 Attribute 를 지연으로 봄) · OQ-2 의 helper 후보가 전체 승인. 의무 문언 변경은 Owner 몫 → **상신 사유**, 위 넷은 그 결정의 사실이다.

## 2. 세 수 · PO · 지적

**`U_r`=6 도출**(독립 기준). U1 구체 연산→transfer 전칭 대응 lemma 없음(재작성 4 는 관계 경로로 우회했을 뿐) · U2 일반 완료 합성 없음(합동은 허가 재작성 둘에만) · U3 실제 callable·중첩 소유자 미해결 + H-bind 프레임 의존 구멍 【직접】 · U4 thunk 안 창(:310 · handler · 포장) 미해결이고 형식 ⑷ 이 시야 밖으로 뺐음 · U5 CONNECT-I 세 전제 미유도 + 전제 집합이 root 보다 약함(OQ-1) · U6 비교 성공⇒I lemma 없음. 전체 폐쇄 0 → **6**. **`B_r`=16/16** 【직접 A.build: 원본·재작성 4·S48 DENIED · R13 넷 T51 제외 · 런타임 10 은 `submitted-original` root 경유로 unresolved】. **`L_r`=0**: 기존 7 재실행 0/7 【물려받음 JSON】 + `build` 가 어떤 후보도 `U5` 로 막으므로 잘못된 전체 승인은 구조적으로 불가 【직접】 — 공허한 0 이며 새 독립 탐색 미완료는 0 으로 세지 않는다. 합성 프로브 3 의 국소 발급은 최종 DENIED 라 L 밖이되 ④ 좁히기 아래서는 L≥3 이 된다.

| PO / I | 상태 | 근거 |
|---|---|---|
| PO-EXEC-01 / I-A | Satisfied | 생산 9모듈 `git diff da25f48..b7f8e47` 0 【직접】 · 44차 근거 유지 |
| PO-RESULT-01 / I-R | Satisfied | 자연 관측 T53 ① 비위반 · 재정 요청 ① 이 「어느 한쪽」으로 재정되면 Violated 로 뒤집힘(남은 목록) |
| PO-FAIL-01 / I-F | Satisfied | 무변경 · 43차 유지 |
| PO-STATE-01 / I-A | Satisfied | Machine 형태 동결 【직접】 · 다른 모듈의 stopped/index/state store 0 【직접 grep】 |
| PO-IO-01 / I-C | Satisfied | 무변경 · IOClear 생성 자리 하나·별칭 0 【직접 grep】 |
| PO-PROFILE-01 / I-C | Satisfied | 무변경 · 43차 유지 |
| PO-PRESERVE-01 / I-P | Satisfied | 무변경 · 43차 유지 |
| PO-ENV-01 / I-E | Satisfied | execute finally tail 형태 동결 【직접】 |
| PO-RESOURCE-01 / I-X | Satisfied | 무변경 · 43차 유지 |
| PO-ISOLATE-01 / I-X | Satisfied | 무변경 · 43차 유지 |
| PO-SEMANTIC-01 / I-S | Satisfied | §5′.10/.12/.13 바이트 동일 【직접】 · 207 ID·부류·기대 무변경 【표본 36 직접 · 나머지 물려받음】 |
| PO-GATE-01 / I-A·I-C·I-S | **Violated** | 원본·필수 16 비승인 · U5 세 전제 미유도 · H-bind 구멍 · 회귀 10 실패 |

`Satisfied=11 Violated=1 Unexamined=0` · 대장 누락 반례 0 · 심사 대상 ①②③⑤ 성립 · **④ 불성립**. 남은 목록 = `PO-GATE-01` · U1~U6 · OQ-1~4 · 재정 요청 ①④ · opener 반환 계약 [명시 없음] · 회귀 S14·S48·S65·S68·S69·S75·S76·S80·S83·S85.

**지적 — T54 는 46차 저작을 두지 않았다. 아래는 「무엇이 끊겼는가」의 기록이며 처분은 T55 가 정한다.**

**OQ-1 · MED — PO-GATE-01 / I-R·I-A / T3·P6 / 갈래 ⑴ / SITE-14·54 / trace: `verify_baseline` → `CONNECT-I`(lemma 3 + 진입 489 + 소유자 10 + 열린 3) → root `connected-I` / 관측 【직접】: 전제 집합에 thunk 안 최초 오류 보존이 없고 ⑷ 이 그것을 시야 밖으로 뺐으며 `R.entry`·`driver_boundary` 보존표는 기록이다 — 좁히기 실험에서 :310 창·포장 완료가 미판정인 채 root 가 섰다 / 문안: 「CONNECT-I 에 전제 ⒠ 『경계 thunk 안 최초 오류 보존』 규칙(부조건 = 창 안 직접 평가·handler·포장 자리 열거 · 정당화 자리별)을 더하거나, root 결론을 『바깥 결과 정리』로 낮추고 `connected-I` 와 다른 이름을 준다.」**

**OQ-2 · MED — PO-GATE-01 / I-A·I-R / P6 / 갈래 ⑴ / `t40_baseline_preconditions.h_bind:563` · 커널 `HELPER-COMPLETION:207` / trace: `def h(): super().m()` + `h()` → BINDING-EVENT → HELPER-COMPLETION(H1~H5 참) → CALLER-COMPOSITION 동일 → 국소 ISSUED / 관측 【직접】: 프로브 3(`super()`·`locals()`·`eval`) 전부 국소 발급 · 실행 결과 상이(RuntimeError · `{}`) · 최종은 U5 로만 DENIED / 문안: 「H2 에 프레임 의존 이름(`super`·`locals`·무인자 `vars`·`eval`·`exec`·`sys._getframe`·`inspect.currentframe`·`__class__`)의 Load 금지를 더하고 ⑸ 정당화에 그 근거를 적는다.」**

**OQ-3 · LOW — PO-GATE-01 검증 근거 / §5′.20 ⑶ / `owner-finalize-diagnostic`·`machine-lemma` 행 / 관측 【직접】: 정당화 문장(「모든 업무 호출은 capture 안」 · 「stopped 미복원」)이 부조건(P-DEFERRED 는 Attribute thunk 를 지연으로 봄 · P-SHAPE-Machine 은 자기 모듈만) 보다 넓다 / 문안: 「문장을 부조건 범위로 좁히거나 `P-OWNER-DIRECT-EVAL`·`P-NO-MACHINE-STATE-STORE` 술어를 더한다.」**

**OQ-4 · 기록(상신 사유) — PO-GATE-01 / I-S·I-C·I-P / `t40_certificate_kernel.OPEN_PREMISES:129,293-296` / 관측: 세 규칙은 형식이 아니라 커널이 이름으로 거부한다 · 쓸 수 있는 규칙은 판명 줄에 지목 / 처분은 T55.**

## 3. 재현 표 · 검증 경로 · 미검증

⒜ 지문 【직접】: HEAD `b7f8e47d82fe9f6e…` · `.audit-sandbox` pin 일치 · 9모듈 sha16 아홉 개 R19-IMMUTABILITY 와 동일(`3d7ee33… e8ea6c3… 56e5f41… a039bf9… b94e549… 2a1a0df… a99bb3a… 62daa44… 06de01e…`) · §5′.10 22,350 `33598684cfd07c2a` · .12 2,818 · .13 2,958 · .18 3,579 `e6fb5b46c97d7bda` · .19 4,276 `423f19bac6221370` · **.20 13,889 `1364351646c69219`** · 메모 267,196 `e484bf937fd69a25` = R19 사본 바이트 동일 · 법 62 · ARTIFACTS 표본 5 sha 일치.
⒝ guards 【직접】: 정상 exit 0 · `-O` exit 0 · `false` 정상 exit 1 · `false -O` exit 1(`14 all_blocked True`) · 실행 후 git status 무변경.
⒞ verify_baseline 【직접】: 위 여섯째 줄 · 좁히기 실험 issued True/approved True · 원 커널에서 `open:*` 뺀 유도는 `RULE_APPLICATION_FAILED:root`.
⒠ 회귀 표본 【직접 · `--src …/pd-m1b-t40-v49/src` · 픽스처 `work/r19-scratch` 매 묶음 제거】: 묶음 2(25 PASS · 63초) · 12(S80 FAIL/S81·S82 PASS · 2분 08초) · 13(S83 FAIL · 2분 46초) · 14(S84 PASS/S85 FAIL · 1분 49초) · 15(5 PASS · 18초) = 36건 · PASS/FAIL 열 19차 로그와 **전건 동일**. 나머지 171 【물려받음】.

| 명령 | 마지막 출력 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD; git status --porcelain` | `pin=b7f8e47…` · `?? .audit-sandbox gate/ src/` |
| venv python 지문·절 분할 | `### §5′.20  13889 1364351646c69219` |
| venv python `K.verify_baseline(base, load('R19-U5-DERIVATION.json'))` | `issued False derived_steps 988 failed_steps [... 'root'] sc 484/484 2.0s` |
| venv python U5 세 경로 | `PATH none: U5 unresolved … no U5 derivation submitted` |
| venv python 좁히기 | `NARROWED admission: U5 solved approved True` |
| venv python H-bind 프로브 | `super-in-method … local_issued True … helper super -> raises RuntimeError super(): no arguments` |
| `t40_r19_guards.py [false] [-O]` ×4 | exit `0 1 0 1` |
| `t40_run_r19.py t40_regress.py --src <사본 src> --only …` ×5 | `PASS/FAIL columns IDENTICAL` ×5 |
| `git diff --stat da25f48..b7f8e47 -- <9모듈>` | (빈 출력) |
| `git checkout -- work/; git status --porcelain` | `?? .audit-sandbox` `?? gate/` `?? src/` |

[미검증] 회귀 171건·불변 37 대조·14종 거짓 유도 개별 값·L 재실행 7·R19-DEPENDENCY 옛 대상 계열은 재실행하지 않았다(코드·JSON 대조만). 자문 7회차 원문·결정문 추기 82·19차 발주문(「11형태 비승인」 문언의 출처)은 동봉되지 않아 [미확인]. I-S 동치의 참은 유한 증인뿐이다. 좁은 확인 판 셋 미열람 · 정본 리포는 python 해석기 외 접근 0.

남긴 파일: 없음 — `git status --porcelain` 출력 그대로:
```
?? .audit-sandbox
?? gate/
?? src/
```
배경 작업 0 · 픽스처 제거 확인(`scratch absent`). 약정 관측: 턴 약 13 · 도구 호출 약 32 · 지적 4(MED 2 · LOW 1 · 기록 1) · 재정 요청 처분 = 상신 2 / 기각 2 · 한도 중단 0 · usage(json) 는 발주자 회수.
