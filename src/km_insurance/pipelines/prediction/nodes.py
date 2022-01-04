from typing import List

import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder


def get_num_features(df: pd.DataFrame, features_list: List[str]) -> List[str]:
    num_cols = df[features_list].select_dtypes(exclude="object").columns.to_list()
    return num_cols


def get_cat_features(df: pd.DataFrame, features_list: List[str]) -> List[str]:
    cat_cols = df[features_list].select_dtypes(include="object").columns.to_list()
    return cat_cols


def preprocess_num_features(
    df: pd.DataFrame, num_cols: List[str], std_scaler
) -> pd.DataFrame:
    df_num = pd.DataFrame(columns=num_cols)
    df_num[num_cols] = std_scaler.transform(df[num_cols])
    return df_num


def preprocess_cat_features(
    df: pd.DataFrame, cat_cols: List[str]  # , oht_encoder
) -> pd.DataFrame:
    df_cat = pd.DataFrame(columns=cat_cols)
    for cat_col in cat_cols:
        lbl_encoder = LabelEncoder()
        lbl_encoder.fit(df[cat_col])
        df_cat[cat_col] = lbl_encoder.transform(df[cat_col])
    # encoded_cols = list(oht_encoder.get_feature_names(cat_cols))
    # df_cat = pd.DataFrame(columns=encoded_cols)
    # df_cat[encoded_cols] = oht_encoder.transform(df[cat_cols])
    return df_cat


def generate_preprocessed_features(
    df_num: pd.DataFrame, df_cat: pd.DataFrame
) -> pd.DataFrame:
    df_features = pd.concat([df_num, df_cat], axis=1)
    return df_features


def predict(
    pred_features_preprocessed: pd.DataFrame, labels_list: List[str], final_model
) -> pd.DataFrame:
    pred_dmatrix = xgb.DMatrix(pred_features_preprocessed.values)
    results = final_model.predict(pred_dmatrix)
    pred_results = pd.DataFrame(data=results, columns=labels_list)
    mlflow.log_artifact("./data/05_model_input/pred_features.csv")
    return pred_results
