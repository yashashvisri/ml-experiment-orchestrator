from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dataset import DatasetResponse
from app.services.dataset_service import DatasetService

router = APIRouter()


@router.post(
    "/projects/{project_id}/datasets",
    response_model=DatasetResponse,
)
def upload_dataset(
    project_id: UUID,
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DatasetService.upload_dataset(
        db,
        project_id,
        file,
        name,
        description,
        current_user,
    )


@router.get(
    "/projects/{project_id}/datasets",
    response_model=list[DatasetResponse],
)
def get_datasets(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DatasetService.get_datasets_by_project(
        db,
        project_id,
        current_user,
    )


@router.delete(
    "/projects/{project_id}/datasets/{dataset_id}",
)
def delete_dataset(
    project_id: UUID,
    dataset_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DatasetService.delete_dataset(
        db,
        project_id,
        dataset_id,
        current_user,
    )
