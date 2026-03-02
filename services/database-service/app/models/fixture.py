from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FixtureDB(Base):
    __tablename__ = "fixtures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(Integer, nullable=False)
    league_id: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    group_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    aggregate_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    round_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    state_id: Mapped[int] = mapped_column(Integer, nullable=False)
    venue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    starting_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    result_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    leg: Mapped[str | None] = mapped_column(String(50), nullable=True)
    details: Mapped[str | None] = mapped_column(String(500), nullable=True)
    length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    placeholder: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_odds: Mapped[bool] = mapped_column(Boolean, nullable=False)
    starting_at_timestamp: Mapped[int | None] = mapped_column(Integer, nullable=True)
