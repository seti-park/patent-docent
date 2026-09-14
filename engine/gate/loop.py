# -*- coding: utf-8 -*-
"""국소 수정 라운드(재정 2026-09-13 T67 ② · M6-a · SPEC §1.10 루프 위상 · D8).

한 라운드 `r<n>` 의 위상(전부 파일 상태로 재진입 안전):

① `50-gate/<v>/revisions/r<n>/directives.json` — `{round, thread_digest, final_eyes_brief_digest, directives[]}`. `directives[]` =
   verdict 의 L0+L1 `defects[]` 전건(`{id, layer, rule, locus, fix_directive}`). flag 는 넣지 않는다(루프를 돌리지 않는다 · §4.2).
② compose 회차(`compose-r<m>/<v>/batch-0` · 기존 회차 규약 · `directives` 인자 → 지시 표 인라인). 펜 미도착 = `pending`.
③ 결과 사본 → `revisions/r<n>/thread.annotated.md`(지시와 결과를 함께 · §1.10). 현행본은 회차 규약대로 `40-compose/<v>/thread.annotated.md`
   (직전 판은 `40-compose/<v>/rounds/r<m-1>/`).
④ **국소성 검사**(총괄 재량 ⓒ · 새 id 아님 · finding rule `annotation.schema` · 「지시 밖 문장이 바뀌었다」) — 지시 좌표 밖 문장이
   바이트 동일한가. 다르면 그 라운드 실패(캡 계수) · 현행본을 직전 판으로 되돌린다(D8 — 지시 밖을 고친 판은 수정 결과가 아니다).
⑤ gate-l0 → gate-l1 재판정(`rounds/` 보존은 러너 규약) · `revision_round = n` · 캡 도달 후에도 결함이면 `decision: escalate` +
   `escalation.json`.

라운드 상태 = `revisions/r<n>/round.json` `{round, status: open|closed, outcome}`. 열린 라운드가 있으면 그 라운드를 잇는다.
★ 캡(`gate.yaml#loop.revision_cap`) · 규칙 id · 좌표계를 코드에 두지 않는다.

**자유 리비전**(재정 2026-09-13 T69 ⑥ · SPEC §1.10 판단 경로 · D8) = `free_revision`. L2 메모 1회 → 펜 자유 리비전 1회 → 위상 봉쇄.
`revisions/free-r1/` 에 `memo.json`(메모 = 데이터 · 개시 판 지문) + `thread.annotated.md`(결과 사본) + `round.json`. compose 회차의
지시 블록은 긍정형 한 단락(「메모를 읽고 네 판단으로 고쳐 쓴다 · 규약 동일 · 고칠 곳이 없으면 원문 그대로」)이고 메모 표는 데이터 절이다.
그 뒤 L0·L1 재판정(`revision_round` 은 결함 루프 계수라 올리지 않는다) · `free_revision_used: true` · L2 는 다시 돌지 않는다.
국소성 검사는 걸지 않는다 — 자유 리비전은 정의상 전역이다.
"""

from __future__ import annotations

import os
import shutil

from reader.lib.report import CheckRow, Finding

from ..annotation.parse import RULE_SCHEMA, parse as parse_annotation
from ..annotation.strip import strip
from ..paths import RunPaths, load_format_parameters, repo_root
from ..stages import StageError, load_json, read_text, rows_to_dicts, sha256_bytes, sha256_file, write_json, write_text
from ..stages import compose as compose_stage
from ..stages import gate as gate_stage

DIRECTIVES_BASENAME = "directives.json"
MEMO_BASENAME = "memo.json"
OUTCOME_UNCHANGED = "unchanged"
FREE_REVISION_REASON = "free revision after L2 memo (T69 ⑥ · D8)"
ROUND_BASENAME = "round.json"
RESULT_BASENAME = "thread.annotated.md"
LOCALITY_BASENAME = "locality.json"
LOCALITY_MESSAGE = "지시 밖 문장이 바뀌었다"
OUTCOME_JUDGED = "judged"
OUTCOME_LOCALITY_FAILED = "locality-failed"
ESCALATION_REASON = "국소 수정 캡 초과 — 상류 결함 신호(대개 재료 반려행) · D8"


# ---------------------------------------------------------------------------
# 라운드 상태
# ---------------------------------------------------------------------------


def _round_dirs(paths: RunPaths, variant: str) -> list[int]:
    base = os.path.dirname(paths.revisions_dir(variant, 1))
    if not os.path.isdir(base):
        return []
    out = []
    for name in os.listdir(base):
        if name.startswith("r") and name[1:].isdigit():
            out.append(int(name[1:]))
    return sorted(out)


def _round_state(paths: RunPaths, variant: str, round_no: int) -> dict | None:
    path = os.path.join(paths.revisions_dir(variant, round_no), ROUND_BASENAME)
    return load_json(path) if os.path.isfile(path) else None


def open_round(paths: RunPaths, variant: str) -> int | None:
    """열린 라운드 번호(있으면). 닫힌 라운드만 있으면 None."""
    for number in reversed(_round_dirs(paths, variant)):
        state = _round_state(paths, variant, number)
        if state is None or state.get("status") == "open":
            return number
    return None


def directives_of(verdict: dict) -> list[dict]:
    out: list[dict] = []
    for layer in ("l0", "l1"):
        for record in (verdict.get(layer) or {}).get("defects") or []:
            out.append({"id": record["id"], "layer": record["layer"], "rule": record["rule"], "locus": dict(record["locus"]),
                        "fix_directive": record["fix_directive"]})
    return out


# ---------------------------------------------------------------------------
# 국소성 검사(재량 ⓒ)
# ---------------------------------------------------------------------------


def _sentence_tuples(text: str, slot_enum) -> tuple[dict, list[tuple[int, str, str]], dict[int, list[tuple]]]:
    """(프런트매터, [(n, slot, figspec)], {n: [(text_raw, citations, narrative)]}) — 파서 + strip 의 결정론 산출."""
    parsed = parse_annotation(text, slot_enum=slot_enum)
    if parsed.errors:
        raise StageError("국소성 검사 대상이 파싱되지 않는다: " + "; ".join(f"{e.locus}: {e.message}" for e in parsed.errors[:3]))
    stripped = strip(text)
    headers = [(t.n, t.slot, t.figspec) for t in parsed.tweets]
    sentences: dict[int, list[tuple]] = {}
    for tweet, stripped_tweet in zip(parsed.tweets, stripped.tweets):
        sentences[tweet.n] = [(raw, tuple(s.citations), bool(s.narrative))
                              for s, raw in zip(tweet.sentences, stripped_tweet.sentences_raw)]
    return dict(parsed.frontmatter), headers, sentences


def locality_check(before: str, after: str, directives: list[dict], *, slot_enum) -> CheckRow:
    """지시 좌표 밖은 바이트 동일해야 한다. 좌표 `sentence: null` 은 트윗 전체를 연다. 행 id 는 `annotation.schema`(새 id 아님)."""
    row = CheckRow(check_id=RULE_SCHEMA, checked=0)
    fm_before, headers_before, sent_before = _sentence_tuples(before, slot_enum)
    fm_after, headers_after, sent_after = _sentence_tuples(after, slot_enum)
    row.extras["locality"] = True
    if fm_before != fm_after:
        row.add(RULE_SCHEMA, "frontmatter", "(변경)", "(동일)", f"{LOCALITY_MESSAGE} — 프런트매터")
    if headers_before != headers_after:
        row.add(RULE_SCHEMA, "headers", str(headers_after), str(headers_before), f"{LOCALITY_MESSAGE} — 트윗 헤더·순서")
        return row
    open_tweets = {int(d["locus"]["tweet"]) for d in directives if d["locus"].get("tweet") is not None and d["locus"].get("sentence") is None}
    open_sentences = {(int(d["locus"]["tweet"]), int(d["locus"]["sentence"])) for d in directives
                      if d["locus"].get("tweet") is not None and d["locus"].get("sentence") is not None}
    for n, _slot, _fig in headers_before:
        if n in open_tweets:
            continue
        old_rows, new_rows = sent_before[n], sent_after.get(n, [])
        if len(old_rows) != len(new_rows):
            row.checked += 1
            row.add(RULE_SCHEMA, f"T{n}", str(len(new_rows)), str(len(old_rows)), f"{LOCALITY_MESSAGE} — 문장 수가 달라졌다")
            continue
        for index, (old, new) in enumerate(zip(old_rows, new_rows), start=1):
            if (n, index) in open_sentences:
                continue
            row.checked += 1
            if old != new:
                row.add(RULE_SCHEMA, f"T{n}/S{index}", new[0][:80], old[0][:80], LOCALITY_MESSAGE)
    return row


# ---------------------------------------------------------------------------
# 라운드
# ---------------------------------------------------------------------------


def _write_round(paths: RunPaths, variant: str, round_no: int, **state) -> None:
    write_json(os.path.join(paths.revisions_dir(variant, round_no), ROUND_BASENAME), {"round": round_no, **state})


def _write_escalation(paths: RunPaths, variant: str, verdict: dict, cap: int) -> str:
    path = paths.gate_escalation_json(variant)
    write_json(path, {
        "variant": variant, "reason": ESCALATION_REASON, "revision_round": verdict["revision_round"], "revision_cap": cap,
        "remaining_defects": [{"id": d["id"], "rule": d["rule"], "locus": d["locus"]} for d in directives_of(verdict)],
        "thread_digest": verdict["thread_digest"], "decision": verdict["decision"],
    })
    return path


def _result(status: str, **extra) -> dict:
    return {"status": status, "pending": [], "lanes_root": None, "rows": [], **extra}


def revise(*, run_root: str, repo: str | None = None, variant: str, adapter=None, l1_adapter=None) -> dict:
    """한 라운드(또는 열린 라운드의 다음 위상) 1회 진입. 반환 `{status: pending|ok|escalate|locality-failed, round, ...}`."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts["gate"]
    cap = gate_stage.revision_cap(contract)
    slot_enum = list(load_format_parameters(repo)["parameters"]["slot_enum"]["value"])
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError("verdict.json 이 없다 — gate-l0 · gate-l1 이 먼저다")
    verdict = load_json(verdict_path)
    current_text = read_text(paths.thread_annotated(variant))
    current_digest = sha256_bytes(current_text.encode("utf-8"))

    round_no = open_round(paths, variant)
    if round_no is None:
        # 새 라운드 — 전제 = decision revise · round < cap · 판정문이 현 주석본의 것.
        if verdict.get("decision") == gate_stage.DECISION_ESCALATE and int(verdict.get("revision_round", 0)) < cap:
            # 소진은 캡에 대한 상태이지 영구 판정이 아니다. 재정으로 캡이 늘면 풀린다(재정 2026-09-14 T70 ①).
            # `escalation.json` 은 지우지 않는다 — 그 시점의 진단은 사료로 남는다.
            verdict["decision"] = gate_stage.DECISION_REVISE
            write_json(verdict_path, verdict)
        if verdict.get("decision") != gate_stage.DECISION_REVISE:
            raise StageError(f"decision 이 revise 가 아니다({verdict.get('decision')}) — 수정 라운드를 열지 않는다")
        if int(verdict.get("revision_round", 0)) >= cap:
            raise StageError(f"revision_round {verdict.get('revision_round')} ≥ 캡 {cap} — escalate 상태다")
        if str(verdict.get("thread_digest")) != current_digest:
            raise StageError("verdict.json 이 현 주석본의 판정이 아니다 — gate-l0 를 먼저 돌린다")
        if not verdict.get("final_eyes_brief_digest"):
            raise StageError("final-eyes-brief.json 핀이 없다 — 루프는 gate-l1 이 발췌본을 만든 뒤에만 열린다(재정 N1)")
        directives = directives_of(verdict)
        if not directives:
            raise StageError("결함이 없는데 decision 이 revise 다 — 판정문이 어긋났다")
        round_no = int(verdict["revision_round"]) + 1
        write_json(os.path.join(paths.revisions_dir(variant, round_no), DIRECTIVES_BASENAME), {
            "round": round_no, "thread_digest": current_digest, "final_eyes_brief_digest": verdict["final_eyes_brief_digest"],
            "directives": directives,
        })
        _write_round(paths, variant, round_no, status="open", phase="compose", opened_from_verdict_digest=current_digest)

    round_dir = paths.revisions_dir(variant, round_no)
    directives_doc = load_json(os.path.join(round_dir, DIRECTIVES_BASENAME))
    directives = list(directives_doc["directives"])
    before_digest = str(directives_doc["thread_digest"])

    # ② compose 회차 — 현행본이 아직 라운드 개시 판이면 펜 요청·응답 소비.
    if current_digest == before_digest:
        report = compose_stage._existing_report(paths)  # noqa: SLF001 - 회차 기록의 정본 자리(러너 모듈 안)
        recorded = int(((report.get("rounds") or {}).get(variant)) or 1)
        outcome = compose_stage.run(run_root=run_root, repo=repo, adapter=adapter, variants=(variant,), round_no=recorded + 1,
                                    directives={"path": os.path.relpath(os.path.join(round_dir, DIRECTIVES_BASENAME), paths.run_root).replace(os.sep, "/"),
                                                "doc": directives_doc, "text": read_text(os.path.join(round_dir, DIRECTIVES_BASENAME))})
        if outcome["status"] == "pending":
            return _result("pending", round=round_no, phase="compose", pending=list(outcome["pending"]), lanes_root=outcome["lanes_root"],
                           rows=outcome["rows"])
        if outcome["status"] != "ok":
            return _result(outcome["status"], round=round_no, phase="compose", rows=outcome["rows"], reason_label=outcome.get("reason_label"))
        current_text = read_text(paths.thread_annotated(variant))
        current_digest = sha256_bytes(current_text.encode("utf-8"))
        if current_digest == before_digest:
            # 펜이 한 글자도 바꾸지 않았다 — 결과는 있으나 라운드는 진전이 없다. 재판정 위상으로 넘어가되 같은 판정이 나온다.
            pass

    # ③ 결과 사본(지시와 결과를 함께).
    result_copy = os.path.join(round_dir, RESULT_BASENAME)
    if not os.path.isfile(result_copy):
        write_text(result_copy, current_text)

    # ④ 국소성 검사 — 직전 판은 compose 회차 보존 자리(`40-compose/<v>/rounds/r<m>/`)에서 찾는다(지문으로 확인).
    locality_path = os.path.join(round_dir, LOCALITY_BASENAME)
    if not os.path.isfile(locality_path):
        previous_text = _find_previous_text(paths, variant, before_digest)
        row = locality_check(previous_text, current_text, directives, slot_enum=slot_enum)
        write_json(locality_path, {"round": round_no, "check_id": row.check_id, "status": row.status, "checked": row.checked,
                                   "findings": [f.as_dict() for f in row.findings]})
        if row.status == "fail":
            # 라운드 실패 — 현행본을 직전 판으로 되돌리고 캡을 센다. 되돌린 판은 verdict 의 판이므로 재판정이 필요 없다.
            write_text(paths.thread_annotated(variant), previous_text)
            verdict["revision_round"] = round_no
            verdict["decision"] = gate_stage.decide(l0_pass=bool(verdict["l0"]["pass"]), l1_pass=verdict["l1"]["pass"],
                                                    revision_round=round_no, cap=cap)
            write_json(verdict_path, verdict)
            escalation = _write_escalation(paths, variant, verdict, cap) if verdict["decision"] == gate_stage.DECISION_ESCALATE else None
            _write_round(paths, variant, round_no, status="closed", outcome=OUTCOME_LOCALITY_FAILED, restored_digest=before_digest,
                         rejected_digest=current_digest)
            return _result(OUTCOME_LOCALITY_FAILED, round=round_no, phase="locality", rows=[row], decision=verdict["decision"],
                           revision_round=round_no, escalation=escalation, findings=[f.as_dict() for f in row.findings])

    # ⑤ 재판정 — L0(지문이 바뀌었으면 rounds/ 보존 뒤 재계산) → revision_round = n → L1.
    gate_stage.run(run_root=run_root, repo=repo, variants=[variant])
    verdict = load_json(verdict_path)
    if int(verdict.get("revision_round", 0)) != round_no:
        verdict["revision_round"] = round_no
        verdict["decision"] = gate_stage.decide(l0_pass=bool(verdict["l0"]["pass"]), l1_pass=verdict["l1"]["pass"],
                                                revision_round=round_no, cap=cap)
        write_json(verdict_path, verdict)
    l1 = gate_stage.run_l1(run_root=run_root, repo=repo, variant=variant, adapter=l1_adapter)
    if l1["status"] == "pending":
        _write_round(paths, variant, round_no, status="open", phase="gate-l1")
        return _result("pending", round=round_no, phase="gate-l1", pending=list(l1["pending"]), lanes_root=l1["lanes_root"])
    verdict = load_json(verdict_path)
    escalation = _write_escalation(paths, variant, verdict, cap) if verdict["decision"] == gate_stage.DECISION_ESCALATE else None
    _write_round(paths, variant, round_no, status="closed", outcome=OUTCOME_JUDGED, decision=verdict["decision"],
                 thread_digest=verdict["thread_digest"])
    status = "escalate" if escalation else "ok"
    return _result(status, round=round_no, phase="judged", decision=verdict["decision"], revision_round=verdict["revision_round"],
                   l0_pass=bool(verdict["l0"]["pass"]), l1_pass=verdict["l1"]["pass"], defects=len(directives_of(verdict)),
                   escalation=escalation)


def _find_previous_text(paths: RunPaths, variant: str, digest: str) -> str:
    """지문이 `digest` 인 직전 판 — compose 회차 보존 자리에서 찾는다(없으면 StageError)."""
    base = os.path.dirname(paths.compose_round_dir(variant, 1))
    candidates: list[str] = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base), reverse=True):
            path = os.path.join(base, name, RESULT_BASENAME)
            if os.path.isfile(path):
                candidates.append(path)
    for path in candidates:
        if sha256_file(path) == digest:
            return read_text(path)
    raise StageError(f"직전 판(지문 {digest})을 40-compose/{variant}/rounds/ 에서 찾지 못했다 — 국소성 검사 불가")


# ---------------------------------------------------------------------------
# 자유 리비전 (재정 2026-09-13 T69 ⑥ · SPEC §1.10 판단 경로 · D8)
# ---------------------------------------------------------------------------


def _free_state(paths: RunPaths, variant: str) -> dict | None:
    path = os.path.join(paths.free_revision_dir(variant), ROUND_BASENAME)
    return load_json(path) if os.path.isfile(path) else None


def _write_free_state(paths: RunPaths, variant: str, **state) -> None:
    write_json(os.path.join(paths.free_revision_dir(variant), ROUND_BASENAME), {"round": "free-r1", **state})


def _close_free(paths: RunPaths, variant: str, verdict_path: str, verdict: dict, memos: list[dict], *, outcome: str,
                previous_round: int, cap: int, lane: dict) -> dict:
    """판정문에 메모를 이어 붙이고 `free_revision_used` 를 세운다. `revision_round` 은 결함 루프 계수라 **되돌린다**(올리지 않는다)."""
    verdict["l2"] = {"memos": memos}
    verdict["free_revision_used"] = True
    verdict["revision_round"] = previous_round
    verdict["decision"] = gate_stage.decide(l0_pass=bool(verdict["l0"]["pass"]), l1_pass=verdict["l1"]["pass"],
                                            revision_round=previous_round, cap=cap, spec_ok=True)
    verdict["inactive_layers"] = [row for row in verdict["inactive_layers"] if row.get("layer") not in gate_stage.L2_PENDING_LAYERS]
    write_json(verdict_path, verdict)
    write_text(paths.l2_md(variant), gate_stage.render_l2_md(verdict=verdict, memos=memos, lane=lane, free_revision_used=True))
    escalation = _write_escalation(paths, variant, verdict, cap) if verdict["decision"] == gate_stage.DECISION_ESCALATE else None
    _write_free_state(paths, variant, status="closed", outcome=outcome, decision=verdict["decision"], thread_digest=verdict["thread_digest"])
    return _result("escalate" if escalation else "ok", round="free-r1", phase="judged", outcome=outcome, decision=verdict["decision"],
                   revision_round=verdict["revision_round"], free_revision_used=True, l0_pass=bool(verdict["l0"]["pass"]),
                   l1_pass=verdict["l1"]["pass"], defects=len(directives_of(verdict)), escalation=escalation)


def free_revision(*, run_root: str, repo: str | None = None, variant: str, adapter=None, l1_adapter=None) -> dict:
    """L2 메모 1회에 대한 펜 자유 리비전 1회. 반환 `{status: pending|ok|escalate, round: free-r1, phase, ...}`.

    전제 = `verdict.json#decision == advance` · L2 메모가 기록되어 있다(`l2.md` 실재) · 아직 소비되지 않았다(`free_revision_used` 아님).
    메모가 0 건이면 리비전을 열지 않는다(고칠 근거가 없다 · `StageError`).
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts["gate"]
    cap = gate_stage.revision_cap(contract)
    free_cap = (contract.get("loop") or {}).get("free_revision")
    if not isinstance(free_cap, int) or free_cap != 1:
        raise StageError(f"gate.yaml#loop.free_revision 이 1 이 아니다({free_cap!r}) — 판단 경로는 1회 왕복이다(D8)")
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError("verdict.json 이 없다 — gate-l0 · gate-l1 · gate-l2 가 먼저다")
    verdict = load_json(verdict_path)
    current_text = read_text(paths.thread_annotated(variant))
    current_digest = sha256_bytes(current_text.encode("utf-8"))
    state = _free_state(paths, variant)
    if state is not None and state.get("status") == "closed":
        raise StageError("자유 리비전은 1회다 — 이미 소비되었다(위상 봉쇄 · D8)")
    free_dir = paths.free_revision_dir(variant)
    memo_path = os.path.join(free_dir, MEMO_BASENAME)

    if state is None:
        if verdict.get("free_revision_used") is True:
            raise StageError("verdict.json 이 이미 free_revision_used 다 — 위상 봉쇄(D8)")
        if verdict.get("decision") != gate_stage.DECISION_ADVANCE:
            raise StageError(f"decision 이 advance 가 아니다({verdict.get('decision')}) — 자유 리비전은 통과본 위에서만 돈다")
        if str(verdict.get("thread_digest")) != current_digest:
            raise StageError("verdict.json 이 현 주석본의 판정이 아니다 — gate-l0 를 먼저 돌린다")
        if not os.path.isfile(paths.l2_md(variant)):
            raise StageError("l2.md 가 없다 — gate-l2 가 먼저다(메모 없이는 자유 리비전의 근거가 없다)")
        memos = list((verdict.get("l2") or {}).get("memos") or [])
        if not memos:
            raise StageError("L2 메모가 0 건이다 — 고칠 근거가 없으므로 자유 리비전을 열지 않는다")
        if not verdict.get("final_eyes_brief_digest"):
            raise StageError("final-eyes-brief.json 핀이 없다 — 루프는 gate-l1 이 발췌본을 만든 뒤에만 열린다(재정 N1)")
        write_json(memo_path, {
            "round": "free-r1", "thread_digest": current_digest, "final_eyes_brief_digest": verdict["final_eyes_brief_digest"],
            "revision_round": int(verdict.get("revision_round", 0)), "l2_md_digest": sha256_file(paths.l2_md(variant)), "memos": memos,
        })
        _write_free_state(paths, variant, status="open", phase="compose", opened_from_verdict_digest=current_digest)
        state = _free_state(paths, variant)

    memo_doc = load_json(memo_path)
    memos = list(memo_doc["memos"])
    before_digest = str(memo_doc["thread_digest"])
    previous_round = int(memo_doc.get("revision_round", 0))
    lane = {"lane_id": None, "model": None, "effort": None}

    # ② compose 회차 — 현행본이 아직 개시 판이면 펜 요청·응답 소비.
    if current_digest == before_digest and not os.path.isfile(os.path.join(free_dir, RESULT_BASENAME)):
        report = compose_stage._existing_report(paths)  # noqa: SLF001
        recorded = int(((report.get("rounds") or {}).get(variant)) or 1)
        outcome = compose_stage.run(run_root=run_root, repo=repo, adapter=adapter, variants=(variant,), round_no=recorded + 1,
                                    memo={"path": os.path.relpath(memo_path, paths.run_root).replace(os.sep, "/"),
                                          "doc": memo_doc, "text": read_text(memo_path)})
        if outcome["status"] == "pending":
            return _result("pending", round="free-r1", phase="compose", pending=list(outcome["pending"]), lanes_root=outcome["lanes_root"],
                           rows=outcome["rows"])
        if outcome["status"] != "ok":
            return _result(outcome["status"], round="free-r1", phase="compose", rows=outcome["rows"], reason_label=outcome.get("reason_label"))
        current_text = read_text(paths.thread_annotated(variant))
        current_digest = sha256_bytes(current_text.encode("utf-8"))

    # ③ 결과 사본(메모와 결과를 함께).
    result_copy = os.path.join(free_dir, RESULT_BASENAME)
    if not os.path.isfile(result_copy):
        write_text(result_copy, current_text)

    # ④ 원문 그대로 낸 응답 — 재판정 없이 닫는다(판정문은 그 판의 것이다).
    if current_digest == before_digest:
        verdict = load_json(verdict_path)
        return _close_free(paths, variant, verdict_path, verdict, memos, outcome=OUTCOME_UNCHANGED, previous_round=previous_round, cap=cap, lane=lane)

    # ⑤ 재판정 — L0(지문이 바뀌었으면 rounds/ 보존 뒤 재계산) → L1. revision_round 은 올리지 않는다.
    gate_stage.run(run_root=run_root, repo=repo, variants=[variant])
    l1 = gate_stage.run_l1(run_root=run_root, repo=repo, variant=variant, adapter=l1_adapter)
    if l1["status"] == "pending":
        _write_free_state(paths, variant, status="open", phase="gate-l1")
        return _result("pending", round="free-r1", phase="gate-l1", pending=list(l1["pending"]), lanes_root=l1["lanes_root"])
    verdict = load_json(verdict_path)
    return _close_free(paths, variant, verdict_path, verdict, memos, outcome=OUTCOME_JUDGED, previous_round=previous_round, cap=cap, lane=lane)


__all__ = ["DIRECTIVES_BASENAME", "ESCALATION_REASON", "FREE_REVISION_REASON", "LOCALITY_MESSAGE", "MEMO_BASENAME", "OUTCOME_JUDGED",
           "OUTCOME_LOCALITY_FAILED", "OUTCOME_UNCHANGED", "directives_of", "free_revision", "locality_check", "open_round", "revise"]
