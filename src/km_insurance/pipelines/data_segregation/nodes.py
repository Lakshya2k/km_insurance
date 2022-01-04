from typing import Any, Dict

import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(
    df_features: pd.DataFrame,
    df_labels: pd.DataFrame,
    test_size: float,
    random_state: int,
) -> Dict[str, Any]:
    train_features, test_features, train_labels, test_labels = train_test_split(
        df_features, df_labels, test_size=test_size, random_state=random_state
    )
    return dict(
        train_features=train_features,
        test_features=test_features,
        train_labels=train_labels,
        test_labels=test_labels,
    )
