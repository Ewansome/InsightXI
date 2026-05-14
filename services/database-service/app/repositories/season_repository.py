import time

import structlog
from sqlalchemy.orm import Session

from app.models.season import SeasonDB
from app.schemas.season import SeasonCreate

logger = structlog.get_logger()


class SeasonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[SeasonDB]:
        return self.db.query(SeasonDB).all()

    def get_by_id(self, season_id: int) -> SeasonDB | None:
        return self.db.query(SeasonDB).filter(SeasonDB.id == season_id).first()

    def create(self, season: SeasonCreate) -> SeasonDB:
        db_season = SeasonDB(**season.model_dump())
        self.db.add(db_season)
        self.db.commit()
        self.db.refresh(db_season)
        return db_season

    def bulk_upsert(self, seasons: list[SeasonCreate]) -> tuple[int, int]:
        logger.info("bulk_upsert_started", entity="seasons", records=len(seasons))
        start = time.perf_counter()

        created = 0
        updated = 0

        for season in seasons:
            existing = self.get_by_id(season.id)
            if existing:
                for key, value in season.model_dump().items():
                    setattr(existing, key, value)
                updated += 1
            else:
                self.db.add(SeasonDB(**season.model_dump()))
                created += 1

        self.db.commit()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "bulk_upsert_completed", entity="seasons", created=created, updated=updated, duration_ms=duration_ms
        )
        return created, updated

    def delete(self, season_id: int) -> bool:
        season = self.get_by_id(season_id)
        if season:
            self.db.delete(season)
            self.db.commit()
            return True
        return False
