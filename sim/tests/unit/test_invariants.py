from __future__ import annotations

from pathlib import Path

import hypothesis.strategies as st
from hypothesis import given

from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.state import GameState, ProductState, ResearchState, TeamState
from ki_dev_tycoon.data import load_assets
from ki_dev_tycoon.economy import project_adoption
from ki_dev_tycoon.products import compute_quality

ASSET_ROOT = Path(__file__).resolve().parents[3] / "assets"


@given(
    cash=st.floats(min_value=0.0, max_value=10_000.0),
    delta=st.floats(min_value=-1_000.0, max_value=1_000.0),
)
def test_cash_never_negative(cash: float, delta: float) -> None:
    state = GameState(
        tick=0,
        cash=cash,
        reputation=50.0,
        team=TeamState(members=()),
        products=(),
        research=ResearchState(unlocked=frozenset(), active=None, progress=0.0, backlog=()),
    )
    result = state.apply_cash_delta(delta)
    assert result.cash >= 0.0


@given(
    quality_bonus=st.floats(min_value=0.0, max_value=0.5),
    reputation=st.floats(min_value=0.0, max_value=100.0),
)
def test_quality_in_bounds(quality_bonus: float, reputation: float) -> None:
    assets = load_assets(ASSET_ROOT)
    product_config = next(iter(assets.products.values()))
    product = ProductState(
        product_id=product_config.id,
        quality=product_config.base_quality,
        adoption=0,
        price=product_config.base_price,
    )
    state = GameState(
        tick=0,
        cash=0.0,
        reputation=reputation,
        team=TeamState(members=()),
        products=(product,),
        research=ResearchState(unlocked=frozenset(), active=None, progress=0.0, backlog=()),
    )
    quality = compute_quality(state, product=product, assets=assets, research_quality_bonus=quality_bonus)
    assert 0.0 <= quality <= 1.0


@given(
    adoption=st.integers(min_value=0, max_value=12_000),
    reputation=st.floats(min_value=0.0, max_value=100.0),
)
def test_adoption_never_exceeds_tam(adoption: int, reputation: float) -> None:
    assets = load_assets(ASSET_ROOT)
    product_config = next(iter(assets.products.values()))
    market = assets.markets[product_config.target_market]
    adoption = min(adoption, market.tam)
    product = ProductState(
        product_id=product_config.id,
        quality=product_config.base_quality,
        adoption=adoption,
        price=product_config.base_price,
    )
    state = GameState(
        tick=0,
        cash=0.0,
        reputation=reputation,
        team=TeamState(members=()),
        products=(product,),
        research=ResearchState(unlocked=frozenset(), active=None, progress=0.0, backlog=()),
    )
    rng = RandomSource(seed=42)
    updated = project_adoption(
        state,
        product=product,
        assets=assets,
        rng=rng,
        demand_bonus=0.0,
        demand_multiplier=1.0,
    )
    assert 0 <= updated <= market.tam
