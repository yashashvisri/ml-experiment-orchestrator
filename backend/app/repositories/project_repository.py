from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:

    @staticmethod
    def create(
        db: Session,
        project: Project,
    ):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_all_by_owner(
        db: Session,
        owner_id: UUID,
    ):
        return (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        project_id: UUID,
    ):
        return (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        project: Project,
    ):
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(
        db: Session,
        project: Project,
    ):
        db.delete(project)
        db.commit()