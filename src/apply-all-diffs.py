from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.diffs.apply_production_diffs import apply_diffs_for_dataset


release_id = '2024-06-25'

for dataset_name in DATASETS.keys():
    apply_diffs_for_dataset(dataset_name, release_id)


