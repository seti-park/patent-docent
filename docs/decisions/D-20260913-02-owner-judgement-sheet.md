# D-20260913-02 — Owner 판독 요청 절 설계 (재정 T58 ③ · 좌석 M4 저작 · 재정 T59 상신용)

**지위.** 설계 메모(총괄 문서 · 원장 아님). 적용은 하지 않았다 — §7 의 diff 는 재정 뒤 M3 가 집행할 초안이다. 헌장·재정 문언은 판단 대상이 아니다.

## §1 무엇을 만드는가

Owner 육성: 「결과물 중 확신이 없거나 자신감이 떨어지는 부분, 애매한 부분이 있다면 판정지로 제공해주면 내가 직접 눈으로 보고 판독해줄게.」(T58 ③)

비유 하나. 시험지를 채점자에게 넘길 때 학생이 「이 문항은 자신 없음」 포스트잇을 붙여 두면, 채점자는 전체를 다시 풀지 않고 그 자리만 본다. 포스트잇은 답이 틀렸다는 증거가 아니고 점수도 아니다. 어디를 볼지 가리키는 손가락일 뿐이다.

**지금 없는 것** — CP1 판독본(SPEC §1.5)은 「기계가 보증하지 못한 것」(§7 도면 유래 수치 · §8 접지 예외 · §10 미분류 종속 · §11 맹검 메모 · §12 수치 인벤토리)을 모은다. 전부 **기계가 판정 불가를 선언한 자리**다. 레인 자신이 「붙이긴 했는데 조응이 확실치 않다」고 느낀 자리는 어디에도 남지 않는다. 09-01 실물에서 접지 56건은 구조 검사를 전부 통과했고, `[0021]`처럼 청구항을 그대로 되풀이한 요약 문단에 붙은 접지와 `[0117]`처럼 어휘가 다른 문단에 붙은 접지가 같은 모습으로 놓여 있다.

**더하는 것** — 레인이 항목 하나를 가리켜 이유 한 문장을 붙이는 필드 하나(`review_requests[]`), 그것을 CP1 판독본이 한 절(§8-b)로 모아 렌더하는 코드, Owner 판정을 봉투에 남길 필드 하나. **안 바뀌는 것** — §9.

## §2 ⑴ 자기 신고 표지 — 자리와 꼴

**결정.** 항목 안의 필드가 아니라 **재료 명세 최상위 배열 `review_requests[]`** 하나. 원소 = `{target, reason}`. `target` 은 항목 ID(`M<n>`) 또는 청구항 경로(`CL-n` · `CL-n/eK` · `CL-n/aK`). `reason` 은 **KR 자유문 한 문장** — 「무엇이 확실치 않고 Owner 가 무엇을 보면 판가름나는가」. 열거형 없음 · 점수 없음. 선택 필드 `refs[]`(`quote_ref` 재사용 — 레인이 가리키고 싶은 반대 문단·도면). 러너가 `read_run`·`task` 를 붙여 `convergence.json#review_requests[]` 에 **전 레인 합집합**을 싣는다(정본 `material-spec.json` 에는 read-a 것만).

| 레인 | 붙일 수 있는 `target` |
|---|---|
| `decompose`(read-a·read-b 각자) | `CL-n` 종속 분류 · `CL-n/eK` 요소 경계 · `CL-n/aK` 부착점(`attaches_to`) |
| `ground-*` | 자기 접지 항목 `M<n>`(조응 의심) |
| `synthesize` | 자기 `implication`·`positioning`·`figure_note`·`fact(derived·figure-sourced)` 항목 |

**두 분해가 다르게 신고하면 합치지 않는다** — 각각 `read_run` 을 달고 나란히 렌더한다(`screening_memos` 원리 · 재정 P-U4: 일치·불일치 자체가 신호). read-b 의 `M<n>` 은 read-a 와 번호가 다르므로(`lanes/id-map.json`) 분해 레인은 청구항 경로로만 가리킨다.

**근거.** ⓐ 스키마 다섯 정의(`component_item`·`grounding_item`·…)가 전부 `additionalProperties:false` 라 항목 안에 넣으면 다섯 곳을 고치고 다섯 렌더 경로가 생긴다. 배열 하나면 스키마 한 정의 · 렌더 한 절 · 봉투 한 필드로 닫힌다. ⓑ 값 공간이 열거형이면 그것은 카탈로그이고 등재는 재정(규율 7 · D7). 자유문은 「레인이 실제로 느낀 것」을 그대로 남기며, 열거형은 레인을 가장 가까운 칸으로 몰아 이유를 잃게 한다. ⓒ `basis.confidence ∈ {stated, inferred}` 는 함의의 **근거 종류**이지 불확신이 아니므로 재사용하지 않는다(§9). ⓓ 이 필드는 자기 신고이므로 **어떤 검사의 입력도 되지 않는다**(SPEC §9.34 · D9). 검사가 이 값을 읽는 순간 레인은 검사를 통과시키는 방향으로 신고를 조정한다.

**버린 대안.** ① 항목별 필드 `review_request` — 위 ⓐ. ② `search_note` 확장(접지에 이미 KR 자유문이 있다) — 접지에만 있고 분해·통합에 없으며, 예외 신고와 조응 의심이 한 문장에 섞이면 §8 이 흐려진다.

## §3 ⑵ 판독본의 「Owner 판독 요청」 절

**위치 = 새 절 `## 8-b ★ Owner 판독 요청 — 레인 자기 신고 (재정 T58 ③)`**, §8 접지 예외 바로 뒤 · §9 drop 앞. §7·§8 과 **나란히 두고 합치지 않는다**. 근거: §7·§8·§10 은 기계가 전건 도출한 목록(증거 등급 = 결정론)이고 이 절은 자기 신고(등급 = 반향)다. 한 절에 섞으면 Owner 가 두 등급을 같은 무게로 읽는다. 같은 `target` 이 §7·§8·§10 에도 있으면 항목 머리에 `(§8 에도 있음)` 포인터만 단다. §0 봉투 안내에 「§8-b 요청은 `review_adjudicated[]` 로 답한다」 한 줄을 더한다.

**정렬** = 청구항 경로 순(CL-1 → CL-25 · 요소 → 부가) → 항목 ID 순. 같은 target 의 read-a·read-b 신고는 한 블록에 묶는다. **비어 있을 때** = `_요청 0 건 — 레인이 판독을 요청한 자리가 없다. 이것은 「확신 있음」의 증거가 아니다(자기 신고는 반향이다 · SPEC §9.34). §7·§8·§10 은 그대로 본다._`

**한 항목의 렌더** — Owner 가 원문을 다시 열지 않도록 여섯 조각을 붙인다.

1. 머리: `target` · kind · 청구항 경로 · `label_en` · 신고 레인(`read_run/task`)
2. 항목 문장(EN verbatim): 구성요소 `text_verbatim` / 접지는 대상 구성요소 문장 / 함의 `statement_en` / 포지셔닝 `asserted_effect`
3. 레인의 이유(KR `reason`)
4. 관련 원문 조각: 접지 `spec_refs[].quote`·`figure_refs`(FIG·부호) / 함의 `evidence_quotes[]` + `derived_from` 라벨 / 종속항 `text_verbatim`·`attaches_to` / 레인이 붙인 `refs[]`
5. 두 실행의 차이(분해 target 에 한함 · `convergence_report.divergences` 에서 같은 경로를 든 줄)
6. 답 자리: `review_adjudicated[]` 한 줄 서식

**버린 대안.** ① §13.1 「상신 축」에 얹기 — 그 절은 수렴 축(집계)이고 이 절은 항목이다. ② 별도 파일 `10-read/review-sheet.md` — D6 「별도 브리핑을 두지 않는다」에 정면 저촉.

## §4 ⑵′ Owner 판정이 남는 자리

**결정.** 승인 봉투에 **`review_adjudicated[]`** 를 신설한다 — CP2 의 `flags_adjudicated[]`(`{flag_id, verdict}`)와 같은 꼴. 원소 `{target, verdict, note?}` · `verdict ∈ {confirmed, defect, undecided}` · `note` KR 선택. `checkpoint == material_approval` 이고 `convergence.json#review_requests` 가 비어 있지 않으면 **결정과 무관하게** 이 배열이 요청 전건을 덮어야 한다(요청 target 집합 = 판정 target 집합). 두 파일을 함께 읽어야 하므로 스키마 밖 · `freeze.approval-valid` 의 몫(봉투 `$comment` (8) 과 같은 구조).

`directives[]` 만으로는 부족한 이유: `directives` 는 `rejected` 에만 존재한다(스키마 (7)). Owner 가 요청 다섯 건을 전부 「조응 맞음」으로 보고 승인하면 그 판독은 어디에도 남지 않고, 다음 런에서 같은 자리를 다시 묻게 된다. `defect` 가 하나라도 있으면 이진 결정상 `rejected` + `directives` 이며 `review_adjudicated` 는 그 옆에 남는다. `undecided` 를 두는 이유는 Owner 육성 「판정 불가」가 실제 값이기 때문이고, `undecided` 채 `approved` 도 허용한다(승인은 Owner 재정이다 · D9).

**재정 필요 범위** = 어휘 3종과 「전건 덮기」 조건(검사 판정 공간 변경 · 규율 11). **재정 불요** = 필드 이름 · 렌더 서식 · 정렬.

**버린 대안.** ① `manual_verification_ack[]` 처럼 ID 배열만 — 「봤다」와 「맞다」가 구별되지 않는다. ② 판정을 `directives[]` 자유문에 섞기 — 기계가 요청과 판정을 대조할 수 없다.

## §5 ⑶ 절차 문서 문구 — 긍정형

각 절차 문서에 같은 골격의 짧은 절을 더한다(규율 4 · 초안 = §7 D).

> **확신이 서지 않는 자리는 그대로 두고 표지를 붙여라.** 네가 붙인 접지·분류·함의는 그대로 산출에 남긴다. 그 위에 `review_requests[]` 로 그 자리를 가리키고, **무엇이 확실치 않고 Owner 가 무엇을 보면 판가름나는지**를 KR 한 문장으로 적는다. 이 표지는 어떤 검사의 입력도 아니고 런을 세우지 않는다 — 적는 비용은 0 이고, 적지 않아 잃는 것은 Owner 의 눈이 갈 자리다. 표지가 붙은 자리는 CP1 에서 Owner 가 직접 본다.

**과잉·과소 신고를 어떻게 다루나 — 임계·개수 목표를 두지 않는다**(D15). 대신 둘을 둔다. ⓐ **형식 요건**: `reason` 은 「무엇을 보면 판가름나는가」를 들어야 한다 — 「확실치 않음」 한 마디는 손가락이 아니다(사람이 CP1 에서 본다 · 기계 검사 아님). ⓑ **사후 관찰**: 봉투의 `review_adjudicated[]` 가 런마다 쌓인다. 요청이 전부 `confirmed` 로 돌아오는 레인, 요청이 없던 자리에서 `directives` 가 나오는 레인 — 둘 다 배치 리뷰의 관찰 재료이지 판정 규칙이 아니다(SPEC §9.35 「그때까지 판정 규칙을 만들지 않는다」와 같은 유보). 새 원장은 만들지 않는다 — 봉투 자체가 기록이다.

**버린 대안.** ① 「n 건 이내로」 — 임계는 굿하트 미끼(D15). ② 「사소한 것은 적지 마라」 — 금지형이며 레인이 「사소」를 스스로 정하게 한다(규율 4).

## §6 ⑷ 뒤 스테이지로의 확장 원칙

원리는 하나다 — **자기 신고는 판정을 트리거하고 판정은 Owner 표면(체크포인트)이 한다. 신고는 검사 입력이 아니고 점수가 아니다.** compose 의 `[narrative]` 는 이미 이 꼴의 자기 신고(근거 불요 서사의 자기 신고 · 규율 2)이고, gate 결함 목록은 기계 도출(§7·§8 과 같은 등급)이다. CP2 에서 둘을 §8-b 와 같은 방식으로 **나란히 · 합치지 않고** 렌더하면 어긋나지 않는다. 지금 남길 것 = 필드 이름 `review_requests[]` 와 봉투 필드 `review_adjudicated[]` 를 스테이지 공통으로 쓴다는 것뿐. design·compose 산출 계약에 넣는 것은 각 스테이지 설계 때 한다(T58 ③ 말미).

## §7 적용 초안 diff (적용하지 않았다 · M3 집행용)

**A. `reader/schemas/material-spec.schema.json`** — v0 미동결(N15) · minor 상향 `0.8.0 → 0.9.0` · `$comment` 이력 추기.

```diff
 "required": ["schema", ..., "provenance", "extensions"],
+"required": [..., "extensions", "review_requests"],
 "properties": {
+  "review_requests": {
+    "$comment": "레인 자기 신고(재정 T58 ③ · T59). 검사 입력 아님 — CP1 §8-b 렌더와 봉투 review_adjudicated[] 대조에만 쓴다. 빈 배열 필수(생략은 누락과 '없음'을 구별하지 못한다).",
+    "type": "array", "minItems": 0,
+    "items": { "$ref": "#/$defs/review_request" } },
 "$defs": {
+  "review_request": {
+    "type": "object", "additionalProperties": false,
+    "required": ["target", "reason"],
+    "properties": {
+      "target": { "type": "string",
+                  "pattern": "^(M[0-9]+|CL-[0-9]+(/(e[0-9]+(/e[0-9]+)*|a[0-9]+))?)$" },
+      "reason": { "type": "string", "minLength": 1 },
+      "refs":   { "type": "array", "items": { "$ref": "#/$defs/quote_ref" } } } }
```
`reason` 은 KR 예외 목록(`$comment` 「drop_signal.reason·search_note 만 KR」)에 셋째로 등재. `target` 해소는 `read.pointer-resolve` 에 넣지 **않는다**(자기 신고를 검사 대상으로 만들지 않기 위해 — 유령 target 은 렌더가 「해소 불가」로 표기).

**B. `contracts/schemas/convergence.schema.json`** — `review_requests[]` 신설. 원소 = A 의 정의 + `read_run`(`$defs.read_run`) + `task`(`lane.sub_lanes[].id`) 필수. `phase: early` 에서는 분해 두 실행분만.

**C. `contracts/stages/read.yaml#owner_checkpoint.mandatory_surfaces`**

```diff
+    - list: review_requests
+      why: "레인 자기 신고 — 기계 검사 밖의 조응·분류·해석 판단을 Owner 가 직접 볼 자리(재정 T58 ③). 검사 근거가 아니며 비어 있음은 확신의 증거가 아니다(SPEC §9.34)."
```
같은 파일 `lane.sub_lanes[].scope` 는 손대지 않는다. (참고: 이 파일의 좌석 값은 아직 T58 ② 집행 전 `opus-5` 다 — 별건 M3.)

**D. `reader/procedure/*.md`** — `10-decompose.md` §5 뒤 · `20-grounding.md` §5 뒤 · `30-synthesis.md` §5 뒤에 §5 본문의 인용 절을 「## n. Owner 판독 요청 — 확신이 서지 않는 자리」로 삽입(target 표는 §2 표의 해당 행만). `40-output-contract.md` §1~§3 JSON 예시에 `"review_requests": [ { "target": "CL-16/a1", "reason": "…KR…" } ]` 한 줄씩 · §5 금지표는 **손대지 않는다**.

**E. `engine/lanes/plan.py`** — `DECOMPOSE_SCHEMA`·`GROUNDING_SCHEMA`·`SYNTHESIS_SCHEMA` 의 `properties` 에 `"review_requests": {"type": "array"}` (required 에 넣지 않음 — 응답 거부 사유가 되지 않게). `engine/stages/read.py#assemble_spec`(529행)이 각 payload 의 배열에 `read_run`·`task` 를 붙여 모으고 `reader/lib/run_checks.py#to_convergence_payload`(115행) 에 `review_requests=` 인자로 넘긴다(`screening_memos=` 와 같은 경로).

**F. `engine/render/material_spec_md.py`** — `render()` 안 `# -- 9. drop 신호` 주석(422행) 직전에 삽입. `§0` 안내(150행 뒤)에 한 줄 추가.

```python
# -- 8-b. Owner 판독 요청 (재정 T58 ③) --------------------------------
requests = convergence.get("review_requests") or []
out("## 8-b. ★ Owner 판독 요청 — 레인 자기 신고 (재정 T58 ③)")
out(); out("레인이 스스로 확신이 서지 않는다고 가리킨 자리다. **자기 신고는 반향이다**(SPEC §9.34) —")
out("여기 없다고 확실한 것이 아니고, 여기 있다고 틀린 것이 아니다. 봉투 `review_adjudicated[]` 로 전건 답한다."); out()
if not requests:
    out("_요청 0 건 — 레인이 판독을 요청한 자리가 없다. 「확신 있음」의 증거가 아니다. §7·§8·§10 은 그대로 본다._"); out()
for target, group in _group_by_target(requests):          # 정렬 = 청구항 경로 → M id
    head = _describe_target(spec, target)                  # kind · claim_ref · label_en · 해소 불가 표기
    out(f"### `{target}` — {head}" + _also_in(target, convergence))   # "(§8 에도 있음)"
    out(f"> {_target_sentence(spec, target)}")             # EN verbatim 문장
    for r in group: out(f"- **{r['read_run']}/{r['task']}** 의 이유: {r['reason']}")
    for line in _related_quotes(spec, target, group): out(line)   # spec_refs·figure_refs·evidence_quotes·refs[]
    for line in _divergence_lines(convergence, target): out(line) # 분해 target 만
    out(f"- 답 자리: `{{target: {target}, verdict: confirmed|defect|undecided}}`"); out()
```

**G. `contracts/schemas/approval-envelope.schema.json`**

```diff
+"review_adjudicated": {
+  "$comment": "CP1 §8-b 요청에 대한 Owner 항목별 판정(재정 T59). 요청 전건 덮기 조건은 두 파일을 읽어야 하므로 freeze.approval-valid 의 몫(규율 (8) 과 같은 구조).",
+  "type": "array",
+  "items": { "type": "object", "additionalProperties": false,
+             "required": ["target", "verdict"],
+             "properties": { "target": { "type": "string", "minLength": 1 },
+                             "verdict": { "enum": ["confirmed", "defect", "undecided"] },
+                             "note": { "type": "string" } } } }
```

**H. `docs/SPEC.md` §1.5 「CP1 이 반드시 보는 목록」 표** 에 행 추가:

```
| `review_requests[]` | 레인 자기 신고 전건 — `{target, reason, refs?, read_run, task}` · 판독본 §8-b(재정 T58 ③·T59) | 기계 검사는 구조만 보증한다(read.yaml ground-dependent 주석 · M-03). 조응·분류·해석의 판단이 필요한 자리를 레인이 가리키고 Owner 가 본다. 자기 신고는 반향이므로(§9.34) 검사 근거가 아니며 비어 있음은 확신의 증거가 아니다 |
```
봉투 표에 `review_adjudicated[]` 행 · §6.3 이력에 `0.9.0` 한 줄.

## §8 목업 — 09-01 실물에서 고른 5건 (§8-b 서식 그대로)

09-01 런에는 이 필드가 없었다. 아래는 「기계 검사 밖의 판단을 요구한다」는 내 판단으로 고른 자리이며 `reason` 은 내가 레인 자리에서 썼다.

```markdown
## 8-b. ★ Owner 판독 요청 — 레인 자기 신고 (재정 T58 ③)

### `CL-13/a1` — addition · CL-13 · attaches_to `CL-1/e2` (read-a) / `CL-1/e2/e1` (read-b)
> a respective score generated based on distance between a query embedding and a respective memory value embedding
- **read-a/decompose** 의 이유: 관련도 점수가 한정하는 것이 「메모리 접근」(e2)인지 그 안의 「메모리 객체」(e2/e1)인지 규약 ①②로 갈리지 않아 ④ 등장 순서로 골랐다 — 어느 요소를 한정하는지 봐 달라.
- **read-b/decompose** 의 이유: 점수는 메모리 값에 붙으므로 더 깊은 e2/e1 로 보았으나 e2 도 성립한다.
- 두 실행의 차이: `addition-attachment` 축 — 정본에만 `… | accessing … memory data …`, 비교본에만 `… | wherein the interaction memory datastore comprises …`
- 답 자리: `{target: CL-13/a1, verdict: confirmed|defect|undecided}`

### `M91` — grounding · 대상 `M35`(CL-16/a1 · analytical-content predictions not exposed on the user interface)
> wherein the plurality of predictions for analytical content are not exposed on a user interface associated with the query
- **read-a/ground-dependent** 의 이유: 둘째 인용 [0117] 의 「raw outputs」가 청구항의 「predictions for analytical content」와 같은 것인지 어휘가 달라 확실치 않다 — 같은 것으로 읽어도 되는지 봐 달라.
- 명세서 [0450]: “the plurality of predictions for analytical content are not exposed on a user interface associated with the query”
- 명세서 [0117]: “The raw outputs may not be surfaced to the user.”
- 도면 FIG-1 (124, 122)
- 답 자리: `{target: M91, verdict: …}`

### `M97` — grounding · 대상 `M41`(CL-18/a5 · matching the current memory object to a prior memory object)
> matching the current memory object to a prior memory object
- **read-a/ground-dependent** 의 이유: 첫 인용 [0021] 은 청구항을 그대로 되풀이한 요약 문단이라 독립 근거가 아니고, 둘째 [0089] 는 「query … retrieve relevant entries … update」라 「matching」을 말하는지 확실치 않다.
- 명세서 [0021]: “In some implementations, the example method includes matching the current memory object to a prior memory object.”
- 명세서 [0089]: “Memory model 105 can query interaction memory datastore 110 to retrieve relevant entries for new information and update the relevant entries based on the new information.”
- 도면 FIG-5 (500, 402) · 탐색 기록: 매칭 동작 자체에는 도면부호가 없다.
- 답 자리: `{target: M97, verdict: …}`

### `M130` — implication · basis `spec` · confidence `inferred`
> FIG. 8, FIG. 9 and FIG. 10 encode a three-way choice about where conflict resolution happens, and the disclosure deliberately declines to settle it. …
- **read-a/synthesize** 의 이유: 「deliberately declines」는 출원인 의도의 귀속이며 원문은 세 방식을 병렬로 적을 뿐이다 — 의도 귀속 없이 「세 방식을 병기한다」로 읽어야 하는지 봐 달라.
- 근거 인용: “This can offload the conflict resolution/interpretation task to a runtime execution of one or more models …” · “Runtime queries can be processed in full view of all retrieved memories.”
- 파생 원천: M69 · M70 · M71 · M92
- 답 자리: `{target: M130, verdict: …}`

### `M140` — implication · basis `claim` · confidence `inferred`
> The claim set carries antecedent-basis defects that a national-phase examiner will raise. Claim 16 recites the plurality of predictions … although that antecedent arises only in claim 15. Claims 4, 11 and 12 recite the one or more memory values … claim 1 … never introduces memory values at all. …
- **read-a/synthesize** 의 이유: 「examiner will raise」는 법적 예측이라 원문으로 확인할 수 없다 — 선행 근거 부재 자체(CL-1 에 「memory values」 미도입)만 사실로 남기고 예측은 뺄지 봐 달라.
- 근거 인용: “16. The method of any of the preceding claims, wherein the plurality of predictions for analytical content are not exposed …” · CL-1 “retrieving … the one or more memory values based on a relevance …”
- 파생 원천: M68 · M80 · M81 · M91
- 답 자리: `{target: M140, verdict: …}`
```

## §9 바뀌지 않는 것

CP1 질문 문구 · 봉투의 이진 결정(`approved`/`rejected` · 조건부 승인 없음) · 결정론 검사의 관할(자기 신고는 어느 검사의 입력도 아니다 · D7 · 규율 6) · D6(별도 브리핑 없음 — 절은 판독본 안) · `basis.confidence` 의 의미 · `search_note`·`screening_memos` 의 자리 · 09-01 런 산출 · 레인 프롬프트의 긍정형 규율(규율 4) · 점수·등급·임계 부재(규율 5 · D15).

## Owner 재정 안건 — T59

- **① `review_requests[]` 신설(재료 명세 최상위 · `{target, reason(KR 자유문), refs?}` · 열거형 없음 · 검사 입력 아님)** — 값 공간 신설이므로 재정. 채택 / 항목별 필드로 / 기각.
- **② 봉투 `review_adjudicated[]` 어휘 = `{confirmed, defect, undecided}` + 「요청 전건 덮기」를 `freeze.approval-valid` 가 집행** — 검사 판정 공간 변경(규율 11). 채택 / 어휘 교정 / 덮기 조건 없이 기록만.
- **③ `refs[].quote` 를 `read.verbatim` 대상에 넣는가** — 넣으면 검사 관할 확장(규율 6), 안 넣으면 레인이 가리킨 반대 문단이 다듬어질 수 있다. 권고 = **넣지 않는다**(자기 신고를 검사 대상으로 만들지 않는다 · 렌더가 verbatim 아님을 표기하지 않음).
- **④ `undecided` 채 `approved` 허용** — 권고 = 허용(승인은 Owner 재정 · D9).
- 재정 불요(총괄 재량): 절 번호 `8-b` 와 위치 · 렌더 서식 · 정렬 · 절차 문서 문구 · `reader_version` 0.9.0 · plan.py 응답 계약(optional) · SPEC 표 행 · 사후 관찰을 봉투에만 두고 새 원장을 만들지 않는 것.
