import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.project_repository import ProjectRepository
from app.comparison.analytics import extract_experiment_comparison
from app.models.user import User

class ComparisonService:
    @staticmethod
    def get_comparison_data(db: Session, project_id: uuid.UUID, experiment_id: uuid.UUID | None, current_user: User):
        project = ProjectRepository.get_by_id(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        return extract_experiment_comparison(db, project_id, experiment_id)
