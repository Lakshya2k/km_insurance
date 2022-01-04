from kedro.pipeline import Pipeline, node

from .nodes import fetch_dataset


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                fetch_dataset,
                inputs=["params:dataset_url"],
                outputs="original_dataset",
                name="fetch_dataset_node",
            ),
        ]
    )
