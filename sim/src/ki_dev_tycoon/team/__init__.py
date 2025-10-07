"""Team subsystem helpers."""

from ki_dev_tycoon.team.hiring import HiringResult, ensure_minimum_staff
from ki_dev_tycoon.team.training import TrainingResult, train_team

__all__ = [
    "HiringResult",
    "TrainingResult",
    "ensure_minimum_staff",
    "train_team",
]
