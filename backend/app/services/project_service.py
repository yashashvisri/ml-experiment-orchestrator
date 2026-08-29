from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:

    @staticmethod
    def create_project(
        db: Session,
        data: ProjectCreate,
        current_user: User,
    ):
        project = Project(
            name=data.name,
            description=data.description,
            owner_id=current_user.id,
        )

        return ProjectRepository.create(db, project)

    @staticmethod
    def get_my_projects(
        db: Session,
        current_user: User,
    ):
        return ProjectRepository.get_all_by_owner(
            db,
            current_user.id,
        )
    

    @staticmethod
    def get_project_by_id(
        db: Session,
        project_id,
        current_user: User,
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized.",
            )

        return project

    @staticmethod
    def update_project(
        db: Session,
        project_id,
        data: ProjectUpdate,
        current_user: User,
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if not project:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Not authorized.",
            )

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        db.commit()
        db.refresh(project)

        return project

    @staticmethod
    def delete_project(
        db: Session,
        project_id,
        current_user: User,
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if not project:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Not authorized.",
            )

        ProjectRepository.delete(
            db,
            project,
        )

        return {
            "message": "Project deleted successfully."
        }