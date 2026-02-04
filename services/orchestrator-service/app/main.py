from fastapi import FastAPI

from app.controllers import sync_controller

app = FastAPI(
    title="Orchestrator Service",
    description="Service for orchestrating data sync workflows",
    version="0.1.0",
)

app.include_router(sync_controller.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
