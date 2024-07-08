import os

from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.datasets.import_dataset import insert_dataset
from s2ag_corpus.synchronisation.config import SyncConfig

class DatasetLoader:
    def __init__(self, config: SyncConfig):
        self.config = config

    def load_dataset(self, release_id: str, dataset_name: str) -> None:
        datasets_dir = f"{self.config.base_dir}/datasets/{release_id}"
        insert_dataset(dataset_name, datasets_dir, self.config.connection, self.config.monitor)

    def load_all_datasets(self, release_id: str) -> None:
        for dataset_name in DATASETS.keys():
            self.load_dataset(release_id, dataset_name)
