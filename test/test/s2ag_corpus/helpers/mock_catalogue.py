from collections import defaultdict
from typing import List, Tuple

from s2ag_corpus.citation_graphs.citation import Citation
from s2ag_corpus.database_catalogue import Catalogue


class MockCatalogue(Catalogue):
    def __init__(self):
        self.citations_dict: dict[int, List[Citation]] = defaultdict(list)
        self.references_dict: dict[int, List[Citation]] = defaultdict(list)

    def create_citation(self,
                     citing_corpus_id: int,
                     cited_corpus_id: int,
                     is_influential: bool):
        citation = Citation(citing_corpus_id, cited_corpus_id, is_influential)
        self.add_citations(citation)
        self.add_citations(citation)

    def add_citations(self, *citations: Citation):
        for citation in citations:
            self.citations_dict[citation.cited_corpus_id].append(citation)
            self.references_dict[citation.citing_corpus_id].append(citation)

    def find_citations_for(self, corpus_id: int, constraint: str = None) -> List[int]:
        return [citation.citing_corpus_id for citation in self.citations_dict[corpus_id]
                if citation.is_influential or len(constraint) == 0]

    def upsert(self, sql: str, data: List[Tuple]) -> None:
        pass

    def fetch(self, sql: str, params=None) -> List[Tuple]:
        pass