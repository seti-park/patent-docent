"""소견 요청: 허용된 원천과 재정된 앵커만 조립한다."""
from dataclasses import dataclass
from typing import ClassVar
import json
import os

from ..lanes.contract import LaneRequest, register_lane_vocabulary
from ..lanes.plan import _accepted_models
from ..paths import load_stage_contract
from ..pens import registry
from ..stages import read_text

LANE_RUN = "critique"
VARIANTS = registry.variant_ids(contract=load_stage_contract("compose"))
register_lane_vocabulary(LANE_RUN, (LANE_RUN,), VARIANTS)
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["memo_md"],
          "properties": {"memo_md": {"type": "string", "minLength": 1}}}
RESPONSE_SCHEMAS = {v: SCHEMA for v in VARIANTS}

@dataclass(frozen=True)
class CritiqueLaneRequest(LaneRequest):
    RUNS: ClassVar[tuple] = (LANE_RUN,)
    TASKS: ClassVar[tuple] = VARIANTS


def build_request(*, paths, repo, variant, version, anchors, attempt=0):
    contract = paths.contracts[LANE_RUN]
    lane = contract["lane"]
    files = [paths.thread_stripped_md(variant), paths.score_json(variant), paths.blueprint_json, paths.frozen_spec(version)]
    slices = {os.path.relpath(p, paths.run_root): read_text(p) for p in files}
    slices["anchors-provided.json"] = json.dumps({"provided": anchors}, ensure_ascii=False, sort_keys=True)
    retry = f"/retry-{attempt}" if attempt else ""
    return CritiqueLaneRequest(lane_id=f"{LANE_RUN}/{variant}{retry}/batch-0", read_run=LANE_RUN, task=variant,
        model=lane["model"], effort=lane["effort"], prompt_path=contract["procedure"], instructions="제공된 계기 관측을 반영하여 소견을 작성한다.",
        slices=slices, repo_root=repo, response_schema=SCHEMA, batch=0,
        accepted_models=_accepted_models(paths.contracts["read"].get("lane") or {}, lane["model"]))
