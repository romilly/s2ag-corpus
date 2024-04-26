import os
from dotenv import load_dotenv

from s2ag_corpus.database_catalogue import local_connection
from s2ag_corpus.load_test_corpus_papers_v7 import copy_json_to_papers

from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS

load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = local_connection()


test_file = base_dir+'/test-data/e2e/papers10'

def drop_and_replace_papers_table():
    with connection.cursor() as cursor:
        cursor.execute('drop table if exists papers')
        cursor.execute(CREATE_PAPERS_TABLE_WITHOUT_KEYS)
        connection.commit()


def test_copy_json_to_papers():
    drop_and_replace_papers_table()
    check_papers_count(0)
    copy_json_to_papers(test_file)
    check_papers_count(10)
    connection.close()


def check_papers_count(i):
    with connection.cursor() as cursor:
        cursor.execute('select * from papers')
        papers = cursor.fetchall()
        assert len(papers) == i
