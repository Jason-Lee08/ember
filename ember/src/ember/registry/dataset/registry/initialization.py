import logging
from typing import Dict, List, Type

from src.ember.registry.dataset.registry.metadata_registry import (
    DatasetMetadataRegistry,
)
from src.ember.registry.dataset.registry.loader_factory import DatasetLoaderFactory
from src.ember.registry.dataset.base.models import TaskType, DatasetInfo
from src.ember.registry.dataset.base.preppers import IDatasetPrepper

from src.ember.registry.dataset.datasets.truthful_qa import TruthfulQAPrepper
from src.ember.registry.dataset.datasets.mmlu import MMLUPrepper
from src.ember.registry.dataset.datasets.commonsense_qa import CommonsenseQAPrepper
from src.ember.registry.dataset.datasets.halueval import HaluEvalPrepper
from src.ember.registry.dataset.datasets.short_answer import ShortAnswerPrepper
from src.ember.registry.dataset.datasets.code_prepper import CodePrepper

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def initialize_dataset_registry(
    metadata_registry: DatasetMetadataRegistry,
    loader_factory: DatasetLoaderFactory,
) -> None:
    """Initializes the dataset registry with known datasets.

    Registers predefined dataset metadata with the metadata registry and maps associated
    data preppers in the loader factory.

    Args:
        metadata_registry (DatasetMetadataRegistry): The registry for dataset metadata.
        loader_factory (DatasetLoaderFactory): The factory for registering dataset preppers.

    Returns:
        None
    """
    # Define dataset metadata configurations.
    dataset_metadatas: List[DatasetInfo] = [
        DatasetInfo(
            name="truthful_qa",
            description="A dataset for measuring truthfulness.",
            source="truthful_qa",
            task_type=TaskType.MULTIPLE_CHOICE,
        ),
        DatasetInfo(
            name="mmlu",
            description="Massive Multitask Language Understanding dataset.",
            source="cais/mmlu",
            task_type=TaskType.MULTIPLE_CHOICE,
        ),
        DatasetInfo(
            name="commonsense_qa",
            description="A dataset for commonsense QA.",
            source="commonsense_qa",
            task_type=TaskType.MULTIPLE_CHOICE,
        ),
        DatasetInfo(
            name="halueval",
            description="Dataset for evaluating hallucination in QA.",
            source="pminervini/HaluEval",
            task_type=TaskType.BINARY_CLASSIFICATION,
        ),
    ]

    # Register each dataset metadata using explicit keyword arguments.
    for dataset_info in dataset_metadatas:
        metadata_registry.register(dataset_info=dataset_info)

    # Define mapping of dataset names to their corresponding prepper classes.
    prepper_mappings: Dict[str, Type[IDatasetPrepper]] = {
        "truthful_qa": TruthfulQAPrepper,
        "mmlu": MMLUPrepper,
        "commonsense_qa": CommonsenseQAPrepper,
        "halueval": HaluEvalPrepper,
        "my_shortanswer_ds": ShortAnswerPrepper,
        "my_code_ds": CodePrepper,
    }

    # Register each dataset prepper using explicit keyword arguments.
    for dataset_name, prepper_class in prepper_mappings.items():
        loader_factory.register(dataset_name=dataset_name, prepper_class=prepper_class)

    logger.info("Initialized dataset registry with known datasets.")
