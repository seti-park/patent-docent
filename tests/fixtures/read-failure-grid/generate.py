#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""커밋에 결박된 READ 실패 판정 8,190칸을 manifest로 생성한다."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


GENERATOR = "tests/fixtures/read-failure-grid/generate.py"
GENERATION_COMMAND = r'''set -euo pipefail; MAIN="${MAIN:-/home/laptop/projects/patent-docent}"; BASE="${BASE:-99fad78}"; OUT_PATH="${OUT_PATH:-$MAIN/tests/fixtures/read-failure-grid/manifest.json}"; PYTHON_BIN="${PYTHON_BIN:-$MAIN/.venv/bin/python}"; cd "$MAIN"
git diff --quiet "$BASE" HEAD -- engine contracts reader
TMP="$(mktemp -d /tmp/pd-golden-XXXXXX)"; trap 'git -C "$MAIN" worktree remove --force "$TMP" >/dev/null 2>&1 || true' EXIT
git worktree add --detach "$TMP" "$BASE"
OUT="$("$PYTHON_BIN" -I "$MAIN/tests/fixtures/read-failure-grid/generate.py" --repo "$TMP" --out "$OUT_PATH" --base-commit "$BASE" | tee /dev/stderr)"; test "${OUT##*$'\n'}" = "EXIT=0"'''
CELL_KEY = (
    "<mask 10진>:<repeated 0|1> — mask 의 비트 i(LSB=0) 가 1 이면 "
    "이 파일의 check_ids[i] ∈ 실패 집합"
)
EXCEPTION_PREDICATE = (
    'repeated == 1 and (mask & (1 << check_ids.index("read.convergence"))) != 0'
)


class ProvenanceFailure(Exception):
    """입력 트리가 지정된 커밋의 단일·깨끗한 코드 출처가 아니다."""


def _git(repo: str, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", repo, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ProvenanceFailure(
            f"git {' '.join(args)} 실패(rc={completed.returncode}): {detail}"
        )
    return completed.stdout.strip()


def _under_repo(path: str, repo: str) -> bool:
    try:
        return os.path.commonpath((os.path.realpath(path), repo)) == repo
    except (TypeError, ValueError):
        return False


def _path_entries(package: Any) -> list[str]:
    raw = getattr(package, "__path__", ())
    return [os.path.realpath(item) for item in raw]


def _load_validator() -> Any:
    vm_path = pathlib.Path(__file__).with_name("validate_manifest.py")
    if not vm_path.is_file():
        raise RuntimeError(f"검증기 파일이 없다: {vm_path}")
    spec = importlib.util.spec_from_file_location("validate_manifest", vm_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"검증기 적재 명세를 만들 수 없다: {vm_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--base-commit", default="99fad78")
    return parser.parse_args(argv)


def _build_manifest(args: argparse.Namespace, out: str) -> tuple[dict[str, Any], str, str, dict[str, Any]]:
    repo_arg = args.repo
    repo = os.path.realpath(repo_arg)
    if not os.path.isabs(repo_arg):
        raise ProvenanceFailure(f"--repo 절대경로 검사 실패: 값={repo_arg!r}")
    if "engine" in sys.modules or "reader" in sys.modules:
        raise ProvenanceFailure(
            "사전 import 검사 실패: engine 또는 reader가 sys.modules에 이미 있다"
        )

    sys.path.insert(0, repo)
    try:
        os.chdir(repo)
    except OSError as exc:
        raise ProvenanceFailure(f"repo chdir 검사 실패: 값={repo!r}: {exc}") from exc

    try:
        engine = importlib.import_module("engine")
        read_stage = importlib.import_module("engine.stages.read")
        reader = importlib.import_module("reader")
        run_checks_module = importlib.import_module("reader.lib.run_checks")
        report_module = importlib.import_module("reader.lib.report")
        paths_module = importlib.import_module("engine.paths")
        stages_module = importlib.import_module("engine.stages")
    except Exception as exc:
        raise ProvenanceFailure(
            "provenance 검사 ⓐ/ⓑ/ⓔ import 실패: "
            f"값={type(exc).__name__}: {exc}"
        ) from exc

    failures: list[str] = []
    read_file = os.path.realpath(getattr(read_stage, "__file__", ""))
    if not _under_repo(read_file, repo):
        failures.append(f"ⓐ read_module 값={read_file!r}, repo={repo!r}")
    run_checks_file = os.path.realpath(getattr(run_checks_module, "__file__", ""))
    if not _under_repo(run_checks_file, repo):
        failures.append(f"ⓑ run_checks_module 값={run_checks_file!r}, repo={repo!r}")

    contract_path = os.path.realpath(os.path.join(repo, "contracts", "stages", "read.yaml"))
    if not os.path.isfile(contract_path):
        failures.append(f"ⓒ contract 실재 값={contract_path!r}")

    try:
        tree_head = _git(repo, "rev-parse", "HEAD")
    except ProvenanceFailure as exc:
        failures.append(f"ⓓ tree_head 값={exc}")
        tree_head = ""
    if tree_head and tree_head[:7] != args.base_commit:
        failures.append(
            f"ⓓ base_commit 값=HEAD[:7]={tree_head[:7]!r}, --base-commit={args.base_commit!r}"
        )

    engine_path = _path_entries(engine)
    reader_path = _path_entries(reader)
    if len(engine_path) != 1 or not all(_under_repo(item, repo) for item in engine_path):
        failures.append(f"ⓔ engine.__path__ 값={engine_path!r}, repo={repo!r}")
    if len(reader_path) != 1 or not all(_under_repo(item, repo) for item in reader_path):
        failures.append(f"ⓔ reader.__path__ 값={reader_path!r}, repo={repo!r}")

    try:
        status = _git(repo, "status", "--porcelain")
    except ProvenanceFailure as exc:
        failures.append(f"ⓕ status 값={exc}")
        status = ""
    if status:
        failures.append(f"ⓕ status --porcelain 값={status!r}")

    if failures:
        raise ProvenanceFailure("; ".join(failures))

    contract = paths_module.load_stage_contract("read", repo)
    check_ids = list(run_checks_module.READ_CHECK_IDS + read_stage.ENGINE_READ_CHECK_IDS)
    cells: dict[str, Any] = {}
    counts = {
        "halt/null": 0,
        "escalate/null": 0,
        "escalate/국면 간 변이 재현 — 코드 결함 의심": 0,
        "StageError": 0,
        "total": 0,
    }
    beta_cells: list[str] = []

    for mask in range(1, 1 << len(check_ids)):
        failing = [
            report_module.CheckRow(check_id=check_id)
            for bit, check_id in enumerate(check_ids)
            if mask & (1 << bit)
        ]
        for repeated_int in (0, 1):
            key = f"{mask}:{repeated_int}"
            try:
                action, label = read_stage._failure_verdict(
                    contract, failing, repeated=bool(repeated_int)
                )
                value: Any = [action, label]
                bucket = f"{action}/{'null' if label is None else label}"
            except stages_module.StageError:
                value = "StageError"
                bucket = "StageError"
            cells[key] = value
            if bucket not in counts:
                raise RuntimeError(f"계수 어휘에 없는 판정: {bucket!r} at {key}")
            counts[bucket] += 1
            counts["total"] += 1
            if eval(
                EXCEPTION_PREDICATE,
                {"__builtins__": {}},
                {"repeated": repeated_int, "mask": mask, "check_ids": check_ids},
            ):
                beta_cells.append(key)

    manifest = {
        "$comment": (
            "재정 T26 §3 ② 「오늘의 표 불변」의 정답지 — 값 표이지 도달성 표가 아니다 · "
            "exceptions 표지는 T28 §3 ② 술어에만 · 생성 절차는 T29를 따른다"
        ),
        "base_commit": args.base_commit,
        "provenance": {
            "tree_head": tree_head,
            "read_module": read_file,
            "run_checks_module": run_checks_file,
            "contract": contract_path,
            "engine_path": engine_path,
            "reader_path": reader_path,
            "out": out,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "generator": GENERATOR,
        "generation_command": GENERATION_COMMAND,
        "check_ids": check_ids,
        "cell_key": CELL_KEY,
        "expected_counts": counts,
        "exceptions": [
            {
                "id": "T28-beta",
                "rule": (
                    "read.convergence ∈ 출구 실패 집합 → 재디스패치 0회 "
                    "(재정 T28 ⒟ · §3 ②)"
                ),
                "predicate": EXCEPTION_PREDICATE,
                "meaning": "값은 그대로 · 출구 경로에서 도달 불능 표지",
                "cell_count": len(beta_cells),
                "cells": beta_cells,
            }
        ],
        "cells": cells,
    }
    return manifest, tree_head, read_file, contract


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    out = os.path.realpath(args.out)
    if not sys.flags.isolated:
        print("경고: isolated 모드가 아니다; 공개 생성은 python -I를 사용해야 한다", file=sys.stderr)
    try:
        manifest, tree_head, read_file, contract = _build_manifest(args, out)
        validator = _load_validator()
        violations = validator.validate_manifest(
            manifest,
            expected_check_ids={entry["id"] for entry in contract["checks_before_exit"]},
            required_base_commit=args.base_commit,
            required_tree_head=tree_head,
        )
        if violations:
            for violation in violations:
                print(f"manifest 검증 실패: {violation}", file=sys.stderr)
            print("EXIT=1")
            return 1
        with open(out, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
    except ProvenanceFailure as exc:
        print(f"provenance 실패: {exc}", file=sys.stderr)
        print("EXIT=1")
        return 1
    except Exception as exc:
        print(f"내부 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("EXIT=2")
        return 2

    print(
        f"tree={tree_head} out={out} read_file={read_file} "
        f"cells={len(manifest['cells'])} beta={manifest['exceptions'][0]['cell_count']}"
    )
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
