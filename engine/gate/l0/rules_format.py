# -*- coding: utf-8 -*-
"""`format.*` 7종 — 스레드 규격 집행(D11 · 재정 R5·R6·N3). 문언 = `l0-format.yaml#rules[]` · 값 = 시트.

규칙마다 행 하나(`CheckRow`)와 결함 목록을 낸다. `checked` = 그 규칙이 실제로 본 대상 수(트윗 수 등).
지시문(`fix_directive`)은 「어디를 · 어느 재료로」 형식이며 대체 문장을 담지 않는다(D8 · SPEC §4.7).

`format.stop-shape` 는 재정 T65 ③(도면 자산층 실물화)으로 **가동**이다 — 매니페스트(`30-figures/assets/manifest.json`)
가 실재하면 헤더 `fig` 의 자산 id 를 매니페스트 항목(`asset_id` · 골든 표기 `figure` · 없으면 `asset_path` basename —
`engine/figures/asset_id_of`)으로 해소해 `edit_class` 를 센다. 매니페스트가 없는 런(T64 ④ 시절의 판)에서는 행을
`checked 0` 으로 내고 `extras.inactive_reason` 에 사유를 적는다 — 러너가 그 사실을 `inactive_layers[]` 에도 옮긴다.
"""

from __future__ import annotations

from reader.lib.report import CheckRow

from ...figures import asset_classes
from ...stages import StageError
from ..sentence_count import count_sentences
from .context import L0Context, RuleResult
from .weighted_length import weighted_length

R_TWEET_COUNT = "format.tweet-count"
R_SLOT_COUNT = "format.slot-count"
R_BODY_LENGTH = "format.body-length"
R_STOP_SHAPE = "format.stop-shape"
R_HASHTAG = "format.hashtag-zero"
R_NO_LINK = "format.no-link-in-body"
R_IMAGES = "format.images-per-post"
#: 매니페스트가 없는 런의 미가동 사유(계약 `gate.yaml#layers` 에 행이 없을 때의 기본 문언).
MANIFEST_ABSENT_REASON = "30-figures/assets/manifest.json 부재 — figures.prepare 가 돌지 않은 런"


def _tweets(ctx: L0Context):
    """구조 규칙은 파서 산출을, 본문 규칙은 strip 산출을 본다 — 둘의 트윗 순서는 같다."""
    return ctx.parsed.tweets


def tweet_count(ctx: L0Context) -> RuleResult:
    bounds = ctx.law.param_of(R_TWEET_COUNT, "tweet_count")
    n = len(_tweets(ctx))
    res = RuleResult(CheckRow(check_id=R_TWEET_COUNT, checked=n))
    low, high = int(bounds["min"]), int(bounds["max"])
    if n < low or n > high:
        res.defect(R_TWEET_COUNT, None, None, f"sheet tweet_count range {low}~{high}", str(n),
                   "트윗 수를 시트 tweet_count 범위 안으로 맞추라 — 블루프린트 슬롯 수를 따르고, 상한 초과는 Owner 결정(overflow_proposal)이다.")
    return res


def slot_count(ctx: L0Context) -> RuleResult:
    placement = ctx.law.param_of(R_SLOT_COUNT, "slot_placement")
    enum = list(ctx.law.param_of(R_SLOT_COUNT, "slot_enum"))
    tweets = _tweets(ctx)
    slots = [tweet.slot for tweet in tweets]
    n = len(slots)
    res = RuleResult(CheckRow(check_id=R_SLOT_COUNT, checked=n))
    if n == 0:
        return res
    named = [name for name in placement if name != "other"]
    other_allowed = list((placement.get("other") or {}).get("allowed") or [])
    designated: set[int] = set()
    for name in named:
        spec = placement[name] or {}
        count = spec.get("count") or {}
        low, high = int(count.get("min", 0)), int(count.get("max", n))
        positions = [i for i, slot in enumerate(slots) if slot == name]
        position_rule = str(spec.get("position", "any"))
        ok_count = low <= len(positions) <= high
        ok_position = True
        if positions and position_rule == "first":
            ok_position = positions == [0]
        elif positions and position_rule == "last":
            ok_position = positions == [n - 1]
        if not (ok_count and ok_position):
            where = ", ".join(f"T{i + 1}" for i in positions) or "(없음)"
            res.defect(R_SLOT_COUNT, None, None,
                       f"{name}: count {low}~{high}" + (f" at {position_rule}" if position_rule != "any" else ""),
                       f"{name} ×{len(positions)} @ {where}",
                       f"슬롯 배치를 시트 slot_placement 대로 고치라 — {name} 은 {low}~{high}개" +
                       (f"이며 위치는 {position_rule} 다" if position_rule != "any" else "다") + ". 라벨로 길이 하한을 우회하지 마라(재정 R6).")
        if ok_count and ok_position:
            designated.update(positions)
    for i, slot in enumerate(slots):
        if i in designated:
            continue
        if slot in named and slot not in other_allowed:
            # 지정 자리 밖의 hook·landing·tail 은 위 개수·위치 결함이 이미 집계했다(한 위반을 두 행에 싣지 않는다).
            continue
        if slot not in other_allowed:
            res.defect(R_SLOT_COUNT, i + 1, None, f"slot in {other_allowed} (sheet slot_placement.other.allowed; enum {enum})", slot,
                       f"T{i + 1} 의 슬롯을 시트 slot_placement.other.allowed 의 값으로 고치라.")
    return res


def body_length(ctx: L0Context) -> RuleResult:
    by_slot = dict(ctx.law.param_of(R_BODY_LENGTH, "length_by_slot").get("by_slot") or {})
    config = ctx.law.param_of(R_BODY_LENGTH, "weighted_length")
    if ctx.stripped is None:
        raise StageError("format.body-length 는 strip 산출 위에서만 돈다")
    res = RuleResult(CheckRow(check_id=R_BODY_LENGTH, checked=0))
    counts: list[int] = []
    for tweet in ctx.stripped.tweets:
        weighted = weighted_length(tweet.text, config, ctx.url_re)
        counts.append(weighted)
        rule = by_slot.get(tweet.slot)
        if not isinstance(rule, dict) or rule.get("exempt"):
            continue
        res.row.checked += 1
        low, high = rule.get("min"), rule.get("max")
        if low is not None and weighted < int(low):
            res.defect(R_BODY_LENGTH, tweet.n, None, f"sheet length_by_slot range for {tweet.slot} (min {low})", str(weighted),
                       f"T{tweet.n} 을 시트 하한까지 채우라 — 블루프린트가 지정한 전시 재료(M id)로 문장을 더하라.")
        if high is not None and weighted > int(high):
            res.defect(R_BODY_LENGTH, tweet.n, None, f"sheet length_by_slot range for {tweet.slot} (max {high})", str(weighted),
                       f"T{tweet.n} 을 시트 상한 아래로 줄이라 — 인용 재료를 유지한 채 문장을 덜어내라.")
    res.row.extras["weighted_char_counts"] = counts
    return res


def stop_shape(ctx: L0Context) -> RuleResult:
    applies_to = list(ctx.law.param_of(R_STOP_SHAPE, "stop_shape.applies_to"))
    assets_min = int(ctx.law.param_of(R_STOP_SHAPE, "stop_shape.edited_assets_min"))
    sentences_max = int(ctx.law.param_of(R_STOP_SHAPE, "stop_shape.sentences_max"))
    edited = (ctx.law.block("stop_shape").get("edited_asset") or {})
    counted = set(edited.get("counted_edit_classes") or [])
    res = RuleResult(CheckRow(check_id=R_STOP_SHAPE, checked=0))
    if ctx.manifest is None:
        layer = ctx.inactive.get(R_STOP_SHAPE) or {}
        res.row.extras["inactive_reason"] = str(layer.get("reason") or MANIFEST_ABSENT_REASON)
        res.row.extras["inactive_ruling"] = str(layer.get("ruling") or "")
        return res
    # 헤더 fig 항목(fig-NN) ↔ 매니페스트 자산 id. 매니페스트의 figure_id(FIG-n)로는 해소하지 않는다 — 헤더는 자산 id 를 든다(§3.2).
    classes = asset_classes(ctx.manifest)
    if ctx.stripped is None:
        raise StageError("format.stop-shape 는 strip 산출 위에서만 돈다")
    counting = ctx.law.block("sentence_counting")
    for tweet in ctx.stripped.tweets:
        if tweet.slot not in applies_to:
            continue
        res.row.checked += 1
        assets = sum(1 for figure in tweet.figures if classes.get(figure) in counted)
        sentences = count_sentences(tweet.text, counting)
        if assets < assets_min or sentences > sentences_max:
            res.defect(R_STOP_SHAPE, tweet.n, None, f">={assets_min} edited asset and <={sentences_max} sentences",
                       f"assets={assets} sentences={sentences}",
                       f"T{tweet.n} 을 전시 스톱 형태로 고치라 — 헤더 fig 에 편집 자산(crop-only 또는 self-authored)을 {assets_min}개 이상 두고 문장 수를 {sentences_max} 이하로 줄이라.")
    return res


def _slot_exempt_from_links(ctx: L0Context) -> str:
    """시트 `link_isolation` 문언에서 허용 슬롯을 읽는다 — 슬롯명 리터럴을 두지 않는다."""
    value = str(ctx.law.param_of(R_NO_LINK, "link_isolation"))
    hits = [slot for slot in ctx.slot_enum if slot in value]
    if len(hits) != 1:
        raise StageError(f"link_isolation 문언에서 허용 슬롯을 하나로 정하지 못했다: {value!r} → {hits}")
    return hits[0]


def hashtag_zero(ctx: L0Context) -> RuleResult:
    limit = int(ctx.law.param_of(R_HASHTAG, "hashtags_max"))
    if ctx.stripped is None:
        raise StageError("format.hashtag-zero 는 출하본 위에서만 돈다")
    res = RuleResult(CheckRow(check_id=R_HASHTAG, checked=len(ctx.stripped.tweets)))
    for tweet in ctx.stripped.tweets:
        text = ctx.url_re.sub(" ", tweet.text) if ctx.url_re is not None else tweet.text   # URL 안의 # 은 토큰이 아니다
        tags = [token for token in text.split() if token.startswith("#") and len(token) > 1 and token[1].isalpha()]
        if len(tags) > limit:
            res.defect(R_HASHTAG, tweet.n, None, str(limit), str(len(tags)),
                       f"T{tweet.n} 의 해시태그를 제거하라 — 시트 hashtags_max 는 {limit} 이다.")
    return res


def no_link_in_body(ctx: L0Context) -> RuleResult:
    exempt = _slot_exempt_from_links(ctx)
    if ctx.stripped is None or ctx.url_re is None:
        raise StageError("format.no-link-in-body 는 출하본과 URL 어형 위에서만 돈다")
    res = RuleResult(CheckRow(check_id=R_NO_LINK, checked=0))
    for tweet in ctx.stripped.tweets:
        if tweet.slot == exempt:
            continue
        res.row.checked += 1
        links = ctx.url_re.findall(tweet.text)
        if links:
            res.defect(R_NO_LINK, tweet.n, None, "0", str(len(links)),
                       f"T{tweet.n} 의 URL 을 {exempt} 슬롯으로 옮기라 — 본문 링크는 격리한다(시트 link_isolation).")
    return res


def images_per_post(ctx: L0Context) -> RuleResult:
    limit = int(ctx.law.param_of(R_IMAGES, "images_per_post_max"))
    tweets = _tweets(ctx)
    res = RuleResult(CheckRow(check_id=R_IMAGES, checked=len(tweets)))
    for tweet in tweets:
        if len(tweet.figures) > limit:
            res.defect(R_IMAGES, tweet.n, None, f"<=sheet images_per_post_max ({limit})", str(len(tweet.figures)),
                       f"T{tweet.n} 헤더 fig 항목을 {limit}개 이하로 줄이라.")
    return res


__all__ = ["body_length", "hashtag_zero", "images_per_post", "no_link_in_body", "slot_count", "stop_shape", "tweet_count"]
