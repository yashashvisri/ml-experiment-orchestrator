import uuid
import mlflow
from typing import Dict, Any, List, Set
from sqlalchemy.orm import Session
from app.models.experiment import Experiment
from app.models.run import Run
from app.core.config import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

def extract_experiment_comparison(db: Session, project_id: uuid.UUID, experiment_id: uuid.UUID | None = None) -> Dict[str, Any]:
    query = db.query(Experiment).filter(Experiment.project_id == project_id)
    if experiment_id:
        query = query.filter(Experiment.id == experiment_id)
    experiments = query.all()

    runs_data: List[Dict[str, Any]] = []
    all_metrics: Set[str] = set()
    all_params: Set[str] = set()
    
    champion_run = None
    best_acc = -1.0
    client = mlflow.tracking.MlflowClient()

    for exp in experiments:
        db_runs = db.query(Run).filter(Run.experiment_id == exp.id).all()
        for r in db_runs:
            metrics_dict: Dict[str, float] = {}
            params_dict: Dict[str, Any] = {}
            try:
                m_run = client.get_run(r.mlflow_run_id)
                if m_run and m_run.data:
                    metrics_dict = dict(m_run.data.metrics)
                    params_dict = dict(m_run.data.params)
                    all_metrics.update(metrics_dict.keys())
                    all_params.update(params_dict.keys())
                    
                    acc = metrics_dict.get("accuracy", -1.0)
                    if acc > best_acc:
                        best_acc = acc
                        champion_run = str(r.id)
            except Exception:
                pass

            runs_data.append({
                "run_id": str(r.id),
                "run_name": r.name,
                "experiment_name": exp.name,
                "status": r.status,
                "metrics": metrics_dict,
                "params": params_dict,
                "logged_at": str(r.created_at)[:19]
            })

    return {
        "project_id": str(project_id),
        "experiment_id": str(experiment_id) if experiment_id else None,
        "metric_keys": sorted(list(all_metrics)),
        "param_keys": sorted(list(all_params)),
        "runs": runs_data,
        "champion_run_id": champion_run,
        "champion_metric": best_acc if best_acc >= 0 else None
    }
