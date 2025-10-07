from ki_dev_tycoon.core.state import (
    GameState,
    ProductState,
    ResearchState,
    TeamMember,
    TeamState,
)
from ki_dev_tycoon.core.time import FrozenTime, TickClock


def _empty_state() -> GameState:
    team = TeamState(members=(TeamMember(role_id="engineer", skill=0.3, training_progress=0.0),))
    products = (ProductState(product_id="p", quality=0.4, adoption=10, price=5.0),)
    research = ResearchState(unlocked=frozenset(), active=None, progress=0.0, backlog=())
    return GameState(tick=0, cash=100.0, reputation=50.0, team=team, products=products, research=research)


def test_game_state_returns_new_snapshot_on_updates() -> None:
    state = _empty_state()
    clock = TickClock()

    clock.advance(3)
    advanced = state.advance_tick(clock)
    updated_cash = advanced.apply_cash_delta(25.0)
    updated_rep = updated_cash.apply_reputation_delta(10.0)

    assert state.tick == 0  # original unchanged
    assert advanced.tick == 3
    assert updated_cash.cash == 125.0
    assert updated_rep.reputation == 60.0


def test_game_state_reputation_is_clamped() -> None:
    state = _empty_state()

    assert state.apply_reputation_delta(-200.0).reputation == 0.0
    assert state.apply_reputation_delta(200.0).reputation == 100.0


def test_game_state_serialization_roundtrip() -> None:
    frozen_time = FrozenTime(tick=12)
    state = _empty_state().advance_tick(frozen_time)

    payload = state.to_dict()
    restored = GameState.from_dict(payload)

    assert restored == state
