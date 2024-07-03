from typing import List, Tuple

from s2ag_corpus.datasets.download_dataset import DownloadRequester


class MockDownloadRequester(DownloadRequester):
    def diff_links(self, dataset_name, start_release_id, end_release_id):
        return

    def __init__(self, target: str,
                 base_path: str,
                 links: List[str],
                 diff_links: List[str],
                 responses: List[bytes]):
        self.target = target
        self.base_path = base_path
        self.links = links
        self.diff_links = diff_links
        self.responses = responses

    def get_links_for(self, dataset_name):
        return self.links

    def get_content_from(self, link) -> Tuple[int, bytes]:
        content = self.responses.pop(0)
        code = 404 if len(content) == 0 else 200
        return code, content

    def download_target(self, dataset_name) -> str:
        return self.target

    def base_path_for(self, dataset_name):
        return self.base_path