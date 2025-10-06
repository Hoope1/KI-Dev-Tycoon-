"""Pydantic schemas describing simulation configuration files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

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
        description="Economic parameters controlling cashflow computations.",
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
