"""Typer-based CLI commands for launching the Textual UI."""

from __future__ import annotations

import typer

from ki_dev_tycoon.ui.app import TycoonApp
from ki_dev_tycoon.ui.presenter import SimulationPresenter, SimulationPresenterConfig


app = typer.Typer(help="Launch the KI Dev Tycoon Textual client.")


def _run_ui(config: SimulationPresenterConfig, *, headless: bool = False) -> None:
    presenter = SimulationPresenter(config)
    tycoon_app = TycoonApp(presenter=presenter)
    tycoon_app.run(headless=headless)


@app.command()
def dev(
    ticks: int = typer.Option(30, help="Number of ticks to simulate for the dashboard."),
    seed: int = typer.Option(42, help="Deterministic simulation seed."),
) -> None:
    """Launch the UI with a local simulation in development mode."""

    config = SimulationPresenterConfig(ticks=ticks, seed=seed, source="simulation")
    _run_ui(config)


@app.command()
def play(
    api_url: str = typer.Option(
        "http://127.0.0.1:8765",
        "--api-url",
        help="Endpoint of a running FastAPI backend.",
    ),
    ticks: int = typer.Option(30, help="Fallback simulation ticks if API is unavailable."),
    seed: int = typer.Option(42, help="Fallback simulation seed."),
) -> None:
    """Connect to the FastAPI backend or fall back to a local simulation."""

    config = SimulationPresenterConfig(
        ticks=ticks,
        seed=seed,
        api_url=api_url,
        source="api",
    )
    _run_ui(config)


@app.command()
def autoplay(
    ticks: int = typer.Option(60, help="Number of ticks for the automated run."),
    seed: int = typer.Option(42, help="Deterministic simulation seed."),
) -> None:
    """Run the UI headlessly using Textual's dummy driver for automation."""

    config = SimulationPresenterConfig(ticks=ticks, seed=seed, source="simulation")
    _run_ui(config, headless=True)

