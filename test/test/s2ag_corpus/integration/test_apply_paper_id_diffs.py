import csv

from s2ag_corpus.database.database_catalogue import local_connection
from s2ag_corpus.diffs.apply_diffs import DiffApplicator
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.helpers.mock_monitor import MockMonitor

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
    csv_file_path = "test/s2ag_corpus/data/initial-diff-data-for-test-db.csv"
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
    monitor = MockMonitor()
    config = SyncConfig(base_dir='test/s2ag_corpus/data/',
                        monitor=monitor,
                        connection=connection)
    applier = DiffApplicator(config)
    count = applier.apply_diff_for('2024-04-02', 'paper-ids')
    expected = read_csv_file('test/s2ag_corpus/data/expected/expected-table-contents.csv')
    actual = fetch_data(connection)
    assert count == 6
    connection.close()
    for e,a in zip(expected, actual):
        assert e == a
    assert len(monitor.infos) == 4
    assert len(monitor.debugs) == 2




