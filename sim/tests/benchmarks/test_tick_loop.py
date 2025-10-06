"""Benchmark smoke tests for the deterministic tick loop."""

from __future__ import annotations

import pytest

from ki_dev_tycoon.app import SimulationConfig, run_simulation


@pytest.mark.benchmark(group="tick_loop")
def test_tick_loop_benchmark(benchmark) -> None:
    """Track the baseline execution time for a one-year simulation run."""

    config = SimulationConfig(
        ticks=365,
        seed=42,
        daily_active_users=5_000,
        arp_dau=0.12,
        operating_costs=450.0,
    )

    result = benchmark(lambda: run_simulation(config))

    assert result.final_tick == config.ticks
    assert result.cash != 0
