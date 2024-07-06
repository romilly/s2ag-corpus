import os

from dotenv import load_dotenv

from s2ag_corpus.database.database_catalogue import production_connection
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.helpers.logging_monitor import LoggingMonitor
from s2ag_corpus.requester import WebDownloadRequester
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.synchronisation.synchronizer import Synchronizer


def synchronise():
    load_dotenv()
    connection = production_connection()
    base_dir = os.getenv('BASE_DIR')
    monitor = LoggingMonitor()
    requester = WebDownloadRequester(monitor)
    filemanager = FileManager(monitor)
    config = SyncConfig(base_dir, connection, monitor, requester, filemanager)
    synchronizer = Synchronizer(config)
    synchronizer.synchronise()