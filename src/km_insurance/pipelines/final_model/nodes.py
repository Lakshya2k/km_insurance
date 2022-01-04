from functools import partial
from typing import Any, Dict

import mlflow
import optuna
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRFRegressor


def optimize_hyperparameters(
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.DataFrame,
    y_test: pd.DataFrame,
    n_trials: int,
    random_state: int,
) -> Dict[str, Any]:
    def optimize(
        trial: int,
        x_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_train: pd.DataFrame,
        y_test: pd.DataFrame,
        random_state: int,
    ) -> float:
        num_parallel_tree = trial.suggest_int("num_parallel_tree", 1, 20)
        colsample_bynode = trial.suggest_uniform("colsample_bynode", 0.01, 1)
        learning_rate = trial.suggest_uniform("learning_rate", 0.01, 1)
        subsample = trial.suggest_uniform("subsample", 0.01, 1)
        max_depth = trial.suggest_int("max_depth", 1, 20)
        min_child_weight = trial.suggest_int("min_child_weight", 1, 20)
        random_state = random_state

        model = XGBRFRegressor(
            num_parallel_tree=num_parallel_tree,
            colsample_bynode=colsample_bynode,
            learning_rate=learning_rate,
            subsample=subsample,
            max_depth=max_depth,
            min_child_weight=min_child_weight,
            random_state=random_state,
        )
        model.fit(x_train.values, y_train.values.ravel())
        y_pred = model.predict(x_test.values)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metric("rmse_optimize", rmse)
        mlflow.log_metric("r2_optimize", r2)
        return r2

    hyperparams_optimized = {"hyperparams": {}}
    study = optuna.create_study(direction="maximize")
    optimization_function = partial(
        optimize,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        random_state=random_state,
    )
    study.optimize(optimization_function, n_trials=n_trials)
    mlflow.log_metric("best_r2", study.best_value)
    hyperparams_optimized["hyperparams"] = study.best_params
    return hyperparams_optimized["hyperparams"]


def save_final_model(params: dict, df_features: pd.DataFrame, df_labels: pd.DataFrame):
    model = XGBRFRegressor(**params)
    model.fit(df_features.values, df_labels.values.ravel())
    return model
