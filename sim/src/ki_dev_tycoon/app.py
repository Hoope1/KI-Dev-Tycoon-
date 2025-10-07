"""Execution layer for deterministic simulation runs."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

from pydantic import BaseModel, Field

from ki_dev_tycoon.achievements import AchievementTracker, default_definitions
from ki_dev_tycoon.core import (
    AchievementUnlocked,
    EventBus,
    RandomSource,
    SimulationCompleted,
    SimulationStarted,
    TickClock,
    TickProcessed,
)
from ki_dev_tycoon.core.loop import TickLoop
from ki_dev_tycoon.core.state import GameState, ProductState, ResearchState, TeamState
from ki_dev_tycoon.core.time import TimeProvider
from ki_dev_tycoon.data import AssetBundle, load_assets
from ki_dev_tycoon.economy import project_adoption
from ki_dev_tycoon.products import compute_quality
from ki_dev_tycoon.research import progress_research
from ki_dev_tycoon.team import ensure_minimum_staff, train_team
from ki_dev_tycoon.utils.logging import get_logger

ClockFactory = Callable[[], TimeProvider]
RandomFactory = Callable[[int], RandomSource]
TickLoopFactory = Callable[[TimeProvider, RandomSource], TickLoop]


def _default_assets_root() -> Path:
    module_path = Path(__file__).resolve()
    search_bases = [module_path.parent] + list(module_path.parents)
    cwd = Path.cwd().resolve()
    search_bases.extend([cwd] + list(cwd.parents))
    seen: set[Path] = set()
    for base in search_bases:
        if base in seen:
            continue
        seen.add(base)
        candidate = base / "assets"
        if candidate.is_dir():
            return candidate
    msg = "Could not locate assets directory. Set SimulationConfig.asset_root explicitly."
    raise FileNotFoundError(msg)


@dataclass(slots=True)
class SimulationConfig:
    """Configuration container for deterministic simulation runs."""

    ticks: int
    seed: int
    daily_active_users: int
    arp_dau: float
    operating_costs: float
    asset_root: Path | None = None

    def resolve_asset_root(self) -> Path:
        """Return the directory containing balancing assets."""

        if self.asset_root is not None:
            return self.asset_root.expanduser().resolve()
        return _default_assets_root()


class SimulationResult(BaseModel):
    """Result payload exposed by the CLI layer."""

    final_tick: int = Field(description="Tick number after the simulation finished")
    cash: float = Field(description="Final company cash reserves in Euro")
    reputation: float = Field(description="Reputation score in range [0, 100]")
    history: list[dict[str, float]] | None = Field(
        default=None,
        description="Optional per-tick KPI history captured during the simulation.",
    )
    achievements: list[dict[str, str | int]] = Field(
        default_factory=list,
        description="Unlocked achievements at the end of the simulation.",
    )
    state: dict[str, Any] = Field(
        description="Final immutable game state snapshot as a dictionary."
    )


def _default_tick_loop(clock: TimeProvider, rng: RandomSource) -> TickLoop:
    """Instantiate the default tick loop for the simulation."""

    return TickLoop(clock=clock, rng=rng)


def _aggregate_research_bonuses(state: ResearchState, assets: AssetBundle) -> tuple[float, float, float]:
    quality_bonus = 0.0
    demand_bonus = 0.0
    training_bonus = 0.0
    for node_id in state.unlocked:
        node = assets.research.get(node_id)
        if node is None:
            continue
        unlocks = node.unlocks
        quality_bonus += unlocks.quality_bonus or 0.0
        demand_bonus += unlocks.demand_bonus or 0.0
        training_bonus += unlocks.training_bonus or 0.0
    return quality_bonus, demand_bonus, training_bonus


def _compute_research_points(team: TeamState) -> float:
    points = 0.0
    for member in team.members:
        if member.role_id == "data_scientist":
            points += member.skill * 2.0
        elif member.role_id == "engineer":
            points += member.skill * 0.75
        else:
            points += member.skill * 0.25
    return points


def _sample_event_effects(rng: RandomSource, assets: AssetBundle) -> dict[str, float]:
    weights = [(event, event.weight) for event in assets.events.values()]
    total_weight = sum(weight for _, weight in weights)
    if total_weight <= 0:
        return {}
    roll = rng.random() * total_weight
    accumulator = 0.0
    for event, weight in weights:
        accumulator += weight
        if roll <= accumulator:
            return dict(event.effects)
    return {}


def run_simulation(
    config: SimulationConfig,
    *,
    logger: Optional[logging.Logger] = None,
    event_bus: Optional[EventBus] = None,
    clock_factory: ClockFactory | None = None,
    rng_factory: RandomFactory | None = None,
    tick_loop_factory: TickLoopFactory | None = None,
    capture_history: bool = False,
) -> SimulationResult:
    """Execute the deterministic simulation using the configured providers."""

    if config.ticks <= 0:
        msg = "Simulation requires at least one tick"
        raise ValueError(msg)

    sim_logger = logger or get_logger("simulation")
    clock_provider = clock_factory or TickClock
    rng_provider = rng_factory or RandomSource
    loop_provider = tick_loop_factory or _default_tick_loop

    assets = load_assets(config.resolve_asset_root())
    clock = clock_provider()
    rng = rng_provider(config.seed)
    loop = loop_provider(clock, rng)

    if event_bus is not None:
        event_bus.publish(SimulationStarted(seed=config.seed))

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
    achievement_tracker = AchievementTracker(default_definitions())
    achievement_tracker.extend(state.achievements)

    sim_logger.info(
        "simulation.start", extra={"seed": config.seed, "ticks": config.ticks}
    )
    start_time = time.perf_counter()

    product_ids = tuple(product.product_id for product in state.products)

    history: list[dict[str, float]] = []

    def process_tick(_: int, tick_rng: RandomSource) -> None:
        nonlocal state
        state = state.advance_tick(clock)
        if sim_logger.isEnabledFor(logging.DEBUG):
            sim_logger.debug(
                "simulation.tick", extra={"tick": state.tick, "seed": config.seed}
            )
        if event_bus is not None:
            event_bus.publish(TickProcessed(tick=state.tick))

        hiring_rng = tick_rng.namespaced(f"hiring:{state.tick}")
        demand_rng = tick_rng.namespaced(f"demand:{state.tick}")
        reputation_rng = tick_rng.namespaced(f"reputation:{state.tick}")
        event_rng = tick_rng.namespaced(f"events:{state.tick}")

        hiring_result = ensure_minimum_staff(
            state.team,
            assets=assets,
            rng=hiring_rng,
            product_ids=product_ids,
        )
        state = state.update_team(hiring_result.team)

        quality_bonus, demand_bonus, training_bonus = _aggregate_research_bonuses(
            state.research, assets
        )

        training_result = train_team(
            state.team, assets=assets, training_bonus=training_bonus
        )
        state = state.update_team(training_result.team)

        research_points = _compute_research_points(state.team)
        research_result = progress_research(
            state.research, assets=assets, research_points=research_points
        )
        state = state.update_research(research_result.state)
        if research_result.completed:
            quality_bonus, demand_bonus, training_bonus = _aggregate_research_bonuses(
                state.research, assets
            )

        event_effects = _sample_event_effects(event_rng, assets)
        demand_multiplier = event_effects.get("demand_multiplier", 1.0)
        quality_penalty = event_effects.get("quality_penalty", 0.0)
        reputation_bonus = event_effects.get("reputation_bonus", 0.0)
        if reputation_bonus:
            state = state.apply_reputation_delta(reputation_bonus)

        total_revenue = 0.0
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

        salary_cost = sum(
            assets.roles[member.role_id].salary for member in state.team.members
        )
        cash_delta = total_revenue - salary_cost - config.operating_costs
        state = state.apply_cash_delta(cash_delta)

        direction = 1 if cash_delta >= 0 else -1
        jitter = (reputation_rng.random() - 0.5) * 0.2
        state = state.apply_reputation_delta(direction * 0.5 + jitter)

        unlocked = achievement_tracker.evaluate(state)
        if unlocked:
            state = state.add_achievements(unlocked)
            if event_bus is not None:
                for achievement in unlocked:
                    event_bus.publish(
                        AchievementUnlocked(tick=state.tick, achievement=achievement)
                    )

        if capture_history:
            total_adoption = sum(product.adoption for product in state.products)
            avg_quality = (
                sum(product.quality for product in state.products) / len(state.products)
                if state.products
                else 0.0
            )
            history.append(
                {
                    "tick": float(state.tick),
                    "cash": float(state.cash),
                    "reputation": float(state.reputation),
                    "revenue": float(total_revenue),
                    "adoption": float(total_adoption),
                    "avg_quality": float(avg_quality),
                }
            )

    processed_ticks = 0
    while processed_ticks < config.ticks:
        processed = loop.advance_by(loop.tick_duration, process_tick)
        if processed == 0:
            processed = loop.advance_by(loop.tick_duration, process_tick)
            if processed == 0:
                msg = "TickLoop failed to advance the simulation tick"
                raise RuntimeError(msg)
        processed_ticks += processed

    duration_ms = (time.perf_counter() - start_time) * 1000
    sim_logger.info(
        "simulation.complete",
        extra={
            "seed": config.seed,
            "tick": state.tick,
            "duration_ms": round(duration_ms, 2),
        },
    )

    if event_bus is not None:
        event_bus.publish(SimulationCompleted(tick=state.tick))

    return SimulationResult(
        final_tick=state.tick,
        cash=round(state.cash, 2),
        reputation=round(state.reputation, 2),
        history=history if capture_history else None,
        achievements=[achievement.to_dict() for achievement in achievement_tracker.unlocked()],
        state=state.to_dict(),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entrypoint used by the ``ki-sim`` script."""

    from ki_dev_tycoon.cli.sim import run_cli

    return run_cli(argv)


if __name__ == "__main__":  # pragma: no cover - manual execution guard
    raise SystemExit(main())
