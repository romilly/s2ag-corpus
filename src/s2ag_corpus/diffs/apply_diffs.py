import gzip
import json
import sys
import os

from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.synchronisation.config import SyncConfig


class DiffApplicator:
    def __init__(self, config: SyncConfig):
        self.connection = config.connection
        self.monitor = config.monitor
        self.diff_directory = config.diffs_dir
        self.count = 0

    def apply_diff_for(self, release_id: str, dataset_name: str):
        self.count = 0
        self.monitor.info(f"Applying diffs for {dataset_name} in {release_id}")
        dataset_path = os.path.join(self.diff_directory, release_id, dataset_name)
        for file_name in sorted(os.listdir(dataset_path)):
            file_path = os.path.join(dataset_path, file_name)
            if file_name.startswith("update_files"):
                self.monitor.info(f"upserting from {file_name}")
                self.upsert(dataset_name, file_path)
            if file_name.startswith("delete_files"):
                self.monitor.info(f"deleting from {file_name}")
                self.delete_rows(dataset_name, file_path)
        self.monitor.info(f"{self.count} rows processed")
        return self.count

    def upsert(self, dataset_name: str, path_to_file):
        cursor = self.connection.cursor()
        dataset = DATASETS[dataset_name]
        with gzip.open(path_to_file, 'rt') as upsert_file:
            for (index, line) in enumerate(upsert_file):
                row = dataset.json_to_tuple(line)
                try:
                    cursor.execute(dataset.upsert, row)
                except Exception as e:
                    self.monitor.error(f"Error {e} in {dataset_name} {path_to_file} ")
                    self.monitor.error(f"line[{index}]: {line}")
                    sys.exit(1)
                self.count += 1
                if 0 == index % 10000:
                    self.connection.commit()
            self.monitor.debug(f"{self.count} rows processed")
            self.connection.commit()

    def delete_rows(self, dataset_name: str, path_to_file):
        dataset = DATASETS[dataset_name]
        cursor = self.connection.cursor()
        with gzip.open(path_to_file, 'rt') as upsert_file:
            for (index, line) in enumerate(upsert_file):
                key = json.loads(line)[dataset.primary_key]
                cursor.execute(dataset.delete_row, (key,))
                self.count += 1
                if 0 == index % 10000:
                    self.connection.commit()
            self.monitor.debug(f"{self.count} rows processed")
            self.connection.commit()







