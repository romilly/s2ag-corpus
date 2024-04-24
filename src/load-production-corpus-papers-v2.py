#!/usr/bin/env python
# coding: utf-8


import os
import json
import csv
from io import StringIO

from dotenv import load_dotenv

from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS


load_dotenv()
base_dir = os.getenv("BASE_DIR")


from s2ag_corpus.database_catalogue import production_connection

connection = production_connection()

release_id = '2024-04-02'
papers_dir = f"{base_dir}/{release_id}/papers/"


with connection.cursor() as cursor:
    cursor.execute(CREATE_PAPERS_TABLE_WITHOUT_KEYS)

def read_records_from_file(file_path):
    """A generator function that returns reformatted lines in a file."""
    output = StringIO()
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            jd = json.loads(line)
            record = (jd['corpusid'], line)
            output.seek(0)
            output.truncate(0)
            writer.writerow(record)
            yield output.getvalue()


class GeneratorFileAdapter:
    def __init__(self, generator):
        self.generator = generator
        self.buffer = ''
        self.count = 0

    def read(self, size=-1):
        # Fill the buffer to meet the size requirement or if size is -1 then try to exhaust the generator
        while (size < 0 or len(self.buffer) < size) and (chunk := next(self.generator, None)) is not None:
            self.buffer += chunk
            if not self.buffer.endswith('\n'):
                self.buffer += '\n'  # Ensure each chunk ends with a newline

        if size < 0 or len(self.buffer) <= size:
            to_return, self.buffer = self.buffer, ''
        else:
            to_return, self.buffer = self.buffer[:size], self.buffer[size:]

        return to_return



def copy_json_to_papers(source_file):
    print(f'starting {source_file}')
    adapter = GeneratorFileAdapter(read_records_from_file(source_file))
    with connection.cursor() as cursor:
        cursor.copy_from(adapter, 'papers', sep=',', null='')
        connection.commit()
    print(f'done {source_file}')


for source_file in papers_dir:
    copy_json_to_papers(os.path.join(papers_dir, source_file))


with connection.cursor() as cursor:
    cursor.execute(ADD_KEY_TO_PAPERS)

