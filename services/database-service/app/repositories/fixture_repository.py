from sqlalchemy.orm import Session

from app.models.fixture import FixtureDB
from app.schemas.fixture import FixtureCreate


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
        return created, updated

    def delete(self, fixture_id: int) -> bool:
        fixture = self.get_by_id(fixture_id)
        if fixture:
            self.db.delete(fixture)
            self.db.commit()
            return True
        return False
