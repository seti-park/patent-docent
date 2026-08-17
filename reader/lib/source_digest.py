# -*- coding: utf-8 -*-
"""`read.source-digest` — 불변식 I1 의 집행자.

SPEC §2.2 불변식 I1: **`sha256(source_path 파일) == source_digest`** 이며, 어긋나면
"결정론 검사 6종 전부 무효. READ 즉시 중단"이다. 즉 이것은 다른 검사와 나란한 검사가
아니라 **다른 검사들의 전제**다 — 인용이 어느 원천의 부분문자열인지가 여기서 정해진다.

집행자가 이식 단위에 있는 이유: 판정에 필요한 것이 `ctx` 의 입력(원천 문자열 + 명세의
`patent.source_digest`)뿐인 **순수 함수**이기 때문이다. 엔진 쪽 `read` 스테이지는
`run.yaml` 기록과 대조하지만 그것은 런의 사실이고, 여기서 보는 것은 **명세 자신이 신고한
기준점**이다. historian 이 재료 명세와 원천을 함께 받아 검증할 때도 같은 판정이 필요하다.
"""

from __future__ import annotations

import hashlib

from .report import CheckContext, CheckRow

CHECK_ID = "read.source-digest"
DIGEST_PREFIX = "sha256:"


def digest_of(source_text: str) -> str:
    """원천 문자열의 다이제스트를 명세 서식(`sha256:<64hex>`)으로 만든다."""
    return DIGEST_PREFIX + hashlib.sha256(source_text.encode("utf-8")).hexdigest()


def check(ctx: CheckContext) -> CheckRow:
    row = CheckRow(check_id=CHECK_ID)
    declared = ((ctx.spec.get("patent") or {}).get("source_digest")) or ""

    if not ctx.source_text:
        # 원천 없이 돌린 호출 — 대조할 대상이 없다. 행의 `vacuous: "empty-target"` 이
        # 그 사실을 날인한다(원천 없는 검사가 통과로 보이면 그 아래 전부가 거짓이 된다).
        row.extras["skipped"] = True
        row.extras["declared"] = declared
        return row

    row.checked = 1
    actual = digest_of(ctx.source_text)
    row.extras["declared"] = declared
    row.extras["actual"] = actual
    if actual != declared:
        row.add(
            "source.digest-match",
            "patent.source_digest",
            declared or "(없음)",
            actual,
            "명세가 신고한 원천 다이제스트가 실제 원천과 다르다 — 불변식 I1 위반이므로 "
            "이 인스턴스의 인용 검사 전부가 무효다(READ 중단 대상)",
        )
    return row
