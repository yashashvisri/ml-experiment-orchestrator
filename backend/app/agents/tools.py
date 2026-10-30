from langchain.tools import tool
from app.database.session import SessionLocal
from app.models.project import Project
from app.models.experiment import Experiment
from app.models.run import Run
from sqlalchemy.orm import Session
import json

def _get_db():
    return SessionLocal()

@tool
def get_user_projects(user_id: str) -> str:
    """Useful to find all Machine Learning projects belonging to a user."""
    db = _get_db()
    try:
        projects = db.query(Project).filter(Project.owner_id == user_id).all()
        if not projects:
            return "No projects found."
        res = [{"id": str(p.id), "name": p.name, "description": p.description} for p in projects]
        return json.dumps(res)
    finally:
        db.close()

@tool
def get_project_experiments(project_id: str) -> str:
    """Useful to find all experiments within a specific ML project ID."""
    db = _get_db()
    try:
        exps = db.query(Experiment).filter(Experiment.project_id == project_id).all()
        if not exps:
            return "No experiments found for this project."
        res = [{"id": str(e.id), "name": e.name, "mlflow_id": e.mlflow_experiment_id} for e in exps]
        return json.dumps(res)
    finally:
        db.close()

@tool
def get_experiment_runs(experiment_id: str) -> str:
    """Useful to fetch all machine learning runs (models trained) inside a specific experiment ID."""
    db = _get_db()
    try:
        runs = db.query(Run).filter(Run.experiment_id == experiment_id).all()
        if not runs:
            return "No runs found."
        res = [{"id": str(r.id), "name": r.name, "status": r.status, "mlflow_run_id": r.mlflow_run_id} for r in runs]
        return json.dumps(res)
    finally:
        db.close()

from app.rag.retriever import retrieve_knowledge

@tool
def search_knowledge_base(query: str, project_id: str) -> str:
    """Useful to search through PDF documents, reports, and logs uploaded to the project's knowledge base to answer questions."""
    return retrieve_knowledge(query, project_id)

from app.reporting.metrics_collector import collect_experiment_metrics
from app.reporting.markdown_generator import generate_markdown_report
import uuid

@tool
def generate_experiment_report(project_id: str) -> str:
    """Useful to automatically summarize and compile a full ML research and performance report for a project."""
    db = _get_db()
    try:
        data = collect_experiment_metrics(db, uuid.UUID(project_id))
        return generate_markdown_report(data)
    except Exception as e:
        return f"Error compiling report: {str(e)}"
    finally:
        db.close()

from app.comparison.analytics import extract_experiment_comparison

@tool
def compare_experiment_models(project_id: str) -> str:
    """Useful to compare all machine learning models, hyperparameters, and accuracy scores in a project."""
    db = _get_db()
    try:
        data = extract_experiment_comparison(db, uuid.UUID(project_id))
        runs = data.get("runs", [])
        if not runs:
            return "No runs available to compare."
        summary = [f"Found {len(runs)} runs. Champion run ID: {data.get('champion_run_id')} with score {data.get('champion_metric')}"]
        for r in runs[:5]:
            summary.append(f"- {r['run_name']}: metrics={r['metrics']}, params={r['params']}")
        return "\n".join(summary)
    except Exception as e:
        return f"Error comparing models: {str(e)}"
    finally:
        db.close()

from app.repositories.dataset_repository import DatasetRepository
from app.profiling.stats_extractor import extract_summary_stats
import pandas as pd
import os

@tool
def profile_dataset(dataset_id: str) -> str:
    """Useful to inspect, profile, and perform Exploratory Data Analysis (EDA) on a dataset CSV."""
    db = _get_db()
    try:
        dataset = DatasetRepository.get_by_id(db, uuid.UUID(dataset_id))
        if not dataset or not os.path.exists(dataset.file_path):
            return f"Dataset {dataset_id} not found on disk."
        df = pd.read_csv(dataset.file_path)
        stats = extract_summary_stats(df)
        cols = list(df.columns)[:10]
        return f"Dataset '{dataset.name}': {stats['total_rows']} rows, {stats['total_columns']} columns. Missing cells: {stats['total_missing_cells_pct']}%. Columns: {cols}"
    except Exception as e:
        return f"Error profiling dataset: {str(e)}"
    finally:
        db.close()
