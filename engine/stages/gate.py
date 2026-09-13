# -*- coding: utf-8 -*-
"""`gate` 스테이지 — L0 결정론 층 + strip + round-trip(재정 2026-09-13 T64 ② · M3).

계약 = `contracts/stages/gate.yaml`(정본 서술 = SPEC §1.10). 이 러너는 변주별 주석본에 대해

① 진입 — 종료선(`partial_until`) · `gate.input-digest`(동결본 · 블루프린트 · 주석본 실재 — 재정 P-C) ·
   대상 변주 = `40-compose/<v>/thread.annotated.md` 가 있는 변주(반려서만 있는 변주는 건너뛴다).
② 변주마다 — `parse(text)` → 오류가 있으면 `annotation.schema`·`annotation.missing-tag` 행만 내고 **나머지
   L0 는 평가하지 않는다**(SPEC §3.2 연쇄 오보 방지 · 행을 내지 않는다) → 오류 0 이면 strip(§3.3 ①~⑤) → L0 규칙
   전량(`contracts/l0-format.yaml#rules[]` 로드 · 출하본 기준) → round-trip 3방향(§3.3) → `l0.json` · `verdict.json`
   (`gate-report/v0`) · `thread.stripped.md` · `thread.json` · `annotation-index.json`.
③ 처분 — 러너는 판정을 **기록**하며 루프를 돌리지 않는다(국소 수정 루프 = M6 미가동). `decision` 은 가동 층만으로
   정한다(총괄 재량 ⓑ · 미가동 층은 `inactive_layers[]` 에 적는다). 어느 변주에 결함이 있어도 러너 status 는 `ok`
   (기록 완료). 산출이 이미 있으면 `thread_digest` 가 같을 때 재계산 없이 `ok`, 다르면 **직전 산출을
   `50-gate/<v>/rounds/r<n>/` 로 옮긴 뒤** 다시 판정한다(재정 T65 ③ · 총괄 재량 ⓔ — 「덮어씀」을 보존으로 · 사료 규율).
④ `format.stop-shape` 는 매니페스트(`30-figures/assets/manifest.json`)가 실재하면 가동이다(재정 T65 ③). 없는 런에서는
   러너가 `inactive_layers[]` 에 그 사실을 동적으로 더한다 — 판정하지 않은 층을 판정한 것처럼 적지 않는다(재정 N5).

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
from ..annotation.parse import parse as parse_annotation
from ..annotation.reassemble import reassemble
from ..annotation.strip import RESIDUAL_TAG_RE, _reference_strip, strip
from ..figures import asset_paths as manifest_asset_paths
from ..gate.l0.rules_format import MANIFEST_ABSENT_REASON, R_STOP_SHAPE
from ..gate.l0 import L0Context, L0Law, Rule, load_rules_from_law, stamp_ruleset
from ..gate.l0.weighted_length import EMOJI_APPROXIMATION_NOTE, weighted_length
from ..paths import ROUNDS_DIRNAME, RunPaths, load_format_parameters, load_stage_contract, repo_root
from ..pens import registry

STAGE_ID = "gate"
GATE_VERSION = "0.1.0"
LAYER_L0 = "l0"

#: URL 최소 어형(총괄 재량 ⓒ) — 시트에 URL 문법이 없다. `https?://…` 와 `www.…` 의 비공백 연속.
URL_RE = re.compile(r"https?://\S+|www\.\S+")
#: `gate.no-rewrite` — 따옴표로 감싼 5토큰 이상의 EN 문장(SPEC §4.7 기제 3 · 탐지 범위의 한계도 그 절에).
_QUOTED_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
_EN_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
NO_REWRITE_TOKENS = 5

CHECK_ENTRY = "gate.input-digest"
CHECK_L0_CLEAN = "gate.l0-clean"
CHECK_INDEX = "gate.annotation-index"
CHECK_NO_REWRITE = "gate.no-rewrite"
CHECK_FORWARD = "strip.roundtrip-forward"
CHECK_REVERSE = "strip.roundtrip-reverse"
CHECK_REASSEMBLY = "strip.reassembly"
CHECK_RESIDUAL = "strip.residual-tag"

DECISION_ADVANCE = "advance"
DECISION_REVISE = "revise"
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


def inactive_layers(contract: dict) -> tuple[dict, list[dict]]:
    """계약 `layers` 블록 → (블록 사본, `inactive_layers[]` 배열). 목록을 코드가 들지 않는다."""
    block = {key: value for key, value in (contract.get("layers") or {}).items() if isinstance(value, dict)}
    rows: list[dict] = []
    for layer, entry in block.items():
        if str(entry.get("status", "")) == "inactive":
            rows.append({"layer": layer, "reason": str(entry.get("reason", "")), "ruling": str(entry.get("ruling", ""))})
    return block, rows


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
    """직전 판정 산출(파일들)을 `50-gate/<v>/rounds/r<n>/` 로 옮긴다. 옮긴 자리를 돌려준다(없으면 None)."""
    gate_dir = paths.gate_dir(variant)
    if not os.path.isdir(gate_dir):
        return None
    files = [name for name in os.listdir(gate_dir) if os.path.isfile(os.path.join(gate_dir, name))]
    if not files:
        return None
    target = paths.gate_round_dir(variant, _round_number(gate_dir))
    if os.path.exists(target):
        raise StageError(f"보존 자리가 이미 있다 — 덮어쓰지 않는다: {target}")
    os.makedirs(target)
    for name in files:
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
    layers_block, inactive = inactive_layers(contract)
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
        "decision": DECISION_ADVANCE if l0_pass else DECISION_REVISE,
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
        if not strip_only and previous == digest:
            verdict = load_json(paths.verdict_json(variant))
            variants_out[variant] = {**_summary(verdict), "reentered": True, "paths": _paths_of(paths, variant)}
            rows_out[variant] = [entry_row]
            continue
        preserved = None
        if not strip_only and previous is not None and previous != digest:
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


def _paths_of(paths: RunPaths, variant: str) -> dict:
    return {
        "l0": paths.l0_json(variant), "verdict": paths.verdict_json(variant),
        "stripped": paths.thread_stripped_md(variant), "thread": paths.thread_json(variant),
        "index": paths.annotation_index_json(variant),
    }


__all__ = ["GATE_VERSION", "URL_RE", "inactive_layers", "judge_variant", "legislated", "no_rewrite_violations", "run"]
