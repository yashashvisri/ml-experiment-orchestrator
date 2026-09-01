from uuid import UUID
from sqlalchemy.orm import Session
from app.models.experiment import Experiment

class ExperimentRepository:
    @staticmethod
    def create(db: Session, experiment: Experiment):
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        return experiment

    @staticmethod
    def get_by_id(db: Session, experiment_id: UUID):
        return db.query(Experiment).filter(Experiment.id == experiment_id).first()

    @staticmethod
    def get_all_by_project(db: Session, project_id: UUID):
        return db.query(Experiment).filter(Experiment.project_id == project_id).all()

    @staticmethod
    def delete(db: Session, experiment: Experiment):
        db.delete(experiment)
        db.commit()
