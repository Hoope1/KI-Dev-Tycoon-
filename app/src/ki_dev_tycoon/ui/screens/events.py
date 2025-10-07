"""Events screen implementation."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ..viewmodels import UiState
from ..widgets import EventLog, NavItem
from .base import BaseScreen


class EventsScreen(BaseScreen):
    """Dedicated event timeline view."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="events", title="Events", nav_items=nav_items)
        self._hint = Static(
            "Zeigt die letzten Spielereignisse und Simulationsturns an.", id="events-hint"
        )
        self._log = EventLog(rows=25)

    def compose_content(self) -> ComposeResult:
        with Vertical():
            yield self._hint
            yield self._log

    def update_view(self, state: UiState) -> None:
        self._log.update_view(state.events)

