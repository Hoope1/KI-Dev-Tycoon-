from __future__ import annotations

import pytest

from ki_dev_tycoon.achievements import (
    AchievementDefinition,
    AchievementSnapshot,
    AchievementTracker,
    default_definitions,
)
from ki_dev_tycoon.core.state import GameState, ResearchState, TeamState


def _base_state() -> GameState:
    return GameState(
        tick=0,
        cash=0.0,
        reputation=50.0,
        team=TeamState(members=()),
        products=(),
        research=ResearchState(unlocked=frozenset(), active=None, progress=0.0, backlog=()),
    )


def test_tracker_unlocks_cash_milestone() -> None:
    tracker = AchievementTracker(default_definitions())
    state = _base_state().apply_cash_delta(60_000.0)

    unlocked = tracker.evaluate(state)

    assert any(item.id == "cash_milestone" for item in unlocked)
    assert tracker.evaluate(state) == ()


def test_tracker_can_be_seeded_with_existing_snapshots() -> None:
    tracker = AchievementTracker(default_definitions())
    snapshot = AchievementSnapshot(
        id="first_hire",
        name="Recruiter",
        description="",
        unlocked_tick=3,
    )
    tracker.extend((snapshot,))

    assert tracker.evaluate(_base_state()) == ()


def test_tracker_validates_unique_identifiers() -> None:
    definition = AchievementDefinition(
        id="duplicate",
        name="Duplicate",
        description="",
        condition=lambda state: True,
    )
    with pytest.raises(ValueError):
        AchievementTracker(())
    tracker = AchievementTracker((definition,))
    assert tracker.evaluate(_base_state()) != ()
