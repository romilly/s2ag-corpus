import os
from dotenv import load_dotenv

class Synchronise:

    def __init__(self):
        load_dotenv()
        self.base_dir = os.getenv('BASE_DIR')
        self.datasets_dir = os.path.join(self.base_dir, 'datasets')
        self.diffs_dir = os.path.join(self.base_dir, 'diffs')

    def find_latest_release_id(self):
        # implementation of the method to find latest release id
        raise NotImplementedError("find_latest_release_id method is not implemented")

    def download_datasets(self, download_path):
        # implementation of the method to download datasets
        raise NotImplementedError("download_datasets method is not implemented")

    def load_datasets_to_database(self, datasets_path):
        # implementation of the method to load dataset to database
        raise NotImplementedError("load_datasets_to_database method is not implemented")

    def download_diffs(self, download_path, from_release_id, to_release_id):
        # implementation of the method to download diffs
        raise NotImplementedError("download_diffs method is not implemented")

    def apply_diffs(self, diffs_path):
        # implementation of the method to apply diffs
        raise NotImplementedError("apply_diffs method is not implemented")

    def synchronise(self):
        latest_release_id = self.find_latest_release_id()

        if not os.path.isdir(self.datasets_dir):
            # create a datasets directory
            os.makedirs(self.datasets_dir)

            # download the datasets
            self.download_datasets(self.datasets_dir)

            # load the datasets into the database
            self.load_datasets_to_database(self.datasets_dir)

        if os.path.isdir(self.diffs_dir):
            # find release_id of original dataset download
            original_release_id = self.find_latest_local_release_id()

            # download the diffs
            self.download_diffs(self.diffs_dir, original_release_id, latest_release_id)

            # apply each set of diffs
            self.apply_diffs(self.diffs_dir)