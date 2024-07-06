import csv
import gzip
import os
from io import StringIO

from s2ag_corpus.datasets.dataset_definitions import DATASETS, Dataset
from s2ag_corpus.helpers.monitor import Monitor


# TODO: Use SyncConfig as source of connection, monitor
def insert_dataset(dataset_name, datasets_dir, connection, monitor: Monitor):
    data_dir = f"{datasets_dir}/{dataset_name}"
    dataset = DATASETS[dataset_name]
    inserter = JsonFileInserter(dataset, connection, monitor)
    inserter.create_table()
    for source_file in sorted(os.listdir(data_dir)):
        full_path = f"{data_dir}/{source_file}"
        monitor.info(f"inserting into {dataset.table} from {full_path}")
        inserter.copy_json_to_table(full_path)
    inserter.index_table()


class JsonFileInserter:
    def __init__(self, dataset: Dataset, connection, monitor: Monitor):
        self.dataset = dataset
        self.connection = connection
        self.monitor = monitor
        self.generator = None
        self.buffer = ''
        self.count = 0

    def read_records_from_file(self, input_file):
        """A generator function that returns reformatted lines in a file."""
        output = StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        for line in input_file:
            line = line.strip()
            record = self.dataset.json_to_tuple(line)
            output.seek(0)
            output.truncate(0)
            writer.writerow(record)
            self.count += 1
            if self.count % 1000000 == 0:
                self.monitor.debug('loaded {self.count}')
            yield output.getvalue()

    def read(self, size=-1):
        # Fill the buffer to meet the size requirement or if size is -1 then try to exhaust the generator
        while (size < 0 or len(self.buffer) < size) and (chunk := next(self.generator, None)) is not None:
            self.buffer += chunk
        if size < 0 or len(self.buffer) <= size:
            to_return, self.buffer = self.buffer, ''
        else:
            to_return, self.buffer = self.buffer[:size], self.buffer[size:]
        return to_return

    def copy_json_to_table(self, file_path):
        self.monitor.info(f"Copying json file {file_path} to table {self.dataset.table}")
        # Use a gzip reader if the file is zipped
        if file_path.endswith('.gz'):
            input_file = gzip.open(file_path, 'rt')
        else:
            input_file = open(file_path,'rt')
        with input_file:
            self.generator = self.read_records_from_file(input_file)
            with self.connection.cursor() as cursor:
                cursor.copy_from(self, self.dataset.table, sep=',', null='')
                self.connection.commit()
        self.monitor.info('done')

# TODO: move the body of these to DatabaseCatalogue
    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.dataset.create_table)
            self.connection.commit()

    def index_table(self):
        self.monitor.info(f'starting to index {self.dataset.table}')
        with self.connection.cursor() as cursor:
            cursor.execute(self.dataset.add_indices)
            self.connection.commit()
        self.monitor.info(f'finished indexing {self.dataset.table}')

