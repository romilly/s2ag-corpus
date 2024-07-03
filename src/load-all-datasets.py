from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.datasets.load_production_dataset import load_dataset

release_id = '2024-06-18'

for dataset_name in DATASETS.keys():
    load_dataset(release_id, dataset_name)


