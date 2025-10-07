import pytest
from hypothesis import given, strategies as st

from ki_dev_tycoon.core.time import FrozenTime, TickClock


def test_tick_clock_advances_monotonically() -> None:
    clock = TickClock()

    assert clock.current_tick() == 0
    assert clock.advance() == 1
    assert clock.advance(4) == 5
    assert clock.current_tick() == 5


def test_tick_clock_rejects_negative_steps() -> None:
    clock = TickClock()

    with pytest.raises(ValueError):
        clock.advance(-1)


def test_frozen_time_returns_constant_tick() -> None:
    frozen = FrozenTime(tick=42)

    assert frozen.current_tick() == 42
    # Frozen time providers never change, even if tick would be modified elsewhere.
    assert frozen.current_tick() == 42


@given(st.lists(st.integers(min_value=0, max_value=5), min_size=1, max_size=20))
def test_tick_clock_advances_by_variable_steps(steps: list[int]) -> None:
    clock = TickClock()
    total = 0
    for step in steps:
        clock.advance(step)
        total += step
    assert clock.current_tick() == total
