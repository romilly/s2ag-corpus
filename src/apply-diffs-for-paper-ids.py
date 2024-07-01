import os

from s2ag_corpus.database_catalogue import production_connection
from s2ag_corpus.diffs.apply_diffs import ApplyDiffs
from s2ag_corpus.logging_monitor import LoggingMonitor

dataset_name = 'paper-ids'
release_id = '2024-06-25'
connection = production_connection()
monitor = LoggingMonitor()
BASE_DIR = os.getenv('BASE_DIR')
diff_directory = os.path.join(BASE_DIR, 'diffs')

applicator = ApplyDiffs(connection, monitor, diff_directory)
applicator.apply_diffs_for(release_id, dataset_name)

