from ki_dev_tycoon.app import SimulationConfig, run_simulation
from ki_dev_tycoon.core import TickClock, RandomSource


def test_simulation_returns_expected_snapshot() -> None:
    config = SimulationConfig(
        ticks=5,
        seed=99,
        daily_active_users=1_000,
        arp_dau=0.1,
        operating_costs=80.0,
    )

    result = run_simulation(config)

    assert result.final_tick == 5
    assert result.cash >= 0.0
    assert 0 <= result.reputation <= 100
    assert result.history is None
    assert result.state["tick"] == 5
    assert isinstance(result.achievements, list)


def test_simulation_history_capture() -> None:
    config = SimulationConfig(
        ticks=4,
        seed=21,
        daily_active_users=500,
        arp_dau=0.2,
        operating_costs=60.0,
    )

    result = run_simulation(config, capture_history=True)

    assert result.history is not None
    assert len(result.history) == config.ticks
    assert all("cash" in row for row in result.history)
    assert result.state["tick"] == config.ticks


def test_simulation_requires_positive_ticks() -> None:
    config = SimulationConfig(
        ticks=0,
        seed=1,
        daily_active_users=100,
        arp_dau=0.1,
        operating_costs=10.0,
    )

    try:
        run_simulation(config)
    except ValueError as exc:
        assert "at least one tick" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("Simulation should require positive ticks")


def test_simulation_accepts_custom_factories() -> None:
    config = SimulationConfig(
        ticks=2,
        seed=7,
        daily_active_users=100,
        arp_dau=0.2,
        operating_costs=10.0,
    )

    created_seeds: list[int] = []

    def clock_factory() -> TickClock:
        return TickClock()

    def rng_factory(seed: int) -> RandomSource:
        created_seeds.append(seed)
        return RandomSource(seed=seed)

    result = run_simulation(
        config, clock_factory=clock_factory, rng_factory=rng_factory
    )

    assert result.final_tick == 2
    assert created_seeds == [config.seed]
