import os

from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.json_file_inserter import JsonFileInserter


def insert_dataset(dataset_name, datasets_dir, connection):
    data_dir = f"{datasets_dir}/{dataset_name}/"
    dataset = DATASETS[dataset_name]
    inserter = JsonFileInserter(dataset, connection)
    inserter.create_table()
    for source_file in sorted(os.listdir(data_dir)):
        full_path = f"{data_dir}/{source_file}"
        print(full_path)
        inserter.copy_json_to_table(full_path)
    inserter.index_table()