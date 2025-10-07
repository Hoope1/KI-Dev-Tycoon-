from __future__ import annotations

import math
from collections import deque
from typing import Deque, List

import pytest
from hypothesis import given, strategies as st

from ki_dev_tycoon.core.loop import TickLoop
from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.time import TickClock


def test_tick_loop_runs_requested_ticks() -> None:
    """The loop should process ticks using the configured time source."""

    samples: Deque[float] = deque([0.0, 0.5, 1.0, 1.5])

    def time_source() -> float:
        return samples.popleft()

    processed: List[int] = []
    loop = TickLoop(
        clock=TickClock(),
        rng=RandomSource(seed=1),
        time_source=time_source,
        sleep=lambda _: None,
    )

    loop.run(3, lambda tick, _: processed.append(tick))

    assert processed == [1, 2, 3]


def test_tick_loop_rejects_negative_delta() -> None:
    clock = TickClock()
    loop = TickLoop(clock=clock, rng=RandomSource(seed=2))

    with pytest.raises(ValueError):
        loop.advance_by(-0.1, lambda *_: None)


@given(st.lists(st.floats(min_value=0.0, max_value=1.5), min_size=1, max_size=25))
def test_tick_loop_tick_count_matches_elapsed(deltas: List[float]) -> None:
    clock = TickClock()
    rng = RandomSource(seed=42)
    loop = TickLoop(clock=clock, rng=rng)

    total_elapsed = 0.0
    processed = 0

    for delta in deltas:
        processed += loop.advance_by(delta, lambda *_: None)
        total_elapsed += delta

    expected_ticks = math.floor(total_elapsed / loop.tick_duration)
    assert clock.current_tick() == expected_ticks
    assert processed == expected_ticks


@given(
    st.integers(min_value=0, max_value=2**32 - 1),
    st.lists(st.floats(min_value=0.0, max_value=2.0), min_size=1, max_size=20),
)
def test_tick_loop_rng_stream_is_deterministic(seed: int, deltas: List[float]) -> None:
    def run_once() -> List[float]:
        clock = TickClock()
        rng = RandomSource(seed=seed)
        loop = TickLoop(clock=clock, rng=rng)
        samples: List[float] = []
        for delta in deltas:
            loop.advance_by(delta, lambda _tick, source: samples.append(source.random()))
        return samples

    first = run_once()
    second = run_once()

    assert first == second
