#!/usr/bin/env python
# coding: utf-8


import json
import csv
import os
from s2ag_corpus.database_catalogue import CorpusDatabaseCatalogue
from s2ag_corpus.database_catalogue import production_connection

from dotenv import load_dotenv
load_dotenv()
base_dir = os.getenv("BASE_DIR")

connection = production_connection()
catalogue = CorpusDatabaseCatalogue(connection)

release_id = '2024-04-02'
papers_dir = f"{base_dir}/{release_id}/papers/"

for filename in sorted(os.listdir(papers_dir)):
    if filename.startswith("file"):
        print(f"processing: {filename}")
        with open(base_dir + f"{papers_dir}{filename}") as f:
            jason_dictionaries = [(line, json.loads(line)) for line in f.readlines()]
            records = [(jd['corpusid'], line.strip()) for  line, jd in jason_dictionaries]
            with open(base_dir+'/2024-04-02/papers/transfer.csv','w') as csvf:
                writer = csv.writer(csvf, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
                for record in records:
                    writer.writerow(record)

        with open(base_dir+'/2024-04-02/papers/transfer.csv','r') as csvf:
            with connection.cursor() as cursor:
                cursor.copy_from(csvf, 'papers', sep=',', null='')
            connection.commit()

print('done')



