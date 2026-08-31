#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""레인 왕복 시점 결속의 **변조 실증** 도구 (재정 2026-08-19 P-12 · S4).

이 도구가 증명하는 것은 하나다: **러너가 낡은 응답을 실제로 거부하는가**, 그리고 **런이 자기가
소비한 응답 파일을 지목할 수 있는가.** 그 이상은 증명하지 않는다 — 계약의 옳음도, 다른 검사의
집행도 증명하지 않는다.

★ 이 도구는 **커밋 전 필수 관문의 넷째**다(재정 2026-08-19 H7 — 승격 승인. 그 전에는 총괄
재량으로 "관문이 아니라 실증 스크립트"였고, 승격이 바꾼 것은 **언제 돌리는가**뿐이다).
앞의 셋(`check_spec_refs` · `check_schema_enforcement` · `check_validator_enforcement`)과 층이
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
  ④ 절차 변조  **요청 필드는 한 글자도 바꾸지 않고** 절차 문서만 고친 뒤 구 응답을 그대로 둔다
               → 거부되는가(재정 2026-08-19 S4 의 재현). 같은 자리에서 **구 규격이었다면
               통과했을 것**임을 함께 보인다 — 구 규격의 지문(요청 필드의 정규 JSON 해시)은 두
               요청에서 **같은 값**이 나오기 때문이다. 이 대조 한 줄이 이 시나리오의 존재 이유다.
               실제 리포는 건드리지 않는다: 임시 작업장 안에 절차 트리 사본을 만들어 그것을
               변조한다.
  ⑤ 위조값     레인 로그의 `request_digest` **값만** `ffff…ffff` 로 바꾼다(파일은 그대로)
               → 신설 검사 `read.lane-log-digest-value` 가 거부하는가. 함께 **형태 검사는 이
               위조를 지금도 통과시킨다**를 보인다(재정 2026-08-31 Q1 이 검사 id 를 나눈 근거).
  ⑥ null 위장  요청 파일을 **실제로 쓴** 행의 지문을 `null` 로 바꾼다 → 제외로 새지 않는가.
               **면제의 자격은 선언이 아니라 사실**이며, 요청 파일이 그 자리에 없을 때만
               면제다. ⑥-b 가 그 뒤집기다 — 파일이 정말 없으면 면제는 **그대로 산다**
               (재정 Q1 의 *"`None` 면제의 현행 축소분을 되돌리지 마라"*).
  ⑦ 정상       정직한 왕복이 값 검사를 통과하고, 그 통과가 **공허하지 않다**(`digest_verified`
               가 실제로 1). 아무것도 대조하지 않아도 `pass` 이므로 이 확인이 함께 선다.

★ ⑤⑥⑦ 이 닫는 것(2026-08-19 감수 D 의 변조표 실측). M-D(값만 위조)와 M-E(`null` 위장)가
**NOT DETECTED** 였고, M-C(소비 후 `request.md` 교체)는 **사람이 손으로 대조해야만** 드러났다.
셋 다 기계 판정으로 옮겨졌으며, 그 판정은 형태 검사가 아니라 **별도 검사 id** 가 낸다 —
재정 2026-08-31 Q1: *"한 검사가 둘을 지면 어느 쪽이 통과시켰는지 판정문에서 사라진다."*

★ 자기매칭이 성립하지 않는 이유. 이 도구는 탐지 패턴을 갖지 않는다 — 거부의 판정은 전량
`engine/lanes/contract.py#load_response` 와 러너가 내리고, 이 소스는 그 결과를 기대와 대조할
뿐이다. 픽스처도 리포 안에 없다(매 실행마다 임시 디렉터리에 만들고 지운다).

★ ④가 재는 결함의 실체(2026-08-19 감수 D 실측). 요청서는 절차 문서 **본문을 인라인**하는데
구 지문은 그 문서의 **경로 문자열**만 쟀다. 그래서 보관된 요청문(29,046 B)과 현행 절차로 재렌더한
요청문(39,152 B)이 같은 지문 `8bcb6066…` 을 들었고, 서로 다른 실제 프롬프트가 같은 시점 표지를
공유했다. 재정 S4 가 지문 대상을 렌더된 요청서 본문 전체로 바꿨고 이 시나리오가 그 처분의 반증이다.

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


def legacy_digest(request) -> str:
    """**구 규격**(재정 S4 이전)의 지문 재현 — 요청 필드 정규 JSON 의 sha256.

    이 함수가 있는 이유는 하나다: 시나리오 ④에서 "구 규격이었다면 이 변조가 통과했다"를
    말이 아니라 값으로 보이기 위해서다. 절차 본문이 아무리 바뀌어도 이 값은 그대로다.
    """
    import hashlib as _hashlib  # noqa: PLC0415
    import json as _json  # noqa: PLC0415

    from engine.lanes.contract import REQUEST_JSON_FIELDS  # noqa: PLC0415

    body = {name: getattr(request, name) for name in REQUEST_JSON_FIELDS}
    blob = _json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_request(repo: str, rows: tuple[str, ...]):
    """요청 1건. `repo` 는 **절차 본문을 어느 트리에서 인라인하는가**다(재정 S4)."""
    from engine.lanes.contract import LaneRequest  # noqa: PLC0415

    return LaneRequest(
        lane_id=LANE_ID,
        read_run=READ_RUN,
        task=TASK,
        model=MODEL,
        effort=EFFORT,
        prompt_path=PROCEDURE,
        repo_root=repo,
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
    # 재정 2026-08-19 S4 · Q8 ③ — 요청 파일 지문은 응답 지문의 거울상이다.
    request_md_path = os.path.join(lanes_root, *LANE_ID.split("/"), "request.md")
    report.check(
        "요청 지문 = 레인이 읽은 request.md 파일 바이트의 sha256",
        expected=sha256_file(request_md_path),
        actual=str(row.get("request_digest")),
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

    # -- ④ 절차 문서 변조 후 구 응답 주입(재정 2026-08-19 S4 의 재현) ---------
    print("\n== ④ 절차 문서 변조 — 요청 필드는 그대로인데 프롬프트가 달라졌다 ==")
    probe_procedure_tampering(repo, workdir, report)

    # -- ⑤⑥⑦ 지문 **값** 대조(재정 2026-08-31 Q1 의 반증) ---------------------
    probe_digest_value(repo, workdir, report)
    return report


def probe_digest_value(repo: str, workdir: str, report: Report) -> None:
    """⑤ 위조값 FAIL · ⑥ `null` 위장 비제외 · ⑦ 정상 통과 (재정 2026-08-31 Q1).

    ★ **세 시나리오 전부 실제 파일 · 실제 러너 경로다** — 로그 행을 손으로 지어내지 않고
    `FileLaneAdapter` 로 요청을 쓰고 `_dispatch` 로 왕복을 돌린 뒤, **그 로그를 변조한다.**
    변조 대상이 러너가 실제로 쓴 산출이어야 이 반증이 성립한다.

    ★ **각 시나리오가 형제 검사(`read.lane-log-shape`)의 판정을 함께 보인다.** 그것이 재정 Q1
    이 검사 id 를 나눈 이유의 실측이며, 이 절의 존재 이유다 — 값 검사가 FAIL 하는 것만 보이면
    *"형태 검사가 이미 잡고 있지 않았나"* 에 답할 수 없다. 답은 **형태 검사가 지금도 통과시킨다**
    이고, 2026-08-19 감수 D 가 `pass checked=5 violations=0` 으로 실측한 그 자리다.
    """
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415
    from engine.stages.read import (  # noqa: PLC0415
        LaneJournal,
        _dispatch,
        check_lane_log_digest_value,
        check_lane_log_shape,
    )

    lanes_root = os.path.join(workdir, "digest-value", "10-read", "lanes")
    adapter = FileLaneAdapter(lanes_root, repo)
    lane_home = os.path.join(lanes_root, *LANE_ID.split("/"))
    request_md = os.path.join(lane_home, "request.md")
    response_path = os.path.join(lane_home, "response.json")

    request = build_request(repo, HARVEST_ROWS_V1)
    adapter.write_request(request)
    write_response(response_path, echo=request.input_digest, payload=PAYLOAD_OLD)
    journal = LaneJournal()
    try:
        _dispatch(adapter, [request], journal)
    except Exception as exc:  # noqa: BLE001
        print(f"  [fail] 기준선 왕복이 막혔다 — {type(exc).__name__}: {exc}")
        report.failures.append("⑤⑥⑦ 기준선 왕복")
        return

    def shape_digest_rules(rows) -> list[str]:
        """형태 검사가 **지문 칸**에 대해 낸 결함만 고른다(다른 형태 결함은 관심사가 아니다)."""
        probe = LaneJournal()
        probe.rows = rows
        row = check_lane_log_shape(probe, read_runs=(READ_RUN,), canonical=READ_RUN)
        return sorted(
            finding.rule
            for finding in row.findings
            if finding.rule.startswith("lane-log.request")
        )

    honest_rows = [dict(entry) for entry in journal.rows]

    # -- ⑦ 정상 통과 --------------------------------------------------------
    print("\n== ⑦ 정상 — 로그의 요청 지문이 그 자리의 파일과 같다 ==")
    probe = LaneJournal()
    probe.rows = [dict(entry) for entry in honest_rows]
    row = check_lane_log_digest_value(probe, lanes_root=lanes_root)
    print(f"  로그가 적은 지문 : {honest_rows[-1].get('request_digest')}")
    print(f"  파일의 sha256    : {sha256_file(request_md)}")
    report.check(
        "정직한 왕복은 값 검사를 통과한다",
        expected="pass",
        actual=row.status,
    )
    report.check(
        "통과가 공허하지 않다(값 대조를 실제로 했다)",
        expected="digest_verified=1",
        actual=f"digest_verified={row.extras.get('digest_verified')}",
    )
    print(
        f"        참고 : `sha256sum {os.path.relpath(request_md, workdir)}` 로 제3자가"
        " 같은 대조를 한다"
    )

    # -- ⑤ 위조값 ----------------------------------------------------------
    print("\n== ⑤ 위조값 — 로그의 지문만 ffff…ffff 로 바꾼다(파일은 그대로) ==")
    forged = [dict(entry) for entry in honest_rows]
    forged[-1]["request_digest"] = "f" * 64
    probe = LaneJournal()
    probe.rows = forged
    row = check_lane_log_digest_value(probe, lanes_root=lanes_root)
    rules = sorted(finding.rule for finding in row.findings)
    report.check(
        "위조값은 값 검사가 거부한다",
        expected="fail",
        actual=row.status,
    )
    report.check(
        "거부 사유가 값 불일치로 지목된다",
        expected="['lane-log.digest-value-mismatch']",
        actual=str(rules),
    )
    report.check(
        "★ 같은 위조를 형태 검사는 지금도 통과시킨다(검사 id 를 나눈 근거)",
        expected="[]",
        actual=str(shape_digest_rules(forged)),
    )
    print(
        "        뜻   : 2026-08-19 감수 D 의 M-D 가 `pass checked=5 violations=0` 으로"
        " 통과했던 자리다.\n               형태와 값은 다른 주장이며, 한 행이 둘을 지면 어느"
        " 쪽이 통과시켰는지 판정문에서 사라진다."
    )

    # -- ⑥ `null` 위장 ------------------------------------------------------
    print("\n== ⑥ null 위장 — 요청 파일을 쓴 행의 지문을 null 로 바꾼다 ==")
    disguised = [dict(entry) for entry in honest_rows]
    disguised[-1]["request_digest"] = None
    probe = LaneJournal()
    probe.rows = disguised
    row = check_lane_log_digest_value(probe, lanes_root=lanes_root)
    rules = sorted(finding.rule for finding in row.findings)
    print(f"  request.md 실재 여부 : {os.path.isfile(request_md)}")
    report.check(
        "null 위장은 제외로 새지 않는다",
        expected="fail",
        actual=row.status,
    )
    report.check(
        "거부 사유가 면제 위장으로 지목된다",
        expected="['lane-log.digest-null-disguise']",
        actual=str(rules),
    )
    report.check(
        "위장 행을 정당한 면제로 세지 않는다",
        expected="exempt_verified=0",
        actual=f"exempt_verified={row.extras.get('exempt_verified')}",
    )
    report.check(
        "★ 같은 위장을 형태 검사는 지금도 면제로 센다(검사 id 를 나눈 근거)",
        expected="[]",
        actual=str(shape_digest_rules(disguised)),
    )
    print(
        "        뜻   : 면제의 자격은 **선언이 아니라 사실**이다 — 요청 파일이 그 자리에"
        " 없을 때만 면제다.\n               감수 D 의 M-E 는 `exempt` 계수만 하나 늘리고"
        " 통과했다."
    )

    # -- ⑥-b 정당한 면제는 그대로 산다(되돌리지 않았음의 실증) ---------------
    print("\n== ⑥-b 정당한 면제 — 요청 파일이 정말 없는 행은 통과한다 ==")
    os.remove(request_md)
    probe = LaneJournal()
    probe.rows = [dict(entry) for entry in disguised]
    row = check_lane_log_digest_value(probe, lanes_root=lanes_root)
    report.check(
        "요청 파일이 없는 행의 null 은 면제로 통과한다",
        expected="pass",
        actual=row.status,
    )
    print(
        "        뜻   : 재정 2026-08-31 Q1 이 *\"`None` 면제의 현행 축소분을 되돌리지"
        " 마라\"* 로 명한 자리다.\n               신설 검사는 면제를 없앤 것이 아니라 그"
        " **자격을 사실로** 판정한다."
    )


def probe_procedure_tampering(repo: str, workdir: str, report: Report) -> None:
    """절차 본문만 바꾸고 요청 필드는 한 글자도 건드리지 않는다.

    ★ **실제 리포를 변조하지 않는다.** 작업장 안에 절차 트리 사본을 만들고 그 사본을 고친다 —
    반증 도구가 자기 리포를 고치면 그 도구는 관문이 아니라 사고다.
    """
    from engine.lanes.contract import LaneStaleResponseError  # noqa: PLC0415
    from engine.lanes.file_adapter import FileLaneAdapter  # noqa: PLC0415
    from engine.stages.read import LaneJournal, _dispatch  # noqa: PLC0415

    mirror = os.path.join(workdir, "repo")
    procedure_src = os.path.join(repo, *PROCEDURE.split("/"))
    procedure_dst = os.path.join(mirror, *PROCEDURE.split("/"))
    os.makedirs(os.path.dirname(procedure_dst), exist_ok=True)
    shutil.copyfile(procedure_src, procedure_dst)

    lanes_root = os.path.join(workdir, "tamper", "10-read", "lanes")
    adapter = FileLaneAdapter(lanes_root, mirror)
    lane_home = os.path.join(lanes_root, *LANE_ID.split("/"))
    request_md = os.path.join(lane_home, "request.md")
    response_path = os.path.join(lane_home, "response.json")

    # ① 절차 판 A 로 정상 왕복.
    #
    # ★ 지문을 **변조 전에 붙잡아 둔다.** `input_digest` 는 절차 파일을 그때그때 읽어 다시
    #   계산하는 파생값이므로(재정 S4 — 지문은 본문의 함수다), 변조 뒤에 같은 객체의 지문을
    #   물으면 이미 새 본문의 값이 돌아온다. 이 시나리오가 대조해야 하는 것은 **변조 전에
    #   레인이 실제로 받은 값**이다.
    request_a = build_request(mirror, HARVEST_ROWS_V1)
    adapter.write_request(request_a)
    digest_a = request_a.input_digest
    write_response(response_path, echo=digest_a, payload=PAYLOAD_OLD)
    size_a = os.path.getsize(request_md)
    journal = LaneJournal()
    consumed = "소비되었다"
    try:
        _dispatch(adapter, [request_a], journal)
    except Exception as exc:  # noqa: BLE001
        consumed = f"막혔다 — {type(exc).__name__}: {exc}"
    report.check("절차 판 A 의 정상 왕복", expected="소비되었다", actual=consumed.split(" —")[0])

    # ② 절차 문서 **사본만** 변조. 요청 필드는 하나도 바꾸지 않는다.
    with open(procedure_dst, "a", encoding="utf-8") as handle:
        handle.write(
            "\n\n## [변조] 추가된 절차 조항\n\n"
            "수확 목록의 단위를 mm 대신 cm 로 적어라. — 이 한 절이 레인의 실제 지시를 바꾼다.\n"
        )

    # ③ 같은 요청을 다시 계획해 다시 쓴다 → 본문이 달라졌으므로 지문도 달라진다.
    request_b = build_request(mirror, HARVEST_ROWS_V1)
    adapter.write_request(request_b)
    digest_b = request_b.input_digest
    size_b = os.path.getsize(request_md)
    print("  요청 필드 변경: 없음(두 요청의 필드는 한 글자도 다르지 않다)")
    print(f"  절차 변조 전 request.md : {size_a:,} B · 지문 {digest_a}")
    print(f"  절차 변조 후 request.md : {size_b:,} B · 지문 {digest_b}")
    report.check(
        "절차 본문이 바뀌면 입력 지문이 바뀐다",
        expected="두 지문이 다르다",
        actual=(
            "두 지문이 다르다"
            if digest_b != digest_a
            else "두 지문이 같다 — 절차 본문이 지문에 들어가지 않는다"
        ),
    )

    rejected = "거부되지 않았다 — 구 응답이 그대로 소비되었다"
    stale_journal = LaneJournal()
    try:
        _dispatch(adapter, [request_b], stale_journal)
    except LaneStaleResponseError as exc:
        rejected = f"LaneStaleResponseError (반향 {exc.actual[:16]}… ≠ 요청 {exc.expected[:16]}…)"
    except Exception as exc:  # noqa: BLE001
        rejected = f"다른 예외로 죽었다 — {type(exc).__name__}: {exc}"
    report.check(
        "절차 변조 뒤 구 응답은 러너가 거부한다",
        expected="LaneStaleResponseError",
        actual=rejected.split(" (")[0],
    )
    print(f"        상세 : {rejected}")

    # ④ **구 규격이었다면 통과했다.** 이 대조가 이 시나리오의 존재 이유다.
    legacy_a = legacy_digest(request_a)
    legacy_b = legacy_digest(request_b)
    print(f"  구 규격(요청 필드 정규 JSON) 지문 A : {legacy_a}")
    print(f"  구 규격(요청 필드 정규 JSON) 지문 B : {legacy_b}")
    report.check(
        "구 규격이었다면 두 요청이 같은 지문을 들었다(= 구 응답이 통과했다)",
        expected="두 지문이 같다",
        actual=("두 지문이 같다" if legacy_a == legacy_b else "두 지문이 다르다"),
    )
    print(
        "        뜻   : 구 규격은 절차 문서를 경로 문자열로만 쟀으므로 본문 변조가 지문에"
        " 닿지 않았다.\n               2026-08-19 감수 D 가 실측한 그 창(29,046 B ↔ 39,152 B,"
        " 지문 동일)을\n               재정 S4 가 닫았고, 위 거부가 그 처분의 실행 반증이다."
    )


def main(argv: list[str] | None = None) -> int:
    default_repo = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    parser = argparse.ArgumentParser(
        prog="check_lane_binding.py",
        description="patent-docent 레인 왕복 시점 결속의 변조 실증 (재정 P-12 · S4).",
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

    print("레인 왕복 시점 결속 — 변조 실증 (재정 2026-08-19 P-12 · S4)")
    print(f"  리포: {repo}")

    # ★ 임시 작업장을 못 만드는 것은 **환경 오류**이지 반증 실패가 아니다(exit 2 — SPEC §8.3 3항).
    #   감싸지 않으면 `FileNotFoundError` 트레이스백과 함께 **exit 1**로 죽고, 그것은
    #   "레인 결속이 깨졌다"와 구별되지 않는다. 2026-08-19 sol 감수 A′ 가 읽기 전용 샌드박스
    #   (쓸 수 있는 `/tmp` 없음)에서 정확히 그 오독을 실측했다 — 재정 H7 로 이 도구가 커밋 전
    #   필수 관문이 된 직후이므로, 환경 때문에 커밋이 막히는데 사유가 "검증 실패"로 적히는
    #   것은 관문의 신호를 마모시킨다.
    try:
        workdir = tempfile.mkdtemp(prefix="lane-binding-")
    except OSError as exc:
        fail_env(
            f"임시 작업장을 만들 수 없다 — {type(exc).__name__}: {exc}. "
            "쓸 수 있는 임시 디렉터리를 TMPDIR 로 지정하라(예: TMPDIR=/dev/shm)"
        )
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
    print(
        "\nRESULT: PASS — 정상 소비 · 낡은 응답 거부 · 사후 교체 탐지 · 절차 변조 거부 · "
        "지문 위조 거부 · null 위장 거부 · 정당한 면제 보존 7종 전건 일치"
    )
    print(
        "        이 도구가 증명한 것은 러너가 낡은 응답을 거부하고 소비본을 지목한다는 것,"
        " 그리고\n        레인 로그의 요청 지문이 그 자리의 파일을 지목한다는 것뿐이다."
        " 그 밖은 증명하지 않는다."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
