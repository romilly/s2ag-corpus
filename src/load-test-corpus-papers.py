#!/usr/bin/env python
# coding: utf-8


import json
import csv
from datetime import datetime

from s2ag_corpus.sql import INSERT_PAPER_SQL
from s2ag_corpus.database_catalogue import CorpusDatabaseCatalogue
from s2ag_corpus.database_catalogue import test_connection

base_dir = '/media/romilly/ss-corpus/2024-04-02/papers'
connection = test_connection()
catalogue = CorpusDatabaseCatalogue(test_connection())


def delete_papers_from_test_db():
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM papers')
        connection.commit()


delete_papers_from_test_db()

start = datetime.now()

with open(base_dir+'/first10000papers') as f:
    with connection.cursor() as cursor:
        for line in f:
            line = line.strip()
            # print(line)
            lj = json.loads(line)
            corpus_id = lj['corpusid']
            cursor.execute(INSERT_PAPER_SQL, (corpus_id, line))
            connection.commit()

end = datetime.now()
print('slowest:', end - start)
delete_papers_from_test_db()

start = datetime.now()


with open(base_dir+'/first10000papers') as f:
    with connection.cursor() as cursor:
        for line in f:
            line = line.strip()
            # print(line)
            lj = json.loads(line)
            corpus_id = lj['corpusid']
            cursor.execute(INSERT_PAPER_SQL, (corpus_id, line))
    connection.commit()

end = datetime.now()
print('commit at end:', end - start)

delete_papers_from_test_db()

start = datetime.now()

with open(base_dir + '/first10000papers') as f:
    jason_dictionaries = [(line, json.loads(line)) for line in f.readlines()]
    records = [(jd['corpusid'], line) for  line, jd in jason_dictionaries]
catalogue.upsert(INSERT_PAPER_SQL, records)

end = datetime.now()
print('upsert:', end - start)
delete_papers_from_test_db()


with open(base_dir + '/first10000papers') as f:
    jason_dictionaries = [(line, json.loads(line)) for line in f.readlines()]
    records = [(jd['corpusid'], line.strip()) for  line, jd in jason_dictionaries]
    with open(base_dir+'/first10000papers.csv','w') as csvf:
        writer = csv.writer(csvf, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        for record in records:
            writer.writerow(record)


delete_papers_from_test_db()

start = datetime.now()
with open(base_dir+'/first10000papers.csv','r') as csvf:
    with connection.cursor() as cursor:
        cursor.copy_from(csvf, 'papers', sep=',', null='')
    connection.commit()

end = datetime.now()
print('copy:', end - start)



