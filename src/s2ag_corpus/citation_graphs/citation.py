from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    citing_corpus_id: int
    cited_corpus_id: int
    is_influential: bool