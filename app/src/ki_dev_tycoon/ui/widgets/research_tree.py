"""Research tree widget."""

from __future__ import annotations

from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import ResearchNodeViewModel, ResearchViewModel


class ResearchTree(Widget):
    """Display research backlog and unlocks."""

    DEFAULT_CSS = "ResearchTree { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self) -> None:
        super().__init__()
        self._research: ResearchViewModel | None = None

    def update_view(self, research: ResearchViewModel) -> None:
        self._research = research
        self.refresh()

    def _render_nodes(self, nodes: Iterable[ResearchNodeViewModel]) -> Table:
        table = Table(title="Research", pad_edge=False)
        table.add_column("Node", justify="left", style="bold")
        table.add_column("Cost", justify="right")
        table.add_column("Status", justify="left")
        for node in nodes:
            status_parts: list[str] = []
            if node.unlocked:
                status_parts.append("Unlocked")
            elif node.in_backlog:
                status_parts.append("Queued")
            else:
                status_parts.append("Locked")
            table.add_row(node.name, str(node.cost), ", ".join(status_parts))
        return table

    def render(self) -> Table:
        if self._research is None:
            return self._render_nodes(())
        return self._render_nodes(self._research.nodes)

