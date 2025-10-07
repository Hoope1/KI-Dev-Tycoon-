"""Custom exceptions for persistence modules."""

from __future__ import annotations


class SaveGameError(RuntimeError):
    """Raised when a savegame cannot be parsed or validated."""

    pass
