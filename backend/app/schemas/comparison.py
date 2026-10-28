from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RunComparisonItem(BaseModel):
    run_id: str
    run_name: str
    experiment_name: str
    status: str
    metrics: Dict[str, float]
    params: Dict[str, Any]
    logged_at: str

class ExperimentComparisonResponse(BaseModel):
    project_id: str
    experiment_id: Optional[str] = None
    metric_keys: List[str]
    param_keys: List[str]
    runs: List[RunComparisonItem]
    champion_run_id: Optional[str] = None
    champion_metric: Optional[float] = None
