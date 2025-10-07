"""FastAPI application that exposes live simulation data."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from threading import Lock
from typing import Iterable, Literal

from fastapi import Depends, FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field

from ki_dev_tycoon import __version__
from ki_dev_tycoon.api.dto import AchievementDTO, ProjectPreviewDTO, SimulationStateDTO
from ki_dev_tycoon.app import SimulationConfig, SimulationResult, run_simulation
from ki_dev_tycoon.core.state import GameState, ProductState
from ki_dev_tycoon.data import load_assets
from ki_dev_tycoon.persistence.savegame import load_game


def _default_simulation_config() -> SimulationConfig:
    return SimulationConfig(
        ticks=30,
        seed=42,
        daily_active_users=5_000,
        arp_dau=0.15,
        operating_costs=750.0,
    )


class SimulationRequest(BaseModel):
    """Payload used to trigger a new simulation run."""

    ticks: int | None = Field(None, ge=1)
    seed: int | None = Field(None, ge=0)
    daily_active_users: int | None = Field(None, ge=0)
    arp_dau: float | None = Field(None, ge=0.0)
    operating_costs: float | None = Field(None, ge=0.0)
    save_path: Path | None = Field(
        None,
        description="Optional path to a savegame that should be loaded instead of running a simulation.",
    )

    def apply(self, base: SimulationConfig) -> SimulationConfig:
        """Return a :class:`SimulationConfig` derived from ``base`` and the overrides."""

        return replace(
            base,
            ticks=self.ticks if self.ticks is not None else base.ticks,
            seed=self.seed if self.seed is not None else base.seed,
            daily_active_users=(
                self.daily_active_users
                if self.daily_active_users is not None
                else base.daily_active_users
            ),
            arp_dau=self.arp_dau if self.arp_dau is not None else base.arp_dau,
            operating_costs=(
                self.operating_costs
                if self.operating_costs is not None
                else base.operating_costs
            ),
        )


class SimulationRepository:
    """Provides the latest simulation snapshot for the API layer."""

    def __init__(
        self,
        config: SimulationConfig,
        *,
        save_path: Path | None = None,
    ) -> None:
        self._lock = Lock()
        self._save_path = save_path.expanduser().resolve() if save_path else None
        self._asset_root = (
            config.asset_root.expanduser().resolve()
            if config.asset_root is not None
            else config.resolve_asset_root()
        )
        self._assets = load_assets(self._asset_root)
        self._config = replace(config, asset_root=self._asset_root)
        self._state: GameState | None = None
        self._result: SimulationResult | None = None
        self.refresh()

    _UNSET = object()

    def refresh(
        self,
        *,
        config_override: SimulationConfig | None = None,
        save_path: Path | None | object = _UNSET,
    ) -> None:
        """Recompute the simulation snapshot."""

        with self._lock:
            if save_path is not self._UNSET:
                if save_path is None:
                    self._save_path = None
                else:
                    self._save_path = save_path.expanduser().resolve()
            if config_override is not None:
                asset_root = (
                    config_override.asset_root.expanduser().resolve()
                    if config_override.asset_root is not None
                    else config_override.resolve_asset_root()
                )
                self._asset_root = asset_root
                self._assets = load_assets(asset_root)
                self._config = replace(config_override, asset_root=asset_root)
            if self._save_path is not None and self._save_path.exists():
                self._state = load_game(self._save_path)
                self._result = None
                return
            result = run_simulation(self._config, capture_history=True)
            self._state = GameState.from_dict(result.state)
            self._result = result

    def get_state(self) -> GameState:
        with self._lock:
            if self._state is None:
                self.refresh()
            assert self._state is not None  # defensive guard
            return self._state

    @property
    def config(self) -> SimulationConfig:
        with self._lock:
            return self._config

    @property
    def save_path(self) -> Path | None:
        with self._lock:
            return self._save_path

    def history(self) -> list[dict[str, float]]:
        with self._lock:
            if self._result and self._result.history:
                return list(self._result.history)
            return []

    def achievements(self) -> Iterable[AchievementDTO]:
        state = self.get_state()
        return (
            AchievementDTO(
                id=achievement.id,
                name=achievement.name,
                description=achievement.description,
                unlocked_tick=achievement.unlocked_tick,
            )
            for achievement in state.achievements
        )

    def build_state_dto(self) -> SimulationStateDTO:
        state = self.get_state()
        projects = [self._project_preview(product) for product in state.products]
        return SimulationStateDTO(
            tick=state.tick,
            in_game_day=state.tick // 10,
            reputation=state.reputation,
            cash=state.cash,
            projects=projects,
            achievements=list(self.achievements()),
        )

    def _project_preview(self, product: ProductState) -> ProjectPreviewDTO:
        config = self._assets.products.get(product.product_id)
        name = config.name if config is not None else product.product_id.replace("_", " ").title()
        project_type = self._classify_product(config)
        stage = self._infer_stage(product)
        return ProjectPreviewDTO(
            project_id=product.product_id,
            name=name,
            project_type=project_type,
            stage=stage,
            quality=product.quality,
        )

    @staticmethod
    def _classify_product(config: object | None) -> Literal["chatbot", "tooling"]:
        if config is None:
            return "tooling"
        identifier = getattr(config, "id", "")
        name = getattr(config, "name", "")
        if "bot" in identifier or "bot" in str(name).lower():
            return "chatbot"
        return "tooling"

    @staticmethod
    def _infer_stage(product: ProductState) -> Literal["planning", "training", "released"]:
        if product.adoption > 0:
            return "released"
        if product.quality >= 0.5:
            return "training"
        return "planning"


def _environment_save_path() -> Path | None:
    raw = os.getenv("KI_DEV_TYCOON_SAVE")
    if not raw:
        return None
    return Path(raw)


def create_app(
    config: SimulationConfig | None = None,
    *,
    save_path: Path | None = None,
) -> FastAPI:
    """Construct the FastAPI application instance."""

    repository = SimulationRepository(
        config or _default_simulation_config(),
        save_path=save_path or _environment_save_path(),
    )

    app = FastAPI(
        title="KI Dev Tycoon API",
        version=__version__,
        description="Read-only adapter that exposes simulation state to the client prototype.",
    )
    app.state.repository = repository

    def get_repository(request: Request) -> SimulationRepository:
        return request.app.state.repository

    @app.get("/state", response_model=SimulationStateDTO, tags=["State"])
    async def read_state(
        repo: SimulationRepository = Depends(get_repository),
    ) -> SimulationStateDTO:
        return repo.build_state_dto()

    @app.get("/state/raw", tags=["State"])
    async def read_raw_state(
        repo: SimulationRepository = Depends(get_repository),
    ) -> dict[str, float | int | list | dict]:
        return repo.get_state().to_dict()

    @app.get("/achievements", response_model=list[AchievementDTO], tags=["State"])
    async def read_achievements(
        repo: SimulationRepository = Depends(get_repository),
    ) -> list[AchievementDTO]:
        return list(repo.achievements())

    @app.get("/history", tags=["State"])
    async def read_history(
        repo: SimulationRepository = Depends(get_repository),
    ) -> list[dict[str, float]]:
        return repo.history()

    @app.post("/simulate", response_model=SimulationStateDTO, tags=["State"])
    async def rerun_simulation(
        payload: SimulationRequest,
        repo: SimulationRepository = Depends(get_repository),
    ) -> SimulationStateDTO:
        save_override: Path | None
        if "save_path" in payload.model_fields_set:
            if payload.save_path is not None and not payload.save_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Savegame {payload.save_path} does not exist",
                )
            save_override = payload.save_path
        else:
            save_override = SimulationRepository._UNSET
        new_config = payload.apply(repo.config)
        repo.refresh(config_override=new_config, save_path=save_override)
        return repo.build_state_dto()

    return app


app = create_app()
