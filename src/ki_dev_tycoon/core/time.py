"""Tick based time utilities."""

from __future__ import annotations

from dataclasses import dataclass


class TimeProvider:
    """Interface describing how the simulation accesses time."""

    def current_tick(self) -> int:
        raise NotImplementedError


@dataclass(slots=True)
class TickClock(TimeProvider):
    """Simple monotonic tick counter."""

    tick: int = 0

    def advance(self, steps: int = 1) -> int:
        if steps < 0:
            msg = "TickClock cannot advance backwards"
            raise ValueError(msg)
        self.tick += steps
        return self.tick

    def current_tick(self) -> int:
        return self.tick
