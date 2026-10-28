import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.comparison_service import ComparisonService
from app.schemas.comparison import ExperimentComparisonResponse

router = APIRouter()

@router.get("/{project_id}", response_model=ExperimentComparisonResponse)
def get_project_run_comparison(
    project_id: str,
    experiment_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        p_uuid = uuid.UUID(project_id)
        e_uuid = uuid.UUID(experiment_id) if experiment_id else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    data = ComparisonService.get_comparison_data(db, p_uuid, e_uuid, current_user)
    return ExperimentComparisonResponse(**data)
