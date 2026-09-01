from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.services.experiment_service import ExperimentService

router = APIRouter()

@router.post(
    "/{project_id}/experiments",
    response_model=ExperimentResponse,
)
def create_experiment(
    project_id: UUID,
    experiment: ExperimentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ExperimentService.create_experiment(
        db,
        project_id,
        experiment,
        current_user,
    )

@router.get(
    "/{project_id}/experiments",
    response_model=list[ExperimentResponse],
)
def get_experiments(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ExperimentService.get_experiments_for_project(
        db,
        project_id,
        current_user,
    )
