"""Team overview widget."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from rich.table import Table
from textual.widget import Widget

from ..viewmodels import TeamMemberViewModel, TeamViewModel


class TeamTable(Widget):
    """Render the current team composition."""

    DEFAULT_CSS = "TeamTable { width: 1fr; height: auto; padding: 0 1; }"

    def __init__(self) -> None:
        super().__init__()
        self._team: TeamViewModel | None = None

    def update_view(self, team: TeamViewModel) -> None:
        self._team = team
        self.refresh()

    def _aggregate(self, members: Iterable[TeamMemberViewModel]) -> Table:
        table = Table(title="Team", pad_edge=False)
        table.add_column("Role", justify="left", style="bold")
        table.add_column("Headcount", justify="right")
        table.add_column("Average skill", justify="right")
        table.add_column("Salary / day", justify="right")

        buckets: dict[str, list[TeamMemberViewModel]] = defaultdict(list)
        for member in members:
            buckets[member.role_name].append(member)
        if not buckets:
            table.add_row("No staff", "0", "–", "–")
            return table
        for role_name, bucket in sorted(buckets.items(), key=lambda item: item[0]):
            average_skill = sum(member.skill for member in bucket) / len(bucket)
            salary = sum(member.salary for member in bucket)
            table.add_row(
                role_name,
                str(len(bucket)),
                f"{average_skill:.2f}",
                f"€{salary:,.0f}",
            )
        return table

    def render(self) -> Table:
        if self._team is None:
            return self._aggregate(())
        return self._aggregate(self._team.members)

