# -*- coding: utf-8 -*-
"""런 작업장 경로 계산 — SPEC §7.2 트리의 유일한 해석기.

★ 경로를 코드에 박지 않는다. 스테이지가 읽고 쓰는 산출물 경로는 전부
`contracts/stages/<id>.yaml` 의 `inputs`·`outputs`·`owner_checkpoint.confirm_file`
선언에서 읽어 온다 — 계약이 트리를 바꾸면 러너가 따라 바뀌거나, 따라가지 못하면
`PathContractError` 로 즉시 넘어진다. 조용히 옛 경로에 쓰는 경로는 없다.

여기서 코드가 들고 있는 리터럴은 **식별자**(파일 basename)뿐이며, 그 이름들의 정본은
`contracts/glossary.md` §5 산출물 경로표다. 디렉터리 구조는 계약이 정한다.

예외 2건(계약에 선언이 없어 러너가 파생시키는 경로)은 아래 주석으로 밝힌다 —
`00-source/PROVENANCE.md`(정본화 변환 기록)과 `10-read/lanes/`(레인 요청·응답·기록).
둘 다 엔진 내부 산출물이며 계약이 선언한 상위 디렉터리 안에서만 산다.
"""

from __future__ import annotations

import os
from typing import Any

import yaml

# engine/paths.py → 리포 루트
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 계약 파일 위치. 이 둘만이 러너가 아는 "리포 안의 자리"다.
_STAGE_CONTRACT_DIR = ("contracts", "stages")
_FORMAT_PARAMETERS = ("contracts", "format-parameters.yaml")
_READER_VERSION = ("reader", "READER-VERSION")

# 러너가 파생시키는 하위 이름(계약 미선언 — 위 docstring 참조).
PROVENANCE_BASENAME = "PROVENANCE.md"
LANES_DIRNAME = "lanes"
LANE_LOG_BASENAME = "lane-log.json"


class PathContractError(Exception):
    """계약이 선언하지 않은 경로를 요구했거나 선언이 모호하다."""


def repo_root() -> str:
    """리포 루트 절대경로."""
    return _REPO_ROOT


def load_stage_contract(stage_id: str, repo: str | None = None) -> dict:
    """`contracts/stages/<stage_id>.yaml` 을 읽는다."""
    target = os.path.join(repo or _REPO_ROOT, *_STAGE_CONTRACT_DIR, f"{stage_id}.yaml")
    try:
        with open(target, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise PathContractError(f"스테이지 계약이 없다: {target}") from exc
    if not isinstance(data, dict):
        raise PathContractError(f"스테이지 계약 최상위가 매핑이 아니다: {target}")
    return data


def load_format_parameters(repo: str | None = None) -> dict:
    """형식 파라미터 시트(`contracts/format-parameters.yaml`)를 읽는다."""
    target = os.path.join(repo or _REPO_ROOT, *_FORMAT_PARAMETERS)
    try:
        with open(target, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise PathContractError(f"형식 파라미터 시트가 없다: {target}") from exc
    if not isinstance(data, dict) or "parameters" not in data:
        raise PathContractError(f"형식 파라미터 시트에 parameters 블록이 없다: {target}")
    return data


def format_parameter(dotted: str, repo: str | None = None) -> Any:
    """시트의 값 1개를 점 경로로 읽는다(예: `tweet_count.value.min`).

    ★ 이 함수가 있는 이유 — 전시물 후보 하한 6 을 코드에 적지 않기 위해서다(재정 N12).
    시트 값이 바뀌면 판정이 따라 바뀌어야 하고, 그 연동은 사본으로는 보장되지 않는다.
    """
    cursor: Any = load_format_parameters(repo)["parameters"]
    trail: list[str] = []
    for key in dotted.split("."):
        trail.append(key)
        if not isinstance(cursor, dict) or key not in cursor:
            raise PathContractError(
                f"형식 파라미터 시트에 {'.'.join(trail)} 이 없다(요청 경로 {dotted})"
            )
        cursor = cursor[key]
    return cursor


def reader_version(repo: str | None = None) -> str:
    """`reader/READER-VERSION` 사본(런 산출물의 `reader_version` 이 이 값을 싣는다)."""
    target = os.path.join(repo or _REPO_ROOT, *_READER_VERSION)
    with open(target, encoding="utf-8") as handle:
        return handle.read().strip()


def _declared_paths(contract: dict) -> list[str]:
    """계약이 선언한 런 상대 경로 전량(inputs·outputs·confirm_file)."""
    out: list[str] = []
    for key in ("inputs", "outputs", "optional_outputs"):
        for entry in contract.get(key) or []:
            if isinstance(entry, str):
                out.append(entry)
    checkpoint = contract.get("owner_checkpoint") or {}
    confirm = checkpoint.get("confirm_file")
    if isinstance(confirm, str):
        out.append(confirm)
    for entry in checkpoint.get("surfaces") or []:
        if isinstance(entry, str):
            out.append(entry)
    return out


class RunPaths:
    """런 작업장(`runs/<run-id>/`)의 경로 해석기.

    모든 상대 경로는 세 스테이지 계약의 선언에서 온다. `declared()` 가 basename 으로
    선언을 조회하고, 없거나 둘 이상이면 `PathContractError` 를 던진다 — 계약과 러너가
    어긋나는 순간을 조용히 넘기지 않기 위해서다.
    """

    STAGES = ("source", "read", "freeze")

    def __init__(self, run_root: str, repo: str | None = None) -> None:
        self.run_root = os.path.abspath(run_root)
        self.repo = repo or _REPO_ROOT
        self.contracts = {
            stage: load_stage_contract(stage, self.repo) for stage in self.STAGES
        }
        declared: list[str] = []
        for contract in self.contracts.values():
            declared.extend(_declared_paths(contract))
        # 중복 선언(같은 파일이 한 스테이지의 출력이자 다른 스테이지의 입력)은 정상이다.
        self._declared = sorted(set(declared))

    # -- 계약 조회 ----------------------------------------------------------

    def declared(self, basename: str) -> str:
        """basename 으로 계약 선언 1건을 찾는다(런 상대 경로)."""
        hits = [
            entry
            for entry in self._declared
            if entry.rstrip("/").rsplit("/", 1)[-1] == basename
        ]
        if not hits:
            raise PathContractError(
                f"계약이 {basename} 을 선언하지 않았다 "
                f"(contracts/stages/{{{','.join(self.STAGES)}}}.yaml)"
            )
        if len(set(hits)) > 1:
            raise PathContractError(f"{basename} 선언이 둘 이상이다: {hits}")
        return hits[0]

    def path(self, basename: str) -> str:
        """계약 선언을 런 작업장 절대경로로 편다."""
        return self.absolute(self.declared(basename))

    def absolute(self, relative: str) -> str:
        return os.path.join(self.run_root, *relative.rstrip("/").split("/"))

    # -- 00-source ----------------------------------------------------------

    @property
    def run_yaml(self) -> str:
        return self.path("run.yaml")

    @property
    def patent_md(self) -> str:
        return self.path("patent.md")

    @property
    def patent_sha256(self) -> str:
        return self.path("patent.sha256")

    @property
    def figures_raw(self) -> str:
        return self.path("figures-raw")

    @property
    def source_report(self) -> str:
        return self.path("source-report.json")

    @property
    def source_dir(self) -> str:
        return os.path.dirname(self.patent_md)

    @property
    def provenance_md(self) -> str:
        """정본화 변환 기록. 계약 미선언 — `00-source/` 안의 러너 산출물이다."""
        return os.path.join(self.source_dir, PROVENANCE_BASENAME)

    # -- 10-read ------------------------------------------------------------

    @property
    def material_spec_json(self) -> str:
        return self.path("material-spec.json")

    @property
    def material_spec_md(self) -> str:
        return self.path("material-spec.md")

    @property
    def claim_trees(self) -> str:
        return self.path("claim-trees")

    @property
    def grounding_md(self) -> str:
        return self.path("grounding.md")

    @property
    def positioning_md(self) -> str:
        return self.path("positioning.md")

    @property
    def drop_signal_md(self) -> str:
        return self.path("drop-signal.md")

    @property
    def convergence_json(self) -> str:
        return self.path("convergence.json")

    @property
    def read_dir(self) -> str:
        return os.path.dirname(self.material_spec_json)

    @property
    def lanes_dir(self) -> str:
        """레인 요청·응답 보관소. 계약 미선언 — `10-read/` 안의 러너 산출물이다.

        레인 왕복이 파일로 남아야 런의 감사 가능성이 생긴다(어떤 프롬프트에 어떤 모델이
        무엇을 답했는가). 그것이 이 디렉터리의 유일한 존재 이유다.
        """
        return os.path.join(self.read_dir, LANES_DIRNAME)

    @property
    def lane_log(self) -> str:
        return os.path.join(self.lanes_dir, LANE_LOG_BASENAME)

    def claim_tree(self, claim_id: str) -> str:
        return os.path.join(self.claim_trees, f"{claim_id}.md")

    # -- 15-frozen ----------------------------------------------------------

    def _versioned(self, basename_pattern: str, version: int) -> str:
        """`<N>` 자리를 판 번호로 채운다. 패턴 자체는 계약이 들고 있다."""
        declared = None
        for entry in self._declared:
            tail = entry.rstrip("/").rsplit("/", 1)[-1]
            if tail == basename_pattern:
                declared = entry
                break
        if declared is None:
            raise PathContractError(f"계약이 {basename_pattern} 을 선언하지 않았다")
        return self.absolute(declared.replace("<N>", str(version)))

    def frozen_spec(self, version: int) -> str:
        return self._versioned("material-spec.v<N>.json", version)

    def approval(self, version: int) -> str:
        return self._versioned("approval-v<N>.md", version)

    @property
    def frozen_dir(self) -> str:
        return os.path.dirname(self.frozen_spec(1))

    # -- 생성 ---------------------------------------------------------------

    def ensure_source_dirs(self) -> None:
        os.makedirs(self.figures_raw, exist_ok=True)

    def ensure_read_dirs(self) -> None:
        os.makedirs(self.claim_trees, exist_ok=True)
        os.makedirs(self.lanes_dir, exist_ok=True)

    def ensure_frozen_dir(self) -> None:
        os.makedirs(self.frozen_dir, exist_ok=True)
