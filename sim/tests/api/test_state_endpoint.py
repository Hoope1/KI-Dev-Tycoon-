from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from ki_dev_tycoon.api import AchievementDTO, SimulationStateDTO, create_app
from ki_dev_tycoon.app import SimulationConfig, run_simulation
from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.data import load_assets
from ki_dev_tycoon.persistence import save_game


def _config() -> SimulationConfig:
    return SimulationConfig(
        ticks=3,
        seed=21,
        daily_active_users=1_000,
        arp_dau=0.12,
        operating_costs=120.0,
    )


def test_state_endpoint_returns_simulation_snapshot() -> None:
    app = create_app(config=_config())
    client = TestClient(app)

    response = client.get("/state")
    assert response.status_code == 200
    payload = SimulationStateDTO.model_validate(response.json())

    assert payload.tick == _config().ticks
    assert payload.in_game_day == payload.tick // 10
    assert payload.cash >= 0.0
    expected_projects = len(load_assets(_config().resolve_asset_root()).products)
    assert len(payload.projects) == expected_projects

    achievements_response = client.get("/achievements")
    assert achievements_response.status_code == 200
    achievements = [
        AchievementDTO.model_validate(entry) for entry in achievements_response.json()
    ]
    assert len(achievements) == len(payload.achievements)

    history_response = client.get("/history")
    assert history_response.status_code == 200
    history_payload = history_response.json()
    assert len(history_payload) == _config().ticks
    assert all("cash" in row for row in history_payload)

    raw_response = client.get("/state/raw")
    assert raw_response.status_code == 200
    raw_payload = raw_response.json()
    assert raw_payload["tick"] == payload.tick


def test_simulate_endpoint_accepts_overrides() -> None:
    app = create_app(config=_config())
    client = TestClient(app)

    response = client.post("/simulate", json={"ticks": 5, "seed": 99})
    assert response.status_code == 200
    payload = SimulationStateDTO.model_validate(response.json())

    assert payload.tick == 5
    history_payload = client.get("/history").json()
    assert len(history_payload) == 5


def test_state_endpoint_can_load_savegame(tmp_path: Path) -> None:
    config = _config()
    result = run_simulation(config)
    state = GameState.from_dict(result.state)
    save_path = tmp_path / "save.zst"
    save_game(save_path, state)

    app = create_app(config=config, save_path=save_path)
    client = TestClient(app)

    response = client.get("/state")
    assert response.status_code == 200
    payload = SimulationStateDTO.model_validate(response.json())
    assert payload.tick == state.tick
    assert abs(payload.cash - state.cash) < 1e-6
