from uuid import UUID
import os
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.run import RunCreate, RunResponse
from app.schemas.train import TrainRequest
from app.services.run_service import RunService
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.experiment_repository import ExperimentRepository
from app.core.config import settings
from app.ml.pipeline import run_training_job

router = APIRouter()

@router.post(
    "/{experiment_id}/runs",
    response_model=RunResponse,
)
def create_run(
    experiment_id: UUID,
    run: RunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RunService.create_run(
        db,
        experiment_id,
        run,
        current_user,
    )

@router.get(
    "/{experiment_id}/runs",
    response_model=list[RunResponse],
)
def get_runs(
    experiment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RunService.get_runs_for_experiment(
        db,
        experiment_id,
        current_user,
    )

@router.post("/{experiment_id}/train")
def start_training_job(
    experiment_id: UUID,
    train_req: TrainRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch Dataset
    dataset = DatasetRepository.get_by_id(db, train_req.dataset_id)
    if not dataset or dataset.project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    filepath = os.path.join(settings.UPLOAD_DIR, dataset.file_path)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset file missing on disk")
        
    # 2. Fetch Experiment to ensure access
    experiment = ExperimentRepository.get_by_id(db, experiment_id)
    if not experiment or experiment.project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    # 3. Create a Run in the DB
    run_create = RunCreate(name=f"AutoML_{train_req.model_type}")
    db_run = RunService.create_run(db, experiment_id, run_create, current_user)
    
    # 4. Fire Background Task
    background_tasks.add_task(
        run_training_job,
        filepath=filepath,
        target_col=train_req.target_column,
        model_type=train_req.model_type,
        n_trials=train_req.n_trials,
        mlflow_experiment_id=experiment.mlflow_experiment_id,
        run_id=db_run.id
    )
    
    return {"message": "Training job started in the background", "run_id": db_run.id}
