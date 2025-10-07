"""Game state representation and deterministic updates."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any, Dict, Iterable, Mapping, Sequence

from ki_dev_tycoon.core.time import TimeProvider

if TYPE_CHECKING:
    from ki_dev_tycoon.achievements import AchievementSnapshot


def _clamp(value: float, lower: float, upper: float) -> float:
    """Clamp ``value`` into ``[lower, upper]``."""

    return max(lower, min(upper, value))


@dataclass(slots=True, frozen=True)
class TeamMember:
    """Immutable snapshot of a single team member."""

    role_id: str
    skill: float
    training_progress: float = 0.0

    def gain_skill(self, delta: float) -> "TeamMember":
        """Return a new member with ``skill`` increased by ``delta``."""

        new_skill = _clamp(self.skill + delta, 0.0, 1.0)
        return replace(self, skill=new_skill)

    def advance_training(self, delta: float) -> "TeamMember":
        """Advance the training progress while keeping it within [0, 1]."""

        new_progress = _clamp(self.training_progress + delta, 0.0, 1.0)
        return replace(self, training_progress=new_progress)

    def reset_training(self) -> "TeamMember":
        """Reset accumulated training progress."""

        return replace(self, training_progress=0.0)

    def to_dict(self) -> Dict[str, float | str]:
        return {
            "role_id": self.role_id,
            "skill": self.skill,
            "training_progress": self.training_progress,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TeamMember":
        return cls(
            role_id=str(payload["role_id"]),
            skill=float(payload["skill"]),
            training_progress=float(payload.get("training_progress", 0.0)),
        )


@dataclass(slots=True, frozen=True)
class TeamState:
    """Immutable container describing the complete team composition."""

    members: tuple[TeamMember, ...]

    def add_member(self, member: TeamMember) -> "TeamState":
        """Return a new team state with ``member`` appended."""

        return replace(self, members=self.members + (member,))

    def members_by_role(self, role_id: str) -> Sequence[TeamMember]:
        """Return all members matching ``role_id``."""

        return tuple(member for member in self.members if member.role_id == role_id)

    def average_skill(self, role_id: str) -> float:
        """Return the average skill for ``role_id`` or zero if empty."""

        relevant = self.members_by_role(role_id)
        if not relevant:
            return 0.0
        return sum(member.skill for member in relevant) / len(relevant)

    def to_dict(self) -> Dict[str, Any]:
        return {"members": [member.to_dict() for member in self.members]}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TeamState":
        members_payload = payload.get("members", [])
        members = tuple(TeamMember.from_dict(raw) for raw in members_payload)
        return cls(members=members)


@dataclass(slots=True, frozen=True)
class ProductState:
    """Immutable representation of a single product."""

    product_id: str
    quality: float
    adoption: int
    price: float

    def update_quality(self, quality: float) -> "ProductState":
        """Return a new product state with clamped quality."""

        return replace(self, quality=_clamp(quality, 0.0, 1.0))

    def update_adoption(self, adoption: int) -> "ProductState":
        """Return a new product state with ``adoption`` set."""

        return replace(self, adoption=max(0, adoption))

    def to_dict(self) -> Dict[str, float | int | str]:
        return {
            "product_id": self.product_id,
            "quality": self.quality,
            "adoption": self.adoption,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ProductState":
        return cls(
            product_id=str(payload["product_id"]),
            quality=float(payload["quality"]),
            adoption=int(payload.get("adoption", 0)),
            price=float(payload.get("price", 0.0)),
        )


@dataclass(slots=True, frozen=True)
class ResearchState:
    """Tracks technology unlocks and the active research project."""

    unlocked: frozenset[str]
    active: str | None
    progress: float
    backlog: tuple[str, ...]

    def with_active(self, node_id: str | None) -> "ResearchState":
        return replace(self, active=node_id, progress=0.0)

    def advance(self, delta: float) -> "ResearchState":
        return replace(self, progress=_clamp(self.progress + delta, 0.0, 1.0))

    def complete(self, node_id: str) -> "ResearchState":
        unlocked = set(self.unlocked)
        unlocked.add(node_id)
        remaining_backlog = tuple(item for item in self.backlog if item != node_id)
        return replace(
            self,
            unlocked=frozenset(unlocked),
            active=None,
            progress=0.0,
            backlog=remaining_backlog,
        )

    def enqueue(self, node_id: str) -> "ResearchState":
        if node_id in self.backlog or node_id in self.unlocked:
            return self
        return replace(self, backlog=self.backlog + (node_id,))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unlocked": sorted(self.unlocked),
            "active": self.active,
            "progress": self.progress,
            "backlog": list(self.backlog),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ResearchState":
        unlocked_payload = payload.get("unlocked", [])
        backlog_payload = payload.get("backlog", [])
        return cls(
            unlocked=frozenset(map(str, unlocked_payload)),
            active=payload.get("active"),
            progress=float(payload.get("progress", 0.0)),
            backlog=tuple(map(str, backlog_payload)),
        )


@dataclass(slots=True, frozen=True)
class GameState:
    """Immutable snapshot of the simulation state."""

    tick: int
    cash: float
    reputation: float
    team: TeamState
    products: tuple[ProductState, ...]
    research: ResearchState
    achievements: tuple["AchievementSnapshot", ...] = field(default_factory=tuple)

    def advance_tick(self, clock: TimeProvider) -> "GameState":
        """Return a new snapshot aligned with ``clock``."""

        return replace(self, tick=clock.current_tick())

    def apply_cash_delta(self, delta: float) -> "GameState":
        """Return a snapshot with adjusted cash."""

        new_cash = max(0.0, self.cash + delta)
        return replace(self, cash=new_cash)

    def apply_reputation_delta(self, delta: float) -> "GameState":
        """Return a snapshot with reputation clamped to ``[0, 100]``."""

        new_reputation = _clamp(self.reputation + delta, 0.0, 100.0)
        return replace(self, reputation=new_reputation)

    def update_product(self, product_id: str, updated: ProductState) -> "GameState":
        products = tuple(
            updated if product.product_id == product_id else product
            for product in self.products
        )
        return replace(self, products=products)

    def update_research(self, research: ResearchState) -> "GameState":
        return replace(self, research=research)

    def update_team(self, team: TeamState) -> "GameState":
        return replace(self, team=team)

    def add_achievements(
        self, achievements: Iterable["AchievementSnapshot"]
    ) -> "GameState":
        """Return a new snapshot with ``achievements`` appended if new."""

        achievements = tuple(achievements)
        if not achievements:
            return self
        known_ids = {achievement.id for achievement in self.achievements}
        new_items = tuple(
            achievement for achievement in achievements if achievement.id not in known_ids
        )
        if not new_items:
            return self
        combined = self.achievements + new_items
        combined = tuple(sorted(combined, key=lambda item: item.unlocked_tick))
        return replace(self, achievements=combined)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "cash": self.cash,
            "reputation": self.reputation,
            "team": self.team.to_dict(),
            "products": [product.to_dict() for product in self.products],
            "research": self.research.to_dict(),
            "achievements": [
                {
                    "id": achievement.id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "unlocked_tick": achievement.unlocked_tick,
                }
                for achievement in self.achievements
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "GameState":
        from ki_dev_tycoon.achievements import AchievementSnapshot

        products_payload: Iterable[Mapping[str, Any]] = payload.get("products", [])
        products = tuple(ProductState.from_dict(raw) for raw in products_payload)
        achievements_payload: Iterable[Mapping[str, Any]] = payload.get("achievements", [])
        achievements = tuple(
            AchievementSnapshot(
                id=str(raw["id"]),
                name=str(raw["name"]),
                description=str(raw.get("description", "")),
                unlocked_tick=int(raw["unlocked_tick"]),
            )
            for raw in achievements_payload
        )
        return cls(
            tick=int(payload["tick"]),
            cash=float(payload["cash"]),
            reputation=float(payload["reputation"]),
            team=TeamState.from_dict(payload.get("team", {})),
            products=products,
            research=ResearchState.from_dict(payload.get("research", {})),
            achievements=achievements,
        )
