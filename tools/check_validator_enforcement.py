#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""검증기 집행 실증 도구 — **검증기 코드가 실제로 거부하는가**의 측정.

이 도구가 증명하는 것은 하나다: `reader/lib/` 의 결정론 검사가, 스키마를 **통과한** 무효
인스턴스를 실제로 잡는가. 그 이상은 증명하지 않는다.

관문 4종의 분업 (SPEC §8.3 7항 — 넷째는 재정 2026-08-19 H7 로 승격되었다)
  `check_spec_refs.py`          문서와 계약이 **서로 어긋나지 않는가**(이름·경로·메타)
  `check_schema_enforcement.py` **스키마가** 강제하는 것의 경계는 어디까지인가
  이 도구                        그 경계 **밖에 남은 불변식**을 검증기가 잡는가
  `check_lane_binding.py`       **러너**가 낡은 응답을 실제로 거부하는가(층이 다르다)

넷은 각자 하나의 주장만 증명하며 **하나의 통과는 다른 하나의 증거가 아니다.** 이 분업이
M0.6 재감수의 판정 요지를 그대로 담고 있다 — "강제는 크게 늘었으나 강제의 범위를 실제보다
넓게 말했다". 이 도구의 존재 이유는 재정 2026-08-18 **N14 ②**다: *M1 종결 요건 = sol 재감수에서
해당 항목들이 "구현으로 해소"되었음을 실증.* 감수자는 코드를 실행할 수 없으므로, 실행의
증거를 기계가 재생산 가능한 형태로 남긴다.

무엇을 어떻게 보는가
  1. **기준선** — 무변조 코퍼스(`base/`)가 검사 **12종**(READ 10 + FREEZE 2)을 **전부 통과**한다. 통과하지 못하면
     아래 모든 판정이 무의미하다(과잉 제약이면 변조본도 "당연히" 실패한다).
  2. **변조본** — 각 변조본에 대해 **정확히 선언된 검사만** 실패한다. 실패해야 할 것이
     실패했는가와 **실패하지 말아야 할 것이 통과했는가**를 함께 본다. 후자가 없으면
     "아무거나 다 실패시키는 검사"도 만점을 받는다.
     ★ 여기에 **상신 축**이 한 겹 더 붙는다(재정 2026-08-18 **P-3**). 수렴 축이 세 정책으로
     갈리면서, 어떤 변조본이 증명해야 할 것이 "검사가 실패하는가"에서 "**상신 트리거가
     뜨는가**"로 바뀌었다 — `escalation-trigger` 축의 미달은 판정 행을 `fail` 로 만들지
     않고 `extras["escalations"]` 에만 실린다. manifest 의 선택 필드 `expect_escalate` 가
     그 기대를 데이터로 적고, 이 도구는 **집합 동등**으로 대조한다(초과·부족 둘 다 불일치).
     `expect_fail` 과 한 수로 뭉개지 않는 이유는 P-3 의 정책 차등이 보고에서 사라지지 않게
     하기 위함이다.
  3. **스키마가 일을 대신하지 않았음** — 전 변조본은 `read.schema` 를 **통과**해야 한다.
     스키마가 잡아 버리면 그 케이스는 검증기를 시험한 것이 아니다.
  4. **하한** — 케이스 수와 검사별 배분의 하한을 강제한다. 픽스처가 0건이면 위 1~3이 전부
     공허하게 통과하며, 그것이 이 리포가 반복해서 벌해 온 결함의 형태다(재정 N5의 공허 2종).

★ 자기매칭 격리 (정본: `docs/SPEC.md` §4.8 + SPEC §8.3 8항)
`tools/check_spec_refs.py` 는 `tests/` 를 스캔 목록에서 배제하고 들어오면 exit 2 로 거부한다.
이 도구는 반대로 `tests/fixtures/reader/` 를 **읽는 것이 임무**인데, 그럼에도 자기매칭이
성립하지 않는다. 근거는 `check_schema_enforcement.py` 와 같다.

  1. 이 도구는 **탐지 패턴을 하나도 갖지 않는다.** 판정은 전량 `reader/lib/` 의 검사와
     `reader/reader-rules.yaml` 의 규칙이 내리며, 이 소스는 그 결과를 manifest 의 정답과
     대조할 뿐이다. 패턴이 없으면 자기매칭의 전제가 없다.
  2. **심은 결함 문자열이 이 소스에 리터럴로 없다.** 전부 `tests/fixtures/reader/invalid/`
     의 데이터 파일에 있고, 무엇을 심었는지는 manifest 의 `mutation` 이 데이터로 적는다.
  3. 픽스처는 **피검체이지 법이 아니다.** 법은 계약 파일이다.

종료 코드 (SPEC §8.3 3항):
  0 = 전건 기대 일치 / 1 = 검증 실패(기대와 실제 불일치·하한 미달) / 2 = 입력·환경 오류

`assert` 를 쓰지 않는다(`python3 -O` 에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any

# 코퍼스 위치 — manifest 와 인스턴스가 함께 산다.
FIXTURE_ROOT = "tests/fixtures/reader"
MANIFEST_REL = f"{FIXTURE_ROOT}/manifest.json"

# 케이스 필수 키. `expect_escalate` 는 **선택**이다(재정 P-3) — 상신 축이 없는 변조본이
# 다수이므로 필수로 만들면 39건 전부에 빈 배열을 적게 되고, 그 빈 배열은 아무것도 뜻하지 않는다.
CASE_KEYS: tuple[str, ...] = ("file", "role", "expect_fail", "mutation", "basis", "traces")
ROLES: tuple[str, ...] = ("spec", "peer", "revision", "source")

# 상신 상태 어휘의 정본은 `reader/reader-rules.yaml#convergence.policies[].status_on_miss` 이고,
# 이 상수는 그 값과의 대조용이다. 어느 축이 어느 정책인지는 **규칙 파일이 정하며 이 도구는
# 고르지 않는다** — 고르는 순간 검사 도구가 자기 입법이 된다(D7).
ESCALATE_STATUS = "escalate"

# ★ 데이터로 낮출 수 없는 하드 하한. manifest 의 floors 는 이보다 **높게만** 설정할 수 있다.
#   하한을 전부 데이터에 두면 "픽스처를 지우고 하한도 함께 낮추는" 경로가 열린다.
ABSOLUTE_MIN_CASES = 20
ABSOLUTE_MIN_PER_CHECK = 1

EPILOG = """\
하는 일:
  ① 무변조 코퍼스가 검사 12종을 전부 통과하는지 (기준선 — 과잉 제약의 반증)
  ② 각 변조본에서 **정확히** 선언된 검사만 실패하는지 (관할의 증명)
     + manifest 의 expect_escalate 와 **정확히 같은 수렴 축만** 상신되는지 (재정 P-3)
  ③ 전 변조본이 read.schema 를 통과하는지 (스키마가 일을 대신하지 않았음)
  ④ 케이스 수·검사별 배분이 하한 이상인지 (픽스처 0건 공허 통과 봉쇄)
     — 상신 케이스는 **따로** 센다(실패와 상신을 한 수로 뭉개면 P-3 의 정책 차등이 사라진다)

★ 이 도구가 증명하는 것은 "검증기가 거부하는 것"뿐이다:
  계약이 옳은지도, 스키마가 강제하는지도 증명하지 않는다. 그 둘은 각각
  check_spec_refs.py 와 check_schema_enforcement.py 의 몫이며, 셋의 통과는 서로의 증거가 아니다.

종료 코드: 0 전건 일치 / 1 검증 실패 / 2 입력·환경 오류
"""


def fail_env(message: str) -> None:
    """입력·환경 오류로 즉시 종료한다(exit 2)."""
    print(f"ENVIRONMENT ERROR: {message}", file=sys.stderr)
    sys.exit(2)


@dataclass
class Case:
    file: str
    role: str
    expect_fail: tuple[str, ...]
    mutation: str
    basis: str
    traces: tuple[str, ...]
    expect_escalate: tuple[str, ...] = ()  # 상신이 뜨기를 기대하는 수렴 축 id (재정 P-3)


@dataclass
class Outcome:
    case: Case
    actual_fail: tuple[str, ...]
    schema_ok: bool
    rule_ids: tuple[str, ...] = ()
    actual_escalate: tuple[str, ...] = ()
    extras_conflict: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        if self.error:
            return False
        if set(self.actual_fail) != set(self.case.expect_fail):
            return False
        # ★ 상신 축 대조(재정 P-3). **집합 동등**이다 — 부족(뜨지 않았다)은 물론 초과(선언하지
        #   않은 축이 떴다)도 불일치로 낸다. 초과를 눈감으면 "아무 축이나 다 상신하는 검사"가
        #   만점을 받으며, 그것은 expect_fail 을 초과 실패로 잡는 이유와 정확히 같은 이유다.
        if set(self.actual_escalate) != set(self.case.expect_escalate):
            return False
        # 같은 사실이 두 자리(escalations[] · axes[].status)에 적히므로 서로 어긋나면 실측을
        # 신뢰할 수 없다. 어긋남 자체가 결함이다.
        if self.extras_conflict:
            return False
        # read.schema 가 기대 목록에 없는데 실제로 실패했다면 위에서 이미 걸린다.
        # 여기서 보는 것은 "스키마가 조용히 일을 대신했는가"이며, 그 경우 schema_ok 가 False 다.
        return self.schema_ok or "read.schema" in self.case.expect_fail


@dataclass
class Baseline:
    read_rows: list = field(default_factory=list)
    freeze_rows: list = field(default_factory=list)

    @property
    def failures(self) -> list[str]:
        return [r.check_id for r in (self.read_rows + self.freeze_rows) if r.status != "pass"]


def load_json(path: str, label: str) -> Any:
    if not os.path.isfile(path):
        fail_env(f"{label} 파일이 없다: {path}")
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail_env(f"{label} 파일을 읽을 수 없다: {path} — {exc}")
    return None  # pragma: no cover - fail_env 가 이미 종료한다


def load_text(path: str, label: str) -> str:
    if not os.path.isfile(path):
        fail_env(f"{label} 파일이 없다: {path}")
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        fail_env(f"{label} 파일을 읽을 수 없다: {path} — {exc}")
    return ""  # pragma: no cover


def load_manifest(repo: str, check_ids: frozenset[str]) -> tuple[dict, list[Case], dict]:
    data = load_json(os.path.join(repo, MANIFEST_REL), "manifest")
    if not isinstance(data, dict):
        fail_env(f"manifest 형식 오류(객체 아님) — {MANIFEST_REL}")

    base = data.get("base")
    if not isinstance(base, dict):
        fail_env(f"manifest 에 base 객체가 없다 — {MANIFEST_REL}")
    for key in ("source", "spec", "peer", "revision"):
        if not isinstance(base.get(key), str):
            fail_env(f"manifest.base.{key} 가 없거나 문자열이 아니다")

    floors = data.get("floors")
    if not isinstance(floors, dict):
        # 하한 선언이 없으면 하드 하한만 적용하되, 그 사실을 드러낸다.
        floors = {}

    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list):
        fail_env(f"manifest 에 cases 배열이 없다 — {MANIFEST_REL}")

    cases: list[Case] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_cases):
        where = f"{MANIFEST_REL} cases[{index}]"
        if not isinstance(raw, dict):
            fail_env(f"{where} 가 객체가 아니다")
        missing = [k for k in CASE_KEYS if k not in raw]
        if missing:
            fail_env(f"{where} 에 필수 키가 없다: {', '.join(missing)}")
        if raw["role"] not in ROLES:
            fail_env(f"{where}.role 이 {ROLES} 밖의 값이다: {raw['role']!r}")
        expect = raw["expect_fail"]
        if not isinstance(expect, list):
            fail_env(f"{where}.expect_fail 은 배열이어야 한다")
        unknown = [c for c in expect if c not in check_ids]
        if unknown:
            fail_env(f"{where}.expect_fail 에 알 수 없는 검사 id: {', '.join(unknown)}")
        escalate = raw.get("expect_escalate", [])
        if not isinstance(escalate, list) or any(not isinstance(a, str) for a in escalate):
            fail_env(f"{where}.expect_escalate 는 수렴 축 id 의 배열이어야 한다(선택 필드)")
        # ★ 빈 expect_fail 의 면제 조건(재정 P-3). `escalation-trigger` 축의 미달은 판정 행을
        #   fail 로 만들지 않으므로 "상신만 뜨는" 변조본이 정상으로 존재한다. 그러나 **둘 다
        #   비면** 그 변조본은 아무것도 증명하지 않는 파일이므로 여전히 입력 오류다 — 면제는
        #   expect_escalate 가 비어 있지 않을 때에 한한다.
        if not expect and not escalate:
            fail_env(
                f"{where}.expect_fail 과 expect_escalate 가 둘 다 비어 있다 — "
                "아무것도 증명하지 않는 변조본은 등재할 수 없다"
            )
        if not isinstance(raw["traces"], list) or not raw["traces"]:
            fail_env(f"{where}.traces 는 비어 있지 않은 배열이어야 한다(문서 근거 없는 케이스 금지)")
        if raw["file"] in seen:
            fail_env(f"{where}.file 이 중복 등재되었다: {raw['file']}")
        seen.add(raw["file"])
        cases.append(
            Case(
                file=raw["file"],
                role=raw["role"],
                expect_fail=tuple(expect),
                mutation=str(raw["mutation"]),
                basis=str(raw["basis"]),
                traces=tuple(str(t) for t in raw["traces"]),
                expect_escalate=tuple(str(a) for a in escalate),
            )
        )
    if not cases:
        fail_env(f"manifest 에 케이스가 하나도 없다 — {MANIFEST_REL}")
    return base, cases, floors


def check_manifest_covers_disk(repo: str, cases: list[Case]) -> None:
    """디스크의 변조본이 전부 manifest 에 등재되었는지 확인한다.

    미등재 픽스처는 집행 증명에 뚫린 구멍이므로 검증 실패가 아니라 입력 오류로 다룬다.
    """
    listed = {c.file for c in cases}
    directory = os.path.join(repo, FIXTURE_ROOT, "invalid")
    if not os.path.isdir(directory):
        fail_env(f"변조본 디렉터리가 없다: {FIXTURE_ROOT}/invalid")
    found = [
        f"invalid/{name}"
        for name in sorted(os.listdir(directory))
        if name.endswith(".json") or name.endswith(".md")
    ]
    orphans = [rel for rel in found if rel not in listed]
    if orphans:
        fail_env("manifest 에 등재되지 않은 변조본이 있다(집행 증명의 구멍): " + ", ".join(orphans))
    if not found:
        fail_env(f"{FIXTURE_ROOT}/invalid 에 변조본이 하나도 없다 — 코퍼스가 비어 있으면 이 도구는 아무것도 증명하지 않는다")


def escalatable_axes(rules) -> dict[str, dict]:
    """축 id → 정책. 계약이 정한 대응을 그대로 옮길 뿐 이 도구가 축을 고르지 않는다(D7).

    반환은 **전 축**이며, 상신을 낼 수 있는 축인지는 정책의 `status_on_*` 로 판별한다
    (`measure-only` 는 pass·miss 어느 쪽도 `escalate` 가 아니다 — 재정 P-3).
    """
    table: dict[str, dict] = {}
    for axis in rules.convergence_axes:
        axis_id = axis.get("id")
        if axis_id is None:
            continue
        table[str(axis_id)] = rules.policy_of(axis) or {}
    return table


def policy_can_escalate(policy: dict) -> bool:
    return ESCALATE_STATUS in (
        str(policy.get("status_on_pass")),
        str(policy.get("status_on_miss")),
    )


def validate_escalate_declarations(cases: list[Case], axis_policies: dict[str, dict]) -> None:
    """`expect_escalate` 의 축 id 가 실재하며 **상신을 낼 수 있는 정책**인지 확인한다.

    판정하지 않는 축(`measure-only`)이나 미달이 곧 실패인 축(`exact-match`)에 상신을 기대하는
    것은 계약 오독이며, 그런 선언은 영원히 충족될 수 없다. 미충족을 케이스 불일치로만 내면
    "고치면 통과하는 문제"처럼 보이지만 실제로는 **선언이 성립하지 않는다** — 그래서 검증
    실패(1)가 아니라 입력 오류(2)로 다룬다. 알 수 없는 검사 id 를 다루는 방식과 같다.
    """
    for case in cases:
        for axis_id in case.expect_escalate:
            policy = axis_policies.get(axis_id)
            if policy is None:
                fail_env(
                    f"{MANIFEST_REL} {case.file}.expect_escalate 에 알 수 없는 수렴 축 id: "
                    f"{axis_id} (계약 = reader-rules.yaml#convergence.axes)"
                )
            if not policy_can_escalate(policy):
                fail_env(
                    f"{MANIFEST_REL} {case.file}.expect_escalate 의 축 {axis_id} 는 "
                    f"policy={policy.get('id')} 라 상신을 내지 않는다 — 판정하지 않거나 "
                    "실패로 처분하는 축에 상신을 기대하는 것은 계약 오독이다(재정 P-3)"
                )


def collect_escalations(rows: list) -> tuple[tuple[str, ...], str]:
    """판정 행에서 **상신 실측**을 모은다(재정 P-3).

    정본은 `row.extras["escalations"]`(`reader/lib/convergence.py` 가 채운다)이고, 같은 사실이
    `row.extras["axes"][].status == "escalate"` 에도 적힌다. 한쪽만 읽으면 다른 한쪽이 조용히
    어긋나도 모르므로 **둘을 대조**하고, 어긋나면 그 사실을 문자열로 돌려준다.
    """
    listed: set[str] = set()
    marked: set[str] = set()
    malformed: list[str] = []
    for row in rows:
        extras = getattr(row, "extras", None) or {}
        for entry in extras.get("escalations") or []:
            if isinstance(entry, dict) and entry.get("axis") is not None:
                listed.add(str(entry["axis"]))
            else:
                malformed.append(f"{row.check_id}: {entry!r}")
        for axis in extras.get("axes") or []:
            if isinstance(axis, dict) and str(axis.get("status")) == ESCALATE_STATUS:
                marked.add(str(axis.get("id")))
    notes: list[str] = []
    if malformed:
        notes.append("escalations[] 원소에 axis 가 없다: " + ", ".join(malformed))
    if listed != marked:
        notes.append(
            f"escalations[]={sorted(listed) or '(없음)'} 와 "
            f"axes[].status=escalate {sorted(marked) or '(없음)'} 가 어긋난다"
        )
    return tuple(sorted(listed)), " · ".join(notes)


def enforce_floors(cases: list[Case], floors: dict, check_ids: tuple[str, ...], exempt: frozenset[str]) -> list[str]:
    """하한 미달 목록을 반환한다(빈 목록 = 통과).

    하한을 데이터에만 두면 픽스처와 함께 하한도 낮추는 경로가 열리므로, 하드 하한과
    manifest 선언 중 **높은 쪽**을 적용한다.
    """
    findings: list[str] = []
    declared_min = floors.get("min_cases")
    min_cases = max(ABSOLUTE_MIN_CASES, declared_min if isinstance(declared_min, int) else 0)
    if len(cases) < min_cases:
        findings.append(f"케이스 수 {len(cases)} < 하한 {min_cases}")

    declared_per = floors.get("per_check_min")
    per_check = max(ABSOLUTE_MIN_PER_CHECK, declared_per if isinstance(declared_per, int) else 0)
    tally: dict[str, int] = {cid: 0 for cid in check_ids}
    for case in cases:
        for cid in case.expect_fail:
            tally[cid] = tally.get(cid, 0) + 1
    for cid in check_ids:
        if cid in exempt:
            continue
        if tally.get(cid, 0) < per_check:
            findings.append(f"검사 {cid} 의 변조본 {tally.get(cid, 0)}건 < 하한 {per_check}")

    # ★ 상신 케이스의 하한은 **선언이 있을 때만** 건다(재정 P-3). 하드 하한을 두지 않는
    #   이유는 상신 축이 수렴 검사에만 있어 코퍼스 대부분이 정상적으로 0건이기 때문이다.
    #   다만 선언되면 래칫으로 작동한다 — 상신 케이스를 지우면서 하한도 함께 낮추는 경로를
    #   막는 것이 floors 절의 존재 이유다.
    declared_escalate = floors.get("min_escalate_cases")
    if isinstance(declared_escalate, int) and declared_escalate > 0:
        have = sum(1 for case in cases if case.expect_escalate)
        if have < declared_escalate:
            findings.append(f"상신 케이스 {have}건 < 하한 {declared_escalate}")
    return findings


def import_reader():
    """`reader/lib` 를 로드한다. 실패는 환경 오류다."""
    try:
        from reader.lib import run_checks  # noqa: PLC0415
        from reader.lib.report import CheckContext  # noqa: PLC0415
        from reader.lib.rules import Rules  # noqa: PLC0415
        from reader.lib import spec_io  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001 - import 실패는 환경 오류
        fail_env(f"reader/lib 로드 실패: {type(exc).__name__}: {exc}")
    return run_checks, CheckContext, Rules, spec_io


def run_all(mod, CheckContext, rules, schema, *, spec, source_text, peer, prior, revision):
    """READ 10행 + FREEZE 2행을 한 번에 낸다(등재의 정본은 `CHECK_REGISTRY` 이며 순회는 동적이다)."""
    read_ctx = CheckContext(
        spec=spec, source_text=source_text, rules=rules, schema=schema, peer_spec=peer
    )
    rows = list(mod.run_read_checks(read_ctx))
    freeze_ctx = CheckContext(
        spec=revision, source_text=source_text, rules=rules, schema=schema, prior_spec=prior
    )
    rows += list(mod.run_freeze_checks(freeze_ctx))
    return rows


def main(argv: list[str] | None = None) -> int:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_repo = os.path.dirname(script_dir)

    parser = argparse.ArgumentParser(
        prog="check_validator_enforcement.py",
        description="patent-docent 검증기 집행 실증 도구 (read-only).",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    parser.add_argument("--verbose", action="store_true", help="통과한 케이스도 변조 내용과 함께 출력")
    parser.add_argument("--json", action="store_true", dest="as_json", help="기계 판독 결과(JSON) 출력")
    args = parser.parse_args(argv)

    repo = os.path.realpath(args.repo)
    if not os.path.isdir(repo):
        fail_env(f"리포 경로가 디렉터리가 아니다: {args.repo}")
    if repo not in sys.path:
        sys.path.insert(0, repo)

    mod, CheckContext, Rules, spec_io = import_reader()
    check_ids: tuple[str, ...] = tuple(mod.READ_CHECK_IDS) + tuple(mod.FREEZE_CHECK_IDS)
    base_decl, cases, floors = load_manifest(repo, frozenset(check_ids))
    check_manifest_covers_disk(repo, cases)

    root = os.path.join(repo, FIXTURE_ROOT)
    try:
        rules = Rules.load()
        schema = spec_io.load_schema()
    except Exception as exc:  # noqa: BLE001
        fail_env(f"규칙·스키마 로드 실패: {type(exc).__name__}: {exc}")

    # 축 → 정책 대응은 규칙 파일이 정본이므로 규칙 로드 이후에 선언을 검증한다(재정 P-3).
    axis_policies = escalatable_axes(rules)
    validate_escalate_declarations(cases, axis_policies)

    base_source = load_text(os.path.join(root, base_decl["source"]), "base source")
    base_spec = load_json(os.path.join(root, base_decl["spec"]), "base spec")
    base_peer = load_json(os.path.join(root, base_decl["peer"]), "base peer")
    base_rev = load_json(os.path.join(root, base_decl["revision"]), "base revision")

    # --- ① 기준선 -----------------------------------------------------------
    baseline_rows = run_all(
        mod, CheckContext, rules, schema,
        spec=base_spec, source_text=base_source, peer=base_peer, prior=base_spec, revision=base_rev,
    )
    baseline_fail = [r.check_id for r in baseline_rows if r.status != "pass"]
    baseline_vacuous = [r.check_id for r in baseline_rows if r.vacuous != "none"]
    # 무변조 코퍼스의 상신은 판정이 아니므로 종료 코드에 넣지 않는다 — 다만 침묵하지도
    # 않는다. 기준선이 이미 상신 중이면 변조본의 상신 델타를 그 위에서 읽어야 한다.
    baseline_escalate, baseline_conflict = collect_escalations(baseline_rows)

    # --- ④ 하한 -------------------------------------------------------------
    floor_findings = enforce_floors(cases, floors, check_ids, frozenset({"read.schema"}))

    # --- ②③ 변조본 ---------------------------------------------------------
    outcomes: list[Outcome] = []
    for case in cases:
        path = os.path.join(root, case.file)
        if not os.path.exists(path):
            fail_env(f"등재된 변조본이 디스크에 없다: {case.file}")
        spec, source_text, peer, revision = base_spec, base_source, base_peer, base_rev
        if case.role == "spec":
            spec = load_json(path, f"변조본 {case.file}")
        elif case.role == "peer":
            peer = load_json(path, f"변조본 {case.file}")
        elif case.role == "revision":
            revision = load_json(path, f"변조본 {case.file}")
        else:  # source
            source_text = load_text(path, f"변조본 {case.file}")
        try:
            rows = run_all(
                mod, CheckContext, rules, schema,
                spec=spec, source_text=source_text, peer=peer, prior=base_spec, revision=revision,
            )
        except Exception as exc:  # noqa: BLE001 - 검사가 던지면 그것도 결함이다
            outcomes.append(
                Outcome(case=case, actual_fail=(), schema_ok=False,
                        error=f"{type(exc).__name__}: {exc}")
            )
            continue
        by_id = {r.check_id: r for r in rows}
        actual = tuple(r.check_id for r in rows if r.status != "pass")
        schema_row = by_id.get("read.schema")
        schema_ok = bool(schema_row is not None and schema_row.status == "pass")
        rule_ids = tuple(sorted({
            f.rule for cid in actual for f in by_id[cid].findings if getattr(f, "rule", "")
        }))
        escalated, conflict = collect_escalations(rows)
        outcomes.append(
            Outcome(
                case=case, actual_fail=actual, schema_ok=schema_ok, rule_ids=rule_ids,
                actual_escalate=escalated, extras_conflict=conflict,
            )
        )

    mismatches = [o for o in outcomes if not o.ok]

    # --- 출력 ---------------------------------------------------------------
    tally: dict[str, int] = {cid: 0 for cid in check_ids}
    for case in cases:
        for cid in case.expect_fail:
            tally[cid] = tally.get(cid, 0) + 1

    # ★ 상신은 **따로** 센다(재정 P-3). 실패로 잡히는 것과 상신으로 뜨는 것을 한 수로 뭉개면
    #   정책 차등이 보고에서 사라진다. `measure-only` 축은 어느 쪽에도 들어가지 않는다 —
    #   그 축은 판정하지 않으므로 셀 대상이 아니다(값은 axes[].jaccard 에만 남는다).
    escalate_axis_ids = tuple(a for a, p in axis_policies.items() if policy_can_escalate(p))
    escalate_tally: dict[str, int] = {axis: 0 for axis in escalate_axis_ids}
    for case in cases:
        for axis in case.expect_escalate:
            escalate_tally[axis] = escalate_tally.get(axis, 0) + 1
    escalate_cases = sum(1 for case in cases if case.expect_escalate)
    # 판정 제외 축 = 미달이 fail 도 escalate 도 아닌 축(계약의 status_on_miss 로 판별한다).
    unjudged_axes = tuple(
        a for a, p in axis_policies.items()
        if str(p.get("status_on_miss")) not in ("fail", ESCALATE_STATUS)
    )

    if args.as_json:
        payload = {
            "repo": repo,
            "result": "PASS" if not (baseline_fail or floor_findings or mismatches) else "FAIL",
            "baseline": {
                "checks": [r.to_row_dict() for r in baseline_rows],
                "failures": baseline_fail,
                "vacuous": baseline_vacuous,
                "escalations": list(baseline_escalate),
                "escalation_conflict": baseline_conflict,
            },
            "cases": len(cases),
            "tally": tally,
            "escalate_tally": escalate_tally,
            "escalate_cases": escalate_cases,
            "unjudged_axes": list(unjudged_axes),
            "floor_findings": floor_findings,
            "mismatches": [
                {
                    "file": o.case.file,
                    "role": o.case.role,
                    "expect_fail": list(o.case.expect_fail),
                    "actual_fail": list(o.actual_fail),
                    "expect_escalate": list(o.case.expect_escalate),
                    "actual_escalate": list(o.actual_escalate),
                    "escalation_conflict": o.extras_conflict,
                    "schema_passed": o.schema_ok,
                    "error": o.error,
                }
                for o in mismatches
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"== ① 기준선 — 무변조 코퍼스가 검사 {len(baseline_rows)}종을 통과하는가 ==")
        for row in baseline_rows:
            mark = "ok " if row.status == "pass" else "FAIL"
            print(
                f"  [{mark}] {row.check_id:<26} checked={row.checked:<4} "
                f"viol={row.violations:<3} vacuous={row.vacuous}"
            )
        if baseline_fail:
            print("  ★ 기준선이 실패했다 — 아래 변조본 판정은 무의미하다(과잉 제약이면 변조본도 당연히 실패한다).")
        if baseline_vacuous:
            print(f"  ★ 공허 날인된 행: {', '.join(baseline_vacuous)} — 대상 0건 검사는 아무것도 반증하지 않는다.")
        if baseline_escalate:
            print(
                f"  ★ 기준선 상신: {', '.join(baseline_escalate)} — 무변조 코퍼스가 이미 상신 중이다"
                "(판정 실패는 아니다 · 재정 P-3). 변조본의 상신은 이 바닥 위에서 읽어야 한다."
            )
        if baseline_conflict:
            print(f"  ★ 기준선 상신 보고가 어긋난다: {baseline_conflict}")

        print("\n== ②③ 변조본 — 정확히 선언된 검사만 실패하는가 ==")
        for outcome in outcomes:
            case = outcome.case
            mark = "ok " if outcome.ok else "FAIL"
            line = f"  [{mark}] {case.file}  (role={case.role})"
            if outcome.ok and not args.verbose:
                print(line)
                continue
            print(line)
            print(f"        변조 : {case.mutation}")
            print(f"        기대 : {', '.join(case.expect_fail)}")
            print(f"        실제 : {', '.join(outcome.actual_fail) or '(전건 통과)'}")
            # 상신은 실패와 **다른 축**이므로 줄을 따로 세운다(재정 P-3). 선언도 실측도 없는
            # 케이스에는 줄을 만들지 않는다 — 빈 줄은 아무것도 뜻하지 않는다.
            if case.expect_escalate or outcome.actual_escalate:
                print(f"        상신 기대 : {', '.join(case.expect_escalate) or '(없음)'}")
                print(f"        상신 실제 : {', '.join(outcome.actual_escalate) or '(없음)'}")
            if outcome.rule_ids:
                print(f"        규칙 : {', '.join(outcome.rule_ids)}")
            if not outcome.ok:
                if outcome.error:
                    print(f"        오류 : {outcome.error}")
                elif not outcome.schema_ok and "read.schema" not in case.expect_fail:
                    print("        판정 : 스키마가 먼저 거부했다 — 이 케이스는 검증기를 시험하지 않았다")
                elif set(outcome.actual_fail) - set(case.expect_fail):
                    print(f"        판정 : 관할 밖 검사가 함께 실패했다 — {', '.join(sorted(set(outcome.actual_fail) - set(case.expect_fail)))}")
                elif set(case.expect_fail) - set(outcome.actual_fail):
                    print(f"        판정 : 잡아야 할 검사가 통과했다 — {', '.join(sorted(set(case.expect_fail) - set(outcome.actual_fail)))}")
                # 상신 불일치는 위 판정과 **함께** 날 수 있으므로 elif 로 잇지 않는다.
                surplus = sorted(set(outcome.actual_escalate) - set(case.expect_escalate))
                shortfall = sorted(set(case.expect_escalate) - set(outcome.actual_escalate))
                if surplus:
                    print(f"        판정 : 선언하지 않은 축이 상신됐다 — {', '.join(surplus)}")
                if shortfall:
                    print(f"        판정 : 상신되어야 할 축이 뜨지 않았다 — {', '.join(shortfall)}")
                if outcome.extras_conflict:
                    print(f"        판정 : 상신 보고가 스스로 어긋난다 — {outcome.extras_conflict}")
                print(f"        근거 : {case.basis}")

        print("\n== ④ 하한 — 픽스처가 비어 공허 통과하지 않는가 ==")
        print(f"  케이스 {len(cases)}건 (하드 하한 {ABSOLUTE_MIN_CASES}, 선언 하한 {floors.get('min_cases', '없음')})")
        print("  검사별 배분: " + " · ".join(f"{cid}={tally.get(cid, 0)}" for cid in check_ids))
        print(
            f"  상신 케이스 {escalate_cases}건"
            + (f" (선언 하한 {floors['min_escalate_cases']})" if isinstance(floors.get("min_escalate_cases"), int) else "")
            + " — 축별 배분: "
            + (" · ".join(f"{axis}={escalate_tally.get(axis, 0)}" for axis in escalate_axis_ids) or "(상신 축 없음)")
        )
        if unjudged_axes:
            print(
                f"  판정 제외 축(측정 전용): {', '.join(unjudged_axes)} — 실패에도 상신에도 "
                "세지 않는다(재정 P-3)."
            )
        for finding in floor_findings:
            print(f"  [FAIL] {finding}")
        if not floor_findings:
            print("  [ok ] 전 하한 충족")

        total_fail = len(baseline_fail) + len(floor_findings) + len(mismatches)
        if total_fail:
            print(
                f"\nRESULT: FAIL — 기준선 실패 {len(baseline_fail)} · 하한 미달 {len(floor_findings)} "
                f"· 케이스 불일치 {len(mismatches)}/{len(outcomes)}",
                file=sys.stderr,
            )
        else:
            passed = len(baseline_rows) - len(baseline_fail)
            print(
                f"\nRESULT: PASS — 기준선 {passed}/{len(baseline_rows)} "
                f"· 변조본 {len(outcomes)}/{len(outcomes)} · 하한 충족"
            )
            print(
                "        이 도구가 증명한 것은 검증기가 거부하는 것뿐이다. "
                "계약의 옳음도, 스키마의 집행도 증명하지 않는다."
            )

    if baseline_fail or floor_findings or mismatches:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
