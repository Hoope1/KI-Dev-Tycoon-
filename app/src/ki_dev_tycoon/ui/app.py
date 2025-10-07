"""Main Textual application entry point."""

from __future__ import annotations

import logging
from typing import Dict

from textual.app import App
from textual.binding import Binding
from textual.events import Mount

from .presenter import SimulationPresenter, SimulationPresenterConfig
from .theme import ThemeController
from .viewmodels import UiState
from .widgets import NavItem
from .screens import (
    DashboardScreen,
    EventsScreen,
    MarketScreen,
    ProductsScreen,
    ResearchScreen,
    TeamScreen,
)
from .screens.base import BaseScreen
from .screens.settings import SettingsDialog


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("dashboard", "Dashboard", "1"),
    NavItem("team", "Team", "2"),
    NavItem("research", "Forschung", "3"),
    NavItem("products", "Produkte", "4"),
    NavItem("market", "Markt", "5"),
    NavItem("events", "Events", "6"),
)


class TycoonApp(App[None]):
    """Textual front-end for the KI Dev Tycoon simulation."""

    CSS_PATH = "app.tcss"
    TITLE = "KI Dev Tycoon UI"
    BINDINGS = [
        Binding("1", "navigate('dashboard')", "Dashboard"),
        Binding("2", "navigate('team')", "Team"),
        Binding("3", "navigate('research')", "Forschung"),
        Binding("4", "navigate('products')", "Produkte"),
        Binding("5", "navigate('market')", "Markt"),
        Binding("6", "navigate('events')", "Events"),
        Binding("ctrl+r", "refresh", "Aktualisieren"),
        Binding("ctrl+p", "open_settings", "Einstellungen"),
        Binding("q", "quit", "Beenden"),
    ]

    def __init__(
        self,
        *,
        presenter: SimulationPresenter | None = None,
        theme_controller: ThemeController | None = None,
        config: SimulationPresenterConfig | None = None,
    ) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self.presenter = presenter or SimulationPresenter(config)
        self.theme_controller = theme_controller or ThemeController()
        self._state: UiState | None = None
        self._screens: Dict[str, BaseScreen] = {}

    async def on_mount(self, event: Mount) -> None:
        del event
        nav_items = NAV_ITEMS
        self._screens = {
            "dashboard": DashboardScreen(nav_items),
            "team": TeamScreen(nav_items),
            "research": ResearchScreen(nav_items),
            "products": ProductsScreen(nav_items),
            "market": MarketScreen(nav_items),
            "events": EventsScreen(nav_items),
        }
        for screen_id, screen in self._screens.items():
            self.install_screen(screen, screen_id)
        self.switch_screen("dashboard")
        self.theme_controller.apply(self, self.theme_controller.settings)
        await self._refresh_state()

    async def _refresh_state(self) -> None:
        self._set_status("Simulation wird geladen…")
        try:
            state = await self.presenter.build_ui_state()
        except Exception:  # pragma: no cover - safeguard for UI experiments
            self._logger.exception("Failed to build UI state")
            self._set_status("Ladevorgang fehlgeschlagen")
            return
        self._state = state
        for screen in self._screens.values():
            screen.update_view(state)
        latest_tick = self.presenter.latest_tick
        status = f"Tick {latest_tick}" if latest_tick else ""
        self._set_status(status or None)

    def _set_status(self, status: str | None) -> None:
        self.sub_title = status or ""

    def action_navigate(self, screen_id: str) -> None:
        if screen_id in self._screens:
            self.switch_screen(screen_id)

    async def action_refresh(self) -> None:
        await self._refresh_state()

    async def action_open_settings(self) -> None:
        dialog = SettingsDialog(self.theme_controller.settings)
        self.push_screen(dialog)

    def on_settings_dialog_submitted(self, message: SettingsDialog.Submitted) -> None:
        self.theme_controller.apply(self, message.settings)

