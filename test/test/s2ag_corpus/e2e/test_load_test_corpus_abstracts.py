import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.import_dataset import insert_dataset

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_dir = base_dir+'/test-data/e2e'
dataset = DATASETS['abstracts']


def drop_paper_ids_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists abstracts')
        connection.commit()


def test_copy_json_to_paper_ids():
    drop_paper_ids_table()
    insert_dataset('abstracts', test_dir,connection)
    check_paper_ids_count(1000)
    connection.close()


def check_paper_ids_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from abstracts')
        papers = cursor.fetchall()
        assert len(papers) == i
