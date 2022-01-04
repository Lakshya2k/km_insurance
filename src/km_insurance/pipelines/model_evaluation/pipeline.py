from kedro.pipeline import Pipeline, node

from .nodes import train_evaluate_models


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                train_evaluate_models,
                inputs=[
                    "params:models_dict",
                    "df_features_preprocessed",
                    "df_labels",
                    "params:n_cv",
                ],
                outputs=dict(
                    models_metrics="models_metrics",
                    rmse_list="rmse_list",
                    r2_list="r2_list",
                ),
                name="train_evaluate_models_node",
            ),
        ]
    )
