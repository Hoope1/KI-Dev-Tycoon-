"""Deterministic tick loop with accumulator semantics."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.time import TimeProvider

TickHandler = Callable[[int, RandomSource], None]
TimeSource = Callable[[], float]
SleepFunction = Callable[[float], None]


@dataclass(slots=True)
class TickLoop:
    """Fixed-step accumulator loop for deterministic tick processing."""

    clock: TimeProvider
    rng: RandomSource
    tick_duration: float = 0.5
    time_source: TimeSource | None = None
    sleep: SleepFunction | None = None
    _accumulator: float = field(default=0.0, init=False)
    _last_time: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        if self.tick_duration <= 0:
            msg = "TickLoop requires a positive tick_duration"
            raise ValueError(msg)
        if self.time_source is None:
            self.time_source = time.perf_counter
        if self.sleep is None:
            self.sleep = lambda _: None
        self._last_time = self.time_source()

    def advance_by(self, delta_seconds: float, handler: TickHandler) -> int:
        """Advance the loop by ``delta_seconds`` and process pending ticks."""

        if delta_seconds < 0:
            msg = "TickLoop cannot be advanced by a negative duration"
            raise ValueError(msg)
        processed = 0
        self._accumulator += delta_seconds
        while self._accumulator + 1e-12 >= self.tick_duration:
            self.clock.advance()
            handler(self.clock.current_tick(), self.rng)
            self._accumulator -= self.tick_duration
            processed += 1
        return processed

    def step(self, handler: TickHandler) -> int:
        """Sample the time source once and process any accumulated ticks."""

        now = self.time_source()
        delta = max(0.0, now - self._last_time)
        self._last_time = now
        return self.advance_by(delta, handler)

    def run(self, ticks: int, handler: TickHandler) -> None:
        """Run the loop until ``ticks`` iterations have been processed."""

        if ticks < 0:
            msg = "TickLoop cannot run a negative number of ticks"
            raise ValueError(msg)
        processed = 0
        while processed < ticks:
            processed += self.step(handler)
            if processed < ticks and self._accumulator < self.tick_duration:
                remaining = self.tick_duration - self._accumulator
                self.sleep(remaining)
