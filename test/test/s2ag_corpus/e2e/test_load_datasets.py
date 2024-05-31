import os
import gzip
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.import_dataset import insert_dataset

load_dotenv()
base_dir = os.getenv("BASE_DIR")
test_dir = base_dir+'/test-data/e2e'


def drop_table(table_name: str, connection):
    with connection.cursor() as cursor:
        cursor.execute(f'drop table if exists {table_name}')
        connection.commit()


def test_copy_json_to_table():
    connection = local_connection()
    for dataset_name in sorted(DATASETS.keys()):
        table = DATASETS[dataset_name].table
        drop_table(table, connection)
        insert_dataset(dataset_name, test_dir, connection)
        check_table_count(count_total_lines(f"{test_dir}/{dataset_name}"), table, connection)
    connection.close()


def check_table_count(i, table_name, connection):
    with connection.cursor() as cursor:
        cursor.execute(f'select * from {table_name}')
        papers = cursor.fetchall()
        assert len(papers) == i



def count_total_lines(directory):
    total_lines = 0
    # Walk through all files and subdirectories in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith('.gz'):
                    # Open gzipped files with gzip module
                    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                        for line in f:
                            total_lines += 1
                else:
                    # Open regular text files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            total_lines += 1
            except Exception as e:
                # Handle cases where file may be unreadable or a binary file
                print(f"Could not read file {file_path}: {e}")
    return total_lines





