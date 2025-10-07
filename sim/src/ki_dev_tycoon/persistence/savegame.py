"""Serialization helpers for :class:`~ki_dev_tycoon.core.state.GameState`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import zstandard as zstd
from pydantic import BaseModel, Field, ValidationError

from ki_dev_tycoon.core.state import GameState
from ki_dev_tycoon.persistence.errors import SaveGameError
from ki_dev_tycoon.persistence.migrations import CURRENT_VERSION, migrate_payload

ZSTD_LEVEL = 7


class GameStateModel(BaseModel):
    """Pydantic representation of the immutable :class:`GameState`."""

    tick: int = Field(ge=0)
    cash: float
    reputation: float = Field(ge=0.0, le=100.0)

    @classmethod
    def from_state(cls, state: GameState) -> "GameStateModel":
        """Create a model instance from the domain state."""

        return cls.model_validate(state.to_dict())

    def to_state(self) -> GameState:
        """Convert the model back into the immutable domain object."""

        return GameState(
            tick=int(self.tick), cash=float(self.cash), reputation=float(self.reputation)
        )


class SavegameModel(BaseModel):
    """Pydantic model representing the canonical savegame payload."""

    version: int = Field(default=CURRENT_VERSION)
    state: GameStateModel

    @classmethod
    def from_state(cls, state: GameState) -> "SavegameModel":
        """Create a savegame model from an immutable :class:`GameState`."""

        return cls(version=CURRENT_VERSION, state=GameStateModel.from_state(state))

    def to_state(self) -> GameState:
        """Return the underlying :class:`GameState`."""

        return self.state.to_state()

    def to_dict(self) -> Mapping[str, Any]:
        """Return a deterministic mapping representation."""

        return self.model_dump()


def encode_savegame(save: SavegameModel, *, compression_level: int = ZSTD_LEVEL) -> bytes:
    """Return a compressed binary representation for ``save``."""

    payload = json.dumps(
        save.to_dict(), separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    compressor = zstd.ZstdCompressor(level=compression_level)
    return compressor.compress(payload)


def decode_savegame(serialised: bytes) -> SavegameModel:
    """Parse ``serialised`` bytes into a :class:`SavegameModel`."""

    decompressor = zstd.ZstdDecompressor()
    try:
        buffer = decompressor.decompress(serialised)
    except zstd.ZstdError as exc:
        msg = "Failed to decompress savegame payload"
        raise SaveGameError(msg) from exc

    try:
        data = json.loads(buffer.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        msg = "Failed to decode savegame JSON payload"
        raise SaveGameError(msg) from exc

    if not isinstance(data, Mapping):
        msg = "Savegame JSON must decode into an object"
        raise SaveGameError(msg)

    migrated = migrate_payload(data)

    try:
        return SavegameModel.model_validate(migrated)
    except ValidationError as exc:
        msg = "Savegame payload failed validation"
        raise SaveGameError(msg) from exc


def save_game(path: Path, state: GameState, *, compression_level: int = ZSTD_LEVEL) -> None:
    """Write ``state`` to ``path`` using the canonical save format."""

    payload = encode_savegame(SavegameModel.from_state(state), compression_level=compression_level)
    path.write_bytes(payload)


def load_game(path: Path) -> GameState:
    """Load a :class:`GameState` snapshot from ``path``."""

    try:
        buffer = path.read_bytes()
    except OSError as exc:  # pragma: no cover - propagated to caller
        msg = f"Failed to read savegame at {path}"
        raise SaveGameError(msg) from exc
    return decode_savegame(buffer).to_state()
