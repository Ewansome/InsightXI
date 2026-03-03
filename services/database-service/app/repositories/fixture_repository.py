import time

import structlog
from sqlalchemy.orm import Session

from app.models.fixture import FixtureDB
from app.schemas.fixture import FixtureCreate

logger = structlog.get_logger()


class FixtureRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[FixtureDB]:
        return self.db.query(FixtureDB).all()

    def get_by_id(self, fixture_id: int) -> FixtureDB | None:
        return self.db.query(FixtureDB).filter(FixtureDB.id == fixture_id).first()

    def create(self, fixture: FixtureCreate) -> FixtureDB:
        db_fixture = FixtureDB(**fixture.model_dump())
        self.db.add(db_fixture)
        self.db.commit()
        self.db.refresh(db_fixture)
        return db_fixture

    def bulk_upsert(self, fixtures: list[FixtureCreate]) -> tuple[int, int]:
        logger.info("bulk_upsert_started", entity="fixtures", records=len(fixtures))
        start = time.perf_counter()

        created = 0
        updated = 0

        for fixture in fixtures:
            existing = self.get_by_id(fixture.id)
            if existing:
                for key, value in fixture.model_dump().items():
                    setattr(existing, key, value)
                updated += 1
            else:
                self.db.add(FixtureDB(**fixture.model_dump()))
                created += 1

        self.db.commit()

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "bulk_upsert_completed", entity="fixtures", created=created, updated=updated, duration_ms=duration_ms
        )
        return created, updated

    def delete(self, fixture_id: int) -> bool:
        fixture = self.get_by_id(fixture_id)
        if fixture:
            self.db.delete(fixture)
            self.db.commit()
            return True
        return False
