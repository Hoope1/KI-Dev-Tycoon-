"""Market demand model."""

from __future__ import annotations

from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.state import GameState, ProductState
from ki_dev_tycoon.data.loader import AssetBundle


def project_adoption(
    state: GameState,
    *,
    product: ProductState,
    assets: AssetBundle,
    rng: RandomSource,
    demand_bonus: float,
    demand_multiplier: float,
) -> int:
    """Compute the adoption count for ``product`` given the current market."""

    product_config = assets.products[product.product_id]
    market = assets.markets[product_config.target_market]
    base_share = market.base_demand + demand_bonus
    price_factor = max(0.1, 1.0 - product.price / max(1.0, market.price_elasticity * 100))
    quality_factor = max(0.0, product.quality)
    reputation_factor = 0.5 + state.reputation / 100
    random_factor = 1.0 + (rng.random() - 0.5) * 0.05
    growth = int(
        market.tam
        * base_share
        * price_factor
        * quality_factor
        * reputation_factor
        * demand_multiplier
        * random_factor
    )
    new_adoption = min(market.tam, product.adoption + max(0, growth))
    return new_adoption
