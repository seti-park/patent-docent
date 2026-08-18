#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""레인 왕복 시점 결속의 **변조 실증** 도구 (재정 2026-08-19 P-12).

이 도구가 증명하는 것은 하나다: **러너가 낡은 응답을 실제로 거부하는가**, 그리고 **런이 자기가
소비한 응답 파일을 지목할 수 있는가.** 그 이상은 증명하지 않는다 — 계약의 옳음도, 다른 검사의
집행도 증명하지 않는다.

관문 3종(`check_spec_refs` · `check_schema_enforcement` · `check_validator_enforcement`)과 층이
다르다. 셋은 **문서·스키마·검증기**를 재고, 이 도구는 **러너의 실행 경로**를 잰다. 재정 P-12 의
④는 "지문 불일치 응답은 러너가 거부한다"인데, 그 문장은 계약에 적는 것만으로는 아무것도
보증하지 않는다 — 거부가 실제로 일어나는지는 낡은 응답을 실제로 주입해 보아야 안다.

무엇을 어떻게 보는가 (전부 실제 파일 · 실제 러너 경로 `engine/stages/read.py#_dispatch`)

  ① 정상       요청을 쓰고, 그 지문을 반향한 응답을 놓는다 → 소비되고 레인 로그에
               `digest_ok: true` 와 **응답 파일 바이트의 sha256** 이 남는가.
  ② 낡은 응답  요청 내용을 바꿔(수확 목록 1행) 지문이 달라진 뒤, **구 지문을 반향하는 옛 응답**을
               그대로 둔다 → `LaneStaleResponseError` 로 거부되고 거부 행이 로그에 남는가.
               거부되지 않으면 이 도구의 반증이 실패한 것이다(감수 OOS-01 의 재현).
  ③ 사후 교체  응답을 소비한 뒤 파일을 다른 내용으로 덮어쓴다 → 로그에 기록된 `response_digest`
               가 **현재 파일의 sha256 과 다름**을 보인다. 이것이 "런이 어느 쪽이 정본인지
               증명한다"의 실측이다(감수 OOS-02 는 이 증명이 불가능했던 사건이다).

★ 자기매칭이 성립하지 않는 이유. 이 도구는 탐지 패턴을 갖지 않는다 — 거부의 판정은 전량
`engine/lanes/contract.py#load_response` 와 러너가 내리고, 이 소스는 그 결과를 기대와 대조할
뿐이다. 픽스처도 리포 안에 없다(매 실행마다 임시 디렉터리에 만들고 지운다).

종료 코드 (SPEC §8.3 3항):
  0 = 전건 기대 일치 / 1 = 반증 실패(거부되어야 할 것이 통과했거나 정상이 막혔다) / 2 = 환경 오류

`assert` 를 쓰지 않는다(`python3 -O` 에서 제거되어 망가진 코드가 공허 통과한다 — CLAUDE.md §3).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile

# 실 운용 레인 배정을 흉내 내되 값은 계약에서 읽지 않는다 — 이 도구가 재는 것은 **결속**이고
# 모델 신원 대조가 아니다. 요청·응답이 같은 값을 들고 있으면 그 축은 조용히 통과한다.
LANE_ID = "read-a/decompose/batch-0"
READ_RUN = "read-a"
TASK = "decompose"
MODEL = "opus-5"
EFFORT = "max"
PROCEDURE = "reader/procedure/10-decompose.md"

# 응답 계약은 최소만 둔다. 낡은 응답이 **스키마를 온전히 통과한다**는 사실이 이 결속의 존재
# 이유이므로, 스키마가 대신 잡아 버리면 시나리오 ②가 시험하는 것이 사라진다.
RESPONSE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "lane-response/binding-probe",
    "type": "object",
    "required": ["items"],
    "properties": {"items": {"type": "array"}},
}

# 요청 지시문 — 재정 P-12 가 지목한 "어느 재료 버전"이 실제로 지문에 들어가는지를 보이기 위해
# 수확 목록을 싣는다. ②는 이 표의 한 행만 고친다.
INSTRUCTION_HEAD = (
    "청구항 구간 전량을 분해한다. 아래 수확 목록의 참조 ID 를 `numeric_refs` 로 되가리킨다.\n\n"
    "| 참조 ID | 라벨 | 정규화 값 | 단위 |\n"
    "|---|---|---|---|\n"
)
HARVEST_ROWS_V1 = ("| `M2001` | frame width | `12.0` | mm |",)
HARVEST_ROWS_V2 = ("| `M2001` | frame width | `12.5` | mm |",)

PAYLOAD_OLD = {"items": [{"id": "M1", "kind": "component", "note": "구 판 응답"}]}
PAYLOAD_NEW = {"items": [{"id": "M1", "kind": "component", "note": "사후 교체본"}]}


def fail_env(message: str) -> None:
    """입력·환경 오류로 즉시 종료한다(exit 2)."""
    print(f"ENVIRONMENT ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def write_response(path: str, *, echo: str, payload: dict) -> None:
    """레인이 쓰는 자리를 대신한다. `echo` 가 응답이 반향하는 입력 지문이다."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "lane_id": LANE_ID,
                "model": MODEL,
                "effort": EFFORT,
                "input_digest": echo,
                "payload": payload,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )
        handle.write("\n")


class Report:
    """시나리오별 판정 누적. 판정은 **명시 비교**로만 내린다(assert 금지 — CLAUDE.md §3)."""

    def __init__(self) -> None:
        self.failures: list[str] = []

    def check(self, label: str, *, expected: str, actual: str) -> bool:
        ok = expected == actual
        mark = "[ok]" if ok else "[fail]"
        print(f"  {mark} {label}")
        print(f"        기대 : {expected}")
        print(f"        실측 : {actual}")
        if not ok:
            self.failures.append(label)
        return ok


def build_request(repo: str, rows: tuple[str, ...]):
    from engine.lanes.contract import LaneRequest  # noqa: PLC0415

    _ = repo
    return LaneRequest(
        lane_id=LANE_ID,
        read_run=READ_RUN,
        task=TASK,
        model=MODEL,
        effort=EFFORT,
        prompt_path=PROCEDURE,
        instructions=INSTRUCTION_HEAD + "\n".join(rows),
        slices={"claims": "1. An apparatus comprising a frame."},
        response_schema=RESPONSE_SCHEMA,
        batch=0,
    )


def run_probe(repo: str, workdir: str) -> Report:
    from engine.lanes.contract import LaneStaleResponseError  # noqa: PLC0415
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415
    from engine.stages.read import LaneJournal, _dispatch  # noqa: PLC0415

    report = Report()
    lanes_root = os.path.join(workdir, "10-read", "lanes")
    adapter = FileLaneAdapter(lanes_root, repo)
    response_path = os.path.join(lanes_root, *LANE_ID.split("/"), "response.json")

    # -- ① 정상 --------------------------------------------------------------
    print("\n== ① 정상 — 요청 지문을 반향한 응답은 소비된다 ==")
    request_v1 = build_request(repo, HARVEST_ROWS_V1)
    adapter.write_request(request_v1)
    write_response(response_path, echo=request_v1.input_digest, payload=PAYLOAD_OLD)
    consumed_digest = sha256_file(response_path)

    journal = LaneJournal()
    try:
        responses = _dispatch(adapter, [request_v1], journal)
    except Exception as exc:  # noqa: BLE001 - 정상 경로가 막히는 것도 반증 실패다
        print(f"  [fail] 정상 응답이 소비되지 않았다 — {type(exc).__name__}: {exc}")
        report.failures.append("① 정상 소비")
        return report

    row = journal.rows[-1] if journal.rows else {}
    report.check(
        "요청 지문이 레인 로그에 남는다",
        expected=request_v1.input_digest,
        actual=str(row.get("input_digest")),
    )
    report.check(
        "응답이 그 지문을 반향했다",
        expected=request_v1.input_digest,
        actual=str(responses[0].input_digest),
    )
    report.check("digest_ok", expected="True", actual=str(row.get("digest_ok")))
    report.check(
        "응답 지문 = 소비한 response.json 파일 바이트의 sha256",
        expected=consumed_digest,
        actual=str(row.get("response_digest")),
    )
    print(f"        참고 : `sha256sum {os.path.relpath(response_path, workdir)}` 로 대조 가능")

    # -- ② 낡은 응답 주입 ----------------------------------------------------
    print("\n== ② 낡은 응답 — 요청이 갱신되었는데 옛 응답이 남아 있다 ==")
    request_v2 = build_request(repo, HARVEST_ROWS_V2)
    print(f"  요청 변경: 수확 목록 1행 {HARVEST_ROWS_V1[0]} → {HARVEST_ROWS_V2[0]}")
    print(f"  구 판 지문 : {request_v1.input_digest}")
    print(f"  신 판 지문 : {request_v2.input_digest}")
    report.check(
        "요청 내용이 바뀌면 입력 지문이 바뀐다",
        expected="두 지문이 다르다",
        actual=(
            "두 지문이 다르다"
            if request_v2.input_digest != request_v1.input_digest
            else "두 지문이 같다 — 재료 변경이 지문에 들어가지 않는다"
        ),
    )

    stale_journal = LaneJournal()
    rejected = "거부되지 않았다 — 낡은 응답이 그대로 소비되었다"
    try:
        _dispatch(adapter, [request_v2], stale_journal)
    except LaneStaleResponseError as exc:
        rejected = f"LaneStaleResponseError (반향 {exc.actual[:16]}… ≠ 요청 {exc.expected[:16]}…)"
    except Exception as exc:  # noqa: BLE001
        rejected = f"다른 예외로 죽었다 — {type(exc).__name__}: {exc}"
    report.check(
        "낡은 응답은 러너가 거부한다",
        expected="LaneStaleResponseError",
        actual=rejected.split(" (")[0],
    )
    print(f"        상세 : {rejected}")

    stale_row = stale_journal.rows[-1] if stale_journal.rows else {}
    report.check(
        "거부 사실이 레인 로그에 남는다(rejected · digest_ok)",
        expected="rejected=True digest_ok=False",
        actual=f"rejected={stale_row.get('rejected')} digest_ok={stale_row.get('digest_ok')}",
    )
    report.check(
        "거부 행이 반향된 옛 지문을 지목한다",
        expected=request_v1.input_digest,
        actual=str(stale_row.get("echoed_digest")),
    )

    # -- ③ 응답 사후 교체(OOS-02 재현) ---------------------------------------
    print("\n== ③ 응답 사후 교체 — 소비한 뒤 파일이 바뀌었다 ==")
    write_response(response_path, echo=request_v1.input_digest, payload=PAYLOAD_NEW)
    current_digest = sha256_file(response_path)
    logged = str(row.get("response_digest"))
    print(f"  로그가 지목한 소비본 : {logged}")
    print(f"  현재 파일의 sha256   : {current_digest}")
    report.check(
        "런이 소비한 응답과 현재 파일이 다름을 지문이 드러낸다",
        expected="두 지문이 다르다",
        actual=("두 지문이 다르다" if logged != current_digest else "두 지문이 같다 — 교체를 못 본다"),
    )
    print(
        "        뜻   : 로그의 response_digest 가 정본을 지목하므로, 같은 자리에 응답이 두 번"
        " 쓰여도\n               런이 어느 쪽을 읽었는지 사후에 판정된다(감수 OOS-02 의 처분)."
    )
    return report


def main(argv: list[str] | None = None) -> int:
    default_repo = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    parser = argparse.ArgumentParser(
        prog="check_lane_binding.py",
        description="patent-docent 레인 왕복 시점 결속의 변조 실증 (재정 P-12).",
    )
    parser.add_argument("--repo", default=default_repo, help="리포 루트 (기본: 이 스크립트의 상위 디렉터리)")
    args = parser.parse_args(argv)

    repo = os.path.realpath(args.repo)
    if not os.path.isdir(repo):
        fail_env(f"리포 경로가 디렉터리가 아니다: {args.repo}")
    if not os.path.isfile(os.path.join(repo, *PROCEDURE.split("/"))):
        fail_env(f"절차 문서가 없다: {PROCEDURE} (요청서 렌더가 이 파일을 인라인한다)")
    if repo not in sys.path:
        sys.path.insert(0, repo)
    try:
        import engine.lanes.contract  # noqa: F401,PLC0415
        import engine.stages.read  # noqa: F401,PLC0415
    except Exception as exc:  # noqa: BLE001
        fail_env(f"엔진 모듈을 불러오지 못했다 — {type(exc).__name__}: {exc}")

    print("레인 왕복 시점 결속 — 변조 실증 (재정 2026-08-19 P-12)")
    print(f"  리포: {repo}")

    workdir = tempfile.mkdtemp(prefix="lane-binding-")
    try:
        report = run_probe(repo, workdir)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    if report.failures:
        print(
            f"\nRESULT: FAIL — 반증 실패 {len(report.failures)}건: {', '.join(report.failures)}",
            file=sys.stderr,
        )
        return 1
    print("\nRESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 3종 전건 일치")
    print(
        "        이 도구가 증명한 것은 러너가 낡은 응답을 거부하고 소비본을 지목한다는 것뿐이다."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
