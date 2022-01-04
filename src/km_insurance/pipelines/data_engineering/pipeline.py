from kedro.pipeline import Pipeline, node

from .nodes import (
    generate_labels,
    generate_preprocessed_features,
    get_cat_features,
    get_num_features,
    preprocess_cat_features,
    preprocess_num_features,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                get_num_features,
                inputs=["original_dataset", "params:features_list"],
                outputs="num_cols",
                name="get_num_features_node",
            ),
            node(
                get_cat_features,
                inputs=["original_dataset", "params:features_list"],
                outputs="cat_cols",
                name="get_cat_features_node",
            ),
            node(
                preprocess_num_features,
                inputs=["original_dataset", "num_cols"],
                outputs=dict(df_num="df_num", std_scaler="std_scaler"),
                name="preprocess_num_features_node",
            ),
            node(
                preprocess_cat_features,
                inputs=["original_dataset", "cat_cols"],
                outputs="df_cat",  # dict(df_cat="df_cat", oht_encoder="oht_encoder"),
                name="preprocess_cat_features_node",
            ),
            node(
                generate_preprocessed_features,
                inputs=["df_num", "df_cat"],
                outputs="df_features_preprocessed",
                name="generate_preprocessed_features_node",
            ),
            node(
                generate_labels,
                inputs=["original_dataset", "params:labels_list"],
                outputs="df_labels",
                name="generate_labels_node",
            ),
        ]
    )
