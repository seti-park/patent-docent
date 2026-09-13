# D-20260913-01 — T40 ④ 검수원(지표 추출기 9모듈) 「가설」 강등 출하 (총괄 저작 · 재정 T56 ④ 경로 · 재정 T58 ① 집행)

**지위.** 총괄 문서(원장 아님). 재정 T56 ④ 「47차 뒤에도 『원본 승인: 아니오』면 『가설』 강등 출하(U 잔여·공리 목록·위반 목록 동봉 · M10 이진 출하 판정)」을 **재정 T58 ① 로 46·47차 없이 지금 집행**한다. 이 문서가 그 출하물이다 — 검수원의 코드·설계 메모·증거는 아래 좌표의 바이트 그대로이며 여기에는 사본을 두지 않는다.

## §1 출하 상태 한 줄

> **검수원(생산 9모듈 · 수리 후 지문)은 「§5′.21 공리 아래 연결된 성질 I 를 모든 Γ 실행에서 만족한다」는 증명이 닫히지 않은 상태로 출하된다. 상태 = 가설.** 원본 승인 = **아니오**(20차 · 45차 【직접】 재현 일치). 용도 = 실측 기반 도구(구동기 · 영수증 · 재조립 대조 · IO 결함 재실측 규약 T42·T43). **좌석 비교 실측 용도(T40 ④ 3 런)는 재정 T58 ① 로 소멸.**

## §2 좌표(바이트 정본)

| 대상 | 좌표 | 지문 |
|---|---|---|
| 저작 작업장 | `~/projects/workspaces/pd-author-t40v33` HEAD `63f5de7`(20차 최종 wip · `9df5520` ref · `b7f8e47` 19차) | — |
| 게이트 사본(46차 미발생 · 사료) | `~/projects/workspaces/pd-m1b-t40-v50`(detached `63f5de7` · `gate/` 27 · `src/`) | — |
| 설계 메모 v50 | `work/T40-MEASURE-DESIGN.md` | 295,721 B `89fa008c79bbd8c2` |
| 공리 절 §5′.21 | 메모 `### §5′.21 `~`## §5 ` | 16,885 B `4a577e0db9679fbf` |
| 생산 9모듈(수리 후) | `work/t40_{metrics,replay,receipts,drive,resources,flow,consume,envelope,excerpts}.py` | `3d7ee3377fdb2fe4` `e8ea6c3f86a9306a` **`b14c4e9257369fd9`**(receipts · 수리 전 `56e5f41aad6a1f1d`) `a039bf9ff5b63cf7` **`619946aead040817`**(resources · 수리 전 `b94e549bf7407527`) `2a1a0dfc6dd2e0c0` `a99bb3aac7e95d29` `62daa44fa917a11a` `06de01e7036aa75d` |
| 20차 보고·증거 | `work/R20-REPORT.md`(첫 줄 「원본 승인: 아니오」) · `R20-U5-DERIVATION.json`(1,016 단계) · `R20-U5-EVIDENCE.json`(blocking 3 · sites 62) · `R20-AXIOMS.json` · `R20-AXIOM-USE.json` · `R20-UNRESOLVED.md` · `R20-REPAIR-{BEFORE,AFTER}.json` · `R20-REPAIR-DIFF.md` · `R20-FINGERPRINTS.json` · `R20-REGRESS-OBSERVED.md` · `R20-L-SEARCH.json` | `R20-ARTIFACTS.tsv` |
| 20차 레인 | `~/projects/workspaces/pd-lanes/fable-m4-t40v33-r20/`(SPEC `801d54d05b12aaa7` · FINAL 21,278 B `72ac0caa7e49706b` · 세션 `95596447-b9da-4271-8ecd-67aa9eef1ef8`) | — |
| 판정 원문 | `docs/lessons/2026-09-06-*t40-measure*.md` ~ `2026-09-12-fable-m1b-t40-measure-v49.md`(45판) | — |

## §3 동봉 ⑴ — 공리 목록(§5′.21 · 15)

| ID | 무엇 | 원본 유도 인용 단계 |
|---|---|---|
| `AX-PY-01` 예외 결속·bare raise | 파이썬 의미 | 492 |
| `AX-PY-02` try/finally 순서·대체 | 〃 | 11 |
| `AX-PY-03` 대입·속성 저장·frozen dataclass | 〃 | 3 |
| `AX-PY-04` 이름 조회 | 〃 | 491 |
| `AX-PY-05` ContextVar | 〃 | 2 |
| `AX-PY-06` list.append · Enum · dataclass 생성자 | 〃 | 3 |
| `AX-PY-07` 데코레이터·wraps | 〃 | 491 |
| `AX-PY-08` 호출·프레임 전파 | 〃 | 504 |
| `AX-PY-09` generator | 〃 | 1 |
| `AX-PY-10` open() 파일 객체 속성 조회 | 〃 | 10 |
| `AX-PY-11` with/contextmanager | 〃 | 1 |
| `AX-PY-12` or/상수/if 스코프 · `AX-PY-13` def/무인자 호출/프레임 의존 이름 | 부속 규칙(재작성 증서) 전용 · **원본 증명 인용 0** | 0 |
| `AX-ENV-01` | 환경 공리 = 재정 T52 문언 그대로 | 2 |
| `AX-PROG-01` | **프로그램 명제** — I-S 두 프로필(legacy4/current5/API/B) 계산 동치 · 증명되지 않음 · 유한 증인(R10 profile 동치 · S73·S74 · 런 20 · 런타임 10)만 | 1 |

정의 10 = DEF-PARSE-SITE · DEF-CONSUMER-SITE · DEF-GATED-REGION · DEF-BUSINESS-RESULT(T53 ① + T56 ① 「어느 한쪽」) · DEF-FIRST-ERROR · DEF-CONTROL-FLOW(정당화 13 / 위반 5) · DEF-AST-EQUAL · DEF-BOUNDARY · DEF-OWNER · DEF-THUNK. 정직성·최소성·정의 적절성은 **게이트 심사를 받지 않았다**(46차 미발생) — 이 목록은 저작자 주장 + 총괄 기계 대조(`R20-AXIOM-USE.json` 인용 0 공리 없음)까지다.

## §4 동봉 ⑵ — U 잔여

| 계수 | 새 대상 | 옛 대상 | 뜻 |
|---|---:|---:|---|
| `U_r`(포함 셈) | 6 | 6 | U1~U6 전부 미해결 · 부분 차감 0 |
| `U_r`(T56 ③ 부속화 단위 U1·U2·U6 제외 셈) | 3 | 3 | 저작자 병기 · 게이트 판단 없음 |
| `B_r`(필수 양성 11 = 원본 + 런타임 10) | 11/11 | 11/11 | 원본 거부(U5) · 옛 셈 16/16 |
| `L_r` | 0/7(공허) | 0/7 | 승인 경로 없음 |
| 유도 | 1,013 / 1,016 | — | I-C 33 자리 · I-P 190 자리 · I-S(가정) 성립 · 전제 ⒠ 불성립 |

U5 를 막는 것 = 전제 ⒠ `FIRST-ERROR-PRESERVATION` 의 부조건 `P-THUNK-HANDLERS`(§5 위반 목록). 41~45차 비감소 이력 = 6/0/2 · 6/0/1 · 6/0/7 · 6/16/0 · 6/16/0 · 20차 6/11/0.

## §5 동봉 ⑶ — 위반 목록(T56 ① 「어느 한쪽」 기준 · 원오류 객체를 바깥 결과 전에 대체하는 자리 62 · 전수 = `R20-U5-EVIDENCE.json` `blocking[0].sites`)

| 부류 | 수 | 자리(모듈:행) |
|---|---:|---|
| wrap(원오류를 다른 예외로 감싸 던짐) | 12 | receipts `:119 :437 :476 :604 :660 :666` · replay `:192` · resources `:251 :341 :368 :383` · consume `:263` |
| wrap-after-capture(잡은 뒤 포장) | 7 | resources `:291 :299 :308 :393 :437` · consume `:377` · drive `:519` |
| disposition(판정 값·신호 `die/bad/Rejected/sys.exit` 로 종결 · failures 에 raw 남음) | 38 | metrics 25(`:114 :119 :161 :332 :346 :347 :361 :364 :366 :379 :393 :438 :467 :497 :509 :514 :518 :543 :729 :745 :769 :791 :812 :851 :911`) · replay 7(`:224 :301 :307 :344 :345 :346 :347`) · drive 6(`:212 :231 :629 :640 :642 :728`) |
| control-flow(정당화 표 밖) | 5 | receipts `_git:97` `manifest_verify:640` · replay `_git:63` `replay:355` · drive `_pointer_and_gate:302` |
| 그 밖(62 밖 · 실행 재현) | 1 | flow `entry:353` 환경 복원 실패 → 호출자 `EnvironmentFailure(__cause__=raw)`(T/T/F) |

실행 재현 8 = `R20-L-SEARCH.json`(총괄 사본 재실행 10/8 일치). 재정 T56 이 허가한 두 자리(`resources.entry:439-441` · `receipts.io_boundary:163-173`)는 **수리됨**(세 `is` 3/3 · `R20-REPAIR-AFTER.json`). 나머지 62 의 처분(전부 수리 / 「처분 투영」 독해 / 유지)은 **재정 없이 남는다**(T57 소멸) — 이 도구를 다시 증명 대상으로 올릴 때의 첫 안건이다.

## §6 알려진 결함·관측(수리 예약)

| ID | 무엇 | 처분 |
|---|---|---|
| **C98** | 두 자리 수리 뒤 `t40_replay._reconstruct:347` 의 `except OSError`(불변 모듈)가 자료 역할 원오류를 「환경 IO · 검수 불능」으로 분류 → 처분이 부적격→검수 불능으로 바뀜 · 회귀 C98 FAIL | **알려진 결함 · 수리 = 이 도구를 다음 계측에 쓰기 전 M3 1건**(역할 기반 분류 · `t40_role` 부기 또는 `R.disposition`) · 발주자 오류 248 |
| **S81 · S14 grid 22** | R12 역사 관계표 19 가 두 수리 함수의 수리 전 사건 지문을 키로 삼음 | 재키 파일 1건(사료 무변경) · 같은 M3 |
| 회귀 207 | PASS 195 / FAIL 12 = C98 · S14 · S48 S65 S68 S69 S75 S76 S80 S81 S83 S85(뒤 열 건 = 원본 승인 요구 · 증인 본체는 실행됨) | 원본 승인 요구는 「가설」 상태에서 FAIL 이 정직한 값 |
| `AX-PY-12·13` | 부속 전용 공리(원본 인용 0) | 정직성 심사 미실시 |
| 규율 이탈 | 20차 회귀 묶음 10·12 가 10분 상한 초과(하네스 배경 → 같은 세션 회수) | 기록 |

## §7 이 출하가 말하지 않는 것

- 검수원이 어떤 실행에서도 원오류를 보존한다는 것 — **말하지 않는다**(§5 62 자리).
- I-S 두 프로필 동치가 참이라는 것 — 가정이다(`AX-PROG-01`).
- 공리 15 가 정직·최소하다는 것 — 게이트 심사 없음.
- 실측 계약(T1~T4 신뢰 전제 · P1~P7 · 회귀 195)이 깨졋다는 것 — **말하지 않는다**. 195 는 그대로 서고 구동기·영수증·재조립 대조·IO 결함 재실측 규약은 그대로 쓰인다.

## §8 M10 이진 출하 판정

기준(재정 T56 ④ 문언) = ⓐ U 잔여·공리 목록·위반 목록이 **동봉**되어 있는가 ⓑ 「가설」 표기가 **정직**한가(출하가 말하지 않는 것을 말하지 않는가 · 원본 승인 「아니오」가 첫 줄에 있는가) ⓒ 좌표가 실측 바이트를 가리키는가. 판정 = `좌석 M10` claude-fable-5-1 low · CLI 단발 · 아래 추기에 원문 그대로.

**M10 판정 = PASS**(2026-09-13 12:0x · `claude -p --model claude-fable-5-1 --effort low` · 세션 `79bee273-212c-4ccc-addf-ee60afed430b` · 3턴 · $0.49 · 도구 Read + sha256sum/head 만 · 프롬프트 = 스크래치 `m10-prompt.md` · 기준 ⓐⓑⓒ 위와 동일). 아래 절은 판정자 저작이며 한 글자도 고치지 않는다(규율 10).

### M10 판정 원문 (claude-fable-5-1 low · 이 아래는 판정자 저작)

```
VERDICT: PASS
ⓐ 동봉: 예 — §3 공리 목록 표(15 항 · AX-PY-01~13 · AX-ENV-01 · AX-PROG-01) · §4 U 잔여 표(U_r 6/3 · B_r 11/11 · L_r 0/7 · 유도 1,013/1,016) · §5 위반 목록 표(62 자리 · 모듈:행 열거) 셋 다 표로 실려 있다.
ⓑ 정직: 예 — §1 「원본 승인 = **아니오**」 · §1 「증명이 닫히지 않은 상태로 출하된다. 상태 = 가설」 · §7 「검수원이 어떤 실행에서도 원오류를 보존한다는 것 — 말하지 않는다」 · §3 「정직성·최소성·정의 적절성은 게이트 심사를 받지 않았다」 · §6 「원본 승인 요구는 「가설」 상태에서 FAIL 이 정직한 값」. 증명되지 않은 것을 증명된 것처럼 적은 문장 없음.
ⓒ 좌표: 예 — `cd ~/projects/workspaces/pd-author-t40v33/work && sha256sum T40-MEASURE-DESIGN.md t40_receipts.py t40_resources.py | cut -c1-16,65- ; head -n1 R20-REPORT.md` → `89fa008c79bbd8c2 T40-MEASURE-DESIGN.md` · `b14c4e9257369fd9 t40_receipts.py` · `619946aead040817 t40_resources.py` · `원본 승인: 아니오`
```

