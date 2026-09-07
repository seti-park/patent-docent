# HANDOFF — 다음 세션은 여기서 시작한다

**작성 2026-09-01 · 갱신 2026-09-07(83차) · HEAD 는 `git log -1` 로 본다(여기 적으면 낡는다).**
**이 문서는 총괄 저작이다**(감수 원문이 아니다 · 규율 10).

---

## 0. 첫 화면 — 지금 무엇을 해야 하나

**★ 09-07 83차 갱신 — Owner 지시로 v33 저작 좌석이 총괄에서 `좌석 M3` gpt-6-astra xhigh 로 바뀌었다(`D-20260905-02` §17 추기 42).** 레인 = `~/projects/workspaces/pd-lanes/astra-m3-t40v33/`(SPEC `SPEC-m3-t40-author-v33.md` · STATUS · FINAL · EV · 기동 10:10:06 · 감시 = `grep ^EXIT= STATUS`) · 작업장 = `~/projects/workspaces/pd-author-t40v33`(자체 git · 출발점 `9e287fe` · 산출 = `work/` 작업 트리 · 회수 `git diff --stat`) · **지금 할 일 = FINAL 회수 → 대조(§3 성공 판정 1~6 을 총괄이 디스크에서 재실행 · sha 표 대조 · 정본 `git status` 빈 출력) → Owner 리뷰 브리핑(설계 판단 목록 · 미해결 행 · OB 폐쇄 근거 · 회귀 결과 · 리뷰 회신 서식) → Owner 회신 → 반입·커밋 → 사본 재핀 → SPEC v31 → 31차.** 82차의 ⑴~⑸ 는 그대로 산출물 정의로 유효하다(저작자만 바뀜). 코드 v32(정본·`t40-measure/` 무변경). Owner 재정 대기 = 없음(리뷰 대기는 FINAL 뒤). 살아 있는 배경 = 저작 레인 1 + 킵얼라이브 cron.

> [정정 2026-09-07 · 83차] 82차의 「v33 저작(총괄 · 약 하루)」은 Owner 지시로 astra xhigh 저작으로 바뀌었다.

**★ 09-07 82차 갱신 — 재정 T45(Owner 육성 `T45: ① A / ② A / ③ A` · `ruling-20260907-03-T45.md` · 브리핑 `226a699f-…` · `D-20260905-02` §17 추기 41 · T44 §3 보정).** ① v33 = **집행 자리·자원 대장(§5′.11)** + 독립 대조기 CLI 폐쇄(기능 유지)·증거 경로 고정 + OB-1~4 수정 ② 게이트 종결 규약 = 고정 범위 의무 충족 + 대장↔코드 양방향 대조 + 남은 자리 목록 제출(PASS 문장 불변 · HIGH 0 PASS 불채택) ③ T44 세 회차 조건 = 재검토 신호 · 처분 범주 4 · 진행도 = 불일치·미충족·미심사 수. **지금 할 일 = v33 저작(총괄 · 약 하루) = ⑴ 메모 v33 §5′.11 대장(사람 분류) · §9 판정 방법 ⑵ `t40_sites.py` 정적 추출·양방향 대조(회귀 사례로 편입) ⑶ `t40_replay.py` `__main__` 폐쇄 · `--receipts`/`--evidence-dispatch` 를 고정 규칙(`<evidence>/calls` · `<evidence>/dispatch`)으로 ⑷ OB-1 공용 `bind_receipts` · OB-2 dispatch 결속·후보 선검사 · OB-3 kind 전달·중첩 형태·영수증 OSError → 부적격 · OB-4 보호 집합(evidence 루트·dispatch·retired·LANE_DIR) ⑸ 회귀 v12 전건 → 커밋 → 사본 재핀 → SPEC v31(§9 개정 · 지적 `OC-*`) → 31차 기동(T45 ① 효력 · 묻지 않음).** 코드 v32. Owner 재정 대기 = 없음. 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 82차] 81차의 「결정 브리핑 T45 → Owner 회신」은 끝났다(① A / ② A / ③ A).

**★ 09-07 81차 갱신 — 자문 4회차 회신 도착·처분(`t40-loop-closure-20260907-0914/REPLY.md` · 「해당 없음」 · D-01~D-05 전부 수용 · `D-20260905-02` §17 추기 40).** 요지 = 발산 아닌 「적용 자리 미발견 루프」 · 빠진 층 = **성질 → 적용 자리·자원·순서 → 기제**(집행 자리·자원 대장 · 사람 분류 + 코드 추출 · 게이트 양방향 대조) · 관찰 2 에 직접 작용 = ⓒ 자유도 축소·ⓔ 대장 · 벤더 교체·실측 먼저는 결손을 안 없앤다 · 종결 규약 = 고정 범위 의무 충족(HIGH 0 PASS 는 부당) · T44 는 재검토 신호 규약(종결 규약 아님). **지금 할 일 = 결정 브리핑 T45 발행(① 다음 단계 ② 게이트 종결 규약 ③ T44 보정) → Owner 회신 `T45: ① _ / ② _ / ③ _` → 재정대로 v33(자리·자원 대장 §5′.11 · `t40_sites.py` 정적 추출 · OB-1~4 수정 · 진입점 정리) → 31차.** 코드 v32. 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 81차] 80차의 「Owner 가 봉투를 넣고 회신」은 끝났다(09:4x).

**★ 09-07 80차 갱신 — Owner 육성 `B`(자문 4회차) → 봉투 발행 `~/projects/workspaces/advice/t40-oracle-closure-20260907/t40-loop-closure-20260907-0914/`(PROMPT `c884d6a5` · zip `5ccdb14d` · 동봉 2 = `SITUATION-4.md` · `APPROACH-4.md` · 질문 Q1~Q6 = 수렴/발산 · 연역 명세의 빈 층(자리 열거) · 구조 선택지 ⓐ~ⓔ · 종결 규약 재설계 · T44 평가 · 반론 · 위험 어휘 0) · `D-20260905-02` §17 추기 39.** **지금 할 일 = Owner 가 PROMPT.md + bundle.zip 을 ChatGPT astra pro 에 넣고 회신을 그 디렉터리 `REPLY.md` 에 원문 저장 → 「t40-loop-closure 회신 왔어」 → 총괄이 봉투 대조(MANIFEST 2 · PROMPT sha) → 처분표(추기 40) → 회신이 가르는 길(ⓐ 총괄 v33 / ⓑ sol-coder 저작 / ⓒ 자유도 축소 v33 / ⓓ 실측 먼저 = PASS 재정)을 Owner 재정으로.** 코드 v32 · 30차 지적 OB-1~4 는 수정 문안 확정·미구현. Owner 재정 대기 = 회신 전달 1건. 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 80차] 79차의 「Owner 채팅 회신 대기 1건(A/B/C/D)」은 B 로 닫혔다.

**★ 09-07 79차 갱신 — M1b 30차 = REVISE 4(OB-1·2·4 HIGH · OB-3 MED · `docs/lessons/2026-09-07-astra-m1b-t40-measure-v30.md` · `D-20260905-02` §17 추기 38 · 심사 대상 ① 충족 · 도출 누락 0 · 새 보증 요구 0 · 갈래 전부 ⑴ · closed 107 · partially 5) → **재정 T44 판정 = 「같은 P/T 세 회차 연속」 충족(T3·P5·P6·P7 넷) → 자동 기동 불가 · Owner 상신.** 잔여 4 = 독립 대조기의 MANIFEST·attempt 결속 누락(OB-1) · 소비기 dispatch 경로 미결속·목록 밖 후보 선읽기(OB-2) · 처분 분류 미전달 4 경계(OB-3) · sandbox 보호 집합에 evidence 루트·dispatch·retired 누락(OB-4). **지금 할 일 = Owner 채팅 회신 대기 1건 = 다음 단계(A 총괄 v33 → 31차 `OC-*` 추천 / B 자문 4회차 / C v33 을 M3 sol-coder 에 발주 / D 실측 먼저 = PASS 문장 변경 재정) → 재정대로**(A·C 면 v33 = 공용 `bind_receipts` · `--evidence-dispatch` 결속 · kind 전달·중첩 형태 검사 · 보호 집합 확장 · C93~C97 · S11~S13 → 회귀 전건 → 사본 재핀 → SPEC v31 → 기동). 코드는 아직 v32(28·29차 반영)다. Owner 사후 확인 대상 = 없음. 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 79차] 78차의 「30차 판정 회수 → PASS 면 실측 · REVISE 면 T44 규약 판정」은 REVISE 4 · T44 세 회차 연속 조건 충족(상신)으로 끝났다.

**★ 09-07 78차 갱신 — Owner 육성 `30차: A / 규약: 채택`(08:3x · 채팅) → **재정 T44 = 상설 기동 규약**(`ruling-20260907-02-T44.md` · 게이트가 도출 누락 0 · 새 보증 요구 0 · 지적 전부 갈래 ⑴ 이면 총괄이 묻지 않고 다음 판 기동 · 갈래 ⑵·⑶ 또는 같은 P/T 세 회차 연속이면 상신) · M1b 30차(`OB-*` · 설계 v32 · 사본 `0990f64` · `pd-lanes/astra-m1b-t40v30/`) 기동 08:35:27 · `D-20260905-02` §17 추기 37.** **지금 할 일 = 30차 판정 회수(Monitor · 약 25분) → 감수 원문 `docs/lessons/2026-09-07-astra-m1b-t40-measure-v30.md` 반입 + DISPOSITIONS + 추기 38 → PASS 면 실측 착수(67차 순서 + v32 절차: 런마다 `read` 완주 뒤 `t40_drive.py seal-evidence <r>` · 지표기 `--receipts <evidence>/calls` · 결함 런 `retire <r> <사유>`(런 폴더는 `retired/…/run/` 보존 · exit 16 이면 새 ID 재정) 뒤 `source <r>` 부터) · REVISE 면 **T44 규약 판정**(조건 충족 → v33 → 31차(`OC-*`) 기동 · 미충족 → Owner 상신).** Owner 재정 대기 = 없음. 살아 있는 배경 = Monitor 1(30차) · 킵얼라이브 cron.

> [정정 2026-09-07 · 78차] 77차의 「Owner 채팅 회신 대기 ①②」는 닫혔다(`30차: A / 규약: 채택` → T44).

**★ 09-07 77차 갱신 — M1b 29차 = REVISE 5(OA-1·2·4·5 HIGH · OA-3 MED · `docs/lessons/2026-09-07-astra-m1b-t40-measure-v29.md` · `D-20260905-02` §17 추기 36 · **심사 대상 ① 도출 완전성 충족(처음)** · 도출 누락 0 · 새 보증 요구 0 · 갈래 전부 ⑴ · NZ-1·2 closed · NZ-3~5 partially) → 설계 메모 **v32**(sha16 `4baa56cfaacb68fb` · v31 = `.v31.md`) · 구동기 **v11**(retire 런 폴더 보존·대조 · seal run_id) · 대조기 **v6**(결속 뒤 선판별) · 영수증 **v6**(run_id 결속 · evidence_files(run_id) · 목록 경로 경계) · 지표 **v31**(kind · 결속 블록 · calls basename) · 회귀표 **v11**(121 사례(L 13 · F 7 · C 89 · X 2 · S 10) FAIL 0(04:46 → 05:0x · EXIT=0)) · 다섯 스크립트 첫 줄 bytecode 쓰기 금지.** **지금 할 일 = Owner 채팅 회신 대기 = ① 30차(`OB-*`) 기동 여부 ② 상설 규약(도출 누락 0 · 새 보증 요구 0 · 갈래 ⑴ 만이면 총괄 기동 · 그 밖·같은 P/T 세 회차 연속이면 상신) 채택 여부**(추천 = A · 채택 · SPEC v30 = `pd-lanes/astra-m1b-t40v30/SPEC-m1b-t40-v30.md` 의 `__PIN__`·`__OWNER_DECISION__`·지문 자리를 채운 뒤 사본 재핀 · bundle 지문 재생성 · `launch.sh` · Monitor). 실측 절차(v32) = 런마다 `read` 완주 뒤 `seal-evidence <r>` · 지표기 `--receipts <evidence>/calls`(basename 규칙) · 결함 런 `retire <r> <사유>`(런 폴더는 `retired/…/run/` 에 보존 · exit 16 이면 새 ID 재정) 뒤 `source <r>` 부터. Owner 사후 확인 대상 = 없음. 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 77차] 76차의 「29차 판정 회수 → PASS 면 실측」은 REVISE 5 로 끝났다(→ v32 · Owner 상신).

**★ 09-07 76차 갱신 — Owner 육성 `29차: A`(04:2x · 채팅) → M1b 29차(`OA-*` · 설계 v31 · 사본 `ed011a1` · `pd-lanes/astra-m1b-t40v29/`) 기동 04:21:43 · `D-20260905-02` §17 추기 35.** **지금 할 일 = 29차 판정 회수(Monitor · 약 25분) → 감수 원문 `docs/lessons/2026-09-07-astra-m1b-t40-measure-v29.md` 반입 + DISPOSITIONS + 추기 36 → PASS 면 실측 착수(67차 순서 + v31 절차: 런마다 `read` 완주 뒤 `t40_drive.py seal-evidence <r>` · 지표기 `--receipts evidence/calls --run <r> --sandbox <새 홈 fs 경로>` · IO 결함 런은 `retire <r> <사유>` 뒤 `source <r>` 부터 · exit 16 이면 새 ID 재정) · REVISE 면 갈래별 처분(P·T 위반·도출 누락 = v32 / 새 보증 요구 = Owner 범위 재정 / 방식 자체 재REVISE = Owner 상신).** Owner 재정 대기 = 없음. 살아 있는 배경 = Monitor 1(29차) · 킵얼라이브 cron.

> [정정 2026-09-07 · 76차] 75차의 「Owner 채팅 회신 대기 1건」은 닫혔다(`29차: A`).

**★ 09-07 75차 갱신 — M1b 28차 = REVISE 5(NZ-1·2 HIGH · NZ-3~5 MED · `docs/lessons/2026-09-07-astra-m1b-t40-measure-v28.md` · `D-20260905-02` §17 추기 34 · 첫 연역 명세 심사 · **도출 누락 0 · 새 보증 요구 0 · 갈래 전부 ⑴** · MY~NY 102 closed) → 설계 메모 **v31**(sha16 `4d2fde278d953391` · v30 = `.v30.md`) · 구동기 **v10**(`retire` · `seal-evidence` · attempt) · 대조기 **v5**(T43 선판별 · disposition · 쓰기 자리) · 영수증 **v5**(VERSION 4 · attempt · attempts · MANIFEST) · 지표 **v30**(law_status · 적재 블록 · 접두 · prompt_path) · 회귀표 **v10**(113 사례(L 13 · F 7 · C 84 · X 2 · S 7) FAIL 0(04:07 → 04:19 · EXIT=0)).** 도전자 명기 「격리·처분 합성 재REVISE — Owner 상신 대상」. **지금 할 일 = Owner 채팅 회신 대기 1건 = 29차(`OA-*`) 기동 여부**(추천 = 기동 · SPEC v29 = `pd-lanes/astra-m1b-t40v29/SPEC-m1b-t40-v29.md` 의 `__PIN__`·`__OWNER_DECISION__` 을 채운 뒤 사본 재핀 · bundle 지문 재생성 · `launch.sh` · Monitor). 실측 절차 변경(v31) = 실측 직후 **`t40_drive.py seal-evidence <r>`**(봉인 · 결과 커밋에) · 결함 런은 **`t40_drive.py retire <r> <사유>`**(exit 16 이면 새 ID 재정) 뒤 `source <r>` 부터 · 지표기는 `--receipts` 디렉터리의 부모에서 `MANIFEST-sha256-<r>.txt`·`attempts-<r>.json` 을 읽는다. Owner 사후 확인 대상 = 없음(§8 ⓟ 는 문언상 제외로 재분류). 살아 있는 배경 = 킵얼라이브 cron 만.

> [정정 2026-09-07 · 75차] 74차의 「28차 판정 회수 → PASS 면 실측」은 REVISE 5 로 끝났다(→ v31 · Owner 상신).

**★ 09-07 74차 갱신 — 접근 전환 집행 완료: 설계 메모 v30(연역 명세 · sha16 `41024407d373334d` · v29 = `.v29.md`) · 코드 v29 불변(9종 바이트 동일) · 회귀 106 전건 재실행 FAIL 0 · 사본 재핀 `6141346` · bundle 51 파일 · SPEC v28 · M1b 28차(`NZ-*`) 기동 03:21(`pd-lanes/astra-m1b-t40v28/` · `D-20260905-02` §17 추기 33).** v30 의 새 것 = §5′(신뢰 전제 T1~T4 · 입력 범위 · 허용 부작용 · 처분 다섯 · 성질 P1~P7 표 · 절차 의무 · 범위 밖 ⓐ~ⓖ · 합성 전제 · 잔여 위험 · v29 문언 보존) · §2 연결 이력 · §9 심사 대상 다섯 + 지적 세 갈래 · PASS 문장 불변. **지금 할 일 = 28차 판정 회수(Monitor · STATUS `EXIT=` · FINAL 바이트 · EV 오류 · 약 25분) → 감수 원문 `docs/lessons/2026-09-07-astra-m1b-t40-measure-v28.md` 반입 + DISPOSITIONS + 추기 34 → PASS 면 실측 착수(67차 순서 · `--sandbox` 는 원본과 겹치지 않는 홈 fs 새 경로) · REVISE 면 지적을 세 갈래로 처분(P#/T# 위반·도출 누락 = v31 · 새 보증 요구 = Owner 범위 재정 상신 · 「방식 자체」 재REVISE 면 Owner 재정 상신).** Owner 사후 확인 대상 1건 = 메모 §8 ⓟ(영수증과 산출물이 함께 바뀐 자료의 진위 = 탐지 약속 밖 · T42 문언 이행으로 분류). 살아 있는 배경 = Monitor 1(28차) · 킵얼라이브 cron.

> [정정 2026-09-07 · 74차] 73차의 「지금 할 일 ⑴~⑸」는 전부 끝났다(28차 기동까지).

**★ 09-07 73차 갱신 — 자문 3회차 회신 도착·처분(`advice/t40-oracle-closure-20260907/t40-oracle-strategy-20260907-0217/REPLY.md` · NOT-READY · 지적 1 + Q1~Q6 · C-01~C-07 전부 수용 · `D-20260905-02` §17 추기 32).** 요지 = **미해결의 본체는 재실행 방식이 아니라 보증 범위와 게이트 종결 기준의 부재** · 성질 후보 G1~G7 + 절차 의무 3 · 닫힘에는 입력 범위·신뢰 전제·허용 부작용·불확실 시 처분이 붙어야 함 · 현 구조(전 검사 + 영수증·격리 재실행 + 후 검사)는 유지(ⓓ 성질별 책임 분리 · 구조를 다시 바꾸면 검증 근거 상실) · 종결 기준 = 심사 대상 5(도출 완전성 · 신뢰·입력·부작용 경계 · 기제 집행·합성 · 검증 근거 · 미충족 상태 처분) · 반례 시험은 보조(성질 위반 → REVISE / 상류 누락 의무 → 완전성 실패 / 새 보증 요구 → Owner 범위 재정 대상) · T43 정합(재실측·제외 이력 연결 필수) · 「실측 먼저」는 Owner 승인 없이 불가. **지금 할 일 = ⑴ 설계 메모 v30 연역 명세(§5 = 성질 P1~P7 · 신뢰 전제 T1~T4 · 입력 범위 · 허용 부작용 · 처분 4종 · 성질별 기제·증명 의무·실패 시 처분 · §2 연결 이력 · §9 심사 대상 5) ⑵ 코드 v29 불변 · 회귀 106 전건 재실행 ⑶ 사본 재핀 · bundle 갱신(자문 3회차 봉투 4 파일 추가) ⑷ SPEC v28 ⑸ M1b 28차(`NZ-*`) 기동 → PASS 면 실측 착수.** PASS 의 문장은 T42·T43 효력 밖 조항대로 불변 — 심사 대상 5 는 그 문장을 게이트가 판정하는 방법.

> [정정 2026-09-07 · 73차] 72차의 「Owner 가 v2 봉투를 넣고 회신을 REPLY.md 에」는 끝났다(03:0x · Owner 가 채팅에 붙임 · 총괄이 저장 · G7 행 뒷부분은 렌더러에서 유실 [미확인]).

**★ 09-07 72차 갱신 — 자문 3회차 봉투 v1 이 ChatGPT 보안 분류기에 차단(어휘 밀도) → v2 재발행 `advice/t40-oracle-closure-20260907/t40-oracle-strategy-20260907-0217/`(PROMPT `f92e9516` · zip `6dda96bf` · 동봉 2 · 거시 진단·전략 질의) · Owner 피드백 2건(귀납 → **연역 명세**로 · 자문 질문은 상황→접근·반복→거시 진단) → D-02 추기 31 · 기억 `advice-and-gate-loop-method` · LANE-RUNTIME 함정 P.** **지금 할 일 = Owner 가 v2 봉투를 넣고 회신을 `REPLY.md` 에 → 처분(추기 32) → 회신의 성질 집합으로 v30 연역 명세(성질 P1..Pn · 기제 · 증명 의무 · 범위 밖 선언) → 28차 발주문에 종결 규약(PASS = 도출 완전성 · 기제 집행 · 기제 없는 성질 0) → 기동.** v29 코드·회귀 106 은 그대로(연역 명세의 기제로 재배치).

> [정정 2026-09-07 · 72차] 71차의 「봉투 전달 → 회신」 중 v1 봉투는 차단됐다 — v2 로 다시 보냈다. 「28차 = v29 그대로」도 바뀐다(v30 연역 명세 뒤).

**★ 09-07 71차 갱신 — M1b 27차 = REVISE 4(NY-1·2 HIGH · NY-3·4 MED · `docs/lessons/2026-09-07-astra-m1b-t40-measure-v27.md` · `D-20260905-02` §17 추기 30) · 도전자 「재조립 방식 자체를 다시 REVISE → T43 ② 자문 3회차」 · T43 ① A 자체는 정합 판정.** v29 = 대조기 v4(런 ID 어휘·선등록·목적지 realpath(dangling 포함) · 포인터 원시 경로 대조 · NUL 토큰) · 영수증 v4(`io_fault` 필수) · 구동기 v9 · 지표 v29 · 회귀 v9(106). **지금 할 일 = 자문 3회차 봉투(`~/projects/workspaces/advice/t40-oracle-closure-20260907/t40-oracle-closure-20260907-0059/PROMPT.md`(sha16 `173d52ff` · zip `0971f9be` · 29 파일) + `bundle.zip`)를 Owner 가 ChatGPT astra pro 에 넣고 회신을 `REPLY.md` 에 붙임 → 총괄 처분(D-02 추기 31) → 28차(`NZ-*`) 발주문에 종결 규약 반영 → 기동.** Owner 몫 1건(봉투 전달·회신).

> [정정 2026-09-07 · 71차] 70차의 「27차 → PASS 면 실측」은 REVISE 4 로 끝났고 T43 ② 대로 자문 3회차로 간다.

**★ 09-07 70차 갱신 — 재정 T43(`ruling-20260907-01-T43.md` · Owner 「T43: ① A / ② A」 · 브리핑 `f4707e4d-…`) = IO 결함 런은 재조립 불가·재실측 · v28 → 27차.** 설계 메모 **v28** · 대조기 **v3**(결함 주입 삭제 · 결함 영수증·halt 4행 = exit 4 「재실측」 · NX-2 경계 보존 치환 · NX-3 링크 해석 전 거부·좌표 어휘·쓰기 직전 realpath) · 영수증 **v3** · 지표 **v28** · 회귀표 **v8**(103 = L 13 · F 7 · C 78 · X 2 · S 3). **지금 할 일 = 회귀 전건 PASS 확인 → 기록 커밋 → 사본 재핀 → M1b 27차(`NY-*`) 기동 → PASS 면 실측 착수.** 재실측 규약 = 메모 §2(결함 런은 증거 보존 · 원인 수리 · 재실행 · 종결 기록 남았으면 새 ID 는 채팅 재정).

> [정정 2026-09-07 · 70차] 69차의 「재정 T43 회수」는 끝났다(① A / ② A).

**★ 09-06 69차 갱신 — M1b 26차 = REVISE 4(NX-1~3 HIGH · NX-4 MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v26.md` · `D-20260905-02` §17 추기 28) · 도전자 명기 「재조립 방식 자체의 두 번째 연속 REVISE → T42 §2 재상신 요건 충족」.** 잔여 = IO 결함 재현 정밀도(NX-1 · 파일 객체 write · 같은 행 n번째 · outcome 종류만) · 경로 포함 예외 문언 정규화(NX-2) · sandbox 링크·좌표 탈출(NX-3) · 남은 손 재구성 표기(NX-4). **지금 할 일 = 재정 T43 회수(결정 브리핑 · ① IO 결함 런 처분 = 재실측(추천) vs 원시 IO 일지 정확 재현 · ② 다음 단계 = v28 소수리 → 27차(추천) vs 자문 3회차 먼저 vs 27차 없이 실측) → 재정대로 v28 → 27차(`NY-*`).** Owner 결정 대기 1건.

> [정정 2026-09-06 · 69차] 68차의 「26차 도전 → PASS」는 REVISE 4 로 끝났고 T42 §2 재상신 요건이 충족돼 T43 을 상신했다.

**★ 09-06 68차 갱신 — M1b 25차 = REVISE 5(NW-1 BLOCKER · NW-2~5 HIGH · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v25.md` · `D-20260905-02` §17 추기 27 · 「T42 이후 재조립 방식 자체의 첫 REVISE」 · 재상신 기준 2연속 미달).** 설계 메모 **v27** · 구동기 **v8**(공용 `run_engine` · 선등록표 `registry()` · 도면 20 디렉터리 `figures-normalized-20/`) · 지표 **v27**(선등록 대응 NW-3 · 봉투 권한 NW-4 · 결함 N/A NW-2) · `t40_replay.py` **v2**(sandbox = 주 작업 트리 공유 클론 + 핀 커밋 linked worktree · 역할 토큰 `<RUN_REPO>`·`<MAIN>` · IO 결함 = traceback 호출 사슬 자리 주입 재현(면제 없음) · 소유 표식 NW-5) · `t40_receipts.py` **v2**(법 HEAD·파일 지문·run.yaml·traceback 지문) · 회귀표 **v7**(101 사례 = L 20 · C 77 · X 2 · S 2 · 픽스처 = 실측 §2 구조). **총괄 자기 발견: `figures-normalized/` 의 `MAPPING.md` 때문에 현재 엔진의 `source <r>` 가 exit 1 — 구동기 상수를 `figures-normalized-20/` 로.** **지금 할 일 = M1b 26차 도전(지적 `NX-*`) → PASS → 실측 착수.** 실측 절차 = 67차와 같고 `--sandbox` 는 **원본과 겹치지 않는 홈 fs 새 경로**(대조기가 소유 표식 없는 기존 디렉터리를 지우지 않는다).

> [정정 2026-09-06 · 68차] 67차의 「25차 도전 → PASS」는 REVISE 5 로 끝났다(→ v27). 67차의 「drive v7 · metrics v26 · replay v1 · receipts v1 · regress v6」는 낡은 판이다.

**★ 09-06 67차 갱신 — ⓓ 집행 완료(D-02 §17 추기 26): 설계 메모 v26 · 구동기 v7(호출별 영수증 `evidence/calls/` · `PYTHONHASHSEED=0`) · 지표 v26(재조립 오라클 + 전/후 검사) · `t40_replay.py` v1 · `t40_receipts.py` v1 · 회귀표 v6(88 사례 PASS · 약 7분).** **지금 할 일 = M1b 25차 도전(지적 `NW-*`) → PASS → 실측 착수.** 실측 절차 변경 = `read` 는 **`PYTHONHASHSEED=0 t40_drive.py read <r>`** · 지표 추출은 `t40_metrics.py <run_dir> --first-early evidence/first-early-<r>.json --receipts evidence/calls --run <r> --sandbox <홈 fs dir>`(재조립이 그 안에서 돈다) · 기준 런은 63차 명령 그대로. 스크립트 = `pd-lanes/t40-measure/`(drive v7 · metrics v26 · replay v1 · receipts v1 · regress v6 · excerpts v4 · workflow v4 · envelope v1).

> [정정 2026-09-06 · 67차] 66차의 「지금 할 일 = ⓓ 집행 ⑴~⑺」은 끝났다(25차 기동 직전).

**★ 09-06 66차 갱신 — 자문 2회차 회신 처분(D-02 §17 추기 25 · B-01~B-06 전부 수용) + 재정 T42(`ruling-20260906-02-T42.md` · Owner 육성 `T42: ① ⓓ` · 브리핑 `07e7b94e-…`).** **지금 할 일 = ⓓ 집행 순서대로**: ⑴ 메모 v26 §5 검증 약속을 여섯 부류로 좁혀 적기(B-04) ⑵ 구동기 `t40_drive.py` v7 — `read` 호출마다 `evidence/calls/<run>-<n>.json` 영수증(호출 전 대기 좌표의 응답 지문 · 호출 뒤 E/full/게이트/lane-log/포인터 지문 · 예외 종류·위치 · 첫 관측 S) ⑶ 재조립 대조기 `pd-lanes/t40-measure/t40_replay.py` — 대상 런의 입력(원천·run.yaml·기록 응답 원시 바이트·봉투)과 영수증으로 빈 sandbox 에서 `read.run` 을 호출 단위로 재실행 · 산출물 대조(정규화 허용 목록 = produced_at·recorded_at·절대 경로 대응만 · PYTHONHASHSEED 고정 · sandbox 원장) ⑷ 회귀표 v6 — 18 부모 재조립 재현 + 65 변형 거부 + FR-4·FA-2 짝 ⑸ 지표 v26 — early_loop_check·tail_chain_check·check_gate·축/소견 재도출을 재조립 결과로 대체 · 입력 진위·핀·외부 증거·계수·N/A 유지 ⑺ 관문 → 커밋 → 사본 재핀 → bundle → SPEC v25(`NW-*` · 25번째) → 25차 기동. 기준 런 B 는 현재 경로 유지.

> [정정 2026-09-06 · 66차] 65차의 「Owner 몫 = 봉투 → REPLY.md」는 끝났다(회신 17:5x · 처분 추기 25). 「v26 보류」도 T42 로 풀렸다.

**★ 09-06 65차 갱신 — M1b 24차 = REVISE 3(NV-1~3 · HIGH 1 = 첫 스냅샷을 후속 E 로 대체해도 수용 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v24.md` · `D-20260905-02` §17 추기 24) · 방식 전환: 자문 2회차 봉투 발행(Owner 육성 「멤돈다 싶으면 말해줘 · Astra pro도 있으니」 → 「지금 만들자」).** 루프 판독 = 맴돈다(13회 같은 컴포넌트 · 22차 수정 → 23차 오거부 → 23차 수정 → 24차 오거부 사슬). **지금 할 일 = ⑴ Owner 가 봉투(`~/projects/workspaces/advice/t40-metrics-closure-20260906/t40-metrics-closure-20260906-1742/PROMPT.md` + `bundle.zip`)를 ChatGPT 웹 astra pro 에 넣고 회신을 `REPLY.md` 에 저장 → 총괄이 봉투 대조·처분표(D-02 추기 25) ⑵ 처분에 따라 v26(후보 = 재실행 오라클: 대상 런의 입력만 빈 sandbox 로 복사해 `read.run` 을 실측 호출 단위로 재실행하고 산출물을 원본과 대조 — `t40_regress.py` v5 의 L 생성기가 그 기계) · 지표 v26 · 회귀표 v6 ⑶ M1b 25차 도전(지적 `NW-*`) → PASS → 실측 착수.** **v26 을 자문 전에 쓰지 않는다.** 메모는 v25 그대로(drafts · sha16 `b1372a1d863a742b`). 사본 `pd-m1b-t40` 은 `d711f25` 핀 · order v25 그대로.

> [정정 2026-09-06 · 65차] 64차의 「24차 도전 → PASS」는 REVISE 3 으로 끝났다. 64차 이하의 「지금 할 일 = 24차/25차 기동」은 자문 회신 뒤로 미룬다.

**★ 09-06 64차 갱신 — M1b 23차 = REVISE 4(NU-1~4 · MED 4 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v23.md` · `D-20260905-02` §17 추기 23).** 설계 메모 **v25** · 지표 v25(조기 루프를 실행별 발번·소비 순서·결함 블록으로 재구성 · 후속 기대 좌표 = 정본 분해 + plan_grounding · 그룹 기록 접두부 셋 · phase-gate 재도출 + 봉투 결속) · **회귀표 v5 = 발주 기록·스냅샷을 구동기 `t40_drive.py` 실제 함수로 수집 · L16(비대칭 재시도)·L17(접지 반향 거부) · 83 사례 PASS**(약 3분). **지금 할 일 = M1b 24차 도전(지적 `NV-*`) → PASS → 실측 착수.** 기준 런 추출 명령은 63차와 같다(v25 재현 = complete · 163 · 56).

> [정정 2026-09-06 · 64차] 63차의 「23차 도전 → PASS」는 REVISE 4 로 끝났다(→ v25). 63차 이하의 「지표 v24 · 회귀표 v4(75 사례)」는 낡은 판이다.

**★ 09-06 63차 갱신 — M1b 22차 = REVISE 5(NT-1~5 · MED 5 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v22.md` · `D-20260905-02` §17 추기 22).** 설계 메모 **v24** · 지표 v24(read.convergence 소견 재도출 · E/full 회차 등식 · 소비 사슬 · 양방향 법 핀 · **run_repo 와 법 트리 분리**) · **회귀표 v4 = 원천 + 빈 lanes 에서 러너를 실측 호출 단위로 반복 호출 · 대기 요청에만 공급 · 발주 기록·스냅샷은 호출 시점 수집**(75 사례 PASS · 약 3분 · `pd-lanes/t40-measure/t40_regress.py` · 픽스처는 홈 fs). **지금 할 일 = M1b 23차 도전(지적 `NU-*`) → PASS → 실측 착수.** 기준 런 추출 = `t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline --law-tree <ad4c6c3 트리>` — 트리는 `git archive ad4c6c3 engine reader contracts | tar -x -C <dir>` 사본으로 충분(v24 로 실행 재현 = complete · 163 · 56). 총괄 자기 발견: v23 까지 이 명령을 디스크에서 실행한 적이 없었다(원장 루트 오해석 exit 4 → v24 수정).

> [정정 2026-09-06 · 63차] 62차의 「22차 도전 → PASS」는 REVISE 5 로 끝났다(→ v24). 62차 이하의 「지표 v23 · 회귀표 v3(61 사례)」는 낡은 판이다.

**★ 09-06 62차 갱신 — M1b 21차 = REVISE 6(NS-1~6 · HIGH 1 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v21.md` · `D-20260905-02` §17 추기 21).** 설계 메모 **v23** · 지표 v23(판정서 내부 정합 · 회차 상한 · 포인터 필수 필드 · law-tree 내용 핀) · **회귀표 v3 = L 행을 실제 `read.run` 실행으로 생성**(61 사례 PASS · `pd-lanes/t40-measure/t40_regress.py` · 픽스처는 홈 fs · 회차당 ~10분). **지금 할 일 = M1b 22차 도전(지적 `NT-*`) → PASS → 실측 착수.** 기준 런 추출은 `--baseline --law-tree <t40-base 체크아웃(ad4c6c3)>` 로만(기준 런 자기 worktree d4e6ca2 는 엔진이 낡아 불가).

> [정정 2026-09-06 · 62차] 61차의 「21차 기동」은 끝났다(REVISE 6 → v23). 61차 문단의 `--law-tree .worktrees/gdm-…`(d4e6ca2) 문안은 **오류** — 그 트리의 엔진에는 종결 가드가 없다(NS-6). t40-base 체크아웃을 쓴다.

**★ 09-06 61차 갱신 — 결제 뒤 재기동한 M1b 20차 = REVISE 6(NR-1~6 · HIGH 2 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v20.md` · `D-20260905-02` §17 추기 20).** 설계 메모 **v22** · 지표 v22(`--law-tree` 신설 · 요청 MD 재렌더 결속 · memo_count 대조) · 회귀표 v2(55 사례 PASS · L 행을 러너 실제 경로로). **지금 할 일 = M1b 21차 도전 기동(사본 재핀 · order v22 · 지적 `NS-*`) → PASS → 실측 착수.** 실측 시 기준 런 추출은 `t40_metrics.py runs/gdm-… --baseline --law-tree .worktrees/gdm-wo2026128750a1-agent-memory`(d4e6ca2) 로.

> [정정 2026-09-06 · 61차] 60차의 「결제 통지 뒤 20차 재기동」은 끝났다(REVISE 6 → v22).

**★ 09-06 60차 갱신 — 자문 회신 처분 완료(`D-20260905-02` §17 추기 19 · NOT-READY · A-01~A-05 전부 수용) → 설계 메모 v21 · 지표 v21 · 회귀표 `pd-lanes/t40-measure/t40_regress.py`(44 사례 PASS · `T40-REGRESS-TABLE.md`).** **지금 할 일 = Owner 결제 통지(T41 ① B) 뒤 M1b 20차 도전 기동**(사본 재핀 · pin = `git rev-parse HEAD` · SPEC v20 파일을 메모 v21·회귀표 기준으로 갱신 · 지적 `NR-*` · 감시 = STATUS EXIT= + FINAL 바이트) → PASS → 실측 착수(39차 순서). 회귀표는 판이 바뀔 때마다 전건 재실행(`--src <리포> --work <홈 fs 디렉터리>` · tmpfs 금지).

> [정정 2026-09-06 · 60차] 59차의 「⑴ 자문 회신 처분」은 끝났다. 남은 것은 ⑵ 결제 통지 뒤 재기동.

**★ 09-06 59차 갱신 — 재정 T41 ① = B(크레딧 구매 · 좌석 유지 · `ruling-20260906-01-T41.md`).** Owner 질문 3건(경위·미해결·astra pro 자문)에 답하며 **자문 봉투 `~/projects/workspaces/advice/t40-metrics-statespace-20260906/`(ROUTING ⑽ ⓑ · 10차부터 충족됐던 트리거를 총괄이 미이행)** 를 발행. **지금 할 일 = ⑴ Owner 가 봉투를 ChatGPT 웹 astra pro 에 넣고 회신(REPLY.md)을 주면 처분 → 메모 v21 · 지표 v21 ⑵ Owner 결제 통지 뒤 20차 재기동(`astra-m1b-t40v20b/` · 같은 접두 `NR-*` · 메모 최신 판 · 감시 = STATUS EXIT= + FINAL 바이트) → PASS → 실측 착수.** 순서는 ⑴ 이 먼저 오면 ⑴→⑵, 결제가 먼저면 ⑵ 를 기다리지 않고 기동해도 되되 회신이 오면 다음 회차에 반입.

> [정정 2026-09-06 · 59차] 58차의 「Owner 재정 대기 1건」은 ① 이 닫혔다. ② 는 총괄 원안(A) 집행.

**★ 09-06 58차 갱신 — M1b 20차 기동(10:50 · SPEC v20 · `NR-*` · 사본 `b692b16`)이 Codex 계정 사용량 한도로 죽었다(FINAL 0 B · STATUS EXIT=1 · EV 「You've hit your usage limit … try again at Sep 12th, 2026 10:38 PM」 · 레인 `pd-lanes/astra-m1b-t40v20/`). 판정 없음 → 감수 원문 파일 없음 · 총괄 오류 누계 불변(134).** 한도는 계정 단위 → gpt-6-astra(M1b) · gpt-5.6-sol(M3 · M1b 폴백) 좌석 전부 09-12 22:38 까지 불가. **Owner 재정 대기 1건 = T41(좌석 한도 대응: 대기 / 크레딧 구매 / 임시 좌석 대체) — 결정 브리핑 발행(drafts `OWNER-BRIEF-T41-codex-quota.html` · URL 은 기억 `patent-docent-project`).** 재정 전까지 **착수 금지**(ROUTING A2 · PASS 전 실측 금지 · ⑽ 유비 「쿼터 시 자체 판단 진행 금지」). 좌석이 돌아오면 = **같은 SPEC v20 · 같은 사본 핀 `b692b16` 으로 20차 재기동**(새 레인 디렉터리 `astra-m1b-t40v20b/` · 감시는 `STATUS` `EXIT=` + `FINAL` 바이트 · LANE-RUNTIME 함정 O). 총괄 자기 오류(지적 밖): Monitor 가 호출자 `RUN_RC=` 만 보고 `EXIT=1` 을 놓쳤다 → 함정 O 로 성문화(agents 커밋).

> [정정 2026-09-06 · 58차] 아래 57차 문단의 「지금 할 일 = M1b 20차 도전 기동」은 **기동했으나 한도로 무산**. 재정 T41 뒤 재기동.

**★ 09-06 57차 갱신 — M1b 19차 = REVISE 3(NQ-1~3 · MED · 거부 행 오거부 · 종결 근거 셋 중 원장 누락 · violations↔findings 미대조 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v19.md` · `D-20260905-02` §17 추기 18).** 설계 메모 **v20**(drafts `T40-MEASURE-DESIGN.md` · v19 = `.v19.md`) + 지표 v20. **지금 할 일 = M1b 20차 도전 기동(사본 재핀 · pin = `git rev-parse HEAD` · 지적 `NR-*`) → PASS → 실측 착수(39차 순서).** 규약은 54차 이하 그대로.

> [정정 2026-09-06 · 57차] 아래 56차 문단의 「지금 할 일 = M1b 19차 도전 기동」은 **끝났다**(REVISE 3 → v20). 경위 보존용으로 남긴다.

**★ 09-06 56차 갱신 — M1b 18차 = REVISE 3(NP-1~3 · MED · 검증 조건이 실패 여부·ok·포인터에 걸린 자리 셋 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v18.md` · `D-20260905-02` §17 추기 17).** 설계 메모 **v19**(drafts `T40-MEASURE-DESIGN.md` · v18 = `.v18.md`) + 지표 v19(실행 경로별 기대 다중집합 · 소비 행 = 응답 흔적 · 종결 = 포인터 → 완주 판정서). **지금 할 일 = M1b 19차 도전 기동(사본 재핀 · pin 은 `git rev-parse HEAD` · 지적 `NQ-*`) → PASS → 실측 착수(39차 순서).** 규약은 54차 이하 그대로.

> [정정 2026-09-06 · 56차] 아래 55차 문단의 「지금 할 일 = M1b 18차 도전 기동」은 **끝났다**(REVISE 3 → v19). 경위 보존용으로 남긴다.

**★ 09-06 55차 갱신 — M1b 17차 = REVISE 4(NO-1~4 · MED · v17 재작성의 오거부·ND-2 회귀 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v17.md` · `D-20260905-02` §17 추기 16).** 설계 메모 **v18**(drafts `T40-MEASURE-DESIGN.md` · v17 = `.v17.md`) + 지표 v18(상태 4종 complete/in-progress/terminated-failure/terminated-incomplete · 손상 exit 4 · 전 상태 공통 검사). **지금 할 일 = M1b 18차 도전 기동(사본 재핀 · 지적 `NP-*`) → PASS → 실측 착수(39차 순서).** 규약은 54차 이하 그대로.

> [정정 2026-09-06 · 55차] 아래 54차 문단의 「지금 할 일 = M1b 17차 도전 기동」은 **끝났다**(REVISE 4 → v18). 경위 보존용으로 남긴다.

**★ 09-06 54차 갱신 — M1b 16차 = REVISE 4(NN-1~4 · MED · NN-3 = v16 이 합법적 대기·실패 자료를 오거부 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v16.md` · `D-20260905-02` §17 추기 15).** 설계 메모 **v17**(drafts `T40-MEASURE-DESIGN.md` · v16 = `.v16.md`) + **지표 v17 = 런 상태 인식 재설계**(complete / awaiting / terminated-failure · 완전성 요건은 complete 만). **지금 할 일 = M1b 17차 도전 기동(사본 재핀 · 지적 `NO-*`) → PASS → 실측 착수(39차 순서).** 규약은 53차 이하 그대로.

> [정정 2026-09-06 · 54차] 아래 53차 문단의 「지금 할 일 = M1b 16차 도전 기동」은 **끝났다**(REVISE 4 → v17). 경위 보존용으로 남긴다.

**★ 09-06 53차 갱신 — M1b 15차 = REVISE 2(NM-1~2 · MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v15.md` · `D-20260905-02` §17 추기 14).** 설계 메모 **v16**(drafts `T40-MEASURE-DESIGN.md` · v15 = `.v15.md`) + 지표 v16(검사 id 집합 전건 · lane-log 엔진 검사 재실행 · dispatch 양방향 · 원천 1회 읽기). **지금 할 일 = M1b 16차 도전 기동(사본 재핀 · 지적 `NN-*`) → PASS → 실측 착수(39차 순서).** 규약은 52차 이하 그대로.

> [정정 2026-09-06 · 53차] 아래 52차 문단의 「지금 할 일 = M1b 15차 도전 기동」은 **끝났다**(REVISE 2 → v16). 경위 보존용으로 남긴다.

**★ 09-06 52차 갱신 — M1b 14차 = REVISE 1(NL-1 · MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v14.md` · `D-20260905-02` §17 추기 13).** 설계 메모 **v15**(drafts `T40-MEASURE-DESIGN.md` · v14 = `.v14.md`) + 지표 v15(명세에 READ 검사 재실행 · 판정서 기록과 대조). **지금 할 일 = M1b 15차 도전 기동(사본 재핀 · 지적 `NM-*`) → PASS → 실측 착수(39차 순서).** 규약은 51차 이하 그대로.

> [정정 2026-09-06 · 52차] 아래 51차 문단의 「지금 할 일 = M1b 14차 도전 기동」은 **끝났다**(REVISE 1 → v15). 경위 보존용으로 남긴다.

**★ 09-06 51차 갱신 — M1b 13차 = REVISE 1(NK-1 · MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v13.md` · `D-20260905-02` §17 추기 12).** 설계 메모 **v14**(drafts `T40-MEASURE-DESIGN.md` · v13 = `.v13.md`) + 지표 v14(명세·판정서 계약 스키마 전체 검증). **지금 할 일 = M1b 14차 도전 기동(사본 재핀 · 지적 `NL-*`) → PASS → 실측 착수(39차 순서).** 규약은 50차 이하 그대로.

> [정정 2026-09-06 · 51차] 아래 50차 문단의 「지금 할 일 = M1b 13차 도전 기동」은 **끝났다**(REVISE 1 → v14). 경위 보존용으로 남긴다.

**★ 09-06 50차 갱신 — M1b 12차 = REVISE 1(NJ-1 · MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v12.md` · `D-20260905-02` §17 추기 11).** 설계 메모 **v13**(drafts `T40-MEASURE-DESIGN.md` · v12 = `.v12.md`) + 지표 v13(patent.md 부재 = exit 4). **지금 할 일 = M1b 13차 도전 기동(사본 재핀 · 지적 `NK-*`) → PASS → 실측 착수(39차 순서).** 규약은 49차 이하 그대로.

> [정정 2026-09-06 · 50차] 아래 49차 문단의 「지금 할 일 = M1b 12차 도전 기동」은 **끝났다**(REVISE 1 → v13). 경위 보존용으로 남긴다.

**★ 09-06 49차 갱신 — M1b 11차 = REVISE 2(NI-1~2 · MED · 특별 요청 「[가설] 등재 후 착수」 = 불가 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v11.md` · `D-20260905-02` §17 추기 10).** 설계 메모 **v12**(drafts `T40-MEASURE-DESIGN.md` · v11 = `.v11.md`) + 지표 v12(요청 MD 지문 재계산 · dispatch 대조 · 원천 지문 사슬). **지금 할 일 = M1b 12차 도전 기동(사본 재핀 · 지적 `NJ-*`) → PASS → 실측 착수(39차 순서).** Owner 질문(가설 등재)은 철회. 규약은 48차 이하 그대로.

> [정정 2026-09-06 · 49차] 아래 48차 문단의 「지금 할 일 = M1b 11차 도전 기동」은 **끝났다**(REVISE 2 → v12). 경위 보존용으로 남긴다.

**★ 09-06 48차 갱신 — M1b 10차 = REVISE 2(NH-1~2 · MED · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v10.md` · `D-20260905-02` §17 추기 9).** 설계 메모 **v11**(drafts `T40-MEASURE-DESIGN.md` · v10 = `.v10.md`) + 지표 v11(입력 결속 사슬 · `--baseline` 한정). **지금 할 일 = M1b 11차 도전 기동(사본 재핀 · 지적 `NI-*`) → PASS → 실측 착수(39차 순서) · PASS 아니면 Owner 에게 「추출기 방어 잔여 [가설] 등재 후 착수」 여부 질문(채팅 · 결정 하나).** 규약은 47차 이하 그대로.

> [정정 2026-09-06 · 48차] 아래 47차 문단의 「지금 할 일 = M1b 10차 도전 기동」은 **끝났다**(REVISE 2 → v11). 경위 보존용으로 남긴다.

**★ 09-06 47차 갱신 — M1b 9차 = REVISE 2(NG-1 MED · NG-2 LOW · 이전 40건 전건 closed · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v9.md` · `D-20260905-02` §17 추기 8).** 설계 메모 **v10**(drafts `T40-MEASURE-DESIGN.md` · v9 = `.v9.md`) + 지표 v10(명세 run_id 대조 · lane-log 소속). **지금 할 일 = M1b 10차 도전 기동(사본 재핀 · 지적 `NH-*`) → PASS → 실측 착수(39차 순서).** 규약은 46차 이하 그대로.

> [정정 2026-09-06 · 47차] 아래 46차 문단의 「지금 할 일 = M1b 9차 도전 기동」은 **끝났다**(REVISE 2 → v10). 경위 보존용으로 남긴다.

**★ 09-06 46차 갱신 — M1b 8차 = REVISE 1(NF-1 · MED · 이전 39건 전건 closed · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v8.md` · `D-20260905-02` §17 추기 7).** 설계 메모 **v9**(drafts `T40-MEASURE-DESIGN.md` · v8 = `.v8.md`) + 지표 v9(완주 판정서 run_id 대조). **지금 할 일 = M1b 9차 도전 기동(사본 재핀 · 지적 `NG-*`) → PASS → 실측 착수(39차 순서).** 규약은 45차 이하 그대로.

> [정정 2026-09-06 · 46차] 아래 45차 문단의 「지금 할 일 = M1b 8차 도전 기동」은 **끝났다**(REVISE 1 → v9). 경위 보존용으로 남긴다.

**★ 09-06 45차 갱신 — M1b 7차 = REVISE 2(NE-1~2 · MED 만 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v7.md` · `D-20260905-02` §17 추기 6).** 설계 메모 **v8**(drafts `T40-MEASURE-DESIGN.md` · v7 = `.v7.md`) + 지표 v8(완주 판정서 = 같은 검증기 · findings = jsonschema `$defs/finding`). **지금 할 일 = M1b 8차 도전 기동(사본 재핀 · 지적 `NF-*`) → PASS → 실측 착수(39차 순서).** 규약은 44차 이하 그대로.

> [정정 2026-09-06 · 45차] 아래 44차 문단의 「지금 할 일 = M1b 7차 도전 기동」은 **끝났다**(REVISE 2 → v8). 경위 보존용으로 남긴다.

**★ 09-06 44차 갱신 — M1b 6차 = REVISE 2(ND-1~2 · MED 만 · B·C·E·F PASS · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v6.md` · `D-20260905-02` §17 추기 5).** 설계 메모 **v7**(drafts `T40-MEASURE-DESIGN.md` · v6 = `.v6.md`) + 지표 v7(findings 형태 검증 · synthesize 응답 단일 바이트 읽기). **지금 할 일 = M1b 7차 도전 기동(사본 재핀 · 지적 `NE-*`) → PASS → 실측 착수(39차 순서).** 규약은 43차 이하 그대로.

> [정정 2026-09-06 · 44차] 아래 43차 문단의 「지금 할 일 = M1b 6차 도전 기동」은 **끝났다**(REVISE 2 → v7). 경위 보존용으로 남긴다.

**★ 09-06 43차 갱신 — M1b 5차 = REVISE 3(NC-1~3 · MED 만 · open 0 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v5.md` · `D-20260905-02` §17 추기 4).** 설계 메모 **v6**(drafts `T40-MEASURE-DESIGN.md` · v5 = `.v5.md`) + 구동·지표 v6(enter 의 SystemExit 도 14 · 스냅샷 단일 읽기 · bool/범위 검사). **지금 할 일 = M1b 6차 도전 기동(사본 재핀 · 지적 `ND-*` · bundle 에 v1~v5 동봉) → PASS → 실측 착수(39차 순서).** 규약은 42차 이하 그대로.

> [정정 2026-09-06 · 43차] 아래 42차 문단의 「지금 할 일 = M1b 5차 도전 기동」은 **끝났다**(REVISE 3 → v6). 경위 보존용으로 남긴다.

**★ 09-06 42차 갱신 — M1b 4차 = REVISE 3(NB-1~3 · HIGH 1 · 전부 수용 · open 0 · B·E·F PASS · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v4.md` · `D-20260905-02` §17 추기 3).** 설계 메모 **v5**(drafts `T40-MEASURE-DESIGN.md` · v4 = `.v4.md`) + 구동·지표 v5(예외 경계에 `enter` 포함·증거 기록 실패 = 14 고정 · dispatch 전건 검사 뒤 기록 · 스냅샷 형태 검증 한 exit 4 경계). **지금 할 일 = M1b 5차 도전 기동(사본 재핀 · 지적 `NC-*` — 발주문의 ID 접두를 기동 전에 확인) → PASS → 실측 착수(39차 순서).** 규약은 41차 이하 그대로.

> [정정 2026-09-06 · 42차] 아래 41차 문단의 「지금 할 일 = M1b 4차 도전 기동」은 **끝났다**(REVISE 3 → v5). 경위 보존용으로 남긴다.

**★ 09-06 41차 갱신 — M1b 3차 = REVISE 7(NA-1~7 · BLOCKER 0 · HIGH 3 · 전부 수용 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v3.md` · `D-20260905-02` §17 추기 2).** 설계 메모 **v4**(drafts `T40-MEASURE-DESIGN.md` · v3 = `.v3.md`) + 스크립트 v4(구동: `lanes` 무변경 조회 / `dispatch <r> <batch>` 발주 확정 · 단일 예외 경계 · 지표: 마지막 synthesize 시도 = 디스크 좌표 · 6축 집합 검사 · 발췌 2: 판정 불가 → ② 보류 · Workflow: 요청/응답 교차·좌표 결속 거부). **지금 할 일 = M1b 4차 도전 기동(사본 재핀 · 지적 `NB-*`) → PASS → 실측 착수(39차 순서 · 배치 발주는 `t40_drive.py dispatch <r> <batch>` · 완료 확인은 `lanes <r>`).** 규약은 40차 이하 그대로.

> [정정 2026-09-06 · 41차] 아래 40차 문단의 「지금 할 일 = M1b 3차 도전 기동」은 **끝났다**(REVISE 7 → v4). 경위 보존용으로 남긴다.

**★ 09-06 40차 갱신 — M1b 2차 = REVISE 9(MZ-1~9 · BLOCKER 1 = 짝짓기 실패의 자동 열위 계수 + 27 분모 변경 · 전부 수용 · `docs/lessons/2026-09-06-astra-m1b-t40-measure-v2.md` · `D-20260905-02` §17 추기).** 설계 메모 **v3**(drafts `T40-MEASURE-DESIGN.md` · v2 = `.v2.md`) + 스크립트 v3(구동 exit 0/10/11/12/13/14/15 · dispatch_id · `--first-early` 필수 · 발췌 1 = 기준 런 27 단위 고정 · Owner 명시 판정). **지금 할 일 = M1b 3차 도전 기동(사본 `pd-m1b-t40` 재핀 · 지적 `NA-*`) → PASS → 실측 착수(39차 문단의 순서 그대로 · 배치는 `t40_drive.py lanes <r> <batch>` 가 dispatch_id 를 부여).** 규약은 39차 이하 그대로.

> [정정 2026-09-06 · 40차] 아래 39차 문단의 「지금 할 일 = M1b 2차 도전 기동」은 **끝났다**(REVISE 9 → v3). 경위 보존용으로 남긴다.

**★ 09-06 39차 갱신 — T40 ④ A 비교 실측 착수 국면.** 재정 **T40 ⑤**(Owner 육성 `T40 ④ 봉투 대행 승인` · `ruling-20260905-05-T40.md` §5 · `6d92cad`) = 실측 3 런의 조기 수렴 escalation-trigger 축 미달에만 총괄이 '계속' 봉투 대행. 실측 설계 메모 = drafts `T40-MEASURE-DESIGN.md`(**v2** · v1 = `.v1.md`) · **M1b 1차 = REVISE 13(MY-1~13 · BLOCKER 1 = 27항목 대응표 부재 · 전부 수용 · `docs/lessons/2026-09-06-astra-m1b-t40-measure.md` · `D-20260905-02` **§17**)**. 계측 브랜치(main 무접촉 · 병합 금지) = **`t40-base` `ad4c6c3`**(main + `reader/procedure/` 를 09-01 핀 `d4e6ca2` 판으로 — 재정 §4 「같은 절차 문서」 이행) · `t40-r1` `530b096`(decompose·synthesize xhigh) · `t40-r2` `00e0bed`(ground-dependent sonnet-5/high). 스크립트 = `~/projects/workspaces/pd-lanes/t40-measure/`(`t40_drive.py` 종료 코드 0/10/11/12/13/14 · `t40_lanes.workflow.js` · `t40_metrics.py` · `t40_excerpts.py` · `t40_envelope.py` · 기준 런 자체 시험 통과). **지금 할 일 = M1b 2차 도전 기동(사본 `pd-m1b-t40` 재핀 · 지적 `MZ-*`) → PASS → `git worktree add --detach .worktrees/gdm-wo2026128750a1-t40-r{0,1,2} <핀>` → `t40_drive.py source r0|r1|r2` → `read` → 배치 A-a(read-a ×3 · Workflow `scriptPath` + args lanes) → 첫 배치 transcript model 검증 → A-b → (exit 11 이면 `t40_envelope.py --quote 'T40 ④ 봉투 대행 승인' --located-at 'ruling-20260905-05-T40.md §5' --write`) → B → C → `t40_metrics.py --first-early` → 결과 표 D-02 §18 + 발췌 2건(`t40_excerpts.py`) → Owner ①② 재정(한 줄 또는 새 브리핑) → M2b-3.** 규약은 38차 이하 그대로(관문 뒤 별도 커밋 · `docs/` 만 커밋 · 레인 산출은 홈 fs).

> [정정 2026-09-06 · 39차] 아래 38차 문단의 「지금 할 일 = T40 ④ A 비교 실측 착수」는 **설계·1차 도전까지 진행됐다**(§17). 경위 보존용으로 남긴다.

**★ 09-06 38차 갱신 — PD-M2b 합본 감사(fable xhigh · M9 4회째) = PASS · LOW 6(RL-1~6) → PD-M2b 집행분 감사상 종결**(`docs/lessons/2026-09-06-fable-audit-round-m2b.md` · `D-20260905-02` **§16** · DISPOSITIONS 278행(45차 · RL-2 로 §0 계수를 실물 60/12/72 로 정정 · RL-3 로 「행 수 = 데이터 행만」)). 감사 세션 사고 1 = 감사자가 pytest 를 배경으로 띄우고 「기다리겠다」로 응답 → 단발 모드 종료 → `--resume` 재접속으로 판정 회수(**LANE-RUNTIME 함정 N** · 안내문 정본 drafts `fable-audit-brief-header.md`). 처분: RL-1~3 기록 정정(이 커밋) · RL-4 발주문 문언 · RL-5(conftest 원본 보관 우회)·RL-6(`lane_file` name) **이월 → 다음 코드 라운드**. **지금 할 일 = T40 ④ A 비교 실측 착수**(재정 `ruling-20260905-05-T40.md` §4 · 소재 WO2026-128750 · 계측 브랜치에 계약 값만 다른 커밋 셋(main 무접촉) · R0 현행 좌석 재런(잡음 폭) · R1 decompose·synthesize `opus-5/xhigh` · R2 ground-dependent `sonnet-5/high` · 레인 = Workflow `{model, effort}` 하드 지정 · `run_kind: partial` · 임계 선등록 = §4 ① ② · 기준 = 09-01 런 `runs/gdm-wo2026128750a1-agent-memory`(engine `d4e6ca2`) · 결과 표 + Owner 발췌 2건 → ①② 재정(한 줄 회신 또는 새 브리핑) → M2b-3 좌석 값 커밋(+ RL-5·6 이월분)). 실측 설계는 새 국면이라 **압축 뒤 ROUTING §5 재독 · 발주문 §0′ 증명표 형식 · Workflow model 하드 지정**(기억 `workflow-model-inherit-trap`)부터. 규약은 37차 이하 그대로.

> [정정 2026-09-06 · 38차] 아래 37차 문단의 「지금 할 일 = 감사 회수」는 **끝났다**(PASS · §16). 경위 보존용으로 남긴다.

**★ 09-06 37차 갱신 — 합본 감사 발주문 M1b 도전 = REVISE 9(MX-1~9 · HIGH 1 = 레인 diff 는 축약본 · 전부 수용 · `D-20260905-02` §15) → v2 → 재도전 없이 fable xhigh 감사 발주.** 사본 `~/projects/workspaces/pd-audit-round-m2b`(재핀 = 이 기록 커밋) · 레인 `pd-lanes/fable-audit-round-m2b/`(brief.md · runner.sh · `setsid nohup` · Monitor `EXIT=`) · basetemp `pd-audit12-basetemp` · 지적 `RL-*`. **지금 할 일 = 감사 회수**(`status` `EXIT=` → `out.txt`·`usage.json` → 원문 `docs/lessons/2026-09-06-fable-audit-round-m2b.md` 규율 10 보존 → DISPOSITIONS → D-02 §16 처분 → FAIL 이면 수리 라운드(sol-coder · M1b) · PASS 면 **T40 ④ A 비교 실측 착수**(계측 브랜치 · R0/R1/R2 · Workflow · `run_kind: partial`)). 규약은 36차 이하 그대로.

> [정정 2026-09-06 · 37차] 아래 36차 문단의 「지금 할 일 = fable xhigh 합본 감사(M1b 도전 →)」 중 M1b 도전은 **끝났다**(REVISE 9 → v2). 경위 보존용으로 남긴다.

**★ 09-06 36차 갱신 — 라운드 M2b-1 병합 `1bf24f1`**(sol-coder PASS · 총괄 재현 909/909 두 모드 · 관문 7종 · docstring 3검사 · `D-20260905-02` **§14**). PD-M2b 집행분 = G-4 `partial` · B-2 `lane_id` · 백로그 ⑼(세 층 = `tests/ledger_guard.py` 허용 목록 관문 + 헬퍼 결속 + `conftest.py` 세션 거부) **전부 병합**. 남은 것 = G-1~G-3 좌석(T40 ①② · ④ A 비교 실측 뒤) · G-12(재정 필요) · 자문 ⓑ(이연). **지금 할 일 = fable xhigh 합본 감사**(drafts `AUDIT-ORDER-round-m2b.md` 자리표 채움 → M1b astra high 도전(사본 `pd-m1b-m2b2` 재핀 · 지적 `MX-*`) → 격리 사본 `~/projects/workspaces/pd-audit-round-m2b`(`git clone --no-hardlinks` · 기록 커밋 detached · `.audit-sandbox`) · 레인 `pd-lanes/fable-audit-round-m2b/`(brief.md · runner = drafts `fable-audit-runner.template.sh`) · basetemp `pd-audit12-basetemp` · `setsid nohup` · Monitor · 지적 `RL-*` → 처분 → T40 ④ A 비교 실측). 규약은 35차 이하 그대로.

> [정정 2026-09-06 · 36차] 아래 35차 문단의 「지금 할 일 = sol-coder M2b-1」은 **끝났다**(병합). 경위 보존용으로 남긴다.

**★ 09-06 35차 갱신 — 라운드 M2b-2 병합 `b0c4fb6`**(sol-coder PASS + 후속 소발주 · 총괄 재현 885/885 두 모드 · 관문 7종 · `D-20260905-02` **§13**). 실물: `run_kind` 3종 + `source.run` 진입 가드(`partial_until`) · `lane_id` 형태+소속+루트 포함(`lane_dir`·`lane_file`) · SPEC B-2·G-4 집행 마커 · **G-12 신설**(종료선·비게시 강제 미구현 · 승격 정책 = 재정 필요 · 백로그). 환경 사고 2: 하니스 배경 Bash 가 메모리 부족으로 죽음(→ 재현도 `setsid nohup`) · 후속 레인이 basetemp 를 `/tmp` 로 옮겨 tmpfs 포화(→ 발주문 문언 「임시물을 `/tmp` 로 옮기지 않는다」 · LANE-RUNTIME 후보). **지금 할 일 = sol-coder M2b-1(v6 · worktree `round-m2b1` · 이 기록 커밋 분기 · 레인 `pd-lanes/sol-coder-round-m2b1/`) → 회수 → 총괄 재현(`setsid nohup` · 두 모드 순차) → 커밋·rebase → 리포 루트 cwd ff 병합 → 기록 → fable xhigh 합본 감사(M2b-1+M2b-2 · 사본 `pd-audit-round-m2b` · basetemp `pd-audit12-basetemp`) → T40 ④ A 비교 실측.** 규약은 34차 이하 그대로.

> [정정 2026-09-06 · 35차] 아래 34차 문단의 「지금 할 일 = sol-coder M2b-2 회수」는 **끝났다**(병합 `b0c4fb6`). 경위 보존용으로 남긴다.

**★ 09-06 34차 갱신 — M2b-1 M1b 4차 = REVISE MED 4(MV-1~4 · 대조표 문언·배치 · 값 공간 상신 0) → v6 → 5차 없이 sol-coder 발주 결정(`D-20260905-02` §12 · M2a-2 선례).** 원문 `docs/lessons/2026-09-06-astra-m1b-m2b1v4.md` · DISPOSITIONS 264행(43차). **기동은 M2b-2 sol-coder 레인(`pd-lanes/sol-coder-round-m2b2/` · 01:15 기동) EXIT 뒤** — 전체 pytest 동시 금지. 절차 = M2b-2 회수·재현·병합 → `git worktree add .worktrees/round-m2b1 -b round-m2b1 HEAD`(리포 루트 cwd) → drafts `SPEC-round-m2b1.md`(v6) 의 분기 줄에 HEAD 기재 → `pd-lanes/sol-coder-round-m2b1/SPEC-round-m2b1.md` 로 복사 → `runner.sh` 기동 → Monitor → 회수 → 재현 → 병합 → fable xhigh 합본 감사. **지금 할 일 = sol-coder M2b-2 회수.** 규약은 33차 이하 그대로.

> [정정 2026-09-06 · 34차] 아래 33차 문단의 「M2b-1 은 4차 도전 회수 뒤」는 **회수됐다**(MED 4 → v6 → 집행 결정). 경위 보존용으로 남긴다.

**★ 09-06 33차 갱신 — M2b-2 M1b 4차 = REVISE LOW 3(MW-1~3 · 문언만 · 값 공간 상신 0) → v6 → 5차 없이 sol-coder 발주(M2a-1 선례 · `D-20260905-02` §11).** 원문 `docs/lessons/2026-09-06-astra-m1b-m2b2v4.md` · DISPOSITIONS 260행(42차). **순서 변경**: M2b-2 sol-coder 를 먼저(worktree `round-m2b2` · 레인 `pd-lanes/sol-coder-round-m2b2/` · 발주문 v6 = drafts `SPEC-round-m2b2.md`) · M2b-1 은 4차 도전(`pd-lanes/astra-m1b-m2b1v4/` · 지적 `MV-*`) 회수 뒤 — **두 레인의 전체 pytest 는 동시에 돌리지 않는다**(M2b-1 sol-coder 는 M2b-2 레인 EXIT 뒤 기동). **지금 할 일 = sol-coder M2b-2 회수(`status` `EXIT=` · `final.txt`) → 총괄 재현(전체 두 모드 순차 · §2 대조표 직접) → worktree 커밋 · rebase → 리포 루트 cwd 에서 ff 병합 · worktree 제거 → 기록 → M2b-1 4차 회수·처분 → (PASS/LOW 면) sol-coder M2b-1 → 같은 절차 → fable xhigh 감사(합본).** 규약은 32차 이하 그대로.

> [정정 2026-09-06 · 33차] 아래 32차 문단의 「지금 할 일 = 두 발주문 v5 → M1b 4차」는 **끝났다**(M2b-2 = LOW 3 → 집행 · M2b-1 = 회수 대기). 경위 보존용으로 남긴다.

**★ 09-06 32차 갱신 — M1b 3차 두 도전 = 둘 다 REVISE 5(M2b-1 MT-1~5 · M2b-2 MU-1~5 · 기각 0 · 값 공간 상신 필요 0).** 원문 `docs/lessons/2026-09-06-astra-m1b-m2b1v3.md`·`-m2b2v3.md` · 처분 `D-20260905-02` **§10** · DISPOSITIONS 257행(41차). 끊긴 지점 = 자문 처분을 발주문으로 옮긴 자리(잔존 5 · 신규 5): **MT-1** 세션 픽스처는 수집 뒤 설치 → 감싸기를 `pytest_sessionstart` 에서 · **MU-1** 「PermissionError 부재 = 열지 않음」 불성립(구 코드 `except OSError` 흡수) → `_bare_sha256_file` 호출 계수 · **MU-2** V6 제거해도 V7 이 로그 ⑶ 을 잡음 → 토큰 변화로 검출 · **MT-3·MU-3** 대조표에 관측 열과 시험 판정 열 분리 · MT-2(사유 토큰) · MT-4(exit 5 · 프로브 재설치) · MT-5(②③ 개별 제거) · MU-4(grep) · MU-5(m16 사실). **지금 할 일 = 두 발주문 v5 → M1b 4차(지적 `MV-*`/`MW-*` · 레인 `pd-lanes/astra-m1b-m2b1v4/`·`-m2b2v4/` · 사본 재핀 = 이 기록 커밋) → PASS → sol-coder M2b-1 → 재현 → 병합 → M2b-2 → fable xhigh 감사.** 규약은 31차 이하 그대로.

> [정정 2026-09-06 · 32차] 아래 31차 문단의 「지금 할 일 = 두 발주문 v4 저작 → M1b 3차」는 **끝났다**(둘 다 REVISE 5 → §10). 경위 보존용으로 남긴다.

**★ 09-06 31차 갱신 — 자문 회신 접수 · 처분 완료(NOT-READY · 8건 전부 수용 · 재정 사항 0).** 원문 = `docs/lessons/2026-09-06-astra-advice-m2b-gate-and-values.md`(봉투 `~/projects/workspaces/advice/m2b-gate-and-values-20260905-2357/REPLY.md` · ENVELOPE sha 일치) · 처분 = `docs/decisions/D-20260905-02-pdm2b-seats.md` **§9**(질문 ⓐ~ⓗ 답·처분 표 + 지적별) · DISPOSITIONS 247행(40차). **끊긴 지점**: M2b-1 = 정적 규칙을 **즉시 평가 (부모, 필드) 닫힌 허용 목록**으로(A-01) · 헬퍼에 호출 대상 결속(`read_stage.shadow_screening_ledger` 감싸기 · A-02) · 원장 경로 realpath/samefile 을 쓰기 전에(A-03) · **시험 전용 두 층 = `tests/conftest.py` `pytest_sessionstart` 정적 관문 + 세션 autouse `append_screening_ledger` 생산 거부**(A-04 · 함수는 `tests/ledger_guard.py`) · 헬퍼 음성 9칸(A-05). M2b-2 = `read_run`·`task` **소속 검사**(B-01 · `READ_RUNS`·`LANE_TASKS` 상수 + 다리 시험) · **`lane_file`** 말단 경로 포함(B-02 · 5 호출 자리) · 종료선·비게시 강제 미구현 = SPEC §8.4 **G-12** 백로그 등재. 절차 = 두 발주문에 **§0′ 변경별 증명표**(C-01) · §2 대조 = 완성본 기준 최소 변조(ⓖ). 엔진 동적 강제(ⓑ)는 **이연**(시험 전용 층이 부족하다고 확인될 때 Owner 재정). **지금 할 일 = 두 발주문 v4 저작(drafts `SPEC-round-m2b1.md`·`SPEC-round-m2b2.md` · v3 는 `.v3.md`) → M1b 3차 각각(사본 재핀 = 이 기록 커밋 · 지적 `MT-*`/`MU-*` · 레인 `pd-lanes/astra-m1b-m2b1v3/`·`astra-m1b-m2b2v3/`) → PASS → sol-coder M2b-1(worktree `round-m2b1` · 이 기록 커밋 분기) → 재현 → 병합 → M2b-2 → fable xhigh 감사.** 좌석·자문·킵얼라이브 규약은 30차 이하 그대로.

> [정정 2026-09-06 · 31차] 아래 30차 문단의 「지금 할 일 = 회신 대기」는 **끝났다**(회신 접수 · §9 처분). 경위 보존용으로 남긴다.

**★ 09-05 30차 갱신 — PD-M2b 착수.** 둘로 갈랐다: ⑴ **재정 불요분 = 소라운드 M2b-1**(백로그 ⑼ 정적 관문 강화 + T39 ② docstring · 발주문 drafts `SPEC-round-m2b1.md` v1 · **M1b astra high 도전 1차 기동 22:45** · 사본 `~/projects/workspaces/pd-m1b-m2b1` · 레인 `pd-lanes/astra-m1b-m2b1/` · 지적 `MP-*`) ⑵ **재정 필요분 = T40 상신**(`docs/decisions/D-20260905-02-pdm2b-seats.md` · 브리핑 아티팩트 **`a5a6d27f-e7ce-445f-a8ef-0b1485bdc1c1`** · drafts `OWNER-BRIEF-T40-m2b-seats.html` · 회신 서식 `T40: ① A / ② A / ③ A` = ① G-1·G-2 `opus-5/xhigh` ② G-3 `sonnet-5/high` ③ G-4 `partial` 추가+enum 강제 · 자잘 ⓐ~ⓓ · RULINGS-LEDGER §3 등재 · **Owner 결정 대기 1건**). **[추기 23:1x · 재정 T40 부분] Owner 육성 → `ruling-20260905-05-T40.md`: ③ G-4 = A(`partial` + enum 강제 · M2b-2 집행) · ①② 좌석 = 비교 실측(max↔xhigh · low↔sonnet high) 뒤 재정 → **④ A 채택(23:1x · 원장 §4 · 3 런 R0/R1/R2 · Workflow 하드 지정 · 임계 선등록) · Owner 결정 대기 0.** 순서 변경: M2b-2 = G-4 + enum + B-2(좌석 무관) → 실측 → M2b-3 좌석 값.** **[추기 23:2x] M1b 2차 = REVISE 3(MQ-1·MQ-3 HIGH · MQ-2 MED · 원문 `docs/lessons/2026-09-05-astra-m1b-m2b1v2.md` · D-02 §6) → **자문 트리거 ⓑ 발동(게이트 명기)** → v3 초안(drafts `SPEC-round-m2b1.md` · v2 는 `.v2.md`) + **advice-bundle 봉투 `~/projects/workspaces/advice/m2b1-gate-<날짜>/`(PROMPT.md · bundle.zip · REPLY.md 빈 파일) → Owner 가 ChatGPT 웹 astra pro 에 붙이고 회신을 REPLY.md 에 저장 → 총괄 처분(D-02 §7) → M1b 3차 또는 집행. 회신 전 M2b-1 집행 금지(폴백 규정). 그 사이 = M2b-2 발주문 설계(G-4 partial + enum 강제 + B-2) → **v1 = drafts `SPEC-round-m2b2.md` · M1b 1차 기동 23:2x(사본 `~/projects/workspaces/pd-m1b-m2b2` · `059e7f6` detached · 레인 `pd-lanes/astra-m1b-m2b2/` · 지적 `MR-*`) → 1차 = REVISE 7(MR-1 BLOCKER = 필드 정합 검사 ↔ m16 충돌 → 제거 · MR-2 승격 정책 입법 → 제거 · `5cebeb5` 반입 · D-02 §7) → v2 → M1b 2차 기동 23:45(레인 `pd-lanes/astra-m1b-m2b2v2/` · `MS-*` · 2번째 REVISE 면 자문 트리거).** **[추기 23:5x] M2b-2 M1b 2차 = REVISE 5(MS-1~5 · `3c4b870` 반입 · D-02 §8) → 자문 트리거 ⓑ(두 라운드 다) → v3(drafts `SPEC-round-m2b2.md` · v2 `.v2.md`) → **합본 봉투 `~/projects/workspaces/advice/m2b-gate-and-values-20260905-2357/`(PROMPT.md 7,294 B · bundle.zip 24파일 · 질문 ⓐ~ⓗ) 를 `SendUserFile` 로 Owner 에게 전달(원격 · 23:5x).** **지금 할 일 = 회신 대기.** 회신이 오면(Owner 가 채팅에 원문 붙임) `REPLY.md` 에 저장 → 봉투 대조(ENVELOPE.md sha) → D-02 §9 처분표(ⓐ~ⓗ 각 지적 = 수용/부분/기각/이연 + 사유) → 두 발주문 v4 → M1b 3차(각각 · 지적 `MT-*`/`MU-*`) → PASS → sol-coder(M2b-1 worktree `round-m2b1` · M2b-2 worktree `round-m2b2` · **전체 pytest 는 순차** — 두 레인을 동시에 띄우지 않는다) → 재현 → 병합(리포 루트 cwd · M2b-1 먼저) → 기록 → fable xhigh 감사(합본 가능). 회신 전 두 라운드 집행 금지. **[추기 23:0x] M1b 1차 = REVISE 8(MP-1~8 · HIGH 2 · `51d4c0d` 반입 · D-02 §5) → v2 → M1b 2차 기동(레인 `pd-lanes/astra-m1b-m2b1v2/` · 사본 재핀 `51d4c0d` · 지적 `MQ-*` · 2번째 REVISE 면 자문 트리거 ⓑ → advice-bundle 봉투).** **지금 할 일 = M1b 회수**(레인 `STATUS` 의 `EXIT=` → `sol-audit.sh finish --log <레인>` → `FINAL` 원문을 `docs/lessons/2026-09-05-astra-m1b-m2b1.md` 에 규율 10 머리말 + `지적 열거 =` 로 보존 → DISPOSITIONS §1(행 수 마커) → D-02 §5 처분 → REVISE 면 v2 → 2차 도전 · PASS 면 sol-coder 발주(worktree `round-m2b1` · `fc04d59` 분기 · 레인 `pd-lanes/sol-coder-round-m2b1/` · `setsid nohup` · Monitor) → 총괄 재현(전체 두 모드 · §2 대조표 직접) → 커밋(worktree) → **리포 루트 cwd** 에서 ff 병합·worktree 제거 → 기록 → fable xhigh 감사(T40 이 와서 M2b-2 가 곧 병합되면 합본). **T40 회신이 오면** `ruling-20260905-05-T40.md` · RULINGS-LEDGER §2 색인 + §3 포인터 · D-02 등재 마커 · 브리핑 배너 없이(재정 뒤 재발행 안 함 · ⒂) → M2b-2 발주문(`read.yaml` 세 값 + `run-kinds.yaml` `partial` + `source.run` enum 강제 + B-2 `lane_id` 어휘·경계 강제(T4) · SPEC C9·§8.2·§8.4 갱신) 설계 → M1b → sol-coder → 감사. 좌석·자문·킵얼라이브 규약은 29차 이하 그대로.

> [정정 2026-09-05 · 30차] 아래 29차 문단의 「지금 할 일 = PD-M2b 착수 — 발주문 설계부터」는 **끝났다**(M2b-1 발주문·M1b 기동 · T40 상신). 경위 보존용으로 남긴다.

**★ 09-05 29차 갱신 — 재정 T39: PD-M2a 러너 무결성(B-1 + G-5) 종결 선언(① A) · 사후 확인 ⓦ fail-closed 추인(② A)**(`ruling-20260905-04-T39.md` · 브리핑 `3292f4fc-…` 2판 배너 · `D-20260903-04` §46). 열린 사후 확인 = **없음**. Owner 재정 대기 = **0**.
**지금 할 일 = PD-M2b 착수 — 발주문 설계부터.** 로드맵 정본 = `ruling-20260901-06-T15.md` §1 ⒜(PD-M2b = G-1~G-4 좌석·계약 어휘 · B-2 `lane_id` 어휘·경계 강제(재정 T4)) + **백로그 ⑼**(정적 관문 `_direct_engine_ledger_calls` 가 `shadow_root=None` 을 통과 · `D-04` §45 · 첫 소라운드 후보) + ⓦ 부속 docstring 한 줄(`_write_shadow_pointer` refused 분기 · 첫 커밋에). 절차 = 설계 메모 → M1b astra high 도전(PASS 까지) → sol-coder(worktree · `setsid nohup` · 레인 홈 fs) → 총괄 재현(전체 두 모드 순차 · 홈 fs basetemp/TMPDIR · 차별 대조 직접) → 커밋·rebase(worktree) → 병합·worktree 제거(**리포 루트 cwd**) → 기록 → fable xhigh 감사(러너 템플릿 drafts `fable-audit-runner.template.sh` · 안내문 `fable-audit-brief-preamble.md` · **발주 직전 `brief.md` 판 표식 실측** · Monitor 감시) · 자문 트리거는 `advice-bundle.sh` 봉투(L-054). 백로그 9 = `D-04` §27 ⑴~⑺ · §33 ⑻ · §45 ⑼.

> [정정 2026-09-05 · 29차] 아래 28차 문단의 「지금 할 일 = T39 종결 상신 브리핑 발행」은 **끝났다**(T39). 경위 보존용으로 남긴다.

**★ 09-05 28차 갱신 — 좁은 재감사 7(RK · fable xhigh 3회째 · `docs/lessons/2026-09-05-fable-audit-round-m2a3.md`) = PASS · 신규 0 · RJ-1~4 closed · `D-20260903-04` **§45**(계열 종합 · M9 관측 3 = 25턴 · 12.3분 · $4.85 · 백로그 ⑼ 후보).** **PD-M2a 러너 무결성(B-1 + G-5) 감사상 닫힘.** 열린 사후 확인 = ⓦ 1건(+ RJ-5 병기). Owner 재정 대기 = **T39(발행 예정)**.
**[추기 20:1x] T39 브리핑 발행 = 아티팩트 `3292f4fc-f855-4846-8f22-8637e4b98a26`(drafts `OWNER-BRIEF-T39-m2a-closure.html` · 회신 서식 `T39: ① A / ② A` · ① 국면 종결 A 지금/B 백로그 ⑼ 뒤/C 전면 재감사 뒤 · ② ⓦ A fail-closed 추인/B fail-open/C fail-closed+refused 기록). Owner 결정 대기 1건.** **지금 할 일 = T39 종결 상신 브리핑 발행**(`/decision-brief` · drafts `OWNER-BRIEF-T39-m2a-closure.html` · 재정 ① 종결 선언 ② ⓦ 처분 A/B/C · RJ-5 병기 · 자잘 = 백로그 ⑻⑼ · 다음 = PD-M2b) → Owner 회신 `T39: ① A / ② A` → `ruling-20260905-04-T39.md` · RULINGS-LEDGER §2 · 브리핑 2판 배너 → **PD-M2b(G-1~G-4 · B-2)** 발주문 설계(M1b astra high → sol-coder → fable xhigh 감사 · 좌석 규약 = 이 파일 위 추기 · 자문은 advice-bundle 봉투). 상신 발행 = 단계 경계 → `/compact`.

> [정정 2026-09-05 · 28차] 아래 27차 문단의 「지금 할 일 = 좁은 재감사 7」은 **끝났다**(PASS). 경위 보존용으로 남긴다.

**★ 09-05 27차 갱신 — 라운드 M2a-3(재감사 6 시험 공백 수리 · 시험만) 병합 `8ceea90`**(sol-coder v2 · M1b MM 6 → MN PASS · 843/843 두 모드 · D7 직접 재현 ⓙ+ⓜ3 붉음 · `D-20260903-04` **§42** 회수 · §43 레인 보고). 열린 사후 확인 = ⓦ 1건(+ RJ-5 병기). Owner 재정 대기 0.
**지금 할 일 = 좁은 재감사 7(RK · 축소 범위 · M9 fable xhigh 3회째).** **[추기 19:5x] M1b astra high(재감사 7 발주문) = REVISE 1(MO-1 LOW · §44) → 발주문 정정 → 발주(사본 재핀 = 이 기록 커밋).** 발주문 drafts `AUDIT-ORDER-round-m2a3.md`(대상 `8ceea90` + 이 기록 커밋 · 자리표 채울 것) → M1b astra high 도전 → 감사 발주(사본 `pd-audit-round-m2a3` · basetemp `pd-audit10-basetemp` · **발주 직전 `bundle/`·`brief.md` 판 표식 실측** · setsid · Monitor) · 감사 중 정본 커밋 금지. **PASS → PD-M2a 러너 무결성 종결 상신 T39**(`/decision-brief` · 재정 = ① 종결 선언 ② ⓦ 추인(판정 불가 = fail-closed · RJ-5 거부 기록 소실 병기 · 감사자 판단 = S2 오류 처리 재량)) → PD-M2b(G-1~G-4 · B-2). **FAIL → 같은 상신 2회째 FAIL = 자문 트리거 ⓑ → `advice-bundle.sh` 봉투를 Owner 에게**(L-054 · fable CLI 자문 금지). 백로그 8.

> [정정 2026-09-05 · 27차] 아래 26차 문단의 「지금 할 일 = 라운드 M2a-3」는 **끝났다**(병합). 경위 보존용으로 남긴다.

**★ 09-05 26차 갱신 — 재감사 6(RJ · fable xhigh 2회째 · `docs/lessons/2026-09-05-fable-audit-round-m2a2.md`) = FAIL(MED 1 · LOW 4 · **구현 결함 0** · 시험 공백) · `D-20260903-04` §39(관측 2 = 66턴 · 39.3분 · $9.82).** RJ-1~4 → **수리 라운드 M2a-3(시험만 · 엔진 무접촉 · m26 에 ⓙⓚⓛⓜ 추가)** · RJ-5 → ⓦ 상신 병기. 열린 사후 확인 = ⓦ 1건(+ RJ-5 병기). Owner 재정 대기 0.
**[좌석 규약 추기 18:5x · ROUTING §5 ⑽ 개정 L-054 · Owner 육성]** **자문(트리거 ⓐ 결정 직전 · ⓑ 같은 문제 2회 저항 · ⓒ 출하 직전)은 fable xhigh CLI 로 부르지 않는다 — `~/.claude/agents/bin/advice-bundle.sh --name <이름> --prompt <질문.md> <파일…>` 로 봉투(PROMPT.md · bundle.zip · ENVELOPE.md)를 만들어 Owner 에게 내고, 회신은 `REPLY.md` 원문 → 총괄 처분표.** 폴백(Owner 부재·긴급)만 fable xhigh CLI. **M9 감사(fable xhigh CLI)는 그대로.** 이 세션의 fable xhigh 호출은 전부 M9 감사였다(자문 호출 0). 다음 자문 후보 = 재감사 7 이 FAIL 이면 ⓑ 발동(같은 상신 2회째 FAIL) → 봉투.
**지금 할 일 = 라운드 M2a-3.** **[추기 19:0x] M1b 2차(v2) = PASS(§41) → sol-coder 발주(레인 `pd-lanes/sol-coder-round-m2a3/` · worktree `round-m2a3`).** **[추기 18:5x] M1b astra high(M2a-3 v1) = REVISE 6(MM-1 HIGH = 임시 법 리포에 절차 문서 없어 통주 불가 · §40) → v2 → M1b 2차.** 발주문 drafts `SPEC-round-m2a3.md`(시험 4묶음 · 차별 대조 = 감사 원문 ③ 표의 D7·D6 / D2·D2b / D1 / D3·D4·D5 변조가 현 스위트 초록 → 새 시험 붉음) → M1b astra high → sol-coder(worktree `round-m2a3`) → 재현(전체 두 모드 · 차별 대조 직접) → 병합(**리포 루트 cwd**) → 기록 → **좁은 재감사 7(RK · 축소 범위 · fable xhigh · 전체 plain 1모드)** → PASS → **PD-M2a 러너 무결성 종결 상신(T39 · `/decision-brief` · ⓦ + RJ-5 추인 포함)** → PD-M2b.

> [정정 2026-09-05 · 26차] 아래 25차 문단의 「지금 할 일 = 재감사 6」는 **끝났다**(FAIL · 시험 공백). 경위 보존용으로 남긴다.

**★ 09-05 25차 갱신 — 라운드 M2a-2(G-5 · 재정 T38 집행) 병합 `1573591`**(sol-coder · 발주문 v3 · M1b astra high 2회 MJ·MK · 재현 835/835 두 모드 · 차별 대조 (i) 구 13 붉음→신 초록 · `D-20260903-04` **§36** 회수 · §37 레인 보고). **열린 사후 확인 = ⓦ 1건**(판정 불가 = fail-closed StageError · 총괄 재량 · §34·§35 · 뒤집으면 `_run_is_terminated` 의 판정 불가 분기 + m26 ⓘ 시험 기대값). Owner 재정 대기 0.
**지금 할 일 = 재감사 6(RJ · M9 fable xhigh 2회째).** **[추기 18:0x] M1b astra high(재감사 6 발주문) = REVISE 4(ML-1~4 · MED 2 LOW 2 · §38) → 발주문 정정 → 발주(사본 재핀 = 이 기록 커밋).** 발주문 drafts `AUDIT-ORDER-round-m2a2.md`(대상 `1573591` + 이 기록 커밋 · 자리표 채울 것) → M1b astra high 도전(사본 = 이 기록 커밋 detached + `bundle/`) → 감사 발주(러너 템플릿 `fable-audit-runner.template.sh` · 안내문 `fable-audit-brief-preamble.md` · 사본 `~/projects/workspaces/pd-audit-round-m2a2` · basetemp `pd-audit9-basetemp` · setsid) · **감사 중 정본 커밋 금지** · 감사 중 배경 대기 명령은 메모리 부족으로 죽으니 Monitor 로. PASS → **PD-M2a 러너 무결성 종결 상신**(B-1 + G-5 · `/decision-brief` · ⓦ 추인 포함) → PD-M2b(G-1~G-4 · B-2). 백로그 8(§27 ⑴~⑺ + §33 ⑻).

> [정정 2026-09-05 · 25차] 아래 24차 문단의 「지금 할 일 = 라운드 M2a-2」는 **끝났다**(병합). 경위 보존용으로 남긴다.

**★ 09-05 24차 갱신 — 재감사 5(RI · M9 fable xhigh 첫 적용 · `docs/lessons/2026-09-05-fable-audit-round-m2a1.md`) = PASS · LOW 3(RI-1 시험 공백 → M2a-2 ⑤ 이월 · RI-2·RI-3 기록 오기 정정) · `D-20260903-04` §33(첫 관측 = 54턴 · 18.5분 · $5.95 · 절단 없음).** 라운드 M2a-1(B-1) 감사상 닫힘. Owner 결정 대기 **0**.
**지금 할 일 = 라운드 M2a-2(G-5 · 재정 T38 집행).** **[추기 17:2x] M1b 2차(v2) = REVISE 5(MK-1~5 · BLOCKER 0 · §35) → v3 → sol-coder 발주(3차 도전 없이 · M2a-1 선례) · 레인 `pd-lanes/sol-coder-round-m2a2/` · worktree `round-m2a2`(`ec6000e` 분기).** **[추기 17:1x] M1b astra high(M2a-2 발주문 v1) = REVISE 6(MJ-1 BLOCKER ~ MJ-6 · §34) → v2 → M1b 2차. 열린 사후 확인 = ⓦ 1건(MJ-1 판정 불가 = fail-closed StageError · 총괄 재량 · Owner 추인 대기 · 뒤집으면 가드 함수 한 곳 + 시험 ⓘ).** 발주문 drafts `SPEC-round-m2a2.md`(v1 · 좌표 `c7b97f1` 판 · ⑤ = RI-1 ⓓ1 시험) → **M1b astra high 도전**(`sol-audit.sh run --model gpt-6-astra --effort high` · setsid · 사본 = 이 기록 커밋 detached + `bundle/`) → PASS/REVISE 반영 → sol-coder(worktree `round-m2a2` · `setsid nohup` · 레인 `pd-lanes/sol-coder-round-m2a2/`) → 총괄 재현(전체 pytest 두 모드 순차 · 홈 fs basetemp/TMPDIR · 차별 대조 (i) 구 트리 직접) → 커밋 → **리포 루트 cwd 에서** rebase·ff 병합·worktree 제거 → 기록 커밋 → 재감사 6(fable xhigh · 러너 템플릿 drafts `fable-audit-runner.template.sh` · 안내문 `fable-audit-brief-preamble.md`). 백로그 8(§27 ⑴~⑺ + §33 ⑻ `__pycache__` 누출).

> [정정 2026-09-05 · 24차] 아래 23차 문단의 「지금 할 일 = 재감사 5」는 **끝났다**(PASS). 경위 보존용으로 남긴다.

**★ 09-05 23차 갱신 — 라운드 M2a-1(B-1 · 재정 T3 집행) 병합 `0f00dc7`**(sol-coder · 발주문 v3 · M1b astra high 2회 경유 · 재현 819/819 두 모드 · 차별 대조 (i) 구 6 붉음→신 8 초록 · `D-20260903-04` **§30** 회수 · §31 레인 보고). **재정 T38 등재 `f3bd05b`**(G-5 전제 셋 · `ruling-20260905-03-T38.md` · Owner 결정 대기 **0**).
**지금 할 일 = 재감사 5(RI) — M9 fable xhigh 첫 적용.** **[추기 16:4x] M1b astra high(재감사 5 발주문) = REVISE 2(MI-1·MI-2 · MED · §32) → 발주문 정정 → 발주(사본 재핀 = 이 기록 커밋).** 발주문 drafts `AUDIT-ORDER-round-m2a1.md`(대상 `0f00dc7` + 이 기록 커밋) → M1b astra high 도전(`sol-audit.sh run --model gpt-6-astra --effort high` · setsid) → 감사 발주(LANE-RUNTIME 「M9 감사 호출 꼴」 · 러너 템플릿 drafts `fable-audit-runner.template.sh` · 격리 사본 `~/projects/workspaces/pd-audit-round-m2a1` + `.audit-sandbox` 마커 · basetemp/TMPDIR 홈 fs `pd-audit8-basetemp` · setsid · `usage.json` 보존) · **감사 중 정본 커밋 금지**. PASS → **라운드 M2a-2(G-5 · 재정 T38)**: 발주문 초안 drafts `SPEC-round-m2a2.md` v1(좌표는 `0f00dc7` 판 `read.py` 로 재실측 뒤 확정) → M1b astra high → sol-coder(worktree `round-m2a2`) → 재현 → 병합 → 재감사 6. **절차 주의(§30)**: 병합·worktree 제거는 **리포 루트 cwd** 에서 — worktree 안에서 `merge --ff-only` 는 자기 브랜치 no-op 이고 `worktree remove` 가 cwd 를 지운다.

> [정정 2026-09-05 · 23차] 아래 22차 문단의 「지금 할 일 = PD-M2 잔여 좌표로 이동 · 추기 …」는 **끝났다**(M2a-1 병합 · T38 등재). 경위 보존용으로 남긴다.

**★ 09-05 22차 갱신 — 재정 T37: PD-M2a 라운드 B 계열 종결 선언(① A) · 사후 확인 ⓡ~ⓥ 추인(② A)**(`ruling-20260905-02-T37.md` · 브리핑 `43141fdb-…` 2판 배너). 열린 사후 확인 = **없음**. **좌석 규약 갱신(ROUTING v2.1 · agents `b1aa4ae` 실측 · T37 §3)**: **M1b = astra high** · **M9(sol·astra 저작 감사) = fable xhigh(CLI · allowlist · 폴백 opus xhigh) · opus max 퇴출(L-053)** · M3 sol-coder high · M2 astra medium(약정) — 이 계열의 감사 7회는 당시 정본 opus max 로 돌았다(기록).
**지금 할 일 = PD-M2 잔여 좌표로 이동.** 후보 순서(총괄 안 · 다음 세션이 실측 뒤 확정): **[추기 16:1x] T38 재정 접수 `① A / ② A / ③ A` → `ruling-20260905-03-T38.md` · Owner 결정 대기 0 · G-5 = 라운드 M2a-2 로 집행(M2a-1 회수·병합 뒤 · M1b astra high → sol-coder → fable xhigh 감사).** **[추기 16:0x] M1b 2차(M2a-1 v2) = REVISE 5(MH · §29) → v3 로 sol-coder 발주 15:59(`pd-lanes/sol-coder-round-m2a1/` · worktree `round-m2a1`) · 회수 뒤 감사 = fable xhigh 첫 적용.** **[추기 16:0x] G-5 상신 발행 — 문서 `docs/decisions/D-20260905-01-g5-termination.md` · 브리핑 아티팩트 `492e8207-6c09-4e3e-a697-c610ab1c5f9c`(drafts `OWNER-BRIEF-T38-g5-termination.html`) · 회신 서식 `T38: ① A / ② A / ③ A` · **Owner 결정 대기 1건(재정 셋 묶음)**.** **[추기 15:5x] M1b astra high(M2a-1 발주문) = REVISE 6 · **BLOCKER MG-1**: G-5 가드가 T17 봉투 재진입을 끊음 → **라운드 M2a-1 = B-1 만**(v2) · **G-5 = 설계 메모 → Owner 상신**(종결 정의 · 원장 기입 시점 · 구 런 처분 · §28).** ⑴ **[정정 15:4x] 로드맵 정본은 재정 T15 §1 ⒜·T1 — 다음 = PD-M2a 러너 무결성 = B-1(레인 로그 검사를 디스크 기록본으로 · T3) + G-5(종결 재진입 멱등 가드) · 신규 재정 0 → 라운드 M2a-1**(발주문 drafts `SPEC-round-m2a1.md` · M1b astra high 도전 15:42 기동 `pd-lanes/astra-m1b-m2a1/`) → PD-M2b(G-1~G-4 · B-2) → PD-M2c. 「절차 문서 라운드」라는 앞 문언은 총괄 오기 — T33 ① 은 `8259075` 로 이미 집행됐다. 백로그 ⑵⑶⑸ 는 M2a-1 뒤 또는 M2c 골든과 함께 ⑵ 백로그 ⑴ reader 폴백 제거는 이식 단위(READER-VERSION · N15) — 별건 ⑶ ⑷ flaky 관측 · ⑹ LANE-RUNTIME 편입(이관 때) · ⑺ LEDGER 셀 형식. 발주문은 **M1b astra high** 를 거쳐 집행 · 감사는 **fable xhigh**(LANE-RUNTIME 「Fable 좌석 호출 경로」 + L-053 allowlist 규격 재독 뒤). **Owner 결정 대기 = 없음.**

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
