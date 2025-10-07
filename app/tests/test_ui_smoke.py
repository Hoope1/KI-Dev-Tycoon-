"""Snapshot-based smoke tests for the Textual UI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_SRC = ROOT / "app" / "src"
SIM_SRC = ROOT / "sim" / "src"
for path in (str(SIM_SRC), str(APP_SRC)):
    if path not in sys.path:
        sys.path.insert(0, path)

import asyncio

from rich.console import Console

from ki_dev_tycoon.ui.presenter import SimulationPresenter, SimulationPresenterConfig
from ki_dev_tycoon.ui.widgets import KpiPanel


SNAPSHOT_DIR = Path(__file__).parent / "__snapshots__"


def test_dashboard_kpi_snapshot() -> None:
    """Render the KPI panel and compare it against the stored snapshot."""

    presenter = SimulationPresenter(SimulationPresenterConfig(ticks=10, seed=7))
    state = asyncio.run(presenter.build_ui_state())
    panel = KpiPanel()
    panel.update_view(state.dashboard)
    console = Console(record=True, width=72)
    console.print(panel.render())
    output = console.export_text()

    snapshot_path = SNAPSHOT_DIR / "dashboard_kpis.txt"
    expected = snapshot_path.read_text(encoding="utf-8")
    assert output == expected

