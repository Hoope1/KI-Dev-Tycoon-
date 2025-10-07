"""Dashboard KPI panel widget."""

from __future__ import annotations

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import DashboardViewModel


class KpiPanel(Widget):
    """Render the primary company KPIs."""

    DEFAULT_CSS = "KpiPanel { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self) -> None:
        super().__init__()
        self._dashboard: DashboardViewModel | None = None

    def update_view(self, dashboard: DashboardViewModel) -> None:
        """Store ``dashboard`` for the next render cycle."""

        self._dashboard = dashboard
        self.refresh()

    def render(self) -> Table:
        dashboard = self._dashboard
        table = Table.grid(padding=(0, 1))
        table.add_column("Metric", justify="left", style="bold")
        table.add_column("Value", justify="right")
        if dashboard is None:
            table.add_row("Status", "Loading…")
            return table
        table.title = f"Tick {dashboard.current_tick}"  # type: ignore[assignment]
        table.add_row("Cash", f"€{dashboard.cash:,.0f}")
        table.add_row("Daily revenue", f"€{dashboard.daily_revenue:,.0f}")
        table.add_row("Burn rate", f"€{dashboard.burn_rate:,.0f}")
        table.add_row("Reputation", f"{dashboard.reputation:.1f}")
        table.add_row("Total adoption", f"{dashboard.adoption:,d}")
        table.add_row("Average quality", f"{dashboard.avg_quality:.2f}")
        return table

