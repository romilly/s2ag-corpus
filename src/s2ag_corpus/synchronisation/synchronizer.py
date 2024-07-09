import os

from s2ag_corpus.datasets.dataset_loader import DatasetLoader
from s2ag_corpus.datasets.download_datasets import DatasetDownloader
from s2ag_corpus.diffs.do_diffs import download_and_apply_all_diffs_for
from s2ag_corpus.synchronisation.config import SyncConfig


class Synchronizer:

    def __init__(self, config: SyncConfig):
        self.config = config
        self.datasets_dir = config.datasets_dir
        self.diffs_dir = config.diffs_dir
        self.monitor = config.monitor
        self.release_catalogue = config.api
        self.dataset_downloader = DatasetDownloader(config)
        self.dataset_loader = DatasetLoader(config)

    def find_latest_release_id(self):
        release_id = self.release_catalogue.find_latest_release_id()
        self.monitor.info(f"latest release id: {release_id}")
        return release_id

    def download_datasets(self, release_id):
        self.dataset_downloader.download_all_datasets(release_id)

    def load_datasets(self, release_id):
        self.dataset_loader.load_all_datasets(release_id)

    def download_and_apply_diffs(self, start_release_id, end_release_id, config):
        if start_release_id == end_release_id:
            self.monitor.info(f"diffs are up to date")
        else:
            download_and_apply_all_diffs_for(start_release_id, end_release_id, config)

    def synchronize(self, ):
        self.monitor.info("starting synchronization")
        latest_release_id = self.find_latest_release_id()
        if self.datasets_not_yet_downloaded():
            self.download_and_load_latest_datasets(latest_release_id)
        elif self.diffs_not_yet_downloaded():
            self.download_all_available_diffs(latest_release_id)
        else:
            self.download_later_diffs(latest_release_id)

    def download_later_diffs(self, latest_release_id):
        start_id = self.find_latest_diff_downloaded()
        self.monitor.info(f"latest diff downloaded is {start_id}")
        self.download_and_apply_diffs(start_id, latest_release_id, self.config)

    def download_all_available_diffs(self, latest_release_id):
        start_id = self.original_release_id()
        self.monitor.info(f"applying diffs after original download {start_id}")
        self.download_and_apply_diffs(start_id, latest_release_id, self.config)

    def download_and_load_latest_datasets(self, latest_release_id):
        os.makedirs(self.datasets_dir, exist_ok=True)
        self.download_datasets(latest_release_id)
        self.load_datasets(latest_release_id)

    def diffs_not_yet_downloaded(self):
        return not os.path.isdir(self.diffs_dir)

    def datasets_not_yet_downloaded(self):
        return not os.path.isdir(self.datasets_dir)

    def original_release_id(self):
        subdirectories = [name for name in os.listdir(self.datasets_dir) if os.path.isdir(os.path.join(self.datasets_dir, name))]
        if len(subdirectories) != 1:
            raise ValueError(f"{self.datasets_dir} should contain exactly one subdirectory")
        return subdirectories[0]

    def find_latest_diff_downloaded(self):
        diff_names = sorted(os.listdir(self.diffs_dir))
        return diff_names[-1]