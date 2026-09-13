# -*- coding: utf-8 -*-
"""`gate` 스테이지 — L0 결정론 층 + strip + round-trip(재정 2026-09-13 T64 ② · M3).

계약 = `contracts/stages/gate.yaml`(정본 서술 = SPEC §1.10). 이 러너는 변주별 주석본에 대해

① 진입 — 종료선(`partial_until`) · `gate.input-digest`(동결본 · 블루프린트 · 주석본 실재 — 재정 P-C) ·
   대상 변주 = `40-compose/<v>/thread.annotated.md` 가 있는 변주(반려서만 있는 변주는 건너뛴다).
② 변주마다 — `parse(text)` → 오류가 있으면 `annotation.schema`·`annotation.missing-tag` 행만 내고 **나머지
   L0 는 평가하지 않는다**(SPEC §3.2 연쇄 오보 방지 · 행을 내지 않는다) → 오류 0 이면 strip(§3.3 ①~⑤) → L0 규칙
   전량(`contracts/l0-format.yaml#rules[]` 로드 · 출하본 기준) → round-trip 3방향(§3.3) → `l0.json` · `verdict.json`
   (`gate-report/v0`) · `thread.stripped.md` · `thread.json` · `annotation-index.json`.
③ 처분 — 러너는 판정을 **기록**한다. 루프는 `engine/gate/loop.py`(재정 T67 ②)가 돌린다. `decision` 은 가동 층만으로
   정한다(총괄 재량 ⓑ · 미가동 층은 `inactive_layers[]` 에 적는다 · L1 이 아직 돌지 않은 판정문에는 l1·speech_act_flag 를
   계약 `pending_reason` 으로 동적으로 더하고 `run_l1` 이 지운다). 어느 변주에 결함이 있어도 러너 status 는 `ok`
   (기록 완료). 산출이 이미 있으면 `thread_digest` 가 같을 때 재계산 없이 `ok`, 다르면 **직전 산출을
   `50-gate/<v>/rounds/r<n>/` 로 옮긴 뒤** 다시 판정한다(재정 T65 ③ · 총괄 재량 ⓔ — 「덮어씀」을 보존으로 · 사료 규율).
④ `format.stop-shape` 는 매니페스트(`30-figures/assets/manifest.json`)가 실재하면 가동이다(재정 T65 ③). 없는 런에서는
   러너가 `inactive_layers[]` 에 그 사실을 동적으로 더한다 — 판정하지 않은 층을 판정한 것처럼 적지 않는다(재정 N5).
⑤ L1 국소 대조(재정 2026-09-13 T67 ② · M6-a) = `run_l1` — `verdict.json` 이 있고 `l0.pass` 인 변주에만 돈다(총괄 재량 ⓐ ·
   문법이 깨진 초안은 게이트에 도달하기 전에 되돌린다). 첫 진입(루프 개시 전)에 `final-eyes-brief.json` 을 1회 생성하고
   그 지문을 `verdict.json#final_eyes_brief_digest` 에 핀한다 — 이후 재진입마다 바이트 불변을 대조하고 다르면 `StageHaltError`
   (루프 산출물로 바뀐 발췌본은 격이 무효 · 재정 N1). k 요청(`engine/gate/l1/plan.py`) → 파일 어댑터 → 미도착 `pending` →
   전건 도착 → 병합(`merge.py` · §4.5) → 검사 `gate.l1-clean` · `gate.no-rewrite`(L0+L1 fix_directive 전건) ·
   `gate.l1-lane-verified`(총괄 재량 ⓑ) → `l1.json` · `verdict.json#l1` · `decision`(§4.3 enum · 캡 = `gate.yaml#loop.revision_cap`).

★ 게이트는 글을 고치지 않는다(D8) — `fix_directive` 는 지시문이고 러너가 자기 산출에 `gate.no-rewrite` 린트를
  건다. `40-compose/**`·`15-frozen/**`·`20-design/**` 에 쓰지 않는다. 회귀 표본(`ledgers/regression/**`)은 읽기만.
★ 수치·슬롯명·규칙 id·예외 목록·토큰화 정규식을 여기 두지 않는다. 코드 상수는 URL 최소 어형(총괄 재량 ⓒ)과
  `GATE_VERSION` 뿐이다.

`GATE_VERSION` — 게이트 구현 버전(SPEC §4.3). §4.8 강제 조건 4: **심은 결함 100% 검출 + golden 100% 통과를
충족할 때만 상향**한다. 첫 실물이므로 `0.1.0`(§4.3 예시값)에서 시작한다.
"""

from __future__ import annotations

import os
import re
import shutil

from reader.lib.report import CheckRow

from . import (
    StageError,
    StageHaltError,
    failure_entry,
    load_json,
    load_yaml,
    read_text,
    rows_to_dicts,
    sha256_bytes,
    sha256_file,
    verify_declared_inputs,
    write_json,
    write_text,
)
from .design import latest_frozen, terminus_index
from ..annotation.index import annotation_dict, build_index, build_thread
from ..gate.l1 import merge as l1_merge
from ..gate.l1 import plan as l1_plan
from ..gate.l2 import lint as l2_lint
from ..gate.l2 import plan as l2_plan
from ..lanes.contract import LanePending
from ..lanes.file_adapter import FileLaneAdapter
from ..annotation.parse import parse as parse_annotation
from ..annotation.reassemble import reassemble
from ..annotation.strip import RESIDUAL_TAG_RE, _reference_strip, strip
from ..figures import asset_paths as manifest_asset_paths
from ..gate.l0.rules_format import MANIFEST_ABSENT_REASON, R_STOP_SHAPE
from ..gate.l0 import L0Context, L0Law, Rule, load_rules_from_law, stamp_ruleset
from ..gate.l0.weighted_length import EMOJI_APPROXIMATION_NOTE, weighted_length
from ..paths import LANES_DIRNAME, REVISIONS_DIRNAME, ROUNDS_DIRNAME, RunPaths, load_format_parameters, load_stage_contract, repo_root
from ..pens import registry

STAGE_ID = "gate"
GATE_VERSION = "0.1.0"
LAYER_L0 = "l0"
LAYER_L1 = "l1"
LAYER_L2 = "l2"
#: L1 이 아직 돌지 않은 판정문에 동적으로 적는 층(계약 `layers.<layer>.pending_reason` 이 문언을 든다).
L1_PENDING_LAYERS = ("l1", "speech_act_flag")
#: L2 가 아직 돌지 않은 판정문에 동적으로 적는 층(재정 T69 ⑥) — `run_l2` 가 지운다.
L2_PENDING_LAYERS = ("l2",)
MEMO_ID_FORMAT = "m-l2-{:03d}"
#: 재판정 보존(`rounds/r<n>/`)에서 **제자리에 두는** 것 — 루프 개시 전 동결물(발췌본)과 보존·라운드 디렉터리 자신.
PRESERVE_KEEP = ("final-eyes-brief.json", "l2.md", ROUNDS_DIRNAME, REVISIONS_DIRNAME)
BRIEF_KIND = "final-eyes-brief"

#: URL 최소 어형(총괄 재량 ⓒ) — 시트에 URL 문법이 없다. `https?://…` 와 `www.…` 의 비공백 연속.
URL_RE = re.compile(r"https?://\S+|www\.\S+")
#: `gate.no-rewrite` — 따옴표로 감싼 5토큰 이상의 EN 문장(SPEC §4.7 기제 3 · 탐지 범위의 한계도 그 절에).
_QUOTED_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
_EN_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
NO_REWRITE_TOKENS = 5

CHECK_ENTRY = "gate.input-digest"
CHECK_L0_CLEAN = "gate.l0-clean"
CHECK_L1_CLEAN = "gate.l1-clean"
CHECK_L1_LANE_VERIFIED = "gate.l1-lane-verified"
CHECK_INDEX = "gate.annotation-index"
CHECK_NO_REWRITE = "gate.no-rewrite"
CHECK_NO_SCORE = l2_lint.CHECK_ID
CHECK_FORWARD = "strip.roundtrip-forward"
CHECK_REVERSE = "strip.roundtrip-reverse"
CHECK_REASSEMBLY = "strip.reassembly"
CHECK_RESIDUAL = "strip.residual-tag"

DECISION_ADVANCE = "advance"
DECISION_REVISE = "revise"
DECISION_ESCALATE = "escalate"
STATE_SKIPPED = "material-defect"

LEXICON = {
    "defect_catalog": ("contracts", "lexicon", "defect-catalog.yaml", "entries"),
    "speech_act": ("contracts", "lexicon", "speech-acts.yaml", "predicates"),
    "score_lint": ("contracts", "lexicon", "score-lint.yaml", "patterns"),
}
PARAMETERS_REL = ("contracts", "parameters.yaml")


# ---------------------------------------------------------------------------
# 작은 도구
# ---------------------------------------------------------------------------


def _check_terminus(meta: dict, repo: str, contract: dict) -> None:
    if meta.get("run_kind") != "partial":
        return
    until = str(meta.get("partial_until", ""))
    if terminus_index(repo, until) < terminus_index(repo, STAGE_ID):
        entry = failure_entry(contract, "partial_until 종료선")
        raise StageHaltError(
            f"[{entry.get('action')}] partial_until={until!r} 은 gate 앞의 종료선이다 — "
            f"{entry.get('note')}. 연장 봉투(extension-envelope/v0)로 종료선을 옮긴 뒤 다시 부른다"
        )


def inactive_layers(contract: dict, *, l1_pending: bool = False, l2_pending: bool = False) -> tuple[dict, list[dict]]:
    """계약 `layers` 블록 → (블록 사본, `inactive_layers[]` 배열). 목록을 코드가 들지 않는다.

    `l1_pending` = L1 이 아직 돌지 않은 판정문(gate-l0 만 돈 시점) — 가동 층이라도 판정하지 않았으므로 계약의
    `pending_reason` 으로 적는다(재정 N5 · T67 ②). `run_l1` 이 그 행을 지운다. `l2_pending` 은 같은 격이며 `run_l2` 가 지운다(T69 ⑥).
    """
    block = {key: value for key, value in (contract.get("layers") or {}).items() if isinstance(value, dict)}
    rows: list[dict] = []
    for layer, entry in block.items():
        status = str(entry.get("status", ""))
        if status == "inactive":
            rows.append({"layer": layer, "reason": str(entry.get("reason", "")), "ruling": str(entry.get("ruling", ""))})
        elif status == "active" and ((l1_pending and layer in L1_PENDING_LAYERS) or (l2_pending and layer in L2_PENDING_LAYERS) or (layer == "final_eyes" and l1_pending)):
            rows.append({"layer": layer, "reason": str(entry.get("pending_reason", "")) or "미실행", "ruling": str(entry.get("ruling", ""))})
    return block, rows


def revision_cap(contract: dict) -> int:
    """국소 수정 캡 — `gate.yaml#loop.revision_cap`(D8 · 값은 계약이 든다)."""
    value = (contract.get("loop") or {}).get("revision_cap")
    if not isinstance(value, int) or value < 1:
        raise StageError("gate.yaml#loop.revision_cap 이 없다")
    return value


def decide(*, l0_pass: bool, l1_pass: bool | None, revision_round: int, cap: int, spec_ok: bool = True) -> str:
    """§4.3 `decision` enum — 가동·판정된 층만으로. `l1_pass is None` = L1 미판정(그 사실은 inactive_layers[] 가 든다)."""
    if not spec_ok:
        return DECISION_ESCALATE
    if l0_pass and (l1_pass is None or l1_pass):
        return DECISION_ADVANCE
    return DECISION_REVISE if int(revision_round) < int(cap) else DECISION_ESCALATE


def legislated(repo: str) -> dict:
    """카탈로그·술어·린트 파일의 version 과 항목 수를 **읽어서** 날인한다(재정 R7 · N4)."""
    out: dict = {}
    for key, (*parts, list_key) in LEXICON.items():
        data = load_yaml(os.path.join(repo, *parts))
        entries = data.get(list_key)
        count = len(entries) if isinstance(entries, list) else 0
        if key == "defect_catalog":
            out["defect_catalog_version"], out["defect_catalog_entries"] = str(data.get("version")), count
        elif key == "speech_act":
            out["speech_act_predicate_version"], out["speech_act_predicates"] = str(data.get("version")), count
        else:
            out["score_lint_version"], out["score_lint_patterns"] = str(data.get("version")), count
    return out


def l1_k(repo: str) -> int:
    data = load_yaml(os.path.join(repo, *PARAMETERS_REL))
    value = (data.get("adjustable") or {}).get("gate.l1.k")
    if not isinstance(value, int):
        raise StageError("parameters.yaml#adjustable.gate.l1.k 가 없다")
    return value


def no_rewrite_violations(directive: str) -> list[str]:
    """따옴표 속 EN 토큰 5개 이상인 구절 목록(비면 통과)."""
    hits: list[str] = []
    for match in _QUOTED_RE.finditer(directive or ""):
        if len(_EN_TOKEN_RE.findall(match.group(1))) >= NO_REWRITE_TOKENS:
            hits.append(match.group(1))
    return hits


def _load_manifest(paths: RunPaths) -> dict | None:
    path = paths.figures_manifest_json
    return load_json(path) if os.path.isfile(path) else None


def _asset_paths(manifest: dict | None) -> dict[str, str]:
    """헤더 fig 자산 id → asset_path(`engine/figures/asset_paths` — stop-shape 와 같은 해소 규칙)."""
    return manifest_asset_paths(manifest)


def _round_number(gate_dir: str) -> int:
    """다음 보존 회차 번호 = 기존 `rounds/r<n>/` 수 + 1."""
    rounds = os.path.join(gate_dir, ROUNDS_DIRNAME)
    if not os.path.isdir(rounds):
        return 1
    used = [int(name[1:]) for name in os.listdir(rounds) if re.fullmatch(r"r[1-9][0-9]*", name)]
    return (max(used) + 1) if used else 1


def _preserve_previous(paths: RunPaths, variant: str) -> str | None:
    """직전 판정 산출 전량을 `50-gate/<v>/rounds/r<n>/` 로 옮긴다. 옮긴 자리를 돌려준다(없으면 None).

    옮기는 것 = 판정 파일(l0·l1·verdict·strip 산출)과 L1 레인 왕복(`lanes/`). **제자리에 두는 것** = `final-eyes-brief.json`
    (루프 개시 전 동결물 · 재정 N1 — 옮기면 「1회 생성·불변」이 깨진다) · **`l2.md`**(위상이 한 번 닫히는 판단 산출 ·
    D8 · 옮기면 재판정마다 CP2 필수 표면이 사라지고 `run_l2` 가 첫 실행으로 보인다) · `rounds/` · `revisions/`(라운드 사료 자신).
    """
    gate_dir = paths.gate_dir(variant)
    if not os.path.isdir(gate_dir):
        return None
    names = [name for name in os.listdir(gate_dir) if name not in PRESERVE_KEEP
             and (os.path.isfile(os.path.join(gate_dir, name)) or name == LANES_DIRNAME)]
    if not names:
        return None
    target = paths.gate_round_dir(variant, _round_number(gate_dir))
    if os.path.exists(target):
        raise StageError(f"보존 자리가 이미 있다 — 덮어쓰지 않는다: {target}")
    os.makedirs(target)
    for name in names:
        shutil.move(os.path.join(gate_dir, name), os.path.join(target, name))
    return target


def _total_words(stripped) -> int:
    return sum(len(tweet.text.split()) for tweet in stripped.tweets)


def _number_records(kind: str, layer: str, records: list[dict]) -> list[dict]:
    out: list[dict] = []
    for index, record in enumerate(records, start=1):
        out.append({"id": f"{kind}-{layer}-{index:03d}", "layer": layer, **record})
    return out


# ---------------------------------------------------------------------------
# 변주 1건 판정
# ---------------------------------------------------------------------------


def judge_variant(*, text: str, variant: str, run_id: str, spec_version: int, spec_digest: str, frozen: dict,
                  meta: dict, law: L0Law, rules: list[Rule], repo: str, contract: dict, manifest: dict | None,
                  slot_enum, entry_row: CheckRow | None = None) -> dict:
    """주석본 텍스트 → `{verdict, l0, thread, index, stripped_md, rows}`. 파일 I/O 없음(순수).

    `entry_row` = 러너의 진입 검사 행(`gate.input-digest`) — verdict.json#checks[] 의 첫 행으로 싣는다.
    """
    layers_block, inactive = inactive_layers(contract, l1_pending=True, l2_pending=True)
    if manifest is None and not any(row.get("layer") == R_STOP_SHAPE for row in inactive):
        # 계약은 가동으로 적었으나 이 런에는 자산층이 없다 — 판정 못 한 층을 그대로 적는다(재정 N5 · T65 ③).
        inactive = [*inactive, {"layer": R_STOP_SHAPE, "reason": MANIFEST_ABSENT_REASON, "ruling": "재정 2026-09-13 T65 ③"}]
    parsed = parse_annotation(text, slot_enum=slot_enum)
    weighted_config = law.param("format-parameters.yaml#weighted_length")
    ctx = L0Context(law=law, repo=repo, parsed=parsed, stripped=None, index=None, frozen=frozen,
                    spec_digest=spec_digest, meta=meta, manifest=manifest, inactive=layers_block, url_re=URL_RE,
                    slot_enum=tuple(slot_enum))
    rows: list[CheckRow] = [entry_row] if entry_row is not None else []
    defects: list[dict] = []
    flags: list[dict] = []
    thread = index = None
    stripped = None
    weighted_counts: list[int] = []

    digest_ok = str(parsed.frontmatter.get("spec_digest", "")) == spec_digest if isinstance(parsed.frontmatter, dict) else False
    annotation_ids = ("annotation.schema", "annotation.missing-tag")
    by_id = {rule.id: rule for rule in rules}

    if parsed.errors or not digest_ok:
        # 연쇄 오보 방지 — 주석층이 깨졌으면 하위 규칙 행을 내지 않는다(§3.2).
        for rule_id in annotation_ids:
            result = by_id[rule_id].run(ctx)
            rows.append(stamp_ruleset(result.row, law, len(rules)))
            defects.extend(result.defects)
    else:
        stripped = strip(text)
        index = build_index(parsed, stripped, run_id=run_id, variant=variant, spec_version=spec_version)
        thread = build_thread(stripped, run_id=run_id, variant=variant, spec_version=spec_version, spec_digest=spec_digest,
                              weighted=lambda body: weighted_length(body, weighted_config, URL_RE),
                              asset_paths=_asset_paths(manifest))
        ctx.stripped, ctx.index = stripped, index
        for rule in rules:
            result = rule.run(ctx)
            rows.append(stamp_ruleset(result.row, law, len(rules)))
            if rule.veto:
                defects.extend(result.defects)
            else:
                # veto: false 규칙의 산출은 defect 가 아니라 flag 다(§4.4.4) — 판정문에 결함으로 실리지 않는다.
                flags.extend({**d, "note": d["fix_directive"], "origin": "advisory-rule"} for d in result.defects)
            flags.extend(result.flags)
            if rule.id == "format.body-length":
                weighted_counts = list(result.row.extras.get("weighted_char_counts") or [])
        rows.extend(_strip_rows(text, stripped, thread, index, parsed))

    defect_records = _number_records("d", LAYER_L0, [{k: v for k, v in d.items()} for d in defects])
    flag_records = _number_records("f", LAYER_L0, [
        {"rule": f["rule"], "locus": f["locus"], "note": f["note"], "origin": f.get("origin", "advisory-rule")} for f in flags
    ])
    l0_pass = not defect_records

    clean = CheckRow(check_id=CHECK_L0_CLEAN, checked=1)
    if not l0_pass:
        clean.add(CHECK_L0_CLEAN, "l0.json#defects", str(len(defect_records)), "0", "L0 결함이 남아 있다 — 국소 수정 지시로 돌아간다")
    rows.append(clean)
    rewrite = CheckRow(check_id=CHECK_NO_REWRITE, checked=len(defect_records))
    for record in defect_records:
        for hit in no_rewrite_violations(record["fix_directive"]):
            rewrite.add(CHECK_NO_REWRITE, record["id"], hit, "지시문(어디를·어느 재료로)", "fix_directive 가 따옴표 속 EN 문장을 담았다 — 게이트가 필자가 되었다(D8)")
    rows.append(rewrite)

    l0_block = {"pass": l0_pass, "defects": defect_records, "flags": flag_records,
                "checks": rows_to_dicts([row for row in rows if row.check_id in by_id])}
    row_dicts = rows_to_dicts(rows)
    total_words = _total_words(stripped) if stripped is not None else 0
    extreme_bounds = law.param("format-parameters.yaml#total_words_extreme")
    extreme = total_words < int(extreme_bounds["below"]) or total_words > int(extreme_bounds["above"])
    verdict = {
        "schema": "gate-report/v0",
        "run_id": run_id,
        "variant": variant,
        "gate_version": GATE_VERSION,
        "spec_version": int(spec_version),
        "spec_digest": spec_digest,
        "thread_digest": sha256_bytes(text.encode("utf-8")),
        "l0": l0_block,
        "l1": {"pass": None, "k": l1_k(repo), "votes": [], "defects": [], "flags": [], "disagreement_log": []},
        "l2": {"memos": []},
        "checks": row_dicts,
        "legislated": legislated(repo),
        "vacuous_pass": [row["check_id"] for row in row_dicts if row["vacuous"] != "none"],
        "advisory_measurements": {
            "total_words": total_words, "extreme": extreme, "weighted_char_counts": weighted_counts,
            "note": EMOJI_APPROXIMATION_NOTE,
        },
        "final_eyes": {"verdict": None, "veto_reason": None, "observations": [], "inputs_read": []},
        "inactive_layers": inactive,
        "decision": decide(l0_pass=l0_pass, l1_pass=None, revision_round=0, cap=revision_cap(contract)),
        "revision_round": 0,
    }
    return {"verdict": verdict, "l0": l0_block, "thread": thread, "index": index,
            "stripped_md": stripped.stripped_md if stripped is not None else None, "rows": rows,
            "annotation": annotation_dict(parsed)}


def _strip_rows(text: str, stripped, thread: dict, index: dict, parsed) -> list[CheckRow]:
    rows: list[CheckRow] = []
    forward = CheckRow(check_id=CHECK_FORWARD, checked=1)
    reference = _reference_strip(text)
    if stripped.stripped_md != reference:
        forward.add(CHECK_FORWARD, "thread.stripped.md", sha256_bytes(stripped.stripped_md.encode("utf-8")),
                    sha256_bytes(reference.encode("utf-8")), "strip 이 본문을 슬쩍 고쳤다 — 참조 구현과 바이트가 다르다(§3.3 순방향)")
    rows.append(forward)
    reverse = CheckRow(check_id=CHECK_REVERSE, checked=1)
    rebuilt = reassemble(thread, index)
    if rebuilt != text:
        reverse.add(CHECK_REVERSE, "thread.annotated.md", sha256_bytes(rebuilt.encode("utf-8")), sha256_bytes(text.encode("utf-8")),
                    "thread.json + annotation-index.json 으로 원본을 복원하지 못했다 — 변환 과정의 정보 손실(§3.3 역방향)")
    rows.append(reverse)
    reassembly = CheckRow(check_id=CHECK_REASSEMBLY, checked=1)
    joined = "\n\n".join(t["text"] for t in thread["tweets"]) + "\n"
    if joined != stripped.stripped_md:
        reassembly.add(CHECK_REASSEMBLY, "thread.json#tweets[].text", sha256_bytes(joined.encode("utf-8")),
                       sha256_bytes(stripped.stripped_md.encode("utf-8")), "인간본과 기계본이 표류했다(§3.3 재조립)")
    rows.append(reassembly)
    residual = CheckRow(check_id=CHECK_RESIDUAL, checked=len(stripped.tweets))
    for tweet in stripped.tweets:
        for match in RESIDUAL_TAG_RE.finditer(tweet.text):
            residual.add(CHECK_RESIDUAL, f"T{tweet.n}", match.group(0), "(없음)", "출하본에 주석 태그 잔존 — strip 정규식 결함(§3.3 안전망)")
    rows.append(residual)
    index_row = CheckRow(check_id=CHECK_INDEX, checked=parsed.sentence_count)
    indexed = sum(len(t["sentences"]) for t in index["tweets"])
    if indexed != parsed.sentence_count:
        index_row.add(CHECK_INDEX, "annotation-index.json", str(indexed), str(parsed.sentence_count), "인덱스 문장 수가 초안 문장 수와 다르다")
    for t_parsed, t_index in zip(parsed.tweets, index["tweets"]):
        for s_parsed, s_index in zip(t_parsed.sentences, t_index["sentences"]):
            if list(s_parsed.citations) != list(s_index["citations"]) or bool(s_parsed.narrative) != bool(s_index["narrative"]):
                index_row.add(CHECK_INDEX, f"T{t_parsed.n}/S{s_parsed.i}", str(s_index["citations"]), str(list(s_parsed.citations)),
                              "인덱스의 인용 ID 가 초안과 다르다")
    rows.append(index_row)
    return rows


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


def _existing_digest(paths: RunPaths, variant: str) -> str | None:
    path = paths.verdict_json(variant)
    if not os.path.isfile(path):
        return None
    try:
        return str(load_json(path).get("thread_digest"))
    except (OSError, ValueError):
        return None


def _summary(verdict: dict) -> dict:
    counts: dict[str, int] = {}
    for record in verdict["l0"]["defects"]:
        counts[record["rule"]] = counts.get(record["rule"], 0) + 1
    return {"l0_pass": bool(verdict["l0"]["pass"]), "decision": verdict["decision"],
            "defects": len(verdict["l0"]["defects"]), "defects_by_rule": counts, "flags": len(verdict["l0"]["flags"]),
            "thread_digest": verdict["thread_digest"]}


def run(*, run_root: str, repo: str | None = None, variants=None, strip_only: bool = False) -> dict:
    """gate 스테이지 1회 진입(L0). `strip_only` = 파싱 오류 0 인 변주에 strip 산출 3종만(verdict 없이 · 열람 준비용).

    반환 = `{status, variants: {v: {l0_pass, decision, defects, paths} | {skipped}}, rows: {v: [...]}, reason_label}`.
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)

    # ① 진입
    _check_terminus(meta, repo, contract)
    frozen_row = latest_frozen(meta)
    version = int(frozen_row["spec_version"])
    spec_digest = str(frozen_row.get("spec_digest", ""))
    all_variants = list(registry.variant_ids(contract=load_stage_contract("compose", repo)))
    wanted = [v for v in (variants or all_variants)]
    unknown = [v for v in wanted if v not in all_variants]
    if unknown:
        raise StageError(f"계약에 없는 변주다: {unknown} (compose.yaml#lane.variants = {all_variants})")
    entry_row = verify_declared_inputs(paths, contract, STAGE_ID, inputs={"spec_version": version, "variants": wanted})
    frozen_path = paths.frozen_spec(version)
    if sha256_file(frozen_path) != spec_digest:
        raise StageError("동결본 실측 지문이 run.yaml 기록과 다르다")
    frozen = load_json(frozen_path)
    law = L0Law.load(repo)
    rules = load_rules_from_law(law)
    slot_enum = list(load_format_parameters(repo)["parameters"]["slot_enum"]["value"])
    manifest = _load_manifest(paths)
    run_id = str(meta.get("run_id", ""))

    variants_out: dict[str, dict] = {}
    rows_out: dict[str, list[CheckRow]] = {}
    for variant in wanted:
        source = paths.thread_annotated(variant)
        if not os.path.isfile(source):
            variants_out[variant] = {"skipped": STATE_SKIPPED if os.path.isfile(paths.material_defect(variant)) else "no-draft"}
            continue
        text = read_text(source)
        digest = sha256_bytes(text.encode("utf-8"))
        previous = _existing_digest(paths, variant)
        previous_verdict = load_json(paths.verdict_json(variant)) if previous is not None else {}
        final_veto = (previous_verdict.get("final_eyes") or {}).get("verdict") == "veto"
        from ..gate.loop import open_round
        final_revision = final_veto and open_round(paths, variant) is not None
        prior_l2 = read_text(paths.l2_md(variant)) if os.path.isfile(paths.l2_md(variant)) else None
        if not strip_only and previous == digest and not final_revision:
            verdict = previous_verdict
            variants_out[variant] = {**_summary(verdict), "reentered": True, "paths": _paths_of(paths, variant)}
            rows_out[variant] = [entry_row]
            continue
        preserved = None
        if not strip_only and previous is not None and (previous != digest or final_revision):
            preserved = _preserve_previous(paths, variant)
        outcome = judge_variant(text=text, variant=variant, run_id=run_id, spec_version=version, spec_digest=spec_digest,
                                frozen=frozen, meta=meta, law=law, rules=rules, repo=repo, contract=contract,
                                manifest=manifest, slot_enum=slot_enum, entry_row=entry_row)
        paths.ensure_gate_dirs([variant])
        if outcome["stripped_md"] is not None:
            write_text(paths.thread_stripped_md(variant), outcome["stripped_md"])
            write_json(paths.thread_json(variant), outcome["thread"])
            write_json(paths.annotation_index_json(variant), outcome["index"])
        if strip_only:
            stripped_ok = outcome["stripped_md"] is not None
            variants_out[variant] = {"stripped": stripped_ok, "parse_errors": 0 if stripped_ok else len(outcome["l0"]["defects"]),
                                     "paths": _paths_of(paths, variant)}
            rows_out[variant] = list(outcome["rows"])
            continue
        if prior_l2 is not None:
            # 재판정(결함 루프·최종 심급 국소 재진입)은 L2 의 위상을 다시 열지 않는다 — 메모는 1회, 자유 리비전도 1회다(D8).
            # 판정문은 회차마다 새로 쓰이므로 L2 블록과 소진 표시를 여기서 승계하지 않으면 CP2 표면과 위상 봉쇄가 함께 사라진다.
            if previous_verdict.get("l2"):
                outcome["verdict"]["l2"] = previous_verdict["l2"]
            if previous_verdict.get("free_revision_used") is not None:
                outcome["verdict"]["free_revision_used"] = previous_verdict["free_revision_used"]
            elif os.path.isdir(paths.free_revision_dir(variant)):
                outcome["verdict"]["free_revision_used"] = True   # 소진 사실의 정본은 디스크다
            write_text(paths.l2_md(variant), prior_l2)
            outcome["verdict"]["inactive_layers"] = [r for r in outcome["verdict"]["inactive_layers"] if r["layer"] != "l2"]
        write_json(paths.l0_json(variant), outcome["l0"])
        write_json(paths.verdict_json(variant), outcome["verdict"])
        variants_out[variant] = {**_summary(outcome["verdict"]), "reentered": False, "paths": _paths_of(paths, variant),
                                 "preserved_previous": preserved}
        rows_out[variant] = list(outcome["rows"])

    judged = [v for v, s in variants_out.items() if "skipped" not in s]
    label = None
    skipped = [f"{v}={s['skipped']}" for v, s in variants_out.items() if "skipped" in s]
    if skipped:
        label = "건너뜀 " + ", ".join(skipped)
    if not judged:
        raise StageError("판정할 변주가 없다 — 주석본이 있는 변주가 0 이다")
    return {"status": "ok", "variants": variants_out, "rows": rows_out, "reason_label": label}


# ---------------------------------------------------------------------------
# L1 국소 대조 (재정 2026-09-13 T67 ② · M6-a)
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    import datetime as _dt  # noqa: PLC0415

    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_final_eyes_brief(*, meta: dict, verdict: dict, thread: dict, k: int) -> dict:
    """최종 심급 발췌본(SPEC §1.10 표 · 재정 N1) — 숫자 화이트리스트 · k · 슬롯 매핑 · 재료 판 지문. 블루프린트 전문·논지·의도 없음."""
    whitelist = []
    for entry in meta.get("numeric_whitelist") or []:
        if isinstance(entry, dict):
            whitelist.append({key: entry.get(key) for key in ("pattern", "rationale", "added_by", "approved_in")})
    return {
        "kind": BRIEF_KIND,
        "run_id": str(meta.get("run_id", "")),
        "variant": str(verdict.get("variant", "")),
        "spec_version": int(verdict.get("spec_version", 0)),
        "spec_digest": str(verdict.get("spec_digest", "")),
        "numeric_whitelist": whitelist,
        "k": int(k),
        "slots": [{"n": int(t["n"]), "slot": str(t["slot"])} for t in (thread.get("tweets") or [])],
        "generated_before_loop": True,
        "revision_round_at_generation": int(verdict.get("revision_round", 0)),
        "generated_at": _now_iso(),
    }


def _pinned_brief_digest(paths: RunPaths, variant: str, verdict: dict) -> str | None:
    """발췌본 지문의 핀 — 현 판정문, 없으면 보존 판정문(`rounds/r<n>/verdict.json` · 높은 n 부터)."""
    pinned = verdict.get("final_eyes_brief_digest")
    if isinstance(pinned, str) and pinned:
        return pinned
    rounds = os.path.join(paths.gate_dir(variant), ROUNDS_DIRNAME)
    if not os.path.isdir(rounds):
        return None
    numbered = sorted((int(name[1:]) for name in os.listdir(rounds) if re.fullmatch(r"r[1-9][0-9]*", name)), reverse=True)
    for number in numbered:
        path = os.path.join(rounds, f"r{number}", "verdict.json")
        if os.path.isfile(path):
            try:
                previous = load_json(path).get("final_eyes_brief_digest")
            except (OSError, ValueError):
                previous = None
            if isinstance(previous, str) and previous:
                return previous
    return None


def ensure_final_eyes_brief(paths: RunPaths, variant: str, *, meta: dict, verdict: dict, k: int) -> str:
    """루프 개시 **전** 1회 생성 · 이후 바이트 불변. 반환 = 파일 지문(호출자가 verdict 에 핀한다). 다르면 `StageHaltError`."""
    path = paths.final_eyes_brief(variant)
    pinned = _pinned_brief_digest(paths, variant, verdict)
    if os.path.isfile(path):
        actual = sha256_file(path)
        if pinned is not None and pinned != actual:
            raise StageHaltError(
                f"[halt] final-eyes-brief.json 이 핀된 지문과 다르다 — 루프 산출물로 바뀐 발췌본은 격이 무효다(재정 N1): "
                f"핀 {pinned} ≠ 실측 {actual}"
            )
        return actual
    if pinned is not None:
        raise StageHaltError(f"[halt] final-eyes-brief.json 이 사라졌다(핀 {pinned}) — 루프 개시 전 동결물은 다시 만들지 않는다")
    if int(verdict.get("revision_round", 0)) != 0:
        raise StageHaltError("[halt] 발췌본이 없는데 수정 라운드가 이미 시작되었다 — 루프 개시 전에 생성되어야 한다(재정 N1)")
    thread = load_json(paths.thread_json(variant))
    brief = build_final_eyes_brief(meta=meta, verdict=verdict, thread=thread, k=k)
    # 생성 시각은 파일의 생성 완료 시각이다. 새 발췌본에 한해 그 시각으로 mtime을 결속한다.
    import datetime
    brief["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write_json(path, brief)
    stamp = datetime.datetime.fromisoformat(brief["generated_at"]).timestamp()
    os.utime(path, (stamp, stamp))
    return sha256_file(path)


def _no_rewrite_row(defects: list[dict]) -> CheckRow:
    row = CheckRow(check_id=CHECK_NO_REWRITE, checked=len(defects))
    for record in defects:
        for hit in no_rewrite_violations(record["fix_directive"]):
            row.add(CHECK_NO_REWRITE, record["id"], hit, "지시문(어디를·어느 재료로)",
                    "fix_directive 가 따옴표 속 EN 문장을 담았다 — 게이트가 필자가 되었다(D8)")
    return row


def _replace_rows(rows: list[dict], fresh: list[CheckRow]) -> list[dict]:
    """같은 check_id 의 기존 행을 새 행으로 바꾸고(없으면 덧붙이고) 순서를 유지한다."""
    fresh_by_id = {row.check_id: row.to_row_dict() for row in fresh}
    out = [fresh_by_id.pop(row["check_id"]) if row["check_id"] in fresh_by_id else row for row in rows]
    out.extend(fresh_by_id[cid] for cid in [r.check_id for r in fresh] if cid in fresh_by_id)
    return out


def _halt_rows(verdict: dict) -> list[str]:
    return [row["check_id"] for row in verdict.get("checks") or []
            if row["check_id"] in (CHECK_NO_REWRITE, CHECK_L1_LANE_VERIFIED, CHECK_NO_SCORE) and row["status"] == "fail"]


def _l1_summary(verdict: dict, **extra) -> dict:
    l1 = verdict["l1"]
    return {"l0_pass": bool(verdict["l0"]["pass"]), "l1_pass": l1["pass"], "decision": verdict["decision"],
            "defects": len(l1["defects"]), "flags": len(l1["flags"]), "disagreements": len(l1["disagreement_log"]),
            "revision_round": verdict["revision_round"], "thread_digest": verdict["thread_digest"],
            "final_eyes_brief_digest": verdict.get("final_eyes_brief_digest"), **extra}


def run_l1(*, run_root: str, repo: str | None = None, variant: str, adapter=None) -> dict:
    """L1 국소 대조 1회 진입(변주 1건). 반환 = `{status: ok|pending|skipped-l0|reentered|halt, ...}` — halt 는 기록 뒤 `StageHaltError`.

    전제 = `verdict.json` 실재(L0 먼저) · 그 `thread_digest` == 현 주석본. `l0.pass` 가 아니면 L1 요청을 만들지 않는다(총괄 재량 ⓐ).
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)
    _check_terminus(meta, repo, contract)
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError(f"verdict.json 이 없다 — gate-l0 가 먼저다: {verdict_path}")
    verdict = load_json(verdict_path)
    text = read_text(paths.thread_annotated(variant))
    digest = sha256_bytes(text.encode("utf-8"))
    if str(verdict.get("thread_digest")) != digest:
        raise StageError("verdict.json 의 thread_digest 가 현 주석본과 다르다 — gate-l0 를 다시 돌린다")
    frozen_row = latest_frozen(meta)
    spec_ok = str(verdict.get("spec_digest")) == str(frozen_row.get("spec_digest", ""))
    config = l1_plan.l1_config(repo, contract)
    cap = revision_cap(contract)
    round_no = int(verdict.get("revision_round", 0))

    # 발췌본 — 루프 개시 전 1회 · 불변(재정 N1). 핀은 판정문에.
    verdict["final_eyes_brief_digest"] = ensure_final_eyes_brief(paths, variant, meta=meta, verdict=verdict, k=config["k"])

    if not spec_ok or not verdict["l0"]["pass"]:
        # 재량 ⓐ — L0 결함이 있으면 L1 을 돌리지 않는다. 판정은 그대로(revise · 캡이면 escalate).
        verdict["decision"] = decide(l0_pass=bool(verdict["l0"]["pass"]), l1_pass=None, revision_round=round_no, cap=cap, spec_ok=spec_ok)
        write_json(verdict_path, verdict)
        return {"status": "skipped-l0" if spec_ok else "spec-mismatch", **_l1_summary(verdict), "paths": _paths_of(paths, variant)}

    if verdict["l1"].get("pass") is not None:
        write_json(verdict_path, verdict)
        halted = _halt_rows(verdict)
        if halted:
            raise StageHaltError(f"[halt] L1 검사 실패가 기록되어 있다({', '.join(halted)}) — 게이트 절차 문서 수정 후 재개(D8)")
        return {"status": "reentered", **_l1_summary(verdict, reentered=True), "paths": _paths_of(paths, variant)}

    index_text = read_text(paths.annotation_index_json(variant))
    requests = [l1_plan.build_request(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, variant=variant, thread_text=text,
                                      index_text=index_text, batch=i, config=config) for i in range(config["k"])]
    adapter = adapter or FileLaneAdapter(paths.gate_lanes_dir(variant), repo)
    write_json(verdict_path, verdict)              # 핀은 요청을 내기 전에 남긴다(루프 개시 전 동결물의 시점 증거)
    try:
        responses = adapter.dispatch(requests)
    except LanePending as pending:
        return {"status": "pending", "pending": list(pending.pending), "lanes_root": pending.request_dir,
                "k": config["k"], **_l1_summary(verdict), "paths": _paths_of(paths, variant)}

    l0 = verdict["l0"]
    merged = l1_merge.merge([r.payload for r in responses], k=config["k"], advisory_rules=config["advisory_rules"],
                            flag_rule=config["flag_rule"], next_defect_no=len(l0["defects"]) + 1, next_flag_no=len(l0["flags"]) + 1)

    clean = CheckRow(check_id=CHECK_L1_CLEAN, checked=1)
    if merged["defects"]:
        clean.add(CHECK_L1_CLEAN, "l1.json#defects", str(len(merged["defects"])), "0", "L1 결함이 남아 있다 — 국소 수정 지시로 돌아간다")
    rewrite = _no_rewrite_row([*l0["defects"], *merged["defects"]])
    verified = CheckRow(check_id=CHECK_L1_LANE_VERIFIED, checked=2 * len(responses))
    for request, response in zip(requests, responses):
        if response.model not in request.accepted_models:
            verified.add("lane.model", response.lane_id, response.model, f"{config['model']} 수용 집합 {list(request.accepted_models)}",
                         "L1 레인의 실호출 모델이 계약 좌석과 다르다 — 판정 자격이 없다(총괄 재량 ⓑ · R10 규율 4)")
        if response.effort != config["effort"]:
            verified.add("lane.effort", response.lane_id, response.effort, config["effort"], "L1 레인의 effort 가 계약 좌석과 다르다")

    verdict["l1"] = merged
    verdict["checks"] = _replace_rows(verdict["checks"], [rewrite, clean, verified])
    verdict["vacuous_pass"] = [row["check_id"] for row in verdict["checks"] if row["vacuous"] != "none"]
    verdict["inactive_layers"] = [row for row in verdict["inactive_layers"] if row.get("layer") not in L1_PENDING_LAYERS]
    verdict["decision"] = decide(l0_pass=True, l1_pass=bool(merged["pass"]), revision_round=round_no, cap=cap, spec_ok=spec_ok)
    write_json(paths.l1_json(variant), merged)
    write_json(verdict_path, verdict)
    halted = _halt_rows(verdict)
    if halted:
        raise StageHaltError(f"[halt] L1 검사 실패({', '.join(halted)}) — D8 위반 또는 좌석 불일치. 절차 문서·좌석 확인 후 재개")
    return {"status": "ok", **_l1_summary(verdict), "lanes": [{"lane_id": r.lane_id, "model": r.model, "effort": r.effort,
                                                                "response_digest": r.response_digest} for r in responses],
            "paths": _paths_of(paths, variant)}


def _paths_of(paths: RunPaths, variant: str) -> dict:
    return {
        "l0": paths.l0_json(variant), "verdict": paths.verdict_json(variant),
        "stripped": paths.thread_stripped_md(variant), "thread": paths.thread_json(variant),
        "index": paths.annotation_index_json(variant), "l1": paths.l1_json(variant),
        "final_eyes_brief": paths.final_eyes_brief(variant), "l2": paths.l2_md(variant),
    }


# ---------------------------------------------------------------------------
# L2 자문 메모 (재정 2026-09-13 T69 ⑥ · M4/M8-a · SPEC §1.10 판단 경로 · §4.6)
# ---------------------------------------------------------------------------


def number_memos(memos: list[dict]) -> list[dict]:
    """레인 payload `memos[]` → §4.2 memo 레코드(id `m-l2-NNN` 연번 · layer l2 · 전 속성 string 또는 locus)."""
    out: list[dict] = []
    for index, memo in enumerate(memos, start=1):
        locus = memo.get("locus") or {}
        out.append({"id": MEMO_ID_FORMAT.format(index), "layer": LAYER_L2, "rule": str(memo.get("rule", "")),
                    "locus": {"tweet": locus.get("tweet"), "sentence": locus.get("sentence")}, "text": str(memo.get("text", ""))})
    return out


def _cell(value) -> str:
    return str("" if value is None else value).replace("|", "\\|").replace("\n", " ")


def render_l2_md(*, verdict: dict, memos: list[dict], lane: dict, free_revision_used: bool = False) -> str:
    """`50-gate/<v>/l2.md` — KR 틀 · 값 그대로 · 점수 없음. verdict.json#l2.memos 와 같은 값의 렌더(정본은 verdict)."""
    lines = [
        f"# L2 자문 메모 — `{verdict.get('run_id')}` / `{verdict.get('variant')}`",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| thread_digest | `{verdict.get('thread_digest')}` |",
        f"| spec_version | `{verdict.get('spec_version')}` |",
        f"| decision (L2 는 바꾸지 않는다) | `{verdict.get('decision')}` |",
        f"| lane | `{lane.get('lane_id')}` · model `{lane.get('model')}` · effort `{lane.get('effort')}` |",
        f"| memos | {len(memos)} |",
        f"| free_revision_used | `{str(bool(free_revision_used)).lower()}` |",
        "",
        "거부권 없음 · 점수 없음(SPEC §4.6 · D8·D15) · 메모 1회 → 펜 자유 리비전 1회 → 위상 봉쇄.",
        "",
        "| id | rule | locus | text |",
        "|---|---|---|---|",
    ]
    for memo in memos:
        locus = memo.get("locus") or {}
        tweet, sentence = locus.get("tweet"), locus.get("sentence")
        where = "전역" if tweet is None else (f"T{tweet}" if sentence is None else f"T{tweet}/S{sentence}")
        lines.append(f"| `{memo['id']}` | `{_cell(memo['rule'])}` | {where} | {_cell(memo['text'])} |")
    if not memos:
        lines.append("| (없음) | | | |")
    return "\n".join(lines) + "\n"


def _l2_summary(verdict: dict, **extra) -> dict:
    return {"decision": verdict["decision"], "memos": len((verdict.get("l2") or {}).get("memos") or []),
            "free_revision_used": bool(verdict.get("free_revision_used", False)), "thread_digest": verdict["thread_digest"], **extra}


def _restore_preserved_l2(paths: RunPaths, variant: str, verdict: dict) -> bool:
    """L2 메모는 **1회 생성·불변**이다(D8 · `final-eyes-brief.json` 과 같은 격). 보존 자리에만 있으면
    제자리와 판정문으로 되돌린다.

    2026-09-14 수리 전에는 `_preserve_previous` 가 `l2.md` 를 라운드 자리로 **옮겼고**, 판정문도 회차마다
    새로 쓰여 L2 블록과 소진 표시가 함께 사라졌다. 그 시절에 돌던 런은 CP2 필수 표면을 잃고 `run_l2` 에는
    첫 실행으로 보인다 — 결함 수정이 판단 경로를 다시 여는 것은 위상 위반이므로, 새로 만들지 않고 되돌린다.
    """
    if os.path.isfile(paths.l2_md(variant)):
        return False
    rounds_dir = os.path.join(paths.gate_dir(variant), ROUNDS_DIRNAME)
    if not os.path.isdir(rounds_dir):
        return False
    for name in sorted(os.listdir(rounds_dir), key=_round_sort_key, reverse=True):
        memo = os.path.join(rounds_dir, name, "l2.md")
        if not os.path.isfile(memo):
            continue
        write_text(paths.l2_md(variant), read_text(memo))
        kept = os.path.join(rounds_dir, name, "verdict.json")
        if os.path.isfile(kept):
            previous = load_json(kept)
            if (previous.get("l2") or {}).get("memos"):
                verdict["l2"] = previous["l2"]
            if previous.get("free_revision_used") is not None:
                verdict["free_revision_used"] = previous["free_revision_used"]
        if verdict.get("free_revision_used") is None and os.path.isdir(paths.free_revision_dir(variant)):
            verdict["free_revision_used"] = True   # 소진 사실의 정본은 디스크다
        verdict["inactive_layers"] = [row for row in verdict.get("inactive_layers", []) if row.get("layer") != LAYER_L2]
        return True
    return False


def _round_sort_key(name: str):
    digits = "".join(ch for ch in name if ch.isdigit())
    return (int(digits) if digits else 0, name)


def run_l2(*, run_root: str, repo: str | None = None, variant: str, adapter=None) -> dict:
    """L2 자문 메모 1회 진입(변주 1건). 반환 = `{status: ok|pending|reentered, memos, decision, ...}` — 린트 실패는 기록 뒤 `StageHaltError`.

    전제 = `verdict.json#decision == advance`(L0·L1 pass) · 그 `thread_digest` == 현 주석본. L2 는 판정을 바꾸지 않는다(거부권 없음).
    위상 봉쇄(D8) — `free_revision_used` 가 true 인 판정문에서는 다시 돌지 않는다(`StageHaltError`). 메모가 이미 기록된 판정문
    (`l2.md` 실재)은 재진입이다.
    """
    repo = repo or repo_root()
    paths = RunPaths(run_root, repo)
    contract = paths.contracts[STAGE_ID]
    meta = load_yaml(paths.run_yaml)
    _check_terminus(meta, repo, contract)
    verdict_path = paths.verdict_json(variant)
    if not os.path.isfile(verdict_path):
        raise StageError(f"verdict.json 이 없다 — gate-l0 · gate-l1 이 먼저다: {verdict_path}")
    verdict = load_json(verdict_path)
    text = read_text(paths.thread_annotated(variant))
    if str(verdict.get("thread_digest")) != sha256_bytes(text.encode("utf-8")):
        raise StageError("verdict.json 의 thread_digest 가 현 주석본과 다르다 — gate-l0 · gate-l1 을 다시 돌린다")
    restored = _restore_preserved_l2(paths, variant, verdict)
    if restored:
        write_json(verdict_path, verdict)
    if verdict.get("free_revision_used") is True:
        # 복원은 위 `_restore_preserved_l2` 가 디스크에 이미 마쳤다 — 봉쇄는 그대로 건다.
        raise StageHaltError("[halt] 위상 봉쇄 · D8 — L2 메모 1회 → 펜 자유 리비전 1회가 이미 소비되었다. 리비전 결과에 L2 를 다시 돌리지 않는다(SPEC §4.6)")
    if verdict.get("decision") != DECISION_ADVANCE:
        raise StageError(f"decision 이 advance 가 아니다({verdict.get('decision')}) — L2 는 L0·L1 을 통과한 판정문에만 돈다")
    config = l2_plan.l2_config(repo, contract)
    law = l2_lint.load_patterns(repo)
    l2_path = paths.l2_md(variant)
    if os.path.isfile(l2_path):
        halted = _halt_rows(verdict)
        if halted:
            raise StageHaltError(f"[halt] L2 검사 실패가 기록되어 있다({', '.join(halted)}) — 절차 문서 수정 후 재개(D8·D15)")
        return {"status": "reentered", **_l2_summary(verdict, reentered=True), "paths": _paths_of(paths, variant)}

    frozen_row = latest_frozen(meta)
    request = l2_plan.build_request(paths=paths, repo=repo, meta=meta, frozen_row=frozen_row, variant=variant, thread_text=text, config=config)
    adapter = adapter or FileLaneAdapter(paths.gate_lanes_dir(variant), repo)
    try:
        response = adapter.dispatch([request])[0]
    except LanePending as pending:
        return {"status": "pending", "pending": list(pending.pending), "lanes_root": pending.request_dir,
                **_l2_summary(verdict), "paths": _paths_of(paths, variant)}

    memos = number_memos(list(response.payload.get("memos") or []))
    row = l2_lint.lint_memos(memos, law)
    lane = {"lane_id": response.lane_id, "model": response.model, "effort": response.effort,
            "response_digest": response.response_digest, "mismatch": response.mismatches(request)}
    row.extras["lane"] = lane
    legislated_now = legislated(repo)
    if legislated_now.get("score_lint_version") != str(law["version"]) or legislated_now.get("score_lint_patterns") != len(law["patterns"]):
        raise StageError("score-lint 날인(legislated)이 로드한 패턴 파일과 다르다 — 두 벌이 갈렸다")
    verdict["l2"] = {"memos": memos}
    verdict["checks"] = _replace_rows(verdict["checks"], [row])
    verdict["vacuous_pass"] = [r["check_id"] for r in verdict["checks"] if r["vacuous"] != "none"]
    verdict["inactive_layers"] = [r for r in verdict["inactive_layers"] if r.get("layer") not in L2_PENDING_LAYERS]
    verdict["legislated"] = legislated_now
    write_json(verdict_path, verdict)
    write_text(l2_path, render_l2_md(verdict=verdict, memos=memos, lane=lane))
    if row.status == "fail":
        entry = failure_entry(contract, "gate.no-score 실패")
        first = row.findings[0]
        raise StageHaltError(f"[{entry.get('action')}] gate.no-score 실패 — {first.rule}@{first.locus}: {first.found!r}. {entry.get('note')}")
    return {"status": "ok", **_l2_summary(verdict), "lane": lane, "paths": _paths_of(paths, variant)}


__all__ = ["GATE_VERSION", "URL_RE", "build_final_eyes_brief", "decide", "ensure_final_eyes_brief", "inactive_layers",
           "judge_variant", "legislated", "no_rewrite_violations", "number_memos", "render_l2_md", "revision_cap", "run", "run_l1",
           "run_l2"]


def run_final_eyes(*, run_root, repo=None, variant, adapter=None):
    from ..gate.final_eyes import run
    return run(run_root, repo, variant, adapter)
