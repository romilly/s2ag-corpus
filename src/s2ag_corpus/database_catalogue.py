from typing import List, Tuple

import psycopg2
from psycopg2.extras import execute_batch

from s2ag_corpus.parser import get_connection_string


def test_connection():
    return psycopg2.connect(
        get_connection_string('TEST_DB'))


def production_connection():
    return psycopg2.connect(
        get_connection_string('PROD_DB'))


class CorpusDatabaseCatalogue:
    def __init__(self, connection):
        self.connection = connection

    def fetch(self, sql: str, params=None) -> List[Tuple]:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def upsert(self, sql: str, data: List[Tuple]) -> None:
        with self.connection.cursor() as cursor:
            execute_batch(cursor, sql, data)
            self.connection.commit()
