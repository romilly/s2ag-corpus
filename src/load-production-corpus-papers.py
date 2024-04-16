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

def read_lines_from_file(file_path):
    """A generator function that reads a file line by line."""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def read_lad_from_file(file_path):
    for line in read_lines_from_file(file_path):
        lad = (line, json.loads(line))
        yield  lad

def read_records_from_file(file_path):
    for line, jd in read_lad_from_file(file_path):
        record = (jd['corpusid'], line.strip())
        yield record


for filename in sorted(os.listdir(papers_dir)):
    # if filename.startswith("file"):
    if filename == "file":
        print(f"processing: {filename}")
        transfer_file = f"{papers_dir}/transfer.csv"
        with open(transfer_file,'w') as csvf:
            writer = csv.writer(csvf, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
            count = 0
            for record in read_records_from_file(f"{papers_dir}{filename}"):
                writer.writerow(record)
                count += 1
                if 0 == count%10000:
                    print(count)
        with open(transfer_file,'r') as csvf:
            with connection.cursor() as cursor:
                cursor.copy_from(csvf, 'papers', sep=',', null='')
            connection.commit()
print('done')



