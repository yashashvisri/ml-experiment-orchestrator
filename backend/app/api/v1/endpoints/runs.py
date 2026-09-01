from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.run import RunCreate, RunResponse
from app.services.run_service import RunService

router = APIRouter()

@router.post(
    "/{experiment_id}/runs",
    response_model=RunResponse,
)
def create_run(
    experiment_id: UUID,
    run: RunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RunService.create_run(
        db,
        experiment_id,
        run,
        current_user,
    )

@router.get(
    "/{experiment_id}/runs",
    response_model=list[RunResponse],
)
def get_runs(
    experiment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RunService.get_runs_for_experiment(
        db,
        experiment_id,
        current_user,
    )
