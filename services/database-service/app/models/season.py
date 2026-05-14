from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SeasonDB(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(Integer, nullable=False)
    league_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tie_breaker_rule_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
    pending: Mapped[bool] = mapped_column(Boolean, default=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    starting_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ending_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    standing_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    games_in_current_week: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
