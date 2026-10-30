import pandas as pd
import numpy as np
from typing import List, Dict, Any

def profile_columns(df: pd.DataFrame) -> List[Dict[str, Any]]:
    columns_data: List[Dict[str, Any]] = []
    total_rows = len(df)

    for col in df.columns:
        s = df[col]
        missing_count = int(s.isna().sum())
        missing_pct = round((missing_count / total_rows * 100.0) if total_rows > 0 else 0.0, 2)
        unique_count = int(s.nunique(dropna=True))

        col_info: Dict[str, Any] = {
            "name": col,
            "dtype": str(s.dtype),
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_count,
            "top_values": None,
            "mean": None,
            "std": None,
            "min": None,
            "median": None,
            "max": None,
            "skewness": None,
            "outlier_count": None
        }

        # Numeric stats
        if pd.api.types.is_numeric_dtype(s):
            clean_s = s.dropna()
            if not clean_s.empty:
                col_info["mean"] = round(float(clean_s.mean()), 3)
                col_info["std"] = round(float(clean_s.std()), 3) if len(clean_s) > 1 else 0.0
                col_info["min"] = round(float(clean_s.min()), 3)
                col_info["median"] = round(float(clean_s.median()), 3)
                col_info["max"] = round(float(clean_s.max()), 3)
                try:
                    skew_val = clean_s.skew()
                    col_info["skewness"] = round(float(skew_val), 3) if not np.isnan(skew_val) else 0.0
                except Exception:
                    col_info["skewness"] = 0.0
                
                # Outliers using IQR
                q25 = clean_s.quantile(0.25)
                q75 = clean_s.quantile(0.75)
                iqr = q75 - q25
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outliers = int(((clean_s < lower_bound) | (clean_s > upper_bound)).sum())
                col_info["outlier_count"] = outliers
        else:
            # Categorical frequency
            top_vals = s.value_counts(dropna=True).head(5).to_dict()
            col_info["top_values"] = {str(k): int(v) for k, v in top_vals.items()}

        columns_data.append(col_info)

    return columns_data
