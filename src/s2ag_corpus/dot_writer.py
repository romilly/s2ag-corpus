from collections import defaultdict
from typing import List, Tuple, Set
from s2ag_corpus.paper import Paper


def shorten(title: List[str]) -> str:
    first_line_words = title[0].split(' ')
    return ' '.join(first_line_words[:3])


def write_dot_file(enriched_links: Set[Tuple[Paper, Paper]], file_path: str):
    with open(file_path, "w") as dot_file:
        dot_file.write("digraph {\n")
        dot_file.write("     rankdir=BT;\n")
        papers = set()
        clusters = defaultdict(list)
        # TODO: I sense an emerging class <clustered_structure> containing papers and clusters
        for p1, p2 in enriched_links:
            papers.add(p1)
            clusters[p1.year].append(p1.corpusid)
            papers.add(p2)
            clusters[p2.year].append(p2.corpusid)

        for paper in papers:
            title = wrap_text(paper.title, 50)
            st = shorten(title) # short title
            # mlt = '\n'.join(title) # multi-line title
            hover = f"title: {paper.title} \\nauthors: {paper.authors}\\npublished: {paper.year}"
            node_spec = f'[label="{st} ...", shape="rectangle", href="{paper.url}", target="_blank", tooltip="{hover}"]'
            dot_file.write(f'    "{paper.corpusid}" {node_spec};\n')

        for i, cluster in enumerate(sorted(clusters.keys())):
            dot_file.write(f"     subgraph cluster_{i} "+"{\n")
            dot_file.write(f"           rank=same;\n")
            dot_file.write(f'           label="{cluster}";\n')
            for corpusid in clusters[cluster]:
                dot_file.write(f"      {corpusid};\n")
            dot_file.write("     }")


        # Add edges
        for p1, p2 in enriched_links:
            dot_file.write(f'    "{p2.corpusid}" -> "{p1.corpusid}";\n')

        dot_file.write("}\n")


def wrap_text(text: str, max_length: int) -> List[str]:
    words = text.split()
    current_line = ""
    lines = []

    for word in words:
        # If adding the next word would exceed the max_length
        if len(current_line) + len(word) + 1 > max_length:
            # If the current line is not empty, save it
            if current_line:
                lines.append(current_line.strip())
                current_line = ""

        # If the word itself is longer than max_length, put it on a new line
        if len(word) > max_length:
            if current_line:
                lines.append(current_line.strip())
                current_line = ""
            lines.append(word)
        else:
            # Otherwise, add the word to the current line
            current_line += word + " "

    # Add the last line if it's not empty
    if current_line:
        lines.append(current_line.strip())

    # Join the lines with newlines
    return lines

