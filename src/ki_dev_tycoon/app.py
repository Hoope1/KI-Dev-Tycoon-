"""CLI entrypoints for running deterministic simulations."""

from __future__ import annotations

import json
from dataclasses import dataclass

import typer
from pydantic import BaseModel, Field

from ki_dev_tycoon.core import RandomSource, TickClock
from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.economy import CashflowParameters, compute_daily_cash_delta

app = typer.Typer(help="Run KI Dev Tycoon backend simulations")


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


def run_simulation(config: SimulationConfig) -> SimulationResult:
    if config.ticks <= 0:
        msg = "Simulation requires at least one tick"
        raise ValueError(msg)

    rng = RandomSource(seed=config.seed)
    clock = TickClock()
    state = GameState(tick=0, cash=0.0, reputation=50.0)
    parameters = config.to_cashflow()

    for _ in range(config.ticks):
        clock.advance()
        state.advance_tick(clock)
        cash_delta = compute_daily_cash_delta(parameters)
        state.apply_cash_delta(cash_delta)

        # Reputation drifts slowly towards success or failure using deterministic jitter.
        direction = 1 if cash_delta >= 0 else -1
        jitter = (rng.random() - 0.5) * 0.2
        state.apply_reputation_delta(direction * 0.5 + jitter)

    return SimulationResult(
        final_tick=state.tick,
        cash=round(state.cash, 2),
        reputation=round(state.reputation, 2),
    )


@app.command()
def run(
    ticks: int = typer.Option(30, help="Number of simulated days"),
    seed: int = typer.Option(42, help="Deterministic random seed"),
    daily_active_users: int = typer.Option(5_000, help="Active users per day"),
    arp_dau: float = typer.Option(0.12, help="Average revenue per daily active user"),
    operating_costs: float = typer.Option(450.0, help="Daily operating costs in Euro"),
    output: typer.FileTextWrite = typer.Option("-", help="Destination for JSON result"),
) -> None:
    """Run a deterministic simulation and print the resulting snapshot as JSON."""

    config = SimulationConfig(
        ticks=ticks,
        seed=seed,
        daily_active_users=daily_active_users,
        arp_dau=arp_dau,
        operating_costs=operating_costs,
    )
    result = run_simulation(config)
    json.dump(result.model_dump(), output, indent=2)
    output.write("\n")


if __name__ == "__main__":
    app()
