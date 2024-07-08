import json
from typing import Optional

from s2ag_corpus.requester.requester import Requester


class MockRequester(Requester):
    def get(self, url: str, parameters: Optional[str] = None) -> dict:
        pass

    def get_citation_items(self):
        pass

    def __init__(self):
        self.papers = {}

    def add_paper(self, pid: str, text: str):
        self.papers[pid] = text

    def get_paper_json(self, pid) -> dict:
        return json.loads(self.papers[pid])
