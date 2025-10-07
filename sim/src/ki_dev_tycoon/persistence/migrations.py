"""Savegame migration helpers."""

from __future__ import annotations

from typing import Any, Mapping

from ki_dev_tycoon.persistence.errors import SaveGameError

CURRENT_VERSION = 1


def migrate_payload(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate and migrate ``payload`` to the current savegame schema."""

    try:
        version = int(payload["version"])
    except (KeyError, TypeError, ValueError) as exc:
        msg = "Savegame payload is missing a valid version field"
        raise SaveGameError(msg) from exc

    if version != CURRENT_VERSION:
        msg = f"Unsupported savegame version: {version}"
        raise SaveGameError(msg)

    return payload
