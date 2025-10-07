"""Pydantic schemas describing configuration and asset files."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

if TYPE_CHECKING:  # pragma: no cover - import guarded for type checking only
    from ki_dev_tycoon.app import SimulationConfig


class EconomyConfig(BaseModel):
    """Economic parameters for a simulation profile."""

    model_config = ConfigDict(extra="forbid")

    daily_active_users: int = Field(
        ge=0,
        description="Projected daily active users in the simulated company.",
    )
    arp_dau: float = Field(
        ge=0.0,
        description="Average revenue per daily active user in Euro.",
    )
    operating_costs: float = Field(
        ge=0.0,
        description="Daily operating costs in Euro.",
    )


class SimulationProfile(BaseModel):
    """Top-level schema for simulation configuration files."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Unique identifier for the profile.")
    description: str | None = Field(
        default=None, description="Optional human readable description."
    )
    ticks: int = Field(gt=0, description="Number of ticks the simulation should run.")
    seed: int = Field(
        description="Deterministic random seed used to initialise the RNG.",
    )
    economy: EconomyConfig = Field(
        description="Economic parameters controlling cashflow computations."
    )

    def to_simulation_config(self) -> SimulationConfig:
        """Convert the profile into :class:`~ki_dev_tycoon.app.SimulationConfig`."""

        from ki_dev_tycoon.app import SimulationConfig

        return SimulationConfig(
            ticks=self.ticks,
            seed=self.seed,
            daily_active_users=self.economy.daily_active_users,
            arp_dau=self.economy.arp_dau,
            operating_costs=self.economy.operating_costs,
        )


class RoleConfig(BaseModel):
    """Balance definition for a single team role."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Unique machine readable identifier")
    name: str = Field(description="Human readable display name")
    salary: float = Field(ge=0.0, description="Daily salary cost in Euro")
    hiring_difficulty: float = Field(
        ge=0.0,
        le=1.0,
        description="Probability in [0,1] that a hire attempt fails due to scarcity.",
    )
    training_rate: float = Field(
        gt=0.0, le=0.5, description="Skill growth per tick while training in [0, 0.5]"
    )
    productivity: float = Field(
        ge=0.0,
        le=1.0,
        description="Contribution of this role towards product quality in [0,1].",
    )


class RoleCatalogue(RootModel[tuple[RoleConfig, ...]]):
    """Root collection holding unique :class:`RoleConfig` entries."""

    root: tuple[RoleConfig, ...]

    @field_validator("root")
    @classmethod
    def _ensure_unique_ids(cls, value: tuple[RoleConfig, ...]) -> tuple[RoleConfig, ...]:
        seen: set[str] = set()
        for role in value:
            if role.id in seen:
                msg = f"Duplicate role id detected: {role.id}"
                raise ValueError(msg)
            seen.add(role.id)
        return value

    def as_dict(self) -> Dict[str, RoleConfig]:
        """Return a mapping keyed by role identifier."""

        return {role.id: role for role in self.root}


class ProductConfig(BaseModel):
    """Definition of a buildable product."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Product identifier")
    name: str = Field(description="Display name of the product")
    target_market: str = Field(description="Market id this product sells into")
    base_quality: float = Field(
        ge=0.0, le=1.0, description="Base quality before team and research modifiers"
    )
    base_price: float = Field(ge=0.0, description="List price per user per tick")
    required_roles: Dict[str, int] = Field(
        default_factory=dict,
        description="Mapping of role id to minimum staffing level",
    )

    @field_validator("required_roles")
    @classmethod
    def _validate_requirements(cls, value: Dict[str, int]) -> Dict[str, int]:
        for role_id, count in value.items():
            if count <= 0:
                msg = f"Role requirement for {role_id} must be positive"
                raise ValueError(msg)
        return value


class ProductCatalogue(RootModel[tuple[ProductConfig, ...]]):
    """Root collection of products."""

    root: tuple[ProductConfig, ...]

    @field_validator("root")
    @classmethod
    def _ensure_unique_ids(cls, value: tuple[ProductConfig, ...]) -> tuple[ProductConfig, ...]:
        seen: set[str] = set()
        for product in value:
            if product.id in seen:
                msg = f"Duplicate product id detected: {product.id}"
                raise ValueError(msg)
            seen.add(product.id)
        return value

    def as_dict(self) -> Dict[str, ProductConfig]:
        """Return a mapping keyed by product identifier."""

        return {product.id: product for product in self.root}


class MarketConfig(BaseModel):
    """Definition of a market segment with a total addressable market."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Market identifier")
    name: str = Field(description="Display name")
    tam: int = Field(gt=0, description="Total addressable market size in customers")
    base_demand: float = Field(
        ge=0.0,
        le=1.0,
        description="Baseline conversion rate per tick expressed as [0,1]",
    )
    price_elasticity: float = Field(
        ge=0.0,
        le=5.0,
        description="Price sensitivity multiplier (higher means more sensitive)",
    )


class MarketCatalogue(RootModel[tuple[MarketConfig, ...]]):
    """Root model describing available markets."""

    root: tuple[MarketConfig, ...]

    @field_validator("root")
    @classmethod
    def _ensure_unique_ids(cls, value: tuple[MarketConfig, ...]) -> tuple[MarketConfig, ...]:
        seen: set[str] = set()
        for market in value:
            if market.id in seen:
                msg = f"Duplicate market id detected: {market.id}"
                raise ValueError(msg)
            seen.add(market.id)
        return value

    def as_dict(self) -> Dict[str, MarketConfig]:
        """Return a mapping keyed by market identifier."""

        return {market.id: market for market in self.root}


class ResearchUnlocks(BaseModel):
    """Modifiers applied when a research node completes."""

    model_config = ConfigDict(extra="forbid")

    quality_bonus: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Additive quality bonus applied multiplicatively.",
    )
    demand_bonus: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Additional demand share in [0,1].",
    )
    training_bonus: float | None = Field(
        default=None,
        ge=0.0,
        le=0.5,
        description="Additional training progress per tick.",
    )


class ResearchNode(BaseModel):
    """Definition of a technology node within the research tree."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Research identifier")
    name: str = Field(description="Human readable name")
    cost: int = Field(gt=0, description="Research points required to complete")
    unlocks: ResearchUnlocks
    prerequisites: tuple[str, ...] = Field(default_factory=tuple)


class ResearchCatalogue(RootModel[tuple[ResearchNode, ...]]):
    """Root collection for technology tree nodes."""

    root: tuple[ResearchNode, ...]

    @field_validator("root")
    @classmethod
    def _ensure_unique_ids(cls, value: tuple[ResearchNode, ...]) -> tuple[ResearchNode, ...]:
        seen: set[str] = set()
        for node in value:
            if node.id in seen:
                msg = f"Duplicate research id detected: {node.id}"
                raise ValueError(msg)
            seen.add(node.id)
        return value

    def as_dict(self) -> Dict[str, ResearchNode]:
        """Return a mapping keyed by research identifier."""

        return {node.id: node for node in self.root}


class EventConfig(BaseModel):
    """Definition for a random event that can occur during the simulation."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Event identifier")
    name: str = Field(description="Display name")
    weight: float = Field(gt=0.0, description="Relative frequency weight")
    effects: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapping of effect keys to numeric payloads",
    )


class EventCatalogue(RootModel[tuple[EventConfig, ...]]):
    """Root collection for event definitions."""

    root: tuple[EventConfig, ...]

    @field_validator("root")
    @classmethod
    def _ensure_unique_ids(cls, value: tuple[EventConfig, ...]) -> tuple[EventConfig, ...]:
        seen: set[str] = set()
        for event in value:
            if event.id in seen:
                msg = f"Duplicate event id detected: {event.id}"
                raise ValueError(msg)
            seen.add(event.id)
        return value

    def as_dict(self) -> Dict[str, EventConfig]:
        """Return a mapping keyed by event identifier."""

        return {event.id: event for event in self.root}
