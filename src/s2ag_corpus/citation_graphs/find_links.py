from typing import Set, Tuple

from s2ag_corpus.database.database_catalogue import Catalogue


class CitationGraph:
    def __init__(self, catalogue: Catalogue):
        self.catalogue = catalogue

    def find_links(self, corpusid: int, influential=True) -> Set[Tuple[int, int]]:
        visited = set()
        to_visit = [corpusid]
        links = set()
        constraint = 'and isinfluential = True' if influential else ''

        while to_visit:
            current_id = to_visit.pop()
            if current_id not in visited:
                visited.add(current_id)
                citations = self.catalogue.find_citations_for(current_id, constraint=constraint)
                for citation in citations:
                    links.add((current_id, citation))
                    if citation not in visited:
                        to_visit.append(citation)

        return links

