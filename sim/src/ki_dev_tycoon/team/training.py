"""Team training logic."""

from __future__ import annotations

from dataclasses import dataclass

from ki_dev_tycoon.core.state import TeamMember, TeamState
from ki_dev_tycoon.data.loader import AssetBundle


@dataclass(slots=True, frozen=True)
class TrainingResult:
    """Outcome of a training tick."""

    team: TeamState
    total_skill_gain: float


def train_team(
    team: TeamState,
    *,
    assets: AssetBundle,
    training_bonus: float,
) -> TrainingResult:
    """Advance training for all team members."""

    updated_members: list[TeamMember] = []
    total_skill_gain = 0.0
    for member in team.members:
        role = assets.roles.get(member.role_id)
        if role is None:  # pragma: no cover - guarded by loader validation
            updated_members.append(member)
            continue
        rate = role.training_rate + training_bonus
        progressed = member.advance_training(rate)
        skill_gain = 0.0
        if progressed.training_progress >= 1.0:
            progressed = progressed.reset_training().gain_skill(0.05)
            skill_gain = 0.05
        updated_members.append(progressed)
        total_skill_gain += skill_gain
    return TrainingResult(team=TeamState(members=tuple(updated_members)), total_skill_gain=total_skill_gain)
