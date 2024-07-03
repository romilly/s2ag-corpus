from collections import defaultdict
from typing import List, Tuple, Set
from dataclasses import dataclass, field
from s2ag_corpus.helpers.paper import Paper


@dataclass(frozen=True)
class ClusteredPapers:
    papers: Set[Paper] = field(default_factory=set)
    clusters: defaultdict[int, List[int]] = field(default_factory=lambda: defaultdict(list))

    def add_paper(self, paper: Paper) -> None:
        self.papers.add(paper)
        year = paper.year if paper.year is not None else 'Unknown'
        self.clusters[year].append(paper.corpusid)


def shorten(title: List[str]) -> str:
    first_line_words = title[0].split(' ')
    return ' '.join(first_line_words[:3])


def write_dot_file(enriched_links: Set[Tuple[Paper, Paper]],
                   file_path: str,
                   show_labels: bool = False) -> None:
    with open(file_path, "w") as dot_file:
        dot_file.write("digraph Citations {\n")
        dot_file.write("     rankdir=BT;\n")
        cp = ClusteredPapers()
        for p1, p2 in enriched_links:
            cp.add_paper(p1)
            cp.add_paper(p2)

        for paper in cp.papers:
            title = wrap_text(paper.title, 50)
            year = paper.year if paper.year is not None else 'Unknown'
            st = shorten(title) if show_labels else '' # short title if wanted
            wt = '\n'.join(wrap_text(paper.title, 80))
            hover = f"title: {wt} \\nauthors: {paper.authors}\\npublished: {year}"
            shape = "rectangle" if show_labels else "circle"
            node_spec = f'[label="{st} ...", shape={shape}, href="{paper.url}", target="_blank", tooltip="{hover}"]'
            dot_file.write(f'    "{paper.corpusid}" {node_spec};\n')

        for i, cluster in enumerate(sorted(cp.clusters.keys())):
            dot_file.write(f"     subgraph cluster_{i} "+"{\n")
            dot_file.write(f"           rank=same;\n")
            dot_file.write(f'           label="{cluster}";\n')
            for corpusid in cp.clusters[cluster]:
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

