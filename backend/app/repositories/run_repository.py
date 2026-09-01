from uuid import UUID
from sqlalchemy.orm import Session
from app.models.run import Run

class RunRepository:
    @staticmethod
    def create(db: Session, run: Run):
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def get_by_id(db: Session, run_id: UUID):
        return db.query(Run).filter(Run.id == run_id).first()

    @staticmethod
    def get_all_by_experiment(db: Session, experiment_id: UUID):
        return db.query(Run).filter(Run.experiment_id == experiment_id).all()

    @staticmethod
    def update_status(db: Session, run: Run, status: str):
        run.status = status
        db.commit()
        db.refresh(run)
        return run
