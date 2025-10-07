from __future__ import annotations

from pathlib import Path

import pytest

from ki_dev_tycoon.data.loader import AssetLoaderError, load_assets


@pytest.fixture()
def asset_root(tmp_path: Path) -> Path:
    root = tmp_path / "assets"
    root.mkdir()
    (root / "roles.yaml").write_text(
        """
- id: engineer
  name: Engineer
  salary: 100
  hiring_difficulty: 0.2
  training_rate: 0.05
  productivity: 0.5
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "products.yaml").write_text(
        """
- id: product
  name: Product
  target_market: market
  base_quality: 0.4
  base_price: 10
  required_roles:
    engineer: 1
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "markets.yaml").write_text(
        """
- id: market
  name: Market
  tam: 100
  base_demand: 0.1
  price_elasticity: 0.8
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "research.yaml").write_text(
        """
- id: node
  name: Node
  cost: 5
  unlocks:
    quality_bonus: 0.1
  prerequisites: []
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "events.yaml").write_text(
        """
- id: event
  name: Event
  weight: 1.0
  effects:
    demand_multiplier: 1.05
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return root


def test_load_assets_success(asset_root: Path) -> None:
    bundle = load_assets(asset_root)

    assert set(bundle.roles) == {"engineer"}
    assert set(bundle.products) == {"product"}
    assert set(bundle.markets) == {"market"}
    assert set(bundle.research) == {"node"}
    assert set(bundle.events) == {"event"}


def test_product_reference_validation(asset_root: Path) -> None:
    (asset_root / "products.yaml").write_text(
        """
- id: product
  name: Product
  target_market: missing_market
  base_quality: 0.4
  base_price: 10
  required_roles:
    engineer: 1
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(AssetLoaderError) as excinfo:
        load_assets(asset_root)

    assert "missing_market" in str(excinfo.value)


def test_event_effect_whitelist(asset_root: Path) -> None:
    (asset_root / "events.yaml").write_text(
        """
- id: event
  name: Event
  weight: 1.0
  effects:
    unsupported: 1
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(AssetLoaderError) as excinfo:
        load_assets(asset_root)

    assert "unsupported" in str(excinfo.value)


def test_research_prerequisites_validation(asset_root: Path) -> None:
    (asset_root / "research.yaml").write_text(
        """
- id: a
  name: A
  cost: 5
  unlocks:
    quality_bonus: 0.1
  prerequisites: []
- id: b
  name: B
  cost: 5
  unlocks:
    demand_bonus: 0.1
  prerequisites:
    - missing
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(AssetLoaderError) as excinfo:
        load_assets(asset_root)

    assert "missing" in str(excinfo.value)
