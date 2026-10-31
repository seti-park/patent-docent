"""재정 2026-08-31 T7 — 도면 캡션 어형의 대소문자 폭.

원장 = `docs/decisions/ruling-20260831-06-T7.md` · 상신 = `docs/decisions/D-20260831-03-wo-preflight.md`.

이 파일이 지는 것은 재정 T7 의 **집행 조건 4종 중 셋**이다(넷째 = 전수 시험·관문은 상시 규약).

  ① 반례 golden 을 세우고, **기대값은 golden 파일이 들고 시험은 그 파일을 읽는다.**
     시험에 값을 복제하면 한 벌이 반드시 낡는다(재정 S3·S7 이 어형 입법에 건 조건과 같은 규율).
  ② **`'854` 무회귀** — 캡션 적중 수가 수정 전후로 동일하다. 폭을 넓히는 수정은 기존 원천에서
     **없던 캡션을 만들어 낼 수 있고**, 그 위험이 실현되지 않았음을 수로 보인다.
  ③ **`WO2026-128750` 적중** — 고쳤다는 주장이 아니라 동작을 보인다.

★ ②③ 의 실측 기준값은 **상신 문서의 실측**이며 이 시험이 그것을 붙든다. `'854` 는 리포 안의
런 산출물을 쓰고, WO 원천은 리포 밖 스테이징이라 **없으면 건너뛴다**(skip) — 리포가 자기 밖의
파일에 시험을 걸면 그 시험은 다른 기계에서 반드시 깨진다.
"""

import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from engine.read_view import ReadView  # noqa: E402
from reader.lib.rules import Rules  # noqa: E402

GOLDEN_DIR = os.path.join(
    REPO, "ledgers", "regression", "golden", "rc-0006-figure-caption-case-counterexamples"
)
CASES_PATH = os.path.join(REPO, "ledgers", "regression", "cases.jsonl")


# WO 원천의 도면 절이 선언한 도면 수. 이 수의 정본은 원천 자신이다(`Figure 1`~`Figure 21`).


def load_json(path: str) -> dict:
    if not os.path.isfile(path):
        pytest.fail(f"golden 표본이 없다: {path} — 반례가 사라지면 그 주장은 근거를 잃는다")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def caption_ids(text: str, rules: Rules | None = None) -> list[str]:
    """뷰가 낸 도면 id 목록.

    ★ **정규식 적중 수와 다르다** — 뷰는 같은 도면이 두 번 나오면 첫 행만 취한다
    (`ReadView.figure_captions`). 상신 D-20260831-03 §3 의 `77`·`42` 는 정규식 적중이고
    여기서 세는 것은 중복 제거 후의 도면 id 다. 두 수를 같은 것으로 읽지 마라.
    """
    return [cap.figure_id for cap in ReadView(text, rules or Rules.load()).figure_captions()]


# ---------------------------------------------------------------------------
# ① 규칙 파일이 폭을 선언하고, 코드는 그 선언을 읽는다
# ---------------------------------------------------------------------------


def test_case_insensitivity_is_declared_in_the_rules_file_not_the_code() -> None:
    """민감도는 규칙 파일의 소관이다 — 플래그를 코드에 박으면 어형의 폭이 코드로 샌다.

    반증 대상: 누군가 `rules.py` 에서 `re.IGNORECASE` 를 직접 박고 선언을 지우는 것.
    그러면 규칙 파일만 읽어서는 폭을 알 수 없게 되고, SPEC §4.8 격리 요건 2항
    (탐지 패턴은 코드에서 분리한다)이 캡션 계열에서만 무너진다.
    """
    rules = Rules.load()
    declared = rules.figure_captions.get("case_insensitive")
    if declared is not True:
        pytest.fail(
            "figure_captions.case_insensitive 선언이 없다(재정 T7) — "
            f"실측 = {declared!r}"
        )
    import re

    if not rules.figure_caption_line.flags & re.IGNORECASE:
        pytest.fail("선언은 있는데 컴파일에 반영되지 않았다 — 선언과 집행의 어긋남")


def test_uppercase_only_rules_file_still_compiles_case_sensitive() -> None:
    """선언이 꺼지면 폭도 꺼져야 한다 — 그러지 않으면 선언이 장식이다."""
    import copy
    import re

    raw = copy.deepcopy(Rules.load().raw)
    raw["figure_captions"].pop("case_insensitive", None)
    narrowed = Rules(raw, "<in-memory>")
    if narrowed.figure_caption_line.flags & re.IGNORECASE:
        pytest.fail("선언을 지웠는데도 대소문자를 무시한다 — 플래그가 코드에 박혀 있다")
    if narrowed.figure_caption_line.search("[0030] Figure 1 is a block diagram."):
        pytest.fail("좁힌 폭이 PCT 어형을 여전히 잡는다 — 대조가 성립하지 않는다")


# ---------------------------------------------------------------------------
# ② golden 표본 — 기대값은 파일이 들고 시험은 읽는다
# ---------------------------------------------------------------------------


def test_golden_samples_match_the_real_view() -> None:
    """각 표본의 기대 figure_id 를 실제 뷰가 그대로 낸다."""
    samples = load_json(os.path.join(GOLDEN_DIR, "samples.json"))["samples"]
    if len(samples) < 8:
        pytest.fail(f"표본이 줄었다: {len(samples)} — 반례가 사라지면 주장도 사라진다")
    failures = []
    for sample in samples:
        got = caption_ids(sample["quote"])
        want = list(sample["expect_figure_ids"])
        if got != want:
            failures.append(f"  {sample['id']} ({sample['role']}): got={got} want={want}")
    if failures:
        pytest.fail("golden 표본 불일치:\n" + "\n".join(failures))


def test_golden_holds_both_directions() -> None:
    """적중만 있고 반례가 없으면 '전부 잡는 규칙'도 만점을 받는다.

    반증 대상: 뒷날 누군가 반례 표본을 지우고 적중만 남기는 것.
    """
    samples = load_json(os.path.join(GOLDEN_DIR, "samples.json"))["samples"]
    hits = [s for s in samples if s["expect_figure_ids"]]
    counters = [s for s in samples if not s["expect_figure_ids"]]
    if not hits:
        pytest.fail("적중 표본이 없다 — 폭이 실물을 잡는지 반증되지 않는다")
    if len(counters) < 2:
        pytest.fail(
            f"반례 표본이 {len(counters)}건뿐이다 — 넓힌 폭이 거짓 캡션을 만들지 "
            "않는다는 주장의 근거가 부족하다"
        )


def test_golden_is_registered_in_the_case_ledger() -> None:
    """장부에 등재되지 않은 golden 은 회귀 스위트가 모르는 파일이다(SPEC §6.5 · 재정 N4)."""
    rows = {}
    with open(CASES_PATH, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                row = json.loads(line)
                rows[row["case_id"]] = row
    row = rows.get("rc-0006")
    if row is None:
        pytest.fail(f"cases.jsonl 에 rc-0006 이 없다: {sorted(rows)}")
    base = os.path.join(REPO, "ledgers", "regression", row["base"])
    if not os.path.isfile(base):
        pytest.fail(f"rc-0006 의 base 가 실물을 가리키지 않는다: {row['base']}")
    if row["expect"]["must_detect"] is not False:
        pytest.fail(f"rc-0006 은 반례이므로 must_detect 가 false 여야 한다: {row['expect']}")
    meta = load_json(os.path.join(GOLDEN_DIR, "meta.json"))
    if meta.get("case_id") != "rc-0006":
        pytest.fail(f"meta.json 의 case_id 가 어긋난다: {meta.get('case_id')}")
    if "ruling-20260831-06-T7.md" not in str(meta.get("note") or ""):
        pytest.fail("rc-0006 의 meta.note 가 등재 근거 재정을 가리키지 않는다")


# ---------------------------------------------------------------------------
# ③ 실물 원천 두 벌 — 무회귀와 적중을 수로 보인다
# ---------------------------------------------------------------------------

