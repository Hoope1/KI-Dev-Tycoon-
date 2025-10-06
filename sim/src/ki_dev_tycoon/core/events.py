"""Publish/subscribe infrastructure for simulation events."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(slots=True, frozen=True)
class SimulationEvent:
    """Base type for all simulation events."""


@dataclass(slots=True, frozen=True)
class SimulationStarted(SimulationEvent):
    """Emitted once the simulation loop has been initialised."""

    seed: int


@dataclass(slots=True, frozen=True)
class TickProcessed(SimulationEvent):
    """Emitted after a simulation tick has finished processing."""

    tick: int


@dataclass(slots=True, frozen=True)
class SimulationCompleted(SimulationEvent):
    """Emitted when the simulation loop terminates successfully."""

    tick: int


EventHandler = Callable[[SimulationEvent], None]


class EventBus:
    """Simple synchronous event dispatcher."""

    def __init__(self) -> None:
        self._subscribers: Dict[type[SimulationEvent], List[EventHandler]] = defaultdict(list)

    def subscribe(
        self, event_type: type[SimulationEvent], handler: EventHandler
    ) -> None:
        """Register ``handler`` to receive ``event_type`` instances."""

        handlers = self._subscribers[event_type]
        if handler not in handlers:
            handlers.append(handler)  # preserve registration order

    def unsubscribe(
        self, event_type: type[SimulationEvent], handler: EventHandler
    ) -> None:
        """Remove ``handler`` from the subscriber list for ``event_type``."""

        handlers = self._subscribers.get(event_type)
        if not handlers:
            return
        try:
            handlers.remove(handler)
        except ValueError:  # handler not registered
            return
        if not handlers:
            del self._subscribers[event_type]

    def publish(self, event: SimulationEvent) -> None:
        """Emit ``event`` to all subscribers synchronously."""

        for event_type, handlers in list(self._subscribers.items()):
            if isinstance(event, event_type):
                for handler in list(handlers):
                    handler(event)

    def clear(self) -> None:
        """Remove all registered subscribers."""

        self._subscribers.clear()
