"""Game state representation and deterministic updates."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Mapping

from ki_dev_tycoon.core.time import TimeProvider


def _clamp(value: float, lower: float, upper: float) -> float:
    """Clamp ``value`` into ``[lower, upper]``."""

    return max(lower, min(upper, value))


@dataclass(slots=True, frozen=True)
class GameState:
    """Immutable snapshot of the simulation state."""

    tick: int
    cash: float
    reputation: float

    def advance_tick(self, clock: TimeProvider) -> "GameState":
        """Return a new snapshot aligned with ``clock``."""

        return replace(self, tick=clock.current_tick())

    def apply_cash_delta(self, delta: float) -> "GameState":
        """Return a snapshot with adjusted cash."""

        return replace(self, cash=self.cash + delta)

    def apply_reputation_delta(self, delta: float) -> "GameState":
        """Return a snapshot with reputation clamped to ``[0, 100]``."""

        new_reputation = _clamp(self.reputation + delta, 0.0, 100.0)
        return replace(self, reputation=new_reputation)

    def to_dict(self) -> Dict[str, float | int]:
        """Serialise the snapshot into a JSON-friendly dictionary."""

        return {"tick": self.tick, "cash": self.cash, "reputation": self.reputation}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "GameState":
        """Create a snapshot from a dictionary payload."""

        return cls(
            tick=int(payload["tick"]),
            cash=float(payload["cash"]),
            reputation=float(payload["reputation"]),
        )
