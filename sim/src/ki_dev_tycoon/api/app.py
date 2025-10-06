"""FastAPI application that exposes a minimal `/state` endpoint."""

from __future__ import annotations

from fastapi import FastAPI

from ki_dev_tycoon import __version__
from ki_dev_tycoon.api.dto import ProjectPreviewDTO, SimulationStateDTO

_DUMMY_STATE = SimulationStateDTO(
    tick=120,
    in_game_day=12,
    reputation=72.5,
    cash=250_000.0,
    projects=[
        ProjectPreviewDTO(
            project_id="proj-aurora",
            name="Aurora QA",
            project_type="tooling",
            stage="training",
            quality=0.62,
        ),
        ProjectPreviewDTO(
            project_id="proj-helix",
            name="Project Helix",
            project_type="chatbot",
            stage="planning",
            quality=0.15,
        ),
    ],
)


def create_app() -> FastAPI:
    """Construct the FastAPI application instance."""

    app = FastAPI(
        title="KI Dev Tycoon API",
        version=__version__,
        description="Read-only adapter that exposes simulation state to the client prototype.",
    )

    @app.get("/state", response_model=SimulationStateDTO, tags=["State"])
    async def read_state() -> SimulationStateDTO:
        """Return a deterministic dummy state for the client mock."""

        return _DUMMY_STATE

    return app


app = create_app()
