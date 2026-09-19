import os
import optuna
import mlflow
from sqlalchemy.orm import Session
from app.ml.data_loader import load_and_prep_data
from app.ml.tuner import get_objective
from app.repositories.run_repository import RunRepository
from app.models.run import Run

from app.database.session import SessionLocal

def run_training_job(
    filepath: str, 
    target_col: str, 
    model_type: str, 
    n_trials: int, 
    mlflow_experiment_id: str, 
    run_id: str
):
    db = SessionLocal()
    try:
        db_run = RunRepository.get_by_id(db, run_id)
        if not db_run:
            return
            
        # 1. Update status
        RunRepository.update_status(db, db_run, "RUNNING")
        
        # 2. Load Data
        X_train, X_test, y_train, y_test, is_classification = load_and_prep_data(filepath, target_col)
        
        # 3. Create Optuna Study
        direction = "maximize" if is_classification else "minimize"
        study = optuna.create_study(direction=direction, study_name=f"study_{db_run.id}")
        
        # 4. We want to group all trials under the specific MLflow run created by our API
        with mlflow.start_run(run_id=db_run.mlflow_run_id):
            mlflow.log_param("target_col", target_col)
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("is_classification", is_classification)
            
            # 5. Optimize
            objective = get_objective(
                X_train, X_test, y_train, y_test, 
                model_type=model_type, 
                is_classification=is_classification, 
                experiment_id=mlflow_experiment_id
            )
            study.optimize(objective, n_trials=n_trials)
            
            # Log best overall params
            mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})
            if is_classification:
                mlflow.log_metric("best_accuracy", study.best_value)
            else:
                mlflow.log_metric("best_mse", study.best_value)
                
        # 6. Complete
        RunRepository.update_status(db, db_run, "COMPLETED")
        
    except Exception as e:
        print(f"Training failed: {e}")
        RunRepository.update_status(db, db_run, "FAILED")
    finally:
        db.close()
