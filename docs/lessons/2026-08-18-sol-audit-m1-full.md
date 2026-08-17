# sol 독립 감수 원문 — M1 READ 모듈 (2026-08-18)

**보존 근거.** 재정 2026-08-18 **N7 ①**(모든 외부 감수·검증 산출물은 수령 즉시 **원문 그대로** `docs/lessons/`에 보존, 처분표·요약은 원문 포인터로만).

| 항목 | 값 |
|---|---|
| 감수자 | GPT-5.6-sol, reasoning effort max, read-only, 교차벤더 독립 |
| 발주 대상 | `2214b99edf3f05bfd0773a0c4abcac083c401702` (범위 `df72690..`) |
| 실제 체크아웃 | `4170ffd` — 대상보다 문서 1커밋 뒤. 감수자가 `git show 2214b99:...`로 대상 시점 처분 문서를 읽고 `git diff 2214b99..HEAD`가 문서 1건뿐임을 확인했다 |
| 판정 | **FAIL** — BLOCKER 4 / MAJOR 5 / MINOR 0. 감수자 문언: *"M1 must not close."* |
| 발주 요건 | ① N14 요구사항표 14행의 "구현으로 해소" 검토 ② 코드↔계약↔스펙 정합 ③ M0.6 생존 지적 재대조(N7 ②) ④ M1이 만든 법의 자체 감사표(S1~S23) 정직성 |
| 실행 비고 | 1차 호출은 600s 예산 초과로 산출 없이 종료. 2차 호출을 연장 예산으로 재실행해 본 보고를 받았다. `.venv/bin/pytest -q`는 read-only 샌드박스의 임시 디렉터리 부재로 **기동 전** 실패했고, 감수자가 `-s -p no:cacheprovider` 등가 실행(149 passed / 43 setup errors, 전부 `tmp_path` 부재)과 `--collect-only`(192 tests)로 **환경 실패와 제품 실패를 구별**했다 |

**본문은 아래 구분선 다음부터 원문 그대로다.** 요약·정정·재배열을 하지 않았다. 이 감수의 처분은 `docs/decisions/D-20260818-03-m1-audit.md`이며, 그 처분표는 이 원문의 **색인이지 대체물이 아니다**.

---

# Verdict: FAIL

**BLOCKER 4 / MAJOR 5 / MINOR 0. M1 must not close.**

The requested target is `2214b99edf3f05bfd0773a0c4abcac083c401702`. The checkout was one docs-only commit later, `4170ffd`; `git diff 2214b99..HEAD` changes only `docs/decisions/D-20260818-02-m1-read.md`. I audited target code/tests unchanged and read the target decision document with `git show 2214b99:...`. Worktree was clean; nothing was modified.

## BLOCKER

### B-01 — The lane ID “repair” makes ordinary READ output impossible to freeze

Location: [engine/lanes/plan.py:29](/home/laptop/projects/patent-docent/engine/lanes/plan.py:29), [engine/lanes/plan.py:376](/home/laptop/projects/patent-docent/engine/lanes/plan.py:376), [engine/lanes/plan.py:464](/home/laptop/projects/patent-docent/engine/lanes/plan.py:464), [reader/lib/freeze_integrity.py:60](/home/laptop/projects/patent-docent/reader/lib/freeze_integrity.py:60), [tests/test_m2_read.py:927](/home/laptop/projects/patent-docent/tests/test_m2_read.py:927), [ground-dependent request:47](/home/laptop/projects/patent-docent/runs/openai-us20260147854a1-m1-smoke/10-read/lanes/read-a/ground-dependent/batch-0/request.md:47), [synthesis request:26](/home/laptop/projects/patent-docent/runs/openai-us20260147854a1-m1-smoke/10-read/lanes/read-a/synthesize/batch-0/request.md:26).

Error: planner S19 assigns 1,000-wide disjoint bands and explicitly says gaps are harmless. Freeze enforces the opposite invariant: every first freeze must contain contiguous `M1..Mn`, with no gaps. `assemble_spec` only concatenates and sorts; it does not renumber. The “prevention” therefore guarantees `freeze.id-monotonic` failure whenever later lanes obey their bands.

The stated test verifies only that request bands exist and do not overlap. It never assembles the responses or invokes freeze, so it proves the local planner property while missing the lifecycle contradiction.

Falsifying evidence: the committed smoke responses contain:

- decompose: `M1..M42`
- independent grounding: `M43..M63`
- dependent grounding: `M100..M120`, which also violates its assigned `M1043..M2042` band
- synthesis: `M2043..M2088`

I assembled those exact responses in memory. All nine READ rows reproduced the coordinator’s PASS counts, but freeze returned:

```text
items 130 first M1 last M2088
freeze.id-monotonic fail
lifecycle.id-contiguous:
M1..M2088 중 결번 M64 ... M99, M121 ...
```

This is the same self-deception pattern described in the order: the planner test and planner implementation share the same narrow assumption; the independent freeze invariant falsifies both. S19 is not closed.

Confidence: **100%**.

### B-02 — CP1 approval can approve the wrong checkpoint, wrong run, and wrong file

Location: [approval-envelope.schema.json:8](/home/laptop/projects/patent-docent/contracts/schemas/approval-envelope.schema.json:8), [approval-envelope.schema.json:87](/home/laptop/projects/patent-docent/contracts/schemas/approval-envelope.schema.json:87), [engine/stages/freeze.py:152](/home/laptop/projects/patent-docent/engine/stages/freeze.py:152), [engine/stages/freeze.py:188](/home/laptop/projects/patent-docent/engine/stages/freeze.py:188), [SPEC.md:414](/home/laptop/projects/patent-docent/docs/SPEC.md:414), [SPEC.md:422](/home/laptop/projects/patent-docent/docs/SPEC.md:422), [tests/test_m2_read.py:546](/home/laptop/projects/patent-docent/tests/test_m2_read.py:546).

Error: `freeze.approval-valid` never checks that:

- `checkpoint == "material_approval"`;
- `envelope.run_id` equals the current run;
- `target.path == "10-read/material-spec.json"`;
- the resolved target remains inside the run root.

It loads `10-read/material-spec.json` separately, but validates the envelope digest against whatever `target.path` names. Thus a valid `ship_approval`, a foreign `run_id`, or a digest for `run.yaml`/another existing file can authorize freezing the current material spec. `../` components can also escape the run root.

Falsifying evidence: the schema tool deliberately accepts `accept/approval-envelope.ship-approved.json`. A search of `freeze.py` finds no use of `checkpoint` or `run_id`; `target.path` is simply joined at line 190. Existing tests always construct the proper checkpoint/current run/default target and test only a stale digest. No test exercises identity binding.

This bypasses the Owner checkpoint rather than merely misreporting it.

Confidence: **100%**.

### B-03 — N14-13 is expressly only partially resolved, so the ledger’s closing condition is unmet

Location: [ruling N14:21](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-02-N14-N15.md:21), [SPEC.md:3914](/home/laptop/projects/patent-docent/docs/SPEC.md:3914), [SPEC.md:3932](/home/laptop/projects/patent-docent/docs/SPEC.md:3932), [M0.6 audit:83](/home/laptop/projects/patent-docent/docs/lessons/2026-08-18-sol-audit-m06-full.md:83).

Error: the controlling ledger says M1 closes only when the re-audit demonstrates that the transferred items were “resolved by implementation.” The requirements table and coordinator decision both label N14-13 **partial**. Markush, conditional, category-switching, and means-plus-function relations still have no typed operators.

The implementation merely declares `alternative-form` unreachable and rejects an instance that uses it. That prevents silent acceptance; it does not represent or parse the relations identified by M0.6 M-06. This is precisely narrow closure of a broad finding.

Falsifying evidence: `invalid/dependency-type-alternative-form.json` exists and is correctly rejected, but it tests only the unreachable enum. The five parser forms still produce only `single`, `multiple-and`, or `multiple-or`.

Confidence: **100%**.

### B-04 — The real-patent “integration smoke” was not an execution of the implemented READ contract

Location: [D-20260818-02:246](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:246), [D-20260818-02:278](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:278), [D-20260818-02:282](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:282), [D-20260818-02:288](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:288), [engine/stages/read.py:349](/home/laptop/projects/patent-docent/engine/stages/read.py:349), [engine/stages/read.py:463](/home/laptop/projects/patent-docent/engine/stages/read.py:463), [contracts/stages/read.yaml:71](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:71), [lane-log.json:1](/home/laptop/projects/patent-docent/runs/openai-us20260147854a1-m1-smoke/10-read/lanes/lane-log.json:1).

Error: the decision says stopping after `read-b` decomposition was “contract compliance,” then two paragraphs later admits the implemented runner does `read-a` complete → `read-b` complete → convergence and that early convergence is unimplemented. Those statements cannot both be true.

The committed smoke directory has no:

- `material-spec.json` or `.md`;
- claim-tree files;
- grounding/positioning/drop-signal documents;
- `convergence.json`;
- CP1 approval or frozen artifact.

Its lane log contains only three rows, omitting the committed read-a synthesis and read-b decomposition responses. This violates the repository’s own `test_lane_log_records_every_round_trip` invariant.

No `retry(1)` was performed after convergence failed. No rerun demonstrates that the newly added decomposition boundary rules caused convergence to pass.

The convergence implementation also remains internally inconsistent:

- `reader-rules.yaml` says addition attachment requires Jaccard ≥ 0.95 but omits the structured `threshold` field at [reader-rules.yaml:564](/home/laptop/projects/patent-docent/reader/reader-rules.yaml:564).
- [convergence.py:169](/home/laptop/projects/patent-docent/reader/lib/convergence.py:169) silently applies 0.95, while [convergence.py:137](/home/laptop/projects/patent-docent/reader/lib/convergence.py:137) reports `threshold: null`.
- Re-execution on the committed responses gives addition attachment `6/36 = 0.1667`, not the decision’s `0.2000`.
- The decision itself admits that true attachment may be to another addition, while the schema restricts `attaches_to` to an element at [material-spec.schema.json:297](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:297). That is acknowledged structural information loss.
- The cited requirement test at [test_m1_reader.py:823](/home/laptop/projects/patent-docent/tests/test_m1_reader.py:823) tests only tree reparenting, not all six axes or the addition-attachment invariant.

The detector correctly detected a failure. That is not evidence that M1 passed, and “working as designed” cannot turn a failed, incomplete, manually sequenced run into completed integration evidence.

Confidence: **100%**.

## MAJOR

### M-01 — Stage I/O and access contracts do not describe actual behavior

Location: [contracts/stages/read.yaml:111](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:111), [contracts/stages/freeze.yaml:19](/home/laptop/projects/patent-docent/contracts/stages/freeze.yaml:19), [contracts/stages/freeze.yaml:26](/home/laptop/projects/patent-docent/contracts/stages/freeze.yaml:26), [engine/stages/freeze.py:311](/home/laptop/projects/patent-docent/engine/stages/freeze.py:311), [engine/stages/freeze.py:324](/home/laptop/projects/patent-docent/engine/stages/freeze.py:324), [SPEC.md:1155](/home/laptop/projects/patent-docent/docs/SPEC.md:1155), [engine/paths.py:4](/home/laptop/projects/patent-docent/engine/paths.py:4), [engine/paths.py:188](/home/laptop/projects/patent-docent/engine/paths.py:188).

Error:

- READ actually executes `read.source-digest`; `contracts/stages/read.yaml` omits it from `checks_before_exit` and failure handling.
- Freeze reads and rewrites `run.yaml`, but `run.yaml` is absent from its inputs, `may_read`, and outputs. The access table assigns its sole W owner to source.
- `engine/paths.py` says `PROVENANCE.md` and `10-read/lanes/` are undeclared exceptions and hardcodes them. Both are now declared outputs in the source/read contracts, so the documentation is false and contract path changes would not move those two implementation paths.
- `freeze.id-monotonic` contract text describes only prior-revision preservation, omitting the first-freeze contiguity rule that invalidates the planner.

All `implemented_by`/`ruleset` coordinates that are actually present in the YAML files resolve to existing files. The defect is completeness and behavioral correspondence: several implemented checks/writes are not declared at all.

Confidence: **100%**.

### M-02 — The coordinate repairs verify existence, not evidence; the same defect class remains open

Location: [tests/test_m1_corpus.py:102](/home/laptop/projects/patent-docent/tests/test_m1_corpus.py:102), [tests/test_m1_corpus.py:141](/home/laptop/projects/patent-docent/tests/test_m1_corpus.py:141), [tests/test_m1_corpus.py:172](/home/laptop/projects/patent-docent/tests/test_m1_corpus.py:172), [check_schema_enforcement.py:199](/home/laptop/projects/patent-docent/tools/check_schema_enforcement.py:199), [SPEC.md:2090](/home/laptop/projects/patent-docent/docs/SPEC.md:2090), [SPEC.md:2109](/home/laptop/projects/patent-docent/docs/SPEC.md:2109).

Error: the three corrected requirements-table coordinates are accurate now:

- the combined coverage test independently mutates shared ownership and reverse mismatch;
- both coverage mutants exist;
- the alternative-form mutant exists and is rejected by `read.dependency-parse`.

But the new guard only checks that a function with the cited name exists and that a mutant filename appears in the manifest. An empty or unrelated test body under that name passes. It does not validate implementation paths, pytest collection, the rule asserted by the test, mutant contents, or the mutant’s expected check. Therefore it does not prevent the requested class, “test has the name but different content.”

Likewise, the §2.8 test compares only row numbers with parenthesized numbers in `$comment`; it does not compare content despite its docstring saying “numbering and content.” Semantic drift with all numbers retained passes.

`check_schema_enforcement.py` requires `enforcement_evidence` to be a nonempty string but does not resolve the node ID. The current self-reference coordinate is genuinely correct—the test constructs a self-reference and requires `pointer.no-self-reference`—but a ghost coordinate would also pass the tool.

There is already further unenforced drift:

- §2.8 says “below 11” although there are 14 rows.
- §2.8 says `check_spec_refs.py` performs the table collation; it does not.
- [SPEC.md:1639](/home/laptop/projects/patent-docent/docs/SPEC.md:1639) still shows obsolete `convergence/v0` with `checks` as an object; the canonical schema requires an array at [convergence.schema.json:32](/home/laptop/projects/patent-docent/contracts/schemas/convergence.schema.json:32).
- [SPEC.md:3176](/home/laptop/projects/patent-docent/docs/SPEC.md:3176) says reader/lib implements ten checks; the registry contains eleven.
- [SPEC.md:3291](/home/laptop/projects/patent-docent/docs/SPEC.md:3291) and [SPEC.md:3617](/home/laptop/projects/patent-docent/docs/SPEC.md:3617) still show `reader_version: 0.3.0`.
- [test_m2_read.py:1513](/home/laptop/projects/patent-docent/tests/test_m2_read.py:1513) is named as proof that paths come from contracts, but it merely checks the current hardcoded expected suffix and misses the two hardcoded exceptions.

The four new coordinate tests are useful regression alarms, but they do not justify class-level closure.

Confidence: **100%**.

### M-03 — Grounding “accuracy is guaranteed” is false; zero exceptions remain unadjudicated

Location: [reader/procedure/20-grounding.md:7](/home/laptop/projects/patent-docent/reader/procedure/20-grounding.md:7), [contracts/stages/read.yaml:33](/home/laptop/projects/patent-docent/contracts/stages/read.yaml:33), [reader/lib/coverage.py:27](/home/laptop/projects/patent-docent/reader/lib/coverage.py:27), [reader/lib/pointers.py:147](/home/laptop/projects/patent-docent/reader/lib/pointers.py:147), [D-20260818-02:240](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:240).

Error: procedure and stage contract say `pointer-resolve` and `coverage` guarantee grounding accuracy. They guarantee only structural existence, kind, ownership, reverse references, and declared found/exception states. Neither tests that the quoted passage semantically supports the component or that a numeral is actually attached to that component in the figure.

The coordinator’s later disclosure is substantially honest when it says the probe does not prove correctness. The stronger phrase “proved not fabricated” is still too broad for figure numerals: checking that a short numeral occurs somewhere in the entire patent does not bind it to the cited figure, component, or quote.

Falsifying evidence: I reproduced the disclosed values:

- locator/quote containment: 78/78;
- 26 locator paragraphs;
- `[0188]`: 24 reference occurrences across 23 distinct items;
- 16 distinct numeral strings all occur somewhere globally.

But 28 of the 78 numeral occurrences do not occur in any specification quote attached to their own grounding item. This does not prove those groundings wrong; it proves the global-existence probe does not establish their linkage.

Because the smoke produced no material-spec CP1 surface or approval envelope, zero exceptions received no human adjudication. The proper conclusion is “not disproved and structurally consistent,” not “accuracy guaranteed.”

Confidence: **98%**.

### M-04 — Multiple claims labeled “measured” do not reproduce

Location: target object `2214b99:docs/decisions/D-20260818-02-m1-read.md:155-185`, [D-20260818-02:96](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:96), [D-20260818-02:250](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:250), [D-20260818-02:175](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:175).

Error and falsifying evidence:

- Target §5.3 records K1 `513`, validator mutants `35`, and pytest `183`. Target-equivalent code measures K1 `515`, mutants `36`, and collects `192` tests.
- The requester’s stated `190 passed` is likewise not the target suite inventory; two tests added by `604f3ca` and `2214b99` make 192.
- S17 says captions changed `0 → 53`; the committed source through the committed `ReadView.figure_captions()` returns **52**. The rule regex has 77 raw matches before figure-ID deduplication.
- Addition attachment is reported as `0.2000`; direct execution returns `6/36 = 0.1667`.
- The post-target commit admits the evidence block was left stale twice. Even after its update, [D-20260818-02:178](/home/laptop/projects/patent-docent/docs/decisions/D-20260818-02-m1-read.md:178) says pointer mutants `6`; the tool currently reports `7`.

Control measurements that did reproduce:

- paragraph markers `282 → 277`;
- source bytes `293,362`;
- element Jaccard `0.5909`;
- tree Jaccard `0.5714`;
- dependent signatures `1.0000`;
- leading-conjunction normalization `0.7500`;
- `[0188]` paragraph length 3,312.

This is recurrence of overstated/stale measurement reporting, not random rounding error.

Confidence: **100%**.

### M-05 — The full M0.6 M-10 defect was improperly placed outside M1 jurisdiction

Location: [SPEC.md:3942](/home/laptop/projects/patent-docent/docs/SPEC.md:3942), [M0.6 audit:107](/home/laptop/projects/patent-docent/docs/lessons/2026-08-18-sol-audit-m06-full.md:107), [material-spec.schema.json:242](/home/laptop/projects/patent-docent/reader/schemas/material-spec.schema.json:242), [SPEC.md:1222](/home/laptop/projects/patent-docent/docs/SPEC.md:1222), [ruling N13:47](/home/laptop/projects/patent-docent/docs/decisions/ruling-20260818-01-N1-N13.md:47).

Error: M0.6 M-10 concerns the current canonical material-spec contract: singular assignee/priority structure, missing bibliographic dimensions, and `drop_signal` cross-project semantic mismatch. M1 explicitly owns and revised that schema and defines `reader/` as the portable historian interface.

N13 authorizes deferring the **family-field** addition until historian bootstrap. It does not dispose of the rest of M-10. The non-M1 table expands that narrow N13 deferral into deferral of the entire D14 contract defect.

Eight of the nine non-M1 classifications are reasonable module/Owner assignments. M-10 is the exception: at minimum, the non-family portions are an M1 contract-surface defect and cannot all be postponed by citing historian’s future existence.

Confidence: **92%**.

## N14 requirements table — row-by-row adjudication

All stated implementation files/anchors exist. The remaining issue is whether they implement and falsify the full finding.

| Row | Verdict | Independent judgment |
|---|---|---|
| N14-1 | **RESOLVED** | Exact B-04 attack is tested: quote/span unchanged, only `value_raw` fabricated; `value.quoted-span` rejects it. |
| N14-2 | **RESOLVED** | Self-reference and two-node cycle tests are substantive. Current validator-scope evidence points to the correct self-reference test. |
| N14-3 | **RESOLVED** | Derived-from-derived fact is constructed and rejected; direct inline source spans remain allowed. |
| N14-4 | **RESOLVED** | Ack tests separately exercise missing IDs, phantom IDs, and exact equality. This does not cure B-02 approval identity bypass. |
| N14-5 | **RESOLVED** | Corrected combined test independently checks shared `material_id` and reverse `claim_ref`; both cited mutants exist and execute. |
| N14-6 | **RESOLVED** | Test requires both schema rejection and `value.en-only`, so it genuinely exercises the second-layer script check. |
| N14-7 | **RESOLVED** | Missing source claim and zero parsed claims are independently rejected; own-claim text containment is also implemented. |
| N14-8 | **PARTIALLY RESOLVED** | Six code branches exist, but the cited test covers only tree edges, true nested addition attachment is unrepresentable, threshold/report data disagree, and no post-repair real run converged. |
| N14-9 | **RESOLVED** | Payload hash, one-way transition, cyclic chain, and inactive terminal are substantively tested. |
| N14-10 | **RESOLVED** | Seven-branch union and parser/render comparison exist. Baseline corpus exercises scalar, range, inequality, tolerance, set, date, and identifier. |
| N14-11 | **RESOLVED BY UPSTREAM RULING** | N15 supplies the authority the original finding said was absent; version/schema-major test is accurate. This is law plus faithful documentation, not a code-only resolution. |
| N14-12 | **RESOLVED against the stated requirement** | `[가설]`, three open questions, per-figure rows, and recomputation basis exist and are tested. This does not ratify the provisional formula. |
| N14-13 | **PARTIALLY RESOLVED** | Corrected mutant coordinate is accurate, but it proves only explicit rejection of unreachable `alternative-form`; the original typed-operator defect remains. |
| N14-14 | **RESOLVED** | `pytest 9.1.1` is recorded. Other statistics in the same evidence block being stale is M-04 above. |

Result: **12 RESOLVED / 2 PARTIALLY RESOLVED / 0 UNRESOLVED.** N14 requires implementation resolution, not partial resolution; therefore the table itself fails the closing condition.

## Code ↔ contract ↔ spec determinations

- The schema `$comment` entries (1)–(14) and the current §2.8 table rows substantively correspond now.
- The surrounding sentence still says “11,” and the new test binds only the numbers—not the content.
- `contracts/glossary.md` §2.1/§2.2 membership is factual: all §2.1 IDs have implementations, and I found no §2.2 ID implemented. The registry test does not enforce correct placement, only that the ID appears somewhere in the document.
- Every `implemented_by` and ruleset file coordinate actually declared in `contracts/stages/*.yaml` exists. Completeness is not checked, which is why `read.source-digest` and freeze’s `run.yaml` mutation escape.
- `reader/lib/**` generally consumes the schema/rules as stated. The concrete exception is convergence’s missing structured threshold and hidden default/report mismatch.
- Stage output/check declarations do not fully match actual behavior, as detailed in M-01.
- The canonical convergence schema and the live SPEC example conflict: array versus legacy object.

## Re-collation of the 24 M0.6 findings

Canonical original: [2026-08-18-sol-audit-m06-full.md:21](/home/laptop/projects/patent-docent/docs/lessons/2026-08-18-sol-audit-m06-full.md:21).

| M0.6 ID | Current judgment | Ground |
|---|---|---|
| B-01 | **RESOLVED** | Decision artifact and ledger chain are committed. |
| B-02 | **PARTIALLY RESOLVED** | Material self-reference is enforced; `completion_proxy: 999` remains open under M10. |
| B-03 | **RESOLVED** | Verdict-row status/violation and ruleset-tuple contradictions are now rejected. |
| B-04 | **RESOLVED** | Exact fabricated-value attack is rejected by implementation. |
| M-01 | **RESOLVED** | Depth-one source restriction and CP1 ack set equality are implemented. |
| M-02 | **PARTIALLY RESOLVED** | Standalone grade pattern was added, but the actual lint executor remains absent. |
| M-03 | **UNRESOLVED** | Two publish prerequisites still lack machine evidence coordinates; Owner/module deferral remains. |
| M-04 | **RESOLVED** | Unauthorized certainty was withdrawn; rule is explicitly provisional with recomputation evidence. |
| M-05 | **RESOLVED** | Numeric whitelist is required in approved CP1 envelopes. |
| M-06 | **PARTIALLY RESOLVED** | Alternative-form silent acceptance closed; typed relations remain absent. |
| M-07 | **PARTIALLY RESOLVED** | Inventory axis is closed; convergence integration/attachment remains partial. |
| M-08 | **RESOLVED** | Payload immutability and lifecycle checks exist. |
| M-09 | **RESOLVED** | Structured value types and parser/render enforcement exist. |
| M-10 | **UNRESOLVED** | Broader D14 material-contract defect remains; full jurisdiction deferral is unsound. |
| M-11 | **UNRESOLVED** | Per-sentence annotation enforcement remains M3 work. |
| M-12 | **UNRESOLVED** | `weakest_tweet` remains non-causal. |
| M-13 | **UNRESOLVED** | Semantic no-rewrite bypasses remain. |
| M-14 | **RESOLVED** | N15 supplies explicit Owner authority. |
| M-15 | **UNRESOLVED** | E26 sample relaxation remains Owner-dependent. |
| M-16 | **RESOLVED** | D1–D15 reconstruction now has per-item decision summaries and pointers. |
| M-17 | **RESOLVED for its original omission** | Prior M0.6 residual list was expanded. New M1 omissions are separately reported above. |
| m-01 | **UNRESOLVED** | Numeric copies remain in `l0-format.yaml` prose/notes. |
| m-02 | **RESOLVED** | Actual pytest version is recorded. |
| m-03 | **RESOLVED** | Later record explicitly establishes M0 as 10/11/1 and preserves the historical wrong counts. |

Total: **13 resolved / 4 partial / 7 unresolved**.

For the nine items declared outside M1 jurisdiction, the assignments for B-02/completion, M-02, M-03, M-11, M-12, M-13, M-15, and m-01 are defensible. The full M-10 assignment is not, for the reasons in M-05.

## S1–S23 and convergence-honesty review

The exact implementation repairs described for S1–S9, S11–S18, and S20–S23 generally exist. The table is nevertheless inflated or incomplete in these places:

- **S10 is only partial.** `enforcement_evidence` is mandatory but not resolved or semantically checked.
- **S17’s implementation works, but “0 → 53” is false for the committed product; it returns 52.**
- **S19 is not closed.** Its band repair directly violates freeze contiguity.
- **S8 fixed one stale `0.3.0` coordinate, but two other current SPEC examples still contain `0.3.0`.**
- **S23 is comparatively honest.** It fixes the exact set syntax but explicitly admits that no completeness check detects a fact silently omitted by a lane.
- The table omits the approval-identity bypass, stage-contract mismatches, hidden convergence threshold, unfreezable bands, and the fact that the real smoke did not execute the implemented stage sequence.

Sections 5.6–5.7 are not an honest convergence closure narrative. “The detector worked” is true. “Stopping there was contract compliance” is false for the implemented runner. “This is not M1 failure” is unacceptable as a closing conclusion when the only real-patent convergence evidence failed, was not retried, and was not regenerated after the purported procedural fix.

## Execution verification

| Command | Independent result |
|---|---|
| `python3 tools/check_spec_refs.py` | Exit 0; K1 515, K2 35, K3 14/6, K4 566, K5 0/13, K6 16, K7 5 |
| `python3 tools/check_schema_enforcement.py` | Exit 0; 35 cases; reject 22/22, accept 11/11, validator-scope 2/2 |
| `python3 tools/check_validator_enforcement.py` | Exit 0; baseline 11/11, mutants 36/36; pointer distribution 7 |
| All three tools under `python3 -O` | Same exits and counts |
| AST audit of the three tools | Zero executable `assert` nodes in each |
| `.venv/bin/pytest --version` | `pytest 9.1.1` |
| `.venv/bin/pytest -q` | Environment failure before startup: no usable temporary directory |
| Fallback `pytest -s -p no:cacheprovider tests/ -q` | 149 passed, 43 setup errors, all caused by unavailable `tmp_path`; product failure not established |
| Optimized fallback | Same 149 passed / 43 environment errors |
| Normal and optimized `--collect-only` | 192 tests collected |

The pytest environment failure is separate from product failure. It prevents me from independently certifying “192 passed,” but it does not explain or mitigate the product defects above.

“36/36” proves that the current validator rejects the 36 mutations jointly declared by the same session and that its synthetic baseline is non-vacuous. It does not prove planner/freeze composition, approval identity, real lane compliance, grounding semantics, stage contract completeness, or correctness of the law encoded by the fixtures. B-01 is a direct counterexample: every validator mutant passes while the real assembled output is unfreezable.