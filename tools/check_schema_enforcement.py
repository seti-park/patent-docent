#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""스키마 집행 실증 도구 — **스키마가 강제하는 것**의 경계 측정.

이 도구가 증명하는 것은 하나다: 계약 **스키마**가 어떤 인스턴스를 거부하고 어떤 인스턴스를
통과시키는가. 그 이상은 증명하지 않는다 — 검증기 코드가 맡은 의미 불변식은 여기서 돌지 않으며,
전건 통과가 "M0.6 의미 집행 완료"를 뜻하지 않는다(M0.6 재감수 B-02).
`tests/fixtures/schema-enforcement/manifest.json`이 인스턴스마다 정답(`expect`)을 적어 두고,
이 도구는 각 인스턴스를 `Draft202012Validator`에 넣어 실제 판정이 정답과 같은지 대조한다.

  - `expect: "reject"`           무효 인스턴스. 스키마가 **거부해야** 한다. 통과하면 집행이 비어 있는 것이다.
  - `expect: "accept"`           유효 인스턴스. 스키마가 **통과시켜야** 한다. 거부하면 과잉 제약이다.
  - `expect: "validator-scope"`  **스키마가 설계상 통과시키는** 무효 인스턴스. 이 불변식의 집행은
    JSON Schema의 표현력 밖이며 지정된 **검증기 검사**(`enforced_by`)가 맡는다. 그러므로 여기서는
    통과가 정답이고, 거부하면 그것도 실패다 — 설계 서술과 실물이 다르다는 뜻이기 때문이다.

`validator-scope` 계수는 자랑이 아니라 **스키마 밖으로 미뤄 둔 불변식의 목록**이다. 요약 줄의
`VALIDATOR_SCOPE n/n`은 "스키마를 통과하는 무효 인스턴스가 n건"이라는 뜻이며, 각 항목의
`enforced_by`가 그 구멍을 닫을 검사의 id다. 이 계열을 REJECT_OK·ACCEPT_OK에 섞지 않는 이유가
여기 있다 — 섞으면 스키마 밖의 집행이 스키마 집행 실적으로 계상된다.

그 n건이 전부 부채인 것은 아니다. `enforced_status`가 그 둘을 가른다.

  - `"planned"`      집행할 검사가 아직 코드로 없다. 이것이 부채다.
  - `"implemented"`  검증기가 이미 막는다. 이때는 `enforcement_evidence`(그 거부를 실증하는
    테스트의 노드 id)를 함께 적어야 하며, 근거 없이 "구현되었다"고 적는 경로는 로드 시 막힌다.

이 구별을 두는 이유는 요약 줄이 **집행 범위를 실제와 다르게 말하는 것**을 막기 위해서다.
검증기가 검사를 구현한 뒤에도 목록이 `(미구현)`이라 말하면 좁게 신고하는 것이고, 증거 없이
`(구현됨)`이라 말하면 넓게 신고하는 것이다. 양방향 모두 M0.6 재감수가 판정한 결함의 뿌리다.

M0.5 재감수의 교훈이 이 도구의 존재 이유다 — 이름·경로·메타스키마 층위의 정합 검사(K1~K7)가
전부 통과해도 스키마가 아무것도 강제하지 않을 수 있다. 정합은 집행의 증거가 아니다.
근거 = M0.5 재감수 B-02·B-07·M-01·M-02·M-03·M-05 + Owner 재정 2026-08-18 N9
      + M0.6 재감수 B-02(정확한 재현식 2건이 ACCEPT되는데 manifest가 그 자리에 다른 변형을 넣어
        13/13이 해당 불변식을 시험하지 않았다).

★ 자기매칭 격리 (정본: `docs/SPEC.md` §4.8 자기매칭 격리 요건 + `docs/decisions/D-20260817-02` §5 규율 3)
`tools/check_spec_refs.py`는 `tests/`를 스캔 목록에서 배제하고 들어오면 exit 2로 거부한다.
이 도구는 반대로 `tests/fixtures/schema-enforcement/`를 **읽는 것이 임무**인데, 그럼에도
자기매칭이 성립하지 않는다. 근거는 셋이다.

  1. 이 도구는 **탐지 패턴을 하나도 갖지 않는다**. 문자열을 찾지 않고 JSON Schema를 인스턴스에
     적용할 뿐이다. 자기매칭은 "검사기가 가진 패턴 견본이 스캔 대상에 섞여 오탐하는" 사고인데,
     패턴이 없으면 그 사고의 전제가 없다.
  2. 판정의 근거는 전적으로 **계약 스키마 실파일**(`reader/schemas/`·`contracts/schemas/`)이며
     이 소스도, 픽스처도 판정 기준을 제공하지 않는다. 픽스처는 피검체이지 법이 아니다.
  3. 이 소스에는 결함 표본 문자열이 리터럴로 없다(격리 요건 2항). 심은 결함은 전부
     `tests/fixtures/schema-enforcement/`의 `reject/`·`validator-scope/` 데이터 파일에만 있고,
     그것이 무엇이었는지는 manifest의 `basis`가 데이터로 적는다.

즉 이 도구가 픽스처를 읽는 것은 스캔이 아니라 **검증 대상 투입**이다. 두 도구의 규율이
서로 어긋나 보이는 자리이므로 감수 오해를 막기 위해 여기 명문화한다.

종료 코드 (SPEC §8.3 관례):
  0 = 전건 기대 일치 / 1 = 검증 실패(기대와 실제 불일치) / 2 = 입력·환경 오류

`assert`를 쓰지 않는다(`python3 -O`에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - 환경 오류 경로
    print(f"ENVIRONMENT ERROR: jsonschema 로드 실패: {exc}", file=sys.stderr)
    sys.exit(2)


# 픽스처 루트 — manifest 와 인스턴스가 함께 산다.
FIXTURE_ROOT = "tests/fixtures/schema-enforcement"
MANIFEST_REL = f"{FIXTURE_ROOT}/manifest.json"

# manifest 항목의 필수 키.
CASE_KEYS: tuple[str, ...] = ("file", "schema", "expect", "series", "basis")
# `validator-scope` 항목에만 추가로 요구하는 키 — 이 불변식을 집행할 검사의 id.
SCOPE_KEY = "enforced_by"
# 같은 항목의 필수 키 — 그 검사가 코드로 존재하는가("planned" | "implemented").
STATUS_KEY = "enforced_status"
# `enforced_status == "implemented"` 일 때만 쓰는 필수 키 — 그 거부를 실증하는 테스트 노드 id.
EVIDENCE_KEY = "enforcement_evidence"
SCOPE_ONLY_KEYS: tuple[str, ...] = (SCOPE_KEY, STATUS_KEY, EVIDENCE_KEY)
STATUS_VALUES: tuple[str, ...] = ("planned", "implemented")
EXPECT_VALUES: tuple[str, ...] = ("reject", "accept", "validator-scope")
# 픽스처 디렉터리(= 기대 클래스 이름과 같다).
FIXTURE_BUCKETS: tuple[str, ...] = EXPECT_VALUES

EPILOG = """\
하는 일:
  manifest 의 각 인스턴스를 지정된 계약 스키마로 검증하고, 실제 판정이 expect 와
  같은지 대조한다. 어긋나면 기대와 실제를 명시 비교로 출력하고 exit 1 한다.

  expect: reject          스키마가 거부해야 하는 무효 인스턴스 (통과 = 집행 공백)
  expect: accept          스키마가 통과시켜야 하는 유효 인스턴스 (거부 = 과잉 제약)
  expect: validator-scope 스키마가 설계상 통과시키는 무효 인스턴스 — 집행은 enforced_by 의
                          검증기 검사 몫이다 (거부 = 설계 서술과 실물 불일치이므로 이것도 실패)

★ 이 도구가 증명하는 것은 "스키마가 강제하는 것"뿐이다:
  전건 통과는 의미 집행 완료가 아니다. VALIDATOR_SCOPE 계수는 스키마 집행 실적이 아니라
  스키마 밖으로 미뤄 둔 불변식의 수이며, 각 항목의 enforced_by 가 그 검사 id 다.
  enforced_status 가 planned(코드 없음 = 부채) 와 implemented(검증기가 이미 막음) 를 가르고,
  implemented 는 enforcement_evidence(그 거부를 실증하는 테스트 노드 id)를 반드시 동반한다.

★ 자기매칭 격리:
  이 도구는 탐지 패턴을 갖지 않는다 — 스키마를 인스턴스에 적용할 뿐이다. 따라서
  tests/fixtures/ 를 읽어도 자기매칭이 성립하지 않는다(스캔이 아니라 검증 대상 투입).
  판정 기준은 전량 계약 스키마 실파일에 있고, 심은 결함 문자열은 이 소스에 없다.
  상세 근거는 모듈 docstring 참조.

종료 코드: 0 전건 일치 / 1 검증 실패 / 2 입력·환경 오류
"""


def fail_env(message: str) -> None:
    """입력·환경 오류로 즉시 종료한다(exit 2)."""
    print(f"ENVIRONMENT ERROR: {message}", file=sys.stderr)
    sys.exit(2)


@dataclass
class Case:
    file: str
    schema: str
    expect: str
    series: str
    basis: str
    enforced_by: str = ""            # expect == "validator-scope" 일 때만 채워진다
    enforced_status: str = ""        # 같은 조건에서 "planned" | "implemented"
    enforcement_evidence: str = ""   # enforced_status == "implemented" 일 때만 채워진다

    @property
    def enforcement_note(self) -> str:
        """집행 상태 한 줄. 구현되었다고 말할 때는 반드시 증거를 함께 말한다."""
        if self.enforced_status == "implemented":
            return f"구현됨 — {self.enforcement_evidence}"
        return "미구현"

    @property
    def schema_verdict(self) -> str:
        """스키마 검증에서 나와야 하는 판정("reject" | "accept").

        `validator-scope` 는 **스키마가 설계상 통과시키는** 계열이므로 기대 판정이 accept 다.
        기대 클래스와 기대 판정을 구별하는 자리이며, 이 구별이 없으면 미구현 불변식이
        REJECT 실적으로 계상된다.
        """
        return "accept" if self.expect == "validator-scope" else self.expect


@dataclass
class Outcome:
    case: Case
    actual: str            # "reject" | "accept"
    first_error: str       # 거부된 경우의 첫 ValidationError 요지, 통과면 ""
    error_path: str        # 그 오류의 인스턴스 경로, 통과면 ""

    @property
    def ok(self) -> bool:
        return self.actual == self.case.schema_verdict


def load_json(path: str, label: str) -> Any:
    if not os.path.isfile(path):
        fail_env(f"{label} 파일이 없다: {path}")
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail_env(f"{label} 파일을 읽을 수 없다: {path} — {exc}")
    return None  # pragma: no cover - fail_env 가 이미 종료한다


def load_manifest(repo: str) -> list[Case]:
    data = load_json(os.path.join(repo, MANIFEST_REL), "manifest")
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        fail_env(f"manifest 형식 오류: 최상위 객체의 cases 배열이 필요하다 — {MANIFEST_REL}")

    cases: list[Case] = []
    seen: set[str] = set()
    for index, raw in enumerate(data["cases"]):
        where = f"{MANIFEST_REL} cases[{index}]"
        if not isinstance(raw, dict):
            fail_env(f"{where} 가 객체가 아니다")
        missing = [key for key in CASE_KEYS if key not in raw]
        if missing:
            fail_env(f"{where} 에 필수 키가 없다: {', '.join(missing)}")
        if raw["expect"] not in EXPECT_VALUES:
            fail_env(f"{where}.expect 가 {EXPECT_VALUES} 밖의 값이다: {raw['expect']!r}")
        if raw["file"] in seen:
            fail_env(f"{where}.file 이 중복 등재되었다: {raw['file']}")
        seen.add(raw["file"])
        fields = {key: raw[key] for key in CASE_KEYS}
        if raw["expect"] == "validator-scope":
            # 집행 주체를 적지 않은 validator-scope 항목은 "아무도 막지 않는다"를 숨긴다.
            enforced_by = raw.get(SCOPE_KEY)
            if not isinstance(enforced_by, str) or not enforced_by:
                fail_env(
                    f"{where} 는 expect=validator-scope 이므로 {SCOPE_KEY}(집행할 검사 id)가 필요하다"
                )
            fields[SCOPE_KEY] = enforced_by
            # 그 검사가 코드로 있는지를 적지 않으면 요약 줄이 집행 범위를 실제와 다르게 말한다.
            status = raw.get(STATUS_KEY)
            if status not in STATUS_VALUES:
                fail_env(
                    f"{where}.{STATUS_KEY} 가 {STATUS_VALUES} 밖의 값이거나 없다: {status!r} "
                    f"— validator-scope 항목은 집행 검사의 구현 여부를 반드시 신고한다"
                )
            fields[STATUS_KEY] = status
            evidence = raw.get(EVIDENCE_KEY)
            if status == "implemented":
                # 증거 없는 "구현됨"은 집행 범위를 실제보다 넓게 말하는 경로다.
                if not isinstance(evidence, str) or not evidence:
                    fail_env(
                        f"{where} 는 {STATUS_KEY}=implemented 이므로 "
                        f"{EVIDENCE_KEY}(그 거부를 실증하는 테스트 노드 id)가 필요하다"
                    )
                fields[EVIDENCE_KEY] = evidence
            elif EVIDENCE_KEY in raw:
                fail_env(
                    f"{where}.{EVIDENCE_KEY} 는 {STATUS_KEY}=implemented 항목에만 쓸 수 있다"
                    f"(현재 {STATUS_KEY}={status!r})"
                )
        else:
            stray = [key for key in SCOPE_ONLY_KEYS if key in raw]
            if stray:
                fail_env(
                    f"{where} 의 {', '.join(stray)} 는 expect=validator-scope 항목에만 쓸 수 있다"
                )
        cases.append(Case(**fields))

    if not cases:
        fail_env(f"manifest 에 케이스가 하나도 없다 — {MANIFEST_REL}")
    return cases


def check_manifest_covers_disk(repo: str, cases: list[Case]) -> None:
    """디스크의 픽스처가 전부 manifest 에 등재되었는지 확인한다.

    미등재 픽스처는 집행 증명에 뚫린 구멍이므로 검증 실패가 아니라 입력 오류로 다룬다.
    """
    listed = {case.file for case in cases}
    found: list[str] = []
    for bucket in FIXTURE_BUCKETS:
        directory = os.path.join(repo, FIXTURE_ROOT, bucket)
        if not os.path.isdir(directory):
            fail_env(f"픽스처 디렉터리가 없다: {FIXTURE_ROOT}/{bucket}")
        for name in sorted(os.listdir(directory)):
            if name.endswith(".json"):
                found.append(f"{bucket}/{name}")

    orphans = [rel for rel in found if rel not in listed]
    if orphans:
        fail_env(
            "manifest 에 등재되지 않은 픽스처가 있다(집행 증명의 구멍): " + ", ".join(orphans)
        )


def load_validators(repo: str, cases: list[Case]) -> dict[str, Draft202012Validator]:
    validators: dict[str, Draft202012Validator] = {}
    for case in cases:
        if case.schema in validators:
            continue
        schema = load_json(os.path.join(repo, case.schema), "스키마")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001 - 메타스키마 위반은 환경 오류로 다룬다
            fail_env(f"스키마 메타 검증 실패: {case.schema} — {exc}")
        validators[case.schema] = Draft202012Validator(schema)
    return validators


def leaf_errors(error: Any) -> list[Any]:
    """`oneOf`·`anyOf` 안쪽까지 내려가 실제 위반 지점(잎 오류)만 모은다.

    분기 선택지 중 `const` 위반이 있는 분기는 **의도된 분기가 아니다**(재료 항목의 `kind`,
    사실 항목의 `origin` 처럼 분기를 식별하는 상수가 어긋난 것이므로 애초에 그 분기의 규칙을
    적용받을 인스턴스가 아니다). 그런 분기가 아닌 후보가 하나라도 있으면 후보만 남긴다.
    """
    if not error.context:
        return [error]
    # oneOf·anyOf 의 context 는 전 분기의 오류가 한 줄로 섞여 있다. 각 오류의 schema_path 첫
    # 요소가 분기 번호이므로 그것으로 다시 분기별로 묶는다.
    branches: dict[Any, list[Any]] = {}
    for sub in error.context:
        branch = sub.schema_path[0] if sub.schema_path else None
        branches.setdefault(branch, []).extend(leaf_errors(sub))
    candidates = [leaves for leaves in branches.values() if not any(err.validator == "const" for err in leaves)]
    chosen = candidates if candidates else list(branches.values())
    flat: list[Any] = []
    for leaves in chosen:
        flat.extend(leaves)
    return flat


def pick_reported_error(errors: list[Any]) -> Any:
    """보고할 오류 1건을 결정론으로 고른다.

    `item` 이 6종 `oneOf` 인 탓에 최상위 오류는 "어느 분기에도 맞지 않는다"는 뭉뚱그린 문장이
    된다. 실제 위반 지점을 보이려면 안쪽으로 내려가야 한다. 선택 규칙 = ① 인스턴스 경로가 가장
    깊은 것 ② `required` 는 상위 구조 신고일 뿐이므로 후순위 ③ 남으면 스키마 경로 사전순.
    """
    leaves: list[Any] = []
    for error in errors:
        leaves.extend(leaf_errors(error))
    if not leaves:
        return errors[0]
    return max(
        leaves,
        key=lambda err: (
            len(list(err.absolute_path)),
            0 if err.validator == "required" else 1,
            [str(part) for part in err.absolute_schema_path],
        ),
    )


def run_case(repo: str, case: Case, validator: Draft202012Validator) -> Outcome:
    instance = load_json(os.path.join(repo, FIXTURE_ROOT, case.file), "인스턴스")
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    if not errors:
        return Outcome(case=case, actual="accept", first_error="", error_path="")
    first = pick_reported_error(errors)
    message = first.message.replace("\n", " ")
    if len(message) > 300:
        message = message[:300] + " …"
    path = "/".join(str(part) for part in first.absolute_path) or "(root)"
    schema_path = "/".join(str(part) for part in first.absolute_schema_path)
    return Outcome(
        case=case,
        actual="reject",
        first_error=message,
        error_path=f"{path} ← 스키마 {schema_path}",
    )


def verdict_line(case: Case, actual: str) -> str:
    """기대와 어긋난 케이스의 판정 문장. 기대 클래스마다 뜻이 다르다."""
    if case.expect == "validator-scope":
        # 기대 판정은 accept 이므로 어긋남 = reject 뿐이다.
        return (
            "스키마가 validator-scope 인스턴스를 거부했다 — 설계 서술과 실물이 다르다"
            f"(이 불변식은 {case.enforced_by} 의 몫이라고 적혀 있다)"
        )
    if actual == "accept":
        return "스키마가 무효 인스턴스를 통과시켰다 — 집행이 비어 있다"
    return "스키마가 유효 인스턴스를 거부했다 — 과잉 제약이다"


def report(outcomes: list[Outcome], verbose: bool) -> None:
    for outcome in outcomes:
        case = outcome.case
        mark = "ok " if outcome.ok else "FAIL"
        line = f"[{mark}] expect={case.expect:<15} actual={case.schema_verdict if outcome.ok else outcome.actual:<6} {case.file}"
        if outcome.ok and not verbose:
            print(line)
            continue
        print(line)
        print(f"        계열 : {case.series}")
        if case.expect == "validator-scope":
            print(
                f"        집행 : {case.enforced_by} ({case.enforcement_note}) "
                "— 검증기 몫이며 스키마는 설계상 통과시킨다"
            )
        if outcome.first_error:
            print(f"        거부 : {case.schema} @ {outcome.error_path} — {outcome.first_error}")
        if not outcome.ok:
            print(f"        기대 : {case.expect} (스키마 판정 {case.schema_verdict})")
            print(f"        실제 : {outcome.actual}")
            print(f"        판정 : {verdict_line(case, outcome.actual)}")
            print(f"        근거 : {case.basis}")


def main(argv: list[str] | None = None) -> int:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_repo = os.path.dirname(script_dir)

    parser = argparse.ArgumentParser(
        prog="check_schema_enforcement.py",
        description="patent-docent 스키마 집행 실증 도구 (read-only).",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    parser.add_argument("--verbose", action="store_true", help="통과한 케이스도 계열·거부 사유와 함께 출력")
    args = parser.parse_args(argv)

    repo = os.path.realpath(args.repo)
    if not os.path.isdir(repo):
        fail_env(f"리포 경로가 디렉터리가 아니다: {args.repo}")

    cases = load_manifest(repo)
    check_manifest_covers_disk(repo, cases)
    validators = load_validators(repo, cases)

    outcomes = [run_case(repo, case, validators[case.schema]) for case in cases]
    report(outcomes, args.verbose)

    expected_reject = [o for o in outcomes if o.case.expect == "reject"]
    expected_accept = [o for o in outcomes if o.case.expect == "accept"]
    expected_scope = [o for o in outcomes if o.case.expect == "validator-scope"]
    reject_ok = [o for o in expected_reject if o.ok]
    accept_ok = [o for o in expected_accept if o.ok]
    scope_ok = [o for o in expected_scope if o.ok]
    mismatches = [o for o in outcomes if not o.ok]

    if mismatches:
        print(
            f"\nFAILED: {len(mismatches)}/{len(outcomes)} 케이스가 기대와 어긋난다 "
            f"(reject {len(reject_ok)}/{len(expected_reject)} · accept {len(accept_ok)}/{len(expected_accept)} "
            f"· validator-scope {len(scope_ok)}/{len(expected_scope)})",
            file=sys.stderr,
        )
        return 1

    print(
        f"SUMMARY: cases={len(outcomes)} "
        f"REJECT_OK {len(reject_ok)}/{len(expected_reject)} "
        f"ACCEPT_OK {len(accept_ok)}/{len(expected_accept)} "
        f"VALIDATOR_SCOPE {len(scope_ok)}/{len(expected_scope)} "
        f"schemas={len(validators)}"
    )
    # 이 도구가 증명한 것은 스키마 층뿐이다. VALIDATOR_SCOPE 는 스키마 집행 실적이 아니므로
    # 무엇이 스키마 밖에 있고 그중 무엇이 아직 코드 없이 열려 있는지를 요약 다음 줄에 남긴다.
    implemented = [o for o in expected_scope if o.case.enforced_status == "implemented"]
    planned = [o for o in expected_scope if o.case.enforced_status != "implemented"]
    print(
        "        스키마가 강제하는 것만 위에서 증명되었다. "
        f"validator-scope {len(expected_scope)}건 = 스키마를 통과하는 무효 인스턴스 "
        f"(구현됨 {len(implemented)} / 미구현 {len(planned)}):"
    )
    for outcome in expected_scope:
        print(f"          - {outcome.case.file} → {outcome.case.enforced_by} ({outcome.case.enforcement_note})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
