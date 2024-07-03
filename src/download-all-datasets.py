from s2ag_corpus.datasets.download_dataset import download
from s2ag_corpus.datasets import DATASETS

release_id = '2024-06-18'

for dataset_name in DATASETS.keys():
    download(release_id, dataset_name)