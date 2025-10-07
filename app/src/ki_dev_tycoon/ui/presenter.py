"""Presenter layer bridging the simulation core with the Textual UI."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal, Sequence

import httpx

from ki_dev_tycoon.achievements import AchievementTracker, default_definitions
from ki_dev_tycoon.core.events import (
    AchievementUnlocked,
    EventBus,
    SimulationCompleted,
    SimulationStarted,
    TickProcessed,
)
from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.state import GameState, ProductState, ResearchState, TeamMember, TeamState
from ki_dev_tycoon.core.time import TickClock
from ki_dev_tycoon.data.loader import AssetBundle, load_assets
from ki_dev_tycoon.economy import project_adoption
from ki_dev_tycoon.platform import steam
from ki_dev_tycoon.products import compute_quality
from ki_dev_tycoon.research import progress_research
from ki_dev_tycoon.team import ensure_minimum_staff, train_team

from .viewmodels import (
    AchievementViewModel,
    DashboardViewModel,
    EventLogEntry,
    KpiSnapshot,
    MarketViewModel,
    ProductViewModel,
    ResearchNodeViewModel,
    ResearchViewModel,
    TeamMemberViewModel,
    TeamViewModel,
    UiState,
)


@dataclass(slots=True, frozen=True)
class SimulationPresenterConfig:
    """Configuration passed to :class:`SimulationPresenter`."""

    ticks: int = 30
    seed: int = 42
    daily_active_users: int = 5_000
    arp_dau: float = 0.12
    operating_costs: float = 450.0
    asset_root: Path | None = None
    api_url: str | None = None
    source: Literal["simulation", "api"] = "simulation"


class SimulationPresenter:
    """Aggregate simulation data for the Textual UI."""

    def __init__(self, config: SimulationPresenterConfig | None = None) -> None:
        self.config = config or SimulationPresenterConfig()
        self._event_bus = EventBus()
        self._event_bus.subscribe(TickProcessed, self._record_tick)
        self._event_bus.subscribe(AchievementUnlocked, self._on_achievement_unlocked)
        self._observed_ticks: list[int] = []
        self._achievement_tracker = AchievementTracker(default_definitions())
        self._recent_achievements: list[AchievementViewModel] = []

    @property
    def event_bus(self) -> EventBus:
        """Expose the underlying event bus for external subscribers."""

        return self._event_bus

    @property
    def latest_tick(self) -> int:
        """Return the highest tick observed while running the simulation."""

        return self._observed_ticks[-1] if self._observed_ticks else 0

    async def build_ui_state(self) -> UiState:
        """Return the :class:`UiState` according to the configured source."""

        if self.config.source == "api" and self.config.api_url:
            try:
                return await self._fetch_from_api(self.config.api_url)
            except httpx.HTTPError:
                # Fallback to local simulation if the API is unreachable.
                pass
        return await asyncio.to_thread(self._simulate_locally)

    def _simulate_locally(self) -> UiState:
        config = self.config
        assets = load_assets(self._resolve_asset_root(config.asset_root))
        clock = TickClock()
        rng = RandomSource(config.seed)
        self._achievement_tracker = AchievementTracker(default_definitions())
        self._recent_achievements.clear()
        self._event_bus.publish(SimulationStarted(seed=config.seed))

        products = tuple(
            ProductState(
                product_id=product.id,
                quality=product.base_quality,
                adoption=0,
                price=product.base_price,
            )
            for product in assets.products.values()
        )
        research_state = ResearchState(
            unlocked=frozenset(),
            active=None,
            progress=0.0,
            backlog=tuple(sorted(assets.research)),
        )
        state = GameState(
            tick=clock.current_tick(),
            cash=0.0,
            reputation=50.0,
            team=TeamState(members=()),
            products=products,
            research=research_state,
        )

        history: list[KpiSnapshot] = []
        events: list[EventLogEntry] = []

        for _ in range(config.ticks):
            clock.advance()
            state = state.advance_tick(clock)
            tick_rng = rng.namespaced(f"tick:{state.tick}")
            self._event_bus.publish(TickProcessed(tick=state.tick))

            state, hired = self._ensure_staffing(state, assets, tick_rng)
            quality_bonus, demand_bonus, training_bonus = self._aggregate_research_bonuses(
                state.research, assets
            )
            state = self._train_team(state, assets, training_bonus)
            state, completed_nodes = self._advance_research(state, assets)
            if completed_nodes:
                quality_bonus, demand_bonus, training_bonus = self._aggregate_research_bonuses(
                    state.research, assets
                )
            state, event_entry, demand_multiplier, quality_penalty, reputation_bonus = self._apply_event(
                state, assets, tick_rng
            )
            if event_entry is not None:
                events.append(event_entry)
            if reputation_bonus:
                state = state.apply_reputation_delta(reputation_bonus)

            state, revenue = self._update_products(
                state,
                assets,
                tick_rng,
                quality_bonus=quality_bonus,
                demand_bonus=demand_bonus,
                demand_multiplier=demand_multiplier,
                quality_penalty=quality_penalty,
            )

            salary_cost = sum(assets.roles[member.role_id].salary for member in state.team.members)
            cash_delta = revenue - salary_cost - config.operating_costs
            state = state.apply_cash_delta(cash_delta)

            direction = 1 if cash_delta >= 0 else -1
            jitter = (tick_rng.random() - 0.5) * 0.2
            state = state.apply_reputation_delta(direction * 0.5 + jitter)

            unlocked = self._achievement_tracker.evaluate(state)
            if unlocked:
                state = state.add_achievements(unlocked)
                for achievement in unlocked:
                    self._event_bus.publish(
                        AchievementUnlocked(tick=state.tick, achievement=achievement)
                    )

            total_adoption = sum(product.adoption for product in state.products)
            avg_quality = (
                sum(product.quality for product in state.products) / len(state.products)
                if state.products
                else 0.0
            )
            history.append(
                KpiSnapshot(
                    tick=state.tick,
                    cash=state.cash,
                    reputation=state.reputation,
                    revenue=revenue,
                    adoption=total_adoption,
                    avg_quality=avg_quality,
                    cash_delta=cash_delta,
                )
            )

            if completed_nodes:
                completion_text = ", ".join(completed_nodes)
                events.append(
                    EventLogEntry(
                        tick=state.tick,
                        name="Research breakthrough",
                        description=f"Unlocked: {completion_text}",
                    )
                )
            if hired:
                events.append(
                    EventLogEntry(
                        tick=state.tick,
                        name="New hires",
                        description=f"Added {len(hired)} team members",
                    )
                )

        self._event_bus.publish(SimulationCompleted(tick=state.tick))

        dashboard = self._build_dashboard(history)
        team = self._build_team_view(state.team, assets)
        research = self._build_research_view(state.research, assets)
        products_vm = self._build_product_view(state.products, assets)
        markets = self._build_market_view(state.products, assets)
        achievement_models = tuple(
            AchievementViewModel(
                achievement_id=achievement.id,
                name=achievement.name,
                description=achievement.description,
                unlocked_tick=achievement.unlocked_tick,
            )
            for achievement in state.achievements
        )

        return UiState(
            dashboard=dashboard,
            team=team,
            research=research,
            products=products_vm,
            markets=markets,
            events=tuple(events[-40:]),
            achievements=achievement_models,
        )

    async def _fetch_from_api(self, base_url: str) -> UiState:
        async with httpx.AsyncClient(base_url=base_url, timeout=5.0) as client:
            response = await client.get("/state")
            response.raise_for_status()
            payload = response.json()

        config = self.config
        assets = load_assets(self._resolve_asset_root(config.asset_root))

        average_quality = (
            sum(float(project["quality"]) for project in payload["projects"])
            / max(1, len(payload["projects"]))
        )
        history = (
            KpiSnapshot(
                tick=int(payload["tick"]),
                cash=float(payload["cash"]),
                reputation=float(payload["reputation"]),
                revenue=config.daily_active_users * config.arp_dau,
                adoption=sum(int(project["quality"] * 1_000) for project in payload["projects"]),
                avg_quality=average_quality,
                cash_delta=0.0,
            ),
        )
        dashboard = self._build_dashboard(list(history))
        team = TeamViewModel(members=())
        research = self._build_research_view(
            ResearchState(
                unlocked=frozenset(),
                active=None,
                progress=0.0,
                backlog=tuple(sorted(assets.research)),
            ),
            assets,
        )
        products_vm = self._build_product_view(tuple(), assets)
        markets = self._build_market_view(tuple(), assets)
        achievement_models = tuple(
            AchievementViewModel(
                achievement_id=str(entry["id"]),
                name=str(entry["name"]),
                description=str(entry.get("description", "")),
                unlocked_tick=int(entry["unlocked_tick"]),
            )
            for entry in payload.get("achievements", [])
        )
        return UiState(
            dashboard=dashboard,
            team=team,
            research=research,
            products=products_vm,
            markets=markets,
            events=(
                EventLogEntry(
                    tick=int(payload["tick"]),
                    name="API Snapshot",
                    description="State retrieved from FastAPI backend",
                ),
            ),
            achievements=achievement_models,
        )

    def _build_dashboard(self, history: Sequence[KpiSnapshot]) -> DashboardViewModel:
        latest = history[-1]
        burn_rate = max(0.0, -latest.cash_delta)
        return DashboardViewModel(
            current_tick=latest.tick,
            cash=latest.cash,
            reputation=latest.reputation,
            burn_rate=burn_rate,
            daily_revenue=latest.revenue,
            adoption=latest.adoption,
            avg_quality=latest.avg_quality,
            history=tuple(history),
        )

    def _build_team_view(self, team: TeamState, assets: AssetBundle) -> TeamViewModel:
        members = tuple(
            TeamMemberViewModel(
                role_id=member.role_id,
                role_name=assets.roles[member.role_id].name,
                skill=member.skill,
                training_progress=member.training_progress,
                salary=assets.roles[member.role_id].salary,
            )
            for member in team.members
        )
        return TeamViewModel(members=members)

    def _build_research_view(self, research: ResearchState, assets: AssetBundle) -> ResearchViewModel:
        nodes = []
        unlocked = set(research.unlocked)
        backlog = set(research.backlog)
        for node in sorted(assets.research.values(), key=lambda item: item.cost):
            nodes.append(
                ResearchNodeViewModel(
                    node_id=node.id,
                    name=node.name,
                    cost=node.cost,
                    unlocked=node.id in unlocked,
                    in_backlog=node.id in backlog,
                )
            )
        return ResearchViewModel(
            active=research.active,
            progress=research.progress,
            unlocked=tuple(sorted(research.unlocked)),
            backlog=tuple(research.backlog),
            nodes=tuple(nodes),
        )

    def _build_product_view(
        self, products: Iterable[ProductState], assets: AssetBundle
    ) -> tuple[ProductViewModel, ...]:
        view_models = []
        for product in products:
            config = assets.products.get(product.product_id)
            if config is None:
                continue
            view_models.append(
                ProductViewModel(
                    product_id=product.product_id,
                    name=config.name,
                    market=assets.markets[config.target_market].name,
                    price=product.price,
                    quality=product.quality,
                    adoption=product.adoption,
                )
            )
        return tuple(view_models)

    def _build_market_view(
        self, products: Iterable[ProductState], assets: AssetBundle
    ) -> tuple[MarketViewModel, ...]:
        adoption_by_market: dict[str, int] = {market_id: 0 for market_id in assets.markets}
        for product in products:
            config = assets.products.get(product.product_id)
            if config is None:
                continue
            adoption_by_market[config.target_market] += product.adoption
        markets = []
        for market_id, market in sorted(assets.markets.items()):
            markets.append(
                MarketViewModel(
                    market_id=market_id,
                    name=market.name,
                    tam=market.tam,
                    base_demand=market.base_demand,
                    price_elasticity=market.price_elasticity,
                    adoption=adoption_by_market.get(market_id, 0),
                )
            )
        return tuple(markets)

    def _ensure_staffing(
        self, state: GameState, assets: AssetBundle, tick_rng: RandomSource
    ) -> tuple[GameState, tuple[TeamMember, ...]]:
        product_ids = tuple(product.product_id for product in state.products)
        hiring_result = ensure_minimum_staff(
            state.team,
            assets=assets,
            rng=tick_rng.namespaced(f"hiring:{state.tick}"),
            product_ids=product_ids,
        )
        state = state.update_team(hiring_result.team)
        return state, hiring_result.hired

    def _train_team(
        self, state: GameState, assets: AssetBundle, training_bonus: float
    ) -> GameState:
        training_result = train_team(
            state.team,
            assets=assets,
            training_bonus=training_bonus,
        )
        return state.update_team(training_result.team)

    def _advance_research(
        self, state: GameState, assets: AssetBundle
    ) -> tuple[GameState, tuple[str, ...]]:
        research_points = self._compute_research_points(state.team)
        progress_result = progress_research(
            state.research,
            assets=assets,
            research_points=research_points,
        )
        state = state.update_research(progress_result.state)
        return state, progress_result.completed

    def _aggregate_research_bonuses(
        self, research: ResearchState, assets: AssetBundle
    ) -> tuple[float, float, float]:
        quality_bonus = 0.0
        demand_bonus = 0.0
        training_bonus = 0.0
        for node_id in research.unlocked:
            node = assets.research.get(node_id)
            if node is None:
                continue
            unlocks = node.unlocks
            quality_bonus += unlocks.quality_bonus or 0.0
            demand_bonus += unlocks.demand_bonus or 0.0
            training_bonus += unlocks.training_bonus or 0.0
        return quality_bonus, demand_bonus, training_bonus

    def _apply_event(
        self,
        state: GameState,
        assets: AssetBundle,
        tick_rng: RandomSource,
    ) -> tuple[GameState, EventLogEntry | None, float, float, float]:
        events = sorted(assets.events.values(), key=lambda event: event.id)
        total_weight = sum(event.weight for event in events)
        if total_weight <= 0:
            return state, None, 1.0, 0.0, 0.0
        roll = tick_rng.namespaced(f"events:{state.tick}").random() * total_weight
        accumulator = 0.0
        selected = None
        for event in events:
            accumulator += event.weight
            if roll <= accumulator:
                selected = event
                break
        if selected is None:
            return state, None, 1.0, 0.0, 0.0
        demand_multiplier = selected.effects.get("demand_multiplier", 1.0)
        quality_penalty = selected.effects.get("quality_penalty", 0.0)
        reputation_bonus = selected.effects.get("reputation_bonus", 0.0)
        effect_parts: list[str] = []
        if demand_multiplier != 1.0:
            effect_parts.append(f"Demand x{demand_multiplier:.2f}")
        if quality_penalty:
            effect_parts.append(f"Quality -{quality_penalty:.2f}")
        if reputation_bonus:
            effect_parts.append(f"Reputation +{reputation_bonus:.1f}")
        description = ", ".join(effect_parts) if effect_parts else "No immediate effects"
        entry = EventLogEntry(
            tick=state.tick,
            name=selected.name,
            description=description,
        )
        return state, entry, demand_multiplier, quality_penalty, reputation_bonus

    def _update_products(
        self,
        state: GameState,
        assets: AssetBundle,
        tick_rng: RandomSource,
        *,
        quality_bonus: float,
        demand_bonus: float,
        demand_multiplier: float,
        quality_penalty: float,
    ) -> tuple[GameState, float]:
        total_revenue = 0.0
        demand_rng = tick_rng.namespaced(f"demand:{state.tick}")
        for product in state.products:
            quality = compute_quality(
                state,
                product=product,
                assets=assets,
                research_quality_bonus=quality_bonus,
            )
            if quality_penalty:
                quality = max(0.0, quality - quality_penalty)
            updated_product = product.update_quality(quality)
            adoption = project_adoption(
                state,
                product=updated_product,
                assets=assets,
                rng=demand_rng.namespaced(f"{product.product_id}:{state.tick}"),
                demand_bonus=demand_bonus,
                demand_multiplier=demand_multiplier,
            )
            updated_product = updated_product.update_adoption(adoption)
            state = state.update_product(product.product_id, updated_product)
            total_revenue += updated_product.adoption * updated_product.price
        return state, total_revenue

    def _compute_research_points(self, team: TeamState) -> float:
        points = 0.0
        for member in team.members:
            if member.role_id == "data_scientist":
                points += member.skill * 2.0
            elif member.role_id == "engineer":
                points += member.skill * 0.75
            else:
                points += member.skill * 0.25
        return points

    def _record_tick(self, event: TickProcessed) -> None:
        self._observed_ticks.append(event.tick)

    def _on_achievement_unlocked(self, event: AchievementUnlocked) -> None:
        view_model = AchievementViewModel(
            achievement_id=event.achievement.id,
            name=event.achievement.name,
            description=event.achievement.description,
            unlocked_tick=event.achievement.unlocked_tick,
        )
        self._recent_achievements.append(view_model)
        steam.unlock_achievement(event.achievement.id)

    def _resolve_asset_root(self, configured: Path | None) -> Path:
        if configured is not None:
            return configured.expanduser().resolve()
        search_root = Path(__file__).resolve()
        for base in [search_root, *search_root.parents]:
            candidate = base / "assets"
            if candidate.is_dir():
                return candidate
        raise FileNotFoundError("Could not locate assets directory for UI presenter")


__all__ = ["SimulationPresenter", "SimulationPresenterConfig"]
