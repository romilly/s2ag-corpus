import os
from typing import List, Tuple
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv

from s2ag_corpus.monitor import Monitor


class DownloadRequester(ABC):

    @abstractmethod
    def base_path_for(self, dataset_name) -> str:
        pass

    @abstractmethod
    def get_links_for(self, dataset_name) -> List[str]:
        pass

    @abstractmethod
    def get_content_from(self, link) -> Tuple[int, bytes]:
        pass

    @abstractmethod
    def download_target(self, dataset_name) -> str:
        pass


class WebDownloadRequester(DownloadRequester):
    def __init__(self, release_id: str, monitor: Monitor) -> None:
        self.release_id = release_id
        self.monitor = monitor
        load_dotenv()
        self.base_url = "https://api.semanticscholar.org/datasets/v1/release/"
        self.api_key = os.getenv('S2_API_KEY')
        self.headers = {"x-api-key": self.api_key}
        self.base_dir = os.getenv('BASE_DIR')

    def url_for_downloads_of(self, dataset_name):
        return f"{self.base_url}{self.release_id}/dataset/{dataset_name}"

    def download_target(self, dataset_name) -> str:
        return f"{self.release_id}/{dataset_name}"

    def base_path_for(self, dataset_name) -> str:
        return f"{self.base_dir}/datasets/{self.download_target(dataset_name)}"

    def get_links_for(self, dataset_name) -> List:
        response = requests.get(self.url_for_downloads_of(dataset_name),
                                headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"could not download links for {dataset_name}: status code {response.status_code}")
        download_links = response.json()["files"]
        return download_links

    def get_content_from(self, link: str) -> Tuple[int, bytes]:
        response = requests.get(link)
        if response.status_code != 200:
            self.monitor.warn(f"could not download from {link}")
            content = b''
        else:
            content = response.content
        return response.status_code, content
