# -*- coding: utf-8 -*-
"""`probe` 스테이지 — 스레드만 읽는 계기 n 대로 전달 충실도를 잰다(재정 2026-09-13 T69 ⑥ · M7-a · SPEC §1.11 · §5 · D9).

계약 = `contracts/stages/probe.yaml`. 위상(전부 파일 상태로 재진입 안전 · 순차):

① 진입 — 종료선 · `probe.input-digest`(재정 P-C) · `verdict.json#decision == advance`(품질 전제 · `StageError`) ·
   **입력 청정** `probe.input-clean`(출하 후보 텍스트에 계약 `input_clean_patterns` 부재 · 위반 = halt · 측정 무효).
② 질문지 — 런 단위 `60-probe/questions.json`(있으면 재사용 · 재료 판 대조). 없으면 레인 `probe-q/<v>/batch-0`(동결본 전문 +
   표적 목록 · 스레드 없음) → 1:1 검증(표적 밖 폐기 · 부족 = retry(1) → escalate).
③ 프로브 n — `probe/<v>/batch-<i>`(동일 바이트 · 좌표만 다름 · 입력 = `thread.stripped.md` + 질문지) → `probe-<i>.json`(probe-report/v0).
④ 정족수(재정 P-6 · `engine/quorum.py`) — 유효 응답 == n. 죽은 인스턴스(구동기가 `dead` 로 신고)만 `retry-<k>` 좌표로 재요청 ·
   상한(`parameters.yaml#instrument_quorum.dead_instance_retry.max_attempts`) 소진 = `escalate`(`escalation.json` · Owner 선택지 3 = 계약 문언).
⑤ 무효 답변 — `quoted_span` 비부분문자열 → `invalidated_answers[]` · 분모 제외.
⑥ 채점 — 결정론 kind 3(`engine/probe/grade.py` · `reader.lib.normalize` 공용) · 모델 채점 kind 3 + 재서술 축 = 레인 `probe-grade/<v>/batch-0`
   1회 묶음(스레드 없음 · 결정론 판정 항목 제외).
⑦ 국소화 — annotation-index 역참조 · 2단 규칙 · `unrepresented`. ⑧ `score.json`(probe-score/v0 · 판정 키 없음).
⑨ 검사 5(`probe.independence` · `probe.input-clean` · `probe.no-self-report` · `probe.target-coverage` · `probe.grader-separation`) →
   `60-probe/<v>/probe-report.json`(행 8키). grader-separation 실패 = halt.

★ 계기는 거부권이 없다(§5.7). 이 러너는 `verdict.json` 에 쓰지 않고 `compose` 를 부르지 않는다.
★ n · 상한 · 좌석 · 판별식 · 정규식 · 라벨을 코드에 두지 않는다 — 계약에서 읽는다.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import shutil
import re

from jsonschema import Draft202012Validator

from reader.lib.report import CheckRow

from . import (
    StageError,
    StageHaltError,
    failure_entry,
    findings_of,
    load_json,
    load_yaml,
    read_text,
    rows_to_dicts,
    sha256_bytes,
    sha256_file,
    verify_declared_inputs,
    write_json,
    write_text,
)
from .design import latest_frozen, terminus_index
from .gate import DECISION_ADVANCE
from .. import quorum as quorum_mod
from ..lanes.contract import LanePending
from ..lanes.file_adapter import FileLaneAdapter
from ..lanes.plan import _accepted_models
from ..paths import RunPaths, repo_root
from ..probe import LANE_GRADE, LANE_PROBE, LANE_QUESTIONS, STAGE_ID, items_by_id, probe_config, targets_of
from ..probe import grade as grade_mod
from ..probe import localize as localize_mod
from ..probe import questions as questions_mod
from ..probe import run_probes as probes_mod

CHECK_ENTRY = "probe.input-digest"
CHECK_INDEPENDENCE = "probe.independence"
CHECK_INPUT_CLEAN = "probe.input-clean"
CHECK_NO_SELF_REPORT = "probe.no-self-report"
CHECK_TARGET_COVERAGE = "probe.target-coverage"
CHECK_GRADER_SEPARATION = "probe.grader-separation"
REPORT_SCHEMA_REL = ("contracts", "schemas", "probe-report.schema.json")
SCORE_SCHEMA_REL = ("contracts", "schemas", "probe-score.schema.json")
QUESTIONS_SCHEMA = "probe-questions/v0"
STATUS_OK = "ok"
STATUS_PENDING = "pending"
STATUS_ESCALATE = "escalate"
STATUS_REENTERED = "reentered"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_terminus(meta: dict, repo: str, contract: dict) -> None:
    if meta.get("run_kind") != "partial":
        return
    until = str(meta.get("partial_until", ""))
    if terminus_index(repo, until) < terminus_index(repo, STAGE_ID):
        entry = failure_entry(contract, "partial_until 종료선")
        raise StageHaltError(f"[{entry.get('action')}] partial_until={until!r} 은 probe 앞의 종료선이다 — {entry.get('note')}")


def _rel(paths: RunPaths, path: str) -> str:
    return os.path.relpath(path, paths.run_root).replace(os.sep, "/")


def _result(status: str, **extra) -> dict:
    return {"status": status, "pending": [], "lanes_root": None, "rows": [], **extra}


# ---------------------------------------------------------------------------
# 검사
# ---------------------------------------------------------------------------


def input_clean_row(text: str, patterns: list[str]) -> CheckRow:
    """`probe.input-clean` — 계약 정규식 전건이 텍스트(멀티라인)에 부재."""
    row = CheckRow(check_id=CHECK_INPUT_CLEAN, ruleset="input_clean_patterns", ruleset_version="probe.yaml", ruleset_size=len(patterns),
                   checked=len(text.split("\n")))
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.MULTILINE):
            line = text.count("\n", 0, match.start()) + 1
            row.add(CHECK_INPUT_CLEAN, f"line {line}", match.group(0), "(없음)", "계기 입력에 주석 태그·헤더·프런트매터가 남아 있다 — 측정 무효(§1.11)")
    return row


def no_self_report_row(reports: list[dict], schema: dict) -> CheckRow:
    """`probe.no-self-report` — 각 보고가 probe-report/v0 스키마(additionalProperties false · 자기평가 필드 없음)를 통과."""
    row = CheckRow(check_id=CHECK_NO_SELF_REPORT, ruleset="probe-report/v0", ruleset_version=str(schema.get("title", "")), ruleset_size=1,
                   checked=len(reports))
    validator = Draft202012Validator(schema)
    for report in reports:
        for error in sorted(validator.iter_errors(report), key=lambda e: list(e.absolute_path)):
            locus = "/".join(str(step) for step in error.absolute_path) or "$"
            row.add(CHECK_NO_SELF_REPORT, f"{report.get('probe_id', '?')}#{locus}", error.message[:80], "probe-report/v0",
                    "프로브 보고가 스키마 밖이다 — 자기평가·점수 필드는 존재할 수 없다(D9)")
    return row


def independence_row(reports: list[dict], lanes: list[dict]) -> CheckRow:
    """`probe.independence` — n 좌표 상이 · 응답 지문 상이 · 보고 본문에 다른 좌표·probe_id 언급 없음."""
    row = CheckRow(check_id=CHECK_INDEPENDENCE, checked=len(reports))
    lane_ids = [str(lane.get("lane_id")) for lane in lanes]
    if len(set(lane_ids)) != len(lane_ids):
        row.add(CHECK_INDEPENDENCE, "lane_id", str(len(set(lane_ids))), str(len(lane_ids)), "두 계기가 같은 좌표에서 생성되었다")
    digests = [str(lane.get("response_digest")) for lane in lanes]
    if len(set(digests)) != len(digests):
        row.add(CHECK_INDEPENDENCE, "response_digest", str(len(set(digests))), str(len(digests)), "두 계기의 응답 바이트가 같다 — 독립 실행이 의심된다")
    ids = {str(r.get("probe_id")) for r in reports}
    for report, lane in zip(reports, lanes):
        body = json.dumps({"a": report.get("a_restatement"), "b": report.get("b_answers")}, ensure_ascii=False)
        for other in ids - {str(report.get("probe_id"))}:
            if re.search(r"\b" + re.escape(other) + r"\b", body):
                row.add(CHECK_INDEPENDENCE, f"{report.get('probe_id')}", other, "(없음)", "보고가 다른 계기를 참조한다")
        for other_lane in set(lane_ids) - {str(lane.get("lane_id"))}:
            if other_lane in body:
                row.add(CHECK_INDEPENDENCE, f"{report.get('probe_id')}", other_lane, "(없음)", "보고가 다른 계기의 좌표를 참조한다")
    return row


def target_coverage_row(per_target: list[dict], targets: list[str]) -> CheckRow:
    row = CheckRow(check_id=CHECK_TARGET_COVERAGE, checked=len(targets))
    covered = [t["material_id"] for t in per_target]
    for missing in [t for t in targets if t not in covered]:
        row.add(CHECK_TARGET_COVERAGE, missing, "(없음)", "per_target 행", "score.json 이 블루프린트 전달 표적을 덮지 않는다")
    for extra in [m for m in covered if m not in targets]:
        row.add(CHECK_TARGET_COVERAGE, extra, "per_target 행", "(없음)", "표적 밖 재료가 per_target 에 있다 — 이해 퀴즈가 되었다(§5.2)")
    return row


def grader_separation_row(grader: dict | None, probe_lanes: list[dict], *, probe_accepted: tuple[str, ...]) -> CheckRow:
    """`probe.grader-separation` — 채점 좌표·모델이 계기의 것과 다르다. 채점 레인이 돌지 않았으면(결정론만) checked 0 · empty-target."""
    row = CheckRow(check_id=CHECK_GRADER_SEPARATION, checked=0)
    if grader is None:
        row.extras["note"] = "모델 채점 대상 0 — 채점 레인 미호출(결정론 채점만)"
        return row
    row.checked = 2 + len(probe_lanes)
    grader_lane = str(grader.get("lane_id", ""))
    if not grader_lane.startswith(LANE_GRADE + "/"):
        row.add(CHECK_GRADER_SEPARATION, "lane_id", grader_lane, f"{LANE_GRADE}/…", "채점 산출의 좌표가 채점 레인 어휘가 아니다")
    for lane in probe_lanes:
        if str(lane.get("lane_id")) == grader_lane:
            row.add(CHECK_GRADER_SEPARATION, "lane_id", grader_lane, "계기 좌표와 다름", "채점 산출이 계기 좌표에서 나왔다 — 자기 채점(D9)")
    if str(grader.get("model")) in probe_accepted:
        row.add(CHECK_GRADER_SEPARATION, "model", str(grader.get("model")), f"계기 라벨 수용 집합 밖 {list(probe_accepted)}",
                "채점자가 계기와 같은 모델 계열이다 — 같은 편향을 공유한다(§5.5 E13)")
    return row


# ---------------------------------------------------------------------------
# ② 질문지
# ---------------------------------------------------------------------------


def _load_questions(paths: RunPaths, spec_digest: str, targets: list[str]) -> dict | None:
    path = paths.questions_json
    if not os.path.isfile(path):
        return None
    doc = load_json(path)
    if str(doc.get("spec_digest")) != spec_digest or [q["target_material_id"] for q in doc.get("questions") or []] != targets:
        raise StageError("60-probe/questions.json 이 다른 재료 판·다른 표적 위에 서 있다 — 런 단위 질문지는 같은 재료·같은 표적에만 재사용한다(§5.2)")
    return doc


def _questions_state(paths: RunPaths) -> dict:
    path = os.path.join(paths.probe_root, "questions-state.json")
    return load_json(path) if os.path.isfile(path) else {"attempt": 0}


def _ensure_questions(*, paths: RunPaths, repo: str, meta: dict, frozen_row: dict, variant: str, targets: list[str], config: dict,
                      adapter, contract: dict) -> tuple[dict | None, dict]:
    """→ (질문지 문서 | None(pending·escalate), 상태). 표적 부족 = retry(1) → escalate(계약 failure)."""
    spec_digest = str(frozen_row.get("spec_digest", ""))
    existing = _load_questions(paths, spec_digest, targets)
    if existing is not None:
        return existing, {"status": STATUS_OK, "reused": True}
    state = _questions_state(paths)
    state_path = os.path.join(paths.probe_root, "questions-state.json")
    entry = failure_entry(contract, "질문지 표적 부족")
    cap = int(re.fullmatch(r"retry\((\d+)\)", str(entry.get("action"))).group(1))
    attempt = int(state.get("attempt", 0))
    request = questions_mod.build_request(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, variant=variant, targets=targets,
                                          config=config, attempt=attempt)
    try:
        response = adapter.dispatch([request])[0]
    except LanePending as pending:
        return None, {"status": STATUS_PENDING, "pending": list(pending.pending), "lanes_root": pending.request_dir}
    accepted, discarded, missing = questions_mod.validate_questions(list(response.payload.get("questions") or []), targets)
    lane = {"lane_id": response.lane_id, "model": response.model, "effort": response.effort, "response_digest": response.response_digest,
            "mismatch": response.mismatches(request)}
    if missing:
        if attempt < cap:
            write_json(state_path, {"attempt": attempt + 1, "last_missing": missing, "last_lane": lane})
            request = questions_mod.build_request(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, variant=variant, targets=targets,
                                                  config=config, attempt=attempt + 1)
            try:
                adapter.dispatch([request])
            except LanePending as pending:
                return None, {"status": STATUS_PENDING, "pending": list(pending.pending), "lanes_root": pending.request_dir, "retry": attempt + 1,
                              "missing": missing}
            raise StageError("재시도 좌표에 응답이 이미 있다 — 질문지 상태가 어긋났다")
        escalation = {"variant": variant, "reason": f"질문지 표적 부족 — 재시도 상한 {cap} 소진 · {entry.get('note')}", "missing_targets": missing,
                      "discarded": discarded, "lane": lane, "attempts": attempt + 1}
        write_json(paths.probe_escalation_json(variant), escalation)
        return None, {"status": STATUS_ESCALATE, "escalation": paths.probe_escalation_json(variant), "missing": missing}
    doc = {
        "schema": QUESTIONS_SCHEMA, "run_id": str(meta.get("run_id", "")), "spec_version": int(frozen_row["spec_version"]),
        "spec_digest": spec_digest, "targets": list(targets), "questions": accepted, "discarded": discarded,
        "question_set_digest": questions_mod.question_set_digest(accepted), "lane": lane, "produced_at": _now_iso(),
    }
    write_json(paths.questions_json, doc)
    if os.path.isfile(state_path):
        os.remove(state_path)
    return doc, {"status": STATUS_OK, "reused": False, "lane": lane, "discarded": len(discarded)}


# ---------------------------------------------------------------------------
# ③④ 프로브 n · 정족수
# ---------------------------------------------------------------------------


def _quorum_state(paths: RunPaths, variant: str, n: int) -> dict:
    path = paths.probe_quorum_json(variant)
    if os.path.isfile(path):
        state = load_json(path)
        if int(state.get("n", 0)) != n:
            raise StageError(f"quorum.json 의 n({state.get('n')})이 계약 probe.n({n})과 다르다 — 대장을 새로 세우지 않는다(재정 P-6)")
        return state
    return {"n": n, "attempts_made": 0, "instances": {str(i): {"attempt": 0, "status": "pending"} for i in range(n)}}


def _supersede_stale_probe(paths: RunPaths, variant: str, index: int, previous_digest) -> None:
    """출하 후보가 바뀌면 옛 관측은 **그 후보의 것이 아니다** — 계기는 후보를 재는 도구이기 때문이다.

    보고와 레인 좌표를 직전 입력 지문 아래 보존하고 다시 묻는다. 이것이 없으면 옛 답변을 새 후보의
    지문으로 채점해 `score.json#input_digest` 는 현 후보를 가리키는데 내용은 옛 판이 된다 — CP2 의
    「계기가 현 출하 후보의 관측인가」 검사가 그대로 통과하므로 어떤 결정론 검사도 이 오염을 잡지 못한다
    (런 -3 09:50 실측 = 무효 답변 16 인데도 `probe ok`).
    """
    tag = str(previous_digest or "unknown").replace("sha256:", "")[:16]
    keep_root = os.path.join(paths.probe_dir(variant), "superseded", tag)
    # 보고가 낡았으면 **그 보고로 만든 점수도 낡았다** — 함께 옮기지 않으면 새 답변을 받고도 옛 점수가
    # 재진입 가드를 통과해 그대로 남는다(런 -3 10:00 실측).
    for stale_path in (paths.score_json(variant), paths.probe_grades_json(variant)):
        if os.path.isfile(stale_path):
            os.makedirs(keep_root, exist_ok=True)
            moved = os.path.join(keep_root, os.path.basename(stale_path))
            if os.path.exists(moved):
                os.remove(stale_path)
            else:
                os.replace(stale_path, moved)
    # 채점 레인의 옛 응답도 같이 간다 — 남겨 두면 새 답변 위에 옛 등급이 붙는다.
    grade_lane = os.path.join(paths.probe_lanes_dir(variant), LANE_GRADE, variant, "batch-0")
    if os.path.isdir(grade_lane):
        os.makedirs(keep_root, exist_ok=True)
        moved = os.path.join(keep_root, "lane-grade")
        if os.path.exists(moved):
            shutil.rmtree(grade_lane)
        else:
            shutil.move(grade_lane, moved)
    report = paths.probe_report(variant, index)
    if os.path.isfile(report):
        os.makedirs(keep_root, exist_ok=True)
        target = os.path.join(keep_root, os.path.basename(report))
        if not os.path.exists(target):
            os.replace(report, target)
        elif os.path.isfile(report):
            os.remove(report)
    lane_dir = os.path.join(paths.probe_lanes_dir(variant), LANE_PROBE, variant, f"batch-{index}")
    if os.path.isdir(lane_dir):
        os.makedirs(keep_root, exist_ok=True)
        target = os.path.join(keep_root, f"lane-batch-{index}")
        if not os.path.exists(target):
            shutil.move(lane_dir, target)
        else:
            shutil.rmtree(lane_dir)


def _collect_probes(*, paths: RunPaths, repo: str, meta: dict, variant: str, text: str, input_digest: str, questions: dict, config: dict,
                    adapter, dead: list[str], report_schema: dict) -> tuple[list[dict], list[dict], dict, dict]:
    """→ (보고 n 건 | 부분, 레인 n 건 | 부분, 대장, 처분 `{status, pending|escalation}`)."""
    n = config["n"]
    state = _quorum_state(paths, variant, n)
    questions_text = questions_mod.probe_facing_text(questions["questions"])
    qs_digest = str(questions["question_set_digest"])
    reports: dict[int, dict] = {}
    lanes: dict[int, dict] = {}
    pending: list[str] = []
    dead_now: list[int] = []
    for i in range(n):
        inst = state["instances"][str(i)]
        report_path = paths.probe_report(variant, i)
        if os.path.isfile(report_path):
            kept = load_json(report_path)
            if str(kept.get("input_digest")) == input_digest and str(kept.get("question_set_digest")) == qs_digest:
                reports[i] = kept
                lanes[i] = dict(inst.get("lane") or {})
                inst["status"] = "live"
                continue
            # 후보가 바뀌었다 — 옛 관측은 버리지 않고 보존한 뒤 다시 묻는다.
            _supersede_stale_probe(paths, variant, i, kept.get("input_digest"))
            inst["attempt"] = 0
            inst["status"] = "pending"
        request = probes_mod.build_request(paths=paths, repo=repo, meta=meta, variant=variant, thread_text=text, input_digest=input_digest,
                                           questions=questions["questions"], questions_text=questions_text, question_set_digest=qs_digest,
                                           batch=i, config=config, attempt=int(inst["attempt"]))
        inst["lane_id"] = request.lane_id
        try:
            response = adapter.dispatch([request])[0]
        except LanePending:
            if request.lane_id in dead:
                dead_now.append(i)
            else:
                pending.append(request.lane_id)
            continue
        report = probes_mod.build_report(index=i, response=response, lane=config["lanes"][LANE_PROBE], input_digest=input_digest,
                                         question_set_digest=qs_digest, produced_at=_now_iso())
        errors = list(Draft202012Validator(report_schema).iter_errors(report))
        if errors:
            raise StageError(f"프로브 보고 {i} 가 probe-report/v0 밖이다: {errors[0].message}")
        write_json(report_path, report)
        inst.update({"status": "live", "lane": {"lane_id": response.lane_id, "model": response.model, "effort": response.effort,
                                                "response_digest": response.response_digest, "mismatch": response.mismatches(request)}})
        reports[i] = report
        lanes[i] = dict(inst["lane"])

    # 정족수 판정(재정 P-6 · engine/quorum.py) — 죽은 대만 재시도 · 살아있는 응답은 보존.
    if dead_now:
        roster = [quorum_mod.Instance(f"p{i}", quorum_mod.LIVE if i in reports else quorum_mod.DEAD,
                                      _rel(paths, paths.probe_report(variant, i)) if i in reports else None) for i in range(n)]
        decision = quorum_mod.evaluate(roster, attempts_made=int(state["attempts_made"]), repo=repo)
        state["last_decision"] = decision.to_dict()
        if decision.outcome == quorum_mod.RETRY:
            state["attempts_made"] = int(state["attempts_made"]) + 1
            for i in dead_now:
                inst = state["instances"][str(i)]
                inst["attempt"] = int(inst["attempt"]) + 1
                inst["status"] = "retrying"
                request = probes_mod.build_request(paths=paths, repo=repo, meta=meta, variant=variant, thread_text=text, input_digest=input_digest,
                                                   questions=questions["questions"], questions_text=questions_text, question_set_digest=qs_digest,
                                                   batch=i, config=config, attempt=int(inst["attempt"]))
                inst["lane_id"] = request.lane_id
                try:
                    adapter.dispatch([request])
                except LanePending:
                    pending.append(request.lane_id)
        else:
            write_json(paths.probe_escalation_json(variant), {"variant": variant, **decision.to_dict()})
            write_json(paths.probe_quorum_json(variant), state)
            return ([reports[i] for i in sorted(reports)], [lanes[i] for i in sorted(lanes)], state,
                    {"status": STATUS_ESCALATE, "escalation": paths.probe_escalation_json(variant), "live": len(reports), "dead": dead_now})
    write_json(paths.probe_quorum_json(variant), state)
    if pending or len(reports) != n:
        return ([reports[i] for i in sorted(reports)], [lanes[i] for i in sorted(lanes)], state,
                {"status": STATUS_PENDING, "pending": pending, "live": len(reports)})
    return [reports[i] for i in range(n)], [lanes[i] for i in range(n)], state, {"status": STATUS_OK}


# ---------------------------------------------------------------------------
# ⑥ 채점
# ---------------------------------------------------------------------------


def _grade(*, paths: RunPaths, repo: str, meta: dict, variant: str, reports: list[dict], questions: list[dict], items: dict, config: dict,
           thesis_en: str, invalid: set[tuple[str, str]], adapter) -> tuple[dict | None, dict]:
    """→ (grades 문서 | None(pending), 처분). grades.json 이 있으면 재사용."""
    grades_path = paths.probe_grades_json(variant)
    grading = config["grading"]
    grading_input = grade_mod.build_grading_input(reports=reports, questions=questions, items=items, grading=grading, thesis_en=thesis_en, invalid=invalid)
    grading_input_digest = sha256_bytes(json.dumps(grading_input, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    if os.path.isfile(grades_path):
        kept = load_json(grades_path)
        if str(kept.get("grading_input_digest")) == grading_input_digest:
            return kept, {"status": STATUS_OK, "reused": True}
        # 채점 입력이 바뀌었다(답변이 새로 왔다) — 옛 등급을 새 답변 위에 붙이지 않는다.
        keep_root = os.path.join(paths.probe_dir(variant), "superseded", str(kept.get("grading_input_digest") or "unknown").replace("sha256:", "")[:16])
        os.makedirs(keep_root, exist_ok=True)
        moved = os.path.join(keep_root, "grades.json")
        os.remove(grades_path) if os.path.exists(moved) else os.replace(grades_path, moved)
        lane_dir = os.path.join(paths.probe_lanes_dir(variant), LANE_GRADE, variant, "batch-0")
        if os.path.isdir(lane_dir):
            target = os.path.join(keep_root, "lane-grade")
            shutil.rmtree(lane_dir) if os.path.exists(target) else shutil.move(lane_dir, target)
    deterministic: dict[str, dict] = {}
    for question in questions:
        item = items[question["target_material_id"]]
        if grade_mod.method_for(str(item["kind"]), grading) != grade_mod.METHOD_DETERMINISTIC:
            continue
        for report in reports:
            for answer in report["b_answers"]:
                if answer["question_id"] == question["question_id"] and (report["probe_id"], answer["question_id"]) not in invalid:
                    deterministic[f"{report['probe_id']}|{question['question_id']}"] = {"grade": grade_mod.grade_deterministic(item, answer),
                                                                                       "evidence": "deterministic"}
    model_grades: dict[str, dict] = {}
    judgements: dict[str, str] = {}
    grader = None
    if grade_mod.model_grades_needed(grading_input):
        request = grade_mod.build_grade_request(paths=paths, repo=repo, meta=meta, variant=variant, grading_input=grading_input, config=config)
        try:
            response = adapter.dispatch([request])[0]
        except LanePending as pending:
            return None, {"status": STATUS_PENDING, "pending": list(pending.pending), "lanes_root": pending.request_dir}
        try:
            graded, judged = grade_mod.apply_model_grades(grading_input, response.payload)
        except ValueError as exc:
            raise StageError(f"채점 응답이 입력과 어긋난다: {exc}") from exc
        model_grades = {f"{p}|{q}": v for (p, q), v in graded.items()}
        judgements = dict(judged)
        grader = {"lane_id": response.lane_id, "model": response.model, "effort": response.effort, "response_digest": response.response_digest,
                  "mismatch": response.mismatches(request)}
    doc = {"variant": variant, "deterministic": deterministic, "model": model_grades, "restatement": judgements, "grader": grader,
           "grading_input_digest": sha256_bytes(json.dumps(grading_input, ensure_ascii=False, sort_keys=True).encode("utf-8"))}
    write_json(grades_path, doc)
    return doc, {"status": STATUS_OK, "reused": False}


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


def run(*, run_root: str, repo: str | None = None, variant: str, adapter=None, dead: list[str] | None = None) -> dict:
    """계기 1회 진입(변주 1건). 반환 `{status: ok|pending|escalate|reentered|halt, ...}` — halt 는 기록 뒤 `StageHaltError`.

    `dead` = 구동기가 신고한 죽은 좌표(응답 없이 호출이 실패한 lane_id). 러너는 파일만 보므로 사망을 스스로 알 수 없다 —
    신고된 좌표만 죽은 인스턴스로 세고(재정 P-6) 나머지 미도착은 `pending` 이다.
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID, inputs={"spec_version": version, "variant": variant})
    config = probe_config(repo, contract)
    verdict = load_json(paths.verdict_json(variant))
    if verdict.get("decision") != DECISION_ADVANCE:
        raise StageError(f"decision 이 advance 가 아니다({verdict.get('decision')}) — 계기는 게이트를 통과한 출하 후보만 잰다")
    text = read_text(paths.thread_stripped_md(variant))
    input_digest = sha256_bytes(text.encode("utf-8"))
    frozen = load_json(paths.frozen_spec(version))
    blueprint = load_json(paths.blueprint_json)
    targets = targets_of(blueprint)
    items = items_by_id(frozen)
    unknown = [t for t in targets if t not in items]
    if unknown:
        raise StageError(f"transmission_targets 가 동결본에 없는 항목을 가리킨다: {unknown}")
    report_schema = load_json(os.path.join(repo, *REPORT_SCHEMA_REL))
    score_schema = load_json(os.path.join(repo, *SCORE_SCHEMA_REL))
    run_id = str(meta.get("run_id", ""))
    paths.ensure_probe_dirs([variant])
    adapter = adapter or FileLaneAdapter(paths.probe_lanes_dir(variant), repo)
    rows: list[CheckRow] = [entry_row]

    # ① 입력 청정 — 위반 = halt(측정 무효).
    clean = input_clean_row(text, config["input_clean_patterns"])
    rows.append(clean)
    if clean.status == "fail":
        entry = failure_entry(contract, "probe.input-clean 실패")
        _write_check_report(paths, variant, "halt", rows, {})
        first = clean.findings[0]
        raise StageHaltError(f"[{entry.get('action')}] probe.input-clean 실패 — {first.locus}: {first.found!r}. {entry.get('note')}")

    # 재진입 — score.json 이 같은 입력·질문지 위에 있으면 재계산하지 않는다.
    score_path = paths.score_json(variant)
    if os.path.isfile(score_path):
        score = load_json(score_path)
        existing_q = _load_questions(paths, spec_digest, targets)
        if score.get("input_digest") == input_digest and existing_q is not None and score.get("question_set_digest") == existing_q.get("question_set_digest"):
            # 지문이 같아도 **보고가 현 후보의 것일 때만** 재진입이다. 후보가 바뀐 뒤 옛 답변으로 채점하면
            # score 의 지문만 새 후보를 가리키게 되어 CP2 의 「현 후보의 관측인가」 검사가 무력화된다.
            fresh = []
            for i in range(int(config["n"])):
                report_i = paths.probe_report(variant, i)
                fresh.append(os.path.isfile(report_i)
                             and str(load_json(report_i).get("input_digest")) == input_digest)
            # 점수가 **현 채점의 산물**인지도 본다 — 후보가 그대로여도 답변이 새로 오면 값이 바뀐다.
            grades_path = paths.probe_grades_json(variant)
            graded_here = (os.path.isfile(grades_path) and score.get("grading_input_digest")
                           and str(load_json(grades_path).get("grading_input_digest")) == str(score.get("grading_input_digest")))
            if all(fresh) and graded_here:
                return _result(STATUS_REENTERED, delivery_fidelity=score.get("delivery_fidelity"), score=score_path, reentered=True)

    # ② 질문지(런 단위).
    questions, q_state = _ensure_questions(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, variant=variant, targets=targets,
                                           config=config, adapter=adapter, contract=contract)
    if questions is None:
        return _result(q_state["status"], phase="questions", rows=rows, lanes_root=q_state.get("lanes_root"), pending=q_state.get("pending", []),
                       escalation=q_state.get("escalation"), missing=q_state.get("missing"))

    # ③④ 프로브 n · 정족수.
    reports, probe_lanes, state, disposition = _collect_probes(paths=paths, repo=repo, meta=meta, variant=variant, text=text, input_digest=input_digest,
                                                                questions=questions, config=config, adapter=adapter, dead=list(dead or []),
                                                                report_schema=report_schema)
    if disposition["status"] != STATUS_OK:
        return _result(disposition["status"], phase="probes", rows=rows, lanes_root=paths.probe_lanes_dir(variant), pending=disposition.get("pending", []),
                       escalation=disposition.get("escalation"), live=disposition.get("live"), n=config["n"])

    # ⑤ 무효 답변.
    invalidated: list[dict] = []
    for report in reports:
        invalidated.extend(probes_mod.invalid_answers(report, text))
    invalid = {(row["probe_id"], row["question_id"]) for row in invalidated}

    # ⑥ 채점.
    thesis_en = str(((blueprint.get("hook") or {}).get("thesis_en")) or "")
    grades, g_state = _grade(paths=paths, repo=repo, meta=meta, variant=variant, reports=reports, questions=questions["questions"], items=items,
                             config=config, thesis_en=thesis_en, invalid=invalid, adapter=adapter)
    if grades is None:
        return _result(STATUS_PENDING, phase="grade", rows=rows, lanes_root=g_state.get("lanes_root"), pending=g_state.get("pending", []))

    # ⑦ 국소화 · ⑧ score.json
    index = load_json(paths.annotation_index_json(variant))
    grading = config["grading"]
    per_target: list[dict] = []
    for question in questions["questions"]:
        item = items[question["target_material_id"]]
        method = grade_mod.method_for(str(item["kind"]), grading)
        verdicts: list[dict] = []
        for report in reports:
            answer = next(a for a in report["b_answers"] if a["question_id"] == question["question_id"])
            key = f"{report['probe_id']}|{question['question_id']}"
            table = grades["deterministic"] if method == grade_mod.METHOD_DETERMINISTIC else grades["model"]
            verdicts.append({"probe_id": report["probe_id"], "answer_kind": answer["answer_kind"], "invalid": (report["probe_id"], question["question_id"]) in invalid,
                             "grade": (table.get(key) or {}).get("grade")})
        per_target.append(localize_mod.target_row(material_id=item["id"], kind=str(item["kind"]), method=method, verdicts=verdicts, index=index,
                                                  scores=grading["scores"]))
    restatement = {value: 0 for value in grading["restatement"]}
    for judgement in (grades.get("restatement") or {}).values():
        restatement[str(judgement)] = restatement.get(str(judgement), 0) + 1
    notes = (f"계기 {config['n']} 대 · 질문 {len(questions['questions'])} · 무효 답변 {len(invalidated)} · 결정론 채점 "
             f"{sum(1 for t in per_target if t['method'] == grade_mod.METHOD_DETERMINISTIC)} 표적 · 모델 채점 "
             f"{sum(1 for t in per_target if t['method'] == grade_mod.METHOD_MODEL)} 표적. 계기는 거부권이 없다(SPEC §5.7).")
    score = localize_mod.build_score(run_id=run_id, variant=variant, n=config["n"], input_digest=input_digest,
                                     question_set_digest=str(questions["question_set_digest"]), per_target=per_target, restatement=restatement,
                                     invalidated=invalidated, notes=notes,
                                     grading_input_digest=str(grades.get("grading_input_digest") or "") or None)
    errors = list(Draft202012Validator(score_schema).iter_errors(score))
    if errors:
        raise StageError(f"score.json 이 probe-score/v0 밖이다: {errors[0].message}")

    # ⑨ 검사 5.
    rows.append(independence_row(reports, probe_lanes))
    rows.append(no_self_report_row(reports, report_schema))
    rows.append(target_coverage_row(per_target, targets))
    probe_accepted = _accepted_models(paths.contracts["read"].get("lane") or {}, config["lanes"][LANE_PROBE]["model"])
    rows.append(grader_separation_row(grades.get("grader"), probe_lanes, probe_accepted=probe_accepted))
    write_json(score_path, score)
    lanes_out = {"questions": questions.get("lane"), "probes": probe_lanes, "grader": grades.get("grader"), "quorum": state.get("last_decision")}
    status = "halt" if any(row.check_id == CHECK_GRADER_SEPARATION and row.status == "fail" for row in rows) else STATUS_OK
    _write_check_report(paths, variant, status, rows, lanes_out)
    if status == "halt":
        entry = failure_entry(contract, "probe.grader-separation 실패")
        raise StageHaltError(f"[{entry.get('action')}] probe.grader-separation 실패 — {entry.get('note')}")
    failed = [row.check_id for row in rows if row.status == "fail"]
    return _result(STATUS_OK, rows=rows, delivery_fidelity=score["delivery_fidelity"], per_target=len(per_target), invalidated=len(invalidated),
                   restatement=restatement, failed_checks=failed, score=score_path, lanes=lanes_out, n=config["n"],
                   questions_reused=bool(q_state.get("reused")), grades_reused=bool(g_state.get("reused")))


def _write_check_report(paths: RunPaths, variant: str, status: str, rows: list[CheckRow], lanes: dict) -> None:
    write_json(paths.probe_check_report(variant), {"stage": STAGE_ID, "variant": variant, "status": status, "rows": rows_to_dicts(rows),
                                                   "findings": findings_of(rows), "lanes": lanes, "produced_at": _now_iso()})


__all__ = ["CHECK_GRADER_SEPARATION", "CHECK_INDEPENDENCE", "CHECK_INPUT_CLEAN", "CHECK_NO_SELF_REPORT", "CHECK_TARGET_COVERAGE",
           "grader_separation_row", "independence_row", "input_clean_row", "no_self_report_row", "run", "target_coverage_row"]
