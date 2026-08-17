# -*- coding: utf-8 -*-
"""`read.convergence` — 독립 2회 READ 비교(SPEC §2.6 검사 4 · reader-rules#convergence).

의미는 품질이 아니라 **안정성**이다. 두 독립 실행이 다른 청구항 트리를 낳으면 그 소재에
대한 독해는 재현되지 않는 것이고, 이후 모든 결정론 검사의 기준점이 흔들린다(SPEC §1.4).

구 검사는 **독립항 수와 element `text_verbatim` 집합**만 봤다. 집합 비교이므로 같은 문자열
집합이 서로 다른 계층으로 조립되어도, 종속항이 통째로 흔들려도 수렴한 것으로 판정됐다
(재감수 M-07). 6축 전부를 본다.

전 축이 **id 가 아니라 원문 문언**으로 비교한다 — 두 독립 실행이 같은 id 를 쓸 이유가 없고,
id 로 비교하면 번호 매기기 관습이 같다는 사실만 확인하게 된다.
"""

from __future__ import annotations

from .report import CheckContext, CheckRow
from .rules import Rules
from .spec_io import SpecIndex

CHECK_ID = "read.convergence"


def jaccard(left: set, right: set) -> float:
    """`|A ∩ B| / |A ∪ B|`. 양쪽이 비면 1.0(비교할 것이 없으면 어긋남도 없다)."""
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def _element_texts(index: SpecIndex) -> set:
    return {element.get("text_verbatim") for element in index.elements.values()}


def _tree_edges(index: SpecIndex) -> set:
    """간선 = (부모 문언, 자식 문언). 최상위 element 의 부모는 소속 독립항 전문."""
    edges = set()
    for element_id, element in index.elements.items():
        parent_id = index.element_parent.get(element_id)
        if parent_id is None:
            claim_id = index.element_claim.get(element_id)
            parent_text = (index.claims.get(claim_id) or {}).get("text_verbatim")
        else:
            parent_text = (index.elements.get(parent_id) or {}).get("text_verbatim")
        edges.add((parent_text, element.get("text_verbatim")))
    return edges


def _dependent_signatures(index: SpecIndex) -> set:
    return {
        (
            claim.get("text_verbatim"),
            tuple(sorted(claim.get("depends_on") or [])),
            claim.get("dependency_type"),
        )
        for claim in index.dependents
    }


def _addition_attachments(index: SpecIndex) -> set:
    out = set()
    for addition in index.additions.values():
        target = index.elements.get(addition.get("attaches_to")) or {}
        out.add((addition.get("text_verbatim"), target.get("text_verbatim")))
    return out


def check(ctx: CheckContext) -> CheckRow:
    rules: Rules = ctx.rules
    row = CheckRow(
        check_id=CHECK_ID,
        ruleset="reader-rules#convergence",
        ruleset_version=rules.version,
        ruleset_size=len(rules.convergence_axes),
    )
    if ctx.peer_spec is None:
        # 2회차 READ 가 없으면 이 검사는 아무것도 반증하지 못한다 — 공허가 행에 드러난다.
        row.extras["skipped"] = True
        row.extras["axes"] = []
        row.extras["independent_count"] = []
        row.extras["dependent_count"] = []
        return row

    left = SpecIndex.build(ctx.spec)
    right = SpecIndex.build(ctx.peer_spec)
    row.checked = len(rules.convergence_axes)
    scores: dict[str, float] = {}

    for axis in rules.convergence_axes:
        axis_id = axis.get("id")
        threshold = axis.get("threshold")
        if axis_id == "independent-count":
            _compare_count(
                row, axis_id, len(left.independent), len(right.independent), "독립항"
            )
        elif axis_id == "dependent-count":
            _compare_count(
                row, axis_id, len(left.dependents), len(right.dependents), "종속항"
            )
        elif axis_id == "element-set":
            scores[axis_id] = _compare_sets(
                row, axis_id, _element_texts(left), _element_texts(right), threshold,
                "element 문언 집합",
            )
        elif axis_id == "tree-edges":
            scores[axis_id] = _compare_sets(
                row, axis_id, _tree_edges(left), _tree_edges(right), threshold,
                "트리 간선 집합(부모-자식 문언)",
            )
        elif axis_id == "dependent-set":
            scores[axis_id] = _compare_sets(
                row, axis_id, _dependent_signatures(left), _dependent_signatures(right),
                threshold, "종속항 서명 집합",
            )
        elif axis_id == "addition-attachment":
            scores[axis_id] = _compare_sets(
                row, axis_id, _addition_attachments(left), _addition_attachments(right),
                threshold, "부가 한정 부착 집합",
            )
        else:
            row.add(
                "convergence.unknown-axis",
                str(axis_id),
                str(axis_id),
                "구현된 수렴 축",
                "규칙 파일의 수렴 축을 검사기가 모른다 — 축이 늘었는데 구현이 따라오지 않았다",
            )

    row.extras["jaccard"] = scores
    row.extras["independent_count"] = [len(left.independent), len(right.independent)]
    row.extras["dependent_count"] = [len(left.dependents), len(right.dependents)]
    # 축별 실측치 — 판정 행은 pass/fail 만 말하므로 "얼마나 가까웠는가"는 여기 남는다.
    # 신설 4축의 임계 0.95 는 실측 근거가 없고(규칙 파일 open_question) 첫 런의 이 값이
    # 그 재정의 근거 자료가 된다.
    failed = {finding.rule for finding in row.findings}
    row.extras["axes"] = [
        {
            "id": axis.get("id"),
            "jaccard": scores.get(axis.get("id")),
            "threshold": float(axis["threshold"]) if axis.get("threshold") is not None else None,
            "status": "fail" if axis.get("id") in failed else "pass",
        }
        for axis in rules.convergence_axes
    ]
    return row


def _compare_count(row: CheckRow, axis_id: str, left: int, right: int, label: str) -> None:
    if left != right:
        row.add(
            axis_id,
            f"claims.{label}",
            f"{left} vs {right}",
            "두 독해가 같은 수",
            f"{label} 수가 다르다 — 트리 개수가 다르면 비교 자체가 무의미하다(즉시 실패)",
        )


def _compare_sets(
    row: CheckRow,
    axis_id: str,
    left: set,
    right: set,
    threshold,
    label: str,
) -> float:
    score = jaccard(left, right)
    if threshold is None:
        # ★ 조용한 기본값을 두지 않는다(M1 재감수 B-04). 구 구현은 임계가 없으면 0.95 를
        #   적용하면서 판정 상세에는 `threshold: null` 로 보고했다 — **계약 어디에도 없는
        #   수로 판정하고 그 사실을 보고서가 감췄다.** 코드가 법을 지어내는 것은 D7 이
        #   금지하는 자기 입법이며, 임계는 규칙 파일이 정하는 것이지 코드가 고르는 것이
        #   아니다. 없으면 판정하지 말고 결함으로 낸다.
        row.add(
            "convergence.threshold-missing",
            f"convergence.{axis_id}",
            "reader-rules.yaml#convergence.axes 에 threshold 없음",
            "축마다 명시된 임계",
            f"{label} 축의 임계가 계약에 없다 — 코드가 기본값을 지어내지 않는다",
        )
        return score
    limit = float(threshold)
    if score < limit:
        row.add(
            axis_id,
            f"convergence.{axis_id}",
            f"jaccard={score:.4f}",
            f"jaccard ≥ {limit}",
            f"{label}이 두 독해에서 수렴하지 않는다 — 절차 신호(Owner 에스컬레이션)",
        )
    return score
