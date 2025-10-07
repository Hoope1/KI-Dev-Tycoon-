"""Base classes for Textual screens."""

from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Sequence

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.events import Show
from textual.screen import Screen
from textual.widgets import Footer, Header

from ..viewmodels import UiState
from ..widgets import NavItem, NavigationBar


class BaseScreen(Screen[UiState]):
    """Common scaffolding for screens with navigation."""

    def __init__(self, *, screen_id: str, title: str, nav_items: Sequence[NavItem]) -> None:
        super().__init__(id=screen_id)
        self._title = title
        self._nav_items = tuple(nav_items)
        self._navigation: NavigationBar | None = None
        self.title = title

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="screen-layout"):
            self._navigation = NavigationBar(self._nav_items, active=self.id or "")
            yield self._navigation
            with Container(id="screen-content"):
                yield from self.compose_content()
        yield Footer()

    @abstractmethod
    def compose_content(self) -> Iterable[object]:
        """Compose the screen specific content widgets."""

    @abstractmethod
    def update_view(self, state: UiState) -> None:
        """Update the widgets using ``state``."""

    def on_navigation_bar_nav_requested(self, message: NavigationBar.NavRequested) -> None:
        message.stop()
        if message.target != self.id:
            self.app.action_navigate(message.target)

    def on_show(self, event: Show) -> None:
        del event
        if self._navigation is not None:
            self._navigation.set_active(self.id or "")

