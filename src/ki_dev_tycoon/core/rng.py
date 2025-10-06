"""Deterministic random number generation utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Iterable


@dataclass(slots=True)
class RandomSource:
    """Wrapper around :class:`random.Random` with explicit seeding."""

    seed: int
    _rng: Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)

    def randint(self, lower: int, upper: int) -> int:
        """Return an integer in ``[lower, upper]``.

        The result is deterministic for a given seed and sequence of calls.
        """

        return self._rng.randint(lower, upper)

    def choice(self, values: Iterable[object]) -> object:
        """Return a deterministic choice from ``values``."""

        sequence = tuple(values)
        if not sequence:
            msg = "RandomSource.choice received an empty sequence"
            raise ValueError(msg)
        return self._rng.choice(sequence)

    def random(self) -> float:
        """Return the next floating point value in [0.0, 1.0)."""

        return self._rng.random()

    def fork(self, offset: int) -> "RandomSource":
        """Create a derived random source with a deterministic offset."""

        return RandomSource(seed=self.seed + offset)
