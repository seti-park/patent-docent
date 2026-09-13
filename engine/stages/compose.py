# -*- coding: utf-8 -*-
"""`compose` 스테이지 — 동결 재료 + 블루프린트만으로 주석층이 붙은 초안을 변주 3판에서 받는다(재정 T64 ③).

계약 = `contracts/stages/compose.yaml`(정본 서술 = SPEC §1.9). 글은 펜 레인(Opus 5 · effort 사다리
high/xhigh/max)이 쓰고, 이 러너는 **요청서 3건을 조립하고 응답을 받아 종료 검사 4를 돌린 뒤 통과한
판만 확정**한다. 러너 자신은 판단하지 않는다.

흐름.

① 진입 — 종료선(`partial_until`) · `compose.input-digest`(동결본 + 블루프린트 · 재정 P-C) ·
   **프롬프트 린트**(`compose.prompt-lint` · 템플릿 + 응답 계약 + 지시 블록 · 실패 = `StageHaltError`) ·
   `run.yaml#pens`·`comparison_axis` 기입(없으면 쓰고 있으면 계약과 대조).
② 요청 3건 — `ComposeLaneRequest`(어휘 `compose`/`v1|v2|v3`). 세 요청은 `effort`·`lane_id`·`task` 와
   지시 블록의 변주 표지 줄만 다르고 나머지는 바이트 동일하다(D10 공정 비교 · R10). 어댑터는 파일
   어댑터이며 변주마다 따로 dispatch 한다 — 한 변주의 미도착이 다른 변주의 평가를 막지 않되, **확정은
   전 변주가 해소된 뒤에만** 한다(한 판씩 확정하면 순서 효과가 생긴다).
③ 응답 소비 — 반려서면 `material-defect.md` 를 쓰고 그 변주 `reject-upstream`. 초안이면 텍스트를 받아
   ④로.
④ 검사 4(변주별) — `compose.frontmatter` → `compose.spec-digest` → `compose.annotation-syntax` →
   `compose.lane-verified`.
⑤ 처분 — 조치의 정본은 계약 `failure[]`. annotation-syntax 실패 = `retry(2)`(그 변주만 · 결함 표 동봉)
   → 소진 시 `escalate` · spec-digest·frontmatter·lane-verified 실패 = `halt` · 레인 결측(오케스트레이터가
   `missing` 으로 신고) = 토너먼트 결측 행 · 생존 변주 ≥ 1 이면 런 계속. 전 변주 해소 후
   `thread.annotated.md`(통과한 판만 · 바이트 그대로 · 끝 개행 하나만 정규화) · `compose-report.json` ·
   `tournament-rows.jsonl`(append · 변주당 1행).

★ 시트 값·슬롯 이름·검사 id·펜 배정을 여기 리터럴로 두지 않는다 — 시트·계약에서 읽는다.
`15-frozen/**`·`20-design/**` 에는 쓰지 않는다(D6 규율 ②).
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
from dataclasses import dataclass
from typing import ClassVar

import yaml

from reader.lib.report import CheckRow

from . import (
    StageError,
    StageHaltError,
    dump_yaml,
    failure_entry,
    findings_of,
    load_json,
    load_yaml,
    read_text,
    rows_to_dicts,
    sha256_file,
    verify_declared_inputs,
    write_json,
    write_text,
)
from .design import latest_frozen, law_commit_of, terminus_index
from ..annotation.parse import parse as parse_annotation
from ..lanes.contract import (
    LanePending,
    LaneRequest,
    LaneResponse,
    register_lane_vocabulary,
    render_request_body,
)
from ..lanes.file_adapter import FileLaneAdapter
from ..lanes.plan import _accepted_models
from ..paths import RunPaths, load_format_parameters, load_stage_contract, repo_root
from ..pens import lint as prompt_lint
from ..pens import registry

STAGE_ID = "compose"
LANE_RUN = "compose"
PROCEDURE_DOC = "engine/pens/prompt-template.md"
RETRY_RE = re.compile(r"^retry\((\d+)\)$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
EFFORT_EVIDENCE = "requested-flag"
OUTCOME_DRAFTED = "drafted"
OUTCOME_MISSING = "missing"
OUTCOME_DEFECT = "material-defect"
TASTE_WEIGHT = "low"                      # R10 규약 4 — 닮은 변주 간 선택은 취향 사료로 낮은 가중
DEFECT_KINDS = ("factual-error", "unresolvable-grounding", "missing-fact")
DEFECT_FIELDS = ("material_ids", "defect_kind", "evidence", "blocked_slots")
# 프런트매터 `pen` 과 대조하는 계약 배정 키(등록부가 돌려주는 4키에서 variant 를 뺀 셋).
CHECK_ORDER = ("compose.frontmatter", "compose.spec-digest", "compose.annotation-syntax", "compose.lane-verified")

# 계약에서 변주 어휘를 읽는다(리터럴 없음). 모듈 import 시점 = 계약의 시점(재정 P-U1 결박 트리).
_CONTRACT_AT_IMPORT = load_stage_contract(STAGE_ID)
VARIANTS: tuple[str, ...] = registry.variant_ids(contract=_CONTRACT_AT_IMPORT)
register_lane_vocabulary(LANE_RUN, (LANE_RUN,), VARIANTS)


@dataclass(frozen=True)
class ComposeLaneRequest(LaneRequest):
    """펜 레인 요청 — 어휘는 `compose`/`v1|v2|v3` 뿐이다(계약 `compose.yaml#lane.lane_id_vocabulary`)."""

    RUNS: ClassVar[tuple[str, ...]] = (LANE_RUN,)
    TASKS: ClassVar[tuple[str, ...]] = VARIANTS


# ---------------------------------------------------------------------------
# 응답 payload 스키마 — 초안 또는 반려서(SPEC §1.9 반려서 4필드)
# ---------------------------------------------------------------------------


def payload_schema() -> dict:
    """`oneOf` 둘 — `{thread_annotated_md}` 또는 `{material_defect}`. 자기완결(참조 없음)."""
    return {
        "type": "object",
        "title": "lane-response/compose",
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["thread_annotated_md"],
                "properties": {"thread_annotated_md": {"type": "string", "minLength": 1}},
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["material_defect"],
                "properties": {
                    "material_defect": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": list(DEFECT_FIELDS),
                        "properties": {
                            "material_ids": {
                                "type": "array",
                                "minItems": 1,
                                "items": {"type": "string", "pattern": "^M[0-9]+$"},
                            },
                            "defect_kind": {"enum": list(DEFECT_KINDS)},
                            "evidence": {"type": "string", "minLength": 1},
                            "blocked_slots": {"type": "array", "items": {"type": "integer", "minimum": 1}},
                        },
                    }
                },
            },
        ],
    }


_PAYLOAD_SCHEMA = payload_schema()
# 셋 다 **같은** 스키마 객체 — 구동기 `wrapper_schema` 가 task(변주 id)로 조회한다.
RESPONSE_SCHEMAS: dict[str, dict] = {variant: _PAYLOAD_SCHEMA for variant in VARIANTS}


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def lane_id_for(variant: str, attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_RUN}/{variant}/retry-{attempt}/batch-0"
    return f"{LANE_RUN}/{variant}/batch-0"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_terminus(meta: dict, repo: str, contract: dict) -> None:
    if meta.get("run_kind") != "partial":
        return
    until = str(meta.get("partial_until", ""))
    if terminus_index(repo, until) < terminus_index(repo, STAGE_ID):
        entry = failure_entry(contract, "partial_until 종료선")
        raise StageHaltError(
            f"[{entry.get('action')}] partial_until={until!r} 은 compose 앞의 종료선이다 — "
            f"{entry.get('note')}. 연장 봉투(extension-envelope/v0)로 종료선을 옮긴 뒤 다시 부른다"
        )


def sheet_values(repo: str) -> dict:
    """펜 지시 블록이 싣는 시트 값 — 값은 시트에서만 온다(재정 N-D11)."""
    params = load_format_parameters(repo)["parameters"]
    try:
        return {
            "tweet_count": params["tweet_count"]["value"],
            "length_by_slot": params["length_by_slot"]["value"],
            "body_char_max": params["body_char_max"]["value"],
            "body_char_min": params["body_char_min"]["value"],
            "images_per_post_max": params["images_per_post_max"]["value"],
            "slot_enum": params["slot_enum"]["value"],
        }
    except (KeyError, TypeError) as exc:
        raise StageError(f"형식 파라미터 시트에 펜이 읽는 값이 없다: {exc}") from exc


def _cell(value) -> str:
    return str("" if value is None else value).replace("|", "\\|").replace("\n", " ")


def sheet_block(sheet: dict) -> str:
    lines = ["| 항목 | 값 |", "|---|---|"]
    lines.append(f"| tweet_count | `{sheet['tweet_count']['min']}`~`{sheet['tweet_count']['max']}` |")
    lines.append(f"| body_char_min | `{sheet['body_char_min']}` (stop·pivot) |")
    lines.append(f"| body_char_max | `{sheet['body_char_max']}` |")
    lines.append(f"| images_per_post_max | `{sheet['images_per_post_max']}` |")
    lines.append(f"| slot_enum | `{', '.join(sheet['slot_enum'])}` |")
    lines.append("")
    lines.append(f"길이 단위 = `{sheet['length_by_slot'].get('unit')}` — X 가중 글자 수이며 코드포인트 수가 아니다(재정 R5).")
    lines.append("")
    lines.append("| slot | min | max | exempt |")
    lines.append("|---|---|---|---|")
    for slot, rule in (sheet["length_by_slot"].get("by_slot") or {}).items():
        lines.append(f"| {slot} | `{rule.get('min')}` | `{rule.get('max')}` | `{rule.get('exempt')}` |")
    return "\n".join(lines)


def blueprint_block(blueprint: dict) -> str:
    """블루프린트 요약 — 데이터 절(린트 대상 밖 · `lint.DATA_SUBSECTION_PREFIX` 와 제목이 맞물린다)."""
    hook = blueprint.get("hook") or {}
    lines = [
        "전문은 「원천 조각」 절의 `20-design/blueprint.json` 에 있다. 아래는 그 요약이다.",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| hook.question_en | {_cell(hook.get('question_en'))} |",
        f"| hook.thesis_en | {_cell(hook.get('thesis_en'))} |",
        f"| hook.figure | `{_cell(hook.get('figure'))}` |",
        f"| transmission_targets | `{', '.join(map(str, blueprint.get('transmission_targets') or []))}` |",
        "",
        "| T | slot | exhibit material_ids | point_en |",
        "|---|---|---|---|",
    ]
    for slot in blueprint.get("slots") or []:
        exhibit = (slot or {}).get("exhibit") or {}
        lines.append(
            f"| T{slot.get('n')} | `{slot.get('slot')}` | `{', '.join(map(str, exhibit.get('material_ids') or []))}` "
            f"| {_cell(exhibit.get('point_en'))} |"
        )
    terms = blueprint.get("new_terms") or []
    lines.append("")
    lines.append("| term_en | tweet | gloss_en |")
    lines.append("|---|---|---|")
    for term in terms:
        lines.append(f"| {_cell(term.get('term_en'))} | T{term.get('tweet')} | {_cell(term.get('gloss_en'))} |")
    if not terms:
        lines.append("| (없음) | | |")
    return "\n".join(lines)


def defect_block(defects: list[dict] | None) -> str:
    if not defects:
        return ""
    lines = [
        "## 재시도 — 직전 판의 결함",
        "",
        "아래는 결정론 검사가 낸 결함이다. 고쳐서 다시 낸다 · 다른 부분은 유지한다.",
        "",
        "| rule | locus | found | expected | message |",
        "|---|---|---|---|---|",
    ]
    for defect in defects:
        lines.append("| " + " | ".join(_cell(defect.get(key, "")) for key in ("rule", "locus", "found", "expected", "message")) + " |")
    return "\n".join(lines)


def build_instructions(*, run_id: str, pen: dict, spec_version: int, spec_digest: str, sheet: dict,
                       blueprint: dict, defects: list[dict] | None) -> str:
    """지시 블록. 세 변주에서 `variant`·`pen` 표지 줄만 다르다(시험이 대조한다)."""
    blocks = [
        "## 런 표지 — 프런트매터에 그대로 옮겨 적는다\n\n"
        "| 항목 | 값 |\n|---|---|\n"
        f"| run_id | `{run_id}` |\n"
        f"| variant | `{pen['variant']}` |\n"
        f"| pen | `{{ vendor: {pen['vendor']}, model: {pen['model']}, effort: {pen['effort']} }}` |\n"
        f"| spec_version | `{spec_version}` |\n"
        f"| spec_digest | `{spec_digest}` |\n\n"
        "너는 펜이다. 원천을 보지 않는다. 「원천 조각」 절의 동결 재료와 블루프린트만 본다.",
        "## 시트 값 (contracts/format-parameters.yaml)\n\n" + sheet_block(sheet),
        "## 블루프린트 요약 (20-design/blueprint.json)\n\n" + blueprint_block(blueprint),
        "## 재정 T64 ④ — 이번 초안의 헤더 `fig` 는 전부 `none`\n\n"
        "도면은 다음 판에서 붙는다. 모든 트윗 헤더의 `fig` 값은 `none` 이다.",
    ]
    retry = defect_block(defects)
    if retry:
        blocks.append(retry)
    return "\n\n".join(blocks) + "\n"


def build_request(*, paths: RunPaths, repo: str, meta: dict, frozen_row: dict, frozen_text: str,
                  blueprint_text: str, blueprint: dict, pen: dict, attempt: int,
                  defects: list[dict] | None) -> ComposeLaneRequest:
    version = int(frozen_row["spec_version"])
    frozen_name = os.path.relpath(paths.frozen_spec(version), paths.run_root).replace(os.sep, "/")
    blueprint_name = os.path.relpath(paths.blueprint_json, paths.run_root).replace(os.sep, "/")
    return ComposeLaneRequest(
        lane_id=lane_id_for(pen["variant"], attempt),
        read_run=LANE_RUN,
        task=pen["variant"],
        model=pen["model"],
        effort=pen["effort"],
        prompt_path=PROCEDURE_DOC,
        instructions=build_instructions(
            run_id=str(meta.get("run_id", "")), pen=pen, spec_version=version,
            spec_digest=str(frozen_row.get("spec_digest", "")), sheet=sheet_values(repo),
            blueprint=blueprint, defects=defects,
        ),
        repo_root=repo,
        slices={frozen_name: frozen_text, blueprint_name: blueprint_text},
        response_schema=RESPONSE_SCHEMAS[pen["variant"]],
        batch=0,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, pen["model"]),
    )


# ---------------------------------------------------------------------------
# ④ 검사 4
# ---------------------------------------------------------------------------


def check_frontmatter(frontmatter: dict, parse_errors: list, *, run_id: str, variant: str, pen: dict,
                      spec_version: int) -> CheckRow:
    row = CheckRow(check_id="compose.frontmatter", checked=5)
    fm_errors = [error for error in parse_errors if error.locus == "frontmatter"]
    for error in fm_errors:
        row.add(error.rule, "frontmatter", error.found, error.expected, error.message)
    if fm_errors and not frontmatter:
        return row
    if str(frontmatter.get("run_id")) != run_id:
        row.add("frontmatter.run-id", "run_id", str(frontmatter.get("run_id")), run_id, "프런트매터 run_id 가 run.yaml 과 다르다")
    if str(frontmatter.get("variant")) != variant:
        row.add("frontmatter.variant", "variant", str(frontmatter.get("variant")), variant, "프런트매터 variant 가 좌표와 다르다")
    assigned = registry.pen_assignment(pen)
    found_pen = frontmatter.get("pen")
    if not isinstance(found_pen, dict) or {k: str(v) for k, v in found_pen.items()} != assigned:
        row.add("frontmatter.pen", "pen", json.dumps(found_pen, ensure_ascii=False, sort_keys=True),
                json.dumps(assigned, ensure_ascii=False, sort_keys=True), "프런트매터 pen 이 계약 배정과 다르다(D10 — 토너먼트 기입의 원천)")
    if frontmatter.get("spec_version") != spec_version:
        row.add("frontmatter.spec-version", "spec_version", str(frontmatter.get("spec_version")), str(spec_version),
                "프런트매터 spec_version 이 최신 동결본과 다르다")
    digest = frontmatter.get("spec_digest")
    if not isinstance(digest, str) or not DIGEST_RE.match(digest):
        row.add("frontmatter.spec-digest-format", "spec_digest", str(digest), "sha256:<64hex>", "spec_digest 형식이 아니다")
    return row


def check_spec_digest(frontmatter: dict, *, spec_digest: str, frozen_path: str) -> CheckRow:
    row = CheckRow(check_id="compose.spec-digest", checked=2)
    actual = sha256_file(frozen_path)
    found = str(frontmatter.get("spec_digest", ""))
    if found != spec_digest:
        row.add("spec-digest.frontmatter", "spec_digest", found or "(없음)", spec_digest,
                "프런트매터 spec_digest 가 run.yaml 의 동결본 기록과 다르다 — 낡은 재료로 쓴 판이다(재정 N11)")
    if actual != spec_digest:
        row.add("spec-digest.frozen", "15-frozen", actual, spec_digest,
                "동결본 실측 지문이 run.yaml 기록과 다르다 — 동결 뒤 재료가 바뀐 런이다")
    return row


def check_annotation_syntax(parsed) -> CheckRow:
    row = CheckRow(check_id="compose.annotation-syntax", checked=max(parsed.sentence_count, 1))
    for error in parsed.errors:
        if error.locus == "frontmatter":
            continue      # 프런트매터 위반은 compose.frontmatter 의 몫(한 위반을 두 행에 싣지 않는다)
        row.add(error.rule, error.locus, error.found, error.expected, error.message)
    return row


def check_lane_verified(response: LaneResponse, *, pen: dict, accepted: tuple[str, ...]) -> CheckRow:
    row = CheckRow(check_id="compose.lane-verified", checked=2)
    row.extras["effort_evidence"] = EFFORT_EVIDENCE
    row.extras["observed"] = {"model": response.model, "effort": response.effort}
    if response.model not in accepted:
        row.add("lane.model", "response.model", response.model, f"{pen['model']} 수용 집합 {list(accepted)}",
                "실호출 모델이 펜 배정과 다르다 — 토너먼트 기입 자격이 없다(재정 R10)")
    if response.effort != pen["effort"]:
        row.add("lane.effort", "response.effort", response.effort, pen["effort"],
                "실호출 effort 가 펜 배정과 다르다(재정 R10 · 근거 = 요청 플래그 값)")
    return row


# ---------------------------------------------------------------------------
# ⑤ 처분
# ---------------------------------------------------------------------------


def _needle_for(check_id: str) -> str:
    return {
        "compose.annotation-syntax": "compose.annotation-syntax 실패",
        "compose.spec-digest": "compose.spec-digest 불일치",
        "compose.frontmatter": "compose.spec-digest 불일치",
        "compose.lane-verified": "compose.lane-verified 실패",
    }[check_id]


def decide(contract: dict, rows: list[CheckRow], attempt: int) -> str:
    """실패 행 → `retry` | `escalate` | `halt`. 재시도는 실패가 전부 retry 행일 때만."""
    failed = [row for row in rows if row.status == "fail"]
    entries = [failure_entry(contract, _needle_for(row.check_id)) for row in failed]
    if any(str(entry.get("action")) == "halt" for entry in entries):
        return "halt"
    budget = 0
    for entry in entries:
        match = RETRY_RE.match(str(entry.get("action")))
        if match:
            budget = max(budget, int(match.group(1)))
    if entries and all(RETRY_RE.match(str(entry.get("action"))) for entry in entries) and attempt < budget:
        return "retry"
    return "escalate"


def _normalize_draft(text: str) -> str:
    """레인 바이트 그대로 — 끝에 개행이 없으면 하나 붙인다(이것 하나만 정규화)."""
    return text if text.endswith("\n") else text + "\n"


def _write_material_defect(path: str, defect: dict) -> None:
    """반려서 — YAML 프런트매터 4필드 + 본문 evidence(SPEC §1.9 반려서 표)."""
    front = yaml.safe_dump(
        {
            "material_ids": [str(value) for value in defect.get("material_ids") or []],
            "defect_kind": defect.get("defect_kind"),
            "evidence": str(defect.get("evidence", "")),
            "blocked_slots": [int(value) for value in defect.get("blocked_slots") or []],
        },
        allow_unicode=True, sort_keys=False,
    )
    write_text(
        path,
        "---\n" + front + "---\n\n# 재료 반려서(D6 규율 ② — 펜은 재료를 고치지 않는다)\n\n"
        + str(defect.get("evidence", "")).rstrip() + "\n",
    )


def _existing_tournament_variants(path: str) -> set[str]:
    out: set[str] = set()
    if not os.path.isfile(path):
        return out
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if raw:
                try:
                    row = json.loads(raw)
                except ValueError as exc:
                    raise StageError(f"tournament-rows.jsonl 행이 JSON 이 아니다: {exc}") from exc
                if isinstance(row, dict) and row.get("variant"):
                    out.add(str(row["variant"]))
    return out


def _append_tournament_rows(path: str, rows: list[dict]) -> int:
    existing = _existing_tournament_variants(path)
    fresh = [row for row in rows if str(row.get("variant")) not in existing]
    if fresh:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as handle:
            for row in fresh:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(fresh)


def _ensure_pens_in_run_yaml(paths: RunPaths, meta: dict, pens: list[dict], axis: str) -> None:
    """`run.yaml#pens`·`comparison_axis` — 없으면 기입, 있으면 계약과 대조(다르면 StageError)."""
    recorded = meta.get("pens")
    recorded_axis = meta.get("comparison_axis")
    if recorded is None and recorded_axis is None:
        meta["pens"] = [dict(pen) for pen in pens]
        meta["comparison_axis"] = axis
        dump_yaml(paths.run_yaml, meta)
        return
    normalized = [{key: str((row or {}).get(key)) for key in registry.PEN_KEYS} for row in (recorded or [])]
    if normalized != pens or str(recorded_axis) != axis:
        raise StageError(
            f"run.yaml 의 펜 배정이 계약과 다르다 — run.yaml pens={normalized} axis={recorded_axis!r} ≠ "
            f"계약 pens={pens} axis={axis!r}. 배정은 런 개시 뒤 바뀌지 않는다(D10)"
        )


def _lint_entry(contract: dict, requests: list[ComposeLaneRequest], repo: str) -> list[CheckRow]:
    """`compose.prompt-lint` — 변주별 렌더된 요청서(원천 조각·블루프린트 요약 제외)를 린트한다."""
    rows: list[CheckRow] = []
    for request in requests:
        target = prompt_lint.lint_target(render_request_body(request, repo))
        for row in prompt_lint.lint_rows(target, repo):
            row.extras["lane_id"] = request.lane_id
            rows.append(row)
    return rows


def _result(status: str, rows: list[CheckRow], **extra) -> dict:
    out = {"status": status, "rows": rows, "pending": [], "lanes_root": None, "variants": {}, "reason_label": None}
    out.update(extra)
    return out


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


def run(*, run_root: str, repo: str | None = None, adapter=None, missing: dict | None = None) -> dict:
    """compose 스테이지 1회 진입.

    `missing` = 오케스트레이터가 신고한 결측 변주 `{variant: missing_reason}`(응답 파일 없이 호출 상한에
    닿은 좌표). 러너는 파일만 보므로 레인 사망을 스스로 알 수 없다 — 신고가 오면 토너먼트 결측 행을
    쓰고, 그 행이 있으면 이후 재진입에서도 결측으로 본다(상태의 자리 = `tournament-rows.jsonl`).

    반환 = `{status: ok|pending|escalate|halt|reject-upstream, rows, pending, lanes_root, variants, reason_label}`.
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)
    missing = dict(missing or {})

    # ① 진입
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    entry_declared = [entry for entry in contract.get("checks_on_entry") or [] if entry.get("on_mismatch") == "environment-error"]
    halt_declared = [str(entry.get("id")) for entry in contract.get("checks_on_entry") or [] if entry.get("on_mismatch") == "halt"]
    if halt_declared != [prompt_lint.CHECK_ID]:
        raise StageError(f"compose.yaml#checks_on_entry 의 halt 검사가 러너 구현과 다르다: {halt_declared}")
    entry_row = verify_declared_inputs(paths, {**contract, "checks_on_entry": entry_declared}, STAGE_ID,
                                       inputs={"spec_version": version})
    pens = registry.pens(contract=contract)
    axis = registry.comparison_axis(contract=contract)
    paths.ensure_compose_dirs([pen["variant"] for pen in pens])
    frozen_path = paths.frozen_spec(version)
    frozen_text = read_text(frozen_path)
    blueprint_text = read_text(paths.blueprint_json)
    blueprint = json.loads(blueprint_text)
    law_commit = law_commit_of(repo)
    run_id = str(meta.get("run_id", ""))
    accepted = _accepted_models(paths.contracts["read"].get("lane") or {}, pens[0]["model"])

    def request_for(pen: dict, attempt: int, defects: list[dict] | None) -> ComposeLaneRequest:
        return build_request(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, frozen_text=frozen_text,
                             blueprint_text=blueprint_text, blueprint=blueprint, pen=pen, attempt=attempt,
                             defects=defects)

    lint_rows = _lint_entry(contract, [request_for(pen, 0, None) for pen in pens], repo)
    if any(row.status == "fail" for row in lint_rows):
        entry = failure_entry(contract, "compose.prompt-lint 실패")
        write_json(paths.compose_report_json, {
            "stage": STAGE_ID, "status": "halt", "variants": {}, "rows": rows_to_dicts([entry_row, *lint_rows]),
            "findings": findings_of(lint_rows), "pens": pens, "comparison_axis": axis, "law_commit": law_commit,
        })
        first = findings_of(lint_rows)[0]
        raise StageHaltError(
            f"[{entry.get('action')}] compose.prompt-lint 실패 — {first['rule']}@{first['locus']}: {first['found']!r}. "
            f"{entry.get('note')}"
        )
    _ensure_pens_in_run_yaml(paths, meta, pens, axis)

    adapter = adapter or FileLaneAdapter(paths.compose_lanes_dir, repo)
    already_missing = _existing_tournament_variants(paths.tournament_rows_jsonl)
    per_variant_rows: dict[str, list[CheckRow]] = {}
    variants: dict[str, dict] = {}
    pending: list[str] = []
    drafts: dict[str, str] = {}
    lane_info: dict[str, dict] = {}

    # ②~⑤ 변주별 — 서로 독립(C8). 확정 쓰기는 루프 뒤.
    for pen in pens:
        variant = pen["variant"]
        attempt = 0
        defects: list[dict] | None = None
        while True:
            request = request_for(pen, attempt, defects)
            try:
                response = adapter.dispatch([request])[0]
            except LanePending as pending_exc:
                if variant in missing or (variant in already_missing and not os.path.isfile(paths.thread_annotated(variant))):
                    reason = missing.get(variant) or "결측 행 기존재(응답 없이 재진입)"
                    variants[variant] = {"status": OUTCOME_MISSING, "path": None, "digest": None,
                                         "lane_id": request.lane_id, "attempt": attempt, "missing_reason": reason}
                    break
                pending.extend(pending_exc.pending)
                variants[variant] = {"status": "pending", "path": None, "digest": None, "lane_id": request.lane_id, "attempt": attempt}
                break

            payload = response.payload
            lane_info[variant] = {"model": response.model, "effort": response.effort, "lane_id": response.lane_id,
                                  "response_digest": response.response_digest, "mismatch": response.mismatches(request)}
            defect = payload.get("material_defect")
            if isinstance(defect, dict):
                path = paths.material_defect(variant)
                _write_material_defect(path, defect)
                entry = failure_entry(contract, "재료 결함")
                variants[variant] = {"status": str(entry.get("action")), "path": path, "digest": sha256_file(path),
                                     "lane_id": request.lane_id, "attempt": attempt, "to": entry.get("to"),
                                     "defect_kind": defect.get("defect_kind")}
                break

            text = _normalize_draft(str(payload.get("thread_annotated_md", "")))
            parsed = parse_annotation(text, slot_enum=sheet_values(repo)["slot_enum"])
            rows = [
                check_frontmatter(parsed.frontmatter, parsed.errors, run_id=run_id, variant=variant, pen=pen, spec_version=version),
                check_spec_digest(parsed.frontmatter, spec_digest=spec_digest, frozen_path=frozen_path),
                check_annotation_syntax(parsed),
                check_lane_verified(response, pen=pen, accepted=accepted),
            ]
            per_variant_rows[variant] = rows
            if all(row.status == "pass" for row in rows):
                drafts[variant] = text
                variants[variant] = {"status": "ok", "path": paths.thread_annotated(variant), "digest": None,
                                     "lane_id": request.lane_id, "attempt": attempt}
                break
            action = decide(contract, rows, attempt)
            if action == "retry":
                attempt += 1
                defects = findings_of([row for row in rows if row.check_id == "compose.annotation-syntax"])
                continue
            variants[variant] = {"status": action, "path": None, "digest": None, "lane_id": request.lane_id,
                                 "attempt": attempt, "failed": [row.check_id for row in rows if row.status == "fail"]}
            break

    all_rows: list[CheckRow] = [entry_row, *lint_rows]
    for variant in (pen["variant"] for pen in pens):
        for row in per_variant_rows.get(variant, []):
            row.extras["variant"] = variant
            all_rows.append(row)

    if pending:
        return _result("pending", all_rows, pending=pending, lanes_root=paths.compose_lanes_dir, variants=variants)

    # 확정 — 전 변주 해소 뒤에만.
    tournament_rows: list[dict] = []
    for pen in pens:
        variant = pen["variant"]
        state = variants[variant]
        base = {"variant": variant, "pen": registry.pen_assignment(pen), "comparison_axis": axis,
                "taste_weight": TASTE_WEIGHT, "spec_version": version, "spec_digest": spec_digest,
                "recorded_at": _now_iso()}
        if state["status"] == "ok":
            path = paths.thread_annotated(variant)
            if not os.path.isfile(path):
                write_text(path, drafts[variant])
            state["digest"] = sha256_file(path)
            tournament_rows.append({**base, "outcome": OUTCOME_DRAFTED})
        elif state["status"] == OUTCOME_MISSING:
            tournament_rows.append({**base, "outcome": OUTCOME_MISSING, "missing_reason": state["missing_reason"]})
        elif state["status"] == "reject-upstream":
            tournament_rows.append({**base, "outcome": OUTCOME_DEFECT})
    _append_tournament_rows(paths.tournament_rows_jsonl, tournament_rows)

    statuses = [state["status"] for state in variants.values()]
    survivors = [variant for variant, state in variants.items() if state["status"] == "ok"]
    if "halt" in statuses:
        status, reason = "halt", "검사 halt(" + ", ".join(v for v, s in variants.items() if s["status"] == "halt") + ")"
    elif "reject-upstream" in statuses:
        rejected = [v for v, s in variants.items() if s["status"] == "reject-upstream"]
        status, reason = "reject-upstream", "재료 반려(→ read): " + ", ".join(str(variants[v]["path"]) for v in rejected)
    elif survivors:
        status, reason = "ok", None
        others = [f"{v}={s['status']}" for v, s in variants.items() if s["status"] != "ok"]
        if others:
            reason = "생존 " + str(len(survivors)) + " · " + ", ".join(others)
    elif "escalate" in statuses:
        status, reason = "escalate", "검사 실패(재시도 소진) — 생존 변주 0"
    else:
        entry = failure_entry(contract, "레인 사망")
        status, reason = str(entry.get("then", "halt")), "전 변주 결측 — 생존 변주 0(재정 R10)"

    report = {
        "stage": STAGE_ID, "status": status, "variants": variants, "rows": rows_to_dicts(all_rows),
        "findings": findings_of(all_rows), "extras": {f"{row.extras.get('variant', '-')}:{row.check_id}": row.extras for row in all_rows if row.extras},
        "pens": pens, "comparison_axis": axis, "lanes": lane_info, "law_commit": law_commit,
    }
    write_json(paths.compose_report_json, report)
    return _result(status, all_rows, lanes_root=paths.compose_lanes_dir, variants=variants, reason_label=reason, report=report)


__all__ = [
    "ComposeLaneRequest",
    "RESPONSE_SCHEMAS",
    "VARIANTS",
    "build_instructions",
    "build_request",
    "check_annotation_syntax",
    "check_frontmatter",
    "check_lane_verified",
    "check_spec_digest",
    "decide",
    "lane_id_for",
    "payload_schema",
    "run",
    "sheet_values",
]
