"""Simulation kernel package for KI Dev Tycoon."""

from __future__ import annotations

from importlib import metadata
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
__all__ = ["__version__"]

try:
    __version__ = metadata.version("ki-dev-tycoon")
except metadata.PackageNotFoundError:  # pragma: no cover - during local edits
    __version__ = "0.0.0"
