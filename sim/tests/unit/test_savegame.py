from __future__ import annotations

from pathlib import Path

import pytest

from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.persistence.savegame import (
    SaveGame,
    SaveGameError,
    decode_savegame,
    encode_savegame,
    load_game,
    save_game,
)


def test_savegame_roundtrip(tmp_path: Path) -> None:
    state = GameState(tick=7, cash=250.5, reputation=60.0)
    target = tmp_path / "save.json"

    save_game(target, state)
    loaded = load_game(target)

    assert loaded == state


def test_encode_and_decode_are_inverse_operations() -> None:
    state = GameState(tick=1, cash=0.0, reputation=50.0)
    save = SaveGame(state=state)

    serialised = encode_savegame(save)
    decoded = decode_savegame(serialised)

    assert decoded.state == state
    assert decoded.version == save.version


def test_decode_savegame_rejects_invalid_payload() -> None:
    with pytest.raises(SaveGameError):
        decode_savegame("{}")
