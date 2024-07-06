import os
from typing import List, Tuple
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv

from s2ag_corpus.helpers.monitor import Monitor

# TODO: change signatures
class DownloadRequester(ABC):

    def base_path_for(self, release_id, dataset_name) -> str:
        return f"{self.base_dir}/datasets/{release_id}/{dataset_name}"

    @abstractmethod
    def get_links_for(self, release_id, dataset_name) -> List[str]:
        pass

    @abstractmethod
    def get_content_from(self, link) -> Tuple[int, bytes]:
        pass

    @abstractmethod
    def diff_links(self, start_release_id, end_release_id, dataset_name):
        pass

    @abstractmethod
    def find_latest_release_id(self) -> str:
        pass

    def download_target(self, release_id, dataset_name) -> str:
        return f"{release_id}/{dataset_name}"


class WebDownloadRequester(DownloadRequester):
    def __init__(self, monitor: Monitor) -> None:
        self.monitor = monitor
        load_dotenv()
        self.base_url = "https://api.semanticscholar.org/datasets/v1/"
        self.api_key = os.getenv('S2_API_KEY')
        self.headers = {"x-api-key": self.api_key}
        self.base_dir = os.getenv('BASE_DIR')

    def find_latest_release_id(self) -> str:
        response = requests.get(f"{self.base_url}/release/")
        if response.status_code != 200:
            raise Exception("could not download releases")
        return response.json()[-1]

    def url_for_downloads_of(self, release_id, dataset_name):
        return f"{self.base_url}/release/{release_id}/dataset/{dataset_name}"

    def get_links_for(self, release_id, dataset_name) -> List:
        url = self.url_for_downloads_of(release_id, dataset_name)
        self.monitor.info("downloading links for {release_id}-{dataset_name} from {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"could not download links for {release_id}-{dataset_name}: status code {response.status_code}")
        download_links = response.json()["files"]
        return download_links

    def diff_links(self, start_release_id, end_release_id, dataset_name):
        url = f"{self.base_url}diffs/{start_release_id}/to/{end_release_id}/{dataset_name}"
        response = requests.get(url, headers=self.headers)
        diffs = response.json()['diffs']
        return diffs

    def get_content_from(self, link: str) -> Tuple[int, bytes]:
        response = requests.get(link)
        if response.status_code != 200:
            self.monitor.warn(f"could not download from {link}")
            content = b''
        else:
            content = response.content
        return response.status_code, content
