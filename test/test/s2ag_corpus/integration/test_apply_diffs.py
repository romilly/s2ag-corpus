import csv
import gzip
import json

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.diffs.apply_diffs import upsert, delete_rows

CREATE_PAPERIDS = """
create table if not exists paperids
(
    sha        text    not null
        constraint paperids_pk
            unique,
    corpusid   text    not null,
    is_primary boolean not null
)"""

def create_empty_paperids_table(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists paperids')
    cursor.execute(CREATE_PAPERIDS)
    connection.commit()
    cursor.close()

def populate_paperids_table(connection):
    csv_file_path = "/home/romilly/git/active/s2ag-corpus/data/diffs/initial-diff-data-for-test-db.csv"
    cursor = connection.cursor()
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cursor.execute(
                f"INSERT INTO paperids (sha, corpusid, is_primary) VALUES (%s, %s, %s)",
                row
            )
    connection.commit()
    cursor.close()


def read_csv_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        data = [(sha, corpusid, is_primary in ['True', 'true']) for sha, corpusid, is_primary in data]
        data.sort(key=lambda x: x[0])
        return data


def fetch_data(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM paperids ORDER BY sha"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def test_diffs():
    connection = local_connection()
    create_empty_paperids_table(connection)
    populate_paperids_table(connection)
    upsert(connection, DATASETS['paper-ids'], '/home/romilly/git/active/s2ag-corpus/data/diffs/update_files-000.gz')
    delete_rows(connection, DATASETS['paper-ids'],
            '/home/romilly/git/active/s2ag-corpus/data/diffs/delete_files-000.gz')

    expected = read_csv_file('/home/romilly/git/active/s2ag-corpus/data/diffs/expected-table-contents.csv')
    actual = fetch_data(connection)
    for e,a in zip(expected, actual):
        assert e == a
    connection.close()




