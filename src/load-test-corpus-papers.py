#!/usr/bin/env python
# coding: utf-8


import json
import csv
import os
from s2ag_corpus.database_catalogue import CorpusDatabaseCatalogue
from s2ag_corpus.database_catalogue import test_connection

from dotenv import load_dotenv
load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = test_connection()
catalogue = CorpusDatabaseCatalogue(test_connection())


def delete_papers_from_test_db():
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM papers')
        connection.commit()


delete_papers_from_test_db()

with open(base_dir + '/papers/first10000papers') as f:
    jason_dictionaries = [(line, json.loads(line)) for line in f.readlines()]
    records = [(jd['corpusid'], line.strip()) for  line, jd in jason_dictionaries]
    with open(base_dir+'/papers/first10000papers.csv','w') as csvf:
        writer = csv.writer(csvf, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        for record in records:
            writer.writerow(record)

with open(base_dir+'/papers/first10000papers.csv','r') as csvf:
    with connection.cursor() as cursor:
        cursor.copy_from(csvf, 'papers', sep=',', null='')
    connection.commit()

print('done')



