#!/usr/bin/env python
# coding: utf-8
import gzip
import os
import json
import csv
from io import StringIO

from dotenv import load_dotenv

from s2ag_corpus.datasets import Dataset
from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS

load_dotenv()
base_dir = os.getenv("BASE_DIR")


class JsonFileInserter:
    class JsonFileInserter:
        """
        This class is responsible for inserting the data in a dataset from a JSON file into a database table.

        Methods
        -------
        __init__(self, dataset: Dataset, connection)
            Initializes the JsonFileInserter with the provided dataset and database connection.

        read_records_from_file(self, input_file)
            Iterates over the lines (records) in a input_file, converts them into the expected tuple format, and yields each line.

        read(self, size=-1)
            Reads 'size' amount of data from the buffer, filling it up from the generator if necessary.

        copy_json_to_table(self, file_path)
            Copies data from a JSON file specified by file_path into a database table.

        create_table(self)
            Creates a new table in the database using the dataset's create table specification.

        index_table(self)
            Adds indices to the table in the database using the dataset's index specification.
        """
    def __init__(self, dataset: Dataset, connection):
        self.connection = connection
        self.dataset = dataset
        self.generator = None
        self.buffer = ''
        self.count = 0

    def read_records_from_file(self, input_file):
        """A generator function that returns reformatted lines in a file."""
        output = StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        for line in input_file:
            line = line.strip()
            record = self.dataset.json_to_tuple(line)
            output.seek(0)
            output.truncate(0)
            writer.writerow(record)
            self.count += 1
            if self.count % 1000000 == 0:
                print('loaded', self.count)
            yield output.getvalue()

    def read(self, size=-1):
        # Fill the buffer to meet the size requirement or if size is -1 then try to exhaust the generator
        while (size < 0 or len(self.buffer) < size) and (chunk := next(self.generator, None)) is not None:
            self.buffer += chunk
        if size < 0 or len(self.buffer) <= size:
            to_return, self.buffer = self.buffer, ''
        else:
            to_return, self.buffer = self.buffer[:size], self.buffer[size:]
        return to_return

    def copy_json_to_table(self, file_path):
        print("Copying json file to table", file_path)
        if file_path.endswith('.gz'):
            input_file = gzip.open(file_path, 'rt')
        else:
            input_file = open(file_path,'rt')
        with input_file:
            self.generator = self.read_records_from_file(input_file)
            with self.connection.cursor() as cursor:
                cursor.copy_from(self, self.dataset.table, sep=',', null='')
                self.connection.commit()
        print('done')

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.dataset.create_table)
            self.connection.commit()

    def index_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.dataset.add_indices)
            self.connection.commit()
        print('done indexing')


