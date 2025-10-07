"""Simulation CLI implemented with Typer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Sequence

import typer

from ki_dev_tycoon.app import SimulationConfig, run_simulation
from ki_dev_tycoon.utils.logging import configure_logging, get_logger

app = typer.Typer(help="Run deterministic KI Dev Tycoon simulations.")


@app.command()
def run(
    *,
    ticks: int = typer.Option(30, min=1, help="Number of simulated days to process."),
    seed: int = typer.Option(42, help="Deterministic random seed used for RNG initialisation."),
    daily_active_users: int = typer.Option(
        5_000, min=0, help="Active users per day in the simulation."
    ),
    arp_dau: float = typer.Option(
        0.12, help="Average revenue per daily active user in Euro."
    ),
    operating_costs: float = typer.Option(
        450.0, help="Daily operating costs in Euro."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional path to write the JSON result to.",
        metavar="PATH",
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Logging verbosity for the simulation run.",
        case_sensitive=False,
    ),
) -> None:
    """Run the deterministic simulation for ``ticks`` days."""

    configure_logging(log_level.upper())
    sim_logger = get_logger("simulation")

    config = SimulationConfig(
        ticks=ticks,
        seed=seed,
        daily_active_users=daily_active_users,
        arp_dau=arp_dau,
        operating_costs=operating_costs,
    )

    result = run_simulation(config, logger=sim_logger)
    payload = json.dumps(result.model_dump(), indent=2)

    if output is None:
        typer.echo(payload)
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload + "\n", encoding="utf-8")
    typer.echo(f"Result written to {output}")


def run_cli(argv: Optional[Sequence[str]] = None) -> int:
    """Execute the Typer application with the provided arguments."""

    command = typer.main.get_command(app)
    try:
        command.main(
            args=list(argv) if argv is not None else None,
            prog_name="ki-sim",
            standalone_mode=False,
        )
    except SystemExit as exc:  # pragma: no cover - click compatibility guard
        return int(exc.code or 0)
    return 0
