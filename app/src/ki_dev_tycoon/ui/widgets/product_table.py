"""Product overview widget."""

from __future__ import annotations

from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import ProductViewModel


class ProductTable(Widget):
    """Display the current product portfolio."""

    DEFAULT_CSS = "ProductTable { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self) -> None:
        super().__init__()
        self._products: tuple[ProductViewModel, ...] = ()

    def update_view(self, products: Iterable[ProductViewModel]) -> None:
        self._products = tuple(products)
        self.refresh()

    def render(self) -> Table:
        table = Table(title="Products", pad_edge=False)
        table.add_column("Name", justify="left", style="bold")
        table.add_column("Market", justify="left")
        table.add_column("Price", justify="right")
        table.add_column("Quality", justify="right")
        table.add_column("Adoption", justify="right")
        if not self._products:
            table.add_row("No products", "–", "–", "–", "–")
            return table
        for product in self._products:
            table.add_row(
                product.name,
                product.market,
                f"€{product.price:,.2f}",
                f"{product.quality:.2f}",
                f"{product.adoption:,d}",
            )
        return table

