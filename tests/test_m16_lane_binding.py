# -*- coding: utf-8 -*-
"""레인 왕복 **시점 결속**(재정 2026-08-19 P-12 · S4)과 섀도 원장 1행 보증의 pytest.

각 테스트의 docstring 한 줄은 **"이 테스트가 없으면 무엇이 공허해지는가"** 다
(`tests/test_m2_read.py` 와 같은 형식).

`assert` 를 쓰지 않는다 — `python3 -O` 에서 전부 제거되어 망가진 코드가 공허 통과한다
(CLAUDE.md §3). 불일치는 `pytest.fail()` 로 명시 비교와 함께 보고한다.

★ 통주 하네스는 `tests/test_m2_read.py` 의 것을 그대로 쓴다(원천 생성 · 레인 응답 트리 ·
**섀도 원장 격리**). 같은 하네스를 두 벌 만들면 한 벌은 반드시 낡고, 특히 격리 규율(재정 G6 ·
P-U2)이 낡는 순간 합성 픽스처가 생산 원장을 오염시킨다 — 과거 실측 1,178행이 그 사고다.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
HERE = os.path.join(REPO, "tests")
for entry in (REPO, HERE):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import test_m2_read as m2  # noqa: E402

from engine import paths as engine_paths  # noqa: E402
from engine.lanes.contract import (  # noqa: E402
    REQUEST_JSON_FIELDS,
    LaneContractError,
    LanePending,
    LaneRequest,
    LaneStaleResponseError,
    compute_input_digest,
    digest_source,
    load_response,
    render_request_md,
)
from engine.paths import RunPaths  # noqa: E402
from engine.stages import load_json, read_text  # noqa: E402
from engine.stages import read as read_stage  # noqa: E402

RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {"items": {"type": "array"}},
}


def probe_request(**overrides) -> LaneRequest:
    """결속 시험용 요청 1건. 값은 어느 것이든 되지만 **판마다 같아야** 한다."""
    fields = {
        "lane_id": "read-a/decompose/batch-0",
        "read_run": "read-a",
        "task": "decompose",
        "model": "opus-5",
        "effort": "max",
        "prompt_path": "reader/procedure/10-decompose.md",
        # 절차 트리도 요청의 일부다(재정 2026-08-19 S4) — 어느 절차 본문을 인라인하는지가
        # 정해지지 않으면 요청이 완전히 지정되지 않는다.
        "repo_root": REPO,
        "instructions": "| `M2001` | frame width | `12.0` | mm |",
        "slices": {"claims": "1. An apparatus comprising a frame."},
        "response_schema": RESPONSE_SCHEMA,
        "batch": 0,
    }
    fields.update(overrides)
    return LaneRequest(**fields)


def write_probe_response(path: str, *, request: LaneRequest, echo: str | None) -> None:
    """레인이 쓰는 자리. `echo=None` 이면 반향 자체를 빠뜨린 응답이다."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = {
        "lane_id": request.lane_id,
        "model": request.model,
        "effort": request.effort,
        "payload": {"items": []},
    }
    if echo is not None:
        body["input_digest"] = echo
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False)


# ===========================================================================
# ① 요청 지문 — 파생값의 결정론과 내용 민감도
# ===========================================================================


def test_input_digest_is_deterministic() -> None:
    """같은 요청이 두 지문을 가지면 대조 자체가 성립하지 않는다(재정 P-12 ①)."""
    first = probe_request().input_digest
    second = probe_request().input_digest
    if first != second:
        pytest.fail(f"같은 요청의 지문이 갈렸다: {first} != {second}")
    if len(first) != 64:
        pytest.fail(f"sha256 16진 64자 기대, 실제 {len(first)}자: {first}")


def test_input_digest_changes_when_any_bound_field_changes() -> None:
    """한 필드라도 지문 밖에 있으면 그 필드의 갱신이 낡은 응답을 살려 낸다(재정 P-12 ①).

    특히 `instructions`(수확 목록 · 재료 버전)와 `slices`(원문 조각)가 핵심이다 — 재정 문언이
    "어느 재료 버전·어느 원문 조각에 대한 요청인지"라고 지목한 그 둘이다.

    ★ 목록의 정본이 `REQUEST_JSON_FIELDS` 인 이유(재정 2026-08-19 S4). 지문 규격은 이제 이
    튜플이 아니라 렌더된 요청서 본문이 정하지만, **요청 파일이 싣는 필드는 전부 그 본문에
    있어야 한다** — 하나라도 본문 밖에 있으면 그 필드의 갱신이 지문에 닿지 않고, 닿지 않는
    필드는 낡은 응답을 살려 낸다. 그래서 이 시험은 "request.json 의 필드 전량이 실제로
    결속되는가"를 묻는 자리로 남는다.
    """
    base = probe_request()
    mutations = {
        "lane_id": "read-b/decompose/batch-0",
        "read_run": "read-b",
        "task": "synthesize",
        "model": "sonnet-5",
        "effort": "low",
        "prompt_path": "reader/procedure/30-synthesis.md",
        "instructions": "| `M2001` | frame width | `12.5` | mm |",
        "slices": {"claims": "1. An apparatus comprising a frame and a lever."},
        "response_schema": {"type": "object", "required": ["items"]},
        "batch": 1,
    }
    missing = [name for name in REQUEST_JSON_FIELDS if name not in mutations]
    if missing:
        pytest.fail(f"지문 대상 필드인데 변조 시험이 없다: {missing}")
    for name, value in mutations.items():
        changed = probe_request(**{name: value}).input_digest
        if changed == base.input_digest:
            pytest.fail(f"{name} 을 바꿨는데 지문이 그대로다: {changed}")


def test_request_json_carries_the_digest_it_binds(tmp_path) -> None:
    """지문이 요청 파일에 없으면 레인은 반향할 값을 알 수 없고 규약이 공허해진다."""
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415

    request = probe_request()
    root = os.path.join(str(tmp_path), "lanes")
    directory = FileLaneAdapter(root, REPO).write_request(request)
    written = load_json(os.path.join(directory, "request.json"))
    if written.get("input_digest") != request.input_digest:
        pytest.fail(f"request.json 의 지문이 다르다: {written.get('input_digest')}")
    prompt = read_text(os.path.join(directory, "request.md"))
    for needle in ("| 입력 지문 |", request.input_digest, "낡은 응답으로 거부한다"):
        if needle not in prompt:
            pytest.fail(f"request.md 에 {needle!r} 이 없다 — 반향 의무가 요청서에 없다")




# ---------------------------------------------------------------------------
# ①-2 지문의 새 규격 (재정 2026-08-19 S4) — 본문 결박과 제3자 재계산
# ---------------------------------------------------------------------------


PROCEDURE_RELATIVE = "reader/procedure/10-decompose.md"


def make_procedure_mirror(tmp_path, name: str, *, extra: str = "") -> str:
    """절차 트리 **사본** 하나. 실제 리포를 변조하지 않고 절차 본문을 바꿔 보는 자리다."""
    mirror = os.path.join(str(tmp_path), name)
    target = os.path.join(mirror, *PROCEDURE_RELATIVE.split("/"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, *PROCEDURE_RELATIVE.split("/")), target)
    if extra:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(extra)
    return mirror


def legacy_digest(request: LaneRequest) -> str:
    """구 규격(재정 S4 이전)의 지문 재현 — 요청 필드 정규 JSON 의 sha256."""
    body = {name: getattr(request, name) for name in REQUEST_JSON_FIELDS}
    blob = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def test_third_party_can_recompute_the_digest_from_the_file_alone(tmp_path) -> None:
    """파일만으로 재계산되지 않는 지문은 **대조를 코드의 특권**으로 만든다(재정 S4).

    두 층으로 본다. ⓐ 라이브러리 왕복(`render → digest_source → compute`)이 요청의 지문과
    같은가 ⓑ **셸 한 줄**(`grep -v '^| 입력 지문 |' request.md | sha256sum`)이 같은 값을
    내는가. ⓑ가 없으면 "제3자가 재계산할 수 있다"는 문언이 파이썬 안에서만 참인 주장이 된다.
    """
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415

    request = probe_request()
    rendered = render_request_md(request)
    if compute_input_digest(digest_source(rendered)) != request.input_digest:
        pytest.fail(
            "지문 행을 지운 본문의 해시가 요청 지문과 다르다: "
            f"{compute_input_digest(digest_source(rendered))} != {request.input_digest}"
        )
    rows = [line for line in rendered.split("\n") if line.startswith("| 입력 지문 |")]
    if len(rows) != 1 or request.input_digest not in rows[0]:
        pytest.fail(f"지문 행이 한 줄로 서지 않았다: {rows}")

    directory = FileLaneAdapter(os.path.join(str(tmp_path), "lanes"), REPO).write_request(
        request
    )
    path = os.path.join(directory, "request.md")
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob != rendered.encode("utf-8"):
        pytest.fail("쓰인 파일 바이트가 렌더 결과와 다르다 — 셸 재계산의 전제가 깨진다")

    proc = subprocess.run(
        ["bash", "-c", "grep -v '^| 입력 지문 |' \"$1\" | sha256sum", "_", path],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        pytest.fail(f"셸 재계산이 실패했다(exit {proc.returncode}): {proc.stderr}")
    shell_digest = proc.stdout.split()[0]
    if shell_digest != request.input_digest:
        pytest.fail(f"셸 재계산 {shell_digest} != 요청 지문 {request.input_digest}")


def test_procedure_body_is_bound_into_the_digest(tmp_path) -> None:
    """이 시험이 없으면 절차 개정이 지문에 닿지 않고 **구 응답이 통과한다**(재정 S4 · NEW BLOCKER ③).

    실측 사고(2026-08-19 감수 D): 보관 요청문 29,046 B 와 현행 절차로 재렌더한 39,152 B 가
    같은 지문을 들었다. 요청서는 절차 문서 **본문**을 인라인하는데 구 지문은 그 문서의 **경로
    문자열**만 쟀기 때문이다. 대조군으로 구 규격을 함께 계산해, 그 규격에서는 두 요청이
    여전히 같은 값을 낸다는 것을 같은 자리에서 보인다.
    """
    plain = make_procedure_mirror(tmp_path, "plain")
    tampered = make_procedure_mirror(
        tmp_path, "tampered", extra="\n\n## [변조] 추가 조항\n\n단위를 cm 로 적어라.\n"
    )
    before = probe_request(repo_root=plain)
    after = probe_request(repo_root=tampered)

    if before.input_digest == after.input_digest:
        pytest.fail(f"절차 본문을 바꿨는데 지문이 그대로다: {before.input_digest}")
    if legacy_digest(before) != legacy_digest(after):
        pytest.fail(
            "대조군이 성립하지 않는다 — 구 규격에서도 지문이 갈렸다: "
            f"{legacy_digest(before)} != {legacy_digest(after)}"
        )
    # 요청 필드는 하나도 바뀌지 않았다(바뀐 것은 절차 트리뿐이다).
    for name in REQUEST_JSON_FIELDS:
        if getattr(before, name) != getattr(after, name):
            pytest.fail(f"요청 필드 {name} 이 달라졌다 — 시험이 재는 것이 절차 본문이 아니다")


def test_request_without_repo_root_is_refused() -> None:
    """절차 트리가 비면 **어느 절차 본문을 인라인하는지**가 정해지지 않는다(재정 S4)."""
    with pytest.raises(LaneContractError) as excinfo:
        probe_request(repo_root="")
    if "repo_root" not in str(excinfo.value):
        pytest.fail(f"진단이 빈 필드를 지목하지 않는다: {excinfo.value}")


def test_request_json_does_not_carry_repo_root(tmp_path) -> None:
    """환경 경로를 요청 파일에 실으면 같은 요청이 리포마다 다른 파일이 된다(재정 S4).

    지문은 **본문**의 함수이므로 같은 절차 본문이면 두 리포에서 같은 값이 나온다 — 그것이
    옳은 동작이고, 경로를 파일에 실으면 그 성질이 깨진다.
    """
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415

    request = probe_request()
    directory = FileLaneAdapter(os.path.join(str(tmp_path), "lanes"), REPO).write_request(
        request
    )
    written = load_json(os.path.join(directory, "request.json"))
    if "repo_root" in written:
        pytest.fail(f"request.json 이 repo_root 를 실었다: {written['repo_root']}")
    if sorted(written) != sorted([*REQUEST_JSON_FIELDS, "input_digest"]):
        pytest.fail(f"request.json 의 키 구성이 계약과 다르다: {sorted(written)}")


# ===========================================================================
# ② 응답의 반향 — 누락·불일치의 거부
# ===========================================================================


def test_response_without_echo_is_rejected(tmp_path) -> None:
    """반향을 선택으로 두면 레인은 그 칸을 비우고, 시점 결속은 선언으로만 남는다(재정 P-12 ②)."""
    request = probe_request()
    path = os.path.join(str(tmp_path), "response.json")
    write_probe_response(path, request=request, echo=None)
    with pytest.raises(LaneContractError) as excinfo:
        load_response(request, path)
    if isinstance(excinfo.value, LaneStaleResponseError):
        pytest.fail("반향 **누락**을 낡은 응답으로 분류했다 — 두 사건은 처분이 다르다")
    if "input_digest" not in str(excinfo.value):
        pytest.fail(f"진단이 빠진 키를 지목하지 않는다: {excinfo.value}")


def test_response_echoing_a_stale_digest_is_rejected(tmp_path) -> None:
    """낡은 응답은 스키마를 통과하므로, 여기서 막지 않으면 어떤 검사도 막지 못한다(재정 P-12 ④).

    ★ 이것이 감수 OOS-01 의 재현이다 — 요청이 갱신된 뒤 옛 응답의 **여전히 유효한 항목 ID** 가
    다른 항목으로 미끄러지고, 재번호가 그 결함을 결함 그대로 옮긴다.
    """
    old = probe_request()
    new = probe_request(instructions="| `M2001` | frame width | `12.5` | mm |")
    path = os.path.join(str(tmp_path), "response.json")
    write_probe_response(path, request=old, echo=old.input_digest)

    # 대조군 — 옛 요청으로 읽으면 같은 파일이 정상 통과한다(과잉 제약 배제).
    loaded = load_response(old, path)
    if loaded.input_digest != old.input_digest:
        pytest.fail(f"정상 왕복이 막혔다: {loaded.input_digest}")
    if loaded.response_digest != hashlib.sha256(open(path, "rb").read()).hexdigest():
        pytest.fail("응답 지문이 파일 바이트의 sha256 이 아니다")

    with pytest.raises(LaneStaleResponseError) as excinfo:
        load_response(new, path)
    error = excinfo.value
    if (error.lane_id, error.expected, error.actual) != (
        new.lane_id,
        new.input_digest,
        old.input_digest,
    ):
        pytest.fail(f"예외가 지목한 좌표가 다르다: {error.lane_id} {error.expected} {error.actual}")
    if "낡" not in str(error):
        pytest.fail(f"진단이 '낡은 응답'의 뜻을 말하지 않는다: {error}")


# ===========================================================================
# ③④ 레인 로그 — 지문 기록과 거부 행
# ===========================================================================


def test_lane_log_rows_carry_the_five_digest_keys(tmp_path) -> None:
    """지문이 로그에 남지 않으면 런이 자기가 소비한 응답을 지목하지 못한다(재정 P-12 ③ · S4).

    실측 사고(감수 OOS-02): 같은 요청 자리에 응답이 두 번 쓰였고 커밋본 `472f…` 와 worktree
    `b6ab…` 가 갈렸는데, 로그에 응답 지문이 없어 **런이 정본을 증명하지 못했다**.

    ★ 다섯째 칸 `request_digest`(재정 2026-08-19 S4 · Q8 ③)는 이 통주에서 **`None` 이 정답**
    이다 — 하네스가 쓰는 재생 어댑터는 요청 파일을 쓰지 않으므로 잴 파일이 없다. 칸은 있어야
    하고 값이 없다는 사실은 그대로 적힌다(파일 어댑터 경로의 값 검증은 아래 별도 시험).
    """
    root, outcome, _ = m2.run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"통주가 ok 를 내지 않았다: {outcome['status']}")
    rows = load_json(RunPaths(root).lane_log)
    if not rows:
        pytest.fail("레인 로그가 비었다")
    lanes_dir = RunPaths(root).lanes_dir
    for row in rows:
        for key in (
            "input_digest",
            "echoed_digest",
            "request_digest",
            "response_digest",
            "digest_ok",
        ):
            if key not in row:
                pytest.fail(f"레인 로그 행에 {key} 가 없다: {row}")
        if row["request_digest"] is not None:
            pytest.fail(
                f"재생 어댑터 왕복인데 요청 파일 지문이 적혔다 — 없는 파일을 잰 것이다: {row}"
            )
        if row["input_digest"] != row["echoed_digest"] or not row["digest_ok"]:
            pytest.fail(f"반향이 요청 지문과 다른데 통과했다: {row}")
        # 기록된 응답 지문이 **그 파일의 sha256** 이어야 사람이 손으로 대조할 수 있다.
        path = os.path.join(lanes_dir, *str(row["lane_id"]).split("/"), "response.json")
        actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if row["response_digest"] != actual:
            pytest.fail(
                f"응답 지문이 파일과 다르다: 로그 {row['response_digest']} ≠ 파일 {actual} ({path})"
            )


def test_runner_rejects_a_stale_response_and_records_it(tmp_path) -> None:
    """거부가 예외로만 존재하면 런 폴더에는 아무 흔적도 남지 않는다(재정 P-12 ③④)."""
    root, _ = m2.run_source(tmp_path)
    lanes_root = m2.write_lane_responses(
        root, payloads_by_run={"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    )
    # 통합 레인의 응답만 **다른 요청에 답한 것**으로 바꾼다(감수 OOS-01 이 지목한 그 레인).
    poisoned = os.path.join(lanes_root, "read-a", "synthesize", "batch-0", "response.json")
    body = load_json(poisoned)
    body["input_digest"] = "0" * 64
    with open(poisoned, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False)

    with pytest.raises(LaneStaleResponseError) as excinfo:
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    if excinfo.value.actual != "0" * 64:
        pytest.fail(f"거부가 지목한 반향값이 다르다: {excinfo.value.actual}")

    rows = load_json(RunPaths(root).lane_log)
    rejected = [row for row in rows if row.get("rejected")]
    if len(rejected) != 1:
        pytest.fail(f"거부 행 1건 기대, 실제 {len(rejected)}건 — {rows}")
    row = rejected[0]
    if row["lane_id"] != "read-a/synthesize/batch-0" or row["digest_ok"] is not False:
        pytest.fail(f"거부 행의 좌표·판정이 다르다: {row}")
    if not row.get("reason") or "낡" not in str(row["reason"]):
        pytest.fail(f"거부 사유가 남지 않았다: {row}")
    if os.path.exists(RunPaths(root).material_spec_json):
        pytest.fail("낡은 응답을 거부했는데 재료 명세가 쓰였다")


def test_lane_log_shape_flags_rows_without_digests() -> None:
    """검사가 지문을 보지 않으면 다음 개정이 결속을 지워도 산출물은 아무 말도 하지 않는다."""
    journal = read_stage.LaneJournal()
    journal.rows = [
        # 지문 없는 구 서식 행 — 형태(ⓐⓑⓒ)는 온전하다.
        {"lane_id": "read-a/decompose/batch-0", "read_run": "read-a", "task": "decompose"},
        {"lane_id": "read-b/decompose/batch-0", "read_run": "read-b", "task": "decompose"},
        {
            "lane_id": "read-a/synthesize/batch-0",
            "read_run": "read-a",
            "task": "synthesize",
            "actual_model": "opus-5",
        },
    ]
    row = read_stage.check_lane_log_shape(
        journal, read_runs=("read-a", "read-b"), canonical="read-a"
    )
    rules = [finding.rule for finding in row.findings]
    for expected in (
        "lane-log.request-digest",
        "lane-log.response-digest",
        "lane-log.request-file-digest",
    ):
        if expected not in rules:
            pytest.fail(f"{expected} 가 뜨지 않았다 — 실제 {rules}")
    if rules.count("lane-log.request-digest") != 3:
        pytest.fail(f"요청 지문 결함 3건 기대, 실제 {rules.count('lane-log.request-digest')}")
    # 응답이 도착하지 않은 행까지 응답 지문을 요구하면 미충족 상태가 결함이 된다.
    if rules.count("lane-log.response-digest") != 1:
        pytest.fail(f"응답 지문 결함 1건 기대, 실제 {rules.count('lane-log.response-digest')}")
    # 구 서식 행 3건 전부가 요청 파일 지문 칸을 갖지 않는다(재정 2026-08-19 S4).
    if rules.count("lane-log.request-file-digest") != 3:
        pytest.fail(
            f"요청 파일 지문 결함 3건 기대, 실제 {rules.count('lane-log.request-file-digest')}"
        )


def test_lane_log_shape_exempts_only_explicit_nulls(tmp_path) -> None:
    """제외를 조용히 하면 그 제외가 판정이 아니라 사각지대가 된다(재정 2026-08-19 S4).

    셋을 한 자리에서 가른다. ⓐ 칸이 **없는** 행 = 결함(구 서식으로의 퇴행) ⓑ 값이 **명시적
    `None`** 인 행 = 대상 제외(요청 파일을 쓰지 않는 재생 어댑터) ⓒ **빈 문자열** = 결함
    (있다고 적어 놓고 아무것도 지목하지 않는다). 그리고 제외 건수는 산출에 남는다.
    """
    journal = read_stage.LaneJournal()
    common = {"input_digest": "a" * 64, "response_digest": "b" * 64, "digest_ok": True}
    journal.rows = [
        # ⓐ 칸 없음
        {"lane_id": "read-a/decompose/batch-0", "read_run": "read-a", "task": "decompose",
         **common},
        # ⓑ 명시적 None — 재생 어댑터
        {"lane_id": "read-b/decompose/batch-0", "read_run": "read-b", "task": "decompose",
         "request_digest": None, **common},
        # ⓒ 빈 문자열
        {"lane_id": "read-a/synthesize/batch-0", "read_run": "read-a", "task": "synthesize",
         "request_digest": "", **common},
    ]
    row = read_stage.check_lane_log_shape(
        journal, read_runs=("read-a", "read-b"), canonical="read-a"
    )
    rules = [finding.rule for finding in row.findings]
    if rules.count("lane-log.request-file-digest") != 2:
        pytest.fail(f"요청 파일 지문 결함 2건(ⓐⓒ) 기대, 실제 {rules} ")
    loci = sorted(
        finding.locus for finding in row.findings
        if finding.rule == "lane-log.request-file-digest"
    )
    if loci != ["10-read/lanes/read-a/decompose/batch-0",
                "10-read/lanes/read-a/synthesize/batch-0"]:
        pytest.fail(f"결함이 지목한 좌표가 다르다: {loci}")
    if row.extras.get("request_digest_exempt") != 1:
        pytest.fail(f"제외 건수가 산출에 남지 않았다: {row.extras}")


def test_file_adapter_round_trip_records_the_request_file_digest(tmp_path) -> None:
    """요청 쪽 지문이 없으면 **레인이 읽은 요청서**가 지금 그 파일인지 사후에 못 판정한다.

    재정 2026-08-19 S4(Q8 ③ 승인)가 명한 응답 지문의 거울상이며, 값은 사람이
    `sha256sum request.md` 로 곧장 맞춰 볼 수 있어야 한다 — 그래서 `request.json` 이 아니라
    `request.md` 를 잰다(레인이 실제로 읽는 파일이 그것이다).
    """
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415

    lanes_root = os.path.join(str(tmp_path), "lanes")
    adapter = FileLaneAdapter(lanes_root, REPO)
    request = probe_request()
    directory = adapter.write_request(request)
    write_probe_response(
        os.path.join(directory, "response.json"),
        request=request,
        echo=request.input_digest,
    )

    journal = read_stage.LaneJournal()
    read_stage._dispatch(adapter, [request], journal)
    row = journal.rows[-1]
    with open(os.path.join(directory, "request.md"), "rb") as handle:
        expected = hashlib.sha256(handle.read()).hexdigest()
    if row.get("request_digest") != expected:
        pytest.fail(f"요청 파일 지문이 파일과 다르다: 로그 {row.get('request_digest')} ≠ {expected}")
    if row["request_digest"] == row["input_digest"]:
        pytest.fail("요청 파일 지문과 입력 지문이 같다 — 전자는 지문 행을 포함한 파일 전체다")

    shape = read_stage.check_lane_log_shape(
        journal, read_runs=("read-a",), canonical="read-a"
    )
    if "lane-log.request-file-digest" in [finding.rule for finding in shape.findings]:
        pytest.fail(f"파일 어댑터 왕복인데 요청 파일 지문 결함이 떴다: {shape.findings}")
    if shape.extras.get("request_digest_exempt") != 0:
        pytest.fail(f"파일 어댑터 왕복이 제외로 새어 나갔다: {shape.extras}")


# ===========================================================================
# ⑤ 섀도 원장 — 러너 재진입 다회에도 run_id 당 1행
# ===========================================================================


def test_shadow_ledger_writes_exactly_one_row_per_run(tmp_path) -> None:
    """재진입마다 원장에 적으면 한 run_id 아래 미완성 행이 쌓인다(재정 P-U4 의 "한 행").

    실측 결함(2026-08-18 감수): 통주 1회에 4행이 남았고 앞 3행은 `final_verdict: null` 이었다.
    원장은 추가 전용이라 사후에 지울 수 없으므로 처방은 **애초에 적지 않는 것**이다 —
    `LanePending` 은 오류가 아니라 러너 재진입 상태이며 아직 기록할 관찰이 아니다.

    ★ 원장은 `m2.run_read_stage` 가 주입하는 **격리 루트**에 쌓는다(재정 G6 · P-U2).
    """
    root, _ = m2.run_source(tmp_path)
    full = {"read-a": m2.payload_set(), "read-b": m2.payload_set()}
    ledger = m2.shadow_ledger_for(root)

    def rows() -> list[dict]:
        if not os.path.exists(ledger):
            return []
        return [
            json.loads(line) for line in read_text(ledger).splitlines() if line.strip()
        ]

    # ① read-a 분해만 응답이 있다 → read-b 분해에서 재진입한다(메모 1건 상태).
    lanes_root = m2.write_lane_responses(
        root, payloads_by_run={"read-a": {"decompose": full["read-a"]["decompose"]}}
    )
    with pytest.raises(LanePending):
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    if rows():
        pytest.fail(f"1회차 재진입에 원장이 기입됐다: {rows()}")
    # 재진입 회차도 자기 사실을 적는다 — "아직 쓰지 않았다"가 그 시점의 사실이다.
    pending_pointer = load_json(RunPaths(root).shadow_pointer)
    if (pending_pointer.get("appended"), pending_pointer.get("terminated")) != (False, False):
        pytest.fail(f"재진입 포인터가 기입·종결을 잘못 적었다: {pending_pointer}")

    # ② 두 분해가 다 있다 → 이번에는 접지에서 재진입한다(메모 2건 상태 — 구 결함이 행을
    #    남기던 자리가 바로 여기다).
    m2.write_lane_responses(
        root,
        payloads_by_run={
            name: {"decompose": payloads["decompose"]} for name, payloads in full.items()
        },
    )
    with pytest.raises(LanePending):
        m2.run_read_stage(
            run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
        )
    if rows():
        pytest.fail(f"2회차 재진입에 원장이 기입됐다: {rows()}")

    # ③ 전량 응답 → 런이 종결된다.
    m2.write_lane_responses(root, payloads_by_run=full)
    outcome = m2.run_read_stage(
        run_root=root, adapter=m2.ReplayLaneAdapter(lanes_root), rules=m2.RULES
    )
    if outcome["status"] != "ok":
        pytest.fail(f"통주가 ok 를 내지 않았다: {outcome['status']}")

    ours = [row for row in rows() if row.get("run_id") == m2.RUN_ID]
    if len(ours) != 1:
        pytest.fail(f"run_id 당 1행 기대, 실제 {len(ours)}행 — {ours}")
    if len(ours[0].get("memos") or []) != 2:
        pytest.fail(f"그 한 행이 메모 2건을 싣지 않았다: {ours[0]}")
    if not ours[0].get("final_verdict"):
        pytest.fail(f"종결 런의 행인데 최종 평가가 비었다: {ours[0]}")


# ===========================================================================
# ⑥ 섀도 원장의 **누적 자리** — 법은 worktree 에서 오고 축적은 리포에 남는다
#    (재정 P-U4 × P-U1 — 2026-08-19 보수)
# ===========================================================================


def make_main_and_worktree(tmp_path) -> tuple[str, str]:
    """주 작업 트리 1개 + 그 커밋의 **링크된 worktree** 1개를 만든다.

    이것이 통주 2 의 상황 재현이다 — 런은 `tools/run_worktree.py` 가 만든 격리 체크아웃에서
    돌고(재정 P-U1), 그 안에서 계약 트리 루트(`repo`)는 worktree 를 가리킨다.
    """
    main = os.path.join(str(tmp_path), "main")
    m2.make_law_repo(main)
    worktree = os.path.join(str(tmp_path), "wt")
    proc = subprocess.run(
        ["git", "-C", main, "worktree", "add", "-q", worktree, "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        pytest.fail(f"worktree 생성 실패(exit {proc.returncode}): {proc.stderr}")
    return os.path.realpath(main), os.path.realpath(worktree)


def test_shadow_root_resolves_out_of_a_linked_worktree(tmp_path) -> None:
    """worktree 안에 원장이 서면 축적물은 런과 함께 사라진다(재정 P-U4 의 목적 소멸).

    실측 결함(2026-08-18 통주 2): `.worktrees/<run-id>/ledgers/shadow/screening.jsonl` 4행 ·
    리포 원장 **0행**. 원인은 `shadow_root or repo or _REPO_ROOT` 폴백이 계약 트리 루트와 원장
    루트를 다시 합친 것이며, `_REPO_ROOT` 도 패키지 위치에서 오므로 worktree 를 가리킨다 —
    `repo` 만 지워서는 낫지 않는다. 이 시험이 없으면 그 폴백이 조용히 되살아난다.
    """
    main, worktree = make_main_and_worktree(tmp_path)

    root, source = engine_paths.shadow_ledger_root(repo=worktree)
    if (root, source) != (main, "main-worktree-resolved"):
        pytest.fail(f"worktree 판정 기대 ({main}, main-worktree-resolved), 실제 ({root}, {source})")

    ledger = engine_paths.shadow_screening_ledger(repo=worktree)
    if ledger != os.path.join(main, "ledgers", "shadow", "screening.jsonl"):
        pytest.fail(f"원장 자리가 주 작업 트리가 아니다: {ledger}")
    if ledger.startswith(worktree + os.sep):
        pytest.fail(f"원장이 worktree 안에 섰다 — 구 폴백이 되살아났다: {ledger}")

    # 대조군 2종 — 주 작업 트리는 그대로, 명시 지정은 언제나 이긴다(과잉 제약 배제).
    if engine_paths.shadow_ledger_root(repo=main) != (main, "main-worktree"):
        pytest.fail(f"주 작업 트리 판정이 틀렸다: {engine_paths.shadow_ledger_root(repo=main)}")
    injected = os.path.join(str(tmp_path), "elsewhere")
    if engine_paths.shadow_ledger_root(repo=worktree, shadow_root=injected) != (
        os.path.realpath(injected),
        "explicit",
    ):
        pytest.fail("명시 지정이 판정에 밀렸다 — 격리(재정 G6)가 깨진다")


def test_worktree_run_grows_the_main_repo_ledger(tmp_path) -> None:
    """자리를 고쳐도 **행이 실제로 도착하는지**를 보지 않으면 경로 문자열만 옳아진다.

    ★ `shadow_root=None` 을 **명시로** 넘긴다. 이 시험의 대상이 "지정이 없을 때의 판정"이기
    때문이며, 그럼에도 정적 관문(`test_test_suite_does_not_write_production_shadow_ledger` ④)의
    형식을 지킨다. 그 관문의 **목적**(생산 원장 무오염 — 재정 G6, 과거 1,178행)은 이 시험이
    직접 반증한다: 기입 대상은 `tmp_path` 의 임시 주 작업 트리이고, 아래 ③이 생산 원장의
    바이트가 변하지 않았음을 같은 실행 안에서 확인한다.
    """
    main, worktree = make_main_and_worktree(tmp_path)
    production = engine_paths.shadow_screening_ledger()
    before = m2._ledger_fingerprint(production)

    written = read_stage.append_screening_ledger(
        worktree,
        run_id="example-xx1111111a1-worktree-probe",
        memos=[
            {"read_run": "read-a", "direction": "clear", "note": "합성 메모 A"},
            {"read_run": "read-b", "direction": "concern", "note": "합성 메모 B"},
        ],
        final={"verdict": "go", "reason": "합성"},
        shadow_root=None,
    )

    # ① 주 작업 트리의 원장이 자랐다.
    expected = os.path.join(main, "ledgers", "shadow", "screening.jsonl")
    if written != expected:
        pytest.fail(f"기입 자리 기대 {expected}, 실제 {written}")
    rows = [json.loads(line) for line in read_text(expected).splitlines() if line.strip()]
    if len(rows) != 1 or len(rows[0]["memos"]) != 2:
        pytest.fail(f"주 리포 원장에 메모 2건짜리 1행이 없다: {rows}")

    # ② worktree 안에는 원장이 서지 않았다 — 통주 2 가 남긴 자리다.
    orphan = os.path.join(worktree, "ledgers", "shadow", "screening.jsonl")
    if os.path.exists(orphan):
        pytest.fail(f"원장이 worktree 안에도 생겼다: {orphan}")

    # ③ 생산 원장은 바이트 하나 변하지 않았다(재정 G6).
    after = m2._ledger_fingerprint(production)
    if after != before:
        pytest.fail(f"생산 섀도 원장이 변했다: {before} → {after} ({production})")


def test_unlocatable_main_worktree_is_refused(tmp_path) -> None:
    """모르면 진행하고 알면서 진행하는 것은 다르다 — 아는 채로 사라지는 장부를 만들지 않는다."""
    main = os.path.join(str(tmp_path), "src")
    m2.make_law_repo(main)
    bare = os.path.join(str(tmp_path), "bare.git")
    detached = os.path.join(str(tmp_path), "detached")
    for args in (
        ["git", "clone", "-q", "--bare", main, bare],
        ["git", "-C", bare, "worktree", "add", "-q", detached, "HEAD"],
    ):
        proc = subprocess.run(args, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            pytest.fail(f"{' '.join(args)} 실패(exit {proc.returncode}): {proc.stderr}")

    with pytest.raises(engine_paths.ShadowLedgerRootError) as excinfo:
        engine_paths.shadow_ledger_root(repo=detached)
    for needle in ("격리 체크아웃", "shadow_root"):
        if needle not in str(excinfo.value):
            pytest.fail(f"거부 진단에 {needle!r} 이 없다: {excinfo.value}")

    # 명시 지정은 이 자리에서도 길을 연다 — 거부는 막다른 길이 아니라 지정 요구다.
    injected = os.path.join(str(tmp_path), "ledger-root")
    if engine_paths.shadow_ledger_root(repo=detached, shadow_root=injected)[1] != "explicit":
        pytest.fail("명시 지정으로도 열리지 않는다 — 거부가 처분이 아니라 벽이 되었다")


def test_run_records_which_ledger_it_wrote(tmp_path) -> None:
    """쓴 자리를 적지 않으면 다음에 또 사라진다 — 통주 2 는 사라진 뒤에야 드러났다."""
    root, outcome, _ = m2.run_read(tmp_path)
    if outcome["status"] != "ok":
        pytest.fail(f"통주가 ok 를 내지 않았다: {outcome['status']}")
    pointer = load_json(RunPaths(root).shadow_pointer)
    expected = {
        "root_source": "explicit",          # 하네스가 격리 루트를 지정한다(재정 G6)
        "ledger": m2.shadow_ledger_for(root),
        "appended": True,
        "terminated": True,
        "memo_count": 2,
    }
    actual = {key: pointer.get(key) for key in expected}
    if actual != expected:
        pytest.fail(f"포인터 산출물이 다르다: 기대 {expected}, 실제 {actual}")
    if not os.path.exists(pointer["ledger"]):
        pytest.fail(f"포인터가 가리키는 원장이 실재하지 않는다: {pointer['ledger']}")


# ===========================================================================
# 반증 도구 — 두 실행 모드에서 같은 결과
# ===========================================================================


def test_binding_probe_tool_passes_in_both_modes() -> None:
    """`assert` 로 자기검증하는 도구는 `python3 -O` 에서 공허 통과한다(CLAUDE.md §3)."""
    tool = os.path.join(REPO, "tools", "check_lane_binding.py")
    codes = []
    for argv in ([sys.executable, tool], [sys.executable, "-O", tool]):
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=REPO, check=False)
        codes.append(proc.returncode)
        if "RESULT: PASS" not in proc.stdout:
            pytest.fail(f"{' '.join(argv)} 가 PASS 를 내지 않았다:\n{proc.stdout}\n{proc.stderr}")
    if codes != [0, 0]:
        pytest.fail(f"종료 코드 기대 [0, 0], 실제 {codes}")
