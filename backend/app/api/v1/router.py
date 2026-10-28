from fastapi import APIRouter

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import projects
from app.api.v1.endpoints import datasets
from app.api.v1.endpoints import experiments
from app.api.v1.endpoints import runs
from app.api.v1.endpoints import assistant
from app.api.v1.endpoints import documents
from app.api.v1.endpoints import reports
from app.api.v1.endpoints import comparison

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

api_router.include_router(
    documents.router,
    prefix="/projects",
    tags=["Knowledge Base"],
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
)

api_router.include_router(
    comparison.router,
    prefix="/comparison",
    tags=["Model Comparison"],
)