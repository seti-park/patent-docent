"""소견 1회와 재시도 1회. 자문 레인 장애는 결번으로 기록한다."""
import json
import os
import shutil

from jsonschema import Draft202012Validator
from reader.lib.report import CheckRow
from ..critique.plan import build_request
from ..pens import registry
from ..gate.l2.lint import hits, load_patterns
from ..lanes.contract import LanePending, LaneContractError, render_request_md
from ..lanes.file_adapter import FileLaneAdapter
from ..paths import RunPaths, repo_root
from . import (StageError, StageHaltError, load_json, load_yaml, write_json, write_text,
               sha256_bytes, sha256_file, rows_to_dicts, verify_declared_inputs, failure_entry, findings_of)
from .design import adjudicated_anchors, check_anchors_adjudicated_only, latest_frozen, terminus_index
from .gate import no_rewrite_violations


def mentions_id(text, target):
    start = text.find(target)
    while start >= 0:
        end = start + len(target)
        if (start == 0 or not text[start - 1].isalnum()) and (end == len(text) or not text[end].isascii() or not text[end].isalnum()):
            return True
        start = text.find(target, start + 1)
    return False


def _supersede_stale_lanes(root: str, previous_digest: str | None) -> bool:
    """요청서가 갱신되면 옛 좌표에 남은 응답은 **새 요청의 답이 될 수 없다**(레인 결속).

    좌표를 비우되 지우지 않고 직전 입력 지문 아래 보존한다 — 구동기가 영수증에 하는 처리와 같은 원리다.
    이것이 없으면 절차 문서 한 줄을 고친 뒤 재실행할 때 러너가 매 회차 옛 응답을 만나 「낡음」으로 실패하고,
    재시도 한도를 소진한 채 결번으로 끝난다(런 -3 02:11 실측).
    """
    source = os.path.join(root, "lanes", "critique")
    if not os.path.isdir(source):
        return False
    tag = (previous_digest or "unknown").replace("sha256:", "")[:16]
    keep = os.path.join(root, "superseded-lanes", tag)
    if os.path.exists(keep):
        return False
    os.makedirs(os.path.dirname(keep), exist_ok=True)
    shutil.move(source, keep)
    return True


def run(run_root, repo=None, variant=None, adapter=None, dead=None):
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts["critique"]
    if variant not in registry.variant_ids(contract=paths.contracts["compose"]):
        raise StageError("소견 변주가 계약 열거 밖이다")
    meta = load_yaml(paths.run_yaml)
    if meta.get("run_kind") == "partial" and terminus_index(repo, str(meta.get("partial_until"))) < terminus_index(repo, "critique"):
        raise StageHaltError("partial_until이 critique 앞이다 — 종료선 연장이 필요하다")
    version = int(latest_frozen(meta)["spec_version"])
    entry = verify_declared_inputs(paths, contract, "critique", inputs={"variant": variant, "spec_version": version})
    verdict = load_json(paths.verdict_json(variant))
    if verdict.get("decision") != "advance":
        raise StageError("소견은 decision advance 뒤에만 실행한다")
    root = paths.critique_dir(variant)
    os.makedirs(root, exist_ok=True)
    report_path = os.path.join(root, "critique-report.json")
    missing_path = os.path.join(root, "memo-missing.json")
    anchors, excluded = adjudicated_anchors(repo)
    provided = os.path.join(root, "anchors-provided.json")
    write_json(provided, {"provided": anchors, "excluded": excluded})
    score = load_json(paths.score_json(variant))
    law = load_patterns(repo)
    if "65-critique/<variant>/memo.md" not in law["targets"]:
        raise StageError("score-lint의 소견 대상 선언이 없다")
    targets = score.get("per_target") or []
    if not targets:
        raise StageError("score.json#per_target 가 비어 있다")
    measured = [t for t in targets if t.get("hit_rate") is not None]
    if not measured:
        raise StageError("계기 유효 관측 0건 — 최약 표적을 결정할 수 없다")
    minimum = min(t["hit_rate"] for t in measured)
    weakest = [t["material_id"] for t in measured if t["hit_rate"] == minimum]
    adapter = adapter or FileLaneAdapter(os.path.join(root, "lanes"), repo)
    cap_text = failure_entry(contract, "레인 실패")["action"]
    cap = int(cap_text.partition("(")[2].rstrip(")"))
    fingerprint = sha256_bytes(json.dumps([build_request(paths=paths, repo=repo, variant=variant, version=version,
        anchors=anchors).input_digest, verdict.get("advisory_measurements")], sort_keys=True).encode())
    old = load_json(report_path) if os.path.isfile(report_path) else {}
    if old.get("input_digest") == fingerprint and old.get("status") in ("ok", "missing"):
        if old["status"] == "missing" and os.path.isfile(missing_path):
            # 결번이 확정이려면 그 좌표가 비어 있어야 한다. 응답이 남은 채 난 결번은 **그 응답 때문에** 난 것이며
            # (요청 갱신 뒤의 낡은 응답 · 런 -3 02:11), 원인을 고친 뒤에는 다시 물어야 한다.
            if not os.path.isdir(os.path.join(root, "lanes", "critique")):
                return {"status": "missing", "reentered": True}
            _supersede_stale_lanes(root, old.get("input_digest"))
        if os.path.isfile(paths.critique_memo(variant)):
            if sha256_file(paths.critique_memo(variant)) == old.get("memo_digest"):
                return {"status": "reentered"}
            raise StageHaltError("소견 파일이 검사 후 바뀌었다")
    if old.get("input_digest") not in (None, fingerprint):
        _supersede_stale_lanes(root, old.get("input_digest"))
    attempt = int(old.get("attempt", 0)) if old.get("input_digest") == fingerprint else 0
    for artifact in (paths.critique_memo(variant), missing_path):
        if os.path.isfile(artifact):
            os.remove(artifact)
    for attempt in range(attempt, cap + 1):
        request = build_request(paths=paths, repo=repo, variant=variant, version=version, anchors=anchors, attempt=attempt)
        try:
            if request.lane_id in (dead or []):
                raise LaneContractError("구동기 신고: 레인 호출 실패")
            response = adapter.dispatch([request])[0]
            errors = list(Draft202012Validator(request.response_schema).iter_errors(response.payload))
            if errors or response.mismatches(request) or response.input_digest != request.input_digest or response.lane_id != request.lane_id:
                raise LaneContractError("소견 응답 서식 또는 좌석 불일치")
            memo = response.payload["memo_md"]
        except LanePending as pending:
            write_json(report_path, {"status": "pending", "attempt": attempt, "candidate_digest": sha256_file(paths.thread_stripped_md(variant)), "input_digest": fingerprint})
            return {"status": "pending", "pending": list(pending.pending), "lanes_root": pending.request_dir}
        except (LaneContractError, OSError, ValueError) as exc:
            if attempt < cap:
                continue
            if os.path.isfile(paths.critique_memo(variant)):
                os.remove(paths.critique_memo(variant))
            missing = {"reason": str(exc), "attempts": attempt + 1, "candidate_digest": sha256_file(paths.thread_stripped_md(variant)), "input_digest": fingerprint}
            write_json(missing_path, missing)
            write_json(report_path, {**missing, "status": "missing", "rows": rows_to_dicts([entry])})
            return {"status": "missing"}
        measurements = verdict.get("advisory_measurements") or {}
        if measurements.get("extreme"):
            memo = f"**총 단어수 극단치: {measurements['total_words']} words**\n" + memo
        rows = [entry]
        for suffix, valid in (
            ("no-score", not hits(memo, law)),
            ("probe-reflected", any(mentions_id(memo, t) for t in weakest)),
            ("no-history", all(t not in render_request_md(request, repo) for t in ("revisions/", "metrics.jsonl"))),
            ("extreme-flagged", not measurements.get("extreme") or str(measurements["total_words"]) in memo.splitlines()[0])):
            row = CheckRow(check_id="critique." + suffix, checked=1)
            if suffix == "no-score":
                row.ruleset, row.ruleset_version, row.ruleset_size = "score-lint", law["version"], len(law["patterns"])
            if not valid:
                row.add(row.check_id, "memo.md", memo[:120], suffix, "소견 계약 위반")
            rows.append(row)
        anchor_row = check_anchors_adjudicated_only(provided)
        anchor_row.check_id = "critique.anchors-adjudicated-only"
        rows.append(anchor_row)
        failed = [r.check_id for r in rows if r.status == "fail"]
        if no_rewrite_violations(memo):
            failed.append("대체 문장 금지")
        write_json(report_path, {"status": "retry" if failed else "ok", "attempt": attempt,
            "candidate_digest": sha256_file(paths.thread_stripped_md(variant)), "input_digest": fingerprint, "rows": rows_to_dicts(rows), "findings": findings_of(rows), "failed_checks": failed,
            "memo_digest": sha256_bytes(memo.encode()), "lane": {"model": response.model, "effort": response.effort}})
        if failed:
            if attempt < cap:
                continue
            raise StageHaltError("소견 재시도 소진: " + ", ".join(failed))
        write_text(paths.critique_memo(variant), memo)
        if os.path.isfile(missing_path):
            os.remove(missing_path)
        return {"status": "ok", "rows": rows_to_dicts(rows)}
