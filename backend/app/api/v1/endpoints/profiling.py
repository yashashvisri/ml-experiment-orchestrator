import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.profiling_service import ProfilingService
from app.schemas.profiling import DatasetProfileResponse

router = APIRouter()

@router.get("/{project_id}/datasets/{dataset_id}/profile", response_model=DatasetProfileResponse)
def get_dataset_profile(
    project_id: str,
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        p_uuid = uuid.UUID(project_id)
        d_uuid = uuid.UUID(dataset_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    return ProfilingService.profile_dataset(db, p_uuid, d_uuid, current_user)
