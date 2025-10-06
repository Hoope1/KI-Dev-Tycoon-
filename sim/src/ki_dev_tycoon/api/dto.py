"""Data transfer objects used by the FastAPI adapter."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectPreviewDTO(BaseModel):
    """Minimal representation of a simulated project for UI previews."""

    model_config = ConfigDict(frozen=True)

    project_id: str = Field(..., description="Stable identifier of the project instance.")
    name: str = Field(..., description="Display name exposed to the client UI.")
    project_type: Literal["chatbot", "tooling"] = Field(
        ..., description="High-level category of the simulated project."
    )
    stage: Literal["planning", "training", "released"] = Field(
        ..., description="Simplified project lifecycle stage."
    )
    quality: float = Field(..., ge=0.0, le=1.0, description="Quality score in [0, 1].")


class SimulationStateDTO(BaseModel):
    """Static snapshot returned by the `/state` endpoint."""

    model_config = ConfigDict(frozen=True)

    tick: int = Field(..., ge=0, description="Current simulation tick.")
    in_game_day: int = Field(..., ge=0, description="Calendar day derived from the tick count.")
    reputation: float = Field(..., ge=0.0, le=100.0, description="Public reputation of the studio.")
    cash: float = Field(..., description="Liquid cash balance in game currency.")
    projects: list[ProjectPreviewDTO] = Field(
        default_factory=list,
        description="Subset of projects visible on the dashboard.",
    )
