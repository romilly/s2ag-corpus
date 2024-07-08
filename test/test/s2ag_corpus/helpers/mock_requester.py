import json
from typing import Optional

from s2ag_corpus.requester.requester import Requester


class MockRequester(Requester):
    def post(self, url: str, ids: dict) -> dict:
        pass

    def get(self, url: str, parameters: Optional[str] = None) -> dict:
        pass

