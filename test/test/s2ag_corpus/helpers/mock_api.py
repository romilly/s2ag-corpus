from typing import List, Tuple

from s2ag_corpus.api import AbstractAPI


class MockAPI(AbstractAPI):

    def __init__(self, base_dir: str, links: List[str], diff_links: List[str], responses: List[bytes],
                 latest_release_id: str):
        self.base_dir = base_dir
        self.links = links
        self._diff_links = diff_links
        self.responses = responses
        self.latest_release_id = latest_release_id

    def find_latest_release_id(self) -> str:
        return self.latest_release_id

    def diff_links(self, start_release_id, end_release_id, dataset_name):
        return self._diff_links

    def get_links_for(self, release_id, dataset_name):
        return self.links

    def get_content_from(self, link) -> Tuple[int, bytes]:
        content = self.responses.pop(0)
        code = 404 if len(content) == 0 else 200
        return code, content
