from s2ag_corpus.citation_graphs.find_links import CitationGraph
from test.test.s2ag_corpus.helpers.parse_dot_file import parse_dot_file

from test.test.s2ag_corpus.helpers.mock_catalogue import MockCatalogue

def test_finds_direct_citations():
    catalogue = MockCatalogue()
    catalogue.create_citation(2, 1, True)
    cg = CitationGraph(catalogue)
    links = cg.find_links(1)
    assert len(links) == 1


def test_influential_citations():
    catalogue = MockCatalogue()
    citations = parse_dot_file("test/s2ag_corpus/data/citations-01.dot")
    catalogue.add_citations(*citations)
    cg = CitationGraph(catalogue)
    links = cg.find_links(1, influential=True)
    assert len(links) == 2
    assert links == {(1, 3), (1, 4)}
    links = cg.find_links(1, influential=False)
    assert len(links) == 7
    assert links == {(1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (2, 6), (3, 6)}



