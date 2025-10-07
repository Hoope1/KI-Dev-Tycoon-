"""Utilities for loading and validating balancing assets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypeVar

import yaml
from pydantic import ValidationError

from ki_dev_tycoon.config.schemas import (
    EventCatalogue,
    EventConfig,
    MarketCatalogue,
    MarketConfig,
    ProductCatalogue,
    ProductConfig,
    ResearchCatalogue,
    ResearchNode,
    RoleCatalogue,
    RoleConfig,
)

T = TypeVar("T")

ASSET_FILES: dict[str, Callable[[list[dict[str, object]]], object]] = {
    "roles.yaml": RoleCatalogue.model_validate,
    "products.yaml": ProductCatalogue.model_validate,
    "markets.yaml": MarketCatalogue.model_validate,
    "research.yaml": ResearchCatalogue.model_validate,
    "events.yaml": EventCatalogue.model_validate,
}

ALLOWED_EVENT_EFFECTS: frozenset[str] = frozenset(
    {"demand_multiplier", "quality_penalty", "reputation_bonus"}
)


class AssetLoaderError(RuntimeError):
    """Raised when balancing assets cannot be loaded or validated."""


@dataclass(frozen=True)
class AssetBundle:
    """Collection of validated balancing data used by the simulation."""

    roles: dict[str, RoleConfig]
    products: dict[str, ProductConfig]
    markets: dict[str, MarketConfig]
    research: dict[str, ResearchNode]
    events: dict[str, EventConfig]

    def require_role(self, role_id: str) -> RoleConfig:
        """Return the :class:`RoleConfig` for ``role_id`` or raise."""

        try:
            return self.roles[role_id]
        except KeyError as exc:  # pragma: no cover - validated by loader
            msg = f"Unknown role referenced: {role_id}"
            raise AssetLoaderError(msg) from exc


def _load_yaml(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        msg = f"Missing asset file: {path}"
        raise AssetLoaderError(msg)
    try:
        payload = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - file IO failure
        msg = f"Failed to read asset file {path}"
        raise AssetLoaderError(msg) from exc
    try:
        raw = yaml.safe_load(payload) or []
    except yaml.YAMLError as exc:
        msg = f"Failed to parse YAML asset file {path}"
        raise AssetLoaderError(msg) from exc
    if not isinstance(raw, list):
        msg = f"Asset file {path} must contain a list of objects"
        raise AssetLoaderError(msg)
    return raw


def _validate_catalogue(path: Path, validator: Callable[[list[dict[str, object]]], T]) -> T:
    raw = _load_yaml(path)
    try:
        return validator(raw)
    except ValidationError as exc:
        msg = f"Asset file {path} failed validation"
        raise AssetLoaderError(msg) from exc


def _ensure_product_references(
    products: dict[str, ProductConfig],
    roles: dict[str, RoleConfig],
    markets: dict[str, MarketConfig],
) -> None:
    for product in products.values():
        if product.target_market not in markets:
            msg = f"Product {product.id} references unknown market {product.target_market}"
            raise AssetLoaderError(msg)
        for role_id in product.required_roles:
            if role_id not in roles:
                msg = f"Product {product.id} requires unknown role {role_id}"
                raise AssetLoaderError(msg)


def _ensure_research_prerequisites(
    research: dict[str, ResearchNode],
) -> None:
    for node in research.values():
        for prerequisite in node.prerequisites:
            if prerequisite not in research:
                msg = f"Research node {node.id} references unknown prerequisite {prerequisite}"
                raise AssetLoaderError(msg)


def _ensure_event_effects(events: dict[str, EventConfig]) -> None:
    for event in events.values():
        invalid = set(event.effects).difference(ALLOWED_EVENT_EFFECTS)
        if invalid:
            msg = f"Event {event.id} defines unsupported effects: {sorted(invalid)}"
            raise AssetLoaderError(msg)


def load_assets(root: Path) -> AssetBundle:
    """Load all balancing assets located under ``root``."""

    root = root.expanduser().resolve()
    roles_catalogue = _validate_catalogue(root / "roles.yaml", ASSET_FILES["roles.yaml"])
    products_catalogue = _validate_catalogue(
        root / "products.yaml", ASSET_FILES["products.yaml"]
    )
    markets_catalogue = _validate_catalogue(
        root / "markets.yaml", ASSET_FILES["markets.yaml"]
    )
    research_catalogue = _validate_catalogue(
        root / "research.yaml", ASSET_FILES["research.yaml"]
    )
    events_catalogue = _validate_catalogue(root / "events.yaml", ASSET_FILES["events.yaml"])

    roles = roles_catalogue.as_dict()
    products = products_catalogue.as_dict()
    markets = markets_catalogue.as_dict()
    research = research_catalogue.as_dict()
    events = events_catalogue.as_dict()

    if not products:
        raise AssetLoaderError("At least one product must be defined")
    if not roles:
        raise AssetLoaderError("At least one role must be defined")
    if not markets:
        raise AssetLoaderError("At least one market must be defined")

    _ensure_product_references(products, roles, markets)
    _ensure_research_prerequisites(research)
    _ensure_event_effects(events)

    return AssetBundle(
        roles=roles,
        products=products,
        markets=markets,
        research=research,
        events=events,
    )
