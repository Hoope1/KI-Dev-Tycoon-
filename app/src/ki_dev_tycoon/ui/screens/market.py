"""Market screen implementation."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ..viewmodels import UiState
from ..widgets import MarketTable, NavItem
from .base import BaseScreen


class MarketScreen(BaseScreen):
    """Display market demand and adoption."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="market", title="Markt", nav_items=nav_items)
        self._summary = Static(id="market-summary")
        self._markets = MarketTable()

    def compose_content(self) -> ComposeResult:
        with Vertical():
            yield self._summary
            yield self._markets

    def update_view(self, state: UiState) -> None:
        markets = state.markets
        total_adoption = sum(market.adoption for market in markets)
        self._summary.update(
            f"Segmente: {len(markets)} · Gesamtadoption: {total_adoption:,d}"
        )
        self._markets.update_view(markets)

