import os

from dotenv import load_dotenv

from s2ag_corpus.database.database_catalogue import production_connection
from s2ag_corpus.datasets.download_datasets import DatasetDownloader
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.helpers.logging_monitor import LoggingMonitor
from s2ag_corpus.api import S2API
from s2ag_corpus.synchronisation.config import SyncConfig


def test_download():
    load_dotenv()
    connection = production_connection()
    base_dir = "test/s2ag_corpus/data/download_test"
    monitor = LoggingMonitor()
    requester = S2API(monitor)
    filemanager = FileManager(monitor)
    config = SyncConfig(base_dir, connection, monitor, requester, filemanager)
    downloader = DatasetDownloader(config)
    downloader.download('2024-07-02', 'publication-venues')


