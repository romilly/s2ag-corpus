import shutil
from typing import List, Optional

import pytest

from s2ag_corpus.api import S2API
from s2ag_corpus.database.database_catalogue import local_connection
from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.helpers.file_manager import FileManager
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.synchronisation.synchronizer import Synchronizer
from test.test.s2ag_corpus.helpers.mock_requester import MockRequester, MockResponse
from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor


RELEASE_URL = "https://api.semanticscholar.org/datasets/v1/release/"
GENERIC_DATASET_URL = r'https://api.semanticscholar.org/datasets/v1/release/2024-06-18/dataset/[a-z\-]*'
GENERIC_DIFF_URL = 'https://api.semanticscholar.org/datasets/v1/diffs/.*'


def diff(from_release: str, to_release: str, update_files: List[str], delete_files: List[str]) -> dict:
    return {
        'from_release': from_release,
        'to_release': to_release,
        'update_files': update_files,
        'delete_files': delete_files
    }


def diffs(dataset_name: str, start_release: str, end_release: str, diffs: Optional[List[dict]] = None) -> dict:
    return {
        "dataset": dataset_name,
        "start_release": start_release,
        "end_release": end_release,
        "diffs": diffs or []
    }


def mock_diffs_for(dataset_name:str):
    return MockResponse(200,
                 diffs(
                     dataset_name,
                     '2024-06-18',
                     '2024-06-25',
                     [diff(
                         '2024-06-18',
                         '2024-06-25',
                         [],
                         []
                     )]))


ALL_TEST_DIFFS = { dataset: mock_diffs_for(dataset) for dataset in DATASETS.keys()}



@pytest.fixture(scope="function")
def test_config():
    base_dir = 'test/s2ag_corpus/data/generated'
    monitor: MockMonitor = MockMonitor()
    filemanager = FileManager(monitor)
    response = MockResponse(200, ['2024-06-18'])
    empty_list = MockResponse(200, {"files" :[]})
    response_map = {
        RELEASE_URL: response,
        GENERIC_DATASET_URL: empty_list,
    }
    for dataset_name in DATASETS.keys():
        url = f"https://api.semanticscholar.org/datasets/v1/diffs/2024-06-18/to/2024-06-25/{dataset_name}"
        response_map[url] = ALL_TEST_DIFFS[dataset_name]

    requester = MockRequester(response_map)
    api: S2API = S2API(monitor, requester)
    config = SyncConfig(base_dir,
                        connection=local_connection(),
                        monitor=monitor,
                        api=api,
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


def test_synchronizer_downloads_and_loads_datasets_on_first_run(test_config):
    synchronizer = Synchronizer(test_config)
    synchronizer.synchronize()
    monitor: MockMonitor = test_config.monitor
    for name, dataset in DATASETS.items():
        assert f"downloading 2024-06-18/{name} : 0 files." in monitor.infos
        assert f"starting to index {dataset.table}" in monitor.infos
        assert f"finished indexing {dataset.table}" in monitor.infos


def test_synchronizer_does_nothing_if_up_to_date(test_config):
    synchronizer = Synchronizer(test_config)
    synchronizer.synchronize()
    synchronizer.synchronize()
    monitor: MockMonitor = test_config.monitor
    assert 'diffs are up to date' in monitor.infos


def test_synchronizer_downloads_and_applies_diffs(test_config):
    synchronizer = Synchronizer(test_config)
    synchronizer.synchronize()
    test_config.api.requester.upsert(RELEASE_URL,MockResponse(200,['2024-06-18', '2024-06-25']))
    synchronizer.synchronize()
    monitor: MockMonitor = test_config.monitor
    assert 'diffs are up to date' not in monitor.infos
    monitor.dump()


