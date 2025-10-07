"""Savegame migration helpers."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ki_dev_tycoon.persistence.errors import SaveGameError

CURRENT_VERSION = 2


def _migrate_v1_to_v2(payload: Mapping[str, Any]) -> MutableMapping[str, Any]:
    state = payload.get("state", {})
    if not isinstance(state, Mapping):
        msg = "Savegame v1 payload expected 'state' mapping"
        raise SaveGameError(msg)
    migrated_state: MutableMapping[str, Any] = {
        "tick": state.get("tick", 0),
        "cash": state.get("cash", 0.0),
        "reputation": state.get("reputation", 50.0),
        "team": {"members": []},
        "products": [],
        "research": {
            "unlocked": [],
            "active": None,
            "progress": 0.0,
            "backlog": [],
        },
    }
    return {"version": CURRENT_VERSION, "state": migrated_state}


def migrate_payload(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate and migrate ``payload`` to the current savegame schema."""

    try:
        version = int(payload["version"])
    except (KeyError, TypeError, ValueError) as exc:
        msg = "Savegame payload is missing a valid version field"
        raise SaveGameError(msg) from exc

    if version == CURRENT_VERSION:
        return payload
    if version == 1:
        return _migrate_v1_to_v2(payload)

    msg = f"Unsupported savegame version: {version}"
    raise SaveGameError(msg)
