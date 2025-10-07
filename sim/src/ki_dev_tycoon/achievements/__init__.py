"""Achievement tracking utilities for KI Dev Tycoon."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, Sequence

if TYPE_CHECKING:
    from ki_dev_tycoon.core.state import GameState

AchievementCondition = Callable[["GameState"], bool]


@dataclass(slots=True, frozen=True)
class AchievementDefinition:
    """Static descriptor that defines how an achievement is unlocked."""

    id: str
    name: str
    description: str
    condition: AchievementCondition


@dataclass(slots=True, frozen=True)
class AchievementSnapshot:
    """Immutable payload describing an unlocked achievement."""

    id: str
    name: str
    description: str
    unlocked_tick: int

    def to_dict(self) -> dict[str, str | int]:
        """Return a serialisable mapping representation."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "unlocked_tick": self.unlocked_tick,
        }


class AchievementTracker:
    """Deterministic achievement evaluation helper."""

    def __init__(self, definitions: Sequence[AchievementDefinition]):
        if not definitions:
            msg = "AchievementTracker requires at least one definition"
            raise ValueError(msg)
        self._definitions: dict[str, AchievementDefinition] = {
            definition.id: definition for definition in definitions
        }
        if len(self._definitions) != len(definitions):
            msg = "Achievement identifiers must be unique"
            raise ValueError(msg)
        self._unlocked: dict[str, AchievementSnapshot] = {}

    def evaluate(self, state: GameState) -> tuple[AchievementSnapshot, ...]:
        """Return newly unlocked achievements based on ``state``."""

        newly_unlocked: list[AchievementSnapshot] = []
        for definition in self._definitions.values():
            if definition.id in self._unlocked:
                continue
            if definition.condition(state):
                snapshot = AchievementSnapshot(
                    id=definition.id,
                    name=definition.name,
                    description=definition.description,
                    unlocked_tick=state.tick,
                )
                self._unlocked[definition.id] = snapshot
                newly_unlocked.append(snapshot)
        if newly_unlocked:
            newly_unlocked.sort(key=lambda item: item.unlocked_tick)
        return tuple(newly_unlocked)

    def extend(self, snapshots: Iterable[AchievementSnapshot]) -> None:
        """Prime the tracker with already unlocked ``snapshots``."""

        for snapshot in snapshots:
            if snapshot.id not in self._definitions:
                continue
            existing = self._unlocked.get(snapshot.id)
            if existing is None or existing.unlocked_tick > snapshot.unlocked_tick:
                self._unlocked[snapshot.id] = snapshot

    def unlocked(self) -> tuple[AchievementSnapshot, ...]:
        """Return a deterministic tuple of unlocked achievements."""

        return tuple(sorted(self._unlocked.values(), key=lambda item: item.unlocked_tick))

    def definitions(self) -> Iterator[AchievementDefinition]:
        """Yield the known achievement definitions."""

        return iter(self._definitions.values())


def default_definitions() -> tuple[AchievementDefinition, ...]:
    """Return the default set of achievements shipped with the core."""

    return (
        AchievementDefinition(
            id="first_hire",
            name="Recruiter",
            description="Hire your first team member.",
            condition=lambda state: bool(state.team.members),
        ),
        AchievementDefinition(
            id="cash_milestone",
            name="First Funding",
            description="Reach at least 50k cash reserves.",
            condition=lambda state: state.cash >= 50_000.0,
        ),
        AchievementDefinition(
            id="research_unlock",
            name="Breakthrough",
            description="Complete your first research project.",
            condition=lambda state: bool(state.research.unlocked),
        ),
    )
