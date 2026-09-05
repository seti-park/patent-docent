# 독립 감수 원문 — M1b 설계 도전 3차(gpt-6-astra medium · 파일럿 런 3/3) · 재감사 3 발주문(라운드 RF + T35 · RG-*) · 판정 REVISE

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`bin/sol-audit.sh finish` 가 남긴 `FINAL` · sha256 `6d1ec91a4c8b3d0ea8b04d1f175c80a61e7a6e22c161d41961f1aacb1cf98fb6` 와 `---` 아래가 동일 · 17310 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-audit3/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` medium · 파일럿 런 3/3**(1차 11:53 REVISE 7 · 2차 12:09 REVISE 6). **두 번 기동** — 첫 기동(12:50:36)은 세션 재개 때 부모 프로세스가 종료되어 2분 만에 죽었다(EXIT 마커 없음 · FINAL 0 B · 사료 `EV.dead-1`·`STATUS.dead-1`) → `setsid nohup` 으로 분리해 재기동(13:05:22 → 13:11:51 · EXIT=0). **USAGE(재기동분) = input 881,984(cached 797,824) · output 10,505(reasoning 495)** · 약정 ⓒ 한도 안. 사본 = 홈 fs `~/projects/workspaces/pd-m1b-audit3`(clone · detached `a48a97f` · 마커 3검증 일치 · `bundle/` = 핀 채운 재감사 3 발주문 · 3차 발주문 · 4차 v2 · 3차·4차 레인 보고). 읽기 전용 · pytest·관문 금지(jsonschema 검증 · git 조회 · grep 허용 — manifest 50건 전건 JSON 검증을 실제로 했다).

**판정 = REVISE · 지적 6건(MED 4 · LOW 2) · 기각 0.** 대상은 감사자에게 넘길 **재감사 3 발주문**이었고 여섯 전부 발주자(총괄) 귀책. **MD-1**(MED): 발주문이 재현표를 §16, 레인 보고를 §17 로 지정 — 실물은 §18(재현표)·§19(3차 보고)·§20(4차 보고 = `final-4.txt` · 정규화 동일 실측) · 기록 커밋 반경에 `RULINGS-LEDGER.md` 누락. **MD-2**(MED): Q5 가 이미 4차 v2 로 대체된 3차 발주문을 독립 수락 기준으로 다시 심판하게 함 — 유효 발주(3차 + v2 대체 조항)를 심판하고 보존된 구 문언은 정정 누락일 때만 신규로 세야 함. **MD-3**(MED): RF-1 변조를 「허용값 조건 두 곳 삭제」로 지정했으나 현행 구현은 세 자리(singleton 선별 · 규격 밖 계수 · 전건 일치). **MD-4**(LOW): 「형태 17종」·「25종」 낡은 계수 잔존(현행 = 고유 ID 30사례) · 「아무 입력」의 분석 범위(`reported_by` JSON 값 · 항목은 객체) 미명시 · 표본 30 ≠ 완비 증명. **MD-5**(MED): 발주문이 T22 파일을 「주석만」으로 전제했으나 RF 커밋에는 다른 시험 두 줄(`deepcopy(schema)` → `deepcopy(dict(schema))`)이 들어 있다 — 발주자의 파일 전체 grep 수락 조건이 유도한 기계 정리(T22 함수 AST 동일 · 파일 AST 상이) · MC-5 검사는 행위시법 함수의 데이터 흐름으로 한정해야 함. **MD-6**(LOW): `96f7582` 는 「문서 넷」이 아니라 감사 원문 반입 포함 다섯 파일. 그 밖 — 「커밋(부모)」 열에 부모 미기재 · SUMMARY 전체 행(`schemas=5`) 인용 권장 · T36 「1:1」은 항목별 지정 좌표 대응(마커 9곳 · 항목 11)으로 읽어야 오탐 없음 · `<RF>`·`<T35>` 치환 표지는 핀으로 채워 제공 · PASS 정의에 partially/open·[미검증] 처리 기준 명시 권장 · 폐쇄 판별 대응표(RF·MB·MC·T35 전건 「가능」).

지적 열거 = MD-1, MD-2, MD-3, MD-4, MD-5, MD-6

처분은 `docs/decisions/DISPOSITIONS.md` 에 행으로 서고 사유 전문은 `D-20260903-04-t31-t32.md` **§21** 에 있다. **전부 수용** → 재감사 3 발주문 정정(drafts · 핀 재기재) → 재감사 3 발주. **약정 강등 판정 = 없음**(ⓐ 해당 없음 · ⓑ 기각 0 · ⓒ 한도 안 · ⓓ 세션 종료로 인한 사망은 벤더 사유 아님). **파일럿 3/3 종료 — 다만 그 사이 다른 세션이 4런 실측으로 M1b 를 `astra high` 로 확정했다(ROUTING v2.1 §3 M1b · L-052 ⑩ · 「medium 은 P1 급 1건을 두 번 놓침」). 이 리포의 세 런은 당시 정본(medium)을 따랐고, 다음 M1b 부터 high · 약정 블록 불요.**

---

# 도전 원문 (gpt-6-astra medium · M1b 3차 · 이 아래는 도전자 저작)

**마커 3검증 실출력 + 정본 HEAD**

```text
$ pwd
/home/laptop/projects/workspaces/pd-m1b-audit3

$ cat .audit-sandbox
path=/home/laptop/projects/workspaces/pd-m1b-audit3
pin=a48a97f163aa4827e6954e242485822fa6891ef5
order=M1B-audit3-20260905
disposable=true

$ git rev-parse HEAD HEAD^{tree}
a48a97f163aa4827e6954e242485822fa6891ef5
7eb112e134866704585f449f10586b113cdd75d9

$ git -C /home/laptop/projects/patent-docent rev-parse HEAD
a48a97f163aa4827e6954e242485822fa6891ef5
```

`path=pwd`·`pin=HEAD`·`disposable=true` 모두 일치한다. 정본은 HEAD만 조회했다. 아래 JSON 검증은 독립 실측이며, pytest·관문 결과는 실행하지 않고 기록과 코드만 대조했다.

**판정 = REVISE · 지적 6건(MED 4 · LOW 2).** 끊긴 곳은 재현·보고 좌표, 폐기된 3차 지시의 적용 범위, 변조 위치 지정, “주석만”이라는 사실 전제다.

**MD-1 · MED — 재현표·레인 보고의 좌표가 틀려 Q4의 동등성 요구를 만족할 수 없다**

좌표: [A:10·17~19·23·35](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:35).

근거 실출력:

```text
724:## §16 M1b 설계 도전 ... MB-1 ~ MB-7 의 처분
744:## §17 M1b 설계 도전 2차 ... MC-1 ~ MC-6 의 처분
763:## §18 라운드 RF + 재정 T35 집행 회수 · 총괄 재현 · 병합
970:## §20 SOL CODER REPORT ... 4차 정정(PASS) ... final-4.txt

SECTION20_NORMALIZED_EQUAL True
FINAL4_SHA256 a40c2bdaec62e70d6b05f6409f5508015cc4ba30357b55ec49e09da4f61b82c3
```

A는 §16을 재현표, §17을 레인 보고로 여러 번 지정하지만, 같은 A:21에서는 §18을 올바르게 가리킨다. §17과 레인 보고의 동일성을 요구하면 정상 산출도 불일치한다. 기록 커밋의 실물 반경에는 A의 표가 빠뜨린 `RULINGS-LEDGER.md`도 있다.

검증 경로: D-04 절 제목 → `a48a97f --stat` → §20 본문과 `bundle/final-4.txt`의 앞뒤 공백 정규화 비교. 외부 `final.txt`의 존재·내용은 조회하지 않았다.

고치는 문안 한 줄: **“재현표는 D-04 §18, 3차 보고는 §19, 최종 4차 보고는 §20=`final-4.txt`로 대조하며, 기록 커밋 반경은 D-04·HANDOFF·RULINGS-LEDGER 세 파일이다.”**

**MD-2 · MED — Q5가 이미 대체된 3차 지시를 독립적인 현행 수락 기준으로 다시 심판한다**

좌표: [A:32·36](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:36), [4차 v2:3](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/SPEC-round-rf-t35-fix4.md:3).

근거 실출력:

```text
4차 v2:
이 문서가 3차 발주문과 충돌하면 이 문서가 3차 항목을 대체한다

3차:
새 시험은 수리 전 ... 판본에서 붉고 수리 후 초록
cases=50 REJECT_OK 34/34 ACCEPT_OK 15/15
전후 실출력이 갈린다(등가 증명 항목 없음)

A Q5:
발주문 SPEC-round-rf-t35.md 자체
차별 대조(A ⓐ~ⓓ · 변조 H · B ⑴⑵③)가 개정판 ⒀ 에 맞고 ...
```

A:21·Q3에는 v2가 등장하지만 Q5에는 **합성된 유효 지시와 보존된 구 문언의 구별**이 없다. 문자 그대로 답하면 이미 MB·MC로 처분하고 대체한 오류를 다시 RG 지적으로 낼 수 있다. 역사적 오류를 감사 대상으로 읽는 것과 현행 미폐쇄로 세는 것은 구분해야 한다.

검증 경로: 3차 A②·공통 §4와 v2 F1·F4·F5·우선 조항을 Q5에 대입.

고치는 문안 한 줄: **“Q5는 3차판에 4차 v2의 대체 조항을 적용한 유효 발주를 심판하고, 보존된 구 문언은 정정 누락이 있을 때만 신규 미폐쇄로 센다.”**

**MD-3 · MED — RF-1 변조를 ‘두 곳 삭제’로 지정하지만 현행 구현에는 세 곳이 있다**

좌표: [A Q1ⓐ:28](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:28), [렌더:484](/home/laptop/projects/workspaces/pd-m1b-audit3/engine/render/material_spec_md.py:484).

근거 실출력:

```text
A: 허용 실행값 조건 두 곳 삭제

4차 v2 F5:
허용값 검사는 singleton 선별 · 규격 밖 계수 · 전건 일치 세 자리에 있다

final-4.txt:
singleton 선별·규격 밖 계수·전건 일치의 허용값 검사 세 자리 삭제
```

실제 렌더도 `split_reports`의 `all`·규격 밖 계수의 `any`·전건 일치의 `all` 세 자리다. 어느 둘을 지울지에 따라 변조가 달라진다. 시험이 붉더라도 레인이 주장한 세 자리 변조를 재현했다는 증거가 되지 않는다.

검증 경로: Q1ⓐ → v2 F5 Aⓐ → `material_spec_md.py` 세 술어 → 4차 보고 변조표.

고치는 문안 한 줄: **“허용값 검사 세 자리(singleton 선별·규격 밖 계수·전건 일치)를 명시해 삭제하고 I05·I06의 결과를 각각 보고한다.”**

**MD-4 · LOW — 형태표 17종·25종이 현행 30사례 지시와 함께 남아 있다**

좌표: [A:21·28~29](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:28).

근거 실출력:

```text
A:21 형태표 30사례가 사례별로 식별되는가
A:28 형태 17종 표 ... 다시 돌려 전후 대조
A:29 M1b 형태표 25종

SHAPE_CASES 30 UNIQUE 30
```

D-04 §16은 이미 전임 “17종”이 구체 16개임을 기록했고, §17 MC-6은 25→30을 정정했다. 현행 시험은 고유 ID 30개다. 또한 “아무 입력”이라는 요구는 `reported_by`가 JSON 값이고 미분류 항목은 객체라는 분석 범위를 명시해야 한다. 30개 표본 자체가 전체 JSON 공간의 완비 증명은 아니다.

검증 경로: 전임 형태표·MB/MC 처분·v2 F2와 시험의 `ATTRIBUTION_SHAPE_CASES` AST 집계. 시험 함수는 실행하지 않았다.

고치는 문안 한 줄: **“현행 형태표는 v2 F2의 고유 ID 30사례이며, 객체 항목의 reported_by JSON 값 공간에서 G/I/T/A 및 I→T의 우선·완비를 별도로 논증한다.”**

**MD-5 · MED — ‘주석만’ 반경에 코드 변경 두 줄이 들어갔고, 원인은 과도한 grep 수락 조건이다**

좌표: [A §1:17·Q3:34](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:17), [4차 보고:33](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/final-4.txt:33).

근거 실출력:

```diff
- no_then = copy.deepcopy(schema); ...
- retry_then = copy.deepcopy(schema); ...
+ no_then = copy.deepcopy(dict(schema)); ...
+ retry_then = copy.deepcopy(dict(schema)); ...
```

```text
final-4.txt:
지정 grep을 위해 기존 T22 변조 생성 두 줄을 의미가 같은
deepcopy(dict(schema))로 기계 정리.

T22_FILE_AST_EQUAL False
T22_FUNCTION_AST_EQUAL True
```

A의 T22 **대상 함수** 코드 무변경 주장은 맞다. 그러나 3차의 해당 **파일 반경은 주석만**이고, 실제로는 다른 시험 함수가 바뀌었다. v2의 `tests/` 전체 `deepcopy(schema)` 무일치 요구가 행위시법과 무관한 정상 변조 생성까지 건드리게 했다.

Q3는 이를 잡을 수 있다. 따라서 Q3의 부재가 아니라, **A의 요약이 감사자가 잡아야 할 예외를 숨기고 있다는 사실 전제 오류**다. 메모리 복원 금지를 문자열 우회로 만족시키는 방식도 별도로 감사해야 한다.

검증 경로: RF 커밋 전체 diff → 3차 주석 한정 반경 → v2 수락 grep → 레인 보고 → 파일 전체·T22 함수 AST 각각 비교.

고치는 문안 한 줄: **“T22 대상 함수는 주석만 변경됐으나 다른 시험의 dict(schema) 두 줄도 포함됐으므로 Q3에서 반경·필요성을 판정하고, MC-5 검사는 행위시법 함수의 실제 데이터 흐름으로 한정한다.”**

**MD-6 · LOW — `96f7582`의 ‘문서 넷’이라는 커밋 반경 계수가 틀리다**

좌표: [A:21](/home/laptop/projects/workspaces/pd-m1b-audit3/bundle/AUDIT-ORDER-round-rf-t35.md:21).

근거 실출력:

```text
$ git diff-tree --no-commit-id --name-only -r 96f7582
HANDOFF-NEXT.md
docs/decisions/D-20260902-02-t26-design-challenge.md
docs/decisions/D-20260903-04-t31-t32.md
docs/decisions/DISPOSITIONS.md
docs/lessons/2026-09-05-opus-audit-round-re.md
```

다섯 파일이다. 감사 원문 반입까지 포함한 전체 커밋 반경과 정정 문서 묶음을 구별해야 한다.

검증 경로: 지정 커밋의 파일 목록 직접 조회.

고치는 문안 한 줄: **“96f7582는 감사 원문 반입을 포함한 문서 다섯 파일이며, 그 안에 §13·골격·HANDOFF 정정과 처분 기록이 있다.”**

**사실 전제 전수 대조**

| 항목 | 실측·판단 |
|---|---|
| 커밋·부모 | `2d01e91 ← ecd4ce7`, `4bb2579 ← 2d01e91`, `a48a97f ← 4bb2579`. A의 SHA는 맞지만 “커밋(부모)” 열에 부모는 기재하지 않았다. |
| HEAD·트리 | A의 핀과 일치. 종료 때 정본 HEAD도 동일. |
| RF 반경 | 3파일, `171 insertions / 63 deletions`. 주석 한정 예외는 MD-5. |
| T35 반경 | 6파일, `287 insertions / 15 deletions`. 신설 accept·reject·manifest·스키마·시험·SPEC 모두 존재. |
| 기록·절 번호 | §15 RF, §16 MB, §17 MC, §18 재현, §19 3차, §20 4차. MD-1. |
| HANDOFF | 18차는 :3·:10에 실재. 감사 중 정본 커밋 금지는 :11에도 명시. |
| 스키마 계수 | 50사례=`accept 15 + reject 33 + validator-scope 2`, 스키마 5개. 경로 부재 0. |
| SUMMARY | 전체 기대 행은 아래와 같다. A Q2의 인용은 맞는 접두부지만 전체 행 인용 요구는 보강할 수 있다. |
| 시험 수 | 형태표는 AST 실측 30개·고유 ID 30개. `55 passed`, 전체 `810 passed` 두 모드는 §20의 **보고값**이며 이번 실행 확인값은 아니다. |
| 실런 | 3런×최종·조기=6파일. 모든 메모 실행값은 a/b. 거부는 cim-fp-3 최종의 required 두 건뿐. |
| SPEC | :1670 값 공간 정본 문단 바로 뒤 :1672에 T35 문단. 참조·상한·무소급 문언이 실물과 맞음. |
| 외부 경로 | 미래 감사 사본, 외부 Python·drafts·레인 파일, 메모리 용량은 사본 밖 무접촉 제약으로 미검증. 현재 M1b 사본과 미래 M9 사본의 경로 차이는 결함으로 세지 않음. |

```text
독립 JSON 검증 집계:
MISSING []
JSON_VALIDATION {
  ('accept', False): 15,
  ('reject', True): 33,
  ('validator-scope', False): 2
}
OLD_ACCEPT_MEMOS {'absent': 12, 'empty': 2}

관문 코드의 출력 형식과 위 집계로 확인한 기대 행:
SUMMARY: cases=50 REJECT_OK 33/33 ACCEPT_OK 15/15 VALIDATOR_SCOPE 2/2 schemas=5
```

위 SUMMARY는 관문 실행 출력으로 주장하지 않는다. validator-scope 두 사례의 별도 의미 검증기도 실행하지 않았다.

**폐쇄 판별 대응표**

“가능”은 A가 요구하는 실측으로 판별할 수 있다는 뜻이며, 이번에 pytest 폐쇄를 확인했다는 뜻은 아니다.

| 대상 | A의 질문 | 폐쇄를 가르는 실측·남은 문제 |
|---|---|---|
| RF-1 | Q1ⓐ | I05·I06에 허용값 검사 삭제를 적용. 위치 지정은 MD-3 수정 필요. |
| RF-2 | Q1ⓒ·§1 | H에서 T22 붉음, 형제·관문 초록; 한정어·⒁ 문언 대조. 비교 집합 셋은 명시돼 있다. |
| RF-3 | Q1ⓓ | 원·정정·재정정 보존 및 새 프로세스의 `law_repo` 경로 실측. 가능. |
| RF-4 | Q1ⓑ | I1T01의 줄·표 동시 출력과 위치 단언, 순서 반전 변조. 가능. |
| RF-5 | Q1ⓐ | I08·I15 중복을 규격 밖으로 세고, 중복 검사 제거 시 실패. 가능. |
| RF-6 | Q1ⓐ·Q5 | I07·I1T01에서 정상 N=1, `len` 변조 N=2. 길이 3×2는 회귀로 분리해야 함. |
| RF-7 | Q1ⓔ | HANDOFF 16차 정정 문언과 §13 대조. 가능. |
| RF-8 | Q1ⓔ·Q5 | ⒀의 두 방향·등가와 유효 발주 대조. MD-2의 적용 기준 정정 필요. |
| MB-1 | Q2ⓑ·§1 MB 대조 | manifest 50/33/15/2, 기존 빈 메모 2·필드 부재 12 확인. 현 계수는 맞음. |
| MB-2 | Q1ⓑ | null·false·0·빈 문자열·객체·리스트·부재 및 G09의 귀속 없음 우선. 가능. |
| MB-3 | §1 MC-1·Q5 | 코드/시험 축 고정 및 H 등가 분리. MD-2·MD-5 주의. |
| MB-4 | Q2ⓑⓓⓔⓕ | 재정·A·SPEC·6파일·새 accept의 정정 전파 대조. 가능. |
| MB-5 | Q2ⓓ | 영속 시험의 Git HEAD 의존·임시 기준 의존 부재 확인. 가능. |
| MB-6 | Q1ⓑ | 출력 순서만 반전시킨 판본에서 I1T01 실패. 명시적으로 보강됨. |
| MB-7 | Q2ⓕ·Q1ⓓ | T36 ⓠ 유지 대상과 자원 경합 가설 주석 대조. 원장 주석 실재. |
| MC-1 | §1·Q4·Q5 | 행마다 고정 대상·변경 축·색을 재측정. 재현표 좌표는 MD-1. |
| MC-2 | §1 MB·MC 대조·Q5 | G·0건 등 구 구현에서도 초록인 회귀와 A-차별 3사례 분리. 가능. |
| MC-3 | Q1ⓐ·Q5 | I07·I1T01의 N 차이와 I2-01의 비판별성을 확인. 가능. |
| MC-4 | Q2ⓑ·§1 MB·MC 대조 | SUMMARY 전체 행과 기존 accept 범위 대조. A에 전체 행을 쓰면 더 명확함. |
| MC-5 | §1·Q2ⓓ | 이전 스키마 복원·비교 부재, `iter_errors` 전량 및 required 두 건 확인. 명시적으로 보강됨; MD-5 별도. |
| MC-6 | §1·Q1ⓐⓑ | 고유 ID 30개와 사례별 결과. MD-4의 낡은 계수 제거 필요. |
| T35 ⑴ | Q2ⓐⓑⓓⓔⓕ | 참조 셋·리터럴 하나·한 필드 reject·accept 15·실런 6파일·SPEC·원장. 가능. |
| T35 ⑵ | Q2ⓒ | 확장 enum에서 오류 집합=`{maxItems}`, 상한 삭제 시 accept, 현재 enum에서는 전후 reject. 가능. |

**새로 생긴 감사 표면과 재현 가능성**

- **30사례의 배타·완비:** G·I·T·A 네 술어 자체를 배타라고 해서는 안 된다. I와 T는 의도적으로 함께 출력한다. 귀속 없음이 우선하고, 이후 I만/T만/I→T/A로 결과를 분류해야 한다. Q1ⓑ는 이를 물을 수 있지만, 표본 30개 통과를 전체 공간 증명으로 대체하면 안 된다.
- **혼재와 귀속 없음 경계:** G09=`[]+[c]+[a]`가 두 출력을 모두 억제하는지 확인할 수 있다. v2 Aⓕ의 우선 가드 변조도 감사 재현 목록에 직접 열거하면 분명해진다.
- **확장 enum의 다른 위반 0:** 실제 시험은 `keywords != ["maxItems"]`로 오류 전량을 검사한다. 독립 JSON 검증도 `maxItems` 하나, 상한 삭제 뒤 오류 0이었다.
- **새 메모 두 건:** accept는 a/clear·b/concern과 비어 있지 않은 영문 note를 가진다. 실런은 a/clear·b/clear다. 필드 형태는 일치하고 방향 차이는 합법적인 합성 사례다. 실런 내용의 복제라고 주장하지 않으므로 결함이 아니다.
- **T36 대응:** 고유 항목 ⓖ~ⓠ 11개는 대응한다. 물리적 마커는 9곳이며 ⓟ는 원장이 지정한 두 문서에 걸친다. Q2ⓕ의 “1:1”은 **항목별 지정 좌표 대응**으로 읽어야 하며, 마커 줄 수 11을 요구하면 오탐이다.
- **판정 어휘:** A에는 “권고는 지적에서 제외” 같은 반대 조항이 없어 `PASS=지적 0`과 격 어휘 사이의 직접 모순은 없다. `partially/open`을 남긴 채 PASS할 수 있는지와 `[미검증]`의 처리 기준은 명시하면 좋다.
- **Owner 권한:** Q6이 계열 종결을 Owner의 것으로 명시한다. 감사 중 정본 커밋 금지도 A와 HANDOFF에 모두 있다.

반경 교집합 명령은 Bash에서 SHA를 대입하면 실행 가능하며 실제 결과는 다음과 같다.

```text
$ comm -12 \
  <(git diff-tree --no-commit-id --name-only -r 2d01e91 | sort) \
  <(git diff-tree --no-commit-id --name-only -r 4bb2579 | sort)
[출력 없음]
exit 0
```

A의 `<RF>`·`<T35>`는 치환 표지다. 그대로 붙여 실행하는 명령은 아니므로 핀을 채운 형태로 제공하는 편이 낫다. 두 커밋의 파일 집합은 실제로 겹치지 않는다.

`law_repo`는 `tempfile.mkdtemp(prefix="patent-docent-law-")`를 사용하며 `dir=`을 덮어쓰지 않는다. 따라서 존재하는 홈 FS의 `TMPDIR`을 새 프로세스에 주라는 처방은 코드와 맞는다. 실제 생성은 하지 않았다.

미래 M9 사본이 개시부터 마커 한 줄이면 종료 조건과 정합한다. 현재 M1b 사본의 `?? bundle/`는 제공 입력이므로 제거할 대상이 아니다.

**관측·종료**

- 신규 지적: **6건 — MED 4, LOW 2**.
- 기존 처분: RF **수용 8**, MB **수용 7**, MC **수용 6**; 각각 부분·기각·이연 0.
- MD 처분: **미결 6**. 발주자의 수용/부분/기각/이연을 임의로 배정하지 않았다.
- 검사기 대조: **pytest·관문 실행 0건**. manifest 전건 JSON 검증과 검사기 집계 코드 대조는 완료했다. 실행 검사기 대비 누락 여부·강등 조건 ⓐ는 미평가다.
- `USAGE`: 허용된 bundle에 이 런의 STATUS/finish 산출물이 없어 확보하지 못했다. finish 후 기재가 필요하다.
- 소요: 종료 관측 시각 **2026-09-05 13:08:56+09:00**. 시작 계측값이 없어 정확한 벽시계 소요·토큰 한도 충족은 주장하지 않는다.
- 파일 쓰기·pytest·관문·`/tmp` 접근 없음. 정본은 HEAD 조회만 수행했다.

```text
$ git status --short
?? .audit-sandbox
?? bundle/

$ git rev-parse HEAD
a48a97f163aa4827e6954e242485822fa6891ef5

$ git -C /home/laptop/projects/patent-docent rev-parse HEAD
a48a97f163aa4827e6954e242485822fa6891ef5
```

VERDICT: REVISE