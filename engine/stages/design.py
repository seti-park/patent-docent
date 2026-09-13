# -*- coding: utf-8 -*-
"""`design` 스테이지 — 동결 재료에서 블루프린트를 만든다(재정 2026-09-13 T64 ②).

계약 = `contracts/stages/design.yaml`(정본 서술 = SPEC §1.7). 판단(훅·슬롯·표적)은 레인(LLM ·
fable-5.1 high 1판)이 하고, 이 러너는 **요청서를 조립하고 응답을 받아 검사 6종을 돌린 뒤 통과한
것만 확정**한다. 러너 자신은 판단하지 않는다.

흐름.

① 진입 — `run.yaml` 을 읽어 종료선(`partial_until`)이 `design` 앞이면 `StageHaltError`. 최신
   동결본의 진입 지문 검사(`design.input-digest` · 재정 P-C). 이미 `blueprint.json` 이 있으면
   재호출 없이 `ok`(재진입 안전 · 단 `spec_digest` 가 현재 동결본과 다르면 `StageHaltError` —
   재정 N11). `escalation.json` 이 있으면 `StageHaltError`(상신 미처분 — 사람이 본다).
② 앵커 필터 — `ledgers/anchors/anchors.jsonl` 에서 `state == "active"` 이고 `adjudicated_in` 이
   찬 행만 제공한다(재정 R12). 제공 목록은 `20-design/anchors-provided.json` 에 남는다.
③ 요청 — `DesignLaneRequest`(어휘 `design`/`blueprint`). 요청서에 동결본 전문 · 시트 값 · 헌장
   발췌 · 재정된 앵커를 인라인한다(전부 지문에 든다 · 재정 S4). 응답이 없으면 `pending`.
④ 응답 소비 — 시점 결속·스키마 대조는 어댑터 안(`load_response`). 러너 6키를 기입해 후보를 만든다.
⑤ 검사 6 — `design.schema` 가 실패면 나머지는 평가하지 않는다(연쇄 오보 방지). 그 뒤
   `design.spec-digest` → `design.anchors-adjudicated-only` → `design.targets-resolve` →
   `design.slot-count` → `design.figure-budget`.
⑥ 처분 — 조치의 정본은 계약 `failure[]` 다. `halt` 는 즉시, `retry(1)` 은 결함 블록을 실은 재시도
   요청을 쓰고 `pending`, 재시도 뒤에도 실패면 `escalate`(`escalation.json` 에 판정 행 동봉).
   레인이 `escalation` 을 채워 보내면 검사 없이 `escalate`. 전부 통과 → `blueprint.json` ·
   `blueprint.md` · `design-report.json` · `run.yaml#numeric_whitelist` 추기.

★ 시트 값(6·12·4)·슬롯 이름·검사 id·조치 어휘를 여기 리터럴로 두지 않는다 — 시트·계약에서
읽는다(단일 진원 · 재정 N-D11). `15-frozen/**` 에는 쓰지 않는다(D6 규율 ②).
"""

from __future__ import annotations

import copy
import json
import os
import re
from dataclasses import dataclass
from typing import ClassVar

from jsonschema import Draft202012Validator

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
    worst_status,
    write_json,
    write_text,
)
from ..gitpin import GitUnavailable, run_git
from ..lanes.contract import (
    LanePending,
    LaneRequest,
    LaneResponse,
    register_lane_vocabulary,
)
from ..lanes.file_adapter import FileLaneAdapter
from ..lanes.plan import _accepted_models
from ..paths import RunPaths, load_format_parameters, repo_root, run_kinds_contract
from ..render.blueprint_md import render as render_blueprint_md

STAGE_ID = "design"
LANE_RUN = "design"
LANE_TASK = "blueprint"
BLUEPRINT_SCHEMA = ("contracts", "schemas", "blueprint.schema.json")
ANCHORS_LEDGER = ("ledgers", "anchors", "anchors.jsonl")
CHARTER_DOC = ("docs", "CHARTER.md")
PROCEDURE_DOC = "engine/procedure/design.md"
CHARTER_SECTIONS = ("D1", "D2", "D3", "D11")
# 러너가 기입하는 6키 — 레인 응답 payload 스키마는 파일 스키마에서 이것을 뺀 파생물이다.
RUNNER_KEYS = ("schema", "run_id", "spec_version", "spec_digest", "lane", "law_commit")
RETRY_RE = re.compile(r"^retry\((\d+)\)$")
# 블루프린트에서 도면 ID 를 참조하는 자리(재량 ⓐ 의 해소 대상).
RESOLUTION_MANIFEST = "assets-manifest"
RESOLUTION_FROZEN = "frozen-figures"
NOTE_NO_ASSETS = "도면 자산층 부재 — 도면은 지정만(T64 ④)"
NOTE_STOP_SHAPE = "`format.stop-shape` 미가동(T64 ④)"

register_lane_vocabulary(LANE_RUN, (LANE_RUN,), (LANE_TASK,))


@dataclass(frozen=True)
class DesignLaneRequest(LaneRequest):
    """설계 레인 요청 — 어휘는 `design`/`blueprint` 뿐이다(계약 `design.yaml#lane.lane_id_vocabulary`)."""

    RUNS: ClassVar[tuple[str, ...]] = (LANE_RUN,)
    TASKS: ClassVar[tuple[str, ...]] = (LANE_TASK,)


# ---------------------------------------------------------------------------
# 스키마
# ---------------------------------------------------------------------------


def load_blueprint_schema(repo: str | None = None) -> dict:
    with open(os.path.join(repo or repo_root(), *BLUEPRINT_SCHEMA), encoding="utf-8") as handle:
        return json.load(handle)


def payload_schema(file_schema: dict) -> dict:
    """파일 스키마 − 러너 6키 = 레인 응답 `payload` 스키마(파생물 · 복사 금지).

    `allOf` 가지에는 `"type": "object"` 가 이미 명시되어 있다(CLI strict 경고 원인 · 추기 133 ⑹).
    """
    derived = copy.deepcopy(file_schema)
    derived.pop("$id", None)
    derived["title"] = "lane-response/blueprint"
    for key in RUNNER_KEYS:
        derived["properties"].pop(key, None)
    derived["required"] = [key for key in derived["required"] if key not in RUNNER_KEYS]
    return derived


RESPONSE_SCHEMAS: dict[str, dict] = {LANE_TASK: payload_schema(load_blueprint_schema())}


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def lane_id_for(attempt: int = 0) -> str:
    if attempt:
        return f"{LANE_RUN}/{LANE_TASK}/retry-{attempt}/batch-0"
    return f"{LANE_RUN}/{LANE_TASK}/batch-0"


def law_commit_of(repo: str) -> str:
    """계약을 읽은 트리의 HEAD(`git -C <repo> rev-parse HEAD`)."""
    try:
        proc = run_git(repo, ["rev-parse", "HEAD"])
    except GitUnavailable as exc:
        raise StageError(f"법 트리의 커밋을 정할 수 없다: {exc}") from exc
    if proc.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", proc.stdout.strip()):
        raise StageError(f"법 트리 {repo} 가 git 작업 트리가 아니다 — law_commit 을 기입할 수 없다")
    return proc.stdout.strip()


def terminus_index(repo: str, stage: str) -> int:
    enum = (
        ((run_kinds_contract(repo).get("kinds") or {}).get("partial") or {}).get("terminates_at_enum")
        or []
    )
    if stage not in enum:
        raise StageError(f"run-kinds.yaml#kinds.partial.terminates_at_enum 에 {stage!r} 가 없다")
    return list(enum).index(stage)


def _check_terminus(meta: dict, repo: str, contract: dict) -> None:
    """부분 런의 종료선이 `design` 앞이면 실행하지 않는다(계약 failure 7행 · T40 ③ G-12)."""
    if meta.get("run_kind") != "partial":
        return
    until = str(meta.get("partial_until", ""))
    if terminus_index(repo, until) < terminus_index(repo, STAGE_ID):
        entry = failure_entry(contract, "partial_until 종료선")
        raise StageHaltError(
            f"[{entry.get('action')}] partial_until={until!r} 은 design 앞의 종료선이다 — "
            f"{entry.get('note')}. 연장 봉투(extension-envelope/v0)로 종료선을 옮긴 뒤 다시 부른다"
        )


def latest_frozen(meta: dict) -> dict:
    rows = [row for row in meta.get("frozen") or [] if isinstance(row, dict)]
    if not rows:
        raise StageError("run.yaml#frozen[] 이 비어 있다 — 동결이 먼저다(C7)")
    return max(rows, key=lambda row: int(row.get("spec_version", 0)))


def charter_sections(repo: str, ids=CHARTER_SECTIONS) -> str:
    """헌장의 `## D<n>` 절 본문을 제목부터 다음 `## ` 직전까지 그대로 잇는다(결정론)."""
    text = read_text(os.path.join(repo, *CHARTER_DOC))
    lines = text.split("\n")
    blocks: list[str] = []
    for wanted in ids:
        start = None
        for index, line in enumerate(lines):
            if line.startswith(f"## {wanted}.") or line.startswith(f"## {wanted} "):
                start = index
                break
        if start is None:
            raise StageError(f"docs/CHARTER.md 에 `## {wanted}` 절이 없다")
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        blocks.append("\n".join(lines[start:end]).rstrip())
    return "\n\n".join(blocks)


# ---------------------------------------------------------------------------
# ② 앵커 필터(재정 R12)
# ---------------------------------------------------------------------------


def adjudicated_anchors(repo: str) -> tuple[list[dict], int]:
    """`ledgers/anchors/anchors.jsonl` 에서 재정된 앵커만 — `(제공 목록, 차단 건수)`. 원장 부재 = 빈 목록."""
    path = os.path.join(repo, *ANCHORS_LEDGER)
    if not os.path.isfile(path):
        return [], 0
    provided: list[dict] = []
    excluded = 0
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except ValueError as exc:
                raise StageError(f"앵커 원장 행이 JSON 이 아니다: {path}: {exc}") from exc
            if isinstance(row, dict) and row.get("state") == "active" and row.get("adjudicated_in"):
                provided.append(row)
            else:
                excluded += 1
    return provided, excluded


def anchors_block(provided: list[dict]) -> str:
    if not provided:
        return "재정된 앵커 0건 — 앵커 없이 설계한다."
    lines = ["| id | adjudicated_in | 내용 |", "|---|---|---|"]
    for row in provided:
        body = {key: value for key, value in row.items() if key not in ("id", "state", "adjudicated_in")}
        lines.append(
            f"| `{row.get('id')}` | `{row.get('adjudicated_in')}` | "
            f"{json.dumps(body, ensure_ascii=False, sort_keys=True)} |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ③ 요청 조립(§3.4 블록 순서 고정)
# ---------------------------------------------------------------------------


def sheet_values(repo: str) -> dict:
    params = load_format_parameters(repo)["parameters"]
    try:
        return {
            "tweet_count": params["tweet_count"]["value"],
            "slot_placement": params["slot_placement"]["value"],
            "images_per_post_max": params["images_per_post_max"]["value"],
            "slot_enum": params["slot_enum"]["value"],
        }
    except (KeyError, TypeError) as exc:
        raise StageError(f"형식 파라미터 시트에 설계가 읽는 값이 없다: {exc}") from exc


def sheet_block(sheet: dict) -> str:
    placement = sheet["slot_placement"]
    lines = ["| 항목 | 값 |", "|---|---|"]
    lines.append(f"| tweet_count.min | `{sheet['tweet_count']['min']}` |")
    lines.append(f"| tweet_count.max | `{sheet['tweet_count']['max']}` |")
    for name in ("hook", "landing", "tail"):
        rule = placement.get(name) or {}
        count = rule.get("count") or {}
        lines.append(
            f"| slot_placement.{name} | count {count.get('min')}~{count.get('max')} · position `{rule.get('position')}` |"
        )
    other = (placement.get("other") or {}).get("allowed") or []
    lines.append(f"| slot_placement.other.allowed | `{', '.join(other)}` |")
    lines.append(f"| images_per_post_max | `{sheet['images_per_post_max']}` |")
    lines.append(f"| slot_enum | `{', '.join(sheet['slot_enum'])}` |")
    return "\n".join(lines)


def defect_block(defects: list[dict] | None) -> str:
    """재시도 지시 — 직전 판정의 결함 표(`plan.py#_defect_block` 과 같은 꼴)."""
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
        cells = [
            str(defect.get(key, "")).replace("|", "\\|").replace("\n", " ")
            for key in ("rule", "locus", "found", "expected", "message")
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_instructions(
    *,
    run_id: str,
    spec_version: int,
    spec_digest: str,
    sheet: dict,
    charter: str,
    provided_anchors: list[dict],
    defects: list[dict] | None,
) -> str:
    blocks = [
        "## 런 표지\n\n"
        f"| 항목 | 값 |\n|---|---|\n| run_id | `{run_id}` |\n| spec_version | `{spec_version}` |\n"
        f"| spec_digest | `{spec_digest}` |\n\n"
        "(정보용 — 레인은 이 값을 반향하지 않는다. 러너가 기입한다.)\n\n"
        "너는 설계 레인이다. 원천을 보지 않는다. 아래 동결 재료(원천 조각 절)만 본다.",
        "## 시트 값 (contracts/format-parameters.yaml)\n\n" + sheet_block(sheet),
        "## 헌장 발췌 (docs/CHARTER.md)\n\n" + charter,
        "## 재정 T64 ④ — 도면은 지정만\n\n"
        "첫 초안은 글만 쓴다. 도면은 **지정만** 한다 — `hook.figure`·`slots[].figures`·`figure_plan` 에 "
        "동결 재료 `figures[].id`(`FIG-…`)를 적되 자산은 아직 없다. `numeric_whitelist` 는 스레드 순번 "
        "`n/N` 하나만 제안한다(재료에 없어도 허용할 수치는 그것뿐이다).",
        "## 재정된 앵커\n\n" + anchors_block(provided_anchors),
    ]
    retry = defect_block(defects)
    if retry:
        blocks.append(retry)
    return "\n\n".join(blocks) + "\n"


def build_request(
    *,
    paths: RunPaths,
    repo: str,
    meta: dict,
    frozen_row: dict,
    frozen_text: str,
    provided_anchors: list[dict],
    attempt: int,
    defects: list[dict] | None,
) -> DesignLaneRequest:
    contract = paths.contracts[STAGE_ID]
    lane = contract.get("lane") or {}
    model, effort = lane.get("model"), lane.get("effort")
    if not model or not effort:
        raise StageError("design.yaml#lane 에 model·effort 가 없다 — 레인 지정은 하드 지정이며 빈 값을 허용하지 않는다")
    version = int(frozen_row["spec_version"])
    slice_name = os.path.relpath(paths.frozen_spec(version), paths.run_root).replace(os.sep, "/")
    return DesignLaneRequest(
        lane_id=lane_id_for(attempt),
        read_run=LANE_RUN,
        task=LANE_TASK,
        model=str(model),
        effort=str(effort),
        prompt_path=PROCEDURE_DOC,
        instructions=build_instructions(
            run_id=str(meta.get("run_id", "")),
            spec_version=version,
            spec_digest=str(frozen_row.get("spec_digest", "")),
            sheet=sheet_values(repo),
            charter=charter_sections(repo),
            provided_anchors=provided_anchors,
            defects=defects,
        ),
        repo_root=repo,
        slices={slice_name: frozen_text},
        response_schema=payload_schema(load_blueprint_schema(repo)),
        batch=0,
        # 모델 신원 표기의 정본은 read.yaml#lane.model_identity 다 — design.yaml 은 그 표를 복제하지 않는다.
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, str(model)),
    )


# ---------------------------------------------------------------------------
# ⑤ 검사 6
# ---------------------------------------------------------------------------


def check_schema(candidate: dict, schema: dict) -> CheckRow:
    row = CheckRow(check_id="design.schema", checked=1)
    for error in sorted(Draft202012Validator(schema).iter_errors(candidate), key=lambda err: list(err.absolute_path)):
        locus = "/".join(str(step) for step in error.absolute_path) or "$"
        row.add("design.schema", locus, repr(error.instance)[:120], "blueprint/v0", f"스키마 위반: {error.message}")
    return row


def check_spec_digest(candidate: dict, *, spec_version: int, spec_digest: str, frozen_path: str) -> CheckRow:
    row = CheckRow(check_id="design.spec-digest", checked=2)
    if candidate.get("spec_version") != spec_version:
        row.add("design.spec-digest", "spec_version", str(candidate.get("spec_version")), str(spec_version),
                "블루프린트가 선 재료 버전이 현재 동결본과 다르다(재정 N11)")
    actual = sha256_file(frozen_path)
    if candidate.get("spec_digest") != spec_digest or actual != spec_digest:
        row.add("design.spec-digest", "spec_digest", str(candidate.get("spec_digest")), actual,
                "블루프린트의 spec_digest 가 현재 동결본 실측과 다르다 — 재료 개정으로 무효화된 블루프린트다(재정 N11)")
    return row


def check_anchors_adjudicated_only(provided_path: str) -> CheckRow:
    """제공 목록 파일 ↔ 규칙(`state == active` 그리고 `adjudicated_in` 참). 제공 0건은 정직한 공허다."""
    row = CheckRow(check_id="design.anchors-adjudicated-only", checked=0)
    provided = (load_json(provided_path) or {}).get("provided") if os.path.isfile(provided_path) else []
    for index, anchor in enumerate(provided or []):
        row.checked += 1
        locus = f"anchors-provided.json#provided[{index}]"
        if not isinstance(anchor, dict):
            row.add("design.anchors-adjudicated-only", locus, repr(anchor)[:80], "객체", "앵커 행이 객체가 아니다")
            continue
        if anchor.get("state") != "active":
            row.add("design.anchors-adjudicated-only", locus, str(anchor.get("state")), "active",
                    "미재정 앵커가 생성계에 닿았다 — 환류 가드가 깨진 런이다(재정 R12)")
        if not anchor.get("adjudicated_in"):
            row.add("design.anchors-adjudicated-only", locus, "(adjudicated_in 비어 있음)", "재정 파일 ID",
                    "누가 언제 재정했는가를 답할 수 없는 앵커는 재정된 것이 아니다(재정 R12)")
    return row


def check_targets_resolve(candidate: dict, frozen: dict) -> CheckRow:
    """재량 ⓑ — `transmission_targets[]` 와 `slots[].exhibit.material_ids[]` 를 같은 행에서, 좌표를 갈라 본다."""
    row = CheckRow(check_id="design.targets-resolve", checked=0)
    status_of = {str(item.get("id")): str(item.get("status")) for item in frozen.get("items") or [] if isinstance(item, dict)}

    def resolve(locus: str, material_id) -> None:
        row.checked += 1
        status = status_of.get(str(material_id))
        if status is None:
            row.add("targets.unresolved", locus, str(material_id), "동결본 items[].id",
                    "동결본에 없는 재료 ID 다(유령)")
        elif status != "active":
            row.add("targets.retracted-or-superseded", locus, f"{material_id} (status {status})", "status active",
                    "retracted/superseded 항목을 지목했다 — 개정본 기준으로 재작성한다")

    for index, target in enumerate(candidate.get("transmission_targets") or []):
        resolve(f"transmission_targets[{index}]", target)
    for slot in candidate.get("slots") or []:
        for index, material_id in enumerate(((slot or {}).get("exhibit") or {}).get("material_ids") or []):
            resolve(f"slots[{slot.get('n')}].exhibit.material_ids[{index}]", material_id)
    return row


def check_slot_count(candidate: dict, sheet: dict) -> CheckRow:
    """시트의 `tweet_count`·`slot_placement`·`slot_enum` 으로 판정한다(값은 시트에서만 온다)."""
    row = CheckRow(check_id="design.slot-count", checked=0)
    slots = [slot for slot in candidate.get("slots") or [] if isinstance(slot, dict)]
    row.checked = len(slots)
    low, high = sheet["tweet_count"]["min"], sheet["tweet_count"]["max"]
    if not (low <= len(slots) <= high):
        row.add("slot.count-range", "slots", str(len(slots)), f"{low}~{high}",
                "트윗 수가 시트의 tweet_count 범위 밖이다")
    numbers = [slot.get("n") for slot in slots]
    if numbers != list(range(1, len(slots) + 1)):
        row.add("slot.n-contiguous", "slots[].n", str(numbers), f"1..{len(slots)} 연속",
                "슬롯 순번이 1부터 연속이 아니다")
    enum = list(sheet["slot_enum"])
    for slot in slots:
        if slot.get("slot") not in enum:
            row.add("slot.enum", f"slots[{slot.get('n')}].slot", str(slot.get("slot")), f"{enum}",
                    "슬롯 이름이 시트의 slot_enum 밖이다")
    placement = sheet["slot_placement"]
    named = [name for name in placement if name != "other"]
    last_n = len(slots)
    for name in named:
        rule = placement.get(name) or {}
        count = rule.get("count") or {}
        hits = [slot for slot in slots if slot.get("slot") == name]
        if not (count.get("min", 0) <= len(hits) <= count.get("max", len(slots))):
            row.add(f"slot.{name}-count", "slots", str(len(hits)), f"{count.get('min')}~{count.get('max')}",
                    f"`{name}` 슬롯 개수가 시트의 slot_placement 밖이다")
        position = rule.get("position")
        for slot in hits:
            if position == "first" and slot.get("n") != 1:
                row.add(f"slot.{name}-position", f"slots[{slot.get('n')}]", f"T{slot.get('n')}", "T1",
                        f"`{name}` 은 T1 위치여야 한다")
            if position == "last" and slot.get("n") != last_n:
                row.add(f"slot.{name}-position", f"slots[{slot.get('n')}]", f"T{slot.get('n')}", f"T{last_n}",
                        f"`{name}` 은 마지막 트윗이어야 한다")
    allowed = list((placement.get("other") or {}).get("allowed") or [])
    for slot in slots:
        if slot.get("slot") in named:
            continue
        if slot.get("slot") not in allowed:
            row.add("slot.other-allowed", f"slots[{slot.get('n')}].slot", str(slot.get("slot")), f"{allowed}",
                    "hook·landing·tail 밖의 트윗은 시트의 other.allowed 값이어야 한다")
    return row


def manifest_figure_ids(manifest) -> set[str]:
    """`30-figures/assets/manifest.json` 이 드는 도면 ID 집합(항목의 `id`, 없으면 `figure_id`)."""
    entries = manifest
    if isinstance(manifest, dict):
        entries = manifest.get("items") or manifest.get("figures") or manifest.get("assets") or []
    out: set[str] = set()
    for entry in entries or []:
        if isinstance(entry, dict):
            value = entry.get("id") or entry.get("figure_id") or entry.get("figure")
            if isinstance(value, str):
                out.add(value)
        elif isinstance(entry, str):
            out.add(entry)
    return out


def check_figure_budget(candidate: dict, frozen: dict, sheet: dict, *, manifest_path: str) -> CheckRow:
    """재량 ⓐ — 매니페스트가 있으면 그 파일에, 없으면 동결본 `figures[].id` 에 해소한다."""
    row = CheckRow(check_id="design.figure-budget", checked=0)
    if os.path.isfile(manifest_path):
        known = manifest_figure_ids(load_json(manifest_path))
        row.extras["resolution_source"] = RESOLUTION_MANIFEST
    else:
        known = {str(figure.get("id")) for figure in frozen.get("figures") or [] if isinstance(figure, dict)}
        row.extras["resolution_source"] = RESOLUTION_FROZEN
    limit = int(sheet["images_per_post_max"])

    def resolve(locus: str, figure_id) -> None:
        row.checked += 1
        if str(figure_id) not in known:
            row.add("figure.unresolved", locus, str(figure_id), f"{row.extras['resolution_source']} 의 도면 ID",
                    "지정한 도면이 해소되지 않는다(유령 도면)")

    hook_figure = (candidate.get("hook") or {}).get("figure")
    resolve("hook.figure", hook_figure)
    slot_figures: dict = {}
    for slot in candidate.get("slots") or []:
        n = slot.get("n")
        figures = list(slot.get("figures") or [])
        slot_figures[n] = set(map(str, figures))
        for index, figure_id in enumerate(figures):
            resolve(f"slots[{n}].figures[{index}]", figure_id)
        if len(figures) > limit:
            row.add("figure.per-tweet-max", f"slots[{n}].figures", str(len(figures)), f"≤ {limit}",
                    "트윗별 도면 수가 시트의 images_per_post_max 를 넘는다")
    plan_figures: dict = {}
    for plan in candidate.get("figure_plan") or []:
        tweet = plan.get("tweet")
        figures = list(plan.get("figures") or [])
        plan_figures[tweet] = set(map(str, figures))
        for index, figure_id in enumerate(figures):
            resolve(f"figure_plan[{tweet}].figures[{index}]", figure_id)
        if len(figures) > limit:
            row.add("figure.per-tweet-max", f"figure_plan[{tweet}].figures", str(len(figures)), f"≤ {limit}",
                    "트윗별 도면 수가 시트의 images_per_post_max 를 넘는다")
    if set(plan_figures) != set(slot_figures):
        row.add("figure.plan-tweet-set", "figure_plan[].tweet", str(sorted(plan_figures, key=str)),
                str(sorted(slot_figures, key=str)), "figure_plan 의 트윗 집합이 slots[].n 집합과 다르다")
    for tweet in sorted(set(plan_figures) & set(slot_figures), key=str):
        if plan_figures[tweet] != slot_figures[tweet]:
            row.add("figure.plan-slot-parity", f"figure_plan[{tweet}].figures", str(sorted(plan_figures[tweet])),
                    str(sorted(slot_figures[tweet])), "같은 트윗의 도면 집합이 slots 와 figure_plan 에서 다르다")
    if hook_figure is not None and str(hook_figure) not in slot_figures.get(1, set()):
        row.add("figure.hook-in-t1", "hook.figure", str(hook_figure), "slots[n=1].figures 의 원소",
                "훅 도면이 T1 슬롯의 도면 목록에 없다")
    return row


def run_checks(
    candidate: dict,
    *,
    schema: dict,
    frozen: dict,
    frozen_path: str,
    spec_version: int,
    spec_digest: str,
    sheet: dict,
    provided_path: str,
    manifest_path: str,
) -> list[CheckRow]:
    schema_row = check_schema(candidate, schema)
    if schema_row.status == "fail":
        return [schema_row]
    return [
        schema_row,
        check_spec_digest(candidate, spec_version=spec_version, spec_digest=spec_digest, frozen_path=frozen_path),
        check_anchors_adjudicated_only(provided_path),
        check_targets_resolve(candidate, frozen),
        check_slot_count(candidate, sheet),
        check_figure_budget(candidate, frozen, sheet, manifest_path=manifest_path),
    ]


# ---------------------------------------------------------------------------
# ⑥ 처분
# ---------------------------------------------------------------------------


def _needle_for(row: CheckRow) -> str:
    if row.check_id == "design.spec-digest":
        return "spec_version·spec_digest 불일치"
    if row.check_id == "design.anchors-adjudicated-only":
        return "design.anchors-adjudicated-only 실패"
    if row.check_id == "design.figure-budget":
        return "design.figure-budget 실패"
    if row.check_id == "design.targets-resolve" and any(
        finding.rule == "targets.retracted-or-superseded" for finding in row.findings
    ):
        return "retracted/superseded"
    return "스키마·슬롯·표적 해소 실패"


def decide(contract: dict, rows: list[CheckRow], attempt: int) -> tuple[str, int]:
    """실패 행 → 계약 조치. 반환 = (`retry` | `escalate` | `halt`, 재시도 예산)."""
    entries = [failure_entry(contract, _needle_for(row)) for row in rows if row.status == "fail"]
    terminal: list[str] = []
    budget = 0
    for entry in entries:
        action = str(entry.get("action"))
        match = RETRY_RE.match(action)
        if match:
            budget = max(budget, int(match.group(1)))
            terminal.append(str(entry.get("then", "escalate")))
        else:
            terminal.append(action)
    worst = worst_status(terminal)
    if worst == "halt":
        return "halt", budget
    if all(RETRY_RE.match(str(entry.get("action"))) for entry in entries) and attempt < budget:
        return "retry", budget
    return "escalate", budget


def _assemble(payload: dict, *, meta: dict, frozen_row: dict, response: LaneResponse, law_commit: str) -> dict:
    candidate = dict(payload)
    candidate["schema"] = "blueprint/v0"
    candidate["run_id"] = str(meta.get("run_id", ""))
    candidate["spec_version"] = int(frozen_row["spec_version"])
    candidate["spec_digest"] = str(frozen_row.get("spec_digest", ""))
    candidate["lane"] = {"model": response.model, "effort": response.effort, "lane_id": response.lane_id}
    candidate["law_commit"] = law_commit
    return candidate


def _append_whitelist(paths: RunPaths, entries: list[dict]) -> int:
    """`run.yaml#numeric_whitelist` 에 4키 행을 추기한다(pattern 중복은 건너뜀 · SPEC §7.3 서식)."""
    meta = load_yaml(paths.run_yaml)
    existing = meta.get("numeric_whitelist")
    if not isinstance(existing, list):
        existing = []
    known = {str(row.get("pattern")) for row in existing if isinstance(row, dict)}
    added = 0
    for entry in entries:
        pattern = str(entry.get("pattern", ""))
        if not pattern or pattern in known:
            continue
        existing.append(
            {
                "pattern": pattern,
                "rationale": str(entry.get("rationale", "")),
                "added_by": "run-discretion",
                "approved_in": None,
            }
        )
        known.add(pattern)
        added += 1
    if added:
        meta["numeric_whitelist"] = existing
        dump_yaml(paths.run_yaml, meta)
    return added


def _result(status: str, rows: list[CheckRow], **extra) -> dict:
    out = {
        "status": status,
        "rows": rows,
        "pending": [],
        "lanes_root": None,
        "path": None,
        "digest": None,
        "reason_label": None,
    }
    out.update(extra)
    return out


def _write_escalation(paths: RunPaths, *, reason: str, note_kr: str, overflow_proposal, payload: dict,
                      lane_id: str, rows: list[CheckRow]) -> None:
    write_json(
        paths.design_escalation_json,
        {
            "reason": reason,
            "note_kr": note_kr,
            "overflow_proposal": overflow_proposal,
            "payload": payload,
            "lane_id": lane_id,
            "rows": rows_to_dicts(rows),
            "findings": findings_of(rows),
        },
    )


def run(*, run_root: str, repo: str | None = None, adapter=None) -> dict:
    """설계 스테이지 1회 진입. 반환 = `{status: ok|pending|escalate|halt, rows, pending, lanes_root, path, digest, reason_label}`."""
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)

    # ① 진입
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID, inputs={"spec_version": version})
    paths.ensure_design_dirs()
    frozen_path = paths.frozen_spec(version)
    if os.path.isfile(paths.design_escalation_json):
        raise StageHaltError(
            f"상신 미처분 — {paths.design_escalation_json} 이 있다. 사람이 본 뒤 파일을 처분해야 다시 돈다"
        )
    if os.path.isfile(paths.blueprint_json):
        existing = load_json(paths.blueprint_json)
        if existing.get("spec_version") != version or existing.get("spec_digest") != spec_digest:
            raise StageHaltError(
                f"[halt] 기존 블루프린트가 선 재료(v{existing.get('spec_version')} · {existing.get('spec_digest')})가 "
                f"현재 동결본(v{version} · {spec_digest})과 다르다 — 재료 개정으로 무효화된 블루프린트다(재정 N11)"
            )
        report = load_json(paths.design_report_json) if os.path.isfile(paths.design_report_json) else {}
        return _result(
            "ok", [entry_row], path=paths.blueprint_json, digest=sha256_file(paths.blueprint_json),
            lanes_root=paths.design_lanes_dir, report=report,
        )

    frozen = load_json(frozen_path)
    frozen_text = read_text(frozen_path)
    sheet = sheet_values(repo)
    schema = load_blueprint_schema(repo)
    law_commit = law_commit_of(repo)

    # ② 앵커 필터
    provided, excluded = adjudicated_anchors(repo)
    write_json(paths.anchors_provided_json, {"provided": provided, "excluded_count": excluded})

    adapter = adapter or FileLaneAdapter(paths.design_lanes_dir, repo)
    attempt = 0
    defects: list[dict] | None = None
    while True:
        # ③ 요청
        request = build_request(
            paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, frozen_text=frozen_text,
            provided_anchors=provided, attempt=attempt, defects=defects,
        )
        try:
            response = adapter.dispatch([request])[0]
        except LanePending as pending:
            return _result("pending", [entry_row], pending=list(pending.pending), lanes_root=pending.request_dir)

        # ④ 응답 소비 — 조용한 대체는 보고에 남긴다(규율 ②).
        mismatch = response.mismatches(request)
        payload = response.payload
        escalation = payload.get("escalation")
        if isinstance(escalation, dict):
            # 레인의 상신 — 검사 없이 Owner 에게 간다(hook-not-feasible · exhibit-overflow).
            _write_escalation(
                paths, reason=str(escalation.get("reason")), note_kr=str(escalation.get("note_kr", "")),
                overflow_proposal=payload.get("overflow_proposal"), payload=payload, lane_id=request.lane_id, rows=[],
            )
            needle = "tweet_count.max" if escalation.get("reason") == "exhibit-overflow" else "훅이 서지 않음"
            entry = failure_entry(contract, needle)
            return _result(str(entry.get("action")), [entry_row], reason_label=str(escalation.get("reason")),
                           lanes_root=paths.design_lanes_dir)

        candidate = _assemble(payload, meta=meta, frozen_row=frozen_row, response=response, law_commit=law_commit)

        # ⑤ 검사 6
        rows = run_checks(
            candidate, schema=schema, frozen=frozen, frozen_path=frozen_path, spec_version=version,
            spec_digest=spec_digest, sheet=sheet, provided_path=paths.anchors_provided_json,
            manifest_path=paths.figures_manifest_json,
        )
        all_rows = [entry_row, *rows]
        if all(row.status == "pass" for row in rows):
            break

        # ⑥ 처분
        action, _budget = decide(contract, rows, attempt)
        if action == "retry":
            attempt += 1
            defects = findings_of(rows)
            continue
        if action == "halt":
            write_json(paths.design_report_json, _report("halt", all_rows, request.lane_id, law_commit, response, mismatch))
            return _result("halt", all_rows, lanes_root=paths.design_lanes_dir, reason_label="검사 halt")
        _write_escalation(
            paths, reason="checks-failed-after-retry", note_kr="재시도 뒤에도 검사가 실패했다 — Owner 가 본다",
            overflow_proposal=None, payload=payload, lane_id=request.lane_id, rows=rows,
        )
        write_json(paths.design_report_json, _report("escalate", all_rows, request.lane_id, law_commit, response, mismatch))
        return _result("escalate", all_rows, lanes_root=paths.design_lanes_dir, reason_label="검사 실패(재시도 소진)")

    # 확정 — blueprint.json · blueprint.md · design-report.json · run.yaml 추기. 15-frozen/ 에는 쓰지 않는다.
    notes = [NOTE_STOP_SHAPE]
    figure_row = next((row for row in rows if row.check_id == "design.figure-budget"), None)
    if figure_row is not None and figure_row.extras.get("resolution_source") == RESOLUTION_FROZEN:
        notes.insert(0, NOTE_NO_ASSETS)
    write_json(paths.blueprint_json, candidate)
    write_text(paths.blueprint_md, render_blueprint_md(candidate, frozen, rows_to_dicts(all_rows), notes=notes))
    report = _report("ok", all_rows, request.lane_id, law_commit, response, mismatch)
    report["notes"] = notes
    write_json(paths.design_report_json, report)
    _append_whitelist(paths, list(candidate.get("numeric_whitelist") or []))
    return _result(
        "ok", all_rows, path=paths.blueprint_json, digest=sha256_file(paths.blueprint_json),
        lanes_root=paths.design_lanes_dir, report=report,
    )


def _report(status: str, rows: list[CheckRow], lane_id: str, law_commit: str, response: LaneResponse, mismatch: bool) -> dict:
    return {
        "stage": STAGE_ID,
        "status": status,
        "rows": rows_to_dicts(rows),
        "findings": findings_of(rows),
        "extras": {row.check_id: row.extras for row in rows if row.extras},
        "lane_id": lane_id,
        "law_commit": law_commit,
        "lane": {
            "model": response.model,
            "effort": response.effort,
            "lane_id": response.lane_id,
            "response_digest": response.response_digest,
            "mismatch": mismatch,
        },
    }


__all__ = [
    "DesignLaneRequest",
    "RESPONSE_SCHEMAS",
    "adjudicated_anchors",
    "build_request",
    "charter_sections",
    "check_anchors_adjudicated_only",
    "check_figure_budget",
    "check_schema",
    "check_slot_count",
    "check_spec_digest",
    "check_targets_resolve",
    "decide",
    "lane_id_for",
    "law_commit_of",
    "load_blueprint_schema",
    "payload_schema",
    "run",
    "run_checks",
]
