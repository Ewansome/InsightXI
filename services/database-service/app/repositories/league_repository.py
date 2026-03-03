import time

import structlog
from sqlalchemy.orm import Session

from app.models.league import LeagueDB
from app.schemas.league import LeagueCreate

logger = structlog.get_logger()


class LeagueRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[LeagueDB]:
        return self.db.query(LeagueDB).all()

    def get_by_id(self, league_id: int) -> LeagueDB | None:
        return self.db.query(LeagueDB).filter(LeagueDB.id == league_id).first()

    def create(self, league: LeagueCreate) -> LeagueDB:
        db_league = LeagueDB(**league.model_dump())
        self.db.add(db_league)
        self.db.commit()
        self.db.refresh(db_league)
        return db_league

    def bulk_upsert(self, leagues: list[LeagueCreate]) -> tuple[int, int]:
        logger.info("bulk_upsert_started", entity="leagues", records=len(leagues))
        start = time.perf_counter()

        created = 0
        updated = 0

        for league in leagues:
            existing = self.get_by_id(league.id)
            if existing:
                for key, value in league.model_dump().items():
                    setattr(existing, key, value)
                updated += 1
            else:
                self.db.add(LeagueDB(**league.model_dump()))
                created += 1

        self.db.commit()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "bulk_upsert_completed", entity="leagues", created=created, updated=updated, duration_ms=duration_ms
        )
        return created, updated

    def delete(self, league_id: int) -> bool:
        league = self.get_by_id(league_id)
        if league:
            self.db.delete(league)
            self.db.commit()
            return True
        return False
