from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import league_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Database Service",
    description="Service for database operations",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(league_controller.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
