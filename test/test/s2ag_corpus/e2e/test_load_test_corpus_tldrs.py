import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.import_dataset import insert_dataset

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_dir = base_dir+'/test-data/e2e'
dataset = DATASETS['tldrs']


def drop_tldrs_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists tldrs')
        connection.commit()


def test_copy_json_to_tldrs():
    drop_tldrs_table()
    insert_dataset('tldrs', test_dir,connection)
    check_tldrs_count(1000)
    connection.close()


def check_tldrs_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from tldrs')
        papers = cursor.fetchall()
        assert len(papers) == i
