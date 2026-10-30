import pandas as pd
from typing import Dict, Any

def analyze_target_candidate(df: pd.DataFrame, target_col: str | None = None) -> Dict[str, Any]:
    if not target_col or target_col not in df.columns:
        # Default heuristic: choose last column or common targets
        for candidate in ["target", "label", "class", "churn", "price", "is_churned"]:
            if candidate in df.columns:
                target_col = candidate
                break
        if not target_col and len(df.columns) > 0:
            target_col = df.columns[-1]

    if not target_col:
        return {"detected": False}

    s = df[target_col].dropna()
    is_classification = s.dtype == 'object' or s.nunique() < 20
    
    class_dist = {}
    if is_classification:
        counts = s.value_counts().head(10).to_dict()
        class_dist = {str(k): int(v) for k, v in counts.items()}

    return {
        "detected": True,
        "target_column": target_col,
        "task_type": "classification" if is_classification else "regression",
        "unique_values": int(s.nunique()),
        "class_distribution": class_dist
    }
