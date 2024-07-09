from s2ag_corpus.api import S2API
from s2ag_corpus.datasets.download_datasets import DatasetDownloader
from s2ag_corpus.synchronisation.config import SyncConfig
from test.test.s2ag_corpus.helpers.mock_requester import MockResponse
from test.test.s2ag_corpus.helpers.mock_requester import MockRequester
from test.test.s2ag_corpus.helpers.mock_file_manager import MockFileManager

from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor


def test_dataset_downloader():
    dataset = 'gubbins'
    release_id = '2021-01-01'
    base_dir = 'some_path'
    # api = MockAPI(base_dir=base_dir, links=[
    #     'http://example.com/a',
    #     'http://example.com/b',
    #     'http://example.com/c',
    # ], diff_links=[], responses=[
    #     b'content of a',
    #     b'content of b',
    #     b'',
    #     b'content of c',
    # ], latest_release_id='does not matter')
    dataset_response = MockResponse(
        200, {
            'files': [
            'http://example.com/a',
            'http://example.com/b',
            'http://example.com/c',
            ]
        }
    )
    requester = MockRequester(
        {
            'https://api.semanticscholar.org/datasets/v1/release/2021-01-01/dataset/gubbins' : dataset_response,
            'http://example.com/a' : MockResponse(200,b'content of a'),
            'http://example.com/b' : [
                MockResponse(429,b'who cares?'),
                MockResponse(200,b'content of b')
                ],
            'http://example.com/c' : MockResponse(200,b'content of c'),

        }
    )
    monitor = MockMonitor()
    api = S2API(monitor, requester)
    filemanager = MockFileManager()
    config = SyncConfig(base_dir,
                        api= api,
                        connection = None,
                        monitor=monitor,
                        filemanager=filemanager)
    downloader = DatasetDownloader(config)
    downloader.download(release_id, dataset)
    assert filemanager.files == {
        'some_path/datasets/2021-01-01/gubbins/gubbins000.gz': b'content of a',
        'some_path/datasets/2021-01-01/gubbins/gubbins001.gz': b'content of b',
        'some_path/datasets/2021-01-01/gubbins/gubbins002.gz': b'content of c'
    }