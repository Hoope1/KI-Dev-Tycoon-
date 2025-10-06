"""Basic cashflow calculations for the earliest prototype."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CashflowParameters:
    """Economic levers used for the simplified revenue model."""

    daily_active_users: int
    arp_dau: float
    operating_costs: float

    def validate(self) -> None:
        if self.daily_active_users < 0:
            msg = "daily_active_users cannot be negative"
            raise ValueError(msg)
        if self.arp_dau < 0:
            msg = "arp_dau cannot be negative"
            raise ValueError(msg)


def compute_daily_cash_delta(params: CashflowParameters) -> float:
    """Compute the net cash delta for a single tick representing one day."""

    params.validate()
    revenue = params.daily_active_users * params.arp_dau
    return revenue - params.operating_costs
