"""Platform integration helpers exposed to the UI layer."""

from __future__ import annotations

from . import steam
from .steam import SteamClient, SteamFeatureFlags, get_client, unlock_achievement

__all__ = [
    "steam",
    "SteamClient",
    "SteamFeatureFlags",
    "get_client",
    "unlock_achievement",
]
