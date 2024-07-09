import csv

from s2ag_corpus.database.database_catalogue import local_connection
from s2ag_corpus.diffs.apply_diffs import DiffApplicator
from s2ag_corpus.synchronisation.config import SyncConfig
from s2ag_corpus.helpers.mock_monitor import MockMonitor

CREATE_CITATIONS = """
create table public.citations (
  citationid bigint primary key not null,
  citingcorpusid integer not null,
  citedcorpusid integer,
  isinfluential boolean,
  contexts text,
  intents text
);
create index citations_citationid_index on citations using btree (citationid);
create index citations_citedcorpusid_index on citations using btree (citedcorpusid);
create index citations_citingcorpusid_index on citations using btree (citingcorpusid);
"""


def create_empty_paperids_table(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists citations')
    cursor.execute(CREATE_CITATIONS)
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
    query = "SELECT * FROM citations ORDER BY citationid"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def test_diffs():
    connection = local_connection()
    create_empty_paperids_table(connection)
    monitor = MockMonitor()
    config = SyncConfig(base_dir='test/s2ag_corpus/data/',
                        monitor=monitor,
                        connection=connection)
    applier = DiffApplicator(config)
    count = applier.apply_diff_for('2024-06-25', 'citations')
    assert count == 20
    connection.close()
    assert len(monitor.infos) == 3
    assert len(monitor.debugs) == 1




