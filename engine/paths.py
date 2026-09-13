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

from .gitpin import GitUnavailable, git_common_dir, worktree_of

# engine/paths.py → 리포 루트
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 계약 파일 위치. 이 둘만이 러너가 아는 "리포 안의 자리"다.
_STAGE_CONTRACT_DIR = ("contracts", "stages")
_FORMAT_PARAMETERS = ("contracts", "format-parameters.yaml")
_RUN_KINDS = ("contracts", "run-kinds.yaml")
_READER_VERSION = ("reader", "READER-VERSION")

# 러너가 파생시키는 하위 이름(계약 미선언 — 위 docstring 참조).
PROVENANCE_BASENAME = "PROVENANCE.md"
LANES_DIRNAME = "lanes"
LANE_LOG_BASENAME = "lane-log.json"
SHADOW_POINTER_BASENAME = "shadow-ledger.json"

# 섀도 원장의 리포 상대 자리(재정 P-U4). 루트가 어디인가는 아래 `shadow_ledger_root` 가 정한다.
SHADOW_LEDGER_RELATIVE = ("ledgers", "shadow", "screening.jsonl")

# `shadow_ledger_root` 가 돌려주는 판정 사유. 산출(포인터 파일)에 그대로 실린다 —
# "어느 원장에 썼는가"만 남기고 "왜 거기인가"를 빼면 다음 사람이 같은 조사를 처음부터 한다.
SHADOW_ROOT_EXPLICIT = "explicit"                 # 호출자가 명시 지정했다
SHADOW_ROOT_MAIN = "main-worktree"                # 여기가 주 작업 트리다
SHADOW_ROOT_RESOLVED = "main-worktree-resolved"   # 여기는 worktree, 주 작업 트리를 찾아 옮겼다
SHADOW_ROOT_NO_GIT = "git-unavailable"            # git 판정을 할 수 없었다(아래 주석)


class PathContractError(Exception):
    """계약이 선언하지 않은 경로를 요구했거나 선언이 모호하다."""


class ShadowLedgerRootError(Exception):
    """섀도 원장의 누적 루트를 판정할 수 없다(재정 P-U4 · P-U1).

    조용히 넘어갈 자리가 아니다. 여기서 아무 자리나 고르면 원장은 **아무 데도 도착하지 않은
    채** 런과 함께 사라진다 — 2026-08-18 통주 2 에서 실제로 일어난 일이며(worktree 안 4행,
    리포 0행) 그때 잃은 것은 행 수가 아니라 축적물 자체다. 없는 장부는 고칠 것이 없다.
    """


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


def run_kinds_contract(repo: str | None = None) -> dict:
    """런 종류 계약(`contracts/run-kinds.yaml`)을 결박된 리포에서 읽는다."""
    target = os.path.join(repo or _REPO_ROOT, *_RUN_KINDS)
    try:
        with open(target, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise PathContractError(f"런 종류 계약이 없다: {target}") from exc
    if not isinstance(data, dict) or "run_kind_enum" not in data:
        raise PathContractError(f"런 종류 계약에 run_kind_enum 이 없다: {target}")
    return data


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
    # 단계 진입 게이트가 선언한 경로(재정 P-U3). `continue_envelope` 는 여기에만 선언되므로
    # 이 수집이 없으면 계약이 부른 파일을 러너가 해소하지 못한다 — 그때 코드가 경로를
    # 지어내는 유혹이 생기고, 그 유혹을 막는 것이 이 모듈의 존재 이유다.
    for gate in contract.get("phase_gates") or []:
        if not isinstance(gate, dict):
            continue
        for key in ("declared_input", "continue_envelope"):
            value = gate.get(key)
            if isinstance(value, str):
                out.append(value)
    return out


def shadow_ledger_root(
    repo: str | None = None, shadow_root: str | None = None
) -> tuple[str, str]:
    """섀도 원장이 누적되는 루트와 그 **판정 사유** — `(root, source)`.

    ★ 층이 둘이다. `repo` 는 **계약 트리의 루트**(이 런의 법이 어디서 오는가)이고 `shadow_root`
    는 **원장의 루트**(축적물이 어디에 쌓이는가)다. 구 판은 `shadow_root or repo or _REPO_ROOT`
    라는 폴백으로 그 둘을 다시 합쳤고, 그래서 재정 P-U1 의 커밋 결박(런은 `.worktrees/<run-id>`
    에서 돈다)과 만나는 순간 원장이 **worktree 안에** 섰다. worktree 는 `.gitignore` 대상이고
    소모품이므로, 2026-08-18 통주 2 의 메모 4행은 리포에 **한 행도** 도착하지 않았다. 법은
    worktree 에서 오고 축적은 리포에 남는다 — 그 귀결을 여기서 집행한다.

    판정 순서와 사유.

    | 순서 | 조건 | `source` | 루트 |
    |---|---|---|---|
    | ① | `shadow_root` 가 있다 | `explicit` | 그 값 |
    | ② | 여기가 주 작업 트리다 | `main-worktree` | `repo`(또는 `_REPO_ROOT`) |
    | ③ | 여기가 링크된 worktree 다 | `main-worktree-resolved` | **주 작업 트리** |
    | ④ | git 판정 자체가 불가능하다 | `git-unavailable` | `repo`(또는 `_REPO_ROOT`) |
    | — | worktree 인데 주 작업 트리를 못 찾는다 | — | `ShadowLedgerRootError` |

    ★ ②③의 판정(`여기가 worktree 인가`)은 **반드시** `engine/gitpin.py` 를 거친다 — 런 결박
    판정의 단일 진원이며(재정 P-U1·P-8), 두 벌째 판정이 생기면 그날 도구와 러너가 같은 런을
    다르게 읽는다. 여기서 gitpin 밖으로 나가는 것은 판정이 아니라 **자리 계산** 한 줄뿐이고
    (공용 git 디렉터리의 부모 = 주 작업 트리) 그 최종 자리는 `gitpin.main_worktree_of()` 다 —
    이관은 gitpin 소관 레인의 몫으로 남긴다.

    ★ ④를 거부가 아니라 진행으로 둔 이유: git 이 없으면 링크된 worktree 라는 것 자체가 성립할
    수 없다(worktree 는 git 의 구조물이다). 그러나 "판정하지 못했다"는 사실은 삼키지 않고
    `source` 로 돌려주며, 러너는 그것을 산출(`10-read/lanes/shadow-ledger.json`)에 적는다.
    반대로 **worktree 임을 알면서 주 트리를 못 찾는** 경우는 거부한다 — 그 자리에서 진행하면
    아는 채로 사라지는 장부를 만드는 것이다.

    ★ `shadow_root` 의 지위(2026-08-19 정정). 이것은 "테스트 하네스 전용 주입구"가 아니라
    **원장 누적 루트의 명시 지정**이며, 테스트 격리(재정 G6·P-U2 — 합성 픽스처의 메모가 생산
    원장을 오염시키면 D4 훈련 데이터가 죽는다)는 그 지정의 **한 사용자**일 뿐이다. 환경 변수
    같은 암묵 경로를 두지 않는 이유는 이 리포의 규율 그대로다 — 경로는 인자로 드러나야 한다.
    """
    if shadow_root:
        return os.path.realpath(shadow_root), SHADOW_ROOT_EXPLICIT
    base = os.path.realpath(repo or _REPO_ROOT)
    try:
        worktree = worktree_of(base)
    except GitUnavailable:
        return base, SHADOW_ROOT_NO_GIT
    if worktree is None:
        return base, SHADOW_ROOT_MAIN
    common = git_common_dir(base)
    main_root = os.path.dirname(common) if os.path.basename(common) == ".git" else None
    if not main_root or not os.path.isdir(main_root):
        raise ShadowLedgerRootError(
            f"여기는 격리 체크아웃({worktree})인데 주 작업 트리를 찾지 못했다 — "
            f"공용 git 디렉터리 {common}. 원장은 worktree 와 함께 사라지므로 여기에 쓰지 "
            "않는다. 처분: 누적 루트를 명시 지정하라(shadow_root)"
        )
    return os.path.realpath(main_root), SHADOW_ROOT_RESOLVED


def shadow_screening_ledger(repo: str | None = None, shadow_root: str | None = None) -> str:
    """맹검 스크리닝 메모의 섀도 원장 — `<누적 루트>/ledgers/shadow/screening.jsonl`.

    ★ 런 **밖**이다(재정 P-U4). 메모는 재료 명세 계약면 밖의 관찰 기록이며, 한 런의 산출이
    아니라 여러 런에 걸쳐 쌓이는 축적물(historian 스크리닝의 사전 훈련 데이터 — 헌장 D4)이다.
    그래서 `RunPaths` 의 프로퍼티가 아니라 리포 수준의 모듈 함수로 노출한다.

    누적 루트의 판정은 `shadow_ledger_root` 하나가 한다 — 사유가 필요하면 그쪽을 부른다.
    """
    root, _ = shadow_ledger_root(repo, shadow_root)
    return os.path.join(root, *SHADOW_LEDGER_RELATIVE)


class RunPaths:
    """런 작업장(`runs/<run-id>/`)의 경로 해석기.

    모든 상대 경로는 세 스테이지 계약의 선언에서 온다. `declared()` 가 basename 으로
    선언을 조회하고, 없거나 둘 이상이면 `PathContractError` 를 던진다 — 계약과 러너가
    어긋나는 순간을 조용히 넘기지 않기 위해서다.
    """

    STAGES = ("source", "read", "freeze", "design", "compose", "gate")

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
    def convergence_early_json(self) -> str:
        """조기 수렴 판정서(재정 P-4). 계약은 이 파일을 outputs 이자 접지 단계의 **선언 입력**
        으로 두 번 적는다(`read.yaml#phase_gates`) — 같은 파일의 중복 선언은 정상이다."""
        return self.path("convergence-early.json")

    @property
    def phase_gate_json(self) -> str:
        """접지 진입 게이트 판정 기록(재정 2026-09-01 T17)."""
        return self.path("phase-gate.json")

    @property
    def convergence_continue_md(self) -> str:
        """수렴 미달 시의 Owner '계속' 봉투(재정 P-U3). 선언 자리는 `phase_gates[].continue_envelope`
        하나뿐이며, 이 경로가 실재하지 않는 것이 정상 상태다(봉투는 필요할 때만 생긴다)."""
        return self.path("convergence-continue.md")

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

    @property
    def shadow_pointer(self) -> str:
        """이 런이 **어느 섀도 원장에 썼는가**의 기록. 계약 미선언 — `10-read/lanes/` 안이다.

        원장 자체는 런 밖에 있으므로(재정 P-U4) 런 산출물만 보아서는 그 자리를 알 수 없고,
        자리를 적지 않으면 다음에 또 사라진다 — 통주 2 의 4행이 worktree 와 함께 없어진 뒤에야
        그 사실이 드러났다. 레인 로그 옆에 두는 이유는 성질이 같기 때문이다: 둘 다 "무엇이
        나왔는가"가 아니라 **"어디로 갔는가"**를 적는 기록이다.
        """
        return os.path.join(self.lanes_dir, SHADOW_POINTER_BASENAME)

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

    def extension(self, version: int) -> str:
        """런 -3 연장 봉투 `15-frozen/extension-v<N>.md`(재정 T64 ① · 계약 라인 extension-envelope/v0).

        계약 미선언 — 오케스트레이터(구동기 `extend`)가 쓰는 봉투이며 `15-frozen/` 안에 산다.
        `freeze.yaml` 의 outputs 는 손대지 않는다(동결 스테이지의 산출이 아니다). 자리를 동결 봉투
        옆으로 둔 이유는 성질이 같기 때문이다 — 둘 다 Owner 육성을 담은 봉투이고 작업 레인은 쓰지 않는다.
        """
        return os.path.join(self.frozen_dir, f"extension-v{version}.md")

    # -- 20-design ----------------------------------------------------------

    @property
    def blueprint_json(self) -> str:
        return self.path("blueprint.json")

    @property
    def blueprint_md(self) -> str:
        return self.path("blueprint.md")

    @property
    def design_report_json(self) -> str:
        return self.path("design-report.json")

    @property
    def design_escalation_json(self) -> str:
        """설계 상신 기록(`optional_outputs`). 실재 = 상신 미처분 · 사람이 본다."""
        return self.path("escalation.json")

    @property
    def anchors_provided_json(self) -> str:
        """설계 레인에 **제공된** 앵커 목록(`optional_outputs`) — `design.anchors-adjudicated-only` 의 대상."""
        return self.path("anchors-provided.json")

    @property
    def design_dir(self) -> str:
        return os.path.dirname(self.blueprint_json)

    @property
    def design_lanes_dir(self) -> str:
        """설계 레인 왕복 보관소. `10-read/lanes/` 와 같은 성질의 러너 산출물이며 `20-design/` 안이다."""
        return os.path.join(self.design_dir, LANES_DIRNAME)

    @property
    def figures_manifest_json(self) -> str:
        """`30-figures/assets/manifest.json`(design 계약의 선언 입력 · 선행 실행된 경우에만 실재)."""
        return self.path("manifest.json")

    # -- 40-compose ---------------------------------------------------------

    def _variant(self, basename_pattern: str, variant: str) -> str:
        """`<variant>` 자리를 변주 id 로 채운다. 패턴 자체는 계약(`compose.yaml`)이 들고 있다."""
        declared = self.declared(basename_pattern)
        if "<variant>" not in declared:
            raise PathContractError(f"계약의 {basename_pattern} 선언에 <variant> 자리가 없다: {declared}")
        return self.absolute(declared.replace("<variant>", variant))

    def thread_annotated(self, variant: str) -> str:
        """`40-compose/<variant>/thread.annotated.md` — 변주의 확정 초안(검사 4 통과 뒤에만 쓴다)."""
        return self._variant("thread.annotated.md", variant)

    def material_defect(self, variant: str) -> str:
        """`40-compose/<variant>/material-defect.md`(`optional_outputs`) — 재료 반려서(D6 규율 ②)."""
        return self._variant("material-defect.md", variant)

    def compose_dir(self, variant: str) -> str:
        return os.path.dirname(self.thread_annotated(variant))

    @property
    def compose_root(self) -> str:
        """`40-compose/` — 변주 디렉터리들의 부모."""
        return os.path.dirname(self.compose_report_json)

    @property
    def compose_report_json(self) -> str:
        return self.path("compose-report.json")

    @property
    def tournament_rows_jsonl(self) -> str:
        """`40-compose/tournament-rows.jsonl` — 런 안의 토너먼트 행(총괄 재량 ⓐ · `ship` 이 원장에 옮긴다)."""
        return self.path("tournament-rows.jsonl")

    @property
    def compose_lanes_dir(self) -> str:
        """펜 레인 왕복 보관소 `40-compose/lanes/` — 계약 outputs 에 선언되어 있다."""
        return os.path.join(self.compose_root, LANES_DIRNAME)

    # -- 50-gate ------------------------------------------------------------

    def gate_dir(self, variant: str) -> str:
        """`50-gate/<variant>/` — 변주별 판정·strip 산출 자리(재정 T64 ② · M3)."""
        return os.path.dirname(self.verdict_json(variant))

    def l0_json(self, variant: str) -> str:
        """`50-gate/<variant>/l0.json` — verdict.json#l0 과 같은 객체(총괄 재량 ⓐ · 별도 계약 라인 없음)."""
        return self._variant("l0.json", variant)

    def verdict_json(self, variant: str) -> str:
        """`50-gate/<variant>/verdict.json`(gate-report/v0)."""
        return self._variant("verdict.json", variant)

    def thread_stripped_md(self, variant: str) -> str:
        """`50-gate/<variant>/thread.stripped.md` — 출하 후보 텍스트(strip 산출 · 예행 종료선의 실물)."""
        return self._variant("thread.stripped.md", variant)

    def thread_json(self, variant: str) -> str:
        """`50-gate/<variant>/thread.json`(thread/v0) — 구조화 출하 객체(재감수 B-04 로 gate 산출)."""
        return self._variant("thread.json", variant)

    def annotation_index_json(self, variant: str) -> str:
        """`50-gate/<variant>/annotation-index.json`(annotation-index/v0) — 계기 국소화(D9)가 소비한다."""
        return self._variant("annotation-index.json", variant)

    @property
    def gate_root(self) -> str:
        """`50-gate/` — 변주 디렉터리들의 부모."""
        return os.path.dirname(self.gate_dir("v1"))

    # -- 생성 ---------------------------------------------------------------

    def ensure_source_dirs(self) -> None:
        os.makedirs(self.figures_raw, exist_ok=True)

    def ensure_read_dirs(self) -> None:
        os.makedirs(self.claim_trees, exist_ok=True)
        os.makedirs(self.lanes_dir, exist_ok=True)

    def ensure_frozen_dir(self) -> None:
        os.makedirs(self.frozen_dir, exist_ok=True)

    def ensure_design_dirs(self) -> None:
        os.makedirs(self.design_lanes_dir, exist_ok=True)

    def ensure_compose_dirs(self, variants=()) -> None:
        os.makedirs(self.compose_lanes_dir, exist_ok=True)
        for variant in variants:
            os.makedirs(self.compose_dir(variant), exist_ok=True)

    def ensure_gate_dirs(self, variants=()) -> None:
        for variant in variants:
            os.makedirs(self.gate_dir(variant), exist_ok=True)
