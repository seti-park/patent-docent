"""M28 — 재정 T58 ② READ 하위 레인 좌석 값(2026-09-13).

원장 = docs/decisions/ruling-20260913-03-T58.md ②. 계약 `contracts/stages/read.yaml` 의
sub_lanes 값과 `model_identity.labels` 의 `fable-5.1` 등재가 그 재정과 같은지를 본다.
"""

from __future__ import annotations

import os

from engine.lanes.plan import lane_profiles

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_t58_seat_values_match_ruling():
    profiles = lane_profiles(REPO)
    seats = {task: (p["model"], p["effort"]) for task, p in profiles.items()}
    expected = {
        "decompose": ("fable-5.1", "low"),
        "synthesize": ("fable-5.1", "low"),
        "ground-independent": ("opus-5", "low"),
        "ground-dependent": ("opus-5", "low"),
    }
    for task, value in expected.items():
        assert seats[task] == value, f"{task}: {seats[task]} != {value} (재정 T58 ②)"


def test_t58_fable_label_normalises_api_identifier():
    profiles = lane_profiles(REPO)
    accepted = profiles["decompose"]["accepted_models"]
    assert "fable-5.1" in accepted
    assert "claude-fable-5-1" in accepted
    assert "fable" in accepted
