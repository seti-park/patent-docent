# 독립 감수 원문 — 좁은 재감사 4(RH · 축소 범위 · 라운드 RG `6173b96` + 기록 `d29c8a2`·`45895ec`·`b1adfc1`) · opus max · 판정 PASS

## ★ 이 절은 총괄 저작이며 감사 원문이 아니다 (2026-09-05 · 머리말)

**규율 10 의 이행 — 원문 보존: 아래 「감사 원문」 절은 전문 보존이며 한 글자도 고치지 않는다**(`raw.json` `.result` → `out.txt` · sha256 `155372093bc888a07bdef2a85edb63d2b6b02ba1383f945df5eb6249b6a50efa` · 11418 B). 레인 디렉터리 = 홈 fs `~/projects/workspaces/pd-lanes/opus-audit-round-rg/`.

**좌석 = opus max**(M9 · sol 저작 → opus) · `claude -p --model claude-opus-5 --effort max --output-format json` · `setsid nohup` · 15:06:11 → 15:22:52 · 53턴 · 16.2분 · 출력 59,680(사고 32,317) · 캐시 읽기 4,803,862 · 캐시 생성 139,010 · 청구 $5.28 · EXIT=0. 발주문 = drafts `AUDIT-ORDER-round-rg.md`(축소 범위 · M1b astra high MF-1~4 반영판 · 전체 스위트 plain 1모드 · **감사 중 정본 커밋 금지 — 지켜졌다**: HEAD `b1adfc1` · 트리 동일 · status 0). 사본 홈 fs `pd-audit-round-rg` · basetemp·`TMPDIR` 홈 fs `pd-audit7-basetemp`(종료 시 삭제) · `/tmp` 무접촉.

**판정 = PASS · 신규 지적 0 · RG-1·RG-2·RG-3 전건 closed.** RG-1 = §13·HANDOFF 마커 실재 · 구 문언 바이트 보존 · 인용이 레인 원문 GAPS 절과 일치. RG-2 = 헬퍼 직접 호출 · 8단언 실측 · **네 칸 대조 감사자 직접 재현**(구 시험 `d29c8a2` × `set()` 변조 = 40 passed 결함 실물 · 신 시험 × 변조 = 1 failed TypeError · 무변조 양쪽 초록) · 원복 sha256 복귀 · docstring 「도달 불능」 참(호출점 사슬 + 계약 층 이중 차단). RG-3 = drafts 중복 제거. Q2 hunk 0 · Q3 기록 전건 정합(§22~§26 · §25 = `final.txt` sha256 · M1b 원문 2건 · 커밋 메시지 오기 마커 · 관문 7종 두 모드 · plain `811 passed`) · **Q4 종결 자격 = 충족**(선언은 Owner). 지적으로 세우지 않은 셋(`I14` 이름 · §10 목록 무방어 join 은 도달 불능 · 8단언 단일 함수). 남은 것 둘(docstring 「도달 불능」을 지키는 기계 없음 · 10-b 방어의 존재 근거 미성문화 → 백로그). [미검증] 4.

지적 열거 = 없음

처분 = 지적 없음 · `docs/decisions/DISPOSITIONS.md` §0 등재 · 사유 = `D-20260903-04-t31-t32.md` **§27** · 다음 = **PD-M2a 라운드 B 계열 종결 상신**(`/decision-brief`).

---

# 감사 원문 (opus max · 이 아래는 감사자 저작)

감사를 마쳤습니다. 판정서를 제출합니다.

---

# 좁은 재감사 4(RH · 축소 범위) — 라운드 RG `6173b96` · RG-1~RG-3 폐쇄

## ① preflight

```
$ cat .audit-sandbox
path=/home/laptop/projects/workspaces/pd-audit-round-rg      ← pwd 와 일치
pin=b1adfc1194700bd14bdff50889de58f62acf728f                 ← HEAD 와 일치
order=AUDIT-round-rg-20260905
disposable=true

$ git rev-parse HEAD        → b1adfc1194700bd14bdff50889de58f62acf728f
$ git status --short        → ?? .audit-sandbox          (개시부터 한 줄)
$ git rev-parse HEAD^{tree} → 88658f8b0a06b0d55810ad8693a9a851684997d5
$ git -C /home/laptop/projects/patent-docent rev-parse HEAD^{tree}
                            → 88658f8b0a06b0d55810ad8693a9a851684997d5   (동일)
$ git -C …/patent-docent status --short → (무출력 · 감사 중 정본 무변경)
```

계보 확인 — `b1adfc1`←`45895ec`←`6173b96`←`d29c8a2`←`1cbcd5b`←`f807ad8`. 메모리 2.9 GB · 전체 스위트는 plain 1모드만 · 겹쳐 돌리지 않음.

## ② RG-1 ~ RG-3 폐쇄표

| ID | 판정 | 근거(실출력) |
|---|---|---|
| **RG-1** | **closed** | §13 RE-1 항목 아래 정정 마커 실재 — 「계약 단독 변조 공간 안의 답」으로 한정 복원 · 「구 문언은 그대로 둔다」. **구 문언 바이트 보존**: `git diff 96f7582 HEAD -- D-04` 의 내용 삭제 줄 **0건**, 해당 hunk 는 `@@ -547,6 +557,7 @@`(1줄 추가만). **HANDOFF 16차 줄**: 마커 문자열을 제거하면 `96f7582` 판 줄과 **바이트 동일**(Python 대조 `True`). 인용 정확성 — 마커의 「고유 **계약** 변조는 없습니다」는 레인 원문 §14:128 「감사자 ⒜의 T22 고유 계약 변조는 없습니다」의 부분 문자열로 일치(§14:91 의 무한정 「고유 변조 없음」과 구별해 GAPS 절을 특정한 것이 옳다). 변조 H 실물 — 재감사 2 원문 :143 「계약 6행 `action: escalate → halt` **와** `APPROVED_FAILURE_TABLE` 6행을 함께 … 형제 골격 시험 `1 passed` · 관문 전부 `EXIT=0` … **T22 행 단언만** 붉는다」 = 마커 문언과 일치. RG-1 「닫는 법」 세 조건 전건 충족 |
| **RG-2** | **closed** | 새 시험이 `_has_duplicate_values` 를 **직접** import(`tests/…:15`)·호출(`:48~65`) · **8단언** 실측 · 네 칸 대조 전건 기대 일치(③) · 원복 뒤 엔진 diff 0 · sha256 복귀 · `I14-duplicate-unhashable-objects` 이름 그대로 `:283`(구판 `:257`) |
| **RG-3** | **closed** | drafts `AUDIT-ORDER-round-rf-t35.md:21` — 중복 문구가 **1회**(중복 제거됨 · 읽기만) |

**RG-2 docstring 정직성 — 감사자 직접 확인.** 「렌더 호출점에서 도달 불능(허용값 검사가 앞선다)」은 참이다. 호출점 1(`:492~495`)은 `or` 사슬에서 `any(reporter not in allowed_reporters …)` 가 헬퍼보다 **앞서고**, 호출점 2(`:521~525`)는 `and` 사슬에서 `all(reporter in allowed_reporters …)` 가 앞선다. `allowed_reporters = ("read-a","read-b")` 는 문자열 튜플이고 튜플 멤버십은 `==` 비교라 비해시 원소도 예외 없이 `not in` = 참으로 **단락**된다 — 어느 사슬이든 헬퍼에 닿는 시점에 원소는 전부 문자열이다. 계약 층에도 같은 차단이 이중으로 있다: `reported_by.items = $defs/read_run enum["read-a","read-b"]` · `maxItems 2` · `uniqueItems true` 이고, `_validate_convergence`(`read.py:1896`)가 유일한 프로덕션 렌더 호출(`:1936`)보다 앞선다.

## ③ Q1 ⓑ — 네 칸 대조 실출력 (감사자 직접 재현)

변조 = `return any(value in values[:index] …)` → `return len(set(values)) != len(values)` (앵커 1건 확인 후 적용).
구 시험 = `git show d29c8a2:tests/test_m22_unclassified_render_notice.py` → `tests/test_zz_audit_old_rg.py`(sha256 `399aa824…`) · 신 시험 = HEAD 판(sha256 `8c972874…` = `45895ec` = `6173b96` 판과 동일).

| | **구 시험**(`d29c8a2` 판) | **신 시험**(`45895ec` 판) |
|---|---|---|
| **무변조** | `40 passed in 0.09s` 🟢 | `41 passed in 0.09s` 🟢 |
| **`set()` 변조** | `40 passed in 0.09s` 🟢 ← **RG-2 결함 실물** | `1 failed, 40 passed in 0.11s` 🔴 |

붉은 칸의 실출력:

```
FAILED tests/test_m22_unclassified_render_notice.py::test_has_duplicate_values_does_not_assume_hashability
>       if _has_duplicate_values([{}, {}]) is not True:
>       return len(set(values)) != len(values)
E       TypeError: cannot use 'dict' as a set element (unhashable type: 'dict')
engine/render/material_spec_md.py:98: TypeError
```

원복 후 — `sha256sum engine/render/material_spec_md.py` = `7413511f16154628cd35a16a1c0a35bfab28d305343763255eb22220fd4e36ef`(기준 복귀) · `git diff --stat engine/` **빈 출력**(MF-1 엔진 diff 0) · 임시 사본 삭제.

**8단언 실측** — ⑴ `[{}, {}]`→True ⑵ `[{}, {"a":1}]`→False ⑶ `[{}, {"a":1}, {}]`→True(비인접) ⑷ `[{"a":1}, {}]`→False(역순) ⑸ `[[1],[1]]`→True ⑹ `[[1],[2]]`→False ⑺ `["read-a","read-a"]`→True ⑻ `["read-a","read-b"]`→False. ⑴~⑹ 이 `set()` 판별(비해시), ⑺⑻ 은 회귀 — 시험 주석이 그 역할 분담을 그대로 말한다.

§24 총괄 재현표와 **전건 일치**(무변조 40/41 · 변조 40 / 1 failed TypeError). §24 가 「HEAD 사본」이라 적은 것도 정당하다 — `1cbcd5b` 판과 `d29c8a2` 판 시험 파일이 바이트 동일(`399aa824…`)이다.

## ④ 신규 지적 — **0건**

`RH-*` 없음. 검토했으나 지적으로 세우지 않은 것 셋과 사유:

- **`I14` 이름** — RG-2 가 「이름이 가리키는 속성을 태우지 못한다」고 짚었고 처분은 유지를 택했다. 파일의 명명 규약이 **입력 서술형**(`I12-list-object`=`[[{}]]` · `I08-duplicate-a`=`[["read-a","read-a"]]`)이고 `I14`=`[[{}, {}]]` 는 그 규약과 일치하므로 이름 자체는 거짓이 아니다. 태우는 일은 새 헬퍼 시험이 맡았다.
- **렌더 §10 의 무방어 `', '.join(reported_by)`(`:460`)** — 10-b 와 달리 형태 방어가 없어 비해시 원소에서 `TypeError` 로 렌더가 죽는다(감사자 계측 중 실측). 그러나 프로덕션 렌더 호출은 `read.py:1936` 한 곳뿐이고 `_validate_convergence`(`:1896`)가 앞서며, 구 런 사료 `cim-fp-3` 은 현행 스키마에서 **거부된다**(위반 2건 — `text_status`·`reported_by` required). 실 산출은 `reported_by=None`→`or []`→건너뜀. **도달 불능이라 결함 아님.**
- **8단언 단일 함수** — 첫 단언 실패 시 나머지가 단락된다(칸 D 에서 실제로 그랬다). 스타일이며 판별력은 손상되지 않는다.

## ⑤ Q2 · Q3 · Q4

**Q2 — 명령되지 않은 hunk 0.**
```
$ git diff-tree --no-commit-id --name-only -r 6173b96
tests/test_m22_unclassified_render_notice.py          ← 단일 파일 · 27 insertions(+), 1 deletion(-)
```
hunk 둘 — ⑴ `@@ -12,7 +12,7 @@` import 줄에 `_has_duplicate_values` 추가(헬퍼 직접 호출에 필수) ⑵ `@@ -40,6 +40,32 @@` 새 시험 함수 26줄. 둘 다 §22 RG-2 「어떻게 닫나」(헬퍼 단위 시험 · docstring · 엔진 무접촉)에 대응. 엔진·계약·문서 접촉 0.

**Q3 — 총괄 기록 정합.**

| 항목 | 결과 |
|---|---|
| §22(RG 처분 · 축소 범위 사유) · §23(ME-1 · astra **high** 첫 적용 관측) · §24(재현표 · 네 칸 대조표) · §25 · §26(MF-1~4) | 전건 실재 |
| §25 = `final.txt` | 정규화 대조 — 전문이 선행부 77(절 제목)·**후행부 0** 으로 보존 · 2,191 B · sha256 `5aab9bd69834e8a27836fbf1031c4c84e6225e5de5284e02a8525e2288382b4f` (§24 기록 `2,191 B`·`5aab9bd6…` 일치) |
| M1b 원문 = `FINAL` | RG 판 6388 B · `504ac18a…` / audit4 판 7158 B · `f607b073…` — 둘 다 lesson 파일 안에 **후행부 0** 으로 전문 보존, 선행부는 「★ 이 절은 총괄 저작이며 도전 원문이 아니다」 저자 명시 절(규율 10) |
| 커밋 메시지 | `6173b96` — 「레인 보고 전문은 D-20260903-04 §24」 **오기 실재**, §24 말미 MF-2 마커가 정정(커밋 메시지는 고칠 수 없으므로 여기 기록) ✓ · `1cbcd5b`·`d29c8a2`·`45895ec`·`b1adfc1` 넷 다 반경·서술 정합, **문서 밖 접촉 0** |
| HANDOFF 19·20차 | `:16`(19차) · `:10`(20차) 실재 · 20차의 「기록 = §24 · 레인 보고 §25」는 정확 |
| DISPOSITIONS | RG 3행(`:275~277`) · ME 1행(`:278`) · MF 4행(`:279~282`) · 지적 열거 줄 3파일 정합 |
| 관문 7종 | plain·`-O` **전건 exit 0 · FAILS=0** · `check_failure_table --self-test` = `mutations=36 rejected=36` exit 0 |
| 전체 스위트 | plain `811 passed in 136.83s` **exit 0** (§24 기록 `811 passed in 134.79s` 와 계수 일치) |

**Q4 — 종결 자격: 충족.** 신규 지적 0 · RG-1~RG-3 **전건 closed**. 「계열 종결」 선언은 Owner 의 것이다.

**남은 것**(발주문이 든 다섯 외):
1. 시험 docstring 의 「도달 불능」 주장을 지키는 기계가 없다 — 호출점의 `or`/`and` 순서나 `allowed_reporters` 가 바뀌면 주장이 조용히 낡는다(방어가 살아나는 방향이라 무해하나 문언은 틀리게 된다).
2. 10-b 의 규격 밖 방어(형태·길이·허용값·중복) 전부가 스키마 검증 뒤에서는 도달 불능이다 — 존재 근거가 「시험 픽스처와 행위시법」이라는 사실이 코드·문서 어디에도 적혀 있지 않고, 같은 성질의 §10 목록은 방어가 없다. 두 자리의 정책 차이를 한 줄로 성문화할 값어치가 있다.

## ⑥ [미검증]

1. **전체 스위트 `-O`** — 발주문이 plain 1모드만 명했다. §24·HANDOFF 20차의 `811 passed, 1 warning` 을 인용한다(대상 시험 파일 단독 `-O` 는 `41 passed, 1 warning` 로 직접 확인).
2. **「DISPOSITIONS N행」의 계수 정의** — HANDOFF 17차 146 / 19차 168 은 §1 처분표 실측(147 / 169)과 **두 시점 모두 정확히 1** 차이다. 일관된 오차이므로 정의 차이(id 가 `V` 인 자문 판정 행 제외 등)로 보이나 정의가 문서화되지 않아 확정하지 못했다. 판정에 영향 없음.
3. **재감사 3 원문의 레인 원본 대조** — `pd-lanes/opus-audit-round-rf-t35/` 에 `FINAL` 이 없고 `out.txt`/`raw.json` 뿐이라 전문 동일성을 sha256 으로 닫지 않았다(발주문이 지정한 대조 대상은 RG 레인 보고와 M1b 원문 둘이며 그 둘은 닫았다).
4. **§10 경로의 전수 진입점** — 프로덕션 호출점 1개와 스키마 선행 검증으로 도달 불능을 논증했으나, 시험 밖 모든 호출 경로를 전수하지는 않았다.

## 종료 조건

```
$ git rev-parse HEAD                → b1adfc1194700bd14bdff50889de58f62acf728f
$ git status --short                → ?? .audit-sandbox        (한 줄)
$ sha256sum engine/render/material_spec_md.py
                                    → 7413511f…4e36ef          (기준 복귀 · 임시 변조 원복)
$ ls …/pd-audit7-basetemp           → No such file or directory (0항 · 삭제 완료)
$ find . -name __pycache__ …| wc -l → 0
$ find . -name .pytest_cache …      → 0
/tmp 생성물                          → 없음(중간 산출 2건 즉시 삭제 · pkill 미사용)
정본 리포                            → HEAD b1adfc1 · status 무출력(무변경)
```

VERDICT: PASS
