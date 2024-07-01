import requests
import os
from dotenv import load_dotenv

from s2ag_corpus.monitor import Monitor

load_dotenv()
api_key = os.getenv('S2_API_KEY')
HEADERS = {"x-api-key": api_key}
BASE_DIR = os.getenv('BASE_DIR')
BASE_URL = "https://api.semanticscholar.org/datasets/v1/diffs"


def download_diffs_for(start_release_id: str, end_release_id: str, dataset_name: str, monitor: Monitor):
    url = f"{BASE_URL}/{start_release_id}/to/{end_release_id}/{dataset_name}"
    response = requests.get(url, headers=HEADERS)
    diffs = response.json()['diffs']
    diff_dir = f"{BASE_DIR}/diffs/{end_release_id}/{dataset_name}"
    os.makedirs(diff_dir, exist_ok=True)
    for diff in diffs:
        for file_type in ['update_files', 'delete_files']:
            links = diff[file_type]
            monitor.info(f"downloading {file_type}: {len(links)} files")
            for (index, link) in enumerate(links):
                response = requests.get(link, headers=HEADERS)
                file_name = f"{file_type}-{index:03}.gz"
                file_path = f"{diff_dir}/{file_name}"
                if os.path.exists(file_path):
                    monitor.info(f"Skipping {file_name}")
                    continue
                with open(file_path,"wb") as uf:
                    uf.write(response.content)
                    monitor.info(f'writing {file_name}')




