import os

from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.datasets.import_dataset import insert_dataset
from s2ag_corpus.synchronisation.config import SyncConfig


def load_dataset(release_id: str, dataset_name: str, config: SyncConfig) -> None:
    datasets_dir = f"{config.base_dir}/datasets/{release_id}"
    insert_dataset(dataset_name, datasets_dir, config.connection, config.monitor)


def load_all_datasets(release_id: str, config: SyncConfig) -> None:
    for dataset_name in DATASETS.keys():
        load_dataset(release_id, dataset_name, config)
