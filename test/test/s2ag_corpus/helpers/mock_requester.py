import re
from typing import Union, List, Any

from s2ag_corpus.requester.requester import Requester


class MockResponse:
    def __init__(self, status_code, contents: Any):
        self.status_code = status_code
        self._contents= contents

    def json(self):
        return self._contents

    @property
    def content(self):
        return self._contents


class MockRequester(Requester):
    def __init__(self, response_map: Union[List[MockResponse], MockResponse] = None):
        self.response_map = response_map or {}


    def get(self, url: str) -> MockResponse:
        for key, value in self.response_map.items():
            if re.fullmatch(key, url):
                if isinstance(value, MockResponse):
                    return value
                else:
                    return value.pop(0)
        raise KeyError(f"No match found for {url}")

    def upsert(self, url: str, response: Union[List[MockResponse], MockResponse]):
        self.response_map[url] = response

