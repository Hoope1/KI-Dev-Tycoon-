"""Modal dialog for theme settings."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Label, RadioButton, RadioSet

from ..theme import ThemeSettings


class SettingsDialog(ModalScreen[ThemeSettings | None]):
    """Allow the user to change theme and accessibility options."""

    CSS = """
    SettingsDialog { align: center middle; }
    #dialog { width: 48; padding: 1 2; border: tall $accent; }
    #controls { padding-top: 1; }
    #actions { padding-top: 1; }
    """

    class Submitted(Message):
        """Emitted when the user confirms new settings."""

        def __init__(self, sender: "SettingsDialog", settings: ThemeSettings) -> None:
            super().__init__()
            self.settings = settings
            self._sender = sender

        @property
        def sender(self) -> "SettingsDialog":  # type: ignore[override]
            return self._sender

    def __init__(self, settings: ThemeSettings) -> None:
        super().__init__()
        self._settings = settings

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Darstellung", id="settings-title")
            with RadioSet(id="controls", allow_no_selection=False):
                yield RadioButton("Dunkles Theme", id="theme-dark", value=self._settings.mode == "dark")
                yield RadioButton("Helles Theme", id="theme-light", value=self._settings.mode == "light")
            yield Checkbox(
                "Farbenblindfreundliche Akzente aktivieren",
                id="colorblind",
                value=self._settings.colorblind_friendly,
            )
            with Vertical(id="actions"):
                yield Button("Übernehmen", id="apply", variant="primary")
                yield Button("Abbrechen", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "apply":
            mode = "dark" if self.query_one("#theme-dark", RadioButton).value else "light"
            colorblind = self.query_one("#colorblind", Checkbox).value
            settings = ThemeSettings(mode=mode, colorblind_friendly=colorblind)
            self.post_message(self.Submitted(self, settings))
            self.dismiss(settings)
        elif event.button.id == "cancel":
            self.dismiss(None)

