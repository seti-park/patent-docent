# -*- coding: utf-8 -*-
"""원천 변경 처분의 **실물** 시험 — 표시·상호 링크·진단 (재정 P-U2).

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다.

이 파일이 생긴 이유는 sol 재감수의 P-U2 **부분** 판정이다: *"Overwrite refusal works …
but `superseded-by-source-change` marking and old/new cross-links exist only in
contract/comment; production code does not record them."* 덮어쓰기 거부는 처음부터 돌고
있었고 그것을 지키는 시험도 있었다(`tests/test_m2_read.py#test_source_change_requires_new_run`).
비어 있던 것은 **거부의 흔적**이다 — 구 런이 무엇 때문에 폐기되었는지가 파일로 남지 않으면
"폐기하되 지우지 않는다"는 규율이 말로만 산다.

★ 표본은 **자기완결 미니 세계**다(재정 P-U2 원문). 다른 시험 모듈의 하네스를 빌리지 않고
법 리포·투입물·런 작업장을 이 파일이 스스로 세운다. 그래서 여기에는 **재봉인 도구가 없다** —
재정은 그 도구의 거처를 테스트 하네스로 허락했지만, 미니 세계를 매번 새로 짓는 편이 더
싸므로 짓지 않았다. 존재하지 않는 능력이 가장 강한 구조적 보증이다.

`assert` 는 쓰지 않는다(CLAUDE.md §3). 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고하고,
서브프로세스의 종료 코드는 명시 비교한다.
"""

from __future__ import annotations

import ast
import glob
import os
import shutil
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TESTS = os.path.join(REPO, "tests")
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.paths import RunPaths  # noqa: E402
from engine.stages import StageEnvironmentError, StageError, load_yaml  # noqa: E402
from engine.stages import source as source_stage  # noqa: E402

OLD_RUN_ID = "example-xx1111111a1-rotary-feeder"
NEW_RUN_ID = "example-xx1111111a1-rotary-feeder-r2"

PATENT_META = {
    "number": "XX1111111A1",
    "title": "Rotary feeder assembly with pocket metering (fictional example)",
    "jurisdiction": "XX",
    "kind_code": "A1",
    "assignee": "Example Powders, Inc.",
    "dates": {"priority": "2024-05-02", "filing": "2025-04-30", "publication": "2026-02-11"},
}

# 가공 원천 — 실재 특허가 아니며 실재 특허를 인용하지 않는다.
SOURCE = """# Rotary Feeder Assembly — worked example (fictional)

Applicant: Example Powders, Inc.
Inventors: Mira Solberg; Tomas Weill
Priority: application XX2024-0000222 filed on 2 May 2024 (XX)

## Claims

1. A feeder assembly comprising: a hopper defining an outlet aperture; and a rotary
valve seated below the outlet aperture, the rotary valve having a plurality of pockets.

2. The feeder assembly of claim 1, wherein the rotary valve turns at 12 rpm.

## Description

The rotary valve meters powder at 12 rpm through pockets of 25 cm3 each.
"""

# 원천 변경 = 이 낱말 하나가 바뀌는 일이다(바이트 규모까지 달라지도록 자릿수를 늘린다).
CHANGED_SOURCE = SOURCE.replace("12 rpm", "18.5 rpm")

MARKING = "superseded-by-source-change"


# ---------------------------------------------------------------------------
# 미니 세계 — 법 리포 · 투입물 · 첫 봉인
# ---------------------------------------------------------------------------


def git_law(repo: str, *args: str) -> None:
    """법 리포에 git 명령 하나. 실패하면 그 자리에서 세운다(조용한 실패 금지)."""
    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"법 리포 git {' '.join(args)} 실패({proc.returncode}): {proc.stderr}")


def make_law_repo(destination: str) -> str:
    """계약 + `reader/READER-VERSION` 만 담은 **깨끗한** git 리포.

    러너는 진입 시점 HEAD 에 런을 결박하고 더러운 트리를 거부하므로(재정 P-U1), 시험이 본
    리포의 작업 상태에 좌우되면 안 된다 — 개발 중 더러운 트리에서는 런 거부가 정상이다.
    """
    os.makedirs(destination, exist_ok=True)
    shutil.copytree(
        os.path.join(REPO, "contracts"),
        os.path.join(destination, "contracts"),
        ignore=shutil.ignore_patterns("__pycache__"),
        dirs_exist_ok=True,
    )
    os.makedirs(os.path.join(destination, "reader"), exist_ok=True)
    shutil.copy2(
        os.path.join(REPO, "reader", "READER-VERSION"),
        os.path.join(destination, "reader", "READER-VERSION"),
    )
    git_law(destination, "init", "-q")
    git_law(destination, "config", "user.email", "runner@example.com")
    git_law(destination, "config", "user.name", "runner")
    git_law(destination, "add", "contracts", "reader")
    git_law(destination, "commit", "-q", "-m", "law snapshot")
    return destination


def figure_bytes(index: int, *, salt: int = 0) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + bytes([index]) * (16 + salt)


def make_inputs(
    base: str, *, figure_count: int = 6, source_text: str = SOURCE, salted: set | None = None
) -> tuple[str, str]:
    """투입물(원문 파일 + 도면 원본). 런 작업장 **밖**의 자리다.

    `salted` = 같은 파일명으로 **내용만** 다른 도면을 만들 도면 번호. 세트 변경 3종(추가·삭제·
    교체) 중 교체는 파일 목록이 그대로이므로, 이 갈래가 없으면 매니페스트 지문의 존재 이유가
    시험되지 않는다.
    """
    figures = os.path.join(base, "figures")
    os.makedirs(figures, exist_ok=True)
    patent_path = os.path.join(base, "patent-source.md")
    with open(patent_path, "w", encoding="utf-8") as handle:
        handle.write(source_text)
    for index in range(1, figure_count + 1):
        with open(os.path.join(figures, f"fig-{index:02d}.png"), "wb") as handle:
            handle.write(figure_bytes(index, salt=1 if index in (salted or set()) else 0))
    return patent_path, figures


def seal(
    world: str,
    *,
    run_id: str = OLD_RUN_ID,
    figure_count: int = 6,
    source_text: str = SOURCE,
    salted: set | None = None,
    supersedes_run_root: str | None = None,
) -> tuple[str, dict]:
    """미니 세계에 런 하나를 봉인한다. 반환 = `(런 작업장, 결과)`."""
    inbox = os.path.join(world, "inbox", run_id)
    os.makedirs(inbox, exist_ok=True)
    patent_path, figures = make_inputs(
        inbox, figure_count=figure_count, source_text=source_text, salted=salted
    )
    run_root = os.path.join(world, "runs", run_id)
    outcome = source_stage.run(
        run_root=run_root,
        source_patent_path=patent_path,
        figures_dir=figures,
        run_id=run_id,
        patent_meta=dict(PATENT_META),
        repo=law_repo(world),
        supersedes_run_root=supersedes_run_root,
    )
    return run_root, outcome


def law_repo(world: str) -> str:
    """미니 세계의 법. 세계마다 하나이며 없으면 짓는다."""
    root = os.path.join(world, "law")
    if not os.path.isdir(os.path.join(root, ".git")):
        make_law_repo(root)
    return root


def reseal_attempt(
    world: str,
    run_root: str,
    *,
    figure_count: int = 6,
    source_text: str = SOURCE,
    salted: set | None = None,
    tag: str = "again",
) -> StageError:
    """같은 작업장에 다시 봉인을 시도하고 **던져진 예외를 돌려준다**.

    예외가 나지 않으면 그 자체가 결함이다 — 00-source/ 는 한 번만 쓴다(SPEC §7.4).
    """
    inbox = os.path.join(world, "inbox", tag)
    os.makedirs(inbox, exist_ok=True)
    patent_path, figures = make_inputs(
        inbox, figure_count=figure_count, source_text=source_text, salted=salted
    )
    try:
        source_stage.run(
            run_root=run_root,
            source_patent_path=patent_path,
            figures_dir=figures,
            run_id=os.path.basename(run_root),
            patent_meta=dict(PATENT_META),
            repo=law_repo(world),
        )
    except StageError as exc:
        return exc
    raise RuntimeError("재투입이 거부되지 않았다 — 00-source/ 는 한 번만 쓴다")


def meta_of(run_root: str) -> dict:
    return load_yaml(RunPaths(run_root).run_yaml)


def sealed_fingerprint(run_root: str) -> dict[str, bytes]:
    """봉인물의 **바이트 그대로**. 지문이 아니라 바이트를 드는 이유 — 이 시험이 지키려는 것이
    "다시 쓰지 않았다"이고, 지문 대조는 재계산 경로를 시험 안으로 들이기 때문이다."""
    paths = RunPaths(run_root)
    out: dict[str, bytes] = {}
    for path in (paths.patent_md, paths.patent_sha256):
        with open(path, "rb") as handle:
            out[os.path.relpath(path, run_root)] = handle.read()
    for name in sorted(os.listdir(paths.figures_raw)):
        target = os.path.join(paths.figures_raw, name)
        with open(target, "rb") as handle:
            out[os.path.relpath(target, run_root)] = handle.read()
    return out


def supersede_scenario(world: str) -> dict:
    """구 런 봉인 → 원문 변경 재투입 → 표시까지의 **한 살림**.

    시험 본체와 `python3 -O` 서브프로세스가 같은 코드를 돈다. 두 벌로 적으면 한 벌이 낡고,
    낡은 사본으로 최적화 모드를 재면 그 측정이 공허해진다.
    """
    run_root, _ = seal(world)
    before = sealed_fingerprint(run_root)
    error = reseal_attempt(world, run_root, source_text=CHANGED_SOURCE, tag="changed")
    meta = meta_of(run_root)
    return {
        "run_root": run_root,
        "error_type": type(error).__name__,
        "message": str(error),
        "status": str(meta.get("status", "")),
        "superseded_by": meta.get("superseded_by"),
        "source_change": meta.get("source_change") or {},
        "seal_intact": sealed_fingerprint(run_root) == before,
    }


# ===========================================================================
# 1. 표시가 실물이 되는가
# ===========================================================================


def test_source_body_change_marks_old_run_in_a_file(tmp_path) -> None:
    """표시가 계약과 주석에만 있으면 "폐기하되 지우지 않는다"가 기록이 아니라 말이 된다(재정 P-U2)."""
    world = str(tmp_path)
    result = supersede_scenario(world)

    if result["error_type"] != "StageEnvironmentError":
        pytest.fail(f"원천 변경이 환경 오류로 판정되지 않았다: {result['error_type']}")
    if result["status"] != MARKING:
        pytest.fail(f"구 런 status 기대 {MARKING!r}, 실제 {result['status']!r}")

    block = result["source_change"]
    if not block:
        pytest.fail("run.yaml 에 source_change 진단 블록이 없다")
    if block.get("link_state") != "pending":
        pytest.fail(f"link_state 기대 'pending', 실제 {block.get('link_state')!r}")
    if result["superseded_by"] is not None:
        pytest.fail(f"신 런이 없는데 superseded_by 가 채워졌다: {result['superseded_by']!r}")
    if not str(block.get("link_note", "")).strip():
        pytest.fail("미완성 링크가 무엇을 뜻하는지 파일이 적지 않는다 — link_note 가 비었다")

    # 진단 = 파일 · 규모 · 구/신 지문(재정 P-U2 "변경 내용(파일·규모)을 명시한다").
    rows = [row for row in block.get("changes") or [] if row.get("path") == "00-source/patent.md"]
    if len(rows) != 1:
        pytest.fail(f"patent.md 변경 행이 1건이 아니다: {block.get('changes')}")
    row = rows[0]
    if row.get("change") != "modified":
        pytest.fail(f"변경 종류 기대 'modified', 실제 {row.get('change')!r}")
    if not (str(row.get("old_sha256", "")).startswith("sha256:")
            and str(row.get("new_sha256", "")).startswith("sha256:")):
        pytest.fail(f"구/신 지문이 없다: {row}")
    if row["old_sha256"] == row["new_sha256"]:
        pytest.fail("구/신 지문이 같다 — 변경이 아닌 것을 변경으로 적었다")
    expected_delta = len(CHANGED_SOURCE.encode("utf-8")) - len(SOURCE.encode("utf-8"))
    if row.get("byte_delta") != expected_delta:
        pytest.fail(f"바이트 증감 기대 {expected_delta}, 실제 {row.get('byte_delta')}")
    if row.get("new_bytes") - row.get("old_bytes") != expected_delta:
        pytest.fail(f"규모 기록이 증감과 어긋난다: {row}")

    # 진단문에도 같은 내용이 실린다 — 파일을 열지 않는 사람도 무엇이 바뀌었는지 안다.
    for needle in ("00-source/patent.md", "bytes", MARKING):
        if needle not in result["message"]:
            pytest.fail(f"진단문에 {needle!r} 이 없다: {result['message']}")


def test_figure_set_change_marks_old_run(tmp_path) -> None:
    """도면 세트가 감지 범위 밖이면 그림만 갈아 끼운 런이 조용히 통과한다(재정 P-U2 = 원천은 도면 세트 전체)."""
    cases = {
        # 이름 → (도면 수, 교체 대상, 기대 변경 경로, 기대 변경 종류)
        "added": (7, None, "00-source/figures-raw/fig-07.png", "added"),
        "removed": (5, None, "00-source/figures-raw/fig-06.png", "removed"),
        "modified": (6, {3}, "00-source/figures-raw/fig-03.png", "modified"),
    }
    for name, (count, salted, path, kind) in cases.items():
        world = str(tmp_path.joinpath(name))
        os.makedirs(world, exist_ok=True)
        run_root, _ = seal(world)
        error = reseal_attempt(
            world, run_root, figure_count=count, salted=salted, tag=f"figures-{name}"
        )
        if not isinstance(error, StageEnvironmentError):
            pytest.fail(f"[{name}] 도면 세트 변경이 환경 오류로 판정되지 않았다: {type(error).__name__}")
        if "매니페스트" not in str(error):
            pytest.fail(f"[{name}] 매니페스트 지문 경로로 판정되지 않았다: {error}")

        meta = meta_of(run_root)
        if str(meta.get("status", "")) != MARKING:
            pytest.fail(f"[{name}] 구 런 status 기대 {MARKING!r}, 실제 {meta.get('status')!r}")
        block = meta.get("source_change") or {}
        rows = {row["path"]: row for row in block.get("changes") or []}
        if path not in rows:
            pytest.fail(f"[{name}] 진단에 {path} 행이 없다: {sorted(rows)}")
        if rows[path]["change"] != kind:
            pytest.fail(f"[{name}] 변경 종류 기대 {kind!r}, 실제 {rows[path]['change']!r}")

        manifest = block.get("figures_manifest_digest") or {}
        if manifest.get("old") == manifest.get("new"):
            pytest.fail(f"[{name}] 매니페스트 지문 구/신 이 같다: {manifest}")
        if not str(manifest.get("old", "")).startswith("sha256:"):
            pytest.fail(f"[{name}] 매니페스트 지문이 기록되지 않았다: {manifest}")

        # 본문은 그대로다 — 도면만 바뀐 사고가 원문 변경으로 오기록되면 진단이 거짓말을 한다.
        if "00-source/patent.md" in rows:
            pytest.fail(f"[{name}] 본문이 그대로인데 변경으로 적혔다: {rows['00-source/patent.md']}")


# ===========================================================================
# 2. 상호 링크
# ===========================================================================


def test_cross_link_round_trips_between_old_and_new_run(tmp_path) -> None:
    """링크가 한쪽뿐이면 구 런에서 후속을 찾을 수 없거나 신 런의 내력이 사라진다(재정 P-U2)."""
    world = str(tmp_path)
    old_root, _ = seal(world)
    reseal_attempt(world, old_root, source_text=CHANGED_SOURCE, tag="changed")

    # 처분은 새 런이다 — 바뀐 원천 위에 신 런을 연다.
    new_root, outcome = seal(
        world, run_id=NEW_RUN_ID, source_text=CHANGED_SOURCE, supersedes_run_root=old_root
    )
    if outcome["status"] != "ok":
        pytest.fail(f"신 런이 ok 를 내지 않았다: {outcome['status']}")

    old_meta, new_meta = meta_of(old_root), meta_of(new_root)
    if old_meta.get("superseded_by") != NEW_RUN_ID:
        pytest.fail(f"구 런 → 신 런 링크가 없다: superseded_by={old_meta.get('superseded_by')!r}")
    if new_meta.get("supersedes") != OLD_RUN_ID:
        pytest.fail(f"신 런 → 구 런 링크가 없다: supersedes={new_meta.get('supersedes')!r}")
    if (old_meta.get("source_change") or {}).get("link_state") != "linked":
        pytest.fail(f"링크가 닫혔는데 link_state 가 갱신되지 않았다: {old_meta.get('source_change')}")

    # 왕복 — 링크만 들고 서로에게 실제로 **도달**한다(디렉터리명 == run_id, source.run-id).
    runs_dir = os.path.dirname(old_root)
    forward = os.path.join(runs_dir, str(old_meta["superseded_by"]))
    backward = os.path.join(runs_dir, str(new_meta["supersedes"]))
    if os.path.realpath(forward) != os.path.realpath(new_root):
        pytest.fail(f"구 런의 링크가 신 런에 닿지 않는다: {forward}")
    if os.path.realpath(backward) != os.path.realpath(old_root):
        pytest.fail(f"신 런의 링크가 구 런에 닿지 않는다: {backward}")

    # 표시 없는 런을 승계로 적을 수 없다 — 링크는 표시의 뒤를 따른다.
    plain_root, _ = seal(world, run_id="example-xx1111111a1-plain")
    with pytest.raises(StageError) as excinfo:
        seal(
            world,
            run_id="example-xx1111111a1-plain-r2",
            source_text=CHANGED_SOURCE,
            supersedes_run_root=plain_root,
        )
    if MARKING not in str(excinfo.value):
        pytest.fail(f"거절 사유가 표시 부재를 밝히지 않는다: {excinfo.value}")


# ===========================================================================
# 3. 반증 — 봉인 불변 · 과잉 표시 금지 · 최적화 모드
# ===========================================================================


def test_marking_does_not_touch_the_seal(tmp_path) -> None:
    """표시가 봉인물에 닿으면 "원천이 바뀌면 새 런"이 표시 절차에 딸린 뒷문을 얻는다(재정 P-U2)."""
    world = str(tmp_path)
    run_root, _ = seal(world)
    before = sealed_fingerprint(run_root)

    reseal_attempt(world, run_root, source_text=CHANGED_SOURCE, tag="changed")
    reseal_attempt(world, run_root, figure_count=7, tag="figures")

    after = sealed_fingerprint(run_root)
    if after != before:
        differing = sorted(
            key for key in set(before) | set(after) if before.get(key) != after.get(key)
        )
        pytest.fail(f"처분 뒤 봉인물의 바이트가 달라졌다: {differing}")
    if meta_of(run_root).get("status") != MARKING:
        pytest.fail("봉인은 지켰으나 표시가 서지 않았다 — 이 시험이 공허해진다")


def test_unchanged_reinput_is_refused_without_marking(tmp_path) -> None:
    """과잉 표시는 표시의 뜻을 지운다 — 정직한 경로(무변경 재실행)가 벌받지 않아야 한다."""
    world = str(tmp_path)
    run_root, _ = seal(world)

    error = reseal_attempt(world, run_root, tag="identical")
    if isinstance(error, StageEnvironmentError):
        pytest.fail(f"같은 투입물인데 지문 불일치로 판정됐다: {error}")
    if "이미 고정" not in str(error):
        pytest.fail(f"덮어쓰기 거부가 아닌 다른 사유로 멈췄다: {error}")

    meta = meta_of(run_root)
    if meta.get("status") != "active":
        pytest.fail(f"무변경 재실행이 런의 상태를 바꿨다: {meta.get('status')!r}")
    if "source_change" in meta:
        pytest.fail(f"무변경인데 변경 진단이 남았다: {meta['source_change']}")

    # 투입물 부재도 런을 넘어뜨린다 — 그것은 다른 사고이므로 표시가 서지 않는다.
    # ★ 실측(2026-08-18): 이 갈래는 진입 검사에 닿기 전에 `FileNotFoundError` 로 죽는다.
    #   러너가 정본화를 위해 투입물을 먼저 열기 때문이다(계약은 이 부재를 환경 오류로 적는다 —
    #   `source.input-digest`). 층이 어긋나 있지만 그것은 P-C 관할이므로 여기서는 실물 그대로
    #   적고, 이 시험이 지키는 것은 하나다: **원천 변경이 아닌 실패는 표시를 남기지 않는다.**
    with pytest.raises(OSError):
        source_stage.run(
            run_root=run_root,
            source_patent_path=os.path.join(world, "inbox", "ghost", "patent-source.md"),
            figures_dir=os.path.join(world, "inbox", "ghost", "figures"),
            run_id=OLD_RUN_ID,
            patent_meta=dict(PATENT_META),
            repo=law_repo(world),
        )
    if meta_of(run_root).get("status") != "active":
        pytest.fail("투입물 부재가 원천 변경으로 표시됐다 — 두 사고가 한 표시로 접혔다")


def test_marking_survives_optimized_mode(tmp_path) -> None:
    """`python3 -O` 에서 표시가 사라지면 생산 실행에서 이 처분이 통째로 공허해진다(CLAUDE.md §3)."""
    world = str(tmp_path.joinpath("optimized"))
    os.makedirs(world, exist_ok=True)
    script = os.path.join(str(tmp_path), "scenario.py")
    with open(script, "w", encoding="utf-8") as handle:
        handle.write(
            "import sys\n"
            f"sys.path.insert(0, {TESTS!r})\n"
            f"sys.path.insert(0, {REPO!r})\n"
            "import test_m16_source_supersede as harness\n"
            f"result = harness.supersede_scenario({world!r})\n"
            "ok = (\n"
            f"    result['status'] == {MARKING!r}\n"
            "    and result['error_type'] == 'StageEnvironmentError'\n"
            "    and result['seal_intact']\n"
            "    and result['source_change'].get('link_state') == 'pending'\n"
            "    and any(row['path'] == '00-source/patent.md'\n"
            "            for row in result['source_change'].get('changes') or [])\n"
            ")\n"
            "print(result['status'])\n"
            "sys.exit(0 if ok else 1)\n"
        )
    proc = subprocess.run(
        [sys.executable, "-O", script], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        pytest.fail(
            f"-O 종료 코드 기대 0, 실제 {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        )
    if proc.stdout.strip() != MARKING:
        pytest.fail(f"-O 산출 기대 {MARKING!r}, 실제 {proc.stdout.strip()!r}")


# ===========================================================================
# 4. 구조 — 재봉인 자리의 부재 · 어휘의 정본
# ===========================================================================

# 봉인물 경로 프로퍼티(`RunPaths` 의 이름). 이 셋에 **쓰는** 자리가 몇 곳인가가 관심사다.
SEALED_ATTRS = ("patent_md", "patent_sha256", "figures_raw")
# 쓰기로 세는 호출. `open` 은 모드 인자에 w·a·x 가 있을 때만 쓰기다(읽기 열기는 위반이 아니다).
# `makedirs` 는 뺀다 — 디렉터리를 **만드는** 일은 봉인물을 다시 쓰는 일이 아니며, 그 자리는
# `RunPaths.ensure_source_dirs` 하나다(빈 자리를 준비하는 것과 내용을 갈아 끼우는 것은 다르다).
WRITE_CALLS = (
    "write_text", "write_json", "dump_yaml",
    "copy", "copy2", "copyfile", "copytree",
    "rename", "replace", "remove", "unlink", "rmtree",
)


def _enclosing_functions(tree: ast.AST) -> list[tuple[int, int, str]]:
    return [
        (node.lineno, getattr(node, "end_lineno", node.lineno), node.name)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def _is_write_call(node: ast.Call) -> bool:
    name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
    if name in WRITE_CALLS:
        return True
    if name != "open":
        return False
    modes = [arg for arg in node.args[1:] if isinstance(arg, ast.Constant)]
    modes += [kw.value for kw in node.keywords if kw.arg == "mode" and isinstance(kw.value, ast.Constant)]
    return any(set("wax") & set(str(mode.value)) for mode in modes)


def _seal_writers() -> set[tuple[str, str]]:
    """봉인물에 쓰는 `(파일, 함수)` 전량 — AST 로 센다."""
    writers: set[tuple[str, str]] = set()
    for path in sorted(glob.glob(os.path.join(REPO, "engine", "**", "*.py"), recursive=True)):
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=path)
        functions = _enclosing_functions(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not _is_write_call(node):
                continue
            touched = any(
                isinstance(inner, ast.Attribute) and inner.attr in SEALED_ATTRS
                for arg in [*node.args, *[kw.value for kw in node.keywords]]
                for inner in ast.walk(arg)
            )
            if not touched:
                continue
            owner = sorted(
                (start, name) for start, end, name in functions if start <= node.lineno <= end
            )
            writers.add((os.path.relpath(path, REPO), owner[-1][1] if owner else "<module>"))
    return writers


def test_only_the_first_seal_writes_the_seal(tmp_path) -> None:
    """재봉인 자리가 생산 경로에 있으면 "지문이 안 맞으니 다시 계산한다"가 함수 호출 하나가 된다(재정 P-U2)."""
    expected = {("engine/stages/source.py", "run")}
    writers = _seal_writers()
    if writers != expected:
        pytest.fail(f"봉인물에 쓰는 자리 기대 {sorted(expected)}, 실제 {sorted(writers)}")

    # 이름으로 숨긴 재봉인 도구도 없다(구 시험이 지키던 금지 목록을 그대로 잇는다).
    with open(os.path.join(REPO, "engine", "stages", "source.py"), encoding="utf-8") as handle:
        code = handle.read()
    for forbidden in ("def reseal", "def rewrite_digest", "def force_source"):
        if forbidden in code:
            pytest.fail(f"생산 경로에 재봉인 자리가 있다: {forbidden}")


def test_marking_vocabulary_lives_in_the_contract(tmp_path) -> None:
    """어휘가 코드에도 있으면 사본이 둘이 되고, 둘이 되면 한 벌은 반드시 낡는다."""
    declared = (
        (source_stage._source_change_policy(RunPaths(str(tmp_path)).contracts["source"])
         .get("marking") or {}).get("old_run") or {}
    )
    if declared.get("status") != MARKING:
        pytest.fail(f"계약이 선언한 표시값이 다르다: {declared.get('status')!r}")

    offenders: list[str] = []
    for path in sorted(glob.glob(os.path.join(REPO, "engine", "**", "*.py"), recursive=True)):
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=path)
        # 서술(docstring)은 위반이 아니다 — 위반은 어휘를 **값으로** 드는 일이다.
        docstrings = {
            id(node.body[0].value)
            for node in ast.walk(tree)
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            and node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
        }
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and MARKING in node.value
                and id(node) not in docstrings
            ):
                offenders.append(f"{os.path.relpath(path, REPO)}:{node.lineno}")
    if offenders:
        pytest.fail(f"엔진이 표시 어휘를 리터럴로 든다(정본은 계약이다): {offenders}")
