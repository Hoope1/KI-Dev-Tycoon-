"""Timeline widget for per-tick KPI history."""

from __future__ import annotations

from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import DashboardViewModel, KpiSnapshot


class Timeline(Widget):
    """Render the KPI history as a compact table."""

    DEFAULT_CSS = "Timeline { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self, *, rows: int = 10) -> None:
        super().__init__()
        self._dashboard: DashboardViewModel | None = None
        self._rows = rows

    def update_view(self, dashboard: DashboardViewModel) -> None:
        self._dashboard = dashboard
        self.refresh()

    def _rows_for(self, history: Iterable[KpiSnapshot]) -> Table:
        table = Table(title="Recent KPIs", pad_edge=False)
        table.add_column("Tick", justify="right")
        table.add_column("Cash", justify="right")
        table.add_column("Revenue", justify="right")
        table.add_column("Adoption", justify="right")
        table.add_column("Quality", justify="right")
        for snapshot in history:
            table.add_row(
                str(snapshot.tick),
                f"€{snapshot.cash:,.0f}",
                f"€{snapshot.revenue:,.0f}",
                f"{snapshot.adoption:,d}",
                f"{snapshot.avg_quality:.2f}",
            )
        return table

    def render(self) -> Table:
        if self._dashboard is None:
            return self._rows_for(())
        return self._rows_for(self._dashboard.tail(self._rows))

