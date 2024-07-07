import pytest
from s2ag_corpus.citation_graphs.dot_file import generate_dot_file

sha = 'a2266a06e752df98615787746599dc81440c0ae1'
dot_file = 'test/s2ag_corpus/data/generated/code-gen.dot'


def read(dot_file):
    with open(dot_file, 'r') as f:
        return f.read()


@pytest.mark.skip(reason="Requires a populated production database!")
def test_small_citation_graph():
    generate_dot_file(sha, dot_file, influential=False, show_labels=True)
    dot_contents = read(dot_file)
    for text in [
        'digraph Citations {',
        'rankdir=BT;',
        '268040009',
        'label="Unveiling Mechanistic Complexity ..."',
        'subgraph cluster_0 {',
        '"267446961" -> "249710437";',
        ]:
        assert text in dot_contents
