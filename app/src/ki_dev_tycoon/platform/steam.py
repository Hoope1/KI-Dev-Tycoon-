"""Optional Steamworks wrapper used by the UI layer."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

try:  # pragma: no cover - optional dependency
    from steamworks import STEAMWORKS
except ImportError:  # pragma: no cover - Steam SDK not installed
    STEAMWORKS = None

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class SteamFeatureFlags:
    """Feature toggles for the Steam integration."""

    achievements: bool = False

    @classmethod
    def from_env(cls) -> "SteamFeatureFlags":
        value = os.getenv("KI_DEV_TYCOON_STEAM_ACHIEVEMENTS", "0").strip().lower()
        enabled = value in {"1", "true", "yes", "on"}
        return cls(achievements=enabled)


class SteamClient:
    """Thin wrapper around the optional ``steamworks`` package."""

    def __init__(
        self,
        *,
        flags: SteamFeatureFlags | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._flags = flags or SteamFeatureFlags.from_env()
        self._logger = logger or _LOGGER
        self._steam: Any | None = None
        self._available = False
        if not self._flags.achievements:
            self._logger.debug("steam.features.disabled")
            return
        if STEAMWORKS is None:
            self._logger.warning("steam.sdk.missing")
            return
        try:
            steam = STEAMWORKS()
            self._available = bool(steam.Initialize())
            if self._available:
                self._steam = steam
                self._logger.info("steam.initialised")
            else:
                self._logger.warning("steam.initialisation_failed")
        except Exception:  # pragma: no cover - defensive guard
            self._logger.exception("steam.initialisation_error")
            self._steam = None
            self._available = False

    @property
    def is_available(self) -> bool:
        """Return whether the Steam client is ready."""

        return self._available

    def run_callbacks(self) -> None:
        """Invoke Steamworks callbacks if available."""

        if not self._steam:
            return
        try:
            callbacks = getattr(self._steam, "RunCallbacks", None)
            if callbacks is not None:
                callbacks()
        except Exception:  # pragma: no cover - optional API
            self._logger.exception("steam.callbacks_failed")

    def unlock_achievement(self, achievement_id: str) -> bool:
        """Attempt to unlock ``achievement_id`` via Steamworks."""

        if not achievement_id:
            msg = "achievement_id must not be empty"
            raise ValueError(msg)
        if not self._steam:
            return False
        try:
            achievements = getattr(self._steam, "Achievements", None)
            if achievements is not None:
                result = achievements.Set(achievement_id)
                achievements.Store()
            else:
                set_fn = getattr(self._steam, "SetAchievement", None)
                if set_fn is None:
                    self._logger.warning("steam.api.missing_set", extra={"id": achievement_id})
                    return False
                result = set_fn(achievement_id)
                store_fn = getattr(self._steam, "StoreStats", None)
                if store_fn:
                    store_fn()
            return bool(result)
        except Exception:  # pragma: no cover - defensive guard
            self._logger.exception("steam.achievement.failed", extra={"id": achievement_id})
            return False

    def shutdown(self) -> None:
        """Dispose of the Steam client if necessary."""

        if not self._steam:
            return
        try:
            shutdown_fn = getattr(self._steam, "Shutdown", None)
            if shutdown_fn:
                shutdown_fn()
        except Exception:  # pragma: no cover - optional API
            self._logger.exception("steam.shutdown_failed")
        finally:
            self._steam = None
            self._available = False


_client: SteamClient | None = None


def get_client() -> SteamClient:
    """Return a lazily instantiated :class:`SteamClient`."""

    global _client
    if _client is None:
        _client = SteamClient()
    return _client


def unlock_achievement(achievement_id: str) -> bool:
    """Unlock ``achievement_id`` if the Steam feature flag is active."""

    client = get_client()
    if not client.is_available:
        return False
    return client.unlock_achievement(achievement_id)
