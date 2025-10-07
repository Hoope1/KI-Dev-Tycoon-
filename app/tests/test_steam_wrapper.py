from __future__ import annotations

import pytest

from ki_dev_tycoon.platform import steam


def test_steam_client_disabled_without_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KI_DEV_TYCOON_STEAM_ACHIEVEMENTS", raising=False)
    client = steam.SteamClient()
    assert not client.is_available
    assert client.unlock_achievement("first_hire") is False
    assert steam.unlock_achievement("first_hire") is False


