"""Navigation widgets used by the Textual UI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from textual import events
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button


@dataclass(slots=True, frozen=True)
class NavItem:
    """Descriptor for a navigation button."""

    screen_id: str
    label: str
    shortcut: str | None = None


class NavigationBar(Widget):
    """Horizontal navigation used to switch between screens."""

    DEFAULT_CSS = "NavigationBar { height: auto; padding: 0 1; }"

    class NavRequested(Message):
        """Message emitted when the user selects a navigation target."""

        def __init__(self, sender: NavigationBar, target: str) -> None:
            super().__init__()
            self.target = target
            self._sender = sender

        @property
        def sender(self) -> NavigationBar:  # type: ignore[override]
            return self._sender

    def __init__(self, items: Sequence[NavItem], active: str) -> None:
        super().__init__()
        self._items = tuple(items)
        self._active = active

    def set_active(self, screen_id: str) -> None:
        """Mark ``screen_id`` as active and update button variants."""

        self._active = screen_id
        for button in self.query(Button):
            button.variant = "primary" if button.id == f"nav-{screen_id}" else "default"

    def compose(self) -> Iterable[Widget]:  # type: ignore[override]
        with Horizontal(id="nav-bar"):
            for item in self._items:
                label = item.label
                if item.shortcut:
                    label = f"{item.label} [{item.shortcut}]"
                variant = "primary" if item.screen_id == self._active else "default"
                yield Button(
                    label,
                    id=f"nav-{item.screen_id}",
                    variant=variant,
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        target = event.button.id.replace("nav-", "", 1)
        self.post_message(self.NavRequested(self, target))

    def on_key(self, event: events.Key) -> None:
        if not event.key:
            return
        for item in self._items:
            if item.shortcut == event.key:
                self.post_message(self.NavRequested(self, item.screen_id))
                return

