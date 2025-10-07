"""Dashboard screen definition."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical

from ..viewmodels import UiState
from ..widgets import EventLog, KpiPanel, NavItem, Timeline
from .base import BaseScreen


class DashboardScreen(BaseScreen):
    """High-level KPI overview."""

    def __init__(self, nav_items: tuple[NavItem, ...]) -> None:
        super().__init__(screen_id="dashboard", title="Dashboard", nav_items=nav_items)
        self._kpi = KpiPanel()
        self._timeline = Timeline(rows=12)
        self._events = EventLog(rows=12)

    def compose_content(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield self._kpi
                yield self._timeline
            yield self._events

    def update_view(self, state: UiState) -> None:
        self._kpi.update_view(state.dashboard)
        self._timeline.update_view(state.dashboard)
        self._events.update_view(state.events)

