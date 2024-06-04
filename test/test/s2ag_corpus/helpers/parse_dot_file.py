import pydot

from s2ag_corpus.citation_graphs.citation import Citation


def parse_dot_file(dot_file):
    # Parse the DOT file using pydot
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]  # Assume the DOT file contains one graph

    # Create a mapping from node names to labels (citation IDs)
    node_label_map = {}
    for node in graph.get_nodes():
        name = node.get_name()
        label = node.get_attributes().get('label', name)
        label = label.strip('"')  # Remove any surrounding quotes
        node_label_map[name] = int(label)  # Assuming labels are integers

    citations = []

    for edge in graph.get_edges():
        citing_name = edge.get_source()
        cited_name = edge.get_destination()
        citing_id = node_label_map[citing_name]
        cited_id = node_label_map[cited_name]
        label = edge.get_attributes().get('label', '')
        is_influential = len(label) > 0  # Non-empty label indicates influential

        citation = Citation(
            citing_corpus_id=citing_id,
            cited_corpus_id=cited_id,
            is_influential=is_influential
        )
        citations.append(citation)

    return citations