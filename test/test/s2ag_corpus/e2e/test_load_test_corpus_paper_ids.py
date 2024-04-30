import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.import_dataset import insert_dataset

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_dir = base_dir+'/test-data/e2e'
dataset = DATASETS['paper-ids']


def drop_paper_ids_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists paperids')
        connection.commit()


def test_copy_json_to_paper_ids():
    drop_paper_ids_table()
    insert_dataset('paper-ids', test_dir,connection)
    check_paper_ids_count(100)
    connection.close()


def check_paper_ids_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from paperids')
        papers = cursor.fetchall()
        assert len(papers) == i