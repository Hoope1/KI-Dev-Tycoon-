"""CLI entrypoints for running deterministic simulations."""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel, Field

from ki_dev_tycoon.core import (
    EventBus,
    RandomSource,
    SimulationCompleted,
    SimulationStarted,
    TickClock,
    TickProcessed,
)
from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.economy import CashflowParameters, compute_daily_cash_delta
from ki_dev_tycoon.utils.logging import configure_logging, get_logger


@dataclass(slots=True)
class SimulationConfig:
    ticks: int
    seed: int
    daily_active_users: int
    arp_dau: float
    operating_costs: float

    def to_cashflow(self) -> CashflowParameters:
        return CashflowParameters(
            daily_active_users=self.daily_active_users,
            arp_dau=self.arp_dau,
            operating_costs=self.operating_costs,
        )


class SimulationResult(BaseModel):
    final_tick: int = Field(description="Tick number after the simulation finished")
    cash: float = Field(description="Final company cash reserves in Euro")
    reputation: float = Field(description="Reputation score in range [0, 100]")


def run_simulation(
    config: SimulationConfig,
    logger: Optional[logging.Logger] = None,
    event_bus: Optional[EventBus] = None,
) -> SimulationResult:
    if config.ticks <= 0:
        msg = "Simulation requires at least one tick"
        raise ValueError(msg)

    sim_logger = logger or get_logger("simulation")
    if event_bus is not None:
        event_bus.publish(SimulationStarted(seed=config.seed))
    rng = RandomSource(seed=config.seed)
    clock = TickClock()
    state = GameState(tick=0, cash=0.0, reputation=50.0)
    parameters = config.to_cashflow()
    sim_logger.info(
        "simulation.start", extra={"seed": config.seed, "ticks": config.ticks}
    )
    start_time = time.perf_counter()

    for _ in range(config.ticks):
        clock.advance()
        state = state.advance_tick(clock)
        if sim_logger.isEnabledFor(logging.DEBUG):
            sim_logger.debug(
                "simulation.tick", extra={"tick": state.tick, "seed": config.seed}
            )
        if event_bus is not None:
            event_bus.publish(TickProcessed(tick=state.tick))
        cash_delta = compute_daily_cash_delta(parameters)
        state = state.apply_cash_delta(cash_delta)

        # Reputation drifts slowly towards success or failure using deterministic jitter.
        direction = 1 if cash_delta >= 0 else -1
        jitter = (rng.random() - 0.5) * 0.2
        state = state.apply_reputation_delta(direction * 0.5 + jitter)

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ki-sim",
        description="Run KI Dev Tycoon backend simulations deterministically.",
    )
    parser.add_argument(
        "--ticks",
        type=int,
        default=30,
        help="Number of simulated days to process.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Deterministic random seed used for RNG initialisation.",
    )
    parser.add_argument(
        "--daily-active-users",
        type=int,
        default=5_000,
        help="Active users per day in the simulation.",
    )
    parser.add_argument(
        "--arp-dau",
        type=float,
        default=0.12,
        help="Average revenue per daily active user in Euro.",
    )
    parser.add_argument(
        "--operating-costs",
        type=float,
        default=450.0,
        help="Daily operating costs in Euro.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        metavar="PATH",
        help="Optional path to write the JSON result to.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity for the simulation run.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entrypoint used by the ``ki-sim`` script."""

    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.log_level)
    sim_logger = get_logger("simulation")

    config = SimulationConfig(
        ticks=args.ticks,
        seed=args.seed,
        daily_active_users=args.daily_active_users,
        arp_dau=args.arp_dau,
        operating_costs=args.operating_costs,
    )
    result = run_simulation(config, logger=sim_logger)
    payload = json.dumps(result.model_dump(), indent=2)

    if args.output is None:
        print(payload)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
