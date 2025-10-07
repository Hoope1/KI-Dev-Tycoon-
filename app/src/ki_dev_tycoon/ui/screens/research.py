"""Research screen implementation."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ..viewmodels import UiState
from ..widgets import NavItem, ResearchTree
from .base import BaseScreen


class ResearchScreen(BaseScreen):
    """Visualise research progress and backlog."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="research", title="Forschung", nav_items=nav_items)
        self._tree = ResearchTree()
        self._status = Static(id="research-status")

    def compose_content(self) -> ComposeResult:
        with Vertical():
            yield self._status
            yield self._tree

    def update_view(self, state: UiState) -> None:
        research = state.research
        active = research.active or "—"
        self._status.update(
            f"Aktiv: [bold]{active}[/bold] · Fortschritt: {research.progress:.0%} · Unlocked: {len(research.unlocked)}"
        )
        self._tree.update_view(research)

