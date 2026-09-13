"""T69 ⑦: 고정 post-l1 사본 · 격리 · CP2 · 출하. 생산 원장은 쓰기 전에 차단한다."""
import builtins
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import shutil

import pytest
import yaml
from jsonschema import Draft202012Validator

from engine.paths import RunPaths, load_stage_contract
from engine.lanes.contract import LaneResponse, LaneContractError, render_request_md
from engine.stages import (StageHaltError, StageError, StageEnvironmentError, load_json, load_yaml,
                           write_json, write_text, sha256_file, dump_yaml)
from engine.stages import critique, ship, gate
from engine.gate import final_eyes, checkpoint2
from engine.gate.l2.lint import load_patterns
from tools import drive_partial_read as drv
from test_m36_t69_probe import make_run, REPO, RUN_ID, VARIANT
from ledger_guard import production_ledger_untouched, production_ledger


def require(value, message="검증 실패"):
    if not value:
        pytest.fail(message)


@pytest.fixture
def setup(tmp_path, monkeypatch):
    law = tmp_path / "law"
    law.mkdir()
    for tree in ("contracts", "reader", "engine", "docs"):
        shutil.copytree(Path(REPO) / tree, law / tree, ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr("engine.stages.compose.law_commit_of", lambda repo: "e" * 40)
    root = make_run(str(tmp_path / "r"))
    paths = RunPaths(root, str(law))
    # 복사 시각은 원 생성 시각이 아니다. 이 합성 시험은 동결 시각을 명시해 N1을 시험한다.
    brief = load_json(paths.final_eyes_brief(VARIANT))
    boundary = datetime.fromisoformat(brief["generated_at"].replace("Z", "+00:00")).timestamp()
    for p in (paths.final_eyes_brief(VARIANT), paths.frozen_spec(1)):
        os.utime(p, (boundary, boundary))
    targets = load_json(paths.blueprint_json)["transmission_targets"]
    write_json(paths.score_json(VARIANT), {"input_digest": sha256_file(paths.thread_stripped_md(VARIANT)),
        "delivery_fidelity": 0.5, "per_target": [{"material_id": t, "hit_rate": i / len(targets), "weakest_tweet": 1} for i, t in enumerate(targets)],
        "restatement": {"aligned": 3}})
    write_text(paths.l2_md(VARIANT), "# L2 자문\n구조의 흐름을 확인했다.\n")
    # 옛 픽스처의 비가동 표시는 해당 층 산출 합성과 함께만 제거한다.
    v = load_json(paths.verdict_json(VARIANT))
    v["inactive_layers"] = []
    write_json(paths.verdict_json(VARIANT), v)
    production_roots = [Path(REPO) / "ledgers", Path(production_ledger()).parents[1]]
    before = {str(p): p.read_bytes() for r in production_roots for p in r.rglob("*") if p.is_file()}
    original = builtins.open
    def guarded(file, mode="r", *args, **kwargs):
        if isinstance(file, (str, os.PathLike)) and any(c in mode for c in "wax+"):
            resolved = Path(file).resolve()
            if any(resolved.is_relative_to(r.resolve()) for r in production_roots):
                pytest.fail("생산 원장 쓰기 시도: " + str(file))
        return original(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", guarded)
    with production_ledger_untouched(tmp_path, str(law)):
        yield paths, str(law)
    require(before == {str(p): p.read_bytes() for r in production_roots for p in r.rglob("*") if p.is_file()}, "생산 원장 바이트 변경")


def good_memo(paths):
    t = load_json(paths.score_json(VARIANT))["per_target"][0]
    return f"훅 조응: {t['material_id']} hit_rate={t['hit_rate']}가 최약 표적이다.\n안도감 착지: 재료로 돌아온다.\n도슨트 보이스: 관찰을 안내한다.\n"


def final_payload(paths, defects=None):
    parsed = gate.parse_annotation(Path(paths.thread_annotated(VARIANT)).read_text())
    return {"l1_recheck": {"defects": defects or [], "narrative_audit": [
        {"locus": {"tweet": t.n, "sentence": s.i}, "observation": "기술 주장 밀수 없음"}
        for t in parsed.tweets for s in t.sentences if s.narrative]}, "observations": ["착지의 여운을 Owner가 판단한다."]}


class Adapter:
    def __init__(self, payload, model=None):
        self.payload, self.model, self.requests = payload, model, []
    def dispatch(self, requests):
        responses = []
        for request in requests:
            self.requests.append(request)
            payload = self.payload(request) if callable(self.payload) else self.payload
            if isinstance(payload, Exception):
                raise payload
            responses.append(LaneResponse(request.lane_id, self.model or request.model, request.effort,
                payload, request.input_digest, "sha256:" + "a" * 64))
        return responses


def final_done(paths, law):
    result = final_eyes.run(paths.run_root, law, VARIANT, Adapter(final_payload(paths)))
    require(result["final_eyes"]["verdict"] == "pass", str(result))
    return result


def approve(paths, law, flags=True):
    verdict = load_json(paths.verdict_json(VARIANT))
    envelope, warnings = checkpoint2.build_envelope(run_root=paths.run_root, repo=law, variant=VARIANT,
        decision="approved", owner_quote="v2 출하 승인", located_at="시험 육성",
        flags_adjudicated=[{"flag_id": f["id"], "verdict": "accept"} for f in checkpoint2.flags_of(verdict)] if flags else [])
    checkpoint2.write_envelope(run_root=paths.run_root, repo=law, envelope=envelope, title="시험 CP2")
    return envelope


def ready(paths, law):
    critique.run(paths.run_root, law, VARIANT, Adapter({"memo_md": good_memo(paths)}))
    final_done(paths, law)
    approve(paths, law)


def test_contracts_paths(setup):
    paths, law = setup
    for stage in ("critique", "ship"):
        require(load_stage_contract(stage, law)["schema"] == "stage-contract/v0")
    require("checkpoint2" not in paths.contracts["gate"])
    require(paths.checkpoint2_md.endswith(paths.contracts["critique"]["owner_checkpoint"]["confirm_file"]))
    require(len(paths.contracts["critique"]["checks_before_exit"]) == 5)
    require(len(paths.contracts["ship"]["checks_before_exit"]) == 6)
    require(paths.thread_json(VARIANT) != paths.ship_thread_json)


def test_critique_request_and_memo(setup):
    paths, law = setup
    adapter = Adapter({"memo_md": good_memo(paths)})
    result = critique.run(paths.run_root, law, VARIANT, adapter)
    require(result["status"] == "ok")
    request = adapter.requests[0]
    rendered = render_request_md(request, law)
    for needle in ("score.json", "blueprint.json", "material-spec.v1.json"):
        require(needle in rendered)
    require("revisions/" not in rendered and "metrics.jsonl" not in rendered)
    require(Path(paths.critique_memo(VARIANT)).exists())
    row = next(r for r in result["rows"] if r["check_id"].endswith("anchors-adjudicated-only"))
    require(row["vacuous"] == "empty-target")
    require(critique.run(paths.run_root, law, VARIANT, adapter)["status"] == "reentered")


@pytest.mark.parametrize("bad,needle", [("관측 없는 메모", "probe-reflected"), ("quality: 8/10", "no-score")])
def test_critique_retry_bad_memo(setup, bad, needle):
    paths, law = setup
    adapter = Adapter({"memo_md": bad})
    with pytest.raises(StageHaltError, match=needle):
        critique.run(paths.run_root, law, VARIANT, adapter)
    require(len(adapter.requests) == 2)


def test_critique_extreme(setup):
    paths, law = setup
    verdict = load_json(paths.verdict_json(VARIANT))
    verdict["advisory_measurements"].update(extreme=True, total_words=9876)
    write_json(paths.verdict_json(VARIANT), verdict)
    critique.run(paths.run_root, law, VARIANT, Adapter({"memo_md": good_memo(paths)}))
    require("9876" in Path(paths.critique_memo(VARIANT)).read_text().splitlines()[0])


def test_critique_failed_lane_missing_cp2(setup):
    paths, law = setup
    adapter = Adapter(lambda r: LaneContractError("quota"))
    require(critique.run(paths.run_root, law, VARIANT, adapter)["status"] == "missing")
    require(len(adapter.requests) == 2 and not Path(paths.critique_memo(VARIANT)).exists())
    final_done(paths, law)
    require("결번" in checkpoint2.surfaces(run_root=paths.run_root, repo=law, variant=VARIANT)["present"]["memo"])


def test_critique_requires_probe(setup):
    paths, law = setup
    Path(paths.score_json(VARIANT)).unlink()
    with pytest.raises(StageEnvironmentError):
        critique.run(paths.run_root, law, VARIANT)


def test_final_four_inputs_and_fingerprints(setup):
    paths, law = setup
    adapter = Adapter(final_payload(paths))
    outcome = final_eyes.run(paths.run_root, law, VARIANT, adapter)
    require(outcome["final_eyes"]["verdict"] == "pass", str(outcome))
    require(len(adapter.requests) == gate.l1_k(law))
    require(len({r.input_digest for r in adapter.requests}) == gate.l1_k(law))
    for request in adapter.requests:
        require(len(request.slices) == 4)
        require(not any(p.startswith("contracts/") for p in request.slices))
        require("revisions/" not in render_request_md(request, law))
        require(request.effort == "max")
    require({r["path"] for r in outcome["final_eyes"]["inputs_read"]} == set(adapter.requests[0].slices))
    schema = load_json(str(Path(law) / "contracts/schemas/gate-report.schema.json"))
    require(not list(Draft202012Validator(schema).iter_errors(load_json(paths.verdict_json(VARIANT)))))


@pytest.mark.parametrize("mutation", ["extra", "late", "pin", "open"])
def test_final_isolation_failures(setup, mutation):
    paths, law = setup
    if mutation == "extra":
        final_done(paths, law)
        v = load_json(paths.verdict_json(VARIANT))
        v["final_eyes"]["inputs_read"].append({"path": "extra", "digest": "sha256:" + "b" * 64})
        write_json(paths.verdict_json(VARIANT), v)
    elif mutation == "late":
        os.utime(paths.frozen_spec(1), None)
    elif mutation == "pin":
        with open(paths.final_eyes_brief(VARIANT), "a") as handle:
            handle.write(" ")
    else:
        write_json(os.path.join(paths.free_revision_dir(VARIANT), "round.json"), {"status": "open"})
    with pytest.raises(StageHaltError):
        final_eyes.run(paths.run_root, law, VARIANT, Adapter(final_payload(paths)))


@pytest.mark.parametrize("mutation,reason", [("l0", "a"), ("strip", "c"), ("json", "c")])
def test_final_deterministic_veto(setup, mutation, reason):
    paths, law = setup
    if mutation == "l0":
        p = paths.thread_annotated(VARIANT)
        text = Path(p).read_text().replace("[narrative]", "[M99999]", 1)
        Path(p).write_text(text)
    elif mutation == "strip":
        with open(paths.thread_stripped_md(VARIANT), "a") as f:
            f.write("x")
    else:
        thread = load_json(paths.thread_json(VARIANT))
        thread["tweets"][0]["text"] += "x"
        write_json(paths.thread_json(VARIANT), thread)
    out = final_eyes.run(paths.run_root, law, VARIANT, Adapter(final_payload(paths)))
    require(out["final_eyes"]["veto_reason"] == reason, str(out))
    require(out["decision"] == "revise")


@pytest.mark.parametrize("majority", [True, False])
def test_final_votes(setup, majority):
    paths, law = setup
    k = gate.l1_k(law)
    defect = {"rule": final_eyes.l1_config(law)["veto_rules"][0], "locus": {"tweet": 1, "sentence": 1},
              "expected": "동결 재료와 정합", "observed": "인용 의미 불일치"}
    adapter = Adapter(lambda r: final_payload(paths, [defect] if r.batch < (k // 2 + 1 if majority else 1) else []))
    out = final_eyes.run(paths.run_root, law, VARIANT, adapter)
    require(out["final_eyes"]["veto_reason"] == ("b" if majority else None))
    require(bool(out["final_eyes"]["observations"]))
    if majority:
        from engine.gate.loop import revise
        require(revise(run_root=paths.run_root, repo=law, variant=VARIANT)["status"] == "pending")


def test_final_cap_escalates(setup):
    paths, law = setup
    v = load_json(paths.verdict_json(VARIANT))
    v["revision_round"] = gate.revision_cap(paths.contracts["gate"])
    write_json(paths.verdict_json(VARIANT), v)
    with open(paths.thread_stripped_md(VARIANT), "a") as f:
        f.write("x")
    require(final_eyes.run(paths.run_root, law, VARIANT)["status"] == "escalate")


def test_final_scope_and_model(setup):
    paths, law = setup
    require(final_eyes.scope_row({"verdict": "veto", "veto_reason": "d"}).status == "fail")
    with pytest.raises(StageHaltError, match="lane-verified"):
        final_eyes.run(paths.run_root, law, VARIANT, Adapter(final_payload(paths), model="fable-5.1"))


def test_cp2_all_surfaces(setup):
    paths, law = setup
    ready(paths, law)
    view = checkpoint2.surfaces(run_root=paths.run_root, repo=law, variant=VARIANT)
    require(set(view["present"]) == {"thread_stripped", "selection", "flags", "l2", "score", "memo", "verdict", "numeric_whitelist"})
    require(view["present"]["thread_stripped"]["text"] == Path(paths.thread_stripped_md(VARIANT)).read_text())
    require(view["draft"]["figure_overrides"] == [])
    Path(paths.l2_md(VARIANT)).unlink()
    with pytest.raises(StageError, match="필수 표면"):
        checkpoint2.surfaces(run_root=paths.run_root, repo=law, variant=VARIANT)


@pytest.mark.parametrize("mutation", ["absent", "digest", "flags", "publishable", "pointer"])
def test_ship_rejections(setup, mutation):
    paths, law = setup
    ready(paths, law)
    if mutation == "absent":
        Path(paths.checkpoint2_md).unlink()
    elif mutation == "digest":
        envelope = approve(paths, law)
        envelope["target"]["digest"] = "sha256:" + "0" * 64
        checkpoint2.write_envelope(run_root=paths.run_root, repo=law, envelope=envelope, title="시험 CP2")
    elif mutation == "flags":
        approve(paths, law, flags=False)
    elif mutation == "publishable":
        manifest = load_json(paths.figures_manifest_json)
        for item in manifest["items"]:
            item["publishable"] = False
        write_json(paths.figures_manifest_json, manifest)
    else:
        selection = load_json(paths.figures_selection_json)
        selection["slots"][0]["asset"] = "fig-99"
        write_json(paths.figures_selection_json, selection)
        require(ship.run(paths.run_root, law)["status"] == "retry")
    with pytest.raises((StageHaltError, StageEnvironmentError)):
        ship.run(paths.run_root, law)
    require(not (Path(law) / "ledgers/tournament.jsonl").exists())


def test_ship_bytes_images_ledgers_idempotence(setup):
    paths, law = setup
    ready(paths, law)
    out = ship.run(paths.run_root, law)
    require(out["status"] == "ok")
    require(Path(paths.ship_thread_md).read_bytes() == Path(paths.thread_stripped_md(VARIANT)).read_bytes())
    require(Path(paths.ship_thread_json).read_bytes() == Path(paths.thread_json(VARIANT)).read_bytes())
    index = load_json(os.path.join(paths.ship_images_dir, "index.json"))
    for assets in index.values():
        for asset in assets:
            require(Path(paths.ship_images_dir, asset + ".png").read_bytes() == Path(paths.figure_asset(asset)).read_bytes())
    for field in ("defense_layers", "figures_usage_rights_decision", "template_freeze", "partial", "Owner"):
        require(field in Path(paths.ship_md).read_text())
    before = {p.name: p.read_bytes() for p in Path(law, "ledgers").iterdir() if p.is_file()}
    ship.run(paths.run_root, law)
    require(before == {p.name: p.read_bytes() for p in Path(law, "ledgers").iterdir() if p.is_file()})
    require(load_yaml(paths.run_yaml)["status"] == "shipped")
    with open(paths.ship_thread_json, "a") as f:
        f.write(" ")
    with pytest.raises(StageHaltError, match="byte-identical"):
        ship.run(paths.run_root, law)


def test_driver_commands_and_seal(setup, tmp_path):
    paths, law = setup
    evidence = str(tmp_path / "evidence")
    calls = []
    def stub(argv, stdin, env, timeout):
        text = stdin.decode()
        lane = drv._lane_id_from_request_md(text)
        model = argv[argv.index("--model") + 1]
        effort = argv[argv.index("--effort") + 1]
        request = next(Path(paths.run_root).rglob("request.json"))
        requests = [load_json(str(p)) for p in Path(paths.run_root).rglob("request.json")]
        req = next(r for r in requests if r["lane_id"] == lane)
        payload = {"memo_md": good_memo(paths)} if lane.startswith("critique/") else final_payload(paths)
        calls.append((lane, effort, argv))
        envelope = {"lane_id": lane, "model": model, "effort": effort, "input_digest": req["input_digest"], "payload": payload}
        body = {"type": "result", "is_error": False, "modelUsage": {model: {"inputTokens": 1, "outputTokens": 1}},
                "session_id": lane, "structured_output": envelope}
        return drv.ExecResult(0, json.dumps(body).encode(), b"", False, 1)
    def drive(*args):
        lines = []
        rc = drv.main(["--repo", law, "--run-root", paths.run_root, "--evidence-dir", evidence, *args], executor=stub, out=lines.append)
        require(rc == 0, str((rc, lines)))
        return lines
    require(len(drv.COMMANDS) == 25)
    drive("critique", RUN_ID, "--variant", VARIANT)
    drive("final-eyes", RUN_ID, "--variant", VARIANT)
    lines = drive("cp2", RUN_ID, "--variant", VARIANT)
    require(any("material_id | hit_rate" in l for l in lines))
    approve(paths, law)
    drive("ship", RUN_ID)
    drive("seal", RUN_ID)
    manifest = Path(evidence, "MANIFEST-sha256.txt").read_text()
    require("65-critique/" in manifest and "70-ship/SHIP.md" in manifest)
    require([e for lane, e, _ in calls if lane.startswith("final-eyes/")] == ["max"] * gate.l1_k(law))
    require(all("--resume" not in argv and "--continue" not in argv for _, _, argv in calls))


def test_final_veto_revise_then_fresh_session(setup):
    paths, law = setup
    from engine.gate.loop import revise
    defect = {"rule": final_eyes.l1_config(law)["veto_rules"][0], "locus": {"tweet": 1, "sentence": 1},
              "expected": "동결 재료 정합", "observed": "재검 필요"}
    first = Adapter(final_payload(paths, [defect]))
    require(final_eyes.run(paths.run_root, law, VARIANT, first)["decision"] == "revise")
    before = Path(paths.thread_annotated(VARIANT)).read_text()
    out = revise(run_root=paths.run_root, repo=law, variant=VARIANT,
        adapter=Adapter({"thread_annotated_md": before}), l1_adapter=Adapter({"defects": [], "flags": [], "speech_acts": []}))
    require(out["decision"] == "advance", str(out))
    require(Path(paths.l2_md(VARIANT)).exists(), "국소 재진입이 L2 메모를 잃었다")
    second = Adapter(final_payload(paths))
    require(final_eyes.run(paths.run_root, law, VARIANT, second)["final_eyes"]["verdict"] == "pass")
    require({r.input_digest for r in first.requests}.isdisjoint({r.input_digest for r in second.requests}), "최종 재검이 이전 세션 지문을 공유했다")


def test_ship_gate_json_tampering(setup):
    paths, law = setup
    ready(paths, law)
    with open(paths.thread_json(VARIANT), "a") as handle:
        handle.write(" ")
    with pytest.raises(StageHaltError, match="byte-identical"):
        ship.run(paths.run_root, law)


def test_final_malformed_annotation_veto_a(setup):
    paths, law = setup
    path = Path(paths.thread_annotated(VARIANT))
    path.write_text(path.read_text().replace("---", "broken", 1))
    require(final_eyes.run(paths.run_root, law, VARIANT)["final_eyes"]["veto_reason"] == "a")


def test_critique_retry_recovers_and_exact_target(setup):
    paths, law = setup
    require(not critique.mentions_id("M100", "M1"))
    adapter = Adapter(lambda r: {"memo_md": good_memo(paths) if "/retry-" in r.lane_id else "표적 누락"})
    require(critique.run(paths.run_root, law, VARIANT, adapter)["status"] == "ok")
    require(len(adapter.requests) == 2)


def test_final_persisted_scope_d_rejected(setup):
    paths, law = setup
    final_done(paths, law)
    verdict = load_json(paths.verdict_json(VARIANT))
    verdict["final_eyes"].update(verdict="veto", veto_reason="d")
    write_json(paths.verdict_json(VARIANT), verdict)
    schema = load_json(str(Path(law) / "contracts/schemas/gate-report.schema.json"))
    require(bool(list(Draft202012Validator(schema).iter_errors(verdict))))
    with pytest.raises(StageHaltError, match="scope"):
        final_eyes.run(paths.run_root, law, VARIANT)


def test_final_crlf_is_byte_change(setup):
    paths, law = setup
    p = Path(paths.thread_stripped_md(VARIANT))
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    require(final_eyes.run(paths.run_root, law, VARIANT)["final_eyes"]["veto_reason"] == "c")


def test_driver_duplicate_sessions_fail_closed(setup, tmp_path):
    paths, law = setup
    ctx = drv.Context(run_id=RUN_ID, repo=law, worktree=law, run_root=paths.run_root,
        evidence=str(tmp_path / "receipts"), law=law, executor=lambda *args: pytest.fail("호출 금지"), dry_run=False)
    lane_ids = [f"final-eyes/{VARIANT}/batch-{i}" for i in range(gate.l1_k(law))]
    for lane_id in lane_ids:
        write_json(drv._receipt_path(ctx, lane_id), {"lane_id": lane_id, "session_id": "shared", "requested": {"model": "opus-5"}})
    with pytest.raises(drv.DriverExit, match="새 세션"):
        drv._verify_fresh_final_sessions(ctx, lane_ids)
    require(any(r["check_id"] == "gate.final-eyes-lane-verified" and r["status"] == "fail" for r in load_json(paths.verdict_json(VARIANT))["checks"]))


def test_ship_requires_resubmitted_cp2(setup):
    paths, law = setup
    ready(paths, law)
    envelope = approve(paths, law)
    envelope["decided_at"] = "2026-09-13T00:00:00Z"
    checkpoint2.write_envelope(run_root=paths.run_root, repo=law, envelope=envelope, title="옛 CP2")
    with pytest.raises(StageHaltError, match="CP2 재상신"):
        ship.run(paths.run_root, law)
