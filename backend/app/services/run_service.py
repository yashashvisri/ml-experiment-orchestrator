import mlflow
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.run import Run
from app.schemas.run import RunCreate
from app.repositories.run_repository import RunRepository
from app.repositories.experiment_repository import ExperimentRepository
from app.repositories.project_repository import ProjectRepository
from app.core.config import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

class RunService:
    @staticmethod
    def create_run(db: Session, experiment_id: UUID, run_in: RunCreate, current_user: User):
        experiment = ExperimentRepository.get_by_id(db, experiment_id)
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
            
        project = ProjectRepository.get_by_id(db, experiment.project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Experiment not found (Access Denied)")

        # Set up in MLflow
        try:
            with mlflow.start_run(experiment_id=experiment.mlflow_experiment_id, run_name=run_in.name) as mlflow_run:
                mlflow_run_id = mlflow_run.info.run_id
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"MLflow error: {str(e)}")

        run = Run(
            name=run_in.name,
            mlflow_run_id=mlflow_run_id,
            experiment_id=experiment.id,
            status="CREATED"
        )
        return RunRepository.create(db, run)

    @staticmethod
    def get_runs_for_experiment(db: Session, experiment_id: UUID, current_user: User):
        experiment = ExperimentRepository.get_by_id(db, experiment_id)
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
            
        project = ProjectRepository.get_by_id(db, experiment.project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Experiment not found (Access Denied)")

        return RunRepository.get_all_by_experiment(db, experiment_id)
