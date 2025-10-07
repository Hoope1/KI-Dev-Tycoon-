"""UI package extensions for the KI Dev Tycoon simulation kernel."""

from __future__ import annotations

from importlib import metadata
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
__all__ = ["__version__"]

try:  # pragma: no cover - query kernel package metadata if installed
    _kernel_version = metadata.version("ki-dev-tycoon")
except metadata.PackageNotFoundError:  # pragma: no cover - editable installs
    _kernel_version = None

try:  # pragma: no cover - query UI package metadata if available
    _ui_version = metadata.version("ki-dev-tycoon-ui")
except metadata.PackageNotFoundError:  # pragma: no cover - editable installs
    if _kernel_version is None:
        __version__ = "0.0.0"
    else:
        __version__ = f"{_kernel_version}+ui"
else:
    if _kernel_version:
        __version__ = f"{_kernel_version}+ui"
    else:
        __version__ = _ui_version
