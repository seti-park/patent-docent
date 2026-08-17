# -*- coding: utf-8 -*-
"""`read` 스테이지 — D5 5단계 독해 실행 경로.

계약 = `contracts/stages/read.yaml`(정본 서술 = SPEC §1.4 + §1.5 CP1).

이 스테이지가 하는 일은 셋이다.

① **레인을 돌린다.** D5 5단계를 하위 작업 4종으로 전개해 두 독립 실행(`read-a`·`read-b`)에
   각각 태운다. 두 실행이 필요한 이유는 품질이 아니라 **안정성**이다 — 두 독해가 다른
   청구항 트리를 낳으면 이후 모든 결정론 검사의 기준점이 흔들린다.
② **조립하고 검사한다.** 레인 산출을 재료 명세로 조립하고 `reader/lib` 의 검사 8종을
   돌린다. 검사 구현은 여기 없다(이식 단위 안에 있다).
③ **CP1 표면을 낸다.** 중간 산출물과 KR 판독본을 남긴다. 감춰진 예외는 예외가 아니라 은폐다.

정본 재료는 `read-a` 의 산출이며 `read-b` 는 **수렴 비교 전용**이다. 그 사실은
`provenance.read_runs[]` 와 판독본 §12 에 남는다.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone

from jsonschema import Draft202012Validator

from reader.lib import run_read_checks, to_convergence_payload
from reader.lib.report import CheckContext, CheckRow
from reader.lib.rules import Rules
from reader.lib.spec_io import load_schema

from . import (
    StageError,
    failure_entry,
    findings_of,
    load_yaml,
    read_text,
    sha256_bytes,
    write_json,
    write_text,
)
from ..lanes.contract import LaneRequest, LaneResponse
from ..lanes.plan import (
    lane_profiles,
    plan_decompose,
    plan_grounding,
    plan_synthesis,
)
from ..paths import RunPaths, reader_version, repo_root
from ..read_view import ReadView
from ..render.material_spec_md import render

STAGE_ID = "read"
CONVERGENCE_SCHEMA = ("contracts", "schemas", "convergence.schema.json")
RETRY_PATTERN = re.compile(r"retry\((?P<count>\d+)\)")


class LaneAssignmentError(StageError):
    """레인이 요청과 다른 모델·effort 로 돌았다(조용한 대체 금지 — SPEC §7.3 규율 4)."""


class RunnerContractError(StageError):
    """러너 산출이 자기 계약(`convergence/v0`)을 위반했다."""


# ---------------------------------------------------------------------------
# 레인 왕복 기록
# ---------------------------------------------------------------------------


class LaneJournal:
    """전 요청·응답의 배정 기록. `10-read/lanes/lane-log.json` 의 본문이 된다."""

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def record(self, request: LaneRequest, response: LaneResponse | None) -> None:
        mismatch = response is not None and response.mismatches(request)
        self.rows.append(
            {
                "lane_id": request.lane_id,
                "read_run": request.read_run,
                "task": request.task,
                "batch": request.batch,
                "requested_model": request.model,
                "requested_effort": request.effort,
                "actual_model": response.model if response else None,
                "actual_effort": response.effort if response else None,
                "ok": response is not None and not mismatch,
                "mismatch": mismatch,
            }
        )

    def mismatched(self) -> list[dict]:
        return [row for row in self.rows if row["mismatch"]]


def _dispatch(adapter, requests: list[LaneRequest], journal: LaneJournal) -> list[LaneResponse]:
    """배치 1개를 보내고 배정 기록을 남긴다. 응답 순서는 요청 순서에 맞춘다."""
    responses = adapter.dispatch(requests)
    by_id = {response.lane_id: response for response in responses}
    ordered: list[LaneResponse] = []
    for request in requests:
        response = by_id.get(request.lane_id)
        journal.record(request, response)
        if response is None:
            raise StageError(f"레인 응답이 요청과 짝지어지지 않았다: {request.lane_id}")
        ordered.append(response)
    return ordered


# ---------------------------------------------------------------------------
# 조립
# ---------------------------------------------------------------------------


def _item_sort_key(item: dict) -> tuple:
    identifier = str(item.get("id", ""))
    match = re.fullmatch(r"M(\d+)", identifier)
    return (0, int(match.group(1))) if match else (1, identifier)


def assemble_spec(
    *,
    run_meta: dict,
    decompose: dict,
    groundings: list[dict],
    synthesis: dict,
    read_runs: tuple[str, ...],
    repo: str | None,
    source_digest: str,
) -> dict:
    """레인 산출 → 재료 명세 초안. 조립은 결정론이며 값을 만들지 않는다."""
    patent = dict((run_meta.get("patent") or {}))
    patent.pop("source_sha256", None)
    patent["source_digest"] = source_digest
    patent.setdefault("source_path", "00-source/patent.md")

    items: list[dict] = []
    items.extend(decompose.get("items") or [])
    for payload in groundings:
        items.extend(payload.get("items") or [])
    items.extend(synthesis.get("items") or [])
    items.sort(key=_item_sort_key)

    engine_block = run_meta.get("engine") or {}
    return {
        "schema": "material-spec/v0",
        "reader_version": reader_version(repo),
        "spec_version": 1,
        "status": "draft",
        "run_id": run_meta.get("run_id", ""),
        "patent": patent,
        "claims": decompose.get("claims") or {},
        "figures": synthesis.get("figures") or [],
        "items": items,
        "drop_signal": synthesis.get("drop_signal") or {},
        "provenance": {
            # 정본은 첫 실행이고 둘째는 수렴 비교 전용이다 — 그 역할을 문자열에 적어 둔다.
            "read_runs": [
                f"{read_runs[0]}:canonical",
                *[f"{name}:convergence-peer" for name in read_runs[1:]],
            ],
            "produced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "engine_commit": str(engine_block.get("commit", "")),
        },
    }


# ---------------------------------------------------------------------------
# 중간 산출물
# ---------------------------------------------------------------------------


def _tree_lines(elements: list, additions_by_target: dict, depth: int, out: list[str]) -> None:
    for element in elements or []:
        indent = "  " * depth
        out.append(
            f"{indent}- `{element.get('id')}` → **{element.get('material_id')}** — "
            f"{element.get('text_verbatim', '')}"
        )
        for addition in additions_by_target.get(element.get("id"), []):
            out.append(
                f"{indent}  - (종속 `{addition['claim']}`) `{addition['id']}` → "
                f"**{addition.get('material_id')}** — {addition.get('text_verbatim', '')}"
            )
        _tree_lines(element.get("children") or [], additions_by_target, depth + 1, out)


def write_claim_trees(paths: RunPaths, spec: dict) -> list[str]:
    """D5 ①② — 독립항별 트리 1장. 종속항 부가 한정은 부착 지점 밑에 누적한다."""
    claims = spec.get("claims") or {}
    additions_by_target: dict[str, list[dict]] = {}
    for claim in claims.get("dependents") or []:
        for addition in claim.get("additions") or []:
            entry = dict(addition)
            entry["claim"] = claim.get("id")
            additions_by_target.setdefault(addition.get("attaches_to"), []).append(entry)

    written: list[str] = []
    for claim in claims.get("independent") or []:
        claim_id = str(claim.get("id"))
        lines = [f"# 청구항 트리 — `{claim_id}`", "", f"> {claim.get('text_verbatim', '')}", ""]
        lines.append("## 골격 (독립항 element)와 누적 층위 (종속항 부가 한정)")
        lines.append("")
        body: list[str] = []
        _tree_lines(claim.get("elements") or [], additions_by_target, 0, body)
        lines.extend(body)
        lines.append("")
        dependents = [
            claim_entry
            for claim_entry in claims.get("dependents") or []
            if claim_id in (claim_entry.get("depends_on") or [])
        ]
        lines.append("## 이 청구항을 인용하는 종속항")
        lines.append("")
        if not dependents:
            lines.append("_없음._")
        for entry in dependents:
            lines.append(
                f"- `{entry.get('id')}` — `{entry.get('dependency_type')}` "
                f"(인용: {', '.join(entry.get('depends_on') or [])})"
            )
        lines.append("")
        path = paths.claim_tree(claim_id)
        write_text(path, "\n".join(lines))
        written.append(path)
    return written


def write_grounding_md(paths: RunPaths, spec: dict, convergence: dict) -> None:
    """D5 ③ — 구성요소 ↔ 명세서 문단 ↔ 도면부호."""
    lines = ["# 3중 접지 (D5 ③)", ""]
    lines.append("접지 전량이 원칙이다(재정 R3). 예외는 아래 §2 에 전량 드러난다.")
    lines.append("")
    lines.append("## 1. 접지 목록")
    lines.append("")
    for item in spec.get("items") or []:
        if item.get("kind") != "grounding":
            continue
        anchor = item.get("anchor_state") or {}
        lines.append(
            f"### **{item.get('id')}** ← 구성요소 {item.get('component')} "
            f"(명세서 `{anchor.get('spec')}` · 도면 `{anchor.get('figure')}`)"
        )
        lines.append("")
        for ref in item.get("spec_refs") or []:
            lines.append(f"- 명세서 `{ref.get('locator', '')}`: “{ref.get('quote', '')}”")
        for ref in item.get("figure_refs") or []:
            numerals = ", ".join(ref.get("numerals") or [])
            lines.append(
                f"- 도면 `{ref.get('figure')}` (도면부호 {numerals}): "
                f"“{ref.get('caption_quote', '')}”"
            )
        if item.get("search_note"):
            lines.append(f"- 탐색 기록: {item.get('search_note')}")
        lines.append("")
    lines.append("## 2. 접지 예외")
    lines.append("")
    exceptions = convergence.get("grounding_exceptions") or []
    if not exceptions:
        lines.append("_예외 없음._")
        lines.append("")
    for entry in exceptions:
        lines.append(
            f"- **{entry.get('material_id')}** (구성요소 {entry.get('component')}) — "
            f"명세서 `{entry.get('spec')}` · 도면 `{entry.get('figure')}`: "
            f"{entry.get('search_note', '')}"
        )
    lines.append("")
    write_text(paths.grounding_md, "\n".join(lines))


def write_positioning_md(paths: RunPaths, spec: dict) -> None:
    """D5 ⑤ — 배경기술·효과 대비."""
    lines = ["# 포지셔닝 (D5 ⑤)", ""]
    for item in spec.get("items") or []:
        if item.get("kind") != "positioning":
            continue
        lines.append(f"## {item.get('id')}")
        lines.append("")
        lines.append(f"- 배경 문제: {item.get('background_problem', '')}")
        lines.append(f"- 주장 효과: {item.get('asserted_effect', '')}")
        lines.append(f"- 차이: {item.get('delta', '')}")
        for quote in item.get("quotes") or []:
            lines.append(f"- 인용: “{quote}”")
        lines.append("")
    lines.append("## 출원인 관심 신호")
    lines.append("")
    interests = ((spec.get("claims") or {}).get("applicant_interest")) or []
    if not interests:
        lines.append("_등재된 신호가 없다._")
    for interest in interests:
        lines.append(
            f"- `{interest.get('claim')}` → **{interest.get('material_id')}** — "
            f"{interest.get('signal', '')}"
        )
    lines.append("")
    write_text(paths.positioning_md, "\n".join(lines))


def write_drop_signal_md(paths: RunPaths, early: dict, final: dict | None) -> None:
    """D4 2단 신호. 조기 신호만 있는 판(즉시 escalate)도 이 파일로 남는다."""
    lines = ["# drop 신호 (D4 · 2단)", ""]
    lines.append("| 단계 | 시점 | 판정 | 사유 |")
    lines.append("|---|---|---|---|")
    lines.append(
        f"| `early` | 청구항 분해 직후 | `{early.get('verdict', '')}` | {early.get('reason', '')} |"
    )
    if final is None:
        lines.append("| `final` | 포지셔닝 확정 후 | _미산출_ | 조기 신호로 중단 |")
    else:
        lines.append(
            f"| `final` | 포지셔닝 확정 후 | `{final.get('verdict', '')}` | "
            f"{final.get('reason', '')} |"
        )
    lines.append("")
    if early.get("verdict") == "drop-proposed":
        lines.append(
            "★ 조기 신호가 `drop-proposed` 이므로 나머지 단계를 돌리지 않고 즉시 escalate 했다. "
            "비용 절약이 아니라, 하류 산출물이 Owner 의 판단을 오염시키는 것을 막기 위함이다(D4)."
        )
        lines.append("")
    if final is not None and final.get("verdict") == "drop-proposed":
        lines.append(
            "★ 최종 신호가 `drop-proposed` 다. 사유 표기는 `안도감 부적합`이며, "
            "`source` 의 `형식 전제 미충족`과는 판단의 종류가 다르다(재정 N12)."
        )
        lines.append("")
    write_text(paths.drop_signal_md, "\n".join(lines))


# ---------------------------------------------------------------------------
# 실행
# ---------------------------------------------------------------------------


def _retry_budget(contract: dict) -> int:
    """계약의 `failure[].action` 에서 `retry(n)` 을 회수한다(코드에 박지 않는다)."""
    budget = 0
    for entry in contract.get("failure") or []:
        match = RETRY_PATTERN.search(str(entry.get("action", "")))
        if match:
            budget = max(budget, int(match.group("count")))
    return budget


def _execute_read_run(
    *,
    read_run: str,
    adapter,
    view: ReadView,
    profiles: dict,
    journal: LaneJournal,
    attempt: int,
    defects: list[dict] | None,
) -> dict:
    """독립 실행 1회. 조기 drop 신호면 접지 지출 **전에** 멈춘다."""
    decompose = _dispatch(
        adapter, plan_decompose(read_run, view, profiles, attempt, defects), journal
    )[0].payload
    early = decompose.get("drop_signal") or {}
    if early.get("verdict") == "drop-proposed":
        return {"early_drop": early, "decompose": decompose}

    claims = decompose.get("claims") or {}
    grounding_requests = plan_grounding(read_run, claims, view, profiles, attempt, defects)
    groundings = [
        response.payload for response in _dispatch(adapter, grounding_requests, journal)
    ]
    synthesis = _dispatch(
        adapter,
        # 접지 산출을 넘기는 이유: `figures[]` 는 synthesize 만 만들 수 있는데 그 배열에
        # 해소되어야 하는 `figure_refs` 는 접지가 만든다. 무엇이 참조되었는지 알려 주지
        # 않으면 두 레인 사이에 아무도 책임지지 않는 구간이 남는다(실특허 스모크 적발).
        plan_synthesis(read_run, claims, view, profiles, attempt, defects, groundings),
        journal,
    )[0].payload
    return {
        "early_drop": None,
        "decompose": decompose,
        "groundings": groundings,
        "synthesis": synthesis,
    }


def _validate_convergence(payload: dict, repo: str | None) -> None:
    target = os.path.join(repo or repo_root(), *CONVERGENCE_SCHEMA)
    with open(target, encoding="utf-8") as handle:
        schema = json.load(handle)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        first = errors[0]
        locus = "/".join(str(step) for step in first.absolute_path) or "$"
        raise RunnerContractError(
            f"convergence.json 이 convergence/v0 를 위반한다(@{locus}): {first.message}"
        )


def run(
    *,
    run_root: str,
    adapter,
    rules: Rules,
    read_runs: tuple[str, str] = ("read-a", "read-b"),
    repo: str | None = None,
) -> dict:
    """D5 5단계를 두 독립 실행으로 돌리고 재료 명세·중간 산출물·`convergence.json` 을 낸다.

    반환 = `{"rows", "spec", "convergence", "status", "reason_label"}`.
    """
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    paths.ensure_read_dirs()

    run_meta = load_yaml(paths.run_yaml)
    source_text = read_text(paths.patent_md)
    actual_digest = sha256_bytes(source_text.encode("utf-8"))
    recorded_digest = read_text(paths.patent_sha256).strip()
    declared_digest = str((run_meta.get("patent") or {}).get("source_sha256", ""))

    if actual_digest != recorded_digest or (
        declared_digest and declared_digest != actual_digest
    ):
        # 원천이 도중에 바뀐 런은 폐기 대상이다 — 모든 verbatim 검사의 기준점이 붕괴한다.
        # 검사 id 는 등재된 이름을 쓴다(`reader/lib/source_digest.py` · 글로사리 §2.1).
        # 그 검사는 **명세가 신고한** 기준점을 보고, 여기서는 **런의 기록**(run.yaml ·
        # patent.sha256)을 본다 — 판정은 같은 불변식 I1 이고 보는 자리가 다르다.
        entry = failure_entry(contract, "원천 다이제스트")
        row = CheckRow(check_id="read.source-digest", checked=1)
        row.add(
            "source.digest-match",
            "00-source/patent.md",
            actual_digest,
            recorded_digest or declared_digest,
            "원천 다이제스트가 기록과 다르다 — 원천이 바뀐 런은 폐기 대상이다",
        )
        return {
            "rows": [row],
            "spec": None,
            "convergence": None,
            "status": str(entry.get("action")),
            "reason_label": entry.get("reason_label"),
        }

    view = ReadView(source_text, rules)
    profiles = lane_profiles(repo)
    journal = LaneJournal()
    schema = load_schema()

    budget = _retry_budget(contract)
    attempt = 0
    defects: list[dict] | None = None
    rows: list[CheckRow] = []
    specs: dict[str, dict] = {}
    early_signals: dict[str, dict] = {}
    final_signal: dict | None = None

    try:
        while True:
            specs = {}
            for read_run in read_runs:
                outcome = _execute_read_run(
                    read_run=read_run,
                    adapter=adapter,
                    view=view,
                    profiles=profiles,
                    journal=journal,
                    attempt=attempt,
                    defects=defects,
                )
                if outcome["early_drop"]:
                    early_signals[read_run] = outcome["early_drop"]
                    _finish_lane_log(paths, journal)
                    write_drop_signal_md(paths, outcome["early_drop"], None)
                    drop_entry = failure_entry(contract, "drop-signal")
                    return {
                        "rows": [],
                        "spec": None,
                        "convergence": None,
                        "status": str(drop_entry.get("action")),
                        "reason_label": drop_entry.get("reason_label"),
                    }
                early_signals[read_run] = (outcome["decompose"].get("drop_signal") or {})
                specs[read_run] = assemble_spec(
                    run_meta=run_meta,
                    decompose=outcome["decompose"],
                    groundings=outcome["groundings"],
                    synthesis=outcome["synthesis"],
                    read_runs=read_runs,
                    repo=repo,
                    source_digest=actual_digest,
                )
                final_signal = outcome["synthesis"].get("drop_signal") or final_signal

            canonical = specs[read_runs[0]]
            peer = specs[read_runs[1]] if len(read_runs) > 1 else None
            rows = run_read_checks(
                CheckContext(
                    spec=canonical,
                    source_text=source_text,
                    rules=rules,
                    schema=schema,
                    peer_spec=peer,
                )
            )
            failing = [row for row in rows if row.status == "fail"]
            if not failing or attempt >= budget:
                break
            # 재시도는 결함 목록을 레인에 되돌려 준다 — 그러지 않으면 같은 오류를 재생산한다.
            defects = findings_of(failing)
            attempt += 1
    finally:
        _finish_lane_log(paths, journal)

    mismatched = journal.mismatched()
    if mismatched:
        raise LaneAssignmentError(
            "레인이 요청과 다른 모델·effort 로 돌았다(조용한 대체 금지): "
            + ", ".join(
                f"{row['lane_id']} 요청 {row['requested_model']}/{row['requested_effort']} "
                f"→ 실제 {row['actual_model']}/{row['actual_effort']}"
                for row in mismatched
            )
            + f" — 기록: {paths.lane_log}"
        )

    canonical = specs[read_runs[0]]
    payload = to_convergence_payload(rows, canonical)
    if payload["convergence_detail"]["executed"]:
        payload["convergence_detail"]["attempt"] = attempt + 1
    _validate_convergence(payload, paths.repo)
    write_json(paths.convergence_json, payload)

    write_drop_signal_md(paths, early_signals.get(read_runs[0], {}), final_signal)

    failing = [row for row in rows if row.status == "fail"]
    if failing:
        # C5 — 검사가 하나라도 실패하면 산출을 확정하지 않는다. 판정 보고서와 drop 신호는
        # Owner 가 판단할 자료이므로 남기되, 재료 명세와 판독본은 쓰지 않는다.
        status, reason_label = _failure_verdict(contract, failing)
        return {
            "rows": rows,
            "spec": None,
            "convergence": payload,
            "status": status,
            "reason_label": reason_label,
        }

    write_json(paths.material_spec_json, canonical)
    write_claim_trees(paths, canonical)
    write_grounding_md(paths, canonical, payload)
    write_positioning_md(paths, canonical)
    write_text(paths.material_spec_md, render(canonical, payload, contract, paths.repo))

    status = "ok"
    reason_label = None
    if (canonical.get("drop_signal") or {}).get("verdict") == "drop-proposed":
        entry = failure_entry(contract, "drop-signal")
        status = str(entry.get("action"))
        reason_label = entry.get("reason_label")
    return {
        "rows": rows,
        "spec": canonical,
        "convergence": payload,
        "status": status,
        "reason_label": reason_label,
    }


def _failure_verdict(contract: dict, failing: list[CheckRow]) -> tuple[str, str | None]:
    """검사 실패 → 조치. 재시도 예산은 이미 소진된 뒤 호출된다."""
    ids = {row.check_id for row in failing}
    if "read.schema" in ids:
        entry = failure_entry(contract, "read.schema 실패")
        return str(entry.get("then", entry.get("action"))), entry.get("reason_label")
    if "read.convergence" in ids:
        entry = failure_entry(contract, "read.convergence 미달")
        return str(entry.get("then", entry.get("action"))), entry.get("reason_label")
    entry = failure_entry(contract, "read.verbatim")
    return str(entry.get("then", entry.get("action"))), entry.get("reason_label")


def _finish_lane_log(paths: RunPaths, journal: LaneJournal) -> None:
    write_json(paths.lane_log, journal.rows)
