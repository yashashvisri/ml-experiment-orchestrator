import uuid
import mlflow
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.experiment import Experiment
from app.models.run import Run
from app.models.dataset import Dataset
from app.core.config import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

def collect_experiment_metrics(db: Session, project_id: uuid.UUID, experiment_id: uuid.UUID | None = None) -> Dict[str, Any]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError("Project not found")

    datasets = db.query(Dataset).filter(Dataset.project_id == project_id).all()
    experiments_query = db.query(Experiment).filter(Experiment.project_id == project_id)
    if experiment_id:
        experiments_query = experiments_query.filter(Experiment.id == experiment_id)
    experiments = experiments_query.all()

    runs_data: List[Dict[str, Any]] = []
    best_run = None
    best_score = -1.0

    client = mlflow.tracking.MlflowClient()

    for exp in experiments:
        db_runs = db.query(Run).filter(Run.experiment_id == exp.id).all()
        for r in db_runs:
            run_info: Dict[str, Any] = {
                "id": str(r.id),
                "name": r.name,
                "status": r.status,
                "experiment_name": exp.name,
                "created_at": str(r.created_at)[:19],
                "metrics": {},
                "params": {}
            }
            try:
                m_run = client.get_run(r.mlflow_run_id)
                if m_run and m_run.data:
                    run_info["metrics"] = dict(m_run.data.metrics)
                    run_info["params"] = dict(m_run.data.params)
                    acc = run_info["metrics"].get("accuracy", -1.0)
                    if acc > best_score:
                        best_score = acc
                        best_run = run_info
            except Exception:
                pass
            runs_data.append(run_info)

    return {
        "project": {
            "id": str(project.id),
            "name": project.name,
            "description": project.description or "No description provided."
        },
        "datasets": [
            {"name": d.name, "size_kb": round(d.file_size / 1024, 2)} for d in datasets
        ],
        "experiments": [
            {"id": str(e.id), "name": e.name, "description": e.description} for e in experiments
        ],
        "runs": runs_data,
        "total_runs": len(runs_data),
        "best_run": best_run
    }
