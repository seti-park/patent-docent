# 독립 감수 원문 — M1b 설계 도전 18차(gpt-6-astra high) · T40 ④ A 비교 실측 설계 메모 v18 · 판정 REVISE(MED 3)

## ★ 이 절은 총괄 저작이며 도전 원문이 아니다 (2026-09-06 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「도전 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`FINAL` · sha256 `0d4d844098cd6cb322b7ff98fb342be2e9d64510e9cdf189319e56de59367e46` · 17786 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/astra-m1b-t40v18/`.

**좌석 = `좌석 M1b` · `gpt-6-astra` high** · `setsid nohup` · 09:5x → 10:2x. 사본 `~/projects/workspaces/pd-m1b-t40`(재핀 detached `4fe83b3` · v18 sha256 `21d5f478…` · v1~v17 동봉). **총괄 발주 오류(지적 밖 · 도전자 기록)**: `.audit-sandbox` 의 pin 이 직전 회차 `4894eee` 로 남았다(sed 가 order 만 갈았다) — 도전자는 HEAD 실측으로 대상을 확정하고 「마커 전부 일치」 판정을 유보했다. 19차부터 pin 은 `git rev-parse HEAD` 로 쓴다. 폐쇄 = **이전 59건 closed 54 · partially 5 · open 0**(NH-1·NM-1·NN-3·NO-2·NO-4 가 NP 로 이어짐). **B·C·E·F PASS**(13회 연속).

**판정 = REVISE · 3건(MED 3) · 기각 0 · 발주자 귀책.** **NP-1**: 검사 id 집합·중복 검증이 `not any_fail ∧ executed` 에만 걸려 있어 fail 행 하나 또는 executed=false 가 다른 손상(fail 근거 제거 · 행 중복 · 엔진 검사 3행 제거 · findings 만 제거)을 「정당한 실패」로 통과시킨다 — 실제 러너의 full/halt 4행 자료에서 4 변형 전부 exit 0. **NP-2**: `ok` 는 소비 여부가 아니라 모델·effort 일치까지 포함한 상태인데 추출기가 `ok ∧ ¬rejected` 행만 응답 SHA·좌표·반향을 검증 → 모델 불일치 소비 행(`ok=false, mismatch=true, response_digest=<소비 바이트>`)의 응답 교체·제거·반향 변조가 전부 통과. **NP-3**: 최종 포인터 기록에만 실패한 런(완주 13행 pass · 명세 실재 · 이전 포인터 terminated=false)을 in-progress 로 보고 — T38 ③ 과 러너 가드 `_run_is_terminated` 는 완주 판정서(phase=full)만으로 종결을 인정한다.

지적 열거 = NP-1, NP-2, NP-3

처분 = `docs/decisions/DISPOSITIONS.md` 행 · 사유 = `D-20260905-02-pdm2b-seats.md` **§17 추기 17**. **전부 수용 → 지표 v19**(실행 경로별 기대 다중집합 — executed=true 13 · executed=false 출구 halt 4 — 를 실패 여부 무관 대조 · fail 행 ↔ findings 정합 · executed=false ∧ fail 없음 = 손상 · 소비 행 = 응답 흔적 있는 행으로 정의해 ok 와 무관하게 응답 실재·SHA·lane_id·model·반향 검증 · ㉣ 적격만 ok ∧ ¬rejected · 종결 = 포인터 → 완주 판정서 phase=full 순서 · 포인터 false ∧ 완주 판정서 = terminated-incomplete(pointer-not-terminated)) → **M1b 19차 도전(지적 `NQ-*`)**.

---

# 도전 원문 (gpt-6-astra high · 이 아래는 도전자 저작)

VERDICT: REVISE

**이전 59건: closed 54 · partially 5 · open 0. 신규 지적 NP-1~3은 모두 MED입니다.** 17차 지정 반례는 해결됐지만, 실패 자료의 손상 판별·모델 불일치 소비 행의 결속·최종 포인터 기록 실패의 상태 판정에 결함이 남았습니다. 실측 착수 불가입니다.

**A — MY~NO 폐쇄표**

범위 표기는 해당 ID 각각에 적용합니다. 지정 반례의 통과와 수용된 처분 전체의 폐쇄를 구별했습니다.

| 이전 지적 | v18 판정 | 근거 |
|---|---|---|
| MY-1~13 | closed | 절차·핀·비교 단위·표본·계수·배치·증거 보존 처분 유지 |
| MZ-1~9 | closed | 병합 후보 재사용·스냅샷 결속·최신 시도 처분·예외 분류·발주 상한 유지 |
| NA-1~7 | closed | 최신 계약 거부 응답의 N/A 처리까지 실제 러너로 재확인 |
| NB-1~3 | closed | 증거 실패→14·발주 전건 검사·판정서 형태 검증 유지 |
| NC-1~3 | closed | 실제 enter 실패→14·스냅샷 단일 읽기·수치 제약 유지 |
| ND-1~2 | closed | findings 계약 검증·검증한 응답 바이트로 계수 |
| NE-1~2 | closed | 조기·완주 공통 형태 검증과 finding 필드 검증 유지 |
| NF-1 | closed | 완주 run_id 대조 |
| NG-1~2 | closed | 명세 run_id 대조·버전 표기 |
| **NH-1** | **partially** | 지정 donor 반례는 차단. 모델 불일치 소비 행에서는 응답 결속을 생략: NP-2 |
| NH-2 | closed | baseline 대상 제한·옵션 상호 배타 |
| NI-1~2 | closed | 요청 MD 재계산·dispatch 대조·명세 포함 원천 지문 사슬 |
| NJ-1 | closed | 원천 부재·변경·읽기 실패 거부 |
| NK-1 | closed | 명세 필수 필드 결측 거부 |
| NL-1 | closed | component·grounding 전량 제거·dependents=[] 거부 |
| **NM-1** | **partially** | 전건 pass 판정서의 엔진 검사 3행 결측은 차단. 실패 판정서에서는 같은 결측 수용: NP-1 |
| NM-2 | closed | 원천 단일 읽기·예외 경계 유지 |
| NN-1~2 | closed | 조기 검사 다중집합·로그 중복·행과 응답 동반 결측 거부 |
| **NN-3** | **partially** | 지정 합법 상태 넷은 해결. 최종 포인터 기록 실패 상태는 NP-3 |
| NN-4 | closed | 필드 결측·타입 검증, batch=true 거부 |
| NO-1 | closed | 접지·통합 LanePending 허용, 미소비 응답 좌표 보존 |
| **NO-2** | **partially** | 전건 pass 손상과 명세 기록 실패는 해결. 실패·미실행 경로의 손상 면제는 NP-1 |
| NO-3 | closed | ND-2 재읽기 반례에서 응답 읽기 1회·fact=3 유지 |
| **NO-4** | **partially** | 지정 다섯 반례 모두 거부. `ok=false` 소비 행은 공통 검사 밖: NP-2 |

§8의 격은 유지됩니다. ⓐⓑⓒⓓⓗⓙⓛⓜ는 운영 재량, ⓔ는 T40 §5 승인, ⓕⓖⓝ는 명시한 범위의 재정 문언 이행입니다. ⓘ의 표본 단위와 ⓚ의 27단위·Owner 판정은 재정 이행이며, 인덱스·후보 제시·런 표기는 재량입니다. G-12의 일반 집행 공백을 해소했다고 주장하지 않고 이번 발주를 `partial/read`로 제한한 점도 정합합니다.

인계 검증에서는 **마커 pin 불일치**가 있었습니다. path·order·disposable은 일치하지만 pin은 `4894eee…`, 실제 HEAD는 요청한 `4fe83b39143585b4f68bd4a9c9fd0fb5671e7e27`입니다. 메모 해시는 요청값 `21d5f4783291d262…`와 일치합니다. 마커까지 전부 일치했다고 판정하지 않았습니다.

**NP-1 · MED — 실패 또는 수렴 미실행이면 검사 집합 손상을 면제한다.**

좌표: 메모 §5 상태 판정·손상 구별·§9 D; [t40_metrics.py:229](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:229)의 `any_fail`, `executed`, `expected_ids`.

검사 ID 집합·중복 검증이 **`not any_fail and executed is True`일 때만** 작동합니다. 따라서 실패 행 하나 또는 `executed=false`가 다른 손상을 통과시키는 조건이 됩니다.

실제 러너의 출구 원천 재독에만 `PermissionError`를 주어 생성한 정상 full/halt 판정서는 다음 4행입니다.

`read.input-digest`, `read.source-digest` **fail**, `read.lane-log-shape`, `read.lane-log-digest-value`.

그 자료에서 독립적으로 변경했습니다.

| 변경 | v18 결과 |
|---|---|
| 유일한 fail 행과 findings 제거 → **3행 전부 pass**, executed=false | **exit 0 · terminated-failure** |
| 정상 pass 행 하나 중복 | **exit 0 · terminated-failure** |
| 엔진 검사 3행 제거 → source-digest fail 한 행만 유지 | **exit 0 · terminated-failure** |
| fail 행·violations는 유지하고 findings만 제거 | **exit 0 · terminated-failure** |

13행·executed=true인 실패 판정서에서도 엔진 검사 3행 제거와 정상 행 중복이 모두 통과했습니다. 반면 **전건 pass인 정상 판정서**의 동일한 제거·중복은 exit 4였습니다.

즉 NO-2의 지정 반례는 닫혔지만, **실패 근거를 지운 자료까지 “정당한 실패”로 수용**합니다. `CheckRow.status`는 findings로부터 파생되며 `to_convergence_payload()`가 행과 findings를 함께 직렬화하므로, 이 불일치는 실제 생성 규칙과도 어긋납니다.

**고치는 문안:** “완주 판정서는 실행 경로별 기대 검사 다중집합과 status·violations·findings의 정합을 실패 여부와 무관하게 검증하고, executed=false 자체를 실패의 증거로 사용하지 않는다.”

**NP-2 · MED — 모델 불일치를 ‘미소비’로 취급하여 실제 소비 응답의 손상을 허용한다.**

좌표: 메모 §5 전 상태 공통 검사·입력 결속 사슬; [t40_metrics.py:258](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:258), [응답 검증 분기:285](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:285); `read._dispatch`, `LaneJournal.record`.

실제 파일 어댑터에 정상 synthesize payload와 다른 모델명을 공급했습니다. 러너는 응답을 읽고 payload를 반환·사용한 뒤 다음 행을 남깁니다.

`ok=false, mismatch=true, rejected=false, actual_model≠null, response_digest=<소비 바이트 SHA>`

이후 `LaneAssignmentError`로 종결합니다. **`ok`는 소비 여부가 아니라 모델·effort 일치 여부를 포함한 상태**입니다.

그러나 추출기는 `ok and not rejected`인 행만 응답 SHA·식별자·반향을 검증합니다. 위 실제 러너 산출에서 다음 변경이 모두 통과했습니다.

| 변경 | v18 결과 |
|---|---|
| 응답을 다른 lane_id·input_digest의 JSON으로 교체 | **exit 0 · terminated-failure** |
| 소비된 response.json 제거 | **exit 0 · terminated-failure** |
| 로그의 echoed_digest 변경·digest_ok=false·response_digest=null | **exit 0 · terminated-failure** |

㉣이 N/A라는 사실은 맞습니다. 그러나 **계수 부적격과 소비 증거 검증 면제는 다른 처분**입니다. 이 경로는 모델 불일치 실패 자료의 사후 교체·결측을 숨깁니다.

**고치는 문안:** “응답 소비 여부를 ok와 분리하여 모델 불일치 소비 행에도 응답 실재·SHA·lane_id·반향 정합을 공통 적용하고, 적격성만 별도로 판단하여 ㉣을 N/A로 둔다.”

**NP-3 · MED — 최종 포인터 기록 실패를 비종결 진행 상태로 잘못 보고한다.**

좌표: 메모 §5 `in-progress=terminated=false`; [t40_metrics.py:237](/home/laptop/projects/workspaces/pd-m1b-t40/bundle/t40_metrics.py:237); `read.run`의 판정서→명세→finally 포인터 순서; [read._run_is_terminated](/home/laptop/projects/workspaces/pd-m1b-t40/engine/stages/read.py:1094); T38 ③.

이전 대기 호출의 `terminated=false` 포인터를 두고, 실제 러너의 **마지막 포인터 기록에만** `PermissionError`를 주었습니다.

남은 자료는 완주 13행 전부 pass·executed=true·명세 실재·이전 포인터 false입니다.

```text
POINTER_WRITE_FAIL exit 0 state in-progress synth None
ACTUAL_TERMINATION_GUARD (True, 'convergence.json')
```

T38 ③과 실제 가드는 **full 판정서만으로도 종결**을 인정합니다. 추출기는 이전 포인터의 false를 우선하여 이미 종결한 런을 진행 중이라고 보고합니다. 명세 기록 실패는 보완했지만, 그 뒤 포인터 기록 실패는 놓쳤습니다.

**고치는 문안:** “T38의 세 근거로 종결 여부를 먼저 확정하고, 최종 포인터 기록 실패로 이전 비종결 포인터가 남은 경우는 terminated-incomplete와 사유별 N/A로 보존한다.”

**A~G 판정**

| 항목 | 판정 | 근거 |
|---|---|---|
| A 원장 정합·폐쇄·격 | **REVISE** | 재정 해석은 유지되나 T38 종결 판정과 결속 집행에 잔여 |
| B 계측 커밋 셋 | **PASS** | 부모·절차 tree·blob·팔 diff·16파일 numstat·프로필·최초 요청 동일성 확인 |
| C 구동 v6 | **PASS** | 종료 분류·실제 enter 실패·증거 실패·스냅샷·조회/발주·상한 재시험 |
| D 지표 v18 | **REVISE** | NP-1~3 |
| E 발췌 v4 | **PASS** | 27단위·병합 후보 재사용·청구항 표본·판정 불가 처분 유지 |
| F Workflow v4 | **PASS** | 지정 사전 거부·wrote/null 구별과 보존 절차 확인 |
| G 결정 공백 | **REVISE** | 실패 자료 손상·소비 행·종결 근거 충돌의 처분을 실행 중 수작업으로 선택해야 함 |

C·E·F는 정적·메모리 검증 범위의 판정입니다.

**B — 직접 대조 결과**

base 부모는 `6d92cad`, R1·R2 부모는 `ad4c6c3`입니다. 기준과 base의 절차 tree는 모두 `d7717eb8750115a49e81ec7803790093b98c40ec`입니다. `6d92cad→base`는 절차 6파일뿐이고, 두 팔은 각각 `2 2 contracts/stages/read.yaml`뿐입니다.

§0′의 변경 열거 **16파일 전부 일치**했습니다.

| 파일 | 추가/삭제 |
|---|---|
| read.yaml · convergence 스키마 · run-kinds | 321/31 · 42/7 · 24/2 |
| read.py · source.py | 713/126 · 46/1 |
| lanes/contract.py | 67/1 |
| lanes/plan.py · file_adapter.py · replay_adapter.py | 2/7 · 6/4 · 2/2 |
| paths.py · stages/__init__.py | 19/0 · 69/0 |
| render/material_spec_md.py | 85/1 |
| reader/lib/run_checks.py · convergence.py · dependency_parse.py | 90/35 · 32/5 · 30/1 |
| reader/lib/__init__.py | 4/0 |

`lane_profiles()`는 R1의 분해·통합만 xhigh, R2의 종속 접지만 sonnet-5/high로 산출했습니다. 최초 요청서 재렌더는 **6/6 바이트 동일**, 신규 최초 분해 요청의 차이 필드는 `[]`였습니다. 소견을 넣은 재시도 요청은 본문·지문이 달라졌습니다. 동일성 범위를 최초 요청으로 한정한 문안은 맞습니다.

**D — 상태·회귀 실측**

실제 `read.run`과 `FileLaneAdapter`를 사용하고 파일 출력을 메모리로 대체했습니다.

| 합법 상태 | 러너 산출 | v18 결과 |
|---|---|---|
| 조기 상신 대기 | 로그 2행·terminated=false | exit 0 · **in-progress** · ㉣ N/A |
| 접지 retry 일부 도착 | LanePending·로그 6행 | exit 0 · **in-progress** · 미소비 응답 2좌표 보존 |
| NA-1 최신 통합 계약 거부 | LaneContractError·최신 응답 존재·해당 행 없음 | exit 0 · **terminated-failure** · 미소비 응답 1좌표 보존 |
| 출구 원천 재독 실패 | halt·full 4행·executed=false | exit 0 · **terminated-failure** · ㉣ N/A |
| 판정서 통과 뒤 명세 기록 실패 | full 13행 pass·terminated=true·명세 없음 | exit 0 · **terminated-incomplete** · ㉣ N/A |
| 정상 통합 응답 대기 | LanePending·로그 5행 | exit 0 · **in-progress** · ㉣ N/A |

NO-4 지정 다섯 반례는 **모두 exit 4**였습니다. 명세 원천 지문, 소비 정상 행의 반향·digest_ok, 로그 파일 부재, batch=true, terminated=1을 각각 시험했습니다.

기존 형태·결측·결속 반례를 재구성한 오류 입력 **254건 모두 exit 4**였습니다. 범위는 조기·완주 필수 필드, 검사·findings 형태, 축 결측·중복, bool·음수 계수, bool·NaN·무한대·범위 밖 Jaccard, 명세 필드·집합 결측, 로그 필드·중복·동반 결측, 요청·응답·dispatch·원천 결속입니다. 실제 CIM-FP-3 명세와 요청·응답 묶음의 donor 반례도 거부됐습니다.

ND-2 프로브는 두 번째 응답 읽기에 fact 제거본을 공급하도록 했습니다. 결과는 다음과 같습니다.

```text
SINGLE_READ {'synth': 1, 'source': 1, 'snapshot': 1}
COUNTED_FACT 3 ELIGIBLE True
```

기준 CLI는 **exit 0·complete·163항목·component 56·전체 anchor 51/5·종속 anchor 45/5·통합 3/20/7/10·na=[]**였습니다.

**검증 경로**

모든 명령의 cwd는 지정 사본입니다. 아래 `PY`는 `PYTHONDONTWRITEBYTECODE=1 /home/laptop/projects/patent-docent/.venv/bin/python`을 뜻합니다. 메모리 시험은 `PY - <<'PY' … PY`로 전경 실행했습니다.

| 명령·호출 경로 | 마지막 출력 또는 확인 행 |
|---|---|
| `cat .audit-sandbox; git rev-parse HEAD` | `4fe83b39143585b4f68bd4a9c9fd0fb5671e7e27` — 마커 pin은 별도 불일치 |
| `sha256sum bundle/T40-MEASURE-DESIGN.md` | `21d5f4783291d2629ea2c9597e527dca37b0395c9a82805ffdd67e361ebde72a` |
| `git diff --stat d4e6ca2 origin/t40-base -- reader/procedure` | 빈 출력 |
| `git diff --numstat 6d92cad origin/t40-base` | `0 139 reader/procedure/HISTORY.md` |
| base→R1·R2 `git diff --numstat` | 각각 `2 2 contracts/stages/read.yaml` |
| `git diff --numstat d4e6ca2 6d92cad -- contracts engine reader/lib` | `90 35 reader/lib/run_checks.py` — 16파일 대조 |
| `PY bundle/t40_metrics.py runs/gdm-wo2026128750a1-agent-memory --baseline` | `}` · exit 0 |
| 같은 명령에서 `--baseline` 생략 | `실측 런은 --first-early 가 필수다` · exit 4 |
| `--first-early /memory/absent.json` | `first-early 스냅샷 없음: /memory/absent.json` · exit 4 |
| 실제 CLI 본문·불일치 sidecar 메모리 공급 | `스냅샷 sha256 불일치` · exit 4 |
| 실제 CLI 본문·오류 입력 회귀 | `REGRESSION_EXPECT_EXIT4 254 COUNTS {4: 254} UNEXPECTED []` |
| 실제 러너→지표, 실패 행 제거 | `HALT_REMOVE_ONLY_FAIL exit 0 state terminated-failure` |
| 실제 러너→지표, mismatch 응답 제거 | `MISMATCH_RESPONSE_ABSENT exit 0 state terminated-failure` |
| 포인터 기록 실패 자료→실제 종결 가드 | `ACTUAL_TERMINATION_GUARD (True, 'convergence.json')` |
| 구동 `classify`·예외 분류 | `CLASSIFY [0, 13, 11, 12, 12, 14, 14]` · `AFTER_EXCEPTION [13, 14]` |
| 실제 enter의 worktree 부재·잘못된 런 이름 | 각각 `14 SYSTEMEXIT_EVIDENCE True` |
| 종결 포인터 true·증거 기록 실패 | `ENGINE_EXCEPTION_EVIDENCE False 14` |
| 스냅샷 메모리 복사·보존 | `SNAPSHOT NOCONV True FIRST_PRESERVED True SHA_MATCH True` |
| 발주 A/A/A/B/C/D·조회 4회 | 코드 `0/14/14/0/0/15`, 회차 `1/1/1/2/3/3`, `LANES_QUERY4_UNCHANGED True` |
| 발췌 순수 함수 import | `EXCERPT_SELF 27 /27` · 병합 후보 `[['M20'], ['M20'], ['M20'], ['M20'], ['M20']]` |
| 표본·원문 단락 대조 | CL-2·4·7·9·12·14·16·19·21·24 · `LOCATORS 27 RESOLVED 27` |
| `node --input-type=module -`·Workflow 본문·agent/pipeline 대체 | toString·constructor·/./·중복·교차·좌표 오류 모두 `calls:0,error:true` |
| Workflow 정상 보고 분기 | `requested:3,wrote:1,not_written:1,dropped:["r2"]` |
| 봉투 stdout 미리보기→러너 검증기 | `(True, '계속 봉투 유효(판정서 지문 결속 확인)')` |
| 최종 `git status --porcelain --untracked-files=no` | 빈 출력 |

**v6에는 `_next_dispatch`가 없습니다.** 현재 구현인 `cmd_dispatch`를 시험했습니다. 발췌 `ex1/ex2`와 발췌 CLI는 실행하지 않았습니다.

지표 시험은 파일 접근 함수를 메모리 자료로 대체하고 **실제 CLI 본문과 검증 함수**를 실행했습니다. 러너 시험에서는 진입 지문·최초 종결 가드·봉투 확인·원장 append를 대체했고, 절차 본문은 base blob을 공급했습니다. 분해·접지·통합 payload는 보관 응답을 사용했으며, 제어 흐름·요청 생성·파일 어댑터·응답 계약 검사·판정서 생성은 실제 코드였습니다. NP-3의 사후 종결 가드는 대체하지 않았습니다.

**[미검증]**

- 외부 스테이징 TXT·도면 20개·MAPPING은 읽지 않았습니다.
- 실제 Workflow 모델 호출·transcript/journal 이벤트 형식·실호출 effort·문맥 격리는 검증하지 않았습니다.
- 실제 worktree 생성·source 봉인·봉투 발행·생산 원장 append는 수행하지 않았습니다.
- 역사적 `d4e6ca2` 러너 재기동과 구동·발췌·Workflow의 전판 실행본 바이트 동일성은 검증하지 않았습니다.
- 비용·시간·토큰·가용 메모리 추정은 검증하지 않았습니다.

**읽은 파일**

- 원장·이력: T40 §1·§4·§5, D-20260905-02 §17와 추기, MY~NO 도전 원문의 지적·반례·처분, SPEC 지정 G행, T14·T17·T38.
- 계약: run-kinds, read의 lane·failure·retry_budget·phase_gates, approval-envelope·convergence·material-spec 스키마.
- 대상: 설계 v3·v17·v18 및 bundle 스크립트 5종.
- 구현: read·source 러너, lanes의 plan·contract·file_adapter, paths·ReadView, reader의 convergence·run_checks·report·관련 검사 호출 경로.
- 실물: 기준 run.yaml·원천·두 판정서·명세·로그·요청/응답 6벌, CIM-FP-3 donor 자료, 지정 Git 부모·tree·blob·diff.

파일·임시물·캐시를 만들지 않았습니다. 정본 리포는 허용된 Python 인터프리터 이용 외에 읽지 않았으며, 실측 레인은 시작하지 않았습니다.