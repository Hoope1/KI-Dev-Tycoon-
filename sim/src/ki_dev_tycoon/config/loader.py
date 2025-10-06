"""Utilities for loading simulation configuration files."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from pydantic import ValidationError

from .schemas import SimulationProfile

SUPPORTED_SUFFIXES: tuple[str, ...] = (".yaml", ".yml", ".toml")


class ConfigLoaderError(RuntimeError):
    """Raised when a configuration file cannot be loaded or validated."""


def _load_raw_payload(path: Path) -> dict[str, Any]:
    try:
        payload = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - file system failures are rare
        msg = f"Failed to read configuration file at {path}"
        raise ConfigLoaderError(msg) from exc

    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(payload)
    elif suffix == ".toml":
        data = tomllib.loads(payload)
    else:  # pragma: no cover - guarded by caller
        msg = f"Unsupported configuration format: {suffix}"
        raise ConfigLoaderError(msg)

    if not isinstance(data, dict):
        msg = (
            "Configuration files must define a mapping at the top level, "
            f"found {type(data).__name__}"
        )
        raise ConfigLoaderError(msg)
    return data


def load_profile(path: Path) -> SimulationProfile:
    """Load and validate a configuration profile from ``path``."""

    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        msg = f"Unsupported configuration file suffix: {path.suffix}"
        raise ConfigLoaderError(msg)

    raw_data = _load_raw_payload(path)
    try:
        return SimulationProfile.model_validate(raw_data)
    except ValidationError as exc:  # pragma: no cover - validation tested separately
        msg = f"Failed to validate configuration file {path}"
        raise ConfigLoaderError(msg) from exc


@dataclass(slots=True)
class ConfigLoader:
    """Resolve and load configuration profiles from a directory."""

    root: Path

    def __post_init__(self) -> None:
        self.root = self.root.expanduser().resolve()

    def _candidate_paths(self, profile_name: str) -> Iterable[Path]:
        for suffix in SUPPORTED_SUFFIXES:
            yield self.root / f"{profile_name}{suffix}"

    def load(self, profile_name: str) -> SimulationProfile:
        """Load ``profile_name`` using one of the supported suffixes."""

        for path in self._candidate_paths(profile_name):
            if path.exists():
                return load_profile(path)
        msg = (
            f"Could not find profile '{profile_name}' in {self.root}. "
            f"Expected suffixes: {', '.join(SUPPORTED_SUFFIXES)}"
        )
        raise ConfigLoaderError(msg)
