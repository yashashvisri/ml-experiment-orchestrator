import optuna
import mlflow
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import xgboost as xgb
import lightgbm as lgb
from typing import Callable

def get_objective(X_train, X_test, y_train, y_test, model_type: str, is_classification: bool, experiment_id: str) -> Callable:
    """
    Returns an Optuna objective function that also logs each trial to MLflow.
    """
    def objective(trial):
        # We start a nested MLflow run for each Optuna trial
        with mlflow.start_run(experiment_id=experiment_id, nested=True, run_name=f"Trial_{trial.number}"):
            model = None
            
            # --- Random Forest ---
            if model_type == "random_forest":
                n_estimators = trial.suggest_int("n_estimators", 50, 300)
                max_depth = trial.suggest_int("max_depth", 3, 20)
                if is_classification:
                    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
                else:
                    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
                    
            # --- XGBoost ---
            elif model_type == "xgboost":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                    "max_depth": trial.suggest_int("max_depth", 3, 15),
                    "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.5, log=True),
                    "random_state": 42
                }
                if is_classification:
                    model = xgb.XGBClassifier(**params)
                else:
                    model = xgb.XGBRegressor(**params)
                    
            # --- LightGBM ---
            elif model_type == "lightgbm":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                    "max_depth": trial.suggest_int("max_depth", 3, 15),
                    "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.5, log=True),
                    "random_state": 42,
                    "verbose": -1
                }
                if is_classification:
                    model = lgb.LGBMClassifier(**params)
                else:
                    model = lgb.LGBMRegressor(**params)
            else:
                raise ValueError(f"Unknown model_type: {model_type}")

            # Fit Model
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            # Log params
            mlflow.log_params(trial.params)
            mlflow.log_param("model_type", model_type)
            
            # Log metrics & Model
            if is_classification:
                acc = accuracy_score(y_test, preds)
                mlflow.log_metric("accuracy", acc)
                mlflow.sklearn.log_model(model, "model")
                return acc
            else:
                mse = mean_squared_error(y_test, preds)
                mlflow.log_metric("mse", mse)
                mlflow.sklearn.log_model(model, "model")
                return mse

    return objective
