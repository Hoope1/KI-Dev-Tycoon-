"""Team screen implementation."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical

from ..viewmodels import UiState
from ..widgets import EventLog, NavItem, TeamTable
from .base import BaseScreen


class TeamScreen(BaseScreen):
    """Display team composition and related events."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="team", title="Team", nav_items=nav_items)
        self._team = TeamTable()
        self._events = EventLog(rows=15)

    def compose_content(self) -> ComposeResult:
        with Vertical():
            yield self._team
            yield self._events

    def update_view(self, state: UiState) -> None:
        self._team.update_view(state.team)
        self._events.update_view(state.events)

