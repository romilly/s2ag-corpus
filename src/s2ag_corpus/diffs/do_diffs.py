import os

from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.diffs.apply_diffs import DiffApplicator
from s2ag_corpus.synchronisation.config import SyncConfig


def do_diffs_for(start_release_id: str,
                 end_release_id: str,
                 dataset_name: str,
                 config: SyncConfig):
    requester = config.api
    diffs = requester.diff_links(start_release_id, end_release_id, dataset_name)
    applicator = DiffApplicator(config)
    for diff in diffs:
        download_diff(config, dataset_name, diff)
        applicator.apply_diff_for(diff['to_release'], dataset_name)



def download_diff(config, dataset_name, diff):
    monitor = config.monitor
    requester = config.api
    filemanager = config.filemanager
    from_release = diff['from_release']
    to_release = diff['to_release']
    this_diff_dir = f"{config.diffs_dir}/{to_release}/{dataset_name}"
    monitor.info(f"Downloading diff from {from_release} to {to_release} into {this_diff_dir}")
    os.makedirs(this_diff_dir, exist_ok=True)
    for file_type in ['update_files', 'delete_files']:
        links = diff[file_type]
        monitor.info(f"downloading {file_type}: {len(links)} files")
        for (index, link) in enumerate(links):
            code, content = requester.get_content_from(link)
            if code != 200:
                raise TimeoutError('Link expired')
            file_name = f"{file_type}-{index:03}.gz"
            file_path = f"{this_diff_dir}/{file_name}"
            if filemanager.exists(file_path):
                monitor.info(f"Skipping {file_name}")
                continue
            filemanager.write_content(file_path, content)
            monitor.info(f'writing {file_name}')


def download_and_apply_all_diffs_for(start_release_id, end_release_id, config: SyncConfig):
    for dataset_name in DATASETS.keys():
        monitor = config.monitor
        monitor.info(f"downloading and applying diffs from {start_release_id} to {end_release_id} for {dataset_name}")
        do_diffs_for(start_release_id, end_release_id, dataset_name, config)