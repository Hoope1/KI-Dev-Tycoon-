from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.core.time import FrozenTime, TickClock


def test_game_state_returns_new_snapshot_on_updates() -> None:
    state = GameState(tick=0, cash=100.0, reputation=50.0)
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
    state = GameState(tick=5, cash=0.0, reputation=5.0)

    assert state.apply_reputation_delta(-10.0).reputation == 0.0
    assert state.apply_reputation_delta(200.0).reputation == 100.0


def test_game_state_serialization_roundtrip() -> None:
    frozen_time = FrozenTime(tick=12)
    state = GameState(tick=0, cash=42.5, reputation=70.0).advance_tick(frozen_time)

    payload = state.to_dict()
    restored = GameState.from_dict(payload)

    assert restored == state
