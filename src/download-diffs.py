import os

from dotenv import load_dotenv

from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.diffs.download_diff import download_diffs_for

load_dotenv()
api_key = os.getenv('S2_API_KEY')
HEADERS = {"x-api-key": api_key}
BASE_DIR = os.getenv('BASE_DIR')

BASE_URL = "https://api.semanticscholar.org/datasets/v1/diffs"
start_release_id = "2024-06-18"
end_release_id = "2024-06-25"

for dataset_name in DATASETS.keys():
    download_diffs_for(start_release_id, end_release_id, dataset_name)