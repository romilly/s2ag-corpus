from s2ag_corpus.api import S2API
from s2ag_corpus.requester.requester import ThrottledRequester
from s2ag_corpus.helpers.mock_monitor import MockMonitor


def test_api_finds_latest_release_id():
    monitor = MockMonitor()
    requester = S2API(monitor, ThrottledRequester())
    latest_release_id = requester.find_latest_release_id()
    assert len(latest_release_id) == 10