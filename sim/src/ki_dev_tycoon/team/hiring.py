"""Deterministic hiring logic."""

from __future__ import annotations

from dataclasses import dataclass

from ki_dev_tycoon.core.rng import RandomSource
from ki_dev_tycoon.core.state import TeamMember, TeamState
from ki_dev_tycoon.data.loader import AssetBundle


@dataclass(slots=True, frozen=True)
class HiringResult:
    """Return value describing changes introduced by hiring."""

    team: TeamState
    hired: tuple[TeamMember, ...]

    @property
    def hiring_cost(self) -> float:
        """Hiring has no upfront cost in the current model."""

        return 0.0


def ensure_minimum_staff(
    team: TeamState,
    *,
    assets: AssetBundle,
    rng: RandomSource,
    product_ids: tuple[str, ...],
) -> HiringResult:
    """Ensure that each product has the required number of staff for every role."""

    hired: list[TeamMember] = []
    updated_team = team

    for product_id in product_ids:
        product = assets.products[product_id]
        for role_id, required in product.required_roles.items():
            members = updated_team.members_by_role(role_id)
            while len(members) < required:
                role = assets.roles[role_id]
                # Probability of successful hire is inverse of difficulty.
                if rng.random() < role.hiring_difficulty:
                    break
                new_member = TeamMember(role_id=role_id, skill=0.4, training_progress=0.0)
                updated_team = updated_team.add_member(new_member)
                hired.append(new_member)
                members = updated_team.members_by_role(role_id)
    return HiringResult(team=updated_team, hired=tuple(hired))
