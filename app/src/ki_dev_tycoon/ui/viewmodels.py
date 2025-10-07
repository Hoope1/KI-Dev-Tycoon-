"""Immutable view models shared between Textual screens."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True, frozen=True)
class KpiSnapshot:
    """Key performance indicator values captured for a single tick."""

    tick: int
    cash: float
    reputation: float
    revenue: float
    adoption: int
    avg_quality: float
    cash_delta: float


@dataclass(slots=True, frozen=True)
class DashboardViewModel:
    """Aggregated dashboard data for the active simulation."""

    current_tick: int
    cash: float
    reputation: float
    burn_rate: float
    daily_revenue: float
    adoption: int
    avg_quality: float
    history: tuple[KpiSnapshot, ...]

    def tail(self, count: int = 10) -> tuple[KpiSnapshot, ...]:
        """Return the most recent ``count`` KPI snapshots."""

        if count <= 0:
            return ()
        return self.history[-count:]


@dataclass(slots=True, frozen=True)
class TeamMemberViewModel:
    """Lightweight representation of a staff member."""

    role_id: str
    role_name: str
    skill: float
    training_progress: float
    salary: float


@dataclass(slots=True, frozen=True)
class TeamViewModel:
    """Immutable team overview used by the team screen."""

    members: tuple[TeamMemberViewModel, ...]

    @property
    def headcount(self) -> int:
        return len(self.members)

    def members_by_role(self, role_id: str) -> Iterable[TeamMemberViewModel]:
        return tuple(member for member in self.members if member.role_id == role_id)


@dataclass(slots=True, frozen=True)
class ResearchNodeViewModel:
    """Describes a single entry in the research tree."""

    node_id: str
    name: str
    cost: int
    unlocked: bool
    in_backlog: bool


@dataclass(slots=True, frozen=True)
class ResearchViewModel:
    """Aggregates the state of the research subsystem."""

    active: str | None
    progress: float
    unlocked: tuple[str, ...]
    backlog: tuple[str, ...]
    nodes: tuple[ResearchNodeViewModel, ...]


@dataclass(slots=True, frozen=True)
class ProductViewModel:
    """View model describing a product and its KPIs."""

    product_id: str
    name: str
    market: str
    price: float
    quality: float
    adoption: int


@dataclass(slots=True, frozen=True)
class MarketViewModel:
    """Aggregated market information for the market screen."""

    market_id: str
    name: str
    tam: int
    base_demand: float
    price_elasticity: float
    adoption: int


@dataclass(slots=True, frozen=True)
class EventLogEntry:
    """Represents a domain event shown in the event log."""

    tick: int
    name: str
    description: str


@dataclass(slots=True, frozen=True)
class AchievementViewModel:
    """Simplified projection of an unlocked achievement."""

    achievement_id: str
    name: str
    description: str
    unlocked_tick: int


@dataclass(slots=True, frozen=True)
class UiState:
    """Complete UI state object consumed by the Textual app."""

    dashboard: DashboardViewModel
    team: TeamViewModel
    research: ResearchViewModel
    products: tuple[ProductViewModel, ...]
    markets: tuple[MarketViewModel, ...]
    events: tuple[EventLogEntry, ...]
    achievements: tuple[AchievementViewModel, ...]
