"""Serialization helpers for the immutable :class:`~ki_dev_tycoon.core.state.GameState`."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from ki_dev_tycoon.core.state import GameState

CURRENT_VERSION = 1


class SaveGameError(RuntimeError):
    """Raised when a savegame cannot be parsed or validated."""


@dataclass(slots=True, frozen=True)
class SaveGame:
    """Container representing an encoded savegame."""

    state: GameState
    version: int = CURRENT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {"version": self.version, "state": self.state.to_dict()}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "SaveGame":
        try:
            version = int(payload["version"])
            raw_state = payload["state"]
        except KeyError as exc:  # pragma: no cover - defensive guard
            msg = "Malformed savegame payload"
            raise SaveGameError(msg) from exc

        if version != CURRENT_VERSION:
            msg = f"Unsupported savegame version: {version}"
            raise SaveGameError(msg)
        if not isinstance(raw_state, Mapping):
            msg = "Savegame payload must contain a state mapping"
            raise SaveGameError(msg)
        return cls(state=GameState.from_dict(raw_state), version=version)


def encode_savegame(save: SaveGame) -> str:
    """Return a canonical JSON representation for ``save``."""

    return json.dumps(save.to_dict(), separators=(",", ":"), sort_keys=True)


def decode_savegame(serialised: str) -> SaveGame:
    """Parse ``serialised`` JSON into a :class:`SaveGame`."""

    try:
        payload = json.loads(serialised)
    except json.JSONDecodeError as exc:
        msg = "Failed to decode savegame JSON"
        raise SaveGameError(msg) from exc
    if not isinstance(payload, dict):
        msg = "Savegame JSON must decode into an object"
        raise SaveGameError(msg)
    return SaveGame.from_dict(payload)


def save_game(path: Path, state: GameState) -> None:
    """Write ``state`` to ``path`` using the canonical save format."""

    payload = encode_savegame(SaveGame(state=state))
    path.write_text(payload + "\n", encoding="utf-8")


def load_game(path: Path) -> GameState:
    """Load a :class:`GameState` snapshot from ``path``."""

    try:
        buffer = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - propagated to caller
        msg = f"Failed to read savegame at {path}"
        raise SaveGameError(msg) from exc
    return decode_savegame(buffer).state
