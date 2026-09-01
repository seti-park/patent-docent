# -*- coding: utf-8 -*-
"""`read.convergence` — 독립 2회 READ 비교(SPEC §2.6 검사 4 · reader-rules#convergence).

의미는 품질이 아니라 **안정성**이다. 두 독립 실행이 다른 청구항 트리를 낳으면 그 소재에
대한 독해는 재현되지 않는 것이고, 이후 모든 결정론 검사의 기준점이 흔들린다(SPEC §1.4).

구 검사는 **독립항 수와 element `text_verbatim` 집합**만 봤다. 집합 비교이므로 같은 문자열
집합이 서로 다른 계층으로 조립되어도, 종속항이 통째로 흔들려도 수렴한 것으로 판정됐다
(재감수 M-07). 6축 전부를 본다.

★ 6축은 이제 **같은 무게가 아니다**(재정 2026-08-18 P-3). 셋은 법이고 둘은 계기이며 하나는
관찰이다:

  - `exact-match`        결정론적으로 유일해야 하는 구조 사실 — 미달 = 판정 행 **fail**
  - `escalation-trigger` 해석 여지가 있는 축 — 미달 = fail 이 **아니라** `escalations[]` 등재
                         (스테이지가 Owner 에게 상신한다)
  - `measure-only`       판정 제외·측정 전용 — 아무 판정도 하지 않고 값만 기록한다

축 → 정책의 대응은 `reader-rules.yaml#convergence.axes[].policy` 가 정본이고, 정책의 의미
(임계 요구·status 어휘)는 같은 파일의 `convergence.policies` 가 정본이다. 코드는 어느 축이
어느 층인지 **고르지 않는다** — 고르는 순간 검사가 자기 입법이 된다(D7).

그래서 이 검사의 산출은 단일 판정이 아니라 **세 층의 보고서**다. 판정 행(법) · 상신 목록
(계기) · 독해 프로파일(관찰). 마지막 것의 프레임이 문언의 일부다 — 갈린 항목의 목록은
"결함 후보"가 아니라 **두 독해가 어떻게 갈렸는가의 기술**이며, 갈림 자체가 실패를 뜻하지
않는다.

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
        row.extras["escalations"] = []
        row.extras["profile"] = {"axes": [], "escalations": [], "divergences": []}
        return row

    left = SpecIndex.build(ctx.spec)
    right = SpecIndex.build(ctx.peer_spec)
    row.checked = len(rules.convergence_axes)

    scores: dict[str, float] = {}
    statuses: dict[str, str] = {}
    escalations: list[dict] = []
    divergences: list[dict] = []

    for axis in rules.convergence_axes:
        axis_id = axis.get("id")
        policy = rules.policy_of(axis)
        if axis_id == "independent-count":
            statuses[axis_id] = _compare_count(
                row, axis, policy, len(left.independent), len(right.independent), "독립항"
            )
        elif axis_id == "dependent-count":
            statuses[axis_id] = _compare_count(
                row, axis, policy, len(left.dependents), len(right.dependents), "종속항"
            )
        elif axis_id == "element-set":
            statuses[axis_id] = _compare_sets(
                row, axis, policy, rules, scores, escalations, divergences,
                _element_texts(left), _element_texts(right), "element 문언 집합",
            )
        elif axis_id == "tree-edges":
            statuses[axis_id] = _compare_sets(
                row, axis, policy, rules, scores, escalations, divergences,
                _tree_edges(left), _tree_edges(right), "트리 간선 집합(부모-자식 문언)",
            )
        elif axis_id == "dependent-set":
            statuses[axis_id] = _compare_sets(
                row, axis, policy, rules, scores, escalations, divergences,
                _dependent_signatures(left), _dependent_signatures(right),
                "종속항 서명 집합",
            )
        elif axis_id == "addition-attachment":
            statuses[axis_id] = _compare_sets(
                row, axis, policy, rules, scores, escalations, divergences,
                _addition_attachments(left), _addition_attachments(right),
                "부가 한정 부착 집합",
            )
        else:
            statuses[axis_id] = "fail"
            row.add(
                "convergence.unknown-axis",
                str(axis_id),
                str(axis_id),
                "구현된 수렴 축",
                "규칙 파일의 수렴 축을 검사기가 모른다 — 축이 늘었는데 구현이 따라오지 않았다",
            )

    axis_rows = [
        {
            "id": axis.get("id"),
            "policy": axis.get("policy"),
            "jaccard": scores.get(axis.get("id")),
            "threshold": (
                float(axis["threshold"]) if axis.get("threshold") is not None else None
            ),
            "status": statuses.get(axis.get("id"), "fail"),
        }
        for axis in rules.convergence_axes
    ]

    row.extras["jaccard"] = scores
    row.extras["independent_count"] = [len(left.independent), len(right.independent)]
    row.extras["dependent_count"] = [len(left.dependents), len(right.dependents)]
    row.extras["axes"] = axis_rows
    row.extras["escalations"] = escalations
    # ★ 독해 프로파일(재정 P-3 의 상신 서식). 축별 값 + 갈린 항목의 실물을 함께 싣는다 —
    #   "얼마나 갈렸는가"(jaccard)만으로는 Owner 가 무엇을 볼지 정할 수 없기 때문이다.
    row.extras["profile"] = {
        "frame": str(rules.convergence_profile.get("frame_label") or ""),
        "axes": axis_rows,
        "escalations": escalations,
        "divergences": divergences,
    }
    return row


def _compare_count(
    row: CheckRow,
    axis: dict,
    policy: dict,
    left: int,
    right: int,
    label: str,
) -> str:
    """개수 축 — 유사도를 재지 않고 같은가 다른가만 본다(임계 대상이 아니다)."""
    axis_id = axis.get("id")
    if left == right:
        return str(policy.get("status_on_pass", "pass"))
    status = str(policy.get("status_on_miss", "fail"))
    if status == "fail":
        row.add(
            axis_id,
            f"claims.{label}",
            f"{left} vs {right}",
            "두 독해가 같은 수",
            f"{label} 수가 다르다 — 트리 개수가 다르면 비교 자체가 무의미하다(즉시 실패)",
        )
    return status


def _compare_sets(
    row: CheckRow,
    axis: dict,
    policy: dict,
    rules: Rules,
    scores: dict,
    escalations: list,
    divergences: list,
    left: set,
    right: set,
    label: str,
) -> str:
    """집합 축 — Jaccard 를 재고 **정책에 따라** 처분한다(재정 P-3)."""
    axis_id = axis.get("id")
    score = jaccard(left, right)
    scores[axis_id] = score

    # 갈린 항목은 정책과 무관하게 기록한다. 측정 전용 축도 "무엇이 갈렸는가"는 남긴다 —
    # 부착 관례 입법의 근거 자료가 바로 그 실물이기 때문이다.
    difference = _divergence(rules, axis_id, left, right)
    if difference is not None:
        divergences.append(difference)

    if not policy.get("threshold_required"):
        # 측정 전용 — 아무 판정도 하지 않는다. threshold 부재가 정상이며, 있어도 쓰지 않는다.
        return str(policy.get("status_on_pass", "measured"))

    threshold = axis.get("threshold")
    if threshold is None:
        # ★ 조용한 기본값을 두지 않는다(M1 재감수 B-04). 구 구현은 임계가 없으면 0.95 를
        #   적용하면서 판정 상세에는 `threshold: null` 로 보고했다 — **계약 어디에도 없는
        #   수로 판정하고 그 사실을 보고서가 감췄다.** 코드가 법을 지어내는 것은 D7 이
        #   금지하는 자기 입법이며, 임계는 규칙 파일이 정하는 것이지 코드가 고르는 것이
        #   아니다. 없으면 판정하지 말고 결함으로 낸다.
        #   재정 P-3 이후에도 이 보수는 유지된다 — 다만 `measure-only` 축은 임계 부재가
        #   정상이므로 위에서 이미 돌아갔고, 여기 오는 것은 임계를 **요구하는** 정책뿐이다.
        row.add(
            "convergence.threshold-missing",
            f"convergence.{axis_id}",
            "reader-rules.yaml#convergence.axes 에 threshold 없음",
            f"policy={axis.get('policy')} 축에 명시된 임계",
            f"{label} 축의 임계가 계약에 없다 — 코드가 기본값을 지어내지 않는다",
        )
        return "fail"

    limit = float(threshold)
    if score >= limit:
        return str(policy.get("status_on_pass", "pass"))

    status = str(policy.get("status_on_miss", "fail"))
    if status == "fail":
        row.add(
            axis_id,
            f"convergence.{axis_id}",
            f"jaccard={score:.4f}",
            f"jaccard ≥ {limit}",
            f"{label}이 두 독해에서 수렴하지 않는다 — 결정론적으로 유일해야 하는 구조 "
            "사실이므로 완전 일치를 요구한다(재정 P-3)",
        )
    else:
        # ★ 상신 축의 미달은 **결함이 아니다**(재정 P-3). `row.add` 하지 않고 상신 목록에만
        #   싣는다 — 판정 행을 fail 로 만들면 "실패가 아니라 상신"이 문서에만 남는다.
        escalations.append({"axis": axis_id, "jaccard": score, "threshold": limit})
    return status


def _divergence(rules: Rules, axis_id: str, left: set, right: set) -> dict | None:
    """갈린 항목의 양쪽 차집합. 상한 건수·절단 폭은 규칙 파일이 정한다."""
    only_left = left - right
    only_right = right - left
    if not only_left and not only_right:
        return None
    profile = rules.convergence_profile
    limit = int(profile.get("max_items_per_direction", 20))
    width = int(profile.get("truncate_chars", 200))
    suffix = str(profile.get("truncation_suffix", " …"))

    def render(values: set) -> list:
        # 정렬해서 자른다 — 집합의 반복 순서는 실행마다 달라질 수 있고, 상신 서식이
        # 결정론이 아니면 같은 두 독해가 매번 다른 보고서를 낸다.
        return [
            _truncate_parts(value, width, suffix)
            for value in sorted(values, key=_sort_key)[:limit]
        ]

    return {
        "axis": axis_id,
        "only_in_canonical": render(only_left),
        "only_in_peer": render(only_right),
    }


def _flatten(value) -> str:
    """축마다 원소 형태가 다르다(문자열·튜플). 상신 서식은 한 줄 문자열로 통일한다."""
    if isinstance(value, tuple):
        return " | ".join(_flatten(part) for part in value)
    if value is None:
        return ""
    return str(value)


def _sort_key(value) -> str:
    return _flatten(value)


# 부분 하나에 최소한 남겨 둘 폭. 원소가 여럿이어도 각 부분이 식별 가능해야 한다.
_MIN_PART_CHARS = 24


def _truncate_parts(value, width: int, suffix: str) -> str:
    """구성 부분마다 **예산을 나눠** 자른다(백로그 G-10 의 처분 · 2026-09-01).

    ★ 구 구현은 이어 붙인 뒤 **앞에서** 잘랐다. 그러면 앞 부분(간선의 부모 문언)이 긴 축에서
    예산을 통째로 먹고 **뒤 부분(자식)이 아예 들어가지 않는다.** 부모가 같은 항목들이
    **저장 문자열까지 동일**해지고, 갈린 자리를 보이려고 존재하는 보고가 **정확히 그때**
    아무것도 못 보인다.

    실측(2026-09-01 · `gdm-wo2026128750a1-agent-memory`): `tree-edges` 의
    `only_in_canonical` 5건이 전부 같은 202자였다 — 부모가 868 B 청구항 전문이었기 때문이다.
    표시만의 문제가 아니라 **파일에 잘린 채 저장**되어 사후 복구도 되지 않았다.

    그래서 폭은 이제 **부분당 예산**이며 전체 길이가 `width` 를 넘을 수 있다. 그것이 의도다 —
    이 값의 목적은 파일 크기 절약이 아니라 **한 항목을 다른 항목과 구별 가능하게 두는 것**이다.
    """
    parts = [_flatten(part) for part in value] if isinstance(value, tuple) else [_flatten(value)]
    if not parts:
        return ""
    share = max(width // len(parts), _MIN_PART_CHARS)
    return " | ".join(
        part if len(part) <= share else part[:share] + suffix for part in parts
    )
