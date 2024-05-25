from dataclasses import dataclass

@dataclass(frozen=True)
class Paper:
    corpusid: int
    title: str
    authors: str
    year: int
    url: str
