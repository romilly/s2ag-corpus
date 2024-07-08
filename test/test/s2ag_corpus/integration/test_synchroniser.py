import shutil

import pytest

from s2ag_corpus.database.database_catalogue import local_connection
from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.synchronisation.synchronizer import Synchronizer
from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor
from test.test.s2ag_corpus.helpers.mock_requester import MockDownloadRequester


@pytest.fixture(scope="function")
def test_config():
    base_dir = 'test/s2ag_corpus/data/generated'
    monitor: MockMonitor = MockMonitor()
    filemanager = FileManager(monitor)
    requester = MockDownloadRequester(base_dir=base_dir, links=[], diff_links=[], responses=[],
                                      latest_release_id='2024-06-18')
    config = SyncConfig(base_dir,
                        connection=local_connection(),
                        monitor=monitor,
                        requester=requester,
                        filemanager=filemanager)
    drop_all_test_tables(config.connection)
    shutil.rmtree(config.datasets_dir, ignore_errors=True)
    shutil.rmtree(config.diffs_dir, ignore_errors=True)
    yield config
    config.connection.close()


def drop_all_test_tables(connection):
    cursor = connection.cursor()
    for dataset in DATASETS.values():
        cursor.execute(f"DROP TABLE IF EXISTS {dataset.table}")

def test_synchroniser_downloads_and_loads_datasets_on_first_run(test_config):
    synchroniser = Synchronizer(test_config)
    synchroniser.synchronise()
    monitor: MockMonitor = test_config.monitor
    for name, dataset in DATASETS.items():
        assert f"downloading 2024-06-18/{name} : 0 files." in monitor.infos
        assert f"starting to index {dataset.table}" in monitor.infos
        assert f"finished indexing {dataset.table}" in monitor.infos


def test_synchroniser_does_nothing_if_up_to_date(test_config):
    synchroniser = Synchronizer(test_config)
    synchroniser.synchronise()
    synchroniser.synchronise()
    monitor: MockMonitor = test_config.monitor
    assert 'diffs are up to date' in monitor.infos

def test_synchroniser_dowloads_and_applies_diffs(test_config):
    synchroniser = Synchronizer(test_config)
    synchroniser.synchronise()
    test_config.requester.latest_release_id = '2024-06-25'
    synchroniser.synchronise()
    # TODO: add tests!
    monitor: MockMonitor = test_config.monitor
    monitor.dump()


