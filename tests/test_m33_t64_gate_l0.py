# -*- coding: utf-8 -*-
"""M33 — `gate` 스테이지 L0 결정론 층 + strip + round-trip(재정 2026-09-13 T64 ② · 집행 ③).

모델 호출 없음(전부 결정론). 픽스처 = `ledgers/regression/golden/rc-0001-numberless/` 의 자족 스냅샷(읽기만 · tmp 로
복사). 결함 판은 시험 안에서 문자열 치환으로 만든다 — 골든 파일은 고치지 않는다. 런 -3 동결본·convergence.json 은
읽기만 한다(⑫).

★ 골든 표본의 알려진 어긋남(총괄에게): `thread.annotated.md` 프런트매터의 `spec_digest`(722c…)는 같은 폴더
`material-spec.frozen.json` 의 sha256(1c89… = `meta.json#spec_digest`)과 **다르다**. 그래서 이 시험은 meta.json 이 적은
지문이 파일 실측과 같음을 먼저 확인하고, 주석본은 프런트매터 지문을 실측값으로 치환해 쓴다.
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import sys

import pytest
import yaml
from jsonschema import Draft202012Validator

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.annotation import index as index_mod  # noqa: E402
from engine.annotation import parse as parse_mod  # noqa: E402
from engine.annotation import reassemble as reassemble_mod  # noqa: E402
from engine.annotation import strip as strip_mod  # noqa: E402
from engine.gate import sentence_count  # noqa: E402
from engine.gate.l0 import L0Context, L0Law, load_rules, load_rules_from_law  # noqa: E402
from engine.gate.l0 import rules_numeric  # noqa: E402
from engine.gate.l0.weighted_length import weighted_length  # noqa: E402
from engine.paths import RunPaths  # noqa: E402
from engine.stages import StageError, StageHaltError, sha256_bytes, sha256_file  # noqa: E402
from engine.stages import gate as gate_stage  # noqa: E402
from tools import drive_partial_read as drv  # noqa: E402

GOLDEN = os.path.join(REPO, "ledgers", "regression", "golden", "rc-0001-numberless")
GOLDEN_THREAD = os.path.join(GOLDEN, "thread.annotated.md")
GOLDEN_FROZEN = os.path.join(GOLDEN, "material-spec.frozen.json")
GOLDEN_META = os.path.join(GOLDEN, "meta.json")
SCHEMAS = os.path.join(REPO, "contracts", "schemas")
GOLDEN_RUN_ID = "example-xx0000000a1-cable-guide"
VARIANT = "v2"
DIGEST_RE = re.compile(r"spec_digest: sha256:[0-9a-f]{64}")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(read_json(os.path.join(SCHEMAS, f"{name}.schema.json")))


def schema_errors(name: str, instance) -> list[str]:
    return [error.message for error in validator(name).iter_errors(instance)]


# ---------------------------------------------------------------------------
# 픽스처 — 법 사본 · 런 작업장
# ---------------------------------------------------------------------------


def make_law(destination: str, *, l0: dict | None = None, sheet: dict | None = None) -> str:
    """`contracts/` 사본. `l0`·`sheet` 로 계약 문서를 통째로 바꿔 넣을 수 있다(값 공간 실험은 사본에서만)."""
    shutil.copytree(os.path.join(REPO, "contracts"), os.path.join(destination, "contracts"), dirs_exist_ok=True)
    if l0 is not None:
        with open(os.path.join(destination, "contracts", "l0-format.yaml"), "w", encoding="utf-8") as handle:
            yaml.safe_dump(l0, handle, allow_unicode=True, sort_keys=False)
    if sheet is not None:
        with open(os.path.join(destination, "contracts", "format-parameters.yaml"), "w", encoding="utf-8") as handle:
            yaml.safe_dump(sheet, handle, allow_unicode=True, sort_keys=False)
    return destination


def l0_doc() -> dict:
    return yaml.safe_load(read(os.path.join(REPO, "contracts", "l0-format.yaml")))


def sheet_doc() -> dict:
    return yaml.safe_load(read(os.path.join(REPO, "contracts", "format-parameters.yaml")))


def golden_body() -> str:
    return read(GOLDEN_THREAD).split("---\n", 2)[2]


def frontmatter(*, run_id: str, variant: str, digest: str, effort: str = "max", spec_version: int = 1) -> str:
    return (f"---\nrun_id: {run_id}\nvariant: {variant}\npen: {{ vendor: anthropic, model: opus-5, effort: {effort} }}\n"
            f"spec_version: {spec_version}\nspec_digest: {digest}\n---\n")


def make_run(root: str, *, spec: dict | None = None, body: str | None = None, whitelist=None, variants=(VARIANT,),
             run_id: str = GOLDEN_RUN_ID, manifest: dict | None = None, partial_until: str = "gate",
             defect_only=()) -> str:
    """골든 자족 스냅샷을 tmp 런으로 편다. `spec` 을 주면 그 동결본으로(지문은 실측으로 다시 계산)."""
    run_root = os.path.join(root, "runs", run_id)
    frozen_dir = os.path.join(run_root, "15-frozen")
    os.makedirs(frozen_dir, exist_ok=True)
    frozen = os.path.join(frozen_dir, "material-spec.v1.json")
    if spec is None:
        shutil.copyfile(GOLDEN_FROZEN, frozen)
    else:
        with open(frozen, "w", encoding="utf-8") as handle:
            json.dump(spec, handle, ensure_ascii=False, indent=2, sort_keys=True)
    os.chmod(frozen, 0o444)
    digest = sha256_file(frozen)
    meta = {
        "schema": "run/v0", "run_id": run_id, "status": "active", "run_kind": "partial", "partial_until": partial_until,
        "engine": {"commit": "e" * 40, "worktree": None}, "numeric_whitelist": list(whitelist or []),
        "frozen": [{"spec_version": 1, "path": "15-frozen/material-spec.v1.json", "spec_digest": digest}],
    }
    with open(os.path.join(run_root, "run.yaml"), "w", encoding="utf-8") as handle:
        yaml.safe_dump(meta, handle, allow_unicode=True, sort_keys=False)
    os.makedirs(os.path.join(run_root, "20-design"), exist_ok=True)
    blueprint = read_json(os.path.join(GOLDEN, "blueprint.json"))
    blueprint["spec_digest"] = digest
    blueprint["run_id"] = run_id
    with open(os.path.join(run_root, "20-design", "blueprint.json"), "w", encoding="utf-8") as handle:
        json.dump(blueprint, handle, ensure_ascii=False, indent=2, sort_keys=True)
    text = frontmatter(run_id=run_id, variant=VARIANT, digest=digest) + (body if body is not None else golden_body())
    for variant in variants:
        os.makedirs(os.path.join(run_root, "40-compose", variant), exist_ok=True)
        with open(os.path.join(run_root, "40-compose", variant, "thread.annotated.md"), "w", encoding="utf-8") as handle:
            handle.write(text.replace(f"variant: {VARIANT}\n", f"variant: {variant}\n", 1))
    for variant in defect_only:
        os.makedirs(os.path.join(run_root, "40-compose", variant), exist_ok=True)
        with open(os.path.join(run_root, "40-compose", variant, "material-defect.md"), "w", encoding="utf-8") as handle:
            handle.write("---\nmaterial_ids: [M1]\ndefect_kind: missing-fact\nevidence: x\nblocked_slots: [2]\n---\n")
    if manifest is not None:
        os.makedirs(os.path.join(run_root, "30-figures", "assets"), exist_ok=True)
        with open(os.path.join(run_root, "30-figures", "assets", "manifest.json"), "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
    return run_root


def run_gate(run_root: str, law: str = REPO, **kwargs) -> dict:
    return gate_stage.run(run_root=run_root, repo=law, **kwargs)


def verdict_of(run_root: str, variant: str = VARIANT) -> dict:
    return read_json(os.path.join(run_root, "50-gate", variant, "verdict.json"))


def rows_by_id(verdict: dict) -> dict[str, dict]:
    return {row["check_id"]: row for row in verdict["checks"]}


def context_for(text: str, *, law: str = REPO, spec: dict | None = None, meta: dict | None = None,
                manifest: dict | None = None, digest: str | None = None) -> L0Context:
    """규칙 단위 시험용 컨텍스트 — 파싱 오류 0 이면 strip·인덱스까지 채운다."""
    law_obj = L0Law.load(law)
    spec = spec if spec is not None else read_json(GOLDEN_FROZEN)
    slot_enum = tuple(law_obj.param("format-parameters.yaml#slot_enum"))
    parsed = parse_mod.parse(text, slot_enum=slot_enum)
    stripped = index = None
    if not parsed.errors:
        stripped = strip_mod.strip(text)
        index = index_mod.build_index(parsed, stripped, run_id=GOLDEN_RUN_ID, variant=VARIANT, spec_version=1)
    contract = yaml.safe_load(read(os.path.join(law, "contracts", "stages", "gate.yaml")))
    layers, _ = gate_stage.inactive_layers(contract)
    return L0Context(law=law_obj, repo=law, parsed=parsed, stripped=stripped, index=index, frozen=spec,
                     spec_digest=digest or str(parsed.frontmatter.get("spec_digest", "")), meta=meta or {"run_kind": "partial"},
                     manifest=manifest, inactive=layers, url_re=gate_stage.URL_RE, slot_enum=slot_enum)


def rule(rule_id: str, law: str = REPO):
    return {r.id: r for r in load_rules(law)}[rule_id]


def thread_text(tweets: list[tuple[str, str, list[str]]], *, digest: str = "sha256:" + "0" * 64) -> str:
    """`(slot, fig, [문장+태그 …])` 목록 → 주석본 전문."""
    blocks = []
    for n, (slot, fig, lines) in enumerate(tweets, start=1):
        blocks.append(f"## T{n} {{slot: {slot}, fig: {fig}}}\n" + "\n".join(lines))
    return frontmatter(run_id=GOLDEN_RUN_ID, variant=VARIANT, digest=digest) + "\n" + "\n\n".join(blocks) + "\n"


def filler(n: int, tag: str = "[narrative]") -> str:
    """가중 글자 n 의 ASCII 문장(마침표 포함) + 태그."""
    body = ("x" * (n - 1)) + "."
    return body + tag


SIX_OK = [
    ("hook", "none", ["Hook line.[M7]"]),
    ("stop", "none", [filler(200, "[M1]")]),
    ("stop", "none", [filler(200, "[M2]")]),
    ("pivot", "none", [filler(200, "[M3]")]),
    ("landing", "none", ["Landing line.[M8]"]),
    ("tail", "none", ["Tail line.[narrative]"]),
]


@pytest.fixture
def run_root(tmp_path) -> str:
    return make_run(str(tmp_path))


# ---------------------------------------------------------------------------
# ⓪ 골든 자족성
# ---------------------------------------------------------------------------


def test_golden_snapshot_digest_is_self_consistent() -> None:
    meta = read_json(GOLDEN_META)
    actual = sha256_file(GOLDEN_FROZEN)
    if meta["spec_digest"] != actual:
        pytest.fail(f"golden meta.json spec_digest {meta['spec_digest']} ≠ 동결본 실측 {actual}")
    in_thread = DIGEST_RE.search(read(GOLDEN_THREAD)).group(0).split(": ", 1)[1]
    # 알려진 어긋남(모듈 docstring) — 여기서는 기록만 한다. 골든이 고쳐지면 이 줄이 참이 된다.
    if in_thread != actual:
        sys.stderr.write(f"[golden] thread.annotated.md 프런트매터 spec_digest {in_thread} ≠ 동결본 {actual}\n")


# ---------------------------------------------------------------------------
# ⑴ 로더
# ---------------------------------------------------------------------------


def test_loader_loads_thirteen_rules_with_item_level_veto() -> None:
    rules = load_rules(REPO)
    doc = l0_doc()
    expected_ids = [entry["id"] for entry in doc["rules"]]
    if [r.id for r in rules] != expected_ids or len(rules) != 13:
        pytest.fail(f"규칙 13 이 계약 순서로 로드되지 않았다: {[r.id for r in rules]}")
    retired = {entry["id"] for entry in doc["retired"]}
    if len(retired) != 3 or retired & {r.id for r in rules}:
        pytest.fail(f"retired 3 이 로드되었다: {retired}")
    vetoes = {r.id: r.veto for r in rules}
    if vetoes != {entry["id"]: entry["veto"] for entry in doc["rules"]}:
        pytest.fail("veto 가 파일 값과 다르다")
    if [rid for rid, veto in vetoes.items() if not veto] != ["numeric.unreviewed-use"]:
        pytest.fail(f"veto false 는 numeric.unreviewed-use 하나여야 한다: {vetoes}")


def test_loader_rejects_resurrected_retired_and_unimplemented(tmp_path) -> None:
    doc = l0_doc()
    doc["rules"].append({"id": doc["retired"][0]["id"], "stage": "thread", "veto": True})
    law = make_law(os.path.join(str(tmp_path), "law-retired"), l0=doc)
    with pytest.raises(StageError):
        load_rules(law)
    doc = l0_doc()
    doc["rules"].append({"id": "format.made-up", "stage": "thread", "veto": True})
    law = make_law(os.path.join(str(tmp_path), "law-unimpl"), l0=doc)
    with pytest.raises(StageError):
        load_rules(law)
    doc = l0_doc()
    del doc["rules"][1]["veto"]
    law = make_law(os.path.join(str(tmp_path), "law-noveto"), l0=doc)
    with pytest.raises(StageError):
        load_rules_from_law(L0Law.load(law))


# ---------------------------------------------------------------------------
# ⑵ 가중 글자 수
# ---------------------------------------------------------------------------


def test_weighted_length_follows_sheet(tmp_path) -> None:
    config = L0Law.load(REPO).param("format-parameters.yaml#weighted_length")
    url_re = gate_stage.URL_RE
    cases = {
        "a" * 100: 100,
        "한" * 10: 20,
        "https://example.com/very/long/path": 23,
        "\U0001F469‍\U0001F4BB": 2,          # 여성 기술자(ZWJ 결합) = 클러스터 1 → default_weight 1회
        "see https://example.com/x now": 4 + 23 + 4,
    }
    got = {text: weighted_length(text, config, url_re) for text in cases}
    if got != cases:
        pytest.fail(f"가중 글자 수가 다르다: {got}")
    sheet = sheet_doc()
    sheet["parameters"]["weighted_length"]["value"]["ranges"].append({"start": 0xAC00, "end": 0xD7A3, "weight": 100})
    law = make_law(os.path.join(str(tmp_path), "law-ranges"), sheet=sheet)
    changed = weighted_length("한" * 10, L0Law.load(law).param("format-parameters.yaml#weighted_length"), url_re)
    if changed != 10:
        pytest.fail(f"시트 ranges 를 바꿨는데 값이 따라오지 않았다: {changed}")


# ---------------------------------------------------------------------------
# ⑶ golden 전 규칙 통과 · numeric.exhaustive 기대 행
# ---------------------------------------------------------------------------


def test_golden_passes_all_rules_and_numeric_row_is_vacuous(run_root) -> None:
    outcome = run_gate(run_root)
    state = outcome["variants"][VARIANT]
    if not state["l0_pass"] or state["decision"] != "advance":
        pytest.fail(f"golden 이 통과하지 않았다: {state}")
    verdict = verdict_of(run_root)
    expected = {"check_id": "numeric.exhaustive", "ruleset": None, "ruleset_version": None, "ruleset_size": None,
                "checked": 0, "violations": 0, "status": "pass", "vacuous": "empty-target"}
    if rows_by_id(verdict)["numeric.exhaustive"] != expected:
        pytest.fail(f"numeric.exhaustive 행이 golden meta.json 기대와 다르다: {rows_by_id(verdict)['numeric.exhaustive']}")
    rule_ids = [entry["id"] for entry in l0_doc()["rules"]]
    if [row["check_id"] for row in verdict["l0"]["checks"]] != rule_ids:
        pytest.fail("규칙 하나당 행 하나가 아니다")
    if any(row["status"] != "pass" for row in verdict["checks"]):
        pytest.fail([row for row in verdict["checks"] if row["status"] != "pass"])


# ---------------------------------------------------------------------------
# ⑷ ~ ⑧ format.*
# ---------------------------------------------------------------------------


def test_tweet_count_bounds_follow_sheet(tmp_path) -> None:
    thirteen = [SIX_OK[0]] + [SIX_OK[1]] * 10 + [SIX_OK[4], SIX_OK[5]]
    res = rule("format.tweet-count").run(context_for(thread_text(thirteen)))
    if res.row.status != "pass" and res.row.checked == 13 and len(res.defects) == 1:
        pass
    else:
        pytest.fail(f"13 트윗이 fail 이어야 한다: {res.row.to_row_dict()}")
    five = [SIX_OK[0], SIX_OK[1], SIX_OK[3], SIX_OK[4], SIX_OK[5]]
    if rule("format.tweet-count").run(context_for(thread_text(five))).row.status != "fail":
        pytest.fail("5 트윗이 fail 이어야 한다")
    sheet = sheet_doc()
    sheet["parameters"]["tweet_count"]["value"]["max"] = 14
    law = make_law(os.path.join(str(tmp_path), "law-14"), sheet=sheet)
    if rule("format.tweet-count", law).run(context_for(thread_text(thirteen), law=law)).row.status != "pass":
        pytest.fail("시트 max 14 사본에서 13 트윗이 통과해야 한다")


def test_slot_count_reports_each_violation() -> None:
    tweets = [
        ("stop", "none", [filler(200, "[M1]")]),          # hook 부재
        ("stop", "none", [filler(200, "[M2]")]),
        ("landing", "none", ["Landing one.[M8]"]),
        ("landing", "none", ["Landing two.[M8]"]),        # landing 2
        ("tail", "none", ["Tail early.[narrative]"]),     # tail 이 마지막 아님
        ("bridge", "none", ["Odd slot.[M3]"]),            # other 밖 값(파서 enum 검사 없이 규칙만 본다)
    ]
    text = thread_text(tweets)
    law_obj = L0Law.load(REPO)
    parsed = parse_mod.parse(text)                        # slot_enum 미전달 → 규칙 단독 판정
    ctx = L0Context(law=law_obj, repo=REPO, parsed=parsed, stripped=strip_mod.strip(text), index=None,
                    frozen=read_json(GOLDEN_FROZEN), spec_digest="", meta={}, url_re=gate_stage.URL_RE,
                    slot_enum=tuple(law_obj.param("format-parameters.yaml#slot_enum")))
    res = rule("format.slot-count").run(ctx)
    observed = sorted(d["observed"] for d in res.defects)
    if len(res.defects) != 4:
        pytest.fail(f"4 위반 각 1건이어야 한다: {observed}")
    if not any("hook" in o for o in observed) or not any("landing ×2" in o for o in observed) \
            or not any("tail" in o for o in observed) or "bridge" not in observed:
        pytest.fail(f"위반 종류가 빠졌다: {observed}")
    if rule("format.slot-count").run(context_for(thread_text(SIX_OK))).row.status != "pass":
        pytest.fail("정상 배치가 통과해야 한다")


def test_body_length_by_slot_follows_sheet(tmp_path) -> None:
    tweets = [
        ("hook", "none", [filler(179, "[M7]")]),          # hook 179 → pass(하한 없음)
        ("stop", "none", [filler(261, "[M1]")]),          # 261 → fail(상한)
        ("stop", "none", [filler(179, "[M2]")]),          # 179 → fail(하한)
        ("pivot", "none", [filler(200, "[M3]")]),
        ("landing", "none", ["Landing.[M8]"]),
        ("tail", "none", [filler(1000, "[narrative]")]),  # tail 1000 → pass(면제)
    ]
    res = rule("format.body-length").run(context_for(thread_text(tweets)))
    loci = sorted(d["locus"]["tweet"] for d in res.defects)
    if loci != [2, 3] or res.row.extras["weighted_char_counts"][:3] != [179, 261, 179]:
        pytest.fail(f"body-length 판정이 다르다: {loci} {res.row.extras}")
    sheet = sheet_doc()
    sheet["parameters"]["length_by_slot"]["value"]["by_slot"]["stop"]["min"] = 100
    law = make_law(os.path.join(str(tmp_path), "law-min100"), sheet=sheet)
    res2 = rule("format.body-length", law).run(context_for(thread_text(tweets), law=law))
    if sorted(d["locus"]["tweet"] for d in res2.defects) != [2]:
        pytest.fail("시트 하한을 100 으로 바꾸면 179 stop 이 통과해야 한다")


def test_stop_shape_inactive_without_manifest_and_active_with_it() -> None:
    text = thread_text([
        ("hook", "fig-01", ["Hook.[M7]"]),
        ("stop", "fig-02", [filler(100, "[M1]"), filler(60, "[M1]"), filler(60, "[M2]")]),   # 자산 1 · 문장 3 → fail
        ("stop", "fig-03", [filler(200, "[M2]")]),                                          # annotated-internal → 자산 0 → fail
        ("pivot", "fig-02", [filler(200, "[M3]")]),                                          # 자산 1 · 문장 1 → pass
        ("landing", "none", ["Landing.[M8]"]),
        ("tail", "none", ["Tail.[narrative]"]),
    ])
    res = rule("format.stop-shape").run(context_for(text))
    row = res.row.to_row_dict()
    if row["checked"] != 0 or row["vacuous"] != "empty-target" or "inactive_reason" not in res.row.extras:
        pytest.fail(f"매니페스트 없이 미가동 행이 아니다: {row} {res.row.extras}")
    manifest = {"items": [{"figure": "fig-02", "edit_class": "crop-only", "publishable": True},
                          {"figure": "fig-03", "edit_class": "annotated-internal", "publishable": False}]}
    res = rule("format.stop-shape").run(context_for(text, manifest=manifest))
    if res.row.checked != 3 or sorted(d["locus"]["tweet"] for d in res.defects) != [2, 3]:
        pytest.fail(f"합성 매니페스트 가동 판정이 다르다: {[d['observed'] for d in res.defects]}")


def test_sentence_counting_rule_from_contract() -> None:
    spec = l0_doc()["sentence_counting"]
    cases = {"One line.": 1, "Two here. And more.": 2, "See e.g. this. Fine.": 2, "Ratio 3.9 holds. Yes.": 2,
             "A. B. Example wrote it.": 1, "Really?! Yes.": 2, "no terminator": 1, "Line one.\nLine two.": 2}
    got = {text: sentence_count.count_sentences(text, spec) for text in cases}
    if got != cases:
        pytest.fail(f"문장 계수가 다르다: {got}")


def test_hashtag_link_and_images_rules() -> None:
    tweets = [
        ("hook", "fig-01+fig-02+fig-03+fig-04+fig-05", ["Hook #alpha tag.[M7]"]),                      # 해시태그 1 · fig 5
        ("stop", "none", ["x" * 149 + ". https://example.com/a#frag more words here to fill.[M1]"]),  # URL in stop
        ("stop", "none", [filler(200, "[M2]")]),
        ("pivot", "none", [filler(200, "[M3]")]),
        ("landing", "none", ["Landing.[M8]"]),
        ("tail", "none", ["Notes: https://example.com/notes#top[narrative]"]),                        # tail URL 허용
    ]
    ctx = context_for(thread_text(tweets))
    hashtag = rule("format.hashtag-zero").run(ctx)
    if [d["locus"]["tweet"] for d in hashtag.defects] != [1]:
        pytest.fail(f"해시태그 판정이 다르다(URL 속 # 은 미계수): {[d['locus'] for d in hashtag.defects]}")
    link = rule("format.no-link-in-body").run(ctx)
    if [d["locus"]["tweet"] for d in link.defects] != [2] or link.row.checked != 5:
        pytest.fail(f"링크 격리 판정이 다르다: {[d['locus'] for d in link.defects]} checked={link.row.checked}")
    images = rule("format.images-per-post").run(ctx)
    if [d["locus"]["tweet"] for d in images.defects] != [1] or images.defects[0]["observed"] != "5":
        pytest.fail(f"images-per-post 판정이 다르다: {images.defects}")


# ---------------------------------------------------------------------------
# ⑨ annotation.schema 단락 · ⑩ citation.resolve
# ---------------------------------------------------------------------------


def test_annotation_violation_short_circuits_other_rules(tmp_path) -> None:
    body = golden_body().replace("This filing claims a way to make the grit stay outside.[M7]",
                                 "This filing claims a way to make the grit stay outside. [M7]", 1)   # 태그 앞 공백
    run_root = make_run(os.path.join(str(tmp_path), "a"), body=body)
    outcome = run_gate(run_root)
    verdict = verdict_of(run_root)
    ids = [row["check_id"] for row in verdict["checks"]]
    if "format.tweet-count" in ids or "numeric.exhaustive" in ids or "strip.roundtrip-forward" in ids:
        pytest.fail(f"주석층 위반 뒤 하위 규칙 행이 나왔다: {ids}")
    if ids[1:3] != ["annotation.schema", "annotation.missing-tag"] or verdict["decision"] != "revise" or outcome["status"] != "ok":
        pytest.fail(f"단락 판정문이 다르다: {ids} {verdict['decision']}")
    if os.path.exists(os.path.join(run_root, "50-gate", VARIANT, "thread.stripped.md")):
        pytest.fail("문법 위반본에 strip 산출이 생겼다")
    # spec_digest 불일치도 annotation.schema
    run2 = make_run(os.path.join(str(tmp_path), "b"))
    path = os.path.join(run2, "40-compose", VARIANT, "thread.annotated.md")
    text = DIGEST_RE.sub("spec_digest: sha256:" + "f" * 64, read(path), count=1)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    run_gate(run2)
    defects = verdict_of(run2)["l0"]["defects"]
    if [d["rule"] for d in defects] != ["annotation.schema"] or defects[0]["locus"] != {"tweet": None, "sentence": None}:
        pytest.fail(f"spec_digest 불일치가 annotation.schema 가 아니다: {defects}")


def test_citation_resolve_ghost_retracted_superseded() -> None:
    spec = read_json(GOLDEN_FROZEN)
    for item in spec["items"]:
        if item["id"] == "M1":
            item["status"] = "retracted"
        if item["id"] == "M2":
            item["status"] = "superseded"
            item["superseded_by"] = "M3"
    body = golden_body().replace("[M9]", "[M99]", 1)
    res = rule("citation.resolve").run(context_for(frontmatter(run_id=GOLDEN_RUN_ID, variant=VARIANT, digest="sha256:" + "0" * 64) + body, spec=spec))
    observed = sorted(d["observed"] for d in res.defects)
    if observed != ["M1 (retracted)", "M99 (absent)"]:
        pytest.fail(f"citation.resolve 결함이 다르다: {observed}")
    if len(res.flags) != 2 or any(f["origin"] != "advisory-rule" for f in res.flags):
        pytest.fail(f"superseded 인용 2건이 flag 여야 한다: {res.flags}")


# ---------------------------------------------------------------------------
# ⑪ numeric.exhaustive · ⑫ numeric.unreviewed-use
# ---------------------------------------------------------------------------


def numeric_spec(extra_facts: list[dict]) -> dict:
    spec = read_json(GOLDEN_FROZEN)
    for i, fact in enumerate(extra_facts, start=900):
        spec["items"].append({"id": f"M{i}", "kind": "fact", "status": "active", "origin": "quoted", **fact})
    return spec


def test_numeric_exhaustive_defects_and_answers(tmp_path) -> None:
    spec = numeric_spec([{"value_normalized": "0.8", "unit": "mm"}, {"value_normalized": "10", "unit": "mm"},
                         {"value_normalized": "20", "unit": "mm"}])
    body = golden_body().replace(
        "The drawing puts that sleeve on the outer face, where a hand can reach it without opening the enclosure at all.[M9]",
        "The drawing puts that sleeve on the outer face, where a hand can reach it without opening the enclosure at all, 12 mm out.[M9]", 1)
    body = body.replace("It buys back the maintenance stop by admitting up front that one soft part is there to be replaced.[M8]",
                        "It buys back the 0.80 mm gap, 10-20 mm apart, on 2024-05-02 under XX0000000A1 as of May 2, 2024.[M8]", 1)
    run_root = make_run(os.path.join(str(tmp_path), "n"), spec=spec, body=body)
    run_gate(run_root)
    verdict = verdict_of(run_root)
    defects = verdict["l0"]["defects"]
    if [(d["rule"], d["locus"]) for d in defects] != [("numeric.exhaustive", {"tweet": 4, "sentence": 2})]:
        pytest.fail(f"12 mm 만 결함이어야 한다(재료 fact·특허번호·날짜·범위 끝값은 통과): {defects}")
    if defects[0]["observed"] != "12|mm" or gate_stage.no_rewrite_violations(defects[0]["fix_directive"]):
        pytest.fail(f"결함 레코드가 다르다: {defects[0]}")
    row = rows_by_id(verdict)["numeric.exhaustive"]
    if row["checked"] != 6 or row["violations"] != 1:          # 12 mm · 0.80 mm · 10-20 mm · 2024-05-02 · XX0000000A1 · May 2, 2024
        pytest.fail(f"토큰 수·위반 수가 다르다: {row}")


def test_numeric_tokenizer_rank_and_whitelist_gap(tmp_path) -> None:
    numeric = l0_doc()["numeric"]
    tokenizers = rules_numeric.load_tokenizers(numeric)
    tokens = rules_numeric.tokenize("See US 2026/0147854 A1 and 3/6 done.", tokenizers)
    kinds = [(kind, raw) for _s, _e, kind, raw in tokens]
    # 재정 2026-09-13 T65 자잘(계수 정정) — rank 0 thread-marker 가 `3/6` 을 한 토큰으로 잡는다(구 판은 bare-number 둘 · 총괄 재량 ⓖ 공백).
    if kinds != [("patent-number-slash", "US 2026/0147854 A1"), ("thread-marker", "3/6")]:
        pytest.fail(f"토큰화 순위·소비가 다르다: {kinds}")
    # `^\d{1,2}/\d{1,2}$` 는 여전히 MATCH_KEY(`3/6|` · 단위 자리 `|`)에 fullmatch 하지 않아 defect 1 이다 — 패턴은 `|` 까지 덮어야 한다.
    body = golden_body().replace("So the invention is smaller than the problem it answers, and more candid about itself than most.[narrative]",
                                 "Thread 3/6 so far.[narrative]", 1)
    run_root = make_run(os.path.join(str(tmp_path), "w1"), body=body,
                        whitelist=[{"pattern": r"^\d{1,2}/\d{1,2}$", "rationale": "n/N", "added_by": "run-discretion", "approved_in": None}])
    run_gate(run_root)
    defects = verdict_of(run_root)["l0"]["defects"]
    if sorted(d["observed"] for d in defects) != ["3/6|"]:
        pytest.fail(f"순번 3/6 은 한 키 `3/6|` 로 결함이어야 한다(T65 자잘): {defects}")
    run_root = make_run(os.path.join(str(tmp_path), "w2"), body=body,
                        whitelist=[{"pattern": r"^\d{1,2}/\d{1,2}\|$", "rationale": "MATCH_KEY 전체에 fullmatch 되는 형태", "added_by": "run-discretion", "approved_in": None}])
    run_gate(run_root)
    if verdict_of(run_root)["l0"]["defects"]:
        pytest.fail("MATCH_KEY 에 fullmatch 하는 화이트리스트는 통과해야 한다")


# ---------------------------------------------------------------------------
# ⑬ ~ ⑯ strip · round-trip
# ---------------------------------------------------------------------------


def test_strip_forward_matches_reference_and_shares_no_code() -> None:
    text = read(GOLDEN_THREAD)
    stripped = strip_mod.strip(text)
    if stripped.stripped_md != strip_mod._reference_strip(text):
        pytest.fail("순방향 바이트 불일치")
    if strip_mod.RESIDUAL_TAG_RE.search(stripped.stripped_md):
        pytest.fail("출하본에 태그 잔존")
    source = read(strip_mod.__file__)
    main_src = source[source.index("def strip("):source.index("def _reference_strip(")]
    ref_src = source[source.index("def _reference_strip("):source.index("__all__")]
    calls_main = re.search(r"(?<![\w.])strip\(", ref_src.replace("_reference_strip(", ""))   # `.strip("\n")` 은 str 메서드다
    if "_reference_strip" in main_src or calls_main or "STRIP_TAG_RE" in ref_src or "HEADER_RE" in ref_src:
        pytest.fail("주 구현과 참조 구현이 코드를 공유한다")


def test_reverse_roundtrip_bytes_identical_including_escapes() -> None:
    text = read(GOLDEN_THREAD)
    escaped = text.replace("This filing claims a way to make the grit stay outside.[M7]",
                           "This filing \\[claims\\] a way to make the grit stay outside.[M7]", 1)
    for sample in (text, escaped):
        parsed = parse_mod.parse(sample)
        stripped = strip_mod.strip(sample)
        index = index_mod.build_index(parsed, stripped, run_id=GOLDEN_RUN_ID, variant=VARIANT, spec_version=1)
        thread = index_mod.build_thread(stripped, run_id=GOLDEN_RUN_ID, variant=VARIANT, spec_version=1,
                                        spec_digest="sha256:" + "0" * 64, weighted=len)
        if reassemble_mod.reassemble(thread, index) != sample:
            pytest.fail("역방향 재조립이 원본과 다르다")
        raw_expected = sample.split("---\n", 2)[1]
        if thread["frontmatter_raw"] != raw_expected:
            pytest.fail(f"frontmatter_raw 가 원문 바이트가 아니다: {thread['frontmatter_raw']!r}")
    stripped = strip_mod.strip(escaped)
    if "[claims\\]" not in stripped.stripped_md or "\\[" in stripped.stripped_md:   # `\[` 만 이스케이프다(§3.2)
        pytest.fail("이스케이프 복원(④)이 되지 않았다")


def test_reassembly_and_index_schemas(run_root) -> None:
    run_gate(run_root)
    gate_dir = os.path.join(run_root, "50-gate", VARIANT)
    thread = read_json(os.path.join(gate_dir, "thread.json"))
    index = read_json(os.path.join(gate_dir, "annotation-index.json"))
    stripped_md = read(os.path.join(gate_dir, "thread.stripped.md"))
    if "\n\n".join(t["text"] for t in thread["tweets"]) + "\n" != stripped_md:
        pytest.fail("재조립 바이트 불일치")
    for name, obj in (("thread", thread), ("annotation-index", index)):
        if schema_errors(name, obj):
            pytest.fail(f"{name} 스키마 위반: {schema_errors(name, obj)}")
    parsed = parse_mod.parse(read(os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")))
    if sum(len(t["sentences"]) for t in index["tweets"]) != parsed.sentence_count or len(index["narrative_sentences"]) != 4:
        pytest.fail("문장 전건 인덱스가 아니다")
    if index["by_material"]["M7"] != [{"tweet": 1, "sentence": 2}, {"tweet": 3, "sentence": 2}]:
        pytest.fail(f"by_material 역인덱스가 다르다: {index['by_material']}")
    annotation = index_mod.annotation_dict(parsed)
    if schema_errors("annotation", annotation):
        pytest.fail(schema_errors("annotation", annotation))


def test_tag_space_is_parser_violation_and_residual_check_bites() -> None:
    text = read(GOLDEN_THREAD).replace(".[M7]", ". [M7]", 1)
    parsed = parse_mod.parse(text)
    if not parsed.errors or parsed.errors[0].rule != "annotation.schema":
        pytest.fail("태그 앞 공백이 파서 위반이 아니다")
    good = read(GOLDEN_THREAD)
    parsed = parse_mod.parse(good)
    stripped = strip_mod.strip(good)
    stripped.tweets[0].sentences[0] = stripped.tweets[0].sentences[0] + " [M1]"      # 잔존 태그를 심는다
    index = index_mod.build_index(parsed, stripped, run_id=GOLDEN_RUN_ID, variant=VARIANT, spec_version=1)
    thread = index_mod.build_thread(stripped, run_id=GOLDEN_RUN_ID, variant=VARIANT, spec_version=1, spec_digest="sha256:" + "0" * 64, weighted=len)
    rows = {row.check_id: row for row in gate_stage._strip_rows(good, stripped, thread, index, parsed)}
    if rows["strip.residual-tag"].status != "fail" or rows["strip.reassembly"].status != "fail" \
            or rows["strip.roundtrip-forward"].status != "pass":
        pytest.fail("잔존 태그를 안전망·재조립이 잡지 못했다(순방향은 strip 시점 산출이라 통과가 맞다)")


# ---------------------------------------------------------------------------
# ⑰ verdict.json · ⑱ 재진입 · ⑲ 종료선·skip · ⑳ 구동기
# ---------------------------------------------------------------------------


def test_verdict_schema_rows_legislated_and_inactive_layers(run_root, tmp_path) -> None:
    run_gate(run_root)
    verdict = verdict_of(run_root)
    if schema_errors("gate-report", verdict):
        pytest.fail(schema_errors("gate-report", verdict))
    row_validator = validator("verdict-check-row")
    for row in verdict["checks"]:
        errors = [e.message for e in row_validator.iter_errors(row)]
        if errors:
            pytest.fail(f"{row['check_id']}: {errors}")
    if verdict["vacuous_pass"] != [row["check_id"] for row in verdict["checks"] if row["vacuous"] != "none"]:
        pytest.fail("vacuous_pass 파생 불일치")
    layers = [entry["layer"] for entry in verdict["inactive_layers"]]
    if len(layers) != 5 or set(layers) != {"l1", "l2", "speech_act_flag", "final_eyes", "format.stop-shape"}:
        pytest.fail(f"inactive_layers 5 가 아니다: {layers}")
    ids = [row["check_id"] for row in verdict["checks"]]
    if any(cid.startswith(("gate.l1", "gate.final-eyes", "gate.no-score")) for cid in ids) or ids[0] != "gate.input-digest":
        pytest.fail(f"미가동 층의 행이 있다거나 진입 행이 없다: {ids}")
    expected = {"defect_catalog_version": "0", "defect_catalog_entries": 0, "speech_act_predicate_version": "1.0",
                "speech_act_predicates": 3, "score_lint_version": "1.0", "score_lint_patterns": 4}
    if verdict["legislated"] != expected:
        pytest.fail(f"legislated 가 파일과 다르다: {verdict['legislated']}")
    if verdict["decision"] != "advance" or verdict["l1"]["pass"] is not None or verdict["l1"]["k"] != 3:
        pytest.fail(f"판정 필드가 다르다: {verdict['decision']} {verdict['l1']}")
    l0_json = read_json(os.path.join(run_root, "50-gate", VARIANT, "l0.json"))
    if l0_json != verdict["l0"] or "schema" in l0_json:
        pytest.fail("l0.json 은 verdict.json#l0 과 같은 객체(schema 키 없음)여야 한다")
    # 결함 판 → revise · fix_directive 가 gate.no-rewrite 통과
    body = golden_body().replace("[M9]", "[M99]", 1)
    defective = make_run(os.path.join(str(tmp_path), "d"), body=body)
    run_gate(defective)
    verdict2 = verdict_of(defective)
    if verdict2["decision"] != "revise" or verdict2["revision_round"] != 0 or rows_by_id(verdict2)["gate.no-rewrite"]["status"] != "pass":
        pytest.fail(f"결함 판 판정이 다르다: {verdict2['decision']} {rows_by_id(verdict2)['gate.no-rewrite']}")
    if schema_errors("gate-report", verdict2):
        pytest.fail(schema_errors("gate-report", verdict2))
    if not gate_stage.no_rewrite_violations('T4/S2 를 "The channel is 0.08 mm wide."로 바꿔라.'):
        pytest.fail("no-rewrite 린트가 따옴표 속 EN 문장을 잡지 못한다")


def test_reentry_is_idempotent_and_follows_thread_digest(run_root) -> None:
    run_gate(run_root)
    gate_dir = os.path.join(run_root, "50-gate", VARIANT)
    before = {name: open(os.path.join(gate_dir, name), "rb").read() for name in os.listdir(gate_dir)}
    outcome = run_gate(run_root)
    after = {name: open(os.path.join(gate_dir, name), "rb").read() for name in os.listdir(gate_dir)}
    if before != after or not outcome["variants"][VARIANT].get("reentered"):
        pytest.fail("같은 주석본 재진입에서 산출이 바뀌었거나 재계산했다")
    path = os.path.join(run_root, "40-compose", VARIANT, "thread.annotated.md")
    text = read(path).replace("[M9]", "[M99]", 1)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    outcome = run_gate(run_root)
    verdict = verdict_of(run_root)
    if outcome["variants"][VARIANT].get("reentered") or verdict["thread_digest"] != sha256_bytes(text.encode("utf-8")) \
            or verdict["decision"] != "revise":
        pytest.fail("주석본 변경 뒤 thread_digest·판정이 갱신되지 않았다")


def test_terminus_halt_and_material_defect_skip(tmp_path) -> None:
    early = make_run(os.path.join(str(tmp_path), "t"), partial_until="compose")
    with pytest.raises(StageHaltError):
        run_gate(early)
    mixed = make_run(os.path.join(str(tmp_path), "m"), variants=("v1",), defect_only=("v2",))
    outcome = run_gate(mixed)
    if outcome["variants"]["v2"] != {"skipped": "material-defect"} or outcome["variants"]["v1"]["l0_pass"] is not True:
        pytest.fail(f"반려서 변주 skip 이 아니다: {outcome['variants']}")
    if "v2" in outcome["reason_label"] and "material-defect" not in outcome["reason_label"]:
        pytest.fail(outcome["reason_label"])
    with pytest.raises(StageError):
        run_gate(mixed, variants=["v9"])


def test_driver_gate_l0_strip_and_seal(tmp_path) -> None:
    law = make_law(os.path.join(str(tmp_path), "law"))
    run_root = make_run(os.path.join(str(tmp_path), "r"), variants=("v1",))
    evidence = os.path.join(str(tmp_path), "evidence")
    lines: list[str] = []
    head = ["--repo", law, "--run-root", run_root, "--evidence-dir", evidence]
    if len(drv.COMMANDS) != 26 or drv.COMMANDS[13:15] != ("gate-l0", "strip"):
        pytest.fail(f"명령 26 가 아니다: {drv.COMMANDS}")
    code = drv.main([*head, "strip", GOLDEN_RUN_ID], out=lines.append)
    if code != 0 or not os.path.isfile(os.path.join(run_root, "50-gate", "v1", "thread.stripped.md")) \
            or os.path.isfile(os.path.join(run_root, "50-gate", "v1", "verdict.json")):
        pytest.fail(f"strip 명령: {code} {lines}")
    code = drv.main([*head, "gate-l0", GOLDEN_RUN_ID, "--variant", "v1"], out=lines.append)
    if code != 0 or not any(line.startswith("v1: l0 pass · defects 0 · advance") for line in lines):
        pytest.fail(f"gate-l0 명령: {code} {lines}")
    code = drv.main([*head, "seal", GOLDEN_RUN_ID], out=lines.append)
    manifest = read(os.path.join(evidence, "MANIFEST-sha256.txt"))
    if code != 0 or not any(line.endswith("50-gate/v1/verdict.json") for line in manifest.splitlines()):
        pytest.fail(f"seal 에 50-gate/v1/verdict.json 이 없다: {manifest}")
    paths = RunPaths(run_root, law)
    if paths.STAGES[-4:-2] != ("gate", "probe") or not paths.verdict_json("v1").endswith("50-gate/v1/verdict.json"):   # T69 ⑥ probe
        pytest.fail("RunPaths 가 gate 경로를 계약에서 해소하지 못한다")
    # 종료선 앞이면 13
    early = make_run(os.path.join(str(tmp_path), "e"), partial_until="compose")
    code = drv.main(["--repo", law, "--run-root", early, "--evidence-dir", evidence, "gate-l0", GOLDEN_RUN_ID], out=lines.append)
    if code != 13:
        pytest.fail(f"종료선 앞 gate-l0 는 13 이어야 한다: {code}")
