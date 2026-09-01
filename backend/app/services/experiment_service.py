import mlflow
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate
from app.repositories.experiment_repository import ExperimentRepository
from app.repositories.project_repository import ProjectRepository
from app.core.config import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

class ExperimentService:
    @staticmethod
    def create_experiment(db: Session, project_id: UUID, experiment_in: ExperimentCreate, current_user: User):
        project = ProjectRepository.get_by_id(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        # Set up in MLflow
        try:
            # Provide a unique name for MLflow since MLflow experiment names must be globally unique
            mlflow_exp_name = f"{project.name}_{experiment_in.name}_{str(project.id)[:8]}"
            mlflow_experiment_id = mlflow.create_experiment(mlflow_exp_name)
        except Exception as e:
            # If it already exists or other error
            raise HTTPException(status_code=400, detail=f"MLflow error: {str(e)}")

        experiment = Experiment(
            name=experiment_in.name,
            description=experiment_in.description,
            mlflow_experiment_id=mlflow_experiment_id,
            project_id=project.id
        )
        return ExperimentRepository.create(db, experiment)

    @staticmethod
    def get_experiments_for_project(db: Session, project_id: UUID, current_user: User):
        project = ProjectRepository.get_by_id(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        return ExperimentRepository.get_all_by_project(db, project_id)
