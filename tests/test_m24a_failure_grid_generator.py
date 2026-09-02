# -*- coding: utf-8 -*-
"""B-0 READ failure-grid 생성기와 순수 manifest 검증기의 단위 시험."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
from collections.abc import Callable
from typing import Any

import pytest

from engine.stages.read import ENGINE_READ_CHECK_IDS
from reader.lib.run_checks import READ_CHECK_IDS


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON_BIN = "/home/laptop/projects/patent-docent/.venv/bin/python"
MAIN_REPO = "/home/laptop/projects/patent-docent"
GENERATOR_PATH = REPO_ROOT / "tests" / "fixtures" / "read-failure-grid" / "generate.py"
OUTPUT_NAMES = (
    "tests/fixtures/read-failure-grid/generate.py",
    "tests/fixtures/read-failure-grid/validate_manifest.py",
    "tests/test_m24a_failure_grid_generator.py",
)
EXPECTED_COUNTS = {
    "halt/null": 6144,
    "escalate/null": 1023,
    "escalate/국면 간 변이 재현 — 코드 결함 의심": 1020,
    "StageError": 3,
    "total": 8190,
}


def _load_path(name: str, path: pathlib.Path) -> Any:
    if not path.is_file():
        pytest.fail(f"적재할 파일이 없다: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"적재 명세를 만들 수 없다: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# T-7과 같은 tests/ 기준 경로식이어야 한다(AC-1).
_vm_path = pathlib.Path(__file__).parent / "fixtures" / "read-failure-grid" / "validate_manifest.py"
validate_manifest_mod = _load_path("validate_manifest", _vm_path)
generate_mod = _load_path("read_failure_grid_generate", GENERATOR_PATH)


def _run(
    command: list[str],
    *,
    cwd: pathlib.Path | str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return _run(["git", "-C", str(repo), *args])


def _require_ok(proc: subprocess.CompletedProcess[str], context: str) -> None:
    if proc.returncode != 0:
        pytest.fail(
            f"{context} 실패(rc={proc.returncode})\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def _commit(repo: pathlib.Path, message: str) -> None:
    proc = _git(
        repo,
        "-c",
        "user.name=B0 Fixture",
        "-c",
        "user.email=b0-fixture@example.invalid",
        "commit",
        "-q",
        "-m",
        message,
    )
    _require_ok(proc, "fixture commit")


@pytest.fixture(scope="module")
def committed_clone(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = tmp_path_factory.mktemp("m24a-committed-clone")
    clone = root / "clone"
    proc = _run(["git", "clone", "-q", "--no-hardlinks", MAIN_REPO, str(clone)])
    _require_ok(proc, "시험용 clone")

    for relative in OUTPUT_NAMES:
        source = REPO_ROOT / relative
        if not source.is_file():
            pytest.fail(f"B-0 산출물이 없다: {source}")
        target = clone / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    status = _git(clone, "status", "--porcelain")
    _require_ok(status, "clone status")
    if status.stdout.strip():
        add = _git(clone, "add", *OUTPUT_NAMES)
        _require_ok(add, "B-0 세 파일 add")
        _commit(clone, "b0-fixture")

    clean = _git(clone, "status", "--porcelain")
    _require_ok(clean, "fixture clone clean 검사")
    if clean.stdout:
        pytest.fail(f"fixture clone이 깨끗하지 않다: {clean.stdout!r}")

    short = _git(clone, "rev-parse", "--short=7", "HEAD")
    full = _git(clone, "rev-parse", "HEAD")
    _require_ok(short, "short HEAD")
    _require_ok(full, "full HEAD")
    return {
        "root": root,
        "repo": clone,
        "base": short.stdout.strip(),
        "head": full.stdout.strip(),
    }


def _run_generator(
    repo: pathlib.Path,
    out: pathlib.Path,
    base: str,
    *,
    isolated: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [PYTHON_BIN]
    if isolated:
        command.append("-I")
    command.extend(
        [str(GENERATOR_PATH), "--repo", str(repo), "--out", str(out), "--base-commit", base]
    )
    return _run(command, cwd=REPO_ROOT, env=env)


@pytest.fixture(scope="module")
def generated(committed_clone: dict[str, Any]) -> dict[str, Any]:
    out = committed_clone["root"] / "normal-manifest.json"
    proc = _run_generator(
        committed_clone["repo"], out, committed_clone["base"], isolated=True
    )
    _require_ok(proc, "정상 생성")
    if proc.stdout.splitlines()[-1:] != ["EXIT=0"]:
        pytest.fail(f"정상 생성 마지막 줄이 EXIT=0이 아니다: {proc.stdout!r}")
    if not out.is_file():
        pytest.fail("정상 생성이 manifest를 만들지 않았다")
    return {"manifest": json.loads(out.read_text(encoding="utf-8")), "proc": proc, "out": out}


def _validate(manifest: dict[str, Any], clone: dict[str, Any]) -> list[str]:
    return validate_manifest_mod.validate_manifest(
        manifest,
        expected_check_ids=set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS),
        required_base_commit=clone["base"],
        required_tree_head=clone["head"],
    )


def _ids(violations: list[str]) -> set[str]:
    return {line.partition(":")[0] for line in violations}


def test_normal_generation_manifest(
    committed_clone: dict[str, Any], generated: dict[str, Any]
) -> None:
    manifest = generated["manifest"]
    assert len(manifest["cells"]) == 8190
    assert manifest["expected_counts"] == EXPECTED_COUNTS
    exception = manifest["exceptions"][0]
    assert exception["cell_count"] == 2048 == len(exception["cells"])
    assert set(manifest["check_ids"]) == set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS)
    assert os.path.commonpath(
        (os.path.realpath(manifest["provenance"]["read_module"]), str(committed_clone["repo"]))
    ) == str(committed_clone["repo"])
    assert _validate(manifest, committed_clone) == []

    predicate_cells = set()
    for mask in range(1, 1 << 12):
        for repeated in (0, 1):
            if eval(
                exception["predicate"],
                {"__builtins__": {}},
                {"mask": mask, "repeated": repeated, "check_ids": manifest["check_ids"]},
            ):
                predicate_cells.add(f"{mask}:{repeated}")
    assert predicate_cells == set(exception["cells"])


def test_canonical_literals_are_byte_identical() -> None:
    assert generate_mod.CELL_KEY == validate_manifest_mod.CELL_KEY
    assert generate_mod.GENERATION_COMMAND == validate_manifest_mod.GENERATION_COMMAND
    assert generate_mod.GENERATION_COMMAND.splitlines() == [
        'set -euo pipefail; MAIN="${MAIN:-/home/laptop/projects/patent-docent}"; BASE="${BASE:-99fad78}"; OUT_PATH="${OUT_PATH:-$MAIN/tests/fixtures/read-failure-grid/manifest.json}"; PYTHON_BIN="${PYTHON_BIN:-$MAIN/.venv/bin/python}"; cd "$MAIN"',
        'git diff --quiet "$BASE" HEAD -- engine contracts reader',
        'TMP="$(mktemp -d /tmp/pd-golden-XXXXXX)"; trap \'git -C "$MAIN" worktree remove --force "$TMP" >/dev/null 2>&1 || true\' EXIT',
        'git worktree add --detach "$TMP" "$BASE"',
        'OUT="$("$PYTHON_BIN" -I "$MAIN/tests/fixtures/read-failure-grid/generate.py" --repo "$TMP" --out "$OUT_PATH" --base-commit "$BASE" | tee /dev/stderr)"; test "${OUT##*$\'\\n\'}" = "EXIT=0"',
    ]
    assert generate_mod.CELL_KEY == (
        "<mask 10진>:<repeated 0|1> — mask 의 비트 i(LSB=0) 가 1 이면 "
        "이 파일의 check_ids[i] ∈ 실패 집합"
    )


def test_public_subprocess_command(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    out = tmp_path / "public-manifest.json"
    proc = _run_generator(committed_clone["repo"], out, committed_clone["base"], isolated=True)
    _require_ok(proc, "공개 python -I 생성 명령")
    assert proc.stdout.splitlines()[-1] == "EXIT=0"
    assert out.is_file()
    assert _validate(json.loads(out.read_text(encoding="utf-8")), committed_clone) == []


def test_isolated_and_plain_modes(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    isolated_out = tmp_path / "isolated.json"
    isolated = _run_generator(
        committed_clone["repo"], isolated_out, committed_clone["base"], isolated=True
    )
    _require_ok(isolated, "isolated 실행")
    assert "isolated 모드가 아니다" not in isolated.stderr

    plain_out = tmp_path / "plain.json"
    plain = _run_generator(
        committed_clone["repo"], plain_out, committed_clone["base"], isolated=False
    )
    _require_ok(plain, "plain 실행")
    assert plain.stdout.splitlines()[-1] == "EXIT=0"
    assert plain.stderr.splitlines() == [
        "경고: isolated 모드가 아니다; 공개 생성은 python -I를 사용해야 한다"
    ]


def _fixed_beta_matches(manifest: dict[str, Any]) -> bool:
    check_ids = manifest["check_ids"]
    bit = check_ids.index("read.convergence")
    fixed = {f"{mask}:1" for mask in range(1, 1 << 12) if (mask >> bit) & 1}
    exception = manifest["exceptions"][0]
    return exception["cell_count"] == len(fixed) and set(exception["cells"]) == fixed


def test_beta_marker_self_consistent_tamper_fails_fixed_expression(
    generated: dict[str, Any]
) -> None:
    tampered = copy.deepcopy(generated["manifest"])
    exception = tampered["exceptions"][0]
    exception["predicate"] = exception["predicate"].replace("read.convergence", "read.schema")
    schema_bit = tampered["check_ids"].index("read.schema")
    exception["cells"] = [
        f"{mask}:1" for mask in range(1, 1 << 12) if (mask >> schema_bit) & 1
    ]
    exception["cell_count"] = len(exception["cells"])
    assert not _fixed_beta_matches(tampered)


def _set_top(key: str, value: Any) -> Callable[[Any], None]:
    return lambda manifest: manifest.__setitem__(key, value)


def _set_exception(key: str, value: Any) -> Callable[[Any], None]:
    return lambda manifest: manifest["exceptions"][0].__setitem__(key, value)


def _set_provenance(key: str, value: Any) -> Callable[[Any], None]:
    return lambda manifest: manifest["provenance"].__setitem__(key, value)


def _count_mutations() -> list[tuple[str, Callable[[Any], None]]]:
    rows: list[tuple[str, Callable[[Any], None]]] = []
    for slug, key in validate_manifest_mod.COUNT_KEY_SLUGS.items():
        rows.append(
            (
                f"expected_counts.{slug}.type",
                lambda manifest, count_key=key: manifest["expected_counts"].__setitem__(
                    count_key, float(manifest["expected_counts"][count_key])
                ),
            )
        )
    for slug, key in validate_manifest_mod.COUNT_KEY_SLUGS.items():
        rows.append(
            (
                f"expected_counts.{slug}.eq",
                lambda manifest, count_key=key: manifest["expected_counts"].__setitem__(
                    count_key, manifest["expected_counts"][count_key] - 1
                ),
            )
        )
    return rows


def _replace_comment(marker: str) -> Callable[[Any], None]:
    return lambda manifest: manifest.__setitem__("$comment", manifest["$comment"].replace(marker, ""))


def _duplicate_exception(manifest: dict[str, Any]) -> None:
    manifest["exceptions"].append(copy.deepcopy(manifest["exceptions"][0]))


def _duplicate_check_id(manifest: dict[str, Any]) -> None:
    manifest["check_ids"].append(manifest["check_ids"][0])


def _ghost_check_id(manifest: dict[str, Any]) -> None:
    index = manifest["check_ids"].index("read.schema")
    manifest["check_ids"][index] = "read.__ghost__"


def _duplicate_beta_cell(manifest: dict[str, Any]) -> None:
    manifest["exceptions"][0]["cells"].append(manifest["exceptions"][0]["cells"][0])


def _schema_beta_cells(manifest: dict[str, Any]) -> None:
    bit = manifest["check_ids"].index("read.schema")
    manifest["exceptions"][0]["cells"] = [
        f"{mask}:1" for mask in range(1, 1 << 12) if (mask >> bit) & 1
    ]


def _bad_cell_keys(manifest: dict[str, Any]) -> None:
    del manifest["cells"]["1024:1"]
    manifest["cells"]["0:1"] = "StageError"


TV_MUTATIONS: list[tuple[str, Callable[[Any], None]]] = [
    ("manifest.type", lambda box: box.__setitem__("manifest", [])),
    ("top.keys.exact", lambda manifest: manifest.__setitem__("extra", None)),
    ("comment.type", _set_top("$comment", 1)),
    ("comment.contains.T26", _replace_comment("T26 §3 ②")),
    ("comment.contains.T28", _replace_comment("T28")),
    ("comment.contains.T29", _replace_comment("T29")),
    ("base_commit.eq", _set_top("base_commit", "99fad79")),
    ("generator.eq", _set_top("generator", "tests/fixtures/read-failure-grid/generate.px")),
    ("generation_command.eq", lambda manifest: manifest.__setitem__("generation_command", manifest["generation_command"] + "x")),
    ("check_ids.type", _set_top("check_ids", {})),
    ("check_ids.items.str", lambda manifest: manifest["check_ids"].__setitem__(0, 7)),
    ("check_ids.items.nonempty", lambda manifest: manifest["check_ids"].__setitem__(0, "")),
    ("check_ids.unique", _duplicate_check_id),
    ("check_ids.expected_set", _ghost_check_id),
    ("cell_key.eq", lambda manifest: manifest.__setitem__("cell_key", manifest["cell_key"] + "x")),
    ("expected_counts.type", _set_top("expected_counts", [])),
    ("expected_counts.keys.exact", lambda manifest: manifest["expected_counts"].__setitem__("extra", 0)),
    *_count_mutations(),
    ("exceptions.type", _set_top("exceptions", {})),
    ("exceptions.len1", _duplicate_exception),
    ("exception.item.type", _set_top("exceptions", [17])),
    ("exception.keys.exact", lambda manifest: manifest["exceptions"][0].__setitem__("extra", None)),
    ("exception.id.eq", _set_exception("id", "T28-alpha")),
    ("exception.rule.eq", _set_exception("rule", "read.schema …")),
    ("exception.predicate.eq", lambda manifest: manifest["exceptions"][0].__setitem__("predicate", manifest["exceptions"][0]["predicate"] + "x")),
    ("exception.meaning.eq", _set_exception("meaning", 17)),
    ("exception.cell_count.type", _set_exception("cell_count", 2048.0)),
    ("exception.cell_count.eq", _set_exception("cell_count", 2047)),
    ("exception.cells.type", _set_exception("cells", {})),
    ("exception.cells.items.str", lambda manifest: manifest["exceptions"][0]["cells"].__setitem__(0, 1)),
    ("exception.cells.items.nonempty", lambda manifest: manifest["exceptions"][0]["cells"].__setitem__(0, "")),
    ("exception.cells.unique", _duplicate_beta_cell),
    ("exception.cells.set", _schema_beta_cells),
    ("cells.type", _set_top("cells", [])),
    ("cells.keys.exact", _bad_cell_keys),
    ("cells.value.type", lambda manifest: manifest["cells"].__setitem__("1024:1", 3)),
    ("cells.value.sentinel", lambda manifest: manifest["cells"].__setitem__("1024:1", "__bogus__")),
    ("cells.value.len2", lambda manifest: manifest["cells"].__setitem__("1024:1", ["halt"])),
    ("cells.value.action_vocab", lambda manifest: manifest["cells"].__setitem__("1024:1", ["retry(1)", None])),
    ("cells.value.label_type", lambda manifest: manifest["cells"].__setitem__("1024:1", ["escalate", 5])),
    ("provenance.type", _set_top("provenance", [])),
    ("provenance.keys.exact", lambda manifest: manifest["provenance"].__setitem__("extra", None)),
    ("provenance.tree_head.eq", _set_provenance("tree_head", 17)),
    ("provenance.read_module.type", _set_provenance("read_module", 17)),
    ("provenance.read_module.absolute", _set_provenance("read_module", "relative.py")),
    ("provenance.run_checks_module.type", _set_provenance("run_checks_module", 17)),
    ("provenance.run_checks_module.absolute", _set_provenance("run_checks_module", "relative.py")),
    ("provenance.contract.type", _set_provenance("contract", 17)),
    ("provenance.contract.absolute", _set_provenance("contract", "relative.yaml")),
    ("provenance.out.type", _set_provenance("out", 17)),
    ("provenance.out.absolute", _set_provenance("out", "relative.json")),
    ("provenance.engine_path.type", _set_provenance("engine_path", "/")),
    ("provenance.engine_path.len1", _set_provenance("engine_path", ["/one", "/two"])),
    ("provenance.engine_path.items.str", _set_provenance("engine_path", [17])),
    ("provenance.engine_path.absolute", _set_provenance("engine_path", ["relative"])),
    ("provenance.reader_path.type", _set_provenance("reader_path", "/")),
    ("provenance.reader_path.len1", _set_provenance("reader_path", ["/one", "/two"])),
    ("provenance.reader_path.items.str", _set_provenance("reader_path", [17])),
    ("provenance.reader_path.absolute", _set_provenance("reader_path", ["relative"])),
    ("provenance.generated_at.type", _set_provenance("generated_at", 17)),
    ("provenance.generated_at.iso", _set_provenance("generated_at", "어제")),
]


def test_constraint_ids_equal_tv_table() -> None:
    ids = validate_manifest_mod.CONSTRAINT_IDS
    tv_ids = [constraint_id for constraint_id, _ in TV_MUTATIONS]
    assert isinstance(ids, tuple)
    assert all(isinstance(item, str) for item in ids)
    assert len(ids) == len(set(ids))
    assert len(ids) == len(tv_ids) == len(set(tv_ids))
    assert set(ids) == set(tv_ids)


@pytest.mark.parametrize("constraint_id,mutate", TV_MUTATIONS, ids=[row[0] for row in TV_MUTATIONS])
def test_each_tv_mutation_has_exactly_one_violation(
    constraint_id: str,
    mutate: Callable[[Any], None],
    generated: dict[str, Any],
    committed_clone: dict[str, Any],
) -> None:
    box: dict[str, Any] = {"manifest": copy.deepcopy(generated["manifest"])}
    if constraint_id == "manifest.type":
        mutate(box)
    else:
        mutate(box["manifest"])
    violations = _validate(box["manifest"], committed_clone)
    assert _ids(violations) == {constraint_id}, violations


def _child_clone(source: pathlib.Path, target: pathlib.Path) -> pathlib.Path:
    proc = _run(["git", "clone", "-q", str(source), str(target)])
    _require_ok(proc, f"하위 clone {target.name}")
    return target


def _run_generation_block(
    repo: pathlib.Path, base: str, out: pathlib.Path
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "MAIN": str(repo),
            "BASE": base,
            "OUT_PATH": str(out),
            "PYTHON_BIN": PYTHON_BIN,
        }
    )
    return _run(["bash", "-c", generate_mod.GENERATION_COMMAND], cwd=REPO_ROOT, env=env)


def test_generation_command_block_success(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "success-clone")
    base = _git(repo, "rev-parse", "--short=7", "HEAD").stdout.strip()
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    out = tmp_path / "block-success.json"
    proc = _run_generation_block(repo, base, out)
    _require_ok(proc, "생성 명령 블록 성공 경로")
    assert out.is_file()
    violations = validate_manifest_mod.validate_manifest(
        json.loads(out.read_text(encoding="utf-8")),
        expected_check_ids=set(READ_CHECK_IDS) | set(ENGINE_READ_CHECK_IDS),
        required_base_commit=base,
        required_tree_head=head,
    )
    assert violations == []


def test_generation_command_block_precondition_failure(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "changed-clone")
    engine_file = repo / "engine" / "__init__.py"
    engine_file.write_text(engine_file.read_text(encoding="utf-8") + "\n# B-0 diff probe\n", encoding="utf-8")
    _require_ok(_git(repo, "add", "engine/__init__.py"), "diff probe add")
    _commit(repo, "engine-diff-probe")
    base = _git(repo, "rev-parse", "--short=7", "HEAD~1").stdout.strip()
    out = tmp_path / "precondition.json"
    proc = _run_generation_block(repo, base, out)
    assert proc.returncode != 0
    assert not out.exists()


def test_generation_command_block_generator_failure_cleans_worktree(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "missing-out-clone")
    base = _git(repo, "rev-parse", "--short=7", "HEAD").stdout.strip()
    out = tmp_path / "does-not-exist" / "manifest.json"
    proc = _run_generation_block(repo, base, out)
    assert proc.returncode != 0
    assert not out.exists()
    listed = _git(repo, "worktree", "list", "--porcelain")
    _require_ok(listed, "실패 뒤 worktree list")
    assert "/tmp/pd-golden-" not in listed.stdout


def test_generation_command_block_diff_error(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "bad-ref-clone")
    out = tmp_path / "bad-ref.json"
    proc = _run_generation_block(repo, "deadbeef0", out)
    assert proc.returncode != 0
    assert not out.exists()


@pytest.mark.parametrize("probe", ["ⓐ", "ⓑ", "ⓔ"])
def test_import_provenance_rejections(
    probe: str, tmp_path: pathlib.Path
) -> None:
    fake = tmp_path / f"fake-{probe}"
    (fake / "engine").mkdir(parents=True)
    (fake / "reader").mkdir()
    out = tmp_path / f"fake-{probe}.json"
    proc = _run_generator(fake, out, "deadbee", isolated=True)
    assert proc.returncode == 1
    assert probe in proc.stderr
    assert not out.exists()


def test_contract_provenance_rejection(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "no-contract-clone")
    (repo / "contracts" / "stages" / "read.yaml").unlink()
    _require_ok(_git(repo, "add", "contracts/stages/read.yaml"), "contract deletion add")
    _commit(repo, "remove-read-contract-probe")
    base = _git(repo, "rev-parse", "--short=7", "HEAD").stdout.strip()
    out = tmp_path / "no-contract.json"
    proc = _run_generator(repo, out, base, isolated=True)
    assert proc.returncode == 1
    assert "ⓒ" in proc.stderr
    assert not out.exists()


def test_base_commit_provenance_rejection(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    out = tmp_path / "wrong-base.json"
    proc = _run_generator(committed_clone["repo"], out, "deadbee", isolated=True)
    assert proc.returncode == 1
    assert "ⓓ" in proc.stderr
    assert not out.exists()


def test_dirty_tree_provenance_rejection(
    committed_clone: dict[str, Any], tmp_path: pathlib.Path
) -> None:
    repo = _child_clone(committed_clone["repo"], tmp_path / "dirty-clone")
    tracked = repo / "engine" / "__init__.py"
    tracked.write_text(tracked.read_text(encoding="utf-8") + "\n# dirty probe\n", encoding="utf-8")
    base = _git(repo, "rev-parse", "--short=7", "HEAD").stdout.strip()
    out = tmp_path / "dirty.json"
    proc = _run_generator(repo, out, base, isolated=True)
    assert proc.returncode == 1
    assert "ⓕ" in proc.stderr
    assert not out.exists()
