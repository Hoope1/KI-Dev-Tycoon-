"""Tick based time utilities."""

from __future__ import annotations

from dataclasses import dataclass


class TimeProvider:
    """Interface describing how the simulation accesses time."""

    def current_tick(self) -> int:
        """Return the current simulation tick."""

        raise NotImplementedError


@dataclass(slots=True)
class TickClock(TimeProvider):
    """Simple monotonic tick counter."""

    tick: int = 0

    def advance(self, steps: int = 1) -> int:
        """Advance the clock by ``steps`` ticks and return the new position."""

        if steps < 0:
            msg = "TickClock cannot advance backwards"
            raise ValueError(msg)
        self.tick += steps
        return self.tick

    def current_tick(self) -> int:
        """Return the current tick value."""

        return self.tick


@dataclass(slots=True)
class FrozenTime(TimeProvider):
    """Time provider that always returns a fixed tick value."""

    tick: int

    def current_tick(self) -> int:
        """Return the frozen tick value without modification."""

        return self.tick
