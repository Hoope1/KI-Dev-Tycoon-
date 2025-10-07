"""Market overview widget."""

from __future__ import annotations

from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import MarketViewModel


class MarketTable(Widget):
    """Render market statistics."""

    DEFAULT_CSS = "MarketTable { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self) -> None:
        super().__init__()
        self._markets: tuple[MarketViewModel, ...] = ()

    def update_view(self, markets: Iterable[MarketViewModel]) -> None:
        self._markets = tuple(markets)
        self.refresh()

    def render(self) -> Table:
        table = Table(title="Markets", pad_edge=False)
        table.add_column("Market", justify="left", style="bold")
        table.add_column("TAM", justify="right")
        table.add_column("Base demand", justify="right")
        table.add_column("Price elasticity", justify="right")
        table.add_column("Adoption", justify="right")
        if not self._markets:
            table.add_row("No markets", "–", "–", "–", "–")
            return table
        for market in self._markets:
            table.add_row(
                market.name,
                f"{market.tam:,d}",
                f"{market.base_demand:.2f}",
                f"{market.price_elasticity:.2f}",
                f"{market.adoption:,d}",
            )
        return table

