"""KI Dev Tycoon simulation kernel."""

from __future__ import annotations

from importlib import metadata

__all__ = ["__version__"]

try:
    __version__ = metadata.version("ki-dev-tycoon")
except metadata.PackageNotFoundError:  # pragma: no cover - during local edits
    __version__ = "0.0.0"
