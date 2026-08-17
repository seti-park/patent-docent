# sol 독립 감수 원문 — M0.6 개정 (2026-08-18)

**보존 근거.** 재정 2026-08-18 **N7 ①**(모든 외부 감수·검증 산출물은 수령 즉시 **원문 그대로** `docs/lessons/`에 보존, 처분표·요약은 원문 포인터로만).

| 항목 | 값 |
|---|---|
| 감수자 | GPT-5.6-sol, reasoning effort max, read-only, 교차벤더 독립 |
| 대상 | HEAD `fedbde265e20e3e35a4f3c3e687a1abf24a651cc`, 범위 `5a82a6b..fedbde2` (9커밋) |
| 판정 | **FAIL** — BLOCKER 4 / MAJOR 17 / MINOR 3 |
| 발주 요건 | ① N1~N13 원장 대조 ② A군 집행 실증 ③ M0 감수 원문 대조 + 독립 재도출 ④ 계약↔스펙↔헌장 정합 |
| 실행 비고 | `.venv/bin/pytest tests/ -q`가 read-only 샌드박스의 임시 디렉터리 부재로 pytest **기동 전** 실패했고, 감수자가 `-s -p no:cacheprovider` 등가 실행으로 **49 passed**를 확인해 제품 실패와 구별했다(원문 필수 명령 실측 표에 명기) |

**본문은 아래 구분선 다음부터 원문 그대로다.** 요약·정정·재배열을 하지 않았다. 이 감수의 처분은 `docs/decisions/D-20260818-01-m06-enforcement.md` §5이며, 그 처분표는 이 원문의 **색인이지 대체물이 아니다**.

---

# 최종 판정: FAIL

대상은 `fedbde265e20e3e35a4f3c3e687a1abf24a651cc`, 범위는 `5a82a6b..fedbde2`, 9개 커밋으로 확인했다.

현행 결함은 BLOCKER 4건 / MAJOR 17건 / MINOR 3건이다.

중요한 범위 사실이 하나 있다. [D-20260818-01-m06-enforcement.md](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:1)는 작업트리에 `??`로 존재하지만 `fedbde2`에는 포함되지 않는다. 아래에서는 발주문이 그 문서를 지목했으므로 내용은 읽었으나, HEAD 산출물로 인정하지 않았다.

## BLOCKER

1. **B-01 — M0.6 처분 기록이 대상 커밋에서 누락되어 재정 추적성과 점수 린트의 권한 근거가 끊겼다.**  
   위치: [SPEC.md:7](/home/laptop/projects/patent-docent/docs/SPEC.md:7), [RULINGS-LEDGER.md:43](/home/laptop/projects/patent-docent/docs/decisions/RULINGS-LEDGER.md:43), [score-lint.yaml:84](/home/laptop/projects/patent-docent/contracts/lexicon/score-lint.yaml:84), [score-lint.yaml:102](/home/laptop/projects/patent-docent/contracts/lexicon/score-lint.yaml:102), [score-lint.yaml:118](/home/laptop/projects/patent-docent/contracts/lexicon/score-lint.yaml:118), [score-lint.yaml:134](/home/laptop/projects/patent-docent/contracts/lexicon/score-lint.yaml:134).  
   오류: `git ls-tree fedbde2`에는 파일이 없고 작업트리에만 비추적 파일로 있다. 더구나 그 파일 자체도 [12행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:12)에서 “재정 문서가 아니다”라고 한다. 그런데 점수 린트 4개 항목은 Owner 원장 N4가 아니라 이 비재정·비추적 문서를 `decision`으로 가리킨다.  
   반증: N6은 “재정 → 원장 → 문서”와 반영처 링크를 요구한다([원장:33](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:33)); N4는 패턴별 재정 기록을 요구한다([원장:29](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:29)).  
   신뢰도: **100%**.

2. **B-02 — A군의 정확한 재현식 두 개가 여전히 ACCEPT되며, “REJECT_OK 13/13”은 해당 의미 불변식을 시험하지 않는다.**  
   위치: [check_schema_enforcement.py:5–14](/home/laptop/projects/patent-docent/tools/check_schema_enforcement.py:5), [check_schema_enforcement.py:226–242](/home/laptop/projects/patent-docent/tools/check_schema_enforcement.py:226), [manifest.json:27–31](/home/laptop/projects/patent-docent/tests/fixtures/schema-enforcement/manifest.json:27), [manifest.json:146–150](/home/laptop/projects/patent-docent/tests/fixtures/schema-enforcement/manifest.json:146), [material-spec.schema.json:5](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:5), [metrics-row.schema.json:5](/home/laptop/projects/patent-docent/contracts/schemas/metrics-row.schema.json:5).  
   오류: 정확한 실측에서 `derivation.inputs[0].ref` 자기참조와 `completion_proxy: 999`가 ACCEPT됐다. 도구는 JSON Schema만 호출하며 `read.pointer-resolve`나 `feedback.row-consistency`를 실행하지 않는다. manifest는 자기참조 대신 `origin` 혼합을, `999` 대신 음수 `-1.5`를 시험한다.  
   반증: M0.5 원문의 정확한 재현식은 [98행과 103행](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m05-full.md:98)이다. 발주 조건상 `drop_decision`만 ACCEPT가 정답이다.  
   신뢰도: **100%**.

3. **B-03 — N5 판정 행 스키마가 서로 모순되는 결과를 유효한 보고로 받아들인다.**  
   위치: [verdict-check-row.schema.json:18–53](/home/laptop/projects/patent-docent/contracts/schemas/verdict-check-row.schema.json:18), [verdict-check-row.schema.json:55–92](/home/laptop/projects/patent-docent/contracts/schemas/verdict-check-row.schema.json:55).  
   오류: 직접 검증에서 `status: pass + violations: 1`, `status: fail + violations: 0`, `ruleset: null + ruleset_version: "1.0"`이 모두 ACCEPT됐다. 스키마는 공허 파생만 확인하고 상태↔위반 수, ruleset 3-튜플 정합을 강제하지 않는다. `check_schema_enforcement.py`의 3개 스키마에도 이 신설 스키마가 포함되지 않는다.  
   반증: N5는 모든 게이트 검사가 수량과 상태를 정량 보고하여 공허와 실제 통과를 구별하도록 명령한다([원장:31](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:31)). 현재 행은 수량과 상태가 서로 반대여도 유효하므로 게이트 판정문 전체가 거짓말할 수 있다.  
   신뢰도: **100%**.

4. **B-04 — M0 B5의 “실재 인용 + 날조 수치” 경로가 실제 스키마에서 여전히 열린다.**  
   위치: [SPEC.md:1436–1450](/home/laptop/projects/patent-docent/docs/SPEC.md:1436), [SPEC.md:1573](/home/laptop/projects/patent-docent/docs/SPEC.md:1573), [SPEC.md:2030](/home/laptop/projects/patent-docent/docs/SPEC.md:2030), [material-spec.schema.json:5](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:5).  
   오류: 유효한 인용문과 `value_span`은 그대로 두고 `value_raw: "999 mm"`, `value_normalized: "999"`만 넣은 인스턴스가 ACCEPT됐다. 문서는 “수치가 원천 밖에서 만들어지는 경로가 남아 있지 않다”고 하지만 그 검증기는 M1 예정이며 현재 존재하지 않는다.  
   반증: 복원 M0 B5는 바로 이 공격을 BLOCKER로 판정했다([원문:43](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:43)). R1도 값을 직접 기입하지 못하게 하고 스팬에서 기계 추출하도록 재정했다([R 재구성:26](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260817-01-R1-R12.md:26)).  
   신뢰도: **100%**.

## MAJOR

1. **M-01 — N9의 “파생 원천은 원문 스팬만”이 “origin이 derived가 아니면 됨”으로 완화됐고, 항목별 승인도 공허하다.**  
   위치: [SPEC.md:1455–1461](/home/laptop/projects/patent-docent/docs/SPEC.md:1455), [material-spec.schema.json:74–97](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:74), [approval-envelope.schema.json:77–80](/home/laptop/projects/patent-docent/contracts/schemas/approval-envelope.schema.json:77), [SPEC.md:455](/home/laptop/projects/patent-docent/docs/SPEC.md:455).  
   오류: 현재 규칙은 참조 대상의 origin이 `derived`만 아니면 되므로 `figure-sourced`와 `bibliographic`을 입력으로 허용한다. 이는 “원문 스팬만”보다 넓다. `derived_fact_ack[]`도 실제 파생 fact 집합과 대조하지 않아 빈 목록이나 유령 ID가 승인 봉투를 통과한다.  
   반증: N9 원문은 원천을 원문 스팬으로 한정하고 스키마·검사 집행 및 항목 단위 승인을 요구한다([원장:39](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:39)).  
   신뢰도: **99%**.

2. **M-02 — N4 점수 린트는 승인된 학점형 등급을 완전히 막지 않고, 관할 문언도 자기모순이며 회귀 표본이 실행되지 않는다.**  
   위치: [score-lint.yaml:106–113](/home/laptop/projects/patent-docent/contracts/lexicon/score-lint.yaml:106), [SPEC.md:2705–2718](/home/laptop/projects/patent-docent/docs/SPEC.md:2705), [SPEC.md:2749](/home/laptop/projects/patent-docent/docs/SPEC.md:2749), [SPEC.md:3893](/home/laptop/projects/patent-docent/docs/SPEC.md:3893).  
   오류: 정규식 실측에서 단독 `B+`가 통과했다. 파일은 이를 의도적으로 허용하지만 복원 M0의 대표 우회가 바로 `B+`였고 N4는 학점형 등급을 승인했다. §4.6은 자문 산출물 전용이라고 한 뒤 2749행에서 “본문까지 본다”고 반대로 적는다. 별점 표본은 데이터로만 있고 실제 린터와 `engine/regression/run_suite.py`는 예정 상태다.  
   반증: N4([원장:29](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:29)), M0 M18([원문:73](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:73)), SPEC 자체의 “심은 결함 100% 검출” 조건([SPEC.md:2844](/home/laptop/projects/patent-docent/docs/SPEC.md:2844)).  
   신뢰도: **100%**.

3. **M-03 — N10 게시 전제조건 3종 중 2종은 기계 판정 좌표가 없다.**  
   위치: [run-kinds.yaml:40–53](/home/laptop/projects/patent-docent/contracts/run-kinds.yaml:40), [run-kinds.yaml:58–65](/home/laptop/projects/patent-docent/contracts/run-kinds.yaml:58).  
   오류: 도면 사용권만 `run_yaml_key`와 파일 실재 증거가 있다. `defense_layers`는 이름 배열뿐이고 “가동”의 증거 경로·상태 술어가 없으며, `template_freeze`는 설명 한 줄뿐이다. 향후 러너가 두 조건을 판정하려면 계약 밖 의미를 새로 발명해야 한다.  
   반증: N10은 런 시작 시점의 기계 봉쇄를 요구한다([원장:41](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:41)).  
   신뢰도: **98%**.

4. **M-04 — N12가 정하지 않은 전시물 후보 산정식을 SPEC이 무단 확정했다.**  
   위치: [SPEC.md:287–300](/home/laptop/projects/patent-docent/docs/SPEC.md:287), 비추적 처분표 [§6 139행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:139).  
   오류: SPEC은 후보 수를 “원천 도면 수 기준”이라고 확정한다. 같은 라운드 처분표는 서브도면 분할 등을 포함한 계산 규칙이 미정이라고 한다. 이 판단은 E20~E27·G9·G10 어디에도 없다.  
   반증: N12는 후보 수 보고와 부족 시 escalate만 정하고 산정식은 정하지 않았다([원장:45](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:45)).  
   신뢰도: **100%**.

5. **M-05 — 숫자 화이트리스트의 CP1 승인 단계가 스키마에서 빠져 원래 B10의 승인 시점 모순이 부분 존속한다.**  
   위치: [SPEC.md:3562](/home/laptop/projects/patent-docent/docs/SPEC.md:3562), [approval-envelope.schema.json:98–112](/home/laptop/projects/patent-docent/contracts/schemas/approval-envelope.schema.json:98), [material-approved fixture](/home/laptop/projects/patent-docent/tests/fixtures/schema-enforcement/accept/approval-envelope.material-approved.json:1).  
   오류: SPEC은 목록 전량을 CP1 봉투에 첨부해 승인하도록 하지만 스키마는 `numeric_whitelist_printed`를 CP2 승인에만 요구한다. 필드가 없는 CP1 승인 봉투가 ACCEPT됐다.  
   반증: D8의 숫자 면제 통제와 M0 B10의 “단일 승인 단계” 요구([원문:57](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:57)).  
   신뢰도: **100%**.

6. **M-06 — M0 B4의 청구항 구조 손실은 일부만 보수됐다.**  
   위치: [SPEC.md:1337–1343](/home/laptop/projects/patent-docent/docs/SPEC.md:1337), [SPEC.md:1374–1397](/home/laptop/projects/patent-docent/docs/SPEC.md:1374), [material-spec.schema.json:181–222](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:181).  
   오류: 배열과 전문은 생겼지만 Markush·조건부·means-plus-function 관계는 여전히 typed operator 없이 문자열에만 남는다. `alternative-form`은 enum에 있으나 5개 파싱 규칙이 모두 `single`/`multiple-and`/`multiple-or`로만 귀결해 사실상 도달 불능이며 처분표도 이를 인정한다([§6 142행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:142)).  
   반증: M0 B4 원문([원문:41](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:41)).  
   신뢰도: **99%**.

7. **M-07 — M0 M12의 원천 청구항 인벤토리·구조 수렴 사각지대가 생존한다.**  
   위치: [SPEC.md:4493–4502](/home/laptop/projects/patent-docent/docs/SPEC.md:4493).  
   오류: 현행 커버리지는 등재된 항목 사이만 검사하고 원천 청구항 누락을 찾지 못한다. 수렴은 종속항과 트리 간선을 비교하지 않는다. 현행 SPEC도 이를 명시적으로 인정한다.  
   반증: M0 M12([원문:59](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:59)); `D-20260817-02`의 “해소” 판정([64행](/home/laptop/projects/patent-docent/docs/decisions/D-20260817-02-spec-revision-m05.md:64))은 과장이었다.  
   신뢰도: **100%**.

8. **M-08 — M0 M13의 동결 항목 payload 불변성이 생존한다.**  
   위치: [SPEC.md:4504–4514](/home/laptop/projects/patent-docent/docs/SPEC.md:4504).  
   오류: ID 존재만 비교하므로 개정본에서 기존 항목 의미를 바꿔도 통과한다. 상태 전이와 승계 사슬도 닫히지 않았다.  
   반증: M0 M13([원문:61](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:61)). 과거 처분은 이를 지표 원장의 append-only 문제로 잘못 치환했다.  
   신뢰도: **100%**.

9. **M-09 — M0 M14의 재료 측 수치 문법 부재가 생존한다.**  
   위치: [SPEC.md:4516–4524](/home/laptop/projects/patent-docent/docs/SPEC.md:4516), [material-spec.schema.json:345–347](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:345).  
   오류: 범위·부등호·공차·포함성·과학표기 등을 구조적으로 담지 못한다. 본문 토크나이저 확장은 재료 값 타입을 만들지 않는다.  
   반증: M0 M14([원문:63](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:63)).  
   신뢰도: **100%**.

10. **M-10 — N13은 M0 M15 전체를 해소하지 않았는데 SPEC은 전체 논점을 종결 처리했다.**  
    위치: [SPEC.md:4395–4401](/home/laptop/projects/patent-docent/docs/SPEC.md:4395), [material-spec.schema.json:148–168](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:148), [SPEC.md:3200](/home/laptop/projects/patent-docent/docs/SPEC.md:3200).  
    오류: N13은 패밀리 필드의 v0 미도입만 결정했다. 현행은 여전히 assignee·priority가 단수이고 jurisdiction/kind, applicant/inventor 배열, classification 등이 없다. 더 근본적으로 같은 필수 `drop_signal`을 historian이 다른 뜻으로 채워도 된다고 명시한다.  
    반증: M0 M15는 패밀리뿐 아니라 필수 필드의 프로젝트 간 의미 불일치를 함께 지적했다([원문:65](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:65)); D14는 하나의 프로젝트 간 계약을 요구한다([CHARTER.md:187–194](/home/laptop/projects/patent-docent/docs/CHARTER.md:187)).  
    신뢰도: **99%**.

11. **M-11 — M0 M16의 역왕복 문제는 대부분 보수됐지만 문장 단위 추적성은 닫히지 않았다.**  
    위치: [SPEC.md:2125–2130](/home/laptop/projects/patent-docent/docs/SPEC.md:2125), [l0-format.yaml:111–118](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:111), [SPEC.md:3424](/home/laptop/projects/patent-docent/docs/SPEC.md:3424).  
    오류: `frontmatter_raw`, 공백 금지, 빈 줄 금지는 개선됐다. 그러나 한 줄의 복수 문장은 재계수될 뿐 명시적으로 거부되지 않아 태그 하나가 여러 기술 문장을 덮을 수 있다. 실제 `annotation.schema.json`도 M3 예정이다.  
    반증: M0 M16의 별도 핵심은 “one sentence = one line” 미검증으로 문장 단위 추적이 무너진다는 것이었다([원문:71](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:71)).  
    신뢰도: **91%**.

12. **M-12 — M0 M19의 인과 없는 weakest_tweet 선택 알고리즘이 그대로다.**  
    위치: [SPEC.md:2955–2971](/home/laptop/projects/patent-docent/docs/SPEC.md:2955).  
    오류: 표적별 hit rate는 변주 전체 값인데, 인용 문장 수가 적은 트윗과 뒤쪽 트윗을 선택한다. 그 트윗이 miss를 일으켰다는 프로브 증거는 없다. 결정론이 된 것은 맞지만 인과적 국소화가 된 것은 아니다.  
    반증: M0 M19는 바로 현재의 “인용 수 최소 → 뒤 트윗” 규칙이 자의적이라고 지적했다([원문:75](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:75)).  
    신뢰도: **100%**.

13. **M-13 — M0 B3의 no-rewrite 우회는 하드/소프트 모순만 고쳐졌고 의미적 우회는 살아 있다.**  
    위치: [SPEC.md:2759–2767](/home/laptop/projects/patent-docent/docs/SPEC.md:2759).  
    오류: 무인용, 한국어, 5토큰 미만, 토큰 교체형 대체문이 통과한다. 현행 문서도 이를 `[OPEN]`으로 인정한다.  
    반증: D8은 게이트의 직접 집필을 전면 금지하며, M0 B3는 이 네 우회를 BLOCKER로 지적했다([원문:39](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:39)).  
    신뢰도: **100%**.

14. **M-14 — G9가 기존 reader 계약의 major 규율을 재정 없이 사후 완화했다.**  
    위치: [CLAUDE.md:31–37](/home/laptop/projects/patent-docent/CLAUDE.md:31), [SPEC.md:1232–1236](/home/laptop/projects/patent-docent/docs/SPEC.md:1232), 비추적 처분표 [123행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:123).  
    오류: 빈 `additions` 금지와 `_en` 언어 제한은 기존에 유효했던 v0 인스턴스를 거부하는 변경이다. 기존 규율은 breaking change에 major+상대 리포 상신을 요구한다. G9는 “미동결이면 minor”라는 예외를 스스로 만들어 0.3.0으로 처리했다. N1~N13에는 이 예외 재정이 없다.  
    반증: [CLAUDE.md:36](/home/laptop/projects/patent-docent/CLAUDE.md:36)과 D14.  
    신뢰도: **98%**.

15. **M-15 — E26은 R9의 n=5를 유효 응답 3으로 완화한 결함을 Owner 재정 없이 “해소”라 불렀다.**  
    위치: [parameters.yaml:22–31](/home/laptop/projects/patent-docent/contracts/parameters.yaml:22), [SPEC.md:4254](/home/laptop/projects/patent-docent/docs/SPEC.md:4254), 비추적 처분표 [116행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:116).  
    오류: `ceil(n/2)`는 n=5에서 실효 표본을 3으로 낮춘다. “현행 동작 불변”은 해소 근거가 아니다. M0.5 감수는 바로 그 현행 동작을 M-04로 지적했다.  
    반증: R9 재구성본은 `probe.n = 5`를 명시한다([R 원장:34](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260817-01-R1-R12.md:34)); M0.5 원문은 이를 완화로 판정하고 `needs confirmation`으로 남겼다([원문:40](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m05-full.md:40)). R계열이 재구성본이라는 한계 때문에 신뢰도를 낮췄다.  
    신뢰도: **86%**.

16. **M-16 — N6의 D계열 원장은 요구된 재구성본 서식을 충족하지 않는다.**  
    위치: [ruling-20260817-00-D1-D15.md:14–25](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260817-00-D1-D15.md:14), [RULINGS-LEDGER.md:18–23](/home/laptop/projects/patent-docent/docs/decisions/RULINGS-LEDGER.md:18).  
    오류: 파일은 의도적으로 포인터만 두고 D1~D15별 재구성 문언이나 결정 요지를 담지 않는다. R/D를 원문처럼 낱말 대조하지는 않았지만, “재구성 문언 + 결정 요지 + 반영처” 자체가 없다는 형식 누락은 직접 판정 가능하다.  
    반증: N6은 D1~D15 재구성본 표시와 해당 필드들을 명시적으로 요구한다([원장:33](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:33)).  
    신뢰도: **100%**.

17. **M-17 — 비추적 처분표 §6의 “잔여 14항”은 실제 미해소 목록을 모두 포함하지 않는다.**  
    위치: [D-20260818-01:128–147](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:128), [SPEC.md:4216](/home/laptop/projects/patent-docent/docs/SPEC.md:4216).  
    오류: §6에는 B5 수치 결속, B10 CP1 화이트리스트, M15의 광범위한 D14 계약 문제, M16 문장 추적성, M18 단독 학점형 등급/실행기 부재, M19 인과 없는 국소화가 없다. A군 자기참조·비율·corrects 구현도 §2에서는 “부분”이라고 하면서 §6에서는 빠졌다. B4도 `alternative-form`만 열거하고 Markush·조건부·means-plus-function 잔여를 누락했다.  
    반증: N7은 미처분 지적의 재도출과 정직한 한계 기록을 요구한다([원장:35](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:35)).  
    신뢰도: **99%**.

## MINOR

1. **m-01 — 형식 수치의 기계 정본은 시트 하나지만, “값 사본 없음”이라는 자체 주장은 사실이 아니다.**  
   위치: [format-parameters.yaml:8–10](/home/laptop/projects/patent-docent/contracts/format-parameters.yaml:8), [l0-format.yaml:9–11](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:9), [l0-format.yaml:28–33](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:28), [l0-format.yaml:53–55](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:53), [l0-format.yaml:68](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:68), [l0-format.yaml:194–197](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:194).  
   오류: `version 3`, `scale 100`, `180/260`, `6/12`, `≥1/≤2` 등이 주석·note에 복제돼 있다. 현재 값은 시트와 일치하고 loader가 쓰는 값은 포인터이므로 현재 행동 표류는 없지만, 향후 시트 변경 시 낡을 사본은 남았다.  
   반증: N-D11의 “수치 전부 이관”([원장:25](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:25)).  
   신뢰도: **100%**.

2. **m-02 — N8이 요구한 `pytest --version` 실출력이 산출물에 첨부되지 않았다.**  
   위치: [원장:37](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:37), [requirements-dev.txt:1–3](/home/laptop/projects/patent-docent/requirements-dev.txt:1), [CLAUDE.md:41](/home/laptop/projects/patent-docent/CLAUDE.md:41).  
   오류: 환경과 의존성 기록은 있으나 리포 및 9개 커밋 메시지 어디에도 실제 출력이 없다. 이번 실측값은 `pytest 9.1.1`이다.  
   신뢰도: **100%**.

3. **m-03 — M0 건수 기록이 아직 서로 모순된다.**  
   위치: [M0 원문:35–77](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:35), [D-20260817-01:5](/home/laptop/projects/patent-docent/docs/decisions/D-20260817-01-sol-audit-m0.md:5), [D-20260817-02:45–47](/home/laptop/projects/patent-docent/docs/decisions/D-20260817-02-spec-revision-m05.md:45).  
   오류: 복원 원문에는 BLOCKER 라벨 10개, MAJOR 라벨 11개, MINOR 1개가 있다. D-01과 D-02는 10/10/1이라고 적는다. 발주문의 “BLOCKER 9”도 원문과 다르므로 본 감수는 누락 방지를 위해 10+11+1 전부를 대조했다. HEAD에는 이 수를 정정하는 추적 문서가 없다.  
   신뢰도: **100%**.

## 필수 명령 실측

| 명령 | 결과 | 판정 |
|---|---|---|
| `python3 tools/check_spec_refs.py` | exit 0, K1~K7 PASS | 주장과 일치. 단 경로·메타 정합 검사이며 위 의미 결함을 보지 않는다 |
| `python3 -O tools/check_spec_refs.py` | exit 0, 동일 | 최적화 공허 통과 없음 |
| `python3 tools/check_schema_enforcement.py` | exit 0, `REJECT_OK 13/13`, `ACCEPT_OK 8/8`, `schemas=3` | 출력 주장은 사실이나 테스트 집합이 불완전해 A군 전체 집행 증명이 아님 |
| `python3 -O tools/check_schema_enforcement.py` | 동일 | `assert` 제거 영향 없음 |
| `.venv/bin/pytest tests/ -q` | exit 1, pytest 시작 전 `FileNotFoundError`: `/tmp`, `/var/tmp`, `/usr/tmp`, repo 중 쓸 수 있는 임시 디렉터리 없음 | 읽기 전용 샌드박스 환경 실패. 제품 테스트 실패와 구별 |
| `.venv/bin/pytest -s -p no:cacheprovider tests/ -q` | **49 passed** | 쓰기·capture를 피한 등가 실행 성공 |
| `PYTHONOPTIMIZE=1 .venv/bin/pytest -s -p no:cacheprovider tests/ -q` | **49 passed** | `-O`에서도 동일. pytest의 일반 경고 1개뿐 |
| `.venv/bin/pytest --version` | `pytest 9.1.1` | 환경 실재 확인 |

도구와 테스트 소스의 AST/텍스트를 확인한 결과 실제 `assert` 문은 없었다. 다만 pytest와 독립 도구가 같은 manifest를 읽으므로, 49 pass는 불완전한 oracle을 두 번 확인한 것이지 별도 의미 검증은 아니다.

## A군 정확 재현 결과

현재 스키마를 `Draft202012Validator`에 넣고 원문 표의 한 축만 변이했다.

| 재현식 | 정답 | 실제 |
|---|---:|---:|
| `additions: []` | REJECT | **REJECT** |
| `derivation.inputs[0].ref` 자기참조 | REJECT | **ACCEPT — 결함** |
| `origin: quoted` + `derivation` | REJECT | **REJECT** |
| 한국어 `label_en` | REJECT | **REJECT** |
| `approved` + `directives` | REJECT | **REJECT** |
| `drop_decision` | ACCEPT | **ACCEPT — 정답** |
| `entry_kind: record` + dangling `corrects` | REJECT | **REJECT** |
| `offset_h: 999` + `within_window: true` | REJECT | **REJECT** |
| `completion_proxy: 999` | REJECT | **ACCEPT — 결함** |

`record + corrects` 거부는 record가 `corrects:null`이어야 한다는 축만 증명한다. 실제 correction 행의 dangling 참조 해소는 여전히 검증기 몫이다.

스키마에서 표현할 수 없는 사항의 표기는 대체로 정직하다.

- 자기참조·비순환·깊이·1:1 역조건은 [material-spec.schema.json:5](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:5)과 [SPEC.md:2046–2060](/home/laptop/projects/patent-docent/docs/SPEC.md:2046)에 검증기 몫으로 적었다.
- 비율 산식·`corrects` 해소는 [metrics-row.schema.json:5](/home/laptop/projects/patent-docent/contracts/schemas/metrics-row.schema.json:5)과 [SPEC.md:1076–1077](/home/laptop/projects/patent-docent/docs/SPEC.md:1076)에 적었다.
- 비추적 처분표도 [47, 50, 52행](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-01-m06-enforcement.md:47)에서 “부분 해소/구현은 M1”이라고 한다.

따라서 “스키마가 못 막는 것을 숨겼다”는 결함은 아니다. 결함은 해당 검증기가 아직 없는데 [CLAUDE.md:77–83](/home/laptop/projects/patent-docent/CLAUDE.md:77)과 실증 도구 헤더가 M0.6 의미 집행 완료처럼 일반화하고, 정확한 재현식을 manifest에서 빼고도 13/13을 전체 증명처럼 제시한 데 있다.

## N1~N13 원장 전사 대조

원장 §1에는 `N1`, `N2`, `N-D11`, `N3`~`N13`이 있으므로 N-D11도 별도 대조했다.

| 항목 | 판정 | 원장 ↔ 하류 대조 |
|---|---|---|
| N1 | **충실** | [원장:21](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:21)의 P1′, 최소 발췌, 열람 목록+해시가 [CHARTER.md:127–129](/home/laptop/projects/patent-docent/docs/CHARTER.md:127), [SPEC.md:778–796](/home/laptop/projects/patent-docent/docs/SPEC.md:778)에 있다. 창작·누락 없음 |
| N2 | **충실** | 자동 검사 완전 제거, 고정 긍정형 문안, `new_terms` 비법률화가 [SPEC.md:658](/home/laptop/projects/patent-docent/docs/SPEC.md:658), [l0-format.yaml:350–356](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:350)에 있다 |
| N-D11 | **부분 충실** | D11은 정확히 4문장이고 시트가 기계 정본이다([CHARTER.md:161–164](/home/laptop/projects/patent-docent/docs/CHARTER.md:161)). 그러나 l0 주석·note의 숫자 사본이 남아 “값 사본 없음”은 완전하지 않다. 현재 값 표류는 없음 |
| N3 | **충실** | 편집 자산 정의, stop/pivot 적용, 문장 계수와 예외가 [l0-format.yaml:76–143](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:76), [185–197](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:185)에 있다 |
| N4 | **불충실** | 자문 전용 범위는 계약에 있으나 SPEC 2749행이 반대로 본문 검사를 말한다. 단독 `B+`를 의도적으로 허용해 “학점형 등급”을 완화했다. 재정 포인터도 비추적·비재정 D 파일이다 |
| N5 | **부분 충실** | 8개 필드와 공허 파생은 존재한다. 그러나 상태·위반 수와 ruleset 튜플 정합이 없어 보고가 거짓이어도 ACCEPT된다 |
| N6 | **불충실** | N·R 지위 표기는 정확하다. D계열은 재구성 문언·결정 요지 없이 포인터뿐이며, M0.6 처분 파일은 HEAD에 없다 |
| N7 | **충실** | M0 및 M0.5 원문이 보존됐다. 이번 감사 파일은 아직 수령 전 산출물이므로 현 시점 부재를 결함으로 세지 않았다 |
| N8 | **부분 충실** | 경계 규칙, `.venv`, 의존성 기록은 있다. 요구된 `pytest --version` 실출력 첨부만 누락됐다 |
| N9 | **불충실** | “원문 스팬만”이 `origin != derived`로 완화됐다. 자기참조·깊이 검증기는 없고 항목별 승인 집합도 대조하지 않는다 |
| N10 | **부분 충실** | 런 종류와 halt 문언은 있다. 방어층·템플릿 동결을 판단할 기계 좌표가 없어 3개 전제조건 전체의 기계 봉쇄는 성립하지 않는다 |
| N11 | **전사 충실** | 전량 무효·재생성, 버전/다이제스트 대조, 원장 표시 보존이 [SPEC.md:3564](/home/laptop/projects/patent-docent/docs/SPEC.md:3564)에 있다. 구현은 후속 모듈 예정이지만 문언 확대·완화는 발견하지 못했다 |
| N12 | **불충실** | 조기 보고·escalate·사유 분리는 충실하다. 그러나 원장이 정하지 않은 “후보 수 = 원천 도면 수” 산정식을 창작했다 |
| N13 | **충실(좁은 의미)** | 패밀리 필드 v0 미도입과 부트스트랩 예약이 [SPEC.md:4097](/home/laptop/projects/patent-docent/docs/SPEC.md:4097)에 있다. 단 이것이 M0 M15의 다른 D14 문제까지 해소하지는 않는다 |

## M0 원문 전건 대조

복원 원문 기준 실제 수는 BLOCKER 10 + MAJOR 11 + MINOR 1 = 22건이다.

| 원 지적 | 현행 판정 | 근거와 처분 진실성 |
|---|---|---|
| [B1 final-eyes](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:35) | **(a) 해소** | 거부 사유 3종, typed veto reason, 비관할 observations가 [SPEC.md:735](/home/laptop/projects/patent-docent/docs/SPEC.md:735), [769–796](/home/laptop/projects/patent-docent/docs/SPEC.md:769), [2501](/home/laptop/projects/patent-docent/docs/SPEC.md:2501)에 정의됨 |
| [B2 종속항 접지](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:37) | **(b) 부분 해소** | 권고 완화는 삭제됐고 빈 additions도 REJECT된다. 실제 1:1·역참조·전량 분해는 미래 검증기 몫. 최신 처분표의 “스키마 축 해소/나머지 부분”이 정확함 |
| [B3 no-rewrite](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:39) | **(b) 부분 해소** | halt 모순은 고쳤으나 네 우회가 [SPEC.md:2765–2767](/home/laptop/projects/patent-docent/docs/SPEC.md:2765)에 그대로 남음 |
| [B4 종속 구조](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:41) | **(b) 부분 해소** | 배열·전문은 해소. Markush·조건부·수단항 operator 및 도달 불능 `alternative-form` 잔존. D-02의 전면 “해소”는 과장 |
| [B5 수치 출처 결속](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:43) | **(b) 부분 해소** | `value_span` 계약은 생겼지만 날조 값이 실제 스키마를 통과. D-02 및 SPEC 2030행의 “해소”는 사실이 아님 |
| [B6 strip regex](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:45) | **(a) 해소** | 코드블록 정규식과 잔존 태그 안전망이 [SPEC.md:2175–2185](/home/laptop/projects/patent-docent/docs/SPEC.md:2175)에 있음 |
| [B7 ship 재-strip](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:47) | **(a) 해소** | ship copy-only와 양방향 byte equality가 [SPEC.md:982–1006](/home/laptop/projects/patent-docent/docs/SPEC.md:982)에 있음 |
| [B8 접근 계약](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:49) | **(a) 해소** | 쓰기 소유와 읽기 행렬 양쪽이 [SPEC.md:1135–1196](/home/laptop/projects/patent-docent/docs/SPEC.md:1135), [3580–3605](/home/laptop/projects/patent-docent/docs/SPEC.md:3580)에서 정합 |
| [B9 D11 슬롯](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:51) | **(a) 해소** | 편집 자산 하한·문장 상한·slot placement가 시트와 l0 규칙으로 존재 |
| [B10 gate-law 계약](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:57) | **(b) 부분 해소** | forbidden은 폐지됐고 whitelist 형태는 통일됐다. CP1 승인 단계는 스키마가 강제하지 않아 여전히 불일치 |
| [M11 word budget/hook](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:53) | **(a) 해소** | word budget은 자문으로 강등되고 슬롯별 길이는 시트로 확정([l0-format.yaml:336–342](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:336)) |
| [M20 new-term 공허 통과](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:55) | **(a) 해소** | N2가 검사 자체를 제거하고 retired에 등재([l0-format.yaml:350–356](/home/laptop/projects/patent-docent/contracts/l0-format.yaml:350)) |
| [M12 검사 사각지대](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:59) | **(b) 부분 해소** | 값·포인터 일부는 보수. 원천 인벤토리·트리 수렴은 [SPEC.md:4493–4502](/home/laptop/projects/patent-docent/docs/SPEC.md:4493)에 생존 |
| [M13 payload 불변](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:61) | **(c) 생존** | [SPEC.md:4504–4514](/home/laptop/projects/patent-docent/docs/SPEC.md:4504)가 현행 결함을 그대로 인정 |
| [M14 재료 수치 문법](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:63) | **(c) 생존** | [SPEC.md:4516–4524](/home/laptop/projects/patent-docent/docs/SPEC.md:4516)가 현행 결함을 그대로 인정 |
| [M15 historian 계약](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:65) | **(b) 부분 해소** | N13은 패밀리 미도입만 재정. 서지 구조와 `drop_signal` 의미 불일치는 생존 |
| [M17 무도면 경로](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:67) | **(a) 해소** | N12가 정상 경로 제외·조기 escalate를 명시적으로 재정. 새 대체 모드를 만들지 않는 것이 결정 |
| [M21 asset_path 변이](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:69) | **(a) 해소** | 동결본 영구 null, manifest 단일 정본이 [SPEC.md:1549–1554](/home/laptop/projects/patent-docent/docs/SPEC.md:1549)에 명시 |
| [M16 round-trip](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:71) | **(b) 부분 해소** | raw frontmatter·공백·빈 줄 문제는 해소. 복수 문장 한 줄의 per-sentence tag 집행은 미완 |
| [M18 score lint](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:73) | **(b) 부분 해소** | 별점·N/100·문맥부 학점은 검출. 단독 `B+` 통과, 범위 모순, 실행기 부재 |
| [M19 weakest_tweet](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:75) | **(c) 생존** | 결정론화됐지만 원문이 비판한 바로 그 비인과 규칙을 유지 |
| [MINOR22 참조 오류](/home/laptop/projects/patent-docent/docs/lessons/2026-08-17-sol-audit-m0-full.md:77) | **(a) 해소** | K1~K7이 exit 0이고 현재 확인된 절 참조 오류 없음 |

요약하면 M0 22건 중 완전 해소 9건, 부분 해소 8건, 생존 5건이다.

## 계약 ↔ SPEC ↔ CHARTER 정합

- D11은 정확히 4문장이다. 기계가 소비하는 형식 수치의 정본도 `contracts/format-parameters.yaml` 하나다. 다만 l0 주석·note와 SPEC 역사 절에 동일 숫자 사본이 남아 있어 “사본 0”은 아니다. 현재 drift는 발견되지 않았다.
- `l0-format.yaml`에서 삭제된 활성 블록이 대체물 없이 증발한 사례는 없다.

  - weighted length, 슬롯, 길이, 트윗 수, stop-shape 수치 → 형식 파라미터 시트.
  - stop-shape 술어와 문장 계수 → l0에 유지.
  - word budget → 시트의 자문 임계와 retired 기록.
  - new-term budget → N2에 따라 명시적 retired + 펜 긍정형 지침.
  - forbidden lexicon → R7에 따라 speech-act 계약으로 대체·폐지 기록.

- 신설 계약 4종의 계약 라인은 파일과 문서 양방향으로 일치한다.

  - `format-parameters/v0`
  - `run-kinds/v0`
  - `score-lint/v1`
  - `verdict-check-row/v0`

  [SPEC.md:3418–3438](/home/laptop/projects/patent-docent/docs/SPEC.md:3418)과 각 파일 선언이 일치하며 K3도 통과했다. 의미 집행 결함은 위 B-03, M-02, M-03과 별개다.

- SPEC §4.8 자기매칭 격리 4항은 신설 도구·표본의 좁은 구조 요건으로는 지켜졌다.

  - `check_spec_refs.py`는 allowlist와 금지 접두를 사용하고 위반 시 exit 2([55–75행](/home/laptop/projects/patent-docent/tools/check_spec_refs.py:55)).
  - 격리 거부 테스트가 있다([test_tools_check_spec_refs.py:160–182](/home/laptop/projects/patent-docent/tests/test_tools_check_spec_refs.py:160)).
  - schema enforcement 도구는 탐지 리터럴 없이 스키마만 적용한다([check_schema_enforcement.py:16–31](/home/laptop/projects/patent-docent/tools/check_schema_enforcement.py:16)).
  - 별점 변조 리터럴은 실제로 [mutated memo 12행](/home/laptop/projects/patent-docent/ledgers/regression/mutated/rc-0003-star-rating/memo.md:12)에만 있다.

  다만 score-lint 실행기가 없으므로 “격리된 표본이 실제 detector로 검출된다”는 단계는 아직 증명되지 않았다.

## 총괄 재량 E20~E27, G9, G10

| 재량 | 판정 |
|---|---|
| E20 시트 파일명·5키 구조 | 재정이 구조를 정하지 않았으므로 범위 내 |
| E21 미지정 항목 tag 배정 + director 표시 | 모든 항목에 태그를 요구한 N-D11을 이행하기 위한 감사 가능한 선택. 범위 내 |
| E22 whitelist 정규식 형태 | 단일 형태를 만드는 공학 선택. 범위 내. 단 CP1 집행 누락은 별도 M-05 |
| E23 `frontmatter_raw` + thread.json 승격 | byte round-trip을 가능하게 하는 최소 구조. 범위 내 |
| E24 final-eyes brief 파일 | N1의 발췌본 요구를 실물화. 범위 내 |
| E25 `adjudicated_in` | 미재정 앵커 차단의 기계 좌표. 범위 내 |
| **E26 `ceil(n/2)`** | **범위 초과/미재정 완화.** M0.5 M-04를 Owner 확인 없이 닫음 |
| E27 검사 ID 3종 | 이름을 정한 공학 선택. 범위 내 |
| **G9 v0 breaking change를 minor 처리** | **범위 초과.** 기존 major 규율의 예외를 스스로 창설 |
| G10 `annotated-internal` 비계수 | N3가 열거한 crop/self-authored 두 종류에 맞춘 것. 범위 내 |

이 밖에 `전시물 후보 = 원천 도면 수`는 목록에조차 없는 추가 재량이며 N12를 넘어섰다.

따라서 M0.6은 문서·경로·메타스키마 수준의 검사는 통과하지만, 의미 불변식과 원장 충실성 수준에서는 PASS할 수 없다. 특히 대상 커밋의 처분 기록 누락, A군 정확 재현 두 건의 ACCEPT, 거짓 판정 행의 ACCEPT, 날조 수치의 ACCEPT는 후속 구현으로 미룰 수 있는 표현상 문제라기보다 현재 “집행 완료” 주장 자체를 반증한다.
