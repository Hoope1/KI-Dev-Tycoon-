from __future__ import annotations

from typing import List

from ki_dev_tycoon.app import SimulationConfig, run_simulation
from ki_dev_tycoon.core.events import (
    EventBus,
    SimulationCompleted,
    SimulationEvent,
    SimulationStarted,
    TickProcessed,
)


def test_event_bus_collects_simulation_events() -> None:
    bus = EventBus()
    received: List[SimulationEvent] = []

    def handler(event: SimulationEvent) -> None:
        received.append(event)

    bus.subscribe(SimulationEvent, handler)
    config = SimulationConfig(
        ticks=2,
        seed=123,
        daily_active_users=100,
        arp_dau=0.2,
        operating_costs=10.0,
    )

    run_simulation(config, event_bus=bus)

    assert len(received) == 4
    assert received[0] == SimulationStarted(seed=123)
    assert received[1] == TickProcessed(tick=1)
    assert received[2] == TickProcessed(tick=2)
    assert received[3] == SimulationCompleted(tick=2)


def test_event_bus_unsubscribe_is_noop_when_missing() -> None:
    bus = EventBus()
    calls: List[int] = []

    def handler(event: SimulationEvent) -> None:
        calls.append(1)

    bus.subscribe(TickProcessed, handler)
    bus.unsubscribe(TickProcessed, handler)
    bus.unsubscribe(TickProcessed, handler)

    bus.publish(TickProcessed(tick=5))

    assert calls == []
