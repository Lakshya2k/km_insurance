from kedro.pipeline import Pipeline, node

from .nodes import split_dataset


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_dataset,
                inputs=[
                    "df_features_preprocessed",
                    "df_labels",
                    "params:test_size",
                    "params:random_state",
                ],
                outputs=dict(
                    train_features="train_features",
                    test_features="test_features",
                    train_labels="train_labels",
                    test_labels="test_labels",
                ),
                name="split_dataset_node",
            ),
        ]
    )
