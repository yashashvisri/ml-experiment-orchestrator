from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ReportGenerateRequest(BaseModel):
    project_id: str
    experiment_id: Optional[str] = None
    title: Optional[str] = "AI Experiment Research & Performance Report"
    include_recommendations: bool = True

class ReportSummaryResponse(BaseModel):
    project_id: str
    project_name: str
    experiment_name: Optional[str] = None
    total_runs: int
    best_model_name: Optional[str] = None
    best_metric: Optional[Dict[str, Any]] = None
    markdown_content: str
