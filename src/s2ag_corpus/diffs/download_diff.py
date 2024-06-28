import os

from dotenv import load_dotenv
import requests

from s2ag_corpus.datasets import DATASETS

load_dotenv()
api_key = os.getenv('S2_API_KEY')
HEADERS = {"x-api-key": api_key}
BASE_DIR = os.getenv('BASE_DIR')

BASE_URL = "https://api.semanticscholar.org/datasets/v1/diffs"
start_release_id = "2024-04-02"
end_release_id = "2024-04-09"
dataset_name = "authors"


def download_diffs_for(start_release_id: str, end_release_id: str, dataset_name: str):
    url = f"{BASE_URL}/{start_release_id}/to/{end_release_id}/{dataset_name}"
    response = requests.get(url, headers=HEADERS)
    diffs = response.json()['diffs']
    diff_dir = f"{BASE_DIR}/diffs/{end_release_id}/{dataset_name}"
    os.makedirs(diff_dir, exist_ok=True)
    for diff in diffs:
        for file_type in ['update_files', 'delete_files']:
            links = diff[file_type]
            for (index, link) in enumerate(links):
                response = requests.get(link, headers=HEADERS)
                file_name = f"{file_type}-{index:03}.gz"
                file_path = f"{diff_dir}/{file_name}"
                if os.path.exists(file_path):
                    print(f"Skipping {file_name}")
                    continue
                with open(file_path,"wb") as uf:
                    uf.write(response.content)


for dataset_name in DATASETS.keys():
    download_diffs_for(start_release_id, end_release_id, dataset_name)




