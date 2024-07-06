import os

from s2ag_corpus.datasets.dataset_loader import load_all_datasets
from s2ag_corpus.datasets.download_datasets import DatasetDownloader
from s2ag_corpus.diffs.do_diffs import download_and_apply_all_diffs_for
from s2ag_corpus.synchronisation.config import SyncConfig


class Synchronizer:

    def __init__(self, config: SyncConfig):
        self.config = config
        self.datasets_dir = config.datasets_dir
        self.diffs_dir = config.diffs_dir
        self.monitor = config.monitor

    def find_latest_release_id(self):
        release_id = self.config.requester.find_latest_release_id()
        self.monitor.info(f"latest release id: {release_id}")
        return release_id

    def download_datasets(self, release_id):
        DatasetDownloader(self.config).download_all_datasets(release_id)

    def load_datasets(self, release_id):
        load_all_datasets(release_id, self.config)

    def download_and_apply_diffs(self, start_release_id, end_release_id, config):
        download_and_apply_all_diffs_for(start_release_id, end_release_id, config)

    def synchronise(self):
        latest_release_id = self.find_latest_release_id()
        if self.datasets_not_yet_downloaded():
            os.makedirs(self.datasets_dir)
            self.download_datasets(latest_release_id)
            self.load_datasets(latest_release_id)
            return

        if self.original_release_id() == latest_release_id:
            self.monitor.info("already up to date")
            return

        if self.diffs_not_yet_downloaded():
            self.download_and_apply_diffs(self.original_release_id(), latest_release_id, self.config)

    def diffs_not_yet_downloaded(self):
        return not os.path.isdir(self.diffs_dir)

    def datasets_not_yet_downloaded(self):
        return not os.path.isdir(self.datasets_dir)

    def find_latest_local_release_id(self):
        pass

    def original_release_id(self):
        subdirectories = [name for name in os.listdir(self.datasets_dir) if os.path.isdir(os.path.join(self.datasets_dir, name))]
        if len(subdirectories) != 1:
            raise ValueError(f"{self.datasets_dir} should contain exactly one subdirectory")
        return subdirectories[0]