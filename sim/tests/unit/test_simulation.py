from ki_dev_tycoon.app import SimulationConfig, run_simulation


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
    assert result.cash == 100.0
    assert 0 <= result.reputation <= 100


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
