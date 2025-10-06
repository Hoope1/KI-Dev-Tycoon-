from __future__ import annotations

from fastapi.testclient import TestClient

from ki_dev_tycoon.api import SimulationStateDTO, create_app


def test_state_endpoint_returns_deterministic_payload() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/state")

    assert response.status_code == 200
    payload = SimulationStateDTO.model_validate(response.json())
    assert payload.tick == 120
    assert payload.in_game_day == 12
    assert payload.reputation == 72.5
    assert payload.projects[0].name == "Aurora QA"
    assert payload.projects[1].project_type == "chatbot"
