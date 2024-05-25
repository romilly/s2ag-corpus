from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Tuple, Set, Optional

import psycopg2
from psycopg2.extras import execute_batch

from s2ag_corpus.parser import get_connection_string


def test_connection():
    return psycopg2.connect(
        get_connection_string('TEST_DB'))


def local_connection():
    return psycopg2.connect(
        get_connection_string('LOCAL_TEST_DB'))


def production_connection():
    return psycopg2.connect(
        get_connection_string('PROD_DB'))


@dataclass(frozen=True)
class Paper:
    corpusid: int
    title: str
    year: int
    url: str


class DatabaseCatalogue(ABC):
    @abstractmethod
    def fetch(self, sql: str, params=None) -> List[Tuple]:
        pass

    @abstractmethod
    def upsert(self, sql: str, data: List[Tuple]) -> None:
        pass


class CorpusDatabaseCatalogue(DatabaseCatalogue):
    CITATION_SQL = """
    select citingcorpusid from citations
                        where citedcorpusid = %s

                        """
    REFERENCE_SQL = """
    select citedcorpusid from citations
                        where citingcorpusid = %s
                        """
    PAPER_DETAILS_SQL="""
    select corpusid, 
    papers.paper_json->>'title' as title,
    papers.paper_json->> 'year',
    papers.paper_json->> 'url'
    from papers where corpusid = %s"""

    def __init__(self, connection):
        self.connection = connection

    def find_corpus_id_from(self, sha: str):
        rows = self.fetch("select corpusid from paperids where sha = %s", (sha,))
        if len(rows) == 0:
            return None
        else:
            return rows[0][0]

    def find_references_for(self, corpus_id: int, filter: str = None) -> List[int]:
        if filter is None:
            filter = ''
        rows = self.fetch(self.REFERENCE_SQL + filter, (corpus_id,))
        return [row[0] for row in rows]

    def find_citations_for(self, corpus_id: int, filter: str = None) -> List[int]:
        if filter is None:
            filter = ''
        rows = self.fetch(self.CITATION_SQL + filter, (corpus_id,))
        return [row[0] for row in rows]

    def transitive_closure(self, corpus_id: int) -> Set[int]:
        visited = set()
        to_visit = [corpus_id]

        while to_visit:
            current_id = to_visit.pop()
            if current_id not in visited:
                visited.add(current_id)
                citations = self.find_citations_for(current_id)
                for citation in citations:
                    if citation not in visited:
                        to_visit.append(citation)

        return visited

    def find_links(self, corpusid: int, influential=True) -> Set[Tuple[int, int]]:
        visited = set()
        to_visit = [corpusid]
        links = set()
        filter = 'and isinfluential = True' if influential else ''

        while to_visit:
            current_id = to_visit.pop()
            if current_id not in visited:
                visited.add(current_id)
                citations = self.find_citations_for(current_id, filter=filter)
                for citation in citations:
                    links.add((current_id, citation))
                    if citation not in visited:
                        to_visit.append(citation)

        return links

    def enriched_links(self, corpusid: int, influential = True) -> Set[Tuple[Paper, Paper]]:
        links = self.find_links(corpusid, influential)
        enriched = [(Paper(*self.find_paper_details(corpusid1)),
                     Paper(*self.find_paper_details(corpusid2)))
                            for (corpusid1, corpusid2) in links]
        return enriched

    def write_dot_file(self, enriched_links: Set[Tuple[Paper, Paper]], file_path: str):
        with open(file_path, "w") as f:
            f.write("digraph {\n")
            papers = set()
            # Add node definitions
            for p1, p2 in enriched_links:
                papers.add(p1)
                papers.add(p2)

            for paper in papers:
                label1 = f"{paper.title[:60]}\\n({paper.corpusid})\\n{p1.year}"
                f.write(f'    "{paper.corpusid}" [label="{label1}", shape="rectangle", URL="{paper.url}"];\n')

            # Add edges
            for p1, p2 in enriched_links:
                f.write(f'    "{p2.corpusid}" -> "{p1.corpusid}";\n')

            f.write("}\n")

    def find_paper_details(self, corpusid: int) -> tuple | None:
        rows = self.fetch(self.PAPER_DETAILS_SQL, (corpusid,))
        if len(rows) == 0:
            return None
        else:
            return rows[0]

    def fetch(self, sql: str, params=None) -> List[Tuple]:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def upsert(self, sql: str, data: List[Tuple]) -> None:
        with self.connection.cursor() as cursor:
            execute_batch(cursor, sql, data)
            self.connection.commit()

