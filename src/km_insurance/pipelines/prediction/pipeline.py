from kedro.pipeline import Pipeline, node

from .nodes import (
    generate_preprocessed_features,
    get_cat_features,
    get_num_features,
    predict,
    preprocess_cat_features,
    preprocess_num_features,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                get_num_features,
                inputs=["pred_features", "params:features_list"],
                outputs="num_cols",
                name="get_num_features_node",
            ),
            node(
                get_cat_features,
                inputs=["pred_features", "params:features_list"],
                outputs="cat_cols",
                name="get_cat_features_node",
            ),
            node(
                preprocess_num_features,
                inputs=["pred_features", "num_cols", "std_scaler"],
                outputs="pred_num",
                name="preprocess_num_features_node",
            ),
            node(
                preprocess_cat_features,
                inputs=["pred_features", "cat_cols"],  # , "oht_encoder"],
                outputs="pred_cat",
                name="preprocess_cat_features_node",
            ),
            node(
                generate_preprocessed_features,
                inputs=["pred_num", "pred_cat"],
                outputs="pred_features_preprocessed",
                name="generate_preprocessed_features_node",
            ),
            node(
                predict,
                inputs=[
                    "pred_features_preprocessed",
                    "params:labels_list",
                    # "num_cols",
                    # "cat_cols",
                    # "std_scaler",
                    # "oht_encoder",
                    "final_model",
                ],
                outputs="pred_results",
                name="predict_node",
            ),
        ]
    )
