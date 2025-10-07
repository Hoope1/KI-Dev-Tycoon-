"""Serialization helpers for :class:`~ki_dev_tycoon.core.state.GameState`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import zstandard as zstd
from pydantic import BaseModel, Field, ValidationError, field_validator

from ki_dev_tycoon.achievements import AchievementSnapshot
from ki_dev_tycoon.core.state import (
    GameState,
    ProductState,
    ResearchState,
    TeamMember,
    TeamState,
)
from ki_dev_tycoon.persistence.errors import SaveGameError
from ki_dev_tycoon.persistence.migrations import CURRENT_VERSION, migrate_payload

ZSTD_LEVEL = 7


class TeamMemberModel(BaseModel):
    role_id: str
    skill: float = Field(ge=0.0, le=1.0)
    training_progress: float = Field(ge=0.0, le=1.0)

    @classmethod
    def from_member(cls, member: TeamMember) -> "TeamMemberModel":
        return cls(
            role_id=member.role_id,
            skill=member.skill,
            training_progress=member.training_progress,
        )

    def to_member(self) -> TeamMember:
        return TeamMember(
            role_id=self.role_id,
            skill=float(self.skill),
            training_progress=float(self.training_progress),
        )


class TeamModel(BaseModel):
    members: tuple[TeamMemberModel, ...]

    @classmethod
    def from_team(cls, team: TeamState) -> "TeamModel":
        return cls(members=tuple(TeamMemberModel.from_member(m) for m in team.members))

    def to_team(self) -> TeamState:
        return TeamState(members=tuple(member.to_member() for member in self.members))


class ProductModel(BaseModel):
    product_id: str
    quality: float = Field(ge=0.0, le=1.0)
    adoption: int = Field(ge=0)
    price: float = Field(ge=0.0)

    @classmethod
    def from_product(cls, product: ProductState) -> "ProductModel":
        return cls(
            product_id=product.product_id,
            quality=product.quality,
            adoption=product.adoption,
            price=product.price,
        )

    def to_product(self) -> ProductState:
        return ProductState(
            product_id=self.product_id,
            quality=float(self.quality),
            adoption=int(self.adoption),
            price=float(self.price),
        )


class ResearchModel(BaseModel):
    unlocked: tuple[str, ...]
    active: str | None
    progress: float = Field(ge=0.0, le=1.0)
    backlog: tuple[str, ...]

    @classmethod
    def from_state(cls, state: ResearchState) -> "ResearchModel":
        return cls(
            unlocked=tuple(sorted(state.unlocked)),
            active=state.active,
            progress=state.progress,
            backlog=state.backlog,
        )

    def to_state(self) -> ResearchState:
        return ResearchState(
            unlocked=frozenset(self.unlocked),
            active=self.active,
            progress=float(self.progress),
            backlog=tuple(self.backlog),
        )


class AchievementModel(BaseModel):
    id: str
    name: str
    description: str
    unlocked_tick: int = Field(ge=0)

    @classmethod
    def from_snapshot(cls, snapshot: AchievementSnapshot) -> "AchievementModel":
        return cls(
            id=snapshot.id,
            name=snapshot.name,
            description=snapshot.description,
            unlocked_tick=snapshot.unlocked_tick,
        )

    def to_snapshot(self) -> AchievementSnapshot:
        return AchievementSnapshot(
            id=self.id,
            name=self.name,
            description=self.description,
            unlocked_tick=int(self.unlocked_tick),
        )


class GameStateModel(BaseModel):
    """Pydantic representation of the immutable :class:`GameState`."""

    tick: int = Field(ge=0)
    cash: float = Field(ge=0.0)
    reputation: float = Field(ge=0.0, le=100.0)
    team: TeamModel
    products: tuple[ProductModel, ...]
    research: ResearchModel
    achievements: tuple[AchievementModel, ...] = ()

    @field_validator("products")
    @classmethod
    def _ensure_quality_bounds(
        cls, value: tuple[ProductModel, ...]
    ) -> tuple[ProductModel, ...]:
        for product in value:
            if not 0.0 <= product.quality <= 1.0:
                msg = f"Product {product.product_id} quality must be within [0,1]"
                raise ValueError(msg)
        return value

    @classmethod
    def from_state(cls, state: GameState) -> "GameStateModel":
        return cls(
            tick=state.tick,
            cash=state.cash,
            reputation=state.reputation,
            team=TeamModel.from_team(state.team),
            products=tuple(ProductModel.from_product(p) for p in state.products),
            research=ResearchModel.from_state(state.research),
            achievements=tuple(
                AchievementModel.from_snapshot(snapshot)
                for snapshot in state.achievements
            ),
        )

    def to_state(self) -> GameState:
        return GameState(
            tick=int(self.tick),
            cash=float(self.cash),
            reputation=float(self.reputation),
            team=self.team.to_team(),
            products=tuple(product.to_product() for product in self.products),
            research=self.research.to_state(),
            achievements=tuple(
                achievement.to_snapshot() for achievement in self.achievements
            ),
        )

    def to_dict(self) -> Mapping[str, Any]:
        """Return a deterministic mapping representation."""

        return self.model_dump()


class SavegameModel(BaseModel):
    """Pydantic model representing the canonical savegame payload."""

    version: int = Field(default=CURRENT_VERSION)
    state: GameStateModel

    @classmethod
    def from_state(cls, state: GameState) -> "SavegameModel":
        """Create a savegame model from an immutable :class:`GameState`."""

        return cls(version=CURRENT_VERSION, state=GameStateModel.from_state(state))

    def to_state(self) -> GameState:
        """Return the underlying :class:`GameState`."""

        return self.state.to_state()

    def to_dict(self) -> Mapping[str, Any]:
        """Return a deterministic mapping representation."""

        return self.model_dump()


def encode_savegame(save: SavegameModel, *, compression_level: int = ZSTD_LEVEL) -> bytes:
    """Return a compressed binary representation for ``save``."""

    payload = json.dumps(
        save.to_dict(), separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    compressor = zstd.ZstdCompressor(level=compression_level)
    return compressor.compress(payload)


def decode_savegame(serialised: bytes) -> SavegameModel:
    """Parse ``serialised`` bytes into a :class:`SavegameModel`."""

    decompressor = zstd.ZstdDecompressor()
    try:
        buffer = decompressor.decompress(serialised)
    except zstd.ZstdError as exc:
        msg = "Failed to decompress savegame payload"
        raise SaveGameError(msg) from exc

    try:
        data = json.loads(buffer.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        msg = "Failed to decode savegame JSON payload"
        raise SaveGameError(msg) from exc

    if not isinstance(data, Mapping):
        msg = "Savegame JSON must decode into an object"
        raise SaveGameError(msg)

    migrated = migrate_payload(data)

    try:
        return SavegameModel.model_validate(migrated)
    except ValidationError as exc:
        msg = "Savegame payload failed validation"
        raise SaveGameError(msg) from exc


def save_game(path: Path, state: GameState, *, compression_level: int = ZSTD_LEVEL) -> None:
    """Write ``state`` to ``path`` using the canonical save format."""

    payload = encode_savegame(
        SavegameModel.from_state(state), compression_level=compression_level
    )
    path.write_bytes(payload)


def load_game(path: Path) -> GameState:
    """Load a :class:`GameState` snapshot from ``path``."""

    try:
        buffer = path.read_bytes()
    except OSError as exc:  # pragma: no cover - propagated to caller
        msg = f"Failed to read savegame at {path}"
        raise SaveGameError(msg) from exc
    return decode_savegame(buffer).to_state()
