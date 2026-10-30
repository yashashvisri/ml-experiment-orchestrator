from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ColumnProfile(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_pct: float
    unique_count: int
    top_values: Optional[Dict[str, int]] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    median: Optional[float] = None
    max: Optional[float] = None
    skewness: Optional[float] = None
    outlier_count: Optional[int] = None

class DatasetSummaryStats(BaseModel):
    total_rows: int
    total_columns: int
    memory_usage_kb: float
    duplicate_rows: int
    duplicate_rows_pct: float
    total_missing_cells: int
    total_missing_cells_pct: float
    numeric_columns_count: int
    categorical_columns_count: int

class CorrelationMatrix(BaseModel):
    columns: List[str]
    matrix: List[List[float]]

class DatasetProfileResponse(BaseModel):
    dataset_id: str
    dataset_name: str
    summary: DatasetSummaryStats
    columns: List[ColumnProfile]
    correlation: CorrelationMatrix
    ai_recommendations: str
