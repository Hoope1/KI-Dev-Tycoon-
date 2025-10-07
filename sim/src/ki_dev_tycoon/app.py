"""Execution layer for deterministic simulation runs."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable, Optional, Sequence

from pydantic import BaseModel, Field

from ki_dev_tycoon.core import (
    EventBus,
    RandomSource,
    SimulationCompleted,
    SimulationStarted,
    TickClock,
    TickProcessed,
)
from ki_dev_tycoon.core.loop import TickLoop
from ki_dev_tycoon.core.time import TimeProvider
from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.economy import CashflowParameters, compute_daily_cash_delta
from ki_dev_tycoon.utils.logging import get_logger

ClockFactory = Callable[[], TimeProvider]
RandomFactory = Callable[[int], RandomSource]
TickLoopFactory = Callable[[TimeProvider, RandomSource], TickLoop]


@dataclass(slots=True)
class SimulationConfig:
    """Configuration container for deterministic simulation runs."""

    ticks: int
    seed: int
    daily_active_users: int
    arp_dau: float
    operating_costs: float

    def to_cashflow(self) -> CashflowParameters:
        """Return the immutable cashflow parameters."""

        return CashflowParameters(
            daily_active_users=self.daily_active_users,
            arp_dau=self.arp_dau,
            operating_costs=self.operating_costs,
        )


class SimulationResult(BaseModel):
    """Result payload exposed by the CLI layer."""

    final_tick: int = Field(description="Tick number after the simulation finished")
    cash: float = Field(description="Final company cash reserves in Euro")
    reputation: float = Field(description="Reputation score in range [0, 100]")


def _default_tick_loop(clock: TimeProvider, rng: RandomSource) -> TickLoop:
    """Instantiate the default tick loop for the simulation."""

    return TickLoop(clock=clock, rng=rng)


def run_simulation(
    config: SimulationConfig,
    *,
    logger: Optional[logging.Logger] = None,
    event_bus: Optional[EventBus] = None,
    clock_factory: ClockFactory | None = None,
    rng_factory: RandomFactory | None = None,
    tick_loop_factory: TickLoopFactory | None = None,
) -> SimulationResult:
    """Execute the deterministic simulation using the configured providers."""

    if config.ticks <= 0:
        msg = "Simulation requires at least one tick"
        raise ValueError(msg)

    sim_logger = logger or get_logger("simulation")
    clock_provider = clock_factory or TickClock
    rng_provider = rng_factory or RandomSource
    loop_provider = tick_loop_factory or _default_tick_loop

    clock = clock_provider()
    rng = rng_provider(config.seed)
    loop = loop_provider(clock, rng)

    if event_bus is not None:
        event_bus.publish(SimulationStarted(seed=config.seed))

    state = GameState(tick=clock.current_tick(), cash=0.0, reputation=50.0)
    parameters = config.to_cashflow()

    sim_logger.info(
        "simulation.start", extra={"seed": config.seed, "ticks": config.ticks}
    )
    start_time = time.perf_counter()

    def process_tick(_: int, tick_rng: RandomSource) -> None:
        nonlocal state
        state = state.advance_tick(clock)
        if sim_logger.isEnabledFor(logging.DEBUG):
            sim_logger.debug(
                "simulation.tick", extra={"tick": state.tick, "seed": config.seed}
            )
        if event_bus is not None:
            event_bus.publish(TickProcessed(tick=state.tick))

        cash_delta = compute_daily_cash_delta(parameters)
        state = state.apply_cash_delta(cash_delta)

        direction = 1 if cash_delta >= 0 else -1
        jitter = (tick_rng.random() - 0.5) * 0.2
        state = state.apply_reputation_delta(direction * 0.5 + jitter)

    processed_ticks = 0
    while processed_ticks < config.ticks:
        processed = loop.advance_by(loop.tick_duration, process_tick)
        if processed == 0:
            processed = loop.advance_by(loop.tick_duration, process_tick)
            if processed == 0:
                msg = 'TickLoop failed to advance the simulation tick'
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
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entrypoint used by the ``ki-sim`` script."""

    from ki_dev_tycoon.cli.sim import run_cli

    return run_cli(argv)


if __name__ == "__main__":  # pragma: no cover - manual execution guard
    raise SystemExit(main())
