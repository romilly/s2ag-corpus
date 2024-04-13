import os
import requests
from dotenv import load_dotenv

# Define base URL for datasets API
base_url = "https://api.semanticscholar.org/datasets/v1/release/"


load_dotenv()
api_key = os.getenv('S2_API_KEY')
headers = {"x-api-key": api_key}
base_dir = os.getenv('BASE_DIR')

def download(release_id: str, dataset_name: str):
    download_links_response = requests.get(base_url + release_id + '/dataset/' + dataset_name, headers=headers)
    if download_links_response.status_code != 200:
        raise Exception(f"downloading links: status code {download_links_response.status_code}")
    download_links = download_links_response.json()["files"]
    print(f"about to download{release_id} of {dataset_name}: {len(download_links)} files.")
    for (i, link) in enumerate(download_links):
        file_name = f"{base_dir}/{release_id}-{dataset_name}{i}.gz"
        print(f"Downloading {file_name}")
        response = requests.get(link)
        if response.status_code != 200:
            break
        with open(f"{base_dir}/{release_id}-{dataset_name}{i}.gz","wb") as pf:
            pf.write(response.content)


