# -*- coding: utf-8 -*-
"""주석 인덱스(`annotation-index/v0`) · 구조화 출하 객체(`thread/v0`) · 파서 산출 직렬화(`annotation/v0`).

세 객체는 같은 두 입력(`Parsed` · `Stripped`)에서 결정론으로 나온다. 좌표계 `{tweet, sentence}` 는 게이트
레코드(SPEC §4.2)와 같다 — 게이트·계기·수정 지시가 같은 좌표를 쓴다는 것이 국소화(D9)의 전제다.

`text_raw`(총괄 재량 ⓕ)는 이스케이프 복원 **전** 문장이다. 역방향 round-trip(`engine/annotation/reassemble.py`)이
`\\[` 를 원래 자리에만 되돌리려면 이것이 있어야 한다.
"""

from __future__ import annotations

from typing import Callable

from .parse import Parsed
from .strip import Stripped

ANNOTATION_INDEX_SCHEMA = "annotation-index/v0"
THREAD_SCHEMA = "thread/v0"
ANNOTATION_SCHEMA = "annotation/v0"


class IndexError_(ValueError):
    """파서 산출과 strip 산출의 문장 수가 어긋난다 — 같은 입력에서 나왔다면 있을 수 없는 일이다."""


def _check_alignment(parsed: Parsed, stripped: Stripped) -> None:
    if len(parsed.tweets) != len(stripped.tweets):
        raise IndexError_(f"트윗 수 불일치: parse {len(parsed.tweets)} ≠ strip {len(stripped.tweets)}")
    for tweet, stripped_tweet in zip(parsed.tweets, stripped.tweets):
        if tweet.n != stripped_tweet.n or len(tweet.sentences) != len(stripped_tweet.sentences):
            raise IndexError_(f"T{tweet.n} 문장 수 불일치: parse {len(tweet.sentences)} ≠ strip {len(stripped_tweet.sentences)}")


def build_index(parsed: Parsed, stripped: Stripped, *, run_id: str, variant: str, spec_version: int) -> dict:
    """`annotation-index/v0` — 모든 문장(`[narrative]` 포함) + `by_material` 역인덱스 + `narrative_sentences`."""
    _check_alignment(parsed, stripped)
    tweets_out: list[dict] = []
    by_material: dict[str, list[dict]] = {}
    narrative: list[dict] = []
    for tweet, stripped_tweet in zip(parsed.tweets, stripped.tweets):
        sentences_out: list[dict] = []
        for sentence, text, text_raw in zip(tweet.sentences, stripped_tweet.sentences, stripped_tweet.sentences_raw):
            locus = {"tweet": tweet.n, "sentence": sentence.i}
            sentences_out.append({
                "i": sentence.i, "text": text, "text_raw": text_raw,
                "citations": list(sentence.citations), "narrative": bool(sentence.narrative),
            })
            for material in sentence.citations:
                by_material.setdefault(material, []).append(dict(locus))
            if sentence.narrative:
                narrative.append(dict(locus))
        tweets_out.append({"n": tweet.n, "slot": tweet.slot, "sentences": sentences_out})
    return {
        "schema": ANNOTATION_INDEX_SCHEMA, "run_id": run_id, "variant": variant, "spec_version": int(spec_version),
        "tweets": tweets_out, "by_material": by_material, "narrative_sentences": narrative,
    }


def build_thread(stripped: Stripped, *, run_id: str, variant: str, spec_version: int, spec_digest: str,
                 weighted: Callable[[str], int], asset_paths: dict[str, str] | None = None) -> dict:
    """`thread/v0` — 구조화 출하 객체. `weighted` = 시트 가중 글자 수 함수(값은 러너가 시트에서 묶어 넘긴다)."""
    assets = asset_paths or {}
    tweets_out: list[dict] = []
    images: list[dict] = []
    for tweet in stripped.tweets:
        tweets_out.append({
            "n": tweet.n, "slot": tweet.slot, "figures": list(tweet.figures),
            "text": tweet.text, "weighted_char_count": int(weighted(tweet.text)),
        })
        for figure in tweet.figures:
            images.append({"figure": figure, "asset_path": assets.get(figure), "tweet": tweet.n})
    return {
        "schema": THREAD_SCHEMA, "run_id": run_id, "variant": variant, "spec_version": int(spec_version),
        "spec_digest": spec_digest, "frontmatter_raw": stripped.frontmatter_raw,
        "frontmatter": dict(stripped.frontmatter), "tweets": tweets_out, "images": images,
    }


def annotation_dict(parsed: Parsed) -> dict:
    """`annotation/v0` — 파서 산출의 직렬화(프런트매터 5키 + tweets[] · 문장 `text` 는 파서의 태그 제거 텍스트)."""
    return {
        "schema": ANNOTATION_SCHEMA,
        "frontmatter": dict(parsed.frontmatter),
        "tweets": [
            {
                "n": tweet.n, "slot": tweet.slot, "figspec": tweet.figspec, "figures": list(tweet.figures),
                "sentences": [
                    {"i": s.i, "text": s.text, "citations": list(s.citations), "narrative": bool(s.narrative)}
                    for s in tweet.sentences
                ],
            }
            for tweet in parsed.tweets
        ],
    }


__all__ = ["ANNOTATION_INDEX_SCHEMA", "ANNOTATION_SCHEMA", "THREAD_SCHEMA", "IndexError_", "annotation_dict",
           "build_index", "build_thread"]
