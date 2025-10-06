import logging

import pytest

from ki_dev_tycoon.app import SimulationConfig, run_simulation
from ki_dev_tycoon.utils.logging import configure_logging


@pytest.fixture(autouse=True)
def reset_logging() -> None:
    # Ensure each test starts with a clean logger state.
    logger = logging.getLogger("ki_dev_tycoon")
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.propagate = True


def test_configure_logging_sets_level() -> None:
    logger = configure_logging("debug")

    assert logger.level == logging.DEBUG
    assert logger.handlers  # handler installed


def test_run_simulation_emits_structured_events(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("INFO")
    config = SimulationConfig(
        ticks=2,
        seed=11,
        daily_active_users=1000,
        arp_dau=0.05,
        operating_costs=40.0,
    )

    run_simulation(config)

    log_text = capsys.readouterr().err
    assert "simulation.start" in log_text
    assert "simulation.complete" in log_text
    assert f"seed={config.seed}" in log_text
    assert f"tick={config.ticks}" in log_text
    assert "duration_ms=" in log_text
