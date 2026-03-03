from fastapi import FastAPI

from app.controllers import fixture_controller, league_controller, team_controller
from app.logging import configure_logging

configure_logging()

app = FastAPI(
    title="SportMonks Service",
    description="Service for interacting with SportMonks API",
    version="0.1.0",
)

app.include_router(fixture_controller.router)
app.include_router(league_controller.router)
app.include_router(team_controller.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
