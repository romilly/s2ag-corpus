from typing import List, Tuple
from dotenv import load_dotenv

from s2ag_corpus.helpers.monitor import Monitor





class S2API:
    def __init__(self, monitor: Monitor, requester) -> None:
        self.monitor = monitor
        load_dotenv()
        self.requester = requester
        self.base_url = "https://api.semanticscholar.org/datasets/v1"

    def download_target(self, release_id, dataset_name) -> str:
        return f"{release_id}/{dataset_name}"

    def find_latest_release_id(self) -> str:
        response = self.requester.get(f"{self.base_url}/release/")
        if response.status_code != 200:
            raise Exception("could not download releases")
        return response.json()[-1]

    def url_for_downloads_of(self, release_id, dataset_name):
        return f"{self.base_url}/release/{release_id}/dataset/{dataset_name}"

    def get_links_for(self, release_id, dataset_name) -> List:
        url = self.url_for_downloads_of(release_id, dataset_name)
        self.monitor.info(f"downloading links for {release_id}-{dataset_name} from {url}")
        response = self.requester.get(url)
        self.monitor.info(f"got response {response.status_code}")
        if response.status_code != 200:
            raise Exception(f"could not download links for {release_id}-{dataset_name}: status code {response.status_code}")
        download_links = response.json()["files"]
        self.monitor.info(f"got {len(download_links)} links for {release_id}-{dataset_name}")
        return download_links

    def diff_links(self, start_release_id, end_release_id, dataset_name):
        url = f"{self.base_url}/diffs/{start_release_id}/to/{end_release_id}/{dataset_name}"
        response = self.requester.get(url)
        diffs = response.json()['diffs']
        return diffs

    def get_content_from(self, link: str) -> Tuple[int, bytes]:
        response = self.requester.get(link)
        if response.status_code != 200:
            self.monitor.warn(f"could not download from {link}")
            content = b''
        else:
            content = response.content
        return response.status_code, content


