# -*- coding: utf-8 -*-
"""역방향 재조립 — `thread.json` + `annotation-index.json` → 주석본 바이트(SPEC §3.3 역방향 round-trip).

원본 `thread.annotated.md` 와 **바이트 동일**해야 한다. 그 조건이 성립하는 자리들.

· 프런트매터 = `---\\n` + `frontmatter_raw`(원문 바이트 그대로 · 끝 개행 포함) + `---\\n`.
· 헤더 = `## T<n> {slot: <slot>, fig: <figspec>}` — `figspec` 은 `figures[]` 를 `+` 로 잇고 비면 `none`.
· 문장 = `text_raw`(이스케이프 복원 전 원문 · 없으면 `text` 에 `[`→`\\[` 재적용 불가이므로 그대로) + 태그.
· 태그 = `[narrative]` 또는 `[M<n>(,M<n>)*]` — 태그 앞 공백 0(§3.2 · 그래서 이 재조립이 성립한다).
· 프런트매터 뒤 빈 줄 1 · 트윗 사이 빈 줄 1 · 끝 개행 1(strip ⑤와 compose 의 끝 개행 정규화의 역).

역방향까지 요구하는 이유(§3.3): 순방향만 보면 「태그를 통째로 버리는」 구현도 통과한다.
"""

from __future__ import annotations


def _figspec(figures: list) -> str:
    return "+".join(str(f) for f in figures) if figures else "none"


def _tag(sentence: dict) -> str:
    if sentence.get("narrative"):
        return "[narrative]"
    return "[" + ",".join(str(c) for c in sentence.get("citations") or []) + "]"


def reassemble(thread: dict, index: dict) -> str:
    """두 산출에서 주석본 전문을 재생성한다(결정론 · 판단 없음)."""
    thread_tweets = list(thread.get("tweets") or [])
    index_tweets = list(index.get("tweets") or [])
    if len(thread_tweets) != len(index_tweets):
        raise ValueError(f"thread.json 트윗 {len(thread_tweets)} ≠ annotation-index 트윗 {len(index_tweets)}")
    blocks: list[str] = []
    for t_thread, t_index in zip(thread_tweets, index_tweets):
        if int(t_thread["n"]) != int(t_index["n"]):
            raise ValueError(f"트윗 번호 불일치: {t_thread['n']} ≠ {t_index['n']}")
        lines = [f"## T{t_thread['n']} {{slot: {t_thread['slot']}, fig: {_figspec(t_thread.get('figures') or [])}}}"]
        for sentence in t_index.get("sentences") or []:
            text = sentence["text_raw"] if "text_raw" in sentence else sentence["text"]
            lines.append(text + _tag(sentence))
        blocks.append("\n".join(lines))
    return "---\n" + str(thread["frontmatter_raw"]) + "---\n\n" + "\n\n".join(blocks) + "\n"


__all__ = ["reassemble"]
