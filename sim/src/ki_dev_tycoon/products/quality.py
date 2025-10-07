"""Product quality computation helpers."""

from __future__ import annotations

from ki_dev_tycoon.core.state import GameState, ProductState
from ki_dev_tycoon.data.loader import AssetBundle


def compute_quality(
    state: GameState,
    *,
    product: ProductState,
    assets: AssetBundle,
    research_quality_bonus: float,
) -> float:
    """Compute the current product quality given team skills and research."""

    config = assets.products[product.product_id]
    quality = config.base_quality + research_quality_bonus
    for role_id, weight in config.required_roles.items():
        role = assets.roles[role_id]
        average_skill = state.team.average_skill(role_id)
        quality += average_skill * role.productivity * (weight / max(1, len(config.required_roles)))
    return max(0.0, min(1.0, quality))
