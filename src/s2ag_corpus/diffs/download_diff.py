import requests
import os
from dotenv import load_dotenv

from s2ag_corpus.helpers.file_manager import AbstractFileManager
from s2ag_corpus.helpers.monitor import Monitor
from s2ag_corpus.requester import DownloadRequester

load_dotenv()
api_key = os.getenv('S2_API_KEY')
HEADERS = {"x-api-key": api_key}
BASE_DIR = os.getenv('BASE_DIR')
# BASE_URL = "https://api.semanticscholar.org/datasets/v1/diffs"


# TODO: add retry logic and integration test
def download_diffs_for(start_release_id: str,
                       end_release_id: str,
                       dataset_name: str,
                       requester: DownloadRequester,
                       monitor: Monitor,
                       file_manager: AbstractFileManager):
    diffs = requester.diff_links(dataset_name, start_release_id, end_release_id)
    diff_dir = f"{BASE_DIR}/diffs/{end_release_id}/{dataset_name}"
    os.makedirs(diff_dir, exist_ok=True)
    for diff in diffs:
        for file_type in ['update_files', 'delete_files']:
            links = diff[file_type]
            monitor.info(f"downloading {file_type}: {len(links)} files")
            for (index, link) in enumerate(links):
                code, content = requester.get_content_from(link)
                if code != 200:
                    raise TimeoutError('Link expired')
                file_name = f"{file_type}-{index:03}.gz"
                file_path = f"{diff_dir}/{file_name}"
                if file_manager.exists(file_path):
                    monitor.info(f"Skipping {file_name}")
                    continue
                file_manager.write_content(file_path, content)
                monitor.info(f'writing {file_name}')





