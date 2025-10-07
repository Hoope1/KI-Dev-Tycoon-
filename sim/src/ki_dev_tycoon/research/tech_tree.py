"""Research tree progression logic."""

from __future__ import annotations

from dataclasses import dataclass

from ki_dev_tycoon.core.state import ResearchState
from ki_dev_tycoon.data.loader import AssetBundle


@dataclass(slots=True, frozen=True)
class ResearchProgressResult:
    """Return value describing the outcome of a research tick."""

    state: ResearchState
    completed: tuple[str, ...]


def _select_next_node(state: ResearchState, assets: AssetBundle) -> str | None:
    """Select the next research node to work on."""

    unlocked = state.unlocked
    backlog_candidates = [node for node in state.backlog if node not in unlocked]
    for candidate in backlog_candidates:
        node = assets.research.get(candidate)
        if node and all(prereq in unlocked for prereq in node.prerequisites):
            return candidate
    for node in assets.research.values():
        if node.id in unlocked:
            continue
        if all(prereq in unlocked for prereq in node.prerequisites):
            return node.id
    return None


def progress_research(
    state: ResearchState,
    *,
    assets: AssetBundle,
    research_points: float,
) -> ResearchProgressResult:
    """Advance research by ``research_points`` progress units."""

    if research_points <= 0:
        return ResearchProgressResult(state=state, completed=())

    active_id = state.active
    if active_id is None:
        active_id = _select_next_node(state, assets)
        if active_id is None:
            return ResearchProgressResult(state=state, completed=())
        state = state.with_active(active_id)

    node = assets.research.get(active_id)
    if node is None:  # pragma: no cover - guarded by loader validation
        return ResearchProgressResult(state=state.with_active(None), completed=())

    progress_delta = min(1.0, research_points / float(node.cost))
    progressed_state = state.advance(progress_delta)
    completed: list[str] = []
    if progressed_state.progress >= 1.0:
        progressed_state = progressed_state.complete(active_id)
        completed.append(active_id)
        next_id = _select_next_node(progressed_state, assets)
        if next_id is not None:
            progressed_state = progressed_state.with_active(next_id)
    return ResearchProgressResult(state=progressed_state, completed=tuple(completed))
