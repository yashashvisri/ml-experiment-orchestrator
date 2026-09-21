from fastapi import APIRouter

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import projects
from app.api.v1.endpoints import datasets
from app.api.v1.endpoints import experiments
from app.api.v1.endpoints import runs
from app.api.v1.endpoints import assistant

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"],
)

api_router.include_router(
    datasets.router,
    prefix="/projects",
    tags=["Datasets"],
)

api_router.include_router(
    experiments.router,
    prefix="/projects",
    tags=["Experiments"],
)

api_router.include_router(
    runs.router,
    prefix="/experiments",
    tags=["Runs"],
)

api_router.include_router(
    assistant.router,
    prefix="/assistant",
    tags=["AI Assistant"],
)