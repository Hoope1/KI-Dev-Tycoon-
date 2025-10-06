"""Deterministic random number generation utilities."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from random import Random
from typing import Iterable, Tuple, TypeVar

T = TypeVar("T")


def _normalise_seed(raw_seed: int) -> int:
    """Clamp ``raw_seed`` into the valid range for :class:`random.Random`."""

    # CPython accepts any hashable seed, but normalising keeps values positive and
    # within a deterministic 63-bit range for reproducibility across platforms.
    return abs(raw_seed) % (2**63 - 1)


@dataclass(slots=True)
class RandomSource:
    """Wrapper around :class:`random.Random` with explicit seeding."""

    seed: int
    _rng: Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = Random(_normalise_seed(self.seed))

    def randint(self, lower: int, upper: int) -> int:
        """Return an integer in ``[lower, upper]`` deterministically."""

        return self._rng.randint(lower, upper)

    def choice(self, values: Iterable[T]) -> T:
        """Return a deterministic choice from ``values``.

        Raises:
            ValueError: If ``values`` is empty.
        """

        sequence: Tuple[T, ...] = tuple(values)
        if not sequence:
            msg = "RandomSource.choice received an empty sequence"
            raise ValueError(msg)
        return self._rng.choice(sequence)

    def random(self) -> float:
        """Return the next floating point value in ``[0.0, 1.0)``."""

        return self._rng.random()

    def fork(self, offset: int) -> "RandomSource":
        """Create a derived random source with a deterministic integer offset."""

        derived_seed = _normalise_seed(self.seed + offset)
        return RandomSource(seed=derived_seed)

    def namespaced(self, namespace: str) -> "RandomSource":
        """Derive a deterministic child source scoped by ``namespace``.

        Using a namespace allows stable seeds for subsystems (e.g. events,
        economy) without relying on implicit call ordering.
        """

        payload = f"{self.seed}:{namespace}".encode("utf-8")
        digest = hashlib.sha256(payload).digest()
        derived_seed = int.from_bytes(digest[:8], "big")
        return RandomSource(seed=_normalise_seed(derived_seed))
