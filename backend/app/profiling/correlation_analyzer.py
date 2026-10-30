import pandas as pd
from typing import Dict, Any, List

def compute_correlation_matrix(df: pd.DataFrame, max_cols: int = 15) -> Dict[str, Any]:
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty or len(numeric_df.columns) < 2:
        return {"columns": [], "matrix": []}

    # Restrict to top columns if too many numeric features
    cols = list(numeric_df.columns[:max_cols])
    corr = numeric_df[cols].corr().fillna(0.0)
    
    matrix: List[List[float]] = []
    for r in corr.values:
        matrix.append([round(float(val), 3) for val in r])

    return {
        "columns": cols,
        "matrix": matrix
    }
