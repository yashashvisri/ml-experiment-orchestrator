import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple, Any

def load_and_prep_data(filepath: str, target_col: str) -> Tuple[Any, Any, Any, Any, bool]:
    """
    Reads a CSV file and prepares it for training.
    Returns: X_train, X_test, y_train, y_test, is_classification
    """
    df = pd.read_csv(filepath)
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    df = df.dropna(subset=[target_col])
    
    # Auto-detect if it's classification or regression based on dtype and unique values
    is_classification = False
    if df[target_col].dtype == 'object' or df[target_col].nunique() < 20:
        is_classification = True
        
    # Basic preprocessing: drop high-cardinality/IDs and encode categoricals
    X = df.drop(columns=[target_col])
    
    # Simple label encoding for target if classification
    y = df[target_col]
    if is_classification and y.dtype == 'object':
        y = y.astype('category').cat.codes
        
    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)
    
    # Fill remaining NaNs with column means (very basic imputation)
    X = X.fillna(X.mean())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, is_classification
