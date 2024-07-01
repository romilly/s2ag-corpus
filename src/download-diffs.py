from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.diffs.download_diff import download_diffs_for
from s2ag_corpus.logging_monitor import LoggingMonitor

start_release_id = "2024-06-18"
end_release_id = "2024-06-25"
monitor = LoggingMonitor()

for dataset_name in DATASETS.keys():
    download_diffs_for(start_release_id, end_release_id, dataset_name, monitor)