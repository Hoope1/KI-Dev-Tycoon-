from __future__ import annotations

from pathlib import Path

import pytest
import zstandard as zstd

from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.persistence import (
    GameStateModel,
    SaveGameError,
    SavegameModel,
    decode_savegame,
    encode_savegame,
    load_game,
    save_game,
)


def test_savegame_roundtrip(tmp_path: Path) -> None:
    state = GameState(tick=7, cash=250.5, reputation=60.0)
    target = tmp_path / "save.zst"

    save_game(target, state)
    loaded = load_game(target)

    assert loaded == state


def test_encode_and_decode_are_inverse_operations() -> None:
    state = GameState(tick=1, cash=0.0, reputation=50.0)
    save = SavegameModel.from_state(state)

    serialised = encode_savegame(save)
    decoded = decode_savegame(serialised)

    assert decoded.state == GameStateModel.from_state(state)
    assert decoded.version == save.version


def test_decode_savegame_rejects_invalid_payload() -> None:
    with pytest.raises(SaveGameError):
        decode_savegame(b"not a valid zstd stream")


def test_decode_savegame_rejects_invalid_json() -> None:
    save = SavegameModel.from_state(GameState(tick=1, cash=0.0, reputation=50.0))
    payload = encode_savegame(save)
    raw = zstd.ZstdDecompressor().decompress(payload).decode("utf-8")
    corrupted = raw.replace("50.0", '"oops"', 1)
    broken_payload = zstd.ZstdCompressor().compress(corrupted.encode("utf-8"))

    with pytest.raises(SaveGameError):
        decode_savegame(broken_payload)


def test_migrate_rejects_unknown_version() -> None:
    corrupt = SavegameModel(
        version=999,
        state=GameStateModel.from_state(GameState(tick=0, cash=0.0, reputation=50.0)),
    )
    payload = encode_savegame(corrupt)

    with pytest.raises(SaveGameError):
        decode_savegame(payload)
