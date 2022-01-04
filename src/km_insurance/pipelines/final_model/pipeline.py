from kedro.pipeline import Pipeline, node

from .nodes import optimize_hyperparameters, save_final_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                optimize_hyperparameters,
                inputs=[
                    "train_features",
                    "test_features",
                    "train_labels",
                    "test_labels",
                    "params:n_trials",
                    "params:random_state",
                ],
                outputs="hyperparams_optimized",
                name="optimize_hyperparameters_node",
            ),
            node(
                save_final_model,
                inputs=[
                    "hyperparams_optimized",
                    "df_features_preprocessed",
                    "df_labels",
                ],
                outputs="final_model",
                name="save_final_model_node",
            ),
        ]
    )
