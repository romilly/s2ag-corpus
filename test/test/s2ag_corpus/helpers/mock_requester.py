import re

from s2ag_corpus.requester.requester import Requester


class MockResponse:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class MockRequester(Requester):
    def __init__(self, response_map = None):
        self.response_map: dict[str, MockResponse] = response_map or {}

    def post(self, url: str, ids: dict):
        raise NotImplementedError()

    def get(self, url: str) -> MockResponse:
        for key, value in self.response_map.items():
            if re.fullmatch(key, url):
                return value
        raise KeyError(f"No match found for {url}")

    def upsert(self, url: str, response: MockResponse):
        self.response_map[url] = response

