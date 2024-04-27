import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.json_file_inserter import JsonFileInserter

from s2ag_corpus.sql import CREATE_CITATIONS_TABLE_WITHOUT_INDICES

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_file = base_dir+'/test-data/e2e/citations1000'
dataset = DATASETS['citations']

def drop_and_replace_citations_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists citations')
        cursor.execute(CREATE_CITATIONS_TABLE_WITHOUT_INDICES)
        connection.commit()


def test_copy_json_to_citations_table():
    drop_and_replace_citations_table()
    check_papers_count(0)
    inserter = JsonFileInserter(test_file, dataset, connection)
    inserter.copy_json_to_table()
    check_papers_count(1000)
    connection.close()


def check_papers_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from citations')
        papers = cursor.fetchall()
        assert len(papers) == i
