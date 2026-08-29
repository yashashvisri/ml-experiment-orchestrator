import os
import shutil
from uuid import UUID

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.core.config import settings
from app.models.dataset import Dataset
from app.models.user import User
from app.repositories.dataset_repository import DatasetRepository
from app.services.project_service import ProjectService


class DatasetService:

    @staticmethod
    def upload_dataset(
        db: Session,
        project_id: UUID,
        file: UploadFile,
        name: str,
        description: str | None,
        current_user: User,
    ):
        # 1. Verify project exists and belongs to the user
        project = ProjectService.get_project_by_id(db, project_id, current_user)

        # 2. Setup storage path
        project_upload_dir = os.path.join(settings.UPLOAD_DIR, str(project.id))
        os.makedirs(project_upload_dir, exist_ok=True)
        
        file_path = os.path.join(project_upload_dir, file.filename)

        # 3. Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

        # 4. Create database record
        dataset = Dataset(
            name=name,
            description=description,
            file_path=file_path,
            file_size=file_size,
            project_id=project.id,
        )

        return DatasetRepository.create(db, dataset)

    @staticmethod
    def get_datasets_by_project(
        db: Session,
        project_id: UUID,
        current_user: User,
    ):
        # Verify access
        ProjectService.get_project_by_id(db, project_id, current_user)
        
        return DatasetRepository.get_all_by_project(db, project_id)

    @staticmethod
    def delete_dataset(
        db: Session,
        project_id: UUID,
        dataset_id: UUID,
        current_user: User,
    ):
        # Verify access
        ProjectService.get_project_by_id(db, project_id, current_user)
        
        dataset = DatasetRepository.get_by_id(db, dataset_id)
        if not dataset or dataset.project_id != project_id:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Dataset not found.",
            )

        # Remove file from disk
        if os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)

        DatasetRepository.delete(db, dataset)
        
        return {"message": "Dataset deleted successfully."}
