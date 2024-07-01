import os

from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import production_connection
from s2ag_corpus.diffs.apply_diffs import ApplyDiffs
from s2ag_corpus.logging_monitor import LoggingMonitor

def apply_diffs_for_dataset(dataset_name, release_id):
    connection = production_connection()
    monitor = LoggingMonitor()

    load_dotenv()
    BASE_DIR = os.getenv('BASE_DIR')
    diff_directory = os.path.join(BASE_DIR, 'diffs')

    applicator = ApplyDiffs(connection, monitor, diff_directory)
    applicator.apply_diffs_for(release_id, dataset_name)
