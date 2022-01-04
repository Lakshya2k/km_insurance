from typing import Any, Dict, List

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


def get_num_features(df: pd.DataFrame, features_list: List[str]) -> List[str]:
    num_cols = df[features_list].select_dtypes(exclude="object").columns.to_list()
    return num_cols


def get_cat_features(df: pd.DataFrame, features_list: List[str]) -> List[str]:
    cat_cols = df[features_list].select_dtypes(include="object").columns.to_list()
    return cat_cols


def preprocess_num_features(df: pd.DataFrame, num_cols: List[str]) -> Dict[str, Any]:
    std_scaler = StandardScaler()
    std_scaler.fit(df[num_cols])
    df_num = pd.DataFrame(columns=num_cols)
    df_num[num_cols] = std_scaler.transform(df[num_cols])
    return dict(df_num=df_num, std_scaler=std_scaler)


def preprocess_cat_features(
    df: pd.DataFrame, cat_cols: List[str]
) -> pd.DataFrame:  # Dict[str, Any]:
    df_cat = pd.DataFrame(columns=cat_cols)
    for cat_col in cat_cols:
        lbl_encoder = LabelEncoder()
        lbl_encoder.fit(df[cat_col])
        df_cat[cat_col] = lbl_encoder.transform(df[cat_col])
    # oht_encoder = OneHotEncoder(sparse=False, drop="first")
    # oht_encoder.fit(df[cat_cols])
    # encoded_cols = list(oht_encoder.get_feature_names_out(cat_cols))
    # df_cat = pd.DataFrame(columns=encoded_cols)
    # df_cat[encoded_cols] = oht_encoder.transform(df[cat_cols])
    # return dict(df_cat=df_cat, oht_encoder=oht_encoder)
    return df_cat


def generate_preprocessed_features(
    df_num: pd.DataFrame, df_cat: pd.DataFrame
) -> pd.DataFrame:
    df_features = pd.concat([df_num, df_cat], axis=1)
    return df_features


def generate_labels(df: pd.DataFrame, labels_list: List[str]) -> pd.DataFrame:
    df_labels = df[labels_list]
    return df_labels
