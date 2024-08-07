import os
import sys

from dotenv import load_dotenv

from s2ag_corpus.database.database_catalogue import production_connection
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.helpers.logging_monitor import LoggingMonitor
from s2ag_corpus.api import S2API
from s2ag_corpus.requester.requester import ThrottledRequester
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.synchronisation.synchronizer import Synchronizer


def synchronize():
    force_download = (len(sys.argv) > 1 and sys.argv[1] == 'force')
    load_dotenv()
    connection = production_connection()
    base_dir = os.getenv('BASE_DIR')
    monitor = LoggingMonitor()
    filemanager = FileManager(monitor)
    api = S2API(monitor, requester = ThrottledRequester())
    config = SyncConfig(base_dir, connection, monitor, api, filemanager)
    synchronizer = Synchronizer(config)
    synchronizer.synchronize(force_download)

synchronize()