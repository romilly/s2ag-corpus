import datetime

from s2ag_corpus.file_manager import AbstractFileManager, FileManager
from s2ag_corpus.logging_monitor import LoggingMonitor
from s2ag_corpus.monitor import Monitor
from s2ag_corpus.requester import DownloadRequester, WebDownloadRequester


class DatasetDownloader:
    def __init__(self, requester: DownloadRequester, file_manager: AbstractFileManager, monitor: Monitor):
        self.requester = requester
        self.file_manager = file_manager
        self.monitor = monitor

    def download(self, dataset_name: str, permitted_attempts = 3):
        base_path = self.requester.base_path_for(dataset_name)
        self.create_path(base_path)
        download_links = self.requester.get_links_for(dataset_name)
        self.monitor.info(
            f"downloading {self.requester.download_target(dataset_name)} : {len(download_links)} files.")
        successful = False
        for i in range(permitted_attempts):
            try:
                for (link_index, link) in enumerate(download_links):
                    self.attempt_download(dataset_name, link_index, link)
                self.monitor.info('completed download')
                successful = True
                break
            except TimeoutError:
                self.monitor.warn("retrying after attempt {i}")
                continue
        if not successful:
            self.monitor.error(f"failed to complete {dataset_name} download after {permitted_attempts} attempts")
            raise TimeoutError()

    def create_path(self, base_path):
        self.file_manager.create_path(base_path)

    def attempt_download(self, dataset_name, link_index, link):
        file_name = f"{dataset_name}{link_index:03}.gz"
        self.monitor.info(f"Downloading {file_name}")
        file_path = f"{self.requester.base_path_for(dataset_name)}/{file_name}"
        if self.file_manager.exists(file_path):
            self.monitor.info(f"skipping {file_path}")
            return
        start = datetime.datetime.now()
        code, content = self.requester.get_content_from(link)
        if code != 200:
            raise TimeoutError('Link expired')
        self.file_manager.write_content(file_path, content)
        end = datetime.datetime.now()
        self.monitor.debug(f"download duration for {file_name}: {end - start}")


def download(release_id, dataset_name, permitted_attempts=3):
    monitor = LoggingMonitor()
    downloader = DatasetDownloader(WebDownloadRequester(release_id, monitor), FileManager(monitor), monitor)
    downloader.download(dataset_name, permitted_attempts)
