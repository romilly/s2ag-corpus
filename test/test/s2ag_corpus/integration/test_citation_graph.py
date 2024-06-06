from s2ag_corpus.citation_graphs.dot_file import generate_dot_file

sha = '4747e72c5bc706c50e76953188f0144df18992d0'
dot_file = 'test/s2ag_corpus/data/generated/code-gen.dot'


def read(dot_file):
    with open(dot_file, 'r') as f:
        return f.read()


def test_small_citation_graph():
    generate_dot_file(sha, dot_file)
    dot_contents = read(dot_file)
    assert 'digraph {\n' in dot_contents
