# -*- coding: utf-8 -*-
"""K8 판정 8(공유 코어 표면 폐쇄 대조)의 반증 시험 — 재정 2026-08-18 P-2 ⓑ.

sol 독립 감수(`docs/lessons/2026-08-18-sol-audit-m15-full.md`)의 P-2 ⓑ **부분** 판정이
이 파일의 존재 이유다. 감수자는 `patent.marketing_verdict` — 순전한 프로젝트 편집 판단 —
를 `[공유 코어]` 표지까지 달아 공유 코어에 심었고, 검사기는 plain·`-O` 양쪽에서
exit 0 · findings=0 을 냈다. 판정 문언: *"Enforces known names, not the boundary
principle."*

그러므로 여기서 증명해야 하는 것은 "K8 이 존재한다" 가 아니라 **그 변조가 이제 잡힌다**는
것이다. 그리고 잡히기만 해서는 부족하다 — 전부 거부하는 검사도 변조를 잡기 때문이다.
그래서 무변조 정본 사본이 통과하는 대조군을 같은 무게로 둔다(과잉 제약의 반증).

규약(CLAUDE.md §3): 테스트 모듈의 맨 `assert` 는 pytest 가 AST 를 재작성하므로 살아남지만,
**서브프로세스의 종료 코드는 명시 비교**로 본다. 아래는 전부 명시 비교 + `pytest.fail()` 이다.

변조는 임시 디렉터리의 리포 사본에서만 한다 — 정본 스키마를 변조 상태로 남기지 않는다.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_spec_refs.py"
SCHEMA_REL = Path("reader") / "schemas" / "material-spec.schema.json"
SURFACE_REL = Path("reader") / "core-surface.yaml"

# 검사기가 읽는 세계 전부 = 문서 2종 + 계약 트리 2개. 리포 사본이라 함은 이것으로 족하다
# (`runs/`·`.git`·`.venv` 는 검사기의 시야 밖이며, 복사 비용만 키운다).
COPIED_TREES = ("docs", "contracts", "reader")


def run_tool(args: list[str], optimized: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable]
    if optimized:
        cmd.append("-O")
    cmd += [str(TOOL)] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))


def repo_copy(dest: Path, mutate=None) -> str:
    """정본 리포의 검사 대상 트리를 사본으로 만들고, 스키마만 변조한다."""
    dest.mkdir(parents=True, exist_ok=True)
    for tree in COPIED_TREES:
        shutil.copytree(
            REPO_ROOT / tree,
            dest / tree,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    if mutate is not None:
        schema_path = dest / SCHEMA_REL
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        mutate(schema)
        schema_path.write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return str(dest)


# ---------------------------------------------------------------------------
# 변조 표본 — 셋 다 "이름을 아는 금칙 목록" 으로는 잡히지 않는 형태다.
# ---------------------------------------------------------------------------


def plant_sol_marketing_verdict(schema: dict) -> None:
    """감수자의 변조 재현 — 편집 판단을 `[공유 코어]` 표지와 함께 코어에 심는다.

    표지가 정확하므로 판정 3(층 표지)은 만족하고, `marketing_verdict` 는 확장 전용 키
    목록에 없으므로 판정 7 도 침묵한다. 오직 판정 8(승인되지 않은 표면)만이 이것을 본다.
    """
    schema["properties"]["patent"]["properties"]["marketing_verdict"] = {
        "$comment": "[공유 코어] 이 특허를 스레드 소재로 밀어붙일 만한가에 대한 판단.",
        "type": "string",
    }


def plant_unknown_new_key(schema: dict) -> None:
    """이름을 아무도 모르는 새 키 — 금칙 목록 방식이 원리적으로 놓치는 자리."""
    schema["$defs"]["claims"]["properties"]["editorial_priority"] = {
        "$comment": "[공유 코어] 어느 청구항을 먼저 보여줄지의 편집 우선순위.",
        "type": "integer",
    }


def delete_declared_path(schema: dict) -> None:
    """정직한 삭제 — 상대 프로젝트가 읽던 필드를 조용히 없앤다."""
    patent = schema["properties"]["patent"]
    del patent["properties"]["kind_code"]
    patent["required"] = [key for key in patent["required"] if key != "kind_code"]


# (id, 변조 함수, 기대 종료 코드, 잡히지 않으면 무엇이 공허해지는가)
CASES = [
    ("pristine", None, 0, "무변조 정본이 걸리면 이 검사는 전부 거부하는 그물이다"),
    (
        "sol-marketing-verdict",
        plant_sol_marketing_verdict,
        1,
        "감수가 심은 프로젝트 판단이 다시 공유 코어에 조용히 살게 된다(P-2 ⓑ 미집행)",
    ),
    (
        "unknown-new-key",
        plant_unknown_new_key,
        1,
        "이름을 모르는 새 키가 코어로 들어와 금칙 목록 방식의 한계가 그대로 남는다",
    ),
    (
        "declared-path-deleted",
        delete_declared_path,
        1,
        "계약면의 축소가 침묵으로 넘어가 그물이 추가만 잡는 반쪽이 된다",
    ),
]


@pytest.mark.parametrize("case_id,mutate,expected,vacuous", CASES, ids=[case[0] for case in CASES])
@pytest.mark.parametrize("optimized", [False, True], ids=["plain", "O"])
def test_core_surface_closure(
    tmp_path: Path, case_id: str, mutate, expected: int, vacuous: str, optimized: bool
) -> None:
    """변조 3종은 exit 1, 무변조 정본은 exit 0 — `python3` 과 `python3 -O` 에서 동일하게.

    감수는 두 모드 **양쪽에서** exit 0 을 받아냈다. 그러므로 반증도 양쪽에서 서야 한다.
    """
    repo = repo_copy(tmp_path / case_id, mutate)
    proc = run_tool(["--repo", repo], optimized=optimized)
    if proc.returncode != expected:
        pytest.fail(
            f"EXIT MISMATCH ({case_id}, {'-O' if optimized else 'plain'}): "
            f"got={proc.returncode} want={expected} — {vacuous}\n"
            f"stdout:\n{proc.stdout[-1500:]}\nstderr:\n{proc.stderr[-800:]}"
        )


@pytest.mark.parametrize(
    "case_id,mutate,needle",
    [
        ("sol-marketing-verdict", plant_sol_marketing_verdict, "marketing_verdict"),
        ("unknown-new-key", plant_unknown_new_key, "editorial_priority"),
        ("declared-path-deleted", delete_declared_path, "kind_code"),
    ],
)
def test_k8_names_the_offending_path(tmp_path: Path, case_id: str, mutate, needle: str) -> None:
    """결함은 K8 하나에서만 나고, 어긋난 **경로를 지목**하며, 근거(재정 P-2)를 문언에 든다.

    경로를 지목하지 않는 판정은 사람이 무엇을 되돌려야 하는지 알려주지 못하고, 그러면
    승인 목록은 "일단 붙여 넣어 통과시키는" 의식이 된다.
    """
    repo = repo_copy(tmp_path / case_id, mutate)
    proc = run_tool(["--repo", repo, "--json"])
    if proc.returncode != 1:
        pytest.fail(f"EXIT MISMATCH ({case_id}): got={proc.returncode} want=1\n{proc.stdout[-1200:]}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"--json 출력 파싱 실패 ({case_id}): {exc}\nstdout:\n{proc.stdout[:800]}")
    failing = {check["id"] for check in payload["checks"] if check["status"] == "FAIL"}
    if failing != {"K8"}:
        pytest.fail(f"FAILING CHECK MISMATCH ({case_id}): got={sorted(failing)} want=['K8']")
    k8 = [finding for finding in payload["findings"] if finding["check"] == "K8"]
    if not any(needle in finding["found"] for finding in k8):
        pytest.fail(f"K8 결함이 경로를 지목하지 않는다 ({case_id}, {needle!r}): {k8}")
    if not any("P-2" in finding["message"] for finding in k8):
        pytest.fail(f"K8 판정 문언에 근거(재정 P-2)가 없다 ({case_id}): {k8}")


def test_print_core_surface_matches_declaration() -> None:
    """`--print-core-surface` 의 실측 출력 == `reader/core-surface.yaml` 의 승인 목록.

    둘이 어긋나면 정본 리포가 이미 미승인 표면을 갖고 있다는 뜻이다(그때는 위 폐쇄 대조도
    같이 실패한다). 이 시험은 갱신 절차가 실제로 붙여 넣을 수 있는 서식을 내는지도 함께 본다.
    """
    proc = run_tool(["--print-core-surface"])
    if proc.returncode != 0:
        pytest.fail(f"EXIT MISMATCH: got={proc.returncode} want=0\nstderr:\n{proc.stderr}")
    printed = yaml.safe_load(proc.stdout)
    declared = yaml.safe_load((REPO_ROOT / SURFACE_REL).read_text(encoding="utf-8"))
    if not isinstance(printed, dict) or not isinstance(printed.get("paths"), list):
        pytest.fail(f"출력이 `paths` 목록을 담은 맵이 아니다: {proc.stdout[:300]!r}")
    if printed["paths"] != declared["paths"]:
        only_printed = sorted(set(printed["paths"]) - set(declared["paths"]))
        only_declared = sorted(set(declared["paths"]) - set(printed["paths"]))
        pytest.fail(
            "실측 표면과 승인 목록이 다르다 — "
            f"출력에만 {only_printed[:5]} · 선언에만 {only_declared[:5]}"
        )


def test_print_core_surface_writes_no_file(tmp_path: Path) -> None:
    """설계 요건 4 — 이 플래그는 표준출력에만 쓴다. 사본의 어느 파일도 바뀌지 않는다."""
    repo = Path(repo_copy(tmp_path / "readonly"))
    before = {
        path: path.read_bytes()
        for path in sorted(repo.rglob("*"))
        if path.is_file()
    }
    proc = run_tool(["--repo", str(repo), "--print-core-surface"])
    if proc.returncode != 0:
        pytest.fail(f"EXIT MISMATCH: got={proc.returncode} want=0\nstderr:\n{proc.stderr}")
    after = {
        path: path.read_bytes()
        for path in sorted(repo.rglob("*"))
        if path.is_file()
    }
    if before != after:
        changed = sorted(
            str(path.relative_to(repo))
            for path in set(before) | set(after)
            if before.get(path) != after.get(path)
        )
        pytest.fail(f"read-only 도구가 파일을 건드렸다: {changed}")


def test_missing_declaration_is_environment_error(tmp_path: Path) -> None:
    """승인 목록의 부재 = 환경 오류(exit 2). 없으면 통과하는 검사는 검사가 아니다."""
    repo = Path(repo_copy(tmp_path / "no-surface"))
    (repo / SURFACE_REL).unlink()
    proc = run_tool(["--repo", str(repo)])
    if proc.returncode != 2:
        pytest.fail(
            f"EXIT MISMATCH: got={proc.returncode} want=2\n"
            f"stdout:\n{proc.stdout[-800:]}\nstderr:\n{proc.stderr[-400:]}"
        )


def test_unsorted_declaration_is_environment_error(tmp_path: Path) -> None:
    """정렬 강제 — 순서가 흔들리면 "무엇이 늘었는가" 가 diff 에서 보이지 않는다."""
    repo = Path(repo_copy(tmp_path / "unsorted"))
    surface_path = repo / SURFACE_REL
    data = yaml.safe_load(surface_path.read_text(encoding="utf-8"))
    data["paths"] = list(reversed(data["paths"]))
    surface_path.write_text(
        yaml.safe_dump(data, allow_unicode=True, default_flow_style=False, width=10**6),
        encoding="utf-8",
    )
    proc = run_tool(["--repo", str(repo)])
    if proc.returncode != 2:
        pytest.fail(
            f"EXIT MISMATCH: got={proc.returncode} want=2\n"
            f"stdout:\n{proc.stdout[-800:]}\nstderr:\n{proc.stderr[-400:]}"
        )
