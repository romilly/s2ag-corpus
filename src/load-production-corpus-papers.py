#!/usr/bin/env python
# coding: utf-8


import os
import json
import csv
from io import StringIO

from dotenv import load_dotenv

from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.json_file_inserter import JsonFileInserter
from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS


load_dotenv()
base_dir = os.getenv("BASE_DIR")


from s2ag_corpus.database_catalogue import production_connection

connection = production_connection()

release_id = '2024-04-02'
papers_dir = f"{base_dir}/{release_id}/papers/"
dataset = DATASETS['papers']

with connection.cursor() as cursor:
    cursor.execute(CREATE_PAPERS_TABLE_WITHOUT_KEYS)
    connection.commit()


for source_file in sorted(os.listdir(papers_dir)):
    full_path = f"{papers_dir}/{source_file}"
    print(full_path)
    inserter = JsonFileInserter(dataset, connection)
    inserter.copy_json_to_table(full_path)


# with connection.cursor() as cursor:
#     cursor.execute(ADD_KEY_TO_PAPERS)
#     cursor.commit()

