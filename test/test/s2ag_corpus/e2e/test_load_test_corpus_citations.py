import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.import_dataset import insert_dataset

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_dir = base_dir+'/test-data/e2e'
dataset = DATASETS['papers']


def drop_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists citations')
        connection.commit()


def test_copy_json_to_papers():
    drop_table()
    insert_dataset('citations', test_dir,connection)
    check_papers_count(21000)
    connection.close()


def check_papers_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from citations')
        papers = cursor.fetchall()
        assert len(papers) == i
