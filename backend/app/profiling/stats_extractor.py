import pandas as pd
from typing import Dict, Any

def extract_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    total_rows = len(df)
    total_columns = len(df.columns)
    mem_usage = round(df.memory_usage(deep=True).sum() / 1024.0, 2)
    duplicates = int(df.duplicated().sum())
    dup_pct = round((duplicates / total_rows * 100.0) if total_rows > 0 else 0.0, 2)
    
    total_cells = total_rows * total_columns
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells * 100.0) if total_cells > 0 else 0.0, 2)
    
    numeric_cols = list(df.select_dtypes(include=['number']).columns)
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "memory_usage_kb": mem_usage,
        "duplicate_rows": duplicates,
        "duplicate_rows_pct": dup_pct,
        "total_missing_cells": missing_cells,
        "total_missing_cells_pct": missing_pct,
        "numeric_columns_count": len(numeric_cols),
        "categorical_columns_count": len(categorical_cols),
    }
