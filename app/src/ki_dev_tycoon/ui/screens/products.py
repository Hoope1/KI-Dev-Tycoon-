"""Products screen implementation."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ..viewmodels import UiState
from ..widgets import EventLog, NavItem, ProductTable
from .base import BaseScreen


class ProductsScreen(BaseScreen):
    """Display portfolio metrics and related events."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="products", title="Produkte", nav_items=nav_items)
        self._products = ProductTable()
        self._summary = Static(id="product-summary")
        self._events = EventLog(rows=10)

    def compose_content(self) -> ComposeResult:
        with Vertical():
            yield self._summary
            yield self._products
            yield self._events

    def update_view(self, state: UiState) -> None:
        products = state.products
        total_adoption = sum(product.adoption for product in products)
        average_quality = (
            sum(product.quality for product in products) / len(products) if products else 0.0
        )
        self._summary.update(
            f"Produkte: {len(products)} · Adoption: {total_adoption:,d} · Qualität: {average_quality:.2f}"
        )
        self._products.update_view(products)
        self._events.update_view(state.events)

