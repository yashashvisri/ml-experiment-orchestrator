from uuid import UUID
from sqlalchemy.orm import Session
from app.models.dataset import Dataset


class DatasetRepository:

    @staticmethod
    def create(
        db: Session,
        dataset: Dataset,
    ):
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def get_by_id(
        db: Session,
        dataset_id: UUID,
    ):
        return (
            db.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .first()
        )

    @staticmethod
    def get_all_by_project(
        db: Session,
        project_id: UUID,
    ):
        return (
            db.query(Dataset)
            .filter(Dataset.project_id == project_id)
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        dataset: Dataset,
    ):
        db.delete(dataset)
        db.commit()
