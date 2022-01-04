import json
from typing import Any, Dict

import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor, XGBRFRegressor


def train_evaluate_models(
    models_dict: dict, df_features: pd.DataFrame, df_labels: pd.DataFrame, cv: int
) -> Dict[str, Any]:
    models_metrics = {"models_metrics": {}}
    rmse_list = []
    r2_list = []
    for model_name, model_object in models_dict.items():
        model_scores = cross_validate(
            eval(model_object),
            df_features.values,
            df_labels.values.ravel(),
            cv=cv,
            scoring=("neg_root_mean_squared_error", "r2"),
        )
        rmse = -model_scores["test_neg_root_mean_squared_error"].mean()
        r2 = model_scores["test_r2"].mean()
        models_metrics["models_metrics"][model_name] = {"rmse": rmse, "r2": r2}
        rmse_list.append(rmse)
        r2_list.append(r2)
    return dict(
        models_metrics=models_metrics["models_metrics"],
        rmse_list=rmse_list,
        r2_list=r2_list,
    )
