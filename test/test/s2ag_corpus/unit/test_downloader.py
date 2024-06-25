from s2ag_corpus.download_dataset import DatasetDownloader
from test.test.s2ag_corpus.helpers.mock_file_manager import MockFileManager

from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor
from test.test.s2ag_corpus.helpers.mock_requester import MockDownloadRequester


def test_dataset_downloader():
    dataset = 'gubbins'
    release_id = '2021-01-01'
    requester = MockDownloadRequester(f'{release_id}/{dataset}',
                                      'some_path',
                                      links = [
                                          'http://example.com/a',
                                          'http://example.com/b',
                                          'http://example.com/c',
                                      ],
                                      responses = [
                                          b'content of a',
                                          b'content of b',
                                          b'',
                                          b'content of c',
                                      ])
    file_manager = MockFileManager()
    monitor = MockMonitor()
    downloader = DatasetDownloader(requester, file_manager, monitor)
    downloader.download(dataset)
    assert file_manager.files == {
        'some_path/gubbins000.gz': b'content of a',
        'some_path/gubbins001.gz': b'content of b',
        'some_path/gubbins002.gz': b'content of c'
    }