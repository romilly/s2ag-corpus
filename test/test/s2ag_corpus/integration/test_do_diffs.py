import pytest

from s2ag_corpus.database.database_catalogue import local_connection
from s2ag_corpus.diffs.do_diffs import do_diffs_for
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.api import S2API
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.helpers.mock_monitor import MockMonitor


@pytest.mark.skip(reason="Currently very slow (37 sec)")
def test_do_diffs():
    base_dir = 'test/s2ag_corpus/data/generated'
    connection = local_connection()
    monitor = MockMonitor()
    requester = S2API(monitor)
    filemanager = FileManager(monitor)
    config = SyncConfig(base_dir, connection, monitor, requester, filemanager)
    start_release_id = '2024-06-18'
    end_release_id = '2024-06-25'
    dataset_name = 'paper-ids'
    do_diffs_for(start_release_id, end_release_id, dataset_name, config)


