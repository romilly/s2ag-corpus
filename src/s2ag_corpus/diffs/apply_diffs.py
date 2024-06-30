import gzip
import json

from s2ag_corpus.datasets import Dataset


def upsert(connection, dataset: Dataset, path_to_file):
    cursor = connection.cursor()
    with gzip.open(path_to_file, 'rt') as upsert_file:
        for (index, line) in enumerate(upsert_file):
            row = dataset.json_to_tuple(line)
            cursor.execute(dataset.upsert, row)
            if 0 == index % 10000:
                connection.commit()
        connection.commit()


def delete_rows(connection, dataset, path_to_file):
    cursor = connection.cursor()
    with gzip.open(path_to_file, 'rt') as upsert_file:
        for (index, line) in enumerate(upsert_file):
            key = json.loads(line)[dataset.primary_key]
            cursor.execute(dataset.delete_row, (key,))
            if 0 == index % 10000:
                connection.commit()
        connection.commit()






