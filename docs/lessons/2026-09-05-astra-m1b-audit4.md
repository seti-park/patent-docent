# 독립 감수 원문 — M1b 설계 도전(gpt-6-astra high) · 재감사 4(RH · 축소 범위) 발주문 · 판정 REVISE

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `f607b073e383f7d371198ffcdb1fdb911cb5ec77b50e6304d40f010cdb7cf90b` · 7158 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-audit4/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high**(확정 좌석) · `setsid nohup` · 14:56:14 → 15:03:57 · EXIT=0 · **USAGE = input 1,482,069(cached 1,384,576) · output 10,490(reasoning 2,017)**. 사본 = `~/projects/workspaces/pd-m1b-audit4`(detached `45895ec`). 읽기 전용.

**판정 = REVISE · 4건(전부 LOW · 발주자 귀책) · 기각 0.** **MF-1**: Q1ⓑ 가 ME-1 의 네 칸 축(같은 `set()` 변조 × 구 시험 `d29c8a2` 초록 → 신 시험 붉음)을 감사자에게 직접 재현하라고 요구하지 않음. **MF-2**: 감사 대상 커밋 메시지 `6173b96` 의 「레인 보고 전문은 §24」는 §25 의 오기(정정 마커 없음). **MF-3**: 「단언 셋」 — 실물은 ME-1 보강 뒤 8단언. **MF-4**: 백로그 좌표 `run_checks.py:168` 은 현재 주석 행 · 폴백은 `:171`. 그 밖 실측 전건 일치(커밋·부모 · 반경 · 절 번호 · RG-1 마커·바이트 보존 · RG-2 시험 실물 · 호출점 순서 · 시험 수 811 정적 계수 · M1b 원문·레인 보고 sha256 · RG-3 제거 · 처분 원장). 향후 opus 사본·레인 디렉터리 부재는 발주 전 생성 사항으로 구분.

지적 열거 = MF-1, MF-2, MF-3, MF-4

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260903-04-t31-t32.md` **§26**. **전부 수용** → 발주문 정정(drafts) + §24 말미 MF-2 정정 마커(이 커밋) → 재감사 4 발주.

---

# 도전 원문 (gpt-6-astra high · M1b · 이 아래는 도전자 저작)

**마커 3검증 + 정본 HEAD**

```text
pwd=/home/laptop/projects/workspaces/pd-m1b-audit4
path=/home/laptop/projects/workspaces/pd-m1b-audit4
pin=45895ec4787a6d19083c407f3499b9f6c59c39e1
order=M1B-audit4-20260905
disposable=true

MARKER_PATH_EQ_PWD True
MARKER_PIN_EQ_HEAD True
MARKER_DISPOSABLE_TRUE True

사본·정본 HEAD:
45895ec4787a6d19083c407f3499b9f6c59c39e1
사본·정본 tree:
f3e056d13bab4e4c8325ce44db0b64bdbfb5d371

개시·종료 git status --short:
?? .audit-sandbox
?? bundle/
```

**판정 = REVISE.** 대조 축의 명시가 다시 끊겼고, 보고 좌표·단언 수·백로그 행 번호에 오기가 있다. 지적 4건 모두 LOW이며 발주자 귀책이다.

**MF-1 · LOW — Q1ⓑ가 ME-1의 구·신 시험 대조를 다시 요구하지 않는다**

좌표: [발주문:26](/home/laptop/projects/workspaces/pd-m1b-audit4/bundle/AUDIT-ORDER-round-rg.md:26)·:33.

근거 실출력:

```text
Q1ⓑ: 헬퍼를 len(set(values)) != len(values) 로 변조
      → 새 시험만 붉는가(TypeError) · 다른 시험은 초록

D-04:1239:
올바른 축은 「같은 set() 변조 고정 × 구 시험(초록) → 신 시험(붉음)」

drafts/SPEC-round-rg.md:16:
구 시험 = git show HEAD:tests/test_m22_unclassified_render_notice.py
```

“다른 시험은 초록”은 신 시험군 안의 비실패 시험을 뜻할 수 있어, **수리 전 시험 판본을 실행했다는 증거를 요구하지 않는다.** Q3의 기록 대조도 감사자 자신의 구 시험 대조를 대신하지 못한다. 또한 집행 당시의 `HEAD`를 감사 사본에서 그대로 쓰면 이미 새 시험을 추출한다.

검증 경로: Q1ⓑ·판정 형식 → M1b 원문 ME-1 → D-04 §23 → 유효 RG 발주문 §2 → `6173b96`의 부모 확인.

고치는 문안 한 줄: **“같은 `set()` 변조에서 구 시험(`d29c8a2`) 초록→신 시험(`45895ec`)의 새 시험만 붉음을 직접 재현하고, 무변조 양쪽 초록까지 네 칸 실출력과 판본을 보고한다.”**

**MF-2 · LOW — Q3가 대조할 RG 커밋 메시지의 보고 좌표가 틀렸다**

좌표: [발주문:28](/home/laptop/projects/workspaces/pd-m1b-audit4/bundle/AUDIT-ORDER-round-rg.md:28), `6173b96` 커밋 메시지.

근거 실출력:

```text
$ git show -s --format=%B 6173b96
… 레인 보고 전문은 D-20260903-04 §24.

D-04:1245: ## §24 라운드 RG 회수 · 총괄 재현 · 병합 …
D-04:1255: ## §25 SOL CODER REPORT 원문 ⑦ …
```

발주문 자체의 §24·§25 구분은 맞지만, 감사 대상으로 명시한 커밋 메시지에는 §24 오기가 남아 있다. 현재 기록에 이 메시지를 특정한 정정 마커는 없다. Q3를 그대로 수행하면 신규 기록 오류가 된다.

검증 경로: 커밋 메시지 → D-04 절 제목 → 외부 `final.txt`와 §25 정규화 비교(`True`).

고치는 문안 한 줄: **“[정정] `6173b96` 메시지의 ‘레인 보고 전문 §24’는 ‘§25’의 오기이며, §24는 총괄 재현 기록이다.”**

**MF-3 · LOW — ‘단언 셋’이 ME-1 반영 후 실물 8단언과 다르다**

좌표: [발주문:17](/home/laptop/projects/workspaces/pd-m1b-audit4/bundle/AUDIT-ORDER-round-rg.md:17)·:26, [새 시험:43](/home/laptop/projects/workspaces/pd-m1b-audit4/tests/test_m22_unclassified_render_notice.py:43).

근거 실출력:

```text
Q1ⓑ: 단언 셋
NEW_TEST_IFS 8
D-04:1249: … 문자열 회귀 8단언
```

§22의 최소 세 사례에 비인접·역순·리스트·문자열 비중복 보강이 추가됐다. Q2가 참조하는 유효 발주문 §1은 이를 허용하므로 명령되지 않은 hunk는 아니다. 다만 현행 시험을 “셋”으로 소개하면 보강분을 잘못 판정할 여지가 있다.

검증 경로: 시험 함수 AST의 `if`/`pytest.fail` 8쌍 → drafts §1:12 → D-04 §24.

고치는 문안 한 줄: **“최소 세 사례와 ME-1 반영 보강을 포함한 8단언을 확인하며, 비해시 사례의 판별과 문자열 회귀를 구분한다.”**

**MF-4 · LOW — 백로그 폴백의 행 번호가 낡았다**

좌표: [발주문:29](/home/laptop/projects/workspaces/pd-m1b-audit4/bundle/AUDIT-ORDER-round-rg.md:29).

근거 실출력:

```text
reader/lib/run_checks.py:168: # 정본 지정은 **선언 순서**이고 내용을 보지 않는다 …
reader/lib/run_checks.py:171: "read_run": canonical_read_run or (read_runs[0] if read_runs else ""),
```

폴백 자체는 실재하지만 지정한 `:168`은 현재 주석이다.

검증 경로: Q4 백로그 → D-04 §5의 전체 파일 경로 → HEAD 파일 행 번호 대조.

고치는 문안 한 줄: **“백로그 좌표를 `reader/lib/run_checks.py:171`의 `canonical_read_run or …` 폴백 제거로 고친다.”**

**나머지 실측**

| 항목 | 결과 |
|---|---|
| 커밋·부모 | `6173b96←d29c8a2`, `1cbcd5b←f807ad8`, `d29c8a2←1cbcd5b`, `45895ec←6173b96` 전부 일치 |
| 파일 반경 | RG는 지정 시험 파일 하나, 2 hunk, `+27 −1`. 기록 커밋 반경도 표와 일치 |
| 절·HANDOFF | §22:1221, §23:1237, §24:1245, §25:1255. HANDOFF 19차:15·20차:10 실재 |
| RG-1 | D-04:560·HANDOFF:35 마커 실재. `96f7582`의 구 문언은 마커 삽입 외 바이트 보존 확인 |
| RG-2 | 시험 이름·직접 호출·docstring 실재. `I14-duplicate-unhashable-objects`는 :283, 형태표 AST는 부모와 동일 |
| 호출점 | :494→495의 `or`, :524→525의 `and` 순서 확인. 비해시 원소가 헬퍼까지 도달하지 않는다는 설명과 일치 |
| 시험 수 | 소스·데이터 정적 계수 **811**. 매개변수 전개 포함 `720+18+50+6+15+2`. 표적 파일은 40→41. 실행 결과로 주장하지 않음 |
| M1b 원문 | 지정 `FINAL` 6,388 B, 보존 원문과 바이트 동일. SHA-256 `504ac18add9830d42da365e53a1e1971c2f66bef27d7352365dd63d1bb67870d` |
| 레인 보고 | `final.txt` 2,191 B, §25와 앞뒤 공백 정규화 동일. SHA-256 `5aab9bd69834e8a27836fbf1031c4c84e6225e5de5284e02a8525e2288382b4f` |
| RG-3 | 지정 drafts의 `96f7582` 괄호에서 중복 문구 제거 확인 |
| 처분 원장 | RG 3행·ME 1행 실재 |

축소 범위는 결함 보고를 금지하지 않고, 이미 closed인 자리의 재개에 근거를 요구한다. 전체 스위트 plain 1모드·최적화 모드 보고값 인용도 명시돼 있다. **신규 0 + RG 전건 closed**와 `[미검증]` 명시 허용은 양립한다. 대체된 구 발주문을 현행 수락 기준으로 다시 적용하라는 요구도 없다.

`git diff-tree` 명령은 실제 성공했고 지정 Python 실행 파일·관문 7종 파일도 존재한다. 다만 **향후 opus 사본 `pd-audit-round-rg`와 opus 레인 디렉터리는 현재 부재**다. 이는 이번 M1b 사본의 오류와 구분하며, 발주 전 생성 후 해당 사본에서 마커·detached HEAD·status 한 줄을 확인해야 한다.

파일 쓰기·pytest·관문·변조 실행·`/tmp` 접근 없음. 종료 시 사본·정본 HEAD 불변, 사본 `__pycache__` 0.

`USAGE: 현재 러너가 토큰 계측값을 아직 제공하지 않음 — 종료 후 input/cached/output/reasoning 관측값 첨부 필요.`

VERDICT: REVISE