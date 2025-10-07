from __future__ import annotations

import json

from pathlib import Path

import pytest
import zstandard as zstd

from ki_dev_tycoon.core.state import (
    GameState,
    ProductState,
    ResearchState,
    TeamState,
)
from ki_dev_tycoon.persistence import (
    GameStateModel,
    SaveGameError,
    SavegameModel,
    decode_savegame,
    encode_savegame,
    load_game,
    save_game,
)


def _state() -> GameState:
    products = (
        ProductState(product_id="p", quality=0.5, adoption=100, price=10.0),
    )
    research = ResearchState(unlocked=frozenset({"n"}), active=None, progress=0.0, backlog=())
    team = TeamState(members=())
    return GameState(
        tick=7,
        cash=250.5,
        reputation=60.0,
        team=team,
        products=products,
        research=research,
    )


def test_savegame_roundtrip(tmp_path: Path) -> None:
    state = _state()
    target = tmp_path / "save.zst"

    save_game(target, state)
    loaded = load_game(target)

    assert loaded == state


def test_encode_and_decode_are_inverse_operations() -> None:
    state = _state()
    save = SavegameModel.from_state(state)

    serialised = encode_savegame(save)
    decoded = decode_savegame(serialised)

    assert decoded.state == GameStateModel.from_state(state)
    assert decoded.version == save.version


def test_decode_savegame_rejects_invalid_payload() -> None:
    with pytest.raises(SaveGameError):
        decode_savegame(b"not a valid zstd stream")


def test_decode_savegame_rejects_invalid_json() -> None:
    save = SavegameModel.from_state(_state())
    payload = encode_savegame(save)
    raw = zstd.ZstdDecompressor().decompress(payload).decode("utf-8")
    as_dict = json.loads(raw)
    as_dict["state"]["cash"] = "oops"
    broken_payload = zstd.ZstdCompressor().compress(json.dumps(as_dict).encode("utf-8"))

    with pytest.raises(SaveGameError):
        decode_savegame(broken_payload)


def test_migrate_rejects_unknown_version() -> None:
    corrupt = SavegameModel(
        version=999,
        state=GameStateModel.from_state(_state()),
    )
    payload = encode_savegame(corrupt)

    with pytest.raises(SaveGameError):
        decode_savegame(payload)
