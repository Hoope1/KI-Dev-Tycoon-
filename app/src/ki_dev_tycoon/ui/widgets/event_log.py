"""Event log widget."""

from __future__ import annotations

from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import EventLogEntry


class EventLog(Widget):
    """Render the recent simulation events."""

    DEFAULT_CSS = "EventLog { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self, *, rows: int = 12) -> None:
        super().__init__()
        self._rows = rows
        self._events: tuple[EventLogEntry, ...] = ()

    def update_view(self, events: Iterable[EventLogEntry]) -> None:
        events_tuple = tuple(events)
        self._events = events_tuple[-self._rows :]
        self.refresh()

    def render(self) -> Table:
        table = Table(title="Event log", pad_edge=False)
        table.add_column("Tick", justify="right")
        table.add_column("Event", justify="left", style="bold")
        table.add_column("Details", justify="left")
        if not self._events:
            table.add_row("–", "No events", "Simulation idle")
            return table
        for entry in self._events:
            table.add_row(str(entry.tick), entry.name, entry.description)
        return table

