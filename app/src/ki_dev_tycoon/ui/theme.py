"""Theme utilities for the Textual UI."""

from __future__ import annotations

from dataclasses import dataclass

from textual.app import App


@dataclass(slots=True, frozen=True)
class ThemeSettings:
    """User-configurable visual preferences."""

    mode: str = "dark"
    colorblind_friendly: bool = False

    def toggle_mode(self) -> "ThemeSettings":
        """Return a copy with ``mode`` flipped between light and dark."""

        return ThemeSettings(
            mode="light" if self.mode == "dark" else "dark",
            colorblind_friendly=self.colorblind_friendly,
        )

    def toggle_colorblind(self) -> "ThemeSettings":
        """Return a copy with the colorblind flag inverted."""

        return ThemeSettings(
            mode=self.mode,
            colorblind_friendly=not self.colorblind_friendly,
        )


class ThemeController:
    """Apply :class:`ThemeSettings` to a running :class:`~textual.app.App`."""

    def __init__(self) -> None:
        self._settings = ThemeSettings()

    @property
    def settings(self) -> ThemeSettings:
        return self._settings

    def apply(self, app: App, settings: ThemeSettings) -> None:
        """Update ``app`` to match the provided ``settings``."""

        self._settings = settings
        app.dark = settings.mode == "dark"
        if app.screen is not None:
            app.screen.set_class(settings.colorblind_friendly, "colorblind-mode")

