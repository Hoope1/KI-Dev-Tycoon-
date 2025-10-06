from __future__ import annotations

from pathlib import Path

import pytest

from ki_dev_tycoon.config import (
    ConfigLoader,
    ConfigLoaderError,
    EconomyConfig,
    SimulationProfile,
    load_profile,
)


def fixture_path(relative: str) -> Path:
    return Path(__file__).resolve().parents[2] / relative


def test_load_profile_from_yaml() -> None:
    profile_path = fixture_path("config/profiles/default.yaml")

    profile = load_profile(profile_path)

    assert profile.name == "default"
    assert profile.ticks == 30
    assert profile.economy.daily_active_users == 5_000
    assert profile.economy.arp_dau == pytest.approx(0.12)


def test_simulation_profile_converts_to_runtime_config() -> None:
    profile = SimulationProfile(
        name="custom",
        ticks=15,
        seed=7,
        economy=EconomyConfig(
            daily_active_users=1_000,
            arp_dau=0.25,
            operating_costs=300.0,
        ),
    )

    config = profile.to_simulation_config()

    assert config.ticks == 15
    assert config.seed == 7
    assert config.daily_active_users == 1_000
    assert config.arp_dau == pytest.approx(0.25)
    assert config.operating_costs == pytest.approx(300.0)


def test_config_loader_finds_profile_by_suffix(tmp_path: Path) -> None:
    target = tmp_path / "baseline.toml"
    target.write_text(
        """
name = "default"
ticks = 8
seed = 99

[economy]
daily_active_users = 200
arp_dau = 0.5
operating_costs = 100.0
""".strip(),
        encoding="utf-8",
    )

    loader = ConfigLoader(tmp_path)

    profile = loader.load("baseline")

    assert profile.ticks == 8
    assert profile.seed == 99
    assert profile.economy.operating_costs == pytest.approx(100.0)


def test_load_profile_requires_mapping(tmp_path: Path) -> None:
    source = tmp_path / "bad.yaml"
    source.write_text("- 1\n- 2\n", encoding="utf-8")

    with pytest.raises(ConfigLoaderError):
        load_profile(source)


def test_config_loader_reports_missing_profile(tmp_path: Path) -> None:
    loader = ConfigLoader(tmp_path)

    with pytest.raises(ConfigLoaderError):
        loader.load("nonexistent")
