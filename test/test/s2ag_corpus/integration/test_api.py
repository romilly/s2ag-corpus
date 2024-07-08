from s2ag_corpus.api import S2API
from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor


def test_api_finds_latest_release_id():
    monitor = MockMonitor()
    requester = S2API(monitor)
    latest_release_id = requester.find_latest_release_id()
    assert len(latest_release_id) == 10