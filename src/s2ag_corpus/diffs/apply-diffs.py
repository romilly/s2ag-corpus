import csv
import gzip
import json

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import Dataset, DATASETS

connection = local_connection()

CREATE_PAPERIDS = """
create table if not exists paperids
(
    sha        text    not null
        constraint paperids_pk
            unique,
    corpusid   text    not null,
    is_primary boolean not null
)"""

cursor = connection.cursor()
cursor.execute('drop table if exists paperids')
cursor.execute(CREATE_PAPERIDS)
connection.commit()

csv_file_path = "/home/romilly/git/active/s2ag-corpus/data/diffs/initial-diff-data-for-test-db.csv"
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        cursor.execute(
            f"INSERT INTO paperids (sha, corpusid, is_primary) VALUES (%s, %s, %s)",
            row
        )
connection.commit()

def upsert(connection, dataset: Dataset, path_to_file):
    cursor = connection.cursor()
    with gzip.open(path_to_file, 'rt') as upsert_file:
        for (index, line) in enumerate(upsert_file):
            row = dataset.json_to_tuple(line)
            cursor.execute(dataset.upsert, row)
            if 0 == index % 10000:
                connection.commit()
        connection.commit()


upsert(connection, DATASETS['paper-ids'], '/home/romilly/git/active/s2ag-corpus/data/diffs/update_files-000.gz')


def delete_rows(connection, dataset, path_to_file):
    with gzip.open(path_to_file, 'rt') as upsert_file:
        for (index, line) in enumerate(upsert_file):
            key = json.loads(line)[dataset.primary_key]
            cursor.execute(dataset.delete_row, (key,))
            if 0 == index % 10000:
                connection.commit()
        connection.commit()


delete_rows(connection, DATASETS['paper-ids'], 
            '/home/romilly/git/active/s2ag-corpus/data/diffs/delete_files-000.gz')

def read_csv_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        data = [(sha, corpusid, is_primary in ['True', 'true']) for sha, corpusid, is_primary in data]
        data.sort(key=lambda x: x[0])
        return data


expected = read_csv_file('/home/romilly/git/active/s2ag-corpus/data/diffs/expected-table-contents.csv')

def fetch_data(cursor):
    query = "SELECT * FROM paperids ORDER BY sha"
    cursor.execute(query)
    return cursor.fetchall()


actual = fetch_data(cursor)


for e,a in zip(expected, actual):
    if e != a:
        print(f"{e} != {a}")




