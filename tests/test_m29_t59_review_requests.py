# -*- coding: utf-8 -*-
"""재정 2026-09-13 T59 — 「Owner 판독 요청」 장치의 반증대.

원장 = `docs/decisions/ruling-20260913-04-T59.md`(①~④ 전건 A) · 설계 = `D-20260913-02` §7 A~H.

무엇을 고정하는가.
  ① 스키마 — 재료 명세 최상위 `review_requests[]` 필수(빈 배열 허용) · target 문법 · 봉투
     `review_adjudicated[]` 어휘 3종.
  ② 러너 — 필드 없는 응답은 **빈 배열로 정규화**(거부 아님) · 전 레인 합집합에 `read_run`·`task`
     부착 · 정본 재료에는 정본 실행분만 · 레인 소유 `M<n>` 은 최종 ID 로 재번호 · 조기 판정서는
     분해 두 실행분만.
  ③ 렌더 — `## 8-b` 절의 여섯 조각 · 정렬(청구항 경로 → 항목 ID) · 빈 절 문구 · 유령 target 은
     「해소 불가」로 표기(검사로 잡지 않는다) · 옛 재료(09-01 런)는 빈 절.
  ④ 동결 — `freeze.approval-valid` 의 전건 덮기(빠짐·유령 각각 결함) · `defect`+`approved` 실패 ·
     `undecided`+`approved` 통과.
  ⑤ 관할 — 어떤 `read.*` 검사도 이 값을 읽지 않는다(값을 바꿔도 판정 행 무변화).

규율: 도구 코드가 아니므로 맨 `assert` 를 쓰지 않고 명시 비교 + `pytest.fail` 로 적는다
(CLAUDE.md §3 — 서브프로세스 종료 코드도 명시 비교).
"""

from __future__ import annotations

import copy
import json
import os
import sys

import pytest
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m1_reader as m1  # noqa: E402
import test_m2_read as m2  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.render import material_spec_md as render_mod  # noqa: E402
from engine.stages import freeze as freeze_stage  # noqa: E402
from engine.stages.read import ID_MAP_BASENAME, lane_review_requests  # noqa: E402
from reader.lib import run_read_checks  # noqa: E402
from reader.lib.run_checks import to_convergence_payload  # noqa: E402

MATERIAL_SCHEMA = os.path.join(REPO, "reader", "schemas", "material-spec.schema.json")
ENVELOPE_SCHEMA = os.path.join(REPO, "contracts", "schemas", "approval-envelope.schema.json")
CONVERGENCE_SCHEMA = os.path.join(REPO, "contracts", "schemas", "convergence.schema.json")
BASE_SPEC = os.path.join(REPO, "tests", "fixtures", "reader", "base", "material-spec.json")

SECTION_TITLE = "## 8-b. ★ Owner 판독 요청 — 레인 자기 신고 (재정 T58 ③)"


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(load_json(path))


def errors(path: str, instance: dict) -> list[str]:
    return [error.message for error in validator(path).iter_errors(instance)]


def review_errors(path: str, instance: dict) -> list[str]:
    """`review_requests` 경로 아래의 위반만 — 판정 행 등 다른 필수 요소는 이 시험의 관심이 아니다."""
    return [
        error.message
        for error in validator(path).iter_errors(instance)
        if "review_requests" in [str(step) for step in error.absolute_path]
    ]


def section_of(markdown: str) -> str:
    start = markdown.index(SECTION_TITLE)
    end = markdown.index("## 9. drop 신호", start)
    return markdown[start:end]


def three_requests() -> list[dict]:
    """가공 코퍼스(base) 위의 요청 3건 — 청구항 경로 · 접지 항목 · 함의 항목."""
    return [
        {
            "target": "M25",
            "reason": "함의가 원문의 병렬 서술을 의도 귀속으로 읽은 것은 아닌지 봐 달라.",
            "read_run": "read-a",
            "task": "synthesize",
        },
        {
            "target": "M29",
            "reason": "둘째 인용의 어휘가 청구항과 달라 같은 것인지 확실치 않다.",
            "refs": [{"locator": "[0031]", "quote": "the channel is formed in the spreader body"}],
            "read_run": "read-a",
            "task": "ground-independent",
        },
        {
            "target": "CL-2/a1",
            "reason": "부착점이 e1 인지 e2 인지 규약으로 갈리지 않았다.",
            "read_run": "read-b",
            "task": "decompose",
        },
    ]


def convergence_for(spec: dict, requests: list[dict]) -> dict:
    return to_convergence_payload([], spec, canonical_read_run="read-a", review_requests=requests)


# ---------------------------------------------------------------------------
# ① 스키마
# ---------------------------------------------------------------------------


def test_material_schema_requires_review_requests_and_checks_target_grammar() -> None:
    """재정 T59 ① — 최상위 필수(빈 배열 허용) · target = M<n> | CL-n | CL-n/eK(/eK…) | CL-n/aK."""
    spec = load_json(BASE_SPEC)
    if errors(MATERIAL_SCHEMA, spec):
        pytest.fail(f"base 픽스처(빈 배열)가 거부됐다: {errors(MATERIAL_SCHEMA, spec)[:2]}")
    missing = copy.deepcopy(spec)
    missing.pop("review_requests")
    if not any("review_requests" in message for message in errors(MATERIAL_SCHEMA, missing)):
        pytest.fail("review_requests 를 생략한 재료가 통과했다 — 생략은 누락과 '없음'을 구별하지 못한다")
    for target in ("M25", "CL-2", "CL-1/e1", "CL-1/e2/e1", "CL-2/a1"):
        candidate = copy.deepcopy(spec)
        candidate["review_requests"] = [{"target": target, "reason": "이유 한 문장"}]
        if errors(MATERIAL_SCHEMA, candidate):
            pytest.fail(f"정당한 target {target!r} 이 거부됐다: {errors(MATERIAL_SCHEMA, candidate)[:1]}")
    for bad in (
        {"target": "FIG-1", "reason": "이유"},
        {"target": "M25", "reason": ""},
        {"target": "M25"},
        {"target": "M25", "reason": "이유", "score": 3},
    ):
        candidate = copy.deepcopy(spec)
        candidate["review_requests"] = [bad]
        if not errors(MATERIAL_SCHEMA, candidate):
            pytest.fail(f"부적격 원소가 통과했다: {bad}")


def test_envelope_schema_accepts_three_verdicts_and_rejects_others() -> None:
    """재정 T59 ② — verdict ∈ {confirmed, defect, undecided} · note 선택 · 잉여 키 거부."""
    base = load_json(os.path.join(REPO, "tests", "fixtures", "schema-enforcement", "accept", "approval-envelope.material-approved.json"))
    for verdict in ("confirmed", "defect", "undecided"):
        candidate = copy.deepcopy(base)
        candidate["review_adjudicated"] = [{"target": "M25", "verdict": verdict, "note": "메모"}]
        if errors(ENVELOPE_SCHEMA, candidate):
            pytest.fail(f"verdict {verdict!r} 가 거부됐다: {errors(ENVELOPE_SCHEMA, candidate)[:1]}")
    for bad in (
        [{"target": "M25", "verdict": "accept"}],
        [{"target": "M25"}],
        [{"target": "M25", "verdict": "confirmed", "score": 1}],
    ):
        candidate = copy.deepcopy(base)
        candidate["review_adjudicated"] = bad
        if not errors(ENVELOPE_SCHEMA, candidate):
            pytest.fail(f"부적격 판정이 통과했다: {bad}")


def test_convergence_schema_binds_read_run_and_task_and_early_phase() -> None:
    """재정 T59 ① — 합집합 원소는 read_run·task 필수 · early 국면은 decompose 만."""
    spec = load_json(BASE_SPEC)
    payload = convergence_for(spec, three_requests())
    if review_errors(CONVERGENCE_SCHEMA, payload):
        pytest.fail(f"합집합 3건이 계약을 위반한다: {review_errors(CONVERGENCE_SCHEMA, payload)[:2]}")
    anonymous = convergence_for(spec, [{"target": "M25", "reason": "이유"}])
    if not review_errors(CONVERGENCE_SCHEMA, anonymous):
        pytest.fail("read_run·task 없는 합집합 원소가 통과했다 — 익명 신고는 병기할 수 없다")
    early = to_convergence_payload(
        [], spec, phase="early", canonical_read_run="read-a",
        review_requests=[{"target": "CL-2", "reason": "이유", "read_run": "read-b", "task": "synthesize"}],
    )
    if not review_errors(CONVERGENCE_SCHEMA, early):
        pytest.fail("조기 판정서에 통합 레인의 신고가 실렸는데 통과했다 — 순서가 무너진 사실은 남아야 한다")
    early_ok = to_convergence_payload(
        [], spec, phase="early", canonical_read_run="read-a",
        review_requests=[{"target": "CL-2", "reason": "이유", "read_run": "read-b", "task": "decompose"}],
    )
    if review_errors(CONVERGENCE_SCHEMA, early_ok):
        pytest.fail(f"조기 판정서의 분해 신고가 거부됐다: {review_errors(CONVERGENCE_SCHEMA, early_ok)}")


# ---------------------------------------------------------------------------
# ② 러너
# ---------------------------------------------------------------------------


def test_lane_response_without_field_normalizes_to_empty_array() -> None:
    """메모 §7 E — 필드 없음·배열 아님 = 빈 배열(거부 아님). 있는 원소는 값을 만들지 않고 옮긴다."""
    if lane_review_requests({}) != [] or lane_review_requests(None) != []:
        pytest.fail("필드 없는 응답이 빈 배열로 정규화되지 않았다")
    if lane_review_requests({"review_requests": "not-a-list"}) != []:
        pytest.fail("배열이 아닌 값이 빈 배열로 정규화되지 않았다")
    entries = lane_review_requests(
        {"review_requests": [{"target": "M4", "reason": "이유", "refs": [], "extra": 1}, "junk"]}
    )
    if entries != [{"target": "M4", "reason": "이유", "refs": []}]:
        pytest.fail(f"원소 정규화가 다르다: {entries}")


def test_runner_defaults_to_empty_arrays_when_lanes_omit_the_field(tmp_path) -> None:
    """필드 없는 레인 응답 → 재료·판정서 모두 빈 배열이고 런은 ok 다(거부 아님 · 메모 §7 E)."""
    root, outcome, _ = m2.run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"기본 통주가 ok 가 아니다: {outcome['status']}")
    paths = RunPaths(root)
    spec = load_json(paths.material_spec_json)
    report = load_json(paths.convergence_json)
    if spec.get("review_requests") != [] or report.get("review_requests") != []:
        pytest.fail("필드 없는 응답이 빈 배열로 실리지 않았다")


def test_runner_unions_all_lanes_with_read_run_and_task(tmp_path) -> None:
    """네 레인이 신고하면 정본 재료에는 정본 실행(read-a)분만 `{target, reason, refs?}` 로, 판정서에는
    read-b 분해분까지 `read_run`·`task` 를 달고 실리며, 레인 소유 `M<n>` 은 최종 ID 로 재번호된다
    (재정 T59 ①). 조기 판정서는 분해 두 실행분만 든다."""
    payloads = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    payloads["read-a"]["decompose"]["review_requests"] = [
        {"target": "CL-2/a1", "reason": "부착점이 확실치 않다."}
    ]
    payloads["read-a"]["ground-independent"]["review_requests"] = [
        {"target": "M4", "reason": "조응이 확실치 않다.", "refs": [{"locator": "[0002]", "quote": "x"}]}
    ]
    payloads["read-a"]["synthesize"]["review_requests"] = [
        {"target": "M10", "reason": "귀속이 확실치 않다."}
    ]
    payloads["read-b"]["decompose"]["review_requests"] = [
        {"target": "CL-2/a1", "reason": "e2 로 보았으나 e1 도 성립한다."}
    ]
    root2, outcome2, _ = m2.run_read(tmp_path, payloads_by_run=payloads)
    if outcome2["status"] != "ok":
        pytest.fail(f"신고가 있는 통주가 ok 가 아니다: {outcome2['status']} / {m2.fail_rows(outcome2['rows'])}")
    paths2 = RunPaths(root2)
    spec2 = load_json(paths2.material_spec_json)
    report2 = load_json(paths2.convergence_json)
    id_map = load_json(os.path.join(paths2.lanes_dir, ID_MAP_BASENAME))
    grounding_final = id_map["read-a/grounding[0]"]["M4"]
    synth_final = id_map["read-a/synthesize"]["M10"]
    expected_spec = [
        {"target": "CL-2/a1", "reason": "부착점이 확실치 않다."},
        {"target": grounding_final, "reason": "조응이 확실치 않다.", "refs": [{"locator": "[0002]", "quote": "x"}]},
        {"target": synth_final, "reason": "귀속이 확실치 않다."},
    ]
    if spec2["review_requests"] != expected_spec:
        pytest.fail(f"정본 재료의 신고가 다르다: {spec2['review_requests']}")
    lanes = [(e["read_run"], e["task"], e["target"]) for e in report2["review_requests"]]
    expected_lanes = [
        ("read-a", "decompose", "CL-2/a1"),
        ("read-a", "ground-independent", grounding_final),
        ("read-a", "synthesize", synth_final),
        ("read-b", "decompose", "CL-2/a1"),
    ]
    if lanes != expected_lanes:
        pytest.fail(f"합집합 귀속이 다르다: {lanes}")
    if errors(CONVERGENCE_SCHEMA, report2):
        pytest.fail(f"판정서가 계약을 위반한다: {errors(CONVERGENCE_SCHEMA, report2)[:2]}")
    early = load_json(paths2.convergence_early_json)
    early_lanes = [(e["read_run"], e["task"]) for e in early["review_requests"]]
    if early_lanes != [("read-a", "decompose"), ("read-b", "decompose")]:
        pytest.fail(f"조기 판정서의 신고가 분해 두 실행분이 아니다: {early_lanes}")
    with open(paths2.material_spec_md, encoding="utf-8") as handle:
        rendered = handle.read()
    if SECTION_TITLE not in rendered or "read-b/decompose" not in section_of(rendered):
        pytest.fail("판독본 8-b 절에 read-b 분해 신고가 병기되지 않았다")


# ---------------------------------------------------------------------------
# ③ 렌더
# ---------------------------------------------------------------------------


def test_render_emits_six_pieces_sorted_claim_path_first() -> None:
    """메모 §3 — 머리 · EN 문장 · 레인 이유 · 관련 인용 · (분해 target 의) 차이 · 답 자리. 정렬 = CL → M."""
    spec = load_json(BASE_SPEC)
    convergence = convergence_for(spec, three_requests())
    convergence["convergence_report"]["divergences"] = [
        {
            "axis": "addition-attachment",
            "only_in_canonical": [spec["claims"]["dependents"][0]["additions"][0]["text_verbatim"] + " | CL-1/e1"],
            "only_in_peer": [spec["claims"]["dependents"][0]["additions"][0]["text_verbatim"] + " | CL-1/e2"],
        }
    ]
    convergence["grounding_exceptions"] = [
        {"material_id": "M29", "component": "M1", "spec": "found", "figure": "not-depicted", "search_note": "n"}
    ]
    body = section_of(render_mod.render(spec, convergence, repo=REPO))
    heads = [line for line in body.splitlines() if line.startswith("### `")]
    order = [line.split("`")[1] for line in heads]
    if order != ["CL-2/a1", "M25", "M29"]:
        pytest.fail(f"정렬이 청구항 경로 → 항목 ID 가 아니다: {order}")
    index = {item["id"]: item for item in spec["items"]}
    addition = spec["claims"]["dependents"][0]["additions"][0]
    expectations = {
        "CL-2/a1": [
            "addition · `CL-2` · attaches_to `" + addition["attaches_to"] + "`",
            "> " + addition["text_verbatim"],
            "- **read-b/decompose** 의 이유: 부착점이 e1 인지 e2 인지",
            "- 두 실행의 차이: `addition-attachment` 축 — 정본에만",
            "- 답 자리: `{target: CL-2/a1, verdict: confirmed|defect|undecided}`",
        ],
        "M25": [
            "implication · basis `" + index["M25"]["basis"] + "`",
            "> " + index["M25"]["statement_en"],
            "- **read-a/synthesize** 의 이유:",
            "- 답 자리: `{target: M25, verdict: confirmed|defect|undecided}`",
        ],
        "M29": [
            "grounding · 대상 **" + index["M29"]["component"] + "**",
            "(§8 에도 있음)",
            "> " + index[index["M29"]["component"]]["text_verbatim"],
            "- **read-a/ground-independent** 의 이유:",
            "- 명세서 `" + index["M29"]["spec_refs"][0]["locator"] + "`: “",
            "- 레인이 가리킨 원문 `[0031]`: “the channel is formed in the spreader body”",
            "- 답 자리: `{target: M29, verdict: confirmed|defect|undecided}`",
        ],
    }
    for target, fragments in expectations.items():
        start = body.index(f"### `{target}`")
        end = body.find("### `", start + 1)
        block = body[start : end if end != -1 else len(body)]
        for fragment in fragments:
            if fragment not in block:
                pytest.fail(f"{target} 블록에 조각이 없다: {fragment!r}\n{block}")
    if "M25" in body.split("### `M29`")[1] and "(§" in body.split("### `M25`")[1].split("### `M29`")[0]:
        pytest.fail("§7·§8·§10 에 없는 target 에 포인터가 붙었다")
    if "요청 0 건" in body:
        pytest.fail("요청이 있는데 빈 절 문구가 나왔다")


def test_render_marks_ghost_target_unresolvable_without_failing() -> None:
    """재정 T59 ① — 유령 target 은 검사가 아니라 렌더가 「해소 불가」로 표기한다."""
    spec = load_json(BASE_SPEC)
    convergence = convergence_for(
        spec,
        [
            {"target": "M999", "reason": "없는 항목.", "read_run": "read-a", "task": "synthesize"},
            {"target": "CL-9/a3", "reason": "없는 경로.", "read_run": "read-a", "task": "decompose"},
        ],
    )
    body = section_of(render_mod.render(spec, convergence, repo=REPO))
    for target in ("M999", "CL-9/a3"):
        block = body[body.index(f"### `{target}`") :]
        if "해소 불가" not in block.splitlines()[0]:
            pytest.fail(f"{target} 이 해소 불가로 표기되지 않았다: {block.splitlines()[0]}")
        if "- 답 자리: `{target: " + target not in block:
            pytest.fail(f"{target} 의 답 자리가 없다")


# ---------------------------------------------------------------------------
# ④ 동결 — 전건 덮기
# ---------------------------------------------------------------------------


def _run_with_requests(tmp_path):
    payloads = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    payloads["read-a"]["ground-independent"]["review_requests"] = [
        {"target": "M4", "reason": "조응이 확실치 않다."}
    ]
    payloads["read-a"]["synthesize"]["review_requests"] = [{"target": "M10", "reason": "귀속."}]
    root, outcome, _ = m2.run_read(tmp_path, payloads_by_run=payloads)
    if outcome["status"] != "ok":
        pytest.fail(f"통주가 ok 가 아니다: {outcome['status']}")
    targets = [e["target"] for e in load_json(RunPaths(root).convergence_json)["review_requests"]]
    if len(targets) != 2:
        pytest.fail(f"요청 2건을 기대했다: {targets}")
    return root, targets


def _rules_hit(outcome) -> list[str]:
    return [finding.rule for row in outcome["rows"] for finding in row.findings]


def test_freeze_requires_every_request_answered_regardless_of_decision(tmp_path) -> None:
    """재정 T59 ② — 요청 target 집합 == 판정 target 집합. 빠짐·유령은 각각 별도 결함이며 사유에 차집합이 적힌다."""
    root, targets = _run_with_requests(tmp_path)
    m2.approval_envelope(root)  # review_adjudicated 없음
    missing = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if "approval.review-complete" not in _rules_hit(missing) or missing["status"] != "halt":
        pytest.fail(f"답 없는 봉투가 통과했다: {_rules_hit(missing)} / {missing['status']}")
    messages = [f.message for row in missing["rows"] for f in row.findings if f.rule == "approval.review-complete"]
    if not any(all(t in message for t in targets) for message in messages):
        pytest.fail(f"사유에 차집합이 없다: {messages}")

    m2.approval_envelope(
        root,
        review_adjudicated=[{"target": targets[0], "verdict": "confirmed"}],
    )
    partial = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    partial_messages = [f.message for row in partial["rows"] for f in row.findings if f.rule == "approval.review-complete"]
    if not partial_messages or targets[1] not in partial_messages[0] or targets[0] in partial_messages[0].split("답 없는 요청")[1]:
        pytest.fail(f"부분 답의 차집합이 정확하지 않다: {partial_messages}")

    m2.approval_envelope(
        root,
        review_adjudicated=[{"target": t, "verdict": "confirmed"} for t in targets]
        + [{"target": "M77", "verdict": "confirmed"}],
    )
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if "approval.review-no-phantom" not in _rules_hit(phantom):
        pytest.fail(f"유령 판정이 통과했다: {_rules_hit(phantom)}")

    # 결정과 무관하다 — rejected 봉투도 전건을 덮어야 한다.
    m2.approval_envelope(root, decision="rejected")
    rejected = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if "approval.review-complete" not in _rules_hit(rejected):
        pytest.fail(f"rejected 봉투가 전건 덮기를 면제받았다: {_rules_hit(rejected)}")

    m2.approval_envelope(
        root, review_adjudicated=[{"target": t, "verdict": "confirmed", "note": "조응 맞음"} for t in targets]
    )
    exact = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if exact["status"] != "ok":
        pytest.fail(f"전건 confirmed 인데 실패했다: {m2.fail_rows(exact['rows'])}")


def test_freeze_rejects_defect_under_approved_but_allows_undecided(tmp_path) -> None:
    """메모 §4 · 재정 T59 ④ — defect 가 있으면 이진 결정상 rejected 여야 하고, undecided 채 승인은 허용된다."""
    root, targets = _run_with_requests(tmp_path)
    m2.approval_envelope(
        root,
        review_adjudicated=[
            {"target": targets[0], "verdict": "defect", "note": "조응 아님"},
            {"target": targets[1], "verdict": "confirmed"},
        ],
    )
    defect = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if "approval.review-defect-approved" not in _rules_hit(defect) or defect["status"] != "halt":
        pytest.fail(f"defect + approved 가 통과했다: {_rules_hit(defect)} / {defect['status']}")

    m2.approval_envelope(
        root,
        review_adjudicated=[
            {"target": targets[0], "verdict": "undecided", "note": "판정 불가"},
            {"target": targets[1], "verdict": "confirmed"},
        ],
    )
    undecided = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if undecided["status"] != "ok":
        pytest.fail(f"undecided + approved 가 거부됐다(재정 T59 ④ 위반): {m2.fail_rows(undecided['rows'])}")


def test_freeze_without_requests_does_not_demand_adjudication(tmp_path) -> None:
    """요청 0 건이면 배열을 요구하지 않는다 — 다만 유령 판정은 여전히 잡는다."""
    root, _, _ = m2.run_read(tmp_path)
    m2.approval_envelope(root)
    plain = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if plain["status"] != "ok":
        pytest.fail(f"요청 없는 런의 정상 봉투가 거부됐다: {m2.fail_rows(plain['rows'])}")
    m2.approval_envelope(root, review_adjudicated=[{"target": "M4", "verdict": "confirmed"}])
    phantom = freeze_stage.run(run_root=root, spec_version=1, rules=m2.RULES)
    if "approval.review-no-phantom" not in _rules_hit(phantom):
        pytest.fail(f"요청 없는 런의 유령 판정이 통과했다: {_rules_hit(phantom)}")


# ---------------------------------------------------------------------------
# ⑤ 관할 — 검사는 이 값을 읽지 않는다
# ---------------------------------------------------------------------------


def test_read_checks_ignore_review_requests_entirely() -> None:
    """재정 T59 ① · 규율 6 — 유령 target·바뀐 이유·refs 유무가 read.* 판정 행을 한 칸도 바꾸지 않는다."""
    golden = m1.golden_spec()
    golden["review_requests"] = []
    baseline = [row.to_row_dict() for row in run_read_checks(m1.context(golden, peer_spec=m1.golden_spec()))]
    if not baseline:
        pytest.fail("검사 행이 없다 — 시험이 공허하다")
    variants = [
        [{"target": "M999", "reason": "유령 target."}],
        [{"target": "CL-1/e1", "reason": "다른 이유.", "refs": [{"locator": "[9999]", "quote": "fabricated"}]}],
        [{"target": "M1", "reason": "a"}, {"target": "M1", "reason": "b"}],
    ]
    for requests in variants:
        candidate = m1.golden_spec()
        candidate["review_requests"] = requests
        rows = [row.to_row_dict() for row in run_read_checks(m1.context(candidate, peer_spec=m1.golden_spec()))]
        if rows != baseline:
            changed = [(a["check_id"], a, b) for a, b in zip(baseline, rows) if a != b]
            pytest.fail(f"review_requests 가 판정을 바꿨다: {changed[:2]}")
