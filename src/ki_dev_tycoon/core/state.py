"""Game state representation and deterministic updates."""

from __future__ import annotations

from dataclasses import dataclass

from ki_dev_tycoon.core.time import TimeProvider


@dataclass(slots=True)
class GameState:
    """Minimal subset of the game state for early prototypes."""

    tick: int
    cash: float
    reputation: float

    def advance_tick(self, clock: TimeProvider) -> None:
        """Synchronise the state tick with the clock."""

        self.tick = clock.current_tick()

    def apply_cash_delta(self, delta: float) -> None:
        self.cash += delta

    def apply_reputation_delta(self, delta: float) -> None:
        self.reputation = max(0.0, min(100.0, self.reputation + delta))
