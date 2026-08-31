# -*- coding: utf-8 -*-
"""M1 합성 코퍼스 관문의 **상설화**.

`tools/check_validator_enforcement.py` 는 커밋 전 관문이지만, 사람이 손으로 돌리는 관문은
돌리지 않으면 없는 것과 같다. 이 파일은 그 도구를 pytest 로 묶어 **매 스위트 실행에서**
재확인한다 — M0.6 재감수가 "표본은 전부 데이터로 존재하나 이를 돌리는 실행기가 없다"를
결함으로 판정한 바로 그 자리다(잔여 목록 19번).

여기서 `assert` 를 쓰는 것은 무방하다(pytest 는 AST 재작성으로 assert 를 if/raise 로 바꾸므로
`python3 -O` 에서도 사라지지 않는다). 다만 **서브프로세스의 종료 코드는 명시 비교**로 본다 —
그것이 이 리포가 요구하는 검증 서식이다(SPEC §8.3 2항).
"""

from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tools", "check_validator_enforcement.py")
CORPUS = os.path.join(REPO, "tests", "fixtures", "reader")


def _run(args: list[str], *, optimize: bool = False) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if optimize:
        env["PYTHONOPTIMIZE"] = "1"
    env["PYTHONPATH"] = REPO + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, TOOL, *args],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_corpus_directory_is_not_empty():
    """코퍼스가 비어 있으면 아래 모든 판정이 공허하게 통과한다 — 이 리포가 반복해서 벌해 온 결함의 형태다."""
    invalid = os.path.join(CORPUS, "invalid")
    assert os.path.isdir(invalid), f"변조본 디렉터리가 없다: {invalid}"
    entries = [n for n in os.listdir(invalid) if n.endswith((".json", ".md"))]
    assert len(entries) >= 20, f"변조본이 {len(entries)}건뿐이다 — 하한 20"


def test_validator_enforcement_gate_passes():
    """검증기가 합성 코퍼스의 변조본을 **정확히 선언된 검사만으로** 잡지 못하면, N14의 '구현으로 해소'가 주장에 그친다."""
    proc = _run([])
    if proc.returncode != 0:
        pytest.fail(
            f"check_validator_enforcement.py 종료 코드 {proc.returncode} (기대 0)\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )


def test_validator_enforcement_gate_is_identical_under_optimize():
    """`python3 -O` 에서 판정이 달라지면 그 도구는 최적화 모드에서 공허 통과하는 것이다(SPEC §8.3 4항)."""
    plain = _run([])
    optimized = _run([], optimize=True)
    if plain.returncode != optimized.returncode:
        pytest.fail(
            f"종료 코드 불일치: python3={plain.returncode} · python3 -O={optimized.returncode}\n"
            f"--- -O stderr ---\n{optimized.stderr}"
        )


def test_baseline_block_reports_every_check():
    """기준선 블록이 검사를 하나라도 빠뜨리면 '무변조가 전부 통과한다'는 주장이 부분 주장이 된다."""
    proc = _run(["--json"])
    if proc.returncode != 0:
        pytest.fail(f"도구 실패(exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    import json

    payload = json.loads(proc.stdout)
    rows = payload["baseline"]["checks"]
    ids = [row["check_id"] for row in rows]
    assert len(ids) == len(set(ids)), f"판정 행이 중복되었다: {ids}"

    sys.path.insert(0, REPO)
    from reader.lib import run_checks  # noqa: PLC0415

    expected = set(run_checks.READ_CHECK_IDS) | set(run_checks.FREEZE_CHECK_IDS)
    assert set(ids) == expected, f"기준선이 덮지 않은 검사: {sorted(expected - set(ids))}"


def test_no_baseline_check_is_vacuous():
    """대상 0건으로 통과한 검사가 기준선에 있으면, 그 검사는 코퍼스에 대해 아무것도 반증하지 않는다(재정 N5)."""
    proc = _run(["--json"])
    import json

    payload = json.loads(proc.stdout)
    vacuous = payload["baseline"]["vacuous"]
    assert not vacuous, f"공허 날인된 기준선 검사: {vacuous}"


def test_requirements_table_cites_only_evidence_that_exists():
    """요구사항표가 없는 테스트를 반증 근거로 적으면, N14 ②의 "구현으로 해소" 실증이 이름뿐이 된다.

    ★ 실제로 일어났다. 총괄이 `docs/SPEC.md` §8.4 M1 요구사항표를 쓰면서 반증 테스트 3건을
    **실재하지 않는 이름**으로 적었고(기능은 다른 이름으로 덮여 있었다), sol 재감수 발주 직후
    자기 점검에서야 드러났다. 재정 N14 ②가 종결 요건으로 지목한 바로 그 표에서 일어난
    일이므로, 표를 실물에 묶는 것이 이 테스트의 임무다.

    M0.6 재감수가 벌한 "강제의 범위를 실제보다 넓게 말한 것"과 같은 층의 결함이다 —
    이번에는 강제가 아니라 **증거**의 범위였다.

    ★ 인용에는 두 종류가 있다(2026-08-18). 하나는 **증거**로 지목한 이름이고, 다른 하나는
    개명 이력을 밝히려고 적은 **구 이름**(`구 \\`test_...\\`` 서식)이다. 둘을 같은 규칙으로
    보면 개명 이력을 적는 순간 표가 자기 자신을 위반하게 되므로, 방향을 반대로 건다 —
    증거는 **실재해야** 하고 구 이름은 **실재하지 않아야** 한다. 후자가 남아 있으면 개명이
    끝나지 않았거나 표의 서술이 사실과 다른 것이다.
    """
    spec = open(os.path.join(REPO, "docs", "SPEC.md"), encoding="utf-8").read()
    start = spec.find("##### M1 요구사항표")
    end = spec.find("**M1 관할이 아닌 생존 지적**", start)
    assert start != -1 and end > start, "SPEC 에서 M1 요구사항표 구간을 찾지 못했다"
    block = spec[start:end]

    import json

    retired = set(re.findall(r"구 `(test_[a-z0-9_]+)`", block))
    cited_tests = sorted(set(re.findall(r"`(test_[a-z0-9_]+)`", block)) - retired)
    assert cited_tests, "요구사항표가 반증 테스트를 하나도 지목하지 않는다"
    # `pytest --collect-only` 를 서브프로세스로 부르면 스위트 전체를 두 번 수집하게 되어
    # 실행 시간이 배로 늘고 스위트가 커질수록 나빠진다. 테스트 소스에서 정의를 직접 찾는다.
    defined: set[str] = set()
    for path in sorted(glob.glob(os.path.join(REPO, "tests", "test_*.py"))):
        source = open(path, encoding="utf-8").read()
        defined |= set(re.findall(r"^def (test_[a-z0-9_]+)\(", source, re.MULTILINE))
    missing = [name for name in cited_tests if name not in defined]
    assert not missing, f"요구사항표가 지목한 테스트가 실재하지 않는다: {missing}"

    survivors = sorted(name for name in retired if name in defined)
    assert not survivors, (
        f"표가 개명되었다고 적은 이름이 아직 살아 있다: {survivors} — "
        "개명이 끝나지 않았거나 표의 서술이 사실과 다르다"
    )

    cited_cases = sorted(set(re.findall(r"`(invalid/[a-z0-9.\-]+\.json)`", block)))
    manifest = json.load(
        open(os.path.join(CORPUS, "manifest.json"), encoding="utf-8")
    )
    known = {case["file"] for case in manifest["cases"]}
    absent = [name for name in cited_cases if name not in known]
    assert not absent, f"요구사항표가 지목한 변조본이 코퍼스에 없다: {absent}"


def test_stage_contracts_declare_every_check_the_stage_runs():
    """계약이 모르는 검사는 사후 감사에서 근거 없는 검사가 되고, 계약에만 있는 검사는 공허한 약속이 된다.

    ★ M1 재감수 M-01 적발. `contracts/stages/read.yaml`이 `read.source-digest`를
    `checks_before_exit`에 넣지 않았는데 스테이지는 그것을 실행하고 있었다. 양방향 다
    결함이다 — 선언 없이 도는 검사는 근거가 없고, 돌지 않는 선언은 약속만 있다.

    ★ 대조는 **두 축**이다(2026-08-18 · 재정 P-C·P-4). 이유는 층의 사실이다 — `reader/`는
    이식 단위라 런 작업장(`runs/`)을 보지 못하므로, 파일 지문(`read.input-digest`)과 레인
    왕복 기록(`read.lane-log-shape`)을 보는 검사는 **엔진 소관**이고 `READ_CHECK_IDS`에
    있을 수 없다. 한쪽 축을 느슨하게 만들어 통과시키지 않는다:

      축 1 (이식 단위) `implemented_by`가 `reader/lib/**`인 검사 ⟺ `READ_CHECK_IDS` **양방향 엄격**
      축 2 (엔진 소관) `implemented_by`가 `engine/**`인 검사 — 그 파일이 실재하고 그 안에
                       검사 id 문자열이 있는가(좌표가 유령이면 실패한다)

    `source`·`freeze`는 검사 id가 두 축 어느 쪽으로도 전량 분류되어 있지 않아 같은 방식으로
    대조할 대상이 없다 — 그 사실 자체가 남은 공백이며 `D-20260818-03`에 적혀 있다.
    """
    import yaml

    sys.path.insert(0, REPO)
    from reader.lib import run_checks  # noqa: PLC0415

    contract = yaml.safe_load(
        open(os.path.join(REPO, "contracts", "stages", "read.yaml"), encoding="utf-8")
    )
    declared = (contract.get("checks_on_entry") or []) + contract["checks_before_exit"]

    nameless = [entry["id"] for entry in declared if not entry.get("implemented_by")]
    assert not nameless, f"구현 좌표(implemented_by)가 없는 선언: {nameless}"

    portable, engine_side, unknown = [], [], []
    for entry in declared:
        where = str(entry["implemented_by"])
        if where.startswith("reader/lib/"):
            portable.append(entry["id"])
        elif where.startswith("engine/"):
            engine_side.append((entry["id"], where))
        else:
            unknown.append((entry["id"], where))
    # 두 축 어디에도 속하지 않는 층이 생겼는데 시험이 모르는 상태가 가장 위험하다.
    assert not unknown, f"두 축 어디에도 속하지 않는 구현 좌표: {unknown}"

    # -- 축 1 — 이식 단위 검사는 양방향 엄격 대조 --------------------------
    executed = list(run_checks.READ_CHECK_IDS)
    undeclared = [check for check in executed if check not in portable]
    assert not undeclared, f"스테이지가 실행하는데 계약이 선언하지 않은 검사: {undeclared}"
    unexecuted = [check for check in portable if check not in executed]
    assert not unexecuted, f"계약이 선언했는데 스테이지가 실행하지 않는 검사: {unexecuted}"

    # -- 축 2 — 엔진 소관 검사는 좌표의 실재를 본다 ------------------------
    assert engine_side, "엔진 소관 검사가 하나도 없다 — 두 축 대조의 전제가 사라졌다"
    for check_id, where in engine_side:
        path = os.path.join(REPO, *where.split("/"))
        assert os.path.isfile(path), f"{check_id}: 구현 좌표가 실재하지 않는다 — {where}"
        source = open(path, encoding="utf-8").read()
        assert check_id in source, (
            f"{check_id}: {where} 안에 그 검사 id 문자열이 없다 — 좌표가 유령이다"
        )


def test_spec_json_examples_validate_against_their_contracts():
    """스펙의 예시가 계약을 통과하지 못하면, 그 예시를 보고 구현한 코드가 계약을 깬다.

    ★ 실제로 일어났다. §2.6의 `convergence/v0` 예시는 재정 N5가 판정 행 서식을 명한 뒤에도
    **구 형태(검사 이름 키의 객체)로 남아** 계약(배열)과 갈린 채 M1 재감수까지 갔다.
    문서 머리말이 "사본은 반드시 낡는다"고 적어 두었는데 **그 문서 자신이 사본이었다.**

    예시는 계약의 사본이므로, 대조가 없으면 낡는다 — 이 테스트가 그 대조다.
    """
    import json

    from jsonschema import Draft202012Validator

    spec = open(os.path.join(REPO, "docs", "SPEC.md"), encoding="utf-8").read()
    contracts = {
        "convergence/v0": "contracts/schemas/convergence.schema.json",
        "material-spec/v0": "reader/schemas/material-spec.schema.json",
    }
    checked = 0
    for line, rel in contracts.items():
        needle = f'"schema": "{line}"'
        at = spec.find(needle)
        if at == -1:
            continue
        opening = spec.rfind("{", 0, at)
        fence = spec.find("```", at)
        assert opening != -1 and fence > opening, f"{line} 예시의 경계를 찾지 못했다"
        instance = json.loads(spec[opening:fence].strip())
        schema = json.load(open(os.path.join(REPO, rel), encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda err: list(err.path),
        )
        assert not errors, (
            f"§ 예시({line})가 {rel} 을 통과하지 못한다: "
            + "; ".join(f"{list(e.path)} {e.message[:80]}" for e in errors[:3])
        )
        checked += 1
    assert checked == len(contracts), f"검증한 예시가 {checked}건뿐이다 — 예시를 찾지 못했다"


def test_spec_verifier_duty_table_matches_the_schema_comment():
    """§2.8 표와 스키마 `$comment` 목록이 어긋나면, "검증기 몫이 무엇인가"의 정본이 둘로 갈린다.

    SPEC §2.8은 스스로 **"번호와 내용은 정본 스키마 파일의 `$comment` 목록과 일치해야 한다"**고
    적고, 어긋나면 "파일이 정본이고 이 표가 결함"이라는 처분까지 규정한다. 그런데 그 일치를
    **집행하는 것이 없었다** — M1이 스키마에 제약 (12)(13)(14)를 더하면서 표는 11행에
    머물렀고, 요구사항표의 유령 테스트명을 고친 직후 같은 종류를 찾다가 드러났다.

    증거의 좌표가 틀린 자리는 대개 혼자 있지 않다.
    """
    spec = open(os.path.join(REPO, "docs", "SPEC.md"), encoding="utf-8").read()
    start = spec.find("스키마로 표현하지 않고 검증기 코드에 맡기는 제약")
    assert start != -1, "SPEC 에서 §2.8 검증기 몫 표를 찾지 못했다"
    rows = [int(n) for n in re.findall(r"^\| (\d+) \|", spec[start:start + 8000], re.MULTILINE)]

    import json

    schema = json.load(
        open(
            os.path.join(REPO, "reader", "schemas", "material-spec.schema.json"),
            encoding="utf-8",
        )
    )
    declared = sorted({int(n) for n in re.findall(r"\((\d+)\)", schema["$comment"])})

    assert rows == declared, (
        f"§2.8 표 번호 {rows} 와 스키마 $comment 번호 {declared} 가 다르다 — "
        "스키마가 정본이므로 표를 맞춰라(§2.8 자신의 처분 규정)"
    )


def test_glossary_registers_every_check_id():
    """식별자 사전이 검사를 빠뜨리면, 그 검사는 계약이 아니라 관습이 된다.

    `contracts/glossary.md`는 "기계가 문자열로 주고받는 이름들"의 정본이고, 그 파일 스스로
    "등재하지 않은 이름을 코드가 쓰기 시작하면 그 이름은 계약이 아니라 관습이 된다"고 적는다.
    그런데 그 규율을 **집행하는 것이 아무것도 없어서**, M1에서 `read.source-digest`를
    신설하고도 사전에 올리지 않은 채 지나갔다(총괄이 사후에 적발). 기억에 의존하는 규율은
    기억이 실패하는 만큼 실패한다.

    ★ **2026-08-31 확장 — 엔진 소관 검사까지 훑는다(재정 Q1 의 집행).** 구 시험은 이식 단위
    등재부(`CHECK_REGISTRY`)만 보았고, 그래서 **엔진이 발행하는 검사 id 는 사전에서 빠져도
    아무도 울지 않았다.** 재정 2026-08-31 Q1 은 신설 검사를 *"`glossary.md` §2.1 목록과
    `CHECK_REGISTRY` 에 동시에 등재한다(대조를 시험이 집행한다)"* 로 명했는데,
    `CHECK_REGISTRY` 항목은 `CheckContext` 만 받아 파일 시스템을 보지 못하므로 디스크를 읽는
    검사는 그 등재부에 들어갈 수 없다. 그래서 재정이 요구한 **효과**를 자리만 옮겨 세운다 —
    엔진 소관 등재부 `engine.stages.read.ENGINE_READ_CHECK_IDS` 를 같은 대조에 넣었다.
    **재정 문언의 축소가 아니라 확장이다**: 대조가 이제 엔진 검사 전체에 걸린다.
    """
    sys.path.insert(0, REPO)
    from engine.stages.read import ENGINE_READ_CHECK_IDS  # noqa: PLC0415
    from reader.lib import run_checks  # noqa: PLC0415

    doc = open(
        os.path.join(REPO, "contracts", "glossary.md"), encoding="utf-8"
    ).read()
    registered = (
        set(run_checks.READ_CHECK_IDS)
        | set(run_checks.FREEZE_CHECK_IDS)
        | set(ENGINE_READ_CHECK_IDS)
    )
    missing = sorted(check_id for check_id in registered if check_id not in doc)
    assert not missing, f"contracts/glossary.md 에 등재되지 않은 검사 id: {missing}"


def test_every_declared_check_has_a_mutant_except_schema():
    """변조본이 배정되지 않은 검사는 '있다고 적혀 있으나 시험되지 않은 검사'다.

    `read.schema` 만 예외이며 그것은 누락이 아니라 이 코퍼스의 정의다 — 전 변조본이 스키마를
    통과해야 검증기를 시험한 것이 되므로, 스키마가 거부하는 판은 정의상 여기 들어올 수 없다
    (그 몫은 `tests/fixtures/schema-enforcement/`).
    """
    proc = _run(["--json"])
    import json

    payload = json.loads(proc.stdout)
    tally = payload["tally"]
    unexercised = sorted(cid for cid, n in tally.items() if n == 0 and cid != "read.schema")
    assert not unexercised, f"변조본 0건인 검사: {unexercised}"
    assert tally.get("read.schema", 0) == 0, (
        "read.schema 에 변조본이 배정되었다 — 스키마가 잡는 결함은 이 코퍼스의 대상이 아니다"
    )
